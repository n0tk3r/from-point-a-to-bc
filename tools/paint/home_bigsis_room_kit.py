"""The Retreat's own painting kit (home_bigsis_room.py): the room is looked at through ONE camera, ray by ray.

Every pixel of the picture is a ray from the game's camera for this scene (room.View). What the ray meets
(floor, low wall, end wall, the great slope of the roof, a rafter, a book, a leaf) is found by measurement in the
room, in centimetres, and is then lit from where the lamps really are. So the roof's boards and rafters, the
floorboards and every piece of furniture share one eye, and every pool of light and every shadow has a place.

What is particular to this room and is provided for here:
  * a roof that is ONE slope (height = KNEE + RISE * Z): anything that lies on it or hangs under it is a box in
    "sheared" measurements (Y' = Y - RISE * Z), so rafters, skylight linings and trimmers are ordinary boxes;
  * boxes seen from INSIDE (a skylight's lining, the well of the hatch);
  * a second, thin sheet of paint for gauze (the canopy), laid over the room with the room showing through;
  * MANY SMALL LIGHTS: a lamp may be `local` (a bulb of a string of lights), worked out only near itself;
  * moonlight that comes through the two skylights and falls as their own shapes, soft-edged.

Room measurements as in room.py: X across, Y up, Z out from the far wall toward us. Nothing here touches the
shared library; nothing is imported from another painter's files."""

import math

import numpy as np

from brush import F32, rgb, lerp, blur

NEAR = 25.0
LUM = np.array([0.3, 0.55, 0.15], dtype=F32)


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


def mixc(a, b, t):
    return lerp(col(a), col(b), t)


# ---------------------------------------------------------------- noise that lies on the surfaces of the room
_T = np.random.default_rng(1907).random((256, 256)).astype(F32)
_TF = _T.reshape(-1)


def vnoise(u, v, seed=0):
    """Value noise, one blob per unit of (u, v). u and v are room measurements, so the pattern is foreshortened
    with the surface it lies on."""
    u = np.asarray(u, dtype=np.float64) + seed * 13.37
    v = np.asarray(v, dtype=np.float64) + seed * 5.91
    iu, iv = np.floor(u), np.floor(v)
    fu, fv = (u - iu).astype(F32), (v - iv).astype(F32)
    fu, fv = fu * fu * (3 - 2 * fu), fv * fv * (3 - 2 * fv)
    iu, iv = iu.astype(np.int64) & 255, iv.astype(np.int64) & 255
    iu1, iv1 = (iu + 1) & 255, (iv + 1) & 255
    a, b, c, d = _T[iv, iu], _T[iv, iu1], _T[iv1, iu], _T[iv1, iu1]
    return (a + (b - a) * fu) * (1 - fv) + (c + (d - c) * fu) * fv


def fbm(u, v, seed=0, octaves=3, gain=0.5):
    total, norm, w = 0.0, 0.0, 1.0
    for k in range(octaves):
        total = total + w * vnoise(u * (2 ** k), v * (2 ** k), seed + k * 3)
        norm += w
        w *= gain
    return (total / norm).astype(F32)


def hashf(i, seed=0):
    """A steady random number 0..1 for each whole number (which board, which book, which leaf)."""
    i = np.asarray(i).astype(np.int64)
    return _TF[((i * 73856093) ^ (seed * 19349663 + 83492791)) & 65535]


def grad_of(field):
    """How much a room measurement changes from one ray to the next."""
    gy, gx = np.gradient(field)
    return (np.sqrt(gx * gx + gy * gy) + 1e-6).astype(F32)


def lines_aa(coord, period, width, g, phase=0.0, fade=True):
    """Coverage of ruled lines at coord = phase + k * period, `width` rays wide, soft-edged; g = grad_of(coord).
    Lines too close together to be drawn fade into a tone."""
    f = (coord - phase) / period
    d = np.abs(f - np.round(f)) * period
    c = np.clip(width * 0.5 + 0.5 - d / g, 0, 1)
    if fade:
        c = c * np.clip((period / g - 1.6) / 2.4, 0.12, 1)
    return c.astype(F32)


def band(coord, lo, hi, g):
    """Coverage of lo <= coord <= hi, soft over one step g."""
    return (np.clip((coord - lo) / g + 0.5, 0, 1) * np.clip((hi - coord) / g + 0.5, 0, 1)).astype(F32)


def rect(u, v, u0, u1, v0, v1, g):
    return band(u, u0, u1, g) * band(v, v0, v1, g)


def disc(u, v, cu, cv, r, g):
    return np.clip((r - np.hypot(u - cu, v - cv)) / g + 0.5, 0, 1).astype(F32)


def lay(base, color, m):
    return base * (1 - m[..., None]) + col(color) * m[..., None]


def sstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0 + 1e-9), 0, 1)
    return t * t * (3 - 2 * t)


def curve3(points, steps=8):
    """A smooth line through a few places in the room."""
    p = [np.asarray(q, dtype=float) for q in points]
    p = [p[0] * 2 - p[1]] + p + [p[-1] * 2 - p[-2]]
    out = []
    for i in range(1, len(p) - 2):
        for s in range(steps):
            t = s / steps
            q = 0.5 * ((2 * p[i]) + (-p[i - 1] + p[i + 1]) * t + (2 * p[i - 1] - 5 * p[i] + 4 * p[i + 1] - p[i + 2]) * t * t
                       + (-p[i - 1] + 3 * p[i] - 3 * p[i + 1] + p[i + 2]) * t ** 3)
            out.append(tuple(float(v) for v in q))
    out.append(tuple(float(v) for v in p[-2]))
    return out


class Ctx:
    """What a paint is told about the places it has to color."""

    def __init__(self, **kw):
        self.__dict__.update(kw)


# ---------------------------------------------------------------- the stage: one ray per pixel (or four)
class Stage:
    def __init__(self, view, ss=1, size=(800, 600)):
        self.v, self.ss = view, ss
        self.W, self.H = size
        self.w, self.h = size[0] * ss, size[1] * ss
        py, px = np.mgrid[0:self.h, 0:self.w].astype(F32)
        a = ((px + 0.5) / ss - view.cx) / view.F
        u = (view.hz - (py + 0.5) / ss) / view.F
        self.dX = (a * view.rx + view.fx).astype(F32)
        self.dY = u.astype(F32)
        self.dZ = (a * view.rz + view.fz).astype(F32)
        for d in (self.dX, self.dY, self.dZ):
            d[np.abs(d) < 1e-7] = 1e-7
        self.C = (float(view.cam_x), float(view.eye), float(view.cam_z))
        self.names, self.groups = {"": 0}, {"back": 0}
        self.occ = []                    # boxes that throw shadows
        self.skip = set()                # groups left out of the picture (they still throw their shadows)
        self.feet = {}                   # name -> the floor it stands on (X0, X1, Z0, Z1)
        self.base = None
        self.gauze = None                # the veil, if the room has one
        self._fresh()

    def _fresh(self):
        h, w = self.h, self.w
        self.t = np.full((h, w), 1e9, dtype=F32)
        self.N = np.zeros((h, w, 3), dtype=F32)
        self.alb = np.zeros((h, w, 3), dtype=F32)
        self.emi = np.zeros((h, w, 3), dtype=F32)
        self.oid = np.zeros((h, w), dtype=np.int16)
        self.grp = np.zeros((h, w), dtype=np.int8)
        self.flag = np.zeros((h, w), dtype=np.uint8)      # 1 thin (lit from both sides)   2 no shadow falls on it
        self.alpha = np.zeros((h, w), dtype=F32)          # only used on a veil

    def veil(self):
        """A second sheet over the same rays, for thin cloth: what is put on it lets the room show through."""
        s = object.__new__(Stage)
        s.__dict__.update(self.__dict__)
        s._fresh()
        s.base = self
        return s

    # ---- names
    def nid(self, name):
        if name is None:
            return 0
        if name not in self.names:
            self.names[name] = len(self.names)
        return self.names[name]

    def gid(self, grp):
        if grp not in self.groups:
            self.groups[grp] = len(self.groups)
        return self.groups[grp]

    # ---- where on the picture a thing can be
    def _slice(self, pts, pad=2):
        v, ss = self.v, self.ss
        xs, ys = [], []
        for p in pts:
            a, u, d = v.cam_space(*p)
            if d < NEAR:
                return (slice(0, self.h), slice(0, self.w))
            k = v.F / d
            xs.append(v.cx + a * k)
            ys.append(v.hz - u * k)
        ax, bx = int(math.floor((min(xs) - pad) * ss)), int(math.ceil((max(xs) + pad) * ss))
        ay, by = int(math.floor((min(ys) - pad) * ss)), int(math.ceil((max(ys) + pad) * ss))
        ax, bx, ay, by = max(ax, 0), min(bx, self.w), max(ay, 0), min(by, self.h)
        if bx <= ax or by <= ay:
            return None
        return (slice(ay, by), slice(ax, bx))

    def _put(self, sl, vis, t, n, alb, emi, name, grp, flag, alpha=None):
        if not vis.any():
            return
        self.t[sl][vis] = t[vis] if isinstance(t, np.ndarray) else t
        if isinstance(n, np.ndarray) and n.ndim == 3:
            self.N[sl][vis] = n[vis]
        else:
            self.N[sl][vis] = np.asarray(n, dtype=F32)
        self.alb[sl][vis] = alb
        self.emi[sl][vis] = 0.0 if emi is None else emi
        self.oid[sl][vis] = self.nid(name)
        self.grp[sl][vis] = self.gid(grp)
        self.flag[sl][vis] = flag
        if alpha is not None:
            if self.base is not None:                              # a veil: layers of gauze add up
                old = self.alpha[sl][vis]
                self.alpha[sl][vis] = 1 - (1 - old) * (1 - alpha)
            else:
                self.alpha[sl][vis] = alpha

    def _mat(self, mat, vis, **kw):
        """A paint is one color, or a function of Ctx -> colors, or -> (colors, own light), or -> (colors, own light,
        which of the places are really there [cut paper, a leaf], and for a veil how thick it is there).
        -> (vis, colors, light, thickness)"""
        if not callable(mat):
            return vis, col(mat), None, None
        r = mat(Ctx(ss=self.ss, F=self.v.F, **kw))
        if not isinstance(r, tuple):
            return vis, r, None, None
        a = r[0]
        e = r[1] if len(r) > 1 else None
        keep = r[2] if len(r) > 2 else None
        thick = r[3] if len(r) > 3 else None
        if keep is not None and not np.all(keep):
            out = np.zeros(vis.shape, dtype=bool)
            out[vis] = keep
            a = a[keep] if isinstance(a, np.ndarray) and a.ndim == 2 else a
            e = e[keep] if isinstance(e, np.ndarray) and e.ndim == 2 else e
            thick = thick[keep] if isinstance(thick, np.ndarray) else thick
            vis = out
        return vis, a, e, thick

    # ---- boxes (upright, or lying on the slope of the roof, or seen from inside)
    def box(self, x0, x1, y0, y1, z0, z1, mat, name=None, grp="back", shadow=True, flag=0, emi=None, foot=False,
            shear=0.0, inside=False, alpha=None):
        """A box. With `shear` its Y measurements are heights BELOW/ABOVE the sloping line Y = shear * Z (so a
        rafter under the roof is a plain box). With `inside` we are looking into it (a lining, a well)."""
        if x1 < x0:
            x0, x1 = x1, x0
        if y1 < y0:
            y0, y1 = y1, y0
        if z1 < z0:
            z0, z1 = z1, z0
        if shadow and not inside:
            if shear:
                self.occ.append((x0, x1, y0 + shear * z0, y1 + shear * z1, z0, z1))
            else:
                self.occ.append((x0, x1, y0, y1, z0, z1))
        if foot and name:
            f = self.feet.get(name)
            self.feet[name] = (x0, x1, z0, z1) if f is None else (min(f[0], x0), max(f[1], x1), min(f[2], z0), max(f[3], z1))
        if grp in self.skip:
            return
        sl = self._slice([(x, y + shear * z, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)])
        if sl is None:
            return
        C = (self.C[0], self.C[1] - shear * self.C[2], self.C[2])
        dY = self.dY[sl] - shear * self.dZ[sl] if shear else self.dY[sl]
        if shear:
            dY = np.where(np.abs(dY) < 1e-7, 1e-7, dY)
        D = (self.dX[sl], dY, self.dZ[sl])
        lo, hi = (x0, y0, z0), (x1, y1, z1)
        tn = np.full(D[0].shape, -1e9, dtype=F32)
        tf = np.full(D[0].shape, 1e9, dtype=F32)
        fn = np.zeros(D[0].shape, dtype=np.int8)
        ff = np.zeros(D[0].shape, dtype=np.int8)
        for k in range(3):
            ta, tb = (lo[k] - C[k]) / D[k], (hi[k] - C[k]) / D[k]
            t0, t1 = np.minimum(ta, tb), np.maximum(ta, tb)
            later = t0 > tn
            fn[later] = k
            tn = np.where(later, t0, tn)
            sooner = t1 < tf
            ff[sooner] = k
            tf = np.where(sooner, t1, tf)
        if inside:
            th, face = tf, ff
            vis = (tn <= tf) & (tf > NEAR) & (tf < self.t[sl])
        else:
            th, face = tn, fn
            vis = (tn <= tf) & (tn > NEAR) & (tn < self.t[sl])
        if not vis.any():
            return
        names = (("left", "right"), ("bottom", "top"), ("back", "front"))
        q = math.sqrt(1 + shear * shear)
        for k in range(3):
            for sgn in (0, 1):                                   # sgn 1: the face on the high side of axis k
                hi_side = (D[k] > 0) if inside else (D[k] < 0)
                m = vis & (face == k) & (hi_side == bool(sgn))
                if not m.any():
                    continue
                s = 1.0 if sgn else -1.0
                n = [(s, 0.0, 0.0), (0.0, s / q, -s * shear / q), (0.0, 0.0, s)][k]
                if inside:
                    n = (-n[0], -n[1], -n[2])
                t = th[m]
                X, Z = self.C[0] + t * self.dX[sl][m], self.C[2] + t * self.dZ[sl][m]
                Y = self.C[1] + t * self.dY[sl][m]
                mm, a, e, _ = self._mat(mat, m, X=X, Y=Y, Z=Z, t=t, fp=t / self.v.F, face=names[k][sgn], n=n,
                                        box=(x0, x1, y0, y1, z0, z1), shear=shear, Yp=Y - shear * Z)
                self._put(sl, mm, th, n, a, e if e is not None else emi, name, grp, flag, alpha)

    # ---- flat pieces at any angle (a sheet of paper, a lid, a leaf, the board of the notice)
    def poly(self, pts, mat, name=None, grp="back", flag=0, emi=None, bias=0.0, alpha=None):
        """A flat convex piece. Its paint is told U, V: centimetres along its first edge and square to it.
        `bias` pulls it that many cm toward the lens (paper lying on something)."""
        if grp in self.skip:
            return
        sl = self._slice(pts)
        if sl is None:
            return
        P = [np.asarray(p, dtype=np.float64) for p in pts]
        e1 = P[1] - P[0]
        n = np.cross(e1, P[2] - P[0])
        ln = np.linalg.norm(n)
        if ln < 1e-9:
            return
        n = n / ln
        C = np.asarray(self.C, dtype=np.float64)
        if np.dot(n, C - P[0]) < 0:
            n = -n
        D = (self.dX[sl], self.dY[sl], self.dZ[sl])
        dn = n[0] * D[0] + n[1] * D[1] + n[2] * D[2]
        dn = np.where(np.abs(dn) < 1e-9, -1e-9, dn)
        t = (np.dot(n, P[0] - C) / dn).astype(F32)
        inside = (t > NEAR) & (t - bias < self.t[sl])
        if not inside.any():
            return
        X, Y, Z = C[0] + t * D[0], C[1] + t * D[1], C[2] + t * D[2]
        tot = np.zeros(3)
        for i in range(len(P)):
            tot += np.cross(P[i], P[(i + 1) % len(P)])
        turn = 1.0 if np.dot(tot, n) > 0 else -1.0
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            e = b - a
            cx = e[1] * (Z - a[2]) - e[2] * (Y - a[1])
            cy = e[2] * (X - a[0]) - e[0] * (Z - a[2])
            cz = e[0] * (Y - a[1]) - e[1] * (X - a[0])
            inside &= (cx * n[0] + cy * n[1] + cz * n[2]) * turn >= -1e-4
        vis = inside
        if not vis.any():
            return
        u1 = e1 / (np.linalg.norm(e1) + 1e-12)
        u2 = np.cross(n, u1)
        if np.dot(u2, P[-1] - P[0]) < 0:
            u2 = -u2
        Xv, Yv, Zv = X[vis] - P[0][0], Y[vis] - P[0][1], Z[vis] - P[0][2]
        U = (Xv * u1[0] + Yv * u1[1] + Zv * u1[2]).astype(F32)
        V = (Xv * u2[0] + Yv * u2[1] + Zv * u2[2]).astype(F32)
        nt = tuple(float(q) for q in n)
        vis, a, e, thick = self._mat(mat, vis, X=X[vis], Y=Y[vis], Z=Z[vis], U=U, V=V, t=t[vis], fp=t[vis] / self.v.F, face="flat", n=nt)
        self._put(sl, vis, t - bias, nt, a, e if e is not None else emi, name, grp, flag, thick if thick is not None else alpha)

    # ---- round things: a cylinder, or a tub or cone (r at a0, r1 at a1)
    def cyl(self, c, r, a0, a1, mat, axis="y", r1=None, name=None, grp="back", shadow=True, flag=0, emi=None,
            hollow=False, cap=None, alpha=None, foot=False, walls="both"):
        """c: the other two coordinates of its middle line: (X, Z) for "y", (Y, Z) for "x", (X, Y) for "z".
        hollow: open at the ends, the inside wall is seen. cap: paint of the flat ends (else the same paint)."""
        r1 = r if r1 is None else r1
        rm = max(r, r1)
        if axis == "y":
            lo, hi = (c[0] - rm, a0, c[1] - rm), (c[0] + rm, a1, c[1] + rm)
        elif axis == "x":
            lo, hi = (a0, c[0] - rm, c[1] - rm), (a1, c[0] + rm, c[1] + rm)
        else:
            lo, hi = (c[0] - rm, c[1] - rm, a0), (c[0] + rm, c[1] + rm, a1)
        ia = "xyz".index(axis)
        if shadow and axis == "y":
            self.occ.append(("c", c[0], c[1], (r + r1) / 2 * 0.96, a0, a1))
        elif shadow:
            k = 0.80
            m = [(lo[i] + hi[i]) / 2 for i in range(3)]
            o = [(m[i] - (m[i] - lo[i]) * (1 if i == ia else k), m[i] + (hi[i] - m[i]) * (1 if i == ia else k)) for i in range(3)]
            self.occ.append((o[0][0], o[0][1], o[1][0], o[1][1], o[2][0], o[2][1]))
        if foot and name and axis == "y":
            f = self.feet.get(name)
            g = (c[0] - r, c[0] + r, c[1] - r, c[1] + r)
            self.feet[name] = g if f is None else (min(f[0], g[0]), max(f[1], g[1]), min(f[2], g[2]), max(f[3], g[3]))
        if grp in self.skip:
            return
        sl = self._slice([(x, y, z) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
        if sl is None:
            return
        i1, i2 = [i for i in range(3) if i != ia]
        D = (self.dX[sl], self.dY[sl], self.dZ[sl])
        d1, d2, da = D[i1], D[i2], D[ia]
        o1, o2, oa = self.C[i1] - c[0], self.C[i2] - c[1], self.C[ia]
        s = (r1 - r) / (a1 - a0)
        R = r + s * (oa - a0)
        A = d1 * d1 + d2 * d2 - s * s * da * da
        B = 2 * (o1 * d1 + o2 * d2 - R * s * da)
        Cq = o1 * o1 + o2 * o2 - R * R
        A = np.where(np.abs(A) < 1e-12, 1e-12, A)
        disc_ = B * B - 4 * A * Cq
        ok = disc_ >= 0
        sq = np.sqrt(np.where(ok, disc_, 0))
        ta, tb = (-B - sq) / (2 * A), (-B + sq) / (2 * A)
        tA, tB = np.minimum(ta, tb), np.maximum(ta, tb)
        best = np.full(d1.shape, 1e9, dtype=F32)
        kind = np.zeros(d1.shape, dtype=np.int8)              # 1 outside wall, 2 inside wall, 3 end at a1, 4 end at a0
        for tt, kk in ((tA, 1), (tB, 2)):
            if (kk == 2 and not hollow) or (kk == 1 and walls == "far") or (kk == 2 and walls == "near"):
                continue
            aa = oa + tt * da
            m = ok & (tt > NEAR) & (aa >= a0) & (aa <= a1) & (tt < best)
            best = np.where(m, tt, best)
            kind[m] = kk
        if not hollow:
            for aend, rend, kk in ((a1, r1, 3), (a0, r, 4)):
                tc = (aend - oa) / da
                q1, q2 = o1 + tc * d1, o2 + tc * d2
                m = (tc > NEAR) & (q1 * q1 + q2 * q2 <= rend * rend) & (tc < best) & ((da < 0) == (kk == 3))
                best = np.where(m, tc, best)
                kind[m] = kk
        vis = (kind > 0) & (best < self.t[sl])
        if not vis.any():
            return
        t = best[vis]
        P = [self.C[i] + t * D[i][vis] for i in range(3)]
        q1, q2, qa = P[i1] - c[0], P[i2] - c[1], P[ia]
        rr = np.sqrt(q1 * q1 + q2 * q2) + 1e-6
        kd = kind[vis]
        n = np.zeros((len(t), 3), dtype=F32)
        wall = kd <= 2
        sg = np.where(kd == 2, -1.0, 1.0)
        nn = math.sqrt(1 + s * s)
        n[:, i1] = np.where(wall, sg * q1 / rr / nn, 0)
        n[:, i2] = np.where(wall, sg * q2 / rr / nn, 0)
        n[:, ia] = np.where(wall, -sg * s / nn, np.where(kd == 3, 1.0, -1.0))
        ang = np.arctan2(q2, q1).astype(F32)
        vis2, a, e, thick = self._mat(mat, vis, X=P[0], Y=P[1], Z=P[2], t=t, fp=t / self.v.F, face="round", kind=kd, ang=ang,
                                      along=(qa - a0).astype(F32), rad=rr.astype(F32), n=n)
        if vis2 is not vis:                                   # the paint cut some of it away
            keep = vis2[vis]
            n, kd, rr, ang, t = n[keep], kd[keep], rr[keep], ang[keep], t[keep]
            P = [p[keep] for p in P]
            vis = vis2
        if cap is not None and (kd >= 3).any():
            a = np.broadcast_to(np.asarray(a, dtype=F32), (len(kd), 3)).copy()
            capc = cap(Ctx(X=P[0], Y=P[1], Z=P[2], rad=rr, ang=ang, fp=t / self.v.F, kind=kd, ss=self.ss)) if callable(cap) else col(cap)
            a[kd >= 3] = capc[kd >= 3] if isinstance(capc, np.ndarray) and capc.ndim == 2 else capc
        full = np.zeros(vis.shape + (3,), dtype=F32)
        full[vis] = n
        self._put(sl, vis, best, full, a, e if e is not None else emi, name, grp, flag, thick if thick is not None else alpha)

    def ball(self, c, r, mat, name=None, grp="back", shadow=True, flag=0, emi=None, squash=(1.0, 1.0, 1.0), foot=False):
        """A ball, or with `squash` an egg / a cushion (radius r * squash along X, Y, Z)."""
        R = (r * squash[0], r * squash[1], r * squash[2])
        if shadow:
            self.occ.append(("c", c[0], c[2], math.sqrt(R[0] * R[2]) * 0.86, c[1] - R[1] * 0.78, c[1] + R[1] * 0.78))
        if foot and name:
            f = self.feet.get(name)
            g = (c[0] - R[0] * 0.8, c[0] + R[0] * 0.8, c[2] - R[2] * 0.8, c[2] + R[2] * 0.8)
            self.feet[name] = g if f is None else (min(f[0], g[0]), max(f[1], g[1]), min(f[2], g[2]), max(f[3], g[3]))
        if grp in self.skip:
            return
        sl = self._slice([(c[0] + i * R[0], c[1] + j * R[1], c[2] + k * R[2]) for i in (-1, 1) for j in (-1, 1) for k in (-1, 1)])
        if sl is None:
            return
        D = [self.dX[sl] / R[0], self.dY[sl] / R[1], self.dZ[sl] / R[2]]
        o = [(self.C[i] - c[i]) / R[i] for i in range(3)]
        A = D[0] ** 2 + D[1] ** 2 + D[2] ** 2
        B = 2 * (o[0] * D[0] + o[1] * D[1] + o[2] * D[2])
        Cq = o[0] ** 2 + o[1] ** 2 + o[2] ** 2 - 1.0
        dsc = B * B - 4 * A * Cq
        ok = dsc >= 0
        tt = (-B - np.sqrt(np.where(ok, dsc, 0))) / (2 * A)
        vis = ok & (tt > NEAR) & (tt < self.t[sl])
        if not vis.any():
            return
        t = tt[vis]
        P = [self.C[0] + t * self.dX[sl][vis], self.C[1] + t * self.dY[sl][vis], self.C[2] + t * self.dZ[sl][vis]]
        u = np.stack([(P[i] - c[i]) / R[i] for i in range(3)], axis=1)              # on the unit ball
        n = np.stack([u[:, i] / R[i] for i in range(3)], axis=1)
        n = (n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)).astype(F32)
        lon = np.arctan2(u[:, 0], u[:, 2]).astype(F32)
        lat = np.arcsin(np.clip(u[:, 1], -1, 1)).astype(F32)
        vis2, a, e, _ = self._mat(mat, vis, X=P[0], Y=P[1], Z=P[2], t=t, fp=t / self.v.F, face="ball", lon=lon, lat=lat, n=n, u=u)
        if vis2 is not vis:
            n = n[vis2[vis]]
            vis = vis2
        full = np.zeros(vis.shape + (3,), dtype=F32)
        full[vis] = n
        self._put(sl, vis, tt.astype(F32), full, a, e if e is not None else emi, name, grp, flag)

    # ---- thin things: cords, stems, legs, rails
    def stick(self, p, q, radius, mat, name=None, grp="back", flag=0, emi=None, min_px=0.55, r1=None, shade=True):
        """A round rod from p to q, `radius` cm thick (r1 at the far end, if it tapers): drawn by its outline on
        the picture, at its true depth, and shaded round."""
        if grp in self.skip:
            return
        v, ss = self.v, self.ss
        a0, u0, d0 = v.cam_space(*p)
        a1, u1, d1 = v.cam_space(*q)
        if d0 < NEAR or d1 < NEAR:
            return
        r1 = radius if r1 is None else r1
        k0, k1 = v.F / d0, v.F / d1
        x0, y0 = (v.cx + a0 * k0) * ss, (v.hz - u0 * k0) * ss
        x1, y1 = (v.cx + a1 * k1) * ss, (v.hz - u1 * k1) * ss
        w0, w1 = max(radius * k0 * ss, min_px * ss), max(r1 * k1 * ss, min_px * ss)
        pad = max(w0, w1) + 2
        ax, bx = int(math.floor(min(x0, x1) - pad)), int(math.ceil(max(x0, x1) + pad))
        ay, by = int(math.floor(min(y0, y1) - pad)), int(math.ceil(max(y0, y1) + pad))
        ax, bx, ay, by = max(ax, 0), min(bx, self.w), max(ay, 0), min(by, self.h)
        if bx <= ax or by <= ay:
            return
        sl = (slice(ay, by), slice(ax, bx))
        yy, xx = np.mgrid[ay:by, ax:bx].astype(F32)
        xx += 0.5
        yy += 0.5
        ex, ey = x1 - x0, y1 - y0
        L2 = ex * ex + ey * ey + 1e-9
        s = np.clip(((xx - x0) * ex + (yy - y0) * ey) / L2, 0, 1)
        dx, dy = xx - (x0 + s * ex), yy - (y0 + s * ey)
        dist = np.sqrt(dx * dx + dy * dy)
        wd = w0 + (w1 - w0) * s
        t = (1.0 / ((1 - s) / d0 + s / d1) - max(radius, r1)).astype(F32)
        vis = (dist <= wd) & (t < self.t[sl])
        if not vis.any():
            return
        side = ((dx * (-ey) + dy * ex) / math.sqrt(L2))[vis] / wd[vis]          # -1 .. 1 across the rod
        tv = t[vis]
        P = [self.C[0] + tv * self.dX[sl][vis], self.C[1] + tv * self.dY[sl][vis], self.C[2] + tv * self.dZ[sl][vis]]
        _, a, e, _ = self._mat(mat, vis, X=P[0], Y=P[1], Z=P[2], t=tv, fp=tv / v.F, face="rod", along=s[vis], side=side)
        a = np.broadcast_to(np.asarray(a, dtype=F32), (len(tv), 3))
        if shade:
            a = a * (0.74 + 0.32 * np.cos(side * 1.45))[:, None]
        ax3 = np.array([q[0] - p[0], q[1] - p[1], q[2] - p[2]], dtype=np.float64)
        ax3 /= np.linalg.norm(ax3) + 1e-12
        toc = np.array([self.C[0] - (p[0] + q[0]) / 2, self.C[1] - (p[1] + q[1]) / 2, self.C[2] - (p[2] + q[2]) / 2])
        toc -= ax3 * np.dot(toc, ax3)
        toc /= np.linalg.norm(toc) + 1e-12
        sidev = np.cross(ax3, toc)
        n = (toc[None, :] * np.sqrt(np.clip(1 - side * side, 0, 1))[:, None] + sidev[None, :] * side[:, None]).astype(F32)
        full = np.zeros(vis.shape + (3,), dtype=F32)
        full[vis] = n
        self._put(sl, vis, t, full, a, e if e is not None else emi, name, grp, flag)

    def rope(self, pts, radius, mat, **kw):
        for a, b in zip(pts[:-1], pts[1:]):
            self.stick(a, b, radius, mat, **kw)

    # ---- the shell of this room: floor, low far wall, two end walls, and the one great slope of the roof
    def room(self, W, knee, rise, mats, holes=None, grp="back"):
        """mats: {"floor", "far", "endL", "endR", "slope"}: paints, each told whole-picture fields (X, Y, Z, and
        S = centimetres up the slope from the far wall) for the patch of picture `m` that the surface fills.
        holes: {surface: function(X, Y, Z) -> True where there is an opening}."""
        C, dX, dY, dZ = self.C, self.dX, self.dY, self.dZ
        big = np.float32(1e9)

        def plane(num, den):
            with np.errstate(divide="ignore", invalid="ignore"):
                t = num / den
            return np.where((den < 0) & (t > 0), t, big).astype(F32)

        tF = plane(-C[1], dY)                                   # floor: inside while Y >= 0
        tB = plane(-C[2], dZ)                                   # far wall: Z >= 0
        tL = plane(-C[0], dX)                                   # left end wall: X >= 0
        tR = plane(-(W - C[0]), -dX)                            # right end wall: X <= W
        tS = plane(-(knee + rise * C[2] - C[1]), rise * dZ - dY)   # the roof: Y <= knee + rise * Z
        ts = np.stack([tF, tB, tL, tR, tS])
        which = ts.argmin(axis=0)
        t = ts.min(axis=0)
        q = math.sqrt(1 + rise * rise)
        normals = [(0, 1, 0), (0, 0, 1), (1, 0, 0), (-1, 0, 0), (0, -1 / q, rise / q)]
        keys = ["floor", "far", "endL", "endR", "slope"]
        for k, key in enumerate(keys):
            m = (which == k) & (t < self.t) & (t < 9e8)
            if not m.any():
                continue
            ys, xs = np.nonzero(m)
            sl = (slice(max(ys.min() - 2, 0), min(ys.max() + 3, self.h)), slice(max(xs.min() - 2, 0), min(xs.max() + 3, self.w)))
            ts_ = t[sl]
            X, Y, Z = C[0] + ts_ * dX[sl], C[1] + ts_ * dY[sl], C[2] + ts_ * dZ[sl]
            mm = m[sl].copy()
            if holes and key in holes:
                mm &= ~holes[key](X, Y, Z)
            r = mats[key](Ctx(m=mm, X=X, Y=Y, Z=Z, S=(Z * q).astype(F32), t=ts_, ss=self.ss, F=self.v.F, face=key, n=normals[k], fp=ts_ / self.v.F))
            a, e = r if isinstance(r, tuple) else (r, None)
            self._put(sl, mm, ts_, normals[k], a[mm] if isinstance(a, np.ndarray) and a.ndim == 3 else a,
                      (e[mm] if isinstance(e, np.ndarray) and e.ndim == 3 else e), key, grp, 0)

    # ---- where every ray has landed
    def places(self):
        t = np.minimum(self.t, 5e4)
        return self.C[0] + t * self.dX, self.C[1] + t * self.dY, self.C[2] + t * self.dZ

    def mask_of(self, *names):
        ids = [self.names[n] for n in names if n in self.names]
        return np.isin(self.oid, ids)

    def pick(self, a):
        o = self.ss // 2
        return a[o::self.ss, o::self.ss]

    def down(self, a):
        """Rays -> picture pixels (the mean of each pixel's rays)."""
        ss = self.ss
        if ss == 1:
            return a.astype(F32) if a.dtype != F32 else a
        h, w = self.h // ss, self.w // ss
        if a.ndim == 3:
            return a.reshape(h, ss, w, ss, a.shape[2]).mean(axis=(1, 3)).astype(F32)
        return a.astype(F32).reshape(h, ss, w, ss).mean(axis=(1, 3))


# ---------------------------------------------------------------- light
class Lamp:
    def __init__(self, pos, color, power, reach=120.0, aim=None, spread=None, soft=0.3, size=6.0, fill=0.0, shadows=True,
                 wrap=0.3, back=0.0, samples=6, local=None, gate=None, name="", core=0.35, ceil=None):
        """pos: where it is in the room. power: how bright a surface facing it is at `reach` cm.
        aim / spread / soft / back: a shaded lamp (cosine of the cone's half angle, softness of its edge, what still
        leaks out sideways). size: the lamp's own size in cm (how soft its shadows are). fill: light that reaches
        everything near it whichever way it faces. wrap: how far the light creeps round a form (soft light: more).
        local: a little light (a bulb on a string): worked out only within that many cm of itself, no shadows.
        gate: ("Y", at, x0, x1, z0, z1): the light only passes through this opening in the floor (the hatch).
        core: how gently the light gathers close to the lamp (bigger: no hot spot beside it).
        ceil: the light does not climb above this height in the room (it is shaded from the roof)."""
        self.pos, self.color, self.power, self.reach = np.asarray(pos, dtype=np.float64), col(color), power, reach
        self.aim = None if aim is None else np.asarray(aim, dtype=np.float64) / np.linalg.norm(aim)
        self.spread, self.soft, self.size, self.fill, self.shadows, self.wrap, self.back = spread, soft, size, fill, shadows, wrap, back
        self.samples, self.local, self.gate, self.name, self.core, self.ceil = samples, local, gate, name, core, ceil


def seg_hits(P, Q, occ):
    """For each place P: does the straight way to Q pass through any of the shadow-throwers?
    A thrower is a box (X0, X1, Y0, Y1, Z0, Z1) or an upright round thing ("c", X, Z, radius, Y0, Y1)."""
    D = [np.asarray(Q[i], dtype=F32) - P[i] for i in range(3)]
    inv = []
    for d in D:
        d = np.where(np.abs(d) < 1e-6, 1e-6, d)
        inv.append((1.0 / d).astype(F32))
    hit = np.zeros(P[0].shape, dtype=bool)
    a2 = None
    for o in occ:
        if o[0] == "c":
            _, cx, cz, r, y0, y1 = o
            if a2 is None:
                a2 = D[0] * D[0] + D[2] * D[2] + 1e-9
            ox, oz = P[0] - cx, P[2] - cz
            b = 2 * (ox * D[0] + oz * D[2])
            c = ox * ox + oz * oz - r * r
            dsc = b * b - 4 * a2 * c
            ok = dsc > 0
            sq = np.sqrt(np.where(ok, dsc, 0))
            s1 = np.maximum((-b - sq) / (2 * a2), 0.0)
            s2 = np.minimum((-b + sq) / (2 * a2), 1.0)
            ya, yb = P[1] + s1 * D[1], P[1] + s2 * D[1]
            hit |= ok & (s1 < s2) & (np.minimum(ya, yb) < y1) & (np.maximum(ya, yb) > y0)
            continue
        (x0, x1, y0, y1, z0, z1) = o
        lo, hi = (x0, y0, z0), (x1, y1, z1)
        ta, tb = (lo[0] - P[0]) * inv[0], (hi[0] - P[0]) * inv[0]
        tn, tf = np.minimum(ta, tb), np.maximum(ta, tb)
        ta, tb = (lo[1] - P[1]) * inv[1], (hi[1] - P[1]) * inv[1]
        tn, tf = np.maximum(tn, np.minimum(ta, tb)), np.minimum(tf, np.maximum(ta, tb))
        ta, tb = (lo[2] - P[2]) * inv[2], (hi[2] - P[2]) * inv[2]
        tn, tf = np.maximum(tn, np.minimum(ta, tb)), np.minimum(tf, np.maximum(ta, tb))
        hit |= (np.maximum(tn, 0.0) < np.minimum(tf, 1.0))
    return hit


def boxes_near(occ, pos, reach):
    """Only the shadow-throwers close enough to a lamp to matter to it."""
    out = []
    for b in occ:
        if b[0] == "c":
            b6 = (b[1] - b[3], b[1] + b[3], b[4], b[5], b[2] - b[3], b[2] + b[3])
        else:
            b6 = b
        dx = max(b6[0] - pos[0], 0, pos[0] - b6[1])
        dy = max(b6[2] - pos[1], 0, pos[1] - b6[3])
        dz = max(b6[4] - pos[2], 0, pos[2] - b6[5])
        if dx * dx + dy * dy + dz * dz < reach * reach:
            out.append(b)
    return out


class Moon:
    """Moonlight through openings in the slope of the roof (the skylights): it falls as their own shapes."""

    def __init__(self, toward, color, power, knee, rise, openings, soft=(3.0, 0.035), bars=None):
        """toward: the way to the moon from inside the room. openings: [(X0, X1, Z0, Z1)] on the slope.
        soft: (cm, and cm more for every cm the light has travelled): the patches' edges are soft.
        bars: function(which opening, u 0..1 across, v 0..1 up) -> 0..1 glass (for a glazing bar's shadow)."""
        m = np.asarray(toward, dtype=np.float64)
        self.dir = m / np.linalg.norm(m)
        self.color, self.power, self.knee, self.rise, self.openings, self.soft, self.bars = col(color), power, knee, rise, openings, soft, bars

    def through(self, P):
        """-> (how much of the moon each place sees through the glass 0..1, where its light crossed the roof)"""
        m = self.dir
        den = m[1] - self.rise * m[2]
        s = (self.knee + self.rise * P[2] - P[1]) / den
        Qx, Qz = P[0] + s * m[0], P[2] + s * m[2]
        w = self.soft[0] + np.clip(s, 0, 2000) * self.soft[1]
        g = np.zeros(P[0].shape, dtype=F32)
        for i, (x0, x1, z0, z1) in enumerate(self.openings):
            k = sstep(x0 - w, x0 + w, Qx) * sstep(x1 + w, x1 - w, Qx) * sstep(z0 - w, z0 + w, Qz) * sstep(z1 + w, z1 - w, Qz)
            if self.bars is not None:
                k = k * self.bars(i, (Qx - x0) / (x1 - x0), (Qz - z0) / (z1 - z0), w)
            g = np.maximum(g, k)
        return (g * (s > 1.0)).astype(F32), (Qx, P[1] + s * m[1], Qz)


def shade(st, lamps, ambient, moon=None, fast=False, seed=5, occ=None, expose=1.0, sh_step=1, skip_names=()):
    """Light every ray's landing place from the lamps (and the moon through the skylights). -> picture, light.
    Shadows are worked out once per picture pixel (or every `sh_step` pixels: soft light does not need more)."""
    occ = st.occ if occ is None else occ
    X, Y, Z = st.places()
    N = st.N
    ss = st.ss
    light = ambient(X, Y, Z, N).astype(F32)
    hit = st.t < 9e8
    thin = (st.flag & 1) > 0
    noshadow = (st.flag & 2) > 0
    rng = np.random.default_rng(seed)
    o, step = ss // 2, ss * sh_step
    Xs, Ys, Zs = X[o::step, o::step], Y[o::step, o::step], Z[o::step, o::step]
    Ns = N[o::step, o::step]
    hs = hit[o::step, o::step]
    Ps = (Xs + Ns[..., 0] * 0.8, Ys + Ns[..., 1] * 0.8, Zs + Ns[..., 2] * 0.8)

    def up(a):
        a = np.repeat(np.repeat(a, step, axis=0), step, axis=1) if step > 1 else a
        return a[:st.h, :st.w]

    v = st.v
    for lamp in lamps:
        if lamp.name in skip_names:
            continue
        if lamp.local:                                           # a little light: only its own neighbourhood
            a, u, d = v.cam_space(*lamp.pos)
            if d < NEAR:
                continue
            k = v.F / d
            cx, cy, rad = (v.cx + a * k) * ss, (v.hz - u * k) * ss, lamp.local * k * ss * 1.25 + 2
            ax, bx, ay, by = max(int(cx - rad), 0), min(int(cx + rad) + 1, st.w), max(int(cy - rad), 0), min(int(cy + rad) + 1, st.h)
            if bx <= ax or by <= ay:
                continue
            sl = (slice(ay, by), slice(ax, bx))
            Lx, Ly, Lz = lamp.pos[0] - X[sl], lamp.pos[1] - Y[sl], lamp.pos[2] - Z[sl]
            d2 = Lx * Lx + Ly * Ly + Lz * Lz + 1e-3
            dd = np.sqrt(d2)
            Nl = N[sl]
            ndl = (Nl[..., 0] * Lx + Nl[..., 1] * Ly + Nl[..., 2] * Lz) / dd
            ndl = np.where(thin[sl], np.abs(ndl) * 0.8 + 0.2, ndl)
            lam = np.clip((ndl + lamp.wrap) / (1 + lamp.wrap), 0, 1)
            win = np.clip(1 - d2 / (lamp.local * lamp.local), 0, 1) ** 2
            k_ = lam * win * lamp.power / (lamp.core + d2 / (lamp.reach * lamp.reach))
            light[sl] += k_[..., None] * lamp.color[None, None, :]
            continue
        Lx, Ly, Lz = (lamp.pos[0] - X), (lamp.pos[1] - Y), (lamp.pos[2] - Z)
        d2 = Lx * Lx + Ly * Ly + Lz * Lz + 1e-3
        d = np.sqrt(d2)
        ndl = (N[..., 0] * Lx + N[..., 1] * Ly + N[..., 2] * Lz) / d
        ndl = np.where(thin, np.abs(ndl) * 0.8 + 0.2, ndl)
        lam = np.clip((ndl + lamp.wrap) / (1 + lamp.wrap), 0, 1)
        fall = lamp.power / (lamp.core + d2 / (lamp.reach * lamp.reach))
        if lamp.aim is not None:
            ca = -(Lx * lamp.aim[0] + Ly * lamp.aim[1] + Lz * lamp.aim[2]) / d
            cone = np.clip((ca - lamp.spread) / lamp.soft + 0.5, 0, 1)
            cone = cone * cone * (3 - 2 * cone)
            fall = fall * (lamp.back + (1 - lamp.back) * cone)
        if lamp.ceil is not None:
            fall = fall * sstep(lamp.ceil + 50.0, lamp.ceil - 30.0, Y)
        if lamp.gate is not None:                                # light from below, coming up through the hatch
            _, at, gx0, gx1, gz0, gz1 = lamp.gate
            s = (at - Y) / np.where(np.abs(Ly) < 1e-4, 1e-4, Ly)
            qx, qz = X + s * Lx, Z + s * Lz
            wg = 5.0
            through = sstep(gx0 - wg, gx0 + wg, qx) * sstep(gx1 + wg, gx1 - wg, qx) * sstep(gz0 - wg, gz0 + wg, qz) * sstep(gz1 + wg, gz1 - wg, qz)
            fall = fall * np.where((s <= 0) | (s >= 1), 1.0, through)
        direct = lam * fall
        if lamp.shadows:
            ds = direct[o::step, o::step]
            act = (ds > 0.003) & hs
            vis = np.ones(act.shape, dtype=F32)
            if act.any():
                near = boxes_near(occ, lamp.pos, lamp.reach * 6.0)
                Pa = tuple(p[act] for p in Ps)
                n = 2 if fast else lamp.samples
                acc = np.zeros(Pa[0].shape, dtype=F32)
                for k in range(n):
                    j = rng.normal(0, 1, 3) * lamp.size * 0.7
                    Q = (lamp.pos[0] + j[0], lamp.pos[1] + j[1], lamp.pos[2] + j[2])
                    acc += np.where(seg_hits(Pa, Q, near), 0.0, 1.0).astype(F32)
                vis[act] = acc / n
            vis = blur(vis, (1.2 if lamp.size < 12 else 2.4) / sh_step + 0.4)
            vis = up(vis)
            vis = np.where(noshadow, 1.0, vis)
            direct = direct * vis
        light += (direct[..., None] * lamp.color[None, None, :]).astype(F32)
        if lamp.fill:
            light += ((lamp.fill * lamp.power / (0.6 + d2 / (lamp.reach * lamp.reach * 4)))[..., None] * lamp.color[None, None, :]).astype(F32)
    if moon is not None:
        m = moon.dir
        g, Q = moon.through(Ps)
        ndl = np.clip(Ns[..., 0] * m[0] + Ns[..., 1] * m[1] + Ns[..., 2] * m[2], 0, 1)
        act = (g * ndl > 0.004) & hs
        vis = np.zeros(act.shape, dtype=F32)
        if act.any():
            Pa = tuple(p[act] for p in Ps)
            Qa = tuple(q[act] for q in Q)
            if fast:
                vis[act] = np.where(seg_hits(Pa, Qa, occ), 0.0, 1.0)
            else:
                acc = np.zeros(Pa[0].shape, dtype=F32)
                for k in range(4):
                    j = rng.normal(0, 1, 3) * 5.0
                    acc += np.where(seg_hits(Pa, (Qa[0] + j[0], Qa[1] + j[1], Qa[2] + j[2]), occ), 0.0, 1.0)
                vis[act] = acc / 4
        vis = up(blur(vis * g, 1.0 / sh_step + 0.5))
        ndl_full = np.clip(N[..., 0] * m[0] + N[..., 1] * m[1] + N[..., 2] * m[2], 0, 1)
        ndl_full = np.where(thin, np.maximum(ndl_full, 0.5), ndl_full)
        st.moonlit = (vis * ndl_full).astype(F32)
        light += ((st.moonlit * moon.power)[..., None] * moon.color[None, None, :]).astype(F32)
    out = st.alb * light * expose + st.emi
    out = 1 - np.exp(-out * 1.1)                                        # a soft shoulder: nothing in this room is harsh
    out = np.where(hit[..., None], out, 0)
    return out.astype(F32), light


def floor_contact(X, Z, feet, reach=9.0, amount=0.45):
    """The floor darkens round the foot of everything that stands on it (so it sits, and does not float)."""
    dark = np.zeros(X.shape, dtype=F32)
    for (x0, x1, z0, z1) in feet:
        dx = np.maximum(np.maximum(x0 - X, X - x1), 0)
        dz = np.maximum(np.maximum(z0 - Z, Z - z1), 0)
        d = np.sqrt(dx * dx + dz * dz)
        dark = np.maximum(dark, np.exp(-d / reach) * (d > 0))
    return dark * amount

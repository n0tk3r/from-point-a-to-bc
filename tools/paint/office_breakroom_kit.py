"""The break room's own painting kit (office_breakroom.py): the room is looked at through ONE camera, ray by ray.
OFFICE-17D.

Every pixel of the picture is a ray from the game's camera for this scene (room.View). What the ray meets (the
floor, a wall, the ceiling, a box, a pie tin, a pot, a cushion) is found by measurement in the room, in centimetres,
and is then lit from where the light really comes from: the two fluorescent fittings in the ceiling (big soft lamps
that light downward), the snack machine's lit window, the hall's light through the door's glass, and the light that is
simply in the room.

It is the store's ray-caster (nevada_store_kit.py, itself the Retreat's) copied whole, as each room keeps its own kit,
so that a change for this room changes no other picture. A windowless room has no sun: the Sun is kept only because
`shade` takes one (this room passes None). Nothing here touches the shared library; nothing is imported from another
painter's files.

Room measurements as in room.py: X across, Y up, Z out from the back wall toward us."""

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
_T = np.random.default_rng(1979).random((256, 256)).astype(F32)
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
    """A steady random number 0..1 for each whole number (which tile, which hubcap, which bottle)."""
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
    """A picture's worth of rays (or a rectangle of it), and what each has met so far.

    ss: rays per pixel each way (2 for the finished picture: edges come out soft).
    rect: (x0, y0, x1, y1) in picture pixels, to paint only a patch (for the small frames)."""

    def __init__(self, view, ss=1, rect=None, size=(800, 600)):
        self.v, self.ss = view, ss
        self.W, self.H = size
        self.rect = rect or (0, 0, size[0], size[1])
        x0, y0, x1, y1 = self.rect
        self.w, self.h = (x1 - x0) * ss, (y1 - y0) * ss
        py, px = np.mgrid[0:self.h, 0:self.w].astype(F32)
        a = ((px + 0.5) / ss + x0 - view.cx) / view.F
        u = (view.hz - ((py + 0.5) / ss + y0)) / view.F
        self.dX = (a * view.rx + view.fx).astype(F32)
        self.dY = u.astype(F32)
        self.dZ = (a * view.rz + view.fz).astype(F32)
        for d in (self.dX, self.dY, self.dZ):
            d[np.abs(d) < 1e-7] = 1e-7
        self.C = (float(view.cam_x), float(view.eye), float(view.cam_z))
        self.names, self.groups = {"": 0}, {"back": 0}
        self.occ = []                    # boxes (and round things) that throw shadows
        self.skip = set()                # groups left out of the picture (they still throw their shadows)
        self.feet = {}                   # name -> the floor it stands on (X0, X1, Z0, Z1)
        self.t = np.full((self.h, self.w), 1e9, dtype=F32)
        self.N = np.zeros((self.h, self.w, 3), dtype=F32)
        self.alb = np.zeros((self.h, self.w, 3), dtype=F32)
        self.emi = np.zeros((self.h, self.w, 3), dtype=F32)
        self.oid = np.zeros((self.h, self.w), dtype=np.int16)
        self.grp = np.zeros((self.h, self.w), dtype=np.int8)
        self.flag = np.zeros((self.h, self.w), dtype=np.uint8)      # 1 thin (lit from both sides)   2 no shadow falls on it   4 outside (the sun's shadows do not apply)

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
        x0, y0 = self.rect[0], self.rect[1]
        ax, bx = int(math.floor((min(xs) - x0 - pad) * ss)), int(math.ceil((max(xs) - x0 + pad) * ss))
        ay, by = int(math.floor((min(ys) - y0 - pad) * ss)), int(math.ceil((max(ys) - y0 + pad) * ss))
        ax, bx, ay, by = max(ax, 0), min(bx, self.w), max(ay, 0), min(by, self.h)
        if bx <= ax or by <= ay:
            return None
        return (slice(ay, by), slice(ax, bx))

    def _put(self, sl, vis, t, n, alb, emi, name, grp, flag):
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

    def _mat(self, mat, vis, **kw):
        """A paint is one color, or a function of Ctx -> colors, or -> (colors, own light), or -> (colors, own light,
        which of the places are really there [cut paper, a leaf, the holes of a wire rack]). -> (vis, colors, light)"""
        if not callable(mat):
            return vis, col(mat), None
        r = mat(Ctx(ss=self.ss, F=self.v.F, **kw))
        if not isinstance(r, tuple):
            return vis, r, None
        a = r[0]
        e = r[1] if len(r) > 1 else None
        keep = r[2] if len(r) > 2 else None
        if keep is not None and not np.all(keep):
            out = np.zeros(vis.shape, dtype=bool)
            out[vis] = keep
            a = a[keep] if isinstance(a, np.ndarray) and a.ndim == 2 else a
            e = e[keep] if isinstance(e, np.ndarray) and e.ndim == 2 else e
            vis = out
        return vis, a, e

    # ---- boxes
    def box(self, x0, x1, y0, y1, z0, z1, mat, name=None, grp="back", shadow=True, flag=0, emi=None, foot=False, inside=False):
        """A box. With `inside` we are looking into it (a lining, the well of a bin)."""
        if x1 < x0:
            x0, x1 = x1, x0
        if y1 < y0:
            y0, y1 = y1, y0
        if z1 < z0:
            z0, z1 = z1, z0
        if shadow and not inside:
            self.occ.append((x0, x1, y0, y1, z0, z1))
        if foot and name:
            f = self.feet.get(name)
            self.feet[name] = (x0, x1, z0, z1) if f is None else (min(f[0], x0), max(f[1], x1), min(f[2], z0), max(f[3], z1))
        if grp in self.skip:
            return
        sl = self._slice([(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)])
        if sl is None:
            return
        C = self.C
        D = (self.dX[sl], self.dY[sl], self.dZ[sl])
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
        for k in range(3):
            for sgn in (0, 1):                                   # sgn 1: the face on the high side of axis k
                hi_side = (D[k] > 0) if inside else (D[k] < 0)
                m = vis & (face == k) & (hi_side == bool(sgn))
                if not m.any():
                    continue
                s = 1.0 if sgn else -1.0
                n = [(s, 0.0, 0.0), (0.0, s, 0.0), (0.0, 0.0, s)][k]
                if inside:
                    n = (-n[0], -n[1], -n[2])
                t = th[m]
                X, Y, Z = C[0] + t * D[0][m], C[1] + t * D[1][m], C[2] + t * D[2][m]
                mm, a, e = self._mat(mat, m, X=X, Y=Y, Z=Z, t=t, fp=t / self.v.F, face=names[k][sgn], n=n, box=(x0, x1, y0, y1, z0, z1))
                self._put(sl, mm, th, n, a, e if e is not None else emi, name, grp, flag)

    # ---- flat pieces at any angle (a card, a lid, a hubcap, a sheet of paper, a pane of glass)
    def poly(self, pts, mat, name=None, grp="back", flag=0, emi=None, bias=0.0, shadow=False):
        """A flat convex piece. Its paint is told U, V: centimetres along its first edge and square to it.
        `bias` pulls it that many cm toward the lens (paper lying on something)."""
        if shadow:
            xs, ys, zs = zip(*pts)
            self.occ.append((min(xs) - 0.5, max(xs) + 0.5, min(ys) - 0.5, max(ys) + 0.5, min(zs) - 0.5, max(zs) + 0.5))
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
        vis, a, e = self._mat(mat, vis, X=X[vis], Y=Y[vis], Z=Z[vis], U=U, V=V, t=t[vis], fp=t[vis] / self.v.F, face="flat", n=nt)
        self._put(sl, vis, t - bias, nt, a, e if e is not None else emi, name, grp, flag)

    def disc3(self, c, r, n, mat, sides=24, **kw):
        """A flat round piece: its middle, its radius, which way it faces (a hubcap, a lid, a plate). Its paint is told
        U, V: centimetres from the middle, U to the right and V up as one sees the disc from in front."""
        n = np.asarray(n, dtype=np.float64)
        n = n / np.linalg.norm(n)
        up = np.array([0.0, 1.0, 0.0]) if abs(n[1]) < 0.9 else np.array([0.0, 0.0, -1.0])
        right = np.cross(-n, up)
        right /= np.linalg.norm(right)
        upv = np.cross(right, -n)
        cx, cy, cz = c
        pts = [(cx + r * (right[0] * math.cos(q) + upv[0] * math.sin(q)), cy + r * (right[1] * math.cos(q) + upv[1] * math.sin(q)),
                cz + r * (right[2] * math.cos(q) + upv[2] * math.sin(q))) for q in np.linspace(0, 2 * math.pi, sides, endpoint=False)]

        def centred(cc):
            dx, dy, dz = cc.X - cx, cc.Y - cy, cc.Z - cz
            cc.U = (dx * right[0] + dy * right[1] + dz * right[2]).astype(F32)
            cc.V = (dx * upv[0] + dy * upv[1] + dz * upv[2]).astype(F32)
            return mat(cc) if callable(mat) else col(mat)
        self.poly(pts, centred, **kw)

    # ---- round things: a cylinder, or a tub or cone (r at a0, r1 at a1)
    def cyl(self, c, r, a0, a1, mat, axis="y", r1=None, name=None, grp="back", shadow=True, flag=0, emi=None,
            hollow=False, cap=None, foot=False, walls="both"):
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
        if foot and name and axis == "y":                       # OFFICE-17D: a round thing stands on a round foot
            self.feet[f"{name}#{len(self.feet)}"] = ("c", c[0], c[1], max(r, r1))
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
        vis2, a, e = self._mat(mat, vis, X=P[0], Y=P[1], Z=P[2], t=t, fp=t / self.v.F, face="round", kind=kd, ang=ang,
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
        self._put(sl, vis, best, full, a, e if e is not None else emi, name, grp, flag)

    def ball(self, c, r, mat, name=None, grp="back", shadow=True, flag=0, emi=None, squash=(1.0, 1.0, 1.0), foot=False):
        """A ball, or with `squash` an egg / a cushion / a hat's crown (radius r * squash along X, Y, Z)."""
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
        vis2, a, e = self._mat(mat, vis, X=P[0], Y=P[1], Z=P[2], t=t, fp=t / self.v.F, face="ball", lon=lon, lat=lat, n=n, u=u)
        if vis2 is not vis:
            n = n[vis2[vis]]
            vis = vis2
        full = np.zeros(vis.shape + (3,), dtype=F32)
        full[vis] = n
        self._put(sl, vis, tt.astype(F32), full, a, e if e is not None else emi, name, grp, flag)

    # ---- thin things: cords, wires, legs, rails, rabbit ears
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
        rx0, ry0 = self.rect[0], self.rect[1]
        x0, y0 = (v.cx + a0 * k0 - rx0) * ss, (v.hz - u0 * k0 - ry0) * ss
        x1, y1 = (v.cx + a1 * k1 - rx0) * ss, (v.hz - u1 * k1 - ry0) * ss
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
        _, a, e = self._mat(mat, vis, X=P[0], Y=P[1], Z=P[2], t=tv, fp=tv / v.F, face="rod", along=s[vis], side=side)
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

    # ---- the shell of this room: a floor, three walls and a flat ceiling, with openings
    def shell(self, W, H, mats, holes=None, grp="back", names=None):
        """mats: {"floor", "back", "left", "right", "ceiling"}: paints, each told whole-picture fields (X, Y, Z) for
        the patch of picture `m` that the surface fills. holes: {surface: function(X, Y, Z) -> True where there is
        an opening} (what is beyond is drawn afterwards, and shows through)."""
        C, dX, dY, dZ = self.C, self.dX, self.dY, self.dZ
        big = np.float32(1e9)

        def plane(num, den):
            with np.errstate(divide="ignore", invalid="ignore"):
                t = num / den
            return np.where((den < 0) & (t > 0), t, big).astype(F32)

        tF = plane(-C[1], dY)                                   # floor: inside while Y >= 0
        tB = plane(-C[2], dZ)                                   # back wall: Z >= 0
        tL = plane(-C[0], dX)                                   # left wall: X >= 0
        tR = plane(-(W - C[0]), -dX)                            # right wall: X <= W
        tC = plane(-(H - C[1]), -dY)                            # ceiling: Y <= H
        ts = np.stack([tF, tB, tL, tR, tC])
        which = ts.argmin(axis=0)
        t = ts.min(axis=0)
        normals = [(0, 1, 0), (0, 0, 1), (1, 0, 0), (-1, 0, 0), (0, -1, 0)]
        keys = ["floor", "back", "left", "right", "ceiling"]
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
            r = mats[key](Ctx(m=mm, X=X, Y=Y, Z=Z, t=ts_, ss=self.ss, F=self.v.F, face=key, n=normals[k], fp=ts_ / self.v.F))
            a, e = r if isinstance(r, tuple) else (r, None)
            self._put(sl, mm, ts_, normals[k], a[mm] if isinstance(a, np.ndarray) and a.ndim == 3 else a,
                      (e[mm] if isinstance(e, np.ndarray) and e.ndim == 3 else e), (names or {}).get(key, key), grp, 0)

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
                 wrap=0.3, back=0.0, samples=6, local=None, name="", core=0.35, inside_only=False):
        """pos: where it is in the room. power: how bright a surface facing it is at `reach` cm.
        aim / spread / soft / back: a shaded lamp (cosine of the cone's half angle, softness of its edge, what still
        leaks out sideways). size: the lamp's own size in cm (how soft its shadows are). fill: light that reaches
        everything near it whichever way it faces. wrap: how far the light creeps round a form (soft light: more).
        local: a little light (a bulb), worked out only within that many cm of itself, no shadows.
        core: how gently the light gathers close to the lamp (bigger: no hot spot beside it).
        inside_only: the lamp does not light what is outside the room (flag 4: the yard, the porch)."""
        self.pos, self.color, self.power, self.reach = np.asarray(pos, dtype=np.float64), col(color), power, reach
        self.aim = None if aim is None else np.asarray(aim, dtype=np.float64) / np.linalg.norm(aim)
        self.spread, self.soft, self.size, self.fill, self.shadows, self.wrap, self.back = spread, soft, size, fill, shadows, wrap, back
        self.samples, self.local, self.name, self.core, self.inside_only = samples, local, name, core, inside_only


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


class Sun:
    """The sun through openings in the walls: it falls as their own shapes, soft-edged, and every box in the room
    throws its shadow away from it."""

    def __init__(self, toward, color, power, openings, soft=(2.5, 0.03), bars=None, size=4.0):
        """toward: the way to the sun from inside the room. openings: [(axis, at, u0, u1, v0, v1)]: on the wall
        X = at (axis "X", u is Z) or Z = at (axis "Z", u is X), v is the height. soft: (cm, and cm more for every cm
        the light has travelled): the patches' edges are soft. bars: function(which opening, u, v, w) -> 0..1 glass.
        size: the sun's apparent size, for the softness of the furniture's shadows (cm of jitter)."""
        m = np.asarray(toward, dtype=np.float64)
        self.dir = m / np.linalg.norm(m)
        self.color, self.power, self.openings, self.soft, self.bars, self.size = col(color), power, openings, soft, bars, size

    def through(self, P):
        """-> (how much of the sun each place sees through the openings 0..1, where its light crossed the wall)"""
        m = self.dir
        g = np.zeros(P[0].shape, dtype=F32)
        Qx, Qy, Qz = P[0].copy(), P[1].copy(), P[2].copy()
        for i, (axis, at, u0, u1, v0, v1) in enumerate(self.openings):
            ia = 0 if axis == "X" else 2
            if abs(m[ia]) < 1e-6:
                continue
            s = (at - P[ia]) / m[ia]
            qx, qy, qz = P[0] + s * m[0], P[1] + s * m[1], P[2] + s * m[2]
            u = qz if axis == "X" else qx
            w = self.soft[0] + np.clip(s, 0, 3000) * self.soft[1]
            k = sstep(u0 - w, u0 + w, u) * sstep(u1 + w, u1 - w, u) * sstep(v0 - w, v0 + w, qy) * sstep(v1 + w, v1 - w, qy)
            k = k * (s > 1.0)
            if self.bars is not None:
                k = k * self.bars(i, (u - u0) / (u1 - u0), (qy - v0) / (v1 - v0), w)
            better = k > g
            Qx, Qy, Qz = np.where(better, qx, Qx), np.where(better, qy, Qy), np.where(better, qz, Qz)
            g = np.maximum(g, k)
        return g.astype(F32), (Qx.astype(F32), Qy.astype(F32), Qz.astype(F32))


def shade(st, lamps, ambient, sun=None, fast=False, seed=5, occ=None, expose=1.0, sh_step=1, skip_names=(), sun_occ=None):
    """Light every ray's landing place from the lamps and the sun. -> picture, light (rays x 3).
    Shadows are worked out once per picture pixel (or every `sh_step` pixels: soft light does not need more).
    What is outside the room (flag 4) gets the ambient's say and its own light (emi) only, from the lamps marked
    inside_only; the sun's patches do not fall there either (its light is painted into the outside already)."""
    occ = st.occ if occ is None else occ
    X, Y, Z = st.places()
    N = st.N
    ss = st.ss
    light = ambient(X, Y, Z, N, st).astype(F32)
    hit = st.t < 9e8
    thin = (st.flag & 1) > 0
    noshadow = (st.flag & 2) > 0
    outside = (st.flag & 4) > 0
    rng = np.random.default_rng(seed)
    o, step = ss // 2, ss * sh_step
    Xs, Ys, Zs = X[o::step, o::step], Y[o::step, o::step], Z[o::step, o::step]
    Ns = N[o::step, o::step]
    hs = hit[o::step, o::step] & ~outside[o::step, o::step]
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
            cx, cy, rad = (v.cx + a * k - st.rect[0]) * ss, (v.hz - u * k - st.rect[1]) * ss, lamp.local * k * ss * 1.25 + 2
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
            if lamp.inside_only:
                k_ = np.where(outside[sl], 0, k_)
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
        direct = lam * fall
        if lamp.inside_only:
            direct = np.where(outside, 0, direct)
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
            f = lamp.fill * lamp.power / (0.6 + d2 / (lamp.reach * lamp.reach * 4))
            if lamp.inside_only:
                f = np.where(outside, 0, f)
            light += (f[..., None] * lamp.color[None, None, :]).astype(F32)
    st.sunlit = np.zeros((st.h, st.w), dtype=F32)
    if sun is not None:
        m = sun.dir
        g, Q = sun.through(Ps)
        ndl = np.clip(Ns[..., 0] * m[0] + Ns[..., 1] * m[1] + Ns[..., 2] * m[2], 0, 1)
        act = (g * ndl > 0.004) & hs
        vis = np.zeros(act.shape, dtype=F32)
        if act.any():
            Pa = tuple(p[act] for p in Ps)
            Qa = tuple(q[act] for q in Q)
            so = occ if sun_occ is None else sun_occ
            if fast:
                vis[act] = np.where(seg_hits(Pa, Qa, so), 0.0, 1.0)
            else:
                acc = np.zeros(Pa[0].shape, dtype=F32)
                for k in range(4):
                    j = rng.normal(0, 1, 3) * sun.size
                    acc += np.where(seg_hits(Pa, (Qa[0] + j[0], Qa[1] + j[1], Qa[2] + j[2]), so), 0.0, 1.0)
                vis[act] = acc / 4
        vis = up(blur(vis * g, 1.0 / sh_step + 0.5))
        ndl_full = np.clip(N[..., 0] * m[0] + N[..., 1] * m[1] + N[..., 2] * m[2], 0, 1)
        ndl_full = np.where(thin, np.maximum(ndl_full, 0.5), ndl_full)
        st.sunlit = (vis * ndl_full).astype(F32)
        light += ((st.sunlit * sun.power)[..., None] * sun.color[None, None, :]).astype(F32)
    out = st.alb * light * expose + st.emi
    out = 1 - np.exp(-out * 1.1)                                        # a soft shoulder: the window is bright, not burnt
    out = np.where(hit[..., None], out, 0)
    return out.astype(F32), light


def floor_contact(X, Z, feet, reach=9.0, amount=0.45):
    """The floor darkens round the foot of everything that stands on it (so it sits, and does not float)."""
    dark = np.zeros(X.shape, dtype=F32)
    for f in feet:
        if f[0] == "c":                                        # OFFICE-17D: a round foot (a pedestal, a pot)
            _, cx, cz, r = f
            d = np.maximum(np.hypot(X - cx, Z - cz) - r, 0)
        else:
            x0, x1, z0, z1 = f
            dx = np.maximum(np.maximum(x0 - X, X - x1), 0)
            dz = np.maximum(np.maximum(z0 - Z, Z - z1), 0)
            d = np.sqrt(dx * dx + dz * dz)
        dark = np.maximum(dark, np.exp(-d / reach) * (d > 0))
    return dark * amount


# ---------------------------------------------------------------- lettering on cards, laid in the room's perspective
def text_card(lines, wide, high, res=8, ink=(40, 36, 60), paper=(244, 238, 220), size=None, font_px=None, lean=0.0, pad=0.08,
              marker=False, seed=0, align="centre", hand=False):
    """A few lines of capitals on a card -> a picture (float, high x wide, `res` pixels to the centimetre) and the
    card's size. The letters are set with Pillow's plain face (no typeface of anyone's), then roughened a little as
    a felt pen leaves them. `size` is the letter height in cm (defaults to fill the card)."""
    from PIL import Image, ImageDraw, ImageFont
    ss = 3
    Wp, Hp = int(round(wide * res)), int(round(high * res))
    im = Image.new("RGB", (Wp * ss, Hp * ss), paper)
    d = ImageDraw.Draw(im)
    n = len(lines)
    if size is None:
        size = min(high * (1 - 2 * pad) / (n * 1.35), 0.8 * wide / max(len(l) for l in lines) * 1.6)
    px = int(round(size * res * ss)) if font_px is None else int(font_px * res * ss)
    f = ImageFont.load_default(px)
    rng = np.random.default_rng(seed)
    gap = size * 1.3 * res * ss
    y = (Hp * ss - gap * n) / 2 + gap * 0.5
    for i, line in enumerate(lines):
        tw = d.textlength(line, font=f)
        if align == "centre":
            x = (Wp * ss - tw) / 2
        elif align == "left":
            x = pad * Wp * ss
        else:
            x = Wp * ss - tw - pad * Wp * ss
        x += rng.normal(0, 0.15) * res * ss * lean if lean else 0
        d.text((x, y), line, fill=ink, font=f, anchor="lm")
        if marker:                                                  # a felt pen: a second pass, a hair off, thickens the stroke
            d.text((x + 0.6 * ss, y + 0.4 * ss), line, fill=ink, font=f, anchor="lm")
        y += gap
    a = np.asarray(im.resize((Wp, Hp), Image.LANCZOS), dtype=F32) / 255
    return a, (wide, high)


def card_paint(tex, wide, high, base=None, shade=0.0, u0=0.0, v0=0.0, flip_v=True):
    """A paint for a flat piece (Stage.poly) that lays a text_card on it: U along, V up, in cm from the piece's
    first corner. Off the card, `base` (a colour, or None: cut away)."""
    tex = np.asarray(tex, dtype=F32)
    H_, W_ = tex.shape[:2]
    ru, rv = W_ / wide, H_ / high

    def f(c):
        u, v = c.U - u0, c.V - v0
        inside = (u >= 0) & (u < wide) & (v >= 0) & (v < high)
        tx = np.clip(u * ru, 0, W_ - 1.001)
        ty = np.clip((high - v) * rv if flip_v else v * rv, 0, H_ - 1.001)
        from brush import sample
        k = sample(tex, tx, ty)
        k = k * (1 - shade)
        if base is None:
            return k, None, inside
        out = np.where(inside[..., None], k, col(base)[None, :])
        return out
    return f


# ---------------------------------------------------------------- capitals, and letters laid through the camera
# The store's own capitals (its kit drew them for its cards), kept here for the break room's words: each letter a few
# pen strokes on a grid 4 wide and 6 high, the baseline at 0. Nobody's typeface. Laid with no wobble and a heavier pen
# they are the Office's printed notices; with a wobble, a felt pen's card. (OFFICE-17D: the middle dot added, below.)
PEN = {
    "A": [[(0, 0), (2, 6), (4, 0)], [(0.8, 2.2), (3.2, 2.2)]],
    "B": [[(0, 0), (0, 6), (2.7, 6), (3.6, 5.3), (3.6, 3.8), (2.7, 3.1), (0, 3.1)], [(2.7, 3.1), (3.9, 2.3), (3.9, 0.8), (2.9, 0), (0, 0)]],
    "C": [[(3.9, 5.0), (3.0, 6), (1.2, 6), (0, 4.8), (0, 1.2), (1.2, 0), (3.0, 0), (3.9, 1.0)]],
    "D": [[(0, 0), (0, 6), (2.3, 6), (3.7, 4.8), (4, 3), (3.7, 1.2), (2.3, 0), (0, 0)]],
    "E": [[(3.8, 6), (0, 6), (0, 0), (3.8, 0)], [(0, 3.1), (3.0, 3.1)]],
    "F": [[(3.8, 6), (0, 6), (0, 0)], [(0, 3.1), (3.0, 3.1)]],
    "G": [[(3.9, 5.0), (3.0, 6), (1.2, 6), (0, 4.8), (0, 1.2), (1.2, 0), (3.0, 0), (4, 1.0), (4, 2.7), (2.2, 2.7)]],
    "H": [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3.1), (4, 3.1)]],
    "I": [[(2, 0), (2, 6)], [(0.9, 6), (3.1, 6)], [(0.9, 0), (3.1, 0)]],
    "J": [[(1.2, 6), (3.6, 6)], [(2.8, 6), (2.8, 1.2), (1.9, 0), (0.8, 0.2), (0.1, 1.3)]],
    "K": [[(0, 0), (0, 6)], [(3.9, 6), (0.1, 2.4)], [(1.3, 3.5), (4, 0)]],
    "L": [[(0, 6), (0, 0), (3.7, 0)]],
    "M": [[(0, 0), (0, 6), (2, 2.4), (4, 6), (4, 0)]],
    "N": [[(0, 0), (0, 6), (4, 0), (4, 6)]],
    "O": [[(1.2, 0), (0.2, 1.1), (0, 3), (0.2, 4.9), (1.2, 6), (2.8, 6), (3.8, 4.9), (4, 3), (3.8, 1.1), (2.8, 0), (1.2, 0)]],
    "P": [[(0, 0), (0, 6), (2.8, 6), (3.9, 5.1), (3.9, 3.9), (2.8, 3), (0, 3)]],
    "Q": [[(1.2, 0), (0.2, 1.1), (0, 3), (0.2, 4.9), (1.2, 6), (2.8, 6), (3.8, 4.9), (4, 3), (3.8, 1.1), (2.8, 0), (1.2, 0)], [(2.4, 1.5), (4.2, -0.5)]],
    "R": [[(0, 0), (0, 6), (2.8, 6), (3.9, 5.2), (3.9, 3.9), (2.8, 3.1), (0, 3.1)], [(2.0, 3.1), (4, 0)]],
    "S": [[(3.9, 5.0), (3.1, 5.9), (2.0, 6), (0.9, 5.8), (0.2, 5.0), (0.3, 3.9), (1.2, 3.3), (2.8, 2.8), (3.8, 2.0), (3.8, 0.9), (2.9, 0.1), (1.8, 0), (0.8, 0.2), (0.0, 1.0)]],
    "T": [[(0, 6), (4, 6)], [(2, 6), (2, 0)]],
    "U": [[(0, 6), (0, 1.4), (0.8, 0.2), (2, 0), (3.2, 0.2), (4, 1.4), (4, 6)]],
    "V": [[(0, 6), (2, 0), (4, 6)]],
    "W": [[(0, 6), (0.9, 0), (2, 4.0), (3.1, 0), (4, 6)]],
    "X": [[(0, 6), (4, 0)], [(4, 6), (0, 0)]],
    "Y": [[(0, 6), (2, 3.1), (4, 6)], [(2, 3.1), (2, 0)]],
    "Z": [[(0, 6), (4, 6), (0, 0), (4, 0)]],
    "0": [[(1.2, 0), (0.2, 1.1), (0, 3), (0.2, 4.9), (1.2, 6), (2.8, 6), (3.8, 4.9), (4, 3), (3.8, 1.1), (2.8, 0), (1.2, 0)]],
    "1": [[(0.9, 4.6), (2.2, 6), (2.2, 0)], [(0.9, 0), (3.5, 0)]],
    "2": [[(0.2, 4.8), (1.2, 5.9), (2.8, 5.9), (3.8, 4.8), (3.6, 3.4), (0, 0), (4, 0)]],
    "3": [[(0.2, 5.4), (1.4, 6), (3.0, 6), (3.8, 5.0), (3.4, 3.6), (1.8, 3.2)], [(3.4, 3.4), (4, 2.0), (3.6, 0.6), (2.4, 0), (1.0, 0.1), (0, 0.9)]],
    "4": [[(3, 0), (3, 6), (0, 1.8), (4, 1.8)]],
    "5": [[(3.8, 6), (0.4, 6), (0.2, 3.4), (2.4, 3.6), (3.8, 2.6), (3.8, 0.9), (2.6, 0), (1.0, 0), (0, 0.8)]],
    "6": [[(3.4, 5.8), (2.0, 6), (0.6, 5.0), (0, 3), (0.2, 1.0), (1.4, 0), (2.8, 0), (3.9, 1.1), (3.7, 2.7), (2.4, 3.5), (1.0, 3.2), (0.1, 2.2)]],
    "7": [[(0, 6), (4, 6), (1.4, 0)]],
    "8": [[(2, 3.2), (0.6, 3.9), (0.4, 5.2), (1.3, 6), (2.7, 6), (3.6, 5.2), (3.4, 3.9), (2, 3.2), (0.3, 2.3), (0.1, 0.9), (1.2, 0), (2.8, 0), (3.9, 0.9), (3.7, 2.3), (2, 3.2)]],
    "9": [[(3.8, 3.4), (2.6, 2.6), (1.2, 2.7), (0.1, 3.7), (0.3, 5.2), (1.4, 6), (2.8, 6), (3.8, 5.0), (4, 3), (3.6, 1.0), (2.2, 0), (0.7, 0.3)]],
    "$": [[(3.6, 4.9), (2.8, 5.5), (1.2, 5.5), (0.3, 4.6), (0.6, 3.6), (2.0, 3.0), (3.4, 2.4), (3.7, 1.3), (2.8, 0.5), (1.2, 0.5), (0.2, 1.2)], [(2, 6.3), (2, -0.3)]],
    ":": [[(2, 1.0), (2, 0.4)], [(2, 4.2), (2, 3.6)]],
    ".": [[(2, 0.6), (2, 0.0)]],
    ",": [[(2.2, 0.6), (1.6, -1.0)]],
    "-": [[(0.8, 3), (3.2, 3)]],
    "(": [[(3.0, 6.4), (1.8, 5.2), (1.2, 3), (1.8, 0.8), (3.0, -0.4)]],
    ")": [[(1.0, 6.4), (2.2, 5.2), (2.8, 3), (2.2, 0.8), (1.0, -0.4)]],
    "!": [[(2, 6), (2, 1.8)], [(2, 0.5), (2, 0.0)]],
    "'": [[(2, 6), (1.8, 4.6)]],
    "?": [[(0.3, 5.0), (1.2, 6), (2.8, 6), (3.8, 5.0), (3.6, 3.8), (2, 2.8), (2, 1.8)], [(2, 0.5), (2, 0.0)]],
    "&": [[(4, 0), (1.0, 4.0), (1.0, 5.4), (1.8, 6), (2.8, 5.6), (2.8, 4.6), (0.4, 2.4), (0.4, 0.8), (1.4, 0), (2.6, 0.2), (4, 2.2)]],
    "/": [[(0.4, 0), (3.6, 6)]],
    "\u00b7": [[(2, 3.3), (2, 2.7)]],                                     # OFFICE-17D: the middle dot (LABEL YOUR LUNCH. \u00b7 MGMT.)
}
NARROW = {"I": 0.62, ".": 0.4, ":": 0.4, ",": 0.4, "'": 0.4, "!": 0.45, "(": 0.6, ")": 0.6, "1": 0.8, "-": 0.8, " ": 0.62, "\u00b7": 0.5}


def pen_width(line, cap, track=0.28, squeeze=1.0):
    """How wide a line of PEN capitals is, in the units of `cap` (the capitals' height)."""
    u = cap / 6.0
    return sum((4 * NARROW.get(ch, 1.0) * squeeze + 6 * track) * u for ch in line) - 6 * track * u


def pen_mask(lines, wide, high, cap, res=24, pen=0.16, track=0.28, lead=1.45, align="centre", seed=0, wobble=0.04, lean=0.0,
             top=None, squeeze=1.0, fit=True):
    """Lines of PEN capitals on a card -> a coverage mask (high x wide cm at `res` pixels to the cm, y down) and nothing
    else. cap: the letters' height in cm. pen: the stroke's width, a share of `cap`. lean: italic slope. Each letter is
    a hair off level and size, as a hand makes it. top: where the first line's caps start, cm from the card's top
    (else the block is centred)."""
    from PIL import Image, ImageDraw
    if fit:                                                              # a line too long for the card is narrowed, never cut
        widest = max(pen_width(l, cap, track, squeeze) for l in lines)
        if widest > wide * 0.96:
            squeeze = squeeze * (wide * 0.96 - 6 * track * cap / 6.0 * 0) / widest
    Wp, Hp = max(2, int(round(wide * res))), max(2, int(round(high * res)))
    im = Image.new("L", (Wp, Hp), 0)
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(seed)
    u = cap / 6.0
    wd = max(1, int(round(pen * cap * res)))
    block = cap * lead * (len(lines) - 1) + cap
    y0 = (high - block) / 2 if top is None else top
    for i, line in enumerate(lines):
        lw = pen_width(line, cap, track, squeeze)
        x = (wide - lw) / 2 if align == "centre" else (0.06 * wide if align == "left" else wide - lw - 0.06 * wide)
        base = y0 + cap + i * cap * lead                                 # the baseline, cm from the top
        for ch in line:
            k = NARROW.get(ch, 1.0) * squeeze
            if ch != " " and ch in PEN:
                sc = 1 + rng.normal(0, wobble)
                dy = rng.normal(0, wobble * 0.6) * cap
                for stroke in PEN[ch]:
                    pts = []
                    for px, py in stroke:
                        xx = x + ((px - 2) * k + 2 * k) * u * sc + py * u * lean
                        yy = base + dy - py * u * sc
                        pts.append((xx * res, yy * res))
                    if len(pts) == 1:
                        pts = pts * 2
                    d.line(pts, fill=255, width=wd, joint="curve")
                    for (qx, qy) in (pts[0], pts[-1]):
                        d.ellipse([qx - wd / 2, qy - wd / 2, qx + wd / 2, qy + wd / 2], fill=255)
            x += (4 * k + 6 * track) * u
    return np.asarray(im, dtype=F32) / 255


def homography(src, dst):
    """The 3x3 projective map taking the four points src to the four points dst."""
    A, b = [], []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        b += [u, v]
    h = np.linalg.solve(np.asarray(A, dtype=np.float64), np.asarray(b, dtype=np.float64))
    return np.append(h, 1.0).reshape(3, 3)


def lay_on(pic, view, quad, mask, ink, amount=1.0, sub=4, crisp=0.5, rect=None, grain=0.0, seed=0):
    """Lay a mask (a card's lettering, a label, a stripe) onto the picture through the camera: `quad` is the mask's
    four corners in the room (top left, top right, bottom right, bottom left, in cm), so the letters lie in the
    perspective of whatever they are on. Each pixel is sampled sub x sub times; with `crisp` the coverage is pushed
    to hard edges (letters 7 px high must stay letters). -> the coverage laid (picture size)."""
    H_, W_ = pic.shape[:2]
    ox, oy = (rect[0], rect[1]) if rect else (0, 0)
    P = [view.pt(*q) for q in quad]
    P = [(x - ox, y - oy) for x, y in P]
    mh, mw = mask.shape
    Hm = homography(P, [(0, 0), (mw, 0), (mw, mh), (0, mh)])
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    x0, x1 = max(int(math.floor(min(xs))) - 1, 0), min(int(math.ceil(max(xs))) + 1, W_)
    y0, y1 = max(int(math.floor(min(ys))) - 1, 0), min(int(math.ceil(max(ys))) + 1, H_)
    if x1 <= x0 or y1 <= y0:
        return np.zeros((H_, W_), dtype=F32)
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float64)
    cov = np.zeros(yy.shape, dtype=np.float64)
    for i in range(sub):
        for j in range(sub):
            px, py = xx + (i + 0.5) / sub, yy + (j + 0.5) / sub
            w = Hm[2, 0] * px + Hm[2, 1] * py + Hm[2, 2]
            u = (Hm[0, 0] * px + Hm[0, 1] * py + Hm[0, 2]) / w
            v = (Hm[1, 0] * px + Hm[1, 1] * py + Hm[1, 2]) / w
            inside = (u >= 0) & (u < mw - 1) & (v >= 0) & (v < mh - 1)
            ui, vi = np.clip(u, 0, mw - 1.001), np.clip(v, 0, mh - 1.001)
            u0, v0 = np.floor(ui).astype(np.intp), np.floor(vi).astype(np.intp)
            fu, fv = ui - u0, vi - v0
            s = (mask[v0, u0] * (1 - fu) * (1 - fv) + mask[v0, u0 + 1] * fu * (1 - fv) + mask[v0 + 1, u0] * (1 - fu) * fv + mask[v0 + 1, u0 + 1] * fu * fv)
            cov += np.where(inside, s, 0)
    cov /= sub * sub
    if crisp:
        cov = np.clip((cov - 0.5 * crisp * 0.6) / (1 - crisp * 0.6) * (1 + crisp), 0, 1)
    full = np.zeros((H_, W_), dtype=F32)
    full[y0:y1, x0:x1] = cov
    a = np.clip(full * amount, 0, 1)[..., None]
    ink = col(ink) if not isinstance(ink, np.ndarray) or ink.ndim == 1 else ink
    if grain:
        rng = np.random.default_rng(seed)
        ink = ink * (1 + rng.normal(0, grain, pic.shape[:2] + (1,)).astype(F32))
    pic[...] = pic * (1 - a) + ink * a
    return full


def normals(c):
    """The normals of the places a paint is colouring, one per place, whatever shape the thing gave them in."""
    n = np.asarray(c.n, dtype=F32)
    X = np.asarray(c.X)
    if n.ndim == 1:
        return np.broadcast_to(n, X.shape + (3,))
    return n

"""The wagon's own painting kit (egypt_car.py): the inside of the car looked at through ONE camera, ray by ray.

Every pixel of the picture is a ray from Dad's eye (room.View, the scene's camera). What the ray meets (the dashboard, a
dial, the rim of the wheel, the headliner, a candy wrapper on the Son's seat) is found by measurement in the car, in
centimetres, and is then lit from where the light really comes from: the low afternoon sun through the glass (a lamp
far away, its shadows cast by the car's own shell: it comes in through the windshield and the passenger's window only),
the sky and the sunlit sand seen through the glass, the light thrown back from the sunlit dash, the open window at
Dad's left, and the warm light that is simply in a tan car standing in the sun. Rays that leave the car through its
glass or its open window are the world outside, which egypt_car_world.py paints (the kit marks them).

Measurements as in room.py: X across, Y up, Z out from the windshield's foot toward Dad. The shapes and the lighting are
the limousine's kit (nevada_limo_kit.py), taken over as they were and kept as this scene's own copy: nothing here is
imported from another painter's files, and nothing in the shared library is touched."""

import math

import numpy as np

from brush import F32, rgb, lerp, blur

NEAR = 25.0
LUM = np.array([0.3, 0.55, 0.15], dtype=F32)


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


def mixc(a, b, t):
    return lerp(col(a), col(b), t)


# ---------------------------------------------------------------- noise that lies on the surfaces of the car
_T = np.random.default_rng(1217).random((256, 256)).astype(F32)
_TF = _T.reshape(-1)


def vnoise(u, v, seed=0):
    """Value noise, one blob per unit of (u, v). u and v are room measurements, so the pattern is foreshortened
    with the surface it lies on."""
    u = np.asarray(u, dtype=np.float64) + seed * 11.37
    v = np.asarray(v, dtype=np.float64) + seed * 6.91
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
    """A steady random number 0..1 for each whole number (which pleat, which jelly bean)."""
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
    """What a material is told about the rays it has to colour."""

    def __init__(self, **kw):
        self.__dict__.update(kw)


# ---------------------------------------------------------------- the stage
class Stage:
    """A picture's worth of rays (or a rectangle of it), and what each has met so far.

    ss: rays per pixel each way (2 for the finished picture: edges come out soft).
    rect: (x0, y0, x1, y1) in picture pixels, to paint only a patch (for small cut-outs)."""

    def __init__(self, view, ss=1, rect=None, size=(800, 600)):
        self.v, self.ss = view, ss
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
        self.t = np.full((self.h, self.w), 1e9, dtype=F32)
        self.N = np.zeros((self.h, self.w, 3), dtype=F32)
        self.alb = np.zeros((self.h, self.w, 3), dtype=F32)
        self.emi = np.zeros((self.h, self.w, 3), dtype=F32)
        self.oid = np.zeros((self.h, self.w), dtype=np.int16)
        self.grp = np.zeros((self.h, self.w), dtype=np.int8)
        self.flag = np.zeros((self.h, self.w), dtype=np.uint8)       # 1: thin (lit from both sides)  2: no shadow falls on it  4: glass (no light falls, keeps its own colour)
        self.names, self.groups = {"": 0}, {"back": 0}
        self.occ = []                                                # boxes that throw shadows
        self.occ_grp = []                                            # ...and the group each belongs to (a thing that goes takes its shadow with it)
        self.skip = set()                                            # groups not drawn (they still throw shadows)
        self.feet = {}                                               # name -> footprint on the floor (X0, X1, Z0, Z1)

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
        """Write the rays `vis` (a mask over the slice) into the buffers. alb / emi: one colour, or one per ray of vis."""
        if not vis.any():
            return
        self.t[sl][vis] = t[vis] if isinstance(t, np.ndarray) else t
        if isinstance(n, np.ndarray) and n.ndim == 3:
            self.N[sl][vis] = n[vis]
        elif isinstance(n, np.ndarray) and n.ndim == 2:
            self.N[sl][vis] = n
        else:
            self.N[sl][vis] = np.asarray(n, dtype=F32)
        self.alb[sl][vis] = alb
        self.emi[sl][vis] = 0.0 if emi is None else emi
        self.oid[sl][vis] = self.nid(name)
        self.grp[sl][vis] = self.gid(grp)
        self.flag[sl][vis] = flag

    def _mat(self, mat, **kw):
        """A material is a colour, or a function of Ctx -> colour(s), or -> (colour(s), light it gives out), or a third
        thing too for a flat piece: which of its rays are really there (cut paper). A material may also set `c.nrm`:
        the surface's own normal at each ray (a pleat's roll, a dent), for the light. -> (colour, light, keep, normal)"""
        if callable(mat):
            c = Ctx(ss=self.ss, F=self.v.F, **kw)
            r = mat(c)
            if not isinstance(r, tuple):
                r = (r,)
            r = tuple(r) + (None,) * (3 - len(r))
            return r[0], r[1], r[2], getattr(c, "nrm", None)
        return col(mat), None, None, None

    @staticmethod
    def _cut(vis, a, e, keep, nrm):
        """Drop the rays a flat piece's material says are not there. -> (vis, colour, light, normal)."""
        if keep is not None and not keep.all():
            out = np.zeros(vis.shape, dtype=bool)
            out[vis] = keep
            pick = lambda v: v[keep] if isinstance(v, np.ndarray) and v.ndim == 2 else v
            return out, pick(a), pick(e), pick(nrm)
        return vis, a, e, nrm

    # ---- boxes
    def box(self, x0, x1, y0, y1, z0, z1, mat, name=None, grp="back", shadow=True, flag=0, emi=None, foot=False, inside=False):
        """A box. `inside`: its inner faces are what we see (the walls of the car are boxes we are inside of)."""
        if x1 < x0:
            x0, x1 = x1, x0
        if y1 < y0:
            y0, y1 = y1, y0
        if z1 < z0:
            z0, z1 = z1, z0
        if shadow:
            self.occ.append((x0, x1, y0, y1, z0, z1)); self.occ_grp.append(grp)
        if foot and name:
            f = self.feet.get(name)
            self.feet[name] = (x0, x1, z0, z1) if f is None else (min(f[0], x0), max(f[1], x1), min(f[2], z0), max(f[3], z1))
        if grp in self.skip:
            return
        sl = self._slice([(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]) if not inside else (slice(0, self.h), slice(0, self.w))
        if sl is None:
            return
        C = self.C
        D = (self.dX[sl], self.dY[sl], self.dZ[sl])
        lo, hi = (x0, y0, z0), (x1, y1, z1)
        tn = np.full(D[0].shape, -1e9, dtype=F32)
        tf = np.full(D[0].shape, 1e9, dtype=F32)
        face = np.zeros(D[0].shape, dtype=np.int8)
        facef = np.zeros(D[0].shape, dtype=np.int8)
        for k in range(3):
            ta, tb = (lo[k] - C[k]) / D[k], (hi[k] - C[k]) / D[k]
            t0, t1 = np.minimum(ta, tb), np.maximum(ta, tb)
            later = t0 > tn
            face[later] = k
            tn = np.where(later, t0, tn)
            sooner = t1 < tf
            facef[sooner] = k
            tf = np.minimum(tf, t1)
        if inside:                                               # we are in the box: the far side of it is what we see
            tn, face = tf, facef
            vis = (tn > NEAR) & (tn < self.t[sl])
        else:
            vis = (tn <= tf) & (tn > NEAR) & (tn < self.t[sl])
        if not vis.any():
            return
        names = (("left", "right"), ("bottom", "top"), ("back", "front"))
        for k in range(3):
            for sgn in (0, 1):                                   # sgn 1: the face on the high side of axis k
                m = vis & (face == k) & ((D[k] < 0) == bool(sgn)) if not inside else vis & (face == k) & ((D[k] > 0) == bool(sgn))
                if not m.any():
                    continue
                t = tn[m]
                n = [0.0, 0.0, 0.0]
                n[k] = (1.0 if sgn else -1.0) * (-1.0 if inside else 1.0)
                # every ray of the slice met with this face's plane: smooth fields, so the material can rule lines
                # of a width in pixels (gX, gY, gZ: how much each measurement changes from one ray to the next)
                pv = hi[k] if sgn else lo[k]
                tp = (pv - C[k]) / D[k]
                g = [grad_of((C[i] + tp * D[i]).astype(F32))[m] for i in range(3)]
                a, e, _, nrm = self._mat(mat, X=C[0] + t * D[0][m], Y=C[1] + t * D[1][m], Z=C[2] + t * D[2][m], t=t,
                                         fp=t / self.v.F, face=names[k][sgn], n=tuple(n), box=(x0, x1, y0, y1, z0, z1),
                                         gX=g[0], gY=g[1], gZ=g[2])
                self._put(sl, m, tn, tuple(n) if nrm is None else nrm, a, e if e is not None else emi, name, grp, flag)

    # ---- flat pieces at any angle (a sheet of paper, a lid, a strap)
    def poly(self, pts, mat, name=None, grp="back", flag=0, emi=None, bias=0.0, shadow=False):
        """A flat convex polygon in the room. The material is told U, V: centimetres along its first edge and
        square to it. `bias` pulls it that many cm toward the lens (for paper lying on something)."""
        if shadow:
            xs, ys, zs = [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts]
            self.occ.append((min(xs) - 0.5, max(xs) + 0.5, min(ys) - 0.5, max(ys) + 0.5, min(zs) - 0.5, max(zs) + 0.5)); self.occ_grp.append(grp)
        if grp in self.skip:
            return
        sl = self._slice(pts)
        if sl is None:
            return
        P = [np.asarray(p, dtype=np.float64) for p in pts]
        e1 = P[1] - P[0]
        n = np.cross(e1, P[2] - P[0])
        n = n / (np.linalg.norm(n) + 1e-12)
        C = np.asarray(self.C, dtype=np.float64)
        if np.dot(n, C - P[0]) < 0:
            n = -n
        D = (self.dX[sl], self.dY[sl], self.dZ[sl])
        dn = n[0] * D[0] + n[1] * D[1] + n[2] * D[2]
        dn = np.where(np.abs(dn) < 1e-9, -1e-9, dn)
        t = (np.dot(n, P[0] - C) / dn).astype(F32)
        X, Y, Z = C[0] + t * D[0], C[1] + t * D[1], C[2] + t * D[2]
        inside = (t > NEAR)
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
        td = t - bias
        vis = inside & (td < self.t[sl])
        if not vis.any():
            return
        u1 = e1 / (np.linalg.norm(e1) + 1e-12)
        u2 = np.cross(n, u1)
        if np.dot(u2, P[-1] - P[0]) < 0:
            u2 = -u2
        Xa, Ya, Za = X - P[0][0], Y - P[0][1], Z - P[0][2]
        U2 = (Xa * u1[0] + Ya * u1[1] + Za * u1[2]).astype(F32)
        V2 = (Xa * u2[0] + Ya * u2[1] + Za * u2[2]).astype(F32)
        gx = dict(gX=grad_of(X.astype(F32))[vis], gY=grad_of(Y.astype(F32))[vis], gZ=grad_of(Z.astype(F32))[vis], gU=grad_of(U2)[vis], gV=grad_of(V2)[vis])
        a, e, keep, nrm = self._mat(mat, X=X[vis], Y=Y[vis], Z=Z[vis], U=U2[vis], V=V2[vis], t=t[vis], fp=t[vis] / self.v.F, face="flat", n=tuple(n), **gx)
        vis, a, e, nrm = self._cut(vis, a, e, keep, nrm)
        self._put(sl, vis, td, tuple(float(q) for q in n) if nrm is None else nrm, a, e if e is not None else emi, name, grp, flag)

    # ---- round things
    def cyl(self, c, r, a0, a1, mat, axis="y", r1=None, name=None, grp="back", shadow=True, flag=0, emi=None, hollow=False, cap=None):
        """A cylinder, or with r1 a cone-sided tub (r at a0, r1 at a1), standing along an axis.
        c: the two other coordinates of its middle line: (X, Z) for "y", (Y, Z) for "x", (X, Y) for "z".
        hollow: open ended, and its inside wall is seen (an ashtray, a cup)."""
        r1 = r if r1 is None else r1
        rm = max(r, r1)
        if axis == "y":
            lo, hi = (c[0] - rm, a0, c[1] - rm), (c[0] + rm, a1, c[1] + rm)
        elif axis == "x":
            lo, hi = (a0, c[0] - rm, c[1] - rm), (a1, c[0] + rm, c[1] + rm)
        else:
            lo, hi = (c[0] - rm, c[1] - rm, a0), (c[0] + rm, c[1] + rm, a1)
        if shadow:
            k = 0.82
            m = [(lo[i] + hi[i]) / 2 for i in range(3)]
            ax = "xyz".index(axis)
            o = [(m[i] - (m[i] - lo[i]) * (1 if i == ax else k), m[i] + (hi[i] - m[i]) * (1 if i == ax else k)) for i in range(3)]
            self.occ.append((o[0][0], o[0][1], o[1][0], o[1][1], o[2][0], o[2][1])); self.occ_grp.append(grp)
        if grp in self.skip:
            return
        sl = self._slice([(x, y, z) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
        if sl is None:
            return
        ia = "xyz".index(axis)
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
        kind = np.zeros(d1.shape, dtype=np.int8)              # 1 outside wall, 2 inside wall, 3 cap at a1, 4 cap at a0
        for tt, kk in ((tA, 1), (tB, 2)):
            if kk == 2 and not hollow:
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
        nn = np.sqrt(1 + s * s)
        n[:, i1] = np.where(wall, sg * q1 / rr / nn, 0)
        n[:, i2] = np.where(wall, sg * q2 / rr / nn, 0)
        n[:, ia] = np.where(wall, -sg * s / nn, np.where(kd == 3, 1.0, -1.0))
        ang = np.arctan2(q2, q1).astype(F32)
        a, e, _, _ = self._mat(mat, X=P[0], Y=P[1], Z=P[2], t=t, fp=t / self.v.F, face="round",
                         kind=kd, ang=ang, along=(qa - a0).astype(F32), rad=rr.astype(F32), n=n)
        if cap is not None and (kd >= 3).any():
            a = np.broadcast_to(a, (len(t), 3)).copy()
            a[kd >= 3] = col(cap)
        full = np.zeros(vis.shape + (3,), dtype=F32)
        full[vis] = n
        self._put(sl, vis, best, full, a, e if e is not None else emi, name, grp, flag)

    def ball(self, c, r, mat, name=None, grp="back", shadow=True, flag=0, emi=None, squash=1.0):
        """A ball (or with `squash` an egg lying along X: a jelly bean)."""
        if shadow:
            k = r * 0.75
            self.occ.append((c[0] - k, c[0] + k, c[1] - k, c[1] + k, c[2] - k, c[2] + k)); self.occ_grp.append(grp)
        if grp in self.skip:
            return
        sl = self._slice([(c[0] + i * r, c[1] + j * r, c[2] + k * r) for i in (-1, 1) for j in (-1, 1) for k in (-1, 1)])
        if sl is None:
            return
        D = (self.dX[sl], self.dY[sl], self.dZ[sl])
        o = [self.C[i] - c[i] for i in range(3)]
        A = D[0] ** 2 + D[1] ** 2 + D[2] ** 2
        B = 2 * (o[0] * D[0] + o[1] * D[1] + o[2] * D[2])
        Cq = o[0] ** 2 + o[1] ** 2 + o[2] ** 2 - r * r
        disc_ = B * B - 4 * A * Cq
        ok = disc_ >= 0
        tt = (-B - np.sqrt(np.where(ok, disc_, 0))) / (2 * A)
        vis = ok & (tt > NEAR) & (tt < self.t[sl])
        if not vis.any():
            return
        t = tt[vis]
        P = [self.C[i] + t * D[i][vis] for i in range(3)]
        n = np.stack([(P[i] - c[i]) / r for i in range(3)], axis=1).astype(F32)
        lon = np.arctan2(n[:, 0], n[:, 2])
        lat = np.arcsin(np.clip(n[:, 1], -1, 1))
        a, e, _, _ = self._mat(mat, X=P[0], Y=P[1], Z=P[2], t=t, fp=t / self.v.F, face="ball", lon=lon, lat=lat, n=n)
        full = np.zeros(vis.shape + (3,), dtype=F32)
        full[vis] = n
        self._put(sl, vis, tt.astype(F32), full, a, e if e is not None else emi, name, grp, flag)

    # ---- thin things: cords, ropes, straws
    def stick(self, p, q, radius, mat, name=None, grp="back", flag=0, emi=None, min_px=0.55, r1=None):
        """A round rod from p to q, `radius` cm thick (r1 at the far end, if it tapers). Drawn by its outline on the
        picture, with its true depth, and shaded round."""
        if grp in self.skip:
            return
        v, ss = self.v, self.ss
        a0, u0, d0 = v.cam_space(*p)
        a1, u1, d1 = v.cam_space(*q)
        if d0 < NEAR or d1 < NEAR:
            return
        r1 = radius if r1 is None else r1
        k0, k1 = v.F / d0, v.F / d1
        x0, y0 = (v.cx + a0 * k0 - self.rect[0]) * ss, (v.hz - u0 * k0 - self.rect[1]) * ss
        x1, y1 = (v.cx + a1 * k1 - self.rect[0]) * ss, (v.hz - u1 * k1 - self.rect[1]) * ss
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
        a, e, _, _ = self._mat(mat, X=P[0], Y=P[1], Z=P[2], t=tv, fp=tv / v.F, face="rod", along=s[vis], side=side)
        a = np.broadcast_to(np.asarray(a, dtype=F32), (len(tv), 3)) * (0.72 + 0.34 * np.cos(side * 1.45))[:, None]
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

    def occ_without(self, *groups):
        """The shadow-throwing boxes, less those of the given groups (a thing that goes takes its shadow with it)."""
        return [b for b, g in zip(self.occ, self.occ_grp) if g not in groups]

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
    def __init__(self, pos, color, power, reach=120.0, aim=None, spread=None, soft=0.15, size=5.0, fill=0.0, shadows=True, wrap=0.15, back=0.0, samples=5):
        """pos: where it is. power: how bright a surface facing it is at `reach` cm. aim/spread: a shaded lamp
        throws most of its light inside a cone (spread = cosine of the half-angle; soft = how soft the cone's edge;
        back = what still gets out sideways). size: the lamp's own size, cm (soft shadow edges). fill: light that
        reaches everything near it regardless of which way the surface faces (bounce)."""
        self.pos, self.color, self.power, self.reach = np.asarray(pos, dtype=np.float64), col(color), power, reach
        self.aim = None if aim is None else np.asarray(aim, dtype=np.float64) / np.linalg.norm(aim)
        self.spread, self.soft, self.size, self.fill, self.shadows, self.wrap, self.back = spread, soft, size, fill, shadows, wrap, back
        self.samples = samples


def seg_hits(P, Q, occ, skip_near=0.0):
    """For each place P: does the straight way to Q pass through any of the boxes? P: 3 arrays; Q: 3 numbers or
    3 arrays. -> boolean array."""
    D = [np.asarray(Q[i], dtype=F32) - P[i] for i in range(3)]
    inv = []
    for d in D:
        d = np.where(np.abs(d) < 1e-6, 1e-6, d)
        inv.append((1.0 / d).astype(F32))
    hit = np.zeros(P[0].shape, dtype=bool)
    for (x0, x1, y0, y1, z0, z1) in occ:
        lo, hi = (x0, y0, z0), (x1, y1, z1)
        tn = np.full(P[0].shape, skip_near, dtype=F32)
        tf = np.ones(P[0].shape, dtype=F32)
        for k in range(3):
            ta, tb = (lo[k] - P[k]) * inv[k], (hi[k] - P[k]) * inv[k]
            tn = np.maximum(tn, np.minimum(ta, tb))
            tf = np.minimum(tf, np.maximum(ta, tb))
        hit |= tn < tf
    return hit


def shade(st, lamps, ambient, fast=False, seed=5, occ=None, expose=1.0):
    """Light every ray's landing place from the lamps. -> (picture, rays x 3; the light alone).
    ambient: function(X, Y, Z, N) -> light that is simply everywhere (rays x 3). Glass (flag 4) keeps its own colour."""
    occ = st.occ if occ is None else occ
    X, Y, Z = st.places()
    N = st.N
    ss = st.ss
    light = ambient(X, Y, Z, N).astype(F32)
    hit = st.t < 9e8
    thin = (st.flag & 1) > 0
    noshadow = (st.flag & 2) > 0
    glass = (st.flag & 4) > 0
    rng = np.random.default_rng(seed)
    o = ss // 2
    Xs, Ys, Zs = X[o::ss, o::ss], Y[o::ss, o::ss], Z[o::ss, o::ss]
    Ns = N[o::ss, o::ss]
    Ps = (Xs + Ns[..., 0] * 0.7, Ys + Ns[..., 1] * 0.7, Zs + Ns[..., 2] * 0.7)
    for lamp in lamps:
        Lx, Ly, Lz = (lamp.pos[0] - X), (lamp.pos[1] - Y), (lamp.pos[2] - Z)
        d2 = Lx * Lx + Ly * Ly + Lz * Lz + 1e-3
        d = np.sqrt(d2)
        ndl = (N[..., 0] * Lx + N[..., 1] * Ly + N[..., 2] * Lz) / d
        ndl = np.where(thin, np.abs(ndl) * 0.8 + 0.2, ndl)
        lam = np.clip((ndl + lamp.wrap) / (1 + lamp.wrap), 0, 1)
        fall = lamp.power / (0.35 + d2 / (lamp.reach * lamp.reach))
        if lamp.aim is not None:
            ca = -(Lx * lamp.aim[0] + Ly * lamp.aim[1] + Lz * lamp.aim[2]) / d
            cone = np.clip((ca - lamp.spread) / lamp.soft + 0.5, 0, 1)
            cone = cone * cone * (3 - 2 * cone)
            fall = fall * (lamp.back + (1 - lamp.back) * cone)
        direct = lam * fall
        if lamp.shadows:
            act = (direct[o::ss, o::ss] > 0.004) & hit[o::ss, o::ss]
            vis = np.ones(act.shape, dtype=F32)
            if act.any():
                Pa = tuple(p[act] for p in Ps)
                n = 1 if fast else lamp.samples
                acc = np.zeros(Pa[0].shape, dtype=F32)
                for k in range(n):
                    j = (rng.normal(0, 1, 3) * lamp.size * (0.0 if n == 1 else 0.6))
                    Q = (lamp.pos[0] + j[0], lamp.pos[1] + j[1], lamp.pos[2] + j[2])
                    blocked = seg_hits(Pa, Q, occ, 0.0)
                    acc += np.where(blocked, 0.0, 1.0).astype(F32)
                vis[act] = acc / n
            vis = blur(vis, 0.7 if lamp.size < 12 else 2.0)
            vis = np.repeat(np.repeat(vis, ss, axis=0), ss, axis=1) if ss > 1 else vis
            vis = np.where(noshadow, 1.0, vis)
            direct = direct * vis
        light += (direct[..., None] * lamp.color[None, None, :]).astype(F32)
        if lamp.fill:
            light += ((lamp.fill * lamp.power / (0.6 + d2 / (lamp.reach * lamp.reach * 4)))[..., None] * lamp.color[None, None, :]).astype(F32)
    out = st.alb * light * expose + st.emi
    out = 1 - np.exp(-out * 1.15)                                        # a soft shoulder: bright places do not go flat
    out = np.where(glass[..., None], st.alb + st.emi, out)               # (glass keeps its own colour exactly)
    out = np.where(hit[..., None], out, 0)
    return out.astype(F32), light


def floor_contact(st, X, Z, feet, reach=9.0, amount=0.45):
    """Darkening of the carpet round the foot of everything that stands on it (so it sits, and does not float)."""
    dark = np.zeros(X.shape, dtype=F32)
    for (x0, x1, z0, z1) in feet:
        dx = np.maximum(np.maximum(x0 - X, X - x1), 0)
        dz = np.maximum(np.maximum(z0 - Z, Z - z1), 0)
        d = np.sqrt(dx * dx + dz * dz)
        dark = np.maximum(dark, np.exp(-d / reach) * (d > 0))
    return dark * amount

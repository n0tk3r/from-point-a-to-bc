"""A painter's kit for one room seen through ONE camera (home_study.py): a small ray-caster built on room.View.

Why a ray-caster: the brief for the house says every surface, every piece of furniture, every shadow and every
pool of light must go through the same camera. So here each pixel of the picture is a ray from that camera, and
what it meets (floor, wall, roof, rafter, box, jar, globe) is found by measurement in the room, in centimetres.
The light is then worked out in the room too: each lamp has a place, brightness falls with distance and with
the angle the light strikes, and a shadow is whatever stands between a place and the lamp. The result is only
the UNDER-painting: the brush pass, the crisp details and the limited palette come afterwards (home_study.py).

Room measurements as in room.py: X across, Y up, Z out from the far wall toward us.
Nothing here touches the shared library."""

import math

import numpy as np

from brush import F32, rgb, lerp, blur, noise, sample

NEAR = 25.0


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


def mixc(a, b, t):
    return lerp(col(a), col(b), t)


# ---------------------------------------------------------------- noise that lives in the room, not in the picture
_T = np.random.default_rng(71).random((256, 256)).astype(F32)


def vnoise(u, v, seed=0):
    """Value noise at any (u, v): one blob per unit. Because u and v are ROOM measurements, the pattern
    lies on the surface and is foreshortened with it."""
    u = np.asarray(u, dtype=np.float64) + seed * 17.13
    v = np.asarray(v, dtype=np.float64) + seed * 7.71
    iu, iv = np.floor(u), np.floor(v)
    fu, fv = (u - iu).astype(F32), (v - iv).astype(F32)
    fu, fv = fu * fu * (3 - 2 * fu), fv * fv * (3 - 2 * fv)
    iu, iv = iu.astype(np.int64) & 255, iv.astype(np.int64) & 255
    iu1, iv1 = (iu + 1) & 255, (iv + 1) & 255
    a, b, c, d = _T[iv, iu], _T[iv, iu1], _T[iv1, iu], _T[iv1, iu1]
    return (a + (b - a) * fu) * (1 - fv) + (c + (d - c) * fu) * fv


def fbm(u, v, seed=0, octaves=4, gain=0.5):
    total, norm, w = 0.0, 0.0, 1.0
    for k in range(octaves):
        total = total + w * vnoise(u * (2 ** k), v * (2 ** k), seed + k * 3)
        norm += w
        w *= gain
    return (total / norm).astype(F32)


def hashf(i, seed=0):
    """A steady random number 0..1 for each whole number i (which board, which book, which rafter)."""
    i = np.asarray(i).astype(np.int64)
    return _T.reshape(-1)[((i * 73856093) ^ (seed * 19349663 + 83492791)) & 65535]


def grad_of(field):
    """How much a room measurement changes from one pixel to the next (its size on the picture)."""
    gy, gx = np.gradient(field)
    return np.sqrt(gx * gx + gy * gy).astype(F32) + 1e-6


def lines_aa(coord, period, width_px, g, phase=0.0, fade=True):
    """Coverage (0..1) of ruled lines at coord = phase + k * period, `width_px` wide on the picture, soft-edged.
    `g` is grad_of(coord). Lines closer together than a couple of pixels fade into a tone instead of flickering."""
    f = (coord - phase) / period
    d = np.abs(f - np.round(f)) * period
    c = np.clip(width_px * 0.5 + 0.5 - d / g, 0, 1)
    if fade:
        c = c * np.clip((period / g - 1.6) / 2.4, 0.12, 1)
    return c.astype(F32)


def band_aa(coord, lo, hi, g):
    """Coverage of the band lo <= coord <= hi, soft-edged by one pixel."""
    return (np.clip((coord - lo) / g + 0.5, 0, 1) * np.clip((hi - coord) / g + 0.5, 0, 1)).astype(F32)


class Ctx:
    """What a material is told about the pixels it has to color."""

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
        self.flag = np.zeros((self.h, self.w), dtype=np.uint8)       # 1: thin (lit from both sides)  2: no shadow falls on it
        self.names, self.groups = {"": 0}, {"back": 0}
        self.occ = []                                                # boxes that throw shadows
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
        """Write the pixels `vis` (a mask over the slice) into the buffers. alb / emi: one color, or one per pixel of vis."""
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
        """A material is a color, or a function of Ctx -> color(s), or -> (color(s), light it gives out)."""
        if callable(mat):
            r = mat(Ctx(ss=self.ss, F=self.v.F, **kw))
            return r if isinstance(r, tuple) else (r, None)
        return col(mat), None

    @staticmethod
    def _cut(vis, r):
        """A flat piece's material may return a third thing: which of its pixels are really there (cut paper).
        -> (vis, color, light) with the others dropped."""
        a, e = r[0], r[1]
        if len(r) > 2 and r[2] is not None and not r[2].all():
            keep = r[2]
            out = np.zeros(vis.shape, dtype=bool)
            out[vis] = keep
            a = a[keep] if isinstance(a, np.ndarray) and a.ndim == 2 else a
            e = e[keep] if isinstance(e, np.ndarray) and e.ndim == 2 else e
            return out, a, e
        return vis, a, e

    # ---- boxes
    def box(self, x0, x1, y0, y1, z0, z1, mat, name=None, grp="back", shadow=True, flag=0, emi=None, foot=False):
        if x1 < x0:
            x0, x1 = x1, x0
        if y1 < y0:
            y0, y1 = y1, y0
        if z1 < z0:
            z0, z1 = z1, z0
        if shadow:
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
        face = np.zeros(D[0].shape, dtype=np.int8)
        for k in range(3):
            ta, tb = (lo[k] - C[k]) / D[k], (hi[k] - C[k]) / D[k]
            t0, t1 = np.minimum(ta, tb), np.maximum(ta, tb)
            later = t0 > tn
            face[later] = k
            tn = np.where(later, t0, tn)
            tf = np.minimum(tf, t1)
        vis = (tn <= tf) & (tn > NEAR) & (tn < self.t[sl])
        if not vis.any():
            return
        names = (("left", "right"), ("bottom", "top"), ("back", "front"))
        for k in range(3):
            for sgn in (0, 1):                                   # sgn 1: the face on the high side of axis k
                m = vis & (face == k) & ((D[k] < 0) == bool(sgn))
                if not m.any():
                    continue
                t = tn[m]
                n = [0.0, 0.0, 0.0]
                n[k] = 1.0 if sgn else -1.0
                a, e = self._mat(mat, X=C[0] + t * D[0][m], Y=C[1] + t * D[1][m], Z=C[2] + t * D[2][m], t=t,
                                 fp=t / self.v.F, face=names[k][sgn], n=tuple(n), box=(x0, x1, y0, y1, z0, z1))
                self._put(sl, m, tn, tuple(n), a, e if e is not None else emi, name, grp, flag)

    # ---- flat pieces at any angle (a door leaf, a lid, a sloping panel, a sheet of paper)
    def poly(self, pts, mat, name=None, grp="back", flag=0, emi=None, bias=0.0):
        """A flat convex polygon in the room. The material is told U, V: centimetres along its first edge and
        square to it. `bias` pulls it that many cm toward the lens (for paper lying on something)."""
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
        # which way round the corners go
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
        Xv, Yv, Zv = X[vis] - P[0][0], Y[vis] - P[0][1], Z[vis] - P[0][2]
        U = (Xv * u1[0] + Yv * u1[1] + Zv * u1[2]).astype(F32)
        V = (Xv * u2[0] + Yv * u2[1] + Zv * u2[2]).astype(F32)
        r = self._mat(mat, X=X[vis], Y=Y[vis], Z=Z[vis], U=U, V=V, t=t[vis], fp=t[vis] / self.v.F, face="flat", n=tuple(n))
        vis, a, e = self._cut(vis, r)
        self._put(sl, vis, td, tuple(float(q) for q in n), a, e if e is not None else emi, name, grp, flag)

    # ---- round things
    def cyl(self, c, r, a0, a1, mat, axis="y", r1=None, name=None, grp="back", shadow=True, flag=0, emi=None, hollow=False, cap=None):
        """A cylinder, or with r1 a cone-sided tub (r at a0, r1 at a1), standing along an axis.
        c: the two other coordinates of its middle line: (X, Z) for "y", (Y, Z) for "x", (X, Y) for "z".
        hollow: open ended, and its inside wall is seen (a lamp shade, a waste basket, a jar's mouth)."""
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
            self.occ.append((o[0][0], o[0][1], o[1][0], o[1][1], o[2][0], o[2][1]))
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
        disc = B * B - 4 * A * Cq
        ok = disc >= 0
        sq = np.sqrt(np.where(ok, disc, 0))
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
        a, e = self._mat(mat if cap is None else mat, X=P[0], Y=P[1], Z=P[2], t=t, fp=t / self.v.F, face="round",
                         kind=kd, ang=ang, along=(qa - a0).astype(F32), rad=rr.astype(F32), n=n)
        if cap is not None and (kd >= 3).any():
            a = np.broadcast_to(a, (len(t), 3)).copy()
            a[kd >= 3] = col(cap)
        full = np.zeros(vis.shape + (3,), dtype=F32)
        full[vis] = n
        self._put(sl, vis, best, full, a, e if e is not None else emi, name, grp, flag)

    def ball(self, c, r, mat, name=None, grp="back", shadow=True, flag=0, emi=None):
        if shadow:
            k = r * 0.75
            self.occ.append((c[0] - k, c[0] + k, c[1] - k, c[1] + k, c[2] - k, c[2] + k))
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
        disc = B * B - 4 * A * Cq
        ok = disc >= 0
        tt = (-B - np.sqrt(np.where(ok, disc, 0))) / (2 * A)
        vis = ok & (tt > NEAR) & (tt < self.t[sl])
        if not vis.any():
            return
        t = tt[vis]
        P = [self.C[i] + t * D[i][vis] for i in range(3)]
        n = np.stack([(P[i] - c[i]) / r for i in range(3)], axis=1).astype(F32)
        lon = np.arctan2(n[:, 0], n[:, 2])
        lat = np.arcsin(np.clip(n[:, 1], -1, 1))
        a, e = self._mat(mat, X=P[0], Y=P[1], Z=P[2], t=t, fp=t / self.v.F, face="ball", lon=lon, lat=lat, n=n)
        full = np.zeros(vis.shape + (3,), dtype=F32)
        full[vis] = n
        self._put(sl, vis, tt.astype(F32), full, a, e if e is not None else emi, name, grp, flag)

    # ---- thin things: cords, strings, spindles, legs, rods
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
        a, e = self._mat(mat, X=P[0], Y=P[1], Z=P[2], t=tv, fp=tv / v.F, face="rod", along=s[vis], side=side)
        a = np.broadcast_to(np.asarray(a, dtype=F32), (len(tv), 3)) * (0.72 + 0.34 * np.cos(side * 1.45))[:, None]
        # the rod's normal: square to the rod, turned toward the lens and a little to the side we are looking at
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


# ---------------------------------------------------------------- the attic: floor, gable, low walls, roof and rafters
class Attic:
    """The shell of a room under a roof: a floor, the far gable wall (Z = 0), a low wall each side, and the two
    slopes of the roof meeting at the ridge, with rafters standing down from the boards every `gap` cm."""

    def __init__(self, width, knee, ridge, rafter=(30.0, 60.0, 2.8, 12.0, 1115.0)):
        self.W, self.K, self.R = float(width), float(knee), float(ridge)
        self.run, self.rise = self.W / 2, self.R - self.K
        self.len = math.hypot(self.run, self.rise)             # the slope, plate to ridge, cm
        self.z0, self.gap, self.half, self.deep, self.zmax = rafter

    def roof_y(self, X):
        return self.K + self.rise * (1 - np.abs(np.asarray(X, dtype=np.float64) - self.run) / self.run)

    def draw(self, st, mats, grp="back", holes=None):
        """mats: {"floor", "gable", "kneeL", "kneeR", "roofL", "roofR", "rafter"}: each a function of Ctx.
        The Ctx carries whole-picture fields (so a material can rule soft lines with grad_of) and `m`, the mask of
        the pixels that are really that surface."""
        C, dX, dY, dZ = st.C, st.dX, st.dY, st.dZ
        big = np.float32(1e9)
        run, rise, L = self.run, self.rise, self.len

        def plane(num, den):
            with np.errstate(divide="ignore", invalid="ignore"):
                t = num / den
            return np.where((den < 0) & (t > 0), t, big).astype(F32)

        # each wall as "inside while f >= 0": the ray leaves where f falls to 0
        tF = plane(-(C[1]), dY)                                              # floor: f = Y
        tG = plane(-(C[2]), dZ)                                              # gable: f = Z
        tL = plane(-(C[0]), dX)                                              # left low wall: f = X
        tR = plane(-(self.W - C[0]), -dX)                                    # right low wall: f = W - X
        fL0 = (rise * C[0] - run * C[1] + run * self.K) / L                  # distance inside the left slope
        fR0 = (rise * (self.W - C[0]) - run * C[1] + run * self.K) / L
        dL = (rise * dX - run * dY) / L
        dR = (-rise * dX - run * dY) / L
        tRL, tRR = plane(-fL0, dL), plane(-fR0, dR)
        ts = np.stack([tF, tG, tL, tR, tRL, tRR])
        which = ts.argmin(axis=0)
        t = ts.min(axis=0)
        normals = [(0, 1, 0), (0, 0, 1), (1, 0, 0), (-1, 0, 0), (rise / L, -run / L, 0), (-rise / L, -run / L, 0)]
        keys = ["floor", "gable", "kneeL", "kneeR", "roofL", "roofR"]

        # ---- rafters: a slab `deep` cm thick under each slope, solid for `half` cm either side of every rafter line
        raft = np.zeros(t.shape, dtype=np.int8)                              # 1 underside, 2 the side toward us
        tr = t.copy()
        rside = np.zeros(t.shape, dtype=np.int8)
        for sd, (f0, df) in enumerate(((fL0, dL), (fR0, dR))):
            tin = np.where(df < 0, (self.deep - f0) / df, big)
            tin = np.maximum(tin, 0).astype(F32) if f0 >= self.deep else np.zeros(t.shape, dtype=F32)
            enter = (df < 0) & (tin < t) if f0 >= self.deep else np.ones(t.shape, dtype=bool)
            Zin = C[2] + tin * dZ
            Zend = C[2] + t * dZ
            i = np.round((Zin - self.z0) / self.gap)
            zc = self.z0 + self.gap * i
            under = enter & (np.abs(Zin - zc) <= self.half) & (zc <= self.zmax) & (zc >= self.z0 - 1) & (tin > NEAR)
            j = np.floor((Zin - self.z0 - self.half) / self.gap)
            j = np.minimum(j, math.floor((self.zmax - self.z0) / self.gap))       # (no rafter nearer the lens than the last one)
            zf = self.z0 + self.gap * j + self.half
            tsd = (zf - C[2]) / dZ
            side = enter & ~under & (zf >= Zend) & (zf - self.half <= self.zmax) & (zf >= self.z0) & (tsd > NEAR) & (tsd < t)
            m = under & (tin < tr)
            tr = np.where(m, tin, tr)
            raft[m], rside[m] = 1, sd
            m = side & (tsd < tr)
            tr = np.where(m, tsd, tr)
            raft[m], rside[m] = 2, sd

        X, Y, Z = C[0] + tr * dX, C[1] + tr * dY, C[2] + tr * dZ
        fields = dict(X=X, Y=Y, Z=Z, t=tr, ss=st.ss, F=st.v.F, attic=self)
        for k, key in enumerate(keys):
            m = (which == k) & (raft == 0) & (tr < st.t)
            if not m.any():
                continue
            for (hx0, hx1, hy0, hy1) in (holes or {}).get(key, []):        # an opening: what is beyond shows through
                m &= ~((X > hx0) & (X < hx1) & (Y > hy0) & (Y < hy1))
            if key in ("roofL", "roofR"):
                s = (X if key == "roofL" else self.W - X) * (L / run)      # cm up the slope from the plate
                extra = dict(S=s.astype(F32))
            else:
                extra = {}
            r = mats[key](Ctx(m=m, face=key, n=normals[k], **fields, **extra))
            a, e = r if isinstance(r, tuple) else (r, None)
            full = (slice(None), slice(None))
            st._put(full, m, tr, normals[k], a[m] if isinstance(a, np.ndarray) and a.ndim == 3 else a,
                    (e[m] if isinstance(e, np.ndarray) and e.ndim == 3 else e), key, grp, 0)
        for sd in (0, 1):
            sgn = 1 if sd == 0 else -1
            for kind, n in ((1, (sgn * rise / L, -run / L, 0)), (2, (0, 0, 1))):
                m = (raft == kind) & (rside == sd) & (tr < st.t)
                if not m.any():
                    continue
                s = (X if sd == 0 else self.W - X) * (L / run)
                r = mats["rafter"](Ctx(m=m, face="under" if kind == 1 else "side", n=n, S=s.astype(F32), sd=sd, **fields))
                a, e = r if isinstance(r, tuple) else (r, None)
                st._put((slice(None), slice(None)), m, tr, n, a[m] if isinstance(a, np.ndarray) and a.ndim == 3 else a, e, "rafter", grp, 0)

    def rafter_shadow(self, P, L, on_roof):
        """For places on the roof boards: is a rafter between the place and the lamp? (1 = lit, 0 = in shadow)"""
        X, Y, Z = P
        run, rise, Ln = self.run, self.rise, self.len
        left = X < run
        f = np.where(left, rise * X - run * Y + run * self.K, rise * (self.W - X) - run * Y + run * self.K) / Ln
        fl = np.where(left, rise * L[0] - run * L[1] + run * self.K, rise * (self.W - L[0]) - run * L[1] + run * self.K) / Ln
        s1 = np.clip((self.deep - f) / np.maximum(fl - f, 1e-3), 0, 1)        # how far along the way to the lamp the slab ends
        Zb = Z + s1 * (L[2] - Z)
        lo, hi = np.minimum(Z, Zb), np.maximum(Z, Zb)
        hit = np.floor((hi - self.z0 + self.half) / self.gap) >= np.ceil((lo - self.z0 - self.half) / self.gap)
        hit &= (lo <= self.zmax + self.half)
        return np.where(on_roof & hit & (f < self.deep * 0.5), 0.0, 1.0).astype(F32)


# ---------------------------------------------------------------- light
class Lamp:
    def __init__(self, pos, color, power, reach=120.0, aim=None, spread=None, soft=0.15, size=5.0, fill=0.0, shadows=True, wrap=0.15, back=0.0, double=False, samples=5):
        """pos: where it is. power: how bright a surface facing it is at `reach` cm. aim/spread: a shaded lamp
        throws most of its light inside a cone (spread = cosine of the half-angle; soft = how soft the cone's edge;
        back = what still gets out sideways through the shade). size: the lamp's own size, cm (soft shadow edges).
        fill: light that reaches everything near it regardless of which way the surface faces (bounce)."""
        self.pos, self.color, self.power, self.reach = np.asarray(pos, dtype=np.float64), col(color), power, reach
        self.aim = None if aim is None else np.asarray(aim, dtype=np.float64) / np.linalg.norm(aim)
        self.spread, self.soft, self.size, self.fill, self.shadows, self.wrap, self.back = spread, soft, size, fill, shadows, wrap, back
        self.double = double                                   # the cone goes both ways along `aim` (a shade open top and bottom)
        self.samples = samples                                 # how many places on the lamp a shadow is tried from (more: softer edge)


def seg_hits(P, Q, occ, skip_near=0.0):
    """For each place P: does the straight way to Q pass through any of the boxes? P: 3 arrays; Q: 3 numbers or
    3 arrays. -> boolean array. (The slab test, for every box in turn.)"""
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


def shade(st, lamps, ambient, moon=None, attic=None, fast=False, seed=5, occ=None, expose=1.0):
    """Light every ray's landing place from the lamps (and the moon through the window). -> picture, rays x 3.

    ambient: function(X, Y, Z, N) -> light that is simply everywhere (rays x 3).
    moon: dict(dir=(toward the moon), color, power, window=(X0, X1, Y0, Y1, Zglass), bars=function(X, Y) -> 0..1)."""
    occ = st.occ if occ is None else occ
    X, Y, Z = st.places()
    N = st.N
    h, w = st.h, st.w
    ss = st.ss
    light = ambient(X, Y, Z, N).astype(F32)
    hit = st.t < 9e8
    thin = (st.flag & 1) > 0
    noshadow = (st.flag & 2) > 0
    rng = np.random.default_rng(seed)
    # shadows are worked out once per picture pixel (not per ray): one ray of each pixel stands for it
    o = ss // 2
    Xs, Ys, Zs = X[o::ss, o::ss], Y[o::ss, o::ss], Z[o::ss, o::ss]
    Ns = N[o::ss, o::ss]
    Ps = (Xs + Ns[..., 0] * 0.7, Ys + Ns[..., 1] * 0.7, Zs + Ns[..., 2] * 0.7)
    roof_s = st.mask_of("roofL", "roofR")[o::ss, o::ss]
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
            if lamp.double:
                ca = np.abs(ca)
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
                    one = np.where(blocked, 0.0, 1.0).astype(F32)
                    if attic is not None:
                        one *= attic.rafter_shadow(Pa, Q, roof_s[act])
                    acc += one
                vis[act] = acc / n
            vis = blur(vis, 0.7 if lamp.size < 12 else 2.2)
            vis = np.repeat(np.repeat(vis, ss, axis=0), ss, axis=1) if ss > 1 else vis
            vis = np.where(noshadow, 1.0, vis)
            direct = direct * vis
        light += (direct[..., None] * lamp.color[None, None, :]).astype(F32)
        if lamp.fill:
            light += ((lamp.fill * lamp.power / (0.6 + d2 / (lamp.reach * lamp.reach * 4)))[..., None] * lamp.color[None, None, :]).astype(F32)
    if moon is not None:
        m = np.asarray(moon["dir"], dtype=np.float64)
        m = m / np.linalg.norm(m)
        x0, x1, y0, y1, zg = moon["window"]
        ndl = np.clip(Ns[..., 0] * m[0] + Ns[..., 1] * m[1] + Ns[..., 2] * m[2], 0, 1)
        s = (zg - Ps[2]) / m[2]                                           # how far to the glass, going toward the moon
        Qx, Qy = Ps[0] + s * m[0], Ps[1] + s * m[1]
        through = (s > 0) & (Qx > x0) & (Qx < x1) & (Qy > y0) & (Qy < y1) & (ndl > 0) & hit[o::ss, o::ss]
        vis = np.zeros(through.shape, dtype=F32)
        if through.any():
            Pa = tuple(p[through] for p in Ps)
            Qa = (Qx[through], Qy[through], np.full(Pa[0].shape, zg, dtype=F32))
            blocked = seg_hits(Pa, Qa, occ, 0.0)
            vis[through] = np.where(blocked, 0.0, 1.0) * moon["bars"](Qx[through], Qy[through])
        vis = blur(vis, 0.9 if fast else 1.3)
        vis = np.repeat(np.repeat(vis, ss, axis=0), ss, axis=1) if ss > 1 else vis
        ndl_full = np.clip(N[..., 0] * m[0] + N[..., 1] * m[1] + N[..., 2] * m[2], 0, 1)
        light += ((vis * ndl_full * moon["power"])[..., None] * col(moon["color"])[None, None, :]).astype(F32)
        st.moonlit = (vis * ndl_full).astype(F32)             # where the moon falls (for the sheen it leaves on a varnished floor)
    out = st.alb * light * expose + st.emi
    out = 1 - np.exp(-out * 1.15)                                        # a soft shoulder: bright places do not go flat
    out = np.where(hit[..., None], out, 0)
    return out.astype(F32), light


def floor_contact(st, X, Z, feet, reach=9.0, amount=0.45):
    """Darkening of the floor round the foot of everything that stands on it (so it sits, and does not float)."""
    dark = np.zeros(X.shape, dtype=F32)
    for (x0, x1, z0, z1) in feet:
        dx = np.maximum(np.maximum(x0 - X, X - x1), 0)
        dz = np.maximum(np.maximum(z0 - Z, Z - z1), 0)
        d = np.sqrt(dx * dx + dz * dz)
        dark = np.maximum(dark, np.exp(-d / reach) * (d > 0))
    return dark * amount

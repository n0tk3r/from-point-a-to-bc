"""The painter's kit for Little Sister's room (home_lilsis_room.py; it began as the girls' room's kit): ONE camera, and everything through it.

A Painter holds the room's View, its lamps and the things that throw shadows. Every surface is painted in
its own measurements (centimetres) and lit from where the lamps really are, pixel by pixel:

    p.face(layer, [(X, Y, Z), ...], albedo)      a flat polygon in the room; albedo is a color or f(X, Y, Z, t)
    p.box(layer, X0, X1, Y0, Y1, Z0, Z1, albedo) the faces of a box that the lens can see, far ones first
    p.quad_image(layer, TL, TR, BL, picture)     a flat painted thing (a sign, a drawing) lying in the room
    p.ball(layer, centre, radius, albedo)        a round thing, lit as a round thing
    p.seg / p.path                               rods, cords, edges
    p.contact(layer, footprint)                  the dark where a thing meets the floor

A Layer is paint with its coverage, a `keep` map (how much of the crisp painting comes back after the brush
pass) and a fine sheet that is laid on after the brush pass. Nothing here touches the shared library."""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, blur, lerp, noise, rgb, sample

LUM = np.array([0.3, 0.55, 0.15], dtype=F32)


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


def mix(a, b, t):
    return lerp(col(a), col(b), t)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k, a[2] + b[2] * k)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def unit(a):
    k = math.sqrt(dot(a, a)) or 1.0
    return (a[0] / k, a[1] / k, a[2] / k)


# ---------------------------------------------------------------- small rasters, each in its own box
def _box_of(xs, ys, shape, pad=1.0):
    h, w = shape
    x0, x1 = max(0, int(math.floor(min(xs) - pad))), min(w, int(math.ceil(max(xs) + pad)) + 1)
    y0, y1 = max(0, int(math.floor(min(ys) - pad))), min(h, int(math.ceil(max(ys) + pad)) + 1)
    if x1 <= x0 or y1 <= y0:
        return None
    return y0, y1, x0, x1


def raster(pts, shape, ss=3):
    """A polygon -> ((y0, y1, x0, x1), mask) in its own bounding box, or None if it is off the picture."""
    sl = _box_of([p[0] for p in pts], [p[1] for p in pts], shape)
    if sl is None:
        return None
    y0, y1, x0, x1 = sl
    im = Image.new("L", ((x1 - x0) * ss, (y1 - y0) * ss), 0)
    ImageDraw.Draw(im).polygon([((x - x0) * ss, (y - y0) * ss) for x, y in pts], fill=255)
    return sl, np.asarray(im.resize((x1 - x0, y1 - y0), Image.BOX), dtype=F32) / 255


def raster_line(pts, width, shape, ss=3):
    sl = _box_of([p[0] for p in pts], [p[1] for p in pts], shape, pad=width / 2 + 1.5)
    if sl is None:
        return None
    y0, y1, x0, x1 = sl
    im = Image.new("L", ((x1 - x0) * ss, (y1 - y0) * ss), 0)
    d = ImageDraw.Draw(im)
    q = [((x - x0) * ss, (y - y0) * ss) for x, y in pts]
    wd = max(1, int(round(width * ss)))
    d.line(q, fill=255, width=wd, joint="curve")
    if wd > 2:
        r = wd / 2
        for px, py in (q[0], q[-1]):
            d.ellipse([px - r, py - r, px + r, py + r], fill=255)
    return sl, np.asarray(im.resize((x1 - x0, y1 - y0), Image.BOX), dtype=F32) / 255


def raster_ellipse(cx, cy, rx, ry, shape, rot=0.0):
    r = max(rx, ry)
    sl = _box_of([cx - r, cx + r], [cy - r, cy + r], shape)
    if sl is None:
        return None
    y0, y1, x0, x1 = sl
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(F32)
    dx, dy = xx + 0.5 - cx, yy + 0.5 - cy
    if rot:
        c, s = math.cos(rot), math.sin(rot)
        dx, dy = dx * c + dy * s, -dx * s + dy * c
    u, v = dx / max(rx, 1e-3), dy / max(ry, 1e-3)
    d = np.sqrt(u * u + v * v)
    m = np.clip((1 - d) * min(rx, ry) + 0.5, 0, 1).astype(F32)
    return sl, m, u, v


class Layer:
    """Paint (kept premultiplied by its coverage), a keep map, and a fine sheet for after the brush."""

    def __init__(self, shape):
        h, w = shape
        self.shape = shape
        self.c, self.a = np.zeros((h, w, 3), F32), np.zeros((h, w), F32)
        self.keep = np.zeros((h, w), F32)
        self.fc, self.fa = np.zeros((h, w, 3), F32), np.zeros((h, w), F32)

    def put(self, sl, color, m, keep=0.6, fine=False):
        y0, y1, x0, x1 = sl
        c, a = (self.fc, self.fa) if fine else (self.c, self.a)
        mm = m[..., None]
        c[y0:y1, x0:x1] = c[y0:y1, x0:x1] * (1 - mm) + color * mm
        a[y0:y1, x0:x1] = a[y0:y1, x0:x1] * (1 - m) + m
        if not fine:
            self.keep[y0:y1, x0:x1] = self.keep[y0:y1, x0:x1] * (1 - m) + keep * m

    def mul(self, sl, color, m, fine=False):
        """Darken (multiply toward a color) what is already there: shadows and glazes."""
        y0, y1, x0, x1 = sl
        c = self.fc if fine else self.c
        mm = m[..., None]
        c[y0:y1, x0:x1] = c[y0:y1, x0:x1] * (1 - mm + col(color) * mm)

    def screen(self, sl, color, m):
        """Add light to what is already there (only where there is paint)."""
        y0, y1, x0, x1 = sl
        a = self.a[y0:y1, x0:x1][..., None]
        c = self.c[y0:y1, x0:x1]
        self.c[y0:y1, x0:x1] = a - (a - c) * (1 - col(color) * m[..., None])

    def color(self):
        return self.c / np.maximum(self.a, 1e-4)[..., None]

    def fine(self):
        return self.fc / np.maximum(self.fa, 1e-4)[..., None]


def lines(u, period, width, fp, offset=0.0):
    """Coverage (0 to 1) of a set of lines every `period` in the coordinate `u`, each `width` wide, filtered
    by the size of a pixel `fp` measured in the same units, so that far lines fade instead of flickering."""
    d = (u - offset) / period
    d = (d - np.round(d)) * period                              # signed distance to the nearest line's middle
    fp = np.maximum(fp, 1e-3)
    cov = np.clip(np.minimum(d + fp / 2, width / 2) - np.maximum(d - fp / 2, -width / 2), 0, None) / fp
    far = np.clip((fp - period * 0.5) / (period * 0.5), 0, 1)   # more than half a period in a pixel: the average
    return (cov * (1 - far) + (width / period) * far).astype(F32)


def footprint(u):
    """How much the coordinate `u` changes across one pixel."""
    gy, gx = np.gradient(u)
    return np.hypot(gx, gy).astype(F32) + 1e-4


def hash01(i, j=0.0, seed=0.0):
    h = np.sin(i * 127.1 + j * 311.7 + seed * 74.7) * 43758.5453
    return (h - np.floor(h)).astype(F32)


class Tile:
    """A piece of cloudy noise to read at any place (X, Z in cm): for grain, stains and wear in a surface's own
    coordinates. It repeats, but nobody will see that."""

    def __init__(self, cell, seed, size=512, octaves=4):
        self.t = noise((size, size), cell, seed, octaves)
        self.size = size

    def at(self, u, v):
        s = self.size - 2
        return sample(self.t, np.mod(u, s), np.mod(v, s))


class Painter:
    def __init__(self, view, shape=(600, 800)):
        self.v, self.shape = view, shape
        rx, ry, rz = view._rays(shape)
        self.rx, self.ry, self.rz = rx.astype(F32), ry.astype(F32), rz.astype(F32)
        self.C = (view.cam_x, view.eye, view.cam_z)
        self.R = (view.rx, 0.0, view.rz)                         # to the right, as the lens sees it
        self.B = (-view.fx, 0.0, -view.fz)                       # back toward the lens
        self.lights, self.blockers = [], []
        self.ambient, self.night = col((0.30, 0.36, 0.66)), 0.45
        self.fill = None                                          # an optional f(X, Y, Z, n) -> extra soft light

    # ------------------------------------------------------------ where things are
    def pt(self, P):
        return self.v.pt(*P)

    def k(self, P):
        """Picture pixels per centimetre at a place in the room."""
        return self.v.F / max(self.v.cam_space(*P)[2], 1.0)

    def normal(self, pts):
        n = unit(cross(sub(pts[1], pts[0]), sub(pts[2], pts[0])))
        mid = [sum(p[i] for p in pts) / len(pts) for i in range(3)]
        return n if dot(n, sub(self.C, mid)) > 0 else (-n[0], -n[1], -n[2])

    def on_plane(self, sl, P0, n):
        y0, y1, x0, x1 = sl
        rx, ry, rz = self.rx[y0:y1, x0:x1], self.ry[y0:y1, x0:x1], self.rz[y0:y1, x0:x1]
        den = n[0] * rx + n[1] * ry + n[2] * rz
        num = n[0] * (P0[0] - self.C[0]) + n[1] * (P0[1] - self.C[1]) + n[2] * (P0[2] - self.C[2])
        den = np.where(np.abs(den) < 1e-7, 1e-7, den)
        t = np.clip(num / den, 1.0, 1e5).astype(F32)
        return self.C[0] + rx * t, self.C[1] + ry * t, self.C[2] + rz * t, t

    # ------------------------------------------------------------ light
    def visible(self, X, Y, Z, L, blockers=None, soft=1.5):
        """1 where the lamp at L can be seen from each place, 0 where something stands between."""
        h, w = X.shape
        st = 2 if min(h, w) >= 8 else 1
        Xs, Ys, Zs = X[::st, ::st], Y[::st, ::st], Z[::st, ::st]
        dx, dy, dz = L[0] - Xs, L[1] - Ys, L[2] - Zs
        vis = np.ones(Xs.shape, F32)
        with np.errstate(divide="ignore", invalid="ignore"):
            ix, iy, iz = 1.0 / np.where(np.abs(dx) < 1e-4, 1e-4, dx), 1.0 / np.where(np.abs(dy) < 1e-4, 1e-4, dy), 1.0 / np.where(np.abs(dz) < 1e-4, 1e-4, dz)
        for (X0, X1, Y0, Y1, Z0, Z1) in (self.blockers if blockers is None else blockers):
            ta, tb = (X0 - Xs) * ix, (X1 - Xs) * ix
            lo, hi = np.minimum(ta, tb), np.maximum(ta, tb)
            ta, tb = (Y0 - Ys) * iy, (Y1 - Ys) * iy
            lo, hi = np.maximum(lo, np.minimum(ta, tb)), np.minimum(hi, np.maximum(ta, tb))
            ta, tb = (Z0 - Zs) * iz, (Z1 - Zs) * iz
            lo, hi = np.maximum(lo, np.minimum(ta, tb)), np.minimum(hi, np.maximum(ta, tb))
            vis[(hi > np.maximum(lo, 0.004)) & (lo < 0.985)] = 0.0
        if st > 1:
            vis = np.repeat(np.repeat(vis, st, 0), st, 1)[:h, :w]
        if soft and min(h, w) > 6:
            vis = blur(vis, soft)
        return vis

    def arrive(self, L, X, Y, Z, n, shadow=False, blockers=None):
        if "dir" in L:
            m = L["dir"]
            I = L["power"] * np.clip(n[0] * m[0] + n[1] * m[1] + n[2] * m[2], 0, 1)
            return I * L["gate"](X, Y, Z)
        lx, ly, lz = L["pos"][0] - X, L["pos"][1] - Y, L["pos"][2] - Z
        d2 = lx * lx + ly * ly + lz * lz
        ndl = (n[0] * lx + n[1] * ly + n[2] * lz) / np.sqrt(d2 + 1e-3)
        wr = L.get("wrap", 0.22)
        I = L["power"] * np.clip(ndl * (1 - wr) + wr, 0, 1) / (1 + d2 / L["r"] ** 2)
        if L.get("gate"):
            I = I * L["gate"](X, Y, Z)
        if shadow and L.get("cast", True):
            I = I * self.visible(X, Y, Z, L["pos"], blockers, L.get("soft", 1.5))
        return I

    def shade(self, albedo, X, Y, Z, n, shadow=False, gain=1.0, amb=1.0, blockers=None, only=None):
        albedo = col(albedo) if not isinstance(albedo, np.ndarray) else albedo
        if albedo.ndim == 1:
            albedo = np.broadcast_to(albedo, np.shape(X) + (3,))
        lum = (albedo @ LUM)[..., None]
        amb = amb[..., None] if isinstance(amb, np.ndarray) else amb
        out = lerp(albedo, lum, self.night) * self.ambient * amb
        if self.fill is not None:
            out = out + albedo * self.fill(X, Y, Z, n)
        for L in self.lights:
            if only is not None and L["name"] not in only:
                continue
            I = self.arrive(L, X, Y, Z, n, shadow, blockers)
            out = out + albedo * L["color"] * np.asarray(I, dtype=F32)[..., None]
        return (out * gain).astype(F32)

    def shade_at(self, albedo, P, n, gain=1.0, amb=1.0):
        X, Y, Z = (np.full((1, 1), v, F32) for v in P)
        return self.shade(col(albedo), X, Y, Z, n, False, gain, amb)[0, 0]

    # ------------------------------------------------------------ flat things
    def face(self, layer, pts, albedo, n=None, keep=0.6, shadow=False, gain=1.0, amb=1.0, fine=False, alpha=1.0, lit=True, blockers=None, hole=None):
        """A flat polygon standing anywhere in the room. `albedo`: a color, or f(X, Y, Z, t) -> color(s)."""
        pp = self.v.poly(pts)
        if len(pp) < 3:
            return None
        r = raster(pp, self.shape)
        if r is None:
            return None
        sl, m = r
        if not m.any():
            return None
        n = n or self.normal(pts)
        X, Y, Z, t = self.on_plane(sl, pts[0], n)
        a = albedo(X, Y, Z, t) if callable(albedo) else col(albedo)
        if hole is not None:
            m = m * (1 - hole(X, Y, Z))
        if callable(amb):
            amb = amb(X, Y, Z)
        c = self.shade(a, X, Y, Z, n, shadow, gain, amb, blockers) if lit else (np.broadcast_to(a, X.shape + (3,)) * gain)
        layer.put(sl, c, m * alpha, keep, fine)
        return sl

    FACES = {
        "top": (lambda b: [(b[0], b[3], b[4]), (b[1], b[3], b[4]), (b[1], b[3], b[5]), (b[0], b[3], b[5])], (0, 1, 0)),
        "bottom": (lambda b: [(b[0], b[2], b[4]), (b[1], b[2], b[4]), (b[1], b[2], b[5]), (b[0], b[2], b[5])], (0, -1, 0)),
        "left": (lambda b: [(b[0], b[2], b[4]), (b[0], b[2], b[5]), (b[0], b[3], b[5]), (b[0], b[3], b[4])], (-1, 0, 0)),
        "right": (lambda b: [(b[1], b[2], b[4]), (b[1], b[2], b[5]), (b[1], b[3], b[5]), (b[1], b[3], b[4])], (1, 0, 0)),
        "back": (lambda b: [(b[0], b[2], b[4]), (b[1], b[2], b[4]), (b[1], b[3], b[4]), (b[0], b[3], b[4])], (0, 0, -1)),
        "front": (lambda b: [(b[0], b[2], b[5]), (b[1], b[2], b[5]), (b[1], b[3], b[5]), (b[0], b[3], b[5])], (0, 0, 1)),
    }

    def box_faces(self, b):
        """-> [(name, room points, normal)] for the faces of a box the lens can see, the farthest first."""
        seen = []
        for name, (make, n) in self.FACES.items():
            pts = make(b)
            mid = [sum(p[i] for p in pts) / 4 for i in range(3)]
            if dot(n, sub(self.C, mid)) <= 0:
                continue
            seen.append((self.v.cam_space(*mid)[2], name, pts, n))
        seen.sort(key=lambda s: -s[0])
        return [(name, pts, n) for _, name, pts, n in seen]

    def box(self, layer, X0, X1, Y0, Y1, Z0, Z1, albedo, keep=0.7, shadow=False, gain=1.0, fine=False, skip=(), amb=1.0, edge=None):
        """A box. `albedo`: one color (or f), or a dict by face name with "all" for the rest.
        `edge`: a color to run along the lit top edges afterwards, on the fine sheet."""
        b = (X0, X1, Y0, Y1, Z0, Z1)
        for name, pts, n in self.box_faces(b):
            if name in skip:
                continue
            a = albedo.get(name, albedo.get("all")) if isinstance(albedo, dict) else albedo
            if a is None:
                continue
            g = gain.get(name, gain.get("all", 1.0)) if isinstance(gain, dict) else gain
            self.face(layer, pts, a, n, keep, shadow, g, amb, fine)
        if edge is not None:
            for p, q in (((X0, Y1, Z1), (X1, Y1, Z1)), ((X0, Y1, Z0), (X0, Y1, Z1)), ((X1, Y1, Z0), (X1, Y1, Z1))):
                self.seg(layer, p, q, edge, 0.6, alpha=0.6)

    def quad_image(self, layer, TL, TR, BL, tex, alpha=None, keep=0.85, lit=True, gain=1.0, fine=False, amb=1.0, shadow=False, opacity=1.0):
        """A flat picture (h, w, 3) with optional coverage (h, w), lying in the room as the parallelogram
        whose corners are TL, TR, BL (and the fourth where it must be)."""
        e1, e2 = sub(TR, TL), sub(BL, TL)
        BR = add(TR, e2)
        pts = [TL, TR, BR, BL]
        pp = self.v.poly(pts)
        if len(pp) < 3:
            return None
        r = raster(pp, self.shape)
        if r is None:
            return None
        sl, m = r
        n = self.normal(pts)
        X, Y, Z, t = self.on_plane(sl, TL, n)
        dx, dy, dz = X - TL[0], Y - TL[1], Z - TL[2]
        u = (dx * e1[0] + dy * e1[1] + dz * e1[2]) / dot(e1, e1)
        v = (dx * e2[0] + dy * e2[1] + dz * e2[2]) / dot(e2, e2)
        th, tw = tex.shape[:2]
        # soften the picture first if it is being made much smaller, so that it does not glitter
        y0, y1, x0, x1 = sl
        shrink = max(tw / max(x1 - x0, 1), th / max(y1 - y0, 1)) * 0.5
        src, sa = tex, alpha
        if shrink > 1.2:
            src = blur(tex, shrink * 0.35)
            sa = blur(alpha, shrink * 0.35) if alpha is not None else None
        c = sample(src, u * (tw - 1), v * (th - 1))
        if sa is not None:
            m = m * sample(sa, u * (tw - 1), v * (th - 1))
        if lit:
            c = self.shade(c, X, Y, Z, n, shadow, gain, amb)
        else:
            c = c * gain
        layer.put(sl, c, m * opacity, keep, fine)
        return sl

    # ------------------------------------------------------------ round things
    def ball(self, layer, P, r_cm, albedo, sx=1.0, sy=1.0, rot=0.0, keep=0.7, fine=False, gain=1.0, flat=0.0, amb=1.0, alpha=1.0, spots=None):
        """A round thing (a head, a cushion, a globe) lit as a ball. sx, sy stretch it across and up."""
        x, y = self.pt(P)
        k = self.k(P)
        r = raster_ellipse(x, y, max(r_cm * sx * k, 0.6), max(r_cm * sy * k, 0.6), self.shape, rot)
        if r is None:
            return None
        sl, m, u, v = r
        if not m.any():
            return None
        if rot:
            c, s = math.cos(rot), math.sin(rot)
            u, v = u * c - v * s, u * s + v * c
        nz = np.sqrt(np.clip(1 - u * u - v * v, 0.0, 1))
        u, v = u * (1 - flat), v * (1 - flat)
        nz = np.sqrt(np.clip(1 - u * u - v * v, 0.02, 1))
        n = (u * self.R[0] + nz * self.B[0], -v + 0 * u, u * self.R[2] + nz * self.B[2])
        X, Y, Z = P[0] + n[0] * r_cm, P[1] + n[1] * r_cm, P[2] + n[2] * r_cm
        a = col(albedo) if not callable(albedo) else albedo(u, v)
        if spots is not None:
            a = spots(u, v, np.broadcast_to(a, u.shape + (3,)).copy())
        c = self.shade(a, X, Y, Z, n, False, gain, amb)
        layer.put(sl, c, m * alpha, keep, fine)
        return sl

    # ------------------------------------------------------------ rods, cords and edges
    def seg(self, layer, p, q, color, w_cm=1.0, min_px=0.8, alpha=1.0, fine=True, lit=None, keep=0.85, gain=1.0, max_px=None):
        """A straight rod or line between two places in the room. `lit` = a normal: then `color` is its
        own color and the lamps light it; otherwise `color` is laid down as it is."""
        ln = self.v.line(p, q)
        if ln is None:
            return
        mid = tuple((p[i] + q[i]) / 2 for i in range(3))
        wd = max(min_px, w_cm * self.k(mid))
        if max_px:
            wd = min(wd, max_px)
        r = raster_line(list(ln), wd, self.shape)
        if r is None:
            return
        sl, m = r
        c = self.shade_at(color, mid, lit, gain) if lit is not None else col(color) * gain
        layer.put(sl, c, m * alpha, keep, fine)

    def path(self, layer, pts, color, w_cm=1.0, min_px=0.8, alpha=1.0, fine=True, lit=None, keep=0.85, gain=1.0):
        for a, b in zip(pts[:-1], pts[1:]):
            self.seg(layer, a, b, color, w_cm, min_px, alpha, fine, lit, keep, gain)

    def line2(self, layer, pts, color, width=1.0, alpha=1.0, fine=True, keep=0.85):
        r = raster_line(pts, width, self.shape)
        if r is not None:
            layer.put(r[0], col(color), r[1] * alpha, keep, fine)

    def poly2(self, layer, pts, color, alpha=1.0, fine=True, keep=0.85):
        r = raster(pts, self.shape)
        if r is not None:
            layer.put(r[0], col(color), r[1] * alpha, keep, fine)

    def dot2(self, layer, x, y, rx, ry, color, alpha=1.0, fine=True, keep=0.85, rot=0.0):
        r = raster_ellipse(x, y, rx, ry, self.shape, rot)
        if r is not None:
            layer.put(r[0], col(color), r[1] * alpha, keep, fine)

    def dot(self, layer, P, r_cm, color, alpha=1.0, fine=True, keep=0.85, sx=1.0, sy=1.0, min_px=0.6, lit=None, gain=1.0):
        x, y = self.pt(P)
        k = self.k(P)
        c = self.shade_at(color, P, lit, gain) if lit is not None else col(color) * gain
        self.dot2(layer, x, y, max(min_px, r_cm * sx * k), max(min_px, r_cm * sy * k), c, alpha, fine, keep)

    def poly3(self, layer, pts, color, alpha=1.0, fine=True, keep=0.85, lit=None, gain=1.0):
        """A small flat shape in the room laid down in one color (lit at its middle if `lit` is a normal)."""
        pp = self.v.poly(pts)
        if len(pp) < 3:
            return
        mid = tuple(sum(p[i] for p in pts) / len(pts) for i in range(3))
        c = self.shade_at(color, mid, lit, gain) if lit is not None else col(color) * gain
        self.poly2(layer, pp, c, alpha, fine, keep)

    # ------------------------------------------------------------ shadow and glow
    def contact(self, layer, pts, strength=0.5, soft=3.0, color=(0.30, 0.26, 0.42), grow=0.0):
        """Darken the paint already on the layer inside a polygon in the room (soft edge): where a thing
        meets the floor or a wall."""
        pp = self.v.poly(pts)
        if len(pp) < 3:
            return
        if grow:
            cx, cy = sum(p[0] for p in pp) / len(pp), sum(p[1] for p in pp) / len(pp)
            pp = [(cx + (x - cx) * (1 + grow), cy + (y - cy) * (1 + grow)) for x, y in pp]
        self.shade2(layer, pp, strength, soft, color)

    def shade2(self, layer, pp, strength=0.5, soft=3.0, color=(0.30, 0.26, 0.42), fine=False):
        h, w = self.shape
        pad = int(soft * 3) + 2
        sl = _box_of([p[0] for p in pp], [p[1] for p in pp], self.shape, pad=pad)
        if sl is None:
            return
        y0, y1, x0, x1 = sl
        im = Image.new("L", ((x1 - x0) * 2, (y1 - y0) * 2), 0)
        ImageDraw.Draw(im).polygon([((x - x0) * 2, (y - y0) * 2) for x, y in pp], fill=255)
        m = np.asarray(im.resize((x1 - x0, y1 - y0), Image.BOX), dtype=F32) / 255
        if soft and min(m.shape) > 4:
            m = blur(m, soft)
        layer.mul(sl, color, np.clip(m * strength, 0, 1), fine)

    def light_on(self, layer, pts, fn, color):
        """Lay light (screen) over the paint already on a flat polygon in the room: fn(X, Y, Z) says how much, place by place."""
        pp = self.v.poly(pts)
        if len(pp) < 3:
            return
        r = raster(pp, self.shape)
        if r is None:
            return
        sl, m = r
        X, Y, Z, t = self.on_plane(sl, pts[0], self.normal(pts))
        layer.screen(sl, color, (m * np.clip(fn(X, Y, Z), 0, 1)).astype(F32))

    def glow(self, layer, P, r_px, color, amount=0.6):
        """A small soft light laid over the paint (a bulb's halo on what is right behind it)."""
        x, y = self.pt(P) if len(P) == 3 else P
        sl = _box_of([x - r_px * 2.5, x + r_px * 2.5], [y - r_px * 2.5, y + r_px * 2.5], self.shape)
        if sl is None:
            return
        y0, y1, x0, x1 = sl
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(F32)
        d2 = ((xx + 0.5 - x) ** 2 + (yy + 0.5 - y) ** 2) / (r_px * r_px)
        layer.screen(sl, color, (np.exp(-d2) * amount).astype(F32))


# ---------------------------------------------------------------- small flat pictures, drawn big and laid in the room
class Card:
    """A sheet to draw a flat thing on (a child's drawing, a sign, a rug), `ppc` pixels to the centimetre."""

    def __init__(self, w_cm, h_cm, ground, ppc=4.0, clear=False):
        self.ppc = ppc
        self.w, self.h = max(2, int(round(w_cm * ppc))), max(2, int(round(h_cm * ppc)))
        g = tuple(int(v * 255) for v in col(ground))
        self.im = Image.new("RGBA", (self.w, self.h), g + ((0,) if clear else (255,)))
        self.d = ImageDraw.Draw(self.im)

    def ink(self, color, alpha=1.0):
        return tuple(int(v * 255) for v in np.clip(col(color), 0, 1)) + (int(alpha * 255),)

    def P(self, pts):
        return [(x * self.ppc, y * self.ppc) for x, y in pts]

    def line(self, pts, color, w_cm=0.5, alpha=1.0):
        q = self.P(pts)
        wd = max(1, int(round(w_cm * self.ppc)))
        self.d.line(q, fill=self.ink(color, alpha), width=wd, joint="curve")
        if wd > 2:
            r = wd / 2
            for px, py in (q[0], q[-1]):
                self.d.ellipse([px - r, py - r, px + r, py + r], fill=self.ink(color, alpha))
        return self

    def poly(self, pts, color, alpha=1.0):
        self.d.polygon(self.P(pts), fill=self.ink(color, alpha))
        return self

    def rect(self, x0, y0, x1, y1, color, alpha=1.0):
        return self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], color, alpha)

    def disc(self, x, y, rx, color, ry=None, alpha=1.0):
        ry = rx if ry is None else ry
        k = self.ppc
        self.d.ellipse([(x - rx) * k, (y - ry) * k, (x + rx) * k, (y + ry) * k], fill=self.ink(color, alpha))
        return self

    def ring(self, x, y, r, color, w_cm=0.5):
        k = self.ppc
        self.d.ellipse([(x - r) * k, (y - r) * k, (x + r) * k, (y + r) * k], outline=self.ink(color), width=max(1, int(round(w_cm * k))))
        return self

    def done(self, rough=0.0, seed=0):
        """-> (color (h, w, 3), coverage (h, w)) as floats."""
        a = np.asarray(self.im, dtype=F32) / 255
        c, al = a[..., :3].copy(), a[..., 3].copy()
        if rough:
            n = noise((self.h, self.w), max(4.0, self.ppc * 3), seed, 3) - 0.5
            c = np.clip(c * (1 + n[..., None] * rough), 0, 1)
        return c, al

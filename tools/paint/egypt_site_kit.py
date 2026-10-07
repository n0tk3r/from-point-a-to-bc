"""Measuring tools for the building site at the foot of the Great Pyramid (egypt_site.py).

Everything solid in that picture is placed in the world first and then looked at through the game's own
camera (persp.Camera), so the casing courses, the stair, the doorway, the sledge and the people the game
draws all agree about size and distance.

World measurements are centimetres: X to the right of the lens, Y up from the flat sand, and Zc straight
away from the lens (not from the `full` row, as persp counts it: Zc = z + Z0)."""

import math

import numpy as np

from brush import *
import persp

W, H = 800, 600
HZ, FULL = 250, 590
CAM = persp.Camera(HZ, FULL)
EYE, FOC, Z0 = CAM.eye, CAM.F, CAM.Z0


# ---------------------------------------------------------------- places
def P(X, Y, Zc):
    """World -> picture."""
    k = FOC / Zc
    return (CAM.vx + X * k, CAM.vy + (EYE - Y) * k)


def floor_at(px, py):
    """Picture place on the flat sand -> world (X, Zc)."""
    Zc = EYE * FOC / max(py - HZ, 1e-3)
    return ((px - CAM.vx) * Zc / FOC, Zc)


def row_of(Zc):
    """The picture row of the sand that far away."""
    return HZ + EYE * FOC / Zc


def size_at(py):
    """How many pixels a centimetre is, for something standing on the sand at this row."""
    return (py - HZ) / EYE


def person(py):
    """How tall the game draws a grown-up whose feet are on this row."""
    return 160.0 * (py - HZ) / (FULL - HZ)


class Frame:
    """A thing standing on the sand, measured in its own length (u), height (v) and depth (d, away from
    us). `at` is the picture place of its origin; `turn` swings its far end away from us, in degrees
    (positive: the +u end goes into the picture)."""

    def __init__(self, at=None, turn=0.0, lift=0.0, world=None):
        self.X0, self.Zc0 = floor_at(*at) if world is None else world
        a = math.radians(turn)
        self.c, self.s, self.lift = math.cos(a), math.sin(a), lift

    def w(self, u, v=0.0, d=0.0):
        return (self.X0 + u * self.c - d * self.s, v + self.lift, self.Zc0 + u * self.s + d * self.c)

    def pt(self, u, v=0.0, d=0.0):
        return P(*self.w(u, v, d))

    def pts(self, points):
        return [self.pt(*p) for p in points]

    def poly(self, sheet, points, color, alpha=1.0):
        sheet.poly(self.pts(points), color, alpha)
        return self

    def line(self, sheet, points, color, width=1.0, alpha=1.0):
        sheet.line(self.pts(points), color, width, alpha)
        return self

    def k(self, u=0.0, d=0.0):
        """Pixels per centimetre at a place in the frame."""
        return FOC / (self.Zc0 + u * self.s + d * self.c)

    def box(self, sheet, u0, u1, v0, v1, d0, d1, front, top, left, right=None, back=None, alpha=1.0):
        """A box: draws the faces the lens can see, far ones first. `left` is the u0 end, `right` the u1 end."""
        right = left if right is None else right
        faces = []
        cx, cy, cz = self.w((u0 + u1) / 2, (v0 + v1) / 2, (d0 + d1) / 2)
        ends = [((u0, v0, d0), (u0, v0, d1), (u0, v1, d1), (u0, v1, d0), left, (-self.c, -self.s)),
                ((u1, v0, d0), (u1, v0, d1), (u1, v1, d1), (u1, v1, d0), right, (self.c, self.s)),
                ((u0, v0, d0), (u1, v0, d0), (u1, v1, d0), (u0, v1, d0), front, (self.s, -self.c)),
                ((u0, v0, d1), (u1, v0, d1), (u1, v1, d1), (u0, v1, d1), back or front, (-self.s, self.c))]
        for a, b, c, e, col, (nx, nz) in ends:
            mx, my, mz = self.w((a[0] + c[0]) / 2, (a[1] + c[1]) / 2, (a[2] + c[2]) / 2)
            if nx * (0 - mx) + nz * (0 - mz) > 0:                       # it faces the lens
                faces.append((mz, [a, b, c, e], col))
        for _, quad, col in sorted(faces, key=lambda f: -f[0]):
            self.poly(sheet, quad, col, alpha)
        if v1 + self.lift < EYE:
            self.poly(sheet, [(u0, v1, d0), (u1, v1, d0), (u1, v1, d1), (u0, v1, d1)], top, alpha)
        return self


# ---------------------------------------------------------------- the sun
SUN_LONG = 0.95                     # a shadow is this many times as long as the thing is tall
SUN_TURN = 30.0                     # and falls to the right, this many degrees toward us
_a = math.radians(SUN_TURN)
SHADOW = (SUN_LONG * math.cos(_a), -SUN_LONG * math.sin(_a))            # where the shadow of a point 1 cm up lands, in (X, Zc)


def shade_of(world_points):
    """Picture places where the shadows of some world points fall on the sand."""
    return [P(X + SHADOW[0] * Y, 0.0, max(Zc + SHADOW[1] * Y, 60.0)) for X, Y, Zc in world_points]


def hull(points):
    """The outline round a set of picture points (convex), for a shadow."""
    pts = sorted(set((round(float(x), 2), round(float(y), 2)) for x, y in points))
    if len(pts) < 3:
        return pts

    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2 and (out[-1][0] - out[-2][0]) * (p[1] - out[-2][1]) - (out[-1][1] - out[-2][1]) * (p[0] - out[-2][0]) <= 0:
                out.pop()
            out.append(p)
        return out[:-1]
    return half(pts) + half(pts[::-1])


def cast_box(shape, frame, u0, u1, v1, d0, d1, v0=0.0, soft=1.2):
    """The shadow a box in a frame throws on the sand, as a mask."""
    top = [frame.w(u, v1, d) for u in (u0, u1) for d in (d0, d1)]
    low = [frame.w(u, v0, d) for u in (u0, u1) for d in (d0, d1)]
    return mask_poly(shape, hull(shade_of(top) + shade_of(low)), soft=soft)


def shadow(picture, mask, amount=0.46, color="#6e5688", cool=0.10):
    """Sand under a shadow: darker (a glaze, as in the riverbank picture) and a little toward violet."""
    m = np.clip(mask, 0, 1).astype(F32)
    tint(picture, color, m * amount)
    over(picture, "#6f5c96", m * cool)
    return picture


# ---------------------------------------------------------------- the pyramid, as two planes
class Slope:
    """One face of the pyramid. `s` runs along its foot from the near corner, `u` up the stone."""

    def __init__(self, corner, along, inward, beta, length):
        self.C = np.array(corner, dtype=float)
        self.d = np.array([along[0], 0.0, along[1]])
        self.cb, self.sb = math.cos(math.radians(beta)), math.sin(math.radians(beta))
        self.n = np.array([inward[0], 0.0, inward[1]])
        self.w = self.n * self.cb + np.array([0.0, self.sb, 0.0])
        self.N = np.cross(self.d, self.w)
        self.L = length

    def at(self, s, v, out=0.0):
        """World place `s` along the foot and `v` centimetres above it; `out` stands off the stone."""
        p = self.C + s * self.d + (v / self.sb) * self.w
        if out:
            nrm = self.N / np.linalg.norm(self.N)
            if nrm[1] < 0:
                nrm = -nrm
            p = p + nrm * out
        return tuple(p)

    def pt(self, s, v, out=0.0):
        return P(*self.at(s, v, out))

    def plumb(self, s, v, q):
        """World place level with (s, v) but `q` cm into the pyramid from the stone's surface there
        (negative: out in the air in front of it)."""
        return tuple(self.C + s * self.d + (v / self.sb) * self.w + q * self.n)

    def coords(self, shape):
        """For every pixel: s, height v, distance Zc, and whether the pixel is on this face."""
        x, y = grid(shape)
        rx, ry = (x - CAM.vx) / FOC, -(y - CAM.vy) / FOC
        E = np.array([0.0, EYE, 0.0])
        den = self.N[0] * rx + self.N[1] * ry + self.N[2]
        den = np.where(np.abs(den) < 1e-9, 1e-9, den)
        t = float(self.N @ (self.C - E)) / den
        rel = np.stack([rx * t - self.C[0], EYE + ry * t - self.C[1], t - self.C[2]], axis=-1)
        s = rel @ self.d
        u = rel @ self.w
        on = (t > 0) & (u >= 0) & (s >= u * self.cb) & (s <= self.L - u * self.cb)
        return s.astype(F32), (u * self.sb).astype(F32), t.astype(F32), on


def masonry(s, v, on, seed, course=(98, 122), block=(120, 270), top=3000.0):
    """Courses of blocks on a face. -> (course number, a number 0..1 for each block, cm to the nearest
    level joint, cm to the nearest upright joint, place up the course 0..1, place along the block 0..1, block length cm)."""
    rng = np.random.default_rng(seed)
    levels = [0.0]
    while levels[-1] < top:
        t = min(levels[-1] / 1400.0, 1.0)
        levels.append(levels[-1] + lerp(course[1], course[0], t) * (0.92 + 0.16 * rng.random()))
    levels = np.array(levels)
    k = np.clip(np.searchsorted(levels, v, side="right") - 1, 0, len(levels) - 2)
    v0, v1 = levels[k], levels[k + 1]
    fv = (v - v0) / (v1 - v0)
    dv = np.minimum(v - v0, v1 - v)
    tone = np.zeros(s.shape, dtype=F32)
    ds = np.full(s.shape, 1e6, dtype=F32)
    fs = np.zeros(s.shape, dtype=F32)
    wide = np.ones(s.shape, dtype=F32)
    smax = float(s[on].max()) + 400 if on.any() else 1000.0
    for c in np.unique(k[on]) if on.any() else []:
        edges = [-300.0 - rng.random() * 200]
        while edges[-1] < smax:
            edges.append(edges[-1] + block[0] + (block[1] - block[0]) * rng.random() ** 1.3)
        edges = np.array(edges)
        tones = rng.random(len(edges))
        here = on & (k == c)
        j = np.clip(np.searchsorted(edges, s[here], side="right") - 1, 0, len(edges) - 2)
        tone[here] = tones[j]
        ds[here] = np.minimum(s[here] - edges[j], edges[j + 1] - s[here])
        fs[here] = (s[here] - edges[j]) / (edges[j + 1] - edges[j])
        wide[here] = edges[j + 1] - edges[j]
    return k, tone, dv.astype(F32), ds, fv.astype(F32), fs, wide, levels


def joint(dist_cm, zc, width=1.0, squash=1.0):
    """A joint as a mask, `width` pixels wide wherever it is: dist is in cm on the stone, zc how far off it is."""
    px = dist_cm * FOC / zc * squash
    return np.clip(width * 0.5 + 0.5 - px, 0, 1).astype(F32)


# ---------------------------------------------------------------- ways worn in the sand, measured on the ground
def floor_grid(shape):
    """For every pixel: the place on the sand it shows, as (X, Zc, below-the-horizon)."""
    x, y = grid(shape)
    Zc = EYE * FOC / np.maximum(y - HZ, 0.35)
    return ((x - CAM.vx) * Zc / FOC).astype(F32), Zc.astype(F32), (y > HZ + 0.5)


def ground_path(points, steps=10):
    """Picture places on the sand -> a smooth path on the ground (X, Zc)."""
    return curve([floor_at(*p) for p in points], steps)


def offset_path(path, off):
    """The same path moved `off` cm to its right-hand side."""
    out = []
    for i, (px, pz) in enumerate(path):
        a, b = path[max(i - 1, 0)], path[min(i + 1, len(path) - 1)]
        dx, dz = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dz) + 1e-6
        out.append((px + dz / n * off, pz - dx / n * off))
    return out


def ground_dist(shape, path):
    """How far (cm, on the ground) every pixel of sand is from a path."""
    X, Z, below = floor_grid(shape)
    best = np.full(shape, 1e9, dtype=F32)
    for (ax, az), (bx, bz) in zip(path[:-1], path[1:]):
        dx, dz = bx - ax, bz - az
        t = np.clip(((X - ax) * dx + (Z - az) * dz) / (dx * dx + dz * dz + 1e-6), 0, 1)
        best = np.minimum(best, np.hypot(X - (ax + t * dx), Z - (az + t * dz)))
    return best


def ground_line(shape, path, wide, soft=10.0):
    """A band `wide` cm across lying along a path on the sand, in true perspective."""
    X, Z, below = floor_grid(shape)
    return (np.clip((wide / 2 - ground_dist(shape, path)) / soft + 0.5, 0, 1) * below).astype(F32)


def ground_tex(shape, seed, cell=60.0, stretch=(1.0, 1.0)):
    """Noise that lies on the sand (cell in cm)."""
    X, Z, below = floor_grid(shape)
    tile = noise((512, 512), 32, seed, 4)
    return sample(tile, mirror(X * 32.0 / (cell * stretch[0]), 510), mirror(Z * 32.0 / (cell * stretch[1]), 510))


def mirror(v, size):
    """Fold a coordinate back and forth over 0..size, so a texture can go on for ever without a seam."""
    return np.abs(((v + size * 64) % (size * 2)) - size)


# ---------------------------------------------------------------- a sheet whose thin paint really is thin
class Paper(Sheet):
    """brush.Sheet draws a half-transparent stroke by REPLACING what is under it on the sheet (so paint
    already there is lost, and on a cut-out a hole appears). That is right for the library's own use
    (thin strokes on bare sheet). Here thin paint is often glazed over solid paint, so this sheet mixes
    it in properly. (Worked round here rather than changed in brush.py.)"""

    def _blend(self, box, draw):
        from PIL import Image, ImageDraw
        w, h = self.im.size
        x0, y0 = int(max(0, math.floor(box[0]) - 2)), int(max(0, math.floor(box[1]) - 2))
        x1, y1 = int(min(w, math.ceil(box[2]) + 3)), int(min(h, math.ceil(box[3]) + 3))
        if x1 <= x0 or y1 <= y0:
            return self
        layer = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        draw(ImageDraw.Draw(layer), -x0, -y0)
        part = self.im.crop((x0, y0, x1, y1))
        part.alpha_composite(layer)
        self.im.paste(part, (x0, y0))
        return self

    def line(self, points, color, width=1.0, alpha=1.0, round_ends=True):
        if alpha >= 0.999:
            return Sheet.line(self, points, color, width, alpha, round_ends)
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        wd = max(1, int(round(width * s)))
        fill = self._fill(color, alpha)

        def draw(d, ox, oy):
            q = [(x + ox, y + oy) for x, y in pts]
            d.line(q, fill=fill, width=wd, joint="curve")
            if round_ends and wd > 2:
                r = wd / 2
                for px, py in (q[0], q[-1]):
                    d.ellipse([px - r, py - r, px + r, py + r], fill=fill)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return self._blend((min(xs) - wd, min(ys) - wd, max(xs) + wd, max(ys) + wd), draw)

    def poly(self, points, color, alpha=1.0):
        if alpha >= 0.999:
            return Sheet.poly(self, points, color, alpha)
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        fill = self._fill(color, alpha)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return self._blend((min(xs), min(ys), max(xs), max(ys)), lambda d, ox, oy: d.polygon([(x + ox, y + oy) for x, y in pts], fill=fill))

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0):
        if alpha >= 0.999:
            return Sheet.ellipse(self, cx, cy, rx, ry, color, alpha)
        s = self.ss
        fill = self._fill(color, alpha)
        box = ((cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s)
        return self._blend(box, lambda d, ox, oy: d.ellipse([box[0] + ox, box[1] + oy, box[2] + ox, box[3] + oy], fill=fill))

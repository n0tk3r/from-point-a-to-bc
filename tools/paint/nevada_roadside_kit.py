"""Tools for the Nevada roadside.

Everything that stands in this picture (the car, the pump, the stand, the shack, the fence, the poles)
is drawn in TRUE perspective through the same camera the game uses for its people, so a table is the
right height for somebody standing at it and a far fence post is the right size for where it is.
The same drawing, laid flat along the sun's rays, gives each thing its own true shadow.

World measurements are centimetres: x to the right of the middle of the picture, y UP, z away from us
(z = 0 is the ground at the picture row `FULL`)."""

import math

import numpy as np

from brush import *
from persp import Camera
from solid import Draft, mix

W, H = 800, 600
HZ, FULL = 290, 590
CAM = Camera(HZ, FULL)
# The sun is low on the right and a little behind our right shoulder. A point one centimetre above the
# ground throws its shadow SUN[0] cm along x and SUN[1] cm along z: far to the left, a little away from us.
SUN = (-1.95, 0.36)
SHADOW = "#6c5f9c"                                          # what a shadow does to the ground: cooler, bluer


# ---------------------------------------------------------------- the ground under the camera
def gp(x, z, y=0.0):
    """World place -> picture place."""
    return CAM.pt(x, y, z)


def kz(z):
    """Picture pixels per centimetre at depth z."""
    return CAM.scale(z)


def row(z):
    """The picture row of the ground at depth z."""
    return CAM.pt(0, 0, z)[1]


def unproject(px, py):
    """A place on the ground in the picture -> (x, z) in the world."""
    z = CAM.depth_at(py)
    return CAM.x_at(px, py), z


def path(points, steps=0):
    """World (x, z) points on the ground -> picture points; with `steps` they are first joined by a smooth curve."""
    pts = curve(points, steps) if steps else points
    return [gp(x, z) for x, z in pts]


def ground_poly(shape, points, soft=0.0, wobble=0.0, seed=0):
    """A mask for a patch of ground outlined in the world."""
    return mask_poly(shape, [gp(x, z) for x, z in points], soft=soft, wobble=wobble, seed=seed)


def strip(shape, points, width_cm, soft=0.0, steps=10):
    """A band of even width ON THE GROUND (a rut, a painted line), following world points."""
    pts = curve(points, steps) if steps else points
    px = [gp(x, z) for x, z in pts]
    wd = [max(0.6, width_cm * kz(z) * 0.62) for x, z in pts]     # seen aslant, a band on the ground looks thinner
    return mask_line(shape, px, wd, soft=soft)


def floor(shape):
    """For every pixel: where on the ground it is. -> (x cm, z cm, mask of pixels below the horizon)."""
    return CAM.floor_grid(shape)


def tone(color, f, warm=0.0):
    """A color made lighter (f > 1) or darker (f < 1), and a touch warmer or cooler."""
    c = rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
    c = c * f if f <= 1 else 1 - (1 - c) / f
    c = c + np.array([warm, warm * 0.2, -warm], dtype=F32)
    return np.clip(c, 0, 1)


# ---------------------------------------------------------------- a sheet that takes thin paint
class Paper(Sheet):
    """brush.Sheet draws half-clear shapes by REPLACING what is under them (so a glaze over a solid shape
    leaves a half-clear hole in it). On this sheet thin paint really lies over what is already there."""

    def _glaze(self, box, color, alpha, draw):
        from PIL import Image, ImageDraw
        w, h = self.im.size
        x0, y0, x1, y1 = max(int(math.floor(box[0])) - 2, 0), max(int(math.floor(box[1])) - 2, 0), min(int(math.ceil(box[2])) + 3, w), min(int(math.ceil(box[3])) + 3, h)
        if x1 <= x0 or y1 <= y0:
            return self
        m = Image.new("L", (x1 - x0, y1 - y0), 0)
        draw(ImageDraw.Draw(m), x0, y0, int(round(alpha * 255)))
        r, g, b, _ = self._fill(color, 1.0)
        layer = Image.new("RGBA", m.size, (r, g, b, 0))
        layer.putalpha(m)
        self.im.alpha_composite(layer, (x0, y0))
        return self

    def poly(self, points, color, alpha=1.0):
        if alpha >= 0.995:
            return super().poly(points, color, alpha)
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        box = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
        return self._glaze(box, color, alpha, lambda d, ox, oy, v: d.polygon([(px - ox, py - oy) for px, py in pts], fill=v))

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0):
        if alpha >= 0.995:
            return super().ellipse(cx, cy, rx, ry, color, alpha)
        s = self.ss
        box = ((cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s)
        return self._glaze(box, color, alpha, lambda d, ox, oy, v: d.ellipse([box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy], fill=v))

    def line(self, points, color, width=1.0, alpha=1.0, round_ends=True):
        if alpha >= 0.995:
            return super().line(points, color, width, alpha, round_ends)
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        wd = max(1, int(round(width * s)))
        r = wd / 2 + 1
        box = (min(p[0] for p in pts) - r, min(p[1] for p in pts) - r, max(p[0] for p in pts) + r, max(p[1] for p in pts) + r)

        def draw(d, ox, oy, v):
            q = [(px - ox, py - oy) for px, py in pts]
            d.line(q, fill=v, width=wd, joint="curve")
            if round_ends and wd > 2:
                for px, py in (q[0], q[-1]):
                    d.ellipse([px - wd / 2, py - wd / 2, px + wd / 2, py + wd / 2], fill=v)
        return self._glaze(box, color, alpha, draw)


# ---------------------------------------------------------------- solid things in true perspective
class Solid(Draft):
    """solid.Draft, but through the scene's camera. The thing is drawn in its own measurements (x along it,
    y up, z back, away from us), stands at the world place `at` = (x, z) and is turned by `yaw` degrees
    (positive brings its right-hand end toward us)."""

    shade = False

    def __init__(self, sheet, at, yaw=0.0, unit=1.0, lift=0.0, cam=CAM):
        self.s, self.cam = sheet, cam
        self.wx, self.wz, self.lift, self.unit = float(at[0]), float(at[1]), lift, unit
        a = math.radians(yaw)
        self.cy, self.sy = math.cos(a), math.sin(a)
        self.k = cam.scale(self.wz) * unit                  # pixels per unit where it stands: line widths use it
        self.o, self.pv, self.dz, self.ca, self.sa = cam.pt(self.wx, 0, self.wz), (0.0, 0.0), (1.0, 1.0), 1.0, 0.0

    def world(self, x, y, z=0.0):
        u = self.unit
        return (self.wx + (x * self.cy + z * self.sy) * u, self.lift + y * u, self.wz + (-x * self.sy + z * self.cy) * u)

    def pt(self, x, y, z=0.0):
        return self.cam.pt(*self.world(x, y, z))

    def kat(self, x, y, z=0.0):
        """Pixels per unit at a place on the thing."""
        return self.cam.scale(self.world(x, y, z)[2]) * self.unit

    def seen_from(self):
        """Where the camera is, in the thing's own measurements (x, z): tells which faces we can see."""
        dx, dz = (0.0 - self.wx) / self.unit, (-self.cam.Z0 - self.wz) / self.unit
        return dx * self.cy - dz * self.sy, dx * self.sy + dz * self.cy

    def box(self, x0, x1, y0, y1, z0, z1, front, top, end, alpha=1.0, back=None):
        """A box: whichever end we can see, its top if it is below the eye, and its front."""
        cx, cz = self.seen_from()
        if cx > x1:
            self.poly([(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)], end, alpha)
        elif cx < x0:
            self.poly([(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)], end if back is None else back, alpha)
        if self.shade or self.lift + y1 * self.unit < self.cam.eye:
            self.poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], top, alpha)
        self.poly([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], front, alpha)
        return self

    def hring(self, cx, y, cz, rx, rz=None, n=28, a0=0.0, a1=360.0):
        """Points round a level circle (or part of one), counter-clockwise seen from above, 0 degrees = +x."""
        rz = rx if rz is None else rz
        out = []
        for i in range(n + 1 if a1 - a0 < 359.9 else n):
            a = math.radians(a0 + (a1 - a0) * i / n)
            out.append((cx + math.cos(a) * rx, y, cz + math.sin(a) * rz))
        return out

    def hdisc(self, cx, y, cz, rx, color, alpha=1.0, rz=None, n=28):
        """A level disc: a table top, the lid of a drum, a pool."""
        self.poly(self.hring(cx, y, cz, rx, rz, n), color, alpha)
        return self

    def ball(self, x, y, z, r, color, alpha=1.0, squash=1.0):
        px, py = self.pt(x, y, z)
        k = self.kat(x, y, z)
        self.s.ellipse(px, py, r * k, r * k * squash, color, alpha)
        return self

    def tube(self, cx, cz, r, y0, y1, tones, n=8, cap=None, r1=None, alpha=1.0):
        """An upright round thing (a post, a drum, a jug) from y0 up to y1: strips across it running from its
        shaded left to its sunlit right. `tones` = (shade, body, light). `cap` colors its top; `r1` tapers it."""
        r1 = r if r1 is None else r1
        (bx, by), (tx, ty) = self.pt(cx, y0, cz), self.pt(cx, y1, cz)
        kb, kt = self.kat(cx, y0, cz), self.kat(cx, y1, cz)
        D = (self.cam.Z0 + self.world(cx, y0, cz)[2])
        eb = r * kb * max(0.0, self.cam.eye - self.world(cx, y0, cz)[1]) / D      # how far the round foot sags in the picture
        et = r1 * kt * (self.cam.eye - self.world(cx, y1, cz)[1]) / D
        cols = [rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32) for c in tones]
        for i in range(n):
            u0, u1 = -1 + 2 * i / n, -1 + 2 * (i + 1) / n
            um = (u0 + u1) / 2
            v = max(0.0, 1 - ((um - 0.45) / 1.25) ** 2)       # brightest right of the middle, darkest at the left edge
            c = lerp(cols[0], cols[1], min(1.0, v * 1.7)) if v < 0.6 else lerp(cols[1], cols[2], (v - 0.6) / 0.4)
            pts = [(bx + u0 * r * kb, by + math.sqrt(max(0.0, 1 - u0 * u0)) * eb), (bx + u1 * r * kb, by + math.sqrt(max(0.0, 1 - u1 * u1)) * eb),
                   (tx + u1 * r1 * kt, ty + math.sqrt(max(0.0, 1 - u1 * u1)) * et), (tx + u0 * r1 * kt, ty + math.sqrt(max(0.0, 1 - u0 * u0)) * et)]
            self.s.poly(pts, c, alpha)
        if cap is not None:
            self.hdisc(cx, y1, cz, r1, cap, alpha)
        return self


class Shade(Solid):
    """The same drawing, laid flat on the ground along the sun's rays: its coverage is the thing's shadow."""

    shade = True

    def __init__(self, sheet, at, yaw=0.0, unit=1.0, lift=0.0, cam=CAM, sun=SUN):
        super().__init__(sheet, at, yaw, unit, lift, cam)
        self.sun = sun

    def pt(self, x, y, z=0.0):
        X, Y, Z = self.world(x, y, z)
        Y = max(Y, 0.0)
        return self.cam.pt(X + self.sun[0] * Y, 0.0, Z + self.sun[1] * Y)

    def kat(self, x, y, z=0.0):
        X, Y, Z = self.world(x, y, z)
        return self.cam.scale(Z + self.sun[1] * max(Y, 0.0)) * self.unit

    def line(self, points, color, width=1.0, alpha=1.0, z=0.0):
        self.s.line(self.pts(points, z), color, max(0.5, width * self.k * 0.6), alpha)
        return self

    def ball(self, x, y, z, r, color, alpha=1.0, squash=1.0):
        L = math.hypot(*self.sun)
        ux, uz = self.sun[0] / L, self.sun[1] / L
        X, Y, Z = self.world(x, y, z)
        cx, cz = X + self.sun[0] * Y, Z + self.sun[1] * Y
        long_r, wide_r = r * self.unit * math.sqrt(1 + L * L), r * self.unit
        pts = []
        for i in range(20):
            a = math.pi * 2 * i / 20
            pts.append(self.cam.pt(cx + math.cos(a) * long_r * ux - math.sin(a) * wide_r * uz, 0.0, cz + math.cos(a) * long_r * uz + math.sin(a) * wide_r * ux))
        self.s.poly(pts, color, alpha)
        return self

    def tube(self, cx, cz, r, y0, y1, tones, n=8, cap=None, r1=None, alpha=1.0):
        r1 = r if r1 is None else r1
        self.poly([(cx, y0, cz - r), (cx, y0, cz + r), (cx, y1, cz + r1), (cx, y1, cz - r1)], tones[0], alpha)
        self.hdisc(cx, y0, cz, r, tones[0], alpha)
        self.hdisc(cx, y1, cz, r1, tones[0], alpha)
        return self


def shadow_of(shape, draw, at, yaw=0.0, unit=1.0, lift=0.0, soft=1.0):
    """The shadow mask of a thing. `draw(base, lines)` is the function that draws it, given two drafts."""
    sh = Paper(shape)
    d = Shade(sh, at, yaw, unit, lift)
    draw(d, d)
    m = sh.done()[1]
    return blur(m, soft) if soft else m


def stand_up(shape, draw, at, yaw=0.0, unit=1.0, lift=0.0):
    """Draw a thing on two clear sheets: `base` (to be brushed) and `lines` (laid crisply on top).
    -> (color, alpha, line color, line alpha)."""
    base, lines = Paper(shape), Paper(shape)
    draw(Solid(base, at, yaw, unit, lift), Solid(lines, at, yaw, unit, lift))
    c, a = base.done()
    lc, la = lines.done()
    return c, a, lc, la


def brushed(color, alpha, lc, la, under, seed=4, sizes=(7, 4, 2), keep=0.42, density=1.8, fast=False):
    """A cut-out, painted: its flat colors brushed over the color it will stand in front of, its crisp lines
    put back on top. Only the part of the picture it covers is worked on. -> (color, alpha)."""
    shape = alpha.shape
    whole = np.maximum(alpha, la)
    ys, xs = np.where(whole > 0.02)
    if len(ys) == 0:
        return color, whole
    y0, y1, x0, x1 = max(ys.min() - 12, 0), min(ys.max() + 13, shape[0]), max(xs.min() - 12, 0), min(xs.max() + 13, shape[1])
    flat = np.empty((y1 - y0, x1 - x0, 3), dtype=F32)
    flat[...] = rgb(under) if isinstance(under, str) else np.asarray(under, dtype=F32)
    over(flat, color[y0:y1, x0:x1], alpha[y0:y1, x0:x1])
    painted = flat if fast else strokes(flat, sizes=sizes, seed=seed, density=density, jitter=0.03, keep=keep)
    over(painted, lc[y0:y1, x0:x1], la[y0:y1, x0:x1])
    out = np.zeros(shape + (3,), dtype=F32)
    out[y0:y1, x0:x1] = painted
    return out, np.clip(whole, 0, 1)


# ---------------------------------------------------------------- desert things
def crackle(shape, cell, seed):
    """Dried mud: for every pixel of ground, how far (cm) it is from the nearest crack of a crazed pattern
    whose plates are about `cell` cm across."""
    X, Z, below = floor(shape)
    gx, gz = np.floor(X / cell), np.floor(Z / cell)
    d1 = np.full(shape, 1e9, dtype=F32)
    d2 = np.full(shape, 1e9, dtype=F32)
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            cx, cz = gx + i, gz + j
            h1 = np.sin(cx * 127.1 + cz * 311.7 + seed) * 43758.5453
            h2 = np.sin(cx * 269.5 + cz * 183.3 + seed * 1.7) * 24634.6345
            px = (cx + 0.15 + 0.7 * (h1 - np.floor(h1))) * cell
            pz = (cz + 0.15 + 0.7 * (h2 - np.floor(h2))) * cell
            d = np.hypot(X - px, Z - pz).astype(F32)
            d2 = np.where(d < d1, d1, np.minimum(d2, d))
            d1 = np.minimum(d1, d)
    return ((d2 - d1) * 0.5).astype(F32), below


def sagebrush(sheet, x, y, r, seed, tones=("#3d4438", "#66705a", "#98a488", "#cdd2b4"), wood="#4a3a30", light=1, tall=0.85):
    """A sagebrush with the middle of its foot at (x, y), about 2r wide: a low dome of grey-green sprays on
    crooked woody stems. Dark sprays first; the silver ones on the sunny side last."""
    rng = np.random.default_rng(seed)
    for k in range(5):                                                  # the woody stems at the foot
        a = math.radians(rng.uniform(40, 140))
        l = r * rng.uniform(0.35, 0.6)
        sheet.taper([(x + rng.normal(0, r * 0.12), y), (x + math.cos(a) * l * 0.6 + rng.normal(0, 1), y - math.sin(a) * l * 0.6), (x + math.cos(a) * l, y - math.sin(a) * l)],
                    wood, max(1.0, r * 0.07), max(0.7, r * 0.03))
    sprays = []
    n = int(26 + r * 1.6)
    for k in range(n):
        a = math.radians(rng.uniform(8, 172))
        d = rng.random() ** 0.6
        bx, by = x + math.cos(a) * r * d * 0.95, y - math.sin(a) * r * tall * d * 0.95 - r * 0.08
        sunny = 0.5 + 0.5 * (math.cos(a) * light) + 0.35 * math.sin(a) * d
        sprays.append((sunny + rng.normal(0, 0.18), bx, by, a))
    for sunny, bx, by, a in sorted(sprays):
        t = min(1.0, max(0.0, sunny))
        c = mix(tones[0], tones[1], min(1.0, t * 2.2)) if t < 0.45 else (mix(tones[1], tones[2], (t - 0.45) / 0.35) if t < 0.8 else mix(tones[2], tones[3], (t - 0.8) / 0.2))
        for j in range(4):                                              # each spray: a few short leaves fanning up and out
            b = a + rng.normal(0, 0.5)
            l = r * rng.uniform(0.16, 0.30)
            sheet.line([(bx, by), (bx + math.cos(b) * l, by - math.sin(b) * l * 0.9 - l * 0.25)], c, max(0.9, r * 0.055), 0.95)
    return sheet


def tuft(sheet, x, y, r, seed, colors=("#6a6a48", "#a89c64", "#d8c88c")):
    """A tuft of dry grass: a few pale blades."""
    rng = np.random.default_rng(seed)
    for k in range(int(7 + r * 0.5)):
        a = math.radians(rng.uniform(35, 145))
        l = r * rng.uniform(0.5, 1.1)
        sheet.line([(x + rng.normal(0, r * 0.15), y), (x + math.cos(a) * l * 0.5, y - math.sin(a) * l * 0.6), (x + math.cos(a) * l + rng.normal(0, 1), y - math.sin(a) * l)],
                   mix(colors[0], colors[2], rng.random()), max(0.8, r * 0.05), 0.9)
    return sheet


# ---------------------------------------------------------------- ground that has no seams
# (land.texture wraps its noise tile with a plain modulo, which leaves straight seams across a big
# floor: a level line and two diagonals. This does the same job with a mirrored wrap.)
_TILES = {}


def _tile(cell, seed, octaves):
    key = (cell, seed, octaves)
    if key not in _TILES:
        _TILES[key] = noise((1024, 1024), cell, seed, octaves)
    return _TILES[key]


def ground_tex(shape, cell_cm, seed, octaves=4, calm=3.0):
    """Noise that lies on the ground, 0 to 1: blotches about `cell_cm` across wherever they are, so they
    are big near the bottom of the picture and fine and flattened far away, where they calm to 0.5."""
    X, Z, below = floor(shape)
    size = 1024
    scale = cell_cm / 48.0                                  # cm of ground to one pixel of the tile
    tile = _tile(48.0, seed, octaves)

    def fold(t):                                            # mirror at the edges of the tile: no seam
        t = np.mod(t / scale + size * 7.3, 2.0 * (size - 2))
        return np.where(t > size - 2, 2.0 * (size - 2) - t, t)
    t = sample(tile, fold(X), fold(Z * 0.9 + 333.0))
    x, y = grid(shape)
    near = np.clip((y - CAM.vy) / (CAM.full - CAM.vy), 0, 1)
    # far away a blotch is thinner than a pixel is tall: let it fade instead of glittering
    size_px = cell_cm * (near * CAM.s0) * (near * CAM.s0) * CAM.eye / CAM.F      # how tall a blotch is in the picture
    fade = np.clip(size_px / calm, 0, 1)
    return (lerp(np.full(shape, 0.5, dtype=F32), t, fade) * below + 0.5 * (1 - below)).astype(F32)


def desert(shape, seed, far, mid, near, patch=0.08):
    """The desert floor from the horizon (far) to the bottom edge (near), blotched and drifted."""
    x, y = grid(shape)
    t = np.clip((y - CAM.vy) / (shape[0] - CAM.vy), 0, 1)
    color = ramp(t ** 0.72, [(0.0, far), (0.40, mid), (1.0, near)])
    blot = ground_tex(shape, 420.0, seed, 4) - 0.5
    fine = ground_tex(shape, 90.0, seed + 1, 3) - 0.5
    color = color * (1 + blot[..., None] * 2 * patch + fine[..., None] * patch * 0.9)
    k = (noise(shape, (360, 110), seed + 2, 3) - 0.5) * 0.07   # warmer and cooler drifts, as when a wash is not quite mixed
    color[..., 0] += k
    color[..., 2] -= k * 0.8
    return np.clip(color, 0, 1).astype(F32)

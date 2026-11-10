"""PAINT-20A: the kit for Yui on Suruga Bay (edo-village): the camera, the lines of the place, the paints by name, the
graded bands and the keyblock contour of the act's style sheet (S/work-20-paintA/style.md).

World measurements are centimetres: x to the right of the picture's middle, y up, z away from us (z = 0 is the ground at
the row FULL). The camera is the roadside's kind (persp.Camera), so the game's people come out the right size anywhere on
the beach and the street.

THE PLACE. We stand on the beach looking south-west along the shore toward the Satta pass. The street (the Tokaido,
running along behind the beach) and the shore both run away from the lower left to the right, at 40 degrees to the
view (direction (0.85, 1) in x, z): the bay is on the left, and across it, Fuji; the village is on the right. The sun is
in the east, behind us and to the left (SUN): lit faces face us and the left; shadows fall to the right and away.
"""

import math

import numpy as np

from brush import F32, Sheet, curve, grid, lerp, mask_line, mask_poly, noise, over, rgb, tint
from persp import Camera
from postimp_paints import PAINTS

W, H = 800, 600
HZ, FULL = 300, 590
CAM = Camera(HZ, FULL)                                     # eye 317 cm up, Z0 875 cm, focal 800, vanishing x 400
M = 0.6                                                    # the slope of the street and the shore: x = a + M z (vanishing at x 880)
STREET_A, STREET_W = -400.0, 175.0                         # the street's centre line, and half its width
FRONT_A = -50.0                                            # the house fronts: 3.5 m behind the street's centre
SHORE_A = -1700.0                                          # the water's edge: 13 m seaward of the street's centre
RISE = 30.0                                                # the street stands this much above the beach (a sand slope joins them)
SUN = (1.6, 0.5)                                           # a point 1 cm up throws its shadow SUN[0] cm along x and SUN[1] along z
SUN3 = np.array([-0.82, 0.50, -0.26], dtype=F32)           # toward the sun, in 3D (x right, y up, z away): behind us and left, 30 degrees up

# ---------------------------------------------------------------- the paints, by name (style.md section 2)
def P(name):
    return rgb(PAINTS[name]["hex"])


WHITE, NAPLES, CERULEAN, COBALT, ULTRA, PRUSSIAN = P("lead-white"), P("naples-yellow"), P("cerulean"), P("cobalt-blue"), P("ultramarine"), P("prussian-blue")
OCHRE, SIENNA, VERONESE, VIRIDIAN, LAKE, VERMILION = P("yellow-ochre"), P("burnt-sienna"), P("veronese-green"), P("viridian"), P("geranium-lake"), P("vermilion")


def mixp(a, b, t):
    """Two paints (arrays or names) mixed, t of the second."""
    a = P(a) if isinstance(a, str) else a
    b = P(b) if isinstance(b, str) else b
    return lerp(a, b, t)


def tintw(c, t):
    """A paint lightened with lead white (a tint)."""
    return lerp(c, WHITE, t)


def shade(c, t):
    """A paint darkened with prussian blue (never black)."""
    return lerp(c, PRUSSIAN, t)


PAPER = tintw(CERULEAN, 0.88)                              # the sky at the horizon: the paper with a breath of blue
SAND = lerp(tintw(PRUSSIAN, 0.70), OCHRE, 0.06)            # grey sand: white + prussian, a touch of ochre (the key warms it a little more)
SAND_WET = lerp(tintw(PRUSSIAN, 0.55), OCHRE, 0.06)
SAND_SHADE = lerp(SAND, COBALT, 0.40)                      # a cast shadow on the sand: the ground pulled toward cobalt, flat
EARTH = lerp(tintw(OCHRE, 0.45), PRUSSIAN, 0.18)           # the street: packed earth, paler and warmer than the sand
WOOD_LIT, WOOD_SHADE = tintw(OCHRE, 0.25), lerp(SIENNA, PRUSSIAN, 0.25)
SHINGLE_LIT, SHINGLE_SHADE = lerp(tintw(PRUSSIAN, 0.58), OCHRE, 0.22), lerp(tintw(PRUSSIAN, 0.26), COBALT, 0.28)
THATCH_LIT, THATCH_SHADE = tintw(OCHRE, 0.4), lerp(OCHRE, PRUSSIAN, 0.5)
PLASTER_LIT, PLASTER_SHADE = tintw(NAPLES, 0.6), lerp(tintw(COBALT, 0.6), NAPLES, 0.15)
INDIGO = lerp(ULTRA, PRUSSIAN, 0.35)                       # dyed cloth (the noren)
PINK = tintw(LAKE, 0.62)                                   # cherry past its best
PINK_DEEP = tintw(LAKE, 0.42)


# ---------------------------------------------------------------- the camera
def gp(x, z, y=0.0):
    """World -> picture."""
    return CAM.pt(x, y, z)


def kz(z):
    """Picture pixels per centimetre at depth z."""
    return CAM.scale(z)


def street_x(z, across=0.0):
    """The street's centre at depth z; `across` in half widths (+ inland, - seaward)."""
    return STREET_A + M * z + across * STREET_W


def shore_x(z):
    return SHORE_A + M * z


def front_x(z):
    return FRONT_A + M * z


def along(a, z0, z1, n=12, y=0.0, across=0.0):
    """Picture points along a line x = a + M z (+ across) from z0 to z1."""
    return [gp(a + M * z + across, z, y) for z in np.linspace(z0, z1, n)]


def floor(shape):
    return CAM.floor_grid(shape)


def unproject(px, py):
    z = CAM.depth_at(py)
    return CAM.x_at(px, py), z


# ---------------------------------------------------------------- a sheet that takes thin paint (the roadside's Paper)
class Paper(Sheet):
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


# ---------------------------------------------------------------- the style sheet's three things
def bands(shape, rows, colors, soft=5.0, wobble=2.0, seed=0, patch=0.02):
    """A graded wash laid as level bands (the prints' bokashi): `rows` the bottom row of each band (the last may be
    the picture's bottom), `colors` one paint per band, top to bottom. Each boundary is blurred `soft` px and wobbles
    `wobble` px; each band is one flat with a little grain. -> a picture."""
    h, w = shape
    pic = np.zeros((h, w, 3), dtype=F32)
    pic[...] = colors[0]
    top = -20
    for i, (row, c) in enumerate(zip(rows, colors)):
        if i == 0:
            top = row
            continue
        m = mask_poly(shape, [(-10, top), (w + 10, top), (w + 10, h + 10), (-10, h + 10)], soft=soft, wobble=wobble, seed=seed + i)
        field = np.empty_like(pic)
        field[...] = c
        field *= (1 + (noise(shape, (300, 90), seed + 40 + i, 3) - 0.5)[..., None] * 2 * patch)
        over(pic, field, m)
        top = row
    return np.clip(pic, 0, 1)


def flat(color, shape, seed, amount=0.03, cell=90):
    """One flat area with the paper's variation only: +-amount of value, a drift of warm and cool of 0.01."""
    c = np.asarray(color, dtype=F32)
    n = noise(shape, cell, seed, 3) - 0.5
    out = np.clip(c[None, None, :] * (1 + 2 * amount * n[..., None]), 0, 1).astype(F32)
    k = (noise(shape, cell * 2, seed + 7, 2) - 0.5) * 0.02
    out[..., 0] = np.clip(out[..., 0] + k, 0, 1)
    out[..., 2] = np.clip(out[..., 2] - k, 0, 1)
    return out


def contour_w(row):
    """The keyblock's weight at a picture row: 1.0 px at the front, 0.5 far off (style.md section 4)."""
    t = np.clip((row - HZ) / (FULL - HZ), 0, 1)
    return 0.5 + 0.5 * t


def contour(sheet, pts, row=None, alpha=None, color=None, warm=False):
    """The contour line along `pts` (picture points)."""
    r = row if row is not None else max(p[1] for p in pts)
    w = contour_w(r)
    a = alpha if alpha is not None else 0.55 + 0.3 * np.clip((r - HZ) / (FULL - HZ), 0, 1)
    sheet.line(pts, color if color is not None else (SIENNA if warm else PRUSSIAN), w, a)
    return sheet


def shadow_pts(pts3):
    """World points (x, y, z) laid flat along the sun -> picture points of their shadow on the ground."""
    return [gp(x + SUN[0] * max(y, 0.0), z + SUN[1] * max(y, 0.0)) for x, y, z in pts3]


def lit(normal):
    """How much a face with this world normal takes the sun: 0 (shade) to 1."""
    n = np.asarray(normal, dtype=F32)
    n = n / (np.linalg.norm(n) + 1e-6)
    return float(np.clip(np.dot(n, SUN3), 0, 1))


def face_color(base_lit, base_shade, normal):
    """A flat's colour by its facing: the lit flat, the shade flat, nothing between (two flats, a hard edge)."""
    return base_lit if lit(normal) > 0.25 else base_shade


# ================================================================ round twenty-three: depth, and watercolour (DEPTH.md)
# The act's flats laid as washes on paper: every area graded, shadows glazed over the local colour, the key line thinner,
# broken, and lost in the light and the distance. What follows is this scene's own; the library's part is watercolor.py
# (the finish: wash, wash_cut) and depth.py (scatter, air, rim).
from PIL import Image as _Image, ImageDraw as _ImageDraw

import watercolor as WC
from brush import blur, sample, step, warp

WPAPER = WC.PAPER                                          # the bare sheet: snow, plaster in the sun, foam, the lightest road
SHADE = lerp(rgb("#ffffff"), lerp(COBALT, ULTRA, 0.30), 0.56)        # a cast shadow: a thin cool wash to multiply over the local colour
SHADE_WARM = lerp(rgb("#ffffff"), lerp(ULTRA, SIENNA, 0.35), 0.46)   # the same under an overhang, a little warmer (light bounced off the ground)
SHADE_PINES = lerp(rgb("#ffffff"), lerp(COBALT, ULTRA, 0.42), 0.66)  # the deep shade of the pines over the near ground
N_IN, U_ST = (0.857, -0.514), (0.514, 0.857)               # inland (square to the street), and along the street away from us


def thin(c, t):
    """A paint thinned with water: `t` of the paper shows through it (a transparent wash, where tintw is body colour)."""
    c = P(c) if isinstance(c, str) else c
    return lerp(c, WPAPER, t)


def squash(row):
    """How flat a circle lying on the ground looks at a picture row (its height over its width)."""
    return max(float(row) - HZ, 1.0) / CAM.F


def resample(pts, stepsize=3.0):
    """Points every `stepsize` px along a line through `pts`."""
    out = [tuple(map(float, pts[0]))]
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(d / stepsize))
        for i in range(1, n + 1):
            out.append((x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n))
    return out


class Wet:
    """A layer of washes: shapes with hard edges, each a graded wash and not a flat. Colour and cover are float
    pictures; a shape is drawn in its own box at three times the size, so many small ones are cheap. Later shapes lie
    over earlier ones, as paint does. -> done(): (colour, cover), to brush, wash and cut out."""

    def __init__(self, shape=(H, W), ss=3):
        self.shape, self.ss = shape, ss
        self.c = np.zeros(shape + (3,), dtype=F32)
        self.a = np.zeros(shape, dtype=F32)

    def _box(self, xs, ys, pad=2.0):
        h, w = self.shape
        x0, y0 = max(int(math.floor(min(xs) - pad)), 0), max(int(math.floor(min(ys) - pad)), 0)
        x1, y1 = min(int(math.ceil(max(xs) + pad)) + 1, w), min(int(math.ceil(max(ys) + pad)) + 1, h)
        return (x0, y0, x1, y1) if x1 > x0 and y1 > y0 else None

    def _mask(self, box, draw):
        x0, y0, x1, y1 = box
        s = self.ss
        im = _Image.new("L", ((x1 - x0) * s, (y1 - y0) * s), 0)
        draw(_ImageDraw.Draw(im), x0, y0, s)
        return np.asarray(im.resize((x1 - x0, y1 - y0), _Image.BOX), dtype=F32) / 255

    def _colour(self, box, c0, c1, g):
        c0 = np.asarray(c0, dtype=F32)
        if c1 is None:
            return c0[None, None, :]
        x0, y0, x1, y1 = box
        c1 = np.asarray(c1, dtype=F32)
        (ax, ay), (bx, by) = g if g is not None else ((x0, y0), (x0, y1))
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(F32)
        d = max((bx - ax) ** 2 + (by - ay) ** 2, 1e-6)
        t = np.clip(((xx - ax) * (bx - ax) + (yy - ay) * (by - ay)) / d, 0, 1)
        return c0[None, None, :] + (c1 - c0)[None, None, :] * t[..., None]

    def _lay(self, box, m, col):
        x0, y0, x1, y1 = box
        a0 = self.a[y0:y1, x0:x1]
        out = m + a0 * (1 - m)
        c0 = self.c[y0:y1, x0:x1]
        self.c[y0:y1, x0:x1] = (col * m[..., None] + c0 * (a0 * (1 - m))[..., None]) / np.maximum(out, 1e-6)[..., None]
        self.a[y0:y1, x0:x1] = out
        return self

    def poly(self, pts, c0, c1=None, g=None, alpha=1.0):
        """A filled shape: `c0` alone, or a wash graded from `c0` to `c1` along g = (from, to) (picture points; top to
        bottom of the shape if not said)."""
        box = self._box([p[0] for p in pts], [p[1] for p in pts])
        if box is None or len(pts) < 3:
            return self
        m = self._mask(box, lambda d, ox, oy, s: d.polygon([((px - ox) * s, (py - oy) * s) for px, py in pts], fill=255)) * alpha
        return self._lay(box, m, self._colour(box, c0, c1, g))

    def ellipse(self, cx, cy, rx, ry, c0, c1=None, g=None, alpha=1.0):
        box = self._box([cx - rx, cx + rx], [cy - ry, cy + ry])
        if box is None:
            return self
        m = self._mask(box, lambda d, ox, oy, s: d.ellipse([(cx - rx - ox) * s, (cy - ry - oy) * s, (cx + rx - ox) * s, (cy + ry - oy) * s], fill=255)) * alpha
        return self._lay(box, m, self._colour(box, c0, c1, g))

    def line(self, pts, color, width=1.0, alpha=1.0):
        if len(pts) < 2:
            return self
        box = self._box([p[0] for p in pts], [p[1] for p in pts], pad=width / 2 + 2)
        if box is None:
            return self
        s = self.ss
        wd = width * s
        if wd < 1.0:                                           # thinner than the sheet can draw: a hair of less paint
            alpha, wd = alpha * wd, 1.0
        wd = max(1, int(round(wd)))

        def draw(d, ox, oy, s_):
            q = [((px - ox) * s_, (py - oy) * s_) for px, py in pts]
            d.line(q, fill=255, width=wd, joint="curve")
            if wd > 2:
                for px, py in (q[0], q[-1]):
                    d.ellipse([px - wd / 2, py - wd / 2, px + wd / 2, py + wd / 2], fill=255)
        return self._lay(box, self._mask(box, draw) * alpha, np.asarray(color, dtype=F32)[None, None, :])

    def taper(self, pts, c0, w0, w1, c1=None, g=None, alpha=1.0):
        """A stroke that changes width along its length (a trunk, a bough, a blade), as one shape."""
        n = len(pts)
        if n < 2:
            return self
        left, right = [], []
        for i, (px, py) in enumerate(pts):
            ax, ay = pts[max(i - 1, 0)]
            bx, by = pts[min(i + 1, n - 1)]
            dx, dy = bx - ax, by - ay
            d = math.hypot(dx, dy) or 1.0
            hw = (w0 + (w1 - w0) * i / (n - 1)) / 2
            left.append((px - dy / d * hw, py + dx / d * hw))
            right.append((px + dy / d * hw, py - dx / d * hw))
        return self.poly(left + right[::-1], c0, c1, g, alpha)

    def glaze(self, pts, color, amount=1.0):
        """A wash over what is already on the layer inside a shape (multiply): a shadow, a darker passage."""
        box = self._box([p[0] for p in pts], [p[1] for p in pts])
        if box is None:
            return self
        x0, y0, x1, y1 = box
        m = (self._mask(box, lambda d, ox, oy, s: d.polygon([((px - ox) * s, (py - oy) * s) for px, py in pts], fill=255)) * amount)[..., None]
        c = self.c[y0:y1, x0:x1]
        self.c[y0:y1, x0:x1] = c * (1 - m) + c * np.asarray(color, dtype=F32)[None, None, :] * m
        return self

    def clear(self, pts):
        box = self._box([p[0] for p in pts], [p[1] for p in pts])
        if box is None:
            return self
        x0, y0, x1, y1 = box
        m = self._mask(box, lambda d, ox, oy, s: d.polygon([((px - ox) * s, (py - oy) * s) for px, py in pts], fill=255))
        self.a[y0:y1, x0:x1] *= (1 - m)
        return self

    def add(self, color, alpha):
        """Lay a whole painted layer (colour, cover) over this one."""
        return self._lay((0, 0, self.shape[1], self.shape[0]), np.clip(alpha, 0, 1).astype(F32), np.asarray(color, dtype=F32))

    def done(self):
        return self.c.copy(), np.clip(self.a, 0, 1).copy()

    def onto(self, picture, amount=1.0):
        return over(picture, self.c, np.clip(self.a, 0, 1) * amount)


def keyline(layer, pts, row=None, lit=False, seed=0, weight=1.0, color=None, alpha=None):
    """The key line, quieter (DEPTH.md, "Japan in watercolour"): thinner than the print's, a little broken, lost
    altogether on the lit side of a thing (`lit`) and in the distance (above the row HZ + 30: no line at all)."""
    if lit or len(pts) < 2:
        return layer
    r = row if row is not None else max(p[1] for p in pts)
    if r < HZ + 30:
        return layer
    t = float(np.clip((r - HZ) / (FULL - HZ), 0, 1))
    w = (0.35 + 0.45 * t) * weight
    a = alpha if alpha is not None else 0.24 + 0.34 * t
    col = PRUSSIAN if color is None else color
    rng = np.random.default_rng(int(seed * 7919 + pts[0][0] * 13 + pts[0][1] * 31) & 0x7FFFFFFF)
    q = resample(pts, 3.0)
    i = 0
    while i < len(q) - 1:
        n = int(rng.uniform(4, 13))                            # a stroke of the pen, 12 to 40 px
        layer.line(q[i:i + n + 1], col, w * rng.uniform(0.8, 1.15), a * rng.uniform(0.55, 1.0))
        i += n + (int(rng.uniform(1, 3)) if rng.random() < 0.55 else 0)      # and, more often than not, a gap
    return layer


def glaze(picture, mask, color=None, amount=1.0):
    """A shadow as a glaze: the picture multiplied toward a thin cool wash through a mask (never a flat of other colour)."""
    return tint(picture, SHADE if color is None else color, np.clip(mask * amount, 0, 1).astype(F32))


_TILES = {}


def world_noise(X, Z, cell, seed, octaves=3, street=False):
    """Noise that lies on the ground, measured in centimetres: `cell` is the size of its blotches (cm), or (across,
    along) for stretched noise; with `street` the two run across and along the street, so streaks run to its vanishing
    point. X, Z: the ground's place at every pixel (floor(SHAPE)). -> 0 to 1, fading to 0.5 where a blotch would be
    smaller than a pixel (far off it would only glitter)."""
    size = 1024
    tile = _TILES.get((seed, octaves))
    if tile is None:
        tile = _TILES[(seed, octaves)] = noise((size, size), 64, seed, octaves)
    cu, cv = (cell, cell) if np.isscalar(cell) else cell
    if street:
        u, v = X * N_IN[0] + Z * N_IN[1], X * U_ST[0] + Z * U_ST[1]
    else:
        u, v = X, Z

    def fold(t):                                               # the tile mirrored end to end: no seam
        m = np.mod(t, 2 * (size - 2))
        return np.where(m > size - 2, 2 * (size - 2) - m, m)
    n = sample(tile, fold(u / cu * 64 + 300), fold(v / cv * 64 + 300))
    k = CAM.F / (CAM.Z0 + np.maximum(Z, -CAM.Z0 + 50))         # px per cm
    small = np.minimum(cu * k, cv * k * k * CAM.eye / CAM.F)   # the blotch's size in the picture: across, and down (foreshortened)
    fade = np.clip((small - 1.0) / 2.5, 0, 1)
    return (0.5 + (n - 0.5) * fade).astype(F32)


def grade_cut(color, alpha, low=0.90, lightfrom=(-1.0, -0.6), seed=0, uneven=0.05):
    """A cut-out's flats turned into washes: a little deeper toward its foot and away from the light, and never even."""
    ys, xs = np.where(alpha > 0.05)
    if len(ys) == 0:
        return color
    h, w = alpha.shape
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    yy, xx = np.mgrid[0:h, 0:w].astype(F32)
    u, v = (xx - x0) / max(x1 - x0, 1), (yy - y0) / max(y1 - y0, 1)
    lx, ly = lightfrom
    n = math.hypot(lx, ly)
    t = np.clip(0.5 + 0.5 * ((u - 0.5) * lx + (v - 0.5) * ly) / n * 2, 0, 1)      # 1 on the side the light comes from
    mult = low + (1 - low) * t
    mult = mult * (1 + (noise((h, w), 26, seed + 5, 3) - 0.5) * 2 * uneven)
    return np.clip(color * mult[..., None], 0, 1).astype(F32)


def painted(color, alpha, under_c, seed=4, sizes=(5, 3, 2), keep=0.62, fast=False):
    """A cut-out, painted: its washes brushed a little over the colour it stands in front of (so its edge is a hand's)."""
    from brush import strokes
    ys, xs = np.where(alpha > 0.02)
    if len(ys) == 0 or fast:
        return color, np.clip(alpha, 0, 1)
    y0, y1, x0, x1 = max(ys.min() - 12, 0), min(ys.max() + 13, H), max(xs.min() - 12, 0), min(xs.max() + 13, W)
    flat_ = np.empty((y1 - y0, x1 - x0, 3), dtype=F32)
    flat_[...] = np.asarray(under_c, dtype=F32)
    over(flat_, color[y0:y1, x0:x1], alpha[y0:y1, x0:x1])
    out = color.copy()
    out[y0:y1, x0:x1] = strokes(flat_, sizes=sizes, seed=seed, density=1.8, jitter=0.02, keep=keep)
    return out, np.clip(alpha, 0, 1)


def under_of(back, alpha):
    """The colour a cut-out stands in front of (the middle colour of the backdrop under it)."""
    ys, xs = np.where(alpha > 0.5)
    return np.median(back[ys, xs], axis=0) if len(ys) else SAND


def hand(color, alpha, seed, amount=0.7, cell=16):
    """A drawn cut-out's edges made a hand's (DEPTH.md: nothing ruled for long): colour and cover pushed about together
    by under a pixel. Its place and its base line stay."""
    return warp(color, amount, cell, seed + 900), np.clip(warp(alpha, amount, cell, seed + 900), 0, 1)

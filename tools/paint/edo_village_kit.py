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

"""PAINT-21D: the kit for the Akashi shore (edo-akashi): the camera, the lines of the place, the paints by name, the
graded bands and the keyblock contour of the act's style sheet (S/work-20-paintA/style.md).

World measurements are centimetres: x to the right of the picture's middle, y up, z away from us (z = 0 is the ground at
the row FULL). The camera is the village's kind (persp.Camera), so the game's people come out the right size anywhere on
the road, the sand and the shallows.

THE PLACE. We stand on the Saigoku-kaido where it runs behind the shore pines, looking out south-west over the white sand
and the strait to Awaji, long and low (4 km). The water's edge runs from far off at the left (the shore curving away east
to the town and the castle on its hill) to near at the right, where rocks stand at the edge with pools among them. The
sun is in the west, to the right and a little in front of us, about 35 degrees up: faces turned to the right are lit;
shadows fall to the left and a little toward us, flat and blue. (The bearings are the game's composition: the facts give
the strait, Awaji, the castle on its hill and the pines, not a surveyor's view; the notes say so.)
"""

import math

import numpy as np

from brush import F32, Sheet, grid, lerp, mask_line, mask_poly, noise, over, rgb
from persp import Camera
from postimp_paints import PAINTS

W, H = 800, 600
HZ, FULL = 262, 590
CAM = Camera(HZ, FULL)                                     # eye 359 cm up, Z0 875 cm, focal 800, vanishing x 400
SUN = (-1.05, -0.22)                                       # a point 1 cm up throws its shadow SUN[0] cm along x, SUN[1] along z
SUN3 = np.array([0.80, 0.55, 0.24], dtype=F32)             # toward the sun (x right, y up, z away): to the right, a little ahead


def P(name):
    return rgb(PAINTS[name]["hex"])


WHITE, NAPLES, CERULEAN, COBALT, ULTRA, PRUSSIAN = P("lead-white"), P("naples-yellow"), P("cerulean"), P("cobalt-blue"), P("ultramarine"), P("prussian-blue")
OCHRE, SIENNA, VERONESE, VIRIDIAN, LAKE, VERMILION = P("yellow-ochre"), P("burnt-sienna"), P("veronese-green"), P("viridian"), P("geranium-lake"), P("vermilion")


def mixp(a, b, t):
    a = P(a) if isinstance(a, str) else a
    b = P(b) if isinstance(b, str) else b
    return lerp(a, b, t)


def tintw(c, t):
    return lerp(c, WHITE, t)


def shade(c, t):
    return lerp(c, PRUSSIAN, t)


PAPER = tintw(CERULEAN, 0.86)                              # the sky at the horizon: the paper with a breath of blue
SAND = lerp(tintw(NAPLES, 0.62), OCHRE, 0.05)              # white sand in the sun: near the paper, warm
SAND_FAR = lerp(SAND, PAPER, 0.35)
SAND_WET = lerp(tintw(PRUSSIAN, 0.62), NAPLES, 0.18)       # the wet sand at the water's edge: a grey-blue
SAND_SHADE = lerp(SAND, COBALT, 0.36)                      # a cast shadow on the sand: flat, toward cobalt
EARTH = lerp(lerp(tintw(OCHRE, 0.42), SIENNA, 0.10), PRUSSIAN, 0.10)    # the road: packed earth
EARTH_SHADE = lerp(EARTH, COBALT, 0.38)
PINE = lerp(VIRIDIAN, PRUSSIAN, 0.22)                      # the pines: deep viridian toward prussian
PINE_LIT = lerp(VIRIDIAN, VERONESE, 0.22)
PINE_DEEP = lerp(VIRIDIAN, PRUSSIAN, 0.55)
BARK, BARK_SHADE = lerp(SIENNA, OCHRE, 0.22), lerp(SIENNA, PRUSSIAN, 0.42)
CLAY, CLAY_SHADE = lerp(lerp(SIENNA, OCHRE, 0.55), WHITE, 0.12), lerp(lerp(SIENNA, OCHRE, 0.3), PRUSSIAN, 0.22)    # the octopus pots: fired clay
WOOD_LIT, WOOD_SHADE = tintw(OCHRE, 0.20), lerp(SIENNA, PRUSSIAN, 0.28)
STONE, STONE_SHADE = lerp(tintw(PRUSSIAN, 0.55), OCHRE, 0.10), lerp(tintw(PRUSSIAN, 0.22), COBALT, 0.20)
PLASTER = WHITE                                            # the castle's plaster: white
ROOF = lerp(tintw(PRUSSIAN, 0.45), COBALT, 0.15)           # its roofs: blue-grey
INDIGO = lerp(ULTRA, PRUSSIAN, 0.35)
AWAJI = lerp(lerp(CERULEAN, VERONESE, 0.30), PAPER, 0.38)  # Awaji: a cool blue-green mass, far
AWAJI_SHADE = lerp(lerp(COBALT, VIRIDIAN, 0.30), PAPER, 0.42)


# ---------------------------------------------------------------- the camera
def gp(x, z, y=0.0):
    return CAM.pt(x, y, z)


def kz(z):
    return CAM.scale(z)


def row_z(row):
    return CAM.depth_at(row)


# ---------------------------------------------------------------- the water's edge (a smooth curve, far left to near right)
EDGE = [(-60000.0, 150000.0), (-9000.0, 22000.0), (-2600.0, 6000.0), (-1300.0, 2700.0), (-700.0, 1500.0), (-280.0, 1000.0),
        (60.0, 760.0), (330.0, 560.0), (560.0, 420.0), (760.0, 340.0), (1100.0, 250.0)]


def edge_z(x):
    """The water's edge's z at a given x (the curve is single-valued in x)."""
    xs = [p[0] for p in EDGE]
    zs = [p[1] for p in EDGE]
    return float(np.interp(x, xs, zs))


def edge_pts(n=60, offset=0.0):
    """Picture points along the water's edge (offset: cm landward, + toward us)."""
    out = []
    for (x0, z0), (x1, z1) in zip(EDGE[:-1], EDGE[1:]):
        for t in np.linspace(0, 1, max(3, n // len(EDGE)), endpoint=False):
            x, z = x0 + (x1 - x0) * t, z0 + (z1 - z0) * t
            out.append(gp(x, max(z - offset, -50.0)))
    out.append(gp(EDGE[-1][0], EDGE[-1][1] - offset))
    return out


# ---------------------------------------------------------------- a sheet that takes thin paint (the village's Paper)
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
    """A graded wash laid as level bands (the prints' bokashi): `rows` the top row of each band, `colors` one paint per
    band, top to bottom; each boundary blurred `soft` px and wobbling `wobble` px; each band a flat with a little grain."""
    h, w = shape
    pic = np.zeros((h, w, 3), dtype=F32)
    pic[...] = colors[0]
    for i, (row, c) in enumerate(zip(rows, colors)):
        if i == 0:
            continue
        m = mask_poly(shape, [(-10, row), (w + 10, row), (w + 10, h + 10), (-10, h + 10)], soft=soft, wobble=wobble, seed=seed + i)
        field = np.empty_like(pic)
        field[...] = c
        field *= (1 + (noise(shape, (300, 90), seed + 40 + i, 3) - 0.5)[..., None] * 2 * patch)
        over(pic, field, m)
    return np.clip(pic, 0, 1)


def flat(color, shape, seed, amount=0.03, cell=90):
    c = np.asarray(color, dtype=F32)
    n = noise(shape, cell, seed, 3) - 0.5
    out = np.clip(c[None, None, :] * (1 + 2 * amount * n[..., None]), 0, 1).astype(F32)
    k = (noise(shape, cell * 2, seed + 7, 2) - 0.5) * 0.02
    out[..., 0] = np.clip(out[..., 0] + k, 0, 1)
    out[..., 2] = np.clip(out[..., 2] - k, 0, 1)
    return out


def contour_w(row):
    t = np.clip((row - HZ) / (FULL - HZ), 0, 1)
    return 0.5 + 0.5 * t


def contour(sheet, pts, row=None, alpha=None, color=None, warm=False):
    r = row if row is not None else max(p[1] for p in pts)
    w = contour_w(r)
    a = alpha if alpha is not None else 0.55 + 0.3 * np.clip((r - HZ) / (FULL - HZ), 0, 1)
    sheet.line(pts, color if color is not None else (SIENNA if warm else PRUSSIAN), w, a)
    return sheet


def shadow_pts(pts3):
    """World points (x, y, z) laid flat along the sun -> picture points of their shadow on the ground."""
    return [gp(x + SUN[0] * max(y, 0.0), z + SUN[1] * max(y, 0.0)) for x, y, z in pts3]


def lit(normal):
    n = np.asarray(normal, dtype=F32)
    n = n / (np.linalg.norm(n) + 1e-6)
    return float(np.clip(np.dot(n, SUN3), 0, 1))

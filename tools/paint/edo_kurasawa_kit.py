"""PAINT-21A: the kit for the Satta Pass (round twenty-one): Nishikurasawa at its foot (edo_kurasawa.py) and the top of
the pass (edo_satta.py). What the two pictures share: the act's paints by name and its three print things (graded bands,
flats, the keyblock contour: S/work-20-paintA/style.md), taken from Yui's kit (edo_village_kit.py) so that the three
places of the first leg are mixed alike; a camera per scene; ONE Fuji and ONE cap of cloud, drawn by the same code at each
scene's size, so the mountain and its cloud are the same mountain and the same cloud in both pictures (and the village's
cone, by its shape); the pass's pines, grass and far shore.

World measurements are centimetres, as the act's: x to the right of the picture's middle, y up from the road, z away from
us (z = 0 is the ground at the row FULL). The sun is the act's (as at Yui): in the east, behind us and to the left, about
30 degrees up; faces turned to us and to the left are lit, shadows fall to the right and away, flat and blue.
"""

import math

import numpy as np

from brush import F32, Sheet, blur, curve, grid, lerp, mask_line, mask_poly, noise, over, rgb, smooth, step, warp
from persp import Camera
from edo_village_kit import (P, mixp, tintw, shade, Paper, bands, flat, WHITE, NAPLES, CERULEAN, COBALT, ULTRA, PRUSSIAN, OCHRE,
                             SIENNA, VERONESE, VIRIDIAN, LAKE, VERMILION)

W, H = 800, 600
SUN = (1.6, 0.5)                                           # a point 1 cm up throws its shadow SUN[0] cm along x and SUN[1] along z
SUN3 = np.array([-0.82, 0.50, -0.26], dtype=F32)           # toward the sun (x right, y up, z away): behind us and left, 30 degrees up

# ---------------------------------------------------------------- the paints of the pass (style.md section 2)
PAPER = tintw(CERULEAN, 0.88)                              # the sky at the horizon: the paper with a breath of blue (Yui's)
EARTH = lerp(tintw(OCHRE, 0.45), PRUSSIAN, 0.18)           # the Tokaido: packed earth (Yui's street)
EARTH_SHADE = lerp(EARTH, COBALT, 0.40)                    # a cast shadow on the road: the ground pulled toward cobalt, flat
EARTH_RUT = lerp(EARTH, PRUSSIAN, 0.16)
GRASS_LIT, GRASS = lerp(VERONESE, NAPLES, 0.12), mixp(VERONESE, VIRIDIAN, 0.38)
GRASS_SHADE = lerp(VIRIDIAN, PRUSSIAN, 0.22)
PINE, PINE_SHADE, PINE_LIT = lerp(VIRIDIAN, PRUSSIAN, 0.30), lerp(VIRIDIAN, PRUSSIAN, 0.55), mixp(VIRIDIAN, VERONESE, 0.35)
BARK, BARK_SHADE = lerp(SIENNA, PRUSSIAN, 0.30), lerp(SIENNA, PRUSSIAN, 0.58)
WOOD_LIT, WOOD_SHADE = tintw(OCHRE, 0.25), lerp(SIENNA, PRUSSIAN, 0.25)
WOOD_DARK = lerp(SIENNA, PRUSSIAN, 0.55)
THATCH_LIT, THATCH_SHADE = tintw(OCHRE, 0.40), lerp(OCHRE, PRUSSIAN, 0.50)
PLASTER_LIT, PLASTER_SHADE = tintw(NAPLES, 0.60), lerp(tintw(COBALT, 0.60), NAPLES, 0.15)
STONE_LIT, STONE, STONE_SHADE = tintw(PRUSSIAN, 0.70), tintw(PRUSSIAN, 0.52), lerp(tintw(PRUSSIAN, 0.32), COBALT, 0.25)
INDIGO = lerp(ULTRA, PRUSSIAN, 0.35)                       # dyed cloth
TATAMI = lerp(tintw(VERONESE, 0.45), NAPLES, 0.45)         # the mats: straw, a little green
RED_BIB = lerp(VERMILION, LAKE, 0.25)                      # the Jizo's bib: the picture's red touch


class View:
    """A scene's camera (the roadside's kind, persp.Camera) with the contour's weights tied to its own rows, and the
    scene's sun for cast shadows (`sun`: a point 1 cm up throws its shadow sun[0] cm along x and sun[1] cm along z)."""

    def __init__(self, hz, full, vanish_x=400.0, sun=SUN):
        self.HZ, self.FULL = hz, full
        self.cam = Camera(hz, full, vanish_x=vanish_x)
        self.sun = sun

    def gp(self, x, z, y=0.0):
        """World -> picture."""
        return self.cam.pt(x, y, z)

    def kz(self, z):
        """Picture pixels per centimetre at depth z."""
        return self.cam.scale(z)

    def depth_at(self, row):
        return self.cam.depth_at(row)

    def x_at(self, col, row):
        return self.cam.x_at(col, row)

    def row(self, z, y=0.0):
        return self.gp(0.0, z, y)[1]

    def contour_w(self, row):
        """The keyblock's weight at a picture row: 1.0 px at the front, 0.5 far off (style.md section 4)."""
        t = float(np.clip((row - self.HZ) / (self.FULL - self.HZ), 0, 1))
        return 0.5 + 0.5 * t

    def contour(self, sheet, pts, row=None, alpha=None, color=None, warm=False):
        r = row if row is not None else max(p[1] for p in pts)
        a = alpha if alpha is not None else 0.55 + 0.3 * float(np.clip((r - self.HZ) / (self.FULL - self.HZ), 0, 1))
        sheet.line(pts, color if color is not None else (SIENNA if warm else PRUSSIAN), self.contour_w(r), a)
        return sheet

    def shadow_pts(self, pts3):
        """World points (x, y, z) laid flat along the sun -> picture points of their shadow on the ground (y = 0)."""
        return [self.gp(x + self.sun[0] * max(y, 0.0), z + self.sun[1] * max(y, 0.0)) for x, y, z in pts3]


def shade_ground(pic, mask, amount=0.42, dark=0.93):
    """A cast shadow: the ground's own colour under it pulled toward cobalt and a little darker, hard-edged and flat
    (style.md section 8): grass in shadow stays grass, earth stays earth."""
    shaded = lerp(pic, COBALT, amount) * dark
    over(pic, shaded, mask)
    return pic


def lit(normal):
    n = np.asarray(normal, dtype=F32)
    n = n / (np.linalg.norm(n) + 1e-6)
    return float(np.clip(np.dot(n, SUN3), 0, 1))


# ---------------------------------------------------------------- Fuji: one mountain for the two pictures
class Fuji:
    """Mount Fuji across the head of Suruga Bay, as the act draws it (Yui's cone: concave flanks, a small flat top with
    the crater's notch toward the right, snow well down the flanks in fingers down the gullies, the lit flank on the left
    and the shade flank on the right, the foot lost in the haze at the far shore). `summit` is the picture point of the
    top's middle, `foot` the row it stands on (the far shore), `half` the half width at the foot, `snow` how far down
    the snow comes (0 summit, 1 foot). Everything scales with the height, so the pass's bigger mountain is the same one."""

    def __init__(self, summit, foot, half, snow=0.40, seed=0):
        self.sx, self.sy = float(summit[0]), float(summit[1])
        self.foot, self.half, self.snow, self.seed = float(foot), float(half), snow, seed
        self.h = self.foot - self.sy                         # its height in the picture
        self.k = self.h / 220.0                              # 1 at Yui's size (summit row 80 over the horizon 300)

    def mask(self, shape):
        x, y = grid(shape)
        t = np.clip((y - self.sy) / (self.foot + 4 - self.sy), 0, 1)
        half = 12 * self.k + (self.half - 12 * self.k) * t ** 1.7
        cap = np.clip((y - self.sy) / (9.0 * self.k), 0, 1)
        half = half * (0.55 + 0.45 * cap)
        m = (np.abs(x - self.sx - 6 * self.k * (1 - cap)) < half) & (y >= self.sy) & (y < self.foot + 4)
        m = warp(m.astype(F32), 1.4 * max(1.0, self.k * 0.8), 40, self.seed + 7)
        return np.clip(m, 0, 1)

    def snow_edge(self, shape):
        """The row of the snow's lower edge at every column (fingers down the gullies)."""
        x, y = grid(shape)
        gul = noise(shape, (26 * self.k, 90 * self.k), self.seed + 3, 3)
        base = self.sy + self.snow * self.h
        return base + (gul - 0.5) * 40 * self.k + np.clip(np.abs(x - self.sx) / (110.0 * self.k), 0, 1) ** 2 * 30 * self.k

    def paint(self, pic, horizon_paper, seed=None):
        """Lay the mountain on `pic`: the body (lit and shade flanks, the foot in haze) and the snow. -> (mask, snow mask)."""
        shape = pic.shape[:2]
        x, y = grid(shape)
        m = self.mask(shape)
        flank_lit, flank_shade = tintw(COBALT, 0.46), tintw(mixp(COBALT, ULTRA, 0.35), 0.30)
        ridge_x = self.sx + 10 * self.k + 0.08 * (y - self.sy)
        flank = np.where((x < ridge_x)[..., None], flank_lit, flank_shade).astype(F32)
        haze_t = np.clip((y - (self.foot - 68 * self.k)) / (70.0 * self.k), 0, 1) ** 1.4
        body = lerp(flank, horizon_paper, haze_t[..., None] * 0.80)
        over(pic, body, m)
        edge = self.snow_edge(shape)
        snow = step(edge + 3, edge - 3, y) * m
        snow_c = np.where((x < self.sx + 4 * self.k)[..., None], WHITE, tintw(CERULEAN, 0.74)).astype(F32)
        over(pic, snow_c, snow)
        return m, snow

    def contour(self, pic, m, amount=0.3):
        """The shoulders against the sky: a breath of contour (0.5 px, alpha 0.4)."""
        x, y = grid(pic.shape[:2])
        edge = np.clip(m - np.roll(m, 2, axis=0), 0, 1) * (y < self.foot - 10)
        over(pic, PRUSSIAN, (blur(edge, 0.6) * amount).astype(F32))

    def box(self, pad=6):
        """Its picture box (x, y, w, h) down to the foot."""
        return [int(self.sx - self.half - pad), int(self.sy - pad), int(2 * self.half + 2 * pad), int(self.foot - self.sy + pad)]


def cloud_cap(sheet, lines, fuji, shift=(0.0, 0.0)):
    """The cap of cloud on Fuji's top (the same cloud in both pictures, at each mountain's size): a flat lens of lead white
    hugging the summit, wider than the top, with a smaller lens riding over it, each with a 1 px prussian edge on its top
    only (style.md section 3); the underside a shade flat of cerulean. It hides the summit and the upper snow: the
    backdrop under it is the clear mountain. -> the cap's outline points (for layout)."""
    k = fuji.k
    cx, cy = fuji.sx + shift[0] * k, fuji.sy + 16 * k + shift[1] * k
    outline = []

    def lens(cx_, cy_, rx, top, bottom, lean=0.0, n=40):
        pts_top, pts_bot = [], []
        for i in range(n + 1):
            u = i / n
            xx = cx_ - rx + 2 * rx * u
            s = math.sin(math.pi * u)
            pts_top.append((xx, cy_ - top * s ** 0.75 - lean * (u - 0.5) * top))
            pts_bot.append((xx, cy_ + bottom * s ** 1.6))
        return pts_top, pts_bot

    under_c = tintw(mixp(CERULEAN, COBALT, 0.3), 0.55)
    body_c = tintw(CERULEAN, 0.88)
    # the main lens: wide and flat, sitting over the top
    t1, b1 = lens(cx, cy, 78 * k, 24 * k, 10 * k, lean=0.10)
    sheet.poly(t1 + list(reversed(b1)), body_c)
    # its underside: a shade flat along the bottom third (the cloud's own shadow side)
    t1s = [(px, py + (b[1] - py) * 0.58) for (px, py), b in zip(t1, b1)]
    sheet.poly(t1s + list(reversed(b1)), under_c)
    # the rider: a smaller lens above it, a little to the right, as the wind takes the top
    t2, b2 = lens(cx + 14 * k, cy - 22 * k, 50 * k, 13 * k, 5 * k, lean=0.15)
    sheet.poly(t2 + list(reversed(b2)), WHITE)
    # a thin streamer drawn off to the right (the wind from the left)
    t3, b3 = lens(cx + 76 * k, cy - 4 * k, 34 * k, 4 * k, 2.5 * k)
    sheet.poly(t3 + list(reversed(b3)), tintw(CERULEAN, 0.82))
    for top in (t1, t2, t3):
        lines.line(top, PRUSSIAN, 1.0 if k > 1.2 else 0.8, 0.55)
    outline = t1 + list(reversed(b1))
    return [(float(a), float(b)) for a, b in outline + t2]


# ---------------------------------------------------------------- the pass's pines and grass
def pine_pads(sheet, lines, trunk, pads, seed, scale=1.0, lit_side=-1, contour=True, alpha_line=0.6, w_line=0.8, trunk_w=None):
    """A pine in the prints' manner: a trunk (a list of picture points, foot first) of tapering width, and its foliage
    as flat layered pads (each (cx, cy, rx, ry)): a dark pad, its lit top a lighter flat, a fine contour along the top.
    `lit_side` -1: the sun from the left."""
    rng = np.random.default_rng(seed)
    n = len(trunk)
    w0 = 7.0 * scale if trunk_w is None else trunk_w
    for i in range(n - 1):
        w = w0 * (1 - 0.75 * i / max(1, n - 1))
        sheet.line([trunk[i], trunk[i + 1]], BARK_SHADE, max(1.0, w), 1.0)
        # the lit side of the trunk: a thinner warm line on the left
        a, b = trunk[i], trunk[i + 1]
        sheet.line([(a[0] + lit_side * w * 0.22, a[1]), (b[0] + lit_side * w * 0.22, b[1])], BARK, max(0.8, w * 0.45), 1.0)
    for (cx, cy, rx, ry) in pads:
        rx, ry = rx * scale, ry * scale
        # the pad: a flat, cloud-edged lens, flatter underneath
        m = 22
        top, bot = [], []
        for j in range(m + 1):
            u = j / m
            xx = cx - rx + 2 * rx * u
            s = math.sin(math.pi * u)
            wob = 1 + 0.10 * math.sin(u * 17 + seed) + 0.06 * rng.normal()
            top.append((xx, cy - ry * s ** 0.6 * wob))
            bot.append((xx, cy + ry * 0.35 * s ** 1.5))
        sheet.poly(top + list(reversed(bot)), PINE_SHADE)
        # the lit top: the upper part of the pad, toward the sun
        lt = [(px + lit_side * rx * 0.06, py + (b[1] - py) * 0.12) for (px, py), b in zip(top, bot)]
        mid = [(px + lit_side * rx * 0.06, py + (b[1] - py) * 0.55) for (px, py), b in zip(top, bot)]
        sheet.poly(lt + list(reversed(mid)), PINE)
        hl = [(px + lit_side * rx * 0.12, py + (b[1] - py) * 0.10) for (px, py), b in zip(top[:m // 2 + 3], bot[:m // 2 + 3])]
        hm = [(px + lit_side * rx * 0.12, py + (b[1] - py) * 0.32) for (px, py), b in zip(top[:m // 2 + 3], bot[:m // 2 + 3])]
        sheet.poly(hl + list(reversed(hm)), PINE_LIT)
        # needles: a comb of short strokes along the pad's lower edge
        for j in range(int(rx / (2.2 * max(scale, 0.5))) + 2):
            u = (j + 0.5) / (int(rx / (2.2 * max(scale, 0.5))) + 2)
            px = cx - rx * 0.92 + 2 * rx * 0.92 * u
            py = cy + ry * 0.33 * math.sin(math.pi * u) ** 1.5
            lines.line([(px, py - 1.5 * scale), (px + 0.6 * scale, py + 1.8 * scale)], PINE_SHADE, max(0.6, 0.8 * scale), 0.7)
        if contour:
            lines.line(top, PRUSSIAN, w_line, alpha_line)


def tuft(sheet, x, y, h, seed, lean=0.0, colors=(GRASS_SHADE, GRASS, GRASS_LIT), n=7, width=1.0):
    """A tuft of grass: blades from a foot, leaning with the wind (lean > 0: to the right)."""
    rng = np.random.default_rng(seed)
    for i in range(n):
        a = (rng.random() - 0.5) * 1.0 + lean
        hh = h * (0.55 + 0.45 * rng.random())
        bx = x + (rng.random() - 0.5) * h * 0.5
        tip = (bx + math.sin(a) * hh, y - math.cos(a) * hh)
        mid = (bx + math.sin(a) * hh * 0.45 + lean * hh * 0.08, y - math.cos(a) * hh * 0.55)
        c = colors[min(len(colors) - 1, int(rng.random() * len(colors)))]
        sheet.line([(bx, y), mid, tip], c, max(0.6, width * (0.7 + 0.6 * rng.random())), 1.0)


def far_roofs(sheet, x0, x1, row, n, seed, h=4.0, colors=None, line=None):
    """A row of far village roofs (beyond a kilometre: no contour, two flats each), along a shore."""
    rng = np.random.default_rng(seed)
    cols = colors or (tintw(PRUSSIAN, 0.55), tintw(mixp(PRUSSIAN, OCHRE, 0.3), 0.55))
    for i in range(n):
        cx = x0 + (x1 - x0) * (i + 0.5 + rng.normal(0, 0.18)) / n
        w = h * (1.6 + rng.random() * 1.4)
        hh = h * (0.7 + rng.random() * 0.5)
        r = row + rng.normal(0, 0.6)
        sheet.poly([(cx - w, r), (cx + w, r), (cx + w * 0.55, r - hh), (cx - w * 0.55, r - hh)], cols[i % len(cols)])
        sheet.poly([(cx - w, r), (cx + w, r), (cx + w, r + hh * 0.7), (cx - w, r + hh * 0.7)], tintw(NAPLES, 0.55))


def sail_boat(sheet, x, y, s, seed, sail=True):
    """A small fishing boat far out on the bay: a dark hull, a square sail of pale cloth (or none)."""
    rng = np.random.default_rng(seed)
    hull = lerp(SIENNA, PRUSSIAN, 0.55)
    sheet.poly([(x - 6 * s, y), (x + 6 * s, y), (x + 7.5 * s, y - 2 * s), (x - 5 * s, y - 1.6 * s)], hull)
    if sail:
        mx = x + rng.uniform(-1.0, 1.0) * s
        sheet.line([(mx, y - 1.5 * s), (mx, y - 13 * s)], hull, max(0.6, 0.7 * s), 1.0)
        sheet.poly([(mx - 4.5 * s, y - 12.5 * s), (mx + 4.0 * s, y - 12.5 * s), (mx + 4.6 * s, y - 3.5 * s), (mx - 3.8 * s, y - 3.2 * s)],
                   tintw(NAPLES, 0.72))
        sheet.line([(mx - 4.5 * s, y - 12.5 * s), (mx + 4.0 * s, y - 12.5 * s)], hull, max(0.5, 0.6 * s), 1.0)


def brushed(color, alpha, lc, la, under, shape=(H, W), seed=4, sizes=(6, 3, 2), keep=0.45, fast=False):
    """A cut-out, painted: flats brushed over the colour it stands in front of, its lines put back on top (Yui's way)."""
    from brush import strokes
    whole = np.maximum(alpha, la)
    ys, xs = np.where(whole > 0.02)
    if len(ys) == 0:
        return color, whole
    h, w = shape
    y0, y1, x0, x1 = max(ys.min() - 12, 0), min(ys.max() + 13, h), max(xs.min() - 12, 0), min(xs.max() + 13, w)
    flat_ = np.empty((y1 - y0, x1 - x0, 3), dtype=F32)
    flat_[...] = np.asarray(under, dtype=F32)
    over(flat_, color[y0:y1, x0:x1], alpha[y0:y1, x0:x1])
    painted = flat_ if fast else strokes(flat_, sizes=sizes, seed=seed, density=1.8, jitter=0.025, keep=keep)
    over(painted, lc[y0:y1, x0:x1], la[y0:y1, x0:x1])
    out = np.zeros(shape + (3,), dtype=F32)
    out[y0:y1, x0:x1] = painted
    return out, np.clip(whole, 0, 1)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02):
    """Grain and the palette (Yui's finish): an 8-bit PNG; with `alpha`, a hard-edged cut-out."""
    import os
    from brush import grain, palette_of, to_palette, save
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)

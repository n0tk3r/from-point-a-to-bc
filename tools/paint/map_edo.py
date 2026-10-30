"""The map of Japan for the map screen (Act Six, round twenty): an Edo travel map. PAINT-20B.

    python3 map_edo.py            paints out/map-edo/ (back.png, place-*.png, path-*.png) and writes its layout.json
    python3 map_edo.py fast       the same without the brush pass
    python3 install.py map-edo    copies it into art/maps/edo/ (as painted, never keyed)

THE SHEET. A travel map printed from woodblocks on a long sheet of soft paper, folded in six panels and worn at the
folds: the coast from Suruga Bay in the EAST (at the right) to Harima in the WEST (at the left), the sea below in rows
of Prussian-blue waves, the land above in soft green with its mountains as cones, Fuji white at the right end, the coast
road dotted along the shore, the places as small pictures with their names (the engine writes the names in Koine Road,
prussian blue on a paper halo). East is at the right, as the design asked.

WHAT IS WHERE (js/content/maps.js, `edo`): yui (a fishing village under a headland on Suruga Bay, Fuji behind it);
osaka (a landmark, no scene: a city at a river mouth); hills (a hollow in wooded hills north of Osaka: the cedars and
the storehouse); himeji (a castle on a hill above a town, the Inland Sea below). Ways: sea (yui to osaka, over the
water round the Kii peninsula: a dotted ship's course), road1 (osaka up into the hills), road2 (the hills down to the
coast road and west to Himeji). Every colour is mixed from the paint box by name (map_edo.py mixes with brush.rgb and
lerp); the map is the interface's and is never keyed."""

import json
import math
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, rgb, lerp, noise, blur, strokes, grain, palette_of, to_palette, save, Sheet, over, mask_poly
from postimp_paints import PAINTS

W, H = 800, 600
OUT = "out/map-edo"
FAST = "fast" in sys.argv
SEED = 1830


def paint(name):
    return rgb(PAINTS[name]["hex"])


def mixp(a, b, t):
    return lerp(paint(a) if isinstance(a, str) else a, paint(b) if isinstance(b, str) else b, t)


def hexof(c):
    return "#" + "".join(f"{int(round(float(v) * 255)):02x}" for v in c)


# ---- the paints of the sheet
PAPER = mixp(mixp("lead-white", "naples-yellow", 0.30), "yellow-ochre", 0.08)
PAPER_WORN = mixp(PAPER, "burnt-sienna", 0.12)
PRUSSIAN = paint("prussian-blue")
COBALT = paint("cobalt-blue")
CERULEAN = paint("cerulean")
SEA_WAVE = mixp("prussian-blue", "cobalt-blue", 0.35)
LAND = mixp(mixp("veronese-green", "lead-white", 0.55), "naples-yellow", 0.15)
LAND_DK = mixp("veronese-green", "viridian", 0.35)
HILL = mixp(mixp("cerulean", "veronese-green", 0.45), "lead-white", 0.35)
HILL_SHADE = mixp("cobalt-blue", "viridian", 0.4)
SNOW = paint("lead-white")
ROAD = mixp("burnt-sienna", "yellow-ochre", 0.5)
ROOF = mixp("prussian-blue", "cobalt-blue", 0.5)
WALL = mixp("lead-white", "naples-yellow", 0.2)
WOOD = paint("yellow-ochre")
CEDAR = paint("viridian")
RED = paint("vermilion")
LABEL = {"color": hexof(mixp("prussian-blue", "ultramarine", 0.25)), "halo": hexof(PAPER), "upper": False, "spacing": 0.04, "size": 15}

SHEET = [44, 170, 756, 540]                # the paper's box
PANELS = 6
# the coast, west (left) to east (right): land above it, sea below; the Kii peninsula bulges down in the middle, Osaka's
# bay is the notch west of it, Suruga Bay the one at the right under Fuji
COAST = [(44, 418), (90, 404), (150, 408), (200, 416), (240, 428), (280, 446), (312, 432), (336, 426), (356, 438), (384, 452),
         (420, 482), (456, 504), (486, 500), (516, 468), (540, 428), (556, 392), (586, 404), (612, 384), (640, 366), (664, 380),
         (700, 350), (734, 326), (756, 318)]
HEADLAND = [(588, 396), (598, 372), (612, 362), (624, 378), (614, 392)]          # the Satta pass's headland, west of Yui
FUJI = (700.0, 232.0, 150.0, 64.0)                                                 # x of the peak, y of the peak, half the base, the height
RIVER = [(306, 284), (318, 320), (326, 360), (332, 392), (336, 426)]               # the river from the hills down to Osaka's mouth
MOUNTAINS = [(100, 300, 26), (150, 262, 22), (210, 290, 30), (250, 240, 20), (340, 232, 26), (390, 300, 32), (430, 262, 24), (470, 320, 28),
             (520, 240, 22), (560, 300, 30), (596, 250, 24), (640, 290, 20), (180, 350, 16), (440, 400, 18), (470, 430, 14), (700, 300, 14), (740, 270, 18)]
HILLS_C = (300, 262)                       # the hollow in the wooded hills north of Osaka
PLACES = {                                 # id: (the drawing's middle, the pin, the name's baseline middle, the name)
    "yui": ((632, 350), (640, 312), (632, 392), "Yui"),
    "osaka": ((335, 408), (300, 448), (300, 388), "Osaka"),
    "hills": ((300, 262), (300, 308), (300, 222), "The hills"),
    "himeji": ((130, 346), (130, 296), (130, 396), "Himeji"),
}
WAYS = {
    ("yui", "osaka"): [(596, 402), (590, 440), (574, 484), (530, 516), (482, 532), (436, 518), (398, 492), (366, 466), (350, 442)],
    ("osaka", "hills"): [(352, 392), (344, 356), (326, 318), (310, 290), (306, 284)],
    ("hills", "himeji"): [(272, 268), (236, 300), (204, 338), (176, 356), (156, 360)],
}


# ---------------------------------------------------------------- drawing helpers
class Pen:
    """Fills and lines on one clear sheet, with a brushed look: the woodblock's flat colour and its thin line."""
    def __init__(self):
        self.s = Sheet((H, W), ss=3)

    def poly(self, pts, color, alpha=1.0):
        self.s.poly(pts, color, alpha)
        return self

    def line(self, pts, color, w=1.0, alpha=1.0):
        self.s.line(pts, color, w, alpha)
        return self

    def dots(self, pts, color, r=1.4, gap=5.0):
        d, carry = 0.0, 0.0
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            t = carry
            while t < L:
                u = t / L
                self.s.ellipse(x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, r, r, color)
                t += gap
            carry = t - L
        return self

    def done(self):
        return self.s.done()


def wobble(pts, amount, seed):
    rs = np.random.RandomState(seed)
    return [(x + rs.uniform(-amount, amount), y + rs.uniform(-amount, amount)) for x, y in pts]


def cone(pen, x, y, half, h, lit=HILL, shade=HILL_SHADE, line=PRUSSIAN, snow=0.0):
    """A mountain as a cone: a lit face and a shade face, one line round it (the prints' hills)."""
    pen.poly([(x - half, y + h), (x, y), (x + half, y + h)], lit)
    pen.poly([(x, y), (x + half, y + h), (x + half * 0.25, y + h)], shade, 0.8)
    if snow > 0:
        s = snow
        pen.poly([(x, y), (x - half * s, y + h * s), (x - half * s * 0.4, y + h * s * 0.8), (x, y + h * s * 1.1), (x + half * s * 0.45, y + h * s * 0.85), (x + half * s, y + h * s)], SNOW)
    pen.line([(x - half, y + h), (x, y), (x + half, y + h)], line, 0.7, 0.8)


def roof_house(pen, x, y, w=14, h=8, roof=ROOF, wall=WALL):
    """A small house in the manner of a travel map's pictures: a wall and a hipped roof, side on."""
    pen.poly([(x - w / 2, y), (x + w / 2, y), (x + w / 2, y - h * 0.55), (x - w / 2, y - h * 0.55)], wall)
    pen.poly([(x - w / 2 - 2, y - h * 0.55), (x + w / 2 + 2, y - h * 0.55), (x + w / 2 - 3, y - h), (x - w / 2 + 3, y - h)], roof)
    pen.line([(x - w / 2 - 2, y - h * 0.55), (x + w / 2 + 2, y - h * 0.55), (x + w / 2 - 3, y - h), (x - w / 2 + 3, y - h), (x - w / 2 - 2, y - h * 0.55)], PRUSSIAN, 0.7, 0.85)
    pen.line([(x - w / 2, y), (x + w / 2, y)], PRUSSIAN, 0.7, 0.7)


# ---------------------------------------------------------------- the sheet (back.png)
def back():
    x0, y0, x1, y1 = SHEET[0] + 3, SHEET[1] + 3, SHEET[2] - 3, SHEET[3] - 3      # the paper's worn edge wobbles inside the sheet's box
    under = np.zeros((H, W, 3), dtype=F32)
    # the paper, its worn edge
    edge = [p for p in wobble([(x0 + (x1 - x0) * i / 40, y0) for i in range(41)] + [(x1, y0 + (y1 - y0) * i / 20) for i in range(1, 21)]
                              + [(x1 - (x1 - x0) * i / 40, y1) for i in range(1, 41)] + [(x0, y1 - (y1 - y0) * i / 20) for i in range(1, 20)], 1.6, 3)]
    sheet_mask = mask_poly((H, W), edge, soft=0.0)
    under[...] = PAPER
    tooth = noise((H, W), 48, SEED, octaves=4)
    under = under * (1 - 0.05 * tooth[..., None])
    # the land: everything above the coast, soft green, deeper toward the hills' feet
    land_poly = [(x0 - 4, y0 - 4), (x1 + 4, y0 - 4)] + [(x1 + 4, COAST[-1][1])] + COAST[::-1] + [(x0 - 4, COAST[0][1])]
    land = mask_poly((H, W), land_poly, soft=0.0)
    under = lerp(under, LAND, (land * (0.72 + 0.12 * noise((H, W), 90, SEED + 1, octaves=3)))[..., None])
    land_edge = np.clip(land - blur(land, 9), 0, 1)
    under = lerp(under, LAND_DK, (land_edge * 0.35)[..., None])
    # the sea is the paper itself, with its waves drawn on it (below); a pale wash of cerulean near the shore
    shore = np.clip(blur(land, 14) - land, 0, 1)
    under = lerp(under, mixp(CERULEAN, "lead-white", 0.6), (shore * 0.5)[..., None])
    # the folds: five faint lines, the paper a little worn along each
    for k in range(1, PANELS):
        fx = x0 + (x1 - x0) * k / PANELS
        fold = mask_poly((H, W), [(fx - 3, y0), (fx + 3, y0), (fx + 3, y1), (fx - 3, y1)], soft=2.0)
        under = lerp(under, PAPER_WORN, (fold * 0.35)[..., None])
    pic = under if FAST else strokes(under, sizes=(10, 5, 2), seed=SEED, density=1.3, jitter=0.02, keep=0.5)
    # the lines and the pictures of the lie of the land, crisp over the brush
    pen = Pen()
    # the waves: rows of curls on the sea, every row offset half a wave, closer toward the horizon... a map has no horizon:
    # the rows are even, 11 px apart, the curls 14 px long
    row = 0
    yy = y0 + 2
    coast_mask = land > 0.5
    while yy < y1 - 2:
        xx = x0 + 4 + (row % 2) * 7
        while xx < x1 - 8:
            cx = int(min(W - 1, max(0, xx + 7)))
            cy = int(min(H - 1, max(0, yy)))
            if not coast_mask[cy, cx] and not coast_mask[min(H - 1, cy + 4), cx] and sheet_mask[cy, cx] > 0.5:
                pen.line([(xx, yy + 3), (xx + 4, yy - 0.5), (xx + 9, yy - 1.0), (xx + 13, yy + 2.5)], SEA_WAVE, 0.9, 0.75)
                pen.line([(xx + 9, yy - 1.0), (xx + 11, yy + 1.5)], SEA_WAVE, 0.7, 0.6)
            xx += 14
        yy += 11
        row += 1
    # the coast's line, the headland, the river
    pen.line(wobble(COAST, 0.6, 5), PRUSSIAN, 1.0, 0.9)
    pen.poly(HEADLAND, LAND_DK, 0.8)
    pen.line(HEADLAND + HEADLAND[:1], PRUSSIAN, 0.8, 0.85)
    pen.line(RIVER, COBALT, 1.4, 0.8)
    pen.line(RIVER, mixp(CERULEAN, "lead-white", 0.4), 0.5, 0.8)
    # the mountains as cones, the hollow's wooded hills a cluster of deeper ones
    for (mx, my, mh) in MOUNTAINS:
        cone(pen, mx, my, mh * 1.3, mh)
    hx, hy = HILLS_C
    for (dx, dy, mh) in ((-34, 8, 22), (34, 10, 24), (0, -14, 26), (-14, 16, 14), (18, 18, 14)):
        cone(pen, hx + dx, hy + dy - mh, mh * 1.25, mh, lit=mixp(HILL, CEDAR, 0.3), shade=mixp(HILL_SHADE, CEDAR, 0.4))
    # Fuji, white at the right end: a wide cone, snow well down its flanks, its foot lost in the land's green
    fxp, fyp, fhalf, fh = FUJI
    cone(pen, fxp, fyp, fhalf, fh, lit=mixp(COBALT, "lead-white", 0.45), shade=mixp(COBALT, "ultramarine", 0.4), snow=0.62)
    pen.line([(fxp - fhalf * 0.62, fyp + fh * 0.62), (fxp - fhalf * 0.3, fyp + fh * 0.5), (fxp, fyp + fh * 0.68), (fxp + fhalf * 0.32, fyp + fh * 0.52), (fxp + fhalf * 0.62, fyp + fh * 0.62)], PRUSSIAN, 0.6, 0.5)
    # the coast road, dotted along the shore (the Tōkaidō east of Osaka, the Sanyō road west of it): the lie of the land
    road = [(756, 330), (720, 346), (690, 364), (660, 382), (632, 376), (606, 396), (576, 410), (548, 410), (530, 440), (500, 476), (470, 488),
            (440, 470), (404, 452), (370, 440), (352, 432), (330, 440), (300, 452), (270, 446), (240, 436), (200, 424), (156, 416), (110, 414), (60, 424)]
    pen.dots(road, ROAD, 1.1, 4.5)
    # the sheet's title block at the top left, in the manner of a printed map: a small cartouche with a red seal
    pen.poly([(x0 + 14, y0 + 12), (x0 + 112, y0 + 12), (x0 + 112, y0 + 46), (x0 + 14, y0 + 46)], PAPER)
    pen.line([(x0 + 14, y0 + 12), (x0 + 112, y0 + 12), (x0 + 112, y0 + 46), (x0 + 14, y0 + 46), (x0 + 14, y0 + 12)], PRUSSIAN, 0.9, 0.9)
    for i in range(3):
        pen.line([(x0 + 22, y0 + 20 + i * 9), (x0 + 72 - i * 10, y0 + 20 + i * 9)], PRUSSIAN, 1.6, 0.7)
    pen.poly([(x0 + 86, y0 + 20), (x0 + 104, y0 + 20), (x0 + 104, y0 + 38), (x0 + 86, y0 + 38)], RED, 0.85)
    # a compass note: east at the right, a small sun
    pen.s.ellipse(x1 - 30, y0 + 28, 7, 7, RED, 0.9)
    pen.line([(x1 - 30, y0 + 40), (x1 - 30, y0 + 52)], PRUSSIAN, 0.8, 0.7)
    c, a = pen.done()
    pic = over(pic, c, a)
    pic = grain(np.clip(pic, 0, 1), SEED, 0.018)
    return pic, sheet_mask


# ---------------------------------------------------------------- the places
def place_yui(pen):
    cx, cy = PLACES["yui"][0]
    for (dx, dy, w) in ((-18, 8, 13), (-4, 10, 14), (12, 7, 12), (24, 11, 11), (4, 0, 11)):
        roof_house(pen, cx + dx, cy + dy, w, 8, roof=mixp(ROOF, WOOD, 0.3))
    # two boats drawn up on the sand, a net rack
    for (bx, by) in ((cx - 10, cy + 22), (cx + 14, cy + 24)):
        pen.poly([(bx - 8, by), (bx + 8, by), (bx + 10, by - 3), (bx - 9, by - 4)], WOOD)
        pen.line([(bx - 9, by - 4), (bx + 10, by - 3), (bx + 8, by), (bx - 8, by), (bx - 9, by - 4)], PRUSSIAN, 0.6, 0.8)
    pen.line([(cx + 30, cy + 16), (cx + 30, cy + 4), (cx + 42, cy + 4), (cx + 42, cy + 16)], WOOD, 1.2, 0.9)


def place_osaka(pen):
    cx, cy = PLACES["osaka"][0]
    for (dx, dy, w) in ((-20, 6, 12), (-8, 10, 13), (6, 8, 12), (18, 12, 12), (-14, -4, 12), (0, -2, 12), (14, -2, 11), (28, 2, 10)):
        roof_house(pen, cx + dx, cy + dy, w, 8)
    # a castle tower above the town (the city's keep), and a bridge over the river mouth
    tx, ty = cx - 4, cy - 14
    pen.poly([(tx - 6, ty + 6), (tx + 6, ty + 6), (tx + 5, ty - 6), (tx - 5, ty - 6)], WALL)
    pen.poly([(tx - 9, ty - 6), (tx + 9, ty - 6), (tx + 4, ty - 12), (tx - 4, ty - 12)], ROOF)
    pen.poly([(tx - 7, ty - 12), (tx + 7, ty - 12), (tx + 2, ty - 17), (tx - 2, ty - 17)], ROOF)
    pen.line([(tx - 6, ty + 6), (tx + 6, ty + 6), (tx + 5, ty - 6), (tx + 9, ty - 6), (tx + 4, ty - 12), (tx + 7, ty - 12), (tx + 2, ty - 17), (tx - 2, ty - 17),
              (tx - 7, ty - 12), (tx - 4, ty - 12), (tx - 9, ty - 6), (tx - 5, ty - 6), (tx - 6, ty + 6)], PRUSSIAN, 0.7, 0.9)
    bx, by = cx + 2, cy + 20
    pen.line([(bx - 12, by + 2), (bx - 6, by - 3), (bx + 6, by - 3), (bx + 12, by + 2)], WOOD, 2.2, 0.95)
    pen.line([(bx - 12, by + 2), (bx - 6, by - 3), (bx + 6, by - 3), (bx + 12, by + 2)], PRUSSIAN, 0.6, 0.7)


def place_hills(pen):
    cx, cy = PLACES["hills"][0]
    # cedars: tall narrow dark triangles on the slopes round a hollow, and in the hollow the charcoal-burner's thatched roof
    for (dx, dy, h) in ((-26, 6, 18), (-18, 12, 22), (-8, 4, 16), (10, 8, 20), (22, 2, 17), (28, 12, 20), (-30, -8, 14), (2, -10, 16), (16, -8, 14)):
        pen.poly([(cx + dx - 3.5, cy + dy + 8), (cx + dx, cy + dy + 8 - h), (cx + dx + 3.5, cy + dy + 8)], CEDAR)
        pen.line([(cx + dx, cy + dy + 8), (cx + dx, cy + dy + 12)], mixp("burnt-sienna", "prussian-blue", 0.4), 1.0, 0.9)
    hx, hy = cx - 2, cy + 20
    pen.poly([(hx - 8, hy), (hx + 8, hy), (hx + 8, hy - 5), (hx - 8, hy - 5)], mixp(WOOD, "burnt-sienna", 0.5))
    pen.poly([(hx - 11, hy - 5), (hx + 11, hy - 5), (hx + 5, hy - 13), (hx - 5, hy - 13)], mixp("yellow-ochre", "lead-white", 0.3))
    pen.line([(hx - 11, hy - 5), (hx + 11, hy - 5), (hx + 5, hy - 13), (hx - 5, hy - 13), (hx - 11, hy - 5)], PRUSSIAN, 0.7, 0.9)
    pen.line([(hx - 8, hy), (hx + 8, hy)], PRUSSIAN, 0.6, 0.7)


def place_himeji(pen):
    cx, cy = PLACES["himeji"][0]
    # the town along the foot, the hill, the keep on it: white walls and three stacked roofs
    for (dx, dy, w) in ((-26, 22, 11), (-12, 24, 12), (4, 24, 12), (20, 22, 11), (32, 18, 10)):
        roof_house(pen, cx + dx, cy + dy, w, 7)
    pen.poly([(cx - 24, cy + 14), (cx + 24, cy + 14), (cx + 14, cy + 2), (cx - 14, cy + 2)], mixp(LAND_DK, HILL, 0.4))
    pen.line([(cx - 24, cy + 14), (cx - 14, cy + 2), (cx + 14, cy + 2), (cx + 24, cy + 14)], PRUSSIAN, 0.7, 0.8)
    kx, ky = cx, cy + 2
    pen.poly([(kx - 10, ky), (kx + 10, ky), (kx + 9, ky - 8), (kx - 9, ky - 8)], WALL)
    pen.poly([(kx - 13, ky - 8), (kx + 13, ky - 8), (kx + 7, ky - 13), (kx - 7, ky - 13)], ROOF)
    pen.poly([(kx - 8, ky - 13), (kx + 8, ky - 13), (kx + 7, ky - 19), (kx - 7, ky - 19)], WALL)
    pen.poly([(kx - 10, ky - 19), (kx + 10, ky - 19), (kx + 5, ky - 24), (kx - 5, ky - 24)], ROOF)
    pen.poly([(kx - 6, ky - 24), (kx + 6, ky - 24), (kx + 5, ky - 29), (kx - 5, ky - 29)], WALL)
    pen.poly([(kx - 8, ky - 29), (kx + 8, ky - 29), (kx + 2, ky - 34), (kx - 2, ky - 34)], ROOF)
    pen.line([(kx - 10, ky), (kx + 10, ky), (kx + 9, ky - 8), (kx + 13, ky - 8), (kx + 7, ky - 13), (kx + 8, ky - 13), (kx + 7, ky - 19), (kx + 10, ky - 19), (kx + 5, ky - 24),
              (kx + 6, ky - 24), (kx + 5, ky - 29), (kx + 8, ky - 29), (kx + 2, ky - 34), (kx - 2, ky - 34), (kx - 8, ky - 29), (kx - 5, ky - 29), (kx - 6, ky - 24), (kx - 10, ky - 24),
              (kx - 5, ky - 19), (kx - 7, ky - 19), (kx - 8, ky - 13), (kx - 7, ky - 13), (kx - 13, ky - 8), (kx - 9, ky - 8), (kx - 10, ky)], PRUSSIAN, 0.7, 0.9)
    # a double cherry at the keep's foot: a round pink head
    pen.s.ellipse(kx + 15, ky - 2, 4.5, 4, mixp("geranium-lake", "lead-white", 0.62), 0.95)
    pen.line([(kx + 15, ky + 2), (kx + 15, ky + 7)], mixp("burnt-sienna", "prussian-blue", 0.4), 1.0, 0.9)


PLACE_PAINTERS = {"yui": place_yui, "osaka": place_osaka, "hills": place_hills, "himeji": place_himeji}


def way_sea(pen):
    pts = WAYS[("yui", "osaka")]
    pen.dots(pts, PRUSSIAN, 1.3, 6.0)
    # a small ship on the course, one square sail
    sx, sy = pts[4]
    pen.poly([(sx - 9, sy + 2), (sx + 9, sy + 2), (sx + 7, sy + 6), (sx - 7, sy + 6)], WOOD)
    pen.line([(sx, sy + 2), (sx, sy - 12)], PRUSSIAN, 0.9, 0.9)
    pen.poly([(sx - 6, sy - 11), (sx + 6, sy - 11), (sx + 6, sy - 1), (sx - 6, sy - 1)], WALL)
    pen.line([(sx - 6, sy - 11), (sx + 6, sy - 11), (sx + 6, sy - 1), (sx - 6, sy - 1), (sx - 6, sy - 11)], PRUSSIAN, 0.6, 0.8)
    pen.line([(sx - 9, sy + 2), (sx + 9, sy + 2), (sx + 7, sy + 6), (sx - 7, sy + 6), (sx - 9, sy + 2)], PRUSSIAN, 0.6, 0.8)


def way_road(key):
    def f(pen):
        pen.dots(WAYS[key], ROAD, 1.5, 5.0)
        pen.dots(WAYS[key], PRUSSIAN, 0.7, 5.0)
    return f


WAY_PAINTERS = {("yui", "osaka"): way_sea, ("osaka", "hills"): way_road(("osaka", "hills")), ("hills", "himeji"): way_road(("hills", "himeji"))}


# ---------------------------------------------------------------- layout.json: shapes measured from the pictures
def trace(m):
    h, w = m.shape
    pad = np.zeros((h + 2, w + 2), bool)
    pad[1:-1, 1:-1] = m
    ys, xs = np.nonzero(pad)
    start = (xs[np.argmin(ys * 10000 + xs)], ys.min())
    x, y = start
    d = 0
    pts = [(x, y)]
    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def filled(px, py):
        return 0 <= py < h + 2 and 0 <= px < w + 2 and pad[py, px]
    for _ in range(400000):
        dx, dy = moves[d]
        if d == 0:
            a, b = (x, y - 1), (x, y)
        elif d == 1:
            a, b = (x, y), (x - 1, y)
        elif d == 2:
            a, b = (x - 1, y), (x - 1, y - 1)
        else:
            a, b = (x - 1, y - 1), (x, y - 1)
        fa, fb = filled(*a), filled(*b)
        if fb and not fa:
            x, y = x + dx, y + dy
        elif fa:
            d = (d - 1) % 4
            continue
        else:
            d = (d + 1) % 4
            continue
        pts.append((x, y))
        if (x, y) == start and len(pts) > 2:
            break
    return [(px - 1, py - 1) for px, py in pts]


def simplify(pts, eps):
    def dp(seg):
        if len(seg) < 3:
            return seg
        a, b = np.asarray(seg[0], float), np.asarray(seg[-1], float)
        ab = b - a
        L = math.hypot(*ab) or 1.0
        d = [abs((p[0] - a[0]) * ab[1] - (p[1] - a[1]) * ab[0]) / L for p in seg[1:-1]]
        i = int(np.argmax(d)) + 1
        if d[i - 1] > eps:
            return dp(seg[:i + 1])[:-1] + dp(seg[i:])
        return [seg[0], seg[-1]]
    far = int(np.argmax([math.hypot(p[0] - pts[0][0], p[1] - pts[0][1]) for p in pts]))
    return dp(pts[:far + 1])[:-1] + dp(pts[far:] + [pts[0]])[:-1]


def dilate(m, r):
    out = m.copy()
    r = int(r)
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r and (dx or dy):
                out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def shape_of(mask, limit=24):
    pts = trace(mask)
    eps = 0.8
    while True:
        s = simplify(pts, eps)
        if len(s) <= limit:
            return [[int(round(x)), int(round(y))] for x, y in s]
        eps *= 1.25


def layout(alphas):
    places = []
    for pid, (mid, pin, label, name) in PLACES.items():
        m = dilate(alphas[pid] > 0.5, 7)                    # (grown so that a place's separate pieces, roofs and boats, join in one shape)
        shape = shape_of(m)
        from PIL import ImageFont
        from letter import KOINE
        f = ImageFont.truetype(KOINE, LABEL["size"])
        width = f.getlength(name) + LABEL["spacing"] * LABEL["size"] * (len(name) - 1)
        places.append({"id": pid, "picture": f"place-{pid}.png", "shape": shape, "pin": list(pin), "label": list(label), "label_max": int(math.ceil(width)) + 8})
    pins = {p["id"]: p["pin"] for p in places}
    paths = []
    for (a, b), pts in WAYS.items():
        paths.append({"a": a, "b": b, "picture": f"path-{a}-{b}.png", "via": [pins[a]] + [list(p) for p in pts] + [pins[b]]})
    return {
        "map": "edo", "size": [800, 600], "sheet": SHEET,
        "material": ("A travel map printed from woodblocks on a long sheet of soft paper, folded in six panels and worn at the folds: the "
                     "coast road from Suruga to Harima, the land soft green with its mountains as cones, the sea in rows of blue waves, Fuji "
                     "white at the east end, the places as small pictures with their names."),
        "label": LABEL,
        "places": places, "paths": paths,
        "note": ("East at the right. yui on the west shore of Suruga Bay under the Satta headland, Fuji across the water (drawn on the sheet: the "
                 "lie of the land); osaka at its river mouth west of the Kii peninsula's bulge (a landmark: no scene); hills north of Osaka up the "
                 "river (the hollow in the wooded hills: cedars and the storehouse); himeji at the west end on its hill above the town, the "
                 "Inland Sea below. The sea way goes out from Yui's shore round the Kii tip into Osaka's bay (a ship drawn on it at its fifth "
                 "point); road1 follows the river up into the hills; road2 comes down to the coast road and west. Each via is a pin, the way's "
                 "drawn points, the other pin. The pins (rows of three portraits, 116 x 36) stand on the land above each place (Osaka's on the "
                 "sea below it); the names below each place (the hills' above)."),
    }


def dumps(lay):
    s = json.dumps(lay, indent=2)
    s = re.sub(r"\[\s+(-?\d+),\s+(-?\d+)\s+\]", r"[\1, \2]", s)
    s = re.sub(r"\[\s+((?:\[-?\d+, -?\d+\],?\s*)+)\]", lambda m: "[" + re.sub(r"\s+", " ", m.group(1)).strip() + "]", s)
    s = re.sub(r"\[\s+(-?\d+),\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+\]", r"[\1, \2, \3, \4]", s)
    return s + "\n"


# ---------------------------------------------------------------- all of it
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    pic, sheet_mask = back()
    files = {"back": (pic, sheet_mask)}
    alphas = {}
    for pid, fn in PLACE_PAINTERS.items():
        pen = Pen()
        fn(pen)
        c, a = pen.done()
        files[f"place-{pid}"] = (over(pic.copy(), c, a), a)
        alphas[pid] = a
    for (a_, b_), fn in WAY_PAINTERS.items():
        pen = Pen()
        fn(pen)
        c, a = pen.done()
        files[f"path-{a_}-{b_}"] = (over(pic.copy(), c, a), a)
    # one palette for all of a map's files: the sheet with everything laid on it
    everything = pic.copy()
    for name, (c, a) in files.items():
        if name != "back":
            everything = over(everything, c, a)
    pal = palette_of([everything], colors=255, seed=3)
    for name, (c, a) in files.items():
        idx = to_palette(c, pal, seed=5, speckle=0.012)
        save(f"{OUT}/{name}.png", idx, pal, alpha=(a > 0.5).astype(F32))
    lay = layout(alphas)
    with open(f"{OUT}/layout.json", "w") as f:
        f.write(dumps(lay))
    Image.fromarray((np.clip(everything, 0, 1) * 255 + 0.5).astype(np.uint8)).save("out/map-edo-look.png")
    print(f"{OUT}: {len(files)} pictures; places", {p['id']: (p['pin'], p['label'], len(p['shape'])) for p in lay['places']})

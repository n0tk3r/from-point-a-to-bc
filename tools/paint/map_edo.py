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
# PAINT-21F: the Yodo comes down from the north-east (from Kyoto, off the sheet's top) past Hirakata to Osaka's mouth
YODO = [(462, 262), (446, 282), (428, 302), (410, 322), (394, 342), (378, 362), (362, 384), (348, 406), (336, 426)]
HIRAKATA = (394, 342)                      # the Kyoto boat's relay port on the Yodo (the river path's turn north)
# PAINT-21F: Awaji, low and long across the strait from Akashi (the island's north tip by Akashi, its length to the south-west)
AWAJI = [(206, 433), (222, 431), (230, 438), (220, 456), (196, 478), (170, 500), (146, 520), (122, 534), (104, 538),
         (100, 528), (116, 510), (140, 488), (166, 466), (188, 448)]
MOUNTAINS = [(100, 300, 26), (150, 262, 22), (210, 290, 30), (250, 240, 20), (340, 232, 26), (390, 300, 32), (430, 262, 24), (470, 320, 28),
             (520, 240, 22), (560, 300, 30), (596, 250, 24), (640, 290, 20), (180, 350, 16), (440, 400, 18), (470, 430, 14), (700, 300, 14), (740, 270, 18)]
HILLS_C = (300, 262)                       # the hollow in the wooded hills north of Osaka
HILL_CONES = [(-34, 8, 22), (34, 10, 24), (0, -14, 26), (-14, 16, 14), (18, 18, 14)]   # PAINT-21F: the hollow's cones about HILLS_C (lifted out of back(): a stop's name keeps off them)
AWAJI_CONES = [(176, 470, 10), (146, 496, 9)]                                       # PAINT-21F: a cone or two on Awaji (lifted out of back())
# the coast road, dotted along the shore (the Tōkaidō east of Osaka, the Sanyō road west of it): the lie of the land
COAST_ROAD = [(756, 330), (720, 346), (690, 364), (660, 382), (632, 376), (606, 396), (576, 410), (548, 410), (530, 440), (500, 476), (470, 488),
              (440, 470), (404, 452), (370, 440), (352, 432), (326, 420), (304, 408), (286, 402), (272, 414), (258, 420), (244, 420), (232, 414),
              (222, 404), (204, 398), (184, 396), (164, 386), (140, 378), (112, 380), (84, 394), (54, 404)]      # PAINT-21F: west of Osaka, the Saigoku road the ways follow (lifted out of back())
CARTOUCHE = (400, 185)                     # PAINT-21F: the title block's top left (it was at the top left of the sheet: Shosha is there now)
PLACES = {                                 # id: (the drawing's middle, the pin, the name's baseline middle, the name)   (PAINT-21F: six, in maps.js's order)
    "yui": ((632, 350), (640, 312), (632, 392), "Yui"),
    "osaka": ((338, 408), (382, 474), (402, 440), "Osaka"),
    "hills": ((300, 262), (300, 308), (300, 222), "The hills"),
    "akashi": ((198, 410), (240, 352), (186, 472), "Akashi"),
    "himeji": ((118, 344), (118, 296), (106, 400), "Himeji"),
    "shosha": ((88, 228), (166, 230), (86, 192), "Shosha"),
}
WAYS = {                                   # (PAINT-21F: five, in maps.js's order; each the drawn points between the two pins)
    ("yui", "osaka"): [(596, 402), (590, 440), (574, 484), (530, 516), (482, 532), (436, 518), (404, 496)],
    ("osaka", "hills"): [(362, 452), (340, 430), (348, 406), (362, 384), (378, 362), (394, 342), (380, 334), (366, 330), (346, 322), (324, 314)],
    ("hills", "akashi"): [(304, 330), (300, 348), (292, 368), (286, 388), (282, 402), (272, 414), (258, 420), (244, 420), (232, 414),
                          (222, 404), (228, 386), (234, 370)],
    ("akashi", "himeji"): [(232, 372), (224, 392), (204, 398), (184, 396), (164, 386), (148, 372), (132, 352), (122, 326)],
    ("himeji", "shosha"): [(112, 278), (116, 262), (130, 250), (148, 238)],
}
RIVER_LEG = 6                              # PAINT-21F: the river path's via: Osaka's pin, then its first RIVER_LEG points are on the water (to Hirakata), the rest the road
STOPS = {                                  # PAINT-21F: the stops (maps.js `stops`, its order): (the drawing's middle, the way, its pin: the point of the way the picture is for)
    "hirakata": ((410, 354), ("osaka", "hills"), (394, 342)),         # (MERGE-21's follow-up: the river's turn, where the river ends and the road begins: the Kyoto boat's first segment ends here)
    # the walk's three: each pin is on the way's line where the portraits stop for it, so that their row (116 x 36 about the pin)
    # stands just above the picture and leaves it clear, and the stop's line, said above the row, does not cover it either
    "koriyama": ((318, 352), ("hills", "akashi"), (302, 320)),        # (just down out of the hills: there is no room lower for the row above the picture)
    "suma": ((262, 434), ("hills", "akashi"), (282, 402)),
    "maiko": ((236, 432), ("hills", "akashi"), (223, 400)),
}
ROW = (116, 36)                            # PAINT-21F: a row of three portraits about a pin (atlas.js faces: 36 across, 4 apart)


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
    land = np.maximum(mask_poly((H, W), land_poly, soft=0.0), mask_poly((H, W), AWAJI, soft=0.0) * sheet_mask)      # PAINT-21F: and Awaji
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
    aw = wobble(AWAJI, 0.5, 6)                                                       # PAINT-21F: Awaji's shore, and a cone or two on it
    pen.line(aw + aw[:1], PRUSSIAN, 0.9, 0.85)
    for (mx, my, mh) in AWAJI_CONES:                                                 # (PAINT-21F: the constant)
        cone(pen, mx, my, mh * 1.4, mh)
    pen.line(YODO, COBALT, 1.4, 0.8)                                                 # PAINT-21F: the Yodo from the north-east (was a river from the hills)
    pen.line(YODO, mixp(CERULEAN, "lead-white", 0.4), 0.5, 0.8)
    # the mountains as cones, the hollow's wooded hills a cluster of deeper ones
    for (mx, my, mh) in MOUNTAINS:
        cone(pen, mx, my, mh * 1.3, mh)
    hx, hy = HILLS_C
    for (dx, dy, mh) in HILL_CONES:                                                  # (PAINT-21F: the constant)
        cone(pen, hx + dx, hy + dy - mh, mh * 1.25, mh, lit=mixp(HILL, CEDAR, 0.3), shade=mixp(HILL_SHADE, CEDAR, 0.4))
    # Fuji, white at the right end: a wide cone, snow well down its flanks, its foot lost in the land's green
    fxp, fyp, fhalf, fh = FUJI
    cone(pen, fxp, fyp, fhalf, fh, lit=mixp(COBALT, "lead-white", 0.45), shade=mixp(COBALT, "ultramarine", 0.4), snow=0.62)
    pen.line([(fxp - fhalf * 0.62, fyp + fh * 0.62), (fxp - fhalf * 0.3, fyp + fh * 0.5), (fxp, fyp + fh * 0.68), (fxp + fhalf * 0.32, fyp + fh * 0.52), (fxp + fhalf * 0.62, fyp + fh * 0.62)], PRUSSIAN, 0.6, 0.5)
    # the coast road, dotted along the shore (PAINT-21F: COAST_ROAD, lifted out to the constants)
    pen.dots(COAST_ROAD, ROAD, 1.1, 4.5)
    # the sheet's title block at the top left, in the manner of a printed map: a small cartouche with a red seal
    cx0, cy0 = CARTOUCHE[0] - 14, CARTOUCHE[1] - 12                                 # PAINT-21F: moved to the top middle (Shosha is at the top left)
    pen.poly([(cx0 + 14, cy0 + 12), (cx0 + 112, cy0 + 12), (cx0 + 112, cy0 + 46), (cx0 + 14, cy0 + 46)], PAPER)
    pen.line([(cx0 + 14, cy0 + 12), (cx0 + 112, cy0 + 12), (cx0 + 112, cy0 + 46), (cx0 + 14, cy0 + 46), (cx0 + 14, cy0 + 12)], PRUSSIAN, 0.9, 0.9)
    for i in range(3):
        pen.line([(cx0 + 22, cy0 + 20 + i * 9), (cx0 + 72 - i * 10, cy0 + 20 + i * 9)], PRUSSIAN, 1.6, 0.7)
    pen.poly([(cx0 + 86, cy0 + 20), (cx0 + 104, cy0 + 20), (cx0 + 104, cy0 + 38), (cx0 + 86, cy0 + 38)], RED, 0.85)
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
    """PAINT-21F: Osaka in 1830, at its river mouth: roofs on roofs, the white warehouses of the rice dealers on the river,
    a bridge, and upstream on its rise the CASTLE'S WALLS AND TURRETS, NO KEEP (it burned in 1665 and was not rebuilt
    until 1931: round twenty's picture had one)."""
    cx, cy = PLACES["osaka"][0]
    for (dx, dy, w) in ((-24, 8, 12), (-12, 12, 13), (2, 10, 12), (16, 14, 12), (-18, -2, 12), (-4, 0, 12), (10, 2, 11), (26, 6, 10)):
        roof_house(pen, cx + dx, cy + dy, w, 8)
    for (dx, dy) in ((-30, 20), (-20, 22)):                                          # two white warehouses on the water: tall walls, dark roofs
        x, y = cx + dx, cy + dy
        pen.poly([(x - 5, y), (x + 5, y), (x + 5, y - 9), (x - 5, y - 9)], WALL)
        pen.poly([(x - 6.5, y - 9), (x + 6.5, y - 9), (x + 4.5, y - 13), (x - 4.5, y - 13)], ROOF)
        pen.line([(x - 5, y), (x - 5, y - 9), (x - 6.5, y - 9), (x - 4.5, y - 13), (x + 4.5, y - 13), (x + 6.5, y - 9), (x + 5, y - 9), (x + 5, y)], PRUSSIAN, 0.6, 0.85)
        pen.line([(x - 2, y - 3), (x + 2, y - 3)], PRUSSIAN, 0.6, 0.6)
    # the castle upstream on its rise: a long stone base, a white wall along it, three small turrets, and nothing on top
    bx, by = cx + 22, cy - 14
    pen.poly([(bx - 20, by + 6), (bx + 20, by + 6), (bx + 16, by), (bx - 16, by)], mixp(WOOD, WALL, 0.45))
    pen.line([(bx - 20, by + 6), (bx - 16, by), (bx + 16, by), (bx + 20, by + 6)], PRUSSIAN, 0.6, 0.8)
    pen.poly([(bx - 16, by), (bx + 16, by), (bx + 16, by - 3), (bx - 16, by - 3)], WALL)
    pen.line([(bx - 16, by - 3), (bx + 16, by - 3)], ROOF, 1.0, 0.9)
    for (tx, h) in ((bx - 13, 6), (bx + 1, 7), (bx + 13, 6)):
        pen.poly([(tx - 3.5, by - 3), (tx + 3.5, by - 3), (tx + 3.5, by - 3 - h * 0.6), (tx - 3.5, by - 3 - h * 0.6)], WALL)
        pen.poly([(tx - 5, by - 3 - h * 0.6), (tx + 5, by - 3 - h * 0.6), (tx + 2.5, by - 3 - h), (tx - 2.5, by - 3 - h)], ROOF)
        pen.line([(tx - 3.5, by - 3), (tx - 3.5, by - 3 - h * 0.6), (tx - 5, by - 3 - h * 0.6), (tx - 2.5, by - 3 - h), (tx + 2.5, by - 3 - h), (tx + 5, by - 3 - h * 0.6), (tx + 3.5, by - 3 - h * 0.6), (tx + 3.5, by - 3)], PRUSSIAN, 0.6, 0.85)
    bx, by = cx - 10, cy + 26                                                        # a bridge over the river mouth
    pen.line([(bx - 12, by + 2), (bx - 6, by - 3), (bx + 6, by - 3), (bx + 12, by + 2)], WOOD, 2.2, 0.95)
    pen.line([(bx - 12, by + 2), (bx - 6, by - 3), (bx + 6, by - 3), (bx + 12, by + 2)], PRUSSIAN, 0.6, 0.7)


def place_akashi(pen):
    """PAINT-21F: Akashi above its strait: the castle on its rise with FOUR CORNER TURRETS AND NO KEEP (none was ever built),
    the town's roofs at its foot, the shore's pines bent toward the sea, the white sand; Awaji low across the strait is the
    sheet's own."""
    cx, cy = PLACES["akashi"][0]
    # the castle: a stone base, a white wall round its top, a turret at each corner (three storeys: three small roofs), no keep
    bx, by = cx + 2, cy - 10
    pen.poly([(bx - 18, by + 6), (bx + 18, by + 6), (bx + 14, by - 1), (bx - 14, by - 1)], mixp(WOOD, WALL, 0.45))
    pen.line([(bx - 18, by + 6), (bx - 14, by - 1), (bx + 14, by - 1), (bx + 18, by + 6)], PRUSSIAN, 0.6, 0.8)
    pen.poly([(bx - 14, by - 1), (bx + 14, by - 1), (bx + 14, by - 3.5), (bx - 14, by - 3.5)], WALL)
    pen.line([(bx - 14, by - 3.5), (bx + 14, by - 3.5)], ROOF, 1.0, 0.9)
    for tx in (bx - 12, bx + 12):
        ty = by - 3.5
        for k in range(3):                                                           # three storeys, each a little smaller
            w = 4.2 - k * 0.9
            pen.poly([(tx - w, ty), (tx + w, ty), (tx + w, ty - 2.4), (tx - w, ty - 2.4)], WALL)
            pen.poly([(tx - w - 1.4, ty - 2.4), (tx + w + 1.4, ty - 2.4), (tx + w - 0.6, ty - 4.0), (tx - w + 0.6, ty - 4.0)], ROOF)
            ty -= 4.0
        pen.line([(tx - 4.2, by - 3.5), (tx - 4.2, ty + 1.6), (tx + 4.2, ty + 1.6), (tx + 4.2, by - 3.5)], PRUSSIAN, 0.5, 0.6)
    for tx in (bx - 6, bx + 6):                                                      # the two far turrets, smaller, behind the wall
        pen.poly([(tx - 2.4, by - 3.5), (tx + 2.4, by - 3.5), (tx + 2.4, by - 6.5), (tx - 2.4, by - 6.5)], WALL)
        pen.poly([(tx - 3.4, by - 6.5), (tx + 3.4, by - 6.5), (tx + 1.6, by - 8.6), (tx - 1.6, by - 8.6)], ROOF)
    # the town at its foot, along the shore
    for (dx, dy, w) in ((-22, 10, 10), (-10, 12, 11), (14, 12, 11), (24, 9, 9)):
        roof_house(pen, cx + dx, cy + dy, w, 6.5)
    # the white sand and the pines along it, bent toward the sea (south)
    pen.poly([(cx - 26, cy + 15), (cx + 30, cy + 15), (cx + 28, cy + 19), (cx - 24, cy + 19)], mixp(WALL, "lead-white", 0.5), 0.95)
    for (px, h) in ((cx - 24, 7), (cx - 17, 8), (cx + 20, 7), (cx + 27, 6)):
        pen.line([(px, cy + 16), (px + 1.5, cy + 16 - h * 0.6), (px + 3.5, cy + 16 - h)], mixp("burnt-sienna", "prussian-blue", 0.4), 1.0, 0.9)
        pen.s.ellipse(px + 4.0, cy + 16 - h, 3.4, 1.7, CEDAR, 0.95)


def place_shosha(pen):
    """PAINT-21F: Mount Shosha north-west of Himeji: a wooded mountain (pines and maples, deeper green than the far cones),
    the east path a dotted line climbing into the trees, and at its foot the small women's hall, deep-roofed on a low base."""
    cx, cy = PLACES["shosha"][0]
    apex = (cx - 4, cy - 30)
    base_y = cy + 22
    pen.poly([(cx - 34, base_y), apex, (cx + 30, base_y)], mixp(HILL, CEDAR, 0.45))
    pen.poly([apex, (cx + 30, base_y), (cx + 6, base_y)], mixp(HILL_SHADE, CEDAR, 0.5), 0.85)
    pen.line([(cx - 34, base_y), apex, (cx + 30, base_y)], PRUSSIAN, 0.7, 0.85)
    rs = np.random.RandomState(27)
    for _ in range(16):                                                              # the trees on its slopes
        t = rs.uniform(0.25, 0.95)
        side = rs.uniform(-0.85, 0.85)
        x = apex[0] + side * 30 * t
        y = apex[1] + 52 * t
        h = rs.uniform(5, 8)
        c = CEDAR if rs.rand() < 0.6 else mixp(CEDAR, "burnt-sienna", 0.35)
        pen.poly([(x - 2.4, y), (x, y - h), (x + 2.4, y)], c, 0.95)
    pen.dots([(cx + 14, base_y - 2), (cx + 8, cy + 8), (cx + 2, cy - 4), (cx - 2, cy - 16)], mixp("burnt-sienna", "yellow-ochre", 0.4), 0.7, 3.0)   # the east path
    hx, hy = cx + 18, base_y + 1                                                     # the women's hall at the path's foot
    pen.poly([(hx - 5, hy), (hx + 5, hy), (hx + 5, hy - 4), (hx - 5, hy - 4)], WOOD)
    pen.poly([(hx - 8, hy - 4), (hx + 8, hy - 4), (hx + 4, hy - 9), (hx - 4, hy - 9)], ROOF)
    pen.line([(hx - 8, hy - 4), (hx + 8, hy - 4), (hx + 4, hy - 9), (hx - 4, hy - 9), (hx - 8, hy - 4)], PRUSSIAN, 0.6, 0.9)
    pen.line([(hx - 6, hy + 1), (hx + 6, hy + 1)], mixp(WALL, "prussian-blue", 0.3), 1.2, 0.9)


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


PLACE_PAINTERS = {"yui": place_yui, "osaka": place_osaka, "hills": place_hills, "akashi": place_akashi, "himeji": place_himeji,
                  "shosha": place_shosha}                                            # PAINT-21F: six


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
    pen.dots([pts[-1], PLACES["osaka"][1]], PRUSSIAN, 1.3, 6.0)                     # PAINT-21F: on to Osaka's pin (it moved east of the city)


def way_river(pen):
    """PAINT-21F: the river path: from Osaka's pin into the river mouth and up the Yodo to Hirakata (a boat's course, dashed
    in blue, with the Kyoto boat drawn on it, hauled from the bank), across by the ferry, and a road north into the hills
    (dotted, as the roads are)."""
    pin = PLACES["osaka"][1]
    pts = [pin] + WAYS[("osaka", "hills")]
    water = pts[:RIVER_LEG + 1]
    road = pts[RIVER_LEG:] + [PLACES["hills"][1]]
    d, carry = 0.0, 0.0
    for (x0, y0), (x1, y1) in zip(water, water[1:]):                                 # the boat's course: short dashes
        L = math.hypot(x1 - x0, y1 - y0)
        t = carry
        while t < L:
            u0, u1 = t / L, min(1.0, (t + 3.0) / L)
            pen.line([(x0 + (x1 - x0) * u0, y0 + (y1 - y0) * u0), (x0 + (x1 - x0) * u1, y0 + (y1 - y0) * u1)], PRUSSIAN, 1.2, 0.95)
            t += 6.0
        carry = t - L
    bx, by = (water[4][0] + water[5][0]) / 2, (water[4][1] + water[5][1]) / 2         # the Kyoto boat, hauled up the river below Hirakata (the stop's landing has its own boat): long, low, a mat roof, its tow line to the bank
    ang = math.atan2(water[5][1] - water[4][1], water[5][0] - water[4][0])
    ca, sa = math.cos(ang), math.sin(ang)
    R_ = lambda pts_: [(bx + x * ca - y * sa, by + x * sa + y * ca) for x, y in pts_]
    pen.poly(R_([(-8, -1.6), (8, -1.6), (9.5, 0), (8, 1.8), (-8, 1.8), (-9.5, 0)]), WOOD)
    pen.poly(R_([(-5, -1.6), (5, -1.6), (4, -3.6), (-4, -3.6)]), mixp("yellow-ochre", "lead-white", 0.3))
    pen.line(R_([(-8, -1.6), (8, -1.6), (9.5, 0), (8, 1.8), (-8, 1.8), (-9.5, 0), (-8, -1.6)]), PRUSSIAN, 0.5, 0.85)
    pen.line([R_([(7, -1)])[0], (bx + 13 * ca + 6 * sa, by + 13 * sa - 6 * ca)], mixp("burnt-sienna", "yellow-ochre", 0.4), 0.9, 0.95)      # (PAINT-21F: a little heavier, so it holds as one line)
    pen.dots(road, ROAD, 1.5, 5.0)
    pen.dots(road, PRUSSIAN, 0.7, 5.0)


def way_road(key, extra=None):
    def f(pen):
        pts = [PLACES[key[0]][1]] + WAYS[key] + [PLACES[key[1]][1]]
        pen.dots(pts, ROAD, 1.5, 5.0)
        pen.dots(pts, PRUSSIAN, 0.7, 5.0)
    return f


WAY_PAINTERS = {("yui", "osaka"): way_sea, ("osaka", "hills"): way_river, ("hills", "akashi"): way_road(("hills", "akashi")),
                ("akashi", "himeji"): way_road(("akashi", "himeji")), ("himeji", "shosha"): way_road(("himeji", "shosha"))}   # PAINT-21F: five


def stop_hirakata(pen):
    """PAINT-21F (MERGE-21's follow-up): Hirakata, the Kyoto boats' relay port on the Yodo's east bank, where the river path
    ends and the ferry crosses to the road north: a little landing of planks out into the river, a passenger boat moored
    at it (long and low, its mat roof), and the boat-waiting inn's roofs on the bank behind."""
    tx, ty = STOPS["hirakata"][2]                                                    # the river's turn (the pin)
    d = (0.625, -0.781)                                                              # the river's way here (upstream, north-east)
    n = (0.781, 0.625)                                                               # toward the east bank
    P_ = lambda a, b: (tx + d[0] * a + n[0] * b, ty + d[1] * a + n[1] * b)           # a point a along the river, b toward the bank
    landing = [P_(-3, 2), P_(3, 2), P_(3, 11), P_(-3, 11)]                          # the landing: planks from the bank into the river
    pen.poly(landing, WOOD)
    pen.line(landing + landing[:1], PRUSSIAN, 0.5, 0.85)
    for k in (4.5, 7.5):
        pen.line([P_(-3, k), P_(3, k)], mixp("burnt-sienna", "prussian-blue", 0.3), 0.4, 0.7)
    hull = [P_(-11, -1.6), P_(6, -1.6), P_(8.5, 0.2), P_(6, 1.8), P_(-11, 1.8), P_(-12.5, 0.2)]       # the moored boat, alongside
    pen.poly(hull, WOOD)
    pen.poly([P_(-8, -1.6), P_(3, -1.6), P_(2, -3.6), P_(-7, -3.6)], mixp("yellow-ochre", "lead-white", 0.3))
    pen.line(hull + hull[:1], PRUSSIAN, 0.5, 0.85)
    pen.line([P_(-2, 1.8), P_(-2, 3.5)], mixp("burnt-sienna", "yellow-ochre", 0.4), 0.6, 0.9)        # its mooring line
    for (a, b, w) in ((-6, 20, 11), (6, 16, 10)):                                     # the inn's roofs on the bank
        x, y = P_(a, b)
        roof_house(pen, x, y, w, 7.5)
    x, y = P_(-6, 20)
    pen.line([(x + 6.5, y), (x + 6.5, y - 9)], WOOD, 0.8, 0.95)                      # a lantern on a post at its door
    pen.s.ellipse(x + 6.5, y - 9.6, 1.4, 1.8, mixp("lead-white", "naples-yellow", 0.4), 0.95)


def stop_koriyama(pen):
    """PAINT-21F: Koriyama: the inn for lords with its gate, and the big camellia by the gate (dark round leaves, red
    flowers) that gave the inn its name."""
    cx, cy = STOPS["koriyama"][0]
    pen.poly([(cx - 9, cy + 5), (cx + 3, cy + 5), (cx + 3, cy - 1), (cx - 9, cy - 1)], WALL)            # the inn's wall
    pen.poly([(cx - 11, cy - 1), (cx + 5, cy - 1), (cx + 2, cy - 5), (cx - 8, cy - 5)], ROOF)
    pen.line([(cx - 11, cy - 1), (cx + 5, cy - 1), (cx + 2, cy - 5), (cx - 8, cy - 5), (cx - 11, cy - 1)], PRUSSIAN, 0.6, 0.85)
    gx = cx + 6                                                                      # the gate: two posts and a roofed lintel
    pen.line([(gx, cy + 5), (gx, cy - 2)], WOOD, 1.2, 0.95)
    pen.line([(gx + 6, cy + 5), (gx + 6, cy - 2)], WOOD, 1.2, 0.95)
    pen.poly([(gx - 2, cy - 2), (gx + 8, cy - 2), (gx + 6.5, cy - 4.5), (gx - 0.5, cy - 4.5)], ROOF)
    pen.line([(gx - 2, cy - 2), (gx + 8, cy - 2)], PRUSSIAN, 0.6, 0.85)
    tx, ty = cx + 14, cy - 2                                                         # the camellia: a big round dark crown, red flowers
    pen.line([(tx, cy + 5), (tx, ty + 2)], mixp("burnt-sienna", "prussian-blue", 0.4), 1.4, 0.95)
    pen.s.ellipse(tx, ty - 3, 7.0, 6.0, mixp(CEDAR, "prussian-blue", 0.25), 0.98)
    pen.s.ellipse(tx - 1.6, ty - 4.6, 4.0, 3.2, CEDAR, 0.9)
    for (fx, fy) in ((-3.5, -5), (2.5, -7), (4.5, -2), (-1, -1), (0.5, -4.5), (-5, -1.5)):
        pen.s.ellipse(tx + fx, ty + fy, 1.1, 1.1, RED, 0.98)


def stop_suma(pen):
    """PAINT-21F: Suma: the stone stupa of five stacked stones for the boy warrior (a cube, a ball, a roof, a bowl, a jewel)
    and beside it the teahouse where travellers rested and ate its soba (a little house, a flag on a pole)."""
    cx, cy = STOPS["suma"][0]
    sx, sy = cx - 6, cy + 5
    stone = mixp("lead-white", "prussian-blue", 0.28)
    stone_d = mixp("lead-white", "prussian-blue", 0.45)
    pen.poly([(sx - 3.4, sy), (sx + 3.4, sy), (sx + 3.4, sy - 4), (sx - 3.4, sy - 4)], stone)            # the cube
    pen.s.ellipse(sx, sy - 6.4, 3.0, 2.6, stone)                                     # the ball
    pen.poly([(sx - 4.4, sy - 8.6), (sx + 4.4, sy - 8.6), (sx + 1.6, sy - 11.2), (sx - 1.6, sy - 11.2)], stone_d)      # the roof
    pen.poly([(sx - 2.0, sy - 11.2), (sx + 2.0, sy - 11.2), (sx + 1.2, sy - 12.8), (sx - 1.2, sy - 12.8)], stone)      # the bowl
    pen.s.ellipse(sx, sy - 14.2, 1.1, 1.5, stone)                                    # the jewel
    pen.line([(sx - 3.4, sy), (sx - 3.4, sy - 4), (sx + 3.4, sy - 4), (sx + 3.4, sy)], PRUSSIAN, 0.5, 0.8)
    hx, hy = cx + 8, cy + 5                                                          # the soba teahouse and its flag
    pen.poly([(hx - 6, hy), (hx + 6, hy), (hx + 6, hy - 5), (hx - 6, hy - 5)], WALL)
    pen.poly([(hx - 8, hy - 5), (hx + 8, hy - 5), (hx + 5, hy - 9), (hx - 5, hy - 9)], mixp("yellow-ochre", "lead-white", 0.25))
    pen.line([(hx - 8, hy - 5), (hx + 8, hy - 5), (hx + 5, hy - 9), (hx - 5, hy - 9), (hx - 8, hy - 5)], PRUSSIAN, 0.6, 0.85)
    pen.poly([(hx - 3, hy), (hx + 1, hy), (hx + 1, hy - 3.5), (hx - 3, hy - 3.5)], ROOF)                  # its open front, a noren
    pen.line([(hx + 9, hy), (hx + 9, hy - 13)], WOOD, 0.9, 0.95)
    pen.poly([(hx + 9, hy - 13), (hx + 13.5, hy - 12), (hx + 13, hy - 8.5), (hx + 9, hy - 9)], mixp("lead-white", "naples-yellow", 0.3))
    pen.line([(hx + 10.4, hy - 12), (hx + 10.4, hy - 9.6)], PRUSSIAN, 0.5, 0.8)


def stop_maiko(pen):
    """PAINT-21F: Maiko: the shore's pines bent by the sea wind, leaning out over the white sand toward the water."""
    cx, cy = STOPS["maiko"][0]
    pen.poly([(cx - 11, cy + 5), (cx + 11, cy + 5), (cx + 9, cy + 8), (cx - 9, cy + 8)], mixp(WALL, "lead-white", 0.5), 0.95)
    trunk = mixp("burnt-sienna", "prussian-blue", 0.4)
    for (px, h, lean) in ((-7, 11, 6), (0, 13, 8), (6, 10, 5)):
        x0, y0 = cx + px, cy + 5
        mid = (x0 + lean * 0.3, y0 - h * 0.55)
        top = (x0 + lean, y0 - h)
        pen.line([(x0, y0), mid, top], trunk, 1.1, 0.95)
        for (dx, dy, rx) in ((0.0, 0.0, 3.6), (-2.4, 2.6, 2.6), (2.0, -1.2, 2.4)):
            pen.s.ellipse(top[0] + dx, top[1] + dy, rx, rx * 0.5, CEDAR, 0.95)


STOP_PAINTERS = {"hirakata": stop_hirakata, "koriyama": stop_koriyama, "suma": stop_suma, "maiko": stop_maiko}     # PAINT-21F


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


def lie_of_land():
    """PAINT-21F: what back() draws that a stop's name keeps off: the cones (Fuji, the mountains, the hollow's, Awaji's), the
    coast road, the Yodo, the coast and Awaji's shore."""
    m = np.zeros((H, W), bool)
    cones = [(FUJI[0], FUJI[1], FUJI[2], FUJI[3])] + [(mx, my, mh * 1.3, mh) for (mx, my, mh) in MOUNTAINS]
    cones += [(mx, my, mh * 1.4, mh) for (mx, my, mh) in AWAJI_CONES]
    cones += [(HILLS_C[0] + dx, HILLS_C[1] + dy - mh, mh * 1.25, mh) for (dx, dy, mh) in HILL_CONES]
    for (x, y, half, h) in cones:
        m |= mask_poly((H, W), [(x - half, y + h), (x, y), (x + half, y + h)], soft=0.0) > 0.5

    def line(pts, r):
        im = Image.new("L", (W, H), 0)
        ImageDraw.Draw(im).line([tuple(q) for q in pts], fill=255, width=1)
        return dilate(np.asarray(im) > 0, r)
    return m | line(COAST_ROAD, 2) | line(YODO, 2) | line(COAST, 1) | line(AWAJI + AWAJI[:1], 1)


STOP_NAME = max(11, LABEL["size"] - 3)     # PAINT-21F: a stop's name is written smaller than a place's: the map's size less 3, as the engine writes a stop's
STOP_ASC, STOP_DESC = int(round(STOP_NAME * 1.3)), int(round(STOP_NAME * 0.35))    # its box about the baseline (a place's, at 15: 20 above, 5 below)


def stop_names(stops, alphas, taken, land):
    """PAINT-21F: each stop's name near its picture, clear of `taken` (and, where it can be, of the lie of the land), the
    names apart: the nearest clear point to each picture (below or beside it before above), the order of placing the one
    that keeps them nearest all together. stops: {sid: (name, label_max)}. Gives {sid: [x, y]} (the baseline's middle)."""
    import itertools

    def sat(m):
        S = np.zeros((H + 1, W + 1), np.int64)
        S[1:, 1:] = m.astype(np.int64).cumsum(0).cumsum(1)
        return S

    def cands(S, box, lm):
        x0, y0, x1, y1 = box
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        LY, LX = np.mgrid[y0 - 30:y1 + 50, x0 - 70:x1 + 71]
        bx0, bx1, by0, by1 = LX - lm // 2, LX + (lm - lm // 2), LY - STOP_ASC, LY + STOP_DESC
        ok = (bx0 >= SHEET[0] + 4) & (bx1 <= SHEET[2] - 4) & (by0 >= SHEET[1] + 4) & (by1 <= SHEET[3] - 4)
        bx0, bx1 = np.clip(bx0, 0, W - 1), np.clip(bx1, 0, W - 1)
        by0, by1 = np.clip(by0, 0, H - 1), np.clip(by1, 0, H - 1)
        ok &= (S[by1 + 1, bx1 + 1] - S[by0, bx1 + 1] - S[by1 + 1, bx0] + S[by0, bx0]) == 0
        dx, dy = LX - cx, (LY - STOP_NAME * 0.4) - cy
        key = np.hypot(dx, dy * np.where(dy > 0, 1.0, 1.6))
        ok &= key < 60
        return sorted(zip(key[ok].tolist(), LX[ok].tolist(), LY[ok].tolist()))

    every, things = sat(taken | land), sat(taken)
    info = {}
    for sid, (name, lm) in stops.items():
        ys, xs = np.nonzero(alphas["stop-" + sid] > 0.5)
        box = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
        info[sid] = (lm, cands(every, box, lm) or cands(things, box, lm), box)

    def apart(a, b):
        return a[2] + 6 < b[0] or b[2] + 6 < a[0] or a[3] + 4 < b[1] or b[3] + 4 < a[1]
    best = None
    for order in itertools.permutations(info):
        placed, total = {}, 0.0
        for sid in order:
            lm, cs, box = info[sid]
            for (k, lx, ly) in cs:
                b = (lx - lm // 2, ly - STOP_ASC, lx + (lm - lm // 2), ly + STOP_DESC)
                if all(apart(b, pb) for (_, pb) in placed.values()):
                    placed[sid], total = ([int(lx), int(ly)], b), total + k
                    break
            else:
                lm, cs, box = info[sid]
                placed[sid], total = ([(box[0] + box[2]) // 2, box[3] + STOP_ASC + 2], (0, 0, 0, 0)), total + 1000     # (nowhere clear: under it)
        if best is None or total < best[0]:
            best = (total, placed)
    return {sid: best[1][sid][0] for sid in stops}


def on_via(via, p, near=1.5):
    """PAINT-21F: the index of the via point p is at, or of the one before the stretch of the line p is on (None: off the line)."""
    for i, q in enumerate(via):
        if math.hypot(q[0] - p[0], q[1] - p[1]) < 0.5:
            return i
    for i in range(len(via) - 1):
        (x1, y1), (x2, y2) = via[i], via[i + 1]
        vx, vy = x2 - x1, y2 - y1
        k = max(0.0, min(1.0, ((p[0] - x1) * vx + (p[1] - y1) * vy) / float(vx * vx + vy * vy or 1)))
        if math.hypot(x1 + vx * k - p[0], y1 + vy * k - p[1]) <= near:
            return i
    return None


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
    paths[1]["river"] = {"via_to": RIVER_LEG, "turn": list(HIRAKATA),
                         "note": "PAINT-21F: via[0..via_to] is the boat up the Yodo (Osaka to Hirakata); the rest the ferry and the road north into the hills"}
    stops = []                                                                       # PAINT-21F: the stops (MERGE-21: with a pin and a label, as places have)
    from PIL import ImageFont
    from letter import KOINE
    font = ImageFont.truetype(KOINE, STOP_NAME)
    names = {"hirakata": "Hirakata", "koriyama": "Kōriyama", "suma": "Suma", "maiko": "Maiko"}
    taken = np.zeros((H, W), bool)                                                   # what a stop's name must keep clear of
    for p in places:
        taken |= dilate(alphas[p["id"]] > 0.5, 2)
        px_, py_ = p["pin"]
        taken[max(0, py_ - 18):py_ + 19, max(0, px_ - 58):px_ + 59] = True          # its row of portraits
        lx, ly = p["label"]
        taken[max(0, ly - 24):ly + 10, max(0, int(lx - p["label_max"] / 2) - 6):int(lx + p["label_max"] / 2) + 7] = True    # its name, and a margin
    for (a_, b_) in WAYS:
        taken |= dilate(alphas["path-%s-%s" % (a_, b_)] > 0.5, 2)
    for sid in STOPS:
        taken |= dilate(alphas["stop-" + sid] > 0.5, 2)
    lms = {sid: int(math.ceil(font.getlength(names[sid]) + LABEL["spacing"] * STOP_NAME * (len(names[sid]) - 1))) + 8 for sid in STOPS}
    at_names = stop_names({sid: (names[sid], lms[sid]) for sid in STOPS}, alphas, taken, lie_of_land())
    for sid, (mid, way, at) in STOPS.items():
        via = [p for p in paths if (p["a"], p["b"]) == way][0]["via"]
        idx = on_via(via, at)                                                        # the via point it is at, or the one before it on the line
        assert idx is not None, f"the stop {sid}: its pin {at} is not on its way's line"
        m = alphas["stop-" + sid] > 0.5
        if sid != "hirakata":                                                        # the walk's: the row of portraits at the pin leaves the picture clear
            rx0, ry0, rx1, ry1 = int(at[0] - ROW[0] / 2) - 2, int(at[1] - ROW[1] / 2) - 2, int(at[0] + ROW[0] / 2) + 3, int(at[1] + ROW[1] / 2) + 3
            assert not m[max(0, ry0):ry1, max(0, rx0):rx1].any(), f"the stop {sid}: the portraits at its pin would stand on its picture"
        stops.append({"id": sid, "picture": f"stop-{sid}.png", "way": list(way), "pin": list(at), "label": at_names[sid], "label_max": lms[sid],
                      "at": list(at), "via_index": idx, "shape": shape_of(dilate(m, 3)), "middle": list(mid)})
    return {
        "map": "edo", "size": [800, 600], "sheet": SHEET,
        "material": ("A travel map printed from woodblocks on a long sheet of soft paper, folded in six panels and worn at the folds: the "
                     "coast road from Suruga to Harima, the land soft green with its mountains as cones, the sea in rows of blue waves, Fuji "
                     "white at the east end, the places as small pictures with their names."),
        "label": LABEL,
        "places": places, "paths": paths, "stops": stops,
        "note": ("East at the right. yui on the west shore of Suruga Bay under the Satta headland, Fuji across the water (drawn on the sheet: the "
                 "lie of the land); osaka at its river mouth west of the Kii peninsula's bulge (PAINT-21F: a place now; its castle has walls and "
                 "turrets and no keep); hills north of Osaka (the hollow in the wooded hills: cedars and the storehouse); akashi on the shore "
                 "above its strait, Awaji across it (PAINT-21F); himeji at the west end on its hill above the town, the Inland Sea below; shosha "
                 "north-west of Himeji, a wooded mountain with the women's hall at its foot (PAINT-21F). The sea way goes out from Yui's shore "
                 "round the Kii tip into Osaka's bay (a ship drawn on it); the river path goes up the Yodo to Hirakata (the Kyoto boat drawn on "
                 "it), across by the ferry at Hirakata and north into the hills (`river`: where the water ends; the stop `hirakata` there); "
                 "the road west comes down by Koriyama, round to Nishinomiya and along the shore by Suma and Maiko to Akashi (`stops`: each a "
                 "picture with its `pin`, the point of its way's line it is for, where the portraits stop: for the walk's three, where their row "
                 "stands just above the picture, the line said above them; Hirakata's at the river's turn; and a `label`, its name's "
                 "baseline middle, for a name written at the map's size less 3, as the engine writes a stop's); the road on to Himeji; "
                 "the walk between Himeji and Shosha. Each via is a pin, the way's drawn points, the other pin. "
                 "The pins (rows of three portraits, 116 x 36) stand beside each place (Osaka's on the sea east of it)."),
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
        alphas[f"path-{a_}-{b_}"] = a                                                 # (PAINT-21F: the stops' names keep clear of the ways)
    for sid, fn in STOP_PAINTERS.items():                                            # PAINT-21F: the three road pictures
        pen = Pen()
        fn(pen)
        c, a = pen.done()
        files[f"stop-{sid}"] = (over(pic.copy(), c, a), a)
        alphas["stop-" + sid] = a
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

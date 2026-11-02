"""PAINT-21C: Osaka, the Dojima shore, about 21 April 1830, afternoon (edo-dojima). In the act's woodblock manner
(S/work-20-paintA/style.md): flat masses, a graded sky in a warm haze, one fine contour in prussian blue, few paints.

LIGHT   The sun low in the west-south-west, to our right (about 4 o'clock, 28 degrees up): faces turned to the right are
        in full warm light, the fronts that face us (north) in a luminous blue shade, the ground warm; shadows fall to
        the left and a little toward us, long.
DEPTH   horizon 262, full 590 (room.View turned 12 degrees to the left: we look south-south-east across the river, and
        upstream is to the left).
TONES   light: the sky low down in the haze, the sunlit side of the rice dealer's house, the warehouses' white across the
        water, the street. middle: the river (brown-green with the sky in it), the roofs' grey-blue, the crowd. dark: the
        house front in shade, the noren, the timber, the contour. The eye comes in at the stall (left), crosses to the
        steps, and goes up the river to the castle's walls far off.
PLACE   (edo_dojima_kit.py's City; world in cm: X to the right (west), Z toward us (north), Y up.) The shore street runs
        across the bottom of the picture; on its river side at the left stands O-Natsu's house (a rice dealer's: its
        front to the street, its back on the water), her alms stall before it; a lower neighbour beyond it; in the middle
        the stone steps down to the water at a gap in the bank; at the right the rice market spills into the road (the
        dealers, the water men); beyond the bank the river, lighters on it; across it the domains' white warehouses and
        their gates on the island (Nakanoshima); a timber bridge, high, crossing at the right; and up the river to the
        left, far off, the castle's walls and corner turrets, with no keep (composed: from where we stand it lies further
        to the left than the picture's edge; a print would bring it in, and so does this).

  python3 edo_dojima.py fast     the composition without the brush pass (out/edo-dojima-1-under.png, -2-all.png)
  python3 edo_dojima.py          the full passes: out/edo-dojima/ (back.png, the cut-outs, the frames, layout.json)
"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
from edo_dojima_kit import *

SEED = 1830
OUT = "out/edo-dojima"
HZ, FULL = 262, 590
CAM = City(HZ, FULL, (0.0, 0.0), -12.0, sun=(0.853, 0.469, -0.229))          # the sun: west-south-west, 28 degrees up

# ---------------------------------------------------------------- where things are (cm)
LIP_Z = -1550.0                       # the near bank's stone lip (the street's river edge, where it is open)
WATER_Y = -180.0                      # the river 1.8 m below the street
FAR_Z = -5550.0                       # the far bank's lip (the island), 40 m across
HOUSE = dict(X0=-880.0, X1=-380.0, Zf=-1450.0, Zb=-2250.0, eave=262.0, upper=470.0, ridge=640.0)   # O-Natsu's house: front to the street, back on the water
NEIGH = dict(X0=-1700.0, X1=-890.0, Zf=-1500.0, Zb=-2200.0, eave=245.0, upper=410.0, ridge=560.0)  # the neighbour beyond it (east), lower, its shop shut
DOOR = (-750.0, -610.0)                                                 # her doorway (the noren hangs in it)
BALES = (-872.0, -765.0)                                                # the rice bales stacked against her front, left of the door
STEPS = dict(X0=-260.0, X1=-60.0, n=7)                                  # the gap in the lip and the steps down
STALL = dict(X0=-700.0, X1=-420.0, Zf=-1230.0, Zb=-1290.0, h=78.0)     # O-Natsu's alms stall, before her house
BRIDGE = dict(X0=640.0, X1=1060.0, rise=330.0)                          # the bridge: its two rails, and how high the deck rises at mid-river
TIP_X = 40.0                                                             # where the island's bank ends at the left (beyond it, up the river)
MARKET = dict(X0=40.0, X1=520.0, Z0=-1600.0, Z1=-1380.0)               # the dealers in the road at the right


def g(X, Z, Y=0.0):
    return CAM.pt(X, Y, Z)


# ================================================================ pass 1: broad and flat
def paint_sky(seed):
    """The graded band (style.md section 3) in Osaka's haze: eight bands, the deep blue at the top paler than Suruga's,
    the lowest ones the warm paper."""
    rows = [0, 40, 84, 126, 164, 196, 222, 244, HZ + 40]
    cols = [mixp(COBALT, PRUSSIAN, 0.22), mixp(COBALT, ULTRA, 0.15), COBALT, mixp(COBALT, CERULEAN, 0.5), CERULEAN,
            tintw(CERULEAN, 0.45), lerp(tintw(CERULEAN, 0.7), NAPLES, 0.12), PAPER, PAPER]
    pic = bands(SHAPE, rows, cols, soft=6.0, wobble=2.5, seed=seed, patch=0.02)
    x, y = grid(SHAPE)
    # the sun's side (right) is warmer in the haze, a whisper
    glow(pic, tintw(NAPLES, 0.3), (np.clip((x - 300) / 500.0, 0, 1) * np.clip(1 - np.abs(y - 236) / 60.0, 0, 1) * 0.14).astype(F32))
    # two lens clouds, flat, a prussian edge on top only (style.md: two or three at most)
    s = Paper(SHAPE)
    for (cx, cy, w, h) in ((190, 70, 230, 12), (600, 118, 170, 9)):
        top = [(cx - w / 2 + w * i / 12, cy - h * (1 - ((i - 6) / 6.3) ** 2) * (0.75 + 0.25 * math.sin(i * 1.7 + cx))) for i in range(13)]
        s.poly(top + [(cx + w / 2, cy + 1), (cx - w / 2, cy + 1)], lerp(WHITE, NAPLES, 0.12), 0.95)
        s.line(top, PRUSSIAN, 0.8, 0.4)
    s.onto(pic)
    return pic


CASTLE = dict(x0=432.0, x1=578.0, base=263.0)


def castle(sheet):
    """Far off up the river: the castle on its rise, a long low line of tall battered stone walls with white walls along
    their tops and three corner turrets of three storeys each (the lower two of a width, the top one smaller, each under
    its own wide grey roof), and NO keep (it burned in 1665: walls and turrets only). Far plane: no contour, two flats
    each, pale and blue in the haze (style.md section 7). Drawn a little larger than the eye would see it, as the prints
    draw a far landmark."""
    far = lambda c, t=0.55: lerp(lerp(c, PAPER, t), CERULEAN, 0.10)
    x0, x1, base = CASTLE["x0"], CASTLE["x1"], CASTLE["base"]
    top = base - 20.0                                        # the top of the stone walls
    sheet.poly([(x0 - 30, base + 2), (x0 - 10, base - 5), (x1 + 12, base - 6), (x1 + 34, base + 2)], far(VIRIDIAN, 0.66))      # the rise
    # the stone walls: tall, battered (their faces curving in toward the top), in shade toward us; their lit returns
    face = [(x0, base - 3)] + [(x0 + 7 * (1 - (1 - t) ** 2), base - 3 - (base - 3 - top) * t) for t in np.linspace(0.1, 1, 6)] + \
           [(x1 - 6 * (1 - (1 - t) ** 2), base - 3 - (base - 3 - top) * t) for t in np.linspace(1, 0.1, 6)] + [(x1, base - 3)]
    sheet.poly(face, far(STONE_SH, 0.28))
    for (a, b) in ((x0 + 52, x0 + 60), (x1 - 6, x1)):
        sheet.poly([(a, base - 3), (a + 4, top), (b, top), (b, base - 3)], far(STONE_LIT, 0.38))
    for t in (0.35, 0.65):                                   # the courses, a breath
        yy = base - 3 - (base - 3 - top) * t
        sheet.line([(x0 + 4, yy), (x1 - 4, yy)], far(STONE_SH, 0.25), 0.6, 0.5)
    # the white walls along the top, with their grey coping
    sheet.poly([(x0 + 7, top), (x1 - 6, top), (x1 - 6, top - 4.0), (x0 + 7, top - 4.0)], lerp(PLASTER_SH, PAPER, 0.10))
    sheet.line([(x0 + 6, top - 4.6), (x1 - 5, top - 4.6)], far(TILE_SH, 0.15), 1.3)
    # three corner turrets, three storeys each: the faces toward us in the scene's shade (a pale blue, as everything that
    # faces us here), a narrow lit return on the right in the low sun, a row of dark windows, a wide grey roof each
    for (tx, sc) in ((x0 + 16, 1.0), (x0 + 84, 0.86), (x1 - 15, 0.95)):
        yb = top - 3.5
        for (ww, hh, rw) in ((15, 7.0, 21), (14, 6.5, 19), (10, 6.0, 14)):
            ww, hh, rw = ww * sc, hh * sc, rw * sc
            ret = ww * 0.32
            sheet.poly([(tx - ww / 2, yb), (tx + ww / 2, yb), (tx + ww / 2, yb - hh), (tx - ww / 2, yb - hh)], lerp(PLASTER_SH, PAPER, 0.12))
            sheet.poly([(tx + ww / 2, yb), (tx + ww / 2 + ret, yb - 1.2), (tx + ww / 2 + ret, yb - hh - 1.2), (tx + ww / 2, yb - hh)], lerp(PLASTER_LIT, NAPLES, 0.2))
            sheet.line([(tx - ww / 2 + 2, yb - hh * 0.52), (tx + ww / 2 - 2, yb - hh * 0.52)], lerp(TILE_DEEP, PAPER, 0.25), 1.1, 0.85)     # a row of windows
            yr = yb - hh
            sheet.poly([(tx - rw / 2, yr + 0.8), (tx + rw / 2 + ret, yr - 0.4), (tx + ww / 2 + ret * 0.5 - 1, yr - 2.4 * sc), (tx - ww / 2 + 1, yr - 2.4 * sc)], lerp(TILE_SH, PAPER, 0.18))
            yb = yr - 2.4 * sc
        sheet.poly([(tx - 4 * sc, yb + 0.5), (tx + 5 * sc, yb + 0.5), (tx + 2 * sc, yb - 2.8 * sc), (tx - 1.5 * sc, yb - 2.8 * sc)], lerp(TILE_SH, PAPER, 0.18))
    # woods on the rise beside it
    for (cx, cy, rx, ry) in ((x0 - 16, base - 7, 13, 6), (x1 + 18, base - 8, 12, 6), (x1 + 34, base - 3, 10, 4)):
        sheet.ellipse(cx, cy, rx, ry, far(VIRIDIAN, 0.58))


def paint_far(pic, seed):
    """Up the river to the left (the window between the house and the island): the reach of water going away, the low
    far banks with roofs and trees, and the castle on its rise; all far, no contour, paled toward the haze."""
    s = Paper(SHAPE)
    castle(s)
    s.onto(pic)


def reach_banks(pic):
    """The low far banks of the reach upstream, in front of the castle's rise: roofs and trees, grey-green, the nearer
    darker; and the water's far end under them, the paper."""
    s = Paper(SHAPE)
    for (x0, x1, y0, h, tone) in ((330, 640, 269, 5, 0.60), (380, 700, 279, 6, 0.46)):
        pts = [(x0 + (x1 - x0) * i / 16, y0 - h * (0.55 + 0.45 * abs(math.sin(i * 2.3 + x0)))) for i in range(17)] + [(x1, y0 + 2), (x0, y0 + 2)]
        s.poly(pts, lerp(lerp(TILE_SH, VIRIDIAN, 0.35), PAPER, tone))
    s.onto(pic)


# ---------------------------------------------------------------- the river
def river_region():
    """Where the river's surface could be seen: from the far bank's foot down to the near lip, across the picture."""
    far_pts = [g(X, FAR_Z, WATER_Y) for X in np.linspace(TIP_X, 6000, 12)]
    near_pts = [g(X, LIP_Z) for X in np.linspace(6000, -4000, 14)]
    reach = [(near_pts[-1][0], 278.0), (far_pts[0][0], 278.0)]                  # beyond the island's tip: the reach upstream
    return mask_poly(SHAPE, reach + far_pts + near_pts, soft=0.6, seed=4)


def paint_river(pic, seed):
    """The river in bands (style.md section 3, big water): far, the haze's paper with the sky's blue in it; nearer,
    brown-green (viridian and ochre, a little sienna) with cerulean where the sky lies on it; the near water deepest.
    The light on it moves (the engine's shimmer); the lighters are the engine's flyers."""
    x, y = grid(SHAPE)
    wm = river_region()
    # level bands (the print's way with big water): the far reach the haze's paper with the sky's blue in it; then
    # cerulean with green in it; then the river's own brown-green (viridian, ochre, a little sienna), deepest near
    rows = [262, 296, 318, 340, 364, 390, 420, 470]
    olive = lerp(lerp(VIRIDIAN, OCHRE, 0.38), SIENNA, 0.12)            # the river's own brown-green
    near_c = lerp(lerp(olive, COBALT, 0.22), PRUSSIAN, 0.18)           # near, deepest, with the sky's blue in it
    cols = [lerp(tintw(CERULEAN, 0.66), NAPLES, 0.10), lerp(tintw(CERULEAN, 0.50), NAPLES, 0.06), tintw(lerp(CERULEAN, VIRIDIAN, 0.15), 0.34),
            tintw(lerp(lerp(CERULEAN, olive, 0.35), COBALT, 0.10), 0.22), tintw(lerp(lerp(olive, CERULEAN, 0.45), COBALT, 0.12), 0.10),
            lerp(lerp(olive, CERULEAN, 0.30), COBALT, 0.14), near_c, near_c]
    field = bands(SHAPE, rows, cols, soft=2.5, wobble=0.0, seed=seed + 20, patch=0.015)
    over(pic, field, wm)
    # the far bank's shade lying on the water under it: a darker band, flat
    sh_pts = [g(X, FAR_Z, WATER_Y) for X in np.linspace(TIP_X, 5000, 10)] + [g(X, FAR_Z + 600, WATER_Y) for X in np.linspace(5000, TIP_X, 10)]
    over(pic, lerp(cols[3], PRUSSIAN, 0.20), (mask_poly(SHAPE, sh_pts, soft=1.0, seed=5) * wm * 0.6).astype(F32))
    # long flat streaks of the sky lying on the water, and short ripple marks: still pattern (the moving light is the
    # engine's shimmer), closer together far off
    rng = np.random.default_rng(seed + 21)
    s = Paper(SHAPE)
    # the white warehouses across, lying on the water under them as pale broken shapes (the print's reflection)
    for (xa, xb) in ((612, 660), (676, 706), (720, 770)):
        for j in range(5):
            yy = 340 + j * 7 + rng.uniform(-1, 1)
            w_ = (xb - xa) * (1 - j * 0.12)
            s.line([(xa + (xb - xa - w_) / 2 + rng.uniform(-3, 3), yy), (xa + (xb - xa + w_) / 2, yy)], tintw(CERULEAN, 0.62), 2.2 - j * 0.25, 0.45 - j * 0.06)
    for i in range(170):
        yy = 300 + (rng.random() ** 1.5) * 150
        xx = rng.uniform(-40, 840)
        L = rng.uniform(8, 50) * (0.35 + (yy - 300) / 150)
        tone = lerp(PAPER, CERULEAN, 0.22) if yy < 372 else tintw(CERULEAN, 0.42)
        s.line([(xx - L / 2, yy), (xx + L / 2, yy)], tone, 0.8 if yy < 360 else 1.2, 0.5 if yy < 372 else 0.40)
    c, a = s.done()
    over(pic, c, (a * wm).astype(F32))
    return wm


def paint_far_bank(pic, seed, wm):
    """The island across the river (Nakanoshima): a stone embankment in courses from the water up to its top, and on it
    the domains' warehouses: a long gatehouse along the bank with its great gate (dark doors under a tiled roof), and
    behind it the white storehouses, roof on roof. Middle distance: contour 0.6 px, flats and their shade only."""
    s = Paper(SHAPE)
    lines = s
    rng = np.random.default_rng(seed + 30)
    X_end = 5200.0
    # the embankment: its face (it faces us: north, in shade), from the water to the top
    face = [g(X, FAR_Z, WATER_Y) for X in (TIP_X, X_end)] + [g(X, FAR_Z, 0) for X in (X_end, TIP_X)]
    s.poly(face, lerp(STONE_SH, PAPER, 0.25))
    # its end at the island's tip turns away (the left face, in shade too) and the bank's top
    s.poly([g(TIP_X, FAR_Z, WATER_Y), g(TIP_X, FAR_Z, 0), g(TIP_X - 60, FAR_Z - 900, 0), g(TIP_X - 60, FAR_Z - 900, WATER_Y)], lerp(STONE_SH, PAPER, 0.35))
    for k in range(1, 4):                                   # courses
        yv = WATER_Y * k / 4
        lines.line([g(TIP_X, FAR_Z, yv), g(X_end, FAR_Z, yv)], PRUSSIAN, 0.5, 0.28)
    # a water gate: steps down at a gap in the far bank (where the domain's lighters land)
    wg = (520.0, 760.0)
    s.poly([g(wg[0], FAR_Z, WATER_Y), g(wg[1], FAR_Z, WATER_Y), g(wg[1], FAR_Z, 0), g(wg[0], FAR_Z, 0)], lerp(STONE_LIT, PAPER, 0.25))
    for k in range(5):
        yv = WATER_Y * (k + 0.5) / 5
        lines.line([g(wg[0], FAR_Z, yv), g(wg[1], FAR_Z, yv)], PRUSSIAN, 0.5, 0.25)
    # the gatehouse (nagaya-mon): a long two-storey building on the bank, white upper wall, dark boards below, a tiled
    # roof; the gate in it: two great dark doors under a lifted roof
    Zg0, Zg1 = FAR_Z - 150.0, FAR_Z - 750.0
    gate_x = (300.0, 1200.0, 2900.0, 4300.0)
    house_ = (TIP_X + 60, X_end)
    hb, hu, hr = 380.0, 520.0, 700.0
    front = [g(X, Zg0, 0) for X in house_] + [g(X, Zg0, hb) for X in house_[::-1]]
    s.poly([g(house_[0], Zg0, 0), g(house_[1], Zg0, 0), g(house_[1], Zg0, 160), g(house_[0], Zg0, 160)], lerp(WOOD_SH, PAPER, 0.3))     # the boards, in shade
    s.poly([g(house_[0], Zg0, 160), g(house_[1], Zg0, 160), g(house_[1], Zg0, hb), g(house_[0], Zg0, hb)], lerp(PLASTER_SH, PAPER, 0.25))
    # barred windows along the white wall
    for X in np.arange(house_[0] + 160, house_[1] - 100, 260):
        if any(abs(X - gx) < 260 for gx in gate_x):
            continue
        a, b = g(X, Zg0, 210), g(X + 90, Zg0, 280)
        s.poly([a, (b[0], a[1]), b, (a[0], b[1])], lerp(WOOD_DARK, PAPER, 0.2))
    # the gatehouse roof: one slope toward us (lit by the side light? it faces north and up: the up part takes the sun)
    roof_slope(s, CAM, lines, (house_[0] - 40, hb, Zg0 + 70), (house_[1] + 40, hb, Zg0 + 70), (house_[0] + 60, hu, Zg1 + 200), (house_[1], hu, Zg1 + 200),
               lit_c=lerp(TILE_LIT, PAPER, 0.25), shade_c=lerp(TILE_SH, PAPER, 0.25))
    # the gates
    for gx in gate_x:
        a0, a1 = gx - 180, gx + 180
        s.poly([g(a0, Zg0 + 5, 0), g(a1, Zg0 + 5, 0), g(a1, Zg0 + 5, 330), g(a0, Zg0 + 5, 330)], lerp(WOOD_DARK, PAPER, 0.12))
        lines.line([g(gx, Zg0 + 5, 0), g(gx, Zg0 + 5, 330)], lerp(WOOD_LIT, PAPER, 0.3), 0.6, 0.6)
        for yv in (90, 200, 300):
            lines.line([g(a0, Zg0 + 5, yv), g(a1, Zg0 + 5, yv)], lerp(STONE_SH, PAPER, 0.2), 0.5, 0.5)
        roof_slope(s, CAM, lines, (a0 - 90, 420, Zg0 + 120), (a1 + 90, 420, Zg0 + 120), (a0 - 20, 560, Zg0 - 250), (a1 + 20, 560, Zg0 - 250),
                   lit_c=lerp(TILE_LIT, PAPER, 0.18), shade_c=lerp(TILE_SH, PAPER, 0.18))
    lines.line(front + [front[0]], PRUSSIAN, 0.6, 0.45)
    # the storehouses behind: white gable ends and long roofs, roof on roof, getting paler with distance
    kura = []
    for row, (Zr, hr_) in enumerate(((Zg1 - 150, (760, 900)), (Zg1 - 1300, (820, 980)), (Zg1 - 2600, (860, 1050)), (Zg1 - 4200, (900, 1100)))):
        X = TIP_X + 80 + rng.uniform(0, 250) - row * 260
        while X < 2600 + row * 900:
            w = rng.uniform(480, 820)
            kura.append((X, X + w, Zr - rng.uniform(0, 500), rng.uniform(*hr_)))
            X += w + rng.uniform(60, 260)
    kura.sort(key=lambda k: k[2])                           # the farthest first
    for (x0, x1, Zf, h) in kura:
        if Zf < FAR_Z - 2000 and x0 < TIP_X + 300:          # (the island narrows to its tip: nothing far back there)
            continue
        pale = 0.16 + 0.30 * np.clip((-Zf - 6500) / 4000.0, 0, 1)
        depth = 900.0
        # the long side toward us (north: shade), the west gable end (lit), the roof's near slope
        s.poly([g(x0, Zf, 0), g(x1, Zf, 0), g(x1, Zf, h * 0.72), g(x0, Zf, h * 0.72)], lerp(PLASTER_SH, PAPER, pale))
        s.poly([g(x1, Zf, 0), g(x1, Zf - depth, 0), g(x1, Zf - depth, h * 0.72), g(x1, Zf - depth / 2, h), g(x1, Zf, h * 0.72)], lerp(PLASTER_LIT, PAPER, pale * 0.6))
        # the dark wainscot at the foot (tiles set in plaster), a small window with its heavy shutter
        s.poly([g(x0, Zf, 0), g(x1, Zf, 0), g(x1, Zf, 120), g(x0, Zf, 120)], lerp(lerp(TILE_SH, PAPER, 0.25), PLASTER_SH, 0.3))
        wx = (x0 + x1) / 2
        s.poly([g(wx - 50, Zf, h * 0.45), g(wx + 50, Zf, h * 0.45), g(wx + 50, Zf, h * 0.58), g(wx - 50, Zf, h * 0.58)], lerp(WOOD_DARK, PAPER, pale + 0.1))
        roof_slope(s, CAM, lines, (x0 - 40, h * 0.72, Zf + 50), (x1 + 40, h * 0.72, Zf + 50), (x0 - 40, h, Zf - depth / 2), (x1 + 40, h, Zf - depth / 2),
                   lit_c=lerp(TILE_LIT, PAPER, pale), shade_c=lerp(TILE_SH, PAPER, pale))
        lines.line([g(x1, Zf, 0), g(x1, Zf, h * 0.72), g(x1, Zf - depth / 2, h)], PRUSSIAN, 0.55, 0.4)
    c, a = s.done()
    over(pic, c, a)


def paint_ground(pic, seed):
    """The shore street: packed earth, warm in the sun, a little paler far off; worn paler where feet go."""
    x, y = grid(SHAPE)
    X, Z, m = CAM.floor()
    ground = (m > 0.5) & (Z > LIP_Z)
    ground = ground.astype(F32)
    earth = flat(EARTH, SHAPE, seed + 40, 0.05, 40)
    t = np.clip((y - HZ) / (H - HZ), 0, 1)
    earth = lerp(earth, PAPER, ((1 - t) ** 1.8 * 0.35)[..., None])
    over(pic, earth, ground)
    # where feet go: along the line before the stall, to the steps, through the market
    walkers = mask_line(SHAPE, [g(-760, -1100), g(-400, -1000), g(-150, -1400)], [40, 50, 30], soft=4.0)
    walkers = np.maximum(walkers, mask_line(SHAPE, [g(-1300, -900), g(-200, -1200), g(600, -1250)], [50, 40, 34], soft=5.0))
    over(pic, lerp(EARTH, PAPER, 0.28), (walkers * ground * 0.35).astype(F32))
    return ground


def paint_lip(pic, seed):
    """The near bank: a broad stone lip along the street's river edge (its coping, lit on top), with the gap where the
    steps go down (the steps themselves, cut into the bank, seen from above: treads catching the light, risers in
    shade), and the mooring posts on each side."""
    s = Paper(SHAPE)
    lines = s
    W_ = 60.0                                              # the coping's width
    x0, x1 = HOUSE["X1"], 4000.0
    # the coping, either side of the steps' gap, and its edge face (the bank's top course, facing the river: unseen)
    for (a, b) in ((x0, STEPS["X0"]), (STEPS["X1"], x1)):
        s.poly([g(a, LIP_Z + W_), g(b, LIP_Z + W_), g(b, LIP_Z), g(a, LIP_Z)], STONE_LIT)
        lines.line([g(a, LIP_Z + W_), g(b, LIP_Z + W_)], PRUSSIAN, 0.7, 0.45)
        for X in np.arange(a + 90, b, 120):
            lines.line([g(X, LIP_Z + W_), g(X, LIP_Z)], PRUSSIAN, 0.5, 0.3)
    # the steps: a flight going down to the water inside the gap, each tread a lit strip and each riser in shade. From
    # a street's height a flight going away and down hides its own treads; it is drawn as the prints draw it, as if
    # seen from a little higher (the drop pressed together), so that it reads as steps going down to the water.
    n = STEPS["n"]
    gs = lambda X, Z, Y=0.0: g(X, Z, Y * 0.12)
    for i in range(n):
        Za, Zb = LIP_Z + W_ - 62 * i, LIP_Z + W_ - 62 * (i + 1)
        Ya = -24.0 * i
        tread = [gs(STEPS["X0"], Za, Ya), gs(STEPS["X1"], Za, Ya), gs(STEPS["X1"], Zb, Ya), gs(STEPS["X0"], Zb, Ya)]
        s.poly(tread, lerp(STONE_LIT, PAPER, 0.05 * i))
        riser = [gs(STEPS["X0"], Zb, Ya), gs(STEPS["X1"], Zb, Ya), gs(STEPS["X1"], Zb, Ya - 24), gs(STEPS["X0"], Zb, Ya - 24)]
        s.poly(riser, lerp(STONE_SH, PRUSSIAN, 0.15))
        lines.line([tread[0], tread[1]], PRUSSIAN, 0.6, 0.45)
    foot_Z = LIP_Z + W_ - 62 * n
    # the gap's two side walls going down with the steps: the west one's inner face looks east (shade), the east one's
    # top course; the water at the foot
    for (X, c) in ((STEPS["X1"], STONE_SH), (STEPS["X0"], STONE_LIT)):
        s.poly([gs(X, LIP_Z + W_, 0), gs(X, foot_Z, -24 * n), gs(X + 14, foot_Z, -24 * n), gs(X + 14, LIP_Z + W_, 0)], c)
        lines.line([gs(X, LIP_Z + W_, 0), gs(X, foot_Z, -24 * n)], PRUSSIAN, 0.7, 0.5)
    info_steps = [gs(STEPS["X0"], LIP_Z + W_), gs(STEPS["X1"] + 14, LIP_Z + W_), gs(STEPS["X1"] + 14, foot_Z, -24 * n), gs(STEPS["X0"], foot_Z, -24 * n)]
    # mooring posts, one each side of the steps, and two more along the bank
    for X in (STEPS["X0"] - 30, STEPS["X1"] + 30, 900.0, -560.0):
        Zp = LIP_Z + 25
        k = CAM.k(X, Zp)
        p0, p1 = g(X, Zp), g(X, Zp, 70)
        s.line([p0, p1], STONE_LIT if X > -400 else STONE_SH, max(1.5, 22 * k))
        s.ellipse(p1[0], p1[1], 11 * k, 4 * k, STONE_LIT)
        lines.line([(p0[0] - 11 * k, p0[1]), (p1[0] - 11 * k, p1[1])], PRUSSIAN, 0.6, 0.5)
    c, a = s.done()
    over(pic, c, a)
    return info_steps


def cast_shadows(pic, ground, seed):
    """Every standing thing's shadow on the street, flat and blue, laid along the sun (to the left, a little toward us)."""
    sh = Paper(SHAPE)
    SH = lerp(EARTH, COBALT, 0.42)
    H_ = HOUSE
    # the house: the shadow of its west wall and eave falls to the left over its own front: nothing on the street but a
    # wedge off its front corner
    pts = [(H_["X1"], 0, H_["Zf"]), (H_["X1"], H_["eave"] + 40, H_["Zf"]), (H_["X1"], H_["ridge"], H_["Zf"] - 300)]
    sh.poly([g(H_["X1"], H_["Zf"])] + CAM.shadow_poly(pts[1:]) + [g(H_["X0"], H_["Zf"])], SH, 0.9)
    # the mooring posts, the stall (its own cut-out lays its shadow here in the backdrop too)
    for X in (STEPS["X0"] - 30, STEPS["X1"] + 30, 900.0, -560.0):
        Zp = LIP_Z + 25
        sh.poly([g(X - 10, Zp)] + CAM.shadow_poly([(X - 10, 70, Zp), (X + 10, 70, Zp)]) + [g(X + 10, Zp)], SH, 0.85)
    import edo_dojima_things as T
    for (X, Z, cm, *_r) in T.MARKET_FIGS + T.WATERMEN:
        sh.poly([g(X - 14, Z)] + CAM.shadow_poly([(X - 14, cm * 0.85, Z), (X + 14, cm * 0.85, Z)]) + [g(X + 14, Z)], SH, 0.75)
    S = STALL
    sh.poly([g(S["X1"], S["Zf"]), g(S["X1"], S["Zb"])] + CAM.shadow_poly([(S["X1"], S["h"], S["Zb"]), (S["X1"], S["h"], S["Zf"]), (S["X0"], S["h"], S["Zf"])]) + [g(S["X0"], S["Zf"])], SH, 0.9)
    sh.poly([g(-808, -1235), g(-738, -1235)] + CAM.shadow_poly([(-738, 18, -1235), (-808, 18, -1235)]), SH, 0.8)      # the sandals' heap
    c, a = sh.done()
    over(pic, c, (a * ground).astype(F32))
    return a


def under(seed=SEED):
    info = {}
    pic = paint_sky(seed)
    paint_far(pic, seed)
    info["water"] = paint_river(pic, seed)
    reach_banks(pic)
    paint_far_bank(pic, seed, info["water"])
    info["ground"] = paint_ground(pic, seed)
    info["steps"] = paint_lip(pic, seed)
    info["shadow"] = cast_shadows(pic, info["ground"], seed)
    return np.clip(pic, 0, 1), info


# ================================================================ pass 3: the crisp things (the backdrop's)
def bridge(sheet, lines):
    """The timber bridge crossing the river at the right: a high arched deck on rows of timber piers, a rail each side;
    its west side (toward the sun) lit. People on it far off are dabs."""
    B = BRIDGE
    zs = np.linspace(LIP_Z + 60, FAR_Z - 60, 40)
    span = (LIP_Z - FAR_Z)
    def deck_y(Z):
        u = (LIP_Z - Z) / span
        return B["rise"] * math.sin(math.pi * min(max(u, 0), 1)) ** 0.8 + 10
    lit_side = [(B["X1"], deck_y(Z), Z) for Z in zs]
    # the piers: rows of posts down to the water (dark, the far ones paler)
    for Z in np.linspace(LIP_Z - 400, FAR_Z + 400, 9):
        for X in (B["X0"] + 40, (B["X0"] + B["X1"]) / 2, B["X1"] - 40):
            a, b = g(X, Z, WATER_Y), g(X, Z, deck_y(Z) - 30)
            sheet.line([a, b], lerp(WOOD_SH, PAPER, np.clip((-Z - 3000) / 5000.0, 0, 0.4)), max(1.0, 26 * CAM.k(X, Z)))
        a, b = g(B["X0"] + 40, Z, deck_y(Z) * 0.45), g(B["X1"] - 40, Z, deck_y(Z) * 0.45)
        sheet.line([a, b], WOOD_SH, max(0.8, 14 * CAM.k(B["X1"], Z)))
    # the deck's west face (the beam along its side, lit) and its top (the planks, seen from below the eye: only near)
    side = [g(X, Z, Y) for (X, Y, Z) in lit_side] + [g(X, Z, Y - 45) for (X, Y, Z) in lit_side[::-1]]
    sheet.poly(side, WOOD_LIT)
    top = [g(B["X1"], Z, deck_y(Z)) for Z in zs] + [g(B["X0"], Z, deck_y(Z)) for Z in zs[::-1]]
    sheet.poly(top, lerp(WOOD, PAPER, 0.15))
    # the rails: posts and a top rail each side
    for X, col in ((B["X0"], WOOD_SH), (B["X1"], WOOD_LIT)):
        rail = [g(X, Z, deck_y(Z) + 95) for Z in zs]
        sheet.line(rail, col, max(0.8, 10 * CAM.k(X, LIP_Z - 600)), 1.0)
        for Z in zs[::3]:
            sheet.line([g(X, Z, deck_y(Z)), g(X, Z, deck_y(Z) + 95)], col, max(0.7, 9 * CAM.k(X, Z)))
    lines.line([g(B["X1"], Z, Y) for (X, Y, Z) in lit_side], SIENNA, 0.9, 0.6)
    lines.line([g(B["X1"], Z, deck_y(Z) - 45) for Z in zs], PRUSSIAN, 0.8, 0.55)
    # people crossing it, far off: a few dabs on the deck
    rng = np.random.default_rng(77)
    for u in (0.32, 0.41, 0.55, 0.63, 0.78):
        Z = LIP_Z - span * u
        X = rng.uniform(B["X0"] + 80, B["X1"] - 80)
        p = g(X, Z, deck_y(Z))
        hh = 156 * CAM.k(X, Z)
        robe = [INDIGO, lerp(SIENNA, OCHRE, 0.35), lerp(tintw(PRUSSIAN, 0.5), OCHRE, 0.25), tintw(INDIGO, 0.3), lerp(VIRIDIAN, PRUSSIAN, 0.2)][int(u * 37) % 5]
        figure(sheet, p[0], p[1], hh, rng, robe=robe, line=False, hat="sedge" if int(u * 100) % 3 == 0 else None)
    return top + side


def house(sheet, lines, Hs, door_at, kind="shop", rng=None):
    """A rice dealer's house on the river side of the street, its front to the street (facing us: in shade) and its
    west side in the sun: the ground storey (posts, the doorway with its noren (a cut-out), a lattice front, rice
    bales stacked by it), the eave (a tiled pent roof) at 2.6 m, the low upper storey of plaster with its slatted
    windows, the main roof. Osaka's rooms are roomier than Edo's: a broad front."""
    X0, X1, Zf, Zb = Hs["X0"], Hs["X1"], Hs["Zf"], Hs["Zb"]
    e, u, r = Hs["eave"], Hs["upper"], Hs["ridge"]
    out = {}
    # ---- the west side wall (lit): boards below, plaster above, under the roofs' ends
    sheet.poly([g(X1, Zf), g(X1, Zb), g(X1, Zb, 180), g(X1, Zf, 180)], lerp(WOOD_LIT, NAPLES, 0.1))
    sheet.poly([g(X1, Zf, 180), g(X1, Zb, 180), g(X1, Zb, u), g(X1, Zf - 60, u + 10), g(X1, Zf, e)], PLASTER_LIT)
    # its gable (the main roof's end): a triangle of plaster to the ridge
    mid = (Zf + Zb) / 2 - 40
    sheet.poly([g(X1, Zf - 60, u + 10), g(X1, Zb, u), g(X1, mid, r - 20)], PLASTER_LIT)
    for Z in np.linspace(Zf, Zb, 7)[1:-1]:                  # boards' joints
        lines.line([g(X1, Z, 0), g(X1, Z, 180)], SIENNA, 0.6, 0.4)
    # ---- the front (facing us: shade): the ground storey
    front_c = lerp(WOOD_SH, ULTRA, 0.1)
    sheet.poly([g(X0, Zf), g(X1, Zf), g(X1, Zf, e), g(X0, Zf, e)], front_c)
    # the doorway (dark inside; the noren hangs in it as a cut-out), a lattice front beside it
    d0, d1 = door_at
    sheet.poly([g(d0, Zf), g(d1, Zf), g(d1, Zf, 205), g(d0, Zf, 205)], lerp(PRUSSIAN, WOOD_DARK, 0.4))
    out["door"] = (d0, d1)
    if kind == "shop":
        lat0, lat1 = (d1 + 30, X1 - 25) if d1 + 30 < X1 - 25 else (X0 + 25, d0 - 30)
        sheet.poly([g(lat0, Zf, 45), g(lat1, Zf, 45), g(lat1, Zf, 215), g(lat0, Zf, 215)], lerp(PRUSSIAN, WOOD_DARK, 0.35))
        lattice(lines, CAM, lat0, lat1, 45, 215, Zf + 2, lerp(WOOD, ULTRA, 0.12), gap=6.0, bar=3.6)
        out["lattice"] = (lat0, lat1)
        # the other side of the door: a plain board front with a high window
        if X0 + 25 < d0 - 30:
            lattice(lines, CAM, X0 + 25, d0 - 30, 150, 215, Zf + 2, lerp(WOOD, ULTRA, 0.12), gap=7.0, bar=3.5)
    else:
        # a house whose shop is shut today: its board shutters across the front, a battened row, a small door open
        for X in np.arange(X0 + 20, X1 - 10, 46):
            if d0 - 10 < X < d1 + 10:
                continue
            lines.line([g(X, Zf + 1, 8), g(X, Zf + 1, 212)], lerp(WOOD_SH, PRUSSIAN, 0.3), 0.6, 0.6)
        for yv in (60, 140):
            lines.line([g(X0 + 20, Zf + 1, yv), g(d0 - 8, Zf + 1, yv)], lerp(WOOD_SH, NAPLES, 0.15), max(0.8, 6 * CAM.k(X0, Zf)), 0.9)
            lines.line([g(d1 + 8, Zf + 1, yv), g(X1 - 10, Zf + 1, yv)], lerp(WOOD_SH, NAPLES, 0.15), max(0.8, 6 * CAM.k(X1, Zf)), 0.9)
    # posts at the ends and either side of the door, the sill beam and the lintel beam
    for X in (X0 + 6, d0 - 6, d1 + 6, X1 - 6):
        lines.line([g(X, Zf + 1, 0), g(X, Zf + 1, e)], lerp(WOOD_SH, PRUSSIAN, 0.2), max(1.0, 13 * CAM.k(X, Zf)), 1.0)
    lines.line([g(X0, Zf + 1, 215), g(X1, Zf + 1, 215)], lerp(WOOD_SH, PRUSSIAN, 0.2), max(1.0, 12 * CAM.k(X1, Zf)), 1.0)
    # ---- the pent roof (the eave over the ground storey): one tiled slope toward us, lit (it faces up and north)
    roof_slope(sheet, CAM, lines, (X0 - 40, e - 20, Zf + 95), (X1 + 40, e - 20, Zf + 95), (X0 - 40, e + 55, Zf - 10), (X1 + 40, e + 55, Zf - 10))
    # its end on the west side (a thin triangle in the sun)
    sheet.poly([g(X1 + 40, Zf + 95, e - 20), g(X1 + 40, Zf - 10, e + 55), g(X1 + 40, Zf - 10, e - 20)], TILE_DEEP)
    # ---- the upper storey: plaster (shade), set back a little, with slatted windows (mushiko)
    Zu = Zf - 30
    sheet.poly([g(X0, Zu, e + 55), g(X1, Zu, e + 55), g(X1, Zu, u), g(X0, Zu, u)], PLASTER_SH)
    n_win = 2 if X1 - X0 > 380 else 1
    for i in range(n_win):
        cx = X0 + (X1 - X0) * (i + 1) / (n_win + 1)
        a0, a1 = cx - 75, cx + 75
        sheet.poly([g(a0, Zu + 1, e + 95), g(a1, Zu + 1, e + 95), g(a1, Zu + 1, u - 40), g(a0, Zu + 1, u - 40)], lerp(PLASTER_SH, PRUSSIAN, 0.45))
        lattice(lines, CAM, a0 + 6, a1 - 6, e + 95, u - 40, Zu + 2, lerp(PLASTER_SH, WHITE, 0.25), gap=7.0, bar=6.0)
        lines.line([g(a0, Zu + 1, e + 95), g(a1, Zu + 1, e + 95), g(a1, Zu + 1, u - 40), g(a0, Zu + 1, u - 40), g(a0, Zu + 1, e + 95)], PRUSSIAN, 0.7, 0.55)
    # ---- the main roof: the slope toward us, ridge along the street; its edge on the west gable (a lit verge)
    eave_a, eave_b = (X0 - 50, u - 10, Zu + 80), (X1 + 50, u - 10, Zu + 80)
    ridge_a, ridge_b = (X0 - 50, r, mid), (X1 + 50, r, mid)
    roof_slope(sheet, CAM, lines, eave_a, eave_b, ridge_a, ridge_b)
    sheet.line([g(X1 + 50, Zu + 80, u - 10), g(X1 + 50, mid, r)], TILE_DEEP, max(1.2, 14 * CAM.k(X1, Zf)))
    # the ridge's cap: a heavy dark line, its ends lifted
    pa, pb = g(X0 - 50, mid, r), g(X1 + 50, mid, r)
    sheet.line([(pa[0], pa[1] - 4), pa, pb, (pb[0], pb[1] - 4)], TILE_DEEP, max(1.5, 16 * CAM.k(X1, mid)))
    # ---- the contour: the silhouette and the corners
    for pts in ([g(X1, Zf), g(X1, Zf, e)], [g(X1, Zb), g(X1, Zb, u)], [g(X0, Zf), g(X1, Zf), g(X1, Zb)],
                [g(X1, Zb, u), g(X1, mid, r - 20)], [g(X0, Zf), g(X0, Zf, e)]):
        CAM.line(lines, pts, CAM.depth(X1, Zf))
    out["front"] = [g(X0, Zf), g(X1, Zf), g(X1, Zf, e), g(X0, Zf, e)]
    out["side"] = [g(X1, Zf), g(X1, Zb), g(X1, Zb, u), g(X1, Zf, e)]
    out["roof"] = [g(X0 - 50, Zu + 80, u - 10), g(X1 + 50, Zu + 80, u - 10), g(X1 + 50, mid, r), g(X0 - 50, mid, r)]
    out["sign"] = None
    return out


def bales_stack(sheet, lines, X0, X1, Zf, rows=3, depth=2):
    """Rice bales stacked against a front: straw bales (tawara), round ends toward us, in rows, the top row set back."""
    rng = np.random.default_rng(int(X0) & 0xffff)
    L, R = 75.0, 24.0                                        # a bale's length and half its height
    out = []
    for row in range(rows):
        n = int((X1 - X0) / (2 * R + 4)) - row
        for i in range(n):
            X = X0 + R + row * R + i * (2 * R + 4)
            Y = R + row * 2 * R * 0.92
            Zc = Zf + L / 2 - row * 6
            p = g(X, Zc + L / 2, Y)                          # its end toward us
            k = CAM.k(X, Zc)
            rx, ry = R * k * 1.05, R * k
            sheet.ellipse(p[0], p[1], rx, ry, STRAW_LIT if rng.random() < 0.7 else lerp(STRAW_LIT, STRAW_SH, 0.3))
            sheet.ellipse(p[0] + rx * 0.15, p[1] + ry * 0.1, rx * 0.55, ry * 0.5, lerp(STRAW_LIT, STRAW_SH, 0.45))
            lines.line([(p[0] - rx * 0.7, p[1] - ry * 0.6), (p[0] - rx * 0.7, p[1] + ry * 0.6)], STRAW_SH, max(0.6, 3 * k), 0.8)       # the binding ropes
            lines.line([(p[0] + rx * 0.7, p[1] - ry * 0.6), (p[0] + rx * 0.7, p[1] + ry * 0.6)], STRAW_SH, max(0.6, 3 * k), 0.8)
            out.append(p)
    return out


def details(pic, info, seed=SEED, fast=False):
    x, y = grid(SHAPE)
    rng = np.random.default_rng(seed + 50)
    sheet = Paper(SHAPE)
    lines = sheet                                            # one sheet in depth order (style.md: a far line never over a near fill)
    info["bridge"] = bridge(sheet, lines)
    # the neighbour (east, lower), then O-Natsu's house
    info["neigh"] = house(sheet, lines, NEIGH, (NEIGH["X1"] - 230, NEIGH["X1"] - 110), kind="shutters", rng=rng)
    info["house"] = house(sheet, lines, HOUSE, DOOR, rng=rng)
    # the fire wall standing up between the two houses' upper storeys (a plastered wing with its own little tiled cap)
    Xu, Zu = HOUSE["X0"] + 10, HOUSE["Zf"] - 30
    ud = [g(Xu, Zu + 60, HOUSE["eave"] + 55), g(Xu, Zu + 60, HOUSE["upper"] + 20), g(Xu + 22, Zu + 60, HOUSE["upper"] + 20), g(Xu + 22, Zu + 60, HOUSE["eave"] + 55)]
    sheet.poly(ud, PLASTER_SH)
    sheet.poly([g(Xu - 14, Zu + 74, HOUSE["upper"] + 20), g(Xu + 36, Zu + 74, HOUSE["upper"] + 20), g(Xu + 30, Zu + 60, HOUSE["upper"] + 46), g(Xu - 8, Zu + 60, HOUSE["upper"] + 46)], TILE_SH)
    lines.line(ud + [ud[0]], PRUSSIAN, 0.8, 0.6)
    # the rice bales stacked against her front, left of the door
    info["bales"] = bales_stack(sheet, lines, BALES[0], BALES[1], HOUSE["Zf"] + 5)
    # a hanging signboard under her eave: the house's name as the shape of writing (no real shop's name)
    sx = HOUSE["X1"] - 120
    a, b = g(sx, HOUSE["Zf"] + 60, 240), g(sx, HOUSE["Zf"] + 60, 150)
    k = CAM.k(sx, HOUSE["Zf"])
    sheet.poly([(a[0] - 14 * k, a[1]), (a[0] + 14 * k, a[1]), (b[0] + 14 * k, b[1]), (b[0] - 14 * k, b[1])], lerp(WOOD_LIT, NAPLES, 0.2))
    writing(sheet, (a[0], a[1] + 4), (b[0], b[1] - 2), np.random.default_rng(7), PRUSSIAN, 0.9, 0.9)
    lines.line([(a[0] - 14 * k, a[1]), (a[0] + 14 * k, a[1]), (b[0] + 14 * k, b[1]), (b[0] - 14 * k, b[1]), (a[0] - 14 * k, a[1])], PRUSSIAN, 0.8, 0.6)
    info["sign_box"] = [int(a[0] - 16 * k), int(a[1]) - 2, int(32 * k) + 2, int(b[1] - a[1]) + 4]
    sheet.onto(pic)
    # pebbles on the street, sparse
    import land
    stones = Sheet(SHAPE)
    land.stones(stones, pic, HZ, seed + 90, 50, zone=((info["ground"] > 0.5) & (y > 470)), ground=info["ground"], size=(0.6, 2.2),
                tones=(tintw(EARTH, 0.4), lerp(EARTH, SIENNA, 0.2), lerp(EARTH, PRUSSIAN, 0.25), lerp(EARTH, PRUSSIAN, 0.4)))
    sc, sa = stones.done()
    over(pic, sc, sa)
    return pic


# ================================================================ the cut-outs, their states, the frames
def cutouts(pic, info, fast=False):
    """Every cut-out of the scene and its other states, brushed over what it stands in front of. -> {name: (c, a)}."""
    import edo_dojima_things as T
    planes, extra = {}, {}

    def made(name, sl, seed, keep=0.45, sizes=(6, 3, 2), under=None):
        s_, l_ = sl[0], sl[1]
        c, a = s_.done()
        lc, la = l_.done()
        planes[name] = brushed(c, a, lc, la, under if under is not None else under_colour(pic, np.maximum(a, la), EARTH), seed=seed, sizes=sizes, keep=keep, fast=fast)

    r = T.lighter_moored()
    made("lighter", r, 11, keep=0.5)
    extra["lighter"] = r[2]
    r = T.market()
    made("market", r, 12, keep=0.55)
    extra["market"] = r[2]
    made("noren", T.noren(info["house"]["door"]), 13, keep=0.6)
    made("sandals", T.sandals(4), 14, keep=0.55)
    made("sandals-few", T.sandals(2), 14, keep=0.55)
    r = T.pot()
    made("pot", r, 15, keep=0.5)
    extra["pot"] = r[2]
    r = T.stall_table()
    made("stall", r, 16, keep=0.5)
    extra["stall"] = r[2]
    made("tray", T.tray(15), 17, keep=0.6)
    made("tray-half", T.tray(6), 17, keep=0.6)
    made("tray-empty", T.tray(0), 17, keep=0.6)
    r = T.kettle()
    made("kettle", r, 18, keep=0.5)
    extra["kettle"] = r[2]
    made("front", T.front(), 19, keep=0.45)
    return planes, extra


ORDER = ["lighter", "market", "noren", "sandals", "pot", "stall", "tray", "kettle", "front"]     # back to front, nobody there


def frames(fast=False):
    """The moving things' frames, each a small cropped picture: -> {name: (c, a, foot in the stage)}."""
    import edo_dojima_things as T
    out = {}
    for name, (length, k, seed, var) in {"lighter-near": (180.0, 0.28, 21, 0), "lighter-far": (112.0, 0.19, 22, 1)}.items():
        s_, l_, at = T.lighter_frame(length, k, seed, var)
        c, a = s_.done()
        lc, la = l_.done()
        out[name] = brushed(c, a, lc, la, lerp(lerp(VIRIDIAN, OCHRE, 0.38), CERULEAN, 0.3), seed=seed, sizes=(3, 2), keep=0.7, fast=fast) + (at,)
    for i, (s_, l_, at) in enumerate(T.runner_frames()):
        c, a = s_.done()
        lc, la = l_.done()
        out[f"runner-{i + 1}"] = brushed(c, a, lc, la, EARTH, seed=30 + i, sizes=(3, 2), keep=0.75, fast=fast) + (at,)
    return out


def splash(origin, fast=False):
    import edo_dojima_things as T
    out = {}
    for i, (s_, l_, at) in enumerate(T.splash_frames(origin)):
        c, a = s_.done()
        lc, la = l_.done()
        over(c, lc, la)
        out[f"splash-{i + 1}"] = (c, np.maximum(a, la), at)
    return out


def save_frames(group, prefix_box=None):
    """Frames of one thing on one canvas size with one foot: crop them all to the union of their boxes."""
    ys0, ys1, xs0, xs1 = H, 0, W, 0
    for c, a, at in group.values():
        ys, xs = np.where(a > 0.5)
        ys0, ys1, xs0, xs1 = min(ys0, ys.min()), max(ys1, ys.max()), min(xs0, xs.min()), max(xs1, xs.max())
    y0, y1, x0, x1 = max(ys0 - 2, 0), min(ys1 + 3, H), max(xs0 - 2, 0), min(xs1 + 3, W)
    meta = {}
    for name, (c, a, at) in group.items():
        finish(c[y0:y1, x0:x1].copy(), f"{OUT}/{name}.png", 40, a[y0:y1, x0:x1].copy())
        meta[name] = dict(size=[int(x1 - x0), int(y1 - y0)], foot=[int(round(at[0] - x0)), int(round(at[1] - y0))], box=[int(x0), int(y0), int(x1 - x0), int(y1 - y0)])
    return meta


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = "fast" in sys.argv or "layout" in sys.argv          # layout: the fast passes (the same geometry and boxes), layout.json only
    base, info = under()
    Image.fromarray((base * 255).astype(np.uint8)).save(OUT + "-1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.26)
    details(pic, info, fast=fast)
    print("details", round(time.time() - t0, 1))
    planes, extra = cutouts(pic, info, fast)
    whole = pic.copy()
    for name in ORDER:
        c, a = planes[name]
        over(whole, c, (a > 0.5).astype(F32))
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-all.png")
    print("cut-outs", round(time.time() - t0, 1))
    fr = frames(fast)
    sp = splash(extra["market"]["bucket"], fast)
    if "layout" in sys.argv:                                   # the frames' sizes and feet from the installed ones
        import edo_dojima_layout as L
        meta = json.load(open(OUT + "/layout.json"))["frames"]
        with open(OUT + "/layout.json", "w") as f:
            json.dump(L.layout(planes, extra, info, meta), f, indent=1)
        print("layout.json only")
        sys.exit()
    if fast:
        sys.exit()
    for f in os.listdir(OUT):
        if f.endswith(".png"):
            os.remove(os.path.join(OUT, f))
    print("back", finish(pic, OUT + "/back.png", 152))
    sizes = {"lighter": 48, "market": 96, "noren": 32, "sandals": 32, "sandals-few": 32, "pot": 48, "stall": 48, "tray": 32, "tray-half": 32,
             "tray-empty": 32, "kettle": 32, "front": 48}
    for name, (c, a) in planes.items():
        print(name, finish(c, f"{OUT}/{name}.png", sizes.get(name, 48), a))
    meta = {}
    meta.update(save_frames({"lighter-near": fr["lighter-near"]}))
    meta.update(save_frames({"lighter-far": fr["lighter-far"]}))
    meta.update(save_frames({k: v for k, v in fr.items() if k.startswith("runner")}))
    meta.update(save_frames(sp))
    import edo_dojima_layout as L
    lay = L.layout(planes, extra, info, meta)
    with open(OUT + "/layout.json", "w") as f:
        json.dump(lay, f, indent=1)
    comp = Image.open(OUT + "/back.png").convert("RGBA")
    for name in ORDER:
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(OUT + "-comp.png")
    print("done", round(time.time() - t0, 1))

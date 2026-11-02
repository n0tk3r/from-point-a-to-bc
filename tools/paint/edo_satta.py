"""PAINT-21A: the top of the Satta Pass, about 8 April 1830, morning, wind (edo-satta). The Tokaido's road of 1655, cut
high on the headland's mountainside between Yui and Okitsu, about 90 m over Suruga Bay. In the woodblock manner of the act's
style sheet (S/work-20-paintA/style.md); keyed at 50 in `edo-morning` (PAINT-20A's key). Our own place on the road and our
own view: the road running across the picture, the drop beyond its bank, the bay spread out below, Fuji across it.

LIGHT   The act's sun: in the east, behind us and to the left, about 30 degrees up: faces toward us and to the left are lit,
        shadows fall to the right and away, flat and blue.
DEPTH   horizon 288, full 590 (persp.Camera: eye 330 cm, Z0 875, focal 800). The road is level here; at the left edge it
        drops away toward Nishikurasawa (the climb they came up), at the right edge it starts down west to Okitsu.
TONES   light: Fuji's snow and its cap of cloud, the paper at the horizon, the white water on the old shore, the sunlit
        road. middle: the bay, the sky, the grass of the bank. dark: the headland's flank at the left, the pine, the
        contour. Fuji, enormous, owns the picture; the Jizo's red bib (the picture's red touch) is where the eye goes
        next, then the pine leaning toward Fuji, then the white water below.
PLACE   We stand on the road at the top of the pass looking out over its bank (the act's compass: the bay in front, Fuji
        across it, west to the right). Below us at the left the headland's flank falls away to the sea; along its foot the
        old shore, where the road ran before 1655, is only white water and rock now ("forget your parent, forget your
        child"); beyond it the coast curves back toward Kurasawa and Yui and on under Fuji. Across the bay, east, Izu lies
        long and low; far to the right, west, Okitsu's roofs and a temple roof in the haze. On the bank: the Jizo at child
        height in its red bib and little straw hat; the bent pine at the right, leaning toward Fuji. O-Shige's stone at
        the road's far edge, left.

  python3 edo_satta.py fast     the composition without the brush pass (out/edo-satta-1-under.png, -2-all.png)
  python3 edo_satta.py          the full passes: out/edo-satta/ (back.png, the cut-outs, layout.json)
"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
import land
from edo_kurasawa_kit import *

SEED = 1655
OUT = "out/edo-satta"
SHAPE = (H, W)
HZ, FULL = 288, 590
V = View(HZ, FULL)                                                   # the act's sun, as at Yui (1.6 : 0.5)
gp, kz = V.gp, V.kz
DROP = 9000.0                                                        # the bay lies this far (cm) below the road

# ---------------------------------------------------------------- where things are (cm; see the module's PLACE)
ROAD = dict(z0=70.0, z1=430.0)                                       # the road across the picture (rows 567 to 491)
BANK = dict(z0=430.0, z1=520.0, h=34.0)                              # the bank at the road's far edge: earth and grass, never a fall
JIZO = dict(x=-25.0, z=446.0, h=129.0)                               # the Jizo before the bank: exactly Little Sister's height at `jizo`
JIZO_MARK = (-110.0, 372.0)                                          # before it and a little to its left (row 500: Little Sister 78 px)
SEAT = dict(x=-400.0, z=420.0, w=92.0, d=56.0, h=44.0)              # O-Shige's stone at the road's far edge
PINE = dict(x=520.0, z=540.0)                                        # the bent pine on the bank's top, right (its foot at x 694)
FUJI = Fuji(summit=(330.0, 40.0), foot=292.0, half=530.0, snow=0.40, seed=21)
COAST = [(-10, 452), (24, 444), (60, 437), (104, 432), (150, 430), (196, 433), (236, 440), (268, 449), (294, 460), (316, 474)]   # the near flank's waterline
CLIFF_FOOT = [(-10, 368), (30, 365), (70, 361), (110, 357), (150, 352), (186, 348), (214, 346)]     # the far stretch's cliffs: their foot
CLIFF_TOP = [(-10, 340), (30, 341), (70, 337), (110, 335), (150, 333), (186, 336), (214, 346)]      # and their lip
RIDGE = [(-10, 236), (30, 246), (70, 260), (110, 276), (146, 294), (176, 314), (198, 332), (214, 346)]   # the far stretch's skyline: Satta's spurs rise above the pass
FAR = [(-10, 300), (60, 306), (120, 311), (170, 316)]                # the coast of Kurasawa and Yui, beyond the flank's tip


def bank_top(x):
    """The row of the bank's grassy top (the edge beyond which the ground falls away), at picture column x: a gentle wave
    of turf, a low place before `view` where one stands to look out; at the left the road and its bank drop toward the
    climb, at the right edge they start down to Okitsu."""
    base = gp(0, BANK["z1"], BANK["h"])[1]
    wav = 2.4 * math.sin(x / 41.0 + 0.7) + 1.4 * math.sin(x / 17.0 + 2.1) + 0.8 * math.sin(x / 7.3)
    dip = 7.0 * math.exp(-((x - 262) / 30.0) ** 2)
    v = base + wav + dip
    if x < 150:
        v += (150 - x) ** 1.6 * 0.020
    if x > 690:
        v += (x - 690) ** 1.5 * 0.022
    return v


def road_far(x):
    """The row of the road's far edge (where the bank begins) at column x."""
    base = gp(0, ROAD["z1"])[1]
    if x < 150:
        return base + (150 - x) ** 1.6 * 0.024
    if x > 690:
        return base + (x - 690) ** 1.5 * 0.020
    return base


# ================================================================ pass 1: broad and flat
def paint_sky(seed):
    """The graded band (style.md section 3): deep at the top, the paper at the horizon; eight bands, the top a little
    deeper than Yui's (we are higher, and the morning wind has cleared the air)."""
    rows = [0, 30, 70, 112, 152, 190, 224, 254, HZ + 2]
    cols = [shade(COBALT, 0.48), shade(COBALT, 0.30), mixp(COBALT, ULTRA, 0.25), COBALT, mixp(COBALT, CERULEAN, 0.55), CERULEAN,
            tintw(CERULEAN, 0.55), PAPER, PAPER]
    pic = bands(SHAPE, rows, cols, soft=6.0, wobble=2.5, seed=seed, patch=0.02)
    x, y = grid(SHAPE)
    glow(pic, tintw(NAPLES, 0.5), (np.clip(1 - x / 420.0, 0, 1) * np.clip(1 - np.abs(y - 262) / 70.0, 0, 1) * 0.10).astype(F32))
    # two long flat clouds streaming in the wind (lead white, a 1 px line on top only): high, and few
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    for (cx_, cy_, rx_, ry_) in ((640, 92, 120, 5.5), (120, 150, 90, 4.5), (720, 176, 70, 3.5)):
        top = [(cx_ - rx_ + 2 * rx_ * u, cy_ - ry_ * math.sin(math.pi * u) ** 0.7) for u in np.linspace(0, 1, 30)]
        bot = [(cx_ - rx_ + 2 * rx_ * u, cy_ + ry_ * 0.35 * math.sin(math.pi * u) ** 1.4) for u in np.linspace(0, 1, 30)]
        sheet.poly(top + list(reversed(bot)), tintw(CERULEAN, 0.80))
        lines.line(top, PRUSSIAN, 0.8, 0.35)
    sheet.onto(pic)
    lines.onto(pic)
    return pic


def paint_far(pic, seed):
    """Fuji (the same mountain as at Kurasawa, bigger: we are higher and nearer the head of the bay's line), the far
    shore at its foot, Izu long and low across the bay to the east, Okitsu's shore far west in the haze."""
    fm, snow = FUJI.paint(pic, PAPER, seed)
    far = mask_poly(SHAPE, [(-10, HZ - 4), (200, HZ - 5), (420, HZ - 3), (560, HZ - 4), (560, HZ + 4), (-10, HZ + 4)], soft=0.8, wobble=1.2, seed=seed + 4)
    over(pic, tintw(mixp(COBALT, VIRIDIAN, 0.35), 0.62), far)
    # Izu: a long low range across the bay (beyond a kilometre: no contour, two flats, cerulean and white)
    izu = [(430, HZ + 1), (452, 279), (480, 274), (516, 270), (548, 272), (584, 268), (612, 271), (646, 276), (672, 281), (700, HZ + 1)]
    im_ = mask_poly(SHAPE, izu, soft=0.8, wobble=1.0, seed=seed + 8)
    over(pic, lerp(tintw(CERULEAN, 0.30), COBALT, 0.22), im_)
    ish = mask_poly(SHAPE, [(516, 270), (548, 272), (584, 268), (612, 271), (646, 276), (672, 281), (700, HZ + 1), (560, HZ + 1)], soft=0.8, wobble=1.0, seed=seed + 9)
    over(pic, lerp(tintw(COBALT, 0.30), CERULEAN, 0.15), (ish * im_ * 0.8).astype(F32))
    # Okitsu's shore, west, far right: low hills in the haze, a pale beach line (roofs and the temple in details())
    ok = [(668, HZ + 2), (690, 284), (716, 276), (742, 272), (770, 276), (800, 270), (812, 270), (812, 316), (770, 314), (720, 310), (690, 302)]
    om = mask_poly(SHAPE, ok, soft=0.8, wobble=1.2, seed=seed + 10)
    over(pic, lerp(mixp(VIRIDIAN, COBALT, 0.45), PAPER, 0.52), om)
    over(pic, tintw(NAPLES, 0.42), (mask_line(SHAPE, [(690, 303), (720, 311), (770, 315), (812, 317)], [1.4, 1.8, 2.2, 2.4], soft=0.4) * om).astype(F32))
    return fm, snow


def water_mask():
    pts = [(x_, bank_top(x_)) for x_ in np.linspace(-10, 810, 60)]
    poly = [(-10, HZ - 1), (W + 10, HZ - 1)] + list(reversed(pts))
    return mask_poly(SHAPE, poly, soft=0.6, wobble=0.6, seed=3)


def paint_bay(pic, seed):
    """The bay far below in eight bands (style.md section 3): the paper at the horizon, cerulean, cobalt, deeper toward
    the foot of the cliffs below us."""
    wm = water_mask()
    rows = [HZ, HZ + 6, HZ + 14, HZ + 26, HZ + 44, HZ + 68, HZ + 100, HZ + 140, HZ + 200]
    cols = [tintw(CERULEAN, 0.62), tintw(CERULEAN, 0.40), tintw(CERULEAN, 0.16), mixp(CERULEAN, COBALT, 0.42), mixp(CERULEAN, COBALT, 0.75),
            COBALT, mixp(COBALT, ULTRA, 0.28), mixp(COBALT, ULTRA, 0.45), mixp(COBALT, ULTRA, 0.45)]
    wb = bands(SHAPE, rows, cols, soft=3.5, wobble=0.0, seed=seed + 20, patch=0.015)
    over(pic, wb, wm)
    return wm


def flank_mask():
    """The headland's near flank falling away below us at the left: from its waterline down to the bank."""
    pts = [(x_, bank_top(x_) + 2) for x_ in np.linspace(330, -10, 20)]
    return mask_poly(SHAPE, COAST + pts, soft=0.6, wobble=1.2, seed=33)


def far_mask():
    """The farther stretch of the headland toward Kurasawa: its slope from the skyline down to its cliffs' foot."""
    return mask_poly(SHAPE, RIDGE + list(reversed(CLIFF_FOOT)), soft=0.6, wobble=1.0, seed=34)


def paint_flank(pic, seed):
    """Two planes of the headland, overlapping as the prints build distance. The near flank: a steep slope of brush and
    pine falling to the sea (dark viridian; its spurs' faces toward the sun lit; scars of crumbly rock). The farther
    stretch toward Kurasawa: its slope paler (the air), and its cliffs facing us, lit, a band of warm grey rock."""
    x, y = grid(SHAPE)
    fm = far_mask()
    over(pic, lerp(lerp(VIRIDIAN, PRUSSIAN, 0.24), PAPER, 0.26), fm)
    # its spurs' faces toward the sun (lit flats), the folds between them darker, all paled by a kilometre of air
    for pts_ in ([(-10, 262), (20, 262), (44, 286), (60, 322), (40, 334), (-10, 334)], [(64, 270), (92, 280), (112, 300), (126, 330), (100, 334), (84, 300)],
                 [(130, 298), (152, 306), (168, 324), (176, 334), (150, 334)]):
        lm = mask_poly(SHAPE, pts_, soft=0.7, wobble=2.0, seed=seed + int(pts_[0][0]) + 50)
        over(pic, lerp(mixp(VIRIDIAN, VERONESE, 0.45), PAPER, 0.24), (lm * fm * 0.9).astype(F32))
    cliff = mask_poly(SHAPE, CLIFF_TOP + list(reversed(CLIFF_FOOT)), soft=0.5, wobble=0.8, seed=seed + 3)
    rock = lerp(lerp(STONE_LIT, STONE, 0.45), COBALT, 0.06)
    over(pic, rock, cliff)
    rock_lo = mask_poly(SHAPE, [(p[0], p[1] - 6) for p in CLIFF_FOOT] + list(reversed(CLIFF_FOOT)), soft=0.5, wobble=0.8, seed=seed + 5)
    over(pic, lerp(STONE, PRUSSIAN, 0.22), (rock_lo * cliff).astype(F32))
    lip = mask_line(SHAPE, [(p[0], p[1] + 1.2) for p in CLIFF_TOP], 1.6, soft=0.4)
    over(pic, lerp(lerp(VIRIDIAN, PRUSSIAN, 0.5), PAPER, 0.15), (lip * 0.8).astype(F32))
    rshade = mask_poly(SHAPE, [(150, 334), (186, 337), (214, 346), (186, 348), (150, 352)], soft=0.5, wobble=0.8, seed=seed + 4)
    over(pic, lerp(STONE, PRUSSIAN, 0.35), (rshade * cliff).astype(F32))
    rng_c = np.random.default_rng(seed + 6)
    xx = 2.0
    while xx < 206:                                                       # the rock's fissures: irregular, some long, some short, leaning
        top_ = float(np.interp(xx, [p[0] for p in CLIFF_TOP], [p[1] for p in CLIFF_TOP]))
        foot_ = float(np.interp(xx, [p[0] for p in CLIFF_FOOT], [p[1] for p in CLIFF_FOOT]))
        a_ = top_ + 2 + rng_c.uniform(0, 6)
        b_ = a_ + (foot_ - a_) * rng_c.uniform(0.4, 1.0)
        lean_ = rng_c.uniform(-2.5, 2.5)
        over(pic, lerp(STONE, PRUSSIAN, 0.45), (mask_line(SHAPE, [(xx, a_), (xx + lean_ * 0.5, (a_ + b_) / 2), (xx + lean_, b_)], rng_c.uniform(0.8, 1.4), soft=0.3) * 0.8).astype(F32))
        xx += rng_c.uniform(5, 16)
    m = flank_mask()
    over(pic, flat(lerp(VIRIDIAN, PRUSSIAN, 0.32), SHAPE, seed + 12, 0.03, 60), m)
    for pts_ in ([(0, 480), (24, 460), (46, 446), (70, 440), (82, 452), (64, 470), (50, 492)],
                 [(118, 490), (140, 462), (160, 444), (178, 438), (194, 446), (176, 472), (166, 496)],
                 [(232, 478), (246, 458), (262, 452), (274, 462), (266, 480)]):
        lm = mask_poly(SHAPE, pts_, soft=0.8, wobble=2.5, seed=seed + int(pts_[0][0]))
        over(pic, mixp(VIRIDIAN, VERONESE, 0.40), (lm * m * 0.9).astype(F32))
    for (cx_, cy_, rx_, ry_) in ((96, 454, 12, 6), (214, 458, 10, 5)):
        sc = mask_ellipse(SHAPE, cx_, cy_, rx_, ry_, soft=0.8, wobble=2.5, seed=seed + int(cx_))
        over(pic, lerp(tintw(OCHRE, 0.30), PRUSSIAN, 0.24), (sc * m * 0.85).astype(F32))
    return np.maximum(m, fm)


def paint_oldshore(pic, seed):
    """The old shore, where the road ran before 1655: white water breaking along the foot of the cliffs (only rock and
    waves now), and round the near flank's foot. Painted still: the broken pale bands; the engine's waves move over them
    (fx oldshore-waves)."""
    x, y = grid(SHAPE)
    wm = water_mask() * (1 - flank_mask()) * (1 - far_mask())
    foam = mask_line(SHAPE, [(p[0], p[1] + 2.0) for p in CLIFF_FOOT], [4.2, 4.0, 3.8, 3.5, 3.2, 2.8, 2.4], soft=0.5)
    brk = step(0.30, 0.50, noise(SHAPE, (14, 5), seed + 3, 3))
    over(pic, tintw(CERULEAN, 0.88), (foam * (0.65 + 0.35 * brk) * wm).astype(F32))
    foam2 = mask_line(SHAPE, [(p[0] + 4, p[1] + 7.5) for p in CLIFF_FOOT], [1.6] * len(CLIFF_FOOT), soft=0.5) * step(0.45, 0.6, noise(SHAPE, (12, 5), seed + 5, 3))
    over(pic, tintw(CERULEAN, 0.78), (foam2 * wm * 0.85).astype(F32))
    near = mask_line(SHAPE, [(p[0], p[1] - 1.2) for p in COAST], [1.6 + 0.25 * i for i in range(len(COAST))], soft=0.5)
    over(pic, tintw(CERULEAN, 0.84), (near * (0.6 + 0.4 * brk) * wm).astype(F32))
    return np.maximum(foam, near)


def paint_ground(pic, seed):
    """The bank (earth and grass, low: never a drop at the road), the road (packed earth), the near verge."""
    x, y = grid(SHAPE)
    X, Z, below = V.cam.floor_grid(SHAPE)
    t = np.clip((y - HZ) / (H - HZ), 0, 1)
    tops = np.array([bank_top(c) for c in range(W)], dtype=F32)
    fars = np.array([road_far(c) for c in range(W)], dtype=F32)
    gm = (y >= tops[None, :] - 0.5).astype(F32)
    gm = blur(gm, 0.6)
    # the bank: grass on earth, its top lit (it faces up and toward us), its foot along the road in shade
    bank = flat(lerp(GRASS, EARTH, 0.18), SHAPE, seed + 31, 0.05, 30)
    over(pic, bank, gm)
    top_band = ((y >= tops[None, :]) & (y < tops[None, :] + 6)).astype(F32)
    over(pic, GRASS_LIT, (blur(top_band, 0.6) * 0.85).astype(F32))
    foot_band = ((y >= fars[None, :] - 7) & (y < fars[None, :])).astype(F32)
    over(pic, lerp(lerp(GRASS, EARTH, 0.4), COBALT, 0.28), (blur(foot_band, 0.6) * 0.8).astype(F32))
    # the road: packed earth, two worn tracks, stones (in details)
    rm = (y >= fars[None, :]).astype(F32)
    road = flat(lerp(EARTH, STONE, 0.20), SHAPE, seed + 36, 0.04, 50)
    road = lerp(road, PAPER, ((1 - t) ** 1.6 * 0.30)[..., None])
    over(pic, road, blur(rm, 0.8))
    for zc, wd in ((170.0, 70.0), (330.0, 60.0)):
        tr = mask_poly(SHAPE, [gp(-4000, zc - wd / 2), gp(4000, zc - wd / 2), gp(4000, zc + wd / 2), gp(-4000, zc + wd / 2)], soft=4.0, wobble=4.0, seed=seed + int(zc))
        over(pic, lerp(lerp(EARTH, STONE, 0.20), PAPER, 0.18), (tr * 0.45 * rm).astype(F32))
    # the near verge: the foot of the cut slope behind us (the road is cut into the mountainside): grass and earth
    near_m = np.clip((ROAD["z0"] - Z) / 30.0 + (noise(SHAPE, (50, 10), seed + 33, 3) - 0.5) * 1.2, 0, 1) * below
    over(pic, flat(lerp(GRASS, EARTH, 0.30), SHAPE, seed + 34, 0.06, 30), (near_m * rm).astype(F32))
    return gm, rm


def cast_shadows(pic, ground):
    """The Jizo's, the stone's and the pine's shadows, flat and blue, laid along the sun (to the right and away)."""
    sh = Paper(SHAPE)
    j = JIZO
    sh.poly(V.shadow_pts([(j["x"] - 18, 0, j["z"]), (j["x"] + 18, 0, j["z"]), (j["x"] + 18, 92, j["z"]), (j["x"] + 22, j["h"], j["z"]), (j["x"] - 22, j["h"], j["z"]), (j["x"] - 18, 92, j["z"])]),
            (0, 0, 0), 1.0)
    s = SEAT
    sh.poly(V.shadow_pts([(s["x"] - s["w"] / 2, 0, s["z"] - s["d"] / 2), (s["x"] + s["w"] / 2, 0, s["z"] - s["d"] / 2), (s["x"] + s["w"] / 2, s["h"], s["z"]),
                          (s["x"] - s["w"] / 2, s["h"], s["z"])]) + [gp(s["x"] + s["w"] / 2, s["z"] + s["d"] / 2)], (0, 0, 0), 1.0)
    c, a = sh.done()
    shade_ground(pic, (a * ground).astype(F32))
    return a


def under(seed=SEED):
    info = {}
    pic = paint_sky(seed)
    info["fuji"], info["snow"] = paint_far(pic, seed)
    info["water"] = paint_bay(pic, seed)
    info["flank"] = paint_flank(pic, seed)
    info["foam"] = paint_oldshore(pic, seed)
    info["ground"], info["road"] = paint_ground(pic, seed)
    info["shadow"] = cast_shadows(pic, info["ground"])
    land.haze(pic, HZ, PAPER, 0.28, 0.10, info["ground"])
    return np.clip(pic, 0, 1), info


# ================================================================ pass 3: the crisp things
def jizo(sheet, info):
    """The Jizo by the road (the pass is named for a holy image a fisherman caught in his net): a small grey stone figure
    on a low stone, a round head, the hands together at the breast, a red bib tied at the neck and a little straw hat on
    the head; exactly Little Sister's height at `jizo` (129 cm with its stone, 78 px here). Lit from the left."""
    J = JIZO
    x, z, h = J["x"], J["z"], J["h"]
    k = kz(z)
    stone_lit, stone_sh = lerp(STONE_LIT, NAPLES, 0.10), lerp(STONE, COBALT, 0.22)
    # the low stone it stands on
    sheet.poly([gp(x - 26, z - 18, 0), gp(x + 26, z - 18, 0), gp(x + 26, z - 18, 22), gp(x - 26, z - 18, 22)], stone_lit)
    sheet.poly([gp(x + 26, z - 18, 0), gp(x + 26, z + 18, 0), gp(x + 26, z + 18, 22), gp(x + 26, z - 18, 22)], stone_sh)
    sheet.poly([gp(x - 26, z - 18, 22), gp(x + 26, z - 18, 22), gp(x + 26, z + 18, 22), gp(x - 26, z + 18, 22)], lerp(stone_lit, PAPER, 0.15))
    # the body: a bell-shaped robe (lit left, shade right), rounded shoulders, the hands together at the breast
    b0, b1 = 22.0, 22.0 + 62.0
    body = []
    for u in np.linspace(0, 1, 9):
        body.append(gp(x - (19 - 6 * u ** 1.6), z - 6, b0 + (b1 - b0) * u))
    for u in np.linspace(1, 0, 9):
        body.append(gp(x + (19 - 6 * u ** 1.6), z - 6, b0 + (b1 - b0) * u))
    sheet.poly(body, stone_lit)
    sheet.poly([p for p in body if p[0] >= gp(x + 3, z - 6)[0]] + [gp(x + 3, z - 6, b0)], stone_sh)
    sheet.line([gp(x - 3, z - 7, b0 + 36), gp(x + 1, z - 7, b0 + 48)], lerp(stone_sh, PRUSSIAN, 0.25), max(1.0, 4.5 * k), 1.0)     # the joined hands
    sheet.line([gp(x - 14, z - 7, b0 + 4), gp(x + 14, z - 7, b0 + 4)], lerp(stone_sh, PRUSSIAN, 0.15), 0.7, 0.6)                # the robe's hem
    # the head: big and round, as the figures are made
    hc = gp(x, z - 6, b1 + 13)
    sheet.ellipse(hc[0], hc[1], 13 * k, 13.5 * k, stone_lit)
    sheet.ellipse(hc[0] + 5 * k, hc[1] + 1 * k, 7 * k, 12 * k, stone_sh)
    sheet.ellipse(hc[0] - 2 * k, hc[1] + 1 * k, 7 * k, 10 * k, stone_lit)
    for dx_ in (-4.5, 3.5):                                               # closed eyes: two small strokes
        sheet.line([(hc[0] + dx_ * k - 1.6 * k, hc[1] + 1.5 * k), (hc[0] + dx_ * k + 1.6 * k, hc[1] + 1.8 * k)], lerp(stone_sh, PRUSSIAN, 0.3), 0.6, 0.8)
    # the red bib: tied at the neck, a rounded apron over the chest (the picture's red touch)
    bib = [gp(x - 15, z - 8, b1 + 1), gp(x + 15, z - 8, b1 + 1), gp(x + 13, z - 8, b1 - 18), gp(x, z - 8, b1 - 27), gp(x - 13, z - 8, b1 - 18)]
    sheet.poly(bib, RED_BIB)
    sheet.poly([gp(x + 4, z - 8, b1 + 1), gp(x + 15, z - 8, b1 + 1), gp(x + 13, z - 8, b1 - 18), gp(x + 4, z - 8, b1 - 25)], lerp(RED_BIB, PRUSSIAN, 0.3))
    sheet.line([gp(x - 15, z - 8, b1 + 1), gp(x + 15, z - 8, b1 + 1)], lerp(RED_BIB, PRUSSIAN, 0.45), max(0.8, 2.4 * k), 1.0)
    # the little straw hat: a shallow cone, wider than the head, tipped a little back
    hat_y = b1 + 24
    hat = [gp(x - 23, z - 6, hat_y - 1), gp(x + 23, z - 6, hat_y - 3), gp(x + 3, z - 6, h)]
    sheet.poly(hat, lerp(tintw(OCHRE, 0.40), NAPLES, 0.12))
    sheet.poly([gp(x + 1, z - 6, hat_y - 2), gp(x + 22, z - 6, hat_y - 3), gp(x + 3, z - 6, h)], lerp(THATCH_SHADE, OCHRE, 0.35))
    for v in (0.35, 0.65):
        a = gp(x - 22 + 22 * v, z - 6, hat_y - 1 + (h - hat_y) * v)
        b = gp(x + 22 - 19 * v, z - 6, hat_y - 3 + (h - hat_y) * v)
        sheet.line([a, b], lerp(OCHRE, PRUSSIAN, 0.4), 0.6, 0.6)
    V.contour(sheet, [hat[0], hat[2], hat[1]], gp(x, z)[1], alpha=0.7)
    V.contour(sheet, body[1:] + body[:1], gp(x, z)[1], alpha=0.55)
    V.contour(sheet, [gp(x - 26, z - 18, 0), gp(x - 26, z - 18, 22), gp(x + 26, z - 18, 22), gp(x + 26, z + 18, 22)], gp(x, z)[1], alpha=0.6)
    info["jizo_box"] = [int(gp(x - 26, z)[0]) - 2, int(gp(x, z, h)[1]) - 2, int(52 * k) + 4, int(gp(x, z - 18)[1] - gp(x, z, h)[1]) + 4]
    info["hat_box"] = [int(gp(x - 24, z)[0]) - 1, int(gp(x, z - 6, h)[1]) - 2, int(48 * k) + 2, int(gp(x, z - 6, hat_y - 4)[1] - gp(x, z - 6, h)[1]) + 3]
    info["hat_pts"] = hat


def stone(sheet, info):
    """O-Shige's stone at the road's far edge: a flat-topped boulder travellers rest on (lit top and front, shade right)."""
    S = SEAT
    x, z, w, d, h = S["x"], S["z"], S["w"], S["d"], S["h"]
    k = kz(z)
    c = gp(x, z - d / 2, h * 0.5)
    rx_, ry_ = w / 2 * k, h * 0.55 * k
    outline = []
    for a in np.linspace(0, 2 * math.pi, 28, endpoint=False):
        wob = 1 + 0.06 * math.sin(3 * a + 1.2) + 0.04 * math.sin(5 * a)
        yy = math.sin(a)
        flat_top = 0.78 if yy < -0.55 else 1.0                       # its top worn flat (a seat)
        outline.append((c[0] + math.cos(a) * rx_ * wob, c[1] + yy * ry_ * wob * flat_top))
    outline = [(px_, min(py_, gp(x, z - d / 2)[1] + 1)) for px_, py_ in outline]
    sheet.poly(outline, STONE)
    sheet.poly([(px_, py_) for px_, py_ in outline if px_ >= c[0] + rx_ * 0.25] + [(c[0] + rx_ * 0.25, c[1] + ry_)], STONE_SHADE)
    top = [(c[0] + math.cos(a) * rx_ * 0.82, c[1] - ry_ * 0.62 + math.sin(a) * ry_ * 0.22) for a in np.linspace(0, 2 * math.pi, 20)]
    sheet.poly(top, STONE_LIT)
    V.contour(sheet, outline + [outline[0]], gp(x, z)[1], alpha=0.65)
    info["stone_box"] = [int(gp(x - w / 2, z)[0]) - 2, int(gp(x, z, h + 2)[1]) - 2, int(w * kz(z)) + 4, int(gp(x, z - d / 2)[1] - gp(x, z, h + 2)[1]) + 4]


def okitsu_roofs(sheet):
    """Okitsu, far west in the haze: a row of small roofs along its shore and, on a rise among dark trees, a temple's roof
    (a broader hipped roof with a lifted ridge). Beyond a kilometre: no contour; two flats each, pulled to the paper."""
    far_roofs(sheet, 704, 796, 306, 7, 77, h=2.2, colors=(lerp(tintw(PRUSSIAN, 0.5), PAPER, 0.35), lerp(tintw(mixp(PRUSSIAN, OCHRE, 0.3), 0.5), PAPER, 0.35)))
    # the trees on the rise
    for (cx_, cy_, r_) in ((734, 288, 9), (748, 285, 10), (762, 289, 8), (724, 292, 6)):
        sheet.ellipse(cx_, cy_, r_, r_ * 0.6, lerp(mixp(VIRIDIAN, COBALT, 0.4), PAPER, 0.40))
    # the temple roof: a broad hip roof among them
    tx, ty = 746.0, 292.0
    roof_c, roof_s = lerp(tintw(PRUSSIAN, 0.38), PAPER, 0.30), lerp(tintw(PRUSSIAN, 0.22), PAPER, 0.28)
    sheet.poly([(tx - 13, ty), (tx + 13, ty), (tx + 8, ty - 6), (tx - 8, ty - 6)], roof_c)
    sheet.poly([(tx - 15, ty + 0.5), (tx + 15, ty + 0.5), (tx + 13, ty - 1), (tx - 13, ty - 1)], roof_s)
    sheet.line([(tx - 9, ty - 6.2), (tx + 9, ty - 6.2)], roof_s, 1.0, 1.0)
    sheet.poly([(tx - 9, ty + 0.5), (tx + 9, ty + 0.5), (tx + 9, ty + 4), (tx - 9, ty + 4)], lerp(tintw(NAPLES, 0.5), PAPER, 0.2))


def details(pic, info, seed=SEED, fast=False):
    x, y = grid(SHAPE)
    crisp = pic.copy()
    paint_far(crisp, seed)
    pic[...] = lerp(pic, crisp, (0.7 * info["fuji"] * (y < HZ) * (1 - far_mask()))[..., None])
    FUJI.contour(pic, info["fuji"] * (1 - far_mask()))
    crisp = pic.copy()
    paint_oldshore(crisp, seed)
    pic[...] = lerp(pic, crisp, (0.6 * blur(info["foam"], 2.0))[..., None])
    sheet = Paper(SHAPE)
    rng = np.random.default_rng(seed + 70)
    # far: the coast of Kurasawa and Yui beyond the flank's tip: a strip of low land, its beach, a few roofs on it
    coast2 = [(186, 306), (230, 302), (280, 299), (340, 297), (400, 295), (440, 294)]
    lm = mask_poly(SHAPE, [(186, 290), (260, 289), (340, 290), (440, 291)] + list(reversed(coast2)), soft=0.7, wobble=1.0, seed=seed + 7)
    over(pic, lerp(mixp(VIRIDIAN, COBALT, 0.45), PAPER, 0.50), (lm * info["water"] * (1 - far_mask())).astype(F32))
    over(pic, tintw(NAPLES, 0.42), (mask_line(SHAPE, coast2, [1.6, 1.5, 1.3, 1.1, 0.9, 0.8], soft=0.4) * info["water"] * (1 - far_mask())).astype(F32))
    far_roofs(sheet, 222, 300, 299, 7, seed + 71, h=1.8)
    # pines scattered on the spur's slope: small dark clumps, paled by the distance, breaking the spurs' flats
    fmask = far_mask()
    for i in range(60):
        px_, py_ = rng.uniform(0, 200), rng.uniform(250, 334)
        if fmask[int(py_), int(px_)] < 0.95:
            continue
        r_ = rng.uniform(1.8, 3.2)
        sheet.ellipse(px_, py_, r_, r_ * 0.62, lerp(lerp(VIRIDIAN, PRUSSIAN, 0.55), PAPER, 0.24))
        sheet.ellipse(px_ - r_ * 0.25, py_ - r_ * 0.25, r_ * 0.55, r_ * 0.3, lerp(mixp(VIRIDIAN, VERONESE, 0.3), PAPER, 0.28))
    # small pines along the spur's skyline (a breath of line: a kilometre off)
    for (px_, py_, s_) in ((14, 240, 1.0), (40, 249, 0.9), (60, 255, 0.8), (96, 270, 0.85), (126, 285, 0.8), (158, 302, 0.7), (180, 316, 0.6)):
        c_dark, c_lit = lerp(lerp(VIRIDIAN, PRUSSIAN, 0.55), PAPER, 0.22), lerp(mixp(VIRIDIAN, VERONESE, 0.3), PAPER, 0.25)
        sheet.ellipse(px_, py_ - 2.5 * s_, 6.5 * s_, 3.6 * s_, c_dark)
        sheet.ellipse(px_ + 2.5 * s_, py_ - 5.5 * s_, 5.0 * s_, 2.8 * s_, c_dark)
        sheet.ellipse(px_ - 1.0 * s_, py_ - 4.0 * s_, 4.0 * s_, 1.6 * s_, c_lit)
    for i, (bx, by, s_) in enumerate(((388, 322, 0.55), (452, 346, 0.75), (560, 312, 0.45), (318, 370, 0.85))):
        sail_boat(sheet, bx, by, s_, seed + 72 + i, sail=(i % 2 == 0))
    okitsu_roofs(sheet)
    # the far bands' wave-curls, painted still (beyond a kilometre nothing moves at this size: style.md section 6): rows of
    # short lead-white arcs with a prussian underline, closer and smaller toward the horizon, each row offset half a wave
    wm = info["water"] * (1 - info["flank"])
    for j, row in enumerate([296, 300, 305, 311, 318, 326, 336]):
        gap = 10 + j * 4.0
        wlen = 2.0 + j * 0.8
        x0_ = (gap * 0.5) * (j % 2) + rng.uniform(0, 3)
        for xx in np.arange(x0_, 800, gap):
            yy = row + rng.normal(0, 0.6)
            if wm[int(min(yy, 599)), int(min(xx, 799))] < 0.9 or abs(xx - 694) < 30 and yy > 300:
                continue
            if rng.random() < 0.35:
                continue
            sheet.line([(xx - wlen, yy + 0.6), (xx, yy - 0.5), (xx + wlen, yy + 0.6)], tintw(CERULEAN, 0.80), 0.7, 0.55)
            sheet.line([(xx - wlen, yy + 1.4), (xx + wlen, yy + 1.4)], PRUSSIAN, 0.5, 0.20)
    # pines on the flank: dark clumps, a few small pines on its spurs
    for i in range(70):
        px_, py_ = rng.uniform(0, 310), rng.uniform(430, 492)
        if info["flank"][int(min(py_, 599)), int(min(px_, 799))] < 0.95:
            continue
        near_ = np.clip((py_ - 430) / 60.0, 0, 1)
        r_ = rng.uniform(2.2, 4.0) * (0.55 + 1.3 * near_)
        sheet.ellipse(px_, py_, r_, r_ * 0.62, lerp(VIRIDIAN, PRUSSIAN, 0.64))
        sheet.ellipse(px_ - r_ * 0.25, py_ - r_ * 0.24, r_ * 0.62, r_ * 0.34, lerp(VIRIDIAN, PRUSSIAN, 0.26) if near_ > 0.3 else lerp(mixp(VIRIDIAN, COBALT, 0.3), PAPER, 0.2))
    sheet.onto(pic)
    sheet = Paper(SHAPE)
    stone(sheet, info)
    jizo(sheet, info)
    sheet.onto(pic)
    # the bank's grass: tufts along its top, leaning left with the wind off the sea (from the right)
    gs = Sheet(SHAPE)
    for i in range(90):
        xx = rng.uniform(0, 800)
        if abs(xx - gp(JIZO["x"], JIZO["z"])[0]) < 16:
            continue
        row = bank_top(xx) + rng.uniform(1, 12)
        tuft(gs, xx, row, rng.uniform(6, 11), seed + 300 + i, lean=-0.35, n=6, width=1.0)
    for i in range(50):
        xx = rng.uniform(0, 800)
        zz = rng.uniform(-30, ROAD["z0"] + 10)
        p = gp(V.x_at(xx, gp(0, zz)[1]), zz)
        tuft(gs, xx, p[1], 10 * kz(zz) / 0.8, seed + 400 + i, lean=-0.3, n=6, width=1.1)
    gs.onto(pic)
    # a few low shrubs on the bank (dark rounded clumps, a lit top toward the sun)
    sh_ = Paper(SHAPE)
    for (sx_, w_, h_) in ((96, 26, 14), (138, 16, 9), (468, 22, 11), (560, 30, 15), (622, 18, 10), (770, 24, 12)):
        row = bank_top(sx_) + 3
        sh_.ellipse(sx_, row - h_ * 0.5, w_ * 0.5, h_ * 0.62, lerp(VIRIDIAN, PRUSSIAN, 0.42))
        sh_.ellipse(sx_ - w_ * 0.12, row - h_ * 0.72, w_ * 0.32, h_ * 0.34, mixp(VIRIDIAN, VERONESE, 0.35))
        sh_.line([(sx_ - w_ * 0.5, row - h_ * 0.55), (sx_ - w_ * 0.2, row - h_ * 1.05), (sx_ + w_ * 0.25, row - h_ * 1.0), (sx_ + w_ * 0.5, row - h_ * 0.5)], PRUSSIAN, 0.7, 0.45)
    sh_.onto(pic)
    stones = Sheet(SHAPE)
    land.stones(stones, pic, HZ, seed + 90, 40, zone=((info["road"] > 0.5) & (y > 495)), ground=info["ground"], size=(0.6, 2.2),
                tones=(tintw(PRUSSIAN, 0.78), tintw(PRUSSIAN, 0.6), tintw(PRUSSIAN, 0.42), tintw(PRUSSIAN, 0.24)))
    sc, sa = stones.done()
    over(pic, sc, sa)
    return pic


# ================================================================ the cut-outs
def cloud_cut(back, seed, fast=False):
    """Fuji's cap of cloud (on / lifted: the scene fades it): the same cloud as at Kurasawa, at this mountain's size."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    outline = cloud_cap(sheet, lines, FUJI)
    c, a = sheet.done()
    lc, la = lines.done()
    out = brushed(c, a, lc, la, tintw(CERULEAN, 0.85), seed=seed, sizes=(4, 2), keep=0.7, fast=fast)
    return out[0], out[1], outline


def pine_cut(back, seed, fast=False):
    """The bent pine on the bank's edge at the right, leaning toward Fuji (bent by the wind off the sea): a trunk that
    leans left and kinks, its foliage in flat layered pads streaming left, the lit tops toward the sun. It sways
    (fx pine-sway, rooted at its foot)."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    P_ = PINE
    k = kz(P_["z"])
    foot = gp(P_["x"], P_["z"])
    pts = [(0, 0), (-14, 110), (-46, 210), (-104, 300), (-170, 368), (-250, 420), (-330, 452)]
    trunk = [gp(P_["x"] + dx, P_["z"], dy) for dx, dy in pts]
    bark_d, bark_l = lerp(SIENNA, PRUSSIAN, 0.62), lerp(SIENNA, PRUSSIAN, 0.30)
    sheet.taper(trunk, bark_d, 30 * k, 10 * k)
    sheet.taper([(p[0] - 1.6, p[1] - 1.2) for p in trunk[:-1]], bark_l, 11 * k, 4 * k)
    for (bx_, by_, ex_, ey_) in ((-46, 210, -40, 345), (-104, 300, -84, 386), (-170, 368, -210, 418), (-250, 420, -300, 468)):
        sheet.taper([gp(P_["x"] + bx_, P_["z"], by_), gp(P_["x"] + ex_, P_["z"], ey_)], bark_d, 10 * k, 4 * k)
    # a dead stub low on the windward side (the wind strips the lower trunk)
    sheet.taper([gp(P_["x"] - 10, P_["z"], 150), gp(P_["x"] + 30, P_["z"], 190)], bark_d, 6 * k, 3 * k)
    pads = []
    rng_ = np.random.default_rng(seed)
    for (dx_, dy_, rx_, ry_) in ((-84, 392, 78, 34), (-200, 430, 86, 34), (-300, 472, 76, 30), (-380, 488, 56, 24), (-40, 350, 44, 20)):
        for j in range(3):                                           # each pad a cluster of three, the middle one highest
            ox = (j - 1) * rx_ * 0.62 + rng_.normal(0, 6)
            oy = (8 if j == 1 else -4) + rng_.normal(0, 4)
            c = gp(P_["x"] + dx_ + ox, P_["z"], dy_ + oy)
            pads.append((c[0], c[1], rx_ * k * (0.62 if j != 1 else 0.78), ry_ * k * (0.85 if j != 1 else 1.0)))
    pine_pads(sheet, lines, [], pads, seed, scale=1.0, lit_side=-1, contour=True, alpha_line=0.55, w_line=0.8)
    V.contour(lines, trunk, foot[1], warm=True, alpha=0.5)
    c, a = sheet.done()
    lc, la = lines.done()
    out = brushed(c, a, lc, la, COBALT, seed=seed, sizes=(4, 2), keep=0.55, fast=fast)
    return out[0], out[1]


def pass_cut(back, seed, fast=False, hat=None):
    """O-Shige's pass, folded in oiled paper, caught on the Jizo's little hat (on / gone): an amber packet tucked under the
    hat's brim on the left, a corner sticking up, a white edge of the paper inside showing."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    J = JIZO
    k = kz(J["z"])
    p = gp(J["x"] - 16, J["z"] - 9, J["h"] - 22)
    w, h = 22 * k, 13 * k
    ang = -0.35
    def rot(dx, dy):
        return (p[0] + dx * math.cos(ang) - dy * math.sin(ang), p[1] + dx * math.sin(ang) + dy * math.cos(ang))
    quad = [rot(-w / 2, -h / 2), rot(w / 2, -h / 2), rot(w / 2, h / 2), rot(-w / 2, h / 2)]
    sheet.poly(quad, lerp(tintw(OCHRE, 0.35), NAPLES, 0.25))
    sheet.poly([rot(-w / 2, h * 0.18), rot(w / 2, h * 0.18), rot(w / 2, h / 2), rot(-w / 2, h / 2)], lerp(OCHRE, SIENNA, 0.25))
    sheet.poly([rot(-w / 2 + 1, -h / 2 - 1.5), rot(w / 2 - 3, -h / 2 - 1.5), rot(w / 2 - 3, -h / 2), rot(-w / 2 + 1, -h / 2)], WHITE)
    lines.line(quad + [quad[0]], PRUSSIAN, 0.8, 0.8)
    lines.line([rot(-w / 2, h * 0.18), rot(w / 2, h * 0.18)], lerp(SIENNA, PRUSSIAN, 0.4), 0.6, 0.7)
    c, a = sheet.done()
    lc, la = lines.done()
    out = brushed(c, a, lc, la, OCHRE, seed=seed, sizes=(2,), keep=0.75, fast=fast)
    return out[0], out[1], quad


def front_cut(back, seed, fast=False):
    """The front plane: the foot of the cut slope behind us at the bottom edge, grass leaning with the wind, stones."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    rng = np.random.default_rng(seed)
    for i in range(34):
        xx = rng.uniform(-10, 240) if i < 18 else rng.uniform(540, 810)
        tuft(sheet, xx, 600 + rng.uniform(0, 6), rng.uniform(14, 30), seed + i, lean=-0.3, n=8, width=1.6)
    for (cx_, cy_, rx_, ry_) in ((60, 601, 34, 13), (700, 600, 30, 11), (770, 603, 40, 15)):
        sheet.ellipse(cx_, cy_, rx_, ry_, STONE)
        sheet.ellipse(cx_ - rx_ * 0.2, cy_ - ry_ * 0.35, rx_ * 0.65, ry_ * 0.45, STONE_LIT)
        lines.line([(cx_ - rx_, cy_), (cx_ - rx_ * 0.6, cy_ - ry_ * 0.85), (cx_ + rx_ * 0.4, cy_ - ry_ * 0.9), (cx_ + rx_, cy_ - ry_ * 0.2)], PRUSSIAN, 1.0, 0.8)
    c, a = sheet.done()
    lc, la = lines.done()
    out = brushed(c, a, lc, la, GRASS, seed=seed, sizes=(4, 2), keep=0.5, fast=fast)
    return out[0], out[1]


ORDER = ["cloud", "pine", "front"]


def comp_all(pic, planes, order=ORDER):
    whole = pic.copy()
    for name in order:
        c, a = planes[name][:2]
        over(whole, c, (a > 0.5).astype(F32))
    return whole


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = "fast" in sys.argv
    base, info = under()
    Image.fromarray((base * 255).astype(np.uint8)).save(OUT + "-1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.26)
    print("brushed", round(time.time() - t0, 1))
    details(pic, info, fast=fast)
    print("details", round(time.time() - t0, 1))
    planes = {}
    c, a, info["cloud_outline"] = cloud_cut(pic, 11, fast)
    planes["cloud"] = (c, a)
    planes["pine"] = pine_cut(pic, 12, fast)
    c, a, info["pass_quad"] = pass_cut(pic, 13, fast)
    planes["pass"] = (c, a)
    planes["front"] = front_cut(pic, 14, fast)
    Image.fromarray((np.clip(comp_all(pic, planes, ["cloud", "pine", "pass", "front"]), 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-all.png")
    Image.fromarray((np.clip(comp_all(pic, planes, ["pine", "front"]), 0, 1) * 255).astype(np.uint8)).save(OUT + "-3-clear.png")
    import edo_satta_layout
    with open(OUT + "/layout.json", "w") as f:
        json.dump(edo_satta_layout.layout(planes, info), f, indent=1)
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    print("back", finish(pic, OUT + "/back.png", 152))
    for name, n in (("cloud", 24), ("pine", 56), ("pass", 16), ("front", 48)):
        print(name, finish(planes[name][0], OUT + f"/{name}.png", n, planes[name][1]))
    print("done", round(time.time() - t0, 1))

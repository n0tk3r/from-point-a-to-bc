"""PAINT-21D: the Akashi shore, an afternoon about 28 April 1830 (edo-akashi), in the woodblock manner of the act's style
sheet (S/work-20-paintA/style.md): flat masses, a graded sky, one fine contour in prussian blue, few paints, the blue
leading. Keyed `edo-shore` (PAINT-21D's key, postimp_paints.py).

What is checked (S/work-21-factsB/facts-21b.md items 9-11): Akashi castle on its hill above the strait HAS NO KEEP (four
three-storey corner turrets, white); the strait about 4 km across to Awaji, long and low, its tide fast (6-7 knots);
"white sand and green pines"; Akashi octopus caught in clay pots on lines (bell-shaped pots; a way of fishing two
thousand years old); Awa pilgrims came across by boat in April 1830 (300-odd landed at Akashi on 18 April); every
pilgrim carried a ladle. The Saigoku-kaido runs behind the pines. Invented: this stretch of shore, its rocks, Heita's
boat and tub, the bearings of the view (the castle's place on the left, Awaji's on the right), the Awa boat's look.

LIGHT   The sun in the west, to the right and a little ahead, 35 degrees up (edo_akashi_kit.SUN3): faces turned to the
        right are lit; shadows fall to the left and a little toward us, flat and blue.
DEPTH   horizon 262, full 590 (persp.Camera; everything standing is drawn through it).
TONES   light: the white sand, the sky and the strait at the horizon (the paper), the castle's plaster, the tide lines.
        middle: Awaji, the near water, the road. dark: the pines, the near water's deepest band, the boats, the pots.
        The strait's hard blue and the white sand own the picture; the eye goes to the water's edge (O-Fusa, the ladle).
PLACE   edo_akashi_kit.py: the road at the bottom (z -60..140), the pines at its seaward edge, the sand down to the
        water's edge (far at the left, near at the right), the shallows with the octopus pots' lines and floats, the
        strait, Awaji; at the far left the shore curving away to the town and the castle on its hill.

  python3 edo_akashi.py fast     the composition without the brush pass (out/edo-akashi-1-under.png, -2-all.png)
  python3 edo_akashi.py          the full passes: out/edo-akashi/ (back.png, the cut-outs, the frames, layout.json)
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
from edo_akashi_kit import *
import edo_akashi_kit as K

SEED = 1830 + 28
OUT = "out/edo-akashi"
SHAPE = (H, W)

# ---------------------------------------------------------------- where things are (cm; edo_akashi_kit's PLACE)
ROAD = dict(z0=-60.0, z1=150.0)                                    # the road's near and seaward edges
PINES = [dict(x=-430.0, z=170.0, h=650.0, lean=0.26, crown=(-40.0, 590.0, 150.0), w=34.0),   # left: leans into the picture; crown (dx, y, radius)
         dict(x=424.0, z=178.0, h=640.0, lean=-0.22, crown=(40.0, 610.0, 130.0), w=32.0)]    # right: leans into the picture
POTS = dict(x0=-470.0, x1=-170.0, z0=300.0, z1=430.0)              # the octopus pots stacked in rows on the sand
HEITA_BOAT = dict(stern=(-760.0, 860.0), bow=(-250.0, 760.0), beam=62.0, side=46.0)   # drawn up, along the shore
TUB = dict(x=-150.0, z=620.0, r=34.0, h=30.0)                       # Heita's tub
ROCKS = [(430.0, 330.0, 70.0, 48.0), (520.0, 380.0, 58.0, 40.0), (600.0, 310.0, 44.0, 30.0), (360.0, 400.0, 36.0, 22.0)]   # x, z, half-width, height
LADLE = dict(x=128.0, z=810.0, L=52.0)                              # the ladle afloat among the pots' lines
FLOATS = [(-60.0, 980.0), (40.0, 900.0), (150.0, 880.0), (240.0, 820.0), (-140.0, 1180.0), (90.0, 1060.0), (300.0, 700.0)]
PBOAT_IN = dict(x=-130.0, z=1900.0, length=900.0, beam=230.0)       # the Awa boat coming in (afloat, sail down), bow to the shore
PBOAT_BEACHED = dict(x=-560.0, z=1330.0, length=900.0, beam=230.0)  # and beached, its bow on the sand (a little up the shore)
CASTLE = dict(x=-33500.0, z=74000.0)                                # the castle on its hill, far left
FAR_SHORE_ROW = 268


# ================================================================ pass 1: broad and flat
def paint_sky(seed):
    rows = [0, 40, 86, 128, 168, 204, 232, HZ + 2]
    cols = [shade(COBALT, 0.40), mixp(COBALT, ULTRA, 0.25), COBALT, mixp(COBALT, CERULEAN, 0.55), CERULEAN,
            tintw(CERULEAN, 0.52), PAPER, PAPER]
    pic = bands(SHAPE, rows, cols, soft=6.0, wobble=2.5, seed=seed, patch=0.02)
    x, y = grid(SHAPE)
    # the sun is to the right and ahead: the paper warms a breath that way
    glow(pic, tintw(NAPLES, 0.45), (np.clip((x - 420) / 380.0, 0, 1) * np.clip(1 - np.abs(y - 240) / 60.0, 0, 1) * 0.14).astype(F32))
    # one flat lens of cloud, lead white with a breath of line on its top (style.md section 3)
    for (cx, cy, rx, ry) in ((250, 92, 70, 6), (300, 86, 38, 4)):
        m = mask_ellipse(SHAPE, cx, cy, rx, ry, soft=0.8)
        over(pic, tintw(CERULEAN, 0.80), m * 0.9)
    return pic


def awaji_mask(seed):
    """Awaji across the strait: long and low, its north end at the left (a low point running into the water), its hills
    rising to the right and running off the picture. No contour (beyond a kilometre)."""
    x, y = grid(SHAPE)
    xs = np.array([212, 236, 270, 320, 380, 440, 500, 560, 620, 690, 760, 820], dtype=F32)
    tops = np.array([HZ, HZ - 4, HZ - 9, HZ - 14, HZ - 20, HZ - 24, HZ - 21, HZ - 26, HZ - 31, HZ - 28, HZ - 33, HZ - 36], dtype=F32)
    top = np.interp(x[0], xs, tops, left=HZ + 5)
    top = top + (noise((1, W), (18, 1), seed, 3)[0] - 0.5) * 3.0
    m = ((y >= top[None, :]) & (y <= HZ + 1) & (x >= 212)).astype(F32)
    return np.clip(blur(m, 0.5), 0, 1), top


def paint_awaji(pic, seed):
    m, top = awaji_mask(seed)
    x, y = grid(SHAPE)
    body = flat(AWAJI, SHAPE, seed + 1, 0.02, 80)
    # its shade: the folds facing us, one flat (the hills' north faces); the foot lost in the haze
    # its shade: the folds facing us, flat shapes running down from the ridge (the hills' north faces)
    fold = step(0.58, 0.62, noise(SHAPE, (90, 26), seed + 2, 2)) * (y > top[None, :] + 3)
    body = lerp(body, AWAJI_SHADE, (fold * 0.85)[..., None])
    body = lerp(body, PAPER, (np.clip((y - (HZ - 6)) / 7.0, 0, 1) * 0.55)[..., None])
    over(pic, body, m)
    return m


def paint_far_left(pic, seed, sheet):
    """At the far left: the shore curving away east, a strip of sand, the town's roofs under a green hill, and on the
    hill the castle: stone bases, white walls, corner turrets of three storeys; no keep (facts-21b item 9)."""
    x, y = grid(SHAPE)
    # the hill: a dark green mass rising behind the town, its top at the picture's left
    hill = [(-10, HZ + 3), (-10, HZ - 40), (18, HZ - 44), (46, HZ - 41), (78, HZ - 33), (104, HZ - 22), (128, HZ - 10), (150, HZ - 2), (160, HZ + 3)]
    mh = mask_poly(SHAPE, hill, soft=0.7, wobble=1.0, seed=seed + 5)
    over(pic, lerp(lerp(VIRIDIAN, PAPER, 0.38), COBALT, 0.12), mh)
    lit_ = mask_poly(SHAPE, [(46, HZ - 41), (78, HZ - 33), (104, HZ - 22), (128, HZ - 10), (150, HZ - 2), (120, HZ - 2), (70, HZ - 24)], soft=0.6) * mh
    over(pic, lerp(lerp(VERONESE, PAPER, 0.35), VIRIDIAN, 0.15), lit_ * 0.8)
    # the castle: its stone bases and white walls along the hill's top, two corner turrets seen (three storeys each), a
    # long low wall between; plaster white, roofs blue-grey (no keep)
    sc = 800.0 / (875.0 + CASTLE["z"])                                  # px per cm there (~0.0106)
    cx = 400 + CASTLE["x"] * sc
    base_y = HZ - 37
    stone = lerp(lerp(tintw(PRUSSIAN, 0.55), OCHRE, 0.12), PAPER, 0.25)
    # the long wall between the turrets
    sheet.poly([(cx - 26, base_y), (cx + 26, base_y + 3), (cx + 26, base_y - 3), (cx - 26, base_y - 6)], lerp(PLASTER, PAPER, 0.2))
    sheet.line([(cx - 27, base_y - 6.5), (cx + 27, base_y - 3.5)], lerp(ROOF, PAPER, 0.2), 1.2)
    turrets = [(cx - 28, base_y + 1, 1.0), (cx + 24, base_y + 4, 0.92)]
    for (tx, ty, k) in turrets:
        # the stone base (battered: wider at its foot)
        sheet.poly([(tx - 9 * k, ty + 3), (tx + 9 * k, ty + 3), (tx + 6.5 * k, ty - 5 * k), (tx - 6.5 * k, ty - 5 * k)], stone)
        # three storeys, each a white box under a blue-grey roof, smaller as they go up
        yy = ty - 5 * k
        for s, (wd, ht) in enumerate(((6.0, 4.6), (4.8, 4.0), (3.6, 3.6))):
            wd, ht = wd * k, ht * k
            sheet.poly([(tx - wd, yy), (tx + wd, yy), (tx + wd, yy - ht), (tx - wd, yy - ht)], PLASTER)
            sheet.poly([(tx + wd * 0.35, yy), (tx + wd, yy), (tx + wd, yy - ht), (tx + wd * 0.35, yy - ht)], lerp(PLASTER, CERULEAN, 0.25))   # the shade side
            yy -= ht
            sheet.poly([(tx - wd - 1.6 * k, yy + 0.8), (tx + wd + 1.6 * k, yy + 0.8), (tx + wd * 0.6, yy - 1.6 * k), (tx - wd * 0.6, yy - 1.6 * k)], ROOF)
            yy -= 1.6 * k
        sheet.line([(tx, yy), (tx, yy - 1.2)], ROOF, 0.8)
    info = {"castle_box": [int(cx - 40), int(base_y - 24), 74, 30]}
    # the town under the hill: rows of grey-blue roofs along the far shore, a few white walls; boats drawn up
    rng = np.random.default_rng(seed + 6)
    for i in range(16):
        rx = 6 + i * 9.5 + rng.normal(0, 2)
        ry = HZ - 2 + rng.normal(0, 1.5) + (i % 3) * 1.5
        wdt = 7 + rng.random() * 4
        sheet.poly([(rx - wdt / 2, ry), (rx + wdt / 2, ry), (rx + wdt * 0.32, ry - 3.2), (rx - wdt * 0.32, ry - 3.2)], lerp(ROOF, PAPER, 0.3 + 0.1 * rng.random()))
        if i % 4 == 1:
            sheet.poly([(rx - 2.5, ry + 2.8), (rx + 2.5, ry + 2.8), (rx + 2.5, ry), (rx - 2.5, ry)], lerp(PLASTER, PAPER, 0.3))
    return mh, info


def water_region():
    """Where the strait is seen: below the horizon, beyond the water's edge (the edge as the picture shows it)."""
    pts = edge_pts(90)
    poly = [(-10, HZ - 1), (W + 10, HZ - 1), (W + 10, pts[-1][1])] + list(reversed(pts)) + [(-10, pts[0][1])]
    poly = [(-10, HZ - 1), (W + 10, HZ - 1)] + [p for p in reversed(pts) if -400 < p[0] < 1300] + [(-10, FAR_SHORE_ROW)]
    return mask_poly(SHAPE, poly, soft=0.6, wobble=1.0, seed=3)


def paint_strait(pic, seed):
    """The strait in bands (style.md section 3): the paper at the horizon, cerulean, cobalt, toward ultramarine and
    prussian at the near edge: the hardest blue in the act after the sea at noon. The tide's lead-white lines lie along
    it far off (painted still: beyond a kilometre nothing moves at this size); near, the engine's waves and glints."""
    wm = water_region()
    rows = [HZ, HZ + 4, HZ + 10, HZ + 20, HZ + 36, HZ + 60, HZ + 96, HZ + 150]
    cols = [tintw(CERULEAN, 0.50), tintw(CERULEAN, 0.22), mixp(CERULEAN, COBALT, 0.45), COBALT, mixp(COBALT, ULTRA, 0.30),
            mixp(COBALT, ULTRA, 0.55), mixp(ULTRA, PRUSSIAN, 0.25), mixp(ULTRA, PRUSSIAN, 0.30)]
    wb = bands(SHAPE, rows, cols, soft=3.0, wobble=0.0, seed=seed + 20, patch=0.015)
    over(pic, wb, wm)
    return wm


def paint_ground(pic, seed, wm):
    """The sand (white, warm), its wet band at the water's edge, the road (packed earth) along the bottom, and the
    grass at the road's seaward edge."""
    x, y = grid(SHAPE)
    X, Z, below = CAM.floor_grid(SHAPE)
    ground = below * (1 - wm)
    sand = flat(SAND, SHAPE, seed + 30, 0.04, 40)
    t = np.clip((y - HZ) / (H - HZ), 0, 1)
    sand = lerp(sand, SAND_FAR, ((1 - t) ** 2.2 * 0.6)[..., None])
    over(pic, sand, ground)
    # the wet sand: a band landward of the edge, narrower far off; and the white thread of the last wave at the edge
    wet = mask_poly(SHAPE, edge_pts(90, 0.0) + list(reversed(edge_pts(90, 110.0))), soft=1.2) * ground
    over(pic, SAND_WET, (wet * 0.55).astype(F32))
    pts = edge_pts(120)
    zs = [row_z(p[1]) for p in pts]
    foam = mask_line(SHAPE, pts, [max(0.7, kz(max(z_, 1.0)) * 6.0) for z_ in zs], soft=0.5)
    over(pic, WHITE, (foam * 0.85).astype(F32))
    # the road along the bottom
    road = mask_poly(SHAPE, [gp(-3000, ROAD["z0"]), gp(3000, ROAD["z0"]), gp(3000, ROAD["z1"]), gp(-3000, ROAD["z1"])], soft=1.0, wobble=2.0, seed=seed + 31)
    earth = flat(EARTH, SHAPE, seed + 32, 0.05, 40)
    over(pic, earth, road * ground)
    # ruts along it, and the bank's lip of grass at its seaward edge (a band of veronese with viridian tufts)
    for dz in (25.0, 95.0):
        rut = mask_line(SHAPE, [gp(-3000, dz), gp(3000, dz)], max(1.0, kz(dz) * 9.0), soft=1.0)
        over(pic, lerp(EARTH, SIENNA, 0.18), (rut * road * 0.45).astype(F32))
    lip = mask_poly(SHAPE, [gp(-3000, ROAD["z1"] - 6), gp(3000, ROAD["z1"] - 6), gp(3000, ROAD["z1"] + 34), gp(-3000, ROAD["z1"] + 34)], soft=1.0, wobble=3.0, seed=seed + 33)
    over(pic, lerp(VERONESE, SAND, 0.35), lip * 0.85)
    tufts = noise(SHAPE, (6, 3), seed + 34, 3) > 0.62
    over(pic, lerp(VIRIDIAN, VERONESE, 0.3), (lip * tufts * 0.8).astype(F32))
    return ground, road


def cast_shadows(pic, ground, planes_info):
    """Every standing thing's shadow on the sand and the road: flat, blue, laid along the sun (SUN)."""
    sh = Paper(SHAPE)
    for p in PINES:
        x0, z0 = p["x"], p["z"]
        top = p["h"] * 0.82
        tx = x0 + p["lean"] * top
        sh.poly(shadow_pts([(x0 - 14, 0, z0), (x0 + 14, 0, z0), (tx + 10, top, z0), (tx - 10, top, z0)]), SAND_SHADE, 0.9)
        # (the crowns' shadows fall on the road behind us, out of the picture's interest: left out)
    # the pots, the boat, the tub, the rocks
    P_ = POTS
    sh.poly(shadow_pts([(P_["x0"], 0, P_["z0"]), (P_["x1"], 0, P_["z0"]), (P_["x1"], 60, P_["z1"]), (P_["x0"], 60, P_["z1"])]), SAND_SHADE, 0.9)
    b = HEITA_BOAT
    (sx, sz), (bx, bz) = b["stern"], b["bow"]
    sh.poly(shadow_pts([(sx, 0, sz), (bx, 0, bz), (bx, b["side"] + 20, bz), (sx, b["side"], sz)]), SAND_SHADE, 0.9)
    t = TUB
    sh.poly(shadow_pts([(t["x"] - t["r"], 0, t["z"]), (t["x"] + t["r"], 0, t["z"]), (t["x"] + t["r"], t["h"], t["z"]), (t["x"] - t["r"], t["h"], t["z"])]), SAND_SHADE, 0.9)
    for (rx, rz, rw, rh) in ROCKS:
        sh.poly(shadow_pts([(rx - rw, 0, rz), (rx + rw, 0, rz), (rx + rw * 0.4, rh, rz), (rx - rw * 0.5, rh, rz)]), SAND_SHADE, 0.85)
    c, a = sh.done()
    over(pic, c, (a * ground).astype(F32))
    return a


def under(seed=SEED):
    info = {}
    pic = paint_sky(seed)
    paint_awaji(pic, seed)
    sheet = Paper(SHAPE)
    info["hill"], far = paint_far_left(pic, seed, sheet)
    info.update(far)
    sheet.onto(pic)
    info["water"] = paint_strait(pic, seed)
    info["ground"], info["road"] = paint_ground(pic, seed, info["water"])
    info["shadow"] = cast_shadows(pic, info["ground"], {})
    land.haze(pic, HZ, PAPER, 0.30, 0.10, info["ground"])
    return np.clip(pic, 0, 1), info


# ================================================================ pass 3: the crisp things of the backdrop
def details(pic, info, seed=SEED, fast=False):
    x, y = grid(SHAPE)
    rng = np.random.default_rng(seed + 50)
    wm = info["water"]
    sheet = Paper(SHAPE)
    # the far left said again crisply (the brush softened the castle)
    s2 = Paper(SHAPE)
    paint_far_left(pic, seed, s2)
    s2.onto(pic)
    # ---- the tide's lead-white lines on the strait: long thin streaks, closer together far off, slanting a little
    # with the current (east to west), painted still (far); a few near ones are the engine's waves
    for i in range(26):
        row = HZ + 3 + (i ** 1.55) * 0.9
        if row > HZ + 70:
            break
        z_ = row_z(row)
        x0 = rng.uniform(-60, 760)
        ln = rng.uniform(60, 220) * (0.4 + 0.6 * (row - HZ) / 70.0)
        slant = rng.uniform(-0.02, 0.02)
        a_ = (x0, row)
        b_ = (x0 + ln, row + ln * slant)
        sheet.line([a_, ((a_[0] + b_[0]) / 2, row + ln * slant / 2 - 0.4), b_], WHITE, max(0.6, 1.2 * (row - HZ) / 70.0), 0.55 * float(np.clip(1.0 - (row - HZ) / 120.0, 0.3, 1)))
    # the far rows of wave-curls (beyond a kilometre: painted still), short white arcs with a prussian underline
    for i in range(140):
        row = rng.uniform(HZ + 6, HZ + 40)
        xx = rng.uniform(150, 800)
        if awaji_mask_row(xx, row):
            continue
        s_ = 1.0 + (row - HZ) / 18.0
        sheet.line([(xx - s_, row + 0.4), (xx, row - 0.5), (xx + s_, row + 0.4)], WHITE, 0.6, 0.6)
    sheet.onto(pic)
    # ---- the octopus pots' lines in the shallows: ropes lying in the water from float to float, dark, thin
    lines = Paper(SHAPE)
    ropes = [((-260.0, 1260.0), (-60.0, 980.0), (40.0, 900.0), (150.0, 880.0), (240.0, 820.0), (330.0, 700.0)),
             ((-140.0, 1180.0), (90.0, 1060.0), (240.0, 820.0))]
    for rope in ropes:
        pts = [gp(x_, z_) for x_, z_ in rope]
        lines.line(pts, lerp(SIENNA, PRUSSIAN, 0.55), 0.8, 0.75)
    lines.onto(pic)
    # ---- the pools among the rocks (sky in them): painted on the sand at the right
    pools = Paper(SHAPE)
    for (px, pz, pr) in ((470.0, 285.0, 26.0), (555.0, 340.0, 20.0), (395.0, 360.0, 16.0)):
        c = gp(px, pz)
        pools.ellipse(c[0], c[1], pr * kz(pz) * 1.6, pr * kz(pz) * 0.45, lerp(CERULEAN, WHITE, 0.25))
        pools.ellipse(c[0] + 1, c[1] + 0.5, pr * kz(pz) * 1.2, pr * kz(pz) * 0.28, lerp(COBALT, CERULEAN, 0.5))
    pools.onto(pic)
    # ---- shells and pebbles on the sand
    stones = Sheet(SHAPE)
    land.stones(stones, pic, HZ, seed + 90, 60, zone=((info["ground"] > 0.5) & (y > 420) & (info["road"] < 0.3)), ground=info["ground"], size=(0.6, 2.0),
                tones=(tintw(PRUSSIAN, 0.80), tintw(PRUSSIAN, 0.62), tintw(OCHRE, 0.5), tintw(PRUSSIAN, 0.4)))
    sc, sa = stones.done()
    over(pic, sc, sa)
    return pic


_AW = None


def awaji_mask_row(xx, row):
    global _AW
    if _AW is None:
        _AW = awaji_mask(SEED)[0]
    xi, yi = int(min(max(xx, 0), W - 1)), int(min(max(row, 0), H - 1))
    return _AW[yi, xi] > 0.3


# ================================================================ the cut-outs
def brushed(color, alpha, lc, la, under, seed=4, sizes=(6, 3, 2), keep=0.45, fast=False):
    """A cut-out, painted: flats brushed over the colour it stands in front of, its lines put back on top (the
    village's way)."""
    whole = np.maximum(alpha, la)
    ys, xs = np.where(whole > 0.02)
    if len(ys) == 0:
        return color, whole
    y0, y1, x0, x1 = max(ys.min() - 12, 0), min(ys.max() + 13, H), max(xs.min() - 12, 0), min(xs.max() + 13, W)
    flat_ = np.empty((y1 - y0, x1 - x0, 3), dtype=F32)
    flat_[...] = np.asarray(under, dtype=F32)
    over(flat_, color[y0:y1, x0:x1], alpha[y0:y1, x0:x1])
    painted = flat_ if fast else strokes(flat_, sizes=sizes, seed=seed, density=1.8, jitter=0.025, keep=keep)
    over(painted, lc[y0:y1, x0:x1], la[y0:y1, x0:x1])
    out = np.zeros(SHAPE + (3,), dtype=F32)
    out[y0:y1, x0:x1] = painted
    return out, np.clip(whole, 0, 1)


def under_of(back, a, default):
    ys, xs = np.where(a > 0.5)
    return np.median(back[ys, xs], axis=0) if len(ys) else default


def pine_cut(back, p, seed, fast=False):
    """A shore pine bent by the sea wind: a leaning, gently bent trunk of two flats (lit to the right, its shade), its
    boughs reaching out, and its crown as flat layered pads of needles (deep viridian going to prussian, the lit tops a
    step lighter, a breath of line on each pad's top): the prints' pine in our own drawing."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    rng = np.random.default_rng(seed)
    x0, z0, h, lean, w0 = p["x"], p["z"], p["h"], p["lean"], p["w"]
    k = kz(z0)
    n = 10
    spine = []
    for i in range(n + 1):
        t = i / n
        yy = h * 0.86 * t
        xx = x0 + lean * yy + 26 * math.sin(t * math.pi * 1.3) * (-1 if lean > 0 else 1)
        spine.append((xx, yy))
    wid = [w0 * (1 - 0.55 * (i / n)) * (1.25 if i == 0 else 1.0) for i in range(n + 1)]
    left = [gp(xx - w_ / 2, z0, yy) for (xx, yy), w_ in zip(spine, wid)]
    right = [gp(xx + w_ / 2, z0, yy) for (xx, yy), w_ in zip(spine, wid)]
    sheet.poly(left + list(reversed(right)), BARK_SHADE)
    litside = [gp(xx + w_ * 0.08, z0, yy) for (xx, yy), w_ in zip(spine, wid)]
    sheet.poly(litside + list(reversed(right)), BARK)
    for i in range(1, n):
        (xx, yy), w_ = spine[i], wid[i]
        for q in range(2):
            y_ = yy + rng.uniform(-20, 20)
            lines.line([gp(xx - w_ * 0.45, z0, y_), gp(xx + w_ * rng.uniform(-0.1, 0.3), z0, y_ + rng.uniform(-4, 4))], lerp(BARK_SHADE, PRUSSIAN, 0.35), 0.9, 0.6)
    contour(lines, left, row=gp(x0, z0)[1], warm=True)
    contour(lines, right, row=gp(x0, z0)[1], warm=True)
    # the crown: flat masses of needles in two or three tiers, the boughs out to them (the boughs under the masses)
    cx_, cy_, cr = p["crown"]
    top = spine[-1]
    pads = []
    for j in range(7):
        side = -1 if j % 2 == 0 else 1
        tier = j // 3
        px_ = top[0] + cx_ + side * cr * (0.45 + 0.6 * rng.random()) * (1.0 + 0.25 * tier)
        py_ = cy_ - tier * cr * 0.55 + rng.normal(0, 14)
        pads.append((px_, py_, cr * (0.42 + 0.22 * rng.random())))
    pads.append((top[0] + cx_ * 0.5, cy_ + cr * 0.32, cr * 0.5))
    for (px_, py_, pr) in pads:
        a_ = gp(top[0] + (px_ - top[0]) * 0.1, z0, min(top[1], py_ + 10))
        b_ = gp(px_, z0, py_ - pr * 0.08)
        sheet.line([a_, b_], BARK_SHADE, max(1.6, 9 * k))
    for (px_, py_, pr) in sorted(pads, key=lambda q: -q[1]):
        c = gp(px_, z0, py_)
        rx, ry = pr * k * 1.3, pr * k * 0.34
        # an irregular flat mass: a lens whose edge wanders (a few lobes), dark under, the paint, a lit top
        lobes = []
        nl = 22
        for q in range(nl):
            t = 2 * math.pi * q / nl
            rr = 1.0 + 0.10 * math.sin(3 * t + px_) + 0.07 * math.sin(7 * t + py_) + rng.normal(0, 0.03)
            lobes.append((c[0] + math.cos(t) * rx * rr, c[1] + math.sin(t) * ry * rr * (1.25 if math.sin(t) > 0 else 1.0)))
        sheet.poly(lobes, PINE_DEEP)
        sheet.poly([(c[0] + (x_ - c[0]) * 0.94 + rx * 0.05, c[1] + (y_ - c[1]) * 0.78 - ry * 0.28) for x_, y_ in lobes], PINE)
        sheet.poly([(c[0] + (x_ - c[0]) * 0.62 + rx * 0.22, c[1] + (y_ - c[1]) * 0.42 - ry * 0.55) for x_, y_ in lobes], PINE_LIT)
        for q in range(max(3, int(rx / 2.6))):
            u = -1 + 2 * (q + 0.5) / max(3, int(rx / 2.6))
            xx = c[0] + u * rx * 0.9
            yy = c[1] + ry * 1.2 * math.sqrt(max(0.0, 1 - u * u)) * 0.92
            lines.line([(xx, yy - 2.0), (xx + 1.0, yy + 2.2)], PINE_DEEP, 0.9, 0.85)
        lines.line([lobes[i] for i in range(nl // 2, nl)] + [lobes[0]], PRUSSIAN, 0.8, 0.4)
    c, a = sheet.done()
    lc, la = lines.done()
    return brushed(c, a, lc, la, under_of(back, a, PINE), seed=seed, keep=0.5, fast=fast)


def bell(sheet, lines, x, z, y=0.0, size=1.0, lit_k=1.0):
    """One octopus pot standing mouth-down on the sand: a clay bell (narrow round top with the rope's hole, the body
    widening to the rim): the lit flat on the right, the shade flat; a dark ring at the rim."""
    k = kz(z)
    b0 = gp(x, z, y)
    b1 = gp(x, z, y + 30 * size)
    w0, w1 = 15 * size * k, 10.5 * size * k
    hh = b0[1] - b1[1]
    body = [(b0[0] - w0, b0[1]), (b0[0] + w0, b0[1]), (b0[0] + w0 * 0.9, b0[1] - hh * 0.45), (b1[0] + w1, b1[1] + hh * 0.05),
            (b1[0] + w1 * 0.7, b1[1] - w1 * 0.45), (b1[0], b1[1] - w1 * 0.62), (b1[0] - w1 * 0.7, b1[1] - w1 * 0.45), (b1[0] - w1, b1[1] + hh * 0.05), (b0[0] - w0 * 0.9, b0[1] - hh * 0.45)]
    sheet.poly(body, CLAY_SHADE)
    lit_ = [(b0[0] + w0 * 0.05, b0[1]), (b0[0] + w0, b0[1]), (b0[0] + w0 * 0.9, b0[1] - hh * 0.45), (b1[0] + w1, b1[1] + hh * 0.05),
            (b1[0] + w1 * 0.7, b1[1] - w1 * 0.45), (b1[0] + w1 * 0.05, b1[1] - w1 * 0.62)]
    sheet.poly(lit_, lerp(CLAY_SHADE, CLAY, lit_k))
    sheet.poly([(b0[0] - w0, b0[1]), (b0[0] + w0, b0[1]), (b0[0] + w0 * 0.97, b0[1] - 2.2 * k * 3), (b0[0] - w0 * 0.97, b0[1] - 2.2 * k * 3)], lerp(SIENNA, PRUSSIAN, 0.45))
    contour(lines, body + [body[0]], b0[1])
    return b0, b1


def pots_cut(back, seed, fast=False):
    """The octopus pots on the sand: clay bells, mouth down, in rows (the far row first), some stacked two high; and two
    lying on their sides at the front, their dark mouths toward us, a loop of rope at the neck."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    rng = np.random.default_rng(seed)
    P_ = POTS
    rows = 4
    for r in range(rows):
        z = P_["z1"] - r * (P_["z1"] - P_["z0"]) / (rows - 1)
        n = 7
        for i in range(n):
            x = P_["x0"] + 10 + (i + 0.5 * (r % 2)) * (P_["x1"] - P_["x0"] - 20) / (n - 0.5) + rng.normal(0, 3)
            bell(sheet, lines, x, z + rng.normal(0, 4))
            if (i + r) % 3 == 0:
                bell(sheet, lines, x + rng.normal(0, 1.5), z, y=21.0, size=0.92)
    for (x, z) in ((P_["x0"] + 40, P_["z0"] - 46), (P_["x0"] + 105, P_["z0"] - 60)):
        k = kz(z)
        c = gp(x, z, 13)
        rw, rh = 14 * k, 13 * k
        sheet.ellipse(c[0], c[1], rw * 1.4, rh, CLAY_SHADE)
        sheet.ellipse(c[0] + rw * 0.25, c[1] - rh * 0.25, rw * 1.0, rh * 0.6, CLAY)
        sheet.ellipse(c[0] - rw * 0.75, c[1] + rh * 0.05, rw * 0.5, rh * 0.8, lerp(SIENNA, PRUSSIAN, 0.7))
        lines.line([(c[0] + rw * 0.6, c[1] - rh), (c[0] + rw * 0.9, c[1] - rh * 1.4), (c[0] + rw * 1.25, c[1] - rh * 1.0)], lerp(OCHRE, SIENNA, 0.4), 1.0, 0.9)
        lines.line([(c[0] - rw * 1.4, c[1]), (c[0] - rw * 0.9, c[1] - rh), (c[0] + rw * 0.9, c[1] - rh), (c[0] + rw * 1.4, c[1])], PRUSSIAN, contour_w(c[1]), 0.6)
    c, a = sheet.done()
    lc, la = lines.done()
    return brushed(c, a, lc, la, under_of(back, a, SAND), seed=seed, fast=fast)


def heitaboat_cut(back, seed, fast=False):
    """Heita's small fishing boat drawn up on the sand along the shore: the near side one lit flat (the sun is to the
    right: the bow is lit), the inside dark over the gunwale, a thwart or two, the stem; a pole and a net in her."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    b = HEITA_BOAT
    (sx, sz), (bx, bz) = b["stern"], b["bow"]
    L = math.hypot(bx - sx, bz - sz)
    ux, uz = (bx - sx) / L, (bz - sz) / L
    nx, nz = -uz, ux                                           # toward us (the near side)
    if nz > 0:
        nx, nz = -nx, -nz
    beam, side = b["beam"], b["side"]
    n = 14
    near_g, far_g, near_c = [], [], []
    for i in range(n + 1):
        u = i / n
        cx_, cz_ = sx + ux * L * u, sz + uz * L * u
        hw = beam * (0.55 + 0.45 * math.sin(math.pi * min(1.0, u * 1.1)) ** 0.7) if u < 0.88 else beam * (1.0 - (u - 0.88) / 0.12) ** 0.6 * 0.9 + 3
        sheer = side + 5 * (1 - u) ** 2 + 30 * max(0.0, u - 0.6) ** 1.6 / 0.4 ** 1.6
        near_g.append((cx_ + nx * hw, sheer, cz_ + nz * hw))
        far_g.append((cx_ - nx * hw, sheer, cz_ - nz * hw))
        near_c.append((cx_ + nx * hw * 0.85, 4.0, cz_ + nz * hw * 0.85))
    G = lambda q: gp(q[0], q[2], q[1])
    hull_lit = lerp(tintw(OCHRE, 0.18), PRUSSIAN, 0.10)
    hull_sh = lerp(SIENNA, PRUSSIAN, 0.40)
    inside = lerp(SIENNA, PRUSSIAN, 0.60)
    sheet.poly([G(q) for q in far_g] + [G(q) for q in reversed(near_g)], inside)
    # a pole and a coil of net lying in her
    mid = near_g[n // 2]
    lines.line([G((sx + ux * 30, side + 6, sz + uz * 30)), G((bx - ux * 40, side + 14, bz - uz * 40))], WOOD_LIT, max(1.0, 4 * kz(sz)), 1.0)
    c = G((mid[0] - nx * beam * 0.6, side - 4, mid[2] - nz * beam * 0.6))
    sheet.ellipse(c[0], c[1], 18 * kz(mid[2]), 5 * kz(mid[2]), lerp(SIENNA, PRUSSIAN, 0.35))
    for u in (0.32, 0.6):
        i = int(u * n)
        lines.line([G((near_g[i][0], near_g[i][1] - 6, near_g[i][2])), G((far_g[i][0], far_g[i][1] - 6, far_g[i][2]))], WOOD_SHADE, max(0.9, 6 * kz(near_g[i][2])), 1.0)
    sheet.poly([G(q) for q in near_g] + [G(q) for q in reversed(near_c)], hull_lit)
    # the bow's planks turning (in the sun: it faces right)
    tip = (bx + ux * 12, 0.0, bz + uz * 12)
    bow_top = (tip[0], side + 36, tip[2])
    sheet.poly([G(near_g[-2]), G(bow_top), G(far_g[-2]), G(far_g[-1]), G(near_g[-1])], lerp(hull_lit, WHITE, 0.15))
    lines.line([G((tip[0], 2, tip[2])), G(bow_top)], hull_sh, max(1.2, 8 * kz(tip[2])), 1.0)
    for v in (0.45, 0.75):
        lines.line([G((a_[0], a_[1] + (c_[1] - a_[1]) * v, a_[2])) for a_, c_ in zip(near_g, near_c)], PRUSSIAN, 0.6, 0.4)
    r0 = G(near_c[-1])[1]
    contour(lines, [G(q) for q in near_g] + [G(bow_top)], r0, warm=True)
    contour(lines, [G(q) for q in near_c] + [G((tip[0], 2, tip[2]))], r0)
    contour(lines, [G(q) for q in far_g], r0, alpha=0.5)
    cc, a = sheet.done()
    lc, la = lines.done()
    return brushed(cc, a, lc, la, under_of(back, a, SAND), seed=seed, fast=fast)


def tub_cut(back, seed, fast=False):
    """Heita's tub: a shallow wooden tub, hooped, seawater in it (for the catch)."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    t = TUB
    k = kz(t["z"])
    b0 = gp(t["x"], t["z"], 0)
    b1 = gp(t["x"], t["z"], t["h"])
    rx = t["r"] * k
    sheet.poly([(b0[0] - rx, b0[1] - rx * 0.12), (b0[0] + rx, b0[1] - rx * 0.12), (b1[0] + rx * 1.04, b1[1]), (b1[0] - rx * 1.04, b1[1])], WOOD_SHADE)
    sheet.poly([(b0[0] + rx * 0.2, b0[1] - rx * 0.12), (b0[0] + rx, b0[1] - rx * 0.12), (b1[0] + rx * 1.04, b1[1]), (b1[0] + rx * 0.2, b1[1])], WOOD_LIT)
    sheet.ellipse(b0[0], b0[1] - rx * 0.12, rx, rx * 0.26, WOOD_SHADE)
    sheet.ellipse(b1[0], b1[1], rx * 1.04, rx * 0.28, lerp(SIENNA, PRUSSIAN, 0.5))
    sheet.ellipse(b1[0], b1[1] + 0.6, rx * 0.88, rx * 0.2, lerp(COBALT, CERULEAN, 0.4))
    for v in (0.3, 0.75):
        yy = b0[1] + (b1[1] - b0[1]) * v
        lines.line([(b0[0] - rx * 1.02, yy), (b0[0], yy + rx * 0.18), (b0[0] + rx * 1.02, yy)], lerp(SIENNA, PRUSSIAN, 0.6), max(1.0, 3 * k), 0.9)
    contour(lines, [(b0[0] - rx, b0[1] - rx * 0.12), (b1[0] - rx * 1.04, b1[1]), (b1[0] + rx * 1.04, b1[1]), (b0[0] + rx, b0[1] - rx * 0.12)], b0[1])
    c, a = sheet.done()
    lc, la = lines.done()
    return brushed(c, a, lc, la, under_of(back, a, SAND), seed=seed, fast=fast)


def rocks_cut(back, seed, fast=False):
    """The rocks at the right, at the water's edge: grey-blue stone in two flats (lit to the right), wet and dark at
    their feet, weed at the waterline; the pools among them are the backdrop's."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    rng = np.random.default_rng(seed)
    for (rx, rz, rw, rh) in sorted(ROCKS, key=lambda r: -r[1]):
        k = kz(rz)
        b = gp(rx, rz)
        w_, h_ = rw * k, rh * k
        n = 9
        pts = []
        for i in range(n + 1):
            a_ = math.pi * i / n
            rr = 1.0 + rng.normal(0, 0.10)
            pts.append((b[0] - math.cos(a_) * w_ * rr, b[1] - math.sin(a_) * h_ * rr * (1.0 + 0.2 * math.sin(a_ * 2.0))))
        sheet.poly(pts, STONE_SHADE)
        litp = [p for p in pts if p[0] >= b[0] - w_ * 0.15]
        sheet.poly([(b[0] - w_ * 0.15, b[1])] + litp, STONE)
        # the wet foot and the weed
        sheet.poly([(b[0] - w_ * 1.02, b[1]), (b[0] + w_ * 1.02, b[1]), (b[0] + w_ * 0.98, b[1] - h_ * 0.22), (b[0] - w_ * 0.98, b[1] - h_ * 0.25)], lerp(STONE_SHADE, PRUSSIAN, 0.35))
        for q in range(int(w_ / 3)):
            xx = b[0] - w_ + q * 3 + rng.uniform(0, 2)
            lines.line([(xx, b[1] - h_ * 0.2), (xx + 0.5, b[1] - h_ * 0.05)], lerp(VIRIDIAN, OCHRE, 0.3), 0.9, 0.8)
        # a crack or two
        lines.line([(b[0] - w_ * 0.2, b[1] - h_ * 0.9), (b[0] - w_ * 0.05, b[1] - h_ * 0.4)], lerp(STONE_SHADE, PRUSSIAN, 0.4), 0.7, 0.6)
        contour(lines, pts, b[1])
    c, a = sheet.done()
    lc, la = lines.done()
    return brushed(c, a, lc, la, under_of(back, a, SAND), seed=seed, fast=fast)


def ladle_cut(back, seed, fast=False):
    """The pilgrim's ladle afloat among the pots' lines: a wooden dipper, its bowl up (room in it for the octopus: the
    sprite is PEOPLE-21B's), its long handle lying on the water."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    L = LADLE
    x, z = L["x"], L["z"]
    k = kz(z)
    c = gp(x, z, 2)
    rb = 10.5 * k
    # the handle: lying on the water, pointing to the right and away
    h0 = (c[0] + rb * 0.9, c[1] - rb * 0.1)
    h1 = gp(x + L["L"] * 0.85, z + 18, 1)
    lines.line([h0, h1], tintw(OCHRE, 0.35), max(1.2, 2.6 * k * 1.4), 1.0)
    lines.line([(h0[0], h0[1] + 0.6), (h1[0], h1[1] + 0.6)], WOOD_SHADE, 0.6, 0.6)
    # the bowl: a little wooden cup, its rim an ellipse, its inside dark-wet
    sheet.ellipse(c[0], c[1], rb, rb * 0.62, lerp(tintw(OCHRE, 0.25), SIENNA, 0.2))
    sheet.ellipse(c[0], c[1] - rb * 0.18, rb * 0.84, rb * 0.36, lerp(SIENNA, PRUSSIAN, 0.45))
    # a ring of water round it
    lines.line([(c[0] - rb * 1.4, c[1] + rb * 0.45), (c[0], c[1] + rb * 0.75), (c[0] + rb * 1.4, c[1] + rb * 0.45)], tintw(CERULEAN, 0.6), 0.8, 0.7)
    contour(lines, [(c[0] - rb, c[1]), (c[0], c[1] - rb * 0.62), (c[0] + rb, c[1])], c[1])
    cc, a = sheet.done()
    lc, la = lines.done()
    info = {"bowl": [int(round(c[0])), int(round(c[1] - rb * 0.18))], "rb": rb}
    out = brushed(cc, a, lc, la, under_of(back, a, COBALT), seed=seed, sizes=(3, 2), keep=0.6, fast=fast)
    return out, info


def floats_cut(back, seed, fast=False):
    """The floats of the pots' lines: little round floats of wood bobbing in the shallows."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    for (x, z) in FLOATS:
        k = kz(z)
        c = gp(x, z, 3)
        r = max(1.6, 6.0 * k)
        sheet.ellipse(c[0], c[1], r, r * 0.7, tintw(OCHRE, 0.25))
        sheet.ellipse(c[0] + r * 0.2, c[1] - r * 0.2, r * 0.55, r * 0.35, tintw(NAPLES, 0.4))
        lines.line([(c[0] - r * 1.3, c[1] + r * 0.6), (c[0] + r * 1.3, c[1] + r * 0.6)], tintw(CERULEAN, 0.55), 0.7, 0.6)
    cc, a = sheet.done()
    lc, la = lines.done()
    return brushed(cc, a, lc, la, COBALT, seed=seed, sizes=(2,), keep=0.7, fast=fast)


def pilgrimboat_cut(back, b, seed, beached=False, fast=False):
    """The Awa boat, bow to the shore, sail down: a small wooden passenger boat, the near (left) side in the half light
    and the right side lit (the sun to the right), the mast stepped and bare, the mat sail furled along its yard lowered
    across the thwarts, bundles aboard. Coming in, she sits in the water: her sides are drawn from the waterline up (a
    thread of white along it); beached, her bow is up on the sand, her stern still in the shallows."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    x0, z0, L, beam = b["x"], b["z"], b["length"], b["beam"]
    n = 12
    free = 52.0 if beached else 36.0                           # freeboard amidships above the chine (less in the water)
    gun_l, gun_r, ch_l, ch_r = [], [], [], []
    for i in range(n + 1):
        u = i / n
        z = z0 + L * u
        hw = beam / 2 * (0.22 + 0.78 * math.sin(math.pi * min(1.0, 0.12 + u * 0.95)) ** 0.6)
        sheer = free + 46 * (1 - u) ** 2.2 + 26 * u ** 3
        gun_l.append((x0 - hw, sheer, z))
        gun_r.append((x0 + hw, sheer, z))
        ch_l.append((x0 - hw * 0.78, 0.0, z))
        ch_r.append((x0 + hw * 0.78, 0.0, z))
    G = lambda q: gp(q[0], q[2], q[1])
    hull_lit = lerp(tintw(OCHRE, 0.22), PRUSSIAN, 0.06)
    hull_sh = lerp(SIENNA, PRUSSIAN, 0.38)
    inside = lerp(SIENNA, PRUSSIAN, 0.58)
    # the inside, seen over the gunwales (we look down a little)
    sheet.poly([G(q) for q in gun_l] + [G(q) for q in reversed(gun_r)], inside)
    for u in (0.22, 0.45, 0.7):
        i = int(u * n)
        lines.line([G((gun_l[i][0], gun_l[i][1] - 6, gun_l[i][2])), G((gun_r[i][0], gun_r[i][1] - 6, gun_r[i][2]))], WOOD_SHADE, max(0.9, 6 * kz(gun_l[i][2])), 1.0)
    mi = int(0.4 * n)
    mz = gun_l[mi][2]
    mast_b = (x0, gun_l[mi][1] - 10, mz)
    mast_t = (x0 + 6, gun_l[mi][1] + 480, mz + 10)
    lines.line([G(mast_b), G(mast_t)], lerp(SIENNA, PRUSSIAN, 0.3), max(1.0, 7 * kz(mz)), 1.0)
    yard = [G((x0 - beam * 0.9, gun_l[mi][1] + 4, mz + 60)), G((x0 + beam * 0.9, gun_l[mi][1] + 4, mz + 40))]
    sheet.line(yard, lerp(tintw(OCHRE, 0.45), SIENNA, 0.15), max(2.0, 26 * kz(mz)))
    lines.line([(yard[0][0], yard[0][1] + 1), (yard[1][0], yard[1][1] + 1)], WOOD_SHADE, 0.7, 0.6)
    for (u, d) in ((0.58, -0.4), (0.62, 0.3), (0.82, 0.0)):
        i = int(u * n)
        c = G((x0 + d * beam * 0.4, gun_l[i][1] - 4, gun_l[i][2]))
        sheet.ellipse(c[0], c[1], 18 * kz(gun_l[i][2]), 12 * kz(gun_l[i][2]), lerp(tintw(PRUSSIAN, 0.5), OCHRE, 0.2))
    # the sides: the left in the half light, the right lit; the bow's planks between them
    sheet.poly([G(q) for q in gun_l] + [G(q) for q in reversed(ch_l)], hull_sh)
    sheet.poly([G(q) for q in gun_r] + [G(q) for q in reversed(ch_r)], hull_lit)
    stem_top = (x0, gun_l[0][1] + 16, z0 - 16)
    stem_foot = (x0, 0.0, z0 - 6)
    sheet.poly([G(gun_l[0]), G(stem_top), G(gun_r[0]), G(ch_r[0]), G(stem_foot), G(ch_l[0])], lerp(hull_lit, hull_sh, 0.45))
    lines.line([G(stem_foot), G(stem_top)], hull_sh, max(1.0, 9 * kz(z0)), 1.0)
    for v in (0.4, 0.75):
        lines.line([G((g_[0] + (c_[0] - g_[0]) * v, g_[1] * (1 - v), g_[2])) for g_, c_ in zip(gun_r, ch_r)], PRUSSIAN, 0.6, 0.35)
    r0 = G(stem_foot)[1]
    contour(lines, [G(q) for q in gun_l] + [G(stem_top)], r0)
    contour(lines, [G(stem_top)] + [G(q) for q in gun_r], r0, warm=True)
    if not beached:
        # the waterline: a thread of white along her sides where they meet the water
        lines.line([G(q) for q in reversed(ch_l[:8])] + [G(stem_foot)] + [G(q) for q in ch_r[:8]], WHITE, max(0.8, 3.0 * kz(z0)), 0.85)
    else:
        contour(lines, [G(q) for q in reversed(ch_l[:6])] + [G(stem_foot)] + [G(q) for q in ch_r[:6]], r0, alpha=0.6)
    cc, a = sheet.done()
    lc, la = lines.done()
    return brushed(cc, a, lc, la, under_of(back, a, COBALT), seed=seed, sizes=(4, 2), keep=0.5, fast=fast)


def front_cut(back, seed, fast=False):
    """The front plane: a tuft of shore grass at the road's edge, bottom right, and a pine root at the left."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    rng = np.random.default_rng(seed)
    for (cx_, cy_, n) in ((770, 600, 14), (30, 600, 10)):
        for i in range(n):
            a_ = -math.pi / 2 + rng.uniform(-0.7, 0.7)
            ln = rng.uniform(16, 38)
            x0 = cx_ + rng.uniform(-26, 26)
            lines.line([(x0, cy_), (x0 + math.cos(a_) * ln, cy_ + math.sin(a_) * ln)], lerp(VIRIDIAN, VERONESE, rng.uniform(0.1, 0.6)), rng.uniform(1.2, 2.4), 1.0)
    c, a = sheet.done()
    lc, la = lines.done()
    return brushed(c, a, lc, la, SAND, seed=seed, keep=0.6, fast=fast)


# ================================================================ the numbers
def layout(planes, info):
    import edo_akashi_layout as L
    return L.layout(planes, info)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


ORDER = ["floats", "ladle", "pilgrimboat", "heitaboat", "tub", "pots", "rocks", "pine-l", "pine-r", "front"]
COLORS = {"floats": 24, "ladle": 32, "pilgrimboat": 48, "pilgrimboat-beached": 48, "heitaboat": 56, "tub": 32, "pots": 56, "rocks": 48,
          "pine-l": 64, "pine-r": 64, "front": 32}


def boat_frame(planes, info):
    """The Awa boat for its approach (a flyer that stops): the coming-in cut-out cropped to its own box, with the point
    under its bow (where it meets the water) as its foot; drawn at the size it is at its stop, grown and shrunk from
    there by the depth (sizeAt its foot's row)."""
    c, a = planes["pilgrimboat"]
    ys, xs = np.where(a > 0.5)
    x0, x1, y0, y1 = xs.min() - 2, xs.max() + 3, ys.min() - 2, ys.max() + 3
    crop = np.dstack([c[y0:y1, x0:x1], (a[y0:y1, x0:x1] > 0.5).astype(F32)])
    foot = gp(PBOAT_IN["x"], PBOAT_IN["z"] - 6, 0)
    return crop, (int(round(foot[0] - x0)), int(round(foot[1] - y0))), [int(x0), int(y0), int(x1 - x0), int(y1 - y0)], [int(round(foot[0])), int(round(foot[1]))]


def relayout():
    """layout.json again from the painted files in out/edo-akashi/ (their alphas) and the placings, without painting."""
    planes = {}
    for name in ORDER + ["pilgrimboat-beached"]:
        a = np.asarray(Image.open(f"{OUT}/{name}.png").convert("RGBA"), np.float32)[..., 3] / 255.0
        planes[name] = (None, a)
    info = {}
    sheet = Paper(SHAPE)
    _, far = paint_far_left(np.zeros(SHAPE + (3,), np.float32), SEED, sheet)
    info.update(far)
    k = kz(LADLE["z"])
    c = gp(LADLE["x"], LADLE["z"], 2)
    rb = 10.5 * k
    info["ladle"] = {"bowl": [int(round(c[0])), int(round(c[1] - rb * 0.18))], "rb": rb}
    ys, xs = np.where(planes["pilgrimboat"][1] > 0.5)
    x0, y0 = xs.min() - 2, ys.min() - 2
    foot = gp(PBOAT_IN["x"], PBOAT_IN["z"] - 6, 0)
    info["boat_frame"] = {"foot": [int(round(foot[0] - x0)), int(round(foot[1] - y0))], "box": [int(x0), int(y0), int(xs.max() + 3 - x0), int(ys.max() + 3 - y0)],
                          "at": [int(round(foot[0])), int(round(foot[1]))]}
    with open(OUT + "/layout.json", "w") as f:
        json.dump(layout(planes, info), f, indent=1)
    print("layout.json written")


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    if "relayout" in sys.argv:
        relayout()
        sys.exit()
    fast = "fast" in sys.argv
    base, info = under()
    Image.fromarray((base * 255).astype(np.uint8)).save(OUT + "-1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.26)
    print("brushed", round(time.time() - t0, 1))
    details(pic, info, fast=fast)
    print("details", round(time.time() - t0, 1))
    planes = {}
    planes["pilgrimboat"] = pilgrimboat_cut(pic, PBOAT_IN, 11, beached=False, fast=fast)
    planes["pilgrimboat-beached"] = pilgrimboat_cut(pic, PBOAT_BEACHED, 12, beached=True, fast=fast)
    planes["floats"] = floats_cut(pic, 13, fast)
    planes["ladle"], info["ladle"] = ladle_cut(pic, 14, fast)
    planes["heitaboat"] = heitaboat_cut(pic, 15, fast)
    planes["tub"] = tub_cut(pic, 16, fast)
    planes["pots"] = pots_cut(pic, 17, fast)
    planes["rocks"] = rocks_cut(pic, 18, fast)
    planes["pine-l"] = pine_cut(pic, PINES[0], 19, fast)
    planes["pine-r"] = pine_cut(pic, PINES[1], 20, fast)
    planes["front"] = front_cut(pic, 21, fast)
    whole = pic.copy()
    for name in ORDER:
        c, a = planes[name]
        over(whole, c, (a > 0.5).astype(F32))
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-all.png")
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    crop, foot, box, at = boat_frame(planes, info)
    info["boat_frame"] = {"foot": list(foot), "box": box, "at": at}
    lay_ = layout(planes, info)
    with open(OUT + "/layout.json", "w") as f:
        json.dump(lay_, f, indent=1)
    print("back", finish(pic, OUT + "/back.png", 152))
    for name in ORDER + ["pilgrimboat-beached"]:
        print(name, finish(planes[name][0], OUT + f"/{name}.png", COLORS[name], planes[name][1]))
    # the boat's frame: an RGBA picture (keyed colour by colour as a frame)
    cimg = np.clip(np.round(crop * 255), 0, 255).astype(np.uint8)
    Image.fromarray(cimg, "RGBA").save(OUT + "/boat-1.png", optimize=True)
    comp = Image.open(OUT + "/back.png").convert("RGBA")
    for name in ORDER:
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(OUT + "-comp.png")
    comp = Image.open(OUT + "/back.png").convert("RGBA")
    for name in [n if n != "pilgrimboat" else "pilgrimboat-beached" for n in ORDER]:
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(OUT + "-comp-beached.png")
    print("done", round(time.time() - t0, 1))

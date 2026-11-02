"""PAINT-21A: Nishikurasawa, the rest village at the eastern foot of the Satta Pass, about 8 April 1830, morning
(edo-kurasawa). In the woodblock manner of the act's style sheet (S/work-20-paintA/style.md): flat masses, a graded sky,
one fine contour in prussian blue, few paints, the blue leading; keyed at 50 in `edo-morning` (PAINT-20A's key).

LIGHT   The act's sun: in the east, behind us and to the left, 30 degrees up (edo_kurasawa_kit.SUN3): faces turned to us
        and to the left are lit, shadows fall to the right and away, flat and blue.
DEPTH   horizon 300, full 590 (persp.Camera, as Yui: eye 317 cm, Z0 875, focal 800).
TONES   light: Fuji's snow and its cap of cloud, the paper at the horizon, the sunlit road. middle: the bay, the sky, the
        thatch, the hackberry's new leaves. dark: Mount Satta and its pines at the right, the teahouse's open front, the
        palanquin, the trunks, the contour. Fuji owns the sky; the teahouse (left, its smoke and its sign) and the mound
        with its palanquin (right) are where the eye goes next; the road west climbs out at the right.
PLACE   We stand on the Tokaido at Nishikurasawa looking across the road to the bay (the act's compass, as at Yui: the bay
        in front, Fuji across it, the way west to the right). The road runs across the picture (z 40 to 560) from the
        left edge (from Yui) to the right edge, where it starts up the mountain. Beyond the road, on the bay's side, a
        ledge at the cliff's foot: at the left O-Kuni's teahouse, its open front to the road (a bench under the eaves, the
        grill with turban shells out front, a signboard of our own, the matted room open behind with the bay in its
        back), then the low wall over the shore and the bay, the far coast curving back toward Yui and under Fuji; at the
        right, the rest place before the 40th distance mound, its hackberry spreading over it, the bearers' palanquin set
        down by it; behind, Mount Satta, dark, the cliff road cut across its face.

  python3 edo_kurasawa.py fast     the composition without the brush pass (out/edo-kurasawa-1-under.png, -2-all.png)
  python3 edo_kurasawa.py          the full passes: out/edo-kurasawa/ (back.png, the cut-outs, layout.json)
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

SEED = 1831
OUT = "out/edo-kurasawa"
SHAPE = (H, W)
HZ, FULL = 300, 590
V = View(HZ, FULL, sun=(1.15, 0.85))                              # the sun a little more behind us than at Yui (an hour on)
gp, kz = V.gp, V.kz

# ---------------------------------------------------------------- where things are (cm; see the module's PLACE)
ROAD = dict(z0=40.0, z1=560.0)                                     # the Tokaido across the picture
TEA = dict(x0=-1150.0, x1=-250.0, z0=640.0, z1=1140.0, eave=215.0, over=95.0, ridge=545.0, floor=48.0, lintel=180.0,
           posts=(-1000.0, -720.0, -440.0, -250.0), door=(-440.0, -250.0))
BENCH = dict(x0=-722.0, x1=-470.0, z0=588.0, z1=632.0, h=44.0)
LEDGE = [(-1600.0, 860.0), (-300.0, 900.0), (100.0, 950.0), (300.0, 1010.0), (430.0, 1120.0), (520.0, 1350.0), (600.0, 1700.0),
         (3000.0, 1700.0)]                                         # the ledge's seaward edge (the wall's top), then the mountain's foot
RAMP_FAR = [(646, 476), (686, 463), (726, 447), (766, 429), (812, 409)]    # the climb: the road's far edge rising to the right edge
RAMP_NEAR = [(812, 441), (768, 460), (728, 476), (694, 488), (664, 492)]   # and its near edge
MOUND = dict(x=640.0, z=1420.0, r=230.0, h=230.0)                 # the 40th distance mound
KAGO = dict(x=180.0, z=880.0, length=96.0, width=84.0, height=104.0, pole=400.0)   # the palanquin, set down (its pole along x)
TRUNKS = dict(x=-115.0, z=598.0, w=56.0, d=40.0, tier=15.0, n=5)  # Soshichi's willow trunks, set down at the road's edge
GRILL = dict(x=-330.0, z=548.0, w=112.0, d=46.0, h=56.0)         # O-Kuni's grill, out before the teahouse's door
SIGN = dict(x=-200.0, z=602.0, w=34.0, h=150.0)                  # the signboard, at the teahouse's corner
FUJI = Fuji(summit=(262.0, 84.0), foot=302.0, half=410.0, snow=0.40, seed=21)
FAR_ROW = 302
ROAD_EARTH = lerp(EARTH, STONE, 0.24)                              # the road: packed earth, a little greyer than Yui's street
COAST = [(236, 352), (270, 334), (310, 322), (360, 314), (430, 309), (520, 305), (620, 303)]   # the coast back toward Yui (its water's edge)


def ledge_z(x):
    xs = [p[0] for p in LEDGE]
    zs = [p[1] for p in LEDGE]
    return float(np.interp(x, xs, zs))


def ledge_top(x0=-1600.0, x1=3000.0, n=60):
    return [gp(x_, ledge_z(x_)) for x_ in np.linspace(x0, x1, n)]


# ================================================================ pass 1: broad and flat
def paint_sky(seed):
    """Yui's graded band: deep at the top, the paper at the horizon; seven bands (style.md section 3)."""
    rows = [0, 44, 92, 140, 186, 226, 260, HZ + 2]
    cols = [shade(COBALT, 0.42), mixp(COBALT, ULTRA, 0.3), COBALT, mixp(COBALT, CERULEAN, 0.55), CERULEAN,
            tintw(CERULEAN, 0.55), PAPER, PAPER]
    pic = bands(SHAPE, rows, cols, soft=6.0, wobble=2.5, seed=seed, patch=0.02)
    x, y = grid(SHAPE)
    glow(pic, tintw(NAPLES, 0.5), (np.clip(1 - x / 420.0, 0, 1) * np.clip(1 - np.abs(y - 272) / 70.0, 0, 1) * 0.10).astype(F32))
    return pic


def paint_far(pic, seed):
    """Fuji, the far shore of the head of the bay at its foot, and the coast curving back toward Yui."""
    fm, snow = FUJI.paint(pic, PAPER, seed)
    far = mask_poly(SHAPE, [(-10, FAR_ROW - 7), (160, FAR_ROW - 8), (360, FAR_ROW - 6), (520, FAR_ROW - 9), (700, FAR_ROW - 7),
                            (820, FAR_ROW - 6), (820, HZ + 3), (-10, HZ + 3)], soft=0.8, wobble=1.4, seed=seed + 4)
    over(pic, tintw(mixp(COBALT, VIRIDIAN, 0.35), 0.62), far)
    # the coast back toward Yui: low hills behind a thread of sand, nearer and lower at the left, curving out to the far
    # shore under Fuji (beyond a kilometre: no contour, two flats, pulled toward the paper and toward blue)
    hills = [(236, 284), (262, 286), (300, 289), (350, 292), (410, 295), (480, 298), (560, 300), (650, 301)]
    hm = mask_poly(SHAPE, hills + list(reversed(COAST)) + [(236, 360)], soft=0.7, wobble=1.2, seed=seed + 5)
    over(pic, lerp(mixp(VIRIDIAN, COBALT, 0.45), PAPER, 0.48), hm)
    # the hills' lit faces (toward the left): a lighter flat in their upper part
    hl = mask_poly(SHAPE, [(236, 286), (262, 287), (300, 290), (350, 293), (410, 296), (480, 299), (480, 302), (410, 301), (350, 300),
                           (300, 300), (262, 303), (236, 305)], soft=0.6, wobble=1.0, seed=seed + 7)
    over(pic, lerp(mixp(VERONESE, COBALT, 0.35), PAPER, 0.42), (hl * hm * 0.8).astype(F32))
    beach = mask_line(SHAPE, COAST, [3.2, 2.8, 2.3, 1.8, 1.4, 1.1, 0.9], soft=0.4)
    over(pic, tintw(NAPLES, 0.40), beach.astype(F32))
    return fm, snow


def satta_outline():
    """Mount Satta at the right: from where its foot meets the bay, up out of the top of the picture."""
    return [(506, 372), (528, 350), (560, 318), (590, 284), (622, 246), (650, 214), (676, 180), (700, 146), (724, 108), (748, 70),
            (772, 36), (794, 4), (812, -10)]


def satta_mask():
    pts = satta_outline()
    return mask_poly(SHAPE, pts + [(820, 640), (600, 640), (560, 430), (530, 404)], soft=0.6, wobble=1.6, seed=31)


def paint_satta(pic, seed):
    """Mount Satta: a dark green mass at the right, close (the road climbs it from here). Flats, not modelling: its spurs
    run down to the left, each spur's face turned to the morning sun a lit flat, the gullies between viridian toward
    prussian; crumbly rock showing pale in two scars; no contour inside (style.md sections 5 and 7)."""
    x, y = grid(SHAPE)
    m = satta_mask()
    body = flat(lerp(VIRIDIAN, PRUSSIAN, 0.34), SHAPE, seed + 12, 0.03, 70)
    over(pic, body, m)
    # the spurs: bands across the slope (running down to the left), warped; the first part of each a lit flat
    u = (x * 0.62 + y * 0.78)
    u = u + (warp(noise(SHAPE, (90, 60), seed + 13, 3), 12.0, 40, seed + 14) - 0.5) * 70
    ph = (u / 92.0) % 1.0
    lit_m = (step(0.04, 0.10, ph) * (1 - step(0.40, 0.46, ph))) * m
    over(pic, mixp(VIRIDIAN, VERONESE, 0.42), (lit_m * 0.9).astype(F32))
    hi_m = (step(0.08, 0.13, ph) * (1 - step(0.20, 0.26, ph))) * m * step(0.45, 0.6, noise(SHAPE, (40, 90), seed + 16, 2))
    over(pic, mixp(VERONESE, NAPLES, 0.18), (hi_m * 0.55).astype(F32))
    gully = (step(0.62, 0.68, ph) * (1 - step(0.86, 0.92, ph))) * m
    over(pic, lerp(VIRIDIAN, PRUSSIAN, 0.64), (gully * 0.6).astype(F32))
    # crumbly rock: two pale scars where the face has slipped
    for (cx_, cy_, w_, h_) in ((722, 296, 16, 40), (774, 182, 10, 28)):     # slip scars: wide where the ground broke away, a tongue below
        tongue = [(cx_ - w_, cy_), (cx_ - w_ * 0.4, cy_ - 3), (cx_ + w_ * 0.5, cy_ - 2), (cx_ + w_, cy_ + 2), (cx_ + w_ * 0.45, cy_ + h_ * 0.55),
                  (cx_ + w_ * 0.15, cy_ + h_), (cx_ - w_ * 0.2, cy_ + h_ * 0.7), (cx_ - w_ * 0.6, cy_ + h_ * 0.3)]
        sc = mask_poly(SHAPE, tongue, soft=0.6, wobble=2.0, seed=seed + int(cx_))
        over(pic, lerp(tintw(OCHRE, 0.30), PRUSSIAN, 0.22), (sc * m * 0.9).astype(F32))
        lip = mask_line(SHAPE, [(cx_ - w_, cy_), (cx_ - w_ * 0.4, cy_ - 3), (cx_ + w_ * 0.5, cy_ - 2), (cx_ + w_, cy_ + 2)], 1.6, soft=0.4)
        over(pic, lerp(VIRIDIAN, PRUSSIAN, 0.65), (lip * m * 0.8).astype(F32))
    # the headland's foot in the bay: a darker band where the rock meets the water (the old shore begins here)
    foot = mask_line(SHAPE, [(506, 372), (520, 384), (540, 398), (560, 412)], [6, 7, 7, 6], soft=1.0)
    over(pic, lerp(SIENNA, PRUSSIAN, 0.55), (foot * m * 0.8).astype(F32))
    return m


def water_mask():
    pts = ledge_top(-1600, 3000, 60)
    poly = [(-10, HZ - 1), (W + 10, HZ - 1), (W + 10, pts[-1][1])] + list(reversed(pts)) + [(-10, pts[0][1])]
    return mask_poly(SHAPE, poly, soft=0.6, wobble=0.6, seed=3)


def paint_bay(pic, seed):
    """The bay in seven bands (style.md section 3): the paper at the horizon, cerulean, cobalt, toward ultramarine near."""
    wm = water_mask()
    rows = [HZ, HZ + 6, HZ + 14, HZ + 27, HZ + 46, HZ + 72, HZ + 108, HZ + 170]
    cols = [tintw(CERULEAN, 0.62), tintw(CERULEAN, 0.40), tintw(CERULEAN, 0.16), mixp(CERULEAN, COBALT, 0.42), mixp(CERULEAN, COBALT, 0.75),
            COBALT, mixp(COBALT, ULTRA, 0.3), mixp(COBALT, ULTRA, 0.3)]
    wb = bands(SHAPE, rows, cols, soft=3.5, wobble=0.0, seed=seed + 20, patch=0.015)
    over(pic, wb, wm)
    return wm


def paint_ground(pic, seed):
    """The ledge (earth and grass; the rest place before the mound), its wall's top over the shore, and the road."""
    x, y = grid(SHAPE)
    X, Z, below = V.cam.floor_grid(SHAPE)
    top = ledge_top()
    gm = mask_poly(SHAPE, [(-10, top[0][1])] + top + [(W + 10, top[-1][1]), (W + 10, H + 10), (-10, H + 10)], soft=0.6, wobble=0.8, seed=seed + 29)
    t = np.clip((y - HZ) / (H - HZ), 0, 1)
    earth = flat(EARTH, SHAPE, seed + 30, 0.05, 40)
    earth = lerp(earth, PAPER, ((1 - t) ** 1.6 * 0.40)[..., None])
    grassy = flat(lerp(GRASS, EARTH, 0.30), SHAPE, seed + 31, 0.05, 30)
    grassy = lerp(grassy, PAPER, ((1 - t) ** 1.6 * 0.30)[..., None])
    ledge_t = np.clip((Z - ROAD["z1"]) / 260.0, 0, 1)
    gr_n = noise(SHAPE, (40, 12), seed + 32, 3)
    grass_m = np.clip(ledge_t * 1.4 - 0.25 + (gr_n - 0.5) * 0.9, 0, 1) * (Z > ROAD["z1"])
    ground = earth.copy()
    over(ground, grassy, grass_m.astype(F32))
    # the rest place before the mound: trodden bare where bearers wait
    worn = mask_poly(SHAPE, [gp(250, 600), gp(560, 600), gp(560, 1250), gp(300, 1150), gp(150, 900)], soft=6.0, wobble=5.0, seed=seed + 37)
    over(ground, lerp(EARTH, PAPER, 0.12), (worn * 0.75).astype(F32))
    near_m = np.clip((ROAD["z0"] - Z) / 40.0 + (noise(SHAPE, (50, 10), seed + 33, 3) - 0.5) * 1.2, 0, 1) * below
    over(ground, flat(lerp(GRASS, EARTH, 0.25), SHAPE, seed + 34, 0.06, 30), near_m.astype(F32))
    over(pic, ground, gm)
    # the wall's top: a band of set stones along the ledge's seaward edge (left and middle)
    edge = [p for p in top if p[0] < 600]
    over(pic, lerp(STONE, PAPER, 0.20), (mask_line(SHAPE, [(p[0], p[1] + 1.5) for p in edge], 3.4, soft=0.4) * 0.95).astype(F32))
    over(pic, lerp(STONE_SHADE, PAPER, 0.15), (mask_line(SHAPE, [(p[0], p[1] + 3.6) for p in edge], 1.2, soft=0.3) * 0.8).astype(F32))
    # the road: packed earth, soft-edged on the grass, two worn tracks along it
    rpoly = [gp(-4000, ROAD["z0"]), gp(4000, ROAD["z0"]), gp(4000, ROAD["z1"]), gp(-4000, ROAD["z1"])]
    rm = mask_poly(SHAPE, rpoly, soft=2.0, wobble=3.0, seed=seed + 35)
    road = flat(ROAD_EARTH, SHAPE, seed + 36, 0.04, 50)
    road = lerp(road, PAPER, ((1 - t) ** 1.6 * 0.35)[..., None])
    over(pic, road, (rm * gm).astype(F32))
    for zc, wd in ((170.0, 80.0), (400.0, 70.0)):
        tr = mask_poly(SHAPE, [gp(-4000, zc - wd / 2), gp(4000, zc - wd / 2), gp(4000, zc + wd / 2), gp(-4000, zc + wd / 2)], soft=4.0, wobble=4.0, seed=seed + int(zc))
        over(pic, lerp(ROAD_EARTH, PAPER, 0.20), (tr * 0.5 * gm).astype(F32))
    # the climb: at the right the road turns up across the mountain's foot: a ramp of road (a lit flat: it faces up to
    # the sun) rising from the rest place to the right edge, the cut bank above it in shade (the mountain cut back for
    # it, grass on its lip), the grassy slope of the foot below it
    slope = mask_poly(SHAPE, [(600, 430), (646, 476), (664, 492), (694, 488), (728, 476), (768, 460), (812, 441), (812, 470), (760, 482),
                              (700, 496), (640, 492)], soft=0.8, wobble=1.6, seed=seed + 40)
    over(pic, flat(lerp(GRASS, EARTH, 0.25), SHAPE, seed + 41, 0.05, 30), slope)
    bank = mask_poly(SHAPE, [(p[0], p[1] - 15 - 0.06 * (p[0] - 646)) for p in RAMP_FAR] + list(reversed(RAMP_FAR)), soft=0.6, wobble=1.2, seed=seed + 38)
    over(pic, lerp(lerp(tintw(OCHRE, 0.20), SIENNA, 0.18), PRUSSIAN, 0.45), bank)
    lip = mask_line(SHAPE, [(p[0], p[1] - 15 - 0.06 * (p[0] - 646)) for p in RAMP_FAR], 2.6, soft=0.5)
    over(pic, GRASS_SHADE, (lip * 0.9).astype(F32))
    ramp = mask_poly(SHAPE, RAMP_FAR + RAMP_NEAR, soft=0.8, wobble=1.0, seed=seed + 39)
    over(pic, lerp(lerp(ROAD_EARTH, PAPER, 0.14), NAPLES, 0.12), ramp)
    over(pic, lerp(ROAD_EARTH, PRUSSIAN, 0.12), (mask_line(SHAPE, RAMP_NEAR, 1.4, soft=0.4) * 0.7).astype(F32))
    return gm, rm


def cast_shadows(pic, ground):
    """Every standing thing's shadow, flat and blue, laid along the sun (to the right and away)."""
    sh = Paper(SHAPE)
    sc = EARTH_SHADE
    # the teahouse: its right end and its roof's eave, laid flat
    xR, z0, z1, e = TEA["x1"], TEA["z0"], TEA["z1"], TEA["eave"]
    eave_z0 = z0 - TEA["over"]
    pts = [(xR + TEA["over"], e, eave_z0), (xR + TEA["over"], e, z1 + TEA["over"]), (xR - 250, TEA["ridge"], (z0 + z1) / 2)]
    shp = V.shadow_pts(pts)
    sh.poly([gp(xR, z0), shp[0], shp[2], shp[1], gp(xR, z1)], sc, 1.0)
    # the signboard and the trunks
    sx, sz = SIGN["x"], SIGN["z"]
    sh.poly(V.shadow_pts([(sx - 15, 0, sz), (sx + 15, 0, sz), (sx + 15, SIGN["h"], sz), (sx - 15, SIGN["h"], sz)]), sc, 0.95)
    tx, tz = TRUNKS["x"], TRUNKS["z"]
    th = TRUNKS["tier"] * TRUNKS["n"] + 10
    sh.poly(V.shadow_pts([(tx - 28, 0, tz - 20), (tx + 28, 0, tz - 20), (tx + 28, th, tz + 20), (tx - 28, th, tz - 20)]) + [gp(tx + 28, tz + 20)], sc, 0.95)
    # the grill
    gx, gz = GRILL["x"], GRILL["z"]
    sh.poly(V.shadow_pts([(gx - 56, 0, gz - 23), (gx + 56, 0, gz - 23), (gx + 56, GRILL["h"], gz - 23), (gx - 56, GRILL["h"], gz - 23)]), sc, 0.95)
    # the mound and its tree: the mound's shadow to the right, the crown's shadow a big flat patch to the right and back
    # the palanquin
    kx, kzz = KAGO["x"], KAGO["z"]
    L, Wd, Hh = KAGO["length"], KAGO["width"], KAGO["height"]
    sh.poly(V.shadow_pts([(kx - L / 2, Hh, kzz - Wd / 2), (kx + L / 2, Hh, kzz - Wd / 2), (kx + L / 2, Hh, kzz + Wd / 2), (kx - L / 2, Hh, kzz + Wd / 2)])
            + [gp(kx - L / 2, kzz + Wd / 2)], sc, 0.85)
    c, a = sh.done()
    shade_ground(pic, (a * ground).astype(F32))
    # the hill behind us (the foot of the mountain the road has come along) throws its morning shadow across the near
    # verge and the near edge of the road, from the left: a hard edge, wavy where the hill's pines are, no gradient
    edge = [(-10, 528), (60, 534), (120, 528), (170, 540), (240, 548), (300, 556), (360, 566), (430, 574), (500, 586), (560, 598), (600, 612)]
    hm = mask_poly(SHAPE, edge + [(-10, 612)], soft=0.7, wobble=2.5, seed=97)
    shade_ground(pic, (hm * ground).astype(F32))
    return np.maximum(a, hm)


def under(seed=SEED):
    info = {}
    pic = paint_sky(seed)
    info["fuji"], info["snow"] = paint_far(pic, seed)
    info["water"] = paint_bay(pic, seed)
    info["satta"] = paint_satta(pic, seed)
    info["ground"], info["road"] = paint_ground(pic, seed)
    info["shadow"] = cast_shadows(pic, info["ground"])
    land.haze(pic, HZ, PAPER, 0.30, 0.10, info["ground"])
    return np.clip(pic, 0, 1), info


# ================================================================ pass 3: the crisp things (the backdrop's)
def teahouse(sheet, info):
    """O-Kuni's teahouse: its open front to the road, a thatched hip roof (the front slope lit, the right hip in shade),
    the matted room behind the bench (its back open on the bay), the door to the earth floor at the right (the noren is a
    cut-out), the right end wall in shade. One flat per face, the contour round the silhouette and the posts."""
    T = TEA
    x0, x1, z0, z1, e, fl, li = T["x0"], T["x1"], T["z0"], T["z1"], T["eave"], T["floor"], T["lintel"]
    dx0, dx1 = T["door"]
    row0 = gp(x1, z0)[1]
    mat_x0, mat_x1 = x0, dx0
    # ---- the inside, seen through the open front: the matted room (left) and the earth floor (right)
    sheet.poly([gp(mat_x0, z0, fl), gp(mat_x1, z0, fl), gp(mat_x1, z1, fl), gp(mat_x0, z1, fl)], TATAMI)
    # the mats' edges: dark cloth borders running back, and across
    for xm in np.arange(mat_x0 + 90, mat_x1, 90.0):
        sheet.line([gp(xm, z0, fl), gp(xm, z1, fl)], lerp(TATAMI, PRUSSIAN, 0.35), max(0.6, 3 * kz(z0)), 0.8)
    for zm in (z0 + 180, z0 + 360):
        sheet.line([gp(mat_x0, zm, fl), gp(mat_x1, zm, fl)], lerp(TATAMI, PRUSSIAN, 0.35), max(0.6, 3 * kz(zm)), 0.8)
    # the back: open on the bay (the bay's own blue through it), its sill and its lintel, two posts
    bay_c = mixp(COBALT, ULTRA, 0.18)
    sheet.poly([gp(mat_x0, z1, fl), gp(mat_x1, z1, fl), gp(mat_x1, z1, 190), gp(mat_x0, z1, 190)], bay_c)
    sheet.poly([gp(mat_x0, z1, fl), gp(mat_x1, z1, fl), gp(mat_x1, z1, fl + 10), gp(mat_x0, z1, fl + 10)], WOOD_SHADE)
    for xp in (-1000.0, -720.0, mat_x1):
        sheet.line([gp(xp, z1, fl), gp(xp, z1, 190)], WOOD_DARK, max(1.0, 9 * kz(z1)), 1.0)
    # the inside's shade: the room under the roof, darker at its top (the ceiling's shadow) and on the left wall
    sheet.poly([gp(mat_x0, z1, 190), gp(mat_x1, z1, 190), gp(mat_x1, z0, li), gp(mat_x0, z0, li)], lerp(WOOD_DARK, PRUSSIAN, 0.2))
    # the earth floor (doma) behind the door: dark, a warmer floor, the stove's mouth faintly warm at the back
    sheet.poly([gp(dx0, z0, 0), gp(dx1, z0, 0), gp(dx1, z0, li), gp(dx0, z0, li)], lerp(WOOD_DARK, PRUSSIAN, 0.25))
    sheet.poly([gp(dx0, z0, 0), gp(dx1, z0, 0), gp(dx1, z1, 0), gp(dx0, z1, 0)], lerp(EARTH, PRUSSIAN, 0.55))
    sheet.poly([gp(dx0 + 40, z1 - 10, 0), gp(dx0 + 120, z1 - 10, 0), gp(dx0 + 120, z1 - 10, 70), gp(dx0 + 40, z1 - 10, 70)], lerp(STONE_SHADE, PRUSSIAN, 0.3))
    sheet.ellipse(*gp(dx0 + 80, z1 - 10, 30), 3.2, 2.0, lerp(VERMILION, SIENNA, 0.5), 0.8)
    # ---- the front: posts, the sill under the mats, the lintel, the wall strip above it to the eave
    wall_c = lerp(PLASTER_LIT, COBALT, 0.28)                                      # the wall strip is in the eave's shade
    sheet.poly([gp(x0, z0, li), gp(x1, z0, li), gp(x1, z0, e + 15), gp(x0, z0, e + 15)], wall_c)
    sheet.poly([gp(x0, z0, li - 8), gp(x1, z0, li - 8), gp(x1, z0, li + 6), gp(x0, z0, li + 6)], WOOD_SHADE)     # the lintel beam
    sheet.poly([gp(mat_x0, z0, fl - 10), gp(mat_x1, z0, fl - 10), gp(mat_x1, z0, fl + 3), gp(mat_x0, z0, fl + 3)], WOOD_LIT)  # the sill
    sheet.poly([gp(mat_x0, z0, 0), gp(mat_x1, z0, 0), gp(mat_x1, z0, fl - 10), gp(mat_x0, z0, fl - 10)], lerp(WOOD_SHADE, PRUSSIAN, 0.25))
    for xp in T["posts"]:
        sheet.line([gp(xp, z0, 0), gp(xp, z0, e + 10)], WOOD_SHADE, max(1.2, 13 * kz(z0)), 1.0)
        sheet.line([gp(xp - 4, z0, 0), gp(xp - 4, z0, e + 10)], WOOD_LIT, max(0.8, 5 * kz(z0)), 1.0)
    # the reed blind rolled up under the eave over the matted part, tied in two places
    for xb0, xb1 in ((x0, mat_x1 - 10),):
        a, b = gp(xb0, z0 - 14, li + 18), gp(xb1, z0 - 14, li + 18)
        sheet.line([a, b], lerp(tintw(OCHRE, 0.35), SIENNA, 0.2), max(2.0, 13 * kz(z0)), 1.0)
        sheet.line([(a[0], a[1] + 3), (b[0], b[1] + 3)], lerp(SIENNA, PRUSSIAN, 0.3), 0.7, 0.6)
    # ---- the right end wall (in shade): plaster between the posts, a little window
    sheet.poly([gp(x1, z0, 0), gp(x1, z1, 0), gp(x1, z1, e + 15), gp(x1, z0, e + 15)], PLASTER_SHADE)
    sheet.line([gp(x1, z1, 0), gp(x1, z1, e + 10)], WOOD_DARK, max(1.0, 11 * kz(z1)), 1.0)
    sheet.poly([gp(x1, z0 + 200, 100), gp(x1, z0 + 330, 100), gp(x1, z0 + 330, 170), gp(x1, z0 + 200, 170)], lerp(WOOD_DARK, PRUSSIAN, 0.3))
    for zz in np.linspace(z0 + 215, z0 + 315, 5):
        sheet.line([gp(x1, zz, 100), gp(x1, zz, 170)], WOOD_SHADE, 0.8, 0.9)
    # ---- the roof: thatch, a hip roof; the front slope (lit) and the right hip (shade), the thick eave
    ov = T["over"]
    eF = [(x0 - ov, z0 - ov), (x1 + ov, z0 - ov)]                 # the front eave's ends
    eB = (x1 + ov, z1 + ov)                                        # the back-right eave corner
    rz = (z0 + z1) / 2
    rR = (x1 - 240.0, rz)                                          # the ridge's right end
    rL = (x0 + 240.0, rz)
    E_H = e
    front_slope = [gp(eF[0][0], eF[0][1], E_H), gp(eF[1][0], eF[1][1], E_H), gp(rR[0], rR[1], T["ridge"]), gp(rL[0], rL[1], T["ridge"])]
    hip = [gp(eF[1][0], eF[1][1], E_H), gp(eB[0], eB[1], E_H), gp(rR[0], rR[1], T["ridge"])]
    sheet.poly(front_slope, THATCH_LIT)
    sheet.poly(hip, THATCH_SHADE)
    # the eave's thickness: thatch is a deep cut edge, a band along the front and down the hip's foot
    thick = 34.0
    sheet.poly([gp(eF[0][0], eF[0][1], E_H), gp(eF[1][0], eF[1][1], E_H), gp(eF[1][0], eF[1][1], E_H + thick), gp(eF[0][0], eF[0][1], E_H + thick)],
               lerp(THATCH_LIT, SIENNA, 0.35))
    sheet.poly([gp(eF[1][0], eF[1][1], E_H), gp(eB[0], eB[1], E_H), gp(eB[0], eB[1], E_H + thick), gp(eF[1][0], eF[1][1], E_H + thick)],
               lerp(THATCH_SHADE, PRUSSIAN, 0.25))
    # thatch texture: rows of short strokes along the eave and up the slope (style.md section 5)
    rng = np.random.default_rng(77)
    for v in (0.0, 0.18, 0.40, 0.66):
        ya = E_H + thick + (T["ridge"] - E_H - thick) * v
        za = eF[0][1] + (rz - eF[0][1]) * v
        for xx in np.arange(x0 - ov, x1 + ov - 20, 26.0):
            if xx < x0 - ov + (rL[0] - (x0 - ov)) * v or xx > x1 + ov - ((x1 + ov) - rR[0]) * v:
                continue
            p0 = gp(xx + rng.normal(0, 4), za, ya)
            p1 = gp(xx + rng.normal(0, 4), za + 30, ya + 26)
            sheet.line([p0, p1], lerp(THATCH_LIT, SIENNA, 0.45), max(0.6, 2.4 * kz(za)), 0.55)
    # the ridge: a dark cap of bound straw along the top, with cross pieces
    sheet.line([gp(rL[0] - 20, rz, T["ridge"] + 8), gp(rR[0] + 20, rz, T["ridge"] + 8)], lerp(SIENNA, PRUSSIAN, 0.5), max(2.0, 18 * kz(rz)), 1.0)
    for xx in np.arange(rL[0], rR[0] + 1, 70.0):
        sheet.line([gp(xx, rz - 20, T["ridge"] - 6), gp(xx, rz - 20, T["ridge"] + 26)], lerp(SIENNA, PRUSSIAN, 0.6), max(1.0, 6 * kz(rz)), 1.0)
    # ---- the contour
    V.contour(sheet, [front_slope[0], front_slope[1], hip[1]], row0)
    V.contour(sheet, [front_slope[3], front_slope[2], hip[0]], row0)
    V.contour(sheet, [hip[2], hip[1]], row0)
    V.contour(sheet, [gp(x1, z0, 0), gp(x1, z0, e + 10)], row0)
    V.contour(sheet, [gp(x1, z1, 0), gp(x1, z1, e + 10)], row0, alpha=0.5)
    V.contour(sheet, [gp(x0, z0, 0), gp(x1, z0, 0), gp(x1, z1, 0)], row0)
    info["tea_front"] = [gp(x0, z0, 0), gp(x1, z0, 0), gp(x1, z0, e), gp(x0, z0, e)]
    info["tea_roof"] = front_slope + hip
    info["tea_box"] = [0, int(min(p[1] for p in front_slope)) - 4, int(gp(eB[0], eB[1], E_H)[0]) + 2, int(row0 - min(p[1] for p in front_slope)) + 6]
    info["mats_box"] = [int(gp(mat_x0, z0, fl)[0]), int(gp(mat_x0, z1, 190)[1]), int(gp(mat_x1, z0, fl)[0] - max(0, gp(mat_x0, z0, fl)[0])),
                        int(gp(mat_x0, z0, fl)[1] - gp(mat_x0, z1, 190)[1])]


def bench(sheet):
    """The bench under the eaves: a long low plank on four legs, a tea tray on it (a pot and two cups)."""
    B = BENCH
    x0, x1, z0, z1, h = B["x0"], B["x1"], B["z0"], B["z1"], B["h"]
    sheet.poly([gp(x0, z0, h), gp(x1, z0, h), gp(x1, z1, h), gp(x0, z1, h)], WOOD_LIT)
    sheet.poly([gp(x0, z0, h - 6), gp(x1, z0, h - 6), gp(x1, z0, h), gp(x0, z0, h)], WOOD_SHADE)
    for xx in (x0 + 12, x1 - 12):
        sheet.line([gp(xx, z0 + 4, 0), gp(xx, z0 + 4, h - 6)], WOOD_DARK, max(1.0, 6 * kz(z0)), 1.0)
    V.contour(sheet, [gp(x0, z0, h - 6), gp(x0, z0, h), gp(x1, z0, h), gp(x1, z0, h - 6)], gp(x0, z0)[1])
    # the tray, the pot, the cups
    tx, tz = x0 + 70, (z0 + z1) / 2
    sheet.poly([gp(tx - 18, tz - 12, h + 1), gp(tx + 18, tz - 12, h + 1), gp(tx + 18, tz + 12, h + 1), gp(tx - 18, tz + 12, h + 1)], lerp(SIENNA, PRUSSIAN, 0.35))
    p = gp(tx - 6, tz, h + 9)
    sheet.ellipse(p[0], p[1], 3.4, 3.0, lerp(tintw(PRUSSIAN, 0.45), OCHRE, 0.2))
    for dx_ in (6.0, 13.0):
        q = gp(tx + dx_, tz, h + 4)
        sheet.ellipse(q[0], q[1], 1.6, 1.3, tintw(CERULEAN, 0.7))


def sign_board(sheet):
    """The signboard at the teahouse's corner: a pale board on a post with a little roof, a turban shell painted on it
    (our own sign: no shop's name), and under it a column of brush marks (pattern, never characters a reader could read)."""
    S = SIGN
    x, z, w, h = S["x"], S["z"], S["w"], S["h"]
    k = kz(z)
    sheet.line([gp(x, z, 0), gp(x, z, h)], WOOD_DARK, max(1.2, 7 * k), 1.0)
    board = [gp(x - w / 2, z, 40), gp(x + w / 2, z, 40), gp(x + w / 2, z, h - 6), gp(x - w / 2, z, h - 6)]
    sheet.poly(board, lerp(tintw(OCHRE, 0.62), NAPLES, 0.2))
    sheet.poly([gp(x - w / 2 - 6, z, h - 6), gp(x + w / 2 + 6, z, h - 6), gp(x + w / 2 + 2, z, h + 6), gp(x - w / 2 - 2, z, h + 6)], WOOD_DARK)
    # the shell: a dark knobbed cone, its mouth up
    c = gp(x, z, h - 34)
    s = 10 * k
    sheet.poly([(c[0] - s * 0.9, c[1] - s * 0.6), (c[0] + s * 0.9, c[1] - s * 0.6), (c[0] + s * 0.35, c[1] + s * 1.1), (c[0] - s * 0.35, c[1] + s * 1.1)],
               lerp(VIRIDIAN, PRUSSIAN, 0.45))
    sheet.ellipse(c[0], c[1] - s * 0.6, s * 0.9, s * 0.32, lerp(tintw(OCHRE, 0.35), SIENNA, 0.2))
    for dx_ in (-0.7, -0.2, 0.3, 0.75):
        sheet.line([(c[0] + dx_ * s, c[1] - s * 0.3), (c[0] + dx_ * s * 1.25, c[1] - s * 0.1)], lerp(VIRIDIAN, PRUSSIAN, 0.6), 0.9, 1.0)
    # the brush marks: a column of short dark strokes
    rng = np.random.default_rng(15)
    yy = h - 60
    while yy > 50:
        ln = rng.uniform(7, 13)
        a, b = gp(x + rng.uniform(-4, 4), z, yy), gp(x + rng.uniform(-4, 4), z, yy - ln)
        sheet.line([a, b], PRUSSIAN, max(1.0, 3.6 * k), 0.95)
        if rng.random() < 0.6:
            sheet.line([gp(x - 7, z, yy - ln * 0.4), gp(x + 7, z, yy - ln * 0.5)], PRUSSIAN, max(0.8, 2.4 * k), 0.9)
        yy -= ln + rng.uniform(4, 8)
    V.contour(sheet, board + [board[0]], gp(x, z)[1], alpha=0.75)


def mound_and_tree(sheet, seed):
    """The 40th distance mound: a grassed dome; on it the hackberry planted for shade (two centuries old): a short thick
    trunk, three limbs, a broad crown of fresh April leaves as flat pads (lit veronese and naples, shade viridian)."""
    M = MOUND
    mx, mz, r, h = M["x"], M["z"], M["r"], M["h"]
    k = kz(mz)
    base = gp(mx, mz)
    # the mound: a dome in two flats, the lit one turned to the left and up, the terminator a curve over its crown
    top = []
    for a in np.linspace(0, math.pi, 31):
        u = math.cos(a)
        top.append(gp(mx + r * u, mz, h * (1 - abs(u) ** 2.2) ** 0.7))
    sheet.poly(top + [gp(mx + r, mz)], GRASS)                                   # (top runs from the right foot over to the left foot)
    term = [gp(mx + r * 0.05 + r * 0.45 * math.sin(t_), mz, h * 0.99 * math.cos(t_) ** 0.8) for t_ in np.linspace(0, math.pi / 2, 10)]
    lit_side = [p for p in top if p[0] <= gp(mx + r * 0.05, mz)[0] + 0.5]
    sheet.poly(lit_side + list(reversed(term)), GRASS_LIT)
    rng = np.random.default_rng(seed)
    for i in range(18):
        u = rng.uniform(-0.92, 0.92)
        hh = h * (1 - abs(u) ** 2.2) ** 0.7
        p = gp(mx + r * u, mz - 30, hh * rng.uniform(0.25, 0.97))
        tuft(sheet, p[0], p[1], 5.5, seed + i, lean=0.3, colors=(GRASS_SHADE, GRASS) if u > 0.2 else (GRASS, GRASS_SHADE), n=4, width=0.8)
    V.contour(sheet, top, base[1], alpha=0.5)
    info = hackberry(sheet, mx, mz, h, seed + 5)
    info["mound"] = [int(gp(mx - r, mz)[0]), int(gp(mx, mz, h)[1]) - 2, int(2 * r * k) + 2, int(base[1] - gp(mx, mz, h)[1]) + 3]
    return info


def hackberry(sheet, mx, mz, h, seed):
    """The mound's hackberry's trunk and limbs (an enoki, planted for the travellers' shade two centuries since): short,
    thick, forking into three; the crown is painted after (hackberry_crown)."""
    k = kz(mz)
    trunk = [gp(mx - 8, mz, h - 10), gp(mx - 4, mz, h + 90), gp(mx + 6, mz, h + 175)]
    sheet.taper(trunk, BARK_SHADE, 44 * k, 34 * k)
    sheet.taper([(p[0] - 7 * k, p[1]) for p in trunk], lerp(BARK, tintw(PRUSSIAN, 0.5), 0.35), 16 * k, 12 * k)
    limbs = [[gp(mx + 6, mz, h + 175), gp(mx - 90, mz, h + 260), gp(mx - 230, mz, h + 330)],
             [gp(mx + 6, mz, h + 175), gp(mx + 100, mz, h + 270), gp(mx + 240, mz, h + 340)],
             [gp(mx + 6, mz, h + 175), gp(mx + 20, mz, h + 300), gp(mx - 10, mz, h + 420)]]
    for L in limbs:
        sheet.taper(L, BARK_SHADE, 22 * k, 10 * k)
    return {"trunk": [int(gp(mx - 40, mz)[0]), int(gp(mx, mz, h + 260)[1]), int(80 * k) + 2, int(gp(mx, mz, h)[1] - gp(mx, mz, h + 260)[1])]}


def hackberry_crown(pic, mx, mz, h, seed):
    """The crown, as the prints paint a broadleaf tree: one scalloped silhouette of fresh April leaf; inside it five
    big masses, each with a lit crescent toward the sun (yellow-green) and a shade crescent under it (viridian); the
    whole underside in shade; a few drawn leaf marks; a breath of contour along the top. Flats with hard edges."""
    k = kz(mz)
    rng = np.random.default_rng(seed)
    leaf_sh, leaf, leaf_lit = lerp(VIRIDIAN, PRUSSIAN, 0.16), mixp(VERONESE, VIRIDIAN, 0.40), lerp(VERONESE, NAPLES, 0.42)
    masses = [(-250, 380, 210, 150), (230, 390, 220, 150), (-40, 470, 260, 175), (-200, 560, 170, 120), (170, 570, 180, 125), (10, 650, 170, 105)]
    union = np.zeros(SHAPE, dtype=F32)
    for (dx_, y_, rx_, ry_) in masses:                                  # the scalloped edge: small clumps round each mass
        for i in range(14):
            a = rng.uniform(0, 2 * math.pi)
            cx_, cy_ = dx_ + math.cos(a) * rx_ * 0.78, y_ + math.sin(a) * ry_ * 0.70
            r_ = rng.uniform(0.32, 0.46) * rx_
            c = gp(mx + cx_, mz, h + cy_)
            union = np.maximum(union, mask_ellipse(SHAPE, c[0], c[1], r_ * k, r_ * k * 0.72))
        c = gp(mx + dx_, mz, h + y_)
        union = np.maximum(union, mask_ellipse(SHAPE, c[0], c[1], rx_ * k * 0.92, ry_ * k * 0.92))
    over(pic, leaf, union)
    x, y = grid(SHAPE)
    for (dx_, y_, rx_, ry_) in masses:
        c = gp(mx + dx_, mz, h + y_)
        m0 = mask_ellipse(SHAPE, c[0], c[1], rx_ * k, ry_ * k * 0.98, wobble=2.0, seed=seed + int(dx_))
        up = mask_ellipse(SHAPE, c[0] - rx_ * k * 0.12, c[1] - ry_ * k * 0.22, rx_ * k, ry_ * k * 0.98, wobble=2.0, seed=seed + int(dx_))
        dn = mask_ellipse(SHAPE, c[0] + rx_ * k * 0.16, c[1] + ry_ * k * 0.26, rx_ * k, ry_ * k * 0.98, wobble=2.0, seed=seed + int(dx_))
        over(pic, leaf_sh, (m0 * (1 - up) * union).astype(F32))                       # the shade crescent, under it
        lit_c = (m0 * (1 - dn) * union) * (x < c[0] + rx_ * k * 0.55)
        over(pic, leaf_lit, lit_c.astype(F32))                                         # the lit crescent, toward the sun
    # the underside: the crown's lowest band in shade (a hard edge, a little wavy)
    low = np.zeros(SHAPE, dtype=F32)
    for (dx_, y_, rx_, ry_) in masses[:3]:
        c = gp(mx + dx_, mz, h + y_ - ry_ * 0.55)
        low = np.maximum(low, mask_ellipse(SHAPE, c[0], c[1] + ry_ * k * 0.5, rx_ * k * 1.05, ry_ * k * 0.62, wobble=3.0, seed=seed + 9))
    over(pic, lerp(leaf_sh, PRUSSIAN, 0.12), (low * union * 0.95).astype(F32))
    # drawn leaf marks: short arcs in the masses (texture drawn, not shaded)
    marks = Sheet(SHAPE)
    for i in range(70):
        dx_ = rng.uniform(-430, 430)
        y_ = rng.uniform(300, 720)
        c = gp(mx + dx_, mz, h + y_)
        if not (0 <= int(c[1]) < H and 0 <= int(c[0]) < W) or union[int(c[1]), int(c[0])] < 0.9:
            continue
        r_ = rng.uniform(4, 7)
        marks.line([(c[0] - r_, c[1]), (c[0] - r_ * 0.3, c[1] + r_ * 0.45), (c[0] + r_ * 0.5, c[1] + r_ * 0.2)], lerp(leaf_sh, PRUSSIAN, 0.2), 0.8, 0.55)
    marks.onto(pic)
    edge = np.clip(union - np.roll(union, 2, axis=0), 0, 1)
    over(pic, PRUSSIAN, (blur(edge, 0.5) * 0.30).astype(F32))
    ys, xs = np.where(union > 0.5)
    return {"crown": [int(xs.min()), int(ys.min()), int(xs.max() - xs.min()) + 1, int(ys.max() - ys.min()) + 1]}, union


def cliff_road(sheet):
    """The road west cut across Mount Satta's face: pale ledges of cut earth with the dark cut above them, climbing in
    two legs up and round to the right (no figures painted on it)."""
    legs = [[(652, 262), (696, 256), (738, 246), (780, 234), (812, 226)], [(770, 116), (790, 104), (812, 92)]]
    for i, L in enumerate(legs):
        w = 5.0 - i * 1.6
        sheet.line([(p[0], p[1] - w * 0.9) for p in L], lerp(VIRIDIAN, PRUSSIAN, 0.70), w * 0.9, 0.9)   # the cut face above
        sheet.line(L, lerp(tintw(OCHRE, 0.42), PRUSSIAN, 0.12), w * 0.75, 1.0)                           # the road's bed
        sheet.line([(p[0], p[1] + w * 0.5) for p in L], lerp(tintw(OCHRE, 0.2), PRUSSIAN, 0.35), 0.7, 0.7)
    # pines along the skyline and on the face, small (middle distance: a breath of contour)
    pass


def details(pic, info, seed=SEED, fast=False):
    x, y = grid(SHAPE)
    crisp = pic.copy()
    paint_far(crisp, seed)
    pic[...] = lerp(pic, crisp, (0.7 * info["fuji"] * (y < HZ) * (1 - info["satta"]))[..., None])
    FUJI.contour(pic, info["fuji"] * (1 - info["satta"]))
    crisp = pic.copy()
    paint_satta(crisp, seed)
    pic[...] = lerp(pic, crisp, (0.5 * info["satta"] * (1 - info["ground"]))[..., None])
    sheet = Paper(SHAPE)
    rng0 = np.random.default_rng(seed + 69)
    # far: boats on the bay, Yui's roofs on the curve of the coast
    for i, (bx, by, s) in enumerate(((410, 331, 0.75), (482, 350, 0.95), (352, 318, 0.55), (300, 326, 0.5))):
        sail_boat(sheet, bx, by, s, seed + 70 + i, sail=(i != 2))
    far_roofs(sheet, 276, 336, 324, 8, seed + 71, h=2.8)
    for i, xx in enumerate(np.linspace(330, 400, 4)):                           # pines along the curve's beach: dabs on the land, no line
        row = float(np.interp(xx, [p[0] for p in COAST], [p[1] for p in COAST])) - 3.0
        sheet.ellipse(xx + rng0.normal(0, 2), row, 2.6 - 1.2 * i / 7, 1.5 - 0.6 * i / 7, lerp(tintw(VIRIDIAN, 0.15), COBALT, 0.30))
    # Mount Satta: the cliff road, pines on the skyline and its face
    cliff_road(sheet)
    rng = np.random.default_rng(seed + 72)
    # pines on the headland: on the skyline, small pines in the prints' manner (a leaning trunk, two or three flat
    # pads); on the face, clumps of dark green without a trunk (the middle distance: no texture, a breath of line)
    for (px_, py_, s_) in ((518, 362, 0.42), (556, 324, 0.5), (598, 280, 0.55), (636, 236, 0.6), (690, 166, 0.66), (718, 128, 0.7),
                           (744, 88, 0.74), (774, 44, 0.78)):
        hgt = 30 * s_
        lean = -5 * s_
        trunk = [(px_, py_ + 2), (px_ + lean * 0.5, py_ - hgt * 0.55), (px_ + lean, py_ - hgt * 0.9)]
        pads = [(px_ + lean * 0.4 - 7 * s_, py_ - hgt * 0.50, 13 * s_, 4.6 * s_), (px_ + lean * 0.8 + 6 * s_, py_ - hgt * 0.76, 12 * s_, 4.2 * s_),
                (px_ + lean, py_ - hgt * 1.0, 9 * s_, 3.6 * s_)]
        pine_pads(sheet, sheet, trunk, pads, int(rng.integers(1e6)), scale=1.0, contour=True, alpha_line=0.3, w_line=0.5, trunk_w=2.2 * s_)
    for i in range(26):
        px_, py_ = rng.uniform(560, 800), rng.uniform(150, 420)
        if not info["satta"][int(min(py_, 599)), int(min(px_, 799))] > 0.9 or py_ > 300 + (px_ - 560) * 0.4 + 100:
            continue
        r_ = rng.uniform(5, 9)
        sheet.ellipse(px_, py_, r_, r_ * 0.55, lerp(VIRIDIAN, PRUSSIAN, 0.62))
        sheet.ellipse(px_ - r_ * 0.25, py_ - r_ * 0.22, r_ * 0.6, r_ * 0.3, lerp(VIRIDIAN, PRUSSIAN, 0.3))
    sheet.onto(pic)
    # the mound and its hackberry: the mound and the trunk, then the crown over them
    sheet = Paper(SHAPE)
    info["tree"] = mound_and_tree(sheet, seed + 80)
    sheet.onto(pic)
    crown_info, info["crown_mask"] = hackberry_crown(pic, MOUND["x"], MOUND["z"], MOUND["h"], seed + 81)
    info["tree"].update(crown_info)
    sheet = Paper(SHAPE)
    # the teahouse, its bench, its sign
    teahouse(sheet, info)
    bench(sheet)
    sign_board(sheet)
    # stones along the road's edges, a few on the road
    stones = Sheet(SHAPE)
    land.stones(stones, pic, HZ, seed + 90, 46, zone=((info["road"] > 0.4) & (y > 470)), ground=info["ground"], size=(0.6, 2.2),
                tones=(tintw(PRUSSIAN, 0.78), tintw(PRUSSIAN, 0.6), tintw(PRUSSIAN, 0.42), tintw(PRUSSIAN, 0.24)))
    sc, sa = stones.done()
    over(pic, sc, sa)
    sheet.onto(pic)
    # grass along the road's near edge and the ledge's edge (drawn, leaning with the wind off the bay: to the right)
    gs = Sheet(SHAPE)
    for i in range(60):
        xx = rng.uniform(0, 800)
        zz = rng.uniform(-20, ROAD["z0"] + 10)
        p = gp(V.x_at(xx, gp(0, zz)[1]), zz)
        tuft(gs, xx, p[1], 9 * kz(zz) / 0.8, seed + 200 + i, lean=0.25, n=6, width=1.1)
    for i in range(40):
        xx = rng.uniform(0, 560)
        row = np.interp(xx, [p[0] for p in ledge_top()], [p[1] for p in ledge_top()])
        if 0 < xx < 270 and row > 380:
            continue
        tuft(gs, xx, row + 1, 5.0, seed + 300 + i, lean=0.25, n=5, width=0.8)
    gs.onto(pic)
    return pic


# ================================================================ the cut-outs
def cloud_cut(back, seed, fast=False):
    """Fuji's cap of cloud (on / off): the same cloud as on the pass (edo_kurasawa_kit.cloud_cap), at this mountain's size."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    outline = cloud_cap(sheet, lines, FUJI)
    c, a = sheet.done()
    lc, la = lines.done()
    out = brushed(c, a, lc, la, tintw(CERULEAN, 0.85), seed=seed, sizes=(4, 2), keep=0.7, fast=fast)
    return out[0], out[1], outline


def grill_cut(back, seed, fast=False):
    """O-Kuni's grill: a long clay firebox on the ground before her door, a bed of charcoal, turban shells standing in it
    mouth up, their juice bubbling (the smoke and the embers are the engine's). O-Kuni stands behind it."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    G = GRILL
    x, z, w, d, h = G["x"], G["z"], G["w"], G["d"], G["h"]
    k = kz(z)
    clay_lit, clay_sh = lerp(tintw(OCHRE, 0.38), PRUSSIAN, 0.22), lerp(lerp(OCHRE, SIENNA, 0.5), PRUSSIAN, 0.45)
    f0, f1 = z - d / 2, z + d / 2
    sheet.poly([gp(x - w / 2, f0, 0), gp(x + w / 2, f0, 0), gp(x + w / 2, f0, h), gp(x - w / 2, f0, h)], clay_lit)        # its front
    sheet.poly([gp(x + w / 2, f0, 0), gp(x + w / 2, f1, 0), gp(x + w / 2, f1, h), gp(x + w / 2, f0, h)], clay_sh)          # its right end
    sheet.poly([gp(x - w / 2, f0, h), gp(x + w / 2, f0, h), gp(x + w / 2, f1, h), gp(x - w / 2, f1, h)], lerp(clay_sh, PRUSSIAN, 0.3))   # the rim
    sheet.poly([gp(x - w / 2 + 7, f0 + 6, h), gp(x + w / 2 - 7, f0 + 6, h), gp(x + w / 2 - 7, f1 - 6, h), gp(x - w / 2 + 7, f1 - 6, h)],
               lerp(PRUSSIAN, SIENNA, 0.25))                                                                                      # the charcoal
    rng = np.random.default_rng(seed)
    for i in range(14):
        p = gp(x + rng.uniform(-w / 2 + 12, w / 2 - 12), rng.uniform(f0 + 9, f1 - 9), h + 1)
        sheet.ellipse(p[0], p[1], 1.4, 0.8, lerp(VERMILION, NAPLES, 0.25), 0.85)
    # the shells: six knobbed cones in the coals, mouth up, a little foam at each mouth
    shells = []
    for i in range(6):
        sx_ = x - w / 2 + 16 + (w - 32) * (i + 0.5) / 6 + rng.normal(0, 2)
        sz_ = z + rng.normal(0, 6)
        b = gp(sx_, sz_, h + 2)
        s = 7.5 * k * 1.6
        sheet.poly([(b[0] - s * 0.55, b[1] - s * 0.9), (b[0] + s * 0.55, b[1] - s * 0.9), (b[0] + s * 0.3, b[1]), (b[0] - s * 0.3, b[1])],
                   lerp(VIRIDIAN, SIENNA, 0.45))
        sheet.ellipse(b[0], b[1] - s * 0.9, s * 0.55, s * 0.2, lerp(tintw(OCHRE, 0.4), SIENNA, 0.25))
        sheet.ellipse(b[0], b[1] - s * 0.9, s * 0.3, s * 0.1, tintw(NAPLES, 0.4))
        for j in (-1, 1):
            lines.line([(b[0] + j * s * 0.45, b[1] - s * 0.6), (b[0] + j * s * 0.75, b[1] - s * 0.72)], lerp(VIRIDIAN, PRUSSIAN, 0.5), 0.8, 1.0)
        shells.append(b)
    V.contour(lines, [gp(x - w / 2, f0, 0), gp(x - w / 2, f0, h), gp(x + w / 2, f0, h), gp(x + w / 2, f1, h)], gp(x, f0)[1])
    V.contour(lines, [gp(x + w / 2, f0, 0), gp(x + w / 2, f0, h)], gp(x, f0)[1])
    c, a = sheet.done()
    lc, la = lines.done()
    out = brushed(c, a, lc, la, EARTH, seed=seed, sizes=(3, 2), keep=0.6, fast=fast)
    return out[0], out[1], shells


def noren_cut(back, seed, fast=False):
    """The noren over the teahouse's door: indigo cloth in two panels, a white turban shell on it (our own mark); its hem
    is free (it stirs: fx noren-sway)."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    dx0, dx1 = TEA["door"]
    z = TEA["z0"] - 4
    top, drop = TEA["lintel"] + 4, 58.0
    for i in range(2):
        u0, u1 = i / 2 + 0.012, (i + 1) / 2 - 0.012
        xa, xb = dx0 + 10 + (dx1 - dx0 - 20) * u0, dx0 + 10 + (dx1 - dx0 - 20) * u1
        q = [gp(xa, z, top), gp(xb, z, top), gp(xb, z, top - drop), gp(xa, z, top - drop)]
        sheet.poly(q, INDIGO)
        lines.line([q[3], q[0], q[1], q[2]], PRUSSIAN, 0.8, 0.7)
    lines.line([gp(dx0 + 4, z, top + 2), gp(dx1 - 4, z, top + 2)], WOOD_SHADE, max(1.0, 5 * kz(z)), 1.0)
    # the mark, white, across the split: a round crest of a shell seen from above (a spiral), our own
    c = gp((dx0 + dx1) / 2, z, top - drop * 0.48)
    s = 10 * kz(z)
    sheet.ellipse(c[0], c[1], s, s, tintw(CERULEAN, 0.88))
    spiral = [(c[0] + s * 0.78 * (1 - t / 11) * math.cos(t), c[1] + s * 0.78 * (1 - t / 11) * math.sin(t)) for t in np.linspace(0, 10, 40)]
    lines.line(spiral, INDIGO, 1.0, 1.0)
    c_, a_ = sheet.done()
    lc, la = lines.done()
    return brushed(c_, a_, lc, la, INDIGO, seed=seed, sizes=(3, 2), keep=0.65, fast=fast)


def kago_cut(back, seed, fast=False):
    """The bearers' palanquin, set down by the mound: an open-sided mountain kago. One long pole carries it (the pole is
    the thing: thick, a little bowed, its far end resting on the mound's foot); under the pole a short hood of matting
    hugs it; under the hood the seat, a shallow woven basket with a low back, slung from the pole by two bamboo slings
    at each end; a blue cushion in it. Empty (Little Sister in it is only a wrong try)."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    K = KAGO
    x, z, L, Wd, Hh, pole = K["x"], K["z"], K["length"], K["width"], K["height"], K["pole"]
    k = kz(z)
    bam_lit, bam_sh, bam_dk = lerp(tintw(OCHRE, 0.45), VERONESE, 0.10), lerp(OCHRE, PRUSSIAN, 0.36), lerp(OCHRE, PRUSSIAN, 0.58)
    mat_lit, mat_sh = lerp(tintw(OCHRE, 0.30), SIENNA, 0.18), lerp(lerp(OCHRE, SIENNA, 0.5), PRUSSIAN, 0.42)
    pole_c = lerp(SIENNA, PRUSSIAN, 0.40)
    z0, z1 = z - Wd / 2, z + Wd / 2
    xa, xb = x - L / 2, x + L / 2
    seat_h = 26.0
    # the pole, from its near (left) end held up on a short forked rest to its far end on the mound's foot
    def pole_y(u):
        return Hh + 18 - 30 * u + 5 * math.sin(math.pi * u)
    us = np.linspace(0, 1, 11)
    pp = [gp(x - pole / 2 + pole * u, z, pole_y(u)) for u in us]
    # the hood: a short arched roof of matting slung under the pole over the seat (its near face lit, its hem in shade)
    def py_at(xx):
        return pole_y((xx - (x - pole / 2)) / pole)
    hood_top = [gp(xx, z, py_at(xx) - 4) for xx in np.linspace(xa - 10, xb + 10, 9)]
    hood_hem = [gp(xx, z0 - 6, py_at(xx) - 34 - 6 * math.sin(math.pi * (xx - xa + 10) / (L + 20))) for xx in np.linspace(xa - 10, xb + 10, 9)]
    sheet.poly(hood_top + list(reversed(hood_hem)), mat_lit)
    sheet.poly(hood_hem + [(p[0], p[1] + 3.2) for p in reversed(hood_hem)], mat_sh)
    for i in range(1, 8):
        lines.line([hood_top[i], hood_hem[i]], lerp(SIENNA, PRUSSIAN, 0.35), 0.6, 0.5)
    # the slings: at each end of the seat two bamboo slips from the pole down to its corners (a narrow V)
    for xe in (xa + 6, xb - 6):
        top_ = gp(xe, z, py_at(xe) - 2)
        for zz in (z0 + 4, z1 - 4):
            lines.line([top_, gp(xe, zz, seat_h)], bam_lit if zz < z else bam_sh, max(1.0, 3.4 * k), 1.0)
    # the seat: a shallow woven basket with a low back at its right end, the cushion in it
    sheet.poly([gp(xa, z0, seat_h), gp(xb, z0, seat_h), gp(xb, z1, seat_h), gp(xa, z1, seat_h)], lerp(bam_dk, PRUSSIAN, 0.2))
    sheet.poly([gp(xa + 8, z0 + 8, seat_h + 1), gp(xb - 16, z0 + 8, seat_h + 1), gp(xb - 16, z1 - 8, seat_h + 1), gp(xa + 8, z1 - 8, seat_h + 1)], lerp(INDIGO, WHITE, 0.15))
    sheet.poly([gp(xb - 8, z0 + 6, seat_h), gp(xb - 8, z1 - 6, seat_h), gp(xb - 8, z1 - 6, seat_h + 34), gp(xb - 8, z0 + 6, seat_h + 34)], bam_sh)
    sheet.poly([gp(xa, z0, 0), gp(xb, z0, 0), gp(xb, z0, seat_h), gp(xa, z0, seat_h)], bam_lit)
    sheet.poly([gp(xb, z0, 0), gp(xb, z1, 0), gp(xb, z1, seat_h), gp(xb, z0, seat_h)], bam_sh)
    for v in (8.0, 16.0):
        lines.line([gp(xa, z0, v), gp(xb, z0, v)], bam_dk, 0.7, 0.55)
    for u in np.linspace(0.1, 0.9, 6):
        lines.line([gp(xa + L * u, z0, 1), gp(xa + L * u, z0, seat_h - 1)], bam_dk, 0.55, 0.45)
    lines.line([gp(xa, z0, seat_h), gp(xb, z0, seat_h)], bam_lit, max(1.0, 3.4 * k), 1.0)
    # the pole over everything, and the forked rest under its near end
    rest = gp(x - pole / 2 + 18, z, 0)
    lines.line([rest, gp(x - pole / 2 + 18, z, pole_y(18 / pole) - 4)], bam_sh, max(1.0, 3.2 * k), 1.0)
    lines.line(pp, pole_c, max(2.0, 9.5 * k), 1.0)
    lines.line([(p[0], p[1] - max(1.0, 2.8 * k)) for p in pp], lerp(tintw(OCHRE, 0.25), SIENNA, 0.25), max(0.9, 3.0 * k), 1.0)
    for e in (pp[0], pp[-1]):
        sheet.ellipse(e[0], e[1], max(1.4, 4.5 * k), max(1.4, 4.5 * k), lerp(tintw(OCHRE, 0.3), SIENNA, 0.4))
    V.contour(lines, [gp(xa, z0, 0), gp(xa, z0, seat_h), gp(xb, z0, seat_h), gp(xb, z1, seat_h)], gp(x, z0)[1], alpha=0.6)
    V.contour(lines, hood_hem, gp(x, z0)[1], alpha=0.5)
    V.contour(lines, [gp(xa, z0, 0), gp(xb, z0, 0), gp(xb, z1, 0)], gp(x, z0)[1], alpha=0.5)
    c, a = sheet.done()
    lc, la = lines.done()
    out = brushed(c, a, lc, la, EARTH, seed=seed, sizes=(4, 2), keep=0.55, fast=fast)
    return out[0], out[1]


def trunks_cut(back, seed, fast=False):
    """Soshichi's willow trunks, set down at the road's edge: five tiers stacked on their carrying cloth, the top one's lid
    up (the ledger on it), a strap; the peddler's sprite carries them on the road (PEOPLE-21A): this is the load set down."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    T = TRUNKS
    x, z, w, d, tier, n = T["x"], T["z"], T["w"], T["d"], T["tier"], T["n"]
    k = kz(z)
    willow_lit, willow_sh = lerp(tintw(OCHRE, 0.48), NAPLES, 0.15), lerp(OCHRE, PRUSSIAN, 0.35)
    z0, z1 = z - d / 2, z + d / 2
    # the carrying cloth spread under them (indigo, its corners loose)
    sheet.poly([gp(x - w / 2 - 22, z0 - 14, 1), gp(x + w / 2 + 26, z0 - 10, 1), gp(x + w / 2 + 20, z1 + 14, 1), gp(x - w / 2 - 18, z1 + 10, 1)], lerp(INDIGO, WHITE, 0.08))
    for i in range(n):
        y0, y1 = 2 + i * tier, 2 + (i + 1) * tier - 1.5
        sheet.poly([gp(x - w / 2, z0, y0), gp(x + w / 2, z0, y0), gp(x + w / 2, z0, y1), gp(x - w / 2, z0, y1)], willow_lit)
        sheet.poly([gp(x + w / 2, z0, y0), gp(x + w / 2, z1, y0), gp(x + w / 2, z1, y1), gp(x + w / 2, z0, y1)], willow_sh)
        lines.line([gp(x - w / 2, z0, y1), gp(x + w / 2, z0, y1), gp(x + w / 2, z1, y1)], lerp(SIENNA, PRUSSIAN, 0.35), 0.8, 0.8)
        for u in (0.25, 0.5, 0.75):                                   # the weave: a few vertical lines
            lines.line([gp(x - w / 2 + w * u, z0, y0 + 2), gp(x - w / 2 + w * u, z0, y1 - 2)], lerp(OCHRE, PRUSSIAN, 0.45), 0.5, 0.5)
    yt = 2 + n * tier
    sheet.poly([gp(x - w / 2, z0, yt), gp(x + w / 2, z0, yt), gp(x + w / 2, z1, yt), gp(x - w / 2, z1, yt)], lerp(willow_sh, PRUSSIAN, 0.2))   # open: the inside
    # the lid propped up behind, and the ledger on the stack's top (a dark-covered book)
    sheet.poly([gp(x - w / 2, z1, yt), gp(x + w / 2, z1, yt), gp(x + w / 2, z1 + 8, yt + 30), gp(x - w / 2, z1 + 8, yt + 30)], willow_lit)
    sheet.poly([gp(x - 14, z0 + 8, yt + 1), gp(x + 10, z0 + 8, yt + 1), gp(x + 10, z0 + 24, yt + 1), gp(x - 14, z0 + 24, yt + 1)], lerp(INDIGO, PRUSSIAN, 0.2))
    # a strap down its side
    lines.line([gp(x - w / 2 + 8, z0, 2), gp(x - w / 2 + 8, z0, yt)], lerp(SIENNA, PRUSSIAN, 0.5), max(0.8, 3 * k), 1.0)
    V.contour(lines, [gp(x - w / 2, z0, 2), gp(x - w / 2, z0, yt), gp(x - w / 2, z1 + 8, yt + 30), gp(x + w / 2, z1 + 8, yt + 30), gp(x + w / 2, z0, yt), gp(x + w / 2, z0, 2)],
              gp(x, z0)[1])
    c, a = sheet.done()
    lc, la = lines.done()
    out = brushed(c, a, lc, la, EARTH, seed=seed, sizes=(3, 2), keep=0.6, fast=fast)
    return out[0], out[1]


def front_cut(back, seed, fast=False):
    """The front plane: the near verge at the bottom edge, grass and two stones, and a worn-out straw sandal a traveller
    left there (they were changed every 40 or 50 km)."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    rng = np.random.default_rng(seed)
    for i in range(26):
        xx = rng.uniform(-10, 250) if i < 15 else rng.uniform(560, 810)
        tuft(sheet, xx, 600 + rng.uniform(0, 6), rng.uniform(14, 26), seed + i, lean=0.25, n=8, width=1.6)
    for (cx_, cy_, rx_, ry_) in ((96, 599, 30, 12), (640, 601, 38, 14)):
        sheet.ellipse(cx_, cy_, rx_, ry_, STONE)
        sheet.ellipse(cx_ - rx_ * 0.2, cy_ - ry_ * 0.35, rx_ * 0.65, ry_ * 0.45, STONE_LIT)
        lines.line([(cx_ - rx_, cy_), (cx_ - rx_ * 0.6, cy_ - ry_ * 0.85), (cx_ + rx_ * 0.4, cy_ - ry_ * 0.9), (cx_ + rx_, cy_ - ry_ * 0.2)], PRUSSIAN, 1.0, 0.8)
    # the sandal: an oval of plaited straw, its cords loose
    sx_, sy_ = 168.0, 594.0
    sheet.ellipse(sx_, sy_, 13, 4.2, lerp(tintw(OCHRE, 0.35), SIENNA, 0.2))
    for j in range(5):
        lines.line([(sx_ - 11 + j * 5.5, sy_ - 3), (sx_ - 11 + j * 5.5, sy_ + 3)], lerp(OCHRE, PRUSSIAN, 0.45), 0.7, 0.7)
    lines.line([(sx_ - 9, sy_ - 2), (sx_ - 2, sy_ - 9), (sx_ + 6, sy_ - 4)], lerp(tintw(OCHRE, 0.25), SIENNA, 0.2), 1.0, 1.0)
    c, a = sheet.done()
    lc, la = lines.done()
    out = brushed(c, a, lc, la, GRASS, seed=seed, sizes=(4, 2), keep=0.5, fast=fast)
    return out[0], out[1]


ORDER = ["cloud", "kago", "noren", "trunks", "grill", "front"]


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
    planes["kago"] = kago_cut(pic, 12, fast)
    planes["trunks"] = trunks_cut(pic, 13, fast)
    c, a, info["shells"] = grill_cut(pic, 14, fast)
    planes["grill"] = (c, a)
    planes["noren"] = noren_cut(pic, 15, fast)
    planes["front"] = front_cut(pic, 16, fast)
    whole = comp_all(pic, planes)
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-all.png")
    clear = pic.copy()
    Image.fromarray((np.clip(comp_all(pic, planes, [n for n in ORDER if n != "cloud"]), 0, 1) * 255).astype(np.uint8)).save(OUT + "-3-clear.png")
    import edo_kurasawa_layout
    with open(OUT + "/layout.json", "w") as f:
        json.dump(edo_kurasawa_layout.layout(planes, info), f, indent=1)
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    print("back", finish(pic, OUT + "/back.png", 152))
    for name, n in (("cloud", 24), ("kago", 48), ("trunks", 40), ("grill", 48), ("noren", 24), ("front", 48)):
        print(name, finish(planes[name][0], OUT + f"/{name}.png", n, planes[name][1]))
    print("done", round(time.time() - t0, 1))

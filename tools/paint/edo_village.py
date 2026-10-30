"""PAINT-20A: Yui, a post town of the Tokaido on Suruga Bay under the Satta pass, about 8 April 1830, early morning
(edo-village). In the woodblock manner of the act's style sheet (S/work-20-paintA/style.md): flat masses, a graded sky,
one fine contour in prussian blue, few paints, the blue leading.

LIGHT   The sun is in the east, behind us and to the left, 30 degrees up (edo_village_kit.SUN3): faces turned to us and
        to the left are lit, shadows fall to the right and away, flat and blue.
DEPTH   horizon 300, full 590 (persp.Camera; everything standing is drawn through it).
TONES   light: Fuji's snow, the sky and the bay at the horizon (the paper), the sunlit sand. middle: the deep sky, the
        near water, the beach, the roofs. dark: the hulls, the net racks, the board's posts, the pines of the pass, the
        contour. Fuji owns the picture; the shop (near right) and the board (middle) are where the eye goes next.
PLACE   The street and the shore run from the lower left away to the right (edo_village_kit: x = a + 0.6 z). Left and
        middle: the beach, the big boat on its props (bottom left), the net racks, Gonroku's tender at the water's edge,
        the bay and, far out, his freighter at anchor; across the bay, Fuji. Right: Kihei's shop, its open front (the
        noren) facing the beach; the hen yard behind its low bamboo fence in the near right corner; the notice-board
        place and the well on the seaward side of the street; the far roofs of the village; the Satta pass closing the
        shore at the upper right, the shrine path and its cherry at its foot, the road climbing it.

  python3 edo_village.py fast     the composition without the brush pass (out/edo-village-1-under.png, -2-all.png)
  python3 edo_village.py          the full passes: out/edo-village/ (back.png, the cut-outs, layout.json)
"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
import sky as skylib
import land
from edo_village_kit import *
import edo_village_kit as K

SEED = 1830
OUT = "out/edo-village"
SHAPE = (H, W)

# ---------------------------------------------------------------- where things are (cm; see the module's PLACE)
SHOP = dict(z0=650.0, z1=1150.0, depth=450.0, eave=230.0, ridge=440.0, over=45.0)       # along the street, its near gable to the beach
YARD = dict(x0=230.0, x1=820.0, z0=40.0, z1=330.0, fence=55.0)                            # the hen yard, near right
BOARD = dict(z=1400.0, off=-280.0, w=170.0, post=240.0, roof=300.0)                        # the notice-board place, seaward side
WELL = dict(z=2100.0, off=-300.0, r=45.0, h=70.0)
RACKS = [dict(x=-600.0, z=1000.0, w=300.0, h=170.0), dict(x=-250.0, z=1250.0, w=260.0, h=165.0)]
BIGBOAT = dict(stern=(-900.0, 900.0), length=650.0, beam=75.0, prop=52.0, side=62.0)
TENDER = dict(stern=(-700.0, 1750.0), length=430.0, beam=52.0, prop=0.0, side=45.0)
INLAND = (0.857, -0.514)                                   # the unit vector inland (square to the street), toward us and right
SHIP_AT = (168.0, 318.0)                                   # Gonroku's freighter at anchor, far out (picture place of its waterline middle)
FAR_SHORE_ROW = 301


def inland(x, z, d):
    return x + INLAND[0] * d, z + INLAND[1] * d


# ================================================================ pass 1: broad and flat
def paint_sky(seed):
    """The graded band: deep at the top, the paper at the horizon; seven bands (style.md section 3)."""
    rows = [0, 44, 92, 140, 186, 226, 258, HZ + 2]
    cols = [shade(COBALT, 0.42), mixp(COBALT, ULTRA, 0.3), COBALT, mixp(COBALT, CERULEAN, 0.55), CERULEAN,
            tintw(CERULEAN, 0.55), PAPER, PAPER]
    pic = bands(SHAPE, rows, cols, soft=6.0, wobble=2.5, seed=seed, patch=0.02)
    # the sun is behind us on the left: the paper warms a breath that way
    x, y = grid(SHAPE)
    glow(pic, tintw(NAPLES, 0.5), (np.clip(1 - x / 420.0, 0, 1) * np.clip(1 - np.abs(y - 272) / 70.0, 0, 1) * 0.10).astype(F32))
    return pic


def fuji_mask():
    """Fuji across the bay: the great concave cone, summit at (300, 80), its foot lost at the far shore."""
    x, y = grid(SHAPE)
    sx, sy = 300.0, 80.0
    # the half-width of the cone at each row: a concave flank (wider faster near the foot)
    t = np.clip((y - sy) / (HZ + 4 - sy), 0, 1)
    half = 12 + 470 * t ** 1.7
    # the summit is a little flattened, with its notch (the crater's lip) toward the right
    cap = np.clip((y - sy) / 9.0, 0, 1)
    half = half * (0.55 + 0.45 * cap)
    m = (np.abs(x - sx - 6 * (1 - cap)) < half) & (y >= sy) & (y < HZ + 4)
    m = m.astype(F32)
    m = warp(m, 1.4, 40, 7)
    return np.clip(m, 0, 1)


def paint_fuji(pic, seed):
    x, y = grid(SHAPE)
    m = fuji_mask()
    sx = 300.0
    # the flanks: cobalt and white far down, bluer in the right-hand (shaded) flank, lost in the paper at the foot
    left = np.clip((sx - x) / 300.0, -1, 1)
    flank_lit, flank_shade = tintw(COBALT, 0.46), tintw(mixp(COBALT, ULTRA, 0.35), 0.30)
    flank = np.where((x < sx + 10 + 0.08 * (y - 80))[..., None], flank_lit, flank_shade).astype(F32)
    haze_t = np.clip((y - 232) / 70.0, 0, 1) ** 1.4
    body = lerp(flank, PAPER, haze_t[..., None] * 0.80)
    over(pic, body, m)
    # the snow: well down the flanks (to row ~190), its edge ragged, fingers down the gullies
    gul = noise(SHAPE, (26, 90), seed + 3, 3)
    snow_edge = 172 + (gul - 0.5) * 40 + np.clip(np.abs(x - sx) / 110.0, 0, 1) ** 2 * 30
    snow = step(snow_edge + 3, snow_edge - 3, y) * m
    snow_c = np.where((x < sx + 4)[..., None], WHITE, tintw(CERULEAN, 0.74)).astype(F32)
    over(pic, snow_c, snow)
    # the far shore across the bay: a thin band of land at the foot of everything, pale and blue, no line
    shore = mask_poly(SHAPE, [(-10, FAR_SHORE_ROW - 10), (120, FAR_SHORE_ROW - 11), (330, FAR_SHORE_ROW - 9), (470, FAR_SHORE_ROW - 12), (600, FAR_SHORE_ROW - 8),
                              (640, FAR_SHORE_ROW - 6), (640, HZ + 2), (-10, HZ + 2)], soft=0.8, wobble=1.5, seed=seed + 4)
    over(pic, tintw(mixp(COBALT, VIRIDIAN, 0.35), 0.62), shore)
    return m, snow


def paint_pass(pic, seed):
    """The Satta pass: a steep green headland closing the shore at the upper right, the road climbing it. Middle distance:
    two flats and their shade, pine clumps along the skyline, no contour."""
    x, y = grid(SHAPE)
    crest = [(520, HZ + 1), (560, 282), (600, 262), (640, 236), (680, 214), (716, 196), (750, 180), (780, 172), (812, 166)]
    m, line = land.ridge(SHAPE, crest, HZ + 40, seed + 11, rough=1.6)
    m = m * (y < HZ + 1) * (x >= crest[0][0] - 4)                   # (ridge holds its first value across the picture: keep it to its own columns, above the horizon)
    base_c = lerp(tintw(VIRIDIAN, 0.22), PAPER, 0.28)
    body = flat(base_c, SHAPE, seed + 12, 0.03, 70)
    over(pic, body, m)
    # the sunlit faces: the slopes that turn to the left and to us take veronese green
    n = warp(noise(SHAPE, (40, 60), seed + 13, 3), 6.0, 30, seed + 14)
    facing = np.clip((np.roll(n, -3, axis=1) - n) * 7.0, 0, 1)
    lit_m = step(0.45, 0.75, n * 0.5 + facing * 0.5) * m
    over(pic, lerp(VERONESE, PAPER, 0.25), (lit_m * 0.85).astype(F32))
    # the shade side under the crest and in the folds: viridian toward prussian
    fold = step(0.55, 0.8, noise(SHAPE, (30, 80), seed + 15, 3)) * m
    over(pic, lerp(VIRIDIAN, PRUSSIAN, 0.3), (fold * 0.7).astype(F32))
    # the foot of it is paler (the air)
    up = np.clip((HZ + 40 - y) / 160.0, 0, 1)
    over(pic, PAPER, (m * (1 - up) ** 2 * 0.5).astype(F32))
    return m, line


def water_region():
    """Where the bay is seen: below the horizon, seaward of the water's edge (the shore line in the picture)."""
    pts = [gp(shore_x(z), z) for z in np.geomspace(60000, 700, 40)]
    poly = [(-10, HZ - 1), (W + 10, HZ - 1), (W + 10, pts[0][1])] + pts + [(-10, pts[-1][1] + 20)]
    return mask_poly(SHAPE, poly, soft=0.8, wobble=1.2, seed=3)


def paint_bay(pic, seed):
    """The bay in seven bands (style.md section 3): the paper at the horizon, cerulean, cobalt in the middle distance,
    toward ultramarine at the near edge; each band a flat, the boundaries soft and level. The near water's light is the
    engine's shimmer; the far rows of wave-curls are painted still in details()."""
    x, y = grid(SHAPE)
    wm = water_region()
    rows = [HZ, HZ + 7, HZ + 17, HZ + 32, HZ + 54, HZ + 84, HZ + 124, HZ + 180]
    cols = [tintw(CERULEAN, 0.62), tintw(CERULEAN, 0.40), tintw(CERULEAN, 0.16), mixp(CERULEAN, COBALT, 0.42), mixp(CERULEAN, COBALT, 0.75),
            COBALT, mixp(COBALT, ULTRA, 0.3), mixp(COBALT, ULTRA, 0.3)]
    wb = bands(SHAPE, rows, cols, soft=3.5, wobble=0.0, seed=seed + 20, patch=0.015)
    over(pic, wb, wm)
    # a thread of white where the water meets the sand (the last of a wave), and the wet sand's blue just inside it
    zs = np.geomspace(60000, 700, 40)
    edge_pts = [gp(shore_x(z), z) for z in zs]
    line = mask_line(SHAPE, edge_pts, [max(0.8, kz(z) * 2.4) for z in zs], soft=0.5)
    over(pic, WHITE, (line * 0.7 * wm).astype(F32))
    return wm


def paint_ground(pic, seed, wm):
    """The beach (grey sand and pebbles) and the street (packed earth, 30 cm up, a sand slope between)."""
    x, y = grid(SHAPE)
    X, Z, below = floor(SHAPE)
    ground = below * (1 - wm)
    sand = flat(SAND, SHAPE, seed + 30, 0.05, 40)
    # paler and bluer far off (the air), a little warmer at our feet
    t = np.clip((y - HZ) / (H - HZ), 0, 1)
    sand = lerp(sand, PAPER, ((1 - t) ** 1.6 * 0.45)[..., None])
    sand = lerp(sand, lerp(SAND, OCHRE, 0.10), (t ** 2 * 0.22)[..., None])
    over(pic, sand, ground)
    # wet sand in a band above the water's edge (the tide went out an hour ago)
    wet_pts = [gp(shore_x(z) - 110, z) for z in np.geomspace(60000, 700, 40)]
    wet = mask_line(SHAPE, wet_pts, [max(1.0, kz(z) * 110 * 2.0) for z in np.geomspace(60000, 700, 40)], soft=2.0) * ground
    over(pic, SAND_WET, (wet * 0.6).astype(F32))
    # the street: the Tokaido running along behind the beach, with its low bank toward the beach
    st = mask_poly(SHAPE, along(STREET_A, 20, 7000, 10, across=STREET_W) + along(STREET_A, 7000, 20, 10, across=-STREET_W), soft=1.0, wobble=2.0, seed=seed + 31)
    earth = flat(EARTH, SHAPE, seed + 32, 0.04, 50)
    earth = lerp(earth, PAPER, ((1 - t) ** 1.6 * 0.45)[..., None])
    over(pic, earth, (st * ground).astype(F32))
    # the bank: the street stands RISE above the beach; its seaward edge is a sand slope a step wide, in shade
    bank = mask_poly(SHAPE, along(STREET_A, 20, 7000, 10, across=-STREET_W) + along(STREET_A, 7000, 20, 10, across=-STREET_W - 0.55), soft=0.8, wobble=1.5, seed=seed + 33)
    over(pic, lerp(SAND, COBALT, 0.22), (bank * ground * 0.8).astype(F32))
    # a worn way up from the beach to the street, and along the street where feet go
    over(pic, lerp(EARTH, PAPER, 0.25), (mask_line(SHAPE, [gp(x_, z_) for x_, z_ in ((-650, 500), (-480, 420), (-330, 330))], [26, 22, 18], soft=3.0) * ground * 0.35).astype(F32))
    return ground, st


def cast_shadows(pic, ground):
    """Every standing thing's shadow, flat and blue, laid along the sun (SUN)."""
    sh = Paper(SHAPE)
    # the shop: its eave line and its gable, laid flat
    z0, z1, d, e = SHOP["z0"], SHOP["z1"], SHOP["depth"], SHOP["eave"]
    x0, x1 = front_x(z0), front_x(z1)
    bx0, bz0 = inland(x0, z0, d)
    bx1, bz1 = inland(x1, z1, d)
    pts = [(x0, 0, z0), (x1, 0, z1), (x1, e, z1), (x0, e, z0)]
    sh.poly(shadow_pts(pts) + [gp(x1, z1), gp(x0, z0)], SAND_SHADE, 1.0)
    sh.poly(shadow_pts([(x0, e, z0), (x0, e, z0), (bx0, e, bz0), (bx0, 0, bz0)]) + [gp(x0, z0)], SAND_SHADE, 1.0)
    # the hen fence and the board's roof and posts, the racks, the well, the boats
    for (xa, za, xb, zb) in ((YARD["x0"], YARD["z0"], YARD["x0"], YARD["z1"]), (YARD["x0"], YARD["z1"], YARD["x1"], YARD["z1"])):
        sh.poly(shadow_pts([(xa, YARD["fence"], za), (xb, YARD["fence"], zb)]) + [gp(xb, zb), gp(xa, za)], SAND_SHADE, 0.85)
    bz = BOARD["z"]
    bx = street_x(bz, 0) + BOARD["off"]
    hw = BOARD["w"] / 2
    pa, pb = inland(bx, bz, 0), inland(bx, bz, 0)
    cx0, cz0 = bx - 0.514 * hw, bz - 0.857 * hw                       # the board runs along the street
    cx1, cz1 = bx + 0.514 * hw, bz + 0.857 * hw
    sh.poly(shadow_pts([(cx0, 0, cz0), (cx1, 0, cz1), (cx1, BOARD["post"], cz1), (cx0, BOARD["post"], cz0)]), SAND_SHADE, 0.9)
    for r in RACKS:
        sh.poly(shadow_pts([(r["x"], 0, r["z"]), (r["x"] + r["w"] * 0.76, 0, r["z"] + r["w"] * 0.64), (r["x"] + r["w"] * 0.76, r["h"], r["z"] + r["w"] * 0.64), (r["x"], r["h"], r["z"])]), SAND_SHADE, 0.85)
    wz = WELL["z"]
    wx = street_x(wz) + WELL["off"]
    sh.poly(shadow_pts([(wx - WELL["r"], 0, wz), (wx + WELL["r"], 0, wz), (wx + WELL["r"], WELL["h"], wz), (wx - WELL["r"], WELL["h"], wz)]), SAND_SHADE, 0.8)
    for b in (BIGBOAT, TENDER):
        sx_, sz_ = b["stern"]
        ex, ez = inland(sx_, sz_, b["length"])
        top = b["prop"] + b["side"]
        sh.poly(shadow_pts([(sx_, top, sz_), (ex, top, ez), (ex, b["prop"], ez), (sx_, b["prop"], sz_)]), SAND_SHADE, 0.9)
        sh.poly(shadow_pts([(sx_ - 0.514 * b["beam"], top, sz_ - 0.857 * b["beam"]), (ex, top, ez), (ex, b["prop"], ez), (sx_, b["prop"], sz_)]), SAND_SHADE, 0.9)
    c, a = sh.done()
    over(pic, c, (a * ground).astype(F32))
    return a


def under(seed=SEED):
    info = {}
    pic = paint_sky(seed)
    info["sky"] = pic.copy()
    info["fuji"], info["snow"] = paint_fuji(pic, seed)
    info["pass"], info["pass_line"] = paint_pass(pic, seed)
    info["water"] = paint_bay(pic, seed)
    info["ground"], info["street"] = paint_ground(pic, seed, info["water"])
    info["shadow"] = cast_shadows(pic, info["ground"])
    land.haze(pic, HZ, PAPER, 0.32, 0.10, info["ground"])
    return np.clip(pic, 0, 1), info


# ================================================================ pass 3: the crisp things (the backdrop's)
U = (0.514, 0.857)                                          # along the street, away from us
N_IN = (0.857, -0.514)                                       # inland (square to the street): toward us and the right


def house(sheet, lines, z0, z1, depth, eave, ridge, over_, walls=(PLASTER_LIT, PLASTER_SHADE), roof=(SHINGLE_LIT, SHINGLE_SHADE),
          gable_open=None, stones=True, thatch=False, a=None, lift=0.0):
    """A house along the street (its seaward side on x = a + M z from z0 to z1, its depth inland), under a hipped roof.
    From this camera its seaward side is turned away: what shows is the near end wall (lit: it faces us and the left),
    the inland side (shade), the near hip of the roof (lit) and the inland slope (shade), split at the hip in one hard
    line. Each face is one flat; the contour goes round the silhouette and the corners only. `gable_open` = (width,
    height) cuts the open shop front into the near end wall; `lift` raises the house (the slope up to the pass)."""
    a = FRONT_A if a is None else a
    F0 = (a + M * z0, z0)
    F1 = (a + M * z1, z1)
    B0 = (F0[0] + N_IN[0] * depth, F0[1] + N_IN[1] * depth)
    B1 = (F1[0] + N_IN[0] * depth, F1[1] + N_IN[1] * depth)
    P = lambda q, y=0.0: gp(q[0], q[1], lift + y)
    hip = depth / 2 * 0.95
    Mn = ((F0[0] + B0[0]) / 2 + U[0] * hip, (F0[1] + B0[1]) / 2 + U[1] * hip)       # the ridge's near end
    Mf = ((F1[0] + B1[0]) / 2 - U[0] * hip, (F1[1] + B1[1]) / 2 - U[1] * hip)       # and its far end
    ov = over_
    eF0 = (F0[0] - U[0] * ov - N_IN[0] * ov, F0[1] - U[1] * ov - N_IN[1] * ov)
    eB0 = (B0[0] - U[0] * ov + N_IN[0] * ov, B0[1] - U[1] * ov + N_IN[1] * ov)
    eB1 = (B1[0] + U[0] * ov + N_IN[0] * ov, B1[1] + U[1] * ov + N_IN[1] * ov)
    e_h = eave - ov * 0.5                                            # the eave's edge, a little below the wall top (the roof's pitch)
    wall_lit, wall_sh = walls
    roof_lit, roof_sh = (THATCH_LIT, THATCH_SHADE) if thatch else roof
    row0 = P(F0)[1]
    # ---- the walls: the near end (lit) and the inland side (shade)
    end = [P(F0), P(B0), P(B0, eave), P(F0, eave)]
    sheet.poly(end, wall_lit)
    sheet.poly([P(B0), P(B1), P(B1, eave), P(B0, eave)], wall_sh)
    if gable_open:
        ow, oh = gable_open
        I0 = (F0[0] + N_IN[0] * 25, F0[1] + N_IN[1] * 25)
        I1 = (F0[0] + N_IN[0] * (25 + ow), F0[1] + N_IN[1] * (25 + ow))
        sheet.poly([P(I0), P(I1), P(I1, oh), P(I0, oh)], lerp(SIENNA, PRUSSIAN, 0.6))                        # the inside, in shade
        sheet.poly([P(I0, oh * 0.22), P(I1, oh * 0.22), P(I1, oh * 0.27), P(I0, oh * 0.27)], WOOD_SHADE)     # the raised floor's edge, inside
        lines.line([P(I0), P(I0, oh), P(I1, oh), P(I1)], PRUSSIAN, contour_w(row0), 0.8)
        # the sill: a beam across the opening's foot
        lines.line([P(I0, 2), P(I1, 2)], WOOD_LIT, max(1.0, 8 * kz(F0[1])), 1.0)
    # the eave's shadow on the walls: one band
    sheet.poly([P(F0, eave), P(B0, eave), P(B0, eave - 16), P(F0, eave - 16)], lerp(wall_lit, COBALT, 0.35))
    sheet.poly([P(B0, eave), P(B1, eave), P(B1, eave - 16), P(B0, eave - 16)], lerp(wall_sh, PRUSSIAN, 0.2))
    # ---- the roof: the near hip (lit) and the inland slope (shade), one hard line between
    hip_face = [P(eF0, e_h), P(eB0, e_h), P(Mn, ridge)]
    slope = [P(eB0, e_h), P(eB1, e_h), P(Mf, ridge), P(Mn, ridge)]
    sheet.poly(hip_face, roof_lit)
    sheet.poly(slope, roof_sh)
    # the eave's underside: a thin dark band under the roof's edge on the near end
    sheet.poly([P(eF0, e_h), P(eB0, e_h), P(eB0, e_h - 5), P(eF0, e_h - 5)], lerp(roof_sh, PRUSSIAN, 0.3))
    if stones and not thatch:
        rng = np.random.default_rng(int(z0) + 3)
        # two rows of weighting stones on each visible face: along the near hip (its base eF0 -> eB0, apex Mn) and the slope
        for (A, B, apex, rows_v) in ((eF0, eB0, Mn, (0.2, 0.5)), (eB0, eB1, Mn, (0.22, 0.6))):
          length = math.hypot(B[0] - A[0], B[1] - A[1])
          for v in rows_v:
            n = max(3, int(length / 85))
            for i in range(n):
                u = (i + 0.5) / n + rng.normal(0, 0.02)
                if A is eF0 and abs(u - 0.5) > 0.5 - v * 0.5:          # the hip narrows toward its apex
                    continue
                qx = A[0] + (B[0] - A[0]) * u + (apex[0] - (A[0] + B[0]) / 2) * v
                qz = A[1] + (B[1] - A[1]) * u + (apex[1] - (A[1] + B[1]) / 2) * v
                q = gp(qx, qz, lift + e_h + (ridge - e_h) * v)
                r = max(1.0, 9 * kz(qz))
                sheet.ellipse(q[0] + r * 0.3, q[1] + r * 0.25, r, r * 0.6, lerp(roof_sh, PRUSSIAN, 0.35))
                sheet.ellipse(q[0], q[1], r, r * 0.7, lerp(tintw(PRUSSIAN, 0.5), OCHRE, 0.12 + 0.12 * rng.random()))
        for v in (0.36, 0.72):                                         # two battens
            pa = gp(eB0[0] + (Mn[0] - eB0[0]) * v, eB0[1] + (Mn[1] - eB0[1]) * v, lift + e_h + (ridge - e_h) * v)
            pb = gp(eB1[0] + (Mf[0] - eB1[0]) * v, eB1[1] + (Mf[1] - eB1[1]) * v, lift + e_h + (ridge - e_h) * v)
            lines.line([pa, pb], PRUSSIAN, 0.6, 0.35)
    if thatch:                                                         # the thatch's eave: a row of short strokes
        length = math.hypot(eB1[0] - eB0[0], eB1[1] - eB0[1])
        n = max(4, int(length / 30))
        for i in range(n):
            u = (i + 0.5) / n
            qx, qz = eB0[0] + (eB1[0] - eB0[0]) * u, eB0[1] + (eB1[1] - eB0[1]) * u
            lines.line([gp(qx, qz, lift + e_h + 2), gp(qx + (Mn[0] - eB0[0]) * 0.1, qz + (Mn[1] - eB0[1]) * 0.1, lift + e_h + 14)], THATCH_SHADE, max(0.5, 2.5 * kz(qz)), 0.6)
    # ---- the contour: the silhouette (eaves, hip, ridge) and the wall corners
    for pts in ([P(eF0, e_h), P(eB0, e_h), P(eB1, e_h)], [P(eF0, e_h), P(Mn, ridge), P(Mf, ridge), P(eB1, e_h)], [P(eB0, e_h), P(Mn, ridge)],
                [P(F0), P(F0, eave)], [P(B0), P(B0, eave)], [P(B1), P(B1, eave)], [P(F0), P(B0), P(B1)]):
        contour(lines, pts, row0)
    return end


def details(pic, info, seed=SEED, fast=False):
    x, y = grid(SHAPE)
    rng = np.random.default_rng(seed + 50)
    ground = info["ground"]
    # ---- Fuji's snow line and the pass, said again crisply (the brush softened them)
    crisp = pic.copy()
    paint_fuji(crisp, seed)
    pic[...] = lerp(pic, crisp, (0.7 * info["fuji"] * (y < HZ))[..., None])
    crisp = pic.copy()
    paint_pass(crisp, seed)
    pic[...] = lerp(pic, crisp, (0.55 * info["pass"] * (y < HZ + 1))[..., None])
    sheet = Paper(SHAPE)
    lines = sheet                                                      # one sheet, in depth order: a far thing's line never lies over a near thing's fill
    # Fuji's shoulders against the sky: a breath of contour (0.5 px, alpha 0.4)
    fm = info["fuji"]
    edge = np.clip(fm - np.roll(fm, 2, axis=0), 0, 1) * (y < 290)
    over(pic, PRUSSIAN, (blur(edge, 0.6) * 0.3).astype(F32))
    # ---- the road up the pass: a pale thread zigzagging to the saddle, and the pines along the skyline
    road = [(566, 296), (610, 282), (640, 268), (628, 258), (668, 244), (704, 228), (690, 220), (736, 204), (770, 190), (796, 182)]
    lines.line(road, lerp(PAPER, OCHRE, 0.3), 1.2, 0.75)
    for (px, py_, hgt) in ((560, 284, 10), (596, 266, 12), (636, 240, 13), (676, 218, 12), (712, 200, 14), (748, 184, 13), (780, 176, 15)):
        sheet.line([(px, py_), (px, py_ - hgt)], lerp(VIRIDIAN, PRUSSIAN, 0.5), 1.0)
        for j, (dx, dy, rx, ry) in enumerate(((-0.3, -0.55, 0.42, 0.14), (0.25, -0.7, 0.4, 0.14), (0.0, -0.9, 0.32, 0.13))):
            sheet.ellipse(px + dx * hgt, py_ + dy * hgt, rx * hgt, ry * hgt, lerp(VIRIDIAN, PRUSSIAN, 0.35 - 0.08 * j))
    # ---- the far village. Beyond the shop the inland side is hidden behind it; what shows is the row of small houses on
    # the seaward side of the street, far along (their near ends lit, their roofs in shade), and two houses up the slope
    # toward the pass, raised on the hillside, showing over the shop's roof at the right.
    for (z0, z1, kind) in ((2500.0, 2900.0, "thatch"), (3000.0, 3400.0, "shingle"), (3550.0, 4000.0, "thatch"), (4150.0, 4700.0, "shingle")):
        house(sheet, lines, z0, z1, 380.0, 200.0, 360.0, 40.0, a=STREET_A - STREET_W - 400.0, thatch=(kind == "thatch"))
    for (z0, z1, lift_, kind) in ((2300.0, 2750.0, 330.0, "shingle"), (2900.0, 3350.0, 520.0, "thatch")):
        house(sheet, lines, z0, z1, 400.0, 210.0, 380.0, 40.0, a=FRONT_A + 380.0, lift=lift_, thatch=(kind == "thatch"))
    # the shrine path up the slope among them, its steps a pale zigzag, a small plain gate; the cherry beside it, past
    # its best (the petals fall there: fx petals), a drift of fallen petals under it
    steps = [(708, 296), (722, 284), (716, 277), (734, 262), (748, 250), (742, 244), (760, 230), (776, 220), (792, 212)]
    lines.line(steps, lerp(PAPER, PRUSSIAN, 0.25), 1.0, 0.7)
    for gx_ in (732, 740):
        sheet.line([(gx_, 276), (gx_, 254)], lerp(VERMILION, PRUSSIAN, 0.25), 1.3)
    sheet.line([(728, 255), (744, 255)], lerp(VERMILION, PRUSSIAN, 0.25), 1.6)
    cx_, cy_ = 688.0, 286.0
    sheet.line([(cx_, cy_), (cx_ - 3, cy_ - 22), (cx_ - 8, cy_ - 34)], lerp(SIENNA, PRUSSIAN, 0.4), 2.0)
    sheet.line([(cx_ - 3, cy_ - 22), (cx_ + 8, cy_ - 38)], lerp(SIENNA, PRUSSIAN, 0.4), 1.4)
    for (dx, dy, r) in ((-18, -42, 16), (8, -50, 17), (-4, -34, 12), (18, -38, 11), (-26, -32, 10), (2, -60, 10)):
        sheet.ellipse(cx_ + dx, cy_ + dy, r, r * 0.8, PINK if dy < -40 else PINK_DEEP)
    sheet.ellipse(cx_ + 2, cy_ + 1, 20, 4, PINK, 0.4)
    info["cherry_box"] = [int(cx_ - 46), int(cy_ - 72), 84, 76]
    # ---- Kihei's shop: the near house on the right; its open front faces the beach (the noren is a cut-out)
    info["shop_gable"] = house(sheet, lines, SHOP["z0"], SHOP["z1"], SHOP["depth"], SHOP["eave"], SHOP["ridge"], SHOP["over"],
                               walls=(tintw(OCHRE, 0.55), lerp(tintw(OCHRE, 0.4), COBALT, 0.3)), gable_open=(185.0, 185.0))
    # ---- the well on the seaward side: a square wooden curb, a roof on two posts, the bucket pole
    wz = WELL["z"]
    wx = street_x(wz) + WELL["off"]
    r = WELL["r"]
    sheet.poly([gp(wx - r, wz - r * 0.8), gp(wx + r, wz - r * 0.8), gp(wx + r, wz - r * 0.8, WELL["h"]), gp(wx - r, wz - r * 0.8, WELL["h"])], WOOD_LIT)
    sheet.poly([gp(wx + r, wz - r * 0.8), gp(wx + r, wz + r * 0.8), gp(wx + r, wz + r * 0.8, WELL["h"]), gp(wx + r, wz - r * 0.8, WELL["h"])], WOOD_SHADE)
    sheet.poly([gp(wx - r, wz - r * 0.8, WELL["h"]), gp(wx + r, wz - r * 0.8, WELL["h"]), gp(wx + r, wz + r * 0.8, WELL["h"]), gp(wx - r, wz + r * 0.8, WELL["h"])], lerp(SIENNA, PRUSSIAN, 0.6))
    for px_, pz_ in ((wx - r * 0.7, wz), (wx + r * 0.7, wz)):
        lines.line([gp(px_, pz_, WELL["h"]), gp(px_, pz_, 230)], WOOD_SHADE, max(0.8, 10 * kz(wz)), 1.0)
    sheet.poly([gp(wx - r * 1.3, wz, 230), gp(wx + r * 1.3, wz, 230), gp(wx + r * 0.9, wz, 262), gp(wx - r * 0.9, wz, 262)], SHINGLE_LIT)
    contour(lines, [gp(wx - r, wz - r * 0.8), gp(wx - r, wz - r * 0.8, WELL["h"]), gp(wx + r, wz - r * 0.8, WELL["h"]), gp(wx + r, wz - r * 0.8)], gp(wx, wz)[1])
    # ---- pebbles and shells on the beach, a line of wrack along the tide line
    stones = Sheet(SHAPE)
    land.stones(stones, pic, HZ, seed + 90, 70, zone=((ground > 0.5) & (y > 380) & (info["street"] < 0.3)), ground=ground, size=(0.7, 2.6),
                tones=(tintw(PRUSSIAN, 0.78), tintw(PRUSSIAN, 0.6), tintw(PRUSSIAN, 0.4), tintw(PRUSSIAN, 0.22)))
    sc, sa = stones.done()
    over(pic, sc, sa)
    sheet.onto(pic)
    return pic


# ================================================================ the cut-outs
def boat_cut(back, b, seed, fast=False):
    """A flat-bottomed fishing boat pulled up on two cross timbers, bow inland (toward us and the right): the near side
    one lit flat with its sheer rising to the bow, the bow planks a shade flat, the inside dark over the gunwale, two
    thwarts, the stem; the gap under it open to the sand. The contour round the silhouette, warm on the lit side."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    sx_, sz_ = b["stern"]
    L, beam, prop, side = b["length"], b["beam"], b["prop"], b["side"]
    n = 16
    near_g, far_g, near_c = [], [], []                                  # the near gunwale, the far gunwale, the near chine
    for i in range(n + 1):
        u = i / n
        cx_, cz_ = inland(sx_, sz_, L * u)
        hw = beam * (0.55 + 0.45 * math.sin(math.pi * min(1.0, u * 1.15)) ** 0.7) if u < 0.87 else beam * (1.0 - (u - 0.87) / 0.13) ** 0.6 * 0.9 + 4
        sheer = side + 6 * (1 - u) ** 2 + 46 * max(0.0, u - 0.55) ** 1.6 / 0.45 ** 1.6
        near_g.append((cx_ - 0.514 * hw, prop + sheer, cz_ - 0.857 * hw))
        far_g.append((cx_ + 0.514 * hw, prop + sheer, cz_ + 0.857 * hw))
        near_c.append((cx_ - 0.514 * hw * 0.92, prop, cz_ - 0.857 * hw * 0.92))
    G = lambda q: gp(q[0], q[2], q[1])
    hull_lit = lerp(tintw(OCHRE, 0.22), PRUSSIAN, 0.12)
    hull_sh = lerp(SIENNA, PRUSSIAN, 0.45)
    inside = lerp(SIENNA, PRUSSIAN, 0.62)
    # the inside, seen over the near gunwale
    sheet.poly([G(q) for q in far_g] + [G(q) for q in reversed(near_g)], inside)
    for u in (0.3, 0.52, 0.74):                                          # thwarts
        i = int(u * n)
        a_, c_ = near_g[i], far_g[i]
        lines.line([gp(a_[0], a_[2], a_[1] - 7), gp(c_[0], c_[2], c_[1] - 7)], WOOD_SHADE, max(0.9, 7 * kz(a_[2])), 1.0)
    # the near side: one lit flat from the gunwale down to the chine
    sheet.poly([G(q) for q in near_g] + [G(q) for q in reversed(near_c)], hull_lit)
    # the bow: the planks turn across the stem, in shade
    tip = inland(sx_, sz_, L + 14)
    bow_top = (tip[0], prop + side + 60, tip[1])
    sheet.poly([G(near_g[-2]), G(bow_top), G(far_g[-2]), G(far_g[-1]), G(near_g[-1])], hull_sh)
    sheet.poly([G(near_g[-1]), G(bow_top), (G(bow_top)[0], G(near_c[-1])[1]), G(near_c[-1])], hull_sh)
    # two plank lines along the side, and the rubbing strake under the gunwale
    for v in (0.42, 0.74):
        lines.line([gp(a_[0], a_[2], a_[1] + (c_[1] - a_[1]) * v) for a_, c_ in zip(near_g, near_c)], PRUSSIAN, 0.65, 0.4)
    lines.line([gp(a_[0], a_[2], a_[1] - 3) for a_ in near_g], lerp(SIENNA, PRUSSIAN, 0.3), max(1.0, 5 * kz(sz_)), 0.9)
    # the stem post
    lines.line([G((tip[0], prop + 2, tip[1])), G(bow_top)], hull_sh, max(1.2, 10 * kz(tip[1])), 1.0)
    # the cross timbers it sits on (the gap between them is open: the sand shows)
    if prop > 0:
        for u in (0.24, 0.70):
            cx_, cz_ = inland(sx_, sz_, L * u)
            a0 = (cx_ - 0.514 * (beam + 28), cz_ - 0.857 * (beam + 28))
            a1 = (cx_ + 0.514 * (beam + 28), cz_ + 0.857 * (beam + 28))
            sheet.poly([gp(*a0), gp(*a1), gp(a1[0], a1[1], 18), gp(a0[0], a0[1], 18)], WOOD_SHADE)
            sheet.poly([gp(a0[0], a0[1], 18), gp(a1[0], a1[1], 18), gp(a1[0], a1[1], prop), gp(a0[0], a0[1], prop)], lerp(WOOD_SHADE, PRUSSIAN, 0.3), 0.9)
            lines.line([gp(*a0), gp(a0[0], a0[1], prop)], PRUSSIAN, 0.7, 0.6)
    # the contour: the sheer, the chine, the stem; warm along the lit side
    r0 = G(near_c[-1])[1]
    contour(lines, [G(q) for q in near_g] + [G(bow_top)], r0, warm=True)
    contour(lines, [G(q) for q in near_c] + [G((tip[0], prop + 2, tip[1]))], r0)
    contour(lines, [G(q) for q in far_g], r0, alpha=0.5)
    c, a = sheet.done()
    lc, la = lines.done()
    ys, xs = np.where(a > 0.5)
    under_c = np.median(back[ys, xs], axis=0) if len(ys) else SAND
    return brushed(c, a, lc, la, under_c, seed=seed, fast=fast)


def brushed(color, alpha, lc, la, under, seed=4, sizes=(6, 3, 2), keep=0.45, fast=False):
    """A cut-out, painted: flats brushed over the colour it stands in front of, its lines put back on top."""
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


def racks_cut(back, seed, fast=False):
    """Nets drying on bamboo racks on the beach: two uprights and a rail, the net hung over it, its lower edge ragged."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    rng = np.random.default_rng(seed)
    for r in RACKS:
        x0, z0 = r["x"], r["z"]
        x1, z1 = x0 + r["w"] * 0.76, z0 + r["w"] * 0.64                # the rack runs along the shore
        k = kz(z0)
        for (px_, pz_) in ((x0, z0), (x1, z1), ((x0 + x1) / 2, (z0 + z1) / 2)):
            lines.line([gp(px_, pz_), gp(px_, pz_, r["h"])], lerp(OCHRE, PRUSSIAN, 0.35), max(1.0, 7 * k), 1.0)
        lines.line([gp(x0, z0, r["h"]), gp(x1, z1, r["h"])], lerp(OCHRE, PRUSSIAN, 0.35), max(1.0, 6 * k), 1.0)
        # the net: a dark veil hanging from the rail, its hem uneven, the mesh drawn as a few crossed lines
        hem = [gp(x0 + (x1 - x0) * u, z0 + (z1 - z0) * u, r["h"] * (0.18 + 0.1 * rng.random())) for u in np.linspace(0, 1, 7)]
        top = [gp(x0 + (x1 - x0) * u, z0 + (z1 - z0) * u, r["h"] - 4) for u in np.linspace(1, 0, 7)]
        sheet.poly(hem + top, lerp(SIENNA, PRUSSIAN, 0.62), 0.92)
        for u in np.linspace(0.05, 0.95, 9):
            p0 = gp(x0 + (x1 - x0) * u, z0 + (z1 - z0) * u, r["h"] - 4)
            p1 = gp(x0 + (x1 - x0) * u + 12, z0 + (z1 - z0) * u, r["h"] * 0.25)
            lines.line([p0, p1], lerp(OCHRE, PRUSSIAN, 0.5), 0.6, 0.45)
        for v in (0.45, 0.65, 0.85):
            lines.line([gp(x0 + (x1 - x0) * u, z0 + (z1 - z0) * u, r["h"] * v) for u in np.linspace(0, 1, 5)], lerp(OCHRE, PRUSSIAN, 0.5), 0.6, 0.4)
        # floats along the hem
        for u in np.linspace(0.1, 0.9, 5):
            p = gp(x0 + (x1 - x0) * u, z0 + (z1 - z0) * u, r["h"] * 0.2)
            sheet.ellipse(p[0], p[1], max(1.0, 5 * k), max(1.0, 5 * k), tintw(OCHRE, 0.3))
        contour(lines, hem, gp(x0, z0)[1])
    c, a = sheet.done()
    lc, la = lines.done()
    ys, xs = np.where(a > 0.5)
    return brushed(c, a, lc, la, np.median(back[ys, xs], axis=0) if len(ys) else SAND, seed=seed, fast=fast)


def board_cut(back, seed, fast=False):
    """The notice-board place at the village entrance: two posts, a little roof, a row of boards dense with writing
    (pattern: columns of short dashes, never characters). The Kirishitan board is among them."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    rng = np.random.default_rng(seed)
    bz = BOARD["z"]
    bx = street_x(bz) + BOARD["off"]
    hw = BOARD["w"] / 2
    ax, az = bx - 0.514 * hw, bz - 0.857 * hw                        # along the street
    cx_, cz_ = bx + 0.514 * hw, bz + 0.857 * hw
    k = kz(bz)
    post_h = BOARD["post"]
    # a low platform of earth faced with stones
    sheet.poly([gp(*inland(ax, az, 60)), gp(*inland(cx_, cz_, 60)), gp(*inland(cx_, cz_, 60), 22), gp(*inland(ax, az, 60), 22)], tintw(PRUSSIAN, 0.5))
    sheet.poly([gp(*inland(ax, az, 60), 22), gp(*inland(cx_, cz_, 60), 22), gp(*inland(cx_, cz_, -40), 22), gp(*inland(ax, az, -40), 22)], tintw(PRUSSIAN, 0.62))
    # the posts
    for px_, pz_ in ((ax, az), (cx_, cz_)):
        lines.line([gp(px_, pz_, 22), gp(px_, pz_, post_h)], WOOD_SHADE, max(1.2, 14 * k), 1.0)
    # the boards: five, hung from a rail, each a pale plank, the writing in columns
    n = 5
    for i in range(n):
        u0, u1 = (i + 0.08) / n, (i + 0.92) / n
        p00 = gp(ax + (cx_ - ax) * u0, az + (cz_ - az) * u0, 120)
        p10 = gp(ax + (cx_ - ax) * u1, az + (cz_ - az) * u1, 120)
        p11 = gp(ax + (cx_ - ax) * u1, az + (cz_ - az) * u1, 205)
        p01 = gp(ax + (cx_ - ax) * u0, az + (cz_ - az) * u0, 205)
        sheet.poly([p00, p10, p11, p01], lerp(tintw(OCHRE, 0.55), COBALT, 0.12))
        cols = 3 if i != 2 else 4
        for c in range(cols):
            v = (c + 0.5) / cols
            q0 = lerp(np.array(p01), np.array(p11), v)
            q1 = lerp(np.array(p00), np.array(p10), v)
            yy = 0.08
            while yy < 0.92:
                ln = rng.uniform(0.03, 0.09)
                a_ = lerp(q0, q1, yy)
                b_ = lerp(q0, q1, min(0.95, yy + ln))
                lines.line([tuple(a_), tuple(b_)], PRUSSIAN, 0.7, 0.75)
                yy += ln + rng.uniform(0.02, 0.05)
        lines.line([p00, p10, p11, p01, p00], PRUSSIAN, 0.6, 0.6)
    # the roof: a little gabled roof of boards over the row
    for (ya, yb, da, db, col) in ((post_h, post_h + 30, -55, -5, SHINGLE_LIT), (post_h, post_h + 30, 55, 5, SHINGLE_SHADE)):
        q = [gp(*inland(ax - 0.514 * 20, az - 0.857 * 20, da), ya), gp(*inland(cx_ + 0.514 * 20, cz_ + 0.857 * 20, da), ya),
             gp(*inland(cx_ + 0.514 * 20, cz_ + 0.857 * 20, db), yb), gp(*inland(ax - 0.514 * 20, az - 0.857 * 20, db), yb)]
        sheet.poly(q, col)
    contour(lines, [gp(*inland(ax - 0.514 * 20, az - 0.857 * 20, -55), post_h), gp(*inland(ax - 0.514 * 20, az - 0.857 * 20, 5), post_h + 30),
                    gp(*inland(cx_ + 0.514 * 20, cz_ + 0.857 * 20, 5), post_h + 30), gp(*inland(cx_ + 0.514 * 20, cz_ + 0.857 * 20, -55), post_h)], gp(bx, bz)[1])
    c, a = sheet.done()
    lc, la = lines.done()
    ys, xs = np.where(a > 0.5)
    return brushed(c, a, lc, la, np.median(back[ys, xs], axis=0) if len(ys) else SAND, seed=seed, fast=fast)


def fence_cut(back, seed, fast=False):
    """The hen yard's low bamboo fence: posts and three horizontal poles, tied; the hens behind it are the engine's."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    Y = YARD
    h = Y["fence"]
    runs = [((Y["x0"], Y["z1"]), (Y["x1"], Y["z1"])), ((Y["x0"], Y["z0"]), (Y["x0"], Y["z1"]))]
    for (a_, b_) in runs:
        n = max(2, int(math.hypot(b_[0] - a_[0], b_[1] - a_[1]) / 110))
        for i in range(n + 1):
            u = i / n
            px_, pz_ = a_[0] + (b_[0] - a_[0]) * u, a_[1] + (b_[1] - a_[1]) * u
            lines.line([gp(px_, pz_), gp(px_, pz_, h + 6)], lerp(OCHRE, PRUSSIAN, 0.4), max(1.2, 6 * kz(pz_)), 1.0)
        for v in (0.3, 0.6, 0.92):
            pts = [gp(a_[0] + (b_[0] - a_[0]) * u, a_[1] + (b_[1] - a_[1]) * u, h * v) for u in np.linspace(0, 1, 6)]
            lines.line(pts, tintw(OCHRE, 0.25), max(1.0, 4 * kz(a_[1])), 1.0)
            lines.line([(p[0], p[1] + 1.2) for p in pts], PRUSSIAN, 0.6, 0.35)
    c, a = sheet.done()
    lc, la = lines.done()
    ys, xs = np.where(la > 0.5)
    return brushed(c, a, lc, la, np.median(back[ys, xs], axis=0) if len(ys) else SAND, seed=seed, fast=fast)


def noren_cut(back, seed, fast=False):
    """Kihei's noren in the shop's open front: indigo cloth in three panels, a white fish on the middle one (our own
    mark), its hem free (it sways: fx noren-sway)."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    z0 = SHOP["z0"]
    x0 = front_x(z0)
    ix, iz = inland(x0, z0, 25)
    jx, jz = inland(x0, z0, 25 + 185)
    top, drop = 183.0, 92.0
    for i in range(3):
        u0, u1 = i / 3 + 0.015, (i + 1) / 3 - 0.015
        q = [gp(ix + (jx - ix) * u0, iz + (jz - iz) * u0, top), gp(ix + (jx - ix) * u1, iz + (jz - iz) * u1, top),
             gp(ix + (jx - ix) * u1, iz + (jz - iz) * u1, top - drop), gp(ix + (jx - ix) * u0, iz + (jz - iz) * u0, top - drop)]
        sheet.poly(q, INDIGO)
        lines.line([q[3], q[0], q[1], q[2]], PRUSSIAN, 0.8, 0.7)
    # the rod it hangs from
    lines.line([gp(ix, iz, top + 2), gp(jx, jz, top + 2)], WOOD_SHADE, max(1.0, 5 * kz(iz)), 1.0)
    # a white fish on the middle panel: a plain shape of our own
    mx_, mz_ = ix + (jx - ix) * 0.5, iz + (jz - iz) * 0.5
    c0 = gp(mx_, mz_, top - drop * 0.5)
    k = kz(mz_)
    sheet.ellipse(c0[0], c0[1], 22 * k, 9 * k, tintw(CERULEAN, 0.85))
    sheet.poly([(c0[0] + 20 * k, c0[1]), (c0[0] + 32 * k, c0[1] - 9 * k), (c0[0] + 32 * k, c0[1] + 9 * k)], tintw(CERULEAN, 0.85))
    sheet.ellipse(c0[0] - 12 * k, c0[1] - 2 * k, 1.6 * k, 1.6 * k, PRUSSIAN)
    c, a = sheet.done()
    lc, la = lines.done()
    ys, xs = np.where(a > 0.5)
    return brushed(c, a, lc, la, np.median(back[ys, xs], axis=0) if len(ys) else INDIGO, seed=seed, keep=0.6, fast=fast)


def ship_cut(back, seed, fast=False):
    """Gonroku's freighter at anchor far out in the bay: one mast, the great square sail furled on its yard, a high
    stern (a benzaisen). Small: it rides at anchor (fx ship-bob)."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    cx_, cy_ = SHIP_AT
    L = 26.0
    hull = lerp(SIENNA, PRUSSIAN, 0.55)
    sheet.poly([(cx_ - L * 0.5, cy_), (cx_ + L * 0.5, cy_), (cx_ + L * 0.56, cy_ - 4.5), (cx_ + L * 0.42, cy_ - 7.5), (cx_ - L * 0.3, cy_ - 5.5), (cx_ - L * 0.52, cy_ - 2.5)], hull)
    sheet.poly([(cx_ + L * 0.36, cy_ - 7.5), (cx_ + L * 0.56, cy_ - 4.5), (cx_ + L * 0.6, cy_ - 11), (cx_ + L * 0.38, cy_ - 12)], lerp(tintw(OCHRE, 0.3), PRUSSIAN, 0.3))   # the high stern's castle
    lines.line([(cx_ - 2, cy_ - 5), (cx_ - 2, cy_ - 38)], hull, 1.3, 1.0)                                                           # the mast
    sheet.poly([(cx_ - 16, cy_ - 33), (cx_ + 12, cy_ - 33), (cx_ + 12, cy_ - 29), (cx_ - 16, cy_ - 29)], tintw(OCHRE, 0.5))        # the sail furled on its yard
    lines.line([(cx_ - 17, cy_ - 34), (cx_ + 13, cy_ - 34)], hull, 0.9, 1.0)
    lines.line([(cx_ - L * 0.52, cy_ - 2.5), (cx_ - L * 0.3, cy_ - 5.5), (cx_ + L * 0.42, cy_ - 7.5), (cx_ + L * 0.6, cy_ - 11)], PRUSSIAN, 0.5, 0.6)
    c, a = sheet.done()
    lc, la = lines.done()
    return brushed(c, a, lc, la, COBALT, seed=seed, sizes=(3, 2), keep=0.6, fast=fast)


def front_cut(back, seed, fast=False):
    """The front plane, bottom left: a coil of rope and a few net floats on the sand, the nearest things in the picture."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    rng = np.random.default_rng(seed)
    cx_, cy_ = 70.0, 598.0
    for i in range(9):
        r = 46 - i * 4.2
        sheet.ellipse(cx_, cy_ - i * 1.6, r, r * 0.42, lerp(tintw(OCHRE, 0.35), PRUSSIAN, 0.1 + 0.03 * i))
        lines.line([(cx_ - r, cy_ - i * 1.6), (cx_, cy_ - i * 1.6 - r * 0.42), (cx_ + r, cy_ - i * 1.6)], PRUSSIAN, 0.8, 0.4)
    for (fx_, fy_, fr) in ((150, 592, 9), (172, 600, 10), (118, 606, 8)):
        sheet.ellipse(fx_, fy_, fr, fr * 0.9, lerp(tintw(OCHRE, 0.4), PRUSSIAN, 0.15))
        lines.line([(fx_ - fr, fy_), (fx_ + fr, fy_)], PRUSSIAN, 0.7, 0.5)
    c, a = sheet.done()
    lc, la = lines.done()
    return brushed(c, a, lc, la, SAND, seed=seed, keep=0.5, fast=fast)


# ================================================================ the numbers
def layout(planes, info):
    import edo_village_layout as L
    return L.layout(planes, info, SHOP, YARD, BOARD, WELL, RACKS, BIGBOAT, TENDER, SHIP_AT)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


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
    planes["ship"] = ship_cut(pic, 11, fast)
    planes["racks"] = racks_cut(pic, 12, fast)
    planes["tender"] = boat_cut(pic, TENDER, 13, fast)
    planes["board"] = board_cut(pic, 14, fast)
    planes["noren"] = noren_cut(pic, 15, fast)
    planes["boat"] = boat_cut(pic, BIGBOAT, 16, fast)
    planes["fence"] = fence_cut(pic, 17, fast)
    planes["front"] = front_cut(pic, 18, fast)
    whole = pic.copy()
    ORDER = ["ship", "racks", "tender", "board", "noren", "boat", "fence", "front"]
    for name in ORDER:
        c, a = planes[name]
        over(whole, c, (a > 0.5).astype(F32))
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-all.png")
    lay_ = layout(planes, info)
    with open(OUT + "/layout.json", "w") as f:
        json.dump(lay_, f, indent=1)
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    print("back", finish(pic, OUT + "/back.png", 152))
    for name, n in (("ship", 32), ("racks", 48), ("tender", 48), ("board", 64), ("noren", 40), ("boat", 64), ("fence", 40), ("front", 40)):
        print(name, finish(planes[name][0], OUT + f"/{name}.png", n, planes[name][1]))
    comp = Image.open(OUT + "/back.png").convert("RGBA")
    for name in ORDER:
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(OUT + "-comp.png")
    print("done", round(time.time() - t0, 1))

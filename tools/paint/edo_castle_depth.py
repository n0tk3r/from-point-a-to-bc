"""Himeji, about 29 April 1830, late afternoon: the castle approach (edo-castle) painted again in three planes and in
the act's watercolour (round twenty-three: tools/paint/DEPTH.md). DEEPEN: the camera, the walked ground and every number
of the scene file stay; what stands beyond the walked ground is staged again through the same camera.

    near     edo_castle_near.py (near.png, plane front): the old cherry's own near limb and boughs of blossom, the moat's
             stone edge and its reeds along the bottom
    middle   here: the white wall with its coping's true eaves and their shadow, the wet grey patch by the scaffold, the
             revetment, the still moat, the banks, the road, the ramp worn up its middle, the terrace; every standing
             thing's shadow thrown through the sun (to the left, a little away), and the long shadow of a pine beyond the
             right edge (edo_castle_model.TREE) across the ramp's foot and the bank, its crown's dappled shade on the moat
             and the bank under the cherry; stones, ruts, tufts and petals through the camera (depth.scatter)
    far      edo_castle_far.py: the sky, the hills, the town, the keep restaged (edo_castle_model.py), the castle hill
    cut-outs edo_castle_cuts.py: the gate, the ladder, the scaffold, the tub, the buckets, the cherry: each painted again
             inside its old outline (the gate's old holes filled: half its roof was see-through)

The light is round twenty's: the sun low in the west, to our right and a little behind us (edo_castle_kit.SUN).

    python3 edo_castle_depth.py          the full run: out/edo-castle/ (every file of the plan, layout.json), out/edo-castle-comp.png
    python3 edo_castle_depth.py fast     no brush pass: out/edo-castle-fast/ and out/edo-castle-fast-comp.png, to compose with
    (python3 edo_castle.py runs this.)
"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
import depth as D
import watercolor as WC
from persp import Camera
from edo_village_kit import (COBALT, CERULEAN, LAKE, NAPLES, OCHRE, PRUSSIAN, SIENNA, ULTRA, VERONESE, VIRIDIAN, WPAPER, SHADE,
                             Wet, keyline, mixp, thin, tintw)
from edo_village_kit import P as PAINT
from edo_castle_kit import EYE, FOC, FULL, H, HZ, SHAPE, W
import edo_castle_model as MD
import edo_castle_far as FAR

SEED = 1830
OUT = "out/edo-castle"
CAM = Camera(HZ, FULL)
LILAC = PAINT("lilac")

# the old picture's places (edo_castle.py, round twenty: the scene file is measured from them)
WALL_TOP, WALL_FOOT = 352, 398
MOAT = dict(x1=432, far=440, near=482)
ROAD_TOP = 540
TERRACE = dict(x0=445, x1=790, top=436, front=470)
RAMP = dict(foot=(432, 582, 540), top=(448, 606, 470))
GATE = dict(x0=575, x1=775, sill=436, open=(629, 729), lintel=310, pent=(282, 300), upper=(592, 758, 226, 282))

# ---------------------------------------------------------------- the paints of the middle ground
PLASTER = lerp(WPAPER, NAPLES, 0.10)
PLASTER_SUN = lerp(WPAPER, mixp(NAPLES, "chrome-orange", 0.2), 0.22)
PLASTER_WET = thin(mixp(COBALT, SIENNA, 0.36), 0.56)                       # new lime, wet: grey (it dries white)
TILE = thin(mixp(PRUSSIAN, COBALT, 0.28), 0.40)
TILE_DEEP = thin(PRUSSIAN, 0.18)
STONE = thin(mixp(OCHRE, SIENNA, 0.20), 0.48)
STONE_PALE = thin(mixp(OCHRE, NAPLES, 0.35), 0.62)
STONE_COOL = thin(mixp(COBALT, SIENNA, 0.30), 0.48)
JOINT = thin(mixp(SIENNA, PRUSSIAN, 0.50), 0.32)
WATER_FAR = thin(mixp(VIRIDIAN, CERULEAN, 0.45), 0.44)
WATER_DEEP = thin(mixp(VIRIDIAN, COBALT, 0.45), 0.12)
GRASS = thin(mixp(VERONESE, OCHRE, 0.30), 0.34)
GRASS_NEAR = thin(mixp(VERONESE, VIRIDIAN, 0.40), 0.22)
GRASS_SHADE = thin(mixp(VIRIDIAN, COBALT, 0.35), 0.40)
PATH = thin(mixp(OCHRE, NAPLES, 0.40), 0.56)
EARTH_FAR = thin(mixp(OCHRE, SIENNA, 0.12), 0.54)
EARTH = thin(mixp(OCHRE, SIENNA, 0.24), 0.38)
EARTH_NEAR = lerp(mixp(SIENNA, OCHRE, 0.50), PRUSSIAN, 0.16)
WOOD = thin(mixp(SIENNA, PRUSSIAN, 0.35), 0.18)
PETAL = thin(LAKE, 0.62)
PETAL_LIT = thin(LAKE, 0.80)
GLAZE = SHADE                                                              # a cast shadow: a thin cool wash, multiplied


# ---------------------------------------------------------------- the ground through the camera
def floor_xz():
    """For every pixel below the horizon: its place on the ground (X across, Z from the lens, cm)."""
    x, y = grid(SHAPE)
    Z = EYE * FOC / np.maximum(y - HZ, 0.5)
    X = (x - 400.0) * Z / FOC
    return X.astype(F32), Z.astype(F32)


def gpt(X, Z):
    return MD.proj(X, 0.0, Z)


def kz(Z):
    return FOC / Z


_TILE = {}


def ground_noise(X, Z, cell, seed, octaves=3):
    """Noise lying on the ground, its blotches `cell` cm across (or (across, along)), fading to 0.5 where a blotch would be
    smaller than a pixel."""
    tile = _TILE.get((seed, octaves))
    if tile is None:
        tile = _TILE[(seed, octaves)] = noise((1024, 1024), 64, seed, octaves)
    cu, cv = (cell, cell) if np.isscalar(cell) else cell

    def fold(t):
        m = np.mod(t, 2 * 1022)
        return np.where(m > 1022, 2 * 1022 - m, m)
    n = sample(tile, fold(X / cu * 64 + 300), fold(Z / cv * 64 + 300))
    k = FOC / np.maximum(Z, 1.0)
    small = np.minimum(cu * k, cv * k * k * EYE / FOC)
    return (0.5 + (n - 0.5) * np.clip((small - 1.0) / 2.5, 0, 1)).astype(F32)


def near_bank_row(px):
    return MOAT["near"] + 3 * math.sin(px / 70.0) - 2 * math.sin(px / 23.0 + 1)


def regions():
    """The picture's parts as masks (the old picture's places)."""
    x, y = grid(SHAPE)
    f0, f1, fy = RAMP["foot"]
    t0, t1, ty = RAMP["top"]
    nb = MOAT["near"] + 3 * np.sin(x / 70.0) - 2 * np.sin(x / 23.0 + 1)
    r = {}
    r["water"] = ((y > MOAT["far"] + 0.5) & (y < nb) & (x < MOAT["x1"] + 8 + (y - MOAT["far"]) * 0.3)).astype(F32)
    r["road"] = mask_poly(SHAPE, [(-10, ROAD_TOP), (810, ROAD_TOP + 1), (810, 610), (-10, 610)])
    r["bank"] = np.clip(mask_poly(SHAPE, [(-10, 470), (TERRACE["x0"] + 6, 470), (TERRACE["x0"] + 6, MOAT["near"] + 2), (t0, ty), (f0, ROAD_TOP), (-10, ROAD_TOP + 2)]) * (y > nb - 0.5) - r["road"], 0, 1)
    r["ramp"] = mask_poly(SHAPE, [(f0, fy), (f1, fy), (t1, ty), (t0, ty)])
    r["rbank"] = np.clip(mask_poly(SHAPE, [(t1, ty), (TERRACE["x1"] + 20, TERRACE["front"]), (810, TERRACE["front"] + 6), (810, ROAD_TOP + 2), (f1, ROAD_TOP)]) - r["ramp"], 0, 1)
    r["terrace"] = np.clip(mask_poly(SHAPE, [(TERRACE["x0"], TERRACE["top"]), (810, TERRACE["top"]), (810, TERRACE["front"] + 6), (TERRACE["x1"] + 20, TERRACE["front"]),
                                             (t1, ty), (t0, ty), (TERRACE["x0"], TERRACE["front"] - 2)]) - r["ramp"], 0, 1)
    r["wall"] = mask_poly(SHAPE, [(-10, WALL_TOP - 6), (200, WALL_TOP - 3), (420, WALL_TOP), (GATE["x0"] + 2, WALL_TOP), (GATE["x0"] + 2, WALL_FOOT), (-10, WALL_FOOT + 4)])
    r["footing"] = mask_poly(SHAPE, [(TERRACE["x0"] - 2, WALL_FOOT), (GATE["x0"] + 2, WALL_FOOT), (GATE["x0"] + 2, TERRACE["top"] + 1), (TERRACE["x0"] - 2, TERRACE["top"] + 1)])
    r["revet"] = mask_poly(SHAPE, [(-10, WALL_FOOT + 4), (MOAT["x1"], WALL_FOOT + 2), (MOAT["x1"] + 12, MOAT["far"] + 2), (-10, MOAT["far"] + 4)])
    r["corner"] = mask_poly(SHAPE, [(MOAT["x1"] - 4, WALL_FOOT + 2), (TERRACE["x0"] + 2, WALL_FOOT + 2), (TERRACE["x0"] + 6, MOAT["near"] + 2), (MOAT["x1"] + 2, MOAT["near"] + 2)])
    r["walkground"] = np.clip(r["road"] + r["bank"] + r["ramp"] + r["terrace"], 0, 1)
    r["ground"] = np.clip(r["walkground"] + r["rbank"], 0, 1)
    return r


# ================================================================ the wall, its coping, the revetment
def paint_wall(pic, R, seed):
    """The white wall from the gate to the left edge: plaster in the low sun (warmer toward the right), its tiled coping
    seen from a little above with the coping's eave throwing a band of shade on the plaster, loopholes (round, square,
    triangular) with depth, the new coat by the scaffold still wet and grey, old weather stains elsewhere; under it the
    stone footing (the revetment into the moat, and above the terrace by the gate)."""
    rng = np.random.default_rng(seed)
    x, y = grid(SHAPE)
    L = Wet(SHAPE)
    top = lambda px: np.interp(px, [-10, 200, 420, 580], [WALL_TOP - 6, WALL_TOP - 3, WALL_TOP, WALL_TOP])
    wall_pts = [(-10, top(-10)), (200, top(200)), (420, top(420)), (GATE["x0"] + 2, WALL_TOP), (GATE["x0"] + 2, WALL_FOOT), (-10, WALL_FOOT + 4)]
    L.poly(wall_pts, PLASTER, PLASTER_SUN, g=((0, 370), (580, 370)))
    # weather: thin grey runs from the coping, darker toward the far left
    for i in range(34):
        px_ = rng.uniform(-5, 440)
        L.poly([(px_, top(px_) + 2), (px_ + rng.uniform(4, 16), top(px_) + 2), (px_ + rng.uniform(2, 10), top(px_) + rng.uniform(10, 34)), (px_ + rng.uniform(-2, 3), top(px_) + rng.uniform(8, 28))],
               thin(mixp(COBALT, SIENNA, 0.4), 0.80), alpha=rng.uniform(0.25, 0.5))
    # the new coat by the scaffold: wet lime, grey, its edge ragged where the trowels stopped; trowel arcs in it
    edge = [(455 + 6 * math.sin(k * 1.7), WALL_TOP + 2 + k * 6) for k in range(8)]
    wet = [(GATE["x0"] + 2, WALL_TOP + 2)] + [(458 + rng.uniform(-3, 3), WALL_TOP + 2)] + [(p[0] + rng.uniform(-4, 4), p[1]) for p in edge] + [(470, WALL_FOOT), (GATE["x0"] + 2, WALL_FOOT)]
    L.poly(wet, PLASTER_WET, lerp(PLASTER_WET, PLASTER, 0.30), g=((470, 360), (575, 395)))
    for i in range(40):                                                         # the trowel's arcs
        cx_, cy_ = rng.uniform(470, 572), rng.uniform(WALL_TOP + 6, WALL_FOOT - 4)
        a0 = rng.uniform(0, math.pi)
        arc = [(cx_ + 7 * math.cos(a0 + t), cy_ + 2.5 * math.sin(a0 + t)) for t in np.linspace(0, 1.6, 6)]
        L.line(arc, lerp(PLASTER_WET, PLASTER, rng.uniform(0.1, 0.5)), 0.6, 0.6)
    for i in range(10):                                                         # patches of the old, dry coat left between
        cx_, cy_ = rng.uniform(462, 520), rng.uniform(WALL_TOP + 8, WALL_FOOT - 8)
        L.ellipse(cx_, cy_, rng.uniform(4, 10), rng.uniform(2, 4), PLASTER, alpha=0.8)
    # the coping: a little tiled roof along the top, its slope toward us seen from a little above, its ridge, its eave
    for (a, b) in ((-10, 200), (200, 420), (420, GATE["x0"] + 6)):
        pass
    cop_top = [(px_, top(px_) - 8) for px_ in np.linspace(-10, GATE["x0"] + 6, 30)]
    cop_eave = [(px_, top(px_) + 1.5) for px_ in np.linspace(GATE["x0"] + 6, -10, 30)]
    L.poly(cop_top + cop_eave, TILE, lerp(TILE, NAPLES, 0.12), g=((0, 345), (580, 345)))
    for px_ in np.arange(-8, GATE["x0"] + 6, 3.2):                               # the rows of round tiles down the slope
        L.line([(px_, top(px_) - 7), (px_ + 0.6, top(px_) + 1)], TILE_DEEP, 0.5, 0.35 * rng.uniform(0.5, 1))
    L.line(cop_top, lerp(WPAPER, NAPLES, 0.12), 1.0, 0.85)                       # the ridge, plastered, in the sun
    L.line([(p[0], p[1] - 0.8) for p in cop_top], TILE_DEEP, 0.6, 0.6)
    L.line([(px_, top(px_) + 1.6) for px_ in np.linspace(-10, GATE["x0"] + 6, 30)], TILE_DEEP, 1.3)     # the eave's tile ends
    # the coping's shadow on the plaster: a band under the eave, a little deeper toward the left (the sun is on the right)
    band = [(px_, top(px_) + 2.4) for px_ in np.linspace(-10, GATE["x0"] + 2, 30)] + [(px_, top(px_) + 8.5 + 1.5 * (1 - px_ / 580)) for px_ in np.linspace(GATE["x0"] + 2, -10, 30)]
    L.glaze(band, lerp(np.ones(3, F32), mixp(COBALT, LILAC, 0.5), 0.42))
    # loopholes at a man's shoulder on the wall-walk inside: round, square, triangular; dark, their sunward rim lit
    for j, px_ in enumerate(range(26, 450, 44)):
        yy = top(px_) + 19
        kind = j % 3
        if 455 < px_:
            continue
        if kind == 0:
            L.ellipse(px_, yy, 2.8, 2.8, lerp(TILE_DEEP, SIENNA, 0.2))
            L.ellipse(px_ + 0.8, yy + 0.6, 1.6, 1.6, thin(PRUSSIAN, 0.05))
        elif kind == 1:
            L.poly([(px_ - 2.6, yy - 2.6), (px_ + 2.6, yy - 2.6), (px_ + 2.6, yy + 2.6), (px_ - 2.6, yy + 2.6)], lerp(TILE_DEEP, SIENNA, 0.2))
            L.poly([(px_ - 1.2, yy - 1.4), (px_ + 2.0, yy - 1.4), (px_ + 2.0, yy + 2.0), (px_ - 1.2, yy + 2.0)], thin(PRUSSIAN, 0.05))
        else:
            L.poly([(px_ - 3.2, yy + 2.6), (px_ + 3.2, yy + 2.6), (px_, yy - 3.0)], lerp(TILE_DEEP, SIENNA, 0.2))
            L.poly([(px_ - 1.4, yy + 2.2), (px_ + 2.4, yy + 2.2), (px_ + 0.6, yy - 1.4)], thin(PRUSSIAN, 0.05))
        L.line([(px_ + 3.4, yy - 2.8), (px_ + 3.4, yy + 3.0)], PLASTER_SUN, 0.6, 0.6)
    # the wall's foot: a dark line where plaster meets stone
    L.line([(-10, WALL_FOOT + 4), (TERRACE["x0"], WALL_FOOT + 2), (GATE["x0"] + 2, WALL_FOOT)], thin(mixp(SIENNA, PRUSSIAN, 0.5), 0.35), 1.0, 0.7)
    c, a = L.done()
    over(pic, c, a)
    # the stone footing: the revetment down into the moat, and above the terrace by the gate: rough courses
    stone = Wet(SHAPE)
    rv = [(-10, WALL_FOOT + 4), (MOAT["x1"], WALL_FOOT + 2), (MOAT["x1"] + 12, MOAT["far"] + 2), (-10, MOAT["far"] + 4)]
    stone.poly(rv, STONE, lerp(STONE, STONE_COOL, 0.35), g=((0, WALL_FOOT), (0, MOAT["far"])))
    ft = [(TERRACE["x0"] - 2, WALL_FOOT), (GATE["x0"] + 2, WALL_FOOT), (GATE["x0"] + 2, TERRACE["top"] + 1), (TERRACE["x0"] - 2, TERRACE["top"] + 1)]
    stone.poly(ft, STONE, lerp(STONE, STONE_PALE, 0.25), g=((450, WALL_FOOT), (575, WALL_FOOT)))
    # fitted stones, every one a different shape and no gap between them: a loose net of joints, the stones larger
    # toward the water, each a little lighter or darker, its top edge catching the light
    for (xa, xb, ya, yb_) in ((-10, MOAT["x1"] + 6, WALL_FOOT + 3, MOAT["far"] + 3), (TERRACE["x0"] - 2, GATE["x0"] + 2, WALL_FOOT, TERRACE["top"])):
        pts_ = []
        yy = ya
        rowy = []
        while yy < yb_:
            rowy.append(yy)
            yy += rng.uniform(5.0, 9.5) * (1 + 0.25 * (yy - ya) / max(yb_ - ya, 1))
        rowy.append(yb_)
        prev = None
        for i in range(len(rowy) - 1):
            y0_, y1_ = rowy[i], rowy[i + 1]
            px_ = xa + rng.uniform(-10, 0)
            cuts = []
            while px_ < xb:
                cuts.append(px_)
                px_ += rng.uniform(8, 20)
            cuts.append(xb + 4)
            for j in range(len(cuts) - 1):
                xa_, xb_ = cuts[j], cuts[j + 1]
                sk0, sk1 = rng.uniform(-2.5, 2.5), rng.uniform(-2.5, 2.5)
                tl = (xa_ + sk0, y0_ + rng.uniform(-1.0, 1.0))
                tr = (xb_ + sk1, y0_ + rng.uniform(-1.0, 1.0))
                br = (xb_ - sk1 * 0.5, y1_)
                bl = (xa_ - sk0 * 0.5, y1_)
                c_ = np.clip(lerp(STONE, STONE_PALE, rng.uniform(0, 0.55)) * rng.uniform(0.90, 1.07), 0, 1)
                if rng.random() < 0.18:
                    c_ = lerp(c_, STONE_COOL, 0.45)
                stone.poly([tl, tr, br, bl], c_, alpha=0.7)
                stone.line([tr, br], JOINT, 0.6, 0.65)
                stone.line([tl, tr], lerp(STONE_PALE, WPAPER, 0.3), 0.5, 0.45)
            stone.line([(xa, y1_), (xb, y1_ + rng.uniform(-0.8, 0.8))], JOINT, 0.55, 0.45)
    # wet and dark at the water line; green where the water licks it
    stone.glaze([(-10, MOAT["far"] - 7), (MOAT["x1"] + 10, MOAT["far"] - 9), (MOAT["x1"] + 12, MOAT["far"] + 3), (-10, MOAT["far"] + 4)], lerp(np.ones(3, F32), mixp(VIRIDIAN, PRUSSIAN, 0.4), 0.45))
    # the terrace's stone side going down into the water, in the shade of its own corner
    stone.poly([(MOAT["x1"] - 4, WALL_FOOT + 2), (TERRACE["x0"] + 2, WALL_FOOT + 2), (TERRACE["x0"] + 6, MOAT["near"] + 2), (MOAT["x1"] + 2, MOAT["near"] + 2)], STONE_COOL, lerp(STONE_COOL, STONE, 0.4))
    cs, as_ = stone.done()
    over(pic, cs, as_)
    return np.clip(a + as_, 0, 1)


# ================================================================ the moat
def paint_water(pic, R, seed):
    """The inner moat, still and green. In it, upside down: right under the far side the wet stones at the water line,
    then the revetment's stones, then the white wall and its dark coping, broken into level bands by the slightest
    ripple; toward us the green of the water itself and the bank's own grass. The herons stand in it (their frames)."""
    rng = np.random.default_rng(seed)
    x, y = grid(SHAPE)
    m = R["water"]
    wob = (noise(SHAPE, (70, 2.5), seed + 1, 3) - 0.5) * 7.0 + (noise(SHAPE, (24, 1.5), seed + 3, 2) - 0.5) * 3.0
    tq = np.clip((y + wob - MOAT["far"]) / (MOAT["near"] - MOAT["far"]), 0, 1)
    refl_stone = lerp(lerp(STONE, STONE_COOL, 0.3), WATER_DEEP, 0.50)
    refl_wall = lerp(lerp(PLASTER, CERULEAN, 0.12), WATER_FAR, 0.45)
    body = ramp(tq, [(0.0, lerp(WATER_DEEP, thin(PRUSSIAN, 0.2), 0.3)), (0.10, lerp(refl_stone, WATER_DEEP, 0.3)), (0.38, refl_stone),
                     (0.46, refl_wall), (0.70, refl_wall), (0.76, lerp(TILE, WATER_DEEP, 0.55)), (0.84, lerp(WATER_FAR, GRASS, 0.25)),
                     (1.0, lerp(WATER_DEEP, GRASS_SHADE, 0.3))])
    body *= (1 + (noise(SHAPE, (110, 5), seed + 2, 3) - 0.5)[..., None] * 0.10)
    over(pic, body, m)
    L = Wet(SHAPE)
    for k in range(120):                                                         # level ripple lines: a light and a dark side
        yy = rng.uniform(MOAT["far"] + 3, MOAT["near"] - 2)
        x0 = rng.uniform(-10, MOAT["x1"])
        ln = rng.uniform(8, 34) * (0.6 + 0.8 * (yy - MOAT["far"]) / 42)
        L.line([(x0, yy), (x0 + ln, yy + rng.uniform(-0.3, 0.3))], lerp(WPAPER, CERULEAN, 0.25), 0.6, 0.45)
        L.line([(x0 + 2, yy + 1.1), (x0 + ln - 2, yy + 1.1)], lerp(WATER_DEEP, thin(PRUSSIAN, 0.2), 0.4), 0.5, 0.35)
    c, a = L.done()
    over(pic, c, a * m)
    return m


# ================================================================ the ground: banks, road, ramp, terrace
def paint_ground(pic, R, seed):
    rng = np.random.default_rng(seed)
    x, y = grid(SHAPE)
    X, Z = floor_xz()
    t = np.clip((y - 430) / 170.0, 0, 1)
    # ---- the near bank: spring grass, deeper toward us, a trodden path along the water and down by the road
    g = ramp(t, [(0.0, lerp(GRASS, FAR.AIR, 0.25)), (0.5, GRASS), (1.0, GRASS_NEAR)])
    g *= (1 + ((ground_noise(X, Z, 160, seed + 1) - 0.5) * 0.16 + (ground_noise(X, Z, 40, seed + 2) - 0.5) * 0.10)[..., None])
    over(pic, np.clip(g, 0, 1), R["bank"])
    nb = MOAT["near"] + 3 * np.sin(x / 70.0) - 2 * np.sin(x / 23.0 + 1)
    path = (np.clip(1 - np.abs(y - (nb + 7)) / 5.0, 0, 1) * 0.55 + np.clip(1 - np.abs(y - (ROAD_TOP - 13 + 3 * np.sin(x / 50.0))) / 8.0, 0, 1) * 0.75) * R["bank"]
    path *= (0.75 + 0.5 * ground_noise(X, Z, 70, seed + 3))
    over(pic, PATH, np.clip(path, 0, 1).astype(F32))
    tint(pic, thin(mixp(VIRIDIAN, PRUSSIAN, 0.5), 0.45), (np.clip(1 - np.abs(y - (nb + 1.5)) / 2.2, 0, 1) * R["bank"] * 0.55).astype(F32))   # the water's edge
    # ---- the bank right of the ramp, falling to the road (nobody walks there): grass, a little rougher
    g2 = ramp(t, [(0.0, GRASS), (0.6, lerp(GRASS, GRASS_NEAR, 0.6)), (1.0, lerp(GRASS_NEAR, GRASS_SHADE, 0.35))])
    g2 *= (1 + ((ground_noise(X, Z, 120, seed + 4) - 0.5) * 0.24 + (ground_noise(X, Z, 30, seed + 41) - 0.5) * 0.12)[..., None])
    over(pic, np.clip(g2, 0, 1), R["rbank"])
    tint(pic, thin(mixp(VIRIDIAN, PRUSSIAN, 0.4), 0.5), (np.clip(1 - np.abs(y - (ROAD_TOP - 3)) / 4.0, 0, 1) * R["rbank"] * 0.5).astype(F32))   # its foot over the road
    # ---- the road: packed earth, paler far, deeper and warmer toward us; two worn tracks and a crown between, ruts
    e = ramp(np.clip((y - ROAD_TOP) / 60.0, 0, 1) ** 0.9, [(0.0, EARTH_FAR), (0.45, EARTH), (1.0, EARTH_NEAR)])
    e *= (1 + ((ground_noise(X, Z, (90, 40), seed + 5) - 0.5) * 0.16 + (ground_noise(X, Z, 24, seed + 6) - 0.5) * 0.10)[..., None])
    for zc in (980.0, 900.0):                                                    # the worn tracks: pale, along the road
        tr = np.exp(-((Z - zc - (ground_noise(X, Z, (900, 60), seed + 7) - 0.5) * 30) / 26.0) ** 2)
        e = lerp(e, thin(mixp(OCHRE, NAPLES, 0.45), 0.66), (tr * 0.45 * R["road"])[..., None])
    for zc in (1015.0, 948.0, 870.0):                                            # ruts: a darker line, its far lip lit
        rut = np.exp(-((Z - zc - (ground_noise(X, Z, (700, 50), seed + 8) - 0.5) * 18) / 5.0) ** 2)
        e *= (1 - (rut * 0.16)[..., None])
    over(pic, np.clip(e, 0, 1), R["road"])
    # ---- the ramp: stone paving in courses, closer as it climbs; worn smooth and pale up its middle by feet; a low
    # parapet each side with a tiled cap
    f0, f1, fy = RAMP["foot"]
    t0, t1, ty = RAMP["top"]
    u = np.clip((x - (f0 + (t0 - f0) * (fy - y) / (fy - ty))) / np.maximum((f1 + (t1 - f1) * (fy - y) / (fy - ty)) - (f0 + (t0 - f0) * (fy - y) / (fy - ty)), 1), 0, 1)
    ramp_c = ramp(np.clip((y - ty) / (fy - ty), 0, 1), [(0.0, lerp(STONE_PALE, FAR.AIR, 0.15)), (1.0, STONE)])
    worn = np.exp(-((u - 0.52) / 0.20) ** 2)
    ramp_c = lerp(ramp_c, lerp(STONE_PALE, WPAPER, 0.25), (worn * 0.55)[..., None])
    ramp_c *= (1 + ((ground_noise(X, Z, 60, seed + 9) - 0.5) * 0.14)[..., None])
    over(pic, np.clip(ramp_c, 0, 1), R["ramp"])
    # ---- the terrace: paved, pale; the lime spattered by the scaffold
    tc = ramp(np.clip((y - 436) / 40.0, 0, 1), [(0.0, lerp(STONE_PALE, FAR.AIR, 0.18)), (1.0, lerp(STONE_PALE, STONE, 0.45))])
    tc *= (1 + ((ground_noise(X, Z, 80, seed + 10) - 0.5) * 0.12)[..., None])
    over(pic, np.clip(tc, 0, 1), R["terrace"])
    return pic


def paving(L, rng):
    """The joints of the ramp's and the terrace's paving, through the camera: courses across, staggered joints along."""
    f0, f1, fy = RAMP["foot"]
    t0, t1, ty = RAMP["top"]
    Zf, Zt = EYE * FOC / (fy - HZ), EYE * FOC / (ty - HZ)
    Z_ = Zf
    k = 0
    while Z_ < Zt - 20:
        Z1 = Z_ + rng.uniform(52, 70)
        y_ = HZ + EYE * FOC / Z_
        y1 = HZ + EYE * FOC / min(Z1, Zt)
        xa = f0 + (t0 - f0) * (fy - y_) / (fy - ty)
        xb = f1 + (t1 - f1) * (fy - y_) / (fy - ty)
        L.line([(xa + 1, y_), (xb - 1, y_ + rng.uniform(-0.4, 0.4))], JOINT, 0.5 + 0.5 * (y_ - ty) / (fy - ty), 0.45)
        n = int(rng.integers(3, 5))
        for j in range(n):
            tt = (j + 0.5 + 0.5 * (k % 2) * rng.uniform(0.6, 1.0)) / (n + 0.5)
            xa1 = f0 + (t0 - f0) * (fy - y1) / (fy - ty)
            xb1 = f1 + (t1 - f1) * (fy - y1) / (fy - ty)
            L.line([(xa + (xb - xa) * tt, y_), (xa1 + (xb1 - xa1) * tt, y1)], JOINT, 0.45, 0.35)
        Z_ = Z1
        k += 1
    # the terrace: three courses across, joints along
    for j, yy in enumerate((442.0, 451.0, 461.0)):
        L.line([(TERRACE["x0"] + 2, yy), (810, yy + 0.6)], JOINT, 0.5, 0.35)
    for i in range(60):
        px_ = rng.uniform(TERRACE["x0"], 800)
        yy = (436.0, 442.0, 451.0, 461.0)[int(rng.integers(0, 3))]
        yn = {436.0: 442.0, 442.0: 451.0, 451.0: 461.0}[yy]
        if t1 - 4 < px_ < t1 + 4:
            continue
        L.line([(px_, yy + 0.4), (px_ + (px_ - 400) * (yn - yy) / (yy - HZ), yn)], JOINT, 0.45, 0.32)


def parapets(L, rng):
    """The ramp's two low parapets: stone, with a tiled cap; the left in the ramp's own light, the right lit on its
    outer face (toward the sun)."""
    f0, f1, fy = RAMP["foot"]
    t0, t1, ty = RAMP["top"]
    for side in (0, 1):
        if side == 0:
            fx, tx = f0, t0
            poly = [(fx - 9, fy + 2), (fx + 1, fy), (tx + 1, ty), (tx - 6, ty + 1), (tx - 6, ty - 9), (fx - 9, fy - 15)]
            L.poly(poly, STONE, lerp(STONE, STONE_COOL, 0.3), g=((fx, fy), (tx, ty)))
            L.poly([(fx + 1, fy), (tx + 1, ty), (tx + 1, ty - 8), (fx + 1, fy - 13)], lerp(STONE_PALE, STONE, 0.3))          # its inner face, lit
            cap = [(fx - 9, fy - 15), (tx - 6, ty - 9)]
        else:
            fx, tx = f1, t1
            poly = [(fx - 1, fy), (fx + 9, fy + 2), (fx + 9, fy - 15), (tx + 6, ty - 9), (tx + 6, ty + 1), (tx - 1, ty)]
            L.poly(poly, STONE_PALE, STONE, g=((fx, fy), (tx, ty)))
            L.poly([(fx - 1, fy), (tx - 1, ty), (tx - 1, ty - 8), (fx - 1, fy - 13)], lerp(STONE_COOL, STONE, 0.3))          # its inner face, in its own shade
            cap = [(fx + 9, fy - 15), (tx + 6, ty - 9)]
        # stones in it
        for j in range(9):
            tt = (j + 0.5) / 9
            px_ = fx + (tx - fx) * tt + (-4 if side == 0 else 4)
            py_ = fy + (ty - fy) * tt
            L.line([(px_, py_ - 1), (px_ + (-0.6 if side == 0 else 0.6), py_ - 12 + 4 * tt)], JOINT, 0.5, 0.45)
        L.line(cap, TILE, 3.0)
        L.line([(cap[0][0], cap[0][1] - 1.3), (cap[1][0], cap[1][1] - 1.3)], lerp(TILE, WPAPER, 0.55), 1.0, 0.9)
        keyline(L, [(p[0], p[1] + 1.4) for p in cap], row=fy, seed=40 + side)


def passage(L):
    """Through the gate's opening: the passage in shade, the door leaves standing open against its walls, and at its far
    end the lit court: a white wall in the sun, its ground."""
    o0, o1 = GATE["open"]
    sill, lintel = GATE["sill"], GATE["lintel"]
    L.poly([(o0, sill), (o1, sill), (o1, lintel), (o0, lintel)], thin(mixp(PRUSSIAN, LILAC, 0.45), 0.30), thin(mixp(PRUSSIAN, SIENNA, 0.3), 0.30), g=((o0, lintel), (o0, sill)))
    L.poly([(o0 + 26, sill - 2), (o1 - 26, sill - 2), (o1 - 30, sill - 40), (o0 + 30, sill - 40)], thin(mixp(OCHRE, NAPLES, 0.4), 0.55), STONE_PALE)
    L.poly([(o0 + 26, sill - 40), (o1 - 26, sill - 40), (o1 - 26, lintel + 40), (o0 + 26, lintel + 40)], lerp(PLASTER_SUN, NAPLES, 0.15), PLASTER_SUN)
    L.poly([(o0 + 26, lintel + 40), (o1 - 26, lintel + 40), (o1 - 26, lintel + 31), (o0 + 26, lintel + 31)], TILE)
    L.poly([(o0 + 26, lintel + 31), (o1 - 26, lintel + 31), (o1 - 26, lintel), (o0 + 26, lintel)], thin(mixp(PRUSSIAN, LILAC, 0.5), 0.36))
    L.glaze([(o0 + 26, sill - 40), (o0 + 52, sill - 40), (o0 + 40, lintel + 40), (o0 + 26, lintel + 40)], lerp(np.ones(3, F32), mixp(COBALT, LILAC, 0.5), 0.4))
    for side, (xa, xb) in enumerate(((o0, o0 + 24), (o1 - 24, o1))):
        L.poly([(xa, sill), (xb, sill - 1), (xb, lintel + 2), (xa, lintel + 1)], WOOD, lerp(WOOD, thin(SIENNA, 0.3), 0.3), g=((xa, lintel), (xa, sill)))
        for k in range(5):
            yy = lintel + 12 + k * 26
            L.line([(xa, yy), (xb, yy)], thin(PRUSSIAN, 0.1), 1.2, 0.7)
        for k in range(3):
            L.ellipse(xa + 6 + k * 6, sill - 20, 1.2, 1.2, thin(PRUSSIAN, 0.1))
    L.poly([(o0 - 2, sill - 2), (o1 + 2, sill - 2), (o1 + 2, sill + 3), (o0 - 2, sill + 3)], STONE_COOL)


# ================================================================ shadows, all one way
def shadow_mask_tree(R, seed):
    """The pine beyond the right edge (edo_castle_model.TREE): its trunk's long shadow and its crown's dapple, on the
    ground and the water, through the sun."""
    X, Z = floor_xz()
    sx, sz = -MD.S3[0] / MD.S3[1], -MD.S3[2] / MD.S3[1]                       # the shadow's step on the ground per cm of height
    L_ = math.hypot(sx, sz)
    ux, uz = sx / L_, sz / L_
    sinE = MD.S3[1]
    m = np.zeros(SHAPE, F32)
    sl = slice(430, H)
    Xs, Zs = X[sl], Z[sl]
    U, V = Xs * ux + Zs * uz, -Xs * uz + Zs * ux
    for (bx, by, bz, r) in MD.tree_blobs():
        gx, gz = MD.ground_shadow_of(bx, by, bz)
        cu, cv = gx * ux + gz * uz, -gx * uz + gz * ux
        wob = (ground_noise(Xs, Zs, (40, 30), seed + int(bx) % 97, 2) - 0.5) * 0.5          # the clump's ragged edge of needles
        e_ = ((U - cu) / (r / sinE * 0.8)) ** 2 + ((V - cv) / (r * 0.95)) ** 2 + wob
        np.maximum(m[sl], np.clip((1 - e_) * 6.0, 0, 1), out=m[sl])
    fleck = step(0.58, 0.64, ground_noise(X, Z, (48, 34), seed + 3, 2))                      # the sun through the needles
    m = m * (1 - fleck * 0.9)
    # the trunk: a band from its foot along the light, a little crooked
    T = MD.TREE
    pts, wds = [], []
    for hgt in np.linspace(0, T["crown"][0] + 60, 14):
        gx, gz = MD.ground_shadow_of(T["X"] + 8 * math.sin(hgt / 70.0), hgt, T["Z"])
        pts.append(gpt(gx, gz))
        wds.append(max(1.0, T["trunk"] * (1 - 0.25 * hgt / 400) * kz(gz)))
    trunk = mask_line(SHAPE, pts, wds, soft=0.7)
    trunk = trunk * (0.85 + 0.15 * ground_noise(X, Z, (30, 30), seed + 5, 2))
    return np.clip(np.maximum(m * 0.88, trunk), 0, 1).astype(F32)


def shadow_mask_things(seed):
    """Every standing thing of the middle ground: its shadow to the left (and a little away) on the ground."""
    sh = np.zeros(SHAPE, F32)

    def add(pts, amount=0.9, soft=0.8, wobble=0.6, s=0):
        np.maximum(sh, mask_poly(SHAPE, pts, soft=soft, wobble=wobble, seed=seed + s) * amount, out=sh)
    f0, f1, fy = RAMP["foot"]
    t0, t1, ty = RAMP["top"]
    # the right parapet's shadow across the ramp (it is low: a band along its inner foot)
    add([(f1 - 1, fy), (f1 - 34, fy - 1), (t1 - 22, ty + 0.5), (t1 - 1, ty)], 0.55, soft=1.6, s=1)
    # the left parapet's, out over the bank
    add([(f0 - 9, fy + 2), (f0 - 58, fy + 4), (t0 - 40, ty + 2), (t0 - 6, ty)], 0.8, s=2)
    # the tub and the three buckets (their places: the old picture's), and the scaffold's poles across the terrace
    add([(499, 466), (541, 466), (537, 462), (479, 461), (476, 465)], 0.85, s=3)
    for (bx, by) in ((500, 494), (527, 503), (553, 490)):
        add([(bx - 9, by + 0.5), (bx + 8, by + 0.5), (bx - 4, by - 2.5), (bx - 40, by - 3.5), (bx - 44, by - 1)], 0.8, s=4 + bx)
    for px_ in (462, 510, 558):
        sh_ = mask_line(SHAPE, [(px_, 450), (px_ - 70, 445), (px_ - 150, 438.5)], [2.4, 2.0, 1.5], soft=0.6)
        np.maximum(sh, sh_ * 0.75, out=sh)
    # the ladder's foot on the terrace
    add([(593, 466), (614, 466), (600, 462), (572, 461)], 0.7, s=7)
    # the cherry's trunk: its long shadow off to the left
    add([(104, 547), (74, 550), (20, 553), (-10, 548), (-10, 538), (30, 541), (70, 541)], 0.85, s=8)
    return sh


def wall_shadows(seed):
    """Shadows on the wall's face: the scaffold's frame (it stands a hand's breadth out from the plaster: its shadow lies
    a little left of it and below), its planks' long slanting shadows."""
    sh = np.zeros(SHAPE, F32)
    dx, dy = -18.0, 6.0
    for px_ in (467, 515, 563):
        np.maximum(sh, mask_line(SHAPE, [(px_ + dx, 437 + dy), (px_ - 1 + dx, 356 + dy)], 2.4, soft=0.6) * 0.75, out=sh)
    for yy in (444, 404, 372, 358):
        np.maximum(sh, mask_line(SHAPE, [(462 + dx, yy + dy), (570 + dx, yy - 1 + dy)], 2.0, soft=0.6) * 0.7, out=sh)
    for yy in (412, 380):                                                       # the planks: their shadow slants down to the left
        np.maximum(sh, mask_poly(SHAPE, [(456 + dx, yy - 6 + dy), (568 + dx, yy - 7 + dy), (568 + dx - 30, yy + 4 + dy + 9), (456 + dx - 30, yy + 4 + dy + 10)], soft=0.8) * 0.55, out=sh)
    return sh


# ================================================================ the details on the ground (after the brush pass)
def ground_details(pic, R, seed, fast=False):
    """What lies on the ground, through the camera (depth.scatter: a true density for every square metre, so that it is
    few and large near us, many and small far off): stones each with its shadow to the left, ruts, footprints, straw;
    tufts, dandelions and violets on the banks, fallen petals drifted under the cherry; lime by the scaffold; the paving's
    joints; the parapets."""
    rng = np.random.default_rng(seed)
    L = Wet(SHAPE)
    ptz = lambda X_, z_: CAM.pt(X_, 0.0, z_)
    pxz = lambda X_, z_: CAM.scale(z_)
    road, bank, rmp, terr, rb = R["road"], R["bank"], R["ramp"], R["terrace"], R["rbank"]
    shadow_c = thin(mixp(COBALT, SIENNA, 0.42), 0.42)
    # ruts along the road: broken dark marks with a lit far lip, wandering, in short lengths (never a ruled line)
    for zc, wd in ((930.0, 1.0), (884.0, 1.2), (1012.0, 0.8), (962.0, 0.9)):
        X_ = -720.0
        while X_ < 720:
            ln = rng.uniform(60, 220)
            if rng.random() < 0.62:
                pts = []
                for t_ in np.linspace(0, 1, 7):
                    xx = X_ + ln * t_
                    z_ = zc - CAM.Z0 + 7 * math.sin(xx / 170.0 + zc) + 3 * math.sin(xx / 47.0) + rng.normal(0, 1.2)
                    pts.append(ptz(xx, z_))
                k = CAM.scale(zc - CAM.Z0)
                L.line(pts, lerp(EARTH_NEAR, thin(PRUSSIAN, 0.2), 0.25), wd * 1.5 * k * rng.uniform(0.6, 1.1), 0.38)
                if rng.random() < 0.5:
                    L.line([(px_, py_ - wd * 1.3 * k) for px_, py_ in pts[1:-1]], thin(mixp(OCHRE, NAPLES, 0.5), 0.60), wd * 0.7 * k, 0.32)
            X_ += ln + rng.uniform(10, 90)
    # patches of the road: dust lighter, the worn ground darker, in blotches lying flat
    for (x_, y_, k, r) in D.scatter(ptz, pxz, (-700, 700, -40, 260), 0.9, seed + 9, size=(60.0, 30.0), zone=road):
        L.ellipse(x_, y_, (40 + 70 * r) * k, (40 + 70 * r) * k * (y_ - HZ) / 800 * 0.9, thin(mixp(OCHRE, NAPLES, 0.4), 0.55) if r > 0.5 else EARTH, alpha=0.22)
    # stones: each with its shadow to the left (the sun is low on the right)
    for (x_, y_, k, r) in D.scatter(ptz, pxz, (-700, 700, -40, 260), 3.2, seed + 1, size=(6.0, 4.0), zone=road):
        sz = (2.0 + 6.0 * r ** 1.5) * k
        if sz < 0.7:
            continue
        L.ellipse(x_ - sz * 1.9, y_ + sz * 0.10, sz * 2.0, sz * 0.40, shadow_c, alpha=0.6)
        L.ellipse(x_, y_ - sz * 0.15, sz, sz * 0.55, lerp(lerp(STONE, STONE_COOL, rng.uniform(0, 0.7)), EARTH_NEAR, 0.15))
        L.ellipse(x_ + sz * 0.30, y_ - sz * 0.34, sz * 0.48, sz * 0.24, STONE_PALE, alpha=0.85)
    # footprints and straw along the road
    for (x_, y_, k, r) in D.scatter(ptz, pxz, (-700, 700, -40, 200), 4.0, seed + 2, size=(10.0, 6.0), zone=road):
        if r < 0.45:
            L.ellipse(x_, y_, 5.0 * k, 1.8 * k * (y_ - HZ) / 300, thin(mixp(SIENNA, OCHRE, 0.5), 0.36), alpha=0.35)
        elif r > 0.93:
            an = rng.uniform(-0.4, 0.4)
            ln = 9 * k
            L.line([(x_, y_), (x_ + math.cos(an) * ln, y_ + math.sin(an) * ln * 0.3)], thin(mixp(OCHRE, NAPLES, 0.6), 0.5), max(0.5, 0.7 * k), 0.85)
    # tufts on both banks: blades, bigger near us; dandelions and violets near the road
    for zone, bounds, dens in ((bank, (-900, 300, 100, 1000), 11.0), (rb, (100, 900, 150, 900), 9.0)):
        for (x_, y_, k, r) in D.scatter(ptz, pxz, bounds, dens, seed + 3 + int(dens), size=(4.0, 9.0), zone=zone):
            hgt = (5 + 10 * r) * k
            if hgt < 1.2:
                continue
            for j in range(3):
                lean = rng.uniform(-0.55, 0.55)
                tone = GRASS_SHADE if j < 2 else lerp(GRASS, NAPLES, 0.35)
                L.line([(x_ + j * 0.8 * k, y_), (x_ + j * 0.8 * k + lean * hgt * 0.5, y_ - hgt)], tone, max(0.45, 1.0 * k), 0.85)
            if r > 0.86 and y_ > 500:
                fc = lerp(PAINT("chrome-yellow"), WPAPER, 0.25) if r > 0.93 else thin(mixp(LILAC, ULTRA, 0.3), 0.35)
                L.ellipse(x_ + 1.5 * k, y_ - hgt * 0.7, max(0.7, 1.3 * k), max(0.6, 1.0 * k), fc)
    # petals fallen: drifts under the cherry and along the road below it, fewer farther off
    for (x_, y_, k, r) in D.scatter(ptz, pxz, (-800, 160, -40, 900), 40.0, seed + 4, size=(2.5, 2.5)):
        if (bank[int(y_), int(x_)] + road[int(y_), int(x_)]) < 0.5:
            continue
        near_tree = math.exp(-((x_ - 130) / 180.0) ** 2) * (0.35 + 0.65 * math.exp(-((y_ - 528) / 36.0) ** 2))
        if rng.random() > near_tree * 1.15:
            continue
        L.ellipse(x_, y_, max(0.6, 1.7 * k), max(0.4, 1.0 * k), PETAL if rng.random() < 0.6 else PETAL_LIT, alpha=0.92)
    # the right bank's azaleas in flower (late April): low clipped mounds along its top under the terrace's edge, each
    # lit on its right, its shadow to the left (low: nobody on the terrace stands behind them)
    for i in range(7):
        cx_ = 630 + i * 24 + rng.uniform(-6, 6)
        cy_ = rng.uniform(486, 496)
        w_ = rng.uniform(9, 14)
        hgt = w_ * 0.62
        L.ellipse(cx_ - w_ * 1.6, cy_ + 0.5, w_ * 1.5, w_ * 0.22, shadow_c, alpha=0.5)
        mound = [(cx_ + math.cos(t) * w_ * (1 + 0.1 * math.sin(5 * t + i)), cy_ - max(math.sin(t), -0.15) * hgt * (1 + 0.1 * math.sin(4 * t))) for t in np.linspace(math.pi, 2 * math.pi, 12)] + [(cx_ + w_, cy_ + 1), (cx_ - w_, cy_ + 1)]
        mound = [(px_, py_ if py_ <= cy_ else cy_ + 1) for px_, py_ in [(px_, 2 * cy_ - py_) for px_, py_ in mound]]
        L.poly(mound, GRASS_SHADE, lerp(GRASS, NAPLES, 0.2), g=((cx_ - w_, cy_), (cx_ + w_, cy_ - hgt)))
        for j in range(int(w_ * 0.8)):
            px_ = cx_ + rng.uniform(-0.85, 0.85) * w_
            py_ = cy_ - rng.uniform(0.15, 0.95) * hgt * math.sqrt(max(0.0, 1 - ((px_ - cx_) / w_) ** 2))
            L.ellipse(px_, py_, 1.1, 0.9, lerp(thin(mixp(LAKE, "vermilion", 0.3), 0.40), WPAPER, 0.25 if px_ > cx_ else 0.0))
    # lime on the terrace by the scaffold, and down the wall's foot
    for i in range(170):
        px_, py_ = rng.normal(512, 48), rng.normal(456, 9)
        if TERRACE["x0"] + 2 < px_ < 604 and TERRACE["top"] + 1 < py_ < TERRACE["front"] - 2:
            L.ellipse(px_, py_, rng.uniform(0.8, 2.8), rng.uniform(0.5, 1.2), lerp(WPAPER, CERULEAN, 0.04), alpha=0.95)
    for i in range(40):
        px_, py_ = rng.uniform(452, 575), TERRACE["top"] - rng.uniform(0, 14) ** 1.25 * 0.7
        L.ellipse(px_, py_, rng.uniform(0.6, 1.8), rng.uniform(0.5, 1.4), lerp(WPAPER, CERULEAN, 0.04), alpha=0.9)
    paving(L, rng)
    parapets(L, rng)
    keyline(L, [(-10, ROAD_TOP + 2), (RAMP["foot"][0], ROAD_TOP)], row=ROAD_TOP, seed=11)
    keyline(L, [(RAMP["foot"][1], ROAD_TOP), (810, ROAD_TOP + 2)], row=ROAD_TOP, seed=12)
    c, a = L.done()
    over(pic, c, a)
    return pic


# ================================================================ the passes
def under(seed=SEED):
    pic, info = FAR.paint_far(seed)
    R = regions()
    info["R"] = R
    info["wall"] = paint_wall(pic, R, seed + 20)
    info["water"] = paint_water(pic, R, seed + 21)
    paint_ground(pic, R, seed + 22)
    L = Wet(SHAPE)
    passage(L)
    c, a = L.done()
    over(pic, c, a)
    # shadows: the things' on the ground, the scaffold's on the wall, the pine's beyond the right edge
    things = shadow_mask_things(seed + 30) * R["ground"]
    tree = shadow_mask_tree(R, seed + 31) * np.clip(R["ground"] + R["water"], 0, 1)
    marks = np.ones(SHAPE, F32)                                                   # thin where people chiefly stand
    for (mx, my) in ((150, 580), (176, 526), (228, 512), (300, 506), (420, 584), (560, 520)):
        marks *= 1 - 0.45 * mask_ellipse(SHAPE, mx, my, 30, 10, soft=8)
    tree *= marks
    walls = wall_shadows(seed + 32) * np.clip(info["wall"], 0, 1)
    info["shadow"] = np.maximum(np.maximum(things, tree * 0.8), walls)
    glaze_ = lambda m, a: tint(pic, GLAZE, np.clip(m * a, 0, 1).astype(F32))
    glaze_(things, 0.95)
    glaze_(tree, 1.0)
    glaze_(walls, 0.85)
    info["tree"] = tree
    D.frame(pic, amount=0.12, bottom=0.16, color="#3a2a30")
    return np.clip(pic, 0, 1).astype(F32), info


def wet_mask(info):
    """watercolor.wash's `soft`: the sky and its clouds wet in wet (1), the hills (0.55 to 0.65) and the town (0.45), the
    water 0.6 at the far wall falling to 0.25 at the near bank; the keep, the hill's pines and everything standing in the
    play wet on dry (0)."""
    x, y = grid(SHAPE)
    sky = (y < HZ + 2).astype(F32) * (1 - np.clip(info["keep"] + info["wing"] + info["hill"], 0, 1))
    m = sky * (1 - 0.40 * info["hills"]) * (1 - 0.45 * info["town"])
    water = info["water"] * np.clip(0.6 - (y - MOAT["far"]) / 120.0, 0.25, 0.6)
    return np.clip(np.maximum(m, water), 0, 1).astype(F32)


def to_file(picture, name, colors=128, alpha=None, seed=7, speckle=0.010, amount=0.010):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


CUTS = ["ladder", "gate", "scaffold", "tub", "bucket-1", "bucket-2", "bucket-3", "cherry", "near"]   # back to front, as the scene lists them
GAME_ORDER = ["gate", "ladder", "scaffold", "tub", "bucket-3", "bucket-1", "bucket-2", "cherry", "near"]     # as the game sorts them (by base)
COLORS = {"ladder": 48, "gate": 128, "scaffold": 64, "tub": 48, "bucket-1": 32, "bucket-2": 32, "bucket-3": 32, "cherry": 128, "near": 128}


def main(argv):
    import edo_castle_cuts as CU
    import edo_castle_near as NEAR
    t0 = time.time()
    fast = "fast" in argv
    out = OUT + ("-fast" if fast else "")
    os.makedirs(out, exist_ok=True)
    base, info = under()
    Image.fromarray((base * 255).astype(np.uint8)).save(OUT + "-1-under.png")
    print("under", round(time.time() - t0, 1))
    wet = wet_mask(info)
    if fast:
        pic = base.copy()
    else:
        brushed_ = strokes(base, sizes=(12, 6, 3), seed=2, density=1.4, jitter=0.02, keep=0.0)
        keep = np.clip(0.52 + 0.36 * wet + 0.30 * np.clip(info["keep"] + info["wing"], 0, 1), 0, 0.92)
        pic = lerp(brushed_, base, keep[..., None]).astype(F32)
    print("brushed", round(time.time() - t0, 1))
    ground_details(pic, info["R"], SEED + 40, fast)
    print("details", round(time.time() - t0, 1))
    planes = CU.cut_layers(pic, info, fast)
    planes["near"] = NEAR.near_cut(pic, info, SEED + 60, fast)
    whole = pic.copy()
    for name in GAME_ORDER:
        c, a = planes[name]
        over(whole, c, (a > 0.5).astype(F32))
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(out + "-2-all.png")
    print("painted", round(time.time() - t0, 1))
    # the watercolour finish: the backdrop washed, every cut-out washed over the unwashed backdrop with the same seed
    back_w = WC.wash(pic, seed=SEED, soft=wet, wander=1.5)
    sizes = {"back": to_file(back_w, out + "/back.png", 250)}
    for name in CUTS:
        c, a = planes[name]
        hard = (a > 0.5).astype(F32)
        keep_ = info.get("tile_keep") if name == "gate" else None                   # the cross on the gable's tile stays as drawn
        washed = WC.wash_cut(c, hard, pic, seed=SEED, soft=wet, keep=keep_, wander=1.5, crisp=True)
        sizes[name] = to_file(washed, out + f"/{name}.png", COLORS[name], hard)
    print(sizes)
    import edo_castle_herons as HE
    HE.paint_all(out)
    import edo_castle_layout as LY
    LY.write(out + "/layout.json", planes={n: planes[n][1] for n in CUTS}, info=info)
    comp = Image.open(out + "/back.png").convert("RGBA")
    for name in GAME_ORDER:
        comp.alpha_composite(Image.open(f"{out}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(out + "-comp.png")
    print("done", round(time.time() - t0, 1))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main(sys.argv[1:])

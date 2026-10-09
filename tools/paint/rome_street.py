"""Rome, 44 B.C., the Ides of March: a shopping street on the way to the Forum, early on a fine morning.

LIGHT. Morning sun from the upper right and a little behind us, low over the roofs: it travels to the
left, downward and away (LIGHT below). The tall right-hand houses throw one big cool shadow over the
roadway, the fountain and the snack bar; the left-hand house is in warm sun from about first-floor
height up; the washing on the lines blazes where it hangs above the edge of the shadow.

THE PLACE. We stand where a side street meets the main one (it runs off to the left, in front of the
snack bar). The main street runs straight away up the middle of the picture to the vanishing point
(400, 230), between a two-storey corner house on the left and a tall apartment block on the right,
and opens far off into the sunlit Forum, where a cream temple stands on its high base.

THREE TONES. Dark: the right-hand wall and the roadway, deepest in the bottom corners. Middle: the
shaded shop under its awning, the far end of the street. Light: the sunlit upper wall on the left,
the washing (brightest of all), the Forum at the end of the street.

WHERE THINGS ARE. Left: the snack bar under its striped awning (counter front x 55-194, y 420-480,
keeper behind it at 151, 459), the price list on the pier at the left edge, the crossroads shrine with
its snake on the corner pier (x 197-229), the basket of washing on the corner of the sidewalk
(266, 494), the low line with the small tunic above it (273, 333). Middle: three stepping stones at
y 451-477, the roadway, a drain cover bottom left, a loaded handcart far up the street, the exit to
the Forum and the temple (x 368-432, y 182-243). Right: the fountain against the wall (x 541-700,
y 355-502), a painted notice and scratched scribbles nearer us, the timber balcony the washing lines
are tied to (x 560-720, y 30-275), the cat on a sill (745, 180). Bottom right, in front of
everything: two wine jars and a handcart wheel.

ROUND FOUR: the fountain's falling water and its rings, the sparrow drinking, the pigeons, the swallows, the cat's tail,
the shrine's flame and the glints on the running water are no longer painted (PAINT_MOVING = True paints them as
before); the game draws them moving from the marks in layout.json "fx". rome_street_four.py paints the frames and
cuts the washing into pieces that can stir; rome_street_check4.py proves nothing else changed."""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
import sky
import letter
from rome_street_kit import *

PAINT_MOVING = False                                        # round four: the fountain's running water, the birds, the cat's tail and the shrine's
                                                            # flame are the game's to draw, moving (layout.json "fx"; rome_street_four.py); True paints
                                                            # them in, still, as the picture was before
LIGHT = (-0.62, -0.50, 0.60)                                # the way the sunlight travels, in the world
SKY_LIGHT = (0.70, -0.70)                                   # toward the sun, in the picture (for clouds)
SUN_T = 0.50 / 0.62                                         # a shadow falls this much for every cm it crosses the street
SUN_Z = 0.60 / 0.62                                         # ...and slides this much down the street

# ---------------------------------------------------------------- the street, in centimetres
KL, KR = -150.0, 150.0                                      # the kerbs of the main street
SWH = 18.0                                                  # how high the sidewalks stand
WL, WR = -250.0, 420.0                                      # the house fronts, left and right
ZF = 330.0                                                  # the snack bar's front wall: it faces us across the side street
ZK = 220.0                                                  # the kerb in front of it
L1 = dict(z0=ZF, z1=930.0, h=640.0, ridge=766.0, zr=630.0)  # the corner house (snack bar below, a room above)
L2 = dict(z0=930.0, z1=3000.0, h=720.0)
L3 = dict(z0=3400.0, z1=6000.0, h=800.0)
RA = dict(z0=-80.0, z1=720.0, h=940.0)                      # right-hand houses: the one with the balcony,
RB = dict(z0=720.0, z1=1650.0, h=1260.0)                    # the apartment block, four floors,
RC = dict(z0=1650.0, z1=3000.0, h=760.0)                    # and a lower one beyond it
R3 = dict(z0=3400.0, z1=6000.0, h=800.0)
FORUM = 6000.0                                              # where the street ends and the open square begins
SHOP = dict(x0=-520.0, x1=-310.0, top=300.0, back=550.0)    # the snack bar's opening and room
BAR = dict(x0=-520.0, x1=-310.0, z0=ZF, z1=410.0, top=108.0)                # the counter's front arm
ARM = dict(x0=-520.0, x1=-452.0, z0=410.0, z1=550.0, top=108.0)             # and the arm that runs back along the wall
AWN = dict(x0=-585.0, x1=-292.0, z0=ZF, z1=212.0, y0=342.0, y1=296.0, drop=26.0)
FOUNT = dict(x0=228.0, x1=414.0, z0=235.0, z1=395.0, h=82.0, wall=15.0)
STONES = [(-137.0, -83.0), (-29.0, 30.0), (82.0, 133.0)]    # the stepping stones, across
STONE_Z = (402.0, 470.0)
STONE_H = 22.0
STONE_OWN = [(0.0, 3.0, 0.0), (-6.0, -4.0, 2.5), (4.0, 0.0, -1.5)]            # each one's own start, end and height, added to those
BALC = dict(x=318.0, z0=180.0, z1=640.0, floor=352.0, rail=452.0, top=598.0, posts=(180.0, 333.0, 486.0, 640.0))
RIDGE_PIGEONS = ((-582.0, 1, "#8d96ac"), (-556.0, -1, "#a8a4a8"), (-436.0, 1, "#7a8298"), (-300.0, -1, "#e8e4dc"))   # x along the ridge, facing, tone
SWALLOWS = ((372, 44, 3.2), (430, 66, 2.6), (352, 78, 2.2), (462, 22, 2.8))                                     # x, y, size (px)
SHADOW_L = 397.0                                            # how high the shadow stands on the left-hand wall
BASKET = (-192.0, 268.0)                                    # where the washing basket stands (x, z), on the sidewalk


def shadow_edge_front(x):
    """How high the shadow stands on the snack bar's front wall (it dips a little to the left)."""
    return SHADOW_L - 4 + 0.075 * (x - WL)


def shadow_air(x):
    """...and in the open air over the street: the shadow is a slope, low on the left and high on the right."""
    return SHADOW_L + (x - WL) * 0.36


# ---------------------------------------------------------------- materials (local colors, before light)
OCHRE, CREAM, RED, DADO = "#e6c084", "#f1e2c2", "#bd4a32", "#8e3128"
BRICK, MORTAR, TUFA = "#b9664a", "#dcc7a4", "#bba98a"
BASALT, KERB, EARTH = "#7a747e", "#c9c0ae", "#a48e76"
TILE, WOOD, WOODD, GREENW, BLUEW = "#d46c40", "#9a6a42", "#5c3c28", "#5e8c7a", "#6a86a8"
STONE = "#cfc6b4"
ROOM = "#30242e"                                            # what a window or door shows of the room behind it


class Dr:
    """A clear sheet drawn on in the world's own measurements."""

    def __init__(self):
        self.s = Sheet2(SHAPE)

    def poly(self, pts, color, a=1.0):
        self.s.poly(Q(pts), color, a)
        return self

    def line(self, pts, color, w=1.0, a=1.0):
        self.s.line(Q(pts), color, w, a)
        return self

    def front(self, x0, x1, y0, y1, z, color, a=1.0):
        return self.poly([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], color, a)

    def side(self, x, z0, z1, y0, y1, color, a=1.0):
        return self.poly([(x, y0, z0), (x, y0, z1), (x, y1, z1), (x, y1, z0)], color, a)

    def flat(self, x0, x1, z0, z1, y, color, a=1.0):
        return self.poly([(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)], color, a)

    def box(self, x0, x1, y0, y1, z0, z1, local, sun=0.0, a=1.0, dim=1.0):
        """A box in the shade (or the sun): top to the sky, front to us, one side to the street."""
        cam.box(self.s, x0, x1, y0, y1, z0, z1, lit(local, sun, "front") * dim, lit(local, sun, "up") * dim,
                (lit(local, sun, "warm") * dim, lit(local, sun * 0.6, "front") * 0.86 * dim), a)
        return self


def plaster(u, y, base, seed, patch=0.10, streak=0.05, mend=0.0):
    """A plastered wall in its own measurements: uneven washes, runs of dirt, warmer and cooler places, and
    (with `mend`) squarish patches where it has been made good with newer, paler plaster."""
    c = np.empty(u.shape + (3,), dtype=F32)
    c[...] = col(base)
    big = wn(u, y, 190, seed, 4) - 0.5
    mid = wn(u, y, 46, seed + 1, 3) - 0.5
    run = wn(u * 5.0, y, 170, seed + 2, 3) - 0.5                # dirt and rain run downward
    c *= (1 + big * 2.6 * patch + mid * patch * 1.1 + run * 2 * streak)[..., None]
    k = (wn(u, y, 260, seed + 3, 3) - 0.5) * 0.09               # warmer and cooler washes
    c[..., 0] += k
    c[..., 2] -= k
    if mend:
        gu, gv = np.floor(u / 150.0), np.floor(y / 110.0)
        pick = _hash(gu, gv, seed + 5) < mend
        fu, fv = u / 150.0 - gu, y / 110.0 - gv
        a0, a1, b0, b1 = (0.10 + 0.25 * _hash(gu, gv, seed + q) for q in (6, 7, 8, 9))
        inside = (fu > a0) & (fu < 1 - a1) & (fv > b0) & (fv < 1 - b1) & pick
        soft = step(0.30, 0.42, wn(u, y, 22, seed + 4, 3))
        c = lerp(c, np.clip(c * 1.10 + 0.03, 0, 1), (inside * soft * 0.8)[..., None])
    return np.clip(c, 0, 1)


def bare(u, y, seed, much=0.5, cell=120.0):
    """Where the plaster has fallen and the wall shows through: ragged patches."""
    n = wn(u, y, cell, seed, 4) + (wn(u, y, cell * 0.2, seed + 1, 3) - 0.5) * 0.3
    return step(1.0 - much * 0.42, 1.03 - much * 0.42, n)


def brickwork(u, y, seed, px=1.0):
    """Courses of flat Roman brick with pale mortar, in a wall's own measurements."""
    course = 7.0
    row = np.floor(y / course)
    fy = y / course - row
    fu = (u + row * 13.0) / 27.0
    fu = fu - np.floor(fu)
    c = np.empty(u.shape + (3,), dtype=F32)
    c[...] = col(BRICK)
    tone = _hash(np.floor((u + row * 13.0) / 27.0), row, seed)
    c *= (0.82 + 0.34 * tone)[..., None]
    soft = np.clip(px / course, 0.12, 2.0)
    joint = np.clip((0.16 - np.minimum(fy, 1 - fy)) / soft + 0.5, 0, 1) * np.clip(1.6 - soft * 1.2, 0, 1)
    joint = np.maximum(joint, np.clip((0.06 - np.minimum(fu, 1 - fu)) / (soft * 0.3) + 0.5, 0, 1) * np.clip(1.2 - soft * 1.5, 0, 1))
    over(c, col(MORTAR), (joint * 0.8).astype(F32))
    return c


def _hash(a, b, seed):
    h = np.sin(a * 127.1 + b * 311.7 + seed * 74.7) * 43758.5453
    return (h - np.floor(h)).astype(F32)


def stones(u, v, cell, seed, jitter=0.9, drop=0.27):
    """Like the kit's `cells`, but some of the cells' middles are left out, so their neighbours spread into the
    room: big slabs among small ones, as a paviour fits what the quarry sends. -> (distance to the nearest
    joint, a random number per stone, another, distance to the stone's middle)"""
    u = u.astype(np.float64)
    v = v.astype(np.float64)
    iu, iv = np.floor(u / cell), np.floor(v / cell)
    best = np.full(u.shape, 1e9)
    second = np.full(u.shape, 1e9)
    r1 = np.zeros(u.shape, dtype=F32)
    r2 = np.zeros(u.shape, dtype=F32)
    for du in range(-2, 3):
        for dv in range(-2, 3):
            cu, cv = iu + du, iv + dv
            su = (cu + 0.5 + (_hash(cu, cv, seed) - 0.5) * jitter) * cell
            sv = (cv + 0.5 + (_hash(cu, cv, seed + 17) - 0.5) * jitter) * cell
            d = np.where(_hash(cu, cv, seed + 91) < drop, 1e9, np.hypot(u - su, v - sv))
            closer = d < best
            second = np.where(closer, best, np.minimum(second, d))
            r1 = np.where(closer, _hash(cu, cv, seed + 31), r1)
            r2 = np.where(closer, _hash(cu, cv, seed + 47), r2)
            best = np.where(closer, d, best)
    return ((second - best) * 0.5).astype(F32), r1, r2, best.astype(F32)


# ================================================================ the backdrop: broad and soft
def under(seed=5):
    """Everything broad and soft: sky, the far Forum, the roadway, the big planes of wall and their light."""
    shape = SHAPE
    x, y = grid(shape)
    info = {}

    # ---- the sky between the roofs: deep blue overhead, paler down the street, one heap of cloud
    pic = sky.field(shape, HZ, [(0.0, "#1c56aa"), (0.30, "#2c72c8"), (0.62, "#5f9fde"), (0.86, "#b4d2ea"), (1.0, "#f3e6c8")], seed, haze="#f8ecd0", patch=0.03)
    sky.paint_clouds(pic, [(474, 96, 130, 58, 16), (110, 44, 240, 32, 9), (372, 26, 110, 22, 6)], seed + 4,
                     tones=("#7d9cd4", "#bccde8", "#fbf2dc", "#fffdf0"), light=SKY_LIGHT, ragged=8, reach=30.0)

    # ---- the Forum at the end of the street: a hill in the haze, the temple on its high base
    hill = mask_poly(shape, [(340, 232), (352, 214), (372, 204), (398, 199), (424, 203), (452, 196), (476, 206), (492, 232)], soft=1.2, wobble=1.5, seed=seed + 7)
    over(pic, ramp(np.clip((y - 196) / 36, 0, 1), [(0.0, "#c9c6dc"), (1.0, "#dcd6dc")]), hill * 0.9)
    far_temple(pic, seed)

    # ---- the ground: roadway of basalt, sidewalks, kerbs
    xf, zf, kf, okf = level(0.0)
    xs, zs, ks, oks = level(SWH)
    ground = okf & (PY > HZ + 0.5)
    out_r = lambda zz: (_hash(np.floor(zz / 118.0 + 0.37), 2.0, seed) - 0.5) * 7.0                # no kerbstone is quite in line with the next
    out_l = lambda zz: (_hash(np.floor(zz / 118.0), 1.0, seed) - 0.5) * 7.0
    out_f = lambda xx: (_hash(np.floor(xx / 104.0), 3.0, seed) - 0.5) * 7.0
    walk_r = oks & (xs > KR + out_r(zs)) & (zs < FORUM)
    walk_l = oks & (xs < KL + out_l(zs)) & (zs > ZK + out_f(xs)) & (zs < FORUM)
    sidewalk = (walk_r | walk_l) & (PY > HZ + 0.5)
    under_walk = ((xf > KR + out_r(zf)) | ((xf < KL + out_l(zf)) & (zf > ZK + out_f(xf)))) & (zf < FORUM)
    kerb = ground & under_walk & ~sidewalk
    road = ground & ~under_walk
    sun_floor = np.clip((zf - (FORUM - 80)) / 160, 0, 1)                                   # the open square is in full sun
    bar = zf + xf * SUN_Z                                                                  # and a bar of sun comes through a side street
    sun_floor = np.maximum(sun_floor, band(bar, 3000 + WR * SUN_Z, 3400 + WR * SUN_Z, 70.0) * 0.92)
    sun_walk = np.maximum(np.clip((zs - (FORUM - 80)) / 160, 0, 1), band(zs + xs * SUN_Z, 3000 + WR * SUN_Z, 3400 + WR * SUN_Z, 70.0) * 0.92)

    stone = paving(xf, zf, kf, seed)
    info["paving"] = stone
    local = stone["soft"].copy()
    wet = wet_places(xf, zf, seed)
    local = local * (1 - wet * 0.30)[..., None]
    floor = light(local, sun_floor, "up")
    sheen = np.clip(stone["crown"] * 0.6 + wet * 0.5, 0, 1) * (1 - sun_floor)              # worn tops and wet places give back the sky
    floor = lerp(floor, col("#7f93c4"), (sheen * 0.30)[..., None])
    pud = puddles(xf, zf, seed) * (1 - sun_floor) * (xf < KR)
    mirror = ramp(wn(xf * 0.4, zf * 2.0, 60, seed + 96, 3), [(0.0, "#2f4f8e"), (0.55, "#4a78bc"), (0.86, "#7fa6dc"), (1.0, "#dbe8fb")])     # they hold the sky, and a white piece of the washing
    floor = lerp(floor, mirror, (pud * 0.9)[..., None])
    over(pic, far(floor, zf, "#c4c8dc", 5200.0, 0.8), road.astype(F32))
    # the square beyond is pale travertine in the sun
    over(pic, far(light(vary("#d9cdb6", shape, seed + 3, 0.04, 30), sun_floor, "up"), zf, "#f1e6cf", 9000.0, 0.8), (road & (zf > FORUM)).astype(F32))

    # sidewalks: beaten earth and broken tile behind a row of kerbstones, paler than the road
    sw_local = np.empty(shape + (3,), dtype=F32)
    sw_local[...] = col("#b3a38e")
    sw_local *= (1 + (wn(xs, zs, 120, seed + 11) - 0.5) * 0.24 + (wn(xs, zs, 26, seed + 12, 3) - 0.5) * 0.14)[..., None]
    edge_r = np.clip(1 - (xs - KR - out_r(zs)) / 34.0, 0, 1) * walk_r                      # the kerbstones themselves are pale grey stone
    edge_l = np.clip(1 - (KL + out_l(zs) - xs) / 34.0, 0, 1) * walk_l
    edge_f = np.clip(1 - (zs - ZK - out_f(xs)) / 34.0, 0, 1) * walk_l
    kerbtop = np.clip(np.maximum(np.maximum(edge_r, edge_l), edge_f) * 30, 0, 1)
    each = np.where(edge_f > 0, _hash(np.floor(xs / 104.0), 3.0, seed), _hash(np.floor(zs / 118.0 + (xs > 0) * 0.37), 1.0 + (xs > 0), seed))
    over(sw_local, vary(KERB, shape, seed + 13, 0.07, 18) * (0.86 + 0.24 * each)[..., None], kerbtop.astype(F32))
    slab_e, slab_r, slab_r2, _ = cells(xs + (wn(xs, zs, 150, seed + 15, 2) - 0.5) * 24, zs * 0.8, 96.0, seed + 16)    # the right-hand one is laid with big worn flags
    flags = walk_r & (xs > KR + 34)
    sw_local *= np.where(flags, 0.92 + 0.16 * slab_r, 1.0)[..., None]
    cob_e, cob_r, cob_r2, _ = cells(xs, zs * 0.9, 38.0, seed + 17)                                     # the other is cobbled with small stones
    cobbles = walk_l & ~((xs < KL + 34) & (xs > KL - 34) & (zs > ZK + 34)) & ~((zs < ZK + 34))
    sw_local *= np.where(cobbles, 0.86 + 0.26 * cob_r, 1.0)[..., None]
    info.update(slab_e=slab_e, flags=flags, cob_e=cob_e, cobbles=cobbles)
    dirty = np.clip(1 - (WR - xs) / 60.0, 0, 1) * walk_r + np.clip(1 - (zs - ZF + 2) / -50.0, 0, 1) * walk_l * (xs < WL) + np.clip(1 - (xs - WL) / 40.0, 0, 1) * walk_l * (zs > ZF)
    sw_local *= (1 - np.clip(dirty, 0, 1) * 0.22 * (0.5 + wn(xs, zs, 50, seed + 18, 3)))[..., None]     # dirt gathers along the foot of every wall
    wet_s = wet_places(xs, zs, seed)
    sw_local *= (1 - wet_s * 0.50)[..., None]
    walk_c = lerp(light(sw_local, sun_walk, "up"), light(sw_local, sun_walk, "warm"), 0.45) * 1.06
    walk_c = lerp(walk_c, col("#4a5a92"), (wet_s * 0.22 * (1 - sun_walk))[..., None])                   # wet stone is darker and bluer
    walk_c = walk_c * np.where(walk_r, 0.92, 1.0)[..., None]
    over(pic, far(walk_c, zs, "#c4c8dc", 5200.0, 0.8), sidewalk.astype(F32))
    kerb_local = vary("#a79f94", shape, seed + 14, 0.08, 14) * (0.84 + 0.28 * _hash(np.floor(zf / 118.0 + (xf > 0) * 0.37), 1.0 + (xf > 0), seed))[..., None]
    over(pic, far(light(kerb_local, sun_floor * 0, "front"), zf, "#c4c8dc", 5200.0, 0.8), kerb.astype(F32))
    info.update(road=road, sidewalk=sidewalk, kerb=kerb, xf=xf, zf=zf, kf=kf, xs=xs, zs=zs, ks=ks, sun_floor=sun_floor, wet=wet, wet_s=wet_s, kerbtop=kerbtop, pud=pud, mirror=mirror)

    # ---- the houses, far ones first
    houses(pic, info, seed)

    # ---- the street floor again where it is darkest: under the walls, in the corners of the picture
    ground_all = (road | sidewalk | kerb).astype(F32) * (1 - info["walls"])                # (only where the ground is not hidden by a house)
    corner = np.clip(((x - 400) / 400) ** 2 * 0.45 + ((y - 430) / 170).clip(0, 2) ** 2 * 0.55, 0, 1)
    tint(pic, "#6a5a86", (corner * 0.36 * ground_all).astype(F32))
    info["ground"] = ground_all
    return np.clip(pic, 0, 1), info


def wet_places(xx, zz, seed):
    """Where the paving is wet: round the fountain, and down the right-hand gutter, which runs away to the Forum."""
    round_f = np.clip(1.25 - np.hypot((xx - 290) / 180.0, (zz - 300) / 170.0), 0, 1) ** 0.7
    round_f *= 0.45 + 0.9 * wn(xx, zz, 60, seed + 91, 3)
    gutter = np.clip(1 - np.abs(xx - (KR - 14)) / (16.0 + 10 * wn(xx, zz, 90, seed + 92, 2)), 0, 1) * np.clip((zz - 230) / 60.0, 0, 1) * np.clip((5200 - zz) / 800.0, 0, 1)
    spill = np.clip(1 - np.abs(zz - 300 - (xx - 150) * 0.2) / 34.0, 0, 1) * band(xx, 140, 240, 12.0)       # from the basin's lip across the sidewalk
    return np.clip(np.maximum(np.maximum(round_f, gutter * 0.95), spill * 0.9), 0, 1).astype(F32)


def puddles(xx, zz, seed):
    """Water standing in the roadway."""
    m = np.zeros(xx.shape, dtype=F32)
    for (cx, cz, rx, rz, s) in ((176.0, 300.0, 22.0, 34.0, 0),):                                        # (only where the basin spills into the gutter)
        d = 1 - np.hypot((xx - cx) / rx, (zz - cz) / rz) + (wn(xx, zz, 30, seed + 95 + s, 3) - 0.5) * 0.9
        m = np.maximum(m, step(0.0, 0.10, d))
    return m.astype(F32)


def far_temple(pic, seed):
    """The temple the street leads to, small and pale with distance: six columns on a high base under a low
    gable. (Another painter has it close up in the next scene: cream stucco, the columns' feet reddish.)"""
    s = Sheet2(SHAPE)
    z = 24000.0

    def at(xx, yy):
        return P(xx, yy, z)
    lit_c, shade_c, dark = "#fdf3dc", "#cbc6dc", "#9c9cc4"
    s.poly([at(-1150, 0), at(1150, 0), at(1150, 430), at(-1150, 430)], "#eadfc9")              # the base
    s.poly([at(-520, 0), at(520, 0), at(430, 430), at(-430, 430)], "#f6ecd6")                  # the steps up its front
    for i in range(1, 7):
        yy = i * 430 / 7
        w2 = lerp(520, 430, i / 7)
        s.line([at(-w2, yy), at(w2, yy)], "#cdbfb4", 0.6, 0.6)
    s.poly([at(-1000, 430), at(1000, 430), at(1000, 1480), at(-1000, 1480)], dark)            # the porch in shadow behind the columns
    for i in range(6):
        cx = -880 + i * 352
        s.poly([at(cx - 75, 430), at(cx + 75, 430), at(cx + 66, 1480), at(cx - 66, 1480)], shade_c)
        s.poly([at(cx - 10, 430), at(cx + 75, 430), at(cx + 66, 1480), at(cx - 6, 1480)], lit_c)
        s.poly([at(cx - 75, 430), at(cx + 75, 430), at(cx + 72, 760), at(cx - 72, 760)], "#e6b8a4", 0.55)   # the feet of the columns are reddish
    s.poly([at(-1080, 1480), at(1080, 1480), at(1080, 1640), at(-1080, 1640)], lit_c)         # the beam they carry
    s.line([at(-1080, 1490), at(1080, 1490)], "#c2b3b4", 0.6, 0.7)
    s.poly([at(-1130, 1640), at(1130, 1640), at(0, 1960)], "#f1dcc0")                         # the gable
    s.poly([at(-1130, 1640), at(0, 1960), at(1130, 1640), at(1040, 1640), at(0, 1900), at(-1040, 1640)], "#dfa184")    # its tiles
    s.onto(pic)
    return pic


def paving(xf, zf, kf, seed):
    """The roadway: big many-sided basalt stones, fitted close, worn round. -> local colors soft and crisp."""
    wob_x = (wn(xf, zf, 130, seed + 21, 3) - 0.5) * 30
    wob_z = (wn(xf, zf, 130, seed + 22, 3) - 0.5) * 30
    edge, r1, r2, mid = stones(xf + wob_x, zf * 0.86 + wob_z, 60.0, seed + 23)
    dz = (Z0 + np.maximum(zf, -40)) ** 2 / (EYE * F)                                        # how many centimetres a pixel covers, going away
    foot = np.maximum(dz * 0.42, 1 / kf)
    seen = np.clip(3.4 / np.maximum(dz, 0.1), 0, 1) ** 0.6                                   # far off the joints run together
    joint = np.clip((1.5 + r2 * 1.9 - edge) / foot + 0.5, 0, 1) * seen
    wide = np.clip((9.0 - edge) / np.maximum(foot, 4.0), 0, 1) * seen                        # the worn shoulder beside each joint
    c = np.empty(xf.shape + (3,), dtype=F32)
    c[...] = col(BASALT)
    tone = 0.74 + 0.52 * r1 ** 1.3 + (wn(xf, zf, 300, seed + 24) - 0.5) * 0.22
    c *= tone[..., None]
    warm = (r2 - 0.5) * 0.09 + (wn(xf, zf, 420, seed + 25, 3) - 0.5) * 0.08                  # some stones browner, some bluer
    c[..., 0] += warm
    c[..., 2] -= warm * 0.8
    crown = np.clip(edge / 26.0, 0, 1) ** 0.7 * np.clip(1.25 - mid / 70.0, 0, 1) * seen                    # each stone's crown, polished by feet
    soft = c * (1 + crown * 0.10 - wide * 0.16)[..., None]
    crisp = c * (1 + crown * 0.16 - wide * 0.10)[..., None]
    over(soft, col("#3a3038"), (joint * 0.55).astype(F32))
    gy, gx = np.gradient(mid)
    return dict(soft=np.clip(soft, 0, 1), crisp=np.clip(crisp, 0, 1), joint=joint.astype(F32), wide=wide.astype(F32), crown=crown.astype(F32),
                seen=seen.astype(F32), r1=r1, r2=r2, gx=np.sign(gx).astype(F32), gy=np.sign(gy).astype(F32), edge=edge, foot=foot.astype(F32))


def sun_left(z, y, wob=0.0):
    """Sun on the left-hand street walls. The right-hand roofs are of three heights, so the shadow's edge steps."""
    low = above(y, SHADOW_L + wob, 9.0)                                   # under the first house: sun from the first floor up
    none = np.zeros_like(low)                                             # under the tall block: no sun at all
    part = above(y, 217.0 + wob, 12.0)                                    # beyond it: sun nearly to the ground
    a = np.clip((z - (RB["z0"] + (WR - WL) * SUN_Z)) / 14.0 + 0.5, 0, 1)
    b = np.clip((z - (RC["z0"] + (WR - WL) * SUN_Z)) / 24.0 + 0.5, 0, 1)
    return lerp(lerp(low, none, a), part, b).astype(F32)


def houses(pic, info, seed):
    shape = SHAPE
    zl, yl, kl, okl = wall_x(WL)
    zr, yr, kr, okr = wall_x(WR)
    dzl = (Z0 + zl) ** 2 / (abs(WL) * F)
    dzr = (Z0 + zr) ** 2 / (abs(WR) * F)
    info.update(zl=zl, yl=yl, kl=kl, zr=zr, yr=yr, kr=kr, dzl=dzl, dzr=dzr)
    built = [(PY > HZ + 0.5).astype(F32)]

    # ================= far houses on both sides, beyond the side street
    for (zz, yy, kk, ok, dz, B, tone, s) in ((zl, yl, kl, okl, dzl, L3, "#ecd3a4", 31), (zr, yr, kr, okr, dzr, R3, "#e6c9a8", 37)):
        m = band(zz, B["z0"], B["z1"], dz) * band(yy, SWH, B["h"], 1 / kk) * ok
        local = plaster(zz, yy, tone, seed + s, 0.06, 0.03)
        sun = above(yy, 260, 30.0) if B is L3 else np.zeros(shape, dtype=F32)
        over(pic, far(light(local, sun, "warm" if B is R3 else "front"), zz, "#c9cee2", 5200.0, 0.8), m)
        built.append(m)
    # the near ends of those far houses, which face us across the side street: slivers, the right one in sun
    xg, yg, kg = wall_z(L3["z0"])
    for tone_, s_, lo_, hi_, hz_ in (("#ecd3a4", 0.9, -900, WL, "#c9cee2"), ("#f0d6ac", 1.0, WR, 900, "#f0e6d0")):
        m = band(xg, lo_, hi_, 1 / kg) * band(yg, SWH, L3["h"], 1 / kg)
        over(pic, far(lit(tone_, s_), L3["z0"], hz_, 5200.0, 0.8), m)
        built.append(m)

    # ================= the left side: the house beyond the corner house
    m2 = band(zl, L2["z0"], L2["z1"], dzl) * band(yl, SWH, L2["h"], 1 / kl) * okl
    local = plaster(zl, yl, "#f0dcb4", seed + 41, 0.09, 0.05)
    over(local, plaster(zl, yl, RED, seed + 42, 0.10, 0.06), band(yl, SWH, 128, 1 / kl))
    sunl = sun_left(zl, yl, (wn(zl, yl, 90, seed + 43, 2) - 0.5) * 8)
    over(pic, far(light(local, sunl, "front"), zl, "#c4c8dc", 5200.0, 0.8), m2)
    built.append(m2)
    info.update(m2=m2, sun_l2=sunl)

    # ================= the right side, all in shade: three houses in a row
    for B, s in ((RC, 57), (RB, 54), (RA, 51)):
        mr = band(zr, B["z0"], B["z1"], dzr) * band(yr, SWH, B["h"], 1 / kr) * okr
        if B is RA:                                                                                 # ochre above a whitewashed band and a dark red dado
            local = plaster(zr, yr, "#e8c68e", seed + s, 0.12, 0.07, mend=0.3)
            over(local, plaster(zr, yr, CREAM, seed + s + 1, 0.10, 0.06, mend=0.2), band(yr, 118, 346, 1 / kr))
            over(local, plaster(zr, yr, DADO, seed + s + 2, 0.14, 0.06), band(yr, SWH, 118, 1 / kr))
            patch = np.maximum(bare(zr, yr, seed + s + 3, 0.52) * band(yr, SWH, 300, 40.0), bare(zr, yr, seed + s + 8, 0.36, 170.0) * band(yr, 380, 900, 60.0))
            over(local, brickwork(zr, yr, seed + s + 4, 1 / kr), patch)
            info["patch_r"] = patch * mr
        elif B is RB:                                                                               # Pompeian red above pale shop fronts
            local = plaster(zr, yr, RED, seed + s, 0.10, 0.06)
            over(local, plaster(zr, yr, "#e9d6b4", seed + s + 1, 0.08, 0.05), band(yr, SWH, 352, 1 / kr))
            over(local, plaster(zr, yr, "#5a4a52", seed + s + 2, 0.12, 0.06), band(yr, SWH, 80, 1 / kr))
        else:
            local = plaster(zr, yr, "#eedcb8", seed + s, 0.08, 0.05)
            over(local, plaster(zr, yr, RED, seed + s + 2, 0.12, 0.06), band(yr, SWH, 120, 1 / kr))
        damp = np.clip(1 - (yr - SWH) / 70.0, 0, 1) * (0.4 + 0.6 * wn(zr, yr, 70, seed + s + 5, 3))     # splashes and damp along the foot
        local *= (1 - damp * 0.25)[..., None]
        for fl in (350.0, 650.0, 950.0):
            local *= (1 - np.clip(1 - np.abs(yr - fl + 14) / 30.0, 0, 1) * 0.10)[..., None]             # grime under each floor line
        shade = in_shade(local, "warm")
        up = smooth((yr - 90) / 560.0)[..., None]                                                       # the wall is cool and dark at its foot, and higher up
        shade = shade * lerp(np.array((0.80, 0.84, 1.02), dtype=F32), np.array((1.20, 1.00, 0.86), dtype=F32), up)   # it takes warm light from the sunny side opposite
        shade *= (1 - np.clip(1 - (yr - SWH) / 46.0, 0, 1) * 0.14)[..., None]
        shade *= (0.86 + 0.14 * np.clip((zr + 60) / 500.0, 0, 1))[..., None]                            # and it is deepest close to us
        over(pic, far(shade, zr, "#b4bcd8", 5200.0, 0.8), mr)
        built.append(mr)
        info["m_" + ("RA" if B is RA else "RB" if B is RB else "RC")] = mr

    # ================= the corner house (snack bar): its street wall with the gable, its roof, its front
    gable = L1["h"] + np.clip(300 - np.abs(zl - L1["zr"]), 0, 300) * ((L1["ridge"] - L1["h"]) / 300.0)
    m1 = band(zl, L1["z0"], L1["z1"], dzl) * band(yl, SWH, gable, 1 / kl) * okl
    local = plaster(zl, yl, OCHRE, seed + 61, 0.12, 0.06, mend=0.25)
    over(local, plaster(zl, yl, DADO, seed + 62, 0.12, 0.06), band(yl, SWH, 122, 1 / kl))
    sunl = sun_left(zl, yl, (wn(zl, yl, 80, seed + 63, 2) - 0.5) * 6)
    sunl = sunl * (1 - above(yl, gable - 26, 4.0) * 0.9)                                            # the verge's shadow under the roof's edge
    over(pic, far(light(local, sunl, "front"), zl, "#c4c8dc", 5200.0, 0.8), m1)
    info.update(m1=m1, sun_l1=sunl)
    built.append(m1)

    # the roof slope that faces us: rows of curved tiles in the sun
    b = (L1["ridge"] - (L1["h"] - 5)) / (L1["zr"] - (ZF - 40))
    a = (L1["h"] - 5) - (ZF - 40) * b
    xt, zt, kt, okt = slope(a, b)
    mroof = band(zt, ZF - 40, L1["zr"], 2.0 / kt) * above(WL + 40 - xt, 0, 1 / kt) * okt
    tiles = np.empty(shape + (3,), dtype=F32)
    tiles[...] = col(TILE)
    tiles *= (1 + (wn(xt, zt, 60, seed + 66, 3) - 0.5) * 0.34 + (_hash(np.floor(xt / 46.0), np.floor(zt / 52.0), seed) - 0.5) * 0.16)[..., None]
    ph = xt / 46.0 - np.floor(xt / 46.0)
    tiles *= (0.86 + 0.26 * np.clip(1 - np.abs(ph - 0.55) / 0.22, 0, 1) - 0.20 * np.clip(1 - np.abs(ph - 0.25) / 0.14, 0, 1))[..., None]    # each curved tile: a lit back, a shaded side
    over(pic, light(tiles, np.ones(shape, dtype=F32), "up"), mroof)
    built.append(mroof)
    info.update(roof=(xt, zt, kt, mroof, a, b))

    # the front wall, facing us
    xw, yw, kw = wall_z(ZF)
    mf = band(xw, -2000, WL, 1 / kw) * band(yw, SWH, L1["h"], 1 / kw)
    local = plaster(xw, yw, OCHRE, seed + 71, 0.13, 0.07, mend=0.25)
    white = band(yw, 356, 446, 1 / kw) * band(xw, -640, -262, 1 / kw)
    over(local, plaster(xw, yw, CREAM, seed + 72, 0.07, 0.05), white * (0.80 + 0.2 * wn(xw, yw, 30, seed + 75, 3)))      # the whitewashed band the notices are painted on
    over(local, plaster(xw, yw, DADO, seed + 73, 0.12, 0.06), band(yw, SWH, 124, 1 / kw))
    quoin = bare(xw, yw, seed + 76, 0.55, 90.0) * band(xw, -330, WL, 14.0) * band(yw, SWH, 300, 30.0)                    # the corner pier has lost plaster low down
    quoin = np.maximum(quoin, bare(xw, yw, seed + 78, 0.40, 150.0) * band(yw, 470, 640, 40.0) * band(xw, -700, -500, 30.0))     # and there is a bare place high on the left
    over(local, brickwork(xw, yw, seed + 77, 1 / kw), quoin)
    info["quoin"] = quoin * mf
    local *= (1 - np.clip(1 - np.abs(yw - 336) / 26.0, 0, 1) * 0.10)[..., None]
    edge = shadow_edge_front(xw) + (wn(xw, yw, 70, seed + 74, 2) - 0.5) * 7
    sun = above(yw, edge, 8.0)
    sun = sun * (1 - above(yw, L1["h"] - 34, 4.0) * 0.92)                                           # the eave's own shadow along the top of the wall
    front = light(local, sun, "front")
    fringe = (sun * (1 - sun) * 4)[..., None]
    front = front * (1 + fringe * np.array((0.10, 0.02, -0.08), dtype=F32))                            # the edge of a shadow is a little warm
    low = smooth((yw - 60) / 330.0)[..., None]
    front = lerp(front, front * lerp(np.array((0.84, 0.88, 1.04), dtype=F32), np.array((1.08, 1.0, 0.94), dtype=F32), low), (1 - sun)[..., None])
    front *= (1 - np.clip(1 - (yw - SWH) / 40.0, 0, 1) * 0.12 * (1 - sun))[..., None]
    over(pic, front, mf)
    built.append(mf)
    info.update(xw=xw, yw=yw, kw=kw, mf=mf, sun_front=sun, built=np.clip(np.max(np.stack(built), axis=0), 0, 1),
                walls=np.clip(np.max(np.stack(built[1:]), axis=0), 0, 1))

    # the shop: we look in through the opening at its floor, back wall and left wall
    shop_inside(pic, info, seed)
    return pic


def shop_inside(pic, info, seed):
    """The snack bar's room, seen through its street opening: all of it in deep shade."""
    shape = SHAPE
    xw, yw, kw = info["xw"], info["yw"], info["kw"]
    opening = band(xw, SHOP["x0"], SHOP["x1"], 1 / kw) * band(yw, SWH, SHOP["top"], 1 / kw)
    xs, zs, ks, oks = level(SWH)
    xb, yb, kb = wall_z(SHOP["back"])
    zl, yl, kl2, okl = wall_x(SHOP["x0"])
    floor_hit = (zs < SHOP["back"]) & (xs > SHOP["x0"])
    back_hit = (~floor_hit) & (xb > SHOP["x0"])
    room = np.empty(shape + (3,), dtype=F32)
    wall_c = plaster(xb, yb, "#dcc49c", seed + 81, 0.10, 0.06)
    over(wall_c, plaster(xb, yb, RED, seed + 82, 0.10, 0.06), band(yb, SWH, 118, 1 / kb))
    side_c = plaster(zl, yl, "#dcc49c", seed + 83, 0.10, 0.06)
    over(side_c, plaster(zl, yl, RED, seed + 84, 0.10, 0.06), band(yl, SWH, 118, 1 / kl2))
    floor_c = vary("#b79f86", shape, seed + 85, 0.08, 20)
    deep_b = in_shade(wall_c, "deep") * (1.15 + np.clip((yb - 40) / 300.0, 0, 1)[..., None] * 0.25)
    deep_s = in_shade(side_c, "deep") * (1.45 - np.clip((zl - ZF) / 260.0, 0, 1)[..., None] * 0.4)    # the wall is lighter near the street
    deep_f = in_shade(floor_c, "deep") * (1.7 - np.clip((zs - ZF) / 240.0, 0, 1)[..., None] * 0.6)
    room[...] = deep_s
    room[back_hit] = deep_b[back_hit]
    room[floor_hit] = deep_f[floor_hit]
    over(pic, room, opening)
    info["opening"] = opening
    return pic


# ================================================================ built things, drawn in the world
def window_side(b, l, X, z0, z1, y0, y1, wood=GREENW, sun=0.0, shut=False, leaf=True, kind="warm", fine=True, haze=0.0):
    """A window in a wall that runs away from us: the dark room, its sill, and wooden shutters, one of them
    standing open at right angles to the wall (so we see its face)."""
    out = -1.0 if X > 0 else 1.0

    def c(local, s=sun, k=kind, dim=1.0):
        v = lit(local, s, k) * dim
        return lerp(v, col("#b9c2dc"), haze) if haze else v
    wl = (z1 - z0) / 2
    if shut:
        b.side(X + out * 2, z0, z1, y0, y1, c(wood))
        if fine:
            l.line([(X + out * 2, y0, (z0 + z1) / 2), (X + out * 2, y1, (z0 + z1) / 2)], c(wood, dim=0.55), 0.8, 0.9)
            for i in range(1, int((y1 - y0) / 11)):
                yy = y0 + i * 11
                l.line([(X + out * 2, yy, z0 + 2), (X + out * 2, yy, z1 - 2)], c(wood, dim=0.66), 0.6, 0.55)
    else:
        b.side(X, z0, z1, y0, y1, c(ROOM, 0, "deep"))
        b.poly([(X, y0, z1), (X - out * 12, y0, z1), (X - out * 12, y1, z1), (X, y1, z1)], c("#d8c4a0", sun * 0.5, "front", 0.9))     # the far jamb
        if leaf:
            b.poly([(X, y0 + 2, z1 + 1), (X + out * wl, y0 + 2, z1 + 1), (X + out * wl, y1 - 2, z1 + 1), (X, y1 - 2, z1 + 1)], c(wood, sun, "front"))
            b.side(X + out * 3, z0 - wl, z0 - 1, y0 + 2, y1 - 2, c(wood, sun, kind, 0.94))
            if fine:
                for i in range(1, int((y1 - y0) / 11)):
                    yy = y0 + i * 11
                    l.line([(X + out * 3, yy, z1 + 1), (X + out * (wl - 3), yy, z1 + 1)], c(wood, sun, "front", 0.66), 0.6, 0.6)
                    l.line([(X + out * 3, yy, z0 - wl + 2), (X + out * 3, yy, z0 - 3)], c(wood, sun, kind, 0.66), 0.6, 0.5)
                l.line([(X + out * wl, y0 + 2, z1 + 1), (X + out * wl, y1 - 2, z1 + 1)], c(wood, sun, "front", 1.25), 0.7, 0.7)
    b.side(X + out * 8, z0 - 7, z1 + 7, y0 - 9, y0, c(STONE, sun))                                    # the sill
    b.poly([(X, y0 - 9, z0 - 7), (X + out * 8, y0 - 9, z0 - 7), (X + out * 8, y0, z0 - 7), (X, y0, z0 - 7)], c(STONE, sun, "front", 0.9))
    if fine:
        l.line([(X + out * 8, y0, z0 - 7), (X + out * 8, y0, z1 + 7)], c(STONE, sun, kind, 1.2), 0.7, 0.7)
        l.line([(X + out * 1, y0 - 10, z0 - 7), (X + out * 1, y0 - 10, z1 + 7)], c("#4a3a44", 0, "deep"), 0.9, 0.6)   # the shade under it
    return


def door_side(b, l, X, z0, z1, y1, wood=WOOD, kind="warm", ajar=True, fine=True, haze=0.0, step_up=True):
    """A street door in a wall that runs away from us: a dark way in, a plank leaf, a stone step."""
    out = -1.0 if X > 0 else 1.0

    def c(local, k=kind, dim=1.0):
        v = in_shade(local, k) * dim
        return lerp(v, col("#b9c2dc"), haze) if haze else v
    b.side(X, z0, z1, SWH, y1, c(ROOM, "deep"))
    b.poly([(X, SWH, z1), (X - out * 22, SWH, z1), (X - out * 22, y1, z1), (X, y1, z1)], c("#cdb894", "front", 0.8))       # the far jamb
    if ajar:
        b.poly([(X - out * 4, SWH, z1 - 2), (X - out * 50, SWH, z1 - 30), (X - out * 50, y1 - 3, z1 - 30), (X - out * 4, y1 - 3, z1 - 2)], c(wood, "deep", 1.5))
    else:
        b.side(X - out * 4, z0, z1, SWH, y1, c(wood, kind, 0.9))
        if fine:
            for i in range(1, 4):
                zz = lerp(z0, z1, i / 4)
                l.line([(X - out * 4, SWH, zz), (X - out * 4, y1, zz)], c(wood, kind, 0.6), 0.7, 0.7)
    b.side(X + out * 3, z0 - 12, z0, SWH, y1 + 14, c("#e2d2b4", kind, 0.95))                           # painted door posts and lintel
    b.side(X + out * 3, z1, z1 + 12, SWH, y1 + 14, c("#e2d2b4", kind, 0.95))
    b.side(X + out * 3, z0 - 12, z1 + 12, y1, y1 + 14, c("#e2d2b4", kind, 1.0))
    if step_up:
        b.box(min(X, X + out * 26), max(X, X + out * 26), SWH, SWH + 14, z0 - 6, z1 + 6, STONE)
    return


def far_dressing(b, l, seed):
    """Doors, windows and awnings down the far part of the street: small, plain, pale."""
    woods = (GREENW, BLUEW, WOOD, "#a4563c", "#7a8a5a")
    # the low house beyond the block, on the right
    for i, z0 in enumerate((1740.0, 2020.0, 2330.0, 2650.0)):
        window_side(b, l, WR, z0, z0 + 90, 440, 570, wood=woods[i % 5], shut=i % 2 == 0, fine=False, haze=0.16)
    door_side(b, l, WR, 1890.0, 1990.0, 235.0, fine=False, haze=0.16, step_up=False)
    door_side(b, l, WR, 2460.0, 2570.0, 235.0, fine=False, haze=0.2, step_up=False, ajar=False)
    b.poly([(WR, 330, 2180), (WR - 120, 290, 2180), (WR - 120, 290, 2330), (WR, 330, 2330)], lerp(in_shade("#5f86b8", "up"), col("#b9c2dc"), 0.2))    # a blue awning
    b.poly([(WR - 120, 290, 2180), (WR - 120, 268, 2180), (WR - 120, 268, 2330), (WR - 120, 290, 2330)], lerp(in_shade("#4f74a4", "warm"), col("#b9c2dc"), 0.2))
    # the long house on the left
    for i, z0 in enumerate((1060.0, 1420.0, 1800.0, 2200.0, 2600.0)):
        sun = 1.0 if (z0 < 1300 or z0 > 2330) else 0.0
        window_side(b, l, WL, z0, z0 + 95, 440, 575, wood=woods[(i + 2) % 5], sun=sun, shut=i % 3 == 1, kind="front", fine=z0 < 1300, haze=0.06 + 0.05 * i)
    door_side(b, l, WL, 1210.0, 1320.0, 240.0, kind="front", fine=False, haze=0.08, step_up=False)
    door_side(b, l, WL, 1960.0, 2060.0, 240.0, kind="front", fine=False, haze=0.16, step_up=False, ajar=False)
    b.poly([(WL, 345, 1560), (WL + 130, 300, 1560), (WL + 130, 300, 1740), (WL, 345, 1740)], lerp(in_shade("#c9573c", "up"), col("#b9c2dc"), 0.12))    # a red awning over a shop
    b.poly([(WL + 130, 300, 1560), (WL + 130, 276, 1560), (WL + 130, 276, 1740), (WL + 130, 300, 1740)], lerp(in_shade("#a8452f", "front"), col("#b9c2dc"), 0.12))
    b.side(WL, 1575, 1725, SWH, 270, lerp(in_shade(ROOM, "deep"), col("#b9c2dc"), 0.12))
    # the last houses before the square: only dabs
    for B, X in ((L3, WL), (R3, WR)):
        for z0 in (3600.0, 4200.0, 4900.0, 5500.0):
            b.side(X, z0, z0 + 120, 450, 590, lerp(in_shade(ROOM, "deep"), col("#c9cee2"), 0.42))
            b.side(X, z0 + 300, z0 + 420, SWH, 240, lerp(in_shade(ROOM, "deep"), col("#c9cee2"), 0.46))
    # a few people out in the sun of the square: dabs of a few pixels, each with its shadow
    for (px, pz, tone) in ((80, 10500, "#f6ead2"), (-150, 12000, "#e8c8a8"), (30, 13500, "#f4e6cc"), (-60, 16000, "#f0dcc0"), (210, 11500, "#d8a488"), (-260, 14500, "#f6ead2")):
        k = kz(pz)
        cx, cy = P(px, 0, pz)
        l.s.line([(cx, cy), (cx - 150 * k * 1.2, cy - 0.5)], "#b8a8a8", max(0.8, 26 * k), 0.5)
        l.s.line([(cx, cy), (cx, cy - 140 * k)], in_sun(tone), max(1.0, 46 * k), 0.95)
        l.s.ellipse(cx, cy - 156 * k, max(0.7, 12 * k), max(0.7, 13 * k), in_sun("#b88a6a"), 0.95)
    return


def block_things(b, l, seed):
    """The apartment block (four floors): shop fronts shut with boards under a tiled pent roof, rows of
    shuttered windows, a balcony high up."""
    woods = (GREENW, WOOD, BLUEW, "#a4563c")
    # shop fronts: wide openings closed with upright boards
    for i, (z0, z1) in enumerate(((770.0, 990.0), (1080.0, 1300.0), (1390.0, 1600.0))):
        if i == 1:
            b.side(WR, z0, z1, SWH, 292, in_shade(ROOM, "deep") * 1.1)                                # this one is open: a dark shop
            b.poly([(WR, SWH, z1), (WR + 26, SWH, z1), (WR + 26, 292, z1), (WR, 292, z1)], in_shade("#cdb894", "front") * 0.75)
            b.box(WR - 2, WR + 60, SWH, SWH + 78, z0 + 20, z0 + 150, "#b8a48a", dim=0.7)            # a counter inside
        else:
            b.side(WR - 3, z0, z1, SWH, 292, in_shade(WOOD, "warm") * 0.92)
            n = 8
            for j in range(1, n):
                zz = lerp(z0, z1, j / n)
                l.line([(WR - 3, SWH, zz), (WR - 3, 292, zz)], in_shade(WOODD, "warm"), 0.7, 0.75)
        b.side(WR - 4, z0 - 14, z1 + 14, 292, 312, in_shade("#8a6a4a", "warm"))                       # the lintel beam
    # the pent roof over them: we see down onto its tiles
    b.poly([(WR, 372, 742), (WR - 86, 330, 742), (WR - 86, 330, 1630), (WR, 372, 1630)], in_shade(TILE, "up") * 1.05)
    b.poly([(WR - 86, 330, 742), (WR - 86, 320, 742), (WR - 86, 320, 1630), (WR - 86, 330, 1630)], in_shade(TILE, "warm") * 0.8)
    b.poly([(WR, 372, 742), (WR - 86, 330, 742), (WR - 86, 320, 742), (WR, 356, 742)], in_shade(WOODD, "front") * 1.2)    # its near end: rafters
    for j in range(0, 21):
        zz = 742 + j * 44.4
        l.line([(WR, 372, zz), (WR - 86, 330, zz)], in_shade(TILE, "up") * (1.3 if j % 2 else 0.74), 0.7, 0.7)
    for j, zz in enumerate((742.0, 1040.0, 1340.0, 1630.0)):                                         # struts holding it
        l.line([(WR, 250, zz), (WR - 80, 322, zz)], in_shade(WOODD, "warm") * 1.1, 1.3)
    # windows, three floors of them
    for f, (y0, y1) in enumerate(((452.0, 585.0), (752.0, 885.0), (1052.0, 1185.0))):
        for i, z0 in enumerate((800.0, 1010.0, 1225.0, 1440.0)):
            if f == 1 and i in (1, 2):
                continue
            window_side(b, l, WR, z0, z0 + 92, y0, y1, wood=woods[(i + f) % 4], shut=(i + f) % 3 == 0, leaf=(i + 2 * f) % 4 != 1, fine=True, haze=0.04 * i)
    # a balcony on the second floor, with a rail of crossed laths
    x0 = WR - 92
    za, zb, fy = 985.0, 1345.0, 652.0
    for zz in (za + 10, (za + zb) / 2, zb - 10):
        l.line([(WR, fy - 90, zz), (x0 + 6, fy - 12, zz)], in_shade(WOODD, "warm") * 1.15, 1.4)      # struts under it
    b.poly([(WR, fy - 12, za), (x0, fy - 12, za), (x0, fy - 12, zb), (WR, fy - 12, zb)], in_shade(WOODD, "deep") * 1.5)    # its underside
    b.side(x0, za, zb, fy - 14, fy + 4, in_shade(WOOD, "warm") * 0.95)
    b.front(x0, WR, fy - 14, fy + 4, za, in_shade(WOOD, "front") * 0.9)
    b.side(WR, za + 60, za + 150, fy, fy + 200, in_shade(ROOM, "deep"))                              # the doors onto it
    b.side(WR, zb - 150, zb - 60, fy, fy + 200, in_shade(ROOM, "deep"))
    lattice(b, l, [(x0, za), (x0, zb)], fy + 4, fy + 96, in_shade(WOOD, "warm") * 1.05, step=30.0, wd=0.7)
    lattice(b, l, [(x0, za), (WR, za)], fy + 4, fy + 96, in_shade(WOOD, "front") * 1.0, step=30.0, wd=0.7)
    return


def lattice(b, l, ends, y0, y1, tone, step=26.0, wd=0.8, posts=True):
    """A rail of crossed laths between two places (x, z), from height y0 to y1."""
    (xa, za), (xb, zb) = ends
    n = max(2, int(round(math.hypot(xb - xa, zb - za) / step)))

    def at(t, yy):
        return (lerp(xa, xb, t), yy, lerp(za, zb, t))
    for i in range(n):
        l.line([at(i / n, y0), at((i + 1) / n, y1)], tone, wd, 0.9)
        l.line([at(i / n, y1), at((i + 1) / n, y0)], tone * 0.86, wd, 0.9)
    l.line([at(0, y1), at(1, y1)], tone * 1.18, wd * 2.0)
    l.line([at(0, y0), at(1, y0)], tone * 0.9, wd * 1.5)
    if posts:
        l.line([at(0, y0), at(0, y1)], tone, wd * 1.6)
        l.line([at(1, y0), at(1, y1)], tone, wd * 1.6)
    return


def near_right_things(b, l, seed):
    """The first house on the right, in whose shade we stand: a door, a barred window, the windows above."""
    # the street door, beyond the fountain
    door_side(b, l, WR, 452.0, 556.0, 236.0, wood="#8a5a3a", ajar=True)
    # a small barred window low down
    b.side(WR, 606.0, 664.0, 196, 262, in_shade(ROOM, "deep"))
    b.poly([(WR, 196, 664), (WR + 12, 196, 664), (WR + 12, 262, 664), (WR, 262, 664)], in_shade("#d8c4a0", "front") * 0.8)
    for zz in (620.0, 635.0, 650.0):
        l.line([(WR, 196, zz), (WR, 262, zz)], in_shade("#3a3038", "front"), 0.8)
    # first floor: the window with the cat, right at the edge of the picture; two doors onto the balcony
    window_side(b, l, WR, 38.0, 132.0, 455.0, 590.0, wood=BLUEW, leaf=True)
    for (z0, z1) in ((236.0, 316.0), (392.0, 472.0), (548.0, 628.0)):
        b.side(WR, z0, z1, BALC["floor"], BALC["floor"] + 205, in_shade(ROOM, "deep") * 0.9)
        b.poly([(WR, BALC["floor"], z1), (WR + 12, BALC["floor"], z1), (WR + 12, BALC["floor"] + 205, z1), (WR, BALC["floor"] + 205, z1)], in_shade("#d8c4a0", "deep") * 1.6)
    # second floor: only the feet of its windows come into the picture
    for i, z0 in enumerate((250.0, 440.0, 620.0)):
        window_side(b, l, WR, z0, z0 + 88, 752.0, 885.0, wood=(WOOD, GREENW, WOOD)[i], shut=i == 1)
    # the ends of the floor beams show as a row of dark squares under each floor
    rng = np.random.default_rng(seed + 21)
    for zz in np.arange(-40.0, 715.0, 62.0):
        j, w_, h_, t_ = rng.normal(0, 4), 11 + rng.random() * 5, 13 + rng.random() * 4, 0.8 + rng.random() * 0.3
        if not (BALC["z0"] - 10 < zz < BALC["z1"] + 10):
            b.side(WR - 2, zz + j, zz + j + w_, 331, 331 + h_, in_shade(WOODD, "warm") * t_)
        if rng.random() < 0.9:
            b.side(WR - 2, zz - j, zz - j + w_, 632, 632 + h_, in_shade(WOODD, "warm") * t_)
    return


def balcony(b, l, seed):
    """The timber balcony on the first floor, under its own little roof: the washing lines are tied to its posts."""
    X, za, zb = BALC["x"], BALC["z0"], BALC["z1"]
    fy, ry, ty = BALC["floor"], BALC["rail"], BALC["top"]
    wood, dark = in_shade("#a07048", "warm"), in_shade(WOODD, "warm")
    # the roof, seen from underneath, and its edge of tiles
    b.poly([(WR, ty + 52, za - 16), (X - 22, ty + 2, za - 16), (X - 22, ty + 2, zb + 16), (WR, ty + 52, zb + 16)], in_shade("#7a5a44", "deep") * 1.35)
    for zz in np.arange(za - 10, zb + 16, 38.0):
        l.line([(WR, ty + 50, zz), (X - 20, ty + 2, zz)], in_shade(WOODD, "deep") * 1.0, 1.0, 0.8)          # rafters
    b.side(X - 22, za - 16, zb + 16, ty + 1, ty + 12, in_shade(TILE, "warm") * 0.95)
    b.poly([(WR, ty + 52, za - 16), (X - 22, ty + 2, za - 16), (X - 22, ty + 12, za - 16), (WR, ty + 62, za - 16)], in_shade(TILE, "front") * 0.9)
    for zz in np.arange(za - 16, zb + 16, 22.0):
        l.line([(X - 22, ty + 2, zz), (X - 22, ty + 12, zz)], in_shade(TILE, "warm") * 0.6, 0.7, 0.7)       # the ends of the tiles
    l.line([(X - 22, ty + 12, za - 16), (X - 22, ty + 12, zb + 16)], in_sun("#f6a468"), 1.3, 0.95)       # the roof's edge stands just clear of the shadow, and takes the sun
    # struts from the wall under the floor
    for zz in BALC["posts"]:
        l.line([(WR, fy - 104, zz + 4), (X + 4, fy - 14, zz + 4)], dark * 1.15, 2.2)
        l.line([(WR, fy - 104, zz + 4), (X + 4, fy - 12, zz + 4)], wood * 0.9, 0.8, 0.7)
    # the floor: its edge beam, and the planks, which we look along
    b.flat(X - 8, WR, za - 8, zb + 8, fy, in_shade("#a8845c", "up") * 0.8)
    b.side(X - 8, za - 8, zb + 8, fy - 18, fy, wood * 0.95)
    b.front(X - 8, WR, fy - 18, fy, za - 8, in_shade("#a07048", "front") * 0.95)
    l.line([(X - 8, fy, za - 8), (X - 8, fy, zb + 8)], wood * 1.3, 0.8, 0.8)
    for zz in np.arange(za + 30, zb, 76.0):
        b.side(X - 9, zz, zz + 12, fy - 17, fy - 4, dark * 0.9)                                             # beam ends
    # rails of crossed laths: the far end, the long side bay by bay, the near end
    posts = BALC["posts"]
    lattice(b, l, [(X, zb), (WR, zb)], fy + 18, ry, in_shade("#a07048", "front") * 0.8, wd=0.7)
    for i in range(len(posts) - 1, 0, -1):
        lattice(b, l, [(X, posts[i - 1]), (X, posts[i])], fy + 18, ry, np.clip(wood * 1.3, 0, 1), step=25.0, wd=1.1, posts=False)
    lattice(b, l, [(X, za), (WR, za)], fy + 18, ry, np.clip(in_shade("#b8875a", "front") * 1.25, 0, 1), step=25.0, wd=1.1, posts=False)
    # the timbers themselves: rails, the roof beam, and the posts, far to near
    local = "#a8784e"
    b.box(X - 5, X + 5, ry - 7, ry + 3, za, zb, local)
    b.box(X - 4, X + 4, fy + 12, fy + 19, za, zb, local, dim=0.9)
    b.front(X, WR, ry - 7, ry + 3, za, in_shade(local, "front") * 1.05)
    b.front(X, WR, fy + 12, fy + 19, za, in_shade(local, "front") * 0.95)
    b.box(X - 7, X + 7, ty - 6, ty + 8, za - 12, zb + 12, local, dim=0.88)
    for zz in reversed(posts):
        b.box(X - 6, X + 6, fy, ty - 6, zz - 6, zz + 6, local, dim=0.95)
        l.line([(X - 6, fy, zz - 6), (X - 6, ty - 6, zz - 6)], np.clip(wood * 1.4, 0, 1), 0.8, 0.8)             # the edge that looks at the sunny wall
        l.line([(X, ty - 44, zz + 6), (X, ty - 6, zz + 40)], dark * 1.1, 1.6)                                   # a brace up to the beam
    b.box(WR - 8, WR, fy, ty + 40, za - 6, za + 6, local, dim=0.8)                                           # the post against the wall
    l.line([(X - 5, ry + 3, za), (X - 5, ry + 3, zb)], np.clip(in_shade("#d8ac7a", "up") * 1.3, 0, 1), 0.8, 0.8)   # the sky along the top of the rail
    return


def left_street_things(b, l, cast, seed):
    """The corner house's wall along the main street: a window above with its shutter standing open in the
    sun, a street door, a little window, hooks for the washing lines."""
    window_side(b, l, WL, 452.0, 548.0, 452.0, 584.0, wood=GREENW, sun=1.0, kind="front", leaf=True)
    # the open shutter's shadow on the wall beyond it
    wl = 48.0
    dz, dy = wl * SUN_Z, wl * SUN_T
    cast.poly([(WL, 454, 549), (WL, 582, 549), (WL, 582 - dy, 549 + dz), (WL, 454 - dy, 549 + dz)], "#ffffff")
    cast.poly([(WL, 443, 445), (WL, 452, 445), (WL, 452 - 7, 560), (WL, 443 - 7, 560)], "#ffffff")
    window_side(b, l, WL, 742.0, 828.0, 452.0, 584.0, wood="#a4563c", sun=1.0, kind="front", shut=True)
    door_side(b, l, WL, 612.0, 706.0, 232.0, wood="#7a5238", kind="front", ajar=False)
    # a small pent of tiles over the door
    b.poly([(WL, 292, 592), (WL + 66, 262, 592), (WL + 66, 262, 726), (WL, 292, 726)], in_shade(TILE, "up") * 1.05)
    b.poly([(WL + 66, 262, 592), (WL + 66, 254, 592), (WL + 66, 254, 726), (WL + 66, 262, 726)], in_shade(TILE, "front") * 0.8)
    b.poly([(WL, 292, 592), (WL + 66, 262, 592), (WL + 66, 254, 592), (WL, 280, 592)], in_shade(WOODD, "front") * 1.1)
    # the far verge of the roof, seen from underneath against the sky
    b.poly([(WL, 766, 630), (WL + 40, 766, 630), (WL + 40, 635, 972), (WL, 640, 930)], in_shade(WOODD, "deep") * 1.6)
    b.poly([(WL, 640, ZF), (WL, 766, 630), (WL + 40, 766, 630), (WL + 40, 635, ZF - 40)], in_shade(WOODD, "deep") * 1.9)
    l.line([(WL + 40, 635, ZF - 40), (WL + 40, 766, 630), (WL + 40, 635, 972)], lit(TILE, 1.0, "up"), 1.3)
    # a round vent in the gable
    cx, cy = P(WL, 690, 630)
    b.s.ellipse(cx, cy, 2.2, 5.0, in_shade(ROOM, "deep"))
    return


def front_wall_things(b, l, cast, seed):
    """The corner house's front: the upstairs window with its shutters back against the wall and a rug over the
    sill, the timber over the shop, the ends of the floor beams, the rafters under the eave."""
    z = ZF
    sx, sy = -LIGHT[0] / LIGHT[2], -LIGHT[1] / LIGHT[2]            # a thing standing 1 cm off this wall throws its shadow this far left and down

    def shadow(x0, x1, y0, y1, off):
        cast.poly([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x1 - sx * off, y1 - sy * off, z), (x1 - sx * off, y0 - sy * off, z), (x0 - sx * off, y0 - sy * off, z), (x0 - sx * off, y1 - sy * off, z), (x0, y1, z)], "#ffffff")

    x0, x1, y0, y1 = -474.0, -382.0, 452.0, 584.0
    sunny = 1.0
    b.front(x0, x1, y0, y1, z, in_shade(ROOM, "deep") * 1.1)
    b.poly([(x0, y0, z), (x0, y0, z + 24), (x0, y1, z + 24), (x0, y1, z)], lit("#ecd2a4", sunny, "front"))                      # the left cheek of the opening takes the sun
    b.poly([(x0, y1, z), (x1, y1, z), (x1, y1, z + 24), (x0, y1, z + 24)], in_shade("#ecd2a4", "front") * 0.8)                  # under its lintel
    wl = (x1 - x0) / 2
    for (a0, a1) in ((x0 - wl - 3, x0 - 3), (x1 + 3, x1 + wl + 3)):
        shadow(a0, a1, y0 + 1, y1 - 1, 4.0)
        b.front(a0, a1, y0 + 1, y1 - 1, z - 4, lit(GREENW, sunny, "front"))
        for i in range(1, 12):
            yy = y0 + 1 + i * 11
            l.line([(a0 + 3, yy, z - 4), (a1 - 3, yy, z - 4)], lit(GREENW, sunny, "front") * 0.70, 0.7, 0.7)
            l.line([(a0 + 3, yy - 1.6, z - 4), (a1 - 3, yy - 1.6, z - 4)], np.clip(lit(GREENW, sunny, "front") * 1.2, 0, 1), 0.6, 0.5)
        l.line([(a0, y0 + 1, z - 4), (a0, y1 - 1, z - 4), (a1, y1 - 1, z - 4), (a1, y0 + 1, z - 4), (a0, y0 + 1, z - 4)], lit(GREENW, sunny, "front") * 0.6, 0.8, 0.8)
    shadow(x0 - 10, x1 + 10, y0 - 10, y0, 10.0)
    b.front(x0 - 10, x1 + 10, y0 - 10, y0, z - 10, lit(STONE, sunny, "front"))                                                   # the sill
    b.poly([(x0 - 10, y0 - 10, z - 10), (x1 + 10, y0 - 10, z - 10), (x1 + 10, y0 - 10, z), (x0 - 10, y0 - 10, z)], in_shade(STONE, "front") * 0.8)
    # a striped rug airing over the sill
    ra, rb, rl = x0 + 14.0, x1 - 20.0, 36.0
    shadow(ra, rb, y0 - rl, y0 - 8, 11.0)
    stripes = ("#b8402e", "#e8d9b0", "#3f6a9a", "#e8d9b0", "#b8402e", "#d9a13c", "#b8402e")
    for i, tone in enumerate(stripes):
        ya, yb = y0 + 3 - rl * i / len(stripes), y0 + 3 - rl * (i + 1) / len(stripes)
        b.front(ra, rb, yb, ya, z - 11, lit(tone, sunny, "front"))
    for xx in np.arange(ra + 2, rb, 5.0):
        l.line([(xx, y0 + 3 - rl, z - 11), (xx + 0.6, y0 - rl - 5, z - 11)], lit("#e8d9b0", sunny, "front"), 0.6, 0.8)             # its fringe
    # the timber lintel over the shop, and the ends of the floor beams above it
    b.front(-548.0, -292.0, SHOP["top"], SHOP["top"] + 26, z - 2, in_shade("#8a6444", "front") * 0.95)
    l.line([(-548.0, SHOP["top"] + 26, z - 2), (-292.0, SHOP["top"] + 26, z - 2)], in_shade("#8a6444", "front") * 1.3, 0.8, 0.7)
    rng = np.random.default_rng(seed + 22)
    for xx in np.arange(-596.0, -262.0, 56.0):
        j = rng.normal(0, 4)
        b.front(xx + j, xx + j + 12 + rng.random() * 5, 336 + rng.normal(0, 1.2), 351 + rng.normal(0, 1.5), z - 3, in_shade(WOODD, "front") * (0.85 + rng.random() * 0.3))
    # rafter ends under the eave, in its shadow
    for xx in np.arange(-600.0, -250.0, 46.0):
        j = rng.normal(0, 3)
        b.front(xx + j, xx + j + 8 + rng.random() * 4, L1["h"] - 16, L1["h"] - 3, z - 20, in_shade(WOODD, "front") * (1.1 + rng.random() * 0.3))
    # the hook for the low washing line, on the corner pier
    l.line([(WL - 6, 252, z - 1), (WL - 6, 258, z - 5)], in_shade("#3a3038", "front"), 1.2)
    return


def shop_things(b, l, seed):
    """What stands in the snack bar's room: the counter's back arm with its sunk jars, shelves of cups, wine jars
    in the corner, a curtained door to the back."""
    zb = SHOP["back"]
    deep = lambda c, d=1.0: in_shade(c, "deep") * d
    # the door to the back room, and a faded curtain half drawn across it
    b.front(-418.0, -344.0, SWH, 212, zb - 1, deep("#1c141c", 0.9))
    b.poly([(-418, 212, zb - 2), (-384, 212, zb - 2), (-390, 120, zb - 2), (-380, 30, zb - 2), (-418, 26, zb - 2)], deep("#5f86b8", 1.5))
    for xx in (-410.0, -400.0, -392.0):
        l.line([(xx, 208, zb - 2), (xx - 1, 120, zb - 2), (xx + 2, 34, zb - 2)], deep("#3f5f8a", 1.4), 0.7, 0.8)
    l.line([(-420, 214, zb - 2), (-342, 214, zb - 2)], deep("#a07048", 1.8), 1.2)
    # two shelves on the back wall, with cups, jugs and bowls
    for sy in (176.0, 222.0):
        b.front(-512.0, -428.0, sy - 5, sy, zb - 14, deep("#a07048", 2.0))
        l.line([(-512, sy, zb - 14), (-428, sy, zb - 14)], deep("#c89868", 2.4), 0.8, 0.9)
    rng = np.random.default_rng(seed + 5)
    for sy in (176.0, 222.0):
        xx = -508.0
        while xx < -436:
            w = 7 + rng.random() * 6
            h = 8 + rng.random() * 12
            tone = ("#c8744a", "#d9b06a", "#b85a3c", "#9a8a6a", "#c89a5a")[int(rng.integers(5))]
            b.poly([(xx + 1, sy, zb - 16), (xx + w - 1, sy, zb - 16), (xx + w, sy + h * 0.7, zb - 16), (xx + w * 0.7, sy + h, zb - 16), (xx + w * 0.3, sy + h, zb - 16), (xx, sy + h * 0.7, zb - 16)], deep(tone, 2.3))
            l.line([(xx + 1, sy + h * 0.8, zb - 16), (xx + 2, sy + h * 0.3, zb - 16)], deep(tone, 3.4), 0.6, 0.8)
            xx += w + 2 + rng.random() * 4
    # wine jars leaning in the corner
    for (xx, lean) in ((-506.0, 0.10), (-486.0, -0.05)):
        cx, cy = P(xx, SWH, zb - 22)
        amphora(b.s, cx, cy, 122 * kz(zb - 22), lean, tones=(deep("#c8744a", 1.3), deep("#c8744a", 2.0), deep("#e0a070", 2.8)))
    # the back arm of the counter, along the left wall
    c_local = "#d8ccb8"
    cam.box(b.s, ARM["x0"], ARM["x1"], SWH, ARM["top"], ARM["z0"], ARM["z1"], deep(c_local, 1.7), in_shade(c_local, "up") * 0.82, (deep(c_local, 1.6), deep("#b8a48c", 1.9)))
    for zz in (452.0, 512.0):
        jar_mouth(b, l, (ARM["x0"] + ARM["x1"]) / 2, ARM["top"], zz, 22.0, dim=0.8)
    return


def jar_mouth(b, l, x, y, z, r, dim=1.0, lid=False):
    """The mouth of a big jar sunk in the counter's top: a ring of fired clay round a dark well."""
    n = 18
    ring = [(x + math.cos(i / n * 2 * math.pi) * r, y + 0.5, z + math.sin(i / n * 2 * math.pi) * r) for i in range(n)]
    well = [(x + math.cos(i / n * 2 * math.pi) * r * 0.72, y + 0.6, z + math.sin(i / n * 2 * math.pi) * r * 0.72) for i in range(n)]
    b.poly(ring, in_shade("#c8744a", "up") * dim)
    if lid:
        b.poly(well, in_shade("#a07048", "up") * dim)
        l.line([(x - r * 0.5, y + 1, z), (x + r * 0.5, y + 1, z)], in_shade(WOODD, "up") * dim, 0.9)
        l.line([(x - 3, y + 2, z), (x + 3, y + 5, z)], in_shade("#c89868", "up") * dim * 1.3, 1.3)
    else:
        b.poly(well, in_shade("#1c1418", "deep"))
        l.line([(x + math.cos(a) * r * 0.72, y + 0.6, z + math.sin(a) * r * 0.72) for a in np.linspace(0.2, 2.9, 8)], in_shade("#7a3a2a", "deep") * 1.6, 0.8, 0.8)   # inside of the far lip
    l.line([(x + math.cos(a) * r, y + 0.5, z + math.sin(a) * r) for a in np.linspace(3.3, 6.1, 9)], np.clip(in_shade("#e8a070", "up") * dim * 1.25, 0, 1), 0.8, 0.9)        # the near lip catches the sky
    return


def amphora(sheet, cx, base, h, lean=0.0, tones=("#7a4636", "#a8644a", "#d09070"), light=-1):
    """A wine jar in picture measurements: pointed foot at (cx, base), `h` tall, leaning by `lean`. `tones` are
    its dark, middle and light; the light side is the left one when `light` is -1."""
    prof = [(0.0, 0.028), (0.05, 0.05), (0.15, 0.115), (0.32, 0.175), (0.5, 0.20), (0.64, 0.185), (0.74, 0.125), (0.79, 0.066), (0.9, 0.056), (0.97, 0.06), (1.0, 0.076)]
    t0, t1, t2 = (np.asarray(col(t), dtype=F32) for t in tones)

    def at(u, v):                                            # u up the jar (0 to 1), v across (in jar heights)
        return (cx + (v + lean * u) * h, base - u * h)

    def tone(t):
        return lerp(t0, t1, t * 2) if t < 0.5 else lerp(t1, t2, (t - 0.5) * 2)
    for side in (-1, 1):                                    # handles first: they stand out behind the neck
        sheet.line([at(0.93, side * 0.058), at(0.955, side * 0.135), at(0.86, side * 0.16), at(0.745, side * 0.125)], tone(0.55 if side * light > 0 else 0.15), max(1.4, h * 0.036))
    for (a, b, t) in ((-1.0, -0.74, 0.50), (-0.74, -0.30, 0.95), (-0.30, 0.22, 0.66), (0.22, 0.66, 0.36), (0.66, 1.0, 0.12)):       # round: strips of tone from the lit side to the dark
        if light > 0:
            a, b = -b, -a
        sheet.poly([at(u, v * a) for u, v in prof] + [at(u, v * b) for u, v in reversed(prof)], tone(t))
    sheet.line([at(u, light * v * 0.52) for u, v in prof[3:7]], np.clip(t2 * 1.12, 0, 1), max(0.9, h * 0.02), 0.85)        # the sky, down its shoulder
    for u in (0.30, 0.42, 0.56):                                                                                          # faint turning rings
        v = np.interp(u, [q[0] for q in prof], [q[1] for q in prof])
        sheet.line([at(u, -v * 0.96), at(u - 0.006, 0), at(u, v * 0.96)], t0, max(0.6, h * 0.008), 0.35)
    sheet.line([at(1.0, -0.08), at(1.0, 0.08)], t2, max(1.2, h * 0.034))
    sheet.line([at(0.985, -0.07), at(0.985, 0.07)], t0, max(0.7, h * 0.012), 0.8)
    return sheet


def street_things(b, l, seed):
    """Three stepping stones across the roadway (worn round, a little higher than the sidewalks). They are
    drawn on both sheets, so that they come through the brushwork whole."""
    for i, (xa, xb) in enumerate(STONES):
        local = ("#b4aeb2", "#a8a2aa", "#b8b0b4")[i]
        za, zb, hgt = STONE_Z[0] + STONE_OWN[i][0], STONE_Z[1] + STONE_OWN[i][1], STONE_H + STONE_OWN[i][2]
        top_c, front_c = np.clip(in_shade(local, "up") * 1.22, 0, 1), in_shade(local, "front") * 0.74
        for d in (b, l):
            d.poly([(xa - 8, 0, za - 10), (xb + 10, 0, za - 10), (xb + 16, 0, zb + 5), (xa - 3, 0, zb + 5)], in_shade("#2a2430", "deep"), 0.6)     # it sits in its own dark
            cam.box(d.s, xa, xb, 0, hgt - 3, za, zb, front_c, top_c, (in_shade(local, "warm") * 0.95, in_shade(local, "front") * 0.6))
            top = [(xa + 6, hgt, za), (xb - 6, hgt, za), (xb, hgt - 3, za + 5), (xb, hgt - 3, zb - 5), (xb - 6, hgt, zb), (xa + 6, hgt, zb), (xa, hgt - 3, zb - 5), (xa, hgt - 3, za + 5)]
            d.poly(top, top_c)
            d.poly([(xa + 5, hgt, za), (xb - 5, hgt, za), (xb, hgt - 4, za - 0.5), (xa, hgt - 4, za - 0.5)], in_shade(local, "front") * 1.0)     # its worn front edge
        l.line([(xa + 6, hgt, za), (xb - 6, hgt, za)], np.clip(in_shade(local, "up") * 1.5, 0, 1), 0.9, 0.8)
        l.line([(xa, 0, za), (xb, 0, za)], in_shade("#201a28", "deep"), 1.2, 0.9)
        mx = (xa + xb) / 2
        l.poly([(mx - 14, hgt, za + 16), (mx + 12, hgt, za + 13), (mx + 16, hgt, zb - 20), (mx - 10, hgt, zb - 16)], np.clip(lerp(top_c, col("#b4c4f0"), 0.5) * 1.06, 0, 1), 0.35)   # polished where feet land
        l.line([(xa + 9, hgt - 9, za - 0.6), (xa + 16, hgt - 15, za - 0.6), (xa + 14, hgt - 21, za - 0.6)], in_shade("#201a28", "deep") * 1.5, 0.7, 0.7)   # a chip
    return


def loose_things(b, l, seed):
    """Things left standing about: a stool by the snack bar, a broom by the door opposite."""
    x0, x1, z0, z1, y = -568.0, -536.0, 256.0, 286.0, SWH + 44.0
    wood = "#a8805a"
    b.poly([(x0 - 4, SWH, z0 - 6), (x1 + 8, SWH, z0 - 6), (x1 + 12, SWH, z1 + 4), (x0, SWH, z1 + 4)], in_shade("#2a2430", "deep"), 0.45)
    for (xx, zz) in ((x0 + 3, z1 - 3), (x1 - 3, z1 - 3), (x0 + 3, z0 + 3), (x1 - 3, z0 + 3)):
        b.line([(xx, SWH, zz), (xx, y - 3, zz)], in_shade(wood, "front") * 0.78, 2.0)
    b.box(x0, x1, y - 4, y, z0, z1, wood)
    l.line([(x0, y, z0), (x1, y, z0)], np.clip(in_shade(wood, "up") * 1.4, 0, 1), 0.8, 0.8)
    # the snack bar's sign: a board with a wine jug painted on it, hung from an iron arm at the corner
    sz = ZF + 30.0
    iron = in_shade("#3a3038", "front")
    l.line([(WL, 356, sz), (WL + 64, 356, sz)], iron, 1.4)
    l.line([(WL, 332, sz), (WL + 26, 356, sz)], iron, 1.0)
    for xx in (WL + 14, WL + 54):
        l.line([(xx, 356, sz), (xx, 344, sz)], iron, 0.8)
    b.front(WL + 8, WL + 60, 300, 344, sz, in_shade("#efe4c8", "front") * 1.05)
    for (q0, q1) in (((WL + 8, 300), (WL + 60, 300)), ((WL + 60, 300), (WL + 60, 344)), ((WL + 60, 344), (WL + 8, 344)), ((WL + 8, 344), (WL + 8, 300))):
        l.line([(q0[0], q0[1], sz), (q1[0], q1[1], sz)], in_shade("#8a2a28", "front") * 1.1, 1.0, 0.9)
    jx_, jy_ = P(WL + 31, 306, sz)
    ks_ = kz(sz)
    l.s.poly([(jx_ - 5 * ks_, jy_), (jx_ + 5 * ks_, jy_), (jx_ + 9 * ks_, jy_ - 12 * ks_), (jx_ + 4 * ks_, jy_ - 22 * ks_), (jx_ + 4.5 * ks_, jy_ - 31 * ks_), (jx_ - 4.5 * ks_, jy_ - 31 * ks_), (jx_ - 4 * ks_, jy_ - 22 * ks_), (jx_ - 9 * ks_, jy_ - 12 * ks_)], in_shade("#a8342c", "front") * 1.15)
    l.s.line([(jx_ + 4.5 * ks_, jy_ - 29 * ks_), (jx_ + 12 * ks_, jy_ - 24 * ks_), (jx_ + 8.5 * ks_, jy_ - 13 * ks_)], in_shade("#a8342c", "front") * 1.15, 1.0)
    for (gx_, gy_) in ((15, 12), (19, 16), (15, 20), (11, 16), (15, 26)):                                   # and a few grapes beside it
        l.s.ellipse(jx_ + gx_ * ks_ + 2, jy_ - gy_ * ks_ + 4, 1.2, 1.2, in_shade("#5a3a7a", "front") * 1.2)
    # a striped blanket airing over the balcony rail
    bx_, r0, r1 = BALC["x"] - 7.5, BALC["rail"] + 3.5, BALC["rail"] - 62
    cols_ = ("#d9a13c", "#b8402e", "#e8d9b0", "#3f6a9a", "#e8d9b0", "#b8402e", "#d9a13c")
    for i, tone in enumerate(cols_):
        za_, zb_ = 356 + i * 13.0, 356 + (i + 1) * 13.0
        b.poly([(bx_, r0, za_), (bx_, r0, zb_), (bx_ - 1.5, r1 - 3 * math.sin(i * 1.3), zb_ + 1), (bx_ - 1.5, r1 - 3 * math.sin((i - 1) * 1.3), za_ + 1)], in_shade(tone, "cloth") * 0.95)
        b.poly([(bx_, r0, za_), (bx_, r0, zb_), (bx_ + 12, r0, zb_), (bx_ + 12, r0, za_)], in_shade(tone, "up") * 1.1)
    l.line([(bx_ - 1.5, r1, 356), (bx_ - 1.5, r1 - 2, 447)], in_shade("#3a2a34", "cloth"), 0.7, 0.6)
    # two wine jars against the wall by the left-hand door
    for (zz, lean, sc) in ((748.0, 0.08, 1.0), (776.0, -0.04, 0.92)):
        cx_, cy_ = P(WL + 16, SWH, zz)
        amphora(b.s, cx_, cy_, 112 * kz(zz) * sc, lean, tones=(in_shade("#b0603e", "deep") * 1.7, in_shade("#c8744a", "front") * 0.95, np.clip(in_shade("#f0a878", "up") * 1.1, 0, 1)), light=1)
    # crates and a sack outside the open shop on the right
    b.box(WR - 62, WR - 8, SWH, SWH + 44, 1140.0, 1200.0, "#b08a5a")
    b.box(WR - 52, WR - 10, SWH + 44, SWH + 78, 1146.0, 1190.0, "#9a7648", dim=0.95)
    sx_, sy_ = P(WR - 78, SWH, 1128.0)
    ks_ = kz(1128.0)
    b.s.ellipse(sx_, sy_ - 22 * ks_, 20 * ks_, 24 * ks_, in_shade("#d8c8a0", "warm"))
    b.s.ellipse(sx_ - 5 * ks_, sy_ - 30 * ks_, 9 * ks_, 11 * ks_, np.clip(in_shade("#f0e4c0", "up") * 1.1, 0, 1), 0.7)
    l.line([(WR - 62, SWH + 22, 1140.0), (WR - 8, SWH + 22, 1140.0)], in_shade("#6a4a2a", "front"), 0.7, 0.7)
    # a handcart stands loaded far up the street, across the left half of the roadway: we see it from the side
    cz, hz = 2480.0, col("#b9c2dc")
    fade = lambda c: lerp(np.asarray(c, dtype=F32), hz, 0.20)
    kc = kz(cz)
    c0 = lambda xx, yy: P(xx, yy, cz)
    b.poly([(-156, 0, cz - 30), (70, 0, cz - 30), (70, 0, cz + 60), (-156, 0, cz + 60)], in_shade("#2a2430", "deep"), 0.4)
    wood_c, wood_k = fade(in_shade("#a8845c", "front")), fade(in_shade("#5a4030", "front") * 0.9)
    for d in (b, l):
        d.s.line([c0(-12, 58), c0(62, 4)], wood_k, max(1.0, 5 * kc))                                       # the prop it rests on, and its handles
        d.s.line([c0(-150, 60), c0(84, 60)], wood_k, max(1.6, 9 * kc))                                     # the bed
        d.s.line([c0(-150, 64), c0(-12, 64)], wood_c, max(0.8, 3 * kc), 0.9)
        for (sx_, tone, rx_, ry_) in ((-130.0, "#8a4a3c", 15, 30), (-98.0, "#9a5a40", 16, 34), (-66.0, "#8a4a3c", 15, 30), (-34.0, "#a89060", 20, 18)):
            px_, py_ = c0(sx_, 66 + ry_)                                                                   # its load: three jars and a sack
            d.s.ellipse(px_, py_, rx_ * kc, ry_ * kc, fade(in_shade(tone, "front") * 0.95))
            d.s.ellipse(px_ - 4 * kc, py_ - 6 * kc, rx_ * 0.4 * kc, ry_ * 0.5 * kc, fade(np.clip(in_shade("#e0a080", "up") * 1.0, 0, 1)), 0.6)
            if ry_ > 20:
                d.s.line([c0(sx_, 66 + ry_ * 2 - 4), c0(sx_, 66 + ry_ * 2 + 12)], fade(in_shade(tone, "front") * 0.95), max(1.0, 9 * kc))
        wx_, wy_ = c0(-92, 36)
        ring = [(wx_ + math.cos(a_) * 35 * kc, wy_ + math.sin(a_) * 35 * kc) for a_ in np.linspace(0, 2 * math.pi, 25)]
        d.s.line(ring, wood_k, max(1.2, 6 * kc))                                                           # the wheel
        for a_ in np.linspace(0, math.pi, 4, endpoint=False):
            d.s.line([(wx_ - math.cos(a_) * 33 * kc, wy_ - math.sin(a_) * 33 * kc), (wx_ + math.cos(a_) * 33 * kc, wy_ + math.sin(a_) * 33 * kc)], wood_c, 0.8, 0.9)
        d.s.ellipse(wx_, wy_, 6 * kc, 6 * kc, wood_k)
    # the broom: a stick and a bundle of twigs, leaning in the angle of the door post
    l.line([(WR - 40, SWH, 590), (WR - 3, 205, 584)], in_shade("#b89868", "warm") * 1.05, 1.4)
    rng = np.random.default_rng(seed + 2)
    for i in range(9):
        l.line([(WR - 37, SWH + 34, 590), (WR - 40 - rng.random() * 22 + 6, SWH + rng.random() * 3, 590 + rng.normal(0, 6))], in_shade("#c8a868", "warm") * (0.8 + 0.4 * rng.random()), 0.8, 0.9)
    l.line([(WR - 39, SWH + 30, 590), (WR - 35, SWH + 36, 590)], in_shade("#5a4030", "warm"), 1.6)
    return


def basket(sheet, lines, seed=0):
    """The washerwoman's basket: wicker, two handles, heaped with wet white washing."""
    bx, bz = BASKET
    k = kz(bz)
    cx, by = P(bx, SWH, bz)
    r0, r1, h = 25 * k, 31 * k, 46 * k
    wick, wick_d, wick_l = in_shade("#c89858", "front"), in_shade("#8a6234", "front") * 0.8, np.clip(in_shade("#e8c080", "up") * 1.15, 0, 1)
    body = [(cx - r0, by - 3), (cx - r0 * 0.6, by + 2.5), (cx + r0 * 0.6, by + 2.5), (cx + r0, by - 3), (cx + r1, by - h), (cx - r1, by - h)]
    sheet.ellipse(cx + 4, by + 1, r0 * 1.5, 5.0, in_shade("#2a2430", "deep"), 0.6)                     # its shade on the sidewalk
    sheet.poly(body, wick)
    sheet.poly([(cx + r0 * 0.35, by + 2.5), (cx + r0, by - 3), (cx + r1, by - h), (cx + r1 * 0.45, by - h)], wick_d, 0.55)
    for i in range(1, 9):                                    # the weave: rows of short dashes, out of step
        yy = by - h * i / 9.0
        rr = lerp(r0, r1, i / 9.0)
        n = 9
        for j in range(n):
            xa = cx - rr + (j + (0.5 if i % 2 else 0.0)) * 2 * rr / n
            lines.line([(xa, yy + 1.2 * abs((xa - cx) / rr) ** 2), (min(xa + rr / n * 1.1, cx + rr), yy + 1.2 * abs((xa - cx) / rr) ** 2)], wick_d if (i + j) % 2 else wick_l, 0.8, 0.75)
    for j in range(1, 8):
        xa = j / 8.0
        lines.line([(cx - r0 + xa * 2 * r0, by), (cx - r1 + xa * 2 * r1, by - h)], wick_d, 0.6, 0.45)
    # the washing: a heap of wet cloth, bluish in the shade, with one end hanging over the rim
    white, white_d, white_l = in_shade("#fbf6ea", "front"), in_shade("#fbf6ea", "front") * 0.78, np.clip(in_shade("#fffdf4", "up") * 1.12, 0, 1)
    heap = [(cx - r1 * 0.95, by - h + 1), (cx - r1 * 0.8, by - h - 9), (cx - r1 * 0.3, by - h - 15), (cx + r1 * 0.15, by - h - 12), (cx + r1 * 0.6, by - h - 16), (cx + r1 * 0.95, by - h - 7), (cx + r1 * 0.95, by - h + 1)]
    sheet.poly(heap, white)
    sheet.poly([(cx + r1 * 0.15, by - h - 12), (cx + r1 * 0.6, by - h - 16), (cx + r1 * 0.95, by - h - 7), (cx + r1 * 0.95, by - h + 1), (cx + r1 * 0.3, by - h + 1)], white_d)
    sheet.poly([(cx - r1 * 0.75, by - h - 8), (cx - r1 * 0.3, by - h - 14), (cx + r1 * 0.05, by - h - 11), (cx - r1 * 0.3, by - h - 6)], white_l)
    sheet.poly([(cx - r1 * 0.62, by - h - 2), (cx - r1 * 0.2, by - h - 3), (cx - r1 * 0.12, by - h + 13), (cx - r1 * 0.3, by - h + 17), (cx - r1 * 0.55, by - h + 12)], white)   # the end over the rim
    lines.line([(cx - r1 * 0.4, by - h - 2), (cx - r1 * 0.36, by - h + 14)], white_d, 0.8, 0.8)
    lines.line([(cx - r1 * 0.1, by - h - 12), (cx + r1 * 0.2, by - h - 4), (cx + r1 * 0.5, by - h - 2)], white_d * 0.92, 0.8, 0.8)
    lines.line([(cx - r1, by - h), (cx + r1, by - h)], wick_l, 1.6)                                    # the rim, over the cloth
    lines.line([(cx - r1, by - h + 1.6), (cx + r1, by - h + 1.6)], wick_d, 0.8, 0.8)
    for side in (-1, 1):                                     # handles
        lines.line([(cx + side * r1 * 0.98, by - h + 2), (cx + side * (r1 + 5), by - h + 7), (cx + side * r1 * 0.98, by - h + 13)], wick_d if side > 0 else wick, 1.5)
    return


# ================================================================ the cut-outs
def scraps(u, v, seed, px=1.0):
    """A face covered with odd pieces of colored marble set in mortar, as the counters of snack bars were."""
    edge, r1, r2, mid = cells(u, v, 16.0, seed, jitter=0.9)
    pal = np.array([col(c) for c in ("#ebe3d2", "#b7c3cb", "#7c9c88", "#b9574c", "#e2bb6c", "#8d8794", "#dccbb8", "#6b7c9e", "#cc9c8a", "#f0e8dc", "#a8b89a")])
    idx = np.minimum((r1 * len(pal)).astype(int), len(pal) - 1)
    c = pal[idx] * (0.90 + 0.20 * r2)[..., None]
    vein = wn(u * 3.0, v * 3.0 + u, 30, seed + 3, 3) - 0.5
    c = c * (1 + vein[..., None] * 0.12)
    joint = np.clip((1.1 - edge) / max(px, 0.5) + 0.5, 0, 1)
    over(c, col("#a89c8c"), (joint * 0.85).astype(F32))
    return np.clip(c, 0, 1).astype(F32), joint.astype(F32)


def hang_garlic(s, x, y, n, k):
    """A braid of garlic hanging from (x, y): white heads, two by two, down a plait of dry stalks."""
    s.line([(x, y), (x + 0.6, y + n * 6.4 * k)], in_shade("#c8b888", "front"), max(1.0, 2.0 * k))
    for i in range(n):
        yy = y + (3 + i * 6.2) * k
        for side in (-1, 1):
            cx = x + side * 3.3 * k + (0.6 if i % 2 else -0.4)
            s.ellipse(cx, yy, 3.6 * k, 3.3 * k, in_shade("#f6f0e2", "cloth") * (0.95 if side > 0 else 1.06))
            s.ellipse(cx - 0.8 * k, yy - 0.9 * k, 1.5 * k, 1.3 * k, np.clip(in_shade("#ffffff", "cloth") * 1.18, 0, 1))
    s.line([(x, y + n * 6.4 * k), (x - 2 * k, y + (n * 6.4 + 6) * k)], in_shade("#c8b888", "front"), 0.8)


def hang_sausages(s, x, y, w, drop, k, n=5):
    """A string of sausages in a loop: fat dark-red links."""
    tone, hi = in_shade("#b8483c", "cloth") * 1.0, np.clip(in_shade("#f08a70", "cloth") * 1.1, 0, 1)
    pts = [(x + (t - 0.5) * w * k, y + drop * k * math.sin(math.pi * t) ** 0.8) for t in np.linspace(0, 1, n * 4 + 1)]
    for i in range(n):
        seg = pts[i * 4:i * 4 + 4]
        s.line(seg, tone, max(1.8, 4.2 * k))
        s.line([(px - 0.5, py - 0.7) for px, py in seg[1:3]], hi, max(0.7, 1.2 * k), 0.8)
    s.line([pts[0], (pts[0][0], y - 3 * k)], in_shade("#c8b888", "front"), 0.7)
    s.line([pts[-1], (pts[-1][0], y - 3 * k)], in_shade("#c8b888", "front"), 0.7)


def hang_loaves(s, x, y, n, k):
    """Ring loaves threaded on a cord."""
    s.line([(x, y), (x, y + (n * 9.5 + 2) * k)], in_shade("#c8b888", "front"), 0.8)
    for i in range(n):
        cy = y + (6 + i * 9.2) * k
        s.ellipse(x, cy, 6.8 * k, 5.4 * k, np.clip(in_shade("#e8b060", "cloth") * 1.12, 0, 1))
        s.ellipse(x - 1.2 * k, cy - 1.5 * k, 3.8 * k, 2.3 * k, np.clip(in_shade("#fbd890", "cloth") * 1.2, 0, 1))
        s.ellipse(x, cy + 0.4 * k, 1.9 * k, 1.5 * k, in_shade("#6a4426", "deep") * 1.6)


def hang_herbs(s, x, y, k, seed=0):
    """A bunch of dry herbs, tied by the stalks and hung head down."""
    rng = np.random.default_rng(seed)
    for i in range(16):
        a = rng.normal(0, 0.28)
        ln = (20 + rng.random() * 14) * k
        tone = lerp(in_shade("#5f7a48", "front"), in_shade("#a8b070", "front"), rng.random()) * 1.1
        s.line([(x, y + 3 * k), (x + math.sin(a) * ln, y + 3 * k + math.cos(a) * ln)], tone, max(0.8, 1.5 * k), 0.95)
    s.line([(x, y - 2 * k), (x, y + 5 * k)], in_shade("#c8b888", "front"), 1.0)


def awning_plane(seed=5):
    """The snack bar's awning, what hangs from it, and the front arm of the counter with what stands on it:
    everything the keeper stands behind. -> (color, alpha, crisp lines color, alpha)"""
    b, l = Dr(), Dr()
    A = AWN
    n = 12
    red, cream = "#c8503a", "#efe2c2"

    def front_y(x):
        t = (x - A["x0"]) / (A["x1"] - A["x0"])
        return A["y1"] - 5.0 * math.sin(math.pi * t)
    zm = (A["z0"] + A["z1"]) / 2
    for i in range(n):
        xa, xb = lerp(A["x0"], A["x1"], i / n), lerp(A["x0"], A["x1"], (i + 1) / n)
        tone = red if i % 2 == 0 else cream
        ym_a, ym_b = (A["y0"] + front_y(xa)) / 2 - 5, (A["y0"] + front_y(xb)) / 2 - 5
        b.poly([(xa, A["y0"], A["z0"]), (xb, A["y0"], A["z0"]), (xb, ym_b, zm), (xa, ym_a, zm)], in_shade(tone, "cloth") * 0.90)      # the cloth sags a little
        b.poly([(xa, ym_a, zm), (xb, ym_b, zm), (xb, front_y(xb), A["z1"]), (xa, front_y(xa), A["z1"])], in_shade(tone, "cloth") * 1.02)
        d = A["drop"] * (0.86 + 0.28 * _hash(np.float32(i), np.float32(3.0), seed))
        ya, yb = front_y(xa), front_y(xb)
        b.poly([(xa, ya, A["z1"]), (xb, yb, A["z1"]), (xb, yb - d * 0.66, A["z1"]), ((xa + xb) / 2, (ya + yb) / 2 - d, A["z1"]), (xa, ya - d * 0.66, A["z1"])], in_shade(tone, "front") * 1.02)   # the scalloped edge hanging down
        l.line([(xa, ya - d * 0.66, A["z1"]), ((xa + xb) / 2, (ya + yb) / 2 - d, A["z1"]), (xb, yb - d * 0.66, A["z1"])], in_shade(tone, "front") * 0.62, 0.8, 0.8)
        l.line([(xa, A["y0"], A["z0"]), (xa, ym_a, zm), (xa, ya, A["z1"])], in_shade("#7a4a4a", "cloth") * 0.9, 0.6, 0.45)
    pa = [(-452.0, 0.30), (-404.0, 0.26), (-400.0, 0.66), (-448.0, 0.72)]                                  # it has been mended: a patch of plain cloth, sewn on
    on = lambda xx, t: (xx, lerp(A["y0"], front_y(xx), t) - 5 * math.sin(math.pi * t), lerp(A["z0"], A["z1"], t))
    b.poly([on(*q) for q in pa], in_shade("#d8c49a", "cloth") * 0.96)
    for i in range(4):
        q0, q1 = pa[i], pa[(i + 1) % 4]
        for u in np.linspace(0.08, 0.92, 6):
            mx_, mt_ = lerp(q0[0], q1[0], u), lerp(q0[1], q1[1], u)
            l.line([on(mx_ - 1.5, mt_ - 0.015), on(mx_ + 1.5, mt_ + 0.015)], in_shade("#4a3440", "cloth"), 0.7, 0.8)
    l.line([(xx, front_y(xx), A["z1"]) for xx in np.linspace(A["x0"], A["x1"], 9)], np.clip(in_shade("#fff6e0", "cloth") * 1.1, 0, 1), 1.0, 0.8)   # the pole along the front, under the cloth
    l.line([(A["x1"], A["y0"], A["z0"]), (A["x1"], (A["y0"] + A["y1"]) / 2 - 5, zm), (A["x1"], A["y1"], A["z1"])], in_shade("#5a3438", "cloth"), 1.0, 0.9)
    l.line([(xx, A["y0"], A["z0"]) for xx in (A["x0"], A["x1"])], in_shade("#3a2c34", "deep") * 1.4, 1.2, 0.8)
    # a rope stay from the front corner up to the wall
    l.line([(A["x1"] + 2, A["y1"], A["z1"]), (A["x1"] + 6, 366, ZF - 2)], in_shade("#d8c8a0", "front"), 2.0, 1.0)

    # the counter's front arm: a face of marble scraps, a pale slab on top with jar mouths sunk in it
    xw, yw, kw = wall_z(BAR["z0"])
    face = band(xw, BAR["x0"], BAR["x1"], 1 / kw) * band(yw, SWH, BAR["top"] - 7, 1 / kw)
    marble, mortar = scraps(xw, yw, seed + 3, 1 / kw)
    over(marble, col("#8f8478"), band(yw, SWH, SWH + 9, 1 / kw))                                     # a plain foot
    local_face = in_shade(marble, "front") * (0.86 + 0.24 * np.clip((yw - SWH) / 90.0, 0, 1))[..., None]
    xt, zt, kt, okt = level(BAR["top"])
    top = band(xt, BAR["x0"], BAR["x1"], 1 / kt) * band(zt, BAR["z0"], BAR["z1"], 2.2 / kt) * okt
    slab = vary("#ddd4c4", SHAPE, seed + 4, 0.06, 14)
    slab_c = in_shade(slab, "up") * 1.10
    lip = band(xw, BAR["x0"] - 2, BAR["x1"], 1 / kw) * band(yw, BAR["top"] - 7, BAR["top"], 1 / kw)
    cc = np.zeros(SHAPE + (3,), dtype=F32)
    ca = np.zeros(SHAPE, dtype=F32)
    for colr, m in ((slab_c, top), (local_face, face), (in_shade(slab, "front") * 1.15, lip)):
        cc = cc * (1 - m[..., None]) + colr * m[..., None]
        ca = np.maximum(ca, m)
    t = Dr()
    for i, xx in enumerate((-488.0, -432.0, -384.0)):
        jar_mouth(t, l, xx, BAR["top"], 371.0, 20.0, lid=(i == 1))
    # a ladle standing in the first jar
    l.line([(-492, BAR["top"] + 2, 372), (-476, BAR["top"] + 30, 366)], in_shade("#c89a4a", "front") * 1.2, 1.1)
    # the charcoal stove at the right end, with a bronze pot on it
    sx0, sx1, sz0, sz1, sy = -352.0, -320.0, 350.0, 392.0, BAR["top"]
    cam.box(t.s, sx0, sx1, sy, sy + 22, sz0, sz1, in_shade("#b86a48", "front"), in_shade("#8a4a34", "up") * 0.8, (in_shade("#b86a48", "warm"), in_shade("#9a5238", "front") * 0.9))
    for xx in (-346.0, -338.0, -330.0):                                                                # the fire shows through holes in its front
        t.front(xx, xx + 4.5, sy + 6, sy + 14, sz0 - 0.5, "#f0803a")
        l.front(xx + 1, xx + 3.5, sy + 8, sy + 12, sz0 - 0.6, "#ffd070")
    px0, py0 = P(-336, sy + 22, 371)
    kk = kz(371)
    t.s.ellipse(px0, py0 - 9 * kk, 15 * kk, 11 * kk, in_shade("#b8873a", "front") * 0.95)                # the pot: a round belly,
    t.s.ellipse(px0, py0 - 17 * kk, 13 * kk, 4.2 * kk, in_shade("#3a2a22", "deep") * 1.3)              # a dark mouth,
    l.s.line([(px0 - 13 * kk, py0 - 17 * kk), (px0 - 9 * kk, py0 - 20.4 * kk), (px0 + 9 * kk, py0 - 20.4 * kk), (px0 + 13 * kk, py0 - 17 * kk)], in_shade("#e8c070", "up") * 1.4, 0.9, 0.9)
    l.s.line([(px0 - 9 * kk, py0 - 12 * kk), (px0 - 11 * kk, py0 - 6 * kk)], in_shade("#f6dc8a", "up") * 1.5, 1.0, 0.85)   # and the sky on its shoulder
    t.s.ellipse(px0, py0 - 1.0 * kk, 13 * kk, 2.4 * kk, "#e8742c", 0.9)                                # the coals glowing under it
    # a jug and two cups at the left end; a rag over the front edge
    jx, jy = P(-508, sy, 366)
    t.s.poly([(jx - 4, jy), (jx + 4, jy), (jx + 5.5, jy - 8), (jx + 2.4, jy - 13), (jx + 2.6, jy - 17), (jx - 2.6, jy - 17), (jx - 2.4, jy - 13), (jx - 5.5, jy - 8)], in_shade("#c8744a", "front") * 1.1)
    l.s.line([(jx + 2.6, jy - 16), (jx + 7, jy - 13), (jx + 5.5, jy - 8)], in_shade("#c8744a", "front") * 0.9, 1.0)
    l.s.line([(jx - 3.6, jy - 9), (jx - 2.6, jy - 3)], in_shade("#f0b088", "up") * 1.3, 0.8, 0.8)
    for cx in (-466.0, -455.0):
        ux, uy = P(cx, sy, 362)
        t.s.poly([(ux - 2.6, uy), (ux + 2.6, uy), (ux + 3.4, uy - 5.5), (ux - 3.4, uy - 5.5)], in_shade("#d9b06a", "front") * 1.1)
        l.s.line([(ux - 3.4, uy - 5.5), (ux + 3.4, uy - 5.5)], in_shade("#f6dc9a", "up") * 1.4, 0.7, 0.9)
    for (lx_, lz_, up_) in ((-452.0, 350.0, 0.0), (-446.0, 362.0, 0.0), (-449.0, 356.0, 7.0)):          # round loaves, scored like wheels
        qx, qy = P(lx_, sy + up_, lz_)
        kq = kz(lz_)
        t.s.ellipse(qx, qy - 3.4 * kq, 10 * kq, 5.6 * kq, in_shade("#d9a054", "front") * 1.12)
        t.s.ellipse(qx - 1.5 * kq, qy - 4.6 * kq, 7 * kq, 3.4 * kq, np.clip(in_shade("#f0c880", "up") * 1.2, 0, 1))
        for a_ in (0.0, 0.8, 1.6, 2.4):
            l.s.line([(qx - math.cos(a_) * 7.5 * kq, qy - 4.2 * kq - math.sin(a_) * 3.2 * kq), (qx + math.cos(a_) * 7.5 * kq, qy - 4.2 * kq + math.sin(a_) * 3.2 * kq)], in_shade("#8a5a2a", "front"), 0.6, 0.7)
    t.poly([(-420, BAR["top"] + 0.5, 334), (-398, BAR["top"] + 0.5, 334), (-398, BAR["top"] + 0.5, 362), (-420, BAR["top"] + 0.5, 362)], in_shade("#e8e0d0", "cloth"))
    t.poly([(-420, BAR["top"], 329.5), (-398, BAR["top"], 329.5), (-399, BAR["top"] - 24, 329.5), (-409, BAR["top"] - 28, 329.5), (-419, BAR["top"] - 22, 329.5)], in_shade("#e8e0d0", "cloth") * 0.92)
    l.line([(-412, BAR["top"], 329.4), (-411, BAR["top"] - 24, 329.4)], in_shade("#a8a4c0", "cloth") * 0.9, 0.7, 0.8)

    # what hangs from the awning's front pole, clear of where the keeper stands
    h = Dr()
    k1 = kz(A["z1"])
    for (xx, what) in ((-548.0, "herbs"), (-512.0, "garlic"), (-474.0, "sausage"), (-436.0, "loaves"), (-398.0, "garlic2"), (-306.0, "sausage2")):
        px1, py1 = P(xx, front_y(xx) - A["drop"] * 0.7, A["z1"])
        if what == "herbs":
            hang_herbs(h.s, px1, py1, k1, seed)
        elif what == "garlic":
            hang_garlic(h.s, px1, py1, 6, k1)
        elif what == "garlic2":
            hang_garlic(h.s, px1, py1, 4, k1)
        elif what == "sausage":
            hang_sausages(h.s, px1, py1 + 2, 22, 30, k1, 5)
        elif what == "sausage2":
            hang_sausages(h.s, px1, py1 + 2, 15, 26, k1, 4)
        else:
            hang_loaves(h.s, px1, py1, 4, k1)
    lc, la = l.s.done()
    jm = mortar * face * (yw > SWH + 9) * 0.55                                                          # the mortar between the scraps, to be said again over the brushwork
    la2 = la + jm * (1 - la)
    lc = np.where(la2[..., None] > 1e-4, (lc * la[..., None] + in_shade("#8c8274", "front") * 0.9 * (jm * (1 - la))[..., None]) / np.maximum(la2[..., None], 1e-4), 0).astype(F32)
    awc, awa = b.s.done()
    worn = (noise(SHAPE, (36, 10), seed + 8, 3) - 0.5) * 0.20 + (noise(SHAPE, (7, 60), seed + 9, 2) - 0.5) * 0.10       # the cloth is faded in places and streaked by rain
    awc = np.clip(awc * (1 + worn)[..., None] + ((PY - 259) / 60.0 * 0.03)[..., None], 0, 1)                                   # and bleached toward its outer edge
    color, alpha = join((cc, ca), (awc, awa), t.s.done(), h.s.done())
    return color, alpha, lc, la2


def fountain_plane(seed=5, moving=None):
    """The public fountain: a basin of four stone slabs, brim full, and a short pillar with a carved face that
    spouts into it. A bronze jug has been left on the rim. -> (color, alpha, lines color, alpha)
    `moving`: with the water falling from the mouth, its rings, and the sparrow drinking (PAINT_MOVING if not said)."""
    moving = PAINT_MOVING if moving is None else moving
    b, l = Dr(), Dr()
    f = FOUNT
    x0, x1, z0, z1 = f["x0"], f["x1"], f["z0"], f["z1"]
    y0, y1, w = SWH, SWH + f["h"], f["wall"]
    yw = y1 - 4.0                                               # the water stands just under the rim
    stone = "#c9c0b0"
    fr, up, wm = in_shade(stone, "front"), in_shade(stone, "up") * 1.06, in_shade(stone, "warm") * 1.08
    # the pillar at the back, with its rounded head
    px0, px1, pz0, pz1, ptop = 289.0, 353.0, z1 - 20.0, z1 + 12.0, SWH + 172.0
    b.side(px0, pz0, pz1, y0, ptop - 8, wm * 0.98)
    head = [(px0, y0, pz0), (px1, y0, pz0), (px1, ptop - 14, pz0)] + [((px0 + px1) / 2 + math.cos(a) * 32, ptop - 14 + math.sin(a) * 14, pz0) for a in np.linspace(0, math.pi, 9)] + [(px0, ptop - 14, pz0)]
    b.poly(head, fr * 1.04)
    # the left slab (it faces the street), the inside, the water
    b.side(x0, z0, z1, y0, y1, wm)
    b.front(x0 + w, x1 - w, yw - 30, y1, z1 - w, in_shade(stone, "deep") * 2.0)                       # inside of the far slab
    b.side(x1 - w, z0 + w, z1 - w, yw - 30, y1, in_shade(stone, "deep") * 2.3)                        # inside of the right slab
    water = [(x0 + w, yw, z0 + w), (x1 - w, yw, z0 + w), (x1 - w, yw, z1 - w), (x0 + w, yw, z1 - w)]
    b.poly(water, "#4a76b8")
    b.poly([(x0 + w, yw, z0 + w + 66), (x1 - w, yw, z0 + w + 66), (x1 - w, yw, z1 - w), (x0 + w, yw, z1 - w)], "#34507e", 0.8)      # the wall's dark lies in it
    b.poly([(px0 + 4, yw, z0 + w + 50), (px1 - 4, yw, z0 + w + 50), (px1, yw, z1 - w), (px0, yw, z1 - w)], "#8a8fae", 0.6)          # and the pillar, upside down
    b.poly([(x0 + w + 6, yw, z0 + w + 18), (x0 + w + 96, yw, z0 + w + 12), (x0 + w + 84, yw, z0 + w + 50), (x0 + w + 4, yw, z0 + w + 56)], "#9cc2f0", 0.75)   # a piece of sky
    # the rim: far slab, left and right slabs, near slab; then the front
    b.flat(x0, x1, z1 - w, z1, y1, up * 0.98)
    b.flat(x0, x0 + w, z0, z1, y1, up * 1.02)
    b.flat(x1 - w, x1, z0, z1, y1, up * 0.94)
    b.flat(x0, x1, z0, z0 + w, y1, up * 1.08)
    b.front(x0, x1, y0, y1, z0, fr)
    color, alpha = b.s.done()
    color = np.clip(color * (1 + (noise(SHAPE, 14, seed + 30, 3) - 0.5) * 0.14)[..., None], 0, 1)             # stone is never one color
    # the front slab's stone: stained, green at the foot where it is always wet
    xw_, yw_, kw_ = wall_z(z0)
    m = band(xw_, x0, x1, 1 / kw_) * band(yw_, y0, y1 - 1, 1 / kw_)
    tex = plaster(xw_, yw_, stone, seed + 31, 0.10, 0.08)
    green = np.clip(1 - (yw_ - y0) / 34.0, 0, 1) * (0.3 + 0.7 * wn(xw_, yw_, 30, seed + 32, 3))
    over(tex, col("#7f9468"), (green * 0.6).astype(F32))
    drip = np.clip(1 - np.abs(xw_ - (x0 + 62) - (wn(xw_, yw_, 40, seed + 33, 2) - 0.5) * 16) / 15.0, 0, 1)             # where it spills over the worn place in the rim
    tex *= (1 - drip * 0.34)[..., None]
    scale = np.clip(1 - np.abs(np.abs(xw_ - (x0 + 62)) - 17) / 5.0, 0, 1) * np.clip((yw_ - y0 - 20) / 40.0, 0, 1) * 0.5        # and has left its lime down both sides of the wet
    over(tex, col("#f0ecdc"), scale.astype(F32))
    blotch = step(0.66, 0.8, wn(xw_, yw_, 16, seed + 34, 3)) * 0.5                                                          # lichen
    over(tex, col("#c8c08a"), (blotch * 0.5).astype(F32))
    texc = in_shade(tex, "front") * (0.80 + 0.32 * np.clip((yw_ - y0) / 80.0, 0, 1))[..., None]
    texc = lerp(texc, col("#7e96cc"), (drip * 0.34)[..., None])
    over(color, texc, m)

    # ---- crisp things
    for (xa, za, xb, zb) in ((x0, z0, x1, z0), (x0, z0, x0, z1)):                                     # the rim's edges catch the sky
        l.line([(xa, y1, za), (xb, y1, zb)], np.clip(up * 1.25, 0, 1), 0.9, 0.85)
    l.line([(x0 + w, y1, z0 + w), (x1 - w, y1, z0 + w)], in_shade(stone, "deep") * 2.0, 0.8, 0.8)
    l.line([(x0 + w, y0, z0), (x0 + w, y1, z0)], in_shade(stone, "front") * 0.66, 0.8, 0.7)           # the joints between the slabs
    l.line([(x1 - w, y0, z0), (x1 - w, y1, z0)], in_shade(stone, "front") * 0.66, 0.8, 0.7)
    l.line([(x0, y0, z0), (x1, y0, z0)], in_shade("#2a2430", "deep"), 1.2, 0.8)
    for (cx, cz, dx, dz) in ((x0 + w, z0 + w * 0.5, 1, 0), (x1 - w, z0 + w * 0.5, 1, 0), (x0 + w * 0.5, z1 - w, 0, 1)):      # iron cramps across the joints
        l.line([(cx - 9 * dx, y1 + 0.5, cz - 7 * dz), (cx + 9 * dx, y1 + 0.5, cz + 7 * dz)], in_shade("#5a4038", "up") * 0.8, 1.6)
    for (xa, xb) in ((x0 + 46.0, x0 + 78.0), (x0 + 124.0, x0 + 150.0)):                               # the rim is worn into hollows where jars are rested
        l.poly([(xa, y1 + 0.6, z0 - 0.4), (xb, y1 + 0.6, z0 - 0.4), (xb - 6, y1 - 5, z0 - 0.4), (xa + 6, y1 - 5, z0 - 0.4)], np.clip(in_shade(stone, "up") * 1.22, 0, 1))
        l.line([(xa, y1 + 0.6, z0 - 0.5), (xa + 6, y1 - 5, z0 - 0.5), (xb - 6, y1 - 5, z0 - 0.5), (xb, y1 + 0.6, z0 - 0.5)], in_shade(stone, "front") * 0.62, 0.8, 0.8)
    for (cx, tone) in ((x0 + w, "#4a3832"), (x1 - w, "#4a3832")):                                          # iron cramps hold the slabs at the corners
        l.line([(cx - 9, y1 - 12, z0 - 0.5), (cx + 9, y1 - 12, z0 - 0.5)], in_shade(tone, "front") * 0.9, 1.6)
        l.line([(cx - 9, y0 + 16, z0 - 0.5), (cx + 9, y0 + 16, z0 - 0.5)], in_shade(tone, "front") * 0.9, 1.6)
    l.poly([(x0, y1, z0 - 0.5), (x0 + 9, y1, z0 - 0.5), (x0, y1 - 8, z0 - 0.5)], in_shade(stone, "deep") * 1.8)                  # a corner knocked off by a cart
    sx_, sy_ = P(x1 - 40, y1, z0 + 7)                                                                      # a sparrow come to drink
    if moving:
        l.s.ellipse(sx_, sy_ - 3.2, 4.0, 2.6, in_shade("#8a6a4a", "front") * 1.2)
        l.s.ellipse(sx_ - 3.4, sy_ - 5.4, 1.9, 1.8, in_shade("#6a4a34", "front") * 1.2)
        l.s.line([(sx_ + 3, sy_ - 3.6), (sx_ + 7.5, sy_ - 5.5)], in_shade("#5a4030", "front") * 1.2, 1.2)
        l.s.line([(sx_ - 5.2, sy_ - 5.2), (sx_ - 6.8, sy_ - 4.6)], in_shade("#d8a060", "front") * 1.2, 0.7)
        l.s.ellipse(sx_ + 0.6, sy_ - 2.6, 2.2, 1.2, np.clip(in_shade("#d8c0a0", "front") * 1.2, 0, 1))
    for (cx, cz, tone) in ((262.0, 300.0, "#e8c468"), (330.0, 286.0, "#dfe4ea"), (300.0, 318.0, "#c8944a"), (372.0, 305.0, "#e8c468"), (352.0, 276.0, "#c8944a"), (282.0, 272.0, "#dfe4ea")):
        ccx, ccy = P(cx, yw, cz)                                                                      # coins under the water
        l.s.ellipse(ccx, ccy, 2.0, 0.9, lerp(col(tone), col("#4f6f9e"), 0.35), 0.95)
        l.s.ellipse(ccx - 0.5, ccy - 0.3, 0.8, 0.5, "#fffbe0", 0.9)
    # the carved face: round cheeks, staring eyes, an open mouth with the pipe in it
    fx, fy = P((px0 + px1) / 2, SWH + 128.0, pz0 - 1)
    kk = kz(pz0)
    r = 22 * kk
    l.s.ellipse(fx, fy, r * 1.16, r * 1.12, fr * 0.80)                                                # hair, a rough ring
    for a in np.linspace(0.2, math.pi - 0.2, 9):
        l.s.line([(fx + math.cos(a) * r * 0.9, fy - math.sin(a) * r * 0.9), (fx + math.cos(a) * r * 1.2, fy - math.sin(a) * r * 1.15)], fr * 1.12, 1.0, 0.8)
    l.s.ellipse(fx, fy + r * 0.06, r * 0.86, r * 0.92, fr * 1.12)                                     # the face
    l.s.ellipse(fx - r * 0.22, fy - r * 0.1, r * 0.5, r * 0.6, np.clip(fr * 1.24, 0, 1), 0.7)         # lit from the left, where the sunny wall is
    for sd in (-1, 1):
        l.s.ellipse(fx + sd * r * 0.36, fy - r * 0.22, r * 0.19, r * 0.13, fr * 0.45)                 # eyes
        l.s.line([(fx + sd * r * 0.16, fy - r * 0.44), (fx + sd * r * 0.58, fy - r * 0.40)], fr * 0.62, 0.9, 0.9)   # brows
        l.s.ellipse(fx + sd * r * 0.50, fy + r * 0.26, r * 0.22, r * 0.2, fr * (1.2 if sd < 0 else 0.98), 0.7)       # cheeks
    l.s.line([(fx, fy - r * 0.2), (fx - r * 0.06, fy + r * 0.14), (fx + r * 0.08, fy + r * 0.16)], fr * 0.6, 0.9, 0.9)   # nose
    l.s.ellipse(fx, fy + r * 0.5, r * 0.26, r * 0.2, fr * 0.30)                                       # the mouth
    l.s.poly([(fx - r * 0.2, fy + r * 0.7), (fx + r * 0.2, fy + r * 0.7), (fx + r * 0.42, fy + r * 2.0), (fx - r * 0.42, fy + r * 2.0)], lerp(fr * 0.7, col("#6f9a6a"), 0.3), 0.55)   # where it has always dribbled: dark and green
    # the water: a thin fall from the mouth, a ring where it lands
    mx, my, mz = (px0 + px1) / 2, SWH + 128.0 - 11.0, pz0 - 2
    fall = []
    for t in np.linspace(0, 1, 9):
        fall.append((mx, my - (my - yw) * t * t, mz - 44 * t))
    lx, ly = P(mx, yw, mz - 44)
    if moving:
        l.line(fall, "#e6f0ff", 1.5, 0.95)
        l.line([(p[0] + 1.6, p[1], p[2]) for p in fall[2:]], "#9fb8e4", 0.8, 0.8)
        for rr, aa in ((5.0, 0.9), (9.0, 0.6), (14.0, 0.35)):
            pts = [(lx + math.cos(a) * rr * 1.6, ly + math.sin(a) * rr * 0.42) for a in np.linspace(0, 2 * math.pi, 22)]
            l.s.line(pts, "#dfeaff", 0.7, aa)
        l.s.ellipse(lx, ly, 3.0, 1.2, "#ffffff", 0.9)
    # a bronze jug left on the corner of the rim
    jx, jy = P(x0 + 16, y1, z0 + 9)
    l.s.poly([(jx - 5, jy), (jx + 5, jy), (jx + 7.5, jy - 9), (jx + 3.2, jy - 15), (jx + 3.6, jy - 20), (jx - 3.6, jy - 20), (jx - 3.2, jy - 15), (jx - 7.5, jy - 9)], in_shade("#b8873a", "front") * 1.05)
    l.s.poly([(jx - 5, jy), (jx - 1, jy), (jx - 2.5, jy - 9), (jx - 1, jy - 15), (jx - 3.2, jy - 15), (jx - 7.5, jy - 9)], np.clip(in_shade("#f0cc7a", "warm") * 1.3, 0, 1))
    l.s.line([(jx + 3.6, jy - 19), (jx + 9.5, jy - 15), (jx + 7.5, jy - 9)], in_shade("#b8873a", "front") * 0.85, 1.2)
    l.s.line([(jx - 3.6, jy - 20), (jx + 3.6, jy - 20)], np.clip(in_shade("#f6dc8a", "up") * 1.5, 0, 1), 0.9)
    lc, la = l.s.done()
    return color, alpha, lc, la


ROPES = {                                                     # washing lines: (left end), (right end), how far each sags
    "low": ((WL - 6.0, 256.0, ZF - 4.0), (BALC["x"], BALC["rail"], BALC["posts"][0]), 26.0),
    "near": ((WL, 548.0, 470.0), (BALC["x"], 546.0, BALC["posts"][1]), 30.0),
    "far": ((WL, 616.0, 640.0), (BALC["x"], 588.0, BALC["posts"][2]), 30.0),
    "beyond": ((WL, 690.0, 1010.0), (WR, 700.0, 1120.0), 44.0),
}


def rope_at(name, t):
    a, b, sag = ROPES[name]
    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t) - sag * 4 * t * (1 - t), lerp(a[2], b[2], t))


WASH = [                                                      # line, from, to, how long it hangs (cm), what, color
    ("beyond", 0.10, 0.26, 105, "sheet", "#f4ecd8"), ("beyond", 0.30, 0.40, 80, "tunic", "#c98a5a"), ("beyond", 0.56, 0.70, 95, "sheet", "#dfe6ee"),
    ("beyond", 0.76, 0.86, 70, "tunic", "#f0e6cc"),
    ("far", 0.03, 0.27, 150, "sheet", "#fffdf2"), ("far", 0.295, 0.405, 92, "tunic", "#f3e2bc"), ("far", 0.64, 0.75, 86, "tunic", "#c75c44"),
    ("far", 0.775, 0.95, 128, "sheet", "#f2ecdc"),
    ("near", 0.035, 0.36, 138, "toga", "#fffdf4"), ("near", 0.60, 0.65, 66, "strip", "#e3b54c"),
    ("near", 0.675, 0.80, 100, "tunic", "#9fb8dc"), ("near", 0.825, 0.975, 124, "sheet", "#f6f0e0"),
]
TUNIC = ("low", 0.075, 0.165, 62, "tunic", "#f4ecd6")


def cloth(item, seed):
    """One piece of washing on its line, with its folds and the light on them. -> (color, mask)"""
    name, t0, t1, length, kind, tone = item
    rng = np.random.default_rng(seed)
    top3 = [rope_at(name, t) for t in np.linspace(t0, t1, 9)]
    zmid = top3[4][2]
    k = kz(zmid)
    tx = np.array([P(*p)[0] for p in top3])
    ty = np.array([P(*p)[1] for p in top3])
    xl, xr = float(tx[0]), float(tx[-1])
    wd = xr - xl
    L = length * k
    top_y = np.interp(PX, tx, ty)
    v = (PY - top_y) / L
    wind = (1.5 + rng.normal(0, 1.2)) * (0.6 if kind == "toga" else 1.0)                              # the morning air leans everything a little to the right
    sway = wind * np.clip(v, 0, 1.3) ** 1.4 + np.sin(v * 5.0 + rng.random() * 6) * 0.8 * np.clip(v, 0, 1)
    u = (PX - sway - xl) / wd
    nf = max(2.0, wd / (15.0 if kind == "toga" else 9.5))                                             # how many folds
    ph = rng.random(3) * 6.283
    spread = 1.0 + np.clip(v, 0, 1) * (0.10 if kind != "toga" else -0.16)                             # folds open out downward (a toga's gather toward the middle)
    uu = (u - 0.5) * spread + 0.5
    f = 0.55 * np.sin(uu * nf * 6.283 + ph[0]) + 0.30 * np.sin(uu * nf * 6.283 * 0.47 + ph[1]) + 0.15 * np.sin(uu * nf * 6.283 * 1.9 + ph[2])
    df = 0.55 * np.cos(uu * nf * 6.283 + ph[0]) + 0.30 * 0.47 * np.cos(uu * nf * 6.283 * 0.47 + ph[1]) + 0.15 * 1.9 * np.cos(uu * nf * 6.283 * 1.9 + ph[2])
    s = np.clip(-df * 0.95, -1, 1) * (0.30 + 0.70 * np.clip(v, 0, 1))                                 # which way each flank of a fold looks: toward the sun or away
    if kind == "toga":
        shape = 0.34 + 0.66 * np.sin(np.pi * np.clip(u, 0, 1)) ** 0.75                                # a great half-round, its curved edge downward
    elif kind == "tunic":
        shape = np.where(np.abs(u - 0.5) < 0.31 + 0.03 * np.clip(v, 0, 1), 1.0, 0.30)                 # hung by the shoulders: sleeves along the line, the body below
    else:
        shape = np.ones(SHAPE, dtype=F32)
    hem = shape * (1 + 0.035 * f * (0.5 if kind == "tunic" else 1.0))                                 # the folds scallop the lower edge
    pinch = 0.022 * np.sin(np.pi * np.clip(v, 0, 1)) if kind != "tunic" else 0.0
    m = band(u, pinch, 1 - pinch, 1 / wd) * band(v, -0.012, hem, 1 / L)
    xw = (PX - cam.vx) / k
    yw = EYE - (PY - cam.vy) / k
    local = np.empty(SHAPE + (3,), dtype=F32)
    local[...] = col(tone)
    if kind == "tunic":
        for uc in (0.37, 0.63):                                                                        # two narrow stripes from shoulder to hem
            over(local, col("#9a3a3a") if tone != "#c75c44" else col("#f0e0c0"), band(u, uc - 0.035, uc + 0.035, 1 / wd) * 0.85)
        neck = np.clip(1 - np.hypot((u - 0.5) / 0.09, v / 0.07), 0, 1)
        local *= (1 - neck * 0.4)[..., None]
    if kind == "toga":                                                                                 # the purple border along the curved edge
        over(local, col("#8a3058"), band(hem - v, -1, 5.0 / length, 1 / L) * band(v, 0.2, 9, 1 / L) * 0.95)
    wob = (noise(SHAPE, 60, seed + 3, 2) - 0.5) * 22
    sun = above(yw, shadow_air(xw) + wob, 7.0)
    tone_sun = ramp((s + 1) / 2, [(0.0, "#bcc0e2"), (0.30, "#e4e1e8"), (0.55, "#fffaf0"), (1.0, "#ffffff")])       # sunlit cloth: warm white, its fold shadows cool
    tone_shade = (0.86 + 0.20 * (s + 1) / 2 + 0.08 * np.clip(s, 0, 1))[..., None]
    sunny = np.clip(local * np.array((1.03, 1.0, 0.96), dtype=F32), 0, 1)
    c = lerp(in_shade(local, "cloth") * tone_shade, sunny * tone_sun, sun[..., None])
    roll = np.clip(1 - np.abs(v - 0.02) / 0.035, 0, 1)                                                 # doubled over the line: a brighter roll along the top
    c = c * (1 + roll * 0.07)[..., None]
    c = c * (1 - 0.10 * np.clip((v - 0.75) * 2, 0, 0.5) * (1 - sun))[..., None]                        # wet cloth is darker toward the hem
    inner = np.minimum(np.minimum(np.roll(m, 1, 0), np.roll(m, -1, 0)), np.minimum(np.roll(m, 1, 1), np.roll(m, -1, 1)))
    rim = np.clip(m - inner, 0, 1) * (m > 0.6)
    c = c * (1 - rim * 0.16)[..., None]                                                                # a firm edge
    if zmid > 900:
        c = lerp(c, col("#b9c2dc"), 0.22)
    return np.clip(c, 0, 1).astype(F32), m.astype(F32)


def laundry_plane(seed=5, items=None, ropes=True):
    """The washing over the street: every line and what hangs on it. -> (color, alpha, lines color, alpha)"""
    color = np.zeros(SHAPE + (3,), dtype=F32)
    alpha = np.zeros(SHAPE, dtype=F32)
    l = Sheet2(SHAPE)
    items = WASH if items is None else items
    for i, item in enumerate(items):
        c, m = cloth(item, seed + 11 * i + (3 if item is TUNIC else 0))
        color = color * (1 - m[..., None]) + c * m[..., None]
        alpha = np.maximum(alpha, m)
    if ropes:
        for name in ROPES:
            pts = [P(*rope_at(name, t)) for t in np.linspace(0, 1, 40)]
            far_one = ROPES[name][0][2] > 900
            for i in range(len(pts) - 1):
                xw, yw, _ = rope_at(name, (i + 0.5) / 39)
                sunny = yw > shadow_air(xw)
                tone = in_sun("#e8d8b0") if sunny else in_shade("#d8c8a8", "cloth") * 0.9
                l.line([pts[i], pts[i + 1]], lerp(tone, col("#b9c2dc"), 0.25) if far_one else tone, 1.5 if far_one else 2.0, 1.0)
        for (t, fc) in ((0.47, 1), (0.52, -1), (0.585, 1)):                                                 # sparrows on the far line
            bx, by, bz = rope_at("far", t)
            px, py = P(bx, by, bz)
            l.ellipse(px, py - 2.6, 3.2, 2.3, "#6a4a34")
            l.ellipse(px + fc * 2.6, py - 4.6, 1.7, 1.6, "#4a3424")
            l.line([(px - fc * 2.5, py - 2.4), (px - fc * 6.0, py - 0.6)], "#4a3424", 1.1)
            l.ellipse(px + fc * 0.6, py - 2.0, 1.6, 1.0, "#c8b090")
    lc, la = l.done()
    return color, alpha, lc, la


def front_plane(seed=5):
    """Right at the front, bottom right: a handcart's wheel leaning on the wall and two wine jars beside it.
    Dark and warm against the cool street, with the sky on their shoulders."""
    s, l = Sheet2(SHAPE), Sheet2(SHAPE)
    cx, cy, r = 750.0, 562.0, 55.0
    wood_d, wood_m, wood_l = in_shade("#7a5636", "deep") * 1.7, in_shade("#a8794a", "front") * 0.92, in_shade("#d8ac74", "warm") * 1.1
    iron, iron_l = in_shade("#4a4650", "front") * 0.8, in_shade("#aab0c8", "up") * 1.2
    # the cart's bed and shaft behind the wheel
    s.poly([(700, 520), (812, 506), (812, 532), (704, 546)], wood_d * 0.9)
    s.poly([(700, 520), (812, 506), (812, 512), (702, 526)], wood_m * 0.9)
    s.line([(706, 532), (640, 470), (628, 462)], wood_d, 5.0)
    s.line([(706, 530), (640, 468), (628, 460)], wood_m, 1.6, 0.9)
    # the wheel: iron tyre, wooden rim, eight spokes, a fat hub
    ring = lambda rr, n=48: [(cx + math.cos(i / n * 2 * math.pi) * rr, cy + math.sin(i / n * 2 * math.pi) * rr) for i in range(n + 1)]
    for i in range(8):
        a = i / 8 * 2 * math.pi + 0.22
        p0, p1 = (cx + math.cos(a) * 9, cy + math.sin(a) * 9), (cx + math.cos(a) * (r - 10), cy + math.sin(a) * (r - 10))
        s.line([p0, p1], wood_d, 6.4)
        l.line([(p0[0] - 1.4, p0[1] - 1.4), (p1[0] - 1.4, p1[1] - 1.4)], wood_l, 1.2, 0.8)
    s.line(ring(r - 1.8), iron, 3.6)
    s.line(ring(r - 8.2), wood_m, 9.6)
    s.poly(ring(11.5), wood_d)
    s.poly(ring(7.0), wood_m)
    s.poly(ring(3.2), iron)
    l.line([(cx + math.cos(a) * (r - 1.0), cy + math.sin(a) * (r - 1.0)) for a in np.linspace(3.5, 5.3, 16)], iron_l, 1.3, 0.9)    # the sky on the tyre
    l.line([(cx + math.cos(a) * (r - 7.5), cy + math.sin(a) * (r - 7.5)) for a in np.linspace(2.9, 4.6, 16)], wood_l, 1.2, 0.8)
    for i in range(6):
        a = i / 6 * 2 * math.pi + 0.5
        l.line([(cx + math.cos(a) * (r - 4), cy + math.sin(a) * (r - 4)), (cx + math.cos(a) * (r - 12), cy + math.sin(a) * (r - 12))], wood_d, 0.8, 0.8)   # joints in the rim
    l.ellipse(cx - 2, cy - 2, 2.2, 2.2, iron_l)
    # two wine jars: one upright against the wheel, one leaning on it
    clay_d, clay_m, clay_l = col("#46283a"), col("#8c5048"), col("#cc9480")
    amphora(s, 664.0, 604.0, 118.0, 0.07, tones=(clay_d, clay_m, clay_l))
    amphora(s, 706.0, 607.0, 104.0, -0.10, tones=(clay_d * 0.92, clay_m * 0.92, clay_l))
    for (ax, ay, h, lean) in ((664.0, 604.0, 118.0, 0.07), (706.0, 607.0, 104.0, -0.10)):
        tx, ty = ax + lean * h, ay - h
        l.line([(tx - h * 0.07, ty - 1), (tx + h * 0.07, ty - 1)], in_shade("#c8d0e8", "up") * 1.3, 1.2, 0.9)                     # the sky on each rim
        l.ellipse(tx, ty - 2.5, h * 0.05, 2.4, in_shade("#b8a888", "up"))                                                     # a stopper of clay
        l.line([(ax + lean * h * 0.62 - h * 0.1, ay - h * 0.62), (ax + lean * h * 0.62 + h * 0.02, ay - h * 0.6)], in_shade("#5a2c2c", "front"), 0.8, 0.7)   # a painted mark
        l.line([(ax + lean * h * 0.55 - h * 0.08, ay - h * 0.55), (ax + lean * h * 0.55 + h * 0.03, ay - h * 0.54)], in_shade("#5a2c2c", "front"), 0.8, 0.6)
    color, alpha = s.done()
    lc, la = l.done()
    return color, alpha, lc, la


def back_solids(info, seed=5):
    """All the built things that belong to the backdrop. -> (faces, lines, shadows cast on sunlit walls)"""
    b, l, cast = Dr(), Dr(), Dr()
    far_dressing(b, l, seed)
    block_things(b, l, seed)
    near_right_things(b, l, seed)
    balcony(b, l, seed)
    left_street_things(b, l, cast, seed)
    front_wall_things(b, l, cast, seed)
    shop_things(b, l, seed)
    street_things(b, l, seed)
    loose_things(b, l, seed)
    basket(b.s, l.s, seed)
    return b.s.done(), l.s.done(), cast.s.done()[1]


# ================================================================ small living things, in picture measurements
def pigeon(s, x, y, size, facing=1, tone="#8d96ac", sun=1.0, kind="front"):
    """A pigeon standing with its feet at (x, y)."""
    body = lit(tone, sun, kind)
    dark, light = body * 0.60, np.clip(body * 1.28, 0, 1)
    s.poly([(x - facing * size * 0.30, y - size * 0.40), (x - facing * size * 0.98, y - size * 0.16), (x - facing * size * 0.34, y - size * 0.14)], dark)       # tail
    s.ellipse(x, y - size * 0.32, size * 0.46, size * 0.27, body)
    s.ellipse(x + facing * size * 0.36, y - size * 0.62, size * 0.16, size * 0.16, dark)                                                               # head
    s.poly([(x + facing * size * 0.24, y - size * 0.52), (x + facing * size * 0.46, y - size * 0.50), (x + facing * size * 0.30, y - size * 0.30)], lit("#7a9a8a", sun, kind))   # the green on its neck
    s.ellipse(x - facing * size * 0.10, y - size * 0.34, size * 0.30, size * 0.16, light)                                                              # wing
    s.line([(x - facing * size * 0.30, y - size * 0.30), (x + facing * size * 0.05, y - size * 0.24)], dark, max(0.7, size * 0.05), 0.9)
    s.line([(x + facing * size * 0.50, y - size * 0.61), (x + facing * size * 0.64, y - size * 0.57)], lit("#d8a060", sun, kind), max(0.7, size * 0.06))
    s.line([(x + facing * size * 0.04, y - size * 0.08), (x + facing * size * 0.04, y)], lit("#c8685a", sun, kind), max(0.7, size * 0.05))
    return s


CAT_TAIL = [(0.26, -0.06), (0.42, 0.12), (0.36, 0.36), (0.44, 0.50)]   # the cat's tail as painted, in her heights from where she sits


def cat_tail(s, x, y, h, kind="warm", bend=None):
    """Her tail, hanging over the edge of the sill (`bend`: another curve than CAT_TAIL, for the game's frames)."""
    ginger = in_shade("#d98a3c", kind) * 1.25
    s.taper(curve([(x + a * h, y + b * h) for a, b in (bend or CAT_TAIL)], 6), ginger, 0.13 * h, 0.08 * h)


def cat(s, x, y, h, kind="warm", tail=True):
    """A ginger-and-white cat sitting on a sill at (x, y), looking down the street to the left; its tail hangs over the edge.
    (`tail` False: without it, for the game's frames of it to swing: round four.)"""
    ginger, white, dark = in_shade("#d98a3c", kind) * 1.25, np.clip(in_shade("#fbf4e6", kind) * 1.2, 0, 1), in_shade("#8a4a24", kind) * 1.1
    if tail:
        cat_tail(s, x, y, h, kind)
    s.poly([(x - 0.30 * h, y), (x + 0.34 * h, y), (x + 0.33 * h, y - 0.34 * h), (x + 0.18 * h, y - 0.62 * h), (x - 0.08 * h, y - 0.68 * h), (x - 0.27 * h, y - 0.42 * h)], ginger)
    s.poly([(x - 0.25 * h, y), (x - 0.02 * h, y), (x - 0.03 * h, y - 0.46 * h), (x - 0.21 * h, y - 0.50 * h)], white)                                 # its white front
    s.poly([(x + 0.12 * h, y), (x + 0.34 * h, y), (x + 0.33 * h, y - 0.30 * h), (x + 0.2 * h, y - 0.36 * h)], dark, 0.5)                              # the haunch, turned from the light
    s.ellipse(x - 0.12 * h, y - 0.79 * h, 0.21 * h, 0.17 * h, ginger)
    s.poly([(x - 0.31 * h, y - 0.86 * h), (x - 0.27 * h, y - 1.04 * h), (x - 0.15 * h, y - 0.93 * h)], ginger)
    s.poly([(x - 0.07 * h, y - 0.94 * h), (x + 0.04 * h, y - 1.04 * h), (x + 0.08 * h, y - 0.84 * h)], ginger)
    s.ellipse(x - 0.18 * h, y - 0.73 * h, 0.10 * h, 0.07 * h, white)
    s.ellipse(x - 0.21 * h, y - 0.82 * h, 0.035 * h, 0.03 * h, "#3a2a1a")
    s.ellipse(x - 0.07 * h, y - 0.82 * h, 0.035 * h, 0.03 * h, "#3a2a1a")
    for i in range(3):                                                                                                                                  # tabby marks
        s.line([(x + (0.06 + i * 0.08) * h, y - (0.56 - i * 0.07) * h), (x + (0.16 + i * 0.07) * h, y - (0.40 - i * 0.08) * h)], dark, max(0.7, 0.04 * h), 0.8)
    return s


def pot_plant(s, x, y, size, seed, bloom="#d8404a", sun=0.0, kind="warm", trail=0.0, tall=1.0):
    """A clay pot standing at (x, y) with something green in it, and a few flowers."""
    rng = np.random.default_rng(seed)
    clay, clay_l = lit("#c8744a", sun, kind), np.clip(lit("#e89a68", sun, kind) * 1.1, 0, 1)
    g0, g1, g2 = lit("#2f5a34", sun, kind), lit("#5f8f46", sun, kind) * 1.1, np.clip(lit("#a8c46a", sun, "up") * 1.2, 0, 1)
    if trail:                                                                                           # something trailing down in front
        for i in range(5):
            px = x + rng.normal(0, size * 0.3)
            pts = [(px, y - size * 0.7)]
            for j in range(int(4 + trail * 5)):
                pts.append((pts[-1][0] + rng.normal(0, size * 0.12), pts[-1][1] + size * 0.32))
            s.line(pts, g0, max(0.7, size * 0.05), 0.9)
            for (qx, qy) in pts[1:]:
                s.ellipse(qx + rng.normal(0, 1), qy, size * 0.13, size * 0.10, g1 if rng.random() < 0.6 else g2)
    s.poly([(x - size * 0.36, y - size * 0.72), (x + size * 0.36, y - size * 0.72), (x + size * 0.26, y), (x - size * 0.26, y)], clay)
    s.poly([(x - size * 0.36, y - size * 0.72), (x - size * 0.10, y - size * 0.72), (x - size * 0.08, y), (x - size * 0.26, y)], clay_l, 0.8)
    s.line([(x - size * 0.40, y - size * 0.72), (x + size * 0.40, y - size * 0.72)], clay_l, max(0.9, size * 0.12))
    for i in range(int(16 * tall)):
        a = rng.random() * math.pi
        r = size * (0.25 + 0.55 * rng.random()) * tall
        px, py = x + math.cos(a) * r * 0.8, y - size * 0.8 - math.sin(a) * r
        s.ellipse(px, py, size * (0.14 + 0.1 * rng.random()), size * (0.10 + 0.08 * rng.random()), (g0, g1, g1, g2)[int(rng.integers(4))])
    if bloom:
        for i in range(5):
            a = rng.random() * math.pi
            r = size * (0.4 + 0.5 * rng.random()) * tall
            s.ellipse(x + math.cos(a) * r * 0.8, y - size * 0.85 - math.sin(a) * r, max(0.8, size * 0.09), max(0.8, size * 0.08), lit(bloom, max(sun, 0.25), kind))
    return s


def crack(l, to3, u0, y0, length, seed, tone, lean=0.0, wd=0.8, a=0.7):
    """A crack running down a wall from (u0, y0), in the wall's own measurements; `to3` puts it in the world."""
    rng = np.random.default_rng(seed)
    pts = [(u0, y0)]
    n = int(length / 13) + 2
    for i in range(n):
        pts.append((pts[-1][0] + rng.normal(lean * 13, 4.5), pts[-1][1] - 13 * (0.5 + rng.random())))
    l.line([to3(u, v) for u, v in pts], tone, wd, a)
    if n > 3:
        j = int(rng.integers(1, n - 1))
        br = [pts[j]]
        for i in range(2 + int(rng.integers(3))):
            br.append((br[-1][0] + rng.normal(8, 3) * (1 if rng.random() < 0.5 else -1), br[-1][1] - 8 * rng.random() - 3))
        l.line([to3(u, v) for u, v in br], tone, wd * 0.8, a * 0.8)
    return pts


def shrine(b, l, seed=0, flame=True):
    """The crossroads shrine on the corner pier: a little arched niche with a lamp burning in it, and below it,
    painted on a white ground, a crested snake gliding up through leaves toward an altar."""
    z = ZF - 0.5
    x0, x1, y0, y1 = -305.0, -257.0, 126.0, 250.0
    sh = lambda c, d=1.0: in_shade(c, "front") * d
    b.front(x0, x1, y0, y1, z, sh("#f1e6cc", 1.04))
    for (a, c) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        l.line([(a[0], a[1], z), (c[0], c[1], z)], sh("#a8322c", 1.1), 1.2, 0.9)
    l.line([(x0 + 3, 182, z), (x1 - 3, 182, z)], sh("#a8322c", 1.1), 0.8, 0.8)
    # the niche: an arched recess, dark, with a lamp
    nx0, nx1, ny0, ny1 = -293.0, -269.0, 194.0, 232.0
    arch = [(nx0, ny0, z), (nx1, ny0, z), (nx1, ny1, z)] + [((nx0 + nx1) / 2 + math.cos(a) * 12, ny1 + math.sin(a) * 10, z) for a in np.linspace(0, math.pi, 8)] + [(nx0, ny1, z)]
    b.poly(arch, in_shade("#4a3440", "deep") * 1.2)
    b.poly([(nx0, ny0, z), (nx0 + 5, ny0, z), (nx0 + 5, ny1 + 6, z), (nx0, ny1, z)], sh("#d8c8a8", 0.9))                  # the cheek of the niche that we see
    b.front(nx0 - 2, nx1 + 2, ny0 - 3, ny0, z - 2, sh("#d8ccb4", 1.15))                                                 # its little shelf
    lx, ly = P(-279.0, ny0, z - 1)
    l.s.poly([(lx - 4.0, ly), (lx + 3.0, ly), (lx + 4.6, ly - 2.4), (lx - 4.4, ly - 2.6)], sh("#c8744a", 1.2))             # the lamp
    if flame:
        l.s.ellipse(lx + 5.0, ly - 4.6, 1.3, 2.4, "#ffb040")                                                           # and its flame
        l.s.ellipse(lx + 5.0, ly - 4.2, 0.7, 1.3, "#fff4b0")
    # the painted snake
    snake = []
    for t in np.linspace(0, 1, 26):
        snake.append((x0 + 5 + 30 * t, 134 + 20 * t ** 1.3 + 6.5 * math.sin(t * 4.2 * math.pi) * (1 - 0.5 * t), z))
    l.line(snake, sh("#5a4a20", 1.0), 3.0, 0.95)
    l.line(snake, sh("#d8b83a", 1.25), 1.7, 1.0)
    hx, hy = P(*snake[-1])
    l.s.ellipse(hx + 1.0, hy - 0.6, 2.2, 1.6, sh("#d8b83a", 1.25))
    l.s.line([(hx, hy - 2), (hx + 1.5, hy - 4.2), (hx + 2.6, hy - 2.2)], sh("#c8382c", 1.3), 0.9)                          # crest
    l.s.line([(hx + 3, hy - 0.4), (hx + 5.4, hy - 1.4)], sh("#c8382c", 1.3), 0.6)                                         # tongue
    rng = np.random.default_rng(seed + 3)
    for i in range(12):                                                                                                 # leaves about it
        px, py = P(x0 + 5 + rng.random() * 38, 131 + rng.random() * 44, z)
        l.s.line([(px, py), (px + rng.normal(0, 2.0), py - 2.5 - rng.random() * 2)], sh("#5a8a4a", 1.15), 1.0, 0.85)
    ax, ay = P(x1 - 9.0, 160.0, z)
    l.s.poly([(ax - 2.6, ay), (ax + 2.6, ay), (ax + 2.0, ay - 5), (ax - 2.0, ay - 5)], sh("#c8a888", 1.1))                 # the little altar it comes to
    l.s.ellipse(ax, ay - 6.2, 1.5, 1.4, sh("#f0e8d0", 1.2))                                                             # with an egg on it
    return


def price_list(b, l, seed=0):
    """The price list painted on the pier at the left of the counter: a white panel of scribbled lines, each
    ending in a few strokes for the price."""
    z = ZF - 0.5
    x0, x1, y0, y1 = -599.0, -534.0, 136.0, 238.0
    sh = lambda c, d=1.0: in_shade(c, "front") * d
    b.front(x0, x1, y0, y1, z, sh("#f3e9d2", 1.04))
    for (a, c) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1))):
        l.line([(a[0], a[1], z), (c[0], c[1], z)], sh("#7a2a28", 1.1), 1.0, 0.85)
    rng = np.random.default_rng(seed + 9)
    for i, yy in enumerate(np.arange(y1 - 14, y0 + 6, -13.5)):
        xx = x0 + 5
        end = x1 - 20 - rng.random() * 8
        pts = [(xx, yy, z)]
        while xx < end:                                                                                                 # a word, more or less
            xx += 2.2 + rng.random() * 2.6
            pts.append((xx, yy + rng.normal(0, 2.4), z))
            if rng.random() < 0.2:
                l.line(pts, sh("#8a2a2a" if i else "#3a2a30", 1.05), 0.8, 0.9)
                xx += 4
                pts = [(xx, yy, z)]
        if len(pts) > 1:
            l.line(pts, sh("#8a2a2a" if i else "#3a2a30", 1.05), 0.8, 0.9)
        for j in range(1 + int(rng.integers(4))):                                                                       # the price: I, II, III, IIII
            px = x1 - 15 + j * 3.4
            l.line([(px, yy - 3.6, z), (px + 0.3, yy + 3.6, z)], sh("#3a2a30", 1.0), 0.8, 0.95)
    return


def details(pic, base, info, solids, seed=5, moving=None):
    """Over the brushwork: say every built edge again, then the small crisp things: joints in the paving, tiles,
    cracks and patches, lettering, the shrine and the price list, pots, the cat, pigeons.
    `moving`: paint in what moves by nature too, still, as before round four (PAINT_MOVING if not said)."""
    moving = PAINT_MOVING if moving is None else moving
    shape = SHAPE
    (bc, ba), (lc, la), cast = solids
    rng = np.random.default_rng(seed + 77)

    # ---- 1. the hard edges of everything built, restated from the block-in
    lum = base @ np.array([0.3, 0.55, 0.15], dtype=F32)
    gy, gx = np.gradient(blur(lum, 0.5))
    edge = step(0.018, 0.06, np.hypot(gx, gy))
    edge = np.clip(blur(edge, 0.9) * 1.7, 0, 1) * info["built"]
    pic[...] = lerp(pic, base, (edge * 0.82)[..., None])
    crisp = pic.copy()
    far_temple(crisp, seed)
    pic[...] = lerp(pic, crisp, 0.85)
    put(pic, (bc, ba), 0.72, wobble=0.5, seed=3)

    # ---- 2. the roadway: each stone's shoulders, the joints, the ruts carts have worn, wet places
    st = info["paving"]
    xf, zf, kf = info["xf"], info["zf"], info["kf"]
    open_ground = (1 - info["walls"]) * (1 - np.clip(ba * 1.5, 0, 1))                                      # the ground we can see: not where a house or a thing stands in front of it
    road = info["road"].astype(F32) * open_ground
    shade_only = road * (1 - info["sun_floor"])
    near = np.clip(1.5 - zf / 1400.0, 0.15, 1)
    pit = wn(xf, zf, 9, seed + 30, 3)                                                                      # basalt is pitted
    tint(pic, "#7a7090", (step(0.62, 0.86, pit) * 0.22 * shade_only * near).astype(F32))
    tint(pic, "#766c8e", (st["wide"] * (st["gx"] > 0) * 0.22 * shade_only * near).astype(F32))             # the side of each stone turned from the sunny wall
    glow(pic, "#8f88b4", (st["wide"] * (st["gx"] < 0) * 0.14 * shade_only * near).astype(F32))             # and the side turned to it
    glow(pic, "#7088c0", (st["crown"] ** 2 * 0.22 * shade_only * near).astype(F32))                        # the polished crown
    earth = 0.45 + 0.55 * wn(xf, zf, 40, seed + 31, 3)
    over(pic, in_shade("#3c3040", "deep") * 1.2, (np.clip(st["joint"] * 1.15, 0, 1) * 0.92 * road * earth * (1 - info["sun_floor"] * 0.5)).astype(F32))
    lip = band(st["edge"], 2.6 + st["r2"] * 1.9, 4.6 + st["r2"] * 1.9, st["foot"]) * (st["gy"] > 0) * st["seen"]      # the arris of the stone beyond each joint
    glow(pic, "#98a2d4", (lip * 0.30 * shade_only * near * (0.4 + 0.6 * wn(xf, zf, 50, seed + 36, 2))).astype(F32))
    moss = step(0.60, 0.80, wn(xf, zf, 110, seed + 32, 3)) * np.clip(info["wet"] * 1.6, 0, 1)             # green in the joints where it is wet
    over(pic, in_shade("#6f9a52", "up") * 1.15, (st["joint"] * moss * 0.8 * road).astype(F32))
    # ruts: one pair straight up the street between the stepping stones, one pair turning off into the side street
    for sx in (-55.0, 55.0):
        wander = (wn(zf * 0.2, zf * 0.2, 300, seed + 33, 2) - 0.5) * 12
        straight = np.clip(1 - np.abs(xf - sx - wander) / 9.0, 0, 1) * np.clip((zf - 240) / 200.0, 0, 1)
        turn_x = sx - (np.clip(430 - zf, 0, 600) / 62.0) ** 2 * 9.0
        turning = np.clip(1 - np.abs(xf - turn_x) / (9.0 + np.clip(300 - zf, 0, 300) * 0.03), 0, 1) * np.clip((560 - zf) / 100.0, 0, 1)
        for rut in (straight, turning):
            tint(pic, "#6c6288", (smooth(rut * 1.5) * 0.34 * shade_only * near).astype(F32))
            glow(pic, "#8c9cd0", (np.clip(rut * 2.5 - 1.6, 0, 1) * 0.16 * shade_only * near).astype(F32))
    # a drain cover: a worn slab let into the paving, pierced with three holes, where the side street's gutter goes under
    dx0, dx1, dz0, dz1 = -366.0, -310.0, 46.0, 100.0
    dfoot = np.maximum(st["foot"], 0.6)
    skew = (zf - 73.0) * 0.12
    cover = band(xf + skew, dx0, dx1, 1 / kf) * band(zf, dz0, dz1, dfoot) * road * step(0.16, 0.24, wn(xf, zf, 46, seed + 38, 2) + np.clip((xf - dx0) / 30.0, 0, 1))
    slab = in_shade(vary("#a39c98", shape, seed + 37, 0.12, 7), "up") * 1.08
    over(pic, slab, (cover * 0.95).astype(F32))
    rim = np.clip(band(xf + skew, dx0 - 3, dx1 + 3, 1 / kf) * band(zf, dz0 - 3, dz1 + 3, dfoot) * road - cover, 0, 1)
    over(pic, in_shade("#2c2630", "deep"), (rim * 0.8).astype(F32))
    for (hx_, hz_, hr_) in ((-350.0, 62.0, 4.4), (-326.0, 68.0, 5.0), (-340.0, 86.0, 4.6)):
        hole = np.clip((hr_ - np.hypot(xf - hx_, (zf - hz_) * 0.9)) / np.maximum(1 / kf, 0.6) + 0.5, 0, 1) * road
        over(pic, in_shade("#141018", "deep"), hole.astype(F32))
        glow(pic, "#aab4e0", (np.clip(np.roll(hole, 1, axis=0) - hole, 0, 1) * 0.4).astype(F32))
    # wet places give back the sky in short level glints
    spark = step(0.76, 0.92, noise(shape, (30, 2.4), seed + 34, 2))
    glow(pic, "#a4bcf0", (spark * info["wet"] * 0.42 * shade_only).astype(F32))
    glow(pic, "#a4bcf0", (spark * info["wet_s"] * 0.50 * info["sidewalk"] * open_ground).astype(F32))
    # the puddles again, crisp: bright water, a dark wet rim, a light where the far edge is
    pud = info["pud"] * road
    wide_p = np.clip(blur(pud, 1.6) * 1.8, 0, 1)
    tint(pic, "#6a6488", ((wide_p - pud).clip(0, 1) * 0.6).astype(F32))
    over(pic, info["mirror"], (pud * 0.86).astype(F32))
    far_edge = np.clip(pud - np.roll(pud, 1, axis=0), 0, 1)
    glow(pic, "#dfe8ff", (far_edge * 0.6).astype(F32))
    # far off, where the sun crosses the street, the stones are warm
    glow(pic, "#ffe8b0", (info["sun_floor"] * road * 0.10).astype(F32))

    # ---- 3. the sidewalks: flags on the right, kerbstones, grit
    xs, zs, ks = info["xs"], info["zs"], info["ks"]
    walk = info["sidewalk"].astype(F32) * open_ground
    dzs = (Z0 + np.maximum(zs, -40)) ** 2 / (EYE * F)
    foot_s = np.maximum(dzs * 0.42, 1 / ks)
    seen_s = np.clip(3.4 / np.maximum(dzs, 0.1), 0, 1) ** 0.6
    flagj = np.clip((1.6 - info["slab_e"]) / foot_s + 0.5, 0, 1) * seen_s * info["flags"]
    over(pic, in_shade("#4a4048", "deep") * 1.3, (flagj * 0.7 * walk).astype(F32))
    cobj = np.clip((1.3 - info["cob_e"]) / foot_s + 0.5, 0, 1) * seen_s * info["cobbles"]
    over(pic, in_shade("#4a4048", "deep") * 1.4, (cobj * 0.5 * walk).astype(F32))
    grit = Sheet2(shape)
    for i in range(300):                                                                                    # grit, potsherds, pebbles trodden into the earth
        zz = -20 + rng.random() ** 1.7 * 1500
        if rng.random() < 0.55:
            xx = KR + 6 + rng.random() * (WR - KR - 10)
        else:
            xx = KL - 6 - rng.random() * 380 if zz < ZF else KL - 6 - rng.random() * 90
            if zz < ZK + 4:
                continue
        px, py = P(xx, SWH, zz)
        k = kz(zz)
        r = (0.6 + rng.random() ** 2 * 2.2) * k
        tone = (in_shade("#d8c8b0", "up") * 1.05, in_shade("#7a6a70", "up") * 0.85, in_shade("#c8744a", "up"), in_shade("#e8dcc8", "up") * 1.1, in_shade("#7a6a70", "up") * 0.8)[int(rng.integers(5))]
        grit.ellipse(px, py, max(0.6, r * 1.4), max(0.5, r * 0.7), tone, 0.55)
    put(pic, grit)
    kb = Dr()
    up_l = np.clip(in_shade(KERB, "up") * 1.35, 0, 1)
    kerb = info["kerb"].astype(F32) * open_ground
    beside = np.clip(np.roll(kerb, 1, 0) + np.roll(kerb, -1, 0) + np.roll(kerb, 1, 1) + np.roll(kerb, -1, 1), 0, 1)
    fade_k = np.clip(1.5 - zs / 1500.0, 0.25, 1)
    glow(pic, "#aab2e0", (beside * walk * 0.34 * fade_k).astype(F32))                                    # the kerbs' top edges catch the sky
    tint(pic, "#584e70", (beside * road * 0.60 * fade_k).astype(F32))                                    # and their feet are dark
    for n in range(0, 23):                                                                                  # the joints between kerbstones, where they really are
        a = 0.7 * np.clip(1.4 - n * 118 / 1500.0, 0.2, 1)
        zz = (n - 0.37) * 118.0
        kb.line([(KR, 0, zz), (KR, SWH, zz), (KR + 32, SWH, zz + rng.normal(0, 3))], in_shade("#3c3440", "deep") * 1.2, 0.8, a)
        zz = n * 118.0
        if zz > ZK + 10:
            kb.line([(KL, 0, zz), (KL, SWH, zz), (KL - 32, SWH, zz + rng.normal(0, 3))], in_shade("#3c3440", "deep") * 1.2, 0.8, a)
    for n in range(-6, -1):
        xj = n * 104.0
        kb.line([(xj, 0, ZK), (xj, SWH, ZK), (xj + rng.normal(0, 3), SWH, ZK + 32)], in_shade("#3c3440", "deep") * 1.2, 0.8, 0.7)
    spill = [(FOUNT["x0"] - 2 - t * 76 + math.sin(t * 9) * 3, SWH + 0.3, 298 + t * 14 + math.sin(t * 5) * 5) for t in np.linspace(0, 1, 12)]
    kb.line([(a_, b_, c_ + 3) for a_, b_, c_ in spill], in_shade("#3a3444", "deep") * 1.2, 2.6, 0.45)        # what spills from the basin runs across the sidewalk to the gutter
    if moving:                                                                                              # (the light on the running water: the game's now)
        kb.line(spill, "#a8c0f0", 1.2, 0.85)
        kb.line([(KR, SWH - 2, 312), (KR, 2, 314)], "#9ab4ea", 1.0, 0.6)
    for i in range(40):                                                                                     # the trickle in the right-hand gutter, running away from the fountain
        zz = 300 + i * 34.0 + rng.random() * 14
        if rng.random() < 0.72:
            trickle = [(KR - 8 - rng.random() * 6, 0.3, zz), (KR - 8 - rng.random() * 6, 0.3, zz + 16 + rng.random() * 22)]     # (drawn or not, the same dice)
            if moving:
                kb.line(trickle, "#a8c0ee", 0.9, 0.5 * np.clip(1.5 - zz / 1300.0, 0.25, 1))
    put(pic, kb.s)

    # ---- 4. walls: where plaster has fallen, its broken edge; cracks; runs of dirt; painted lines
    for patch in (info["patch_r"], info["quoin"]):
        lower = np.clip(patch - np.roll(np.roll(patch, 1, axis=0), 1, axis=1), 0, 1)                        # the plaster's thickness throws a line of shade into each hole
        upper = np.clip(np.roll(np.roll(patch, 1, axis=0), 1, axis=1) - patch, 0, 1)
        tint(pic, "#5a4a66", (lower * 0.65).astype(F32))
        glow(pic, "#b8a8c0", (upper * 0.22).astype(F32))
    w = Dr()
    R = lambda u, v: (WR - 0.5, v, u)
    Lw = lambda u, v: (WL + 0.5, v, u)
    Fw = lambda u, v: (u, v, ZF - 0.5)
    dark_r, dark_f = in_shade("#4a3440", "warm") * 0.9, in_shade("#4a3440", "front") * 0.9
    for i, (u0, y0, ln, lean) in enumerate(((60.0, 346.0, 150.0, 0.2), (212.0, 330.0, 110.0, -0.3), (590.0, 346.0, 190.0, 0.15), (700.0, 640.0, 240.0, -0.1), (-20.0, 300.0, 120.0, 0.3),
                                              (900.0, 640.0, 200.0, 0.2), (1180.0, 940.0, 230.0, 0.0), (1500.0, 420.0, 160.0, 0.3), (380.0, 640.0, 120.0, 0.25))):
        crack(w, R, u0, y0, ln, seed + 40 + i, dark_r, lean)
    sun_dark = lit("#8a5a3a", 1.0, "front") * 0.82
    for i, (u0, y0, ln, lean, sunny) in enumerate(((-560.0, 636.0, 130.0, 0.2, 1), (-350.0, 620.0, 150.0, -0.25, 1), (-292.0, 440.0, 90.0, 0.1, 1), (-585.0, 300.0, 120.0, 0.1, 0), (-270.0, 126.0, 70.0, 0.2, 0))):
        crack(w, Fw, u0, y0, ln, seed + 60 + i, sun_dark if sunny else dark_f, lean)
    for i, (u0, y0, ln, lean, sunny) in enumerate(((420.0, 630.0, 160.0, 0.3, 1), (700.0, 452.0, 60.0, 0.4, 1), (880.0, 640.0, 180.0, 0.2, 1), (1400.0, 700.0, 200.0, 0.3, 0), (560.0, 380.0, 150.0, 0.2, 0))):
        crack(w, Lw, u0, y0, ln, seed + 70 + i, sun_dark if sunny else dark_f, lean)
    # runs of dirt under sills and beam ends (thin, upright, faint)
    for (u0, y0, ln) in ((-476.0, 440.0, 60.0), (-386.0, 440.0, 46.0), (-430.0, 440.0, 30.0)):
        w.line([Fw(u0, y0), Fw(u0 + 2, y0 - ln)], lit("#9a7a4a", 1.0, "front"), 1.6, 0.30)
    for zz in (48.0, 120.0, 250.0, 330.0, 480.0, 600.0):
        w.line([R(zz, 446.0 if zz < 140 else 330.0), R(zz + 3, (446.0 if zz < 140 else 330.0) - 50 - rng.random() * 50)], in_shade("#5a4450", "warm"), 1.4, 0.30)
    # the painted line along the top of each dado, and the edge of the whitewash
    w.line([R(-60.0, 119.0), R(718.0, 119.0)], in_shade("#f0e4c8", "warm") * 1.1, 0.8, 0.55)
    w.line([R(-60.0, 123.0), R(718.0, 123.0)], in_shade("#3a2a30", "warm"), 0.7, 0.5)
    w.line([R(-60.0, 346.0), R(718.0, 346.0)], in_shade("#7a3a34", "warm"), 0.9, 0.6)
    w.line([Lw(ZF, 123.0), Lw(928.0, 123.0)], in_shade("#f0e4c8", "front") * 1.1, 0.8, 0.5)
    for (xa, xb) in ((-700.0, SHOP["x0"]), (SHOP["x1"], WL)):
        w.line([Fw(xa, 125.0), Fw(xb, 125.0)], in_shade("#f0e4c8", "front") * 1.1, 0.8, 0.55)
    # the corners of the houses, firm
    w.line([(WL, SWH, ZF), (WL, 300, ZF)], in_shade("#f0dcb4", "front") * 1.15, 1.0, 0.7)
    w.line([(WL, 400, ZF), (WL, L1["h"], ZF)], in_sun("#fff0cc"), 1.0, 0.75)
    w.line([(WR, SWH, RB["z0"]), (WR, 700, RB["z0"])], in_shade("#3a2a34", "warm"), 1.0, 0.6)
    w.line([(WR, SWH, RC["z0"]), (WR, RC["h"], RC["z0"])], in_shade("#3a2a34", "warm") * 1.3, 0.9, 0.5)
    w.line([(WL, SWH, L2["z0"]), (WL, L2["h"], L2["z0"])], in_shade("#4a3a44", "front") * 1.3, 0.9, 0.5)
    # scratched scribbles: a tally, a little ship, somebody's stick man
    sc = np.clip(in_shade("#f4e4c8", "warm") * 1.25, 0, 1)
    for j in range(7):
        w.line([R(214.0 - j * 6, 96.0), R(213.0 - j * 6, 80.0)], sc, 0.7, 0.8)
    w.line([R(220.0, 82.0), R(172.0, 94.0)], sc, 0.7, 0.8)
    w.line([R(150.0, 78.0), R(140.0, 70.0), R(112.0, 70.0), R(104.0, 80.0), R(150.0, 78.0)], sc, 0.7, 0.8)      # the ship: hull,
    w.line([R(128.0, 71.0), R(128.0, 100.0)], sc, 0.7, 0.8)                                                      # mast,
    w.line([R(128.0, 98.0), R(112.0, 84.0), R(128.0, 82.0)], sc, 0.7, 0.8)                                       # sail
    w.line([R(60.0, 92.0), R(60.0, 76.0), R(66.0, 62.0)], sc, 0.7, 0.8)                                          # the stick man
    w.line([R(60.0, 76.0), R(54.0, 62.0)], sc, 0.7, 0.8)
    w.line([R(68.0, 86.0), R(52.0, 86.0)], sc, 0.7, 0.8)
    cx, cy = P(*R(60.0, 97.0))
    w.s.ellipse(cx, cy, 2.2, 2.6, sc, 0.8)
    sc2 = np.clip(in_shade("#f4e4c8", "front") * 1.2, 0, 1)
    for j in range(5):
        w.line([Fw(-296.0 + j * 5, 100.0), Fw(-297.0 + j * 5, 86.0)], sc2, 0.7, 0.8)
    put(pic, w.s)

    # ---- 5. lettering: election notices in red on the whitewashed bands
    xw, yw, kw, sunf = info["xw"], info["yw"], info["kw"], info["sun_front"]

    def front_words(words, x_mid, y_mid, cap, tone, hand=True, squash=1.0, sd=0, amount=0.92, spacing=0):
        cx_, cy_ = P(x_mid, y_mid, ZF)
        m = letter.mask(shape, words, (cx_, cy_), cap * kw / 0.72, hand=hand, anchor="mm", rough=0.6, squash=squash, seed=sd, spacing=spacing)
        wear = (0.66 + 0.34 * step(0.22, 0.55, wn(xw, yw, 10, seed + sd + 1, 3))) * (1 - 0.45 * step(0.74, 0.86, wn(xw, yw, 70, seed + sd + 2, 3)))
        local = np.empty(shape + (3,), dtype=F32)
        local[...] = col(tone)
        over(pic, light(local, sunf, "front"), (m * wear * amount * info["mf"]).astype(F32))
    front_words("MARCVS", -470.0, 386.0, 43.0, "#b3282a", sd=1, spacing=1)
    front_words("VOTA", -302.0, 384.0, 30.0, "#b3282a", sd=2)

    zr, yr, kr = info["zr"], info["yr"], info["kr"]

    def right_words(words, z_far, y_mid, cap, tone, hand=True, sd=0, amount=0.9):
        res = 2.0                                                                                           # the lettering is set flat, 2 pixels to the centimetre, then laid along the wall
        m, (wd_, ht_) = words_flat(words, cap * res / 0.72, hand=hand, seed=sd)
        u = (z_far - zr) * res
        v = (y_mid - yr) * res + ht_ / 2
        inside = (u > 0) & (u < wd_ - 1) & (v > 0) & (v < ht_ - 1)
        mm = sample(blur(m, 0.6), np.clip(u, 0, wd_ - 1.01), np.clip(v, 0, ht_ - 1.01)) * inside
        wear = (0.50 + 0.50 * step(0.22, 0.55, wn(zr, yr, 10, seed + sd + 1, 3))) * (1 - 0.7 * step(0.72, 0.84, wn(zr, yr, 70, seed + sd + 2, 3)))
        over(pic, in_shade(tone, "warm"), (mm * wear * amount * info["m_RA"]).astype(F32))
    right_words("RVFVS", 172.0, 218.0, 46.0, "#b3282a", sd=4)
    right_words("FELIX", 150.0, 164.0, 20.0, "#4a3038", hand=False, sd=5, amount=0.8)
    right_words("VOTA", 440.0, 260.0, 34.0, "#b3282a", sd=6, amount=0.8)

    # ---- 6. the corner house's roof: lines of curved tiles, the eave, the ridge, pigeons
    xt, zt, kt, mroof, ra, rb = info["roof"]
    rp = lambda xx, zz: (xx, ra + rb * zz, zz)
    r = Dr()
    tile_l, tile_d = in_sun("#f6a468"), in_sun(TILE) * 0.62
    rows = list(np.arange(ZF - 40, L1["zr"] + 1, 52.0))
    for n in range(-15, -4):
        x0 = n * 46.0
        for j in range(len(rows) - 1):                                                                      # tile by tile, none quite in line with the next
            jx = rng.normal(0, 1.3)
            za_, zb_ = rows[j], rows[j + 1]
            if x0 + 15 < WL + 40:
                r.line([rp(x0 + 15 + jx, za_), rp(x0 + 15 + jx, zb_)], tile_d, 0.9, 0.55 + 0.3 * rng.random())
            if x0 + 28 < WL + 40:
                r.line([rp(x0 + 28 + jx, za_), rp(x0 + 28 + jx, zb_)], tile_l, 0.8, 0.4 + 0.35 * rng.random())
                if rng.random() < 0.06:                                                                     # one has slipped, and shows the dark under it
                    r.poly([rp(x0 + 6, za_ + 6), rp(x0 + 40, za_ + 6), rp(x0 + 40, za_ + 30), rp(x0 + 6, za_ + 30)], in_sun(TILE) * 0.42, 0.8)
            r.line([rp(x0 + 3, zb_ + rng.normal(0, 2)), rp(x0 + 44, zb_ + rng.normal(0, 2))], tile_d, 0.7, 0.25 + 0.3 * rng.random())
        if x0 + 28 < WL + 40:
            ex, ey = P(*rp(x0 + 25, ZF - 40))
            r.s.ellipse(ex, ey + 0.6, 2.4, 1.8, in_sun("#e88a54"))                                          # the end of each cover tile, at the eave
            r.s.ellipse(ex - 0.5, ey + 1.0, 1.1, 0.9, in_sun(TILE) * 0.5)
    for i in range(16):                                                                                     # lichen, yellow-grey, in the sun
        lx_, lz_ = -640 + rng.random() * 420, ZF + rng.random() * 280
        px_, py_ = P(*rp(lx_, lz_))
        r.s.ellipse(px_, py_, 1.5 + rng.random() * 2.5, 0.7 + rng.random() * 0.9, in_sun("#d8cc8a"), 0.55)
    r.line([rp(-700.0, L1["zr"]), rp(WL + 40, L1["zr"])], in_sun("#f8b078"), 2.0, 0.95)                    # the ridge
    r.line([(-700.0, L1["ridge"] - 5, L1["zr"]), (WL + 40, L1["ridge"] - 5, L1["zr"])], tile_d, 0.8, 0.6)
    for xx in np.arange(-690.0, WL + 40, 40.0):
        r.line([(xx, L1["ridge"] + 3, L1["zr"]), (xx, L1["ridge"] - 5, L1["zr"])], tile_d, 0.7, 0.55)
    r.line([(-700.0, L1["h"] - 8, ZF - 40), (WL + 40, L1["h"] - 8, ZF - 40)], in_shade("#4a2a24", "deep") * 1.4, 1.2, 0.85)   # under the eave it is dark
    put(pic, r.s)
    birds = Sheet2(shape)
    kk = kz(L1["zr"])
    if moving:
        for (xx, fc, tone) in RIDGE_PIGEONS:
            bx, by = P(xx, L1["ridge"] + 3, L1["zr"])
            pigeon(birds, bx, by, 34 * kk, fc, tone, sun=1.0)
        bx, by = P(BALC["x"] - 22, BALC["top"] + 14, 300.0)
        pigeon(birds, bx, by, 30 * kz(300.0), -1, "#8d96ac", sun=0.0, kind="warm")
        for (sx, sy, sz) in SWALLOWS:                                                                       # swallows, high up
            birds.line([(sx - sz, sy - sz * 0.5), (sx, sy), (sx + sz, sy - sz * 0.6)], "#1c2a4a", 0.9, 0.85)

    # ---- 7. pots of flowers, the cat on her sill
    k1 = kz(85.0)
    cx, cy = P(WR - 7, 455.0, 96.0)
    cat(birds, cx, cy, 36 * k1, tail=moving)
    # what she is watching: a songbird in a wicker cage, hung from the balcony's beam
    gz = 246.0
    gk = kz(gz)
    gx, gy = P(BALC["x"] - 4, BALC["top"] - 8, gz)
    wick, wick_l = in_shade("#b08a52", "warm") * 1.05, np.clip(in_shade("#e8c488", "warm") * 1.25, 0, 1)
    birds.line([(gx, gy), (gx, gy + 12 * gk)], in_shade("#3a3038", "front"), 0.8)
    top, bot, r_ = gy + 12 * gk, gy + 52 * gk, 13 * gk
    birds.ellipse(gx, (top + bot) / 2 + 2, r_ * 0.9, (bot - top) / 2, in_shade(ROOM, "deep") * 1.2, 0.55)                    # the dark inside it
    birds.ellipse(gx + 1.5, bot - 8 * gk, 3.4 * gk, 2.6 * gk, "#e8c838")                                                  # the bird: yellow,
    birds.ellipse(gx - 1.0 * gk, bot - 11.5 * gk, 2.0 * gk, 1.9 * gk, "#f0d850")
    birds.line([(gx - 3.2 * gk, bot - 11.5 * gk), (gx - 5.2 * gk, bot - 11 * gk)], "#d87830", 0.7)
    for i in range(7):                                                                                                    # the bars, bent over to a point
        u = (i - 3) / 3.0
        birds.line([(gx, top), (gx + u * r_ * 0.8, top + 9 * gk), (gx + u * r_, top + 20 * gk), (gx + u * r_, bot)], wick_l if i in (1, 2) else wick, 0.7, 0.9)
    for yy in (top + 20 * gk, bot):
        birds.line([(gx - r_, yy), (gx + r_, yy)], wick, 1.0)
    for i, (zz, bloom) in enumerate(((212.0, "#d8404a"), (284.0, "#f0d860"), (408.0, "#e88ab0"), (560.0, "#d8404a"))):
        px, py = P(BALC["x"] - 2, BALC["rail"] + 1, zz)
        pot_plant(birds, px, py, 24 * kz(zz), seed + i, bloom=bloom, trail=0.8 if i == 1 else 0.0)
    px, py = P(-392.0, 453.0, ZF - 8)
    pot_plant(birds, px, py, 22 * kw, seed + 9, bloom="#e86a8a", sun=1.0, kind="front")
    px, py = P(WR - 16, SWH, 432.0)
    pot_plant(birds, px, py, 40 * kz(432.0), seed + 11, bloom=None, tall=1.5)
    px, py = P(WR - 40, 652.0 + 96, 1040.0)
    pot_plant(birds, px, py, 24 * kz(1040.0), seed + 12, bloom="#e8a0b8")
    put(pic, birds)

    # ---- 8. the lines of everything built
    put(pic, (lc, la))

    # ---- 9. the shrine and the price list on the snack bar's piers
    sb, sl = Dr(), Dr()
    shrine(sb, sl, seed, flame=moving)
    price_list(sb, sl, seed)
    put(pic, sb.s, wobble=0.4, seed=8)
    put(pic, sl.s)

    # ---- 10. what people have dropped: leaves in the gutter, straw, a broken pot
    lit_ = Sheet2(shape)
    for i in range(46):
        zz = 180 + rng.random() ** 1.5 * 700
        side = -1 if rng.random() < 0.6 else 1
        xx = side * (KR - 4 - rng.random() ** 2 * 36) if zz > ZK + 10 else -150 - rng.random() * 400
        zz = zz if zz > ZK + 10 else ZK - 6 - rng.random() ** 2 * 30
        px, py = P(xx, 0, zz)
        k = kz(zz)
        what = rng.random()
        if what < 0.45:                                                                                     # straw
            a = rng.random() * math.pi
            lit_.line([(px, py), (px + math.cos(a) * 9 * k, py - math.sin(a) * 3 * k)], in_shade("#e8d080", "up") * 1.2, 0.7, 0.85)
        elif what < 0.8:                                                                                    # a cabbage leaf
            lit_.ellipse(px, py, 4.2 * k, 1.9 * k, in_shade("#7fa85a", "up") * 1.15, 0.9)
            lit_.line([(px - 3 * k, py), (px + 3 * k, py - 0.4)], in_shade("#c8dc98", "up") * 1.2, 0.6, 0.8)
        else:                                                                                               # a sherd
            lit_.poly([(px - 3 * k, py), (px + 2 * k, py + 1.2 * k), (px + 3.4 * k, py - 1.6 * k)], in_shade("#c8744a", "up") * 1.1, 0.9)
    for i, (cx_, cz_, ln_, ang_) in enumerate(((-60.0, 40.0, 60.0, 0.3), (210.0, 10.0, 50.0, -0.6), (-300.0, 170.0, 70.0, 0.9), (120.0, 190.0, 48.0, 0.1), (-470.0, 60.0, 60.0, -0.3),
                                                 (30.0, 300.0, 52.0, 1.2), (-110.0, 330.0, 40.0, -0.9), (60.0, -10.0, 40.0, 0.7), (-200.0, 20.0, 55.0, 1.4), (-90.0, 560.0, 50.0, 0.5))):
        pts_ = [(cx_, cz_)]                                                                                 # a few stones are cracked across
        for j in range(5):
            pts_.append((pts_[-1][0] + math.cos(ang_) * ln_ / 5 + rng.normal(0, 3), pts_[-1][1] + math.sin(ang_) * ln_ / 5 + rng.normal(0, 3)))
        lit_.line([P(a_, 0, b_) for a_, b_ in pts_], in_shade("#2c2630", "deep") * 1.2, 0.8, 0.7)
        lit_.line([P(a_ + 1.5, 0, b_ + 2.0) for a_, b_ in pts_], in_shade("#aab0d0", "up"), 0.6, 0.35)
    put(pic, lit_)
    # weeds at the feet of the walls and round the fountain, where it is damp
    import flora
    wd = Sheet2(shape)
    greens = (in_shade("#3f5a34", "front"), in_shade("#6f9a4e", "front") * 1.1, np.clip(in_shade("#a8c468", "up") * 1.2, 0, 1))
    spots = [(WR - 3, zz) for zz in (-10.0, 62.0, 196.0, 420.0, 590.0, 700.0, 870.0, 1010.0, 1340.0)] + [(FOUNT["x0"] - 5, 262.0), (FOUNT["x0"] - 4, 380.0), (FOUNT["x0"] + 40, FOUNT["z0"] - 4)]
    spots += [(WL + 3, zz) for zz in (420.0, 560.0, 760.0, 905.0, 1150.0)] + [(-534.0, ZF - 3), (-262.0, ZF - 3), (-600.0, ZF - 2)]
    for i, (xx, zz) in enumerate(spots):
        px, py = P(xx, SWH, zz)
        flora.scrub(wd, px, py + 0.5, (5 + rng.random() * 6) * kz(zz) * 1.4, seed + 200 + i, colors=greens)
    for i in range(14):                                                                                     # and grass in the joints of the kerb
        zz = 40 + rng.random() ** 1.3 * 900
        px, py = P(KR + rng.random() * 3, 0.5, zz) if rng.random() < 0.6 else P(KL - rng.random() * 3, 0.5, max(zz, ZK + 30))
        flora.scrub(wd, px, py, 3.2 * kz(zz) * 1.4, seed + 240 + i, colors=greens)
    put(pic, wd)
    return pic


def grade(picture, vib=0.6, lift=0.055):
    """The last glaze, the same for the backdrop and every cut-out: colors that have gone dull in the shade are
    made richer (strong ones are left alone), and the darks are given a little blue air."""
    lum = (picture @ np.array([0.3, 0.55, 0.15], dtype=F32))[..., None]
    s = (picture.max(-1) - picture.min(-1))[..., None]
    out = lum + (picture - lum) * (1 + vib * np.clip(1 - s / 0.45, 0, 1))
    out = out + lift * np.clip(1 - lum / 0.5, 0, 1) * np.array([0.6, 0.8, 1.4], dtype=F32)
    return np.clip(out, 0, 1).astype(F32)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02, was=None):
    """Grain, then a palette chosen for the picture, with speckle. `was` (round four) = (the picture as it was approved,
    its alpha): the palette is chosen from that, exactly as it was then, so that every pixel that has not changed since
    keeps its old color. -> the size of the file"""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    if was is not None:
        g0 = grain(was[0], seed, amount)
        sample_of = g0 if was[1] is None else g0[was[1] > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    PALETTES[name] = pal                                                       # (round four: rome_street_four.py paints frames in it)
    return os.path.getsize(name)


PALETTES = {}


def show(picture, name):
    Image.fromarray((np.clip(picture, 0, 1) * 255).astype(np.uint8)).save(name)


def brushed(color, alpha, fast, sizes=(7, 4, 2), keep=0.42, seed=4):
    """A cut-out given its brushwork. It is painted on a flat ground of its own middle color, so that the
    strokes do not drag anything in at its edges, and only inside the box it fills."""
    if fast or not (alpha > 0.5).any():
        return color
    ys, xs = np.where(alpha > 0.02)
    y0, y1, x0, x1 = max(0, ys.min() - 10), min(H, ys.max() + 11), max(0, xs.min() - 10), min(W, xs.max() + 11)
    c, a = color[y0:y1, x0:x1], alpha[y0:y1, x0:x1]
    flat = np.empty(c.shape, dtype=F32)
    flat[...] = np.median(c[a > 0.5], axis=0)
    over(flat, c, a)
    out = color.copy()
    out[y0:y1, x0:x1] = strokes(flat, sizes=sizes, seed=seed, density=1.8, jitter=0.03, keep=keep)
    return out


def fountain_cut(fast, seed=5, moving=None):
    fc, fa, flc, fla = fountain_plane(seed, moving)
    c = brushed(fc, fa, fast, keep=0.45)
    over(c, flc, fla)
    return c, np.maximum(fa, fla)


def planes(fast, seed=5):
    """Every cut-out, finished. -> {name: (color, alpha)}"""
    out = {}
    ac, aa, alc, ala = awning_plane(seed)
    c = brushed(ac, aa, fast, keep=0.5)
    over(c, alc, ala)
    out["awning"] = (c, np.maximum(aa, ala))
    out["fountain"] = fountain_cut(fast, seed)
    wc, wa, wlc, wla = laundry_plane(seed)
    c = brushed(wc, wa, fast, sizes=(6, 3, 2), keep=0.45)
    over(c, wlc, wla)
    out["laundry"] = (c, np.maximum(wa, wla))
    tc, ta, tlc, tla = laundry_plane(seed, items=[TUNIC], ropes=False)
    c = brushed(tc, ta, fast, sizes=(4, 2), keep=0.5)
    over(c, tlc, tla)
    out["tunic"] = (c, np.maximum(ta, tla))
    pc, pa, plc, pla = front_plane(seed)
    c = brushed(pc, pa, fast, keep=0.42)
    over(c, plc, pla)
    out["front"] = (c, np.maximum(pa, pla))
    return out


ORDER = ("awning", "fountain", "laundry", "tunic", "front")

CACHE = "out/rome-street-work/under.npz"


def keep_under(base, info):
    """Put the block-in away, so that a later run that only changes details can start from it (`keep`)."""
    flat = {"base": base}
    for k_, v in info.items():
        if isinstance(v, dict):
            for k2, v2 in v.items():
                flat["D|%s|%s" % (k_, k2)] = v2
        elif isinstance(v, tuple):
            for i, v2 in enumerate(v):
                flat["T|%s|%d" % (k_, i)] = np.asarray(v2)
        else:
            flat["A|" + k_] = v
    np.savez(CACHE, **flat)


def kept_under():
    z = np.load(CACHE)
    info, tuples = {}, {}
    for key in z.files:
        if key == "base":
            continue
        kind, rest = key.split("|", 1)
        if kind == "A":
            info[rest] = z[key]
        elif kind == "D":
            a, b = rest.split("|")
            info.setdefault(a, {})[b] = z[key]
        else:
            a, i = rest.split("|")
            tuples.setdefault(a, {})[int(i)] = z[key]
    for a, parts in tuples.items():
        info[a] = tuple(parts[i] if parts[i].ndim else float(parts[i]) for i in range(len(parts)))
    return z["base"], info


def layout(cut):
    """The numbers the game needs, measured from the finished picture."""
    r = lambda p: [int(round(p[0])), int(round(p[1]))]
    pw = lambda x, z: r(P(x, SWH, z))                          # a place on a sidewalk
    pr = lambda x, z: r(P(x, 0.0, z))                          # a place on the roadway

    def box_of(name, pad=2):
        ys, xs = np.where(cut[name][1] > 0.5)
        return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 2 * pad, int(ys.max() - ys.min()) + 2 * pad]
    f = FOUNT
    far = 2300.0
    walk = [pw(WL + 14, far), pw(WL + 14, ZF + 16), pw(WL + 6, ZF - 12), [2, r(P(-590, SWH, ZF - 12))[1]], [2, 598], [796, 598],
            pw(WR - 14, -20), pw(WR - 14, far), pr(KR, far), pr(KL, far)]
    blocked = [
        [pw(f["x0"] - 8, f["z0"] - 8), pw(f["x1"] + 6, f["z0"] - 8), pw(f["x1"] + 6, f["z1"] + 40), pw(f["x0"] - 8, f["z1"] + 40)],          # the fountain
        [pw(BASKET[0] - 42, BASKET[1] - 30), pw(BASKET[0] + 42, BASKET[1] - 30), pw(BASKET[0] + 42, ZF - 6), pw(BASKET[0] - 42, ZF - 6)],   # the basket
        [[624, 598], [636, 566], [700, 548], [796, 540], [796, 598]],                                                                        # the jars and the wheel
        [pw(-574, 250), pw(-530, 250), pw(-530, 292), pw(-574, 292)],                                                                        # the stool
    ] + [[pr(xa - 4, STONE_Z[0] - 6), pr(xb + 4, STONE_Z[0] - 6), pr(xb + 4, STONE_Z[1] + 6), pr(xa - 4, STONE_Z[1] + 6)] for xa, xb in STONES]
    aw, fo, la, tu = box_of("awning"), box_of("fountain"), box_of("laundry"), box_of("tunic", 4)
    bx, by = P(BASKET[0], SWH, BASKET[1])
    kb = kz(BASKET[1])
    out = {
        "id": "rome-street", "horizon": HZ, "full": FULL,
        "light": "morning sun from the upper right and a little behind us; the roadway and the right side are in the shade of the right-hand houses",
        "walk": walk, "blocked": blocked,
        "planes": [
            {"id": "awning", "file": "awning.png", "base": int(round(row_of(SWH, ZF)))},
            {"id": "fountain", "file": "fountain.png", "base": int(round(row_of(SWH, f["z0"])))},
            {"id": "laundry", "file": "laundry.png", "plane": "front"},
            {"id": "tunic", "file": "tunic.png", "plane": "front"},
            {"id": "front", "file": "front.png", "plane": "front"},
        ],
        "things": [
            {"id": "snack-bar", "what": "the snack bar: counter, stove, awning", "shape": {"rect": [0, aw[1], 236, aw[3]]}, "stand": pw(-380, 288), "face": "N"},
            {"id": "fountain", "what": "the public fountain", "shape": {"rect": fo}, "stand": pw(188, 262), "face": "E"},
            {"id": "laundry", "what": "the washing on the lines over the street", "shape": {"poly": [[256, 106], [614, 102], [614, 238], [456, 238], [456, 154], [374, 154], [374, 244], [256, 244]]}, "stand": pr(-20, 380), "face": "N"},
            {"id": "tunic", "what": "the small tunic on the low line", "shape": {"rect": tu}, "stand": pr(-122, 215), "face": "N"},
            {"id": "basket", "what": "the washerwoman's basket of wet washing", "shape": {"rect": [int(bx - 36 * kb), int(by - 66 * kb), int(72 * kb), int(72 * kb)]}, "stand": pr(-122, 215), "face": "N"},
            {"id": "shrine", "what": "the crossroads shrine: a niche with a lamp, a painted snake", "shape": {"rect": [r(P(-305, 250, ZF))[0], r(P(-305, 250, ZF))[1], int(48 * kz(ZF)), int(124 * kz(ZF))]}, "stand": pw(-282, 288), "face": "N"},
            {"id": "price-list", "what": "the price list painted on the pier", "shape": {"rect": [2, r(P(-599, 238, ZF))[1], int(66 * kz(ZF)), int(102 * kz(ZF))]}, "stand": pw(-520, 288), "face": "N"},
            {"id": "notices", "what": "election notices painted in red: MARCVS, VOTA", "shape": {"rect": [4, r(P(0, 446, ZF))[1], 228, int(74 * kz(ZF))]}, "stand": pr(-300, 150), "face": "N"},
            {"id": "notice-right", "what": "a painted notice (RVFVS) and scratched scribbles on the right-hand wall", "shape": {"poly": [[716, 372], [799, 345], [799, 520], [716, 478]]}, "stand": pw(300, 150), "face": "E"},
            {"id": "cat", "what": "a cat on a window sill", "shape": {"rect": [728, 146, 40, 62]}, "stand": pw(260, 120), "face": "E"},
            {"id": "sign", "what": "the snack bar's hanging sign: a wine jug and grapes", "shape": {"rect": [r(P(WL + 8, 344, ZF + 30))[0] - 2, r(P(WL + 8, 358, ZF + 30))[1] - 2, int(56 * kz(ZF + 30)) + 4, int(60 * kz(ZF + 30)) + 4]}, "stand": pr(-120, 300), "face": "N"},
            {"id": "birdcage", "what": "a songbird in a wicker cage on the balcony (the cat is watching it)", "shape": {"rect": [r(P(BALC["x"] - 4, BALC["top"], 246))[0] - 12, r(P(BALC["x"] - 4, BALC["top"], 246))[1], 24, 44]}, "stand": pw(260, 200), "face": "N"},
            {"id": "stepping-stones", "what": "three stepping stones across the street", "shape": {"rect": [pr(STONES[0][0], STONE_Z[1])[0] - 4, pr(0, STONE_Z[1])[1] - 16, pr(STONES[2][1], STONE_Z[1])[0] - pr(STONES[0][0], STONE_Z[1])[0] + 8, 34]}, "stand": pr(0, 330), "face": "N"},
            {"id": "balcony", "what": "the timber balcony the washing lines are tied to", "shape": {"poly": [r(P(BALC["x"], BALC["top"], 180)), r(P(WR, BALC["top"] + 50, 180)), r(P(WR, BALC["floor"] - 20, 180)), r(P(BALC["x"], BALC["floor"] - 20, 180)), r(P(BALC["x"], BALC["floor"] - 20, 640)), r(P(BALC["x"], BALC["top"], 640))]}, "stand": pw(260, 200), "face": "N"},
        ],
        "exits": [{"to": "rome-steps", "id": "to-forum", "shape": {"poly": [[376, 178], [454, 178], [454, 240], [478, 332], [326, 332], [352, 246], [376, 246]]}, "stand": pr(0, 2050), "face": "N"}],
        "marks": {"keeper": r(P(-410, SWH, 440)), "washer": pr(-100, 270), "urchin": pr(150, 141), "son": pr(24, 80)},
        "notes": "The keeper's mark is on the shop floor, which is a sidewalk's height above the road, so it is 11 px higher than the brief's. "
                 "The urchin sits on the right-hand kerb with his feet in the road at his mark. The stepping stones are listed under blocked; drop them if they get in the way. "
                 "Things are listed small before big: where two shapes overlap, the earlier one is meant. Only snack-bar, fountain, laundry, basket, tunic and the exit to-forum "
                 "are asked for by the brief; the rest are extra things to look at.",
    }
    first = ("tunic", "basket", "shrine", "price-list", "sign", "birdcage", "cat", "fountain", "snack-bar", "notices", "laundry", "stepping-stones", "balcony", "notice-right")
    out["things"].sort(key=lambda t: first.index(t["id"]))                 # small things before the big ones they lie in
    inside = lambda p: [min(max(int(p[0]), 0), W - 1), min(max(int(p[1]), 0), H - 1)]
    out["walk"] = [inside(p) for p in out["walk"]]
    out["blocked"] = [[inside(p) for p in poly] for poly in out["blocked"]]
    return out


def check_layout(whole, lay, name):
    """A picture of the layout laid over the scene, to look at."""
    from PIL import ImageDraw
    im = Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.polygon([tuple(p) for p in lay["walk"]], fill=(60, 255, 120, 50), outline=(60, 255, 120, 255))
    for bl in lay["blocked"]:
        d.polygon([tuple(p) for p in bl], fill=(255, 60, 60, 80), outline=(255, 60, 60, 255))
    for t in lay["things"] + lay["exits"]:
        sh = t["shape"]
        if "rect" in sh:
            x, y, w, h = sh["rect"]
            d.rectangle([x, y, x + w, y + h], outline=(255, 255, 0, 255))
        else:
            d.polygon([tuple(p) for p in sh["poly"]], outline=(255, 255, 0, 255))
        sx, sy = t["stand"]
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 255, 0, 255))
        d.text((sx + 5, sy - 5), t["id"], fill=(255, 255, 255, 255))
    for k_, (mx, my) in lay["marks"].items():
        hgt = 160 * (my - HZ) / (FULL - HZ) * (0.8 if k_ in ("son", "urchin") else 1.0)
        d.rectangle([mx - hgt * 0.14, my - hgt, mx + hgt * 0.14, my], outline=(80, 200, 255, 255))
        d.text((mx - 10, my + 2), k_, fill=(80, 200, 255, 255))
    for pl in lay["planes"]:
        if "base" in pl:
            d.line([0, pl["base"], 799, pl["base"]], fill=(255, 0, 255, 120))
    Image.alpha_composite(im, ov).convert("RGB").save(name)


if __name__ == "__main__":
    # python3 rome_street.py        paints everything and writes out/rome-street/ and out/rome-street-comp.png
    # python3 rome_street.py fast   skips the brush passes and writes only the pictures to look at (out/rome-street-work/)
    # (while working: add `cache` to put the block-in and the brushwork away, `keep` to start from the kept block-in,
    #  `kb` to reuse the kept brushwork as well; both only make sense while the block-in itself is not being changed)
    t0 = time.time()
    fast = "fast" in sys.argv
    cache = "cache" in sys.argv or "keep" in sys.argv
    os.makedirs("out/rome-street", exist_ok=True)
    os.makedirs("out/rome-street-work", exist_ok=True)
    if "keep" in sys.argv and os.path.exists(CACHE):
        base, info = kept_under()
    else:
        base, info = under()
        if cache:
            keep_under(base, info)
    print("under", round(time.time() - t0, 1))
    solids = back_solids(info)
    tint(base, (0.50, 0.50, 0.84), solids[2] * 0.92)                          # shadows thrown on the sunlit walls
    put(base, solids[0], wobble=0.5, seed=3)
    base = warp(base, 0.8, 34.0, 11)                                          # nothing a hand draws is ruled
    show(base, "out/rome-street-work/1-under.png")
    BR = "out/rome-street-work/brushed.npy"
    if fast:
        pic = base.copy()
    elif "kb" in sys.argv and os.path.exists(BR):
        pic = np.load(BR)
    else:
        away = np.arctan2(PY - cam.vy, PX - cam.vx)                           # on the walls that run away from us the brush follows them back
        side_walls = np.clip(info["m_RA"] + info["m_RB"] + info["m_RC"] + info["m1"] + info["m2"], 0, 1) > 0.5
        pic = strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.22, flow=np.where(side_walls, away, 0.0).astype(F32))
        if cache:
            np.save(BR, pic)
    print("brushed", round(time.time() - t0, 1))
    if not PAINT_MOVING:                                                      # round four: the picture as it was approved (its palette is kept)
        pic_was = grade(details(pic.copy(), base, info, solids, moving=True))
    details(pic, base, info, solids)
    ungraded = pic.copy()
    pic = grade(pic)
    print("details", round(time.time() - t0, 1))
    cut = {name: (grade(c), a) for name, (c, a) in planes(fast).items()}
    whole = pic.copy()
    for name in ORDER:
        c, a = cut[name]
        over(whole, c, (a > 0.5).astype(F32))
    show(pic, "out/rome-street-work/2-back.png")
    show(whole, "out/rome-street-work/2-all.png")
    lay = layout(cut)
    check_layout(whole, lay, "out/rome-street-work/3-layout.png")
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    if PAINT_MOVING:
        print("back", finish(pic, "out/rome-street/back.png", 152))
    else:
        print("back", finish(pic, "out/rome-street/back.png", 152, was=(pic_was, None)))
        fountain_was = tuple(np.asarray(v) for v in fountain_cut(fast, moving=True))
        fountain_was = (grade(fountain_was[0]), fountain_was[1])
    for name, colors in (("awning", 72), ("fountain", 64), ("laundry", 72), ("tunic", 32), ("front", 56)):
        c, a = cut[name]
        print(name, finish(c, "out/rome-street/%s.png" % name, colors, a, was=fountain_was if name == "fountain" and not PAINT_MOVING else None))
    if not PAINT_MOVING:                                                      # round four: frames, the washing in pieces, the marks
        import rome_street_four as four
        lay.update(four.everything(sys.modules[__name__], pic, pic_was, ungraded, cut, fountain_was, info))
    with open("out/rome-street/layout.json", "w") as fh:
        json.dump(lay, fh, indent=1)
    os.system("%s comp.py out/rome-street back %s" % (sys.executable, " ".join(ORDER)))
    print("done", round(time.time() - t0, 1))

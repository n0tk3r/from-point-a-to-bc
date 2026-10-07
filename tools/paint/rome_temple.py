"""Rome, 44 B.C., the Ides of March: inside the old temple that is also the treasury of the Roman People.
One dark room seen straight down its length; the god at the far end; the money down both walls; and one
hard patch of morning sun on the floor from the doors behind us.

THE PLAN
  Light      ONE key light: the sun through the doors behind us (a little from our left), lying on the floor
             as a hard four-sided patch at the bottom middle. Everything else is what that can reach: the cool
             daylight of the doorway dying away up the room, the warm bounce off the patch, two braziers of
             coals (one at the front left, one by the altar on the right) and the clerk's lamp. Light is warm,
             the dark is black-green, wine red and violet, never plain black. Light comes FROM US and FROM
             BELOW: faces that look toward the door are the lit ones, tops are dim, the side walls are darkest.
  Depth      horizon 120, full 585 (a high eye, 5 m up: we look down the room as on a stage).
             The room is 8 m wide, 13 m long, 7 m to its timber ceiling. persp.Camera gives every size.
  Three      DARK: the walls (red and black panels), the ceiling, the far floor.
  tones      MIDDLE: the near floor in the door's daylight, the god and his pedestal, the faces of the chests.
             LIGHT: the sun patch (the only really bright thing); then small sparks: coals, the lamp, gold lines.
             The eye goes in at the patch, up the floor to the altar and the god in his dark niche.
  Things     statue      far end, on its pedestal in an arched niche          (346-454, 127-336); stand (400, 354)
             sunpatch    bottom middle                                         (303,598) (366,430) (480,430) (475,598)
             hum         bare wall between two chests, left, in shadow         at (190, 330); stand (232, 480)
             chests      down both walls; sacks; law tablets; standards in the far left corner
             table       the clerk's table, right middle (cut-out, base 488)   about (503-657, 382-492); clerk (614, 464)
             front       the two door leaves at the borders, a brazier bottom left (front plane)
             (layout.json has every number, worked out from the same measurements the picture is drawn with)

The picture is a backdrop and two cut-outs: `table` (the clerk sits behind it) and `front`."""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
from persp import Camera, tiles
import letter
from rome_temple_kit import *

W, H = 800, 600
SHAPE = (H, W)
HZ, FULL = 120, 585
OUT = "out/rome-temple"

cam = Camera(HZ, FULL)
A, ZB, HC = 400.0, 1260.0, 700.0                            # half the room's width, how far the back wall is, the ceiling
room = Room(cam, A, ZB, HC)
P = room.P

# ---- the lamps
SUN_Z = 437.0                                               # how far up the room the sun reaches
SUN_SLANT = 0.11                                            # it comes a little from our left
SUN_X0, SUN_W = -103.0, 186.0                               # its left edge where the picture ends (z = -27), and its width
BRAZIER1 = (-286.0, 60.0, -6.0)                             # x, the height of its fire, z   (front plane): a long bronze box on lions' feet
BOX1 = (-340.0, -232.0, -40.0, 30.0)                        # its x0, x1, z0, z1
BRAZIER2 = (168.0, 92.0, 925.0)                             # by the altar
LAMP = (338.0, 106.0, 264.0)                                # the flame of the clerk's lamp
TABLE = (205.0, 348.0, 230.0, 292.0, 76.0)                  # the clerk's table: x0, x1, z0, z1, height
room.lights = [
    dict(kind="door", dir=(0.0, 0.28, -0.96), rgb=col((0.72, 0.82, 1.0)), power=0.80, z0=200.0, reach=360.0, width=330.0, top=420.0, wrap=0.22),
    dict(kind="bounce", at=[(-40.0, 60.0), (0.0, 200.0), (28.0, 360.0)], rgb=col((1.0, 0.80, 0.52)), power=0.46, reach=320.0, top=250.0),
    dict(kind="point", at=(BRAZIER1[0], BRAZIER1[1] + 44, BRAZIER1[2]), rgb=col((1.0, 0.40, 0.14)), power=1.0, reach=140.0,
         rects=[(BOX1[0], BOX1[1], BOX1[2], BOX1[3], BRAZIER1[1], 14.0)]),
    dict(kind="point", at=(BRAZIER2[0], BRAZIER2[1] + 10, BRAZIER2[2]), rgb=col((1.0, 0.42, 0.15)), power=1.40, reach=128.0,
         discs=[(BRAZIER2[0], BRAZIER2[2], 7.0, BRAZIER2[1])]),
    dict(kind="point", at=LAMP, rgb=col((1.0, 0.70, 0.34)), power=1.15, reach=68.0, core=0.6,
         rects=[(TABLE[0] - 3, TABLE[1] + 3, TABLE[2] - 3, TABLE[3] + 3, TABLE[4], 9.0)]),
]

# ---- what the walls and the floor are made of (their colors in full light)
TILE = 120.0
STONE_LIGHT, STONE_DARK, STONE_EDGE = col((0.74, 0.67, 0.55)), col((0.40, 0.44, 0.41)), col((0.25, 0.22, 0.22))
RED, BLACK, GOLD = col((0.54, 0.15, 0.10)), col((0.16, 0.19, 0.19)), col((0.88, 0.66, 0.26))
DADO, PLINTH, OCHRE = col((0.12, 0.24, 0.19)), col((0.30, 0.27, 0.25)), col((0.60, 0.43, 0.19))
FRIEZE, UPPER = col((0.15, 0.13, 0.14)), col((0.30, 0.11, 0.09))
BEAM, COFFER, NICHE = col((0.28, 0.19, 0.12)), col((0.12, 0.09, 0.07)), col((0.09, 0.23, 0.25))
V_PLINTH, V_DADO, V_CAP, V_MAIN, V_FRIEZE = 22.0, 128.0, 136.0, 470.0, 520.0      # heights where the wall's bands change
RED_SIDE = [(-200.0, 280.0), (470.0, 770.0), (960.0, 1245.0)]                      # the red panels of a side wall, along z
RED_BACK = [(-385.0, -190.0), (190.0, 385.0)]                                     # and of the back wall, along x
NICHE_W, NICHE_SPRING = 140.0, 420.0                                              # the god's niche: half width, where its arch springs
HUM = (-A, 108.0, 649.0)                                                          # the place that hums: on the bare left wall

# ---- the treasury: (x0, x1, y0, y1, z0, z1, seed, options)
LEFT = [
    dict(box=(-400, -318, 0, 84, 52, 196), seed=11),
    dict(box=(-400, -326, 0, 62, 226, 346), seed=12, metal=BRONZE, trim="#d8b060"),
    dict(box=(-396, -338, 62, 101, 242, 318), seed=13, wood="#6a2a1e", metal=BRONZE, trim="#e0bc6a", lock=False, straps=(0.25, 0.75), boards=2, feet=False),
    dict(box=(-400, -322, 0, 54, 378, 500), seed=14, plated=True, seal=True),
    dict(box=(-400, -328, 0, 72, 900, 1012), seed=15, metal=BRONZE, trim="#d8b060"),
]
RIGHT = [
    dict(box=(322, 400, 0, 86, 18, 146), seed=21, seal=True),
    dict(box=(326, 400, 0, 68, 506, 640), seed=22, metal=BRONZE, trim="#d8b060"),
    dict(box=(340, 398, 68, 110, 522, 612), seed=23, plated=True, lock=False, feet=False),
]
RACK = (360.0, 400.0, 0.0, 215.0, 308.0, 470.0)
STOOL = (296.0, 336.0, 302.0, 338.0)                        # where the clerk sits: x0, x1, z0, z1
OPEN = (322.0, 400.0, 0.0, 62.0, 676.0, 800.0)             # the chest that stands open
PED = dict(x=112.0, z0=1040.0, z1=1232.0, top=150.0)       # the god's pedestal
PLACES = {}                                                # faces that the last pass letters on
STATUE_SCALE = 1.15                                        # the god, a little over twice the size of a man


def sun_edges(z):
    """World x of the left and right edges of the sun patch at depth z."""
    xl = SUN_X0 + SUN_SLANT * (z + 27.0)
    return xl, xl + SUN_W


def wall_bands(u, v, reds, ground=None):
    """The painted scheme of a wall, as its own color at every place: u along it, v up it."""
    out = np.empty(u.shape + (3,), dtype=F32)
    out[...] = BLACK if ground is None else ground
    red = np.zeros(u.shape, dtype=bool)
    for (a, b) in reds:
        red |= (u > a) & (u < b)
    red &= (v > V_CAP + 14) & (v < V_MAIN - 14)
    out[red] = RED
    out[v < V_CAP] = OCHRE
    out[v < V_DADO] = DADO
    out[v < V_PLINTH] = PLINTH
    fr = (v >= V_MAIN) & (v < V_FRIEZE)
    out[fr] = FRIEZE
    out[fr & ((v < V_MAIN + 7) | (v > V_FRIEZE - 7))] = OCHRE
    out[v >= V_FRIEZE] = UPPER
    return out


# ======================================================================== the bare room
def shell(seed=7):
    """The bare room: floor, walls, ceiling, each with its own colors, in the light of the lamps. Soft:
    no lines yet. -> (picture, info)"""
    ss = 2
    ids, X, Y, Z = room.maps(SHAPE, ss)
    shape2 = ids.shape
    alb = np.zeros(shape2 + (3,), dtype=F32)
    cloud = noise((1024, 1024), 90, seed, 5)                 # one cloudy sheet, laid on every wall and on the floor in the world's own measure
    fine = noise((1024, 1024), 22, seed + 1, 4)

    def on(u, v, sheet=cloud, scale=0.9):
        return sample(sheet, (u * scale + 4000.0) % 1020.0, (v * scale + 4000.0) % 1020.0)

    # ---- the floor: big squares of pale and grey-green stone, a dark band along the walls
    fl = ids == 0
    iu, iv = np.floor(X / TILE), np.floor(Z / TILE)
    fu, fv = X / TILE - iu, Z / TILE - iv
    hsh = np.sin(iu * 127.1 + iv * 311.7 + 3.0) * 43758.5453
    each = (hsh - np.floor(hsh)).astype(F32)                 # every slab a little different
    check = ((iu + iv) % 2) == 0
    stone = np.where(check[..., None], STONE_LIGHT, STONE_DARK)
    stone = lerp(stone, (STONE_LIGHT + STONE_DARK) / 2, (np.clip(Z / ZB, 0, 1) * 0.40)[..., None])     # far off the two stones draw together
    stone = stone * (1 + (each[..., None] - 0.5) * 0.24)
    warm = (np.sin(iu * 12.9 + iv * 78.2) * 0.5 + 0.5)[..., None] * np.array([0.05, 0.0, -0.05], dtype=F32)     # some slabs warmer, some cooler
    stone = stone + warm
    vein = on(X * 1.7 + iu * 300, Z * 0.7 + iv * 170, fine, 1.0)
    stone = stone * (1 + (vein[..., None] - 0.5) * 0.22)
    border = np.abs(X) > 360.0
    stone = np.where(border[..., None], STONE_EDGE * (1 + (on(X, Z, fine)[..., None] - 0.5) * 0.3), stone)
    kk = cam.F / (cam.Z0 + Z)
    edge_cm = np.minimum(np.minimum(fu, 1 - fu), np.minimum(fv, 1 - fv)) * TILE
    joint = np.clip(1 - edge_cm / (1.5 * (cam.scale(0) / np.maximum(kk, 1e-3)) ** 0.6), 0, 1)
    worn = on(X, Z, cloud, 0.6)
    stone = stone * (1 + (worn[..., None] - 0.5) * 0.26)
    stone = stone * (1 - joint[..., None] * 0.45)
    path = np.exp(-(X / 210.0) ** 2)                         # feet have polished the middle of the room
    stone = stone * (0.92 + 0.12 * path[..., None])
    alb[fl] = stone[fl]

    # ---- the side walls and the back wall
    for pid in (1, 2):
        sel = ids == pid
        a = wall_bands(Z, Y, RED_SIDE)
        stain = on(Z + pid * 700, Y * 1.0, cloud, 0.8)
        drip = on(Z * 2.2 + pid * 300, Y * 0.25, fine, 1.0)   # soot and damp run down a wall
        a = a * (1 + (stain[..., None] - 0.5) * 0.40 + (drip[..., None] - 0.5) * 0.24)
        alb[sel] = a[sel]
    sel = ids == 3
    a = wall_bands(X, Y, RED_BACK)
    r2 = X * X + np.maximum(Y - NICHE_SPRING, 0) ** 2
    frame = (r2 < (NICHE_W + 17) ** 2)
    niche = (r2 < NICHE_W ** 2)
    a[frame] = OCHRE
    a[niche] = NICHE
    stain = on(X + 300, Y + 500, cloud, 0.8)
    a = a * (1 + (stain[..., None] - 0.5) * 0.40)
    alb[sel] = a[sel]

    # ---- the ceiling: timber coffers
    sel = ids == 4
    cu, cv = (X / 132.0) % 1.0, (Z / 132.0) % 1.0
    beam = (np.minimum(cu, 1 - cu) < 0.13) | (np.minimum(cv, 1 - cv) < 0.13)
    a = np.where(beam[..., None], BEAM, COFFER) * (1 + (on(X, Z, fine)[..., None] - 0.5) * 0.4)
    alb[sel] = a[sel]

    # ---- light
    m = room.lightmap(ids, X, Y, Z)
    # corners and feet of walls sit in their own shade; the top of the room is lost
    wallish = (ids == 1) | (ids == 2) | (ids == 3)
    ao = np.ones(shape2, dtype=F32)
    ao[wallish] *= (1 - 0.34 * np.exp(-Y / 46.0))[wallish]
    ao[wallish] *= (1 - 0.42 * smooth((Y - 400.0) / 280.0))[wallish]
    side = (ids == 1) | (ids == 2)
    ao[side] *= (1 - 0.30 * np.exp(-(ZB - Z) / 70.0))[side]
    ao[ids == 3] *= (1 - 0.30 * np.exp(-(A - np.abs(X)) / 70.0))[ids == 3]
    ao[fl] *= (1 - 0.30 * np.exp(-(A - np.abs(X)) / 55.0))[fl]
    ao[fl] *= (1 - 0.25 * np.exp(-(ZB - Z) / 60.0))[fl]
    ao[niche & (ids == 3)] *= 0.78
    m[ids == 4] += 0.07
    pic2 = alb * m * ao[..., None]
    pic2 = room.air(pic2, Z)
    pic = np.clip(resize(pic2, SHAPE, Image.BOX), 0, 1).astype(F32)

    slab_tone, _ = tiles(cam, SHAPE, (TILE, TILE), seed + 9)   # the library's paving: one more step of difference from slab to slab
    fl1 = (resize((ids == 0).astype(F32), SHAPE, Image.BOX) > 0.5)
    pic[fl1] *= (1 + (slab_tone[fl1] - 0.5) * 0.14)[..., None]

    # ---- the sun on the floor: the one bright thing
    sunstone = np.where(check[..., None], col("#fff4d6"), col("#f0d09a"))
    sunstone = sunstone * (1 + (each[..., None] - 0.5) * 0.06 + (worn[..., None] - 0.5) * 0.07) * (1 - joint[..., None] * 0.22)
    sunstone = np.clip(resize(sunstone.astype(F32), SHAPE, Image.BOX), 0, 1)
    z0 = -70.0
    l0, r0 = sun_edges(z0)
    l1, r1 = sun_edges(SUN_Z)
    quad = [P(l0, 0, z0), P(l1, 0, SUN_Z), P(r1, 0, SUN_Z), P(r0, 0, z0)]
    patch = mask_poly(SHAPE, quad, wobble=0.5, seed=seed + 3)
    x, y = grid(SHAPE)
    patch = np.where(y < quad[1][1] + 5, blur(patch, 1.5), blur(patch, 0.55))        # the far edge is the lintel's shadow: a breath softer
    floor1 = (resize((ids == 0).astype(F32), SHAPE, Image.BOX) > 0.5).astype(F32)
    # the door leaf's shadow lies along its left side, and a blade of sun comes through at the hinge beyond it
    band_w, slit_w = 52.0, 13.0
    band = mask_poly(SHAPE, [P(l0 - band_w, 0, z0), P(l1 - band_w, 0, SUN_Z), P(l1, 0, SUN_Z), P(l0, 0, z0)], soft=0.8)
    slit = mask_poly(SHAPE, [P(l0 - band_w - slit_w, 0, z0), P(l1 - band_w - slit_w, 0, SUN_Z - 3), P(l1 - band_w, 0, SUN_Z - 3), P(l0 - band_w, 0, z0)], soft=0.6)
    tint(pic, "#56506e", (band * 0.58 * floor1).astype(F32))
    halo = np.clip(blur(np.maximum(patch, slit), 14) * 1.25 - np.maximum(patch, slit), 0, 1) * floor1
    glow(pic, "#ffc98a", (halo * 0.16).astype(F32))
    over(pic, sunstone, patch * floor1)
    over(pic, sunstone * col("#fff0d0"), np.clip(slit * 0.95, 0, 1) * floor1)
    lip = np.clip(blur(np.maximum(patch, slit), 1.3) * 2.2, 0, 1) * (1 - np.maximum(patch, slit)) * floor1      # where light ends it burns a little orange
    glow(pic, "#ff8a3a", (lip * 0.30).astype(F32))
    info = dict(ids=ids, X=X, Y=Y, Z=Z, floor=floor1, patch=patch, quad=quad, slit=slit, band=band)
    return pic, info


# ======================================================================== shadows that things throw
def ground_shadow(pic, floor, x0, x1, z0, z1, amount=0.5, grow=(14, 14, 12, 8), soft=4.0, color="#2e2634"):
    quad = [P(x0 - grow[0], 0, z0 - grow[2]), P(x1 + grow[1], 0, z0 - grow[2]), P(x1 + grow[1], 0, z1 + grow[3]), P(x0 - grow[0], 0, z1 + grow[3])]
    m = mask_poly(SHAPE, quad, soft=soft * room.k(z0)) * floor
    tint(pic, color, np.clip(m * amount, 0, 1).astype(F32))


def wall_shadow(pic, side, u0, u1, v0, v1, amount=0.45, soft=3.0, color="#241c28"):
    quad = [P(*room.wall(side, u0, v0)), P(*room.wall(side, u1, v0)), P(*room.wall(side, u1, v1)), P(*room.wall(side, u0, v1))]
    m = mask_poly(SHAPE, quad, soft=soft)
    tint(pic, color, np.clip(m * amount, 0, 1).astype(F32))


def shadows(pic, info):
    floor = info["floor"]
    for c in LEFT + RIGHT:
        x0, x1, y0, y1, z0, z1 = c["box"]
        if y0 > 0:
            continue
        left = x1 < 0
        ground_shadow(pic, floor, x0, x1, z0, z1, 0.55, grow=(0, 30, 14, 4) if left else (30, 0, 14, 4), soft=7)
        wall_shadow(pic, "L" if left else "R", z0 - 12, z1 + 20, y1 - 10, y1 + 44, 0.42, soft=5)
    x0, x1, y0, y1, z0, z1 = OPEN
    ground_shadow(pic, floor, x0, x1, z0, z1, 0.55, grow=(30, 0, 14, 4), soft=7)
    x0, x1, y0, y1, z0, z1 = RACK
    ground_shadow(pic, floor, x0, x1, z0, z1, 0.55, grow=(26, 0, 12, 30), soft=7)
    wall_shadow(pic, "R", z1, z1 + 110, 0, y1 + 30, 0.40, soft=7)             # the lamp throws the rack's shadow up the wall beyond it
    # the pedestal and the god: a pool of dark at their foot and a great soft shadow up the niche behind
    ground_shadow(pic, floor, -PED["x"] - 10, PED["x"] + 10, PED["z0"] - 6, PED["z1"], 0.6, grow=(26, 8, 22, 0), soft=8)
    sil = [(-70, 150), (-70, 392), (-34, 400), (-22, 444), (22, 444), (34, 400), (70, 392), (70, 150)]
    m = mask_poly(SHAPE, [P(sx * STATUE_SCALE - 30, 150 + (sy - 150) * STATUE_SCALE + 24, ZB) for sx, sy in sil], soft=5.0)
    tint(pic, "#161a26", (m * 0.62).astype(F32))
    # the altar table, the far brazier, the jars in the corner
    ground_shadow(pic, floor, -52, 52, 903, 960, 0.5, grow=(22, 4, 10, 16), soft=5)
    ground_shadow(pic, floor, BRAZIER2[0] - 22, BRAZIER2[0] + 22, BRAZIER2[2] - 20, BRAZIER2[2] + 20, 0.45, grow=(6, 6, 6, 6), soft=5)
    ground_shadow(pic, floor, 336, 396, 1170, 1240, 0.5, grow=(30, 0, 10, 0), soft=5)
    ground_shadow(pic, floor, -372, -292, 1215, 1255, 0.45, grow=(0, 10, 10, 0), soft=4)
    ground_shadow(pic, floor, -190, -162, 926, 950, 0.45, grow=(22, 2, 4, 4), soft=4)
    # under the clerk's table it is dark; the lamp is ON the table, so the floor all round it stays dim (that is in the light itself)
    ground_shadow(pic, floor, TABLE[0], TABLE[1], TABLE[2], TABLE[3], 0.50, grow=(8, 8, 10, 10), soft=6)
    ground_shadow(pic, floor, STOOL[0], STOOL[1], STOOL[2], STOOL[3], 0.4, grow=(6, 6, 6, 6), soft=4)
    # the paving is worn smooth: it gives back a little of what stands over it, in soft upright smears
    x, y = grid(SHAPE)
    streak = 0.55 + 0.9 * noise(SHAPE, (5, 70), 91, 2)
    a, b = P(-PED["x"], 0, PED["z0"] - 10), P(PED["x"], 0, PED["z0"] - 10)
    m = mask_poly(SHAPE, [a, b, (b[0] + 2, b[1] + 46), (a[0] - 2, a[1] + 46)], soft=2.5) * np.clip(1 - (y - a[1]) / 46.0, 0, 1) * floor
    glow(pic, "#b8a48a", np.clip(m * streak * 0.20, 0, 1).astype(F32))
    cx, cy = P(BRAZIER2[0], -BRAZIER2[1], BRAZIER2[2])
    m = mask_ellipse(SHAPE, cx, cy - 4, 9, 20, soft=3.0) * floor
    glow(pic, "#ff7a2a", np.clip(m * streak * 0.34, 0, 1).astype(F32))
    # the far brazier's own fire throws the shadows of its three legs out across the floor
    for a in (100, 215, 325):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        f0 = P(BRAZIER2[0] + ca * 25, 0, BRAZIER2[2] + sa * 25)
        f1 = P(BRAZIER2[0] + ca * 84, 0, BRAZIER2[2] + sa * 84)
        m = mask_line(SHAPE, [f0, f1], [1.6, 3.6], soft=1.0) * floor
        tint(pic, "#2a1c20", (m * 0.42).astype(F32))
    # the near brazier: dark under it (the box's own shadow is in the light itself)
    ground_shadow(pic, floor, BOX1[0], BOX1[1], BOX1[2], BOX1[3], 0.55, grow=(6, 10, 6, 6), soft=5)
    return pic


# ======================================================================== painted lines on the walls and floor
def gold(D, side, uv, width=1.3, alpha=0.95, gain=1.3, rng=None, breaks=0.05, least=0.7):
    lit_line(D, room, [room.wall(side, u, v, 0.5) for u, v in uv], room.wall_n(side), GOLD, width, alpha, gain, least=least, rng=rng, breaks=breaks, floor=0.20)


def dark_line(D, pts3, width=1.2, alpha=0.6, color="#120e12", rng=None, breaks=0.0, step_cm=60.0):
    for p, q in zip(pts3[:-1], pts3[1:]):
        p, q = np.array(p, dtype=float), np.array(q, dtype=float)
        n = max(1, int(np.linalg.norm(q - p) / step_cm))
        for i in range(n):
            if rng is not None and breaks and rng.random() < breaks:
                continue
            s0, s1 = p + (q - p) * (i / n), p + (q - p) * ((i + 1) / n)
            wd = width * room.k((s0[2] + s1[2]) / 2)
            a = alpha * min(1.0, max(wd / 0.7, 0.3)) * (1.0 if rng is None else 0.75 + 0.25 * rng.random())
            D.line([P(*s0), P(*s1)], color, max(wd, 0.7), a, round_ends=False)


def wall_lines(D, seed=21):
    rng = np.random.default_rng(seed)
    near = -70.0
    for side in ("L", "R"):
        # ---- red panels: a gold line a hand inside the edge, and a hairline inside that
        for (a, b) in RED_SIDE:
            u0, u1, v0, v1 = max(a, near) + 13, b - 13, V_CAP + 27, V_MAIN - 27
            box = [(u0, v0), (u1, v0), (u1, v1), (u0, v1), (u0, v0)] if a > near else [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
            gold(D, side, box, 1.5, 0.95, rng=rng)
            gold(D, side, [(u0 + 9, v0 + 9), (u1 - 9, v0 + 9), (u1 - 9, v1 - 9), (u0 + 9, v1 - 9)] + ([(u0 + 9, v0 + 9)] if a > near else []), 0.6, 0.55, rng=rng, breaks=0.12, least=0.5)
        # ---- the black fields between: a thin frame, a slender stem, a lozenge in the middle
        for (a, b) in zip([r[1] for r in RED_SIDE[:-1]], [r[0] for r in RED_SIDE[1:]]):
            u0, u1, v0, v1 = a + 30, b - 30, V_CAP + 44, V_MAIN - 44
            gold(D, side, [(u0, v0), (u1, v0), (u1, v1), (u0, v1), (u0, v0)], 0.9, 0.8, rng=rng)
            um, vm = (a + b) / 2, (v0 + v1) / 2
            gold(D, side, [(um, vm + 26), (um + 15, vm), (um, vm - 26), (um - 15, vm), (um, vm + 26)], 1.0, 0.9, rng=rng, breaks=0)
            gold(D, side, [(um, v0), (um, vm - 26)], 0.6, 0.55, rng=rng, least=0.5)
            gold(D, side, [(um, vm + 26), (um, v1)], 0.6, 0.55, rng=rng, least=0.5)
        # ---- the dado: its cap catches light, a shadow under the cap, joints, the plinth's edge
        gold(D, side, [(near, V_CAP), (ZB, V_CAP)], 1.2, 0.95, 1.6, rng=rng, breaks=0.02)
        dark_line(D, [room.wall(side, near, V_DADO - 1.5, 0.5), room.wall(side, ZB, V_DADO - 1.5, 0.5)], 1.6, 0.55)
        for u in np.arange(-30.0, ZB, 150.0):
            dark_line(D, [room.wall(side, u, V_PLINTH, 0.5), room.wall(side, u, V_DADO - 2, 0.5)], 1.0, 0.5)
            gold(D, side, [(u + 3, V_PLINTH + 6), (u + 3, V_DADO - 8)], 0.5, 0.35, 1.0, least=0.5)
        lit_line(D, room, [room.wall(side, near, V_PLINTH, 0.5), room.wall(side, ZB, V_PLINTH, 0.5)], room.wall_n(side), "#8a8078", 1.0, 0.7, 1.5)
        for _ in range(26):                                  # veins in the green marble
            u, v = near + rng.random() * (ZB - near), V_PLINTH + 8 + rng.random() * (V_DADO - V_PLINTH - 16)
            run = [(u, v)]
            for _k in range(3):
                run.append((run[-1][0] + 8 + rng.random() * 26, run[-1][1] + rng.normal(0, 9)))
            lit_line(D, room, [room.wall(side, a_, min(max(b_, V_PLINTH + 3), V_DADO - 3), 0.5) for a_, b_ in run], room.wall_n(side), "#5a9480", 0.6, 0.30, 1.1, least=0.5)
        # ---- the frieze: two hairlines and a running key
        gold(D, side, [(near, V_MAIN + 13), (ZB, V_MAIN + 13)], 0.6, 0.5, rng=rng, least=0.5)
        gold(D, side, [(near, V_FRIEZE - 13), (ZB, V_FRIEZE - 13)], 0.6, 0.5, rng=rng, least=0.5)
        for u in np.arange(near + 10, ZB - 20, 44.0):
            gold(D, side, [(u, V_MAIN + 18), (u, V_FRIEZE - 18), (u + 22, V_FRIEZE - 18), (u + 22, V_MAIN + 18), (u + 44, V_MAIN + 18)], 0.8, 0.6, 1.1, least=0.5, breaks=0)
    # ---- the back wall
    for (a, b) in RED_BACK:
        u0, u1, v0, v1 = a + 13, b - 13, V_CAP + 27, V_MAIN - 27
        gold(D, "B", [(u0, v0), (u1, v0), (u1, v1), (u0, v1), (u0, v0)], 1.5, 0.95, rng=rng)
        gold(D, "B", [(u0 + 9, v0 + 9), (u1 - 9, v0 + 9), (u1 - 9, v1 - 9), (u0 + 9, v1 - 9), (u0 + 9, v0 + 9)], 0.6, 0.55, rng=rng, breaks=0.12, least=0.5)
    for sgn in (-1, 1):
        gold(D, "B", [(sgn * (NICHE_W + 17), V_CAP), (sgn * A, V_CAP)], 1.2, 0.95, 1.6)
        dark_line(D, [room.wall("B", sgn * (NICHE_W + 17), V_DADO - 1.5, 0.5), room.wall("B", sgn * A, V_DADO - 1.5, 0.5)], 1.6, 0.55)
        gold(D, "B", [(sgn * (NICHE_W + 30), V_MAIN + 13), (sgn * A, V_MAIN + 13)], 0.6, 0.5, least=0.5)
        gold(D, "B", [(sgn * (NICHE_W + 22), V_FRIEZE - 13), (sgn * A, V_FRIEZE - 13)], 0.6, 0.5, least=0.5)
        for u in np.arange(NICHE_W + 34, A - 30, 44.0):
            gold(D, "B", [(sgn * u, V_MAIN + 18), (sgn * u, V_FRIEZE - 18), (sgn * (u + 22), V_FRIEZE - 18), (sgn * (u + 22), V_MAIN + 18), (sgn * (u + 44), V_MAIN + 18)], 0.8, 0.6, 1.1, least=0.5, breaks=0)
    for R_, wd, g in ((NICHE_W + 17, 1.4, 1.5), (NICHE_W, 1.1, 0.9), (NICHE_W + 8.5, 0.6, 1.0)):     # the niche's arch
        arc = [(-R_, 0.0), (-R_, NICHE_SPRING)] + [(-math.cos(t) * R_, NICHE_SPRING + math.sin(t) * R_) for t in np.linspace(0, math.pi, 22)] + [(R_, NICHE_SPRING), (R_, 0.0)]
        gold(D, "B", arc, wd, 0.9, g, breaks=0)
    stars = np.random.default_rng(seed + 5)                                                             # the vault of the niche is sown with small gilt stars
    placed = []
    while len(placed) < 17:
        sx_, sy_ = (stars.random() * 2 - 1) * (NICHE_W - 14), NICHE_SPRING - 70 + stars.random() * (NICHE_W + 56)
        if sx_ * sx_ + max(sy_ - NICHE_SPRING, 0) ** 2 > (NICHE_W - 14) ** 2 or any((sx_ - a_) ** 2 + (sy_ - b_) ** 2 < 34 ** 2 for a_, b_ in placed):
            continue
        if abs(sx_) < 42 and sy_ < 470:                                                                # none behind his head
            continue
        placed.append((sx_, sy_))
        px, py = P(*room.wall("B", sx_, sy_, 0.5))
        big = stars.random() < 0.35
        D.ellipse(px, py, 0.9 if big else 0.6, 0.9 if big else 0.6, room.tone(GOLD, (sx_, sy_, ZB), TO_US, 2.3 if big else 1.7), 0.9 if big else 0.7, fine=True)
        if big:
            D.line([(px - 1.8, py), (px + 1.8, py)], room.tone(GOLD, (sx_, sy_, ZB), TO_US, 1.6), 0.5, 0.5)
            D.line([(px, py - 1.8), (px, py + 1.8)], room.tone(GOLD, (sx_, sy_, ZB), TO_US, 1.6), 0.5, 0.5)
    for t in np.linspace(0.12, math.pi - 0.12, 15):                                                    # little bosses round the arch
        px, py = P(*room.wall("B", -math.cos(t) * (NICHE_W + 8.5), NICHE_SPRING + math.sin(t) * (NICHE_W + 8.5), 0.5))
        D.ellipse(px, py, 0.9, 0.9, room.tone(GOLD, (0, 500, ZB), TO_US, 1.5), 0.8, fine=True)
    # ---- where planes meet
    for sgn in (-1, 1):
        dark_line(D, [(sgn * A, 0, ZB), (sgn * A, HC, ZB)], 2.2, 0.6)
        dark_line(D, [(sgn * A, 0, near), (sgn * A, 0, ZB)], 2.4, 0.7)
        dark_line(D, [(sgn * A, HC, 200), (sgn * A, HC, ZB)], 2.4, 0.6)
    dark_line(D, [(-A, 0, ZB), (A, 0, ZB)], 2.4, 0.7)
    dark_line(D, [(-A, HC, ZB), (A, HC, ZB)], 2.4, 0.6)
    # ---- the floor's joints, said again: a dark line, broken, and a pale lip on the slab beyond
    for i in range(-3, 4):
        xj = i * TILE
        dark_line(D, [(xj, 0, -60), (xj, 0, ZB)], 1.5, 0.50, "#241a18", rng, 0.06)
    for j in range(0, 11):
        zj = j * TILE
        dark_line(D, [(-A, 0, zj), (A, 0, zj)], 1.5, 0.50, "#241a18", rng, 0.06, step_cm=80.0)
        if zj < 700:
            lit_line(D, room, [(-360, 0, zj + 2.2), (360, 0, zj + 2.2)], UP, "#d8ccb0", 0.7, 0.30, 1.2, least=0.5, rng=rng, breaks=0.3, step_cm=70.0)
    for sgn in (-1, 1):
        dark_line(D, [(sgn * 360.0, 0, -60), (sgn * 360.0, 0, ZB)], 1.6, 0.5, "#1a1414", rng, 0.05)
    # ---- cracks and chips in the paving
    for (cx, cz, n_) in ((250, 80, 5), (-180, 330, 4), (60, 620, 4), (-70, 150, 3), (300, 420, 3), (-250, 760, 3), (130, 300, 3)):
        run = [(cx, cz)]
        ang = rng.random() * 6.28
        for _k in range(n_):
            ang += rng.normal(0, 0.7)
            run.append((run[-1][0] + math.cos(ang) * (14 + rng.random() * 22), run[-1][1] + math.sin(ang) * (14 + rng.random() * 22)))
        dark_line(D, [(a_, 0, b_) for a_, b_ in run], 0.8, 0.55, "#1c1414", step_cm=200)
    for _ in range(26):                                      # corners knocked off slabs
        i, j = rng.integers(-3, 4), rng.integers(0, 7)
        cx, cz = i * TILE + rng.normal(0, 1.5), j * TILE + rng.normal(0, 1.5)
        s = 3 + rng.random() * 6
        px, py = P(cx, 0, cz)
        k_ = room.k(cz)
        D.poly([(px - s * k_, py), (px, py - s * k_ * 0.5), (px + s * k_ * 0.8, py + s * k_ * 0.2)], "#1c1616", 0.45, fine=True)
    # ---- cobwebs in the top corners of the far wall
    for sgn in (-1, 1):
        c = P(sgn * (A - 2), HC - 4, ZB - 2)
        for i in range(5):
            a = (0.15 + i * 0.28)
            e = (c[0] - sgn * math.cos(a) * 34, c[1] + math.sin(a) * 30)
            D.line([c, e], "#8a8a94", 0.5, 0.13)
        for r_ in (10, 19, 28):
            D.line([(c[0] - sgn * math.cos(a) * r_, c[1] + math.sin(a) * r_ * 0.9) for a in np.linspace(0.15, 1.27, 6)], "#8a8a94", 0.5, 0.10)


# ======================================================================== plain blocks
def block(D, x0, x1, y0, y1, z0, z1, albedo, gain=1.0, nu=2, nv=2, rng=None, jitter=0.04, top_gain=0.95, fine=False):
    """A squared block in the room: the faces we can see, each in the light of its own place.
    -> dict of its Faces (front, top, side)."""
    out = {}
    if x0 > 0:
        out["side"] = Face(room, (x0, y0, z1), (x0, y0, z0), (x0, y1, z0), (x0, y1, z1), TO_LEFT).fill(D, albedo, max(1, nu // 2), nv, rng, jitter, gain * 0.9, fine=fine)
    if x1 < 0:
        out["side"] = Face(room, (x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0), TO_RIGHT).fill(D, albedo, max(1, nu // 2), nv, rng, jitter, gain * 0.9, fine=fine)
    if y1 < cam.eye:
        out["top"] = Face(room, (x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1), UP).fill(D, albedo, nu, 1, rng, jitter, gain * top_gain, fine=fine)
    out["front"] = Face(room, (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), TO_US).fill(D, albedo, nu, nv, rng, jitter, gain, fine=fine)
    return out


def tones(albedo, pos, gain=1.0):
    """Four tones of one stuff where the god sits: turned to the fire and the floor's light; square to us;
    turned away to the left; tops and hollows."""
    return (room.tone(albedo, pos, (0.50, -0.30, -0.80), gain * 1.18), room.tone(albedo, pos, (0.0, 0.0, -1.0), gain * 0.95),
            room.tone(albedo, pos, (-0.62, 0.15, -0.75), gain * 0.72), room.tone(albedo, pos, (-0.4, 0.85, -0.3), gain * 0.46))


# ======================================================================== the god
def pedestal(D, seed=31):
    rng = np.random.default_rng(seed)
    stone = "#7e746a"
    px, z0, z1 = PED["x"], PED["z0"], PED["z1"]
    block(D, -px - 10, px + 10, 0, 14, z0 - 10, z1 + 4, stone, 0.95, 6, 1, rng)
    block(D, -px - 4, px + 4, 14, 24, z0 - 4, z1, stone, 1.08, 6, 1, rng)
    die = block(D, -px + 6, px - 6, 24, 126, z0 + 4, z1 - 4, stone, 0.98, 8, 4, rng)["front"]
    block(D, -px - 4, px + 4, 126, 138, z0 - 4, z1, stone, 1.12, 6, 1, rng)
    block(D, -px - 10, px + 10, 138, PED["top"], z0 - 10, z1 + 4, stone, 1.18, 6, 1, rng, top_gain=0.80)
    # edges: light along the tops of the mouldings, dark under them
    for (hx, y, zz, g) in ((px + 10, 14, z0 - 10, 1.5), (px + 4, 24, z0 - 4, 1.5), (px + 4, 138, z0 - 4, 1.7), (px + 10, PED["top"], z0 - 10, 1.9)):
        lit_line(D, room, [(-hx, y, zz), (hx, y, zz)], TO_US, stone, 1.2, 0.85, g)
    for (hx, y, zz) in ((px + 4, 126, z0 - 4), (px + 10, 138, z0 - 10)):
        dark_line(D, [(-hx, y, zz), (hx, y, zz)], 2.4, 0.6)
    dark_line(D, [(-px + 6, 122, z0 + 4), (px - 6, 122, z0 + 4)], 4.0, 0.35)
    dark_line(D, [(-px - 10, 0, z0 - 10), (px + 10, 0, z0 - 10)], 2.4, 0.7)
    # a bronze plate let into the front (its letters are cut in the last pass), and two swags of dry laurel
    die.rect(D, 0.27, 0.73, 0.50, 0.92, BRONZE, 1.05, fine=False)
    die.line(D, [(0.27, 0.50), (0.27, 0.92), (0.73, 0.92)], BRONZE, 1.4, 0.9, 1.9)
    die.line(D, [(0.27, 0.50), (0.73, 0.50), (0.73, 0.92)], BRONZE, 1.4, 0.8, 0.5)
    for (ua, ub) in ((0.03, 0.25), (0.75, 0.97)):
        pts = [(lerp(ua, ub, t), 0.95 - 0.26 * math.sin(t * math.pi)) for t in np.linspace(0, 1, 9)]
        die.line(D, pts, "#5a6a3a", 5.5, 0.95, 1.0)
        die.line(D, [(u, v + 0.02) for u, v in pts[1:-1]], "#8a9a52", 2.0, 0.8, 1.3)
        for (u, v) in (pts[0], pts[-1]):
            die.dot(D, u, v + 0.01, 3.0, BRONZE, 1.8)
            die.line(D, [(u, v), (u + 0.01, v - 0.2), (u - 0.012, v - 0.34)], "#b03a2a", 1.6, 0.9, 1.2)       # a ribbon end
    PLACES["die"] = die
    wx, wz = -78.0, 1068.0                                    # a wreath someone left at his feet, gone brown
    cx, cy = P(wx, PED["top"], wz)
    k = room.k(wz)
    sq = room.squash(PED["top"], wz)
    for t in np.linspace(0, 2 * math.pi, 14, endpoint=False):
        D.ellipse(cx + math.cos(t) * 15 * k, cy + math.sin(t) * 15 * k * sq - 1.0, 2.0, 1.2, room.tone("#6a7a3a" if math.sin(t * 3) > 0 else "#8a6a34", (wx, 152, wz), (0.3, 0.6, -0.7), 1.6), fine=True)
    lx, ly = P(82, PED["top"], 1062)                           # and a small clay lamp, out
    D.poly([(lx - 4, ly - 0.5), (lx - 2, ly - 3), (lx + 3, ly - 3), (lx + 5.5, ly - 1.4), (lx + 3, ly + 0.6), (lx - 3, ly + 0.6)], room.tone("#b4683e", (82, 152, 1062), (0.4, 0.3, -0.8), 1.6))
    return die


def statue(D, seed=33):
    """The old god: seated, bearded, his mantle drawn up over his head, a pruning hook in his right hand,
    his feet bound round with white wool. Our own figure, drawn from no statue that exists."""
    T = PED["top"]
    zb, zt, zh, zk, zf = 1205.0, 1165.0, 1160.0, 1072.0, 1060.0
    G = 1.75                                                  # the god catches the light: he is the second thing we look at
    SC = STATUE_SCALE
    at = (0.0, 300.0, 1120.0)

    def Q(x_, y_, z):
        return P(x_ * SC, T + (y_ - T) * SC, z)

    def S(pts, z):
        return [Q(x_, y_, z) for x_, y_ in pts]

    IVO = tones("#e2bf90", at, G)                             # old ivory gone the color of honey: face, hands, feet
    MAN = tones("#c8963e", at, G)                             # the mantle: faded gilding over ochre
    TUN = tones("#c9b488", at, G)                             # the tunic under it
    BRD = tones("#e0dccc", at, G)                             # beard and hair
    WOD = tones("#5a3422", at, G * 0.9)                       # the throne
    GLD = tones("#e8b848", at, G)
    WOL = tones("#f6f1e2", at, G * 1.12)                      # the wool
    RDC = tones("#8a2a20", at, G)
    px = SC * 0.40                                            # about one centimetre in pixels here

    # ---- the throne: a high back with knobs, a block of a seat, a footstool
    D.poly(S([(-62, 252), (62, 252), (62, 394), (-62, 394)], zb), WOD[2])
    D.poly(S([(0, 252), (62, 252), (62, 394), (0, 394)], zb), WOD[1], 0.7)
    D.poly(S([(-62, 384), (62, 384), (62, 396), (-62, 396)], zb), WOD[1])
    D.line(S([(-62, 396), (62, 396)], zb), GLD[2], 0.9, 0.9)
    D.line(S([(-54, 262), (-54, 378), (54, 378), (54, 262)], zb), GLD[2], 0.7, 0.8)
    for sx in (-62, 62):
        cx, cy = Q(sx, 404, zb)
        D.ellipse(cx, cy, 3.2, 3.6, WOD[1])
        D.ellipse(cx + 0.7, cy + 0.6, 1.5, 1.6, GLD[0 if sx > 0 else 2], 0.9, fine=True)
    D.poly(S([(-66, T), (66, T), (66, 250), (-66, 250)], 1104), WOD[2])
    D.poly(S([(40, T), (66, T), (66, 250), (40, 250)], 1104), WOD[1])
    for sx in (-66, -52, 52, 66):
        D.line(S([(sx, T + 2), (sx, 248)], 1104), GLD[2 if sx < 0 else 1], 0.8, 0.8)
    D.poly(S([(-66, 250), (66, 250), (64, 263), (-64, 263)], 1104), RDC[2])
    D.poly(S([(30, 250), (66, 250), (64, 263), (30, 263)], 1104), RDC[0], 0.8)
    D.line(S([(-64, 263), (64, 263)], 1104), RDC[1], 0.8, 0.8)
    # footstool
    D.poly(S([(-42, T), (42, T), (42, 172), (-42, 172)], 1048), WOD[1])
    D.poly([Q(-42, 172, 1048), Q(42, 172, 1048), Q(42, 172, 1098), Q(-42, 172, 1098)], WOD[3])
    D.poly(S([(10, T), (42, T), (42, 172), (10, 172)], 1048), WOD[0], 0.6)
    D.line(S([(-38, T + 5), (-38, 168), (38, 168), (38, T + 5), (-38, T + 5)], 1048), GLD[1], 0.7, 0.85)
    D.line(S([(-42, 172), (42, 172)], 1048), GLD[0], 0.8, 0.9)

    # ---- the mantle behind him: over the head, over both shoulders, down to the seat
    cloak = [(-54, 366), (-38, 392), (-27, 418), (-19, 434), (-8, 441), (8, 441), (19, 434), (27, 418), (38, 392), (54, 366), (64, 330), (68, 290), (64, 262), (-64, 262), (-68, 290), (-64, 330)]
    D.poly(S(cloak, zt), MAN[2])
    D.poly(S([(4, 441), (19, 434), (27, 418), (38, 392), (54, 366), (64, 330), (68, 290), (64, 262), (40, 262), (44, 330), (36, 368), (18, 400), (12, 428)], zt), MAN[1])
    D.poly(S([(38, 392), (54, 366), (64, 330), (68, 290), (64, 262), (54, 262), (58, 300), (56, 334), (48, 362)], zt), MAN[0])
    D.poly(S([(-19, 434), (-8, 441), (8, 441), (19, 434), (12, 431), (0, 435), (-12, 431)], zt), MAN[3], 0.9)          # the top of the head is turned from the light
    # ---- the body: tunic, and the mantle's thick fold from his left shoulder across to his right hip
    D.poly(S([(-36, 374), (36, 374), (42, 332), (40, 296), (-40, 296), (-42, 332)], zt), TUN[1])
    D.poly(S([(-36, 374), (-10, 374), (-14, 296), (-40, 296), (-42, 332)], zt), TUN[2])
    D.poly(S([(14, 372), (36, 374), (42, 332), (40, 296), (22, 296), (26, 334)], zt), TUN[0], 0.85)
    for (xa, xb) in ((-22, -8), (-8, -2), (8, 2), (22, 9)):                              # folds falling to the girdle
        D.line(S([(xa, 372), (xb, 304)], zt), TUN[3], 0.8, 0.5)
    band = [(46, 376), (56, 362), (30, 330), (2, 306), (-30, 296), (-42, 296), (-40, 310), (-10, 322), (20, 346)]
    D.poly(S(band, zt), MAN[1])
    D.poly(S([(46, 376), (56, 362), (30, 330), (2, 306), (-30, 296), (-20, 301), (8, 314), (34, 340), (50, 366)], zt), MAN[0], 0.9)
    D.line(S([(46, 376), (20, 346), (-10, 322), (-40, 310)], zt), MAN[3], 0.9, 0.7)
    D.line(S([(-36, 298), (40, 298)], zt), MAN[3], 1.0, 0.6)
    D.poly(S([(-12, 374), (12, 374), (9, 352), (0, 346), (-9, 352)], zt), TUN[3], 0.55)          # the beard's shadow on his chest
    D.poly(S([(-40, 296), (-42, 332), (-37, 362), (-33, 330), (-34, 296)], zt), TUN[3], 0.6)     # and the dark of his right side

    # ---- lap and legs under the mantle
    D.poly([Q(-42, 298, 1150), Q(42, 298, 1150), Q(48, 279, zk), Q(-48, 279, zk)], MAN[3])
    D.poly([Q(4, 298, 1150), Q(42, 298, 1150), Q(48, 279, zk), Q(8, 279, zk)], MAN[2], 0.8)
    skirt = [(-48, 279), (48, 279), (44, 236), (41, 196), (-41, 196), (-44, 236)]
    D.poly(S(skirt, zk), MAN[2])
    for sx, tn in ((-1, (MAN[1], MAN[2])), (1, (MAN[0], MAN[1]))):                      # the two shins: forms under the cloth
        c = 25 * sx
        D.poly(S([(c - 15, 280), (c + 15, 280), (c + 12, 236), (c * 0.72 + 10, 198), (c * 0.72 - 10, 198), (c - 12, 236)], zk), tn[1])
        D.poly(S([(c - 3, 280), (c + 15, 280), (c + 12, 236), (c * 0.72 + 10, 198), (c * 0.72 + 1, 198), (c + 2, 236)], zk), tn[0])
        kx, ky = Q(c, 276, zk)
        D.ellipse(kx, ky, 17 * px, 9 * px, tn[1])                                        # the knee
        D.ellipse(kx + 4 * px, ky + 0.8 * px, 10 * px, 6 * px, tn[0])
    for i, yy in enumerate((262, 246, 228, 210)):                                       # the cloth sags between the knees
        w_ = 10 - i * 1.2
        D.line(S([(-w_, yy + 5), (-w_ * 0.5, yy - 2), (0, yy - 4), (w_ * 0.5, yy - 2), (w_, yy + 5)], zk), MAN[3], 0.9, 0.75)
        D.line(S([(-w_ * 0.5, yy - 5), (0, yy - 7), (w_ * 0.5, yy - 5)], zk), MAN[1], 0.7, 0.5)
    for sx in (-1, 1):
        D.line(S([(sx * 46, 276), (sx * 43, 236), (sx * 40, 198)], zk), MAN[3], 0.8, 0.6)
        D.line(S([(sx * 38, 270), (sx * 37, 236), (sx * 33, 200)], zk), MAN[3], 0.6, 0.4)
    hem = [(x_, 198 - (3 if i % 2 else 0)) for i, x_ in enumerate(np.linspace(-41, 41, 13))]
    D.line(S(hem, zk), MAN[3], 0.9, 0.7)

    # ---- the feet on the footstool, bound round and round with white wool
    for sx in (-1, 1):
        D.poly(S([(sx * 5, 172.5), (sx * 28, 172.5), (sx * 29, 181), (sx * 23, 187), (sx * 6, 187)], zf), IVO[1 if sx > 0 else 2])
        D.poly(S([(sx * 5, 172.5), (sx * 28, 172.5), (sx * 28.5, 176), (sx * 5, 176)], zf), IVO[0 if sx > 0 else 1], 0.9)
        for t in (10, 15, 20, 24.5):
            D.line(S([(sx * t, 172.8), (sx * t, 177.5)], zf), IVO[3], 0.55, 0.75)
    D.poly(S([(-32, 181), (32, 181), (33, 201), (-33, 201)], zf), WOL[1])
    D.poly(S([(3, 181), (32, 181), (33, 201), (5, 201)], zf), WOL[0])
    D.poly(S([(-32, 181), (-20, 181), (-22, 201), (-33, 201)], zf), WOL[2], 0.8)
    for i in range(7):                                                                   # the turns of the band, crossing
        xa = -31 + i * 9.8
        D.line(S([(xa, 182), (xa + 7, 200)], zf), "#8f8aa2", 0.6, 0.8)
        D.line(S([(xa + 7, 182), (xa, 200)], zf), "#b8b4c0", 0.5, 0.5)
    D.line(S([(-33, 201), (33, 201)], zf), "#fffdf2", 0.7, 0.9)
    D.line(S([(-32, 181), (32, 181)], zf), "#6e6a80", 0.7, 0.8)
    D.poly(S([(-6, 185), (6, 185), (7, 196), (-7, 196)], zf), WOL[0])                    # the knot, and its two short ends
    D.line(S([(-6, 190.5), (6, 190.5)], zf), "#8f8ca0", 0.6, 0.7)
    D.poly(S([(-7, 186), (-13, 178), (-9, 177), (-4, 185)], zf), WOL[1])
    D.poly(S([(7, 186), (14, 177.5), (10, 176.5), (4, 185)], zf), WOL[0])

    # ---- arms. His right (our left) is bare from the elbow and holds the hook; his left lies along his knee in the mantle
    D.poly([Q(-54, 366, zt), Q(-40, 366, zt), Q(-46, 314, 1150), Q(-66, 316, 1150)], TUN[2])
    D.poly([Q(-66, 318, 1150), Q(-48, 318, 1150), Q(-36, 294, 1086), Q(-50, 290, 1086)], IVO[2])
    D.poly([Q(-58, 318, 1150), Q(-48, 318, 1150), Q(-36, 294, 1086), Q(-43, 292, 1086)], IVO[1])
    D.poly([Q(40, 366, zt), Q(56, 364, zt), Q(68, 316, 1150), Q(48, 314, 1150)], MAN[0])
    D.poly([Q(48, 318, 1150), Q(68, 318, 1150), Q(50, 290, 1086), Q(34, 292, 1086)], MAN[1])
    D.poly([Q(58, 318, 1150), Q(68, 318, 1150), Q(50, 290, 1086), Q(44, 291, 1086)], MAN[0])
    D.line([Q(50, 316, 1150), Q(38, 294, 1086)], MAN[3], 0.7, 0.6)
    hx, hy = Q(40, 287, 1080)
    D.ellipse(hx, hy, 10.5 * px, 6.5 * px, IVO[1])                                       # his left hand, flat on the knee
    D.ellipse(hx + 2.5 * px, hy + 0.8 * px, 6.5 * px, 4 * px, IVO[0])
    D.line([(hx - 7 * px, hy + 3 * px), (hx + 7 * px, hy + 4 * px)], IVO[3], 0.5, 0.6)

    # ---- the pruning hook: a short dark staff, and a blade that goes up, over and down again like a claw
    zq = 1090.0
    D.line([Q(-43, 278, 1084), Q(-48, 312, zq), Q(-51, 336, zq)], WOD[3], 1.7)
    D.line([Q(-42.3, 280, 1084), Q(-50.3, 334, zq)], WOD[0], 0.5, 0.7)
    D.line([Q(-51, 334, zq), Q(-52, 342, zq)], GLD[0], 2.1)                               # a bronze collar
    c0 = (-70.0, 352.0)
    outer = [(-52, 340)] + [(c0[0] + math.cos(a) * 18.5, c0[1] + math.sin(a) * 19.5) for a in np.linspace(-0.2, 3.5, 13)]
    inner = [(c0[0] + math.cos(a) * lerp(17.0, 11.5, t), c0[1] + math.sin(a) * lerp(18.0, 12.5, t)) for t, a in zip(np.linspace(0, 1, 11), np.linspace(3.4, 0.25, 11))] + [(-57.5, 341)]
    D.poly(S(outer + inner, zq), GLD[1])
    half = [(c0[0] + math.cos(a) * 18.5, c0[1] + math.sin(a) * 19.5) for a in np.linspace(-0.2, 1.5, 7)] + [(c0[0] + math.cos(a) * 14.5, c0[1] + math.sin(a) * 15.5) for a in np.linspace(1.5, 0.2, 6)]
    D.poly(S(half, zq), GLD[0])
    D.line(S(inner[:-1], zq), GLD[3], 0.6, 0.85)                                          # the cutting edge, in shadow
    D.line(S([(c0[0] + math.cos(a) * 18.5, c0[1] + math.sin(a) * 19.5) for a in np.linspace(0.5, 2.4, 8)], zq), "#fff2b8", 0.7, 0.9)
    grip = Q(-44, 290, 1084)
    D.ellipse(grip[0], grip[1], 8.5 * px, 7 * px, IVO[1])                                  # his right hand round the staff
    D.ellipse(grip[0] + 2 * px, grip[1] + 1 * px, 5 * px, 4 * px, IVO[0])
    D.line([(grip[0] - 6.5 * px, grip[1] - 1.5 * px), (grip[0] + 7 * px, grip[1] + 0.5 * px)], IVO[3], 0.5, 0.6)

    # ---- the head: the mantle's shadow round the face, the face, the long beard
    D.poly(S([(-20, 392), (-22, 414), (-15, 430), (0, 435), (15, 430), (22, 414), (20, 392), (0, 384)], zh), MAN[3])
    face = [(-13, 398), (-14, 412), (-11, 423), (0, 426.5), (11, 423), (14, 412), (13, 398), (0, 392)]
    D.poly(S(face, zh), IVO[1])
    D.poly(S([(1, 426.5), (11, 423), (14, 412), (13, 398), (4, 394), (4.5, 412), (3, 423)], zh), IVO[0])
    D.poly(S([(-13, 398), (-14, 412), (-11, 423), (-7, 425), (-8.5, 412), (-8, 398)], zh), IVO[2], 0.9)
    D.poly(S([(-12, 419.5), (0, 422), (12, 419.5), (11, 423.5), (0, 427), (-11, 423.5)], zh), mixc(IVO[2], IVO[3], 0.55), 0.9)   # the brow in the mantle's shade
    for sx in (-1, 1):                                                                   # heavy brows, and the eyes deep under them
        D.line(S([(sx * 2.4, 417.6), (sx * 6, 418.4), (sx * 10.5, 416.8)], zh), "#4a3428", 0.7, 0.85)
        ex, ey = Q(sx * 6.2, 414.6, zh)
        D.ellipse(ex, ey, 1.2, 0.75, "#241a1a", 1.0, fine=True)
    D.line(S([(0.6, 416), (0.9, 406.8)], zh), mixc(IVO[0], "#fff0d0", 0.4), 0.9, 0.95)        # the nose, lit along its ridge
    D.line(S([(-1.9, 414.5), (-1.6, 407)], zh), IVO[3], 0.6, 0.7)
    D.line(S([(-2.4, 405.8), (3.0, 405.8)], zh), IVO[3], 0.6, 0.8)
    beard = [(-13, 404), (-13, 392), (-10, 374), (-5, 358), (0, 352), (5, 358), (10, 374), (13, 392), (13, 404), (8, 402.5), (3, 404.6), (0, 403.6), (-3, 404.6), (-8, 402.5)]
    D.poly(S(beard, zh), BRD[1])
    D.poly(S([(0, 403.6), (3, 404.6), (8, 402.5), (13, 404), (13, 392), (10, 374), (5, 358), (2, 356), (5, 378), (4, 396)], zh), BRD[0])
    D.poly(S([(-13, 404), (-13, 392), (-10, 374), (-6, 360), (-6, 380), (-8.5, 400)], zh), BRD[2])
    for bx in (-8, -4, 0, 4, 8):
        D.line(S([(bx, 396), (bx * 0.9 + 0.8, 384), (bx * 0.6, 366)], zh), BRD[3], 0.5, 0.5)
    for sx in (-1, 1):                                                                   # the moustache, drooping
        D.line(S([(sx * 0.8, 404.6), (sx * 5, 403.4), (sx * 9, 399.5)], zh), BRD[0] if sx > 0 else BRD[1], 1.0, 0.95)
    D.line(S([(-3.6, 400.2), (0, 399.4), (3.6, 400.2)], zh), "#5a4840", 0.7, 0.85)          # the mouth, under it
    D.line(S([(-12.5, 419), (-14, 409)], zh), BRD[1], 1.0, 0.8)                            # grey hair at the temples
    D.line(S([(12.5, 419), (14, 409)], zh), BRD[0], 1.0, 0.9)
    # the mantle's edge round the face catches the fire on his left side (our right)
    D.line(S([(8, 441), (19, 434), (27, 418), (38, 392), (54, 366)], zt), MAN[0], 0.9, 0.9)
    D.line(S([(15, 430), (22, 414), (20, 394)], zh), MAN[1], 0.8, 0.8)
    D.line(S([(-15, 430), (-22, 414), (-20, 394)], zh), MAN[2], 0.8, 0.7)
    D.line(S([(54, 366), (64, 330), (68, 290), (64, 264)], zt), "#f6d48a", 0.7, 0.7)
    # a border of gilt dots along the mantle's fold and its hem
    for t in np.linspace(0.06, 0.94, 11):
        bx_, by_ = lerp(50.0, -36.0, t), lerp(367.0, 301.0, t) + math.sin(t * math.pi) * 3.0
        cx, cy = Q(bx_, by_, zt)
        D.ellipse(cx, cy, 0.75, 0.75, GLD[0], 0.9, fine=True)
    for x_ in np.linspace(-36, 36, 10):
        cx, cy = Q(x_, 203, zk)
        D.ellipse(cx, cy, 0.75, 0.75, GLD[0 if x_ > 0 else 1], 0.85, fine=True)


def standards(D, seed=35):
    """Three old standards of the legions leaning in the far left corner: the eagle, a staff of discs with
    a hand on top, and a small red flag on a cross-bar."""
    at = (-340.0, 220.0, 1240.0)
    wood = room.tone("#6a4a30", at, TO_US, 1.5)
    GL = tones("#e0b040", at, 1.9)
    RD = tones("#a02a22", at, 1.8)
    # the eagle
    f0, t0 = P(-356, 0, 1236), P(-384, 292, 1254)
    D.line([f0, t0], wood, 1.6, fine=False)
    D.line([f0, (f0[0] + 0.4, f0[1] - 6)], "#3a3a44", 1.4)
    ex, ey = t0
    D.poly([(ex - 5.5, ey + 1), (ex + 5.5, ey + 1), (ex + 4, ey + 3.2), (ex - 4, ey + 3.2)], GL[1])                       # the thunderbolt it stands on
    D.poly([(ex - 1.8, ey + 1), (ex + 1.8, ey + 1), (ex + 2.2, ey - 6), (ex + 0.5, ey - 9.5), (ex - 2.2, ey - 7.5)], GL[1])  # body and head
    D.poly([(ex - 1.5, ey - 3), (ex - 8.5, ey - 12.5), (ex - 6.5, ey - 5.5), (ex - 4, ey - 1.5)], GL[2])                  # wings raised
    D.poly([(ex + 1.5, ey - 3), (ex + 9, ey - 12), (ex + 6.5, ey - 5), (ex + 4, ey - 1.5)], GL[0])
    D.line([(ex + 0.5, ey - 9.5), (ex + 3.4, ey - 8.6)], GL[0], 1.0)                                                       # the beak
    D.line([(ex + 2, ey - 3), (ex + 8, ey - 11)], "#fff0b0", 0.6, 0.8)
    # the staff of discs
    f1, t1 = P(-326, 0, 1241), P(-346, 304, 1255)
    D.line([f1, t1], wood, 1.6, fine=False)
    for i, tt in enumerate((0.86, 0.76, 0.66, 0.56)):
        cx, cy = lerp(f1[0], t1[0], tt), lerp(f1[1], t1[1], tt)
        D.ellipse(cx, cy, 3.6, 3.6, GL[2])
        D.ellipse(cx + 0.5, cy + 0.4, 2.6, 2.6, GL[1 if i % 2 else 0])
        D.ellipse(cx, cy, 0.9, 0.9, GL[3], 0.9, fine=True)
    cx, cy = lerp(f1[0], t1[0], 0.47), lerp(f1[1], t1[1], 0.47)
    D.line([(cx - 4, cy - 2), (cx - 2.5, cy + 1.5), (cx, cy + 2.4), (cx + 2.5, cy + 1.5), (cx + 4, cy - 2)], GL[1], 1.2)    # a crescent
    D.line([(t1[0] - 6, t1[1] + 9), (t1[0] + 6, t1[1] + 8)], wood, 1.3)                                                     # cross-bar and its two ribbons
    for sx in (-1, 1):
        D.line([(t1[0] + sx * 5.5, t1[1] + 8.5), (t1[0] + sx * 6.5, t1[1] + 19)], RD[1 if sx > 0 else 2], 1.3)
    D.poly([(t1[0] - 2.2, t1[1] + 2), (t1[0] + 2.2, t1[1] + 2), (t1[0] + 2.8, t1[1] - 5), (t1[0] + 1, t1[1] - 8.5), (t1[0] - 1.4, t1[1] - 8.5), (t1[0] - 3, t1[1] - 4)], GL[1])   # the open hand
    D.line([(t1[0] + 1.2, t1[1] - 8), (t1[0] + 2.4, t1[1] - 4)], GL[0], 0.8)
    # the little flag
    f2, t2 = P(-296, 0, 1238), P(-304, 262, 1253)
    D.line([f2, t2], wood, 1.5, fine=False)
    D.line([(t2[0] - 9, t2[1] + 4), (t2[0] + 9, t2[1] + 3)], wood, 1.4)
    D.poly([(t2[0] - 8, t2[1] + 4.5), (t2[0] + 8, t2[1] + 3.5), (t2[0] + 7, t2[1] + 20), (t2[0] - 7.5, t2[1] + 21)], RD[2])
    D.poly([(t2[0] + 1, t2[1] + 4), (t2[0] + 8, t2[1] + 3.5), (t2[0] + 7, t2[1] + 20), (t2[0] + 2, t2[1] + 20.5)], RD[1])
    D.line([(t2[0] - 2, t2[1] + 6), (t2[0] - 1.5, t2[1] + 19)], RD[3], 0.7, 0.6)
    for i in range(8):
        fx = t2[0] - 7.5 + i * 2.1
        D.line([(fx, t2[1] + 20.5), (fx, t2[1] + 23.5)], GL[1], 0.7, 0.9)
    D.line([(t2[0], t2[1] + 3), (t2[0] + 0.5, t2[1] - 6)], "#b8bcc8", 1.2)                                                  # a spear point
    for (f, t) in ((f0, t0), (f1, t1), (f2, t2)):
        D.line([(f[0] + 0.5, f[1]), (lerp(f[0], t[0], 0.9) + 0.5, lerp(f[1], t[1], 0.9))], room.tone("#b08a5a", at, TO_US, 1.6), 0.5, 0.5)


def amphora(D, x, z, h, seed, clay="#b4683e", gain=1.0):
    k = room.k(z)
    cx, cy = P(x, 0, z)
    hh, r = h * k, h * 0.2 * k
    pos = (x, h * 0.5, z)
    lite, mid, half, dark = (room.tone(clay, pos, (-0.55, -0.1, -0.8), gain * 1.2), room.tone(clay, pos, TO_US, gain),
                             room.tone(clay, pos, (0.6, 0.2, -0.7), gain * 0.7), room.tone(clay, pos, (0.5, 0.8, -0.3), gain * 0.45))
    body = [(-0.25, 0), (-0.75, -0.2), (-1.0, -0.45), (-0.95, -0.66), (-0.5, -0.8), (-0.34, -0.88), (-0.36, -1.0), (0.36, -1.0), (0.34, -0.88), (0.5, -0.8), (0.95, -0.66), (1.0, -0.45), (0.75, -0.2), (0.25, 0)]
    D.poly([(cx + u * r, cy + v * hh) for u, v in body], mid)
    D.poly([(cx + u * r, cy + v * hh) for u, v in [(0.2, 0), (0.75, -0.2), (1.0, -0.45), (0.95, -0.66), (0.5, -0.8), (0.34, -0.9), (0.2, -0.82), (0.5, -0.6), (0.52, -0.4), (0.3, -0.15)]], half)
    D.poly([(cx + u * r, cy + v * hh) for u, v in [(-0.7, -0.26), (-0.9, -0.46), (-0.84, -0.64), (-0.5, -0.76), (-0.56, -0.5)]], lite, 0.9)
    D.ellipse(cx, cy - hh, r * 0.42, r * 0.16, dark)
    for sx in (-1, 1):
        D.line([(cx + sx * r * 0.36, cy - hh * 0.96), (cx + sx * r * 0.8, cy - hh * 0.9), (cx + sx * r * 0.78, cy - hh * 0.72)], mid if sx < 0 else half, max(0.8, 2.6 * k))


def far_end(D, seed=40):
    tablet(D, room, "B", 232, 340, 204, 330, seed + 1, 1.35, pediment=True)
    standards(D)
    amphora(D, 372, 1216, 96, seed + 2, gain=1.4)
    amphora(D, 344, 1190, 84, seed + 3, "#a8603a", gain=1.4)
    pedestal(D)
    statue(D)


def altar(D, seed=44):
    """Before the god: a small table for offerings with a bronze bowl; a jug; the far brazier and its basket of charcoal."""
    rng = np.random.default_rng(seed)
    # a jug standing on the floor to the left
    jx, jz = -150.0, 944.0
    k = room.k(jz)
    cx, cy = P(jx, 0, jz)
    br = tones("#b08a44", (jx, 25, jz), 1.5)
    D.poly([(cx - 5.5 * k * 2, cy - 14 * k), (cx - 9 * k, cy - 26 * k), (cx - 4 * k, cy - 36 * k), (cx - 3.4 * k, cy - 46 * k), (cx + 3.4 * k, cy - 46 * k), (cx + 4 * k, cy - 36 * k), (cx + 9 * k, cy - 26 * k), (cx + 11 * k, cy - 14 * k), (cx + 7 * k, cy), (cx - 7 * k, cy)], br[2])
    D.poly([(cx + 1 * k, cy - 46 * k), (cx + 3.4 * k, cy - 46 * k), (cx + 4 * k, cy - 36 * k), (cx + 9 * k, cy - 26 * k), (cx + 11 * k, cy - 14 * k), (cx + 7 * k, cy), (cx + 2 * k, cy), (cx + 5 * k, cy - 16 * k), (cx + 3 * k, cy - 30 * k)], br[0])
    D.line([(cx - 3.4 * k, cy - 44 * k), (cx - 11 * k, cy - 38 * k), (cx - 9.5 * k, cy - 24 * k)], br[1], max(0.8, 2.0 * k))
    # a tall bronze lamp-stand on the left, its lamp out: it answers the brazier on the right
    sx_, sz_ = -176.0, 938.0
    k = room.k(sz_)
    cs = tones("#a8823e", (sx_, 80, sz_), 1.6)
    for a in (205, 335, 90):
        D.line([P(sx_, 14, sz_), P(sx_ + math.cos(math.radians(a)) * 17, 0, sz_ + math.sin(math.radians(a)) * 17)], cs[2 if a != 335 else 1], max(0.9, 2.4 * k), fine=False)
    D.line([P(sx_, 10, sz_), P(sx_, 146, sz_)], cs[2], max(1.0, 2.6 * k), fine=False)
    D.line([P(sx_ + 0.9, 12, sz_), P(sx_ + 0.9, 144, sz_)], cs[0], 0.6, 0.8)
    for yy in (16, 52, 104, 140):
        cx, cy = P(sx_, yy, sz_)
        D.ellipse(cx, cy, 2.9 * k, 2.0 * k, cs[1])
        D.ellipse(cx + 0.6, cy - 0.2, 1.4 * k, 1.0 * k, cs[0], 0.9, fine=True)
    cx, cy = P(sx_, 148, sz_)
    D.poly([(cx - 9 * k, cy), (cx - 5 * k, cy + 3.4 * k), (cx + 5 * k, cy + 3.4 * k), (cx + 9 * k, cy)], cs[2])
    D.ellipse(cx, cy, 9 * k, 9 * k * room.squash(148, sz_), cs[1])
    D.line([(cx - 9 * k, cy), (cx, cy + 9 * k * room.squash(148, sz_)), (cx + 9 * k, cy)], cs[0], 0.6, 0.9)
    D.poly([(cx - 4.5 * k, cy - 0.5), (cx - 2 * k, cy - 4 * k), (cx + 3 * k, cy - 4 * k), (cx + 6.5 * k, cy - 1.5 * k), (cx + 3 * k, cy + 0.6), (cx - 3 * k, cy + 0.6)], room.tone("#b4683e", (sx_, 150, sz_), (0.4, 0.3, -0.8), 1.6))
    # the far brazier, and beside it a basket of charcoal with the tongs
    bx, bz = 214.0, 968.0
    k = room.k(bz)
    cx, cy = P(bx, 0, bz)
    wk = tones("#8a6a40", (bx, 15, bz), 1.4)
    rx, ry = 19 * k, 19 * k * room.squash(26, bz)
    D.poly([(cx - rx * 0.86, cy), (cx - rx, cy - 26 * k), (cx + rx, cy - 26 * k), (cx + rx * 0.86, cy)], wk[2])
    D.poly([(cx + rx * 0.1, cy), (cx + rx * 0.14, cy - 26 * k), (cx + rx, cy - 26 * k), (cx + rx * 0.86, cy)], wk[0], 0.8)
    for yy in (0.25, 0.5, 0.75):
        D.line([(cx - rx * 0.92, cy - 26 * k * yy), (cx + rx * 0.92, cy - 26 * k * yy)], wk[3], 0.6, 0.6)
    D.ellipse(cx, cy - 26 * k, rx, ry, "#1a1416")
    for _ in range(9):
        a, r_ = rng.random() * 6.28, rng.random() ** 0.5 * 0.8
        D.ellipse(cx + math.cos(a) * rx * r_, cy - 26 * k + math.sin(a) * ry * r_ - 1, 1.6, 1.2, "#2c2428" if rng.random() < 0.7 else "#4a4048", fine=True)
    brazier(D, room, BRAZIER2[0], BRAZIER2[2], BRAZIER2[1], 29.0, seed + 5, gain=1.3, heat=1.05)
    D.line([P(BRAZIER2[0] + 30, 0, BRAZIER2[2] + 4), P(BRAZIER2[0] + 24, BRAZIER2[1] + 2, BRAZIER2[2] + 2)], "#3a3840", 0.9)   # the tongs lean on its rim
    # the table: bronze legs with lions' feet, a dark slab, a red cloth laid over it, the bowl
    x0, x1, z0, z1, yt = -52.0, 52.0, 903.0, 960.0, 86.0
    bz_ = tones("#a8823e", (0, 40, z0), 1.5)
    k = room.k(z0)
    for (lx, lz) in ((x0 + 6, z1 - 5), (x1 - 6, z1 - 5), (x0 + 6, z0 + 5), (x1 - 6, z0 + 5)):
        top_, knee_, foot_ = P(lx, yt - 4, lz), P(lx + (5 if lx > 0 else -5), yt * 0.52, lz), P(lx, 0, lz)
        tone_ = bz_[0] if lx > 0 else bz_[2]
        if lz > z0 + 10:
            tone_ = bz_[3]
        D.taper([top_, knee_], tone_, 5.0 * k, 4.0 * k, fine=False)
        D.taper([knee_, foot_], tone_, 4.0 * k, 3.0 * k, fine=False)
        D.ellipse(knee_[0], knee_[1], 3.0 * k, 3.2 * k, tone_)
        D.ellipse(foot_[0], foot_[1] - 1.2 * k, 4.4 * k, 2.4 * k, tone_)
        if lz < z0 + 10:
            D.line([(top_[0] + 0.5, top_[1]), (knee_[0] + 0.5, knee_[1])], bz_[0], 0.6, 0.7)
    D.line([P(x0 + 8, 30, z0 + 5), P(x1 - 8, 30, z0 + 5)], bz_[1], max(0.9, 2.2 * k))
    slab = block(D, x0, x1, yt - 8, yt, z0, z1, "#4a403c", 1.5, 4, 1, rng)
    lit_line(D, room, [(x0, yt, z0), (x1, yt, z0)], TO_US, "#b0a090", 1.0, 0.9, 1.8)
    RD = tones("#9a2a20", (0, yt, z0), 1.6)
    D.poly([P(-30, yt, z0), P(30, yt, z0), P(30, yt, z1), P(-30, yt, z1)], RD[2])                    # the cloth on the slab...
    D.poly([P(-30, yt, z0), P(30, yt, z0), P(31, yt - 34, z0 - 1), P(-31, yt - 34, z0 - 1)], RD[1])  # ...and hanging down in front
    D.poly([P(4, yt, z0), P(30, yt, z0), P(31, yt - 34, z0 - 1), P(6, yt - 34, z0 - 1)], RD[0], 0.8)
    for xx in (-18, -4, 12, 23):
        D.line([P(xx, yt - 2, z0), P(xx + 1, yt - 32, z0 - 1)], RD[3], 0.6, 0.6)
    D.line([P(-31, yt - 34, z0 - 1), P(31, yt - 34, z0 - 1)], "#e0b848", 0.9, 0.9)
    D.line([P(-30, yt, z0), P(30, yt, z0)], RD[0], 0.7, 0.8)
    cx, cy = P(0, yt, (z0 + z1) / 2)
    rx = 23 * k
    ry = rx * room.squash(yt + 9, (z0 + z1) / 2)
    D.poly([(cx - rx, cy - 9 * k), (cx - rx * 0.5, cy), (cx + rx * 0.5, cy), (cx + rx, cy - 9 * k)], bz_[2])                 # the bowl
    D.poly([(cx + rx * 0.1, cy - 9 * k), (cx + rx * 0.1, cy), (cx + rx * 0.5, cy), (cx + rx, cy - 9 * k)], bz_[0])
    D.ellipse(cx, cy - 9 * k, rx, ry, bz_[1])
    D.ellipse(cx, cy - 9 * k + 0.4, rx * 0.8, ry * 0.7, "#3a2616")
    D.line([(cx - rx, cy - 9 * k), (cx - rx * 0.4, cy - 9 * k + ry * 0.9), (cx + rx * 0.5, cy - 9 * k + ry * 0.85), (cx + rx, cy - 9 * k)], "#f6d888", 0.8, 0.95)
    jx_, jy_ = P(42, yt, z0 + 22)                                                           # a little flask
    D.poly([(jx_ - 2.2, jy_), (jx_ - 2.8, jy_ - 5), (jx_ - 1, jy_ - 8), (jx_ + 1, jy_ - 8), (jx_ + 2.8, jy_ - 5), (jx_ + 2.2, jy_)], bz_[1])
    D.line([(jx_ + 1.4, jy_ - 6), (jx_ + 2.2, jy_ - 2)], bz_[0], 0.7)
    for _ in range(14):                                                                     # crumbs of charcoal and ash by the brazier
        ax, az = BRAZIER2[0] + rng.normal(0, 34), BRAZIER2[2] - 20 + rng.normal(0, 26)
        px_, py_ = P(ax, 0, az)
        D.ellipse(px_, py_, 1.1, 0.6, "#141014" if rng.random() < 0.7 else "#8a8480", 0.7, fine=True)
    return slab


# ======================================================================== the two walls of treasure
def open_chest(D, seed=51):
    """A chest standing open against the right wall, its lid thrown back: sacks inside, and loose silver."""
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1, z0, z1 = OPEN
    wood = "#6b4526"
    lidf = Face(room, (x1 - 5, y1, z0), (x1 - 5, y1, z1), (x1 - 5, y1 + 74, z1), (x1 - 5, y1 + 74, z0), TO_LEFT)   # the lid stands up against the wall
    lidf.fill(D, "#8a6238", 3, 3, rng, 0.05, 1.15)
    for s in (0.2, 0.8):
        lidf.rect(D, s - 0.04, s + 0.04, 0, 1, IRON, 1.2, fine=False)
    lidf.line(D, [(0, 0), (0, 1), (1, 1)], "#8a6238", 1.0, 0.8, 1.8)
    parts = chest(D, room, x0, x1, y0, y1, z0, z1, seed, toward=-1, wood=wood, lid=0.99, ring=True, lock=True)
    top = parts["top"]
    top.rect(D, 0.07, 0.93, 0.05, 0.95, "#120c0c", fine=False, flat=True)                   # the dark inside
    for (u, v, r_) in ((0.3, 0.72, 15), (0.68, 0.66, 14), (0.42, 0.34, 15), (0.74, 0.3, 12)):
        cx, cy = top.at(u, v)
        k = top.k(u, v)
        c = top.tone("#bfa26a", u, v, 1.5)
        D.ellipse(cx, cy, r_ * k, r_ * k * 0.5, c * 0.75)
        D.ellipse(cx + 1.5 * k, cy - 1.0 * k, r_ * k * 0.6, r_ * k * 0.3, c)
        D.ellipse(cx, cy - 0.5 * k, 2.2 * k, 1.4 * k, top.tone("#4a3424", u, v, 1.4), fine=True)
    for _ in range(30):                                                                     # loose coin between the sacks
        u, v = 0.12 + rng.random() * 0.76, 0.1 + rng.random() * 0.8
        cx, cy = top.at(u, v)
        D.ellipse(cx, cy, 0.9, 0.6, top.tone("#e6ecf0", u, v, 1.6 + rng.random()), 0.9, fine=True)
    top.line(D, [(0.07, 0.05), (0.93, 0.05)], wood, 1.2, 0.9, 1.9)
    top.line(D, [(0.07, 0.05), (0.07, 0.95)], wood, 1.2, 0.9, 1.7)


def rack(D, seed=53):
    """The clerk's rack against the wall behind him: pigeon-holes of rolled accounts and bundles of
    tablets, the keys of the chests hanging at its end."""
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1, z0, z1 = RACK
    wood = "#7a5630"
    f = block(D, x0, x1, y0, y1, z0, z1, wood, 1.0, 2, 5, rng)
    side, front = f["side"], f["front"]                         # `side` is the long face with the holes (u runs from far to near)
    cols, rows = 3, 6
    for i in range(cols):
        for j in range(rows):
            u0, u1 = 0.05 + i * 0.31, 0.05 + i * 0.31 + 0.27
            v0, v1 = 0.07 + j * 0.152, 0.07 + j * 0.152 + 0.118
            side.rect(D, u0, u1, v0, v1, "#16100e", fine=False, flat=True)
            kind = rng.random()
            if kind < 0.62:                                    # rolls, end on: pale rounds with a dark middle
                n = 2 + int(rng.random() * 3)
                for q in range(n):
                    uu = u0 + (u1 - u0) * (0.2 + 0.6 * (q + rng.random() * 0.4) / n)
                    vv = v0 + (v1 - v0) * (0.28 + 0.28 * (q % 2))
                    side.dot(D, uu, vv, 4.4, "#d8c8a0", 1.25)
                    side.dot(D, uu, vv, 1.5, "#4a3a2a", 1.0)
            elif kind < 0.86:                                  # a bundle of wax tablets lying flat
                for q in range(3):
                    vv = v0 + (v1 - v0) * (0.15 + 0.2 * q)
                    side.line(D, [(u0 + 0.03, vv), (u1 - 0.04, vv)], "#a8824e", 2.6, 0.95, 1.2)
            side.line(D, [(u0, v0), (u1, v0)], wood, 1.2, 0.9, 1.8)          # the shelf's lip in the lamplight
    front.line(D, [(0, 0), (0, 1)], wood, 1.2, 0.8, 1.7)
    for v in (0.2, 0.4, 0.6, 0.8):
        front.line(D, [(0, v), (1, v)], wood, 0.9, 0.5, 0.5)
    # keys on a ring, hanging from a nail at the end
    nx, ny = front.at(0.55, 0.72)
    k = front.k()
    D.ellipse(nx, ny, 1.2, 1.2, "#1a1a20", fine=True)
    D.line([(nx + math.cos(a) * 5.5 * k, ny + 7 * k + math.sin(a) * 6.5 * k) for a in np.linspace(0, 6.3, 14)], front.tone(BRONZE, 0.5, 0.7, 1.6), max(0.7, 1.2 * k))
    for i, dx in enumerate((-3.5, -0.5, 3.0)):
        D.line([(nx + dx * k, ny + 13 * k), (nx + dx * k * 1.5, ny + (24 + i * 2) * k)], front.tone(IRON, 0.5, 0.6, 2.2), max(0.7, 1.4 * k))
        D.line([(nx + dx * k * 1.5, ny + (24 + i * 2) * k), (nx + dx * k * 1.5 + 2.4 * k, ny + (24 + i * 2) * k)], front.tone(IRON, 0.5, 0.6, 2.2), max(0.7, 1.4 * k))
    # on top: a jug and a slumped sack
    sack(D, room, x0 + 20, y1, z0 + 40, 30, 26, seed + 2, gain=1.1, side=-1, tag=False)


def stool(D, seed=55):
    rng = np.random.default_rng(seed)
    x0, x1, z0, z1 = STOOL
    wood = "#7a5630"
    for (lx, lz) in ((x0 + 3, z1 - 3), (x1 - 3, z1 - 3), (x0 + 3, z0 + 3), (x1 - 3, z0 + 3)):
        D.line([P(lx, 0, lz), P(lx, 40, lz)], room.tone(wood, (lx, 20, lz), TO_US, 1.0), max(0.9, 3.4 * room.k(lz)), fine=False)
    block(D, x0, x1, 38, 44, z0, z1, wood, 1.0, 2, 1, rng)
    block(D, x0 + 2, x1 - 2, 44, 50, z0 + 2, z1 - 2, "#8a2a20", 1.1, 2, 1, rng)


def lettered(D, seed=57):
    """Two bronze tablets of the laws leaning on the end of the nearest right-hand chest, close enough to read
    that they are written on. -> the face of the front one, for the letters."""
    rng = np.random.default_rng(seed)
    back = Face(room, (300, 0, 6), (356, 0, 6), (356, 96, 16), (300, 96, 16), TO_US)
    back.fill(D, "#9a7a40", 2, 4, rng, 0.06, 0.9)
    back.line(D, [(0, 0), (0, 1), (1, 1)], BRONZE, 1.2, 0.9, 1.8)
    for v in np.linspace(0.84, 0.94, 3):
        back.line(D, [(0.1, v), (0.5 + 0.3 * rng.random(), v)], BRONZE, 1.3, 0.7, 0.4)
    f = Face(room, (318, 0, -6), (378, 0, -6), (378, 80, 12), (318, 80, 12), TO_US)
    f.fill(D, BRONZE, 3, 5, rng, 0.05, 0.95)
    for _ in range(4):
        u, v = rng.random(), rng.random() ** 2 * 0.7
        cx, cy = f.at(u, v)
        D.ellipse(cx, cy, 3 + 5 * rng.random(), 2 + 3 * rng.random(), f.tone(VERDIGRIS, u, v, 1.0), 0.45)
    f.line(D, [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], BRONZE, 1.6, 0.9, 0.5)
    f.line(D, [(0.05, 0.04), (0.05, 0.96), (0.95, 0.96)], BRONZE, 1.0, 0.85, 1.8)
    f.line(D, [(0.05, 0.04), (0.95, 0.04), (0.95, 0.96)], BRONZE, 1.0, 0.7, 0.45)
    f.line(D, [(0, 1), (1, 1)], BRONZE, 1.3, 0.95, 2.0)
    for (u, v) in ((0.08, 0.06), (0.92, 0.06), (0.08, 0.94), (0.92, 0.94)):
        f.dot(D, u, v, 1.6, BRONZE, 2.2)
    return f


CAT = (-350.0, 84.0, 146.0)                                # where the treasury's cat sleeps: on the first chest, in the brazier's warmth


def cat(D, seed=65):
    """The only guard the money has: a ginger cat asleep on the chest nearest the fire, curled nose to tail."""
    x_, y_, z_ = CAT
    cx, cy = P(x_, y_, z_)
    k = room.k(z_)
    fur = "#c8803a"
    lite = room.tone(fur, (x_, y_ + 10, z_), (0.5, 0.1, -0.85), 1.0)
    mid = room.tone(fur, (x_, y_ + 10, z_), (0.0, 0.5, -0.85), 0.80)
    dark = room.tone(fur, (x_, y_ + 10, z_), (-0.6, 0.7, -0.3), 0.50)
    cream = room.tone("#f0dcb8", (x_, y_ + 10, z_), (0.4, 0.2, -0.9), 0.95)
    u = k / 0.78                                               # sizes below are for the scale it has on this chest
    D.ellipse(cx + 1 * u, cy + 0.6 * u, 19 * u, 4.6 * u, "#140c0c", 0.6, fine=True)                 # its shadow on the lid
    D.ellipse(cx - 1 * u, cy - 6.5 * u, 16.5 * u, 7.2 * u, mid)                                     # the body, a round loaf
    D.ellipse(cx - 7.5 * u, cy - 8.2 * u, 9.5 * u, 6.4 * u, dark)                                   # the haunch, away from the fire
    D.ellipse(cx + 2.5 * u, cy - 5.4 * u, 11 * u, 5.2 * u, lite, 0.9)                               # the flank the fire warms
    for i, dx in enumerate((-9.5, -5, -0.5, 4)):                                                   # tabby bars over the back
        D.line([(cx + dx * u, cy - 13.2 * u + abs(dx) * 0.12 * u), (cx + (dx + 1.6) * u, cy - 8.6 * u)], dark, max(0.7, 1.2 * u), 0.75)
    tail = [(cx - 16.5 * u, cy - 5 * u), (cx - 15 * u, cy - 1.2 * u), (cx - 8 * u, cy + 0.6 * u), (cx + 1 * u, cy + 0.4 * u), (cx + 7.5 * u, cy - 1.0 * u)]
    D.line(tail, mid, max(1.4, 3.2 * u), fine=False)                                               # the tail, brought round to its nose
    D.line(tail[1:], lite, max(0.7, 1.3 * u), 0.8)
    for t in (0.25, 0.5, 0.75):
        i = int(t * (len(tail) - 1))
        px_, py_ = lerp(tail[i][0], tail[i + 1][0], 0.5), lerp(tail[i][1], tail[i + 1][1], 0.5)
        D.line([(px_, py_ - 1.6 * u), (px_ + 0.6 * u, py_ + 1.6 * u)], dark, max(0.6, 1.0 * u), 0.7)
    hx, hy = cx + 12.5 * u, cy - 5.2 * u                                                           # the head, down on its paws
    D.ellipse(hx, hy, 5.4 * u, 4.6 * u, mid)
    D.ellipse(hx + 1.2 * u, hy + 0.6 * u, 3.8 * u, 3.2 * u, lite)
    D.poly([(hx - 4.6 * u, hy - 2.6 * u), (hx - 3.8 * u, hy - 7.6 * u), (hx - 0.9 * u, hy - 3.9 * u)], mid)       # ears
    D.poly([(hx + 0.8 * u, hy - 4.0 * u), (hx + 3.6 * u, hy - 7.8 * u), (hx + 4.6 * u, hy - 2.8 * u)], lite)
    D.poly([(hx + 1.9 * u, hy - 4.2 * u), (hx + 3.4 * u, hy - 6.4 * u), (hx + 3.9 * u, hy - 3.6 * u)], "#6a3a2a", 0.8, fine=True)
    D.ellipse(hx + 1.6 * u, hy + 2.0 * u, 2.6 * u, 1.7 * u, cream)                                  # the pale muzzle
    D.line([(hx - 2.6 * u, hy - 0.4 * u), (hx - 0.8 * u, hy + 0.2 * u)], "#2a1a14", max(0.6, 0.8 * u), 0.9)       # eyes shut: two small strokes
    D.line([(hx + 1.6 * u, hy - 0.2 * u), (hx + 3.5 * u, hy - 0.7 * u)], "#2a1a14", max(0.6, 0.8 * u), 0.9)
    D.ellipse(hx + 1.4 * u, hy + 1.3 * u, 0.7 * u, 0.5 * u, "#8a3a30", fine=True)                   # nose
    D.ellipse(cx + 9.5 * u, cy - 0.4 * u, 3.4 * u, 1.6 * u, cream)                                  # one white paw showing
    D.line([(cx - 13 * u, cy - 12.6 * u), (cx - 4 * u, cy - 13.6 * u), (cx + 5 * u, cy - 11.8 * u)], lite, max(0.6, 0.8 * u), 0.6)   # firelight along its back


def left_side(D, seed=60):
    L4, L3, L2a, L2b, L1 = LEFT[4], LEFT[3], LEFT[1], LEFT[2], LEFT[0]

    def put(c, **more):
        o = {k_: v_ for k_, v_ in c.items() if k_ != "box"}
        o.update(more)
        return chest(D, room, *c["box"], toward=1, **o)
    put(L4, gain=1.25)
    sack(D, room, -366, 72, 950, 34, 36, seed + 1, gain=1.25, side=1)
    sack(D, room, -298, 0, 934, 36, 42, seed + 2, gain=1.25, side=1)
    sack(D, room, -276, 0, 975, 34, 36, seed + 3, cloth="#a88c5c", lean=0.12, gain=1.25, side=1)
    tablet(D, room, "L", 808, 925, 200, 330, seed + 4, 1.2)
    put(L3, gain=1.35)
    tablet(D, room, "L", 318, 432, 196, 338, seed + 5, 1.1)
    put(L2a, gain=1.0)
    put(L2b, gain=1.05)
    sack(D, room, -304, 0, 304, 40, 36, seed + 9, cloth="#a88c5c", lean=-0.22, side=1)
    tablet(D, room, "L", 62, 190, 214, 330, seed + 6, 1.0)
    put(L1, gain=1.0)
    cat(D)
    sack(D, room, -372, 84, 92, 40, 44, seed + 7, side=-1)


def right_side(D, seed=70):
    R1, R2a, R2b = RIGHT

    def put(c, **more):
        o = {k_: v_ for k_, v_ in c.items() if k_ != "box"}
        o.update(more)
        return chest(D, room, *c["box"], toward=-1, **o)
    tablet(D, room, "R", 808, 930, 196, 326, seed + 1, 1.3)
    for i, (sx, sy, sz, lean) in enumerate(((372, 0, 905, 0.0), (344, 0, 880, -0.1), (378, 0, 858, 0.06), (352, 0, 842, 0.14), (362, 34, 884, 0.0))):
        sack(D, room, sx, sy, sz, 36, 40, seed + 10 + i, cloth=("#bfa26a", "#a88c5c")[i % 2], lean=lean, gain=1.3, side=-1)
    open_chest(D)
    tablet(D, room, "R", 652, 752, 206, 322, seed + 2, 1.2)
    tablet(D, room, "R", 518, 628, 186, 300, seed + 3, 1.2)
    put(R2a, gain=1.1)
    put(R2b, gain=1.1)
    tablet(D, room, "R", 322, 446, 242, 344, seed + 4, 1.1)
    rack(D)
    stool(D)
    tablet(D, room, "R", 64, 176, 218, 336, seed + 5, 1.0)
    put(R1, gain=1.0)
    sack(D, room, 368, 86, 62, 40, 44, seed + 20, side=-1)
    sack(D, room, 348, 86, 112, 38, 40, seed + 21, cloth="#a88c5c", lean=0.1, side=-1)
    return lettered(D)


def scar(D, side, u, v, w, h, seed, gain=1.0):
    """A place where the painted plaster has come away and the grey tufa blocks show: an old temple."""
    rng = np.random.default_rng(seed)
    n = room.wall_n(side)
    ring = []
    for t in np.linspace(0, 2 * math.pi, 11, endpoint=False):
        r = 0.7 + 0.5 * rng.random()
        ring.append((u + math.cos(t) * w * r, v + math.sin(t) * h * r))
    c = room.wall(side, u, v, 0.6)
    stone = room.tone("#7a6654", c, n, gain)
    D.poly([P(*room.wall(side, a, b, 0.6)) for a, b in ring], stone * 0.85)
    for j in (-0.3, 0.3):
        D.line([P(*room.wall(side, u - w * 0.7, v + h * j, 0.6)), P(*room.wall(side, u + w * 0.7, v + h * j, 0.6))], stone * 0.5, 0.6, 0.7)
    for i, a in enumerate((-0.35, 0.1, 0.5)):
        D.line([P(*room.wall(side, u + w * a, v - h * 0.3 * (1 if i % 2 else -1), 0.6)), P(*room.wall(side, u + w * a, v + h * (0.3 if i % 2 == 0 else 0.0), 0.6))], stone * 0.5, 0.6, 0.6)
    low = [p_ for p_ in ring if p_[1] < v]
    low.sort()
    if len(low) > 1:
        D.line([P(*room.wall(side, a, b, 0.4)) for a, b in low], np.clip(stone * 1.7, 0, 1), 0.7, 0.7)    # the broken edge, lit from below
    return ring


def crack(D, side, uv, gain=1.0):
    n = room.wall_n(side)
    pts = [P(*room.wall(side, a, b, 0.4)) for a, b in uv]
    D.line(pts, "#0e0a0c", 0.7, 0.7)
    D.line([(x_ + 0.8, y_ + 0.3) for x_, y_ in pts], room.tone("#b09080", room.wall(side, *uv[len(uv) // 2]), n, gain), 0.5, 0.35)


def age(D, seed=27):
    scar(D, "R", 600, 606, 40, 24, seed + 1, 0.85)
    scar(D, "L", 640, 590, 30, 20, seed + 2, 0.85)
    scar(D, "R", 1010, 150, 22, 18, seed + 4, 0.8)
    crack(D, "B", [(300, 470), (296, 430), (306, 392), (300, 350), (312, 318)])
    crack(D, "R", [(210, 470), (204, 420), (216, 384), (208, 340), (214, 300)])
    crack(D, "L", [(880, 470), (872, 424), (884, 380), (876, 356)])
    crack(D, "L", [(180, 136), (176, 100), (186, 70), (180, 30)])
    crack(D, "B", [(-250, 700), (-262, 640), (-252, 590), (-266, 540)])


def shield(D, side, u, v, r, seed, gain=1.7):
    """A round bronze shield hung high on a wall: an old trophy, dull, with a glint on the edge toward the door."""
    n = room.wall_n(side)
    c = room.wall(side, u, v, 3.0)
    base = room.tone("#8a6a34", c, n, gain)

    def circle(f, t0=0.0, t1=2 * math.pi, m=22):
        return [P(*room.wall(side, u + math.cos(t) * r * f, v + math.sin(t) * r * f, 3.0)) for t in np.linspace(t0, t1, m)]
    D.line([P(*room.wall(side, u, v + r, 1.0)), P(*room.wall(side, u, v + r * 1.5, 1.0))], base * 0.8, 0.7, 0.8)
    D.poly(circle(1.0), base * 0.62)
    D.poly(circle(0.84), base * 0.95)
    D.poly(circle(0.5), base * 0.75)
    D.poly(circle(0.2), np.clip(base * 1.5, 0, 1))
    D.line(circle(0.93, math.pi * 0.9, math.pi * 1.6, 9), np.clip(base * 2.3, 0, 1), 0.8, 0.85)
    D.line(circle(0.62, math.pi * 1.0, math.pi * 1.5, 6), np.clip(base * 1.7, 0, 1), 0.6, 0.6)


def litter(D, seed=75):
    """Small things on the floor: silver that has rolled off the table, a leaf and some straw blown in at the door."""
    rng = np.random.default_rng(seed)
    for (x_, z_) in ((188, 300), (236, 200), (164, 224), (252, 318), (120, 258)):
        cx, cy = P(x_, 0, z_)
        k = room.k(z_)
        D.ellipse(cx + 0.6, cy + 0.5, 1.5 * k * 1.2, 0.9 * k, "#141014", 0.5, fine=True)
        D.ellipse(cx, cy, 1.5 * k * 1.2, 0.9 * k, room.tone("#e6ecf0", (x_, 1, z_), UP, 2.2), fine=True)
        D.ellipse(cx - 0.3, cy - 0.2, 0.6, 0.4, "#ffffff", 0.8, fine=True)
    for (x_, z_, a) in ((14, 118, 0.4), (-36, 262, 2.0), (52, 334, 1.1), (96, 60, 2.6), (-70, 30, 0.2), (30, 210, 1.7)):     # straw, in the sun
        dx, dz = math.cos(a) * 9, math.sin(a) * 9
        D.line([P(x_ - dx, 0, z_ - dz), P(x_ + dx, 0, z_ + dz)], "#b89a5c", 0.6, 0.75)
        D.line([P(x_ - dx + 1.5, 0, z_ - dz - 1), P(x_ + dx + 1.5, 0, z_ + dz - 1)], "#8a6a4a", 0.6, 0.35)
    lx, lz = -22.0, 172.0                                                                # a dry leaf
    c = P(lx, 0, lz)
    D.poly([(c[0] - 5, c[1]), (c[0] - 1, c[1] - 2.2), (c[0] + 5, c[1] - 0.6), (c[0] + 1, c[1] + 1.8)], "#9a5a2a")
    D.line([(c[0] - 5, c[1]), (c[0] + 5, c[1] - 0.6)], "#5a2e16", 0.5, 0.8)
    D.poly([(c[0] - 4, c[1] + 2.2), (c[0] + 5.5, c[1] + 1.4), (c[0] + 2, c[1] + 3.2)], "#8a7a5a", 0.5, fine=True)
    for _ in range(40):                                                                  # grit, mostly along the walls
        sx = rng.choice([-1, 1])
        x_, z_ = sx * (300 + rng.random() * 60), rng.random() * 1100
        cx, cy = P(x_, 0, z_)
        D.ellipse(cx, cy, 0.7, 0.45, "#8a8078" if rng.random() < 0.5 else "#1c1616", 0.5, fine=True)


def leaning(D, seed=77):
    """Three tablets nobody has hung yet, leaning on the right wall at the far end."""
    rng = np.random.default_rng(seed)
    for i, (za, zb_, h, off) in enumerate(((1050, 1150, 118, 0), (1020, 1108, 104, 9), (990, 1066, 92, 18))):
        f = Face(room, (356 - off, 0, zb_), (356 - off, 0, za), (392 - off, h, za), (392 - off, h, zb_), TO_LEFT)
        f.fill(D, "#8a6a34", 2, 3, rng, 0.06, 1.25)
        f.line(D, [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], BRONZE, 1.4, 0.9, 0.6)
        f.line(D, [(0, 1), (1, 1)], BRONZE, 1.2, 0.9, 2.2)
        f.line(D, [(1, 0), (1, 1)], BRONZE, 1.0, 0.8, 1.9)
        for v in np.linspace(0.2, 0.85, 6):
            f.line(D, [(0.12, v), (0.5 + 0.38 * rng.random(), v)], BRONZE, 1.2, 0.7, 0.4, least=0.5)


def dress(seed=3):
    """Everything that stands in the room, far to near, on a pair of sheets. -> (Dual, places for the last pass)"""
    D = Dual(SHAPE)
    wall_lines(D)
    age(D)
    hung = {"L": ((375, 600, 44), (865, 596, 42), (140, 604, 46)), "R": ((392, 594, 40), (884, 602, 45), (150, 608, 43))}
    for side in ("L", "R"):                                   # old trophies high up in the dark, no two hung quite alike
        for i, (u, v, r) in enumerate(hung[side]):
            shield(D, side, u, v, r, seed + i)
    far_end(D)
    altar(D)
    leaning(D)
    left_side(D)
    law = right_side(D)
    litter(D)
    return D, dict(law=law)


# ======================================================================== the clerk's table (cut-out)
def table_plane(seed=80):
    D = Dual(SHAPE)
    rng = np.random.default_rng(seed)
    x0, x1, z0, z1, yt = TABLE
    wood = "#80582e"
    # a sack of coin waiting on the floor at the table's end, and a small one slumped on it
    sack(D, room, x0 - 34, 0, z0 + 14, 44, 50, seed + 1, gain=1.05, side=1)
    sack(D, room, x0 - 12, 0, z0 + 2, 30, 30, seed + 2, cloth="#a88c5c", lean=0.16, gain=1.05, side=1)
    for (lx, lz) in ((x0 + 5, z1 - 5), (x1 - 5, z1 - 5)):                                   # far legs
        block(D, lx - 3.5, lx + 3.5, 0, yt - 6, lz - 3.5, lz + 3.5, wood, 0.8, 1, 3, rng)
    lit_line(D, room, [(x0 + 5, 16, z1 - 5), (x1 - 5, 16, z1 - 5)], TO_US, wood, 3.0, 1.0, 0.8, fine=False)
    Face(room, (x0 + 3, yt - 18, z1 - 3), (x0 + 3, yt - 18, z0 + 3), (x0 + 3, yt - 6, z0 + 3), (x0 + 3, yt - 6, z1 - 3), TO_LEFT).fill(D, wood, 2, 1, rng, 0.04, 0.9)
    apron = Face(room, (x0 + 3, yt - 18, z0 + 3), (x1 - 3, yt - 18, z0 + 3), (x1 - 3, yt - 6, z0 + 3), (x0 + 3, yt - 6, z0 + 3), TO_US).fill(D, wood, 6, 1, rng, 0.04, 0.95)
    apron.line(D, [(0, 0), (1, 0)], "#120c0c", 1.4, 0.7, flat=True)
    apron.rect(D, 0.36, 0.64, 0.12, 0.9, wood, 1.15, fine=True)                               # a drawer, and its ring
    apron.line(D, [(0.36, 0.12), (0.36, 0.9), (0.64, 0.9), (0.64, 0.12), (0.36, 0.12)], "#1c1210", 0.8, 0.8, flat=True)
    apron.dot(D, 0.5, 0.5, 1.8, BRONZE, 2.0)
    lit_line(D, room, [(x0 + 5, 16, z0 + 5), (x0 + 5, 16, z1 - 5)], TO_LEFT, wood, 3.0, 1.0, 0.8, fine=False)       # stretchers
    for (lx, lz) in ((x0 + 5, z0 + 5), (x1 - 5, z0 + 5)):                                   # near legs, with bronze shoes
        f = block(D, lx - 3.5, lx + 3.5, 0, yt - 6, lz - 3.5, lz + 3.5, wood, 1.0, 1, 4, rng)
        f["front"].rect(D, 0, 1, 0, 0.09, BRONZE, 1.3)
        f["front"].line(D, [(0, 0), (0, 1)], wood, 0.8, 0.7, 1.7)
    lit_line(D, room, [(x0 + 5, 16, z0 + 5), (x1 - 5, 16, z0 + 5)], TO_US, wood, 3.2, 1.0, 1.0, fine=False)
    slab = block(D, x0 - 3, x1 + 3, yt - 6, yt, z0 - 3, z1 + 3, wood, 1.0, 10, 1, rng, top_gain=1.0)
    top = slab["top"]
    for v in (0.34, 0.67):
        top.line(D, [(0, v), (1, v)], wood, 0.7, 0.5, 0.5)
    pool = P(LAMP[0] - 8, yt, LAMP[2] - 4)                                                   # where the lamp's light lies thickest on the wood
    kk_ = room.k(LAMP[2])
    D.ellipse(pool[0], pool[1], 30 * kk_, 30 * kk_ * room.squash(yt, LAMP[2]), "#ffb860", 0.22)
    D.ellipse(pool[0], pool[1], 16 * kk_, 16 * kk_ * room.squash(yt, LAMP[2]), "#ffd088", 0.25)
    lit_line(D, room, [(x0 - 3, yt, z0 - 3), (x1 + 3, yt, z0 - 3)], UP, wood, 1.1, 0.9, 1.5)
    dark_line(D, [(x0 - 3, yt - 6, z0 - 3), (x1 + 3, yt - 6, z0 - 3)], 1.4, 0.7)

    def T(x_, z_, y_=0.0):
        return P(x_, yt + y_, z_)
    k = room.k((z0 + z1) / 2)
    sq = room.squash(yt, (z0 + z1) / 2)
    BZ = tones("#b89048", (260, yt + 20, 262), 1.0)
    lampc = col((1.0, 0.74, 0.40))

    def lit(albedo, x_, z_, y_=2.0, n=UP, gain=1.0):
        return room.tone(albedo, (x_, yt + y_, z_), n, gain)

    # ---- wax tablets, open, and the stylus
    for (tx, tz) in ((296.0, 240.0), (313.0, 240.5)):
        q = [T(tx, tz), T(tx + 15, tz), T(tx + 15, tz + 22), T(tx, tz + 22)]
        D.poly(q, lit("#b8905a", tx, tz, gain=1.0))
        q2 = [T(tx + 1.8, tz + 2.5), T(tx + 13.2, tz + 2.5), T(tx + 13.2, tz + 19.5), T(tx + 1.8, tz + 19.5)]
        D.poly(q2, lit("#2a3a30", tx, tz, gain=1.0))
        for i in range(4):
            zz = tz + 5 + i * 3.6
            D.line([T(tx + 3, zz), T(tx + 3 + 4 + 5 * rng.random(), zz)], lit("#c8d0b8", tx, tz, gain=1.0), 0.5, 0.75)
    D.line([T(331, 236), T(318, 246)], lit("#e0c070", 325, 240, gain=1.3), 0.7)
    # ---- the ink pot and a reed pen
    ix, iy = T(280, 284)
    D.ellipse(ix, iy - 2.5 * k, 3.2 * k, 3.4 * k, lit("#3a3438", 280, 284))
    D.ellipse(ix, iy - 5 * k, 2.4 * k, 2.4 * k * sq, "#0c0a10")
    D.line([(ix + 1, iy - 5 * k), (ix + 9 * k, iy - 17 * k)], lit("#d8c090", 280, 284, 10), 0.7)
    # ---- heaps of silver: counted stacks in a row, an uncounted heap, strays
    silver = "#dfe6ea"
    hx, hz = 303.0, 270.0
    cx, cy = T(hx, hz)
    heap = [(-15, 0), (-12, -4), (-6, -8.5), (0, -10), (7, -8), (12, -4.5), (15, 0), (8, 2.4), (-8, 2.4)]
    D.poly([(cx + u * k, cy + v * k) for u, v in heap], lit("#8e98a2", hx, hz, 5, (0, 0.5, -0.8)))
    D.poly([(cx + u * k, cy + v * k) for u, v in [(1, -10), (7, -8), (12, -4.5), (15, 0), (8, 2.4), (5, -3)]], lit("#c4ccd4", hx, hz, 5, (0.6, 0.5, -0.6)))
    for _ in range(46):
        u, v = rng.normal(0, 6.5), -abs(rng.normal(0, 3.4))
        if abs(u) > 14 or v < -9.5 + abs(u) * 0.55:
            continue
        D.ellipse(cx + u * k, cy + v * k, 1.0, 0.62, lit(silver, hx + u, hz, 5, (0.3, 0.7, -0.5), 0.8 + rng.random() * 0.7), 0.95, fine=True)
    for i in range(9):                                                                     # stacks, each a different height
        sx_ = 252.0 + i * 5.2
        hgt = 2.5 + rng.random() * 7.5 if i != 4 else 11.0
        bx, by = T(sx_, 243.0)
        D.poly([(bx - 1.9 * k, by), (bx + 1.9 * k, by), (bx + 1.9 * k, by - hgt * k), (bx - 1.9 * k, by - hgt * k)], lit("#9aa4ae", sx_, 243, 4, TO_US))
        D.line([(bx + 1.5 * k, by), (bx + 1.5 * k, by - hgt * k)], lit(silver, sx_, 243, 4, (0.7, 0, -0.7), 1.2), 0.6, 0.9)
        D.ellipse(bx, by - hgt * k, 1.9 * k, 1.9 * k * sq, lit(silver, sx_, 243, hgt, UP, 1.25))
    for _ in range(16):
        sx_, sz_ = 240 + rng.random() * 95, 236 + rng.random() * 50
        px_, py_ = T(sx_, sz_)
        D.ellipse(px_, py_, 1.2, 0.7, lit(silver, sx_, sz_, 1, UP, 1.1 + rng.random() * 0.5), 0.9, fine=True)
    # ---- the balance: a post, a beam, two pans on their chains
    px_, pz_ = 236.0, 276.0
    base = T(px_, pz_)
    D.ellipse(base[0], base[1], 7.5 * k, 7.5 * k * sq, BZ[2])
    D.ellipse(base[0], base[1] - 1.2 * k, 5.5 * k, 5.5 * k * sq, BZ[1])
    top_ = T(px_, pz_, 50)
    D.line([base, top_], BZ[2], max(1.0, 2.6 * k), fine=False)
    D.line([(base[0] + 0.6, base[1]), (top_[0] + 0.6, top_[1])], BZ[0], 0.7, 0.9)
    D.ellipse(top_[0], top_[1] - 1.5 * k, 2.2 * k, 2.4 * k, BZ[0])
    tilt = 4.0
    la, ra = T(px_ - 27, pz_, 47 - tilt), T(px_ + 27, pz_, 47 + tilt)
    D.line([la, ra], BZ[1], max(0.9, 1.8 * k))
    D.line([la, ra], "#f4dc90", 0.5, 0.7)
    D.line([T(px_, pz_, 47), T(px_ - 1.5, pz_, 36)], BZ[0], 0.7)                               # the pointer
    for (arm, drop, load) in ((la, 24.0, "coin"), (ra, 22.0, "weight")):
        pan = (arm[0], arm[1] + drop * k)
        prx = 8.5 * k
        for dx in (-1, 0, 1):
            D.line([arm, (pan[0] + dx * prx * 0.9, pan[1] - (0.6 if dx else -0.6) * k)], "#d8c080", 0.6, 0.95)
        D.poly([(pan[0] - prx, pan[1]), (pan[0] - prx * 0.6, pan[1] + 3.2 * k), (pan[0] + prx * 0.6, pan[1] + 3.2 * k), (pan[0] + prx, pan[1])], BZ[2])
        D.ellipse(pan[0], pan[1], prx, prx * sq * 0.9, BZ[1])
        D.line([(pan[0] - prx, pan[1]), (pan[0], pan[1] + prx * sq * 0.9), (pan[0] + prx, pan[1])], BZ[0], 0.6, 0.9)
        if load == "coin":
            for _ in range(7):
                D.ellipse(pan[0] + rng.normal(0, prx * 0.35), pan[1] - 0.6 + rng.normal(0, 0.5), 1.1, 0.7, lit(silver, px_, pz_, 20, UP, 1.4), fine=True)
        else:
            D.poly([(pan[0] - 2.4 * k, pan[1]), (pan[0] + 2.4 * k, pan[1]), (pan[0] + 1.8 * k, pan[1] - 5 * k), (pan[0] - 1.8 * k, pan[1] - 5 * k)], lit("#5a5450", px_, pz_, 20, TO_US, 1.3))
    for i, (wx, wz, s_) in enumerate(((262, 282, 4.2), (270, 284, 3.4), (277, 281, 2.6))):       # spare weights in a row
        bx, by = T(wx, wz)
        D.poly([(bx - s_ * k * 0.7, by), (bx + s_ * k * 0.7, by), (bx + s_ * k * 0.5, by - s_ * k * 1.3), (bx - s_ * k * 0.5, by - s_ * k * 1.3)], lit("#6a625c", wx, wz, 3, TO_US, 1.2))
        D.line([(bx + s_ * k * 0.4, by), (bx + s_ * k * 0.3, by - s_ * k * 1.2)], lit("#b0a698", wx, wz, 3, TO_US, 1.4), 0.5, 0.8)
    # ---- the lamp on its little stand, and its flame
    lx, lz = LAMP[0], LAMP[2]
    b0 = T(lx + 2, lz)
    D.ellipse(b0[0], b0[1], 5.5 * k, 5.5 * k * sq, BZ[2])
    D.line([b0, T(lx + 2, lz, 20)], BZ[1], max(1.0, 2.4 * k), fine=False)
    D.line([(b0[0] + 0.6, b0[1]), (b0[0] + 0.6, T(lx + 2, lz, 20)[1])], "#ffd890", 0.5, 0.8)
    c = T(lx + 2, lz, 22)
    D.poly([(c[0] - 9 * k, c[1] - 1.5 * k), (c[0] - 4 * k, c[1] - 4.6 * k), (c[0] + 5 * k, c[1] - 4.6 * k), (c[0] + 7.5 * k, c[1] - 1.5 * k), (c[0] + 5 * k, c[1] + 1.4 * k), (c[0] - 5 * k, c[1] + 1.4 * k)], BZ[2])
    D.poly([(c[0] - 9 * k, c[1] - 1.5 * k), (c[0] - 4 * k, c[1] - 4.6 * k), (c[0] + 5 * k, c[1] - 4.6 * k), (c[0] + 3 * k, c[1] - 2.6 * k), (c[0] - 5 * k, c[1] - 2.2 * k)], np.clip(BZ[0] * 0.7 + lampc * 0.5, 0, 1))
    D.line([(c[0] + 7.5 * k, c[1] - 1.5 * k), (c[0] + 10.5 * k, c[1] - 4 * k), (c[0] + 8 * k, c[1] - 6 * k)], BZ[1], max(0.7, 1.2 * k))            # its handle
    fx, fy = c[0] - 8.6 * k, c[1] - 2.4 * k
    D.poly([(fx - 2.3, fy), (fx - 1.9, fy - 4.4), (fx + 0.3, fy - 10.0), (fx + 2.1, fy - 4.4), (fx + 2.2, fy)], "#ff9a2c")
    D.poly([(fx - 1.4, fy - 0.2), (fx - 0.9, fy - 3.8), (fx + 0.3, fy - 7.4), (fx + 1.3, fy - 3.6), (fx + 1.3, fy - 0.2)], "#ffe9a0")
    D.ellipse(fx, fy - 1.8, 1.0, 1.5, "#fffbe8", fine=True)
    return D


# ======================================================================== the front plane (cut-out)
LEAF_X, LEAF_Z = 372.0, -8.0                                # the door leaves stand open against the side walls; their free edges


def leaf(D, sgn, seed):
    rng = np.random.default_rng(seed)
    xl = sgn * LEAF_X
    zf, zn = LEAF_Z, -150.0
    n = (-sgn, 0, 0)
    bronze = "#5c4c2e"
    f = Face(room, (xl, 2, zn), (xl, 2, zf), (xl, 760, zf), (xl, 760, zn), n)          # u runs from the border to the free edge
    f.fill(D, bronze, 3, 16, rng, 0.06, 0.92)
    D.poly([P(xl, -6, zn), P(xl, -6, zf), P(xl, 2, zf), P(xl, 2, zn)], "#0c0a0c")      # the dark under it
    rails = [(2, 36), (150, 178), (322, 348), (486, 512), (650, 676)]
    us = 1 - 27.0 / (zf - zn)                                                           # the stile along the free edge starts here
    for (a, b) in zip(rails[:-1], rails[1:]):                                           # sunk panels between the rails
        v0, v1 = (a[1] + 4) / 758.0, (b[0] - 4) / 758.0
        f.fill(D, bronze, 2, 3, rng, 0.05, 0.78, u0=0.0, u1=us - 0.04, v0=v0, v1=v1)
        f.line(D, [(0, v1), (us - 0.04, v1)], "#0c0a0c", 1.6, 0.7, flat=True)
        f.line(D, [(us - 0.04, v0), (us - 0.04, v1)], "#0c0a0c", 1.4, 0.6, flat=True)
        f.line(D, [(0, v0), (us - 0.04, v0)], bronze, 1.2, 0.8, 1.7)
        for _ in range(5):                                                              # green where the rain has run down it
            u, v = rng.random() * (us - 0.1), v0 + (0.3 + 0.7 * rng.random()) * (v1 - v0)
            drop = (0.25 + 0.6 * rng.random()) * (v - v0)
            f.line(D, [(u, v), (u + rng.normal(0, 0.01), v - drop)], VERDIGRIS, 2.5 + 3 * rng.random(), 0.30, 0.9, fine=False)
    f.fill(D, BRONZE, 1, 12, rng, 0.05, 0.85, u0=us + (1 - us) * 0.25, u1=us + (1 - us) * 0.62, alpha=0.30)   # the long shine of metal down the stile
    for (a, b) in zip(rails[:-1], rails[1:]):
        v0, v1 = (a[1] + 4) / 758.0, (b[0] - 4) / 758.0
        f.fill(D, BRONZE, 1, 2, rng, 0.05, 0.8, u0=(us - 0.04) * 0.55, u1=(us - 0.04) * 0.80, v0=v0 + (v1 - v0) * 0.1, v1=v1 - (v1 - v0) * 0.08, alpha=0.16)
        f.line(D, [(us - 0.06, v0 + 0.004), (us - 0.06, v1 - 0.004)], bronze, 0.9, 0.5, 1.5)
    for (a, b) in rails:                                                                # the rails' upper edges catch the door's light
        f.line(D, [(0, b / 758.0), (us, b / 758.0)], bronze, 1.1, 0.75, 1.8)
        f.line(D, [(0, a / 758.0), (us, a / 758.0)], "#0c0a0c", 1.3, 0.55, flat=True)
    for (a, b) in rails:                                                                # big bosses on the rails and down the stile
        vm = (a + b) / 2 / 758.0
        for u in np.arange(us - 0.14, 0.0, -0.20):
            boss(D, f, u, vm, 4.6, bronze)
    for y_ in np.arange(60.0, 740.0, 43.0):
        boss(D, f, us + (1 - us) * 0.5, y_ / 758.0, 4.2, bronze)
    f.line(D, [(us, 0), (us, 1)], "#0c0a0c", 1.2, 0.5, flat=True)
    # a ring to pull it by
    cx, cy = f.at(us - 0.16, 0.262)
    k = f.k(us, 0.26)
    D.ellipse(cx, cy - 8 * k, 4.2 * k * 0.6, 4.2 * k, f.tone(bronze, us - 0.16, 0.27, 1.6), fine=True)
    ring = [(cx + math.cos(a) * 6.4 * k, cy + math.sin(a) * 10.5 * k) for a in np.linspace(0, 6.3, 18)]
    D.line(ring, f.tone(BRONZE, us - 0.16, 0.25, 1.3), max(0.9, 2.4 * k))
    D.line(ring[2:8], f.tone(BRONZE, us - 0.16, 0.25, 2.2), max(0.6, 1.0 * k), 0.9)
    return f


def boss(D, f, u, v, r_cm, albedo):
    cx, cy = f.at(u, v)
    k = f.k(u, v)
    r = r_cm * k
    D.ellipse(cx + 0.6, cy + 1.0, r * 0.62, r * 1.02, "#0c0a0c", 0.6, fine=True)
    D.ellipse(cx, cy, r * 0.6, r, f.tone(albedo, u, v, 1.25), fine=True)
    D.ellipse(cx - r * 0.12, cy + r * 0.25, r * 0.3, r * 0.42, f.tone(BRONZE, u, v, 2.3), 0.9, fine=True)


def front_plane(seed=90):
    D = Dual(SHAPE)
    leaf(D, -1, seed + 1)
    leaf(D, 1, seed + 2)
    # the sun, coming in past the right-hand leaf, runs a hot line down its edge
    edge = [P(LEAF_X, y_, LEAF_Z) for y_ in np.linspace(40, 560, 24)]
    rng = np.random.default_rng(seed)
    for a, b in zip(edge[:-1], edge[1:]):
        if rng.random() < 0.8:
            D.line([(a[0] - 0.4, a[1]), (b[0] - 0.4, b[1])], "#ffd896", 1.2, 0.55 + 0.4 * rng.random())
    brazier_box(D, seed + 3)
    return D


def brazier_box(D, seed):
    """The near brazier: a long bronze box on four lions' feet, a toothed rim, a bed of coals in it."""
    rng = np.random.default_rng(seed)
    x0, x1, z0, z1 = BOX1
    y0, y1 = 22.0, BRAZIER1[1]
    bronze = "#8c6c36"
    ember = np.array([1.0, 0.46, 0.16], dtype=F32)
    for (lx, lz) in ((x0 + 8, z1 - 8), (x1 - 8, z1 - 8), (x0 + 8, z0 + 8), (x1 - 8, z0 + 8)):     # feet: far pair, then near pair
        f = block(D, lx - 6, lx + 6, 0, y0 + 2, lz - 6, lz + 6, bronze, 0.9, 1, 2, rng)
        cx, cy = P(lx, 0, lz - 6)
        k = room.k(lz)
        D.ellipse(cx, cy - 2.5 * k, 8.5 * k, 4.5 * k, f["front"].tone(bronze, 0.5, 0.1, 1.0))
        for dx in (-4, 0, 4):
            D.line([(cx + dx * k, cy - 4.5 * k), (cx + dx * k, cy - 0.5 * k)], "#1a120c", 0.7, 0.7)
    f = block(D, x0, x1, y0, y1, z0, z1, bronze, 1.0, 8, 3, rng, top_gain=1.0)
    front, side, top = f["front"], f["side"], f["top"]
    # ---- the fire: the inside of the box, its far wall lit, the coals
    top.rect(D, 0.04, 0.96, 0.07, 0.93, "#3a0e08", fine=False, flat=True)
    inner_far = [top.at(0.04, 0.93), top.at(0.96, 0.93), P(x1 - 4, y1 - 9, z1 - 5), P(x0 + 4, y1 - 9, z1 - 5)]
    D.poly(inner_far, np.clip(col(bronze) * 0.7 + ember * 0.55, 0, 1))
    bed = Face(room, (x0 + 5, y1 - 7, z0 + 6), (x1 - 5, y1 - 7, z0 + 6), (x1 - 5, y1 - 7, z1 - 6), (x0 + 5, y1 - 7, z1 - 6), UP)
    D.poly([bed.at(0, 0), bed.at(1, 0), bed.at(1, 1), bed.at(0, 1)], "#b8341a")
    D.poly([bed.at(0.1, 0.12), bed.at(0.9, 0.12), bed.at(0.86, 0.88), bed.at(0.14, 0.88)], "#ff7a20")
    D.poly([bed.at(0.24, 0.26), bed.at(0.72, 0.22), bed.at(0.70, 0.74), bed.at(0.3, 0.76)], "#ffae3c", 0.9)
    k = room.k(0)
    lumps = sorted(((rng.random(), rng.random(), rng.random()) for _ in range(120)), key=lambda p: -p[1])
    for (u, v, t) in lumps:
        cx, cy = bed.at(0.04 + u * 0.92, 0.05 + v * 0.9)
        lift = (1 - (2 * u - 1) ** 2) * (1 - (2 * v - 1) ** 2) * 7.0 * k                 # heaped in the middle
        cy -= lift
        r = (3.6 + 3.4 * rng.random()) * k
        if t > 0.84:
            D.ellipse(cx, cy, r * 0.8, r * 0.62, "#ffd070")
            D.ellipse(cx - r * 0.1, cy - r * 0.1, r * 0.4, r * 0.3, "#fff6cc", 0.9, fine=True)
            continue
        D.ellipse(cx, cy, r, r * 0.74, mixc("#6a160c", "#c03a14", t))
        D.ellipse(cx + r * 0.05, cy - r * 0.22, r * 0.88, r * 0.50, mixc("#1a0b0b", "#3a1612", t))
        if t < 0.22:
            D.ellipse(cx - r * 0.2, cy - r * 0.3, r * 0.3, r * 0.16, "#7a6a66", 0.75, fine=True)
    # ---- the rim: a flat lip and a row of teeth along the two sides we see
    top.line(D, [(0, 0), (1, 0)], bronze, 2.2, 1.0, 1.9)
    top.line(D, [(1, 0), (1, 1)], bronze, 2.0, 1.0, 1.5)
    top.line(D, [(0, 1), (1, 1)], bronze, 1.6, 0.9, 1.3)
    for i in range(13):
        u = (i + 0.5) / 13
        a, b = P(lerp(x0, x1, u) - 2.6, y1, z0), P(lerp(x0, x1, u) + 2.6, y1, z0)
        c = front.tone(bronze, u, 1.0, 1.25)
        D.poly([a, b, (b[0] - 0.4, b[1] - 5.2 * k), ((a[0] + b[0]) / 2, a[1] - 7.2 * k), (a[0] + 0.4, a[1] - 5.2 * k)], c)
        D.line([(a[0] + 0.5, a[1] - 5.0 * k), ((a[0] + b[0]) / 2, a[1] - 7.0 * k)], np.clip(c * 1.5 + ember * 0.2, 0, 1), 0.7, 0.9)
    for i in range(8):
        v = (i + 0.5) / 8
        zz = lerp(z0, z1, v)
        a, b = P(x1, y1, zz - 2.6), P(x1, y1, zz + 2.6)
        kk_ = room.k(zz)
        c = side.tone(bronze, v, 1.0, 1.2)
        D.poly([a, b, (b[0], b[1] - 5.2 * kk_), ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 7.2 * kk_), (a[0], a[1] - 5.2 * kk_)], c)
    # ---- the front: a sunk field, three bosses (the middle one a lion's face with a ring), reeded ends
    front.fill(D, bronze, 6, 1, rng, 0.04, 0.78, u0=0.08, u1=0.92, v0=0.16, v1=0.80)
    front.line(D, [(0.08, 0.80), (0.92, 0.80)], "#120c0a", 1.3, 0.75, flat=True)
    front.line(D, [(0.92, 0.16), (0.92, 0.80)], "#120c0a", 1.1, 0.6, flat=True)
    front.line(D, [(0.08, 0.16), (0.92, 0.16)], bronze, 1.2, 0.85, 1.8)
    front.line(D, [(0.08, 0.16), (0.08, 0.80)], bronze, 1.0, 0.7, 1.6)
    for u in (0.02, 0.045, 0.955, 0.98):
        front.line(D, [(u, 0.04), (u, 0.96)], bronze, 0.9, 0.7, 0.5)
    for (u, r_) in ((0.22, 6.0), (0.5, 8.5), (0.78, 6.0)):
        cx, cy = front.at(u, 0.5)
        kk_ = front.k(u, 0.5)
        D.ellipse(cx + 0.8, cy + 1.2, r_ * kk_, r_ * kk_, "#120c0a", 0.6, fine=True)
        D.ellipse(cx, cy, r_ * kk_, r_ * kk_, front.tone(bronze, u, 0.5, 1.25))
        D.ellipse(cx - r_ * kk_ * 0.22, cy - r_ * kk_ * 0.25, r_ * kk_ * 0.5, r_ * kk_ * 0.45, front.tone(BRONZE, u, 0.5, 1.9), 0.9, fine=True)
    cx, cy = front.at(0.5, 0.5)
    kk_ = front.k(0.5, 0.5)
    for sx in (-1, 1):                                                                   # the lion: two eyes, a muzzle, the ring in its mouth
        D.ellipse(cx + sx * 3.0 * kk_, cy - 2.2 * kk_, 1.2, 0.9, "#1a100a", 0.9, fine=True)
    D.line([(cx - 2.4 * kk_, cy + 2.6 * kk_), (cx + 2.4 * kk_, cy + 2.6 * kk_)], "#1a100a", 0.8, 0.8)
    ring = [(cx + math.cos(a) * 7.5 * kk_, cy + 8.5 * kk_ + math.sin(a) * 7.5 * kk_) for a in np.linspace(-0.3, math.pi + 0.3, 14)]
    D.line(ring, front.tone(BRONZE, 0.5, 0.3, 1.5), max(0.9, 2.0 * kk_))
    D.line(ring[2:7], front.tone(BRONZE, 0.5, 0.3, 2.5), 0.7, 0.9)
    for u in np.linspace(0.12, 0.88, 9):
        front.dot(D, u, 0.90, 1.5, BRONZE, 2.0)
    # ---- the side toward the room: plain, with a carrying ring
    side.line(D, [(0.1, 0.2), (0.1, 0.8), (0.9, 0.8), (0.9, 0.2), (0.1, 0.2)], bronze, 1.0, 0.6, 0.5)
    cx, cy = side.at(0.5, 0.56)
    kk_ = side.k(0.5, 0.5)
    D.line([(cx + math.cos(a) * 3.2 * kk_, cy + 6 * kk_ + math.sin(a) * 6.5 * kk_) for a in np.linspace(0, 6.3, 14)], side.tone(BRONZE, 0.5, 0.4, 1.7), max(0.8, 1.6 * kk_))
    front.line(D, [(0, 0), (1, 0)], "#120c0a", 1.6, 0.7, flat=True)
    front.line(D, [(0, 1), (1, 1)], bronze, 1.2, 0.9, 2.0)
    # ---- an iron poker leaning on its corner
    a, b = P(x1 + 22, 0, z0 + 22), P(x1 - 6, y1 + 16, z0 + 8)
    D.line([a, b], "#34343c", 1.6, fine=False)
    D.line([(a[0] - 0.5, a[1]), (b[0] - 0.5, b[1])], "#8a8690", 0.5, 0.7)
    D.line([(b[0] + math.cos(t) * 2.6, b[1] - 2.6 + math.sin(t) * 2.6) for t in np.linspace(0, 6.3, 10)], "#34343c", 1.1)


# ======================================================================== putting it together
def wobble_field(seed=5, amount=0.9):
    """A gentle push for every ruled edge, so nothing in the picture is drawn with a ruler: whole
    pixels only (here one to the left, there one up), so that nothing is blurred by it."""
    x, y = grid(SHAPE)
    dx = np.rint((noise(SHAPE, (64, 64), seed, 2) - 0.5) * 2 * amount)
    dy = np.rint((noise(SHAPE, (64, 64), seed + 1, 2) - 0.5) * 2 * amount)
    return np.clip(x + dx, 0, W - 1).astype(np.intp), np.clip(y + dy, 0, H - 1).astype(np.intp)


WOB = wobble_field()


def wob(a):
    return np.ascontiguousarray(a[WOB[1], WOB[0]]).astype(F32)


def mottle(pic, seed=13, amount=1.0):
    """Paint is never an even coat: patches a little lighter and darker, warmer and cooler, at the size of
    a brush mark. This is what the brush pass then turns into strokes."""
    n1 = noise(SHAPE, 30, seed, 3) - 0.5
    n2 = noise(SHAPE, 10, seed + 1, 2) - 0.5
    d = noise(SHAPE, 80, seed + 2, 3) - 0.5
    out = pic * (1 + (n1 * 0.16 + n2 * 0.10)[..., None] * amount)
    out[..., 0] *= 1 + d * 0.10 * amount
    out[..., 2] *= 1 - d * 0.12 * amount
    return np.clip(out, 0, 1).astype(F32)


def sheets(D):
    """A Dual's five pictures, each pushed about by the same gentle wobble."""
    bc, ba, lc, la, diff = D.done()
    return wob(bc), wob(ba), wob(lc), wob(la), wob(diff)


def cutout(D, back, seed, fast, sizes=(7, 4, 2), keep=0.40, restate=0.60):
    """Brush a pair of sheets as a cut-out standing on the backdrop. -> (color, hard alpha)"""
    bc, ba, lc, la, diff = sheets(D)
    ys, xs = np.nonzero(la > 0.02)
    if len(ys) == 0:
        return back.copy(), np.zeros(SHAPE, dtype=F32)
    y0, y1, x0, x1 = max(ys.min() - 14, 0), min(ys.max() + 15, H), max(xs.min() - 14, 0), min(xs.max() + 15, W)
    flat = back.copy()
    over(flat, bc, ba)
    flat = lerp(flat, mottle(flat, seed, 0.7), ba[..., None])
    painted = flat.copy()
    if not fast:
        painted[y0:y1, x0:x1] = strokes(flat[y0:y1, x0:x1].copy(), sizes=sizes, seed=seed, density=1.8, jitter=0.04, keep=keep)
    over(painted, lc, la * (restate + (1 - restate) * diff))
    return painted, (la > 0.5).astype(F32)


def details(pic, places, seed=17):
    """The last crisp things, over everything: letters."""
    f = places["law"]
    cx, cy = f.at(0.5, 0.80)
    letter.carve(pic, "S·P·Q·R", (cx, cy), 8.5, dark="#3a2814", light="#f6dc98", amount=0.85, hand=False, rough=0.25, spacing=0.4, seed=seed)
    rng = np.random.default_rng(seed)
    for i in range(7):                                         # the law itself: lines of small letters
        v = 0.68 - i * 0.085
        u = 0.12
        while u < 0.86:
            run = 0.05 + 0.13 * rng.random()
            e = min(u + run, 0.88)
            a, b = f.at(u, v), f.at(e, v)
            m = mask_line(SHAPE, [a, b], 1.3)
            over(pic, "#3a2814", m * 0.7)
            over(pic, "#f0d490", np.roll(m, 1, axis=0) * (1 - m) * 0.35)
            u = e + 0.035 + 0.03 * rng.random()
    die = places["die"]
    cx, cy = die.at(0.5, 0.71)
    letter.carve(pic, "SATVRNO", (cx, cy), 6.6, dark="#2c1c10", light="#f8dc98", amount=0.9, hand=False, rough=0.2, spacing=0.5, seed=seed + 1)
    return pic


def paint(fast):
    t0 = time.time()
    base, info = shell()
    shadows(base, info)
    show(base, "out/rome-temple-0-shell.png")
    D, places = dress()
    places["die"] = PLACES["die"]
    bc, ba, lc, la, diff = sheets(D)
    under = wob(base)
    over(under, bc, ba)
    under = mottle(under)
    x, y = grid(SHAPE)
    corner = np.clip(((x - 400) / 400) ** 2 * 0.55 + ((y - 330) / 330) ** 2 * 0.45, 0, 1)     # the corners go deeper
    tint(under, "#3a2024", (corner ** 2 * 0.5).astype(F32))
    show(under, "out/rome-temple-1-under.png")
    print("under", round(time.time() - t0, 1))
    ids1 = info["ids"][::2, ::2]
    flow = np.where((ids1 == 1) | (ids1 == 2) | (ids1 == 3), math.pi / 2, 0.0).astype(F32)   # the brush goes down a wall and along a floor
    pic = under.copy() if fast else strokes(under, sizes=(10, 5, 2), seed=2, density=1.5, jitter=0.05, flow=flow, keep=0.30)
    over(pic, lc, la * (0.68 + 0.32 * diff))
    details(pic, places)
    print("back", round(time.time() - t0, 1))
    tc, ta = cutout(table_plane(), pic, 5, fast, sizes=(5, 3, 2), keep=0.45, restate=0.78)
    fc, fa = cutout(front_plane(), pic, 6, fast, sizes=(8, 4, 2))
    whole = pic.copy()
    over(whole, tc, ta)
    over(whole, fc, fa)
    show(whole, "out/rome-temple-2-all.png")
    show(pic, "out/rome-temple-2-back.png")
    print("painted", round(time.time() - t0, 1))
    return pic, (tc, ta), (fc, fa), info


# ======================================================================== the numbers the game needs
def hull(points):
    """The outline that goes round a set of points (convex), as whole pixels."""
    pts = sorted(set((round(float(x), 1), round(float(y), 1)) for x, y in points))

    def half(seq):
        out = []
        for p_ in seq:
            while len(out) >= 2 and (out[-1][0] - out[-2][0]) * (p_[1] - out[-2][1]) - (out[-1][1] - out[-2][1]) * (p_[0] - out[-2][0]) <= 0:
                out.pop()
            out.append(p_)
        return out
    lower, upper = half(pts), half(reversed(pts))
    return [[int(round(min(max(x, 0), W))), int(round(min(max(y, 0), H)))] for x, y in lower[:-1] + upper[:-1]]


def corners(x0, x1, y0, y1, z0, z1):
    return [P(x, y, z) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]


def layout(info):
    def fl(x, z):
        px, py = P(x, 0, z)
        return [int(round(px)), int(round(min(py, 598)))]

    def rect(pts, pad=2):
        xs, ys = [p_[0] for p_ in pts], [p_[1] for p_ in pts]
        x0, y0 = max(0, int(min(xs)) - pad), max(0, int(min(ys)) - pad)
        return [x0, y0, min(W, int(max(xs)) + pad) - x0, min(H, int(max(ys)) + pad) - y0]

    WX0, WX1, WZ = -272.0, 285.0, 872.0                       # the floor between the two rows of chests, up to the altar
    walk = [fl(-195, -26), fl(-195, 52), fl(WX0, 62), fl(WX0, WZ), fl(WX1, WZ), fl(WX1, -26)]
    blocked = [[fl(136, 198), fl(WX1, 198), fl(WX1, 350), fl(136, 350)]]                # the clerk's table, his sacks, his stool
    l0, r0 = sun_edges(-27.0)
    l1, r1 = sun_edges(SUN_Z)
    sun = [fl(l0, -27), fl(l1, SUN_Z), fl(r1, SUN_Z), fl(r0, -27)]
    T, SC = PED["top"], STATUE_SCALE
    god = corners(-PED["x"] - 10, PED["x"] + 10, 0, T, PED["z0"] - 10, PED["z0"]) + [P(-24 * SC, T + 291 * SC, 1165), P(24 * SC, T + 291 * SC, 1165), P(-106 * SC, T + 255 * SC, 1092)]
    hum = P(*HUM)
    left_near = [q for c in LEFT[:4] for q in corners(*c["box"])] + [P(-370, 130, 96), P(-304, 0, 300)]
    left_far = corners(*LEFT[4]["box"]) + [P(-366, 110, 950), P(-262, 0, 975), P(-316, 0, 934)]
    right_near = corners(*RIGHT[0]["box"]) + [P(368, 132, 62), P(300, 96, 16), P(318, 0, -6)]
    right_far = [q for c in RIGHT[1:] for q in corners(*c["box"])] + corners(*OPEN) + [P(395, 136, 800), P(336, 0, 842), P(380, 44, 905), P(390, 0, 930)]
    tx0, tx1, tz0, tz1, ty = TABLE
    table_pts = corners(tx0 - 3, tx1 + 3, 0, ty, tz0 - 3, tz1 + 3) + [P(236 - 27, ty + 52, 276), P(236 + 27, ty + 52, 276), P(tx0 - 58, 0, tz0 + 14), P(tx0 - 34, 52, tz0 + 14), P(LAMP[0], LAMP[1] + 8, LAMP[2])]
    std = [P(-362, 0, 1236), P(-290, 0, 1238), P(-396, 318, 1254), P(-292, 270, 1253), P(-330, 320, 1255)]
    out = {
        "id": "rome-temple", "horizon": HZ, "full": FULL,
        "light": "one hard patch of morning sun on the floor from the doors behind us (a little from the left); a brazier of coals at the front left, another by the altar, the clerk's lamp; the rest is dark",
        "walk": walk,
        "blocked": blocked,
        "planes": [{"id": "table", "file": "table.png", "base": int(round(P(tx0, 0, tz0 + 2)[1]))},
                   {"id": "front", "file": "front.png", "plane": "front"}],
        "things": [
            {"id": "sunpatch", "what": "the patch of sunlight on the floor", "shape": {"poly": sun}, "stand": fl(0, 60), "face": "NW"},
            {"id": "statue", "what": "the seated god on his pedestal", "shape": {"rect": rect(god)}, "stand": fl(0, 862), "face": "N"},
            {"id": "hum", "what": "the bare patch of wall that hums", "shape": {"rect": [int(hum[0]) - 22, int(hum[1]) - 44, 44, 84]}, "at": [int(round(hum[0])), int(round(hum[1]))], "stand": fl(-237, 255), "face": "NW"},
            {"id": "chests", "what": "the chests down the left wall", "shape": {"poly": hull(left_near)}, "stand": fl(-262, 250), "face": "W"},
            {"id": "chests2", "what": "the chest and sacks at the far left", "shape": {"poly": hull(left_far)}, "stand": fl(-250, 860), "face": "NW"},
            {"id": "chests3", "what": "the chests down the right wall, one of them open", "shape": {"poly": hull(right_far)}, "stand": fl(270, 640), "face": "E"},
            {"id": "chests4", "what": "the chest by the door on the right, law tablets leaning on it", "shape": {"poly": hull(right_near)}, "stand": fl(262, 60), "face": "E"},
            {"id": "table", "what": "the clerk's table: balance, silver, wax tablets, lamp", "shape": {"rect": rect(table_pts)}, "stand": fl(150, 172), "face": "NE"},
            {"id": "standards", "what": "old military standards leaning in the corner", "shape": {"rect": rect(std)}, "stand": fl(-240, 866), "face": "N"},
            {"id": "altar", "what": "the small altar table and its bowl", "shape": {"rect": rect(corners(-52, 52, 0, 96, 903, 960))}, "stand": fl(0, 862), "face": "N"},
            {"id": "brazier", "what": "the brazier of coals by the door", "shape": {"rect": rect(corners(BOX1[0], BOX1[1], 0, BRAZIER1[1] + 8, BOX1[2], BOX1[3]))}, "stand": fl(-190, 40), "face": "W"},
            {"id": "brazier2", "what": "the brazier by the altar", "shape": {"rect": rect(corners(BRAZIER2[0] - 30, BRAZIER2[0] + 30, 0, BRAZIER2[1] + 8, BRAZIER2[2] - 20, BRAZIER2[2] + 20))}, "stand": fl(150, 866), "face": "N"},
            {"id": "rack", "what": "the clerk's rack of rolls and tablets, and the keys", "shape": {"rect": rect(corners(*RACK))}, "stand": fl(270, 372), "face": "E"},
            {"id": "cat", "what": "a ginger cat asleep on the chest nearest the brazier (set dressing; a hotspot only if the story wants one)",
             "shape": {"rect": rect([P(CAT[0] - 24, CAT[1], CAT[2]), P(CAT[0] + 26, CAT[1] + 20, CAT[2])], 3)}, "stand": fl(-262, 150), "face": "W"},
        ],
        "exits": [{"to": "rome-steps", "shape": {"poly": [[290, 586], [510, 586], [510, 600], [290, 600]]}, "stand": [400, 594]}],
        "marks": {"son": fl(0, 29.2), "clerk": fl((STOOL[0] + STOOL[1]) / 2, STOOL[2] + 6)},
        "lights": {"sun": sun, "brazier": [int(round(v)) for v in P(BRAZIER1[0], BRAZIER1[1], BRAZIER1[2])],
                   "brazier2": [int(round(v)) for v in P(BRAZIER2[0], BRAZIER2[1], BRAZIER2[2])],
                   "lamp": [int(round(v)) for v in P(LAMP[0] - 9, LAMP[1] - 2, LAMP[2])]},
        "notes": "Cut-outs are 800x600, laid at 0,0. `hum.at` is the exact spot on the wall. The clerk's mark is his stool behind the table (not walking floor). `lights` are where the game may draw live glow; nothing glows in the paint but the coals and the flame themselves.",
    }
    with open(OUT + "/layout.json", "w") as f:
        json.dump(out, f, indent=1)
    return out


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.010, amount=0.016, gamma=0.6):
    """Grain, then a limited palette with speckle, as in the example; but this is a dark picture, so the
    grain is laid on in proportion to the light and the palette is chosen with the darks stretched out,
    or the shadows would be all noise and four colors."""
    h, w, _ = picture.shape
    rng = np.random.default_rng(seed)
    lum = picture @ np.array([0.3, 0.55, 0.15], dtype=F32)
    fine = rng.normal(0, 1, (h, w)).astype(F32)
    coarse = blur(rng.normal(0, 1, (h, w)).astype(F32), 0.8) * 1.6
    g = np.clip(picture + ((fine * 0.7 + coarse * 0.6) * amount * (0.30 + 0.9 * np.sqrt(np.clip(lum, 0, 1))))[..., None], 0, 1) ** gamma
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, np.clip(pal, 0, 1) ** (1 / gamma), alpha)
    return os.path.getsize(name)


def show(pic, name):
    Image.fromarray((np.clip(pic, 0, 1) * 255).astype(np.uint8)).save(name)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fast = len(sys.argv) > 1
    t0 = time.time()
    pic, (tc, ta), (fc, fa), info = paint(fast)
    layout(info)
    if fast:
        sys.exit()
    print("back", finish(pic, OUT + "/back.png", 152))
    print("table", finish(tc, OUT + "/table.png", 80, ta))
    print("front", finish(fc, OUT + "/front.png", 80, fa))
    comp = Image.open(OUT + "/back.png").convert("RGBA")       # everything laid together, as comp.py does it
    for name in ("table", "front"):
        comp.alpha_composite(Image.open(OUT + "/" + name + ".png").convert("RGBA"))
    comp.convert("RGB").save(OUT + "-comp.png")
    print("done", round(time.time() - t0, 1))

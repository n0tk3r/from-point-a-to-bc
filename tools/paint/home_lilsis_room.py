"""Little Sister's room, under the roof: 9:40 at night. We look along the ridge at the far gable and its window.
She is seven. What she loves above everything is chickens; after chickens, stuffed animals.

ONE camera (home_lilsis_room_model.VIEW) and everything through it: floor, walls, roof, every thing in the
room, every shadow and every pool of light (see home_lilsis_room_kit.Painter). The camera, the shell, the blanket
fort (its sign, its lights), the flashlight in its way in and the door at the right edge are where they were when
this was the girls' room.

LIGHT (kept to, everywhere):
  * The ROOSTER LAMP on her bedside table (right, half-way back), warm: the brightest thing in the room. It lights
    the pillow and its sign, the heap on the bed, the tea party from the right, the chart on the far wall.
  * The string of small lights on the fort (left), warm; the EGG night-light on the floor by the flock (far left), warm.
  * The moon in the window, pale blue: it falls as the window's own shape, slanted, down the floor and a little to
    the LEFT (the moon stands to the right), across the fried-egg rug.
  * A little warm light from the landing through the open door, front right, where people come in (it is what
    lights the hens on the foot of her quilt, and the nest).
  Everything no lamp reaches is cool blue-violet; the near corners and the foreground are the deepest, warmest darks.

THREE TONES: dark = the roof overhead, the foreground (hen house, toy box, crate, nest, door), the corners;
middle = the floor and the gable in the half-light; light = the window, the moon on the rug, the rooster lamp's
pool on the right, the fort's lights and the egg's glow on the left. The eye goes window -> moonlit rug -> the tea
party in the lamplight -> the bed and its sign; then left to the flock and the fort.

WHERE THINGS ARE (centimetres, home_lilsis_room_model.py). FAR WALL: her drawings (left of the window), the
chicken chart (right of it), her coat and boots. FAR LEFT: the flock, a mountain of stuffed animals with the chickens
on top. LEFT: the blanket fort. MIDDLE: the tea party; every guest is a chicken. RIGHT: her bed, heaped with
animals, one round place kept free on the pillow, RESERVED. FRONT PLANE: toy box, a crate of picture books, the toy
hen house (the dollhouse: a hen in every window, a ramp), the nest, a mobile of felt chickens, the door.

    python3 home_lilsis_room.py          everything (brush pass, PNG-8 files, layout.json)
    python3 home_lilsis_room.py fast     no brush pass: out/home-lilsis-room-2-all.png only
"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

import home_lilsis_room_model as M
from brush import F32, blur, grain, lerp, noise, palette_of, rgb, sample, save, smooth, strokes, to_palette, warp
from home_lilsis_room_hens import BEAK, RED, egg, flat_hen, hen, stroke_word, tiny_width, tiny_word
from home_lilsis_room_kit import Card, Layer, Painter, Tile, add, col, footprint, hash01, lines, mix, sub, unit
from room import View

SHAPE = (600, 800)
OUT = "out/home-lilsis-room"
v = View(**M.VIEW)
p = Painter(v, SHAPE)
p.ambient, p.night = col((0.37, 0.40, 0.60)), 0.24
rng = np.random.default_rng(41)
SIGNS = {}                                                   # where the lettering came out in the picture (for layout.json)

WD, KNEE, RIDGE = M.W, M.KNEE, M.RIDGE
RUN = (RIDGE - KNEE) / (WD / 2)                              # how fast the roof climbs (cm up per cm across)
SLOPE_LEN = math.hypot(WD / 2, RIDGE - KNEE)
NL = unit((RIDGE - KNEE, -WD / 2, 0))                        # the left slope's face (looking down into the room)
NR = unit((-(RIDGE - KNEE), -WD / 2, 0))                     # the right slope's
WX0, WX1, WY0, WY1 = M.WINDOW


def roof_y(X):
    return KNEE + RUN * min(X, WD - X)


# ================================================================ light
LAMP = (583, 106, 220)                                       # the bulb of the rooster lamp, on her bedside table
EGG = (288, 15, 40)                                          # the egg-shaped night-light, on the floor by the flock
MOON = unit((math.cos(math.radians(38)) * math.sin(math.radians(15)), math.sin(math.radians(38)), -math.cos(math.radians(38)) * math.cos(math.radians(15))))
DOORL = (566, 150, 800)                                      # the lamp on the landing, seen through the doorway
PPC = 4.0                                                    # the window is drawn at 4 pixels to the centimetre
BRANCHES = [                                                 # the tree outside, in window measurements (cm from the glass's left, from its top), with widths
    ([(-6, 150), (10, 118), (22, 84), (40, 52), (52, 26), (60, -4)], 5.0),
    ([(22, 84), (44, 78), (66, 62), (92, 56), (122, 40)], 2.6),
    ([(40, 52), (26, 30), (20, 8), (18, -4)], 2.2),
    ([(10, 118), (36, 122), (58, 112), (84, 114), (104, 100)], 2.4),
    ([(66, 62), (74, 40), (86, 24), (90, 6)], 1.5),
    ([(58, 112), (70, 134), (88, 146), (110, 150)], 1.6),
    ([(92, 56), (104, 70), (118, 76)], 1.2),
    ([(44, 78), (40, 98), (48, 108)], 1.1),
    ([(26, 30), (10, 22), (-4, 26)], 1.3),
    ([(84, 114), (96, 126), (116, 124)], 1.0),
]


def window_pictures():
    """-> (the night seen through the glass, how much moonlight each place of the glass lets through)."""
    gw, gh = WX1 - WX0, WY1 - WY0
    w, h = int(gw * PPC), int(gh * PPC)
    yy, xx = np.mgrid[0:h, 0:w].astype(F32)
    t = yy / h
    sky = lerp(col((0.035, 0.07, 0.24)), col((0.11, 0.20, 0.47)), t[..., None] ** 1.3) * (0.9 + 0.2 * noise((h, w), 90, 5, 3)[..., None])
    sky = sky + col((0.10, 0.13, 0.20)) * np.clip((t - 0.78) / 0.22, 0, 1)[..., None] ** 2          # a paler band low down
    cloud = noise((h, w), (240, 60), 9, 4)                                                           # one thin cloud
    sky = sky + col((0.10, 0.13, 0.22)) * (smooth((cloud - 0.56) / 0.2) * np.clip(1 - np.abs(t - 0.36) / 0.2, 0, 1))[..., None]
    star = np.random.default_rng(3)
    for _ in range(46):
        sx, sy = star.random() * w, star.random() * h * 0.8
        b = 0.35 + star.random() * 0.65
        r = 1.2 + star.random() * 1.3
        sky += (np.exp(-((xx - sx) ** 2 + (yy - sy) ** 2) / (r * r)) * b)[..., None] * col((0.85, 0.9, 1.0))
    mx, my, mr = 84 * PPC, 44 * PPC, 9.5 * PPC                                                       # the moon, upper right
    d = np.hypot(xx - mx, yy - my)
    sky += (np.exp(-(d / (mr * 3.4)) ** 2) * 0.30)[..., None] * col((0.55, 0.68, 1.0))               # its halo
    disc = np.clip((mr - d) + 0.5, 0, 1)
    face = col((1.0, 0.98, 0.86)) * (0.92 + 0.16 * noise((h, w), 26, 12, 3)[..., None]) * 1.5
    sky = sky * (1 - disc[..., None]) + face * disc[..., None]
    # far off, the dark hill and one neighbour's window
    hill = (yy > h * (0.90 + 0.035 * np.sin(xx / w * 5.0 + 1.0) + 0.02 * noise((h, w), 70, 4, 2))).astype(F32)
    sky = sky * (1 - hill[..., None]) + col((0.03, 0.045, 0.10)) * hill[..., None]
    c = Card(gw, gh, (0, 0, 0), PPC, clear=True)
    for pts, wd in BRANCHES:
        c.line(pts, (0.02, 0.03, 0.07), wd)
    twig = np.random.default_rng(8)
    for pts, wd in BRANCHES[1:]:                                                                     # twigs and the last leaves
        for (ax, ay), (bx, by) in zip(pts[:-1], pts[1:]):
            for _ in range(3):
                u = twig.random()
                px, py = ax + (bx - ax) * u, ay + (by - ay) * u
                ang = twig.random() * 6.28
                ln = 5 + twig.random() * 9
                c.line([(px, py), (px + math.cos(ang) * ln, py - abs(math.sin(ang)) * ln)], (0.02, 0.03, 0.07), 0.6)
                if twig.random() < 0.5:
                    c.disc(px + math.cos(ang) * ln, py - abs(math.sin(ang)) * ln, 1.4, (0.03, 0.05, 0.09), 0.9)
    c.rect(96, 170, 99.5, 173.5, (1.0, 0.75, 0.35))                                                   # the neighbour's lit window
    tc, ta = c.done()
    night = sky * (1 - ta[..., None]) + tc * ta[..., None]
    # what the moon's light gets through: the glass, less the tree, the sash bars and the frame
    pad = int(6 * PPC)
    through = np.zeros((h + 2 * pad, w + 2 * pad), F32)
    glass = (1 - ta * 0.85)
    for bx, hw in ((gw / 2, 1.8),):
        glass *= 1 - (np.abs(xx / PPC - bx) < hw)
    for by, hw in ((gh / 2, 3.0), (gh * 0.25, 1.3), (gh * 0.75, 1.3)):
        glass *= 1 - (np.abs(yy / PPC - by) < hw)
    glass *= ((xx / PPC > 5) & (xx / PPC < gw - 5) & (yy / PPC > 5) & (yy / PPC < gh - 5))
    through[pad:pad + h, pad:pad + w] = glass
    return night.astype(F32), blur(through, 2.2 * PPC), pad


NIGHT, THROUGH, TPAD = window_pictures()


def moon_gate(X, Y, Z):
    s = np.maximum(Z, 0) / -MOON[2]
    qx, qy = X + MOON[0] * s, Y + MOON[1] * s
    g = sample(THROUGH, (qx - WX0) * PPC + TPAD, (WY1 - qy) * PPC + TPAD)
    return g * (Z > 0.5)


def lamp_gate(X, Y, Z):
    """The shade: full light below its rim and straight up through its top; the shade itself only glows."""
    dx, dy, dz = X - LAMP[0], Y - LAMP[1], Z - LAMP[2]
    e = dy / np.sqrt(dx * dx + dy * dy + dz * dz + 1e-3)
    return 0.40 + 0.60 * np.maximum(smooth((-0.22 - e) / 0.22), smooth((e - 0.72) / 0.16))


def door_gate(X, Y, Z):
    s = (700 - Z) / np.maximum(DOORL[2] - Z, 1e-3)
    qx, qy = X + (DOORL[0] - X) * s, Y + (DOORL[1] - Y) * s
    g = smooth((qx - 533) / 5 + 0.5) * smooth((M.DOOR_X - qx) / 5 + 0.5) * smooth((203 - qy) / 5 + 0.5)
    return np.where(Z < 700, g, 0.0)


FORT_BULBS = []                                              # filled in by fort(): where the little bulbs are
WARM = col((1.0, 0.76, 0.42))
p.lights = [
    dict(name="lamp", pos=LAMP, color=WARM, power=4.6, r=136, gate=lamp_gate, wrap=0.18, soft=1.8),
    dict(name="lampair", pos=(LAMP[0], LAMP[1] + 40, LAMP[2] + 20), color=col((1.0, 0.72, 0.44)), power=0.22, r=300, wrap=1.0, cast=False),
    dict(name="moon", dir=MOON, color=col((0.50, 0.68, 1.0)), power=1.7, gate=moon_gate),
    dict(name="sky", pos=(360, 205, -70), color=col((0.38, 0.52, 0.95)), power=1.0, r=300, wrap=0.3, cast=False, gate=lambda X, Y, Z: (Z > 1.0)),
    dict(name="fort1", pos=(96, 126, 330), color=col((1.0, 0.80, 0.46)), power=0.80, r=64, wrap=0.4, cast=False),
    dict(name="fort2", pos=(90, 118, 418), color=col((1.0, 0.80, 0.46)), power=1.25, r=70, wrap=0.4, cast=False),
    dict(name="fort3", pos=(166, 84, 418), color=col((1.0, 0.80, 0.46)), power=1.05, r=62, wrap=0.4, cast=False),
    dict(name="fortair", pos=(110, 140, 430), color=col((1.0, 0.78, 0.50)), power=0.16, r=220, wrap=1.0, cast=False),
    dict(name="egg", pos=(EGG[0], EGG[1] + 4, EGG[2] + 6), color=col((1.0, 0.70, 0.40)), power=3.2, r=84, wrap=0.45, soft=2.4),
    dict(name="door", pos=DOORL, color=col((1.0, 0.72, 0.42)), power=2.5, r=230, gate=door_gate, wrap=0.2, soft=2.0),
    dict(name="coop", pos=(348, 26, 608), color=col((1.0, 0.78, 0.44)), power=0.5, r=44, wrap=0.5, cast=False),
]

p.fill = lambda X, Y, Z, n: col((0.36, 0.28, 0.26)) * (np.clip(-(n[1] + 0 * X), 0, 1) * 0.5)[..., None]      # what comes back up off the floor
GRAIN = Tile(48, 21)
STAIN = Tile(120, 22, octaves=3)
FINE = Tile(9, 23, octaves=2)


def tone(x):
    """Roll the brights off softly (a lamp must not burn a hole in the picture)."""
    return 1 - np.exp(-np.clip(x, 0, 8) * 1.22)


def tone_inv(c):
    """The paint to ask for so that it comes out of tone() as the color wanted."""
    c = np.clip(col(c), 0, 0.985)
    return -np.log(1 - c) / 1.22


# ================================================================ the shell: floor, walls, roof
WOOD = col((0.50, 0.32, 0.18))
PINE = col((0.80, 0.58, 0.36))
MINT = col((0.68, 0.87, 0.77))
MINT_LOW = col((0.42, 0.68, 0.62))
WHITE = col((0.92, 0.90, 0.84))


def floor_albedo(X, Y, Z, t):
    fx, fz = footprint(X), footprint(Z)
    b = np.floor(X / 12.0)
    per = 150 + 100 * hash01(b, 1.0)
    off = per * hash01(b, 2.0)
    seg = np.floor((Z + off) / per)
    tn = hash01(b, seg, 3.0)
    c = lerp(col((0.68, 0.40, 0.18)), col((0.92, 0.64, 0.32)), tn[..., None])
    c = c * (1 + (GRAIN.at(X * 7.0 + b * 37, Z * 0.55) - 0.5)[..., None] * 0.20)          # grain, drawn out along each board
    c = c * (1 + (STAIN.at(X * 1.1, Z * 1.1) - 0.5)[..., None] * 0.22)                    # old wear and polish
    worn = np.exp(-((X - 350) / 170.0) ** 2) * np.clip((Z - 60) / 200, 0, 1)              # paler where feet go
    c = lerp(c, c * col((1.10, 1.07, 1.02)), (worn * 0.55)[..., None])
    gap = lines(X, 12.0, 0.75, fx)
    joint = lines(Z + off, per, 0.7, fz) * (1 - gap)
    c = c * (1 - 0.62 * gap - 0.50 * joint)[..., None]
    lip = lines(X, 12.0, 0.5, fx, offset=0.9)                                             # the lit edge beside each gap
    return c * (1 + 0.10 * lip * (1 - gap))[..., None] * col((0.93, 0.85, 0.75))          # (deep and warm: the same boards as the study next door)


RAIL = 92.0                                                  # a white rail round the room at the height of the window sill


def wall_paint(u, Y, fu, fy, seed=0.0):
    """Painted boards, upright, 11 cm wide: a pale green above the rail, a deeper green below it; a white skirting board."""
    b = np.floor(u / 11.0)
    low = np.clip((RAIL - Y) / np.maximum(fy, 1e-3) + 0.5, 0, 1)
    c = lerp(MINT, MINT_LOW, low[..., None]) * (0.95 + 0.10 * hash01(b, seed + 1.0))[..., None]
    c = c * (1 + (STAIN.at(u * 1.4 + seed * 90, Y * 1.4) - 0.5)[..., None] * 0.16)
    c = c * (1 - 0.40 * lines(u, 11.0, 0.8, fu))[..., None]
    c = c * (1 + 0.07 * lines(u, 11.0, 0.6, fu, offset=1.0))[..., None]
    rail = np.clip((2.6 - np.abs(Y - (RAIL + 2.2))) / np.maximum(fy, 1e-3) + 0.5, 0, 1)
    c = lerp(c, WHITE, rail[..., None])
    c = c * (1 - 0.34 * np.clip(1 - np.abs(Y - (RAIL - 1.2)) / np.maximum(fy * 0.9, 0.6), 0, 1))[..., None]        # the rail's shadow
    sk = np.clip((13.0 - Y) / np.maximum(fy, 1e-3) + 0.5, 0, 1)
    c = lerp(c, WHITE * (0.95 + 0.1 * FINE.at(u * 2, Y * 6))[..., None], sk[..., None])
    c = c * (1 - 0.45 * np.clip(1 - np.abs(Y - 13.0) / np.maximum(fy * 0.9, 0.5), 0, 1))[..., None]
    return c * (1 - 0.30 * np.clip(1 - np.abs(Y - 9.5) / np.maximum(fy * 0.7, 0.4), 0, 1))[..., None]


def gable_albedo(X, Y, Z, t):
    return wall_paint(X, Y, footprint(X), footprint(Y), 0.0)


def left_wall_albedo(X, Y, Z, t):
    return wall_paint(Z, Y, footprint(Z), footprint(Y), 3.0)


def right_wall_albedo(X, Y, Z, t):
    return wall_paint(Z, Y, footprint(Z), footprint(Y), 7.0)


def roof_albedo(side):
    def f(X, Y, Z, t):
        s = np.hypot(X if side < 0 else WD - X, Y - KNEE)                                  # up the slope from the knee wall
        fs = footprint(s)
        b = np.floor(s / 15.0)
        c = PINE * (0.90 + 0.20 * hash01(b, 11.0 + side))[..., None]
        c = c * (1 + (STAIN.at(Z * 0.8, s * 2.2 + side * 60) - 0.5)[..., None] * 0.24)
        c = c * (1 + (GRAIN.at(Z * 0.5, s * 6.0) - 0.5)[..., None] * 0.16)
        c = c * (1 - 0.50 * lines(s, 15.0, 0.9, fs))[..., None]
        seg_off = 300 * hash01(b, 12.0 + side)
        knot = STAIN.at(Z * 2.1 + 40 * b, s * 9.0) > 0.86                                  # a knot here and there
        c = c * (1 - 0.30 * knot)[..., None]
        return c * (1 - 0.30 * lines(Z + seg_off, 330.0, 0.8, footprint(Z)))[..., None]    # where two boards butt
    return f


def roof_amb(X, Y, Z):
    return (0.92 + 0.36 * np.exp(-np.maximum(Z, 0) / 500.0) - 0.16 * np.clip((Y - 250) / 170.0, 0, 1)) * (1 - 0.40 * np.clip((Z - 660) / 420.0, 0, 1))


def floor_amb(X, Y, Z):
    a = 1 - 0.30 * np.exp(-np.maximum(Z, 0) / 45.0) - 0.26 * np.exp(-np.maximum(X, 0) / 40.0) - 0.26 * np.exp(-np.maximum(WD - X, 0) / 40.0)
    return np.clip(a, 0.3, 1)


def wall_amb(X, Y, Z):
    return np.clip(0.80 + 0.20 * np.clip(Y / 60.0, 0, 1) - 0.10 * np.clip((Y - 200) / 220, 0, 1), 0.3, 1)


def rafter_albedo(tn, seed):
    def f(X, Y, Z, t):
        s = np.hypot(np.minimum(X, WD - X), Y - KNEE)
        g = GRAIN.at(s * 0.6 + seed * 31, (Y - RUN * np.minimum(X, WD - X)) * 9.0 + seed * 17)
        return WOOD * tn * (0.86 + 0.28 * g)[..., None]
    return f


def shell(L):
    far = 1186.0
    floor = [(0, 0, 0), (WD, 0, 0), (WD, 0, far), (0, 0, far)]
    p.face(L, floor, floor_albedo, (0, 1, 0), keep=0.62, shadow=True, amb=floor_amb)
    p.light_on(L, floor, lambda X, Y, Z: moon_gate(X, Y, Z) * 0.34, (0.55, 0.70, 1.0))      # the boards are polished: the moon lies ON them, pale blue
    p.face(L, [(0, 0, 0), (WD, 0, 0), (WD, KNEE, 0), (WD / 2, RIDGE, 0), (0, KNEE, 0)], gable_albedo, (0, 0, 1), keep=0.62, shadow=True, amb=wall_amb)
    p.face(L, [(0, 0, 0), (0, 0, far), (0, KNEE, far), (0, KNEE, 0)], left_wall_albedo, (1, 0, 0), keep=0.62, shadow=True, amb=wall_amb)
    p.face(L, [(WD, 0, 0), (WD, 0, far), (WD, KNEE, far), (WD, KNEE, 0)], right_wall_albedo, (-1, 0, 0), keep=0.62, shadow=True, amb=wall_amb)
    p.face(L, [(0, KNEE, 0), (WD / 2, RIDGE, 0), (WD / 2, RIDGE, far), (0, KNEE, far)], roof_albedo(-1), NL, keep=0.55, amb=roof_amb)
    p.face(L, [(WD, KNEE, 0), (WD / 2, RIDGE, 0), (WD / 2, RIDGE, far), (WD, KNEE, far)], roof_albedo(1), NR, keep=0.55, amb=roof_amb)
    # the wall plates along the tops of the knee walls
    p.box(L, 0, 7, KNEE - 7, KNEE + 1, 0, far, WOOD * 1.1, keep=0.75, amb=0.8)
    p.box(L, WD - 7, WD, KNEE - 7, KNEE + 1, 0, far, WOOD * 1.1, keep=0.75, amb=0.8)
    # rafters every 60 cm, the far ones first: each a beam 7 wide and 13 deep under the boards
    dp, hw = 13.0, 3.5
    for i in range(0, 20):
        zc = 4 + 60.0 * i
        if zc + hw > v.cam_z - 30:
            break
        for side, n, K, Rg in ((-1, NL, (0, KNEE), (WD / 2 - 6, RIDGE - 6 * RUN)), (1, NR, (WD, KNEE), (WD / 2 + 6, RIDGE - 6 * RUN))):
            k2, r2 = (K[0] + n[0] * dp, K[1] + n[1] * dp), (Rg[0] + n[0] * dp, Rg[1] + n[1] * dp)
            tn = 0.9 + 0.2 * ((i * 7 + (side > 0) * 3) % 5) / 4.0
            # the face toward us, then the underside, then the light along its lower edge
            p.face(L, [(K[0], K[1], zc + hw), (Rg[0], Rg[1], zc + hw), (r2[0], r2[1], zc + hw), (k2[0], k2[1], zc + hw)], rafter_albedo(tn, i + side), (0, 0, 1), keep=0.75, amb=roof_amb)
            p.face(L, [(k2[0], k2[1], zc - hw), (r2[0], r2[1], zc - hw), (r2[0], r2[1], zc + hw), (k2[0], k2[1], zc + hw)], WOOD * tn * 0.92, n, keep=0.75, amb=roof_amb)
            p.seg(L, (k2[0], k2[1], zc + hw), (r2[0], r2[1], zc + hw), WOOD * 1.9, 0.9, min_px=0.7, alpha=0.55, max_px=1.5, fine=False, lit=(0, -0.6, 0.8), keep=0.8)
    # the ridge beam, high along the middle
    p.box(L, WD / 2 - 9, WD / 2 + 9, RIDGE - 34, RIDGE - 2, 0, far, {"all": WOOD * 0.95, "bottom": WOOD * 1.1}, keep=0.75, amb=0.8)
    # a purlin half-way up each slope: it runs straight to the vanishing point
    for side, n in ((-1, NL), (1, NR)):
        cx = WD / 2 + side * (WD / 4 + 4)
        cy = roof_y(cx) - 22
        p.box(L, cx - 6, cx + 6, cy, cy + 14, 0, far, {"all": WOOD * 1.0, "bottom": WOOD * 1.15}, keep=0.75, amb=0.85)
        p.seg(L, (cx - side * 6, cy, 0), (cx - side * 6, cy, far - 90), WOOD * 2.0, 1.0, alpha=0.5, max_px=1.8, fine=False, lit=(-side * 0.5, -0.7, 0.5), keep=0.8)
    p.seg(L, (WD / 2 - 9, RIDGE - 34, 0), (WD / 2 - 9, RIDGE - 34, far - 90), WOOD * 2.0, 1.0, alpha=0.5, max_px=1.8, fine=False, lit=(-0.6, -0.7, 0.4), keep=0.8)


# ================================================================ helpers for cloth, paper and toys
def tex_xy(tex, x0, y1, ppc):
    """A drawn sheet hung in a plane that faces us: read it by X (across) and Y (height)."""
    return lambda X, Y, Z, t: sample(tex, (X - x0) * ppc, (y1 - Y) * ppc)


def folds(u, period, depth=0.22, seed=0.0, sharp=1.0):
    """Light and dark down the folds of hanging cloth (a multiplier), `u` across the folds in cm."""
    w = np.sin(u / period * 6.2832 + seed) * 0.6 + np.sin(u / period * 6.2832 * 2.3 + seed * 3.1) * 0.4
    return 1 + depth * np.tanh(w * sharp)


def rot2(cx, cy, w, h, deg):
    """The corners (TL, TR, BL) of a sheet w x h, turned by `deg` about its middle, in a plane's own (u, v) with v UP."""
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    def at(du, dv):
        return (cx + du * c - dv * s, cy + du * s + dv * c)
    return at(-w / 2, h / 2), at(w / 2, h / 2), at(-w / 2, -h / 2)


def on_gable(L, tex, alpha, cx, cy, w, h, deg=0.0, z=0.5, **kw):
    tl, tr, bl = rot2(cx, cy, w, h, deg)
    return p.quad_image(L, (tl[0], tl[1], z), (tr[0], tr[1], z), (bl[0], bl[1], z), tex, alpha, **kw)


CRAYON = dict(red=(0.86, 0.16, 0.14), blue=(0.16, 0.32, 0.80), green=(0.18, 0.58, 0.26), yellow=(0.98, 0.80, 0.12), purple=(0.52, 0.24, 0.66),
              pink=(0.94, 0.38, 0.62), orange=(0.96, 0.52, 0.12), brown=(0.48, 0.30, 0.16), black=(0.14, 0.12, 0.16), sky=(0.42, 0.70, 0.94))


def scribble(card, x0, y0, x1, y1, color, w=0.5, n=14, seed=0):
    """Fill a box the way a child colors in: back and forth, not quite to the edges."""
    r = np.random.default_rng(seed)
    pts = []
    for i in range(n + 1):
        yy = y0 + (y1 - y0) * i / n
        pts.append((x0 + r.random() * 0.8, yy + r.normal(0, 0.15)) if i % 2 == 0 else (x1 - r.random() * 0.8, yy + r.normal(0, 0.15)))
    card.line(pts, color, w)


def stick_person(card, x, y, h, color, hair=None, skirt=False, seed=0):
    """A child's person: round head, a line for a body, lines for arms and legs. (x, y) is the feet."""
    r = np.random.default_rng(seed)
    hd = h * 0.17
    card.ring(x, y - h + hd, hd, color, 0.55)
    top, hip = y - h + 2 * hd, y - h * 0.36
    card.line([(x, top), (x + r.normal(0, 0.2), hip)], color, 0.55)
    card.line([(x - h * 0.24, top + h * 0.20 + r.normal(0, 0.4)), (x, top + h * 0.10), (x + h * 0.24, top + h * 0.20 + r.normal(0, 0.4))], color, 0.5)
    if skirt:
        card.poly([(x, top + h * 0.16), (x - h * 0.2, hip + h * 0.06), (x + h * 0.2, hip + h * 0.06)], color)
    card.line([(x - h * 0.16, y), (x, hip), (x + h * 0.16, y)], color, 0.55)
    card.disc(x - hd * 0.38, y - h + hd * 0.85, 0.28, CRAYON["black"])
    card.disc(x + hd * 0.38, y - h + hd * 0.85, 0.28, CRAYON["black"])
    card.line([(x - hd * 0.4, y - h + hd * 1.35), (x, y - h + hd * 1.6), (x + hd * 0.4, y - h + hd * 1.35)], CRAYON["red"], 0.3)
    if hair is not None:
        for a in np.linspace(-1.2, 1.2, 6):
            card.line([(x + math.sin(a) * hd, y - h + hd - math.cos(a) * hd), (x + math.sin(a) * hd * 1.5, y - h + hd - math.cos(a) * hd * 1.2 + (hd * 1.6 if abs(a) > 0.9 and skirt else 0))], hair, 0.4)


def taped(L, cx, cy, w, h, deg, z=0.7, wall="gable", at=0.0):
    """Four scraps of tape on a sheet's corners (so that it is a thing put up by hand, not printed on the wall)."""
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    for du, dv in ((-w / 2, h / 2), (w / 2, h / 2)):
        u, vv = cx + du * c - dv * s, cy + du * s + dv * c
        if wall == "gable":
            p.poly3(L, [(u - 2.4, vv + 1.0, z), (u + 2.4, vv + 1.6, z), (u + 2.6, vv - 0.8, z), (u - 2.2, vv - 1.4, z)], (0.94, 0.90, 0.74), 0.9, fine=False, lit=(0, 0, 1), keep=0.8)
        else:
            p.poly3(L, [(at, vv + 1.0, u - 2.4), (at, vv + 1.6, u + 2.4), (at, vv - 0.8, u + 2.6), (at, vv - 1.4, u - 2.2)], (0.94, 0.90, 0.74), 0.9, fine=False, lit=(1 if at < 360 else -1, 0, 0), keep=0.8)


def animal(L, kind, P, h, turn=0.0, lean=0.0, keep=0.75, fine=False, flop=False, fur_=None, pale_=None):
    """A stuffed animal, sitting, made of round parts and lit like everything else. P = where it sits; h = its height (cm)."""
    R = (p.R[0] * math.cos(turn), 0, p.R[2] * math.cos(turn))
    def at(dx, dy, dz=0.0):
        return (P[0] + R[0] * dx * h + lean * dy * h, P[1] + dy * h, P[2] + R[2] * dx * h + dz * h)
    fur, pale, extra = dict(bear=((0.62, 0.42, 0.24), (0.86, 0.72, 0.52), None), rabbit=((0.93, 0.90, 0.88), (0.98, 0.72, 0.78), None),
                            elephant=((0.60, 0.68, 0.82), (0.82, 0.86, 0.94), None), giraffe=((0.96, 0.78, 0.32), (0.99, 0.92, 0.66), (0.60, 0.36, 0.14)),
                            frog=((0.42, 0.72, 0.36), (0.80, 0.92, 0.56), None), lamb=((0.95, 0.93, 0.87), (0.36, 0.30, 0.30), None),
                            duck=((0.98, 0.84, 0.24), (0.96, 0.54, 0.14), None), pig=((0.96, 0.66, 0.70), (0.99, 0.82, 0.84), None))[kind]
    fur = fur if fur_ is None else fur_
    pale = pale if pale_ is None else pale_
    kw = dict(keep=keep, fine=fine)
    if kind == "giraffe":
        spots = lambda u, vv, a: np.where((np.sin(u * 7 + 1) * np.sin(vv * 7 + 2) > 0.35)[..., None], col(extra), a)
        p.ball(L, at(0, 0.20), 0.17 * h, fur, sy=1.05, spots=spots, **kw)
        for i in range(5):
            p.ball(L, at(0.02 * i, 0.36 + i * 0.105), 0.075 * h, fur, spots=spots, **kw)
        p.ball(L, at(0.11, 0.90), 0.10 * h, fur, sx=1.25, sy=0.8, **kw)
        p.ball(L, at(0.20, 0.87), 0.05 * h, pale, **kw)
        for s in (-1, 1):
            p.seg(L, at(0.05 + s * 0.03, 0.96), at(0.05 + s * 0.05, 1.04), extra, 1.2, fine=fine, lit=p.B)
        p.dot(L, at(0.13, 0.925, 0.02), 0.012 * h, (0.08, 0.06, 0.08), fine=True)
        return
    # legs first (they stick out toward us), then body, arms, head
    for s in (-1, 1):
        p.ball(L, at(s * 0.20, 0.09, 0.10), 0.115 * h, fur, sx=0.95, sy=0.8, **kw)
        if kind in ("bear", "rabbit", "pig"):
            p.ball(L, at(s * 0.21, 0.09, 0.16), 0.055 * h, pale, **kw)
    p.ball(L, at(0, 0.30), 0.27 * h, fur, sx=0.95, sy=1.05, **kw)
    if kind in ("bear", "frog", "duck", "pig"):
        p.ball(L, at(0, 0.27, 0.1), 0.17 * h, pale, sx=0.9, sy=1.0, flat=0.3, **kw)
    for s in (-1, 1):
        p.ball(L, at(s * 0.27, 0.40 if not flop else 0.30, 0.04), 0.085 * h, fur, sx=0.8, sy=1.25, rot=s * 0.5, **kw)
    hy = 0.70
    if kind == "rabbit":
        for s in (-1, 1):
            p.ball(L, at(s * 0.10 + (0.06 if flop and s > 0 else 0), hy + 0.33), 0.20 * h, fur, sx=0.30, sy=1.0, rot=s * 0.16 + (0.9 if flop and s > 0 else 0), **kw)
            p.ball(L, at(s * 0.10 + (0.06 if flop and s > 0 else 0), hy + 0.33), 0.14 * h, pale, sx=0.22, sy=1.0, rot=s * 0.16 + (0.9 if flop and s > 0 else 0), flat=0.5, **kw)
    elif kind in ("bear", "pig", "frog"):
        for s in (-1, 1):
            p.ball(L, at(s * 0.155, hy + 0.165), 0.075 * h, fur if kind != "frog" else (0.95, 0.95, 0.9), **kw)
            if kind == "bear":
                p.ball(L, at(s * 0.155, hy + 0.165, 0.02), 0.04 * h, pale, flat=0.5, **kw)
            if kind == "frog":
                p.dot(L, at(s * 0.155, hy + 0.165, 0.03), 0.03 * h, (0.06, 0.06, 0.08), fine=True)
    elif kind == "elephant":
        for s in (-1, 1):
            p.ball(L, at(s * 0.24, hy + 0.02), 0.15 * h, fur, sx=0.75, sy=1.1, **kw)
            p.ball(L, at(s * 0.24, hy + 0.02, 0.02), 0.10 * h, pale, sx=0.7, sy=1.1, flat=0.5, **kw)
    elif kind == "lamb":
        for s in (-1, 1):
            p.ball(L, at(s * 0.20, hy + 0.03), 0.07 * h, pale, sx=1.3, sy=0.7, rot=s * 0.4, **kw)
    p.ball(L, at(0, hy), 0.20 * h, fur, **kw)
    if kind == "bear":
        p.ball(L, at(0, hy - 0.05, 0.1), 0.095 * h, pale, sx=1.1, sy=0.85, flat=0.3, **kw)
        p.dot(L, at(0, hy - 0.02, 0.2), 0.03 * h, (0.10, 0.07, 0.07), fine=True)
    elif kind == "rabbit":
        p.dot(L, at(0, hy - 0.04, 0.2), 0.026 * h, (0.90, 0.40, 0.50), fine=True)
    elif kind == "elephant":
        for i in range(4):
            p.ball(L, at(0.0 + 0.012 * i * i, hy - 0.06 - i * 0.085, 0.12), (0.075 - 0.009 * i) * h, fur, **kw)
    elif kind == "lamb":
        p.ball(L, at(0, hy - 0.03, 0.1), 0.11 * h, pale, sx=0.9, sy=1.05, flat=0.3, **kw)
    elif kind == "duck":
        p.ball(L, at(0, hy - 0.05, 0.14), 0.085 * h, pale, sx=1.5, sy=0.55, **kw)
    elif kind == "pig":
        p.ball(L, at(0, hy - 0.04, 0.12), 0.075 * h, pale, sx=1.2, sy=0.85, flat=0.3, **kw)
    elif kind == "frog":
        p.seg(L, at(-0.11, hy - 0.07, 0.1), at(0.11, hy - 0.07, 0.1), (0.2, 0.36, 0.16), 0.02 * h, fine=True)
    if kind != "frog":
        ec = (0.06, 0.05, 0.07) if kind != "lamb" else (0.9, 0.9, 0.9)
        for s in (-1, 1):
            p.dot(L, at(s * 0.075, hy + 0.035, 0.12), 0.022 * h, ec, fine=True, min_px=0.7)


# ================================================================ the window, and her chicken curtains
def curtain_cloth():
    """The stuff her curtains are made of: butter yellow, one white hen after another down it, small red hearts between."""
    w, h = 44.0, 216.0
    c = Card(w, h, (0.99, 0.84, 0.42), 4.0)
    for i in range(8):
        y = 26 + i * 27.5
        flat_hen(c, 22 + (1.5 if i % 2 else -1.5), y, 20.0, (0.99, 0.98, 0.94), face=1 if i % 2 else -1, wing=(0.86, 0.84, 0.80), tail=(0.90, 0.88, 0.84), edge=(0.62, 0.40, 0.14), edge_w=0.7)
        for hx in (6.5, 37.5):
            c.disc(hx, y - 22.5, 1.9, (0.90, 0.20, 0.18))
    c.rect(0, h - 9, w, h - 5.5, (0.90, 0.20, 0.18))                                               # a red band along the hem
    return c.done(0.06, 3)


def window(L):
    """The gable window: a sash window with the night in it, a painted sill and frame, and her chicken curtains."""
    gx0, gx1, gy0, gy1 = WX0, WX1, WY0, WY1
    white = col((0.92, 0.90, 0.82))
    p.box(L, gx0 - 10, gx1 + 10, gy0 - 8, gy1 + 10, 0, 3, white, keep=0.85)                        # the casing round it
    p.quad_image(L, (gx0, gy1, 3.2), (gx1, gy1, 3.2), (gx0, gy0, 3.2), NIGHT, keep=0.95, lit=False)
    for bx, hw in ((gx0 + 2.5, 2.5), (gx1 - 2.5, 2.5), ((gx0 + gx1) / 2, 1.8)):                    # the sash: stiles
        p.face(L, [(bx - hw, gy0, 3.6), (bx + hw, gy0, 3.6), (bx + hw, gy1, 3.6), (bx - hw, gy1, 3.6)], white, (0, 0, 1), keep=0.92)
    gh = gy1 - gy0
    for by, hw in ((gy0 + 2.5, 2.5), (gy1 - 2.5, 2.5), (gy0 + gh / 2, 3.0), (gy0 + gh * 0.25, 1.3), (gy0 + gh * 0.75, 1.3)):
        p.face(L, [(gx0, by - hw, 3.6), (gx1, by - hw, 3.6), (gx1, by + hw, 3.6), (gx0, by + hw, 3.6)], white, (0, 0, 1), keep=0.92)
    p.box(L, gx0 - 13, gx1 + 13, gy0 - 9, gy0 - 5, 0, 13, white * 1.02, keep=0.88)                 # the sill, and the dark under it
    p.contact(L, [(gx0 - 12, gy0 - 20, 0.5), (gx1 + 12, gy0 - 20, 0.5), (gx1 + 12, gy0 - 9, 0.5), (gx0 - 12, gy0 - 9, 0.5)], 0.30, 2.0)
    # ---- the curtains: a rod, two straight lengths of chicken cloth, a red-checked frill across the top
    cloth, _ = curtain_cloth()
    rod_y = gy1 + 18
    p.seg(L, (gx0 - 52, rod_y, 7), (gx1 + 52, rod_y, 7), (0.52, 0.36, 0.20), 2.6, lit=(0, 0.5, 0.86), fine=False)
    for x in (gx0 - 53, gx1 + 53):
        p.ball(L, (x, rod_y, 7), 3.4, (0.52, 0.36, 0.20))
    def length(x_out, x_in, seed):
        top, bot = rod_y + 2, gy0 - 26
        w = abs(x_in - x_out)
        x0 = min(x_out, x_in)
        def stuff(X, Y, Z, t):
            a = sample(cloth, (X - x0) / w * (cloth.shape[1] - 1), (top - Y) / (top - bot) * (cloth.shape[0] - 1))
            return a * folds(X, 9.5, 0.20, seed, 1.3)[..., None]
        pts = [(x_out, top), (x_in, top), (x_in + (2 if x_in > x_out else -2), (top + bot) / 2), (x_in, bot), (x_out, bot - 1.5), (x_out - (1.5 if x_in > x_out else -1.5), (top + bot) / 2)]
        pts = [(x, y, 6.5) for x, y in pts]
        p.contact(L, [(x + 3, y - 3, 0.4) for x, y, z in pts], 0.30, 2.0)
        p.face(L, pts if x_in > x_out else pts[::-1], stuff, (0, 0, 1), keep=0.88)
    length(gx0 - 46, gx0 - 3, 1.0)
    length(gx1 + 46, gx1 + 3, 2.4)
    def frill(X, Y, Z, t):
        a = (np.floor(X / 3.6) % 2) + (np.floor(Y / 3.6) % 2)
        c_ = np.where((a == 0)[..., None], col((0.98, 0.95, 0.90)), np.where((a == 1)[..., None], col((0.94, 0.52, 0.48)), col((0.86, 0.22, 0.20))))
        return c_ * folds(X, 7.0, 0.20, 0.5, 1.2)[..., None]
    fr = [(gx0 - 48, rod_y + 3)] + [(gx0 - 48 + i * (gx1 - gx0 + 96) / 16.0, gy1 - 3 - (2.5 if i % 2 else 0)) for i in range(17)][::-1] + []
    fr = [(gx0 - 48, rod_y + 3), (gx1 + 48, rod_y + 3)] + [(gx1 + 48 - i * (gx1 - gx0 + 96) / 16.0, gy1 - 4 - (3.0 if i % 2 else 0)) for i in range(17)]
    p.contact(L, [(x + 2, y - 3, 0.5) for x, y in fr], 0.28, 1.6)
    p.face(L, [(x, y, 8.0) for x, y in fr], frill, (0, 0, 1), keep=0.88)
    p.seg(L, (gx0 - 13, gy0 - 5, 13), (gx1 + 13, gy0 - 5, 13), (0.90, 0.93, 1.0), 0.8, alpha=0.8, fine=False, keep=0.92)      # light along the sill
    # ---- on the sill: a jar with a paper flower, three pebbles, and a small china hen keeping watch
    sy = gy0 - 5
    p.box(L, 318, 324, sy, sy + 8, 6, 11, (0.70, 0.86, 0.90), keep=0.85)
    p.seg(L, (321, sy + 8, 8.5), (322, sy + 17, 8.5), (0.30, 0.56, 0.26), 0.8, fine=False)
    p.ball(L, (322, sy + 18.5, 8.5), 2.8, (0.98, 0.50, 0.62))
    for i, cc in enumerate(((0.62, 0.60, 0.58), (0.80, 0.72, 0.60), (0.46, 0.46, 0.52))):
        p.ball(L, (334 + i * 5.2, sy + 1.4, 9), 2.0 - i * 0.2, cc, sy=0.7)
    hen(p, L, (390, sy, 8), 17, "white", face=-1, keep=0.9)


# ================================================================ on the walls




PAPER = (0.97, 0.95, 0.88)
EDGE = (0.20, 0.16, 0.18)                                      # the dark crayon she outlines with


def grass(c, w, y, n=None, color=None):
    color = color or CRAYON["green"]
    c.line([(1, y), (w - 1, y + 0.4)], color, 1.6)
    for i in range(n or int(w / 3)):
        x = 1.5 + i * (w - 3) / max((n or int(w / 3)) - 1, 1)
        c.line([(x, y), (x + 0.5, y - 2.2)], color, 0.5)


def sun(c, x, y, r=4.4):
    c.disc(x, y, r, CRAYON["yellow"])
    for a in range(0, 360, 45):
        c.line([(x + math.cos(math.radians(a)) * (r + 1.2), y + math.sin(math.radians(a)) * (r + 1.2)), (x + math.cos(math.radians(a)) * (r + 4.0), y + math.sin(math.radians(a)) * (r + 4.0))], CRAYON["yellow"], 0.9)


def drawing(kind, seed=0):
    """One of Little Sister's drawings, on its sheet. Most of them are chickens. -> (color, coverage, width cm, height cm)"""
    if kind == "family":                                   # five stick people and a red car: and now a chicken, on the roof of the car
        w, h = 80.0, 54.0
        c = Card(w, h, PAPER, 5.0)
        c.line([(1, 47.5), (79, 48)], CRAYON["green"], 1.8)
        sun(c, 8, 8, 4.6)
        def person(x, hgt, color, skirt):
            hd = hgt * 0.19
            y = 47.0
            c.disc(x, y - hgt + hd, hd, color); c.disc(x, y - hgt + hd, hd - 1.0, PAPER)
            top, hip = y - hgt + 2 * hd, y - hgt * 0.36
            c.line([(x, top), (x, hip)], color, 1.25)
            c.line([(x - hgt * 0.25, top + hgt * 0.17), (x, top + hgt * 0.07), (x + hgt * 0.25, top + hgt * 0.17)], color, 1.15)
            if skirt:
                c.poly([(x, top + hgt * 0.12), (x - hgt * 0.22, hip + hgt * 0.07), (x + hgt * 0.22, hip + hgt * 0.07)], color)
            c.line([(x - hgt * 0.17, y), (x, hip), (x + hgt * 0.17, y)], color, 1.25)
        # the family, tallest to smallest: Dad, Mom, Big Sister, brother, herself
        person(8.5, 34, CRAYON["blue"], False)
        person(20.0, 31, CRAYON["purple"], True)
        person(30.5, 27, CRAYON["blue"], True)
        person(39.5, 22, CRAYON["green"], False)
        person(47.0, 17, CRAYON["pink"], True)
        # the red car, with wheels as round as she could make them
        c.poly([(53, 44), (53, 37), (57, 36.2), (60, 30), (71, 30), (73.5, 36.2), (78, 37), (78, 44)], CRAYON["red"])
        c.poly([(61, 31.4), (64.6, 31.4), (64.6, 36), (58.8, 36)], (0.82, 0.93, 1.0))
        c.poly([(66.2, 31.4), (70.2, 31.4), (72, 36), (66.2, 36)], (0.82, 0.93, 1.0))
        for wx in (59, 72.5):
            c.disc(wx, 45, 3.8, CRAYON["black"])
            c.disc(wx, 45, 1.4, (0.85, 0.85, 0.85))
        # and General Feathers, riding on the roof
        flat_hen(c, 65.5, 30.2, 15.0, (0.99, 0.99, 0.96), face=-1, edge=EDGE, edge_w=0.55, legs=False, kind="sitting")
        return c.done(0.05, seed) + (w, h)
    w, h = (42.0, 30.0) if kind in ("rainbow", "hen", "chicks", "henhouse", "run") else (30.0, 42.0) if kind in ("flower", "rooster", "heart", "tall") else (30.0, 21.0)
    ground = (0.10, 0.14, 0.36) if kind == "moon" else PAPER
    c = Card(w, h, ground, 5.0)
    if kind == "hen":
        grass(c, w, 25.6)
        sun(c, 35, 6.5, 3.6)
        flat_hen(c, 19, 25.4, 21.0, (0.99, 0.99, 0.96), face=1, edge=EDGE, edge_w=0.6)
        for i in range(7):
            c.disc(30 + (i % 4) * 2.6, 27.6 - (i // 4) * 1.4, 0.5, CRAYON["orange"])
    elif kind == "rooster":
        c.line([(14, 41), (14.4, 30)], CRAYON["brown"], 2.4); c.line([(3, 33), (27, 32.4)], CRAYON["brown"], 1.8)
        flat_hen(c, 15, 31.6, 25.0, (0.80, 0.30, 0.14), face=1, kind="rooster", wing=(0.16, 0.36, 0.34), edge=EDGE, edge_w=0.6, seed=seed)
        c.disc(24, 6.5, 4.4, CRAYON["yellow"])
        for a in (200, 240, 280, 320):
            c.line([(24 + math.cos(math.radians(a)) * 5.6, 6.5 - math.sin(math.radians(a)) * 5.6), (24 + math.cos(math.radians(a)) * 8.4, 6.5 - math.sin(math.radians(a)) * 8.4)], CRAYON["yellow"], 0.8)
    elif kind == "chicks":
        grass(c, w, 25.6)
        flat_hen(c, 31, 25.4, 18.0, (0.72, 0.42, 0.20), face=1, edge=EDGE, edge_w=0.55)
        for i, x in enumerate((6, 13, 20)):
            flat_hen(c, x, 25.6, 8.6, (0.99, 0.84, 0.18), face=1, kind="chick", wing=(0.96, 0.66, 0.10), edge=EDGE, edge_w=0.4)
    elif kind == "egg":
        egg(c, 15, 12.5, 7.4, (0.99, 0.98, 0.94))
        c.line([(8, 11), (10.6, 13.4), (13, 10.6), (15.4, 13.4), (18, 10.6), (20.4, 13.2), (22.2, 11)], EDGE, 0.55)
        c.disc(15, 5.4, 4.2, (0.99, 0.84, 0.18)); c.poly([(15.6, 9.4), (8.2, 11.2), (10.6, 13.4), (13, 10.8), (15.4, 13.4), (18, 10.8), (20.4, 13.2), (22, 11)], (0.99, 0.98, 0.94))
        c.disc(13.4, 4.6, 0.6, EDGE); c.disc(16.6, 4.6, 0.6, EDGE); c.poly([(14.2, 6.0), (15.8, 6.0), (15, 7.6)], CRAYON["orange"])
        c.ring(15, 12.5, 0.1, EDGE, 0.1)
    elif kind == "henhouse":
        grass(c, w, 26.0)
        scribble(c, 9, 12, 27, 26, CRAYON["red"], 1.0, 12, seed)
        c.poly([(7, 12.4), (18, 3.4), (29, 12.4)], CRAYON["brown"])
        c.rect(15, 17, 21, 26, (0.16, 0.12, 0.14))
        flat_hen(c, 18, 25.6, 8.0, (0.99, 0.99, 0.96), face=1, edge=EDGE, edge_w=0.4, legs=False, kind="sitting")
        c.line([(21, 26), (31, 28.4)], CRAYON["brown"], 1.6)
        flat_hen(c, 35.5, 26, 11.0, (0.99, 0.99, 0.96), face=-1, edge=EDGE, edge_w=0.45)
        sun(c, 36, 6, 3.2)
    elif kind == "heart":                                  # her favourite: a general's star on his chest
        pts = []
        for a in np.linspace(0, 6.2832, 40, endpoint=False):
            pts.append((15 + 12.4 * (math.sin(a) ** 3), 20 - 11.0 * (0.8125 * math.cos(a) - 0.3125 * math.cos(2 * a) - 0.125 * math.cos(3 * a) - 0.0625 * math.cos(4 * a))))
        c.line(pts + [pts[0]], CRAYON["red"], 1.5)
        flat_hen(c, 14.6, 30.4, 20.5, (0.99, 0.99, 0.96), face=1, edge=EDGE, edge_w=0.6)
        sx_, sy_ = 17.2, 21.2
        c.poly([(sx_ + math.cos(a) * (2.6 if i % 2 == 0 else 1.1), sy_ + math.sin(a) * (2.6 if i % 2 == 0 else 1.1)) for i, a in enumerate(np.linspace(-1.57, 4.71, 11))], CRAYON["yellow"])
        for (hx, hy) in ((5, 37), (25, 37.6), (15, 38.6)):
            c.disc(hx - 0.8, hy, 1.0, CRAYON["pink"]); c.disc(hx + 0.8, hy, 1.0, CRAYON["pink"]); c.poly([(hx - 1.7, hy + 0.4), (hx + 1.7, hy + 0.4), (hx, hy + 2.4)], CRAYON["pink"])
    elif kind == "tall":                                   # a hen in the rain, in boots like hers
        for i in range(9):
            x = 3 + i * 3.1
            c.line([(x, 3 + (i % 3) * 2.2), (x - 1.2, 7.5 + (i % 3) * 2.2)], CRAYON["sky"], 0.5)
        c.line([(2, 38.4), (28, 38.6)], CRAYON["sky"], 1.4)
        flat_hen(c, 14, 38.0, 24.0, (0.99, 0.84, 0.30), face=-1, edge=EDGE, edge_w=0.6, boots=CRAYON["red"])
    elif kind == "eggs":
        for i, name in enumerate(("pink", "sky", "yellow", "green", "purple")):
            egg(c, 4.6 + i * 5.2, 11, 2.3, CRAYON[name], stripe=(0.99, 0.98, 0.94) if i % 2 == 0 else None, dots=(0.99, 0.98, 0.94) if i % 2 else None)
        c.line([(2, 16.6), (28, 16.8)], CRAYON["brown"], 1.0)
    elif kind == "moon":                                   # a hen on the moon (why not)
        r = np.random.default_rng(seed)
        for _ in range(9):
            sx, sy, sr = 2.5 + r.random() * 25, 2.5 + r.random() * 9, 0.8 + r.random() * 0.8
            c.poly([(sx + math.cos(a) * (sr if i % 2 == 0 else sr * 0.45), sy + math.sin(a) * (sr if i % 2 == 0 else sr * 0.45)) for i, a in enumerate(np.linspace(-1.57, 4.71, 11))], CRAYON["yellow"])
        c.disc(15, 15.4, 5.6, (0.98, 0.95, 0.72)); c.disc(16.8, 13.4, 5.2, ground)
        flat_hen(c, 11.4, 12.2, 8.6, (0.99, 0.99, 0.96), face=1, legs=False, kind="sitting")
    elif kind == "rainbow":
        for i, name in enumerate(("red", "orange", "yellow", "green", "blue", "purple")):
            r_ = 17.0 - i * 2.1
            pts = [(21 + math.cos(a) * r_, 25 - math.sin(a) * r_) for a in np.linspace(0.05, 3.09, 26)]
            c.line(pts, CRAYON[name], 2.0)
        flat_hen(c, 21, 27.4, 11.0, (0.99, 0.99, 0.96), face=1, edge=EDGE, edge_w=0.45)
    elif kind == "run":                                    # three hens running after a worm
        grass(c, w, 25.6)
        for i, (x, cc) in enumerate(((8, (0.99, 0.99, 0.96)), (19, (0.20, 0.19, 0.24)), (30, (0.80, 0.50, 0.22)))):
            flat_hen(c, x, 25.4 - (i % 2) * 1.2, 12.0, cc, face=1, edge=EDGE, edge_w=0.45)
        c.line([(37, 25), (38.4, 23.6), (39.6, 25), (40.6, 23.8)], CRAYON["pink"], 0.8)
    elif kind == "flower":
        c.line([(15, 40), (15.5, 20)], CRAYON["green"], 1.1)
        c.poly([(15.2, 30), (22, 25.4), (21, 31)], CRAYON["green"]); c.poly([(15.2, 33), (8, 28.4), (9.4, 34)], CRAYON["green"])
        for a in range(0, 360, 45):
            c.disc(15.5 + math.cos(math.radians(a)) * 6.2, 14 + math.sin(math.radians(a)) * 6.2, 3.6, CRAYON["pink"] if a % 90 == 0 else CRAYON["purple"])
        c.disc(15.5, 14, 3.4, CRAYON["yellow"])
    elif kind == "hands":
        for (hx, hy, name) in ((9, 8, "pink"), (21, 13, "yellow")):
            c.disc(hx, hy + 2, 3.4, CRAYON[name], 3.8)
            for a in (-70, -35, 0, 32, 80):
                c.line([(hx, hy + 1), (hx + math.sin(math.radians(a)) * 6.0, hy + 1 - math.cos(math.radians(a)) * 6.0)], CRAYON[name], 1.3)
    else:                                                  # "scribble": something only she can explain
        r = np.random.default_rng(seed)
        for name in ("purple", "pink", "sky"):
            pts = [(4 + r.random() * 22, 3 + r.random() * 15) for _ in range(9)]
            c.line(pts, CRAYON[name], 0.9)
    return c.done(0.05, seed) + (w, h)


def chart_card():
    """THE CHICKEN CHART: every kind she knows (and two she made up), a row at a time, each with its name under it.
    The names are too small to read from here, and in her writing."""
    x0, x1, y0, y1 = M.CHART
    w, h = x1 - x0, y1 - y0
    c = Card(w, h, (0.98, 0.95, 0.84), 6.0)
    c.rect(0, 0, w, 1.2, (0.90, 0.84, 0.66)); c.rect(0, h - 1.2, w, h, (0.90, 0.84, 0.66))
    top = 19.0                                                 # the title goes above this (set pixel by pixel afterwards)
    c.line([(6, top - 2.2), (w - 6, top - 1.8)], CRAYON["red"], 0.9)
    rows, cols = 3, 4
    cw, ch = (w - 8) / cols, (h - top - 3) / rows
    birds = [dict(body=(0.99, 0.99, 0.96)), dict(body=(0.66, 0.38, 0.18)), dict(body=(0.17, 0.16, 0.21), specks=(0.96, 0.96, 0.92)), dict(body=(0.99, 0.84, 0.18), kind="chick", wing=(0.96, 0.66, 0.10), s=0.62),
             dict(body=(0.82, 0.28, 0.12), kind="rooster", wing=(0.14, 0.36, 0.34)), dict(body=(0.64, 0.68, 0.80), crest=True), dict(body=(0.94, 0.64, 0.26), kind="sitting"), dict(body=(0.96, 0.96, 0.94), specks=(0.16, 0.15, 0.20)),
             dict(body=(0.74, 0.24, 0.16), s=0.66), dict(body=(0.99, 0.99, 0.96), boots=CRAYON["pink"], s=1.06), dict(body=(0.62, 0.36, 0.76), wing=(0.94, 0.52, 0.72), comb=CRAYON["orange"]), dict(body=(0.99, 0.99, 0.96), star=True)]
    r = np.random.default_rng(21)
    for j in range(rows):
        for i in range(cols):
            b = dict(birds[j * cols + i])
            cx, base = 4 + cw * (i + 0.5), top + ch * (j + 1) - 9.0
            s_ = 19.5 * b.pop("s", 1.0)
            star = b.pop("star", False)
            kind = b.pop("kind", "hen")
            if kind == "sitting":                              # on her eggs, in straw
                for k_ in range(9):
                    c.line([(cx - 9 + k_ * 2.2, base + 0.6), (cx - 10.6 + k_ * 2.4 + r.normal(0, 0.8), base - 3.0)], CRAYON["yellow"], 0.7)
                for ex in (-6.5, 6.8):
                    egg(c, cx + ex, base - 1.2, 1.7, (0.99, 0.98, 0.94))
            if star:                                           # the last one is the General: a star, and a heart beside him
                c.line([(cx - 13, base + 1.0), (cx + 13, base + 1.2)], CRAYON["red"], 0.8)
            flat_hen(c, cx - 1.5, base, s_, face=1 if (i + j) % 3 else -1, kind=kind, edge=EDGE, edge_w=0.55, seed=i + j * 4, **b)
            if star:
                sx_, sy_ = cx - 1.5 + (1 if (i + j) % 3 else -1) * 2.8, base - s_ * 0.5
                c.poly([(sx_ + math.cos(a) * (2.4 if n % 2 == 0 else 1.0), sy_ + math.sin(a) * (2.4 if n % 2 == 0 else 1.0)) for n, a in enumerate(np.linspace(-1.57, 4.71, 11))], CRAYON["yellow"])
                hx, hy = cx + 10.4, base - 15.5
                c.disc(hx - 1.4, hy, 1.8, CRAYON["red"]); c.disc(hx + 1.4, hy, 1.8, CRAYON["red"]); c.poly([(hx - 3.0, hy + 0.7), (hx + 3.0, hy + 0.7), (hx, hy + 4.2)], CRAYON["red"])
            # its name, in her writing
            ink = (CRAYON["blue"], CRAYON["purple"], CRAYON["green"], CRAYON["brown"])[(i + j) % 4]
            lw = 9 + r.random() * 9
            pts = [(cx - lw / 2 + k_ * lw / 8.0, base + 4.4 + (0.9 if k_ % 2 else -0.6) + r.normal(0, 0.2)) for k_ in range(9)]
            c.line(pts, ink, 0.75)
    for i in range(1, cols):                                   # ruled, more or less
        c.line([(4 + cw * i, top + 1), (4 + cw * i + 0.6, h - 4)], (0.70, 0.74, 0.86), 0.4)
    for j in range(1, rows):
        c.line([(5, top + ch * j), (w - 5, top + ch * j + 0.5)], (0.70, 0.74, 0.86), 0.4)
    return c.done(0.04, 3)


def quilt_card(cols, rows, sq=33.0, seed=1, bind=3.0):
    """The quilt of hens: a hen to every square, turned this way and that; red binding round the edge."""
    w, h = cols * sq + 2 * bind, rows * sq + 2 * bind
    c = Card(w, h, (0.86, 0.20, 0.18), 4.0)
    grounds = [(0.99, 0.90, 0.56), (0.60, 0.80, 0.94), (0.98, 0.70, 0.74), (0.66, 0.88, 0.70), (0.97, 0.94, 0.86), (0.82, 0.72, 0.94)]
    hens = [(0.99, 0.99, 0.95), (0.99, 0.99, 0.95), (0.99, 0.99, 0.95), (0.99, 0.99, 0.95), (0.80, 0.28, 0.16), (0.99, 0.99, 0.95)]
    for j in range(rows):
        for i in range(cols):
            k = (i * 2 + j * 3 + seed) % len(grounds)
            x0, y0 = bind + i * sq, bind + j * sq
            c.rect(x0, y0, x0 + sq, y0 + sq, (0.97, 0.94, 0.86))                                   # the sashing between squares
            c.rect(x0 + 1.6, y0 + 1.6, x0 + sq - 1.6, y0 + sq - 1.6, grounds[k])
            flat_hen(c, x0 + sq / 2 + (1.5 if (i + j) % 2 else -1.5), y0 + sq - 5.0, 23.0, hens[k], face=1 if (i + j) % 2 else -1,
                     wing=mix(hens[k], grounds[k], 0.45), tail=mix(hens[k], (0.5, 0.4, 0.4), 0.25), edge=mix(grounds[k], (0.2, 0.1, 0.1), 0.55), edge_w=0.7)
    return c.done(0.06, seed)


DRAWN = [  # kind, middle X, middle Y, turn (degrees), seed     -- on the gable, left of the window
    ("heart", 118, 177, 4.0, 6), ("moon", 138, 211, -5.0, 7),
    ("rooster", 174, 227, 3.0, 2), ("chicks", 223, 224, -3.0, 3), ("family", 204, 166, -2.5, 1),
]
UNDER = [("hen", 334, 58, 3.0, 11), ("tall", 393, 60, -4.0, 12), ("henhouse", 110, 132, -3.0, 4), ("run", 466, 48, -3.0, 15), ("eggs", 528, 44, 5.0, 16)]    # two more, under the window sill
BIG = 1.2                                                      # she draws on big paper


def wall_things(L):
    # ---- her drawings: the gable to the left of the window, as high as she can reach from the top of the flock
    for kind, cx, cy, deg, seed in DRAWN + UNDER:
        tex, al, w, h = drawing(kind, seed)
        w, h = w * BIG, h * BIG
        p.contact(L, [(cx - w / 2 + 1.5, cy - h / 2 - 2.0, 0.4), (cx + w / 2 + 1.5, cy - h / 2 - 2.0, 0.4), (cx + w / 2 + 1.5, cy + h / 2 - 2.0, 0.4), (cx - w / 2 + 1.5, cy + h / 2 - 2.0, 0.4)], 0.22, 1.2)
        on_gable(L, tex, al, cx, cy, w, h, deg, keep=0.93)
        taped(L, cx, cy, w, h, deg)
    # crayon on the wall itself, low down (nobody has owned up)
    for i, name in enumerate(("pink", "sky", "purple")):
        r = np.random.default_rng(60 + i)
        pts = [(268 + i * 6 + r.normal(0, 4), 30 + r.random() * 26, 0.4) for _ in range(6)]
        p.path(L, pts, mix(CRAYON[name], MINT, 0.35), 0.8, 0.7, alpha=0.7, fine=False, lit=(0, 0, 1))
    # ---- and more on her knee wall, and where the roof comes down to it
    for kind, zc, yc, deg, seed in (("run", 150, 86, 3, 11), ("flower", 198, 96, -6, 12), ("scribble", 236, 104, 4, 13), ("rainbow", 262, 84, -3, 14)):
        tex, al, w, h = drawing(kind, seed)
        tl, tr, bl = rot2(zc, yc, w, h, deg)
        p.quad_image(L, (0.6, tl[1], tl[0]), (0.6, tr[1], tr[0]), (0.6, bl[1], bl[0]), tex, al, keep=0.9)
    for kind, zc, sc, seed in (("hen", 96, 34, 21), ("eggs", 150, 30, 22), ("moon", 205, 26, 23), ("hands", 252, 30, 24), ("chicks", 316, 30, 25)):
        tex, al, w, h = drawing(kind, seed)
        def up(z, s_):                                       # a place on the left slope: z along the room, s_ up the slope from the knee wall
            return (s_ * (WD / 2) / SLOPE_LEN + NL[0] * 0.6, KNEE + s_ * (RIDGE - KNEE) / SLOPE_LEN + NL[1] * 0.6, z)
        p.quad_image(L, up(zc - w / 2, sc + h / 2), up(zc + w / 2, sc + h / 2), up(zc - w / 2, sc - h / 2), tex, al, keep=0.9)
    # ---- THE CHICKEN CHART, to the right of the window
    tx0, tx1, ty0, ty1 = M.CHART
    tex, al = chart_card()
    p.contact(L, [(tx0 + 2, ty0 - 3, 0.4), (tx1 + 2, ty0 - 3, 0.4), (tx1 + 2, ty1 - 3, 0.4), (tx0 + 2, ty1 - 3, 0.4)], 0.28, 1.5)
    p.quad_image(L, (tx0, ty1, 0.6), (tx1, ty1, 0.6), (tx0, ty0, 0.6), tex, al, keep=0.95)
    for (u, vv) in ((tx0, ty1), (tx1, ty1), (tx0, ty0), (tx1, ty0)):
        p.poly3(L, [(u - 3.4, vv + 1.6, 0.8), (u + 3.4, vv + 2.4, 0.8), (u + 3.6, vv - 1.4, 0.8), (u - 3.2, vv - 2.2, 0.8)], (0.94, 0.90, 0.74), 0.9, fine=False, lit=(0, 0, 1), keep=0.85)
    (xa, ya), (xb, yb) = p.pt((tx0, ty1, 0.6)), p.pt((tx1, ty1, 0.6))
    title = "MY CHICKENS"
    inks = [tone_inv(c_) for c_ in ((0.74, 0.10, 0.10), (0.12, 0.22, 0.66), (0.10, 0.42, 0.18), (0.44, 0.16, 0.56), (0.76, 0.34, 0.04))]
    tiny_word(L, title, (xa + xb) / 2 - tiny_width(title) / 2.0, (ya + yb) / 2 + 2.6, inks)
    SIGNS["chart"] = [round((xa + xb) / 2 - tiny_width(title) / 2.0), round((ya + yb) / 2 + 2.6), round((xa + xb) / 2 + tiny_width(title) / 2.0), round((ya + yb) / 2 + 9.6)]
    # ---- her small coat on its peg, and her boots under it
    p.box(L, 584, 616, 109, 115, 0, 2, WHITE, keep=0.88)
    for x in (590, 600, 610):
        p.box(L, x - 1, x + 1, 110.5, 113.5, 2, 6, WOOD, keep=0.88)
    yellow = col((1.0, 0.80, 0.14))
    def raincoat(X, Y, Z, t):
        return yellow * folds(X + (110 - Y) * 0.12, 8.5, 0.16, 1.0, 1.2)[..., None] * (1 - 0.5 * (np.abs(X - 600) < 0.5))[..., None]
    body = [(592, 110), (608, 110), (612, 96), (616, 59), (584, 59), (588, 96)]
    p.contact(L, [(x + 3, y - 3, 0.4) for x, y in body], 0.32, 2.0)
    p.face(L, [(x, y, 4.5) for x, y in body], raincoat, (0, 0, 1), keep=0.9)
    p.face(L, [(592, 108, 5), (586, 82, 5), (580.5, 84, 5), (588, 110, 5)][::-1], yellow * 0.9, (0, 0, 1), keep=0.9)
    p.face(L, [(608, 108, 5), (614, 82, 5), (619.5, 84, 5), (612, 110, 5)], yellow * 0.9, (0, 0, 1), keep=0.9)
    p.ball(L, (600, 108.5, 6), 7.2, yellow, sy=0.85, flat=0.3, keep=0.9)                             # its hood
    for yy in (98, 88, 78):
        p.dot(L, (601.5, yy, 5.2), 0.9, (0.30, 0.34, 0.60), fine=False, min_px=0.7)
    p.ball(L, (613.5, 106.5, 6.5), 6.4, (0.97, 0.96, 0.92), sy=0.9, keep=0.9)                       # and her hat: knitted, white, with a comb
    for dx in (-2.4, 0, 2.4):
        p.ball(L, (613.5 + dx, 113.4 - abs(dx) * 0.3, 6.5), 1.6, RED, keep=0.9)
    p.poly3(L, [(608.0, 106.5, 9), (608.0, 104.0, 9), (604.6, 105.0, 9)], BEAK, fine=False, lit=(0, 0, 1), keep=0.9)
    red = col((0.88, 0.18, 0.16))
    p.contact(L, [(584, 0, 4), (616, 0, 4), (618, 0, 30), (586, 0, 30)], 0.35, 3.0)
    for bx in (588, 603):                                                                           # two rubber boots, one fallen in a little
        p.box(L, bx, bx + 8, 0, 19, 8, 16, red, keep=0.9)
        p.ball(L, (bx + 4, 3.6, 20), 5.0, red, sx=0.86, sy=0.72, keep=0.9)
        p.box(L, bx - 0.4, bx + 8.4, 16, 19, 7.6, 16.4, (0.98, 0.94, 0.84), keep=0.9)


def egg_light(L):
    """The night-light: an egg that glows, standing on the floor by the flock."""
    x, y, z = EGG
    p.contact(L, [(x - 12, 0, z - 8), (x + 12, 0, z - 8), (x + 12, 0, z + 12), (x - 12, 0, z + 12)], 0.2, 2.5)
    p.ball(L, (x, 2.0, z), 9.0, (0.92, 0.90, 0.84), sy=0.36, keep=0.9)                               # its foot
    P = (x, 17.5, z)
    k = p.k(P)
    cx, cy = p.pt(P)
    p.glow(L, P, 30 * k, (1.0, 0.64, 0.34), 0.60)
    def shell_(rx, ry):
        return [(cx + math.cos(a) * rx * (1.0 - 0.17 * (-math.sin(a))), cy + math.sin(a) * ry) for a in np.linspace(0, 6.2832, 30, endpoint=False)]
    p.poly2(L, shell_(10.4 * k + 0.7, 14.2 * k + 0.7), tone_inv((0.86, 0.50, 0.22)), fine=False, keep=0.92)
    p.poly2(L, shell_(10.2 * k, 14.0 * k), tone_inv((0.985, 0.88, 0.56)), fine=False, keep=0.92)
    p.dot2(L, cx - 0.8 * k, cy + 1.4 * k, 6.8 * k, 9.6 * k, tone_inv((0.985, 0.96, 0.78)), fine=False, keep=0.92)
    p.glow(L, P, 12 * k, (1.0, 0.86, 0.60), 0.35)


# ================================================================ the flock: a mountain of stuffed animals, the chickens on top
def flock(L):
    X0, X1, Y0, Y1, Z0, Z1 = M.FLOCK
    p.contact(L, [(X0 - 6, 0, Z0 - 4), (X1 + 8, 0, Z0 - 4), (X1 + 14, 0, Z1 + 18), (X0 - 4, 0, Z1 + 18)], 0.52, 6.0)
    p.contact(L, [(X0 - 4, 0, 0.5), (X1 + 4, 0, 0.5), (X1 - 26, 100, 0.5), (X0 + 36, 104, 0.5)], 0.40, 6.0)
    # what it is all heaped on: her beanbag, and a cushion or two
    lilac = (0.64, 0.46, 0.76)
    def seams(u, vv, a):
        dots = (np.hypot(np.mod(u * 5.0 + (np.floor(vv * 5.0) % 2) * 0.5, 1.0) - 0.5, np.mod(vv * 5.0, 1.0) - 0.5) < 0.17)
        a = np.where(dots[..., None], col((0.90, 0.82, 0.96)), a)
        return a * (1 - 0.18 * (np.abs(np.mod(u * 2.2 + 0.5, 1.0) - 0.5) < 0.035))[..., None]
    p.ball(L, (170, 31, 34), 51, lilac, sx=1.30, sy=0.74, flat=0.08, spots=seams, keep=0.82)
    p.ball(L, (112, 13, 70), 27, (0.98, 0.80, 0.36), sx=1.15, sy=0.5, flat=0.1, keep=0.82)
    p.ball(L, (236, 11, 82), 24, (0.96, 0.52, 0.62), sx=1.2, sy=0.48, flat=0.1, keep=0.82)
    tan, rose, choc = (0.80, 0.62, 0.42), (0.97, 0.66, 0.74), (0.42, 0.26, 0.16)
    pile = [  # what ("a" an animal, "h" a chicken), kind, X, Y, Z, height, way it faces (chickens) or fur (animals)
        ("a", "giraffe", 250, 0, 26, 86, None), ("a", "elephant", 92, 0, 52, 46, None),
        ("h", "white", 124, 57, 44, 34, -1), ("h", "rooster", 171, 66, 40, 50, 1), ("h", "white", 218, 55, 46, 32, 1),
        ("a", "bear", 146, 0, 76, 46, None), ("a", "rabbit", 196, 0, 80, 46, rose), ("a", "pig", 252, 0, 70, 34, None),
        ("a", "frog", 120, 22, 78, 26, None), ("a", "bear", 224, 0, 96, 30, tan), ("a", "bear", 162, 34, 62, 30, choc), ("a", "pig", 200, 40, 58, 26, None),
        ("h", "buff", 172, 0, 106, 30, 1), ("h", "chick", 222, 28, 97, 16, 1),
        ("h", "white", 138, 0, 112, 28, -1),
        ("h", "speckled", 244, 0, 118, 34, -1), ("h", "chick", 272, 0, 116, 22, -1),
    ]
    pile.sort(key=lambda t: (t[4], t[3]))
    for what, kind, X, Y, Z, h, how in pile:
        if what == "a":
            animal(L, kind, (X, Y, Z), h, keep=0.82, fur_=how)
        else:
            hen(p, L, (X, Y, Z), h, kind, face=how, keep=0.88, seed=X * 0.1, gain=1.5 if kind == "chick" else 1.0)
    # she feeds them: a dish of corn, a dish of water
    for (x, z, cc, corn) in ((282, 96, (0.86, 0.30, 0.30), True), (298, 84, (0.36, 0.56, 0.86), False)):
        p.contact(L, [(x - 9, 0, z - 5), (x + 9, 0, z - 5), (x + 9, 0, z + 6), (x - 9, 0, z + 6)], 0.28, 1.6)
        cone2(L, (x, 0, z), (x, 4.5, z), 6.0, 7.5, p.shade_at(cc, (x, 2, z + 4), (0, 0.3, 0.95), 1.1), rim=p.shade_at((1.0, 0.84, 0.20) if corn else (0.70, 0.86, 0.98), (x, 4.5, z), (0, 1, 0), 1.2), keep=0.9)


# ================================================================ her bed: the quilt of hens, the heap, and one place kept free
def bed(L):
    X0, X1, Y0, Y1, Z0, Z1 = M.BED
    yel = col((1.0, 0.80, 0.30))
    mid = (X0 + X1) / 2
    p.contact(L, [(X0 - 12, 0, Z0 - 4), (X1, 0, Z0 - 4), (X1, 0, Z1 + 16), (X0 - 12, 0, Z1 + 16)], 0.5, 5.0)
    def head(X, Y, Z, t):                                       # painted boards; a small heart cut out toward each side
        hole = np.zeros(X.shape, bool)
        for hx in (mid - 35, mid + 35):
            u, vv = (X - hx) / 6.5, (Y - 93) / 6.5
            hole |= ((u * u + vv * vv - 1) ** 3 - u * u * vv ** 3) < 0
        return np.where(hole[..., None], col((0.30, 0.22, 0.30)), yel * (1 - 0.25 * lines(X, 16.6, 0.8, footprint(X)))[..., None])
    p.box(L, X0, X1, 0, 104, Z0, Z0 + 4, {"all": yel, "front": head}, keep=0.88)
    for x in (X0 - 1, X1 - 4):
        p.box(L, x, x + 5, 0, 110, Z0 - 0.5, Z0 + 4.5, yel * 1.03, keep=0.88)
        p.ball(L, (x + 2.5, 112.5, Z0 + 2), 3.6, yel, keep=0.88)
    p.box(L, X0 + 2, X1 - 2, 0, 14, Z0 + 6, Z1 - 3, (0.07, 0.06, 0.10), keep=0.8)                  # the dark under it
    for x in (X0, X1 - 5):
        p.box(L, x, x + 5, 0, 14, Z1 - 5, Z1, yel * 0.9, keep=0.88)
    p.box(L, X0, X1, 14, 28, Z0 + 4, Z1, yel * 0.97, keep=0.88)                                    # the rail
    p.box(L, X0 + 1, X1 - 1, 28, Y1, Z0 + 4, Z1 - 1, (0.96, 0.95, 0.90), keep=0.86)                # mattress and sheet
    # ---- the quilt of hens: over the top, down the side toward the room, and down the foot (which faces us)
    top, _ = quilt_card(3, 4, seed=1)
    p.quad_image(L, (X0 - 2, Y1 + 0.8, 256), (X1 + 2, Y1 + 0.8, 256), (X0 - 2, Y1 + 0.8, Z1 + 2), top, None, keep=0.9, shadow=True)
    side, _ = quilt_card(4, 1, seed=3)
    p.quad_image(L, (X0 - 2.2, Y1 + 1, 256), (X0 - 2.2, Y1 + 1, Z1 + 2), (X0 - 2.2, 8, 256), side, None, keep=0.9)
    foot, _ = quilt_card(3, 1, seed=2)
    p.quad_image(L, (X0 - 2, Y1 + 1, Z1 + 2.2), (X1 + 2, Y1 + 1, Z1 + 2.2), (X0 - 2, 8, Z1 + 2.2), foot, None, keep=0.94)
    for xf in (X0 + 30, X0 + 68):                                                                   # two soft folds down the foot
        p.shade2(L, [p.pt((xf - 1.5, Y1, Z1 + 2.4)), p.pt((xf + 1.5, Y1, Z1 + 2.4)), p.pt((xf + 3.0, 9, Z1 + 2.4)), p.pt((xf - 2.0, 9, Z1 + 2.4))], 0.16, 1.0)
    p.box(L, X0 - 1, X1 + 1, Y1 + 0.6, Y1 + 2.4, 247, 258, (0.97, 0.96, 0.92), keep=0.88)          # the sheet turned down over it
    # ---- the pillow, propped against the headboard, and on it the one round place that is kept free
    ang = math.radians(40)
    sa, ca = math.sin(ang), math.cos(ang)
    def on_pillow(x, s_, lift=0.0):                             # s_ = how far up the pillow from its lower edge (cm)
        return (x, Y1 + 2.0 + s_ * sa + lift * ca, 247 - s_ * ca + lift * sa)
    x_l, x_r, plen = X0 + 7, X1 - 7, 52.0
    dc, drx, drs = 27.0, 28.0, 19.0                             # the free place: its middle (up the pillow), half-width, half-height
    case = col((0.98, 0.58, 0.70))                                # her pillowcase: pink, white spots, a white frill
    def pface(X, Y, Z, t):
        s_ = (Y - (Y1 + 2.0)) / sa
        u, w_ = (X - mid) / drx, (s_ - dc) / drs
        d = u * u + w_ * w_
        rd = np.sqrt(d)
        inside = smooth((1.0 - d) / 0.16)
        sh = inside * (0.24 + 0.46 * np.clip(0.5 - u * 0.7 + w_ * 0.25, 0, 1))                      # the hollow: its left side falls away from the lamp
        crease = np.exp(-((rd - 0.93) / 0.085) ** 2) * np.clip(0.25 - u * 0.9 + w_ * 0.3, 0, 1) * 0.42     # the shadow under its left lip
        rim = np.exp(-((rd - 1.06) / 0.10) ** 2) * np.clip(0.15 + u * 0.8 - w_ * 0.3, 0, 1) * 0.30         # the light along its right lip
        rim = rim + np.exp(-((rd - 0.88) / 0.10) ** 2) * np.clip(u * 0.9 - 0.2, 0, 1) * 0.20               # and on the side of the dent that faces the lamp
        edge = np.minimum(np.minimum(X - x_l, x_r - X), np.minimum(s_, plen - s_))
        puff = 1 - 0.18 * np.clip(1 - edge / 8.0, 0, 1) ** 2
        dx_, ds_ = np.mod(X + 3.5, 7.0) - 3.5, np.mod(s_ + (np.floor(X / 7.0) % 2) * 3.5, 7.0) - 3.5
        spot = np.clip((1.15 - np.hypot(dx_, ds_)) / np.maximum(footprint(X), 0.3) + 0.5, 0, 1) * (1 - inside)
        c = lerp(case, col((0.99, 0.96, 0.95)), spot[..., None])
        c = np.where((edge < 2.6)[..., None], col((0.98, 0.97, 0.95)), c)
        c = c * puff[..., None] * (1 + rim)[..., None]
        return c * (1 - sh[..., None] * (1 - col((0.56, 0.34, 0.58)))) * (1 - crease)[..., None]
    p.ball(L, (mid, Y1 + 5.5, 247), 43, case * 0.96, sy=0.14, flat=0.2, keep=0.86)                  # its lower edge, plump on the sheet
    p.contact(L, [on_pillow(x_l - 2, -2, -1), on_pillow(x_r + 2, -2, -1), (x_r + 2, Y1 + 1.2, 262), (x_l - 2, Y1 + 1.2, 262)], 0.22, 2.0)
    p.face(L, [on_pillow(x_l, 0), on_pillow(x_r, 0), on_pillow(x_r, plen), on_pillow(x_l, plen)], pface, keep=0.9, gain=0.74)
    for (a_, b_) in ((on_pillow(x_l, 0), on_pillow(x_l, plen)), (on_pillow(x_r, 0), on_pillow(x_r, plen)), (on_pillow(x_l, plen), on_pillow(x_r, plen))):
        p.seg(L, a_, b_, (0.97, 0.96, 0.94), 3.0, fine=False, lit=(0, 0.6, 0.8), keep=0.88)         # its frilled edges
    # the sign, propped at the back of that place (so that the whole round of it can be seen, empty, before the sign)
    sx0, sx1 = mid - 27.5, mid + 27.5
    cs = dc + 13.0
    b0, b1 = on_pillow(sx0, cs, 0.6), on_pillow(sx1, cs, 0.6)
    card = [b0, b1, (sx1, b1[1] + 15.2, b1[2] - 3.0), (sx0, b0[1] + 15.2, b0[2] - 3.0)]
    p.contact(L, [on_pillow(sx0 + 1, cs, 0.3), on_pillow(sx1 + 1.5, cs, 0.3), on_pillow(sx1 + 3, cs - 6, 0.3), on_pillow(sx0 + 2.5, cs - 6, 0.3)], 0.30, 1.3, color=(0.50, 0.50, 0.66))
    edge_c = tone_inv((0.58, 0.44, 0.58))
    (xa, ya), (xb, yb), (xc, yc) = p.pt(card[3]), p.pt(card[2]), p.pt(card[0])
    p.poly2(L, [(xa - 1.0, ya - 1.0), (xb + 1.0, yb - 1.0), (xb + 1.0, yc + (yb - ya) + 1.2), (xa - 1.0, yc + 1.2)], edge_c, fine=False, keep=0.96)
    p.face(L, card, (0.99, 0.98, 0.95), keep=0.96, gain=1.15)
    word = "RESERVED"
    p.line2(L, [(xa, yc + 0.3), (xb, yc + 0.3 + (yb - ya))], tone_inv((0.60, 0.58, 0.66)), 0.9, fine=True)        # the card's lower edge
    tiny_word(L, word, (xa + xb) / 2 - tiny_width(word) / 2.0, (ya + yb) / 2 + ((yc - ya) - 7) / 2.0, tone_inv((0.50, 0.08, 0.36)))
    SIGNS["reserved"] = [round(xa), round(ya), round(xb - xa), round(yc - ya)]
    # the little ones that are allowed on the pillow keep to its two ends
    hen(p, L, on_pillow(X0 + 13, 15, 1.0), 14, "chick", face=1, keep=0.88)
    animal(L, "rabbit", on_pillow(X1 - 13, 14, 1.0), 18, keep=0.86, fur_=(0.80, 0.62, 0.42))
    # ---- the heap: low by the pillow (so that the free place can be seen), high toward the foot
    heap = [  # what, kind, X, Z, height, facing / fur
        ("h", "chick", 632, 277, 13, 1), ("a", "frog", 680, 278, 13, None),
        ("a", "pig", 622, 301, 19, None), ("h", "white", 653, 302, 21, -1), ("a", "rabbit", 686, 301, 20, (0.97, 0.66, 0.74)),
        ("h", "brown", 628, 331, 28, 1), ("a", "elephant", 661, 332, 29, None), ("h", "speckled", 693, 331, 28, -1),
        ("h", "chick", 616, 366, 14, 1), ("a", "bear", 641, 366, 40, None), ("h", "grey", 675, 368, 31, 1), ("a", "bear", 701, 364, 24, (0.80, 0.62, 0.42)),
    ]
    for what, kind, X, Z, h, how in heap:
        if what == "a":
            animal(L, kind, (X, Y1 + 1.5, Z), h, keep=0.84, fur_=how)
        else:
            hen(p, L, (X, Y1 + 1.5, Z), h, kind, face=how, keep=0.88, seed=X * 0.1)
    # her slippers on the floor beside it, where she stepped out of them
    for i, (dx, dz, rot_) in enumerate(((-9, 352, 0.5), (-20, 366, -0.6))):      # they are chickens too
        P_ = (X0 + dx, 3.6, dz)
        p.contact(L, [(P_[0] - 7, 0, dz - 4), (P_[0] + 7, 0, dz - 4), (P_[0] + 7, 0, dz + 5), (P_[0] - 7, 0, dz + 5)], 0.3, 1.5)
        p.ball(L, P_, 5.6, (1.0, 0.86, 0.30), sx=1.15, sy=0.68, rot=rot_, keep=0.88)
        p.ball(L, (P_[0] - 3.5, 7.4, dz + 1), 1.5, RED, keep=0.88)
        p.poly3(L, [(P_[0] - 7.5, 5.0, dz + 2), (P_[0] - 7.5, 3.2, dz + 2), (P_[0] - 10.5, 4.0, dz + 2)], BEAK, fine=False, lit=p.B, keep=0.88)
        p.dot(L, (P_[0] - 5.4, 5.6, dz + 2.5), 0.55, (0.06, 0.05, 0.07), fine=False, min_px=0.6)
    # ---- over the bed, on the knee wall: a shelf of small treasures, and a rosette (first prize, for a hen)
    wx = WD - 0.8
    p.box(L, WD - 12, WD, 97, 99.5, 252, 352, WHITE, keep=0.88)
    p.contact(L, [(wx, 97, 250), (wx, 97, 354), (wx, 88, 354), (wx, 88, 250)], 0.3, 2.0)
    items = [("hen", "white", 262, 12), ("cup", (0.98, 0.52, 0.70), 278, 0), ("hen", "brown", 293, 11), ("cup", (0.50, 0.78, 0.96), 308, 0), ("hen", "chick", 321, 9), ("cup", (0.62, 0.88, 0.60), 334, 0), ("hen", "black", 345, 11)]
    for what, kd, z, h in items:
        if what == "hen":
            hen(p, L, (WD - 6.5, 99.5, z), h, kd, face=-1, keep=0.9, outline=0.6)
        else:
            cone2(L, (WD - 6.5, 99.5, z), (WD - 6.5, 103.5, z), 1.8, 2.6, p.shade_at((0.95, 0.94, 0.90), (WD - 7, 101, z), (-1, 0.2, 0.2)), keep=0.9)
            p.ball(L, (WD - 6.5, 106.0, z), 2.7, kd, sy=1.25, keep=0.9, gain=1.1)
    rz, ry = 226, 108                                           # the rosette
    for a in np.linspace(0, 6.2832, 10, endpoint=False):
        p.poly3(L, [(wx, ry, rz), (wx, ry + math.sin(a - 0.36) * 7.5, rz + math.cos(a - 0.36) * 7.5), (wx, ry + math.sin(a + 0.36) * 7.5, rz + math.cos(a + 0.36) * 7.5)], (0.20, 0.36, 0.78), fine=False, lit=(-1, 0, 0), keep=0.9)
    p.poly3(L, [(wx, ry - 4, rz - 3), (wx, ry - 19, rz - 5), (wx, ry - 17, rz - 1.5), (wx, ry - 4, rz)], (0.20, 0.36, 0.78), fine=False, lit=(-1, 0, 0), keep=0.9)
    p.poly3(L, [(wx, ry - 4, rz + 3), (wx, ry - 19, rz + 5), (wx, ry - 17, rz + 1.5), (wx, ry - 4, rz)], (0.16, 0.30, 0.68), fine=False, lit=(-1, 0, 0), keep=0.9)
    p.dot(L, (wx - 0.2, ry, rz), 3.6, (0.98, 0.84, 0.30), fine=False, lit=(-1, 0, 0), keep=0.9)




def lamp_table(L):
    """Her bedside table, and on it the rooster lamp: a china rooster, the stem rising behind him, a shade."""
    X0, X1, Y0, Y1, Z0, Z1 = M.LAMPTABLE
    p.contact(L, [(X0 - 6, 0, Z0 - 4), (X1 + 4, 0, Z0 - 4), (X1 + 4, 0, Z1 + 8), (X0 - 6, 0, Z1 + 8)], 0.42, 4.0)
    for (x, z) in ((X0, Z0), (X1 - 3, Z0), (X0, Z1 - 3), (X1 - 3, Z1 - 3)):
        p.box(L, x, x + 3, 0, Y1 - 3, z, z + 3, WHITE * 0.95, keep=0.88)
    p.box(L, X0 + 1, X1 - 1, 14, 16, Z0 + 1, Z1 - 1, WHITE * 0.9, keep=0.88)
    p.box(L, X0 + 5, X1 - 9, 16, 20.5, Z0 + 6, Z1 - 3, {"all": (0.36, 0.62, 0.80), "front": (0.92, 0.90, 0.84)}, keep=0.88)   # a picture book on its shelf
    p.box(L, X0, X1, Y1 - 12, Y1 - 3, Z0, Z1, WHITE, keep=0.88)
    p.dot(L, ((X0 + X1) / 2, Y1 - 7.5, Z1 + 0.6), 1.5, (0.86, 0.68, 0.26), fine=False, lit=(0, 0, 1), min_px=0.9)
    p.box(L, X0 - 2, X1 + 2, Y1 - 3, Y1, Z0 - 2, Z1 + 2, WHITE * 1.02, keep=0.88, edge=(1, 0.98, 0.9))
    bx, bz = LAMP[0], LAMP[2]
    p.ball(L, (bx, Y1 + 1.3, bz), 10.5, (0.34, 0.56, 0.30), sy=0.30, keep=0.9)                       # the green china mound he stands on
    p.seg(L, (bx + 2.5, Y1 + 2, bz - 3), (bx + 2.5, LAMP[1] - 12, bz - 3), (0.82, 0.64, 0.26), 1.8, fine=False, lit=p.B, min_px=1.3, keep=0.9)
    hen(p, L, (bx - 0.5, Y1 + 2.0, bz + 2), 33, "snowrooster", face=-1, keep=0.93, gain=1.0)
    sb, st_ = (bx, LAMP[1] - 13, bz), (bx, LAMP[1] + 15, bz)
    cone2(L, sb, st_, 16.5, 9.0, tone_inv((0.985, 0.86, 0.54)), rim=tone_inv((0.985, 0.95, 0.78)), keep=0.92)
    (sx, sy_) = p.pt((bx, LAMP[1] + 2, bz))
    kk = p.k(LAMP)
    p.poly2(L, [(sx - 13.6 * kk, sy_ + 2.0 * kk), (sx + 13.6 * kk, sy_ + 2.0 * kk), (sx + 11.6 * kk, sy_ - 4 * kk), (sx - 11.6 * kk, sy_ - 4 * kk)], tone_inv((0.985, 0.955, 0.80)), 0.7, fine=False, keep=0.92)
    (x0, y0) = p.pt(sb)
    k0 = p.k(sb)
    rick = [(x0 + math.cos(a) * 16.5 * k0, y0 + math.sin(a) * 16.5 * k0 * 0.34 - 0.6) for a in np.linspace(0.0, 3.1416, 13)]
    p.line2(L, rick, tone_inv((0.86, 0.20, 0.16)), 1.3, fine=False, keep=0.92)                       # a red braid round the shade's rim
    # also on the table: her alarm clock
    p.box(L, X0 + 2, X0 + 11, Y1, Y1 + 8, Z1 - 9, Z1 - 3, (0.86, 0.26, 0.22), keep=0.9)
    p.dot(L, (X0 + 6.5, Y1 + 4, Z1 - 2.7), 3.0, (0.96, 0.95, 0.88), fine=False, lit=(0, 0, 1))


def egg_rug(L):
    """A rug like a fried egg, in the middle of the floor."""
    cx, cz, rx, rz = M.EGGRUG
    c = Card(2 * rx, 2 * rz, (0, 0, 0), 3.0, clear=True)
    def blob(k_):
        return [(rx + math.cos(a) * rx * 0.88 * k_ * (1 + 0.10 * math.sin(3 * a + 0.6) + 0.07 * math.sin(5 * a + 1.9) + 0.05 * math.sin(2 * a + 4.0)),
                 rz + math.sin(a) * rz * 0.88 * k_ * (1 + 0.10 * math.sin(3 * a + 0.6) + 0.07 * math.sin(5 * a + 1.9) + 0.05 * math.sin(2 * a + 4.0))) for a in np.linspace(0, 6.2832, 72, endpoint=False)]
    c.poly(blob(1.0), (0.90, 0.88, 0.82)); c.poly(blob(0.95), (0.98, 0.97, 0.93))
    c.disc(rx + 14, rz - 5, 29, (0.90, 0.60, 0.08), 23); c.disc(rx + 14, rz - 6, 27, (0.99, 0.76, 0.14), 21)
    c.disc(rx + 6, rz - 13, 8, (1.0, 0.90, 0.50), 5)
    tex, al = c.done(0.07, 5)
    q = [(cx - rx, 0.5, cz - rz), (cx + rx, 0.5, cz - rz), (cx + rx, 0.5, cz + rz), (cx - rx, 0.5, cz + rz)]
    p.contact(L, [(cx - rx * 0.86, 0.2, cz - rz * 0.86), (cx + rx * 0.86, 0.2, cz - rz * 0.86), (cx + rx * 0.9, 0.2, cz + rz * 0.92), (cx - rx * 0.86, 0.2, cz + rz * 0.92)], 0.14, 3.0)
    p.quad_image(L, q[0], q[1], q[3], tex, al, keep=0.86, shadow=True)


# ================================================================ the tea party (a cut-out: people walk behind it and in front)
def tea_party(L, back):
    cx, cz, r, ht = M.TEATABLE
    def ring(y, rr, n=30):
        return [(cx + math.cos(a) * rr, y, cz + math.sin(a) * rr) for a in np.linspace(0, 6.2832, n, endpoint=False)]
    def stool(x, z, color):
        p.contact(back, [(x - 15, 0, z - 10), (x + 13, 0, z - 10), (x + 13, 0, z + 12), (x - 15, 0, z + 12)], 0.36, 3.0)
        cone2(L, (x, 0, z), (x, 22, z), 10.5, 11.5, p.shade_at(color, (x, 11, z), (-0.3, 0.2, 0.93)), rim=p.shade_at(mix(color, (1, 1, 1), 0.25), (x, 22, z), (0, 1, 0)), keep=0.88)
    p.contact(back, [(cx - r - 10, 0, cz - r - 4), (cx + r + 4, 0, cz - r - 4), (cx + r + 4, 0, cz + r + 10), (cx - r - 10, 0, cz + r + 10)], 0.34, 7.0)
    # the guest on the far side
    p.contact(back, [(cx - 2, 0, cz - 58), (cx + 26, 0, cz - 58), (cx + 26, 0, cz - 34), (cx - 2, 0, cz - 34)], 0.36, 3.0)
    cone2(L, (cx + 12, 0, cz - 46), (cx + 12, 31, cz - 46), 10.5, 11.5, p.shade_at((0.56, 0.80, 0.70), (cx + 12, 16, cz - 46), (-0.3, 0.2, 0.93)), rim=p.shade_at((0.70, 0.90, 0.82), (cx + 12, 31, cz - 46), (0, 1, 0)), keep=0.88)
    hen(p, L, (cx + 12, 31, cz - 44), 35, "dotty", face=1, keep=0.9)                           # (she has the high stool)
    # the table: a foot, a column, a round top with a checked cloth laid cornerwise
    wood = (0.94, 0.92, 0.86)
    p.face(L, ring(1.2, 17), wood, (0, 1, 0), keep=0.88)
    cone2(L, (cx, 1, cz), (cx, ht - 3, cz), 4.6, 4.6, p.shade_at(wood, (cx, 20, cz), (-0.4, 0, 0.9)), keep=0.88)
    p.face(L, ring(ht - 3.4, r + 0.4), col(wood) * 0.70, (0, 1, 0), keep=0.88)
    p.face(L, ring(ht, r), wood, (0, 1, 0), keep=0.88)
    g = Card(48, 48, (0.99, 0.96, 0.92), 4.0)
    for i in range(12):
        for j in range(12):
            a = (i % 2) + (j % 2)
            if a:
                g.rect(i * 4.0, j * 4.0, (i + 1) * 4.0, (j + 1) * 4.0, (0.96, 0.62, 0.66) if a == 1 else (0.90, 0.30, 0.38))
    gt, _ = g.done(0.05, 2)
    q = r - 1
    p.quad_image(L, (cx, ht + 0.4, cz - q), (cx + q, ht + 0.4, cz), (cx - q, ht + 0.4, cz), gt, None, keep=0.9)
    y = ht + 0.6
    china = (0.97, 0.96, 0.92)
    def cup(x, z):
        p.dot(L, (x, y + 0.2, z), 5.4, china, fine=False, lit=(0, 1, 0), sy=0.36, keep=0.9)
        cone2(L, (x, y + 0.4, z), (x, y + 5.2, z), 2.6, 3.4, p.shade_at(china, (x, y + 2, z), (-0.3, 0.3, 0.9), 1.1), rim=(0.42, 0.22, 0.10), keep=0.9)
    cup(cx + 1, cz - 23)
    cup(cx - 23, cz + 1)
    cup(cx + 23, cz + 1)
    # the pot: big and round, sky blue with white spots; a dark edge under it (as the hens have) so that its spout and
    # handle can be told against the cloth and the guest behind
    dots = lambda u, vv, a: np.where(((np.sin(u * 7 + 1) * np.sin(vv * 7 + 2)) > 0.5)[..., None], col((0.99, 0.97, 0.94)), a)
    blue, dark = (0.26, 0.62, 0.94), (0.045, 0.035, 0.055)
    pz = cz - 1
    o = 0.8 / max(p.k((cx, y, pz)), 1e-3)
    spout = [(cx + 6, y + 5.5, pz), (cx + 13.5, y + 8.5, pz), (cx + 16.5, y + 14.5, pz)]
    handle = [(cx - 7, y + 13.5, pz), (cx - 14, y + 12.5, pz), (cx - 14, y + 5.5, pz), (cx - 7, y + 4.5, pz)]
    body, lid = (cx, y + 8.6, pz), (cx, y + 18.4, pz)
    p.path(L, spout, dark, 3.4 + 2 * o, 1.0, fine=False, keep=0.9)
    p.path(L, handle, dark, 2.2 + 2 * o, 1.0, fine=False, keep=0.9)
    p.ball(L, body, 9.4 + o, dark, sy=0.94, keep=0.9)
    p.ball(L, lid, 2.2 + o, dark, keep=0.9)
    p.path(L, spout, blue, 3.4, 1.6, fine=False, lit=p.B, keep=0.9, gain=1.15)
    p.path(L, handle, blue, 2.2, 1.3, fine=False, lit=p.B, keep=0.9, gain=1.15)
    p.ball(L, body, 9.4, blue, sy=0.94, spots=dots, keep=0.9, gain=1.15)
    p.ball(L, lid, 2.2, (0.99, 0.95, 0.90), keep=0.9, gain=1.15)
    # a plate of corn for the guests, and one cup more
    p.dot(L, (cx + 10, y + 0.2, cz + 17), 8.0, (0.62, 0.80, 0.92), fine=False, lit=(0, 1, 0), sy=0.36, keep=0.9)
    cr = np.random.default_rng(3)
    for _ in range(10):
        p.dot(L, (cx + 10 + cr.normal(0, 3.0), y + 1.0, cz + 17 + cr.normal(0, 2.4)), 1.0, (1.0, 0.82, 0.16), fine=False, lit=(0, 1, 0), min_px=0.8, gain=1.2)
    cup(cx - 13, cz + 21)
    # the guests at the sides (beaks over the cloth)
    stool(cx - 49, cz, (0.98, 0.84, 0.40))
    hen(p, L, (cx - 49, 22, cz + 1), 37, "white", face=1, keep=0.9, gain=1.3)
    stool(cx + 49, cz, (0.60, 0.78, 0.94))
    hen(p, L, (cx + 49, 22, cz + 1), 35, "calico", face=-1, keep=0.9)
    # the smallest guest needs two books to reach
    p.contact(back, [(cx - 40, 0, cz + 28), (cx - 8, 0, cz + 28), (cx - 8, 0, cz + 54), (cx - 40, 0, cz + 54)], 0.34, 3.0)
    p.box(L, cx - 38, cx - 12, 0, 6.5, cz + 30, cz + 50, {"all": (0.80, 0.24, 0.22), "front": (0.94, 0.92, 0.86)}, keep=0.9)
    p.box(L, cx - 36, cx - 14, 6.5, 12, cz + 32, cz + 48, {"all": (0.22, 0.42, 0.72), "front": (0.94, 0.92, 0.86)}, keep=0.9)
    hen(p, L, (cx - 25, 12, cz + 40), 22, "chick", face=1, keep=0.9, gain=1.7)
    # and her own place: a cushion on the floor
    p.contact(back, [(cx + 10, 0, cz + 38), (cx + 52, 0, cz + 38), (cx + 52, 0, cz + 66), (cx + 10, 0, cz + 66)], 0.26, 3.0)
    p.ball(L, (cx + 31, 6.0, cz + 52), 20, (0.98, 0.58, 0.70), sy=0.32, keep=0.88)
    p.ball(L, (cx + 31, 10.4, cz + 52), 2.2, (0.99, 0.86, 0.40), sy=0.6, keep=0.88)


# ================================================================ round things that taper


def cone2(L, base, top, r0, r1, color, fine=False, keep=0.85, gain=1.0, rim=None):
    """An upright round thing that tapers (a lampshade, a jar, a pot), drawn through the camera: `base` and `top`
    are the middles of its two ends, r0 and r1 their radii in cm. `color` is laid as it is (times gain)."""
    (x0, y0), (x1, y1) = p.pt(base), p.pt(top)
    k0, k1 = p.k(base), p.k(top)
    sq = 0.34                                                    # how flat a level circle looks from this height
    pts = [(x0 - r0 * k0, y0), (x0 - r0 * k0 * 0.7, y0 + r0 * k0 * sq * 0.72), (x0, y0 + r0 * k0 * sq), (x0 + r0 * k0 * 0.7, y0 + r0 * k0 * sq * 0.72), (x0 + r0 * k0, y0),
           (x1 + r1 * k1, y1), (x1 + r1 * k1 * 0.7, y1 - r1 * k1 * sq * 0.72), (x1, y1 - r1 * k1 * sq), (x1 - r1 * k1 * 0.7, y1 - r1 * k1 * sq * 0.72), (x1 - r1 * k1, y1)]
    p.poly2(L, pts, col(color) * gain, fine=fine, keep=keep)
    if rim is not None:
        p.dot2(L, x1, y1, r1 * k1, max(0.6, r1 * k1 * sq), col(rim), fine=fine, keep=keep)




# ================================================================ the blanket fort
ZF, ZB = 403.0, 294.0                                            # its front and its back
FRF, FRB = (96, 110, ZF), (98, 104, ZB)                          # the ridge: the top rail of the clothes-horse
FLF, FLB = (14, 64, ZF), (14, 62, ZB + 6)                        # the left chair's back
FSF, FSB = (190, 64, ZF), (190, 62, ZB + 6)                      # the right chair's back
WAY_IN = [(121, 0), (119, 30), (124, 58), (134, 75), (148, 80), (166, 71), (181, 60), (187, 40), (189, 0)]   # the way in, on the front (X, Y)
SIGN = (62, 43, 80, 39, -3.0)                                    # middle X, middle Y, width, height, turn
LETTERS = {
    "N": [[(0, 6), (0, 0), (4, 6), (4, 0)]],
    "O": [[(2, 0), (0.7, 0.7), (0, 3), (0.7, 5.3), (2, 6), (3.3, 5.3), (4, 3), (3.3, 0.7), (2, 0)]],
    "B": [[(0, 6), (0, 0), (2.5, 0), (3.6, 0.8), (3.6, 2.2), (2.6, 3), (0, 3)], [(2.6, 3), (3.9, 3.8), (3.9, 5.2), (2.8, 6), (0, 6)]],
    "I": [[(2, 0), (2, 6)], [(0.7, 0), (3.3, 0)], [(0.7, 6), (3.3, 6)]],
    "G": [[(3.8, 1.1), (2.7, 0), (1.3, 0), (0, 1.4), (0, 4.6), (1.3, 6), (2.8, 6), (3.9, 5), (3.9, 3.3), (2.1, 3.3)]],
    "S": [[(3.7, 1.0), (2.7, 0), (1.3, 0), (0.2, 0.9), (0.2, 2.0), (1.2, 2.8), (2.8, 3.2), (3.8, 4.0), (3.8, 5.1), (2.8, 6), (1.2, 6), (0.1, 5.0)]],
    "T": [[(0, 0), (4, 0)], [(2, 0), (2, 6)]],
    "E": [[(3.6, 0), (0, 0), (0, 6), (3.7, 6)], [(0, 3), (2.8, 3)]],
    "R": [[(0, 6), (0, 0), (2.6, 0), (3.7, 0.8), (3.7, 2.3), (2.6, 3.1), (0, 3.1)], [(1.8, 3.1), (3.9, 6)]],
}


def sign_card():
    """NO BIG SISTERS, in crayon capitals, by somebody who is seven and means it."""
    w, h = SIGN[2], SIGN[3]
    c = Card(w, h, (0.97, 0.94, 0.82), 8.0)
    c.rect(0, 0, w, 1.0, (0.86, 0.80, 0.66)); c.rect(0, h - 1.0, w, h, (0.86, 0.80, 0.66))
    r = np.random.default_rng(4)
    inks = [CRAYON["purple"], CRAYON["red"], CRAYON["blue"], (0.10, 0.46, 0.22), (0.84, 0.16, 0.46), CRAYON["blue"], CRAYON["red"]]
    def word(text, x0, y0, lh, lw, gap, k0):
        x = x0
        for i, ch in enumerate(text):
            if ch == " ":
                x += lw * 0.75
                continue
            sc = 1 + r.normal(0, 0.035)
            dy = r.normal(0, 0.45)
            lean = r.normal(0, 0.05)
            for st in LETTERS[ch]:
                pts = [(x + (px / 4.0) * lw * sc + (6 - py) / 6.0 * lean * lh, y0 + dy + (py / 6.0) * lh * sc) for px, py in st]
                c.line(pts, inks[(k0 + i) % len(inks)], 1.75)
            x += lw * sc + gap
    word("NO BIG", 9.5, 4.6, 12.6, 8.4, 2.6, 0)
    word("SISTERS", 5.2, 21.8, 12.6, 7.9, 2.1, 2)
    c.line([(9.5, 18.8), (27.5, 19.3)], CRAYON["red"], 0.9)                                        # NO, underlined twice
    c.line([(9.5, 20.2), (27.5, 20.5)], CRAYON["red"], 0.7)
    c.disc(72.5, 8.4, 2.6, CRAYON["yellow"])                                                        # and one flower, because it looked bare
    for a in range(0, 360, 60):
        c.disc(72.5 + math.cos(math.radians(a)) * 3.6, 8.4 + math.sin(math.radians(a)) * 3.6, 1.7, CRAYON["pink"])
    c.disc(72.5, 8.4, 1.8, CRAYON["yellow"])
    return c.done(0.04, 2)


def afghan_card(w, h, sq=11.0, seed=3):
    """Crocheted squares: every one a different three colors, bordered in dark wool."""
    c = Card(w, h, (0.15, 0.13, 0.20), 3.0)
    r = np.random.default_rng(seed)
    wool = [(0.96, 0.52, 0.66), (0.98, 0.84, 0.36), (0.56, 0.84, 0.72), (0.74, 0.62, 0.90), (0.98, 0.95, 0.86), (0.50, 0.74, 0.94), (0.96, 0.62, 0.36)]
    for j in range(int(h / sq) + 1):
        for i in range(int(w / sq) + 1):
            x0, y0 = i * sq, j * sq
            ks = r.choice(len(wool), 3, replace=False)
            for n, (inset, k) in enumerate(zip((sq * 0.08, sq * 0.24, sq * 0.38), ks)):
                c.rect(x0 + inset, y0 + inset, x0 + sq - inset, y0 + sq - inset, wool[k])
    return c.done(0.10, seed)


def fort(L, back, flash):
    r = np.random.default_rng(15)
    pink, yel = col((0.94, 0.50, 0.63)), col((0.98, 0.84, 0.42))
    # ---- on the floor under and round it
    p.contact(back, [(-4, 0, ZB - 4), (206, 0, ZB - 4), (212, 0, ZF + 14), (-6, 0, ZF + 16)], 0.55, 6.0)
    # ---- the left slope: a striped blanket
    def striped(X, Y, Z, t):
        k = np.floor((Z + 3) / 6.5) % 4
        c = np.where((k == 0)[..., None], col((0.95, 0.56, 0.68)), np.where((k == 2)[..., None], col((0.98, 0.86, 0.48)), col((0.97, 0.94, 0.86))))
        return c * folds(Z + X * 0.4, 31.0, 0.14, 0.4)[..., None]
    p.face(L, [FRB, FRF, FLF, FLB], striped, keep=0.8)
    # ---- the right slope: the crocheted one, and it hangs on down the right side
    tex, al = afghan_card(112, 104, 17.0)
    tex = np.clip(tex * (1 + (noise(tex.shape[:2], 60, 4, 3) - 0.5)[..., None] * 0.25), 0, 1)
    p.quad_image(L, FRB, FRF, FSB, tex, None, keep=0.82)
    def side(X, Y, Z, t):
        return yel * folds(Z, 24.0, 0.2, 2.0)[..., None] * (0.86 + 0.14 * np.clip(Y / 60, 0, 1))[..., None]
    p.face(L, [FSB, FSF, (199, 0, ZF + 1), (198, 0, ZB)], side, keep=0.8)
    # ---- the front: her pink blanket, hung from the ridge; daisies on it
    c = Card(204, 114, pink, 3.0)
    for j in range(9):
        for i in range(15):
            x, y = 6 + i * 14.5 + (j % 2) * 7.2 + r.normal(0, 0.8), 6 + j * 13.0 + r.normal(0, 0.8)
            for a in range(0, 360, 72):
                c.disc(x + math.cos(math.radians(a)) * 2.5, y + math.sin(math.radians(a)) * 2.5, 1.7, (0.99, 0.95, 0.90))
            c.disc(x, y, 1.4, (0.98, 0.80, 0.30))
    c.rect(0, 104, 204, 114, (0.98, 0.80, 0.86))                                                    # a satin edge along the bottom
    ftex, _ = c.done(0.10, 5)
    def front(X, Y, Z, t):
        a = sample(ftex, X * 3.0, (114 - Y) * 3.0)
        sag = folds(X + (110 - Y) * 0.35 * np.sign(X - 96), 26.0, 0.17, 0.7, 1.4)
        return a * sag[..., None] * (0.90 + 0.10 * np.clip(Y / 40.0, 0, 1))[..., None]
    outline = [(2, 0), (8, 40), (FLF[0], FLF[1]), (FRF[0], FRF[1]), (FSF[0], FSF[1]), (195, 40), (199, 0)]
    p.face(L, [(x, y, ZF) for x, y in outline], front, (0, 0, 1), keep=0.82)
    # ---- the way in: dark inside; what can be made out is the second chair, a rail of the clothes-horse, a pillow
    p.face(L, [(x, y, ZF + 0.3) for x, y in WAY_IN], (0.085, 0.06, 0.10), (0, 0, 1), keep=0.8, lit=False)
    g = 0.55
    wood = (0.86, 0.74, 0.52)
    p.box(L, 150, 186, 30, 33, 334, 372, wood, keep=0.8, gain=g)                                      # the chair's seat, its legs
    for (x, z) in ((151, 370), (183, 370)):
        p.box(L, x, x + 3, 0, 30, z - 3, z, wood, keep=0.8, gain=g)
    p.seg(L, (100, 103, ZF - 5), (126, 0, ZF - 7), wood, 2.4, fine=False, lit=(0.3, 0, 0.95), gain=0.8)      # the clothes-horse: a leg, and the rails going back
    for yy in (34, 66):
        x = 126 - 26 * yy / 103.0
        p.seg(L, (x, yy, ZF - 7), (x + 1, yy, ZB + 14), wood, 1.8, fine=False, lit=(0.5, 0.5, 0.7), gain=0.5)
    p.ball(L, (144, 9, 372), 21, (0.98, 0.74, 0.80), sy=0.42, gain=0.75)                             # a pillow to lie on
    # ---- the front blanket drawn back from the way in, and pegged
    flap = [(108, 96), (118, 78), (126, 58), (120, 30), (123, 0), (106, 0), (103, 38), (104, 70)]
    def flapc(X, Y, Z, t):
        return pink * 0.86 * folds(X * 2.2 + Y * 0.3, 9.0, 0.3, 0.9, 1.6)[..., None]
    p.face(L, [(x, y, ZF + 1.0) for x, y in flap], flapc, (0.25, 0, 0.97), keep=0.82)
    p.box(L, 121, 124, 50, 60, ZF + 1, ZF + 3, (0.86, 0.72, 0.48), keep=0.9)                        # a clothes-peg
    # ---- the blankets' edges hanging over the front
    def over_r(X, Y, Z, t):
        a = sample(tex, np.clip((X - 96) * 3.3, 0, tex.shape[1] - 2), np.full_like(X, 6.0))
        return a * 0.9
    p.face(L, [(FRF[0], FRF[1] + 1.5, ZF + 1.2), (FSF[0] + 2, FSF[1] + 1.5, ZF + 1.2), (FSF[0] + 3, FSF[1] - 9, ZF + 1.2), (FRF[0] + 3, FRF[1] - 10, ZF + 1.2)], over_r, (0, 0, 1), keep=0.82)
    p.face(L, [(FRF[0], FRF[1] + 1.5, ZF + 1.2), (FLF[0] - 2, FLF[1] + 1.5, ZF + 1.2), (FLF[0] - 3, FLF[1] - 7, ZF + 1.2), (FRF[0] - 3, FRF[1] - 8.5, ZF + 1.2)],
           lambda X, Y, Z, t: np.where((np.floor(X / 5.0) % 2 == 0)[..., None], col((0.95, 0.56, 0.68)), col((0.97, 0.94, 0.86))), (0, 0, 1), keep=0.82)
    # ---- the chairs' backs stand up through it; the ridge pole sticks out in front
    for (x, z) in ((FLF[0] + 1, ZB + 40), (FLF[0] + 1, ZF - 22), (FSF[0] - 1, ZB + 40), (FSF[0] - 1, ZF - 22)):
        p.box(L, x - 1.6, x + 1.6, 60, 72, z - 1.6, z + 1.6, WHITE, keep=0.85)
        p.ball(L, (x, 73.5, z), 2.6, WHITE)
    p.seg(L, (FRF[0], FRF[1] + 0.5, ZF - 4), (FRF[0], FRF[1] + 0.5, ZF + 9), wood, 3.0, fine=False, lit=(0.4, 0.5, 0.75), min_px=1.6)
    p.dot(L, (FRF[0], FRF[1] + 0.5, ZF + 9.2), 1.6, mix(wood, (1, 1, 1), 0.3), fine=False)
    # ---- the sign
    cx, cy, w, h, deg = SIGN
    stex, sal = sign_card()
    tl, tr, bl = rot2(cx, cy, w, h, deg)
    p.contact(L, [(tl[0] + 2, tl[1] - 3, ZF + 1), (tr[0] + 2, tr[1] - 3, ZF + 1), (tr[0] + 2 + (bl[0] - tl[0]), bl[1] - 3 + (tr[1] - tl[1]), ZF + 1), (bl[0] + 2, bl[1] - 3, ZF + 1)], 0.35, 1.6)
    p.quad_image(L, (tl[0], tl[1], ZF + 2.2), (tr[0], tr[1], ZF + 2.2), (bl[0], bl[1], ZF + 2.2), stex, sal, keep=0.97, gain=1.08)
    for (px, py) in ((tl[0] + 9, tl[1] + 0.5), (tr[0] - 9, tr[1] + 0.5)):                             # two clothes-pegs hold it to the blanket
        p.box(L, px - 1.4, px + 1.4, py - 5, py + 4.5, ZF + 2.4, ZF + 4, (0.86, 0.72, 0.48), keep=0.9)
    # ---- the string of small lights: along the ridge, then down both edges of the front
    def hang(a, b, n, sag):
        out = []
        for i in range(n + 1):
            u = i / n
            out.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u - sag * math.sin(u * math.pi), a[2] + (b[2] - a[2]) * u))
        return out
    wire = hang((FRB[0], FRB[1] + 3, FRB[2] + 2), (FRF[0], FRF[1] + 3.5, ZF + 4), 8, 2.0)
    wire += hang((FRF[0], FRF[1] + 3.5, ZF + 4), (144, 92, ZF + 3), 5, 4.0)[1:] + hang((144, 92, ZF + 3), (FSF[0] + 1, FSF[1] + 5, ZF + 3), 5, 4.0)[1:] + hang((FSF[0] + 1, FSF[1] + 5, ZF + 3), (197, 18, ZF + 3), 5, -1.5)[1:]
    wire_l = hang((FRF[0], FRF[1] + 3.5, ZF + 4), (54, 91, ZF + 3), 5, 4.0) + hang((54, 91, ZF + 3), (FLF[0], FLF[1] + 5, ZF + 3), 5, 4.0)[1:]
    for wr in (wire, wire_l):
        p.path(L, wr, (0.10, 0.20, 0.12), 0.5, 0.7, fine=False, alpha=0.9)
    bulbs = [wire[i] for i in range(2, len(wire), 2)] + [wire_l[i] for i in range(2, len(wire_l), 2)]
    FORT_BULBS[:] = bulbs
    for i, b in enumerate(bulbs):
        P = (b[0], b[1] - 1.6, b[2] + 0.4)
        p.glow(L, P, 4.6 * p.k(P), (1.0, 0.72, 0.36), 0.60)
        p.dot(L, P, 1.35, (2.6, 2.2, 1.4), fine=False, min_px=1.1)
    # ---- the hem lies in heaps along the floor
    for i in range(11):
        x = 6 + i * 10.6 + r.normal(0, 1.5)
        if x > 106:
            continue
        p.ball(L, (x, 1.6, ZF + 2 + r.random() * 3), 6.0 + r.random() * 2, (0.98, 0.80, 0.86), sy=0.34)
    # ---- a guard
    animal(L, "bear", (64, 0, ZF + 13), 25)
    # ---- the flashlight, just inside the way in: its own cut-out, because she takes it
    a, b = (137, 4.2, ZF + 3), (158, 4.6, ZF + 7)
    x0, y0 = p.pt(a); x1, y1 = p.pt(b)
    p.shade2(L, [(x0 - 1, y0 + 1.5), (x1 + 3, y1 + 1.5), (x1 + 3, y1 + 4.5), (x0 - 1, y0 + 4.5)], 0.5, 1.2)
    body = p.shade_at((0.99, 0.84, 0.16), a, (0, 0.5, 0.86), 1.5)
    head = p.shade_at((0.97, 0.36, 0.62), b, (0, 0.5, 0.86), 1.5)
    k = p.k(a)
    p.line2(flash, [(x0, y0), (x1 - 4.6 * k, y1 - 0.3)], body, 5.6 * k, fine=False, keep=0.95)
    p.line2(flash, [(x0 + 1.0 * k, y0 - 1.5 * k), (x1 - 6.0 * k, y1 - 1.9 * k)], np.clip(body * 1.3 + 0.1, 0, 3), 1.3 * k, fine=False, keep=0.95)   # the shine along its top
    p.line2(flash, [(x1 - 4.4 * k, y1 - 0.2), (x1 + 1.2 * k, y1)], head, 8.2 * k, fine=False, keep=0.95)
    p.dot2(flash, x1 + 2.8 * k, y1 + 0.1, 2.0 * k, 3.9 * k, np.clip(head * 0.55, 0, 3), fine=False, keep=0.95)
    p.dot2(flash, x1 + 3.2 * k, y1 + 0.1, 1.4 * k, 3.0 * k, col((0.80, 0.92, 1.0)) * 0.9, fine=False, keep=0.95)                        # the glass
    p.dot2(flash, (x0 + x1) / 2 - 1.5 * k, (y0 + y1) / 2 - 2.2 * k, 1.5 * k, 1.1 * k, head, fine=False, keep=0.95)                      # its button
    lp = [(x0 - 0.5 * k, y0), (x0 - 4.5 * k, y0 - 2.4 * k), (x0 - 7.2 * k, y0 + 0.8 * k), (x0 - 4.0 * k, y0 + 2.6 * k), (x0 - 0.5 * k, y0 + 0.8 * k)]
    p.line2(flash, lp, head * 0.9, 1.0, fine=False, keep=0.95)                                       # and its wrist loop


def fort_doormat(L):
    """A small rag rug before the fort's way in (she made it a front step)."""
    cx, cz, rx, rz = 158, 438, 34, 21
    c = Card(2 * rx, 2 * rz, (0, 0, 0), 4.0, clear=True)
    for i, cc in enumerate(((0.92, 0.46, 0.58), (0.98, 0.86, 0.48), (0.56, 0.80, 0.70), (0.97, 0.93, 0.84), (0.92, 0.46, 0.58), (0.98, 0.86, 0.48))):
        k = 1 - i * 0.165
        c.disc(rx, rz, rx * k, cc, rz * k)
    tex, al = c.done(0.12, 8)
    p.contact(L, [(cx - rx - 2, 0.2, cz - rz - 2), (cx + rx + 2, 0.2, cz - rz - 2), (cx + rx + 2, 0.2, cz + rz + 3), (cx - rx - 2, 0.2, cz + rz + 3)], 0.16, 2.0)
    p.quad_image(L, (cx - rx, 0.5, cz - rz), (cx + rx, 0.5, cz - rz), (cx - rx, 0.5, cz + rz), tex, al, keep=0.8, shadow=True)


# ================================================================ the foreground: things near us, cut off by the bottom edge
def emit(c):
    return tone_inv(c)


def door(L, back):
    """The door to the landing: its open leaf, edge on to us at the picture's right, and the frame it hangs in."""
    X, (Z0, Z1), H = M.DOOR_X, M.DOOR_Z, M.DOOR_H
    p.contact(back, [(X - 10, 0, Z0 - 4), (X + 8, 0, Z0 - 4), (X + 8, 0, Z1 + 6), (X - 10, 0, Z1 + 6)], 0.4, 4.0)
    paint = col((0.80, 0.70, 0.60)) * 0.74
    def leaf(X_, Y, Z, t):
        c = np.broadcast_to(paint, Y.shape + (3,)).copy()
        mid = (Z0 + Z1) / 2
        for (z0, z1) in ((Z0 + 10, mid - 5), (mid + 5, Z1 - 10)):
            for (y0, y1) in ((18, 86), (106, 190)):
                inside = (Z > z0) & (Z < z1) & (Y > y0) & (Y < y1)
                c = np.where(inside[..., None], paint * 0.93, c)
                c = np.where(((np.abs(Y - y1) < 1.6) & (Z > z0) & (Z < z1))[..., None], paint * 0.62, c)      # each panel's own small shadows
                c = np.where(((np.abs(Z - z1) < 1.2) & (Y > y0) & (Y < y1))[..., None], paint * 0.66, c)
                c = np.where(((np.abs(Y - y0) < 1.2) & (Z > z0) & (Z < z1))[..., None], paint * 1.12, c)
                c = np.where(((np.abs(Z - z0) < 1.0) & (Y > y0) & (Y < y1))[..., None], paint * 1.10, c)
        return c * (0.94 + 0.12 * STAIN.at(Z * 2, Y * 2))[..., None]
    p.box(L, X, X + 4, 0, H, Z0, Z1, {"all": paint, "left": leaf, "top": paint * 1.1}, keep=0.85)
    p.ball(L, (X - 3.0, 100, Z0 + 7), 3.4, (0.90, 0.70, 0.28))                                         # the knob
    p.dot(L, (X - 0.4, 100, Z0 + 7), 4.6, (0.60, 0.46, 0.20), fine=False, lit=(-1, 0, 0), sx=0.5) if False else None
    for yy in (24, 176):                                                                               # hinges
        p.box(L, X - 0.6, X + 0.2, yy, yy + 9, Z1 - 1.5, Z1 + 1.0, (0.78, 0.62, 0.28), keep=0.9)
    wall = [(X + 4, 0, Z1 + 8), (WD + 60, 0, Z1 + 8), (WD + 60, roof_y(X + 4) + 3, Z1 + 8), (X + 4, roof_y(X + 4) + 3, Z1 + 8)]
    p.face(L, wall, (0.10, 0.065, 0.075), (0, 0, 1), keep=0.8, lit=False)                               # the wall it hangs in, cut through
    p.box(L, X, X + 9, 0, H + 7, Z1, Z1 + 8.5, paint * 0.9, keep=0.85)                                  # the jamb
    p.box(L, X - 9, X + 9, H + 1, H + 9, Z1 + 1, Z1 + 8.5, paint * 0.9, keep=0.85)                      # and the end of the head of the frame


def window_hen(L, cx, y0, z, kind="white", face=1, size=1.0):
    """A hen looking out of a lit window of the hen house: her breast, neck and head over the sill, dark-edged against the light."""
    K = dict(white=((0.86, 0.87, 0.92), (0.70, 0.71, 0.80)), brown=((0.56, 0.32, 0.17), (0.40, 0.22, 0.12)), black=((0.16, 0.15, 0.21), (0.26, 0.25, 0.34)),
             buff=((0.88, 0.60, 0.26), (0.70, 0.44, 0.16)), speckled=((0.82, 0.82, 0.86), (0.20, 0.19, 0.25)), chick=((0.98, 0.82, 0.20), (0.90, 0.64, 0.10)),
             grey=((0.60, 0.62, 0.74), (0.46, 0.48, 0.60)))[kind]
    f, s_ = face, size
    body, shade_ = tone_inv(K[0]), tone_inv(K[1])
    edge, red, beak = tone_inv((0.10, 0.07, 0.09)), tone_inv((0.86, 0.14, 0.12)), tone_inv((0.98, 0.66, 0.14))
    k = p.k((cx, y0, z))
    def P_(dx, dy):
        return p.pt((cx + f * dx * s_, y0 + dy * s_, z))
    def disc(dx, dy, rx, ry, colr, grow=0.0):
        x, y = P_(dx, dy)
        p.dot2(L, x, y, rx * s_ * k + grow, ry * s_ * k + grow, colr, fine=False, keep=0.95)
    if kind == "chick":
        disc(0.0, 3.2, 4.4, 3.6, edge, 0.8); disc(0.6, 8.4, 3.5, 3.4, edge, 0.8)
        disc(0.0, 3.2, 4.4, 3.6, body); disc(0.6, 8.4, 3.5, 3.4, body)
        p.poly2(L, [P_(3.6, 9.0), P_(3.6, 7.4), P_(5.8, 8.1)], beak, fine=False, keep=0.95)
        disc(1.6, 9.0, 0.62, 0.62, edge)
        return
    disc(-1.6, 3.6, 5.6, 4.6, edge, 0.8); disc(0.8, 7.4, 3.2, 4.0, edge, 0.8); disc(1.5, 11.6, 3.5, 3.5, edge, 0.8)
    for dx in (-0.3, 1.5, 3.2):                                 # the comb
        disc(dx, 15.3 - abs(dx - 1.5) * 0.3, 1.25, 1.35, edge, 0.6)
    for dx in (-0.3, 1.5, 3.2):
        disc(dx, 15.3 - abs(dx - 1.5) * 0.3, 1.25, 1.35, red)
    disc(-1.6, 3.6, 5.6, 4.6, body); disc(0.8, 7.4, 3.2, 4.0, body); disc(1.5, 11.6, 3.5, 3.5, body)
    disc(-2.6, 3.2, 3.4, 2.6, shade_)
    if kind == "speckled":
        for (dx, dy) in ((-3.6, 4.6), (-0.6, 5.2), (-2.0, 2.0), (0.8, 3.2), (1.4, 7.6), (-4.4, 2.6)):
            disc(dx, dy, 0.7, 0.7, shade_)
    p.poly2(L, [P_(4.6, 12.6), P_(4.6, 10.6), P_(7.6, 11.4)], edge, fine=False, keep=0.95)
    p.poly2(L, [P_(4.5, 12.2), P_(4.5, 10.9), P_(7.0, 11.4)], beak, fine=False, keep=0.95)
    disc(3.9, 9.2, 1.0, 1.5, red)
    disc(2.6, 12.3, 0.62, 0.62, edge)


def coop(L, back):
    """The toy hen house: the dollhouse, turned to face us and given over to the hens. A hen looks out of every lit
    window; a ramp she made goes up to the front door."""
    X0, X1, Y0, Y1, Z0, Z1 = M.COOP
    wall_h, zr, mid = 54.0, (Z0 + Z1) / 2, (X0 + X1) / 2
    zf = Z1
    p.contact(back, [(X0 - 6, 0, Z0 - 6), (X1 + 6, 0, Z0 - 6), (X1 + 6, 0, Z1 + 4), (X0 - 6, 0, Z1 + 4)], 0.5, 6.0)
    def clap(X, Y, Z, t):
        c = col((1.0, 0.80, 0.34)) * (1 - 0.30 * lines(Y, 4.6, 0.7, footprint(Y)))[..., None] * (0.93 + 0.14 * STAIN.at(X * 3, Y * 3))[..., None]
        trim = (X < X0 + 4) | (X > X1 - 4) | (Y > wall_h - 3.2) | (Y < 2.5) | (np.abs(Y - 29.5) < 1.2)
        return np.where(trim[..., None], col((0.95, 0.94, 0.88)), c)
    p.face(L, [(X0, 0, zf), (X1, 0, zf), (X1, wall_h, zf), (X0, wall_h, zf)], clap, (0, 0, 1), keep=0.88, gain=2.0)
    p.shade2(L, [p.pt((X0, wall_h, zf + 0.2)), p.pt((X1, wall_h, zf + 0.2)), p.pt((X1, wall_h - 5, zf + 0.2)), p.pt((X0, wall_h - 5, zf + 0.2))], 0.42, 1.2)
    lit_c = emit((0.99, 0.80, 0.36))
    white = (0.96, 0.95, 0.90)
    def win(x, y0, y1, kind, face, w=17.0):
        z = zf + 0.5
        p.face(L, [(x - w / 2 - 1.6, y0 - 1.6, z), (x + w / 2 + 1.6, y0 - 1.6, z), (x + w / 2 + 1.6, y1 + 1.6, z), (x - w / 2 - 1.6, y1 + 1.6, z)], white, (0, 0, 1), keep=0.9, gain=1.15)
        p.face(L, [(x - w / 2, y0, z + 0.2), (x + w / 2, y0, z + 0.2), (x + w / 2, y1, z + 0.2), (x - w / 2, y1, z + 0.2)], lit_c, (0, 0, 1), keep=0.95, lit=False)
        window_hen(L, x - face * 1.5, y0, z + 0.4, kind, face, size=(y1 - y0) / 18.5)
        p.box(L, x - w / 2 - 2.6, x + w / 2 + 2.6, y0 - 3.2, y0 - 1.6, zf, zf + 2.6, white, keep=0.9, gain=1.15)                # the sill
        sr = np.random.default_rng(int(x * 7 + y0))
        for _ in range(7):                                      # straw on the sill
            sx = x + sr.uniform(-w / 2 - 1, w / 2 + 1)
            p.seg(L, (sx, y0 - 1.4, zf + 2.2), (sx + sr.normal(0, 2.4), y0 - 1.4 - sr.uniform(1.0, 4.5), zf + 2.8), tone_inv((0.96, 0.80, 0.30)), 0.5, min_px=0.9, fine=False, keep=0.9)
    win(X0 + 21, 34, 51, "white", 1)
    win(mid, 34, 51, "brown", -1)
    win(X1 - 21, 34, 51, "speckled", -1)
    win(X0 + 21, 8, 26, "black", 1)
    win(X1 - 21, 8, 26, "buff", -1)
    # the front door, open, a chick on the step; the ramp
    p.face(L, [(mid - 10.5, 5, zf + 0.5), (mid + 10.5, 5, zf + 0.5), (mid + 10.5, 28, zf + 0.5), (mid - 10.5, 28, zf + 0.5)], white, (0, 0, 1), keep=0.9, gain=1.15)
    p.face(L, [(mid - 8.5, 6.5, zf + 0.7), (mid + 8.5, 6.5, zf + 0.7), (mid + 8.5, 26.5, zf + 0.7), (mid - 8.5, 26.5, zf + 0.7)], lit_c, (0, 0, 1), keep=0.95, lit=False)
    p.face(L, [(mid - 8.5, 6.5, zf + 0.9), (mid - 15.5, 6.5, zf + 6.5), (mid - 15.5, 26.5, zf + 6.5), (mid - 8.5, 26.5, zf + 0.9)], (0.84, 0.30, 0.38), keep=0.9, gain=1.2)   # the door leaf, pink, standing open
    window_hen(L, mid + 1.5, 6.5, zf + 1.0, "chick", -1, size=1.05)
    ramp = [(mid - 7.5, 6.0, zf + 0.6), (mid + 7.5, 6.0, zf + 0.6), (mid + 9.5, 0.4, zf + 30), (mid - 5.5, 0.4, zf + 30)]
    p.contact(back, [(mid - 9, 0, zf), (mid + 12, 0, zf), (mid + 14, 0, zf + 32), (mid - 7, 0, zf + 32)], 0.35, 3.0)
    p.face(L, ramp, (0.78, 0.60, 0.38), keep=0.9, gain=1.15)
    for i in range(1, 6):                                       # the cleats, so that nobody slips
        t = i / 6.0
        a = tuple(ramp[0][j] + (ramp[3][j] - ramp[0][j]) * t for j in range(3))
        b = tuple(ramp[1][j] + (ramp[2][j] - ramp[1][j]) * t for j in range(3))
        p.seg(L, (a[0], a[1] + 0.6, a[2]), (b[0], b[1] + 0.6, b[2]), (0.52, 0.36, 0.20), 1.3, min_px=1.2, fine=False, lit=(0, 0.8, 0.6), keep=0.9, gain=1.2)
    # the roof: scalloped shingles, a ridge, a chimney, one dormer (a chick up there too), and her sign
    eave = (wall_h - 1.0, zf + 5.0)
    rise, run = Y1 - eave[0], eave[1] - zr
    def shingle(X, Y, Z, t):
        s_ = np.hypot(Y - eave[0], eave[1] - Z)
        row = np.floor(s_ / 5.2)
        u = X + (row % 2) * 3.0
        tile_ = np.floor(u / 6.0)
        tn = hash01(tile_, row, 5.0)
        c = lerp(col((0.74, 0.30, 0.34)), col((0.94, 0.50, 0.50)), tn[..., None])
        within = (s_ / 5.2 - row)
        c = c * (0.70 + 0.34 * np.clip(within * 2.2, 0, 1))[..., None]                              # each row shades the next one down
        return c * (1 - 0.35 * lines(u, 6.0, 0.7, footprint(X)))[..., None]
    def on_roof(x, t, lift=0.5):                                # a place on the front slope: t = 0 at the eave, 1 at the ridge
        return (x, eave[0] + rise * t + lift * 0.8, eave[1] - run * t + lift * 0.6)
    p.face(L, [(X0 - 4, eave[0], eave[1]), (X1 + 4, eave[0], eave[1]), (X1 + 4, Y1, zr), (X0 - 4, Y1, zr)], shingle, keep=0.88, gain=1.12)
    p.seg(L, (X0 - 4, eave[0], eave[1] + 0.3), (X1 + 4, eave[0], eave[1] + 0.3), white, 1.6, fine=False, lit=(0, 0, 1), min_px=1.5, gain=1.15)   # the fascia
    p.seg(L, (X0 - 4, Y1 + 0.6, zr), (X1 + 4, Y1 + 0.6, zr), (0.98, 0.82, 0.80), 2.0, fine=False, lit=(0, 1, 0), min_px=1.5, gain=1.25)         # the ridge
    cz_ = zr + run * 0.36
    cy0 = eave[0] + rise * (1 - 0.36)
    p.box(L, X1 - 30, X1 - 18, cy0 - 6, Y1 + 9, cz_ - 6, cz_ + 6, (0.70, 0.36, 0.28), keep=0.88, gain=1.1)        # chimney
    p.box(L, X1 - 31.5, X1 - 16.5, Y1 + 9, Y1 + 12, cz_ - 7.5, cz_ + 7.5, (0.92, 0.90, 0.84), keep=0.88, gain=1.1)
    dzf = zr + run * 0.74                                       # the dormer's face
    dy0 = eave[0] + rise * (1 - 0.74)
    ddx = X0 + 26
    p.box(L, ddx - 11, ddx + 11, dy0 - 2, dy0 + 18, dzf - 14, dzf, (1.0, 0.80, 0.34), keep=0.88, gain=1.15)
    p.face(L, [(ddx - 7, dy0 + 2, dzf + 0.3), (ddx + 7, dy0 + 2, dzf + 0.3), (ddx + 7, dy0 + 15, dzf + 0.3), (ddx - 7, dy0 + 15, dzf + 0.3)], lit_c, (0, 0, 1), keep=0.95, lit=False)
    window_hen(L, ddx, dy0 + 2, dzf + 0.5, "chick", 1, size=0.9)
    p.face(L, [(ddx - 13, dy0 + 17, dzf + 1.5), (ddx, dy0 + 28, dzf + 1.5), (ddx, dy0 + 28, dzf - 16), (ddx - 13, dy0 + 17, dzf - 16)], (0.74, 0.30, 0.36), keep=0.88, gain=1.1)
    p.face(L, [(ddx + 13, dy0 + 17, dzf + 1.5), (ddx, dy0 + 28, dzf + 1.5), (ddx, dy0 + 28, dzf - 16), (ddx + 13, dy0 + 17, dzf - 16)], (0.88, 0.46, 0.50), keep=0.88, gain=1.1)
    p.poly3(L, [(ddx - 13, dy0 + 17, dzf + 1.6), (ddx + 13, dy0 + 17, dzf + 1.6), (ddx, dy0 + 28, dzf + 1.6)], white, fine=False, lit=(0, 0, 1), gain=1.15)
    # her sign, taped to the roof
    sw, sh = 62.0, 12.5
    c = Card(sw, sh, (0.98, 0.96, 0.86), 8.0)
    inks = [CRAYON["red"], CRAYON["blue"], (0.10, 0.46, 0.22), CRAYON["purple"], (0.84, 0.16, 0.46)]
    stroke_word(c, "HEN HOUSE", 3.2, 2.2, 8.2, 5.0, 1.25, [(0.74, 0.06, 0.06), (0.06, 0.14, 0.60), (0.02, 0.36, 0.12), (0.38, 0.08, 0.50), (0.74, 0.08, 0.36)], w_cm=1.45, seed=6, wobble=0.8)
    stex, sal = c.done(0.04, 3)
    sx0 = mid - 20
    p.quad_image(L, on_roof(sx0, 0.80), on_roof(sx0 + sw, 0.80), on_roof(sx0, 0.80 - sh / math.hypot(rise, run)), stex, sal, keep=0.97, gain=1.3)
    SIGNS["henhouse"] = [round(v_) for v_ in (p.pt(on_roof(sx0, 0.80)) + p.pt(on_roof(sx0 + sw, 0.80 - sh / math.hypot(rise, run))))]
    # corn in a jar lid by the ramp, and two eggs that rolled
    p.dot(L, (mid + 26, 0.6, zf + 14), 6.0, (0.70, 0.72, 0.78), fine=False, lit=(0, 1, 0), sy=0.36, keep=0.9, gain=1.2)
    cr = np.random.default_rng(5)
    for _ in range(8):
        p.dot(L, (mid + 26 + cr.normal(0, 2.4), 1.2, zf + 14 + cr.normal(0, 1.8)), 0.9, (1.0, 0.82, 0.16), fine=False, lit=(0, 1, 0), min_px=0.9, gain=1.3)


def nest(L, back):
    """The nest: a cardboard box she has made into a nesting box. Straw, a hen sitting, plastic eggs in colors no hen ever laid."""
    X0, X1, Y0, Y1, Z0, Z1 = M.NEST
    card = col((0.80, 0.62, 0.40))
    p.contact(back, [(X0 - 8, 0, Z0 - 6), (X1 + 8, 0, Z0 - 6), (X1 + 8, 0, Z1 + 4), (X0 - 8, 0, Z1 + 4)], 0.5, 6.0)
    p.face(L, [(X0 + 1, 6, Z0 + 1), (X1 - 1, 6, Z0 + 1), (X1 - 1, Y1, Z0 + 1), (X0 + 1, Y1, Z0 + 1)], card * 0.62, (0, 0, 1), keep=0.85)       # the far side, seen inside
    p.face(L, [(X0, Y1, Z0), (X0, Y1, Z1), (X0 - 13, Y1 - 5, Z1), (X0 - 13, Y1 - 5, Z0)], card * 1.05, keep=0.88)                               # a flap folded out, left
    p.face(L, [(X1, Y1, Z0), (X1, Y1, Z1), (X1 + 13, Y1 - 5, Z1), (X1 + 13, Y1 - 5, Z0)], card * 0.95, keep=0.88)                               # and right
    def straw_top(X, Y, Z, t):
        g = GRAIN.at(X * 9 + Z * 3, Z * 9 - X * 3)
        return lerp(col((0.78, 0.60, 0.22)), col((1.0, 0.86, 0.42)), g[..., None])
    p.face(L, [(X0 + 1, Y1 - 6, Z0 + 1), (X1 - 1, Y1 - 6, Z0 + 1), (X1 - 1, Y1 - 6, Z1 - 1), (X0 + 1, Y1 - 6, Z1 - 1)], straw_top, (0, 1, 0), keep=0.88, gain=1.1)
    sr = np.random.default_rng(12)
    def straws(n, zlo, zhi, up):
        for _ in range(n):
            x, z = sr.uniform(X0 + 2, X1 - 2), sr.uniform(zlo, zhi)
            a = sr.uniform(0, 6.28)
            ln = sr.uniform(6, 13)
            p.seg(L, (x, Y1 - 6, z), (x + math.cos(a) * ln, Y1 - 6 + sr.uniform(up * 0.3, up), z + math.sin(a) * ln * 0.5),
                  (1.0, 0.86, 0.40) if sr.random() < 0.6 else (0.82, 0.62, 0.22), 0.7, min_px=0.9, fine=False, lit=(0, 0.8, 0.6), keep=0.9, gain=1.15)
    straws(34, Z0 + 2, Z1 - 20, 9)
    mid = (X0 + X1) / 2
    hen(p, L, (mid + 2, Y1 - 9, Z0 + 26), 37, "buff", face=-1, keep=0.92, feet=False)
    eggs = [((X0 + 9, Y1 - 3.4, Z1 - 9), (0.98, 0.52, 0.70)), ((X1 - 12, Y1 - 3.4, Z1 - 8), (0.50, 0.78, 0.96)), ((mid - 6, Y1 - 3.2, Z1 - 5), (0.62, 0.88, 0.60)),
            ((X1 - 24, Y1 - 3.0, Z1 - 12), (1.0, 0.86, 0.32))]
    for P_, cc in eggs:
        p.ball(L, P_, 4.1, cc, sx=1.25, sy=0.95, rot=0.3, keep=0.92, gain=1.6)
    straws(26, Z1 - 16, Z1 - 1, 7)
    # the side toward us: NEST, in crayon (and nothing beside the word: a drawn egg there read as a fifth letter)
    fw, fh = X1 - X0, Y1
    c = Card(fw, fh, tuple(card), 6.0)
    for yy in (6.0, 13.0, 21.0, 28.5):
        c.line([(0, yy), (fw, yy + 0.3)], tuple(card * 0.90), 0.5)
    stroke_word(c, "NEST", 9.5, 9.0, 18.0, 11.2, 3.8, [(0.70, 0.05, 0.06), (0.05, 0.12, 0.56), (0.02, 0.34, 0.10), (0.36, 0.06, 0.46)], w_cm=2.7, seed=9, wobble=0.9)
    ftex, _ = c.done(0.06, 4)
    p.quad_image(L, (X0, Y1, Z1), (X1, Y1, Z1), (X0, 0, Z1), ftex, None, keep=0.95, gain=1.25)
    SIGNS["nest"] = [round(v_) for v_ in (p.pt((X0, Y1, Z1)) + p.pt((X1, 0, Z1)))]
    p.box(L, X0, X0 + 0.6, 0, Y1, Z0, Z1, card * 0.8, keep=0.88)                                    # its left side (we see a little of it)
    # the ones that got away
    for (ex, ez, cc) in ((X0 - 20, Z1 - 2, (0.66, 0.42, 0.96)), (X0 - 42, Z1 - 16, (0.98, 0.36, 0.60)), (X0 - 30, Z1 - 34, (1.0, 0.80, 0.16)), (X1 + 22, Z1 - 20, (0.30, 0.66, 0.98))):
        p.contact(back, [(ex - 5, 0, ez - 3), (ex + 5, 0, ez - 3), (ex + 5, 0, ez + 4), (ex - 5, 0, ez + 4)], 0.3, 1.6)
        p.ball(L, (ex, 3.5, ez), 4.3, cc, sx=1.25, sy=0.92, rot=-0.2, keep=0.92, gain=2.1)
    for _ in range(9):
        x, z = sr.uniform(X0 - 34, X0 - 4), sr.uniform(Z1 - 40, Z1 + 2)
        a = sr.uniform(0, 3.14)
        p.seg(L, (x, 0.5, z), (x + math.cos(a) * 9, 0.5, z + math.sin(a) * 4), (1.0, 0.86, 0.40), 0.6, min_px=0.9, fine=False, lit=(0, 1, 0), keep=0.9, gain=1.1)


def crate(L, back):
    """Picture books in a low crate; the one she is reading now leans against it, cover out."""
    X0, X1, Y0, Y1, Z0, Z1 = M.CRATE
    wood = col((0.78, 0.60, 0.38))
    p.contact(back, [(X0 - 6, 0, Z0 - 6), (X1 + 6, 0, Z0 - 6), (X1 + 6, 0, Z1 + 4), (X0 - 6, 0, Z1 + 4)], 0.5, 5.0)
    p.face(L, [(X0, Y1 - 1, Z0), (X1, Y1 - 1, Z0), (X1, Y1 - 1, Z1), (X0, Y1 - 1, Z1)], (0.07, 0.06, 0.09), (0, 1, 0), keep=0.8, lit=False)
    cols_ = [(0.86, 0.22, 0.20), (0.22, 0.46, 0.80), (0.98, 0.80, 0.22), (0.30, 0.64, 0.40), (0.92, 0.50, 0.70), (0.52, 0.34, 0.72), (0.96, 0.58, 0.18), (0.40, 0.72, 0.86)]
    x = X0 + 3.0
    br = np.random.default_rng(8)
    i = 0
    while x < X1 - 5:                                           # the books, standing, their spines up
        w_ = br.uniform(3.4, 6.5)
        hgt = br.uniform(26, 36)
        p.box(L, x, x + w_ - 0.5, 4, hgt, Z0 + 4, Z1 - 4, {"all": cols_[i % len(cols_)], "top": mix(cols_[i % len(cols_)], (1, 1, 1), 0.35), "front": (0.94, 0.92, 0.86)}, keep=0.9, gain=1.1)
        x += w_
        i += 1
    def slats(X, Y, Z, t):
        gap = (np.mod(Y, 9.0) > 7.2)
        return np.where(gap[..., None], col((0.10, 0.08, 0.10)), wood * (0.86 + 0.28 * GRAIN.at(X * 0.8 + Z * 0.8, Y * 8.0))[..., None])
    p.box(L, X0, X1, 0, Y1, Z1 - 2, Z1, {"all": wood, "front": slats}, keep=0.88, gain=1.1)
    p.box(L, X1 - 2, X1, 0, Y1, Z0, Z1, {"all": wood, "right": slats}, keep=0.88, gain=1.1)
    # the book leaning on it: a hen on the cover (no title that anyone could read)
    c = Card(27, 33, (0.42, 0.72, 0.92), 6.0)
    c.rect(0, 0, 2.2, 33, (0.22, 0.42, 0.66))
    c.disc(21, 7.5, 3.6, (1.0, 0.86, 0.30))
    c.rect(2.2, 25.5, 27, 33, (0.44, 0.72, 0.36))
    flat_hen(c, 14.5, 27.5, 17.5, (0.99, 0.98, 0.95), face=1, edge=(0.20, 0.16, 0.18), edge_w=0.45)
    c.line([(6, 4.6), (9, 3.8), (12, 4.8), (15, 3.8), (17, 4.6)], (0.98, 0.96, 0.90), 1.1)
    btex, _ = c.done(0.05, 2)
    p.contact(back, [(X0 + 2, 0, Z1), (X0 + 34, 0, Z1), (X0 + 36, 0, Z1 + 14), (X0 + 4, 0, Z1 + 14)], 0.4, 3.0)
    p.quad_image(L, (X0 + 5, 31.0, Z1 + 1.0), (X0 + 32, 31.0, Z1 + 1.0), (X0 + 5, 0.6, Z1 + 11.0), btex, None, keep=0.95, gain=1.15)


def toybox(L, back):
    X0, X1, Y0, Y1, Z0, Z1 = M.TOYBOX
    mint = col((0.52, 0.80, 0.70))
    p.contact(back, [(X0 - 6, 0, Z0 - 6), (X1 + 8, 0, Z0 - 6), (X1 + 8, 0, Z1 + 4), (X0 - 6, 0, Z1 + 4)], 0.5, 6.0)
    p.face(L, [(X0, Y1 - 1, Z0), (X1, Y1 - 1, Z0), (X1, Y1 - 1, Z1), (X0, Y1 - 1, Z1)], (0.06, 0.05, 0.09), (0, 1, 0), keep=0.8, lit=False)
    p.face(L, [(X0 + 3, 4, Z0 + 3), (X1 - 3, 4, Z0 + 3), (X1 - 3, Y1, Z0 + 3), (X0 + 3, Y1, Z0 + 3)], mint * 0.6, (0, 0, 1), keep=0.8)     # the far side, seen inside
    animal(L, "bear", (X0 + 22, 22, Z0 + 22), 40, keep=0.85)
    animal(L, "rabbit", (X0 + 60, 20, Z0 + 26), 36, flop=True, keep=0.85, fur_=(0.96, 0.72, 0.78))
    hen(p, L, (X0 + 42, 30, Z0 + 42), 26, "grey", face=1, keep=0.9)
    p.ball(L, (X0 + 70, Y1 + 2, Z0 + 42), 9.5, (0.92, 0.30, 0.32), spots=lambda u, vv, a: np.where((np.abs(u + vv * 0.4) < 0.24)[..., None], col((0.98, 0.88, 0.40)), a))
    def star(X, Y, Z, t):
        u, vv = (X - (X0 + X1) / 2) / 13.0, (Y - 22) / 13.0
        ang = np.arctan2(vv, u)
        rr = np.hypot(u, vv)
        st = rr < (0.55 + 0.45 * np.cos(ang * 5 + 1.57) ** 2) * 0.9
        board = 1 - 0.25 * lines(Y, 14.6, 0.7, footprint(Y))
        return np.where(st[..., None], col((0.98, 0.86, 0.44)), mint * board[..., None])
    p.box(L, X0, X1, 0, Y1, Z1 - 2.5, Z1, {"all": mint, "front": star}, keep=0.88, edge=(0.9, 1.0, 0.9))
    p.box(L, X1 - 2.5, X1, 0, Y1, Z0, Z1, mint * 0.95, keep=0.88)
    # what did not get put away: blocks
    blk = [(0.96, 0.52, 0.60), (0.98, 0.84, 0.36), (0.50, 0.74, 0.92), (0.56, 0.82, 0.60), (0.80, 0.62, 0.92)]
    for i, (x, z, hh) in enumerate(((258, 574, 6), (270, 590, 6), (262, 606, 12), (252, 598, 6))):
        p.contact(back, [(x - 2, 0, z - 2), (x + 9, 0, z - 2), (x + 9, 0, z + 9), (x - 2, 0, z + 9)], 0.3, 1.6)
        p.box(L, x, x + 6, 0, 6, z, z + 6, blk[i % 5], keep=0.88, edge=(1, 1, 1))
        if hh > 6:
            p.box(L, x + 0.5, x + 6.5, 6, 12, z + 0.5, z + 6.5, blk[(i + 2) % 5], keep=0.88)


def mobile(L):
    """Felt chickens on threads from a rafter over the foot of her bed (front plane: nobody is tall enough to pass before it)."""
    hx, hy, hz = M.MOBILE
    hub = (hx, hy, hz)
    p.seg(L, (hx, hy + 22, hz), hub, (0.86, 0.84, 0.78), 0.4, min_px=1.25, fine=False)
    rods = [((hx - 22, hy, hz), (hx + 22, hy, hz)), ((hx, hy - 2, hz - 22), (hx, hy - 2, hz + 22))]
    for a, b in rods:
        p.seg(L, a, b, (0.80, 0.66, 0.44), 1.0, min_px=1.1, fine=False, lit=(0, -0.3, 0.9), gain=1.3)
    birds = [((hx - 22, hy, hz), 30, dict(body=(0.99, 0.98, 0.94)), 1, 0.25), ((hx + 22, hy, hz), 21, dict(body=(1.0, 0.82, 0.14), kind="chick", wing=(0.96, 0.60, 0.06)), -1, -0.3),
             ((hx, hy - 2, hz - 22), 40, dict(body=(0.86, 0.26, 0.14), wing=(0.62, 0.16, 0.08)), 1, -0.2), ((hx, hy - 2, hz + 22), 17, dict(body=(0.99, 0.46, 0.66), wing=(0.90, 0.30, 0.52)), -1, 0.3),
             ((hx, hy - 1, hz), 54, dict(body=(0.30, 0.62, 0.96), wing=(0.16, 0.42, 0.82)), 1, 0.1)]
    for top, drop, kw, face, turn in birds:
        P = (top[0], top[1] - drop, top[2])
        p.seg(L, top, (P[0], P[1] + 8.5, P[2]), (0.90, 0.88, 0.82), 0.3, min_px=1.25, fine=False)
        c = Card(24, 21, (0, 0, 0), 6.0, clear=True)
        flat_hen(c, 12 - face * 1.2, 20.5, 20.0, face=face, edge=(0.16, 0.12, 0.14), edge_w=0.5, legs=False, kind=kw.pop("kind", "sitting"), **kw)
        tex, al = c.done(0.05, 1)
        ct, st_ = math.cos(turn), math.sin(turn)
        ex = (p.R[0] * ct + p.B[0] * st_, 0.0, p.R[2] * ct + p.B[2] * st_)                          # each one turns a little on its thread
        tl = (P[0] - ex[0] * 12, P[1] + 10.5, P[2] - ex[2] * 12)
        tr = (P[0] + ex[0] * 12, P[1] + 10.5, P[2] + ex[2] * 12)
        bl = (tl[0], P[1] - 10.5, tl[2])
        p.quad_image(L, tl, tr, bl, tex, al, keep=0.95, lit=False, gain=float(tone_inv((0.86, 0.86, 0.86))[0]))


def garland(L):
    """Paper eggs she cut out and colored, on a string from the ridge beam down to the purlin, above the chart."""
    a, b = (WD / 2 + 8, RIDGE - 36, 520), (WD / 2 + 184, roof_y(WD / 2 + 184) - 24, 384)
    n = 15
    pts = []
    for i in range(n + 1):
        u = i / n
        pts.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u - 34 * math.sin(u * math.pi), a[2] + (b[2] - a[2]) * u))
    p.path(L, pts, (0.86, 0.84, 0.78), 0.4, 0.8, fine=False, alpha=0.8)
    cols_ = [(0.98, 0.56, 0.70), (0.99, 0.86, 0.36), (0.54, 0.80, 0.96), (0.62, 0.88, 0.62), (0.80, 0.66, 0.96), (0.99, 0.70, 0.40)]
    for i in range(1, n):
        P = pts[i]
        c = Card(13, 17, (0, 0, 0), 6.0, clear=True)
        egg(c, 6.5, 8.6, 5.4, cols_[i % len(cols_)], stripe=(0.99, 0.98, 0.94) if i % 2 else None, dots=(0.99, 0.98, 0.94) if i % 2 == 0 else None)
        tex, al = c.done(0.05, i)
        tl = (P[0] - p.R[0] * 6.5, P[1] - 1.0, P[2] - p.R[2] * 6.5)
        tr = (P[0] + p.R[0] * 6.5, P[1] - 1.0, P[2] + p.R[2] * 6.5)
        p.quad_image(L, tl, tr, (tl[0], P[1] - 18.0, tl[2]), tex, al, keep=0.92, gain=1.5)


def floor_things(L):
    """Flat and small things on the open floor (people walk over them)."""
    # a drawing she left half done, by the rug, and the crayons where they rolled
    c = Card(42, 30, PAPER, 5.0)
    grass(c, 42, 25.6)
    flat_hen(c, 15, 25.4, 20.0, (0.99, 0.99, 0.96), face=1, edge=EDGE, edge_w=0.6)
    c.line([(26, 20), (30, 14), (34, 19), (37, 12)], CRAYON["red"], 0.8)
    tex, al = c.done(0.05, 31)
    p.contact(L, [(226, 0.2, 176), (272, 0.2, 172), (276, 0.2, 206), (230, 0.2, 210)], 0.14, 1.6)
    p.quad_image(L, (228, 0.4, 178), (270, 0.4, 174), (231, 0.4, 208), tex, al, keep=0.92, shadow=True)
    r = np.random.default_rng(17)
    for i, name in enumerate(("red", "yellow", "blue", "green", "orange", "purple")):
        a = r.uniform(0, 3.14)
        x, z = 276 + r.uniform(0, 30), 180 + r.uniform(0, 34)
        p.seg(L, (x, 0.7, z), (x + math.cos(a) * 9, 0.7, z + math.sin(a) * 5), CRAYON[name], 1.2, fine=False, lit=(0, 1, 0), min_px=1.3, gain=1.25, keep=0.9)
    # plastic eggs, still out from her last egg hunt
    eggs = [((340, 150), (0.98, 0.36, 0.60)), ((420, 132), (0.30, 0.66, 0.98)), ((252, 330), (0.40, 0.84, 0.44)), ((536, 386), (1.0, 0.80, 0.16)),
            ((364, 404), (0.66, 0.42, 0.96)), ((500, 172), (0.98, 0.50, 0.20)), ((560, 290), (0.30, 0.66, 0.98)), ((308, 232), (0.98, 0.36, 0.60))]
    for (x, z), cc in eggs:
        p.contact(L, [(x - 5, 0, z - 3), (x + 6, 0, z - 3), (x + 6, 0, z + 4), (x - 5, 0, z + 4)], 0.3, 1.4)
        p.ball(L, (x, 3.6, z), 4.3, cc, sx=1.25, sy=0.92, rot=r.uniform(-0.5, 0.5), keep=0.92, gain=1.5)
    # corn the guests spilled
    for _ in range(14):
        x, z = M.TEATABLE[0] + r.normal(0, 30), M.TEATABLE[1] + 44 + r.uniform(0, 30)
        p.dot(L, (x, 0.5, z), 0.9, (1.0, 0.82, 0.16), fine=False, lit=(0, 1, 0), min_px=0.8, gain=1.2)


def crown(L):
    """Over the window, on the curtain rod: a big paper rooster she made at school, crowing."""
    w, h = 78.0, 70.0
    c = Card(w, h, (0, 0, 0), 5.0, clear=True)
    flat_hen(c, 44, 68.5, 64.0, (0.84, 0.26, 0.12), face=1, kind="rooster", wing=(0.98, 0.72, 0.16), edge=(0.99, 0.97, 0.90), edge_w=1.5, seed=2)
    tex, al = c.done(0.06, 4)
    cx, y0 = (WX0 + WX1) / 2 - 4, WY1 + 20
    p.contact(L, [(cx - 30, y0 + 4, 0.5), (cx + 32, y0 + 4, 0.5), (cx + 30, y0 + 62, 0.5), (cx - 26, y0 + 60, 0.5)], 0.26, 2.5)
    p.quad_image(L, (cx - w / 2, y0 + h, 1.2), (cx + w / 2, y0 + h, 1.2), (cx - w / 2, y0, 1.2), tex, al, keep=0.95)


def edges(L):
    """The room's own edges, said again crisply. They are laid before anything is stood in the room, so that
    furniture covers them as it should; a high `keep` brings them back through the brush."""
    far = 1100.0
    dark = (0.10, 0.09, 0.15)
    kw = dict(fine=False, keep=0.92)
    p.seg(L, (0, 0.4, 0.4), (WD, 0.4, 0.4), dark, 0.8, alpha=0.5, **kw)
    p.seg(L, (0.4, 0.4, 0), (0.4, 0.4, far), dark, 0.8, alpha=0.45, **kw)
    p.seg(L, (WD - 0.4, 0.4, 0), (WD - 0.4, 0.4, far), dark, 0.8, alpha=0.45, **kw)
    for (a, b_) in (((0.3, 0, 0.3), (0.3, KNEE - 7, 0.3)), ((WD - 0.3, 0, 0.3), (WD - 0.3, KNEE - 7, 0.3))):
        p.seg(L, a, b_, dark, 0.7, alpha=0.4, **kw)
    for side in (-1, 1):                                        # the rake of the gable where the roof meets it
        K, Rg = ((0, KNEE), (WD / 2 - 9, RIDGE - 9 * RUN)) if side < 0 else ((WD, KNEE), (WD / 2 + 9, RIDGE - 9 * RUN))
        p.seg(L, (K[0], K[1], 0.4), (Rg[0], Rg[1], 0.4), dark, 0.9, alpha=0.5, **kw)


def door_drawing(L):
    """A crayon hen, taped to the door as high as she can reach (the leaf itself is as it was). The face of the leaf
    that we see is the one that looks out on the landing when the door is shut: this is the hen the landing shows."""
    X = M.DOOR_X - 0.5
    tex, al, w, h = drawing("hen", 5)
    z0, y1 = 624.0, 134.0
    p.quad_image(L, (X, y1, z0), (X, y1, z0 + w * BIG), (X, y1 - h * BIG, z0), tex, al, keep=0.93, gain=1.25)
    for (yy, zz) in ((y1, z0), (y1, z0 + w * BIG)):
        p.poly3(L, [(X - 0.2, yy + 1.4, zz - 2.6), (X - 0.2, yy + 2.0, zz + 2.6), (X - 0.2, yy - 1.4, zz + 2.8), (X - 0.2, yy - 2.0, zz - 2.4)], (0.94, 0.90, 0.74), 0.9, fine=False, lit=(-1, 0, 0), keep=0.85, gain=1.2)


def front_plane(L, back):
    toybox(L, back)
    crate(L, back)
    coop(L, back)
    nest(L, back)
    door(L, back)
    door_drawing(L)
    mobile(L)


# ================================================================ putting it together


def blockers():
    """What stands in the lamps' light: boxes, near enough to the shape of each thing."""
    tx, tz, tr, th = M.TEATABLE
    b = [(60, 134, 0, 104, 296, 400), (8, 60, 0, 62, 296, 400), (134, 198, 0, 62, 296, 400),                  # the fort
         (84, 258, 0, 58, 18, 108), (112, 232, 58, 100, 24, 66),                                               # the flock
         M.BED, (606, 706, 0, 92, 192, 196), (612, 702, 44, 76, 262, 384),                                      # the bed, its headboard, the heap
         (M.LAMPTABLE[0], M.LAMPTABLE[1], 36, 48, M.LAMPTABLE[4], M.LAMPTABLE[5]),
         (tx - tr, tx + tr, th - 4, th, tz - tr, tz + tr), (tx - 4, tx + 4, 0, th, tz - 4, tz + 4),             # the tea table
         (tx - 52, tx - 32, 0, 50, tz - 10, tz + 10), (tx + 32, tx + 52, 0, 50, tz - 10, tz + 10), (tx - 10, tx + 10, 0, 50, tz - 50, tz - 30),
         (286, 410, 0, 54, 526, 596), (286, 410, 54, 76, 546, 576), M.NEST, M.TOYBOX, M.CRATE,
         (M.DOOR_X, M.DOOR_X + 4, 0, M.DOOR_H, M.DOOR_Z[0], M.DOOR_Z[1])]
    return b


def build():
    p.blockers = blockers()
    back = Layer(SHAPE)
    shell(back)
    edges(back)
    window(back)
    crown(back)
    wall_things(back)
    egg_rug(back)
    floor_things(back)
    egg_light(back)
    flock(back)
    bed(back)
    lamp_table(back)
    garland(back)
    fort_doormat(back)
    ft, fl, fr, tp = Layer(SHAPE), Layer(SHAPE), Layer(SHAPE), Layer(SHAPE)
    tea_party(tp, back)
    fort(ft, back, fl)
    front_plane(fr, back)
    return dict(back=back, fort=ft, flashlight=fl, front=fr, teaparty=tp)


def flatten(layers, order):
    """Lay the layers' crisp paint over one another. -> (h, w, 3)"""
    pic = layers[order[0]].color().copy()
    for name in order[1:]:
        L = layers[name]
        pic = pic * (1 - L.a[..., None]) + L.c
    return pic


def depth_air(pic):
    """Depth by tone: the near corners and the foreground deep and warm, the roof overhead falling away into the dark."""
    h, w = SHAPE
    yy, xx = np.mgrid[0:h, 0:w].astype(F32)
    near = np.clip((yy - 440) / 160.0, 0, 1) ** 1.4
    side = np.clip((np.abs(xx - 400) - 150) / 250.0, 0, 1) ** 1.6
    corner = np.clip(near * (0.45 + 0.75 * side), 0, 1)
    top = np.clip((190 - yy) / 190.0, 0, 1) ** 0.8 * np.clip((np.abs(xx - 380) - 40) / 260.0, 0, 1)
    k = np.clip(corner * 0.50 + top * 0.62, 0, 0.74)
    return pic * (1 - k[..., None] * (1 - col((0.50, 0.32, 0.34))))


def palette_pick(px, colors, seed=3, rounds=10):
    """Choose a palette for a picture with many small bright things in it. A third of the colors start as far from
    one another as the picture's colors go (so a comb's red, a chick's yellow, the felt blue each get a place of
    their own); the rest start where the paint is thickest (floor, roof, wall). Then both settle (k-means)."""
    rng = np.random.default_rng(seed)
    px = px.astype(F32)
    far = max(2, colors // 3)
    first = px[rng.integers(len(px))]
    centres = [first]
    d = ((px - first) ** 2).sum(axis=1)
    for _ in range(far - 1):
        j = int(d.argmax())
        centres.append(px[j])
        d = np.minimum(d, ((px - px[j]) ** 2).sum(axis=1))
    rest = px[rng.choice(len(px), size=colors - far, replace=False)]
    C = np.vstack([np.array(centres, dtype=F32), rest]).astype(F32)
    for _ in range(rounds):
        near = np.empty(len(px), dtype=np.int32)
        for a in range(0, len(px), 20000):
            part = px[a:a + 20000]
            near[a:a + 20000] = ((part[:, None, :] - C[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        for k in range(colors):
            mine = px[near == k]
            if len(mine):
                C[k] = mine.mean(axis=0)
    return C


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.008, amount=0.013, dear=()):
    """Grain, then a limited palette (see palette_pick). The boxes in `dear` (x0, y0, x1, y1) are counted again
    when the palette is chosen: they hold the small things that must not go grey."""
    g = grain(picture, seed, amount)
    sample_of = (g if alpha is None else g[alpha > 0.5]).reshape(-1, 3)
    n = len(np.unique((sample_of * 255).astype(np.uint8), axis=0))
    rs = np.random.default_rng(seed)
    parts = [sample_of[rs.choice(len(sample_of), size=min(len(sample_of), 40000), replace=False)]]
    for (x0, y0, x1, y1) in dear:
        d = g[y0:y1, x0:x1].reshape(-1, 3)
        parts.append(d[rs.choice(len(d), size=min(len(d), 4000), replace=False)])
    pal = palette_pick(np.vstack(parts), min(colors, max(2, n)))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def show(pic, name):
    Image.fromarray((np.clip(pic, 0, 1) * 255).astype(np.uint8)).save(name)


WOBBLE = dict(amount=0.75, cell=34.0, seed=77)
ORDER = ("back", "fort", "flashlight", "teaparty", "front")


def hand(a):
    """The same slight unsteadiness for every layer (so that they still fit one another exactly)."""
    return warp(a, WOBBLE["amount"], WOBBLE["cell"], WOBBLE["seed"])


def paint_all(layers, order, fast=False):
    """Crisp paint -> brush pass -> the hard things said again -> the fine sheet. -> {name: (color, alpha or None)}"""
    out = {}
    L = layers["back"]
    crisp_back = hand(depth_air(tone(L.color())))
    keep = hand(L.keep)
    brushed = crisp_back if fast else strokes(crisp_back, sizes=(9, 5, 2), seed=2, density=1.5, jitter=0.03, keep=0.0)
    back = lerp(brushed, crisp_back, keep[..., None])
    fa = L.fa[..., None]
    back = back * (1 - fa) + depth_air(tone(L.fine())) * fa
    out["back"] = (np.clip(back, 0, 1), None)
    h, w = SHAPE
    for name in order[1:]:
        L = layers[name]
        a = hand(L.a)
        ys, xs = np.where(a > 0.02)
        if len(ys) == 0:
            continue
        y0, y1, x0, x1 = max(0, ys.min() - 14), min(h, ys.max() + 15), max(0, xs.min() - 14), min(w, xs.max() + 15)
        warm = col((0.98, 0.86, 0.76)) if name == "front" else 1.0
        whole = crisp_back * (1 - a[..., None]) + hand(depth_air(tone(L.color()))) * warm * a[..., None]
        crop = whole[y0:y1, x0:x1]
        br = crop if fast else strokes(crop, sizes=(7, 4, 2), seed=3 + len(name), density=1.6, jitter=0.03, keep=0.0)
        kp = hand(L.keep)[y0:y1, x0:x1]
        colr = whole.copy()
        colr[y0:y1, x0:x1] = lerp(br, crop, kp[..., None])
        fa = L.fa[..., None]
        colr = colr * (1 - fa) + depth_air(tone(L.fine())) * fa
        out[name] = (np.clip(colr, 0, 1), (np.maximum(a, L.fa) > 0.5).astype(F32))
    return out


def lay_together(done, order):
    pic = done["back"][0].copy()
    for name in order[1:]:
        if name in done:
            c, a = done[name]
            pic = pic * (1 - a[..., None]) + c * a[..., None]
    return pic


if __name__ == "__main__":
    t0 = time.time()
    fast = len(sys.argv) > 1 and sys.argv[1] == "fast"
    os.makedirs(OUT, exist_ok=True)
    layers = build()
    order = [n for n in ORDER if n in layers]
    print("built", round(time.time() - t0, 1))
    done = paint_all(layers, order, fast)
    show(lay_together(done, order), "out/home-lilsis-room-2-all.png")
    print("painted", round(time.time() - t0, 1))
    if fast:                                                # the layers too, unfinished, for standing people among them
        mid = lay_together(done, [n for n in order if n in ("back", "fort", "flashlight")])
        show(mid, "out/home-lilsis-room-fast-mid.png")
        for name in ("teaparty", "front"):
            c, a = done[name]
            Image.fromarray((np.dstack([np.clip(c, 0, 1), a]) * 255).astype(np.uint8), "RGBA").save(f"out/home-lilsis-room-fast-{name}.png")
        sys.exit()
    dear = [(140, 180, 300, 390), (395, 215, 520, 310), (500, 240, 700, 460), (380, 350, 520, 440), (255, 120, 440, 310)]
    print("back", finish(done["back"][0], f"{OUT}/back.png", 160, dear=dear))
    for name, colors in (("fort", 80), ("flashlight", 24), ("teaparty", 64), ("front", 96)):
        print(name, finish(done[name][0], f"{OUT}/{name}.png", colors, done[name][1]))
    import home_lilsis_room_mobile                          # round four: the mobile is lifted out of front.png, its own cut-out, to stir
    print("mobile", home_lilsis_room_mobile.split(OUT))
    import home_lilsis_room_layout
    home_lilsis_room_layout.write(f"{OUT}/layout.json", signs=dict(SIGNS))
    print("done", round(time.time() - t0, 1))

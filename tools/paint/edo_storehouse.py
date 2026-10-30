"""PAINT-20C: inside the charcoal-burner's storehouse (edo-storehouse), the same dusk in rain, through one camera.

A small dim room of dark boards on a raised floor, the rain loud on the thatch overhead: the back wall with the small
high square window (grey rain-light in it) and charcoal sacks of straw piled under it; the front door on the right
wall with a wooden bar across it inside; a straw mat in the middle of the floor over a trapdoor; a lantern on a hook
on the left wall; tools (a saw and a rake on the back wall, baskets, coils of straw rope on pegs); light between the
floorboards when the room below is lit.

CAMERA: persp.Camera(horizon 285, full 480, focal 400): the eye about 2.1 m up; the back wall's floor line on row
410, 4.2 m wide, the walls 2.4 m high; the room runs 1.7 m nearer than the `full` row (the foreground) and 2.45 m
behind it. A grown-up is 160 px on row 480, about 114 px at the back wall and 200 px at the bottom edge.

LIGHT: dim, cool, from the window (grey-blue) and the gaps round the door; the lantern unlit at first; the floorgaps'
light and the lantern lit are cut-outs the game shows (warm, the only warm things). No black: the dark leans blue.

    python3 edo_storehouse.py          out/edo-storehouse/ (back and every cut-out and state, layout.json, a comp)
    python3 edo_storehouse.py fast     no brush pass, no palette: out/edo-storehouse-work/ only"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
from persp import Camera
from edo_cedars_kit import Paper, col, mix
from postimp_paints import PAINTS

ID = "edo-storehouse"
W, H = 800, 600
SHAPE = (H, W)
HZ, FULL, FOCAL = 285, 480, 400
CAM = Camera(HZ, FULL, vanish_x=400, focal=FOCAL)
OUT = "out/edo-storehouse"
WORK = "out/edo-storehouse-work"
LINE = "#1a2846"
PX, PY = grid(SHAPE)
# the room, cm: x across (0 the middle), y up, z from the `full` row (the back wall at Z_BACK, the front edge at Z_NEAR)
X0, X1 = -210.0, 210.0
Z_BACK, Z_NEAR = 245.0, -170.0
WALL_H = 240.0
WINDOW = {"x0": 55, "x1": 110, "y0": 168, "y1": 223}                   # in the back wall
DOOR = {"z0": 10, "z1": 95, "h": 180}                                  # on the right wall (x = X1)
MAT = {"x0": -70, "x1": 60, "z0": 40, "z1": 150}
MAT_ASIDE = {"x0": -200, "x1": -70, "z0": 60, "z1": 170}
TRAP = {"x0": -45, "x1": 35, "z0": 55, "z1": 135}
LANTERN = {"z": 170, "y": 150, "r": 16}                                # on the left wall (x = X0)
SACKS = [(70, 195, 0, 32, 190, 245), (118, 160, 0, 32, 190, 245), (160, 205, 0, 32, 188, 243),                 # the pile under the window: (x0, x1, y0, y1, z0, z1)
         (85, 140, 32, 62, 192, 245), (140, 195, 32, 62, 192, 245), (108, 170, 62, 90, 196, 245)]
SACKS_LEFT = [(-205, -150, 0, 32, 150, 205), (-205, -150, 0, 32, 205, 245), (-200, -160, 32, 60, 190, 245)]
SACKS_HEAP = [(-60, 0, 0, 32, 60, 115), (0, 55, 0, 32, 60, 115), (-55, 10, 0, 32, 112, 150), (-30, 30, 32, 62, 70, 130)]   # #27: over the mat
P = CAM.pt


def grownup_px(y):
    return float(160.0 * (y - HZ) / (FULL - HZ))


def fpt(x, z):
    return P(x, 0, z)


def poly3(s, pts, c, a=1.0):
    s.poly([P(*p) for p in pts], c, a)


# ================================================================ the paints, by name (the act's style sheet)
def paint(name):
    return rgb(PAINTS[name]["hex"])


PRUSSIAN, COBALT, ULTRA, CERULEAN = paint("prussian-blue"), paint("cobalt-blue"), paint("ultramarine"), paint("cerulean")
WHITE, OCHRE, SIENNA, NAPLES, VIRIDIAN = paint("lead-white"), paint("yellow-ochre"), paint("burnt-sienna"), paint("naples-yellow"), paint("viridian")
PAPER = lerp(lerp(WHITE, CERULEAN, 0.30), PRUSSIAN, 0.10)                      # the rain's grey light, as outside
LINE = PRUSSIAN
LAMP = lerp(NAPLES, OCHRE, 0.15)                                               # the lamp's warmth: naples yellow


def shade_of(c, t=0.35):
    """The shade flat of a lit flat: pulled toward the key's shade (cobalt into prussian), never darkened grey."""
    return lerp(c, lerp(COBALT, PRUSSIAN, 0.6), t)


# the room's flats: dim, but every one readable: ochre planks pulled toward prussian, the shade blue
WALL_L = lerp(OCHRE, PRUSSIAN, 0.44)                 # the left wall: the window's light rakes it
WALL_R = lerp(OCHRE, PRUSSIAN, 0.50)                 # the right wall, with the door
WALL_B = lerp(OCHRE, PRUSSIAN, 0.56)                 # the back wall, against the light
FLOOR = lerp(lerp(OCHRE, SIENNA, 0.4), PRUSSIAN, 0.42)
ROOF = lerp(PRUSSIAN, SIENNA, 0.28)                  # the roof space: the thatch's underside, deep
RAFTER = lerp(lerp(OCHRE, SIENNA, 0.5), PRUSSIAN, 0.45)
STRAW = lerp(OCHRE, WHITE, 0.30)                     # straw bales, lit
IRON = lerp(PRUSSIAN, SIENNA, 0.12)


# ================================================================ the shell, as flats with drawn lines
def shell(pic, seed=11):
    """Floor, walls and the roof space: one flat per face (the shade blue, not black), the planks drawn as lines running
    to the vanishing point, the rafters as flats; a hard-edged patch of the window's light on the back wall under the
    window and on the floor (a flat, not a pool)."""
    x, y = PX, PY
    k = CAM.scale(Z_BACK)
    wy = HZ + CAM.eye * k
    wtop = HZ + (CAM.eye - WALL_H) * k
    wx0, wx1 = CAM.vx + X0 * k, CAM.vx + X1 * k
    pic[...] = vary(ROOF, SHAPE, seed, 0.03, 90)
    s = Paper(SHAPE)
    far_z = Z_NEAR - 180
    # the floor
    s.poly([fpt(X0 - 60, far_z), fpt(X1 + 60, far_z), fpt(X1, Z_BACK), fpt(X0, Z_BACK)], FLOOR, 1.0)
    # the walls
    s.poly([fpt(X0, Z_BACK), fpt(X1, Z_BACK), P(X1, WALL_H, Z_BACK), P(X0, WALL_H, Z_BACK)], WALL_B, 1.0)
    s.poly([fpt(X0, Z_BACK), P(X0, WALL_H, Z_BACK), P(X0, WALL_H, far_z), fpt(X0, far_z)], WALL_L, 1.0)
    s.poly([fpt(X1, Z_BACK), P(X1, WALL_H, Z_BACK), P(X1, WALL_H, far_z), fpt(X1, far_z)], WALL_R, 1.0)
    # the window's light: a flat of the paper pulled toward cobalt, on the wall under the window and on the floor in front
    Wd = WINDOW
    light_wall = [P(Wd["x0"] - 20, Wd["y0"], Z_BACK), P(Wd["x1"] + 30, Wd["y0"], Z_BACK), P(Wd["x1"] + 60, 0, Z_BACK), P(Wd["x0"] - 50, 0, Z_BACK)]
    s.poly(light_wall, lerp(WALL_B, PAPER, 0.10), 1.0)
    s.poly([fpt(Wd["x0"] - 50, Z_BACK), fpt(Wd["x1"] + 60, Z_BACK), fpt(Wd["x1"] + 110, Z_BACK - 150), fpt(Wd["x0"] - 10, Z_BACK - 150)], lerp(FLOOR, PAPER, 0.16), 1.0)
    # the wall plates and the rafters: flats
    s.poly([P(X0, WALL_H, Z_BACK), P(X1, WALL_H, Z_BACK), P(X1, WALL_H + 14, Z_BACK), P(X0, WALL_H + 14, Z_BACK)], RAFTER, 1.0)
    for xs in (X0, X1):
        s.poly([P(xs, WALL_H, Z_BACK), P(xs, WALL_H, far_z), P(xs, WALL_H + 14, far_z), P(xs, WALL_H + 14, Z_BACK)], shade_of(RAFTER, 0.3), 1.0)
    for z in np.arange(Z_BACK - 10, far_z + 40, -90):
        for xs in (X0, X1):
            w = max(2.0, 6 * CAM.scale(z))
            a, b = P(xs, WALL_H + 14, z), P(0, WALL_H + 150, z)
            s.line([a, b], RAFTER, w, 1.0)
            s.line([a, b], LINE, 0.7, 0.5)
    # bundles hung from the rafters: a coil of rope, a basket: flats
    s.ellipse(*P(-120, WALL_H + 70, 150), 9, 16, lerp(STRAW, PRUSSIAN, 0.45), 1.0)
    s.ellipse(*P(150, WALL_H + 60, 60), 12, 10, lerp(STRAW, PRUSSIAN, 0.5), 1.0)
    # drawn lines: the floorboards (24 cm, running back) and their butt joints; the walls' planks (20 cm, level)
    for bx in np.arange(-216, 217, 24):
        s.line([fpt(bx, Z_BACK), fpt(bx, far_z)], LINE, 0.7, 0.32)
    for (bx, z) in ((-96, 60), (24, 180), (120, -60), (-168, 200), (72, -120), (-24, 120)):
        s.line([fpt(bx, z), fpt(bx + 24, z)], LINE, 0.6, 0.3)
    for hh in np.arange(20, WALL_H, 20):
        s.line([P(X0, hh, Z_BACK), P(X1, hh, Z_BACK)], LINE, 0.6, 0.28)
        s.line([P(X0, hh, Z_BACK), P(X0, hh, far_z)], LINE, 0.6, 0.28)
        s.line([P(X1, hh, Z_BACK), P(X1, hh, far_z)], LINE, 0.6, 0.28)
    # the thatch's underside: three rows of short strokes along each wall plate
    rng = np.random.default_rng(seed)
    for row in range(3):
        for z in np.arange(Z_BACK, far_z, -14):
            for xs, d in ((X0, 1), (X1, -1)):
                a = P(xs + d * (8 + row * 16), WALL_H + 22 + row * 10, z)
                s.line([a, (a[0] + d * 2, a[1] - rng.uniform(3, 6))], lerp(ROOF, STRAW, 0.25), 0.7, 0.6)
    s.onto(pic)
    return {"wy": wy, "wtop": wtop, "wx0": wx0, "wx1": wx1}


def window(s):
    """The small high square window in the back wall: a flat of the rain's grey light, a bar across, a sienna frame
    and its contour."""
    Wd = WINDOW
    pts = [P(Wd["x0"], Wd["y0"], Z_BACK), P(Wd["x1"], Wd["y0"], Z_BACK), P(Wd["x1"], Wd["y1"], Z_BACK), P(Wd["x0"], Wd["y1"], Z_BACK)]
    fr = [P(Wd["x0"] - 5, Wd["y0"] - 5, Z_BACK), P(Wd["x1"] + 5, Wd["y0"] - 5, Z_BACK), P(Wd["x1"] + 5, Wd["y1"] + 5, Z_BACK), P(Wd["x0"] - 5, Wd["y1"] + 5, Z_BACK)]
    s.poly(fr, lerp(SIENNA, PRUSSIAN, 0.35), 1.0)
    s.poly(pts, lerp(PAPER, COBALT, 0.12), 1.0)
    s.line([P((Wd["x0"] + Wd["x1"]) / 2, Wd["y0"], Z_BACK), P((Wd["x0"] + Wd["x1"]) / 2, Wd["y1"], Z_BACK)], IRON, 2.0, 1.0)
    s.line(fr + [fr[0]], LINE, 0.7, 0.6)


def sacks(s, which, seed=21):
    """Charcoal bales wrapped in straw (tawara): cylinders lying along the wall, each a lit flat and a shade flat with
    the straw's weave drawn as lines along it, two rope bindings, and the round end toward the room: an ellipse of
    straw with its lines radiating to a dark plug. The contour round each."""
    rng = np.random.default_rng(seed)
    for (x0, x1, y0, y1, z0, z1) in which:
        lit = lerp(STRAW, PRUSSIAN, 0.08 + rng.uniform(0, 0.06))
        shade = shade_of(lit, 0.35)
        zc = (z0 + z1) / 2
        r = (y1 - y0) / 2
        yc = (y0 + y1) / 2
        k = CAM.scale(z0)
        # the side toward us: the cylinder's front, lit above its middle and shade below (two flats, hard edge)
        s.poly([P(x0, yc - r * 0.15, z0), P(x1, yc - r * 0.15, z0), P(x1, y1, z0), P(x0, y1, z0)], lit, 1.0)
        s.poly([P(x0, y0, z0), P(x1, y0, z0), P(x1, yc - r * 0.15, z0), P(x0, yc - r * 0.15, z0)], shade, 1.0)
        # its top, seen from above: a lighter flat
        s.poly([P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1)], lerp(lit, PAPER, 0.12), 1.0)
        # the straw's weave: lines along the bale
        for t in (0.22, 0.4, 0.58, 0.76, 0.9):
            s.line([P(x0, y0 + (y1 - y0) * t, z0), P(x1, y0 + (y1 - y0) * t, z0)], LINE, 0.6, 0.28)
        # the rope bindings: two dark bands round it
        for t in (0.28, 0.72):
            xx = x0 + (x1 - x0) * t
            s.line([P(xx, y0, z0), P(xx, y1, z0), P(xx, y1, z1)], lerp(SIENNA, PRUSSIAN, 0.55), max(1.2, 3 * k), 1.0)
        # the round end toward the middle of the room
        ex = x1 if (x0 + x1) / 2 < 0 else x0
        if abs(ex) < 195:
            cx, cy = P(ex, yc, zc)
            rr = r * CAM.scale(zc)
            s.ellipse(cx, cy, rr * 0.5, rr, lerp(lit, PRUSSIAN, 0.12), 1.0)
            for a in np.linspace(0, 2 * math.pi, 9, endpoint=False):
                s.line([(cx, cy), (cx + math.cos(a) * rr * 0.5, cy + math.sin(a) * rr)], LINE, 0.6, 0.3)
            s.ellipse(cx, cy, rr * 0.18, rr * 0.36, IRON, 1.0)
            s.line([(cx + math.cos(a) * rr * 0.5, cy + math.sin(a) * rr) for a in np.linspace(0, 2 * math.pi, 24)], LINE, 0.8, 0.6)
        s.line([P(x0, y0, z0), P(x1, y0, z0), P(x1, y1, z0), P(x0, y1, z0), P(x0, y0, z0)], LINE, 0.8, 0.6)


def mat(s, M):
    """A straw mat: one flat of straw on the floor, its weave as lines, a dark border, its contour."""
    pts = [fpt(M["x0"], M["z0"]), fpt(M["x1"], M["z0"]), fpt(M["x1"], M["z1"]), fpt(M["x0"], M["z1"])]
    s.poly(pts, lerp(STRAW, PRUSSIAN, 0.22), 1.0)
    for t in np.linspace(0.1, 0.9, 8):
        z = M["z0"] + (M["z1"] - M["z0"]) * t
        s.line([fpt(M["x0"] + 4, z), fpt(M["x1"] - 4, z)], LINE, 0.6, 0.3)
    s.poly([fpt(M["x0"], M["z0"]), fpt(M["x1"], M["z0"]), fpt(M["x1"], M["z0"] + 7), fpt(M["x0"], M["z0"] + 7)], lerp(SIENNA, PRUSSIAN, 0.45), 1.0)
    s.poly([fpt(M["x0"], M["z1"] - 7), fpt(M["x1"], M["z1"] - 7), fpt(M["x1"], M["z1"]), fpt(M["x0"], M["z1"])], lerp(SIENNA, PRUSSIAN, 0.45), 1.0)
    s.line(pts + [pts[0]], LINE, 0.9, 0.7)


def trapdoor(s, open_=False):
    """The trapdoor. Shut: a square of boards flush with the floor, a step lighter than it, three drawn board lines, an
    iron ring, its contour: Little Sister's job to find. Open: the lid standing up at the back edge (two flats: its
    underside lit by the lamp below), the dark hole, the ladder's top, and the lamplight in the hole."""
    T = TRAP
    sq = [fpt(T["x0"], T["z0"]), fpt(T["x1"], T["z0"]), fpt(T["x1"], T["z1"]), fpt(T["x0"], T["z1"])]
    if not open_:
        s.poly(sq, lerp(FLOOR, STRAW, 0.22), 1.0)
        for t in (0.25, 0.5, 0.75):
            xx = T["x0"] + (T["x1"] - T["x0"]) * t
            s.line([fpt(xx, T["z0"]), fpt(xx, T["z1"])], LINE, 0.7, 0.5)
        cx, cy = fpt((T["x0"] + T["x1"]) / 2, T["z0"] + 20)
        s.ellipse(cx, cy, 6, 3, IRON, 1.0)
        s.ellipse(cx, cy, 3.2, 1.3, lerp(FLOOR, STRAW, 0.22), 1.0)
        s.line([(cx - 6, cy), (cx + 6, cy)], LINE, 0.0, 0.0)
        s.line(sq + [sq[0]], LINE, 1.0, 0.8)
        return
    # the hole: the dark of the room below, and the lamplight in it (the lit room seen through)
    s.poly(sq, PRUSSIAN, 1.0)
    s.poly([fpt(T["x0"] + 6, T["z0"] + 6), fpt(T["x1"] - 6, T["z0"] + 6), fpt(T["x1"] - 6, T["z1"] - 6), fpt(T["x0"] + 6, T["z1"] - 6)], lerp(LAMP, SIENNA, 0.45), 1.0)
    s.poly([fpt(T["x0"] + 18, T["z0"] + 16), fpt(T["x1"] - 18, T["z0"] + 16), fpt(T["x1"] - 18, T["z1"] - 18), fpt(T["x0"] + 18, T["z1"] - 18)], LAMP, 1.0)
    # the ladder's uprights and top rung at the near edge
    for xx in (T["x0"] + 14, T["x1"] - 14):
        s.line([fpt(xx, T["z0"] + 4), P(xx, 28, T["z0"] + 4)], lerp(SIENNA, PRUSSIAN, 0.3), 3.0, 1.0)
    s.line([P(T["x0"] + 14, 24, T["z0"] + 4), P(T["x1"] - 14, 24, T["z0"] + 4)], lerp(SIENNA, PRUSSIAN, 0.3), 2.5, 1.0)
    # the lid, standing up at the back edge, leaning back a little: its underside toward us, lit from the hole
    lid = [P(T["x0"], 0, T["z1"]), P(T["x1"], 0, T["z1"]), P(T["x1"], 80, T["z1"] + 12), P(T["x0"], 80, T["z1"] + 12)]
    s.poly(lid, lerp(lerp(FLOOR, STRAW, 0.22), LAMP, 0.35), 1.0)
    for t in (0.25, 0.5, 0.75):
        xx = T["x0"] + (T["x1"] - T["x0"]) * t
        s.line([P(xx, 0, T["z1"]), P(xx, 80, T["z1"] + 12)], LINE, 0.7, 0.5)
    s.line(lid + [lid[0]], LINE, 1.0, 0.8)
    s.line(sq + [sq[0]], LINE, 1.0, 0.8)
    # the lamplight on the floor round the hole: a hard-edged flat
    s.poly([fpt(T["x0"] - 14, T["z0"] - 12), fpt(T["x1"] + 14, T["z0"] - 12), fpt(T["x1"] + 10, T["z0"]), fpt(T["x0"] - 10, T["z0"])], lerp(FLOOR, LAMP, 0.3), 1.0)


def door(s, open_=False):
    """The front door on the right wall: a sienna frame; shut, the leaf of planks (two flats: the leaf and its ledge)
    with the grey crack of light round it; open, it stands swung into the room at an angle (its inner face toward us,
    its edge showing its thickness) and the opening holds the rain outside: the paper's grey, a trunk, the ground."""
    D = DOOR
    frame_c = lerp(SIENNA, PRUSSIAN, 0.4)
    frame = [P(X1, 0, D["z0"] - 7), P(X1, 0, D["z1"] + 7), P(X1, D["h"] + 9, D["z1"] + 7), P(X1, D["h"] + 9, D["z0"] - 7)]
    s.poly(frame, frame_c, 1.0)
    if not open_:
        leaf = [P(X1 - 1, 0, D["z0"]), P(X1 - 1, 0, D["z1"]), P(X1 - 1, D["h"], D["z1"]), P(X1 - 1, D["h"], D["z0"])]
        s.poly(leaf, shade_of(WALL_R, 0.2), 1.0)
        for t in (0.25, 0.5, 0.75):
            z = D["z0"] + (D["z1"] - D["z0"]) * t
            s.line([P(X1 - 1, 2, z), P(X1 - 1, D["h"] - 2, z)], LINE, 0.6, 0.35)
        for hh in (D["h"] * 0.22, D["h"] * 0.78):
            s.poly([P(X1 - 3, hh - 5, D["z0"] + 3), P(X1 - 3, hh - 5, D["z1"] - 3), P(X1 - 3, hh + 5, D["z1"] - 3), P(X1 - 3, hh + 5, D["z0"] + 3)], lerp(WALL_R, STRAW, 0.15), 1.0)
        s.line(leaf + [leaf[0]], lerp(PAPER, COBALT, 0.2), 1.0, 0.8)          # the crack of grey light round the leaf
        s.line(frame + [frame[0]], LINE, 0.9, 0.7)
        return
    opening = [P(X1, 0, D["z0"]), P(X1, 0, D["z1"]), P(X1, D["h"], D["z1"]), P(X1, D["h"], D["z0"])]
    s.poly(opening, lerp(PAPER, COBALT, 0.18), 1.0)
    s.poly([P(X1, 0, D["z0"]), P(X1, 0, D["z1"]), P(X1, 26, D["z1"]), P(X1, 26, D["z0"])], lerp(lerp(OCHRE, SIENNA, 0.5), PRUSSIAN, 0.5), 1.0)
    s.line([P(X1, 0, D["z0"] + 30), P(X1, D["h"], D["z0"] + 26)], lerp(SIENNA, PRUSSIAN, 0.6), 9.0, 1.0)             # a cedar outside
    s.line([P(X1, 0, D["z1"] - 12), P(X1, D["h"], D["z1"] - 16)], lerp(lerp(SIENNA, PRUSSIAN, 0.6), PAPER, 0.4), 5.0, 1.0)
    s.line(frame + [frame[0]], LINE, 0.9, 0.7)
    # the leaf, swung into the room on its hinge at z0: it stands at about 70 degrees to the wall, its free edge toward
    # us and to the left; its inner face is a shade flat, its thickness (6 cm) a lit sliver along the free edge
    th = 6.0
    hx, hz = X1, D["z1"]                                            # hinged on the far jamb: it swings in on the far side, and the opening shows beside it
    ang = math.radians(70)
    fx_, fz_ = hx - math.sin(ang) * (D["z1"] - D["z0"]), hz + math.cos(ang) * (D["z1"] - D["z0"])
    face = [P(hx, 0, hz), P(fx_, 0, fz_), P(fx_, D["h"], fz_), P(hx, D["h"], hz)]
    s.poly(face, shade_of(WALL_R, 0.42), 1.0)
    edge = [P(fx_, 0, fz_), P(fx_ - math.cos(ang) * th, 0, fz_ - math.sin(ang) * th), P(fx_ - math.cos(ang) * th, D["h"], fz_ - math.sin(ang) * th), P(fx_, D["h"], fz_)]
    s.poly(edge, lerp(WALL_R, STRAW, 0.2), 1.0)
    for t in (0.25, 0.5, 0.75):
        px, pz = hx + (fx_ - hx) * t, hz + (fz_ - hz) * t
        s.line([P(px, 2, pz), P(px, D["h"] - 2, pz)], LINE, 0.6, 0.35)
    for hh in (D["h"] * 0.22, D["h"] * 0.78):
        s.line([P(hx, hh, hz), P(fx_, hh, fz_)], lerp(WALL_R, STRAW, 0.15), 3.0, 1.0)
    s.line(face + [face[0]], LINE, 1.0, 0.8)
    s.line(edge + [edge[0]], LINE, 0.8, 0.7)


def bar(s, up=False):
    """The wooden bar across the door in its two iron brackets; lifted, it leans against the wall past the door."""
    D = DOOR
    wood = lerp(OCHRE, PRUSSIAN, 0.3)
    for z in (D["z0"] - 4, D["z1"] + 4):
        s.poly([P(X1 - 1, 80, z - 3), P(X1 - 9, 80, z - 3), P(X1 - 9, 100, z - 3), P(X1 - 1, 100, z - 3)], IRON, 1.0)
    if not up:
        pts = [P(X1 - 6, 84, D["z0"] - 16), P(X1 - 6, 84, D["z1"] + 16), P(X1 - 6, 96, D["z1"] + 16), P(X1 - 6, 96, D["z0"] - 16)]
        s.poly(pts, wood, 1.0)
        s.poly([P(X1 - 6, 84, D["z0"] - 16), P(X1 - 6, 84, D["z1"] + 16), P(X1 - 11, 84, D["z1"] + 16), P(X1 - 11, 84, D["z0"] - 16)], lerp(wood, STRAW, 0.25), 1.0)
        s.line(pts + [pts[0]], LINE, 0.9, 0.7)
        return
    pts = [P(X1 - 4, 0, D["z1"] + 30), P(X1 - 14, 0, D["z1"] + 36), P(X1 - 10, 120, D["z1"] + 18), P(X1 - 2, 120, D["z1"] + 14)]
    s.poly(pts, wood, 1.0)
    s.line(pts + [pts[0]], LINE, 0.9, 0.7)


def lantern(s, lit=False):
    """A paper lantern on a hook on the left wall: unlit, the paper's grey pulled toward ochre; lit, naples yellow,
    with a flat of its warmth on the wall behind it (a hard-edged flat, not a pool)."""
    Ln = LANTERN
    cx, cy = P(X0 + 10, Ln["y"], Ln["z"])
    k = CAM.scale(Ln["z"])
    r = Ln["r"] * k
    if lit:
        s.poly([P(X0, Ln["y"] - 70, Ln["z"] + 40), P(X0, Ln["y"] - 70, Ln["z"] - 46), P(X0, Ln["y"] + 60, Ln["z"] - 46), P(X0, Ln["y"] + 60, Ln["z"] + 40)], lerp(WALL_L, LAMP, 0.35), 1.0)
    s.line([P(X0, Ln["y"] + 42, Ln["z"]), P(X0 + 10, Ln["y"] + 40, Ln["z"])], IRON, 2.0, 1.0)
    s.line([(cx, cy - r * 1.4), (cx, cy - r * 2.3)], IRON, 1.4, 1.0)
    s.ellipse(cx, cy, r * 0.85, r * 1.35, LAMP if lit else lerp(PAPER, OCHRE, 0.3), 1.0)
    for t in (-0.5, 0.0, 0.5):
        s.line([(cx - r * 0.85, cy + r * 1.3 * t), (cx + r * 0.85, cy + r * 1.3 * t)], LINE, 0.6, 0.4)
    s.ellipse(cx, cy - r * 1.35, r * 0.85, r * 0.2, IRON, 1.0)
    s.ellipse(cx, cy + r * 1.35, r * 0.85, r * 0.2, IRON, 1.0)
    s.line([(cx + math.cos(a) * r * 0.85, cy + math.sin(a) * r * 1.35) for a in np.linspace(0, 2 * math.pi, 24)], LINE, 0.8, 0.6)


def tools(s):
    """A saw and a rake on the back wall; baskets by the right wall; coils of straw rope on pegs; a broom by the door."""
    s.line([P(-60, 200, Z_BACK), P(-60, 125, Z_BACK)], lerp(PAPER, PRUSSIAN, 0.35), 3.0, 1.0)
    s.line([P(-60, 200, Z_BACK), P(-60, 228, Z_BACK)], lerp(SIENNA, PRUSSIAN, 0.3), 3.2, 1.0)
    s.line([P(-61, 200, Z_BACK), P(-61, 125, Z_BACK)], LINE, 0.6, 0.5)
    s.line([fpt(-150, 230), P(-120, 215, 244)], lerp(OCHRE, PRUSSIAN, 0.35), 2.6, 1.0)
    s.line([fpt(-168, 232), fpt(-132, 232)], lerp(SIENNA, PRUSSIAN, 0.4), 2.0, 1.0)
    for (x, z, r) in ((175, 150, 22), (150, 200, 18)):
        cx, cy = fpt(x, z)
        k = CAM.scale(z)
        body = lerp(STRAW, PRUSSIAN, 0.25)
        s.ellipse(cx, cy - r * k * 0.9, r * k, r * k * 0.9, body, 1.0)
        s.ellipse(cx + r * k * 0.5, cy - r * k * 0.9, r * k * 0.5, r * k * 0.9, shade_of(body, 0.35), 1.0)
        s.ellipse(cx, cy - r * k * 1.55, r * k * 0.95, r * k * 0.32, lerp(body, PAPER, 0.1), 1.0)
        s.ellipse(cx, cy - r * k * 1.55, r * k * 0.7, r * k * 0.2, lerp(PRUSSIAN, SIENNA, 0.3), 1.0)
        for t in (-0.5, 0.0, 0.5):
            s.line([(cx - r * k * 0.95, cy - r * k * 0.9 + r * k * 0.5 * t), (cx + r * k * 0.95, cy - r * k * 0.9 + r * k * 0.5 * t)], LINE, 0.6, 0.3)
        s.line([(cx + math.cos(a) * r * k, cy - r * k * 0.9 + math.sin(a) * r * k * 0.9) for a in np.linspace(0, math.pi, 14)], LINE, 0.8, 0.6)
    for z, h in ((150, 150), (190, 145)):
        cx, cy = P(X1 - 4, h, z)
        k = CAM.scale(z)
        s.ellipse(cx, cy, 10 * k, 14 * k, lerp(STRAW, PRUSSIAN, 0.2), 1.0)
        s.ellipse(cx, cy, 4 * k, 6 * k, WALL_R, 1.0)
        s.line([(cx + math.cos(a) * 10 * k, cy + math.sin(a) * 14 * k) for a in np.linspace(0, 2 * math.pi, 20)], LINE, 0.6, 0.5)
    s.line([fpt(190, -40), P(196, 140, -50)], lerp(OCHRE, PRUSSIAN, 0.35), 2.2, 1.0)
    s.poly([fpt(176, -42), fpt(206, -36), P(200, 30, -44), P(184, 30, -46)], lerp(STRAW, PRUSSIAN, 0.15), 1.0)


def floorgaps(s):
    """The lamplight from below between the floorboards round the trapdoor: naples yellow lines along the gaps,
    brightest nearest the trapdoor, out to about a metre."""
    T = TRAP
    for bx in np.arange(-192, 192, 24):
        if abs(bx) > 110:
            continue
        a = 0.95 - abs(bx) / 150.0
        for (z0, z1) in ((T["z0"] - 70, T["z0"] - 2), (T["z1"] + 2, T["z1"] + 70)):
            s.line([fpt(bx, z0), fpt(bx, z1)], LAMP, 1.4, a)
        if not (T["x0"] - 2 <= bx <= T["x1"] + 2):
            s.line([fpt(bx, T["z0"] - 2), fpt(bx, T["z1"] + 2)], LAMP, 1.4, a)
    for (a, b) in (((T["x0"], T["z0"]), (T["x1"], T["z0"])), ((T["x0"], T["z1"]), (T["x1"], T["z1"])), ((T["x0"], T["z0"]), (T["x0"], T["z1"])), ((T["x1"], T["z0"]), (T["x1"], T["z1"]))):
        s.line([fpt(*a), fpt(*b)], lerp(LAMP, WHITE, 0.3), 1.2, 0.95)


# ================================================================ passes
def under():
    pic = np.zeros(SHAPE + (3,), F32)
    info = shell(pic)
    s = Paper(SHAPE)
    window(s)
    tools(s)
    sacks(s, SACKS_LEFT, seed=23)
    s.onto(pic)
    # the cast shade under the sacks: a flat of the floor pulled toward prussian, hard-edged
    for (x0, x1, y0, y1, z0, z1) in SACKS + SACKS_LEFT:
        if y0 == 0:
            over(pic, lerp(FLOOR, PRUSSIAN, 0.35), mask_poly(SHAPE, [fpt(x0 - 4, z0 - 10), fpt(x1 + 4, z0 - 10), fpt(x1 + 2, z0 + 1), fpt(x0 - 2, z0 + 1)], wobble=1.0, seed=3))
    info["flats"] = pic.copy()
    return np.clip(pic, 0, 1), info


def plane(fn, *a, **kw):
    s = Paper(SHAPE)
    fn(s, *a, **kw)
    c, al = s.done()
    return c, (al > 0.5).astype(F32)


def details(pic, info):
    """The flats restated over the brushwork (the brush leaves its marks; the masses stay flat), then the keyblock's
    line: the walls' corners and plates, the window and the door's frame, 1 px near and 0.7 far."""
    pic[...] = lerp(pic, info["flats"], 0.5)
    s = Paper(SHAPE)
    far_z = Z_NEAR - 180
    ln = lambda pts, w=0.8, a=0.7: s.line(pts, LINE, w, a)
    ln([P(X0, 0, Z_BACK), P(X1, 0, Z_BACK)], 0.8, 0.75)
    ln([P(X0, WALL_H, Z_BACK), P(X1, WALL_H, Z_BACK)], 0.7, 0.6)
    ln([P(X0, 0, Z_BACK), P(X0, WALL_H, Z_BACK)], 0.7, 0.6)
    ln([P(X1, 0, Z_BACK), P(X1, WALL_H, Z_BACK)], 0.7, 0.6)
    ln([P(X0, 0, Z_BACK), fpt(X0, far_z)], 1.0, 0.8)
    ln([P(X1, 0, Z_BACK), fpt(X1, far_z)], 1.0, 0.8)
    ln([P(X0, WALL_H, Z_BACK), P(X0, WALL_H, far_z)], 0.8, 0.6)
    ln([P(X1, WALL_H, Z_BACK), P(X1, WALL_H, far_z)], 0.8, 0.6)
    s.onto(pic)
    return pic


def grade(picture):
    lum = (picture @ np.array([0.3, 0.55, 0.15], dtype=F32))[..., None]
    out = picture + 0.05 * np.clip(1 - lum / 0.4, 0, 1) * np.array([0.45, 0.6, 1.3], dtype=F32)
    return np.clip(out, 0, 1).astype(F32)


PALETTES = {}


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.012, amount=0.018):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def show(picture, name):
    Image.fromarray((np.clip(picture, 0, 1) * 255).astype(np.uint8)).save(name)


def brushed_plane(color, alpha, ground, fast, seed=4):
    if fast or not (alpha > 0.5).any():
        return color
    flat = ground.copy()
    over(flat, color, alpha)
    painted = strokes(flat, sizes=(7, 4, 2), seed=seed, density=1.6, jitter=0.025, keep=0.28)
    return lerp(painted, flat, 0.55)


def box_of(alpha):
    ys, xs = np.where(alpha > 0.5)
    return None if not len(ys) else [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


# the cut-outs back to front as the scene lays them with nobody there, and the other states
FIRST = ["lantern", "sacks", "door", "bar", "trapdoor", "mat"]
ALTS = {"lantern-lit": "lantern", "sacks-heaped": "sacks", "door-open": "door", "bar-up": "bar", "mat-aside": "mat", "trapdoor-open": "trapdoor", "floorgaps-on": None}


def layout(cut):
    Mk = {"door": fpt(150, 40), "windowIn": P(140, 90, 215), "sacks": fpt(80, 140), "mat": fpt(-5, 95), "trapdoor": fpt(80, 95),
          "lantern": fpt(-118, 150), "isuke": fpt(120, 20), "default": fpt(-60, 0), "bigsis": fpt(-70, 60), "lilsis": fpt(40, 150)}
    marks = {k: [int(round(v[0])), int(round(v[1]))] for k, v in Mk.items()}
    stands = {k: {"at": v, "grownup_px": round(grownup_px(v[1]), 1)} for k, v in marks.items()}
    stands["windowIn"] = {"at": marks["windowIn"], "grownup_px": round(160.0 * CAM.scale(215) / CAM.scale(0) * (FULL - HZ) / (FULL - HZ), 1), "scale": round(CAM.scale(215) / (160 / 175), 3),
                          "note": "on top of the sacks under the window (90 cm up): her feet on the sacks' top, drawn at this scale, sorted behind nothing (the sacks' base is nearer)"}
    T, M, Ma, D = TRAP, MAT, MAT_ASIDE, DOOR
    walk = [fpt(-190, 232), fpt(50, 232), fpt(60, 186), fpt(200, 140), fpt(200, 110), fpt(196, -40), fpt(170, -120), fpt(220, -170), fpt(-250, -170), fpt(-200, -60), fpt(-196, 140), fpt(-140, 146), fpt(-140, 190), fpt(-190, 190)]
    walk = [[int(round(a)), int(round(b))] for a, b in walk]
    quad = lambda x0, x1, z0, z1: [[int(round(v)) for v in fpt(x0, z0)], [int(round(v)) for v in fpt(x1, z0)], [int(round(v)) for v in fpt(x1, z1)], [int(round(v)) for v in fpt(x0, z1)]]
    things = [
        {"id": "sacks", "what": "charcoal sacks of straw piled against the back wall under the window (and more along the left wall): fat, bound with rope, black at the mouth", "shape": {"poly": quad(60, 210, 188, 246) + []}, "stand": marks["sacks"], "face": "N"},
        {"id": "mat", "what": "a straw mat on the floor in the middle of the room; a line of light shows at its edge when the room below is lit", "shape": {"poly": quad(M["x0"], M["x1"], M["z0"], M["z1"])}, "stand": marks["mat"], "face": "N"},
        {"id": "trapdoor", "what": "the trapdoor under the mat: boards flush with the floor and an iron ring; the way down to edo-chapel", "shape": {"poly": quad(T["x0"], T["x1"], T["z0"], T["z1"])}, "stand": marks["trapdoor"], "face": "W"},
        {"id": "floorgaps", "what": "light between the floorboards round the trapdoor, when the room below is lit (the cut-out floorgaps-on)", "shape": {"poly": quad(-110, 110, T["z0"] - 70, T["z1"] + 70)}, "stand": marks["mat"], "face": "N"},
        {"id": "door", "what": "the front door, inside: planks in a frame, the wooden bar across it", "shape": {"poly": [[int(round(v)) for v in p] for p in (P(X1, 0, D["z0"] - 6), P(X1, 0, D["z1"] + 6), P(X1, D["h"] + 8, D["z1"] + 6), P(X1, D["h"] + 8, D["z0"] - 6))]}, "stand": marks["door"], "face": "E"},
        {"id": "bar", "what": "the wooden bar across the door in its two iron brackets (across; lifted)", "shape": {"poly": [[int(round(v)) for v in p] for p in (P(X1 - 6, 78, D["z0"] - 16), P(X1 - 6, 78, D["z1"] + 16), P(X1 - 6, 102, D["z1"] + 16), P(X1 - 6, 102, D["z0"] - 16))]}, "stand": marks["door"], "face": "E"},
        {"id": "window", "what": "the small high square window in the back wall, grey with the rain's light; the sacks under it", "shape": {"poly": [[int(round(v)) for v in p] for p in (P(WINDOW["x0"] - 3, WINDOW["y0"] - 3, Z_BACK), P(WINDOW["x1"] + 3, WINDOW["y0"] - 3, Z_BACK), P(WINDOW["x1"] + 3, WINDOW["y1"] + 3, Z_BACK), P(WINDOW["x0"] - 3, WINDOW["y1"] + 3, Z_BACK))]}, "stand": marks["sacks"], "face": "N"},
        {"id": "tools", "what": "a saw and a rake on the back wall, a broom by the door", "shape": {"poly": [[int(round(v)) for v in p] for p in (P(-70, 230, Z_BACK), P(-50, 230, Z_BACK), P(-50, 120, Z_BACK), P(-70, 120, Z_BACK))]}, "stand": [int(round(fpt(-60, 190)[0])), int(round(fpt(-60, 190)[1]))], "face": "N"},
        {"id": "lantern", "what": "a paper lantern on a hook on the left wall (unlit; lit)", "shape": {"rect": [int(round(P(X0 + 10, LANTERN["y"], LANTERN["z"])[0] - 14)), int(round(P(X0 + 10, LANTERN["y"], LANTERN["z"])[1] - 24)), 28, 48]}, "stand": marks["lantern"], "face": "W"},
        {"id": "baskets", "what": "two baskets on the floor by the right wall", "shape": {"poly": quad(150, 200, 130, 220)}, "stand": [int(round(fpt(130, 170)[0])), int(round(fpt(130, 170)[1]))], "face": "E"},
        {"id": "straw", "what": "coils of straw rope on pegs on the right wall", "shape": {"poly": [[int(round(v)) for v in p] for p in (P(X1, 125, 140), P(X1, 125, 200), P(X1, 170, 200), P(X1, 170, 140))]}, "stand": [int(round(fpt(170, 170)[0])), int(round(fpt(170, 170)[1]))], "face": "E"},
        {"id": "isuke", "what": "Isuke, the constable's man, inside the door in #27 (PEOPLE-20 draws him); at marks.isuke", "shape": {"rect": [marks["isuke"][0] - 24, marks["isuke"][1] - 170, 48, 172]}, "stand": [marks["isuke"][0] - 70, marks["isuke"][1] + 4], "face": "E", "when": "edo.isukeIn"},
        {"id": "jinsuke", "what": "Jinsuke, when he is up here with the girls in #27 (PEOPLE-20 draws him); by the door", "shape": {"rect": [marks["door"][0] - 60, marks["door"][1] - 170, 48, 172]}, "stand": [marks["door"][0] - 110, marks["door"][1]], "face": "E", "when": "edo.jinsukeUp"},
    ]
    planes = []
    for name in FIRST:
        c, a = cut[name]
        base = {"lantern": "back", "sacks": [[int(round(fpt(60, 188)[0])), int(round(fpt(60, 188)[1]))], [int(round(fpt(210, 188)[0])), int(round(fpt(210, 188)[1]))]], "door": "back", "bar": "back",
                "mat": "back", "trapdoor": "back"}[name]
        entry = {"id": name, "file": f"{name}.png", "box": box_of(a)}
        if base == "back":
            entry["plane"] = "back"
        else:
            entry["base"] = base
            entry["solid"] = quad(60, 210, 186, 246)
        planes.append(entry)
    notes = {"lantern-lit": "the lantern lit: replaces lantern", "sacks-heaped": "#27: the sacks heaped over the mat (the pile under the window thinner): replaces sacks; its base is the heap's front",
             "door-open": "the door standing open inward, the rain and the path outside in the opening: replaces door", "bar-up": "the bar lifted, leaning by the door: replaces bar",
             "mat-aside": "the mat pulled aside to the left, the trapdoor bare: replaces mat", "trapdoor-open": "the trapdoor open, the ladder's top and the lamplight coming up: replaces trapdoor (show with mat-aside)",
             "floorgaps-on": "the light between the floorboards round the trapdoor, while the room below is lit: lies over the backdrop (and under the mat: list it before mat)"}
    for name, repl in ALTS.items():
        c, a = cut[name]
        entry = {"id": name, "file": f"{name}.png", "alt": repl or True, "box": box_of(a), "note": notes[name]}
        if name == "sacks-heaped":
            entry["base"] = [[int(round(fpt(-60, 58)[0])), int(round(fpt(-60, 58)[1]))], [int(round(fpt(60, 58)[0])), int(round(fpt(60, 58)[1]))]]
            entry["solid"] = quad(-62, 58, 58, 152)
        else:
            entry["plane"] = "back"
        planes.append(entry)
    return {
        "id": ID, "horizon": HZ, "full": FULL, "view": {"camera": "persp.Camera", "horizon": HZ, "full": FULL, "vanish_x": 400, "focal": FOCAL, "eye_cm": round(CAM.eye, 1), "room_cm": {"x": [X0, X1], "z": [Z_NEAR, Z_BACK], "wall_h": WALL_H}},
        "light": "dim and cool: the grey rain-light of the window down the back wall and over the sacks, a little round the door's cracks; the corners and the foreground deep blue; the lantern unlit (lantern-lit is the warm state) and the floorgaps' light (floorgaps-on) the only warm things",
        "walk": walk, "walk_note": "one outline: the floor between the sacks, clear of the baskets, the mat walkable (people stand on it: marks.mat); 14 px off the walls; its front edge where a grown-up is about 200 px tall",
        "blocked": [quad(140, 205, 125, 225), quad(-210, -140, 148, 250)],
        "planes": planes, "things": things, "marks": marks, "stands": stands,
        "exits": [{"to": "edo-cedars", "via": "door", "name": "out of the door (once it is unbarred and open)", "walkTo": marks["door"], "spawn": "door"},
                  {"to": "edo-chapel", "via": "trapdoor", "name": "down the ladder (once the trapdoor is open)", "walkTo": marks["trapdoor"], "spawn": "ladder"}],
        "cutouts": {name: box_of(a) for name, (c, a) in cut.items()},
        "fx": [{"id": "rain-roof", "type": "sound", "what": "the rain loud on the thatch: no moving thing to draw inside; a sound (ENGINE-20)"}],
        "fx_note": "nothing moves by nature inside but the rain's sound on the thatch and, through the open door (door-open), the rain outside: a `rain` mark clipped to the door's opening would serve (ENGINE-20's kind), given here as rain-door",
        "rain_door": {"type": "rain", "clip": [[int(round(v)) for v in p] for p in (P(X1, 0, D["z0"]), P(X1, 0, D["z1"]), P(X1, D["h"], D["z1"]), P(X1, D["h"], D["z0"]))], "slant": [-8, 1.0], "density": 0.0011, "when": "door-open shown"},
        "sizes": {k: round(grownup_px(v[1]), 1) for k, v in marks.items()},
    }


if __name__ == "__main__":
    t0 = time.time()
    fast = "fast" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    base, info = under()
    show(base, f"{WORK}/1-under.png")
    pic = base.copy() if fast else strokes(base, sizes=(9, 5, 2), seed=2, density=1.4, jitter=0.02, keep=0.28)
    ground = pic.copy()
    details(pic, info)
    pic = grade(pic)
    show(pic, f"{WORK}/2-back.png")
    print("back", round(time.time() - t0, 1))
    raw = {
        "lantern": plane(lantern, False), "lantern-lit": plane(lantern, True),
        "sacks": plane(sacks, SACKS, seed=21), "sacks-heaped": plane(lambda s: (sacks(s, SACKS[:3], seed=21), sacks(s, SACKS_HEAP, seed=25))),
        "door": plane(door, False), "door-open": plane(door, True),
        "bar": plane(bar, False), "bar-up": plane(bar, True),
        "mat": plane(mat, MAT), "mat-aside": plane(mat, MAT_ASIDE),
        "trapdoor": plane(trapdoor, False), "trapdoor-open": plane(trapdoor, True),
        "floorgaps-on": plane(floorgaps),
    }
    cut = {}
    for i, (name, (c, a)) in enumerate(raw.items()):
        warm = name in ("floorgaps-on", "lantern-lit", "trapdoor-open")
        cc = c if warm else brushed_plane(c, a, ground, fast, seed=20 + i)
        cut[name] = (cc if warm else grade(cc), a)
    whole = pic.copy()
    for name in ["floorgaps-on"] + FIRST:
        c, a = cut[name]
        over(whole, c, a)
    show(whole, f"{WORK}/2-all.png")
    alt = pic.copy()
    for name in ("floorgaps-on", "lantern-lit", "sacks-heaped", "door-open", "bar-up", "mat-aside", "trapdoor-open"):
        c, a = cut[name]
        over(alt, c, a)
    show(alt, f"{WORK}/2-alts.png")
    lay = layout(cut)
    with open(f"{OUT}/layout.json", "w") as fh:
        json.dump(lay, fh, indent=1)
    print("planes", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    print("back", finish(pic, f"{OUT}/back.png", 160))
    for name, (c, a) in cut.items():
        print(name, finish(c, f"{OUT}/{name}.png", 40 if name in ("floorgaps-on",) else 64, a))
    os.system(f"{sys.executable} comp.py {OUT} back " + " ".join(FIRST))
    print("done", round(time.time() - t0, 1))

"""PAINT-20E: edo-keeptop, the top floor of Himeji's keep at sunset, spring 1830 (S/briefs/out/edo-design.md, section 5,
#30 and "Hold Hands"), in the act's manner (S/work-20-paintA/style.md: flats, one contour round the silhouettes, the
blue leading; the sunset's chrome orange and geranium lake in the SKY's bands only).

    python3 edo_keeptop.py fast     the two states' under-paintings with the contours, no brush pass (seconds)
    python3 edo_keeptop.py          everything: out/edo-keeptop/ (back, lit, every cut-out in both lights, the herons'
                                    flight frames, layout.json)

ONE CAMERA (room.View): horizon 270, full 430 (the lens 175 cm up, a grown-up's eye), standing at X 380, Z 760: IN THE SOUTH BAY, looking
north into a plain room 760 wide (the west wall is X 0, the east wall X 760) and 700 deep (the north wall is Z 0; the
south wall, Z 700, is behind the lens, and so are its shutters: the player stands in its bay). A wide lens (focal 400),
so that the west and east bays, in the middle of the side walls, are both in the picture. Walls 300 high; above them
the roof's rafters rise to a ridge along the room's middle.

THE PICTURE. The north wall with its bay in the middle (two heavy shutters; open, the mountains, blue); the west wall
on the left with its bay (open, the sunset: the sky in bands, the sun on the Inland Sea, the town below); the east wall
on the right with its bay (shut: the plain at dusk when opened) and, on the panel north of it, THE HUM: a shimmer in
the air the engine draws (nothing painted). Along the north wall left of the bay, stored chests and the old lantern
(unlit: no fire is allowed up). At the front left, the stairs' opening in the floor with its rail, where everybody
arrives. Dust. Nothing else: a plain room of dark wood, high up.

TWO LIGHTS, TWO BACKDROPS. `back.png`: the shutters shut (the cut-outs' first state), the room near dark: the plaster
deep in the blue shade, the wood prussian-dark, the last of the day in thin cracks round the shutters. `lit.png`: the
west shutters open, the low sun (12 degrees up, due west) in: a broad beam lies across the floor from the room's middle
to the east wall's foot (a hard-edged flat of the sun's paper), and the whole room a step lighter and warmer (the
plaster a rose-cream: lead white toward naples with a whisper of geranium; the floor ochre wood); the hum, at a
person's height on the east wall, stays out of the direct light, so that the mirror's patch shows on it. Every cut-out
has a `-lit` twin: the same thing in that light. Light is otherwise never painted: the mirror's patch, the door and the
shimmer are the engine's (layout.json gives the numbers).

PAINT-20E."""

import json
import math
import os
import sys
import time

import numpy as np

from brush import F32, lerp, noise, blur, mask_poly, mask_ellipse, mask_line, Sheet, over, vary, grain, palette_of, to_palette, save
from room import View
from edo_keep_kit import (Room, Passes, boards, panels, post, box, finish_scene, save_rgba, to_image, ipt, col, stand_in,
                          shade_of, dark_of, tint_of, boundary, _hull, W, H, SHAPE, P, PAPER, NAPLES, OCHRE, SIENNA, PRUSSIAN,
                          COBALT, ULTRA, CERULEAN, SHADE)

ID = "edo-keeptop"
OUT = "out/edo-keeptop"
WORK = "out/edo-keeptop-work"
VIEW = dict(horizon=270, full=430, cam=(380.0, 760.0), yaw=0.0, focal=400.0)
RW, RD, RH = 760.0, 700.0, 300.0                        # the room: width (west to east), depth (north wall to south), the walls' height
RIDGE = 480.0                                           # the roof's ridge, along Z over the room's middle
WALL_T = 60.0                                           # the walls' thickness: the bays' reveals
V = View(**VIEW)

# the bays: one in the middle of each wall; (wall, u0, u1, y0, y1): u along the wall (X on the north wall, Z on a side wall)
BAYS = {
    "north": ("N", 280.0, 480.0, 90.0, 250.0),
    "west": ("W", 200.0, 400.0, 90.0, 280.0),
    "east": ("E", 200.0, 400.0, 90.0, 280.0),
}
FRONT_CHEST = (560.0, 760.0, 450.0, 580.0, 64.0)          # a stored chest near us at the right, cut by the picture's edge (the front plane)
HUM = (RW, 135.0, 130.0)                                # the hum's middle: on the east wall, a person's height, north of the east bay
STAIRWELL = (40.0, 160.0, 380.0, 520.0)                 # the stairs' opening in the floor: X0, X1, Z0, Z1 (the rail on its east and north sides)
CHESTS = [(40.0, 130.0, 0.0, 62.0, 56.0), (134.0, 250.0, 0.0, 58.0, 50.0), (60.0, 118.0, 62.0, 112.0, 40.0)]     # X0, X1, Z0, Z1, height
LANTERN = (300.0, 48.0)                                 # X, Z of the old lantern's foot (by the chests)
SUN_EL = 14.0                                           # the sun, due west, this high

# where people stand (X, Z), facing
MARKS = {
    "stairs": ((215.0, 400.0), "N"), "shinnosuke": ((262.0, 372.0), "W"),
    "west": ((48.0, 330.0), "W"), "south": ((380.0, 400.0), "N"), "north": ((380.0, 70.0), "N"), "east": ((690.0, 300.0), "E"),
    "hum": ((700.0, 170.0), "E"), "m1": ((560.0, 230.0), "E"), "m2": ((400.0, 260.0), "E"), "m3": ((240.0, 290.0), "E"),
    "farwest": ((14.0, 300.0), "E"), "mid": ((400.0, 300.0), "S"),
}
# the mirror's patch on the east wall: its diameter grows with the mirror's distance from the wall (a convex mirror):
# D(d) = 12 + 0.254 d cm (the mirror 12 cm across): a hand's breadth at `hum`, a plate, a door, a doorway at `farwest`
PATCH_A, PATCH_B = 12.0, 0.254

# the act's paints, by name
PLASTER_LIT = lerp(lerp(PAPER, NAPLES, 0.3), P("geranium-lake"), 0.06)      # the rose-cream of the lit walls
PLASTER_DARK = lerp(lerp(PAPER, PRUSSIAN, 0.2), SHADE, 0.62)                # the walls shut in: deep in the blue shade
WOOD_LIT = lerp(SIENNA, OCHRE, 0.3)
WOOD_DARK = lerp(SIENNA, PRUSSIAN, 0.55)
FLOOR_LIT = lerp(SIENNA, OCHRE, 0.35)
FLOOR_DARK = lerp(lerp(SIENNA, OCHRE, 0.2), PRUSSIAN, 0.55)
RAFTER_LIT = lerp(SIENNA, PRUSSIAN, 0.45)
RAFTER_DARK = lerp(SIENNA, PRUSSIAN, 0.78)
ROOF_LIT = lerp(SIENNA, PRUSSIAN, 0.3)
ROOF_DARK = lerp(SIENNA, PRUSSIAN, 0.68)
SHUTTER_LIT = lerp(SIENNA, PRUSSIAN, 0.25)
SHUTTER_DARK = lerp(SIENNA, PRUSSIAN, 0.62)
BEAM_C = lerp(NAPLES, PAPER, 0.45)                       # the sun on the floor: the paper warmed with naples
STEEL = lerp(PAPER, PRUSSIAN, 0.45)


def bay_pts(name, out=0.0):
    """The bay's opening as room points (its inner edge; `out` cm into the wall's thickness)."""
    wall, u0, u1, y0, y1 = BAYS[name]
    if wall == "N":
        z = -out
        return [(u0, y0, z), (u1, y0, z), (u1, y1, z), (u0, y1, z)]
    x = -out if wall == "W" else RW + out
    return [(x, y0, u0), (x, y0, u1), (x, y1, u1), (x, y1, u0)]


def bay_mask(name):
    pp = V.poly(bay_pts(name))
    return mask_poly(SHAPE, pp) if len(pp) >= 3 else np.zeros(SHAPE, F32), pp


# ---------------------------------------------------------------- the views out (the far: flats, no contour)
def bands(R, m, stops, y0, y1):
    """Horizontal bands within a mask, from row y0 (the first stop) to y1 (the last): each a flat with a soft, wobbled
    lower edge (the prints' bokashi quantised into bands)."""
    n = len(stops)
    for i, c in enumerate(stops):
        ya = y0 + (y1 - y0) * i / n
        yb = y0 + (y1 - y0) * (i + 1) / n
        if i == 0:
            ya = -10
        if i == n - 1:
            yb = 610
        band = mask_poly(SHAPE, [(-10, ya), (810, ya), (810, yb), (-10, yb)], soft=3.0 if 0 < i else 0.0, wobble=1.5 if i else 0.0, seed=70 + i)
        R.fill(m * band, c, amount=0.02, cell=90)


def view_west(R, m):
    """The sunset: the sky in bands (chrome orange and geranium lake: the act's one place for them), the sun on the
    Inland Sea, the town's roofs below."""
    hz = V.hz
    sky = [lerp(COBALT, PRUSSIAN, 0.2), COBALT, lerp(CERULEAN, COBALT, 0.3), CERULEAN, lerp(CERULEAN, PAPER, 0.6), lerp(PAPER, NAPLES, 0.5),
           lerp(NAPLES, P("chrome-orange"), 0.55), lerp(P("chrome-orange"), P("geranium-lake"), 0.5), lerp(P("geranium-lake"), PAPER, 0.3)]
    bands(R, m * (np.mgrid[0:H, 0:W][0] < hz), sky, 20, hz)
    sea = [lerp(P("geranium-lake"), COBALT, 0.5), lerp(COBALT, PAPER, 0.3), COBALT, lerp(COBALT, ULTRA, 0.5), ULTRA]
    sea_rows = (np.mgrid[0:H, 0:W][0] >= hz) & (np.mgrid[0:H, 0:W][0] < hz + 70)
    bands(R, m * sea_rows, sea, hz, hz + 70)
    # the sun: a disc of the paper on the horizon's band, and its path on the water
    sy = hz - math.tan(math.radians(SUN_EL - 3.0)) * V.F          # (drawn a little lower than the beam's angle, so that it shows in the window)
    sun = mask_ellipse(SHAPE, 30, sy, 12, 12)
    R.fill(m * sun, lerp(PAPER, NAPLES, 0.2), amount=0.0)
    path = mask_poly(SHAPE, [(24, hz + 1), (36, hz + 1), (46, hz + 40), (14, hz + 40)], soft=1.5)
    R.fill(m * path, lerp(PAPER, NAPLES, 0.5), amount=0.0, alpha=0.55)
    # the town below: rows of small roofs (flats of the shade), a few white walls, no contour
    rows = np.mgrid[0:H, 0:W][0]
    town = m * (rows >= hz + 70)
    R.fill(town, lerp(SHADE, PAPER, 0.35), amount=0.03, cell=40)
    rng = np.random.default_rng(5)
    sh = Sheet(SHAPE)
    for i in range(70):
        x = rng.uniform(0, 140)
        y = rng.uniform(hz + 72, hz + 150)
        w = rng.uniform(5, 11)
        sh.poly([(x, y), (x + w, y), (x + w + 2, y + 3), (x - 2, y + 3)], lerp(SHADE, PAPER, 0.15))
        sh.poly([(x + 1, y + 3), (x + w + 1, y + 3), (x + w + 1, y + 6), (x + 1, y + 6)], lerp(PAPER, PRUSSIAN, 0.2))
    c, a = sh.done()
    over(R.img, c, a * m)


def view_north(R, m):
    """The mountains to the north at dusk: the sky paling to the paper, two flats of blue hills, no contour."""
    hz = V.hz
    sky = [lerp(COBALT, PRUSSIAN, 0.25), COBALT, lerp(CERULEAN, COBALT, 0.4), CERULEAN, lerp(CERULEAN, PAPER, 0.55), lerp(PAPER, NAPLES, 0.25)]
    bands(R, m, sky, 30, hz + 20)
    far = mask_poly(SHAPE, [(-10, hz - 8), (120, hz - 30), (240, hz - 10), (330, hz - 36), (430, hz - 14), (520, hz - 28), (640, hz - 6), (810, hz - 18), (810, 700), (-10, 700)], soft=0.8)
    R.fill(m * far, lerp(CERULEAN, PAPER, 0.45), amount=0.02)
    near = mask_poly(SHAPE, [(-10, hz + 10), (160, hz - 4), (300, hz + 12), (400, hz + 2), (520, hz + 14), (700, hz + 6), (810, hz + 16), (810, 700), (-10, 700)], soft=0.8)
    R.fill(m * near, lerp(COBALT, PAPER, 0.35), amount=0.02)
    nearer = mask_poly(SHAPE, [(-10, hz + 40), (810, hz + 36), (810, 700), (-10, 700)])
    R.fill(m * nearer, lerp(COBALT, ULTRA, 0.4), amount=0.02)


def view_east(R, m):
    """The plain to the east at dusk: a sky going to ultramarine, the plain in two flats, a river of the paper."""
    hz = V.hz
    sky = [ULTRA, lerp(ULTRA, COBALT, 0.5), COBALT, lerp(COBALT, CERULEAN, 0.5), lerp(CERULEAN, PAPER, 0.5), lerp(PAPER, P("geranium-lake"), 0.12)]
    bands(R, m, sky, 30, hz)
    rows = np.mgrid[0:H, 0:W][0]
    R.fill(m * (rows >= hz), lerp(P("viridian"), PAPER, 0.45), amount=0.02)
    R.fill(m * (rows >= hz + 30), lerp(P("viridian"), COBALT, 0.4), amount=0.03, cell=40)
    river = mask_poly(SHAPE, [(600, hz + 12), (700, hz + 14), (760, hz + 26), (800, hz + 40), (800, hz + 48), (750, hz + 34), (690, hz + 19), (600, hz + 16)], soft=0.6)
    R.fill(m * river, lerp(PAPER, CERULEAN, 0.3), amount=0.0)


# ---------------------------------------------------------------- the room
def shell(R, lit):
    """Floor, walls with their bays open to the views, the reveals, the roof: flats in depth order."""
    plaster = PLASTER_LIT if lit else PLASTER_DARK
    wood = WOOD_LIT if lit else WOOD_DARK
    floor_c = FLOOR_LIT if lit else FLOOR_DARK
    X, Z, okf, fp = R.floor_uv()
    floor_m = okf * (X >= -5) * (X <= RW + 5) * (Z >= -5) * (Z <= RD)
    bay_m = {n: bay_mask(n) for n in BAYS}
    # the views, through the openings (painted first: the walls are laid round them)
    view_west(R, bay_m["west"][0])
    view_north(R, bay_m["north"][0])
    view_east(R, bay_m["east"][0])
    # the walls, their plaster cut round the openings; the posts flank the bays
    u, v, okw, fpw = R.wall_uv("Z", 0.0)
    back_m = okw * (u >= 0) * (u <= RW) * (v >= 0) * (v <= RH)
    ul, vl, okl, fpl = R.wall_uv("X", 0.0)
    left_m = okl * (ul >= 0) * (ul <= RD) * (vl >= 0) * (vl <= RH)
    ur, vr, okr, fpr = R.wall_uv("X", RW)
    right_m = okr * (ur >= 0) * (ur <= RD) * (vr >= 0) * (vr <= RH)
    # in the lit room the east wall faces the sun (the brightest), the north wall a step into the shade, the west wall
    # (its inner face turned from the sun) the most
    k_n, k_w, k_e = (0.18, 0.35, 0.0) if lit else (0.0, 0.12, 0.0)
    panels(R, back_m, "Z", 0.0, shade_of(plaster, k_n), wood, dark_of(wood, 0.2), RW, RH, post_at=[0.0, 258.0, 480.0, RW - 22], post_w=22.0,
           sill_h=26.0, lintel_h=22.0, nageshi=(204.0, 218.0), seed=4, alpha=0.6, cut=bay_m["north"][0])
    panels(R, left_m, "X", 0.0, shade_of(plaster, k_w), wood, dark_of(wood, 0.2), RD, RH, post_at=[0.0, 178.0, 400.0, 600.0], post_w=22.0,
           sill_h=26.0, lintel_h=22.0, nageshi=(204.0, 218.0), seed=5, alpha=0.55, cut=bay_m["west"][0])
    panels(R, right_m, "X", RW, shade_of(plaster, k_e), wood, dark_of(wood, 0.2), RD, RH, post_at=[0.0, 178.0, 400.0, 600.0], post_w=22.0,
           sill_h=26.0, lintel_h=22.0, nageshi=(204.0, 218.0), seed=6, alpha=0.55, cut=bay_m["east"][0])
    # the reveals: the sill's top and the far jamb's face of each bay (the wall is 60 thick), the sun's paper on the
    # west bay's sill when the room is lit
    for name, (wall, u0, u1, y0, y1) in BAYS.items():
        if wall == "N":
            sill = [(u0, y0, 0), (u1, y0, 0), (u1, y0, -WALL_T), (u0, y0, -WALL_T)]
            jl = [(u0, y0, 0), (u0, y0, -WALL_T), (u0, y1, -WALL_T), (u0, y1, 0)]
            jr = [(u1, y0, 0), (u1, y0, -WALL_T), (u1, y1, -WALL_T), (u1, y1, 0)]
            faces = [(sill, lerp(plaster, PAPER, 0.1)), (jl, shade_of(plaster, 0.3)), (jr, shade_of(plaster, 0.3))]
        else:
            x = 0.0 if wall == "W" else RW
            o = -WALL_T if wall == "W" else RW + WALL_T
            sill = [(x, y0, u0), (x, y0, u1), (o, y0, u1), (o, y0, u0)]
            jf = [(x, y0, u0), (o, y0, u0), (o, y1, u0), (x, y1, u0)]
            sc = BEAM_C if (lit and wall == "W") else lerp(plaster, PAPER, 0.1)
            faces = [(sill, sc), (jf, shade_of(plaster, 0.3) if not (lit and wall == "W") else lerp(plaster, PAPER, 0.2))]
        for pts, c in faces:
            mk = R.flat(pts, c, amount=0.02)
            R.thing(mk, 0.55)
    # the gable of the north wall above the lintel, and the roof: two slopes to the ridge, the rafters as flats
    gable = R.flat([(0, RH, 0), (RW, RH, 0), (RW / 2, RIDGE, 0)], shade_of(plaster, 0.25 + k_n), amount=0.03)
    R.thing(gable, 0.5)
    roof_c = ROOF_LIT if lit else ROOF_DARK
    raft_c = RAFTER_LIT if lit else RAFTER_DARK
    for (xa, xb) in ((0.0, RW / 2), (RW, RW / 2)):
        slope = R.flat([(xa, RH, 0), (xb, RIDGE, 0), (xb, RIDGE, RD), (xa, RH, RD)], shade_of(roof_c, 0.25 if xa == 0 else 0.0), amount=0.03)
        R.thing(slope, 0.45)
        z = 30.0
        while z < RD:
            rf = R.flat([(xa, RH - 2, z), (xb, RIDGE - 2, z), (xb, RIDGE - 2, z + 14), (xa, RH - 2, z + 14)], raft_c, amount=0.03)
            R.thing(rf, 0.45)
            z += 92.0
        # a purlin along the slope's middle
        pm = R.flat([((xa + xb) / 2 - 12, (RH + RIDGE) / 2 - 16, 0), ((xa + xb) / 2 + 12, (RH + RIDGE) / 2 - 16, 0), ((xa + xb) / 2 + 12, (RH + RIDGE) / 2 - 16, RD), ((xa + xb) / 2 - 12, (RH + RIDGE) / 2 - 16, RD)], dark_of(raft_c, 0.15), amount=0.03)
        R.thing(pm, 0.45)
    ridge = R.flat([(RW / 2 - 14, RIDGE - 22, 0), (RW / 2 + 14, RIDGE - 22, 0), (RW / 2 + 14, RIDGE - 22, RD), (RW / 2 - 14, RIDGE - 22, RD)], dark_of(raft_c, 0.2), amount=0.03)
    R.thing(ridge, 0.5)
    # the floor: boards running toward us; the beam on it when lit (a hard-edged flat)
    boards(R, floor_m, floor_c, along="Z", width=30.0, offset=10.0, seed=3, line_alpha=0.3)
    beam = None
    if lit:
        wall, u0, u1, y0, y1 = BAYS["west"]
        t = math.tan(math.radians(SUN_EL))
        x_near = y0 / t                                 # where the sill's ray meets the floor
        x_far = min(RW, y1 / t)
        pts = [(x_near, 0.5, u0), (x_far, 0.5, u0), (x_far, 0.5, u1), (x_near, 0.5, u1)]
        beam = R.flat(pts, BEAM_C, amount=0.02) * floor_m
        # and up the east wall's foot, as high as the head's ray reaches
        y_wall = y1 - t * RW
        if y_wall > 0:
            R.flat([(RW, 0, u0), (RW, 0, u1), (RW, y_wall, u1), (RW, y_wall, u0)], BEAM_C, amount=0.02)
        R.things.append((beam, np.zeros(SHAPE, F32), PRUSSIAN, 0.0))         # (the beam covers the floor's joints under it)
        beam_pts = [[min(799, max(0, q[0])), min(599, max(0, q[1]))] for q in (ipt(V.pt(*p)) for p in pts)]
    else:
        beam_pts = None
    # the stairs' opening in the floor: a dark hole with the stair's top treads showing
    X0, X1, Z0, Z1 = STAIRWELL
    hole = R.flat([(X0, 0.2, Z0), (X1, 0.2, Z0), (X1, 0.2, Z1), (X0, 0.2, Z1)], dark_of(SIENNA, 0.85), amount=0.02)
    R.thing(hole, 0.6)
    for i in range(3):
        y = -12 - i * 27
        z0 = Z0 + 14 + i * 22
        tr = R.flat([(X0 + 4, y, z0), (X1 - 4, y, z0), (X1 - 4, y, z0 + 22), (X0 + 4, y, z0 + 22)], shade_of(wood, 0.2 + 0.15 * i), amount=0.03)
        R.thing(tr, 0.5)
    return floor_m, bay_m, beam_pts


def shutters(R, name, open_, lit, grp):
    """A bay's two heavy shutters: shut, a pair of dark leaves filling the opening at the inner face of the wall (the
    last of the day in the cracks round them); open, the leaves swung inward to lie flat against the wall either side."""
    wall, u0, u1, y0, y1 = BAYS[name]
    c = SHUTTER_LIT if lit else SHUTTER_DARK
    leaf_w = (u1 - u0) / 2
    m = np.zeros(SHAPE, F32)

    def quad(a, b, ya, yb, off):
        if wall == "N":
            return [(a, ya, off), (b, ya, off), (b, yb, off), (a, yb, off)]
        x = off if wall == "W" else RW - off
        return [(x, ya, a), (x, ya, b), (x, yb, b), (x, yb, a)]
    if not open_:
        for (a, b) in ((u0, u0 + leaf_w), (u0 + leaf_w, u1)):
            mk = R.flat(quad(a + 1.5, b - 1.5, y0 + 1.5, y1 - 1.5, 2.0), c, grp, amount=0.03)
            m = np.maximum(m, mk)
            R.thing(mk, 0.7)
            # the battens across each leaf: two flats
            for yy in (y0 + 24, y1 - 32):
                mb = R.flat(quad(a + 4, b - 4, yy, yy + 9, 4.0), dark_of(c, 0.25), grp, amount=0.03)
                m = np.maximum(m, mb)
                R.thing(mb, 0.5)
        # the cracks of light: the paper, thin, round the leaves and down their meeting
        ln = np.zeros(SHAPE, F32)
        for pts in (quad(u0 + 1.5, u1 - 1.5, y0 + 1.5, y1 - 1.5, 2.0),):
            pp = V.poly(pts)
            if len(pp) >= 3:
                ln = np.maximum(ln, boundary(mask_poly(SHAPE, pp)))
        r = V.line(quad(u0 + leaf_w, u0 + leaf_w, y0 + 1.5, y1 - 1.5, 2.0)[0], quad(u0 + leaf_w, u0 + leaf_w, y0 + 1.5, y1 - 1.5, 2.0)[2])
        if r:
            ln = np.maximum(ln, mask_line(SHAPE, [r[0], r[1]], 1.0))
        R.things.append((np.zeros(SHAPE, F32), ln * np.maximum(m, blur(m, 1.0) > 0.1), lerp(PAPER, NAPLES, 0.4), 0.55 if not lit else 0.4))
    else:
        for (a, b) in ((u0 - leaf_w, u0), (u1, u1 + leaf_w)):
            mk = R.flat(quad(a, b, y0, y1, 6.0), c, grp, amount=0.03)
            m = np.maximum(m, mk)
            R.thing(mk, 0.7)
            for yy in (y0 + 24, y1 - 32):
                mb = R.flat(quad(a + 3, b - 3, yy, yy + 9, 8.0), dark_of(c, 0.25), grp, amount=0.03)
                m = np.maximum(m, mb)
                R.thing(mb, 0.5)
    return m


def front(R, lit, grp="front"):
    """The front plane: a stored chest near us at the right, cut by the picture's edge."""
    X0, X1, Z0, Z1, h = FRONT_CHEST
    c = lerp(SIENNA, OCHRE, 0.15) if lit else lerp(SIENNA, PRUSSIAN, 0.55)
    m = box(R, X0, X1, 0, h, Z0, Z1, c, grp=grp, alpha=0.85, lit=("top",), shade_k=0.35, wobble=0.6)
    mb = R.flat([(X0 + 8, h + 0.5, Z0 + 10), (X1, h + 0.5, Z0 + 10), (X1, h + 0.5, Z0 + 20), (X0 + 8, h + 0.5, Z0 + 20)], dark_of(SIENNA, 0.8), grp, amount=0.02)
    return np.maximum(m, mb)


def rail(R, lit, grp="rail"):
    """The rail round the stairs' opening: posts at its corners and a top rail, on its east and north sides."""
    X0, X1, Z0, Z1 = STAIRWELL
    c = WOOD_LIT if lit else WOOD_DARK
    m = np.zeros(SHAPE, F32)
    for (x, z) in ((X1, Z0), (X1, Z1), (X0, Z0)):
        m = np.maximum(m, box(R, x - 5, x + 5, 0, 92, z - 5, z + 5, c, grp=grp, alpha=0.85, lit=("top", "right") if lit else ("top",), shade_k=0.3))
    m = np.maximum(m, box(R, X1 - 4, X1 + 4, 84, 92, Z0, Z1, c, grp=grp, alpha=0.85, lit=("top",), shade_k=0.3))
    m = np.maximum(m, box(R, X0, X1, 84, 92, Z0 - 4, Z0 + 4, c, grp=grp, alpha=0.85, lit=("top",), shade_k=0.3))
    return m, [ipt(V.pt(X1 + 5, 0, Z1 + 5)), ipt(V.pt(X1 + 5, 0, Z0 - 5))]


def chests(R, lit, grp="chests"):
    c = lerp(SIENNA, OCHRE, 0.2) if lit else lerp(SIENNA, PRUSSIAN, 0.5)
    m = np.zeros(SHAPE, F32)
    base = 0
    for (X0, X1, Z0, Z1, h) in sorted(CHESTS, key=lambda t: t[2]):
        m = np.maximum(m, box(R, X0, X1, 0, h, Z0, Z1, c, grp=grp, alpha=0.7, lit=("top", "right") if lit else ("top",), shade_k=0.35, wobble=0.6))
        # a band of dark iron across the lid: a flat
        mb = R.flat([(X0 + 6, h + 0.5, Z0 + 8), (X1 - 6, h + 0.5, Z0 + 8), (X1 - 6, h + 0.5, Z0 + 16), (X0 + 6, h + 0.5, Z0 + 16)], dark_of(SIENNA, 0.8), grp, amount=0.02)
        m = np.maximum(m, mb)
        base = max(base, V.pt(X0, 0, Z1)[1])
    return m, int(round(base))


def lantern(R, lit, grp="lantern"):
    """An old wooden lantern standing on the floor by the chests: a box of paper on four legs, a little roof; unlit."""
    X, Z = LANTERN
    c = WOOD_LIT if lit else WOOD_DARK
    pc = lerp(PAPER, PRUSSIAN, 0.18) if lit else lerp(lerp(PAPER, PRUSSIAN, 0.3), SHADE, 0.5)
    m = np.zeros(SHAPE, F32)
    for (x, z) in ((X - 11, Z - 11), (X + 11, Z - 11), (X - 11, Z + 11), (X + 11, Z + 11)):
        m = np.maximum(m, box(R, x - 2, x + 2, 0, 30, z - 2, z + 2, c, grp=grp, alpha=0.6, lit=("top",), shade_k=0.3))
    m = np.maximum(m, box(R, X - 13, X + 13, 30, 66, Z - 13, Z + 13, pc, grp=grp, alpha=0.75, lit=("right", "top") if lit else ("top",), shade_k=0.3))
    m = np.maximum(m, box(R, X - 17, X + 17, 66, 74, Z - 17, Z + 17, c, grp=grp, alpha=0.75, lit=("top",), shade_k=0.3))
    return m, int(round(V.pt(X, 0, Z + 13)[1]))


# ---------------------------------------------------------------- the herons' flight frames
def heron_frames(folder):
    """A heron going past the windows: three small frames (glide, wings up, wings down), 56 x 36, foot [28, 24], facing
    east: a grey-blue silhouette with the neck folded in flight and the legs trailing, as a print would cut it."""
    out = []
    for i, wing in enumerate((0, -1, 1)):
        sh = Sheet((36, 56))
        body = lerp(PAPER, PRUSSIAN, 0.55)
        dark = lerp(PAPER, PRUSSIAN, 0.8)
        sh.poly([(14, 20), (26, 16), (40, 17), (46, 20), (38, 24), (26, 25)], body)              # the body
        sh.line([(40, 18), (47, 15), (52, 16)], dark, 2.2)                                        # the neck folded, the head
        sh.line([(52, 16), (56, 15)], lerp(NAPLES, OCHRE, 0.5), 1.4)                               # the bill
        sh.line([(14, 21), (4, 23)], dark, 1.6)                                                    # the legs trailing
        if wing == 0:
            sh.poly([(22, 18), (36, 17), (44, 10), (30, 11), (18, 15)], dark)                     # wings level
            sh.poly([(22, 22), (36, 22), (44, 29), (30, 29), (18, 25)], body)
        elif wing < 0:
            sh.poly([(24, 18), (34, 17), (40, 4), (30, 2), (22, 10)], dark)                       # wings up
        else:
            sh.poly([(24, 21), (34, 22), (40, 34), (30, 35), (22, 28)], dark)                     # wings down
        c, a = sh.done()
        rgba = np.dstack([c, (a >= 0.5).astype(F32)])
        name = f"heron-fly-{i + 1}.png"
        from PIL import Image
        Image.fromarray(np.clip(np.round(rgba * 255), 0, 255).astype(np.uint8), "RGBA").save(os.path.join(folder, name), optimize=True)
        out.append(name)
    return out


# ---------------------------------------------------------------- the whole picture
CUTS = ["rail", "chests", "lantern", "northshutter", "eastshutter", "westshutter", "front"]


def render(lit, include=("rail", "chests", "lantern", "front"), shut=("north", "east", "west"), open_=(), seed=1):
    R = Room(V, seed=seed + (7 if lit else 0), base=dark_of(SIENNA, 0.85))
    info = {}
    floor_m, bay_m, beam_pts = shell(R, lit)
    info["beam"] = beam_pts
    info["bays"] = {n: [ipt(p) for p in pp] for n, (mk, pp) in bay_m.items()}
    if "chests" in include:
        info["chests"] = chests(R, lit)[1]
    if "lantern" in include:
        info["lantern"] = lantern(R, lit)[1]
    for n in ("north", "west", "east"):
        if n in shut:
            shutters(R, n, False, lit, n + "shutter")
        elif n in open_:
            shutters(R, n, True, lit, n + "shutter")
    if "rail" in include:
        info["rail"] = rail(R, lit)[1]
    if "front" in include:
        front(R, lit)
    return R, info


PASS = Passes(seed=13)


def paint(R, fast):
    pic = R.img.copy()
    if not fast:
        pic = PASS.paint(pic, keep=0.28)
    return np.clip(R.contours(pic), 0, 1)


def layout(info_dark, info_lit):
    pt = lambda X, Z: [min(799, max(0, ipt(V.pt(X, 0, Z))[0])), min(599, max(0, ipt(V.pt(X, 0, Z))[1]))]
    marks = {k: {"at": pt(*xz), "face": f} for k, (xz, f) in MARKS.items()}
    X0, X1, Z0, Z1 = STAIRWELL
    walk = [pt(24, 20), pt(RW - 24, 20), pt(RW - 24, 400), pt(X1 + 30, 400), pt(X1 + 30, Z0 - 20), pt(24, Z0 - 20)]
    walk = [pt(10, 40), pt(RW - 24, 40), pt(RW - 24, 410), pt(X1 + 30, 410), pt(X1 + 30, Z0 - 20), pt(10, Z0 - 20)]
    blocked = [{"id": "chests", "poly": [pt(30, 0), pt(260, 0), pt(260, 120), pt(30, 120)]},
               {"id": "lantern", "poly": [pt(LANTERN[0] - 20, LANTERN[1] - 20), pt(LANTERN[0] + 20, LANTERN[1] - 20), pt(LANTERN[0] + 20, LANTERN[1] + 20), pt(LANTERN[0] - 20, LANTERN[1] + 20)]},
               {"id": "stairwell", "poly": [pt(X0 - 10, Z0 - 10), pt(X1 + 10, Z0 - 10), pt(X1 + 10, Z1 + 10), pt(X0 - 10, Z1 + 10)]}]
    # the hum and the door: the east wall's panel north of the east bay
    hx, hy = V.pt(*HUM)
    hd = V.depth(HUM[0], HUM[2])
    scale = V.F / hd                                     # px per cm on the wall at the hum
    wide = (abs(HUM[0] - V.cam_x) / hd)                  # a length along the wall beside a height, seen from here
    keep_x = sorted([int(round(V.pt(RW, 0, BAYS["east"][1] - 24)[0])), int(round(V.pt(RW, 0, 24)[0]))])
    patch = {}
    for k in ("hum", "m1", "m2", "m3", "farwest"):
        (mx, mz), _ = MARKS[k]
        d = abs(HUM[0] - mx)                             # the mirror's distance from the wall, cm (held before her, at the wall's foot's line)
        D = PATCH_A + PATCH_B * d
        patch[k] = {"distance_cm": round(d), "diameter_cm": round(D), "radius_px": round(D / 2 * scale, 1),
                    "distance_px": round(math.hypot(marks[k]["at"][0] - hx, marks[k]["at"][1] - hy), 1)}
    things = {
        "hum": {"at": ipt((hx, hy)), "poly": [ipt((hx + 22 * math.cos(a) * wide, hy + 22 * math.sin(a))) for a in np.linspace(0, 2 * math.pi, 12, endpoint=False)],
                "size_px": [round(44 * wide), 44], "stand": marks["hum"]["at"], "note": "a shimmer in the air before this panel: the engine's; nothing painted"},
        "lantern": {"stand": marks["north"]["at"]}, "floor": {"stand": marks["mid"]["at"]},
        "rafters": {"poly": [ipt(V.pt(0, RH, 0)), ipt(V.pt(RW, RH, 0)), [800, 0], [0, 0]]},
        "view": {"poly": info_dark["bays"]["west"], "stand": marks["west"]["at"], "note": "through the west bay, open: the town and the Inland Sea under the sun"},
        "herons": {"poly": info_dark["bays"]["west"], "note": "going past the west bay, clipped to its opening"},
        "shinnosuke": {"stand": marks["shinnosuke"]["at"]},
        "southshutter": {"poly": [[0, 584], [799, 584], [799, 599], [0, 599]], "stand": marks["south"]["at"],
                         "note": "at the player's back: the camera stands in the south bay; its shutters are not in the picture (a look only)"},
    }
    for n in ("north", "west", "east"):
        things[n + "shutter"] = {"poly": info_dark["bays"][n], "stand": marks[n]["at"], "states": ["shut", "open"]}
    planes = [
        {"id": "rail", "src": "rail.png", "base": info_dark["rail"], "lit": "rail-lit.png"},
        {"id": "chests", "src": "chests.png", "base": info_dark["chests"], "lit": "chests-lit.png"},
        {"id": "lantern", "src": "lantern.png", "base": info_dark["lantern"], "lit": "lantern-lit.png"},
        {"id": "northshutter", "src": "northshutter.png", "plane": "back", "open": "northshutter-open.png", "lit": "northshutter-lit.png", "open_lit": "northshutter-open-lit.png"},
        {"id": "eastshutter", "src": "eastshutter.png", "plane": "back", "open": "eastshutter-open.png", "lit": "eastshutter-lit.png", "open_lit": "eastshutter-open-lit.png"},
        {"id": "westshutter", "src": "westshutter.png", "plane": "back", "open": "westshutter-open.png", "open_lit": "westshutter-open-lit.png"},
        {"id": "front", "src": "front.png", "plane": "front", "lit": "front-lit.png"},
    ]
    out = {
        "scene": ID, "size": [W, H], "view": VIEW, "horizon": VIEW["horizon"], "full": VIEW["full"],
        "room_cm": {"X": [0, RW], "Z": [0, RD], "H": RH, "ridge": RIDGE, "note": "west wall X 0, east wall X 760, north wall Z 0; the camera in the south bay at (380, 760), the lens 175 cm up"},
        "walk": walk, "blocked": blocked, "marks": marks,
        "stands": {k: {"at": v["at"], "grownup_px": int(round(V.person(*MARKS[k][0])[2] * 160 / 175))} for k, v in marks.items()},
        "planes": planes,
        "states": {"shut": "back.png with the planes in their first state (the three shutters shut): the room near dark",
                   "lit": "lit.png (an alt covering the whole stage) with westshutter-open-lit and every other plane's -lit twin: the west shutters open, the sun in",
                   "note": "a shutter opened while the room is dark takes its -open file; in the lit room its -open-lit file"},
        "things": things,
        "sun": {"elevation_deg": SUN_EL, "from": "due west, through the west bay", "beam_floor": info_lit["beam"],
                "note": "the beam lies on the floor from the room's middle (X 361 cm) to the east wall and climbs its foot to 91 cm (the shut east shutters' lowest board); the hum, 135 cm up, is out of the direct light"},
        "hum": {"at": ipt((hx, hy)), "room_cm": list(HUM), "scale_px_per_cm": round(scale, 3)},
        "door": {"type": "portal", "at": ipt((hx, hy)), "r": round(100 * scale), "wide": round(wide, 2), "keep": keep_x, "base": int(round(V.pt(RW, 0, HUM[2])[1])),
                 "under": ["eastshutter"], "note": "a doorway 200 cm tall at the hum, as PORTAL-9's open: r is half its height in px wide open; wide squeezes it to the wall's foreshortening"},
        "patch": {"rule": "D(d) = 12 + 0.254 d (cm): the mirror 12 cm across, d its distance from the east wall", "at_marks": patch,
                  "sizes_for_engine": [[patch["hum"]["distance_px"], patch["hum"]["radius_px"]], [patch["farwest"]["distance_px"], patch["farwest"]["radius_px"]]],
                  "note": "sizes_for_engine: [distance of the holder's mark from the hum in px, the patch's radius in px] at `hum` and at `farwest`; the marks m1, m2, m3 step between"},
        "fx": [
            {"id": "door", "type": "portal", "at": ipt((hx, hy)), "r": round(100 * scale), "wide": round(wide, 2), "keep": keep_x, "base": int(round(V.pt(RW, 0, HUM[2])[1])), "pale": "#fff4d8", "light": True},
            {"id": "mirror", "type": "mirror", "target": ipt((hx, hy)), "holder": "mom", "door": "door", "image": "cross",
             "sizes": [[patch["hum"]["distance_px"], patch["hum"]["radius_px"]], [patch["farwest"]["distance_px"], patch["farwest"]["radius_px"]]],
             "reach": [int(round(V.pt(0, 0, 420)[0])), int(round(V.pt(0, 0, 20)[1])), 800, int(round(V.pt(0, 0, 420)[1] - V.pt(0, 0, 20)[1]))], "when": "edo.lit (the west shutters open)"},
            {"id": "herons", "type": "birds", "lanes": [[[-40, 250], [220, 236]], [[200, 262], [-40, 272]]], "every": [18, 40], "group": [1, 2], "speed": 55, "scale": 0.9,
             "clip": [info_dark["bays"]["west"]], "frames": {"foot": [28, 24], "face": "E", "glide": ["heron-fly-1.png"], "flap": ["heron-fly-2.png", "heron-fly-3.png"]},
             "when": "the west shutters open", "note": "the flyers kept inside the west bay's opening (ENGINE-20's clip); the north bay could take the same lanes mirrored"},
            {"id": "dust", "type": "shimmer", "poly": [[180, 240], [620, 240], [800, 520], [0, 520]], "count": 40, "size": 2, "flow": [1, 0], "life": 3.0, "color": "#f6eed8", "opacity": 0.25,
             "note": "PROPOSED: motes in the lit room's beam (shown only when lit)"},
        ],
        "notes": "Two backdrops: back.png (shut, near dark) and lit.png (the west shutters open, the sun in: an alt over the whole stage); each cut-out has a -lit twin for the lit room, and each shutter -open and -open-lit. The south bay is behind the camera. The hum and the door are the engine's at the numbers under `hum`, `door` and `patch`. PAINT-20E.",
    }
    return out


def main():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    fast = mode == "fast"
    # the two lights, each: the room with everything (its first state), and the room bare (the backdrop under them)
    Rd, info_d = render(False)
    pic_d = paint(Rd, fast)
    Rl, info_l = render(True, shut=("north", "east"), open_=("west",))
    pic_l = paint(Rl, fast)
    if fast:
        to_image(pic_d).save(f"{WORK}/fast-shut.png")
        to_image(pic_l).save(f"{WORK}/fast-lit.png")
        json.dump(layout(info_d, info_l), open(f"{WORK}/layout-fast.json", "w"), indent=1)
        print("fast", round(time.time() - t0, 1), "s")
        return
    Rd0, _ = render(False, include=(), shut=())
    Rl0, _ = render(True, include=(), shut=())
    back = paint(Rd0, fast)
    litp = paint(Rl0, fast)
    pictures = {"back": (back, None), "lit": (litp, None)}
    hard = lambda m: (m >= 0.5).astype(F32)
    for name in ("rail", "chests", "lantern", "front"):
        pictures[name] = (pic_d, hard(Rd.masks[name]))
        pictures[name + "-lit"] = (pic_l, hard(Rl.masks[name]))
    for n in ("north", "east"):
        pictures[n + "shutter"] = (pic_d, hard(Rd.masks[n + "shutter"]))
        pictures[n + "shutter-lit"] = (pic_l, hard(Rl.masks[n + "shutter"]))
    pictures["westshutter"] = (pic_d, hard(Rd.masks["westshutter"]))
    pictures["westshutter-open-lit"] = (pic_l, hard(Rl.masks["westshutter"]))
    # the open shutters in the dark room (each alone, the others shut), and in the lit room (north, east open)
    for n in ("north", "east", "west"):
        Ro, _ = render(False, shut=tuple(x for x in ("north", "east", "west") if x != n), open_=(n,))
        po = paint(Ro, fast)
        pictures[n + "shutter-open"] = (po, hard(Ro.masks[n + "shutter"]))
    for n in ("north", "east"):
        Ro, _ = render(True, shut=tuple(x for x in ("north", "east") if x != n), open_=(n, "west"))
        po = paint(Ro, fast)
        pictures[n + "shutter-open-lit"] = (po, hard(Ro.masks[n + "shutter"]))
    finish_scene(OUT, pictures, colors=160, seed=9)
    heron_frames(OUT)
    json.dump(layout(info_d, info_l), open(f"{OUT}/layout.json", "w"), indent=1)
    to_image(pic_d).save(f"{WORK}/composed-shut.png")
    to_image(pic_l).save(f"{WORK}/composed-lit.png")
    print("full", round(time.time() - t0, 1), "s:", len(pictures), "pictures + 3 heron frames, layout.json")


if __name__ == "__main__":
    main()

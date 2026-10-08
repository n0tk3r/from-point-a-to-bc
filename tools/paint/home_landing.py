"""home-landing: the upstairs landing of the family's house, at night, seen from out in the air over the
living room, level with the landing, looking along it toward the top of the stairs at the far left.

ONE CAMERA (home_landing_model.VIEW, not to be changed): horizon 135, full 322, lens at X 775, Z 760, 204 cm
above the landing's floor, turned 40 degrees to the left. Lines along the landing run to a vanishing point
far off to the left (-267, 135); lines running out toward us (the stair wall, the ceiling beams, the boards
of the living-room floor) run to one just off the right edge (870, 135). Every surface is found per pixel
through that camera (home_landing_kit.Tracer), painted in its own centimetres, and lit from where the lamps
stand; flat things (doors, the notice, the window, photographs, the rug) are painted face-on and laid on
their walls through the same camera.

MEASUREMENTS are the house's own centimetres (room.py): X along the back wall, Y up FROM THE LANDING'S FLOOR
(the living room's floor is at Y = -285), Z out from the back wall toward us.

LIGHT (it is night, 9:40 p.m.):
  * the lamp on the hall table (warm), against the back wall between the girls' door and the study door:
    the pool of light people stand in; the far end of the landing by the Son's door falls away cool;
  * the moon (pale blue), through the tall stair window in the left wall: it falls DOWN AND TO THE RIGHT
    (and a little toward us, as in the living room's picture), down the treads of the stairs and in the
    window's own shape, with the tree's branches in it, on the floor at their foot;
  * the glow from below (warm): the lamp on the piano, the lit kitchen doorway and the wedge of light it
    throws across the floor, and from under us, out of the picture, the pendant over the dinner table and
    Dad's reading lamp.
THREE TONES: dark = the ceiling toward us, the stair wall, the corners; middle = the lit floor of the
  living room, the papered walls away from the lamp; light = the lamplit wall, doors and woodwork where
  people stand, the white balusters, the kitchen doorway, the moon.

THE HOUSE IS THE LIVING ROOM'S HOUSE: sea-green striped paper over white boarded woodwork, oak floors, a red
runner with a brass edge, white balusters under a dark handrail with newel posts at X 108, 276, 444, 612, a
quilt over the rail, a brass hanging light: all as the living room's picture has them (its model and lamp
places are read from home_living_room_model.py when this is run).

WHERE THINGS ARE (X along the landing): the stairs come up at the far left (X 0..108); the Son's bag and shoes
150..180; the Son's door 190..275; photographs and the hamper 293..387; the girls' door 400..485 (NOW Little
Sister's); the hall table, lamp, key bowl and the trip countdown chart 500..595; the attic hatch in the ceiling
479..557, its cord hanging by the girls' door (NOW open at 514..590, the ladder down from it to X 627, its sides
at Z 50 and 108); Dad's study door 610..695 with his notice on it.
Below (heights lowered by 285): bookcase, kitchen doorway, the framed print, the piano with its lamp, the
front door; the rug; the staircase with its panelled side, the low cupboard door ajar and Dad's cable.
NOT IN THE PICTURE, because this camera cannot see them: the dinner table and Dad's armchair (they are almost
under the lens); the clock and the sampler (hidden by the landing's own edge).

Pictures: back.png (everything but the railing and the ladder), ladder.png (the attic ladder, with a base),
rail.png (front plane: the whole railing, the newel posts, the banister of the stairs, the quilt, and the unlit
hanging light out in the room), study-open.png (the study door standing open, and the light it lets out, laid
exactly over the shut one).

THE SECOND PASS (briefs/ROOMS-2.md, C): the middle door is now LITTLE SISTER's alone (one name-plate buried in
chicken stickers, her crayon hen, her sign BEWARE OF CHICKENS), and the attic hatch is OPEN with the folding loft
ladder let down from it (its own cut-out, ladder.png, with Big Sister's card on it: THE RETREAT). The landing is
painted twice: THEN (the picture as first delivered, which this script still reproduces to the byte, and from
which rail.png and study-open.png are made unchanged) and NOW. back.png is THEN with only the changes laid in: the
new door, the ceiling round the old and the new hatch, the lamp and key bowl moved a little left, taken from NOW;
the ladder's shadows and its feet on the floor laid onto THEN's own brushwork as a ratio of light. Every other
pixel keeps its old palette index; the palette gains eight colors (160). out/home-landing-2-changed.png shows
which pixels changed.

    python3 home_landing.py          everything (about fifty seconds)
    python3 home_landing.py fast     NOW only, no brush pass, coarser: for composing

The people check (the game's server on port 8765): those behind the ladder first, then the ladder over them,
then the rest and the rail:
    python3 people_on.py out/home-landing/back.png 135 322 "mom|631|306|270|walk(0.3)" plans/landing-people-pass1.png out/home-landing/ladder.png
    python3 people_on.py plans/landing-people-pass1.png 135 322 "lilsis|433|279|0;mom|544|288|180;bigsis|718|325|270;lilsis|651|331|90|walk(0.6)" out/home-landing-people.png out/home-landing/rail.png
"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
import home_landing_model as M
try:                                                          # the same house: the living room's own measurements, as they are now
    import home_living_room_model as LR
except Exception:                                             # (if that file cannot be read, what it held when this was written is used)
    LR = None
from home_landing_kit import *
import home_landing_things as TH
from room import View

W, H = 800, 600
SHAPE = (H, W)
V = View(**M.VIEW)
G = 285.0                                     # the living room's floor is this far below the landing's
OUT = "out/home-landing"


def low(y):
    """A height above the living-room floor -> a height in this picture's measurements."""
    return y - G


# ---------------------------------------------------------------- the house, in centimetres
STAIR = dict(X=(0.0, 108.0), z_foot=575.0, z_top=175.0, steps=16)
RISE, GOING = G / 16, 25.0
SON, GIRLS, STUDY = (190.0, 275.0), (400.0, 485.0), (610.0, 695.0)
DOOR_H = 205.0
CEIL = 275.0
WINDOW = dict(Z=(240.0, 400.0), Y=(-55.0, 215.0))
BEAMS = [78.0, 208.0, 338.0, 468.0, 598.0, 728.0]            # middles of the ceiling beams (they run out toward us)
BEAM_DEEP = 10.0                                              # shallow, or each would hide the ceiling beyond it from here
HATCH = (479.0, 557.0, 44.0, 122.0)                           # X0, X1, Z0, Z1 in the ceiling, over the hall table
TABLE = (505.0, 590.0, 78.0, 2.0, 32.0)                       # X0, X1, height, Z0, Z1
HAMPER = (297.0, 345.0, 62.0, 3.0, 40.0)
RUNNER = (22.0, 790.0, 52.0, 132.0)                           # X0, X1, Z0, Z1 on the landing floor
SIGN = (613.5, 691.5, 104.0, 168.0)                           # Dad's notice on the study door: X0, X1, Y0, Y1
BAG = (148.0, 178.0)                                          # the Son's school bag on its peg: X0, X1 on the back wall
CHART = (500.0, 595.0, 124.0, 162.0)                          # the long strip of paper pinned up over the hall table

# ---------------------------------------------------------------- the picture THEN and the picture NOW
# THEN is the landing as it was first painted: the girls' shared door, the attic hatch shut, its cord hanging.
# NOW the middle door is Little Sister's alone, and the hatch (35 cm farther along the ceiling, so that its ladder
# hides neither the lamp nor a door handle nor Dad's notice) is open, with the attic ladder let down to the floor.
# rail.png and study-open.png are still made from THEN, and so is every pixel of back.png that the two changes do
# not touch: the game's scene file is fitted to that picture.
LILSIS = GIRLS                                                # the middle door: the same door, hers alone now
HATCH2 = (514.0, 590.0, 44.0, 122.0)                          # the open hatch: X0, X1, Z0, Z1 in the ceiling (the beam at X 591..605 is its right side)
# The ladder runs ALONG the landing and rises to the left, so that from here it is seen from its side: its top at
# the hatch's left end under the ceiling (X 516), its feet on the floor at X 627, just in front of the study door's
# left edge; its two sides at Z 50 and Z 108. People pass it IN FRONT (between its feet and the rail) and stand
# BEHIND it under its high end, at the hall table. (A way behind its feet too would need the landing deeper than it
# is: the game keeps everyone 12 px and 5 px clear of blocked ground, and the floor here is only ~30 px deep, so
# a ladder standing out from the wall far enough to pass behind it cuts the landing in two.) It folds in four
# lengths (`joints`: cm down its front edge); the top length lies on the hatch's own door, hanging down with it.
LADDER = dict(hinge=516.0, foot=627.0, z=(50.0, 108.0), step=23.5, treads=11, deep=7.4, thick=2.6, tread=8.0, tthick=2.4,
              door=76.0, joints=(76.0, 152.0, 228.0))
CARD_WH = (50.0, 29.0)                                         # Big Sister's card (home_landing_things.retreat_card), hung on the near side
CARD_AT = 172.0                                                # at eye height: the height of its middle
LADDER_GROUND = [(590.0, 40.0), (630.0, 40.0), (630.0, 110.0), (590.0, 110.0)]   # the ground under its feet and its low end, back to the wall's side of the walk (X, Z)
LADDER_BASE = ((516.0, 108.0), (627.0, 108.0))                # its base: the line on the floor under its near side, out to its feet (X, Z)
THEN = dict(name="then", ladder=False, lamp=(527.0, 18.0), bowl=(553.0, 21.0))
NOW = dict(name="now", ladder=True, lamp=(515.0, 18.0), bowl=(537.0, 23.0))        # (the lamp and the key bowl stand 12 and 16 cm farther left on the
#                                                                                     table, clear of the ladder; the lamp's LIGHT is where it was)
HATCH_GLOW = 0.50                                              # the warm breath of The Retreat's light on the rim of the open hatch
ATTIC_LADDER = 0.80                                            # how strongly that light falls on the ladder's top rungs


def ladder_frame(L=None):
    """The ladder's own measure. -> (length of its front edge, the way down it (dX, dY), the way out of its face
    toward the climber (nX, nY), at(s, back) -> (X, Y): s cm down the front edge from the top, `back` cm behind it,
    Xf(Y): the front edge's X at height Y, Xb(Y): the back edge's X at height Y)."""
    L = L or LADDER
    h, f, deep = L["hinge"], L["foot"], L["deep"]
    Ls = math.hypot(f - h, CEIL)
    dX, dY = (f - h) / Ls, -CEIL / Ls
    nX, nY = CEIL / Ls, (f - h) / Ls

    def at(s, back=0.0):
        return h + dX * s - nX * back, CEIL + dY * s - nY * back

    def Xf(Y):
        return f - (f - h) * Y / CEIL

    def Xb(Y):
        return f - (f - h) * (Y + nY * deep) / CEIL - nX * deep
    return Ls, (dX, dY), (nX, nY), at, Xf, Xb


def ladder_boxes(L=None, bands=34):
    """The ladder as boxes, for the shadows it throws (its sides in short steps, each tread, the hatch's door)."""
    L = L or LADDER
    Ls, (dX, dY), (nX, nY), at, Xf, Xb = ladder_frame(L)
    z0, z1, th = L["z"][0], L["z"][1], L["thick"]
    out = []
    for i in range(bands):
        ya, yb = CEIL * i / bands, CEIL * (i + 1) / bands
        xs = (Xf(ya), Xf(yb), Xb(ya), Xb(yb))
        for za, zb in ((z0, z0 + th), (z1 - th, z1)):
            out.append((min(xs), max(xs), ya, yb, za, zb))
    for k in range(1, L["treads"] + 1):
        yk = k * L["step"]
        xn = Xf(yk) - 0.8
        out.append((xn - L["tread"], xn, yk - L["tthick"], yk, z0 + th, z1 - th))
    hz0, hz1 = HATCH2[2], HATCH2[3]
    n = 8
    for i in range(n):                                       # the hatch's door, hanging behind the top length
        (xa, ya), (xb, yb) = at(L["door"] * i / n, L["deep"]), at(L["door"] * (i + 1) / n, L["deep"] + 2.0)
        out.append((min(xa, xb) - 1.0, max(xa, xb) + 1.0, min(ya, yb), max(ya, yb), hz0 + 2.0, hz1 - 2.0))
    return out

# ---------------------------------------------------------------- the living room below: read from its own model
def lr_box(name, otherwise):
    """(X0, X1, Y0, Y1, Z0, Z1) of a thing in the living room's model, heights above ITS floor."""
    return next((tuple(float(q) for q in b[1:]) for b in getattr(LR, "BOXES", []) if b[0] == name), otherwise)


def lr_flat(name, otherwise):
    """(u0, u1, v0, v1) of a flat thing on a wall of the living room."""
    return next((tuple(float(q) for q in f[2:]) for f in getattr(LR, "FLATS", []) if f[0] == name), otherwise)


def lr_light(name, otherwise):
    L = getattr(LR, "LIGHTS", {}).get(name)
    return tuple(float(q) for q in L) if L else otherwise


LR_PIANO = lr_box("piano", (468, 624, 0, 128, 0, 62))
LR_STOOL = lr_box("stool", (512, 580, 0, 48, 80, 114))
LR_BOOKS = lr_box("books", (118, 250, 0, 218, 0, 34))
_rug = lr_box("rug", (250, 560, 0, 1, 230, 470))
RUG = (_rug[0], _rug[1], _rug[4], _rug[5])
LR_FRAME = lr_flat("frame", (414, 458, 150, 212))
LR_CLOCK = lr_flat("clock", (525, 560, 170, 205))
LR_DOOR = lr_flat("door", (658, 762, 0, 214))
LR_PHOTOS = lr_flat("photos", (420, 560, 150, 215))
_k = lr_flat("kitchen", (268, 400, 0, 225))
KITCHEN = (_k[0], _k[1], low(_k[3]))                          # the doorway: X0, X1, top

# ---------------------------------------------------------------- the lamps
WARM = np.array([1.00, 0.75, 0.44], dtype=F32)
WARM2 = np.array([1.00, 0.66, 0.36], dtype=F32)
MOON = np.array([0.46, 0.64, 1.00], dtype=F32)
SKY = np.array([0.30, 0.42, 0.72], dtype=F32)
HALL = (527.0, 124.0, 18.0)                                   # the bulb of the hall-table lamp (the living room has it at 527, 18)
_pl = lr_light("piano", (LR_PIANO[1] - 30.0, LR_PIANO[3] + 34.0, 26.0))
PIANO_LAMP = (min(max(_pl[0], LR_PIANO[0] + 14), LR_PIANO[1] - 14), 24.0)       # where the lamp stands on the piano: X, Z
PIANO = (PIANO_LAMP[0], low(LR_PIANO[3] + 32.0), PIANO_LAMP[1])                # its bulb
KLAMP = ((KITCHEN[0] + KITCHEN[1]) / 2, low(214.0), -64.0)    # a light left on in the kitchen, just inside its doorway
_pd = lr_light("pendant", (610.0, 166.0, 677.0))
TABLE_GLOW = (_pd[0], low(95.0), _pd[2])                      # the lit cloth of the dinner table, below us and out of the picture
_rd = lr_light("reading", (378.0, 150.0, 773.0))
READING = (_rd[0], low(_rd[1]), _rd[2])                       # Dad's reading lamp, out of the picture
LIGHT_AT = (338.0, -28.0, 440.0)                              # the hanging light out in the room: the middle of its ring
def moon_way():
    """The way to the moon from inside the room, as the living room's painter has it (read from his script as
    text, never run), so that the moonlight lies on the same boards in both pictures."""
    try:
        import re
        text = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "home_living_room_room.py")).read()
        way = tuple(float(q) for q in re.search(r"^MOON_WAY\s*=\s*\(([^)]*)\)", text, re.M).group(1).split(","))
        if len(way) == 3 and way[0] < 0 < way[1]:
            return way
    except Exception:
        pass
    return (-0.445, 0.847, -0.289)


TO_MOON = np.array(moon_way()) / np.linalg.norm(moon_way())


def stair_painting():
    """Where the living room hangs its landscape on the stair wall: (Z0, Z1, Y0, Y1 above its floor), read from
    that painter's script as text; None if it has none."""
    try:
        import re
        text = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "home_living_room_room.py")).read()
        part = text[text.index("def painting("):]
        got = re.search(r"z0, z1, y0, y1 = ([0-9.]+), ([0-9.]+), ([0-9.]+), ([0-9.]+)", part[:900])
        return tuple(float(q) for q in got.groups())
    except Exception:
        return (452.0, 548.0, 338.0, 408.0)


def stair_line(Z):
    """The height of the line through the noses of the steps, at Z."""
    return np.clip(-G + G * (STAIR["z_foot"] - Z) / (STAIR["z_foot"] - STAIR["z_top"]), -G, 0.0)


def step_top(i):
    return -G + RISE * (i + 1)


# ---------------------------------------------------------------- what the house is made of (as in the living room's picture)
WOODWORK = np.array([0.80, 0.76, 0.63], dtype=F32)             # painted woodwork: doors, dado, stair side, balusters
PAPER = np.array([0.44, 0.57, 0.53], dtype=F32)                # the wallpaper: a grey sea-green, striped
CREAM = np.array([0.86, 0.79, 0.62], dtype=F32)
OAK = np.array([0.64, 0.44, 0.24], dtype=F32)
DARKWOOD = np.array([0.30, 0.17, 0.10], dtype=F32)
BRASS = np.array([0.80, 0.60, 0.24], dtype=F32)
RED = np.array([0.52, 0.13, 0.11], dtype=F32)
NAVY = np.array([0.13, 0.18, 0.34], dtype=F32)
PITCH = RISE / GOING


def stair_base(Z):
    """Where the woodwork of the stair wall starts at Z: it climbs with the steps (heights in this picture's measure)."""
    return -G + np.clip((STAIR["z_foot"] - Z) * PITCH + RISE, 0.0, G)


# ====================================================================== the room, as surfaces
def build(tr, open_study=False, state=None):
    state = state or THEN
    T = {}

    def tag(name, color, mat="flat"):
        T[name] = tr.new(name, color, mat)
        return T[name]

    # ---- the shell
    ceil = tag("ceiling", "#cfc4ae", "ceiling")
    if state["ladder"]:                                      # the hatch stands open: a hole, and the sides of the way up
        hx0, hx1, hz0, hz1 = HATCH2
        tr.rect("Y", CEIL, -40, hx0, -400, 1400, ceil)
        tr.rect("Y", CEIL, hx1, 900, -400, 1400, ceil)
        tr.rect("Y", CEIL, hx0, hx1, -400, hz0, ceil)
        tr.rect("Y", CEIL, hx0, hx1, hz1, 1400, ceil)
        shaft = tag("shaft", "#b8875a")                       # the sides of the way up: the joists' wood, lit from above
        tr.rect("X", hx0, CEIL, CEIL + 44, hz0, hz1, shaft)
        tr.rect("X", hx1, CEIL, CEIL + 44, hz0, hz1, shaft)
        tr.rect("Z", hz0, hx0, hx1, CEIL, CEIL + 44, shaft)
        tr.rect("Z", hz1, hx0, hx1, CEIL, CEIL + 44, shaft)
        tr.rect("Y", CEIL + 44, hx0, hx1, hz0, hz1, tag("attic", "#f2c79a"))     # and The Retreat beyond, rose and amber
    else:
        tr.rect("Y", CEIL, -40, 900, -400, 1400, ceil)
    up = tag("wall", "#d6bd8c", "wall")
    if open_study:
        tr.rect("Z", 0, -40, STUDY[0], 0, CEIL, up)
        tr.rect("Z", 0, STUDY[1], 900, 0, CEIL, up)
        tr.rect("Z", 0, STUDY[0], STUDY[1], DOOR_H, CEIL, up)
    else:
        tr.rect("Z", 0, -40, 900, 0, CEIL, up)
    dn = tag("wall-below", "#d6bd8c", "wall")
    tr.rect("Z", 0, -40, KITCHEN[0], -G, 0, dn)
    tr.rect("Z", 0, KITCHEN[1], 900, -G, 0, dn)
    tr.rect("Z", 0, KITCHEN[0], KITCHEN[1], KITCHEN[2], 0, dn)
    tr.rect("X", 0, -G, CEIL, 0, 1400, tag("wall-left", "#d6bd8c", "wall-left"))
    tr.rect("Y", -G, 0, 900, 0, 1400, tag("floor-below", "#84583a", "floor-below"))

    # ---- the landing: a slab across the back wall, and the head of the stairs
    tr.box(108, 900, -18, 0, 0, 175, tag("slab", "#b8ad98"), top=tag("landing", "#94643c", "landing"), front=tag("fascia", "#ccc2a1", "fascia"))
    trim = tag("trim", WOODWORK * 0.95)
    tr.box(108, 900, -22, -17, 175, 177.6, trim)                                           # a moulding under the edge of the landing
    tr.box(108, 115, -62, -22, 150, 177.6, trim)                                           # and a bracket where it meets the staircase
    tr.box(0, 108, -18, 0, 0, 175, T["slab"], top=T["landing"])
    side = tag("stair-side", WOODWORK, "stair-side")
    tr.box(0, 108, -G, -18, 0, 175, side)
    tread, riser = tag("tread", OAK, "tread"), tag("riser", WOODWORK, "riser")
    for i in range(STAIR["steps"]):
        z1 = STAIR["z_foot"] - GOING * i
        tr.box(0, 108, -G, step_top(i), z1 - GOING, z1, side, top=tread, front=riser)

    # ---- left on the stairs to go up: two library books (the rabbit sitting above them is drawn by hand, in details)
    i = 2
    z1 = STAIR["z_foot"] - GOING * i
    tr.box(5, 27, step_top(i), step_top(i) + 3.2, z1 - 21, z1 - 4, tag("book1", "#2f5a8a"), occl=False)
    tr.box(7, 26, step_top(i) + 3.2, step_top(i) + 6.0, z1 - 20, z1 - 6, tag("book2", "#c8a23a"), occl=False)

    # ---- the ceiling beams
    beam = tag("beam", "#6a4c34", "beam")
    for bx in BEAMS:
        tr.box(bx - 7, bx + 7, CEIL - BEAM_DEEP, CEIL + 1, 0, 1400, beam)

    # ---- on the landing: the hall table and the hamper
    x0, x1, th, z0, z1 = TABLE
    wood = tag("table", "#74482c", "wood")
    tr.box(x0 - 1.5, x1 + 1.5, th - 3.5, th, z0 - 1, z1 + 1.5, wood, top=tag("table-top", "#8a5a36", "wood"))
    tr.box(x0 + 2, x1 - 2, th - 17, th - 3.5, z0 + 2, z1 - 1.5, wood, front=tag("table-front", "#7c4e30", "drawer"))
    for lx in (x0 + 2, x1 - 6):
        for lz in (z0 + 2, z1 - 5.5):
            tr.box(lx, lx + 4, 0, th - 17, lz, lz + 4, wood)
    tr.box(x0 + 4, x1 - 4, 14, 16.5, z0 + 3, z1 - 3, wood)                                 # a low shelf for shoes
    hx0, hx1, hh, hz0, hz1 = HAMPER
    wick = tag("hamper", "#b08a52", "wicker")
    tr.box(hx0, hx1, 0, hh - 4, hz0, hz1, wick)
    tr.box(hx0 - 1.5, hx1 + 1.5, hh - 4, hh, hz0 - 1, hz1 + 1.5, tag("hamper-lid", "#c09a5e", "wicker"))
    tr.box(hx0 + 6, hx1 - 8, hh, hh + 9, hz0 + 5, hz1 - 6, tag("towels", "#d8dfe6", "towels"))               # folded washing left on it
    tr.box(572, 588, th, th + 2.2, 6, 26, tag("post", "#e9e2cf"))                           # the day's post, and a book, on the hall table
    tr.box(574, 586, th + 2.2, th + 5.0, 8, 25, tag("book", "#7a2e2a"))
    # the Son's things, left where he dropped them: his school bag on a peg, his shoes under it
    tr.box(BAG[0], BAG[1], 62, 104, 0, 12, tag("bag", "#c8482c", "bag"))
    tr.box(BAG[0] + 12, BAG[0] + 18, 104, 112, 0, 5, tag("peg", "#6a4428"))
    tr.box(BAG[0] - 4, BAG[0] + 7, 0, 9, 4, 30, tag("shoe", "#e8e4da", "shoe"))
    tr.box(BAG[0] + 11, BAG[0] + 22, 0, 9, 8, 34, T["shoe"])

    # ---- behind the study door, when it stands open
    if open_study:
        tr.rect("Y", 0, 300, 900, -700, 0, tag("study-floor", "#8a5c36", "study-floor"))
        tr.rect("Z", -620, 100, 900, 0, 330, tag("study-far", "#cbb894", "study-wall"))
        tr.rect("X", STUDY[0], 0, DOOR_H, -12, 0, tag("study-jamb", "#e6dcc8"))
        tr.box(STUDY[0] + 0.5, STUDY[0] + 4.5, 1, DOOR_H - 1, -85, -1, tag("study-leaf", "#e6dcc8", "leaf"))
        tr.box(572, 720, 0, 76, -335, -255, tag("study-desk", "#7a4c2c", "wood"), top=tag("study-desk-top", "#8c5a36", "wood"))
        tr.box(578, 584, 0, 72, -262, -256, T["study-desk"])
        tr.box(640, 694, 0, 44, -206, -158, tag("study-box", "#b08a5a", "carton"))
        tr.box(652, 700, 0, 34, -122, -84, tag("study-cooler", "#3f78b4", "cooler"), top=tag("study-cooler-lid", "#e8e2d2"))

    # ---- the living room below (home_living_room_model.py, heights lowered by 285)
    bx0, bx1, _, btop, bz0, bz1 = LR_BOOKS
    tr.box(bx0, bx1, -G, low(btop), bz0, bz1, tag("bookcase", "#6e3420", "wood"), front=tag("books", "#4a2616", "books"))
    px0, px1, _, ptop, pz0, pz1 = LR_PIANO
    pw = tag("piano", "#532a1a", "wood")
    tr.box(px0, px1, -G, low(ptop), pz0, pz0 + 36, pw, front=tag("piano-front", "#5c2f1c", "piano-front"), top=tag("piano-top", "#6a3822", "wood"))
    tr.box(px0, px1, low(60), low(72), pz0 + 36, pz1, pw, top=tag("keys", "#ece4d0", "keys"), front=tag("key-slip", "#532a1a", "wood"))
    for cx in (px0, px1 - 6):
        tr.box(cx, cx + 6, low(60), low(86), pz0 + 36, pz1 + 1, pw)                        # the cheeks at each end of the keys
        tr.box(cx + 1, cx + 5, -G, low(60), pz1 - 7, pz1 - 2, pw)                           # and the legs under them
    tr.box(px0 + 44, px1 - 44, -G, low(6), pz0 + 36, pz0 + 46, pw)                         # the pedal board
    sx0, sx1, _, stop_, sz0, sz1 = LR_STOOL
    tr.box(sx0, sx1, low(stop_ - 8), low(stop_), sz0, sz1, tag("stool", "#7a2a2a"), top=tag("stool-top", "#8f3030", "cushion"))
    for lx in (sx0 + 2, sx1 - 6):
        for lz in (sz0 + 2, sz1 - 6):
            tr.box(lx, lx + 4, -G, low(stop_ - 8), lz, lz + 4, pw)
    # the kitchen beyond its doorway
    tr.rect("Y", -G, -100, 520, -360, 0, tag("kitchen-floor", "#e2d8ba", "kitchen-floor"))
    tr.rect("Z", -360, -100, 620, -G, 0, tag("kitchen-wall", "#edcc80", "kitchen-wall"))
    tr.rect("X", KITCHEN[0], -G, KITCHEN[2], -15, 0, tag("jamb", WOODWORK))
    tr.box(196, 252, -G, low(172), -150, -92, tag("fridge", "#e9e6da", "fridge"))
    tr.box(252, 430, -G, low(88), -300, -236, tag("counter", "#d6ccb2", "counter"), top=tag("counter-top", "#7c8c84", "counter-top"))
    tr.box(252, 430, low(88), low(90.5), -302, -233, T["counter-top"])
    return T


# ====================================================================== what each surface is made of
def wall_paper(u, y, fp, top=None, seed=0.0, dado=True):
    """A papered wall over painted woodwork, in its own centimetres: u along it, y up from where its woodwork
    starts. Sea-green paper in nine-centimetre stripes with a pale pin line and a sprig; narrow white boards with
    a bead below a rail at 96; a skirting; with `top` (the wall's height) a white cornice under the ceiling."""
    n = len(u)
    i, f = repeat(u, 9.0)
    even = np.mod(i, 2) < 0.5
    col = PAPER[None, :] * np.where(even, 1.0, 0.84)[:, None]
    pin = line_cover(np.minimum(f, 9.0 - f), 0.28, fp)
    col = lerp(col, CREAM[None, :] * 0.8, (pin * 0.5)[:, None])
    j, g = repeat(y, 13.0)
    sprig = (hash2(i, j, 4.0) > 0.5) & even
    dd = np.hypot(f - 4.5, g - 6.5)
    col = lerp(col, CREAM[None, :] * 0.9, (np.clip(1 - dd / 1.7, 0, 1) * sprig * np.clip(1.5 - fp, 0, 1) * 0.55)[:, None])
    col = col * (0.93 + 0.14 * hash2(i, 0.0, seed + 13.0))[:, None]
    if dado:
        wb = WOODWORK[None, :] * (0.95 + 0.08 * hash2(i, 0.0, 17.0))[:, None]
        wb = wb * (1 - 0.32 * line_cover(np.minimum(f, 9.0 - f), 0.45, fp))[:, None]
        low_ = y < 96.0
        col[low_] = wb[low_]
        rail = (y > 92.0) & (y < 100.0)
        col[rail] = WOODWORK * 1.06
        col = col * (1 - 0.42 * line_cover(y - 91.2, 0.9, fp))[:, None]
        col = col * (1 - 0.25 * line_cover(y - 100.4, 0.5, fp))[:, None]
        skirt = y < 14.0
        col[skirt] = WOODWORK * 0.98
        col = col * (1 - 0.40 * line_cover(y - 14.5, 0.7, fp))[:, None]
    if top is not None:
        c = y > top - 22.0
        col[c] = WOODWORK[None, :] * (0.92 + 0.10 * np.sin((y[c] - (top - 22.0)) / 22.0 * 9.0))[:, None]
        col = col * (1 - 0.40 * line_cover(y - (top - 22.6), 0.8, fp))[:, None]
        col = col * (1 - 0.28 * np.exp(-np.maximum(top - y, 0) / 9.0))[:, None]
    if dado:
        col = col * (1 - 0.28 * np.exp(-np.maximum(y, 0) / 9.0))[:, None]                   # darker where wall meets floor
    return col.astype(F32)


def mat_wall(X, Y, Z, fp, alb):
    up = Y >= 0
    out = np.empty_like(alb)
    if up.any():
        out[up] = wall_paper(X[up], Y[up], fp[up], top=CEIL, seed=1.0)
    if (~up).any():
        out[~up] = wall_paper(X[~up], Y[~up] + G, fp[~up], top=None, seed=1.0)
    return out


def mat_wall_left(X, Y, Z, fp, alb):
    base = np.where(Z < STAIR["z_top"], 0.0, stair_base(Z))   # the woodwork climbs with the stairs
    col = wall_paper(Z, Y - base, fp, top=None, seed=2.0)
    two = Z >= STAIR["z_top"]                                 # a picture rail where the upstairs floor is, on the two-storey wall
    pr = two & (Y > -4.0) & (Y < 5.0) & (Y - base > 100.0)
    col[pr] = WOODWORK * 1.02
    col = col * (1 - 0.35 * line_cover(Y + 5.0, 0.8, fp) * two * (Y - base > 100.0))[:, None]
    c = Y > CEIL - 22.0
    col[c] = WOODWORK[None, :] * (0.92 + 0.10 * np.sin((Y[c] - (CEIL - 22.0)) / 22.0 * 9.0))[:, None]
    col = col * (1 - 0.40 * line_cover(Y - (CEIL - 22.6), 0.8, fp))[:, None]
    return col.astype(F32)


def mat_floor_below(X, Y, Z, fp, alb):
    tone, joint = boards(Z, X, fp, 12.0, 175.0, seed=4.0)
    col = OAK[None, :] * (0.80 + 0.40 * tone)[:, None]
    grain = hash2(np.floor(X / 1.6), np.floor(Z / 46.0), 7.0)
    col = col * (0.95 + 0.1 * grain[:, None] * np.clip(1.6 - fp, 0, 1)[:, None])
    return lerp(col, rgb("#2c1a10"), (joint * 0.72)[:, None])


def runner_colors(a, c, la, lc, fp):
    """A red runner with a dark blue border: `a` cm along it and `c` across it, of a strip `la` long, `lc` wide."""
    edge = np.minimum(c, lc - c)
    end = np.minimum(a, la - a)
    e = np.minimum(edge, end * 1.0)
    col = np.empty((len(a), 3), dtype=F32)
    col[:] = RED * 1.0
    i, f = repeat(a + 6.0, 30.0)
    lozenge = np.clip(1.25 - (np.abs(f - 15.0) / 6.5 + np.abs(c - lc / 2) / 9.0), 0, 1) * np.clip(1.5 - fp * 0.5, 0, 1)
    col = lerp(col, rgb("#c9a05a"), (np.clip(lozenge * 2.2, 0, 1) * 0.85)[:, None])
    col = lerp(col, rgb("#2a3157"), (np.clip(lozenge * 2.2 - 1.2, 0, 1))[:, None])
    dots = np.clip(1.3 - np.hypot(f - 0.0, np.abs(c - lc / 2) - 15.0) / 1.8, 0, 1) + np.clip(1.3 - np.hypot(f - 30.0, np.abs(c - lc / 2) - 15.0) / 1.8, 0, 1)
    col = lerp(col, rgb("#c9a05a"), (np.clip(dots, 0, 1) * np.clip(1.3 - fp * 0.7, 0, 1) * 0.8)[:, None])
    col[e < 9.0] = NAVY * 1.1
    col[e < 6.0] = BRASS * 0.7                                # the brass-coloured edge the living room sees from below
    col[e < 1.2] = RED * 0.7
    return col


def mat_landing(X, Y, Z, fp, alb):
    tone, joint = boards(X, Z, fp, 12.0, 210.0, seed=5.0)
    col = OAK[None, :] * 0.95 * (0.80 + 0.40 * tone)[:, None]
    col = lerp(col, rgb("#3a2414"), (joint * 0.7)[:, None])
    x0, x1, z0, z1 = RUNNER
    on = (X > x0) & (X < x1) & (Z > z0) & (Z < z1)
    if on.any():
        col[on] = runner_colors(X[on] - x0, Z[on] - z0, x1 - x0, z1 - z0, fp[on])
    turn = (X > 21.0) & (X < 87.0) & (Z >= z1 - 9.0)       # the stair carpet comes up onto the landing and meets the runner
    if turn.any():
        col[turn] = stair_runner(X[turn], Z[turn], col[turn], fp[turn])
    nose = Z > 171.5                                        # the white nosing along the open edge
    col[nose & (X > 108)] = WOODWORK * 1.05
    return col


def mat_fascia(X, Y, Z, fp, alb):
    col = np.empty_like(alb)
    col[:] = WOODWORK
    col = col * (1 - 0.30 * line_cover(Y + 5.0, 0.7, fp))[:, None]
    col = col * (1 - 0.22 * line_cover(Y + 13.0, 0.6, fp))[:, None]
    return col


def stair_runner(X, along, col, fp):
    """The stair carpet: a deep red runner with a brass and navy border down the middle of the steps."""
    d = np.abs(X - 54.0)
    red = RED[None, :] * (0.92 + 0.2 * hash2(np.floor(X / 6.0), np.floor(along / 7.0), 8.0))[:, None]
    out = np.where((d < 33.0)[:, None], red, col)
    out = np.where(((d > 25.5) & (d < 30.0))[:, None], BRASS[None, :] * 0.8, out)
    out = np.where(((d > 30.0) & (d < 33.0))[:, None], NAVY[None, :], out)
    dia = np.abs(np.mod(X - 54.0, 12.0) - 6.0) + np.abs(np.mod(along, 12.5) - 6.25)
    out = np.where(((d < 22.0) & (dia < 2.2) & (fp < 1.4))[:, None], BRASS[None, :] * 0.62, out)
    return out.astype(F32)


def mat_tread(X, Y, Z, fp, alb):
    i, f = repeat(STAIR["z_foot"] - Z, GOING)                 # f: cm back from the nose of the step
    col = OAK[None, :] * 0.82 * (0.88 + 0.24 * hash2(np.floor(X / 14.0), i, 6.5))[:, None]
    col = stair_runner(X, Z + Y * 1.4, col, fp)
    return lerp(col, col * 1.35, (np.clip(1 - f / 2.6, 0, 1) * 0.6)[:, None])                # the worn nose catches the light


def mat_riser(X, Y, Z, fp, alb):
    i = np.round((STAIR["z_foot"] - Z) / GOING)
    under = (-G + RISE * (i + 1)) - Y                         # cm below the tread above
    col = np.empty_like(alb)
    col[:] = WOODWORK * 0.97
    col = stair_runner(X, Z + Y * 1.4, col, fp)
    return col * (1 - 0.5 * np.clip(1 - under / 3.0, 0, 1))[:, None]                         # the shadow under the nose


def mat_stair_side(X, Y, Z, fp, alb):
    """The panelled side of the staircase (the plane X = 108): a string board under the steps, then white
    frames with a low panel and, where there is room, a tall one above it."""
    line = np.where(Z < STAIR["z_top"], -18.0 + 14.0, stair_line(Z) + RISE)
    below = line - Y                                        # cm below the line of the steps
    y = Y + G                                               # cm above the living-room floor
    col = np.empty_like(alb)
    col[:] = WOODWORK
    col = col * (0.96 + 0.07 * hash2(np.floor(Z / 31.0), np.floor(y / 29.0), 31.0))[:, None]
    stiles = np.array([0.0, 88.0, 175.0, 247.0, 320.0, 402.0, 486.0, 591.0])
    ds = np.min(np.abs(Z[:, None] - stiles[None, :]), axis=1)
    hi = y + below - 30.0                                   # the height of the underside of the string, above the floor
    low_p = (ds > 7.0) & (y > 21.0) & (y < np.minimum(hi, 104.0))
    tall_p = (ds > 7.0) & (y > 118.0) & (y < hi) & (hi > 132.0)
    d_low = np.minimum(np.minimum(ds - 7.0, y - 21.0), np.minimum(hi, 104.0) - y)
    d_tall = np.minimum(np.minimum(ds - 7.0, y - 118.0), hi - y)
    for inp, dist in ((low_p, d_low), (tall_p, d_tall)):
        col[inp] = col[inp] * 0.90
        col = col * (1 - 0.34 * line_cover(dist - 1.2, 1.2, fp) * inp)[:, None]             # the sunk edge, in its own shade
        col = col * (1 + 0.10 * line_cover(dist - 3.6, 0.6, fp) * inp)[:, None]
    string = (below < 23.0) & (Z >= STAIR["z_top"])
    col[string] = WOODWORK * 1.03
    col = col * (1 - 0.35 * line_cover(below - 23.6, 0.8, fp) * (Z >= STAIR["z_top"]))[:, None]
    col[y < 14.0] = WOODWORK * 0.98
    col = col * (1 - 0.40 * line_cover(y - 14.5, 0.7, fp))[:, None]
    col = col * (1 - 0.28 * np.exp(-np.maximum(y, 0) / 8.0))[:, None]
    return col.astype(F32)


def mat_ceiling(X, Y, Z, fp, alb):
    return alb * (0.96 + 0.08 * hash2(np.floor(X / 37.0), np.floor(Z / 41.0), 8.0)[:, None])


def mat_wood(X, Y, Z, fp, alb):
    g = hash2(np.floor(X / 2.3) + np.floor(Y / 2.9), np.floor(Z / 3.1), 9.0)
    return alb * (0.93 + 0.14 * g[:, None] * np.clip(1.8 - fp, 0, 1)[:, None])


def mat_beam(X, Y, Z, fp, alb):
    g = hash2(np.floor(X / 3.0), np.floor(Y / 2.5) + np.floor(Z / 90.0), 10.0)
    return alb * (0.9 + 0.2 * g[:, None])


def mat_kitchen_floor(X, Y, Z, fp, alb):
    a, fa = repeat(X + Z, 21.2)                             # laid on the diagonal
    b, fb = repeat(X - Z, 21.2)
    dark = np.mod(a + b, 2) < 0.5
    col = np.where(dark[:, None], np.array([0.50, 0.62, 0.54], dtype=F32), np.array([0.88, 0.83, 0.68], dtype=F32))
    edge = np.minimum(np.minimum(fa, 21.2 - fa), np.minimum(fb, 21.2 - fb))
    return (col * (1 - 0.3 * line_cover(edge, 0.3, fp))[:, None] * (0.95 + 0.1 * hash2(a, b, 2.0))[:, None]).astype(F32)


def mat_kitchen_wall(X, Y, Z, fp, alb):
    y = Y + G
    col = np.empty_like(alb)
    col[:] = np.array([0.93, 0.80, 0.50], dtype=F32)
    i, f = repeat(X, 15.0)
    j, g = repeat(y, 15.0)
    tile = (y > 90.0) & (y < 150.0)                         # a band of white tiles over the counter
    edge = np.minimum(np.minimum(f, 15 - f), np.minimum(g, 15 - g))
    col[tile] = lerp(rgb("#e9e6d6"), rgb("#aeb4a2"), (line_cover(edge, 0.4, fp) * 0.7)[:, None])[tile]
    return col


def mat_keys(X, Y, Z, fp, alb):
    """The keyboard from above: white keys with the black ones in twos and threes at the back."""
    px0, px1 = LR_PIANO[0], LR_PIANO[1]
    u = X - px0 - 8.0
    i, f = repeat(u, 2.35)
    col = np.empty_like(alb)
    col[:] = rgb("#efe8d6")
    col = lerp(col, rgb("#8d846e"), (line_cover(np.minimum(f, 2.35 - f), 0.16, fp) * 0.55)[:, None])
    k, s = repeat(u + 1.2, 2.35)
    note = np.mod(k, 7)
    black = ((note != 2) & (note != 6)) & (s > 0.45) & (s < 1.9) & (Z < LR_PIANO[4] + 36.0 + 15.0)
    col[black] = rgb("#16121a")
    ends = (u < 0) | (u > px1 - px0 - 16.0)
    col[ends] = rgb("#532a1a")
    col[Z < LR_PIANO[4] + 36.0 + 2.0] = rgb("#3a1c12")
    return col


def mat_books(X, Y, Z, fp, alb):
    """The front of Mom's bookcase: five shelves of spines."""
    bx0, bx1 = LR_BOOKS[0], LR_BOOKS[1]
    u, y = X - bx0, Y + G
    wide = bx1 - bx0
    col = np.empty_like(alb)
    col[:] = rgb("#523420")
    shelf, s = repeat(y - 8.0, 41.0)
    inside = (u > 5.0) & (u < wide - 5.0) & (y > 8.0) & (y < 213.0) & (s > 3.5)
    # books: each shelf has its own run of spines
    w = 3.4 + 2.2 * hash2(np.floor(u / 5.0), shelf, 11.0)
    bi = np.floor((u + shelf * 1.7) / 4.3)
    tall = 26.0 + 9.0 * hash2(bi, shelf, 12.0)
    hue = hash2(bi, shelf, 13.0)
    spines = np.array([rgb(c) for c in ("#7a2e2a", "#2f4a6a", "#3f5c44", "#8a6a34", "#5a3a5c", "#b8a070", "#4a2c22", "#28405a", "#9a4a30", "#c8b48a")])
    sc = spines[np.minimum((hue * len(spines)).astype(int), len(spines) - 1)]
    book = inside & (s - 3.5 < tall)
    col[inside] = rgb("#22140e")
    col[book] = sc[book]
    f = (u + shelf * 1.7) / 4.3 - bi
    col = lerp(col, rgb("#1a100a"), (np.clip(1 - np.minimum(f, 1 - f) * 4.3 / np.maximum(fp, 0.4), 0, 1) * book * 0.5 * np.clip(1.7 - fp, 0, 1))[:, None])
    band = book & (np.abs(s - 3.5 - tall * 0.72) < 1.3) & (hue > 0.35)
    col[band] = lerp(col[band], rgb("#e0c888"), 0.7)
    return col


def mat_wicker(X, Y, Z, fp, alb):
    a = np.where(np.abs(Z - np.round(Z)) < 1e-3, X, X + Z)
    i, f = repeat(Y, 4.2)
    j, g = repeat(a + (i % 2) * 2.4, 4.8)
    weave = 0.82 + 0.3 * np.abs(np.sin((g / 4.8) * math.pi)) * np.clip(1.5 - fp, 0, 1)
    col = alb * weave[:, None]
    return lerp(col, rgb("#5e4424"), (line_cover(np.minimum(f, 4.2 - f), 0.3, fp) * 0.5)[:, None])


def mat_towels(X, Y, Z, fp, alb):
    i, f = repeat(Y - HAMPER[2], 3.0)
    tones = np.array([rgb("#d8dfe6"), rgb("#f0b8c6"), rgb("#e9e4d6")])
    col = tones[np.clip(i.astype(int), 0, 2)]
    return lerp(col, rgb("#7d8088"), (line_cover(np.minimum(f, 3.0 - f), 0.2, fp) * 0.5)[:, None])


def mat_bag(X, Y, Z, fp, alb):
    col = alb.copy()
    col[(Y > 66) & (Y < 82) & (X > BAG[0] + 6) & (X < BAG[1] - 6)] = rgb("#963220")       # its pocket
    col[np.abs(X - (BAG[0] + BAG[1]) / 2) < 1.0] = rgb("#f0e0a0")                           # the zip
    col[Y > 100.0] = rgb("#7a2a1c")
    return col


def mat_shoe(X, Y, Z, fp, alb):
    col = alb.copy()
    col[Y < 2.4] = rgb("#f4f1ea")
    col[(Y > 5.5)] = rgb("#3f6fb0")
    return col


def mat_carton(X, Y, Z, fp, alb):
    col = alb * (0.95 + 0.1 * hash2(np.floor(X / 5.0), np.floor(Y / 6.0), 3.0)[:, None])
    return lerp(col, rgb("#d9c79a"), (np.abs(Y - 30.0) < 2.2)[:, None] * 0.8)


def mat_cooler(X, Y, Z, fp, alb):
    return lerp(alb, rgb("#e8eef4"), (np.abs(Y - 20.0) < 2.5)[:, None] * 0.9)


def mat_study_wall(X, Y, Z, fp, alb):
    col = alb * (0.96 + 0.08 * hash2(np.floor(X / 23.0), np.floor(Y / 19.0), 4.0)[:, None])
    col[Y < 14.0] = rgb("#6a4428")
    return col


def mat_leaf(X, Y, Z, fp, alb):
    """The inside face of the study door, standing open: panels, as on its other side."""
    u = -Z
    col = alb.copy()
    for x0, x1 in ((8, 39), (46, 77)):
        for y0, y1 in ((12, 62), (74, 146), (158, 196)):
            inp = (u > x0) & (u < x1) & (Y > y0) & (Y < y1)
            col[inp] = rgb("#d9cdb5")
            d = np.minimum(np.minimum(u - x0, x1 - u), np.minimum(Y - y0, y1 - Y))
            col = lerp(col, rgb("#8f846c"), (line_cover(d, 0.5, fp) * 0.8)[:, None])
    return col


def mat_drawer(X, Y, Z, fp, alb):
    col = alb.copy()
    x0, x1, th = TABLE[0], TABLE[1], TABLE[2]
    u = X - x0
    edge = np.minimum(np.minimum(u - 8.0, (x1 - x0) - 8.0 - u), np.minimum(Y - (th - 15.5), th - 5.0 - Y))
    col = lerp(col, rgb("#2e1a10"), (line_cover(edge, 0.45, fp) * 0.8)[:, None])
    return col


MATERIALS = {
    "wall": mat_wall, "wall-left": mat_wall_left, "floor-below": mat_floor_below, "landing": mat_landing, "fascia": mat_fascia,
    "tread": mat_tread, "riser": mat_riser, "stair-side": mat_stair_side, "ceiling": mat_ceiling, "wood": mat_wood, "beam": mat_beam,
    "kitchen-floor": mat_kitchen_floor, "kitchen-wall": mat_kitchen_wall, "keys": mat_keys, "books": mat_books, "wicker": mat_wicker,
    "drawer": mat_drawer, "study-floor": mat_floor_below, "towels": mat_towels, "bag": mat_bag, "shoe": mat_shoe,
    "carton": mat_carton, "cooler": mat_cooler, "study-wall": mat_study_wall, "leaf": mat_leaf,
}


def materials(tr):
    alb = tr.base_colors()
    PX, PY, PZ = tr.world()
    fp = tr.footprint()
    mats = np.asarray(tr.mats)
    for name, fn in MATERIALS.items():
        ids = np.nonzero(mats == name)[0]
        if not len(ids):
            continue
        sel = np.isin(tr.tag, ids)
        if sel.any():
            alb[sel] = fn(PX[sel], PY[sel], PZ[sel], fp[sel], alb[sel])
    return alb


# ====================================================================== flat things, laid on through the camera
_NIGHT = None


def night_sky():
    global _NIGHT
    if _NIGHT is None:
        _NIGHT = TH.night()
    return _NIGHT


def decals(tr, T, open_study=False, state=None):
    state = state or THEN
    sky, tree = night_sky()
    frame, glass = TH.window(sky)
    (z0, z1), (y0, y1) = WINDOW["Z"], WINDOW["Y"]
    tr.decal(frame, "X", 0, "Z", z1 + 11, z0 - 11, "Y", y0 - 11, y1 + 11)
    tr.decal(glass, "X", 0, "Z", z1, z0, "Y", y0, y1, emit=True)
    tr.decal(TH.curtains().array(), "X", 0, "Z", z1 + 22, z0 - 22, "Y", y0 - 20, y1 + 22)
    # ---- the landing's wall
    middle = TH.lilsis_door() if state["ladder"] else TH.girls_door()
    for (x0, x1), tex in ((SON, TH.sons_door()), (GIRLS, middle), (STUDY, TH.door(open_=open_study))):
        tr.decal(tex.array(), "Z", 0, "X", x0 - 10, x1 + 10, "Y", 0, 216, k=3)
    if not open_study:
        tr.decal(TH.notice().array(), "Z", 0, "X", SIGN[0], SIGN[1], "Y", SIGN[2], SIGN[3], k=3)
    tr.decal(TH.landing_photos().array(), "Z", 0, "X", 290, 390, "Y", 101, 181, k=3)
    tr.decal(TH.corner_photos().array(), "Z", 0, "X", 112, 176, "Y", 116, 180, k=3)
    tr.decal(TH.chart().array(), "Z", 0, "X", CHART[0], CHART[1], "Y", CHART[2], CHART[3], k=3)
    tr.decal(TH.switch().array(), "Z", 0, "X", 702, 711, "Y", 118, 131)
    tr.decal(TH.switch().array(), "Z", 0, "X", 180, 189, "Y", 104, 117)
    tr.decal(TH.picture().array(), "X", 0, "Z", 122, 76, "Y", 118, 156)
    if state["ladder"]:
        hx0, hx1, hz0, hz1 = HATCH2
        tr.decal(TH.hatch_trim(hx1 - hx0, hz1 - hz0, 6.0).array(), "Y", CEIL, "X", hx0 - 6, hx1 + 6, "Z", hz1 + 6, hz0 - 6)
    else:
        tr.decal(TH.hatch().array(), "Y", CEIL, "X", HATCH[0], HATCH[1], "Z", HATCH[3], HATCH[2])
    # ---- the living room below
    tr.decal(TH.rug(), "Y", -G, "X", RUG[0], RUG[1], "Z", RUG[3], RUG[2])
    f0, f1, g0, g1 = LR_FRAME
    tr.decal(TH.preamble().array(), "Z", 0, "X", f0, f1, "Y", low(g0), low(g1))
    f0, f1, g0, g1 = LR_CLOCK
    tr.decal(TH.clock().array(), "Z", 0, "X", f0, f1, "Y", low(g0), low(g1))
    f0, f1, g0, g1 = LR_DOOR
    tr.decal(TH.front_door().array(), "Z", 0, "X", f0 - 10, f1 + 10, "Y", low(g0), low(g1 + 10))
    tr.decal(TH.closet_door().array(), "X", 108, "Z", 400, 320, "Y", low(0), low(108))
    hang = stair_painting()
    if hang:
        tr.decal(TH.landscape(hang[1] - hang[0], hang[3] - hang[2]).array(), "X", 0, "Z", hang[1] + 8, hang[0] - 8, "Y", low(hang[2] - 8), low(hang[3] + 8))
    f0, f1, g0, g1 = LR_PHOTOS
    tr.decal(TH.stair_photos(f0, f1, g0, g1, PITCH, STAIR["z_foot"], RISE).array(), "X", 0, "Z", f1, f0, "Y", low(g0), low(g1))
    tr.decal(TH.fridge_drawings(3).array(), "Z", -92, "X", 196, 252, "Y", low(46), low(166))
    tr.decal(TH.fridge_drawings(8).array(), "X", 252, "Z", -92, -150, "Y", low(46), low(166))
    if open_study:                                           # a glimpse of Trip Headquarters: the big map on its wall
        t = Tex(150, 100, res=3, color="#e9e0c4")
        t.frame(0, 0, 150, 100, 2.0, "#6a4a2a")
        t.poly([(14, 18), (40, 12), (72, 20), (104, 14), (136, 24), (130, 70), (100, 84), (60, 78), (30, 86), (12, 60)], "#cfd8b0")
        t.poly([(14, 18), (40, 12), (52, 40), (30, 86), (12, 60)], "#d9c79a")
        t.line([(30, 30), (52, 44), (76, 40), (98, 56), (122, 50)], "#c8322a", 1.6, solid=False)
        for px, py in ((30, 30), (52, 44), (76, 40), (98, 56), (122, 50)):
            t.ellipse(px, py, 2.0, 2.0, "#2a3a6a")
        tr.decal(t.array(), "Z", -620, "X", 492, 642, "Y", 72, 172)


# ====================================================================== the light
def window_glass(a_y, b_z):
    """Is this place in the tall window clear glass (not casing, not a glazing bar)?"""
    (z0, z1), (y0, y1) = WINDOW["Z"], WINDOW["Y"]
    u, w = (b_z - z0) / (z1 - z0), (a_y - y0) / (y1 - y0)
    ok = (u > 0.12) & (u < 0.88) & (w > 0.02) & (w < 0.98)           # (the curtains keep the outer hand's breadth of each side)
    cu = np.abs((u * 3) - np.round(u * 3)) * (z1 - z0) / 3          # cm from an upright bar
    cw = np.abs((w * 5) - np.round(w * 5)) * (y1 - y0) / 5
    return ok & (cu > 2.2) & (cw > 2.2)


STUDY_LAMP = (624.0, 124.0, -296.0)
AMBIENT = np.array([0.042, 0.052, 0.100], dtype=F32)


ATTIC = np.array([1.00, 0.74, 0.50], dtype=F32)                # the soft light of The Retreat, coming down its hatch
ATTIC_BELOW = 0.0                                              # how much of it reaches the landing under the hatch: none to speak of beside the hall
#                                                                lamp (tried 0.3: one or two levels over the study door and its notice, and no more);
#                                                                the light shows on the hatch's rim and on the ladder's top, which are lit apart


def light_on(P, N, vis, open_study=False, branches=None, hall=HALL, hatch=None, attic=0.55):
    """Light every place P (arrays of X, Y, Z) that faces N from where the lamps really are. `vis(L, e, directional,
    soft)` says how much of each lamp's light gets there past the boxes. `hall` is where the hall-table lamp's bulb
    is; `hatch` (X0, X1, Z0, Z1), when the attic hatch stands open, lets the attic's light down. -> (..., 3)."""
    PX, PY, PZ = P
    NX, NY, NZ = N
    light = np.zeros(PX.shape + (3,), dtype=F32)
    above = PY > -19.0                                       # the landing and everything over it
    behind = PZ < -0.5                                       # through a doorway: the kitchen below, the study above

    # ---- the hall-table lamp: the bulb itself (with its shade, and true shadows), and the glow it fills the landing with
    e = lamp(P, N, hall, 2.05, 95.0, 0.9) * shade(P, hall, 10.0, 15.0, 0.6) * above * (~behind)
    e = e * vis(hall, e)
    fill = lamp(P, N, (hall[0] + 10, 140.0, 105.0), 1.3, 175.0, 1.0, wrap=0.35) * above * (~behind)
    light += (e + fill)[..., None] * WARM

    # ---- the lamp on the piano, below
    e = lamp(P, N, PIANO, 1.9, 70.0, 0.78) * shade(P, PIANO, 9.0, 13.0, 0.5) * (~above) * (~behind)
    e = e * vis(PIANO, e)
    light += e[..., None] * WARM

    # ---- the kitchen: lit inside, and its light comes out through the doorway across the floor
    e = lamp(P, N, KLAMP, 1.9, 170.0, 0.9, wrap=0.25) * (~above)
    ok, _, _ = through_rect(P, KLAMP, "Z", 0.0, KITCHEN[0], KITCHEN[1], -G, KITCHEN[2])
    e = e * np.where(behind, 1.0, ok)
    e = e * vis(KLAMP, e)
    light += e[..., None] * np.array([1.0, 0.80, 0.50], dtype=F32)

    # ---- from under us, out of the picture: the dinner table's pendant on its white cloth, and Dad's reading lamp
    e = lamp(P, N, TABLE_GLOW, 0.22, 300.0, 1.0, wrap=0.3) * (~behind)
    e = e * vis(TABLE_GLOW, e, soft=1.6)
    light += e[..., None] * WARM2
    down = np.clip((READING[1] + 40.0 - PY) / 160.0, 0.0, 1.0)             # its shade throws its light down
    e = lamp(P, N, READING, 1.3, 240.0, 1.05, wrap=0.3) * (0.06 + 0.94 * down * down) * (~behind)
    e = e * vis(READING, e, soft=1.6)
    light += e[..., None] * WARM2
    down = np.clip((low(150.0) - PY) / 150.0, 0.0, 1.0)                     # the pendant over the table: its pool spreads over the near floor
    e = lamp(P, N, (TABLE_GLOW[0], low(150.0), TABLE_GLOW[2]), 0.65, 230.0, 1.05, wrap=0.2) * down * (~behind)
    e = e * vis(TABLE_GLOW, e, soft=1.6)
    light += e[..., None] * WARM

    # ---- and what all that lit floor throws back up: on the edge of the landing, the beams, the ceiling over the big room
    up_glow = (0.30 * np.clip(NZ, 0, 1) + 0.11 * np.clip(-NY, 0, 1)) * above * (PZ > 168.0)
    light += up_glow[..., None] * WARM2
    light *= np.where(NY < -0.5, 0.74 * np.clip(1.12 - PZ / 620.0, 0.22, 1.0), 1.0)[..., None]      # the ceiling goes dark toward us

    # ---- the moon, through the tall window: only where the way to the moon passes through clear glass
    (z0, z1), (y0, y1) = WINDOW["Z"], WINDOW["Y"]
    ok, A, B = through_rect(P, TO_MOON, "X", 0.0, y0, y1, z0, z1, directional=True)
    ndl = np.clip(NX * TO_MOON[0] + NY * TO_MOON[1] + NZ * TO_MOON[2], 0, 1)
    e = ndl * ok * window_glass(A, B) * (PX > 0.5)
    if branches is not None:                                 # the tree outside throws its branches into the patch
        bh, bw = branches.shape
        e = e * (1.0 - 0.85 * sample(branches, np.clip((z1 - B) / (z1 - z0), 0, 1) * (bw - 1), np.clip((y1 - A) / (y1 - y0), 0, 1) * (bh - 1)))
    e = e * vis(TO_MOON, e, directional=True, soft=0.6)
    light += (e * 2.2)[..., None] * MOON

    # ---- the night sky in the window: a soft cool light on whatever faces it
    e = lamp(P, N, (-40.0, 70.0, 320.0), 0.80, 330.0, 0.8, wrap=0.45) * (~behind)
    light += e[..., None] * SKY

    # ---- when the study door is open: its lamp lights the room behind and throws a bar of light out over the landing
    if open_study:
        e = lamp(P, N, STUDY_LAMP, 2.6, 170.0, 0.8, wrap=0.2) * above
        ok, _, _ = through_rect(P, STUDY_LAMP, "Z", 0.0, STUDY[0], STUDY[1], 0.0, DOOR_H)
        e = e * np.where(behind, 1.0, ok)
        e = e * vis(STUDY_LAMP, e)
        light += e[..., None] * WARM
        light += (behind & above)[..., None] * np.array([0.26, 0.19, 0.11], dtype=F32)      # a lit room is never black anywhere

    # ---- when the attic hatch is open: the soft light of the room above comes down through it, and the way up glows
    if hatch is not None:
        hx0, hx1, hz0, hz1 = hatch
        up = ((hx0 + hx1) / 2, CEIL + 110.0, (hz0 + hz1) / 2)       # (high in the room above, so its light comes down the hatch in a soft cone)
        below = PY < CEIL + 0.5
        e = lamp(P, N, up, attic, 200.0, 0.8, wrap=0.25) * below * above * (~behind)
        ok, _, _ = through_rect(P, up, "Y", CEIL, hx0, hx1, hz0, hz1)
        e = e * ok
        e = e * vis(up, e, soft=1.8)
        light += e[..., None] * ATTIC
        light += (~below)[..., None] * (ATTIC * 2.2)               # the way up itself, seen from below, glows

    # ---- what is left when no lamp reaches: the cool dark of a house at night
    light += AMBIENT * (0.78 + 0.22 * NY[..., None] + 0.10 * NZ[..., None])
    return light


SHADOW_HUE = np.array([-0.08, 0.0, 0.15], dtype=F32)
LIGHT_HUE = np.array([0.05, 0.0, -0.10], dtype=F32)


def expose(albedo, light, gain=1.5):
    lit = albedo * light * gain
    out = 1.0 - np.exp(-lit * 1.25)
    peak = out.max(axis=-1, keepdims=True)                   # where a lamp burns a surface out it goes to warm white, not to orange
    out = lerp(out, np.maximum(out, peak * np.array([1.0, 0.90, 0.66], dtype=F32)), np.clip((peak - 0.82) / 0.18, 0, 1) * 0.7)
    # a painter's night: what the lamps do not reach is blue-violet, what they do is gold, and both are a little richer than life
    lum = (out @ np.array([0.3, 0.55, 0.15], dtype=F32))[..., None]
    out = out * (1 + (1 - smooth((lum - 0.05) / 0.40)) * SHADOW_HUE) * (1 + smooth((lum - 0.45) / 0.45) * LIGHT_HUE)
    mean = out.mean(axis=-1, keepdims=True)
    return np.clip(mean + (out - mean) * 1.12, 0, 1).astype(F32)


def tone_at(color, X, Y, Z, n, boxes, open_study=False, extra=None, state=None, attic=0.55):
    """The color a small thing of this paint shows at a place in the room, facing n (for things drawn by hand)."""
    state = state or THEN
    P = tuple(np.atleast_1d(np.asarray(q, dtype=F32)) for q in (X, Y, Z))
    N = tuple(np.full(P[0].shape, q, dtype=F32) for q in n)

    def vis(L, e, directional=False, soft=0):
        return 1.0 - blocked(P, L, boxes, directional).astype(F32)
    c = rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
    light = light_on(P, N, vis, open_study, hatch=HATCH2 if state["ladder"] else None, attic=attic)
    if extra is not None:
        light = light + np.asarray(extra, dtype=F32)
    out = expose(c[None, :], light)
    return out if len(out) > 1 else out[0]


# ====================================================================== the picture
def render(ss=2, open_study=False, window=(0, 0, W, H), state=None):
    """-> dict: `pic` the lit room (crisp, unbrushed) at picture size, the tracer, the tags."""
    state = state or THEN
    tr = Tracer(V, ss=ss, window=window)
    T = build(tr, open_study, state)
    materials(tr)
    decals(tr, T, open_study, state)
    PX, PY, PZ = tr.world()
    P, N = (PX, PY, PZ), tr.normal()
    Ps = tuple(q[::ss, ::ss] for q in P)                      # shadows on a coarser grid: one per picture pixel
    boxes = list(tr.boxes)
    # the ladder (when it is down) is not in the backdrop, but it throws its shadow there: from the lamps up on the
    # landing (the hall-table lamp, the light of The Retreat through the hatch), not from the moon or the room below
    with_ladder = boxes + (ladder_boxes() if state["ladder"] else [])

    def vis(L, e, directional=False, soft=0.9):
        hit = np.zeros(Ps[0].shape, dtype=bool)
        idx = np.nonzero(e[::ss, ::ss] > 0.004)
        near = with_ladder if (not directional and L[1] > -19.0) else boxes
        if len(idx[0]):
            hit[idx] = blocked(tuple(q[idx] for q in Ps), L, near, directional)
        clear = 1.0 - hit.astype(F32)
        if soft:
            clear = blur(clear, soft)
        return resize(clear, PX.shape, Image.BILINEAR) if ss > 1 else clear
    sky, tree = night_sky()
    light = light_on(P, N, vis, open_study, branches=blur(tree, 2.0), hatch=HATCH2 if state["ladder"] else None, attic=ATTIC_BELOW)
    hh, ww = PX.shape
    x0_, y0_ = window[0], window[1]
    big = noise((H * ss, W * ss), 90 * ss, 41, 4)[y0_ * ss:y0_ * ss + hh, x0_ * ss:x0_ * ss + ww]
    hue = noise((H * ss, W * ss), 60 * ss, 42, 3)[y0_ * ss:y0_ * ss + hh, x0_ * ss:x0_ * ss + ww] - 0.5
    light = light * (0.88 + 0.24 * big[..., None])
    light[..., 0] *= 1 + 0.10 * hue
    light[..., 2] *= 1 - 0.12 * hue
    lit = expose(tr.albedo, light)
    lit = lit * (1 - tr.ecov[..., None]) + tr.emit * tr.ecov[..., None]
    pic = tr.down(lit)
    return dict(pic=pic, tr=tr, T=T, tag=tr.tag[::ss, ::ss].copy(), t=tr.t[::ss, ::ss].copy(), boxes=boxes, window=window, open=open_study, state=state)


def tags_of(R, *names):
    ids = [R["T"][n] for n in names if n in R["T"]]
    return np.isin(R["tag"], ids)


# ---------------------------------------------------------------- brushwork, and saying the hard things again
def brushed(base, seed=2, fast=False):
    if fast:
        return base.copy()
    return strokes(base, sizes=(9, 5, 2), seed=seed, density=1.5, jitter=0.03, keep=0.34)


def restate(pic, base, R, amount=0.86):
    """Over the brushwork, put back every built edge and every small pattern crisply."""
    lum = base @ np.array([0.3, 0.55, 0.15], dtype=F32)
    fine = np.abs(base - blur(base, 1.6)).sum(axis=2)
    m = np.clip(fine * 7.0, 0, 1)
    tag = R["tag"]
    edge = np.zeros(tag.shape, dtype=F32)
    edge[:, 1:] = np.maximum(edge[:, 1:], tag[:, 1:] != tag[:, :-1])
    edge[1:, :] = np.maximum(edge[1:, :], tag[1:, :] != tag[:-1, :])
    m = np.clip(np.maximum(m, blur(edge, 0.8) * 1.6), 0, 1)
    m = np.clip(blur(m, 0.6) * 1.25, 0, 1) * amount
    m = np.maximum(m, lettering_mask(R["open"], R.get("state")))
    pic[...] = lerp(pic, base, m[..., None])
    return m


# ====================================================================== small round things, drawn by hand through the camera
def hull(points):
    pts = sorted(set((round(x, 3), round(y, 3)) for x, y in points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def ring(X, Y, Z, r, n=20):
    """A level circle in the room -> its ellipse in the picture."""
    return [V.pt(X + math.cos(i / n * math.tau) * r, Y, Z + math.sin(i / n * math.tau) * r) for i in range(n)]


def turned(sheet, X, Z, profile, colors, steps=None):
    """A thing turned on a lathe (a lamp base, a bowl, a shade): `profile` is [(height, radius), ...] from the
    bottom up; each band between two heights is filled with its color (the hull of its two rings)."""
    for (y0, r0), (y1, r1), c in zip(profile[:-1], profile[1:], colors):
        sheet.poly(hull(ring(X, y0, Z, r0) + ring(X, y1, Z, r1)), c)


def table_lamp(sheet, X, Y, Z, k=1.0, lit=True):
    """A lamp with a pleated shade standing at (X, Y, Z): a turned base, a brass neck, the glowing shade."""
    turned(sheet, X, Z, [(Y, 6.5 * k), (Y + 2 * k, 6.5 * k), (Y + 3 * k, 3.4 * k), (Y + 9 * k, 6.2 * k), (Y + 16 * k, 4.6 * k), (Y + 21 * k, 2.0 * k), (Y + 27 * k, 1.4 * k)],
           ["#7c5c26", "#c9a85a", "#3f7088", "#4c84a0", "#35607a", "#c79c44"])
    hi = V.pt(X + 3.0 * k, Y + 11 * k, Z + 4.0 * k)
    sheet.ellipse(hi[0], hi[1], 1.3 * k, 2.2 * k, "#dff0f4", 0.8)
    y0, y1, r0, r1 = Y + 26 * k, Y + 50 * k, 15.0 * k, 10.0 * k
    body = hull(ring(X, y0, Z, r0) + ring(X, y1, Z, r1))
    sheet.poly(body, "#e8973c" if lit else "#b9ad94")
    # the shade is brightest where the bulb is nearest the cloth, and it is pleated
    cx0, cy0 = V.pt(X, y0, Z)
    cx1, cy1 = V.pt(X, y1, Z)
    s = V.scale_at(X, Z)
    for f, c, a in ((0.84, "#f6b352", 1.0), (0.62, "#ffcd72", 1.0), (0.38, "#ffe29a", 1.0), (0.17, "#fff3c4", 0.95)):
        sheet.poly(hull([(cx0 - r0 * s * f, cy0 + 0.5), (cx0 + r0 * s * f, cy0 + 0.5), (cx1 + r1 * s * f, cy1 + 1.5), (cx1 - r1 * s * f, cy1 + 1.5)]), c if lit else "#cfc4ac", a)
    for i in range(-5, 6):
        f = i / 5.5
        sheet.line([(cx0 + r0 * s * f, cy0 + (1 - f * f) ** 0.5 * 1.0), (cx1 + r1 * s * f, cy1 + (1 - f * f) ** 0.5 * 0.6)], "#d08a34" if lit else "#8f8570", 0.5, 0.45)
    sheet.poly(ring(X, y1, Z, r1), "#ffe9a8" if lit else "#d8cfba")                   # looking down into the top of it
    sheet.poly(ring(X, y1, Z, r1 * 0.6), "#fffbe6" if lit else "#e6dfcc", 0.95)
    edge = ring(X, y1, Z, r1)
    sheet.line(edge + [edge[0]], "#b06a24" if lit else "#7a705a", 0.8, 0.95)
    low_ = ring(X, y0, Z, r0)
    half = [p for p in low_ if p[1] >= cy0 - 0.2]
    sheet.line(sorted(half), "#a85f20" if lit else "#7a705a", 0.9, 0.95)


def details(pic, R, fast=False):
    """The small crisp things over the brushwork: lamps, the key bowl, cords, handles, the hymnal, the kettle,
    the dark lines where things meet, the bright edges that face a lamp."""
    shape = SHAPE
    tag = R["tag"]
    boxes = R["boxes"]
    state = R.get("state") or THEN
    x, y = grid(shape)

    # ---- where one thing stops and another starts: a broken dark line, as a pen would restate it
    edge = np.zeros(tag.shape, dtype=F32)
    edge[:, 1:] = np.maximum(edge[:, 1:], tag[:, 1:] != tag[:, :-1])
    edge[1:, :] = np.maximum(edge[1:, :], tag[1:, :] != tag[:-1, :])
    t = R["t"]
    jump = np.zeros(tag.shape, dtype=F32)
    jump[:, 1:] = np.abs(t[:, 1:] - t[:, :-1]) > 12
    jump[1:, :] = np.maximum(jump[1:, :], np.abs(t[1:, :] - t[:-1, :]) > 12)
    broken = 0.45 + 0.55 * noise(shape, 9, 31, 3)
    tint(pic, "#3a2c3c", (np.clip(blur(edge * jump, 0.55) * 2.0, 0, 1) * 0.5 * broken).astype(F32))
    tint(pic, "#5a4a52", (np.clip(blur(edge * (1 - jump), 0.5) * 1.6, 0, 1) * 0.22 * broken).astype(F32))

    # ---- contact shadows: things that stand on a floor are darkest where they meet it
    s = Sheet(shape)
    for (X0, X1, Z0, Z1, yb, a) in ((TABLE[0], TABLE[1], 0, TABLE[4] + 3, 0.0, 0.34), (HAMPER[0] - 2, HAMPER[1] + 5, 0, HAMPER[4] + 5, 0.0, 0.42),
                                    (120, 150, 2, 38, 0.0, 0.3), (LR_STOOL[0], LR_STOOL[1], LR_STOOL[4] - 2, LR_STOOL[5] + 4, -G, 0.4),
                                    (LR_PIANO[0] - 4, LR_PIANO[1] + 4, 0, LR_PIANO[5] + 6, -G, 0.45), (LR_BOOKS[0] - 2, LR_BOOKS[1] + 4, 0, LR_BOOKS[5] + 6, -G, 0.4)):
        s.poly(V.poly([(X0, yb + 0.3, Z0), (X1, yb + 0.3, Z0), (X1, yb + 0.3, Z1), (X0, yb + 0.3, Z1)]), "#1a1420", a)
    sc, sa = s.done()
    floors = tags_of(R, "landing", "floor-below")
    tint(pic, "#2a2030", (blur(sa, 2.2) * floors).astype(F32) * 0.9)

    # ---- on the hall table: the lamp (lit), the key bowl
    top = TABLE[2]
    front = Sheet(shape)
    lamp_x, lamp_z = state["lamp"]
    table_lamp(front, lamp_x, top, lamp_z, 1.22)
    bx, bz = state["bowl"]
    turned(front, bx, bz, [(top, 4.5), (top + 2.5, 6.5), (top + 6.5, 10.0)], ["#2c5670", "#3d7896"])
    front.poly(ring(bx, top + 6.5, bz, 10.0), "#5596b4")
    front.poly(ring(bx, top + 6.0, bz, 8.4), "#234a62")
    kx, ky = V.pt(bx, top + 5.5, bz)
    front.line([(kx - 4, ky + 0.6), (kx - 0.5, ky - 0.4), (kx + 3.5, ky + 0.8)], "#e8c45a", 1.1)          # keys: Mom's car keys are NOT here
    front.ellipse(kx + 3.6, ky + 0.6, 1.5, 1.1, "#c8322a")
    front.ellipse(kx - 3.8, ky + 0.8, 1.3, 1.0, "#d9dde2")
    fc, fa = front.done()
    lx, ly = V.pt(HALL[0], top + 46, HALL[2])                # (the halo stays where the light is, wherever the lamp is set down)
    if state["ladder"]:                                      # where the ladder's feet stand on the floor (under the lamp's own glow)
        ladder_shadow(pic, R)
    glow(pic, "#ffcf8a", mask_ellipse(shape, lx, ly, 50, 44, soft=15) * 0.16)                # the lamp's halo, then the lamp itself
    over(pic, fc, fa)

    if state["ladder"]:
        # ---- the open hatch: the soft light of the room above, on the rim of the opening
        hx0, hx1, hz0, hz1 = HATCH2
        cx_, cy_ = V.pt((hx0 + hx1) / 2 + 4, CEIL + 3, (hz0 + hz1) / 2)
        glow(pic, "#ffc98a", mask_ellipse(shape, cx_, cy_, 44, 10, soft=6) * HATCH_GLOW)
        glow(pic, "#ffd9a8", mask_ellipse(shape, cx_ - 6, cy_ + 1, 22, 4, soft=3) * HATCH_GLOW * 0.8)
    else:
        # ---- the attic hatch's cord, with its wooden toggle
        cord = Sheet(shape)
        cxh, czh = (HATCH[0] + HATCH[1]) / 2, HATCH[3] - 5
        p0, p1 = V.pt(cxh, CEIL - 0.5, czh), V.pt(cxh, 199.0, czh)
        cord.line([p0, (p0[0] + 0.4, (p0[1] + p1[1]) / 2), p1], "#e9dfc6", 1.0, 0.95)
        cord.line([(p0[0] + 0.9, p0[1]), (p1[0] + 0.9, p1[1])], "#6a5a48", 0.6, 0.6)
        cord.poly([(p1[0] - 1.6, p1[1]), (p1[0] + 1.8, p1[1]), (p1[0] + 1.4, p1[1] + 7), (p1[0] - 1.2, p1[1] + 7)], "#a8763e")
        cord.line([(p1[0] - 1.2, p1[1] + 1), (p1[0] - 1.0, p1[1] + 6)], "#e0b070", 0.7)
        cord.onto(pic)

    # ---- below: the lamp on the piano, the open hymnal on its stand, things on its lid
    low_sheet = Sheet(shape)
    px0, px1, _, ptop_, pz0, pz1 = LR_PIANO
    ptop = low(ptop_)
    table_lamp(low_sheet, PIANO_LAMP[0], ptop, PIANO_LAMP[1], 0.82)
    mid = (px0 + px1) / 2 - 8.0
    hy0, hy1, hz = low(86.0), low(110.0), pz0 + 37.5
    for (a0, a1, c) in ((mid - 19.0, mid - 0.5, "#f6eed8"), (mid + 0.5, mid + 19.0, "#efe5cc")):
        low_sheet.poly(V.poly([(a0, hy0, hz + 3.0), (a1, hy0, hz + 3.0), (a1, hy1, hz), (a0, hy1, hz)]), c)
        for k in range(5):
            yy = lerp(hy0 + 3, hy1 - 3, k / 4)
            zz = lerp(hz + 2.6, hz + 0.4, k / 4)
            low_sheet.line([V.pt(a0 + 2, yy, zz), V.pt(a1 - 2, yy, zz)], "#5a5048", 0.7, 0.75)
    low_sheet.line([V.pt(mid, hy0, hz + 3.0), V.pt(mid, hy1, hz)], "#7a2e2a", 1.0)
    low_sheet.line([V.pt(mid - 21.0, hy0 - 1, hz + 3.4), V.pt(mid + 21.0, hy0 - 1, hz + 3.4)], "#2a1a12", 1.4)
    for bx_, fr, inner in ((px0 + 16.0, "#8a6a34", "#9cc0a0"), (px0 + 33.0, "#2a1a12", "#d8c8a8")):         # two framed photographs standing on the lid
        low_sheet.poly(V.poly([(bx_, ptop, 15), (bx_ + 13, ptop, 15), (bx_ + 13, ptop + 17, 12), (bx_, ptop + 17, 12)]), fr)
        low_sheet.poly(V.poly([(bx_ + 2, ptop + 2.2, 14.6), (bx_ + 11, ptop + 2.2, 14.6), (bx_ + 11, ptop + 14.8, 12.4), (bx_ + 2, ptop + 14.8, 12.4)]), inner)
        hx_, hy_ = V.pt(bx_ + 6.5, ptop + 8.0, 13.5)
        low_sheet.ellipse(hx_, hy_, 1.6, 2.2, "#5a4a6a")
    mx_ = PIANO_LAMP[0] - 30.0                               # the metronome
    low_sheet.poly(hull([V.pt(mx_ - 5, ptop, 16), V.pt(mx_ + 5, ptop, 16), V.pt(mx_, ptop + 21, 16)]), "#6a4428")
    low_sheet.line([V.pt(mx_, ptop + 3, 16.5), V.pt(mx_ + 1.5, ptop + 17, 16.5)], "#d8c088", 0.6)
    lc, la = low_sheet.done()
    below = tags_of(R, "wall-below", "piano", "piano-front", "piano-top", "keys", "key-slip", "floor-below", "stool", "stool-top")
    lx, ly = V.pt(PIANO[0], ptop + 30, PIANO_LAMP[1])
    glow(pic, "#ffcf8a", mask_ellipse(shape, lx, ly, 34, 30, soft=11) * 0.15 * below)
    over(pic, lc, la * below)

    # ---- the cable Dad ran from the cupboard under the stairs, along the foot of the panelling to the bookcase
    cab = Sheet(shape)
    pts = [(111.0, 394.0, 2.0), (117.0, 382.0, 0.8), (114.5, 250.0, 0.8), (112.5, 120.0, 0.8), (113.0, 40.0, 0.8), (LR_BOOKS[0] - 2.0, 38.0, 0.8)]
    line = [V.pt(X_, -G + up_, Z_) for X_, Z_, up_ in pts]
    cab.line(line, "#15161c", 1.0, 0.9)
    cab.line([(x_ + 0.3, y_ - 0.7) for x_, y_ in line], "#5a5a66", 0.5, 0.5)
    cc, ca = cab.done()
    over(pic, cc, ca * tags_of(R, "floor-below", "stair-side"))

    # ---- in the kitchen: a kettle on the counter, the fridge's handle
    ks = Sheet(shape)
    kx_, kz_, ky_ = 286.0, -268.0, low(88.0)
    turned(ks, kx_, kz_, [(ky_ + 2.5, 9.0), (ky_ + 11, 9.5), (ky_ + 17, 6.5), (ky_ + 19, 2.5)], ["#b02c22", "#d8463a", "#8a1e18"])
    a_, b_ = V.pt(kx_ + 9, ky_ + 11, kz_), V.pt(kx_ + 17, ky_ + 16, kz_)
    ks.line([a_, b_], "#c8382c", 1.4)
    g_ = V.pt(kx_ + 3.5, ky_ + 9, kz_ + 6)
    ks.ellipse(g_[0], g_[1], 1.0, 1.6, "#ffd8c0", 0.9)
    a_, b_, c_ = V.pt(kx_ - 7, ky_ + 15, kz_), V.pt(kx_, ky_ + 25, kz_), V.pt(kx_ + 6, ky_ + 16, kz_)
    ks.line(curve([a_, b_, c_], 6), "#2a2a30", 1.3)
    ks.line([V.pt(250.5, low(96), -93), V.pt(250.5, low(150), -93)], "#b8bcc0", 1.2)
    kc, ka = ks.done()
    over(pic, kc, ka * tags_of(R, "kitchen-wall", "kitchen-floor", "counter", "counter-top", "fridge"))

    # ---- Little Sister's rabbit, left sitting on the stairs
    rb = Sheet(shape)
    i = 5
    rz, rx, ry = STAIR["z_foot"] - GOING * i - 13.0, 15.0, step_top(i)
    fur = tone_at("#e8d6d8", rx, ry + 8, rz, (0.3, 0.9, 0.3), boxes, state=state, attic=ATTIC_BELOW)
    dark = np.clip(np.asarray(fur) * 0.72, 0, 1)
    turned(rb, rx, rz, [(ry, 6.5), (ry + 7, 7.0), (ry + 13, 4.0)], [fur, dark])
    hx_, hy_ = V.pt(rx, ry + 17.0, rz)
    k_ = V.scale_at(rx, rz)
    rb.ellipse(hx_, hy_, 4.6 * k_, 4.4 * k_, fur)
    for dx_ in (-2.4, 2.4):
        e0, e1 = V.pt(rx + dx_, ry + 20.0, rz), V.pt(rx + dx_ * 1.9, ry + 31.0, rz)
        rb.taper([e0, e1], fur, 2.6 * k_, 1.8 * k_)
        rb.line([(e0[0] + 0.3, e0[1] - 1), (e1[0] + 0.2, e1[1] + 1.5)], "#d89aa8", 0.8 * k_, 0.8)
    rb.ellipse(hx_ - 1.4 * k_, hy_ - 0.4 * k_, 0.6, 0.6, "#2a2030")
    rb.ellipse(hx_ + 1.6 * k_, hy_ - 0.4 * k_, 0.6, 0.6, "#2a2030")
    rc_, ra_ = rb.done()
    over(pic, rc_, ra_ * tags_of(R, "tread", "riser", "wall-left"))

    # ---- bright edges that face a lamp
    hl = Sheet(shape)
    for i in range(STAIR["steps"]):                          # the noses of the steps, where the moon lies on them
        z1 = STAIR["z_foot"] - GOING * i
        yy = step_top(i)
        lit = tone_at("#f2e6cf", 54.0, yy, z1 - 3.0, (0, 1, 0), boxes, state=state, attic=ATTIC_BELOW)
        hl.line([V.pt(1.0, yy, z1), V.pt(107.0, yy, z1)], lit, 0.9, 0.75)
    for xx in np.arange(110.0, 780.0, 30.0):                 # the nose of the landing
        lit = tone_at("#fbf4e2", xx + 15, 0.0, 173.0, (0, 1, 0), boxes, state=state, attic=ATTIC_BELOW)
        hl.line([V.pt(xx, 0.2, 175.0), V.pt(xx + 30.5, 0.2, 175.0)], lit, 0.9, 0.9)
    hl.line([V.pt(TABLE[0] - 1.5, top, TABLE[4] + 1.5), V.pt(TABLE[1] + 1.5, top, TABLE[4] + 1.5)], "#e2b47a", 0.8, 0.8)
    hl.line([V.pt(LR_PIANO[0] + 7.0, low(72.0), LR_PIANO[5]), V.pt(LR_PIANO[1] - 7.0, low(72.0), LR_PIANO[5])], "#fff6e0", 0.7, 0.6)
    hc, ha = hl.done()
    over(pic, hc, ha * (R["t"] > 0))
    return pic


# ====================================================================== the attic ladder (its own cut-out: people pass in front of it and behind it)
PINE = "#c99a5e"                                            # a pine loft ladder, its wood left bare
PINE_DOOR = "#b98c5c"                                       # the hatch's door, seen from its attic side
LADDER_FILL = (0.10, 0.085, 0.085)                          # what the ladder gets back from the lit wall and the room below
BELOW_FILL = (0.12, 0.085, 0.05)                            # and, on the faces turned to us, the warm glow of the lit room below
CARD_FILL = (0.50, 0.42, 0.33)                              # and the card on it, facing the lit room below (so that it reads)


def light_at(X, Y, Z, n, boxes, state=None, attic=0.55, extra=None):
    """The light (not yet a color) that reaches places in the room facing n. -> (k, 3)."""
    state = state or THEN
    P = tuple(np.atleast_1d(np.asarray(q, dtype=F32)) for q in (X, Y, Z))
    N = tuple(np.full(P[0].shape, q, dtype=F32) for q in n)

    def vis(L, e, directional=False, soft=0):
        return 1.0 - blocked(P, L, boxes, directional).astype(F32)
    light = light_on(P, N, vis, False, hatch=HATCH2 if state["ladder"] else None, attic=attic)
    return light + (np.asarray(extra, dtype=F32) if extra is not None else 0.0)


def plane_tex(tex, Z, X0, X1, Y0, Y1, k=4):
    """A flat painting (h, w, 4) on the upright plane Z = const, from X0 to X1 and Y0 to Y1, as the lens sees it
    (k x k samples a pixel). -> (color, cover) at picture size."""
    corners = [V.pt(X, Y, Z) for X in (X0, X1) for Y in (Y0, Y1)]
    x0, x1 = int(math.floor(min(c[0] for c in corners))) - 1, int(math.ceil(max(c[0] for c in corners))) + 2
    y0, y1 = int(math.floor(min(c[1] for c in corners))) - 1, int(math.ceil(max(c[1] for c in corners))) + 2
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    h, w = y1 - y0, x1 - x0
    py, px = np.mgrid[0:h * k, 0:w * k].astype(F32)
    a = ((px + 0.5) / k + x0 - V.cx) / V.F
    u = (V.hz - ((py + 0.5) / k + y0)) / V.F
    dX, dY, dZ = a * V.rx + V.fx, u, a * V.rz + V.fz
    t = (Z - V.cam_z) / dZ
    Xs, Ys = V.cam_x + dX * t, V.eye + dY * t
    fu, fv = (Xs - X0) / (X1 - X0), (Y1 - Ys) / (Y1 - Y0)
    inside = ((t > 0) & (fu >= 0) & (fu <= 1) & (fv >= 0) & (fv <= 1)).astype(F32)
    th_, tw_ = tex.shape[:2]
    got = sample(tex, np.clip(fu, 0, 1) * (tw_ - 1), np.clip(fv, 0, 1) * (th_ - 1))
    cov = got[..., 3] * inside
    col = (got[..., :3] * cov[..., None]).reshape(h, k, w, k, 3).mean(axis=(1, 3))
    cv = cov.reshape(h, k, w, k).mean(axis=(1, 3))
    color, cover = np.zeros((H, W, 3), dtype=F32), np.zeros((H, W), dtype=F32)
    color[y0:y1, x0:x1] = col / np.maximum(cv, 1e-4)[..., None]
    cover[y0:y1, x0:x1] = cv
    return color, cover


def card_place(L=None):
    """Where Big Sister's card hangs: flat against the outer face of the ladder's near side, its middle on that
    side's middle at eye height. -> (X0, X1, Y0, Y1, Z)."""
    L = L or LADDER
    _, _, _, _, Xf, Xb = ladder_frame(L)
    w, h = CARD_WH
    xc = (Xf(CARD_AT) + Xb(CARD_AT)) / 2
    return xc - w / 2, xc + w / 2, CARD_AT - h / 2, CARD_AT + h / 2, L["z"][1] + 0.6


def ladder_plane(R):
    """The folding loft ladder let down from the open hatch to the landing floor, the hatch's door hanging with
    it, the joints of its four lengths, its rubber feet, and Big Sister's card hung on it at eye height:
    THE RETREAT. Lit where it stands (the hall lamp is behind it and to the left, so the faces we see are in its
    own shade, the treads' tops and undersides catch the lamp, and the light of The Retreat comes down the hatch
    onto its top rungs). -> (color, alpha)."""
    L = LADDER
    boxes = R["boxes"]                                      # the room's own boxes: the ladder does not shade itself here
    Ls, (dX, dY), (nX, nY), at, Xf, Xb = ladder_frame(L)
    z0, z1, th, deep = L["z"][0], L["z"][1], L["thick"], L["deep"]
    eye = V.eye
    NF = (nX, nY, 0.0)
    jobs = []                                               # (3d polygon, normal, paint, where its light is taken)

    def face(poly3, n, paint):
        c = np.mean(np.asarray(poly3, dtype=F32), axis=0)
        jobs.append((poly3, n, paint, (float(c[0]), float(c[1]), float(c[2]))))

    # ---- the hatch's door, hanging behind the top length (its attic side toward us)
    hz0, hz1 = z0 - 3.0, z1 + 3.0
    n = 8
    for i in range(n):
        sa, sb = L["door"] * i / n, L["door"] * (i + 1) / n
        (xa, ya), (xb, yb) = at(sa, deep), at(sb, deep)
        face([(xa, ya, hz0), (xb, yb, hz0), (xb, yb, hz1), (xa, ya, hz1)], NF, PINE_DOOR)
        (xc, yc), (xd, yd) = at(sa, deep + 2.2), at(sb, deep + 2.2)
        face([(xa, ya, hz1), (xb, yb, hz1), (xd, yd, hz1), (xc, yc, hz1)], (0.0, 0.0, 1.0), "#ddd2bc")      # its edge, painted like the ceiling

    # ---- the far side: its inner face and its front edge
    bands = 26
    ys = np.linspace(0.0, CEIL, bands + 1)
    for side_z, inner in ((z0, z0 + th), (z1, z1)):
        if side_z == z1:
            continue
        for ya, yb in zip(ys[:-1], ys[1:]):
            face([(Xf(ya), ya, inner), (Xf(yb), yb, inner), (Xb(yb), yb, inner), (Xb(ya), ya, inner)], (0.0, 0.0, 1.0), PINE)
            face([(Xf(ya), ya, z0), (Xf(yb), yb, z0), (Xf(yb), yb, inner), (Xf(ya), ya, inner)], NF, PINE)
    # ---- the treads
    for k in range(1, L["treads"] + 1):
        yk = k * L["step"]
        xn = Xf(yk) - 0.8
        xa, za, zb = xn - L["tread"], z0 + th, z1 - th
        if yk < eye:
            face([(xa, yk, za), (xn, yk, za), (xn, yk, zb), (xa, yk, zb)], (0.0, 1.0, 0.0), PINE)
        elif yk - L["tthick"] > eye:
            y_ = yk - L["tthick"]
            face([(xa, y_, za), (xn, y_, za), (xn, y_, zb), (xa, y_, zb)], (0.0, -1.0, 0.0), PINE)
        face([(xn, yk - L["tthick"], za), (xn, yk, za), (xn, yk, zb), (xn, yk - L["tthick"], zb)], (1.0, 0.0, 0.0), PINE)
    # ---- the near side: its front edge, then its outer face
    for ya, yb in zip(ys[:-1], ys[1:]):
        face([(Xf(ya), ya, z1 - th), (Xf(yb), yb, z1 - th), (Xf(yb), yb, z1), (Xf(ya), ya, z1)], NF, PINE)
    for ya, yb in zip(ys[:-1], ys[1:]):
        face([(Xf(ya), ya, z1), (Xf(yb), yb, z1), (Xb(yb), yb, z1), (Xb(ya), ya, z1)], (0.0, 0.0, 1.0), PINE)

    # ---- every face takes the light where it is (one call for each way a face can look)
    lit = [None] * len(jobs)
    for nrm in set(j[1] for j in jobs):
        ids = [i for i, j in enumerate(jobs) if j[1] == nrm]
        for paint in set(jobs[i][2] for i in ids):
            sel = [i for i in ids if jobs[i][2] == paint]
            A = np.asarray([jobs[i][3] for i in sel], dtype=F32)
            fill = np.asarray(LADDER_FILL, dtype=F32) + (np.asarray(BELOW_FILL, dtype=F32) if nrm == (0.0, 0.0, 1.0) else 0.0)
            c = tone_at(paint, A[:, 0], A[:, 1], A[:, 2], nrm, boxes, extra=fill, state=NOW, attic=ATTIC_LADDER)
            c = np.atleast_2d(c)
            for i, ci in zip(sel, c):
                lit[i] = ci
    s = Sheet(SHAPE)
    rng = np.random.default_rng(23)
    for (poly3, n_, paint, _), c in zip(jobs, lit):
        pp = V.poly(poly3)
        if len(pp) >= 3:
            s.poly(pp, np.clip(c * (0.96 + 0.08 * rng.random()), 0, 1))

    # ---- what a painter says again crisply: the grain and edges of the near side, its joints, its feet
    def near_line(Y0_, Y1_, back, color, wd=0.8, alpha=0.9, z=z1 + 0.05):
        pts = []
        for Y in np.linspace(Y0_, Y1_, 12):
            X = Xf(Y) - (Xf(Y) - Xb(Y)) * back
            pts.append(V.pt(X, Y, z))
        s.line(pts, color, wd, alpha)
    lum_out = float(np.mean([lit[i] for i, j in enumerate(jobs) if j[1] == (0.0, 0.0, 1.0) and j[2] == PINE], axis=(0, 1)))
    dark = np.clip(rgb(PINE) * max(lum_out, 0.08) * 0.42, 0, 1)
    near_line(0.0, CEIL, 0.97, dark, 0.9, 0.9)                         # its back edge, in its own shade
    near_line(0.0, CEIL, 0.03, np.clip(rgb("#f0c888") * 0.85, 0, 1), 0.6, 0.55)     # its front edge just catches the light
    for b_, a_ in ((0.35, 0.22), (0.62, 0.18)):                         # the grain of the wood, running its length
        near_line(4.0, CEIL - 6.0, b_, dark, 0.45, a_)
    for sj in L["joints"]:                                              # the hinges where it folds: a steel plate across each side, a rivet
        yj = CEIL + dY * sj
        for zz in (z1 + 0.25,):
            q = [(Xf(yj + 5.0) + 0.2, yj + 5.0, zz), (Xf(yj - 5.0) + 0.2, yj - 5.0, zz), (Xb(yj - 5.0) - 0.2, yj - 5.0, zz), (Xb(yj + 5.0) - 0.2, yj + 5.0, zz)]
            s.poly(V.poly(q), "#3d3b40")
            s.line([V.pt(Xf(yj + 5.0), yj + 5.0, zz), V.pt(Xb(yj + 5.0), yj + 5.0, zz)], "#8a8890", 0.5, 0.8)
            rx_, ry_ = V.pt((Xf(yj) + Xb(yj)) / 2, yj, zz)
            s.ellipse(rx_, ry_, 0.8, 0.8, "#b8b6bc")
        a1, a2 = V.pt(Xf(yj), yj, z0), V.pt(Xf(yj), yj, z0 + th)      # and the line of the joint on the far side
        s.line([a1, a2], "#2a2226", 0.7, 0.8)
    for zz, back in ((z1 + 0.25, None), (z0 + th + 0.1, None)):         # rubber feet
        q = [(Xf(0.0), 0.0, zz), (Xf(4.5), 4.5, zz), (Xb(4.5), 4.5, zz), (Xb(0.0), 0.0, zz)]
        s.poly(V.poly(q), "#26201f")
    q = [(Xf(0.0), 0.0, z1 - th), (Xf(4.5), 4.5, z1 - th), (Xf(4.5), 4.5, z1), (Xf(0.0), 0.0, z1)]
    s.poly(V.poly(q), "#3a302c")
    # the light of The Retreat, in a thread down the front edges of the top rungs
    for k in range(L["treads"] - 2, L["treads"] + 1):
        yk = k * L["step"]
        xn = Xf(yk) - 0.8
        a1, a2 = V.pt(xn + 0.2, yk - 0.3, z0 + th + 1.0), V.pt(xn + 0.2, yk - 0.3, z1 - th - 1.0)
        s.line([a1, a2], "#ffd9a0", 0.7, 0.35 + 0.15 * (k - L["treads"] + 2))
    near_line(CEIL - 64.0, CEIL - 1.0, 0.04, "#ffd59a", 0.7, 0.65)

    # ---- Big Sister's card, tied on with a ribbon, flat against the near side
    X0, X1, Y0, Y1, Zc = card_place(L)
    ky = Y1 + 7.0                                               # the knot, on the side just above the card
    kx = (Xf(ky) + Xb(ky)) / 2
    knot = V.pt(kx, ky, Zc + 0.2)
    for hx in ((X0 + X1) / 2 - 14.0, (X0 + X1) / 2 + 14.0):
        s.line([V.pt(hx, Y1 - 2.6, Zc + 0.1), knot], "#b8505e", 0.75, 1.0)
    s.ellipse(knot[0], knot[1], 0.9, 0.8, "#c8606e")
    color, alpha = s.done()
    tex = TH.retreat_card().array()
    lt = light_at((X0 + X1) / 2, (Y0 + Y1) / 2, Zc, (0.0, 0.0, 1.0), boxes, state=NOW, attic=ATTIC_LADDER, extra=CARD_FILL)[0]
    cc, cv = plane_tex(tex, Zc, X0, X1, Y0, Y1, k=4)
    cc = expose(cc, lt[None, None, :])
    over(color, cc, cv)
    alpha = np.maximum(alpha, cv)
    # the ribbon goes over the card's top edge to its holes: say it again on top
    s2 = Sheet(SHAPE)
    for hx in ((X0 + X1) / 2 - 14.0, (X0 + X1) / 2 + 14.0):
        p = V.pt(hx, Y1 - 2.6, Zc + 0.1)
        s2.line([p, (p[0] + (knot[0] - p[0]) * 0.18, p[1] + (knot[1] - p[1]) * 0.18)], "#b8505e", 0.75, 1.0)
    c2, a2 = s2.done()
    over(color, c2, a2)
    return color, alpha


def ladder_shadow(pic, R):
    """Where the ladder's feet meet the floor: dark close under each foot, a soft dimness under its low end."""
    L = LADDER
    _, _, _, _, Xf, Xb = ladder_frame(L)
    z0, z1, th = L["z"][0], L["z"][1], L["thick"]
    s = Sheet(SHAPE)
    x0, x1 = Xb(0.0) - 9.0, Xf(0.0) + 7.0
    s.poly(V.poly([(x0, 0.3, z0 - 5), (x1, 0.3, z0 - 5), (x1, 0.3, z1 + 6), (x0, 0.3, z1 + 6)]), "#1a1420", 0.22)
    for zz in (z0 + th / 2, z1 - th / 2):
        s.poly(V.poly([(Xb(0.0) - 2.5, 0.3, zz - 3.2), (Xf(0.0) + 3.0, 0.3, zz - 3.2), (Xf(0.0) + 3.0, 0.3, zz + 3.2), (Xb(0.0) - 2.5, 0.3, zz + 3.2)]), "#1a1420", 0.75)
    sc, sa = s.done()
    floors = tags_of(R, "landing")
    tint(pic, "#2a2030", (blur(sa, 1.4) * floors).astype(F32) * 0.95)


def ladder_ground_mask(R):
    """The same, as a mask (for laying it on the picture as it was)."""
    p = np.zeros(SHAPE + (3,), dtype=F32) + 1.0
    ladder_shadow(p, R)
    return p


# ====================================================================== the railing (front plane)
RAIL_Z = 175.0
POSTS = [108.0, 276.0, 444.0, 612.0]                        # newel posts along the landing's edge (as the living room has them)
QUILT = (698.0, 766.0)                                      # a patchwork quilt hung over the railing to air: X0, X1


def as_wood(c):
    """The same light on dark wood instead of white paint (for the handrails)."""
    c = rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)
    return np.clip(c * np.array([0.50, 0.33, 0.25], dtype=F32) + np.array([0.02, 0.0, 0.0], dtype=F32), 0, 1)
WHITE = "#ebe4d3"


def baluster_profile(u):
    """How wide a turned baluster is at each height (u: 0 at its foot, 1 under the handrail), 1 = its square block."""
    pts = [(0.0, 1.0), (0.10, 1.0), (0.105, 0.62), (0.14, 0.9), (0.17, 0.55), (0.30, 1.02), (0.42, 0.86), (0.70, 0.5), (0.80, 0.46), (0.83, 0.8), (0.86, 0.5), (0.895, 1.0), (1.0, 1.0)]
    return float(np.interp(u, [p[0] for p in pts], [p[1] for p in pts]))


def rail_plane(R):
    """The white railing along the landing, its newel posts, the banister of the stairs, and the hanging light
    out in the room: everything people are always behind. -> (color, alpha)."""
    boxes = R["boxes"]
    asked = []
    draw_rail(Sheet(SHAPE), lambda X, Y, Z: (asked.append((float(X), float(Y), float(Z))) or (WHITE, WHITE, WHITE)), boxes)
    A = np.asarray(asked, dtype=F32)
    room = (0.19, 0.20, 0.27)
    top = tone_at(WHITE, A[:, 0], A[:, 1], A[:, 2], (0, 1, 0), boxes, extra=room)
    front = tone_at(WHITE, A[:, 0], A[:, 1], A[:, 2] + 2, (0, 0, 1), boxes, extra=room)
    side = tone_at(WHITE, A[:, 0] + 2, A[:, 1], A[:, 2], (1, 0, 0), boxes, extra=(0.17, 0.165, 0.19))
    top, front, side = (np.atleast_2d(q) for q in (top, front, side))
    turn = iter(range(len(asked)))

    def answer(X, Y, Z):
        i = next(turn)
        return top[i], front[i], side[i]
    s = Sheet(SHAPE)
    draw_rail(s, answer, boxes)
    return s.done()


def draw_rail(s, tones, boxes):
    """`tones(X, Y, Z)` -> the paint's color on the faces a thing there shows us: (top, the face toward us, the face toward +X)."""
    shape = SHAPE

    def quad(pts3, color, alpha=1.0):
        pp = V.poly(pts3)
        if len(pp) >= 3:
            s.poly(pp, color, alpha)

    def upright(X, Z, y0, y1, sect, turned_=True, cool=None):
        """One baluster: a square foot and head with a turned shaft between, the face toward us and the face
        toward +X each in the light that reaches them."""
        mid = (y0 + y1) / 2
        _, cf, cs = tones(X, mid, Z)
        xa, ya = V.pt(X, y0, Z)
        xb, yb = V.pt(X, y1, Z)
        k = V.scale_at(X, Z)
        wfull = max(sect * k * 1.25, 1.9)                    # a square seen corner-on is wider than its side
        n = 14 if wfull > 2.6 else 1
        for i in range(n):
            u0, u1 = i / n, (i + 1) / n
            w = wfull * (baluster_profile((u0 + u1) / 2) if (turned_ and n > 1) else (1.0 if n > 1 else 0.86))
            w = max(w, 1.7)
            ytop, ybot = lerp(ya, yb, u1), lerp(ya, yb, u0)
            cx = round(xa * 2) / 2 if wfull < 2.6 else xa
            split = cx - w / 2 + w * 0.46
            s.poly([(cx - w / 2, ybot), (split, ybot), (split, ytop), (cx - w / 2, ytop)], cf)
            s.poly([(split, ybot), (cx + w / 2, ybot), (cx + w / 2, ytop), (split, ytop)], cs)

    # ---- the stair banister first (it is farther from us than the landing's rail where they meet)
    zt, zf = STAIR["z_top"], STAIR["z_foot"]
    xs = 108.0
    for i in range(STAIR["steps"] - 1):
        z1 = zf - GOING * i
        for dz in (5.5, 18.0):
            z = z1 - dz
            upright(xs, z, step_top(i), float(stair_line(z)) + 86.0 + RISE * 0.5, 3.0)
    # its handrail: a sloping bar, in short lengths so that each takes the light where it is
    n = 16
    for i in range(n):
        za, zb = lerp(zf + 6, zt, i / n), lerp(zf + 6, zt, (i + 1) / n)
        ya_, yb_ = float(-G + G * (zf - za) / (zf - zt)) + 95.0, float(-G + G * (zf - zb) / (zf - zt)) + 95.0
        ct, cf, cs = tones(xs, (ya_ + yb_) / 2, (za + zb) / 2)
        quad([(xs - 3.5, ya_, za), (xs + 3.5, ya_, za), (xs + 3.5, yb_, zb), (xs - 3.5, yb_, zb)], as_wood(ct) * 1.25)
        quad([(xs + 3.5, ya_, za), (xs + 3.5, yb_, zb), (xs + 3.5, yb_ - 6.5, zb), (xs + 3.5, ya_ - 6.5, za)], as_wood(cs))
        a, b = V.pt(xs + 3.5, ya_ - 6.5, za), V.pt(xs + 3.5, yb_ - 6.5, zb)
        s.line([a, b], "#1c1218", 0.7, 0.7)
        a, b = V.pt(xs + 3.5, ya_, za), V.pt(xs + 3.5, yb_, zb)
        s.line([a, b], np.clip(as_wood(ct) * 2.2, 0, 1), 0.6, 0.6)
    # the newel at the foot of the stairs (its top just shows at the bottom-left corner)
    def newel(X, Z, base, tall=102.0, sect=10.0):
        h = sect / 2
        ct, cf, cs = tones(X, base + tall * 0.6, Z)
        quad([(X - h, base, Z + h), (X + h, base, Z + h), (X + h, base + tall, Z + h), (X - h, base + tall, Z + h)], cf)
        quad([(X + h, base, Z - h), (X + h, base, Z + h), (X + h, base + tall, Z + h), (X + h, base + tall, Z - h)], cs)
        c = h + 2.2                                          # the cap: a flat square, then a ball
        ctop, cfr, csd = tones(X, base + tall + 3, Z)
        quad([(X - c, base + tall, Z + c), (X + c, base + tall, Z + c), (X + c, base + tall + 3.5, Z + c), (X - c, base + tall + 3.5, Z + c)], cfr)
        quad([(X + c, base + tall, Z - c), (X + c, base + tall, Z + c), (X + c, base + tall + 3.5, Z + c), (X + c, base + tall + 3.5, Z - c)], csd)
        quad([(X - c, base + tall + 3.5, Z - c), (X + c, base + tall + 3.5, Z - c), (X + c, base + tall + 3.5, Z + c), (X - c, base + tall + 3.5, Z + c)], ctop)
        bx_, by_ = V.pt(X, base + tall + 8.5, Z)
        r = 5.4 * V.scale_at(X, Z)
        s.ellipse(bx_, by_, r, r, cfr)
        s.ellipse(bx_ + r * 0.28, by_ - r * 0.1, r * 0.72, r * 0.8, csd)
        s.ellipse(bx_ + r * 0.3, by_ - r * 0.38, r * 0.3, r * 0.3, ctop, 0.9)
        for yy in (base + tall * 0.2, base + tall * 0.86):   # two grooves cut round it
            s.line([V.pt(X - h, yy, Z + h), V.pt(X + h, yy, Z + h), V.pt(X + h, yy, Z - h)], "#5a5262", 0.7, 0.55)
    newel(xs, zf + 6.0, -G)

    # ---- the landing's railing: a shoe along the edge, balusters every 12.5 cm, the handrail, the posts
    x_end = 900.0
    step_ = 20.0
    xx = 108.0
    while xx < x_end:                                        # the shoe rail the balusters stand in
        xb = min(xx + step_, x_end)
        ct, cf, cs = tones((xx + xb) / 2, 5.0, RAIL_Z)
        quad([(xx, 0.0, RAIL_Z + 3.5), (xb, 0.0, RAIL_Z + 3.5), (xb, 5.0, RAIL_Z + 3.5), (xx, 5.0, RAIL_Z + 3.5)], cf)
        quad([(xx, 5.0, RAIL_Z - 3.5), (xb, 5.0, RAIL_Z - 3.5), (xb, 5.0, RAIL_Z + 3.5), (xx, 5.0, RAIL_Z + 3.5)], ct)
        xx = xb
    xx = 108.0 + 12.5
    while xx < x_end:
        if min(abs(xx - p) for p in POSTS) > 8.0:
            upright(xx, RAIL_Z, 5.0, 88.5, 3.4)
        xx += 12.5
    xx = 108.0
    while xx < x_end:                                        # the handrail
        xb = min(xx + step_, x_end)
        ct, cf, cs = tones((xx + xb) / 2, 95.0, RAIL_Z)
        quad([(xx, 88.0, RAIL_Z + 4.0), (xb, 88.0, RAIL_Z + 4.0), (xb, 95.0, RAIL_Z + 4.0), (xx, 95.0, RAIL_Z + 4.0)], as_wood(cf))
        quad([(xx, 95.0, RAIL_Z - 4.0), (xb, 95.0, RAIL_Z - 4.0), (xb, 95.0, RAIL_Z + 4.0), (xx, 95.0, RAIL_Z + 4.0)], np.clip(as_wood(ct) * 1.3, 0, 1))
        a, b = V.pt(xx, 88.0, RAIL_Z + 4.0), V.pt(xb, 88.0, RAIL_Z + 4.0)
        s.line([a, b], "#1c1218", 0.7, 0.6)
        a, b = V.pt(xx, 95.0, RAIL_Z + 4.0), V.pt(xb, 95.0, RAIL_Z + 4.0)
        s.line([a, b], np.clip(as_wood(ct) * 2.4, 0, 1), 0.6, 0.6)                 # the polished edge
        xx = xb
    for px_ in POSTS:
        newel(px_, RAIL_Z, 0.0)

    # ---- a patchwork quilt hung over the railing to air (the living room sees it from below)
    xa, xb = QUILT
    patch = np.array([[0.62, 0.20, 0.18], [0.82, 0.74, 0.56], [0.20, 0.30, 0.50], [0.74, 0.56, 0.22], [0.30, 0.46, 0.36], [0.84, 0.80, 0.72]], dtype=F32)
    pick = np.random.default_rng(6).integers(0, 6, size=(12, 12))
    ct, cf, cs = tones((xa + xb) / 2, 60.0, RAIL_Z + 6)
    k_front = (rgb(cf) if isinstance(cf, str) else np.asarray(cf)) / rgb(WHITE)
    k_top = (rgb(ct) if isinstance(ct, str) else np.asarray(ct)) / rgb(WHITE)
    z_top, z_hem = RAIL_Z + 5.0, RAIL_Z + 6.5

    def hem(X):                                              # the quilt hangs a little crooked
        return lerp(30.0, 22.0, (X - xa) / (xb - xa))
    quad([(xa, 96.5, RAIL_Z - 5), (xb, 96.5, RAIL_Z - 5), (xb, 96.5, z_top), (xa, 96.5, z_top)], np.clip(patch[1] * k_top, 0, 1))
    i = 0
    while xa + i * 9.0 < xb - 0.5:
        x0_, x1_ = xa + i * 9.0, min(xa + (i + 1) * 9.0, xb)
        j = 10
        while j * 9.0 > hem(x0_) - 9.0:
            y1_ = min((j + 1) * 9.0, 96.5)
            y0_ = max(j * 9.0, hem((x0_ + x1_) / 2))
            if y1_ > y0_:
                def at(X, Y):
                    f = (96.5 - Y) / 74.0
                    return V.pt(X + f * 1.5, Y, lerp(z_top, z_hem, f))
                fold = 0.86 + 0.20 * math.sin((x0_ - xa) / 11.0 + y0_ * 0.05)
                c = np.clip(patch[pick[i % 12, j % 12]] * k_front * fold, 0, 1)
                s.poly([at(x0_, y0_), at(x1_, y0_), at(x1_, y1_), at(x0_, y1_)], c)
                if (i + j) % 2 == 0 and y1_ - y0_ > 8.0:   # half the squares are cut corner to corner
                    c2 = np.clip(patch[pick[j % 12, i % 12]] * k_front * fold, 0, 1)
                    s.poly([at(x1_, y0_), at(x1_, y1_), at(x0_, y1_)], c2)
            j -= 1
        i += 1
    s.line([V.pt(xa, 96.5, z_top), V.pt(xb, 96.5, z_top)], np.clip(patch[5] * k_top, 0, 1), 0.8, 0.8)

    # ---- the hanging light out in the room: brass, six arms with frosted glass cups, on a long chain from a
    #      beam; not lit tonight, but it catches the lamps. From up here we look down on it.
    cx, cz, y0, rr = LIGHT_AT[0], LIGHT_AT[2], LIGHT_AT[1] - 26.0, 38.0
    y1 = y0 + 74.0
    brass_d, brass, brass_l, glint = "#4a3418", "#8a6626", "#b98e3c", "#f2d488"
    top_ = V.pt(cx, CEIL - BEAM_DEEP, cz)
    hub = V.pt(cx, y1 + 6.0, cz)
    for k in range(int((hub[1] - top_[1]) / 4.6)):           # the chain, link by link
        yy = top_[1] + k * 4.6
        if k % 2:
            s.ellipse(top_[0], yy + 2.3, 1.5, 2.9, brass_d)
        else:
            s.line([(top_[0], yy), (top_[0], yy + 4.8)], brass, 1.1)
    s.poly(hull(ring(cx, CEIL - BEAM_DEEP, cz, 8.0) + ring(cx, CEIL - BEAM_DEEP - 4.0, cz, 5.0)), brass_d)   # the rose it hangs from
    arms = []
    for k in range(6):
        a = math.radians(k * 60 + 18)
        arms.append((math.cos(a), math.sin(a)))
    order = sorted(arms, key=lambda d: V.depth(cx + d[0] * rr, cz + d[1] * rr), reverse=True)

    def arm(dx_, dz_):
        ex, ez = cx + dx_ * rr, cz + dz_ * rr
        pts = [V.pt(cx + dx_ * 7, y0 + 32, cz + dz_ * 7), V.pt(cx + dx_ * rr * 0.55, y0 + 17, cz + dz_ * rr * 0.55), V.pt(ex - dx_ * 4, y0 + 15, ez - dz_ * 4), V.pt(ex, y0 + 24, ez)]
        s.line(curve(pts, 6), brass, 2.6)
        s.line(curve([(p[0] + 0.5, p[1] - 0.6) for p in pts], 6), brass_l, 0.9, 0.8)
        turned(s, ex, ez, [(y0 + 23, 1.4), (y0 + 27, 5.4), (y0 + 28.5, 5.4)], [brass, brass_l])
        turned(s, ex, ez, [(y0 + 28.5, 3.0), (y0 + 36, 7.0), (y0 + 44, 8.0), (y0 + 47, 6.8)], ["#5f6578", "#747b90", "#868da2"])   # a frosted glass shade
        s.poly(ring(ex, y0 + 47, ez, 6.8, 12), "#a2a9ba")
        s.poly(ring(ex, y0 + 46, ez, 5.0, 12), "#454a5e")
        g1, g2 = V.pt(ex + 4.0, y0 + 33, ez - 2.5), V.pt(ex + 6.0, y0 + 43, ez - 2.5)
        s.line([g1, g2], "#ffe2b0", 0.9, 0.9)                # a lamp below finds the glass
    for d_ in order[:3]:
        arm(*d_)
    turned(s, cx, cz, [(y0 - 5, 4.2), (y0 + 2, 0.6), (y0 + 8, 5.5), (y0 + 16, 2.6), (y0 + 30, 8.0), (y0 + 38, 9.0), (y0 + 48, 3.6), (y1 - 10, 4.6), (y1 + 6, 1.6)],
           [brass_d, brass, brass_d, brass, brass_l, brass, brass_d, brass])
    hx_, hy_ = V.pt(cx + 4.0, y0 + 34, cz - 3.0)
    s.ellipse(hx_, hy_, 1.4, 3.2, glint, 0.9)
    for d_ in order[3:]:
        arm(*d_)


# ====================================================================== the study door standing open
def study_details(pic, R):
    """What is seen through the open door: the lamp on Dad's desk, its glow, papers."""
    s = Sheet(SHAPE)
    table_lamp(s, STUDY_LAMP[0], 76.0, STUDY_LAMP[2], 1.0)
    for k, (px_, pz_, c) in enumerate(((588.0, -282.0, "#f4eedc"), (644.0, -276.0, "#e8dcae"), (600.0, -310.0, "#dfe8f2"))):       # papers and maps on the desk
        s.poly(V.poly([(px_, 76.4, pz_), (px_ + 16, 76.4, pz_ + 3), (px_ + 14, 76.4, pz_ + 16), (px_ - 2, 76.4, pz_ + 13)]), c)
    a, b = V.pt(652.0, 44.5, -186.0), V.pt(668.0, 66.0, -176.0)                 # a rolled map sticking out of the box
    s.line([a, b], "#e9e0c4", 2.2)
    sc, sa = s.done()
    inside = tags_of(R, "study-floor", "study-far", "study-desk", "study-desk-top", "study-box", "study-cooler", "study-cooler-lid")
    over(pic, sc, sa * inside)
    lx, ly = V.pt(STUDY_LAMP[0], 116.0, STUDY_LAMP[2])
    glow(pic, "#ffcf8a", mask_ellipse(SHAPE, lx, ly, 30, 26, soft=9) * 0.22 * inside)
    # the edge of the door and its knob
    e = Sheet(SHAPE)
    k1 = V.pt(STUDY[0] + 5.5, 99.0, -78.0)
    e.ellipse(k1[0] + 1.5, k1[1], 2.6, 3.0, "#c79c44")
    e.ellipse(k1[0] + 2.2, k1[1] - 0.8, 1.0, 1.1, "#f8e6a8")
    ec, ea = e.done()
    over(pic, ec, ea * tags_of(R, "study-leaf", "study-floor", "study-far"))


def study_open_plane(base_closed, fast=False):
    """The same picture with the study door standing open; only what differs is kept. -> (color, alpha)."""
    Ro = render(ss=1 if fast else 2, open_study=True)
    bo = hand(Ro["pic"], Ro)
    po = brushed(bo, seed=5, fast=fast)
    if not fast:
        restate(po, bo, Ro)
    details(po, Ro, fast)
    study_details(po, Ro)
    x, y = grid(SHAPE)
    door = mask_poly(SHAPE, V.poly([(STUDY[0] - 0.3, 0, 0), (STUDY[1] + 0.3, 0, 0), (STUDY[1] + 0.3, DOOR_H + 0.3, 0), (STUDY[0] - 0.3, DOOR_H + 0.3, 0)]))
    diff = np.abs(bo - base_closed).max(axis=2)
    spill = (blur((diff > 0.05).astype(F32), 0.7) > 0.5) & tags_of(Ro, "landing")
    alpha = np.maximum(door > 0.5, spill).astype(F32)
    alpha *= (x > 540)
    return po, alpha, Ro


# ====================================================================== finishing, and the files
def grained(picture, seed=7, amount=0.014):
    lum = (picture @ np.array([0.3, 0.55, 0.15], dtype=F32))[..., None]
    return np.clip(picture + (grain(picture, seed, amount) - picture) * (0.3 + 1.1 * lum), 0, 1)


def finish_parts(picture, colors=128, alpha=None, seed=7, speckle=0.010, amount=0.014):
    """-> (the grained picture, its palette, the palette picture)."""
    g = grained(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    return g, pal, idx


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.010, amount=0.014):
    g, pal, idx = finish_parts(picture, colors, alpha, seed, speckle, amount)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def finish_over(picture, changed, pal_then, idx_then, name, extra=8, speckle=0.010):
    """Finish a picture that is the old one with some places changed: every pixel that did not change keeps
    exactly the color it had (same palette, same index); the changed ones are grained and put into the old
    palette, which gains up to `extra` colors for what it had no color for."""
    g = grained(picture)
    sel = changed > 0.5
    pal = np.asarray(pal_then, dtype=F32)
    if sel.any() and extra:
        px = g[sel].reshape(-1, 3)
        err = ((px[:, None, :] - pal[None, :, :]) ** 2).sum(axis=2).min(axis=1)
        far = px[err > 0.0025]
        if len(far) > extra * 4:
            more = palette_of([far.reshape(-1, 1, 3)], colors=extra, seed=11)
            pal = np.concatenate([pal, more]).astype(F32)
    idx_new = to_palette(g, pal, speckle=speckle)
    idx = np.where(sel, idx_new, idx_then).astype(np.uint8)
    save(name, idx, pal)
    return os.path.getsize(name), len(pal), int(sel.sum())


def save_rgb(a, name):
    Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)).save(name)


def lettering_mask(open_study=False, state=None):
    """Where the words are that must be read: they are kept exactly as lettered."""
    s = Sheet(SHAPE)
    if (state or THEN)["ladder"]:                            # BEWARE OF CHICKENS, on her door
        bx0, by0, bx1, by1 = TH.BEWARE
        x0 = LILSIS[0] - 10.0
        s.poly(V.poly([(x0 + bx0, by0, 0), (x0 + bx1, by0, 0), (x0 + bx1, by1, 0), (x0 + bx0, by1, 0)]), "#ffffff")
    if not open_study:
        s.poly(V.poly([(SIGN[0], SIGN[2], 0), (SIGN[1], SIGN[2], 0), (SIGN[1], SIGN[3], 0), (SIGN[0], SIGN[3], 0)]), "#ffffff")
    s.poly(V.poly([(SON[0] + 3, 124, 0), (SON[1] - 3, 124, 0), (SON[1] - 3, 187, 0), (SON[0] + 3, 187, 0)]), "#ffffff")
    return s.done()[1]


def hand(base, R, seed=7):
    """Nothing in a painting is ruled: let every edge wander by half a pixel (the lettering stays as lettered)."""
    out = warp(base, 0.55, 15.0, seed)
    keep = lettering_mask(R["open"], R.get("state"))
    return lerp(out, base, keep[..., None]).astype(F32)


# ====================================================================== the numbers the game needs
def P2(X, Z, Y=0.0):
    x, y = V.pt(X, Y, Z)
    return [int(round(x)), int(round(y))]


def outline(pts3):
    """Room points -> a picture polygon kept inside the picture."""
    pp = V.poly(pts3)
    return [[int(round(min(max(x, 0), W - 1))), int(round(min(max(y, 0), H - 1)))] for x, y in pp]


def bounds(pts3, pad=0):
    pp = outline(pts3)
    xs, ys = [p[0] for p in pp], [p[1] for p in pp]
    x0, y0, x1, y1 = max(0, min(xs) - pad), max(0, min(ys) - pad), min(W, max(xs) + pad), min(H, max(ys) + pad)
    return [x0, y0, x1 - x0, y1 - y0]


def inside(pt, poly):
    x, y = pt
    n, hit = len(poly), False
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            hit = not hit
    return hit


def wall_quad(x0, x1, y0, y1, z=0.0):
    return [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)]


def layout():
    walk = outline([(X, 0.0, Z) for X, Z in M.WALK])
    ground = outline([(X, 0.0, Z) for X, Z in LADDER_GROUND])
    L = {"id": M.ID, "horizon": M.VIEW["horizon"], "full": M.VIEW["full"], "eye_cm": round(V.eye), "view": M.VIEW,
         "light": "night: a warm lamp on the hall table (right of the middle), cool moonlight from the tall window on the left, a warm glow from the living room below",
         "walk": walk, "blocked": [ground]}
    base_line = [P2(*LADDER_BASE[0]), P2(*LADDER_BASE[1])]
    L["planes"] = [
        {"id": "rail", "file": "rail.png", "plane": "front", "what": "the whole railing (white balusters, dark handrail, newel posts), the banister of the stairs, the quilt hung over the rail, and the hanging light out in the room"},
        {"id": "study-open", "file": "study-open.png", "base": [P2(STUDY[0], 0), P2(STUDY[1], 0)], "state": "the study door stands open (laid exactly over the shut door; people are always in front of it)"},
        {"id": "ladder", "file": "ladder.png", "base": base_line, "what": "the attic ladder let down from the open hatch, the hatch's door hanging with it, Big Sister's card on it (THE RETREAT); its base is the line under its near side out to its feet: people between it and the wall are behind it, people between it and the rail in front"},
    ]

    def stand(name):
        (X, Z), face = M.STANDS[name]
        return {"stand": P2(X, Z), "face": face, "grownup_px": int(round(V.person(X, Z)[2]))}
    # the ladder: its outline as the lens sees it (both sides, top to feet, and the hatch's door behind its top)
    Ls, _, _, at, Xf, Xb = ladder_frame()
    z0, z1 = LADDER["z"]
    pts = []
    for z in (z0, z1):
        pts += [V.pt(Xf(Y), Y, z) for Y in (0.0, CEIL)] + [V.pt(Xb(Y), Y, z) for Y in (0.0, CEIL)]
    for z in (z0 - 3.0, z1 + 3.0):
        pts += [V.pt(*at(s_, LADDER["deep"] + 2.2), z) for s_ in (0.0, LADDER["door"])]
    ladder_poly = [[int(round(min(max(x, 0), W - 1))), int(round(min(max(y, 0), H - 1)))] for x, y in hull(pts)]
    X0, X1, Y0, Y1, Zc = card_place()
    card_rect = bounds([(X0, Y0, Zc), (X1, Y0, Zc), (X1, Y1, Zc), (X0, Y1, Zc)], 1)
    hx0, hx1, hz0, hz1 = HATCH2
    opening = outline([(hx0, CEIL, hz0), (hx1, CEIL, hz0), (hx1, CEIL, hz1), (hx0, CEIL, hz1)])
    (wz0, wz1), (wy0, wy1) = WINDOW["Z"], WINDOW["Y"]
    stairs_shape = outline([(2, 0, 176), (106, 0, 176), (106, float(stair_line(330.0)), 330), (2, float(stair_line(330.0)), 330)])
    things = [
        dict(id="son", what="the Son's door: his notices, his KEEP OUT sign, the toy alarm by the handle (it stays shut)", shape={"poly": outline(wall_quad(SON[0], SON[1], 0, DOOR_H))}, **stand("son")),
        dict(id="lilsis", what="Little Sister's door, hers alone now: one name-plate buried in chicken stickers, her crayon drawing of a hen taped on at her height, and her hand-lettered sign BEWARE OF CHICKENS", shape={"poly": outline(wall_quad(LILSIS[0], LILSIS[1], 0, DOOR_H))}, **stand("lilsis")),
        dict(id="study", what="Dad's study door", shape={"poly": outline(wall_quad(STUDY[0], STUDY[1], 0, DOOR_H))}, **stand("study")),
        dict(id="sign", what="Dad's notice taped to the study door", shape={"poly": outline(wall_quad(SIGN[0], SIGN[1], SIGN[2], SIGN[3]))}, **stand("sign")),
        dict(id="halltable", what="the hall table: the lamp (lit), the key bowl, the day's post", shape={"rect": bounds([(TABLE[0], 0, TABLE[4]), (TABLE[1], 0, TABLE[4]), (TABLE[0], 140, 2), (TABLE[1], 140, 2), (TABLE[1], 0, 2)], 2)}, **stand("halltable")),
        dict(id="chart", what="the long strip of paper pinned up over the hall table: a countdown to the trip, days crossed off, a little red car at the end", shape={"rect": bounds(wall_quad(CHART[0], CHART[1], CHART[2], CHART[3]))}, **stand("halltable")),
        dict(id="photos", what="framed family photographs", shape={"rect": bounds(wall_quad(293, 387, 105, 179))}, **stand("photos")),
        dict(id="hamper", what="the laundry hamper, folded washing on its lid", shape={"rect": bounds([(HAMPER[0], 0, HAMPER[4]), (HAMPER[1], 0, HAMPER[4]), (HAMPER[0], 72, 2), (HAMPER[1], 72, 2)], 2)}, **stand("hamper")),
        dict(id="ladder", what="the attic ladder, let down from the open hatch to the floor: the way up to Big Sister's room, The Retreat (soft warm light up there); her card hangs on it at eye height: THE RETREAT (ladder.png)", shape={"poly": ladder_poly}, card=card_rect, hatch=opening, **stand("ladder")),
        dict(id="window", what="the tall stair window: the moon, the tree", shape={"poly": outline([(0, wy0, wz1), (0, wy0, wz0), (0, wy1, wz0), (0, wy1, wz1)])}, **stand("window")),
        dict(id="rail", what="the railing: look down on the living room", shape={"rect": bounds([(250, 0, 175), (560, 0, 175), (560, 96, 175), (250, 96, 175)])}, **stand("rail")),
        dict(id="stairs", what="the stairs down to the living room", shape={"poly": stairs_shape}, **stand("stairs")),
        dict(id="bag", what="the Son's school bag on its peg, his shoes under it (look only)", shape={"rect": bounds([(BAG[0] - 6, 0, 30), (BAG[1] + 2, 0, 30), (BAG[0] - 6, 112, 0), (BAG[1] + 2, 112, 0)], 1)}, stand=P2(156, 90), face="N"),
        dict(id="quilt", what="a patchwork quilt hung over the railing to air (part of rail.png)", shape={"rect": bounds([(QUILT[0], 22, 182), (QUILT[1], 22, 182), (QUILT[0], 97, 170), (QUILT[1], 97, 170)])}, stand=P2(672, 140), face="S"),
        dict(id="chandelier", what="the hanging light out over the living room, not lit tonight (part of rail.png)", shape={"rect": bounds([(LIGHT_AT[0] - 46, LIGHT_AT[1] - 32, LIGHT_AT[2]), (LIGHT_AT[0] + 46, LIGHT_AT[1] + 26, LIGHT_AT[2])])}, **stand("rail")),
        dict(id="living-room", what="the living room below: the rug, the piano and its lamp, the kitchen doorway, the bookcase, the front door", shape={"rect": [320, 400, 480, 200]}, **stand("rail")),
    ]
    L["things"] = things
    L["exits"] = [
        {"to": "home-living-room", "way": "stairs", "shape": {"poly": stairs_shape}, "stand": P2(*M.STANDS["stairs"][0])},
        {"to": "home-lilsis-room", "way": "lilsis", "shape": {"poly": outline(wall_quad(LILSIS[0], LILSIS[1], 0, DOOR_H))}, "stand": P2(*M.STANDS["lilsis"][0])},
        {"to": "home-study", "way": "study", "shape": {"poly": outline(wall_quad(STUDY[0], STUDY[1], 0, DOOR_H))}, "stand": P2(*M.STANDS["study"][0])},
        {"to": "home-bigsis-room", "way": "ladder", "shape": {"poly": ladder_poly}, "stand": P2(*M.STANDS["ladder"][0])},
    ]
    L["marks"] = {way: {who: P2(X, Z) for who, (X, Z) in folk.items()} for way, folk in M.WAYS.items()}
    L["stands"] = {name: P2(X, Z) for name, ((X, Z), face) in M.STANDS.items()}
    L["sizes"] = {way: {who: int(round(V.person(X, Z, {"lilsis": 118.0, "bigsis": 158.0, "mom": 168.0}[who])[2])) for who, (X, Z) in folk.items()} for way, folk in M.WAYS.items()}
    L["vanishing"] = {"along_the_landing": [round(V.vanishing()[1][0]), 135], "out_toward_us": [round(V.vanishing()[0][0]), 135]}
    L["notes"] = ["The rail plane is drawn over everybody: people are seen through its balusters from the knee down.",
                  "Below the landing's edge everything is the living room, 285 cm lower: nobody walks there in this picture.",
                  "Not painted (the game lights them): the lamp of the Son's toy alarm (beside his door handle).",
                  "The attic ladder (ladder.png) stands with its feet just in front of the study door's left edge. People pass it in front (between it and the rail) and stand behind it under its high end, at the hall table. Its blocked ground reaches back to the wall: there is no way past behind its feet (the floor here is about 30 px deep, and the game keeps people 5 px clear of blocked ground above and below)."]
    # every place a person is sent to must be on the floor people may stand on, and not where the ladder stands
    for name, pt in list(L["stands"].items()) + [(f"{w}.{k}", p) for w, d in L["marks"].items() for k, p in d.items()] + [(t["id"], t["stand"]) for t in things]:
        assert inside(pt, walk), (name, pt)
        assert not inside(pt, ground), (name, pt)
        assert 0 <= pt[0] < W and 0 <= pt[1] < H, (name, pt)
    return L


def paint(fast=False, open_study=False, window=(0, 0, W, H), state=None):
    R = render(ss=1 if fast else 2, open_study=open_study, window=window, state=state)
    base = R["pic"]
    return R, base


def painted(state, fast=False):
    """The four passes up to the finish, for one state of the landing. -> (R, the unbrushed base, the picture)."""
    R, base = paint(fast, state=state)
    base = hand(base, R)
    pic = brushed(base, fast=fast)
    if not fast:
        restate(pic, base, R)
    details(pic, R, fast)
    return R, base, pic


def change_masks(R_then, R_now):
    """Where the picture's CONTENT changes (her door, the ceiling round the old and the new hatch, the cord that is
    gone, the lamp and key bowl set down a little farther left). Everywhere else only the light changes."""
    def poly_mask(pts3, grow=0.0):
        m = mask_poly(SHAPE, V.poly(pts3))
        return (blur(m, grow) > 0.02).astype(F32) if grow else (m > 0.5).astype(F32)
    door = poly_mask(wall_quad(LILSIS[0] - 10.0, LILSIS[1] + 10.0, 0.0, 216.0), 0.6)
    hx0, hx1, hz0, hz1 = HATCH2
    ceil = np.maximum(poly_mask([(HATCH[0] - 3, CEIL, HATCH[2] - 3), (HATCH[1] + 3, CEIL, HATCH[2] - 3), (HATCH[1] + 3, CEIL, HATCH[3] + 3), (HATCH[0] - 3, CEIL, HATCH[3] + 3)], 1.5),
                      poly_mask([(hx0 - 9, CEIL, hz0 - 9), (hx1 + 9, CEIL, hz0 - 9), (hx1 + 9, CEIL, hz1 + 9), (hx0 - 9, CEIL, hz1 + 9)], 1.5))
    cx_, cy_ = V.pt((hx0 + hx1) / 2 + 4, CEIL + 3, (hz0 + hz1) / 2)
    ceil = np.maximum(ceil, (mask_ellipse(SHAPE, cx_, cy_, 44, 10, soft=6) > 0.01).astype(F32))
    ceil *= tags_of(R_now, "ceiling", "beam", "shaft", "attic") | tags_of(R_then, "ceiling", "beam")
    s = Sheet(SHAPE)                                          # the cord of the shut hatch, and its toggle
    cxh, czh = (HATCH[0] + HATCH[1]) / 2, HATCH[3] - 5
    p0, p1 = V.pt(cxh, CEIL - 0.5, czh), V.pt(cxh, 199.0, czh)
    s.poly([(p0[0] - 2.5, p0[1] - 1), (p0[0] + 3.5, p0[1] - 1), (p1[0] + 4.0, p1[1] + 9), (p1[0] - 3.5, p1[1] + 9)], "#ffffff")
    for st in (THEN, NOW):                                    # the lamp and the bowl, where they were and where they are
        lx_, lz_ = st["lamp"]
        table_lamp(s, lx_, TABLE[2], lz_, 1.22)
        bx_, bz_ = st["bowl"]
        turned(s, bx_, bz_, [(TABLE[2], 4.5), (TABLE[2] + 2.5, 6.5), (TABLE[2] + 6.5, 10.0)], ["#ffffff", "#ffffff"])
        s.poly(ring(bx_, TABLE[2] + 6.5, bz_, 10.0), "#ffffff")
    things = (blur(s.done()[1], 1.0) > 0.03).astype(F32)
    return np.clip(door + ceil + things, 0, 1)


def changed_picture(R_then, pic_then, R_now, pic_now):
    """The landing as delivered, with the two changes laid in: the changed content from the new painting, and the
    new light (the ladder's shadows, its feet on the floor) laid onto the old painting's own brushwork as a ratio,
    so that nothing the changes do not touch moves by a single pixel. -> (picture, mask of the changed pixels)."""
    content = change_masks(R_then, R_now)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(R_then["pic"] > 1e-3, R_now["pic"] / np.maximum(R_then["pic"], 1e-3), 1.0)
    ratio = np.clip(ratio, 0.25, 2.5).astype(F32)
    ratio = np.where((np.abs(ratio - 1.0).max(axis=2) > 0.004)[..., None], ratio, 1.0).astype(F32)
    ratio = warp(ratio, 0.55, 15.0, 7)                        # registered with the painting's own hand-drawn wobble
    ratio = np.where((np.abs(ratio - 1.0).max(axis=2) > 0.004)[..., None], ratio, 1.0).astype(F32)
    out = pic_then * ratio
    out = out * ladder_ground_mask(R_now)
    soft = np.clip(blur(content, 0.5) * 1.6, 0, 1)[..., None] * (content[..., None] > 0)
    out = out * (1 - soft) + pic_now * soft
    changed = (np.abs(out - pic_then).max(axis=2) > 1.0 / 1024).astype(F32)
    return np.clip(out, 0, 1).astype(F32), changed


def comp_files(name, layers):
    im = Image.open(f"{OUT}/back.png").convert("RGBA")
    for n in layers:
        im.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
    im.convert("RGB").save(name)


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = "fast" in sys.argv
    if fast:                                                  # composing: the new landing, unbrushed, the ladder and the rail on it
        R, base, pic = painted(NOW, fast=True)
        save_rgb(base, "out/home-landing-1-under.png")
        lc, la = ladder_plane(R)
        rc, ra = rail_plane(R)
        whole = pic.copy()
        over(whole, lc, (la > 0.5).astype(F32))
        save_rgb(whole, "out/home-landing-2-ladder.png")
        over(whole, rc, (ra > 0.5).astype(F32))
        save_rgb(whole, "out/home-landing-2-all.png")
        print("fast", round(time.time() - t0, 1))
        sys.exit()

    # ---- THEN: the landing exactly as it was delivered (rail.png and study-open.png are made from it, as before)
    R0, base0, pic0 = painted(THEN)
    rc, ra = rail_plane(R0)
    ra = (ra > 0.5).astype(F32)
    oc, oa, Ro = study_open_plane(base0, False)
    g0, pal0, idx0 = finish_parts(pic0, 152)
    print("then", round(time.time() - t0, 1))
    # ---- NOW: her door, the hatch open, the ladder down
    R1, base1, pic1 = painted(NOW)
    save_rgb(base1, "out/home-landing-1-under.png")
    back, changed = changed_picture(R0, pic0, R1, pic1)
    lc, la = ladder_plane(R1)
    la = (la > 0.5).astype(F32)
    print("now", round(time.time() - t0, 1))
    save_rgb(back, "out/home-landing-2-back.png")
    whole = back.copy()
    over(whole, lc, la)
    over(whole, rc, ra)
    save_rgb(whole, "out/home-landing-2-all.png")
    Image.fromarray((np.dstack([np.clip(lc, 0, 1), la]) * 255 + 0.5).astype(np.uint8), "RGBA").save("out/home-landing-2-ladder.png")
    Image.fromarray((changed * 255).astype(np.uint8)).save("out/home-landing-2-changed.png")
    print("back", finish_over(back, changed, pal0, idx0, f"{OUT}/back.png"))
    print("ladder", finish(lc, f"{OUT}/ladder.png", 64, la, speckle=0.008, amount=0.012))
    print("rail", finish(rc, f"{OUT}/rail.png", 56, ra, speckle=0.008, amount=0.012))
    print("study-open", finish(oc, f"{OUT}/study-open.png", 72, oa))
    json.dump(layout(), open(f"{OUT}/layout.json", "w"), indent=1)
    # everything laid together, to look at: the door shut, and the door open (the ladder stands in front of the door's foot)
    comp_files("out/home-landing-comp.png", ("ladder", "rail"))
    comp_files("out/home-landing-open-comp.png", ("study-open", "ladder", "rail"))
    print("done", round(time.time() - t0, 1))

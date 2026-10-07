"""Where everything stands at the foot of the pyramid (egypt_site.py): the measurements, and nothing painted.

The pyramid's near corner comes down at CORNER. Its shaded face runs off to the right, turning a little
away from us (PHI); its sunlit face runs away to the left, seen almost edge-on. It stands on a low bank
of chips, 1.2 m above the sand people walk on. The way in is a notch cut back into the shaded face with a
doorway in its upright back wall; a podium of mud brick stands before it and a flight of steps comes down
from the podium toward us."""

import math

import numpy as np

from egypt_site_kit import *

PHI, BETA = 17.1, 60.0                       # how far the shaded face turns from us; how steep the stone is
CORNER, CORNER_ZC = (268.0, 334.0), 2400.0   # the near corner's foot in the picture, and how far off it is
BASE = 10450.0                               # one side of the pyramid (it is a stage pyramid: only its foot is in the picture)

_c, _s = math.cos(math.radians(PHI)), math.sin(math.radians(PHI))
DX, NX = (_c, _s), (-_s, _c)                 # along the shaded face's foot; into the pyramid from it (X, Zc)
CX = (CORNER[0] - CAM.vx) * CORNER_ZC / FOC
CY = EYE - (CORNER[1] - HZ) * CORNER_ZC / FOC             # how high the pyramid's foot is above the sand
SHADE = Slope((CX, CY, CORNER_ZC), DX, NX, BETA, BASE)   # the face we mostly see
LIT = Slope((CX, CY, CORNER_ZC), NX, DX, BETA, BASE)     # the narrow sunlit one
TAN = math.tan(math.radians(BETA))
BANK = 130.0                                 # how far the bank of chips runs out from the pyramid's foot


def G(s, q, y=0.0):
    """World place `s` along the shaded face's foot, `q` into the pyramid from the foot line (negative:
    out toward us), `y` above the sand."""
    return (CX + s * DX[0] + q * NX[0], y, CORNER_ZC + s * DX[1] + q * NX[1])


def GP(s, q, y=0.0):
    return P(*G(s, q, y))


# ---- the pyramid's own shadow. Its near edge throws a line across the sand from where the edge would meet
# the flat ground (FOOT0), running to the right and a little toward us; everything beyond that line is in shade.
ARRIS = ((DX[0] + NX[0]) / TAN, 1.0, (DX[1] + NX[1]) / TAN)             # the near edge, per centimetre of height (X, Y, Zc)
FOOT0 = (CX - CY * ARRIS[0], 0.0, CORNER_ZC - CY * ARRIS[2])
SHADE_TURN = 4.0


def shadow_edge(X, Y=0.0):
    """How far off (Zc) the edge of the pyramid's shadow is, at a place X across and Y up. Beyond it is shade."""
    return FOOT0[2] + ARRIS[2] * Y - (X - FOOT0[0] - ARRIS[0] * Y) * math.tan(math.radians(SHADE_TURN))


def shaded(X, Y, Zc):
    return (Zc > shadow_edge(X, Y)) and (X > FOOT0[0] + ARRIS[0] * Y)


def floor_shade(shape):
    """The pyramid's shadow on the flat sand, as a mask: crisp by the corner, softer far along."""
    X, Z, below = floor_grid(shape)
    soft = 5.0 + np.clip(X - FOOT0[0], 0, None) * 0.035
    m = np.clip((Z - shadow_edge(X)) / soft + 0.5, 0, 1) * np.clip((X - FOOT0[0]) / 30.0 + 0.5, 0, 1)
    return (m * below).astype(F32)


# ---- the way in
NOTCH_S, NOTCH_W = 1075.0, 410.0             # middle of the notch along the foot, and its width
SILL, NOTCH_H = 190.0, 500.0                 # the floor of the notch above the pyramid's foot; its height
DOOR_W, DOOR_H, DOOR_OFF = 190.0, 258.0, 38.0     # the doorway in the back wall (shifted a little right of the middle)
LINTEL = 44.0
Q_BACK = (SILL + NOTCH_H) / TAN              # how far in the back wall stands
Q_FACE = SILL / TAN                          # how far in the casing is at the height of the sill
LAND_Y = CY + SILL                           # the landing's height above the sand


def back(u, v):
    """A place on the notch's back wall: `u` from its middle, `v` above the sill."""
    return G(NOTCH_S + u, Q_BACK, LAND_Y + v)


def backp(u, v):
    return P(*back(u, v))


# ---- the podium and the steps
POD_OUT = 150.0                              # the podium's front stands this far out from the pyramid's foot line
POD_S0, POD_S1 = NOTCH_S - NOTCH_W / 2 - 115, NOTCH_S + NOTCH_W / 2 + 85
STEPS, STAIR_W = 17, 150.0
STAIR_TOP_S = NOTCH_S + 95.0                 # where the middle of the top step is, along the podium's front
STAIR_FOOT = (716.0, 400.0)                  # where the middle of the bottom step meets the sand, in the picture
_top = G(STAIR_TOP_S, -POD_OUT, LAND_Y)
_fx, _fz = floor_at(*STAIR_FOOT)
_run = math.hypot(_fx - _top[0], _fz - _top[2])
AX = ((_fx - _top[0]) / _run, (_fz - _top[2]) / _run)       # down the steps, on the ground (X, Zc)
LAT = (AX[1], -AX[0]) if AX[1] < 0 else (-AX[1], AX[0])     # across them, toward our left
if LAT[0] > 0:
    LAT = (-LAT[0], -LAT[1])
RISE, TREAD, RUN = LAND_Y / STEPS, _run / STEPS, _run


def stair(along, side, y):
    """A place on the steps: `along` cm down from the top (on the ground), `side` -1 our left edge .. +1 right, `y` up."""
    return (_top[0] + AX[0] * along + LAT[0] * (-side) * STAIR_W / 2, y, _top[2] + AX[1] * along + LAT[1] * (-side) * STAIR_W / 2)


def stairp(along, side, y):
    return P(*stair(along, side, y))


def step_top(i):
    """Height of tread i (0 is the landing itself, STEPS is the sand)."""
    return LAND_Y - i * RISE


def stair_walk(t):
    """Where feet are, t = 0 at the foot of the steps .. 1 on the landing, in the picture."""
    i = (1 - t) * STEPS
    return stairp(i * TREAD, 0.0, LAND_Y - i * RISE)


# ---- the things on the sand (picture places of their feet)
SUNSPOT = (330.0, 520.0)
MARKS = {"scribe": (150, 448), "overseer": (360, 430), "hauler1": (300, 400), "hauler2": (270, 390), "hauler3": (240, 382), "guard": (690, 420)}
MAT = dict(at=(62.0, 474.0), turn=3.0, wide=255.0, deep=240.0, tall=205.0)        # the scribe's reed mat: near left corner, size; the awning's height
SLEDGE = dict(at=(420.0, 467.0), turn=-18.0)                                     # near front (left) corner of the sledge's runners; its tail comes toward us
STACK = dict(at=(612.0, 640.0), turn=-9.0)                                       # the waiting blocks, bottom right


def wire(path="out/egypt-site-wire.png"):
    """A drawing of the plan, to check places and sizes before any paint goes on."""
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (W, H), (236, 226, 204))
    d = ImageDraw.Draw(im)

    def ln(pts, col=(60, 60, 60), wd=1):
        d.line([(float(a), float(b)) for a, b in pts], fill=col, width=wd)

    ln([(0, HZ), (W, HZ)], (150, 170, 220))
    for face, col in ((SHADE, (110, 100, 170)), (LIT, (220, 150, 60))):
        ln([face.pt(0, 0), face.pt(face.L, 0)], col, 2)
        top = face.L / 2 * TAN
        ln([face.pt(0, 0), face.pt(face.L / 2, top)], col, 2)
        ln([face.pt(face.L, 0), face.pt(face.L / 2, top)], col, 1)
    for k in range(0, 14):
        ln([SHADE.pt(k * 105 / TAN, k * 105), SHADE.pt(3000, k * 105)], (190, 185, 215))
        ln([LIT.pt(k * 105 / TAN, k * 105), LIT.pt(9000, k * 105)], (240, 205, 150))
    for s in range(0, 2400, 200):
        ln([SHADE.pt(s, 0), SHADE.pt(s, 1100)], (205, 200, 225))
    # the bank
    ln([GP(s, -130, 0) for s in range(-200, 2400, 100)], (150, 120, 90))
    # notch, back wall, door
    s0, s1 = NOTCH_S - NOTCH_W / 2, NOTCH_S + NOTCH_W / 2
    ln([SHADE.pt(s0, SILL), SHADE.pt(s1, SILL), SHADE.pt(s1, SILL + NOTCH_H), SHADE.pt(s0, SILL + NOTCH_H), SHADE.pt(s0, SILL)], (40, 40, 90), 2)
    ln([backp(-NOTCH_W / 2, 0), backp(NOTCH_W / 2, 0), backp(NOTCH_W / 2, NOTCH_H), backp(-NOTCH_W / 2, NOTCH_H), backp(-NOTCH_W / 2, 0)], (90, 40, 40))
    u0, u1 = DOOR_OFF - DOOR_W / 2, DOOR_OFF + DOOR_W / 2
    d.polygon([backp(u0, 0), backp(u1, 0), backp(u1, DOOR_H), backp(u0, DOOR_H)], fill=(30, 24, 40))
    ln([backp(u0 - 60, DOOR_H + LINTEL), backp(DOOR_OFF, NOTCH_H - 20), backp(u1 + 60, DOOR_H + LINTEL)], (200, 60, 60), 2)
    # podium and steps
    ln([GP(POD_S0, -POD_OUT, LAND_Y), GP(POD_S1, -POD_OUT, LAND_Y), GP(POD_S1, -POD_OUT, 0), GP(POD_S0, -POD_OUT, 0), GP(POD_S0, -POD_OUT, LAND_Y), GP(POD_S0, Q_FACE, LAND_Y)], (120, 80, 40), 2)
    for i in range(STEPS + 1):
        ln([stairp(i * TREAD, -1, step_top(i)), stairp(i * TREAD, 1, step_top(i))], (160, 90, 30))
    ln([stairp(0, -1, LAND_Y), stairp(_run, -1, 0), stairp(0, -1, 0), stairp(0, -1, LAND_Y)], (120, 80, 40), 2)
    ln([stairp(0, 1, LAND_Y), stairp(_run, 1, 0)], (120, 80, 40), 2)
    # people, as posts of the height the game will draw them
    for name, (mx, my) in list(MARKS.items()) + [("sun", SUNSPOT)]:
        hgt = person(my)
        d.rectangle([mx - hgt * 0.13, my - hgt, mx + hgt * 0.13, my], outline=(200, 30, 30))
        d.text((mx - 10, my + 2), name, fill=(120, 0, 0))
    for t in (0.0, 0.5, 1.0):
        fx, fy = stair_walk(t)
        hgt = 175 * FOC / stair(0, 0, 0)[2] if t == 1 else person(fy) if t == 0 else 175 * FOC / ((stair(0, 0, 0)[2] + _fz) / 2)
        d.rectangle([fx - hgt * 0.13, fy - hgt, fx + hgt * 0.13, fy], outline=(30, 130, 30))
    # the mat and awning, the sledge, the stack
    m = Frame(MAT["at"], MAT["turn"])
    ln(m.pts([(0, 0, 0), (MAT["wide"], 0, 0), (MAT["wide"], 0, MAT["deep"]), (0, 0, MAT["deep"]), (0, 0, 0)]), (40, 120, 40))
    for u in (0, MAT["wide"]):
        for dd in (0, MAT["deep"]):
            ln(m.pts([(u, 0, dd), (u, MAT["tall"], dd)]), (40, 120, 40))
    ln(m.pts([(0, MAT["tall"], 0), (MAT["wide"], MAT["tall"], 0), (MAT["wide"], MAT["tall"], MAT["deep"]), (0, MAT["tall"], MAT["deep"]), (0, MAT["tall"], 0)]), (40, 120, 40), 2)
    sl = Frame(SLEDGE["at"], SLEDGE["turn"])
    for v in (22, 122):
        ln(sl.pts([(40, v, 8), (208, v, 8), (208, v, 108), (40, v, 108), (40, v, 8)]), (20, 20, 20))
    ln(sl.pts([(0, 0, 0), (235, 0, 0), (235, 0, 116), (0, 0, 116), (0, 0, 0)]), (90, 60, 30))
    st = Frame(STACK["at"], STACK["turn"])
    for v in (0, 105):
        ln(st.pts([(0, v, 0), (150, v, 0), (150, v, 130), (0, v, 130), (0, v, 0)]), (20, 20, 20))
    # the line from the sunny spot up to the doorway
    ln([(SUNSPOT[0] + 40, SUNSPOT[1] - 100), backp(DOOR_OFF, DOOR_H * 0.5)], (250, 200, 0), 1)
    im.save(path)
    info = dict(corner_top=SHADE.pt(1100 / TAN * 0 + 0, 0), door=[backp(u0, 0), backp(u1, DOOR_H)], landing=stair_walk(1.0), foot=stair_walk(0.0),
                rise=RISE, tread=TREAD, run=_run, land_y=LAND_Y, door_zc=back(0, 0)[2], k_door=FOC / back(0, 0)[2], cy=CY)
    return info


if __name__ == "__main__":
    for key, val in wire().items():
        print(key, np.round(np.array(val, dtype=float), 1))

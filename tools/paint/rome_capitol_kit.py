"""The Capitol (rome-capitol): the measurements of the place, and the tools its scripts share.

Everything in the precinct is measured in centimetres through the game's own camera (persp.Camera with the scene's
depth, horizon 275 and full 590: the lens stands 344.5 cm above the paving), so that the people the game draws stand
in it at the right size. World places are (X across, from the line of sight, + to the right; Y up from the paving;
Z away from the lens). Buildings and statues that stand at an angle to us have a Frame of their own (rome_steps_kit:
u along the front, v back into it, h up).

The great temple stands far off (its steps begin some 60 metres away), because the camera stands low and looks
level: a temple this tall must be that far off for its pediment and the bronze chariot on its peak to be in the
picture. So the precinct in front of it is deep, and the things on it come forward toward us: the altar, the
dictator's chariot and his statue on the world, the row of kings with the boy's base in the middle of it, the hut,
the pen, the tablets. rome_capitol_plan.py draws all of it as plain blocks, to look at before painting.
"""

import math

import numpy as np

from brush import F32, rgb
from persp import Camera
from rome_steps_kit import Frame, Light, unit

W, H = 800, 600
SHAPE = (H, W)
HZ, FULL = 275, 590                                          # the master brief's depth: fixed
CAM = Camera(HZ, FULL)
EYE, FOC = CAM.eye, CAM.F                                    # 344.5 cm, 800 px
OUT = "out/rome-capitol"


def P(X, Y, Z):
    """A place in the world -> the picture."""
    k = FOC / Z
    return (CAM.vx + X * k, CAM.vy + (EYE - Y) * k)


def k_at(Z):
    return FOC / Z


def Z_row(y):
    """How far off the paving is at a picture row."""
    return EYE * FOC / (y - HZ)


def X_at(x, y):
    """The world X of a place on the paving seen at picture (x, y)."""
    return (x - CAM.vx) * Z_row(y) / FOC


def ground(x, y):
    """Picture point on the paving -> (X, Z)."""
    Z = Z_row(y)
    return ((x - CAM.vx) * Z / FOC, Z)


def scale_at(y):
    return (y - HZ) / (FULL - HZ)


# ---------------------------------------------------------------- light: the sun low in the east-south-east, on our right
SUN = unit((0.80, 0.55, -0.24))                              # toward the sun: (to the right, up, toward us); about 33 degrees up
LIT = Light(SUN)
SKY_LIGHT = (0.70, -0.70)                                    # toward the sun in the picture (for the clouds)
CAST = (-SUN[0] / SUN[1], -SUN[2] / SUN[1])                  # where a shadow falls on the paving, per cm of height: (across, away)

# ---------------------------------------------------------------- the temple of Jupiter Best and Greatest
TA = 10.0                                                    # its front turns a little to our right (the front runs away to the right)
T = Frame.at(CAM, TA, 205.0, 6480.0)                         # the front-left corner of the podium's top (u = 0, v = 0)
UW = 3200.0                                                  # the front, podium and steps
BACK = 5600.0                                                # how far the podium runs back
HP = 450.0                                                   # the porch floor: 25 steps of 18
RISE, TREAD, NSTEP = 18.0, 36.0, 25
CHEEK = 150.0                                                # the blocks at either end of the steps
RUN = NSTEP * TREAD                                          # the steps come forward of the podium by this much
COL_R = 84.0                                                 # a column's radius at its foot (plain Doric: no flutes)
HC = 1130.0                                                  # a column, base to abacus
GAP = 552.0
COLS = [220.0 + GAP * i for i in range(6)]                   # the six columns of the front, at v = COLV
COLV = 120.0
ROWS_V = [COLV, COLV + 600.0, COLV + 1200.0]                 # three rows of columns: a very deep porch
FLANK_V = [COLV + 600.0 * i for i in range(9)]               # and down each flank
DEEP = 1860.0                                                # the wall with the three doors
CELLA = (640.0, UW - 640.0)                                  # the three rooms span this much of the front
E0 = HP + HC                                                 # the top of the columns
ARCH, FRIEZE, CORN = 150.0, 120.0, 52.0                      # the beam over the columns, the band with the name, the cornice
E1, E2, E3 = E0 + ARCH, E0 + ARCH + FRIEZE, E0 + ARCH + FRIEZE + CORN
EAVE = 46.0                                                  # how far the cornice stands out
PITCH = math.tan(math.radians(13.0))                         # a low, broad Tuscan gable
APEX = E3 + (UW / 2 + EAVE) * PITCH
QUAD_H = 300.0                                               # the bronze chariot on the peak
NAME = "Q LVTATIVS CATVLVS"                                  # the one name across the front (the inscription's own words are not known)

# ---------------------------------------------------------------- what stands in the precinct (world cm: X, Z of the middle of its foot)
ALTAR = dict(X=(600.0, 1160.0), Z=(3300.0, 3540.0), h=150.0)                 # the great altar of Jupiter: long, stone, on a step
CHARIOT = dict(X=1150.0, Z=2750.0, base=(280.0, 430.0, 150.0))              # the dictator's chariot on its base: it faces the doors (we see it from behind)
WORLD = dict(X=330.0, Z=2600.0, base=(110.0, 110.0, 300.0), r=72.0, man=200.0)   # his statue on the bronze ball, the world, on a tall base
KINGS_Z = 1600.0                                             # the front line of the kings' bases
KINGS = [  # x of the middle (picture px, at the bases' front line), base width, depth and height (cm), statue (cm), what
    dict(x=236.0, w=72.0, d=80.0, h=168.0, statue=222.0, kind="old"),
    dict(x=278.0, w=72.0, d=80.0, h=180.0, statue=226.0, kind="brutus"),
    dict(x=336.0, w=140.0, d=140.0, h=120.0, statue=230.0, kind="seat"),     # the middle base: Titus's seat
    dict(x=394.0, w=72.0, d=80.0, h=160.0, statue=228.0, kind="new"),        # the dictator's, set among the kings last year
    dict(x=436.0, w=72.0, d=80.0, h=174.0, statue=224.0, kind="old2"),
]
HUT = dict(X=-730.0, Z=1600.0, r=150.0, wall=110.0, top=250.0)               # Romulus's hut: round, wattle and thatch, low and old
PEN = dict(X=(-470.0, -240.0), Z=(1150.0, 1340.0), h=62.0, gate=(-240.0, 1195.0, 1300.0))  # the geese's pen, its gate on the right side (open)
WALL = dict(Z=1800.0, h=104.0, t=60.0)                                       # the parapet across the left, over the drop
TABLETS = dict(X=405.0, Z=(880.0, 1255.0), n=4)                              # the row of bronze tablets on posts, bottom right, running away from us


def seat_base():
    return KINGS[2]


def base_box(kg):
    """A king's base as world cm: X0, X1, Z0 (front), Z1 (back), height."""
    Xm = X_at(kg["x"], P(0, 0, KINGS_Z)[1])
    return (Xm - kg["w"] / 2, Xm + kg["w"] / 2, KINGS_Z, KINGS_Z + kg["d"], kg["h"])

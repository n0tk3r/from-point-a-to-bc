"""The Forum (rome-forum): the measurements of everything in the picture, in centimetres, shared by the painter
(rome_forum.py), its mock (rome_forum_mock.py) and its checks.

THE CAMERA is the game's own: horizon 235, full 590 (a grown-up, 175 cm, is 160 pixels tall with his feet on row
590). So the lens stands 388 cm above the paving: we look from the rise of the Sacred Way at the Forum's east end,
west up the square to the temple of Saturn, with the Capitol above everything.

Places are given as (x, D): x across, to the right of the camera's middle; D how far from the lens, along the ground
(the row `full` is D 875). A height h is up from the paving. A building at an angle is a rome_steps_kit.Frame: u along
its front (left to right as we see it), v back into it.

THE LIGHT: the sun is low in the east-south-east, behind the camera's left shoulder (SUN, toward it: left, up and
toward us). Everything that faces us is lit; the fronts on the left side of the square (which face north, to our
right) are in shade; the fronts on the right side (which face south, to our left) take the sun at a slant; long
shadows run away from us up the square and to the right.
"""

import math

import numpy as np

from persp import Camera
from rome_steps_kit import Frame, unit

W, H = 800, 600
SHAPE = (H, W)
HZ, FULL = 235, 590
CAM = Camera(HZ, FULL)
EYE, F, VX, VY = CAM.eye, CAM.F, CAM.vx, CAM.vy          # 388.3 cm, 800 px, 400, 235
Z0 = CAM.Z0                                              # 875: the lens's distance from the paving at row `full`

SUN = unit((-0.30, 0.46, -0.84))                        # toward the sun: (to the right, up, away from us): low (27 degrees), behind our left shoulder
CAST = (-SUN[0] / SUN[1], -SUN[2] / SUN[1])             # where a shadow falls on the ground, per cm of height: (across, away)
SKY_LIGHT = (-0.55, -0.83)                              # toward the sun in the picture, for the clouds (up and a little left)


def k(D):
    """Pixels per cm at a distance D from the lens."""
    return F / D


def pt(x, y, D):
    """A place (x across, y up, D from the lens) -> the picture."""
    return (VX + x * F / D, VY + (EYE - y) * F / D)


def row_of(D, h=0.0):
    return VY + (EYE - h) * F / D


def D_of(row, h=0.0):
    """How far from the lens the ground (or the level h) is at a picture row."""
    return (EYE - h) * F / (row - VY)


def x_of(col, row, h=0.0):
    D = D_of(row, h)
    return (col - VX) * D / F, D


def frame(angle, x, D, fine=1):
    """A building's frame whose corner (u = 0, v = 0) stands at (x, D)."""
    return Frame(CAM, angle, VX + x * F / D, D, fine=fine)


def scale_at(row):
    """The size the game draws a person at, with feet on this row (walk.js scaleAt, before its limits)."""
    return (row - HZ) / (FULL - HZ)


# ---------------------------------------------------------------- the temple of Castor (near left)
# Its front faces us, turned a little to our right; we see its right-hand corner, the high podium, the broad flight of
# steps coming down toward us, and two or three of its columns, cut by the top of the picture.
CASTOR = dict(angle=14.0, xR=-620.0, DR=2050.0, width=2300.0, podium=470.0, cols=1120.0, steps=23, rise=470.0 / 23, tread=30.0,
              porch=80.0, gap=282.0)


def castor_frame(fine=1):
    """u = 0 at the left end of the front (far off the picture), u = width at the right-hand corner (v = 0, the line
    of the columns)."""
    c = CASTOR
    a = math.radians(c["angle"])
    x0 = c["xR"] - c["width"] * math.cos(a)
    D0 = c["DR"] - c["width"] * math.sin(a)
    return frame(c["angle"], x0, D0, fine)


def castor_steps_foot():
    """v of the foot of the steps (the riser of the first step), in Castor's frame."""
    c = CASTOR
    return -c["porch"] - c["steps"] * c["tread"]


# ---------------------------------------------------------------- Juturna's spring, and Phyllis's place
BASIN = dict(x0=-820.0, x1=-410.0, D0=1140.0, D1=1272.0, h=58.0, wall=16.0)      # a square stone basin before Castor's steps
PHYLLIS = (-345.0, 1262.0)                                                    # the ground under her hips (x, D)
POLE = (-255.0, 1330.0)                                                       # the pole hung with her finished garlands
BASKETS = [(-398.0, 1190.0, 0.0, 50.0, "violets"), (-372.0, 1336.0, 0.0, 56.0, "laurel"), (-300.0, 1385.0, 20.4, 44.0, "myrtle")]   # x, D, standing on, across, what

# ---------------------------------------------------------------- the Tuscan street and Caesar's basilica (left, beyond Castor)
TUSCAN = dict(D0=3300.0, D1=5200.0, x=-1020.0)            # the street's mouth: between Castor's back and the basilica's near end
JULIA = dict(x=-1020.0, D0=5200.0, D1=6700.0, h1=400.0, h2=760.0, roof=820.0, bay=380.0)    # its front faces the square (to our right)

# ---------------------------------------------------------------- the far end: Saturn, the platform, Concord
SATURN = dict(angle=16.0, x=-1000.0, D=7300.0)            # the corner (u = 0, v = 0) of the temple as rome_steps.py measures it
ROSTRA = dict(x0=-200.0, x1=1160.0, D=6400.0, h=300.0, bulge=140.0)
CONCORD = dict(angle=6.0, x=350.0, D=10500.0, width=1100.0, podium=280.0, cols=700.0)

# ---------------------------------------------------------------- the Capitol
HILL_D = 23000.0                                         # how far off the hill's face is, for its haze
JUPITER = dict(angle=-60.0, x=-8950.0, D=34590.0, length=6200.0, width=5300.0, podium=450.0, cols=1450.0, base=5226.0)
MONETA = dict(angle=10.0, x=5906.0, D=27000.0, width=1700.0, podium=300.0, cols=850.0, base=4809.0)
TABULARIUM = dict(x0=-2250.0, x1=3600.0, D=18000.0, h0=1300.0, h1=2300.0, h2=2750.0)

# ---------------------------------------------------------------- the right side: the senate house's site, the basilica of Paullus
HOARD = dict(a=(760.0, 1350.0), b=(520.0, 2900.0), h=230.0, gate=(0.45, 0.58))   # its foot runs from a (near) to b (far); the gateway between those fractions
CRANE = dict(x=1100.0, D=2600.0)                         # the foot of the treadwheel crane, inside the site
# the new senate house going up inside the site, as much of it as shows over the hoarding: its front wall (facing us)
# risen out of the pit to some two metres and a half, its near end stepped down where the courses stop; a stack of tufa
# blocks waiting at its foot; a little timber scaffold under the crane's load (which goes down onto the wall's top)
SITE_WALL = dict(x0=620.0, x1=1700.0, D=2850.0, thick=120.0, h=240.0)    # (inside the site's far edge, which the walk keeps to)
SITE_STACK = dict(x0=1265.0, x1=1385.0, D=2700.0, d=62.0, courses=3, high=60.0)
SITE_SCAFFOLD = dict(xs=(620.0, 760.0), D=2790.0, h=460.0, ledgers=(250.0, 430.0))
PAULLUS = dict(x=1300.0, D0=3200.0, D1=7400.0, h1=440.0, h2=780.0, roof=840.0, bay=360.0)  # its front faces the square (to our left)

# ---------------------------------------------------------------- the square
PUTEAL = dict(x=-60.0, D=2050.0, r=95.0, h=80.0)
TABLE = dict(x=120.0, D=1930.0, w=170.0, d=78.0, h=82.0, awning=212.0)
STATUES = [(-560.0, 3300.0, 540.0), (700.0, 4300.0, 580.0), (-260.0, 5300.0, 520.0)]      # x, D, the column's height
FRONT_BASE = dict(x=560.0, D=1190.0, w=160.0, d=120.0, h=100.0)                          # a statue's base at the very front, bottom right
SATURN_FOOT_D = None                                     # (set below, from the steps of the temple of Saturn)

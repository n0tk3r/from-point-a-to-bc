"""Across the Tiber (rome-tiber): the place, measured. Read by rome_tiber.py (the painting), rome_tiber_things.py
(what stands about), rome_tiber_hens.py (the hens), rome_tiber_plan.py (the skeleton) and rome_tiber_check.py.

World measurements are centimetres, as in persp.py: x to the right of the camera's axis, y up from the lane, z away
from us (z = 0 is the row `full`, where a grown man is 160 px tall). The camera is the game's own for this scene
(horizon 250, full 590: the master brief's numbers), so its lens is 3.72 m above the lane: we stand where the stone
bridge comes down onto the right bank, and look downstream.

THE PLACE (plan, looking down, the river on the left):

    the river            |  the quay edge, x = Q, straight away to the vanishing point
      the barge  |=====| |  moored off the quay downstream of the landing, its stern by the landing's far edge
                 |=====| |                 the road on south along the river ->  (Caesar's gardens, far off, on its right)
      [landing ]---------+          the house of prayer (front turned toward the bridge), the bench before it
      [ steps  ]   the little square at the bridgehead
                                    Eleazar's house (front turned toward the bridge), the hen yard in front of it
           (we stand here, on the end of the bridge)

The two near houses stand along one front line turned GAMMA degrees from the river, so that they face the bridgehead
and the river at a slant: the sun (low, ahead and to the left, over the far bank) lights their fronts at a slant, and
we see the window and the door well enough for a man to show in the one and come out of the other."""

import math

from persp import Camera

W, H = 800, 600
HZ, FULL = 250, 590                                          # fixed by the master brief
VX = 380.0                                                   # the vanishing point of the river and the road
CAM = Camera(HZ, FULL, vanish_x=VX)
EYE, F, Z0 = CAM.eye, CAM.F, CAM.Z0

# ---- the sun: low, ahead and to the left, over the far bank (east-south-east on the morning of the Ides)
SUN_AZ, SUN_EL = 62.0, 22.0                                  # degrees left of straight ahead; above the horizon
_a, _e = math.radians(SUN_AZ), math.radians(SUN_EL)
SUN = (-math.sin(_a) * math.cos(_e), math.sin(_e), math.cos(_a) * math.cos(_e))     # toward the sun (x, y, z)

# ---- the river and its bank
Q = -400.0                                                   # the quay's edge, all the way along
WATER = -72.0                                                # the river's face, below the lane (a spring river, running high)
FAR_BANK = -8400.0                                           # the far shore (the river is some 80 m wide here)
LANDING = dict(x0=-700.0, x1=Q, z0=290.0, z1=640.0)          # the stone landing that juts into the river
STEPS = dict(x0=-560.0, x1=-430.0, n=5, rise=18.0, tread=30.0)   # steps down into the water from its near edge (toward us)
CURB = 14.0                                                  # the landing's edge stones stand this much proud of it

# ---- the barge (moored off the quay, its stern by the landing; held off by poles, a plank to it from the landing)
BARGE = dict(xs=-585.0, xp=-965.0, z0=700.0, z1=2380.0, deck=-44.0, gunwale=-20.0)

# ---- the near houses: one front line, turned toward the bridgehead
GAMMA = 25.0                                                 # degrees from the river's line
_g = math.radians(GAMMA)
D = (-math.sin(_g), math.cos(_g))                            # along the front, away from us (to the left)
N = (-math.cos(_g), -math.sin(_g))                           # out of the front, toward the square (left and toward us)
FRONT0 = (651.0, 365.0)                                      # where the front's foot leaves the picture at its right edge (x, z): s = 0


def along(s):
    """The foot of the front line, s cm from where it leaves the picture at the right (+ away, toward the road)."""
    return (FRONT0[0] + D[0] * s, FRONT0[1] + D[1] * s)


def out(p, d):
    """A point d cm out from the front, in front of the plan point p."""
    return (p[0] + N[0] * d, p[1] + N[1] * d)


EL = dict(s0=-260.0, s1=600.0, floor2=300.0, eave=610.0, depth=900.0)       # Eleazar's house: s from its near end (out of the picture) to the corner
PR = dict(s0=600.0, s1=1200.0, eave=560.0, depth=1100.0)                    # the house of prayer, from the corner on
WINDOW = dict(s0=245.0, s1=345.0, sill=402.0, top=512.0)     # Eleazar's upper window, open, the shutter folded back
WINDOW2 = dict(s0=470.0, s1=520.0, sill=405.0, top=470.0)    # his small upper window, over the door
DOOR_E = dict(s0=452.0, s1=548.0, h=205.0)                   # Eleazar's door
MEZUZAH = dict(s0=440.0, s1=444.0, h0=134.0, h1=153.0)        # the little case on its right-hand post (the near one, as one goes in): upright
DOOR_P = dict(s0=905.0, s1=1075.0, h=290.0)                  # the broad door of the house of prayer
BENCH = dict(s0=640.0, s1=840.0, out=56.0, deep=38.0, h=45.0)  # the stone bench before the house of prayer: along the front, out from it
YARD = dict(s0=-260.0, s1=405.0, out=235.0, fence=62.0,       # the hen yard before Eleazar's house: from out of the picture to short of his door
            split=180.0)                                      # the stake where the fence's two cut-outs meet (fence, fence-corner)
FIG = dict(s=-90.0, out=140.0)                               # the fig tree in the yard, by the near corner
HENS = [("brown", 85.0, 100.0), ("speckled", 130.0, 88.0), ("white", 180.0, 70.0), ("brown", 232.0, 58.0), ("speckled", 282.0, 48.0)]
                                                              # the hens, in a loose row across the yard from in front of the coop
                                                              # back toward the house: (colouring, s along the front, cm out from it)
HENS_ROW = dict(s0=HENS[0][1], o0=HENS[0][2], s1=HENS[-1][1], o1=HENS[-1][2])     # the row from end to end (marks.hens)
STACK = dict(x0=-694.0, x1=-596.0, z0=436.0, z1=606.0)      # what waits on the landing to go aboard: bales, a bolt of linen, two jars
WASH = dict(s0=350.0, s1=466.0, out=18.0, h=484.0)            # the washing line between his two upper windows, pegged out from the wall
ROAD_X = 144.0                                               # the fronts of the houses along the road, beyond (x)
WELL = dict(x=-120.0, z=1000.0, r=55.0, h=88.0)              # the well in the square


def P(x, y, z):
    return CAM.pt(x, y, z)


def k_at(z):
    """Picture pixels per cm at depth z."""
    return F / (Z0 + z)


def ground_at(x, z):
    return P(x, 0.0, z)


def row_of_ground(z):
    return HZ + EYE * F / (Z0 + z)


def depth_of_row(row):
    """z of the lane under a picture row."""
    return EYE * F / (row - HZ) - Z0


def plan_of(px, py, y=0.0):
    """The place (x, z) on the level y that a picture point looks at."""
    Z = (EYE - y) * F / (py - HZ)
    return ((px - VX) * Z / F, Z - Z0)


def man_scale(z):
    """How big the game must draw a grown man whose feet are at depth z (1 at the row `full`)."""
    return Z0 / (Z0 + z)

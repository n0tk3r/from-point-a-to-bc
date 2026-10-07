"""The plan of the living room: where everything stands, and the lamps that light it.

All measurements are centimetres in the room (x right of the middle, y up from the floor, z away from
us); the camera in home_living_room_kit.py turns them into picture places that agree with the game's
depth numbers (horizon -150, full 585), so the people the game draws fit the furniture.

LIGHT. Night. Nothing comes from the sky: the room is lit by its own lamps, each a warm pool, and
between and above them it falls away into cool blue-violet.
  1. the pendant over the dining table (left foreground): light straight DOWN, a hard bright pool on
     the white cloth, a wide soft one on the floor round it; chairs throw their shadows outward from it.
  2. the reading lamp behind Dad's armchair (right foreground): light down and to the left onto the
     chair, the stair foot and the closet door, and a disc of light up onto the ceiling.
  3. the little lamp on the piano (back wall, right of middle): lights the music, the keys and the
     family photographs on the wall above.
  Cool: the monitor on the desk (a blue-white glow on the desk top, forward), and the window (street
  lamp and night sky), which lights nothing much but its own sill and curtains.
"""

from home_living_room_kit import *

CEIL_Y = 130                                               # the picture row where wall meets ceiling
WALL_H = (WALL_Y - CEIL_Y) / KW                            # so the wall is about 380 cm high: an old house
PICRAIL = 286.0                                            # picture rail
DADO = 92.0                                                # top of the wood panelling

# ---- along the back wall, left to right
DOOR = dict(x0=-575.0, x1=-463.0, top=213.0, lx0=-565.0, lx1=-473.0, ltop=205.0)
WIN = dict(x0=-430.0, x1=-190.0, y0=80.0, y1=250.0, m1=-367.0, m2=-253.0, rail=168.0)
POLE = 263.0                                               # the curtain pole
DESK = dict(x0=-150.0, x1=-6.0, z0=ZW - 70.0, top=76.0)
MON = dict(x0=-112.0, x1=-44.0, y0=86.0, y1=128.0, z=ZW - 42.0)          # the monitor's face
SCR = dict(x0=-108.0, x1=-48.0, y0=90.0, y1=124.0)                         # the lit part of it
BOOKS = dict(x0=8.0, x1=134.0, z0=ZW - 32.0, top=205.0)
PIANO = dict(x0=150.0, x1=300.0, z0=ZW - 60.0, top=125.0, keys=ZW - 88.0)
PHOTO = dict(x0=186.0, x1=262.0, y0=166.0, y1=222.0)
STAIR = dict(x0=308.0, z0=ZW - 92.0, tread=25.0, rise=18.0, steps=11)
CLOSET = dict(x0=487.0, x1=547.0, top=102.0, ajar=20.0)

# ---- out on the floor
TABLE = dict(x0=-352.0, x1=-152.0, z0=42.0, z1=140.0, top=76.0)
ARM = dict(cx=300.0, cz=84.0, ang=-40.0)               # turned to face into the room
RUG = dict(x0=-92.0, x1=232.0, z0=58.0, z1=242.0, ang=-2.4)   # it never lies quite square to the room
MAT = dict(x0=-566.0, x1=-470.0, z0=ZW - 64.0, z1=ZW - 8.0)

# ---- the lamps (where the bulb is)
PENDANT = (-252.0, 198.0, 91.0)
FLOORLAMP = (386.0, 150.0, 96.0)
PIANOLAMP = (282.0, 158.0, ZW - 26.0)
SCREEN = (-78.0, 107.0, ZW - 46.0)
WARM = (1.0, 0.80, 0.50)

LIGHTS = Lights([
    Lamp("pendant", PENDANT, (1.0, 0.80, 0.49), 6.2, down=(34, 66, 1.0), side=0.10, bounce=0.80, reach=300),
    Lamp("floorlamp", FLOORLAMP, (1.0, 0.78, 0.46), 4.0, down=(30, 62, 1.0), up=(18, 40, 0.58), side=0.28, bounce=0.60, reach=250),
    Lamp("pianolamp", PIANOLAMP, (1.0, 0.80, 0.50), 1.0, down=(35, 64, 1.0), up=(22, 46, 0.6), side=0.36, r0=30, bounce=0.34, reach=150),
    Lamp("screen", SCREEN, (0.55, 0.74, 1.0), 1.0, facing=(0, 0, -1, 1.0), r0=30, wrap=0.3),
    Lamp("window", (-310.0, 150.0, ZW - 4.0), (0.40, 0.58, 1.0), 1.5, facing=(0, 0, -1, 0.5), r0=70, wrap=0.45),
], cool=(0.13, 0.155, 0.28), expo=1.35, high=(150.0, 400.0, 0.80))


class Collector:
    """Stands in for a layer while the furniture is gone over once only to learn where its boxes are,
    so that their shadows can be laid on the floor and wall before anything is painted."""

    def __init__(self):
        self.boxes = []


def B(L, x0, x1, y0, y1, z0, z1, color, cast=True, **kw):
    """A box of the furniture: painted, or (first time round) only noted for its shadow."""
    if isinstance(L, Collector):
        if cast:
            L.boxes.append(corners(x0, x1, y0, y1, z0, z1, kw.get("ang", 0.0), kw.get("about")))
        return None
    return box(L, LIGHTS, x0, x1, y0, y1, z0, z1, color, **kw)


def Fc(L, pts, albedo, **kw):
    if isinstance(L, Collector):
        return None
    return face(L, LIGHTS, pts, albedo, **kw)


def lit(albedo, pos, n=(0, 1, 0), dim=1.0):
    """The paint for a small thing of local color `albedo` at a place in the room."""
    return LIGHTS.paint(albedo, pos, n, dim)


def pts2(points):
    return [P(*p) for p in points]


def ceil_pt(X, z):
    """A place on the ceiling -> picture. (The ceiling is the one part of the room drawn as a stage
    painter would: seen from below, though the floor is seen from above.)"""
    z = min(max(z, 0.0), ZW)
    return (VX + X * cam.scale(z), CEIL_Y * (z / ZW) ** (1 / 1.2))

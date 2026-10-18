"""The Office's lot (scene `office-lot`, OFFICE-17A, round seventeen): the camera, the light, where everything is, and
the small tools the painter (office_lot.py), the layout (office_lot_layout.py) and the check (office_lot_check.py) share.

THE CAMERA. One camera for the whole picture, worked out from the scene's own numbers: horizon 140, full 588. A grown-up
is 160 px tall with his feet on row 588, nothing at row 140, so the lens is (588 - 140) x 175 / 160 = 490 cm up: we look
down on the lot from a little rise, over the roof of a building three metres high, and see its roof and the air
conditioner on it. The lens is 760 px (a normal lens), square on to the building's front (yaw 0: every front is parallel
to the picture, every line running back goes to the one point at x 400 on the horizon).

MEASUREMENTS are centimetres, the kit's way (persp.Camera, as the roadside's): x across from the middle of the picture,
y up from the gravel, z away from us, z = 0 the ground on row `full`. For the layout file the same camera is given as
room.View numbers (VIEW), where the room's Z runs toward us: Z = -z.

THE LIGHT. Early afternoon, 31 October: the sun high (about 49 degrees) and a little behind us to the left. Fronts face
it and are lit, tops are brightest, right-hand ends are in shade; everything throws a short shadow back and to the right
(SUN: a point 1 cm up throws its shadow 0.33 cm right and 0.80 cm back). A clear sky with high thin cloud: the shade is
full of blue sky."""

import math

import numpy as np

from brush import F32, blur, grid, lerp, noise, rgb, sample
from persp import Camera

W, H = 800, 600
HZ, FULL, FOCAL, VX = 140, 588, 760.0, 400.0
CAM = Camera(HZ, FULL, vanish_x=VX, focal=FOCAL)
EYE = CAM.eye                                                   # 490 cm
VIEW = dict(horizon=HZ, full=FULL, cam=[0.0, round(CAM.Z0, 2)], yaw=0.0, focal=FOCAL, centre_x=VX)

# ---- the sun: TOWARD is the way to it (x right, y up, z away); SUN is how far a point's shadow falls per cm of height
TOWARD = np.array([-0.252, 0.756, -0.605], dtype=F32)
TOWARD = TOWARD / np.linalg.norm(TOWARD)
SUN = (float(-TOWARD[0] / TOWARD[1]), float(-TOWARD[2] / TOWARD[1]))      # (0.333, 0.800): right, and back


def lambert(n):
    """How squarely the sun strikes a face with outward normal n (0 to 1)."""
    n = np.asarray(n, dtype=F32)
    return float(max(0.0, np.dot(TOWARD, n / np.linalg.norm(n))))


FRONT, TOP, RIGHT, LEFT = lambert((0, 0, -1)), lambert((0, 1, 0)), lambert((1, 0, 0)), lambert((-1, 0, 0))

# ---------------------------------------------------------------- where everything is (cm)
# The building: one storey of beige cinder block, the size of a two-car garage, its front square to us.
BLD = dict(x=(-500.0, 80.0), z=(470.0, 1030.0), deck=300.0, cope=306.0)
DOOR = dict(x=(-250.0, -150.0), h=210.0, jamb=7.0)              # steel, beige, on the front
KEYPAD = dict(x=(-136.0, -123.0), y=(116.0, 135.0))             # beside it, on the right
AWNING = dict(x=(-296.0, -104.0), y=(218.0, 225.0), out=75.0)   # a small flat awning over the door, 75 cm out from the wall
SIGN = dict(x=(-472.0, 52.0), y=(233.0, 295.0), proud=2.5)      # the long sign, on the wall over the awning
WINDOW = dict(x=(-420.0, -356.0), y=(168.0, 208.0))             # the one small high window, frosted
MAT = dict(x=(-246.0, -154.0), z=(402.0, 458.0))                # WIPE
PIPE = dict(x=66.0, z=463.0, r=4.6, top=288.0, elbow=96.0, mouth=(88.0, 437.0), straps=(120.0, 162.0, 204.0, 246.0))
SCUPPER = dict(x=(55.0, 77.0), y=(284.0, 306.0), z=(456.0, 470.0))
# The trash can, steel, lidded, the lid's handle chained to it: where it stands by the wall, where it lies tipped over,
# and where it stands under the drainpipe's elbow (middle of its foot; radius; height of the body and of the lid's top)
CAN = dict(r=26.0, body=70.0, top=77.0, standing=(-22.0, 440.0), tipped=(8.0, 398.0), pipe=(66.0, 440.0))
# The rooftop unit: an air conditioner the size of a minivan on its curb, set back on the roof; its intake grille on the
# side toward us, four wing nuts at the grille's corners, the maintenance switch beside it.
UNIT = dict(x=(-440.0, 40.0), z=(770.0, 1010.0), curb=318.0, top=532.0)
GRILLE = dict(x=(-176.0, -56.0), y=(330.0, 432.0), proud=3.0)
NUTS = [(-168.0, 338.0), (-64.0, 338.0), (-168.0, 424.0), (-64.0, 424.0)]       # 1 and 2 low, 3 and 4 high (x, y)
FAN = dict(x=-116.0, y=381.0, r=42.0)                           # the fan behind the grille: its hub and its reach
SWITCH = dict(box=(-19.0, 13.0, 322.0, 360.0), proud=10.0, pivot=(-19.0, 339.0), up=(-25.4, 353.8), down=(-27.6, 324.2))
DUCTS = [dict(x=(-492.0, -440.0), y=(300.0, 392.0), z=(796.0, 846.0)), dict(x=(-492.0, -440.0), y=(300.0, 364.0), z=(880.0, 936.0))]
# The flagpole, by the building's front left corner (its shadow climbs the wall just left of the sign)
FLAG = dict(x=-500.0, z=420.0, h=650.0, r=4.6, pennant=92.0)
# The chain-link fence across the back, and its gate at the left, standing open, the sign on the open leaf
FENCE = dict(z=1250.0, h=185.0, posts=300.0, x=(-1500.0, 1600.0))
GATE = dict(x=(-1150.0, -930.0), swing=65.0)                    # the leaf is hung on the right post and swung in toward us
# The limousine, parked beside the building, nose to the right (its near side on z 640; the tail at x 205)
LIMO = dict(tail=205.0, z=640.0, door=(369.0, 438.0), swing=50.0)

# ---------------------------------------------------------------- the camera's small sums
def P(x, y, z):
    """Lot place -> picture place."""
    return CAM.pt(x, y, z)


def k_at(z):
    """Picture pixels per cm at depth z."""
    return CAM.scale(z)


def scale_at(z):
    """How big a person is drawn at depth z (1 on row `full`)."""
    return CAM.scale(z) / CAM.s0


def row_of(z, y=0.0):
    return CAM.pt(0.0, y, z)[1]


def ground_at(px, py):
    """A point of the gravel in the picture -> (x, z)."""
    z = CAM.depth_at(py)
    return CAM.x_at(px, py), z


def plane_full(y):
    """The row on which a grown-up standing on a level floor y cm up would be full size (160 px): for the roof, whose
    people are sized by their own floor. horizon stays 140."""
    return HZ + (FULL - HZ) * (EYE - y) / EYE


def on_plane(px, py, y):
    """A point of the picture -> the place on the level plane y cm up that it shows: (x, z)."""
    t = (EYE - y) * FOCAL / max(py - HZ, 1e-3)                 # = Z0 + z
    return (px - VX) * t / FOCAL, t - CAM.Z0


def wall_xy(shape, z):
    """For every pixel: the place (x, y) on the upright plane at depth z that it shows."""
    x, y = grid(shape)
    k = CAM.scale(z)
    return ((x - VX) / k).astype(F32), (EYE - (y - HZ) / k).astype(F32)


def floor_xz(shape, y=0.0):
    """For every pixel below the horizon: the place (x, z) on the level plane y cm up that it shows, and a mask."""
    px, py = grid(shape)
    below = py > HZ + 0.5
    t = (EYE - y) * FOCAL / np.maximum(py - HZ, 0.5)
    return ((px - VX) * t / FOCAL).astype(F32), (t - CAM.Z0).astype(F32), below.astype(F32)


# ---------------------------------------------------------------- colour
def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


def lit(base, f, warm="#fff1d6", cool="#5d6aa8", amb=0.42):
    """A surface of colour `base` struck by the sun at f (0 to 1): the shade is the base under the blue sky (cool), the
    light is the base in warm sun."""
    b = col(base)
    shade = b * col(cool) * 1.35 * amb + b * 0.18
    sunny = b * col(warm) * (0.62 + 0.62 * f)
    return np.clip(lerp(shade, sunny, min(1.0, f * 1.35)), 0, 1)


def ground_noise(shape, cell_cm, seed, y=0.0, calm=2.5, octaves=4):
    """Noise lying on a level plane (y cm up), 0 to 1: blotches cell_cm across wherever they are, fine and calm far off."""
    X, Z, below = floor_xz(shape, y)
    tile = noise((1024, 1024), 48.0, seed, octaves)
    scale = cell_cm / 48.0

    def fold(t):                                                # mirrored wrap: no seams
        t = np.mod(t / scale + 1024 * 7.3, 2.0 * 1022)
        return np.where(t > 1022, 2.0 * 1022 - t, t)
    t = sample(tile, fold(X), fold(Z * 0.93 + 211.0))
    k = CAM.F / (CAM.Z0 + np.maximum(Z, -CAM.Z0 + 50))
    size_px = cell_cm * k * k * (EYE - y) / CAM.F
    fade = np.clip(size_px / calm, 0, 1)
    return (lerp(np.full(shape, 0.5, dtype=F32), t, fade) * below + 0.5 * (1 - below)).astype(F32)

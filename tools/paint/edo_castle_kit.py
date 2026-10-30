"""The castle approach at Himeji (edo-castle), about 29 April 1830, late afternoon: the measurements, the camera, the
light and the colours its scripts share (PAINT-20D, round twenty).

PLAN
  Light     The sun low in the west, to our right and a little behind us (SUN, about 17 degrees up): everything facing
            right or facing us is warm (lead white and naples yellow, turning toward chrome orange in the last light);
            left-facing planes and the undersides of the roofs are lilac and cobalt violet; shadows on the ground run
            far to the LEFT and a little away, three times as long as a thing is tall. The gate faces us (its west
            face), so its gable and the cross tile on it are in the light.
  Depth     horizon 290, full 588 (the land camera: the lens 3.26 m above the road, looking level). The road runs
            across the bottom; the stone ramp climbs from it to the terrace before the gate (rows 470 to 436); the
            moat lies left of the terrace under the white wall; the keep stands on its hill far behind, high.
  Tones     LIGHT  the keep's white walls, the gate's white, the sky low down, the blossom's lit side.
            DARK   the keep's roofs and the gate's roof (prussian blue-grey), the pines, the trunk, the water's shade.
            MIDDLE the sky's blue, the stone, the bank, the road, the hills.
            The eye comes in along the road, climbs the ramp to the gate, and goes up the white wall to the keep.
  Places    the keep: x 265 to 455, the ridge at row 36, the stone base's foot at row 330 (behind the wall).
            the gate: x 575 to 775, its threshold at row 436, the ridge of its tower at row 160; the gable's apex and
            its tile at about (675, 170).  the wall: from the gate to the left edge, top row 352, foot row 398.
            the moat: x 0 to 432, rows 440 to 482.  the ramp: foot at the road (x 430 to 580, row 540), top at the
            terrace (row 470).  the terrace: x 445 to 790, rows 436 to 470.  the cherry: its foot at (88, 540), its
            crown x 0 to 290, rows 60 to 300, its low boughs to row 440.  the scaffold: x 455 to 565 against the wall.
            the ladder: against the gate's outer wall, foot (598, 462).

Everything is in picture pixels (the woodblock manner draws flat masses), and the ground plane is the game's camera
(persp.Camera) so that the things people stand beside come out the right size for them."""

import math

import numpy as np

from brush import F32, rgb
from persp import Camera
from rome_steps_kit import Light, unit

W, H = 800, 600
SHAPE = (H, W)
HZ, FULL = 290, 588
CAM = Camera(HZ, FULL)
EYE, FOC = CAM.eye, CAM.F                                    # 326 cm, 800 px
OUT = "out/edo-castle"


def Z_row(y):
    """How far off the ground is at a picture row (cm from the lens)."""
    return EYE * FOC / max(y - HZ, 0.5)


def k_at(y):
    """Picture pixels per cm for something standing on the ground at row y."""
    return FOC / Z_row(y)


def scale_at(y):
    """The game's size for a person with feet on row y (1 at full)."""
    return (y - HZ) / (FULL - HZ)


def P(X, Y, Z):
    """A place in the world (cm across from the middle, up from the ground, from the lens) -> the picture."""
    k = FOC / Z
    return (CAM.vx + X * k, CAM.vy + (EYE - Y) * k)


# ---------------------------------------------------------------- light: the sun low in the west, on our right and a little behind us
SUN = unit((0.90, 0.30, -0.30))                              # toward the sun: (right, up, depth: negative is toward us)
LIT = Light(SUN, sun=(1.10, 0.98, 0.78), shade=(0.52, 0.58, 0.88), bounce=(0.26, 0.16, 0.04))
CAST = (-SUN[0] / SUN[1], -SUN[2] / SUN[1])                  # a shadow on the ground per cm of height: (across, away): (-3.0, 1.0)
SKY_LIGHT = (0.85, -0.45)                                    # toward the sun in the picture (for the clouds)

# ---------------------------------------------------------------- the colours (the box's, as the key will pull them)
C = dict(
    sky_top="#2a5cb4", sky_mid="#5f98d2", sky_low="#9fcbe3", sky_pale="#dfe6e0", sky_warm="#f4dfb8", sun_glow="#f7cf96",
    cloud="#f4ecde", cloud_shade="#c5bfe0",
    hills_far="#a9b6d8", hills_mid="#8fa0c6",
    pine_dark="#1f3a3a", pine="#2e5a4a", pine_lit="#4f8060", pine_far="#5c7a86",
    white_lit="#f5ebd2", white_warm="#f2dfb2", white_shade="#b9c2dc", white_deep="#98a6cc",
    roof="#2e3c56", roof_lit="#5c6a86", roof_edge="#8c96ae", roof_deep="#1c2640",
    stone="#b89a6e", stone_lit="#d8bb86", stone_shade="#857e94", stone_joint="#5e5a60",
    water="#3f74a8", water_deep="#2d5586", water_light="#86b4d0", water_glint="#e8f2ee",
    bank="#9eaa62", bank_lit="#c7c478", bank_shade="#6f8460", path="#d8c496",
    road="#cdb384", road_lit="#e3cc9c", road_shade="#9a8e94", road_dark="#86726a",
    trunk="#3c2a2c", trunk_lit="#6a4c3e", trunk_rim="#8a6a4e",
    bloom_lit="#f3cdd3", bloom="#e9adbd", bloom_mid="#dc8aa5", bloom_shade="#c47498", bloom_deep="#a06a92",
    bamboo="#c9a85a", bamboo_lit="#e6cc7e", bamboo_dark="#8a6e34", rope="#6a5236",
    wood="#6a4a34", wood_lit="#9a7452", wood_dark="#3e2c24",
    lime="#f6f1e4", lime_shade="#d4d6e0", cast="#6c7ab2",
    line="#1a2846",                                          # prussian blue: the keyblock's contour
)


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


def mix(a, b, t):
    return col(a) + (col(b) - col(a)) * t


def far(color, t):
    """A colour through the evening air: paler and bluer by t (0 near, 1 the far hills)."""
    return mix(color, "#c9d3e4", 0.75 * t)

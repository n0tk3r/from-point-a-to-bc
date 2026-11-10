"""PAINT-23 (round twenty-three, DEPTH.md): what the top of the Satta Pass's scripts share (edo_satta.py, _far, _near,
_layout): its one camera, where things are, and the act's watercolour tools in this camera's rows.

The camera and the placings are round twenty-one's (PAINT-21A) and have not moved: persp.Camera(288, 590), the eye
330 cm over the road, Z0 875, focal 800; the road z 70 to 430 cm, its bank z 430 to 520, the Jizo, O-Shige's stone, the
bent pine, Fuji. World measurements are centimetres: x to the right of the picture's middle, y up from the road, z away
from us (z = 0 is the road at the row FULL). The bay lies 90 m under the road (DROP).

The watercolour is Yui's (edo_village_kit: Wet, thin, glaze, hand, grade_cut, painted, world_noise; imported, never
changed). Two of its tools read Yui's own rows (horizon 300): keyline() and squash() here are the same in ours.
"""

import math

import numpy as np

from brush import F32, grid, lerp, mask_poly, noise, rgb
from edo_kurasawa_kit import View, Fuji, SUN, SUN3
import edo_village_kit as YK
from edo_village_kit import (P, mixp, tintw, thin, Wet, glaze, hand, grade_cut, painted, under_of, world_noise, WPAPER, SHADE,
                             SHADE_WARM, SHADE_PINES, WHITE, NAPLES, CERULEAN, COBALT, ULTRA, PRUSSIAN, OCHRE, SIENNA, VERONESE,
                             VIRIDIAN, LAKE, VERMILION)
from edo_village_far import HORIZON_C

W, H = 800, 600
SHAPE = (H, W)
HZ, FULL = 288, 590
V = View(HZ, FULL)                                                   # the act's sun, as at Yui (1.6 : 0.5)
CAM = V.cam
gp, kz = V.gp, V.kz
DROP = 9000.0                                                        # the bay lies this far (cm) below the road

# ---------------------------------------------------------------- where things are (round twenty-one's numbers)
ROAD = dict(z0=70.0, z1=430.0)                                       # the road across the picture (rows 567 to 491)
BANK = dict(z0=430.0, z1=520.0, h=34.0)                              # the bank at the road's far edge: earth and grass, never a fall
JIZO = dict(x=-25.0, z=446.0, h=129.0)                               # the Jizo before the bank: exactly Little Sister's height at `jizo`
JIZO_MARK = (-110.0, 372.0)                                          # before it and a little to its left (row 500: Little Sister 78 px)
SEAT = dict(x=-400.0, z=420.0, w=92.0, d=56.0, h=44.0)              # O-Shige's stone at the road's far edge
PINE = dict(x=520.0, z=540.0)                                        # the bent pine on the bank's top, right (its foot at x 694)
FUJI = Fuji(summit=(330.0, 40.0), foot=292.0, half=530.0, snow=0.40, seed=21)
COAST = [(-10, 452), (24, 444), (60, 437), (104, 432), (150, 430), (196, 433), (236, 440), (268, 449), (294, 460), (316, 474)]   # the near flank's waterline
CLIFF_FOOT = [(-10, 368), (30, 365), (70, 361), (110, 357), (150, 352), (186, 348), (214, 346)]     # the far stretch's cliffs: their foot
CLIFF_TOP = [(-10, 340), (30, 341), (70, 337), (110, 335), (150, 333), (186, 336), (214, 346)]      # and their lip
RIDGE = [(-10, 236), (30, 246), (70, 260), (110, 276), (146, 294), (176, 314), (198, 332), (214, 346)]   # the far stretch's skyline
FAR = [(-10, 300), (60, 306), (120, 311), (170, 316)]                # the coast of Kurasawa and Yui, beyond the flank's tip

# ---------------------------------------------------------------- round twenty-three: the near plane's ground
BLOCK = [[660, 600], [672, 587], [700, 575], [730, 563], [760, 553], [784, 547], [800, 544], [800, 600]]   # the road under the near rock (scene file `blocked`)


def bank_top(x):
    """The row of the bank's grassy top (the edge beyond which the ground falls away), at picture column x: a gentle wave
    of turf, a low place before `view` where one stands to look out; at the left the road and its bank drop toward the
    climb, at the right edge they start down to Okitsu."""
    base = gp(0, BANK["z1"], BANK["h"])[1]
    wav = 2.4 * math.sin(x / 41.0 + 0.7) + 1.4 * math.sin(x / 17.0 + 2.1) + 0.8 * math.sin(x / 7.3)
    dip = 7.0 * math.exp(-((x - 262) / 30.0) ** 2)
    v = base + wav + dip
    if x < 150:
        v += (150 - x) ** 1.6 * 0.020
    if x > 690:
        v += (x - 690) ** 1.5 * 0.022
    return v


def road_far(x):
    """The row of the road's far edge (where the bank begins) at column x."""
    base = gp(0, ROAD["z1"])[1]
    if x < 150:
        return base + (150 - x) ** 1.6 * 0.024
    if x > 690:
        return base + (x - 690) ** 1.5 * 0.020
    return base


TOPS = np.array([bank_top(c) for c in range(W)], dtype=F32)        # (per column, for masks)
FARS = np.array([road_far(c) for c in range(W)], dtype=F32)


def floor():
    """For every pixel below the horizon: the place on the road's level it shows (x, z cm) and a mask."""
    return CAM.floor_grid(SHAPE)


def sea():
    """For every pixel below the horizon: the place on the bay it shows, 90 m under the road (x, z cm, from the same
    lens), and its distance (cm)."""
    px, py = grid(SHAPE)
    eye = CAM.eye + DROP
    Zs = eye * CAM.F / np.maximum(py - HZ, 0.35)
    X = (px - CAM.vx) * Zs / CAM.F
    return X.astype(F32), (Zs - CAM.Z0).astype(F32), Zs.astype(F32)


def sea_row(dist):
    """The picture row of the bay at a distance (cm from the lens)."""
    return HZ + (CAM.eye + DROP) * CAM.F / dist


def sea_pt(X, dist, y=0.0):
    """A place on the bay (x cm across, `dist` cm from the lens, y cm above the water) -> picture point."""
    k = CAM.F / dist
    return (CAM.vx + X * k, HZ + (CAM.eye + DROP - y) * k)


def squash(row):
    """How flat a circle lying on the road looks at a picture row (its height over its width)."""
    return max(float(row) - HZ, 1.0) / CAM.F


def yui_row(row):
    """A row of ours as the same place in Yui's rows (horizon 300, full 590), for her kit's tools that read rows."""
    return YK.HZ + (row - HZ) * (YK.FULL - YK.HZ) / float(FULL - HZ)


def keyline(layer, pts, row=None, lit=False, seed=0, weight=1.0, color=None, alpha=None):
    """Yui's quiet key line (edo_village_kit.keyline), its weight read at our rows."""
    r = row if row is not None else max(p[1] for p in pts)
    return YK.keyline(layer, pts, yui_row(r), lit=lit, seed=seed, weight=weight, color=color, alpha=alpha)


def air(c, t):
    """A colour with `t` of the air between (0 to 1): toward the sky's colour at the horizon, never grey."""
    return lerp(np.asarray(c, dtype=F32), HORIZON_C, float(np.clip(t, 0, 1)))


def poly_rows(pts_fn, xs):
    return [(float(x_), float(pts_fn(x_))) for x_ in xs]

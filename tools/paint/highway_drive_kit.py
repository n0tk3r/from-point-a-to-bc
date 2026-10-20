"""The numbers every picture of the drive shares (highway_drive.py, ROAD-18P), and a few tools.

THE CAMERA (ROAD-18, fixed for the engine and the painter): highway.py's own: level, the horizon on row 330, the vanishing
point (400, 330) in the middle of the sun, the focal length 800 px, the eye 2.70 m above the road. A point X m right of
the middle of the road (negative: left), z m ahead and Y m up is on the stage at x = 400 + 800 X / z, y = 330 + 800
(2.70 - Y) / z; the camera going forward s m makes every z s smaller.

THE GROUND, from straight above, in three strips across the road (the contract's `grounds`). Each strip's columns run
along the road, forward to the right, and repeat end to end every LOOP metres; its rows run across, from its `from`
(its top row) to its `to` (its bottom row): a pixel's row is (X - from) * ppm, its column ((z + s) * ppm) mod width.

    drive-road.png       from -6 to +6 m, 48 px a metre: 576 rows, 3072 columns
    drive-desert-l.png   from -30 to -6 m (its BOTTOM row is next to the road), 24 px a metre: 576 rows, 1536 columns
    drive-desert-r.png   from +6 to +30 m (its TOP row is next to the road), 24 px a metre: 576 rows, 1536 columns

LOOP is 64 m, not the brief's "about 60": the painting's yellow line is a dash of 3.05 m every 9.14 m, and 64 m is seven
of them (9.1429 m), so the dashes keep their rhythm across the seam and still fall within 4 cm of the painting's own all
the way to the horizon. 64 m is also a whole number of pixels at both 48 and 24 px a metre.

THE STOP. Column c of every strip is the ground at s + z = c / ppm (mod 64). The painting's road (its cracks, patches,
brake marks, the worn white lines, the dashes, the hubcap, the bottle and the strip of tire) is laid in it as the
painting has it from 8 to 72 m ahead of its lens, where the camera stands when s = 0 (mod 64): so the camera must stop
at s = 64 n for the road under the stopped picture to be the painting's (STOP_S).

THE COLOURS. A strip carries the ground's own colours as they are close by; the engine lays the haze over it with distance.
The painting (highway.under()) paints its ground by distance, each part with a ramp from near to the horizon; with its
light left out (the shine, the glows, the long shadows, the deep corners: those are light, and fixed on the screen),
the ramps are matched best (highway_drive_check.py fits them again and says how well) by the engine's haze
1 - 2^(-d / HAZE_FAR) toward HAZE, over these colours close by (BASE, as the painting grades them)."""

import math

import numpy as np

from brush import F32, lerp, rgb

HZ, VX, FOCAL, EYE = 330.0, 400.0, 800.0, 2.70
W, H = 800, 600
LOOP = 64.0
STOP_S = 0.0                                       # the camera stops at s = STOP_S (mod LOOP)
STRIPS = {                                         # name: (from, to, ppm)
    "road": (-6.0, 6.0, 48.0),
    "desert-l": (-30.0, -6.0, 24.0),
    "desert-r": (6.0, 30.0, 24.0),
    "far-l": (-150.0, -30.0, 8.0),                 # PAINT-18B: the desert on from 30 m out to 150 m, 8 px a metre
    "far-r": (30.0, 150.0, 8.0),
}
DASH = 3.05                                        # the painting's dash, and its period made seven to a loop
DASH_EVERY = LOOP / 7.0                            # 9.142857 m (the painting's: 9.14)
HAZE, HAZE_FAR = "#ffba8c", 120.0                  # (graded, before the scene's key: the engine keys it)
BASE = {"road": "#74679b", "shoulder": "#a57375", "plain": "#62325a"}       # graded


def strip_shape(name):
    lo, hi, ppm = STRIPS[name]
    return int(round((hi - lo) * ppm)), int(round(LOOP * ppm))


def strip_X(name):
    """The X (metres) of each row's middle."""
    lo, hi, ppm = STRIPS[name]
    h, _ = strip_shape(name)
    return (lo + (np.arange(h, dtype=F32) + 0.5) / ppm).astype(F32)


def strip_w(name):
    """Where along the road (metres, 0 to LOOP) each column's middle is."""
    lo, hi, ppm = STRIPS[name]
    _, w = strip_shape(name)
    return ((np.arange(w, dtype=F32) + 0.5) / ppm).astype(F32)


def ungrade(color, contrast=1.10, chroma=1.12, pivot=0.40):
    """The colour that highway_kit.grade() turns into `color` (grade is affine: lightness about a pivot, chroma about
    lightness)."""
    q = (np.asarray(rgb(color) if isinstance(color, str) else color, F32) - pivot) / contrast + pivot
    lum = float(q @ np.array([0.3, 0.55, 0.15], F32))
    return np.clip(lum + (q - lum) / chroma, 0, 1).astype(F32)


def hexof(c):
    c = np.clip(np.asarray(c, F32), 0, 1)
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c)

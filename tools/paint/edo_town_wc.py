"""Himeji town (edo-town) in watercolour (round twenty-three, tools/paint/DEPTH.md, "Japan in watercolour"): this scene's own
tools for laying its print-style drawing (edo_town.py, edo_town_kit.py) as washes on paper. edo_town_kit.py is shared with
Shosha and the lock and is not changed: everything new for the town is here, or in edo_town_near.py and edo_town_far.py.

  WSheet      a sheet with the same calls as brush.Sheet (poly, line, ellipse, taper, clear, done, onto), on which every
              flat is laid as a GRADED wash (a little lighter at its top, deeper toward its foot, never even): Yui's Wet
              (edo_village_kit) underneath, which also glazes a half-strength stroke over what is under it
  keyline     the key line, quieter: 0.35 to 0.8 px, broken into strokes of the pen, lost on the edges that face the
              light (the top and the left of a form: the sun is high behind us, a little to the left), and none at all in
              the far layers
  floor       the street's place under every pixel (X across, D away, in cm, through the town's camera), and noise that
              lies on the street in centimetres (so blotches shrink with distance)
  the light   the noon sun (SUN: 0.10 across and 0.36 away per cm of height, about 68 degrees up, behind us and a little
              left); SHADE, the cool glaze of a cast shadow; WALL_SHADE, the same under an eave with the street's warm
              light thrown up into it (warmer toward the foot of the wall)

The paper is watercolor.PAPER; a paint `thin`ned shows that much of the paper through it (a transparent wash)."""

import math

import numpy as np
from PIL import Image as _Image, ImageDraw as _ImageDraw

import watercolor as WC
from brush import F32, rgb, lerp, blur, grid, noise, sample, step, warp, over, tint
from edo_village_kit import Wet
from edo_town_kit import P, HZ, FULL, FOC, VX, EYE, W, H, SHAPE, PAINT, PAPER, LINE, mix, col

WPAPER = WC.PAPER                                         # the bare sheet: the lightest light (plaster in sun, the lit street)
SUN = (0.10, 0.36)                                        # a shadow on the ground per cm of height: across (right), away (north)
LIGHT = (-0.55, -0.83)                                    # where the light comes from, on the picture (x right, y down): high, a little left


def thin(c, t):
    """A paint thinned with water: `t` of the paper shows through it."""
    return lerp(col(c), WPAPER, t).astype(F32)


def deepen(c, t, cool=0.35):
    """A wash laid again over itself: deeper, and a little cooler (toward prussian)."""
    c = col(c)
    return np.clip(lerp(c * (1 - t), col(PAINT["prussian"]), t * cool), 0, 1).astype(F32)


# a cast shadow at noon: a thin cool wash, multiplied over the local colour (never a flat of another colour)
SHADE = lerp(rgb("#ffffff"), lerp(col(PAINT["cobalt"]), col(PAINT["ultra"]), 0.30), 0.50).astype(F32)
SHADE_DEEP = lerp(rgb("#ffffff"), lerp(col(PAINT["cobalt"]), col(PAINT["ultra"]), 0.38), 0.62).astype(F32)
BOUNCE = lerp(rgb("#ffffff"), lerp(col(PAINT["ochre"]), col(PAINT["naples"]), 0.5), 0.40).astype(F32)   # the street's light thrown up


# ---------------------------------------------------------------- graded washes on a sheet with brush.Sheet's calls
class WSheet(Wet):
    """brush.Sheet's calls (poly(points, color, alpha), ellipse(cx, cy, rx, ry, color, alpha), line, taper(points, color,
    w0, w1, alpha)), every flat laid as a graded wash: `top` lighter toward the paper at its top, `foot` deeper at its foot
    (a wash pools as it dries, and walls darken toward the ground). Set `grade` = (0, 0) for flats that must stay even."""

    def __init__(self, shape=SHAPE, ss=3, grade=(0.05, 0.085)):
        super().__init__(shape, ss)
        self.grade = grade

    def _pair(self, color):
        c = col(color)
        top, foot = self.grade
        return thin(c, top), deepen(c, foot, 0.25)

    def poly(self, points, color, alpha=1.0, c1=None, g=None):
        if c1 is not None:
            return Wet.poly(self, points, col(color), col(c1), g, alpha)
        c0, c1_ = self._pair(color)
        return Wet.poly(self, points, c0, c1_, g, alpha)

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0, c1=None, g=None):
        if c1 is not None:
            return Wet.ellipse(self, cx, cy, rx, ry, col(color), col(c1), g, alpha)
        c0, c1_ = self._pair(color)
        return Wet.ellipse(self, cx, cy, rx, ry, c0, c1_, g, alpha)

    def line(self, points, color, width=1.0, alpha=1.0, round_ends=True):
        return Wet.line(self, [(float(x), float(y)) for x, y in points], col(color), width, alpha)

    def taper(self, points, color, w0, w1, alpha=1.0):
        return Wet.taper(self, [(float(x), float(y)) for x, y in points], col(color), w0, w1, None, None, alpha)

    def flat(self, points, color, alpha=1.0):
        """An even wash (no grade): for a thing that must not be graded (a glaze already graded by its light)."""
        return Wet.poly(self, points, col(color), None, None, alpha)


def wsheet_layer(draw, amount=0.6, shape=SHAPE, grade=(0.05, 0.085), seed_push=0):
    """Draw with a WSheet onto a clear Canvas, the edges pushed a little by hand (as edo_town_kit.sheet_layer). -> Canvas"""
    from rome_steps_kit import Canvas
    from edo_town_kit import hand
    s = WSheet(shape, 3, grade)
    draw(s)
    c, a = s.done()
    out = Canvas(shape)
    if amount:
        both = hand(np.dstack([c * a[..., None], a]), amount)
        out.c, out.a = both[..., :3].astype(F32), np.clip(both[..., 3], 0, 1).astype(F32)
    else:
        out.c, out.a = (c * a[..., None]).astype(F32), a
    return out


# ---------------------------------------------------------------- the key line, quieter
def _resample(pts, stepsize=3.0):
    out = [tuple(map(float, pts[0]))]
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(d / stepsize))
        for i in range(1, n + 1):
            out.append((x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n))
    return out


def keyline(s, pts, width=1.0, alpha=0.6, close=True, color=None, light=LIGHT, weight=0.62, seed=0):
    """The key line as a watercolour keeps it: thinner than the print's (0.35 to 0.8 px), a little broken, and lost on the
    side of a form that faces the light (a segment whose outward side looks toward LIGHT is not drawn). `width`, `alpha`:
    the print's, scaled down. Points are picture points; a closed outline's outward side is found from its winding."""
    pts = [(float(x), float(y)) for x, y in pts]
    if len(pts) < 2:
        return s
    col_ = col(LINE if color is None else color)
    w = float(np.clip(width * weight, 0.35, 0.8))
    a = float(np.clip(alpha * 0.72, 0.18, 0.52))
    ring = pts + ([pts[0]] if close else [])
    area = sum(ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1] for i in range(len(ring) - 1)) if close else 0.0
    sgn = 1.0 if area > 0 else -1.0                        # (picture y runs down: positive area is clockwise on the screen)
    lx, ly = light
    ln = math.hypot(lx, ly)
    rng = np.random.default_rng((int(seed) * 7919 + int(pts[0][0] * 13) + int(pts[0][1] * 31)) & 0x7FFFFFFF)
    for (x0, y0), (x1, y1) in zip(ring[:-1], ring[1:]):
        dx, dy = x1 - x0, y1 - y0
        d = math.hypot(dx, dy)
        if d < 0.5:
            continue
        if close:
            nx, ny = sgn * dy / d, -sgn * dx / d             # outward
            if (nx * lx + ny * ly) / ln > 0.42:              # it faces the light: the edge is lost in it
                continue
        q = _resample([(x0, y0), (x1, y1)], 3.0)
        i = 0
        while i < len(q) - 1:
            n = int(rng.uniform(4, 13))                      # a stroke of the pen, 12 to 40 px
            s.line(q[i:i + n + 1], col_, w * rng.uniform(0.8, 1.15), a * rng.uniform(0.55, 1.0))
            i += n + (int(rng.uniform(1, 3)) if rng.random() < 0.5 else 0)
    return s


# ---------------------------------------------------------------- the street under every pixel
def floor():
    """-> X (cm across), D (cm away) of the street under every pixel, and a mask of the rows below the horizon."""
    x, y = grid(SHAPE)
    below = (y > HZ + 0.5).astype(F32)
    D = EYE * FOC / np.maximum(y - HZ, 0.5)
    X = (x - VX) * D / FOC
    return X.astype(F32), D.astype(F32), below


_TILES = {}


def street_noise(X, D, cell, seed, octaves=3):
    """Noise lying on the street, measured in cm: `cell` (across, away) is the size of its blotches. It fades to 0.5 where
    a blotch would be smaller than a pixel (far off it would only glitter)."""
    size = 1024
    tile = _TILES.get((seed, octaves))
    if tile is None:
        tile = _TILES[(seed, octaves)] = noise((size, size), 64, seed, octaves)
    cu, cv = (cell, cell) if np.isscalar(cell) else cell

    def fold(t):
        m = np.mod(t, 2 * (size - 2))
        return np.where(m > size - 2, 2 * (size - 2) - m, m)
    n = sample(tile, fold(X / cu * 64 + 300), fold(D / cv * 64 + 300))
    k = FOC / np.maximum(D, 1.0)
    small = np.minimum(cu * k, cv * k * k * EYE / FOC)
    fade = np.clip((small - 1.0) / 2.5, 0, 1)
    return (0.5 + (n - 0.5) * fade).astype(F32)


def ground_pt(X, D):
    """A place on the street -> the picture."""
    return P(X, 0.0, D)


def px_per_cm(X, D):
    return FOC / D

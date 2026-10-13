"""Tools for painting the Forum (rome_forum.py): the world as a frame of its own, sun and shade, air, the surfaces
the place is built of, and a few ways of laying a painted box or wall on a canvas.

Everything is measured as in rome_forum_model.py: x across (cm, right of the camera's middle), D away from the lens
(cm), h up from the paving. WORLD is a rome_steps_kit.Frame whose u is x and whose v is D, so the steps' tools
(face, on_front, on_side, on_floor, lathe, sunless) work on the world directly; a building at an angle has its own
Frame (model.frame)."""

import math

import numpy as np

from brush import (F32, Sheet, blur, grid, lerp, mask_ellipse, mask_line, mask_poly, noise, over, ramp, rgb, sample, smooth, step,
                   tint, glow, vary, warp, curve)
from rome_steps_kit import Canvas, Frame, Light, col, courses, hash2, holes, lathe, mix, stone, sunless, tex, unit
from rome_street_kit import Sheet2
from rome_forum_model import *

WORLD = Frame(CAM, 0.0, VX, 0.0)                         # u = x, v = D
LIT = Light(SUN, sun=(1.10, 1.0, 0.80), shade=(0.50, 0.55, 0.88), bounce=(0.26, 0.15, 0.03))
WSU, WSV, WSH = WORLD.to_frame(SUN)                      # the sun along x, along D, and up

PX, PY = grid(SHAPE)

# ---------------------------------------------------------------- colours (before light)
PAVE = "#e4d8c0"                                         # the square's travertine
TRAV, TUFA, STUCCO, MARBLE = "#efe6d2", "#c9b38e", "#f1e4c6", "#f4efe4"
RED, DADO = "#a8553c", "#8f4338"
BRONZE, PATINA, GILT = "#a67c3a", "#4f7d6c", "#f2c14e"
WOOD, WOOD_D, WOOD_L = "#9a6c44", "#5e3e28", "#c99a62"
TILE = "#c9724a"
P_RED, P_BLACK, P_CREAM, P_BLUE, P_OCHRE = "#a8382b", "#2f2a33", "#f0e2c0", "#3d6f96", "#d9a441"


def far(color, D, most=0.80, reach=40000.0):
    """A colour as it looks through the morning air at a distance D (cm): paler, bluer, softer. (Warm sunlit colours keep
    their warmth longer, as in the other Rome pictures.)"""
    c = col(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
    t = np.clip(1 - np.exp(-np.maximum(np.asarray(D, dtype=F32) - 1500.0, 0) / reach), 0, most)
    if c.ndim == 1:
        warm = float(np.clip((c[0] - c[2]) * 4, 0, 1))
        to = lerp(col("#c9dcee"), col("#f4ead4"), warm)
        return lerp(c, to, float(t) * (1 - 0.35 * warm)).astype(F32)
    warm = np.clip((c[..., 0] - c[..., 2]) * 4, 0, 1)[..., None]
    to = lerp(col("#c9dcee")[None, None, :], col("#f4ead4")[None, None, :], warm)
    tt = (t if np.ndim(t) == 0 else t[..., None])
    return lerp(c, to, tt * (1 - 0.35 * warm)).astype(F32)


def facing_of(normal):
    """How squarely a face with this outward normal (x, y, D) takes the sun (0 to 1, before the Light's own curve)."""
    n = unit(normal)
    return float(max(0.0, n[0] * SUN[0] + n[1] * SUN[1] + n[2] * SUN[2]))


FACE_US = facing_of((0, 0, -1))                          # a wall that faces us
FACE_LEFT = facing_of((-1, 0, 0))                        # a wall on the right of the square, facing across it
FACE_RIGHT = facing_of((1, 0, 0))                        # a wall on the left of the square: 0, it is in shade
FACE_UP = facing_of((0, 1, 0))                           # the paving


# ---------------------------------------------------------------- surfaces
def travertine(a, b, ppc, seed, base=TRAV, long=118.0, high=58.0, spread=0.07, joint=1.4, holes_=True):
    """Squared travertine: pale, warm, pitted with small dark holes, its joints fine."""
    c, jm = stone(a, b, ppc, base, seed, long=long, high=high, spread=spread, joint=joint, joint_color="#8a7a68", blot=0.06)
    if holes_:
        pits = step(0.78, 0.86, tex(a * 1.0, b * 2.2, 9.0, seed + 40, 3)) * np.clip(ppc * 3.0, 0, 1)
        c = c * (1 - 0.18 * pits[..., None])
    return c, jm


def tufa(a, b, ppc, seed, base=TUFA, long=120.0, high=60.0):
    """Squared tufa: grey-ochre, softer, its blocks more varied and its arrises worn."""
    c, jm = stone(a, b, ppc, base, seed, long=long, high=high, spread=0.12, joint=1.8, joint_color="#6f5c50", blot=0.10)
    worn = step(0.55, 0.85, tex(a * 3.0, b * 1.2, 60, seed + 41, 3)) * 0.10
    return np.clip(c * (1 - worn[..., None]), 0, 1).astype(F32), jm


def plain(a, b, base, seed, amount=0.08, cell=120.0):
    """A plain surface with the gentle unevenness of a hand-laid wash: plaster, stucco, a painted board."""
    c = col(base)[None, None, :] * (1 + (tex(a, b, cell, seed)[..., None] - 0.5) * 2 * amount + (tex(a, b, cell / 5.0, seed + 1)[..., None] - 0.5) * amount)
    k = (tex(a, b, cell * 2.0, seed + 2)[..., None] - 0.5) * amount * 0.6
    return np.clip(c + np.concatenate([k, k * 0.1, -k], axis=-1), 0, 1).astype(F32)


def boards(a, b, seed, width=24.0, base="#b48a5c", gap=1.6, ppc=None):
    """Upright boards, side by side (a hoarding): each its own tone and grain, dark gaps between them, weathering
    paler toward the top. `a` across, `b` up, in cm."""
    i = np.floor(a / width)
    f = a / width - i
    tone = hash2(i, 3, seed)
    c = col(base)[None, None, :] * (0.82 + 0.30 * tone[..., None])
    warm = (hash2(i, 5, seed) - 0.5) * 0.08
    c = c + np.stack([warm, warm * 0.3, -warm], axis=-1)
    grain = tex(a * 5.0, b * 0.25, 40, seed + 1, 3)                    # long grain, up the board
    c = c * (0.90 + 0.18 * grain[..., None])
    knot = step(0.86, 0.92, tex(a * 2.0, b * 0.8, 30, seed + 2, 3))
    c = c * (1 - 0.25 * knot[..., None])
    w = gap if ppc is None else np.maximum(gap, 0.9 / np.maximum(ppc, 1e-3))
    seam = np.clip(1.5 - np.minimum(f, 1 - f) * width / (w * 0.5), 0, 1)
    if ppc is not None:
        seam = seam * np.clip(ppc * gap / 0.5, 0.25, 1.0)
    c = c * (1 - 0.55 * seam[..., None])
    c = c * (1 + 0.10 * np.clip((b - 60) / 160.0, 0, 1)[..., None])  # sun-bleached above
    return np.clip(c, 0, 1).astype(F32)


# ---------------------------------------------------------------- laying painted pieces on a canvas
def wall(canvas, fr, corners, paint, facing, shadow=0.0, deep=0.0, bounce=0.4, up=0.0, kind="front", plane=0.0, D=None, haze=None):
    """A flat piece of a building on a canvas: `corners` (u, v, h) in the frame `fr`; `kind` says which plane it lies in
    ("front": v = plane, "side": u = plane, "floor": h = plane); `paint(a, b, ppc, Wf)` gives its own colour from its
    two surface measurements (front: u, h; side: v, h; floor: u, v); `shadow` is a number or a function of (a, b)."""
    for Wf, m in fr.face(corners):
        if kind == "front":
            a, b, ppc = Wf.on_front(plane)
        elif kind == "side":
            a, b, ppc = Wf.on_side(plane)
        else:
            a, b, ppc = Wf.on_floor(plane)
        own = paint(a, b, ppc, Wf) if callable(paint) else col(paint)[None, None, :] * np.ones(a.shape + (1,), dtype=F32)
        cut = shadow(a, b, Wf) if callable(shadow) else shadow
        c = LIT.on(own, facing, cut, up=up, deep=deep, bounce=bounce)
        if haze is not None:
            c = far(c, haze)
        canvas.put(c, m, Wf)


def soft_canvas(c, soft=1.2):
    out = Canvas(c.shape)
    out.c, out.a = blur(c.c, soft), blur(c.a, soft)
    return out


def hand(a, seed=5):
    """A hand does not rule its lines (the same push as the steps' picture)."""
    return warp(warp(a, 0.7, 26, seed), 1.0, (150, 70), seed + 1)


def handed(layer, seed=5):
    out = Canvas(layer.shape)
    both = hand(np.dstack([layer.c, layer.a]), seed)
    out.c, out.a = both[..., :3].astype(F32), np.clip(both[..., 3], 0, 1).astype(F32)
    return out


def ground_uv():
    """For every pixel below the horizon: the place on the paving it shows (x, D) and pixels per cm."""
    u, v, ppc = WORLD.on_floor(0.0)
    return u, v, ppc


def person_px(row, height=1.0):
    """How tall the game draws someone with feet on this row (no limits)."""
    return 160.0 * height * scale_at(row)


def leaf(sheet, x, y, angle, length, tone, wide=0.26, rib=None, alpha=1.0):
    """One pointed leaf from its stalk end (as the steps' laurel)."""
    ca, sa = math.cos(angle), math.sin(angle)
    pts = []
    for t, w in ((0, 0), (0.25, 0.8), (0.5, 1.0), (0.78, 0.62), (1, 0)):
        pts.append((x + ca * length * t - sa * length * wide * w, y + sa * length * t + ca * length * wide * w))
    for t, w in ((0.78, 0.62), (0.5, 1.0), (0.25, 0.8)):
        pts.append((x + ca * length * t + sa * length * wide * w, y + sa * length * t - ca * length * wide * w))
    sheet.poly(pts, tone, alpha)
    if rib is not None:
        sheet.line([(x, y), (x + ca * length * 0.92, y + sa * length * 0.92)], rib, max(0.6, length * 0.05), 0.8)

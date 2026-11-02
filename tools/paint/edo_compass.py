"""PAINT-21B: the ship's clock (edo-compass): a close-up of the compass box on its post by Gonroku's helm, seen from
above, noon, the fifth day out (the key edo-sea). Nobody stands in it: the scene is a close-up (ROUND-21, "Close-ups";
the Egypt car's way: a tiny walk patch at the bottom middle until ENGINE-21's close-up mode makes it needless).

WHAT IS PAINTED (facts-21a item 8, facts-21d item 5: the funa-dokei, "the ship's clock", its card of twelve directions
named by the zodiac animals, and on a ship's compass cut the other way round, so that the needle names the heading):
    the box       a square box of worn wood filling the stage, its lid propped open at the top (hinged at the far edge)
    the card      the bowl's white floor: a ring of twelve marks, each a character (our own brush lettering, never a
                  font) with, beside it, a tiny animal in ink as a boy who cannot read would draw it (Kota drew them:
                  the game's), cut ANTICLOCKWISE: the rat at the bow mark (top), then clockwise round the card the boar,
                  the dog, the rooster (right), the monkey, the sheep, the horse (bottom), the snake, the dragon, the
                  hare (left), the tiger, the ox
    the bow mark  a small vermilion wedge on the bowl's rim at the top, where the box faces the bow
    the needle    on its pin, its tip on the monkey (120 degrees clockwise of the rat: west-south-west, the heading);
                  a cut-out in three positions for its tremble (needle, needle-l, needle-r)
    the thumb     Kanbei's weathered thumb on the box's near rim (a cut-out; the hand point `thumb`)
LIGHT   Noon, the sun high behind us and a little left: the rim and the card in full light; the bowl's near wall throws a
        crescent of blue shade on the card's near edge; the needle's shadow lies a little above and right of it.

  python3 edo_compass.py fast     without the brush pass (out/edo-compass-1-under.png, -2-all.png)
  python3 edo_compass.py          the full passes: out/edo-compass/ (back.png, the cut-outs, layout.json)
"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
from edo_deck_kit import (P, WHITE, NAPLES, CERULEAN, COBALT, ULTRA, PRUSSIAN, OCHRE, SIENNA, VERMILION, mixp, tintw, shade, Paper,
                          flat, WOOD_LIT, WOOD_MID, WOOD_SHADE, WOOD_DARK, IRON, DECK_SHADOW)

SEED = 1414
OUT = "out/edo-compass"
W, H = 800, 600
SHAPE = (H, W)
C = (400.0, 334.0)                          # the card's middle (the needle's pin)
SQ = 0.975                                  # the card is seen from a little in front: its height over its width
R_BOWL = 214.0                              # the bowl's rim
R_CARD = 196.0                              # the card's edge
R_OUT, R_IN = 190.0, 140.0                  # the ring of marks: its outer and inner circles
R_CORE = 96.0                               # the inner circle round the needle's middle
INK = lerp(PRUSSIAN, SIENNA, 0.18)          # sumi ink, as the act's palette has it: a blue-black (never black)
CARD = lerp(WHITE, NAPLES, 0.10)            # the card: white paper, warmed a breath by the sun
FLESH_D, FLESH_S, FLESH_L = P("flesh-deep"), P("flesh-shadow"), P("flesh-light")

# the twelve marks, clockwise from the bow mark (the ship's card: anticlockwise to a map's), with their angle (degrees
# clockwise from the top) and the branch's character
MARKS = [("rat", 0), ("boar", 30), ("dog", 60), ("rooster", 90), ("monkey", 120), ("sheep", 150), ("horse", 180),
         ("snake", 210), ("dragon", 240), ("hare", 270), ("tiger", 300), ("ox", 330)]
HEADING = "monkey"
THUMB_TIP = (590.0, 577.0)                  # Kanbei's thumb's tip, on the box's near rim (the hand point `thumb`)


def polar(r, deg, c=C):
    """A point on the card at radius r (px across) and an angle clockwise from the top."""
    t = math.radians(deg)
    return (c[0] + r * math.sin(t), c[1] - r * math.cos(t) * SQ)


# ================================================================ the lettering: our own brush strokes, no font
# Each character in a unit cell (x right, y down, 0..1), as strokes (polylines), drawn with a tapering brush. They are
# the twelve branches, written plainly as a ship's carpenter might cut them: legible as characters, nobody's typeface.
GLYPHS = {
    "rat": [[(0.26, 0.17), (0.72, 0.17), (0.50, 0.37)], [(0.50, 0.37), (0.51, 0.86), (0.41, 0.80)], [(0.13, 0.55), (0.87, 0.53)]],
    "ox": [[(0.22, 0.20), (0.70, 0.20), (0.66, 0.80)], [(0.44, 0.20), (0.44, 0.54)], [(0.27, 0.51), (0.74, 0.51)], [(0.11, 0.82), (0.89, 0.81)]],
    "tiger": [[(0.50, 0.04), (0.53, 0.12)], [(0.17, 0.20), (0.19, 0.30)], [(0.19, 0.20), (0.82, 0.20), (0.78, 0.30)], [(0.30, 0.35), (0.71, 0.35)],
              [(0.31, 0.43), (0.31, 0.71)], [(0.31, 0.43), (0.70, 0.43), (0.70, 0.71)], [(0.31, 0.57), (0.70, 0.57)], [(0.50, 0.30), (0.50, 0.71)],
              [(0.31, 0.71), (0.70, 0.71)], [(0.41, 0.78), (0.22, 0.93)], [(0.60, 0.78), (0.80, 0.93)]],
    "hare": [[(0.30, 0.13), (0.17, 0.28)], [(0.21, 0.27), (0.21, 0.82)], [(0.21, 0.30), (0.42, 0.30), (0.42, 0.62), (0.30, 0.60)],
             [(0.57, 0.20), (0.83, 0.20), (0.83, 0.64), (0.73, 0.59)], [(0.57, 0.20), (0.57, 0.93)]],
    "dragon": [[(0.30, 0.16), (0.85, 0.16)], [(0.30, 0.16), (0.28, 0.60), (0.13, 0.90)], [(0.43, 0.32), (0.76, 0.32)], [(0.38, 0.47), (0.85, 0.47)],
               [(0.43, 0.60), (0.43, 0.87), (0.58, 0.78)], [(0.57, 0.58), (0.72, 0.73), (0.89, 0.89)], [(0.80, 0.55), (0.66, 0.67)]],
    "snake": [[(0.23, 0.19), (0.73, 0.19), (0.73, 0.49)], [(0.23, 0.19), (0.23, 0.79), (0.35, 0.87), (0.84, 0.87), (0.85, 0.71)], [(0.23, 0.49), (0.73, 0.49)]],
    "horse": [[(0.35, 0.10), (0.21, 0.34)], [(0.27, 0.29), (0.77, 0.29)], [(0.14, 0.56), (0.87, 0.55)], [(0.51, 0.29), (0.51, 0.93)]],
    "sheep": [[(0.28, 0.26), (0.72, 0.26)], [(0.13, 0.45), (0.87, 0.45)], [(0.50, 0.08), (0.50, 0.93)], [(0.48, 0.49), (0.17, 0.83)], [(0.52, 0.49), (0.85, 0.83)]],
    "monkey": [[(0.28, 0.24), (0.28, 0.66)], [(0.28, 0.24), (0.72, 0.24), (0.72, 0.66)], [(0.28, 0.45), (0.72, 0.45)], [(0.28, 0.66), (0.72, 0.66)],
               [(0.50, 0.07), (0.50, 0.94)]],
    "rooster": [[(0.12, 0.13), (0.88, 0.13)], [(0.20, 0.30), (0.20, 0.90)], [(0.20, 0.30), (0.80, 0.30), (0.80, 0.90)], [(0.41, 0.13), (0.41, 0.50), (0.30, 0.58)],
                [(0.59, 0.13), (0.59, 0.55), (0.70, 0.55)], [(0.20, 0.71), (0.80, 0.71)], [(0.20, 0.90), (0.80, 0.90)]],
    "dog": [[(0.20, 0.30), (0.86, 0.30)], [(0.26, 0.30), (0.23, 0.66), (0.10, 0.91)], [(0.35, 0.58), (0.56, 0.58)], [(0.53, 0.09), (0.60, 0.50), (0.88, 0.90)],
            [(0.86, 0.60), (0.61, 0.83)], [(0.70, 0.11), (0.80, 0.19)]],
    "boar": [[(0.50, 0.05), (0.53, 0.14)], [(0.15, 0.20), (0.85, 0.20)], [(0.52, 0.21), (0.28, 0.45)], [(0.30, 0.43), (0.66, 0.40), (0.19, 0.79)],
             [(0.64, 0.50), (0.33, 0.90)], [(0.43, 0.66), (0.86, 0.90)], [(0.65, 0.58), (0.74, 0.67)]],
}


def glyph(sheet, name, cx, cy, size, deg, color=INK, width=2.5, seed=0):
    """A character centred at (cx, cy), `size` px tall, turned `deg` clockwise (its top toward the card's edge), with a
    brush's taper and a hand's small unevenness."""
    rng = np.random.default_rng(seed)
    t = math.radians(deg)
    ct, st = math.cos(t), math.sin(t)

    def to(u, v):
        x, y = (u - 0.5) * size, (v - 0.5) * size
        return (cx + x * ct - y * st, cy + (x * st + y * ct) * SQ)
    for stroke in GLYPHS[name]:
        pts = [to(u + rng.normal(0, 0.008), v + rng.normal(0, 0.008)) for u, v in stroke]
        dense = []
        for a, b in zip(pts[:-1], pts[1:]):
            for k in range(6):
                f = k / 6
                dense.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
        dense.append(pts[-1])
        n = len(dense)
        for i in range(n - 1):
            f = i / max(1, n - 2)
            w = width * (0.75 + 0.45 * math.sin(math.pi * min(1.0, f * 1.15)) - 0.25 * f)       # the brush presses in, lifts at the end
            sheet.line([dense[i], dense[i + 1]], color, max(0.9, w), 1.0)


# ================================================================ Kota's animals: a boy's ink drawings, upright
def doodle(sheet, name, cx, cy, s, seed=0, color=INK, width=1.3):
    """One of the twelve animals, as a twelve-year-old who cannot read draws it: a few wobbling lines, a dot for an eye.
    Centred at (cx, cy), about `s` px across. The game's own drawings."""
    rng = np.random.default_rng(seed)

    def P_(u, v):
        return (cx + (u - 0.5) * s + rng.normal(0, 0.35), cy + (v - 0.5) * s + rng.normal(0, 0.35))

    def L(*uv, w=width):
        pts = [P_(u, v) for u, v in uv]
        sheet.line(pts, color, w, 1.0)

    def O(u, v, ru, rv, n=16, start=0.0, end=2 * math.pi, w=width):
        pts = [P_(u + ru * math.cos(a), v + rv * math.sin(a)) for a in np.linspace(start, end, n)]
        sheet.line(pts, color, w, 1.0)

    def eye(u, v):
        p = P_(u, v)
        sheet.ellipse(p[0], p[1], max(0.9, s * 0.028), max(0.9, s * 0.028), color)
    if name == "rat":
        O(0.48, 0.58, 0.26, 0.15); L((0.72, 0.55), (0.88, 0.60), (0.73, 0.66)); O(0.66, 0.42, 0.06, 0.06); eye(0.76, 0.56)
        L((0.22, 0.60), (0.10, 0.50), (0.12, 0.34), (0.22, 0.30)); L((0.38, 0.72), (0.36, 0.80)); L((0.58, 0.72), (0.60, 0.80))
    elif name == "ox":
        L((0.20, 0.40), (0.70, 0.40), (0.72, 0.68), (0.22, 0.68), (0.20, 0.40)); O(0.80, 0.42, 0.10, 0.09); eye(0.82, 0.40)
        L((0.74, 0.34), (0.70, 0.22)); L((0.86, 0.34), (0.92, 0.22)); L((0.26, 0.68), (0.26, 0.84)); L((0.40, 0.68), (0.40, 0.84))
        L((0.56, 0.68), (0.56, 0.84)); L((0.68, 0.68), (0.68, 0.84)); L((0.20, 0.44), (0.10, 0.60))
    elif name == "tiger":
        O(0.46, 0.56, 0.26, 0.13); O(0.78, 0.44, 0.11, 0.10); eye(0.80, 0.42); L((0.72, 0.35), (0.72, 0.28), (0.76, 0.34)); L((0.84, 0.35), (0.86, 0.28), (0.88, 0.36))
        for u in (0.34, 0.44, 0.54):
            L((u, 0.45), (u + 0.03, 0.55))
        L((0.24, 0.66), (0.24, 0.80)); L((0.36, 0.68), (0.36, 0.80)); L((0.56, 0.68), (0.56, 0.80)); L((0.66, 0.66), (0.66, 0.80))
        L((0.20, 0.54), (0.08, 0.44), (0.10, 0.32))
    elif name == "hare":
        O(0.46, 0.62, 0.24, 0.15); O(0.70, 0.48, 0.10, 0.09); eye(0.73, 0.46); O(0.66, 0.24, 0.035, 0.16); O(0.76, 0.25, 0.035, 0.16)
        O(0.20, 0.58, 0.05, 0.05); L((0.36, 0.76), (0.32, 0.82)); L((0.56, 0.76), (0.60, 0.82))
    elif name == "dragon":
        L((0.08, 0.62), (0.22, 0.48), (0.38, 0.62), (0.54, 0.46), (0.70, 0.58), (0.80, 0.44))
        L((0.10, 0.70), (0.24, 0.56), (0.40, 0.70), (0.55, 0.54), (0.70, 0.66), (0.84, 0.54))
        O(0.88, 0.44, 0.08, 0.07); eye(0.89, 0.42); L((0.94, 0.46), (0.99, 0.40)); L((0.94, 0.48), (0.99, 0.54))
        for u in (0.22, 0.54):
            L((u, 0.48), (u + 0.02, 0.38))
        L((0.30, 0.66), (0.28, 0.78)); L((0.62, 0.62), (0.62, 0.74))
    elif name == "snake":
        L((0.14, 0.72), (0.30, 0.64), (0.36, 0.48), (0.50, 0.38), (0.64, 0.46), (0.66, 0.60), (0.78, 0.66), (0.88, 0.60), w=width * 1.6)
        eye(0.86, 0.58); L((0.91, 0.62), (0.98, 0.64)); L((0.98, 0.64), (1.0, 0.60)); L((0.98, 0.64), (1.0, 0.68))
    elif name == "horse":
        L((0.20, 0.46), (0.64, 0.46), (0.66, 0.64), (0.22, 0.64), (0.20, 0.46)); L((0.62, 0.46), (0.72, 0.24), (0.86, 0.26), (0.88, 0.34), (0.74, 0.36), (0.66, 0.52))
        eye(0.78, 0.29); L((0.66, 0.30), (0.62, 0.36)); L((0.69, 0.25), (0.64, 0.30))
        for u in (0.26, 0.36, 0.52, 0.62):
            L((u, 0.64), (u, 0.84))
        L((0.20, 0.48), (0.10, 0.56), (0.08, 0.68))
    elif name == "sheep":
        for k in range(7):
            a = k / 7 * 2 * math.pi
            O(0.44 + 0.20 * math.cos(a), 0.54 + 0.12 * math.sin(a), 0.07, 0.06, n=10)
        O(0.76, 0.44, 0.08, 0.07); eye(0.78, 0.42); L((0.70, 0.40), (0.66, 0.34))
        for u in (0.32, 0.42, 0.50, 0.58):
            L((u, 0.68), (u, 0.82))
    elif name == "monkey":
        O(0.46, 0.58, 0.16, 0.18); O(0.48, 0.30, 0.12, 0.11); eye(0.44, 0.29); eye(0.53, 0.29); L((0.44, 0.35), (0.49, 0.37), (0.54, 0.35))
        O(0.34, 0.28, 0.04, 0.05); O(0.62, 0.28, 0.04, 0.05)
        L((0.32, 0.52), (0.18, 0.60), (0.20, 0.70)); L((0.60, 0.52), (0.74, 0.46), (0.80, 0.38))
        L((0.40, 0.74), (0.36, 0.86)); L((0.54, 0.74), (0.58, 0.86))
        L((0.60, 0.70), (0.80, 0.78), (0.90, 0.66), (0.84, 0.56), (0.76, 0.62))
    elif name == "rooster":
        O(0.46, 0.58, 0.20, 0.15); O(0.64, 0.36, 0.08, 0.08); eye(0.66, 0.34); L((0.72, 0.37), (0.80, 0.40), (0.72, 0.42))
        L((0.58, 0.28), (0.60, 0.20), (0.64, 0.26), (0.67, 0.18), (0.70, 0.27)); L((0.68, 0.43), (0.67, 0.49))
        L((0.27, 0.52), (0.14, 0.32), (0.22, 0.30)); L((0.27, 0.56), (0.08, 0.42)); L((0.28, 0.60), (0.12, 0.56))
        L((0.42, 0.72), (0.40, 0.86), (0.36, 0.88)); L((0.52, 0.72), (0.54, 0.86), (0.58, 0.88))
    elif name == "dog":
        L((0.22, 0.46), (0.66, 0.46), (0.66, 0.64), (0.22, 0.64), (0.22, 0.46)); O(0.76, 0.40, 0.10, 0.09); eye(0.79, 0.38)
        L((0.70, 0.34), (0.66, 0.48)); L((0.86, 0.42), (0.92, 0.44)); L((0.22, 0.48), (0.12, 0.34), (0.16, 0.30))
        for u in (0.28, 0.38, 0.52, 0.62):
            L((u, 0.64), (u, 0.80))
    elif name == "boar":
        O(0.46, 0.56, 0.28, 0.16); O(0.80, 0.56, 0.06, 0.06); eye(0.70, 0.48); L((0.76, 0.62), (0.80, 0.68), (0.84, 0.64))
        for u in (0.30, 0.40, 0.50, 0.60):
            L((u, 0.40), (u + 0.02, 0.32))
        L((0.62, 0.40), (0.66, 0.30), (0.70, 0.40))
        for u in (0.28, 0.40, 0.54, 0.64):
            L((u, 0.70), (u, 0.80))
        L((0.18, 0.54), (0.10, 0.48), (0.12, 0.42))


# ================================================================ the box, the bowl, the card
BOX_FAR = (152.0, 648.0, 84.0)              # the box's far rim edge: x from, x to, row
BOX_NEAR = (112.0, 688.0, 606.0)            # its near rim edge (just under the picture's bottom)
RIM = 44.0                                  # the rim's width (px at the near edge)


def box_quad(inset=0.0):
    """The box's top, as the picture shows it (a little narrower far off), inset by `inset` px."""
    fx0, fx1, fy = BOX_FAR
    nx0, nx1, ny = BOX_NEAR
    k_far = 0.92
    return [(fx0 + inset * k_far, fy + inset * k_far), (fx1 - inset * k_far, fy + inset * k_far), (nx1 - inset, ny - inset), (nx0 + inset, ny - inset)]


def paint_deck_below(pic, seed):
    """The deck far below the box, at the stage's sides: planks running fore and aft (left to right), seen from above,
    pale (the air), and the box's shadow on them, short and blue, toward the top right (the sun is behind us)."""
    x, y = grid(SHAPE)
    wood = flat(lerp(tintw(OCHRE, 0.40), NAPLES, 0.15), SHAPE, seed + 1, 0.035, 40)
    over(pic, wood, np.ones(SHAPE, F32))
    sh = Paper(SHAPE)
    q = box_quad(-6)
    sh.poly([(p[0] + 46, p[1] - 58) for p in q], lerp(lerp(tintw(OCHRE, 0.40), NAPLES, 0.15), COBALT, 0.42), 0.9)
    c, a = sh.done()
    over(pic, c, a)
    lines = Paper(SHAPE)
    for r_ in np.arange(-6.0, 610.0, 15.5):
        lines.line([(-4, r_), (804, r_ + 2)], PRUSSIAN, 0.7, 0.30)
    rng = np.random.default_rng(seed)
    for r_ in np.arange(-6.0, 610.0, 15.5):
        for x_ in np.arange(rng.uniform(-80, 0), 820, rng.uniform(150, 230)):
            lines.line([(x_, r_), (x_ + 1, r_ + 15.5)], PRUSSIAN, 0.6, 0.28)
    lines.onto(pic)


def paint_lid(sheet, lines):
    """The lid, hinged at the box's far edge and propped open: its inside face toward us, leaning back out of the top
    of the picture; two iron hinges; a stick props it."""
    fx0, fx1, fy = BOX_FAR
    lid = [(fx0 + 4, fy + 2), (fx1 - 4, fy + 2), (fx1 - 30, -12), (fx0 + 30, -12)]
    sheet.poly(lid, lerp(WOOD_MID, COBALT, 0.10))
    # its grain, and the board's joint
    for k, x_ in enumerate(np.linspace(fx0 + 40, fx1 - 40, 7)):
        lines.line([(x_ + 6 * math.sin(k), fy - 2), (x_ * 0.95 + 20 + 4 * math.sin(k * 2), -10)], lerp(WOOD_MID, SIENNA, 0.45), 0.7, 0.45)
    lines.line([(400, fy - 1), (400, -10)], WOOD_DARK, 1.0, 0.6)
    # the inner batten across it
    sheet.poly([(fx0 + 24, 36), (fx1 - 24, 36), (fx1 - 22, 44), (fx0 + 22, 44)], lerp(WOOD_MID, SIENNA, 0.30))
    # hinges
    for hx in (fx0 + 70, fx1 - 70):
        sheet.poly([(hx - 18, fy - 12), (hx + 18, fy - 12), (hx + 16, fy + 8), (hx - 16, fy + 8)], IRON)
        for dx in (-10, 10):
            sheet.ellipse(hx + dx, fy - 4, 1.8, 1.8, lerp(IRON, CERULEAN, 0.5))
    # the prop: a stick from the box's far right corner up to the lid
    lines.line([(fx1 - 22, fy + 14), (fx1 - 46, 18)], WOOD_DARK, 4.0, 1.0)
    lines.line([(fx1 - 23, fy + 13), (fx1 - 47, 17)], tintw(OCHRE, 0.35), 1.4, 1.0)
    lines.line([lid[0], lid[3]], PRUSSIAN, 1.0, 0.8)
    lines.line([lid[1], lid[2]], PRUSSIAN, 1.0, 0.8)


def paint_box(sheet, lines, seed):
    """The box's top: a frame of old wood round a square opening, worn pale where hands have held it for years, its
    corners dovetailed, dents and a crack; in the opening, the bowl set in its packing."""
    rng = np.random.default_rng(seed)
    outer = box_quad(0)
    inner = box_quad(RIM)
    # the frame: four boards (two flats: the near and left boards turned to the sun a little more)
    sides = [(outer[0], outer[1], inner[1], inner[0], tintw(OCHRE, 0.30)),       # far
             (outer[1], outer[2], inner[2], inner[1], lerp(tintw(OCHRE, 0.22), SIENNA, 0.08)),   # right
             (outer[2], outer[3], inner[3], inner[2], tintw(OCHRE, 0.38)),       # near (most worn)
             (outer[3], outer[0], inner[0], inner[3], tintw(OCHRE, 0.34))]       # left
    for a, b, c, d, col in sides:
        sheet.poly([a, b, c, d], col)
    # the mitred corners
    for i in range(4):
        lines.line([outer[i], inner[i]], WOOD_DARK, 1.0, 0.8)
    # grain along each board, dents, a crack, worn pale patches on the near board where thumbs rest
    for (a, b, c, d, col) in sides:
        for v in np.linspace(0.18, 0.86, 5):
            p0 = (a[0] + (d[0] - a[0]) * v, a[1] + (d[1] - a[1]) * v)
            p1 = (b[0] + (c[0] - b[0]) * v, b[1] + (c[1] - b[1]) * v)
            mid = ((p0[0] + p1[0]) / 2 + rng.normal(0, 2), (p0[1] + p1[1]) / 2 + rng.normal(0, 2))
            lines.line([p0, mid, p1], lerp(col, SIENNA, 0.5), 0.7, 0.42)
    near = sides[2]
    for _ in range(9):
        u, v = rng.uniform(0.1, 0.9), rng.uniform(0.25, 0.8)
        px_ = near[1][0] + (near[0][0] - near[1][0]) * u
        py_ = near[0][1] + (near[3][1] - near[0][1]) * v
        sheet.ellipse(px_, py_, rng.uniform(2, 5), rng.uniform(1, 2), lerp(tintw(OCHRE, 0.38), SIENNA, 0.35), 0.6)
    sheet.poly([(500, 566), (640, 566), (636, 590), (504, 590)], lerp(tintw(OCHRE, 0.5), NAPLES, 0.3), 0.55)
    lines.line([(210, 112), (236, 120), (262, 118)], WOOD_DARK, 0.8, 0.7)                       # a crack in the far board
    # corner plates of iron at the near corners
    for cx_ in (outer[3][0] + 20, outer[2][0] - 20):
        sheet.poly([(cx_ - 16, 584), (cx_ + 16, 584), (cx_ + 16, 604), (cx_ - 16, 604)], IRON)
        sheet.ellipse(cx_, 592, 2.0, 2.0, lerp(IRON, CERULEAN, 0.5))
    # the opening: the packing round the bowl, in shade
    sheet.poly(inner, lerp(WOOD_SHADE, PRUSSIAN, 0.18))
    lines.line(outer + [outer[0]], PRUSSIAN, 1.2, 0.85)
    lines.line(inner + [inner[0]], PRUSSIAN, 1.0, 0.8)


def ell(c, rx, ry, n=90, a0=0.0, a1=2 * math.pi):
    return [(c[0] + rx * math.sin(a), c[1] - ry * math.cos(a)) for a in np.linspace(a0, a1, n)]


def paint_bowl_and_card(sheet, lines, seed):
    """The bowl (turned wood, its rim and inner wall) and the card on its floor: the ring of twelve marks with their
    characters and Kota's animals, the dividing lines, the bow mark; the near wall's crescent of shade on the card."""
    rng = np.random.default_rng(seed)
    # the bowl's rim, and its inner wall: the far side of the wall faces us and the sun (lit), the near side in shade
    sheet.poly(ell(C, R_BOWL, R_BOWL * SQ), lerp(WOOD_MID, SIENNA, 0.18))
    sheet.poly(ell(C, R_BOWL - 9, (R_BOWL - 9) * SQ), lerp(WOOD_LIT, NAPLES, 0.05))
    wall = ell((C[0], C[1] + 7), R_CARD + 2, (R_CARD + 2) * SQ)
    sheet.poly(ell(C, R_BOWL - 12, (R_BOWL - 12) * SQ), lerp(WOOD_SHADE, SIENNA, 0.1))
    # the card
    sheet.poly(ell((C[0], C[1] + 6), R_CARD, R_CARD * SQ), CARD)
    # the near wall's shade across the card's near edge (the sun is behind us: the wall nearest us throws it inward)
    crescent = ell((C[0], C[1] + 6), R_CARD, R_CARD * SQ, 60, math.radians(100), math.radians(260)) + \
        ell((C[0] - 4, C[1] - 6), R_CARD - 2, (R_CARD - 2) * SQ, 60, math.radians(256), math.radians(104))
    sheet.poly(crescent, lerp(CARD, COBALT, 0.30), 0.85)
    # the rings: the outer and inner circles of the marks, the core circle, a thin double line at the edge
    for rr, w, a in ((R_OUT, 1.6, 0.95), (R_OUT - 4, 0.7, 0.8), (R_IN, 1.4, 0.95), (R_CORE, 1.0, 0.85)):
        lines.line(ell(C, rr, rr * SQ, 120), INK, w, a)
    # the dividing lines between the marks (at the half-hours: 15, 45 ... degrees)
    for k in range(12):
        d = k * 30 + 15
        lines.line([polar(R_IN, d), polar(R_OUT, d)], INK, 1.2, 0.9)
        # the twelve directions as faint lines inward (a rose), and the half-points as dots
        lines.line([polar(R_CORE + 6, k * 30), polar(R_IN - 8, k * 30)], INK, 0.7, 0.35)
        p = polar((R_IN + R_CORE) / 2, d)
        sheet.ellipse(p[0], p[1], 1.4, 1.4, INK, 0.6)
    # each mark: its character (radial, its top toward the card's edge) on the counter-clockwise side of the sector,
    # and Kota's animal (upright, as he looks from the helm) on the clockwise side
    spots = {}
    for i, (name, deg) in enumerate(MARKS):
        gx, gy = polar((R_OUT + R_IN) / 2, deg - 6.5)
        glyph(lines, name, gx, gy, 30.0, deg - 6.5, seed=seed + i)
        ax_, ay_ = polar((R_OUT + R_IN) / 2 + 1, deg + 8.0)
        doodle(lines, name, ax_, ay_, 30.0, seed=seed + 50 + i, color=lerp(INK, SIENNA, 0.25), width=1.1)
        spots[name] = {"char": (gx, gy), "animal": (ax_, ay_), "deg": deg}
    # the bow mark: a vermilion wedge on the bowl's rim at the top, pointing in at the rat, and a cut line across the rim
    tip = polar(R_BOWL - 17, 0)
    b0, b1 = polar(R_BOWL + 3, -4.6), polar(R_BOWL + 3, 4.6)
    sheet.poly([tip, b1, b0], VERMILION)
    lines.line([tip, b1, b0, tip], lerp(VERMILION, PRUSSIAN, 0.35), 0.7, 0.6)
    # and a line of the same red painted across the box's far board, square to the bow (the way the box is set)
    top_in = BOX_FAR[2] + RIM * 0.92
    sheet.poly([(C[0] - 3.2, polar(R_BOWL + 3, 0)[1]), (C[0] + 3.2, polar(R_BOWL + 3, 0)[1]), (C[0] + 2.8, top_in - 30), (C[0] - 2.8, top_in - 30)], VERMILION)
    # the contour round the bowl
    lines.line(ell(C, R_BOWL, R_BOWL * SQ, 140), PRUSSIAN, 1.2, 0.85)
    lines.line(ell((C[0], C[1] + 6), R_CARD, R_CARD * SQ, 140), PRUSSIAN, 0.9, 0.6)
    return spots


# ================================================================ the cut-outs
def needle_cut(seed, offset=0.0):
    """The needle on its pin: a slim steel needle (prussian, lit along one edge), pointed at its tip, its tail blunt with
    a small cross-bar; the brass cap of the pin at its middle; its shadow a little up and right on the card.
    `offset`: degrees turned from the heading (the tremble: -1.4, 0, +1.4)."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    deg = dict(MARKS)[HEADING] + offset
    tip, tail = polar(R_IN - 6, deg), polar(R_CORE + 12, deg + 180)
    t = math.radians(deg)
    nx, ny = math.cos(t), math.sin(t) * SQ                             # across the needle, in the picture
    w = 5.0
    mid = C

    def body(dx=0.0, dy=0.0):
        return [(tip[0] + dx, tip[1] + dy), (mid[0] + nx * w + dx, mid[1] + ny * w + dy), (tail[0] + nx * w * 0.55 + dx, tail[1] + ny * w * 0.55 + dy),
                (tail[0] - nx * w * 0.55 + dx, tail[1] - ny * w * 0.55 + dy), (mid[0] - nx * w + dx, mid[1] - ny * w + dy)]
    sheet.poly(body(5.0, -6.0), lerp(CARD, COBALT, 0.35), 0.75)          # its shadow on the card
    sheet.poly(body(), lerp(IRON, ULTRA, 0.12))
    sheet.poly([tip, (mid[0] + nx * w, mid[1] + ny * w), mid], lerp(IRON, CERULEAN, 0.45))     # its lit edge
    # the tail's cross-bar
    a_, b_ = (tail[0] + nx * w * 1.6, tail[1] + ny * w * 1.6), (tail[0] - nx * w * 1.6, tail[1] - ny * w * 1.6)
    lines.line([a_, b_], IRON, 2.4, 1.0)
    # the pin's cap: brass
    sheet.ellipse(mid[0], mid[1], 8.5, 8.0, lerp(OCHRE, NAPLES, 0.3))
    sheet.ellipse(mid[0] - 1.5, mid[1] - 1.8, 3.5, 3.0, tintw(NAPLES, 0.6))
    lines.line(ell(mid, 8.5, 8.0, 30), lerp(SIENNA, PRUSSIAN, 0.4), 0.9, 0.9)
    lines.line(body() + [tip], PRUSSIAN, 0.9, 0.9)
    c, a = sheet.done()
    lc, la = lines.done()
    over(c, lc, la)
    return c, np.maximum(a, la)


def needle_poly(pad=7.0):
    """The needle's clickable outline: along it from the tail's bar to the tip, `pad` px either side."""
    deg = dict(MARKS)[HEADING]
    t = math.radians(deg)
    nx, ny = math.cos(t), math.sin(t) * SQ
    tip, tail = polar(R_IN - 2, deg), polar(R_CORE + 14, deg + 180)
    pts = [(tip[0] + nx * pad * 0.6, tip[1] + ny * pad * 0.6), (C[0] + nx * (pad + 4), C[1] + ny * (pad + 4)), (tail[0] + nx * pad, tail[1] + ny * pad),
           (tail[0] - nx * pad, tail[1] - ny * pad), (C[0] - nx * (pad + 4), C[1] - ny * (pad + 4)), (tip[0] - nx * pad * 0.6, tip[1] - ny * pad * 0.6)]
    return [[int(round(x)), int(round(y))] for x, y in pts]


def thumb_cut(seed, fast=False):
    """Kanbei's thumb on the box's near rim, seen from above: old, weathered, sun-browned (flesh-deep; its shade struck
    with cobalt, as the paints have it), lying on the rim, its tip toward the card; the nail thick and ridged and worn
    at its edge, the joint's creases; the ball of his hand at the stage's bottom edge."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    T = np.array(THUMB_TIP)                                           # the thumb's tip, on the rim
    B = np.array([694.0, 622.0])                                      # where it meets the hand, below the stage's edge
    L = float(np.linalg.norm(B - T))
    ax_ = (B - T) / L
    nx_ = np.array([ax_[1], -ax_[0]])                                 # across it, toward its upper (far) edge

    def at(u, v):
        p = T + ax_ * u * L + nx_ * v
        return (float(p[0]), float(p[1]))
    h = lambda u: 11.5 + 8.0 * u
    up = [at(u, h(u)) for u in np.linspace(1, 0, 16)]
    cap = [at(-(h(0) / L) * math.sin(a_), h(0) * math.cos(a_)) for a_ in np.linspace(0, math.pi, 13)]
    dn = [at(u, -h(u)) for u in np.linspace(0, 1, 16)]
    body = up + cap[1:-1] + dn
    # the ball of the hand beyond the base, at the stage's bottom
    palm = [at(0.78, h(0.78)), at(1.0, h(1.0) + 10), (790.0, 610.0), (790.0, 640.0), (620.0, 640.0), at(0.86, -h(0.86))]
    sheet.poly(palm, lerp(FLESH_D, SIENNA, 0.12))
    sheet.poly(body, lerp(FLESH_D, FLESH_S, 0.38))
    # its near (lower) side in shade, its far ridge catching the light
    sheet.poly([at(u, -h(u)) for u in np.linspace(0.02, 1, 10)] + [at(u, -h(u) * 0.30) for u in np.linspace(1, 0.02, 10)], lerp(FLESH_D, COBALT, 0.24))
    sheet.poly([at(u, h(u) * 0.86) for u in np.linspace(0.30, 0.95, 8)] + [at(u, h(u) * 0.40) for u in np.linspace(0.95, 0.30, 8)], lerp(FLESH_S, FLESH_L, 0.32), 0.85)
    # the nail: thick, ridged, pale, its free edge worn white
    nl = 0.30
    nail = [at(nl * (0.5 - 0.5 * math.cos(a_)), 8.6 * math.sin(a_)) for a_ in np.linspace(0, math.pi, 12)] + \
           [at(nl * (0.5 + 0.5 * math.cos(a_)), -8.2 * math.sin(a_)) for a_ in np.linspace(0, math.pi, 12)]
    sheet.poly(nail, lerp(tintw(OCHRE, 0.52), FLESH_L, 0.42))
    sheet.poly([at(0.0, 0.0), at(0.03, 6.8), at(0.07, 7.6), at(0.07, -7.2), at(0.03, -6.4)], tintw(NAPLES, 0.62))
    for k in (-3.6, 0.0, 3.6):
        lines.line([at(0.08, k), at(nl - 0.03, k * 1.05)], lerp(FLESH_S, SIENNA, 0.45), 0.6, 0.7)
    lines.line(nail + [nail[0]], lerp(SIENNA, PRUSSIAN, 0.35), 0.8, 0.9)
    # the joint's creases (across it, a little beyond the nail), the weather's lines toward the hand
    for u, w_ in ((0.44, 0.9), (0.48, 0.7), (0.52, 0.8)):
        lines.line([at(u, h(u) * 0.75), at(u + 0.02, 0.0), at(u, -h(u) * 0.7)], lerp(SIENNA, PRUSSIAN, 0.35), w_, 0.75)
    for u in (0.66, 0.74, 0.82):
        lines.line([at(u, h(u) * 0.55), at(u + 0.03, h(u) * 0.05)], lerp(SIENNA, PRUSSIAN, 0.3), 0.6, 0.5)
    # the contour: warm on the lit (far) side, prussian under it
    lines.line(up + cap[:7], lerp(SIENNA, PRUSSIAN, 0.25), 1.1, 0.95)
    lines.line(cap[6:] + dn, PRUSSIAN, 1.1, 0.9)
    c, a = sheet.done()
    lc, la = lines.done()
    over(c, lc, la)
    return c, np.maximum(a, la)


# ================================================================ the passes
def under(seed=SEED):
    pic = np.zeros(SHAPE + (3,), F32)
    paint_deck_below(pic, seed)
    sheet = Paper(SHAPE)
    paint_lid(sheet, sheet)
    paint_box(sheet, sheet, seed + 5)
    sheet.onto(pic)
    card = Paper(SHAPE)
    spots = paint_bowl_and_card(card, card, seed + 9)
    cc, ca = card.done()
    over(pic, cc, ca)
    return np.clip(pic, 0, 1), {"spots": spots, "card": (cc, ca)}


def details(pic, info, seed=SEED):
    """The card, the box's lines and the lid said again crisply over the brush: the lettering and the animals must be
    exact."""
    sheet = Paper(SHAPE)
    paint_lid(sheet, sheet)
    paint_box(sheet, sheet, seed + 5)
    c, a = sheet.done()
    over(pic, c, (a * 0.7).astype(F32))
    cc, ca = info["card"]
    over(pic, cc, ca)
    return pic


def layout(planes, info):
    """layout.json: the close-up's things (each mark a sector big enough to click), the hand point, the cut-outs."""
    def r(p):
        return [int(round(p[0])), int(round(p[1]))]

    def box_of(alpha, pad=0):
        ys, xs = np.where(alpha > 0.5)
        return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 1 + 2 * pad, int(ys.max() - ys.min()) + 1 + 2 * pad]
    things = []
    for name, deg in MARKS:
        # the mark's sector of the card, from inside the ring of marks out to the bowl's rim: about 92 px deep
        pts = [r(polar(R_CORE + 16, d)) for d in np.linspace(deg - 14.5, deg + 14.5, 5)] + \
              [r(polar(R_BOWL - 14, d)) for d in np.linspace(deg + 14.5, deg - 14.5, 7)]
        sp = info["spots"][name]
        things.append({"id": name, "what": f"the {name}'s mark: its character and, beside it, Kota's {name} in ink" + (" (the needle's tip is on it: the heading)" if name == HEADING else "")
                       + (" (at the bow mark)" if name == "rat" else ""), "shape": {"poly": pts}, "deg": deg,
                       "char_at": r(sp["char"]), "animal_at": r(sp["animal"])})
    nb = box_of(np.maximum.reduce([planes["needle"][1], planes["needle-l"][1], planes["needle-r"][1]]), 4)
    tb = box_of(planes["thumb"][1], 2)
    fx0, fx1, fy = BOX_FAR
    outer = box_quad(0)
    inner = box_quad(RIM)
    things = [
        {"id": "box", "what": "the compass box: old wood, worn pale where hands have held it", "shape": {"poly": [r(outer[0]), r(outer[1]), r((outer[2][0], 598)), r((outer[3][0], 598)), r(outer[3])] if False else
                                                                                                  [r(outer[0]), r(outer[1]), [688, 598], [112, 598]]}},
        {"id": "lid", "what": "the lid, propped open (hinged at the far edge)", "shape": {"poly": [[int(fx0 + 4), int(fy)], [int(fx1 - 4), int(fy)], [int(fx1 - 30), 2], [int(fx0 + 30), 2]]}},
        {"id": "card", "what": "the card: the ship's clock, twelve marks cut the other way round", "shape": {"poly": [r(p) for p in ell(C, R_CORE, R_CORE * SQ, 24)]}},
        {"id": "bowmark", "what": "the bow mark: a little vermilion wedge on the rim, at the rat", "shape": {"rect": [int(C[0] - 16), int(polar(R_BOWL + 6, 0)[1]) - 6, 32, 26]}},
        {"id": "needle", "what": "the needle on its pin, trembling; its tip on the monkey", "shape": {"poly": needle_poly()}},
        {"id": "thumb", "what": "Kanbei's thumb on the box's edge, weathered", "shape": {"rect": tb}},
    ] + things
    return {
        "id": "edo-compass", "closeup": True,
        "horizon": 300, "full": 600,
        "view": {"what": "a close-up from above (nobody stands in it): the box on its post seen from over the helm, a little in front; no floor",
                 "card": {"centre": r(C), "squash": SQ, "ring_out": R_OUT, "ring_in": R_IN, "bowl": R_BOWL,
                          "order": "clockwise from the top: rat (the bow mark), boar, dog, rooster (right), monkey, sheep, horse (bottom), snake, dragon, hare (left), tiger, ox: the ship's card, cut anticlockwise to a map's"}},
        "light": "noon, the sun high behind us and a little left: the rim and the card lit; the bowl's near wall throws a crescent of blue shade over the card's near edge; the needle's shadow lies a little above and right of it",
        "walk": [[380, 586], [420, 586], [420, 598], [380, 598]], "walk_note": "a tiny patch at the bottom middle, as the Egypt car's: nobody walks here (until ENGINE-21's close-up mode makes it needless)",
        "blocked": [],
        "marks": {"default": [400, 594]},
        "hands": {"thumb": [int(THUMB_TIP[0]), int(THUMB_TIP[1])]},
        "hands_note": "`thumb`: the tip of Kanbei's thumb on the box's near rim (painted: the cut-out `thumb`); a hand the engine draws for whoever is active would go to the card's edge by its mark",
        "planes": [
            {"id": "needle", "file": "needle.png", "plane": "front", "states": {"still": "needle.png", "left": "needle-l.png", "right": "needle-r.png"},
             "what": "the needle on its pin, its tip on the monkey; the three are its tremble (fx needle-tremble)"},
            {"id": "thumb", "file": "thumb.png", "plane": "front", "what": "Kanbei's thumb on the box's near rim"},
        ],
        "cutouts": {"needle": box_of(planes["needle"][1]), "needle-l": box_of(planes["needle-l"][1]), "needle-r": box_of(planes["needle-r"][1]), "thumb": box_of(planes["thumb"][1])},
        "things": things,
        "fx": [{"id": "needle-tremble", "type": "frames", "plane": "needle", "cycle": ["needle.png", "needle-l.png", "needle.png", "needle-r.png"], "fps": 3, "jitter": 0.5,
                "what": "the needle trembling on its pin: the three positions in turn, unevenly, three or four times a second",
                "note": "a cut-out's states flipped in turn (ENGINE-21: a 'frames' kind, or the scene's own small loop); for less motion, still"}],
    }


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.012, amount=0.018):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = "fast" in sys.argv
    base, info = under()
    Image.fromarray((base * 255).astype(np.uint8)).save(OUT + "-1-under.png")
    pic = base.copy() if fast else strokes(base, sizes=(9, 5, 2), seed=4, density=1.5, jitter=0.025, keep=0.34)
    details(pic, info)
    planes = {"needle": needle_cut(SEED + 1, 0.0), "needle-l": needle_cut(SEED + 1, -1.4), "needle-r": needle_cut(SEED + 1, 1.4), "thumb": thumb_cut(SEED + 2)}
    whole = pic.copy()
    for name in ("needle", "thumb"):
        c, a = planes[name]
        over(whole, c, (a > 0.5).astype(F32))
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-all.png")
    with open(OUT + "/layout.json", "w") as f:
        json.dump(layout(planes, info), f, indent=1)
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    print("back", finish(pic, OUT + "/back.png", 160))
    for name, n in (("needle", 32), ("needle-l", 32), ("needle-r", 32), ("thumb", 40)):
        print(name, finish(planes[name][0], OUT + f"/{name}.png", n, planes[name][1]))
    comp = Image.open(OUT + "/back.png").convert("RGBA")
    for name in ("needle", "thumb"):
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(OUT + "-comp.png")
    print("done", round(time.time() - t0, 1))

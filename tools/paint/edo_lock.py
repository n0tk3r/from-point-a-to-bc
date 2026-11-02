"""The shipwright's lock on the women's hall's doors (edo-lock): a close-up, late afternoon. PAINT-21E, round twenty-one.

The design (S/briefs/out/edo2-design.md, section 5 and #37; S/briefs/PAINT-21E.md; ROUND-21.md "Close-ups"): a whole-stage
picture of one thing seen close, nobody standing in it (the Egypt car's way: a tiny walk patch at the bottom middle until
ENGINE-21's close-up mode makes it unneeded). The lock is the game's invention, made from the documented features of Edo
trick locks (several keys, a hidden keyhole, a sound when the trick is solved: facts-21c item 11): a block of dark wood
bound with iron, carved as a rabbit running over waves (the moon rabbit running on the waves is a woman's motif of the
period, on a travel comb box and a hand mirror: facts-21d item 13; a lock in that shape is ours, and the carving is our own
drawing, copied from no piece).

FLAT AND FRONTAL, 22 pixels to the centimetre (the lock's body 21 x 10 cm is 462 x 220 px): the doors' lattice behind and
the seam where the two leaves meet; on the left leaf the hasp's iron plate and its staple; the lock on the right leaf's
stile, its bolt through the staple; slips pasted on the stiles. The light: the low gold sun from the left, raking across
the carving, so that every raised edge is lit on its upper left and shaded on its lower right.

The moving parts, each a cut-out with its states, each big enough to click:
  ear           the long ear laid back along the rabbit's back, its tiny hole black with dust     (ear-clean: the hole clean)
  wave          the middle of the three waves, in place                                           (wave-slid: slid aside to the right)
  (the post)    under the middle wave, in its recess: a square iron post (the backdrop: seen when the wave is slid)
  post-coin     the one-mon coin seated on the post
  post-turned   the post and the coin turned a quarter
  back-open     along the rabbit's back, the carved line opened into a row of thin slits (shut: the backdrop's line)
  bolt          the bolt through the staple                                                       (bolt-out: drawn back)

  python3 edo_lock.py          paints everything into out/edo-lock/ (and out/edo-lock-comp.png to look at)
  python3 edo_lock.py fast     no brush pass: out/edo-lock-2-all.png and the states only"""

import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, Sheet, grid, noise, blur, over, tint, glow, lerp, mask_poly, mask_ellipse, strokes, curve, warp, vary
from rome_steps_kit import Canvas
from edo_town_kit import (PAINT, PAPER, LINE, mix, shade_of, sheet_layer, outline, brushed, finish, to_png, hull, box_of)

W, H = 800, 600
SHAPE = (H, W)
OUT = "out/edo-lock"
S = 22.0                                   # pixels to the centimetre
O = (204.0, 196.0)                         # the lock body's top-left corner, picture
BODY = (21.0, 10.0)                        # the lock body, cm
SEAM = 176.0                               # the seam between the two leaves (picture x)


def Q(x, y):
    """A point on the lock in its own measure (cm from the body's top-left, y down) -> the picture."""
    return (O[0] + x * S, O[1] + y * S)


def QS(pts):
    return [Q(x, y) for (x, y) in pts]


# ---------------------------------------------------------------- colours: the late gold light from the left
C = dict(
    wood=mix(mix(PAINT["sienna"], PAINT["ochre"], 0.25), PAINT["naples"], 0.08), wood_lit=mix(mix(PAINT["ochre"], PAINT["naples"], 0.4), PAINT["sienna"], 0.25),
    wood_sh=shade_of(mix(PAINT["sienna"], PAINT["ochre"], 0.2), 0.45), wood_dark=mix(PAINT["sienna"], PAINT["prussian"], 0.55),
    gap=mix(PAINT["prussian"], PAINT["sienna"], 0.28), gap_deep=mix(PAINT["prussian"], "#000000", 0.25),
    lock=mix(mix(PAINT["sienna"], PAINT["prussian"], 0.62), "#000000", 0.12), lock_top=mix(mix(PAINT["sienna"], PAINT["prussian"], 0.42), PAINT["ochre"], 0.08),
    lock_lit=mix(mix(PAINT["sienna"], PAINT["ochre"], 0.45), PAINT["naples"], 0.25), lock_sh=mix(PAINT["prussian"], "#000000", 0.30),
    iron=mix(PAINT["prussian"], "#4a4e58", 0.45), iron_lit=mix("#8c96ae", PAINT["naples"], 0.35), iron_sh=mix(PAINT["prussian"], "#000000", 0.35),
    rust=mix(PAINT["sienna"], PAINT["ochre"], 0.3),
    paper=mix(PAPER, PAINT["naples"], 0.18), paper_old=mix(PAPER, PAINT["ochre"], 0.32), paper_sh=shade_of(mix(PAPER, PAINT["naples"], 0.1), 0.3), ink=LINE,
    copper=mix(mix(PAINT["orange"], PAINT["ochre"], 0.45), PAINT["naples"], 0.15), copper_lit=mix(PAINT["naples"], PAPER, 0.25),
    copper_sh=mix(PAINT["sienna"], PAINT["orange"], 0.25), copper_rim=mix(PAINT["sienna"], PAINT["prussian"], 0.25), patina=mix(PAINT["viridian"], PAINT["veronese"], 0.45),
    dust=mix(mix(PAINT["sienna"], PAINT["prussian"], 0.5), "#7a7468", 0.35), dust_fluff=mix("#9a948a", PAINT["ochre"], 0.15),
    sun=mix(PAINT["naples"], PAPER, 0.3), line=LINE,
)


# ---------------------------------------------------------------- the doors behind
LEFT_STILE = (84.0, SEAM)                  # the left leaf's meeting stile (x), the right leaf's (the lock is on it)
RIGHT_STILE = (SEAM, 690.0)


def doors(s):
    """The two leaves' lattice: a grid of square bars of weathered wood, the dim hall seen between them; the two
    meeting stiles wide and plain, the seam a dark line between them; the light from the left on the bars' left faces."""
    s.poly([(-10, -10), (810, -10), (810, 610), (-10, 610)], C["gap"])
    # the far dim: a little of the hall's inside, a darker band low
    s.poly([(-10, 430), (810, 430), (810, 610), (-10, 610)], C["gap_deep"], 0.6)
    # the lattice bars (only off the stiles)
    xs = [-30.0, 716.0, 800.0]                               # vertical bars beyond the stiles
    ys = [-30.0, 92.0, 500.0]                                 # horizontal bars
    bw = 26.0
    for y in ys:
        s.poly([(-10, y), (810, y), (810, y + bw), (-10, y + bw)], C["wood"])
        s.poly([(-10, y), (810, y), (810, y + 5), (-10, y + 5)], C["wood_lit"], 0.9)
        s.poly([(-10, y + bw - 6), (810, y + bw - 6), (810, y + bw), (-10, y + bw)], C["wood_sh"], 0.8)
    for x in xs:
        s.poly([(x, -10), (x + bw, -10), (x + bw, 610), (x, 610)], C["wood"])
        s.poly([(x, -10), (x + 6, -10), (x + 6, 610), (x, 610)], C["wood_lit"], 0.9)
        s.poly([(x + bw - 6, -10), (x + bw, -10), (x + bw, 610), (x + bw - 6, 610)], C["wood_sh"], 0.8)
        for y in ys:                                          # the joints, halved: a hairline
            s.line([(x, y), (x + bw, y)], C["wood_dark"], 0.8, 0.6)
    # the meeting stiles: wide, plain, worn smooth at the middle by hands
    for (x0, x1) in (LEFT_STILE, RIGHT_STILE):
        st = [(x0, -10), (x1, -10), (x1, 610), (x0, 610)]
        s.poly(st, C["wood"])
        s.poly([(x0, -10), (x0 + 10, -10), (x0 + 10, 610), (x0, 610)], C["wood_lit"], 0.85)
        s.poly([(x1 - 9, -10), (x1, -10), (x1, 610), (x1 - 9, 610)], C["wood_sh"], 0.75)
        for k in range(6):                                    # the grain, drawn
            xx = x0 + 18 + k * (x1 - x0 - 30) / 5
            s.line([(xx, -10), (xx + 4, 300), (xx - 2, 610)], C["wood_dark"], 0.7, 0.28)
    s.line([(SEAM, -10), (SEAM, 610)], C["gap_deep"], 3.0)
    s.line([(SEAM - 2, -10), (SEAM - 2, 610)], C["wood_sh"], 1.0, 0.8)


SLIPS = [  # (x, y, w, h, age) on the stiles: paper and thin wood, round the lock but clear of it
    (100, 20, 40, 150, 0.2), (96, 430, 44, 150, 0.7), (190, 470, 40, 130, 0.4), (612, 20, 44, 150, 0.5), (640, 450, 40, 140, 0.15),
    (420, 486, 38, 120, 0.85), (300, 18, 36, 120, 0.4), (520, 40, 34, 104, 0.95),
]


def sign_column(s, cx, y0, y1, rng, ink, scale=1.0):
    """A column of brushed signs of our own down a slip, top to bottom: short verticals, pairs, dots, ticks, hooks, small
    boxes and loops, each in a cell of its own with a gap above and below. No stroke crosses or touches another: in a
    women's hall of 1830 the cross was the forbidden sign (and the act's hidden Christians make one loaded), so nothing
    written here may read as one (PAINT-21E, at the lead's word)."""
    kinds = ["vert", "vert", "vert", "pair", "dot", "dots", "tick", "hook", "box", "loop"]
    tall = {"vert": (6.0, 10.0), "pair": (5.0, 7.0), "dot": (3.0, 3.0), "dots": (6.0, 6.0), "tick": (4.0, 6.0), "hook": (7.0, 10.0),
            "box": (5.0, 5.0), "loop": (5.5, 5.5)}
    y = y0
    while True:
        k = kinds[int(rng.integers(len(kinds)))]
        h = rng.uniform(*tall[k]) * scale
        if y + h > y1:
            break
        x = cx + rng.uniform(-0.8, 0.8)
        wd = rng.uniform(1.5, 2.1) * scale
        if k == "vert":
            s.line([(x, y), (x + rng.uniform(-0.6, 0.6), y + h)], ink, wd, 0.88)
        elif k == "pair":
            for dx in (-2.4, 2.4):
                s.line([(x + dx * scale, y), (x + dx * scale, y + h)], ink, wd * 0.72, 0.85)
        elif k == "dot":
            s.ellipse(x, y + h / 2, 1.5 * scale, 1.3 * scale, ink, 0.9)
        elif k == "dots":
            s.ellipse(x, y + 1.3 * scale, 1.3 * scale, 1.1 * scale, ink, 0.9)
            s.ellipse(x, y + h - 1.3 * scale, 1.3 * scale, 1.1 * scale, ink, 0.9)
        elif k == "tick":
            side = 1 if rng.random() < 0.5 else -1
            s.line([(x - side * 2.0 * scale, y), (x + side * 2.0 * scale, y + h)], ink, wd * 0.8, 0.85)
        elif k == "hook":
            side = 1 if rng.random() < 0.5 else -1
            s.line([(x, y), (x, y + h * 0.78), (x + side * 2.6 * scale, y + h)], ink, wd * 0.85, 0.88)
        elif k == "box":
            bw = 2.8 * scale
            s.line([(x - bw, y), (x + bw, y), (x + bw, y + h), (x - bw, y + h), (x - bw, y)], ink, wd * 0.6, 0.85)
        else:
            s.line([(x + 2.6 * scale * math.cos(t), y + h / 2 + h / 2 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 13)], ink, wd * 0.6, 0.85)
        y += h + rng.uniform(3.0, 5.0) * scale


def slips(s):
    """Name slips pasted on the stiles (paper; one of thin wood): the pilgrimage's name brushed down the middle, the
    province, the name and the date at the sides: here our own brush marks, no real text. Old ones yellowed, torn at a
    corner; the newest white."""
    rng = np.random.default_rng(71)
    for (x, y, w, h, age) in SLIPS:
        tone = C["paper"] if age < 0.5 else (C["paper_old"] if age < 0.9 else mix(C["wood_lit"], C["paper"], 0.45))
        p = [(x, y), (x + w, y + 1), (x + w - 1, y + h), (x + 1, y + h - 1)]
        if age > 0.6:                                        # a torn corner
            p = [(x, y + 8), (x + 8, y), (x + w, y + 1), (x + w - 1, y + h), (x + 1, y + h - 1)]
        s.poly(p, tone)
        s.poly([(x + w - 5, y + 1), (x + w, y + 1), (x + w - 1, y + h), (x + w - 6, y + h)], C["paper_sh"], 0.35)
        # the brush marks: a column of signs down the middle (PAINT-21E fix: no stroke crosses another), two thin
        # columns of short strokes at the sides
        sign_column(s, x + w / 2, y + 10, y + h - 12, rng, C["ink"])
        for sx in (x + 6, x + w - 7):
            yy = y + 16
            while yy < y + h * 0.7:
                s.line([(sx, yy), (sx, yy + 4)], C["ink"], 0.8, 0.6)
                yy += rng.uniform(7, 11)
        outline(s, p, 0.7, 0.45)


# ---------------------------------------------------------------- the hasp and its staple
STAPLE = (130.0, 306.0)                    # the staple's loop centre (picture)


def hasp(s):
    """The hasp's iron plate on the left leaf's stile, riveted, its staple standing out through which the bolt goes;
    rust at its edges."""
    plate = [(100, 226), (164, 222), (168, 392), (104, 396)]
    s.poly(plate, C["iron"])
    s.poly([(100, 226), (164, 222), (165, 234), (101, 238)], C["iron_lit"], 0.8)
    s.poly([(157, 228), (164, 222), (168, 392), (161, 392)], C["iron_sh"], 0.7)
    for (x, y) in ((112, 238), (154, 236), (116, 380), (157, 378)):
        s.ellipse(x, y, 4.2, 4.2, C["iron_sh"])
        s.ellipse(x - 1, y - 1, 3.2, 3.2, C["iron_lit"])
    for k in range(9):                                       # rust at its edges
        x = 102 + k * 7
        s.ellipse(x, 394 - (k % 3), 3.0, 1.6, C["rust"], 0.6)
    outline(s, plate, 1.0, 0.7)
    # the staple: a thick iron loop standing out from the plate
    cx, cy = STAPLE
    s.ellipse(cx, cy, 26, 32, C["iron_sh"])
    s.ellipse(cx - 2, cy - 2, 26, 32, C["iron"])
    s.ellipse(cx, cy, 15, 20, C["gap_deep"])                  # its hole (the bolt passes through it)
    s.line([(cx - 24, cy - 12), (cx - 16, cy - 26)], C["iron_lit"], 2.6, 0.9)
    outline(s, [(cx - 2 + 26 * math.cos(t), cy - 2 + 32 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 28, endpoint=False)], 0.9, 0.7)


# ---------------------------------------------------------------- the lock
RABBIT = [  # the rabbit's outline, cm: running to the left over the waves, stretched out, its ears laid back
    (2.3, 3.6), (2.9, 3.0), (3.7, 2.6), (4.6, 2.5), (5.6, 2.5), (7.0, 2.35), (8.6, 2.2), (10.2, 2.2), (11.8, 2.35), (13.2, 2.6), (14.3, 2.9),
    (15.1, 2.7), (15.8, 2.9), (15.7, 3.5), (15.1, 3.7),                       # the round tail
    (16.4, 4.4), (17.6, 5.3), (18.0, 5.8), (17.3, 5.9), (16.0, 5.3), (14.6, 4.7),   # the hind leg, pushing back
    (13.0, 4.9), (11.0, 5.0), (8.8, 4.95), (6.9, 4.7),                       # the belly
    (5.4, 5.2), (3.6, 5.9), (2.4, 6.1), (2.2, 5.7), (3.3, 5.2), (4.6, 4.5),  # the fore leg, reaching forward
    (3.6, 4.3), (2.6, 4.1),                                                  # the jaw
]
EAR = [(4.8, 2.6), (5.8, 1.55), (7.4, 1.05), (9.2, 0.85), (10.9, 0.95), (11.9, 1.3), (11.2, 1.75), (9.4, 1.85), (7.6, 2.05), (6.1, 2.6), (5.5, 3.0)]
EARHOLE = (9.3, 1.38)
SLITS = (11.9, 15.0, 2.52)                 # along the back behind the ear: from x, to x, at y (cm)
WAVES = [  # three waves: (x0, x1) cm, each a curling crest
    (1.0, 7.6), (6.9, 13.5), (12.8, 19.6)]
WAVE_Y = (5.9, 9.6)
POST = (10.4, 8.05, 0.72)                  # the square post in the middle wave's recess: centre, side (cm)
BOLT_Y = 5.0                               # the bolt's height on the body (cm)


def wave_shape(x0, x1, y0=WAVE_Y[0], y1=WAVE_Y[1]):
    """A carved wave: the swell rising from the right to a tall crest that curls over to the left (the way the rabbit
    runs) and breaks into foam fingers; under the curl its hollow. -> (body, hollow, fingers)"""
    w = x1 - x0
    h = y1 - y0
    body = [(x0, y1), (x0 + w * 0.02, y0 + h * 0.62), (x0 + w * 0.10, y0 + h * 0.30), (x0 + w * 0.22, y0 + h * 0.10), (x0 + w * 0.36, y0 + h * 0.02),
            (x0 + w * 0.50, y0 + h * 0.06), (x0 + w * 0.66, y0 + h * 0.24), (x0 + w * 0.82, y0 + h * 0.50), (x0 + w * 0.94, y0 + h * 0.72), (x1, y1)]
    hollow = [(x0 + w * 0.09, y0 + h * 0.30), (x0 + w * 0.11, y0 + h * 0.50), (x0 + w * 0.19, y0 + h * 0.64), (x0 + w * 0.30, y0 + h * 0.66),
              (x0 + w * 0.38, y0 + h * 0.56), (x0 + w * 0.31, y0 + h * 0.55), (x0 + w * 0.23, y0 + h * 0.52), (x0 + w * 0.18, y0 + h * 0.42),
              (x0 + w * 0.16, y0 + h * 0.30)]
    fingers = []
    for k in range(5):                                        # the foam: claws curling down off the crest's front
        fx = x0 + w * (0.06 + 0.06 * k)
        fy = y0 + h * (0.30 - 0.04 * k)
        fingers.append([(fx + w * 0.05, fy - h * 0.06), (fx, fy), (fx - w * 0.025, fy + h * 0.12)])
    return body, hollow, fingers


def wave_lines(s, x0, x1, dx=0.0):
    """The swell's carved lines, following the wave's back."""
    w = x1 - x0
    h = WAVE_Y[1] - WAVE_Y[0]
    for k in range(3):
        t = 0.30 + k * 0.18
        pts = [(x0 + dx + w * (0.40 + 0.1 * k), WAVE_Y[0] + h * (0.22 + t * 0.6)), (x0 + dx + w * 0.62, WAVE_Y[0] + h * (0.36 + t * 0.5)),
               (x0 + dx + w * 0.86, WAVE_Y[0] + h * (0.66 + t * 0.3))]
        s.line(QS(pts), C["lock_sh"], 1.2, 0.75)


def carve(s, pts, top, lit, sh, lw=1.6):
    """A raised flat in relief, as the raking light from the left shows it: the shade side drawn first, offset down and
    right; then the flat; then its lit edge along the upper left."""
    pp = QS(pts)
    s.poly([(x + 3.2, y + 3.2) for (x, y) in pp], sh)
    s.poly(pp, top)
    n = len(pp)
    for i in range(n):
        a, b = pp[i], pp[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        nl = math.hypot(dx, dy) + 1e-6
        nx, ny = dy / nl, -dx / nl                            # the edge's outward normal (for a clockwise outline)
        if nx * -0.7 + ny * -0.7 > 0.25:                      # facing up and left: lit
            s.line([a, b], lit, lw, 0.95)
    outline(s, pp, 0.9, 0.55)


def lock_body(s):
    """The lock's body: a block of dark wood, its front face, its top and its right end in shade; iron bands round both
    ends with their rivets; the carving on its face (the rabbit, the outer two waves; the ear, the middle wave, the slits
    and the bolt are cut-outs). The carved line along the rabbit's back (shut) and the middle wave's recess with the
    square post in it are here, under the cut-outs."""
    bw, bh = BODY
    face = QS([(0, 0), (bw, 0), (bw, bh), (0, bh)])
    # its top face (seen a little from below? No: from the front, level: a thin lit edge), its right end in shade
    s.poly([(face[1][0], face[1][1]), (face[1][0] + 10, face[1][1] + 8), (face[2][0] + 10, face[2][1] + 8), (face[2][0], face[2][1])], C["lock_sh"])
    s.poly([(face[3][0], face[3][1]), (face[2][0], face[2][1]), (face[2][0] + 10, face[2][1] + 8), (face[3][0] + 10, face[3][1] + 8)], C["lock_sh"])
    s.poly(face, C["lock"])
    # the grain of the dark wood, drawn faintly
    rng = np.random.default_rng(72)
    for k in range(9):
        y = 0.6 + k * 1.05
        s.line([Q(0.3, y), Q(7, y + rng.uniform(-0.2, 0.2)), Q(14, y + rng.uniform(-0.2, 0.2)), Q(bw - 0.3, y)], C["lock_top"], 0.8, 0.35)
    # the recess the middle wave slides in (inside the wave's own outline, so the wave in place hides it), the post in it
    x0, x1 = WAVES[1]
    body, _, _ = wave_shape(x0, x1)
    cxw = (x0 + x1) / 2
    cyw = (WAVE_Y[0] + WAVE_Y[1]) / 2 + 0.6
    rec = [(cxw + (x - cxw) * 0.80, cyw + (y - cyw) * 0.78) for (x, y) in body]
    s.poly(QS(rec), C["lock_sh"])
    s.poly(QS([(x, y) for (x, y) in rec if y < cyw]), mix(C["lock_sh"], "#000000", 0.3))
    post(s, 0.0)
    # the outer two waves, carved
    for (wx0, wx1) in (WAVES[0], WAVES[2]):
        body, hollow, fingers = wave_shape(wx0, wx1)
        carve(s, body, C["lock_top"], C["lock_lit"], C["lock_sh"])
        s.poly(QS(hollow), C["lock_sh"])
        for f in fingers:
            s.line(QS(f), C["lock_lit"], 1.6, 0.85)
        wave_lines(s, wx0, wx1)
    # the rabbit, carved
    carve(s, RABBIT, C["lock_top"], C["lock_lit"], C["lock_sh"], lw=1.8)
    # its eye, the line of its haunch and shoulder
    ex, ey = Q(3.6, 3.15)
    s.ellipse(ex, ey, 4.0, 3.4, C["lock_sh"])
    s.ellipse(ex - 1, ey - 1, 1.4, 1.2, C["lock_lit"])
    s.line(QS([(13.6, 3.0), (13.0, 3.9), (13.7, 4.6)]), C["lock_sh"], 1.4, 0.85)
    s.line(QS([(6.2, 3.0), (5.6, 3.9), (5.9, 4.5)]), C["lock_sh"], 1.2, 0.8)
    s.line(QS([(2.6, 3.7), (2.4, 3.9)]), C["lock_sh"], 1.2, 0.8)                     # the nostril
    # the carved line along its back (the slits are shut: a fine groove)
    a, b, y = SLITS
    s.line(QS([(a, y), (b, y + 0.08)]), C["lock_sh"], 2.0)
    s.line(QS([(a, y + 0.12), (b, y + 0.2)]), C["lock_lit"], 0.8, 0.7)
    # the iron bands round both ends, their rivets
    for (bx0, bx1) in ((0.0, 1.4), (bw - 1.4, bw)):
        band = QS([(bx0, -0.15), (bx1, -0.15), (bx1, bh + 0.15), (bx0, bh + 0.15)])
        s.poly(band, C["iron"])
        s.poly([band[0], (band[0][0] + 5, band[0][1]), (band[3][0] + 5, band[3][1]), band[3]], C["iron_lit"], 0.75)
        for yy in (1.2, bh / 2, bh - 1.2):
            rx, ry = Q((bx0 + bx1) / 2, yy)
            s.ellipse(rx + 1, ry + 1, 4.6, 4.6, C["iron_sh"])
            s.ellipse(rx, ry, 4.2, 4.2, C["iron"])
            s.ellipse(rx - 1.2, ry - 1.2, 1.8, 1.8, C["iron_lit"])
        outline(s, band, 0.9, 0.65)
    # the bolt's hole in the left band
    hx, hy = Q(0.0, BOLT_Y)
    s.ellipse(hx + 7, hy, 9, 14, C["gap_deep"])
    outline(s, face, 1.1, 0.7)


def post(s, turn=0.0, coin=False):
    """The square iron post in the recess (seen end on from the front: we look straight at its square end), with a groove
    across it that shows how it is turned; with the coin seated on it (its square hole over the post), turned with it."""
    cx, cy = Q(POST[0], POST[1])
    half = POST[2] * S / 2
    th = math.radians(turn)

    def rot(x, y):
        return (cx + x * math.cos(th) - y * math.sin(th), cy + x * math.sin(th) + y * math.cos(th))
    if coin:
        r = 1.25 * S                                         # a one-mon coin: about 2.5 cm across
        s.ellipse(cx + 3, cy + 3, r, r, mix(C["lock_sh"], "#000000", 0.2))                 # its shadow on the post's recess
        s.ellipse(cx, cy, r, r, C["copper_rim"])
        s.ellipse(cx, cy, r - 2.5, r - 2.5, C["copper"])
        s.poly([(cx - r * 0.7, cy - r * 0.2), (cx - r * 0.2, cy - r * 0.7), (cx + r * 0.1, cy - r * 0.62), (cx - r * 0.62, cy + r * 0.1)], C["copper_lit"], 0.55)
        # the rim, and four marks round the hole (a coin's characters: here our own, turned with the coin): each two short
        # strokes lying along the hole's side, one outside the other, apart (PAINT-21E fix: no stroke crosses or meets
        # another, and none points at the hole: four strokes pointing in would make a cross)
        rim = [(cx + r * 0.86 * math.cos(t), cy + r * 0.86 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 30, endpoint=False)]
        s.line(rim + [rim[0]], C["copper_sh"], 1.0, 0.8)
        for k in range(4):
            a = th + k * math.pi / 2
            ux, uy = math.cos(a - math.pi / 2), math.sin(a - math.pi / 2)      # outward, toward this mark
            tx, ty = math.cos(a), math.sin(a)                                  # along the hole's side
            for (rho, l0, l1, wd) in ((0.48, -3.2, 3.2, 1.6), (0.65, -2.2, 1.4, 1.2)):
                mx, my = cx + r * rho * ux, cy + r * rho * uy
                s.line([(mx + l0 * tx, my + l0 * ty), (mx + l1 * tx, my + l1 * ty)], C["copper_sh"], wd, 0.9)
        for k in range(6):                                   # a little green patina
            a = k * 1.1 + 0.4
            s.ellipse(cx + r * 0.7 * math.cos(a), cy + r * 0.7 * math.sin(a), 2.2, 1.6, C["patina"], 0.5)
        hole = [rot(-half - 1.0, -half - 1.0), rot(half + 1.0, -half - 1.0), rot(half + 1.0, half + 1.0), rot(-half - 1.0, half + 1.0)]
        s.poly(hole, C["gap_deep"])
        outline(s, [(cx + r * math.cos(t), cy + r * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 30, endpoint=False)], 1.0, 0.7)
    sq = [rot(-half, -half), rot(half, -half), rot(half, half), rot(-half, half)]
    s.poly([(x + 1.5, y + 1.5) for (x, y) in sq], C["iron_sh"])
    s.poly(sq, C["iron"])
    s.line([rot(-half, -half), rot(half, -half)], C["iron_lit"], 1.2, 0.9)
    s.line([rot(-half, -half), rot(-half, half)], C["iron_lit"], 1.2, 0.9)
    s.line([rot(-half * 0.8, 0), rot(half * 0.8, 0)], C["iron_sh"], 1.6)            # the groove across its end
    outline(s, sq, 0.8, 0.7)


# ---------------------------------------------------------------- the moving parts (cut-outs)
def ear(s, clean=False):
    """The long ear laid back along the rabbit's back, carved; its tiny hole black with forty years of dust (clean: the
    hole open and dark, a glint of iron inside, the dust wiped from round it)."""
    carve(s, EAR, mix(C["lock_top"], C["lock_lit"], 0.15), C["lock_lit"], C["lock_sh"], lw=1.6)
    s.line(QS([(5.8, 2.3), (7.6, 1.6), (9.4, 1.35), (11.2, 1.35)]), C["lock_sh"], 1.2, 0.75)        # the ear's inner line
    hx, hy = Q(*EARHOLE)
    if not clean:
        s.ellipse(hx, hy, 6.5, 4.6, C["dust"])                # grime round it
        s.ellipse(hx, hy, 3.0, 2.4, mix(C["dust"], C["dust_fluff"], 0.5))
        for k in range(7):                                    # fluff
            a = k * 0.9
            s.line([(hx + 2 * math.cos(a), hy + 1.5 * math.sin(a)), (hx + 6 * math.cos(a), hy + 4.4 * math.sin(a))], C["dust_fluff"], 0.8, 0.8)
    else:
        s.ellipse(hx, hy, 2.6, 2.2, C["gap_deep"])
        s.ellipse(hx + 0.6, hy + 0.4, 1.0, 0.8, C["iron_lit"], 0.9)
        s.ellipse(hx - 4, hy - 2.4, 3.0, 1.4, C["lock_lit"], 0.45)      # the wiped place, a little brighter
    s.ellipse(hx, hy, 3.2, 2.6, LINE, 0.0)


def wave_mid(s, slid=False):
    """The middle wave, a separate block in its recess: in place; or slid to the right, along its groove, over the
    third wave's foot, so that the recess and the square post show."""
    x0, x1 = WAVES[1]
    dx = 3.6 if slid else 0.0
    body, hollow, fingers = wave_shape(x0 + dx, x1 + dx)
    carve(s, body, mix(C["lock_top"], C["lock_lit"], 0.08), C["lock_lit"], C["lock_sh"])
    s.poly(QS(hollow), C["lock_sh"])
    for f in fingers:
        s.line(QS(f), C["lock_lit"], 1.6, 0.85)
    wave_lines(s, x0, x1, dx)
    s.line(QS([(x0 + dx + 0.1, WAVE_Y[1] - 0.05), (x1 + dx - 0.1, WAVE_Y[1] - 0.05)]), C["lock_sh"], 1.6)   # its foot in the groove


def back_open(s):
    """Along the rabbit's back, behind the ear, the carved line opened into a row of thin slits, as close together as
    the teeth of a fine comb, dark, each with a lit lip."""
    a, b, y = SLITS
    n = 30
    for k in range(n):
        x = a + (b - a) * (k + 0.5) / n
        p0, p1 = Q(x, y - 0.08), Q(x, y + 0.5)
        s.line([p0, p1], C["gap_deep"], 1.6)
        s.line([(p0[0] - 1.2, p0[1]), (p1[0] - 1.2, p1[1])], C["lock_lit"], 0.6, 0.7)
    s.line(QS([(a - 0.1, y - 0.12), (b + 0.1, y - 0.04)]), C["lock_lit"], 1.0, 0.8)


def bolt(s, out_=False):
    """The bolt: a round iron rod from the lock's left end through the staple (in); or drawn back into the lock, only
    its blunt end showing at the band (out)."""
    hx, hy = Q(0.0, BOLT_Y)
    if out_:
        s.ellipse(hx + 2, hy, 11, 15, C["iron"])
        s.ellipse(hx + 1, hy - 1, 7, 10, C["iron_lit"], 0.6)
        outline(s, [(hx + 2 + 11 * math.cos(t), hy + 15 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 20, endpoint=False)], 0.8, 0.7)
        return
    x0 = STAPLE[0] - 46
    rod = [(x0, hy - 13), (hx + 4, hy - 13), (hx + 4, hy + 13), (x0, hy + 13)]
    s.poly(rod, C["iron"])
    s.poly([(x0, hy - 13), (hx + 4, hy - 13), (hx + 4, hy - 6), (x0, hy - 6)], C["iron_lit"], 0.85)
    s.poly([(x0, hy + 6), (hx + 4, hy + 6), (hx + 4, hy + 13), (x0, hy + 13)], C["iron_sh"], 0.8)
    s.ellipse(x0, hy, 8, 13, C["iron_sh"])
    s.ellipse(x0 - 1, hy - 1, 5, 9, C["iron"])
    outline(s, rod, 0.9, 0.7)
    # the staple's near side crosses in front of the rod (the rod goes THROUGH the loop)
    cx, cy = STAPLE
    s.line([(cx - 26, cy + 14), (cx - 28, cy - 2), (cx - 26, cy - 18)], C["iron"], 9.0)
    s.line([(cx - 30, cy + 10), (cx - 32, cy - 2)], C["iron_lit"], 2.6, 0.9)
    s.line([(cx - 21, cy + 14), (cx - 23, cy - 2), (cx - 21, cy - 18)], LINE, 0.8, 0.6)


# ---------------------------------------------------------------- the passes
def under():
    pic = np.zeros(SHAPE + (3,), F32)
    layers = {}
    for name, fn, amt in (("doors", doors, 0.3), ("slips", slips, 0.2), ("hasp", hasp, 0.0), ("lock", lock_body, 0.0)):
        lay = sheet_layer(fn, amt)
        lay.onto(pic)
        layers[name] = lay
    # the late light raking from the left: a broad warm wash on the lock's left and the stile, falling off to the right
    x, y = grid(SHAPE)
    g = np.clip(1 - (x - 120) / 760.0, 0, 1) ** 1.6
    glow(pic, C["sun"], (g * 0.10).astype(F32))
    # the lock's shadow on the stile, down and to the right (the light low from the left)
    sh = Sheet(SHAPE)
    bw, bh = BODY
    face = QS([(0, 0), (bw, 0), (bw, bh), (0, bh)])
    sh.poly([(face[1][0], face[1][1] + 6), (face[1][0] + 26, face[1][1] + 26), (face[2][0] + 26, face[2][1] + 26), (face[3][0] + 26, face[3][1] + 26), (face[3][0], face[3][1])], C["gap"])
    c, a = sh.done()
    lm = sheet_layer(lock_body, 0.0).a
    tint(pic, mix(C["gap"], C["wood_sh"], 0.3), np.clip(a - lm, 0, 1) * 0.45)
    return np.clip(pic, 0, 1), layers


def details(pic, layers):
    crisp = pic.copy()
    for name in ("hasp", "lock", "slips"):
        layers[name].onto(crisp)
    pic[...] = lerp(pic, crisp, 0.86)
    return pic


CUTS = ["wave", "ear", "bolt"]                                              # back to front, as the scene lists them
ALTS = ["ear-clean", "wave-slid", "post-coin", "post-turned", "back-open", "bolt-out"]


def cut_layers():
    return {
        "wave": sheet_layer(lambda s: wave_mid(s), 0.0),
        "wave-slid": sheet_layer(lambda s: wave_mid(s, True), 0.0),
        "ear": sheet_layer(lambda s: ear(s), 0.0),
        "ear-clean": sheet_layer(lambda s: ear(s, True), 0.0),
        "post-coin": sheet_layer(lambda s: post(s, 0.0, True), 0.0),
        "post-turned": sheet_layer(lambda s: post(s, 90.0, True), 0.0),
        "back-open": sheet_layer(back_open, 0.0),
        "bolt": sheet_layer(lambda s: bolt(s), 0.0),
        "bolt-out": sheet_layer(lambda s: bolt(s, True), 0.0),
    }


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = len(sys.argv) > 1 and sys.argv[1] == "fast"
    base, layers = under()
    pic = base.copy() if fast else strokes(base, sizes=(9, 5, 2), seed=4, density=1.4, jitter=0.02, keep=0.45)
    ground_ = pic.copy()
    details(pic, layers)
    details(ground_, layers)
    cuts = cut_layers()
    whole = pic.copy()
    cut = {}
    for i, n in enumerate(CUTS + ALTS):
        layer = cuts[n]
        if fast:
            c, a = layer.straight()
            a = (a > 0.5).astype(F32)
        else:
            c, a = brushed(layer, ground_, seed=80 + i, sizes=(4, 2, 2), restate=0.94)
        cut[n] = (c, a)
        if n in CUTS:
            over(whole, c, a)
    to_png(whole, f"{OUT}-2-all.png")
    states = whole.copy()
    for n in ("ear-clean", "wave-slid", "post-turned", "back-open", "bolt-out"):
        c, a = cut[n]
        over(states, c, a)
    to_png(states, f"{OUT}-2-open.png")
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    print("back", finish(pic, f"{OUT}/back.png", 160)[0])
    for n, (c, a) in cut.items():
        print(n, finish(c, f"{OUT}/{n}.png", 64, a)[0])
    import edo_lock_layout as LY
    LY.write(f"{OUT}/layout.json")
    comp = Image.open(f"{OUT}/back.png").convert("RGBA")
    for n in CUTS:
        comp.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
    comp.convert("RGB").save(f"{OUT}-comp.png")
    print("done", round(time.time() - t0, 1))

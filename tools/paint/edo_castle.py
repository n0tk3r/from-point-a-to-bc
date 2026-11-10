"""Himeji, about 29 April 1830, late afternoon: the approach to the keep (edo-castle). PAINT-20D, round twenty.

The design (S/briefs/out/edo-design.md, section 4): the game's own painting, composed and coloured as the woodblock
landscape prints are: big flat masses and silhouettes, a graded sky, a fine even contour in prussian blue, few colours,
the deep blue leading. Nothing is copied from any print: the composition is our own.

What is in it (edo_castle_kit.py has the measurements): the one old double cherry in the foreground at the left, its
heavy pink clusters framing the top-left; the road across the bottom; the moat under the white wall at the left, where
the herons stand (the game's frames: edo_castle_herons.py); the stone ramp up to the terrace before the Ni-no-mon gate at
the right, a gate in a white wall with a small tiled tower over it and a gable whose end tile carries a cross (small);
the plasterers' bamboo scaffold against the wall by the gate, the mixing tub, three buckets of lime, Tomezo's ladder
against the gate's outer wall; and the keep, white, five roofs on its tall sloping stone base, high on its hill at the
back against the sky. Not painted: people (the game's), petals (ENGINE-20's moving thing), the herons (frames), light.

The picture is a backdrop and cut-outs: ladder (behind everybody), gate (its opening clear: people pass into it), scaffold
(people pass in front of and behind it), tub, bucket-1 to bucket-3 (the crew carries them away: the scene hides each),
cherry (the trunk and the boughs: people pass under and behind them).

  python3 edo_castle.py          paints everything into out/edo-castle/ (and out/edo-castle-comp.png to look at)
  python3 edo_castle.py fast     skips the brush pass: out/edo-castle-fast/ and out/edo-castle-fast-comp.png

DEPTH-23 (round twenty-three, tools/paint/DEPTH.md): the scene is painted by edo_castle_depth.py now, in three planes and
in the act's watercolour (with edo_castle_model.py, _far.py, _cuts.py, _near.py); running this script runs that one. This
file's drawing functions stay exactly as round twenty left them: the outlines of the cut-outs are theirs (edo_castle_cuts
lays them again), and edo_town.py draws Himeji's keep from the town with keep() below."""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
import sky
from rome_steps_kit import Canvas, courses, hash2
from edo_castle_kit import *


def hand(a, amount=1.0):
    """A hand does not rule its lines: push a picture or mask about a little (always the same push)."""
    return warp(warp(a, 0.5 * amount, 24, 5), 0.8 * amount, (140, 60), 6)


def sheet_layer(draw, amount=0.6, ss=3):
    """Draw with a Sheet onto a clear Canvas, the edges pushed a little by hand. -> Canvas"""
    s = Sheet(SHAPE, ss)
    draw(s)
    c, a = s.done()
    out = Canvas(SHAPE)
    if amount:
        both = hand(np.dstack([c * a[..., None], a]), amount)
        out.c, out.a = both[..., :3].astype(F32), np.clip(both[..., 3], 0, 1).astype(F32)
    else:
        out.c, out.a = (c * a[..., None]).astype(F32), a
    return out


def outline(s, pts, width=1.0, alpha=0.6, close=True):
    """The keyblock's contour: a fine even prussian-blue line."""
    p = list(pts) + ([pts[0]] if close else [])
    s.line(p, C["line"], width, alpha)


def eave(x0, x1, y, lift=4.0, n=14):
    """The line of a tiled eave: level in the middle, its corners lifted a little (as the roofs are)."""
    out = []
    cx, half = (x0 + x1) / 2, (x1 - x0) / 2
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        out.append((x, y - lift * (abs(x - cx) / half) ** 3.2))
    return out


# ---------------------------------------------------------------- the sky, the hills
PAPER = "#f6eed8"                                            # lead white: the paper


def sky_layer(seed=20, bands=8):
    """The graded sky as the prints print it (bokashi): eight flat bands of the box's blues, deepest at the top, the
    lowest band the paper, their boundaries soft and a little wobbled; a whisper of naples at the sun's side; three flat
    lens clouds with a prussian edge on their tops only."""
    x, y = grid(SHAPE)
    drift = (noise(SHAPE, (520, 260), seed, 3) - 0.5) * 0.10
    t = np.clip(y / HZ + drift, 0, 1)
    tq = ((np.floor(t * bands) + 0.5) / bands).astype(F32)
    tq = warp(blur(tq, 2.4), 2.0, 40, seed + 3)                                   # the boundaries blurred and wobbled
    stops = [(0.0, mix("#2f63b8", "#1a2846", 0.4)), (0.28, "#2f63b8"), (0.55, "#7fb8de"), (0.80, mix("#7fb8de", PAPER, 0.6)), (1.0, PAPER)]
    pic = ramp(np.clip(tq, 0, 1), stops)
    pic *= (1 + (noise(SHAPE, (300, 120), seed + 1, 4) - 0.5)[..., None] * 0.04)   # the wash is even: 2%
    g = np.clip(1 - np.hypot((x - 900) / 520.0, (y - 300) / 200.0), 0, 1) ** 1.6 * (y < HZ + 2) * (t > 0.7)
    over(pic, "#f4d88e", (g * 0.22).astype(F32))                                   # naples, a whisper, at the sun's side
    s = Sheet(SHAPE)
    for (cx, cy, w, h) in ((560, 78, 300, 16), (640, 96, 180, 10), (120, 48, 150, 10)):
        top = [(cx - w / 2 + w * i / 10, cy - h * (0.5 + 0.5 * math.sin(i * 1.9 + cx) * 0.6) * (1 - ((i - 5) / 5.5) ** 2)) for i in range(11)]
        s.poly(top + [(cx + w / 2, cy), (cx - w / 2, cy)], PAPER, 0.96)
        s.line(top, C["line"], 0.9, 0.5)                                          # the keyblock's edge on the top only
    s.onto(pic)
    return np.clip(pic, 0, 1).astype(F32)


def hills(s):
    """The Harima hills far off, flat and pale, right of the keep's hill (no contour: the far plane); the hill the keep
    stands on, a low dark mass just over the wall, with pines standing on it against the sky in three depths."""
    rng = np.random.default_rng(21)
    ridge = [(430, 262), (470, 254), (520, 258), (580, 246), (640, 250), (700, 240), (760, 248), (810, 244), (810, 300), (430, 300)]
    s.poly(curve(ridge[:8], 4) + ridge[8:], far(C["hills_far"], 0.5))
    ridge2 = [(520, 275), (580, 268), (640, 272), (720, 262), (790, 270), (810, 266), (810, 300), (520, 300)]
    s.poly(curve(ridge2[:6], 4) + ridge2[6:], far(C["hills_mid"], 0.3))
    crest = [(px, 322 - 5 * math.sin(px / 90.0) - 3 * math.sin(px / 31.0)) for px in range(-20, 840, 20)]
    s.poly(crest + [(840, 360), (-20, 360)], C["pine_dark"])
    for depth, (yb, step_, hs, tone, lit) in enumerate(((300, 30, (20, 32), far(C["pine"], 0.55), far(C["pine_lit"], 0.55)),
                                                         (322, 44, (34, 56), far(C["pine"], 0.25), far(C["pine_lit"], 0.25)),
                                                         (346, 62, (44, 74), C["pine_dark"], C["pine"]))):
        for px in np.arange(-10 + depth * 13, 830, step_):
            if rng.random() < 0.22:
                continue                                      # gaps: sky between the trees
            h = rng.uniform(*hs)
            pine(s, px + rng.uniform(-6, 6), yb + rng.uniform(-3, 3), h, tone, lit, rng)


def pine(s, x, y, h, tone, lit, rng):
    """A pine as the prints draw it: a bent dark trunk showing between flat layered pads, each pad a lens, narrower
    going up, its top edge toward the sun a shade lighter."""
    bend = rng.uniform(-0.12, 0.12)
    trunk = [(x, y), (x + h * bend * 0.5, y - h * 0.45), (x + h * bend, y - h * 0.92)]
    s.line(trunk, mix(tone, "#000000", 0.35), max(0.9, h * 0.05))
    n = 3 if h < 36 else 4
    for j in range(n):
        f = (j + 0.9) / (n + 0.5)
        cx = x + h * bend * f + rng.uniform(-1, 1)
        cy = y - h * (0.28 + 0.66 * f)
        rx = h * (0.50 - 0.30 * f) * rng.uniform(0.85, 1.15)
        ry = max(2.0, rx * 0.24)
        top = [(cx - rx + 2 * rx * i / 10, cy - ry * (0.55 + 0.45 * math.sin(i / 10 * math.pi))) for i in range(11)]
        bottom = [(cx + rx - 2 * rx * i / 7, cy + ry * 0.45 * rng.uniform(0.4, 1.0)) for i in range(1, 7)]
        s.poly(top + bottom, tone)
        s.poly([(q[0], q[1]) for q in top[4:]] + [(cx + rx * 0.3, cy - ry * 0.1)], lit, 0.55)   # the pad's top toward the sun


# ---------------------------------------------------------------- the keep
KEEP = [  # each storey: wall x0, x1, wall top row, wall foot row; its roof: eave x0, x1, eave row, the row the roof meets the next wall
    dict(w=(280, 440), top=222, foot=266, r=(258, 462), eave=222, up=203, gable="chidori"),
    dict(w=(294, 426), top=174, foot=203, r=(276, 444), eave=174, up=156),
    dict(w=(306, 414), top=130, foot=156, r=(290, 430), eave=130, up=114, gable="chidori"),
    dict(w=(318, 402), top=90, foot=114, r=(304, 416), eave=90, up=76, gable="kara"),
    dict(w=(328, 392), top=56, foot=76, r=(316, 404), eave=56, up=38, ridge=(342, 378)),
]
BASE = dict(foot=(246, 474, 332), top=(276, 444, 266))        # the stone base: x0, x1 at its foot row; x0, x1 at its top row


def keep(s):
    """The keep: white walls, five roofs with their lifted corners, white gables, the plastered undersides of the
    eaves, on its tall sloping stone base. The right faces warm, the left lilac; the roofs prussian blue-grey."""
    rng = np.random.default_rng(22)
    # the stone base, its sides curving out toward the foot
    fx0, fx1, fy = BASE["foot"]
    tx0, tx1, ty = BASE["top"]
    left = [(tx0 + (fx0 - tx0) * ((i / 8) ** 1.8), ty + (fy - ty) * i / 8) for i in range(9)]
    right = [(tx1 + (fx1 - tx1) * ((i / 8) ** 1.8), ty + (fy - ty) * i / 8) for i in range(9)]
    base_poly = left + right[::-1]
    s.poly(base_poly, C["stone"])
    s.poly([(tx0 + 2, ty), ((tx0 + tx1) / 2 + 10, ty)] + [((l[0] + (r[0] - l[0]) * 0.56), l[1]) for l, r in zip(left[1:], right[1:])][::-1][::-1] + [left[-1]] , C["stone_shade"], 0.0)
    # the left half of the base in shade, the right lit (a soft division)
    shade = [left[i] for i in range(9)] + [((left[i][0] + right[i][0]) / 2 - 8 + i * 1.5, left[i][1]) for i in range(8, -1, -1)]
    s.poly(shade, C["stone_shade"], 0.75)
    lit_ = [((left[i][0] + right[i][0]) / 2 + 12, left[i][1]) for i in range(9)] + [right[i] for i in range(8, -1, -1)]
    s.poly(lit_, C["stone_lit"], 0.55)
    for i in range(1, 9):                                     # the courses, faint
        s.line([left[i], right[i]], C["stone_joint"], 0.6, 0.35)
    for j in range(60):                                       # and a few upright joints
        i = rng.integers(0, 8)
        t = rng.random()
        xa = left[i][0] + (right[i][0] - left[i][0]) * t
        xb = left[i + 1][0] + (right[i + 1][0] - left[i + 1][0]) * t
        s.line([(xa, left[i][1]), (xb, left[i + 1][1])], C["stone_joint"], 0.6, 0.3)
    outline(s, base_poly, 0.9, 0.5)
    # the storeys, from the bottom up: wall, then roof over it
    for i, st in enumerate(KEEP):
        x0, x1 = st["w"]
        top, foot = st["top"], st["foot"]
        s.poly([(x0, foot), (x1, foot), (x1, top), (x0, top)], C["white_lit"])
        s.poly([(x0, foot), (x0 + 9, foot), (x0 + 8, top), (x0, top)], C["white_shade"], 0.6)                                  # the left end turning from the light
        s.poly([(x0, top), (x1, top), (x1, top + (foot - top) * 0.34), (x0, top + (foot - top) * 0.38)], C["white_shade"], 0.55)   # the eaves' shadow across the top of the wall
        s.poly([(x1 - 6, foot), (x1, foot), (x1, top), (x1 - 6, top)], C["white_warm"], 0.8)
        # window slots: dark, barred
        n = 4 - i // 2
        for j in range(n):
            wx = x0 + (x1 - x0) * (j + 1) / (n + 1)
            wh = min(9, (foot - top) * 0.36)
            s.poly([(wx - 4, foot - 6), (wx + 4, foot - 6), (wx + 4, foot - 6 - wh), (wx - 4, foot - 6 - wh)], C["roof_deep"])
            s.line([(wx - 4, foot - 6 - wh * 0.5), (wx + 4, foot - 6 - wh * 0.5)], C["white_shade"], 0.7, 0.8)
        # a dark band of boards under each wall's foot (the wall sits on the roof below)
        if i > 0:
            s.line([(x0, foot), (x1, foot)], C["wood_dark"], 1.2, 0.7)
        # the roof: the front slope (a trapezoid narrowing to the next wall), its eave lifted at the corners
        rx0, rx1, ey, uy = st["r"][0], st["r"][1], st["eave"], st["up"]
        if "ridge" in st:
            nx0, nx1 = st["ridge"]
        else:
            nx0, nx1 = KEEP[i + 1]["w"][0] - 2, KEEP[i + 1]["w"][1] + 2
        ev = eave(rx0, rx1, ey, lift=3.5 + i * 0.4)
        roof_poly = [(nx0, uy), (nx1, uy)] + ev[::-1]
        s.poly(roof_poly, C["roof"])
        s.poly([(nx0 + (nx1 - nx0) * 0.5, uy), (nx1, uy), (rx1, ev[-1][1]), (rx0 + (rx1 - rx0) * 0.55, ey)], C["roof_lit"], 0.45)   # the right half catches the low sun
        # the ridge and the hips: light lines; the ridge's end ornaments
        s.line([(nx0, uy), (nx1, uy)], C["roof_edge"], 1.6, 0.9)
        s.line([(nx0, uy), ev[0]], C["roof_edge"], 1.0, 0.6)
        s.line([(nx1, uy), ev[-1]], C["roof_edge"], 1.0, 0.6)
        s.line(ev, C["roof_edge"], 1.0, 0.7)
        # the white plastered underside of the eave: a pale band just under the eave line
        under_ = [(p[0], p[1] + 1) for p in ev]
        s.line(under_, C["white_shade"], 2.4, 0.9)
        s.line([(p[0], p[1] + 2.6) for p in ev], C["line"], 0.8, 0.5)
        # gables
        g = st.get("gable")
        if g == "chidori":
            cx = (rx0 + rx1) / 2 + (18 if i == 0 else -12)
            gw, gh = (26, 16) if i == 0 else (18, 11)
            gy = uy + (ey - uy) * 0.95
            s.poly([(cx - gw, gy), (cx + gw, gy), (cx, gy - gh)], C["white_lit"])
            s.poly([(cx - gw, gy), (cx - gw * 0.1, gy), (cx, gy - gh)], C["white_shade"], 0.5)
            s.line([(cx - gw, gy), (cx, gy - gh), (cx + gw, gy)], C["roof"], 1.8)
            s.poly([(cx - 3, gy - 1), (cx + 3, gy - 1), (cx + 3, gy - 6), (cx - 3, gy - 6)], C["roof_deep"])
        elif g == "kara":
            cx = (rx0 + rx1) / 2
            gy = uy + (ey - uy) * 0.95
            cur = curve([(cx - 20, gy), (cx - 12, gy - 1), (cx - 6, gy - 8), (cx, gy - 10), (cx + 6, gy - 8), (cx + 12, gy - 1), (cx + 20, gy)], 6)
            s.poly(cur + [(cx + 20, gy + 2), (cx - 20, gy + 2)], C["white_lit"])
            s.line(cur, C["roof"], 1.8)
        if "ridge" in st:                                     # the top ridge's two fish, as dabs
            for ex in (nx0 - 1, nx1 + 1):
                s.poly([(ex - 2, uy + 1), (ex + 2, uy + 1), (ex + 1.5, uy - 7), (ex - 1.5, uy - 7)], C["roof_deep"])
                s.ellipse(ex, uy - 8, 2.2, 1.6, C["roof_deep"])
        # the contour round the wall and the roof
        outline(s, [(x0, foot), (x1, foot), (x1, top), (x0, top)], 0.9, 0.55)
        outline(s, roof_poly, 0.9, 0.55)


# ---------------------------------------------------------------- the wall, the moat, the bank, the road, the ramp, the terrace
WALL_TOP, WALL_FOOT = 352, 398
MOAT = dict(x1=432, far=440, near=482)
ROAD_TOP = 540
TERRACE = dict(x0=445, x1=790, top=436, front=470)
RAMP = dict(foot=(432, 582, 540), top=(448, 606, 470))
GATE = dict(x0=575, x1=775, sill=436, open=(629, 729), lintel=310, pent=(282, 300), upper=(592, 758, 226, 282), roof=(568, 782, 226, 190, 628, 722))
GABLE = dict(apex=(675, 194), base=((650, 223), (700, 223)), tile=(675, 201), r=4.2)


def wall_poly():
    top = [(-10, WALL_TOP - 6), (200, WALL_TOP - 3), (420, WALL_TOP), (GATE["x0"] + 2, WALL_TOP)]
    return top + [(GATE["x0"] + 2, WALL_FOOT), (TERRACE["x0"], WALL_FOOT), (TERRACE["x0"], WALL_FOOT + 2), (-10, WALL_FOOT + 4)]


def wall(s):
    """The white wall from the gate to the left edge, on its stone revetment above the moat; the loopholes along
    it; the stretch by the gate newly whitened, the far stretch grey with the winter."""
    rng = np.random.default_rng(23)
    wp = wall_poly()
    s.poly(wp, C["white_lit"])
    s.poly([(-10, WALL_TOP - 6), (330, WALL_TOP - 1), (330, WALL_FOOT + 3), (-10, WALL_FOOT + 4)], mix(C["white_lit"], C["white_shade"], 0.35), 0.8)   # the old lime, grey
    s.poly([(455, WALL_TOP), (GATE["x0"] + 2, WALL_TOP), (GATE["x0"] + 2, WALL_FOOT), (455, WALL_FOOT)], C["lime"], 0.9)                      # the new coat by the scaffold
    for i in range(40):                                       # stains and the plasterers' half-done patches
        px, py = rng.uniform(0, 440), rng.uniform(WALL_TOP + 6, WALL_FOOT - 2)
        s.ellipse(px, py, rng.uniform(6, 18), rng.uniform(2, 5), mix(C["white_shade"], "#9a9690", 0.4), 0.25)
    # the tiled coping along the top: a dark band with a light top line, its own small eave
    cop = [(-10, WALL_TOP - 10), (200, WALL_TOP - 7), (420, WALL_TOP - 4), (GATE["x0"] + 6, WALL_TOP - 4), (GATE["x0"] + 6, WALL_TOP + 1), (420, WALL_TOP + 1), (200, WALL_TOP - 2), (-10, WALL_TOP - 5)]
    s.poly(cop, C["roof"])
    s.line([(-10, WALL_TOP - 10), (200, WALL_TOP - 7), (420, WALL_TOP - 4), (GATE["x0"] + 6, WALL_TOP - 4)], C["roof_edge"], 1.2, 0.8)
    s.line([(-10, WALL_TOP - 4), (200, WALL_TOP - 1), (420, WALL_TOP + 2), (GATE["x0"] + 6, WALL_TOP + 2)], C["white_shade"], 1.4, 0.8)
    # loopholes: round, square and triangular, at the height of a man's shoulder on the wall-walk inside
    for j, px in enumerate(range(30, 440, 46)):
        yy = WALL_TOP + 16 + (px / 440) * 1.5
        kind = j % 3
        if kind == 0:
            s.ellipse(px, yy, 2.6, 2.6, C["roof_deep"])
        elif kind == 1:
            s.poly([(px - 2.6, yy - 2.6), (px + 2.6, yy - 2.6), (px + 2.6, yy + 2.6), (px - 2.6, yy + 2.6)], C["roof_deep"])
        else:
            s.poly([(px - 3, yy + 2.6), (px + 3, yy + 2.6), (px, yy - 2.8)], C["roof_deep"])
    outline(s, wp[:4], 0.9, 0.5, close=False)
    s.line([(-10, WALL_FOOT + 4), (TERRACE["x0"], WALL_FOOT + 2)], C["line"], 0.9, 0.5)
    # the revetment under it, down to the water, in courses, its left part in the wall's shadow-colour
    rv = [(-10, WALL_FOOT + 4), (MOAT["x1"], WALL_FOOT + 2), (MOAT["x1"] + 12, MOAT["far"] + 2), (-10, MOAT["far"] + 4)]
    s.poly(rv, C["stone"])
    for k in range(5):
        yy = WALL_FOOT + 4 + k * 8.5
        s.line([(-10, yy), (MOAT["x1"] + 3 + k * 2, yy - 0.5)], C["stone_joint"], 0.7, 0.45)
    for j in range(70):
        px = rng.uniform(-5, MOAT["x1"])
        k = rng.integers(0, 5)
        s.line([(px, WALL_FOOT + 4 + k * 8.5), (px + rng.uniform(-1, 1), WALL_FOOT + 4 + (k + 1) * 8.5)], C["stone_joint"], 0.7, 0.4)
    s.poly([(MOAT["x1"] - 4, WALL_FOOT + 2), (MOAT["x1"] + 14, WALL_FOOT + 2), (TERRACE["x0"] + 6, MOAT["near"] + 2), (MOAT["x1"] + 2, MOAT["near"] + 2)], mix(C["stone_shade"], C["line"], 0.35))   # the terrace's stone side, into the water


def water(pic):
    """The inner moat: flat cobalt with rows of lighter lines, the white wall's reflection broken in it."""
    x, y = grid(SHAPE)
    rng = np.random.default_rng(24)
    near_bank = MOAT["near"] + 3 * np.sin(x / 70.0) - 2 * np.sin(x / 23.0 + 1)
    m = ((y > MOAT["far"]) & (y < near_bank) & (x < MOAT["x1"] + 8 + (y - MOAT["far"]) * 0.3)).astype(F32)
    t = np.clip((y - MOAT["far"]) / (MOAT["near"] - MOAT["far"]), 0, 1)
    tone = ramp(t, [(0.0, C["water_light"]), (0.25, C["water"]), (1.0, C["water_deep"])])
    over(pic, tone, m)
    s = Sheet(SHAPE)
    for k in range(9):                                        # the prints' water: rows of fine lines
        yy = MOAT["far"] + 5 + k * 4.6
        for seg in range(14):
            x0 = rng.uniform(-10, MOAT["x1"])
            s.line([(x0, yy + rng.uniform(-0.6, 0.6)), (x0 + rng.uniform(12, 40), yy + rng.uniform(-0.6, 0.6))], C["water_light"], 0.9, 0.45)
    for j in range(26):                                       # the wall's reflection, broken: pale dashes down from the far bank
        px = rng.uniform(0, MOAT["x1"] - 10)
        s.line([(px, MOAT["far"] + 1), (px + rng.uniform(-1, 1), MOAT["far"] + rng.uniform(6, 16))], mix(C["white_lit"], C["water"], 0.35), rng.uniform(1.0, 2.6), 0.55)
    for j in range(5):                                        # the cherry's pink in the water at the left
        px = rng.uniform(20, 170)
        s.line([(px, MOAT["far"] + 10), (px, MOAT["far"] + rng.uniform(16, 26))], mix(C["bloom"], C["water"], 0.5), 2.0, 0.4)
    s.onto(pic)
    return m


def ground(pic):
    """The near bank, the road, the ramp with its parapets, the terrace, the bank right of the ramp."""
    x, y = grid(SHAPE)
    rng = np.random.default_rng(25)
    s = Sheet(SHAPE)
    # the near bank: grass, warm toward the road, a trodden path along the water
    near_bank = [(-10, MOAT["near"] - 2)] + [(px, MOAT["near"] + 3 * math.sin(px / 70.0) - 2 * math.sin(px / 23.0 + 1)) for px in range(0, MOAT["x1"] + 20, 16)]
    bank = near_bank + [(TERRACE["x0"] + 6, MOAT["near"] + 2), (RAMP["top"][0], RAMP["top"][2]), (RAMP["foot"][0], ROAD_TOP), (-10, ROAD_TOP + 2)]
    s.poly(bank, C["bank"])
    s.poly([(p[0], p[1] + 10) for p in near_bank] + [(RAMP["foot"][0] - 10, ROAD_TOP - 12), (-10, ROAD_TOP - 10)], C["bank_lit"], 0.45)
    s.poly([(-10, ROAD_TOP - 14)] + [(px, ROAD_TOP - 16 + 3 * math.sin(px / 50.0)) for px in range(0, 440, 20)] + [(RAMP["foot"][0] - 6, ROAD_TOP), (-10, ROAD_TOP + 2)], C["path"], 0.7)   # the path
    s.line([(p[0], p[1] + 1) for p in near_bank], C["bank_shade"], 1.6, 0.7)                                                     # the water's edge
    # the bank right of the ramp, falling to the road
    rb = [(RAMP["top"][1], RAMP["top"][2]), (TERRACE["x1"] + 20, TERRACE["front"]), (810, TERRACE["front"] + 6), (810, ROAD_TOP + 2), (RAMP["foot"][1], ROAD_TOP)]
    s.poly(rb, C["bank"])
    s.poly([(RAMP["top"][1] + 10, RAMP["top"][2] + 8), (810, TERRACE["front"] + 14), (810, ROAD_TOP - 6), (RAMP["foot"][1] + 14, ROAD_TOP - 4)], C["bank_shade"], 0.35)
    for i in range(7):                                        # shrubs on the banks, flat dark tufts
        px, py = rng.uniform(600, 800), rng.uniform(TERRACE["front"] + 14, ROAD_TOP - 8)
        s.ellipse(px, py, rng.uniform(6, 12), rng.uniform(3, 6), C["bank_shade"], 0.8)
        s.ellipse(px + 3, py - 2, rng.uniform(3, 6), rng.uniform(2, 3), C["bank_lit"], 0.5)
    # the road: dusty ochre, warm in the light, its wheel-ruts and foot-worn middle
    s.poly([(-10, ROAD_TOP), (810, ROAD_TOP), (810, 610), (-10, 610)], C["road"])
    s.poly([(-10, ROAD_TOP + 22), (810, ROAD_TOP + 18), (810, 600), (-10, 600)], C["road_lit"], 0.5)
    s.poly([(-10, ROAD_TOP), (810, ROAD_TOP), (810, ROAD_TOP + 7), (-10, ROAD_TOP + 9)], C["road_shade"], 0.5)   # the bank's shadow-edge
    for k in range(3):
        yy = 556 + k * 14
        s.line([(-10, yy + rng.uniform(-2, 2)), (300, yy + rng.uniform(-2, 2)), (810, yy + rng.uniform(-2, 2))], C["road_shade"], 1.4, 0.25)
    # the ramp: stone paving, its courses closer together as it climbs; a low parapet each side
    f0, f1, fy = RAMP["foot"]
    t0, t1, ty = RAMP["top"]
    ramp_poly = [(f0, fy), (f1, fy), (t1, ty), (t0, ty)]
    s.poly(ramp_poly, C["stone_lit"])
    s.poly([(f0, fy), (f0 + (f1 - f0) * 0.35, fy), (t0 + (t1 - t0) * 0.35, ty), (t0, ty)], C["stone"], 0.45)
    yy = fy
    k = 0
    while yy > ty + 2:
        yy -= 9 * scale_at(yy) + 2
        xa = f0 + (t0 - f0) * (fy - yy) / (fy - ty)
        xb = f1 + (t1 - f1) * (fy - yy) / (fy - ty)
        s.line([(xa, yy), (xb, yy + rng.uniform(-0.6, 0.6))], C["stone_joint"], 0.8, 0.4)
        for j in range(3):
            tt = (j + 0.5 + 0.5 * (k % 2)) / 3.5
            s.line([(xa + (xb - xa) * tt, yy), (xa + (xb - xa) * tt + 0.5, yy + 9 * scale_at(yy) * 0.9)], C["stone_joint"], 0.7, 0.3)
        k += 1
    for side in (0, 1):                                       # the parapets: stone, with a tiled cap
        if side == 0:
            fx, tx = f0, t0
            poly = [(fx - 9, fy + 2), (fx + 1, fy), (tx + 1, ty), (tx - 6, ty + 1), (tx - 6, ty - 9), (fx - 9, fy - 15)]
        else:
            fx, tx = f1, t1
            poly = [(fx - 1, fy), (fx + 9, fy + 2), (fx + 9, fy - 15), (tx + 6, ty - 9), (tx + 6, ty + 1), (tx - 1, ty)]
        s.poly(poly, C["stone"] if side == 0 else C["stone_lit"])
        s.poly(poly[-2:] + poly[:1] if side == 0 else poly[2:4] + [poly[1]], C["stone_shade"], 0.0)
        cap = [(fx - 9, fy - 15), (tx - 6, ty - 9)] if side == 0 else [(fx + 9, fy - 15), (tx + 6, ty - 9)]
        s.line(cap, C["roof"], 2.4, 0.9)
        s.line([(cap[0][0], cap[0][1] - 1.2), (cap[1][0], cap[1][1] - 1.2)], C["roof_edge"], 1.0, 0.8)
        outline(s, poly, 0.9, 0.5)
    # the terrace: paved, pale, a stone edge along its front
    tp = [(TERRACE["x0"], TERRACE["top"]), (810, TERRACE["top"]), (810, TERRACE["front"] + 6), (TERRACE["x1"] + 20, TERRACE["front"]), (t1, ty), (t0, ty), (TERRACE["x0"], TERRACE["front"] - 2)]
    s.poly(tp, C["stone_lit"])
    s.poly([(TERRACE["x0"], TERRACE["top"]), (560, TERRACE["top"]), (560, TERRACE["front"] - 2), (TERRACE["x0"], TERRACE["front"] - 2)], C["stone"], 0.3)
    for j in range(4):
        yy = TERRACE["top"] + 7 + j * 8
        s.line([(TERRACE["x0"], yy), (810, yy + 0.5)], C["stone_joint"], 0.7, 0.35)
    for j in range(40):
        px = rng.uniform(TERRACE["x0"], 800)
        yy = TERRACE["top"] + 7 + rng.integers(0, 3) * 8
        s.line([(px, yy), (px, yy + 8)], C["stone_joint"], 0.7, 0.3)
    s.line([(TERRACE["x0"], TERRACE["front"] - 2), (t0, ty), (t1, ty), (TERRACE["x1"] + 20, TERRACE["front"]), (810, TERRACE["front"] + 6)], C["stone_joint"], 1.4, 0.7)
    s.line([(TERRACE["x0"], TERRACE["front"] - 1), (t0, ty + 1)], C["white_shade"], 1.0, 0.6)
    # the ramp's and the terrace's long shadows: the left parapet's across the ramp, the scaffold's and the gate's across the terrace
    s.onto(pic)
    sh = Sheet(SHAPE)
    sh.poly([(f0 + 1, fy), (f0 - 60, fy + 2), (t0 - 46, ty + 1), (t0 + 1, ty)], "#000000", 0.0)
    sh.onto(pic)
    shadow = Sheet(SHAPE)
    shadow.poly([(GATE["x0"], TERRACE["top"]), (GATE["x0"] - 150, TERRACE["top"] + 2), (GATE["x0"] - 120, TERRACE["front"] - 4), (GATE["x0"] + 20, TERRACE["front"] - 4), (GATE["x0"] + 30, TERRACE["top"])], C["cast"], 0.55)   # the gate's, across the terrace
    shadow.poly([(f1 - 2, fy - 1), (f1 - 48, fy - 1), (t1 - 30, ty), (t1 - 2, ty)], C["cast"], 0.9)                  # the right parapet's, across the ramp
    shadow.poly([(f0 - 8, fy + 2), (f0 - 52, fy + 4), (t0 - 32, ty + 2), (t0 - 6, ty)], C["cast"], 0.9)              # the left parapet's, on the bank
    shadow.poly([(74, 549), (30, 552), (-10, 540), (-10, 500), (40, 520), (72, 536)], C["cast"], 0.7)               # the cherry's trunk, off to the left
    c, a = shadow.done()
    tint(pic, C["cast"], blur(a, 1.2) * 0.55)
    return pic


def passage(s):
    """What shows through the gate's opening (in the backdrop): the dark passage, the door leaves standing open, and
    the lit court beyond: the way to the keep."""
    o0, o1 = GATE["open"]
    sill, lintel = GATE["sill"], GATE["lintel"]
    s.poly([(o0, sill), (o1, sill), (o1, lintel), (o0, lintel)], "#4a3f66")                      # the passage in shade
    s.poly([(o0 + 26, sill - 2), (o1 - 26, sill - 2), (o1 - 30, sill - 40), (o0 + 30, sill - 40)], "#c9b48c")   # the court's ground, lit, at the far end
    s.poly([(o0 + 26, sill - 40), (o1 - 26, sill - 40), (o1 - 26, lintel + 40), (o0 + 26, lintel + 40)], C["white_warm"])   # a white wall of the inner court in the sun
    s.poly([(o0 + 26, lintel + 40), (o1 - 26, lintel + 40), (o1 - 26, lintel + 30), (o0 + 26, lintel + 30)], C["roof"])      # its coping
    s.poly([(o0 + 26, lintel + 30), (o1 - 26, lintel + 30), (o1 - 26, lintel), (o0 + 26, lintel)], "#6a5e86")                 # the passage's far ceiling
    for side, (xa, xb) in enumerate(((o0, o0 + 24), (o1 - 24, o1))):                                 # the door leaves, standing open against the walls
        s.poly([(xa, sill), (xb, sill - 1), (xb, lintel + 2), (xa, lintel + 1)], C["wood_dark"])
        for k in range(5):
            yy = lintel + 12 + k * 26
            s.line([(xa, yy), (xb, yy)], "#2a2a30", 1.4, 0.8)
        for k in range(3):
            s.ellipse(xa + 6 + k * 6, sill - 20, 1.3, 1.3, "#2a2a30")
    s.poly([(o0 - 2, sill - 2), (o1 + 2, sill - 2), (o1 + 2, sill + 3), (o0 - 2, sill + 3)], C["stone_shade"])   # the threshold stone


# ---------------------------------------------------------------- the gate (a cut-out: its opening clear)
def gate(s):
    """The Ni-no-mon: a gate in a white wall under a small tiled tower; posts and lintel of dark wood; a pent roof
    across the front; above, the tower's white walls with two barred windows, its hipped roof with a gable toward
    us, and at the gable's apex the end tile with the cross."""
    x0, x1, sill = GATE["x0"], GATE["x1"], GATE["sill"]
    o0, o1 = GATE["open"]
    lintel = GATE["lintel"]
    p0, p1 = GATE["pent"]
    # the lower storey's white wall either side of the opening (the opening itself is left clear)
    for (xa, xb) in ((x0, o0 - 8), (o1 + 8, x1)):
        s.poly([(xa, sill), (xb, sill), (xb, p1), (xa, p1)], C["white_lit"])
    s.poly([(x0, sill), (x0 + 16, sill), (x0 + 16, p1), (x0, p1)], C["white_shade"], 0.45)
    s.poly([(x1 - 10, sill), (x1, sill), (x1, p1), (x1 - 10, p1)], C["white_warm"], 0.8)
    for (xa, xb) in ((x0, o0 - 8), (o1 + 8, x1)):            # the plinth of dark boards at the foot
        s.poly([(xa, sill), (xb, sill), (xb, sill - 14), (xa, sill - 14)], C["wood"])
        s.line([(xa, sill - 14), (xb, sill - 14)], C["wood_lit"], 1.0, 0.7)
    # the posts and the lintel round the opening
    for (xa, xb) in ((o0 - 8, o0), (o1, o1 + 8)):
        s.poly([(xa, sill), (xb, sill), (xb, lintel - 10), (xa, lintel - 10)], C["wood"])
        s.line([(xa + 1.5, sill), (xa + 1.5, lintel - 10)], C["wood_lit"], 1.2, 0.6)
    s.poly([(o0 - 14, lintel), (o1 + 14, lintel), (o1 + 14, lintel - 14), (o0 - 14, lintel - 14)], C["wood"])
    s.line([(o0 - 14, lintel - 14), (o1 + 14, lintel - 14)], C["wood_lit"], 1.2, 0.7)
    for k in range(6):                                       # iron studs along the lintel
        s.ellipse(o0 + 6 + k * (o1 - o0 - 12) / 5, lintel - 7, 1.6, 1.6, "#2a2a30")
    # the pent roof across the front, tile, its underside white
    ev = eave(x0 - 10, x1 + 10, p1, lift=2.5)
    s.poly([(x0 - 2, p0), (x1 + 2, p0)] + ev[::-1], C["roof"])
    s.poly([(x0 + (x1 - x0) * 0.5, p0), (x1 + 2, p0), (x1 + 10, p1), (x0 + (x1 - x0) * 0.55, p1)], C["roof_lit"], 0.4)
    s.line(ev, C["roof_edge"], 1.0, 0.7)
    s.line([(p[0], p[1] + 1.2) for p in ev], C["white_shade"], 2.4, 0.9)
    s.line([(x0 - 2, p0), (x1 + 2, p0)], C["roof_edge"], 1.4, 0.8)
    # the tower: white walls, set back a little, two windows with bars
    ux0, ux1, ut, uf = GATE["upper"]
    s.poly([(ux0, uf), (ux1, uf), (ux1, ut), (ux0, ut)], C["white_lit"])
    s.poly([(ux0, uf), (ux0 + 22, uf), (ux0 + 20, ut), (ux0, ut)], C["white_shade"], 0.45)
    s.poly([(ux1 - 8, uf), (ux1, uf), (ux1, ut), (ux1 - 8, ut)], C["white_warm"], 0.8)
    s.line([(ux0, uf), (ux1, uf)], C["wood_dark"], 1.4, 0.7)
    for wx in (628, 722):
        s.poly([(wx - 13, uf - 14), (wx + 13, uf - 14), (wx + 13, uf - 42), (wx - 13, uf - 42)], C["roof_deep"])
        for k in range(4):
            s.line([(wx - 10 + k * 6.5, uf - 14), (wx - 10 + k * 6.5, uf - 42)], C["white_shade"], 1.2, 0.8)
        s.line([(wx - 13, uf - 28), (wx + 13, uf - 28)], C["white_shade"], 1.0, 0.7)
    # the tower's roof: hipped, the ridge short; the gable toward us; the fish at the ridge ends
    rx0, rx1, ey, ry, nx0, nx1 = GATE["roof"]
    ev = eave(rx0, rx1, ey, lift=3.5)
    roof_poly = [(nx0, ry), (nx1, ry)] + ev[::-1]
    s.poly(roof_poly, C["roof"])
    s.poly([(nx0 + (nx1 - nx0) * 0.5, ry), (nx1, ry), (rx1, ev[-1][1]), (rx0 + (rx1 - rx0) * 0.55, ey)], C["roof_lit"], 0.4)
    s.line([(nx0, ry), (nx1, ry)], C["roof_edge"], 1.8, 0.9)
    s.line([(nx0, ry), ev[0]], C["roof_edge"], 1.0, 0.6)
    s.line([(nx1, ry), ev[-1]], C["roof_edge"], 1.0, 0.6)
    s.line(ev, C["roof_edge"], 1.0, 0.7)
    s.line([(p[0], p[1] + 1.2) for p in ev], C["white_shade"], 2.6, 0.9)
    for ex in (nx0 - 1, nx1 + 1):
        s.poly([(ex - 2.2, ry + 1), (ex + 2.2, ry + 1), (ex + 1.6, ry - 8), (ex - 1.6, ry - 8)], C["roof_deep"])
        s.ellipse(ex, ry - 9, 2.4, 1.8, C["roof_deep"])
    # the gable (chidori-hafu) on the front slope: white face, dark bargeboards, the end tile at its apex
    ax, ay = GABLE["apex"]
    (b0x, b0y), (b1x, b1y) = GABLE["base"]
    s.poly([(b0x, b0y), (b1x, b1y), (ax, ay)], C["white_lit"])
    s.poly([(b0x, b0y), (ax - 2, b0y), (ax, ay)], C["white_shade"], 0.4)
    s.line([(b0x - 2, b0y + 1), (ax, ay - 1), (b1x + 2, b1y + 1)], C["roof"], 2.4)
    s.line([(b0x - 2, b0y + 1), (ax, ay - 1), (b1x + 2, b1y + 1)], C["roof_edge"], 0.8, 0.7)
    tx, ty = GABLE["tile"]
    r = GABLE["r"]
    s.ellipse(tx, ty, r + 1.0, r + 1.0, C["roof_deep"])      # the round end tile (gegyo): its rim
    s.ellipse(tx, ty, r, r, "#6f7890")                      # its face
    s.line([(tx, ty - r * 0.72), (tx, ty + r * 0.72)], "#dfe4ec", 1.0)   # the cross on it: two strokes, a shade lighter than the clay
    s.line([(tx - r * 0.55, ty - r * 0.15), (tx + r * 0.55, ty - r * 0.15)], "#dfe4ec", 1.0)
    # the contour
    outline(s, [(x0, sill), (o0 - 8, sill), (o0 - 8, lintel - 14), (o1 + 8, lintel - 14), (o1 + 8, sill), (x1, sill), (x1, p1), (x0, p1)], 0.9, 0.55)
    outline(s, [(ux0, uf), (ux1, uf), (ux1, ut), (ux0, ut)], 0.9, 0.55)
    outline(s, roof_poly, 0.9, 0.55)


def gate_clear(s):
    """The opening, wiped clear of the gate's sheet (people walk into it; the backdrop's passage shows)."""
    o0, o1 = GATE["open"]
    s.clear([(o0, GATE["sill"] + 4), (o1, GATE["sill"] + 4), (o1, GATE["lintel"]), (o0, GATE["lintel"])])


# ---------------------------------------------------------------- the plasterers' things
SCAF = dict(x=(462, 510, 558), foot=450, back=437, top=354, lifts=(412, 380))
LADDER = dict(foot=((594, 464), (612, 464)), top=((603, 318), (619, 318)), rungs=11)
TUB = dict(at=(520, 466), w=42, h=13)
BUCKETS = [dict(at=(500, 494), w=18, h=18), dict(at=(527, 503), w=19, h=19), dict(at=(553, 490), w=17, h=17)]


def bamboo(s, a, b, w, rng):
    """A bamboo pole: one flat with its lit edge toward the sun, the nodes as short dark lines, the contour along it."""
    s.line([a, b], C["bamboo"], w)
    s.line([(a[0] + w * 0.28, a[1]), (b[0] + w * 0.28, b[1])], C["bamboo_lit"], w * 0.34, 0.9)
    n = int(math.hypot(b[0] - a[0], b[1] - a[1]) / 14)
    for k in range(1, n):
        t = k / n
        px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        s.line([(px - w * 0.6, py), (px + w * 0.6, py)], C["bamboo_dark"], 1.0, 0.85)
    s.line([(a[0] - w * 0.5, a[1]), (b[0] - w * 0.5, b[1])], C["line"], 0.8, 0.7)   # the keyblock's line along the pole
    s.line([(a[0] + w * 0.5, a[1]), (b[0] + w * 0.5, b[1])], C["line"], 0.6, 0.45)


def scaffold(s):
    """The bamboo scaffold against the wall by the gate: three bays, two lifts of planks, lashed; a brace; a bucket
    hung on it. Its front poles stand on the terrace (base row 450), its back poles at the wall's foot."""
    rng = np.random.default_rng(26)
    xs, foot, back, top = SCAF["x"], SCAF["foot"], SCAF["back"], SCAF["top"]
    for px in xs:                                              # the back poles
        bamboo(s, (px + 5, back), (px + 4, top + 2), 2.8, rng)
    for yy in (foot - 6,) + SCAF["lifts"] + (top + 4,):        # the back ledgers
        s.line([(xs[0] + 3, yy - 1), (xs[-1] + 7, yy - 1)], C["bamboo_dark"], 2.2)
    for yy in SCAF["lifts"]:                                   # the planks on each lift, and the putlogs under them
        for px in xs:
            s.line([(px - 1, yy + 2), (px + 6, yy - 10)], C["bamboo_dark"], 2.2)
        s.poly([(xs[0] - 6, yy + 1), (xs[-1] + 8, yy), (xs[-1] + 10, yy - 7), (xs[0] - 4, yy - 6)], C["wood_lit"])
        s.line([(xs[0] - 6, yy + 1), (xs[-1] + 8, yy)], C["line"], 0.9, 0.7)
        s.line([(xs[0] - 4, yy - 6), (xs[-1] + 10, yy - 7)], mix(C["wood_lit"], C["lime"], 0.5), 1.0, 0.8)
        s.line([(xs[0] - 4, yy - 7), (xs[-1] + 10, yy - 8)], C["line"], 0.7, 0.5)
    for yy in (foot - 8,) + tuple(l - 8 for l in SCAF["lifts"]) + (top + 2,):   # the front ledgers
        bamboo(s, (xs[0] - 8, yy), (xs[-1] + 10, yy - 1), 2.6, rng)
    for px in xs:                                              # the front poles
        bamboo(s, (px, foot), (px - 1, top - 2), 3.4, rng)
    bamboo(s, (xs[0] - 4, foot - 10), (xs[-1] + 4, top + 6), 2.2, rng)   # the brace
    for px in xs:                                              # the lashings: rope crosses at the joints, two strands, lined
        for yy in (foot - 8,) + tuple(l - 8 for l in SCAF["lifts"]) + (top + 2,):
            for (dx, dy) in ((0, 0), (1.2, 0.8)):
                s.line([(px - 4 + dx, yy - 4 + dy), (px + 4 + dx, yy + 4 + dy)], C["rope"], 1.5)
                s.line([(px - 4 + dx, yy + 4 + dy), (px + 4 + dx, yy - 4 + dy)], C["rope"], 1.5)
            s.line([(px - 5, yy - 5), (px + 5, yy + 5)], C["line"], 0.6, 0.55)
            s.line([(px - 5, yy + 5), (px + 5, yy - 5)], C["line"], 0.6, 0.55)
    # a bucket hung from the top ledger by its rope; lime dripped down a pole
    s.line([(xs[1] + 20, top + 2), (xs[1] + 20, top + 14)], C["rope"], 1.0)
    s.poly([(xs[1] + 14, top + 14), (xs[1] + 26, top + 14), (xs[1] + 25, top + 26), (xs[1] + 15, top + 26)], C["wood"])
    s.line([(xs[1] + 14, top + 15), (xs[1] + 26, top + 15)], C["lime"], 1.6)
    s.line([(xs[2] - 1, SCAF["lifts"][0] + 2), (xs[2] - 1, SCAF["lifts"][0] + 18)], C["lime"], 1.4, 0.8)



def ladder(s):
    """Tomezo's ladder against the gate's outer wall, left of the opening: two rails, eleven rungs."""
    (f0, f1), (t0, t1) = LADDER["foot"], LADDER["top"]
    n = LADDER["rungs"]
    for k in range(n):
        t = (k + 0.5) / n
        a = (f0[0] + (t0[0] - f0[0]) * t, f0[1] + (t0[1] - f0[1]) * t)
        b = (f1[0] + (t1[0] - f1[0]) * t, f1[1] + (t1[1] - f1[1]) * t)
        s.line([a, b], C["wood"], 2.6)
        s.line([(a[0], a[1] - 0.8), (b[0], b[1] - 0.8)], C["wood_lit"], 1.0, 0.8)
    for a, b in ((f0, t0), (f1, t1)):
        s.line([a, b], C["wood"], 3.4)
        s.line([(a[0] - 0.8, a[1]), (b[0] - 0.8, b[1])], C["wood_dark"], 1.0, 0.8)
        s.line([(a[0] + 0.9, a[1]), (b[0] + 0.9, b[1])], C["wood_lit"], 1.0, 0.8)
    for a, b in ((f0, t0), (f1, t1)):
        s.line([(a[0], a[1] + 1), (b[0], b[1])], C["line"], 0.8, 0.45)
    s.line([(f0[0] - 4, f0[1] + 1), (f1[0] + 4, f1[1] + 1)], C["lime"], 1.2, 0.6)   # lime on the terrace at its foot


def tub(s):
    """The mixing tub: a wide, low wooden tub, hooped, lime in it."""
    x, y = TUB["at"]
    w, h = TUB["w"], TUB["h"]
    s.poly([(x - w / 2, y), (x + w / 2, y), (x + w / 2 - 2, y - h), (x - w / 2 + 2, y - h)], C["wood"])
    s.poly([(x - w / 2, y), (x - w / 2 + 10, y), (x - w / 2 + 11, y - h), (x - w / 2 + 2, y - h)], C["wood_dark"], 0.5)
    s.poly([(x + w / 2 - 8, y), (x + w / 2, y), (x + w / 2 - 2, y - h), (x + w / 2 - 9, y - h)], C["wood_lit"], 0.6)
    for yy in (y - 3, y - h + 4):
        s.line([(x - w / 2 + 1, yy), (x + w / 2 - 1, yy)], "#2a2a30", 1.0, 0.8)
    s.ellipse(x, y - h, w / 2 - 1, 3.6, C["wood_lit"])
    s.ellipse(x, y - h + 0.5, w / 2 - 4, 2.4, C["lime"])
    s.ellipse(x - 4, y - h + 0.8, w / 2 - 10, 1.4, C["lime_shade"], 0.5)
    s.line([(x - 6, y - h - 12), (x + 2, y - h + 1)], C["wood_lit"], 1.6)        # the paddle in it
    outline(s, [(x - w / 2, y + 1), (x + w / 2, y + 1), (x + w / 2 - 2, y - h - 2), (x - w / 2 + 2, y - h - 2)], 0.8, 0.45)


def bucket(s, b):
    """A wooden pail of lime, a rope handle."""
    x, y = b["at"]
    w, h = b["w"], b["h"]
    s.poly([(x - w / 2 + 1, y), (x + w / 2 - 1, y), (x + w / 2, y - h), (x - w / 2, y - h)], C["wood"])
    s.poly([(x - w / 2 + 1, y), (x - w / 2 + 5, y), (x - w / 2 + 4, y - h), (x - w / 2, y - h)], C["wood_dark"], 0.5)
    s.poly([(x + w / 2 - 4, y), (x + w / 2 - 1, y), (x + w / 2, y - h), (x + w / 2 - 3, y - h)], C["wood_lit"], 0.6)
    s.line([(x - w / 2 + 1, y - 3), (x + w / 2 - 1, y - 3)], "#2a2a30", 0.9, 0.8)
    s.line([(x - w / 2 + 0.5, y - h + 3), (x + w / 2 - 0.5, y - h + 3)], "#2a2a30", 0.9, 0.8)
    s.ellipse(x, y - h, w / 2, 2.4, C["wood_lit"])
    s.ellipse(x, y - h + 0.3, w / 2 - 2.5, 1.5, C["lime"])
    s.line(curve([(x - w / 2 + 1, y - h), (x, y - h - w * 0.55), (x + w / 2 - 1, y - h)], 6), C["rope"], 1.2)
    s.line([(x - w / 2 + 1, y + 0.8), (x + w / 2 - 1, y + 0.8)], C["line"], 0.9, 0.5)


# ---------------------------------------------------------------- the double cherry
LIMBS = [  # each a curve of (x, y) from the fork outward, with its width at the start and at the end
    ([(92, 440), (70, 380), (44, 300), (20, 220), (6, 160)], 14, 4),
    ([(92, 440), (104, 380), (118, 310), (124, 240), (118, 170), (100, 110)], 15, 4),
    ([(96, 445), (150, 400), (210, 372), (246, 340), (262, 300), (258, 240)], 13, 3.5),
    ([(150, 400), (190, 410), (232, 426), (262, 440)], 6, 2),              # the low bough over the bank
    ([(118, 310), (170, 290), (212, 276), (240, 256)], 6, 2),
    ([(44, 300), (60, 262), (90, 230), (126, 212)], 6, 2),
    ([(246, 340), (224, 326), (198, 330)], 4, 2),
]
MASSES = [  # the big flats of blossom: centre, half-widths (the crown fills the top-left, clear of the keep from x 292)
    (56, 232, 56, 50), (82, 146, 62, 48), (150, 96, 70, 42), (214, 136, 54, 42), (222, 220, 48, 46), (146, 190, 56, 46),
    (110, 300, 46, 38), (190, 300, 48, 38), (234, 296, 32, 30), (158, 372, 48, 32), (224, 394, 42, 28), (198, 430, 30, 16),
    (30, 322, 32, 34), (190, 36, 46, 22), (60, 70, 40, 26),
]


def scallop(cx, cy, rx, ry, rng, lobes=9, bump=0.14, n=54):
    """A blossom mass's outline: an oval whose edge is broken into small round lobes."""
    ph = rng.uniform(0, 6.3)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 1 + bump * (0.5 + 0.5 * math.cos(a * lobes + ph)) + rng.uniform(-0.02, 0.02)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return pts


def limbs(s, width=1.0, alpha=1.0):
    for pts, w0, w1 in LIMBS:
        cv = curve(pts, 8)
        n = len(cv)
        for i in range(n - 1):
            w = (w0 + (w1 - w0) * i / (n - 1)) * width
            s.line([cv[i], cv[i + 1]], C["trunk"], w, alpha)
            if width >= 1.0:
                s.line([(cv[i][0] + w * 0.22, cv[i][1]), (cv[i + 1][0] + w * 0.22, cv[i + 1][1])], C["trunk_lit"], w * 0.35, 0.7 * alpha)


def cherry(s):
    """The one old double cherry: a leaning trunk, three great limbs and the lesser ones, and the blossom as the prints
    cut it: a few big flat masses (geranium lake with lead white: one shade flat, one lit flat toward the low sun), their
    edges broken into small lobes and dabs, gaps of sky through them, the dark branches drawn into and through them."""
    rng = np.random.default_rng(27)
    shade_, lit_ = mix(PAPER, "#c9375e", 0.46), mix(PAPER, "#c9375e", 0.24)
    trunk = [(74, 548), (104, 546), (106, 500), (108, 460), (100, 440), (84, 440), (78, 480), (72, 520)]
    s.poly(trunk, C["trunk"])
    s.poly([(96, 546), (104, 546), (106, 500), (108, 460), (100, 440), (94, 446), (98, 500)], C["trunk_lit"], 0.7)
    s.poly([(74, 548), (82, 548), (84, 500), (86, 446), (84, 440), (78, 480), (72, 520)], "#2a1e22", 0.5)
    for k in range(9):
        s.line([(78 + k * 3 + rng.uniform(-1, 1), 546), (84 + k * 2.6 + rng.uniform(-2, 2), 446)], "#2a1e22", 0.8, 0.35)
    s.ellipse(89, 548, 26, 4, "#3a3034", 0.5)
    limbs(s)
    # the masses: the shade flat, then the lit flat set toward the sun (up and to the right), each scalloped
    for (cx, cy, rx, ry) in MASSES:
        s.poly(scallop(cx, cy, rx, ry, rng), shade_)
    for (cx, cy, rx, ry) in MASSES:
        s.poly(scallop(cx + rx * 0.24, cy - ry * 0.26, rx * 0.70, ry * 0.66, rng, lobes=7), lit_)
    # gaps of sky through the crown
    for (cx, cy, rx, ry) in MASSES:
        for j in range(rng.integers(1, 4)):
            hx, hy = cx + rng.uniform(-0.6, 0.6) * rx, cy + rng.uniform(-0.6, 0.6) * ry
            hr = rng.uniform(3.5, 7.5)
            s.clear(scallop(hx, hy, hr, hr * 0.8, rng, lobes=5, bump=0.2, n=18))
    # the edges broken further into dabs, shade outside, lit on the sun's side
    for (cx, cy, rx, ry) in MASSES:
        for j in range(14):
            a = rng.uniform(0, 2 * math.pi)
            px, py = cx + (rx + 2) * math.cos(a), cy + (ry + 2) * math.sin(a)
            tone = lit_ if (math.cos(a) > 0.2 and math.sin(a) < 0.1) else shade_
            s.ellipse(px, py, rng.uniform(2.5, 4.5), rng.uniform(2, 3.5), tone)
    # the branches through the blossom: the limbs again, thinner, and twigs reaching into the masses
    limbs(s, 0.55, 0.9)
    for (cx, cy, rx, ry) in MASSES:
        for j in range(3):
            a = rng.uniform(-2.6, -0.4)
            x0, y0 = cx + rng.uniform(-0.4, 0.4) * rx, cy + rng.uniform(0.2, 0.9) * ry
            mid = (x0 + math.cos(a) * rx * 0.3, y0 + math.sin(a) * ry * 0.3 + rng.uniform(-3, 3))
            s.line([(x0, y0), mid, (x0 + math.cos(a) * rx * 0.6, y0 + math.sin(a) * ry * 0.6)], C["trunk"], 1.0, 0.85)
    # a few deeper flecks in the shade and lit dabs over the branches' ends (the blossom in front of the twigs)
    for j in range(120):
        (cx, cy, rx, ry) = MASSES[rng.integers(len(MASSES))]
        px, py = cx + rng.uniform(-0.8, 0.8) * rx, cy + rng.uniform(-0.8, 0.8) * ry
        s.ellipse(px, py, rng.uniform(1.6, 3.0), rng.uniform(1.3, 2.4), lit_ if rng.random() < 0.6 else mix(shade_, "#c9375e", 0.25), 0.9)


def cherry_contour(s):
    """The keyblock's line round the trunk and the limbs (the blossom is left soft-edged, as the prints leave it)."""
    trunk = [(74, 548), (104, 546), (106, 500), (108, 460), (100, 440), (84, 440), (78, 480), (72, 520)]
    s.line(trunk + [trunk[0]], "#8c3b20", 1.0, 0.6)                     # the warm line on a warm dark thing (style.md section 4)
    for pts, w0, w1 in LIMBS[:3]:
        cv = curve(pts, 8)
        s.line([(p[0] - w0 * 0.5 * (1 - i / len(cv)) - 0.5, p[1]) for i, p in enumerate(cv)], "#8c3b20", 0.9, 0.5)


# ---------------------------------------------------------------- the passes
def under(seed=20):
    pic = sky_layer(seed)
    s = Sheet(SHAPE)
    hills(s)
    s.onto(pic)
    keep_l = sheet_layer(keep, 0.5)
    keep_l.onto(pic)
    wall_l = sheet_layer(wall, 0.5)
    wall_l.onto(pic)
    wm = water(pic)
    ground(pic)
    s = Sheet(SHAPE)
    passage(s)
    s.onto(pic)
    # the evening air: the far things paler and bluer; a warm film low on the right
    x, y = grid(SHAPE)
    haze = np.clip((HZ + 80 - y) / 300.0, 0, 1) ** 1.5 * (y < WALL_TOP)
    over(pic, "#c9d3e4", (haze * 0.22).astype(F32))
    glow(pic, "#f4d9a8", (np.clip((x - 400) / 500.0, 0, 1) * np.clip(1 - np.abs(y - 330) / 220.0, 0, 1) * 0.10).astype(F32))
    return np.clip(pic, 0, 1), dict(keep=keep_l, wall=wall_l, water=wm)


def details(pic, info, seed=20):
    """Over the brushwork: the keep and the wall said again crisply, the contour, the small things."""
    rng = np.random.default_rng(seed + 5)
    crisp = pic.copy()
    info["keep"].onto(crisp)
    info["wall"].onto(crisp)
    pic[...] = lerp(pic, crisp, 0.82)
    s = Sheet(SHAPE)
    passage(s)
    s.onto(pic, 0.85)
    s = Sheet(SHAPE)
    # the contour on the ground's forms
    f0, f1, fy = RAMP["foot"]
    t0, t1, ty = RAMP["top"]
    s.line([(-10, ROAD_TOP + 2), (f0, ROAD_TOP)], C["line"], 0.9, 0.45)
    s.line([(f1, ROAD_TOP), (810, ROAD_TOP + 2)], C["line"], 0.9, 0.45)
    near_bank = [(px, MOAT["near"] + 3 * math.sin(px / 70.0) - 2 * math.sin(px / 23.0 + 1)) for px in range(0, MOAT["x1"] + 20, 16)]
    s.line(near_bank, C["line"], 0.9, 0.45)
    s.line([(-10, MOAT["far"] + 4), (MOAT["x1"] + 12, MOAT["far"] + 2)], C["line"], 0.8, 0.4)
    # grass tufts along the bank and the road's edge; stones on the road; lime spatters on the terrace by the scaffold
    for i in range(70):
        px = rng.uniform(0, 440)
        py = rng.uniform(MOAT["near"] + 4, ROAD_TOP - 2)
        h = rng.uniform(3, 7) * scale_at(py)
        for k in range(3):
            s.line([(px + k * 1.5, py), (px + k * 1.5 + rng.uniform(-2, 2), py - h * rng.uniform(0.6, 1.1))], C["bank_shade"] if k < 2 else C["bank_lit"], 0.9)
    for i in range(50):
        px, py = rng.uniform(0, 800), rng.uniform(ROAD_TOP + 4, 598)
        r = rng.uniform(0.8, 2.2) * scale_at(py)
        s.ellipse(px, py, r * 1.4, r * 0.8, [C["road_shade"], C["road_dark"], C["road_lit"]][int(rng.integers(3))], 0.8)
    for i in range(90):
        px, py = rng.normal(505, 50), rng.normal(458, 10)
        if TERRACE["x0"] + 2 < px < 600 and TERRACE["top"] + 2 < py < TERRACE["front"] - 2:
            s.ellipse(px, py, rng.uniform(1, 3), rng.uniform(0.6, 1.4), C["lime"], 0.85)
    for i in range(30):                                       # and up the wall's foot
        px, py = rng.uniform(455, 575), WALL_FOOT - rng.uniform(0, 10) ** 1.3 * 0.6
        s.ellipse(px, py, rng.uniform(0.8, 2), rng.uniform(0.6, 1.6), C["lime"], 0.9)
    # petals already fallen: a drift of pink on the bank and the road under the tree
    for i in range(160):
        px, py = rng.normal(150, 70), rng.normal(530, 26)
        if 0 < px < 420 and MOAT["near"] + 6 < py < 598:
            s.ellipse(px, py, 1.3, 0.9, C["bloom"] if rng.random() < 0.7 else C["bloom_lit"], 0.85)
    s.onto(pic)
    return pic


def brushed(layer, ground_, seed, sizes=(6, 3, 2), keep=0.45, restate=0.7):
    """A cut-out, repainted with a small brush on the ground it stands against, then said again crisply.
    -> (colour, hard coverage)."""
    c, a = layer.straight()
    ys, xs = np.where(a > 0.02)
    if len(xs) == 0:
        return c, a
    x0, x1, y0, y1 = max(0, xs.min() - 12), min(W, xs.max() + 13), max(0, ys.min() - 12), min(H, ys.max() + 13)
    flat = ground_[y0:y1, x0:x1].copy()
    over(flat, c[y0:y1, x0:x1], a[y0:y1, x0:x1])
    painted = strokes(flat, sizes=sizes, seed=seed, density=1.8, jitter=0.025, keep=keep)
    painted = lerp(painted, flat, (restate * a[y0:y1, x0:x1])[..., None])
    out = c.copy()
    out[y0:y1, x0:x1] = painted
    return out, (a > 0.5).astype(F32)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.012, amount=0.016, palette=None):
    """A little grain, then a limited palette with speckle, written as a PNG-8. -> (file size, palette)"""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette if palette is not None else palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name), pal


CUTS = ["ladder", "gate", "scaffold", "tub", "bucket-1", "bucket-2", "bucket-3", "cherry"]     # back to front, as the scene lists them


def cut_layers():
    def gate_all(s):
        gate(s)
        gate_clear(s)

    def cherry_all(s):
        cherry(s)
        cherry_contour(s)
    layers = {
        "ladder": sheet_layer(ladder, 0.3),
        "gate": sheet_layer(gate_all, 0.4),
        "scaffold": sheet_layer(scaffold, 0.3),
        "tub": sheet_layer(tub, 0.2),
        "cherry": sheet_layer(cherry_all, 0.6),
    }
    for i, b in enumerate(BUCKETS):
        layers[f"bucket-{i + 1}"] = sheet_layer(lambda s, b=b: bucket(s, b), 0.2)
    # the gate's opening must be clear of everything (the hand's push could leave a sliver): wipe it hard
    o0, o1 = GATE["open"]
    g = layers["gate"]
    m = mask_poly(SHAPE, [(o0 + 1, GATE["sill"] + 6), (o1 - 1, GATE["sill"] + 6), (o1 - 1, GATE["lintel"] + 1), (o0 + 1, GATE["lintel"] + 1)])
    g.a *= (1 - m)
    g.c *= (1 - m)[..., None]
    return layers


if __name__ == "__main__":                                   # DEPTH-23: round twenty-three's painting (edo_castle_depth.py)
    import edo_castle_depth
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    edo_castle_depth.main(sys.argv[1:])

"""PAINT-20C: the cedar path in the hills north of Osaka, dusk, spring rain (edo-cedars). See edo_cedars_kit.py for
the place, the light and every measurement.

In the manner of the woodblock landscape prints and the act's style sheet (S/work-20-paintA/style.md): big flat
masses with strong silhouettes (a thing is two flats, lit and shade, with a hard edge between), a graded sky laid in
bands, one fine even contour (prussian blue; burnt sienna on the near trunks), few colours with the blue leading,
distance in three planes (near trunks dark and warm with the contour and drawn bark lines; middle trunks paler and
bluer with a thinner line; far trunks lost in the mist with no line), the cedars' crowns closing the top as dark
foliage masses with the banded sky between them. Nothing copied from any print. Rain, drips, the puddles' rings and
the mist are moving things (layout.json "fx"): the painting holds only the wet.

    python3 edo_cedars.py          paints out/edo-cedars/ (back, front, cedar-l, cedar-r, light-on, window-lit,
                                   layout.json) and out/edo-cedars-comp.png
    python3 edo_cedars.py fast     skips the brush pass and the palette: out/edo-cedars-work/ only"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
from edo_cedars_kit import *
import edo_cedars_layout as LAY
from postimp_paints import PAINTS

OUT = "out/edo-cedars"
WORK = "out/edo-cedars-work"


def paint(name):
    return rgb(PAINTS[name]["hex"])


PRUSSIAN, COBALT, ULTRA, CERULEAN = paint("prussian-blue"), paint("cobalt-blue"), paint("ultramarine"), paint("cerulean")
WHITE, OCHRE, SIENNA, VIRIDIAN, VERONESE, NAPLES, VERMILION = (paint("lead-white"), paint("yellow-ochre"), paint("burnt-sienna"),
                                                              paint("viridian"), paint("veronese-green"), paint("naples-yellow"), paint("vermilion"))
PAPER = lerp(lerp(WHITE, CERULEAN, 0.30), PRUSSIAN, 0.10)      # the horizon paper of a rainy dusk: lead white, a little cerulean, a breath of prussian
SKY_HZ = 300                                                   # the sky's bands run down to the far slope's top
LINE = PRUSSIAN


def shade_of(c, t=0.35):
    """The shade flat of a lit flat: pulled toward the key's shade (cobalt into prussian), never darkened grey."""
    return lerp(c, lerp(COBALT, PRUSSIAN, 0.6), t)


def far_of(c, t):
    """A colour pulled toward the horizon paper and toward blue, for the middle and far planes."""
    return lerp(lerp(c, PAPER, t), CERULEAN, t * 0.25)


# ================================================================ under: the flats
def sky_layer(seed=11):
    """The last of the light: a graded wash from cobalt-prussian overhead to the paper at the far slope, quantised into
    seven level bands, each a flat, the boundaries soft and a little wobbled (the prints' bokashi)."""
    x, y = PX, PY
    grey = lerp(PAPER, PRUSSIAN, 0.35)                           # the rain's grey: the paper with prussian in it
    stops = [lerp(lerp(COBALT, PRUSSIAN, 0.6), grey, 0.3), lerp(lerp(COBALT, PRUSSIAN, 0.35), grey, 0.4), lerp(COBALT, grey, 0.5),
             lerp(CERULEAN, grey, 0.5), lerp(CERULEAN, PAPER, 0.5), lerp(CERULEAN, PAPER, 0.8), PAPER]
    n = len(stops)
    pic = np.empty(SHAPE + (3,), F32)
    pic[...] = vary(stops[0], SHAPE, seed, 0.02, 120)
    for i in range(1, n):
        edge = SKY_HZ * i / n + (noise(SHAPE, (200, 40), seed + i, 3)[0] - 0.5) * 4.0
        m = step(0.0, 1.0, (y - edge) / 6.0)
        over(pic, vary(stops[i], SHAPE, seed + 10 + i, 0.02, 120), m)
    # under the last band, down to the ground: the paper (the far slope and the mist lie over it)
    over(pic, vary(PAPER, SHAPE, seed + 30, 0.02, 120), step(0.0, 1.0, (y - SKY_HZ) / 6.0))
    return np.clip(pic, 0, 1).astype(F32)


def slope(pic, seed=21):
    """The hillside the path climbs, as flats: the far slope behind everything (cerulean + white, pulled to the paper,
    no line), a nearer rise of it a step darker, then the ground round the house and down to us: wet earth as one
    flat with moss as a second flat; no gradients, no pools."""
    x, y = PX, PY
    top = 300 + (noise(SHAPE, (260, 40), seed, 3)[0] - 0.5) * 36 - (x - 400) * 0.06
    far = step(0.0, 1.0, (y - top) / 5.0)
    far_c = far_of(lerp(VIRIDIAN, CERULEAN, 0.5), 0.62)
    over(pic, vary(far_c, SHAPE, seed + 1, 0.02, 120), far)
    top2 = 352 + (noise(SHAPE, (200, 30), seed + 9, 3)[0] - 0.5) * 26 - (x - 400) * 0.04
    mid_c = far_of(lerp(VIRIDIAN, COBALT, 0.35), 0.42)
    over(pic, vary(mid_c, SHAPE, seed + 8, 0.03, 90), step(0.0, 1.0, (y - top2) / 5.0))
    # the ground: one flat of wet earth (ochre and sienna pulled to prussian), its upper edge round the house's foot
    gy = 446 - (np.abs(x - 440) * 0.05) + (noise(SHAPE, (120, 20), seed + 3, 3)[0] - 0.5) * 6
    ground = step(0.0, 1.0, (y - gy) / 4.0)
    earth = lerp(lerp(OCHRE, SIENNA, 0.5), PRUSSIAN, 0.56)
    over(pic, vary(earth, SHAPE, seed + 2, 0.05, 40), ground)
    # moss: a second flat in patches with hard, wobbling edges
    moss = step(0.58, 0.64, noise(SHAPE, 70, seed + 4, 3)) * ground
    over(pic, vary(lerp(VIRIDIAN, PRUSSIAN, 0.45), SHAPE, seed + 5, 0.04, 60), moss)
    # the nearer ground a step deeper (the near plane holds the deepest darks)
    near = step(0.0, 1.0, (y - 520) / 6.0) * ground
    over(pic, vary(lerp(earth, PRUSSIAN, 0.22), SHAPE, seed + 6, 0.05, 40), near * 0.85)
    return ground


def steps_mask():
    pts_l, pts_r = [], []
    for yy in range(606, 426, -4):
        hw = half_width(yy)
        cx = path_x(yy)
        pts_l.append((cx - hw, yy))
        pts_r.append((cx + hw, yy))
    poly = pts_l + pts_r[::-1]
    return mask_poly(SHAPE, poly, wobble=1.5, seed=3), poly


STEP_ROWS = []


def step_rows():
    """Each tread's bottom row and height, bottom first (shared by the painting, the sheen and the contour)."""
    if STEP_ROWS:
        return STEP_ROWS
    yy, i = 600.0, 0
    while yy > 430:
        k = float(k_at(yy))
        rise = max(4.0, (13.0 + 5.0 * math.sin(i * 2.3)) * k)
        STEP_ROWS.append((yy, rise, i))
        yy -= rise
        i += 1
    return STEP_ROWS


def paint_steps(pic, seed=31):
    """Worn stone steps, wet: each tread one flat (a wet pebble is prussian 0.5 in white), each riser the shade flat;
    a sheen of lead white along every tread's far edge (the wet); no modelling."""
    m, poly = steps_mask()
    tread = lerp(WHITE, PRUSSIAN, 0.52)
    riser = shade_of(tread, 0.45)
    over(pic, vary(tread, SHAPE, seed, 0.03, 60), m)
    s = Paper(SHAPE)
    for (yy, rise, i) in step_rows():
        cx, hw = path_x(yy), half_width(yy)
        wob = math.sin(i * 1.7) * 2.0
        s.poly([(cx - hw, yy), (cx + hw, yy), (cx + hw - 2, yy - rise * 0.42 + wob), (cx - hw + 2, yy - rise * 0.42 + wob)], riser, 1.0)
        t = lerp(tread, PAPER, 0.08 * ((i % 3) - 1))
        s.poly([(cx - hw + 2, yy - rise * 0.42 + wob), (cx + hw - 2, yy - rise * 0.42 + wob), (cx + hw - 4, yy - rise), (cx - hw + 4, yy - rise)], t, 1.0)
        if i % 4 == 1:                                            # moss in a joint, a flat fleck
            s.poly([(cx - hw * 0.5, yy - rise * 0.42 + wob), (cx - hw * 0.1, yy - rise * 0.42 + wob), (cx - hw * 0.15, yy - rise * 0.42 + wob + 2), (cx - hw * 0.45, yy - rise * 0.42 + wob + 2)], lerp(VIRIDIAN, PRUSSIAN, 0.3), 1.0)
    # the puddles: flat lenses of the paper (the rings on them are the engine's)
    for (px, py_, r) in ((392, 585, 20), (440, 540, 15), (418, 506, 11), (446, 476, 8)):
        s.ellipse(px, py_, r, r * 0.3, lerp(PAPER, CERULEAN, 0.2), 1.0)
    s.onto(pic)
    return m


def house(s):
    """The charcoal-burner's storehouse as flats: the front wall and the end wall (dark wet boards: ochre and sienna
    pulled to prussian; the end wall the shade flat), the thatch in two flats (front slope, end slope) with rows of
    short strokes along the eave, the eaves' dark underside, the door, the small high window, the floor on its posts
    with the dark gap under it, the lean-to."""
    fl, fr, br = HOUSE["fl"], HOUSE["fr"], HOUSE["br"]
    wh, rh, gap = HOUSE["wall_h"], HOUSE["ridge_h"], HOUSE["floor_gap"]
    sill = lambda p: (p[0], p[1] - gap)
    wall = lerp(lerp(OCHRE, SIENNA, 0.55), PRUSSIAN, 0.52)
    wall_end = shade_of(wall, 0.40)
    dark = lerp(PRUSSIAN, SIENNA, 0.15)
    # under the floor: the dark gap, the posts
    s.poly([fl, fr, (fr[0], fr[1] - gap), (fl[0], fl[1] - gap)], dark, 1.0)
    s.poly([fr, br, (br[0], br[1] - gap), (fr[0], fr[1] - gap)], dark, 1.0)
    for px in np.linspace(fl[0] + 8, fr[0] - 8, 7):
        s.poly([(px - 2.5, fl[1] + 1), (px + 2.5, fl[1] + 1), (px + 2.5, fl[1] - gap - 1), (px - 2.5, fl[1] - gap - 1)], wall_end, 1.0)
    # the walls
    front = [sill(fl), sill(fr), (fr[0], fr[1] - gap - wh), (fl[0], fl[1] - gap - wh)]
    s.poly(front, wall, 1.0)
    end = [sill(fr), sill(br), (br[0], br[1] - gap - wh * 0.92), (fr[0], fr[1] - gap - wh)]
    s.poly(end, wall_end, 1.0)
    # the door: a darker flat, its frame a sienna flat
    dx0, dx1 = HOUSE["door"]
    dh = wh * 0.76
    base_y = lambda px: fl[1] - gap + (fr[1] - fl[1]) * (px - fl[0]) / (fr[0] - fl[0])
    s.poly([(dx0 - 3, base_y(dx0 - 3)), (dx1 + 3, base_y(dx1 + 3)), (dx1 + 3, base_y(dx1 + 3) - dh - 3), (dx0 - 3, base_y(dx0 - 3) - dh - 3)], lerp(SIENNA, PRUSSIAN, 0.35), 1.0)
    s.poly([(dx0, base_y(dx0)), (dx1, base_y(dx1)), (dx1, base_y(dx1) - dh), (dx0, base_y(dx0) - dh)], lerp(wall, PRUSSIAN, 0.35), 1.0)
    # the window: a flat of the rain's grey light, its frame sienna
    wx0, wx1, wy0, wy1 = HOUSE["window"]
    sl = (br[1] - fr[1]) / (br[0] - fr[0])
    win = [(wx0, wy1), (wx1, wy1 + sl * (wx1 - wx0)), (wx1, wy0 + sl * (wx1 - wx0)), (wx0, wy0)]
    s.poly([(wx0 - 2, wy1 + 2), (wx1 + 2, wy1 + 2 + sl * (wx1 - wx0 + 4)), (wx1 + 2, wy0 - 2 + sl * (wx1 - wx0 + 4)), (wx0 - 2, wy0 - 2)], lerp(SIENNA, PRUSSIAN, 0.3), 1.0)
    s.poly(win, lerp(PAPER, COBALT, 0.45), 1.0)
    # the eaves' underside: a dark flat over the walls
    ex = 14
    s.poly([(fl[0] - ex, fl[1] - gap - wh + 6), (fr[0] + ex * 0.6, fr[1] - gap - wh + 4), (fr[0] + ex * 0.6, fr[1] - gap - wh - 8), (fl[0] - ex, fl[1] - gap - wh - 6)], dark, 1.0)
    s.poly([(fr[0] + ex * 0.6, fr[1] - gap - wh + 4), (br[0] + ex, br[1] - gap - wh * 0.92 + 2), (br[0] + ex, br[1] - gap - wh * 0.92 - 10), (fr[0] + ex * 0.6, fr[1] - gap - wh - 8)], dark, 1.0)
    # the thatch: two flats (the front slope lit by the sky, the end slope its shade), heavy with wet
    ridge_l = (fl[0] + 36, fl[1] - gap - rh)
    ridge_r = (br[0] - 50, br[1] - gap - rh * 0.93 - 2)
    thatch = lerp(lerp(OCHRE, SIENNA, 0.3), PRUSSIAN, 0.5)
    roof_front = [(fl[0] - ex, fl[1] - gap - wh - 6), (fr[0] + ex * 0.6, fr[1] - gap - wh - 8), ridge_r, ridge_l]
    roof_end = [(fr[0] + ex * 0.6, fr[1] - gap - wh - 8), (br[0] + ex, br[1] - gap - wh * 0.92 - 10), ridge_r]
    s.poly(roof_front, thatch, 1.0)
    s.poly(roof_end, shade_of(thatch, 0.38), 1.0)
    # the thatch's texture, drawn: four rows of short strokes along the eave (and three along the end's)
    rng = np.random.default_rng(41)
    for row in range(4):
        for t in np.linspace(0.01, 0.99, 42):
            bx = lerp(roof_front[0][0], roof_front[1][0], t)
            by = lerp(roof_front[0][1], roof_front[1][1], t)
            tx = lerp(ridge_l[0], ridge_r[0], t)
            ty = lerp(ridge_l[1], ridge_r[1], t)
            u = 0.92 - row * 0.09 + rng.uniform(-0.02, 0.02)
            px, py_ = lerp(tx, bx, u), lerp(ty, by, u)
            s.line([(px, py_), (px + 0.3, py_ + rng.uniform(4, 7))], lerp(thatch, PRUSSIAN, 0.45), 0.7, 0.55)
    for row in range(3):
        for t in np.linspace(0.02, 0.98, 14):
            bx = lerp(roof_end[0][0], roof_end[1][0], t)
            by = lerp(roof_end[0][1], roof_end[1][1], t)
            u = 0.92 - row * 0.1
            px, py_ = lerp(ridge_r[0], bx, u), lerp(ridge_r[1], by, u)
            s.line([(px, py_), (px + 0.5, py_ + rng.uniform(3, 6))], lerp(thatch, PRUSSIAN, 0.55), 0.7, 0.5)
    s.line([ridge_l, ridge_r], lerp(thatch, PAPER, 0.3), 3.0, 1.0)                          # the ridge, bound with bamboo
    # the lean-to: a board roof (one flat), two posts, faggots and sacks under it (flats)
    L = LEANTO
    s.poly([(L["x0"], L["roof_y"] + 6), (L["x1"], L["wall_y"] - 10), (L["x1"], L["wall_y"] - 22), (L["x0"] - 6, L["roof_y"] - 8)], shade_of(wall, 0.2), 1.0)
    for px in (L["x0"] + 4, L["x0"] + 34):
        s.line([(px, L["roof_y"] + 6 - (px - L["x0"]) * 0.2), (px, L["post_y"] - (px - L["x0"]) * 0.1)], lerp(SIENNA, PRUSSIAN, 0.4), 3.0, 1.0)
    for i in range(7):
        px = L["x0"] + 10 + i * 8
        s.ellipse(px, L["post_y"] - 16 - (i % 2) * 6, 7, 5, lerp(PRUSSIAN, SIENNA, 0.25 + 0.1 * (i % 2)), 1.0)
    s.poly([(L["x0"] + 6, L["post_y"] - 2), (L["x1"] - 4, L["post_y"] - 8), (L["x1"] - 4, L["post_y"] - 30), (L["x0"] + 6, L["post_y"] - 26)], lerp(PRUSSIAN, SIENNA, 0.2), 1.0)
    return s


def kiln(s):
    """The charcoal kiln: an earth dome in two flats (lit top, shade side), a dark arched mouth, cold."""
    K = KILN
    earth = lerp(lerp(OCHRE, SIENNA, 0.5), PRUSSIAN, 0.45)
    s.ellipse(K["cx"], K["cy"] - 4, K["rx"], K["ry"], earth, 1.0)
    pts = [(K["cx"] + math.cos(a) * K["rx"], K["cy"] - 4 + math.sin(a) * K["ry"]) for a in np.linspace(-math.pi * 0.05, -math.pi * 0.55, 12)]
    s.poly(pts + [(K["cx"] + K["rx"] * 0.1, K["cy"] - 4 + K["ry"]), (K["cx"] + K["rx"], K["cy"] - 4 + K["ry"] * 0.6)], shade_of(earth, 0.45), 1.0)
    s.poly([(K["cx"] - K["rx"], K["cy"] + 2), (K["cx"] + K["rx"], K["cy"] + 2), (K["cx"] + K["rx"], K["cy"] - 6), (K["cx"] - K["rx"], K["cy"] - 6)], shade_of(earth, 0.25), 1.0)
    m = (K["cx"] - 12, K["cy"] + 1)
    s.poly([(m[0] - 9, m[1]), (m[0] + 9, m[1]), (m[0] + 9, m[1] - 9), (m[0], m[1] - 15), (m[0] - 9, m[1] - 9)], PRUSSIAN, 1.0)
    for i in range(5):                                            # cut logs beside it
        s.ellipse(K["cx"] + K["rx"] + 8 + i * 5, K["cy"] + 2 - (i % 2) * 4, 6, 4, lerp(PRUSSIAN, SIENNA, 0.3), 1.0)
    return s


def pipe(s):
    a, b = PIPE["from"], PIPE["to"]
    s.line([a, b], lerp(OCHRE, PAPER, 0.35), 4.0, 1.0)
    for t in (0.35, 0.7):
        px, py_ = lerp(a[0], b[0], t), lerp(a[1], b[1], t)
        s.line([(px, py_ - 2.5), (px + 0.5, py_ + 2.5)], lerp(SIENNA, PRUSSIAN, 0.3), 0.8, 0.9)
    s.ellipse(b[0], b[1], 2.2, 2.2, PRUSSIAN, 1.0)
    return s


def figure(s):
    """The small stone figure by the path: two flats of wet stone, a scrap of vermilion cloth, pebbles at its foot."""
    Fg = FIGURE
    x, b, h = Fg["x"], Fg["base"], Fg["h"]
    stone = lerp(WHITE, PRUSSIAN, 0.42)
    s.poly([(x - 9, b), (x + 9, b), (x + 8, b - h * 0.62), (x - 8, b - h * 0.62)], stone, 1.0)
    s.poly([(x + 1, b), (x + 9, b), (x + 8, b - h * 0.62), (x + 1, b - h * 0.62)], shade_of(stone, 0.35), 1.0)
    s.ellipse(x, b - h * 0.78, 7.5, 8.5, stone, 1.0)
    s.poly([(x, b - h * 0.98), (x + 7.5, b - h * 0.8), (x + 6, b - h * 0.64), (x, b - h * 0.64)], shade_of(stone, 0.35), 1.0)
    s.poly([(x - 8, b - h * 0.66), (x + 8, b - h * 0.66), (x + 7, b - h * 0.56), (x - 7, b - h * 0.56)], VERMILION, 1.0)
    s.poly([(x + 6, b - h * 0.6), (x + 12, b - h * 0.52), (x + 9, b - h * 0.44), (x + 5, b - h * 0.56)], lerp(VERMILION, PRUSSIAN, 0.25), 1.0)
    for (dx, dy) in ((-14, -1), (-10, 1), (12, 0)):
        s.ellipse(x + dx, b + dy, 3, 1.8, stone, 1.0)
    return s


# ---------------------------------------------------------------- the cedars, in three planes
def trunk(s, x, base, hw, plane, seed=0, top=-20):
    """One cedar as flats. `plane`: 0 near (burnt sienna toward prussian, in three bands that pale a step each toward
    the paper as the trunk rises into the mist; the lit left flat and the shade right flat with a hard edge between;
    drawn bark lines), 1 middle (the same pulled 0.3 toward the paper and blue, no texture), 2 far (pulled 0.65, one
    flat, lost in the mist). The contour is drawn afterwards (details()), by plane."""
    rng = np.random.default_rng(seed)
    pull = (0.0, 0.32, 0.66)[plane]
    lit = far_of(lerp(SIENNA, PRUSSIAN, 0.55), pull)
    shade = far_of(lerp(SIENNA, PRUSSIAN, 0.78), pull)
    bands = 3 if plane < 2 else 1
    span = base - top
    cuts = [0.0, 0.46 + rng.uniform(-0.08, 0.08), 0.78 + rng.uniform(-0.06, 0.06), 1.0] if bands == 3 else [0.0, 1.0]
    for i in range(bands):
        y1 = base - span * cuts[i]
        y0 = base - span * cuts[i + 1]
        w1 = hw * (1 - 0.3 * cuts[i])
        w0 = hw * (1 - 0.3 * cuts[i + 1])
        mist = (0.0, 0.2, 0.0)[plane] * i                           # the middle plane pales a step into the mist with each band; the near plane keeps its colour
        wob = math.sin(seed * 0.7 + i) * hw * 0.05
        l_c, s_c = lerp(lit, PAPER, mist), lerp(shade, PAPER, mist)
        split = 0.42
        s.poly([(x - w1 + wob, y1), (x - w1 + 2 * w1 * split + wob, y1), (x - w0 + 2 * w0 * split + wob * 1.2, y0), (x - w0 + wob * 1.2, y0)], l_c, 1.0)
        s.poly([(x - w1 + 2 * w1 * split + wob, y1), (x + w1 + wob, y1), (x + w0 + wob * 1.2, y0), (x - w0 + 2 * w0 * split + wob * 1.2, y0)], s_c, 1.0)
    # the roots: a spread at the foot, the same two flats
    s.poly([(x - hw * 1.7, base + 2), (x - hw * 0.1, base + 2), (x - hw * 0.1, base - hw * 1.2), (x - hw * 1.05, base - hw * 1.2)], lit, 1.0)
    s.poly([(x - hw * 0.1, base + 2), (x + hw * 1.7, base + 2), (x + hw * 1.05, base - hw * 1.2), (x - hw * 0.1, base - hw * 1.2)], shade, 1.0)
    if plane == 0:                                                 # texture drawn: a few vertical bark lines on the lit flat
        for i in range(rng.integers(3, 6)):
            px = x - hw * 0.85 + rng.uniform(0, hw * 1.5)
            y0 = rng.uniform(top + 60, base - 10)
            ln = rng.uniform(40, 140)
            s.line([(px, y0), (px + rng.uniform(-1.5, 1.5), y0 - ln)], lerp(SIENNA, PRUSSIAN, 0.65), 0.7, 0.45)
    return s


def crown(s, cx, cy, r, plane, seed=0):
    """A cedar's crown at the top of the frame: boughs that leave the trunk at (cx, cy) and sweep out and down, each
    carrying flat masses of foliage (the undersides, seen from below: viridian toward prussian near, pulled toward the
    paper far), and a mass over the trunk's top. Flat, lobed, no line."""
    rng = np.random.default_rng(seed)
    pull = (0.0, 0.3, 0.62)[plane]
    under = far_of(lerp(VIRIDIAN, PRUSSIAN, 0.64), pull)
    upper = far_of(lerp(VIRIDIAN, PRUSSIAN, 0.42), pull)

    def mass(mx, my, mr, c):
        pts = []
        for t in np.linspace(0, 2 * math.pi, 22, endpoint=False):
            rr = mr * (1 + 0.18 * math.sin(t * 5 + seed) + (0.22 if math.sin(t) > 0.3 and int(t * 4) % 2 else 0))
            pts.append((mx + math.cos(t) * rr * 1.7, my + math.sin(t) * rr * 0.55))
        s.poly(pts, c, 1.0)

    mass(cx, cy, r * 0.55, upper)
    for i in range(rng.integers(3, 6)):
        d = 1 if (i % 2 == 0) else -1
        reach = rng.uniform(0.9, 1.7) * r
        droop = rng.uniform(0.25, 0.6) * r
        y0 = cy + rng.uniform(-0.3, 0.5) * r
        tip = (cx + d * reach, y0 + droop)
        mid = (cx + d * reach * 0.55, y0 + droop * 0.35)
        s.line([(cx, y0), mid, tip], lerp(under, PRUSSIAN, 0.2), max(1.5, r * 0.06), 1.0)
        for (mx, my), k in ((mid, 0.42), (tip, 0.5)):
            mass(mx, my + r * 0.06, r * k * rng.uniform(0.8, 1.1), under)
    return s


def mist(pic, seed=61):
    """The mist's still body: a level band of the paper over the far slope and the feet of the far trunks (a flat with
    a soft edge: it is air), and the top of the picture dimmed toward the paper behind the far crowns."""
    x, y = PX, PY
    band = np.exp(-((y - 352) / 36.0) ** 2) * (0.6 + 0.4 * noise(SHAPE, (300, 50), seed, 3))
    over(pic, PAPER, np.clip(band * 0.40, 0, 1).astype(F32))
    return band


def under(seed=5):
    pic = sky_layer()
    ground = slope(pic)
    info = {"ground": ground}
    # the far plane: trunks and crowns lost in the mist, no line
    s = Paper(SHAPE)
    for i, (x, b, hw) in enumerate(TRUNKS_FAR):
        trunk(s, x, b, hw, 2, seed=100 + i, top=-10)
    for i, (cx, cy, r) in enumerate(CROWNS_FAR):
        crown(s, cx, cy, r, 2, seed=130 + i)
    s.onto(pic)
    info["mist"] = mist(pic)
    info["steps"] = paint_steps(pic)
    # the house, the kiln, the pipe, the figure
    s = Paper(SHAPE)
    pipe(s)
    house(s)
    kiln(s)
    figure(s)
    s.onto(pic)
    # a cast shade under the house and along the foot of the near trunks: a flat of the ground pulled to prussian, hard-edged
    fl, fr, br = HOUSE["fl"], HOUSE["fr"], HOUSE["br"]
    tint(pic, lerp(COBALT, PRUSSIAN, 0.5) * 1.6, mask_poly(SHAPE, [(fl[0] - 10, fl[1] + 1), (br[0] + 6, br[1] + 1), (br[0] + 10, br[1] + 12), (fl[0] - 6, fl[1] + 14)], wobble=1.5, seed=7) * 0.42)
    # the middle plane: trunks and their crowns
    s = Paper(SHAPE)
    for i, (x, b, hw) in enumerate(TRUNKS_L[:3] + TRUNKS_R[:3]):
        trunk(s, x, b, hw, 1, seed=200 + i)
    for i, (cx, cy, r) in enumerate(CROWNS_MID):
        crown(s, cx, cy, r, 1, seed=230 + i)
    s.onto(pic)
    for (x, b, hw) in TRUNKS_L[:3] + TRUNKS_R[:3]:
        tint(pic, lerp(COBALT, PRUSSIAN, 0.5) * 1.6, mask_ellipse(SHAPE, x, b + 2, hw * 2.4, hw * 0.7, wobble=1.0, seed=9) * 0.4)
    # the near plane's crowns (the near trunks themselves are cut-outs): the dark masses at the very top
    s = Paper(SHAPE)
    for i, (cx, cy, r) in enumerate(CROWNS_NEAR):
        crown(s, cx, cy, r, 0, seed=260 + i)
    s.onto(pic)
    info["flats"] = pic.copy()
    return np.clip(pic, 0, 1), info


# ================================================================ the cut-outs
def plane_trunks(which):
    s = Paper(SHAPE)
    if which == "front":
        for (x, b, hw), sd in ((FRONT_L, 301), (FRONT_R, 302)):
            trunk(s, x, b, hw, 0, seed=sd, top=-40)
    elif which == "cedar-l":
        for (x, b, hw), sd in ((TRUNKS_L[3], 311), (TRUNKS_L[4], 312)):
            trunk(s, x, b, hw, 0, seed=sd, top=-30)
    elif which == "cedar-r":
        for (x, b, hw), sd in ((TRUNKS_R[3], 321), (TRUNKS_R[4], 322)):
            trunk(s, x, b, hw, 0, seed=sd, top=-30)
    c, a = s.done()
    return c, (a > 0.5).astype(F32)


def plane_light():
    """The line of lamplight under the storehouse's floor between the posts: naples yellow (the lamp's warmth), a flat."""
    s = Paper(SHAPE)
    fl, fr = HOUSE["fl"], HOUSE["fr"]
    gap = HOUSE["floor_gap"]
    posts = list(np.linspace(fl[0] + 8, fr[0] - 8, 7))
    edges = [fl[0] + 1] + posts + [fr[0] - 1]
    for a, b in zip(edges[:-1], edges[1:]):
        x0, x1 = a + 3, b - 3
        if x1 <= x0:
            continue
        ya = fl[1] + (fr[1] - fl[1]) * (x0 - fl[0]) / (fr[0] - fl[0]) - gap * 0.55
        yb = fl[1] + (fr[1] - fl[1]) * (x1 - fl[0]) / (fr[0] - fl[0]) - gap * 0.55
        s.poly([(x0, ya - 1.6), (x1, yb - 1.6), (x1, yb + 1.6), (x0, ya + 1.6)], lerp(NAPLES, OCHRE, 0.3), 1.0)
        s.poly([(x0 + 1, ya - 0.6), (x1 - 1, yb - 0.6), (x1 - 1, yb + 0.6), (x0 + 1, ya + 0.6)], lerp(NAPLES, WHITE, 0.35), 1.0)
    c, a = s.done()
    return c, (a > 0.5).astype(F32)


def plane_window_lit():
    """The small high window lit from inside: a flat of naples yellow in the opening (a lantern behind it)."""
    s = Paper(SHAPE)
    fr, br = HOUSE["fr"], HOUSE["br"]
    wx0, wx1, wy0, wy1 = HOUSE["window"]
    sl = (br[1] - fr[1]) / (br[0] - fr[0])
    win = [(wx0, wy1), (wx1, wy1 + sl * (wx1 - wx0)), (wx1, wy0 + sl * (wx1 - wx0)), (wx0, wy0)]
    s.poly(win, lerp(NAPLES, OCHRE, 0.2), 1.0)
    s.poly([(wx0 + 3, wy1 - 3), (wx1 - 3, wy1 - 3 + sl * (wx1 - wx0 - 6)), (wx1 - 3, wy0 + 3 + sl * (wx1 - wx0 - 6)), (wx0 + 3, wy0 + 3)], lerp(NAPLES, WHITE, 0.4), 1.0)
    c, a = s.done()
    return c, (a > 0.5).astype(F32)


# ================================================================ details: the flats said again, then the contour
def details(pic, info):
    """The flats of the built and grown things restated over the brushwork (so the brush leaves its marks but the
    masses stay flat), then the keyblock's line by plane: 1 px burnt sienna at 0.6 on the near trunks' edges, 0.7 px
    prussian at 0.55 on the middle trunks and the house, 0.9 px on the nearest steps' edges, none on the far plane,
    the sky, the mist or the ground."""
    flats = info["flats"]
    restate = mask_poly(SHAPE, [(0, 0), (800, 0), (800, 460), (0, 460)]) * 0.55          # the trunks, crowns and house
    pic[...] = lerp(pic, flats, restate[..., None])
    s = Paper(SHAPE)
    fl, fr, br = HOUSE["fl"], HOUSE["fr"], HOUSE["br"]
    gap, wh = HOUSE["floor_gap"], HOUSE["wall_h"]
    ln = lambda pts, w=0.7, a=0.55, c=LINE: s.line(pts, c, w, a)
    # the house (middle distance): 0.7 px
    ln([(fl[0], fl[1]), (fl[0], fl[1] - gap - wh), (fr[0], fr[1] - gap - wh), (fr[0], fr[1]), (fl[0], fl[1])])
    ln([(fr[0], fr[1]), (br[0], br[1]), (br[0], br[1] - gap - wh * 0.92)])
    ln([(fl[0], fl[1] - gap), (fr[0], fr[1] - gap), (br[0], br[1] - gap)])
    dx0, dx1 = HOUSE["door"]
    dh = wh * 0.76
    base_y = lambda px: fl[1] - gap + (fr[1] - fl[1]) * (px - fl[0]) / (fr[0] - fl[0])
    ln([(dx0, base_y(dx0)), (dx0, base_y(dx0) - dh), (dx1, base_y(dx1) - dh), (dx1, base_y(dx1))])
    wx0, wx1, wy0, wy1 = HOUSE["window"]
    sl = (br[1] - fr[1]) / (br[0] - fr[0])
    ln([(wx0, wy1), (wx1, wy1 + sl * (wx1 - wx0)), (wx1, wy0 + sl * (wx1 - wx0)), (wx0, wy0), (wx0, wy1)])
    ex = 14
    ridge_l = (fl[0] + 36, fl[1] - gap - HOUSE["ridge_h"])
    ridge_r = (br[0] - 50, br[1] - gap - HOUSE["ridge_h"] * 0.93 - 2)
    ln([(fl[0] - ex, fl[1] - gap - wh - 6), ridge_l, ridge_r, (br[0] + ex, br[1] - gap - wh * 0.92 - 10)])        # the roof's top edges
    ln([(fl[0] - ex, fl[1] - gap - wh + 6), (fr[0] + ex * 0.6, fr[1] - gap - wh + 4), (br[0] + ex, br[1] - gap - wh * 0.92 + 2)])   # the eave
    ln([(fr[0] + ex * 0.6, fr[1] - gap - wh - 8), ridge_r])                                                      # the hip
    # the boards of the front wall, drawn: 0.6 px prussian at 0.3
    for i in range(1, 9):
        t = i / 9
        s.line([(fl[0], fl[1] - gap - wh * t), (fr[0], fr[1] - gap - wh * t)], LINE, 0.6, 0.3)
        s.line([(fr[0], fr[1] - gap - wh * t), (br[0], br[1] - gap - wh * 0.92 * t)], LINE, 0.6, 0.3)
    # the kiln, the figure, the pipe: 0.7 px
    K = KILN
    ln([(K["cx"] + math.cos(a) * K["rx"], K["cy"] - 4 - math.sin(a) * K["ry"]) for a in np.linspace(0.05, math.pi - 0.05, 20)])
    Fg = FIGURE
    x, b, h = Fg["x"], Fg["base"], Fg["h"]
    ln([(x - 9, b), (x - 8, b - h * 0.62), (x - 6, b - h * 0.7), (x - 7.5, b - h * 0.78), (x, b - h), (x + 7.5, b - h * 0.78), (x + 6, b - h * 0.7), (x + 8, b - h * 0.62), (x + 9, b)], 0.8, 0.7)
    ln([PIPE["from"], PIPE["to"]], 0.6, 0.45)
    # the steps: the nearest treads' front edges, 1 px near thinning to 0.6 far, and the path's two edges
    for (yy, rise, i) in step_rows():
        k = float(k_at(yy))
        cx, hw = path_x(yy), half_width(yy)
        s.line([(cx - hw, yy), (cx + hw, yy)], LINE, 0.5 + 0.5 * k, 0.35 + 0.4 * k)
        # the wet: a sheen of lead white along the tread's far edge
        s.line([(cx - hw * 0.8 + 4, yy - rise + 1), (cx + hw * 0.8 - 4, yy - rise + 1)], WHITE, 0.5 + 0.5 * k, 0.28 + 0.3 * k)
    s.line([(path_x(y_) - half_width(y_), y_) for y_ in range(600, 428, -6)], LINE, 0.9, 0.5)
    s.line([(path_x(y_) + half_width(y_), y_) for y_ in range(600, 428, -6)], LINE, 0.9, 0.5)
    # the middle trunks: 0.7 px prussian at 0.5 down both edges (the far ones: none)
    for (x, b, hw) in TRUNKS_L[:3] + TRUNKS_R[:3]:
        ln([(x - hw * 1.0, b - hw), (x - hw * 0.7, -20)], 0.7, 0.5)
        ln([(x + hw * 1.0, b - hw), (x + hw * 0.7, -20)], 0.7, 0.5)
        ln([(x - hw * 1.7, b + 2), (x - hw * 1.05, b - hw * 1.2), (x - hw, b - hw * 1.3)], 0.7, 0.5)
        ln([(x + hw * 1.7, b + 2), (x + hw * 1.05, b - hw * 1.2), (x + hw, b - hw * 1.3)], 0.7, 0.5)
    # the middle crowns' undersides: a breath of line along their lower lobes
    s.onto(pic)
    return pic


def contour_near(c, a, trunks):
    """The warm contour on a near trunk cut-out: burnt sienna, 1 px, alpha 0.6, down both edges and round the roots."""
    s = Paper(SHAPE)
    for (x, b, hw) in trunks:
        s.line([(x - hw * 1.0, b - hw), (x - hw * 0.7, -40)], SIENNA, 1.0, 0.6)
        s.line([(x + hw * 1.0, b - hw), (x + hw * 0.7, -40)], SIENNA, 1.0, 0.6)
        s.line([(x - hw * 1.7, b + 2), (x - hw * 1.05, b - hw * 1.2), (x - hw, b - hw * 1.3)], SIENNA, 1.0, 0.6)
        s.line([(x + hw * 1.7, b + 2), (x + hw * 1.05, b - hw * 1.2), (x + hw, b - hw * 1.3)], SIENNA, 1.0, 0.6)
    col_, al = s.done()
    out = c.copy()
    over(out, col_, al * a)                                       # only within the cut-out's own edge
    return out


# ================================================================ finishing
def grade(picture):
    """The last glaze: the darks lifted a little toward prussian blue (there is no black under rain)."""
    lum = (picture @ np.array([0.3, 0.55, 0.15], dtype=F32))[..., None]
    out = picture + 0.04 * np.clip(1 - lum / 0.4, 0, 1) * np.array([0.3, 0.5, 1.2], dtype=F32)
    return np.clip(out, 0, 1).astype(F32)


PALETTES = {}


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.012, amount=0.02):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    PALETTES[name] = pal
    return os.path.getsize(name)


def show(picture, name):
    Image.fromarray((np.clip(picture, 0, 1) * 255).astype(np.uint8)).save(name)


def brushed_plane(color, alpha, ground, fast, seed=4):
    """A cut-out repainted with the brush against the ground it stands on, then restated (its flats stay flat); its
    edge stays exactly as it was."""
    if fast or not (alpha > 0.5).any():
        return color
    flat = ground.copy()
    over(flat, color, alpha)
    painted = strokes(flat, sizes=(9, 5, 2), seed=seed, density=1.6, jitter=0.025, keep=0.26)
    return lerp(painted, flat, 0.55)


if __name__ == "__main__":
    t0 = time.time()
    fast = "fast" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    base, info = under()
    show(base, f"{WORK}/1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.025, keep=0.26)
    print("brushed", round(time.time() - t0, 1))
    ground = pic.copy()
    details(pic, info)
    pic = grade(pic)
    show(pic, f"{WORK}/2-back.png")
    raw = {"front": plane_trunks("front"), "cedar-l": plane_trunks("cedar-l"), "cedar-r": plane_trunks("cedar-r"),
           "light-on": plane_light(), "window-lit": plane_window_lit()}
    near_of = {"front": [FRONT_L, FRONT_R], "cedar-l": TRUNKS_L[3:], "cedar-r": TRUNKS_R[3:]}
    cut = {}
    for i, (name, (c, a)) in enumerate(raw.items()):
        if name in near_of:
            cc = contour_near(brushed_plane(c, a, ground, fast, seed=20 + i), a, near_of[name])
            cut[name] = (grade(cc), a)
        else:
            cut[name] = (c, a)
    whole = pic.copy()
    for name in ("light-on", "cedar-l", "cedar-r", "front"):
        c, a = cut[name]
        over(whole, c, a)
    show(whole, f"{WORK}/2-all.png")
    lit = whole.copy()
    over(lit, *cut["window-lit"])
    show(lit, f"{WORK}/2-window-lit.png")
    print("planes", round(time.time() - t0, 1))
    lay = LAY.layout(info, cut)
    with open(f"{OUT}/layout.json", "w") as fh:
        json.dump(lay, fh, indent=1)
    if fast:
        sys.exit()
    print("back", finish(pic, f"{OUT}/back.png", 160))
    for name, colors in (("front", 48), ("cedar-l", 48), ("cedar-r", 48), ("light-on", 12), ("window-lit", 12)):
        c, a = cut[name]
        print(name, finish(c, f"{OUT}/{name}.png", colors, a))
    os.system(f"{sys.executable} comp.py {OUT} back light-on cedar-l cedar-r front")
    print("done", round(time.time() - t0, 1))

"""The foot of Mount Shosha, about 29 April 1830: the women's hall of Engyo-ji (edo-shosha), late afternoon and then
sunset. PAINT-21E, round twenty-one.

The design (S/briefs/out/edo2-design.md, sections 2, 4, 5 and #37; S/briefs/PAINT-21E.md), in the act's manner
(S/work-20-paintA/style.md): flat masses, graded skies, one fine prussian contour, few colours; the sunset's chrome orange
and geranium lake in the sky's bands and the light, nowhere else. The composition is our own (edo_shosha_kit.py has the
plan, the camera and the two lights).

What is in it: the mountain rising behind and to the left (pines, maples in new leaf, a late cherry in the shade, a band
of mist behind the hall); the east path climbing into the trees by stone steps, out of sight; at its foot the small stone
(women may not pass: its writing our own marks); O-Ume's thatched hut at the left by the path, its lantern on a hook; the
women's hall in the middle, small, deep-roofed, on a low stone base, turned so that its west side shows with its lattice
window; its latticed double doors (cut-outs: shut, half open, open), slips of paper and thin wood pasted round them and
up the posts, the lock on the hasp (a cut-out: shut, open), a step with a rice ball on a leaf (a cut-out); the bench
where the women wait (a cut-out), their failed combs and hairpins in a heap on a cloth; beyond the terrace's edge at the
right, far below, the Harima plain, and small and white on its hill, the castle; the road up from the town at the bottom
right. Not painted: people (the game's), the petals and the birds and the leaves' stirring (fx), light.

TWO LIGHTS: back.png is the gold afternoon with every cut-out in that light; sunset.png is the whole stage at sunset (a
layer the scene fades in over back.png, under the people), and every cut-out has its -sunset twin.

  python3 edo_shosha.py          paints both lights into out/edo-shosha/ (and out/edo-shosha-comp-*.png to look at)
  python3 edo_shosha.py fast     no brush pass: out/edo-shosha-2-gold.png and out/edo-shosha-2-sunset.png only"""

import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, Sheet, grid, noise, blur, over, tint, glow, lerp, mask_poly, mask_ellipse, strokes, curve, warp, vary
from rome_steps_kit import Canvas
from edo_town_kit import (PAINT, PAPER, LINE, mix, shade_of, sheet_layer, outline, eave, brushed, finish, to_png, pine, bands, hull, box_of)
from edo_shosha_kit import *

LIGHT = "gold"
L = palette("gold")


def set_light(name):
    global LIGHT, L
    LIGHT = name
    L = palette(name)


def F(normal, base, lit, sh):
    """A face's flat in the current light."""
    return face_colour(L, base, lit, sh, LIGHT, normal)


# ---------------------------------------------------------------- the sky, the sun, the plain far below
def sky_layer():
    pic = bands(L["sky"], 0, 286, seed=51, wobble=2.2, soft=2.6)
    s = Sheet(SHAPE)
    if LIGHT == "gold":
        for (cx, cy, w, h) in ((640, 64, 220, 12), (720, 92, 120, 8), (520, 30, 140, 9)):
            top = [(cx - w / 2 + w * i / 10, cy - h * (0.5 + 0.5 * math.sin(i * 1.9 + cx) * 0.6) * (1 - ((i - 5) / 5.5) ** 2)) for i in range(11)]
            s.poly(top + [(cx + w / 2, cy), (cx - w / 2, cy)], mix(PAPER, PAINT["naples"], 0.2), 0.96)
            s.line(top, LINE, 0.9, 0.42)
    else:
        for (cx, cy, w, h) in ((620, 120, 260, 12), (700, 150, 160, 9), (540, 96, 120, 8)):     # flat clouds lit from below
            top = [(cx - w / 2 + w * i / 10, cy - h * (0.5 + 0.5 * math.sin(i * 1.9 + cx) * 0.6) * (1 - ((i - 5) / 5.5) ** 2)) for i in range(11)]
            s.poly(top + [(cx + w / 2, cy), (cx - w / 2, cy)], mix(PAINT["lake"], PAINT["ultra"], 0.35), 0.95)
            s.line([(cx - w / 2 + 6, cy), (cx + w / 2 - 6, cy)], mix(PAINT["orange"], PAINT["naples"], 0.4), 1.6, 0.9)
    s.onto(pic)
    if LIGHT == "sunset":
        x, y = grid(SHAPE)
        g = np.clip(1 - np.hypot((x + 40) / 420.0, (y - 250) / 200.0), 0, 1) ** 1.4
        glow(pic, mix(PAINT["orange"], PAINT["naples"], 0.35), (g * 0.45).astype(F32))
    return pic


CASTLE_AT = (742.0, 286.0)          # the foot of the castle's hill on the plain (picture), and its size
CASTLE_K = 0.085


def plain(s):
    """The Harima plain far below at the right: far hills on the horizon (no contour), the plain in flat bands of
    fields, a river's pale ribbon, villages as specks of roof, the castle small and white on its hill."""
    rng = np.random.default_rng(52)
    fh = curve([(380, 284), (470, 274), (560, 279), (640, 270), (720, 276), (800, 268), (840, 274)], 6)
    s.poly(fh + [(840, 300), (380, 300)], L["far_hills"])
    ys = [284, 292, 304, 320, 344, 380, 460]
    for i in range(len(ys) - 1):
        tone = L["plain"][min(i, len(L["plain"]) - 1)]
        s.poly([(380, ys[i]), (840, ys[i] - 2), (840, ys[i + 1]), (380, ys[i + 1])], tone)
        # the fields' divisions: faint flat strips
        for k in range(int((10 + i * 4) * (1.0 if LIGHT == "gold" else 0.45))):
            xx = rng.uniform(380, 820)
            ww = rng.uniform(8, 30) * (1 + i * 0.6)
            yy = rng.uniform(ys[i], ys[i + 1] - 1)
            s.poly([(xx, yy), (xx + ww, yy - 0.3), (xx + ww + 2, yy + 1.0 + i * 0.6), (xx + 2, yy + 1.0 + i * 0.6)],
                   mix(tone, L["plain"][0] if k % 2 else L["plain"][-1], 0.18), 0.5)
        for k in range(int(4 + i * 3)):                       # copses: small dark clumps of trees on the fields
            xx = rng.uniform(390, 820)
            yy = rng.uniform(ys[i], ys[i + 1] - 1)
            rr = 1.4 + i * 0.9
            s.ellipse(xx, yy, rr * 1.8, rr, mix(L["plain"][-1], L["pine"], 0.5), 0.85)
    river = curve([(380, 312), (480, 306), (600, 300), (700, 296), (840, 290)], 6)
    s.line(river, L["river"], 2.0, 0.85)
    for i in range(46):                                       # villages: specks of roof among trees
        xx = rng.uniform(420, 800)
        yy = rng.uniform(286, 350)
        w = rng.uniform(1.5, 4.0) * (1 + (yy - 284) / 40)
        s.poly([(xx, yy), (xx + w, yy), (xx + w * 0.8, yy - w * 0.45), (xx + w * 0.2, yy - w * 0.45)], mix(L["castle_roof"], L["far_hills"], 0.35), 0.8)
    # the castle's hill and the castle, small and white (seen 6 km off, drawn larger than the eye would: the prints' way)
    cx, cy = CASTLE_AT
    hill = curve([(cx - 40, cy + 2), (cx - 20, cy - 8), (cx, cy - 11), (cx + 22, cy - 7), (cx + 44, cy + 2)], 5)
    s.poly(hill, mix(L["plain"][-1], L["far_hills"], 0.35))
    kw = 300 * CASTLE_K
    # the keep: three white blocks narrowing, dark roofs between
    tiers = [(cx - 10, cy - 12, 20, 6), (cx - 8, cy - 18, 16, 5), (cx - 6, cy - 23, 12, 4), (cx - 4, cy - 27, 8, 3)]
    for (x0, y0, w, h) in tiers:
        s.poly([(x0, y0 + h), (x0 + w, y0 + h), (x0 + w, y0), (x0, y0)], L["castle"])
        s.line([(x0 - 1.5, y0), (x0 + w + 1.5, y0)], L["castle_roof"], 1.4)
    s.poly([(cx - 2, cy - 30), (cx + 2, cy - 30), (cx + 1.5, cy - 27), (cx - 1.5, cy - 27)], L["castle_roof"])
    for (x0, w) in ((cx - 30, 10), (cx + 18, 12)):            # its lower turrets and walls
        s.poly([(x0, cy - 6), (x0 + w, cy - 6), (x0 + w, cy - 10), (x0, cy - 10)], L["castle"])
        s.line([(x0 - 1, cy - 10), (x0 + w + 1, cy - 10)], L["castle_roof"], 1.0)


# ---------------------------------------------------------------- the mountain, its trees, the mist
def mountain(s):
    """The mountain's flank: a dark flat rising to the top-left, its edge against the sky broken by the crowns of pines;
    a paler far shoulder behind it; then the trees of its lower slopes in three depths."""
    rng = np.random.default_rng(53)
    far = curve([(300, -10), (380, 40), (470, 110), (560, 170), (640, 228), (700, 262), (760, 282)], 8)
    s.poly(far + [(760, 320), (-10, 320), (-10, -10)], L["mount_far"])
    near = curve([(180, -10), (290, 48), (390, 120), (470, 186), (540, 236), (590, 268), (624, 290)], 8)
    s.poly(near + [(624, 330), (-10, 330), (-10, -10)], L["mount"])
    # pines along the near ridge against the sky (silhouettes with their lit pads toward the sun, left)
    for i in range(16):
        t = i / 15
        px = 200 + t * 420 + rng.uniform(-8, 8)
        py = np.interp(px, [p[0] for p in near], [p[1] for p in near]) + 6
        pine(s, px, py, rng.uniform(26, 46) * (1.1 - 0.4 * t), L["pine"], L["pine_lit"], rng, pads=4)


def mist(s):
    """A band of mist lying across the trees behind the hall (the prints' way of setting a dark roof off): a flat pale
    shape with a soft-edged top, the tree crowns rising out of it."""
    top = curve([(160, 236), (260, 214), (360, 226), (460, 206), (560, 236), (640, 262)], 8)
    bot = curve([(640, 300), (520, 296), (400, 300), (280, 292), (160, 300)], 6)
    s.poly(top + bot, L["mist"], 0.92)


NEAR_RIDGE = [(180, -10), (290, 48), (390, 120), (470, 186), (540, 236), (590, 268), (624, 290)]


def ridge_y(x):
    xs = [p[0] for p in NEAR_RIDGE]
    ys = [p[1] for p in NEAR_RIDGE]
    return float(np.interp(x, xs, ys, left=-10, right=400))


def slope_trees(s):
    """The lower slopes' trees behind the hall and over the glade, kept within the mountain's mass: pines (dark, flat
    pads) and maples in fresh leaf (bright broken flats), in two depths."""
    rng = np.random.default_rng(54)
    for (n, hs) in ((16, (34, 60)), (12, (50, 84))):
        k = 0
        tries = 0
        while k < n and tries < 400:
            tries += 1
            px = rng.uniform(240, 620)
            py = rng.uniform(150, 300)
            if py < ridge_y(px) + 16 or py > 300:
                continue
            h = rng.uniform(*hs)
            if rng.random() < 0.5:
                pine(s, px, py + h * 0.2, h, L["pine"], L["pine_lit"], rng, pads=4)
            else:
                maple_crown(s, px, py, h * 0.38, rng)
            k += 1


def serrate(cx, cy, rx, ry, rng, teeth=22, depth=0.12):
    """An outline with small sharp teeth: a maple's leafy edge."""
    ph = rng.uniform(0, 6.3)
    pts = []
    n = teeth * 2
    for i in range(n):
        t = 2 * math.pi * i / n
        r = 1.0 + (depth if i % 2 == 0 else -depth * 0.4) + 0.08 * math.sin(3 * t + ph)
        pts.append((cx + rx * r * math.cos(t), cy + ry * r * math.sin(t)))
    return pts


def maple_crown(s, cx, cy, r, rng, alpha=1.0):
    """A maple in new leaf as a print cuts it: a broken flat of bright yellow-green with a fine toothed edge, a
    darker flat under it, its lit side toward the sun (left), the dark branches showing through."""
    s.line([(cx, cy + r * 1.5), (cx - r * 0.1, cy + r * 0.2)], L["trunk"], max(1.0, r * 0.12), alpha)
    s.poly(serrate(cx + r * 0.1, cy + r * 0.12, r * 1.05, r * 0.62, rng), L["maple_sh"], alpha)
    s.poly(serrate(cx - r * 0.12, cy - r * 0.08, r * 0.86, r * 0.48, rng, teeth=18), L["maple"], alpha)
    s.poly(serrate(cx - r * 0.35, cy - r * 0.2, r * 0.42, r * 0.24, rng, teeth=10, depth=0.18), L["maple_lit"], alpha * 0.9)


GLADE = [(-10, 190), (60, 178), (140, 186), (206, 200), (252, 224), (266, 346), (-10, 356)]
SUN_DISC = (122.0, 256.0, 14.0)


def glade(pic):
    """The open forest at the foot of the slope, left of the path: the light seen between the trunks (gold: the bright
    haze of the afternoon; sunset: the sky's red and orange in bands, and the sun itself, low, red, through the trees),
    the pines' trunks dark against it, their flat crowns above, merging into the mountain."""
    m = mask_poly(SHAPE, GLADE, soft=0.8)
    bp = bands(L["glade"], 196, 346, seed=61, wobble=1.6, soft=2.0)
    over(pic, bp, m)
    if LIGHT == "sunset":
        x, y = grid(SHAPE)
        sx, sy, sr = SUN_DISC
        g = np.clip(1 - np.hypot((x - sx) / 150.0, (y - sy) / 70.0), 0, 1) ** 1.5
        glow(pic, mix(PAINT["orange"], PAINT["naples"], 0.5), (g * m * 0.5).astype(F32))
        over(pic, mix(PAINT["naples"], PAPER, 0.55), mask_ellipse(SHAPE, sx, sy, sr, sr, soft=0.6) * m)
    rng = np.random.default_rng(62)
    s = Sheet(SHAPE)
    trunks = [(14, 7.0), (52, 5.0), (86, 8.0), (128, 4.5), (150, 6.5), (190, 5.5), (232, 4.0)]
    for (x, w) in trunks:
        foot = 350 - (x / 260.0) * 8 + rng.uniform(-3, 3)
        lean = rng.uniform(-6, 6)
        pts = [(x, foot), (x + lean * 0.5, 280), (x + lean, 190)]
        tone = L["trunk"] if LIGHT == "gold" else mix(L["trunk"], LINE, 0.35)
        s.taper(pts, tone, w, w * 0.7)
        if LIGHT == "gold":
            s.taper([(p[0] - w * 0.25, p[1]) for p in pts], L["trunk_lit"], w * 0.35, w * 0.25, 0.85)
        else:
            s.taper([(p[0] - w * 0.42, p[1]) for p in pts], mix(PAINT["orange"], PAINT["naples"], 0.4), 1.0, 0.8, 0.8)
            s.taper([(p[0] + w * 0.42, p[1]) for p in pts], mix(PAINT["orange"], PAINT["naples"], 0.4), 1.0, 0.8, 0.6)
    # the crowns over the glade: flat dark pads, low branches reaching out over the light
    for (x, y, rx) in ((30, 196, 46), (96, 186, 52), (170, 198, 44), (232, 210, 30), (60, 232, 24), (150, 238, 22)):
        for j in range(2):
            pad(s, x + j * 6, y - j * 12, rx * (1 - j * 0.25), rng)
    s.onto(pic)
    # the ground at the glade's foot: its own grass and the trunks' feet
    return pic


def cherry(s):
    """The late cherry in the shade on the slope left of the hall: a few soft flats of pale pink (geranium lake with
    white), its dark trunk leaning out of the slope."""
    rng = np.random.default_rng(55)
    s.line([(196, 352), (204, 300), (214, 262)], L["trunk"], 4.0)
    s.line([(204, 300), (180, 270)], L["trunk"], 2.2)
    s.line([(210, 280), (240, 256)], L["trunk"], 2.0)
    for (cx, cy, rx, ry) in ((200, 262, 38, 22), (178, 276, 26, 16), (236, 254, 26, 16), (214, 238, 24, 14)):
        s.ellipse(cx, cy, rx, ry, L["cherry_sh"])
        s.ellipse(cx - rx * 0.2, cy - ry * 0.25, rx * 0.72, ry * 0.62, L["cherry"])
        for j in range(8):
            a = rng.uniform(0, 2 * math.pi)
            s.ellipse(cx + (rx + 1) * math.cos(a), cy + (ry + 1) * math.sin(a), rng.uniform(2, 4), rng.uniform(1.5, 3), L["cherry"] if math.cos(a) < 0 else L["cherry_sh"])
    s.line([(204, 300), (196, 270), (184, 252)], L["trunk"], 1.2, 0.8)


# ---------------------------------------------------------------- the east path
PATH = [(-330.0, 0.0, 1520.0), (-360.0, 60.0, 1690.0), (-410.0, 120.0, 1880.0), (-490.0, 186.0, 2120.0), (-590.0, 240.0, 2380.0)]
PATH_W = 110.0


def path(s):
    """The east path: stone steps climbing steeply into the trees from the hall's side, each tread a flat lit on top,
    its riser in shade; the trees close over it and it is gone."""
    pts = PATH
    # the steps: walk up the centre line, a tread every 34 cm of climb
    steps = []
    for i in range(len(pts) - 1):
        (x0, y0, d0), (x1, y1, d1) = pts[i], pts[i + 1]
        n = max(1, int((y1 - y0) / 30))
        for j in range(n):
            t = j / n
            steps.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, d0 + (d1 - d0) * t))
    # the earth either side, then the steps from the top down (nearer over farther)
    left = [P(x - PATH_W / 2 - 30, y, d) for (x, y, d) in pts]
    right = [P(x + PATH_W / 2 + 30, y, d) for (x, y, d) in pts]
    s.poly(left + right[::-1], mix(L["ground"], L["grass_sh"], 0.55))
    rng = np.random.default_rng(63)
    tread_c = mix(mix(L["stone"], L["ground"], 0.35), L["grass_sh"], 0.18)
    riser_c = mix(mix(L["stone_sh"], L["grass_sh"], 0.35), LINE, 0.10)
    for i, (x, y, d) in enumerate(steps[::-1]):
        far_ = 1.0 - i / max(1, len(steps) - 1)                  # the far steps sink into the trees' shade
        a, b = P(x - PATH_W / 2, y, d), P(x + PATH_W / 2, y, d)
        c_, d_ = P(x + PATH_W / 2, y, d + 34), P(x - PATH_W / 2, y, d + 34)
        tread = [a, b, c_, d_]
        riser = [P(x - PATH_W / 2, y - 30, d), P(x + PATH_W / 2, y - 30, d), b, a]
        s.poly(riser, mix(riser_c, L["pine"], 0.35 * far_))
        s.poly(tread, mix(tread_c, L["grass_sh"], 0.45 * far_))
        for j in range(2):                                       # moss at the treads' ends
            xx = x + (-PATH_W / 2 + 8 if j == 0 else PATH_W / 2 - 14)
            s.ellipse(*P(xx, y + 1, d + 10), 3.0 * k_at(d) * 3, 1.4, L["grass"], 0.8)
        outline(s, [a, b], 0.6, 0.45, close=False)
    # where it goes into the trees: low maples and pine pads over its top steps
    for (x, y, r) in ((194, 338, 17), (236, 344, 14), (214, 322, 12)):
        maple_crown(s, x, y, r, rng)
    pad(s, 206, 312, 26, rng)


# ---------------------------------------------------------------- the terrace
EDGE = [(560, 420), (640, 410), (720, 404), (810, 400)]          # the terrace's edge at the right, the plain beyond it
ROAD = [(810, 470), (760, 500), (720, 540), (690, 610)]           # the road up from the town: its centre line, picture


def terrace(pic):
    """The ground before the hall: packed earth and gravel, grass at its edges and along the edge over the plain; the
    road from the town coming up at the bottom right."""
    rng = np.random.default_rng(56)
    s = Sheet(SHAPE)
    ground = [(-10, 330), (560, 330)] + EDGE + [(810, 610), (-10, 610)]
    s.poly(ground, L["ground"])
    s.poly([(-10, 470), (300, 470), (480, 490), (700, 520), (810, 540), (810, 610), (-10, 610)], L["ground_lit"], 0.55 if LIGHT == "gold" else 0.0)
    # the grass along the edge and at the foot of the slope; a line of low shrubs along the edge, the slope below out of sight
    s.poly(EDGE + [(810, 420), (700, 424), (620, 432), (560, 440)], L["grass"])
    for i in range(22):
        t = i / 21
        x = 560 + t * 250 + rng.uniform(-6, 6)
        y = float(np.interp(x, [p[0] for p in EDGE], [p[1] for p in EDGE])) + rng.uniform(0, 4)
        r = rng.uniform(7, 13)
        s.ellipse(x, y, r, r * 0.55, L["grass_sh"])
        s.ellipse(x - r * 0.25, y - r * 0.2, r * 0.6, r * 0.3, L["grass_lit"] if LIGHT == "gold" else L["grass"], 0.8)
    s.poly([(-10, 330), (560, 330), (560, 350), (300, 360), (-10, 372)], L["grass_sh"])
    # the road: a paler worn band up from the right edge
    road_l = [(p[0] - 30 - i * 6, p[1]) for i, p in enumerate(ROAD)]
    road_r = [(p[0] + 30 + i * 6, p[1]) for i, p in enumerate(ROAD)]
    s.poly(road_l + road_r[::-1], mix(L["ground"], L["ground_lit"], 0.55))
    # tufts of grass, small stones
    for i in range(90):
        x = rng.uniform(0, 800)
        y = rng.uniform(440, 598)
        h = rng.uniform(3, 8) * scale_at(y)
        c = L["grass_lit"] if rng.random() < 0.4 else L["grass_sh"]
        for k in range(3):
            s.line([(x + k * 1.6, y), (x + k * 1.6 + rng.uniform(-2, 2), y - h)], c, 0.9, 0.85)
    for i in range(40):
        x, y = rng.uniform(0, 800), rng.uniform(440, 598)
        r = rng.uniform(0.8, 2.6) * scale_at(y)
        s.ellipse(x, y, r * 1.5, r * 0.8, L["stone_sh"] if rng.random() < 0.5 else L["stone"], 0.8)
    s.onto(pic)
    # the printmaker's graded band along the bottom: three flat steps
    for (y0, a) in ((566, 0.10), (582, 0.18), (594, 0.26)):
        band = mask_poly(SHAPE, [(-10, y0), (810, y0 - 4), (810, 610), (-10, 610)], soft=2.0, wobble=1.5, seed=int(y0))
        over(pic, L["ground_sh"], band * a)
    return pic


# ---------------------------------------------------------------- O-Ume's hut
HUTX = (-700.0, -470.0)
HUT_D = (1600.0, 1830.0)


def hut(s):
    """O-Ume's hut by the path's foot: a small thatched hut of boards and mud plaster, its front to us, a door with a
    straw curtain, a little window, a lantern on a hook beside the door (unlit), firewood stacked against it."""
    x0, x1 = HUTX
    d0, d1 = HUT_D
    wall_c = F((0, 0, -1), L["plaster"], mix(L["plaster"], L["sun"], 0.35), L["plaster_sh"])
    side_c = F((-1, 0, 0), L["plaster"], mix(L["plaster"], L["sun"], 0.45), L["plaster_sh"])
    front = [P(x0, 0, d0), P(x1, 0, d0), P(x1, 190, d0), P(x0, 190, d0)]
    side = [P(x0, 0, d0), P(x0, 0, d1), P(x0, 190, d1), P(x0, 190, d0)]
    s.poly(side, side_c)
    s.poly(front, wall_c)
    s.poly([P(x0, 0, d0), P(x1, 0, d0), P(x1, 60, d0), P(x0, 60, d0)], L["wood"])                     # the board skirt
    for xx in (x0, x1 - 10, x0 + 110):
        s.poly([P(xx, 0, d0 - 1), P(xx + 10, 0, d0 - 1), P(xx + 10, 190, d0 - 1), P(xx, 190, d0 - 1)], L["wood_dark"])
    door = [P(x0 + 20, 0, d0 - 2), P(x0 + 100, 0, d0 - 2), P(x0 + 100, 170, d0 - 2), P(x0 + 20, 170, d0 - 2)]
    s.poly(door, L["inside"])
    for k in range(6):                                        # the straw curtain over the doorway, rolled half up
        xx = x0 + 24 + k * 13
        s.line([P(xx, 170, d0 - 3), P(xx, 110, d0 - 3)], L["thatch_lit"], 2.0, 0.9)
    s.line([P(x0 + 20, 108, d0 - 3), P(x0 + 100, 108, d0 - 3)], L["thatch"], 3.0)
    win = [P(x1 - 90, 90, d0 - 2), P(x1 - 30, 90, d0 - 2), P(x1 - 30, 140, d0 - 2), P(x1 - 90, 140, d0 - 2)]
    s.poly(win, L["inside"])
    for k in range(1, 5):
        xx = x1 - 90 + 12 * k
        s.line([P(xx, 90, d0 - 2), P(xx, 140, d0 - 2)], L["wood_dark"], 1.4)
    outline(s, win, 0.6, 0.5)
    outline(s, front, 0.8, 0.55)
    outline(s, side, 0.7, 0.5)
    # the thatched roof: a hip-and-gable seen from the front-left: its front slope and its left end, thick eaves
    ev_l, ev_r = P(x0 - 50, 190, d0 - 60), P(x1 + 50, 190, d0 - 60)
    ridge_l, ridge_r = P(x0 + 40, 330, (d0 + d1) / 2), P(x1 - 40, 330, (d0 + d1) / 2)
    back_l = P(x0 - 50, 190, d1 + 60)
    front_roof = [ev_l, ev_r, ridge_r, ridge_l]
    end_roof = [ev_l, ridge_l, back_l]
    s.poly(end_roof, F((-1, 0.6, 0), L["thatch"], L["thatch_lit"], L["thatch_sh"]))
    s.poly(front_roof, F((0, 0.6, -1), L["thatch"], L["thatch_lit"], L["thatch_sh"]))
    for k in range(1, 6):                                     # the thatch's rows: short strokes along the eave
        t = k / 6
        a = (ev_l[0] + (ridge_l[0] - ev_l[0]) * t, ev_l[1] + (ridge_l[1] - ev_l[1]) * t)
        b = (ev_r[0] + (ridge_r[0] - ev_r[0]) * t, ev_r[1] + (ridge_r[1] - ev_r[1]) * t)
        s.line([a, b], L["thatch_sh"], 0.8, 0.45)
    s.line([ev_l, ev_r], mix(L["thatch_sh"], LINE, 0.3), 3.0)                                          # the thick eave's edge
    s.line([ridge_l, ridge_r], mix(L["thatch_sh"], LINE, 0.3), 3.0)
    outline(s, front_roof + [], 0.8, 0.5)
    outline(s, end_roof, 0.7, 0.5)
    # the lantern on its hook by the door (unlit): a folding paper lantern
    hx, hy = P(x0 + 112, 150, d0 - 12)
    k = k_at(d0)
    s.line([(hx, hy - 10 * k), (hx, hy)], L["wood_dark"], 1.0)
    lw, lh = 14 * k, 26 * k
    lan = [(hx - lw, hy + 2), (hx + lw, hy + 2), (hx + lw * 1.1, hy + lh * 0.5), (hx + lw, hy + lh), (hx - lw, hy + lh), (hx - lw * 1.1, hy + lh * 0.5)]
    s.poly(lan, L["lantern"])
    for j in range(1, 5):
        yy = hy + 2 + (lh - 2) * j / 5
        s.line([(hx - lw * 1.05, yy), (hx + lw * 1.05, yy)], mix(L["lantern"], LINE, 0.25), 0.6, 0.8)
    s.poly([(hx - lw * 0.7, hy), (hx + lw * 0.7, hy), (hx + lw * 0.7, hy + 2.5), (hx - lw * 0.7, hy + 2.5)], L["wood_dark"])
    s.poly([(hx - lw * 0.7, hy + lh), (hx + lw * 0.7, hy + lh), (hx + lw * 0.7, hy + lh + 2.5), (hx - lw * 0.7, hy + lh + 2.5)], L["wood_dark"])
    outline(s, lan, 0.5, 0.55)
    # firewood stacked against the hut's right end
    for j in range(5):
        yy = 6 + j * 14
        s.poly([P(x1 + 4, yy, d0 + 10), P(x1 + 60, yy, d0 + 10), P(x1 + 60, yy + 12, d0 + 10), P(x1 + 4, yy + 12, d0 + 10)], L["wood"])
        for q in range(4):
            s.ellipse(*P(x1 + 12 + q * 14, yy + 6, d0 + 8), 2.6, 2.4, L["wood_lit"])


HUT_LANTERN = (-700.0 + 112.0, 150.0, 1600.0 - 12.0)


# ---------------------------------------------------------------- the women's hall
def hall(s):
    """The women's hall: the stone base; the west side (boards between posts, the lattice window); the front (posts,
    board panels either side of the doorway: the doors are cut-outs); the deep eaves; the pyramid roof of tiles, its
    two faces we see, the hips; the finial; the step; the slips pasted round the doors and up the posts."""
    # the base: a low drum of dressed stones, a little wider than the walls
    bo = 30.0
    b_fl, b_fr, b_bl = HP(-bo, -bo, 0), HP(SIDE + bo, -bo, 0), HP(-bo, SIDE + bo, 0)
    t_fl, t_fr, t_bl = HP(-bo, -bo, BASE_H), HP(SIDE + bo, -bo, BASE_H), HP(-bo, SIDE + bo, BASE_H)
    s.poly([b_fl, b_fr, t_fr, t_fl], F(N_FRONT, L["stone"], L["stone_lit"], L["stone_sh"]))
    s.poly([b_bl, b_fl, t_fl, t_bl], F(N_WEST, L["stone"], L["stone_lit"], L["stone_sh"]))
    s.poly([t_fl, t_fr, HP(SIDE + bo, SIDE + bo, BASE_H), t_bl], L["stone_lit"] if LIGHT == "gold" else L["stone"])
    for k in range(1, 6):                                     # the stones' joints
        a = -bo + (SIDE + 2 * bo) * k / 6
        s.line([HP(a, -bo, 0), HP(a, -bo, BASE_H)], L["stone_sh"], 0.7, 0.6)
        s.line([HP(-bo, a, 0), HP(-bo, a, BASE_H)], L["stone_sh"], 0.7, 0.6)
    outline(s, [b_fl, b_fr, t_fr, t_fl], 0.7, 0.55)
    outline(s, [b_bl, b_fl, t_fl, t_bl], 0.7, 0.55)
    # the walls
    y0, y1 = BASE_H, EAVE_Y
    front_c = F(N_FRONT, L["wood"], L["wood_lit"], L["wood_sh"])
    west_c = F(N_WEST, L["wood"], L["wood_lit"], L["wood_sh"])
    west = [HP(0, SIDE, y0), HP(0, 0, y0), HP(0, 0, y1), HP(0, SIDE, y1)]
    s.poly(west, west_c)
    for k in range(1, 9):                                     # boards
        b_ = SIDE * k / 9
        s.line([HP(0, b_, y0), HP(0, b_, y1)], mix(west_c, LINE, 0.25), 0.6, 0.5)
    # the lattice window in the west side: dark inside, vertical bars
    la, lb = LATTICE_B
    ly0, ly1 = LATTICE_Y
    win = [HP(0, la, ly0), HP(0, lb, ly0), HP(0, lb, ly1), HP(0, la, ly1)]
    s.poly(win, L["inside"])
    for k in range(1, 12):
        b_ = la + (lb - la) * k / 12
        s.line([HP(0, b_, ly0), HP(0, b_, ly1)], mix(west_c, PAPER, 0.15), 1.6)
    s.line([HP(0, la - 6, ly0 - 4), HP(0, lb + 6, ly0 - 4)], L["wood_dark"], 2.0)
    s.line([HP(0, la - 6, ly1 + 4), HP(0, lb + 6, ly1 + 4)], L["wood_dark"], 2.0)
    outline(s, win, 0.6, 0.6)
    outline(s, west, 0.8, 0.55)
    # the front: panels and the doorway (the doors themselves are cut-outs; behind them the backdrop is the dim inside)
    front = [HP(0, 0, y0), HP(SIDE, 0, y0), HP(SIDE, 0, y1), HP(0, 0, y1)]
    s.poly(front, front_c)
    for k in range(1, 12):
        a = SIDE * k / 12
        if DOOR_A[0] - 6 < a < DOOR_A[1] + 6:
            continue
        s.line([HP(a, 0, y0), HP(a, 0, y1)], mix(front_c, LINE, 0.25), 0.6, 0.5)
    da, db = DOOR_A
    dy0, dy1 = DOOR_Y
    s.clear([HP(da, 0, dy0), HP(db, 0, dy0), HP(db, 0, dy1), HP(da, 0, dy1)])                       # the doorway: its inside is a layer of its own
    # posts: the corners and the doorway's sides, a little proud of the wall
    for a in (0, da - 10, db, SIDE - 10):
        p = [HP(a, -2, y0), HP(a + 10, -2, y0), HP(a + 10, -2, y1), HP(a, -2, y1)]
        s.poly(p, mix(front_c, L["wood_dark"], 0.45))
        outline(s, p, 0.5, 0.5)
    # the lintel over the doorway, the sill under it
    s.poly([HP(da - 10, -2, dy1), HP(db + 10, -2, dy1), HP(db + 10, -2, dy1 + 14), HP(da - 10, -2, dy1 + 14)], mix(front_c, L["wood_dark"], 0.55))
    s.poly([HP(da - 10, -2, dy0 - 8), HP(db + 10, -2, dy0 - 8), HP(db + 10, -2, dy0), HP(da - 10, -2, dy0)], mix(front_c, L["wood_dark"], 0.45))
    outline(s, front, 0.8, 0.55)
    slips(s)
    # the deep eaves: their underside (rafters) in shade, seen from below
    e = EAVE_OUT
    e_fl, e_fr, e_bl = HP(-e, -e, y1), HP(SIDE + e, -e, y1), HP(-e, SIDE + e, y1)
    w_fl, w_fr, w_bl = HP(0, 0, y1), HP(SIDE, 0, y1), HP(0, SIDE, y1)
    under_c = mix(L["wood_sh"], L["inside_far"], 0.35)
    s.poly([w_fl, w_fr, e_fr, e_fl], under_c)
    s.poly([w_bl, w_fl, e_fl, e_bl], under_c)
    for k in range(1, 16):                                    # the rafters' ends
        a = -e + (SIDE + 2 * e) * k / 16
        s.line([HP(min(max(a, 0), SIDE), 0, y1), HP(a, -e, y1)], mix(under_c, L["wood_lit"], 0.25), 1.0, 0.7)
        s.line([HP(0, min(max(a, 0), SIDE), y1), HP(-e, a, y1)], mix(under_c, L["wood_lit"], 0.25), 1.0, 0.7)
    # the pyramid roof: its front face and its west face, the hips light lines, the eave's edge
    apex = HP(SIDE / 2, SIDE / 2, APEX_Y)
    lift = 12.0
    e_fl2, e_fr2, e_bl2 = HP(-e, -e, y1 + lift), HP(SIDE + e, -e, y1 + lift), HP(-e, SIDE + e, y1 + lift)
    n_front_roof = (N_FRONT[0], 0.75, N_FRONT[2])
    n_west_roof = (N_WEST[0], 0.75, N_WEST[2])
    front_roof = [e_fl2] + [HP(a, -e, y1) for a in np.linspace(-e + 40, SIDE + e - 40, 8)] + [e_fr2, apex]
    west_roof = [e_bl2] + [HP(-e, b_, y1) for b_ in np.linspace(SIDE + e - 40, -e + 40, 8)] + [e_fl2, apex]
    s.poly(west_roof, F(n_west_roof, L["tile"], L["tile_lit"], L["tile_sh"]))
    s.poly(front_roof, F(n_front_roof, L["tile"], L["tile_lit"], L["tile_sh"]))
    for k in range(1, 14):                                    # the tile rows running down each face
        t = k / 14
        a_ = -e + (SIDE + 2 * e) * t
        s.line([apex, HP(a_, -e, y1)], mix(F(n_front_roof, L["tile"], L["tile_lit"], L["tile_sh"]), LINE, 0.3), 0.6, 0.45)
        s.line([apex, HP(-e, a_, y1)], mix(F(n_west_roof, L["tile"], L["tile_lit"], L["tile_sh"]), LINE, 0.3), 0.6, 0.45)
    s.line([e_fl2] + [HP(a, -e, y1) for a in np.linspace(-e + 40, SIDE + e - 40, 8)] + [e_fr2], L["tile_edge"], 1.4, 0.9)
    s.line([e_bl2] + [HP(-e, b_, y1) for b_ in np.linspace(SIDE + e - 40, -e + 40, 8)] + [e_fl2], L["tile_edge"], 1.4, 0.9)
    for c_ in (e_fl2, e_fr2, e_bl2):                          # the hips
        s.line([c_, apex], L["tile_edge"], 2.0, 0.9)
    outline(s, front_roof, 0.8, 0.55)
    outline(s, west_roof, 0.8, 0.55)
    # the finial: a jewel in a lotus cup on the peak (finial(), below)
    finial(s, apex)
    # the step before the doors: one broad dressed stone
    st0, st1 = DOOR_A[0] - 30, DOOR_A[1] + 30
    tr = [HP(st0, -bo - 70, 22), HP(st1, -bo - 70, 22), HP(st1, -bo, 22), HP(st0, -bo, 22)]
    rs = [HP(st0, -bo - 70, 0), HP(st1, -bo - 70, 0), HP(st1, -bo - 70, 22), HP(st0, -bo - 70, 22)]
    s.poly(rs, F(N_FRONT, L["stone"], L["stone_lit"], L["stone_sh"]))
    s.poly(tr, L["stone_lit"] if LIGHT == "gold" else L["stone"])
    outline(s, rs + [tr[3], tr[2]][::-1][:0], 0.6, 0.55)
    outline(s, tr, 0.6, 0.55)


def finial(s, apex):
    """The roof's finial, as a Buddhist hall carries it: a wish-granting jewel (hoju), round below and drawn up to a point
    like an onion, of dark bronze, sitting directly in a small lotus cup on the peak. No stem, no plate, nothing across:
    the cup is narrower than the jewel's swell, so that nothing stands out sideways (PAINT-21E fix, at the lead's word: a
    cross on a Buddhist hall of 1830 would be wrong). Small (the jewel 26 x 32 cm, the cup 20 cm across), in flats: one
    bronze flat, its lit flat toward the sun at the left, a fine contour."""
    ax, ay = apex
    k = k_at(H_(SIDE / 2, SIDE / 2)[1])                       # pixels to the cm at the peak
    W_, H_j = 26.0 * k, 32.0 * k                              # the jewel
    cw, ch = 20.0 * k, 9.0 * k                                # the cup
    bronze = mix(L["wood_dark"], LINE, 0.2)
    lit = mix(bronze, L["sun"], 0.5 if LIGHT == "gold" else 0.62)
    foot = ay - ch * 0.55                                     # the jewel's foot, down inside the cup
    prof = [(0.00, 0.00), (0.26, 0.03), (0.40, 0.12), (0.47, 0.26), (0.48, 0.38), (0.43, 0.52), (0.33, 0.66), (0.20, 0.80),
            (0.09, 0.91), (0.00, 1.00)]                       # half-width (of W_) and height (of H_j) from the foot to the point
    right = [(ax + u * W_, foot - v * H_j) for (u, v) in prof]
    left = [(ax - u * W_, foot - v * H_j) for (u, v) in prof[::-1]]
    jewel = right + left[1:-1]
    s.poly(jewel, bronze)
    s.poly([(ax - u * W_ * 0.94, foot - v * H_j) for (u, v) in prof[1:9]] + [(ax - 0.12 * W_, foot - 0.62 * H_j), (ax - 0.16 * W_, foot - 0.30 * H_j)], lit, 0.85)
    s.ellipse(ax - 0.22 * W_, foot - 0.50 * H_j, max(0.8, 0.07 * W_), max(0.8, 0.09 * H_j), mix(lit, PAPER, 0.4), 0.8)
    outline(s, jewel, 0.8, 0.7)
    # the lotus cup, in front of the jewel's foot: a small bowl, its rim three petal points
    rim = ay - ch
    top = []
    for i in range(3):
        x0 = ax - cw / 2 + cw * i / 3
        x1 = ax - cw / 2 + cw * (i + 1) / 3
        top += [(x0, rim), ((x0 + x1) / 2, rim - ch * 0.38)]
    top.append((ax + cw / 2, rim))
    bowl = [(ax + cw / 2 * math.cos(t), rim + ch * math.sin(t)) for t in np.linspace(0.0, math.pi, 12)]
    cup = top + bowl[1:-1]
    s.poly(cup, mix(bronze, LINE, 0.12))
    for i in range(3):                                        # the petals' faces, a shade lighter on the lit side
        x0 = ax - cw / 2 + cw * i / 3
        x1 = ax - cw / 2 + cw * (i + 1) / 3
        tone = mix(bronze, L["sun"], 0.32 if i == 0 else 0.18)
        s.poly([(x0 + 0.4, rim + 0.3), ((x0 + x1) / 2, rim - ch * 0.30), (x1 - 0.4, rim + 0.3), ((x0 + x1) / 2, rim + ch * 0.62)], tone, 0.9)
    outline(s, cup, 0.8, 0.7)


def inside_hall(s):
    """What the open doors show (in the backdrop, behind the door cut-outs): the dim hall, its boards, at the back the
    small shut cabinet on its stand, and the bars of light from the west lattice lying across the floor from the left.
    (Drawn on a sheet of its own and kept to the doorway.)"""
    da, db = DOOR_A
    dy0, dy1 = DOOR_Y
    s.poly([HP(da - 40, 0, dy0 - 40), HP(db + 40, 0, dy0 - 40), HP(db + 40, 0, dy1 + 40), HP(da - 40, 0, dy1 + 40)], L["inside"])
    # the far wall seen through the doorway: dark boards, the cabinet on its stand, a lamp's dark shape
    s.poly([HP(da, SIDE, dy0), HP(db, SIDE, dy0), HP(db, SIDE, dy1), HP(da, SIDE, dy1)], L["inside_far"])
    s.poly([HP(da, 40, dy0), HP(db, 40, dy0), HP(db, SIDE, dy0), HP(da, SIDE, dy0)], L["inside"])       # the floor
    cab = [HP(160, SIDE - 6, dy0 + 40), HP(204, SIDE - 6, dy0 + 40), HP(204, SIDE - 6, dy0 + 120), HP(160, SIDE - 6, dy0 + 120)]
    s.poly([HP(150, SIDE - 4, dy0), HP(214, SIDE - 4, dy0), HP(214, SIDE - 4, dy0 + 40), HP(150, SIDE - 4, dy0 + 40)], mix(L["inside"], L["wood"], 0.35))
    s.poly(cab, mix(L["inside"], L["wood_dark"], 0.3))
    s.line([HP(182, SIDE - 7, dy0 + 42), HP(182, SIDE - 7, dy0 + 118)], mix(L["inside"], L["sun"], 0.25), 0.8)
    # the east wall's inner face (seen at the right of the doorway's view, as we look in toward the north-east)
    s.poly([HP(SIDE - 2, 40, dy0), HP(SIDE - 2, SIDE, dy0), HP(SIDE - 2, SIDE, dy1), HP(SIDE - 2, 40, dy1)], mix(L["inside"], L["inside_far"], 0.5))
    # the bars of light from the west lattice: across the floor toward the front and the east, then up the east wall
    for j in range(4):
        b0 = 150 + j * 30
        floor_bar = [HP(60, b0, dy0 + 1), HP(SIDE - 2, b0 - 150, dy0 + 1), HP(SIDE - 2, b0 - 136, dy0 + 1), HP(60, b0 + 14, dy0 + 1)]
        s.poly(floor_bar, L["bar"], 0.55)
        wall_bar = [HP(SIDE - 3, b0 - 150, dy0 + 1), HP(SIDE - 3, b0 - 136, dy0 + 1), HP(SIDE - 3, b0 - 120, dy0 + 120), HP(SIDE - 3, b0 - 134, dy0 + 120)]
        s.poly(wall_bar, L["bar"], 0.75)


SLIPS = []                                                    # (a, y, w, h, tone) on the front, built once


def build_slips():
    rng = np.random.default_rng(57)
    out = []
    da, db = DOOR_A
    # round the doorway: on the panels either side and on the posts, many, old and new, some overlapping
    for (a0, a1) in ((14, da - 12), (db + 12, SIDE - 14)):
        for i in range(13):
            a = rng.uniform(a0, a1 - 8)
            y = rng.uniform(80, 236)
            out.append((a, y, rng.uniform(6, 8), rng.uniform(18, 26), rng.random()))
    for a in (da - 10, db, 0, SIDE - 10):                     # up the posts
        for i in range(6):
            out.append((a + 1, 70 + i * 30 + rng.uniform(-3, 3), 8, rng.uniform(16, 22), rng.random()))
    for i in range(9):                                        # on the lintel
        out.append((da + 2 + i * 19, 250, 8, 11, rng.random()))
    return out


def slips(s):
    """The name slips pasted round the doors and on the posts: paper and thin wood, old and new (the new white, the
    old yellowed and greyed), each with a few ink marks of our own (no real text)."""
    global SLIPS
    if not SLIPS:
        SLIPS = build_slips()
    for (a, y, w, h, t) in SLIPS:
        tone = L["paper"] if t < 0.45 else (L["paper_old"] if t < 0.85 else mix(L["wood_lit"], L["paper"], 0.5))
        p = [HP(a, -3, y), HP(a + w, -3, y), HP(a + w, -3, y + h), HP(a, -3, y + h)]
        s.poly(p, tone)
        cx = HP(a + w / 2, -3.5, y + h * 0.75)
        cy2 = HP(a + w / 2, -3.5, y + h * 0.25)
        s.line([cx, cy2], L["ink"], 0.6, 0.55)


# ---------------------------------------------------------------- the cut-outs
def doors(s, state="shut"):
    """The double doors (Kannon-opening: they part in the middle and swing outward): each leaf a frame round a fine
    lattice, the dim hall seen through the bars. shut / half (each leaf turned 45 degrees out) / open (turned flat back
    toward us, against the front)."""
    da, db = DOOR_A
    dy0, dy1 = DOOR_Y
    mid = (da + db) / 2
    leaf_w = (db - da) / 2
    ang = {"shut": 0.0, "half": 45.0, "open": 86.0}[state]
    for side in (-1, 1):
        hinge = da if side < 0 else db
        sgn = 1 if side < 0 else -1                           # the leaf runs from its hinge toward the middle
        th = math.radians(ang)
        # the leaf's free edge: from the hinge, along the front by cos, out toward us by sin
        fa = hinge + sgn * leaf_w * math.cos(th)
        fb = -leaf_w * math.sin(th) - 2
        corners = [HP(hinge, -2, dy0), HP(fa, fb, dy0), HP(fa, fb, dy1), HP(hinge, -2, dy1)]
        n_leaf = (N_FRONT[0] * math.cos(th) + sgn * UX * math.sin(th) * 0.0, 0, N_FRONT[2])
        frame_c = F(N_FRONT, L["wood"], L["wood_lit"], L["wood_sh"]) if ang < 60 else (L["wood_sh"] if side < 0 else F(N_FRONT, L["wood"], L["wood_lit"], L["wood_sh"]))
        s.poly(corners, frame_c)
        # the lattice: the inner panel dark, crossed by fine bars
        def at(u, y):
            a = hinge + sgn * leaf_w * u * math.cos(th)
            b = -leaf_w * u * math.sin(th) - 2.5
            return HP(a, b, y)
        inner = [at(0.12, dy0 + 14), at(0.88, dy0 + 14), at(0.88, dy1 - 12), at(0.12, dy1 - 12)]
        s.poly(inner, L["inside"])
        for k in range(1, 7):
            u = 0.12 + 0.76 * k / 7
            s.line([at(u, dy0 + 14), at(u, dy1 - 12)], frame_c, 1.2)
        for k in range(1, 12):
            y = dy0 + 14 + (dy1 - dy0 - 26) * k / 12
            s.line([at(0.12, y), at(0.88, y)], frame_c, 1.0)
        outline(s, corners, 0.7, 0.6)
        # the hasp's plate on each leaf at the middle (shut): an iron strap
        if ang == 0:
            ha = [at(0.80, 140), at(1.0, 140), at(1.0, 150), at(0.80, 150)]
            s.poly(ha, mix(L["wood_dark"], LINE, 0.4))


LOCK_AT = (180.0, 145.0)            # the lock on the hasp: the doors' middle (a), height (y)


def lock(s, state="shut"):
    """The shipwright's lock on the hasp, small (the close-up is where it is seen): a block of dark wood bound with
    iron, its bolt through the staple. Open: the bolt drawn, the lock hanging from the staple on one side."""
    a, y = LOCK_AT
    if state == "shut":
        body = [HP(a - 9, -5, y - 4), HP(a + 9, -5, y - 4), HP(a + 9, -5, y + 4), HP(a - 9, -5, y + 4)]
        s.poly(body, mix(L["wood_dark"], LINE, 0.3))
        s.line([HP(a - 9, -5.5, y - 4), HP(a - 9, -5.5, y + 4)], mix(L["sun"], L["wood_dark"], 0.45), 1.0)       # its iron band
        s.line([HP(a + 9, -5.5, y - 4), HP(a + 9, -5.5, y + 4)], mix(L["sun"], L["wood_dark"], 0.45), 1.0)
        s.line([HP(a - 4, -5.5, y + 1), HP(a + 3, -5.5, y + 2)], mix(L["sun"], L["wood_dark"], 0.6), 0.8)          # the rabbit's back, a glint
        outline(s, body, 0.5, 0.7)
    else:
        body = [HP(a + 2, -5, y - 12), HP(a + 18, -5, y - 12), HP(a + 18, -5, y - 4), HP(a + 2, -5, y - 4)]
        s.line([HP(a, -5, y), HP(a + 4, -5, y - 5)], L["wood_dark"], 1.0)
        s.poly(body, mix(L["wood_dark"], LINE, 0.3))
        outline(s, body, 0.5, 0.7)


def stepball(s):
    """O-Ume's rice ball for the voice, on a leaf on the step: bale-shaped, white, on a broad green leaf."""
    a = (DOOR_A[0] + DOOR_A[1]) / 2 + 26
    b = -30 - 36
    y = 22.0
    leaf = [HP(a - 14, b - 9, y + 0.5), HP(a + 2, b - 13, y + 0.5), HP(a + 16, b - 4, y + 0.5), HP(a + 2, b + 10, y + 0.5), HP(a - 12, b + 5, y + 0.5)]
    s.poly(leaf, L["leaf"])
    s.line([HP(a - 14, b - 9, y + 0.6), HP(a + 16, b - 4, y + 0.6)], mix(L["leaf"], PAPER, 0.3), 0.7)
    cx, cy = HP(a, b - 1, y + 4)
    k = k_at(H_(a, b)[1])
    rx, ry = 6.5 * k * 1.5, 4.2 * k * 1.5
    s.ellipse(cx, cy, rx, ry, L["rice"])
    s.ellipse(cx - rx * 0.25, cy - ry * 0.3, rx * 0.55, ry * 0.45, mix(L["rice"], PAPER, 0.5))
    s.ellipse(cx + rx * 0.3, cy + ry * 0.2, rx * 0.5, ry * 0.4, shade_of(L["rice"], 0.18), 0.6)
    outline(s, [(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 16, endpoint=False)], 0.5, 0.55)


STONE = (-252.0, 1440.0)            # the stone at the path's foot (X, D)


def stone(s):
    """The small stone at the foot of the east path: a rough upright slab, its face dressed and cut with a few lines of
    writing (our own marks: not a real inscription), a little moss at its foot."""
    X, D = STONE
    w, h, t = 34.0, 104.0, 18.0
    face = [P(X - w / 2, 0, D), P(X + w / 2, 0, D), P(X + w / 2 - 2, h, D), P(X, h + 8, D), P(X - w / 2 + 1, h - 2, D)]
    side = [P(X - w / 2, 0, D), P(X - w / 2, 0, D + t), P(X - w / 2 + 1, h - 2, D + t), P(X - w / 2 + 1, h - 2, D)]
    s.poly(side, F((-1, 0, 0), L["stone"], L["stone_lit"], L["stone_sh"]))
    s.poly(face, F((0.2, 0, -1), L["stone"], L["stone_lit"], L["stone_sh"]))
    # two columns of cut signs (our own), down from the top: short verticals, dots, ticks and hooks, each apart from the
    # next; no cut crosses another (PAINT-21E fix: in 1830 the cross was the forbidden sign, and nothing may read as one)
    rng = np.random.default_rng(64)
    ink = mix(L["stone_sh"], LINE, 0.45)
    for col_ in (-7.0, 6.0):
        yy = h - 12.0
        while True:
            kind = ("vert", "vert", "dot", "tick", "hook")[int(rng.integers(5))]
            ln = {"vert": rng.uniform(8.0, 11.0), "dot": 3.0, "tick": 6.0, "hook": rng.uniform(8.0, 10.0)}[kind]
            if yy - ln < 22.0:
                break
            if kind == "vert":
                s.line([P(X + col_, yy, D - 0.5), P(X + col_, yy - ln, D - 0.5)], ink, 1.0, 0.85)
            elif kind == "dot":
                s.ellipse(*P(X + col_, yy - ln / 2, D - 0.5), 1.0, 0.9, ink, 0.85)
            elif kind == "tick":
                s.line([P(X + col_ - 2.0, yy, D - 0.5), P(X + col_ + 2.0, yy - ln, D - 0.5)], ink, 0.9, 0.8)
            else:
                s.line([P(X + col_, yy, D - 0.5), P(X + col_, yy - ln * 0.78, D - 0.5), P(X + col_ - 2.5, yy - ln, D - 0.5)], ink, 0.9, 0.85)
            yy -= ln + rng.uniform(4.5, 6.0)
    s.ellipse(*P(X, 2, D - 2), 12, 3, L["grass_sh"])
    outline(s, face, 0.7, 0.6)
    outline(s, side, 0.6, 0.5)


BENCH_X, BENCH_D = (300.0, 500.0), 1300.0


def bench(s):
    """The bench where the women wait: a long plain plank on four legs, worn."""
    x0, x1 = BENCH_X
    d = BENCH_D
    top = [P(x0, 42, d), P(x1, 42, d), P(x1, 42, d + 34), P(x0, 42, d + 34)]
    edge = [P(x0, 36, d), P(x1, 36, d), P(x1, 42, d), P(x0, 42, d)]
    for xl in (x0 + 10, x1 - 16):
        for dl in (d + 4, d + 28):
            s.poly([P(xl, 0, dl), P(xl + 6, 0, dl), P(xl + 6, 36, dl), P(xl, 36, dl)], L["wood_dark"])
    s.poly(top, F((0, 1, 0), L["wood"], L["wood_lit"], L["wood_sh"]))
    s.poly(edge, F((0, 0, -1), L["wood"], L["wood_lit"], L["wood_sh"]))
    outline(s, edge + [top[2], top[3]][::-1][:0], 0.6, 0.6)
    outline(s, top, 0.6, 0.55)


COMBS = (448.0, 1210.0)             # the heap of combs and pins on its cloth (X, D)


def combs(s):
    """The heap of failed combs and hairpins on a faded cloth on the ground by the bench: half-moon combs of boxwood
    (honey), of tortoiseshell (mottled brown), of black lacquer, and pins (thin sticks, a bead or a flower at the end)."""
    rng = np.random.default_rng(58)
    X, D = COMBS
    cl = [P(X - 40, 0.5, D - 26), P(X + 40, 0.5, D - 30), P(X + 46, 0.5, D + 26), P(X - 38, 0.5, D + 30)]
    s.poly(cl, L["cloth"])
    outline(s, cl, 0.5, 0.5)
    k = k_at(D)
    for i in range(26):
        x = X + rng.uniform(-28, 28)
        d = D + rng.uniform(-16, 18)
        cx, cy = P(x, 2 + rng.uniform(0, 6), d)
        r = rng.uniform(4.0, 5.5) * k * 1.4
        tone = [L["boxwood"], L["shell"], L["lacquer"]][int(rng.integers(3))]
        if rng.random() < 0.6:                                 # a half-moon comb
            pts = [(cx + r * math.cos(t), cy - r * 0.6 * math.sin(t)) for t in np.linspace(0, math.pi, 8)]
            s.poly(pts + [(cx - r, cy + 1.2), (cx + r, cy + 1.2)], tone)
            s.line([(cx - r * 0.8, cy + 0.6), (cx + r * 0.8, cy + 0.6)], mix(tone, LINE, 0.35), 0.6)
        else:                                                  # a pin
            a = rng.uniform(-0.6, 0.6)
            ln = rng.uniform(9, 13) * k * 1.4
            s.line([(cx, cy), (cx + ln * math.cos(a), cy + ln * math.sin(a) * 0.4)], mix(L["sun"], L["wood_dark"], 0.4), 0.9)
            s.ellipse(cx, cy, 1.4, 1.4, [L["red"], L["paper"], L["boxwood"]][int(rng.integers(3))])


def near_pine(s):
    """A pine near us at the left edge, cut by the frame (the front plane: we see past it; its pads stir, fx sway): a
    straight dark trunk, its bark lit at the left, and flat layered pads reaching in over the top-left."""
    rng = np.random.default_rng(59)
    trunk = curve([(24, 612), (27, 480), (26, 360), (31, 240), (33, 130), (38, 30), (40, -12)], 6)
    s.taper(trunk, L["trunk"], 40, 26)
    lit_c = L["trunk_lit"] if LIGHT == "gold" else mix(PAINT["orange"], PAINT["vermilion"], 0.4)
    s.taper([(p[0] - 11, p[1]) for p in trunk], lit_c, 9, 6, 0.85)
    for k in range(14):                                       # bark plates
        y = rng.uniform(40, 590)
        x = float(np.interp(y, [p[1] for p in trunk][::-1], [p[0] for p in trunk][::-1]))
        s.line([(x - 6, y), (x + 4, y + 3)], mix(L["trunk"], LINE, 0.4), 1.0, 0.7)
    s.line([(p[0] + 19, p[1]) for p in trunk], LINE, 0.9, 0.55)
    s.line([(p[0] - 19, p[1]) for p in trunk], LINE, 0.8, 0.4)
    # the pads reaching in over the top-left: flat masses of needles on short dark limbs
    for (x0, y0, x1, y1, rx) in ((40, 132, 118, 112, 62), (42, 66, 150, 44, 72), (44, 14, 116, 6, 54), (36, 190, 88, 176, 36)):
        s.line([(x0, y0), (x1 - rx * 0.4, y1 + 6)], L["trunk"], 3.4)
        pad(s, x1, y1, rx, rng)


def pad(s, cx, cy, rx, rng, dark=None, lit=None):
    """A pine's pad of needles, flat: a few overlapping lobes in one dark flat, its top toward the light a shade
    lighter, a fringe of short needle strokes along its underside."""
    dark = L["pine"] if dark is None else dark
    lit = L["pine_lit"] if lit is None else lit
    ry = rx * 0.26
    lobes = [(cx - rx * 0.55, cy + ry * 0.15, rx * 0.5), (cx, cy - ry * 0.25, rx * 0.62), (cx + rx * 0.5, cy + ry * 0.1, rx * 0.5)]
    for (lx, ly, lr) in lobes:
        s.ellipse(lx, ly, lr, lr * 0.42, dark)
    for (lx, ly, lr) in lobes:
        if LIGHT == "gold":
            s.ellipse(lx - lr * 0.15, ly - lr * 0.16, lr * 0.68, lr * 0.2, lit, 0.55)
        else:
            s.line([(lx - lr * 0.8, ly + lr * 0.3), (lx + lr * 0.6, ly + lr * 0.36)], mix(PAINT["orange"], PAINT["lake"], 0.3), 1.0, 0.7)
    for i in range(int(rx * 0.7)):                            # the needles' fringe under the pad
        x = cx - rx + 2 * rx * rng.random()
        y = cy + ry * 0.55 + rng.uniform(-1.5, 1.5)
        s.line([(x, y), (x + rng.uniform(-2, 2), y + rng.uniform(3, 6))], dark, 1.0, 0.85)


# ---------------------------------------------------------------- cast shadows
def shadows(pic):
    """The cast shadows on the ground, from the light's sun: the hall's, the hut's, the stone's, the bench's, the
    trees'. Gold: moderate, to the right and a little away. Sunset: very long, to the right and toward us; most of the
    terrace in shade, with a few long streaks of red light lying through the gaps between the trees."""
    cx, cd = cast_of(LIGHT)
    s = Sheet(SHAPE)

    def sh(points_xyd):
        """The shadow of a set of world points (X, Y, D) on the ground: the hull of the points and their shadows."""
        pts = []
        for (X, Y, D) in points_xyd:
            pts.append((X, D))
            pts.append((X + cx * Y, D + cd * Y))
        pts = [p for p in pts if p[1] > 300]
        if len(pts) < 3:
            return
        from scipy.spatial import ConvexHull
        arr = np.array(pts)
        hv = arr[ConvexHull(arr).vertices]
        s.poly([P(x, 0, d) for x, d in hv], L["cast"])
    # the hall: its walls' top corners and the eaves' corners, the apex
    hall_pts = []
    for (a, b) in ((0, 0), (SIDE, 0), (0, SIDE), (SIDE, SIDE)):
        X, D = H_(a, b)
        hall_pts.append((X, 0, D))
    for (a, b) in ((-EAVE_OUT, -EAVE_OUT), (SIDE + EAVE_OUT, -EAVE_OUT), (-EAVE_OUT, SIDE + EAVE_OUT), (SIDE + EAVE_OUT, SIDE + EAVE_OUT)):
        X, D = H_(a, b)
        hall_pts.append((X, EAVE_Y, D))
    X, D = H_(SIDE / 2, SIDE / 2)
    hall_pts.append((X, APEX_Y, D))
    sh(hall_pts)
    x0, x1 = HUTX
    d0, d1 = HUT_D
    sh([(x0, 0, d0), (x1, 0, d0), (x0, 0, d1), (x1, 0, d1), (x0 - 50, 190, d0 - 60), (x1 + 50, 190, d0 - 60), (x0 + 40, 330, (d0 + d1) / 2), (x1 - 40, 330, (d0 + d1) / 2)])
    X, D = STONE
    sh([(X - 17, 0, D), (X + 17, 0, D), (X, 108, D), (X - 17, 0, D + 18)])
    bx0, bx1 = BENCH_X
    sh([(bx0, 0, BENCH_D), (bx1, 0, BENCH_D), (bx0, 42, BENCH_D), (bx1, 42, BENCH_D), (bx0, 42, BENCH_D + 34), (bx1, 42, BENCH_D + 34)])
    if LIGHT == "sunset":
        # the trees at the left throw their shadows across everything: the terrace in shade but for a few streaks of light
        s.poly([(-10, 330), (810, 330), (810, 610), (-10, 610)], L["cast"])
        c, a = s.done()
        streaks = Sheet(SHAPE)
        for (y0, w) in ((488, 7), (522, 10), (560, 14), (452, 9)):
            streaks.poly([(-10, y0 - 30), (300, y0 - 8), (820, y0 + 26), (820, y0 + 26 + w), (300, y0 - 8 + w * 0.7), (-10, y0 - 30 + w * 0.5)], "#ffffff")
        _, sa = streaks.done()
        a = np.clip(a - sa * (np.asarray(grid(SHAPE)[1]) > 420), 0, 1)
        tint(pic, L["cast"], blur(a, 0.5) * 0.62)
        over(pic, L["ground_lit"], (sa * (np.asarray(grid(SHAPE)[1]) > 420) * 0.55).astype(F32))
        return pic
    c, a = s.done()
    tint(pic, L["cast"], blur(a, 0.5) * L["cast_amt"])
    return pic


# ---------------------------------------------------------------- the passes
def under():
    pic = sky_layer()
    layers = {}
    for name, fn, amt in (("plain", plain, 0.0), ("mountain", mountain, 0.4), ("mist", mist, 0.6)):
        lay = sheet_layer(fn, amt)
        lay.onto(pic)
        layers[name] = lay
    glade(pic)
    for name, fn, amt in (("trees", slope_trees, 0.3), ("cherry", cherry, 0.3)):
        lay = sheet_layer(fn, amt)
        lay.onto(pic)
        layers[name] = lay
    terrace(pic)
    ins = sheet_layer(inside_hall, 0.0)
    da, db = DOOR_A
    dy0, dy1 = DOOR_Y
    dm = mask_poly(SHAPE, [HP(da, 0, dy0), HP(db, 0, dy0), HP(db, 0, dy1), HP(da, 0, dy1)])
    ins.a *= dm
    ins.c *= dm[..., None]
    ins.onto(pic)
    layers["inside"] = ins
    for name, fn, amt in (("path", path, 0.25), ("hut", hut, 0.25), ("hall", hall, 0.2), ("combs", combs, 0.1)):
        lay = sheet_layer(fn, amt)
        lay.onto(pic)
        layers[name] = lay
    shadows(pic)
    return np.clip(pic, 0, 1), layers


def details(pic, layers):
    crisp = pic.copy()
    for name in ("plain", "hut", "hall", "path", "combs", "inside"):
        layers[name].onto(crisp)
    pic[...] = lerp(pic, crisp, 0.80)
    return pic


CUTS = ["doors", "lock", "stepball", "stone", "bench", "pine"]                    # back to front, as the scene lists them
ALTS = ["doors-half", "doors-open", "lock-open"]


def cut_layers():
    return {
        "doors": sheet_layer(lambda s: doors(s, "shut"), 0.1),
        "doors-half": sheet_layer(lambda s: doors(s, "half"), 0.1),
        "doors-open": sheet_layer(lambda s: doors(s, "open"), 0.1),
        "lock": sheet_layer(lambda s: lock(s, "shut"), 0.0),
        "lock-open": sheet_layer(lambda s: lock(s, "open"), 0.0),
        "stepball": sheet_layer(stepball, 0.0),
        "stone": sheet_layer(stone, 0.2),
        "bench": sheet_layer(bench, 0.15),
        "pine": sheet_layer(near_pine, 0.3),
    }


def paint_light(name, fast):
    set_light(name)
    t0 = time.time()
    base, layers = under()
    pic = base.copy() if fast else strokes(base, sizes=(10, 5, 3), seed=3, density=1.4, jitter=0.022, keep=0.42)
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
            c, a = brushed(layer, ground_, seed=60 + i, sizes=(5, 3, 2), restate=0.92 if n not in ("pine",) else 0.8)
        cut[n] = (c, a)
        if n in CUTS:
            over(whole, c, a)
    print(name, "painted", round(time.time() - t0, 1))
    return pic, cut, whole


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = len(sys.argv) > 1 and sys.argv[1] == "fast"
    results = {}
    for name in ("gold", "sunset"):
        pic, cut, whole = paint_light(name, fast)
        to_png(whole, f"{OUT}-2-{name}.png")
        results[name] = (pic, cut)
    if fast:
        sys.exit()
    pic, cut = results["gold"]
    print("back", finish(pic, f"{OUT}/back.png", 160)[0])
    for n, (c, a) in cut.items():
        print(n, finish(c, f"{OUT}/{n}.png", 64, a)[0])
    pic, cut = results["sunset"]
    print("sunset", finish(pic, f"{OUT}/sunset.png", 160)[0])
    for n, (c, a) in cut.items():
        print(n + "-sunset", finish(c, f"{OUT}/{n}-sunset.png", 64, a)[0])
    import edo_shosha_layout as LY
    LY.write(f"{OUT}/layout.json")
    for name, back in (("gold", "back"), ("sunset", "sunset")):
        comp = Image.open(f"{OUT}/{back}.png").convert("RGBA")
        for n in CUTS:
            comp.alpha_composite(Image.open(f"{OUT}/{n}{'' if name == 'gold' else '-sunset'}.png").convert("RGBA"))
        comp.convert("RGB").save(f"{OUT}-comp-{name}.png")
    print("done", round(time.time() - t0, 1))

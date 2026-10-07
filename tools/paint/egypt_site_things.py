"""The things that stand on the sand in egypt_site.py: the scribe's station under its awning, the sledge
with its block, the waiting blocks at the front, and the windshield shade. Each has a part painted into
the backdrop (what lies on the ground, and shadows) and a part that is a cut-out people walk behind."""

import math

import numpy as np

from egypt_site_kit import *
from egypt_site_plan import *
import flora
import egypt_site_props as props

MW, MD, MT = MAT["wide"], MAT["deep"], MAT["tall"]
BLOCK_U, BLOCK_V, BLOCK_D = (42.0, 208.0), (33.0, 131.0), (8.0, 108.0)      # the block on the sledge, in the sledge's own measure
RUNNERS = (0.0, 236.0, 116.0)                                               # from, to, across
STONE = dict(top="#fff2cc", front="#ecd09c", left="#fbe3b0", side="#a99aa6", joint="#7d6258", chip="#fffbe8")


def mat_frame():
    return Frame(MAT["at"], MAT["turn"])


def sledge_frame():
    return Frame(SLEDGE["at"], SLEDGE["turn"])


def stack_frame():
    return Frame(STACK["at"], STACK["turn"])


# ---------------------------------------------------------------- shadows (painted into the backdrop)
def awning_shadow(shape):
    """The shade the awning and its side cloth throw across the mat and on to the right."""
    m = mat_frame()
    cloth = [m.w(u, MT, d) for u in (-10, MW + 12) for d in (-14, MD + 8)]
    flap = [m.w(-8, v, d) for v in (70, MT) for d in (0, MD)]
    out = np.maximum(mask_poly(shape, hull(shade_of(cloth)), soft=2.2), mask_poly(shape, hull(shade_of(flap)), soft=1.6))
    for u in (0, MW):
        for d in (0, MD):
            out = np.maximum(out, mask_line(shape, [m.pt(u, 0, d), shade_of([m.w(u, MT, d)])[0]], 2.2, soft=0.8))
    return out


def sledge_shadow(shape):
    sl = sledge_frame()
    a = cast_box(shape, sl, BLOCK_U[0], BLOCK_U[1], BLOCK_V[1], BLOCK_D[0], BLOCK_D[1], soft=1.6)
    b = cast_box(shape, sl, RUNNERS[0] - 24, RUNNERS[1], BLOCK_V[0], 0, RUNNERS[2], soft=1.2)
    return np.maximum(a, b)


def cutout(shape, base, lines, back, seed, fast=False, sizes=(7, 4, 2), keep=0.42, density=1.8):
    """A finished cut-out from two sheets: `base` (its big planes) is brushed, then `lines` (the crisp
    things) goes back on top, as the wagon is done. Only the part of the picture it covers is worked."""
    color, alpha = base.done()
    lc, la = lines.done()
    whole = np.maximum(alpha, la)
    ys, xs = np.nonzero(whole > 0.02)
    out = np.zeros(shape + (3,), dtype=F32)
    out[...] = rgb(back)
    if len(xs) == 0:
        return out, whole
    y0, y1, x0, x1 = max(ys.min() - 12, 0), min(ys.max() + 12, shape[0]), max(xs.min() - 12, 0), min(xs.max() + 12, shape[1])
    flat = out[y0:y1, x0:x1].copy()
    over(flat, color[y0:y1, x0:x1], alpha[y0:y1, x0:x1])
    painted = flat if fast else strokes(flat, sizes=sizes, seed=seed, density=density, jitter=0.03, keep=keep)
    over(painted, lc[y0:y1, x0:x1], la[y0:y1, x0:x1])
    out[y0:y1, x0:x1] = painted
    return out, np.clip(whole, 0, 1)


# ---------------------------------------------------------------- the scribe's station
def station_under(sheet):
    """The reed mat, flat on the sand (its weave comes later)."""
    m = mat_frame()
    m.poly(sheet, [(0, 0, 0), (MW, 0, 0), (MW, 0, MD), (0, 0, MD)], props.REED[2])
    m.poly(sheet, [(0, 0, 0), (MW, 0, 0), (MW, 0, 26), (0, 0, 26)], props.REED[3], 0.35)
    return sheet


def station(sheet, seed=31):
    """What stands on the mat behind the awning's near poles: the far poles, the scribe's chest with his
    palette, jars of rolled papyrus, the sherds he tallies on, and the day's wages in bread and beer."""
    rng = np.random.default_rng(seed)
    m = mat_frame()
    for d in np.arange(5, MD, 8.5):                                         # the reeds of the mat
        m.line(sheet, [(2, 0, d), (MW * 0.5, 0, d + rng.normal(0, 0.8)), (MW - 2, 0, d)], props.REED[0], 0.7, 0.20 + 0.12 * rng.random())
    for u in (5, 56, 106, 156, 206, MW - 5):                                # the cords that bind them
        m.line(sheet, [(u, 0, 1), (u + rng.normal(0, 1), 0, MD - 1)], props.REED[0], 0.9, 0.55)
        m.line(sheet, [(u + 2.5, 0, 1), (u + 2.5, 0, MD - 1)], props.REED[3], 0.7, 0.35)
    m.line(sheet, [(0, 0, 0), (MW, 0, 0), (MW, 0, MD), (0, 0, MD), (0, 0, 0)], props.REED[0], 1.0, 0.6)
    for d in np.arange(4, MD, 11):                                          # frayed ends
        m.line(sheet, [(MW, 0, d), (MW + 5 + rng.random() * 5, 0, d + rng.normal(0, 2))], props.REED[1], 0.7, 0.7)
        m.line(sheet, [(0, 0, d), (-4 - rng.random() * 5, 0, d + rng.normal(0, 2))], props.REED[2], 0.7, 0.7)
    for u in (0, MW):                                                       # the far poles
        props.log(sheet, m.pt(u, 0, MD), m.pt(u, MT + 4, MD), 3.0)
    # the wages, at the back: baskets of bread, loaves stacked beside them
    props.basket(sheet, *m.pt(42, 0, 204), 22, 13, loaves=7, seed=1)
    props.basket(sheet, *m.pt(86, 0, 224), 17, 10, loaves=4, seed=2)
    props.loaf(sheet, *m.pt(118, 0, 228), 4.6)
    props.loaf(sheet, *m.pt(128, 0, 218), 4.2)
    # jars of rolled papyrus, back right
    props.rolls(sheet, *m.pt(200, 0, 224), 21, n=3, seed=4)
    props.rolls(sheet, *m.pt(228, 0, 206), 24, n=4, seed=3)
    # his chest, and the palette on it: two cakes of ink, black and red, and his pens
    m.box(sheet, 142, 214, 0, 30, 120, 160, front="#8a623c", top="#cba56c", left="#b08450", right="#6e4c30")
    m.line(sheet, [(142, 22, 120), (214, 22, 120)], "#5a3c24", 0.8, 0.8)
    m.line(sheet, [(142, 30, 120), (214, 30, 120)], "#ecd09a", 0.9, 0.9)
    m.poly(sheet, [(150, 30.5, 131), (188, 30.5, 131), (188, 30.5, 141), (150, 30.5, 141)], "#f4e4b4")
    for u, col in ((156, "#1c1616"), (163, "#b0382a")):
        c = m.pt(u, 30.5, 136)
        sheet.ellipse(c[0], c[1], 1.5, 0.9, col)
    m.line(sheet, [(168, 31, 136), (186, 31, 134)], "#6a5630", 0.7, 0.9)
    m.line(sheet, [(184, 31, 126), (206, 33, 150)], "#c8b06a", 0.8, 0.95)     # a pen laid across
    props.jar(sheet, *m.pt(203, 30, 150), 5.5, "water", props.MARL, shadow=False)
    # a sheet half unrolled on the mat in front of where he sits
    m.poly(sheet, [(58, 0.5, 128), (116, 0.5, 124), (118, 0.5, 148), (60, 0.5, 152)], "#f6e8c4")
    m.line(sheet, [(58, 2.5, 128), (60, 2.5, 152)], "#fff8e0", 1.8)
    m.line(sheet, [(58, 1.0, 128), (60, 1.0, 152)], "#b89a62", 0.8, 0.8)
    for i in range(4):
        m.line(sheet, [(70 + i * 3, 0.6, 132 + i * 4.4), (108 - (i % 2) * 14, 0.6, 130 + i * 4.4)], "#3a2c28", 0.6, 0.6)
    # sherds, with the tallies of who hauled what
    props.sherds(sheet, *m.pt(236, 0, 104), 15, 9, seed=5)
    c = m.pt(214, 0, 84)
    big = [(c[0] - 5, c[1]), (c[0] - 6, c[1] - 7), (c[0] - 1, c[1] - 10), (c[0] + 5, c[1] - 8), (c[0] + 6, c[1] - 1)]
    sheet.ellipse(c[0] + 5, c[1], 7, 1.6, "#5e4a7c", 0.4)
    sheet.poly(big, props.MARL[2])
    sheet.line([big[1], big[2], big[3]], "#fff8e0", 0.8, 0.8)
    for i in range(4):
        sheet.line([(c[0] - 3.4 + i * 2.1, c[1] - 7.5), (c[0] - 3.0 + i * 2.1, c[1] - 3.6)], "#241c20", 0.7, 0.95)
    sheet.line([(c[0] - 4.4, c[1] - 4.4), (c[0] + 4.2, c[1] - 6.8)], "#241c20", 0.7, 0.95)
    # beer jars at the near corner, sealed with mud, and one more basket of bread
    for (u, d, hh, sd) in ((14, 62, 25, 3), (40, 44, 26, 1), (18, 30, 27, 0), (70, 36, 24, 2), (48, 14, 27, 4)):
        props.jar(sheet, *m.pt(u, 0, d), hh, "beer", stopper="#a39078")
    props.basket(sheet, *m.pt(228, 0, 36), 20, 12, loaves=6, seed=6)
    return sheet


def awning_sheets(shape, seed=33):
    """The awning's cloth, its side cloth toward the sun, the two near poles and their ropes. -> (base, lines)"""
    rng = np.random.default_rng(seed)
    base, lines = Paper(shape), Paper(shape)
    m = mat_frame()
    L = props.LINEN
    sag = 15.0

    def hgt(u, d):
        return MT - sag * math.sin(math.pi * np.clip(u / MW, 0, 1)) * (0.45 + 0.55 * math.sin(math.pi * np.clip(d / MD, 0, 1)))
    us = np.linspace(-8, MW + 8, 11)
    near = [m.pt(u, hgt(u, 0), -8) for u in us]
    far = [m.pt(u, hgt(u, MD), MD + 6) for u in us[::-1]]
    # the side cloth toward the sun: we see its inside, and the sun comes through the linen
    flap = [m.pt(-6, MT, -4), m.pt(-6, MT, MD + 4), m.pt(-6, 72, MD + 2), m.pt(-6, 66, -2)]
    base.poly(flap, "#f9d894")
    for i, d in enumerate(np.linspace(14, MD - 10, 8)):
        d += rng.normal(0, 5)
        col, a = (("#d9a660", 0.55) if i % 2 else ("#fff2c2", 0.6))
        lines.line([m.pt(-6, MT - 3, d), m.pt(-6, MT * 0.6, d + rng.normal(0, 4)), m.pt(-6, 70, d + rng.normal(0, 4))], col, 1.2, a)
    lines.line([flap[3], flap[2]], "#b58450", 1.2, 0.9)
    lines.line([(flap[3][0], flap[3][1] - 2.5), (flap[2][0], flap[2][1] - 2.5)], "#b4583a", 1.0, 0.85)       # a red band along the hem
    # the cloth itself, seen from above: bright, with a hollow where it sags
    base.poly(near + far, L[2])
    hollow = [m.pt(u, hgt(u, d) + 0.5, d) for u, d in ((40, 40), (130, 24), (215, 44), (228, 130), (200, 205), (120, 222), (44, 200), (26, 120))]
    base.poly(hollow, L[1], 0.55)
    base.poly([m.pt(u, hgt(u, d) + 0.6, d) for u, d in ((70, 80), (130, 66), (190, 84), (196, 150), (130, 176), (72, 150))], "#c9bfae", 0.45)
    for u in (62, 126, 190):                                                 # the seams where the lengths of linen are sewn
        lines.line([m.pt(u, hgt(u, d) + 0.6, d) for d in np.linspace(-8, MD + 6, 7)], "#b9ad94", 0.8, 0.6)
    lines.line(far, "#fffaea", 1.0, 0.7)
    # the right-hand edge hangs in shade
    side_top = [m.pt(MW + 8, hgt(MW, d), d) for d in np.linspace(-8, MD + 6, 6)]
    side_low = [m.pt(MW + 8, hgt(MW, d) - 24 - 2 * math.sin(d * 0.11), d) for d in np.linspace(MD + 6, -8, 6)]
    base.poly(side_top + side_low, "#a79bb6")
    lines.line(side_low, "#8a6c84", 0.9, 0.7)
    # the near edge hangs down in a valance cut into tabs, with a red band
    low = []
    for i, u in enumerate(us):
        low.append(m.pt(u, hgt(u, 0) - 27 - (5 if i % 2 else 0), -8))
    base.poly(near + low[::-1], "#e6d8b8")
    tabs = []
    for i in range(len(us) - 1):
        ua, ub = us[i], us[i + 1]
        um = (ua + ub) / 2
        tabs += [m.pt(ua + 3, hgt(ua, 0) - 27, -8), m.pt(um, hgt(um, 0) - 38, -8), m.pt(ub - 3, hgt(ub, 0) - 27, -8)]
    for i in range(0, len(tabs), 3):
        base.poly([tabs[i], tabs[i + 1], tabs[i + 2]], "#e0d0ae")
    lines.line([m.pt(u, hgt(u, 0) - 21, -8) for u in us], "#b4583a", 1.5, 0.9)
    lines.line([m.pt(u, hgt(u, 0) - 17.5, -8) for u in us], "#2f5a7a", 0.8, 0.7)      # and a thin blue one
    lines.line(near, "#fffaea", 1.2, 0.9)                                              # the fold where it turns over the rope
    for i, u in enumerate(us[1:-1]):                                                    # soft folds in the valance
        lines.line([m.pt(u, hgt(u, 0) - 3, -8), m.pt(u + rng.normal(0, 2), hgt(u, 0) - 26, -8)], "#bfb098", 0.8, 0.45)
    # the two near poles, their lashings and guy ropes
    for u in (0, MW):
        foot, head = m.pt(u, 0, 0), m.pt(u, MT + 12, 0)
        props.log(base, foot, head, 4.4, knots=3, seed=int(u))
        props.log(lines, foot, head, 4.4, knots=3, seed=int(u))
        props.lash(lines, head[0], head[1] + 7, 3.0, seed=int(u) + 1)
        lines.ellipse(foot[0], foot[1], 4.0, 1.4, "#c9a070", 0.9)                       # sand heaped round its foot
    peg = m.pt(MW + 78, 0, -52)
    a = m.pt(MW, MT + 6, 0)
    props.rope(lines, [a, (lerp(a[0], peg[0], 0.5), lerp(a[1], peg[1], 0.5) + 3), peg], 1.2)
    lines.line([(peg[0] - 2, peg[1] + 2), (peg[0] + 2.5, peg[1] - 5)], props.WOOD[0], 2.2)
    lines.line([(peg[0] - 2.4, peg[1] + 1.4), (peg[0] + 2.0, peg[1] - 5.4)], props.WOOD[2], 0.8)
    a = m.pt(0, MT + 6, 0)
    props.rope(lines, [a, (a[0] - 34, a[1] + 52), (a[0] - 70, a[1] + 112)], 1.2)
    # a water jar slung in a net from the near right pole, to keep cool
    hook = m.pt(MW - 6, MT - 30, -6)
    jx, jy = hook[0] - 7, hook[1] + 40
    lines.line([hook, (jx, jy - 22)], props.ROPE[0], 0.9)
    props.jar(lines, jx, jy, 20, "water", shadow=False)
    for dx in (-5.5, -2, 2, 5.5):
        lines.line([(jx, jy - 22), (jx + dx, jy - 12), (jx + dx * 0.8, jy - 2)], props.ROPE[2], 0.6, 0.8)
    lines.line([(jx - 7.5, jy - 9), (jx + 7.5, jy - 9)], props.ROPE[2], 0.6, 0.8)
    return base, lines


def awning_plane(shape, fast=False):
    base, lines = awning_sheets(shape)
    return cutout(shape, base, lines, "#e6cfa2", 12, fast=fast)


# ---------------------------------------------------------------- stone blocks, as the masons leave them
def bil(q, a, b):
    """A place on a four-cornered face: `a` across (corner 0 to 1), `b` up (corner 0 to 3)."""
    lo = (lerp(q[0][0], q[1][0], a), lerp(q[0][1], q[1][1], a))
    hi = (lerp(q[3][0], q[2][0], a), lerp(q[3][1], q[2][1], a))
    return (lerp(lo[0], hi[0], b), lerp(lo[1], hi[1], b))


def tooling(sheet, q, rng, color, n=60, alpha=0.22, length=0.06, slant=0.5):
    """The marks a chisel leaves on a face: rows of short slanting strokes."""
    for _ in range(n):
        a, b = rng.random() * 0.94 + 0.03, rng.random() * 0.9 + 0.05
        sheet.line([bil(q, a, b), bil(q, min(a + length * slant, 1), min(b + length, 1))], color, 0.8, alpha * (0.5 + rng.random()))
    return sheet


def ochre(sheet, q, at, size, rng, color="#b4452c"):
    """A gang's mark daubed on a block in red ochre: an eye-shaped ring, a wavy line under it, an arch
    and three dots. (Invented signs: no real writing.)"""
    a0, b0 = at
    ring = [bil(q, a0 + math.cos(t) * size * 0.75, b0 + size * 0.5 + math.sin(t) * size * 0.55) for t in np.linspace(0.2, 6.5, 13)]
    sheet.line(ring, color, 1.3, 0.8)
    c = bil(q, a0, b0 + size * 0.5)
    sheet.ellipse(c[0], c[1], 1.1, 1.1, color, 0.85)
    wave = [bil(q, a0 - size * 0.9 + i * size * 0.3, b0 - size * 0.75 + (size * 0.22 if i % 2 else -size * 0.22)) for i in range(8)]
    sheet.line(wave, color, 1.1, 0.75)
    arch = [bil(q, a0 + size * (2.1 + 0.5 * math.cos(t)), b0 - size * 0.6 + size * 1.5 * math.sin(t)) for t in np.linspace(0, math.pi, 8)]
    sheet.line(arch, color, 1.3, 0.8)
    for (da, db) in ((3.3, 0.6), (3.9, 0.6), (3.6, -0.3)):
        c = bil(q, a0 + size * da, b0 + size * db)
        sheet.ellipse(c[0], c[1], 1.3, 1.3, color, 0.8)
    return sheet


def stone_block(base, lines, f, u0, u1, v0, v1, d0, d1, rng, marks=None, rough=1.0, tones=STONE):
    """A squared block of white limestone in a frame: sunlit top, front in half light, its left end lit,
    its right end in shade. Edges, chips and tool marks go on the `lines` sheet."""
    f.box(base, u0, u1, v0, v1, d0, d1, front=tones["front"], top=tones["top"], left=tones["left"], right=tones["side"])
    front = f.pts([(u0, v0, d0), (u1, v0, d0), (u1, v1, d0), (u0, v1, d0)])
    top = f.pts([(u0, v1, d0), (u1, v1, d0), (u1, v1, d1), (u0, v1, d1)])
    left = f.pts([(u0, v0, d1), (u0, v0, d0), (u0, v1, d0), (u0, v1, d1)])
    right = f.pts([(u1, v0, d0), (u1, v0, d1), (u1, v1, d1), (u1, v1, d0)])
    see_left = -f.c * (0 - f.w(u0, 0, (d0 + d1) / 2)[0]) - f.s * (0 - f.w(u0, 0, (d0 + d1) / 2)[2]) > 0
    see_right = f.c * (0 - f.w(u1, 0, (d0 + d1) / 2)[0]) + f.s * (0 - f.w(u1, 0, (d0 + d1) / 2)[2]) > 0
    # the front goes a little darker and cooler toward its foot; the top has a warm bloom
    base.poly([bil(front, 0, 0), bil(front, 1, 0), bil(front, 1, 0.45), bil(front, 0, 0.3)], "#c9a688", 0.35)
    base.poly([bil(top, 0.1, 0.15), bil(top, 0.7, 0.1), bil(top, 0.85, 0.7), bil(top, 0.2, 0.85)], "#fffbe6", 0.4)
    tooling(lines, front, rng, "#b08c68", int(70 * rough), 0.26)
    if see_left:
        tooling(lines, left, rng, "#c9a070", int(40 * rough), 0.22)
    if see_right:
        tooling(lines, right, rng, "#7a6c88", int(30 * rough), 0.3)
    # drafted margins: a smoother band chiselled along each edge of the front
    for (a0, b0, a1, b1) in ((0.06, 0.07, 0.94, 0.07), (0.06, 0.93, 0.94, 0.93), (0.05, 0.07, 0.05, 0.93), (0.95, 0.07, 0.95, 0.93)):
        lines.line([bil(front, a0, b0), bil(front, a1, b1)], "#fff0cc", 0.9, 0.4)
    # edges: light where a top meets the sky, dark in the corners turned from the sun
    lines.line([top[0], top[1]], "#fffbe8", 1.2, 0.9)
    lines.line([top[3], top[2]], "#fff6dc", 0.9, 0.7)
    lines.line([front[0], front[1]], tones["joint"], 1.1, 0.55)
    if see_left:
        lines.line([left[2], left[3]], "#fffbe8", 1.0, 0.8)
        lines.line([front[0], front[3]], "#fff6dc", 0.9, 0.55)
    else:
        lines.line([front[0], front[3]], tones["joint"], 0.9, 0.5)
    if see_right:
        lines.line([front[1], front[2]], tones["joint"], 1.0, 0.6)
        lines.line([right[3], right[2]], "#d8cfe0", 0.9, 0.6)
    # chips knocked off the edges
    for _ in range(int(5 * rough)):
        a = rng.random()
        c = bil(front, a, 1.0)
        r = 1.5 + rng.random() * 2.5
        lines.poly([(c[0] - r, c[1] - 0.6), (c[0] + r, c[1] - 0.6), (c[0] + r * 0.3, c[1] + r * 0.9)], "#c8a67e", 0.8)
    if marks:
        ochre(lines, front, marks[0], marks[1], rng)
    return front, top, left, right


# ---------------------------------------------------------------- the sledge and its block
SLED = dict(dark="#3e2a1c", side="#93683f", top="#c9a068", shade="#644630", end="#7a5632")


def sledge_sheets(shape, seed=41):
    """The sledge, heading away up-left: two runners turned up at the front, cross beams, the block
    roped down on them. -> (base, lines)"""
    rng = np.random.default_rng(seed)
    base, lines = Paper(shape), Paper(shape)
    f = sledge_frame()
    r0, r1, across = RUNNERS
    prow = [(r1, 0), (r1, 22), (16, 22), (-8, 30), (-26, 47), (-35, 44), (-21, 23), (-5, 6), (8, 0)]
    for d0 in (across - 14, 0):                                              # the far runner first
        base.poly([f.pt(u, v, d0 + 14) for u, v in prow], SLED["shade"])
        f.poly(base, [(16, 22, d0), (r1, 22, d0), (r1, 22, d0 + 14), (16, 22, d0 + 14)], SLED["top"])
        f.poly(base, [(-8, 30, d0), (16, 22, d0), (16, 22, d0 + 14), (-8, 30, d0 + 14)], SLED["top"])
        f.poly(base, [(-26, 47, d0), (-8, 30, d0), (-8, 30, d0 + 14), (-26, 47, d0 + 14)], SLED["top"])
        base.poly([f.pt(u, v, d0) for u, v in prow], SLED["side"])
        f.poly(base, [(r1, 0, d0), (r1, 0, d0 + 14), (r1, 22, d0 + 14), (r1, 22, d0)], SLED["end"])       # its sawn end
        lines.line([f.pt(u, v, d0) for u, v in (prow[1:6] if d0 == 0 else prow[2:6])], "#e6c48c", 1.0, 0.85)
        if d0 == 0:
            lines.line([f.pt(u, v, d0) for u, v in (prow[5:] + prow[:1])], SLED["dark"], 1.1, 0.8)
        for k in range(5 if d0 == 0 else 0):                                 # grain
            ua = 30 + rng.random() * 150
            lines.line([f.pt(ua, 6 + k * 3.2, d0), f.pt(ua + 30 + rng.random() * 40, 6 + k * 3.2 + rng.normal(0, 0.6), d0)], SLED["dark"], 0.7, 0.35)
    for u in (30, 96, 162, 224):                                             # cross beams, lashed to the runners
        f.box(base, u - 6, u + 6, 22, 33, -5, across + 5, front=SLED["end"], top=SLED["top"], left=SLED["side"], right=SLED["shade"])
        c = f.pt(u, 27.5, -5)
        lines.ellipse(c[0], c[1], 2.4, 2.9, "#5a3c24")
        lines.ellipse(c[0] - 0.4, c[1] - 0.4, 1.3, 1.7, "#a67c4c")
        props.lash(lines, f.pt(u, 21, 0)[0], f.pt(u, 21, 0)[1], 2.6, seed=u)
    # the dark under the block, between the beams
    f.poly(base, [(BLOCK_U[0], 22, 0), (BLOCK_U[1], 22, 0), (BLOCK_U[1], 34, 0), (BLOCK_U[0], 34, 0)], "#2e2028", 0.75)
    for u in (30, 96, 162, 224):
        f.poly(base, [(u - 6, 22, -5), (u + 6, 22, -5), (u + 6, 33, -5), (u - 6, 33, -5)], SLED["end"])
    # the block
    front, top, left, right = stone_block(base, lines, f, BLOCK_U[0], BLOCK_U[1], BLOCK_V[0], BLOCK_V[1], BLOCK_D[0], BLOCK_D[1], rng, marks=((0.36, 0.58), 0.05))
    lines.line([bil(front, 0.04, 0.26), bil(front, 0.5, 0.25 + rng.normal(0, 0.01)), bil(front, 0.96, 0.26)], "#b4452c", 0.9, 0.5)     # a levelling line, snapped with a red string
    # ropes over it, twisted tight with a stick
    for u in (BLOCK_U[0] + 34, BLOCK_U[1] - 36):
        props.rope(lines, [f.pt(u, 20, 2), f.pt(u, BLOCK_V[1] + 1, BLOCK_D[0] - 1)], 1.8)
        props.rope(lines, [f.pt(u, BLOCK_V[1] + 1, BLOCK_D[0] - 1), f.pt(u + 2, BLOCK_V[1] + 1, BLOCK_D[1])], 1.6)
    a, b = f.pt(BLOCK_U[0] + 20, BLOCK_V[1] + 3, 46), f.pt(BLOCK_U[0] + 52, BLOCK_V[1] + 3, 64)
    lines.line([(a[0] + 1, a[1] + 1.6), (b[0] + 1, b[1] + 1.6)], "#8a7a90", 2.0, 0.5)
    props.log(lines, a, b, 2.4)
    # a lever left lying on top, and the hauling rope made fast to the first beam
    a, b = f.pt(BLOCK_U[0] + 70, BLOCK_V[1] + 3, 84), f.pt(BLOCK_U[1] - 8, BLOCK_V[1] + 3, 30)
    lines.line([(a[0] + 1.5, a[1] + 2), (b[0] + 1.5, b[1] + 2)], "#8a7a90", 2.6, 0.5)
    props.log(lines, a, b, 3.0, knots=2, seed=3)
    props.rope(lines, [f.pt(30, 30, across * 0.5), f.pt(4, 26, across * 0.5), f.pt(-34, 10, across * 0.52), f.pt(-62, 1, across * 0.56)], 2.6)
    props.lash(lines, *f.pt(30, 30, across * 0.5), 3.2, seed=77)
    return base, lines


def sledge_plane(shape, fast=False):
    base, lines = sledge_sheets(shape)
    return cutout(shape, base, lines, "#e2c08c", 13, fast=fast)


# ---------------------------------------------------------------- the waiting blocks, at the very front
def stack_frame():
    return Frame(world=(215.0, 775.0), turn=16.0)


STACK_A = (0.0, 165.0, 108.0, 0.0, 125.0)                   # the near block: u0, u1, height, d0, d1
STACK_B = (150.0, 320.0, 108.0, 150.0, 268.0)               # the one behind it, its outer face already cut to the pyramid's slope


def front_sheets(shape, seed=51):
    """Casing blocks waiting their turn, bottom right, with the masons' tools left on the nearest:
    copper chisels, mallets, a set-square, a plumb line, a pounding stone. -> (base, lines)"""
    rng = np.random.default_rng(seed)
    base, lines = Paper(shape), Paper(shape)
    back_base, back_lines = base, lines
    f = stack_frame()
    shade_tones = dict(STONE, front="#c2a698")                              # the nearest block's front is turned right away from the sun
    # ---- the block behind: one face is sloped, as every casing block's is
    u0, u1, hh, d0, d1 = STACK_B
    back = hh / TAN
    f.poly(base, [(u0, 0, d0), (u0, 0, d1), (u0, hh, d1), (u0, hh, d0 + back)], STONE["left"])
    slope = f.pts([(u0, 0, d0), (u1, 0, d0), (u1, hh, d0 + back), (u0, hh, d0 + back)])
    base.poly(slope, "#ead2a2")
    base.poly([bil(slope, 0, 0), bil(slope, 1, 0), bil(slope, 1, 0.5), bil(slope, 0, 0.35)], "#cfae90", 0.35)
    topb = f.pts([(u0, hh, d0 + back), (u1, hh, d0 + back), (u1, hh, d1), (u0, hh, d1)])
    base.poly(topb, STONE["top"])
    tooling(lines, slope, rng, "#b8946c", 60, 0.2, slant=0.15)
    lines.line([topb[0], topb[1]], "#fffbe8", 1.2, 0.9)
    lines.line([slope[0], slope[3]], "#fff6dc", 1.0, 0.7)
    lines.line([topb[0], topb[3]], "#fffbe8", 1.0, 0.8)
    lines.line([bil(slope, 0.05, 0.62), bil(slope, 0.95, 0.60)], "#b4452c", 0.9, 0.5)
    ochre(lines, slope, (0.12, 0.34), 0.04, rng)
    props.jar(lines, *bil(topb, 0.3, 0.5), 30, "water", props.MARL, shadow=False)          # somebody's water, and his dipper
    c = bil(topb, 0.52, 0.45)
    lines.ellipse(c[0] + 2, c[1] + 1, 7, 2.6, "#8a7a90", 0.5)
    lines.ellipse(c[0], c[1], 6, 2.6, props.POT[1])
    lines.ellipse(c[0], c[1] - 0.6, 4.4, 1.6, props.POT[0])
    props.mallet(lines, bil(topb, 0.66, 0.30), bil(topb, 0.86, 0.62), 2.2 * f.k(240, 235))      # and a second mallet
    # ---- the near block (on fresh sheets: it stands in front of the other)
    base, lines = Paper(shape), Paper(shape)
    u0, u1, hh, d0, d1 = STACK_A
    front, top, left, right = stone_block(base, lines, f, u0, u1, 0, hh, d0, d1, rng, marks=((0.16, 0.66), 0.045), rough=1.5, tones=shade_tones)
    base.poly([bil(front, 0, 0), bil(front, 1, 0), bil(front, 1, 0.3), bil(front, 0, 0.22)], "#d8b494", 0.4)        # light off the sand comes back up at its foot
    k = f.k(80, 60)

    def on(u, d, v=0.0):
        return f.pt(u, hh + v, d)
    # a wooden mallet, two copper chisels
    props.mallet(lines, on(18, 46), on(68, 78), 2.9 * k)
    props.chisel(lines, on(84, 20), on(122, 42), 2.3 * k)
    props.chisel(lines, on(76, 62), on(112, 50), 2.1 * k)
    # the set-square: two arms and a brace, of pale wood
    sq = [(150, 104), (150, 58), (108, 104)]
    for a, b in ((sq[0], sq[1]), (sq[0], sq[2])):
        lines.line([(on(*a)[0] + 1.2, on(*a)[1] + 1.6), (on(*b)[0] + 1.2, on(*b)[1] + 1.6)], "#8a7a90", 4.2 * k, 0.45)
    for a, b in ((sq[0], sq[1]), (sq[0], sq[2])):
        lines.line([on(*a), on(*b)], "#8a623c", 4.6 * k)
        lines.line([on(a[0] - 0.6, a[1] - 0.6), on(b[0] - 0.6, b[1] - 0.6)], "#e2c088", 2.6 * k)
    lines.line([on(150, 74), on(124, 104)], "#8a623c", 2.6 * k)
    lines.line([on(150, 74), on(124, 104)], "#d6b078", 1.2 * k)
    # the plumb line: its cord wound on a peg, run over the edge, the bob hanging down the block's front
    lines.line([on(128, 26), on(138, 30)], props.WOOD[0], 4.0 * k)
    lines.line([on(128.5, 25.5), on(138.5, 29.5)], props.WOOD[2], 1.6 * k)
    lines.line([on(133, 28), on(127, 0)], "#f6ecd2", 0.9, 0.95)
    a, b = f.pt(127, hh, 0), f.pt(127, hh - 58, -1.5)
    lines.line([a, b], "#f6ecd2", 0.9, 0.95)
    lines.line([(a[0] + 5, a[1] + 3), (b[0] + 5, b[1] + 3)], "#7c6a80", 1.0, 0.4)
    lines.poly([(b[0] - 3.2 * k, b[1]), (b[0] + 3.2 * k, b[1]), (b[0] + 2.2 * k, b[1] + 6 * k), (b[0], b[1] + 12 * k), (b[0] - 2.2 * k, b[1] + 6 * k)], "#565c58")
    lines.poly([(b[0] - 3.2 * k, b[1]), (b[0] - 0.6 * k, b[1]), (b[0] - 0.8 * k, b[1] + 8 * k), (b[0] - 2.2 * k, b[1] + 6 * k)], "#98a098")
    # a pounding stone: a ball of hard dark rock
    c = on(26, 102)
    lines.ellipse(c[0] + 4 * k, c[1] + 1.5 * k, 10 * k, 3.4 * k, "#8a7a90", 0.5)
    lines.ellipse(c[0], c[1] - 6 * k, 8.5 * k, 8 * k, "#2f3632")
    lines.ellipse(c[0] - 1.6 * k, c[1] - 7.6 * k, 5.6 * k, 5.0 * k, "#515c56")
    lines.ellipse(c[0] - 3.2 * k, c[1] - 9.4 * k, 2.2 * k, 1.8 * k, "#9aa69e")
    # chips on the block and a little heap of them swept to one corner
    for _ in range(26):
        c = on(rng.uniform(4, 160), rng.uniform(4, 120))
        r = rng.uniform(0.8, 2.2)
        lines.poly([(c[0] - r, c[1]), (c[0], c[1] - r * 0.8), (c[0] + r, c[1] + r * 0.2)], "#fffbe8" if rng.random() < 0.6 else "#d8bc92", 0.9)
    # two levers leaning against its sunny end
    for (ua, da, db, top_v, wd) in ((-74, 30, 52, 150, 5.2), (-50, 92, 100, 132, 4.4)):
        a = f.pt(ua, -12, da)
        b = f.pt(ua * (1 - top_v / 108.0), top_v, lerp(da, db, 1.0))
        props.log(base, a, b, wd * k)
        props.log(lines, a, b, wd * k, knots=3, seed=int(da))
    # a coil of rope at the very edge
    props.coil(lines, 546, 592, 24, 8, turns=4, width=2.8)
    props.rope(lines, [(566, 590), (584, 584), (596, 590), (604, 600)], 2.8)
    water_rack(base, lines)
    return (back_base, back_lines), (base, lines)


WET_POT = ("#562a1e", "#9c5236", "#c98054", "#f2c096")
RACK = Frame(world=(-452.0, 846.0), turn=-12.0)


def water_rack(base, lines, seed=57):
    """Bottom left, where the road comes up from the river: the site's water, in two great jars on a
    wooden rack, dark with damp; a dipper hung on the post; grass where they drip."""
    rng = np.random.default_rng(seed)
    w = RACK
    k = w.k(50, 20)
    for d in (46, 0):                                                        # the rack: two rails on four legs
        for u in (-10, 118):
            props.log(base, w.pt(u, -6, d), w.pt(u, 44 + (22 if (u > 100 and d == 0) else 0), d), 6.5 * k)
            props.log(lines, w.pt(u, -6, d), w.pt(u, 44 + (22 if (u > 100 and d == 0) else 0), d), 6.5 * k, knots=1, seed=abs(int(u + d)))
        props.log(base, w.pt(-22, 36, d), w.pt(130, 36, d), 6.0 * k)
        props.log(lines, w.pt(-22, 36, d), w.pt(130, 36, d), 6.0 * k)
        for u in (-10, 118):
            c = w.pt(u, 36, d)
            props.lash(lines, c[0], c[1], 3.4 * k, seed=abs(int(u + d)) + 5)
    for u, hh in ((26, 74), (88, 68)):
        c = w.pt(u, 26, 23)
        props.jar(base, c[0], c[1], hh * k, "water", WET_POT, shadow=False)
        wide = 0.41 * hh * k
        lines.ellipse(c[0], c[1] - hh * k, 0.22 * hh * k, 0.08 * hh * k, WET_POT[0])                 # the rim and the dark mouth
        lines.ellipse(c[0], c[1] - hh * k - 0.6, 0.18 * hh * k, 0.055 * hh * k, "#1e1418")
        lines.line([(c[0] - 0.24 * hh * k, c[1] - hh * k), (c[0] + 0.1 * hh * k, c[1] - hh * k - 0.07 * hh * k)], WET_POT[3], 1.2, 0.9)
        lines.line([(c[0] - wide * 0.72, c[1] - hh * k * 0.72), (c[0] - wide * 0.86, c[1] - hh * k * 0.46), (c[0] - wide * 0.7, c[1] - hh * k * 0.26)], WET_POT[3], 1.6, 0.85)
        for i in range(4):                                                   # damp running down from the shoulder
            px = c[0] - wide * 0.5 + rng.random() * wide * 1.1
            lines.line([(px, c[1] - hh * k * (0.5 + 0.2 * rng.random())), (px + rng.normal(0, 1), c[1] - hh * k * 0.14)], "#4a241c", 1.3, 0.35)
        lines.line([(c[0] - wide * 0.8, c[1] - hh * k * 0.6), (c[0] + wide * 0.8, c[1] - hh * k * 0.6)], "#e6c8a0", 1.0, 0.5)           # a scored band
    c = w.pt(118, 62, 0)                                                     # the dipper: half a gourd on a cord
    lines.line([c, (c[0] + 2, c[1] + 15 * k)], props.ROPE[1], 1.0)
    lines.poly([(c[0] - 6 * k, c[1] + 15 * k), (c[0] + 9 * k, c[1] + 15 * k), (c[0] + 6 * k, c[1] + 25 * k), (c[0] - 2 * k, c[1] + 26 * k)], "#b8904c")
    lines.poly([(c[0] - 6 * k, c[1] + 15 * k), (c[0] + 1 * k, c[1] + 15 * k), (c[0] + 0 * k, c[1] + 25 * k), (c[0] - 2 * k, c[1] + 26 * k)], "#e2c07c")
    for (gx, gy, r, sd) in ((112, 597, 17, 1), (134, 600, 13, 2), (96, 601, 12, 3), (150, 598, 9, 4)):     # grass where the jars drip
        flora.scrub(lines, gx, gy, r, seed + sd, colors=("#55652e", "#8c9c46", "#c8c672"))
    return base, lines


def front_plane(shape, fast=False, cloud=None):
    behind, before = front_sheets(shape)
    color, alpha = cutout(shape, behind[0], behind[1], "#d8b68c", 16, fast=fast, sizes=(8, 4, 2), keep=0.40)
    c2, a2 = cutout(shape, before[0], before[1], "#d8b68c", 14, fast=fast, sizes=(8, 4, 2), keep=0.40)
    over(color, c2, (a2 > 0.5).astype(F32))
    alpha = np.maximum(alpha, a2)
    if cloud is not None:                                                    # the cloud's shadow that lies on the sand lies on them too: white stone goes lilac in it
        tint(color, "#a9a0c6", (cloud * 0.44).astype(F32))
        over(color, "#8a82aa", (cloud * 0.08).astype(F32))
    return color, alpha


# ---------------------------------------------------------------- the windshield shade, held up at the sunny spot
def shade_sheets(shape, seed=61):
    """A folding car windshield sun-shade, silver foil in accordion folds, about 130 cm by 60, as a man
    standing on the sunny spot and facing right would hold it up to the sun. -> (base, lines)"""
    rng = np.random.default_rng(seed)
    base, lines = Paper(shape), Paper(shape)
    sx, sy = SUNSPOT
    k = size_at(sy)                                                          # pixels per centimetre where he stands
    p0 = np.array([sx + 20 * k, sy - 118 * k])                               # the near corner by his hands
    along = np.array([0.925, -0.38]) * 130 * k                               # its length rises to the right
    up = np.array([0.30, -0.954]) * 60 * k * 0.50                            # its width, seen at a slant
    n = 10
    fold = np.array([0.0, 1.0]) * 3.4 * k                                    # how far a fold stands up or dips

    def at(a, b, i=None):
        p = p0 + along * a + up * b
        if i is not None:
            p = p + fold * (1 if i % 2 else -1)
        return (float(p[0]), float(p[1]))
    under = [at(i / n, 0, i) for i in range(n + 1)]
    base.poly([(px, py + 2.6 * k) for px, py in under] + under[::-1], "#566078")                 # its thickness, seen along the near edge
    for i in range(n):
        quad = [at(i / n, 0, i), at((i + 1) / n, 0, i + 1), at((i + 1) / n, 1, i + 1), at(i / n, 1, i)]
        sunny = i % 2 == 0
        tone = ("#f4f8fc", "#ffffff", "#dfe8f2")[i % 3] if sunny else ("#9eacc2", "#8a9ab4", "#aab8cc")[i % 3]
        base.poly(quad, tone)
        if sunny:
            base.poly([quad[0], quad[1], bil(quad, 1, 0.35), bil(quad, 0, 0.5)], "#cfe2f6", 0.6)   # the sky in it
        else:
            base.poly([bil(quad, 0, 0.55), bil(quad, 1, 0.5), quad[2], quad[3]], "#c9b79a", 0.45)  # and the sand
    for i in range(n + 1):                                                    # the folds: a bright ridge, a dark valley
        a, b = at(i / n, 0, i), at(i / n, 1, i)
        lines.line([a, b], "#ffffff" if i % 2 else "#5c6880", 1.0 if i % 2 else 0.9, 0.95 if i % 2 else 0.8)
    edge = [at(i / n, 1, i) for i in range(n + 1)]
    lines.line(edge, "#eef4fa", 1.1, 0.9)
    lines.line(under, "#3f4960", 1.1, 0.9)
    lines.line([under[0], edge[0]], "#3f4960", 1.2, 0.9)                      # the bound ends
    lines.line([under[-1], edge[-1]], "#3f4960", 1.2, 0.9)
    for i in (1, 4, 7):                                                       # where the sun flashes on a crease
        c = bil([under[i], under[i + 1], edge[i + 1], edge[i]], 0.15, 0.3 + 0.1 * (i % 3))
        lines.line([(c[0] - 3.2, c[1]), (c[0] + 3.2, c[1])], "#ffffff", 0.9)
        lines.line([(c[0], c[1] - 3.2), (c[0], c[1] + 3.2)], "#ffffff", 0.9)
        lines.ellipse(c[0], c[1], 1.3, 1.3, "#ffffff")
    # the elastic loop that holds it shut, hanging from the far end
    e = edge[-1]
    lines.line([e, (e[0] + 5, e[1] + 9), (e[0] + 1.5, e[1] + 17), (e[0] - 2, e[1] + 9), (under[-1][0], under[-1][1])], "#1e2230", 1.1, 0.95)
    return base, lines


def shade_plane(shape, fast=False):
    base, lines = shade_sheets(shape)
    return cutout(shape, base, lines, "#c8d2e0", 15, fast=fast, sizes=(5, 3, 2), keep=0.5)

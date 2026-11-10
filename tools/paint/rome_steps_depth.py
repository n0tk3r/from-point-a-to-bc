"""The steps of the temple of Saturn, deepened (round twenty-three, the fast pass: tools/paint/DEPTH.md). Works over the
painting as rome_steps.py makes it (out/rome-steps-orig/, never changed) and writes the scene's full set back into
out/rome-steps/, every file as before plus near.png.

WHERE WE STAND. The lens is 3.6 m above the Forum's paving (persp.Camera(260, 590)): a grown-up's eyes on the raised
floor of the portico on our side of the square, the Basilica's, at its corner. So, through the scene's own camera:

  near.png   the portico's corner column, 3.3 m from the lens, 52 cm thick: the right edge of its shaft up the left side
             of the frame (its foot and its capital are both off the picture), in the portico's shade, warm, its red
             lower third and fluted stucco as Saturn's own columns are, a thin warm rim on the edge that faces the
             sunlit square. Behind it a laurel's boughs come across the top left corner, over the open sky, dark, the
             outer leaves catching the light. It stops short of the way to the street (the box of whoever stands there
             begins at x 18) and of the hill and Jupiter's temple.
  the old front plane (the statue base and the laurel bush at the bottom left: front.png = front-base.png + laurel.png)
             keeps its outline exactly; its colours go a little deeper and warmer, to belong to the near plane.
  back.png   the long morning shadows of the Forum's tall things out of the picture on our right (the sun is to the
             right and a little behind us) laid across the paving, the largest from the bottom right corner (an
             honorary column and its statue); worn spots and chipped joints on the paving, few and large near us, many
             and small far off (depth.scatter); the near paving deeper, the far paving paler; the Forum and the hill
             behind it moved toward the sky's colour, the hill most. Nothing clicked moves.

    python3 rome_steps_depth.py      -> out/rome-steps/ (the full set), out/rome-steps-depth-look.png
"""

import os
import shutil
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

from brush import F32, Sheet, blur, grid, lerp, mask_poly, noise, palette_of, rgb, save, step, to_palette, grain
import depth
import rome_forum_near as FN
from rome_steps_kit import Canvas
import rome_steps as RS

SRC = "out/rome-steps-orig"
OUT = "out/rome-steps"
SHAPE = (600, 800)
H, W = SHAPE
CAM = RS.CAM
CAST = RS.CAST                                            # a shadow on the ground, per cm of height: (across, away)
SHADE = "#2b2134"                                        # the near plane's shade (the Forum's: the key's own dark)
RIM = "#ffe6b0"                                          # light off the sunlit square
SKY = "#d4dee4"                                          # the sky's colour at the horizon (measured, left of the temple)

WALK = [[0, 597], [797, 597], [797, 433], [797, 298], [763, 298], [648, 291], [342, 296], [396, 305], [382, 306], [461, 461],
        [400, 462], [340, 452], [240, 446], [120, 442], [0, 438]]
STEPS = [[382, 306], [461, 461], [797, 433], [797, 298], [763, 298], [648, 291], [342, 296], [396, 305]]
HILL = [[0, 212], [14, 186], [22, 174], [31, 175], [34, 195], [54, 187], [55, 144], [97, 118], [101, 118], [137, 143], [138, 181], [148, 182], [160, 183],
        [200, 201], [238, 209], [240, 236], [225, 234], [209, 230], [208, 222], [200, 222], [199, 229], [190, 227], [186, 214], [170, 214], [166, 220], [160, 226],
        [160, 184], [148, 183], [148, 230], [138, 230], [125, 225], [108, 221], [86, 229], [78, 226], [75, 218], [61, 218], [60, 222], [45, 223], [0, 220]]
FORUM = [[0, 220], [45, 223], [60, 222], [61, 218], [75, 218], [78, 226], [86, 229], [108, 221], [125, 225], [138, 230], [148, 230], [148, 183], [160, 184],
         [160, 226], [166, 220], [170, 214], [186, 214], [190, 227], [199, 229], [200, 222], [208, 222], [209, 230], [225, 234], [240, 236], [240, 288], [236, 304], [0, 304]]


def load_rgb(name):
    return np.asarray(Image.open(f"{SRC}/{name}").convert("RGB"), dtype=F32) / 255.0


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


# ================================================================ the front plane
COLUMN = dict(D=330.0, r=26.0, edge=16.2)                 # 3.3 m from the lens; its right edge at picture x 16
FLOOR = 200.0                                            # the portico's floor above the paving (cm): the eye is 161 cm above it
RED_TOP = 118.0                                          # the column's red, up from that floor


def column(cv, seed=401):
    """The portico's corner column, in its shade: the right edge of its shaft, from the top of the picture to the bottom."""
    c = COLUMN
    k = CAM.F / c["D"]                                   # pixels per cm at the column
    rp = c["r"] * k
    x, y = grid(SHAPE)
    edge = c["edge"] + (noise(SHAPE, 60, seed, 3)[:, :1] - 0.5) * 1.4             # no long edge is ruled
    axis = edge - rp
    s = np.clip((x + 0.5 - axis) / rp, -1, 1)
    theta = np.arcsin(s)                                                            # where on the round we are (90 deg: the edge)
    h = CAM.eye - (y - CAM.vy) / k                                                  # height above the paving
    b = h - FLOOR                                                                   # above the portico's floor
    around = theta * c["r"]                                                         # cm round the shaft
    stucco = col(RS.STUCCO)[None, None, :] * (1 + (noise(SHAPE, 90, seed + 1, 3)[..., None] - 0.5) * 0.10)
    red = col(RS.RED)[None, None, :] * (0.94 + 0.12 * noise(SHAPE, 40, seed + 2, 3)[..., None])
    own = np.where((b < RED_TOP)[..., None], red, stucco)
    ring = np.abs(b - RED_TOP - 3.0) < 3.0
    own = np.where(ring[..., None], col("#2f2a33") * 1.4, own)
    flute = np.cos(around / (2 * np.pi * c["r"] / 20.0) * 2 * np.pi)                # twenty flutes round
    flute = np.where((b > RED_TOP + 8)[..., None], (flute * 0.5 + 0.5)[..., None], 1.0)
    base = lerp(own, col(SHADE)[None, None, :], 0.78) * np.array([1.26, 0.97, 0.86], dtype=F32)    # deep, warm: the floor's light in it
    base = base * (0.86 + 0.14 * flute)
    turn = np.clip((s - 0.80) / 0.20, 0, 1) ** 1.6                                  # the round turning toward the sunlit square
    warm = own * np.array([0.98, 0.80, 0.58], dtype=F32)
    out = lerp(base, warm, (0.42 * turn)[..., None])
    out = lerp(out, col(RIM)[None, None, :] * own / np.maximum(own.max(axis=-1, keepdims=True), 1e-3), (0.75 * np.clip((s - 0.965) / 0.035, 0, 1))[..., None])
    low = np.clip((y - 430) / 170.0, 0, 1)                                          # lower down, light thrown up off the paving
    out = out * (1 + 0.10 * low[..., None] * np.array([1.0, 0.85, 0.6], dtype=F32))
    a = np.clip(edge + 0.5 - x, 0, 1).astype(F32)                                   # its silhouette, antialiased
    cv.put(np.clip(out, 0, 1).astype(F32), a)


# a laurel's boughs across the top left corner, from behind the column (picture points, as rome_forum_near's)
LIMBS = [([(-24, 18), (24, 16), (74, 24), (122, 36), (170, 48), (214, 56)], 12.0, 4.0),
         ([(-24, 70), (10, 78), (36, 96), (50, 116)], 8.0, 3.0),
         ([(60, -8), (130, 2), (210, 8), (290, 14), (360, 18)], 8.0, 2.6)]
SHOOTS = [
    ([(-16, -6), (40, -4), (100, 3), (160, 10), (214, 19), (258, 31)], 4.6, 1.8),                 # along the frame's top
    ([(100, 3), (150, 0), (204, 0), (256, 6), (304, 12), (350, 20), (392, 30)], 4.0, 1.6),        # out over the temple's corner
    ([(300, 12), (340, 8), (380, 6), (420, 10), (446, 18)], 3.4, 1.4),
    ([(24, 16), (44, 40), (56, 64), (60, 84)], 3.6, 1.5),                                         # hanging, short of the hill
    ([(74, 24), (94, 46), (104, 66), (106, 80)], 3.4, 1.4),
    ([(122, 36), (144, 56), (156, 74), (160, 86)], 3.2, 1.4),
    ([(170, 48), (198, 58), (222, 70), (238, 84)], 3.4, 1.4),
    ([(214, 56), (246, 62), (272, 76), (288, 92)], 3.2, 1.4),
    ([(-16, 36), (4, 58), (16, 88), (22, 118)], 3.6, 1.5),                                         # down beside the column
    ([(-24, 70), (6, 98), (18, 128), (22, 158)], 3.2, 1.4),
    ([(-20, 120), (8, 146), (20, 176), (24, 204)], 3.0, 1.3),
    ([(214, 19), (236, 36), (250, 56)], 2.8, 1.3),
    ([(60, 22), (84, 6), (116, -4)], 2.8, 1.3),
    ([(256, 6), (282, 22), (298, 42)], 2.8, 1.3),
    ([(330, 16), (346, 32), (354, 50)], 2.8, 1.3),
    ([(36, 96), (40, 112), (36, 128)], 2.6, 1.2),
    ([(140, 8), (170, 30), (186, 52)], 2.8, 1.3),
    ([(40, 4), (60, 26), (70, 46)], 2.8, 1.3),
]
KEEP_CLEAR = [((52, 140), 112), ((140, 200), 98)]          # (x range, lowest row a leaf may reach): Jupiter's temple, the hill
DARK = ["#1d2a1c", "#22311f", "#283823", "#2e3f26", "#24321e"]   # bay in the portico's shade: deep, warm
MID = ["#3a5032", "#425a36", "#4b6338"]
LIT = ["#7f9a4c", "#94ac56", "#a9bb62"]


def bough(cv, limbs, shoots, out_of, seed):
    """A bough of bay (rome_forum_near.bough, in shade: no buds, few leaves in the sun, close-set): `out_of(x)` says
    how far out of the portico's shade a place is (0 to 1)."""
    import math
    rng = np.random.default_rng(seed)
    deep, back_, front, lit = FN.Sheet2(SHAPE), FN.Sheet2(SHAPE), FN.Sheet2(SHAPE), FN.Sheet2(SHAPE)
    wood, wood_l = "#2a201b", "#5e4432"
    leaves = []

    def stem(pts_, w0, w1, sheet):
        cur = FN.curve(pts_, 10)
        n = len(cur)
        for i in range(n - 1):
            wd = lerp(w0, w1, i / max(n - 2, 1))
            sheet.line([cur[i], cur[i + 1]], wood, wd)
            sheet.line([(cur[i][0] - 0.3, cur[i][1] - wd * 0.30), (cur[i + 1][0] - 0.3, cur[i + 1][1] - wd * 0.30)], wood_l, max(0.7, wd * 0.26), 0.5)
        return cur

    for (pts_, w0, w1) in limbs:
        stem(pts_, w0, w1, back_)
    for si, (pts_, w0, w1) in enumerate(shoots):
        cur = stem(pts_, w0, w1, back_)
        n = len(cur)
        seg = [math.hypot(cur[i + 1][0] - cur[i][0], cur[i + 1][1] - cur[i][1]) for i in range(n - 1)]
        total = sum(seg)
        want, acc, i, side = 3.0, 0.0, 0, 1
        while i < n - 1:
            while acc + seg[i] >= want:
                t = (want - acc) / max(seg[i], 1e-6)
                px_, py_ = lerp(cur[i][0], cur[i + 1][0], t), lerp(cur[i][1], cur[i + 1][1], t)
                tang = math.atan2(cur[i + 1][1] - cur[i][1], cur[i + 1][0] - cur[i][0])
                along = want / total
                ang = tang + side * rng.uniform(0.28, 0.95) * (1 - 0.45 * along) + 0.20 * math.cos(tang)
                ln = rng.uniform(21.0, 29.0) * (rng.uniform(0.65, 1.0) if rng.random() < 0.6 else 1.0) * (0.9 + 0.15 * (1 - along))
                leaves.append((px_, py_, ang, ln, rng.random(), rng.uniform(-0.10, 0.10)))
                side = -side
                want += rng.uniform(3.4, 5.6)
            acc += seg[i]
            i += 1
        tip = cur[-1]
        tang = math.atan2(cur[-1][1] - cur[-2][1], cur[-1][0] - cur[-2][0])
        for d_ in (-0.55, -0.2, 0.15, 0.5):
            leaves.append((tip[0], tip[1], tang + d_ + rng.normal(0, 0.1), rng.uniform(22, 29), rng.random(), rng.uniform(-0.08, 0.08)))
    for (x, y, ang, ln, r_, curl) in leaves:
        tx = x + math.cos(ang) * ln * 0.6
        out_ = float(np.clip(out_of(tx), 0, 1))
        up_ = float(np.clip(-math.sin(ang) * 0.6 + 0.55, 0, 1))
        p_lit = 0.02 + 0.30 * out_ * (0.40 + 0.60 * up_)
        wide = rng.uniform(0.31, 0.38)
        if rng.random() < 0.65:                                                    # the leaf behind it, in the bough's own dark
            FN.laurel_leaf(deep, x + rng.normal(0, 2.5), y + rng.normal(0, 2.5), ang + rng.normal(0, 0.45), ln * rng.uniform(0.8, 1.05), DARK[int(rng.integers(2))], wide)
        if r_ < p_lit * 0.4:
            FN.laurel_leaf(lit, x, y, ang, ln, LIT[int(rng.integers(3))], wide, rib="#d8dc98", curl=curl)
        elif r_ < p_lit:
            FN.laurel_leaf(front, x, y, ang, ln, MID[int(rng.integers(3))], wide, rib="#5f7c48", curl=curl)
        elif r_ > 0.62:
            FN.laurel_leaf(back_, x, y, ang, ln, DARK[int(rng.integers(5))], wide, curl=curl)
        else:
            FN.laurel_leaf(front, x, y, ang, ln, DARK[int(rng.integers(5))], wide, rib="#33452c" if r_ > 0.50 else None, curl=curl)
    for sh in (deep, back_, front, lit):
        sc, sa = sh.done()
        cv.put(sc, sa)


def boughs(cv, seed=411):
    leaves = Canvas(SHAPE)
    bough(leaves, LIMBS, SHOOTS, lambda x: (x - 170) / 260.0, seed)
    c, a = leaves.straight()
    x, y = grid(SHAPE)
    for (x0, x1), low in KEEP_CLEAR:                                                # the far view stays clear
        a = a * (1 - ((x >= x0) & (x < x1)).astype(F32) * step(low, low + 6, y))
    c = c * np.array([1.10, 0.97, 0.84], dtype=F32)                                  # a frankly warm note in the darks
    cv.put(np.clip(c, 0, 1).astype(F32), a)


def fill_holes(c, a, most=60, tone=None):
    """No small specks of light shut in by the near plane's darks: holes under `most` pixels are filled with the
    darkest leaf tone round them."""
    hard = a > 0.5
    holes, n = ndimage.label(~hard)
    sizes = ndimage.sum(np.ones_like(holes), holes, index=np.arange(1, n + 1))
    small = np.isin(holes, np.where(sizes < most)[0] + 1) & ~hard
    if tone is None:
        tone = depth.near_tone("#1c3023", SHADE, 0.35, 0.05)
    c = np.where(small[..., None], tone, c)
    a = np.where(small, 1.0, a)
    return c.astype(F32), a.astype(F32)


def near_plane():
    cv = Canvas(SHAPE)
    boughs(cv)
    column(cv)
    c, a = cv.straight()
    c, a = fill_holes(c, a)
    hard = (a > 0.5).astype(F32)
    rim = depth.rim(hard, light=(1.0, -0.8), width=2.0) * 0.70 * (0.55 + 0.45 * noise(SHAPE, 30, 421, 3))
    c = c * (1 - rim[..., None]) + col(RIM) * rim[..., None]
    return np.clip(c, 0, 1).astype(F32), hard


# ================================================================ the backdrop
def masks():
    walk = mask_poly(SHAPE, WALK)
    steps = mask_poly(SHAPE, STEPS)
    x, y = grid(SHAPE)
    pave = np.clip(walk - steps, 0, 1)
    beyond = ((x < 245) & (y > 300) & (y < 445)).astype(F32)                       # the paving left of the temple, beyond the walk
    return np.clip(pave + beyond * (1 - walk), 0, 1).astype(F32), walk, steps


def shade_ratio(back):
    """How a shadow changes this paving's colour: the painter's own shaded paving over the sunlit (measured)."""
    sun = back[560:590, 560:640].reshape(-1, 3).mean(axis=0)
    shd = back[365:395, 140:200].reshape(-1, 3).mean(axis=0)
    return np.clip(shd / np.maximum(sun, 1e-3), 0.3, 1.8)


def capsule(a, b, r, n=10):
    """Ground places round the segment a-b (cm), radius r: a long shadow's outline."""
    ax, az = a
    bx, bz = b
    dx, dz = bx - ax, bz - az
    L = max(np.hypot(dx, dz), 1e-6)
    px, pz = -dz / L * r, dx / L * r
    ang0 = np.arctan2(pz, px)
    pts = [(ax + px, az + pz), (bx + px, bz + pz)]
    for t in np.linspace(0, np.pi, n):
        pts.append((bx + r * np.cos(ang0 - t), bz + r * np.sin(ang0 - t)))
    pts.append((ax - px, az - pz))
    return pts


def long_shadows(back, ground, seed=431):
    """The long morning shadows of tall things in the Forum out of the picture on our right (the sun is to the right and
    a little behind us): an honorary column and its statue, the largest, in from the bottom right corner; two more,
    farther off. -> the shadow mask (0 to 1)."""
    pt = lambda X, Z: CAM.pt(X, 0, Z)
    m = np.zeros(SHAPE, dtype=F32)
    things = [((1142.0, -73.0), 1000.0, 36.0, True),          # foot (X, z), height, radius, a statue on top
              ((1230.0, 225.0), 1100.0, 28.0, False),
              ((1074.0, 371.0), 700.0, 24.0, True)]
    for i, ((X, Z), hh, r, statue) in enumerate(things):
        tip = (X + CAST[0] * hh * 0.86, Z + CAST[1] * hh * 0.86)
        m = np.maximum(m, mask_poly(SHAPE, [pt(*p) for p in capsule((X, Z), tip, r)], soft=1.4, wobble=2.2, seed=seed + i))
        if statue:                                            # the statue's shadow at the end: a figure, its arm raised
            top = (X + CAST[0] * hh, Z + CAST[1] * hh)
            mid = (X + CAST[0] * hh * 0.93, Z + CAST[1] * hh * 0.93)
            body = capsule(tip, mid, r * 0.95, 8)
            head = capsule(mid, top, r * 0.55, 8)
            arm = capsule((mid[0] + 10, mid[1] - 26), (top[0] + 30, top[1] - 60), r * 0.22, 6)
            for j, part in enumerate((body, head, arm)):
                m = np.maximum(m, mask_poly(SHAPE, [pt(*p) for p in part], soft=1.2, wobble=0.8, seed=seed + 10 * i + j))
    m = m * ground
    ratio = shade_ratio(back)
    ratio = lerp(ratio, np.full(3, float(ratio.mean()), F32), 0.32) * 0.86          # (a cast shadow on warm stone: violet, not blue)
    far_soft = blur(m, 2.2)
    x, y = grid(SHAPE)
    m = lerp(m, far_soft, np.clip((600 - y) / 120.0, 0, 1))                          # the farther, the softer its edge
    deep = np.clip(back * ratio[None, None, :], 0, 1)
    edge = np.clip(1 - np.abs(blur(m, 1.2) - 0.5) * 2, 0, 1)                         # a warm edge where the sun is lost
    out = back * (1 - m[..., None] * 0.90) + deep * (m[..., None] * 0.90)
    out = out * (1 + 0.05 * edge[..., None] * np.array([1.0, 0.7, 0.2], dtype=F32))
    back[...] = np.clip(out, 0, 1)
    return m


def ground_texture(back, pave, seed=441):
    """Worn spots, chips at the joints and a few fine cracks in the paving, few and large near us, many and small far
    off, at a true density (depth.scatter)."""
    pt = lambda X, Z: CAM.pt(X, 0, Z)
    kk = lambda X, Z: CAM.scale(Z)
    zone = (pave > 0.5).astype(F32)
    dark, light = Sheet(SHAPE), Sheet(SHAPE)
    for (x, y, k, r) in depth.scatter(pt, kk, (-1500, 1500, -120, 2600), 0.9, seed, size=(9.0, 4.0), zone=zone):
        if r < 0.45:                                          # a chip out of a slab's edge
            w_, h_ = (4 + 7 * r) * k, (1.6 + 2 * r) * k
            dark.ellipse(x, y, max(w_, 0.5), max(h_ * 0.45, 0.4), "#5a4a52", 0.55)
        elif r < 0.75:                                        # a worn, paler patch
            w_ = (9 + 14 * r) * k
            light.ellipse(x, y, max(w_, 0.6), max(w_ * 0.28, 0.4), "#fff4dc", 0.30)
        else:                                                 # a fine crack
            ln = (12 + 20 * r) * k
            dark.line([(x - ln * 0.5, y + 0.15 * ln * (r - 0.85)), (x, y), (x + ln * 0.45, y - 0.1 * ln)], "#4e4048", max(0.5, 0.9 * k), 0.50)
    dc, da = dark.done()
    lc, la = light.done()
    da, la = da * zone, la * zone
    back[...] = back * (1 - da[..., None] * 0.55) + back * dc * 1.4 * (da[..., None] * 0.55)
    back[...] = back * (1 - la[..., None]) + lerp(back, lc, 0.45) * la[..., None]
    np.clip(back, 0, 1, out=back)


def ground_tone(back, pave):
    """The paving deepens toward us and pales toward the horizon."""
    x, y = grid(SHAPE)
    near_ = np.clip((y - 470) / 130.0, 0, 1) ** 1.2 * pave
    back[...] = back * (1 - near_[..., None] * np.array([0.10, 0.14, 0.16], dtype=F32))
    far_ = np.clip((470 - y) / 170.0, 0, 1) ** 1.3 * pave
    depth.air(back, far_, SKY, amount=0.14)


def far_layers(back):
    """The Forum and the hill behind it toward the sky's colour, layer by layer: the hill and Jupiter's temple most."""
    hill = blur(mask_poly(SHAPE, HILL), 1.2)
    forum = blur(mask_poly(SHAPE, FORUM), 1.2)
    x, y = grid(SHAPE)
    up = np.clip((304 - y) / 90.0, 0, 1)                      # in the Forum, the higher the farther
    depth.air(back, hill, SKY, amount=0.30)
    depth.air(back, forum * (0.06 + 0.16 * up), SKY, amount=1.0)


# ================================================================ finishing
def repalette_back(new, orig_idx, pal0, seed=451):
    """Back to 8 bits: the backdrop's own palette (rome_steps_palette) first, so that every pixel not changed keeps its
    index, and up to 64 more colours for the new shadows and the paled far layers."""
    old = pal0[orig_idx]
    changed = np.abs(new - old).max(axis=-1) > 1.5 / 255
    g = grain(new, seed, 0.010)
    extra = palette_of([g[changed].reshape(-1, 1, 3)], colors=64) if changed.sum() > 500 else np.zeros((0, 3), F32)
    pal = np.concatenate([pal0, extra]).astype(F32)
    idx = to_palette(g, pal, seed=5, speckle=0.010)
    idx = np.where(changed, idx, orig_idx).astype(np.uint8)
    return idx, pal, float(changed.mean())


def finish_cut(c, a, name, colors=64):
    return RS.finish(c, f"{OUT}/{name}", colors, a)


def deeper_front():
    """The old front plane (statue base and laurel bush) a little deeper and warmer, outline for outline: the same
    change to the palette of front.png, front-base.png and laurel.png (laid together they stay front.png)."""
    for name in ("front.png", "front-base.png", "laurel.png"):
        im = Image.open(f"{SRC}/{name}")
        t = im.info["transparency"]
        p = np.array(im.getpalette()[:3 * t], dtype=F32).reshape(-1, 3) / 255.0
        q = np.stack([depth.near_tone(c, SHADE, 0.22, 0.035) for c in p])
        out = im.copy()
        flat = (np.clip(q, 0, 1) * 255 + 0.5).astype(np.uint8).reshape(-1).tolist()
        out.putpalette(flat + im.getpalette()[3 * t:])
        out.save(f"{OUT}/{name}", optimize=True, transparency=t)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)                                 # every file as it was: the cut-outs, the frames, layout.json
    im = Image.open(f"{SRC}/back.png")
    orig_idx = np.asarray(im)
    pal0 = np.array(im.getpalette()[:3 * 160], dtype=F32).reshape(-1, 3) / 255.0
    back = pal0[orig_idx].astype(F32)
    pave, walk, steps = masks()
    far_layers(back)
    ground_tone(back, pave)
    ground_texture(back, pave)
    sh = long_shadows(back, pave)
    idx, pal, share = repalette_back(back, orig_idx, pal0)
    save(f"{OUT}/back.png", idx, pal)
    print("back: changed", round(share * 100, 1), "% of the pixels; shadow", round(float(sh.mean()) * 100, 1), "%; palette", len(pal))
    c, a = near_plane()
    print("near.png", finish_cut(c, a, "near.png", 72), "bytes; covers", round(float(a.mean()) * 100, 1), "%")
    deeper_front()
    # to look at: everything laid together
    whole = Image.open(f"{OUT}/back.png").convert("RGBA")
    for n in ("columns", "altar", "tripod", "stone", "cage-front", "front-base", "laurel", "near"):
        whole.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
    whole.convert("RGB").save("out/rome-steps-depth-look.png")


if __name__ == "__main__":
    main()

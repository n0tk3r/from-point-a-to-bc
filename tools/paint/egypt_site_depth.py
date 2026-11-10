"""The foot of the pyramid: the depth pass (round twenty-three, wave two: DEPTH.md), worked over the painting as it is.

    python3 egypt_site_depth.py         reads out/egypt-site-orig/ (the painting as installed, unkeyed: egypt_site.py's
                                        full run, never changed), writes the scene's full set into out/egypt-site/:
                                        every file as before, back.png deepened, and near.png

The scene's own light and camera (egypt_site_kit): the sun on the left and a little beyond the pyramid, shadows to the
right and 30 degrees toward us, 0.95 as long as the thing is tall; the eye 3.7 m up, the bottom row 8.5 m off.

near.png    a date palm by the track up from the river, just outside the picture on the left: its trunk across the top
            left corner and out through the left edge (39 cm at 5 m: 62 px), its fronds along the top and one hanging
            beside the trunk, all of it seen against the sun (egypt1_near's palm, the same tree as down by the river):
            deep warm darks, lit along the edges toward the sun. Clear of the small pyramids, the yard, the kites' circle
            and every place anyone stands.
back.png    the dappled shade of the next palm of that row, outside the picture on the left, lying in from the left edge
            over the sand round the water jars; the sledges' ruts and the footprints of the gangs across the trampled
            sand, few and large near us, many and small far off; limestone chips with their short shadows; the floor a
            little deeper toward us (the sunny spot kept in full sun, as the shade puzzle needs); the far desert, the
            queens' pyramids and the town moved toward the sky's colour at the horizon.
The cut-outs (awning, sledge, shade, front, streamers) and the kites' frames are copied as they were.
"""

import math
import os
import shutil

import numpy as np
from PIL import Image

from brush import F32, Sheet, blur, curve, grid, lerp, mask_poly, noise, over, palette_of, rgb, save, step, to_palette
import depth
from egypt_site_kit import EYE, FOC, HZ, P, SHADOW, floor_at, tint
import egypt1_near as palm

W, H = 800, 600
SHAPE = (H, W)
ORIG = "out/egypt-site-orig"
OUT = "out/egypt-site"
LIGHT = (-0.78, -0.62)                          # toward the sun, in the picture (egypt_site.py)
SKY_LOW = "#f8e6be"                             # the sky at the horizon (egypt_site.SKY)

# ---------------------------------------------------------------- the scene file's shapes (js/content/scenes/egypt-site.js)
WALK = [(0, 578), (0, 398), (120, 392), (212, 381), (248, 378), (318, 381), (405, 376), (487, 372), (515, 372), (616, 372), (635, 381),
        (670, 399), (696, 396), (731, 396), (752, 409), (800, 411), (800, 506), (722, 504), (612, 516), (552, 572), (544, 596), (122, 596), (112, 587)]
KEEP_OFF = [                                                     # things lying or standing on the sand: no rut or print over them
    [(507, 373), (589, 374), (591, 384), (617, 385), (636, 390), (636, 398), (592, 397), (507, 386)],                      # bricks
    [(392, 444), (400, 460), (300, 414), (226, 388), (222, 374), (300, 396)],                                              # rope
    [(394, 453), (424, 469), (559, 481), (568, 463), (552, 385), (478, 379), (442, 389), (443, 433), (415, 428), (398, 438)],  # sledge
    [(54, 475), (224, 473), (245, 437), (103, 439)],                                                                       # scribe's station
    [(57, 343), (241, 333), (244, 349), (239, 440), (221, 475), (62, 475)],                                                # awning
    [(356, 474), (388, 474), (388, 458), (356, 458)],                                                                      # a jar
    [(660, 362), (718, 362), (760, 414), (664, 406)],                                                                      # the foot of the steps
]
SUNSPOT = (330, 519)                                             # the sunny spot: kept in full sun and swept clear
KITES = (186, 74, 34, 14)                                        # the kites' circle (fx): kept clear of the fronds
SMALL_PYRAMIDS_TOP = 226                                         # nothing of the near plane below this on the left


def ground_mask():
    g = mask_poly(SHAPE, WALK, soft=1.0)
    for poly in KEEP_OFF:
        g = g * (1 - mask_poly(SHAPE, poly, soft=2.0))
    x, y = grid(SHAPE)
    spot = np.clip(1 - (((x - SUNSPOT[0]) / 58.0) ** 2 + ((y - SUNSPOT[1]) / 22.0) ** 2), 0, 1)
    return (g * (1 - step(0.0, 0.25, spot))).astype(F32)


def pt(X, Z):
    return P(X, 0.0, Z)


def k_at(X, Z):
    return FOC / Z


# ---------------------------------------------------------------- near.png: the palm
TOP_X, LEAN, R = 50.0, 0.40, 40.0


def axis(y):
    return TOP_X - LEAN * y + 2.5 * np.sin(np.clip(y, -140, 300) / 300.0 * math.pi)


FRONDS = [
    # the high fringe along the top, to the right: only the hanging blades come into the picture
    dict(rib=[(84, -52), (160, -54), (238, -42), (306, -20), (356, 6)], seed=5, long=78, wide=7.0, spread=62, thick=8.0, start=0.06, glow=0.26, pitch=6.0),
    # the long one, high over the kites and out along the top, its end coming down over the pyramid's sunlit edge
    dict(rib=[(96, -84), (200, -104), (306, -86), (384, -44), (430, 10)], seed=3, long=84, wide=7.2, spread=44, thick=10.0, start=0.42, glow=0.24),
    # one hanging beside the trunk, left of the kites' circle
    dict(rib=[(72, -56), (96, -10), (110, 46), (118, 104), (120, 168)], seed=7, long=62, wide=6.6, spread=38, thick=8.5, start=0.16, glow=0.20),
    # one over the corner, out through the left edge
    dict(rib=[(80, -60), (40, -44), (6, -14), (-26, 26)], seed=9, long=70, wide=6.8, spread=44, thick=8.5, start=0.10, glow=0.22),
    # and one low over the top, between the others, its end dipping toward the cloud
    dict(rib=[(84, -58), (128, -42), (166, -18), (190, 8)], seed=11, long=56, wide=6.4, spread=46, thick=7.5, start=0.20, glow=0.22),
]


def near_palm(seed=0):
    palm.TRUNK_TOP_X, palm.TRUNK_LEAN, palm.TRUNK_R = TOP_X, LEAN, R
    palm.trunk_axis = axis
    tc, ta = palm.trunk(seed=41)
    color = np.zeros(SHAPE + (3,), dtype=F32)
    alpha = np.zeros(SHAPE, dtype=F32)
    over(color, tc, (ta > 0.5).astype(F32))
    alpha = np.maximum(alpha, ta)
    for f in FRONDS:
        sheets = (Sheet(SHAPE), Sheet(SHAPE), Sheet(SHAPE))
        palm.frond(sheets, f["rib"], f["seed"] + seed, f.get("long", 84), f.get("wide", 7.0), f.get("spread", 44), f.get("sag", 0.20),
                   f.get("glow", 0.22), f.get("thick", 9.0), f.get("start", 0.0), f.get("pitch", 5.4))
        for sheet in sheets:
            c, a = sheet.done()
            over(color, c, (a > 0.5).astype(F32))
            alpha = np.maximum(alpha, a)
    # keep the kites' sky and the small pyramids clear
    x, y = grid(SHAPE)
    kx, ky, rx, ry = KITES
    clear = (((x - kx) / (rx + 10)) ** 2 + ((y - ky) / (ry + 10)) ** 2 < 1.0) | (y > SMALL_PYRAMIDS_TOP - 6)
    alpha = np.where(clear, 0.0, alpha).astype(F32)
    # warmer in the shade (the keying turns warm darks violet: a frankly warm note), and a hot rim toward the sun
    solid = alpha > 0.5
    lum = color @ np.array([0.3, 0.55, 0.15], dtype=F32)
    dark = (lum < 0.30) & solid
    warm = depth.near_tone(rgb("#5a3a1e"), shade="#241c30", k=0.35, warm=0.08)
    color[dark] = color[dark] * 0.82 + warm * 0.18
    rim = depth.rim(alpha, light=LIGHT, width=2.0) * solid
    over(color, rgb("#f6c878"), (rim * 0.55).astype(F32))
    return np.clip(color, 0, 1).astype(F32), alpha.astype(F32)


# ---------------------------------------------------------------- back.png
def palm_shade(seed=3):
    """The dappled shade of a palm outside the picture on the left, through the camera: the crown drawn on a map of the
    ground (2 cm to a pixel), its shadow moved by the sun, then looked at."""
    base, height = (-1040.0, 1460.0), 760.0
    cx, cz = base[0] + SHADOW[0] * height, base[1] + SHADOW[1] * height          # where the crown's shadow lies
    X0, Z0, cm = cx - 420.0, cz - 380.0, 2.0
    mw, mh = int(840 / cm), int(760 / cm)
    sheets = (Sheet((mh, mw), ss=2), Sheet((mh, mw), ss=2), Sheet((mh, mw), ss=2))
    rng = np.random.default_rng(seed)
    mx, my = (cx - X0) / cm, (cz - Z0) / cm
    for i in range(13):
        a = i * 2 * math.pi / 13 + rng.normal(0, 0.18)
        ln = (200 + 45 * rng.random()) / cm
        bend = rng.normal(0, 0.25)
        rib = [(mx + math.cos(a + bend * t) * ln * t, my + math.sin(a + bend * t) * ln * t) for t in (0.08, 0.35, 0.65, 1.0)]
        palm.frond(sheets, rib, seed + i, long=52 / cm, wide=7 / cm, spread=50, sag=0.05, glow=0.0, thick=9 / cm, start=0.05, pitch=9 / cm)
    m = np.zeros((mh, mw), dtype=F32)
    for s in sheets:
        m = np.maximum(m, s.done()[1])
    # the trunk's shadow, from the base to the crown's shadow
    t = Sheet((mh, mw), ss=2)
    bx, bz = (base[0] - X0) / cm, (base[1] - Z0) / cm
    t.line([(bx, bz), (mx, my)], "#000000", 36 / cm)
    m = np.maximum(m, t.done()[1])
    m = blur(m, 4.0)                                                               # the sun's own blur, 7 m down
    # look at it through the camera
    x, y = grid(SHAPE)
    yy = np.maximum(y, HZ + 1.0)
    Zc = EYE * FOC / (yy - HZ)
    X = (x - 400.0) * Zc / FOC
    u, v = (X - X0) / cm, (Zc - Z0) / cm
    inside = (u >= 0) & (u < mw - 1) & (v >= 0) & (v < mh - 1) & (y > HZ + 2)
    ui, vi = np.clip(u.astype(int), 0, mw - 1), np.clip(v.astype(int), 0, mh - 1)
    out = np.where(inside, m[vi, ui], 0.0).astype(F32)
    return blur(out, 0.9)


def ruts_and_prints(pic, ground, seed=21):
    rng = np.random.default_rng(seed)
    dark, lit = Sheet(SHAPE), Sheet(SHAPE)
    # the sledges' ruts: pairs of runners 95 cm apart, from the track up from the river toward the pyramid's foot, and
    # behind the sledge where it was dragged in
    paths = [
        [(-560, 860), (-470, 1120), (-330, 1420), (-150, 1800), (40, 2300), (180, 2900)],
        [(-300, 860), (-240, 1050), (-120, 1300), (40, 1600), (230, 1950), (420, 2300)],
        [(520, 860), (430, 1050), (330, 1280), (250, 1520), (200, 1800)],
        [(150, 860), (100, 1000), (-40, 1250), (-200, 1600), (-330, 1950)],
    ]
    for path in paths:
        pts = [(X + 8.0 * math.sin(Z / 150.0 + path[0][0]), Z) for X, Z in curve(path, 18)]       # a runner never ran straight
        for side in (-47.5, 47.5):
            line = []
            for i, (X, Z) in enumerate(pts):
                if i + 1 < len(pts):
                    dX, dZ = pts[i + 1][0] - X, pts[i + 1][1] - Z
                else:
                    dX, dZ = X - pts[i - 1][0], Z - pts[i - 1][1]
                n = math.hypot(dX, dZ) or 1.0
                line.append((X - dZ / n * side, Z + dX / n * side))
            seg = [(pt(X, Z), k_at(X, Z)) for X, Z in line]
            for (a, ka), (b, kb) in zip(seg, seg[1:]):
                w = max(0.6, 7.0 * (ka + kb) * 0.5)
                if rng.random() < 0.12:                                 # broken here and there, scuffed out
                    continue
                al = 0.13 + 0.10 * rng.random()
                dark.line([a, b], "#7a5236", w, al)
                o = max(0.6, 3.5 * (ka + kb) * 0.5)
                lit.line([(a[0] + o, a[1] + o * 0.3), (b[0] + o, b[1] + o * 0.3)], "#ffe3a8", w * 0.5, al * 0.6)
    # footprints: the gangs and the water carriers, thick along the ways they go, a few everywhere
    ways = [[(-430, 860), (-300, 1100), (-150, 1350), (-60, 1700)], [(-300, 1150), (-80, 1400), (200, 1650), (420, 1700)], [(-120, 900), (40, 1150), (260, 1400), (480, 1500)]]
    way_pts = [curve(w, 24) for w in ways]

    def near_way(X, Z):
        d = min(math.hypot(X - a, Z - b) for w in way_pts for a, b in w)
        return d < 120 or rng.random() < 0.18

    for x, y, k, r in depth.scatter(pt, k_at, (-900, 900, 860, 3400), 3.2, seed + 1, size=(11, 26), zone=ground, keep=near_way, most=2600):
        L, Wd = 25 * k, 10 * k
        if L < 1.6:
            continue
        a = rng.normal(0.6, 0.9)
        ca, sa = math.cos(a), math.sin(a) * 0.45                     # foreshortened on the ground
        foot = [(x + ca * L * 0.5 * c - (-sa) * Wd * 0.5 * s, y + sa * L * 0.5 * c + ca * 0.45 * Wd * 0.5 * s) for c, s in ((1, 0), (0.7, 1), (-0.7, 1), (-1, 0), (-0.7, -1), (0.7, -1))]
        dark.poly(foot, "#8a5a38", 0.22)
        lit.poly([(px + 0.6 + 0.08 * L, py + 0.5) for px, py in foot], "#fff0c8", 0.14)
    dc, da = dark.done()
    lc, la = lit.done()
    over(pic, dc, da * ground)
    over(pic, lc, la * ground)


def chips(pic, ground, seed=31):
    """Limestone chips from the dressing of the casing, with their short shadows toward us and to the right."""
    s = Sheet(SHAPE)
    rng = np.random.default_rng(seed)
    for x, y, k, r in depth.scatter(pt, k_at, (-900, 900, 860, 3400), 0.32, seed, size=(9, 9), zone=ground, most=400):
        sz = (4 + 9 * r) * k
        if sz < 1.2:
            continue
        sx, sy = SHADOW[0] * sz * 0.9, -SHADOW[1] * sz * 0.35
        s.ellipse(x + sx * 0.6, y + sy * 0.6 + 0.4, sz * 0.75, sz * 0.32, "#7d5a6a", 0.30)
        pts = [(x + math.cos(t) * sz * 0.5 * (0.7 + 0.5 * rng.random()), y + math.sin(t) * sz * 0.28 * (0.7 + 0.5 * rng.random()) - sz * 0.12) for t in np.linspace(0, 2 * math.pi, 6, endpoint=False)]
        s.poly(pts, lerp(rgb("#dcbf8c"), rgb("#f2dcb0"), rng.random()))
    c, a = s.done()
    over(pic, c, a * ground)


def far_air(pic):
    """The desert, the queens' pyramids, the town and the river toward the sky at the horizon: left of the pyramid."""
    x, y = grid(SHAPE)
    edge = np.interp(y, [0, 250, 274, 300, 336], [345, 182, 165, 200, 270])           # the pyramid's left outline
    left = step(0.0, -14.0, x - edge)
    far = np.clip((330.0 - y) / 70.0, 0, 1) ** 0.8 * step(196.0, 226.0, y)
    depth.air(pic, far * left, SKY_LOW, amount=0.26)


def deepen(pic):
    ground = ground_mask()
    x, y = grid(SHAPE)
    # the floor a little deeper toward us, warm (the sunny spot kept)
    t = np.clip((y - 372.0) / 228.0, 0, 1) ** 1.1
    walk = mask_poly(SHAPE, WALK, soft=2.0)
    spot = np.clip(1 - (((x - SUNSPOT[0]) / 64.0) ** 2 + ((y - SUNSPOT[1]) / 26.0) ** 2), 0, 1)
    deep = t * 0.26 * walk * (1 - step(0.0, 0.3, spot))
    pic[...] = pic * (1 - deep[..., None]) + pic * rgb("#b07850")[None, None, :] * deep[..., None]
    # the next palm's shade, lying in from the left
    sh = palm_shade() * walk
    tint(pic, "#6e5688", sh * 0.42)
    over(pic, "#6f5c96", sh * 0.08)
    ruts_and_prints(pic, ground)
    chips(pic, ground)
    far_air(pic)
    return np.clip(pic, 0, 1)


# ---------------------------------------------------------------- the files
def load_rgb(path):
    return np.asarray(Image.open(path).convert("RGB"), dtype=F32) / 255


def write_back(new):
    im = Image.open(ORIG + "/back.png")
    old_idx = np.asarray(im)
    old_pal = np.asarray(im.getpalette()[: 3 * (int(old_idx.max()) + 1)], dtype=F32).reshape(-1, 3) / 255
    old = old_pal[old_idx]
    changed = np.abs(new - old).max(axis=2) > 1.5 / 255
    room = 255 - len(old_pal)
    add = palette_of([new[changed].reshape(-1, 1, 3)], colors=min(room, 100))
    pal = np.concatenate([old_pal, add]).astype(F32)
    idx = old_idx.astype(np.uint8).copy()
    part = to_palette(new[changed].reshape(-1, 1, 3), pal, speckle=0.008)
    idx[changed] = part[:, 0]
    save(OUT + "/back.png", idx, pal)
    return int(changed.sum())


def write_cut(name, color, alpha, colors):
    solid = alpha > 0.5
    pal = palette_of([color[solid].reshape(-1, 1, 3)], colors=colors)
    idx = to_palette(color, pal, speckle=0.010)
    save(OUT + "/" + name + ".png", idx, pal, alpha)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(ORIG):
        if f != "back.png":
            shutil.copyfile(os.path.join(ORIG, f), os.path.join(OUT, f))
    pic = deepen(load_rgb(ORIG + "/back.png"))
    print("back: changed", write_back(pic))
    c, a = near_palm()
    write_cut("near", c, a, 72)
    print("near: share", round(float((a > 0.5).mean()) * 100, 1))
    comp = Image.open(OUT + "/back.png").convert("RGBA")
    for n in ("streamers", "awning", "sledge", "front", "near"):
        comp.alpha_composite(Image.open(OUT + "/" + n + ".png").convert("RGBA"))
    comp.convert("RGB").save("out/egypt-site-depth-comp.png")

"""Across the Tiber (rome-tiber), the depth pass (round twenty-three, DEPTH.md): worked over the finished painting.

Reads out/rome-tiber-orig/ (rome_tiber.py's full run, never changed) and writes the scene's full set back into
out/rome-tiber/, every file as before plus near.png:

  near.png    the front plane: a fig leaning out over the river by the bridgehead, close by the lens on our left, its
              smooth trunk up the left edge (we see only its shaded side: the sun is low over the far bank, ahead and to
              the left) and its boughs across the top in first leaf, every edge that faces the sun lit; reeds at the
              bank's lip beside the steps down into the water, where nobody walks.
  back.png    deepened: the long morning shadow of a poplar on the landing's outer corner (out of the picture on the
              left) laid across the landing and the square toward us and to the right, its crown's shade dappled where
              it reaches the bottom of the frame; ruts, stones and joints on the lane and the road through the camera,
              big and few near us, small and many far off; the far bank, its hill and city, and the far end of the road
              moved toward the sky's colour at the horizon; the near ground a little deeper.
  the rest    as they were (window-wall.png cut again from the new backdrop, so laid over it, it still changes nothing).

  python3 rome_tiber_depth.py
"""
import math
import os
import shutil

import numpy as np
from PIL import Image

from brush import *
import depth
import rome_tiber_model as M

ORIG = "out/rome-tiber-orig"
OUT = "out/rome-tiber"
SHAPE = (600, 800)
H, W = SHAPE
LIGHT = (-0.88, -0.48)                                       # toward the sun in the picture (rome_tiber.SKY_LIGHT)
SUN_G = (M.SUN[0], M.SUN[2])
_n = math.hypot(*SUN_G)
DOWN_SUN = (-SUN_G[0] / _n, -SUN_G[1] / _n)                   # a shadow's way on the ground (X, Z): right, and toward us
TAN = M.SUN[1] / math.hypot(M.SUN[0], M.SUN[2])               # height to shadow length: L = h / TAN

WALK = [[29, 598], [131, 497], [0, 497], [1, 497], [1, 462], [22, 452], [174, 452], [287, 341], [410, 341], [422, 377], [416, 379], [541, 418], [549, 418], [602, 434], [507, 446], [513, 448], [532, 456], [552, 464], [574, 473], [599, 482], [625, 492], [653, 504], [685, 516], [719, 530], [758, 545], [798, 561], [798, 598]]
ROAD = [[252, 375], [429, 375], [392, 280], [348, 280]]
FARBANK = [[0, 148], [40, 146], [90, 154], [140, 168], [190, 186], [240, 212], [290, 234], [330, 244], [370, 250], [372, 256], [240, 260], [120, 266], [0, 272]]
GARDENS = [[300, 214], [442, 206], [442, 262], [300, 262]]


def pt(X, Z):
    x, y = M.CAM.pt(X, 0, Z)[:2]
    return (float(x), float(y))


def k_at(X, Z):
    return float(M.CAM.scale(Z))


def load_rgb(path):
    return np.asarray(Image.open(path).convert("RGB"), dtype=F32) / 255.0


# ---------------------------------------------------------------- the back: shadows, texture, air
def ground_mask():
    g = np.maximum(mask_poly(SHAPE, WALK, soft=1.5), mask_poly(SHAPE, ROAD + [[380, 262]], soft=1.0))
    return np.clip(g, 0, 1).astype(F32)


def poplar_shadow(pic, ground):
    """The poplar on the landing's outer corner, out of the picture on the left: its trunk's shadow runs from the
    landing across the square toward us and to the right; its crown's, dappled, comes in at the bottom of the frame."""
    bx, bz = -705.0, 560.0
    dx, dz = DOWN_SUN
    px_, pz_ = -dz, dx                                                       # across the shadow
    crown0, crown1 = 380.0 / TAN, 1750.0 / TAN                              # the crown from 3.8 m up to 17.5 m
    def at(t, s):
        return (bx + dx * t + px_ * s, bz + dz * t + pz_ * s)
    def clip_z(p):
        return (p[0], max(p[1], -70.0))
    trunk = [at(0, -26), at(crown0, -17), at(crown0, 17), at(0, 26)]
    trunk = [clip_z(p) for p in trunk]
    m = mask_poly(SHAPE, [pt(*p) for p in trunk], soft=1.4, wobble=0.8, seed=41)
    side = []
    n = 24
    for i in range(n + 1):
        t = crown0 + (crown1 - crown0) * i / n
        u = i / n
        side.append(150.0 * math.sin(math.pi * min(1.0, 0.18 + u * 0.95)) ** 0.7 + 30)
    left = [clip_z(at(crown0 + (crown1 - crown0) * i / n, -side[i])) for i in range(n + 1)]
    right = [clip_z(at(crown0 + (crown1 - crown0) * i / n, side[i])) for i in range(n + 1)]
    crown = mask_poly(SHAPE, [pt(*p) for p in left + right[::-1]], soft=4.0, wobble=3.0, seed=42)
    dapple = noise(SHAPE, 22, 43, 4)
    crown = crown * np.clip((dapple - 0.30) * 3.2, 0.25, 1.0)                # flecks of sun through the leaves
    m = np.clip(np.maximum(m, crown * 0.85), 0, 1) * ground
    c = rgb("#4a4470") * 1.5
    k = (m * 0.40)[..., None]
    pic[...] = np.clip(pic * (1 - k) + pic * c * k, 0, 1)
    return m


def texture(pic, ground, seed=51):
    """Ruts along the road, stones and the joints of old paving on the lane, through the camera."""
    rng = np.random.default_rng(seed)
    sh = Sheet(SHAPE)
    hi = Sheet(SHAPE)
    # two cart ruts from the bridgehead along the road to the far end, a little wandering
    for X0 in (-95.0, 45.0):
        pts, ws = [], []
        for Z in np.concatenate([np.linspace(-40, 600, 30), np.linspace(620, 3200, 30)]):
            X = X0 + 9.0 * math.sin(Z / 410.0 + X0) + 4.0 * math.sin(Z / 97.0)
            pts.append(pt(X, Z))
            ws.append(14.0 * k_at(X, Z))
        for i in range(len(pts) - 1):
            if rng.random() < 0.82:                                                             # worn away in places
                sh.line([pts[i], pts[i + 1]], "#4a4060", max(0.6, ws[i]), 0.17)
    # stones, big and few near us, small and many far off
    for (x, y, k, r) in depth.scatter(pt, k_at, (-420.0, 760.0, -40.0, 5200.0), 0.9, seed + 1, size=(9.0, 6.0), zone=ground):
        s = (5.0 + 10.0 * r) * k
        if s < 0.7:
            continue
        sh.ellipse(x + s * 0.45, y + s * 0.22, s * 0.62, s * 0.30, "#3e3450", 0.30)              # its shadow, right and toward us
        g = pic[min(int(y), H - 1), min(int(x), W - 1)]
        body = np.clip(g * (0.86 + 0.22 * ((r * 7.3) % 1.0)), 0, 1)
        sh.ellipse(x, y, s * 0.55, s * 0.30, body, 0.9)
        hi.ellipse(x - s * 0.18, y - s * 0.10, s * 0.28, s * 0.12, "#fff1d6", 0.28)              # lit on the sun's side
    # tufts at the foot of the house fronts and along the quay, where feet do not go
    for (x, y, k, r) in depth.scatter(pt, k_at, (-420.0, 760.0, -40.0, 3000.0), 0.35, seed + 2, size=(14.0, 10.0), zone=ground):
        s = (8.0 + 8.0 * r) * k
        if s < 1.2:
            continue
        for j in range(4):
            a = -math.pi / 2 + (j - 1.5) * 0.35 + rng.normal(0, 0.1)
            sh.line([(x + j * s * 0.15, y), (x + j * s * 0.15 + math.cos(a) * s, y + math.sin(a) * s)], "#5e6a3a" if r > 0.5 else "#6e6a40", max(0.6, s * 0.12), 0.75)
    # the joints of the old paving at the bridgehead (near us only)
    for Z in np.arange(-40.0, 700.0, 62.0):
        X0, X1 = -400.0, 700.0
        a, b = pt(X0, Z), pt(X1, Z)
        if rng.random() < 0.7:
            sh.line([a, b], "#463c56", max(0.6, 2.2 * k_at(0, Z)), 0.16)
    for X in np.arange(-380.0, 700.0, 85.0):
        for Z in np.arange(-40.0, 700.0, 62.0):
            if rng.random() < 0.45:
                X2 = X + rng.uniform(-20, 20)
                sh.line([pt(X2, Z), pt(X2, Z + 62.0)], "#463c56", max(0.6, 2.0 * k_at(X2, Z)), 0.14)
    for s_ in (sh, hi):
        c, a = s_.done()
        over(pic, c, a * ground)


def far_air(pic):
    """The far bank, its hill and city, and the far end of the road: toward the sky's colour at the horizon."""
    sky = (rgb("#bdd3e8") + rgb("#c1dff5")) / 2
    fb = mask_poly(SHAPE, FARBANK, soft=3.0)
    gd = mask_poly(SHAPE, GARDENS, soft=3.0)
    x, y = grid(SHAPE)
    hill = np.clip((272 - y) / 126.0, 0, 1)                                 # the hill's top is the farthest of the bank
    far = fb * (0.55 + 0.45 * hill) + gd * 0.75
    far = np.clip(far, 0, 1)
    depth.air(pic, far, sky, amount=0.26, power=1.0)
    road_far = mask_poly(SHAPE, [[300, 341], [470, 341], [410, 262], [360, 262]], soft=6.0) * np.clip((341 - y) / 79.0, 0, 1)
    depth.air(pic, road_far, sky, amount=0.22)


# ---------------------------------------------------------------- the near plane
BARK = "#8a6448"
BARK_DARK = "#2a1a1a"
LEAF = "#6c8a3e"
LEAF_DEEP = "#3c4a2c"
LIT = "#ffdca0"


def trunk_edge(y):
    """Where the fig's trunk ends on the right (it leans out of the picture to the left as it goes down)."""
    pts = [(0, 76), (60, 70), (140, 60), (200, 50), (260, 40), (330, 26), (400, 19), (470, 17), (540, 14), (600, 12)]
    ys = [p[0] for p in pts]
    xs = [p[1] for p in pts]
    return float(np.interp(y, ys, xs))


def near(seed=61):
    rng = np.random.default_rng(seed)
    wood = Sheet(SHAPE)
    leaves_back = Sheet(SHAPE)
    leaves = Sheet(SHAPE)
    lit = Sheet(SHAPE)
    deep = near_c = depth.near_tone(BARK, shade=BARK_DARK, k=0.60, warm=0.07)
    mid = depth.near_tone(BARK, shade=BARK_DARK, k=0.45, warm=0.08)
    # the trunk: its edge a little bumpy, the near side smooth
    edge = []
    for y in np.arange(-4, 606, 6):
        edge.append((trunk_edge(y) + 1.6 * math.sin(y / 23.0) + rng.normal(0, 0.5), float(y)))
    wood.poly([(-10, -4)] + edge + [(-10, 606)], deep)
    # fig bark: soft pale streaks and the creases round the trunk, on the shaded side
    for i in range(26):
        y0 = rng.uniform(0, 600)
        xr = trunk_edge(y0)
        x0 = rng.uniform(1, max(2, xr - 4))
        wood.line([(x0, y0), (x0 + rng.uniform(-2, 2), y0 + rng.uniform(14, 40))], lerp(deep, mid, 0.6), rng.uniform(1.0, 2.4))
    for i in range(22):
        y0 = rng.uniform(0, 600)
        xr = trunk_edge(y0)
        wood.line([(0, y0), (xr * rng.uniform(0.5, 0.95), y0 + rng.uniform(-3, 3))], lerp(deep, rgb("#1e1416"), 0.5), 1.0)
    # the boughs: one up and out of the top of the frame, one sweeping along the top to the right
    b1 = curve([(40, 210), (70, 150), (110, 80), (150, 20), (172, -10)], 30)
    b2 = curve([(50, 120), (130, 92), (230, 58), (330, 34), (430, 14), (520, -6)], 40)
    b3 = curve([(70, 172), (105, 160), (140, 154)], 20)
    wood.taper(b1, deep, 34, 20)
    wood.taper(b2, deep, 20, 6)
    wood.taper(b3, deep, 12, 3)
    twigs = []
    for base, n in ((b2, 14), (b1, 7), (b3, 4)):
        for j in range(n):
            p = base[int(len(base) * (0.25 + 0.7 * j / max(n - 1, 1))) - 1]
            ang = rng.uniform(-0.3, 1.2) * (1 if rng.random() < 0.7 else -1) + math.pi / 2 * 0.6
            ln = rng.uniform(28, 60)
            q = (p[0] + math.cos(ang) * ln * 0.8 + rng.uniform(-10, 10), p[1] + math.sin(ang) * ln * 0.6)
            wood.line([p, q], deep, rng.uniform(2.0, 4.0))
            twigs.append(q)
            twigs.append(((p[0] + q[0]) / 2, (p[1] + q[1]) / 2))
    # the young leaves in clusters at the twigs' ends and along the boughs: solid clusters, no light shut inside them
    spots = twigs + [(20, 40), (62, 22), (104, 48), (30, 96), (130, 18), (200, 8), (165, 62), (245, 34), (300, 52), (362, 22), (420, 34), (474, 12), (90, 112)] + [b2[i] for i in range(4, len(b2), 3)] + [b1[i] for i in range(10, len(b1), 4)]
    for (cx, cy) in spots:
        if cy > 132 and cx > 40:
            continue
        nleaf = int(rng.integers(9, 15))
        for j in range(nleaf):
            a = rng.uniform(0, 2 * math.pi)
            d = rng.uniform(0, 16)
            lx, ly = cx + math.cos(a) * d, cy + math.sin(a) * d * 0.8 + 3
            r = rng.uniform(7.5, 12.0)
            ang = rng.uniform(0, math.pi)
            leaves_back.ellipse(lx + 2, ly + 2, r * 1.05, r * 0.85, depth.near_tone(LEAF_DEEP, shade=BARK_DARK, k=0.45, warm=0.03))
            tone = depth.near_tone(LEAF, shade=BARK_DARK, k=rng.uniform(0.58, 0.72), warm=0.06)
            leaves.ellipse(lx, ly, r, r * 0.78, tone)
            # three lobes, as a fig leaf has
            for lb in (-0.9, 0.0, 0.9):
                leaves.ellipse(lx + math.cos(ang + lb) * r * 0.8, ly + math.sin(ang + lb) * r * 0.6, r * 0.45, r * 0.38, tone)
    # reeds at the bank's lip beside the steps into the water
    for i in range(30):
        x0 = rng.uniform(-6, 46)
        top = rng.uniform(515, 575) + x0 * 0.35
        lean = rng.uniform(-6, 12)
        w0 = rng.uniform(2.0, 3.6)
        cur = curve([(x0, 606), (x0 + lean * 0.4, (606 + top) / 2), (x0 + lean, top)], 10)
        tone = depth.near_tone("#7a8a46" if rng.random() < 0.6 else "#9a8a52", shade=BARK_DARK, k=rng.uniform(0.55, 0.70), warm=0.07)
        leaves.taper(cur, tone, w0, 0.6)
        if rng.random() < 0.5:
            lit.taper([(p[0] - w0 * 0.3, p[1]) for p in cur[3:]], LIT, 0.8, 0.4, 0.5)
    c = np.zeros(SHAPE + (3,), F32)
    a = np.zeros(SHAPE, F32)
    for s_ in (wood, leaves_back, leaves, lit):
        sc, sa = s_.done()
        c = c * (1 - sa[..., None]) + sc * sa[..., None]
        a = a + sa * (1 - a)
    hard = (a > 0.5).astype(F32)
    cs = np.where(a[..., None] > 1e-4, c / np.maximum(a[..., None], 1e-4) * np.minimum(a[..., None], 1), c)
    cs = c / np.maximum(a, 1e-4)[..., None]
    cs = np.clip(cs, 0, 1)
    # the rim: every edge that faces the low sun over the far bank, warm and broken
    rm = depth.rim(hard, light=LIGHT, width=2.2) * (0.55 + 0.45 * noise(SHAPE, 30, 66, 3))
    cs = cs * (1 - rm[..., None] * 0.85) + rgb(LIT) * (rm[..., None] * 0.85)
    # warm light thrown up from the sunlit lane on the trunk's foot, a little
    up = np.clip((np.arange(H, dtype=F32)[:, None] - 380) / 220.0, 0, 1) * np.ones(SHAPE, F32)
    cs = cs * (1 - up[..., None] * 0.10) + rgb("#a87a58") * (up[..., None] * 0.10)
    return cs.astype(F32), hard


# ---------------------------------------------------------------- the files
def finish_cut(color, alpha, path, colors, seed=7):
    g = grain(color, seed, 0.02)
    pal = palette_of([g[alpha > 0.5].reshape(-1, 1, 3)], colors=colors)
    idx = to_palette(g, pal, speckle=0.014)
    save(path, idx, pal, alpha)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(ORIG):
        shutil.copy2(os.path.join(ORIG, f), os.path.join(OUT, f))
    pic = load_rgb(f"{ORIG}/back.png")
    ground = ground_mask()
    depth.frame(pic, amount=0.10, bottom=0.10)
    poplar_shadow(pic, ground)
    texture(pic, ground)
    far_air(pic)
    pal = palette_of([pic], colors=160)
    idx = to_palette(pic, pal, speckle=0.008)
    save(f"{OUT}/back.png", idx, pal)
    # the window wall: cut again from the new backdrop with its old outline
    ww = np.asarray(Image.open(f"{ORIG}/window-wall.png").convert("RGBA"), dtype=F32)[..., 3] / 255.0
    save(f"{OUT}/window-wall.png", idx, pal, ww)
    c, a = near()
    finish_cut(c, a, f"{OUT}/near.png", 64)
    print("near covers %.1f%%" % (a.mean() * 100))
    look = pal[idx].copy()
    for name in ("well", "window-wall", "washing", "barge", "curb", "fence-corner", "fence", "landing-edge", "near"):
        im = np.asarray(Image.open(f"{OUT}/{name}.png").convert("RGBA"), dtype=F32) / 255.0
        over(look, im[..., :3], (im[..., 3] > 0.5).astype(F32))
    Image.fromarray((np.clip(look, 0, 1) * 255).astype(np.uint8)).save("out/rome-tiber-depth-look.png")

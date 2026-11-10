"""The Office's lot: the depth pass (round twenty-three, wave two: DEPTH.md), worked over the painting as it is.
    python3 office_lot_depth.py     reads out/office-lot-orig/ (office_lot.py's full run, never changed) and writes the
                                    scene's full set into out/office-lot/: every file as before, back.png deepened,
                                    front.png a little deeper and warmer, and near.png
The scene's own camera and light (office_lot_kit): the lens 4.9 m up, square on; early afternoon, the sun high, behind
us and to the left: shadows fall right and back (SUN 0.333, 0.800 per cm of height).
near.png    the lot's light pole, a creosoted wooden pole 4 m from the lens up the right edge of the frame, its flood lamp
            on a bracket against the sky at the top; behind it the end of the lot's near fence (its last post, top rail
            and chain-link) across the bottom right corner, and the gravel's edge there: the pad's raised lip, the bare
            desert beyond it, sagebrush and dry tufts. In shade and warm, lit along the edges toward the sun (left).
back.png    the dappled shade of a tamarisk outside the picture on the left lying in over the gravel at the left; the
            building's shadow glazed once more; old tire tracks from the gate to the corner and stones with their
            short shadows, few and large near us, many and small far off; the near gravel a little deeper; the desert,
            the fence line and the far range moved toward the sky's colour.
The other cut-outs and the fan's and pennant's frames are copied as they were.
"""
import math
import os
import shutil
import sys
import numpy as np
from PIL import Image
from brush import F32, Sheet, blur, curve, grain, grid, lerp, mask_poly, noise, over, palette_of, rgb, save, step, tint, to_palette
import depth
import office_lot_kit as K
from nevada_roadside_kit import Paper, sagebrush, tuft

W, H = 800, 600
SHAPE = (H, W)
ORIG = os.environ.get("ORIG", "out/office-lot-orig")
OUT = os.environ.get("OUTDIR", "out/office-lot")
LIGHT = (-0.85, -0.55)                                  # toward the sun in the picture: left, and up
SUNX, SUNZ = K.SUN

# ---------------------------------------------------------------- the scene file's shapes (js/content/scenes/office-lot.js)
GRAVEL = [(0, 393.1), (88, 393.1), (88, 430.2), (500.7, 430.2), (488.7, 395.5), (800, 395.5), (800, 597), (0, 597)]
KEEP_OFF = [
    [(248, 444), (311, 444), (311, 427), (252, 427)],                                   # the mat
    [(76, 446), (116, 446), (116, 428), (76, 428)],                                     # the flagpole's foot
    [(366, 442), (408, 442), (408, 424), (366, 424)],                                   # the can by the wall
    [(492, 400), (800, 400), (800, 360), (492, 360)],                                   # under the limousine
]


def pt(X, Z):
    return K.P(X, 0.0, Z)


def k_at(X, Z):
    return K.k_at(Z)


def ground_mask():
    g = mask_poly(SHAPE, GRAVEL, soft=1.0)
    for poly in KEEP_OFF:
        g = g * (1 - mask_poly(SHAPE, poly, soft=2.0))
    return g.astype(F32)


# ---------------------------------------------------------------- near.png
POLE_X0, POLE_X1 = 754.0, 812.0                         # the pole: 28 cm at 4 m (1.9 px to the cm)
FENCE_TOP = 480.3                                       # the near fence (z -150): its top rail's row
POST_X = 600.0                                          # its last post
EDGE = [(500, 602), (548, 592), (606, 574), (662, 554), (716, 536), (762, 521), (804, 508), (804, 602)]   # the gravel's edge


def pole(seed=3):
    """The wooden light pole, its flood lamp and bracket. -> (colour, alpha)"""
    x, y = grid(SHAPE)
    cx, r = (POLE_X0 + POLE_X1) / 2, (POLE_X1 - POLE_X0) / 2
    u = (x - cx) / r                                                    # -1 at its left edge, 1 at its right
    a = np.clip((1.0 - np.abs(u)) * r / 1.2, 0, 1)
    a = np.where(u < 1.0, a, 0.0).astype(F32)
    # round: lit at its front-left (the sun is behind us, left), falling into deep shade to the right
    th = np.arcsin(np.clip(u, -1, 1))
    lit = np.clip(np.cos(th + 0.42) * 1.1 - 0.15, 0, 1)
    wood = rgb("#4a3324")
    grainmap = noise(SHAPE, (3, 90), seed, octaves=3)                   # long checks and streaks up the wood
    c = wood[None, None, :] * (0.50 + 0.45 * lit[..., None]) * (0.85 + 0.3 * grainmap[..., None])
    # checks: a few dark cracks running up the pole
    for cxk, w_ in ((cx - 9, 1.1), (cx + 4, 0.9), (cx - 15, 0.7)):
        crack = np.clip(1 - np.abs(x - cxk - 1.5 * np.sin(y / 70.0 + cxk)) / w_, 0, 1) * (noise(SHAPE, (4, 60), seed + int(cxk), octaves=2) > 0.45)
        c = c * (1 - 0.45 * crack[..., None])
    c = np.clip(c, 0, 1).astype(F32)
    # a galvanized step and the pole's tag, small
    s = Sheet(SHAPE)
    s.line([(POLE_X0 + 6, 300), (POLE_X0 - 14, 296)], "#3a3836", 4.0)
    s.line([(POLE_X0 + 6, 299), (POLE_X0 - 12, 295)], "#9a948a", 1.2, 0.8)
    s.poly([(POLE_X0 + 10, 250), (POLE_X0 + 26, 250), (POLE_X0 + 26, 262), (POLE_X0 + 10, 262)], "#6c6a66")
    # the flood lamp on its bracket, against the sky: we see its back and top, its glass turned to the lot
    s.line([(POLE_X0 + 4, 64), (POLE_X0 - 30, 56), (POLE_X0 - 44, 50)], "#2e2622", 7.0)
    s.line([(POLE_X0 + 4, 92), (POLE_X0 - 26, 58)], "#2e2622", 4.0)
    lamp = [(POLE_X0 - 92, 30), (POLE_X0 - 46, 22), (POLE_X0 - 34, 36), (POLE_X0 - 36, 58), (POLE_X0 - 84, 66), (POLE_X0 - 96, 52)]
    s.poly(lamp, "#3a302c")
    s.poly([(POLE_X0 - 96, 52), (POLE_X0 - 84, 66), (POLE_X0 - 74, 64), (POLE_X0 - 88, 48)], "#5c5650")     # the glass's edge, dull by day
    s.line([(POLE_X0 + 4, 128), (POLE_X0 - 24, 124), (POLE_X0 - 36, 120)], "#2e2622", 6.0)                 # a second, lower
    lamp2 = [(POLE_X0 - 80, 104), (POLE_X0 - 40, 98), (POLE_X0 - 30, 110), (POLE_X0 - 32, 128), (POLE_X0 - 72, 134), (POLE_X0 - 84, 122)]
    s.poly(lamp2, "#3a302c")
    s.poly([(POLE_X0 - 84, 122), (POLE_X0 - 72, 134), (POLE_X0 - 64, 132), (POLE_X0 - 76, 118)], "#5c5650")
    for i in range(4):                                                  # the cooling fins along its back
        s.line([(POLE_X0 - 88 + i * 11, 27 - i * 1.5), (POLE_X0 - 82 + i * 11, 40 - i * 1.5)], "#26201e", 1.6)
    s.line([(POLE_X0 - 30, 300), (POLE_X0 - 30, 300)], "#000000", 0.1, 0.0)
    # the crossarm at the top, out through the top edge, its insulators against the sky
    s.poly([(POLE_X0 - 150, -4), (812, -4), (812, 13), (POLE_X0 - 150, 11)], "#3a2a20")
    s.line([(POLE_X0 - 150, 10.5), (POLE_X0 - 8, 12.5)], "#241a14", 2.0)
    for ix in (POLE_X0 - 136, POLE_X0 - 92):
        s.line([(ix, 2), (ix, -6)], "#5a5450", 5.0)
    s.line([(POLE_X0 - 40, 12), (POLE_X0 + 2, 46)], "#2e2622", 3.5)                   # its brace
    # the conduit up the pole's right side, into shade
    s.line([(POLE_X1 - 12, 610), (POLE_X1 - 12, -10)], "#2a2826", 4.0)
    sc, sa = s.done()
    over(c, sc, sa)
    a = np.maximum(a, sa)
    return c, a


def fence_and_edge(seed=11):
    """The end of the near fence across the bottom right corner, and the gravel's edge with sage and tufts behind it."""
    color = np.zeros(SHAPE + (3,), dtype=F32)
    alpha = np.zeros(SHAPE, dtype=F32)
    x, y = grid(SHAPE)
    # the bare desert beyond the gravel's edge, in the fence's broken shade, and the pad's raised lip along it
    g = mask_poly(SHAPE, EDGE, soft=1.2, wobble=3.0, seed=seed)
    n = noise(SHAPE, 18, seed + 1, octaves=4)
    soil = lerp(rgb("#6e5440"), rgb("#94745a"), n[..., None]) * (0.82 + 0.18 * noise(SHAPE, 4, seed + 2, octaves=2)[..., None])
    over(color, soil.astype(F32), g)
    alpha = np.maximum(alpha, g)
    s = Paper(SHAPE)
    pts = curve(EDGE[:7], 10)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):                        # the lip: piled gravel, its top in the sun
        s.line([(x0, y0 + 2), (x1, y1 + 2)], "#7a6450", 6.0)
        s.line([(x0, y0 - 0.5), (x1, y1 - 0.5)], "#d8c4a2", 2.0, 0.85)
    rng = np.random.default_rng(seed)
    for X in np.linspace(0, 1, 26):                                     # pebbles on the lip, larger toward the corner
        px = 512 + X * 288 + rng.normal(0, 4)
        py = np.interp(px, [p[0] for p in EDGE[:7]], [p[1] for p in EDGE[:7]]) + rng.uniform(-1, 4)
        rr = 1.6 + 2.6 * X
        s.ellipse(px + rr * 0.5, py + rr * 0.4, rr * 1.1, rr * 0.5, "#4e3c34", 0.6)
        s.ellipse(px, py, rr, rr * 0.6, lerp(rgb("#b8a088"), rgb("#e0d0b0"), rng.random()))
    tones = ("#26271e", "#424434", "#6a6c50", "#a4a27c")
    sagebrush(s, 590, 610, 30, seed + 3, tones=tones)
    sagebrush(s, 664, 596, 44, seed + 4, tones=tones)
    sagebrush(s, 742, 580, 50, seed + 5, tones=("#22231c", "#3c3e30", "#64664c", "#9c9a76"))
    sagebrush(s, 796, 548, 38, seed + 6, tones=tones)
    tuft(s, 544, 600, 12, seed + 7, colors=("#5a5236", "#8a7c50", "#b8a670"))
    tuft(s, 628, 574, 14, seed + 8, colors=("#5a5236", "#8a7c50", "#b8a670"))
    tuft(s, 706, 548, 12, seed + 9, colors=("#5a5236", "#8a7c50", "#b8a670"))
    # and in the other bottom corner, the sage at the gravel's edge there (beside the scene's own)
    sagebrush(s, 14, 614, 44, seed + 12, tones=("#22231c", "#3c3e30", "#64664c", "#9c9a76"))
    sagebrush(s, 84, 622, 30, seed + 13, tones=tones)
    tuft(s, 124, 602, 12, seed + 14, colors=("#5a5236", "#8a7c50", "#b8a670"))
    sc, sa = s.done()
    over(color, sc, sa)
    alpha = np.maximum(alpha, sa)
    # the fence: the last post, the top rail, and the chain-link from the post off the right edge (behind the pole)
    f = Sheet(SHAPE)
    mesh = np.zeros(SHAPE, dtype=F32)
    xm, ym = x - POST_X, y - FENCE_TOP
    d1 = np.abs(((xm + ym) % 7.8) - 3.9)                                # 5 cm diamonds at 1.1 px to the cm
    d2 = np.abs(((xm - ym) % 7.8) - 3.9)
    wire = np.clip(1.25 - np.minimum(d1, d2) * 1.6, 0, 1)
    inside = (x > POST_X + 2) & (y > FENCE_TOP + 2)
    mesh = (wire * inside).astype(F32) * 0.92
    over(color, rgb("#3c3c3a"), mesh)
    alpha = np.maximum(alpha, mesh)
    f.line([(POST_X, FENCE_TOP + 1), (812, FENCE_TOP + 1)], "#3e3e3c", 5.0)          # the top rail
    f.line([(POST_X + 2, FENCE_TOP - 0.6), (812, FENCE_TOP - 0.6)], "#c8c4b8", 1.3, 0.85)
    f.line([(POST_X, FENCE_TOP - 3), (POST_X, 612)], "#36363a", 7.0)                 # the post
    f.line([(POST_X - 2.2, FENCE_TOP), (POST_X - 2.2, 612)], "#cfcabe", 1.6, 0.8)
    f.ellipse(POST_X, FENCE_TOP - 4, 5.2, 3.0, "#3a3a3c")                            # its cap
    f.ellipse(POST_X - 1.5, FENCE_TOP - 5, 3.0, 1.4, "#d6d0c4", 0.85)
    for yy in (510, 548, 586):                                                       # the bands holding the mesh
        f.line([(POST_X + 2, yy), (POST_X + 8, yy)], "#4a4a48", 2.0)
    fc, fa = f.done()
    over(color, fc, fa)
    alpha = np.maximum(alpha, fa)
    return color, alpha


def near_plane():
    color, alpha = fence_and_edge()
    pc, pa = pole()
    over(color, pc, pa)
    alpha = np.maximum(alpha, pa)
    solid = alpha > 0.5
    # deep and warm in the shade (the keying turns warm darks violet: a frankly warm note), a hot rim toward the sun
    lum = color @ np.array([0.3, 0.55, 0.15], dtype=F32)
    dark = (lum < 0.32) & solid
    warm = depth.near_tone(rgb("#6a4224"), shade="#241c30", k=0.35, warm=0.08)
    color[dark] = color[dark] * 0.80 + warm * 0.20
    rim = depth.rim(alpha, light=LIGHT, width=2.0) * solid
    over(color, rgb("#f4cc8a"), (rim * 0.55).astype(F32))
    return np.clip(color, 0, 1).astype(F32), alpha.astype(F32)


# ---------------------------------------------------------------- back.png
def tree_shade(seed=5):
    """The dappled shade of a tamarisk outside the picture on the left (its crown 4 to 7 m up, centred 8 m left of the
    lens's line): drawn on the ground through the camera, moved by the sun."""
    x, y = grid(SHAPE)
    yy = np.maximum(y, K.HZ + 2.0)
    Zc = K.EYE * K.FOCAL / (yy - K.HZ)
    X = (x - K.VX) * Zc / K.FOCAL
    z = Zc - K.CAM.Z0
    hgt = 560.0
    cx, cz = -820.0 + SUNX * hgt, 40.0 + SUNZ * hgt                     # where the crown's shadow lies
    rng = np.random.default_rng(seed)
    m = np.zeros(SHAPE, dtype=F32)
    for i in range(16):                                                  # the crown in clumps
        a = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(0, 210)
        bx, bz, br = cx + math.cos(a) * d, cz + math.sin(a) * d * 0.9, rng.uniform(110, 190)
        m = np.maximum(m, np.clip(1.25 - np.hypot((X - bx) / br, (z - bz) / (br * 0.9)), 0, 1))
    leaf = np.zeros(SHAPE, dtype=F32)
    for i in range(7):                                                   # the fine leaf-pattern: flecks of sun in it
        a = rng.uniform(0, math.pi)
        wl = rng.uniform(26, 60)
        leaf += np.sin((X * math.cos(a) + z * math.sin(a)) / wl * 2 * math.pi + rng.uniform(0, 6.3)).astype(F32)
    leaf = leaf / 7.0
    shade = np.clip(m * 2.2, 0, 1) * np.clip(0.82 + leaf * 1.4, 0, 1)
    shade = shade * (y > K.HZ + 150)
    return blur(shade.astype(F32), 1.2)


def ruts(pic, ground, seed=21):
    """Old tire tracks, from the gate round toward the corner where the lot's cars turn: faint, scuffed."""
    rng = np.random.default_rng(seed)
    dark, lit = Sheet(SHAPE), Sheet(SHAPE)
    path = [(-1040, 1240), (-930, 820), (-700, 420), (-330, 210), (180, 110), (620, 10), (900, -60)]
    pts = curve(path, 30)
    for side in (-78.0, 78.0):
        line = []
        for i, (X, Z) in enumerate(pts):
            j = min(i + 1, len(pts) - 1)
            i0 = j - 1
            dX, dZ = pts[j][0] - pts[i0][0], pts[j][1] - pts[i0][1]
            n = math.hypot(dX, dZ) or 1.0
            line.append((X - dZ / n * side, Z + dX / n * side))
        seg = [(pt(X, Z), K.k_at(Z)) for X, Z in line]
        for (a, ka), (b, kb) in zip(seg, seg[1:]):
            if rng.random() < 0.15:
                continue
            w = max(0.7, 16.0 * (ka + kb) * 0.5)
            al = 0.10 + 0.08 * rng.random()
            dark.line([a, b], "#7a6050", w, al)
            o = max(0.5, 4.0 * (ka + kb) * 0.5)
            lit.line([(a[0] - o, a[1] - o * 0.4), (b[0] - o, b[1] - o * 0.4)], "#fff0d0", w * 0.35, al * 0.7)
    dc, da = dark.done()
    lc, la = lit.done()
    over(pic, dc, da * ground)
    over(pic, lc, la * ground)


def stones(pic, ground, seed=31):
    """Stones in the gravel with their short shadows (right, and back: up the picture)."""
    s = Sheet(SHAPE)
    rng = np.random.default_rng(seed)
    for x, y, k, r in depth.scatter(pt, k_at, (-1500, 1500, -40, 1100), 0.9, seed, size=(7, 7), zone=ground, most=900):
        sz = (3 + 8 * r) * k
        if sz < 1.0:
            continue
        s.ellipse(x + SUNX * sz * 0.5, y - sz * 0.22, sz * 0.7, sz * 0.32, "#6a6080", 0.30)
        pts_ = [(x + math.cos(t) * sz * 0.5 * (0.7 + 0.5 * rng.random()), y + math.sin(t) * sz * 0.26 * (0.7 + 0.5 * rng.random()) - sz * 0.1)
                for t in np.linspace(0, 2 * math.pi, 6, endpoint=False)]
        s.poly(pts_, lerp(rgb("#b49c80"), rgb("#ece0c8"), rng.random()))
    c, a = s.done()
    over(pic, c, a * ground)


def building_shadow(pic, ground):
    """The building's shadow on the gravel to its right, glazed once more (the same sun, through the camera)."""
    h = K.BLD["cope"]
    x0, x1 = K.BLD["x"]
    z0, z1 = K.BLD["z"]
    places = [(x1, z0), (x1 + SUNX * h, z0 + SUNZ * h), (x1 + SUNX * h, z1 + SUNZ * h), (x1, z1)]
    depth.shadow_on_ground(pic, pt, places, color="#4a4470", amount=0.16, soft=1.4, wobble=0.8, seed=4, ground=ground)


def far_air(pic, sky):
    x, y = grid(SHAPE)
    far = np.clip((322.0 - y) / (322.0 - K.HZ), 0, 1) ** 0.7
    band = step(96.0, 108.0, y) * step(330.0, 318.0, y)
    # the building and its unit stand in the middle: no air on them (the flagpole and the limousine are cut-outs)
    bld = [(168, 182), (190, 182), (190, 103), (421, 103), (421, 214), (453, 247), (453, 434), (105, 434), (105, 248), (168, 214)]
    keep = (1 - mask_poly(SHAPE, bld, soft=1.0)).astype(F32)
    depth.air(pic, far, sky, amount=0.24, mask=(band * keep).astype(F32))


def deepen(pic):
    ground = ground_mask()
    x, y = grid(SHAPE)
    sky = pic[96:101, 440:800].reshape(-1, 3).mean(axis=0)
    # the lot's ground, all of it (not the building, the flagpole, the limousine): for the tree's shade
    lot = step(318.0, 330.0, y).astype(F32)
    for x0, y0, x1, y1 in ((104, 100, 454, 433), (76, 30, 118, 445), (494, 292, 800, 396)):
        lot = lot * (1 - mask_poly(SHAPE, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], soft=1.0))
    # the near gravel a little deeper and warmer
    t = np.clip((y - 430.0) / 170.0, 0, 1) ** 1.2
    walk = mask_poly(SHAPE, GRAVEL, soft=2.0)
    deep = (t * 0.38 * walk).astype(F32)
    pic[...] = pic * (1 - deep[..., None]) + pic * rgb("#b88a64")[None, None, :] * deep[..., None]
    building_shadow(pic, ground)
    ruts(pic, ground)
    stones(pic, ground)
    sh = tree_shade() * lot
    tint(pic, "#6a5e8e", (sh * 0.40).astype(F32))
    over(pic, "#6c6496", (sh * 0.06).astype(F32))
    far_air(pic, sky)
    return np.clip(pic, 0, 1)


# ---------------------------------------------------------------- the files
def load_rgb(path):
    return np.asarray(Image.open(path).convert("RGB"), dtype=F32) / 255


def write_back(new):
    im = Image.open(ORIG + "/back.png")
    if im.mode == "P":
        old_idx = np.asarray(im)
        old_pal = np.asarray(im.getpalette()[: 3 * (int(old_idx.max()) + 1)], dtype=F32).reshape(-1, 3) / 255
    else:
        old = np.asarray(im.convert("RGB"), dtype=F32) / 255
        old_pal = palette_of([old], colors=150)
        old_idx = to_palette(old, old_pal, speckle=0.0)
    old = old_pal[old_idx]
    changed = np.abs(new - old).max(axis=2) > 1.5 / 255
    room = 255 - len(old_pal)
    add = palette_of([new[changed].reshape(-1, 1, 3)], colors=min(room, 95))
    pal = np.concatenate([old_pal, add]).astype(F32)
    idx = old_idx.astype(np.uint8).copy()
    part = to_palette(new[changed].reshape(-1, 1, 3), pal, speckle=0.008)
    idx[changed] = part[:, 0]
    save(OUT + "/back.png", idx, pal)
    return int(changed.sum())


def write_cut(name, color, alpha, colors, seed):
    g = grain(color, seed, 0.012)
    solid = alpha > 0.5
    pal = palette_of([g[solid].reshape(-1, 1, 3)], colors=colors)
    idx = to_palette(g, pal, speckle=0.010)
    save(OUT + "/" + name + ".png", idx, pal, solid.astype(F32))


def front_deeper():
    """The scene's own front plane (the sage in the bottom corners): deeper and warmer, to count beside the new."""
    im = Image.open(ORIG + "/front.png").convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255
    c, al = a[..., :3].copy(), a[..., 3]
    c = c * 0.78
    c[..., 0] = c[..., 0] + 0.035
    c[..., 1] = c[..., 1] + 0.008
    c = np.clip(c, 0, 1)
    solid = al > 0.5
    pal = palette_of([c[solid].reshape(-1, 1, 3)], colors=40)
    idx = to_palette(c, pal, speckle=0.004)
    save(OUT + "/front.png", idx, pal, solid.astype(F32))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(ORIG):
        if f not in ("back.png", "front.png", "near.png"):
            src = os.path.join(ORIG, f)
            if os.path.isfile(src):
                shutil.copyfile(src, os.path.join(OUT, f))
    pic = deepen(load_rgb(ORIG + "/back.png"))
    print("back: changed", write_back(pic))
    front_deeper()
    c, a = near_plane()
    write_cut("near", c, a, 56, 29)
    print("near: share", round(float((a > 0.5).mean()) * 100, 1))
    comp = Image.open(OUT + "/back.png").convert("RGBA")
    for n in ("door", "awning", "trash", "flagpole", "limo", "front", "near"):
        p = OUT + "/" + n + ".png"
        if os.path.exists(p):
            comp.alpha_composite(Image.open(p).convert("RGBA"))
    comp.convert("RGB").save(OUT + "-depth-comp.png")

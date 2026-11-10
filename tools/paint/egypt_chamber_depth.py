"""The burial chamber in three planes (round twenty-three, DEPTH.md; the fast pass over the painting as it is).

    python3 egypt_chamber_depth.py        reads out/egypt-chamber-orig/ (the full run of egypt_chamber.py, untouched),
                                          writes the scene's set into out/egypt-chamber/: back, bench, mirror, front, near

NEAR   the granite of the way in: we look into the chamber through a doorway of red granite. Its left jamb stands up the
       left edge of the frame and its lintel runs across the top and off the right edge (the right jamb is beyond the
       frame). Plain stone, as the room is: a front face in deep warm shade, and the jamb's inner face and the lintel's
       underside seen running to the room's own vanishing point (450, 150), lit a little by the lamps inside, with a
       thread of lamplight on the far arris. The banded chest, the jars, lamp E on its gilded stand and the oil jar stand
       on our side of it (the things not yet carried in), so near.png is cut round them: they are in front of the jamb.
       front.png keeps its outline exactly and is made to count: darker and warmer, but for lamp E in its own light.
BACK   air in the room: the far wall a little cooler and paler (the farther a surface, the more), the corners and the
       ceiling in cool dark, the near floor deeper; the floor's joints said again in perspective (the painter's own slabs,
       from the kit), grit and granite chips across the paving at a true density, few and large near, many and small
       far; the lamps' warm pools on the floor a little warmer, the dark between them a little cooler.
The light is the painter's: six small oil lamps and nothing else. Nothing clicked is moved or redrawn; the place that
hums (x 457..545) keeps its bare wall exactly, and bench.png and mirror.png are copied byte for byte.
"""

import math
import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import F32, blur, grid, lerp, mask_poly, noise, palette_of, rgb, save, step, to_palette, glow, tint, over
import depth
from egypt_chamber_kit import (BW_MASK, CEIL_MASK, FLOOR_D, FLOOR_K, FLOOR_MASK, FLOOR_ROWS, FLOOR_X, LW_MASK, LW_U, RW_MASK,
                               RW_U, SHAPE, ashlar, k_of, P)
from egypt_chamber import SLABS

SRC = "out/egypt-chamber-orig"
OUT = "out/egypt-chamber"
H, W = SHAPE
X_PIX, Y_PIX = grid(SHAPE)
VP = (450.0, 150.0)                      # where the side walls, the beams and the doorway's own depth run to
HUM_WALL = (457, 545)                    # the bare wall that hums: kept exactly


def load(name):
    im = Image.open(f"{SRC}/{name}").convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def to8(picture, name, colors, alpha=None, accents=(), speckle=0.010, seed=5):
    """Back to a palette as the scene's own finish does (its grain is in the painting already)."""
    sample = picture if alpha is None else picture[alpha > 0.5]
    parts = [sample.reshape(-1, 1, 3)]
    for (x, y, w, h, times) in accents:
        parts += [picture[y:y + h, x:x + w].reshape(-1, 1, 3)] * times
    n = len(np.unique((sample * 255).astype(np.uint8).reshape(-1, 3), axis=0))
    pal = palette_of(parts, colors=min(colors, max(2, n)))
    idx = to_palette(picture, pal, seed=seed, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def poly_any(shape, pts):
    return mask_poly(shape, pts)


# ---------------------------------------------------------------- what may not be touched
# the scene file's areas of things on the floor and at the back (the painter's layout and the scene's hotspots)
THINGS = [
    [[128, 447], [136, 425], [137, 375], [152, 368], [154, 272], [166, 272], [168, 365], [172, 190], [208, 190], [208, 296], [230, 296], [232, 346], [306, 346], [308, 338], [336, 338], [338, 352], [364, 352], [365, 279], [377, 279], [378, 355], [414, 343], [457, 341], [461, 390], [471, 414], [471, 450], [408, 456], [345, 451], [240, 447]],   # the treasure
    [[560, 500], [746, 500], [746, 415], [731, 383], [554, 383], [560, 415]],                                       # the sarcophagus
    [[588, 331], [751, 331], [751, 384], [588, 384]],                                                               # its lid
    [[189, 517], [212, 516], [223, 505], [239, 509], [249, 485], [255, 490], [257, 512], [268, 507], [331, 507], [342, 512], [353, 463], [345, 456], [324, 460], [313, 436], [302, 439], [294, 456], [265, 457], [260, 453], [264, 434], [259, 424], [250, 434], [254, 462], [244, 481], [237, 474], [228, 475], [223, 500], [195, 505]],   # the bench
    [[356, 480], [356, 486], [364, 496], [361, 508], [367, 511], [382, 508], [392, 514], [401, 514], [407, 509], [409, 494], [401, 490], [389, 489], [383, 478], [377, 475], [364, 475]],   # the brazier
    [[135, 330], [135, 413], [67, 469], [67, 369]],                                                                 # the low doorway
]


def objects_mask(back, cut_alphas):
    """Everything that is not bare stone: the areas above, the cut-outs, and whatever the painter set on the floor
    (jars, gold, poles, rollers: anything more coloured, brighter or darker than granite), a little enlarged."""
    m = np.zeros(SHAPE, F32)
    for pts in THINGS:
        m = np.maximum(m, poly_any(SHAPE, pts))
    for a in cut_alphas:
        m = np.maximum(m, a)
    mx, mn = back.max(axis=2), back.min(axis=2)
    sat = (mx - mn) / np.maximum(mx, 1e-3)
    lum = back @ np.array([0.3, 0.55, 0.15], F32)
    odd = ((sat > 0.36) | (lum > 0.62)).astype(F32)
    m = np.maximum(m, odd)
    return np.clip(blur(m, 2.2) * 3.0, 0, 1)


# ---------------------------------------------------------------- NEAR: the granite of the way in
XL_FRONT = 33.0                          # the jamb's front arris (its face toward us runs off the left edge)
TOP_FRONT = 50.0                         # the lintel's front arris (its face runs off the top)
DEPTH_S = 0.955                          # how much nearer the front arrises are than the far ones (the frame's thickness)


def toward_vp(x, y, s=DEPTH_S):
    return VP[0] + (x - VP[0]) * s, VP[1] + (y - VP[1]) * s


def near_plane(back, front_a, seed=2318):
    """-> (color, alpha) of the doorway's left jamb and lintel."""
    rng = np.random.default_rng(seed)
    wob = lambda cell, s, amt: (noise(SHAPE, cell, seed + s, 3) - 0.5) * amt
    # the arrises, hand-made: each wanders a little, none is ruled
    xf = XL_FRONT + wob((9, 70), 1, 1.6)                                   # the jamb's front arris, per row
    yf = TOP_FRONT + wob((80, 9), 2, 1.4) + 1.2 * np.sin(X_PIX / W * math.pi)    # the lintel's, with the least sag
    xb = VP[0] + (xf - VP[0]) * DEPTH_S + wob((9, 50), 3, 1.0)               # the far arris of the jamb's inner face
    yb = VP[1] + (yf - VP[1]) * DEPTH_S + wob((60, 9), 4, 0.9)                # and of the lintel's underside
    # where the underside and the inner face meet (the inner corner of the opening), along the line to the vanishing point
    cx_f, cy_f = XL_FRONT, TOP_FRONT
    cx_b, cy_b = toward_vp(cx_f, cy_f)
    jamb_face = np.clip(xf - X_PIX + 0.5, 0, 1)                             # left of the front arris
    lintel_face = np.clip(yf - Y_PIX + 0.5, 0, 1)                           # above it
    face = np.maximum(jamb_face, lintel_face)
    reveal = np.clip(xb - X_PIX + 0.5, 0, 1) * (1 - jamb_face) * np.clip(Y_PIX - (cy_f + (X_PIX - cx_f) * (cy_b - cy_f) / (cx_b - cx_f)) + 0.5, 0, 1)
    soffit = np.clip(yb - Y_PIX + 0.5, 0, 1) * (1 - lintel_face) * (1 - reveal) * np.clip(X_PIX - (cx_f + (Y_PIX - cy_f) * (cx_b - cx_f) / (cy_b - cy_f)) + 0.5, 0, 1)
    # a few chips out of the far arrises: the silhouette broken here and there
    bites = np.zeros(SHAPE, F32)
    for _ in range(5):
        y = rng.uniform(70, 560)
        r = rng.uniform(1.4, 2.6)
        x = VP[0] + (XL_FRONT - VP[0]) * DEPTH_S
        bites = np.maximum(bites, np.clip(1 - np.hypot((X_PIX - x - 0.6) / r, (Y_PIX - y) / (r * 2.2)), 0, 1))
    for _ in range(5):
        x = rng.uniform(90, 790)
        r = rng.uniform(1.4, 2.8)
        y = VP[1] + (TOP_FRONT - VP[1]) * DEPTH_S
        bites = np.maximum(bites, np.clip(1 - np.hypot((X_PIX - x) / (r * 2.4), (Y_PIX - y - 0.5) / r), 0, 1))
    alpha = np.clip(face + reveal + soffit, 0, 1) * (1 - (bites > 0.25) * (1 - face))
    reveal, soffit = reveal * alpha, soffit * alpha

    # ---- the stone: red granite in deep shade, warm (the keying turns warm darks violet: it is frankly warm here)
    mott = noise(SHAPE, 16, seed + 5, 4) - 0.5
    fine = noise(SHAPE, 4, seed + 6, 2) - 0.5
    face_c = rgb("#2c1712")[None, None, :] * (1 + 0.24 * mott + 0.10 * fine)[..., None]
    # darker toward the frame's own corner and the bottom: the lamps are low and far
    fall = 0.82 + 0.18 * np.clip(1 - np.hypot(X_PIX - 30, (Y_PIX - 330) * 0.6) / 420, 0, 1)
    face_c = face_c * fall[..., None]
    lit = rgb("#74422f")[None, None, :] * (1 + 0.16 * mott + 0.08 * fine)[..., None]
    # the inner face and the underside are turned toward the room: lamplight grazes them, more at their far edge
    t_rev = np.clip((X_PIX - xf) / np.maximum(xb - xf, 1), 0, 1)
    t_sof = np.clip((Y_PIX - yf) / np.maximum(yb - yf, 1), 0, 1)
    height_light = np.clip(1 - np.abs(Y_PIX - 330) / 360, 0.35, 1)          # the lamps stand low in the room
    rev_c = lerp(rgb("#2e1813")[None, None, :], lit, (0.10 + 0.80 * t_rev ** 1.8)[..., None] * height_light[..., None])
    sof_c = lerp(rgb("#2c1712")[None, None, :], lit * 0.9, (0.10 + 0.70 * t_sof ** 1.8)[..., None]
                 * (0.55 + 0.45 * np.clip(1 - np.abs(X_PIX - 330) / 520, 0, 1))[..., None])
    col = face_c.copy()
    col = col * (1 - reveal[..., None]) + rev_c * reveal[..., None]
    col = col * (1 - soffit[..., None]) + sof_c * soffit[..., None]
    # the grain of red granite: pink feldspar and black mica, large here (it is near)
    spots = rng.random(SHAPE)
    pink = (spots > 0.996).astype(F32)
    black = (spots < 0.010).astype(F32)
    pink, black = np.clip(blur(pink, 0.6) * 3, 0, 1), np.clip(blur(black, 0.55) * 3, 0, 1)
    over(col, "#4e3027", pink * 0.5 * (0.5 + 0.5 * (reveal + soffit)))
    tint(col, "#2a1c1c", black * 0.55)
    # the blocks: a joint where the lintel sits on the jamb, two joints up the jamb, one in the lintel; on the inner
    # faces they run to the vanishing point
    jl = np.zeros(SHAPE, F32)
    for yj in (float(yf.mean()), 262.0, 470.0):
        on_face = np.exp(-((Y_PIX - yj - wob((50, 9), 7, 1.0)) ** 2) / 0.45) * np.clip(xf - X_PIX, 0, 1)
        yb_j = VP[1] + (yj - VP[1]) * DEPTH_S
        line_y = yj + (X_PIX - xf) * (yb_j - yj) / np.maximum(xb - xf, 1)
        on_rev = np.exp(-((Y_PIX - line_y) ** 2) / 0.4) * reveal
        jl = np.maximum(jl, np.maximum(on_face, on_rev))
    xj = 488.0
    on_lint = np.exp(-((X_PIX - xj - wob((9, 40), 8, 1.0)) ** 2) / 0.45) * lintel_face
    xb_j = VP[0] + (xj - VP[0]) * DEPTH_S
    line_x = xj + (Y_PIX - yf) * (xb_j - xj) / np.maximum(yb - yf, 1)
    jl = np.maximum(jl, np.maximum(on_lint, np.exp(-((X_PIX - line_x) ** 2) / 0.4) * soffit))
    tint(col, "#2a1614", jl * 0.75)
    # the rim: a thread of lamplight on the far arris of the jamb and of the lintel (the edge that faces the lamps)
    rim_j = np.exp(-((X_PIX - (xb - 0.9)) ** 2) / 0.5) * (Y_PIX > yb) * reveal
    rim_l = np.exp(-((Y_PIX - (yb - 0.9)) ** 2) / 0.5) * (X_PIX > xb) * soffit
    rim = np.clip(rim_j * (0.35 + 0.65 * height_light) + rim_l * 0.75, 0, 1) * (0.7 + 0.3 * (noise(SHAPE, (8, 30), seed + 9, 2)))
    glow(col, "#f2a564", rim * 0.72)
    # the lamps at the jamb's foot (lamp F on the floor just beyond it): a warm breath on the low inner face
    lf = np.exp(-((X_PIX - 58) ** 2 + (Y_PIX - 496) ** 2) / (2 * 38.0 ** 2)) * reveal
    glow(col, "#d8743c", lf * 0.30)
    # the chest, the jars and lamp E stand on our side of it
    alpha = alpha * (1 - np.clip(front_a, 0, 1))
    return np.clip(col, 0, 1).astype(F32), (alpha > 0.5).astype(F32)


def front_counts(front, front_a):
    """front.png made to count: its things deeper and warmer, inside exactly the same outline. Lamp E, in its own light,
    keeps its bright stand top; its light falls off down the stand and on the oil jar."""
    d_e = np.hypot(X_PIX - 779.5, Y_PIX - 452.0)
    in_lamp = np.clip(1 - d_e / 140.0, 0, 1) * (X_PIX > 690)
    k = 0.30 * (1 - in_lamp) + 0.06 * in_lamp
    shade = rgb("#2a1a16")
    out = front * (1 - k[..., None]) + front * shade * 2.0 * k[..., None]          # a warm, deep glaze
    out[..., 0] = np.minimum(out[..., 0] * (1 + 0.05 * (1 - in_lamp)), 1)
    # a rim on the side toward the lamps of the room (to the right and a little up), for the things at the bottom left
    r = depth.rim(front_a, light=(1.0, -0.35), width=1.6) * (X_PIX < 300)
    glow(out, "#e09a62", r * 0.30)
    return np.clip(out, 0, 1).astype(F32)


# ---------------------------------------------------------------- BACK: air, the corners, the floor
def far_map():
    """0 for what is nearest the lens to 1 for the back wall: by the floor's depth, along the side walls from the back
    corners, the ceiling by its depth."""
    far = np.zeros(SHAPE, F32)
    far += BW_MASK * 1.0
    side_l = np.clip(1 - LW_U / 560.0, 0, 1) * LW_MASK
    side_r = np.clip(1 - RW_U / 560.0, 0, 1) * RW_MASK
    far = np.maximum(far, np.maximum(side_l, side_r) ** 1.2)
    fl = np.clip(1 - FLOOR_D / 560.0, 0, 1) ** 1.3 * FLOOR_MASK
    far = np.maximum(far, fl)
    far = np.maximum(far, CEIL_MASK * np.clip(1 - (150 - np.minimum(Y_PIX, 150)) / 150, 0, 1) * 0.8)
    return blur(far, 1.5)


def floor_joints():
    """The painter's own paving (egypt_chamber.room: ashlar over the floor, seed 21 + 7), as a distance in pixels to the
    nearest joint."""
    seed = 21
    wx = (noise(SHAPE, (70, 30), seed + 11, 3) - 0.5) * 1.6
    wy = (noise(SHAPE, (90, 26), seed + 12, 3) - 0.5) * 1.7
    _, _, fda, fdb, _ = ashlar(FLOOR_X + wx, FLOOR_D + wy * 2.0, SLABS, seed + 7, lengths=(150.0, 290.0))
    return np.minimum(fda * FLOOR_K, fdb * FLOOR_ROWS) * FLOOR_MASK + (1 - FLOOR_MASK) * 9


def deepen_back(back, objects):
    out = back.copy()
    keep = np.zeros(SHAPE, F32)                                                        # the wall that hums, exactly
    keep[230:440, HUM_WALL[0]:HUM_WALL[1]] = 1
    bare = (1 - objects)
    lum = out @ np.array([0.3, 0.55, 0.15], F32)

    # the lamps' pools on the floor a little warmer, the dark between them a little cooler
    lowf = blur(lum, 14)
    mean = float((lowf * FLOOR_MASK).sum() / FLOOR_MASK.sum())
    pool = np.clip((lowf - mean) / 0.10, 0, 1) * FLOOR_MASK * bare
    gap = np.clip((mean - lowf) / 0.08, 0, 1) * FLOOR_MASK * bare
    glow(out, "#ff9a4a", pool * 0.10)
    tint(out, "#8a7c9c", gap * 0.16)

    # the floor's joints, said again in perspective (wider and darker near us, hairlines far off), with the lit lip
    dist = floor_joints()
    near_k = np.clip((Y_PIX - 400) / 200, 0, 1)
    width = 0.55 + 0.75 * near_k
    line = np.clip(1.15 - dist / width, 0, 1)
    wander = 0.6 + 0.4 * noise(SHAPE, (40, 7), 77, 3)
    tint(out, "#3a2430", line * wander * (0.30 + 0.25 * near_k) * bare * FLOOR_MASK)
    lip = np.clip(1.0 - np.abs(dist - (width + 0.9)) / 0.7, 0, 1) * np.clip(lowf * 1.6, 0, 1)
    glow(out, "#ffcf9a", lip * wander * 0.07 * bare * FLOOR_MASK)

    # grit and chips of granite on the paving at a true density: big and few near us, small and many far off
    pt = lambda X, D: P(X, 0.0, D)
    kk = lambda X, D: k_of(D)
    zone = FLOOR_MASK * (objects < 0.2)
    sheet_dark = np.zeros(SHAPE, F32)
    sheet_lite = np.zeros(SHAPE, F32)
    rng = np.random.default_rng(91)
    for (x, y, k, r) in depth.scatter(pt, kk, (-460, 430, 10, 545), 26, seed=4, size=(2.4, 2.4), zone=zone):
        rad = max(0.5, (0.8 + 2.0 * r) * k)                                          # 1 to 3 cm across
        xi, yi = int(x), int(y)
        y0, y1, x0, x1 = max(yi - 4, 0), min(yi + 5, H), max(xi - 4, 0), min(xi + 5, W)
        sub_x, sub_y = X_PIX[y0:y1, x0:x1], Y_PIX[y0:y1, x0:x1]
        sq = (row_of_ratio(y))
        m = np.clip(rad - np.hypot(sub_x - x, (sub_y - y) / sq), 0, 1)
        if r < 0.62:
            sheet_dark[y0:y1, x0:x1] = np.maximum(sheet_dark[y0:y1, x0:x1], m)
        else:
            sheet_lite[y0:y1, x0:x1] = np.maximum(sheet_lite[y0:y1, x0:x1], m)
            sheet_dark[y0 + 1:y1, x0:x1] = np.maximum(sheet_dark[y0 + 1:y1, x0:x1], m[:y1 - y0 - 1] * 0.5)   # its shadow, toward us
    tint(out, "#4a3038", sheet_dark * 0.45 * zone)
    glow(out, "#c8a898", sheet_lite * 0.22 * np.clip(lowf * 1.5, 0.3, 1) * zone)

    # air: the farther a surface, the more it goes toward the room's cool dusk (cooler and a little paler); the gold
    # and the linen keep their own colour
    far = far_map()
    mx, mn = back.max(axis=2), back.min(axis=2)
    sat = (mx - mn) / np.maximum(mx, 1e-3)
    bright = np.clip((sat - 0.30) / 0.15, 0, 1) + np.clip((lum - 0.55) / 0.12, 0, 1)
    protect = np.clip(blur(np.clip(bright, 0, 1), 1.2) * 1.5, 0, 1)
    depth.air(out, far, "#a89cb4", amount=0.13, power=1.0, mask=(1 - protect) * (1 - keep))

    # the corners and the ceiling in cool dark, the near floor deeper (thin where people stand: y 500..535)
    depth.frame(out, amount=0.24, bottom=0.20, color="#2a2440")
    ceiling = np.clip((60 - Y_PIX) / 60, 0, 1) * CEIL_MASK
    tint(out, "#6a6488", ceiling * 0.18)

    # the bare wall that hums stays exactly as painted
    out = out * (1 - keep[..., None]) + back * keep[..., None]
    return np.clip(out, 0, 1).astype(F32)


def row_of_ratio(y):
    """How flat a round thing on the floor looks at this row (the floor's own foreshortening)."""
    return float(np.clip(FLOOR_ROWS[int(min(max(y, 401), 599)), 400] / max(FLOOR_K[int(min(max(y, 401), 599)), 400], 1e-6), 0.2, 1.0))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back.png")
    front, front_a = load("front.png")
    bench, bench_a = load("bench.png")
    mirror, mirror_a = load("mirror.png")
    objects = objects_mask(back, (bench_a, mirror_a, front_a))
    new_back = deepen_back(back, objects)
    near_c, near_a = near_plane(back, front_a)
    new_front = front_counts(front, front_a)
    gold = [(130, 220, 330, 250, 2), (240, 430, 160, 90, 3)]
    print("back", to8(new_back, f"{OUT}/back.png", 160, accents=gold, speckle=0.012))
    print("front", to8(new_front, f"{OUT}/front.png", 56, front_a))
    print("near", to8(near_c, f"{OUT}/near.png", 48, near_a))
    for name in ("bench.png", "mirror.png", "layout.json"):
        shutil.copyfile(f"{SRC}/{name}", f"{OUT}/{name}")
    comp = Image.open(f"{OUT}/back.png").convert("RGBA")
    for name in ("bench", "mirror", "front", "near"):
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save("out/egypt-chamber-depth-comp.png")
    big = comp.convert("RGB").resize((1600, 1200), Image.NEAREST)
    big.crop((0, 0, 1600, 1200)).save("out/egypt-chamber-depth-comp2x.png")
    print("near share", round(float(near_a.mean()) * 100, 1), "%")

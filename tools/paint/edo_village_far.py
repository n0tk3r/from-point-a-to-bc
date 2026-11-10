"""PAINT-23A (round twenty-three, DEPTH.md): the far plane of Yui (edo-village), laid wet in wet, layer behind layer.

From the farthest to the nearest, each layer paler, plainer and nearer the sky's colour at the horizon (HORIZON_C) than
the one in front of it, and none of them with a key line:

    the sky         a graded wash, deep at the top, the paper at the horizon; clouds lifted out of it, large overhead,
                    small and flat toward the horizon (a sky has perspective too)
    Fuji            the cone as it was (the scene's `fuji` area follows it), but a form: the lit flank and the shade
                    flank, ridges and gullies running down from the summit, the snow BARE PAPER with a thin blue wash
                    on its shade side, the snow line ragged down the gullies
    its cloud       a band of cloud lying across its flank (in front of it: the mountain stands beyond it)
    the foothills   a low range before its foot, and the far shore of the bay under them
    two capes       beyond the Satta headland, each lower and paler, stepping out into the bay
    the headland    the Satta pass in two spurs: the far one blue-green and soft, the near one green, with its trees
    the bay         a graded wash from the paper at the horizon to cobalt at our feet, dragged dry in level streaks
                    (the paper sparkles through); far out it holds the far shore, the cloud and Fuji's flank upside down;
                    sails at three distances and a sculling boat (Gonroku's ship, the cut-out, is the nearest of them)

Nothing here is copied from any print or painting: the mountain's shape and the place are the scene's own (round twenty).
"""

import math

import numpy as np

from brush import *
import sky as skylib
import land
from edo_village_kit import *

SHAPE = (H, W)
FAR_SHORE_ROW = 301
HORIZON_C = lerp(WPAPER, CERULEAN, 0.10)                    # the sky at the horizon: the paper with a breath of blue
FUJI_AT = (300.0, 80.0)


# ---------------------------------------------------------------- the sky
def paint_sky(seed):
    """The graded wash (the print's band, laid wet): deep at the top, the paper at the horizon, never even."""
    x, y = grid(SHAPE)
    drift = (noise(SHAPE, (520, 220), seed, 3) - 0.5) * 0.12
    t = np.clip(y / float(HZ) + drift, 0, 1)
    pic = ramp(t, [(0.0, thin(mixp(COBALT, ULTRA, 0.32), 0.04)), (0.16, thin(mixp(COBALT, ULTRA, 0.16), 0.10)), (0.36, thin(COBALT, 0.24)),
                   (0.58, thin(mixp(COBALT, CERULEAN, 0.55), 0.42)), (0.78, thin(CERULEAN, 0.70)), (0.93, HORIZON_C), (1.0, HORIZON_C)])
    pic *= (1 + (noise(SHAPE, (420, 34), seed + 1, 3) - 0.5)[..., None] * 0.07)          # the wide brush, drawn across
    # the sun is behind us on the left: the paper warms a breath low on that side
    glow(pic, thin(NAPLES, 0.4), (np.clip(1 - x / 460.0, 0, 1) * np.clip(1 - np.abs(y - 268) / 80.0, 0, 1) * 0.12).astype(F32))
    return np.clip(pic, 0, 1).astype(F32)


def paint_clouds(pic, seed):
    """Clouds lifted out of the wet wash: bare paper where the sun is on them, a thin grey-blue under them. Large and
    high near the top of the sheet, small and flat near the horizon. -> a mask of them (they are laid wet in wet)."""
    x, y = grid(SHAPE)
    shade = thin(mixp(COBALT, SIENNA, 0.14), 0.68)
    tones = (shade, thin(mixp(COBALT, SIENNA, 0.10), 0.84), WPAPER, WPAPER)
    #         middle x, base row, width, height, billows: the farther (lower), the smaller and flatter
    masses = [(560, 110, 190, 42, 26), (128, 150, 150, 26, 14), (716, 152, 130, 24, 13),
              (470, 196, 120, 14, 9), (40, 214, 110, 11, 8), (610, 222, 90, 9, 7)]
    thick = skylib.paint_clouds(pic, masses, seed + 5, tones, light=(-0.7, -0.7), ragged=11.0, amount=0.92, reach=30.0)
    # high wisps near the top, slanting away to the right, and level threads near the horizon
    n = noise(SHAPE, (300, 15), seed + 6, 4)
    slant = sample(n, x + (140 - y) * 1.3, y)
    high = step(0.62, 0.90, slant) * np.clip(1 - y / 96.0, 0, 1) * 0.30
    low = step(0.62, 0.9, noise(SHAPE, (240, 7), seed + 7, 3)) * np.clip(1 - np.abs(y - 262) / 30.0, 0, 1) * 0.5
    wisp = blur((high + low).astype(F32), 1.0)
    over(pic, WPAPER, wisp)
    return np.clip(thick + wisp, 0, 1).astype(F32)


# ---------------------------------------------------------------- Fuji
def fuji_mask():
    """Fuji across the bay: the great concave cone, summit at (300, 80), its foot lost at the far shore (round
    twenty's shape, kept: the scene's `fuji` area is drawn round it)."""
    x, y = grid(SHAPE)
    sx, sy = FUJI_AT
    t = np.clip((y - sy) / (HZ + 4 - sy), 0, 1)
    half = 12 + 470 * t ** 1.7
    cap = np.clip((y - sy) / 9.0, 0, 1)
    half = half * (0.55 + 0.45 * cap)
    m = (np.abs(x - sx - 6 * (1 - cap)) < half) & (y >= sy) & (y < HZ + 4)
    m = warp(m.astype(F32), 1.4, 40, 7)
    return np.clip(m, 0, 1)


def paint_fuji(pic, seed):
    """The mountain as a form. The sun is behind us and to the left: the left flank is lit and the right is in shade,
    softly; ridges run down from the summit, each with a lit side; the snow is the bare paper."""
    x, y = grid(SHAPE)
    m = fuji_mask()
    sx, sy = FUJI_AT
    dx, dy = x - (sx + 3), np.maximum(y - (sy - 10), 1.0)
    ang = np.arctan2(dx, dy)                                          # 0 straight down the mountain, negative to the left
    rad = np.hypot(dx, dy)
    tile = noise((512, 512), (13, 230), seed + 3, 3)                  # ridges: thin across, long down the slope
    wide = noise((512, 512), (26, 300), seed + 4, 3)                  # the gullies the snow lies in

    def rid(t, a, r):
        return sample(t, (a + 1.7) / 3.4 * 500, np.clip(r * 0.9, 0, 500))
    d = 0.02
    lit_r = np.clip(0.5 + 3.0 * (rid(tile, ang + d, rad) - rid(tile, ang - d, rad)), 0, 1)       # a ridge's left side takes the sun
    lit_r = lerp(0.5, lit_r, np.clip(rad / 90.0, 0.15, 1.0))          # (the summit itself is smooth at this distance)
    term = sx + 16 + 0.10 * (y - sy)                                  # where the light leaves the cone
    broad = 1 - step(term - 34, term + 44, x)
    L_snow = np.clip((broad * (0.66 + 0.34 * lit_r) + (1 - broad) * 0.18 * lit_r) * 1.30, 0, 1)
    L_rock = np.clip(broad * (0.74 + 0.26 * lit_r) + (1 - broad) * 0.12 * lit_r, 0, 1)
    snow_c = lerp(thin(mixp(COBALT, ULTRA, 0.25), 0.52), WPAPER, L_snow[..., None])
    rock_c = lerp(thin(mixp(COBALT, ULTRA, 0.32), 0.42), thin(mixp(COBALT, ULTRA, 0.10), 0.58), L_rock[..., None])
    # the snow line: well down the flanks, ragged, in fingers down the gullies; patches of it lower still
    g = 0.62 * rid(wide, ang, rad * 0.5) + 0.38 * rid(tile, ang, rad * 0.4)
    edge = 172 + (g - 0.5) * 84 + np.clip(np.abs(x - sx) / 120.0, 0, 1) ** 2 * 26
    snow = step(edge + 4, edge - 4, y)
    patch = step(0.62, 0.76, rid(tile, ang, rad)) * step(edge + 34, edge + 2, y) * 0.45
    snow = np.clip(snow + patch, 0, 1)
    body = lerp(rock_c, snow_c, snow[..., None])
    # the air: the mountain pales toward its foot, toward the sky's own colour there
    haze_t = np.clip((y - 208) / 92.0, 0, 1) ** 1.25
    body = lerp(body, HORIZON_C, (haze_t * 0.80)[..., None])
    over(pic, body, m)
    return m, (snow * m).astype(F32)


def paint_fuji_cloud(pic, seed):
    """The band of cloud lying across the mountain's flank, and a wisp below the summit: bare paper, soft below. The
    mountain stands beyond it. -> its mask."""
    x, y = grid(SHAPE)
    n1 = noise(SHAPE, (150, 1), seed + 8, 3)
    yc = 239 + (n1 - 0.5) * 12 + 4 * np.sin(x / 83.0)
    hw = 5 + 8 * noise(SHAPE, (110, 1), seed + 9, 2)
    gaps = step(0.30, 0.52, noise(SHAPE, (120, 60), seed + 10, 3))
    ends = np.clip((x - 24) / 60.0, 0, 1) * np.clip((486 - x) / 80.0, 0, 1)
    up = np.clip(1 - (yc - y) / hw, 0, 1) * (y <= yc)                                         # its top: firmer
    down = np.clip(1 - (y - yc) / (hw * 1.5), 0, 1) ** 1.6 * (y > yc)                          # its underside: it melts
    band = blur(((up + down) * gaps * ends).astype(F32), 1.3)
    # a small wisp caught under the summit on the lee side
    wisp = mask_ellipse(SHAPE, 362, 150, 34, 5.5, soft=2.2, wobble=3.0, seed=seed + 11) * 0.8
    cloud = np.clip(band * 0.95 + wisp, 0, 1)
    tint(pic, thin(mixp(COBALT, SIENNA, 0.14), 0.62), np.clip(blur(np.roll(cloud, 3, axis=0), 2.0) * 0.5 * (1 - cloud), 0, 1))   # its shadow on the flank
    over(pic, WPAPER, cloud)
    return cloud


# ---------------------------------------------------------------- the far land, in layers
def layer(pic, crest, color, seed, rough=1.6, x0=None, x1=None, base=HZ + 2, foot=0.55, foot_rows=14.0, lit=None, lit_amount=0.0):
    """One far layer of land under a skyline: a wash of `color`, paler toward its foot (the air lies in the hollows
    between layers), a little lighter where it turns to the sun (`lit`). No line. -> its mask."""
    x, y = grid(SHAPE)
    m, line = land.ridge(SHAPE, crest, base, seed, rough=rough)
    lo = crest[0][0] if x0 is None else x0
    hi = crest[-1][0] if x1 is None else x1
    m = m * (x >= lo) * (x <= hi) * (y < HZ + 1)
    body = np.empty(SHAPE + (3,), dtype=F32)
    body[...] = color
    body *= (1 + (noise(SHAPE, (60, 22), seed + 2, 3) - 0.5)[..., None] * 0.08)
    if lit is not None and lit_amount:
        n = noise(SHAPE, (34, 16), seed + 3, 3)
        facing = np.clip((np.roll(n, -3, axis=1) - n) * 9.0, 0, 1)
        body = lerp(body, np.asarray(lit, dtype=F32), (facing * lit_amount)[..., None])
    down = np.clip((y - (line[None, :] + 1)) / foot_rows, 0, 1)                 # 0 at the skyline, 1 toward the foot
    body = lerp(body, HORIZON_C, (down ** 1.3 * foot)[..., None])
    over(pic, body, m.astype(F32))
    return m.astype(F32)


def paint_far_land(pic, seed):
    """Behind the bay, far to near: Fuji's foothills, the far shore under them, and the two capes beyond the Satta
    headland. -> the union of their masks."""
    hills = [(-10, 281), (50, 277), (110, 281), (170, 272), (235, 276), (300, 268), (360, 273), (430, 270), (500, 277), (560, 284), (620, 291), (664, 297)]
    m = layer(pic, hills, thin(mixp(COBALT, VIRIDIAN, 0.24), 0.60), seed + 40, rough=1.8, foot=0.70, foot_rows=16.0,
              lit=thin(mixp(CERULEAN, VERONESE, 0.3), 0.66), lit_amount=0.5)
    shore = [(-10, 293), (80, 291), (180, 294), (260, 290), (340, 293), (420, 291), (480, 294), (540, 296), (604, 298)]
    m = np.maximum(m, layer(pic, shore, thin(mixp(COBALT, VIRIDIAN, 0.36), 0.50), seed + 44, rough=0.9, foot=0.35, foot_rows=8.0))
    # the capes along our own coast beyond the headland: each nearer one steeper, darker and greener, its nose a little farther in
    cape_c = [(398, 302), (412, 297), (434, 294), (458, 295), (490, 293), (530, 291), (580, 288), (640, 283), (700, 280)]
    m = np.maximum(m, layer(pic, cape_c, thin(mixp(COBALT, VIRIDIAN, 0.40), 0.36), seed + 48, rough=0.9, foot=0.40, foot_rows=9.0,
                            lit=thin(VERONESE, 0.5), lit_amount=0.35))
    cape_b = [(450, 302), (462, 296), (478, 291), (498, 290), (520, 286), (548, 280), (580, 272), (626, 262), (700, 246)]
    m = np.maximum(m, layer(pic, cape_b, thin(mixp(VIRIDIAN, COBALT, 0.40), 0.22), seed + 52, rough=1.1, foot=0.45, foot_rows=12.0,
                            lit=thin(VERONESE, 0.42), lit_amount=0.45))
    return m


PASS_CREST = [(520, HZ + 1), (560, 282), (600, 262), (640, 236), (680, 214), (716, 196), (750, 180), (780, 172), (812, 166)]
NEAR_SPUR = [(588, HZ + 2), (618, 290), (648, 276), (676, 258), (706, 247), (742, 228), (776, 208), (812, 196)]


def paint_pass(pic, seed):
    """The Satta pass: a steep green headland closing the shore at the upper right, in two spurs. The far spur is the
    skyline (round twenty's crest, kept: the scene's `pass` area follows it), blue-green and soft; the near spur
    stands before it, greener and firmer, with the mist of the hollow between them along its top."""
    x, y = grid(SHAPE)
    m, line = land.ridge(SHAPE, PASS_CREST, HZ + 40, seed + 11, rough=1.6)
    m = m * (y < HZ + 1) * (x >= PASS_CREST[0][0] - 4)
    far_c = thin(mixp(VIRIDIAN, COBALT, 0.26), 0.15)
    body = np.empty(SHAPE + (3,), dtype=F32)
    body[...] = far_c
    body *= (1 + (noise(SHAPE, (70, 40), seed + 12, 3) - 0.5)[..., None] * 0.10)
    n = warp(noise(SHAPE, (40, 60), seed + 13, 3), 6.0, 30, seed + 14)
    facing = np.clip((np.roll(n, -3, axis=1) - n) * 7.0, 0, 1)
    lit_m = step(0.45, 0.75, n * 0.5 + facing * 0.5)
    body = lerp(body, thin(mixp(VERONESE, OCHRE, 0.10), 0.22), (lit_m * 0.75)[..., None])            # the slopes that turn to the sun
    fold = step(0.55, 0.8, noise(SHAPE, (30, 80), seed + 15, 3))
    body = lerp(body, thin(mixp(VIRIDIAN, PRUSSIAN, 0.30), 0.12), (fold * 0.6)[..., None])           # the folds, in shade
    down = np.clip((y - line[None, :]) / 70.0, 0, 1)
    body = lerp(body, HORIZON_C, (down ** 1.5 * 0.42)[..., None])                                   # the air at its foot
    over(pic, body, m.astype(F32))
    # the near spur
    m2, line2 = land.ridge(SHAPE, NEAR_SPUR, HZ + 40, seed + 17, rough=1.4)
    m2 = m2 * (y < HZ + 1) * (x >= NEAR_SPUR[0][0] - 2) * m
    over(pic, HORIZON_C, (np.clip(1 - np.abs(y - (line2[None, :] - 3)) / 7.0, 0, 1) * m * 0.38).astype(F32))   # mist behind its top
    near_c = thin(mixp(VIRIDIAN, OCHRE, 0.12), 0.10)
    body2 = np.empty(SHAPE + (3,), dtype=F32)
    body2[...] = near_c
    n2 = warp(noise(SHAPE, (26, 34), seed + 18, 3), 5.0, 24, seed + 19)
    facing2 = np.clip((np.roll(n2, -2, axis=1) - n2) * 8.0, 0, 1)
    body2 = lerp(body2, thin(mixp(VERONESE, NAPLES, 0.18), 0.12), (step(0.42, 0.72, n2 * 0.5 + facing2 * 0.5) * 0.8)[..., None])
    body2 = lerp(body2, mixp(VIRIDIAN, PRUSSIAN, 0.36), (step(0.56, 0.78, noise(SHAPE, (22, 46), seed + 20, 3)) * 0.55)[..., None])
    down2 = np.clip((y - line2[None, :]) / 60.0, 0, 1)
    body2 = lerp(body2, HORIZON_C, (down2 ** 1.6 * 0.22)[..., None])
    over(pic, body2, m2.astype(F32))
    return m.astype(F32), line, m2.astype(F32), line2


# ---------------------------------------------------------------- the bay
def water_region():
    """Where the bay is seen: below the horizon, seaward of the water's edge (round twenty's, kept)."""
    pts = [gp(shore_x(z), z) for z in np.geomspace(60000, 700, 40)]
    poly = [(-10, HZ - 1), (W + 10, HZ - 1), (W + 10, pts[0][1])] + pts + [(-10, pts[-1][1] + 20)]
    return mask_poly(SHAPE, poly, soft=0.8, wobble=1.2, seed=3)


def paint_bay(pic, seed):
    """The bay: one wash graded from the paper at the horizon to cobalt at our feet, dragged dry in level streaks so
    the paper sparkles through; paler again in the shallows, and a thread of bare paper where it meets the sand. The
    light that moves on it is the engine's (shimmer, waves). -> the water's mask."""
    x, y = grid(SHAPE)
    X, Z, below = floor(SHAPE)
    wm = water_region()
    t = np.clip((y - HZ) / 132.0, 0, 1)
    wash_ = ramp(t, [(0.0, lerp(HORIZON_C, CERULEAN, 0.16)), (0.07, thin(CERULEAN, 0.48)), (0.20, thin(mixp(CERULEAN, COBALT, 0.25), 0.16)),
                     (0.42, thin(mixp(CERULEAN, COBALT, 0.62), 0.08)), (0.70, thin(COBALT, 0.04)), (1.0, thin(mixp(COBALT, ULTRA, 0.30), 0.02))])
    # level streaks, long near us and short far off (they lie on the water: measured in the world)
    streak = world_noise(X, Z, (900, 46), seed + 21, 3) - 0.5
    wash_ *= (1 + streak[..., None] * 0.20)
    # the shallows: paler and greener within a few metres of the edge
    s = X - M * Z
    shallow = np.clip(1 - (SHORE_A - s) / 520.0, 0, 1) ** 1.5 * below
    wash_ = lerp(wash_, thin(mixp(CERULEAN, VERONESE, 0.22), 0.30), (shallow * 0.55)[..., None])
    # the mountain stands in it upside down (Mom's words for the bay): far out the water is flat and holds what is above
    # the horizon, mirrored and smeared level: the far shore, the foothills, the band of cloud, Fuji's blue flank. Toward
    # the shore the morning's first air breaks it.
    n_ = 140
    mirror = np.zeros_like(pic)
    mirror[HZ:HZ + n_ + 1] = pic[HZ - n_:HZ + 1][::-1]
    mirror = blur(sum(np.roll(mirror, d_, axis=0) for d_ in (-3, -2, -1, 0, 1, 2, 3)) / 7.0, 1.4)
    calm = np.clip(1.0 - (y - HZ) / 118.0, 0, 1) ** 1.3 * np.clip(0.75 + streak * 1.6, 0.3, 1.0)
    wash_ = lerp(wash_, lerp(wash_, mirror, 0.72) * np.array([0.96, 0.98, 1.0], dtype=F32), (calm * 0.62)[..., None]).astype(F32)
    over(pic, wash_, wm)
    # the dry brush: broken level threads of bare paper, most in the middle distance
    spark = step(0.66, 0.76, world_noise(X, Z, (900, 26), seed + 22, 2)) * np.clip(t * 5, 0, 1) * np.clip(1.25 - t, 0, 1)
    over(pic, WPAPER, (spark * 0.70 * wm).astype(F32))
    # two wavelets coming in along the shore, and the thread of white where the water meets the sand
    zs = np.geomspace(60000, 700, 40)
    for off, a in ((-150.0, 0.32), (-62.0, 0.5)):
        pts = [gp(shore_x(z) + off + 16 * math.sin(z / 190.0 + off), z) for z in zs]
        line = mask_line(SHAPE, pts, [max(0.5, kz(z) * 2.0) for z in zs], soft=0.4)
        brk = step(0.35, 0.6, world_noise(X, Z, (260, 260), seed + 23 + int(off), 2))
        over(pic, WPAPER, (line * a * wm * brk).astype(F32))
    edge_pts = [gp(shore_x(z), z) for z in zs]
    line = mask_line(SHAPE, edge_pts, [max(0.8, kz(z) * 2.6) for z in zs], soft=0.5)
    over(pic, WPAPER, (line * 0.8 * wm).astype(F32))
    return wm


def far_boats(layer_):
    """Boats on the bay at three distances, painted still (beyond a few hundred metres nothing moves at this size):
    sails out by the horizon, two nearer under sail, a small boat sculled out from the beach. Each a few touches, the
    farthest the palest; the sails are set (a patch of paper), so no mast stands bare."""
    hull_far = thin(mixp(COBALT, PRUSSIAN, 0.35), 0.42)
    for (bx, by, hgt, pale) in ((58, 304.5, 5.0, 0.55), (236, 303.5, 4.0, 0.62), (318, 305.0, 5.5, 0.52), (398, 303.5, 4.0, 0.62), (94, 309.0, 8.0, 0.40), (452, 310.0, 9.0, 0.36)):
        wdt = hgt * 0.62
        sail = thin(mixp(NAPLES, COBALT, 0.10), 0.80 - (0.55 - pale) * 0.4)
        layer_.poly([(bx - wdt * 0.5, by - hgt * 0.22), (bx + wdt * 0.5, by - hgt * 0.22), (bx + wdt * 0.42, by - hgt), (bx - wdt * 0.42, by - hgt)],
                    WPAPER, sail, g=((bx - wdt, by), (bx + wdt, by)))
        layer_.line([(bx - wdt * 0.85, by), (bx + wdt * 0.95, by - 0.4)], thin(hull_far, pale), max(0.8, hgt * 0.16), 0.9)
        layer_.line([(bx - wdt * 0.6, by + 1.3), (bx + wdt * 0.7, by + 1.3)], WPAPER, 0.6, 0.5)               # its light on the water
    # the sculling boat, a hundred and fifty metres out: a low hull, one man standing at the oar, one sitting
    bx, by = 352.0, 331.0
    c = thin(mixp(COBALT, PRUSSIAN, 0.50), 0.30)
    layer_.poly([(bx - 9, by - 1.2), (bx + 8, by - 1.6), (bx + 10.5, by - 3.4), (bx + 7, by + 1.0), (bx - 7, by + 1.2)], c)
    layer_.line([(bx + 4.5, by - 1.5), (bx + 4.2, by - 8.0)], c, 1.5, 1.0)                                     # the man at the oar
    layer_.ellipse(bx + 4.2, by - 9.0, 1.1, 1.1, c)
    layer_.line([(bx + 4.6, by - 5.5), (bx + 10.5, by + 2.6)], c, 0.7, 0.9)                                    # the sculling oar, over the stern
    layer_.ellipse(bx - 3.5, by - 3.4, 1.4, 1.9, c)                                                            # the one sitting
    layer_.line([(bx - 10, by + 2.2), (bx + 9, by + 2.4)], WPAPER, 0.7, 0.55)
    layer_.line([(bx + 11, by + 1.4), (bx + 24, by + 3.0)], WPAPER, 0.6, 0.4)                                  # its wake
    return layer_

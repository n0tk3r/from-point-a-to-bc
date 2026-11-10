"""PAINT-23 (round twenty-three, DEPTH.md): the FAR plane of the top of the Satta Pass (edo-satta), laid wet in wet,
layer behind layer, each paler, plainer and nearer the sky's colour at the horizon (HORIZON_C, Yui's) than the one in
front of it, and none of them with a key line. Far to near:

    the sky         Yui's graded wash (edo_village_far.paint_sky): deep at the top, the paper at the horizon; clouds
                    lifted out of it, large high up, small and flat low, drawn out to the left by the wind off the sea
    Fuji            the same mountain as at Yui and Nishikurasawa: the kit's cone (edo_kurasawa_kit.Fuji: the cap of
                    cloud and the scene's `fuji` area are drawn round it), painted by Yui's method (edo_village_far.
                    paint_fuji) at this mountain's size: the lit flank and the shade flank, ridges and gullies running
                    down from the summit, the snow BARE PAPER to the shoulders, ragged down the gullies, its foot lost
                    in the air; Yui's band of cloud across its flank and the wisp under its summit, at the same places
    the far coast   to the left of the head of the bay, beyond the Satta headland: the hills behind Yui and Kambara,
                    then the low shore of Kurasawa and Yui with its crumbs of roofs (capes one behind another)
    Izu             east across the bay: three ranges, the backbone (five bumps on its crest: Little Sister counts them),
                    a lower range, and the capes folding out to sea, each nearer one a little firmer
    Okitsu          far west at the right: its hills, a town of a great many small roofs along its shore, and the
                    temple's great roof among dark trees on a rise
    the bay         90 m under the road: one wash graded from the paper at the horizon to deep cobalt under the cliffs,
                    level streaks measured on the water (so they shrink with distance), the paper sparkling through,
                    the far calm holding a breath of what stands above it; the shadows of the wind's clouds lying on it
                    far below; deeper in the near flank's shade at its foot, greener and paler in the shallows
    the far stretch of the headland toward Kurasawa: two spurs, mist between them; its cliffs facing us at the water,
                    rock in strata, lit; THE OLD SHORE at their foot: white water on the rocks (the road ran there
                    before 1655: "forget your parent, forget your child")
    the near flank  our own mountainside falling away under the bank at the left, seen from above: woods whose crowns
                    are large at its top and small at its foot, rock scars, rocks and white water at the waterline

What the engine moves over it is unchanged (the scene file's fx): white water along the old shore and round the near
flank's foot (the coastlines COAST and CLIFF_FOOT have not moved), the bay's glitter and its middle rows, the gulls.
Nothing here is copied from any print or painting: the place is the scene's own (round twenty-one).
"""

import math

import numpy as np

from brush import *
import sky as skylib
import land
from edo_satta_kit import *
import edo_village_far as YF

_TILE = {}
YUI_SEED = 1830                                                      # Yui's (edo_village.SEED): Fuji's ridges, gullies and snow are the same mountain's


def tile(seed, octaves=3, size=1024):
    t = _TILE.get((seed, octaves))
    if t is None:
        t = _TILE[(seed, octaves)] = noise((size, size), 64, seed, octaves)
    return t


def sea_noise(X, D, cell, seed, octaves=3):
    """Noise that lies on the bay, measured in centimetres on the water (`cell`: across, along), fading to 0.5 where a
    blotch would be smaller than a pixel. X, D: the water's place at every pixel (kit.sea)."""
    size = 1024
    t = tile(seed, octaves, size)
    cu, cv = (cell, cell) if np.isscalar(cell) else cell

    def fold(v):
        m = np.mod(v, 2 * (size - 2))
        return np.where(m > size - 2, 2 * (size - 2) - m, m)
    n = sample(t, fold(X / cu * 64 + 300), fold(D / cv * 64 + 300))
    k = CAM.F / np.maximum(D, 100.0)
    small = np.minimum(cu * k, cv * k * k * (CAM.eye + DROP) / CAM.F)
    fade = np.clip((small - 1.0) / 2.5, 0, 1)
    return (0.5 + (n - 0.5) * fade).astype(F32)


def layer(pic, crest, color, seed, rough=1.6, base=None, foot=0.55, foot_rows=14.0, lit=None, lit_amount=0.0, mask=None):
    """One far layer of land under a skyline (Yui's `layer`, its foot at any row): a wash of `color`, paler toward its
    foot (the air lies in the hollows between layers), lighter where it turns to the sun. No line. -> its mask."""
    x, y = grid(SHAPE)
    base = HZ + 2 if base is None else base
    m, line = land.ridge(SHAPE, crest, base, seed, rough=rough)
    m = m * (x >= crest[0][0]) * (x <= crest[-1][0])
    if mask is not None:
        m = m * mask
    body = np.empty(SHAPE + (3,), dtype=F32)
    body[...] = color
    body *= (1 + (noise(SHAPE, (60, 22), seed + 2, 3) - 0.5)[..., None] * 0.08)
    if lit is not None and lit_amount:
        n = noise(SHAPE, (34, 16), seed + 3, 3)
        facing = np.clip((np.roll(n, -3, axis=1) - n) * 9.0, 0, 1)
        body = lerp(body, np.asarray(lit, dtype=F32), (facing * lit_amount)[..., None])
    down = np.clip((y - (line[None, :] + 1)) / foot_rows, 0, 1)
    body = lerp(body, HORIZON_C, (down ** 1.3 * foot)[..., None])
    over(pic, body, m.astype(F32))
    return m.astype(F32), line


# ================================================================ the sky
def paint_sky(seed):
    """Yui's wash (its own horizon is 300: at ours, 288, it is already the paper), a breath deeper at the top: we are
    ninety metres higher, and the wind has scoured the air."""
    pic = YF.paint_sky(seed)
    x, y = grid(SHAPE)
    deep = np.clip(1 - y / 170.0, 0, 1) ** 1.6 * 0.10
    pic = lerp(pic, pic * np.array([0.86, 0.90, 0.97], dtype=F32), deep[..., None])
    return np.clip(pic, 0, 1).astype(F32)


def paint_clouds(pic, seed):
    """Clouds lifted out of the wet wash (Yui's tones: bare paper where the sun is on them, a thin grey-blue under
    them), large and high at the upper left, smaller and flatter lower down, and in the gap between Fuji's shoulder and
    the near pine; the wind off the sea draws their edges out to the left in streamers. -> a mask of them."""
    x, y = grid(SHAPE)
    shade = thin(mixp(COBALT, SIENNA, 0.14), 0.68)
    tones = (shade, thin(mixp(COBALT, SIENNA, 0.10), 0.84), WPAPER, WPAPER)
    #         middle x, base row, width, height, billows: the farther (lower), the smaller and flatter
    masses = [(126, 112, 236, 46, 26), (566, 140, 128, 24, 12), (40, 202, 120, 13, 8), (650, 204, 96, 11, 7), (210, 160, 90, 12, 7)]
    thick = skylib.paint_clouds(pic, masses, seed + 5, tones, light=(-0.7, -0.7), ragged=11.0, amount=0.92, reach=30.0)
    # streamers: long level threads torn off the clouds' left ends, and high mares' tails
    n = noise(SHAPE, (260, 7), seed + 6, 4)
    tear = step(0.60, 0.86, n) * np.clip(blur(thick, 14.0) * 5.0, 0, 1) * (1 - thick) * 0.55
    high = step(0.64, 0.90, sample(noise(SHAPE, (300, 13), seed + 7, 4), x + (y - 40) * 0.6, y)) * np.clip(1 - y / 90.0, 0, 1) * 0.30
    low = step(0.62, 0.90, noise(SHAPE, (240, 6), seed + 8, 3)) * np.clip(1 - np.abs(y - 244) / 26.0, 0, 1) * 0.45
    wisp = blur((tear + high + low).astype(F32), 1.0)
    over(pic, WPAPER, np.clip(wisp, 0, 1))
    return np.clip(thick + wisp, 0, 1).astype(F32)


# ================================================================ Fuji (Yui's method, at this mountain's size)
def paint_fuji(pic, seed):
    """The mountain as a form (edo_village_far.paint_fuji, every measure scaled by the mountain's size, FUJI.k): the
    sun behind us and to the left lights the left flank; ridges run down from the summit, each with a lit side; the snow
    is the bare paper, well down to the shoulders and ragged down the gullies; the air takes its foot. The shape is the
    kit's cone (FUJI.mask), so the cap of cloud and the `fuji` area are as they were. -> (mask, snow)."""
    x, y = grid(SHAPE)
    m = FUJI.mask(SHAPE)
    k = FUJI.k
    sx, sy = FUJI.sx, FUJI.sy
    dx, dy = x - (sx + 3 * k), np.maximum(y - (sy - 10 * k), 1.0)
    ang = np.arctan2(dx, dy)
    rad = np.hypot(dx, dy) / k                                       # (in Yui's measure: the same ridges, k times larger)
    tl = noise((512, 512), (13, 230), seed + 3, 3)
    wide = noise((512, 512), (26, 300), seed + 4, 3)

    def rid(t, a, r):
        return sample(t, (a + 1.7) / 3.4 * 500, np.clip(r * 0.9, 0, 500))
    d = 0.02
    lit_r = np.clip(0.5 + 3.0 * (rid(tl, ang + d, rad) - rid(tl, ang - d, rad)), 0, 1)
    lit_r = lerp(0.5, lit_r, np.clip(rad / 90.0, 0.15, 1.0))
    term = sx + 16 * k + 0.10 * (y - sy)
    broad = 1 - step(term - 34 * k, term + 44 * k, x)
    L_snow = np.clip((broad * (0.66 + 0.34 * lit_r) + (1 - broad) * 0.18 * lit_r) * 1.30, 0, 1)
    L_rock = np.clip(broad * (0.74 + 0.26 * lit_r) + (1 - broad) * 0.12 * lit_r, 0, 1)
    snow_c = lerp(thin(mixp(COBALT, ULTRA, 0.25), 0.52), WPAPER, L_snow[..., None])
    rock_c = lerp(thin(mixp(COBALT, ULTRA, 0.32), 0.42), thin(mixp(COBALT, ULTRA, 0.10), 0.58), L_rock[..., None])
    g = 0.62 * rid(wide, ang, rad * 0.5) + 0.38 * rid(tl, ang, rad * 0.4)
    edge = sy + 92 * k + (g - 0.5) * 84 * k + np.clip(np.abs(x - sx) / (120.0 * k), 0, 1) ** 2 * 26 * k
    snow = step(edge + 4 * k, edge - 4 * k, y)
    patch = step(0.62, 0.76, rid(tl, ang, rad)) * step(edge + 34 * k, edge + 2 * k, y) * 0.45
    snow = np.clip(snow + patch, 0, 1)
    body = lerp(rock_c, snow_c, snow[..., None])
    haze_t = np.clip((y - (sy + 128 * k)) / (92.0 * k), 0, 1) ** 1.25
    body = lerp(body, HORIZON_C, (haze_t * 0.80)[..., None])
    over(pic, body, m)
    return m, (snow * m).astype(F32)


def paint_fuji_cloud(pic, seed):
    """Yui's band of cloud lying across the mountain's flank, and the wisp under the summit on the lee side, at the same
    places on the same mountain (edo_village_far.paint_fuji_cloud, scaled): bare paper, soft below. -> its mask."""
    x, y = grid(SHAPE)
    k = FUJI.k
    sx, sy = FUJI.sx, FUJI.sy
    n1 = noise(SHAPE, (150 * k, 1), seed + 8, 3)
    yc = sy + 159 * k + (n1 - 0.5) * 12 * k + 4 * k * np.sin(x / (83.0 * k))
    hw = (5 + 8 * noise(SHAPE, (110 * k, 1), seed + 9, 2)) * k
    gaps = step(0.30, 0.52, noise(SHAPE, (120 * k, 60 * k), seed + 10, 3))
    ends = np.clip((x - (sx - 276 * k)) / (60.0 * k), 0, 1) * np.clip((sx + 186 * k - x) / (80.0 * k), 0, 1)
    up = np.clip(1 - (yc - y) / hw, 0, 1) * (y <= yc)
    down = np.clip(1 - (y - yc) / (hw * 1.5), 0, 1) ** 1.6 * (y > yc)
    band = blur(((up + down) * gaps * ends).astype(F32), 1.3 * k)
    wisp = mask_ellipse(SHAPE, sx + 62 * k, sy + 70 * k, 34 * k, 5.5 * k, soft=2.2 * k, wobble=3.0 * k, seed=seed + 11) * 0.8
    cloud = np.clip(band * 0.95 + wisp, 0, 1) * FUJI.mask(SHAPE)
    tint(pic, thin(mixp(COBALT, SIENNA, 0.14), 0.62), np.clip(blur(np.roll(cloud, int(round(3 * k)), axis=0), 2.0 * k) * 0.5 * (1 - cloud), 0, 1))
    over(pic, WPAPER, cloud)
    return cloud


# ================================================================ the far land, in layers
# to the left of the head of the bay, beyond the Satta headland, near to far: the hills behind Kurasawa and Yui (their low
# shore and its roofs under them), the hills of Kambara beyond, the flat land at the head of the bay
YUI_HILLS = [(176, 289), (190, 282), (206, 276), (222, 279), (240, 272), (258, 268), (276, 274), (294, 270), (312, 276), (332, 273), (352, 280), (374, 284), (404, 289), (432, 292)]
KAMBARA = [(250, 289), (286, 284), (320, 281), (356, 283), (392, 280), (428, 284), (462, 287), (500, 290), (530, 292)]
BAYHEAD = [(380, 291), (430, 289), (480, 289), (530, 290), (560, 292)]
YUI_SHORE = [(186, 291), (230, 289), (280, 290), (330, 289), (380, 291), (430, 292), (452, 294)]
YUI_BEACH = [(186, 306), (230, 302), (280, 299), (340, 297), (400, 295), (452, 294)]
# Izu, east across the bay: its backbone (five bumps: Little Sister counts them), a lower range, the capes at the water
IZU_BACK = [(424, 292), (440, 284), (462, 276), (482, 281), (500, 274), (514, 270), (532, 277), (552, 271), (570, 265), (590, 270), (604, 273),
            (620, 268), (638, 274), (662, 272), (680, 280), (706, 290)]
IZU_MID = [(462, 292), (488, 287), (516, 283), (546, 281), (578, 282), (604, 279), (630, 281), (656, 285), (684, 289), (708, 292)]
IZU_CAPES = [(522, 293), (548, 289), (572, 287), (596, 289), (618, 286), (642, 289), (664, 288), (688, 290), (712, 293)]
OKITSU_HILLS = [(668, 291), (690, 284), (716, 276), (742, 272), (770, 276), (800, 270), (812, 270)]
OKITSU_SHORE = [(690, 303), (720, 309), (770, 313), (812, 316)]


def paint_far_land(pic, seed):
    """Behind the bay, far to near (each nearer one firmer, each farther one paler and plainer, none with a line): the
    flat land at the head of the bay and the hills of Kambara before Fuji's foot, the hills behind Yui; Izu's three
    ranges, the farthest the palest; Okitsu's hills. -> (union, dict of masks)."""
    ms = {}
    ms["bayhead"], _ = layer(pic, BAYHEAD, thin(mixp(COBALT, VIRIDIAN, 0.20), 0.70), seed + 38, rough=0.5, foot=0.6, foot_rows=4.0)
    ms["kambara"], _ = layer(pic, KAMBARA, thin(mixp(COBALT, VIRIDIAN, 0.28), 0.60), seed + 40, rough=1.0, foot=0.70, foot_rows=8.0,
                             lit=thin(mixp(CERULEAN, VERONESE, 0.3), 0.66), lit_amount=0.40)
    ms["yuihills"], _ = layer(pic, YUI_HILLS, thin(mixp(VIRIDIAN, COBALT, 0.42), 0.46), seed + 42, rough=1.3, foot=0.55, foot_rows=12.0,
                              lit=thin(mixp(VERONESE, CERULEAN, 0.3), 0.50), lit_amount=0.55)
    ms["izu3"], _ = layer(pic, IZU_BACK, thin(mixp(COBALT, ULTRA, 0.22), 0.40), seed + 44, rough=0.6, foot=0.62, foot_rows=14.0,
                          lit=thin(mixp(CERULEAN, COBALT, 0.3), 0.52), lit_amount=0.45)
    ms["izu2"], _ = layer(pic, IZU_MID, thin(mixp(COBALT, VIRIDIAN, 0.20), 0.30), seed + 46, rough=0.6, foot=0.55, foot_rows=8.0,
                          lit=thin(mixp(CERULEAN, VERONESE, 0.2), 0.44), lit_amount=0.45)
    ms["izu1"], _ = layer(pic, IZU_CAPES, thin(mixp(COBALT, VIRIDIAN, 0.32), 0.20), seed + 48, rough=0.5, foot=0.35, foot_rows=5.0,
                          lit=thin(mixp(CERULEAN, VERONESE, 0.35), 0.36), lit_amount=0.5)
    ms["okitsu"], _ = layer(pic, OKITSU_HILLS, thin(mixp(VIRIDIAN, COBALT, 0.42), 0.40), seed + 50, rough=1.2, base=320, foot=0.30, foot_rows=22.0,
                            lit=thin(mixp(VERONESE, OCHRE, 0.2), 0.44), lit_amount=0.5)
    union = np.zeros(SHAPE, dtype=F32)
    for v in ms.values():
        np.maximum(union, v, out=union)
    return union, ms


def okitsu_mask():
    pts = OKITSU_HILLS + list(reversed(OKITSU_SHORE)) + [(668, 296)]
    return mask_poly(SHAPE, pts, soft=0.7, wobble=1.0, seed=31)


def yui_mask():
    return mask_poly(SHAPE, YUI_SHORE + list(reversed(YUI_BEACH)), soft=0.7, wobble=1.0, seed=37)


def paint_far_coast(pic, seed, water):
    """Over the bay's far edge: the low shore of Kurasawa and Yui beyond the flank's tip (a strip of land under its
    hills, its beach a thread of paper), and Okitsu's land down to its shore. -> their masks."""
    x, y = grid(SHAPE)
    ym = yui_mask()
    body = np.empty(SHAPE + (3,), dtype=F32)
    body[...] = thin(mixp(VIRIDIAN, COBALT, 0.36), 0.36)
    body = lerp(body, thin(mixp(VERONESE, OCHRE, 0.25), 0.40), (step(0.55, 0.8, noise(SHAPE, (22, 8), seed + 60, 3)) * 0.5)[..., None])
    over(pic, body, ym)
    over(pic, thin(NAPLES, 0.60), (mask_line(SHAPE, YUI_BEACH, [1.5, 1.4, 1.2, 1.0, 0.9, 0.8], soft=0.4) * 0.9).astype(F32))
    om = okitsu_mask()
    ob = np.empty(SHAPE + (3,), dtype=F32)
    ob[...] = thin(mixp(VIRIDIAN, COBALT, 0.40), 0.36)
    t = np.clip((y - 272) / 40.0, 0, 1)
    ob = lerp(ob, thin(mixp(VIRIDIAN, OCHRE, 0.20), 0.34), (t * 0.6)[..., None])
    over(pic, ob, (om * (y > 284)).astype(F32))
    over(pic, thin(NAPLES, 0.55), (mask_line(SHAPE, OKITSU_SHORE, [1.4, 1.7, 2.0, 2.2], soft=0.4) * 0.9).astype(F32))
    return ym, om


# ================================================================ the bay
def bank_mask():
    pts = [(x_, bank_top(x_)) for x_ in np.linspace(-10, 810, 60)]
    return mask_poly(SHAPE, pts + [(810, 610), (-10, 610)], soft=0.6, wobble=0.6, seed=3)


def water_mask():
    pts = [(x_, bank_top(x_)) for x_ in np.linspace(-10, 810, 60)]
    poly = [(-10, HZ - 1), (W + 10, HZ - 1)] + list(reversed(pts))
    return mask_poly(SHAPE, poly, soft=0.6, wobble=0.6, seed=3)


def paint_bay(pic, seed):
    """The bay ninety metres down: one wash graded from the paper at the horizon to deep cobalt under the cliffs,
    greener where we look straight down into it; level streaks measured on the water, long near and short far; the
    far calm holding a breath of what stands above it (the wind roughs it nearer in); dry-brush threads of paper.
    -> the water's mask."""
    x, y = grid(SHAPE)
    X, Zs, D = sea()
    wm = water_mask()
    t = np.clip((y - HZ) / 186.0, 0, 1)
    wash_ = ramp(t, [(0.0, lerp(HORIZON_C, CERULEAN, 0.14)), (0.04, thin(CERULEAN, 0.50)), (0.12, thin(mixp(CERULEAN, COBALT, 0.30), 0.22)),
                     (0.30, thin(mixp(CERULEAN, COBALT, 0.62), 0.08)), (0.58, thin(COBALT, 0.03)), (0.85, mixp(COBALT, ULTRA, 0.22)),
                     (1.0, lerp(mixp(COBALT, ULTRA, 0.30), VIRIDIAN, 0.12))])
    streak = sea_noise(X, D, (5200, 420), seed + 21, 3) - 0.5
    fine = sea_noise(X, D, (1400, 160), seed + 24, 2) - 0.5
    wash_ *= (1 + (streak * 0.22 + fine * 0.08)[..., None])
    # what stands above the horizon, mirrored and smeared level, in the far calm; the wind breaks it nearer in
    n_ = 60
    mirror = np.zeros_like(pic)
    mirror[HZ + 3:HZ + 3 + n_] = pic[HZ - n_ + 3:HZ + 3][::-1]
    mirror = blur(sum(np.roll(mirror, d_, axis=0) for d_ in (-2, -1, 0, 1, 2)) / 5.0, 1.6)
    calm = np.clip(1.0 - (y - HZ) / 46.0, 0, 1) ** 1.4 * np.clip(0.65 + streak * 1.8, 0.2, 1.0) * (y > HZ + 2)
    wash_ = lerp(wash_, lerp(wash_, mirror, 0.6), (calm * 0.40)[..., None]).astype(F32)
    over(pic, wash_, wm)
    # the dry brush: broken level threads of bare paper, most in the middle distance
    spark = step(0.66, 0.76, sea_noise(X, D, (5200, 260), seed + 22, 2)) * np.clip(t * 6, 0, 1) * np.clip(1.15 - t, 0, 1)
    over(pic, WPAPER, (spark * 0.62 * wm).astype(F32))
    # the shadows of the clouds the wind drives over it, lying on the water far below: large near, small and flat far off
    for (cX, cD, a_, b_, amt) in ((-2.6e4, 7.0e4, 2.2e4, 1.3e4, 0.55), (3.0e4, 1.25e5, 3.0e4, 2.2e4, 0.45), (-7.0e4, 2.6e5, 5.0e4, 4.0e4, 0.35), (1.4e5, 4.0e5, 7.0e4, 6.0e4, 0.25)):
        e_ = ((X - cX) / a_) ** 2 + ((D - cD) / b_) ** 2
        sh_ = np.clip((1.0 - e_) * 3.0, 0, 1) * (0.7 + 0.3 * (sea_noise(X, D, (9000, 6000), seed + 26, 2)))
        tint(pic, thin(mixp(COBALT, PRUSSIAN, 0.45), 0.30), (blur(sh_.astype(F32), 2.0) * amt * wm).astype(F32))
    # the wind's dark cat's-paws, nearer in
    paws = step(0.62, 0.78, sea_noise(X, D, (3000, 900), seed + 25, 3)) * np.clip((t - 0.25) * 3, 0, 1)
    tint(pic, thin(mixp(COBALT, ULTRA, 0.4), 0.55), (paws * 0.35 * wm).astype(F32))
    # the water at the foot of the near flank lies in the flank's own shade: deeper, and green where it is shallow
    coast = np.interp(np.arange(W), [p[0] for p in COAST], [p[1] for p in COAST]).astype(F32)
    near_shore = np.clip(1 - (coast[None, :] - y) / 26.0, 0, 1) * (y < coast[None, :] + 2) * (x < 330) * np.clip((330 - x) / 40.0, 0, 1)
    tint(pic, thin(mixp(PRUSSIAN, VIRIDIAN, 0.35), 0.40), (blur(near_shore.astype(F32), 2.0) * 0.55 * wm).astype(F32))
    return wm


# ================================================================ the headland: the far stretch (the old shore) and the near flank
NEAR_SPUR = [(-10, 290), (24, 296), (60, 306), (92, 318), (118, 330), (140, 338)]


def far_mask():
    return mask_poly(SHAPE, RIDGE + list(reversed(CLIFF_FOOT)), soft=0.6, wobble=1.0, seed=34)


def flank_mask():
    pts = [(x_, bank_top(x_) + 2) for x_ in np.linspace(330, -10, 20)]
    return mask_poly(SHAPE, COAST + pts, soft=0.6, wobble=1.2, seed=33)


def cliff_mask():
    return mask_poly(SHAPE, CLIFF_TOP + list(reversed(CLIFF_FOOT)), soft=0.5, wobble=0.8, seed=3 + 1655)


def paint_far_stretch(pic, seed):
    """The farther stretch of the headland toward Kurasawa, a kilometre and more off: two spurs, the far one (round
    twenty-one's skyline) blue-green and soft, the near one greener and firmer with the mist of the hollow along its
    top; the slopes that turn to the sun lit, the folds in shade. Its cliffs at the water are painted after (cliffs()).
    -> (its mask, the near spur's mask)."""
    x, y = grid(SHAPE)
    fm = far_mask()
    body = np.empty(SHAPE + (3,), dtype=F32)
    body[...] = air(thin(mixp(VIRIDIAN, COBALT, 0.30), 0.18), 0.34)
    body *= (1 + (noise(SHAPE, (70, 40), seed + 12, 3) - 0.5)[..., None] * 0.10)
    n = warp(noise(SHAPE, (34, 52), seed + 13, 3), 6.0, 30, seed + 14)
    facing = np.clip((np.roll(n, -3, axis=1) - n) * 7.0, 0, 1)
    lit_m = step(0.45, 0.75, n * 0.5 + facing * 0.5)
    body = lerp(body, air(thin(mixp(VERONESE, OCHRE, 0.10), 0.22), 0.30), (lit_m * 0.75)[..., None])
    fold = step(0.55, 0.8, noise(SHAPE, (26, 70), seed + 15, 3))
    body = lerp(body, air(thin(mixp(VIRIDIAN, PRUSSIAN, 0.30), 0.10), 0.30), (fold * 0.6)[..., None])
    rl = np.interp(np.arange(W), [p[0] for p in RIDGE], [p[1] for p in RIDGE]).astype(F32)
    down = np.clip((y - rl[None, :]) / 60.0, 0, 1)
    body = lerp(body, HORIZON_C, ((1 - down) ** 2 * 0.18)[..., None])                              # its skyline in the air
    over(pic, body, fm)
    # the near spur
    m2, line2 = land.ridge(SHAPE, NEAR_SPUR, 380, seed + 17, rough=1.3)
    m2 = m2 * (x <= NEAR_SPUR[-1][0] + 40) * fm
    ends = np.clip((NEAR_SPUR[-1][0] + 40 - x) / 40.0, 0, 1)
    m2 = m2 * ends
    over(pic, HORIZON_C, (np.clip(1 - np.abs(y - (line2[None, :] - 3)) / 7.0, 0, 1) * fm * (x < 170) * 0.36).astype(F32))
    near_c = air(thin(mixp(VIRIDIAN, OCHRE, 0.12), 0.10), 0.18)
    body2 = np.empty(SHAPE + (3,), dtype=F32)
    body2[...] = near_c
    n2 = warp(noise(SHAPE, (24, 30), seed + 18, 3), 5.0, 24, seed + 19)
    facing2 = np.clip((np.roll(n2, -2, axis=1) - n2) * 8.0, 0, 1)
    body2 = lerp(body2, air(thin(mixp(VERONESE, NAPLES, 0.18), 0.12), 0.16), (step(0.42, 0.72, n2 * 0.5 + facing2 * 0.5) * 0.8)[..., None])
    body2 = lerp(body2, air(mixp(VIRIDIAN, PRUSSIAN, 0.36), 0.20), (step(0.56, 0.78, noise(SHAPE, (20, 40), seed + 20, 3)) * 0.5)[..., None])
    over(pic, body2, m2.astype(F32))
    return fm, m2.astype(F32)


def paint_cliffs(pic, seed):
    """The far stretch's cliffs at the water, a kilometre off, facing us and the sun: warm grey rock in buttresses, each
    lit on its left face and shaded on its right (the sun behind us and to the left), the beds of the rock dipping a
    little to the left, green on its ledges, its foot dark and wet. No line. The white water at its foot is old_shore().
    -> the cliffs' mask."""
    x, y = grid(SHAPE)
    cm = cliff_mask()
    top = np.interp(np.arange(W), [p[0] for p in CLIFF_TOP], [p[1] for p in CLIFF_TOP]).astype(F32)
    foot = np.interp(np.arange(W), [p[0] for p in CLIFF_FOOT], [p[1] for p in CLIFF_FOOT]).astype(F32)
    v = np.clip((y - top[None, :]) / np.maximum(foot - top, 1)[None, :], 0, 1)             # 0 at the lip, 1 at the water
    lit_rock = air(thin(mixp(OCHRE, NAPLES, 0.40), 0.40), 0.16)
    mid_rock = air(thin(mixp(PRUSSIAN, OCHRE, 0.30), 0.42), 0.18)
    shade_rock = air(thin(mixp(PRUSSIAN, COBALT, 0.30), 0.30), 0.18)
    wet = air(mixp(PRUSSIAN, SIENNA, 0.32), 0.18)
    # the buttresses: a profile across the cliff, each rib's left face toward the sun
    prof = noise((1, W * 4), (11, 1), seed + 30, 3)[0, :W]
    prof = np.cumsum(prof - prof.mean())
    ridge_ = np.gradient(blur(np.tile(prof[None, :], (8, 1)).astype(F32), 1.0)[4])
    face = np.clip(0.5 - ridge_[None, :] * 0.9, 0, 1) * np.ones(SHAPE, dtype=F32)          # 1: a face turned to the left (lit)
    rock = lerp(shade_rock, lit_rock, face[..., None])
    rock = lerp(rock, mid_rock, 0.35)
    beds = sample(noise(SHAPE, (160, 2.4), seed + 31, 3), x, y + (x - 100) * 0.06)
    rock *= (1 + (beds - 0.5)[..., None] * 0.12)
    rock = lerp(rock, wet, (step(0.72, 1.0, v) * 0.85)[..., None])
    ledge = step(0.62, 0.80, noise(SHAPE, (18, 3), seed + 34, 3)) * step(0.15, 0.3, v) * (1 - step(0.6, 0.75, v))
    rock = lerp(rock, air(thin(mixp(VIRIDIAN, OCHRE, 0.3), 0.20), 0.18), (ledge * 0.7)[..., None])
    over(pic, rock, cm)
    lip = mask_line(SHAPE, [(p[0], p[1] + 1.0) for p in CLIFF_TOP], 2.4, soft=0.6) * step(0.30, 0.55, noise(SHAPE, (12, 4), seed + 33, 2))
    over(pic, air(thin(mixp(VIRIDIAN, PRUSSIAN, 0.3), 0.10), 0.20), (lip * 0.85).astype(F32))
    return cm


def paint_flank(pic, seed):
    """The near flank: our own mountainside falling away under the bank at the left, from about 300 m out (just over
    the bank's top) to its waterline 500 m out and 90 m down. It falls away from the sun, so it lies in its own shade:
    a cool deep green, a little warmer and darker at its top, paler and bluer toward the water (the air), ribs and
    gullies running down it. Its wood and rocks are flank_things(). -> its mask."""
    x, y = grid(SHAPE)
    m = flank_mask()
    coast = np.interp(np.arange(W), [p[0] for p in COAST], [p[1] for p in COAST]).astype(F32)
    v = np.clip((TOPS[None, :] - y) / np.maximum(TOPS - coast, 6)[None, :], 0, 1)             # 0 just over the bank, 1 at the water
    body = ramp(v, [(0.0, lerp(mixp(VIRIDIAN, PRUSSIAN, 0.55), SIENNA, 0.06)), (0.5, mixp(VIRIDIAN, PRUSSIAN, 0.46)),
                    (1.0, air(thin(mixp(VIRIDIAN, COBALT, 0.45), 0.08), 0.24))])
    # ribs and gullies down the fall of the slope: they run away from us toward the water (up the picture), narrowing as
    # they go; each rib's left side turned to the sun, its right side and the gully beyond it darker
    fan = (x - 120) * (1 + (TOPS[None, :] - y) / 45.0)
    rib = sample(noise((1, W * 4), (30, 1), seed + 44, 3), np.clip(fan + 600, 0, W * 4 - 1), np.zeros_like(fan))
    slope_ = np.gradient(rib, axis=1) * (1 + (TOPS[None, :] - y) / 45.0) ** -1
    facing = np.clip(-slope_ * 60.0, -1, 1)
    body = lerp(body, air(lerp(mixp(VIRIDIAN, VERONESE, 0.35), OCHRE, 0.08), 0.12), (np.clip(facing, 0, 1) * 0.55)[..., None])
    body = lerp(body, air(mixp(PRUSSIAN, VIRIDIAN, 0.30), 0.05), (np.clip(-facing, 0, 1) * 0.50)[..., None])
    body *= (1 + (noise(SHAPE, (30, 14), seed + 41, 3) - 0.5)[..., None] * 0.10)
    over(pic, body, m)
    return m, facing.astype(F32)


# ================================================================ the crisp far things (wet on dry, still no line)
def crowns(L, mask, box, n, seed, size, body, lit, shade, density=None, facing=None, vary=0.08):
    """A wood seen from above: crowns packed close, the farthest first, each the wood's own colour a little varied
    (some bluer, some yellower), lighter where the ground under it turns to the sun and darker in the gullies
    (`facing`, -1 to 1), with a fleck of sun on its upper left (the sun behind us and to the left) and its own shade low
    on the right. No outline: the crowns run together, as a canopy does. `size(x, y)` is a crown's half width there;
    `body`, `lit`, `shade` colours, or functions of the row."""
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = box
    pts = []
    for _ in range(n):
        px_, py_ = rng.uniform(x0, x1), rng.uniform(y0, y1)
        ix, iy = int(min(max(px_, 0), W - 1)), int(min(max(py_, 0), H - 1))
        if mask[iy, ix] < 0.6:
            continue
        if density is not None and rng.random() > density[iy, ix]:
            continue
        pts.append((py_, px_, rng.random(), rng.normal(0, 1), rng.normal(0, 1)))
    col = lambda c, r: np.asarray(c(r) if callable(c) else c, dtype=F32)
    for (py_, px_, r, v1, v2) in sorted(pts):
        s = size(px_, py_) * (0.7 + 0.6 * r)
        if s < 0.5:
            continue
        ix, iy = int(min(max(px_, 0), W - 1)), int(min(max(py_, 0), H - 1))
        f = float(facing[iy, ix]) if facing is not None else 0.0
        b = col(body, py_) * (1 + vary * v1)
        b = b + np.array([0.0, 0.5, -0.5], dtype=F32) * vary * 0.25 * v2
        b = lerp(b, col(lit, py_), max(f, 0.0) * 0.45) if f > 0 else lerp(b, col(shade, py_), -f * 0.40)
        L.ellipse(px_ + s * 0.28, py_ + s * 0.24, s * 1.05, s * 0.78, col(shade, py_), alpha=0.35)
        L.ellipse(px_, py_, s, s * 0.80, np.clip(b, 0, 1), alpha=0.95)
        L.ellipse(px_ - s * 0.30, py_ - s * 0.28, s * 0.55, s * 0.36, col(lit, py_), alpha=(0.55 + 0.35 * max(f, 0)) if r > 0.3 else 0.25)
    return L


def flank_things(L, info, seed):
    """On the near flank, seen from above and in its own shade: a wood of pine and evergreen scrub packed close, the
    crowns larger at its top (300 m off) and smaller toward the water (500 m), the sun catching their tops on the
    left; bare scars of crumbling rock where it is steepest; at the waterline dark wet rock, the sea white along it and
    greener in the shallows."""
    m = info["flank"]
    coast = np.interp(np.arange(W), [p[0] for p in COAST], [p[1] for p in COAST]).astype(F32)

    def v_of(px_, py_):
        i = int(min(max(px_, 0), W - 1))
        return float(np.clip((TOPS[i] - py_) / max(TOPS[i] - coast[i], 6.0), 0, 1))

    def size(px_, py_):
        v = v_of(px_, py_)                                                      # the slope is 60 m under the road at its top, 90 m at the water
        D = (CAM.eye + DROP * (0.66 + 0.34 * v)) * CAM.F / max(py_ - HZ, 1.0)
        return float(np.clip(240.0 * CAM.F / D, 1.0, 6.5))                      # a crown five metres across
    rng = np.random.default_rng(seed)
    air_of = lambda r: float(np.clip((474 - r) / 70.0, 0, 1))
    # scars of bare rock first (the wood overlaps their edges)
    for (cx, cy, rx, ry) in ((30, 468, 14, 6), (98, 447, 9, 4), (166, 438, 7, 3), (230, 448, 6, 3), (60, 490, 10, 5), (134, 452, 5, 2.5)):
        pts = [(cx + rx * math.cos(a) * (0.7 + 0.4 * rng.random()), cy + ry * math.sin(a) * (0.6 + 0.5 * rng.random())) for a in np.linspace(0, 2 * math.pi, 12)[:-1]]
        L.poly(pts, air(thin(mixp(OCHRE, PRUSSIAN, 0.25), 0.40), 0.08 + 0.2 * air_of(cy)), air(mixp(PRUSSIAN, SIENNA, 0.4), 0.1 + 0.2 * air_of(cy)), g=((cx - rx, cy - ry), (cx + rx * 0.5, cy + ry)))
        for j in range(3):
            a0 = (cx + rng.uniform(-rx, rx) * 0.6, cy - ry * 0.7)
            L.line([a0, (a0[0] + rng.normal(0, 1.2), a0[1] + ry * rng.uniform(0.9, 1.4))], air(mixp(SIENNA, PRUSSIAN, 0.5), 0.12), 0.6, 0.45)
    body = lambda r: air(lerp(mixp(VIRIDIAN, PRUSSIAN, 0.46), SIENNA, 0.05), 0.20 * air_of(r))
    lit = lambda r: air(thin(lerp(mixp(VERONESE, VIRIDIAN, 0.35), OCHRE, 0.18), 0.10), 0.28 * air_of(r))
    shade = lambda r: air(mixp(PRUSSIAN, VIRIDIAN, 0.45), 0.18 * air_of(r))
    dens = np.clip(noise(SHAPE, (34, 16), seed + 5, 3) * 1.8 - 0.1, 0.5, 1.0)
    crowns(L, m, (-10, 330, 420, 525), 9000, seed + 1, size, body, lit, shade, density=dens, facing=info["flank_facing"], vary=0.10)
    # the foot of the slope where the cove's far side faces us: a band of sea cliff, lit, under the white water
    xs = np.arange(30.0, 262.0, 1.0)
    hn = noise((1, 400), (9, 1), seed + 11, 3)[0]
    tn = noise((1, 400), (5, 1), seed + 12, 2)[0]
    rock_l, rock_d = air(thin(mixp(OCHRE, PRUSSIAN, 0.30), 0.34), 0.18), air(mixp(PRUSSIAN, SIENNA, 0.40), 0.15)
    for i, x_ in enumerate(xs):
        c_ = float(np.interp(x_, [p[0] for p in COAST], [p[1] for p in COAST]))
        hgt = (1.0 + 3.6 * float(hn[i]) ** 1.3) * math.sin((x_ - 30) / 232.0 * math.pi) ** 0.5
        if hgt < 0.8:
            continue
        L.line([(x_, c_ + 0.3), (x_, c_ + hgt)], lerp(rock_d, rock_l, float(np.clip((tn[i] - 0.35) * 2.5, 0, 1))), 1.1, 0.85)
    # the waterline: dark wet rock along it, the sea white against it, greener and paler in the shallows beyond
    rng = np.random.default_rng(seed + 9)
    xs = np.arange(-6.0, 318.0, 1.5)
    pts = [(x_, float(np.interp(x_, [p[0] for p in COAST], [p[1] for p in COAST]))) for x_ in xs]
    L.line([(px_, py_ - 2.2) for px_, py_ in pts], air(thin(mixp(CERULEAN, VERONESE, 0.40), 0.30), 0.06), 3.6, 0.55)
    L.line([(px_, py_ + 0.6) for px_, py_ in pts], air(mixp(PRUSSIAN, SIENNA, 0.45), 0.10), 1.6, 0.85)
    surge = noise((1, 400), (12, 1), seed + 3, 3)[0]
    for i, (px_, py_) in enumerate(pts):
        w_ = 0.8 + 2.6 * float(surge[i % 400]) ** 1.6
        L.line([(px_ - 0.9, py_ - 0.8 - w_ * 0.3), (px_ + 0.9, py_ - 0.8 - w_ * 0.3)], WPAPER, w_, 0.9)
    return L


def far_stretch_things(L, info, seed):
    """On the far stretch, a kilometre and more off: its wood as a fine canopy (crowns a pixel or two across, the sun on
    their tops), thicker in the folds; a few pines along its skyline, small against the air."""
    fm = info["far"]
    dens = np.clip(noise(SHAPE, (30, 26), seed + 3, 3) * 1.6 - 0.2, 0.15, 1.0)

    def size(px_, r):
        return float(np.clip(0.55 + (r - 236) / 90.0, 0.6, 1.8))
    body = lambda r: air(mixp(VIRIDIAN, PRUSSIAN, 0.34), 0.34)
    lit = lambda r: air(thin(mixp(VERONESE, OCHRE, 0.2), 0.14), 0.30)
    shade = lambda r: air(mixp(PRUSSIAN, VIRIDIAN, 0.4), 0.36)
    crowns(L, fm * (1 - info["cliff"]), (-10, 220, 232, 346), 3200, seed + 1, size, body, lit, shade, density=dens)
    for (px, py_, s_) in ((14, 240, 0.8), (36, 246, 0.6), (58, 254, 0.7), (96, 270, 0.65), (122, 283, 0.6), (160, 304, 0.55), (186, 320, 0.5)):
        cd = air(mixp(VIRIDIAN, PRUSSIAN, 0.5), 0.32)
        L.line([(px, py_ + 1), (px + 0.3, py_ - 6.0 * s_)], cd, 0.7, 0.7)
        L.ellipse(px, py_ - 3.4 * s_, 4.2 * s_, 1.7 * s_, cd, alpha=0.9)
        L.ellipse(px + 1.2 * s_, py_ - 5.8 * s_, 3.0 * s_, 1.4 * s_, cd, alpha=0.9)
    return L


def old_shore(L, seed):
    """THE OLD SHORE: the white water breaking along the foot of the cliffs, broken, wider where it piles up on a rock
    (the paper), the wet rock dark above it, a few black rocks out in the wash with the sea white on their seaward
    side; the road ran here before 1655. The engine's waves move over it (fx oldshore-waves)."""
    rng = np.random.default_rng(seed)
    xs = np.arange(-8.0, 216.0, 1.2)
    pts = [(x_, float(np.interp(x_, [p[0] for p in CLIFF_FOOT], [p[1] for p in CLIFF_FOOT]))) for x_ in xs]
    surge = noise((1, 400), (14, 1), seed + 2, 3)[0]
    for i, (px_, py_) in enumerate(pts):
        w_ = 1.2 + 4.0 * float(surge[i % 400]) ** 1.4
        if rng.random() < 0.92:
            L.line([(px_ - 1.0, py_ + 0.6), (px_ + 1.0, py_ + 0.6 + rng.uniform(-0.3, 0.3))], WPAPER, w_, rng.uniform(0.75, 1.0))
        if float(surge[i % 400]) > 0.62 and rng.random() < 0.35:                    # where it piles up, it climbs the rock
            L.line([(px_, py_ - 0.5), (px_ + rng.normal(0, 0.8), py_ - rng.uniform(2.0, 5.0))], WPAPER, rng.uniform(1.0, 2.0), 0.8)
        if rng.random() < 0.06:
            dy = rng.uniform(3.5, 8.0)
            L.line([(px_ - rng.uniform(2, 5), py_ + dy), (px_ + rng.uniform(2, 6), py_ + dy + 0.4)], WPAPER, 0.7, rng.uniform(0.25, 0.45))
    for (px_, py_) in pts[::23]:
        if rng.random() < 0.30:
            dy = rng.uniform(3, 7)
            s = rng.uniform(0.9, 1.8)
            L.poly([(px_ - s * 1.6, py_ + dy + s * 0.3), (px_ - s * 0.5, py_ + dy - s * 0.7), (px_ + s * 0.9, py_ + dy - s * 0.5), (px_ + s * 1.6, py_ + dy + s * 0.4)],
                   air(mixp(PRUSSIAN, SIENNA, 0.4), 0.2))
            L.line([(px_ - s * 2.0, py_ + dy + s * 0.9), (px_ + s * 2.2, py_ + dy + s * 0.8)], WPAPER, max(0.8, s * 0.9), 0.85)
    return L


def okitsu_town(L, seed):
    """Okitsu, far west in the haze: a great many small roofs along its shore (crumbs: twice the size of Yui), and on
    a rise among dark trees the temple's great hipped roof. Two flats each, pulled toward the air; no line."""
    rng = np.random.default_rng(seed)
    roof_d, roof_l = air(thin(PRUSSIAN, 0.42), 0.36), air(thin(mixp(PRUSSIAN, OCHRE, 0.3), 0.52), 0.34)
    wall = air(thin(NAPLES, 0.55), 0.20)
    for i in range(70):
        cx = rng.uniform(696, 806)
        shore = float(np.interp(cx, [p[0] for p in OKITSU_SHORE], [p[1] for p in OKITSU_SHORE]))
        r = shore - rng.uniform(1.5, 9.0) * (0.6 + 0.4 * (cx - 690) / 120.0)
        if abs(cx - 746) < 16 and r < 300:
            continue
        w = rng.uniform(1.6, 3.2)
        hh = w * rng.uniform(0.45, 0.65)
        L.poly([(cx - w, r + hh * 0.6), (cx + w, r + hh * 0.6), (cx + w, r + hh * 1.2), (cx - w, r + hh * 1.2)], wall, alpha=0.9)
        L.poly([(cx - w, r + hh * 0.6), (cx + w, r + hh * 0.6), (cx + w * 0.55, r), (cx - w * 0.55, r)], roof_d if i % 3 else roof_l)
    # the trees on the rise, and the temple's great roof among them
    for (cx_, cy_, r_) in ((732, 289, 8), (746, 285, 10), (762, 289, 8), (722, 293, 6), (774, 293, 6)):
        L.ellipse(cx_, cy_, r_, r_ * 0.6, air(mixp(VIRIDIAN, PRUSSIAN, 0.42), 0.34))
        L.ellipse(cx_ - r_ * 0.3, cy_ - r_ * 0.25, r_ * 0.55, r_ * 0.3, air(thin(mixp(VERONESE, VIRIDIAN, 0.3), 0.15), 0.34), alpha=0.8)
    tx, ty = 746.0, 292.0
    roof_c, roof_s = air(thin(PRUSSIAN, 0.30), 0.32), air(thin(PRUSSIAN, 0.18), 0.30)
    L.poly([(tx - 14, ty), (tx + 14, ty), (tx + 9, ty - 6.5), (tx - 9, ty - 6.5)], roof_c, roof_s, g=((tx, ty - 6.5), (tx, ty)))
    L.poly([(tx - 15.5, ty + 0.6), (tx + 15.5, ty + 0.6), (tx + 14, ty - 0.8), (tx - 14, ty - 0.8)], roof_s)
    L.line([(tx - 9.5, ty - 6.8), (tx + 9.5, ty - 6.8)], roof_s, 1.0, 1.0)
    L.poly([(tx - 9, ty + 0.6), (tx + 9, ty + 0.6), (tx + 9, ty + 4.2), (tx - 9, ty + 4.2)], air(thin(NAPLES, 0.5), 0.15))
    return L


def yui_town(L, seed):
    """Kurasawa and Yui along their shore under their hills: crumbs of roofs, paler than Okitsu's (farther)."""
    rng = np.random.default_rng(seed)
    for i in range(34):
        cx = rng.uniform(206, 360)
        shore = float(np.interp(cx, [p[0] for p in YUI_BEACH], [p[1] for p in YUI_BEACH]))
        r = shore - rng.uniform(1.0, 4.5)
        w = rng.uniform(1.2, 2.2)
        L.poly([(cx - w, r + 1.1), (cx + w, r + 1.1), (cx + w * 0.55, r), (cx - w * 0.55, r)], air(thin(PRUSSIAN, 0.42), 0.40) if i % 3 else air(thin(mixp(PRUSSIAN, OCHRE, 0.3), 0.5), 0.40))
    return L


#        where it is on the bay (picture), length (m), under sail, heading (+1 to the right); far to near
FLEET = [(232, 297.5, 9, True, 1), (300, 296.5, 8, True, -1), (468, 295.5, 10, True, -1), (556, 297.0, 8, True, 1), (640, 296.0, 9, True, -1),
         (382, 312.0, 9, True, -1), (522, 318.0, 8, True, 1), (612, 335.0, 9, True, -1),
         (444, 372.0, 10, True, -1), (560, 412.0, 8, False, 1), (290, 398.0, 9, True, 1)]


def boats(L, seed):
    """Sails on the bay at several distances: specks of paper near the horizon, small boats under sail further in, and
    the nearest, far below us, seen from above with their wakes (heading downwind, to the left, most of them). Their
    sizes are the water's: a boat nine metres long is four pixels two kilometres out, eleven pixels at six hundred
    metres; a sail is a patch of paper, its far side a breath of blue."""
    rng = np.random.default_rng(seed)
    hull = mixp(SIENNA, PRUSSIAN, 0.55)
    for (px_, py_, ln, sail, hd) in FLEET:
        Dd = (CAM.eye + DROP) * CAM.F / (py_ - HZ)                               # how far off it is (cm)
        k = CAM.F / Dd
        L_ = max(1.2, ln * 100 * k)
        far = float(np.clip((Dd - 5.0e4) / 4.0e5, 0, 1))
        hc = air(hull, 0.10 + 0.55 * far)
        sq = (CAM.eye + DROP) / Dd                                               # how much of its deck we see from up here
        dk = max(0.7, L_ * sq * 1.6)
        if L_ > 3.5:
            if sail or True:                                                     # its wake: a white V spreading behind it on the water
                st = (px_ - hd * L_ / 2, py_ - 0.2)
                L.line([st, (px_ - hd * L_ * 2.6, py_ + L_ * sq * 2.4)], WPAPER, max(0.6, L_ * 0.09), 0.55)
                L.line([st, (px_ - hd * L_ * 2.2, py_ - L_ * sq * 1.2)], WPAPER, max(0.5, L_ * 0.07), 0.40)
            bow, stern = px_ + hd * L_ / 2, px_ - hd * L_ / 2
            L.poly([(stern, py_ - dk), (bow - hd * L_ * 0.12, py_ - dk), (bow + hd * L_ * 0.06, py_ - dk * 0.4), (bow - hd * L_ * 0.12, py_ + 0.3), (stern, py_ + 0.3)], hc)
            L.line([(stern + hd * 0.6, py_ - dk * 0.55), (bow - hd * L_ * 0.18, py_ - dk * 0.55)], air(thin(OCHRE, 0.35), 0.15 + 0.5 * far), max(0.5, dk * 0.5), 0.8)
            if not sail:                                                         # a man at the sculling oar
                L.line([(stern + hd * L_ * 0.15, py_ - dk * 0.6), (stern + hd * L_ * 0.12, py_ - dk * 0.6 - L_ * 0.28)], hc, max(0.7, L_ * 0.09), 0.9)
                L.line([(stern + hd * L_ * 0.12, py_ - dk * 0.6 - L_ * 0.18), (stern - hd * L_ * 0.25, py_ + 0.8)], hc, 0.6, 0.8)
        else:
            L.line([(px_ - L_ / 2, py_), (px_ + L_ / 2, py_)], hc, max(0.7, L_ * 0.35), 0.8)
        if sail:
            sh = max(1.6, 650 * k)
            sw = max(1.0, 420 * k)
            mx = px_ + rng.uniform(-0.1, 0.1) * L_
            bot = py_ - dk * 0.6
            L.poly([(mx - sw * 0.5, bot), (mx + sw * 0.5, bot), (mx + sw * 0.46, bot - sh), (mx - sw * 0.44, bot - sh)],
                   WPAPER, air(thin(mixp(NAPLES, COBALT, 0.14), 0.62), 0.2 * far), g=((mx - hd * sw, bot - sh), (mx + hd * sw, bot)))
            if sh > 3.5:
                L.line([(mx - sw * 0.5, bot - sh), (mx + sw * 0.46, bot - sh)], hc, 0.6, 0.7)
    return L


def wet_mask(info):
    """What was laid wet in wet (watercolor.wash's `soft`): the sky and its clouds 1; Fuji 0.65; the far land a good deal
    firmer (thin layers must not run together); the far stretch 0.5, its cliffs and the old shore 0.3 (the engine's
    white water runs along their foot); the near flank 0.35; the open water 0.75 at the horizon falling to 0.2 at the
    bank; nothing on the bank, the road or anything standing."""
    x, y = grid(SHAPE)
    m = (y < HZ + 1).astype(F32)
    m = m * (1 - 0.35 * info["fuji"])
    m = m * (1 - 0.55 * info["farland"])
    water = info["water"] * np.clip(1.0 - (y - HZ) / 186.0, 0.27, 1.0) * 0.75
    m = np.maximum(m, water)
    m = m * (1 - 0.45 * info["coastland"])
    m = lerp(m, np.minimum(m, 0.5), info["far"])
    m = lerp(m, np.minimum(m, 0.3), np.clip(info["cliff"] + blur(info["foam"], 2.0), 0, 1))
    m = lerp(m, np.minimum(m, 0.35), info["flank"])
    m = m * (1 - info["bank"])
    return np.clip(m, 0, 1).astype(F32)

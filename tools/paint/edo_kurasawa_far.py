"""PAINT-23 (round twenty-three, DEPTH.md): the FAR plane of Nishikurasawa, laid wet in wet, layer behind layer, by Yui's
recipe (edo_village_far.py: the same paints, the same washes, the same mountain) at this scene's camera, so that the two
places on the one shore agree. From the farthest to the nearest, each paler, plainer and nearer the sky's colour at the
horizon (HORIZON_C) than the one in front of it, and none with a key line:

    the sky         a graded wash, deep at the top, the paper at the horizon; ONE cloud in the whole sky (the cap on
                    Fuji: a cut-out, edo_kurasawa.py) and nothing else, as the three say ("One cloud in the whole sky")
    Fuji            Yui's cone as a form: the lit flank and the shade flank, ridges and gullies down from the summit, the
                    snow BARE PAPER with a thin blue wash on its shade side, the snow line ragged down the gullies
    the far shore   Fuji's foothills and the far shore of the head of the bay under them, curving back toward Yui at
                    the left, a thread of sand and Yui's roofs at its near end
    two capes       stepping out into the bay from under Mount Satta, each nearer one steeper, darker and greener
    Mount Satta     the headland at the right: the pass. Close (its foot is the end of the rest place), so the firmest
                    of the far layers: green, its slopes that turn to the sun lit, its folds in shade, pines on its
                    shoulder, the cliff road a pale scratch across its face, white water at its seaward foot
    the bay         a graded wash from the paper at the horizon to cobalt toward us, dragged dry in level streaks (the
                    paper sparkles through); far out it holds the far shore and Fuji's flank upside down; sails at
                    three distances and a sculling boat

The mountain's shape is Yui's (round twenty's cone, the summit 210 px over the horizon, concave flanks); the place and
the view are the scene's own.
"""

import math

import numpy as np

from brush import F32, blur, glow, grid, lerp, mask_ellipse, mask_line, mask_poly, noise, over, ramp, sample, step, tint, warp
import land
from edo_village_kit import (WPAPER, thin, mixp, tintw, WHITE, NAPLES, CERULEAN, COBALT, ULTRA, PRUSSIAN, OCHRE, SIENNA, VERONESE,
                             VIRIDIAN)
from edo_village_far import HORIZON_C
from edo_kurasawa_view import HZ, SHAPE, W, H, FUJI_AT, FUJI_FOOT, FUJI_HALF, CAM, ground_grid, P, k

FAR_ROW = HZ + 1


# ---------------------------------------------------------------- noise lying on the water and the ground (cm)
_TILES = {}


def world_noise(X, Z, cell, seed, octaves=3):
    """Noise lying on the ground or the water, in centimetres (Yui's kit's, at this camera): `cell` the blotches' size
    in cm, or (across, along); it fades to 0.5 where a blotch would be smaller than a pixel. X, Z: ground_grid()."""
    size = 1024
    tile = _TILES.get((seed, octaves))
    if tile is None:
        tile = _TILES[(seed, octaves)] = noise((size, size), 64, seed, octaves)
    cu, cv = (cell, cell) if np.isscalar(cell) else cell

    def fold(t):
        m = np.mod(t, 2 * (size - 2))
        return np.where(m > size - 2, 2 * (size - 2) - m, m)
    n = sample(tile, fold(X / cu * 64 + 300), fold(Z / cv * 64 + 300))
    kk = CAM.F / np.maximum(Z, 50.0)
    small = np.minimum(cu * kk, cv * kk * kk * CAM.eye / CAM.F)
    fade = np.clip((small - 1.0) / 2.5, 0, 1)
    return (0.5 + (n - 0.5) * fade).astype(F32)


def world_noise_uv(Uc, Vc, Z, cell, seed, octaves=3):
    """The same, laid along a way: Uc across it and Vc along it (cm), Z the lens distance for the fade (so streaks run
    round the road's bend)."""
    size = 1024
    tile = _TILES.get((seed, octaves))
    if tile is None:
        tile = _TILES[(seed, octaves)] = noise((size, size), 64, seed, octaves)
    cu, cv = (cell, cell) if np.isscalar(cell) else cell

    def fold(t):
        m = np.mod(t, 2 * (size - 2))
        return np.where(m > size - 2, 2 * (size - 2) - m, m)
    n = sample(tile, fold(Uc / cu * 64 + 300), fold(Vc / cv * 64 + 300))
    kk = CAM.F / np.maximum(Z, 50.0)
    small = np.minimum(cu * kk, cv * kk * kk * CAM.eye / CAM.F)
    fade = np.clip((small - 1.0) / 2.5, 0, 1)
    return (0.5 + (n - 0.5) * fade).astype(F32)


# ---------------------------------------------------------------- the sky
def paint_sky(seed):
    """Yui's graded wash: deep at the top, the paper at the horizon, never even; the sun behind us on the left warms
    the paper a breath low on that side. No clouds: the cap on Fuji is the one cloud."""
    x, y = grid(SHAPE)
    drift = (noise(SHAPE, (520, 220), seed, 3) - 0.5) * 0.10
    t = np.clip(y / float(HZ) + drift, 0, 1)
    pic = ramp(t, [(0.0, thin(mixp(COBALT, ULTRA, 0.32), 0.04)), (0.16, thin(mixp(COBALT, ULTRA, 0.16), 0.10)), (0.36, thin(COBALT, 0.24)),
                   (0.58, thin(mixp(COBALT, CERULEAN, 0.55), 0.42)), (0.78, thin(CERULEAN, 0.70)), (0.93, HORIZON_C), (1.0, HORIZON_C)])
    pic *= (1 + (noise(SHAPE, (420, 34), seed + 1, 3) - 0.5)[..., None] * 0.07)          # the wide brush, drawn across
    glow(pic, thin(NAPLES, 0.4), (np.clip(1 - x / 460.0, 0, 1) * np.clip(1 - np.abs(y - (HZ - 32)) / 80.0, 0, 1) * 0.12).astype(F32))
    # the morning's haze lying on the water at the horizon: a level breath of paper, not a cloud
    band = np.clip(1 - np.abs(y - (HZ - 6)) / 14.0, 0, 1) * (0.6 + 0.4 * noise(SHAPE, (300, 8), seed + 2, 3))
    over(pic, HORIZON_C, (band * 0.45).astype(F32))
    return np.clip(pic, 0, 1).astype(F32)


# ---------------------------------------------------------------- Fuji (Yui's, at this scene's place)
def fuji_mask():
    x, y = grid(SHAPE)
    sx, sy = FUJI_AT
    t = np.clip((y - sy) / (FUJI_FOOT + 2 - sy), 0, 1)
    half = 12 + (FUJI_HALF - 12) * t ** 1.7
    cap = np.clip((y - sy) / 9.0, 0, 1)
    half = half * (0.55 + 0.45 * cap)
    m = (np.abs(x - sx - 6 * (1 - cap)) < half) & (y >= sy) & (y < FUJI_FOOT + 2)
    m = warp(m.astype(F32), 1.4, 40, 7)
    return np.clip(m, 0, 1)


def paint_fuji(pic, seed):
    """The mountain as a form (Yui's: edo_village_far.paint_fuji). The sun is behind us and to the left: the left flank
    lit, the right in shade, softly; ridges down from the summit, each with a lit side; the snow the bare paper."""
    x, y = grid(SHAPE)
    m = fuji_mask()
    sx, sy = FUJI_AT
    hgt = FUJI_FOOT - sy                                              # (Yui's is 220: the same mountain within a few per cent)
    s = hgt / 220.0
    dx, dy = x - (sx + 3), np.maximum(y - (sy - 10), 1.0)
    ang = np.arctan2(dx, dy)
    rad = np.hypot(dx, dy) / s
    tile = noise((512, 512), (13, 230), seed + 3, 3)
    wide = noise((512, 512), (26, 300), seed + 4, 3)

    def rid(t, a, r):
        return sample(t, (a + 1.7) / 3.4 * 500, np.clip(r * 0.9, 0, 500))
    d = 0.02
    lit_r = np.clip(0.5 + 3.0 * (rid(tile, ang + d, rad) - rid(tile, ang - d, rad)), 0, 1)
    lit_r = lerp(0.5, lit_r, np.clip(rad / 90.0, 0.15, 1.0))
    term = sx + 16 * s + 0.10 * (y - sy)
    broad = 1 - step(term - 34 * s, term + 44 * s, x)
    L_snow = np.clip((broad * (0.66 + 0.34 * lit_r) + (1 - broad) * 0.18 * lit_r) * 1.30, 0, 1)
    L_rock = np.clip(broad * (0.74 + 0.26 * lit_r) + (1 - broad) * 0.12 * lit_r, 0, 1)
    snow_c = lerp(thin(mixp(COBALT, ULTRA, 0.25), 0.52), WPAPER, L_snow[..., None])
    rock_c = lerp(thin(mixp(COBALT, ULTRA, 0.32), 0.42), thin(mixp(COBALT, ULTRA, 0.10), 0.58), L_rock[..., None])
    g = 0.62 * rid(wide, ang, rad * 0.5) + 0.38 * rid(tile, ang, rad * 0.4)
    edge = sy + 92 * s + (g - 0.5) * 84 * s + np.clip(np.abs(x - sx) / (120.0 * s), 0, 1) ** 2 * 26 * s
    snow = step(edge + 4, edge - 4, y)
    patch = step(0.62, 0.76, rid(tile, ang, rad)) * step(edge + 34 * s, edge + 2, y) * 0.45
    snow = np.clip(snow + patch, 0, 1)
    body = lerp(rock_c, snow_c, snow[..., None])
    haze_t = np.clip((y - (sy + 128 * s)) / (92.0 * s), 0, 1) ** 1.25
    body = lerp(body, HORIZON_C, (haze_t * 0.80)[..., None])
    over(pic, body, m)
    return m, (snow * m).astype(F32)


# ---------------------------------------------------------------- the far land, in layers
def layer(pic, crest, color, seed, rough=1.6, x0=None, x1=None, base=None, foot=0.55, foot_rows=14.0, lit=None, lit_amount=0.0):
    """One far layer of land under a skyline (Yui's): a wash of `color`, paler toward its foot, a little lighter where
    it turns to the sun. No line. -> its mask."""
    x, y = grid(SHAPE)
    m, line = land.ridge(SHAPE, crest, HZ + 2 if base is None else base, seed, rough=rough)
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
    down = np.clip((y - (line[None, :] + 1)) / foot_rows, 0, 1)
    body = lerp(body, HORIZON_C, (down ** 1.3 * foot)[..., None])
    over(pic, body, m.astype(F32))
    return m.astype(F32)


HILLS = [(-10, HZ - 18), (60, HZ - 22), (130, HZ - 17), (200, HZ - 25), (270, HZ - 20), (340, HZ - 27), (410, HZ - 21), (470, HZ - 15), (520, HZ - 9), (560, HZ - 4)]
SHORE = [(-10, HZ - 6), (90, HZ - 8), (190, HZ - 5), (280, HZ - 7), (360, HZ - 5), (430, HZ - 4), (500, HZ - 2)]
CAPE_C = [(414, HZ + 1), (430, HZ - 5), (452, HZ - 8), (480, HZ - 9), (508, HZ - 12), (536, HZ - 15), (560, HZ - 17)]
CAPE_B = [(456, HZ + 1), (470, HZ - 6), (490, HZ - 12), (510, HZ - 16), (532, HZ - 24), (556, HZ - 31), (580, HZ - 38)]
YUI_ROOFS = (232.0, 300.0)                                   # where Yui's roofs lie along the far shore (x from, to)


def paint_far_land(pic, seed):
    """Behind the bay, far to near: Fuji's foothills, the far shore under them curving back toward Yui, and two capes
    stepping out from under Satta. -> the union of their masks."""
    m = layer(pic, HILLS, thin(mixp(COBALT, VIRIDIAN, 0.24), 0.60), seed + 40, rough=1.6, foot=0.70, foot_rows=14.0,
              lit=thin(mixp(CERULEAN, VERONESE, 0.3), 0.66), lit_amount=0.5)
    m = np.maximum(m, layer(pic, SHORE, thin(mixp(COBALT, VIRIDIAN, 0.36), 0.50), seed + 44, rough=0.8, foot=0.35, foot_rows=7.0))
    m = np.maximum(m, layer(pic, CAPE_C, thin(mixp(COBALT, VIRIDIAN, 0.40), 0.36), seed + 48, rough=0.9, foot=0.40, foot_rows=8.0,
                            lit=thin(VERONESE, 0.5), lit_amount=0.35))
    m = np.maximum(m, layer(pic, CAPE_B, thin(mixp(VIRIDIAN, COBALT, 0.40), 0.22), seed + 52, rough=1.1, foot=0.45, foot_rows=11.0,
                            lit=thin(VERONESE, 0.42), lit_amount=0.45))
    return m


def far_marks(L, seed):
    """On the far shore: a thread of sand along it, Yui's roofs at the near end of the curve (beyond a few km: two
    flats each, no line), and a few dabs of shore pines."""
    rng = np.random.default_rng(seed)
    xs = np.linspace(-10, 470, 30)
    sand = [(float(xx), HZ - 3.2 + 0.6 * math.sin(xx / 40.0)) for xx in xs]
    L.line(sand, thin(NAPLES, 0.55), 1.1, 0.75)
    x0, x1 = YUI_ROOFS
    for i in range(11):
        cx = x0 + (x1 - x0) * (i + 0.5 + rng.normal(0, 0.2)) / 11
        w = rng.uniform(2.2, 3.8)
        r = HZ - 4.2 + rng.normal(0, 0.4)
        hh = rng.uniform(1.6, 2.6)
        L.poly([(cx - w, r), (cx + w, r), (cx + w * 0.55, r - hh), (cx - w * 0.55, r - hh)], thin(mixp(PRUSSIAN, OCHRE, 0.3), 0.55 + 0.1 * rng.random()))
        L.poly([(cx - w, r), (cx + w, r), (cx + w, r + hh * 0.6), (cx - w, r + hh * 0.6)], thin(NAPLES, 0.6), alpha=0.85)
    for xx in np.linspace(320, 410, 6):
        L.ellipse(xx + rng.normal(0, 3), HZ - 5.5, 2.0, 1.2, thin(mixp(VIRIDIAN, COBALT, 0.4), 0.45), alpha=0.8)
    return L


# ---------------------------------------------------------------- Mount Satta, the headland at the right
SATTA_CREST = [(522, HZ + 2), (532, HZ - 6), (546, 322), (562, 302), (582, 280), (604, 256), (628, 232), (654, 206), (680, 178), (706, 148),
               (734, 116), (762, 84), (790, 52), (812, 30)]
SHOULDER = [(600, 272), (640, 250), (684, 240), (730, 226), (780, 208), (812, 200)]   # a fold of the slope: the shoulder the cliff road crosses


def paint_satta(pic, seed):
    """Mount Satta: a steep green headland at the right, the nearest of the far layers (no line, but firm). Its seaward
    foot slopes down into the bay to meet the end of the wall; its slopes that turn to the morning sun are lit, the
    gullies running down them in shade; air in the hollow at its foot. -> its mask, its skyline."""
    x, y = grid(SHAPE)
    m, line = land.ridge(SHAPE, SATTA_CREST, H + 10, seed + 11, rough=1.8)
    foot_x = 522.0 + np.clip(y - (HZ + 2), 0, None) * 0.46                  # its seaward foot, down into the bay toward the wall's end
    m = m * np.clip(x - foot_x + 0.5, 0, 1)
    base_c = thin(mixp(VIRIDIAN, OCHRE, 0.12), 0.14)
    body = np.empty(SHAPE + (3,), dtype=F32)
    body[...] = base_c
    body *= (1 + (noise(SHAPE, (90, 60), seed + 12, 3) - 0.5)[..., None] * 0.08)
    # the slope's spurs and gullies run down to the left: a field stretched along that direction
    u = x * 0.62 + y * 0.78
    v_ = -x * 0.78 + y * 0.62
    n = sample(noise((700, 1100), (26, 120), seed + 13, 3), np.clip(u, 0, 1099), np.clip(v_ + 640, 0, 699))
    lit_m = step(0.50, 0.70, n)
    body = lerp(body, thin(mixp(VERONESE, NAPLES, 0.16), 0.16), (lit_m * 0.55)[..., None])               # the spurs that turn to the sun
    gully = step(0.62, 0.80, 1 - n) * step(0.4, 0.7, noise(SHAPE, (60, 90), seed + 15, 2))
    body = lerp(body, mixp(VIRIDIAN, PRUSSIAN, 0.34), (gully * 0.40)[..., None])                          # the gullies, in shade
    sh = np.interp(np.arange(W), [p[0] for p in SHOULDER], [p[1] for p in SHOULDER])
    below = np.clip((y - sh[None, :]) / 22.0, 0, 1) * np.clip(1 - (y - sh[None, :] - 22) / 40.0, 0, 1) * (x > SHOULDER[0][0] - 10)
    body = lerp(body, mixp(VIRIDIAN, PRUSSIAN, 0.30), (below * 0.30)[..., None])
    body = lerp(body, HORIZON_C, ((1 - np.clip((x - 520) / 80.0, 0, 1)) * 0.30)[..., None])            # its seaward foot, farthest off
    body = lerp(body, HORIZON_C, (np.clip((y - 360) / 80.0, 0, 1) * 0.18)[..., None])                  # the air in the hollow at its foot
    over(pic, body, m.astype(F32))
    return m.astype(F32), line


def satta_marks(L, info, seed):
    """On Satta: the cliff road, a pale scratch across its face (the cut above it in shade), pines on its shoulder and
    skyline (small, soft), white water at its seaward foot where the old shore begins."""
    rng = np.random.default_rng(seed)
    road = [(586, 322), (606, 314), (628, 308), (652, 300), (680, 294), (708, 284), (736, 279), (766, 268), (796, 258), (812, 254)]
    rr = np.random.default_rng(seed + 3)
    for i in range(len(road) - 1):
        (x0, y0), (x1, y1) = road[i], road[i + 1]
        wd0, wd1 = 1.6 + 0.10 * (x0 - 586) / 10, 1.6 + 0.10 * (x1 - 586) / 10
        cut0, cut1 = 2.8 + 0.12 * (x0 - 586) / 10, 2.8 + 0.12 * (x1 - 586) / 10
        L.poly([(x0, y0 - 0.6), (x1, y1 - 0.6), (x1, y1 - cut1), (x0, y0 - cut0)], lerp(thin(mixp(OCHRE, SIENNA, 0.4), 0.22), PRUSSIAN, 0.30), alpha=0.75)   # the cut above, in shade
        L.poly([(x0, y0 - 0.6), (x1, y1 - 0.6), (x1, y1 + wd1), (x0, y0 + wd0)], lerp(thin(mixp(NAPLES, OCHRE, 0.32), 0.36), HORIZON_C, 0.12), alpha=0.9)   # the road's bed, lit
    for i in range(16):                                                                     # scrub on the slope below it, here and there over it
        t_ = rr.uniform(0, 1)
        j = min(int(t_ * (len(road) - 1)), len(road) - 2)
        f_ = t_ * (len(road) - 1) - j
        px = road[j][0] + (road[j + 1][0] - road[j][0]) * f_
        py = road[j][1] + (road[j + 1][1] - road[j][1]) * f_ + rr.uniform(-1.0, 4.0)
        r_ = rr.uniform(2.0, 4.2)
        L.ellipse(px, py, r_ * 1.3, r_ * 0.7, lerp(thin(mixp(VIRIDIAN, PRUSSIAN, 0.40), 0.10), HORIZON_C, 0.12), alpha=0.8)
    pine_c, pine_l = lerp(thin(mixp(VIRIDIAN, PRUSSIAN, 0.46), 0.18), HORIZON_C, 0.18), lerp(thin(mixp(VERONESE, VIRIDIAN, 0.40), 0.22), HORIZON_C, 0.18)
    for (px, py_, hgt) in ((548, 318, 9), (566, 300, 10), (588, 278, 11), (614, 252, 12), (642, 226, 12), (668, 198, 13), (694, 168, 13),
                           (720, 136, 14), (748, 104, 14), (776, 72, 15), (636, 262, 9), (700, 238, 10), (760, 222, 11), (602, 290, 8)):
        L.line([(px, py_), (px + 0.8, py_ - hgt)], pine_c, 1.1, 0.9)
        for (ddx, ddy, rx, ry) in ((-0.30, -0.55, 0.42, 0.14), (0.25, -0.72, 0.40, 0.14), (0.0, -0.92, 0.30, 0.12)):
            L.ellipse(px + ddx * hgt, py_ + ddy * hgt, rx * hgt, ry * hgt, pine_c)
            L.ellipse(px + ddx * hgt - 0.1 * hgt, py_ + ddy * hgt - 0.05 * hgt, rx * hgt * 0.6, ry * hgt * 0.5, pine_l, alpha=0.75)
    for i in range(5):                                                                      # white water where the headland meets the bay
        x0 = 522 + i * 6 + rng.uniform(-2, 2)
        L.line([(x0, HZ + 2 + i * 1.1), (x0 + 8 + rng.uniform(0, 5), HZ + 2.6 + i * 1.1)], WPAPER, 0.9, 0.7)
    return L


# ---------------------------------------------------------------- the bay
def paint_bay(pic, seed, region):
    """The bay (Yui's): one wash graded from the paper at the horizon to cobalt toward us, dragged dry in level streaks
    so the paper sparkles through. Far out the water is flat and holds what is above the horizon, mirrored and smeared
    level: the far shore, the capes, Fuji's blue flank. The light that moves on it is the engine's. -> its mask."""
    x, y = grid(SHAPE)
    X, Z, below = ground_grid(SHAPE)
    wm = region
    t = np.clip((y - HZ) / 110.0, 0, 1)
    wash_ = ramp(t, [(0.0, lerp(HORIZON_C, CERULEAN, 0.16)), (0.07, thin(CERULEAN, 0.48)), (0.20, thin(mixp(CERULEAN, COBALT, 0.25), 0.16)),
                     (0.42, thin(mixp(CERULEAN, COBALT, 0.62), 0.08)), (0.70, thin(COBALT, 0.04)), (1.0, thin(mixp(COBALT, ULTRA, 0.30), 0.02))])
    streak = world_noise(X, Z, (900, 46), seed + 21, 3) - 0.5
    wash_ *= (1 + streak[..., None] * 0.20)
    n_ = 120
    mirror = np.zeros_like(pic)
    mirror[HZ:HZ + n_ + 1] = pic[HZ - n_:HZ + 1][::-1]
    mirror = blur(sum(np.roll(mirror, d_, axis=0) for d_ in (-3, -2, -1, 0, 1, 2, 3)) / 7.0, 1.4)
    calm = np.clip(1.0 - (y - HZ) / 96.0, 0, 1) ** 1.3 * np.clip(0.75 + streak * 1.6, 0.3, 1.0)
    wash_ = lerp(wash_, lerp(wash_, mirror, 0.72) * np.array([0.96, 0.98, 1.0], dtype=F32), (calm * 0.62)[..., None]).astype(F32)
    over(pic, wash_, wm)
    spark = step(0.66, 0.76, world_noise(X, Z, (900, 26), seed + 22, 2)) * np.clip(t * 5, 0, 1) * np.clip(1.25 - t, 0, 1)
    over(pic, WPAPER, (spark * 0.70 * wm).astype(F32))
    return wm


def far_boats(L):
    """Boats on the bay at three distances, painted still: sails out by the horizon, two nearer under sail, a small
    boat sculled out from the shore below the wall. Each a few touches, the farthest the palest; every sail set (a
    patch of paper), so no mast stands bare."""
    hull_far = thin(mixp(COBALT, PRUSSIAN, 0.35), 0.42)
    for (bx, by, hgt, pale) in ((338, HZ + 2.5, 4.0, 0.62), (372, HZ + 3.5, 5.0, 0.55), (452, HZ + 2.5, 3.6, 0.64), (494, HZ + 3.0, 4.2, 0.6),
                                (406, HZ + 9.0, 8.0, 0.42), (470, HZ + 14.0, 10.0, 0.34)):
        wdt = hgt * 0.62
        sail = thin(mixp(NAPLES, COBALT, 0.10), 0.80 - (0.55 - pale) * 0.4)
        L.poly([(bx - wdt * 0.5, by - hgt * 0.22), (bx + wdt * 0.5, by - hgt * 0.22), (bx + wdt * 0.42, by - hgt), (bx - wdt * 0.42, by - hgt)],
               WPAPER, sail, g=((bx - wdt, by), (bx + wdt, by)))
        L.line([(bx - wdt * 0.85, by), (bx + wdt * 0.95, by - 0.4)], thin(hull_far, pale), max(0.8, hgt * 0.16), 0.9)
        L.line([(bx - wdt * 0.6, by + 1.3), (bx + wdt * 0.7, by + 1.3)], WPAPER, 0.6, 0.5)
    # the sculling boat, a hundred metres out: a low hull, one man standing at the oar, one sitting
    bx, by = 430.0, 380.0
    c = thin(mixp(COBALT, PRUSSIAN, 0.50), 0.24)
    L.poly([(bx - 11, by - 1.4), (bx + 10, by - 1.9), (bx + 13, by - 4.0), (bx + 8.5, by + 1.2), (bx - 8.5, by + 1.4)], c)
    L.line([(bx + 5.5, by - 1.8), (bx + 5.1, by - 9.8)], c, 1.8, 1.0)
    L.ellipse(bx + 5.1, by - 11.0, 1.35, 1.35, c)
    L.line([(bx + 5.6, by - 6.6), (bx + 12.8, by + 3.1)], c, 0.8, 0.9)
    L.ellipse(bx - 4.2, by - 4.1, 1.7, 2.3, c)
    L.line([(bx - 12, by + 2.6), (bx + 11, by + 2.9)], WPAPER, 0.8, 0.55)
    L.line([(bx + 13, by + 1.7), (bx + 29, by + 3.6)], WPAPER, 0.7, 0.4)
    return L

"""PAINT-23: the FAR plane of the foot of Mount Shosha (edo-shosha), in either light (edo_shosha_kit.LIGHT): the sky with
its clouds smaller and flatter toward the horizon, the far hills on the horizon, the Harima plain far below in layers of
air (painted through the scene's camera: its fields shrink with distance), the castle small and white on its hill, and
the mountain's slope rising behind the hall in layers, each paler and nearer the sky's colour, a band of haze between.
No line anywhere here (DEPTH.md: far layers have none). Everything here was laid wet in wet (the `soft` mask)."""

import math

import numpy as np

from brush import F32, Sheet, blur, curve, grid, lerp, mask_poly, mask_ellipse, noise, over, ramp, sample, step, tint, warp, glow
import land
import edo_shosha_kit as K
from edo_shosha_kit import (W, H, SHAPE, HZ, F, CX, EYE, thin, mixp, tintw, WPAPER, NAPLES, CERULEAN, COBALT, ULTRA, PRUSSIAN, OCHRE, SIENNA,
                            VERONESE, VIRIDIAN, LAKE, VERMILION, ORANGE, VIOLET, LILAC, CHROME)

X_, Y_ = grid(SHAPE)

# The mountain's spur: where its flank turns away and the valley opens at the right (picture points, top to bottom).
SPUR = [(452.0, -12.0), (474.0, 18.0), (500.0, 44.0), (520.0, 58.0), (538.0, 84.0), (560.0, 132.0), (578.0, 150.0), (596.0, 182.0), (612.0, 236.0),
        (624.0, 252.0), (636.0, 290.0), (646.0, 333.0)]
# The mid slope's own edge, in front of the spur, lower (a shoulder of the mountain's foot)
SHOULDER = [(330.0, -12.0), (372.0, 40.0), (420.0, 112.0), (468.0, 178.0), (510.0, 232.0), (548.0, 278.0), (574.0, 312.0), (590.0, 336.0)]
FAR_HILLS = [(560.0, 331.0), (604.0, 322.0), (640.0, 318.0), (676.0, 314.0), (708.0, 318.0), (736.0, 312.0), (772.0, 307.0), (812.0, 310.0)]
CASTLE_AT = (747.0, 337.0)          # the foot of the castle's hill on the plain (picture)
PLAIN_Y = -4200.0                   # the plain's level below the terrace (cm)


def left_of(curve_pts, soft=0.8):
    """A mask of everything to the left of a line that runs from the top of the picture down (the mountain's side)."""
    ys = [p[1] for p in curve_pts]
    xs = [p[0] for p in curve_pts]
    edge = np.interp(Y_[:, 0], ys, xs, left=xs[0], right=xs[-1])
    m = np.clip((edge[:, None] - X_) / max(soft, 0.3) + 0.5, 0, 1)
    return m.astype(F32), edge


# ---------------------------------------------------------------- the sky
def sky():
    """The graded wash, laid wet: deepest at the top, the paper toward the horizon, never even. GOLD: a clear afternoon,
    a warm breath of haze low down. SUNSET: the eastern sky at sundown: cobalt going violet at the top, a band of rose
    (geranium lake thinned) over the far hills, the haze at the horizon lilac (the act's licence: chrome orange and
    geranium lake, here and in the clouds lit from below)."""
    drift = (noise(SHAPE, (520, 220), 31, 3) - 0.5) * 0.10
    t = np.clip(Y_ / float(HZ) + drift, 0, 1)
    if K.LIGHT == "gold":
        pic = ramp(t, [(0.0, thin(mixp(COBALT, ULTRA, 0.30), 0.06)), (0.20, thin(mixp(COBALT, ULTRA, 0.12), 0.14)), (0.42, thin(COBALT, 0.30)),
                       (0.64, thin(mixp(COBALT, CERULEAN, 0.6), 0.48)), (0.82, thin(CERULEAN, 0.70)), (0.95, K.horizon_c()), (1.0, K.horizon_c())])
        glow(pic, thin(NAPLES, 0.35), (np.clip((Y_ - 200) / 130.0, 0, 1) * 0.16).astype(F32))
    else:
        pic = ramp(t, [(0.0, thin(mixp(ULTRA, VIOLET, 0.30), 0.10)), (0.22, thin(mixp(COBALT, VIOLET, 0.35), 0.22)), (0.48, thin(mixp(COBALT, LILAC, 0.5), 0.42)),
                       (0.70, thin(mixp(LAKE, LILAC, 0.45), 0.52)), (0.84, thin(mixp(LAKE, ORANGE, 0.25), 0.58)), (0.93, thin(mixp(LILAC, COBALT, 0.25), 0.55)),
                       (1.0, K.horizon_c())])
    pic *= (1 + (noise(SHAPE, (420, 34), 32, 3) - 0.5)[..., None] * 0.07)              # the wide brush, drawn across
    return np.clip(pic, 0, 1).astype(F32)


def clouds(pic):
    """A few clouds over the valley, lifted out of the wet wash: heaped high up, smaller and flatter toward the far hills
    (the nearest a pile of rounded heads on a flat grey base, the farthest a pale thread). Painted as a watercolourist
    builds a heap, head by head from the back: each head's face toward the light left as the paper, a soft crescent of
    grey-violet on the side away from it, the next head in front laid over that; the base one flat grey wash, its edge
    lost. GOLD: the sun behind us at the left, so the heads face it and only thin crescents fall at their lower right.
    SUNSET: the low sun at our left: their left halves peach and rose, their right halves and bases violet. -> their
    mask."""
    rng = np.random.default_rng(33)
    gold = K.LIGHT == "gold"
    if gold:
        c_lit, c_half = lerp(WPAPER, NAPLES, 0.10), thin(mixp(COBALT, LAKE, 0.20), 0.76)
        c_shade, c_base = thin(mixp(COBALT, SIENNA, 0.22), 0.64), thin(mixp(ULTRA, SIENNA, 0.30), 0.56)
        off = (-0.20, -0.24, 0.98)                       # the lit face: shifted toward the light, nearly the whole head
    else:
        c_lit, c_half = thin(mixp(ORANGE, LAKE, 0.40), 0.48), thin(mixp(LAKE, LILAC, 0.5), 0.54)
        c_shade, c_base = thin(mixp(VIOLET, COBALT, 0.40), 0.48), thin(mixp(VIOLET, LAKE, 0.30), 0.44)
        off = (-0.40, -0.10, 0.92)
    x0, y0, x1, y1 = 420, 0, W, HZ + 4                    # the sky's window: worked there, laid into the picture
    sh = (y1 - y0, x1 - x0)
    yy = np.arange(y0, y1, dtype=F32)[:, None] + np.zeros((1, x1 - x0), F32)
    col = np.zeros(sh + (3,), F32)
    cov = np.zeros(sh, F32)

    def lay(c, m):
        nonlocal col, cov
        out = m + cov * (1 - m)
        col = (c * m[..., None] + col * (cov * (1 - m))[..., None]) / np.maximum(out, 1e-6)[..., None]
        cov = out
    #          middle x, base row, width, height (the heads above the base)
    heaps = [(712.0, 122.0, 210.0, 66.0), (598.0, 182.0, 124.0, 34.0), (774.0, 210.0, 92.0, 20.0)]
    flats = [(664.0, 246.0, 86.0, 7.0), (742.0, 272.0, 62.0, 5.0), (616.0, 287.0, 48.0, 3.5), (782.0, 293.0, 40.0, 3.0)]
    for k_, (cx, by, w, h) in enumerate(heaps):
        lobes = []
        n = max(3, int(round(w / (h * 0.85))))
        for i in range(n):
            u = (i + 0.5) / n
            prof = max(0.0, 1 - (2 * u - 1) ** 2) ** 0.55
            r = h * (0.28 + 0.38 * prof) * rng.uniform(0.85, 1.15)
            x = cx - w / 2 + w * u + rng.normal(0, w * 0.02)
            y = by - r * 0.62 - h * 0.42 * prof * rng.uniform(0.75, 1.0)
            lobes.append((x, y, r * 1.25, r))
            if prof > 0.8 and rng.random() < 0.5:                                      # a head rising out of the middle
                lobes.append((x + rng.normal(0, r * 0.3), y - r * 0.75, r * 0.98, r * 0.82))
            if prof > 0.3 and i % 2 == 0:                                              # and a lower one in front
                lobes.append((x + rng.normal(0, r * 0.4), by - r * 0.45, r * 1.2, r * 0.58))
        heap = np.zeros(sh, F32)
        for j, (x, y, rx, ry) in enumerate(sorted(lobes, key=lambda l: l[1])):        # from the back (the top) forward
            lm = mask_ellipse(sh, x - x0, y - y0, rx, ry, wobble=0.5 + ry * 0.05, seed=k_ * 41 + j) * np.clip((by + 1.0 - yy) / 1.5, 0, 1)
            face = mask_ellipse(sh, x - x0 + off[0] * rx, y - y0 + off[1] * ry, rx * off[2], ry * off[2], wobble=0.8 + ry * 0.06, seed=k_ * 43 + j)
            face = blur(face, 1.0 + ry * 0.10)
            c = lerp(c_shade[None, None, :], c_lit[None, None, :], face[..., None])
            c = lerp(c, c_half[None, None, :], (np.clip(face * (1 - face) * 4, 0, 1) * 0.35)[..., None])
            c = lerp(c, c_base[None, None, :], (np.clip((yy - (by - h * 0.30)) / (h * 0.30), 0, 1) * 0.7)[..., None])
            lay(c, lm)
            np.maximum(heap, lm, out=heap)
        base = mask_poly(sh, [(cx - x0 - w * 0.5, by + 1), (cx - x0 + w * 0.5, by + 1), (cx - x0 + w * 0.46, by - h * 0.15), (cx - x0 - w * 0.48, by - h * 0.15)], soft=1.4, wobble=1.2, seed=k_)
        b_ = base * heap * 0.55
        col = lerp(col, c_base[None, None, :], b_[..., None])
    for k_, (cx, cy, w, h) in enumerate(flats):
        pts = []
        for i in range(15):
            u = i / 14
            x = cx - w / 2 + w * u
            bump = h * (0.55 + 0.45 * math.sin(u * 7.1 + cx * 0.01)) * (1 - (2 * u - 1) ** 2) ** 0.7
            pts.append((x - x0, cy - y0 - bump - rng.uniform(0, h * 0.18)))
        cm = mask_poly(sh, pts + [(cx - x0 + w / 2, cy + h * 0.12), (cx - x0 - w / 2, cy + h * 0.12)], soft=1.4 + h * 0.06, wobble=2.0 + h * 0.08, seed=int(cx + cy)) * 0.55
        c = lerp(c_lit[None, None, :], c_half[None, None, :], np.clip((yy - (cy - h * 0.8)) / max(h, 1.0), 0, 1)[..., None])
        lay(c, cm)
    col = lerp(c_half[None, None, :], col, np.clip(cov * 4.0, 0, 1)[..., None])          # (no dark fringe where the edge spreads)
    col = col * (1 + (noise(sh, (30, 18), 36, 3) - 0.5)[..., None] * 0.06)              # never an even wash
    # the edge: crisp where a head is lit against the blue, lost and soft along the base (wet in wet)
    cov = warp(cov, 1.2, 22, 34)
    solid = blur((cov > 0.5).astype(F32), 4.0)
    lower = np.clip((np.roll(solid, -6, axis=0) - solid) * 3.0, 0, 1)
    edge = np.clip(lerp(blur(cov, 0.6), blur(cov, 2.2), lower), 0, 1)
    full = np.zeros(SHAPE, F32)
    full[y0:y1, x0:x1] = edge
    colf = np.zeros(SHAPE + (3,), F32)
    colf[y0:y1, x0:x1] = np.clip(col, 0, 1)
    over(pic, colf, full * 0.94)
    # level threads of haze near the horizon
    n = noise(SHAPE, (240, 6), 35, 3)
    thread = step(0.62, 0.9, n) * np.clip(1 - np.abs(Y_ - 296) / 26.0, 0, 1) * 0.42
    over(pic, K.horizon_c(), blur(thread.astype(F32), 1.0))
    return np.clip(full + thread, 0, 1).astype(F32)


# ---------------------------------------------------------------- the far hills and the plain
def far_hills(pic):
    """The hills on the horizon beyond the valley: one soft wash nearly the sky's own colour, a second nearer and a
    breath deeper, their tops catching the light. No line."""
    m1, line1 = land.ridge(SHAPE, [(p[0], p[1] - 4) for p in FAR_HILLS], HZ + 1, 36, rough=1.4)
    if K.LIGHT == "gold":
        c1 = lerp(K.horizon_c(), thin(mixp(COBALT, CERULEAN, 0.4), 0.40), 0.78)
        c2 = lerp(K.horizon_c(), thin(mixp(COBALT, VIRIDIAN, 0.3), 0.30), 0.80)
    else:
        c1 = lerp(K.horizon_c(), thin(mixp(VIOLET, COBALT, 0.4), 0.45), 0.55)
        c2 = lerp(K.horizon_c(), thin(mixp(VIOLET, ULTRA, 0.3), 0.40), 0.66)
    body = np.empty(SHAPE + (3,), F32)
    body[...] = c1
    body = lerp(body, K.horizon_c()[None, None, :], (np.clip((Y_ - line1[None, :]) / 12.0, 0, 1) * 0.45)[..., None])
    over(pic, body, (m1 * (X_ > 540)).astype(F32))
    near = [(600.0, 334.0), (640.0, 326.0), (690.0, 323.0), (722.0, 326.0), (760.0, 320.0), (812.0, 322.0)]
    m2, line2 = land.ridge(SHAPE, near, HZ + 2, 37, rough=1.0)
    body2 = np.empty(SHAPE + (3,), F32)
    body2[...] = c2
    if K.LIGHT == "sunset":                                                              # the last light on their tops
        body2 = lerp(body2, thin(mixp(LAKE, ORANGE, 0.4), 0.45)[None, None, :], (np.clip(1 - (Y_ - line2[None, :]) / 4.0, 0, 1) * 0.5)[..., None])
    over(pic, body2, (m2 * (X_ > 560)).astype(F32))
    return np.clip(m1 + m2, 0, 1).astype(F32)


def plain_place():
    """For every pixel below the horizon: the place on the plain far below (X, D in cm)."""
    D = (EYE - PLAIN_Y) * F / np.maximum(Y_ + 0.5 - HZ, 0.3)
    X = (X_ + 0.5 - CX) * D / F
    return X.astype(F32), D.astype(F32)


def plain(pic, region):
    """The Harima plain, far below beyond the terrace's edge, through the camera (its level 42 m under the terrace): at
    this grazing angle its fields lie as thin bands, the nearest a finger wide and warm, the far ones threads lost in
    the air: barley going gold, young green, paddies flooded for planting holding the sky, a rape field's yellow; lines
    of trees between them, villages in their groves, the river a pale ribbon. Paler and plainer toward the far hills.
    SUNSET: the plain gone into the evening's blue, the water holding the rose of the sky. -> its mask."""
    X, D = plain_place()
    below = (Y_ > HZ + 0.5).astype(F32)
    m = region * below
    gold = K.LIGHT == "gold"
    a = math.radians(14.0)
    U, V = X * math.cos(a) + D * math.sin(a), -X * math.sin(a) + D * math.cos(a)
    fu, fv = 7000.0, 2600.0
    iu, iv = np.floor(U / fu + (noise(SHAPE, 120, 38, 2) - 0.5) * 0.3), np.floor(V / fv)
    h = np.sin(iu * 127.1 + iv * 311.7) * 43758.5453
    pick = (h - np.floor(h)).astype(F32)
    if gold:
        tones = [thin(mixp(VERONESE, OCHRE, 0.40), 0.40), thin(mixp(OCHRE, NAPLES, 0.45), 0.46), thin(mixp(VERONESE, VIRIDIAN, 0.25), 0.40),
                 thin(mixp(CHROME, NAPLES, 0.4), 0.55), thin(mixp(CERULEAN, WPAPER, 0.4), 0.62), thin(mixp(OCHRE, SIENNA, 0.20), 0.52)]
    else:
        tones = [thin(mixp(VIRIDIAN, ULTRA, 0.45), 0.42), thin(mixp(VIRIDIAN, VIOLET, 0.40), 0.44), thin(mixp(ULTRA, VIRIDIAN, 0.35), 0.40),
                 thin(mixp(VIOLET, OCHRE, 0.35), 0.46), thin(mixp(LAKE, LILAC, 0.55), 0.55), thin(mixp(VIOLET, SIENNA, 0.35), 0.44)]
    field = np.zeros(SHAPE + (3,), F32)
    edges = [0.0, 0.28, 0.50, 0.66, 0.74, 0.88, 1.0]
    for i, c in enumerate(tones):
        sel = ((pick >= edges[i]) & (pick < edges[i + 1])).astype(F32)
        field += sel[..., None] * c[None, None, :]
    field = lerp(field, blur(field, 0.8), 0.5)
    field = lerp(field, blur(field, 6.0), 0.35)                                 # (the tones closer: thin washes, far off)
    field *= (1 + (noise(SHAPE, (60, 4), 39, 3) - 0.5)[..., None] * 0.06)
    # lines of trees along some of the dikes, and the groves of villages: dark soft strokes, lit on top in the gold light
    px_cm = F / D
    kv = np.abs(V / fv - np.round(V / fv)) * fv
    rowsel = np.sin(np.round(V / fv) * 91.7) > 0.25
    hedge = np.clip(1 - kv * px_cm / 1.4, 0, 1) * rowsel * step(0.35, 0.6, noise(SHAPE, (34, 3), 40, 3)) * np.clip((Y_ - HZ - 6) / 16.0, 0, 1)
    gro = step(0.80, 0.86, noise(SHAPE, (30, 2), 41, 3)) * np.clip((Y_ - HZ - 3) / 10.0, 0, 1)
    gc = mixp(VIRIDIAN, mixp(OCHRE, PRUSSIAN, 0.5), 0.35) if gold else thin(mixp(VIRIDIAN, ULTRA, 0.5), 0.10)
    field = lerp(field, gc[None, None, :], (np.clip(hedge + gro, 0, 1) * 0.55)[..., None])
    if gold:                                                                   # going gold in the low sun
        field = lerp(field, thin(mixp(NAPLES, OCHRE, 0.35), 0.30)[None, None, :], 0.22)
    # the river, a pale ribbon wandering across, holding the sky
    river_x = 30000.0 + 12000.0 * np.sin(D / 70000.0) - 0.18 * D
    riv = np.clip(1 - np.abs(X - river_x) / 2400.0, 0, 1)
    riv = step(0.3, 0.6, riv) * np.clip((Y_ - HZ - 2) / 6.0, 0, 1)
    rc = lerp(K.horizon_c(), WPAPER, 0.5) if gold else thin(mixp(LAKE, ORANGE, 0.3), 0.5)
    field = lerp(field, rc[None, None, :], (riv * 0.85)[..., None])
    # the air: three bands, each nearer the horizon's colour, the farthest nearly gone into it
    depth_t = np.clip(1.0 - (Y_ - HZ) / 115.0, 0, 1)
    field = lerp(field, K.horizon_c()[None, None, :], (0.04 + 0.80 * depth_t ** 3.2)[..., None])
    for (row, amt) in ((HZ + 9, 0.35), (HZ + 26, 0.22)):                      # haze lying in the air at two depths
        field = lerp(field, K.horizon_c()[None, None, :], (np.clip(1 - np.abs(Y_ - row) / 5.0, 0, 1) * amt)[..., None])
    over(pic, np.clip(field, 0, 1), m.astype(F32))
    # villages: small roofs among their trees (true size: 10 m roofs)
    s = Sheet(SHAPE)
    rng = np.random.default_rng(41)
    for _ in range(46):
        px_, py_ = rng.uniform(600, 800), rng.uniform(HZ + 5, 450)
        if region[int(py_), int(min(px_, 799))] < 0.5:
            continue
        Dd = (EYE - PLAIN_Y) * F / max(py_ - HZ, 0.5)
        w = 1100.0 * F / Dd
        if w < 1.4:
            continue
        roof = thin(mixp(PRUSSIAN, OCHRE, 0.25), 0.45) if gold else thin(mixp(ULTRA, VIOLET, 0.3), 0.40)
        roof = lerp(roof, K.horizon_c(), float(np.clip(1 - (py_ - HZ) / 115.0, 0, 1)) * 0.6)
        for q in range(int(rng.integers(1, 4))):
            ox = rng.uniform(-w, w)
            s.poly([(px_ + ox - w / 2, py_), (px_ + ox + w / 2, py_), (px_ + ox + w * 0.3, py_ - w * 0.30), (px_ + ox - w * 0.3, py_ - w * 0.30)], roof, 0.85)
        tc_ = lerp(gc, K.horizon_c(), float(np.clip(1 - (py_ - HZ) / 115.0, 0, 1)) * 0.5)
        for q in range(int(rng.integers(1, 4))):                               # its trees: a few dark crowns about it
            r_ = max(0.5, w * rng.uniform(0.12, 0.22))
            s.ellipse(px_ + rng.uniform(-1.6, 1.6) * w, py_ - rng.uniform(0.0, 0.5) * w, r_ * 1.2, r_ * 0.8, tc_, 0.8)
    c_, a_ = s.done()
    over(pic, c_, a_ * m)
    return m.astype(F32)


class _Scaled:
    """A Sheet seen through a scale about a point (to draw a small thing a little larger)."""
    def __init__(self, sheet, at, k):
        self.s, self.at, self.k = sheet, at, k

    def _p(self, pts):
        ax, ay = self.at
        return [(ax + (x - ax) * self.k, ay + (y - ay) * self.k) for x, y in pts]

    def poly(self, pts, c, a=1.0):
        return self.s.poly(self._p(pts), c, a)

    def line(self, pts, c, w=1.0, a=1.0):
        return self.s.line(self._p(pts), c, w * self.k, a)

    def done(self):
        return self.s.done()


def castle(pic):
    """Himeji's keep on its hill, small and white (drawn about three times the size the eye would see it 6 km off, as
    round twenty-one did: 'the size of a thumbnail'): the hill a soft mound, the stone base, the keep in tiers of white
    walls under grey roofs, two lesser towers. White is the paper; its sunward side the brightest; no line."""
    s = _Scaled(Sheet(SHAPE), CASTLE_AT, 1.18)
    cx, cy = CASTLE_AT
    hz = K.horizon_c()
    hill = thin(mixp(VIRIDIAN, COBALT, 0.40), 0.22) if K.LIGHT == "gold" else thin(mixp(VIRIDIAN, VIOLET, 0.45), 0.30)
    hill = lerp(hill, hz, 0.22)
    s.poly(curve([(cx - 30, cy + 2), (cx - 20, cy - 2), (cx - 11, cy - 6.5), (cx - 3, cy - 9), (cx + 7, cy - 8.5), (cx + 17, cy - 5.5), (cx + 26, cy - 1.5), (cx + 33, cy + 2)], 6) + [(cx + 33, cy + 3), (cx - 30, cy + 3)], hill)
    s.poly(curve([(cx - 18, cy + 1), (cx - 8, cy - 4), (cx + 4, cy - 6), (cx + 16, cy - 2), (cx + 24, cy + 1.5)], 5) + [(cx + 24, cy + 2.5), (cx - 18, cy + 2.5)], lerp(hill, hz, 0.25), 0.7)
    white = WPAPER if K.LIGHT == "gold" else lerp(WPAPER, thin(mixp(LAKE, ORANGE, 0.3), 0.55), 0.55)
    side = lerp(white, thin(mixp(COBALT, LILAC, 0.4), 0.45), 0.55)
    roof = lerp(thin(mixp(PRUSSIAN, COBALT, 0.3), 0.22), hz, 0.15)
    stone = lerp(thin(mixp(PRUSSIAN, OCHRE, 0.3), 0.55), hz, 0.3)
    s.poly([(cx - 9, cy - 7), (cx + 8, cy - 7), (cx + 7, cy - 10), (cx - 8, cy - 10)], stone)
    tiers = [(cx - 7.5, cy - 10, 15.0, 3.6), (cx - 6.2, cy - 14.4, 12.4, 3.4), (cx - 5.0, cy - 18.4, 10.0, 3.2), (cx - 3.6, cy - 22.2, 7.2, 3.0), (cx - 2.4, cy - 25.6, 4.8, 2.6)]
    for (x0, y0, w, h) in tiers:
        s.poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 - h), (x0, y0 - h)], white)
        s.poly([(x0 + w * 0.62, y0), (x0 + w, y0), (x0 + w, y0 - h), (x0 + w * 0.62, y0 - h)], side)
        s.poly([(x0 - 1.4, y0 - h + 0.2), (x0 + w + 1.4, y0 - h + 0.2), (x0 + w * 0.8, y0 - h - 1.3), (x0 + w * 0.2, y0 - h - 1.3)], roof)
    s.poly([(cx - 1.2, cy - 28.2), (cx + 1.2, cy - 28.2), (cx + 0.8, cy - 29.6), (cx - 0.8, cy - 29.6)], roof)
    for (x0, w, h) in ((cx - 21, 7.0, 6.0), (cx + 12, 8.0, 5.2)):                    # the lesser towers and their walls
        s.poly([(x0, cy - 4), (x0 + w, cy - 4), (x0 + w, cy - 4 - h), (x0, cy - 4 - h)], white)
        s.poly([(x0 + w * 0.6, cy - 4), (x0 + w, cy - 4), (x0 + w, cy - 4 - h), (x0 + w * 0.6, cy - 4 - h)], side)
        s.poly([(x0 - 1, cy - 4 - h), (x0 + w + 1, cy - 4 - h), (x0 + w * 0.7, cy - 5.6 - h), (x0 + w * 0.3, cy - 5.6 - h)], roof)
    s.poly([(cx - 21, cy - 3.6), (cx + 20, cy - 3.6), (cx + 20, cy - 2.2), (cx - 21, cy - 2.2)], lerp(white, hz, 0.4), 0.8)
    c_, a_ = s.done()
    over(pic, c_, a_)
    m = np.zeros(SHAPE, F32)
    m[int(cy - 32):int(cy + 3), int(cx - 28):int(cx + 30)] = 1
    return (a_ > 0.1).astype(F32)


# ---------------------------------------------------------------- the mountain's slope, in layers
def crowns(shape_mask, seed, cell, dark, lit, amount=0.5, light=(-1.0, -0.4)):
    """A wooded slope seen from below, as a wash: the texture of crowns, each lit on the side toward the sun, at a size
    `cell` px. -> a colour picture (lay it through the slope's mask)."""
    n = warp(noise(SHAPE, cell, seed, 4), cell * 0.18, cell * 1.6, seed + 1)
    sh = int(max(1, round(cell * 0.18)))
    facing = np.clip((n - np.roll(np.roll(n, sh, axis=1), sh // 2 + 1, axis=0)) * 6.0 * (-light[0]) + 0.5, 0, 1)
    tone = np.clip(0.5 * n + 0.5 * facing, 0, 1)
    pic = lerp(dark[None, None, :], lit[None, None, :], (smoothstep(0.30, 0.78, tone) * amount + (1 - amount) * 0.4)[..., None])
    return pic.astype(F32)


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def mountain(pic):
    """The mountain going up behind the hall: the far slope and the spur (palest, bluest, nearly the sky's colour, its
    edge against the sky ragged with the crowns of pines), the haze lying in the hollow, the shoulder in front of it (a
    breath deeper and greener, its crowns larger). -> (far mask, shoulder mask, spur edge)."""
    far_m, spur_x = left_of(SPUR, soft=1.0)
    crest = (noise((H, 1), (6, 1), 47, 3)[:, 0] - 0.5) * 7.0 + (noise((H, 1), (2, 1), 48, 2)[:, 0] - 0.5) * 3.5
    far_m = np.clip((spur_x[:, None] + crest[:, None] - X_) / 1.0 + 0.5, 0, 1).astype(F32)       # the crowns along its edge
    # its crest against the sky: the crowns of the pines along it, each a rounded head, smaller as it runs down and away
    rng = np.random.default_rng(49)
    heads = np.zeros(SHAPE, F32)
    pts = curve(SPUR, 8)
    for (ax_, ay_), (bx_, by_) in zip(pts[:-1], pts[1:]):
        ln = math.hypot(bx_ - ax_, by_ - ay_)
        for q in range(max(1, int(ln / 5.5))):
            t = (q + rng.random()) / max(1, int(ln / 5.5))
            x_, y_ = ax_ + (bx_ - ax_) * t, ay_ + (by_ - ay_) * t
            r = (3.8 - 2.2 * np.clip(y_ / HZ, 0, 1)) * rng.uniform(0.7, 1.25)
            tall = 1.7 if rng.random() < 0.15 else 1.0                           # now and then a pine standing above the rest
            heads = np.maximum(heads, mask_ellipse(SHAPE, x_ + r * 0.2, y_ - r * 0.35 * tall, r * 0.85, r * 1.05 * tall))
    far_m = np.maximum(far_m, heads * (X_ > 430))
    far_m = far_m * (Y_ < HZ + 3)
    if K.LIGHT == "gold":
        dark, lit_ = thin(mixp(VIRIDIAN, COBALT, 0.45), 0.42), thin(mixp(VERONESE, CERULEAN, 0.35), 0.50)
    else:
        dark, lit_ = thin(mixp(ULTRA, VIRIDIAN, 0.35), 0.40), thin(mixp(VIOLET, LAKE, 0.25), 0.50)
    body = crowns(far_m, 43, 9.0, dark, lit_, 0.30)
    up = np.clip(1 - Y_ / float(HZ), 0, 1)
    crest_band = np.clip(1 - (spur_x[:, None] - X_) / 9.0, 0, 1)                # its crowns against the sky: the air thinner there
    body = lerp(body, K.horizon_c()[None, None, :], ((0.28 + 0.22 * up) * (1 - 0.40 * crest_band))[..., None])
    over(pic, body, far_m.astype(F32))
    # the haze in the hollow between the spur and the shoulder, and along the spur's foot
    hz_m = np.clip(1 - np.abs(Y_ - 300) / 40.0, 0, 1) * far_m
    over(pic, K.horizon_c(), (hz_m * 0.45).astype(F32))
    # the shoulder: nearer, greener, firmer
    sh_m, sh_x = left_of(SHOULDER, soft=0.8)
    sh_m = warp(sh_m, 2.6, 9, 44) * (Y_ < HZ + 6)
    if K.LIGHT == "gold":
        dark2, lit2 = thin(mixp(VIRIDIAN, PRUSSIAN, 0.25), 0.26), thin(mixp(VERONESE, NAPLES, 0.25), 0.36)
    else:
        dark2, lit2 = thin(mixp(VIRIDIAN, ULTRA, 0.45), 0.24), thin(mixp(VIRIDIAN, VIOLET, 0.35), 0.38)
    body2 = crowns(sh_m, 45, 13.0, dark2, lit2, 0.30)
    body2 = lerp(body2, K.horizon_c()[None, None, :], (0.20 + 0.18 * up)[..., None])
    # pale streaks where the haze lies along its folds
    fold = step(0.6, 0.85, noise(SHAPE, (60, 14), 46, 3)) * 0.18
    body2 = lerp(body2, K.horizon_c()[None, None, :], fold[..., None])
    over(pic, body2, sh_m.astype(F32))
    if K.LIGHT == "sunset":                                                               # the last red light on the spur's crest
        crest = np.clip(1 - np.abs(X_ - (spur_x[:, None] - 3)) / 5.0, 0, 1) * far_m * (Y_ < 250)
        glow(pic, thin(mixp(ORANGE, LAKE, 0.4), 0.35), (blur(crest.astype(F32), 1.2) * 0.35).astype(F32))
    return far_m.astype(F32), sh_m.astype(F32), spur_x


def paint_far(pic, vista):
    """All of it, back to front, onto the sky. `vista`: where the plain is seen (below the horizon, beyond the
    terrace's edge, right of the mountain). -> masks."""
    info = {}
    info["clouds"] = clouds(pic)
    info["hills"] = far_hills(pic)
    info["plain"] = plain(pic, vista)
    info["castle"] = castle(pic)
    info["far"], info["shoulder"], info["spur_x"] = mountain(pic)
    return info

"""The far ranges and the middle distance beside the road (nevada_limo_drive.py, DRIVE-16P): drive-far-l.png,
drive-far-r.png, drive-mid-l.png, drive-mid-r.png.

Each is a side view, low and long: its columns run along the road (they repeat end to end), its bottom row is the
ground at the band's foot, and above the land it is clear. The engine stands it `distance` metres out and draws each
column where that stretch of it is seen, at `focal / z / ppm` of its own size, so it is painted at the size it is drawn
at the near end of the near pane and goes smaller toward the vanishing point.

LEFT (the windows look away from the sun): across the valley, the long ranges (6 km, 0.07 px a metre): broken ranges
and a flat tableland lit full on, warm on the faces turned to the sun, violet in the gullies, pale and blue with the
air between; their aprons of washed-down stone; a dry lake shining at their feet. Nearer (850 m, 0.5 px a metre): the
valley floor, a dry wash with its cut bank and its brush, a few low knolls, and a ranch: a windmill, a stock tank, a
house and a barn in a clump of cottonwoods gone gold for October, a corral.

RIGHT (the windows look toward the sun's side): nearer, lower hills (3 km, 0.14 px a metre), layer behind layer in
the bright air, their faces in shade and a rim of light along every crest. Nearer (850 m): low flat-topped buttes and
knolls, dark against the glare with their sunward edges lit, and a far line of power poles on wooden poles."""

import math

import numpy as np

from brush import F32, Sheet, blur, glow, grid, lerp, over, ramp, rgb, smooth, tint
from nevada_limo_drive_kit import AIR, BANDS, brush_wrapped, pnoise, pwave, smoke, wrap
from nevada_roadside_kit import Paper
from solid import mix


# ---------------------------------------------------------------- profiles that repeat across
def periodic_x(w):
    return np.arange(w, dtype=F32)


def dist_wrap(x, c, w):
    """Signed distance from c to x along a picture that repeats every w."""
    d = (x - c + w / 2) % w - w / 2
    return d


def hill(w, c, half, height, power=0.7):
    """A rounded hill or range's mass: height at c, nothing beyond `half` either side."""
    x = periodic_x(w)
    t = np.clip(1 - (dist_wrap(x, c, w) / half) ** 2, 0, 1)
    return (height * t ** power).astype(F32)


def mesa(w, c, half, height, cap=0.6, talus=0.35):
    """A flat-topped mesa: a cap `cap` of its width, cliffs, then talus slopes spreading to `half`."""
    x = periodic_x(w)
    d = np.abs(dist_wrap(x, c, w))
    top = half * cap
    cliff_w = max(1.5, half * 0.06)
    body = np.where(d <= top, 1.0, np.clip(1 - (d - top) / cliff_w, 0, 1) * (1 - talus) + talus * np.clip(1 - (d - top) / (half - top + 1e-6), 0, 1) ** 1.4)
    return (height * body).astype(F32)


def coverage(h, H):
    """A layer whose top edge is h(x) px above the band's bottom: how much of each pixel it covers (anti-aliased)."""
    y = np.arange(H, dtype=F32)[:, None]
    return np.clip(h[None, :] - (H - 1 - y), 0, 1).astype(F32)


def slope(h):
    """d h / d x, round the seam."""
    return ((np.roll(h, -1) - np.roll(h, 1)) * 0.5).astype(F32)


def lay_made(pic, land, c, a):
    """Lay the made things (poles, the windmill, the ranch) over the band: where one is finer than a pixel and is made
    opaque (cut), it takes most of its own colour, not a ghost of it mixed with the air."""
    thin = (a >= 0.3) & (land < 0.5)
    k = np.where(thin, np.clip(a * 1.7, 0, 1), a)[..., None]
    pic[...] = pic * (1 - k) + c * k


def cut(land, made=None):
    """The band's hard edge: land where it covers half a pixel; a made thing (a pole, the windmill) where it covers
    0.3, so that a leg finer than a pixel stays, as a faint pixel of its colour mixed with the air."""
    a = (land >= 0.5)
    if made is not None:
        a = a | (made >= 0.3)
    return a.astype(F32)


def lay(pic, alpha, color, cov):
    """Lay a layer's colour over the band (colour and coverage), front over back."""
    c = rgb(color) if isinstance(color, str) else color
    m = cov[..., None]
    pic[...] = pic * (1 - m) + c * m
    alpha[...] = np.maximum(alpha, cov)


# ---------------------------------------------------------------- the far ranges, left: lit full on, 6 km off
def peak(w, c, half, height, power=1.2):
    """A pointed summit: height at c, its sides falling straight-ish to nothing at `half` either side."""
    x = periodic_x(w)
    t = np.clip(1 - np.abs(dist_wrap(x, c, w)) / half, 0, 1)
    return (height * t ** power).astype(F32)


def summits(w, c, half, ht, seed, n):
    """A range as a row of pointed summits along its length, unevenly spaced and sized, the tallest toward the middle,
    lesser points on their shoulders, saddles between, on a body that carries them; its crest broken."""
    rng = np.random.default_rng(seed)
    out = hill(w, c, half, ht * 0.42, 0.9)
    us = np.sort(rng.uniform(-0.92, 0.92, n))
    for u in us:
        top = ht * (0.45 + 0.55 * math.sqrt(max(0.0, 1 - u * u))) * rng.uniform(0.62, 1.0)
        wide = half / n * rng.uniform(0.9, 2.4)
        out = np.maximum(out, peak(w, c + u * half, wide, top, rng.uniform(0.85, 1.5)))
        for side in (-1, 1):                                                 # a lesser point on a shoulder
            if rng.random() < 0.6:
                out = np.maximum(out, peak(w, c + u * half + side * wide * rng.uniform(0.45, 0.8), wide * rng.uniform(0.3, 0.5), top * rng.uniform(0.55, 0.8), 1.1))
    jag = pnoise((1, w), 5, seed + 1, 3)[0] - 0.5
    return (out + (out > 2) * jag * 1.4).astype(F32)


def faces(h, H, seed, light=1.0, reach=26.0):
    """How lit each pixel of a mountain face is, lit from the screen's right. Below a stretch of crest that falls to
    the right the face is turned to the sun, below one that rises it is in shade, and these planes run down the face as
    spurs and gullies, wandering a little and fading out toward the foot; the rock's knobs over them."""
    w = h.shape[0]
    yy = np.arange(H, dtype=F32)[:, None]
    depth = np.maximum(h[None, :] - (H - 1 - yy), 0)                        # px below the skyline
    sl = slope(blur(h[None, :], 1.0)[0])
    wob = (pnoise((H, w), (10, 6), seed + 2, 3) - 0.5) * 2.0 * np.clip(depth / 6.0, 0, 3)
    xs = (np.arange(w, dtype=F32)[None, :] + wob) % w
    i0 = np.floor(xs).astype(np.intp)
    f = xs - i0
    s_at = sl[i0] * (1 - f) + sl[(i0 + 1) % w] * f                       # the crest's facing, carried down the face
    spur = np.clip(-s_at * 1.3, -1, 1) * np.exp(-depth / reach)
    knobs = pnoise((H, w), (4, 11), seed, 3)                                # rock ribs, down the fall line
    kx = (np.roll(knobs, -1, axis=1) - np.roll(knobs, 1, axis=1)) * 0.5
    return (spur * 0.6 - kx * 2.2 * light + (knobs - 0.5) * 0.10).astype(F32)


def far_left(fast=False, seed=301):
    w, H, ppm, dist = BANDS["far-l"]
    x = periodic_x(w)
    air = rgb(AIR)
    pic = np.empty((H, w, 3), F32)
    pic[...] = air
    alpha = np.zeros((H, w), F32)
    yy = np.arange(H, dtype=F32)[:, None]
    up = (H - 1 - yy) / H                                                   # 0 at the foot, 1 at the top
    # the farthest range, all along, low and palest
    back = 4.0 + 10.0 * pnoise((1, w), 320, seed, 4)[0] ** 1.4 + 2.0 * (pnoise((1, w), 60, seed + 1, 3)[0] - 0.5)
    cov = coverage(back, H)
    lit = np.clip(0.6 + faces(back, H, seed + 2, 0.6), 0, 1)
    col = ramp(lit, [(0.0, "#a2a4d2"), (0.55, "#c0b8da"), (1.0, "#ecccc4")])
    lay(pic, alpha, lerp(col, air[None, None, :], 0.42), cov)
    # the ranges across the valley: summits and saddles, a flat tableland, a few lone hills
    ranges = [(520, 430, 31.0, 7), (1940, 330, 26.0, 5)]
    tables = [(1290, 215, 19.0), (985, 44, 9.5)]
    hills_ = [(1650, 60, 7.0), (2330, 95, 11.0), (150, 70, 8.0), (1120, 36, 5.0)]
    front = np.zeros(w, F32)
    for i, (c, half, ht, n) in enumerate(ranges):
        front = np.maximum(front, summits(w, c, half, ht, seed + 10 + i, n))
    jag = pnoise((1, w), 7, seed + 4, 3)[0] - 0.5
    for c, half, ht in hills_:
        front = np.maximum(front, hill(w, c, half, ht, 0.9) * (0.88 + 0.24 * pnoise((1, w), 30, seed + int(c), 3)[0]))
    table = np.zeros(w, F32)
    for c, half, ht in tables:
        table = np.maximum(table, mesa(w, c, half, ht, cap=0.62, talus=0.40) + (mesa(w, c, half, ht, 0.62, 0.40) > ht * 0.97) * jag * 0.6)
    front = np.maximum(front, table)
    apron = np.zeros(w, F32)                                                 # washed-down stone spreading out at their feet
    for c, half, ht, n in ranges:
        apron = np.maximum(apron, hill(w, c, half * 1.4, 4.5, 1.7))
    for c, half, ht in tables + hills_:
        apron = np.maximum(apron, hill(w, c, half * 1.5, min(3.5, ht * 0.25), 1.7))
    front = np.maximum(np.maximum(front, apron), 0)
    cov = coverage(front, H)
    lit = 0.64 + faces(front, H, seed + 5)
    depth = np.maximum(front[None, :] - (H - 1 - yy), 0)
    # the tablelands: a cap in the sun, a band of cliff under it broken into buttresses, then the talus
    in_table = (table[None, :] >= front[None, :] - 0.01) & (table[None, :] > 2)
    band_d = 0.45 * table[None, :]                                           # the cliff's depth under the rim
    b = pnoise((1, w), 2.6, seed + 6, 2)[0]                                  # buttresses and the gullies between them
    reach = (0.45 + 0.55 * pnoise((1, w), 3.5, seed + 7, 2)[0])[None, :] * band_d
    sunward = np.zeros(w, F32)                                               # more of the sun toward each table's right end
    for c, half, ht in tables:
        sunward = np.maximum(sunward, np.clip((dist_wrap(x, c, w) + half * 0.62) / (half * 1.24), 0, 1) * (np.abs(dist_wrap(x, c, w)) < half))
    butt = (b[None, :] > 0.48) & (depth < reach)
    cliff = in_table & (depth > 0.8) & (depth < band_d)
    lit = np.where(cliff, np.where(butt, 0.50 + 0.38 * sunward[None, :] ** 1.2, 0.22), lit)
    lit = np.where(in_table & (depth <= 0.8), 0.98, lit)
    lit = np.clip(lit - np.clip(1 - up * 4.0, 0, 1) * 0.06, 0, 1)
    col = ramp(lit, [(0.0, "#6a66aa"), (0.30, "#8880c0"), (0.50, "#b094b6"), (0.70, "#eca486"), (1.0, "#ffd4ae")])
    on_apron = (front <= apron + 0.01)[None, :] & (cov > 0)
    col = np.where(on_apron[..., None], lerp(col, rgb("#e6c0a6")[None, None, :], 0.5), col)
    haze = 0.24 + 0.28 * np.clip(1 - up * 3.2, 0, 1)                        # thicker toward the valley floor
    lay(pic, alpha, lerp(col, air[None, None, :], haze[..., None]), cov)
    # the valley floor at their feet, and the dry lake shining on it
    playa = smooth(np.clip((x - 1480) / 50.0, 0, 1)) * smooth(np.clip((2080 - x) / 50.0, 0, 1))
    cov = coverage(np.full(w, 1.6, F32) + playa * 0.9, H)
    fcol = np.empty((H, w, 3), F32)
    fcol[...] = lerp(rgb("#e4c2a8"), air, 0.42)
    fcol = lerp(fcol, rgb("#faf6f0")[None, None, :], playa[None, :, None] * 0.85)
    lay(pic, alpha, fcol, cov)
    if not fast:
        pic = brush_wrapped(pic, sizes=(4, 2), seed=seed + 7, density=1.4, jitter=0.02, keep=0.58, margin=120, blend=40)
    # crisp: the sunlit rims of the crests turned to the sun, the tablelands' caps, the dry lake's shine
    lines = Paper((H, w), ss=4)
    sl = slope(blur(front[None, :], 0.8)[0])
    for xx in range(w):
        if -sl[xx] > 0.2 and front[xx] > 5 and front[xx] > apron[xx] + 1:
            yt = H - front[xx]
            lines.line([(xx, yt + 0.55), (xx + 1, yt + 0.55 - sl[xx])], "#ffe4c8", 0.8, float(min(0.8, 0.3 + -sl[xx] * 0.35)))
    for c, half, ht in tables:
        for xc in wrap(c, w, 60):
            lines.line([(xc - half * 0.6, H - ht + 0.5), (xc + half * 0.6, H - ht + 0.5)], "#ffe2c0", 0.9, 0.85)
    rng = np.random.default_rng(seed + 8)
    for k in range(80):                                                      # the dry lake: a mirage's glints along it
        gx_ = rng.uniform(1500, 2060)
        lines.line([(gx_, H - 1.6), (gx_ + rng.uniform(3, 16), H - 1.6)], "#ffffff", 0.7, 0.65)
    lc, la = lines.done()
    over(pic, lc, la * (alpha > 0.5))
    return smoke(pic), cut(alpha)


# ---------------------------------------------------------------- the far hills, right: lit from behind, 3 km off
def far_right(fast=False, seed=331):
    w, H, ppm, dist = BANDS["far-r"]
    x = periodic_x(w)
    air = rgb(AIR)
    bright = rgb("#f6eadc")                                                 # the air toward the sun: lit, warm
    pic = np.empty((H, w, 3), F32)
    pic[...] = air
    alpha = np.zeros((H, w), F32)
    yy = np.arange(H, dtype=F32)[:, None]
    up = (H - 1 - yy) / H
    layers = [  # (base height, swell, cell, haze, shade, half tone, rim)
        (10.0, 14.0, 260, 0.58, "#9290c4", "#aaa4cc", "#fff4e0"),
        (5.0, 18.0, 170, 0.38, "#7672b0", "#9690c0", "#ffecd0"),
        (2.5, 22.0, 120, 0.16, "#58548e", "#76709e", "#ffe2bc"),
    ]
    rng = np.random.default_rng(seed)
    for i, (base, swell, cell, hz, shade, half, rimc) in enumerate(layers):
        n = pnoise((1, w), cell, seed + 10 * i, 4)[0]
        h = base + swell * n ** 1.6 + 1.6 * (pnoise((1, w), 18, seed + 10 * i + 1, 3)[0] - 0.5)
        if i == 2:                                                          # rocky knobs on the nearest crests
            for c in rng.uniform(0, w, 9):
                h = np.maximum(h, hill(w, c, rng.uniform(14, 34), float(h[int(c) % w] + rng.uniform(2, 5)), 0.9))
        h = np.maximum(h, 0)
        cov = coverage(h, H)
        sl = slope(blur(h[None, :], 1.2)[0])
        face = pnoise((H, w), (9, 22), seed + 10 * i + 2, 3)
        lit = np.clip(0.30 + (face - 0.5) * 0.3 - sl * 0.6, 0, 1)
        col = ramp(lit, [(0.0, shade), (1.0, half)])
        hz_ = hz + 0.30 * np.clip(1 - (up * H) / np.maximum(h[None, :], 1) * 1.4, 0, 1)    # each layer's foot lost in the bright air
        col = lerp(col, lerp(air, bright, 0.6)[None, None, :], np.clip(hz_, 0, 1)[..., None])
        lay(pic, alpha, col, cov)
        layers[i] = (h, sl, rimc, cov)
    # the bright air along the foot of it all
    floor_ = np.full(w, 1.4, F32)
    lay(pic, alpha, lerp(rgb("#e6cdb8"), bright, 0.55), coverage(floor_, H))
    if not fast:
        pic = brush_wrapped(pic, sizes=(4, 2), seed=seed + 5, density=1.4, jitter=0.02, keep=0.55, margin=120, blend=40)
    for i, (h, sl, rimc, cov_i) in enumerate(layers):                       # the rim of light along every crest turned to the sun
        lines = Paper((H, w), ss=4)
        for xx in range(w):
            r = -sl[xx]
            if r > -0.15 and h[xx] > 3:
                lines.line([(xx, H - h[xx] + 0.45), (xx + 1, H - h[xx] + 0.45 - sl[xx])], rimc, 0.8, float(np.clip(0.45 + r * 0.9, 0.3, 0.95)))
        lc, la = lines.done()
        nearer = np.zeros((H, w), F32)
        for j in range(i + 1, len(layers)):
            nearer = np.maximum(nearer, layers[j][3])
        over(pic, lc, la * (alpha > 0.5) * (nearer < 0.5))
    lines = Paper((H, w), ss=4)
    h3 = layers[2][0]
    for k in range(260):                                                    # dark shrubs on the nearest hills
        xx = rng.uniform(0, w)
        if h3[int(xx) % w] < 5:
            continue
        yv = H - rng.uniform(1.5, h3[int(xx) % w] - 1)
        lines.ellipse(xx, yv, 0.7, 0.45, "#5c5a8c", 0.55)
    lc, la = lines.done()
    over(pic, lc, la * (alpha > 0.5))
    return smoke(pic), cut(alpha)


# ---------------------------------------------------------------- the middle distance (850 m, 0.5 px a metre)
def ground_rows(pic, alpha, w, H, color, seed, specks=900, speck="#6e6a58"):
    """The plain at the band's foot (its bottom two rows) and the brush on it, a pixel or so high."""
    x = periodic_x(w)
    h = np.full(w, 2.0, F32)
    col = np.empty((H, w, 3), F32)
    col[...] = rgb(color) if isinstance(color, str) else color
    col = col * (1 + (pnoise((H, w), (60, 4), seed, 3)[..., None] - 0.5) * 0.08)
    lay(pic, alpha, col, coverage(h, H))
    rng = np.random.default_rng(seed + 1)
    sh = Paper((H, w), ss=4)
    for k in range(specks):
        xx = rng.uniform(0, w)
        r = rng.uniform(0.5, 1.3)
        for xc in wrap(xx, w, 4):
            sh.ellipse(xc, H - 2.0 - r * 0.25, r, r * 0.55, speck, 0.8)
    return sh


def tree(sheet, x, foot, ht, wd, seed, crown=("#7a6a2c", "#b49a34", "#e8c858", "#f8e488"), trunk="#5a4a40"):
    """A cottonwood at 850 m: a few pixels of crown on a short dark trunk, lit on the right."""
    rng = np.random.default_rng(seed)
    sheet.line([(x, foot), (x + rng.normal(0, 0.2), foot - ht * 0.45)], trunk, 0.8)
    cy = foot - ht * 0.62
    for k in range(9):
        a = rng.uniform(0, 2 * math.pi)
        d = rng.random() ** 0.6
        bx, by = x + math.cos(a) * wd * 0.42 * d, cy + math.sin(a) * ht * 0.32 * d
        t = 0.5 + 0.5 * math.cos(a) * d
        sheet.ellipse(bx, by, wd * 0.24, ht * 0.18, crown[min(3, int(t * 3.2))])
    sheet.ellipse(x + wd * 0.18, cy - ht * 0.12, wd * 0.14, ht * 0.1, crown[3], 0.8)


def mid_left(fast=False, seed=361):
    w, H, ppm, dist = BANDS["mid-l"]
    x = periodic_x(w)
    air = rgb(AIR)
    pic = np.empty((H, w, 3), F32)
    pic[...] = air
    alpha = np.zeros((H, w), F32)
    HZ_ = 0.20                                                               # the air over 850 m
    yy = np.arange(H, dtype=F32)[:, None]
    # low knolls, rocky, lit on the right
    knolls = np.zeros(w, F32)
    for c, half, ht in ((1010, 26, 5.5), (1080, 18, 3.5), (2060, 34, 6.5), (420, 14, 2.6), (1790, 20, 3.0)):
        knolls = np.maximum(knolls, hill(w, c, half, ht, 0.9) * (0.85 + 0.3 * pnoise((1, w), 8, seed + int(c), 2)[0]))
    cov = coverage(knolls, H)
    sl = slope(knolls)
    lit = np.clip(0.55 - sl * 0.9 + (pnoise((H, w), (5, 6), seed + 2, 3) - 0.5) * 0.4, 0, 1)
    col = ramp(lit, [(0.0, "#7a6890"), (0.5, "#b08a84"), (1.0, "#f0c09a")])
    lay(pic, alpha, lerp(col, air[None, None, :], HZ_), cov)
    sh = ground_rows(pic, alpha, w, H, lerp(rgb("#d4a274"), air, HZ_), seed + 3, specks=1100, speck=mix("#5c6248", AIR, HZ_))
    # the dry wash: its far bank a step of pale cut earth along the plain, its brush darker and taller
    wash = smooth(np.clip((x - 170) / 30.0, 0, 1)) * smooth(np.clip((780 - x) / 30.0, 0, 1))
    bank = wash * (1.2 + 0.8 * pnoise((1, w), 24, seed + 4, 3)[0])
    cov_b = coverage(2.0 + bank, H) - coverage(np.full(w, 2.0, F32), H)
    bcol = np.empty((H, w, 3), F32)
    bcol[...] = lerp(rgb("#ecc8a0"), air, HZ_)
    lay(pic, alpha, bcol, np.clip(cov_b, 0, 1))
    rng = np.random.default_rng(seed + 5)
    for k in range(70):                                                       # mesquite and desert willow along the wash
        xx = rng.uniform(180, 770)
        hgt = rng.uniform(1.6, 3.4)
        for xc in wrap(xx, w, 6):
            sh.ellipse(xc, H - 2.2 - hgt * 0.45, rng.uniform(1.0, 2.2), hgt * 0.55, mix("#4c5a3c", AIR, HZ_), 0.95)
            sh.ellipse(xc + 0.6, H - 2.4 - hgt * 0.6, 0.8, hgt * 0.3, mix("#8a9a5c", AIR, HZ_), 0.8)
    # the ranch, at x 1430..1560: trees, the house, the barn, the stock tank and the windmill, the corral
    R = 1490.0
    for dx, ht, wd in ((-48, 7.5, 6.0), (-40, 8.5, 7.0), (-30, 7.0, 5.5), (18, 8.0, 6.5), (27, 6.5, 5.0), (52, 7.8, 6.0)):
        tree(sh, R + dx, H - 2.0, ht, wd, seed + 100 + dx, crown=tuple(mix(c, AIR, HZ_) for c in ("#6a5a28", "#a88e30", "#e0c050", "#f8e488")))
    base_y = H - 2.0
    # the house: pale walls, a tin roof that catches the light
    sh.poly([(R - 22, base_y), (R - 22, base_y - 2.6), (R - 6, base_y - 2.6), (R - 6, base_y)], mix("#e8e0d0", AIR, HZ_))
    sh.poly([(R - 23, base_y - 2.5), (R - 5, base_y - 2.5), (R - 6.5, base_y - 3.6), (R - 21.5, base_y - 3.6)], mix("#b8b8c4", AIR, HZ_))
    sh.line([(R - 21, base_y - 3.5), (R - 7, base_y - 3.5)], mix("#ffffff", AIR, HZ_), 0.5, 0.9)
    sh.poly([(R - 4, base_y), (R - 4, base_y - 3.2), (R + 3, base_y - 4.6), (R + 10, base_y - 3.2), (R + 10, base_y)], mix("#9a5a46", AIR, HZ_))   # the barn
    sh.line([(R + 3, base_y - 4.6), (R + 10, base_y - 3.2)], mix("#e4a080", AIR, HZ_), 0.6, 0.9)
    # the stock tank and the windmill over it: a lattice tower, its wheel, its tail
    sh.poly([(R + 30, base_y), (R + 30, base_y - 1.0), (R + 35, base_y - 1.0), (R + 35, base_y)], mix("#8a90a4", AIR, HZ_))
    sh.line([(R + 30, base_y - 1.0), (R + 35, base_y - 1.0)], mix("#e8eef4", AIR, HZ_), 0.4, 0.9)
    wx = R + 38.0
    iron = mix("#4a4652", AIR, HZ_)
    sh.line([(wx - 1.5, base_y), (wx - 0.3, base_y - 6.4)], iron, 0.55)        # the tower's legs, a little taller than true
    sh.line([(wx + 1.5, base_y), (wx + 0.3, base_y - 6.4)], iron, 0.55)
    for yb in (2.0, 4.2):
        sh.line([(wx - 1.5 + yb * 0.19, base_y - yb), (wx + 1.5 - yb * 0.19, base_y - yb)], iron, 0.4, 0.9)
    sh.ellipse(wx - 0.2, base_y - 7.6, 1.7, 1.7, iron)                          # the wheel, nearly face on: a ring of blades
    sh.ellipse(wx - 0.2, base_y - 7.6, 0.9, 0.9, mix("#9aa4b8", AIR, HZ_))
    sh.ellipse(wx - 0.2, base_y - 7.6, 0.35, 0.35, iron)
    sh.line([(wx + 0.4, base_y - 7.5), (wx + 2.6, base_y - 7.9)], iron, 0.45)   # its tail, and the vane
    sh.poly([(wx + 2.2, base_y - 8.9), (wx + 3.5, base_y - 8.7), (wx + 3.5, base_y - 7.2), (wx + 2.2, base_y - 7.2)], mix("#d8d4cc", AIR, HZ_))
    for k in range(8):                                                        # the corral's rails and posts
        px_ = R + 56 + k * 3.0
        sh.line([(px_, base_y), (px_, base_y - 1.1)], mix("#6a5a50", AIR, HZ_), 0.35)
    sh.line([(R + 56, base_y - 0.95), (R + 77, base_y - 0.95)], mix("#8a7868", AIR, HZ_), 0.3, 0.8)
    if not fast:
        pic = brush_wrapped(pic, sizes=(3, 2), seed=seed + 6, density=1.3, jitter=0.02, keep=0.62, margin=100, blend=32)
    c, a = sh.done()                                                          # the made things and the brush, crisp, after
    lay_made(pic, alpha, c, a)
    return smoke(pic), cut(alpha, a)


def mid_right(fast=False, seed=391):
    w, H, ppm, dist = BANDS["mid-r"]
    x = periodic_x(w)
    air = rgb(AIR)
    bright = rgb("#f4e6d8")
    pic = np.empty((H, w, 3), F32)
    pic[...] = air
    alpha = np.zeros((H, w), F32)
    HZ_ = 0.26
    yy = np.arange(H, dtype=F32)[:, None]
    up = (H - 1 - yy)
    # low buttes and knolls, dark against the bright air, their sunward edges lit
    shapes = np.zeros(w, F32)
    caps = []
    BUTTES = ((380, 46, 17.0), (930, 26, 10.0), (1700, 62, 23.0))
    for c, half, ht, kind in tuple((c, h_, t, "mesa") for c, h_, t in BUTTES) + ((1250, 22, 5.0, "hill"), (2210, 28, 7.0, "hill"),
                                                                              (640, 14, 3.5, "hill"), (1480, 16, 4.0, "hill"), (2000, 12, 3.0, "hill")):
        if kind == "mesa":
            m = mesa(w, c, half, ht, cap=0.34, talus=0.52) + (pnoise((1, w), 6, seed + int(c), 2)[0] - 0.5) * 1.0 * (mesa(w, c, half, ht, 0.34, 0.52) > 2)
            caps.append((c, half * 0.34, ht))
        else:
            m = hill(w, c, half, ht, 0.85)
        shapes = np.maximum(shapes, m)
    shapes = np.maximum(shapes, 0)
    cov = coverage(shapes, H)
    sl = slope(blur(shapes[None, :], 0.8)[0])
    depth = np.maximum(shapes[None, :] - up, 0)
    face = pnoise((H, w), (2.2, 7), seed + 2, 3)                              # gullies down the cliffs
    lit = np.clip(0.30 + (face - 0.5) * 0.5 - sl * 0.25, 0, 1)
    talus = np.zeros(w, F32)
    for c, half, ht in BUTTES:
        talus = np.maximum(talus, (np.abs(dist_wrap(x, c, w)) < half) * ht * 0.52)
    low = (up < talus[None, :]) & (cov > 0)                                    # the talus: smoother, paler, hazier
    lit = np.where(low, 0.45 + (face - 0.5) * 0.15, lit)
    cap = (depth < 1.6) & (cov > 0)
    lit = np.where(cap, 0.18, lit)                                             # the caprock's dark lip under the rim
    col = ramp(lit, [(0.0, "#4c4682"), (0.35, "#625c94"), (0.6, "#7e74a4"), (1.0, "#a48aa4")])
    foot_air = np.clip(1 - up / np.maximum(shapes[None, :] * 0.6, 1.0), 0, 1)       # their feet lost in bright air
    col = lerp(col, lerp(air, bright, 0.5)[None, None, :], np.clip(HZ_ + foot_air * 0.35, 0, 1)[..., None])
    lay(pic, alpha, col, cov)
    sh = ground_rows(pic, alpha, w, H, lerp(rgb("#d0a07a"), lerp(air, bright, 0.5), HZ_ + 0.08), seed + 3, specks=1000, speck=mix("#4e4e5c", AIR, HZ_))
    if not fast:
        pic = brush_wrapped(pic, sizes=(3, 2), seed=seed + 6, density=1.3, jitter=0.02, keep=0.6, margin=100, blend=32)
    # rims of light on the crests and the caps' edges turned to the sun
    lines = Paper((H, w), ss=4)
    for xx in range(w):
        if shapes[xx] > 2.2 and -sl[xx] > -0.2:
            lines.line([(xx, H - shapes[xx] + 0.4), (xx + 1, H - shapes[xx] + 0.4 - sl[xx])], "#ffe6c4", 0.7, float(np.clip(0.4 - sl[xx] * 0.8, 0.25, 0.9)))
    for c, top, ht in caps:
        for xc in wrap(c, w, 80):
            lines.line([(xc + top - 0.5, H - ht + 0.5), (xc + top + 1.6, H - ht * 0.62)], "#f8d4b0", 0.8, 0.8)   # the sunward cliff
    # the far power line: wooden poles 12 m tall every 120 m, from x 1060 to 2380 (their wires, at 850 m, are
    # finer than a pixel: the engine's own wires are for the poles beside the road)
    pc = mix("#3e3a52", AIR, HZ_ * 0.6)
    for k in range(23):
        for xc in wrap(1060.5 + 60.0 * k, w, 70):                                  # (on a pixel's middle: a pole is one pixel wide)
            sh.line([(xc, H - 2.0), (xc, H - 8.0)], pc, 0.8)
            sh.line([(xc - 1.2, H - 7.5), (xc + 1.2, H - 7.5)], pc, 0.6)
    lc, la = lines.done()
    over(pic, lc, la * (alpha > 0.5))
    c, a = sh.done()
    lay_made(pic, alpha, c, a)
    return smoke(pic), cut(alpha, a)

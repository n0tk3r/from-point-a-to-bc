"""Ground, water and distance: the flat world a scene stands on, seen in perspective."""

import math

import numpy as np

from brush import F32, blur, grid, lerp, mask_ellipse, mask_line, mask_poly, noise, over, ramp, rgb, sample, smooth, step, tint, vary


def lay(shape, horizon):
    """Where each pixel below the horizon is on the ground. Returns (across, away, near): `near` runs from
    0 at the horizon to 1 at the bottom edge; `away` is distance (1 at the bottom edge, large far off);
    `across` is sideways position at that distance."""
    h, w = shape
    x, y = grid(shape)
    near = np.clip((y - horizon) / max(h - horizon, 1), 1e-3, 1.0)
    away = 1.0 / near
    across = (x - w / 2) * away
    return across.astype(F32), away.astype(F32), near.astype(F32)


def texture(shape, horizon, seed, cell=90.0, octaves=4, stretch=1.0):
    """Noise that lies on the ground: big blotches near the bottom of the picture, fine and flattened far away."""
    across, away, near = lay(shape, horizon)
    size = 1024
    tile = noise((size, size), cell, seed, octaves)
    u = (across * 0.9 + size * 4.5) % (size - 2)
    v = (away * 260.0 * stretch + size * 0.3) % (size - 2)
    t = sample(tile, u, v)
    fade = np.clip(near * 3.0, 0, 1)                                 # far away it would only glitter: calm it
    return lerp(np.full(shape, 0.5, dtype=F32), t, fade)


def sand(shape, horizon, seed, far, mid, near, patch=0.10, ripple=0.0):
    """A sweep of sand or dirt, from its far color at the horizon to its near color at the bottom edge."""
    across, away, t = lay(shape, horizon)
    color = ramp(t ** 0.75, [(0.0, far), (0.42, mid), (1.0, near)])
    blot = texture(shape, horizon, seed, 150.0, 4) - 0.5
    fine = texture(shape, horizon, seed + 1, 34.0, 3) - 0.5
    color *= (1 + blot[..., None] * 2 * patch + fine[..., None] * patch * 0.8)
    # warmer and cooler drifts, as when a wash is not quite mixed
    k = (noise(shape, (340, 120), seed + 2, 3) - 0.5) * 0.06
    color[..., 0] += k
    color[..., 2] -= k * 0.8
    if ripple:
        wave = np.sin(away * 55.0 + (texture(shape, horizon, seed + 3, 120.0, 3) - 0.5) * 22.0 + across * 0.004)
        color *= (1 + (wave * np.clip(t * 1.5, 0, 1) * ripple)[..., None])
    return np.clip(color, 0, 1).astype(F32)


def water(shape, horizon, seed, far, mid, near, streak=0.10, glint=0.5, glint_color="#f4ffff", sun_x=None):
    """Open water under a sky: pale by the horizon, deep below, drawn out in level streaks, with glints."""
    h, w = shape
    x, y = grid(shape)
    across, away, t = lay(shape, horizon)
    color = ramp(t ** 0.7, [(0.0, far), (0.3, mid), (1.0, near)])
    long = noise(shape, (300, 5), seed, 4) - 0.5
    short = noise(shape, (60, 3), seed + 1, 3) - 0.5
    rows = (long * 1.2 + short * 0.8) * np.clip(0.35 + t, 0, 1)
    color *= (1 + rows[..., None] * 2 * streak)
    # glints: short level dashes of light, thicker toward the sun's side
    spark = noise(shape, (26, 2.2), seed + 2, 2)
    where = step(0.80, 0.93, spark) * glint
    if sun_x is not None:
        where *= np.exp(-((x - sun_x) / (w * 0.22)) ** 2) * 1.6 + 0.25
    where *= np.clip(1.2 - t * 0.9, 0.2, 1)
    over(color, glint_color, np.clip(where, 0, 1).astype(F32))
    return np.clip(color, 0, 1).astype(F32)


def haze(picture, horizon, color, amount=0.5, depth=0.25, mask=None):
    """Air between us and far things: they pale toward the sky's color near the horizon line."""
    h, w = picture.shape[:2]
    x, y = grid((h, w))
    t = np.clip(np.abs(y - horizon) / (h * depth), 0, 1)
    m = (1 - t) ** 1.6 * amount
    if mask is not None:
        m = m * mask
    over(picture, color, m.astype(F32))
    return picture


def shadow(picture, mask, color="#5a4a78", amount=0.5, soft=2.0):
    """A cast shadow: the ground under the mask goes darker and cooler."""
    m = blur(mask, soft) * amount if soft else mask * amount
    tint(picture, color, np.clip(m, 0, 1))
    return picture


def pebbles(picture, horizon, seed, count, light, dark, zone=None, size=(1.0, 4.5)):
    """Small stones and their shadows, bigger near the bottom of the picture."""
    h, w = picture.shape[:2]
    rng = np.random.default_rng(seed)
    done = 0
    for _ in range(count * 6):
        if done >= count:
            break
        y = horizon + (h - horizon) * rng.random() ** 0.55
        x = rng.random() * w
        if zone is not None and zone[int(min(y, h - 1)), int(min(x, w - 1))] < 0.5:
            continue
        t = (y - horizon) / (h - horizon)
        r = lerp(size[0], size[1], t) * (0.5 + rng.random())
        m = mask_ellipse((h, w), x, y, r * 1.5, r * 0.75)
        sh = mask_ellipse((h, w), x + r * 0.9, y + r * 0.45, r * 1.5, r * 0.5)
        tint(picture, "#6a5a70", sh * 0.55)
        over(picture, lerp(rgb(dark), rgb(light), rng.random()), m)
        done += 1
    return picture


def ridge(shape, points, base, seed, rough=6.0):
    """A mask for everything under a skyline (hills, a far bank, an escarpment). The skyline runs through
    `points` and is made uneven by `rough` pixels."""
    h, w = shape
    x, y = grid(shape)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    line = np.interp(np.arange(w), xs, ys).astype(F32)
    line += (noise((1, w * 4), (90, 1), seed, 4)[0, :w] - 0.5) * 2 * rough
    line += (noise((1, w * 4), (14, 1), seed + 1, 2)[0, :w] - 0.5) * rough * 0.5
    m = np.clip(y - line[None, :] + 0.5, 0, 1) * np.clip(base - y + 0.5, 0, 1)
    return m.astype(F32), line


def dune(picture, crest, foot, shade="#8f7590", amount=0.5, lip="#fff0c4", ground=None, fall=1.25, lip_amount=0.45):
    """A dune's shaded side. `crest` is its ridge and `foot` the line where the shaded slope runs out onto the
    flat, both as points from left to right. The shade is crisp along the ridge and dies away toward the
    foot; just over the ridge the sunlit side has a pale lip."""
    h, w = picture.shape[:2]
    x, y = grid((h, w))
    xs = np.arange(w)
    cy = np.interp(xs, [p[0] for p in crest], [p[1] for p in crest])
    fy = np.interp(xs, [p[0] for p in foot], [p[1] for p in foot])
    x0, x1 = max(crest[0][0], foot[0][0]), min(crest[-1][0], foot[-1][0])
    span = np.clip((xs - x0) / 26.0, 0, 1) * np.clip((x1 - xs) / 26.0, 0, 1)            # both ends taper away
    v = (y - cy[None, :]) / np.maximum(fy - cy, 1.0)[None, :]
    a = np.where((v >= 0) & (v <= 1), (1 - np.clip(v, 0, 1)) ** fall, 0.0) * np.clip(y - cy[None, :] + 0.5, 0, 1) * span[None, :]
    band = np.clip(1 - np.abs(y - (cy[None, :] - 2.5)) / 3.0, 0, 1) * span[None, :]
    if ground is not None:
        a = a * ground
        band = band * ground
    tint(picture, shade, (a * amount).astype(F32))
    over(picture, lip, (band * lip_amount).astype(F32))
    return picture


def long_shadow(picture, foot, length, width, crown=None, color="#63527f", amount=0.42, ground=None, rise=0.04, seed=0):
    """The shadow of something tall and thin (a palm, a post) lying along the ground to the right of `foot`.
    `crown` is (radius across, radius up-and-down) of whatever is on top of it. The shadow is crisp at the
    foot and loose at the far end, and a crown of fronds throws a ragged one with holes in it."""
    shape = picture.shape[:2]
    end = (foot[0] + length, foot[1] - length * rise)
    m = mask_line(shape, [foot, end], [width, width * 0.6], soft=0.8)
    x, y = grid(shape)
    along = np.clip((x - foot[0]) / max(length, 1), 0, 1)
    m = lerp(m, blur(m, 2.5), along)
    if crown:
        c = mask_ellipse(shape, end[0] + crown[0] * 0.35, end[1], crown[0], crown[1], soft=2.0, wobble=crown[1] * 1.3, seed=seed)
        rays = noise(shape, (crown[0] * 0.35, max(2.0, crown[1] * 0.5)), seed + 3, 3)
        c = c * step(0.30, 0.56, rays + c * 0.25)
        m = np.maximum(m, blur(c, 1.2))
    if ground is not None:
        m = m * ground
    tint(picture, color, np.clip(m * amount, 0, 1).astype(F32))
    return picture


def rock(sheet, x, y, rx, ry, seed, tones=("#fff2cc", "#e4c898", "#a58c86", "#66545e"), light=-1):
    """A boulder sitting on the ground with the middle of its foot at (x, y): a dark shape first, then the
    planes that face the sun, then the brightest one, then a crack or two."""
    rng = np.random.default_rng(seed)
    n = 9
    pts = []
    for i in range(n):
        a = math.pi * 2 * i / n + rng.normal(0, 0.14)
        r = 0.80 + 0.28 * rng.random()
        pts.append((x + math.cos(a) * rx * r, min(y - ry + math.sin(a) * ry * r, y + ry * 0.04)))
    cx, cy = x, y - ry
    sheet.poly(pts, tones[2])
    low = [(px, py) for px, py in pts if py > cy]
    if len(low) >= 2:                                                           # the underside is darkest
        sheet.poly([(px, py) for px, py in pts if py > cy + ry * 0.2] + [(x + rx * 0.5, cy + ry * 0.45), (x - rx * 0.4, cy + ry * 0.6)], tones[3], 0.55)
    lit = [(cx + (px - cx) * 0.78 + light * rx * 0.17, cy + (py - cy) * 0.70 - ry * 0.20) for px, py in pts]
    sheet.poly(lit, tones[1])
    top = [(cx + (px - cx) * 0.50 + light * rx * 0.30, cy + (py - cy) * 0.40 - ry * 0.42) for px, py in pts]
    sheet.poly(top, tones[0])
    for _ in range(2):
        a = rng.random() * math.pi
        px, py = x + rng.normal(0, rx * 0.3), cy + rng.normal(0, ry * 0.25)
        l = min(rx, ry) * (0.4 + 0.5 * rng.random())
        sheet.line([(px, py), (px + math.cos(a) * l * 0.5, py + math.sin(a) * l * 0.5 + 1), (px + math.cos(a + 0.5) * l, py + math.sin(a + 0.5) * l)], tones[3], max(0.8, rx * 0.04), 0.6)
    return sheet


def rock_shadow(picture, x, y, rx, ry, color="#6a5884", amount=0.42, ground=None, reach=1.5):
    """The shadow a boulder throws to the right, along the ground."""
    m = mask_ellipse(picture.shape[:2], x + rx * reach * 0.62, y - ry * 0.10, rx * reach, max(1.5, ry * 0.42), soft=1.2)
    if ground is not None:
        m = m * ground
    tint(picture, color, (m * amount).astype(F32))
    return picture


def stones(sheet, picture, horizon, seed, count, zone=None, size=(0.8, 3.4), tones=("#f8e6ba", "#dcbc8a", "#a2846e", "#6c5560"), ground=None):
    """Many small stones, bigger toward the bottom of the picture, each with its shadow. They lie in
    drifts, not evenly."""
    h, w = picture.shape[:2]
    rng = np.random.default_rng(seed)
    drift = noise((h, w), 70, seed + 1, 3) > 0.52
    zone = drift if zone is None else (zone & drift)
    done = 0
    for _ in range(count * 8):
        if done >= count:
            break
        y = horizon + (h - horizon) * rng.random() ** 0.6
        x = rng.random() * w
        if zone is not None and not zone[int(min(y, h - 1)), int(min(x, w - 1))]:
            continue
        t = (y - horizon) / (h - horizon)
        r = lerp(size[0], size[1], t) * (0.5 + rng.random())
        rock_shadow(picture, x, y, r * 1.3, r * 0.8, ground=ground, amount=0.36)
        rock(sheet, x, y, r * 1.3, r * 0.8, seed + done * 7 + 1, tones)
        done += 1
    return sheet


def strata(sheet, line, x0, x1, seed, offsets=(5, 11, 18, 26), color="#9a7c8a", light="#fff0c8", alpha=0.6):
    """The beds of a cliff, drawn under its skyline (`line`, one height per pixel across): broken dark lines
    where one bed overhangs the next, a pale edge on top of each, and short gullies cutting down."""
    rng = np.random.default_rng(seed)
    for k, off in enumerate(offsets):
        x = x0 + rng.random() * 20
        while x < x1:
            run = 14 + rng.random() * 46
            gap = 4 + rng.random() * 18
            xs = np.arange(int(x), int(min(x + run, x1)), 4)
            if len(xs) >= 2:
                wander = rng.normal(0, 0.5)
                pts = [(float(px), float(line[min(int(px), len(line) - 1)] + off + wander + math.sin(px * 0.11 + k) * 0.8)) for px in xs]
                sheet.line(pts, color, 1.0, alpha * (0.6 + 0.4 * rng.random()))
                sheet.line([(px, py - 1.2) for px, py in pts], light, 0.9, alpha * 0.55)
            x += run + gap
    gx = x0 + rng.random() * 30
    while gx < x1:                                              # gullies: dark wedges, wide at the top, no two alike
        top = line[min(int(gx), len(line) - 1)] + 1 + rng.random() * 5
        depth = 6 + rng.random() ** 2 * 26
        wide = 1.2 + rng.random() * 3.4
        sheet.poly([(gx - wide, top), (gx + wide, top + rng.normal(0, 1)), (gx + rng.normal(0, 2.5), top + depth)], color, alpha * (0.45 + 0.5 * rng.random()))
        gx += 9 + rng.random() ** 1.6 * 70
    return sheet


def crest(sheet, points, color="#fff2c8", under="#a07888", alpha=0.6):
    """Restate a dune's ridge as a crisp line: light on the sunny lip, dark just below it."""
    pts = [(float(a), float(b)) for a, b in points]
    sheet.line([(a, b + 1.6) for a, b in pts], under, 1.4, alpha * 0.55)
    sheet.line([(a, b - 0.4) for a, b in pts], color, 1.2, alpha)
    return sheet


def ripples(picture, horizon, seed, zone, color="#b8845c", amount=0.16, spacing=9.0):
    """Wind ripples in sand: fine level lines that wander and break, closer together far away."""
    shape = picture.shape[:2]
    across, away, near = lay(shape, horizon)
    wob = (texture(shape, horizon, seed, 160.0, 3) - 0.5) * 26.0
    wave = np.sin(away * (math.pi * 2 * 28.0 / spacing) + wob + across * 0.01)
    lines = step(0.72, 0.98, wave) * step(0.45, 0.7, noise(shape, (120, 30), seed + 1, 3))
    lines *= np.clip((near - 0.25) * 2.2, 0, 1)                # only where they are big enough to see
    tint(picture, color, (lines * zone * amount).astype(F32))
    return picture


def cast(picture, alpha, foot, sun=1.2, color="#63527f", amount=0.42, ground=None, toward=0.10, flat=0.30, soft=1.0, upright=True):
    """The true shadow of a cut-out: its own shape laid down on the ground to the right.

    `alpha` is the cut-out's mask at picture size and `foot` the place it stands. For something round and
    upright (a palm) the shape is turned on its side: its height runs away along the ground, `sun` times
    as long, and its width becomes the shadow's thickness, flattened by `flat`. For something long and low
    that we see from the side (a car) pass upright=False: every point simply slides right and toward us
    by its height. `toward` slants the shadow toward the bottom of the picture."""
    shape = picture.shape[:2]
    x, y = grid(shape)
    fx, fy = foot
    if upright:
        run = x - fx                                            # how far along the shadow we are
        h = run / sun
        dx = (y - fy - run * toward) / flat
        m = sample(alpha, fx + dx, fy - h) * (run > 0)
    else:
        h = (y - fy) / max(toward, 1e-3)
        m = sample(alpha, x - h * sun, fy - h) * (y >= fy) * (h < shape[0])
    m = blur(m.astype(F32), soft)
    if ground is not None:
        m = m * ground
    tint(picture, color, np.clip(m * amount, 0, 1).astype(F32))
    return m


def mound(shape, points, light=(-0.8, -0.6), soft=7.0, gain=1.0):
    """A heap of sand or earth as light and shade to multiply into the ground it lies on. `points`
    outline it. -> (multiplier picture, mask). At its edge the multiplier is 1, so the heap grows out
    of the ground without a seam."""
    blob = blur(mask_poly(shape, points), soft)
    gy, gx = np.gradient(blur(blob, 2.0))
    slope = -(gx * light[0] + gy * light[1])
    slope = slope / (np.abs(slope).max() + 1e-6)
    mult = 1 + np.where(slope > 0, slope * 0.30, slope * 0.42) * gain
    mult = mult + blob * 0.06 * gain                             # the top of it catches a little more sky
    return mult.astype(F32), (blob > 0.12).astype(F32)

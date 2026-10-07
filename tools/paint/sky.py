"""Skies: a soft field of blue (or dusk, or night) and clouds built up from billows, each with a lit
side and a shaded underside. No bands anywhere."""

import math

import numpy as np

from brush import F32, blur, grid, lerp, noise, over, ramp, rgb, sample, smooth, step


def field(shape, horizon, stops, seed, haze=None, patch=0.035):
    """The open sky. `stops` runs from the top of the picture (0) to the horizon (1). The color drifts a
    little from place to place, as washes do. `haze` is a color for the last stretch above the horizon."""
    h, w = shape
    x, y = grid(shape)
    drift = (noise(shape, (520, 260), seed, 3) - 0.5) * 0.16          # the wash is never even
    t = np.clip(y / max(horizon, 1) + drift, 0, 1)
    sky = ramp(t, stops)
    sky *= (1 + (noise(shape, (300, 120), seed + 1, 4) - 0.5)[..., None] * 2 * patch)
    if haze is not None:
        band = step(0.72, 1.0, y / max(horizon, 1)) * (0.75 + 0.5 * noise(shape, (400, 60), seed + 2, 3))
        over(sky, haze, np.clip(band * 0.8, 0, 1))
    return np.clip(sky, 0, 1).astype(F32)


def billows(shape, masses, seed, ragged=14.0):
    """Clouds as heaps of round billows. Each mass is (middle x, base y, width, height, how many billows).
    Returns (thickness 0-1, height map) at picture size. The height map is what gets lit."""
    h, w = shape
    rng = np.random.default_rng(seed)
    x, y = grid(shape)
    height = np.zeros(shape, dtype=F32)
    for (mx, base, width, tall, count) in masses:
        for _ in range(count):
            u = rng.normal(0, 0.34)                                # along the mass, bunched toward the middle
            u = max(-1.0, min(1.0, u))
            dome = math.sqrt(max(0.0, 1 - u * u))                   # tallest in the middle
            r = tall * (0.16 + 0.34 * rng.random()) * (0.45 + 0.75 * dome)
            cx = mx + u * width / 2
            cy = base - r * 0.55 - rng.random() ** 1.6 * tall * 0.78 * dome
            d2 = ((x - cx) / (r * 1.25)) ** 2 + ((y - cy) / r) ** 2
            cap = np.sqrt(np.clip(1 - d2, 0, 1)) * r
            height = np.maximum(height, cap + (base - cy) * 0.15 * (d2 < 1))
        # a long flat shelf under the heap, so the bottom reads as a base and not as more balls
        shelf = np.clip(1 - ((x - mx) / (width * 0.62)) ** 2, 0, 1) * np.clip(1 - np.abs(y - (base - tall * 0.06)) / (tall * 0.11), 0, 1)
        height = np.maximum(height, shelf * tall * 0.22)
    # ragged edges: push the whole thing about with noise, twice, coarse then fine
    dx = (noise(shape, 90, seed + 11, 4) - 0.5) * 2
    dy = (noise(shape, 90, seed + 12, 4) - 0.5) * 2
    height = sample(height, x + dx * ragged * 1.6, y + dy * ragged)
    fx = (noise(shape, 22, seed + 13, 3) - 0.5) * 2
    fy = (noise(shape, 22, seed + 14, 3) - 0.5) * 2
    height = sample(height, x + fx * ragged * 0.35, y + fy * ragged * 0.3)
    thick = smooth(height / (height.max() * 0.16 + 1e-6))
    return thick.astype(F32), height.astype(F32)


def lit(thick, height, light=(-0.6, -0.8), seed=0, reach=44.0, rise=0.55):
    """How bright each bit of cloud is, 0 (deep shade) to 1 (sunlit top).

    Each billow has a shoulder turned to the light and a side turned away; a billow that stands
    between another and the sun throws its shadow on it; and the hollows between billows are dim."""
    h, w = thick.shape
    x, y = grid((h, w))
    soft = blur(height, 2.5)
    shadow = np.zeros((h, w), dtype=F32)
    steps = 8
    for k in range(1, steps + 1):
        d = reach * k / steps
        ahead = sample(soft, x + light[0] * d, y + light[1] * d)
        shadow = np.maximum(shadow, np.clip((ahead - soft - d * rise) / 6.0, 0, 1))
    gy, gx = np.gradient(blur(height, 3.5))
    slope = (-gx * light[0] - gy * light[1])
    slope = np.clip(slope / (np.percentile(np.abs(slope), 96) + 1e-6), -1, 1)
    crease = np.clip((blur(height, 10) - height) / (height.max() * 0.10 + 1e-6), 0, 1)
    shade = 0.70 + 0.36 * slope - 0.42 * blur(shadow, 2.0) - 0.20 * crease
    shade += (noise((h, w), 60, seed + 21, 4) - 0.5) * 0.18
    return np.clip(shade, 0, 1).astype(F32)


def paint_clouds(picture, masses, seed, tones, light=(-0.6, -0.8), ragged=14.0, amount=1.0, reach=44.0, rise=0.55):
    """Paint cumulus onto a sky. `tones` are (shade, half tone, light, brightest) colors.
    The shade color should be close to the sky behind, so shaded sides melt into it."""
    shape = picture.shape[:2]
    thick, height = billows(shape, masses, seed, ragged)
    bright = lit(thick, height, light, seed, reach, rise)
    color = ramp(bright, [(0.0, tones[0]), (0.38, tones[1]), (0.72, tones[2]), (1.0, tones[3])])
    # edges: crisp where the light catches them, soft and thin where the cloud is in shade
    fray = 0.55 + 0.9 * noise(shape, 30, seed + 31, 4)
    body = smooth(blur(thick, 1.5) * fray)
    edge = lerp(blur(body, 5.0) * 0.9, body, np.clip(bright * 1.4, 0, 1)) * amount
    over(picture, color, np.clip(edge, 0, 1))
    return thick


def wisps(picture, horizon, seed, color, top=0.0, amount=0.5, cell=(360, 26)):
    """Thin streaks of high cloud and horizon haze: long, level, soft."""
    shape = picture.shape[:2]
    x, y = grid(shape)
    n = noise(shape, cell, seed, 5)
    band = step(top, 1.0, y / max(horizon, 1)) if top else np.ones(shape, dtype=F32)
    m = step(0.56, 0.86, n) * band * amount * (y < horizon)
    over(picture, color, blur(m.astype(F32), 1.2))
    return picture

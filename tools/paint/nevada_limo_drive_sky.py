"""The sky through the limousine's windows (nevada_limo_drive.py, DRIVE-16P): drive-sky.png, the stage's own size,
drawn still wherever a pane shows sky.

Each pixel of the stage is a direction out of the camera (its elevation above the horizon and its bearing from the
road ahead), and the sky is painted by direction: the panes show only the lowest few degrees of it (about 4.5 degrees
at the near panes' outer ends, 3 at the far panes), so the washes are spread a little to show the morning's blue at the
top of the glass and its warm haze at the horizon. The sun is up on the right, a little behind the car: the windows on
the right look toward its side of the sky (paler, warmer, a glow growing to the right, clouds lit from behind with
bright edges); those on the left look away from it (a deeper, cleaner blue, clouds lit full on, cream with violet
undersides). The clouds are a deck of long flat cloud 2.4 km up, painted on that plane and seen through the camera, so
they close up into thin streaks toward the horizon and run off toward the vanishing point, as everything else does."""

import math

import numpy as np

from brush import F32, blur, glow, grid, lerp, noise, over, ramp, rgb, sample, smooth, tint
from nevada_limo_drive_kit import FOCAL, H, HZ, SUN_EL, VX, W, smoke

SUN_AZ = 100.5          # degrees right of the road ahead: on the right, a little behind


def directions(shape=(H, W)):
    """For every pixel of the stage: (bearing from the road ahead, degrees, + right; elevation, degrees)."""
    x, y = grid(shape)
    dx = x + 0.5 - VX
    az = np.degrees(np.arctan2(dx, FOCAL))
    el = np.degrees(np.arctan2(HZ - (y + 0.5), np.hypot(dx, FOCAL)))
    return az.astype(F32), el.astype(F32)


def to_sun(az, el):
    """The angle (degrees) between each direction and the sun."""
    a, e = np.radians(az), np.radians(el)
    sa, se = math.radians(SUN_AZ), math.radians(SUN_EL)
    c = np.sin(e) * math.sin(se) + np.cos(e) * math.cos(se) * np.cos(a - sa)
    return np.degrees(np.arccos(np.clip(c, -1, 1))).astype(F32)


#   the clouds on the deck: (km ahead, km deep, km out from, to (- left, + right), how much). At 2.4 km up, a cloud
#   30 km ahead is 28 rows above the horizon and one 90 km ahead 9: the panes see the sky from about 43 rows above it
#   (the near panes' outer ends) to 20 (the far panes), so these are placed where the glass shows them.
CLOUDS = [
    (25.0, 5.5, -50.0, -14.0, 1.0), (36.0, 5.0, -24.0, -8.0, 0.85), (56.0, 12.0, -66.0, -16.0, 0.95), (96.0, 22.0, -100.0, -30.0, 0.8),
    (31.0, 5.5, 10.0, 42.0, 0.85), (49.0, 9.0, 22.0, 72.0, 0.95), (78.0, 16.0, 16.0, 66.0, 0.75),
]


def deck(shape, seed, height_km=2.4):
    """The cloud deck seen through the camera: for every pixel above the horizon, how much cloud (0 to 1), and how far
    off it is (km). Long flat clouds, stretched across the road, their edges broken."""
    h, w = shape
    x, y = grid(shape)
    up = np.maximum(HZ - (y + 0.5), 0.05)
    z = FOCAL * height_km / up                                    # km ahead where the ray meets the deck
    X = (x + 0.5 - VX) * z / FOCAL                                # km across (- left)
    tile_n = 1024
    span = 600.0                                                  # a noise tile laid on 600 km square of the deck
    rag = noise((tile_n, tile_n), (60, 14), seed, 5)
    fine = noise((tile_n, tile_n), (14, 5), seed + 1, 3)
    u = (X / span + 0.5) * (tile_n - 1)
    v = np.clip(z / span, 0, 1) * (tile_n - 1)
    n = sample(rag, u, v) * 0.7 + sample(fine, u, v) * 0.3
    d = np.zeros(shape, F32)
    for zc, dz, x0, x1, amt in CLOUDS:
        along = np.exp(-((z - zc) / dz) ** 2)
        ends = smooth((X - x0) / (0.18 * (x1 - x0))) * smooth((x1 - X) / (0.18 * (x1 - x0)))
        d = np.maximum(d, along * ends * amt * (0.5 + 0.8 * n))
    return np.clip(d, 0, 1).astype(F32), z.astype(F32)


def paint_sky(seed=61):
    shape = (H, W)
    az, el = directions(shape)
    x, y = grid(shape)
    # the washes by elevation (spread a little: the glass shows only the lowest few degrees)
    pic = ramp(np.clip(el, 0, 40), [(0.0, "#f4dcb6"), (0.3, "#e8dccc"), (0.8, "#c4d6e4"), (1.6, "#98c2e4"), (2.7, "#70a8de"),
                                    (4.0, "#5290d4"), (6.0, "#3e7ac8"), (10.0, "#3266b8"), (22.0, "#2a58aa"), (40.0, "#2452a4")])
    drift = (noise(shape, (300, 90), seed, 4) - 0.5)
    pic = pic * (1 + drift[..., None] * 0.07)
    # the sun's side: paler and warmer low down, a glow growing toward it; the other side a deeper, cooler blue
    th = to_sun(az, el)
    near = np.exp(-((th - 40.0) / 34.0) ** 2) * (th > 40) + (th <= 40)
    low = np.clip(1 - el / 7.0, 0, 1)
    glow(pic, "#ffdcae", (near * low * 0.55).astype(F32))
    over(pic, "#f4e6d2", (np.clip((95 - th) / 45.0, 0, 1) * low ** 2 * 0.35).astype(F32))
    away = np.clip((th - 105) / 40.0, 0, 1)
    tint(pic, "#8a9ad8", (away * np.clip(el / 5.0, 0, 1) * 0.22).astype(F32))
    # the haze along the horizon itself: warm and pale, thicker toward the sun
    band = np.exp(-(np.maximum(el, 0) / 0.55) ** 2) * (0.55 + 0.45 * noise(shape, (220, 6), seed + 2, 3))
    over(pic, "#f8e2c2", (band * (0.45 + 0.35 * near)).astype(F32))
    # the cloud deck
    d, dist = deck(shape, seed + 3)
    m = np.clip((d - 0.36) / 0.28, 0, 1)
    m = smooth(m) * (el > 0) * np.clip((el - 0.15) / 0.5, 0, 1)                 # melting into the haze at the horizon
    m = blur(m.astype(F32), 0.9)
    gy = np.gradient(blur(m, 1.2), axis=0)                                       # + where the cloud ends going down: its base
    top = np.clip(-gy * 6.0, 0, 1)                                               # the edge facing up, toward the light
    base = np.clip(gy * 6.0, 0, 1)
    right = np.clip((x - 400) / 140.0, 0, 1)                                     # the windows on the right look toward the sun
    # left: lit full on, cream and gold on top, violet underneath
    lit_l = lerp(lerp(rgb("#d8cce0")[None, None, :], rgb("#fbefdc")[None, None, :], np.clip(0.55 + top * 0.9 - base * 0.6, 0, 1)[..., None]),
                 rgb("#b4a6cc")[None, None, :], (base * 0.7)[..., None])
    # right: lit from behind: grey-violet bodies, bright silver-gold where the cloud is thin or its edge faces the sun
    thin = np.clip(1 - m * 1.6, 0, 1)
    lit_r = lerp(rgb("#a8a4c8")[None, None, :], rgb("#fff0d4")[None, None, :], np.clip(thin * 0.85 + top * 0.6, 0, 1)[..., None])
    col = lerp(lit_l, lit_r, right[..., None])
    over(pic, col, (m * 0.88).astype(F32))
    # below the horizon the stage is the ground's: carry the horizon's haze down, plain (never seen behind the ground)
    hz_row = int(HZ)
    below = (y >= hz_row + 1)
    edge = pic[hz_row:hz_row + 1]
    pic = np.where(below[..., None], np.broadcast_to(edge, pic.shape), pic)
    return smoke(np.clip(pic, 0, 1)), el

"""Steam from under the wagon's hood: four small frames that go round (0, 1, 2, 3, 0, ...).

The steam is a plume with a fixed outline (thin where it leaves the hood, wide and leaning with the wind
where it thins out) and, inside it, puffs that climb: after four frames each puff has climbed exactly to
where the one above it was, so the round has no jump in it. Soft edges: these are RGBA pictures, placed
by the middle of their bottom edge."""

import math

import numpy as np
from PIL import Image

from brush import *

W, H = 60, 104                                              # the size of a frame; its foot is (W / 2, H)
RISE = 26.0                                                 # how far a puff climbs in one round of four frames
LIGHT = (-0.78, -0.62)
PUFFS = [(-0.36, 0.14, 0.74, 0.33), (0.38, 0.44, 0.70, 0.30), (-0.12, 0.74, 0.78, 0.32), (0.44, 0.93, 0.52, 0.24)]    # in one stretch of the plume: across (-1..1), up (0..1), half-width, half-height


def frame(t, seed=3):
    """One frame, `t` of the way round (0 to 1). -> (color, alpha) as float pictures."""
    shape = (H, W)
    x, y = grid(shape)
    wx = (noise(shape, 11, seed, 3) - 0.5) * 5.0             # a fixed unevenness in the air, so no two puffs keep one shape
    wy = (noise(shape, 11, seed + 1, 3) - 0.5) * 5.0
    px, py = x + wx, y + wy
    up = np.clip((H - 3 - py) / (H - 3), 0, 1)               # 0 at the hood, 1 at the top of the frame
    middle = W / 2 - 4 + 15 * up ** 1.5 + 2.2 * np.sin(up * 7.0 + 0.6)      # the plume leans with the wind, and wanders
    half = 3.6 + 19.0 * up ** 0.85                          # and widens as it climbs
    u = (px - middle) / half
    v = (H - 3 - py) / RISE - t                              # the puffs climb through it
    d = np.zeros(shape, dtype=F32)
    for (cu, cv, ru, rv) in PUFFS:
        for whole in (-1, 0, 1):
            dv = (v - np.floor(v)) - cv + whole
            d = np.maximum(d, np.clip(1 - np.sqrt(((u - cu) / ru) ** 2 + (dv / rv) ** 2), 0, 1))
    core = np.clip(1 - np.abs(u) * 1.25, 0, 1) * 0.42        # a thin steady thread joins them
    d = np.maximum(smooth(d * 1.5), core)
    fade = step(0.0, 0.10, up) * (1 - up) ** 1.05            # it starts at the hood and thins out upward
    d = blur((d * fade).astype(F32), 1.1)
    gy, gx = np.gradient(blur(d, 1.6))
    lit = np.clip(0.5 + 9.0 * (-(gx * LIGHT[0] + gy * LIGHT[1])), 0, 1)       # the side toward the sun is warm white
    color = ramp(lit, [(0.0, "#cfc9d6"), (0.45, "#f0ebe4"), (1.0, "#fffaf0")])
    alpha = np.clip(d * 1.05, 0, 0.86)
    return grain(color, seed + 5, 0.012), alpha.astype(F32)


def frames(count=4):
    return [frame(i / count) for i in range(count)]


def save(folder, count=4):
    """Write steam-0.png ... as RGBA. -> [paths]"""
    out = []
    for i, (c, a) in enumerate(frames(count)):
        rgba = np.dstack([np.clip(c, 0, 1), a])
        path = f"{folder}/steam-{i}.png"
        Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), "RGBA").save(path, optimize=True)
        out.append(path)
    return out


if __name__ == "__main__":
    k = 4
    fs = frames()
    sheet = np.empty((H, W * 5 + 12, 3), dtype=F32)
    sheet[...] = rgb("#d39a58")
    sheet[:, W * 2 + 6:] = rgb("#7a4a36")                    # (and against something dark, to see the edges)
    for i, (c, a) in enumerate(fs + fs[:1]):
        x0 = i * W + (6 if i >= 2 else 0) + (6 if i >= 4 else 0)
        over(sheet[:, x0:x0 + W], c, a)
    Image.fromarray((np.clip(sheet, 0, 1) * 255).astype(np.uint8)).resize((sheet.shape[1] * k, H * k), Image.NEAREST).save("out/egypt1-look/steam-try.png")
    print("ok")

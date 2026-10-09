"""Round four: the kites over the building site, as frames for the game to fly (they were painted still in the sky).

    python3 egypt_site_kite.py      writes out/egypt-site/kite-0.png .. kite-3.png and out/egypt-site-kites.png (a look, 8x)

A black kite high up is only a few pixels: the painting gave each one as a single dark stroke, a shallow W, the wings
bowed and the right one a little higher (it is turning). The frames keep that stroke and that colour (#3a3a4e at
0.8, as painted) and move the wings:
    kite-0  gliding (the stroke as painted)        kite-1  wings up        kite-2  wings down        kite-3  banking
Each frame is 13 x 8 px, transparent; the bird's middle (where the painted stroke dipped, under the body) is at
[6.5, 5.0] of the frame. They are drawn for the nearest kite (4.5 px from the middle to a wing tip); for the others
the game may draw them a little smaller (the painting had 4.2, 3.2 and 2.6)."""

import os

import numpy as np
from PIL import Image

from brush import Sheet

OUT = "out/egypt-site"
SIZE = (13, 8)                    # w, h
MIDDLE = (6.5, 5.0)
R = 4.5
COLOR, ALPHA = "#3a3a4e", 0.8
# the stroke through five points, as (x, y) in units of R from the middle (y down), for each frame
KITE_FRAMES = [
    [(-1.0, -0.35), (-0.3, -0.10), (0.0, 0.25), (0.35, -0.15), (1.0, -0.50)],     # gliding: as painted
    [(-1.0, -0.95), (-0.32, -0.32), (0.0, 0.22), (0.34, -0.36), (0.98, -1.00)],   # wings up
    [(-0.96, 0.32), (-0.34, -0.02), (0.0, 0.25), (0.36, -0.04), (0.97, 0.22)],    # wings down
    [(-0.86, 0.12), (-0.28, -0.02), (0.0, 0.25), (0.36, -0.30), (1.04, -0.80)],   # banking
]


def frame(points):
    w, h = SIZE
    s = Sheet((h, w), ss=6)
    s.line([(MIDDLE[0] + x * R, MIDDLE[1] + y * R) for x, y in points], COLOR, 1.0, ALPHA)
    c, a = s.done()
    rgba = np.concatenate([c, a[..., None]], axis=2)
    return Image.fromarray((np.clip(rgba, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    k = 8
    look = Image.new("RGBA", (len(KITE_FRAMES) * (SIZE[0] * k + 8), SIZE[1] * k), (150, 186, 228, 255))
    for i, pts in enumerate(KITE_FRAMES):
        im = frame(pts)
        im.save(f"{OUT}/kite-{i}.png", optimize=True)
        look.alpha_composite(im.resize((SIZE[0] * k, SIZE[1] * k), Image.NEAREST), (i * (SIZE[0] * k + 8), 0))
    look.convert("RGB").save("out/egypt-site-kites.png")
    print("kites", [os.path.getsize(f"{OUT}/kite-{i}.png") for i in range(len(KITE_FRAMES))])

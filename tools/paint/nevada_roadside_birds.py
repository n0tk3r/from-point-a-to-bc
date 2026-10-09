"""Round four: the two big birds over the desert, as frames for the game to fly (they were painted still in the sky).

    python3 nevada_roadside_birds.py      writes out/nevada-roadside/bird-0.png .. bird-3.png and out/nevada-roadside-birds.png (a look, 8x)

High up, a raven or a hawk is only a dark stroke: the painting gave each one as a shallow W in #2e3a5c at 0.85, the
right wing a little higher and longer (it is turning). The frames keep that stroke and that colour and move the wings:
    bird-0  gliding (the stroke as painted)        bird-1  wings up        bird-2  wings down        bird-3  banking
Each frame is 15 x 9 px, transparent; the bird's middle (where the painted stroke dipped, under the body) is at
[7.0, 5.5] of the frame. They are drawn for the nearer bird (5 px from the middle to the left wing tip); the farther
one was 3.6: the game may draw it at 0.7."""

import os

import numpy as np
from PIL import Image

from brush import Sheet

OUT = "out/nevada-roadside"
SIZE = (15, 9)                    # w, h
MIDDLE = (7.0, 5.5)
R = 5.0
COLOR, ALPHA, WIDTH = "#2e3a5c", 0.85, 0.9
# the stroke through five points, as (x, y) in units of R from the middle (y down), for each frame
BIRD_FRAMES = [
    [(-1.0, -0.35), (-0.3, -0.05), (0.0, 0.25), (0.4, -0.15), (1.1, -0.50)],      # gliding: as painted
    [(-0.98, -0.92), (-0.32, -0.30), (0.0, 0.22), (0.38, -0.34), (1.04, -1.02)],  # wings up
    [(-0.96, 0.36), (-0.34, 0.0), (0.0, 0.25), (0.40, -0.02), (1.05, 0.28)],      # wings down
    [(-0.84, 0.16), (-0.28, 0.0), (0.0, 0.25), (0.40, -0.30), (1.12, -0.82)],     # banking
]


def frame(points):
    w, h = SIZE
    s = Sheet((h, w), ss=6)
    s.line([(MIDDLE[0] + x * R, MIDDLE[1] + y * R) for x, y in points], COLOR, WIDTH, ALPHA)
    c, a = s.done()
    rgba = np.concatenate([c, a[..., None]], axis=2)
    return Image.fromarray((np.clip(rgba, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    k = 8
    look = Image.new("RGBA", (len(BIRD_FRAMES) * (SIZE[0] * k + 8), SIZE[1] * k), (96, 150, 214, 255))
    for i, pts in enumerate(BIRD_FRAMES):
        im = frame(pts)
        im.save(f"{OUT}/bird-{i}.png", optimize=True)
        look.alpha_composite(im.resize((SIZE[0] * k, SIZE[1] * k), Image.NEAREST), (i * (SIZE[0] * k + 8), 0))
    look.convert("RGB").save("out/nevada-roadside-birds.png")
    print("birds", [os.path.getsize(f"{OUT}/bird-{i}.png") for i in range(len(BIRD_FRAMES))])

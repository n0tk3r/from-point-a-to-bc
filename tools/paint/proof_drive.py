#!/usr/bin/env python3
"""DRIVE-16E: the proof's pictures for the engine's `drive` (the world going by a car's side windows), plain shapes and
plain colours, so that the geometry can be checked by eye and by test (docs/DESIGN.md, section 2, "The world going by a
car's side windows").

    python3 proof_drive.py          (in tools/paint) writes art/proof/drive/: the engine's own proof pictures, drawn as
                                    they are (never keyed)

The proof's camera (js/content/scenes/engine-proof.js, DRIVE_CAM): the vanishing point (400, 226), the focal length 320
pixels, the eye 1.6 m above the road; one window each side of the vanishing point, its top and bottom edges running to it
(PANES below, the same numbers as the scene's). What it writes:

  car.png          the car's side seen from the back seat, 800 x 600: a grey band across the picture with the two windows
                   cut clear (a pixel is clear where its middle is in the pane, as the engine's mask has it), a dark frame
                   round each, and a small light cross on the vanishing point
  sky.png          the sky, 800 x 600: blue at the top, pale at the horizon, a few plain clouds (drawn still)
  ground-l.png,    the ground beside the road from straight above, 1024 x 512 at 16 pixels a metre: columns along the road
  ground-r.png     (64 m, looping end to end), rows outward from 4 m (to 36 m). Squares two metres a side (sand on the left,
                   olive on the right), a band across the road every 16 m (a colour of its own each: a loop shows all four),
                   and stripes along the road 6 m (white), 10 m (red), 16 m (blue) and 24 m (yellow) out, which run to the
                   vanishing point on the stage. Its last rows plain, for the ground beyond it
  far-l.png,       the far ranges, 1200 x 48 at 0.1 pixels a metre (3 km out in the scene): plain pale triangles, clear above,
  far-r.png        the bottom two rows solid (the ground at their foot); a different set each side
  mid-l.png,       the middle distance, 1000 x 40 at 0.5 pixels a metre (400 m out): darker triangles and a flat-topped butte
  mid-r.png        or two
  things.png,      the upright things, painted from the side at 24 pixels a metre, each in its box, its foot the middle of the
  things.json      box's bottom edge: a red post (1.2 m), a brown pole with a crossarm (8 m), a magenta marker (0.5 x 2 m: the
                   test reads it back), a green bush, an orange cone, a yellow board on a post
"""

import json, os
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "art", "proof", "drive")
VANISH, FOCAL, EYE = (400.0, 226.0), 320.0, 1.6
PANES = {"L": [(40, 120), (300, 196.56), (300, 254.89), (40, 330)], "R": [(760, 120), (500, 196.56), (500, 254.89), (760, 330)]}
GW, GH, PPM, FROM = 1024, 512, 16, 4.0
STRIPES = [(6.0, 0.25, (250, 250, 250)), (10.0, 0.4, (210, 40, 40)), (16.0, 0.4, (40, 70, 210)), (24.0, 0.5, (240, 210, 40))]
BANDS = [(0, (226, 70, 60)), (16, (60, 160, 230)), (32, (250, 250, 250)), (48, (40, 40, 40))]      # metres along: the bands across the road, their colours


def inside(poly, xs, ys):
    """Is each point (pixel middles) in the polygon? The engine's rule (effects.js `inside`), for whole arrays."""
    hit = np.zeros(xs.shape, bool)
    n = len(poly)
    for i in range(n):
        (xi, yi), (xj, yj) = poly[i], poly[i - 1]
        cross = ((yi > ys) != (yj > ys)) & (xs < (xj - xi) * (ys - yi) / ((yj - yi) or 1e-12) + xi)
        hit ^= cross
    return hit


def car():
    """The car's side from the back seat: a grey band, the two windows cut clear, dark frames, a cross on the vanishing point."""
    ys, xs = np.mgrid[0:600, 0:800].astype(float) + 0.5
    pic = np.zeros((600, 800, 4), np.uint8)
    band = (ys >= 88) & (ys < 356)
    pic[band] = (104, 108, 118, 255)
    pic[(ys >= 88) & (ys < 94)] = (72, 75, 84, 255)                  # the roof's edge
    pic[(ys >= 348) & (ys < 356)] = (72, 75, 84, 255)                # the sill
    for poly in PANES.values():
        hole = inside(poly, xs, ys)
        near = np.zeros_like(hole)
        for dy in range(-6, 7):
            for dx in range(-6, 7):
                if dx * dx + dy * dy <= 36: near |= np.roll(np.roll(hole, dy, 0), dx, 1)
        pic[near & ~hole] = (40, 42, 48, 255)                        # the frame
        pic[hole] = (0, 0, 0, 0)
    vx, vy = int(VANISH[0]), int(VANISH[1])
    pic[vy, vx - 6:vx + 7] = (226, 226, 226, 255); pic[vy - 6:vy + 7, vx] = (226, 226, 226, 255)
    return Image.fromarray(pic, "RGBA")


def sky():
    y = np.arange(600, dtype=float)[:, None]
    t = np.clip(y / VANISH[1], 0, 1)
    top, low = np.array([46, 96, 186.0]), np.array([214, 228, 240.0])
    col = top + (low - top) * (t ** 1.4)[..., None]
    pic = np.concatenate([np.broadcast_to(col, (600, 800, 3)), np.full((600, 800, 1), 255.0)], 2).astype(np.uint8)
    im = Image.fromarray(pic, "RGBA")
    d = ImageDraw.Draw(im)
    for (cx, cy, rx, ry) in [(120, 150, 60, 10), (210, 170, 40, 7), (560, 140, 70, 11), (690, 185, 45, 8), (380, 120, 50, 9)]:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(246, 248, 252, 255))
    return im


def ground(tones):
    """Squares two metres a side, bands across the road every 16 m, stripes along it: rows outward from FROM metres."""
    b = np.arange(GH)[:, None]; a = np.arange(GW)[None, :]
    X = FROM + (b + 0.5) / PPM                                       # metres out, each row
    sq = ((a // 32) + (b // 32)) % 2
    pic = np.where(sq[..., None] == 0, np.array(tones[0]), np.array(tones[1])).astype(np.uint8)
    pic = np.broadcast_to(pic, (GH, GW, 3)).copy()
    for (m, col) in BANDS:                                           # across the road: half a metre wide
        pic[:, int(m * PPM):int(m * PPM) + 8] = col
    for (x, width, col) in STRIPES:                                  # along the road
        rows = (X[:, 0] >= x) & (X[:, 0] < x + width)
        pic[rows, :] = col
    pic[GH - 16:, :] = tones[2]                                      # its last metre plain: the ground beyond it
    return Image.fromarray(np.concatenate([pic, np.full((GH, GW, 1), 255, np.uint8)], 2), "RGBA")


def band(w, h, seed, col, foot, n, tall, flat=0):
    """Plain triangles (and flat-topped ones), clear above, the bottom two rows solid: looping end to end."""
    rng = np.random.default_rng(seed)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(n):
        x = rng.uniform(0, w); half = rng.uniform(tall[0], tall[1]) * rng.uniform(1.2, 2.6); top = h - 2 - rng.uniform(*tall)
        shade = tuple(int(c * rng.uniform(0.86, 1.06)) for c in col) + (255,)
        for dx in (-w, 0, w):                                        # (drawn at x and a width either side: it loops)
            if i < flat:
                d.polygon([(x + dx - half, h - 1), (x + dx - half * 0.55, top), (x + dx + half * 0.55, top), (x + dx + half, h - 1)], fill=shade)
            else:
                d.polygon([(x + dx - half, h - 1), (x + dx, top), (x + dx + half, h - 1)], fill=shade)
    d.rectangle([0, h - 2, w, h - 1], fill=foot + (255,))
    return im


def things():
    """The upright things: (name, width, height in metres, how it is drawn) at 24 pixels a metre, side by side on a sheet."""
    P = 24
    kinds = [("post", 0.16, 1.2), ("pole", 1.7, 8.0), ("marker", 0.5, 2.0), ("bush", 1.0, 0.8), ("cone", 0.6, 0.9), ("board", 1.3, 2.3)]
    boxes, x = {}, 2
    for name, wm, hm in kinds:
        w, h = int(round(wm * P)), int(round(hm * P))
        boxes[name] = [x, 2, w, h]
        x += w + 4
    sheet = Image.new("RGBA", (x + 2, max(b[3] for b in boxes.values()) + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(sheet)
    for name, (bx, by, w, h) in boxes.items():
        if name == "post":
            d.rectangle([bx, by, bx + w - 1, by + h - 1], fill=(206, 44, 40, 255))
        elif name == "pole":
            mid = bx + w // 2
            d.rectangle([mid - 3, by, mid + 3, by + h - 1], fill=(112, 76, 44, 255))
            d.rectangle([bx, by + 10, bx + w - 1, by + 14], fill=(90, 60, 34, 255))          # the crossarm, 7.4 m up
            for ix in (bx + 2, bx + w - 4):
                d.rectangle([ix, by + 6, ix + 2, by + 9], fill=(170, 210, 220, 255))      # its insulators, a little higher
        elif name == "marker":
            d.rectangle([bx, by, bx + w - 1, by + h - 1], fill=(255, 0, 255, 255))
        elif name == "bush":
            d.ellipse([bx, by, bx + w - 1, by + h - 1 + 6], fill=(58, 128, 52, 255))
            d.rectangle([bx, by + h, bx + w, by + h + 8], fill=(0, 0, 0, 0))
        elif name == "cone":
            d.polygon([(bx, by + h - 1), (bx + w / 2, by), (bx + w - 1, by + h - 1)], fill=(240, 130, 30, 255))
        elif name == "board":
            mid = bx + w // 2
            d.rectangle([mid - 1, by + 18, mid + 1, by + h - 1], fill=(120, 120, 126, 255))
            d.rectangle([bx, by, bx + w - 1, by + 19], fill=(244, 206, 40, 255))
            d.rectangle([bx + 3, by + 3, bx + w - 4, by + 16], outline=(30, 30, 30, 255))
    sprites = {name: {"box": b, "foot": [b[2] / 2, b[3]], "height": dict((k[0], k[2]) for k in kinds)[name]} for name, b in boxes.items()}
    return sheet, {"ppm": P, "note": "DRIVE-16E: the proof's upright things, painted from the side at 24 pixels a metre; foot: in the box", "sprites": sprites}


def main():
    os.makedirs(OUT, exist_ok=True)
    car().save(os.path.join(OUT, "car.png"))
    sky().save(os.path.join(OUT, "sky.png"))
    ground([(222, 196, 150), (196, 166, 118), (206, 180, 136)]).save(os.path.join(OUT, "ground-l.png"))
    ground([(150, 170, 104), (122, 142, 84), (136, 156, 94)]).save(os.path.join(OUT, "ground-r.png"))
    band(1200, 48, 11, (150, 170, 206), (176, 190, 214), 26, (14, 46)).save(os.path.join(OUT, "far-l.png"))
    band(1200, 48, 12, (176, 150, 196), (196, 184, 210), 26, (14, 46)).save(os.path.join(OUT, "far-r.png"))
    band(1000, 40, 21, (92, 118, 84), (122, 140, 104), 30, (8, 38), flat=4).save(os.path.join(OUT, "mid-l.png"))
    band(1000, 40, 22, (132, 104, 72), (150, 130, 100), 30, (8, 38), flat=4).save(os.path.join(OUT, "mid-r.png"))
    sheet, meta = things()
    sheet.save(os.path.join(OUT, "things.png"))
    with open(os.path.join(OUT, "things.json"), "w") as f: json.dump(meta, f, indent=1)
    print("wrote", OUT)


if __name__ == "__main__":
    main()

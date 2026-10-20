#!/usr/bin/env python3
"""ROAD-18E: the proof's pictures for the engine's `drive` seen straight ahead (side: "ahead": the whole stage, both sides
of the road and the road between), plain shapes and plain colours, so that the geometry can be checked by eye and by test
(docs/DESIGN.md, section 2, "The world going by a car's side windows", and its "Straight ahead").

    python3 proof_road.py           (in tools/paint) writes art/proof/road/: the engine's own proof pictures, drawn as
                                    they are (never keyed)

The proof's camera is the highway's (tools/paint/highway.py, CAM: level, the horizon on row 330, the vanishing point
(400, 330), the focal length 800 pixels, the eye 2.70 m above the road). What it writes:

  sky.png          800 x 600, opaque: a plain sky over the proof's stage (deep violet at the top to pale gold at the
                   horizon, a few flat clouds), and below the horizon a plain far plain (the drive draws the ground over it
                   as far off as `far` says)
  road.png         the road from straight above at 32 pixels a metre: rows across the road from 6 m left (its top row) to
                   6 m right (its bottom row), 384 of them; columns along it, 48 m looping end to end (1536). Asphalt in
                   squares a metre a side (two greys), a yellow centre line in dashes 3 m long every 12 m, white edge lines
                   from 2.95 to 3.10 m out each side, shoulders of sand in squares two metres a side to 6 m, a red band
                   across the shoulders every 12 m (so the motion shows); its outermost rows plain
  desert-l.png,    the desert either side from straight above at 16 pixels a metre: 24 m across (384 rows; the left's top
  desert-r.png     row 30 m out, its bottom row 6 m out, by the road; the right's top row 6 m out), 48 m along (768 columns,
                   looping). Squares two metres a side (sand on the left, olive on the right), stripes along the road 10 m
                   (red) and 20 m (blue) out, which run to the vanishing point on the stage, a band across every 16 m; the
                   outermost metre plain (the ground beyond it)
  things.png,      the upright things on a sheet at 48 pixels a metre, each in its box, its foot the middle of its bottom
  things.json      edge: a brown telephone pole 8.5 m tall with two crossarms and glass insulators; a white reflector post
                   (1.1 m) with a red top; two green bushes; a grey stone; a magenta marker (0.5 x 2 m: the test reads it
                   back); and the sign at 800 / 17.3 = 46.24 pixels a metre, as the painting's is (so that 17.3 m ahead it
                   is drawn at its own size, pixel for pixel): `sign` (a green board 4.30 to 7.60 m across and 1.70 to
                   3.62 m up, a white rim and a white B, on two grey posts at 4.86 and 7.06 m; its foot between them, at
                   5.95 m) and `sign-bc` (the same board saying B.C., with an orange rim)
  car.png          the proof's own car seen from behind (a box of a car: a dark red body, its back window, two tail lights,
                   a bumper, the wheels under it), at its size in the lane at row 548 (9.91 m ahead: 80.7 pixels a metre),
                   for a cut-out standing still in the lane while the road goes by under it
"""

import json, os
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "art", "proof", "road")
HZ, VX, FOCAL, EYE = 330.0, 400.0, 800.0, 2.70
LOOP = 48.0                                                          # metres along the road, every ground picture


def rgba(pic):
    return Image.fromarray(np.concatenate([pic.astype(np.uint8), np.full(pic.shape[:2] + (1,), 255, np.uint8)], 2), "RGBA")


def sky():
    """A plain dusk sky, opaque, with flat clouds; a plain far plain below the horizon."""
    y = np.arange(600, dtype=float)[:, None]
    t = np.clip(y / HZ, 0, 1)
    top, low = np.array([52, 40, 104.0]), np.array([250, 214, 150.0])
    col = top + (low - top) * (t ** 1.6)[..., None]
    pic = np.broadcast_to(col, (600, 800, 3)).copy()
    pic[int(HZ):] = (214, 170, 140)                                  # the far plain (where the drive does not draw)
    im = rgba(pic)
    d = ImageDraw.Draw(im)
    for (cx, cy, rx, ry) in [(110, 120, 70, 9), (250, 200, 46, 6), (560, 110, 80, 10), (690, 230, 52, 7), (420, 160, 60, 8), (330, 270, 40, 5)]:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(255, 196, 170, 255))
    return im


def road():
    """The road from above: 32 px a metre, 384 rows from 6 m left (row 0) to 6 m right, 1536 columns (48 m) along."""
    P, H, W = 32, 384, int(LOOP * 32)
    b = np.arange(H)[:, None]; a = np.arange(W)[None, :]
    X = -6.0 + (b + 0.5) / P                                         # metres across, each row (negative: left)
    A = (a + 0.5) / P                                                # metres along, each column
    asphalt = np.where(((np.floor(A) + np.floor(X + 6)) % 2)[..., None] == 0, np.array([96, 96, 104]), np.array([74, 74, 84]))
    sand = np.where(((np.floor(A / 2) + np.floor((X + 6) / 2)) % 2)[..., None] == 0, np.array([200, 168, 128]), np.array([180, 148, 110]))
    side = np.abs(X)
    pic = np.where((side < 3.1)[..., None], asphalt, sand).astype(float)
    pic = np.broadcast_to(pic, (H, W, 3)).copy()
    edge = ((side >= 2.95) & (side < 3.10))[:, 0]
    pic[edge, :] = (240, 240, 236)                                   # the edge lines
    mid = (np.abs(X[:, 0]) < 0.06)
    dash = (A[0] % 12.0) < 3.0
    pic[np.ix_(mid, dash)] = (236, 196, 40)                          # the centre line: dashes 3 m long every 12 m
    bands = ((A[0] % 12.0) >= 6.0) & ((A[0] % 12.0) < 6.5)
    pic[np.ix_(side[:, 0] >= 3.3, bands)] = (204, 52, 44)            # a red band across the shoulders every 12 m
    pic[:8] = (190, 158, 118); pic[-8:] = (190, 158, 118)            # its outermost rows plain
    return rgba(pic)


def desert(left, tones):
    """The desert from above: 16 px a metre, 384 rows (24 m across), 768 columns (48 m) along."""
    P, H, W = 16, 384, int(LOOP * 16)
    b = np.arange(H)[:, None]; a = np.arange(W)[None, :]
    out = (30.0 - (b + 0.5) / P) if left else (6.0 + (b + 0.5) / P)  # metres out from the middle of the road, each row
    A = (a + 0.5) / P
    sq = ((np.floor(A / 2) + np.floor(out / 2)) % 2)
    pic = np.where(sq[..., None] == 0, np.array(tones[0]), np.array(tones[1])).astype(float)
    pic = np.broadcast_to(pic, (H, W, 3)).copy()
    pic[:, ((A[0] % 16.0) < 0.5)] = (60, 60, 60)                     # a band across every 16 m
    for (x, width, col) in [(10.0, 0.4, (210, 40, 40)), (20.0, 0.4, (40, 70, 210))]:
        rows = (out[:, 0] >= x) & (out[:, 0] < x + width)
        pic[rows, :] = col
    far = out[:, 0] >= 29.0
    pic[far, :] = tones[2]                                           # its outermost metre plain: the ground beyond it
    return rgba(pic)


GLYPHS = {   # 5 x 7, for the sign's letters
    "B": ["1111.", "1...1", "1...1", "1111.", "1...1", "1...1", "1111."],
    "C": [".111.", "1...1", "1....", "1....", "1....", "1...1", ".111."],
    ".": [".....", ".....", ".....", ".....", ".....", ".11..", ".11.."],
    "4": ["...1.", "..11.", ".1.1.", "1..1.", "11111", "...1.", "...1."],
    "0": [".111.", "1...1", "1..11", "1.1.1", "11..1", "1...1", ".111."],
}


def letters(d, text, x, y, k, fill):
    for ch in text:
        for r, line in enumerate(GLYPHS[ch]):
            for c, v in enumerate(line):
                if v == "1": d.rectangle([x + c * k, y + r * k, x + c * k + k - 1, y + r * k + k - 1], fill=fill)
        x += 6 * k


def things():
    """The upright things: each drawn in its own box on a sheet (48 px a metre; the signs 46.24), foot the middle of its bottom edge."""
    P, PS = 48, 800 / 17.3
    sign_w, sign_h = int(round(3.30 * PS)), int(round(3.62 * PS))
    kinds = [("pole", 2.0 * P, 8.5 * P), ("post", 0.1 * P, 1.1 * P), ("bush", 0.9 * P, 0.7 * P), ("bush-2", 1.3 * P, 0.95 * P),
             ("stone", 0.5 * P, 0.3 * P), ("marker", 0.5 * P, 2.0 * P), ("sign", sign_w, sign_h), ("sign-bc", sign_w, sign_h)]
    boxes, x = {}, 2
    for name, w, h in kinds:
        boxes[name] = [x, 2, int(round(w)), int(round(h))]
        x += int(round(w)) + 6
    sheet = Image.new("RGBA", (x + 2, max(b[3] for b in boxes.values()) + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(sheet)
    sprites = {}
    for name, (bx, by, w, h) in boxes.items():
        foot = [w / 2, h]
        if name == "pole":
            mid = bx + w // 2
            d.rectangle([mid - 6, by + 4, mid + 6, by + h - 1], fill=(112, 76, 44, 255))                      # 25 cm thick
            for arm in (8.1, 7.6):                                                                          # two crossarms, their wires' heights
                ay = by + h - int(round(arm * P))
                d.rectangle([bx, ay, bx + w - 1, ay + 5], fill=(88, 58, 32, 255))
                for ix in (bx + 2, bx + w // 4, bx + 3 * w // 4, bx + w - 8):
                    d.rectangle([ix, ay - 8, ix + 5, ay - 1], fill=(150, 214, 220, 255))                    # glass insulators
        elif name == "post":
            d.rectangle([bx, by, bx + w - 1, by + h - 1], fill=(236, 236, 230, 255))
            d.rectangle([bx, by + 4, bx + w - 1, by + 12], fill=(220, 40, 30, 255))
        elif name == "bush":
            d.ellipse([bx, by, bx + w - 1, by + h + 10], fill=(58, 128, 52, 255))
            d.rectangle([bx, by + h, bx + w, by + h + 12], fill=(0, 0, 0, 0))
        elif name == "bush-2":
            d.ellipse([bx, by, bx + w - 1, by + h + 14], fill=(36, 92, 62, 255))
            d.rectangle([bx, by + h, bx + w, by + h + 16], fill=(0, 0, 0, 0))
        elif name == "stone":
            d.ellipse([bx, by, bx + w - 1, by + 2 * h], fill=(130, 126, 120, 255))
            d.rectangle([bx, by + h, bx + w, by + 2 * h + 1], fill=(0, 0, 0, 0))
        elif name == "marker":
            d.rectangle([bx, by, bx + w - 1, by + h - 1], fill=(255, 0, 255, 255))
        else:                                                                                               # the signs
            at = lambda m: bx + int(round((m - 4.30) * PS))                                                  # metres across -> the sheet
            up = lambda m: by + int(round((3.62 - m) * PS))                                                  # metres up -> the sheet
            for post in (4.86, 7.06):
                d.rectangle([at(post) - 2, up(1.70), at(post) + 1, by + h - 1], fill=(120, 124, 130, 255))
            rim = (250, 250, 246, 255) if name == "sign" else (250, 150, 40, 255)
            d.rectangle([bx, by, bx + w - 1, up(1.70)], fill=(30, 128, 72, 255))
            d.rectangle([bx + 4, by + 4, bx + w - 5, up(1.70) - 4], outline=rim, width=3)
            if name == "sign":
                letters(d, "B", bx + 18, by + 18, 7, (250, 250, 246, 255)); letters(d, "40", bx + 78, by + 38, 5, (250, 250, 246, 255))
            else:
                letters(d, "B.C.", bx + 14, by + 22, 6, (250, 250, 246, 255))
            foot = [(5.95 - 4.30) * PS, h]
        sprites[name] = {"box": [bx, by, w, h], "foot": [round(foot[0], 3), foot[1]], "height": round(h / (PS if name.startswith("sign") else P), 3)}
        if name.startswith("sign"):
            sprites[name]["ppm"] = round(PS, 4)
            sprites[name]["air"] = 0                                                                         # (in its own air at 17.3 m, as the painting's sign is)
    return sheet, {"ppm": P, "note": "ROAD-18E: the proof's upright things, seen from behind at 48 pixels a metre (the signs at 800 / 17.3); foot: in the box", "sprites": sprites}


def car():
    """The proof's car from behind, at its size 9.91 m ahead (row 548): 80.7 pixels a metre."""
    k = FOCAL / (FOCAL * EYE / (548 - HZ))
    w, h = int(round(1.8 * k)), int(round(1.5 * k))
    im = Image.new("RGBA", (w + 2, h + 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([4, h - 10, 22, h], fill=(20, 20, 22, 255)); d.rectangle([w - 22, h - 10, w - 4, h], fill=(20, 20, 22, 255))      # wheels
    d.rectangle([0, int(h * 0.45), w, h - 8], fill=(150, 34, 38, 255))                                                        # body
    d.polygon([(10, int(h * 0.47)), (24, 4), (w - 24, 4), (w - 10, int(h * 0.47))], fill=(120, 26, 30, 255))                  # cabin
    d.polygon([(22, int(h * 0.43)), (32, 12), (w - 32, 12), (w - 22, int(h * 0.43))], fill=(120, 150, 176, 255))              # back window
    d.rectangle([6, int(h * 0.55), 26, int(h * 0.66)], fill=(255, 60, 50, 255)); d.rectangle([w - 26, int(h * 0.55), w - 6, int(h * 0.66)], fill=(255, 60, 50, 255))
    d.rectangle([0, h - 18, w, h - 10], fill=(170, 170, 176, 255))                                                            # bumper
    return im, [w / 2 + 1, h]


def main():
    os.makedirs(OUT, exist_ok=True)
    sky().save(os.path.join(OUT, "sky.png"))
    road().save(os.path.join(OUT, "road.png"))
    desert(True, [(222, 196, 150), (196, 166, 118), (206, 180, 136)]).save(os.path.join(OUT, "desert-l.png"))
    desert(False, [(150, 170, 104), (122, 142, 84), (136, 156, 94)]).save(os.path.join(OUT, "desert-r.png"))
    sheet, meta = things()
    sheet.save(os.path.join(OUT, "things.png"))
    with open(os.path.join(OUT, "things.json"), "w") as f: json.dump(meta, f, indent=1)
    im, foot = car()
    im.save(os.path.join(OUT, "car.png"))
    print("wrote", OUT, "(the car's foot:", foot, ")")


if __name__ == "__main__":
    main()

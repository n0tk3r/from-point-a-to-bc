"""Kihei's cat (scene `edo-fishshop`): a ginger-and-white Japanese cat with a short bobbed tail, her painted frames and
`cat.json`, as Ranger's (nevada_ranger.py). PAINT-20B.

    python3 edo_fishshop_cat.py        writes out/edo-fishshop/cat-*.png, cat.json and out/edo-fishshop-cat-sheet.png

The frames are at the size of the scene's row `full` (160 px to 175 cm: a cat 45 cm long nose to rump is 41 px), on one
canvas, the ground point under her at FOOT; she faces EAST (the engine turns her round). Sets: sit (2: the tail moving),
walk (4), run (3, a mackerel in her mouth), under (3: going under the raised floor, her back end disappearing: the engine
shows them where `under` is, her head end toward the gap), sleep (2: lying curled, a breath). Flat colours, one darker
tone each, and the dark line round her, as every creature of the game is drawn; keyed as the scene's frames."""

import json
import os

import numpy as np
from PIL import Image, ImageDraw

OUT = "out/edo-fishshop"
CW, CH = 64, 40
FOOT = (32, 38)
SS = 8
GINGER, GINGER_DK = (214, 134, 62), (168, 96, 40)
WHITE, WHITE_DK = (244, 238, 226), (200, 192, 176)
LINE = (46, 32, 24)
PINK = (222, 150, 140)
EYE = (70, 120, 60)
FISH, FISH_DK = (124, 147, 166), (72, 92, 108)


def canvas():
    im = Image.new("RGBA", (CW * SS, CH * SS), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def P(pts):
    return [(x * SS, y * SS) for x, y in pts]


def ell(d, cx, cy, rx, ry, fill, outline=LINE, w=1.0):
    d.ellipse([(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS], fill=fill, outline=outline, width=int(w * SS * 0.9))


def poly(d, pts, fill, outline=LINE, w=1.0):
    d.polygon(P(pts), fill=fill, outline=outline, width=int(w * SS * 0.9))


def head(d, hx, hy, r=5.0, eyes=True, mouth=None, ears=True):
    if ears:
        poly(d, [(hx - r * 0.9, hy - r * 0.3), (hx - r * 0.6, hy - r * 1.8), (hx - r * 0.05, hy - r * 0.9)], GINGER)
        poly(d, [(hx + r * 0.2, hy - r * 0.95), (hx + r * 0.7, hy - r * 1.75), (hx + r * 1.0, hy - r * 0.3)], GINGER)
    ell(d, hx, hy, r, r * 0.9, GINGER)
    ell(d, hx + r * 0.35, hy + r * 0.25, r * 0.55, r * 0.5, WHITE, outline=None)          # the white muzzle
    if eyes:
        ell(d, hx + r * 0.35, hy - r * 0.2, 0.9, 0.9, EYE, outline=None)
        ell(d, hx + r * 0.42, hy - r * 0.2, 0.3, 0.7, LINE, outline=None)
    d.ellipse([(hx + r * 0.78 - 0.6) * SS, (hy + r * 0.1 - 0.5) * SS, (hx + r * 0.78 + 0.6) * SS, (hy + r * 0.1 + 0.5) * SS], fill=PINK)
    if mouth is not None:                                                             # the mackerel held crosswise
        fx, fy = hx + r * 0.9, hy + r * 0.45
        poly(d, [(fx - 7, fy - 1.5), (fx + 6, fy - 2.2), (fx + 9, fy - 0.2), (fx + 6, fy + 1.8), (fx - 7, fy + 1.0)], FISH)
        poly(d, [(fx - 7, fy - 1.5), (fx - 10, fy - 3.5), (fx - 10, fy + 3.0), (fx - 7, fy + 1.0)], FISH_DK)


def body_side(d, x0, y0, L=22.0, h=9.0, legs=(0, 0, 0, 0), tail=0.0):
    """Her body side on, standing or walking: x0 is the rump's x, y0 the ground row; legs are each one's forward swing."""
    bx, by = x0 + L / 2, y0 - h - 4
    # the far legs first (darker), then the body, then the near legs
    for i, (lx, dark) in enumerate(((x0 + 4, True), (x0 + L - 4, True))):
        sw = legs[i * 2 + 1]
        poly(d, [(lx - 1.5 + sw, by + 2), (lx + 1.5 + sw, by + 2), (lx + 1.8 + sw * 1.4, y0 - 1), (lx - 1.8 + sw * 1.4, y0 - 1)], GINGER_DK)
    tx, ty = x0 - 1, by - 2
    poly(d, [(tx + 1, ty + 2), (tx - 3 - tail, ty - 3 - tail * 0.8), (tx - 1 - tail, ty - 5 - tail), (tx + 2.5, ty - 1)], GINGER)   # the short bobbed tail
    ell(d, bx, by, L / 2, h / 2 + 1, GINGER)
    ell(d, bx + 1, by + h * 0.25, L / 2 - 3, h / 2 - 1.5, WHITE, outline=None)       # the white belly and chest
    for i, lx in enumerate((x0 + 5, x0 + L - 3)):
        sw = legs[i * 2]
        poly(d, [(lx - 1.8 + sw, by + 2), (lx + 1.8 + sw, by + 2), (lx + 2.2 + sw * 1.4, y0 - 1), (lx - 2.2 + sw * 1.4, y0 - 1)], GINGER)
        ell(d, lx + sw * 1.4 + 0.4, y0 - 1.2, 2.4, 1.2, WHITE, outline=LINE, w=0.7)  # a white sock
    d.line(P([(x0 + 3, y0 - 0.5), (x0 + L + 4, y0 - 0.5)]), fill=(0, 0, 0, 90), width=int(1.2 * SS))   # the dark line under her
    return bx, by


def frame_sit(tail_up):
    im, d = canvas()
    x0, y0 = FOOT[0] - 10, FOOT[1]
    tx, ty = x0 - 2, y0 - 6
    poly(d, [(tx + 2, ty + 3), (tx - 6, ty + 4 - tail_up * 7), (tx - 7, ty + 1 - tail_up * 7), (tx + 2, ty - 1)], GINGER)
    ell(d, x0 + 7, y0 - 9, 8.5, 9.5, GINGER)                                      # haunches
    ell(d, x0 + 11, y0 - 11, 5.0, 10.0, WHITE, outline=None)                      # the white front
    for lx in (x0 + 10, x0 + 14):
        poly(d, [(lx - 1.8, y0 - 12), (lx + 1.8, y0 - 12), (lx + 2.0, y0 - 1), (lx - 2.0, y0 - 1)], GINGER)
        ell(d, lx + 0.6, y0 - 1.2, 2.4, 1.2, WHITE, outline=LINE, w=0.7)
    head(d, x0 + 14, y0 - 21, 5.2)
    d.line(P([(x0 - 2, y0 - 0.5), (x0 + 19, y0 - 0.5)]), fill=(0, 0, 0, 90), width=int(1.2 * SS))
    return im


def frame_walk(k):
    im, d = canvas()
    ph = k / 4 * 2 * np.pi
    legs = (np.sin(ph) * 2.2, np.sin(ph + np.pi) * 2.2, np.sin(ph + np.pi) * 2.2, np.sin(ph) * 2.2)
    bx, by = body_side(d, FOOT[0] - 12, FOOT[1], legs=legs, tail=0.5 + 0.5 * np.sin(ph))
    head(d, bx + 13, by - 2 + 0.4 * np.sin(ph * 2), 5.0)
    return im


def frame_run(k):
    im, d = canvas()
    stretch = (0, 1, -1)[k]
    legs = ((3.5, 3.0, -3.5, -3.0), (0.5, -0.5, 0.5, -0.5), (-3.5, -3.0, 3.5, 3.0))[k]
    bx, by = body_side(d, FOOT[0] - 13 - stretch, FOOT[1], L=24 + 2 * abs(stretch), h=8.0, legs=legs, tail=1.0)
    head(d, bx + 14 + abs(stretch), by - 1, 5.0, mouth="fish")
    return im


def frame_under(k):
    """Going under the raised floor, which is to the EAST of her: her head end gone first. k 0: half in; 1: hindquarters
    only; 2: a tail-tip. Drawn without the part that is under the floor (the engine shows nothing there)."""
    im, d = canvas()
    cut = (FOOT[0] + 6, FOOT[0] - 2, FOOT[0] - 8)[k]            # everything east of this column is under the floor: not drawn
    legs = ((2.5, -2.5, -2.5, 2.5), (-2.5, 2.5, 2.5, -2.5), (0, 0, 0, 0))[k]
    body_side(d, FOOT[0] - 12, FOOT[1], legs=legs, tail=1.2)
    if k == 0:
        head(d, FOOT[0] + 1, FOOT[1] - 15, 5.0, eyes=False)
    d.rectangle([cut * SS, 0, CW * SS, CH * SS], fill=(0, 0, 0, 0))
    return im


def frame_sleep(k):
    im, d = canvas()
    cx, cy = FOOT[0], FOOT[1] - 6
    ell(d, cx, cy, 13, 6 + 0.4 * k, GINGER)                                  # curled: a loaf with the head tucked
    ell(d, cx - 2, cy + 1.5, 7, 3, WHITE, outline=None)
    poly(d, [(cx + 10, cy + 1), (cx + 14, cy - 2), (cx + 13, cy + 3)], GINGER)   # the tail tip
    head(d, cx - 7, cy - 2 - 0.4 * k, 4.6, eyes=False)
    d.line(P([(cx - 11, cy - 2.5), (cx - 9, cy - 2.5)]), fill=LINE, width=int(0.8 * SS))      # the shut eye
    d.line(P([(cx - 13, FOOT[1] - 0.5), (cx + 13, FOOT[1] - 0.5)]), fill=(0, 0, 0, 90), width=int(1.2 * SS))
    return im


def down(im):
    """8x -> the frame, each pixel the majority of its block (hard edges, as Ranger's)."""
    a = np.asarray(im)
    h, w = CH, CW
    blocks = a.reshape(h, SS, w, SS, 4).transpose(0, 2, 1, 3, 4).reshape(h, w, SS * SS, 4)
    out = np.zeros((h, w, 4), dtype=np.uint8)
    cover = (blocks[..., 3] > 0).mean(axis=2)
    for yy in range(h):
        for xx in range(w):
            if cover[yy, xx] < 0.5:
                continue
            px = blocks[yy, xx][blocks[yy, xx][:, 3] > 0]
            vals, counts = np.unique(px, axis=0, return_counts=True)
            out[yy, xx] = vals[counts.argmax()]
            out[yy, xx, 3] = 255
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sets = {
        "sit": [frame_sit(0), frame_sit(1)],
        "walk": [frame_walk(k) for k in range(4)],
        "run": [frame_run(k) for k in range(3)],
        "under": [frame_under(k) for k in range(3)],
        "sleep": [frame_sleep(k) for k in range(2)],
    }
    made, tall = {}, {}
    for name, frs in sets.items():
        files = []
        for i, im in enumerate(frs):
            a = down(im)
            fn = f"cat-{name}-{i}.png"
            Image.fromarray(a, "RGBA").save(f"{OUT}/{fn}", optimize=True)
            files.append(fn)
            rows = np.nonzero(a[..., 3] > 0)[0]
            if len(rows):
                tall[name] = max(tall.get(name, 0), int(FOOT[1] - rows.min()))
        made[name] = files
    sidecar = {
        "id": "cat", "face": "E", "foot": list(FOOT), "canvas": [CW, CH],
        "tall": {"stand": tall["walk"], "sit": tall["sit"], "run": tall["run"], "under": tall["under"], "sleep": tall["sleep"]},
        "stride": {"walk": 14.0, "run": 30.0}, "pace": 60.0,
        "frames": made,
        "fps": {"sit": 1.2, "walk": 8, "run": 12, "under": 6, "sleep": 0.8},
        "fidgets": ["sit"],
        "sizeAt": 401,
        "note": "PAINT-20B: Kihei's cat, ginger and white, a short tail. Frames at the scene's row full (401); `under` is her going east under the raised floor at mark `under` (her head end first: the frames are cut at the gap's edge).",
    }
    with open(f"{OUT}/cat.json", "w") as f:
        json.dump(sidecar, f, indent=2)
    # a sheet to look at, 4x, on the earth floor's colour
    zoom = 4
    n = sum(len(v) for v in made.values())
    sheet = Image.new("RGB", (CW * zoom * 7 + 20, (CH * zoom + 24) * len(made) + 20), (140, 124, 100))
    y = 10
    for name, files in made.items():
        for i, fn in enumerate(files):
            im = Image.open(f"{OUT}/{fn}").convert("RGBA").resize((CW * zoom, CH * zoom), Image.NEAREST)
            sheet.paste(im, (10 + i * (CW * zoom + 6), y), im)
        y += CH * zoom + 24
    sheet.save("out/edo-fishshop-cat-sheet.png")
    print("cat:", n, "frames; tall", sidecar["tall"])

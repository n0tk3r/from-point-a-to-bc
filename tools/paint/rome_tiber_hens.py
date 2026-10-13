"""Mariam's hens, across the Tiber: painted as frames for the game to move. They stand in a row across the yard,
looking over the river at the city, and will not eat: so they stand, turn their heads a little, hold their heads up
very still, and now and then shuffle along the row. They never peck.

  hen-<set>-<n>.png    <set>: brown (a red-brown hen, a dark tail), speckled (grey barred with dark), white
                       <n>:   1, 2, 3 stand (the head as it is, turned a little toward us, a little lower), 4 look (the
                              head up, the neck stretched, very still), 5, 6 walk (a shuffle: the weight from foot to foot)

Seen side on, FACING WEST (to the left): toward the river and the sun, so the side of her we see is in her own shade
and the light runs along her breast, her back and the top of her head. Painted at the size a hen is where a person is
160 px tall (sizeAt 590): about 40 cm, 37 px. Every frame is on one canvas with her feet at one point (FOOT), so the
game can swap frames without the bird jumping. Flat colour, hard edges, pigment grain, then the backdrop's own palette
with its speckle, as the temple steps' birds are (rome_steps_birds.py).

    python3 rome_tiber_hens.py      paints the frames into out/rome-tiber/ (in back.png's palette) and the sheet
                                    out/rome-tiber-hens-sheet.png (4x, each frame's foot point marked)"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, Sheet, lerp
from rome_steps_birds import finish_frame, oval, turned
from rome_steps_kit import col, mix

CANVAS = (50, 46)                     # every frame: width, height
FOOT = (24, 42)                       # the point between her feet, on the ground, in every frame
SIZE = 37.0 * 1.0                     # her height in px at full size (40 cm where a man of 175 cm is 160 px)
SETS = {  # body, side in shade, wing, tail, hackles, light along her top, legs
    "brown": ("#9c5a30", "#6e3a22", "#7a4224", "#2e2a26", "#c8843e", "#f0b070", "#d8a040"),
    "speckled": ("#9a9aa6", "#6c6c7c", "#7e7e8e", "#3a3a48", "#b4b4c0", "#e8e8f0", "#d0b04a"),
    "white": ("#eee8dc", "#bcb4b0", "#d6cec4", "#ddd6cc", "#f6f0e6", "#fffcf4", "#e0b450"),
}
FRAMES = {  # n: head (dx, dy) from her neck's base in units of SIZE, turn (0 side on, 1 a little toward us), body tilt, feet
    1: dict(head=(-0.20, -0.70), turn=0.0, tilt=0.0, feet="stand"),
    2: dict(head=(-0.18, -0.72), turn=1.0, tilt=0.0, feet="stand"),
    3: dict(head=(-0.23, -0.65), turn=0.0, tilt=-0.04, feet="stand"),
    4: dict(head=(-0.17, -0.84), turn=0.0, tilt=0.08, feet="stand"),
    5: dict(head=(-0.21, -0.69), turn=0.0, tilt=0.03, feet="left"),
    6: dict(head=(-0.21, -0.71), turn=0.0, tilt=-0.02, feet="right"),
}
ACTS = {"stand": [1, 2, 1, 3], "look": [4], "walk": [5, 6]}


def hen(sh, ox, oy, s, n, tones, seed=0):
    """A hen with her feet at (ox, oy), facing left (west), `s` her height in px."""
    body, shade_, wing, tail, hackle, light, legs = [col(c) for c in tones]
    f = FRAMES[n]
    tilt = f["tilt"]
    rng = np.random.default_rng(seed + n)
    P = lambda pts: [(ox + x * s, oy + y * s) for x, y in turned(pts, (0.05, -0.42), tilt)]
    pt = lambda x, y: P([(x, y)])[0]
    # legs first (yellow, scaly), the body sits on them
    lw = max(1.0, s * 0.045)
    feet = {"stand": [(-0.06, 0.0), (0.10, 0.0)], "left": [(-0.14, -0.04), (0.10, 0.0)], "right": [(-0.06, 0.0), (0.18, -0.04)]}[f["feet"]]
    for (hx, hy), (fx, fy) in zip(((-0.04, -0.18), (0.10, -0.18)), feet):
        a = pt(hx, hy)
        b = (ox + fx * s, oy + fy * s)
        sh.line([a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), b], legs, lw)
        sh.line([(b[0] - 0.09 * s, b[1]), (b[0] + 0.05 * s, b[1])], legs, lw * 0.9)          # her toes
        sh.line([(b[0], b[1]), (b[0] - 0.05 * s, b[1] - 0.02 * s)], legs, lw * 0.8)
    # the tail: a fan of feathers standing up behind her (to the right)
    for j, (tx, ty) in enumerate(((0.40, -0.80), (0.48, -0.74), (0.53, -0.62))):             # the tail: three feathers fanned up behind her
        sh.poly(P([(0.20, -0.36), (tx - 0.05, ty - 0.02), (tx + 0.03, ty + 0.03), (0.32, -0.26)]), mix(tail, light, 0.08 * j))
    sh.line(P([(0.28, -0.40), (0.42, -0.76)]), mix(tail, "#000000", 0.25), max(0.7, s * 0.03))
    sh.line(P([(0.36, -0.80), (0.44, -0.80)]), mix(tail, light, 0.45), max(0.6, s * 0.025))
    # the body: a deep oval, its belly in shade, light along its back
    c0 = pt(0.03, -0.38)
    oval(sh, c0[0], c0[1], 0.36 * s, 0.25 * s, 0.12 - tilt, body)
    c1 = pt(0.03, -0.29)
    oval(sh, c1[0], c1[1], 0.30 * s, 0.13 * s, 0.10 - tilt, shade_)
    oval(sh, pt(0.07, -0.40)[0], pt(0.07, -0.40)[1], 0.22 * s, 0.13 * s, 0.06 - tilt, wing)          # the folded wing
    sh.line(P([(-0.12, -0.50), (0.10, -0.58), (0.26, -0.52)]), light, max(0.8, s * 0.04))             # the sun along her back
    sh.line(P([(-0.30, -0.40), (-0.29, -0.29), (-0.20, -0.20)]), mix(light, body, 0.35), max(0.8, s * 0.035))   # and down her breast
    if tones[0] == SETS["speckled"][0]:                                                               # bars and specks
        for k in range(16):
            x, y = rng.uniform(-0.26, 0.30), rng.uniform(-0.54, -0.24)
            px_, py_ = pt(x, y)
            sh.line([(px_ - 0.04 * s, py_), (px_ + 0.04 * s, py_ - 0.01 * s)], col("#40404e"), max(0.7, s * 0.03), 0.9)
    # the neck and its hackles, up to the head
    nb = pt(-0.20, -0.50)
    hx, hy = nb[0] + f["head"][0] * s * 0.55, nb[1] + (f["head"][1] + 0.50) * s
    sh.line([nb, (hx + 0.03 * s, hy + 0.05 * s)], hackle, 0.22 * s)
    sh.line([(nb[0] - 0.05 * s, nb[1] - 0.02 * s), (hx - 0.02 * s, hy + 0.04 * s)], mix(hackle, light, 0.4), max(0.7, s * 0.04))
    # the head, the comb, the wattle, the beak, the eye
    r = 0.115 * s
    sh.ellipse(hx, hy, r * 1.05, r, mix(hackle, body, 0.3))
    turn = f["turn"]
    comb = col("#d0362a")
    teeth = [(-0.08, -0.07), (-0.05, -0.15), (-0.02, -0.08), (0.01, -0.16), (0.04, -0.08), (0.07, -0.13), (0.09, -0.04)]
    sh.poly([(hx + x * s + turn * 0.01 * s, hy + y * s - r * 0.35) for x, y in teeth] + [(hx + 0.08 * s, hy - r * 0.1), (hx - 0.09 * s, hy - r * 0.1)], comb)
    sh.ellipse(hx - 0.09 * s, hy + 0.11 * s, 0.035 * s, 0.05 * s, comb)                              # the wattle
    bk = col("#e2b040")
    sh.poly([(hx - 0.09 * s, hy - 0.02 * s), (hx - 0.20 * s, hy + 0.02 * s), (hx - 0.09 * s, hy + 0.05 * s)], bk)
    ex = hx - 0.035 * s + turn * 0.015 * s
    sh.ellipse(ex, hy - 0.012 * s, max(0.9, 0.032 * s), max(0.9, 0.032 * s), col("#e88838"))
    sh.ellipse(ex - 0.004 * s, hy - 0.012 * s, max(0.55, 0.016 * s), max(0.55, 0.016 * s), col("#1a1418"))
    if turn:                                                  # her head turned a little toward us: the other eye's edge, the comb wider
        sh.ellipse(hx + 0.035 * s, hy - 0.01 * s, max(0.6, 0.02 * s), max(0.6, 0.02 * s), col("#c8702e"))
    sh.line([(hx - 0.05 * s, hy - r * 0.92), (hx + 0.06 * s, hy - r * 0.85)], light, max(0.6, s * 0.025), 0.8)   # light on her crown


def frame_of(draw, palette, ss=6):
    w, h = CANVAS
    sh = Sheet((h, w), ss=ss)
    draw(sh, FOOT[0], FOOT[1])
    c, a = sh.done()
    return finish_frame(c, a, palette)


def paint(out, palette):
    """Every frame of every set, into the folder `out`. -> {set: [file names in frame order]}"""
    from brush import save
    os.makedirs(out, exist_ok=True)
    made = {}
    for name, tones in SETS.items():
        made[name] = []
        for n in FRAMES:
            idx, a = frame_of(lambda sh, fx, fy, n=n: hen(sh, fx, fy, SIZE, n, tones, seed=len(name)), palette)
            fn = f"hen-{name}-{n}.png"
            save(f"{out}/{fn}", idx, palette, a)
            made[name].append(fn)
    return made


def frames_block(name):
    """A set as the engine's flock takes it (DESIGN.md, "Painted frames for birds"): her foot point, which way she
    faces as painted, the row at which she is the right size, and the files for each thing she does."""
    f = lambda ns: [f"hen-{name}-{n}.png" for n in ns]
    return {"foot": list(FOOT), "face": "W", "sizeAt": 590, "stand": f(ACTS["stand"]), "look": f(ACTS["look"]), "walk": f(ACTS["walk"])}


def sheet(out, made, path, zoom=4):
    """All the frames side by side, 4x, on the yard's earth, each with its foot point marked."""
    rows = []
    for name, files in made.items():
        ims = [Image.open(f"{out}/{f}").convert("RGBA") for f in files]
        w = sum(im.width + 4 for im in ims)
        row = Image.new("RGBA", (w, CANVAS[1]), (156, 132, 102, 255))
        x = 0
        for im in ims:
            row.alpha_composite(im, (x, 0))
            x += im.width + 4
        rows.append(row)
    W_ = max(r.width for r in rows)
    H_ = sum(r.height + 4 for r in rows)
    big = Image.new("RGBA", (W_, H_), (70, 66, 80, 255))
    y = 0
    for r in rows:
        big.alpha_composite(r, (0, y))
        y += r.height + 4
    big = big.resize((W_ * zoom, H_ * zoom), Image.NEAREST)
    d = ImageDraw.Draw(big)
    y = 0
    for name, files in made.items():
        x = 0
        for f in files:
            fx, fy = (x + FOOT[0]) * zoom + zoom // 2, (y + FOOT[1]) * zoom + zoom // 2
            d.line([(fx - 6, fy), (fx + 6, fy)], fill=(255, 40, 200, 255), width=1)
            d.line([(fx, fy - 6), (fx, fy + 6)], fill=(255, 40, 200, 255), width=1)
            x += CANVAS[0] + 4
        y += CANVAS[1] + 4
    big.convert("RGB").save(path)


def back_palette(path="out/rome-tiber/back.png"):
    im = Image.open(path)
    n = len(im.getpalette()) // 3
    clear = im.info.get("transparency")
    n = clear if isinstance(clear, int) else n
    return np.array(im.getpalette()[:3 * n], dtype=F32).reshape(-1, 3) / 255.0


if __name__ == "__main__":
    pal = back_palette()
    made = paint("out/rome-tiber", pal)
    sheet("out/rome-tiber", made, "out/rome-tiber-hens-sheet.png")
    print({k: len(v) for k, v in made.items()})

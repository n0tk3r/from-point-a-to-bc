"""PAINT-20A: the hens of Yui, in their yard by Kihei's shop, painted as frames for the engine's flock kind. Every one of
them faces WEST along the coast (puzzle #24: "the hens all face west"), which on this stage is to the RIGHT (the street
runs south-west, away from us and to the right), so the frames are painted facing right: the Tiber's hen drawn as
there (rome_tiber_hens.hen, facing left) and turned round. Brown and speckled, four or five of them.

  hen-<set>-<n>.png    <set>: brown, speckled
                       <n>:   1, 2, 3 stand (the head as it is, turned a little toward us, a little lower), 4 look (the
                              head up, very still), 5, 6 walk (the weight from foot to foot), 7 peck (the beak to the
                              ground), 8 the peck half way (the head coming back up: she turns back to face west)

Painted at the size a hen is where a person is 160 px tall (sizeAt 590): 40 cm, 37 px, on one 50 x 46 canvas with her
feet at FOOT in every frame. Flat colour, hard edges, pigment grain, then back.png's own palette with its speckle, as
the Tiber's hens are (so they must be painted after the full run of edo_village.py).

    python3 edo_village_hens.py      paints the frames into out/edo-village/ and the sheet out/edo-village-hens-sheet.png"""

import os

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, Sheet, save
import rome_tiber_hens as TH
from rome_steps_birds import finish_frame

CANVAS = TH.CANVAS                    # (50, 46)
FOOT = (CANVAS[0] - 1 - TH.FOOT[0], TH.FOOT[1])    # (25, 42): the Tiber's foot point, mirrored
SIZE = TH.SIZE
SETS = {"brown": TH.SETS["brown"], "speckled": TH.SETS["speckled"]}
# the two frames of ours, added to the Tiber's six (its FRAMES dict is extended at import, that file untouched)
TH.FRAMES[7] = dict(head=(-0.30, -0.20), turn=0.0, tilt=-0.14, feet="stand")      # the peck: the beak to the ground, the body tipped forward
TH.FRAMES[8] = dict(head=(-0.26, -0.46), turn=0.0, tilt=-0.07, feet="stand")      # half way back up
FRAMES = [1, 2, 3, 4, 5, 6, 7, 8]
ACTS = {"stand": [1, 2, 1, 3], "look": [4], "walk": [5, 6], "peck": [8, 7, 7, 8, 1]}


def frame_of(n, tones, seed, palette, ss=6):
    w, h = CANVAS
    sh = Sheet((h, w), ss=ss)
    TH.hen(sh, TH.FOOT[0], TH.FOOT[1], SIZE, n, tones, seed=seed)
    c, a = sh.done()
    c, a = c[:, ::-1].copy(), a[:, ::-1].copy()                      # turned round: she faces right (west along this coast)
    return finish_frame(c, a, palette)


def paint(out, palette):
    os.makedirs(out, exist_ok=True)
    made = {}
    for name, tones in SETS.items():
        made[name] = []
        for n in FRAMES:
            idx, a = frame_of(n, tones, len(name), palette)
            fn = f"hen-{name}-{n}.png"
            save(f"{out}/{fn}", idx, palette, a)
            made[name].append(fn)
    return made


def frames_block(name):
    """A set as the engine's flock takes it (docs/DESIGN.md, "Painted frames for birds")."""
    f = lambda ns: [f"hen-{name}-{n}.png" for n in ns]
    return {"foot": list(FOOT), "face": "E", "sizeAt": 590, "stand": f(ACTS["stand"]), "look": f(ACTS["look"]), "walk": f(ACTS["walk"]), "peck": f(ACTS["peck"])}


def sheet(out, made, path, zoom=4):
    rows = []
    for name, files in made.items():
        ims = [Image.open(f"{out}/{f}").convert("RGBA") for f in files]
        w = sum(im.width + 4 for im in ims)
        row = Image.new("RGBA", (w, CANVAS[1]), (176, 170, 158, 255))
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


def back_palette(path="out/edo-village/back.png"):
    im = Image.open(path)
    n = len(im.getpalette()) // 3
    clear = im.info.get("transparency")
    n = clear if isinstance(clear, int) else n
    return np.array(im.getpalette()[:3 * n], dtype=F32).reshape(-1, 3) / 255.0


if __name__ == "__main__":
    pal = back_palette()
    made = paint("out/edo-village", pal)
    sheet("out/edo-village", made, "out/edo-village-hens-sheet.png")
    print({k: len(v) for k, v in made.items()}, "foot", FOOT)

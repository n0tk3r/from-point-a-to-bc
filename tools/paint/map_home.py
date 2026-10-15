"""The map of the house (MAP-15H): the house as Dad would draw it for his family, in pencil, on a sheet of squared
paper that has been folded into a pocket. Tidy, ruled where a man with a ruler rules, freehand for the furniture and
the arrows, and a little proud of itself: every title underlined.

THE SHEET. Lead white, a breath cooler than the tube, printed with pale blue-grey squares (one square is two feet:
the plans are drawn to them), a heavier line every fifth; warmer and a shade darker toward the edges where it has been
handled; creased down the middle and across, the creases worn pale where they cross; the top right corner turned over;
an eraser smudge or two where something was drawn wrong and rubbed out. LIGHT: the room's, from the top left, so a
crease's facets are a shade apart and the turned corner throws a soft shadow down and to the right.

THE PLANS (map_home_things.py; the house measured from the rooms' models: map_home_house.py). The ground floor, the
upstairs and the attic, side by side, each titled, at one scale; the house turned so that the street is at the bottom.
The back (back.png) carries the walls of every floor, the doors as gaps, the windows, the stairs, the hatches, the
porch, the rooms that are not places (empty and unnamed), the titles: nothing inside the five rooms that are places.
Each place (place-<id>.png) is its room's furniture in plan, from its model; each way (path-<a>-<b>.png) is Dad's
arrow up the stairs, or a line of dots through a door or up the ladder. Pencil lies ON the paper: every place and way is
painted over the finished sheet, so that the paper's grain and the walls under a mark are in its colours.

  python3 map_home.py          paints everything into out/map-home/ and writes layout.json (map_home_layout.py)
  python3 map_home.py fast     skips the brush pass and the palette: out/map-home-work/ only, to look at"""

import hashlib
import os
import sys
import time

import numpy as np
from PIL import Image

import brush
from brush import F32, grain, noise, over, palette_of, save, strokes, to_palette
import map_home_kit as K
import map_home_layout
import map_home_things as T

OUT = "out/map-home"
WORK = "out/map-home-work"
SHAPE = (600, 800)
COLOURS = 208                                     # the whole map's one palette


def fields(seed=40):
    """The paper's tooth, the pencil's pressure coming and going, and where graphite catches the light: shared by
    every file, so that a mark sits on the sheet as if drawn on it."""
    tooth = np.clip(noise(SHAPE, 1.6, seed, 2) * 0.6 + noise(SHAPE, 5, seed + 1, 2) * 0.4, 0, 1)
    pressure = noise(SHAPE, (60, 60), seed + 2, 3)
    sheen = noise(SHAPE, (9, 9), seed + 3, 2)
    return tooth, pressure, sheen


def under(seed=11):
    """Pass 1: the sheet, broad and soft (map_home_kit.paper_under) and the eraser smudges rubbed into it."""
    outline, flap, fold = K.sheet_outline(T.SHEET_BOX, seed, T.TURNED)
    pic, sheet = K.paper_under(SHAPE, outline, flap, fold, T.CREASES, seed)
    # two eraser smudges: a wall drawn one square too far and rubbed out, and the attic's title tried once too low
    a = T.GF(-150.0, -250.0)
    K.smudge(pic, (a[0] + 6, a[1] + 4), (16, 6), -8, 0.34, seed + 5, ghost=[(a[0] - 8, a[1] - 6), (a[0] + 20, a[1] - 5)], shape_=sheet)
    t = T.TITLES["attic"][1]
    K.smudge(pic, (t[0] - 36, t[1] + 22), (24, 7), 4, 0.30, seed + 6, ghost=[(t[0] - 66, t[1] + 22), (t[0] - 6, t[1] + 23)], shape_=sheet)
    return pic, sheet, outline, flap, fold


def details_sheet(pic, sheet, flap, fold, seed=12):
    """Pass 3, the sheet's crisp things: the printed squares, the creases' lines, the turned corner laid over them."""
    origin = T.GF(-214.0 + 0.0, 1150.0)                    # the squares start where the plans do (Dad drew to them)
    thin, heavy = K.grid_masks(SHAPE, (origin[0] % T.SQUARE, origin[1] % T.SQUARE), T.SQUARE, 5)
    fade = 0.86 + 0.14 * noise(SHAPE, (140, 140), seed, 2)
    over(pic, K.GRID, thin * 0.36 * fade * sheet)
    over(pic, K.GRID_HEAVY, heavy * 0.44 * fade * sheet)
    K.crease_lines(pic, T.CREASES, sheet, seed + 1)
    fm = K.flap_paint(pic, flap, fold, seed + 2) if flap is not None else np.zeros(SHAPE, F32)
    # the sheet's own edge: a hair darker, where the paper has been handled and its cut edge catches the dust
    edge = np.clip(sheet - brush.blur(sheet, 0.9) * 1.0, 0, 1) * 2.0 + np.clip(fm - brush.blur(fm, 0.9), 0, 1) * 2.0
    brush.tint(pic, K.mixp(K.WHITE, K.SHADE, 0.6), np.clip(edge, 0, 1) * 0.55)
    return np.clip(np.maximum(sheet, fm), 0, 1)


def leads():
    """Every pencil layer: the back, each place, each way. -> {name: Lead}"""
    out = {}
    L = K.Lead(SHAPE, seed=1)
    T.draw_back(L)
    out["back"] = L
    for i, (pid, fn) in enumerate(T.PLACES.items()):
        L = K.Lead(SHAPE, seed=10 + i, bold=1.22)
        fn(L)
        out["place-" + pid] = L
    for i, ((a, b), fn) in enumerate(T.WAYS.items()):
        L = K.Lead(SHAPE, seed=30 + i, bold=1.1)
        fn(L)
        out[f"path-{a}-{b}"] = L
    return out


def paint(fast=False):
    t0 = time.time()
    tooth, pressure, sheen = fields()
    pic, sheet, outline, flap, fold = under()
    if not fast:                                            # pass 2: the brush over the paper, calm (a flat sheet seen close)
        key = hashlib.sha1(pic.tobytes()).hexdigest()[:16]
        cache = os.path.join(WORK, f"brushed-{key}.npy")       # (the paper alone: kept, so a change to the plans repaints fast)
        if os.path.exists(cache):
            brushed = np.load(cache)
        else:
            flow = np.zeros(SHAPE, F32) + 0.05
            brushed = strokes(pic, sizes=(7, 4, 2), seed=3, density=1.4, jitter=0.03, flow=flow, keep=0.62)
            os.makedirs(WORK, exist_ok=True)
            for old in os.listdir(WORK):
                if old.startswith("brushed-"):
                    os.remove(os.path.join(WORK, old))
            np.save(cache, brushed)
        pic = brush.lerp(pic, brushed, sheet[..., None])
    alpha_back = details_sheet(pic, sheet, flap, fold)
    layers = leads()
    cov = {k: L.done() for k, L in layers.items()}
    back_cov = cov["back"]
    if flap is not None:                                    # nothing is drawn on the back of the turned corner
        fm = brush.mask_poly(SHAPE, flap, ss=3)
        for k in back_cov:
            back_cov[k] = back_cov[k] * (1 - fm)
    K.graphite(pic, back_cov, tooth, pressure, sheen)
    pics = {"back": (pic, alpha_back)}
    for name, c in cov.items():
        if name == "back":
            continue
        p = pic.copy()
        K.graphite(p, c, tooth, pressure, sheen)
        pics[name] = (p, K.coverage(c))
    print(f"  painted in {time.time() - t0:.1f}s")
    return pics


def finish(pics, folder):
    """Pass 4: pigment grain, one palette for the whole map (the sheet with every place and way laid on it), each file
    reduced to it and written with its alpha as a mask (under half is clear: hard edges)."""
    os.makedirs(folder, exist_ok=True)
    every = pics["back"][0].copy()
    for name, (p, a) in pics.items():
        if name != "back":
            m = (a >= 0.5).astype(F32)
            every = brush.lerp(every, p, m[..., None])
    sample = grain(every, seed=21, amount=0.010)
    sheet = pics["back"][1] >= 0.5
    pal = palette_of([sample[sheet]], colors=COLOURS, seed=4)
    out = {}
    for name, (p, a) in pics.items():
        g = grain(p, seed=21, amount=0.010)
        idx = to_palette(g, pal, seed=5, speckle=0.010)
        alpha = a.copy()
        alpha[:128] = 0
        alpha[572:] = 0
        save(os.path.join(folder, name + ".png"), idx, pal, alpha)
        out[name] = (idx, alpha)
    return pal, out


def look(pics, folder):
    """Quick look (fast): the sheet with everything laid on it, and the back alone."""
    os.makedirs(folder, exist_ok=True)
    every = pics["back"][0].copy()
    for name, (p, a) in pics.items():
        if name != "back":
            every = brush.lerp(every, p, (a >= 0.5).astype(F32)[..., None])
    for nm, im in (("all", every), ("back", pics["back"][0])):
        rgba = np.dstack([np.clip(im, 0, 1), (pics["back"][1] >= 0.5).astype(F32)])
        Image.fromarray((rgba * 255 + 0.5).astype(np.uint8), "RGBA").save(os.path.join(folder, nm + ".png"))


if __name__ == "__main__":
    fast = "fast" in sys.argv
    pics = paint(fast)
    if fast:
        look(pics, WORK)
        print("fast look:", WORK)
        sys.exit(0)
    pal, files = finish(pics, OUT)
    lay = map_home_layout.measure(OUT)
    with open(os.path.join(OUT, "layout.json"), "w") as f:
        f.write(map_home_layout.dumps(lay))
    total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
    print(f"wrote {len(files)} pictures and layout.json into {OUT}: palette {len(pal)} colours, {total / 1024:.0f} KB")

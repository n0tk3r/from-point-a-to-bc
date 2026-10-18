"""The map of the Office (OFFICE-17B): a blueprint of the ground floor of the Office of Peculiar Sectors' desert field
headquarters, sheet 1 of 8, white lines on blueprint blue.

THE SHEET. A contact print: the blue of the print (prussian blue with cobalt), developed a little unevenly, paler and
greyer toward the edges where it has been handled, creased where it was folded in four, the top right corner
dog-eared. Its border; in the corner the title block (OFFICE OF PECULIAR SECTORS · DESERT FIELD HQ · GROUND FLOOR · SHEET
1 OF 8); a scale bar; a north arrow; general notes. LIGHT: the room's, from the top left, so a crease's facets are a
shade apart and the dog-ear throws a soft shadow down and to the left.

THE PLAN (map_office_things.py). The ground floor, north up, the lot at the bottom. The back (back.png) carries the
sheet's furniture and the walls, doors and room numbers, nothing of a place. Each place (place-<id>.png) is its drawing
and each way (path-<a>-<b>.png) its route, printed in the same white; the B-7 shaft and the elevator carry a red rubber
stamp, B-7 · RESTRICTED. Every place and way is laid on the finished sheet, so that the paper under a line is the sheet's.

  python3 map_office.py          paints everything into out/map-office/ and writes layout.json (map_office_layout.py)
  python3 map_office.py fast     skips the brush pass and the palette: out/map-office-work/ only, to look at"""

import hashlib
import os
import sys
import time

import numpy as np
from PIL import Image

import brush
from brush import F32, grain, noise, over, palette_of, save, strokes, to_palette
import map_office_kit as K
import map_office_things as T

OUT = "out/map-office"
WORK = "out/map-office-work"
SHAPE = (600, 800)
COLOURS = 200                                     # the whole map's one palette


def under(seed=17):
    """Pass 1: the sheet, broad and soft."""
    x0, y0, x1, y1 = T.SHEET_BOX
    outline, flap, fold = K.sheet_outline((x0 + 2, y0 + 2, x1 - 2, y1 - 2), seed, ((x1 - 2, y0 + 2), T.EAR[1]))   # (its wandering edge kept inside the box)
    pic, sheet = K.paper_under(SHAPE, outline, flap, T.CREASES, seed)
    return pic, sheet, outline, flap, fold


def details_sheet(pic, sheet, flap, fold, seed=18):
    """Pass 3, the sheet's crisp things: the creases' lines, the dog-ear laid over them, the sheet's own edge."""
    K.crease_lines(pic, T.CREASES, sheet, seed)
    fm = K.flap_paint(pic, flap, fold, seed + 2) if flap is not None else np.zeros(SHAPE, F32)
    edge = np.clip(sheet - brush.blur(sheet, 0.9), 0, 1) * 2.0 + np.clip(fm - brush.blur(fm, 0.9), 0, 1) * 2.0
    brush.tint(pic, K.mixp("lead-white", K.SHADE, 0.6), np.clip(edge, 0, 1) * 0.5)
    return np.clip(np.maximum(sheet, fm), 0, 1), fm


def pens():
    """Every drawing: the back, each place, each way. -> {name: Pen}"""
    out = {}
    P = K.Pen(SHAPE, seed=1)
    T.draw_back(P)
    out["back"] = P
    for i, (pid, fn) in enumerate(T.PLACES.items()):
        P = K.Pen(SHAPE, seed=10 + i)
        fn(P)
        out["place-" + pid] = P
    for i, ((a, b), fn) in enumerate(T.WAYS.items()):
        P = K.Pen(SHAPE, seed=30 + i)
        fn(P)
        out[f"path-{a}-{b}"] = P
    return out


def paint(fast=False):
    t0 = time.time()
    pic, sheet, outline, flap, fold = under()
    if not fast:                                            # pass 2: the brush over the print, calm (a flat sheet seen close)
        key = hashlib.sha1(pic.tobytes()).hexdigest()[:16]
        cache = os.path.join(WORK, f"brushed-{key}.npy")
        if os.path.exists(cache):
            brushed = np.load(cache)
        else:
            flow = np.zeros(SHAPE, F32) + 0.05
            brushed = strokes(pic, sizes=(7, 4, 2), seed=3, density=1.4, jitter=0.03, flow=flow, keep=0.6)
            os.makedirs(WORK, exist_ok=True)
            for old in os.listdir(WORK):
                if old.startswith("brushed-"):
                    os.remove(os.path.join(WORK, old))
            np.save(cache, brushed)
        pic = brush.lerp(pic, brushed, sheet[..., None])
    alpha_back, fm = details_sheet(pic, sheet, flap, fold)
    grain_ = np.clip(noise(SHAPE, 1.4, 5, 2) * 0.7 + noise(SHAPE, 6, 6, 2) * 0.3, 0, 1)
    layers = pens()
    cov = {k: P.done() for k, P in layers.items()}
    back_cov = cov["back"]
    for k in back_cov:                                      # nothing is printed on the back of the dog-ear
        back_cov[k] = back_cov[k] * (1 - fm)
    K.prints(pic, back_cov, grain_)
    pics = {"back": (pic, alpha_back)}
    for name, c in cov.items():
        if name == "back":
            continue
        p = pic.copy()
        a = K.prints(p, c, grain_)
        alpha = K.coverage(c)
        if name == "place-b7":                              # the rubber stamp, in red ink over the print
            st = T.STAMP
            ink = K.stamp(SHAPE, st["centre"], st["lines"], st["cap"], st["angle"], seed=23)
            over(p, K.STAMP_RED, np.clip(ink * 1.1, 0, 0.92))
            alpha = np.maximum(alpha, (ink > 0.22).astype(F32))
        pics[name] = (p, alpha)
    print(f"  painted in {time.time() - t0:.1f}s")
    return pics


def finish(pics, folder):
    """Pass 4: grain, one palette for the whole map (the sheet with every place and way laid on it), each file reduced
    to it and written with its alpha as a mask (under half is clear: hard edges); the band and the label line clear."""
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
        idx = to_palette(g, pal, seed=5, speckle=0.008)
        alpha = a.copy()
        alpha[:128] = 0
        alpha[572:] = 0
        save(os.path.join(folder, name + ".png"), idx, pal, alpha)
        out[name] = (idx, alpha)
    return pal, out


def look(pics, folder):
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
    import map_office_layout
    pal, files = finish(pics, OUT)
    lay = map_office_layout.measure(OUT)
    with open(os.path.join(OUT, "layout.json"), "w") as f:
        f.write(map_office_layout.dumps(lay))
    total = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT))
    print(f"wrote {len(files)} pictures and layout.json into {OUT}: palette {len(pal)} colours, {total / 1024:.0f} KB")

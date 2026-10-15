"""The map of Egypt, about 1920 B.C. (MAP-15E): a scribe's sketch on papyrus, for the game's map screen.

    python3 map_egypt.py fast     a quick look (no brush pass): out/map-egypt-all.png
    python3 map_egypt.py          the full passes: out/map-egypt/ (back.png, place-*.png, path-*.png, layout.json),
                                  then the checks and their pictures (map_egypt_check.py: out/map-egypt-check/)
    python3 install.py map-egypt  copies out/map-egypt/ into art/maps/egypt/ as painted (maps are not keyed)

THE PLAN
  Material   one sheet of papyrus, landscape, made of two sheets joined: its strips laid across and along, a fine
             weave, a warm straw paler in the middle, the edges frayed and browned, an old fold, a stain or two.
  Hand       a reed pen: black (carbon) for the drawing, red (ochre) for the ways and the marks; a little thin colour
             laid with a brush where a scribe's brush would lay it (the river, the palms' heads, the red box).
  Lie of     the Nile along the bottom (zigzag water between two lines, fish and lotus in it); the edge of the desert
  the land   (a red rim, the sand as red dots above it); the far small pyramids; the Horizon's outline as it is seen
             from the river, its inside blank (back.png: never a place, never a way).
  Places     river (the wagon nose down among the reeds and palms, the donkey drinking), site (the works at the
             pyramid's foot and the stair up the face to the entrance), gallery (inside the outline: the passage
             climbing steeply, its lamps as red dots), chamber (the room at the top, the king's furniture small, its
             far wall plain).
  Ways       river-site the track up from the river with the boy's small prints; site-gallery up the stair and in at
             the entrance; gallery-chamber the ramp up to the doorway at the top.
  Three      the material is the light; the ink is the dark; the thin colours and the red are the middle. The eye
  tones      goes up the red track from the red box to the great outline, and in.
  Finish     one palette for the whole map (the sheet with every place and way laid on it), each file reduced to it;
             every place and way is ink on papyrus (the sheet's grain is in its picture), on a hard-edged mask.

The places and ways are drawn in map_egypt_things.py, measured in map_egypt_kit.py; map_egypt_layout.py measures
layout.json from the finished pictures; map_egypt_check.py checks it and draws the four check pictures."""

import os
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, blur, grain, palette_of, save, strokes, to_palette
import map_egypt_kit as K
import map_egypt_things as T

SHAPE = K.SHAPE
OUT = K.OUT
SPECKLE = 0.011
GRAIN = 0.016
COLORS = 208


def under(seed=11, ss=2):
    """The papyrus, blocked in: its colour, strips, fibres, joins, edges, fold and stains."""
    return K.papyrus(seed, ss)


def brushed(pic, info, fast=False):
    """The brush over the whole sheet, its marks running with the strips, small and kept light so the sheet stays
    calm enough to read names on."""
    if fast:
        return pic.copy()
    flow = np.zeros(SHAPE, F32)                       # along the strips
    return strokes(pic, sizes=(7, 4, 2), seed=3, density=1.3, jitter=0.022, keep=0.58, flow=flow)


def details(pic, under_pic, info):
    """Over the brushwork: the sheet's finest strands and the frayed threads restated crisp, as they are."""
    fine = under_pic - blur(under_pic, 1.2)
    out = np.clip(pic + fine * 0.55, 0, 1)
    edge = info["edge"]
    near = (edge < 2.0)[..., None]
    return np.where(near, under_pic, out).astype(F32)


def layers():
    back = T.back()
    places = {k: f() for k, f in T.PLACES.items()}
    ways, routes = {}, {}
    for key, f in T.WAYS.items():
        ways[key], routes[key] = f()
    return back, places, ways, routes


def pictures(fast=False):
    """Every file's picture as painted (floats) and its mask: {name: (picture, mask)}, and the routes."""
    t0 = time.time()
    paper, sheet_alpha, info = under(ss=1 if fast else 2)
    print("  under", round(time.time() - t0, 1))
    pic = brushed(paper, info, fast)
    print("  brush", round(time.time() - t0, 1))
    pic = details(pic, paper, info)
    back, places, ways, routes = layers()
    print("  drawn", round(time.time() - t0, 1))
    sheet = sheet_alpha > 0.5
    base = K.lay(pic, back, info)
    files = {"back": (base, sheet)}
    for name, pen in places.items():
        files["place-" + name] = (K.lay(base, pen, info), (pen.coverage() > 0.10) & sheet)
    for (a, b), pen in ways.items():
        files[f"path-{a}-{b}"] = (K.lay(base, pen, info), (pen.coverage() > 0.10) & sheet)
    print("  laid", round(time.time() - t0, 1))
    return files, routes, info


def finish(files, colors=COLORS):
    """Grain, one palette for the whole map, each file reduced to it with the same speckle, so that where two files
    hold the same paint they hold the same pixels."""
    grained = {k: (grain(p, 7, GRAIN), m) for k, (p, m) in files.items()}
    sample = [grained["back"][0][grained["back"][1]].reshape(-1, 1, 3)]
    for k, (p, m) in grained.items():
        if k != "back" and m.any():
            sample.append(np.repeat(p[m].reshape(-1, 1, 3), 3, axis=0))   # the drawings count three times: their few darks matter
    pal = palette_of(sample, colors=colors, seed=3, rounds=14)
    out = {}
    for k, (p, m) in grained.items():
        idx = to_palette(p, pal, seed=5, speckle=SPECKLE)
        out[k] = (idx, m)
    return pal, out


def write(pal, reduced, folder=OUT):
    os.makedirs(folder, exist_ok=True)
    total = 0
    for k, (idx, m) in reduced.items():
        path = os.path.join(folder, k + ".png")
        save(path, idx, pal, m.astype(F32))
        total += os.path.getsize(path)
        print(f"  {k}.png {os.path.getsize(path) // 1024} KB")
    print(f"  {len(reduced)} pictures, {total // 1024} KB, {len(pal)} colours")
    return total


def preview(files, name):
    """Everything drawn, over a dark ground: for a quick look."""
    back, sheet = files["back"]
    pic = np.where(sheet[..., None], back, np.array([0.14, 0.12, 0.11], F32))
    for k, (p, m) in files.items():
        if k != "back":
            pic = np.where(m[..., None], p, pic)
    Image.fromarray((np.clip(pic, 0, 1) * 255 + 0.5).astype(np.uint8)).save(name)


if __name__ == "__main__":
    t0 = time.time()
    fast = "fast" in sys.argv
    draft = "draft" in sys.argv                       # (the files, layout and checks without the brush pass: for the layout's sake)
    os.makedirs("out", exist_ok=True)
    files, routes, info = pictures(fast or draft)
    preview(files, OUT + "-all.png")
    if fast:
        print("fast look:", OUT + "-all.png", round(time.time() - t0, 1))
        sys.exit()
    pal, reduced = finish(files)
    write(pal, reduced)
    import map_egypt_layout
    map_egypt_layout.main(routes)
    import map_egypt_check
    ok = map_egypt_check.main()[0]
    print("done", round(time.time() - t0, 1), "checks", "passed" if ok else "FAILED", "(draft: no brush pass)" if draft else "")

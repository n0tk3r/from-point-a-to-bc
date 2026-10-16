"""The world outside the limousine's windows (nevada-limo, Act Five), for the engine's `drive` kind (DRIVE-16P).

    python3 nevada_limo_drive.py            every picture, the full passes (under a minute)
    python3 nevada_limo_drive.py fast       a quick look: no brush passes
    python3 nevada_limo_drive.py sky bands  only those parts (sky, bands, ground, things)
    python3 nevada_limo_drive_check.py      the checks, and the pictures seen through the four panes (look at them)

writes, into out/nevada-limo/ beside the scene's other paintings (install.py keys them as the scene's frames):

    drive-sky.png                  800 x 600, the stage: the sky, drawn still wherever a pane shows sky
    drive-far-l.png, drive-far-r.png    the far ranges, each side's own: 2400 x 48, ppm 0.07 (left, for 6000 m out) and
                                        0.14 (right, nearer, lower hills, for 3000 m)
    drive-mid-l.png, drive-mid-r.png    the middle distance: 2400 x 40, ppm 0.5 (for 850 m)
    drive-ground-l.png, drive-ground-r.png   the ground from straight above: 1024 x 512, 16 px a metre, from 6 m out
    drive-things.png, drive-things.json      the upright things, 24 px a metre, each in two lights (-l, -r)

and looks at each into out/nevada-limo-drive/. What the engine does with them is DRIVE-16's contract (S/briefs/DRIVE-16.md):
the camera of the scene (horizon 220, vanishing point 424, focal 345, the eye 1.83 m above the road), the bands stood
`distance` metres out and drawn column by column, the ground read under every pixel, the things stood along the road.

THE LIGHT is the roadside's morning, a few miles on: the sun low on the car's right and a little behind (shadows to
the screen's left through both sides' windows; the left windows have the sun at their back, the right ones look toward
its side of the sky). THE GLASS: every picture is painted in the roadside's colours and then smoked, darker and bluer,
as desert-strip.png was. Every picture but the sky repeats end to end along the road with no seam
(nevada_limo_drive_kit.py says how). The parts: _kit (the numbers, the tools for pictures that repeat), _sky, _bands,
_ground, _things, _check."""

import json
import os
import sys
import time

import numpy as np

from brush import F32, strokes
from nevada_limo_drive_kit import BANDS, finish, look, seam, write

OUT = "out/nevada-limo"
WORK = "out/nevada-limo-drive"
SEED = 16


def report(name, path, idx, pal, alpha=None, loops=True):
    shown = pal[idx]
    s = seam(shown) if loops else None
    size = os.path.getsize(path)
    print(f"  {os.path.basename(path)}: {idx.shape[1]} x {idx.shape[0]}, {len(pal)} colours, {size:,} bytes"
          + (f", seam {s[0]:.4f} (neighbouring columns anywhere {s[1]:.4f})" if s else "")
          + (f", {100 * float((alpha >= 0.5).mean()):.1f}% painted" if alpha is not None else ""))
    return shown


def do_sky(fast):
    from nevada_limo_drive_sky import paint_sky
    pic, el = paint_sky(SEED + 1)
    if not fast:                                                             # the brush over the part any pane can show
        top = pic[:262].copy()
        pic[:262] = strokes(top, sizes=(5, 3, 2), seed=SEED + 2, density=1.5, jitter=0.02, keep=0.5)
    # grain and speckle only where a pane can show the sky (rows 165 to 262, beside the panes' columns): elsewhere it is
    # never seen, and plain paint costs fewer bytes
    yy, xx = np.mgrid[0:600, 0:800].astype(F32)
    seen = np.clip(1 - np.maximum(165 - yy, yy - 262) / 12.0, 0, 1) * np.clip(1 - np.minimum(xx - 312, 532 - xx) / 12.0, 0, 1)
    idx, pal = finish(pic, SEED + 3, 96, grain=0.012, speckle=0.008, where=seen)
    path = write(f"{OUT}/drive-sky.png", idx, pal)
    shown = report("sky", path, idx, pal, loops=False)
    look(f"{WORK}/sky.png", shown[150:260], k=2)


def do_bands(fast):
    import nevada_limo_drive_bands as B
    for name, fn, colors in (("far-l", B.far_left, 72), ("far-r", B.far_right, 64), ("mid-l", B.mid_left, 72), ("mid-r", B.mid_right, 64)):
        pic, alpha = fn(fast=fast)
        idx, pal = finish(pic, SEED + 10 + len(name) + ord(name[-1]), colors, alpha=alpha, grain=0.010, speckle=0.006)
        path = write(f"{OUT}/drive-{name}.png", idx, pal, alpha)
        shown = report(name, path, idx, pal, alpha)
        w = shown.shape[1]
        look(f"{WORK}/{name}.png", np.concatenate([shown[:, :w // 2], shown[:, w // 2:]], axis=0), k=2, alpha=np.concatenate([alpha[:, :w // 2], alpha[:, w // 2:]], axis=0))


def do_ground(fast):
    import nevada_limo_drive_ground as G
    for name, fn in (("ground-l", G.ground_left), ("ground-r", G.ground_right)):
        t = time.time()
        pic = fn(fast=fast)
        # grain and speckle full near the road, thinning out from 15 m (the far rows are only ever seen squeezed and
        # averaged, where they would only cost bytes) to a fifth at 30 m
        X = 6.0 + np.arange(512, dtype=F32)[:, None] / 16.0
        where = np.broadcast_to(np.clip(1 - (X - 15.0) / 15.0, 0.2, 1.0), (512, 1024))
        idx, pal = finish(pic, SEED + 20 + ord(name[-1]), 96, grain=0.012, speckle=0.007, where=where)
        path = write(f"{OUT}/drive-{name}.png", idx, pal)
        shown = report(name, path, idx, pal)
        look(f"{WORK}/{name}.png", shown)
        look(f"{WORK}/{name}-near.png", shown[:200, :400], k=3)
        print(f"    ({time.time() - t:.0f} s)")


def do_things(fast):
    import nevada_limo_drive_things as T
    items = T.paint_things()
    rgb_, alpha, boxes = T.pack(items)
    heights = {n: boxes[n][3] / T.PPM for n in boxes}
    idx, pal = finish(rgb_, SEED + 30, 128, alpha=alpha, grain=0.010, speckle=0.006)
    path = write(f"{OUT}/drive-things.png", idx, pal, alpha)
    report("things", path, idx, pal, alpha, loops=False)
    meta = T.sheet_json(boxes, heights)
    with open(f"{OUT}/drive-things.json", "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    print(f"  drive-things.json: {len(meta['sprites'])} names ({len(boxes)} pictures, each thing in two lights, and {len(T.ALIASES)} plain names)")
    look(f"{WORK}/things.png", pal[idx], alpha=alpha, under="#c8b49a")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    fast = "fast" in sys.argv
    parts = [a for a in sys.argv[1:] if a in ("sky", "bands", "ground", "things")] or ["sky", "bands", "ground", "things"]
    t0 = time.time()
    for p in parts:
        t = time.time()
        print(p + (" (fast)" if fast else ""))
        {"sky": do_sky, "bands": do_bands, "ground": do_ground, "things": do_things}[p](fast)
        print(f"  {time.time() - t:.0f} s")
    print(f"done in {time.time() - t0:.0f} s")

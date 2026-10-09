"""Round four, the proof for the street: back.png and fountain.png changed only where the moving things were.

  python3 rome_street_check4.py OLD_DIR NEW_DIR [OUT.png]

Uses the mask rome_street.py writes beside NEW_DIR (rome-street-moved.png: every pixel the things taken out had
touched, before the finish). Also: the other cut-outs byte for byte; the washing's pieces laid together are
laundry.png; the cat's first frame over the new back.png gives the old one back."""

import json
import os
import sys

import numpy as np
from PIL import Image

old_dir, new_dir = sys.argv[1], sys.argv[2]
out_png = sys.argv[3] if len(sys.argv) > 3 else None
moved = np.asarray(Image.open(os.path.join(os.path.dirname(new_dir.rstrip("/")), "rome-street-moved.png"))) > 0
bad = 0
for f in ("back.png", "fountain.png"):
    a, b = Image.open(f"{old_dir}/{f}"), Image.open(f"{new_dir}/{f}")
    ia, ib = np.asarray(a), np.asarray(b)
    ch = ia != ib
    stray = int((ch & ~moved).sum())
    bad += stray + (a.getpalette() != b.getpalette())
    ys, xs = np.nonzero(ch)
    print(f"{f}: palette the same: {a.getpalette() == b.getpalette()}; {int(ch.sum())} px changed"
          + (f" (x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()})" if len(xs) else "") + f"; outside where the moving things were: {stray} (must be 0)")
for f in ("awning.png", "front.png", "laundry.png", "tunic.png"):
    same = open(f"{old_dir}/{f}", "rb").read() == open(f"{new_dir}/{f}", "rb").read()
    bad += not same
    print(f"{f}: {'byte for byte the same' if same else 'CHANGED'}")

lay = json.load(open(f"{new_dir}/layout.json"))
lau = Image.open(f"{new_dir}/laundry.png")
clear = lau.info["transparency"]
stack = np.full((600, 800), clear, np.uint8)
for name in lay["frames"]["laundry"]["files"][1:] + lay["frames"]["laundry"]["files"][:1]:
    a = np.asarray(Image.open(f"{new_dir}/{name}"))
    stack = np.where(a != clear, a, stack)
same = bool((stack == np.asarray(lau)).all())
bad += not same
print(f"the washing's {len(lay['frames']['laundry']['files'])} pieces laid together are laundry.png: {same}")

cat = lay["frames"]["cat"]
c1 = Image.open(f"{new_dir}/cat-1.png")
x0, y0 = cat["at"][0] - cat["foot"][0], cat["at"][1] - cat["foot"][1]
w, h = c1.size
back_new = np.asarray(Image.open(f"{new_dir}/back.png"))[y0:y0 + h, x0:x0 + w]
back_old = np.asarray(Image.open(f"{old_dir}/back.png"))[y0:y0 + h, x0:x0 + w]
ci = np.asarray(c1)
over = np.where(ci != c1.info["transparency"], ci, back_new)
print(f"the cat's frame 1 over the new back.png, against the old back.png, in its {w}x{h} box: {int((over != back_old).sum())} px differ")

if out_png:
    im = Image.open(f"{new_dir}/back.png").convert("RGB")
    px = np.asarray(im).copy()
    ch = np.asarray(Image.open(f"{old_dir}/back.png")) != np.asarray(Image.open(f"{new_dir}/back.png"))
    px[ch] = (px[ch] * 0.3 + np.array([255, 0, 0]) * 0.7).astype(np.uint8)
    Image.fromarray(px).save(out_png)
sys.exit(1 if bad else 0)

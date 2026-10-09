"""Round four, the proof for the temple: table.png lost its lamp flame and nothing else.

  python3 rome_temple_check4.py OLD_DIR NEW_DIR [OUT.png]

Every pixel of table.png that changed (index or clear/not clear) must lie where the flame was (the mask
rome_temple.py writes beside NEW_DIR: rome-temple-moved.png); the palette must be the same; back.png and front.png
must be byte for byte the same."""

import os
import sys

import numpy as np
from PIL import Image

old_dir, new_dir = sys.argv[1], sys.argv[2]
out_png = sys.argv[3] if len(sys.argv) > 3 else None
place = np.asarray(Image.open(os.path.join(os.path.dirname(new_dir.rstrip("/")), "rome-temple-moved.png"))) > 0
a, b = Image.open(f"{old_dir}/table.png"), Image.open(f"{new_dir}/table.png")
ia, ib = np.asarray(a), np.asarray(b)
ta, tb = a.info.get("transparency"), b.info.get("transparency")
changed = ia != ib
print(f"table.png: palette the same: {a.getpalette() == b.getpalette()}; clear index {ta} / {tb}")
print(f"  pixels changed: {int(changed.sum())}, outside where the flame was: {int((changed & ~place).sum())} (must be 0)")
ys, xs = np.nonzero(changed)
if len(xs):
    print(f"  all inside x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()}; now clear: {int(((ib == tb) & changed).sum())}, "
          f"now lamp: {int(((ib != tb) & changed).sum())}")
for f in ("back.png", "front.png"):
    print(f"  {f}: {'byte for byte the same' if open(f'{old_dir}/{f}', 'rb').read() == open(f'{new_dir}/{f}', 'rb').read() else 'CHANGED'}")
if out_png:
    comp = Image.open(f"{new_dir}/back.png").convert("RGBA")
    comp.alpha_composite(b.convert("RGBA"))
    comp.alpha_composite(Image.open(f"{new_dir}/front.png").convert("RGBA"))
    old = Image.open(f"{old_dir}/back.png").convert("RGBA")
    old.alpha_composite(a.convert("RGBA"))
    old.alpha_composite(Image.open(f"{old_dir}/front.png").convert("RGBA"))
    box = (596, 376, 664, 424)
    pair = Image.new("RGB", ((box[2] - box[0]) * 2 + 4, box[3] - box[1]), (255, 0, 255))
    pair.paste(old.crop(box).convert("RGB"), (0, 0))
    pair.paste(comp.crop(box).convert("RGB"), (box[2] - box[0] + 4, 0))
    pair.resize((pair.width * 8, pair.height * 8), Image.NEAREST).save(out_png)
sys.exit(0 if not (changed & ~place).any() and a.getpalette() == b.getpalette() else 1)

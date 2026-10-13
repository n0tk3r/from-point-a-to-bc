"""A look at the limousine as the game will show it: the desert strip behind the panes, the cut-outs over it.

    python3 nevada_limo_look.py [folder] [out.png] [t]      (folder: out/nevada-limo, or the installed art/scenes/nevada-limo)

The strip is laid as the engine's `strip` kind lays it: its bottom edge on the stage row `strip.row`, the column `pos`
of it at the stage's left edge, cut to each window's polygon (a pixel is in the window when its middle is); the left
windows' strip `t` seconds gone by to the left (speed 90), the right windows' to the right (speed -90). Then the
cut-outs in their first state (divider up, the ropes' four strands, the bag, the juice, the clipboard, our seat), and
a second picture of the later state (divider down, one strand, the things taken) beside it."""

import json
import sys

import numpy as np
from PIL import Image

from nevada_limo import inside_poly

folder = sys.argv[1] if len(sys.argv) > 1 else "out/nevada-limo"
out = sys.argv[2] if len(sys.argv) > 2 else "out/nevada-limo-look.png"
t = float(sys.argv[3]) if len(sys.argv) > 3 else 7.0
L = json.load(open(f"{folder}/layout.json")) if not folder.startswith("../") else json.load(open(f"{folder}/layout.json"))
strip = np.asarray(Image.open(f"{folder}/desert-strip.png").convert("RGB"))
sh, sw = strip.shape[:2]
row = L["strip"]["row"]


def with_strip(back, t):
    pic = back.copy()
    for wdw in L["windows"]:
        m = inside_poly(wdw["poly"])
        speed = 90.0 if wdw["side"] == "L" else -90.0
        pos = int(round(speed * t))
        ys, xs = np.nonzero(m)
        sy = ys - (row - sh)
        ok = (sy >= 0) & (sy < sh)
        sx = (xs + pos) % sw
        pic[ys[ok], xs[ok]] = strip[sy[ok], sx[ok]]
    return pic


def lay(pic, names):
    im = Image.fromarray(pic).convert("RGBA")
    for n in names:
        im.alpha_composite(Image.open(f"{folder}/{n}.png").convert("RGBA"))
    return np.asarray(im.convert("RGB"))


back = np.asarray(Image.open(f"{folder}/back.png").convert("RGB"))
first = lay(with_strip(back, t), ["divider-up", "ropes-4", "bag", "juice", "clipboard", "front"])
later = lay(with_strip(back, t + 3.0), ["divider-down", "ropes-1", "front"])
Image.fromarray(first).save(out)
Image.fromarray(later).save(out.replace(".png", "-later.png"))
print(out, out.replace(".png", "-later.png"))

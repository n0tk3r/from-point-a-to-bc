"""Draw the Forum's layout.json over its finished pictures, to look at (as the Rome painters' *_check.py do): the walk
(green), blocked ground (red), the cut-outs' patches (orange) and bases (magenta), every thing's shape (yellow) and
place to stand (a dot), and every mark with a figure's box at the size the game draws it there (blue).

    python3 rome_forum_check.py [folder]      (default out/rome-forum) -> out/rome-forum-check.png

The places are checked against the engine's own walk map by forum-walkcheck.mjs (in the painter's notes): this picture
is for the eye."""

import json
import sys

import numpy as np
from PIL import Image

from rome_forum_layout import check_layout

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "out/rome-forum"
    lay = json.load(open(f"{folder}/layout.json"))
    im = Image.open(f"{folder}/back.png").convert("RGBA")
    for p in lay["planes"]:
        if "file" in p:
            im.alpha_composite(Image.open(f"{folder}/{p['file']}").convert("RGBA"))
    whole = np.asarray(im.convert("RGB"), dtype=np.float32) / 255.0
    out = folder.rstrip("/") + "-check.png"
    check_layout(whole, lay, out)
    print(out)

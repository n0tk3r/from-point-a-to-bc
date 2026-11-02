"""Checks on the lock close-up as painted (out/edo-lock/) or as installed (art/scenes/edo-lock/), and the pictures to look
at. PAINT-21E.

  python3 edo_lock_check.py [out|art] [shots_dir]
      every file of the plan, sizes, hard edges, every thing of ROUND-21.md's list with a shape; then
      <shots_dir>/lock-states-<which>.png (the four steps of the puzzle side by side: shut; the ear cleaned and the wave
      slid; the coin on the post, turned, the slits open; the bolt drawn) and <shots_dir>/lock-hands-<which>.png (the
      three hand points, each with the line its hand comes in along, and a stand-in hand's reach at 22 px/cm)."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

from edo_town_check import check_files, HERE

NEEDED = ["rabbit", "ear", "earhole", "waves", "wave", "post", "back", "bolt", "hasp", "lattice"]


def comp(folder, names):
    im = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    for n in names:
        im.alpha_composite(Image.open(os.path.join(folder, n + ".png")).convert("RGBA"))
    return im


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "out"
    shots = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "out")
    folder = os.path.join(HERE, "out", "edo-lock") if which == "out" else os.path.join(HERE, "..", "..", "art", "scenes", "edo-lock")
    os.chdir(HERE)
    bad = check_files("edo-lock", folder)
    lay = json.load(open(os.path.join(folder, "layout.json")))
    ids = {t["id"] for t in lay["things"]}
    for t in NEEDED:
        if t not in ids:
            bad.append(f"thing {t} has no shape")
    for h in ("handEar", "handPost", "handComb"):
        if h not in lay.get("hands", {}):
            bad.append(f"hand point {h} missing")
    print("CHECK edo-lock", which, "OK" if not bad else "")
    for b in bad:
        print("  ", b)
    os.makedirs(shots, exist_ok=True)
    steps = [["wave", "ear", "bolt"], ["wave-slid", "ear-clean", "bolt"], ["wave-slid", "ear-clean", "post-turned", "back-open", "bolt"],
             ["wave-slid", "ear-clean", "post-turned", "back-open", "bolt-out"]]
    tiles = [comp(folder, s).convert("RGB").resize((400, 300), Image.LANCZOS) for s in steps]
    sheet = Image.new("RGB", (810, 610), (30, 30, 30))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 2) * 410, (i // 2) * 310))
    sheet.save(os.path.join(shots, f"lock-states-{which}.png"))
    im = comp(folder, ["wave-slid", "ear-clean", "post-coin", "back-open", "bolt"])
    d = ImageDraw.Draw(im, "RGBA")
    for name, h in lay["hands"].items():
        x, y = h["at"]
        fx, fy = h["from"]
        d.line([(fx, fy), (x, y)], fill=(255, 255, 255, 140), width=26)            # a stand-in forearm and hand, 26 px wide
        d.ellipse([x - 6, y - 6, x + 6, y + 6], outline=(255, 0, 255, 255), width=2)
        d.text((x + 8, y - 16), name, fill=(255, 255, 255, 255))
    for t in lay["things"]:
        d.polygon([tuple(p) for p in t["shape"]["poly"]], outline=(255, 200, 0, 150))
    im.convert("RGB").save(os.path.join(shots, f"lock-hands-{which}.png"))
    print("pictures written")

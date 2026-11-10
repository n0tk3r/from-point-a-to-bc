#!/usr/bin/env python3
"""The depth pass over Grandma Jolene's store (scene `nevada-store`, round twenty-three: DEPTH.md).

    python3 nevada_store_depth.py          reads out/nevada-store-orig/ (the seeded full run, never changed) and writes
                                           the scene's whole set back into out/nevada-store/, every file as before
                                           plus near.png

THE NEAR PLANE (near.png, plane "front"): what stands by the lens just inside the front door, in warm shade, lit only on
the edges toward the window (the sun, low behind us on the left) and from below by the sunlit floor:
  - the ceiling beam across the top of the frame, sagging a little;
  - a hanging rack from it at the top left: a souvenir blanket down the very left edge (above the front door) and a row
    of bandanas over the hubcaps;
  - at the right edge, the end of a tall shelf unit (its upright and its kick plate along the bottom), and a hanging rack
    of shirts in front of it, over the side wall and clear of the pay phone, the chair and the rock bins.
The old front plane (front.png: the water flats, the crate of empties, the tyre) is made to count: darker and warmer, in
the same outline.

THE BACK (back.png): the far wall a little cooler and paler (air), the near floor deeper and warmer, a large soft shadow
of the front wall's pier (outside the picture, behind us on the left) lying across the foreground with its edge leading
in toward the counter, a cool spill of the yard's light from the back door, and worn scuffs on the tiles that shrink
toward the far wall. Nothing clicked is moved or redrawn. Every other file is copied byte for byte."""

import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import F32, Sheet, rgb, lerp, blur, noise, grid, mask_poly
import depth
from nevada_store import finish

SRC = os.environ.get("DEPTH_SRC", "out/nevada-store-orig")
OUT = os.environ.get("DEPTH_OUT", "out/nevada-store")
H, W = 600, 800
SHADE = "#1c0e08"                       # the near plane's dark: frankly warm (keying turns warm darks violet)


def load(name):
    im = Image.open(f"{SRC}/{name}").convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def nt(c, k=0.62, warm=0.04):
    return depth.near_tone(c, shade=SHADE, k=min(k + 0.16, 0.92), warm=warm)


# ---------------------------------------------------------------- the near plane
def near_plane():
    x, y = grid((H, W))
    sh = Sheet((H, W), ss=3)

    # the beam across the top: its underside sags a little; the lens sees its face in shade
    beam = [(-4, -4), (804, -4), (804, 27)] + [(px, 27 + (38 - 27) * (1 - px / 800) + 4 * np.sin(np.pi * px / 800)) for px in range(780, -1, -20)] + [(-4, 39)]
    sh.poly(beam, nt("#7a5236", 0.66))

    # the left rack: two cords from the beam, a pole, and what hangs from it
    sh.line([(26, 30), (24, 60)], nt("#8a6a48", 0.5), 2.2)
    sh.line([(192, 30), (190, 60)], nt("#8a6a48", 0.5), 2.2)
    # bandanas over the hubcaps (they overlap: no holes of light between them), each bottom a point or a ragged hem
    hems = [(52, 98, "#b83a2a"), (82, 92, "#2f4f7a"), (110, 100, "#c08a34"), (138, 90, "#b83a2a"), (166, 97, "#3c6a64"), (196, 88, "#7a3a5a")]
    left = 46
    for i, (right, bottom, col) in enumerate(hems):
        mid = (left + right) / 2
        sh.poly([(left - 3, 60), (right + 3, 60), (right + 1, bottom - 10), (mid + 2, bottom), (left + 1, bottom - 8)], nt(col, 0.6))
        left = right - 4
    # the blanket down the very left edge, above the front door: striped, its hem fringed
    sh.poly([(-4, 58), (56, 58), (54, 226), (44, 232), (30, 228), (16, 236), (-4, 232)], nt("#a8442c", 0.6))
    for yy, col in ((92, "#d2a24a"), (100, "#2f5a6a"), (170, "#d2a24a"), (178, "#2f5a6a"), (206, "#d2a24a")):
        sh.poly([(-4, yy), (55, yy - 1), (55, yy + 5), (-4, yy + 6)], nt(col, 0.6))
    sh.line([(-6, 60), (214, 57)], nt("#6a4a30", 0.55), 4.0)          # the pole

    # the right: the end of a tall shelf unit, its upright off the right edge, its kick plate along the bottom
    sh.poly([(786, -4), (804, -4), (804, 604), (787, 604)], nt("#8a5a3a", 0.64))
    sh.poly([(714, 532), (787, 524), (804, 523), (804, 604), (708, 604)], nt("#8a5a3a", 0.66))
    sh.poly([(714, 532), (787, 524), (788, 529), (716, 537)], nt("#c08a5a", 0.45))          # the kick plate's top edge
    # the shirts on a rack hung from the beam, in front of the upright
    sh.line([(752, 28), (752, 56)], nt("#8a6a48", 0.5), 2.0)
    shirts = [(738, 772, 336, "#c8b48a"), (752, 790, 356, "#3c6a8a"), (768, 806, 322, "#b04a32")]
    for x0, x1, bottom, col in shirts:
        sh.poly([(x0 + 6, 58), (x1 - 6, 58), (x1, 76), (x1 - 2, bottom - 6), (x1 - 8, bottom), (x0 + 4, bottom - 3), (x0, 78)], nt(col, 0.6))
    sh.line([(732, 58), (806, 56)], nt("#6a4a30", 0.55), 4.0)

    col, a = sh.done()
    # inside: the weave and the grain, and a slow fall of light from the top (the beam is darkest)
    n = noise((H, W), 9, 41, octaves=3)
    col = col * (0.92 + 0.12 * n[..., None])
    col = col * (0.94 + 0.08 * np.clip(y / 300.0, 0, 1))[..., None]
    # rims: the window's sun from the left, warm; the sunlit floor's bounce from below, weaker
    r_sun = depth.rim(a, light=(-1.0, -0.25), width=2.0)
    r_up = depth.rim(a, light=(-0.3, 1.0), width=2.0)
    col = lerp(col, rgb("#d89464")[None, None, :], (np.clip(r_sun, 0, 1) * 0.42)[..., None])
    col = lerp(col, rgb("#a8704a")[None, None, :], (np.clip(r_up, 0, 1) * 0.22)[..., None])
    return np.clip(col, 0, 1).astype(F32), a


# ---------------------------------------------------------------- the back
def deepen(pic):
    x, y = grid((H, W))
    # the far wall, cooler and paler (only the wall: the counter, the cooler and the door's frame are cut-outs over it)
    wall = mask_poly((H, W), [(214, 96), (722, 90), (722, 384), (560, 374), (214, 360)], soft=5.0)
    depth.air(pic, np.ones((H, W), F32), "#c6d6da", amount=0.13, mask=wall)
    # the floor: deeper and warmer toward us
    floor = mask_poly((H, W), [(0, 488), (214, 360), (722, 384), (804, 474), (804, 604), (-4, 604)], soft=3.0)
    t = np.clip((y - 420) / 180.0, 0, 1) ** 1.3 * floor
    pic *= (1 - 0.26 * t)[..., None]
    pic[..., 0] += 0.025 * t
    pic[..., 2] -= 0.015 * t
    # the pier of the front wall, behind us on the left, throws its shadow across the foreground: the edge leads in
    shadow = mask_poly((H, W), [(-4, 466), (180, 512), (420, 568), (566, 604), (-4, 604)], soft=10.0, wobble=2.0, seed=7)
    shadow = blur(shadow, 4.0) * floor
    pic[...] = pic * (1 - 0.24 * shadow[..., None]) + rgb("#3a3050") * (0.06 * shadow[..., None])
    # the yard's cool light in through the back door, spilling on the floor toward us
    spill = blur(mask_poly((H, W), [(592, 384), (684, 388), (752, 468), (566, 456)], soft=8.0), 8.0) * floor
    pic[...] = lerp(pic, rgb("#dfe8ee")[None, None, :], (0.10 * spill)[..., None])
    # scuffs and worn joints on the tiles, bigger and fewer near us
    n = noise((H, W), 3.5, 77, octaves=3)
    m = np.clip((n - 0.62) * 5.0, 0, 1) * floor * (0.35 + 0.65 * np.clip((y - 360) / 240.0, 0, 1))
    pic *= (1 - 0.10 * m)[..., None]
    return np.clip(pic, 0, 1).astype(F32)


def main():
    os.makedirs(OUT, exist_ok=True)
    names = sorted(os.listdir(SRC))
    for f in names:                                   # everything as it was (the cut-outs, the frames, layout.json, hens.json)
        if f != "near.png":
            shutil.copy2(f"{SRC}/{f}", f"{OUT}/{f}")
    back, _ = load("back.png")
    back = deepen(back)
    finish(back, f"{OUT}/back.png", 160)
    # the old front plane, made to count: darker and warmer, in its own outline
    fc, fa = load("front.png")
    fc = lerp(fc, rgb(SHADE)[None, None, :], 0.30)
    fc[..., 0] = np.clip(fc[..., 0] + 0.03, 0, 1)
    fr = depth.rim(fa, light=(-1.0, -0.25), width=2.0)
    fc = lerp(fc, rgb("#f0a860")[None, None, :], (fr * 0.35)[..., None])
    finish(np.clip(fc, 0, 1), f"{OUT}/front.png", 72, (fa > 0.5).astype(F32) * fa)
    col, a = near_plane()
    a = np.where(a > 0.5, 1.0, 0.0).astype(F32)       # a clean outline (the game keys it on alpha)
    finish(col, f"{OUT}/near.png", 64, a)
    print("near.png", round(float(a.mean()) * 100, 1), "% of the picture; front.png", round(float((fa > 0.5).mean()) * 100, 1), "%")


if __name__ == "__main__":
    main()

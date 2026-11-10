"""The living room's depth pass (round twenty-three): worked over the painting as it is.

    python3 home_living_room.py            first, once: the painting as installed, into out/home-living-room/
    (copied, untouched, to out/home-living-room-orig/)
    python3 home_living_room_depth.py      reads out/home-living-room-orig/, writes the full set back to out/home-living-room/

NEAR. The near plane was the armchair (front left) and the table (front right): both on the bottom edge only. What
was missing is a near edge up a second side: a square timber post of the dining end's opening, 2 m from the lens on
our right, from the top of the picture to the bottom (through the room's own camera, room.View: verticals stay
vertical, its side face runs back to the room's vanishing point). Its face toward us is in deep, warm shade; the
pendant behind it, over the table, catches its side face and its corner (the rim). The armchair and the table are
made to count: darker and warmer toward the frame, their lit cloth, lampshade, crossword and Bible kept as they were,
and a warm rim on the side of their lamp.

BACK. The lamps' pools made plainer (the reading lamp's on the floor, the pendant's round the table, the piano lamp's
and the upstairs lamp's on the wall); the far wall and the gallery a little cooler and paler (the room's air), the
lower back wall less so; the near floor deeper and warmer toward us. Nothing clicked is moved or redrawn.
"""
import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import F32, rgb, lerp, blur, mask_poly, mask_ellipse, noise, palette_of, to_palette, save, grain, Sheet, over
import depth
import home_living_room_model as M
from room import View

ID = M.ID
SRC, OUT = (sys.argv[1:3] + [None, None])[:2] if len(sys.argv) > 2 else (f"out/{ID}-orig", f"out/{ID}")      # (a trial: SRC OUT)
W, H = 800, 600
V = View(**M.VIEW)
Y, X = np.mgrid[0:H, 0:W].astype(F32)


def load(name):
    a = np.asarray(Image.open(f"{SRC}/{name}").convert("RGBA"), dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def lum(c):
    return c[..., 0] * 0.3 + c[..., 1] * 0.59 + c[..., 2] * 0.11


def finish(pic, name, colors, alpha=None, amount=0.006, speckle=0.007, seed=7):
    g = grain(pic, seed, amount) if amount else np.clip(pic, 0, 1)
    sample = g if alpha is None else g[alpha > 0.5]
    n = min(colors, max(2, len(np.unique((sample * 255).astype(np.uint8).reshape(-1, 3), axis=0))))
    pal = palette_of([sample.reshape(-1, 1, 3)], colors=n)
    save(f"{OUT}/{name}", to_palette(g, pal, speckle=speckle), pal, alpha)
    return os.path.getsize(f"{OUT}/{name}")


def light(pic, m, gain, warm=(1.0, 0.78, 0.48)):
    """Lamp light laid on: the picture multiplied up, warm, through the soft mask m."""
    pic *= 1.0 + (m * gain)[..., None] * np.asarray(warm, F32)


def floor_pool(X0, Z0, r, soft):
    pts = [(X0 + r * np.cos(t), 0.0, Z0 + r * np.sin(t)) for t in np.linspace(0, 2 * np.pi, 40, endpoint=False)]
    poly = [(float(x), float(y)) for x, y in V.poly(pts)]
    m = mask_poly((H, W), poly, soft=0)
    return blur(m, soft)


def poly_mask(points, soft=2.0):
    return blur(mask_poly((H, W), points, soft=0), soft)


# ---------------------------------------------------------------- the backdrop
def deepen_back(back):
    pic = back.copy()
    # the far wall and the gallery: cooler and paler (the room's air, toward the moon's pale blue)
    upper = poly_mask([(276, -5), (805, -5), (805, 192), (755, 190), (276, 182)], 5.0)
    stairwall = poly_mask([(-5, -5), (276, -5), (276, 182), (-5, 300)], 5.0) * np.clip(X / 276.0, 0, 1) ** 1.6 * 0.7
    lower = poly_mask([(276, 182), (755, 190), (730, 367), (276, 326)], 4.0) * 0.38
    rightwall = poly_mask([(730, 190), (805, 192), (805, 420), (730, 367)], 4.0) * 0.45
    far = np.clip(upper + stairwall + lower + rightwall, 0, 1)
    keep_lit = 1.0 - np.clip((lum(pic) - 0.62) / 0.25, 0, 1) * 0.6          # the lamps themselves keep their heat
    depth.air(pic, far, "#9aa7c0", amount=0.09, mask=keep_lit)

    # the near floor deeper and warmer toward us
    t = np.clip((Y - 330.0) / 270.0, 0, 1) ** 1.05
    pic *= 1.0 - t[..., None] * np.asarray((0.29, 0.35, 0.41), F32)

    # the lamps' pools
    light(pic, floor_pool(234, 735, 120, 14) * 0.9, 0.26)                     # the reading lamp, on the floor round it
    light(pic, floor_pool(600, 686, 175, 16), 0.16)                           # the pendant, on the floor round the table
    light(pic, blur(mask_ellipse((H, W), 618, 236, 62, 52), 16), 0.20)      # the piano lamp, on the wall over it
    light(pic, blur(mask_ellipse((H, W), 561, 108, 66, 46), 16), 0.20)      # the lamp upstairs, on the gallery wall
    return np.clip(pic, 0, 1)


# ---------------------------------------------------------------- the near cut-outs, made to count
CROSSWORD = [(180, 534), (226, 516), (236, 529), (234, 540), (192, 551)]
BIBLE = [(523, 456), (577, 461), (573, 484), (520, 478)]


def deepen_cut(c, a, k, keep, light_dir, rim_gain):
    """Darker and warmer by k (a map), except where `keep` (a map) says; then a warm rim toward the lamp."""
    out = c.copy()
    bright = np.clip((lum(c) - 0.55) / 0.3, 0, 1)                              # lit cloth, paper, shades stay lit
    kk = (k * (1.0 - bright) * (1.0 - keep))[..., None]
    deep = np.empty_like(c)
    for i in range(3):
        deep[..., i] = c[..., i] * 0.5 + rgb("#2a1a20")[i] * 0.5
    deep[..., 0] = np.minimum(deep[..., 0] + 0.07, 1.0)
    out = out * (1 - kk) + deep * kk
    r = depth.rim(a, light=light_dir, width=2.2) * (1.0 - keep)
    light(out, r, rim_gain, warm=(1.0, 0.70, 0.36))
    return np.clip(out, 0, 1)


# ---------------------------------------------------------------- the near post
def near_post():
    """A square timber post, 18 cm, 2 m from the lens on our right: from the top of the picture to the bottom."""
    s = 18.0
    best = None
    for zc in np.arange(880.0, 1000.0, 1.0):                                   # its far left edge on x = 757
        xc = 620.0 + (1150.0 - zc) * 0.23
        x_far = V.pt(xc - s / 2, V.eye, zc - s / 2)[0]
        if best is None or abs(x_far - 757) < abs(best[2] - 757):
            best = (xc, zc, x_far)
    xc, zc, _ = best
    X0, X1, Z0, Z1 = xc - s / 2, xc + s / 2, zc - s / 2, zc + s / 2
    xf = V.pt(X0, V.eye, Z0)[0]                                                  # side face: far edge
    xn = V.pt(X0, V.eye, Z1)[0]                                                  # the near corner
    xr = V.pt(X1, V.eye, Z1)[0]                                                  # front face: right edge (off the frame)
    print("post at", round(xc), round(zc), "edges", round(xf, 1), round(xn, 1), round(xr, 1))

    front = depth.near_tone(rgb("#5a3420"), k=0.50, shade="#1a0f0c", warm=0.03)   # stained timber, in deep warm shade
    side = depth.near_tone(rgb("#7a4a2a"), k=0.45, shade="#1a0f0c", warm=0.04)
    sh = Sheet((H, W), ss=4)
    sh.poly([(xn, -2), (W + 4, -2), (W + 4, H + 2), (xn, H + 2)], front)
    sh.poly([(xf, -2), (xn, -2), (xn, H + 2), (xf, H + 2)], side)
    c, a = sh.done()
    # the grain of the timber, running up and down; the side face lit more toward the lamp's height
    g = noise((H, W), 9.0, 41, octaves=3)
    streak = blur(np.random.default_rng(41).normal(0, 1, (H, W)).astype(F32), 0.6)
    streak = np.asarray(Image.fromarray(((streak - streak.min()) / (np.ptp(streak) + 1e-6) * 255).astype(np.uint8)).resize((W, H // 24)).resize((W, H), Image.BICUBIC), dtype=F32) / 255
    c *= (0.92 + 0.10 * g + 0.10 * (streak - 0.5))[..., None]
    on_side = ((X >= xf - 0.5) & (X < xn)).astype(F32)
    lamp = np.exp(-((Y - 405.0) / 230.0) ** 2)                                  # the pendant's height (y 405)
    light(c, on_side * (0.15 + 0.85 * lamp), 0.45, warm=(1.0, 0.70, 0.38))
    # the panel moulding on the face toward us: two dark grooves and a lit lip
    for gx, col, al in ((xn + 7.0, "#120a0a", 0.7), (xn + 8.2, "#7a4a2c", 0.30)):
        ln = Sheet((H, W), ss=4)
        ln.line([(gx, -2), (gx, H + 2)], col, 1.0, al)
        lc, la = ln.done()
        over(c, lc, la)
    # the rim: the near corner catches the pendant
    corner = np.clip(1.0 - np.abs(X - xn) / 1.6, 0, 1) * (0.35 + 0.65 * lamp)
    light(c, corner, 1.6, warm=(1.0, 0.74, 0.42))
    a = np.where(X >= xf, a, 0).astype(F32)
    return np.clip(c, 0, 1), a


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back.png")
    print("back", finish(deepen_back(back), "back.png", 156))

    ac, aa = load("armchair.png")
    keep = poly_mask(CROSSWORD, 3.0)
    k = 0.18 + 0.20 * np.clip((Y - 470.0) / 130.0, 0, 1)
    print("armchair", finish(deepen_cut(ac, aa, k, keep, (-1.0, -0.7), 0.55), "armchair.png", 80, aa))

    tc, ta = load("table.png")
    keep = poly_mask(BIBLE, 3.0)
    k = 0.28 * np.clip((Y - 470.0) / 130.0, 0, 1) ** 0.9
    print("table", finish(deepen_cut(tc, ta, k, keep, (-0.45, -1.0), 0.45), "table.png", 96, ta))

    nc, na = near_post()
    print("near", finish(nc, "near.png", 40, na, amount=0.014, speckle=0.011), "share", round(float((na > 0.5).mean()) * 100, 1), "%")

    for name in ("piano.png", "piano-open.png", "pencil.png", "layout.json"):
        shutil.copyfile(f"{SRC}/{name}", f"{OUT}/{name}")
    print("done")

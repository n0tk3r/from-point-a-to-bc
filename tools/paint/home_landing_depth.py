"""home-landing, the fast depth pass (round twenty-three): over the painting as it is (out/home-landing-orig/).

THE NEAR PLANE (near.png): what stands by the lens out here in the air over the living room, in deep warm dark:
  * the summer beam of the living-room ceiling, the one nearest us, across the top of the frame: it runs along the
    landing, so its edges go to the far vanishing point (-267, 135) (deep on the left, thin on the right); its face
    toward us in shade, its underside catching the hanging light's warm glow from below, a warm arris between them;
  * the stair's bottom newel post, close to us at the frame's left and bottom edges, where the banister ends: white
    paint in deep shade, lit on its right by the hanging light.
  The railing cut-out (rail.png: the landing's rail, the banister, the quilt, the hanging light) is made to count:
  the banister's lower run, nearest us, goes darker and warmer toward the frame's corner.
THE BACK (back.png): the far wall of the landing a little cooler and paler (not in the hall lamp's pool); the lamps'
  pools (the hall table's lamp, the piano's lamp, the hanging light's pool on the floor below it, the kitchen doorway);
  one large shadow leading in from under us (Dad's armchair, out of the picture, against the pendant over the dinner
  table behind us: it falls away from us, up and to the left); the floor below falling into warm dark toward us.
Nothing clicked is moved or redrawn. The ladder and the open study door are copied over as they were.

    python3 home_landing_depth.py            -> out/home-landing/ (back, ladder, rail, study-open, near, layout.json)
"""

import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import *
import depth as D

SRC = "out/home-landing-orig"
OUT = "out/home-landing"
H, W = 600, 800
SHAPE = (H, W)
VPL = (-267.0, 135.0)          # lines along the landing (and the beam) run here
SEED = 23


def load_rgba(path):
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im, dtype=np.float32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def to_vp(x0, y0, x):
    """y at x on the line from (x0, y0) toward the far vanishing point."""
    return y0 + (x - x0) * (VPL[1] - y0) / (VPL[0] - x0)


def beam_y(x, y_right):
    return to_vp(800.0, y_right, x)


def near_plane():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # ---- the beam: face toward us (top of frame down to the arris), underside (arris to its far bottom edge)
    arris = beam_y(xx, 16.0)
    far_edge = beam_y(xx, 29.0)
    face = np.clip((arris - yy) + 0.5, 0, 1)
    under = np.clip((far_edge - yy) + 0.5, 0, 1) * (1 - face)
    wood = rgb("#6a4428")
    deep = D.near_tone(wood, shade="#1a110c", k=0.86, warm=0.02)
    # along its length: the grain runs to the vanishing point (stripes in the distance from the arris)
    t = (arris - yy)                                           # pixels above the arris
    streak = noise(SHAPE, 6, SEED, octaves=3)
    grainline = 0.5 + 0.5 * np.sin(t * 0.55 + 3.0 * streak + xx * 0.004)
    fc = deep[None, None, :] * (0.86 + 0.16 * grainline[..., None] + 0.08 * (noise(SHAPE, 30, SEED + 1)[..., None] - 0.5))
    # a little warm bounce on the face's lower part, from the room below
    bounce = np.clip(1 - t / 26.0, 0, 1) ** 2
    fc = fc + rgb("#5a3418")[None, None, :] * 0.22 * bounce[..., None]
    # the underside: lit warm from below, most toward the hanging light (x 262)
    glow_u = np.exp(-((xx - 262) / 260.0) ** 2)
    uc = lerp(deep, rgb("#8a5a30"), 0.28)[None, None, :] * (0.85 + 0.35 * glow_u[..., None]) * (0.92 + 0.12 * streak[..., None])
    col = fc * face[..., None] + uc * under[..., None]
    alpha = np.clip(face + under, 0, 1)
    # the warm arris (the lit rim between the face and the underside)
    ar = np.clip(1 - np.abs(yy - arris) / 1.1, 0, 1) * (0.55 + 0.45 * glow_u)
    col = lerp(col, np.broadcast_to(rgb("#c08a4c"), col.shape), (ar * 0.55)[..., None])
    # ---- the bottom newel post, close by at the left: white paint in deep shade, lit on its right
    s = Sheet(SHAPE)
    white_sh = D.near_tone("#e6d8c0", shade="#1e140f", k=0.85, warm=0.04)
    white_mid = D.near_tone("#e6d8c0", shade="#1e140f", k=0.74, warm=0.05)
    s.poly([(-4, 486), (30, 486), (30, 601), (-4, 601)], white_sh)               # the shaft
    s.poly([(22, 486), (30, 486), (30, 601), (22, 601)], white_mid)               # its right face, toward the light
    s.poly([(-4, 474), (35, 474), (38, 480), (38, 488), (-4, 488)], white_mid)    # the cap
    s.poly([(-4, 470), (33, 470), (35, 474), (-4, 474)], white_sh)                # the cap's top edge
    s.ellipse(13, 459, 12, 11, white_sh)                                         # the ball on top
    s.ellipse(13, 470, 7, 3, white_sh)
    s.poly([(-4, 520), (30, 520), (30, 524), (-4, 524)], D.near_tone("#e6d8c0", shade="#1e140f", k=0.9, warm=0.03))   # a moulding
    nc, na = s.done()
    nrim = D.rim(na, light=(1.0, -0.6), width=2.0)
    nc = lerp(nc, np.broadcast_to(rgb("#d8a466"), nc.shape), (np.clip(nrim * 1.6, 0, 1) * 0.6)[..., None])
    col = col * (1 - na[..., None]) + nc * na[..., None]
    alpha = np.maximum(alpha, na)
    col = np.clip(col, 0, 1).astype(np.float32)
    return col, alpha.astype(np.float32)


def deepen_rail(rc, ra):
    """The railing cut-out, made to count: the banister's lower run, nearest us, darker and warmer toward the corner."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    stair = mask_poly(SHAPE, [(0, 470), (0, 601), (60, 601), (330, 300), (330, 180), (300, 180)], soft=8)   # the banister's run
    near = stair * (0.62 + 0.36 * np.clip((yy - 200) / 330.0, 0, 1))                 # deeper toward the bottom-left
    hang = mask_poly(SHAPE, [(195, 320), (325, 320), (325, 432), (195, 432)], soft=4)   # the hanging light's brass
    landing = (1 - stair) * (1 - hang) * 0.52                                          # the landing's railing, under the lamp
    lum = rc @ np.array([0.3, 0.59, 0.11], dtype=np.float32)
    lit = np.clip((lum - 0.72) / 0.18, 0, 1) * hang            # (the hanging light's lit shades stay lit)
    k = (np.maximum(np.maximum(near, landing), 0.5 * hang) * (1 - lit))[..., None]
    out = lerp(rc, rc * np.array([0.50, 0.40, 0.33], dtype=np.float32), k)
    return np.clip(out, 0, 1).astype(np.float32)


def deepen_back(b):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    out = b.copy()
    # ---- the lamps' pools: where each light falls (screened in, soft)
    def pool(cx, cy, rx, ry, color, amt):
        m = np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2))
        return m * amt, rgb(color)
    pools = [pool(622, 205, 130, 85, "#ffc070", 0.24),        # the hall table's lamp, on the landing
             pool(692, 420, 115, 95, "#ffb860", 0.24),        # the piano's lamp
             pool(270, 520, 150, 55, "#f0a858", 0.16),        # the hanging light's pool on the floor below it
             pool(505, 430, 70, 90, "#ffd28a", 0.12)]         # the kitchen doorway
    lampmask = np.zeros(SHAPE, np.float32)
    for m, c in pools:
        out = 1 - (1 - out) * (1 - c[None, None, :] * m[..., None])
        lampmask = np.maximum(lampmask, m)
    # ---- the far wall of the landing a little cooler and paler, out of the hall lamp's pool
    far = mask_poly(SHAPE, [(300, 92), (800, 52), (800, 300), (300, 262)], soft=6)
    far = far * np.clip(1 - lampmask / 0.12, 0, 1)
    out = D.air(out, far.astype(np.float32), rgb("#8a9cb4"), amount=0.16)
    # ---- one large shadow leading in from under us: Dad's armchair against the pendant behind us
    sh = mask_poly(SHAPE, [(395, 601), (660, 601), (560, 545), (430, 500), (360, 505), (330, 540)], soft=14, wobble=4, seed=SEED)
    sh = blur(sh, 6) * np.clip((yy - 470) / 60.0, 0, 1)
    out = out * (1 - (0.38 * sh)[..., None] * (1 - rgb("#3a2418")[None, None, :]))
    # ---- the floor below falling into warm dark toward us and the corners
    down = np.clip((yy - 430) / 170.0, 0, 1) ** 1.3
    side = np.clip(np.abs(xx - 330) / 470.0, 0, 1) ** 2
    dark = np.clip(0.30 * down + 0.18 * side * np.clip((yy - 330) / 270.0, 0, 1), 0, 0.45)
    dark = dark * (1 - np.clip(lampmask / 0.16, 0, 1) * 0.6)
    out = lerp(out, out * rgb("#6a4a34")[None, None, :], dark[..., None])
    return np.clip(out, 0, 1).astype(np.float32)


def finish(picture, path, colors, alpha=None, speckle=0.010, amount=0.012, seed=7):
    g = picture if amount == 0 else np.clip(picture + (grain(picture, seed, amount) - picture) * 0.8, 0, 1)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=colors)
    idx = to_palette(g, pal, speckle=speckle)
    save(path, idx, pal, alpha)
    return len(pal)


def main():
    src = SRC
    out = OUT
    if "--dev" in sys.argv:                       # (a preview from the installed, keyed art: never installed)
        src, out = "../../art/scenes/home-landing", "out/home-landing-dev"
    os.makedirs(out, exist_ok=True)
    back, _ = load_rgba(f"{src}/back.png")
    nb = deepen_back(back)
    print("back", finish(nb, f"{out}/back.png", 160, amount=0))
    rc, ra = load_rgba(f"{src}/rail.png")
    print("rail", finish(deepen_rail(rc, ra), f"{out}/rail.png", 64, (ra > 0.5).astype(np.float32), speckle=0.006, amount=0))
    for n in ("ladder.png", "study-open.png", "layout.json"):
        if os.path.abspath(src) != os.path.abspath(out):
            shutil.copy(f"{src}/{n}", f"{out}/{n}")
    col, a = near_plane()
    print("near", finish(col, f"{out}/near.png", 40, a, speckle=0.006, amount=0.010))
    print("near share", round(float((a > 0.5).mean()) * 100, 1))
    # everything together, to look at
    im = Image.open(f"{out}/back.png").convert("RGBA")
    for n in ("ladder", "rail", "near"):
        im.alpha_composite(Image.open(f"{out}/{n}.png").convert("RGBA"))
    im.convert("RGB").save(f"out/home-landing-depth-comp{'-dev' if '--dev' in sys.argv else ''}.png")


if __name__ == "__main__":
    main()

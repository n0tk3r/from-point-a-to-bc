"""ROUND-23 (the fast depth pass, LITE.md): the ship's clock (edo-compass) with depth, worked over its painting.

edo_compass.py's full run, copied untouched to out/edo-compass-orig/, is read here and the scene's set written back into
out/edo-compass/ (every file as before, plus near.png):

    near.png    the front plane: the edge of the box's surroundings close to the lens and out of focus: the deck's planks
                at the frame's left and right, the propped lid's near (free) edge across the top, in deep warm shade,
                darker toward the frame; a soft warm rim where the right-hand edge faces the sun (behind us, a little left)
    back.png    deepened: the lid's shadow on the deck (the lid's top is out of the picture: the shadow comes in from the
                top edge and runs down into the box's own), both shadows the same way (+46, -58 per box height), a little
                deeper and cooler; the deck's planks textured (treenails, knots, grain, salt bloom), a breath of noon
                haze over the deck far below; the box's near board deeper toward the lens
    thumb.png   washed on the same paper (wash_cut, crisp)
    needle*.png as they were (the needle is kept out of the wash: the card, the needle and the bow mark are the puzzle)

JAPAN: watercolor.wash(seed 1830, wander 1.4, fleck 0.3) with `keep` over the card and the bow mark; WET 0.25 on the deck
far below the box (out of the focal plane), 0 for the box, the lid and the card.

    python3 edo_compass_depth.py
"""

import os
import shutil

import numpy as np
from PIL import Image

import depth
import watercolor
from brush import F32, blur, grid, lerp, mask_poly, rgb, step, grain, palette_of, to_palette, save
from edo_deck_kit import OCHRE, NAPLES, COBALT, PRUSSIAN, SIENNA, CERULEAN, WHITE, tintw
from edo_compass import box_quad, BOX_FAR, C, R_CARD, SQ, polar

ORIG = "out/edo-compass-orig"
OUT = "out/edo-compass"
SEED = 1830
W, H = 800, 600
SHAPE = (H, W)
SUN_OFF = np.array([46.0, -58.0])          # where a point at the box's top falls on the deck (edo_compass.py's shadow)
TO_LIGHT = (-0.62, 0.78)                   # the direction to the sun in the picture (behind us, a little left)
SHADE = rgb("#2b1b12")                     # the near plane's shade: a frankly warm deep brown (the key turns warm darks violet)


def load(name):
    im = Image.open(os.path.join(ORIG, name)).convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255.0
    return a[..., :3].copy(), a[..., 3].copy()


def smooth(e0, e1, v):
    t = np.clip((v - e0) / (e1 - e0), 0, 1)
    return (t * t * (3 - 2 * t)).astype(F32)


# ================================================================ where things are
fx0, fx1, fy = BOX_FAR
LID = [(fx0 + 4, fy + 2), (fx1 - 4, fy + 2), (fx1 - 30, -12), (fx0 + 30, -12)]
BOX = box_quad(0)
X, Y = grid(SHAPE)
standing = np.maximum(mask_poly(SHAPE, BOX, soft=0.6), mask_poly(SHAPE, LID, soft=0.6))
DECK = np.clip(1 - blur(standing, 0.8) * 1.15, 0, 1).astype(F32)            # the deck far below, at the stage's sides
DECK_HARD = (DECK > 0.98).astype(F32)


def keep_mask():
    """The puzzle stays as painted: the card (its twelve marks and Kota's animals) and the bow mark."""
    rx, ry = R_CARD + 3.0, (R_CARD + 3.0) * SQ
    d = np.sqrt(((X - C[0]) / rx) ** 2 + ((Y - C[1]) / ry) ** 2)
    card = 1 - smooth(0.985, 1.02, d)
    bx, by = polar(R_CARD + 24, 0)
    bow = (1 - smooth(16, 22, np.abs(X - bx))) * (1 - smooth(18, 24, np.abs(Y - by)))
    return np.maximum(card, bow).astype(F32)


# ================================================================ the back, deepened
def dab(m, cx, cy, rx, ry, v=1.0):
    """An anti-aliased ellipse into the mask m (max)."""
    x0, x1 = int(max(cx - rx - 2, 0)), int(min(cx + rx + 3, W))
    y0, y1 = int(max(cy - ry - 2, 0)), int(min(cy + ry + 3, H))
    if x0 >= x1 or y0 >= y1:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(F32)
    d = np.sqrt(((xx + 0.5 - cx) / max(rx, 0.3)) ** 2 + ((yy + 0.5 - cy) / max(ry, 0.3)) ** 2)
    a = np.clip((1.0 - d) * max(rx, ry) + 0.5, 0, 1) * v
    m[y0:y1, x0:x1] = np.maximum(m[y0:y1, x0:x1], a)


def deck_texture(seed):
    """The planks' marks, through the view from above (a breath larger toward us, at the bottom): treenails in pairs,
    knots, grain streaks, a bloom of salt."""
    rng = np.random.default_rng(seed)
    dark = np.zeros(SHAPE, F32)
    pale = np.zeros(SHAPE, F32)
    for r_ in np.arange(-6.0, 610.0, 15.5):                       # the planks (edo_compass.paint_deck_below's rows)
        for x_ in np.arange(rng.uniform(-60, 20), 820, rng.uniform(60, 120)):
            s = 1.0 + 0.18 * (r_ / 600)
            y_mid = r_ + 7.75 + 2 * x_ / 808
            kind = rng.uniform()
            if kind < 0.45:                                       # treenails, a pair across the plank
                for dy in (-3.6, 3.6):
                    dab(dark, x_, y_mid + dy * s, 1.15 * s, 1.0 * s, 0.75)
            elif kind < 0.62:                                     # a knot with its pale ring
                rx, ry = rng.uniform(2.5, 4.5) * s, rng.uniform(1.3, 2.2) * s
                dab(pale, x_, y_mid, rx + 2.0, ry + 1.2, 0.55)
                dab(dark, x_, y_mid, rx, ry, 0.8)
            elif kind < 0.92:                                     # a streak of grain along the plank
                L = rng.uniform(20, 60) * s
                yy = y_mid + rng.uniform(-4.5, 4.5)
                tgt = dark if rng.uniform() < 0.6 else pale
                for t in np.linspace(0, 1, int(L / 1.5)):
                    dab(tgt, x_ + t * L, yy + 0.6 * np.sin(t * 6), 0.9, 0.45, 0.45 * (1 - abs(2 * t - 1)) + 0.15)
    bloom = blur(rng.normal(0, 1, (H // 8, W // 8)).astype(F32), 2.0)
    bloom = np.asarray(Image.fromarray(bloom).resize((W, H), Image.BILINEAR), dtype=F32)
    bloom = np.clip((bloom - 0.25) * 2.5, 0, 1)
    return blur(dark, 0.4), blur(pale, 0.5), bloom


def deepen(back):
    b = back.copy()
    # the old shadow of the box on the deck, and its colour against the lit planks
    old = mask_poly(SHAPE, [(p[0] + SUN_OFF[0], p[1] + SUN_OFF[1]) for p in box_quad(-6)], soft=0.6) * DECK
    lit_px = b[(old < 0.02) & (DECK_HARD > 0.5) & (X > 600)]
    sh_px = b[(old > 0.98) & (DECK_HARD > 0.5)]
    ratio = np.clip(np.median(sh_px, axis=0) / np.maximum(np.median(lit_px, axis=0), 1e-3), 0.3, 1.0)
    # the lid's shadow: hinged at the box's far edge (one box height), its free edge out of the picture (about 1.9)
    free = 1.9
    far = box_quad(-6)                                             # (the hinge line's shadow joins the box's own)
    lid_sh = [(far[0][0] + SUN_OFF[0], far[0][1] + SUN_OFF[1] + 2), (far[1][0] + SUN_OFF[0], far[1][1] + SUN_OFF[1] + 2),
              (LID[2][0] + SUN_OFF[0] * free, LID[2][1] + SUN_OFF[1] * free), (LID[3][0] + SUN_OFF[0] * free, LID[3][1] + SUN_OFF[1] * free)]
    # (the prop's shadow: a stick from the box's far right corner to the lid, a thin line inside the lid's shadow)
    # the planks as they would be lit under the old shadow, then both shadows laid again with a soft edge (cast from
    # a height: a penumbra)
    lit = b / (1 - old[..., None] * (1 - ratio[None, None, :]))
    whole = np.maximum(mask_poly(SHAPE, [(p[0] + SUN_OFF[0], p[1] + SUN_OFF[1]) for p in box_quad(-6)], soft=0.6),
                       mask_poly(SHAPE, lid_sh, soft=0.8, wobble=0.6, seed=SEED))
    shadow = np.clip(blur(whole, 1.8), 0, 1) * DECK
    b = lit * (1 - shadow[..., None]) + lit * ratio[None, None, :] * shadow[..., None]
    # both a little deeper and cooler, deepest by the box (the post's shade gathers under it), as one glaze
    near_box = 1 - smooth(0, 70, np.maximum(X - (fx1 + (Y - fy) * 40 / 514), 0))
    glaze = shadow * (0.24 + 0.14 * near_box)
    cool = lerp(np.array([1, 1, 1], F32), lerp(COBALT, PRUSSIAN, 0.2) * 1.75, 0.55)
    b = b * (1 - glaze[..., None]) + b * np.clip(cool, 0, 1.2)[None, None, :] * glaze[..., None]
    # the planks' marks
    dark, pale, bloom = deck_texture(SEED + 3)
    plank_dark = lerp(SIENNA, PRUSSIAN, 0.35)
    m = dark * 0.42 * DECK
    b = b * (1 - m[..., None]) + b * (plank_dark * 1.25)[None, None, :] * m[..., None]
    lightc = lerp(tintw(OCHRE, 0.55), NAPLES, 0.4)
    m = pale * 0.30 * DECK * (1 - 0.6 * shadow)
    b = lerp(b, lightc[None, None, :], m[..., None])
    m = bloom * 0.10 * DECK * (1 - shadow)
    b = lerp(b, lerp(WHITE, NAPLES, 0.3)[None, None, :], m[..., None])
    # the noon light on the deck far below: warm, a breath of haze over it (the box and card stand forward)
    haze = lerp(WHITE, CERULEAN, 0.10)
    b = depth.air(b, DECK * (1 - 0.5 * shadow), haze, amount=0.09)
    # the box's near board a little deeper toward the lens
    near = smooth(548, 606, Y) * mask_poly(SHAPE, BOX, soft=0.6) * 0.10
    b = b * (1 - near[..., None]) + b * lerp(SIENNA, OCHRE, 0.5)[None, None, :] * 1.2 * near[..., None]
    return np.clip(b, 0, 1).astype(F32), shadow


# ================================================================ the front plane
def near_plane(back):
    """The edge of the box's surroundings close to the lens and out of focus: soft, deep warm shade, darker toward the
    frame. Left and right: the deck's planks; across the top: the propped lid's free edge, nearest the lens."""
    rng = np.random.default_rng(SEED + 7)
    # the near planks: the deck's own run (left to right), nearer and so larger (a plank 15.5 px far below, ~38 here);
    # their ends a little ragged, all of it seen soft
    PL = 38.0
    row = np.floor((Y + 9) / PL).astype(int)
    offL = rng.uniform(-5, 5, 40)[np.clip(row, 0, 39)]
    offR = rng.uniform(-5, 5, 40)[np.clip(row, 0, 39)]
    eL = 56 + 12 * (Y / 600.0) + offL + 3 * np.sin(Y / 140.0 + 0.6)
    eR = 754 - 6 * (Y / 600.0) + offR - 3 * np.sin(Y / 120.0 + 2.0)
    eR = np.where(Y > 540, np.maximum(eR, 748), eR)                # (clear of Kanbei's thumb)
    eT = 17 + 4 * np.sin(X / 160.0 + 0.3)
    left_h = (X < eL).astype(F32)
    right_h = (X > eR).astype(F32)
    top_h = (Y < eT).astype(F32)
    left, right, top = blur(left_h, 5.5), blur(right_h, 5.5), blur(top_h, 7.0)
    a = np.clip(np.maximum.reduce([left, right, top]) * 1.08, 0, 1)
    # out of focus: the planks and the lid seen soft
    soft = blur(back, 4.2)
    seams = np.abs(((Y + 9) % PL) - PL / 2) / (PL / 2)              # 1 at a seam, 0 mid-plank
    seams = blur(smooth(0.80, 1.0, seams), 2.2) * np.maximum(left, right)
    # darker toward the frame
    kL = 0.56 + 0.36 * smooth(0, 1, np.clip((eL - X) / np.maximum(eL, 1), 0, 1))
    kR = 0.56 + 0.36 * smooth(0, 1, np.clip((X - eR) / np.maximum(W - eR, 1), 0, 1))
    kT = 0.50 + 0.40 * smooth(0, 1, np.clip((eT + 8 - Y) / np.maximum(eT + 8, 1), 0, 1))
    k = np.maximum.reduce([kL * left, kR * right, kT * top]) / np.maximum(a, 1e-3)
    k = np.clip(k + 0.10 * seams, 0.45, 0.94)
    col = soft * (1 - k[..., None]) + SHADE[None, None, :] * k[..., None]
    col[..., 0] = np.minimum(col[..., 0] + 0.055, 1)                 # warm (near_tone's way)
    col[..., 2] = np.maximum(col[..., 2] - 0.015, 0)
    # the rim: the right-hand edge faces the sun (behind us, a little left); the lid's edge a breath of it
    rim = blur(depth.rim(right_h, light=TO_LIGHT, width=3.0), 1.4)
    rim = np.clip(rim * 1.6, 0, 1) * 0.42
    rim_c = lerp(tintw(OCHRE, 0.45), NAPLES, 0.35) * 0.92
    col = lerp(col, rim_c[None, None, :], rim[..., None])
    return np.clip(col, 0, 1).astype(F32), a.astype(F32)


# ================================================================ the finish
def finish(picture, path, colors, alpha=None, seed=7):
    g = grain(picture, seed, 0.010)
    sample = g if alpha is None else g[alpha > 0.5]
    n = min(colors, max(2, len(np.unique((sample * 255).astype(np.uint8).reshape(-1, 3), axis=0))))
    pal = palette_of([sample.reshape(-1, 1, 3)], colors=n)
    idx = to_palette(g, pal, speckle=0.010)
    save(path, idx, pal, alpha)
    return os.path.getsize(path)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    back0, _ = load("back.png")
    thumb_c, thumb_a = load("thumb.png")
    back, shadow = deepen(back0)
    KEEP = keep_mask()
    WET = (DECK * 0.25).astype(F32)
    kw = dict(seed=SEED, soft=WET, wander=1.4, fleck=0.3, keep=KEEP)
    washed = watercolor.wash(back, **kw)
    t_col = watercolor.wash_cut(thumb_c, thumb_a, back, crisp=True, **kw)
    n_col, n_a = near_plane(back)
    n_washed = watercolor.wash_cut(n_col, n_a, back, crisp=True, **kw)
    n_bin = (n_a > 0.12).astype(F32)
    print("near share", round(float(n_bin.mean()) * 100, 1), "%")
    print("back", finish(washed, OUT + "/back.png", 160))
    print("thumb", finish(t_col, OUT + "/thumb.png", 40, thumb_a))
    print("near", finish(n_washed, OUT + "/near.png", 48, n_bin))
    for name in ("needle.png", "needle-l.png", "needle-r.png", "layout.json"):
        shutil.copyfile(os.path.join(ORIG, name), os.path.join(OUT, name))
    comp = Image.open(OUT + "/back.png").convert("RGBA")
    for name in ("needle", "thumb", "near"):
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save("out/edo-compass-depth-comp.png")
    print("done")

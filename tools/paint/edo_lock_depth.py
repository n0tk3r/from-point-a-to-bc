"""The shipwright's lock (edo-lock), deepened: round twenty-three's fast depth pass, over the painting as it is.

    python3 edo_lock_depth.py      reads out/edo-lock-orig/ (edo_lock.py's full run, never changed), writes out/edo-lock/

A close-up, flat and frontal, late afternoon, the low gold sun from the left (edo_lock.py). Nobody stands in it, so the
three planes are three depths of wood:

  NEAR   the edge of a nearer lattice at each side of the frame, between us and the doors (the hall's outer lattice,
         folded back): a thick stile with its bars running off the frame, much larger than the doors' own lattice
         because it is close to the lens, in deep warm shade, only its edges toward the sun lit; through its gaps the
         doors beyond, out of focus and shaded. It covers the doors' lattice areas (the `lattice` areas are the near
         thing itself) and nothing else that is clicked: the slips, the hasp and the bolt stay in the open.
  MIDDLE the lock, exactly as painted and kept out of the wash: every part of it and its holes is the puzzle. Round it
         the light falls across the boards: a broad band of low sun, the curved eave's shadow lying across the top of
         the door and leading in from the right, the lower boards a little deeper; the lock's shadow on the door
         deeper and cooler, with a dark contact edge; the boards weathered along their grain (streaks, no knots and no
         holes: nothing that could be taken for a part of the lock).
  FAR    the dim hall seen between the doors' bars, a little paler and cooler (behind the near dark, never as dark).

Then the act's watercolour (watercolor.wash, seed 1830; the lock kept), and back to the scene's own palettes. The
lock's cut-outs (the ear, the wave, the coin and post, the slits, the bolt: every state) are parts of the lock and are
copied over as painted, byte for byte."""

import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import F32, Sheet, blur, grid, lerp, mask_poly, noise, rgb, tint, glow, step
import depth
import watercolor
from edo_town_kit import PAINT, PAPER, LINE, mix, finish

W, H = 800, 600
SHAPE = (H, W)
SRC = "out/edo-lock-orig"
OUT = "out/edo-lock"
SEED = 1830
CUTS = ["wave", "ear", "bolt", "ear-clean", "wave-slid", "post-coin", "post-turned", "back-open", "bolt-out"]

# the lock as edo_lock.py measures it: the body 21 x 10 cm at 22 px to the cm from (204, 196); the hasp's plate and the
# bolt from the scene's areas
LOCK_BODY = [(204, 196), (666, 196), (666, 416), (204, 416)]
HASP = [(98, 220), (168, 216), (172, 398), (102, 402)]
BOLT = [(211, 293), (211, 319), (105, 328), (78, 321), (73, 312), (73, 302), (79, 292), (105, 280)]

WOOD = mix(mix(PAINT["sienna"], PAINT["ochre"], 0.25), PAINT["naples"], 0.08)
WOOD_LIT = mix(mix(PAINT["ochre"], PAINT["naples"], 0.4), PAINT["sienna"], 0.25)
GAP = mix(PAINT["prussian"], PAINT["sienna"], 0.28)
SUN = mix(PAINT["naples"], PAPER, 0.3)
SHADE = mix(mix(PAINT["prussian"], "#8a7fa8", 0.55), PAPER, 0.25)          # a cool glaze (multiplied)


def load_rgb(p):
    return np.asarray(Image.open(p).convert("RGB"), F32) / 255.0


def load_rgba(p):
    a = np.asarray(Image.open(p).convert("RGBA"), F32) / 255.0
    return a[..., :3].copy(), a[..., 3].copy()


def c3(color):
    return rgb(color) if isinstance(color, str) else np.asarray(color, F32)


# ---------------------------------------------------------------- the lock: kept exactly
def lock_keep():
    m = np.maximum(mask_poly(SHAPE, LOCK_BODY), np.maximum(mask_poly(SHAPE, HASP), mask_poly(SHAPE, BOLT)))
    m = np.clip(blur(m, 2.0) * 2.2, 0, 1)                    # a little round it, feathered
    return m.astype(F32)


# ---------------------------------------------------------------- NEAR: the nearer lattice at the frame's edges
L_STILE = (24.0, 64.0)          # the left near stile (x); its bars run off the left edge
R_STILE = (712.0, 752.0)        # the right near stile; its bars run off the right edge
BARS = [(-16.0, 26.0), (226.0, 268.0), (468.0, 510.0)]    # the near bars (y): larger than the doors' 26 px bars


def wobble_x(x, y, seed, amp=1.2):
    return x + amp * np.sin(y / 37.0 + seed) + 0.6 * np.sin(y / 11.0 + 2 * seed)


def near_masks():
    """-> (whole, solid, bars, stiles): the near plane's cover (the gaps between its bars included: through them we see
    the doors beyond, out of focus, in its shade), its wood, its bars, its stiles."""
    ys = np.arange(-10, H + 11, 6.0)
    stiles = np.zeros(SHAPE, F32)
    for (x0, x1), sd in ((L_STILE, 1.0), (R_STILE, 2.0)):
        left = [(wobble_x(x0, y, sd), y) for y in ys]
        right = [(wobble_x(x1, y, sd + 0.7), y) for y in ys[::-1]]
        stiles = np.maximum(stiles, mask_poly(SHAPE, left + right))
    for (x0, x1), sd in (((-34.0, 7.0), 3.0), ((786.0, 830.0), 4.0)):
        left = [(wobble_x(x0, y, sd), y) for y in ys]
        right = [(wobble_x(x1, y, sd + 0.7), y) for y in ys[::-1]]
        stiles = np.maximum(stiles, mask_poly(SHAPE, left + right))
    bars = np.zeros(SHAPE, F32)
    for (y0, y1) in BARS:
        for (xa, xb) in ((-20.0, L_STILE[0] + 4), (R_STILE[1] - 4, W + 20.0)):
            sag = 1.5
            top = [(xa, y0), ((xa + xb) / 2, y0 + sag), (xb, y0 + 0.5)]
            bot = [(xb, y1 + 0.5), ((xa + xb) / 2, y1 + sag), (xa, y1)]
            bars = np.maximum(bars, mask_poly(SHAPE, top + bot))
    solid = np.maximum(stiles, bars)
    x, _ = grid(SHAPE)
    whole = np.maximum(solid, ((x < L_STILE[0] + 2) | (x > R_STILE[1] - 2)).astype(F32))
    return whole, solid, bars, stiles


def paint_near(back0):
    """The near lattice, painted. -> (colour, alpha)."""
    whole, solid, bars, stiles = near_masks()
    x, y = grid(SHAPE)
    # through the gaps: the doors beyond, out of focus and in the near lattice's shade
    beyond = blur(back0, 7.0)
    beyond = beyond * 0.30 + c3(GAP)[None, None, :] * 0.05
    beyond = lerp(beyond, depth.near_tone(GAP, shade="#1c1418", k=0.60, warm=0.04)[None, None, :], 0.45)
    col = beyond.copy()
    # the wood: deep and warm, graded darker toward the bottom; a little grain along the stiles
    deep = depth.near_tone(WOOD, shade="#1c1418", k=0.80, warm=0.06)
    deep2 = depth.near_tone(mix(WOOD, PAINT["sienna"], 0.5), shade="#1c1418", k=0.86, warm=0.05)
    g = np.clip(y / H, 0, 1)[..., None]
    wood = lerp(deep[None, None, :], deep2[None, None, :], g * 0.8)
    grain_ = noise(SHAPE, 9, 41, 3)
    vert = np.clip((noise((H, W // 4 + 1), 6, 47, 3)[:, :, None].repeat(4, axis=2).reshape(H, -1)[:, :W]), 0, 1)
    wood = wood * (1 + (vert[..., None] - 0.5) * 0.18 * stiles[..., None]) * (1 + (grain_[..., None] - 0.5) * 0.06)
    col = lerp(col, wood, solid[..., None])
    # the side away from the light: a darker line down each stile's right edge and under each bar
    sh = np.clip(solid - np.roll(solid, -3, axis=1), 0, 1) + np.clip(solid - np.roll(solid, -3, axis=0), 0, 1)
    tint(col, depth.near_tone(GAP, k=0.75, warm=0.02), np.clip(sh, 0, 1) * 0.55)
    # the rim: the edges toward the low sun (left, a little above), warm
    r = depth.rim(solid, light=(-1.0, -0.45), width=2.4)
    r = np.clip(r * 1.6, 0, 1) * (0.75 + 0.25 * noise(SHAPE, 14, 51, 2))
    lit = mix(WOOD_LIT, SUN, 0.35)
    col = lerp(col, c3(lit)[None, None, :] * 0.92, (r * 0.85)[..., None])
    # a faint warm bounce from the lit door on the stiles' faces toward the middle of the picture
    toward = np.where(x < W / 2, np.clip((x - L_STILE[0]) / (L_STILE[1] - L_STILE[0]), 0, 1),
                      np.clip((R_STILE[1] - x) / (R_STILE[1] - R_STILE[0]), 0, 1))
    glow(col, c3(mix(PAINT["orange"], PAINT["sienna"], 0.5)), (stiles * toward ** 3 * 0.10).astype(F32))
    # a quiet key line, broken, on the shade side only
    edge = np.clip(whole - np.roll(whole, -1, axis=1), 0, 1) * (noise(SHAPE, 7, 53, 2) > 0.42)
    tint(col, c3(LINE), (edge * 0.35).astype(F32))
    return np.clip(col, 0, 1).astype(F32), whole.astype(F32)


# ---------------------------------------------------------------- MIDDLE and FAR: the back deepened
def deepen_back(back0, keep):
    pic = back0.copy()
    x, y = grid(SHAPE)
    xf = x / W
    # the eave's shadow across the top of the door: its edge sags with the eave's curve, lower to the right, soft
    edge_y = 70 + 78 * xf + 10 * np.sin(xf * 3.0 + 0.4) + 3.0 * (noise(SHAPE, 40, 61, 2) - 0.5)
    eave = 1 - step(-10, 12, y - edge_y)
    # the lower boards a little deeper (the veranda's own shadow, low)
    low = step(430, 610, y) * 0.55
    shade = np.clip(eave * 0.92 + low, 0, 1)
    tint(pic, c3(SHADE), (shade * 0.55 * (1 - keep)).astype(F32))
    # the low sun across the boards between: warm, strongest by the lock, fading to the right
    band = (1 - eave) * (1 - low) * np.clip(1 - (x - 80) / 900.0, 0.25, 1)
    glow(pic, c3(SUN), (band * 0.08 * (1 - keep)).astype(F32))
    # the lock's shadow on the door, deeper and cooler, with a dark contact edge (the lock stands ~4 cm proud)
    body = mask_poly(SHAPE, LOCK_BODY)
    far_sh = np.clip(np.roll(np.roll(blur(body, 5.0), 24, axis=1), 22, axis=0) - body, 0, 1)
    near_sh = np.clip(np.roll(np.roll(blur(body, 2.0), 6, axis=1), 6, axis=0) - body, 0, 1)
    tint(pic, c3(mix(SHADE, GAP, 0.35)), (far_sh * 0.30 + near_sh * 0.35).astype(F32))
    # the hasp's plate throws a little shadow too
    hasp = mask_poly(SHAPE, HASP)
    hs = np.clip(np.roll(np.roll(blur(hasp, 2.5), 7, axis=1), 6, axis=0) - hasp, 0, 1)
    tint(pic, c3(mix(SHADE, GAP, 0.35)), (hs * 0.40 * (1 - keep)).astype(F32))
    # the boards weathered along the grain: long vertical streaks, darker and lighter, away from the lock
    streaks = blur(noise(SHAPE, 6, 71, 3), 0.7)
    sx = np.asarray(Image.fromarray((streaks * 255).astype(np.uint8)).resize((W, 12)).resize((W, H), Image.BICUBIC), F32) / 255
    wood_here = np.clip(((x > 84) & (x < 690)).astype(F32) - blur(lock_keep(), 6.0) * 1.5, 0, 1)
    pic *= (1 + (sx[..., None] - 0.5) * 0.10 * wood_here[..., None])
    # the far: the dim hall between the doors' bars, toward a cool haze (never as dark as the near)
    lum = pic @ np.array([0.30, 0.55, 0.15], F32)
    hall = (((x < 84) | (x > 690)) & (lum < 0.30)).astype(F32)
    hall = blur(hall, 1.0)
    pic = lerp(pic, c3(mix(GAP, "#b8b4c8", 0.35))[None, None, :] * np.ones_like(pic), (hall * 0.22)[..., None])
    return np.clip(pic, 0, 1).astype(F32), hall


def wet_map(hall):
    # nothing far but the dim hall between the bars; everything else stands
    return (hall * 0.5).astype(F32)


if __name__ == "__main__":
    if not os.path.isdir(SRC):
        sys.exit(f"no {SRC}: run edo_lock.py and copy out/edo-lock to it first")
    os.makedirs(OUT, exist_ok=True)
    back0 = load_rgb(f"{SRC}/back.png")
    keep = lock_keep()
    back1, hall = deepen_back(back0, keep)
    WET = wet_map(hall)
    washed = watercolor.wash(back1, seed=SEED, soft=WET, keep=keep, wander=1.4, fleck=0.3)
    washed = lerp(washed, back0, keep[..., None])              # the lock exactly as painted
    print("back", finish(washed, f"{OUT}/back.png", 160, amount=0.0, speckle=0.004)[0])   # (its grain is the painting's own)
    nc, na = paint_near(back1)
    ncw = watercolor.wash_cut(nc, na, back1, seed=SEED, soft=WET, wander=1.4, fleck=0.3, crisp=True)
    hard = (na > 0.5).astype(F32)
    print("near", finish(ncw, f"{OUT}/near.png", 64, hard, amount=0.010, speckle=0.010)[0])
    for n in CUTS:                                              # the lock's parts: as painted
        shutil.copyfile(f"{SRC}/{n}.png", f"{OUT}/{n}.png")
    if os.path.exists(f"{SRC}/layout.json"):
        shutil.copyfile(f"{SRC}/layout.json", f"{OUT}/layout.json")
    comp = Image.open(f"{OUT}/back.png").convert("RGBA")
    for n in ["wave", "ear", "bolt", "near"]:
        comp.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
    comp.convert("RGB").save("out/edo-lock-depth-comp.png")
    print("share", round(float(hard.mean()) * 100, 1))

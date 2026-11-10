#!/usr/bin/env python3
"""Big Sister's room in the attic, the Retreat: the depth pass (round twenty-three, tools/paint/DEPTH.md).

    python3 home_bigsis_room_depth.py [SRC]

Reads the painting as home_bigsis_room.py paints it (out/home-bigsis-room-orig/, or SRC) and writes the scene's full set
back into out/home-bigsis-room/: every file as before, back.png deepened, and near.png, the front plane:

  near.png   the roof near the lens across the top left corner (two rafters and the boards between them, the nearer
             rafter's under-edge lit by the lamps below) and a squared post at the right edge, standing from below the
             frame to above it, its inner face warm from the lanterns at the bed's foot. Deep warm dark; nothing that is
             clicked or stood on lies behind either.
  back.png   through the room's own camera (room.View, the numbers in home_bigsis_room_model.VIEW): the far end of the
             room (the low wall, the far floor, the ceiling where it comes down to the wall) a little cooler and paler;
             pools of lamplight on the floorboards under the lanterns, by the salt lamp, the floor candle and the two
             lanterns at the bed's foot; the near floor deeper and warmer toward the hatch.
  desk.png, front.png, layout.json   as they were.
"""

import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import F32, Sheet, blur, grid, lerp, mask_ellipse, noise, rgb, save, to_palette
import depth
from home_bigsis_room import palette_for
from home_bigsis_room_model import VIEW, W as ROOM_W, KNEE, RISE

SRC = sys.argv[1] if len(sys.argv) > 1 else "out/home-bigsis-room-orig"
OUT = sys.argv[2] if len(sys.argv) > 2 else "out/home-bigsis-room"
SHAPE = (600, 800)
HZ, FOCAL, CX = VIEW["horizon"], VIEW["focal"], VIEW["centre_x"]
CAM_X, CAM_Z = VIEW["cam"]
EYE = 350.0                                  # the lens's height above the floor, cm (layout.json `eye_cm`)


def load(name):
    im = Image.open(os.path.join(SRC, name)).convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def depth_map():
    """Depth along the lens axis (cm) of what is seen at each pixel: the room is a box with a slanted ceiling, seen
    through its open near side, so each ray ends on the nearest of floor, far wall, end walls and ceiling."""
    x, y = grid(SHAPE)
    big = np.full(SHAPE, 1e9, F32)
    d_floor = np.where(y > HZ + 0.5, EYE * FOCAL / np.maximum(y - HZ, 0.5), big)
    d_far = np.full(SHAPE, float(CAM_Z), F32)
    half = ROOM_W - CAM_X
    d_left = np.where(x < CX - 0.5, CAM_X * FOCAL / np.maximum(CX - x, 0.5), big)
    d_right = np.where(x > CX + 0.5, half * FOCAL / np.maximum(x - CX, 0.5), big)
    k = (HZ - y) / FOCAL + RISE                          # the ceiling: KNEE + RISE * Z, with Z = CAM_Z - d
    d_ceil = np.where(k > 1e-3, (KNEE + RISE * CAM_Z - EYE) / np.maximum(k, 1e-3), big)
    d = np.minimum.reduce([d_floor, d_far, d_left, d_right, d_ceil])
    floor = (d_floor <= d + 0.5)
    return d.astype(F32), floor.astype(F32)


def floor_pt(X, Z):
    dd = CAM_Z - Z
    return CX + (X - CAM_X) * FOCAL / dd, HZ + EYE * FOCAL / dd


# ---------------------------------------------------------------- the back, deepened

def deepen(back):
    pic = back.copy()
    d, floor = depth_map()
    dmin, dmax = EYE * FOCAL / (SHAPE[0] - HZ), float(CAM_Z)
    far = np.clip((d - dmin) / (dmax - dmin), 0, 1)
    x, y = grid(SHAPE)

    # the far end of the room: a little cooler and paler (toward the moonlit lavender of the plaster in shade)
    depth.air(pic, far, "#a69fc4", amount=0.15, power=2.2)

    # pools of lamplight on the floorboards: under each paper lantern, by the salt lamp and the floor candle, and the
    # two candle lanterns at the bed's foot (their places on the floor, through the camera)
    pools = []
    for (X, Z, _Y, _r) in [(120, 196, 236, 15), (392, 222, 268, 21), (540, 150, 226, 17)]:
        px, py = floor_pt(X, Z)
        pools.append((px, py, 74, 0.07, "#ffbf80"))
    sx, sy = floor_pt(38, 142)
    pools.append((sx + 4, sy + 3, 52, 0.15, "#ff9450"))          # the salt lamp: deep amber
    fx, fy = floor_pt(68, 328)
    pools.append((fx, fy + 2, 46, 0.13, "#ffb066"))              # the floor candle by the towels
    for (X, Z) in [(622, 372), (648, 392)]:
        px, py = floor_pt(X, Z)
        pools.append((px, py + 3, 66, 0.14, "#ffb066"))          # the lanterns at the bed's foot
    lit = np.zeros(SHAPE + (3,), F32)
    for (px, py, rx, k, col) in pools:
        ry = rx * (py - HZ) / (EYE * 2.6)                        # flattened by the floor's foreshortening
        m = mask_ellipse(SHAPE, px, py, rx, max(ry, 6), soft=rx * 0.9)
        m = m * floor * (0.85 + 0.15 * noise(SHAPE, 18, 4100 + int(px), octaves=3))
        lit += rgb(col) * (m * k)[..., None]
    pic = 1 - (1 - pic) * (1 - np.clip(lit, 0, 1))                # screened on: light, never paint

    # the near floor deeper and warmer, toward the hatch (thin where people stand)
    t = np.clip((y - 455) / 145, 0, 1) ** 1.3 * 0.34 * floor
    pic = lerp(pic, rgb("#2b1720")[None, None, :], t[..., None])
    return np.clip(pic, 0, 1).astype(F32)


# ---------------------------------------------------------------- the near plane

def unit(v):
    v = np.asarray(v, dtype=float)
    return v / np.hypot(*v)


def near_plane():
    s = Sheet(SHAPE, ss=3)
    wood = depth.near_tone("#2e1a12", shade="#140c0e", k=0.4, warm=0.04)
    wood_lo = depth.near_tone("#40261a", shade="#140c0e", k=0.35, warm=0.05)
    board_a = depth.near_tone("#22140f", shade="#120a0e", k=0.45, warm=0.03)
    board_b = depth.near_tone("#2a1812", shade="#120a0e", k=0.45, warm=0.03)

    # ---- the roof near the lens, top left: the boards (running across, along the ridge: level in the picture) ...
    A, B = np.array([272.0, 0.0]), np.array([0.0, 190.0])           # the near rafter's under-edge
    u = unit(B - A)
    n = np.array([-u[1], u[0]])
    if n[1] < 0:
        n = -n                                                      # n points down into the room
    wedge = [(-6, -6), (A[0] + 8, -6), tuple(A), tuple(B), (-6, B[1] + 8)]
    s.poly(wedge, board_a)
    yb, i = 0.0, 0
    rng = np.random.default_rng(1823)
    while yb < B[1]:
        hgt = 15 + 9 * rng.random() + yb * 0.04
        s.poly([(-6, yb), (A[0] + 8, yb), (A[0] + 8, yb + hgt), (-6, yb + hgt)], board_b if i % 2 else board_a)
        s.line([(-6, yb + 0.5), (A[0] + 8, yb + 0.5)], "#140c10", width=1.4, alpha=0.8, round_ends=False)
        yb += hgt
        i += 1

    # ... and the two rafters across them, the far one slimmer, near the corner
    def rafter(edge_a, edge_b, thick, lit):
        a2, b2 = edge_a - n * thick, edge_b - n * thick
        far_a, far_b = edge_a - u * 40, edge_b + u * 40
        s.poly([tuple(far_a), tuple(far_b), tuple(b2 + u * 40), tuple(a2 - u * 40)], wood)
        # its under-face, seen from below and warm from the lamps: a narrow strip along the lower edge
        f = 7 if lit else 4
        s.poly([tuple(far_a), tuple(far_b), tuple(far_b - n * f), tuple(far_a - n * f)], wood_lo)
        for k in range(3):                                          # the grain, along it
            o = thick * (0.3 + 0.22 * k) + rng.random() * 3
            s.line([tuple(far_a - n * o), tuple(far_b - n * o)], "#160d10", width=0.9, alpha=0.45, round_ends=False)
        s.line([tuple(a2 - u * 40), tuple(b2 + u * 40)], "#120a0e", width=1.6, alpha=0.9, round_ends=False)

    rafter(A - n * 96, B - n * 96, 24, False)
    rafter(A, B, 36, True)
    s.clear([tuple(A), (812, -12), (812, 612), (-12, 612), tuple(B)])    # nothing below the near rafter's edge

    # ---- the post at the right: a squared timber standing from below the frame to above it; we see its front and
    # the side that faces the room (lit a little, warm, from the lanterns at the bed's foot)
    X0, X1, X2 = 755, 768, 812
    s.poly([(X1, -6), (X2, -6), (X2, 606), (X1, 606)], wood)
    s.poly([(X0, -6), (X1, -6), (X1, 606), (X0, 606)], depth.near_tone("#3a2218", shade="#140c0e", k=0.35, warm=0.05))
    for gx, al in [(774, 0.4), (781.5, 0.35), (790, 0.4), (761, 0.3)]:
        s.line([(gx, -6), (gx + 0.6, 606)], "#150c10", width=0.9, alpha=al, round_ends=False)
    s.line([(X1, -6), (X1, 606)], "#120a0e", width=1.2, alpha=0.7, round_ends=False)      # the arris between the faces

    color, alpha = s.done()
    color = color * 0.78                                            # deeper still: the darkest, warmest mass of the picture
    alpha = np.where(alpha > 0.02, alpha, 0).astype(F32)
    x, y = grid(SHAPE)

    # the lit rims: the rafter's under-edge (the lanterns are below it, to the right) and the post's inner edge, warmest
    # at the height of the lanterns by the bed
    roof = alpha * (x < 400)
    post = alpha * (x >= 700)
    r1 = depth.rim(roof, light=(0.55, 1.0), width=2.2)
    r2 = depth.rim(post, light=(-1.0, 0.1), width=2.0)
    by_lamp = np.clip(1.0 - np.abs(y - 470) / 260, 0.25, 1.0)
    rim_col = rgb("#e8a464")
    color = lerp(color, rim_col[None, None, :], (np.clip(r1 * 0.75, 0, 1))[..., None])
    color = lerp(color, rim_col[None, None, :], (np.clip(r2 * 0.6 * by_lamp, 0, 1))[..., None])
    # a little warm bounce on the post's room side, toward the lamps
    side = ((x >= X0) & (x < X1)).astype(F32) * alpha
    color = lerp(color, rgb("#8a5634")[None, None, :], (side * 0.22 * by_lamp)[..., None])
    # and a soft variation of tone over everything (no holes: the alpha is solid inside)
    color = color * (0.94 + 0.08 * noise(SHAPE, 60, 1831, octaves=3))[..., None]
    return np.clip(color, 0, 1).astype(F32), alpha


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(SRC):
        if os.path.isfile(os.path.join(SRC, f)) and f != "back.png":
            shutil.copyfile(os.path.join(SRC, f), os.path.join(OUT, f))

    back, _ = load("back.png")
    deep = deepen(back)
    pal = palette_for(deep, 160)
    save(os.path.join(OUT, "back.png"), to_palette(deep, pal, speckle=0.006), pal)

    color, alpha = near_plane()
    solid = alpha > 0.5
    pal = palette_for(color[solid], 48)
    save(os.path.join(OUT, "near.png"), to_palette(color, pal, speckle=0.004), pal, alpha)
    print("near covers", round(float((alpha > 0.5).mean()) * 100, 1), "% of the picture")


if __name__ == "__main__":
    main()

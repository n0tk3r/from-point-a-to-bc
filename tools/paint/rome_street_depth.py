"""The street to the Forum, with depth (round twenty-three, the fast pass: tools/paint/DEPTH.md). Works over the painting
as it is (rome_street.py, run once into out/rome-street/ and kept in out/rome-street-orig/, never changed) and writes
the scene's full set back into out/rome-street/: every file as before, a deepened back.png, and near.png.

THE NEAR PLANE (near.png, plane "front", last): the house on our right, nearest the lens, across the side street from
the corner where we stand, through the scene's own camera (rome_street_kit.cam: the lens 3.9 m up, 8.75 m before the
`full` row):

  its corner  the shaded corner of a tall insula, standing out a little into the street (its face 3.15 m right of the
              middle, the corner 2.1 m before the `full` row): up the right edge of the frame from top to bottom, x 779
              on. Plaster in deep, warm shade over brick, the corner's stones, a string course at the first floor, the
              plinth at its foot; a warm bounce from the sunlit houses opposite along its edge.
  the cloths  dyed cloths hung out to dry on a line strung from its upper window, high over the street near us (4 m
              before the lens): their hems hang into the top right corner, madder, saffron and woad, in the house's
              shade. Nothing near the lens is a thing to pick up: they are far over everybody's head.

  It hides nothing clicked or stood on: the corner keeps clear of RVFVS (its letters end at x 772) and of the cat; the
  cloths' hems stay above the birdcage (95), the washing lines (100) and the balcony; the swallows' way in is left open.

THE BACK: the shadow of that tall house, thrown across the street by the low sun (from the upper right, behind us) onto
the sunlit corner of the house opposite, over the snack bar (a large shadow from outside the picture leading in); the
air: the far end of the street and the Forum's buildings a step paler toward the sky at the horizon (a far map from
the camera: the ground and the house fronts at their own distance); the near ground and the bottom corners a little
deeper. Nothing clicked is moved or redrawn. The cut-outs, the frames and layout.json are copied over as they were.

    python3 rome_street_depth.py        (light: a few seconds)"""

import json
import os
import shutil

import numpy as np
from PIL import Image

from brush import F32, Sheet, blur, grain, grid, lerp, mask_poly, noise, palette_of, rgb, save, to_palette
import depth
from rome_street_kit import cam

ORIG = "out/rome-street-orig"
OUT = "out/rome-street"
W, H = 800, 600
X, Y = grid((H, W))
X = X + 0.5
Y = Y + 0.5

LIGHT = (-0.62, -0.50, 0.60)                       # rome_street.py: the way the sunlight travels (left, down, away)
TO_SUN = (0.70, -0.70)                             # toward the sun, in the picture
SHADE = "#1a0f14"                                  # the near plane's shade: deep and warm
BOUNCE = "#f2b878"                                 # warm light off the sunlit house fronts opposite
SKY_LOW = (0.70, 0.746, 0.811)                     # the sky just over the temple (measured in back.png)
NEAR_LUM = 0.088                                   # the near plane's mean light

# the near house: its street face, its corner, its height (cm, in the street's own measure: rome_street.py)
NEAR_X, NEAR_Z, NEAR_H = 315.0, -210.0, 980.0
EDGE = 779.0                                       # where its corner stands in the picture
K_NEAR = cam.scale(NEAR_Z)                         # pixels per cm at the corner (about 1.2)


def load(name):
    im = Image.open(os.path.join(ORIG, name)).convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


# ---------------------------------------------------------------------------------------------------- the near plane
def near_house(seed=23):
    """The corner of the house on our right: colour, alpha."""
    c = np.zeros((H, W, 3), dtype=F32)
    a = np.zeros((H, W), dtype=F32)
    # its outline: the corner's edge wanders a hair (worn stones), a string course sticks out at the first floor, the
    # plinth at its foot
    k = K_NEAR
    course = 230 + (394 - 352) * k                 # the string course, 3.5 m up: its underside, in the picture
    plinth = 230 + (394 - 60) * k                  # (the plinth's top is below the frame: 60 cm up at the corner)
    rng = np.random.default_rng(seed)
    pts = [(W + 2, -2), (EDGE + 0.6, -2)]
    yy, done_course = 0.0, False
    while yy < H:
        step = 30 * k * (0.9 + 0.2 * rng.random())                    # a quoin stone, 30 cm high
        nick = rng.random() * 1.4
        if not done_course and course - 10 < yy + step:                # the course: a little projecting ledge
            pts += [(EDGE + 0.3, course - 9), (EDGE - 5.5, course - 8), (EDGE - 6.0, course - 2), (EDGE - 4.5, course),
                    (EDGE + 0.2, course + 1.5)]
            yy, done_course = course + 1.5, True
            continue
        pts += [(EDGE + nick, yy + 1.5), (EDGE + nick * 0.5, yy + step - 1.5)]
        yy += step
    pts += [(EDGE - 2.5, H - 7), (EDGE - 3.5, H + 2), (W + 2, H + 2)]
    m = mask_poly((H, W), pts, soft=0.35)
    plaster = col("#b0704c")                       # ochre plaster, as the houses across the way
    brick = col("#8a4a34")
    t = noise((H, W), 18, seed + 1, 4)
    fine = noise((H, W), 4, seed + 2, 3)
    base = lerp(plaster, brick, np.clip((t - 0.62) * 4, 0, 1)[..., None] * 0.8)       # plaster fallen away in places
    base = base * (0.92 + 0.16 * fine)[..., None]
    body = lerp(base, np.broadcast_to(col(SHADE), base.shape), 0.74)
    body[..., 0] += 0.035
    up = np.clip(1 - Y / H, 0, 1)                                     # a little lighter high up (sky light over the roofs)
    body *= (0.86 + 0.20 * up)[..., None]
    # the quoin joints (lines to the vanishing point) and the course's top and shadow
    sh = Sheet((H, W))
    yy = 0.0
    rng = np.random.default_rng(seed + 3)
    while yy < H:
        yy += 30 * k * (0.9 + 0.2 * rng.random())
        if abs(yy - course) < 12:
            continue
        slope = (yy - cam.vy) / (EDGE - cam.vx)
        sh.line([(EDGE + 1, yy), (W + 1, yy + slope * (W - EDGE))], (0.10, 0.06, 0.08), 0.8, 0.55)
    slope = (course - cam.vy) / (EDGE - cam.vx)
    sh.poly([(EDGE - 6, course - 2), (W + 1, course - 2 + slope * (W - EDGE)), (W + 1, course + 4 + slope * (W - EDGE)),
             (EDGE - 4.5, course + 2)], (0.09, 0.05, 0.07), 0.85)                     # the course's underside
    sh.line([(EDGE - 5.5, course - 8.5), (W + 1, course - 8.5 + slope * (W - EDGE))], (0.62, 0.40, 0.30), 1.0, 0.7)   # its top
    jc, ja = sh.done()
    body = lerp(body, jc, ja[..., None])
    # the bounce: warm light off the sunlit fronts across the street, along the corner's edge, stronger high up
    r = depth.rim(m, light=(-1.0, -0.25), width=2.2)
    glow = np.clip(r * (0.35 + 0.65 * up ** 0.7), 0, 1) * 0.75
    body = lerp(body, lerp(body, col(BOUNCE), 0.55), glow[..., None])
    # the foot: deepest where it meets the ground
    body *= (1 - np.clip((Y - 470) / 130, 0, 1) * 0.22)[..., None]
    c = body
    a = m
    return np.clip(c, 0, 1), a


CLOTHS = [  # left, right (px at the top), the hem at its left, middle and right (px), its colour, its folds
    dict(x0=474.0, x1=558.0, hem=(96, 104, 92), color="#33447e", folds=3, seed=31),     # woad
    dict(x0=552.0, x1=666.0, hem=(92, 88, 86), color="#b07a2a", folds=4, seed=32),      # saffron
    dict(x0=658.0, x1=W + 4.0, hem=(124, 136, 134), color="#a03626", folds=5, seed=33),  # madder, the long one
    dict(x0=761.0, x1=W + 4.0, hem=(316, 322, 318), color="#7a3a2c", folds=2, seed=34, stripes=True),  # a blanket over the sill
]


def cloth(spec):
    """One dyed cloth hanging from the line above the frame: colour, alpha."""
    x0, x1 = spec["x0"], spec["x1"]
    h0, hm, h1 = spec["hem"]
    rng = np.random.default_rng(spec["seed"])
    xs = np.linspace(x0, x1, 40)
    t = (xs - x0) / (x1 - x0)
    hem = (1 - t) ** 2 * h0 + 2 * t * (1 - t) * hm + t ** 2 * h1                       # a slack hem, lowest in the middle
    hem = hem + np.sin(t * np.pi * spec["folds"] + rng.random() * 3) * 3.0              # ...and the folds' scallops
    side_l = [(x0 + 0.6 * math.sin(v * 0.07), v) for v in np.linspace(-2, hem[0], 6)]
    side_r = [(x1 - 0.6 * math.sin(v * 0.05), v) for v in np.linspace(hem[-1], -2, 6)]
    pts = [(x0, -3)] + side_l + list(zip(xs, hem)) + side_r + [(x1, -3)]
    m = mask_poly((H, W), pts, soft=0.4, wobble=0.6, seed=spec["seed"])
    local = col(spec["color"])
    # folds: soft vertical bands, sharper toward the hem
    u = (X - x0) / max(x1 - x0, 1)
    fold = 0.5 + 0.5 * np.sin(u * np.pi * 2 * spec["folds"] + rng.random() * 6 + noise((H, W), 30, spec["seed"], 2) * 1.6)
    tone = depth.near_tone(local, SHADE, k=0.66, warm=0.04)
    c = np.broadcast_to(tone, (H, W, 3)).copy()
    if spec.get("stripes"):                                                             # woven bands across it
        band = (np.sin(Y * 0.21 + 1.3) > 0.55).astype(F32) * (Y > 150)
        c = lerp(c, np.broadcast_to(depth.near_tone(col("#c89a4a"), SHADE, k=0.70, warm=0.04), c.shape), (band * 0.8)[..., None])
    c *= (0.78 + 0.34 * fold)[..., None]
    weave = noise((H, W), 3, spec["seed"] + 5, 2)
    c *= (0.94 + 0.10 * weave)[..., None]
    # the hem's turned edge, a hair darker; light let through the thin cloth near its hem (a warm glow)
    hem_y = np.interp(X[0], xs, hem)[None, :]
    near_hem = np.clip(1 - (hem_y - Y) / 7.0, 0, 1) * m
    c = lerp(c, c * 0.8, (near_hem * 0.6)[..., None])
    # the bounce on the edge toward the sunlit fronts across the street (the left) and the sky light from above
    r = depth.rim(m, light=(-1.0, 0.15), width=2.0)
    c = lerp(c, lerp(c, col(BOUNCE), 0.40), (r * 0.55)[..., None])
    return np.clip(c, 0, 1), m


def awning(seed=41):
    """An awning's edge across the top left corner: canvas stretched from the house on our left, at our corner of the
    side street, 4.6 to 5 m up (outer edge 1.2 m out over the main street, its end 3.3 m before the `full` row): seen
    from below, in the tall house's shadow, its valance hanging in scallops. Through the camera: the outer edge runs
    toward the vanishing point, the end square across."""
    zf = -330.0
    def P(x, y, z):
        return cam.pt(x, y, z)
    o_end = P(-120.0, 460.0, zf)                       # the outer edge at the end
    w_end = P(-300.0, 500.0, zf)                       # the end at the wall (off the frame)
    vx, vy = cam.vx, cam.vy
    def toward_us(p, t):                               # along the street toward us: away from the vanishing point
        return (vx + (p[0] - vx) * t, vy + (p[1] - vy) * t)
    o_near = toward_us(o_end, 2.6)
    drop = 15.0                                        # the valance, 15 cm deep
    v_end = P(-120.0, 460.0 - drop, zf)
    v_near = toward_us(v_end, 2.6)
    # the canvas underside: the end, the outer edge; the valance: a band under the outer edge, scalloped
    under = [w_end, o_end, o_near, (w_end[0] - 400, w_end[1] - 260)]
    m = mask_poly((H, W), under, soft=0.4)
    n = 22
    val = [o_near]
    for i in range(n + 1):
        t = i / n
        top = (o_near[0] + (o_end[0] - o_near[0]) * t, o_near[1] + (o_end[1] - o_near[1]) * t)
        bot = (v_near[0] + (v_end[0] - v_near[0]) * t, v_near[1] + (v_end[1] - v_near[1]) * t)
        sc = 0.55 + 0.45 * abs(math.sin(t * math.pi * n / 2))                         # the scallops
        val.append((top[0] + (bot[0] - top[0]) * sc, top[1] + (bot[1] - top[1]) * sc))
    val += [o_end]
    mv = mask_poly((H, W), val, soft=0.4, wobble=0.5, seed=seed)
    a = np.maximum(m, mv)
    canvas = depth.near_tone(col("#8a5a3a"), SHADE, k=0.70, warm=0.05)
    c = np.broadcast_to(canvas, (H, W, 3)).copy()
    # the canvas sags between its battens: soft bands across, lines toward the vanishing point
    ang = np.arctan2(Y - vy, X - vx)
    c *= (0.86 + 0.20 * (0.5 + 0.5 * np.sin(ang * 60.0)))[..., None]
    vc = depth.near_tone(col("#9a3c2a"), SHADE, k=0.64, warm=0.05)                     # the valance, a red border
    c = lerp(c, np.broadcast_to(vc, c.shape), mv[..., None])
    r = depth.rim(a, light=TO_SUN, width=2.0)                                          # its edges toward the light
    c = lerp(c, lerp(c, col(BOUNCE), 0.45), (r * 0.6)[..., None])
    return np.clip(c, 0, 1), a


import math  # (cloth uses it)


def near_plane():
    c, a = near_house()
    ac, aa = awning()
    c = c * (1 - aa[..., None]) + ac * aa[..., None]
    a = np.maximum(a, aa)
    for spec in CLOTHS:
        cc, ca = cloth(spec)
        c = c * (1 - ca[..., None]) + cc * ca[..., None]
        a = np.maximum(a, ca)
    # (the house's corner: the long cloth hangs in front of it, nearer)
    # all of it in the tall house's shade: as deep as the darkest of the picture (measured: the plane's mean light to
    # about a tenth), then the rims laid again over the deepened plane
    lum = c @ np.array([0.30, 0.55, 0.15], dtype=F32)
    mean = float((lum * a).sum() / max(a.sum(), 1))
    f = float(np.clip(NEAR_LUM / max(mean, 1e-3), 0.45, 1.0))
    c = c * f
    c = c * np.array([1.30, 0.94, 0.62], dtype=F32)                           # a frankly warm note (the same light), so it
    c[..., 0] = np.minimum(c[..., 0] + 0.010, 1)                              # stays warm when keyed (warm darks turn violet)
    r = depth.rim(a, light=TO_SUN, width=1.8) * 0.55 + depth.rim(a, light=(-1.0, 0.15), width=1.6) * 0.45
    c = lerp(c, lerp(c, col(BOUNCE), 0.42), np.clip(r, 0, 0.6)[..., None])
    print("near: mean light %.3f, deepened by %.2f" % (mean, f))
    return c, a


# ---------------------------------------------------------------------------------------------------- the back
def wedge_shadow(back):
    """The near house's shadow on the sunlit corner of the house opposite (the snack bar's upper floor): on its front
    (z 330, facing us) and on its side (x -250, facing the street), where the sun's ray from the wall passes through the
    near house (x >= NEAR_X, z <= NEAR_Z, up to NEAR_H). Only where the wall is in the sun now (warm and light)."""
    lx, ly, lz = LIGHT
    sx, sy, sz = -lx, -ly, -lz                       # toward the sun
    # the front wall, z = 330: its picture strip
    zf = 330.0
    kf = cam.scale(zf)
    Xw = (X - cam.vx) / kf
    Yw = cam.eye - (Y - cam.vy) / kf
    s_enter = np.maximum((NEAR_X - Xw) / sx, (zf - NEAR_Z) / -sz)
    front_in = (Yw + sy * s_enter <= NEAR_H) & (Xw >= -585) & (Xw <= -250) & (Yw > 300) & (Yw < 640)
    # the side wall, x = -250, from z 330 to 930
    xs_ = -250.0
    ks = np.maximum((cam.vx - X) / -xs_, 1e-3)
    Zs = cam.F / ks - cam.Z0
    Ys = cam.eye - (Y - cam.vy) / ks
    s2 = np.maximum((NEAR_X - xs_) / sx, (Zs - NEAR_Z) / -sz)
    side_in = (Ys + sy * s2 <= NEAR_H) & (Zs >= 330) & (Zs <= 930) & (X < cam.vx) & (Ys > 300) & (Ys < 640)
    m = (front_in | side_in).astype(F32)
    # a soft, slightly ragged edge (the near house's eave and its tiles)
    m = blur(m, 0.9)
    rag = noise((H, W), 6, 77, 3)
    m = np.clip((m - 0.5) * 2.2 + (rag - 0.5) * 0.5 + 0.5, 0, 1)
    # only on the sunlit wall: warm and light now (the shade already there stays as it is)
    lum = back @ np.array([0.30, 0.55, 0.15], dtype=F32)
    sunny = np.clip((lum - 0.55) / 0.12, 0, 1) * np.clip((back[..., 0] - back[..., 2] - 0.18) / 0.10, 0, 1)
    sunny = blur(sunny, 1.2)
    g = m * sunny * 0.92
    shade = back * np.array([0.50, 0.51, 1.04], dtype=F32)                          # as the painter's shadows on these walls
    shade = shade + np.array([0.05, 0.02, 0.0], dtype=F32) * (1 - np.clip((Y - 140) / 90, 0, 1))[..., None]  # a warm bounce high up
    return lerp(back, np.clip(shade, 0, 1), g[..., None]), g


def far_map(back):
    """How far each pixel is, 0 near to 1 the Forum, from the camera: the nearest of the ground and the two house
    fronts on the view ray; the sky left out (it is the air)."""
    kg = np.where(Y > cam.vy + 0.5, (Y - cam.vy) / cam.eye, 0.0)
    kl = np.where(X < cam.vx, (cam.vx - X) / 250.0, 0.0)
    kr = np.where(X > cam.vx, (X - cam.vx) / 420.0, 0.0)
    k = np.maximum(np.maximum(kg, kl), kr)
    z = cam.F / np.maximum(k, 1e-3) - cam.Z0
    f = np.clip((z - 1800.0) / (7500.0 - 1800.0), 0, 1) ** 0.85
    r, g, b = back[..., 0], back[..., 1], back[..., 2]
    sky = ((g - r > 0.035) & (b > g) & (Y < 250)).astype(F32)
    sky = blur(sky, 1.0)
    return blur(f, 1.5) * (1 - sky)


def deepen_near(back):
    """The near ground and the bottom corners a little deeper (a thin glaze: people stand there)."""
    low = np.clip((Y - 470) / 130, 0, 1) ** 1.3
    corner = np.clip(((X - 400) / 400) ** 2 + ((Y - 300) / 300) ** 2 - 0.9, 0, 1) * 0.5
    m = np.clip(low * 0.13 + corner * 0.12, 0, 0.22)
    tone = col("#3a2c48") * 1.6
    return back * (1 - m[..., None]) + back * tone * m[..., None]


# ---------------------------------------------------------------------------------------------------- finish
def finish_back(pic, name):
    pal = palette_of([pic.reshape(-1, 1, 3)], colors=152)
    idx = to_palette(pic, pal, speckle=0.008)
    save(name, idx, pal)


def finish_cut(c, a, name, colors, seed=7):
    g = grain(c, seed, 0.02)
    pal = palette_of([g[a > 0.5].reshape(-1, 1, 3)], colors=colors)
    idx = to_palette(g, pal, speckle=0.014)
    save(name, idx, pal, a)


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(ORIG):                                      # every file as it was ...
        if f != "back.png":
            shutil.copy2(os.path.join(ORIG, f), os.path.join(OUT, f))
    back, _ = load("back.png")
    back, g = wedge_shadow(back)                                    # ... the back deepened
    far = far_map(back)
    depth.air(back, far, SKY_LOW, amount=0.30)
    back = deepen_near(back)
    finish_back(np.clip(back, 0, 1), os.path.join(OUT, "back.png"))
    c, a = near_plane()                                             # ... and the near plane
    finish_cut(c, a, os.path.join(OUT, "near.png"), 64)
    Image.fromarray((np.clip(far, 0, 1) * 255).astype(np.uint8)).save("out/rome-street-work/depth-far.png")
    Image.fromarray((np.clip(g, 0, 1) * 255).astype(np.uint8)).save("out/rome-street-work/depth-wedge.png")
    print("near covers %.1f%% of the picture" % (100 * float((a > 0.5).mean())))


if __name__ == "__main__":
    main()

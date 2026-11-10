"""The fast depth pass (round twenty-three, wave two: DEPTH.md, LITE.md) over PAINT-21D's Inari theatre, edo-theatre.

    python3 edo_theatre_depth.py          reads out/edo-theatre-orig/ (edo_theatre.py's full run, kept as it was) and
                                          writes the scene's whole set again into out/edo-theatre/, plus near.png

It works over the finished painting and changes no existing script. One camera: edo_theatre_model.VIEW (room.View; the
lens 405 cm up, turned 25 degrees to the right). The light kept: the house's daylight from its high windows (from the
far right, falling toward us and to the left), the backstage dim warmed by the lamp.

NEAR (near.png, plane "front", last): what stands by the lens in the backstage room, in shade, warm and deep, lit only along
the edge that faces the lamp and the lit hall: a post of the wing at the right (its foot far below the frame; it runs off
the top, the right and the bottom), a beam across the top under the backstage ceiling, and the edge of a black masking
drape hanging at the left. The troupe's boxes (front.png) stay, darker and warmer.

BACK (back.png, and the show's layer the same way, so the two meet without a seam): the floorboards of the wing, the stage
and the backstage room drawn again in the camera's perspective (joints along X every 28 or 30 cm as painted, butt joints,
a shade to each board, knots and nail heads fewer and larger near us); the lamp's warm pool on the floor and the wall; the
stage a step brighter than the wing; the house beyond the rail in the air of its own daylight (the far wall a little
cooler and paler); the near floor deeper; one large shadow over the near right of the floor from the backstage room's
right side, out of the picture, its edge along the daylight's direction, leading in toward the stage; shadows of the
boxes and the stand away from the lamp.

JAPAN: watercolor.wash (seed 1830, amount 0.6: a lamplit room), every cut-out and near.png washed over the unwashed
backdrop with wash_cut(crisp=True); the shafts of light (frames) and layout.json as they were. One palette (160) for all.
"""

import math
import os
import shutil
import sys
import time

T0 = time.time()

import numpy as np
from PIL import Image

from brush import F32, lerp, blur, noise, mask_poly, grid, step, rgb, Sheet, palette_of, to_palette, save
import depth as D
import watercolor as WC
from room import View
import edo_theatre_model as M
from edo_keep_kit import P, PAPER, NAPLES, OCHRE, SIENNA, PRUSSIAN, COBALT, ULTRA, CERULEAN, hash01

SRC = "out/edo-theatre-orig"
OUT = "out/edo-theatre"
V = View(**M.VIEW)
H, W = 600, 800
SHAPE = (H, W)
SEED = 1830
AMOUNT = 0.6                                       # a lamplit room: the darks stay deep
CUTS = ["robes", "stagerail", "lamp", "boypuppet", "curtain", "gate", "housefront", "front", "gate-show", "housefront-show"]
COPY = ["shaft-house.png", "shaft-stage.png", "layout.json"]

PLANK = lerp(SIENNA, OCHRE, 0.35)
LAMPLIT = lerp(lerp(OCHRE, NAPLES, 0.55), PAPER, 0.1)
CURT = lerp(ULTRA, PRUSSIAN, 0.62)
CURT_L = lerp(ULTRA, PRUSSIAN, 0.40)
DAY_AIR = lerp(lerp(PAPER, NAPLES, 0.35), CERULEAN, 0.08)      # the house's lit air
COOL_AIR = lerp(PAPER, CERULEAN, 0.22)

# the scene file's numbers (edo-theatre.js): the walk, the blocked patches, the areas the near plane must not hide
STAGE_FLOOR = [(19, 509), (45, 504), (69, 499), (93, 495), (116, 491), (138, 486), (160, 482), (161, 486), (161, 489), (162, 493), (162, 497),
               (163, 501), (163, 505), (184, 501), (204, 497), (224, 493), (244, 489), (262, 485), (281, 481), (279, 478), (277, 474), (275, 471),
               (273, 467), (271, 464), (270, 461), (278, 460), (286, 458), (294, 456), (303, 455), (311, 453), (319, 452), (322, 457), (327, 462),
               (331, 468), (335, 474), (340, 480), (344, 486), (351, 484), (358, 483), (365, 481), (372, 480), (378, 478), (385, 477), (379, 471),
               (373, 465), (368, 459), (363, 453), (358, 448), (353, 443), (405, 433), (453, 424), (498, 415), (540, 407), (578, 400), (615, 393),
               (619, 395), (623, 397), (627, 399), (632, 400), (636, 402), (641, 404), (637, 406), (632, 407), (628, 409), (647, 417), (668, 427),
               (691, 437), (716, 448), (743, 461), (773, 474), (785, 475), (798, 475), (798, 594), (2, 594), (2, 564), (3, 560)]
LAMP_PT = (291.0, 486.0)                           # the lamp's foot in the picture (the lamp: X -118, Z 880)
FLAME = (291.0, 396.0)


def load(name):
    im = np.asarray(Image.open(f"{SRC}/{name}.png").convert("RGBA"), F32) / 255.0
    return im[..., :3].copy(), (im[..., 3] > 0.5).astype(F32)


# ================================================================ the floor through the camera
def floor_uv():
    """Every pixel below the horizon -> the floor place (X, Z) it shows, and the size of a pixel there in cm."""
    x, y = grid(SHAPE)
    below = y > V.hz + 0.5
    d = np.where(below, V.eye * V.F / np.maximum(y - V.hz, 0.5), 1e6)
    a = (x - V.cx) * d / V.F
    X = V.cam_x + a * V.rx + d * V.fx
    Z = V.cam_z + a * V.rz + d * V.fz
    fp = d / V.F                                     # cm per pixel across, on the floor there
    return X.astype(F32), Z.astype(F32), below, fp.astype(F32)


def floor_mask(pic, X, Z, below):
    """The visible boards (wing, stage, backstage room): on the floor plan beyond the house, warm in colour (not the
    stand, the rail, the black curtain), not the boxes or the dais."""
    on_plan = below & (Z > M.WING[2] + 2) & (X > M.WING[0]) & (X < M.HALL_X1 - 2) & (Z < 2400)
    warm = (pic[..., 0] - pic[..., 2]) > 0.035
    m = (on_plan & warm).astype(F32)
    m *= 1 - mask_poly(SHAPE, [(168, 402), (274, 402), (274, 496), (168, 496)], soft=1.0)          # the boxes under the shelf
    m *= 1 - mask_poly(SHAPE, [(533, 334), (606, 326), (728, 362), (728, 390), (650, 405), (533, 360)], soft=1.0)   # the dais
    return m


def thin_line(u, period, fp, offset=0.0, width=1.0):
    f = np.mod(u - offset, period)
    f = np.minimum(f, period - f)
    return np.clip(1 - f / (fp * width + 1e-6) + 0.5, 0, 1)


def boards(pic, m, X, Z, fp, zone, width, offset, seed, joint=0.30):
    """Each board its own shade, a grain along it, the long joints along X and the butt joints across, darker as they
    come near (wider in pixels: true size through the camera)."""
    ids = np.floor((Z - offset) / width).astype(np.int64)
    k = hash01(ids, seed) - 0.5
    streak = np.sin(X / 23.0 + ids * 1.7) * np.sin(X / 71.0 + ids * 0.37)
    shade = 1 + 0.085 * k + 0.022 * streak
    mm = m * zone
    pic[...] = pic * (1 + (shade - 1) * mm)[..., None]
    # the long joints (one pixel far off, two or three near), the butt joints every 1.8 to 3.2 m, staggered
    fpz = np.maximum(fp, 0.05)
    j = thin_line(Z, width, fpz * 0.9, offset, 1.0)
    per = 180.0 + 140.0 * hash01(ids, seed + 5)
    off = per * hash01(ids, seed + 9)
    f = np.mod(X - off, per)
    f = np.minimum(f, per - f)
    b = np.clip(1 - f / (fpz * 1.2 + 1e-6) + 0.5, 0, 1)
    near = np.clip((np.max(fpz) - fpz) / np.max(fpz), 0, 1)
    lines = np.maximum(j, b * 0.85) * mm
    dark = lerp(np.array([0.30, 0.20, 0.22], F32), np.array([0.25, 0.16, 0.18], F32), 0.5)
    a = lines * joint
    pic[...] = pic * (1 - a[..., None]) + pic * dark * 1.6 * a[..., None]
    # a lit lip on the near side of each long joint (the board's edge catching the house's light), far boards only faintly
    lip = thin_line(Z, width, fpz * 0.9, offset + fpz * 1.6, 1.0) * mm * (1 - j)
    pic[...] = np.clip(pic + (lip * 0.035)[..., None], 0, 1)


def knots(pic, m, seed):
    """Knots and nail heads: few and large near us, many and small far off (depth.scatter through the camera)."""
    pt = lambda X, Z: V.pt(X, 0, Z)
    kpc = lambda X, Z: V.scale_at(X, Z)
    S = Sheet(SHAPE)
    for (x, y, k, r) in D.scatter(pt, kpc, (-800.0, 800.0, 780.0, 1900.0), 1.6, seed, size=(5.0, 2.0), zone=m):
        rx = max(0.6, 2.6 * k * (0.7 + 0.6 * r))
        ry = max(0.45, rx * np.clip((y - V.hz) / 520.0, 0.18, 0.7))
        S.ellipse(x, y, rx, ry, "#3a2620", alpha=0.45 if r < 0.7 else 0.3)
    for (x, y, k, r) in D.scatter(pt, kpc, (-800.0, 800.0, 780.0, 1900.0), 3.0, seed + 1, size=(1.4, 1.4), zone=m):
        rr = max(0.45, 0.7 * k)
        S.ellipse(x, y, rr, rr * 0.6, "#2c2028", alpha=0.5)
    c, a = S.done()
    a = a * m
    pic[...] = pic * (1 - a[..., None]) + c * a[..., None]


def deepen(pic, fl, X, Z, below, fp, seed=7):
    """The backdrop deepened (the same for the backdrop and the show's state, pixel for pixel where they agree)."""
    out = pic.copy()
    x, y = grid(SHAPE)
    # --- the boards
    stage = ((X >= M.STAGE[0]) & (X <= M.STAGE[1]) & (Z >= M.STAGE[2]) & (Z <= M.STAGE[3])).astype(F32)
    boards(out, fl, X, Z, fp, 1 - stage, 28.0, 4.0, 31, joint=0.34)
    boards(out, fl, X, Z, fp, stage, 30.0, 12.0, 33, joint=0.28)
    knots(out, fl, seed + 40)
    # --- the stage a step brighter than the wing (its polished boards take the hall's light)
    st = blur(stage * fl, 1.0)
    out = out * (1 + 0.10 * st)[..., None] + (lerp(NAPLES, OCHRE, 0.4) * 0.025)[None, None, :] * st[..., None]
    # --- the lamp's pool: on the floor round its foot (in floor centimetres), and on the wing's wall round the flame
    r = np.hypot(X + 118.0, Z - 880.0)
    pool = np.exp(-(r / 150.0) ** 2) * fl * below
    glow_w = np.exp(-(((x - FLAME[0]) / 120.0) ** 2 + ((y - FLAME[1]) / 95.0) ** 2)) * (1 - fl) * (y < 500)
    warm = lerp(LAMPLIT, NAPLES, 0.3)
    for m_, k_ in ((pool, 0.30), (glow_w, 0.16)):
        a = (m_ * k_)[..., None]
        out = out * (1 - a) + (1 - (1 - out) * (1 - warm * 0.8)) * a           # a screen of the lamp's naples
    # --- the boxes and the stand: their shadows thrown from the lamp, away from it, soft, on the floor
    sh = mask_poly(SHAPE, [(176, 484), (262, 482), (240, 506), (150, 512)], soft=5.0, wobble=1.5, seed=3) * 0.42
    sh = np.maximum(sh, mask_poly(SHAPE, [(304, 518), (322, 516), (346, 588), (318, 592)], soft=4.0, wobble=1.0, seed=4) * 0.30)
    sh *= fl
    out = out * (1 - sh[..., None]) + out * rgb("#3c2c40")[None, None, :] * 1.5 * sh[..., None]
    # --- one large shadow from outside the picture: the backstage room's right side cuts off the house's daylight
    # (from the far right, toward us and the left: its lines run to the day's vanishing point on the horizon) over the
    # near right of the floor; its edge leads in from the bottom toward the stage and the house front
    vp = (1462.0, 190.0)
    def along(px, py, xx):
        return py + (xx - px) * (vp[1] - py) / (vp[0] - px)
    edge = [(250.0, 600.0)] + [(xx, along(250.0, 600.0, xx)) for xx in (330.0, 420.0, 520.0, 620.0, 720.0, 800.0)]
    big = mask_poly(SHAPE, edge + [(800.0, 600.0)], soft=9.0, wobble=4.0, seed=12)
    big = big * (0.80 + 0.20 * noise(SHAPE, 60, 13, 3)) * fl * 0.40
    out = out * (1 - big[..., None]) + out * rgb("#46344e")[None, None, :] * 1.5 * big[..., None]
    # --- the near floor deeper, and the frame's corners
    low = step(470, 600, y) * 0.16 * fl
    out = out * (1 - low[..., None]) + out * rgb("#3a2a3c")[None, None, :] * 1.5 * low[..., None]
    D.frame(out, amount=0.10, bottom=0.0, color="#2a2032")
    # --- the house beyond the rail in its own day's air; its far wall a little cooler and paler
    house = mask_poly(SHAPE, [(281, 100), (800, 40), (800, 392), (724, 392), (609, 389), (344, 441), (281, 447)], soft=3.0)
    farwall = house * (1 - step(250, 300, y))
    D.air(out, house, DAY_AIR, amount=0.13)
    D.air(out, farwall, COOL_AIR, amount=0.08)
    return np.clip(out, 0, 1).astype(F32)


def wet_map():
    """WET: a room, so nothing is wet but the hall's high air (the far wall and the windows' light), a little."""
    x, y = grid(SHAPE)
    house = mask_poly(SHAPE, [(281, 100), (800, 40), (800, 392), (724, 392), (609, 389), (344, 441), (281, 447)], soft=8.0)
    return (house * (1 - step(230, 300, y)) * 0.35).astype(F32)


# ================================================================ the near plane
def near_cut(seed=5):
    """near.png: the post of the wing at the right, the beam across the top, the masking drape's edge at the left."""
    rng = np.random.default_rng(seed)
    wood = lerp(lerp(SIENNA, OCHRE, 0.35), PRUSSIAN, 0.52)
    wood_f = D.near_tone(wood, k=0.46, warm=0.05)              # the faces turned to us: deep and warm
    wood_s = D.near_tone(lerp(wood, PLANK, 0.30), k=0.40, warm=0.07)   # the faces turned to the lamp
    curt = D.near_tone(lerp(CURT, SIENNA, 0.30), k=0.52, warm=0.05)
    curt_l = D.near_tone(lerp(CURT_L, SIENNA, 0.28), k=0.28, warm=0.05)
    parts = {}

    # --- the post: an 18 cm squared timber 2.4 m from the lens, at the right; we see its face toward us and its left face
    S = Sheet(SHAPE)
    Xp, Zp, hw = -79.0, 1543.0, 9.0
    faces = V.box(Xp - hw, Xp + hw, -400.0, 900.0, Zp - hw, Zp + hw)
    for name, pp, nrm in faces:
        if name in ("front", "left") and len(pp) >= 3:
            S.poly(pp, wood_f if name == "front" else wood_s)
    # its grain: long hand lines down it, a check (split) or two
    xl = min(p[0] for nm, pp, nr in faces if nm in ("front", "left") for p in pp)
    for i in range(9):
        gx = xl + 4 + rng.uniform(0, 44)
        pts = [(gx + math.sin(t * 0.021 + i) * 1.4, t) for t in np.arange(-4, 606, 30)]
        S.line(pts, lerp(wood_f, rgb("#1c1418"), 0.45), rng.uniform(0.5, 1.0), alpha=0.55)
    S.line([(xl + 30, 140), (xl + 31, 230), (xl + 29.5, 300)], rgb("#160f14"), 1.4, alpha=0.8)
    parts["post"] = S.done()

    # --- the beam across the top: along X, 1.0 m nearer than the head of the opening, its underside 4.9 m up
    S = Sheet(SHAPE)
    Zb, y0, y1, wz = 1330.0, 487.0, 507.0, 9.0
    xa, xb = -1400.0, 900.0                          # (its right end runs on behind the post)
    front_ = V.poly([(xa, y0, Zb + wz), (xb, y0, Zb + wz), (xb, y1, Zb + wz), (xa, y1, Zb + wz)])
    under = V.poly([(xa, y0, Zb - wz), (xb, y0, Zb - wz), (xb, y0, Zb + wz), (xa, y0, Zb + wz)])
    S.poly(under, wood_s)
    S.poly(front_, wood_f)
    for i in range(5):
        t0 = rng.uniform(0.05, 0.9)
        a_ = V.pt(lerp(xa, xb, t0), y0 + 8 + i * 4, Zb + wz)
        b_ = V.pt(lerp(xa, xb, min(t0 + 0.12, 0.99)), y0 + 8 + i * 4 + rng.uniform(-1, 1), Zb + wz)
        S.line([a_, b_], lerp(wood_f, rgb("#1c1418"), 0.4), 0.8, alpha=0.5)
    parts["beam"] = S.done()

    # --- the masking drape's edge at the left: black cloth hanging from the beam, drawn back to the frame's edge, its
    # folds falling to the floor as a narrow edge (a few pixels of it over the door's frame and the puppets' rail)
    S = Sheet(SHAPE)
    def edge_x(yy):
        # the drape's free edge: out to 58 px under the beam, drawn back to 14 px by 300, then straight down
        t = np.clip((yy - 40.0) / 260.0, 0, 1)
        return 14.0 + (58.0 - 14.0) * (1 - t) ** 1.6 + 2.0 * math.sin(yy / 23.0)
    ys = np.arange(-6.0, 610.0, 6.0)
    outline = [(-6.0, -6.0)] + [(edge_x(yy), yy) for yy in ys] + [(-6.0, 610.0)]
    S.poly(outline, curt)
    # the folds: lighter ridges and deep troughs, running down and in toward the edge
    for i, f0 in enumerate((0.18, 0.42, 0.66, 0.86)):
        pts = [(edge_x(yy) * f0 + rng.normal(0, 0.4), yy) for yy in ys]
        S.taper(pts, curt_l if i % 2 == 0 else lerp(curt, rgb("#120c16"), 0.45), 3.4, 1.2)
    parts["drape"] = S.done()

    # --- together, with the rims: the post's left edge and the beam's underside catch the lamp and the lit hall; the
    # drape's free edge (its right) the same
    c = np.zeros(SHAPE + (3,), F32)
    a = np.zeros(SHAPE, F32)
    rims = {"drape": (1.0, 0.25), "beam": (-0.3, 1.0), "post": (-1.0, 0.15)}
    for name in ("drape", "beam", "post"):
        cc, aa = parts[name]
        hard = (aa > 0.5).astype(F32)
        rim = D.rim(hard, light=rims[name], width=2.0)
        lit = np.clip(cc * 1.5 + np.array([0.16, 0.10, 0.02], F32), 0, 1)
        cc = lerp(cc, lit, (np.clip(rim, 0, 1) * 0.65)[..., None])
        c = c * (1 - aa[..., None]) + cc * aa[..., None]
        a = np.maximum(a, aa)
    # the wood and cloth a little uneven (a wash is never flat): darker toward the frame's edges
    x, y = grid(SHAPE)
    vary_ = 1 + 0.06 * (noise(SHAPE, 40, seed + 3, 3) - 0.5)
    edge_dark = 1 - 0.18 * np.clip((x - 760) / 40.0, 0, 1) - 0.12 * np.clip((24 - x) / 24.0, 0, 1) - 0.10 * np.clip((30 - y) / 30.0, 0, 1)
    c = np.clip(c * (vary_ * edge_dark)[..., None], 0, 1)
    return c.astype(F32), a.astype(F32)


def darker_warmer(c, a, k=0.20, warm=0.04):
    """The old front plane (the troupe's boxes) made to count: deeper, warmer."""
    out = lerp(c, rgb("#2a1c24"), k)
    out[..., 0] = np.clip(out[..., 0] + warm, 0, 1)
    return out.astype(F32)


# ================================================================ the whole set
def main():
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back")
    show_c, show_a = load("show")
    cuts = {n: load(n) for n in CUTS}
    X, Z, below, fp = floor_uv()
    show_full = back * (1 - show_a[..., None]) + show_c * show_a[..., None]
    fl = floor_mask(back, X, Z, below)
    fl_s = floor_mask(show_full, X, Z, below)
    back_d = deepen(back, fl, X, Z, below, fp)
    show_d = deepen(show_full, fl_s, X, Z, below, fp)
    near_c, near_a = near_cut()
    fc, fa = cuts["front"]
    cuts["front"] = (darker_warmer(fc, fa), fa)
    print("deepened", round(time.time() - T0, 1), flush=True)
    # the watercolour, as one sheet of paper: the backdrop, the show's layer over it, and the cut-outs over the unwashed
    # backdrop with the same seed (cut-outs that do not come within 12 px of each other are washed together: the wash
    # reaches only a few pixels, so each comes out as it would alone)
    wet = wet_map()
    back_w = WC.wash(back_d, seed=SEED, amount=AMOUNT, soft=wet, wander=1.4, fleck=0.3)
    out = {"back": (back_w, None)}
    out["show"] = (WC.wash_cut(show_d, show_a, back_d, seed=SEED, amount=AMOUNT, soft=wet, wander=1.4, fleck=0.3, crisp=True), show_a)
    print("washed back and show", round(time.time() - T0, 1), flush=True)
    near_hard = (near_a > 0.5).astype(F32)
    cuts["near"] = (near_c, near_hard)
    reach = {n: blur(a, 4.0) > 0.02 for n, (c, a) in cuts.items()}
    groups = []
    for n in list(cuts):
        for g in groups:
            if not any((reach[n] & reach[m]).any() for m in g):
                g.append(n)
                break
        else:
            groups.append([n])
    for g in groups:
        col = np.zeros(SHAPE + (3,), F32)
        al = np.zeros(SHAPE, F32)
        for n in g:
            c, a = cuts[n]
            col = col * (1 - a[..., None]) + c * a[..., None]
            al = np.maximum(al, a)
        washed = WC.wash_cut(col, al, back_d, seed=SEED, amount=AMOUNT, soft=wet, wander=1.4, fleck=0.3, crisp=True)
        for n in g:
            out[n] = (washed, cuts[n][1])
    print("washed cut-outs in", len(groups), "groups", groups, round(time.time() - T0, 1), flush=True)
    # back to one palette, as the scene's own finish does it (finish_shared: 160 colours, a fine speckle)
    sample = [p if a is None else p[a >= 0.5] for p, a in out.values()]
    sample = [s_.reshape(-1, 1, 3) for s_ in sample if s_.size]
    pal = palette_of(sample, colors=160, seed=9)
    for n, (p, a) in out.items():
        if a is None:
            idx = to_palette(p, pal, seed=10, speckle=0.010)
        else:
            ys_, xs_ = np.where(a >= 0.5)
            idx = np.zeros(SHAPE, np.uint8)
            if len(ys_):
                y0_, y1_, x0_, x1_ = ys_.min(), ys_.max() + 1, xs_.min(), xs_.max() + 1
                idx[y0_:y1_, x0_:x1_] = to_palette(p[y0_:y1_, x0_:x1_], pal, seed=10, speckle=0.010)
        save(f"{OUT}/{n}.png", idx, pal, alpha=a)
    print("saved", round(time.time() - T0, 1), flush=True)
    for f in COPY:
        shutil.copyfile(f"{SRC}/{f}", f"{OUT}/{f}")
    # comps to look at
    comp = Image.open(f"{OUT}/back.png").convert("RGBA")
    order = ["robes", "stagerail", "lamp", "boypuppet", "curtain", "gate", "housefront", "front", "near"]
    for n in order:
        comp.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
    comp.convert("RGB").save("out/edo-theatre-depth-comp.png")
    comp = Image.open(f"{OUT}/back.png").convert("RGBA")
    comp.alpha_composite(Image.open(f"{OUT}/show.png").convert("RGBA"))
    for n in ["stagerail", "lamp", "curtain", "gate-show", "housefront-show", "front", "near"]:
        comp.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
    comp.convert("RGB").save("out/edo-theatre-depth-comp-show.png")
    # what the near plane covers of the areas that must stay in sight
    rafters = np.zeros(SHAPE, F32); rafters[:150, :] = 1
    hf = np.zeros(SHAPE, F32); hf[292:442, 637:797] = 1
    print("near share %.1f%%; of the rafters %.0f%%, of the house front %.0f%%" % (near_hard.mean() * 100,
          (near_hard * rafters).sum() / rafters.sum() * 100, (near_hard * hf).sum() / hf.sum() * 100))


if __name__ == "__main__":
    main()

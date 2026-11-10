#!/usr/bin/env python3
"""The room under the storehouse (edo-chapel), by oil lamp: the fast depth pass (round twenty-three, wave two; DEPTH.md).

    python3 edo_chapel_depth.py     reads out/edo-chapel-orig/ (edo_chapel.py's full run: the painting as installed, before
                                    the keying), writes the whole set back into out/edo-chapel/, every name as before, and
                                    near.png

THE NEAR PLANE (near.png), through the scene's own camera (room.View, edo_chapel_model.VIEW: the lens 130 cm up, a metre
from the near end of the room): the storehouse's floor beam right over the lens, across the top of the frame (its
underside catching a little of the lamps, the arris toward them lit); under it, by the lens at the left edge, a rough
round prop; round that prop's foot, the foot of the earth wall left uncut in the lower left corner. All in the deep warm
shade of the near end of the room, lit only along the edges that face the lamps. The old front post (front.png) is the
same plane: kept in its outline, made deeper and warmer, with the lamps' rim down its left side.

THE BACK (back.png): the mats' rush weave and their binding cords and the wear of feet, the earth floor's clods, pebbles
and charcoal dust, all through the camera so that they shrink with distance; the ladder's two shadows (it had none) from
the lamp on the left wall and the lamp on the stand, laid on the floor by the lamps' own geometry; the far wall a little
cooler and paler, the corners falling into cool dark, the near floor deeper and warmer.

Then the act's watercolour, amount 0.6 (a lamplit room: the darks stay deep): `watercolor.wash` on the backdrop and
`wash_cut` on every cut-out and the near plane, one sheet of paper (seed 1830); and the scene's own palettes
(home_study.finish, the colour counts edo_chapel.py gives each picture)."""

import math
import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import F32, Sheet, blur, grid, lerp, mask_poly, noise, rgb, step, tint
import depth as D
import watercolor as WC
from room import View
import edo_chapel_model as M
from home_study import finish

W, H = 800, 600
SRC = "out/edo-chapel-orig"
OUT = "out/edo-chapel"
SEED = 1830
V = View(**M.VIEW)
AMOUNT = 0.6                                                     # the lamplit room
WANDER, FLECK = 1.4, 0.3
# the colour counts edo_chapel.py finishes each picture with (and the near plane as the front's)
COLORS = {"back": 160, "altar-shut": 64, "mirror": 24, "props": 40, "front": 72, "lamps": 32, "trapdoor-shut": 48,
          "trapdoor-lamp": 40, "ladder": 48, "trapdoor-day": 64, "ladder-day": 48, "altar-open": 72, "lamps-out": 24, "near": 72}
# the lamps' flames, as edo_chapel.py lights them (edo_chapel_things.lamp_places, +2 up)
LAMP_LEFT = (M.NICHE[2] * 0.45, M.LAMPS["lamp-left"][1] + M.LAMP_H + 3.5, M.LAMPS["lamp-left"][2])
LAMP_STAND = (M.LAMPS["lamp-stand"][0], M.LAMPS["lamp-stand"][1] + M.LAMP_H + 3.5, M.LAMPS["lamp-stand"][2])
NAPLES = rgb("#f2d48a")
WARM_DARK = rgb("#2a1a14")


def load(name):
    a = np.asarray(Image.open(f"{SRC}/{name}.png").convert("RGBA"), dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


# ---------------------------------------------------------------- the room's shell, seen through the lens
def shell():
    """Per pixel: the depth along the lens, which surface of the room's box (1 floor, 2 ceiling, 3 left, 4 right, 5 back
    wall), and the room place X, Y, Z there (the things standing in the room are not in it: see standing())."""
    x, y = grid((H, W))
    a = (x + 0.5 - V.cx) / V.F
    u = (V.hz - (y + 0.5)) / V.F
    dX, dZ, dY = a * V.rx + V.fx, a * V.rz + V.fz, u
    big = np.float32(1e9)
    t = np.full((H, W), big, dtype=F32)
    surf = np.zeros((H, W), np.int8)
    with np.errstate(divide="ignore", invalid="ignore"):
        for tt, s in ((np.where(dY < 0, -V.eye / dY, big), 1), (np.where(dY > 0, (M.H - V.eye) / dY, big), 2),
                      (np.where(dX < 0, -V.cam_x / dX, big), 3), (np.where(dX > 0, (M.W - V.cam_x) / dX, big), 4),
                      (np.where(dZ < 0, -V.cam_z / dZ, big), 5)):
            m = (tt > 0) & (tt < t)
            t = np.where(m, tt, t).astype(F32)
            surf = np.where(m, s, surf).astype(np.int8)
    return t, surf, V.cam_x + t * dX, V.eye + t * dY, V.cam_z + t * dZ


def box_poly(X0, X1, Y0, Y1, Z0, Z1):
    pts = [V.pt(X, Y, Z) for X in (X0, X1) for Y in (Y0, Y1) for Z in (Z0, Z1)]
    pts = sorted(set((round(px, 2), round(py, 2)) for px, py in pts))
    # convex hull (monotone chain)
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def standing():
    """A mask of the things that stand in the backdrop (the altar, the stand, the sack, the lamp stand, the basket, the
    jar), so that nothing laid on the floor climbs them."""
    m = np.zeros((H, W), F32)
    for b in M.BOXES:
        m = np.maximum(m, mask_poly((H, W), box_poly(*b[1:]), soft=0.6))
    return np.clip(blur(m, 1.0) * 1.6, 0, 1)


# ---------------------------------------------------------------- the back
def floor_texture(pic, t, surf, X, Z, keep_off):
    """The mats' weave, cords and wear, and the earth's clods, pebbles and charcoal dust: true sizes, so they shrink."""
    _, y = grid((H, W))
    floor = (surf == 1).astype(F32) * (1 - keep_off)
    on_mats = floor * (X > M.MATS[0]) * (X < M.MATS[1]) * (Z > M.MATS[2]) * (Z < M.MATS[3])
    earth = floor * (1 - on_mats)
    across = t / V.F                                               # cm of floor across one pixel
    along = t * t / (V.F * V.eye)                                  # cm of floor along (Z) one pixel
    # the rush runs along each strip (along Z): fine ribs 3.6 cm apart, fading out where they would alias
    rib = np.cos(2 * math.pi * X / 3.6)
    fade = np.clip(1.25 - across / 1.4, 0, 1)
    # binding cords across the strip every 24 cm (thin darker lines), and their shadow side
    zc = (Z % 24.0) - 12.0
    cord_w = np.maximum(0.9, along * 0.55)
    cord = np.exp(-(zc / cord_w) ** 2) * np.clip(1.6 / (along + 0.4), 0, 1)
    # wear: where feet go the straw is darker and smoother; elsewhere a little paler (in floor places, so it shrinks too)
    wear = (noise((H, W), 26, SEED + 3, 4) - 0.5)
    strip = np.floor((X - M.MATS[0]) / M.MAT_W)
    tone = ((strip * 0.6180339) % 1.0 - 0.5) * 0.07                # each strip a slightly different straw
    toward = np.clip((y - 352.0) / 80.0, 0, 1)                      # the mats a shade deeper toward us
    mult = 1 + on_mats * (0.050 * rib * fade - 0.16 * cord + 0.12 * wear + tone - 0.09 * toward)
    pic *= mult[..., None]
    # bits on the mats: charcoal dust walked down the ladder, a few broken rushes
    sh = Sheet((H, W))
    for x, y, k, r in D.scatter(lambda a, b: V.pt(a, 0, b), V.scale_at, (M.MATS[0], M.MATS[1], M.MATS[2], M.MATS[3]), 9.0,
                                SEED + 4, size=(2.2, 1.0), zone=on_mats):
        if r < 0.55:
            sh.ellipse(x, y, max(0.5, 1.1 * k), max(0.4, 0.45 * k), "#3a3040", 0.45)
        else:
            L = (3 + 5 * r) * k
            sh.line([(x - L * 0.5, y + 0.15 * L * (r - 0.75)), (x + L * 0.5, y - 0.15 * L * (r - 0.75))], "#d8b868", max(0.5, 0.35 * k), 0.55)
    c, a = sh.done()
    pic[...] = pic * (1 - a[..., None]) + c * a[..., None]
    # the earth floor: hollows trodden smooth, clods with their lit far side, pebbles, charcoal dust
    sh = Sheet((H, W))
    for x, y, k, r in D.scatter(lambda a, b: V.pt(a, 0, b), V.scale_at, (0, M.W, 0, 598), 1.4, SEED + 5, size=(30, 30), zone=earth):
        sh.ellipse(x, y, 14 * k * (0.7 + 0.6 * r), 4.2 * k * (0.7 + 0.6 * r), "#2e2432", 0.16)
    for x, y, k, r in D.scatter(lambda a, b: V.pt(a, 0, b), V.scale_at, (0, M.W, 0, 598), 9.0, SEED + 6, size=(3.0, 3.0), zone=earth):
        s = (1.0 + 2.4 * r) * k
        sh.ellipse(x, y + 0.25 * s, s, 0.5 * s, "#2a2230", 0.38)                 # its shade side toward us
        sh.ellipse(x, y - 0.12 * s, 0.7 * s, 0.26 * s, "#6e5c4c", 0.26)          # its top toward the lamps
    for x, y, k, r in D.scatter(lambda a, b: V.pt(a, 0, b), V.scale_at, (0, M.W, 0, 598), 4.0, SEED + 7, size=(8, 8), zone=earth):
        sh.ellipse(x, y, (4 + 6 * r) * k, (1.4 + 2 * r) * k, "#1c1820", 0.30)     # charcoal dust
    c, a = sh.done()
    pic[...] = pic * (1 - a[..., None]) + c * a[..., None]
    return pic


def ladder_shadow(lamp, amount, seed):
    """The ladder's shadow on the floor from one lamp (a point): its two rails and its rungs, each place of them laid down
    along the lamp's ray, softer as it lengthens."""
    Lx, Ly, Lz = lamp
    lad = M.LADDER
    X0, X1 = lad["x"]
    r = lad["rail"] / 2

    def z_at(Y):
        return lad["foot_z"] + (lad["top_z"] - lad["foot_z"]) * Y / lad["top_y"]

    def down(X, Y, Z):
        k = Ly / (Ly - Y)
        return Lx + (X - Lx) * k, Lz + (Z - Lz) * k, k

    sharp, soft = Sheet((H, W)), Sheet((H, W))
    ymax = Ly * 0.82
    for xr in (X0 + r, X1 - r):
        ys = np.linspace(0, ymax, 28)
        for y0, y1 in zip(ys[:-1], ys[1:]):
            a0, b0, k0 = down(xr, y0, z_at(y0))
            a1, b1, k1 = down(xr, y1, z_at(y1))
            if not (0 <= a1 <= M.W and 0 <= b1 <= 598):
                break
            w0, w1 = r * k0, r * k1
            # the strip's two edges, across the ray (on the floor: X across the ray direction)
            dx, dz = a1 - a0, b1 - b0
            n = math.hypot(dx, dz) or 1.0
            nx, nz = -dz / n, dx / n
            quad = [V.pt(a0 + nx * w0, 0, b0 + nz * w0), V.pt(a1 + nx * w1, 0, b1 + nz * w1),
                    V.pt(a1 - nx * w1, 0, b1 - nz * w1), V.pt(a0 - nx * w0, 0, b0 - nz * w0)]
            (sharp if k1 < 1.9 else soft).poly(quad, "#000000", float(np.clip(1.25 / k1, 0.3, 1.0)))
    Y = lad["rung"]
    while Y < ymax:
        a0, b0, k0 = down(X0 + r, Y, z_at(Y))
        a1, b1, k1 = down(X1 - r, Y, z_at(Y))
        if 0 <= a0 <= M.W and 0 <= a1 <= M.W and b0 <= 598 and b1 <= 598:
            p0, p1 = V.pt(a0, 0, b0), V.pt(a1, 0, b1)
            th = max(0.8, 1.6 * k0 * V.scale_at(a0, b0))
            (sharp if k0 < 1.9 else soft).line([p0, p1], "#000000", th, float(np.clip(1.25 / k0, 0.3, 1.0)))
        Y += lad["rung"]
    _, a = sharp.done()
    _, b = soft.done()
    m = np.clip(blur(a, 0.7) + blur(b, 1.8), 0, 1)
    return m * amount


def deepen_back(pic, t, surf, X, Z):
    keep_off = standing()
    floor = (surf == 1).astype(F32)
    pic = floor_texture(pic, t, surf, X, Z, keep_off)
    # the ladder had no shadow: the lamp on the left wall throws it right and toward us, the lamp on the stand left and
    # toward us; cool glazes, on the floor only
    sh = np.clip(ladder_shadow(LAMP_LEFT, 0.42, 1) + ladder_shadow(LAMP_STAND, 0.34, 2), 0, 0.6) * floor * (1 - keep_off)
    tint(pic, rgb("#5a5490") * 1.25, sh)
    # the far wall a little cooler and paler (the air of a small room: not much), the far floor and ceiling with it
    far = np.clip((t - 300.0) / (590.0 - 300.0), 0, 1)
    D.air(pic, far, "#a9adc6", amount=0.13, power=1.2)
    # the corners falling into cool dark: away from the lamps' pools, where it is already dark, a cool glaze
    x, y = grid((H, W))
    L = pic @ np.array([0.30, 0.55, 0.15], F32)
    away = np.clip(((x - 390) / 430) ** 2 + ((y - 300) / 330) ** 2, 0, 1.6)
    dark = np.clip((0.42 - L) / 0.30, 0, 1)
    tint(pic, rgb("#7078b8"), np.clip(away * dark * 0.30, 0, 0.35))
    # the near floor deeper and warmer (toward the near plane's warm dark): nothing from the full row in, all of it at
    # the frame's foot
    near = floor * np.clip((330.0 - t) / (330.0 - 171.0), 0, 1) ** 1.2
    pic[...] = lerp(pic, pic * rgb("#9a7c6c"), (near * 0.55)[..., None])
    return np.clip(pic, 0, 1)


# ---------------------------------------------------------------- the near plane
def timber_tex(shape, seed, along="v"):
    """Adze and grain: streaks along the timber, a few checks (splits)."""
    cell = (3, 46) if along == "v" else (60, 3)
    g = noise(shape, cell, seed, 4) - 0.5
    adze = noise(shape, (16, 10) if along == "v" else (12, 9), seed + 1, 3) - 0.5
    return g * 0.55 + adze * 0.45


def near_plane(back_orig, front_c, front_a):
    """-> (colour, alpha) of near.png, and the front post re-toned (colour)."""
    props_c, props_a = load("props")
    wood = props_c[props_a > 0.5].mean(axis=0)                       # the props' own timber
    earth = back_orig[560:590, 260:340].reshape(-1, 3).mean(axis=0)  # the earth floor at the near end
    timber_dark = D.near_tone(wood * 0.3, shade="#0e0806", k=0.75, warm=0.02)
    timber_mid = D.near_tone(wood * 0.5, shade="#1c100a", k=0.50, warm=0.04)
    earth_dark = D.near_tone(earth * 0.35, shade="#100a07", k=0.70, warm=0.025)
    x, y = grid((H, W))
    col = np.zeros((H, W, 3), F32)
    alpha = np.zeros((H, W), F32)

    # -- the floor beam overhead: front face (toward us, away from the lamps: the darkest) and underside (a little of the lamps)
    Yb, Yt, Zb, Zf = 170.0, 182.0, 500.0, 514.0
    Xs = np.linspace(0, M.W, 60)
    under_back = [V.pt(X, Yb, Zb) for X in Xs]
    under_front = [V.pt(X, Yb, Zf) for X in Xs]
    top_front = [V.pt(X, Yt + 30, Zf) for X in Xs]
    ub = np.interp(x[0], [p[0] for p in under_back], [p[1] for p in under_back])      # the underside's far arris, per column
    uf = np.interp(x[0], [p[0] for p in under_front], [p[1] for p in under_front])    # the front face's foot
    # hewn by hand: the arris wanders a pixel or two, with a notch here and there
    rng = np.random.default_rng(SEED)
    jag = (noise((1, W), (40, 1), SEED + 11, 3)[0] - 0.5) * 3.0 + (noise((1, W), (9, 1), SEED + 12, 2)[0] - 0.5) * 1.6
    for _ in range(5):
        c0 = rng.uniform(40, 760)
        jag -= 2.2 * np.exp(-((x[0] - c0) / rng.uniform(3, 7)) ** 2)
    ub = ub + jag
    beam = (y < ub[None, :]).astype(F32)
    under = beam * (y >= uf[None, :])
    face = beam * (y < uf[None, :])
    tex = timber_tex((H, W), SEED + 13, "h")
    under_t = np.clip((y - uf[None, :]) / np.maximum(ub - uf, 1)[None, :], 0, 1)        # 0 at its near edge, 1 at the far arris
    c_face = timber_dark[None, None, :] * (1 + 0.30 * tex[..., None])
    c_under = lerp(timber_dark, timber_mid, 0.25 + 0.55 * under_t[..., None]) * (1 + 0.35 * tex[..., None])
    col = col * (1 - beam[..., None]) + (c_face * face[..., None] + c_under * under[..., None])
    alpha = np.maximum(alpha, beam)
    # the arris toward the lamps catches them: brightest over the pools
    pool = np.exp(-((x[0] - 330) / 260) ** 2)
    arris = beam * np.clip(1 - (ub[None, :] - y) / 2.2, 0, 1) * (0.35 + 0.65 * pool[None, :])
    col = lerp(col, lerp(timber_mid, NAPLES, 0.42)[None, None, :], (arris * 0.6)[..., None])
    # the joint of the front face and the underside: a dark line
    col *= (1 - 0.45 * np.exp(-((y - uf[None, :]) / 0.9) ** 2) * beam)[..., None]

    # -- the prop under it by the lens, at the left edge: a rough round timber 17 cm through
    Zp = 506.0
    rp = 8.5
    lo, hi = 0.0, 260.0                                                    # find the X that puts its middle at x = 2
    for _ in range(40):
        mid = (lo + hi) / 2
        if V.pt(mid, 100, Zp)[0] < 2.0:
            lo = mid
        else:
            hi = mid
    Xp = (lo + hi) / 2
    cx = V.pt(Xp, 100, Zp)[0]
    hw = rp * V.F / V.depth(Xp, Zp)
    top = V.pt(Xp, Yb, Zp)[1]
    wob = (noise((H, 1), (1, 30), SEED + 14, 3)[:, 0] - 0.5) * 3.0 + (noise((H, 1), (1, 7), SEED + 15, 2)[:, 0] - 0.5) * 1.4
    right = cx + hw + wob[:, None]
    post = ((x <= right) & (y >= top - 2)).astype(F32)
    u = np.clip((x - cx) / hw, -1, 1)
    lit = np.clip(u * 0.8 + 0.1, 0, 1) ** 2                                # the lamps are to its right
    ptex = timber_tex((H, W), SEED + 16, "v")
    c_post = lerp(timber_dark, timber_mid, lit[..., None] * 0.9) * (1 + 0.32 * ptex[..., None])
    # a check (a split) down it, and the bark left in a strip near its dark side
    check = np.exp(-((x - (cx + hw * 0.35 + 1.5 * np.sin(y / 37.0))) / 0.7) ** 2) * step(120, 160, y) * (1 - step(470, 520, y))
    c_post *= (1 - 0.5 * check)[..., None]
    c_post = lerp(c_post, c_post * rgb("#7a5a48"), (np.exp(-((u + 0.55) / 0.12) ** 2) * 0.6)[..., None])
    col = col * (1 - post[..., None]) + c_post * post[..., None]
    alpha = np.maximum(alpha, post)
    # where it carries the beam: a dark notch under the beam
    seat = post * np.exp(-((y - (top + 1)) / 2.0) ** 2)
    col *= (1 - 0.5 * seat)[..., None]
    # a knee brace from the prop up to the beam (in the prop's plane), with the room seen through the gap it makes
    b0 = V.pt(Xp + rp * 0.6, 147.0, Zp)
    b1 = V.pt(Xp + 30.0, 171.0, Zp)
    bw = 6.5 * V.F / V.depth(Xp, Zp) * 0.5
    dx, dy = b1[0] - b0[0], b1[1] - b0[1]
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * bw, dx / n * bw
    back_y = b0[1] - 30 * dy / dx                                          # its foot run back into the prop
    brace_pts = [(b0[0] - 30 + nx, back_y + ny), (b1[0] + nx, b1[1] + ny), (b1[0] + 18 - nx, b1[1] - ny),
                 (b0[0] - 30 - nx, back_y - ny)]
    brace = mask_poly((H, W), brace_pts, soft=0.4, wobble=0.8, seed=SEED + 20) * (1 - beam)
    v = ((x - b0[0]) * dx + (y - b0[1]) * dy) / (n * n)
    btex = noise((H, W), 10, SEED + 21, 3) - 0.5
    across_b = ((x - b0[0]) * (-dy) + (y - b0[1]) * dx) / n / bw                      # -1 its upper side, +1 its lower
    c_brace = lerp(timber_dark, timber_mid, np.clip(across_b * 0.5 + 0.35, 0, 1)[..., None] * 0.8) * (1 + 0.3 * btex[..., None])
    col = col * (1 - brace[..., None]) + c_brace * brace[..., None]
    alpha = np.maximum(alpha, brace)
    post = np.maximum(post, brace)

    # -- the foot of the earth wall heaped round the prop's foot, in the lower left corner
    ex = np.array([0, 18, 40, 62, 86, 110, 136, 160, 186, 208, 232], F32)
    ey = np.array([476, 482, 490, 499, 512, 524, 540, 556, 572, 588, 604], F32)
    edge = np.interp(x[0], ex, ey) + (noise((1, W), (34, 1), SEED + 17, 3)[0] - 0.5) * 9.0 + (noise((1, W), (8, 1), SEED + 18, 2)[0] - 0.5) * 3.0
    foot = (y >= edge[None, :]).astype(F32)
    etex = noise((H, W), 18, SEED + 19, 4) - 0.5
    depth_in = np.clip((y - edge[None, :]) / 26.0, 0, 1)
    c_earth = lerp(lerp(earth_dark, NAPLES * 0.5, 0.10), earth_dark, depth_in[..., None]) * (1 + 0.38 * etex[..., None])
    # its crest toward the lamps catches them a little
    crest = foot * np.clip(1 - (y - edge[None, :]) / 2.5, 0, 1) * (1 - step(150, 230, x))
    c_earth = lerp(c_earth, lerp(earth_dark, NAPLES, 0.35), (crest * 0.5)[..., None])
    # a few stones in the earth, their lit tops
    sh = Sheet((H, W))
    for i in range(14):
        sx, sy = rng.uniform(0, 200), rng.uniform(0, 1)
        sy = float(np.interp(sx, ex, ey)) + 10 + sy * (600 - float(np.interp(sx, ex, ey)) - 10)
        s = rng.uniform(3, 7)
        sh.ellipse(sx, sy, s, s * 0.6, "#1a120e", 0.8)
        sh.ellipse(sx - 0.6, sy - s * 0.25, s * 0.7, s * 0.3, "#3a2c22", 0.6)
    sc, sa = sh.done()
    c_earth = c_earth * (1 - sa[..., None]) + sc * sa[..., None]
    foot = foot * (1 - post)
    col = col * (1 - foot[..., None]) + c_earth * foot[..., None]
    alpha = np.maximum(alpha, foot)

    # -- the lamps' rim on the near things: the prop's right edge, at the left lamp's height brightest
    a_soft = np.clip(alpha, 0, 1)
    r = D.rim(post, light=(1.0, -0.15), width=2.0) * (0.45 + 0.55 * np.exp(-((y - 300) / 150) ** 2))
    col = lerp(col, lerp(timber_mid, NAPLES, 0.5)[None, None, :], (np.clip(r, 0, 1) * 0.7)[..., None])
    col = np.clip(col, 0, 1)
    alpha = np.clip(a_soft, 0, 1)

    # -- the old front post: the same plane, deeper and warmer, the lamps' rim down its left
    fa = front_a
    fc = front_c.copy()
    fc = lerp(fc, fc * rgb("#c8a090") * 0.92 + rgb("#1c1008") * 0.25, 0.85)
    fr = D.rim(fa, light=(-1.0, -0.2), width=2.0) * (0.5 + 0.5 * np.exp(-((y - 330) / 160) ** 2))
    fc = lerp(fc, lerp(timber_mid, NAPLES, 0.55)[None, None, :], (np.clip(fr, 0, 1) * 0.7)[..., None])
    return col.astype(F32), alpha.astype(F32), np.clip(fc, 0, 1).astype(F32)


# ---------------------------------------------------------------- the watercolour and the palettes
def wet_map(surf):
    """Nothing here is sky or water or far land: the earth ceiling, which the lamps barely reach, a little wet; the rest
    dry (the ground and everything standing)."""
    ceiling = (surf == 2).astype(F32)
    return blur(ceiling, 2.0) * 0.30


def main():
    if not os.path.isdir(SRC):
        sys.exit(f"{SRC} is missing: run edo_chapel.py (full) and copy out/edo-chapel to it first")
    names = [n[:-4] for n in sorted(os.listdir(SRC)) if n.endswith(".png")]
    back, _ = load("back")
    t, surf, X, Y, Z = shell()
    deep = deepen_back(back.copy(), t, surf, X, Z)
    front_c, front_a = load("front")
    near_c, near_a, front_new = near_plane(back, front_c, front_a)
    wet = wet_map(surf)
    os.makedirs(OUT, exist_ok=True)
    washed = WC.wash(deep, seed=SEED, amount=AMOUNT, soft=wet, wander=WANDER, fleck=FLECK)
    finish(washed, f"{OUT}/back.png", COLORS["back"], amount=0.008, speckle=0.007)
    comp = washed.copy()
    for name in names:
        if name == "back":
            continue
        c, a = load(name)
        if name == "front":
            c = front_new
        cw = WC.wash_cut(c, a, deep, seed=SEED, amount=AMOUNT, soft=wet, wander=WANDER, fleck=FLECK, crisp=True)
        finish(cw, f"{OUT}/{name}.png", COLORS.get(name, 48), (a > 0.5).astype(F32), amount=0.008 if name != "lamps-out" else 0.006, speckle=0.007)
    nw = WC.wash_cut(near_c, near_a, deep, seed=SEED, amount=AMOUNT, soft=wet, wander=WANDER, fleck=FLECK, crisp=True)
    finish(nw, f"{OUT}/near.png", COLORS["near"], (near_a > 0.5).astype(F32), amount=0.008, speckle=0.007)
    # a look at the whole: the night with everything as first seen, and the morning
    for label, layers in (("night", ("back", "props", "trapdoor-shut", "altar-shut", "mirror", "lamps", "ladder", "front", "near")),
                          ("day", ("back", "props", "trapdoor-day", "altar-open", "lamps", "ladder-day", "front", "near"))):
        im = Image.open(f"{OUT}/{layers[0]}.png").convert("RGBA")
        for n in layers[1:]:
            im.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
        im.convert("RGB").save(f"out/edo-chapel-depth-comp-{label}.png")
    print("near covers %.1f%%" % (100 * (near_a > 0.5).mean()), "with the front post %.1f%%" % (100 * np.maximum(near_a > 0.5, front_a > 0.5).mean()))


if __name__ == "__main__":
    main()

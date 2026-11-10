"""edo-keeptop in depth (round twenty-three, the fast pass: /home/claude/r23/LITE.md, tools/paint/DEPTH.md): the top floor
of Himeji's keep at sunset, worked over edo_keeptop.py's own painting and not repainted.

    python3 edo_keeptop.py              first (seeded: it paints what is installed), then copy out/edo-keeptop/ to
                                        out/edo-keeptop-orig/ (never changed)
    python3 edo_keeptop_depth.py        reads out/edo-keeptop-orig/, writes every file of out/edo-keeptop/ again, + near.png

ONE CAMERA: edo_keeptop.V (room.View: the lens 175 cm up in the south bay at X 380, Z 760, looking north; focal 400). The
light is the scene's own: the sun due west, 14 degrees up, through the west bay (lit.png); in the dark room (back.png) only
the last of it, in the cracks round the west shutters.

    near     near.png (plane front): the room's tie beam across the top, a hewn log in deep shade seen from below (it runs off
             both sides), carried on the right by an inner post standing a metre in front of the stored chest (cut off by the
             frame's right edge and bottom), a bracket arm under the beam at each post (the left post is just out of the
             frame). Lit only along the edges that face the west window. The old front plane (front.png, the chest at the
             right) made deeper and warmer inside its own outline.
    middle   the floor: every board its own tone, the grain along the boards, knots, the walked middle a little worn, the
             near floor deeper; soft shade at the feet of the walls, the chests, the lantern and the rail, thrown away from
             the west; lit: the sun's patch with the boards' joints through it, its far edges softer, a warm glow round it,
             the shadow of the stairwell's rail lying along its south edge; dark: the last light through the west shutters'
             cracks lying across the floor in thin warm lines (where the patch will be).
    far      the north wall and the far corners a little cooler and paler; the roof deeper toward the frame's top.
    Japan    watercolor.wash on both backdrops (seed 1830; the dark room amount 0.6, the lit one 0.85), every cut-out and
             near.png washed on the same paper (wash_cut, crisp); the views through the bays wet. The herons' frames as
             they were.

Nothing clicked moves; the west bay's view and the east wall at the hum (where the mirror's light lands) are kept as painted
apart from the paper. Then one palette for all (160 colours, as edo_keep_kit.finish_scene does it).
"""

import json
import math
import os
import shutil
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, lerp, blur, noise, mask_poly, Sheet, grid, step, rgb, grain, palette_of, to_palette, save
import depth as D
import watercolor as WC
from edo_keeptop import (V, RW, RD, RH, BAYS, SUN_EL, STAIRWELL, CHESTS, LANTERN, FRONT_CHEST, WOOD_LIT, WOOD_DARK, BEAM_C,
                         bay_mask)
from edo_keep_kit import PAPER, NAPLES, OCHRE, SIENNA, PRUSSIAN, COBALT, ULTRA, SHADE, P

SRC = "out/edo-keeptop-orig"
OUT = "out/edo-keeptop"
SEED = 1830
W, H = 800, 600
SHAPE = (H, W)
LIT_NAMES = ("lit",)
CUTS = ["rail", "rail-lit", "chests", "chests-lit", "lantern", "lantern-lit", "front", "front-lit",
        "northshutter", "northshutter-lit", "eastshutter", "eastshutter-lit", "westshutter", "westshutter-open-lit",
        "northshutter-open", "eastshutter-open", "westshutter-open", "northshutter-open-lit", "eastshutter-open-lit"]
T = math.tan(math.radians(SUN_EL))


def load(name):
    im = Image.open(os.path.join(SRC, name + ".png")).convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def is_lit(name):
    return name == "lit" or name.endswith("-lit")


# ---------------------------------------------------------------- the floor through the camera
X_, Y_ = grid(SHAPE)
DEPTH = np.where(Y_ > V.hz + 0.5, V.F * V.eye / np.maximum(Y_ - V.hz, 0.5), 1e6).astype(F32)
FX = (V.cam_x + (X_ - V.cx) * DEPTH / V.F).astype(F32)
FZ = (V.cam_z - DEPTH).astype(F32)
SX0, SX1, SZ0, SZ1 = STAIRWELL
FLOOR = ((FX >= 0) & (FX <= RW) & (FZ >= 0) & (FZ <= RD) & (Y_ > V.hz + 0.5)).astype(F32)
HOLE = ((FX >= SX0 - 1) & (FX <= SX1 + 1) & (FZ >= SZ0 - 1) & (FZ <= SZ1 + 1)).astype(F32)
BOARDS = FLOOR * (1 - HOLE)
pt = lambda X, Z: V.pt(X, 0, Z)
kpx = lambda X, Z: V.scale_at(X, Z)


def hash01(i, seed):
    i = np.asarray(i, dtype=np.int64)
    v = (i * 374761393 + seed * 668265263) & 0xFFFFFFFF
    v = ((v ^ (v >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((v ^ (v >> 16)) & 0xFFFF).astype(F32) / 65535.0


_TILE = {}


def ground_noise(cu, cv, seed, octaves=3):
    """Noise lying on the floor, its blotches cu cm across and cv cm along (fading where smaller than a pixel)."""
    tile = _TILE.get((seed, octaves))
    if tile is None:
        tile = _TILE[(seed, octaves)] = noise((1024, 1024), 64, seed, octaves)
    u = np.mod(FX / cu * 64 + 300, 2044)
    v = np.mod(FZ / cv * 64 + 300, 2044)
    u = np.where(u > 1022, 2044 - u, u).astype(np.int32).clip(0, 1023)
    v = np.where(v > 1022, 2044 - v, v).astype(np.int32).clip(0, 1023)
    n = tile[v, u]
    k = V.F / np.maximum(DEPTH, 1.0)
    small = np.minimum(cu * k, cv * k * k * V.eye / V.F)
    return (0.5 + (n - 0.5) * np.clip((small - 1.0) / 2.5, 0, 1)).astype(F32)


def floor_texture(pic, lit):
    """Every board its own tone, the grain along it, the walked middle worn, the near floor deeper, knots."""
    band = np.floor((FX - 10.0) / 30.0).astype(np.int64)
    k_board = hash01(band, 7) - 0.5
    per = 180.0 + 140.0 * hash01(band, 3 + 5)
    seg = np.floor((FZ + per * hash01(band, 3 + 9)) / per).astype(np.int64)
    k_seg = hash01(band * 131 + seg, 21) - 0.5
    grain_ = ground_noise(2.2, 70.0, 31, 3) - 0.5
    figure = ground_noise(9.0, 160.0, 37, 2) - 0.5
    f = 1 + 0.16 * k_board + 0.08 * k_seg + 0.20 * grain_ + 0.12 * figure
    # the walked middle: from the stairs' head to the room's middle and the west bay, a little paler and smoother
    walked = np.exp(-(((FX - 330.0) / 230.0) ** 2 + ((FZ - 330.0) / 190.0) ** 2))
    f = f * (1 + 0.05 * walked)
    m = BOARDS[..., None]
    pic[...] = pic * (1 - m) + np.clip(pic * f[..., None], 0, 1) * m
    # knots: few and large near us, many and small far off (true places through the camera)
    sh = Sheet(SHAPE)
    knot = lerp(SIENNA, PRUSSIAN, 0.55 if not lit else 0.4)
    for (x, y, k, r) in D.scatter(pt, kpx, (0, RW, 0, RD), 0.9, SEED + 3, size=(3.0, 2.0), zone=BOARDS):
        rx = max(0.6, 2.0 * k * (0.7 + 0.6 * r))
        ry = max(0.4, rx * 0.45)
        sh.ellipse(x, y, rx, ry, knot, 0.30)
        if k > 0.9:
            sh.ellipse(x - rx * 0.2, y, rx * 0.45, ry * 0.45, lerp(knot, PRUSSIAN, 0.4), 0.35)
    # nail heads in pairs at the board's ends (the butt joints lie where k_seg changes: put them by eye near the joints)
    for (x, y, k, r) in D.scatter(pt, kpx, (0, RW, 0, RD), 2.2, SEED + 4, size=(1.2, 1.2), zone=BOARDS):
        if r < 0.5:
            sh.ellipse(x, y, max(0.35, 0.5 * k), max(0.3, 0.3 * k), lerp(SIENNA, PRUSSIAN, 0.7), 0.22)
    c, a = sh.done()
    a = a * BOARDS
    pic[...] = pic * (1 - a[..., None]) + c * a[..., None]


def ground_shade(pic, places, amount, color=None, soft=2.0):
    D.shadow_on_ground(pic, pt, places, color=color if color is not None else lerp(SHADE, SIENNA, 0.25), amount=amount, soft=soft,
                       wobble=1.0, seed=int(abs(places[0][0]) + abs(places[0][1])), ground=FLOOR)


def box_shadow(pic, X0, X1, Z0, Z1, lean, amount, grow=6.0):
    """A thing's shade on the floor round its foot, leaning away from the west (the light)."""
    ground_shade(pic, [(X0 - grow * 0.4, Z0 - grow * 0.6), (X1 + lean, Z0 - grow * 0.6), (X1 + lean + grow, Z1 + grow * 0.5),
                       (X0 + lean * 0.3, Z1 + grow), (X0 - grow * 0.4, Z1 + grow * 0.4)], amount, soft=2.5)


def middle(pic, lit):
    """Shadows and air on the walked floor and round it."""
    floor_texture(pic, lit)
    # the near floor deeper (the shade of the bay we stand in), the far floor a little paler and cooler
    near = np.clip((Y_ - 362.0) / (600.0 - 362.0), 0, 1) ** 1.15
    deep = lerp(SIENNA, SHADE, 0.55)
    m = (BOARDS * near * (0.36 if lit else 0.34))[..., None]
    pic[...] = pic * (1 - m) + pic * deep * 1.4 * m
    farf = np.clip((430.0 - Y_) / 68.0, 0, 1) * BOARDS
    cool = lerp(PAPER, COBALT, 0.35) if lit else lerp(SHADE, PAPER, 0.35)
    D.air(pic, farf, cool, amount=0.12 if lit else 0.13)
    # soft shade at the feet of the walls (the floor's edges against them)
    edge = np.minimum(np.minimum(FX, RW - FX), FZ)
    ao = np.exp(-np.maximum(edge, 0) / 16.0) * FLOOR * (0.34 if lit else 0.26)
    pic[...] = pic * (1 - ao[..., None]) + pic * lerp(SHADE, SIENNA, 0.3)[None, None, :] * 1.3 * ao[..., None]
    # the things' shade, thrown away from the west
    for (X0, X1, Z0, Z1, h) in CHESTS:
        box_shadow(pic, X0, X1, Z0, Z1, h * (0.9 if lit else 0.35), 0.40 if lit else 0.34)
    LX, LZ = LANTERN
    box_shadow(pic, LX - 14, LX + 14, LZ - 14, LZ + 14, 40.0 if lit else 14.0, 0.36 if lit else 0.30, grow=4.0)
    X0, X1, Z0, Z1, h = FRONT_CHEST
    box_shadow(pic, X0, X1, Z0, Z1, h * 0.6, 0.38, grow=8.0)
    for (x, z) in ((SX1, SZ0), (SX1, SZ1), (SX0, SZ0)):
        box_shadow(pic, x - 5, x + 5, z - 5, z + 5, 18.0 if lit else 8.0, 0.30, grow=3.0)
    # under the rail's east side (it stands over the stairwell's lip)
    ground_shade(pic, [(SX1 + 2, SZ0 - 4), (SX1 + 22, SZ0), (SX1 + 22, SZ1 + 6), (SX1 + 2, SZ1 + 4)], 0.22, soft=3.0)
    if lit:
        sun_patch(pic)
    else:
        cracks(pic)
    return pic


def sun_patch(pic):
    """The low sun through the west bay on the floor (lit.png paints it as one flat of the sun's paper): the boards' joints
    through it, its far end softer, a warm glow round it, and the shadow of the stairwell's rail along its south edge."""
    wall, u0, u1, y0, y1 = BAYS["west"]
    x_near = y0 / T
    inpatch = ((FX >= x_near - 1) & (FX <= RW) & (FZ >= u0) & (FZ <= u1)).astype(F32) * FLOOR
    # the joints between the boards (along Z, every 30 cm from X 10) and the boards' tones, faint in the glare
    u = (FX - 10.0) / 30.0
    px_per_cm = V.F / np.maximum(DEPTH, 1.0)
    dist = np.abs(u - np.round(u)) * 30.0 * px_per_cm * (V.eye / np.maximum(DEPTH, 1)) * (DEPTH / V.eye)
    joint = np.clip(1.0 - np.abs((FX - 10.0) - 30.0 * np.round((FX - 10.0) / 30.0)) * px_per_cm / 0.7, 0, 1)
    band = np.floor((FX - 10.0) / 30.0).astype(np.int64)
    tone = 1 + 0.05 * (hash01(band, 7) - 0.5) + 0.07 * (ground_noise(2.2, 70.0, 31, 3) - 0.5)
    sunwood = lerp(BEAM_C, OCHRE, 0.12)
    m = inpatch[..., None]
    pic[...] = pic * (1 - m) + np.clip(pic * tone[..., None], 0, 1) * m
    jm = (joint * inpatch * 0.38)[..., None]
    pic[...] = pic * (1 - jm) + lerp(sunwood, SIENNA, 0.55)[None, None, :] * jm
    # the far end (toward the east wall) a little softer: the sun's disc widens the edges with distance from the window
    soft = blur(inpatch, 2.2)
    far = np.clip((FX - 500.0) / 260.0, 0, 1) * FLOOR
    edge = np.abs(soft - inpatch) * far
    pic[...] = pic * (1 - edge[..., None] * 0.5) + lerp(sunwood, SIENNA, 0.35)[None, None, :] * edge[..., None] * 0.5
    # warm glow round it on the floor (light bounced off the patch)
    glow = np.clip(blur(inpatch, 26.0) * 1.6, 0, 1) * (1 - inpatch) * FLOOR * 0.20
    pic[...] = pic * (1 - glow[..., None]) + lerp(NAPLES, P("chrome-orange"), 0.25)[None, None, :] * glow[..., None]
    # the rail's shadow: its north rail (X 40-160, Y 84-92) and the post at its north-east corner, thrown east along Z 376-384
    sh = [(x_near, 375.0), (SX1 + 92.0 / T, 375.0), (SX1 + 92.0 / T + 4, 385.0), (x_near, 385.0)]
    D.shadow_on_ground(pic, pt, sh, color=lerp(SIENNA, SHADE, 0.45), amount=0.55, soft=1.0, wobble=0.6, seed=5, ground=inpatch)


def cracks(pic):
    """The dark room: the last of the sun through the cracks round the west shutters and down their meeting stiles, lying
    across the floor in thin warm lines where the patch will be (and climbing the east wall's foot)."""
    wall, u0, u1, y0, y1 = BAYS["west"]
    x_near = y0 / T
    y_wall = y1 - T * RW
    sh = Sheet(SHAPE)
    warm = lerp(lerp(NAPLES, P("chrome-orange"), 0.35), SIENNA, 0.25)
    for z, a, w in ((300.0, 0.60, 1.2), (u1 - 3, 0.26, 0.8)):
        pts = []
        for X in np.linspace(x_near, RW, 24):
            pts.append(pt(X, z))
        sh.line(pts, warm, w, a)
        sh.line([V.pt(RW, 0, z), V.pt(RW, y_wall * 0.85, z)], warm, w * 0.8, a * 0.7)
    # the sill's crack: a line along Z where the lowest rays meet the floor
    c, a = sh.done()
    # broken: the cracks are not even
    brk = step(0.36, 0.62, noise(SHAPE, 18, 77, 3))
    a = a * (0.45 + 0.55 * brk)
    glow = np.clip(blur(a, 3.0) * 2.0, 0, 1) * 0.16
    pic[...] = pic * (1 - glow[..., None]) + pic * lerp(NAPLES, SIENNA, 0.4)[None, None, :] * 1.6 * glow[..., None]
    pic[...] = np.clip(pic * (1 - a[..., None]) + c * a[..., None], 0, 1)


def far(pic, lit):
    """The north wall and the far corners a little cooler and paler; the roof deeper toward the frame's top."""
    x0, x1 = 200.0, 600.0
    north = ((X_ > x0) & (X_ < x1) & (Y_ < 362.5)).astype(F32)
    bay = bay_mask("north")[0]
    north = north * (1 - np.clip(blur(bay, 1.0) * 1.5, 0, 1))
    roof_line = 204.0 - (np.abs(X_ - 400.0) - 200.0).clip(0) * 0                     # (the wall's top, y 204 between the corners)
    wall = north * (Y_ > 204).astype(F32)
    cool = lerp(PAPER, COBALT, 0.25) if lit else lerp(SHADE, PAPER, 0.45)
    D.air(pic, wall, cool, amount=0.10 if lit else 0.09)
    # the far corners (where the north wall meets the side walls): a cool glaze, soft
    cor = np.zeros(SHAPE, F32)
    for cx in (200.0, 600.0):
        cor = np.maximum(cor, np.exp(-(((X_ - cx) / 55.0) ** 2 + ((Y_ - 330.0) / 70.0) ** 2)))
    cor = cor * (Y_ > 204).astype(F32) * (1 - bay)
    m = (cor * (0.22 if lit else 0.20))[..., None]
    pic[...] = pic * (1 - m) + pic * lerp(SHADE, COBALT, 0.4)[None, None, :] * 1.5 * m
    # the roof: deeper toward the top of the frame (the near shade under the beam)
    top = np.clip((150.0 - Y_) / 150.0, 0, 1) ** 1.3 * (Y_ < 204).astype(F32)
    m = (top * (0.30 if lit else 0.26))[..., None]
    pic[...] = pic * (1 - m) + pic * lerp(SIENNA, SHADE, 0.6)[None, None, :] * 1.2 * m
    return pic


# ---------------------------------------------------------------- the near plane
BEAM_Z = (585.0, 610.0)           # the tie beam: along X at Z 580-610 (the posts' line), its underside 274 cm up
BEAM_U = 274.0
POST_R = (545.0, 575.0)           # the inner post on the right: X 545-575, Z 580-610 (in front of the chest)
POST_L = (150.0, 180.0)           # the inner post on the left: out of the frame
ARM = (22.0, 50.0)                # the bracket arms under the beam: 22 cm deep, 50 cm long


def near_plane():
    """-> (colour, alpha) of near.png: the beam, the post, the bracket arms."""
    sh = Sheet(SHAPE)
    zf, zb = BEAM_Z[1], BEAM_Z[0]
    deep = "#1c1014"                                                 # a warm near-black: the richest dark of the picture
    face = D.near_tone(WOOD_DARK, shade=deep, k=0.80, warm=0.05)    # the beam's face toward us: the deepest
    soffit = D.near_tone(WOOD_DARK, shade=deep, k=0.70, warm=0.07)  # its underside: a little light off the floor
    postc = D.near_tone(WOOD_DARK, shade=deep, k=0.72, warm=0.07)
    armc = D.near_tone(WOOD_DARK, shade=deep, k=0.75, warm=0.06)
    # the beam: a log hewn on its faces, its belly not ruled (it sags and swells a little along its length)
    xs = np.linspace(-20, 820, 43)
    rng = np.random.default_rng(SEED)
    belly = 2.2 * np.sin(xs / 95.0 + 0.6) + 1.4 * np.sin(xs / 37.0 + 2.0) + rng.normal(0, 0.5, len(xs))
    y_far = [V.pt(380, BEAM_U, zb)[1] + 3.0 * math.sin(math.pi * (x + 20) / 840.0) + b for x, b in zip(xs, belly)]
    y_near = [V.pt(380, BEAM_U, zf)[1] + 0.6 * b for b in belly]
    sh.poly([(x, -5) for x in xs] + [(x, y) for x, y in zip(xs[::-1], y_near[::-1])], face)
    sh.poly([(x, y) for x, y in zip(xs, y_near)] + [(x, y) for x, y in zip(xs[::-1], y_far[::-1])], soffit)
    # the bracket arms (sashi-hijiki) under the beam at the posts, each with its end cut in a curve underneath
    for side in ("R", "L"):
        a0, a1 = ARM
        if side == "R":
            xe, xp, dr = POST_R[0] - a1, POST_R[0], 1.0
        else:
            xe, xp, dr = POST_L[1] + a1, POST_L[1], -1.0
        yb = BEAM_U - a0
        zfa, zba = zf - 5.0, zb + 5.0
        P_ = lambda X, Y, Z: V.pt(X, Y, Z)
        cut = a1 * 0.3                                              # the end's lower corner cut away in a curve
        arc = lambda z: [P_(xe + dr * cut * (1 - math.cos(t)), yb + 9 * (1 - math.sin(t)), z) for t in np.linspace(0, math.pi / 2, 7)]
        # the front face, the underside, the end face (each a quad, the curve on the end's lower corner)
        sh.poly([P_(xp, BEAM_U, zfa), P_(xe, BEAM_U, zfa), P_(xe, yb + 9, zfa)] + arc(zfa)[1:] + [P_(xp, yb, zfa)], armc)
        sh.poly([P_(xe + dr * cut, yb, zfa), P_(xp, yb, zfa), P_(xp, yb, zba), P_(xe + dr * cut, yb, zba)], lerp(armc, soffit, 0.6))
        endc = lerp(armc, soffit, 0.5) if side == "R" else lerp(armc, face, 0.4)
        sh.poly([P_(xe, BEAM_U, zfa), P_(xe, BEAM_U, zba), P_(xe, yb + 9, zba), P_(xe, yb + 9, zfa)], endc)
        fa, ba = arc(zfa), arc(zba)
        for i in range(len(fa) - 1):
            sh.poly([fa[i], fa[i + 1], ba[i + 1], ba[i]], endc)
    # the post on the right: its west face (the one we see), from under the beam to below the frame
    X = POST_R[0]
    sh.poly([V.pt(X, BEAM_U, 580.0), V.pt(X, BEAM_U, 610.0), V.pt(X, -20, 610.0), V.pt(X, -20, 580.0)], postc)
    col, alpha = sh.done()
    # inside: the adze's shallow scallops along the hewn faces, the grain, one check (crack) down the post; quiet
    sc = noise(SHAPE, 9, SEED + 11, 2)
    streak = noise((H, W), 26, SEED + 12, 3)
    post_m = ((X_ >= 760) & (Y_ > 40)).astype(F32)
    beam_m = (Y_ < 100).astype(F32) * (1 - post_m)
    adze = (np.sin(X_ / 7.5 + 2.4 * sc) * 0.5 + 0.5) * beam_m + (np.sin(Y_ / 9.0 + 2.0 * sc) * 0.5 + 0.5) * post_m
    f = 1 + 0.07 * (adze - 0.5) + 0.06 * (streak - 0.5)
    col = np.clip(col * f[..., None], 0, 1)
    # the soffit's roundness: lighter along its middle (the floor's light), darker at the arrises
    ys = np.interp(X_, xs, y_near)
    yf = np.interp(X_, xs, y_far)
    t = np.clip((Y_ - ys) / np.maximum(yf - ys, 1), 0, 1)
    round_ = np.sin(t * math.pi) * (Y_ > ys) * (Y_ < yf) * (1 - post_m)
    col = lerp(col, lerp(soffit, lerp(WOOD_LIT, NAPLES, 0.2), 0.14), (round_ * 0.5)[..., None])
    chk = np.exp(-((X_ - 781.0 - 1.5 * np.sin(Y_ / 40.0)) / 0.7) ** 2) * post_m * step(0.4, 0.6, noise(SHAPE, 30, SEED + 13, 2))
    col = lerp(col, D.near_tone(WOOD_DARK, shade="#1c1014", k=0.9, warm=0.02), (chk * 0.7)[..., None])
    # the rim: the edges that face the west window (left) and the floor's light (below), warm, thin
    rim = D.rim(alpha, light=(-1.0, 0.35), width=2.0)
    rimc = lerp(lerp(WOOD_LIT, NAPLES, 0.35), P("chrome-orange"), 0.12)
    col = lerp(col, rimc, (np.clip(rim, 0, 1) * 0.55)[..., None])
    # the beam's far arris catches the floor's light along its length (broken)
    arris = np.exp(-((Y_ - (yf - 1.2)) / 0.9) ** 2) * (1 - post_m) * step(0.3, 0.55, noise(SHAPE, 22, SEED + 14, 2))
    col = lerp(col, rimc, (arris * alpha * 0.35)[..., None])
    return col.astype(F32), alpha.astype(F32)


# ---------------------------------------------------------------- the cut-outs
def deeper_front(colour, alpha, lit):
    """The old front plane (the chest near us at the right): deeper and warmer inside its own outline."""
    c = D.near_tone(colour.reshape(-1, 3).mean(axis=0) * 0 + 0.5, k=0.0)          # (placeholder: per pixel below)
    shade = rgb("#241c30")
    out = lerp(colour, shade[None, None, :], 0.30 if lit else 0.24)
    out[..., 0] = np.clip(out[..., 0] + 0.035, 0, 1)
    out[..., 2] = np.clip(out[..., 2] - 0.015, 0, 1)
    return out.astype(F32)


def wet_map():
    """1 the sky through the bays, less for the land and sea under it; 0 the room and everything in it."""
    wet = np.zeros(SHAPE, F32)
    for name, sky_row, land in (("west", 300.0, 0.45), ("north", 262.0, 0.55), ("east", 285.0, 0.5)):
        m, pp = bay_mask(name)
        ys = [p[1] for p in pp]
        top, bot = min(ys), max(ys)
        k = np.clip((sky_row - Y_) / 18.0 + 0.5, 0, 1)
        wet = np.maximum(wet, m * (land + (0.85 - land) * k))
    return wet


def to_pal(picture, palette, seed, speckle, mask=None):
    """brush.to_palette, only where the picture shows (a cut-out's outside is transparent: left at index 0)."""
    h, w, _ = picture.shape
    rng = np.random.default_rng(seed)
    noisy = picture + rng.normal(0, speckle, (h, w, 1)).astype(F32) + rng.normal(0, speckle * 0.35, (h, w, 3)).astype(F32)
    sel = np.ones((h, w), bool) if mask is None else (mask >= 0.5)
    flat = noisy[sel]
    index = np.zeros((h, w), dtype=np.uint8)
    out = np.empty(len(flat), dtype=np.uint8)
    for start in range(0, len(flat), 40000):
        part = flat[start:start + 40000]
        out[start:start + 40000] = ((part[:, None, :] - palette[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
    index[sel] = out
    return index


T0 = time.time()


def main():
    if not os.path.isdir(SRC):
        sys.exit(f"no {SRC}: run edo_keeptop.py and copy its out folder there first")
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back")
    lit, _ = load("lit")
    back_d = middle(back.copy(), False)
    back_d = far(back_d, False)
    lit_d = middle(lit.copy(), True)
    lit_d = far(lit_d, True)
    # the west bay's view and the east wall at the hum stay as painted (only the paper goes over them)
    keep = np.zeros(SHAPE, F32)
    keep = np.maximum(keep, bay_mask("west")[0])
    back_d = lerp(back_d, back, keep[..., None])
    lit_d = lerp(lit_d, lit, keep[..., None])
    WET = wet_map()
    AMT = {False: 0.6, True: 0.85}
    pics = {}
    pics["back"] = (WC.wash(back_d, seed=SEED, amount=AMT[False], soft=WET, wander=1.4, fleck=0.3), None)
    pics["lit"] = (WC.wash(lit_d, seed=SEED, amount=AMT[True], soft=WET, wander=1.4, fleck=0.3), None)
    print("backdrops washed", round(time.time() - T0, 1), "s", flush=True)
    # the cut-outs, washed on the same paper (wash_cut, crisp): those of one state never overlap, so each group is laid
    # over its unwashed backdrop together and washed once (the same as one wash_cut each, at a quarter of the cost)
    groups = [(False, ["rail", "chests", "lantern", "northshutter", "eastshutter", "westshutter", "front"]),
              (False, ["northshutter-open", "eastshutter-open", "westshutter-open"]),
              (True, ["rail-lit", "chests-lit", "lantern-lit", "northshutter-lit", "eastshutter-lit", "westshutter-open-lit", "front-lit"]),
              (True, ["northshutter-open-lit", "eastshutter-open-lit"])]
    nc, na = near_plane()
    cuts = {}
    for L, names in groups:
        whole = (lit_d if L else back_d).copy()
        hard = np.zeros(SHAPE, F32)
        for name in names:
            c, a = load(name)
            if name in ("front", "front-lit"):
                c = deeper_front(c, a, L)
            cuts[name] = a
            whole = whole * (1 - a[..., None]) + c * a[..., None]
            hard = np.maximum(hard, np.clip(blur((a > 0.3).astype(F32), 1.2) * 2, 0, 1))
        washed = WC.wash(whole, SEED, AMT[L], WET * (1 - hard), None, 0.07, 1.4, 0.3)
        for name in names:
            pics[name] = (washed, (cuts[name] >= 0.5).astype(F32))
        print("washed", names, round(time.time() - T0, 1), "s", flush=True)
    pics["near"] = (WC.wash_cut(nc, na, back_d, seed=SEED, amount=0.6, soft=WET, wander=1.4, fleck=0.3, crisp=True), (na >= 0.5).astype(F32))
    print("near washed", round(time.time() - T0, 1), "s", flush=True)
    # back to palettes, as edo_keep_kit.finish_scene does it (grain, one palette of 160 for all, speckle)
    seed, colors, speckle, amount = 9, 160, 0.012, 0.02
    grained = {n: grain(p, seed + i, amount) for i, (n, (p, a)) in enumerate(pics.items())}
    sample = [grained[n] if a is None else grained[n][a >= 0.5] for n, (p, a) in pics.items()]
    sample = [s.reshape(-1, 1, 3) for s in sample if len(s)]
    pal = palette_of(sample, colors=colors, seed=seed)
    print("palette", round(time.time() - T0, 1), "s", flush=True)
    for n, (p, a) in pics.items():
        idx = to_pal(grained[n], pal, seed + 1, speckle, a)
        save(os.path.join(OUT, n + ".png"), idx, pal, alpha=None if a is None else a)
    for f in os.listdir(SRC):
        if f.startswith("heron-fly-") or f == "layout.json":
            shutil.copy2(os.path.join(SRC, f), os.path.join(OUT, f))
    # a look: the two lights composed with every first-state cut-out and the near plane
    comp = {}
    for state, base, names in (("shut", "back", ["northshutter", "eastshutter", "westshutter", "rail", "chests", "lantern", "front"]),
                               ("lit", "lit", ["northshutter-lit", "eastshutter-lit", "westshutter-open-lit", "rail-lit", "chests-lit", "lantern-lit", "front-lit"])):
        im = Image.open(os.path.join(OUT, base + ".png")).convert("RGBA")
        for n in names + ["near"]:
            im.alpha_composite(Image.open(os.path.join(OUT, n + ".png")).convert("RGBA"))
        comp[state] = im
    sheet = Image.new("RGB", (W * 2 + 8, H), (20, 20, 20))
    sheet.paste(comp["shut"].convert("RGB"), (0, 0))
    sheet.paste(comp["lit"].convert("RGB"), (W + 8, 0))
    sheet.save("out/edo-keeptop-comp.png")
    print("written", len(pics), "pictures to", OUT, "+ herons, layout.json; out/edo-keeptop-comp.png")


if __name__ == "__main__":
    main()

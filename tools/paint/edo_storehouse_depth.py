"""Round twenty-three (the fast depth pass: tools/paint/DEPTH.md): inside the charcoal-burner's storehouse (edo-storehouse),
worked over the painting as edo_storehouse.py makes it, through its own camera (persp.Camera 285/480, focal 400) and its
own light (the grey rain-light of the small high window in the back wall, a little round the door's cracks; dusk).

    near     the front truss of the roof, 1.7 m from the lens: a rough log tie beam across the top, bowed a little, its
             underside catching the window's grey light; its two sasu poles rising out of the top corners, lashed, with
             the thatch's underside and its battens beyond them; the wall post at the left edge rising into the beam
             (its edge toward the room lit). The right wall's posts are spaced round the door: none at the edge.
    back     the floor's boards each a little different, with their grain, knots, charcoal crumbs, straw and the earth
             tracked in from the door (depth.scatter: few and large near, many and small far); the sacks', the
             baskets' and the left sacks' shadows thrown forward away from the window; the window's light and the
             door's falling away across the floor; the near floor deeper (the room's front in its own shade, its edge
             running in from the left); the far wall a little cooler and paler (depth.air by true depth); the far
             corners and the floor's edges dark.
    JAPAN    watercolor.wash (amount 0.7: dusk in rain, a dim room), every cut-out and near.png with wash_cut (crisp),
             seed 1830, wander 1.4, fleck 0.3; the window's rain-light the only wet passage.

Reads out/edo-storehouse-orig/ (the unkeyed painting: never changed), writes out/edo-storehouse/ (every file as before,
plus near.png), each picture to its palette as edo_storehouse.finish does it.

    python3 edo_storehouse_depth.py
"""

import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import *
import depth as D
import watercolor as WC
import edo_storehouse as S

SEED = 1830
AMOUNT = 0.7
ORIG = "out/edo-storehouse-orig"
OUT = "out/edo-storehouse"
SHAPE = S.SHAPE
CAM = S.CAM
F, VX, VY, EYE, Z0 = CAM.F, CAM.vx, CAM.vy, CAM.eye, CAM.Z0
P = CAM.pt
INF = 1e9

CUTS = ["lantern", "lantern-lit", "sacks", "sacks-heaped", "door", "door-open", "bar", "bar-up", "mat", "mat-aside",
        "trapdoor", "trapdoor-open", "floorgaps-on"]

# the scene's paints
PRUSSIAN, COBALT, SIENNA, OCHRE, WHITE, NAPLES = S.PRUSSIAN, S.COBALT, S.SIENNA, S.OCHRE, S.WHITE, S.NAPLES
LIGHT = lerp(S.PAPER, S.WALL_B, 0.25)                         # the window's grey rain-light, as it lands in here
AIR = lerp(S.PAPER, S.WALL_B, 0.40)                           # the room's air toward the far wall: cooler, paler
GLAZE = lerp(lerp(COBALT, PRUSSIAN, 0.55), SIENNA, 0.18)      # a cast shadow: a cool glaze (multiplied)
DEEP = lerp(PRUSSIAN, SIENNA, 0.30)                           # the corners
WOOD_NEAR = D.near_tone(lerp(SIENNA, S.RAFTER, 0.35), shade="#1c100c", k=0.80, warm=0.07)      # the near timber: deep and warm
WOOD_NEAR2 = D.near_tone(lerp(SIENNA, OCHRE, 0.30), shade="#1c100c", k=0.78, warm=0.07)
THATCH_NEAR = D.near_tone(lerp(S.STRAW, SIENNA, 0.45), shade="#1a1014", k=0.82, warm=0.06)
RIM = lerp(LIGHT, NAPLES, 0.10)
ROPE_NEAR = D.near_tone(lerp(S.STRAW, OCHRE, 0.3), shade="#2a1c18", k=0.66, warm=0.05)


def load(name):
    im = Image.open(f"{ORIG}/{name}.png").convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


# ================================================================ where every pixel is in the room
def room():
    """-> Z (cm from the `full` row) of what every pixel shows, and masks of the floor, the walls, the back wall, the
    roof space (the shell of edo_storehouse.py: walls at X = +-210 to 254 cm, the roof up to its ridge at 390)."""
    x, y = grid(SHAPE)
    dx, dy = x - VX, y - VY
    Df = np.where(dy > 0.5, F * EYE / np.maximum(dy, 0.5), INF)
    Df = np.where(np.abs(dx * Df / F) <= 210, Df, INF)
    Dl = np.where(dx < -0.5, 210 * F / np.maximum(-dx, 0.5), INF)
    Dr = np.where(dx > 0.5, 210 * F / np.maximum(dx, 0.5), INF)
    Yl, Yr = EYE - dy * Dl / F, EYE - dy * Dr / F
    Dl = np.where((Yl >= 0) & (Yl <= S.WALL_H + 14), Dl, INF)
    Dr = np.where((Yr >= 0) & (Yr <= S.WALL_H + 14), Dr, INF)
    den = (390 - 254) / 210.0 * np.abs(dx) - dy
    Dt = np.where(den > 0.05, F * (390 - EYE) / np.maximum(den, 0.05), INF)
    Dt = np.where((EYE - dy * Dt / F) >= 254, Dt, INF)
    Db = np.full(SHAPE, Z0 + S.Z_BACK, F32)
    stack = np.stack([Df, Dl, Dr, Dt, Db])
    which = stack.argmin(axis=0)
    Dv = stack.min(axis=0)
    Z = (Dv - Z0).astype(F32)
    X = (dx * Dv / F).astype(F32)
    Y = (EYE - dy * Dv / F).astype(F32)
    m = {k: (which == i).astype(F32) for i, k in enumerate(["floor", "left", "right", "roof", "back"])}
    return X, Y, Z, m


def gpt(X, Z):
    return P(X, 0, Z)


def kz(X, Z):
    return CAM.scale(Z)


def soft(m, s):
    return np.clip(blur(m.astype(F32), s), 0, 1)


# ================================================================ the back, deepened
def deepen(back, seed=SEED):
    pic = back.copy()
    rng = np.random.default_rng(seed)
    X, Y, Z, R = room()
    floor = soft(R["floor"], 0.6)
    walls = np.clip(R["left"] + R["right"], 0, 1)
    # ---- the boards: each a little lighter or darker than the next, with its grain running back (fading out where a
    # board is too small to show it), the floor's own edge of earth and dust
    board = np.floor((X + 216) / 24.0)
    h = np.sin(board * 12.9898 + 4.1) * 43758.5453
    tone = (h - np.floor(h)) - 0.5
    k = F / np.maximum(Z + Z0, 1.0)
    show_ = np.clip((24 * k - 6) / 10, 0, 1)
    tile = noise((512, 512), 32, seed + 1, 3)

    def fold(t):
        mm = np.mod(t, 2 * 510)
        return np.where(mm > 510, 2 * 510 - mm, mm)
    grain_ = sample(tile, fold(X * 2.6 + 260), fold(Z * 0.22 + 300)) - 0.5
    fine = sample(noise((512, 512), 12, seed + 2, 2), fold(X * 1.6 + 100), fold(Z * 0.35 + 77)) - 0.5
    mult = 1 + (tone * 0.20 + grain_ * 0.30 * show_ + fine * 0.20 * show_)
    pic *= (1 + (mult - 1) * floor)[..., None]
    # the earth tracked in from the door (the path outside is mud in this rain): a wandering trodden band from the
    # threshold toward the middle of the room, broken
    tx = np.clip((210 - X) / 230.0, 0, 1)
    zc = 52 + (30 - 52) * tx + 14 * np.sin(X / 37.0)
    band = np.exp(-((Z - zc) / (26 + 18 * tx)) ** 2) * (1 - tx) ** 0.8 * step(-30, 10, X + 230)
    brk = step(0.42, 0.66, sample(noise((512, 512), 40, seed + 3, 3), fold(X * 1.3 + 50), fold(Z * 1.3 + 50)))
    earth = lerp(lerp(OCHRE, SIENNA, 0.55), PRUSSIAN, 0.38)
    over(pic, earth, (band * brk * 0.30 * floor).astype(F32))
    # ---- the light: the window's falling away across the floor and the back wall; the door's cracks on the floor
    dw = np.hypot((X - 82) / 1.0, (Z - 205) / 1.15)
    lw = np.exp(-dw / 150.0) * floor
    over(pic, LIGHT, (lw * 0.16).astype(F32))
    dwall = np.hypot(X - 82, (Y - 150) * 1.3)
    over(pic, LIGHT, (np.exp(-dwall / 95.0) * R["back"] * 0.12).astype(F32))
    dd = np.hypot(X - 210, (Z - 52) * 0.9)
    over(pic, LIGHT, (np.exp(-dd / 85.0) * floor * 0.11).astype(F32))
    dside = np.hypot(Z - 52, (Y - 90) * 0.7)
    over(pic, LIGHT, (np.exp(-dside / 70.0) * R["right"] * 0.07).astype(F32))
    # ---- shadows thrown forward, away from the window (a point of light high in the back wall, X 82, 195 up)
    sh = [
        ([(56, 192), (212, 192), (214, 150), (150, 128), (96, 126), (50, 146)], 0.30, 5.0),      # the sacks under the window
        ([(-150, 152), (-150, 205), (-210, 196), (-210, 110), (-176, 128)], 0.28, 4.0),       # the sacks along the left wall
        ([(150, 132), (200, 132), (210, 104), (166, 100), (148, 118)], 0.26, 3.0),            # the baskets
    ]
    for i, (pl, amt, sft) in enumerate(sh):
        D.shadow_on_ground(pic, gpt, pl, color=GLAZE, amount=amt, soft=sft, wobble=1.0, seed=seed + 10 + i, ground=floor)
    # ---- the near floor deeper: the room's front in its own shade, its edge running in from the left wall
    D.shadow_on_ground(pic, gpt, [(-420, -420), (420, -420), (420, -95), (180, -70), (0, -25), (-120, 30), (-420, 70)],
                       color=lerp(GLAZE, SIENNA, 0.15), amount=0.34, soft=26.0, wobble=2.0, seed=seed + 20, ground=floor)
    near_w = np.clip((-60 - Z) / 170.0, 0, 1) * walls
    tint(pic, lerp(GLAZE, SIENNA, 0.2) * 1.5, (near_w * 0.30).astype(F32))
    # ---- the far: the back wall and the far reaches cooler and paler, toward the window's air
    far = np.clip((Z + 170) / (S.Z_BACK + 170), 0, 1)
    D.air(pic, far, AIR, amount=0.15, power=1.4, mask=np.clip(1 - R["roof"] * 0.6, 0, 1))
    # ---- the far corners dark, and every edge where the floor meets a wall (deeper the farther)
    ao = np.zeros(SHAPE, F32)
    ao += R["floor"] * (np.exp(-(210 - np.abs(X)) / 26.0) + np.exp(-(S.Z_BACK - Z) / 34.0))
    ao += (R["left"] + R["right"]) * (np.exp(-np.maximum(Y, 0) / 30.0) + np.exp(-(S.Z_BACK - Z) / 40.0) + np.exp(-np.abs(S.WALL_H - Y) / 26.0) * 0.6)
    ao += R["back"] * (np.exp(-(210 - np.abs(X)) / 34.0) + np.exp(-np.maximum(Y, 0) / 30.0) + np.exp(-np.abs(S.WALL_H - Y) / 30.0))
    ao = np.clip(blur(ao, 1.2), 0, 1.4) * (0.35 + 0.65 * far)
    tint(pic, DEEP * 1.6, np.clip(ao * 0.30, 0, 0.42).astype(F32))
    # the roof space deeper toward us and at its far end (its ridge in the dark)
    tint(pic, DEEP * 1.6, (R["roof"] * (0.10 + 0.18 * np.clip((VY - grid(SHAPE)[1]) / 285.0, 0, 1))).astype(F32))
    # ---- what lies on the boards, through the camera: few and large near, many and small far
    zone = (R["floor"] > 0.5).astype(F32)
    L = Sheet(SHAPE)
    crumb = lerp(PRUSSIAN, SIENNA, 0.22)
    for (x_, y_, k_, r) in D.scatter(gpt, kz, (-208, 208, -175, 243), 6, seed + 30, size=(1.6, 1.6, 1.6), zone=zone,
                                      keep=lambda X_, Z_: (X_ > 30 and Z_ > 110) or (X_ < -140 and Z_ > 120) or np.random.default_rng(int(abs(X_ * 7 + Z_ * 13))).random() < 0.35):
        rx = max(0.45, (0.5 + 0.9 * r) * k_)
        L.ellipse(x_, y_, rx, max(0.35, rx * EYE * k_ / F * 1.6), crumb, 0.35 + 0.25 * r)
    for (x_, y_, k_, r) in D.scatter(gpt, kz, (-208, 208, -175, 243), 7, seed + 31, size=(9, 1, 9), zone=zone):
        ln = (5 + 7 * r) * k_
        a = r * 6.283
        fy = EYE * k_ / F
        L.line([(x_, y_), (x_ + ln * np.cos(a), y_ + ln * np.sin(a) * fy)], lerp(S.STRAW, S.FLOOR, 0.35), max(0.5, 0.5 * k_), 0.55)
    for (x_, y_, k_, r) in D.scatter(gpt, kz, (-208, 208, -175, 243), 2.2, seed + 32, size=(4, 1, 6), zone=zone):
        rx = (1.5 + 1.5 * r) * k_
        L.ellipse(x_, y_, rx, max(0.4, rx * EYE * k_ / F * 2.2), lerp(S.FLOOR, PRUSSIAN, 0.35), 0.30)        # knots
    for (x_, y_, k_, r) in D.scatter(gpt, kz, (60, 208, -60, 140), 7, seed + 33, size=(6, 6, 6), zone=zone):
        rx = (2 + 4 * r) * k_
        L.ellipse(x_, y_, rx, max(0.4, rx * EYE * k_ / F * 1.4), lerp(earth, S.FLOOR, 0.4), 0.30)            # mud by the door
    L.onto(pic)
    return np.clip(pic, 0, 1).astype(F32), R


# ================================================================ the near plane: the front truss and a wall post
ZT = -270.0          # the truss, cm from the `full` row (1.7 m from the lens)
YC, RB = 247.0, 12.5  # the tie beam's middle height at its ends, its radius


def camber(X):
    return 8.0 * (1 - (X / 260.0) ** 2) + 2.2 * np.sin(X / 43.0 + 0.6) + 0.8 * np.sin(X / 11.0)


def near_plane(seed=SEED):
    rng = np.random.default_rng(seed)
    S_ = Sheet(SHAPE)
    Xs = np.linspace(-320, 320, 161)
    # the thatch's underside nearer than the truss, in the top corners, and its battens running back to the room
    for side in (-1, 1):
        a = P(side * 215, 247, ZT)
        b = P(0, 400, ZT)
        t = np.array(b) - np.array(a)
        far_ = (np.array(a) - 2.0 * t, np.array(a) + 2.0 * t)
        corner = (-40 if side < 0 else 840, -40)
        poly = [tuple(far_[0]), tuple(far_[1]), corner]
        S_.poly(poly, THATCH_NEAR)
    # the sasu: two rough poles from the beam's ends to the ridge, over the thatch
    for side in (-1, 1):
        pts_hi, pts_lo = [], []
        for u in np.linspace(-0.25, 1.15, 40):
            Xc = side * (200 - 200 * u)
            Yc = 252 + 148 * u
            wob = 1.1 * np.sin(u * 9 + side) + 0.6 * np.sin(u * 23)
            r = 10.5 + 0.9 * np.sin(u * 5)
            nx, ny = -148.0 * side, 200.0
            nn = np.hypot(nx, ny)
            pts_hi.append(P(Xc + (r + wob * 0.3) * nx / nn * -1, Yc + (r + wob * 0.3) * ny / nn, ZT))
            pts_lo.append(P(Xc - (r - wob * 0.3) * nx / nn * -1, Yc - (r - wob * 0.3) * ny / nn, ZT))
        S_.poly(pts_hi + pts_lo[::-1], WOOD_NEAR2)
    # the tie beam: a log, its top seen from below its front, its underside toward the window
    top = [P(X, YC + RB + camber(X) + 0.9 * np.sin(X / 7.0 + 2), ZT - 5) for X in Xs]
    bot = [P(X, YC - RB + camber(X) + 0.7 * np.sin(X / 9.0 + 1), ZT + 7) for X in Xs[::-1]]
    S_.poly(top + bot, WOOD_NEAR)
    # the wall post at the left edge, its inner face, rising into the beam
    post = [P(-199, -60, -243), P(-199, -60, -219), P(-199, 262, -219), P(-199, 262, -243)]
    S_.poly(post, WOOD_NEAR)
    color, alpha = S_.done()
    alpha = (alpha > 0.5).astype(F32)
    # ---- inside: little detail, the outline first. Shading and grain on a second sheet laid through the alpha
    pic = color.copy()
    x, y = grid(SHAPE)
    # the beam rounder: its top a shade lighter (bounce from the thatch), its lower half deeper; adze facets
    Dt = Sheet(SHAPE)
    mid = [P(X, YC + camber(X) - 2, ZT - 2) for X in Xs]
    Dt.poly(mid + bot, lerp(WOOD_NEAR, PRUSSIAN, 0.22), 0.55)
    for i in range(26):
        X0 = rng.uniform(-300, 300)
        ln = rng.uniform(25, 70)
        yy = YC + rng.uniform(-6, 9)
        Dt.line([P(X0, yy + camber(X0), ZT - 4), P(X0 + ln, yy + camber(X0 + ln), ZT - 4)], lerp(WOOD_NEAR, NAPLES, 0.10), rng.uniform(0.8, 1.6), 0.35)
    for i in range(6):                                                    # checks (cracks) along the log
        X0 = rng.uniform(-300, 260)
        ln = rng.uniform(40, 110)
        yy = YC + rng.uniform(-3, 6)
        Dt.line([P(X0 + s_ * ln, yy + camber(X0 + s_ * ln) + 1.2 * np.sin(s_ * 5), ZT - 4) for s_ in np.linspace(0, 1, 8)], lerp(WOOD_NEAR, PRUSSIAN, 0.5), 0.9, 0.7)
    # the post: an adzed face, vertical facets
    for i in range(9):
        zz = rng.uniform(-241, -221)
        Dt.line([P(-199, -40, zz), P(-199, 255, zz + rng.uniform(-1, 1))], lerp(WOOD_NEAR, NAPLES if i % 2 else PRUSSIAN, 0.10), rng.uniform(0.8, 1.5), 0.45)
    # the sasu: their undersides deeper, bark left in strips
    for side in (-1, 1):
        for i in range(10):
            u0 = rng.uniform(-0.2, 1.0)
            u1 = u0 + rng.uniform(0.04, 0.12)
            off = rng.uniform(-6, 6)
            Dt.line([P(side * (200 - 200 * u0) + off * 0.6 * side, 252 + 148 * u0 + off * 0.8, ZT), P(side * (200 - 200 * u1) + off * 0.6 * side, 252 + 148 * u1 + off * 0.8, ZT)],
                    lerp(WOOD_NEAR2, PRUSSIAN, 0.35), rng.uniform(1.0, 2.2), 0.5)
    # the thatch's underside: straw down the slope, deep; battens running back toward the vanishing point
    for side in (-1, 1):
        for i in range(320):
            u = rng.uniform(-0.3, 1.2)
            d_ = rng.uniform(4, 60)
            a0 = np.array(P(side * (200 - 200 * u) + side * d_ * 0.6, 252 + 148 * u + d_ * 0.8, ZT - d_ * 1.4))
            dirv = np.array(P(side * (200 - 200 * (u + 0.08)), 252 + 148 * (u + 0.08), ZT)) - np.array(P(side * (200 - 200 * u), 252 + 148 * u, ZT))
            Dt.line([tuple(a0), tuple(a0 + dirv * rng.uniform(0.3, 0.9))], lerp(THATCH_NEAR, NAPLES if rng.random() < 0.5 else PRUSSIAN, 0.14), rng.uniform(0.7, 1.4), 0.45)
        for u in (0.15, 0.42, 0.70, 0.98):
            Xb, Yb = side * (200 - 200 * u), 252 + 148 * u
            Dt.line([P(Xb, Yb - 4, ZT - 2), P(Xb, Yb - 4, ZT - 140)], lerp(THATCH_NEAR, SIENNA, 0.25), 2.4, 0.9)
    # straw-rope lashings round the sasu where they are tied to the battens
    for side in (-1, 1):
        for u in (0.15, 0.42, 0.70):
            c = P(side * (200 - 200 * u), 252 + 148 * u, ZT)
            for j in range(3):
                Dt.line([(c[0] - 9 + j * 3.5, c[1] - 14 + j * 2.5 * side), (c[0] + 7 + j * 3.5, c[1] + 10 + j * 2.5 * side)], ROPE_NEAR, 1.8, 0.75)
    dc, da = Dt.done()
    over(pic, dc, da * alpha)
    # ---- the rim: the edges toward the window's light (below the beam, the sasu's lower edges, the post's room side)
    wx, wy = P(82, 195, S.Z_BACK)
    rims = np.zeros(SHAPE, F32)
    rims += D.rim(alpha, light=(0.0, 1.0), width=2.2) * step(150, 175, y) * (x > 60)
    rims += D.rim(alpha, light=(1.0, 0.45), width=2.0) * (x < 300) * (y < 200)
    rims += D.rim(alpha, light=(-1.0, 0.45), width=2.0) * (x > 500) * (y < 200)
    rims += D.rim(alpha, light=(1.0, 0.0), width=2.2) * (x < 60) * (y > 230)
    fall = np.clip(1.0 - np.hypot(x - wx, (y - wy) * 1.3) / 520.0, 0.25, 1.0)
    over(pic, RIM, np.clip(rims * fall * 0.75, 0, 0.8).astype(F32))
    return np.clip(pic, 0, 1).astype(F32), alpha


# ================================================================ the act's watercolour, and back to palettes
def wet_map():
    m = mask_poly(SHAPE, [P(S.WINDOW["x0"], S.WINDOW["y0"], S.Z_BACK), P(S.WINDOW["x1"], S.WINDOW["y0"], S.Z_BACK),
                          P(S.WINDOW["x1"], S.WINDOW["y1"], S.Z_BACK), P(S.WINDOW["x0"], S.WINDOW["y1"], S.Z_BACK)], soft=0.8)
    return (m * 0.8).astype(F32)


def main():
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back")
    deep, R = deepen(back)
    WET = wet_map()
    washed = WC.wash(deep, seed=SEED, amount=AMOUNT, soft=WET, wander=1.4, fleck=0.3)
    print("back", S.finish(washed, f"{OUT}/back.png", 160, seed=7, speckle=0.010, amount=0.008))
    nc, na = near_plane()
    out = {"near": (nc, na)}
    for name in CUTS:
        out[name] = load(name)
    for name, (c, a) in out.items():
        wc = WC.wash_cut(c, a, deep, seed=SEED, amount=AMOUNT, soft=WET, wander=1.4, fleck=0.3, crisp=True)
        n = 40 if name == "floorgaps-on" else 64
        print(name, S.finish(wc, f"{OUT}/{name}.png", n, a, seed=7, speckle=0.010, amount=0.008))
    shutil.copy(f"{ORIG}/layout.json", f"{OUT}/layout.json")
    # a comp to look at (nobody there; the first states)
    comp = np.asarray(Image.open(f"{OUT}/back.png").convert("RGB"), dtype=F32) / 255
    for name in ["lantern", "sacks", "door", "bar", "trapdoor", "mat", "near"]:
        im = np.asarray(Image.open(f"{OUT}/{name}.png").convert("RGBA"), dtype=F32) / 255
        over(comp, im[..., :3], im[..., 3])
    Image.fromarray((np.clip(comp, 0, 1) * 255).astype(np.uint8)).save("out/edo-storehouse-depth-comp.png")
    print("near share", round(float((na > 0.5).mean()) * 100, 1))


if __name__ == "__main__":
    main()

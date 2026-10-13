"""The Capitol as plain blocks through the game's camera, with stand-in people at the game's sizes: to look at the
composition before anything is painted (python3 rome_capitol_plan.py -> out/rome-capitol-plan.png)."""

import math
import os
import sys

import numpy as np
from PIL import Image

from brush import Sheet, lerp
from rome_capitol_kit import *

S = Sheet(SHAPE, ss=2)


def poly(pts, c, a=1.0):
    S.poly(pts, c, a)


def tpts(pts):
    return [T.pt(*p) for p in pts]


def box_world(X0, X1, Z0, Z1, h0, h1, front, side, top):
    """A box standing square to us: its front, the side toward the middle, its top if below the eye."""
    if X0 > 0:
        poly([P(X0, h0, Z0), P(X0, h0, Z1), P(X0, h1, Z1), P(X0, h1, Z0)], side)
    if X1 < 0:
        poly([P(X1, h0, Z0), P(X1, h0, Z1), P(X1, h1, Z1), P(X1, h1, Z0)], side)
    if h1 < EYE:
        poly([P(X0, h1, Z0), P(X1, h1, Z0), P(X1, h1, Z1), P(X0, h1, Z1)], top)
    poly([P(X0, h0, Z0), P(X1, h0, Z0), P(X1, h1, Z0), P(X0, h1, Z0)], front)


def figure(x, y, height_px, color="#c0392b", seated=False):
    """A stand-in person: feet at (x, y)."""
    h = height_px
    w = h * 0.26
    if seated:
        S.poly([(x - w / 2, y - h * 0.55), (x + w / 2, y - h * 0.55), (x + w / 2, y), (x - w / 2, y)], color)
        S.ellipse(x, y - h * 0.62, w * 0.42, h * 0.08, color)
        return
    S.poly([(x - w / 2, y - h * 0.86), (x + w / 2, y - h * 0.86), (x + w * 0.35, y), (x - w * 0.35, y)], color)
    S.ellipse(x, y - h * 0.92, w * 0.42, h * 0.08, color)


def goose(x, y, s, color="#ffffff"):
    S.ellipse(x - 4 * s, y - 14 * s, 20 * s, 10 * s, color)
    S.line([(x + 10 * s, y - 18 * s), (x + 16 * s, y - 44 * s)], color, 5 * s)
    S.ellipse(x + 17 * s, y - 46 * s, 5 * s, 4 * s, color)
    S.line([(x + 20 * s, y - 46 * s), (x + 27 * s, y - 45 * s)], "#e08030", 2.5 * s)


def main():
    # sky
    poly([(0, 0), (800, 0), (800, HZ), (0, HZ)], "#7fb0e0")
    # the paving everywhere below the horizon first
    poly([(0, HZ), (800, HZ), (800, 600), (0, 600)], "#e2d6bc")
    # the view over the wall at the left: the plain, the river, the far ridge
    wl = P(0, WALL["h"], WALL["Z"])[1]
    wall_end = KINGS[0]["x"] - 30
    poly([(0, HZ - 26), (60, HZ - 30), (140, HZ - 22), (240, HZ - 16), (300, HZ - 8), (300, wl), (0, wl)], "#b8c4a8")   # Janiculum
    poly([(0, HZ - 4), (300, HZ - 4), (300, wl), (0, wl)], "#d8d4c0")
    poly([(0, 350), (90, 340), (200, 352), (260, 368), (260, 382), (180, 372), (60, 370), (0, 378)], "#7fb0a8")        # the river
    poly([(60, 318), (90, 298), (150, 296), (190, 318)], "#e8dcc0")                                              # theater
    # the parapet across the left
    Zw, hw, t = WALL["Z"], WALL["h"], WALL["t"]
    Xe = X_at(wall_end, P(0, 0, Zw)[1])
    box_world(-3000, Xe, Zw, Zw + t, 0, hw, "#cfc0a0", "#b0a090", "#e8dcc0")
    # the temple
    poly(tpts([(0, -RUN, 0), (0, BACK, 0), (0, BACK, HP), (0, -RUN, HP)]), "#a0a0c0")                     # left flank of the podium
    poly(tpts([(0, -RUN, 0), (CHEEK, -RUN, 0), (CHEEK, -RUN, HP), (0, -RUN, HP)]), "#e8d8b0")             # cheek blocks
    poly(tpts([(UW - CHEEK, -RUN, 0), (UW, -RUN, 0), (UW, -RUN, HP), (UW - CHEEK, -RUN, HP)]), "#e8d8b0")
    for k in range(NSTEP, 0, -1):                                                                        # the steps
        vk = -RUN + (k - 1) * TREAD
        poly(tpts([(CHEEK, vk, (k - 1) * RISE), (UW - CHEEK, vk, (k - 1) * RISE), (UW - CHEEK, vk, k * RISE), (CHEEK, vk, k * RISE)]), "#f0e4c8" if k % 2 else "#e4d8bc")
    poly(tpts([(CHEEK, 0, HP), (UW - CHEEK, 0, HP), (UW - CHEEK, DEEP, HP), (CHEEK, DEEP, HP)]), "#d8ccb0")
    poly(tpts([(CELLA[0], DEEP, HP), (CELLA[1], DEEP, HP), (CELLA[1], DEEP, E0), (CELLA[0], DEEP, E0)]), "#3a3048")   # porch, deep in shade
    poly(tpts([(0, COLV, HP), (UW, COLV, HP), (UW, DEEP, HP), (0, DEEP, HP)]), "#4a4060", 0.6)
    for vrow in reversed(FLANK_V):                                                                        # the flank columns
        if vrow > ROWS_V[-1]:
            c0, c1 = T.pt(COLS[0] - COL_R, vrow, HP), T.pt(COLS[0] + COL_R, vrow, E0)
            poly([(c0[0], c0[1]), (c1[0], c0[1]), (c1[0], c1[1]), (c0[0], c1[1])], "#9a94b4")
    for vrow in reversed(ROWS_V):
        for cu in COLS:
            c0, c1 = T.pt(cu - COL_R, vrow, HP), T.pt(cu + COL_R, vrow, E0)
            poly([(c0[0], c0[1]), (c1[0], c0[1]), (c1[0], c1[1]), (c0[0], c1[1])], "#f2e6c8" if vrow == COLV else "#8a84a4")
    fv = COLV - COL_R - 10
    poly(tpts([(-EAVE, fv, E0), (UW + EAVE, fv, E0), (UW + EAVE, fv, E2), (-EAVE, fv, E2)]), "#e8c890")       # beam and frieze
    poly(tpts([(-EAVE, fv, E0), (-EAVE, BACK, E0), (-EAVE, BACK, E2), (-EAVE, fv, E2)]), "#a89878")
    poly(tpts([(-EAVE * 2, fv - EAVE, E2), (UW + EAVE * 2, fv - EAVE, E2), (UW + EAVE * 2, fv - EAVE, E3), (-EAVE * 2, fv - EAVE, E3)]), "#f0d070")
    poly(tpts([(-EAVE * 2, fv - EAVE, E2), (-EAVE * 2, BACK, E2), (-EAVE * 2, BACK, E3), (-EAVE * 2, fv - EAVE, E3)]), "#c8a050")
    poly(tpts([(0, fv, E3), (UW / 2, fv, APEX), (UW, fv, E3)]), "#e0d4b8")                                # the pediment
    poly(tpts([(-EAVE * 2, fv - EAVE, E3), (UW / 2, fv - EAVE, APEX + 40), (UW + EAVE * 2, fv - EAVE, E3), (UW + EAVE * 2, fv - EAVE, E3 + 34), (UW / 2, fv - EAVE, APEX + 74), (-EAVE * 2, fv - EAVE, E3 + 34)]), "#f4c040")
    q0, q1 = T.pt(UW / 2 - 200, fv, APEX + 40), T.pt(UW / 2 + 200, fv, APEX + 40 + QUAD_H)
    poly([(q0[0], q0[1]), (q1[0], q0[1]), (q1[0], q1[1]), (q0[0], q1[1])], "#7a6030")
    for i in range(18):
        a = T.pt(300 + i * 145, fv, E1 + 20)
        b = T.pt(300 + i * 145 + 90, fv, E1 + 90)
        if i != 1 and i != 10:
            poly([(a[0], a[1]), (b[0], a[1]), (b[0], b[1]), (a[0], b[1])], "#6a4a20")
    # things in the precinct, far to near
    things = []
    a = ALTAR
    things.append((a["Z"][0], lambda: (box_world(a["X"][0] - 30, a["X"][1] + 30, a["Z"][0] - 30, a["Z"][1] + 30, 0, 20, "#d8ccb4", "#b8ac98", "#ece2cc"),
                                       box_world(a["X"][0], a["X"][1], a["Z"][0], a["Z"][1], 20, a["h"], "#d0c4ac", "#a89c8c", "#e8dcc4"))))
    c = CHARIOT
    bw, bd, bh = c["base"]

    def chariot():
        box_world(c["X"] - bw / 2, c["X"] + bw / 2, c["Z"], c["Z"] + bd, 0, bh, "#d8ccb4", "#b0a490", "#ece2cc")
        box_world(c["X"] - 150, c["X"] + 150, c["Z"] + 60, c["Z"] + 420, bh, bh + 210, "#6a5a40", "#5a4a30", "#7a6a50")
    things.append((c["Z"], chariot))
    w = WORLD

    def world_statue():
        bw_, bd_, bh_ = w["base"]
        box_world(w["X"] - bw_ / 2, w["X"] + bw_ / 2, w["Z"], w["Z"] + bd_, 0, bh_, "#e0d4bc", "#b8ac98", "#ece2cc")
        g = P(w["X"], bh_ + w["r"], w["Z"] + bd_ / 2)
        kk = k_at(w["Z"] + bd_ / 2)
        S.ellipse(g[0], g[1], w["r"] * kk, w["r"] * kk, "#8a7040")
        f0 = P(w["X"], bh_ + 2 * w["r"], w["Z"] + bd_ / 2)
        figure(f0[0], f0[1], w["man"] * kk, "#5a4a30")
    things.append((w["Z"], world_statue))
    for kg in KINGS:
        X0, X1, Z0, Z1, h = base_box(kg)

        def king(X0=X0, X1=X1, Z0=Z0, Z1=Z1, h=h, kg=kg):
            box_world(X0, X1, Z0, Z1, 0, h, "#d8ccb4" if kg["kind"] != "seat" else "#e4d4b4", "#b0a490", "#ece2cc")
            Xm = (X0 + X1) / 2
            Zs = Z1 - 40 if kg["kind"] == "seat" else (Z0 + Z1) / 2
            f = P(Xm, h, Zs)
            figure(f[0], f[1], kg["statue"] * k_at(Zs), "#c8a050" if kg["kind"] == "new" else "#4a6050")
        things.append((Z0, king))
    hut = HUT

    def hut_():
        X, Z, r = hut["X"], hut["Z"], hut["r"]
        a0, a1 = P(X - r, 0, Z), P(X + r, hut["wall"], Z)
        poly([(a0[0], a0[1]), (a1[0], a0[1]), (a1[0], a1[1]), (a0[0], a1[1])], "#8a7050")
        t0 = P(X, hut["top"], Z)
        poly([(a0[0] - 6, a1[1] + 3), (a1[0] + 6, a1[1] + 3), (t0[0], t0[1])], "#b09050")
    things.append((HUT["Z"] - HUT["r"], hut_))
    p = PEN

    def pen():
        X0, X1 = p["X"]
        Z0, Z1 = p["Z"]
        poly([P(X0, 0, Z0), P(X1, 0, Z0), P(X1, 0, Z1), P(X0, 0, Z1)], "#c8b890")
        gx, g0, g1 = p["gate"]
        for (A, B) in (((X0, Z1), (X1, Z1)), ((X0, Z0), (X0, Z1)), ((X1, g1), (X1, Z1)), ((X1, Z0), (X1, g0)), ((X0, Z0), (X1, Z0))):
            poly([P(A[0], 0, A[1]), P(B[0], 0, B[1]), P(B[0], p["h"], B[1]), P(A[0], p["h"], A[1])], "#8a6a40", 0.85)
    things.append((PEN["Z"][0], pen))
    def tablets():
        import rome_capitol_things as TH
        w, d, h = TH.POST
        for Xc, Zc in reversed(TH.tablet_posts()):
            box_world(Xc - w / 2, Xc + w / 2, Zc, Zc + d, 0, h, "#d0c4ac", "#a89c8c", "#e8dcc4")
            box_world(Xc - 35, Xc + 35, Zc - 6, Zc + d + 6, h, h + 26, "#8a7040", "#6a5a30", "#b09050")
    things.append((TABLETS["Z"][0], tablets))
    for z, f in sorted(things, key=lambda t: -t[0]):
        f()
    # stand-ins: the boy, Titus on the base, the goose-keeper, geese
    X0, X1, Z0, Z1, h = base_box(seat_base())
    foot = P((X0 + X1) / 2, 0, Z0)
    seat_top = P((X0 + X1) / 2, h, Z0)
    figure(foot[0], seat_top[1] + 2, 0.78 * 160 * scale_at(foot[1]), "#e06030", seated=True)
    for (gx, gy) in ((318, 466), (345, 476), (372, 462), (400, 472), (296, 480), (368, 488)):
        goose(gx, gy, scale_at(gy) * 0.95)
    for (x, y, who) in ((560, 570, "son"), (430, 505, "son"), (150, 440, "son"), (272, 500, "anser"), (700, 372, "diod")):
        hh = (0.74 if who == "son" else 1.0) * 160 * scale_at(y)
        figure(x, y, hh, {"son": "#3050c0", "anser": "#80a040", "diod": "#c0b080"}[who])
    c, a = S.done()
    pic = np.zeros(SHAPE + (3,), np.float32) + 1
    pic = pic * (1 - a[..., None]) + c
    im = Image.fromarray((np.clip(pic, 0, 1) * 255).astype(np.uint8))
    from PIL import ImageDraw
    d = ImageDraw.Draw(im)
    d.line([(0, HZ), (800, HZ)], fill=(255, 0, 0))
    d.line([(0, FULL), (800, FULL)], fill=(255, 0, 0))
    os.makedirs("out", exist_ok=True)
    im.save("out/rome-capitol-plan.png")
    print("temple: front-left foot", [round(v) for v in T.pt(0, -RUN, 0)], "porch", [round(v) for v in T.pt(0, 0, HP)],
          "apex", [round(v) for v in T.pt(UW / 2, COLV - COL_R - 10, APEX)], "chariot top", round(T.pt(UW / 2, COLV, APEX + 40 + QUAD_H)[1]),
          "right foot", [round(v) for v in T.pt(UW, -RUN, 0)])
    print("seat base: foot", [round(v) for v in foot], "top", round(seat_top[1]), "px tall", round(foot[1] - seat_top[1]))


if __name__ == "__main__":
    main()

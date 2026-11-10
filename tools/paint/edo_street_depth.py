"""Osaka, Shinsaibashi-suji at a crossroads, about 21 April 1830, late afternoon (edo-street): the fast depth pass of round
twenty-three (DEPTH.md; the lead's LITE.md). It works over PAINT-21C's painting as it is (edo_street.py, run once into
out/edo-street-orig/, never changed) and writes the scene's set back into out/edo-street/: every old file plus near.png.

    near     WHERE WE STAND: the lens is 3.59 m up, under the deep eave of a shop on our own side of the street. Across the
             top left: that eave seen from below, the rafters running out over the beam they lie on, the edge with the
             lips of its tiles, its corner swept up at about x 190 where the house ends (beyond it the sky is open over
             the cross street's fire tower); under the edge a short shop curtain (mizuhiki noren: three panels of indigo
             cotton and our own white mark, a ring round a little hill: no real house's); down the left edge a sliver of
             its post, its bearing block at its head. Through the scene's camera (edo_street.CAM) at its true size: the
             beam 2.5 m from the lens, the edge 3.4 m. All of it in the shade of our side's houses: the warmest darks of
             the picture, lit only along the edges that face the sunlit street (the post's street side, the hem, the
             lips and the beam's underside: the light thrown up from the band of sun at the crossroads).
    back     the street floor given its texture through the camera (depth.scatter: footprints of straw sandals, pebbles,
             straw, two worn cart tracks along the street, its earth mottled in patches a metre across), all shrinking
             toward the far end; the floor deeper toward us; the eaves' shadows across the band of sun (the toothed edge
             of our side's tile lips and a shop sign's shadow on its two edges); the road god's own shadow thrown away
             from the low sun; a little shade under each thing standing on the floor; the far layers (the roofs along
             the horizon, the drum tower, the fire tower, the cross street going away, the far end of the street) moved
             toward the sky's colour at the horizon.
    japan    the act's watercolour: watercolor.wash(back, seed 1830, soft=WET, wander 1.4, fleck 0.3), WET 1.0 the sky and
             0.55 the far roofs; every cut-out and near.png washed on the same sheet (wash_cut, crisp).
    finish   each picture back to its palette as edo_street.py finishes it (edo_dojima_kit.finish: the back 152 colours,
             the cut-outs their own counts), the grain and speckle 0.010 (the act's watercolour recipe).

The sun is the scene's own: low in the west-south-west, behind us and to the right (edo_street.SUN). Nothing clicked or
stood on moves; the cut-outs keep their outlines exactly.

    python3 edo_street_depth.py        reads out/edo-street-orig/, writes out/edo-street/ and out/edo-street-depth-comp.png
"""

import json
import math
import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import *
from edo_dojima_kit import *
import depth as D
import watercolor as WC
import edo_street as ES
from edo_street import CAM, SUN, ZE, ZW, CROSS, HZ, FULL, SEED as PAINT_SEED

SRC = "out/edo-street-orig"
OUT = "out/edo-street"
SEED = 1830
NAMES = ["prints-1", "prints-2", "noren-kelp", "noren-med", "noren-comb", "bench", "print", "print-ghost", "print-clean", "sign",
         "roadgod", "watervendor"]
SIZES = {"prints-1": 64, "prints-2": 48, "noren-kelp": 32, "noren-med": 32, "noren-comb": 32, "bench": 48, "print": 24, "print-ghost": 32,
         "print-clean": 32, "sign": 40, "roadgod": 32, "watervendor": 48}
BASES = {"roadgod": (251, 491, 34), "watervendor": (733, 448, 52), "sign": (651, 440, 30)}     # x, y of the foot, its width (px)
SKY_LOW = lerp(lerp(tintw(CERULEAN, 0.66), NAPLES, 0.14), PAPER, 0.45)                          # the sky's colour at the horizon


def load(name):
    a = np.asarray(Image.open(os.path.join(SRC, name)).convert("RGBA"), dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def pp(X, Y, Z):
    p = CAM.pt(X, Y, Z)
    return (float(p[0]), float(p[1]))


def gpt(X, Z):
    return pp(X, 0.0, Z)


def kk(X, Z):
    return float(CAM.k(X, Z))


# ================================================================ the near plane
X_POST = -4.0          # the street side of the post's face toward us (its face is 12 cm: the rest is out of the frame)
Z_BEAM = -250.0        # the beam's face toward us; it is 12 cm deep and 20 high (408 to 428 cm)
Y_BEAM = (408.0, 428.0)
Z_EDGE = -337.0        # the eave's edge (75 cm beyond the beam): the rafters drop 0.42 to it
X_END = 60.0           # where the house and its eave end
PITCH = 0.42


def under_y(Z):
    """The underside of the rafters at Z (they lie on the beam and fall toward the street)."""
    return Y_BEAM[1] + PITCH * (Z - (Z_BEAM - 12.0))


def sweep(X):
    """The corner swept up: how much the edge rises near the end of the eave (cm)."""
    t = np.clip((X - (X_END - 70.0)) / 70.0, 0, 1)
    return float(14.0 * t ** 2)


NEAR_WOOD = D.near_tone(lerp(WOOD_SH, SIENNA, 0.40), shade="#2e1c15", k=0.64, warm=0.09)        # a frankly warm dark: the
NEAR_WOOD_DEEP = D.near_tone(WOOD_DARK, shade="#2a1711", k=0.60, warm=0.08)                      # game's paints turn warm
NEAR_SOFFIT = D.near_tone(lerp(WOOD, WOOD_SH, 0.50), shade="#30201a", k=0.64, warm=0.09)          # darks violet
NEAR_TILE = D.near_tone(lerp(TILE_SH, WOOD_SH, 0.45), shade="#2a2026", k=0.68, warm=0.07)
NEAR_INDIGO = D.near_tone(INDIGO, k=0.52, warm=0.05)
NEAR_MARK = D.near_tone(lerp(PLASTER_SH, NAPLES, 0.25), k=0.52, warm=0.05)
NEAR_KAKI = D.near_tone(lerp(SIENNA, mixp(OCHRE, "chrome-orange", 0.3), 0.25), k=0.58, warm=0.08)   # persimmon-dyed cotton
BOUNCE = lerp(mixp(OCHRE, "chrome-orange", 0.35), NAPLES, 0.25)            # the street's warm light thrown up into the shade


def paint_near():
    """-> (colour, alpha) of near.png, before the wash."""
    S = Sheet(SHAPE)
    rng = np.random.default_rng(SEED + 1)
    xl = -60.0                                                    # well off the left edge
    # --- the eave's underside, both sides of the beam, to its edge and its end
    edge = [pp(X, under_y(Z_EDGE) + sweep(X), Z_EDGE) for X in np.linspace(xl, X_END, 24)]
    side = [pp(X_END, under_y(Z) + sweep(X_END), Z) for Z in np.linspace(Z_EDGE, -120.0, 16)]
    outer = [pp(X_END + 4, under_y(Z) + sweep(X_END) + 4, Z) for Z in np.linspace(Z_EDGE - 6, -150.0, 14)]
    top_side = [p for p in outer if p[1] >= -60]
    poly = [(-8.0, -8.0)] + [(top_side[-1][0] + 2, -8.0)] + top_side[::-1] + edge[::-1] + [(-8.0, edge[0][1])]
    S.poly(poly, NEAR_SOFFIT)
    # boards between the rafters: a warmer underside toward the edge (it takes the light from the street)
    for i, Xr in enumerate(np.arange(xl, X_END - 4, 23.0)):
        a, b = Xr + 6.0, min(Xr + 23.0, X_END - 1.0)
        quad = [pp(a, under_y(-262.0), -262.0), pp(b, under_y(-262.0), -262.0), pp(b, under_y(Z_EDGE) + sweep(b), Z_EDGE), pp(a, under_y(Z_EDGE) + sweep(a), Z_EDGE)]
        S.poly(quad, lerp(NEAR_SOFFIT, BOUNCE, 0.05 + 0.04 * rng.random()))
        inner = [pp(a, under_y(-240.0) + 1, -240.0), pp(b, under_y(-240.0) + 1, -240.0), pp(b, under_y(-120.0), -120.0), pp(a, under_y(-120.0), -120.0)]
        S.poly(inner, lerp(NEAR_SOFFIT, NEAR_WOOD_DEEP, 0.25))
    # the rafters: 6 cm, every 31 cm, out over the beam to the edge, and back over us
    for Xr in np.arange(xl, X_END - 2, 23.0):
        for (Z0, Z1) in ((-262.0, Z_EDGE), (-240.0, -120.0)):
            p0 = pp(Xr + 3, under_y(Z0) - 3, Z0)
            p1 = pp(Xr + 3, under_y(Z1) - 3 + (sweep(Xr) if Z1 == Z_EDGE else 0), Z1)
            w0, w1 = 6.0 * kk(Xr, Z0), 6.0 * kk(Xr, Z1)
            q0 = pp(Xr + 6, under_y(Z0) - 3, Z0)
            q1 = pp(Xr + 6, under_y(Z1) - 3 + (sweep(Xr + 6) if Z1 == Z_EDGE else 0), Z1)
            S.poly([pp(Xr, under_y(Z0) - 3, Z0), q0, q1, pp(Xr, under_y(Z1) - 3 + (sweep(Xr) if Z1 == Z_EDGE else 0), Z1)], NEAR_WOOD_DEEP)
            S.line([(p0[0] + w0 * 0.35, p0[1] + 1), (p1[0] + w1 * 0.35, p1[1] + 0.5)], lerp(NEAR_WOOD, BOUNCE, 0.22), max(1.0, w1 * 0.22), 0.7)
    # the edge: a board, then the lips of the round tiles hanging a little below it; the end tile turned up at the corner
    fas_top = [pp(X, under_y(Z_EDGE) + sweep(X), Z_EDGE - 2) for X in np.linspace(xl, X_END + 6, 26)]
    fas_bot = [pp(X, under_y(Z_EDGE) - 7.0 + sweep(X), Z_EDGE - 4) for X in np.linspace(X_END + 6, xl, 26)]
    S.poly(fas_top + fas_bot, NEAR_WOOD_DEEP)
    for Xt in np.arange(xl, X_END - 6, 26.0):
        c = pp(Xt, under_y(Z_EDGE) - 10.0 + sweep(Xt), Z_EDGE - 8)
        r = 7.5 * kk(Xt, Z_EDGE)
        S.ellipse(c[0], c[1], r * 1.05, r * 0.85, NEAR_TILE)
        S.line([(c[0] - r * 0.75, c[1] + r * 0.50), (c[0] + r * 0.65, c[1] + r * 0.58)], lerp(NEAR_TILE, BOUNCE, 0.45), max(1.0, r * 0.20), 0.85)
    # the end of the eave: its verge board along the side, turned up at the corner
    vb = [pp(X_END + 4, under_y(Z) + sweep(X_END) + 4, Z) for Z in np.linspace(Z_EDGE - 6, -150.0, 14)]
    vb2 = [pp(X_END + 4, under_y(Z) + sweep(X_END) - 6, Z) for Z in np.linspace(-150.0, Z_EDGE - 6, 14)]
    S.poly(vb + vb2, NEAR_WOOD_DEEP)
    # --- the beam: its face toward us and its underside, its cut end at the corner
    face = [pp(xl, Y_BEAM[1], Z_BEAM), pp(X_END - 6, Y_BEAM[1], Z_BEAM), pp(X_END - 6, Y_BEAM[0], Z_BEAM), pp(xl, Y_BEAM[0], Z_BEAM)]
    S.poly(face, NEAR_WOOD_DEEP)
    und = [pp(xl, Y_BEAM[0], Z_BEAM), pp(X_END - 6, Y_BEAM[0], Z_BEAM), pp(X_END - 6, Y_BEAM[0], Z_BEAM - 12), pp(xl, Y_BEAM[0], Z_BEAM - 12)]
    S.poly(und, lerp(NEAR_WOOD, BOUNCE, 0.22))
    endf = [pp(X_END - 6, Y_BEAM[1], Z_BEAM), pp(X_END - 6, Y_BEAM[1], Z_BEAM - 12), pp(X_END - 6, Y_BEAM[0], Z_BEAM - 12), pp(X_END - 6, Y_BEAM[0], Z_BEAM)]
    S.poly(endf, lerp(NEAR_WOOD, BOUNCE, 0.18))
    # --- the curtain under the edge: three panels on a pole, two slits, the hem stirring; our mark on the middle panel
    Zc, top, hem = Z_EDGE + 16.0, 393.0, 357.0
    xs = np.linspace(-14.0, X_END - 10.0, 4)
    pole = [pp(xs[0] - 4, top + 2, Zc), pp(xs[-1] + 5, top + 2, Zc)]
    for i in range(3):
        a, b = xs[i] + (0.0 if i == 0 else 1.2), xs[i + 1] - (0.0 if i == 2 else 1.2)
        hem_pts = [pp(X, hem + 1.6 * math.sin(X / 9.0 + i * 1.3) - (2.5 if i == 2 else 0.0) * (X - a) / max(b - a, 1), Zc) for X in np.linspace(b, a, 8)]
        S.poly([pp(a, top, Zc), pp(b, top, Zc)] + hem_pts, NEAR_INDIGO)
        S.line([pp(a + 1.0, top - 1, Zc), pp(a + 1.0, hem + 2, Zc)], lerp(NEAR_INDIGO, PRUSSIAN, 0.3), 1.0, 0.45)   # a fold
    mid = (xs[1] + xs[2]) / 2
    c = pp(mid, (top + hem) / 2 - 1.0, Zc)
    r = 6.8 * kk(mid, Zc)
    S.ellipse(c[0], c[1], r, r, NEAR_MARK)
    S.ellipse(c[0], c[1], r * 0.74, r * 0.74, NEAR_INDIGO)
    S.poly([(c[0] - r * 0.52, c[1] + r * 0.30), (c[0] - r * 0.12, c[1] - r * 0.40), (c[0] + r * 0.08, c[1] - r * 0.12), (c[0] + r * 0.24, c[1] - r * 0.30),
            (c[0] + r * 0.54, c[1] + r * 0.30)], NEAR_MARK)
    for Xh in (xs[0] + 6, mid, xs[-1] - 6):                       # the cords it hangs by
        S.line([pp(Xh, under_y(Zc) - 2, Zc), pp(Xh, top + 3, Zc)], NEAR_WOOD_DEEP, 1.2, 0.9)
    # --- across the top right corner: the hem of the next shop's curtain (two panels of persimmon-dyed cotton, a slit),
    # hanging from a pole under that house's eave, out of the frame above; clear of the drum tower and the roofs
    for (a, b, hm) in ((727.0, 765.0, 106.0), (768.5, 812.0, 112.0)):
        hem_pts = [(xx, hm + 2.2 * math.sin(xx / 7.0) + (xx - a) * 0.05) for xx in np.linspace(b, a, 9)]
        S.poly([(a + 1.5, -6.0), (b, -6.0)] + hem_pts, NEAR_KAKI)
        S.line([(a + 4.0, -4.0), (a + 3.0, hm - 2)], lerp(NEAR_KAKI, NEAR_WOOD_DEEP, 0.45), 1.0, 0.5)
    S.line([(738.0, 40.0), (800.0, 40.0)], lerp(NEAR_KAKI, NEAR_MARK, 0.55), 2.2, 0.85)                  # a dyed band
    S.line([(738.0, 46.0), (800.0, 46.0)], lerp(NEAR_KAKI, NEAR_MARK, 0.55), 1.0, 0.7)
    # --- the post: a sliver of its face down the left edge, its bearing block under the beam
    bx = pp(X_POST, Y_BEAM[0], Z_BEAM)
    blk_top = pp(X_POST + 5, Y_BEAM[0] + 1, Z_BEAM)
    blk_bot = pp(X_POST + 5, Y_BEAM[0] - 9, Z_BEAM)
    S.poly([(-40.0, blk_top[1]), (blk_top[0], blk_top[1]), (blk_bot[0] - 1, blk_bot[1]), (-40.0, blk_bot[1])], NEAR_WOOD_DEEP)
    S.poly([(-40.0, blk_bot[1] - 1), (bx[0], blk_bot[1] - 1), (bx[0] + 0.6, 601.0), (-40.0, 601.0)], NEAR_WOOD)
    col, alpha = S.done()
    # the post's grain and a little variation in every flat (a near thing is never one even colour)
    x, y = grid(SHAPE)
    n = noise(SHAPE, 24, SEED + 3, 3) - 0.5
    col = col * (1 + 0.10 * n[..., None])
    post = ((x < bx[0] + 1.5) & (y > blk_bot[1])).astype(F32) * alpha
    streak = noise((600, 8), 6, SEED + 4, 2)[:, :1] - 0.5
    col = col * (1 + 0.10 * post[..., None] * np.repeat(streak, 800, axis=1)[..., None])
    # deeper toward us and toward the frame's corner (the eave over us is in the deepest shade)
    deep = np.clip(1.0 - (y / 190.0), 0, 1) * np.clip(1.0 - x / 300.0, 0, 1)
    col = lerp(col, col * lerp(np.ones(3, F32), rgb("#6e5244"), 0.5), (0.35 * deep * alpha)[..., None])
    # the lit edges: the post's street side (the sun is to our right), and every edge that faces the sunlit street below
    r_side = D.rim(alpha, light=(1.0, -0.15), width=2.2) * post
    r_low = D.rim(alpha, light=(0.25, 1.0), width=1.8) * (1 - post)
    col = lerp(col, BOUNCE, (np.clip(r_side * 0.85, 0, 1))[..., None])
    col = lerp(col, lerp(BOUNCE, col, 0.35), (np.clip(r_low * 0.65, 0, 1))[..., None])
    return np.clip(col, 0, 1).astype(F32), alpha


# ================================================================ the backdrop
def far_masks():
    """Where the far layers are (their alpha, drawn again through the painter's own functions: geometry only)."""
    z, o = np.zeros((H, W, 3), F32), np.ones((H, W, 3), F32)

    def alpha_of(fn):
        a0, a1 = z.copy(), o.copy()
        fn(a0)
        fn(a1)
        return np.clip(1.0 - (a1 - a0).mean(axis=2), 0, 1)

    roofs = alpha_of(lambda p: ES.far_roofs(p, PAINT_SEED))
    s = Paper(SHAPE)
    ES.drum_tower(s)
    drum = s.done()[1]
    s = Paper(SHAPE)
    ES.fire_tower(s, s)
    fire = s.done()[1]
    cross = alpha_of(lambda p: ES.paint_cross(p, PAINT_SEED))
    ground = alpha_of(lambda p: ES.paint_ground(p, PAINT_SEED))

    def fronts(p):
        ES.details(p, {}, seed=PAINT_SEED, fast=True)
    stand = alpha_of(fronts)
    # what of each layer is still seen (the painter laid them in this order: roofs, drum tower, cross street and fire
    # tower, the street's floor, the fronts)
    ground = ground * (1 - stand)
    cross = cross * (1 - ground) * (1 - stand)
    fire = fire * (1 - ground) * (1 - stand)
    drum = drum * (1 - cross) * (1 - ground) * (1 - stand)
    roofs = roofs * (1 - drum) * (1 - cross) * (1 - ground) * (1 - stand)
    return roofs, drum, fire, cross, ground, stand


def paint_back(back):
    pic = back.copy()
    x, y = grid(SHAPE)
    X, Z, m = CAM.floor()
    street = ((m > 0.5) & (Z > ZE + 20) & (y > HZ)).astype(F32)
    Xw = X + SUN[0] / SUN[2] * (ZW - Z)
    band = ((Xw >= CROSS[0]) & (Xw <= CROSS[1])).astype(F32) * street
    shade_m = street * (1 - band)
    pt, k = gpt, kk
    rng = np.random.default_rng(SEED + 20)
    # --- the earth mottled in patches (damp and dust), a metre across, and its grit; both lie on the ground
    tile = noise((1024, 1024), 64, SEED + 21, 4)
    tile2 = noise((1024, 1024), 64, SEED + 22, 3)

    def fold(t):
        mm = np.mod(t, 2 * 1022)
        return np.where(mm > 1022, 2 * 1022 - mm, mm)
    Xs, Zs = np.where(street > 0, X, 0), np.where(street > 0, Z, -1000)
    kpx = np.where(street > 0, CAM.v.F / np.maximum(CAM.v.depth(Xs, Zs), 1e-3), 0.01)
    big = sample(tile, fold(Xs / 110.0 * 64 + 300), fold(Zs / 70.0 * 64 + 300)) - 0.5
    grit = sample(tile2, fold(Xs / 9.0 * 64 + 100), fold(Zs / 9.0 * 64 + 100)) - 0.5
    fine = np.clip((9.0 * kpx - 1.2) / 3.0, 0, 1)                  # the grit fades where a grain would be under a pixel
    shade_tone = 1 + (0.085 * big + 0.075 * grit * fine) * street
    pic *= shade_tone[..., None]
    # --- the floor deeper toward us (and a little cooler in the shade), paler toward the far end
    t = np.clip((y - 430.0) / 170.0, 0, 1) ** 1.3
    pic = lerp(pic, pic * rgb("#8a8098") * 1.08, (0.30 * t * shade_m + 0.16 * t * band)[..., None])
    # --- two cart tracks worn along the street (X), wandering; footprints of straw sandals; pebbles; straw
    S = Sheet(SHAPE)
    for (Z0, wob) in ((-1010.0, 1.0), (-1095.0, 1.3), (-860.0, 0.7)):
        Xs_ = np.linspace(-600.0, 4200.0, 220)
        Zr = Z0 + 9.0 * np.sin(Xs_ / 260.0 * wob) + 5.0 * np.sin(Xs_ / 97.0 + Z0)
        for i in range(len(Xs_) - 1):
            a, b = pt(Xs_[i], Zr[i]), pt(Xs_[i + 1], Zr[i + 1])
            if not (-20 < a[0] < 820 and HZ < a[1] < 610):
                continue
            w = 7.0 * k(Xs_[i], Zr[i])
            S.line([a, b], rgb("#3a3450"), max(0.6, w * 0.55), 0.20 if Z0 > -900 else 0.26)
            S.line([(a[0], a[1] + w * 0.35), (b[0], b[1] + w * 0.35)], rgb("#fff4dc"), max(0.5, w * 0.22), 0.10)
    zone = (street > 0.5).astype(F32)
    for (sx, sy, kp, r) in D.scatter(pt, k, (-700, 4200, -1290, -560), 0.9, SEED + 30, size=(24, 10), zone=zone):
        ang = math.radians(rng.uniform(-25, 25) + (0 if r < 0.6 else 180))
        dX, dZ = math.cos(ang), math.sin(ang)
        Xg, Zg = [float(v) for v in CAM.floor_at(sx, sy)]
        for side in (-1, 1):
            if r < 0.25 and side == 1:
                continue
            Xc, Zc = Xg + side * 9.0 * -dZ, Zg + side * 9.0 * dX
            pts = [pt(Xc + 12 * dX * math.cos(u) - 4.5 * -dZ * math.sin(u), Zc + 12 * dZ * math.cos(u) - 4.5 * dX * math.sin(u)) for u in np.linspace(0, 2 * math.pi, 10)]
            S.poly(pts, rgb("#40385a"), 0.16)
    for (sx, sy, kp, r) in D.scatter(pt, k, (-700, 4200, -1290, -560), 3.0, SEED + 31, size=(3.0, 2.0), zone=zone):
        rr = max(0.45, (1.2 + 1.8 * r) * kp)
        S.ellipse(sx, sy + rr * 0.35, rr * 1.1, rr * 0.55, rgb("#2e2a44"), 0.30)
        S.ellipse(sx, sy, rr, rr * 0.62, lerp(EARTH, NAPLES, 0.25), 0.32)
    for (sx, sy, kp, r) in D.scatter(pt, k, (-700, 4200, -1290, -560), 1.2, SEED + 32, size=(14, 1)):
        if zone[int(sy), int(sx)] < 0.5:
            continue
        L = 14.0 * kp
        ang = rng.uniform(0, math.pi)
        S.line([(sx, sy), (sx + L * math.cos(ang), sy + L * math.sin(ang) * 0.35)], lerp(OCHRE, NAPLES, 0.5), max(0.5, 1.2 * kp), 0.55)
    c, a = S.done()
    over(pic, c, a * street)
    # --- the eaves' shadows across the band of sun: our side's tile lips (a toothed edge) and a shop sign's shadow
    sh = np.zeros(SHAPE, F32)
    over_hang = 55.0
    lips = 0.5 + 0.5 * np.cos(2 * math.pi * (Z / 26.0))
    for (edge_x, sgn) in ((CROSS[0], 1.0), (CROSS[1], -1.0)):
        d = (Xw - edge_x) * sgn                                    # how far into the band (cm, at our side's fronts)
        strip = ((d >= 0) & (d < over_hang - 9.0 * lips) & (Z > -1213.0)).astype(F32)
        sh = np.maximum(sh, strip)
    # a sign hanging from the corner house at the right of the gap (its shadow: a board on two cords)
    sgx, sgz0, sgz1 = CROSS[1] - 95.0, -1150.0, -1010.0
    sign = ((Xw > sgx - 34) & (Xw < sgx) & (Z > sgz0) & (Z < sgz1)).astype(F32)
    cords = ((np.abs(Xw - (sgx - 6)) < 1.6) | (np.abs(Xw - (sgx - 28)) < 1.6)).astype(F32) * ((Z >= sgz1) & (Z < sgz1 + 130)).astype(F32)
    sh = np.maximum(sh, np.maximum(sign, cords))
    sh = blur(sh, 0.8) * band
    glaze = lerp(np.ones(3, F32), rgb("#6f6a9a"), 1.0)
    pic = lerp(pic, pic * glaze, (0.45 * sh)[..., None])
    # --- the road god's shadow, thrown away from the sun (left and away), on the sunlit floor; shade under what stands
    dX, dZ = -SUN[0], -SUN[2]
    L = 1.0 / math.hypot(dX, dZ) * (SUN[1] / math.hypot(SUN[0], SUN[2])) ** -1
    gx, gz = [float(v) for v in CAM.floor_at(251, 491)]
    h = 66.0
    ex, ez = gx + dX * L * h, gz + dZ * L * h
    wv = 17.0
    nx, nz = -dZ / math.hypot(dX, dZ), dX / math.hypot(dX, dZ)
    places = [(gx + nx * wv, gz + nz * wv), (ex + nx * wv * 0.7, ez + nz * wv * 0.7), (ex - nx * wv * 0.7, ez - nz * wv * 0.7), (gx - nx * wv, gz - nz * wv)]
    D.shadow_on_ground(pic, gpt, places, color="#55507a", amount=0.50, soft=1.4, wobble=0.8, seed=SEED + 40, ground=band)
    for name, (bx, by, bw) in BASES.items():
        mm = mask_ellipse(SHAPE, bx, by + 1, bw * 0.62, max(3.0, bw * 0.13), soft=3.0)
        pic = lerp(pic, pic * rgb("#6c6890"), (0.45 * mm * street)[..., None])
    return np.clip(pic, 0, 1), street, band


def air_back(pic, masks, street):
    roofs, drum, fire, cross, ground, stand = masks
    x, y = grid(SHAPE)
    X, Z, m = CAM.floor()
    far = np.zeros(SHAPE, F32)
    far = np.maximum(far, roofs * 0.62)
    far = np.maximum(far, drum * 0.50)
    far = np.maximum(far, fire * 0.36)
    xc = np.clip((470.0 - x) / 220.0, 0, 1)
    far = np.maximum(far, cross * (1 - fire) * (0.22 + 0.36 * xc))
    dist = np.where(street > 0, np.hypot(X, Z), 0)
    far = np.maximum(far, street * np.clip((dist - 1500.0) / 3200.0, 0, 1) * 0.55)
    # the far end of the street at the right: the comb-maker's and beyond, a little into the air
    right = np.clip((x - 700.0) / 100.0, 0, 1) * stand * (y < 420)
    far = np.maximum(far, right * 0.16)
    far = blur(far, 1.0)
    return D.air(pic, far, SKY_LOW, amount=0.60), far


def wet_map(masks):
    roofs, drum, fire, cross, ground, stand = masks
    solid = np.clip(roofs + drum + fire + cross + ground + stand, 0, 1)
    sky = np.clip(1 - solid, 0, 1)
    wet = np.maximum(sky * 1.0, roofs * 0.55)
    return wet.astype(F32)


if __name__ == "__main__":
    import time
    t0 = time.time()
    back, _ = load("back.png")
    masks = far_masks()
    print("masks", round(time.time() - t0, 1))
    deep, street, band = paint_back(back)
    deep, far = air_back(deep, masks, street)
    print("back", round(time.time() - t0, 1))
    WET = wet_map(masks)
    near_c, near_a = paint_near()
    print("near", round(time.time() - t0, 1), "share", round(float(near_a.mean()) * 100, 1))
    washed = WC.wash(deep, seed=SEED, soft=WET, wander=1.4, fleck=0.3)
    print("wash", round(time.time() - t0, 1))
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".png"):
            os.remove(os.path.join(OUT, f))
    finish(washed, OUT + "/back.png", 152, None, amount=0.010, speckle=0.010)
    # the cut-outs washed on the same sheet as the backdrop (wash_cut, the same seed, crisp): those that stand together
    # in the game are laid in together and washed once (the three states of the print each with the bench under it)
    cuts = {name: load(name + ".png") for name in NAMES}
    groups = [[n for n in NAMES if n not in ("print-ghost", "print-clean")], ["bench", "print-ghost"], ["bench", "print-clean"]]
    comp = washed.copy()
    for gi, group in enumerate(groups):
        col, alpha = deep.copy(), np.zeros(SHAPE, F32)
        for n in group:
            c, a = cuts[n]
            col = col * (1 - a[..., None]) + c * a[..., None]
            alpha = np.maximum(alpha, a)
        wc = WC.wash_cut(col, alpha, deep, seed=SEED, soft=WET, wander=1.4, fleck=0.3, crisp=True)
        for n in group:
            if gi > 0 and n == "bench":
                continue
            c, a = cuts[n]
            finish(wc, f"{OUT}/{n}.png", SIZES[n], a, amount=0.010, speckle=0.010)
            if gi == 0:
                over(comp, wc, (a > 0.5).astype(F32))
        print("cut-outs", gi, round(time.time() - t0, 1))
    wn = WC.wash_cut(near_c, near_a, deep, seed=SEED, soft=WET, wander=1.4, fleck=0.3, crisp=True)
    finish(wn, OUT + "/near.png", 64, near_a, amount=0.010, speckle=0.010)
    over(comp, wn, (near_a > 0.5).astype(F32))
    shutil.copy(os.path.join(SRC, "layout.json"), os.path.join(OUT, "layout.json"))
    Image.fromarray((np.clip(comp, 0, 1) * 255).astype(np.uint8)).save("out/edo-street-depth-comp.png")
    Image.fromarray((np.clip(far, 0, 1) * 255).astype(np.uint8)).save("out/edo-street-depth-far.png")
    Image.fromarray((np.clip(WET, 0, 1) * 255).astype(np.uint8)).save("out/edo-street-depth-wet.png")
    print("done", round(time.time() - t0, 1))

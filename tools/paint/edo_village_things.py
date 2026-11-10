"""PAINT-23A (round twenty-three, DEPTH.md): the built things of Yui's backdrop, drawn through the scene's one camera
with more truth than boxes, each face a graded wash (edo_village_kit.Wet): Kihei's shop, the houses down the street
overlapping one another, the well, the cherry and the shrine's gate, pines, and the set dressing that stands where
nobody walks.

The research is round twenty's (edo_village.py's header): a fishing village and post town of the Tokaido in 1830; roofs
of wooden shingles weighted with stones on battens, a few of thatch; walls of boards below and earth plaster above in a
frame of posts and beams; shop fronts open to the street, with noren. Nothing wheeled stands in the street (goods went
on backs and packhorses on this road). Nothing here reads as a cross: no bare mast and yard, no crossed poles.

LIGHT  the sun behind us and to the left, 30 degrees up (kit.SUN3). Faces turned to us and the left are lit; an eave
       throws its shadow down the wall under it; a wall in shade is a cool wash, warmer toward the sunlit ground.
"""

import math

import numpy as np

from brush import *
from edo_village_kit import *
from edo_village_far import HORIZON_C

SHAPE = (H, W)
TIMBER = mixp(SIENNA, PRUSSIAN, 0.52)
TIMBER_LIT = thin(mixp(SIENNA, OCHRE, 0.42), 0.22)
BOARD_LIT = thin(mixp(SIENNA, OCHRE, 0.50), 0.42)
BOARD_SHADE = thin(mixp(SIENNA, PRUSSIAN, 0.42), 0.22)
EARTHWALL = thin(mixp(OCHRE, NAPLES, 0.45), 0.66)             # an earth-plaster wall in the sun: nearly the paper
WALL_SHADE = thin(mixp(COBALT, SIENNA, 0.26), 0.44)           # a wall in shade: a cool wash
WALL_BOUNCE = thin(mixp(OCHRE, SIENNA, 0.30), 0.52)           # the same near the sunlit ground: warm light bounced up
SHINGLE = thin(lerp(SHINGLE_LIT, NAPLES, 0.22), 0.30)         # weathered shingles in the sun: silver, a little warm
SHINGLE_LOW = thin(lerp(SHINGLE_LIT, COBALT, 0.20), 0.10)
SHINGLE_SH = thin(lerp(SHINGLE_SHADE, SIENNA, 0.12), 0.30)
THATCH = thin(THATCH_LIT, 0.34)
THATCH_LOW = thin(lerp(THATCH_LIT, SIENNA, 0.22), 0.14)
THATCH_SH = thin(lerp(THATCH_SHADE, COBALT, 0.20), 0.24)
STONE = thin(lerp(PRUSSIAN, OCHRE, 0.16), 0.52)


def aired(c, z, most=0.55):
    """A colour as it is at depth z (cm): toward the sky's colour at the horizon, more the farther."""
    return lerp(np.asarray(c, dtype=F32), HORIZON_C, float(np.clip((z - 1400.0) / 9000.0, 0, most)))


def add2(p, d, k=1.0):
    return (p[0] + d[0] * k, p[1] + d[1] * k)


def house(L, z0, z1, depth, eave, ridge, over_, a=None, lift=0.0, thatch=False, level=0, seed=0, shop=None, stones=True):
    """A house along the street (its street side on x = a + M z from z0 to z1, its depth inland), under a hipped roof.
    From this camera what shows is its near end (lit: it faces us and the left), its inland side (in shade), the near
    hip of the roof (lit) and the inland slope (hardly lit). `level`: how much is drawn (0 far, 1 nearer, 2 the shop).
    -> its near end wall as picture points (the shop's is the scene's `shop` area)."""
    a = FRONT_A if a is None else a
    rng = np.random.default_rng(int(z0) * 3 + seed)
    F0, F1 = (a + M * z0, z0), (a + M * z1, z1)
    B0, B1 = add2(F0, N_IN, depth), add2(F1, N_IN, depth)
    G = lambda q, y=0.0: gp(q[0], q[1], lift + y)
    hip = depth / 2 * 0.95
    Mn = add2(((F0[0] + B0[0]) / 2, (F0[1] + B0[1]) / 2), U_ST, hip)
    Mf = add2(((F1[0] + B1[0]) / 2, (F1[1] + B1[1]) / 2), U_ST, -hip)
    ov = over_
    eF0 = add2(add2(F0, U_ST, -ov), N_IN, -ov)
    eB0 = add2(add2(B0, U_ST, -ov), N_IN, ov)
    eB1 = add2(add2(B1, U_ST, ov), N_IN, ov)
    e_h = eave - ov * 0.5
    zc = (z0 + z1) / 2
    air = lambda c: aired(c, zc)
    row0 = G(F0)[1]
    kk = kz(z0)
    W_ = lambda d, y=0.0: G(add2(F0, N_IN, d), y)                    # a point of the near end wall: d cm from its street corner, y up
    S_ = lambda d, y=0.0: G(add2(B0, U_ST, d), y)                    # a point of the inland side: d cm along it from the near corner
    side_len = math.hypot(B1[0] - B0[0], B1[1] - B0[1])
    # ---------------- the walls
    end = [G(F0), G(B0), G(B0, eave), G(F0, eave)]
    L.poly(end, air(WPAPER if level == 2 else thin(EARTHWALL, 0.2)), air(EARTHWALL), g=(end[3], end[1]))
    L.poly([G(B0), G(B1), G(B1, eave), G(B0, eave)], air(WALL_SHADE), air(WALL_BOUNCE), g=(G(B0, eave), G(B0)))
    if level >= 1:
        # boards on the lower wall of the near end, a rail over them; posts at the corners
        hb = 92.0
        L.poly([W_(0), W_(depth), W_(depth, hb), W_(0, hb)], air(BOARD_LIT), air(lerp(BOARD_LIT, BOARD_SHADE, 0.45)), g=(W_(0, hb), W_(0)))
        if level == 2 or kk > 0.2:
            for d in np.arange(12.0, depth, 24.0 if level == 2 else 40.0):
                L.line([W_(d, 2), W_(d, hb - 2)], air(TIMBER), 0.5, 0.30 + 0.2 * rng.random())
        L.line([W_(0, hb), W_(depth, hb)], air(TIMBER), max(0.7, 5 * kk), 0.85)
        for d in (5.0, depth - 5.0):
            L.poly([W_(d - 6), W_(d + 6), W_(d + 6, eave), W_(d - 6, eave)], air(TIMBER_LIT), air(lerp(TIMBER_LIT, TIMBER, 0.5)))
        L.line([W_(0, eave - 5), W_(depth, eave - 5)], air(TIMBER), max(0.7, 7 * kk), 0.8)             # the plate under the eave
        # the inland side: boards to the eave, a door and a window in it, dark
        nb = max(3, int(side_len / (26.0 if level == 2 else 60.0)))
        for i in range(1, nb):
            d = side_len * i / nb
            L.line([S_(d, 3), S_(d, eave - 6)], air(lerp(WALL_SHADE, PRUSSIAN, 0.45)), 0.5, 0.22 + 0.15 * rng.random())
        for (d0, d1, y0, y1, c) in ((side_len * 0.16, side_len * 0.34, 0.0, 172.0, mixp(SIENNA, PRUSSIAN, 0.66)), (side_len * 0.52, side_len * 0.80, 88.0, 158.0, mixp(SIENNA, PRUSSIAN, 0.58))):
            L.poly([S_(d0, y0), S_(d1, y0), S_(d1, y1), S_(d0, y1)], air(thin(c, 0.10)))
            if y0 > 0:                                                      # the window's bars
                for d in np.linspace(d0, d1, 6)[1:-1]:
                    L.line([S_(d, y0), S_(d, y1)], air(WALL_BOUNCE), 0.6, 0.6)
    if shop:
        shop_front(L, W_, kk, rng)
    # ---------------- the eave's shadow down the wall (the sun is 30 degrees up: a deep eave shades a good band)
    drop = ov * 0.78
    L.glaze([W_(-2, eave), W_(depth + 2, eave), W_(depth + 2, eave - drop), W_(-2, eave - drop * 0.86)], SHADE_WARM, 0.85)
    L.glaze([S_(-2, eave), S_(side_len, eave), S_(side_len, eave - 20), S_(-2, eave - 20)], SHADE, 0.45)
    if shop:
        shop_hangings(L, W_, kk, rng)
    # ---------------- the roof: the near hip (lit) and the inland slope, one hard edge between
    A, B, apex = eF0, eB0, Mn
    R = lambda q, y: G(q, y)

    def hp(u, v):                                                           # a point of the hip: u along its eave, v up to the apex
        bx, bz = A[0] + (B[0] - A[0]) * u, A[1] + (B[1] - A[1]) * u
        return R((bx + (apex[0] - bx) * v, bz + (apex[1] - bz) * v), e_h + (ridge - e_h) * v)

    def sp(u, v):                                                           # a point of the inland slope: u along its eave, v up to the ridge
        ex, ez = eB0[0] + (eB1[0] - eB0[0]) * u, eB0[1] + (eB1[1] - eB0[1]) * u
        rx, rz = Mn[0] + (Mf[0] - Mn[0]) * u, Mn[1] + (Mf[1] - Mn[1]) * u
        return R((ex + (rx - ex) * v, ez + (rz - ez) * v), e_h + (ridge - e_h) * v)
    lit_c, low_c, sh_c = (THATCH, THATCH_LOW, THATCH_SH) if thatch else (SHINGLE, SHINGLE_LOW, SHINGLE_SH)
    th = (34.0 if thatch else 9.0)
    hip_face = [hp(0, 0), hp(1, 0), hp(0.5, 1)]
    slope = [sp(0, 0), sp(1, 0), sp(1, 1), sp(0, 1)]
    L.poly(slope, air(lerp(sh_c, lit_c, 0.18)), air(sh_c), g=(sp(0.3, 1), sp(0.3, 0)))
    L.poly(hip_face, air(lit_c), air(low_c), g=(hp(0.5, 1), hp(0.5, 0)))
    # the eave's edge has a thickness: the cut ends of the thatch (pale, layered), or the shingles' ends and the board under them
    edge_c = air(lerp(THATCH_LOW, SIENNA, 0.25)) if thatch else air(lerp(SHINGLE_SH, PRUSSIAN, 0.25))
    L.poly([R(eF0, e_h), R(eB0, e_h), R(eB0, e_h - th), R(eF0, e_h - th)], edge_c, air(lerp(edge_c, PRUSSIAN, 0.35)))
    L.poly([R(eB0, e_h), R(eB1, e_h), R(eB1, e_h - th), R(eB0, e_h - th)], air(lerp(edge_c, PRUSSIAN, 0.30)))
    if thatch:
        if level >= 1 or kk > 0.16:
            n = max(5, int(math.hypot(B[0] - A[0], B[1] - A[1]) / 26))
            for i in range(n):                                              # the straw runs down the slope: dry strokes
                u = (i + rng.random()) / n
                v0 = rng.uniform(0.0, 0.5)
                L.line([hp(u, v0), hp(u + rng.normal(0, 0.01), min(0.96, v0 + rng.uniform(0.2, 0.45)))], air(lerp(THATCH_LOW, SIENNA, 0.3)), 0.6, 0.22 + 0.2 * rng.random())
            for i in range(max(4, int(side_len / 40))):
                u = (i + rng.random()) / max(4, int(side_len / 40))
                v0 = rng.uniform(0.0, 0.5)
                L.line([sp(u, v0), sp(u, min(0.96, v0 + rng.uniform(0.2, 0.45)))], air(lerp(THATCH_SH, PRUSSIAN, 0.3)), 0.6, 0.25)
        # the ridge: a roll of straw bound along it
        L.line([sp(0, 1), sp(1, 1)], air(lerp(THATCH_LOW, SIENNA, 0.4)), max(1.0, 16 * kk), 0.95)
        L.line([add2(sp(0, 1), (0, -max(0.5, 5 * kk))), add2(sp(1, 1), (0, -max(0.5, 5 * kk)))], air(THATCH), max(0.6, 5 * kk), 0.8)
    else:
        nc = 13 if level == 2 else (7 if kk > 0.16 else 0)
        for i in range(1, nc):                                              # the courses of shingles, along the eave
            v = i / nc
            keyline(L, [hp(u, v) for u in np.linspace(0, 1, 6)], row=max(row0, HZ + 80), seed=i + seed, color=air(mixp(SIENNA, PRUSSIAN, 0.40)), alpha=0.34 if level == 2 else 0.18)
            keyline(L, [sp(u, v) for u in np.linspace(0, 1, 6)], row=max(row0, HZ + 80), seed=i + 40 + seed, color=air(PRUSSIAN), alpha=0.20)
            if level == 2:                                                  # the joints between shingles, staggered course by course; a few shingles darker, a few bleached
                m_ = int(26 * (1 - v)) + 3
                for j in range(m_):
                    u = (j + 0.5 * (i % 2) + rng.uniform(-0.15, 0.15)) / m_
                    if 0.02 < u < 0.98:
                        L.line([hp(u, v), hp(u, v - 1.0 / nc * 0.92)], air(mixp(SIENNA, PRUSSIAN, 0.40)), 0.5, 0.20 + 0.16 * rng.random())
                        t_ = rng.random()
                        if t_ < 0.16:
                            u2 = min(0.98, u + 1.0 / m_)
                            L.poly([hp(u, v), hp(u2, v), hp(u2, v - 0.92 / nc), hp(u, v - 0.92 / nc)], air(SHINGLE_SH if t_ < 0.09 else WPAPER), alpha=0.16)
        if level == 2:
            for _ in range(9):                                              # rain has streaked it, down the slope
                u, v0 = rng.uniform(0.08, 0.92), rng.uniform(0.25, 0.8)
                L.line([hp(u, v0), hp(u + rng.normal(0, 0.01), max(0.02, v0 - rng.uniform(0.15, 0.4)))], air(mixp(SIENNA, PRUSSIAN, 0.45)), rng.uniform(1.0, 2.2), 0.10)
        if stones:
            for (pt_, base_len, rows_v) in ((hp, math.hypot(B[0] - A[0], B[1] - A[1]), (0.16, 0.44, 0.70) if level == 2 else (0.2, 0.55)),
                                             (sp, math.hypot(eB1[0] - eB0[0], eB1[1] - eB0[1]), (0.2, 0.52, 0.8) if level == 2 else (0.25, 0.62))):
                for v in rows_v:
                    span = (1 - v) if pt_ is hp else 1.0                    # (a course of the hip shortens toward the apex)
                    n = max(2, int(base_len * span / 62))
                    L.line([pt_(u, v) for u in np.linspace(0.03, 0.97, 5)], air(lerp(sh_c, PRUSSIAN, 0.4)), max(0.6, 3.5 * kk), 0.7)      # the batten the stones sit on
                    for i in range(n):
                        u = 0.04 + 0.92 * (i + 0.5 + rng.normal(0, 0.12)) / n
                        q = pt_(u, v)
                        r = max(0.9, rng.uniform(7.5, 11.0) * kk)
                        L.ellipse(q[0] + r * 0.45, q[1] + r * 0.30, r * 1.05, r * 0.55, air(lerp(sh_c, PRUSSIAN, 0.45)), alpha=0.6)      # its shadow, to the right
                        L.ellipse(q[0], q[1] - r * 0.25, r, r * 0.72, air(thin(STONE, 0.25)), air(lerp(STONE, PRUSSIAN, 0.35)), g=((q[0] - r, q[1] - r), (q[0] + r, q[1] + r)))
        L.line([sp(0, 1), sp(1, 1)], air(lerp(sh_c, PRUSSIAN, 0.35)), max(0.8, 8 * kk), 0.9)          # the ridge board
    if level == 2:                                                          # the paper left bare along the sunlit edges: the hip's left edge, the eave's lip
        L.line([hp(0.0, 0.0), hp(0.5, 1.0)], WPAPER, 1.1, 0.75)
        L.line([hp(0.02, 0.012), hp(0.98, 0.012)], WPAPER, 0.9, 0.55)
    # ---------------- the key line: only on the shade side and under things; the lit edges are left to the paper
    for pts in ([R(eF0, e_h - th), R(eB0, e_h - th), R(eB1, e_h - th)], [G(B0), G(B0, eave)], [G(B1), G(B1, eave)], [G(B0), G(B1)], [sp(0, 1), sp(1, 1), sp(1, 0)]):
        keyline(L, pts, row0, seed=seed + 3)
    keyline(L, [hp(0.5, 1), hp(1, 0)], row0, seed=seed + 5, alpha=0.3)                                 # the hip between light and shade
    return end


def shop_front(L, W_, kk, rng):
    """Kihei's shop, its near end (the scene's `shop` area; the noren hangs in the opening as a cut-out): the frame of
    posts and beams, the open front with the raised floor inside in shade, a barred window, things hung under the eave."""
    # the opening: 185 wide and high, 25 from the corner (round twenty's: the noren fits it)
    o0, o1, oh = 25.0, 210.0, 185.0
    inside_top, inside_low = mixp(SIENNA, PRUSSIAN, 0.70), thin(mixp(SIENNA, PRUSSIAN, 0.46), 0.10)
    L.poly([W_(o0), W_(o1), W_(o1, oh), W_(o0, oh)], inside_top, inside_low, g=(W_(o0, oh), W_(o0, 0)))
    # inside: the earth floor at the left, the raised floor's edge, tubs and a basket on it, in the light from the door
    L.poly([W_(o0 + 52, 0), W_(o1, 0), W_(o1, 38), W_(o0 + 52, 38)], mixp(SIENNA, PRUSSIAN, 0.60))
    L.poly([W_(o0 + 52, 38), W_(o1, 38), W_(o1, 45), W_(o0 + 52, 45)], thin(mixp(OCHRE, SIENNA, 0.35), 0.25))
    for (d, wd, hg, c) in ((92.0, 38.0, 26.0, thin(mixp(OCHRE, SIENNA, 0.5), 0.3)), (146.0, 46.0, 20.0, thin(mixp(OCHRE, PRUSSIAN, 0.45), 0.35)), (188.0, 26.0, 34.0, thin(mixp(SIENNA, OCHRE, 0.3), 0.3))):
        L.poly([W_(d - wd / 2, 45), W_(d + wd / 2, 45), W_(d + wd / 2 + 3, 45 + hg), W_(d - wd / 2 - 3, 45 + hg)], lerp(c, PRUSSIAN, 0.35), lerp(c, PRUSSIAN, 0.6))
        L.line([W_(d - wd / 2 - 3, 45 + hg), W_(d + wd / 2 + 3, 45 + hg)], c, max(0.7, 3 * kk), 0.8)
    L.line([W_(o0 + 20, 0), W_(o0 + 46, 0)], thin(EARTH, 0.2), max(1.0, 9 * kk), 0.5)                 # daylight on the earth floor inside the door
    # the frame: jambs, the lintel, a beam at the same height along the wall, the sill
    for d in (o0 - 6.0, o1 + 6.0, 300.0, 391.0):
        L.poly([W_(d - 6), W_(d + 6), W_(d + 6, 225), W_(d - 6, 225)], TIMBER_LIT, lerp(TIMBER_LIT, TIMBER, 0.6))
        L.line([W_(d + 6, 2), W_(d + 6, 224)], TIMBER, 0.6, 0.5)
    L.poly([W_(o0 - 12, oh), W_(450, oh), W_(450, oh + 13), W_(o0 - 12, oh + 13)], TIMBER_LIT, lerp(TIMBER_LIT, TIMBER, 0.5))
    L.line([W_(o0 - 12, oh), W_(450, oh)], TIMBER, 0.7, 0.6)
    L.poly([W_(o0, 0), W_(o1, 0), W_(o1, 7), W_(o0, 7)], thin(TIMBER_LIT, 0.2))
    # the barred window to the right
    w0, w1, wy0, wy1 = 322.0, 380.0, 104.0, 168.0
    L.poly([W_(w0, wy0), W_(w1, wy0), W_(w1, wy1), W_(w0, wy1)], mixp(SIENNA, PRUSSIAN, 0.66), mixp(SIENNA, PRUSSIAN, 0.5))
    for d in np.linspace(w0, w1, 8)[1:-1]:
        L.line([W_(d, wy0), W_(d, wy1)], TIMBER_LIT, max(0.7, 3.2 * kk), 0.95)
    for y_ in (wy0, wy1):
        L.line([W_(w0 - 4, y_), W_(w1 + 4, y_)], TIMBER_LIT, max(0.8, 5 * kk), 1.0)
    # a sedge hat hung on the post (the fish drying under the eave are laid after the eave's shadow: shop_hangings)
    hat = W_(300, 150)
    L.ellipse(hat[0], hat[1], 15 * kk, 15 * kk, thin(OCHRE, 0.45), thin(mixp(OCHRE, SIENNA, 0.4), 0.2), g=((hat[0] - 8, hat[1] - 8), (hat[0] + 8, hat[1] + 8)))
    L.ellipse(hat[0] + 0.5, hat[1] + 0.5, 4.5 * kk, 4.5 * kk, thin(mixp(OCHRE, SIENNA, 0.5), 0.2))
    # the footing: a row of flat stones under the sill beam
    for d in np.arange(214.0, 450.0, 26.0):
        q = W_(d + 12, 5)
        L.ellipse(q[0], q[1], 12 * kk, 5.5 * kk, thin(STONE, 0.3), lerp(STONE, PRUSSIAN, 0.3))


def shop_hangings(L, W_, kk, rng):
    """Under Kihei's eave, right of the door: a bamboo pole on two cords, split fish hung on it by their tails to dry in
    the shade (a fish shop's morning work). Small and pale against the wall; in the eave's shadow at the top."""
    pole_c = lerp(OCHRE, PRUSSIAN, 0.40)
    for d in (226.0, 294.0):
        L.line([W_(d, 222), W_(d, 197)], pole_c, 0.6, 0.8)
    L.line([W_(222, 197), W_(298, 197)], pole_c, max(0.8, 3.2 * kk), 0.95)
    for d in np.linspace(232, 288, 5):
        top = W_(d + rng.normal(0, 1.5), 196)
        ln = (21 + 5 * rng.random()) * kk
        hw = 5.0 * kk
        c = thin(mixp(OCHRE, COBALT, 0.34 + 0.08 * rng.random()), 0.30)
        L.poly([(top[0], top[1]), (top[0] + hw, top[1] + ln * 0.42), (top[0] + hw * 0.3, top[1] + ln), (top[0] - hw * 0.3, top[1] + ln), (top[0] - hw, top[1] + ln * 0.42)], thin(c, 0.25), lerp(c, PRUSSIAN, 0.25))
        L.line([(top[0], top[1] + 1), (top[0], top[1] + ln - 1)], lerp(c, PRUSSIAN, 0.45), 0.5, 0.6)


# ---------------------------------------------------------------- the well
def well(L, WELL):
    """The well on the seaward side of the street: a square wooden curb, a little roof on two posts (its seaward slope in
    the sun, the other in shade), the bucket hung under it on its rope. Darker and firmer than the houses beyond it: it
    stands well before them."""
    wz = WELL["z"]
    wx = street_x(wz) + WELL["off"]
    r, hgt = WELL["r"], WELL["h"]
    k = kz(wz)
    c_lit, c_sh, c_dark = thin(WOOD_LIT, 0.22), lerp(WOOD_SHADE, OCHRE, 0.12), mixp(SIENNA, PRUSSIAN, 0.60)
    L.poly([gp(wx - r, wz - r * 0.8), gp(wx + r, wz - r * 0.8), gp(wx + r, wz - r * 0.8, hgt), gp(wx - r, wz - r * 0.8, hgt)], c_lit, lerp(c_lit, c_sh, 0.45))
    L.poly([gp(wx + r, wz - r * 0.8), gp(wx + r, wz + r * 0.8), gp(wx + r, wz + r * 0.8, hgt), gp(wx + r, wz - r * 0.8, hgt)], c_sh)
    L.poly([gp(wx - r, wz - r * 0.8, hgt), gp(wx + r, wz - r * 0.8, hgt), gp(wx + r, wz + r * 0.8, hgt), gp(wx - r, wz + r * 0.8, hgt)], c_dark)
    L.line([gp(wx - r, wz - r * 0.8, hgt), gp(wx + r, wz - r * 0.8, hgt)], thin(WOOD_LIT, 0.45), max(0.7, 5 * k), 0.95)             # the curb's rim in the sun
    for px_, pz_ in ((wx - r * 0.85, wz), (wx + r * 0.85, wz)):
        L.line([gp(px_, pz_, hgt), gp(px_, pz_, 232)], c_dark, max(1.0, 11 * k), 1.0)
        L.line([add2(gp(px_, pz_, hgt), (-0.7, 0)), add2(gp(px_, pz_, 232), (-0.7, 0))], c_lit, max(0.5, 3 * k), 0.8)
    apex, lft, rgt = gp(wx, wz, 270), gp(wx - r * 1.6, wz, 224), gp(wx + r * 1.6, wz, 224)
    L.poly([lft, apex, (apex[0], lft[1])], thin(SHINGLE, 0.15), lerp(SHINGLE, SHINGLE_SH, 0.4), g=(apex, lft))                           # the slope that takes the sun
    L.poly([apex, rgt, (apex[0], rgt[1])], lerp(SHINGLE_SH, PRUSSIAN, 0.25), lerp(SHINGLE_SH, PRUSSIAN, 0.45), g=(apex, rgt))
    L.line([add2(lft, (-1, 1.2)), add2(rgt, (1, 1.2))], c_dark, max(0.9, 6 * k), 1.0)                                                    # its eave, dark underneath
    L.line([gp(wx, wz, 226), gp(wx, wz, 118)], lerp(OCHRE, PRUSSIAN, 0.5), 0.7, 0.85)        # the rope
    bq = gp(wx, wz, 104)
    L.poly([(bq[0] - 13 * k, bq[1] - 12 * k), (bq[0] + 13 * k, bq[1] - 12 * k), (bq[0] + 10 * k, bq[1] + 12 * k), (bq[0] - 10 * k, bq[1] + 12 * k)], c_lit, c_sh, g=((bq[0] - 4, bq[1]), (bq[0] + 4, bq[1])))
    keyline(L, [gp(wx - r, wz - r * 0.8), gp(wx + r, wz - r * 0.8), gp(wx + r, wz + r * 0.8)], gp(wx, wz)[1], seed=41)
    return L


# ---------------------------------------------------------------- trees
def pine(L, foot, height, seed, lean=0.0, z=2500.0, spread=1.0, tiers=4):
    """A black pine of the shore in the middle distance (picture measures: `foot`, `height` px): a leaning trunk, a
    few level boughs, each with its flat pad of needles, lit along the top and left, dark beneath."""
    rng = np.random.default_rng(seed)
    x0, y0 = foot
    top = (x0 + lean * height, y0 - height)
    mid = (x0 + lean * height * 0.35 + rng.normal(0, height * 0.03), y0 - height * 0.5)
    trunk = curve([(x0, y0), mid, top], 10)
    bark, bark_l = aired(mixp(SIENNA, PRUSSIAN, 0.55), z), aired(thin(mixp(SIENNA, OCHRE, 0.35), 0.25), z)
    dark, mid_g, lit_g = aired(mixp(VIRIDIAN, PRUSSIAN, 0.50), z), aired(mixp(VIRIDIAN, PRUSSIAN, 0.22), z), aired(thin(mixp(VERONESE, OCHRE, 0.18), 0.12), z)
    L.taper(trunk, bark, max(1.2, height * 0.07), max(0.8, height * 0.03))
    L.taper([(px - height * 0.012, py) for px, py in trunk], bark_l, max(0.6, height * 0.022), max(0.4, height * 0.01), alpha=0.8)
    for i in range(tiers):
        f = 0.42 + 0.56 * (i + 0.5) / tiers
        j = min(int(f * (len(trunk) - 1)), len(trunk) - 1)
        bx, by = trunk[j]
        side = -1 if (i + seed) % 2 else 1
        reach = height * spread * (0.50 - 0.30 * (i / max(tiers - 1, 1))) * rng.uniform(0.85, 1.15)
        tip = (bx + side * reach, by - height * 0.03 + rng.normal(0, height * 0.02))
        L.taper([(bx, by), ((bx + tip[0]) / 2, by + height * 0.015), tip], bark, max(0.7, height * 0.028), max(0.4, height * 0.01))
        cx, cy = bx + side * reach * 0.55, tip[1] - height * 0.035
        rx, ry = reach * 0.62, max(1.5, height * 0.055)
        L.ellipse(cx, cy + ry * 0.35, rx, ry, dark)
        L.ellipse(cx - rx * 0.08, cy, rx * 0.92, ry * 0.85, mid_g, dark, g=((cx, cy - ry), (cx, cy + ry)))
        L.ellipse(cx - rx * 0.16, cy - ry * 0.42, rx * 0.66, ry * 0.42, lit_g, alpha=0.85)
    L.ellipse(top[0], top[1], height * 0.16 * spread, height * 0.06, mid_g, dark)
    L.ellipse(top[0] - height * 0.02, top[1] - height * 0.025, height * 0.10 * spread, height * 0.03, lit_g, alpha=0.85)
    return L


def cherry(L, at=(688.0, 286.0)):
    """The cherry by the shrine path, past its best: its blossom in small pale touches laid wet (the paper left bare
    among them), ragged at the edge, the trunk and boughs showing through, a drift of fallen petals under it.
    -> the box of its blossom (the scene's `cherry` area)."""
    cx_, cy_ = at
    rng = np.random.default_rng(88)
    bark = aired(mixp(SIENNA, PRUSSIAN, 0.45), 3200)
    L.taper([(cx_, cy_), (cx_ - 3, cy_ - 22), (cx_ - 8, cy_ - 36)], bark, 3.0, 1.6)
    L.taper([(cx_ - 3, cy_ - 22), (cx_ + 4, cy_ - 32), (cx_ + 12, cy_ - 44)], bark, 1.8, 0.9)
    L.taper([(cx_ - 6, cy_ - 30), (cx_ - 16, cy_ - 38), (cx_ - 26, cy_ - 42)], bark, 1.4, 0.8)
    L.taper([(cx_ - 7, cy_ - 34), (cx_ - 6, cy_ - 48), (cx_ + 0, cy_ - 60)], bark, 1.2, 0.7)
    pale, deep, mid = thin(PINK, 0.36), thin(PINK_DEEP, 0.04), thin(PINK, 0.08)
    blobs = ((-18, -42, 15), (8, -50, 16), (-4, -34, 11), (18, -38, 10), (-26, -32, 9), (2, -60, 9), (-10, -54, 9), (22, -50, 7))
    for (dx, dy, r, ) in blobs:                                                # the masses, thin
        L.ellipse(cx_ + dx, cy_ + dy, r, r * 0.8, pale, mid, g=((cx_ + dx - r, cy_ + dy - r), (cx_ + dx + r, cy_ + dy + r)), alpha=0.94)
    for (dx, dy, r) in blobs:                                                  # and the touches over them
        for _ in range(int(r * 1.6)):
            a = rng.uniform(0, 2 * math.pi)
            rr = r * math.sqrt(rng.random()) * 1.12
            px_, py_ = cx_ + dx + math.cos(a) * rr, cy_ + dy + math.sin(a) * rr * 0.8
            t = rng.random()
            c = thin(PINK, 0.72) if (t < 0.22 and math.cos(a) < 0.2 and math.sin(a) < 0.3) else (deep if (t > 0.66 or math.sin(a) > 0.5) else mid)
            L.ellipse(px_, py_, rng.uniform(1.6, 3.2), rng.uniform(1.2, 2.4), c, alpha=0.9)
    for (ax, ay, bx, by) in ((-6, -32, -14, -44), (4, -34, 12, -46), (-2, -40, 0, -54)):                        # boughs through the blossom
        L.line([(cx_ + ax, cy_ + ay), (cx_ + bx, cy_ + by)], bark, 0.8, 0.5)
    for _ in range(22):                                                         # fallen petals under it
        L.ellipse(cx_ + rng.normal(2, 10), cy_ + rng.normal(1, 1.6), 1.3, 0.8, thin(PINK, 0.3), alpha=0.6)
    return [int(cx_ - 46), int(cy_ - 72), 84, 76]


def shrine_path(L):
    """The shrine path up the slope beyond the houses: worn steps as a pale thread, a small plain gate of two posts
    and a lintel across their tops (a village shrine's)."""
    steps = [(708, 296), (722, 284), (716, 277), (734, 262), (748, 250), (742, 244), (760, 230), (776, 220), (792, 212)]
    L.line(steps, thin(mixp(NAPLES, COBALT, 0.2), 0.55), 1.6, 0.8)
    for i in range(len(steps) - 1):                                         # the risers: short level strokes across the thread
        (ax, ay), (bx, by) = steps[i], steps[i + 1]
        for f in (0.25, 0.55, 0.85):
            px, py = ax + (bx - ax) * f, ay + (by - ay) * f
            L.line([(px - 1.6, py + 0.6), (px + 1.6, py + 0.6)], aired(mixp(VIRIDIAN, PRUSSIAN, 0.4), 4000), 0.5, 0.45)
    # the gate stands across the path where it shows above Kihei's roof (round twenty's stood lower, behind the roof)
    red = aired(mixp(VERMILION, PRUSSIAN, 0.20), 3000)
    for gx_ in (755.5, 764.5):
        L.line([(gx_, 232), (gx_, 217.5)], red, 1.4, 1.0)
    L.line([(751.5, 217), (768.5, 217)], red, 1.8, 1.0)
    L.line([(753.5, 221), (766.5, 221)], red, 1.0, 0.95)
    return L


def hen_basket(L, X, z, r=21.0, hgt=38.0, seed=5):
    """A fusego in the hen yard: the domed basket of split bamboo that is set over a broody hen or her chicks. Open
    weave: the sand shows through it low down; the sun on its left."""
    rng = np.random.default_rng(seed)
    k = kz(z)
    cx_, cy_ = gp(X, z)
    rx, ry = r * k, hgt * k
    fl = r * k * squash(cy_) * 1.1                                       # its round foot, lying on the ground
    cane, cane_l, cane_d = lerp(OCHRE, PRUSSIAN, 0.30), thin(mixp(OCHRE, NAPLES, 0.45), 0.30), lerp(OCHRE, PRUSSIAN, 0.55)
    dome = [(cx_ + rx * math.cos(t_), cy_ - ry * math.sin(t_)) for t_ in np.linspace(0, math.pi, 15)]
    L.poly(dome + [(cx_ + rx * math.cos(t_), cy_ + fl * math.sin(t_)) for t_ in np.linspace(math.pi, 0, 9)],
           thin(cane_l, 0.2), cane, g=((cx_ - rx, cy_ - ry), (cx_ + rx, cy_)), alpha=0.62)
    for i in range(1, 8):                                                   # the upright canes, bent over to the crown
        t_ = math.pi * i / 8
        px_ = cx_ + rx * math.cos(t_)
        L.line([(px_, cy_ + fl * 0.5 * abs(math.sin(t_))), (cx_ + (px_ - cx_) * 0.92, cy_ - ry * 0.55), (cx_ + (px_ - cx_) * 0.45, cy_ - ry * 0.93), (cx_, cy_ - ry)], cane_l if px_ < cx_ else cane_d, max(0.6, 1.3 * k), 0.9)
    for f in (0.2, 0.45, 0.68, 0.86):                                       # the hoops woven round
        w_ = rx * math.cos(math.asin(min(1.0, f)))
        yy = cy_ - ry * f
        L.line([(cx_ - w_, yy), (cx_ - w_ * 0.5, yy + fl * 0.45 * (1 - f)), (cx_ + w_ * 0.5, yy + fl * 0.45 * (1 - f)), (cx_ + w_, yy)], cane_d, max(0.6, 1.2 * k), 0.75)
    L.line([(cx_ - rx, cy_), (cx_ - rx * 0.5, cy_ + fl * 0.8), (cx_ + rx * 0.5, cy_ + fl * 0.8), (cx_ + rx, cy_)], cane_d, max(0.7, 1.8 * k), 0.9)
    return L


def beach_boat(L, stern, length, beam, side, z_air, heading=None, seed=0):
    """A small boat pulled up on the far beach, bow inland, a few touches but a boat's lines: the sunlit side with its
    sheer rising to the bow, the dark inside over the gunwale, the stem standing up, the bow's planks in shade."""
    sx_, sz_ = stern
    hd = N_IN if heading is None else heading
    port = (-hd[1], hd[0])                                                  # across the boat, away from us
    n = 12
    near, far_, low = [], [], []
    for i in range(n + 1):
        u = i / n
        c = add2((sx_, sz_), hd, length * u)
        hw = beam * (0.55 + 0.45 * math.sin(math.pi * min(1.0, u * 1.15)) ** 0.7) if u < 0.87 else beam * (1.0 - (u - 0.87) / 0.13) ** 0.6 * 0.9 + 4
        sheer = side + 6 * (1 - u) ** 2 + 46 * max(0.0, u - 0.55) ** 1.6 / 0.45 ** 1.6
        near.append(gp(*add2(c, port, -hw), sheer))
        far_.append(gp(*add2(c, port, hw), sheer))
        low.append(gp(*add2(c, port, -hw * 0.9)))
    tip = add2((sx_, sz_), hd, length + 12)
    bow_top = gp(tip[0], tip[1], side + 62)
    hull, hull_s, inside = aired(thin(lerp(OCHRE, PRUSSIAN, 0.16), 0.34), z_air), aired(mixp(SIENNA, PRUSSIAN, 0.46), z_air), aired(mixp(SIENNA, PRUSSIAN, 0.62), z_air)
    L.poly(far_ + near[::-1], inside)
    L.poly(near + low[::-1], hull, aired(lerp(thin(OCHRE, 0.12), mixp(SIENNA, PRUSSIAN, 0.35), 0.45), z_air), g=(near[n // 2], low[n // 2]))
    L.poly([near[-2], bow_top, far_[-2], far_[-1], near[-1]], hull_s)
    L.poly([near[-1], bow_top, (bow_top[0], low[-1][1]), low[-1]], hull_s)
    L.line([gp(tip[0], tip[1], 2), bow_top], hull_s, max(0.9, 9 * kz(tip[1])), 1.0)
    L.line(near, aired(lerp(SIENNA, PRUSSIAN, 0.3), z_air), max(0.6, 4 * kz(sz_)), 0.8)
    keyline(L, low, max(p[1] for p in low), seed=seed, alpha=0.3)
    return L


def far_rack(L, x0, z0, wdt, hgt, seed=0):
    """A rack of nets far along the beach: two uprights, a rail, the net a dark veil with a ragged hem clear of the sand."""
    rng = np.random.default_rng(seed + 400)
    x1, z1 = x0 + wdt * 0.76, z0 + wdt * 0.64
    bamboo = aired(lerp(OCHRE, PRUSSIAN, 0.40), z0)
    P_ = lambda u, h_: gp(x0 + (x1 - x0) * u, z0 + (z1 - z0) * u, h_)
    hem = [P_(u, hgt * (0.20 + 0.12 * rng.random())) for u in np.linspace(0, 1, 7)]
    L.poly(hem + [P_(1, hgt - 3), P_(0, hgt - 3)], aired(mixp(SIENNA, PRUSSIAN, 0.56), z0), aired(mixp(SIENNA, PRUSSIAN, 0.66), z0), alpha=0.86)
    for u in (0.0, 0.5, 1.0):
        L.line([P_(u, 0), P_(u, hgt + 8)], bamboo, max(0.7, 7 * kz(z0)), 0.95)
    L.line([P_(-0.04, hgt), P_(1.04, hgt)], bamboo, max(0.7, 6 * kz(z0)), 0.95)
    return L

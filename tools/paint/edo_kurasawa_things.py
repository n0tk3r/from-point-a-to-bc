"""PAINT-23 (round twenty-three, RECOMPOSE: DEPTH.md): the built things of Nishikurasawa, drawn through the scene's one
camera (edo_kurasawa_view) in the act's watercolour (Yui's way: edo_village_kit.Wet, every face a graded wash, the key
line quieter, broken, none on lit edges), and the floor cut-outs: the palanquin, the noren, Soshichi's trunks, O-Kuni's
grill, Fuji's cap of cloud.

The research is round twenty-one's (edo_kurasawa.py's header): O-Kuni's teahouse at the foot of the pass, its front open
to the road with a bench under the eaves, the grill of turban shells out before her door, a signboard of our own (a shell
painted on it, a column of brush marks that are not characters); the matted room open behind on the bay; the 40th
distance mound with its hackberry planted for the travellers' shade; an open mountain kago on one long pole; a Toyama
peddler's five willow trunks. Nothing here reads as a cross: the palanquin's pole and its rest are never drawn crossing.

LIGHT  the sun behind us and to the left, 39 degrees up (view.SUN3). The teahouse's near end and the faces turned to us
       and the left are lit; its front, along the road, is turned a little from the sun and lies under its own eave in
       shade; the inside is in shade, the bay bright through the open back.
"""

import math

import numpy as np

from brush import F32, Sheet, blur, curve, grid, lerp, mask_poly, noise, over, rgb, tint, warp
from edo_village_kit import (WPAPER, SHADE, SHADE_WARM, Wet, thin, mixp, tintw, shade, glaze, hand, grade_cut, painted, resample,
                             WHITE, NAPLES, CERULEAN, COBALT, ULTRA, PRUSSIAN, OCHRE, SIENNA, VERONESE, VIRIDIAN, LAKE, VERMILION)
from edo_village_far import HORIZON_C
from edo_kurasawa_kit import Fuji, cloud_cap
import edo_kurasawa_view as V
from edo_kurasawa_view import (HZ, FULL, SHAPE, W, H, P, k, G, U, NL, NR, TEA, BENCH, GRILL, KUNI_AT, SIGN, MOUND, HACK, KAGO, TRUNKS,
                               WALL, SUN, SUN3, add, row_of)

# ---------------------------------------------------------------- the paints of the things (Yui's, the same act)
TIMBER = mixp(SIENNA, PRUSSIAN, 0.52)
TIMBER_LIT = thin(mixp(SIENNA, OCHRE, 0.42), 0.22)
TIMBER_DARK = mixp(SIENNA, PRUSSIAN, 0.70)
BOARD_LIT = thin(mixp(SIENNA, OCHRE, 0.50), 0.42)
BOARD_SHADE = thin(mixp(SIENNA, PRUSSIAN, 0.42), 0.22)
EARTHWALL = thin(mixp(OCHRE, NAPLES, 0.45), 0.66)
WALL_SHADE = thin(mixp(COBALT, SIENNA, 0.26), 0.44)
WALL_BOUNCE = thin(mixp(OCHRE, SIENNA, 0.30), 0.52)
THATCH = thin(lerp(tintw(OCHRE, 0.40), NAPLES, 0.10), 0.30)
THATCH_LOW = thin(lerp(tintw(OCHRE, 0.40), SIENNA, 0.24), 0.12)
THATCH_SH = thin(lerp(lerp(OCHRE, PRUSSIAN, 0.5), COBALT, 0.20), 0.20)
THATCH_EDGE = lerp(lerp(THATCH_LOW, SIENNA, 0.25), THATCH_SH, 0.32)              # the straw's cut ends at the eave: pale, a little warm
THATCH_UNDER = mixp(SIENNA, PRUSSIAN, 0.62)
STONE = thin(lerp(PRUSSIAN, OCHRE, 0.16), 0.52)
TATAMI = lerp(thin(mixp(VERONESE, NAPLES, 0.55), 0.30), OCHRE, 0.10)
INSIDE = mixp(SIENNA, PRUSSIAN, 0.74)
INDIGO = lerp(ULTRA, PRUSSIAN, 0.35)
GRASS = thin(mixp(VERONESE, VIRIDIAN, 0.40), 0.12)
GRASS_LIT = thin(mixp(VERONESE, NAPLES, 0.20), 0.18)
GRASS_SH = mixp(VIRIDIAN, PRUSSIAN, 0.30)
BARK = mixp(SIENNA, PRUSSIAN, 0.46)
BARK_LIT = thin(mixp(SIENNA, OCHRE, 0.40), 0.26)
BARK_DARK = mixp(SIENNA, PRUSSIAN, 0.66)


def lit(normal):
    """How much a face with this world normal (X, Y, Z) takes the sun: 0 (shade) to 1."""
    n = np.asarray(normal, dtype=F32)
    n = n / (np.linalg.norm(n) + 1e-6)
    return float(np.clip(np.dot(n, SUN3), 0, 1))


def aired(c, Z, most=0.55):
    """A colour at a lens distance Z (cm): toward the sky's colour at the horizon, more the farther."""
    return lerp(np.asarray(c, dtype=F32), HORIZON_C, float(np.clip((Z - 1600.0) / 9000.0, 0, most)))


def keyline(layer, pts, row=None, lit_=False, seed=0, weight=1.0, color=None, alpha=None):
    """The key line, quieter (DEPTH.md; Yui's kit's keyline at this camera's rows): thinner than the print's, a little
    broken, lost on the lit side of a thing and in the distance (above the row HZ + 22: none)."""
    if lit_ or len(pts) < 2:
        return layer
    r = row if row is not None else max(p[1] for p in pts)
    if r < HZ + 22:
        return layer
    t = float(np.clip((r - HZ) / (FULL - HZ), 0, 1))
    w = (0.35 + 0.45 * t) * weight
    a = alpha if alpha is not None else 0.24 + 0.34 * t
    col = PRUSSIAN if color is None else color
    rng = np.random.default_rng(int(seed * 7919 + pts[0][0] * 13 + pts[0][1] * 31) & 0x7FFFFFFF)
    q = resample(pts, 3.0)
    i = 0
    while i < len(q) - 1:
        n = int(rng.uniform(4, 13))
        layer.line(q[i:i + n + 1], col, w * rng.uniform(0.8, 1.15), a * rng.uniform(0.55, 1.0))
        i += n + (int(rng.uniform(1, 3)) if rng.random() < 0.55 else 0)
    return layer


def squash(row):
    """How flat a circle lying on the ground looks at a picture row."""
    return max(float(row) - HZ, 1.0) / V.FOCAL


# ================================================================ O-Kuni's teahouse
EAVE_POSTS = ()                                            # (the eave is carried on its rafters: no posts out at its edge)
POST_W = -96.0                                             # where they stand (back from the front: out toward the road)


def teahouse(L, info, seed=0):
    """O-Kuni's teahouse, far parts first. -> its outline pieces in info (for the layout)."""
    T = TEA
    rng = np.random.default_rng(seed + 5)
    tp = T.pt
    e, th = T.eave, T.thick
    d0, d1 = T.door
    r = T.roof_pts()
    A, B, C, D_, R0, R1 = (r[k_] for k_ in ("A", "B", "C", "D", "R0", "R1"))
    top = r["top"]
    zc = T.xz(T.L / 2, T.D / 2)[1]
    # ---------------- the inside, seen through the open front: the bay bright through the back, the matted room, the dark
    back_lo, back_hi = T.floor + 2, 196.0
    L.poly([tp(0, T.D, back_lo), tp(d0, T.D, back_lo), tp(d0, T.D, back_hi), tp(0, T.D, back_hi)], thin(mixp(CERULEAN, COBALT, 0.30), 0.30),
           thin(mixp(CERULEAN, COBALT, 0.50), 0.10), g=(tp(0, T.D, back_hi), tp(0, T.D, back_lo)))
    L.poly([tp(0, T.D, back_hi - 22), tp(d0, T.D, back_hi - 22), tp(d0, T.D, back_hi - 30), tp(0, T.D, back_hi - 30)], thin(mixp(COBALT, VIRIDIAN, 0.30), 0.45), alpha=0.8)  # the far shore through it
    for u in (0.0, 150.0, 300.0, d0):                                                   # the back posts, dark against the light
        L.line([tp(u, T.D, T.floor), tp(u, T.D, back_hi + 4)], TIMBER_DARK, max(1.0, 10 * k(T.xz(u, T.D)[1])), 1.0)
    L.poly([tp(0, T.D, back_lo - 2), tp(d0, T.D, back_lo - 2), tp(d0, T.D, back_lo + 7), tp(0, T.D, back_lo + 7)], TIMBER, alpha=0.95)    # the back sill
    L.poly([tp(0, T.D, back_hi), tp(d0, T.D, back_hi), tp(d0, 0, e - 40), tp(0, 0, e - 40)], INSIDE, mixp(SIENNA, PRUSSIAN, 0.82),
           g=(tp(0, T.D, back_hi), tp(0, 0, e - 40)))                                      # the room under the roof: dark, darkest high up
    # the mats: straw, a little green, their dark cloth borders running back and across, the light from the open back on them
    fl = T.floor
    L.poly([tp(0, 0, fl), tp(d0, 0, fl), tp(d0, T.D, fl), tp(0, T.D, fl)], lerp(TATAMI, INSIDE, 0.35), lerp(TATAMI, WPAPER, 0.10),
           g=(tp(0, 0, fl), tp(0, T.D, fl)))
    for u in np.arange(90.0, d0, 90.0):
        L.line([tp(u, 4, fl + 0.5), tp(u, T.D - 4, fl + 0.5)], lerp(TATAMI, PRUSSIAN, 0.45), max(0.6, 3.2 * k(T.xz(u, 100)[1])), 0.75)
    for w in (180.0, 360.0):
        L.line([tp(4, w, fl + 0.5), tp(d0 - 4, w, fl + 0.5)], lerp(TATAMI, PRUSSIAN, 0.45), max(0.6, 3.2 * k(T.xz(200, w)[1])), 0.75)
    # a tea tray left on the mats, and a cushion
    q = tp(220, 260, fl + 1)
    L.ellipse(q[0], q[1], 7.0, 7.0 * squash(q[1]) * 1.4, thin(mixp(SIENNA, LAKE, 0.4), 0.15), alpha=0.9)
    q = tp(120, 330, fl + 1)
    L.poly([(q[0] - 7, q[1]), (q[0] + 6, q[1] - 1), (q[0] + 8, q[1] + 3), (q[0] - 5, q[1] + 4)], thin(INDIGO, 0.25), alpha=0.85)
    # the earth floor behind the door: dark, the stove's mouth faintly warm at the back
    L.poly([tp(d0, 0, 0), tp(d1, 0, 0), tp(d1, T.D, 0), tp(d0, T.D, 0)], mixp(SIENNA, PRUSSIAN, 0.66), mixp(OCHRE, PRUSSIAN, 0.55),
           g=(tp(d0, T.D, 0), tp(d0, 0, 0)))
    L.poly([tp(d0, T.D, 0), tp(d1, T.D, 0), tp(d1, T.D, 200), tp(d0, T.D, 200)], mixp(SIENNA, PRUSSIAN, 0.78))
    L.poly([tp(d0 + 30, T.D - 30, 0), tp(d0 + 100, T.D - 30, 0), tp(d0 + 100, T.D - 30, 66), tp(d0 + 30, T.D - 30, 66)], mixp(PRUSSIAN, SIENNA, 0.35))
    q = tp(d0 + 65, T.D - 30, 26)
    L.ellipse(q[0], q[1], 2.6, 1.8, lerp(VERMILION, SIENNA, 0.45), alpha=0.85)
    # ---------------- the front: the far bay's wall (past the door) with a barred window, the wall strip above the openings
    L.poly([tp(d1, 0, 0), tp(T.L, 0, 0), tp(T.L, 0, e), tp(d1, 0, e)], WALL_SHADE, WALL_BOUNCE, g=(tp(d1, 0, e), tp(d1, 0, 0)))
    L.poly([tp(d1, 0, 0), tp(T.L, 0, 0), tp(T.L, 0, 88), tp(d1, 0, 88)], BOARD_SHADE, alpha=0.9)
    wq = [tp(d1 + 18, 0, 108), tp(T.L - 14, 0, 108), tp(T.L - 14, 0, 168), tp(d1 + 18, 0, 168)]
    L.poly(wq, mixp(SIENNA, PRUSSIAN, 0.70))
    for u in np.linspace(d1 + 18, T.L - 14, 6)[1:-1]:
        L.line([tp(u, 0, 108), tp(u, 0, 168)], lerp(TIMBER_LIT, WALL_SHADE, 0.5), max(0.6, 2.6 * k(T.xz(u, 0)[1])), 0.9)
    lin = 196.0
    L.poly([tp(0, 0, lin), tp(T.L, 0, lin), tp(T.L, 0, e), tp(0, 0, e)], lerp(WALL_SHADE, mixp(SIENNA, PRUSSIAN, 0.62), 0.72),
           lerp(WALL_SHADE, mixp(SIENNA, PRUSSIAN, 0.5), 0.45), g=(tp(0, 0, e), tp(0, 0, lin)))    # the wall strip under the eave, in its shade
    for u in np.arange(30.0, T.L, 40.0):                                                  # its boards, faint
        L.line([tp(u, 0, lin + 6), tp(u, 0, e - 2)], mixp(SIENNA, PRUSSIAN, 0.70), 0.6, 0.25)
    L.poly([tp(0, 0, lin - 9), tp(T.L, 0, lin - 9), tp(T.L, 0, lin + 5), tp(0, 0, lin + 5)], TIMBER, lerp(TIMBER, TIMBER_LIT, 0.4))        # the lintel beam
    L.poly([tp(0, 0, fl - 12), tp(d0, 0, fl - 12), tp(d0, 0, fl + 3), tp(0, 0, fl + 3)], lerp(TIMBER_LIT, TIMBER, 0.35))                   # the sill under the mats
    L.poly([tp(0, 0, 0), tp(d0, 0, 0), tp(d0, 0, fl - 12), tp(0, 0, fl - 12)], mixp(SIENNA, PRUSSIAN, 0.62))                                # the dark under the floor
    for u in T.posts:
        zz = T.xz(u, 0)[1]
        wd = max(1.2, 12 * k(zz))
        L.line([tp(u, 0, 0), tp(u, 0, e)], TIMBER, wd, 1.0)
        L.line([add(tp(u, 0, 0), (-wd * 0.32, 0)), add(tp(u, 0, e), (-wd * 0.32, 0))], TIMBER_LIT, max(0.6, wd * 0.30), 0.85)
    # the reed blind rolled up under the eave over the matted part, tied in two places
    for (ua, ub) in ((8.0, d0 - 8),):
        a_, b_ = tp(ua, -10, lin + 30), tp(ub, -10, lin + 30)
        L.line([a_, b_], lerp(mixp(OCHRE, SIENNA, 0.35), PRUSSIAN, 0.30), max(1.6, 9 * k(T.xz(ua, 0)[1])), 0.95)
        L.line([add(a_, (0, 2.0)), add(b_, (0, 1.8))], mixp(SIENNA, PRUSSIAN, 0.55), 0.8, 0.6)
        for f in (0.28, 0.72):
            q = tp(ua + (ub - ua) * f, -12, lin + 30)
            L.line([(q[0], q[1] - 4), (q[0], q[1] + 4)], TIMBER_DARK, 1.0, 0.8)
    # ---------------- the near end (it faces us and the left: in the sun); mostly beyond the frame
    L.poly([tp(0, 0, 0), tp(0, T.D, 0), tp(0, T.D, e), tp(0, 0, e)], EARTHWALL, lerp(EARTHWALL, BOARD_LIT, 0.4), g=(tp(0, 0, e), tp(0, 0, 0)))
    L.poly([tp(0, 0, 0), tp(0, T.D, 0), tp(0, T.D, 90), tp(0, 0, 90)], BOARD_LIT, alpha=0.95)
    # ---------------- the eave's underside (we stand lower than the eave: we see under it), then the roof
    q_ = lambda uw, y: tp(uw[0], uw[1], y)
    soffit = [q_(A, e), q_(B, e), tp(T.L, 0, e + 24), tp(0, 0, e + 24)]
    L.poly(soffit, THATCH_UNDER, lerp(THATCH_UNDER, INSIDE, 0.4), g=(q_(A, e), tp(0, 0, e + 24)))
    for u in np.arange(40.0, T.L, 60.0):                                                  # the rafters' ends under the thatch
        L.line([tp(u, -T.over + 6, e + 2), tp(u, 0, e + 22)], TIMBER_DARK, max(0.6, 3.0 * k(T.xz(u, 0)[1])), 0.55)
    # the roof's faces: the near hip (it faces us and the left: lit), the front slope (half lit), and the far hip's edge
    n_front = (NR[0], math.cos(math.radians(T.pitch)) / max(math.sin(math.radians(T.pitch)), 1e-3) * 0 + 1.0, NR[1])
    lf = lit((NR[0] * math.sin(math.radians(T.pitch)), math.cos(math.radians(T.pitch)), NR[1] * math.sin(math.radians(T.pitch))))
    lh = lit((-U[0] * math.sin(math.radians(T.pitch)), math.cos(math.radians(T.pitch)), -U[1] * math.sin(math.radians(T.pitch))))
    info["roof_light"] = (round(lf, 2), round(lh, 2))
    et = e + th
    front_slope = [q_(A, et), q_(B, et), q_(R1, top), q_(R0, top)]
    near_hip = [q_(D_, et), q_(A, et), q_(R0, top)]
    OLD = lerp(THATCH_SH, SIENNA, 0.10)                                                     # straw two winters old: grey-brown, as Yui's roofs
    L.poly(front_slope, lerp(THATCH, OLD, 0.46), lerp(THATCH_LOW, OLD, 0.66), g=(q_(R0, top), q_(A, et)))
    L.poly(near_hip, lerp(THATCH, OLD, 0.16), lerp(THATCH_LOW, OLD, 0.42), g=(q_(R0, top), q_(A, et)))
    # the cut edge: the thatch's thickness along the front and down the near hip's foot (the straw's cut ends: pale, layered)
    L.poly([q_(A, e), q_(B, e), q_(B, et), q_(A, et)], lerp(THATCH_EDGE, PRUSSIAN, 0.10), lerp(THATCH_EDGE, NAPLES, 0.10), g=(q_(A, e), q_(A, et)))
    L.poly([q_(D_, e), q_(A, e), q_(A, et), q_(D_, et)], lerp(THATCH_EDGE, NAPLES, 0.30), THATCH_EDGE, g=(q_(A, et), q_(A, e)))
    for frac in np.linspace(0.08, 0.92, 5):                                                # layers in the cut edge
        a_ = add(q_(A, e + th * frac), (0, 0))
        b_ = q_(B, e + th * frac)
        L.line([a_, b_], lerp(THATCH_EDGE, PRUSSIAN, 0.30), 0.6, 0.35)
    # the straw running down the slopes: dry strokes; moss and weathering in the low parts
    def hp(uw0, uw1, apex, s_, v_):
        bu, bw = uw0[0] + (uw1[0] - uw0[0]) * s_, uw0[1] + (uw1[1] - uw0[1]) * s_
        return tp(bu + (apex[0] - bu) * v_, bw + (apex[1] - bw) * v_, et + (top - et) * v_)

    def fp(s_, v_):
        bu = A[0] + (B[0] - A[0]) * s_
        ru = R0[0] + (R1[0] - R0[0]) * s_
        return tp(bu + (ru - bu) * v_, A[1] + (R0[1] - A[1]) * v_, et + (top - et) * v_)
    for i in range(26):                                                                     # the rain's long darker runs down the old straw
        s_ = rng.uniform(0.02, 0.98)
        v0 = rng.uniform(0.25, 0.8)
        L.line([fp(s_, v0), fp(s_ + rng.normal(0, 0.003), 0.02)], lerp(OLD, PRUSSIAN, 0.22), rng.uniform(1.5, 4.0), 0.10 + 0.10 * rng.random())
    for i in range(240):                                                                    # the straw: dry strokes down the fall line
        s_ = rng.random()
        v0 = rng.uniform(0.0, 0.9)
        dark = rng.random() < 0.6
        L.line([fp(s_, min(0.98, v0 + rng.uniform(0.05, 0.14))), fp(s_ + rng.normal(0, 0.004), v0)],
               lerp(OLD, PRUSSIAN, 0.28) if dark else lerp(THATCH, NAPLES, 0.15), rng.uniform(0.6, 1.1), (0.22 if dark else 0.30) + 0.18 * rng.random())
    for i in range(120):
        s_ = rng.random()
        v0 = rng.uniform(0.0, 0.85)
        dark = rng.random() < 0.45
        L.line([hp(D_, A, R0, s_, min(0.98, v0 + rng.uniform(0.06, 0.16))), hp(D_, A, R0, s_ + rng.normal(0, 0.004), v0)],
               lerp(THATCH_LOW, SIENNA, 0.35) if dark else lerp(THATCH, NAPLES, 0.25), rng.uniform(0.6, 1.1), 0.20 + 0.16 * rng.random())
    # the courses the thatch was laid in: faint steps across the slopes, level with the eave (a darker line under each,
    # its lit lip over it), broken where the straw has settled
    for v_ in np.linspace(0.12, 0.78, 6):
        for s0 in np.arange(0.0, 1.0, 0.11):
            if rng.random() < 0.35:
                continue
            s1 = min(1.0, s0 + rng.uniform(0.06, 0.12))
            vv = v_ + rng.normal(0, 0.008)
            L.line([fp(s0, vv - 0.010), fp(s1, vv - 0.010 + rng.normal(0, 0.004))], lerp(OLD, PRUSSIAN, 0.26), rng.uniform(3.0, 4.5), 0.13 + 0.06 * rng.random())
            L.line([fp(s0, vv + 0.010), fp(s1, vv + 0.010)], lerp(THATCH, NAPLES, 0.25), 1.2, 0.22)
        for s0 in np.arange(0.0, 1.0, 0.12):
            if rng.random() < 0.25:
                continue
            s1 = min(1.0, s0 + rng.uniform(0.07, 0.12))
            L.line([hp(D_, A, R0, s0, v_), hp(D_, A, R0, s1, v_)], lerp(THATCH_LOW, SIENNA, 0.40), 0.9, 0.18)
    # moss and the damp's grey in the low part of the slope over the eave: soft blotches that follow no pattern
    slope_m = mask_poly(SHAPE, front_slope)
    xg, yg = grid(SHAPE)
    (ax_, ay_), (bx_, by_) = q_(A, et), q_(B, et)
    eave_row = ay_ + (by_ - ay_) * np.clip((xg - ax_) / max(bx_ - ax_, 1.0), 0, 1)
    low = np.clip(1.0 - (eave_row - yg) / 70.0, 0, 1) ** 1.5
    blot = np.clip((noise(SHAPE, (34.0, 12.0), seed + 41, 4) - 0.50) * 3.0, 0, 1)
    L.add(np.ones(SHAPE + (3,), F32) * lerp(mixp(VIRIDIAN, OCHRE, 0.50), THATCH_SH, 0.45)[None, None, :], (slope_m * low * blot * 0.38).astype(F32))
    L.add(np.ones(SHAPE + (3,), F32) * lerp(THATCH_SH, PRUSSIAN, 0.18)[None, None, :], (slope_m * low * np.clip(0.42 - blot, 0, 1) * 0.30).astype(F32))
    # the ridge: a roll of bound straw along the top, with cross pieces; the bare paper along the near hip's lit edge
    kr = k(T.xz((R0[0] + R1[0]) / 2, R0[1])[1])
    L.line([add(q_(R0, top), (-3, 1)), add(q_(R1, top), (2, 1))], lerp(THATCH_LOW, SIENNA, 0.45), max(2.0, 26 * kr), 0.95)
    L.line([add(q_(R0, top), (-3, -2)), add(q_(R1, top), (2, -2))], lerp(THATCH, NAPLES, 0.25), max(1.0, 8 * kr), 0.8)
    for f in np.linspace(0.05, 0.95, 5):
        c_ = lerp(np.asarray(q_(R0, top)), np.asarray(q_(R1, top)), f)
        L.line([(c_[0] - 3, c_[1] - 5), (c_[0] + 1, c_[1] + 6)], mixp(SIENNA, PRUSSIAN, 0.55), max(1.0, 7 * kr), 0.9)
    L.line([q_(A, et), q_(R0, top)], WPAPER, 1.2, 0.7)
    L.line([add(q_(D_, et), (0, -0.6)), add(q_(A, et), (0, -0.6))], WPAPER, 0.9, 0.45)
    # ---------------- the eave's posts, slim, on flat stones; their shadows are the ground's
    for u in EAVE_POSTS:
        zz = T.xz(u, POST_W)[1]
        wd = max(1.0, 10 * k(zz))
        foot_, head_ = tp(u, POST_W, 0), tp(u, POST_W, e - 2)
        L.line([foot_, head_], TIMBER, wd, 1.0)
        L.line([add(foot_, (-wd * 0.3, 0)), add(head_, (-wd * 0.3, 0))], TIMBER_LIT, max(0.5, wd * 0.32), 0.9)
        L.ellipse(foot_[0], foot_[1], wd * 1.5, wd * 1.5 * squash(foot_[1]) * 2.2, STONE, lerp(STONE, PRUSSIAN, 0.3))
    # ---------------- the key line: only on the shade side and under things; the lit edges are left to the paper
    row0 = tp(T.L, 0)[1]
    keyline(L, [q_(A, e), q_(B, e)], row0 + 40, seed=seed + 1, weight=1.1)
    keyline(L, [q_(B, e), q_(B, et), q_(R1, top)], row0, seed=seed + 2, weight=0.9, alpha=0.32)
    keyline(L, [q_(R0, top), q_(R1, top)], row0, seed=seed + 3, alpha=0.25)
    keyline(L, [tp(d1, 0, 0), tp(T.L, 0, 0), tp(T.L, 0, e)], row0, seed=seed + 4)
    keyline(L, [tp(0, 0, fl - 12), tp(d0, 0, fl - 12)], row0 + 30, seed=seed + 5, alpha=0.3)
    info["tea_roof"] = [q_(D_, et), q_(R0, top), q_(R1, top), q_(B, et), q_(B, e), q_(A, e)]
    info["tea_front"] = [tp(0, 0, 0), tp(T.L, 0, 0), tp(T.L, 0, e), tp(0, 0, e)]
    info["tea_eave"] = [q_(A, e), q_(B, e)]
    return L


def bench(L, seed=0):
    """The bench under the eave: a long low plank on four legs, a tea tray on it (a pot and two cups)."""
    T = TEA
    B = BENCH
    tp = T.pt
    u0, u1, w0, w1, h = B["u0"], B["u1"], B["w0"], B["w1"], B["h"]
    zz = T.xz((u0 + u1) / 2, w0)[1]
    kk = k(zz)
    for uu in (u0 + 14, u1 - 14):
        for ww in (w0 + 6, w1 - 6):
            L.line([tp(uu, ww, 0), tp(uu, ww, h - 5)], TIMBER_DARK, max(1.0, 6 * kk), 1.0)
    L.poly([tp(u0, w0, h - 6), tp(u1, w0, h - 6), tp(u1, w0, h), tp(u0, w0, h)], TIMBER, lerp(TIMBER, TIMBER_LIT, 0.3))          # its edge, toward the road
    L.poly([tp(u0, w0, h), tp(u1, w0, h), tp(u1, w1, h), tp(u0, w1, h)], lerp(TIMBER_LIT, BOARD_LIT, 0.4), lerp(BOARD_SHADE, TIMBER, 0.2),
           g=(tp(u0, w0, h), tp(u1, w0, h)))
    L.line([tp(u0, w0, h), tp(u1, w0, h)], lerp(TIMBER_LIT, WPAPER, 0.3), 0.8, 0.6)
    # the tray, the pot, the cups
    tu, tw = u0 + 70, (w0 + w1) / 2
    L.poly([tp(tu - 20, tw - 13, h + 1), tp(tu + 20, tw - 13, h + 1), tp(tu + 20, tw + 13, h + 1), tp(tu - 20, tw + 13, h + 1)], mixp(SIENNA, PRUSSIAN, 0.40))
    p_ = tp(tu - 6, tw, h + 10)
    L.ellipse(p_[0], p_[1], 4.6 * kk * 10 / 10, 4.0 * kk * 10 / 10, thin(mixp(PRUSSIAN, OCHRE, 0.25), 0.25), mixp(PRUSSIAN, OCHRE, 0.3),
              g=((p_[0] - 3, p_[1]), (p_[0] + 3, p_[1])))
    for du in (7.0, 15.0):
        q = tp(tu + du, tw, h + 4)
        L.ellipse(q[0], q[1], 2.2 * kk * 10 / 10 + 0.6, 1.8 * kk * 10 / 10 + 0.4, thin(CERULEAN, 0.66))
    keyline(L, [tp(u0, w0, h - 6), tp(u1, w0, h - 6)], tp(u0, w0)[1], seed=seed + 9, alpha=0.35)
    return [tp(u0, w0, 0), tp(u1, w0, 0), tp(u1, w1, h), tp(u0, w1, h)]


def signboard(L, seed=0):
    """The signboard at the teahouse's far corner, toward the road: a pale board on a post under a little roof, a turban
    shell painted on it (our own sign: no shop's name) and a column of brush marks under it (a pattern, never characters
    a reader could read). Its face turned toward the road behind us, so the people coming from Yui see it."""
    T = TEA
    S_ = SIGN
    u, w, hgt, wid = S_["u"], S_["w"], S_["h"], S_["wid"]
    X, Z = T.xz(u, w)
    kk = k(Z)
    face = (-U[0], -U[1])                                    # the board faces back along the road, toward Yui
    side = (U[1], -U[0])                                     # its width runs across the road (right-toward-us)
    pt = lambda a, y: P(X + side[0] * a, Z + side[1] * a, y)
    L.line([pt(0, 0), pt(0, hgt + 6)], TIMBER_DARK, max(1.2, 8 * kk), 1.0)
    L.line([add(pt(0, 0), (-1, 0)), add(pt(0, hgt), (-1, 0))], TIMBER_LIT, max(0.6, 2.4 * kk), 0.8)
    board = [pt(-wid / 2, 42), pt(wid / 2, 42), pt(wid / 2, hgt - 6), pt(-wid / 2, hgt - 6)]
    L.poly(board, thin(mixp(OCHRE, NAPLES, 0.35), 0.45), thin(mixp(OCHRE, NAPLES, 0.35), 0.25), g=(board[3], board[0]))
    L.poly([pt(-wid / 2 - 7, hgt - 6), pt(wid / 2 + 7, hgt - 6), pt(wid / 2 + 3, hgt + 7), pt(-wid / 2 - 3, hgt + 7)], TIMBER_DARK)
    c = pt(0, hgt - 32)
    s = 10 * kk
    dark, pale = mixp(VIRIDIAN, PRUSSIAN, 0.45), thin(mixp(OCHRE, SIENNA, 0.2), 0.3)
    # the turban shell on its side: its round body to the left with the pale mouth in it, its spire stepping to a point at
    # the right, knobs along its back
    L.ellipse(c[0] - s * 0.25, c[1], s * 0.62, s * 0.56, dark)
    L.poly([(c[0] - s * 0.1, c[1] - s * 0.50), (c[0] + s * 0.55, c[1] - s * 0.28), (c[0] + s * 1.0, c[1] - s * 0.02), (c[0] + s * 0.55, c[1] + s * 0.22),
            (c[0] - s * 0.1, c[1] + s * 0.46)], dark)
    for dx_ in (-0.55, -0.15, 0.25):
        L.poly([(c[0] + dx_ * s - s * 0.12, c[1] - s * 0.42), (c[0] + dx_ * s, c[1] - s * 0.80), (c[0] + dx_ * s + s * 0.12, c[1] - s * 0.38)], dark)
    L.ellipse(c[0] - s * 0.45, c[1] + s * 0.05, s * 0.26, s * 0.30, pale)
    # a column of brush marks under it (a pattern, never characters a reader could read, and no stroke ever crosses
    # another): a stroke with a hook at its foot, two strokes parting, a stroke that turns down at its end
    rng = np.random.default_rng(15)
    yy = hgt - 58
    wd_ = max(1.0, 3.4 * kk)
    kind = 0
    while yy > 54:
        ln = rng.uniform(8, 12)
        if kind == 0:
            L.line([pt(-1.5, yy), pt(-2.0, yy - ln * 0.8), pt(4.0, yy - ln)], PRUSSIAN, wd_, 0.9)
        elif kind == 1:
            L.line([pt(-1.5, yy), pt(-5.5, yy - ln)], PRUSSIAN, wd_, 0.9)
            L.line([pt(2.0, yy - ln * 0.2), pt(5.5, yy - ln)], PRUSSIAN, wd_, 0.9)
        else:
            L.line([pt(-5.0, yy), pt(4.0, yy), pt(0.5, yy - ln)], PRUSSIAN, wd_, 0.9)
        kind = (kind + 1) % 3
        yy -= ln + rng.uniform(5, 8)
    keyline(L, [board[1], board[2]], pt(0, 0)[1], seed=seed + 11)
    return [pt(-wid / 2 - 6, 0), pt(wid / 2 + 6, hgt + 8)]


def wall(L, seed=0):
    """The low wall over the shore along the ledge's seaward edge: set stones, their tops in the sun, a little grass."""
    rng = np.random.default_rng(seed)
    top = [P(X, Z, 52) for X, Z in V.WALL]
    foot = [P(X, Z) for X, Z in V.WALL]
    L.poly(top + foot[::-1], thin(lerp(PRUSSIAN, OCHRE, 0.20), 0.46), thin(lerp(PRUSSIAN, OCHRE, 0.20), 0.30), g=(top[0], foot[0]))
    L.line(top, thin(lerp(PRUSSIAN, OCHRE, 0.14), 0.66), 1.4, 0.9)
    for i in range(len(V.WALL) - 1):                                                        # the joints between stones
        (x0, z0), (x1, z1) = V.WALL[i], V.WALL[i + 1]
        for f in np.linspace(0, 1, 7)[1:]:
            X_, Z_ = x0 + (x1 - x0) * f, z0 + (z1 - z0) * f
            a_, b_ = P(X_, Z_, 50), P(X_ + rng.normal(0, 8), Z_, 4)
            L.line([a_, b_], thin(mixp(PRUSSIAN, SIENNA, 0.4), 0.35), 0.6, 0.45)
    return top


# ================================================================ the mound and the hackberry's trunk (the crown is the near plane's)
FORK_Y = 470.0                                             # how high the hackberry forks (cm above the road)


def mound(L, seed=0):
    """The 40th distance mound: a grassed mound, its profile a little uneven (two centuries of roots under it), the
    side turned to us and the left lit, the far right in shade; its grass drawn in short strokes that shrink up its
    slope; a few stones at its foot where the bearers sit. -> its outline."""
    m = MOUND
    mx, mz, r, h = m["X"], m["Z"], m["r"], m["h"]
    rng = np.random.default_rng(seed)
    bump = lambda u: 1 + 0.06 * math.sin(u * 7.0 + 1.3) + 0.04 * math.sin(u * 13.0)
    prof = []
    for a in np.linspace(0, math.pi, 41):
        u = math.cos(a)
        prof.append(P(mx + r * u, mz, h * (1 - abs(u) ** 2.0) ** 0.62 * bump(u)))
    shape = prof + [P(mx + r * math.cos(a), mz - r * 0.85 * math.sin(a)) for a in np.linspace(math.pi, 2 * math.pi, 21)][1:]
    L.poly(shape, GRASS, lerp(GRASS, GRASS_SH, 0.40), g=(P(mx - r, mz, h), P(mx + r, mz)))
    lit_side = [p for p in shape if p[0] < P(mx + r * 0.10, mz)[0]]
    if len(lit_side) > 2:
        L.poly(lit_side, GRASS_LIT, lerp(GRASS_LIT, GRASS, 0.55), g=(P(mx - r, mz, h), P(mx, mz)), alpha=0.80)
    kk = k(mz)
    for i in range(9):                                                                      # broad wet passages: the grass is not one green
        u = rng.uniform(-0.8, 0.8)
        hh = h * (1 - abs(u) ** 2.0) ** 0.62 * bump(u)
        q = P(mx + r * u, mz - r * 0.3, hh * rng.uniform(0.15, 0.7))
        tone = lerp(GRASS_SH, PRUSSIAN, 0.15) if (u > 0.1 or rng.random() < 0.4) else lerp(GRASS_LIT, OCHRE, 0.2)
        L.ellipse(q[0], q[1], rng.uniform(14, 30), rng.uniform(5, 10), tone, alpha=0.22)
    for i in range(720):                                                                    # its grass, in strokes, leaning a little with the wind
        u = rng.uniform(-0.97, 0.97)
        hh = h * (1 - abs(u) ** 2.0) ** 0.62 * bump(u)
        y_ = hh * rng.uniform(0.0, 0.96)
        q = P(mx + r * u, mz - r * 0.6 * rng.random() * (1 - y_ / h), y_)
        tone = GRASS_SH if (u > 0.3 or rng.random() < 0.18) else (GRASS_LIT if (u < -0.1 and rng.random() < 0.55) else GRASS)
        an = rng.uniform(-0.5, 0.5) + 0.2
        ln = rng.uniform(6, 14) * kk * (1.0 - 0.4 * y_ / h)
        L.line([q, (q[0] + math.sin(an) * ln, q[1] - math.cos(an) * ln)], lerp(tone, PRUSSIAN, 0.16), 0.8, 0.62)
    for (px_, py_) in prof[2:-2:2]:                                                         # tufts along its outline against the sea and the hill
        for j in range(int(rng.integers(2, 5))):
            an = rng.uniform(-0.6, 0.6) + 0.15
            ln = rng.uniform(3.0, 7.0)
            L.line([(px_ + rng.normal(0, 1.5), py_ + 1.5), (px_ + math.sin(an) * ln, py_ - math.cos(an) * ln)],
                   lerp(GRASS_SH if px_ > P(mx, mz)[0] else GRASS, PRUSSIAN, 0.2), 0.8, 0.8)
    for (u, s_) in ((-0.95, 1.0), (-0.75, 0.7), (-0.35, 0.8), (0.5, 0.6)):                    # stones round its foot
        q = P(mx + r * u, mz - r * 0.75 * math.sqrt(max(0.0, 1 - u * u)) - 10, 0)
        rx_ = 22 * kk * s_
        L.ellipse(q[0] + rx_ * 0.4, q[1] + 1, rx_ * 1.1, rx_ * 0.35, lerp(GRASS_SH, PRUSSIAN, 0.3), alpha=0.5)
        L.ellipse(q[0], q[1] - rx_ * 0.3, rx_, rx_ * 0.55, STONE, lerp(STONE, PRUSSIAN, 0.35), g=((q[0] - rx_, q[1] - rx_), (q[0] + rx_, q[1])))
    keyline(L, shape[:41], P(mx, mz)[1], seed=seed + 3, alpha=0.18)
    return shape


def hackberry_trunk(L, seed=0):
    """The hackberry's trunk on the mound: short and thick, a little leaning, its roots gripping the mound's top,
    forking low into three limbs (the crown and the bough it sends toward us are the near plane). Smooth grey bark,
    lit along its left. -> the trunk's outline, and the fork."""
    m = MOUND
    mx, mz, h = m["X"] + 30.0, m["Z"] + 10.0, m["h"]
    tr = HACK["r"]
    rng = np.random.default_rng(seed)
    ys = np.linspace(h - 40, FORK_Y + 30, 8)
    pts = [(mx + 14 * (y_ - ys[0]) / (ys[-1] - ys[0]) + 4 * math.sin(i * 1.1), y_) for i, y_ in enumerate(ys)]
    wid = lambda i: tr * (1.25 - 0.30 * i / 7) * (1.0 + (0.22 if i == 0 else 0))
    left = [P(x_ - wid(i), mz, y_) for i, (x_, y_) in enumerate(pts)]
    right = [P(x_ + wid(i), mz, y_) for i, (x_, y_) in enumerate(pts)]
    for (dx_, ln) in ((-1, 140), (-0.45, 90), (0.55, 100), (1, 150)):                       # roots spreading over the mound's top
        L.taper([P(mx + dx_ * tr * 0.8, mz, h - 18), P(mx + dx_ * (tr + ln * 0.6), mz - 30, h - 34), P(mx + dx_ * (tr + ln), mz - 40, h - 62)],
                BARK, 26 * k(mz), 6 * k(mz))
    L.poly(left + right[::-1], lerp(BARK, STONE, 0.18), BARK_DARK, g=(left[0], right[0]))
    inner = [((l[0] * 0.58 + r_[0] * 0.42), l[1]) for l, r_ in zip(left, right)]
    L.poly(left + inner[::-1], BARK_LIT, lerp(BARK_LIT, BARK, 0.5), g=(left[0], inner[0]), alpha=0.9)
    for i in range(48):                                                                     # the bark: smooth, grey, ringed with fine lines and a few knobs
        f = rng.uniform(0.08, 0.92)
        j = rng.uniform(0, len(left) - 1.01)
        i0 = int(j)
        g_ = j - i0
        lo = lerp(np.asarray(left[i0]), np.asarray(left[i0 + 1]), g_)
        ro = lerp(np.asarray(right[i0]), np.asarray(right[i0 + 1]), g_)
        a_ = lerp(lo, ro, f)
        if rng.random() < 0.7:
            L.line([tuple(lerp(lo, ro, max(0.0, f - 0.12))), tuple(lerp(lo, ro, min(1.0, f + 0.12)))], BARK_DARK, 0.7, 0.35)
        else:
            L.ellipse(a_[0], a_[1], 2.0, 1.4, BARK_DARK, alpha=0.45)
    keyline(L, [right[0], right[-1]], P(mx, mz)[1], seed=seed + 2, alpha=0.4)
    fork = P(pts[-1][0], mz, pts[-1][1])
    return left + right[::-1], fork


# ================================================================ the floor cut-outs
def finish_cut(L, seed, under_c, fast=False, keep=0.66, sizes=(3, 2)):
    c, a = L.done()
    c = grade_cut(c, a, 0.90, seed=seed, uneven=0.05)
    c, a = hand(c, a, seed, amount=0.5, cell=14)
    a = (a > 0.5).astype(F32)
    return painted(c, a, under_c, seed=seed, sizes=sizes, keep=keep, fast=fast)


def grill_cut(seed, under_c, fast=False):
    """O-Kuni's grill: a long clay firebox on the ground before her door, a bed of charcoal, turban shells standing in it
    mouth up, their juice bubbling (the smoke and the embers are the engine's). O-Kuni stands behind it.
    -> (colour, cover, the shells' picture points, its base line)."""
    T = TEA
    Gd = GRILL
    u, w, ln, wd, hgt = Gd["u"], Gd["w"], Gd["len"], Gd["wid"], Gd["h"]
    L = Wet(SHAPE)
    tp = T.pt
    zz = T.xz(u, w)[1]
    kk = k(zz)
    clay_lit = lerp(thin(mixp(OCHRE, SIENNA, 0.30), 0.30), mixp(SIENNA, PRUSSIAN, 0.45), 0.30)          # fired clay, smoked
    clay_sh = lerp(mixp(mixp(OCHRE, SIENNA, 0.5), PRUSSIAN, 0.45), mixp(SIENNA, PRUSSIAN, 0.75), 0.30)
    soot = mixp(SIENNA, PRUSSIAN, 0.78)
    u0, u1, w0, w1 = u - ln / 2, u + ln / 2, w - wd / 2, w + wd / 2
    # it is turned with the teahouse: its long front faces the road (w0), its near end faces back along the road (u0)
    L.poly([tp(u0, w0, 0), tp(u1, w0, 0), tp(u1, w0, hgt), tp(u0, w0, hgt)], lerp(clay_lit, clay_sh, 0.45), clay_sh, g=(tp(u0, w0, hgt), tp(u0, w0, 0)))
    L.poly([tp(u0, w0, 0), tp(u0, w1, 0), tp(u0, w1, hgt), tp(u0, w0, hgt)], clay_lit, lerp(clay_lit, clay_sh, 0.3), g=(tp(u0, w0, hgt), tp(u0, w0, 0)))
    L.poly([tp(u0, w0, hgt), tp(u1, w0, hgt), tp(u1, w1, hgt), tp(u0, w1, hgt)], lerp(clay_sh, PRUSSIAN, 0.25))
    for (y_a, y_b, al) in ((hgt - 7, hgt, 0.55), (hgt - 15, hgt - 7, 0.28)):                                # soot along its top, darkest at the rim
        L.poly([tp(u0, w0, y_a), tp(u1, w0, y_a), tp(u1, w0, y_b), tp(u0, w0, y_b)], soot, alpha=al)
        L.poly([tp(u0, w0, y_a), tp(u0, w1, y_a), tp(u0, w1, y_b), tp(u0, w0, y_b)], soot, alpha=al * 0.8)
    L.poly([tp(u0 + 7, w0 + 6, hgt), tp(u1 - 7, w0 + 6, hgt), tp(u1 - 7, w1 - 6, hgt), tp(u0 + 7, w1 - 6, hgt)], lerp(PRUSSIAN, SIENNA, 0.25))
    L.poly([tp(u0 + 9, w0 + 8, hgt + 0.5), tp(u1 - 9, w0 + 8, hgt + 0.5), tp(u1 - 9, w1 - 8, hgt + 0.5), tp(u0 + 9, w1 - 8, hgt + 0.5)],
           lerp(VERMILION, SIENNA, 0.55), alpha=0.55)                                                               # the coals' bed, glowing dull red
    L.line([tp(u0 + 7, w0 + 6, hgt + 0.6), tp(u1 - 7, w0 + 6, hgt + 0.6)], lerp(VERMILION, NAPLES, 0.35), max(0.8, 2.0 * kk), 0.8)   # the glow at the near rim
    for ww in np.linspace(w0 + 10, w1 - 10, 4):                                                                     # the iron bars across it, lengthwise
        L.line([tp(u0 + 6, ww, hgt + 2), tp(u1 - 6, ww, hgt + 2)], mixp(PRUSSIAN, SIENNA, 0.35), max(0.6, 1.3 * kk), 0.75)
    rng = np.random.default_rng(seed)
    for i in range(16):
        q = tp(rng.uniform(u0 + 12, u1 - 12), rng.uniform(w0 + 9, w1 - 9), hgt + 1)
        L.ellipse(q[0], q[1], 1.4, 0.8, lerp(VERMILION, NAPLES, 0.25), alpha=0.85)
    shells = []
    shell_dk, shell_md = mixp(mixp(VIRIDIAN, SIENNA, 0.55), PRUSSIAN, 0.50), mixp(mixp(VIRIDIAN, SIENNA, 0.45), PRUSSIAN, 0.28)
    for i in range(14):                                                                     # the embers glowing between them
        q = tp(rng.uniform(u0 + 10, u1 - 10), rng.uniform(w0 + 8, w1 - 8), hgt + 1)
        L.ellipse(q[0], q[1], rng.uniform(1.2, 2.4), rng.uniform(0.7, 1.2), lerp(VERMILION, NAPLES, rng.uniform(0.1, 0.5)), alpha=0.9)
    for i in range(6):
        su = u0 + 16 + (ln - 32) * (i + 0.5) / 6 + rng.normal(0, 2)
        sw = w + rng.normal(0, 6)
        b = tp(su, sw, hgt + 1)
        s = 6.4 * kk * 1.6
        # the shell, mouth up in the coals: a knobbed cone, dark, its whorls ridged; its juice boiling in its mouth
        L.poly([(b[0] - s * 0.58, b[1] - s * 0.70), (b[0] + s * 0.58, b[1] - s * 0.70), (b[0] + s * 0.40, b[1] - s * 0.18), (b[0], b[1] + s * 0.04),
                (b[0] - s * 0.40, b[1] - s * 0.18)], shell_md, shell_dk, g=((b[0] - s * 0.6, b[1] - s), (b[0] + s * 0.6, b[1])))
        for j in (-0.46, -0.06, 0.32):
            L.ellipse(b[0] + j * s, b[1] - s * 0.62, s * 0.10, s * 0.09, mixp(OCHRE, SIENNA, 0.55), alpha=0.75)                 # the knobs
        L.ellipse(b[0], b[1] - s * 0.72, s * 0.56, s * 0.18, mixp(mixp(OCHRE, SIENNA, 0.5), PRUSSIAN, 0.35))                   # the mouth's lip
        L.ellipse(b[0] + s * 0.04, b[1] - s * 0.72, s * 0.38, s * 0.11, mixp(SIENNA, PRUSSIAN, 0.65))                         # its juice, dark
        L.ellipse(b[0] - s * 0.16, b[1] - s * 0.76, s * 0.10 + 0.25, s * 0.06 + 0.2, thin(NAPLES, 0.5), alpha=0.8)              # a bubble catching the light
        shells.append(b)
    L.line([tp(u0, w0, hgt), tp(u1, w0, hgt)], thin(mixp(OCHRE, NAPLES, 0.3), 0.35), 0.9, 0.7)
    keyline(L, [tp(u0, w0, 0), tp(u1, w0, 0), tp(u1, w0, hgt)], tp(u0, w0)[1], seed=seed + 1)
    c, a = finish_cut(L, seed, under_c, fast)
    base = [tp(u0, w0), tp(u1, w0)]
    return c, a, shells, base


def noren_cut(seed, under_c, fast=False):
    """The noren over the teahouse's door: indigo cloth in two panels, a white turban shell on it (our own mark); its hem
    is free (it stirs: fx noren-sway). -> (colour, cover, base line)."""
    T = TEA
    d0, d1 = T.door
    tp = T.pt
    L = Wet(SHAPE)
    w = -4.0
    top_, drop = 196.0 + 4.0, 62.0
    kk = k(T.xz((d0 + d1) / 2, 0)[1])
    for i in range(2):
        ua, ub = d0 + 8 + (d1 - d0 - 16) * (i / 2 + 0.012), d0 + 8 + (d1 - d0 - 16) * ((i + 1) / 2 - 0.012)
        q = [tp(ua, w, top_), tp(ub, w, top_), tp(ub, w, top_ - drop), tp(ua, w, top_ - drop)]
        L.poly(q, lerp(INDIGO, PRUSSIAN, 0.15), INDIGO, g=(q[0], q[3]))
        keyline(L, [q[3], q[2]], q[2][1] + 60, seed=seed + i, alpha=0.4)
    L.line([tp(d0 + 2, w, top_ + 2), tp(d1 - 2, w, top_ + 2)], TIMBER, max(1.0, 5 * kk), 1.0)
    c = tp((d0 + d1) / 2, w, top_ - drop * 0.48)
    s = 10 * kk
    L.ellipse(c[0], c[1], s * 0.72, s, thin(CERULEAN, 0.80))
    spiral = [(c[0] + s * 0.56 * (1 - t / 11) * math.cos(t), c[1] + s * 0.78 * (1 - t / 11) * math.sin(t)) for t in np.linspace(0, 10, 40)]
    L.line(spiral, INDIGO, 1.0, 1.0)
    c_, a_ = L.done()
    c_ = grade_cut(c_, a_, 0.92, seed=seed, uneven=0.05)
    a_ = (a_ > 0.5).astype(F32)
    out_c, out_a = painted(c_, a_, under_c, seed=seed, sizes=(3, 2), keep=0.7, fast=fast)
    return out_c, out_a, [tp(d0, 0), tp(d1, 0)]


def kago_cut(seed, under_c, fast=False):
    """The bearers' palanquin, set down at the mound's foot: an open-sided mountain kago on one long pole (the pole is
    the thing: thick, a little bowed, its far end resting on the ground), a short hood of matting under the pole, the
    seat a shallow woven basket slung from it, a blue cushion in it. Empty. -> (colour, cover, base line, the seat)."""
    K = KAGO
    x, z, Ln, Wd, Hh, pole = K["X"], K["Z"], K["length"], K["width"], K["height"], K["pole"]
    L = Wet(SHAPE)
    kk = k(z)
    along = U                                                # the pole lies along the road's line
    across = NL
    pt = lambda a, b, y: P(x + along[0] * a + across[0] * b, z + along[1] * a + across[1] * b, y)
    bam_lit, bam_sh, bam_dk = thin(mixp(OCHRE, VERONESE, 0.10), 0.40), mixp(OCHRE, PRUSSIAN, 0.36), mixp(OCHRE, PRUSSIAN, 0.58)
    mat_lit, mat_sh = thin(mixp(OCHRE, SIENNA, 0.18), 0.30), mixp(mixp(OCHRE, SIENNA, 0.5), PRUSSIAN, 0.42)
    pole_c = mixp(SIENNA, PRUSSIAN, 0.40)
    seat_h = 26.0
    a0, a1 = -Ln / 2, Ln / 2
    b0, b1 = -Wd / 2, Wd / 2

    def pole_y(f):                                           # held in the slings over the set-down seat, sagging a little
        return Hh - 6 * math.sin(math.pi * f)
    fs = np.linspace(0, 1, 13)
    pp = [pt(-pole / 2 + pole * f, 0, pole_y(f)) for f in fs]
    py_at = lambda a: pole_y((a + pole / 2) / pole)
    # the hood: a short arch of matting hugging the pole over the seat
    hood_top = [pt(a, 0, py_at(a) + 2) for a in np.linspace(a0 - 4, a1 + 4, 9)]
    hood_hem = [pt(a, b0 + 4, py_at(a) - 26 - 4 * math.sin(math.pi * (a - a0 + 4) / (Ln + 8))) for a in np.linspace(a0 - 4, a1 + 4, 9)]
    L.poly(hood_top + hood_hem[::-1], lerp(mat_lit, mat_sh, 0.25), lerp(mat_lit, mat_sh, 0.55), g=(hood_top[4], hood_hem[4]))
    L.poly(hood_hem + [(p[0], p[1] + 2.2) for p in hood_hem[::-1]], mat_sh)
    for i in range(1, 8):
        L.line([hood_top[i], hood_hem[i]], mixp(SIENNA, PRUSSIAN, 0.35), 0.5, 0.4)
    # the seat: a shallow woven basket on the ground, a low back at its far end, the cushion in it
    L.poly([pt(a0, b0, seat_h), pt(a1, b0, seat_h), pt(a1, b1, seat_h), pt(a0, b1, seat_h)], lerp(bam_dk, PRUSSIAN, 0.2))
    L.poly([pt(a0 + 8, b0 + 8, seat_h + 1), pt(a1 - 16, b0 + 8, seat_h + 1), pt(a1 - 16, b1 - 8, seat_h + 1), pt(a0 + 8, b1 - 8, seat_h + 1)], lerp(INDIGO, WHITE, 0.22))
    L.poly([pt(a1 - 8, b0 + 6, seat_h), pt(a1 - 8, b1 - 6, seat_h), pt(a1 - 8, b1 - 6, seat_h + 34), pt(a1 - 8, b0 + 6, seat_h + 34)], bam_sh)
    L.poly([pt(a0, b0, 0), pt(a1, b0, 0), pt(a1, b0, seat_h), pt(a0, b0, seat_h)], bam_lit, lerp(bam_lit, bam_sh, 0.4), g=(pt(a0, b0, seat_h), pt(a0, b0, 0)))
    L.poly([pt(a0, b0, 0), pt(a0, b1, 0), pt(a0, b1, seat_h), pt(a0, b0, seat_h)], lerp(bam_lit, WPAPER, 0.2))
    for v in (8.0, 16.0):
        L.line([pt(a0, b0, v), pt(a1, b0, v)], bam_dk, 0.7, 0.55)
    for f in np.linspace(0.1, 0.9, 6):
        L.line([pt(a0 + Ln * f, b0, 1), pt(a0 + Ln * f, b0, seat_h - 1)], bam_dk, 0.55, 0.45)
    L.line([pt(a0, b0, seat_h), pt(a1, b0, seat_h)], bam_lit, max(1.0, 3.4 * kk), 1.0)
    for ae in (a0 + 6, a1 - 6):                                   # the slings, a narrow V at each end, up to the pole
        t_ = pt(ae, 0, py_at(ae) - 2)
        for bb in (b0 + 4, b1 - 4):
            L.line([t_, pt(ae, bb, seat_h)], bam_lit if bb < 0 else bam_sh, max(1.0, 3.0 * kk), 1.0)
    L.line(pp, pole_c, max(2.0, 9.5 * kk), 1.0)
    L.line([(p[0], p[1] - max(1.0, 2.8 * kk)) for p in pp], thin(mixp(OCHRE, SIENNA, 0.25), 0.25), max(0.9, 3.0 * kk), 1.0)
    for e_ in (pp[0], pp[-1]):
        L.ellipse(e_[0], e_[1], max(1.4, 4.5 * kk), max(1.4, 4.5 * kk), thin(mixp(OCHRE, SIENNA, 0.4), 0.3))
    keyline(L, [pt(a0, b0, 0), pt(a1, b0, 0), pt(a1, b0, seat_h)], pt(0, b0, 0)[1], seed=seed + 1)
    keyline(L, pp, pt(0, 0, 0)[1], seed=seed + 2, alpha=0.3)
    c, a = finish_cut(L, seed, under_c, fast, keep=0.62, sizes=(4, 2))
    base = [pt(-pole / 2, b0 - 4, 0), pt(pole / 2, b0 - 4, 0)]
    seat = pt(0, 0, 0)
    return c, a, base, seat


def trunks_cut(seed, under_c, fast=False):
    """Soshichi's willow trunks, set down on the inland verge: five tiers stacked chest high, the lower four wrapped in his
    indigo carrying cloth (full over each tier, drawn in at the rims, creased from its knot, a white ring for his house's
    mark); the top tier unwrapped and open, paper packets in it, its lid propped behind, the ledger on its rim.
    -> (colour, cover, base line)."""
    T_ = TRUNKS
    x, z, w, d, tier, n = T_["X"], T_["Z"], T_["w"], T_["d"], T_["tier"], T_["n"]
    L = Wet(SHAPE)
    kk = k(z)
    along, across = U, NL
    pt = lambda a, b, y: P(x + along[0] * a + across[0] * b, z + along[1] * a + across[1] * b, y)
    rng = np.random.default_rng(seed)
    willow_lit, willow_sh = thin(mixp(OCHRE, SIENNA, 0.20), 0.26), mixp(mixp(OCHRE, SIENNA, 0.3), PRUSSIAN, 0.38)
    cloth_lit = lerp(INDIGO, WPAPER, 0.10)
    cloth_sh = lerp(INDIGO, PRUSSIAN, 0.55)
    a0, a1, b0, b1 = -w / 2, w / 2, -d / 2, d / 2
    L.poly([pt(a0 - 18, b0 - 10, 1), pt(a1 + 20, b0 - 8, 1), pt(a1 + 16, b1 + 10, 1), pt(a0 - 14, b1 + 8, 1)], lerp(mixp(OCHRE, PRUSSIAN, 0.5), PRUSSIAN, 0.2))   # a mat spread under them
    yt = 2 + n * tier
    yw = yt - tier                                           # the cloth's top: the four lower tiers wrapped
    ys_ = np.linspace(2, yw, 4 * 8 + 1)
    bulge = lambda y_: 1.8 * math.sin(math.pi * ((y_ - 2) % tier) / tier)          # the cloth full over each tier, drawn in at its rims
    front_ = [pt(a0 - bulge(y_) * 0.5, b0 - bulge(y_), y_) for y_ in ys_] + [pt(a1 + bulge(y_), b0 - bulge(y_), y_) for y_ in ys_[::-1]]
    side_ = [pt(a0 - bulge(y_), b0 - bulge(y_) * 0.5, y_) for y_ in ys_] + [pt(a0 - bulge(y_), b1 + bulge(y_), y_) for y_ in ys_[::-1]]
    # the wrapped part: the side toward the sun (the near end, a0) lit, the long side (b0) in half shade
    L.poly(front_, lerp(cloth_lit, cloth_sh, 0.40), cloth_sh, g=(pt(a0, b0, yw), pt(a0, b0, 2)))
    L.poly(side_, cloth_lit, lerp(cloth_lit, cloth_sh, 0.25), g=(pt(a0, b0, yw), pt(a0, b0, 2)))
    L.line([pt(a0 - 1, b0 - 1, 3), pt(a0 - 1, b0 - 1, yw)], lerp(cloth_lit, WPAPER, 0.25), max(0.8, 2.0 * kk), 0.7)          # the cloth's fold over the corner
    for y_ in (2 + tier * 1.0, 2 + tier * 2.0, 2 + tier * 3.0):                                              # drawn in at the tiers' rims
        L.line([pt(a0, b1, y_), pt(a0, b0, y_), pt(a1, b0, y_)], lerp(cloth_sh, PRUSSIAN, 0.45), 0.7, 0.45)
    for (fa, fb) in ((0.0, a0 + 4), (0.0, a1 - 4), (-3.0, a0 + 14), (3.0, a1 - 14)):                         # creases running down from the knot
        L.line([pt(fa, b0 - 1.5, yw - 3), pt((fa + fb) / 2, b0 - 1.8, yw * 0.55), pt(fb, b0 - 1.0, 6)], lerp(cloth_sh, PRUSSIAN, 0.4), 0.7, 0.40)
    rc = pt(4, b0 - 2, yw * 0.46)                                                                            # the house's mark: a white ring
    rr_ = max(2.0, 11.0 * kk)
    L.ellipse(rc[0], rc[1], rr_, rr_ * 1.05, WPAPER, alpha=0.85)
    L.ellipse(rc[0], rc[1], rr_ * 0.62, rr_ * 0.66, lerp(cloth_lit, cloth_sh, 0.45))
    # the top tier, unwrapped: willow, its weave in short upright strokes; open, the packets in it; its lid propped behind
    y0, y1 = yw, yt
    L.poly([pt(a0, b0, y0), pt(a1, b0, y0), pt(a1, b0, y1), pt(a0, b0, y1)], lerp(willow_lit, willow_sh, 0.45), willow_sh, g=(pt(a0, b0, y1), pt(a0, b0, y0)))
    L.poly([pt(a0, b0, y0), pt(a0, b1, y0), pt(a0, b1, y1), pt(a0, b0, y1)], willow_lit, lerp(willow_lit, willow_sh, 0.25))
    for f in np.linspace(0.06, 0.94, 11):
        L.line([pt(a0 + w * f, b0, y0 + 2), pt(a0 + w * f, b0, y1 - 2)], mixp(OCHRE, PRUSSIAN, 0.45), 0.5, 0.40)
    for f in np.linspace(0.1, 0.9, 7):
        L.line([pt(a0, b0 + d * f, y0 + 2), pt(a0, b0 + d * f, y1 - 2)], mixp(OCHRE, PRUSSIAN, 0.35), 0.5, 0.35)
    L.line([pt(a0, b1, y1), pt(a0, b0, y1), pt(a1, b0, y1)], lerp(willow_lit, WPAPER, 0.35), max(0.8, 2.2 * kk), 0.85)   # the rim in the sun
    L.poly([pt(a0 + 3, b0 + 3, yt), pt(a1 - 3, b0 + 3, yt), pt(a1 - 3, b1 - 3, yt), pt(a0 + 3, b1 - 3, yt)], lerp(willow_sh, PRUSSIAN, 0.45))
    for (pa, pb, col) in ((-18.0, -10.0, VERMILION), (-6.0, -12.0, COBALT), (6.0, -9.0, VERMILION), (16.0, -11.0, OCHRE), (-12.0, 2.0, COBALT), (2.0, 1.0, VERMILION)):
        q = [pt(pa - 5, pb - 3, yt + 1), pt(pa + 5, pb - 3, yt + 1), pt(pa + 5, pb + 3, yt + 1), pt(pa - 5, pb + 3, yt + 1)]
        L.poly(q, thin(mixp(OCHRE, NAPLES, 0.3), 0.55))                                                      # paper packets of medicine
        L.poly([q[0], q[1], lerp(np.asarray(q[1]), np.asarray(q[2]), 0.35), lerp(np.asarray(q[0]), np.asarray(q[3]), 0.35)], thin(col, 0.25), alpha=0.85)
    L.poly([pt(a0, b1, yt), pt(a1, b1, yt), pt(a1, b1 + 10, yt + 34), pt(a0, b1 + 10, yt + 34)], willow_lit, lerp(willow_lit, willow_sh, 0.3))
    for f in np.linspace(0.08, 0.92, 9):
        L.line([pt(a0 + w * f, b1, yt + 1), pt(a0 + w * f, b1 + 10, yt + 33)], mixp(OCHRE, PRUSSIAN, 0.40), 0.5, 0.35)
    # the knot: the cloth's two corners tied at the front of its top, their ears up over the top tier's foot
    kn = pt(0, b0 - 2.5, yw + 1)
    s_ = max(2.5, 8.0 * kk)
    L.poly([(kn[0] - s_ * 0.2, kn[1]), (kn[0] - s_ * 1.3, kn[1] - s_ * 1.0), (kn[0] - s_ * 0.7, kn[1] - s_ * 1.35), (kn[0] + s_ * 0.1, kn[1] - s_ * 0.3)], cloth_lit)
    L.poly([(kn[0] + s_ * 0.2, kn[1]), (kn[0] + s_ * 1.1, kn[1] - s_ * 1.15), (kn[0] + s_ * 1.35, kn[1] - s_ * 0.6), (kn[0] + s_ * 0.3, kn[1] + s_ * 0.1)], cloth_sh)
    L.ellipse(kn[0], kn[1], s_ * 0.55, s_ * 0.45, lerp(cloth_lit, WPAPER, 0.15))
    # the ledger on the rim at the near end: a thick book of pale paper, its dark cover and its cord
    lg = [pt(a0 - 2, b0 + 4, yt + 2), pt(a0 + 22, b0 + 4, yt + 2), pt(a0 + 22, b0 + 20, yt + 2), pt(a0 - 2, b0 + 20, yt + 2)]
    L.poly([pt(a0 - 2, b0 + 4, yt), pt(a0 + 22, b0 + 4, yt), pt(a0 + 22, b0 + 4, yt + 3), pt(a0 - 2, b0 + 4, yt + 3)], thin(NAPLES, 0.55))
    L.poly(lg, thin(mixp(OCHRE, NAPLES, 0.25), 0.40))
    L.line([lg[0], lg[3]], mixp(SIENNA, PRUSSIAN, 0.55), max(0.8, 2.0 * kk), 0.9)
    keyline(L, [pt(a1, b0, 2), pt(a1, b0, yt), pt(a1, b1 + 10, yt + 34)], pt(0, b0, 0)[1], seed=seed + 1)
    keyline(L, [pt(a0, b0, 2), pt(a1, b0, 2)], pt(0, b0, 0)[1], seed=seed + 2, alpha=0.4)
    c, a = finish_cut(L, seed, under_c, fast)
    base = [pt(a0 - 18, b0 - 10, 0), pt(a1 + 20, b0 - 8, 0)]
    return c, a, base


def fuji():
    """Fuji as round twenty-one's kit knows it (for the cap of cloud: the same cloud as at the top of the pass, by the
    same code at this mountain's size)."""
    return Fuji(summit=V.FUJI_AT, foot=V.FUJI_FOOT, half=V.FUJI_HALF, snow=0.40, seed=21)


def cloud_cut(seed, fast=False):
    """Fuji's cap of cloud (on / off): the kit's cap (edo_kurasawa_kit.cloud_cap, the top of the pass's own) at this
    mountain's size, laid as a watercolour: lifted out of the sky as bare paper where the sun is on it, a thin cool wash
    under it, its top edge firm (there is no key line in the distance). -> (colour, cover, outline)."""
    sheet, lines = Sheet(SHAPE), Sheet(SHAPE)
    outline = cloud_cap(sheet, lines, fuji())
    c, a = sheet.done()
    a = (a > 0.5).astype(F32)
    x, y = grid(SHAPE)
    ys, xs = np.where(a > 0.5)
    y0, y1 = ys.min(), ys.max()
    t = np.clip((y - y0) / max(y1 - y0, 1), 0, 1)
    under = thin(mixp(COBALT, SIENNA, 0.14), 0.62)
    col = lerp(WPAPER[None, None, :] * np.ones_like(c), lerp(WPAPER, under, 0.85)[None, None, :] * np.ones_like(c), (np.clip((t - 0.45) / 0.5, 0, 1) ** 1.2)[..., None])
    col = lerp(col, c, 0.18)                                 # (the kit's own flats, a breath of them: its rider and its streamer)
    col *= (1 + (noise(SHAPE, (40, 12), seed, 3) - 0.5)[..., None] * 0.05)
    return np.clip(col, 0, 1).astype(F32), a, outline

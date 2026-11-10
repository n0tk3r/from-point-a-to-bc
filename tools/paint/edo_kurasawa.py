"""PAINT-21A: Nishikurasawa, the rest village at the eastern foot of the Satta Pass, about 8 April 1830, morning
(edo-kurasawa). PAINT-23 (round twenty-three, tools/paint/DEPTH.md, RECOMPOSE): seen again from a new place, through a new
camera, in THREE PLANES and in WATERCOLOUR (the act's woodblock drawing laid in washes on paper, as Yui's pilot was).

PLACE   We stand ON THE TOKAIDO at the rest village, on the road's inland verge a few steps short of O-Kuni's teahouse,
        and look along the road the way it goes: west, toward the pass (the act's compass, as at Yui: the bay on the left
        with Fuji across it, the way west to the right). The road comes in from behind us at the left (from Yui), runs
        along the teahouse's open front and away to the right; at the rest place it bends right, in front of the 40th
        distance mound, and starts up the hill (the climb to the pass), out at the right edge. On the bay's side of the
        road, beyond the teahouse, the trodden rest place out to a low wall over the shore; beyond the wall the bay, its
        boats, the far shore curving back toward Yui and two capes stepping out from under Mount Satta, the headland at
        the right; across the bay, Fuji, under its cap of cloud. (Camera and places: edo_kurasawa_view.py.)
        O-Kuni's teahouse: thatched, its front open to the road under a deep eave on slim posts, a bench under the eave,
        the matted room open behind on the bay, the door to the earth floor at its far end with the noren, the grill of
        turban shells out before it, a signboard of our own at the corner (a shell, and brush marks that are not
        characters). The bearers' palanquin set down at the mound's foot; Soshichi's willow trunks on the verge.
LIGHT   The act's sun: in the east, behind us and to the left, about 39 degrees up (view.SUN3), low along the road from
        Yui: the teahouse's near end, the mound's and the trunk's left sides lit; the teahouse's front, along the road,
        under its eave in shade, the inside in shade, the bay bright through its open back. Shadows fall to the right and
        away, each a cool glaze over the local colour; a shore pine behind us on the left, out of the picture, lays its
        long shadow across the road at our feet, dappled, its edge leading in.
DEPTH   horizon 342, full 562 (persp.Camera, FOCAL 680): the eye 2.4 m above the road; a grown-up 90 to 160 px where
        people stand. The road and the teahouse turned 45 degrees: two vanishing points, neither in the picture.
NEAR    (near.png, front.png: edo_kurasawa_near.py) the hackberry's crown and the bough it sends out toward us, over the
        top right corner; the near end of O-Kuni's eave with a reed blind let down in the first bay, at the top left; the
        roadside's bank along the bottom (sasa, pampas, a stone), in the shade of the hill behind us. Dark, warm in the
        darks, lit only along the edges the sun finds.
MIDDLE  the play, the best lit: the road (packed earth, tracks worn by feet, stones and tufts that shrink with distance),
        the teahouse's front and its things, the rest place, the mound and the hackberry's trunk, the palanquin, the
        trunks; every standing thing throws its shadow one way. NOTHING NEW STANDS WHERE SOMEBODY CAN WALK BEHIND IT.
FAR     (edo_kurasawa_far.py: Yui's recipe at this camera) the bay with boats at three distances; the far shore and
        Fuji's foothills, two capes, Mount Satta with the cliff road across its face; Fuji, the snow bare paper; one
        cloud in the whole sky, the cap on Fuji (cloud.png). Each layer paler toward the sky's colour. No line.
LIGHTS  the lightest light is the paper: Fuji's snow and its cap of cloud; in the play the sunlit road beyond the pine's
        shade, leading to the bend.
PAPER   watercolor.wash on the backdrop and wash_cut (the same seed) on every cut-out, just before the palette (finish_all):
        WET (the `soft` mask) the sky 1, Fuji 0.65, the far shore and the capes 0.5, Satta 0.3, the open water 0.75 at
        the horizon falling to 0.2 at the wall; 0 on everything that stands in the play.

  python3 edo_kurasawa.py fast        the composition without the brush pass (out/edo-kurasawa-1-under.png, -2-all.png)
  python3 edo_kurasawa.py fast wash   the same with the paper's finish (out/edo-kurasawa-fast-comp.png)
  python3 edo_kurasawa.py             the full passes: out/edo-kurasawa/ (back.png, the cut-outs, layout.json), -comp.png
  python3 install.py edo-kurasawa     keys it in the game's paints and installs it; then python3 ../stamp.py
"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import (F32, blur, glow, grid, lerp, mask_line, mask_poly, noise, over, ramp, rgb, step, strokes, tint, warp, grain,
                   palette_of, to_palette, save)
import land
import depth as D
import watercolor as WC
from edo_village_kit import (WPAPER, SHADE, SHADE_WARM, SHADE_PINES, Wet, thin, mixp, glaze, hand, NAPLES, CERULEAN, COBALT, ULTRA,
                             PRUSSIAN, OCHRE, SIENNA, VERONESE, VIRIDIAN)
from edo_village_far import HORIZON_C
import edo_kurasawa_view as V
from edo_kurasawa_view import (HZ, FULL, SHAPE, W, H, P, k, G, U, NL, NR, TEA, GRILL, SIGN, MOUND, HACK, KAGO, TRUNKS, SUN, ROAD_W,
                               road_mid, road_edge, road_lift, S_CLIMB, add, ground_grid)
import edo_kurasawa_far as FAR
import edo_kurasawa_things as T
import edo_kurasawa_near as NEAR

SEED = 1831
OUT = "out/edo-kurasawa"
EARTH = lerp(thin(OCHRE, 0.45), PRUSSIAN, 0.16)            # the Tokaido: packed earth (Yui's street, a little greyer)
GRASS = thin(mixp(VERONESE, VIRIDIAN, 0.40), 0.16)
GRASS_DRY = thin(mixp(OCHRE, VERONESE, 0.40), 0.28)


# ================================================================ where things are on the ground, for every pixel
def road_field(X, Z):
    """For every pixel of the ground: how far along the road (s, cm) its nearest point is, and how far to the side of
    the road's middle (d, cm; positive to the right, inland)."""
    best = np.full(X.shape, 1e9, dtype=F32)
    s_of = np.zeros(X.shape, dtype=F32)
    d_of = np.zeros(X.shape, dtype=F32)
    for s in np.arange(-500.0, 2400.0, 12.0):
        mx, mz = road_mid(s)
        dx, dz = V.road_dir(s)
        rx, rz = dz, -dx                                       # to the right of the way
        ex, ez = X - mx, Z - mz
        dist = ex * ex + ez * ez
        closer = dist < best
        best = np.where(closer, dist, best)
        s_of = np.where(closer, s, s_of)
        d_of = np.where(closer, ex * rx + ez * rz, d_of)
    return s_of, d_of


def tea_field(X, Z):
    """For every pixel of the ground: the place relative to the teahouse (u along its front, w back from it)."""
    c0 = TEA.c0
    ex, ez = X - c0[0], Z - c0[1]
    return ex * U[0] + ez * U[1], ex * NL[0] + ez * NL[1]


def ground_region():
    return mask_poly(SHAPE, V.ground_outline(), soft=0.8, wobble=1.2, seed=29)


# ================================================================ pass 1: broad, in washes
def paint_ground(pic, seed):
    """The level ground: the road, its verges, the rest place on the bay's side, the inland verge, the climb's foot.
    Each a graded wash, pale and cool far off, deeper and warmer toward us, never even; measured in the world, so its
    patches and the road's worn tracks shrink with distance and follow the road round its bend."""
    x, y = grid(SHAPE)
    X, Z, below = ground_grid(SHAPE)
    gm = ground_region() * below
    s_, d_ = road_field(X, Z)
    tu, tw = tea_field(X, Z)
    wn = FAR.world_noise
    t = np.clip((y - HZ) / float(H - HZ), 0, 1) ** 0.85
    hw = ROAD_W / 2
    wander = (wn(X, Z, 150, seed + 60, 2) - 0.5) * 40
    road = (1 - step(hw - 12, hw + 12, np.abs(d_ + wander))) * gm
    # ---- everything off the road: earth with grass coming up in it, greener inland and toward the wall
    base = ramp(t, [(0.0, lerp(HORIZON_C, EARTH, 0.42)), (0.30, thin(EARTH, 0.36)), (0.70, thin(lerp(EARTH, SIENNA, 0.06), 0.14)), (1.0, lerp(EARTH, SIENNA, 0.20))])
    base *= (1 + ((wn(X, Z, 160, seed + 30, 3) - 0.5) * 0.12 + (wn(X, Z, 40, seed + 31, 2) - 0.5) * 0.07)[..., None])
    kk = (wn(X, Z, 420, seed + 32, 2) - 0.5) * 0.04
    base[..., 0] += kk
    base[..., 2] -= kk
    over(pic, np.clip(base, 0, 1), gm)
    inland = np.clip((d_ - hw - 20) / 120.0, 0, 1) * gm
    bayside = np.clip((-d_ - hw - 40) / 200.0, 0, 1) * gm
    tread = 1 - step(0.40, 0.70, wn(X, Z, 230, seed + 33, 3))                   # trodden patches stay bare
    grass_c = ramp(t, [(0.0, lerp(HORIZON_C, GRASS, 0.5)), (0.4, GRASS), (1.0, lerp(GRASS, mixp(VIRIDIAN, PRUSSIAN, 0.4), 0.25))])
    grass_c = lerp(grass_c, GRASS_DRY, (wn(X, Z, 120, seed + 34, 2) * 0.55)[..., None])
    grass_c *= (1 + (wn(X, Z, 34, seed + 39, 2) - 0.5)[..., None] * 0.16)
    over(pic, grass_c, (np.clip(inland * (0.78 + 0.22 * (1 - tread)), 0, 1) * 0.95).astype(F32))
    wall_side = np.clip((tw - 380) / 260.0, 0, 1) * (tu > TEA.L - 40) * bayside        # toward the wall, beyond the teahouse
    over(pic, grass_c, (wall_side * (1 - tread * 0.7) * 0.7).astype(F32))
    # the rest place: trodden pale where people stop and bearers wait (before the mound, beyond the teahouse)
    rest = mask_poly(SHAPE, [P(*TEA.xz(TEA.L + 20, -60)), P(*TEA.xz(TEA.L + 40, 300)), P(200, 2050), P(560, 1740), P(700, 1520),
                             P(560, 1380), P(250, 1330)], soft=8.0, wobble=6.0, seed=seed + 37) * gm
    over(pic, thin(EARTH, 0.66), (rest * 0.55 * (0.7 + 0.3 * tread)).astype(F32))
    # ---- the road: packed earth; three tracks worn pale by feet (no wheel ruts: nothing wheeled used this road), its
    # middle and edges rougher; a little greyer than the verges
    earth = ramp(t, [(0.0, lerp(HORIZON_C, EARTH, 0.46)), (0.28, thin(lerp(EARTH, PRUSSIAN, 0.05), 0.36)), (0.60, thin(lerp(EARTH, SIENNA, 0.10), 0.12)),
                     (1.0, lerp(lerp(EARTH, SIENNA, 0.22), PRUSSIAN, 0.06))])
    across = d_ / hw
    wob = (wn(X, Z, (70, 900), seed + 35, 2) - 0.5) * 0.30
    track = sum(np.exp(-((across - c - wob) / 0.17) ** 2) for c in (-0.52, 0.04, 0.56))
    wuv = FAR.world_noise_uv
    streak = wuv(d_, s_, Z, (12, 220), seed + 41, 2)                           # the tracks are many short scuffs, along the way
    earth = lerp(earth, thin(EARTH, 0.78), (np.clip(track, 0, 1) * (0.25 + 0.45 * streak))[..., None])
    earth *= (1 + ((wuv(d_, s_, Z, (26, 400), seed + 36, 3) - 0.5) * 0.14 + (wn(X, Z, 90, seed + 38, 2) - 0.5) * 0.06)[..., None])
    scuff = step(0.66, 0.80, wuv(d_, s_, Z, (8, 60), seed + 42, 2))             # small dark scuffs and dents, where feet have dug in
    earth *= (1 - (scuff * 0.08)[..., None])
    rough = step(0.78, 1.0, np.abs(across)) * 0.16 + np.exp(-((across - 0.30 - wob) / 0.07) ** 2) * 0.10 + np.exp(-((across + 0.26 - wob) / 0.07) ** 2) * 0.10
    earth *= (1 - rough[..., None])
    over(pic, np.clip(earth, 0, 1), road)
    tint(pic, thin(mixp(OCHRE, PRUSSIAN, 0.5), 0.40), ((1 - step(5.0, 24.0, np.abs(np.abs(d_ + wander) - hw))) * gm * 0.62).astype(F32))   # the road's crumbling edges
    # ---- the climb: from the bend the road starts up the hill; its surface turns up toward the sun (lighter), the hill
    # cut back for it on its far side (a bank of earth in shade, grass on its lip)
    climb = road * np.clip((s_ - S_CLIMB) / 140.0, 0, 1)
    over(pic, lerp(thin(EARTH, 0.60), NAPLES, 0.10), (climb * 0.45).astype(F32))
    # the drip line along the teahouse's front, where the rain comes off the thatch: a shallow gutter of darker earth,
    # with small stones set in it; it runs to the road's vanishing point
    drip = (1 - step(6.0, 20.0, np.abs(tw + TEA.over - 6))) * (tu > -TEA.over_end) * (tu < TEA.L + TEA.over_end) * gm
    tint(pic, thin(mixp(SIENNA, PRUSSIAN, 0.45), 0.42), (drip * 0.55).astype(F32))
    info = dict(ground=gm, road=road, s=s_, d=d_, tu=tu, tw=tw, inland=inland, bayside=bayside, rest=rest)
    return info


def climb_bank(pic, seed):
    """The bank cut back for the climb on its far side, behind the road at the right edge, under the mound."""
    pts_top, pts_foot = [], []
    for s in np.linspace(S_CLIMB - 120, S_CLIMB + 700, 14):
        e = road_edge(s, -1, 10)
        lift = road_lift(s)
        pts_foot.append(P(e[0], e[1], lift))
        pts_top.append(P(e[0] + NL[0] * 20, e[1] + NL[1] * 20, lift + 30 + 0.16 * max(0, s - S_CLIMB)))
    m = mask_poly(SHAPE, pts_top + pts_foot[::-1], soft=0.7, wobble=1.2, seed=seed + 40)
    over(pic, lerp(thin(mixp(OCHRE, SIENNA, 0.25), 0.30), PRUSSIAN, 0.30), (m * 0.85).astype(F32))
    lip = mask_line(SHAPE, pts_top, 2.4, soft=0.5)
    over(pic, mixp(VIRIDIAN, PRUSSIAN, 0.30), (lip * 0.8).astype(F32))
    return m


def hull(points):
    pts = sorted(set((round(p[0], 3), round(p[1], 3)) for p in points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def shadow_poly(foot, tops):
    """The shadow on the ground of a thing: its foot (ground places X, Z) and its high points (X, Y, Z) laid along the
    sun. -> picture points of the hull."""
    pts = list(foot) + [V.shadow_of(X, Z, Y) for X, Y, Z in tops]
    return [P(px, pz) for px, pz in hull(pts)]


def cast_shadows(pic, info, seed):
    """Every standing thing's shadow, one way (to the right and away), as a glaze over the ground; and the long shadow of
    a shore pine behind us on the left, out of the picture, lying across the road at our feet, dappled. -> its mask."""
    gm = info["ground"]
    X, Z, below = ground_grid(SHAPE)
    sh = np.zeros(SHAPE, dtype=F32)

    def add(pts, amount=0.9, soft=0.7, wobble=0.8, s=0):
        if len(pts) >= 3:
            np.maximum(sh, mask_poly(SHAPE, pts, soft=soft, wobble=wobble, seed=seed + s) * amount, out=sh)
    Tt = TEA
    r = Tt.roof_pts()
    foot = [Tt.xz(0, 0), Tt.xz(Tt.L, 0), Tt.xz(Tt.L, Tt.D), Tt.xz(0, Tt.D)]
    tops = [(*Tt.xz(*r[k_])[:1], r["e"], Tt.xz(*r[k_])[1]) for k_ in ("A", "B", "C", "D")]
    tops = [(Tt.xz(*r[k_])[0], r["e"] + Tt.thick, Tt.xz(*r[k_])[1]) for k_ in ("A", "B", "C", "D")] + \
           [(Tt.xz(*r[k_])[0], r["top"], Tt.xz(*r[k_])[1]) for k_ in ("R0", "R1")]
    add(shadow_poly(foot + [Tt.xz(*r["A"]), Tt.xz(*r["B"])], tops), 0.92, s=1)
    for u in T.EAVE_POSTS:                                                  # the eave's posts: thin lines along the light
        X0, Z0 = Tt.xz(u, T.POST_W)
        X1, Z1 = V.shadow_of(X0, Z0, Tt.eave)
        np.maximum(sh, mask_line(SHAPE, [P(X0, Z0), P(X1, Z1)], [max(1.0, 10 * k(Z0)), max(1.0, 10 * k(Z1))], soft=0.5) * 0.85, out=sh)
    Xs, Zs = Tt.xz(SIGN["u"], SIGN["w"])
    X1, Z1 = V.shadow_of(Xs, Zs, SIGN["h"])
    np.maximum(sh, mask_line(SHAPE, [P(Xs, Zs), P(X1, Z1)], [max(1.0, 8 * k(Zs)), max(1.5, 30 * k(Z1))], soft=0.5) * 0.85, out=sh)
    # the grill, the palanquin, the trunks (cut-outs: their shadows are the backdrop's)
    g = GRILL
    gfoot = [Tt.xz(g["u"] - g["len"] / 2, g["w"] - g["wid"] / 2), Tt.xz(g["u"] + g["len"] / 2, g["w"] - g["wid"] / 2),
             Tt.xz(g["u"] + g["len"] / 2, g["w"] + g["wid"] / 2), Tt.xz(g["u"] - g["len"] / 2, g["w"] + g["wid"] / 2)]
    add(shadow_poly(gfoot, [(fx, g["h"], fz) for fx, fz in gfoot]), 0.85, s=3)
    kg = KAGO
    kc = (kg["X"], kg["Z"])
    kfoot = [add_(kc, -kg["length"] / 2, -kg["width"] / 2), add_(kc, kg["length"] / 2, -kg["width"] / 2), add_(kc, kg["length"] / 2, kg["width"] / 2),
             add_(kc, -kg["length"] / 2, kg["width"] / 2)]
    add(shadow_poly(kfoot, [(fx, kg["height"], fz) for fx, fz in kfoot] + [(*add_(kc, -kg["pole"] / 2, 0)[:1], kg["height"] + 18, add_(kc, -kg["pole"] / 2, 0)[1])]), 0.8, s=4)
    tk = TRUNKS
    tc = (tk["X"], tk["Z"])
    tfoot = [add_(tc, -tk["w"] / 2 - 20, -tk["d"] / 2 - 12), add_(tc, tk["w"] / 2 + 24, -tk["d"] / 2 - 10), add_(tc, tk["w"] / 2 + 20, tk["d"] / 2 + 12),
             add_(tc, -tk["w"] / 2 - 18, tk["d"] / 2 + 10)]
    tfoot_b = [add_(tc, -tk["w"] / 2, -tk["d"] / 2), add_(tc, tk["w"] / 2, -tk["d"] / 2), add_(tc, tk["w"] / 2, tk["d"] / 2), add_(tc, -tk["w"] / 2, tk["d"] / 2)]
    add(shadow_poly(tfoot_b, [(fx, tk["tier"] * tk["n"] + 34, fz) for fx, fz in tfoot_b]), 0.85, s=5)
    # the mound and the hackberry's trunk (their shadows go behind them, toward Satta's foot)
    m = MOUND
    mfoot = [(m["X"] + m["r"] * math.cos(a), m["Z"] + m["r"] * 0.9 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 18)[:-1]]
    add(shadow_poly(mfoot, [(m["X"], m["h"], m["Z"])]), 0.8, s=6)
    add(shadow_poly([(m["X"] - HACK["r"], m["Z"]), (m["X"] + HACK["r"], m["Z"])], [(m["X"] - HACK["r"], 560, m["Z"]), (m["X"] + HACK["r"], 560, m["Z"])]), 0.8, s=7)
    sh = (sh * gm).astype(F32)
    glaze(pic, sh, SHADE, 1.0)
    # ---- the shore pine behind us on the left: its trunk's long shadow comes in across the road from the left edge,
    # and its crown's lies at our feet in the bottom left: a body of shade, its edge scalloped by the pads of needles,
    # running in along the light; the sun comes through it in flecks
    x0_, z0_ = -1150.0, -120.0
    ln_ = math.hypot(*SUN)
    ux, uz = SUN[0] / ln_, SUN[1] / ln_
    sl = slice(480, H)
    trunk = [P(x0_ + SUN[0] * t_ + 10 * math.sin(t_ / 70.0), z0_ + SUN[1] * t_) for t_ in np.linspace(300, 760, 14)]
    pine = np.zeros(SHAPE, dtype=F32)
    np.maximum(pine, mask_line(SHAPE, trunk, [max(1.2, 40 * k(z0_ + SUN[1] * t_)) for t_ in np.linspace(300, 760, 14)], soft=0.8) * 0.9, out=pine)
    rngp = np.random.default_rng(seed + 77)
    Uw, Vw = X[sl] * ux + Z[sl] * uz, -X[sl] * uz + Z[sl] * ux
    mm = np.zeros_like(Uw)
    for i in range(34):                                                   # each pad of needles throws a long oval along the light
        hgt = rngp.uniform(760.0, 1180.0)
        side = rngp.normal(0, 120.0)
        cxw, czw = x0_ + SUN[0] * hgt - uz * side, z0_ + SUN[1] * hgt + ux * side
        a_, b_ = rngp.uniform(90.0, 170.0), rngp.uniform(40.0, 80.0)
        e_ = ((Uw - (cxw * ux + czw * uz)) / a_) ** 2 + ((Vw - (-cxw * uz + czw * ux)) / b_) ** 2
        np.maximum(mm, np.clip((1 - e_) * 30.0, 0, 1), out=mm)
    for i in range(40):                                                   # smaller pads at its edge: the scallops
        hgt = rngp.uniform(760.0, 1180.0)
        side = rngp.normal(-60, 150.0)
        cxw, czw = x0_ + SUN[0] * hgt - uz * side, z0_ + SUN[1] * hgt + ux * side
        a_, b_ = rngp.uniform(40.0, 80.0), rngp.uniform(20.0, 36.0)
        e_ = ((Uw - (cxw * ux + czw * uz)) / a_) ** 2 + ((Vw - (-cxw * uz + czw * ux)) / b_) ** 2
        np.maximum(mm, np.clip((1 - e_) * 30.0, 0, 1), out=mm)
    # the body of it: everything on the far side of the crown's middle line is shade (it lies off the frame's left)
    cxw0, czw0 = x0_ + SUN[0] * 960.0, z0_ + SUN[1] * 960.0
    body = np.clip(((-(Uw - (cxw0 * ux + czw0 * uz)) / 120.0) * 0 + (-(Vw - (-cxw0 * uz + czw0 * ux)) - 40.0) / 30.0), 0, 1)
    body = body * np.clip(1 - np.abs(Uw - (cxw0 * ux + czw0 * uz)) / 260.0, 0, 1) ** 0.3
    mm = np.maximum(mm, body)
    fleck = step(0.70, 0.74, FAR.world_noise(X, Z, (70, 50), seed + 72, 2))[sl]
    pine[sl] = np.maximum(pine[sl], mm * (1 - fleck * 0.85))
    pine = (blur(pine, 0.5) * gm).astype(F32)
    glaze(pic, pine, SHADE_PINES, 0.52)
    info["pine_shade"] = pine
    return np.maximum(sh, pine)


def add_(c, a, b):
    """A place a cm along the road's line and b cm toward the bay's side from c."""
    return (c[0] + U[0] * a + NL[0] * b, c[1] + U[1] * a + NL[1] * b)


def water_region(info):
    """Where the bay is seen: below the horizon, above the far edge of the ground, not on Satta."""
    x, y = grid(SHAPE)
    return ((y > HZ - 0.5) * (1 - info["satta"]) * (1 - ground_region())).astype(F32)


def under(seed=SEED):
    info = {}
    pic = FAR.paint_sky(seed)
    info["sky"] = pic.copy()
    info["fuji"], info["snow"] = FAR.paint_fuji(pic, seed)
    info["farland"] = FAR.paint_far_land(pic, seed)
    info["satta"], info["satta_line"] = FAR.paint_satta(pic, seed)
    info["water"] = FAR.paint_bay(pic, seed, water_region(info))
    info.update(paint_ground(pic, seed))
    info["bank"] = climb_bank(pic, seed)
    info["shadow"] = cast_shadows(pic, info, seed)
    land.haze(pic, HZ, HORIZON_C, 0.22, 0.10, info["ground"])
    return np.clip(pic, 0, 1).astype(F32), info


def wet_mask(info):
    """What was laid wet in wet (watercolor.wash's `soft`): the sky, Fuji, the far land, Satta a little, the open water
    (less toward the wall). Everything standing in the play is wet on dry: crisp."""
    x, y = grid(SHAPE)
    m = (y < HZ + 1).astype(F32)
    m = m * (1 - 0.35 * info["fuji"]) * (1 - 0.50 * info["farland"]) * (1 - 0.70 * info["satta"])
    water = info["water"] * np.clip(1.0 - (y - HZ) / 100.0, 0.25, 1.0) * 0.75
    return np.clip(np.maximum(m, water), 0, 1).astype(F32)


# ================================================================ pass 3: the crisp things of the backdrop, wet on dry
def pebbles(L, zone, seed, per_m2, size=(5.0, 14.0), bounds=(-1500, 1800, 600, 2600), tones=None):
    tones = tones or (thin(PRUSSIAN, 0.74), thin(PRUSSIAN, 0.58), thin(lerp(PRUSSIAN, OCHRE, 0.25), 0.50), thin(PRUSSIAN, 0.40))
    for (px_, py_, kk, r) in D.scatter(lambda X_, Z_: P(X_, Z_), lambda X_, Z_: k(Z_), bounds, per_m2, seed, size=(size[1], size[1] * 0.6), zone=zone, most=2600):
        s = (size[0] + (size[1] - size[0]) * r * r) * kk * 0.5
        if s < 0.3:
            continue
        ry = s * (0.42 + 0.5 * T.squash(py_))
        c = tones[int(r * 977) % len(tones)]
        L.ellipse(px_ + s * 0.9, py_ + ry * 0.2, s * 1.15, max(0.4, ry * 0.7), lerp(thin(EARTH, 0.2), PRUSSIAN, 0.35), alpha=0.40)
        L.ellipse(px_, py_ - ry * 0.5, s, max(0.45, ry), thin(c, 0.35), lerp(c, PRUSSIAN, 0.25), g=((px_ - s, py_ - ry), (px_ + s, py_ + ry)))
    return L


def footprints(L, path, seed, stride=68.0, wide=17.0, strength=1.0, scatter_=6.0):
    """A line of footprints along a way (ground places), left, right, left: small hollows, a shaded lip toward the sun."""
    rng = np.random.default_rng(seed)
    pts = []
    for (x0, z0), (x1, z1) in zip(path[:-1], path[1:]):
        dd = math.hypot(x1 - x0, z1 - z0)
        n = max(1, int(dd / stride))
        for i in range(n):
            f = (i + rng.uniform(-0.12, 0.12)) / n
            pts.append((x0 + (x1 - x0) * f, z0 + (z1 - z0) * f, (z1 - z0) / dd, -(x1 - x0) / dd))
    for i, (wx_, wz_, nx_, nz_) in enumerate(pts):
        side = 1 if i % 2 else -1
        fx_, fz_ = wx_ + nx_ * side * wide / 2 + rng.normal(0, scatter_), wz_ + nz_ * side * wide / 2 + rng.normal(0, scatter_)
        kk = k(fz_)
        px_, py_ = P(fx_, fz_)
        rx = 7.0 * kk
        if rx < 0.45 or not (0 < px_ < W and HZ < py_ < H):
            continue
        ry = max(0.4, 10.0 * kk * T.squash(py_) * 1.4)
        a = strength * min(1.0, 0.35 + kk * 0.7) * rng.uniform(0.6, 1.0)
        L.ellipse(px_ + rx * 0.45, py_ + ry * 0.3, rx, ry, WPAPER, alpha=0.32 * a)
        L.ellipse(px_, py_, rx, ry, lerp(thin(EARTH, 0.2), PRUSSIAN, 0.32), alpha=0.50 * a)
    return L


def trample(L, places, seed, n=40, spread=120.0, strength=0.8):
    rng = np.random.default_rng(seed)
    for (cx_, cz_) in places:
        for _ in range(n):
            fx_, fz_ = cx_ + rng.normal(0, spread), cz_ + rng.normal(0, spread * 0.8)
            kk = k(fz_)
            px_, py_ = P(fx_, fz_)
            rx = 7.0 * kk
            if rx < 0.45 or not (0 < px_ < W and HZ < py_ < H):
                continue
            ry = max(0.4, 10.0 * kk * T.squash(py_) * 1.4)
            a = strength * min(1.0, 0.35 + kk * 0.7) * rng.uniform(0.5, 1.0)
            L.ellipse(px_ + rx * 0.45, py_ + ry * 0.3, rx, ry, WPAPER, alpha=0.30 * a)
            L.ellipse(px_, py_, rx, ry, lerp(thin(EARTH, 0.2), PRUSSIAN, 0.30), alpha=0.48 * a)
    return L


def tuft(L, px_, py_, kk, r, seed, tall=22.0, green=None):
    """A tuft of coarse grass: a fan of blades, darker at the foot, the tips catching the light on the left."""
    rng = np.random.default_rng(seed)
    dark = green or thin(lerp(mixp(VIRIDIAN, OCHRE, 0.45), PRUSSIAN, 0.12), 0.12)
    lit_c = thin(mixp(VERONESE, OCHRE, 0.45), 0.30)
    hgt = tall * (0.6 + 0.8 * r) * kk
    if hgt < 1.0:
        return
    L.ellipse(px_ + hgt * 0.55, py_ + 0.4, hgt * 0.7, max(0.5, hgt * 0.16), lerp(thin(EARTH, 0.2), PRUSSIAN, 0.25), alpha=0.32)
    n = 5 + int(r * 5)
    for j in range(n):
        an = math.radians(rng.uniform(-48, 48))
        ln = hgt * rng.uniform(0.6, 1.0)
        tip = (px_ + math.sin(an) * ln, py_ - math.cos(an) * ln)
        mid = (px_ + math.sin(an) * ln * 0.45 - 0.6, py_ - math.cos(an) * ln * 0.55)
        L.taper([(px_ + rng.normal(0, hgt * 0.08), py_), mid, tip], lit_c if an < -0.1 and j % 2 else dark, max(0.6, hgt * 0.10), 0.3, alpha=0.9)


def satta_foot(L, info, seed):
    """Mount Satta's foot behind the mound and the climb: the slope's shrubs and young pines as dabs, darker and firmer
    than the far slope above them (it is near), the cut bank of the climb's far side."""
    rng = np.random.default_rng(seed)
    sat = info["satta"]
    thick = noise(SHAPE, (40, 30), seed + 1, 3)
    for _ in range(1400):
        px_, py_ = rng.uniform(520, 800), rng.uniform(250, 452)
        ix, iy = int(px_), int(py_)
        if sat[iy, ix] < 0.5 or rng.random() > thick[iy, ix] ** 2 * 1.2:
            continue
        near = (py_ - 250) / 200.0
        r_ = 1.6 + 3.0 * near * rng.random()
        dk = lerp(thin(mixp(VIRIDIAN, PRUSSIAN, 0.40), 0.10), HORIZON_C, 0.18 * (1 - near))
        lt = lerp(thin(mixp(VERONESE, OCHRE, 0.18), 0.10), HORIZON_C, 0.18 * (1 - near))
        L.ellipse(px_ + r_ * 0.25, py_ + r_ * 0.2, r_ * 1.3, r_ * 0.7, dk, alpha=0.55)
        if rng.random() < 0.35:
            L.ellipse(px_ - r_ * 0.3, py_ - r_ * 0.2, r_ * 0.7, r_ * 0.35, lt, alpha=0.45)
    return L


def details(pic, info, seed=SEED, fast=False):
    """The crisp things of the backdrop, wet on dry: first the far marks, then what lies ON the ground, then what stands,
    far to near, then the grass at the foot of things. Every edge a hand's. -> the backdrop."""
    x, y = grid(SHAPE)
    gm, road = info["ground"], info["road"]
    # ================ the far plane's marks (no line: the distance)
    Lf = Wet(SHAPE)
    FAR.far_marks(Lf, seed + 50)
    FAR.satta_marks(Lf, info, seed + 51)
    FAR.far_boats(Lf)
    satta_foot(Lf, info, seed + 52)
    c_, a_ = Lf.done()
    over(pic, c_, a_ * (1 - gm * (y > 452)))
    # ================ what lies on the ground
    G_ = Wet(SHAPE)
    for i, c in enumerate((-0.55, -0.02, 0.5, -0.30, 0.28)):                    # people's feet along the road, and round its bend
        way = [add(road_mid(s), (-U[1] * 0 + V.road_dir(s)[1] * c * ROAD_W / 2, -V.road_dir(s)[0] * c * ROAD_W / 2)) for s in np.arange(-200 + 37 * i, 1500, 120)]
        footprints(G_, [q for q in way if q[1] > 1200], seed + 110 + i, stride=70.0, strength=0.30, scatter_=9.0)
    trample(G_, [TEA.xz(TEA.L + 120, -120), (KAGO["X"] - 120, KAGO["Z"] - 80), (420, 1330)], seed + 116, n=26, spread=90.0, strength=0.4)
    rng_d = np.random.default_rng(seed + 117)
    for u_ in np.arange(-TEA.over_end, TEA.L + TEA.over_end, 13.0):                 # the drip line's stones
        q = TEA.pt(u_ + rng_d.normal(0, 3), -TEA.over + 6 + rng_d.normal(0, 4))
        kk_ = k(TEA.xz(u_, -TEA.over)[1])
        r_ = rng_d.uniform(3.0, 6.0) * kk_
        if r_ < 0.5:
            continue
        G_.ellipse(q[0] + r_ * 0.5, q[1] + r_ * 0.15, r_ * 1.1, r_ * 0.35, lerp(thin(EARTH, 0.2), PRUSSIAN, 0.4), alpha=0.45)
        G_.ellipse(q[0], q[1] - r_ * 0.15, r_, r_ * 0.45, thin(lerp(PRUSSIAN, OCHRE, 0.25), 0.42), lerp(PRUSSIAN, OCHRE, 0.2), g=((q[0] - r_, q[1] - r_), (q[0] + r_, q[1])))
    over(pic, G_.c, G_.a * gm)
    # ================ what stands, far to near
    L = Wet(SHAPE)
    T.wall(L, seed + 60)
    info["mound_shape"] = T.mound(L, seed + 61)
    info["trunk_shape"], info["fork"] = T.hackberry_trunk(L, seed + 62)
    info["sign_box"] = T.signboard(L, seed + 63)
    T.teahouse(L, info, seed + 64)
    info["bench_pts"] = T.bench(L, seed + 65)
    built_c, built_a = L.done()
    built_c, built_a = hand(built_c, built_a, seed + 66, amount=0.8, cell=18)
    over(pic, built_c, np.clip(built_a, 0, 1))
    info["built"] = np.clip(built_a, 0, 1)
    # ================ the grass at the foot of things, along the road's edges, by the wall, on the verges
    R_ = Wet(SHAPE)
    free = blur(info["built"], 1.5) < 0.12
    d_ = info["d"]
    hw = ROAD_W / 2
    edge = (np.abs(np.abs(d_) - hw - 30) < 40) & (gm > 0.5)
    tufts = D.scatter(lambda X_, Z_: P(X_, Z_), lambda X_, Z_: k(Z_), (-1500, 1800, 600, 2600), 0.85, seed + 140, size=(22, 30), zone=free & edge, most=600)
    tufts += D.scatter(lambda X_, Z_: P(X_, Z_), lambda X_, Z_: k(Z_), (-1500, 1800, 600, 2600), 0.30, seed + 141, size=(22, 30),
                       zone=free & (info["inland"] > 0.4) & (gm > 0.5), most=300)
    wall_band = mask_poly(SHAPE, [P(X_, Z_ - 60) for X_, Z_ in V.WALL] + [P(X_, Z_) for X_, Z_ in V.WALL][::-1]) > 0.5
    tufts += D.scatter(lambda X_, Z_: P(X_, Z_), lambda X_, Z_: k(Z_), (-1500, 900, 1400, 2400), 1.2, seed + 142, size=(20, 26), zone=free & wall_band, most=200)
    tufts.sort(key=lambda p: p[1])
    for i, (px_, py_, kk, r) in enumerate(tufts):
        tuft(R_, px_, py_, kk, r, seed + 150 + i)
    R_.onto(pic)
    return pic


# ================================================================ the cut-outs, the finish, the numbers
def under_colour(back, alpha):
    ys, xs = np.where(alpha > 0.5)
    return np.median(back[ys, xs], axis=0) if len(ys) else EARTH


def cuts(pic, info, fast=False):
    planes = {}
    c, a, info["cloud_outline"] = T.cloud_cut(11, fast)
    planes["cloud"] = (c, a)
    c, a, info["kago_base"], info["kago_seat"] = T.kago_cut(12, EARTH, fast)
    planes["kago"] = (c, a)
    c, a, info["noren_base"] = T.noren_cut(15, T.INSIDE, fast)
    planes["noren"] = (c, a)
    c, a, info["trunks_base"] = T.trunks_cut(13, EARTH, fast)
    planes["trunks"] = (c, a)
    c, a, info["shells"], info["grill_base"] = T.grill_cut(14, EARTH, fast)
    planes["grill"] = (c, a)
    planes["front"] = NEAR.front_cut(16, fast)
    planes["near"] = NEAR.near_cut(17, fast)
    return planes


ORDER = ["cloud", "kago", "noren", "trunks", "grill", "front", "near"]
COUNTS = (("cloud", 24), ("kago", 64), ("noren", 32), ("trunks", 48), ("grill", 64), ("front", 64), ("near", 128))


def to_file(picture, name, colors=128, alpha=None, seed=7, speckle=0.010, amount=0.010):
    """Pigment grain (little: the wash has its own granulation), then a limited palette with speckle: an 8-bit PNG."""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def finish_all(pic, planes, counts, info, out=OUT):
    """THE WATERCOLOUR FINISH (DEPTH.md; Yui's finish_all): the backdrop washed (watercolor.wash), every cut-out washed
    over the unwashed backdrop with the same seed (wash_cut), its own edge kept crisp, so the paper is one sheet; then
    the palette. soft = wet_mask(info); amount 1.0 (daylight); wander 1.4 (the far shore and the capes are thin layers)."""
    soft = wet_mask(info)
    back_washed = WC.wash(pic, seed=SEED, soft=soft, wander=1.4)
    sizes = {"back": to_file(back_washed, out + "/back.png", 250)}
    for name, n in counts:
        c, a = planes[name]
        hard = np.clip(blur((a > 0.3).astype(F32), 1.2) * 2.0, 0, 1)
        washed = WC.wash_cut(c, (a > 0.5).astype(F32), pic, seed=SEED, soft=soft * (1 - hard), wander=1.4, fleck=0.0 if name in ("near", "front") else 0.5)
        planes[name] = (washed, a)
        sizes[name] = to_file(washed, out + f"/{name}.png", n, a)
    return back_washed, sizes


def comp_all(pic, planes, order=ORDER):
    whole = pic.copy()
    for name in order:
        c, a = planes[name][:2]
        over(whole, c, (a > 0.5).astype(F32))
    return whole


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = "fast" in sys.argv
    base, info = under()
    Image.fromarray((base * 255).astype(np.uint8)).save(OUT + "-1-under.png")
    print("under", round(time.time() - t0, 1))
    if fast:
        pic = base.copy()
    else:
        # the brush pass, light: the far plane stays as the wet washes left it, the ground is half brushed
        brushed_ = strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.02, keep=0.0)
        keep = np.clip(0.50 + 0.38 * wet_mask(info), 0, 0.92)
        pic = lerp(brushed_, base, keep[..., None]).astype(F32)
    print("brushed", round(time.time() - t0, 1))
    details(pic, info, fast=fast)
    print("details", round(time.time() - t0, 1))
    planes = cuts(pic, info, fast)
    whole = comp_all(pic, planes)
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-all.png")
    import edo_kurasawa_layout as LAY
    lay_ = LAY.layout(planes, info)
    with open(OUT + "/layout.json", "w") as f:
        json.dump(lay_, f, indent=1)
    with open("out/edo-kurasawa-remap.json", "w") as f:
        json.dump({"points": lay_["remap"]["points"]}, f, indent=1)
    for b in lay_["problems"]:
        print("LAYOUT:", b)
    print("painted", round(time.time() - t0, 1))
    if "wash" in sys.argv or not fast:
        target = OUT if not fast else OUT + "-fast"
        os.makedirs(target, exist_ok=True)
        back_washed, sizes = finish_all(pic, planes, COUNTS, info, target)
        print(sizes)
        comp = Image.open(target + "/back.png").convert("RGBA")
        for name in ORDER:
            comp.alpha_composite(Image.open(f"{target}/{name}.png").convert("RGBA"))
        comp.convert("RGB").save(OUT + ("-comp.png" if not fast else "-fast-comp.png"))
    print("done", round(time.time() - t0, 1))

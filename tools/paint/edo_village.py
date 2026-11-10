"""PAINT-20A: Yui, a post town of the Tokaido on Suruga Bay under the Satta pass, about 8 April 1830, early morning
(edo-village). PAINT-23A (round twenty-three, tools/paint/DEPTH.md): painted again in THREE PLANES, and in WATERCOLOUR
(the act's woodblock drawing laid in washes on paper). The camera, the placings and every number of the scene file are
round twenty's and have not moved.

LIGHT   The sun is in the east, behind us and to the left, 30 degrees up (edo_village_kit.SUN3): faces turned to us and
        to the left are lit; shadows fall to the right and away (kit.SUN), each a cool glaze over the local colour.
DEPTH   horizon 300, full 590 (persp.Camera; everything standing is drawn through it). The eye is 3.2 m up: we stand on
        a grassy bank at the foot of the hill, under a black pine of the shore road.
NEAR    (near.png, front.png: edo_village_near.py) the pine's trunk leaning in up the left side, its boughs across the
        top left; a bough of the next pine in the top right; the bank's lip along the bottom (sasa, a few blades of
        pampas grass, stones); the coil of rope and the floats on its turf. Dark, in the shade of the pines, the
        morning sun along their left edges. People always pass behind it.
MIDDLE  the play, the best lit: the beach (tide lines of wrack and shells, footprints, pebbles), the street (the tracks
        feet and hooves have worn running to its vanishing point: no wheel ruts, nothing wheeled used this road), the
        boats on their trestles, racks, the board, the well, Kihei's shop drawn as a house (posts and beams, boards and
        plaster, a deep eave and its shadow, shingles under stones), the houses down the street overlapping. Every
        standing thing throws its shadow one way; the shade of the pines behind us lies across the bottom of the
        picture, flecked with sun, and its edge leads in. NOTHING NEW STANDS WHERE SOMEBODY CAN WALK BEHIND IT (the
        backdrop is always behind people): new things are flat on the ground, beyond the walk's far end (z 2600), on a
        wall, or in the hen yard.
FAR     (edo_village_far.py) the bay with boats at three distances; the far shore, Fuji's foothills, two capes beyond the
        Satta headland, the headland in two spurs; Fuji, a form, the snow bare paper, a band of cloud across its flank;
        a graded sky with clouds that shrink toward the horizon. Each layer paler toward the sky's colour. No line.
LIGHTS  the lightest light is the paper: Fuji's snow, and in the play the sunlit wall round Kihei's door.
PLACE   The street and the shore run from the lower left away to the right (edo_village_kit: x = a + 0.6 z). Left and
        middle: the beach, the big boat on its props (bottom left), the net racks, Gonroku's tender at the water's edge,
        the bay and, far out, his freighter at anchor; across the bay, Fuji. Right: Kihei's shop, its open front (the
        noren) facing us; the hen yard behind its low bamboo fence in the near right corner; the notice-board place and
        the well on the seaward side of the street; the far roofs of the village; the Satta pass closing the shore at the
        upper right, the shrine path and its cherry at its foot, the road climbing it.
PAPER   watercolor.wash on the backdrop and wash_cut (the same seed) on every cut-out, just before the palette: see
        finish_all(). What was laid wet in wet (WET, the `soft` mask): the sky and its clouds, Fuji, the far land, the
        far spur of the pass, the open water.

  python3 edo_village.py fast        the composition without the brush pass (out/edo-village-1-under.png, -2-all.png)
  python3 edo_village.py fast wash   the same with the paper's finish, to judge the washes (out/edo-village-fast-comp.png)
  python3 edo_village.py             the full passes: out/edo-village/ (back.png, the cut-outs, layout.json), -comp.png
  python3 edo_village_hens.py        then the hens' frames (round twenty's, unchanged: in round twenty's palette)
  python3 install.py edo-village     keys it in the game's paints and installs it; then python3 ../stamp.py
"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
import land
import depth as D
import watercolor as WC
from edo_village_kit import *
import edo_village_kit as K
import edo_village_far as FAR
import edo_village_things as T
from edo_village_far import HORIZON_C

SEED = 1830
OUT = "out/edo-village"
SHAPE = (H, W)

# ---------------------------------------------------------------- where things are (cm; see the module's PLACE)
SHOP = dict(z0=650.0, z1=1150.0, depth=450.0, eave=230.0, ridge=440.0, over=45.0)       # along the street, its near gable to the beach
YARD = dict(x0=230.0, x1=820.0, z0=40.0, z1=330.0, fence=55.0)                            # the hen yard, near right
BOARD = dict(z=1400.0, off=-280.0, w=170.0, post=240.0, roof=300.0)                        # the notice-board place, seaward side
WELL = dict(z=2100.0, off=-300.0, r=45.0, h=70.0)
RACKS = [dict(x=-600.0, z=1000.0, w=300.0, h=170.0), dict(x=-250.0, z=1250.0, w=260.0, h=165.0)]
BIGBOAT = dict(stern=(-900.0, 900.0), length=650.0, beam=75.0, prop=52.0, side=62.0)
TENDER = dict(stern=(-700.0, 1750.0), length=430.0, beam=52.0, prop=0.0, side=45.0)
INLAND = (0.857, -0.514)                                   # the unit vector inland (square to the street), toward us and right
SHIP_AT = (168.0, 318.0)                                   # Gonroku's freighter at anchor, far out (picture place of its waterline middle)
# the houses down the street, far to near: (z0, z1, depth, eave, ridge, over, the line they stand on, lift, thatch)
ROW_A = STREET_A - STREET_W - 400.0                         # the seaward row's street side
HOUSES = [
    (5600.0, 6300.0, 380.0, 200.0, 350.0, 40.0, ROW_A, 0.0, False),
    (4750.0, 5350.0, 400.0, 205.0, 380.0, 45.0, ROW_A, 0.0, True),
    (4000.0, 4550.0, 380.0, 195.0, 345.0, 40.0, ROW_A, 0.0, False),
    (3420.0, 3880.0, 400.0, 210.0, 395.0, 48.0, ROW_A, 0.0, True),
    (2960.0, 3330.0, 370.0, 196.0, 340.0, 40.0, ROW_A, 0.0, False),
    (2500.0, 2900.0, 380.0, 200.0, 360.0, 44.0, ROW_A, 0.0, True),
]
HEN_BASKET = (248.0, 168.0)                                 # a small fusego by the yard's left fence (x, z): left of the first hen's whole run
PT = lambda X, Z: CAM.pt(X, 0.0, Z)
PX = lambda X, Z: CAM.scale(Z)


def inland(x, z, d):
    return x + INLAND[0] * d, z + INLAND[1] * d


def hull(points):
    """The convex outline of some places on the ground (Andrew's chain)."""
    pts = sorted(set((round(float(x), 2), round(float(y), 2)) for x, y in points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


# ================================================================ pass 1: the washes, broad and soft
def paint_ground(pic, seed, wm):
    """The beach (grey sand), the street (packed earth, 30 cm up a sunlit slope of sand) and the open ground on its
    inland side: each a graded wash, pale and cool far off, deeper and warmer toward us, never even. Measured in the
    world, so its drifts and the street's worn tracks shrink with distance and run to the street's vanishing point."""
    x, y = grid(SHAPE)
    X, Z, below = floor(SHAPE)
    ground = below * (1 - wm)
    kpx = CAM.F / (CAM.Z0 + np.maximum(Z, -800.0))
    S0 = X - M * Z                                                    # which line parallel to the street a place is on (cm)
    S = S0 + (world_noise(X, Z, 150, seed + 60, 2) - 0.5) * 30        # the same, its edges wandering a hand's breadth
    e = 1.2 / kpx                                                     # a pixel, in cm
    band = lambda a, b: step(a - e, a + e, S) * (1 - step(b - e, b + e, S))
    street = band(STREET_A - STREET_W, STREET_A + STREET_W)
    slope = band(STREET_A - STREET_W - 96.0, STREET_A - STREET_W)
    inl = step(STREET_A + STREET_W - e, STREET_A + STREET_W + e, S)
    t = np.clip((y - HZ) / float(H - HZ), 0, 1) ** 0.85
    # ---- the beach
    sand = ramp(t, [(0.0, lerp(HORIZON_C, SAND, 0.40)), (0.28, thin(lerp(SAND, OCHRE, 0.07), 0.36)), (0.66, thin(lerp(SAND, OCHRE, 0.11), 0.17)),
                    (1.0, lerp(SAND, mixp(OCHRE, PRUSSIAN, 0.42), 0.22))])
    sand *= (1 + ((world_noise(X, Z, 190, seed + 30, 3) - 0.5) * 0.13 + (world_noise(X, Z, 38, seed + 31, 2) - 0.5) * 0.08)[..., None])
    k_ = (world_noise(X, Z, 420, seed + 32, 2) - 0.5) * 0.045         # warmer here, cooler there
    sand[..., 0] += k_
    sand[..., 2] -= k_
    over(pic, np.clip(sand, 0, 1), ground)
    # wet sand above the water's edge (the tide went out an hour ago): a cool glaze, and the sky's light in it at the edge
    wet = np.clip(1 - (S0 - SHORE_A) / 250.0, 0, 1) * (S0 > SHORE_A) * ground
    tint(pic, thin(mixp(COBALT, PRUSSIAN, 0.22), 0.42), (wet ** 0.8 * 0.72).astype(F32))
    over(pic, HORIZON_C, (np.clip(1 - (S0 - SHORE_A) / 54.0, 0, 1) * (S0 > SHORE_A) * ground * 0.34).astype(F32))
    # ---- the open ground inland of the street: sandy earth, grass coming up in it in patches
    lot = lerp(sand, ramp(t, [(0.0, lerp(HORIZON_C, EARTH, 0.4)), (0.4, thin(EARTH, 0.34)), (1.0, lerp(EARTH, PRUSSIAN, 0.10))]), 0.46)
    lot *= (1 + ((world_noise(X, Z, 120, seed + 36, 3) - 0.5) * 0.12)[..., None])
    over(pic, np.clip(lot, 0, 1), (inl * ground).astype(F32))
    grass = step(0.56, 0.78, world_noise(X, Z, 230, seed + 37, 3)) * step(STREET_A + STREET_W + 60, STREET_A + STREET_W + 200, S) * ground
    tint(pic, thin(mixp(VERONESE, OCHRE, 0.18), 0.45), (grass * 0.36 * inl).astype(F32))
    # ---- the street: the Tokaido, packed earth; three tracks worn pale by feet and hooves, its middle and edges rougher
    earth = ramp(t, [(0.0, lerp(HORIZON_C, EARTH, 0.42)), (0.28, thin(EARTH, 0.40)), (0.66, thin(EARTH, 0.20)), (1.0, lerp(EARTH, SIENNA, 0.10))])
    across = (S0 - STREET_A) / STREET_W
    wander = (world_noise(X, Z, (70, 1100), seed + 34, 2, street=True) - 0.5) * 0.30
    track = sum(np.exp(-((across - c - wander) / 0.17) ** 2) for c in (-0.52, 0.03, 0.55))
    earth = lerp(earth, thin(EARTH, 0.84), (np.clip(track, 0, 1) * 0.62)[..., None])
    earth *= (1 + ((world_noise(X, Z, (28, 600), seed + 35, 3, street=True) - 0.5) * 0.14 + (world_noise(X, Z, 90, seed + 38, 2) - 0.5) * 0.07)[..., None])
    rough = step(0.74, 1.0, np.abs(across)) * 0.20 + np.exp(-((across - 0.29 - wander) / 0.07) ** 2) * 0.12 + np.exp(-((across + 0.25 - wander) / 0.07) ** 2) * 0.12
    earth *= (1 - rough[..., None])
    over(pic, np.clip(earth, 0, 1), (street * ground).astype(F32))
    # ---- the slope of sand from the beach up to the street: it faces the sea and the sun, the lightest of the ground
    bank = thin(lerp(SAND, OCHRE, 0.10), 0.62)
    over(pic, bank, (slope * ground * 0.85).astype(F32))
    tint(pic, thin(mixp(OCHRE, PRUSSIAN, 0.5), 0.45), (band(STREET_A - STREET_W - 6.0, STREET_A - STREET_W + 12.0) * ground * 0.5).astype(F32))    # the street's crumbling edge
    # ---- worn ways: up from the beach to the street, and from the street to Kihei's door and the yard's corner
    for pts_w, wd in (([(-650, 500), (-480, 420), (-330, 330)], 70.0), ([(-170, 420), (40, 560), (250, 640), (380, 600)], 80.0), ([(-900, 700), (-760, 620), (-660, 560)], 60.0)):
        m = mask_line(SHAPE, [gp(x_, z_) for x_, z_ in pts_w], [wd * kz(z_) for x_, z_ in pts_w], soft=3.0) * ground
        over(pic, thin(EARTH, 0.72), (m * 0.34).astype(F32))
    return ground, (street * ground).astype(F32), dict(S=S0, across=across, slope=slope * ground, inland=inl * ground, kpx=kpx)


def box_shadow(foot, height, extra=()):
    """The shadow on the ground of an upright thing with a level top: the outline of its foot and of its top laid
    along the sun (kit.SUN). `foot`: ground places (x, z); `extra`: higher points (x, y, z), a ridge. -> picture points."""
    pts = [(fx, fz) for fx, fz in foot] + [(fx + SUN[0] * height, fz + SUN[1] * height) for fx, fz in foot]
    pts += [(ex + SUN[0] * ey, ez + SUN[1] * ey) for ex, ey, ez in extra]
    return [gp(px, pz) for px, pz in hull(pts)]


def cast_shadows(pic, ground, seed, extra):
    """Every standing thing's shadow, one way (to the right and away), as a glaze over the ground; and the shade of the
    pines that stand behind us and to our left, out of the picture, lying across its bottom, dappled, its edge running
    in along the light. -> the shadow's mask."""
    x, y = grid(SHAPE)
    X, Z, below = floor(SHAPE)
    sh = np.zeros(SHAPE, dtype=F32)

    def add(pts, amount=0.9, soft=0.7, wobble=0.8, s=0):
        if len(pts) >= 3:
            np.maximum(sh, mask_poly(SHAPE, pts, soft=soft, wobble=wobble, seed=seed + s) * amount, out=sh)
    # the houses down the street: their shadows lie across it, toward the inland row
    for i, (z0, z1, depth, eave, ridge, ov, a, lift, thatch) in enumerate(HOUSES):
        F0, F1 = (a + M * z0, z0), (a + M * z1, z1)
        foot = [F0, F1, inland(*F1, depth), inland(*F0, depth)]
        mid = (((F0[0] + F1[0]) / 2 + INLAND[0] * depth / 2), ridge, ((F0[1] + F1[1]) / 2 + INLAND[1] * depth / 2))
        add(box_shadow(foot, eave, [mid]), 0.85, s=i)
    # Kihei's shop (most of its shadow lies behind it)
    F0, F1 = (front_x(SHOP["z0"]), SHOP["z0"]), (front_x(SHOP["z1"]), SHOP["z1"])
    add(box_shadow([F0, F1, inland(*F1, SHOP["depth"]), inland(*F0, SHOP["depth"])], SHOP["eave"]), 0.9, s=11)
    # the hen yard's fence: its rails and posts, thin
    for (xa, za, xb, zb) in ((YARD["x0"], YARD["z0"], YARD["x0"], YARD["z1"]), (YARD["x0"], YARD["z1"], YARD["x1"], YARD["z1"])):
        for hgt in (0.3, 0.6, 0.92):
            hh = YARD["fence"] * hgt
            line = mask_line(SHAPE, [gp(xa + SUN[0] * hh, za + SUN[1] * hh), gp(xb + SUN[0] * hh, zb + SUN[1] * hh)], [max(1.0, 5 * kz(za)), max(1.0, 5 * kz(zb))], soft=0.5)
            np.maximum(sh, line * 0.7, out=sh)
        n = max(2, int(math.hypot(xb - xa, zb - za) / 110))
        for i in range(n + 1):
            px_, pz_ = xa + (xb - xa) * i / n, za + (zb - za) * i / n
            hh = YARD["fence"] + 6
            line = mask_line(SHAPE, [gp(px_, pz_), gp(px_ + SUN[0] * hh, pz_ + SUN[1] * hh)], max(1.2, 6 * kz(pz_)), soft=0.5)
            np.maximum(sh, line * 0.75, out=sh)
    # the board's place: its platform, posts, boards and roof
    bz = BOARD["z"]
    bx = street_x(bz, 0) + BOARD["off"]
    hw = BOARD["w"] / 2 + 20
    add(box_shadow([(bx - 0.514 * hw, bz - 0.857 * hw), (bx + 0.514 * hw, bz + 0.857 * hw), inland(bx + 0.514 * hw, bz + 0.857 * hw, 30), inland(bx - 0.514 * hw, bz - 0.857 * hw, 30)], BOARD["post"] + 30), 0.85, s=21)
    # the racks: the nets let a little light through
    for i, r in enumerate(RACKS):
        x1, z1 = r["x"] + r["w"] * 0.76, r["z"] + r["w"] * 0.64
        add(shadow_pts([(r["x"], 0, r["z"]), (x1, 0, z1), (x1, r["h"], z1), (r["x"], r["h"], r["z"])]), 0.62, s=30 + i)
    # the well and its roof
    wz = WELL["z"]
    wx = street_x(wz) + WELL["off"]
    add(box_shadow([(wx - WELL["r"], wz - 36), (wx + WELL["r"], wz - 36), (wx + WELL["r"], wz + 36), (wx - WELL["r"], wz + 36)], WELL["h"]), 0.85, s=40)
    add(shadow_pts([(wx - 60, 226, wz), (wx + 60, 226, wz), (wx, 268, wz)]), 0.8, s=41)
    # the boats: under the hull and beyond it
    for i, b in enumerate((BIGBOAT, TENDER)):
        sx_, sz_ = b["stern"]
        ex, ez = inland(sx_, sz_, b["length"])
        top = b["prop"] + b["side"]
        add(shadow_pts([(sx_, top, sz_), (ex, top + 30, ez), (ex, b["prop"], ez), (sx_, b["prop"], sz_)]), 0.9, s=50 + i)
        add(shadow_pts([(sx_ - 0.514 * b["beam"], top, sz_ - 0.857 * b["beam"]), (ex, top, ez), (ex, 0, ez), (sx_ - 0.514 * b["beam"], 0, sz_ - 0.857 * b["beam"])]), 0.9, s=52 + i)
        add(shadow_pts([(sx_ + 0.514 * b["beam"], top, sz_ + 0.857 * b["beam"]), (ex, top, ez), (ex, 0, ez), (sx_ + 0.514 * b["beam"], 0, sz_ + 0.857 * b["beam"])]), 0.9, s=54 + i)
    # one of the shore pines that stand out of the picture on the left: its trunk's long shadow comes in across the beach
    # and the road, and its crown's lies on the road beyond, in ovals
    x0_, z0_ = -640.0, 396.0
    tr = [gp(x0_ + SUN[0] * t_ + 10 * math.sin(t_ / 60.0), z0_ + SUN[1] * t_) for t_ in np.linspace(-60, 330, 12)]
    np.maximum(sh, mask_line(SHAPE, tr, [max(1.2, 30 * kz(z0_ + SUN[1] * t_) * (1 - 0.0012 * t_)) * 0.33 for t_ in np.linspace(-60, 330, 12)], soft=0.7) * 0.8, out=sh)
    rngc = np.random.default_rng(seed + 81)
    cx0, cz0 = x0_ + SUN[0] * 420.0, z0_ + SUN[1] * 420.0
    for i in range(16):
        ox, oz = rngc.normal(0, 150.0), rngc.normal(0, 60.0)
        a_, b_ = rngc.uniform(60.0, 130.0), rngc.uniform(28.0, 55.0)
        ux_, uz_ = SUN[0] / math.hypot(*SUN), SUN[1] / math.hypot(*SUN)
        pts_o = [gp(cx0 + ox + ux_ * a_ * math.cos(t_) - uz_ * b_ * math.sin(t_), cz0 + oz + uz_ * a_ * math.cos(t_) + ux_ * b_ * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 14)[:-1]]
        add(pts_o, 0.78, soft=0.8, wobble=0.6, s=90 + i)
    # whatever else the details stand on the ground (edo_village.details gives their outlines)
    for i, pts in enumerate(extra):
        add(pts, 0.8, s=60 + i)
    sh = (sh * ground).astype(F32)
    glaze(pic, sh, SHADE, 1.0)
    # ---- the shade of the pines behind us: everything nearer than a line that runs in along the light. Its edge is the
    # outline of their crowns, in big scallops; the sun comes through the boughs in flecks, most of them near the edge;
    # a few flecks of shade lie out beyond it.
    slope_ = SUN[1] / SUN[0]
    edge = 128.0 + (X + 330.0) * slope_                                   # the shade's edge: z on it at each x (cm)
    d = (edge - Z) / 100.0                                                # metres inside the shade
    rngp = np.random.default_rng(seed + 77)
    sl = slice(460, H)                                                    # (the rows it can lie in)
    ln_ = math.hypot(*SUN)
    ux, uz = SUN[0] / ln_, SUN[1] / ln_                                   # along the light, on the ground
    Uw, Vw = X[sl] * ux + Z[sl] * uz, -X[sl] * uz + Z[sl] * ux
    m = np.zeros_like(Uw)
    for i in range(190):                                                  # each pad of needles throws a long oval, lying along the light
        cxw = rngp.uniform(-800.0, 300.0)
        deep = rngp.exponential(1.2) - 1.0                                # metres inside the edge (a few lie out beyond it)
        czw = 128.0 + (cxw + 330.0) * slope_ - deep * 100.0
        a_, b_ = rngp.uniform(80.0, 190.0), rngp.uniform(38.0, 80.0)
        e_ = ((Uw - (cxw * ux + czw * uz)) / a_) ** 2 + ((Vw - (-cxw * uz + czw * ux)) / b_) ** 2
        np.maximum(m, np.clip((1 - e_) * 4.0, 0, 1), out=m)
    solid = step(1.5, 2.2, d[sl])                                         # deep inside it is all shade
    fleck = step(0.62, 0.68, world_noise(X, Z, (62, 44), seed + 72, 2))[sl] * np.clip(1.0 - (d[sl] - 1.2) / 3.0, 0.15, 1)      # the sun through the boughs
    pines = np.zeros(SHAPE, dtype=F32)
    pines[sl] = np.clip(np.maximum(m, solid) * (1 - fleck * 0.9), 0, 1)
    pines = pines * (1 - step(110.0, 240.0, X)) * below
    pines = (blur(pines.astype(F32), 0.6) * ground).astype(F32)
    glaze(pic, pines, SHADE_PINES, 0.96)
    return np.maximum(sh, pines)


def under(seed=SEED):
    info = {}
    pic = FAR.paint_sky(seed)
    info["clouds"] = FAR.paint_clouds(pic, seed)
    info["sky"] = pic.copy()
    info["fuji"], info["snow"] = FAR.paint_fuji(pic, seed)
    info["cloud2"] = FAR.paint_fuji_cloud(pic, seed)
    info["farland"] = FAR.paint_far_land(pic, seed)
    info["pass"], info["pass_line"], info["spur"], info["spur_line"] = FAR.paint_pass(pic, seed)
    info["water"] = FAR.paint_bay(pic, seed)
    info["ground"], info["street"], info["parts"] = paint_ground(pic, seed, info["water"])
    return np.clip(pic, 0, 1), info


def wet_mask(info):
    """What was laid wet in wet (watercolor.wash's `soft`): the sky and its clouds, Fuji, the far land, the far spur of
    the pass, the open water (less toward the shore). Everything standing in the play is wet on dry: crisp."""
    x, y = grid(SHAPE)
    sky = (y < HZ + 1).astype(F32)
    m = sky * 1.0
    m = m * (1 - 0.35 * info["fuji"])                                   # the mountain's own edges a little firmer than the sky's
    m = m * (1 - 0.50 * info["farland"])                                # the far shore and the capes: thin layers, they must not run together
    m = m * (1 - 0.45 * info["pass"]) * (1 - 0.40 * info["spur"])       # the headland firmer, its near spur firmer again
    water = info["water"] * np.clip(1.0 - (y - HZ) / 120.0, 0.25, 1.0) * 0.75
    return np.clip(np.maximum(m, water), 0, 1).astype(F32)


# ================================================================ pass 3: the crisp things (the backdrop's)
def tide_lines(L, seed):
    """The tide's lines along the shore: wrack and broken shell left where each tide turned, three of them, the highest
    the heaviest. Never a ruled row: it lies in clumps with bare sand between, and wanders as the last wave did. Dots
    and dashes, measured in the world: big and few near us, a thread far off."""
    rng = np.random.default_rng(seed)
    weed, weed2 = mixp(VIRIDIAN, PRUSSIAN, 0.55), mixp(SIENNA, PRUSSIAN, 0.50)
    zk = np.arange(600.0, 9400.0, 110.0)
    for (off, per_m, spread) in ((92.0, 6.0, 9.0), (236.0, 4.0, 13.0), (452.0, 9.0, 24.0)):
        wander = np.cumsum(rng.normal(0, 13.0, len(zk)))
        wander -= np.linspace(wander[0], wander[-1], len(zk))                 # (it comes back to its own line)
        clump = np.clip(rng.normal(0.9, 0.9, len(zk)), 0.05, 3.0)              # how much lies here
        z = 640.0
        while z < 9000.0:
            k = kz(z)
            dens = float(np.interp(z, zk, clump))
            z += rng.exponential(100.0 / (per_m * dens)) * (1.0 if k > 0.25 else 0.25 / k)
            px_, py_ = gp(shore_x(z) + off + float(np.interp(z, zk, wander)) + rng.normal(0, spread * (0.6 + dens * 0.4)), z)
            if not (-5 < px_ < W + 5):
                continue
            ln = rng.uniform(3, 15) * k
            if ln < 0.35:
                continue
            a = (0.30 + 0.5 * rng.random()) * min(1.0, 0.45 + k)
            if rng.random() < 0.20:                                           # a shell, or a bleached stick: the paper
                L.ellipse(px_, py_, max(0.6, ln * 0.35), max(0.5, ln * 0.2), WPAPER, alpha=min(1.0, a + 0.3))
            else:
                tilt = rng.normal(0, 0.9) * squash(py_) * 2.0
                L.line([(px_ - ln / 2, py_ - tilt), (px_ + ln / 2, py_ + tilt)], weed if rng.random() < 0.6 else weed2, max(0.5, rng.uniform(1.6, 3.4) * k), a)
    return L


def pebbles(L, zone, seed, per_m2, size=(5.0, 14.0), bounds=(-2700, 1500, -40, 5200), tones=None):
    """Stones lying on the ground at a true density (depth.scatter): each a touch with a light top and its little
    shadow to the right."""
    tones = tones or (thin(PRUSSIAN, 0.74), thin(PRUSSIAN, 0.58), thin(lerp(PRUSSIAN, OCHRE, 0.25), 0.50), thin(PRUSSIAN, 0.40))
    for (px_, py_, k, r) in D.scatter(PT, PX, bounds, per_m2, seed, size=(size[1], size[1] * 0.6), zone=zone, most=2600):
        s = (size[0] + (size[1] - size[0]) * r * r) * k * 0.5
        if s < 0.3:
            continue
        ry = s * (0.42 + 0.5 * squash(py_))
        c = tones[int(r * 977) % len(tones)]
        L.ellipse(px_ + s * 0.8, py_ + ry * 0.25, s * 1.15, max(0.4, ry * 0.7), lerp(SAND_SHADE, PRUSSIAN, 0.2), alpha=0.42)
        L.ellipse(px_, py_ - ry * 0.5, s, max(0.45, ry), thin(c, 0.35), lerp(c, PRUSSIAN, 0.25), g=((px_ - s, py_ - ry), (px_ + s, py_ + ry)))
    return L


def footprints(L, path, seed, stride=68.0, wide=17.0, strength=1.0, scatter_=6.0):
    """A line of footprints along a way on the ground (world places): left, right, left, each a small hollow with its
    shaded lip toward the sun and a light lip beyond."""
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
        k = kz(fz_)
        px_, py_ = gp(fx_, fz_)
        rx = 7.5 * k
        if rx < 0.45 or not (0 < px_ < W and HZ < py_ < H):
            continue
        ry = max(0.4, 10.0 * k * squash(py_) * 1.4)
        a = strength * min(1.0, 0.35 + k * 0.7) * rng.uniform(0.6, 1.0)
        L.ellipse(px_ + rx * 0.45, py_ + ry * 0.3, rx, ry, WPAPER, alpha=0.40 * a)
        L.ellipse(px_, py_, rx, ry, lerp(SAND_SHADE, PRUSSIAN, 0.30), alpha=0.60 * a)
    return L


def tuft(L, px_, py_, k, r, seed, tall=19.0, green=None):
    """A tuft of coarse grass: a fan of blades, darker at the foot, the tips catching the light on the left."""
    rng = np.random.default_rng(seed)
    dark = green or thin(lerp(mixp(VIRIDIAN, OCHRE, 0.45), PRUSSIAN, 0.12), 0.12)
    lit_c = thin(mixp(VERONESE, OCHRE, 0.45), 0.30)
    hgt = tall * (0.6 + 0.8 * r) * k
    if hgt < 1.0:
        return
    L.ellipse(px_ + hgt * 0.5, py_ + 0.4, hgt * 0.7, max(0.5, hgt * 0.16), lerp(SAND_SHADE, PRUSSIAN, 0.2), alpha=0.35)
    n = 5 + int(r * 5)
    for j in range(n):
        an = math.radians(rng.uniform(-48, 48))
        ln = hgt * rng.uniform(0.6, 1.0)
        tip = (px_ + math.sin(an) * ln, py_ - math.cos(an) * ln)
        mid = (px_ + math.sin(an) * ln * 0.45 - 0.6, py_ - math.cos(an) * ln * 0.55)
        L.taper([(px_ + rng.normal(0, hgt * 0.08), py_), mid, tip], lit_c if an < -0.1 and j % 2 else dark, max(0.6, hgt * 0.10), 0.3, alpha=0.9)


def woods(L, info, seed):
    """The headland's woods: the crowns of trees as dabs laid wet on dry over its washes, thick in the folds and on
    the near spur, thin and pale on the far one; a grove of bamboo, lighter, by the village."""
    rng = np.random.default_rng(seed)
    near_m, far_m = info["spur"], info["pass"]
    dark_n, lit_n = T.aired(mixp(VIRIDIAN, PRUSSIAN, 0.34), 3000), T.aired(thin(mixp(VERONESE, OCHRE, 0.16), 0.06), 3000)
    dark_f, lit_f = T.aired(thin(mixp(VIRIDIAN, COBALT, 0.30), 0.10), 7000), T.aired(thin(mixp(VERONESE, CERULEAN, 0.2), 0.2), 7000)
    thick = noise(SHAPE, (34, 46), seed + 1, 3)
    dabs = []
    for _ in range(2600):
        px_, py_ = rng.uniform(516, 800), rng.uniform(166, 301)
        ix, iy = int(px_), int(py_)
        if near_m[iy, ix] > 0.5:
            if rng.random() < 0.25 + 0.75 * thick[iy, ix]:
                dabs.append((py_, px_, rng.uniform(2.6, 5.2), True))
        elif far_m[iy, ix] > 0.5 and rng.random() < 0.10 + 0.5 * thick[iy, ix]:
            dabs.append((py_, px_, rng.uniform(1.6, 3.4), False))
    for (py_, px_, r_, near) in sorted(dabs):
        dk, lt = (dark_n, lit_n) if near else (dark_f, lit_f)
        L.ellipse(px_ + r_ * 0.25, py_ + r_ * 0.2, r_, r_ * 0.72, dk, alpha=0.78 if near else 0.5)
        L.ellipse(px_ - r_ * 0.2, py_ - r_ * 0.2, r_ * 0.62, r_ * 0.42, lt, alpha=0.7 if near else 0.45)
    for (cx_, cy_) in ((628, 292), (642, 286), (760, 268), (774, 258), (790, 270)):          # bamboo: a pale, feathery grove
        for _ in range(7):
            bx_, by_ = cx_ + rng.normal(0, 5), cy_ + rng.normal(0, 3)
            L.ellipse(bx_, by_, rng.uniform(3, 5), rng.uniform(4, 7), T.aired(thin(mixp(VERONESE, NAPLES, 0.35), 0.18), 3000), alpha=0.6)
    return L


def trample(L, places, seed, n=40, spread=140.0, strength=0.8):
    """Where people have stood about and worked (round the boats, under the racks, before the board and the door): the
    sand is all footprints, this way and that."""
    rng = np.random.default_rng(seed)
    for (cx_, cz_) in places:
        for _ in range(n):
            fx_, fz_ = cx_ + rng.normal(0, spread), cz_ + rng.normal(0, spread * 0.8)
            k = kz(fz_)
            px_, py_ = gp(fx_, fz_)
            rx = 7.5 * k
            if rx < 0.45 or not (0 < px_ < W and HZ < py_ < H):
                continue
            ry = max(0.4, 10.0 * k * squash(py_) * 1.4)
            a = strength * min(1.0, 0.35 + k * 0.7) * rng.uniform(0.5, 1.0)
            L.ellipse(px_ + rx * 0.45, py_ + ry * 0.3, rx, ry, WPAPER, alpha=0.40 * a)
            L.ellipse(px_, py_, rx, ry, lerp(SAND_SHADE, PRUSSIAN, 0.30), alpha=0.60 * a)
    return L


def details(pic, info, seed=SEED, fast=False):
    """The crisp things of the backdrop, wet on dry. First what lies ON the ground (so that whatever stands on it
    covers it rightly); then what stands, far to near; then the grass at the foot of things. Every edge is a hand's:
    the drawn layers are pushed about by under a pixel before they are laid. -> the backdrop."""
    x, y = grid(SHAPE)
    ground, street, parts = info["ground"], info["street"], info["parts"]
    S, across = parts["S"], parts["across"]
    beach = (ground > 0.5) & (S < STREET_A - STREET_W - 100) & (S > SHORE_A + 40)
    lot = (ground > 0.5) & (S > STREET_A + STREET_W + 10)
    edges = (ground > 0.5) & (np.abs(across) > 0.80) & (np.abs(across) < 1.12)
    # ================ what lies on the ground
    G_ = Wet(SHAPE)
    tide_lines(G_, seed + 80)
    # footprints: up the beach from the boats and the racks to the street, along the water, round the board; along the street
    ways = [[(-900, 760), (-720, 640), (-560, 480), (-420, 380)], [(-560, 960), (-640, 760), (-600, 560)], [(-260, 1180), (-420, 900), (-520, 640)],
            [(-820, 1500), (-560, 1380), (-320, 1260)], [(-640, 1720), (-420, 1560), (-230, 1420), (-60, 1300)], [(-1250, 760), (-1050, 980), (-880, 1320), (-720, 1640)],
            [(60, 1320), (300, 1540), (520, 1900)], [(-1500, 420), (-1280, 520), (-1040, 600)], [(-1180, 380), (-960, 300), (-760, 180), (-600, 40)],
            [(-1320, 1020), (-1100, 1200), (-940, 1500), (-800, 1800), (-560, 2300), (-300, 2800)], [(-720, 280), (-800, 520), (-860, 760)]]
    for i, way in enumerate(ways):
        footprints(G_, way, seed + 90 + i, strength=1.15)
    for i, c in enumerate((-0.5, 0.05, 0.55, -0.48, 0.5)):
        way = [(street_x(z, c) + 10 * math.sin(z / 300.0 + i), z) for z in np.arange(-30 + 37 * i, 3000, 150)]
        footprints(G_, way, seed + 110 + i, stride=72.0, strength=0.26, scatter_=9.0)
    trample(G_, [(-640, 820), (-450, 1080), (-760, 620), (-120, 1330), (-560, 1620), (-880, 1080)], seed + 115, n=46)
    trample(G_, [(300, 560), (420, 520)], seed + 116, n=30, spread=110.0, strength=0.5)
    pebbles(G_, beach, seed + 120, 0.9)
    drift = noise(SHAPE, (90, 26), seed + 123, 3) > 0.56                         # and more of them where the sea has sorted them into drifts
    pebbles(G_, beach & drift, seed + 124, 2.4, size=(4.0, 10.0))
    pebbles(G_, lot, seed + 121, 0.35, size=(5.0, 12.0), bounds=(-300, 1500, -40, 3000), tones=(thin(lerp(PRUSSIAN, OCHRE, 0.3), 0.6), thin(lerp(PRUSSIAN, OCHRE, 0.2), 0.45)))
    pebbles(G_, edges, seed + 122, 1.6, size=(4.0, 9.0), bounds=(-900, 1700, -40, 3200), tones=(thin(lerp(PRUSSIAN, OCHRE, 0.35), 0.55), thin(PRUSSIAN, 0.5)))
    pebbles(G_, (street > 0.5), seed + 125, 0.30, size=(3.0, 7.0), bounds=(-900, 1900, -40, 3400), tones=(thin(lerp(PRUSSIAN, OCHRE, 0.45), 0.5), thin(lerp(PRUSSIAN, OCHRE, 0.3), 0.4)))
    # the hen yard: where they scratch (small dark dabs), straw, grain; a water dish, clear of where the hens stand
    for (px_, py_, k, r) in D.scatter(PT, PX, (YARD["x0"] + 20, YARD["x1"], YARD["z0"], YARD["z1"] - 20), 3.0, seed + 150, size=(14, 10), most=220):
        if r < 0.45:
            G_.line([(px_ - 6 * k, py_), (px_ + 6 * k, py_ + r)], lerp(SAND_SHADE, PRUSSIAN, 0.3), max(0.5, 2.4 * k), 0.30)
        elif r < 0.8:
            an = r * 40
            G_.line([(px_ - 9 * k * math.cos(an), py_ - 2.5 * k * math.sin(an)), (px_ + 9 * k * math.cos(an), py_ + 2.5 * k * math.sin(an))], thin(THATCH_LIT, 0.25), max(0.5, 1.6 * k), 0.75)
        else:
            G_.ellipse(px_, py_, 2.2 * k, 1.2 * k, WPAPER, alpha=0.8)
    dq = gp(YARD["x0"] + 96, YARD["z1"] - 60)
    kq = kz(YARD["z1"] - 60)
    G_.ellipse(dq[0] + 3, dq[1] + 1.5, 15 * kq, 15 * kq * squash(dq[1]) * 1.25, lerp(SAND_SHADE, PRUSSIAN, 0.3), alpha=0.5)
    G_.ellipse(dq[0], dq[1], 14 * kq, 14 * kq * squash(dq[1]) * 1.25, thin(mixp(SIENNA, OCHRE, 0.4), 0.25), mixp(SIENNA, PRUSSIAN, 0.4), g=((dq[0] - 8, dq[1]), (dq[0] + 8, dq[1])))
    G_.ellipse(dq[0], dq[1] - 0.6, 10.5 * kq, 10.5 * kq * squash(dq[1]) * 1.2, thin(CERULEAN, 0.45))
    over(pic, G_.c, G_.a * ground)
    # ================ what stands, far to near
    L = Wet(SHAPE)
    # ---- the pass: the road climbing it (a pale thread), pines along its skyline (soft, small), its woods
    road = [(566, 296), (610, 282), (640, 268), (628, 258), (668, 244), (704, 228), (690, 220), (736, 204), (770, 190), (796, 182)]
    L.line(road, thin(mixp(NAPLES, OCHRE, 0.3), 0.55), 1.2, 0.7)
    pine_far, pine_far_l = thin(mixp(VIRIDIAN, PRUSSIAN, 0.42), 0.24), thin(mixp(VERONESE, VIRIDIAN, 0.35), 0.25)
    for (px, py_, hgt) in ((560, 284, 9), (596, 266, 11), (636, 240, 12), (676, 218, 11), (712, 200, 13), (748, 184, 12), (780, 176, 14), (622, 250, 8), (696, 208, 9)):
        L.line([(px, py_), (px + 0.6, py_ - hgt)], pine_far, 1.0, 0.9)
        for j, (dx, dy, rx, ry) in enumerate(((-0.3, -0.55, 0.42, 0.14), (0.25, -0.7, 0.4, 0.14), (0.0, -0.9, 0.32, 0.13))):
            L.ellipse(px + dx * hgt, py_ + dy * hgt, rx * hgt, ry * hgt, pine_far)
            L.ellipse(px + dx * hgt - 0.1 * hgt, py_ + dy * hgt - 0.05 * hgt, rx * hgt * 0.6, ry * hgt * 0.5, pine_far_l, alpha=0.7)
    woods(L, info, seed + 55)
    # ---- boats on the bay
    FAR.far_boats(L)
    # ---- the far beach, beyond where anybody walks: boats pulled up, a far rack of nets
    T.beach_boat(L, (shore_x(3600) + 130, 3600), 430.0, 50.0, 46.0, 3600, seed=3)
    T.beach_boat(L, (shore_x(2850) + 60, 2850), 400.0, 48.0, 44.0, 2850, seed=4)       # (its bow beyond where anybody can stand: z 2644)
    T.far_rack(L, shore_x(3050) + 330, 3050, 230.0, 160.0, seed=1)
    # ---- the houses down the street, the farthest first, each overlapping the one beyond; a pine between two of them
    for i, (z0, z1, depth, eave, ridge, ov, a, lift, thatch) in enumerate(HOUSES):
        T.house(L, z0, z1, depth, eave, ridge, ov, a=a, lift=lift, thatch=thatch, level=(1 if i >= 4 else 0), seed=i)
        if i == 2:
            T.pine(L, gp(a + M * 3900 - 120, 3900), 62 * 1.0, 31, lean=0.10, z=3900, tiers=3)
    # the shrine path and its gate; the cherry beside it
    T.shrine_path(L)
    info["cherry_box"] = T.cherry(L)
    # ---- the well, a pine beyond it on the top of the beach
    T.pine(L, gp(shore_x(3300) + 300, 3300), 64.0, 37, lean=-0.08, z=3300, tiers=4, spread=1.1)
    T.well(L, WELL)
    # ---- Kihei's shop: the near house on the right; its open front faces us (the noren is a cut-out)
    info["shop_gable"] = T.house(L, SHOP["z0"], SHOP["z1"], SHOP["depth"], SHOP["eave"], SHOP["ridge"], SHOP["over"], level=2, shop=True, seed=9)
    T.hen_basket(L, HEN_BASKET[0], HEN_BASKET[1], r=15.0, hgt=28.0)           # in the hen yard, clear of where the hens stand
    built_c, built_a = L.done()
    built_c, built_a = warp(built_c, 0.85, 18, seed + 61), warp(built_a, 0.85, 18, seed + 61)      # a hand's lines: nothing ruled for long
    over(pic, built_c, np.clip(built_a, 0, 1))
    info["built"] = np.clip(built_a, 0, 1)
    # ================ the grass at the foot of things: along the top of the sand slope, along the street's inland edge, in
    # the open ground, round the board and the well; never where something built stands in front of its roots
    R_ = Wet(SHAPE)
    free = blur(info["built"], 1.5) < 0.12
    tufts = D.scatter(PT, PX, (-1200, 1700, -40, 3400), 0.6, seed + 130, size=(20, 28), zone=free & (ground > 0.5) & (S > STREET_A - STREET_W - 110) & (S < STREET_A - STREET_W - 30), most=400)
    tufts += D.scatter(PT, PX, (-700, 1900, -40, 3400), 0.5, seed + 131, size=(20, 26), zone=free & (ground > 0.5) & (S > STREET_A + STREET_W + 4) & (S < STREET_A + STREET_W + 46), most=300)
    tufts += D.scatter(PT, PX, (-200, 1500, -40, 1500), 0.07, seed + 132, size=(22, 30), zone=free & lot & (S > STREET_A + STREET_W + 70), most=160)
    bz = BOARD["z"]
    bxw = street_x(bz) + BOARD["off"]
    tufts += [(gp(bxw + dx_, bz + dz_)[0], gp(bxw + dx_, bz + dz_)[1], kz(bz + dz_), rr) for (dx_, dz_, rr) in ((-150, -40, 0.7), (-128, 30, 0.3), (120, 130, 0.5), (146, 96, 0.9), (-20, -130, 0.4))]
    wz = WELL["z"]
    wxw = street_x(wz) + WELL["off"]
    tufts += [(gp(wxw + dx_, wz + dz_)[0], gp(wxw + dx_, wz + dz_)[1], kz(wz + dz_), rr) for (dx_, dz_, rr) in ((-84, -30, 0.8), (-70, 40, 0.4), (80, -50, 0.6))]
    tufts.sort(key=lambda p: p[1])
    for i, (px_, py_, k, r) in enumerate(tufts):
        tuft(R_, px_, py_, k, r, seed + 140 + i)
    R_.onto(pic)
    return pic


def ground_shadows_of_details():
    """The outlines of the shadows of what details() stands on the ground (world -> picture), for cast_shadows."""
    out = []
    for (fx_, fz_, hgt, rad) in ((shore_x(3300) + 300, 3300, 330.0, 150.0), (ROW_A + M * 3900 - 120, 3900, 320.0, 130.0)):       # the two pines: trunk and crown
        out.append([gp(fx_ - 14, fz_), gp(fx_ + 14, fz_), gp(fx_ + 14 + SUN[0] * hgt * 0.6, fz_ + SUN[1] * hgt * 0.6), gp(fx_ - 14 + SUN[0] * hgt * 0.6, fz_ + SUN[1] * hgt * 0.6)])
        cx_, cz_ = fx_ + SUN[0] * hgt * 0.8, fz_ + SUN[1] * hgt * 0.8
        out.append([gp(cx_ + rad * math.cos(t_), cz_ + rad * 0.8 * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 14)[:-1]])
    bx_, bz_ = HEN_BASKET                                                    # the hen basket: a low dome
    out.append(box_shadow([(bx_ - 13, bz_ - 10), (bx_ + 13, bz_ - 10), (bx_ + 13, bz_ + 10), (bx_ - 13, bz_ + 10)], 19.0))
    for (sx_, sz_, ln, hh) in ((shore_x(3600) + 130, 3600, 430.0, 60.0), (shore_x(2850) + 60, 2850, 400.0, 58.0)):                     # the far boats
        ex, ez = inland(sx_, sz_, ln)
        out.append(shadow_pts([(sx_, 0, sz_), (ex, 0, ez), (ex, hh, ez), (sx_, hh, sz_)]))
    return out


# ================================================================ the cut-outs
def boat_cut(back, b, seed, fast=False):
    """A flat-bottomed fishing boat pulled up on two cross timbers, bow inland (toward us and the right): the near side
    a wash of sunlit wood deepening as it turns under, its sheer rising to the bow, the bow planks in shade, the inside
    dark over the gunwale with its thwarts, a net heaped in the stern, an oar laid along; the gap under it open to the
    sand. The key line under it and on its shade side only."""
    L = Wet(SHAPE)
    rng = np.random.default_rng(seed)
    sx_, sz_ = b["stern"]
    Ln, beam, prop, side = b["length"], b["beam"], b["prop"], b["side"]
    n = 16
    near_g, far_g, near_c = [], [], []                                  # the near gunwale, the far gunwale, the near chine
    for i in range(n + 1):
        u = i / n
        cx_, cz_ = inland(sx_, sz_, Ln * u)
        hw = beam * (0.55 + 0.45 * math.sin(math.pi * min(1.0, u * 1.15)) ** 0.7) if u < 0.87 else beam * (1.0 - (u - 0.87) / 0.13) ** 0.6 * 0.9 + 4
        sheer = side + 6 * (1 - u) ** 2 + 46 * max(0.0, u - 0.55) ** 1.6 / 0.45 ** 1.6
        near_g.append((cx_ - 0.514 * hw, prop + sheer, cz_ - 0.857 * hw))
        far_g.append((cx_ + 0.514 * hw, prop + sheer, cz_ + 0.857 * hw))
        near_c.append((cx_ - 0.514 * hw * 0.92, prop, cz_ - 0.857 * hw * 0.92))
    G = lambda q: gp(q[0], q[2], q[1])
    k0 = kz(sz_)
    hull_top = thin(lerp(OCHRE, PRUSSIAN, 0.14), 0.36)
    hull_low = lerp(thin(OCHRE, 0.12), mixp(SIENNA, PRUSSIAN, 0.35), 0.42)
    hull_sh = mixp(SIENNA, PRUSSIAN, 0.46)
    inside_a, inside_b = mixp(SIENNA, PRUSSIAN, 0.66), mixp(SIENNA, PRUSSIAN, 0.50)
    # the inside, seen over the near gunwale: darker toward the stern
    L.poly([G(q) for q in far_g] + [G(q) for q in reversed(near_g)], inside_a, inside_b, g=(G(near_g[0]), G(near_g[-1])))
    for i in range(2, n - 1, 2):                                          # ribs up the far side
        a_, c_ = far_g[i], near_g[i]
        L.line([gp(a_[0], a_[2], a_[1] - 2), gp(a_[0] - 0.514 * 10, a_[2] - 0.857 * 10, a_[1] - side * 0.5)], lerp(inside_b, OCHRE, 0.25), max(0.5, 3 * kz(a_[2])), 0.5)
    # a net heaped in the stern, a float or two on it
    i0 = 2
    hp_ = [gp((near_g[i][0] + far_g[i][0]) / 2, (near_g[i][2] + far_g[i][2]) / 2, prop + side * (0.55 + 0.25 * math.sin(i * 1.7))) for i in range(i0, i0 + 4)]
    lo_ = [gp((near_g[i][0] * 0.75 + far_g[i][0] * 0.25), (near_g[i][2] * 0.75 + far_g[i][2] * 0.25), prop + side * 0.2) for i in range(i0, i0 + 4)]
    L.poly(hp_ + lo_[::-1], lerp(mixp(SIENNA, PRUSSIAN, 0.62), COBALT, 0.12), mixp(SIENNA, PRUSSIAN, 0.72))
    for q in hp_[1:3]:
        L.ellipse(q[0], q[1] + 1.5, max(0.8, 4.5 * k0), max(0.7, 3.5 * k0), thin(OCHRE, 0.35))
    for u in (0.3, 0.52, 0.74):                                           # thwarts: their tops catch the sun
        i = int(u * n)
        a_, c_ = near_g[i], far_g[i]
        L.line([gp(a_[0], a_[2], a_[1] - 7), gp(c_[0], c_[2], c_[1] - 7)], mixp(SIENNA, PRUSSIAN, 0.40), max(0.9, 8 * kz(a_[2])), 1.0)
        L.line([gp(a_[0], a_[2], a_[1] - 5), gp(c_[0], c_[2], c_[1] - 5)], thin(mixp(OCHRE, SIENNA, 0.3), 0.3), max(0.6, 3 * kz(a_[2])), 0.9)
    # a sculling oar laid along the thwarts
    oa, ob = near_g[4], near_g[12]
    L.line([gp(oa[0] + 0.514 * 30, oa[2] + 0.857 * 30, oa[1] - 3), gp(ob[0] + 0.514 * 34, ob[2] + 0.857 * 34, ob[1] - 12)], thin(OCHRE, 0.42), max(0.7, 3.2 * k0), 0.95)
    # the near side: sunlit wood from the gunwale down to the chine, turning under
    L.poly([G(q) for q in near_g] + [G(q) for q in reversed(near_c)], hull_top, hull_low, g=(G(near_g[n // 2]), G(near_c[n // 2])))
    # the bow: the planks turn across the stem, in shade
    tip = inland(sx_, sz_, Ln + 14)
    bow_top = (tip[0], prop + side + 60, tip[1])
    L.poly([G(near_g[-2]), G(bow_top), G(far_g[-2]), G(far_g[-1]), G(near_g[-1])], hull_sh, lerp(hull_sh, PRUSSIAN, 0.2))
    L.poly([G(near_g[-1]), G(bow_top), (G(bow_top)[0], G(near_c[-1])[1]), G(near_c[-1])], lerp(hull_sh, OCHRE, 0.12), hull_sh)
    # the strakes: two plank seams along the side, the rubbing strake under the gunwale, weather streaks down the wood
    seam = mixp(SIENNA, PRUSSIAN, 0.48)
    for j, v in enumerate((0.34, 0.64)):                                  # each plank a little darker under the one above it; the seam between
        pts_ = [gp(a_[0], a_[2], a_[1] + (c_[1] - a_[1]) * v) for a_, c_ in zip(near_g, near_c)]
        low_ = [gp(a_[0], a_[2], a_[1] + (c_[1] - a_[1]) * min(1.0, v + 0.10)) for a_, c_ in zip(near_g, near_c)]
        L.poly(pts_ + low_[::-1], seam, alpha=0.16)
        L.line(pts_, seam, max(0.8, 2.0 * k0), 0.62)
        for i in range(2 + j, n - 1, 4):                                    # the butts where two lengths of plank meet, staggered
            a_, c_ = near_g[i], near_c[i]
            v1 = 1.0 if j else 0.64
            L.line([gp(a_[0], a_[2], a_[1] + (c_[1] - a_[1]) * v), gp(a_[0], a_[2], a_[1] + (c_[1] - a_[1]) * v1)], seam, 0.7, 0.45)
    L.line([gp(a_[0], a_[2], a_[1] - 3) for a_ in near_g], lerp(SIENNA, PRUSSIAN, 0.3), max(1.0, 5 * k0), 0.85)
    L.line([gp(a_[0], a_[2], a_[1] + 0.5) for a_ in near_g], thin(OCHRE, 0.55), max(0.6, 2.2 * k0), 0.9)             # the gunwale's top in the sun
    for i in range(1, n):
        if rng.random() < 0.7:
            a_, c_ = near_g[i], near_c[i]
            f0, f1 = rng.uniform(0.15, 0.5), rng.uniform(0.6, 0.98)
            L.line([gp(a_[0], a_[2], a_[1] + (c_[1] - a_[1]) * f0), gp(a_[0] + 3, a_[2], a_[1] + (c_[1] - a_[1]) * f1)], mixp(SIENNA, PRUSSIAN, 0.4), 0.6, 0.16 + 0.14 * rng.random())
    # the stem post
    L.line([G((tip[0], prop + 2, tip[1])), G(bow_top)], hull_sh, max(1.2, 10 * kz(tip[1])), 1.0)
    L.line([add_px(G((tip[0], prop + 2, tip[1])), -1.2, 0), add_px(G(bow_top), -1.2, 0)], thin(mixp(OCHRE, SIENNA, 0.4), 0.3), max(0.6, 3 * kz(tip[1])), 0.8)
    # the cross timbers it sits on: each a baulk across under the hull on two stub legs (the gap between and under them
    # is open: the sand shows). Their faces toward us are in shade; their tops catch the sun.
    if prop > 0:
        dark, darker, top_c = lerp(WOOD_SHADE, OCHRE, 0.10), lerp(WOOD_SHADE, PRUSSIAN, 0.35), thin(mixp(OCHRE, SIENNA, 0.4), 0.28)
        for u in (0.24, 0.70):
            cx_, cz_ = inland(sx_, sz_, Ln * u)
            ext = beam + 28
            a0 = (cx_ - 0.514 * ext, cz_ - 0.857 * ext)
            a1 = (cx_ + 0.514 * ext, cz_ + 0.857 * ext)
            for f0, f1 in ((0.03, 0.17), (0.83, 0.97)):                       # the legs
                q0 = (a0[0] + (a1[0] - a0[0]) * f0, a0[1] + (a1[1] - a0[1]) * f0)
                q1 = (a0[0] + (a1[0] - a0[0]) * f1, a0[1] + (a1[1] - a0[1]) * f1)
                L.poly([gp(*q0), gp(*q1), gp(q1[0], q1[1], prop - 15), gp(q0[0], q0[1], prop - 15)], darker, lerp(darker, PRUSSIAN, 0.3))
            L.poly([gp(a0[0], a0[1], prop - 17), gp(a1[0], a1[1], prop - 17), gp(a1[0], a1[1], prop), gp(a0[0], a0[1], prop)], dark, darker)     # the baulk
            b0, b1 = inland(a0[0], a0[1], -16), inland(a1[0], a1[1], -16)
            L.poly([gp(a0[0], a0[1], prop), gp(a1[0], a1[1], prop), gp(b1[0], b1[1], prop), gp(b0[0], b0[1], prop)], top_c, lerp(top_c, dark, 0.4))  # its top
            for f in (0.3, 0.55, 0.78):                                       # the grain of it
                L.line([gp(a0[0] + (a1[0] - a0[0]) * f, a0[1] + (a1[1] - a0[1]) * f, prop - 13), gp(a0[0] + (a1[0] - a0[0]) * (f + 0.14), a0[1] + (a1[1] - a0[1]) * (f + 0.14), prop - 11)], PRUSSIAN, 0.5, 0.3)
            keyline(L, [gp(a0[0], a0[1], prop - 17), gp(a1[0], a1[1], prop - 17)], gp(*a0)[1], seed=seed + 7)
    # the key line: under the hull and round the shaded bow; the sunlit sheer is left to the paper
    r0 = G(near_c[-1])[1]
    keyline(L, [G(q) for q in near_c] + [G((tip[0], prop + 2, tip[1]))], r0, seed=seed + 1)
    keyline(L, [G(q) for q in far_g], r0, seed=seed + 2, alpha=0.35)
    c, a = hand(*L.done(), seed)
    return painted(grade_cut(c, a, 0.93, seed=seed), a, under_of(back, a), seed=seed, fast=fast)


def add_px(p, dx, dy):
    return (p[0] + dx, p[1] + dy)


def racks_cut(back, seed, fast=False):
    """Nets drying on bamboo racks on the beach: three uprights and a rail, the net hung over it in swags, its hem
    ragged and weighted with floats. A net is a veil: what is behind it shows through, darkened, with the mesh on it."""
    L = Wet(SHAPE)
    rng = np.random.default_rng(seed)
    x, y = grid(SHAPE)
    net = Wet(SHAPE)
    bamboo, bamboo_l = lerp(OCHRE, PRUSSIAN, 0.38), thin(mixp(OCHRE, NAPLES, 0.4), 0.3)
    for r in RACKS:
        x0, z0 = r["x"], r["z"]
        x1, z1 = x0 + r["w"] * 0.76, z0 + r["w"] * 0.64                # the rack runs along the shore
        k = kz(z0)
        P_ = lambda u, hgt: gp(x0 + (x1 - x0) * u, z0 + (z1 - z0) * u, hgt)
        # the net: hung from the rail in three swags, its hem uneven; gaps between the swags near the hem
        hem_n = 13
        hems = [r["h"] * (0.17 + 0.11 * rng.random() + (0.10 if i % 4 == 0 else 0.0)) for i in range(hem_n)]
        ties = 9                                                           # it is tied to the rail every pace and sags a little between the ties
        top_n = [P_(u, r["h"] - 3 - (10.0 if j % 2 else 0.0)) for j, u in enumerate(np.linspace(1, 0, 2 * ties - 1))]
        net.poly([P_(i / (hem_n - 1), hems[i]) for i in range(hem_n)] + top_n, (1, 1, 1))
        for u_gap in (0.36, 0.69):                                         # where two lengths of net meet: a slit, a little open at the hem
            net.clear([P_(u_gap - 0.003, r["h"] * 0.80), P_(u_gap + 0.003, r["h"] * 0.80), P_(u_gap + 0.016, r["h"] * 0.12), P_(u_gap - 0.012, r["h"] * 0.12)])
        for (px_, pz_, u) in ((x0, z0, 0.0), (x1, z1, 1.0), ((x0 + x1) / 2, (z0 + z1) / 2, 0.5)):
            L.line([gp(px_, pz_), gp(px_, pz_, r["h"])], bamboo, max(1.0, 7 * k), 1.0)
            L.line([add_px(gp(px_, pz_), -0.8, 0), add_px(gp(px_, pz_, r["h"]), -0.8, 0)], bamboo_l, max(0.5, 2 * k), 0.85)
        L.line([P_(0, r["h"]), P_(1, r["h"])], bamboo, max(1.0, 6 * k), 1.0)
        L.line([add_px(P_(0, r["h"]), 0, -0.6), add_px(P_(1, r["h"]), 0, -0.6)], bamboo_l, max(0.5, 2 * k), 0.85)
        # floats along the hem
        for i in range(1, hem_n - 1, 2):
            p = P_(i / (hem_n - 1), hems[i] + 2)
            L.ellipse(p[0], p[1], max(1.0, 5 * k), max(0.9, 4 * k), thin(OCHRE, 0.40), lerp(OCHRE, PRUSSIAN, 0.3), g=((p[0] - 2, p[1] - 2), (p[0] + 2, p[1] + 2)))
    nc, na = net.done()
    # the veil: the backdrop behind it, darkened and cooled; the mesh across it; folds hanging down it
    mesh = (0.5 + 0.5 * np.sin((x + y) * 2 * math.pi / 3.3)) * (0.5 + 0.5 * np.sin((x - y) * 2 * math.pi / 3.3))
    folds = noise(SHAPE, (8, 70), seed + 3, 2)                               # it hangs in folds: thicker (darker) and thinner down its length
    tone = lerp(mixp(SIENNA, PRUSSIAN, 0.56), mixp(SIENNA, PRUSSIAN, 0.76), folds[..., None])
    veil = lerp(back, tone, 0.46 + 0.34 * folds[..., None]) * (0.86 + 0.28 * mesh[..., None])
    out = Wet(SHAPE)
    out.add(np.clip(veil, 0, 1), na)
    lc, la = L.done()
    out.add(lc, la)
    c, a = hand(*out.done(), seed)
    return painted(c, a, under_of(back, a), seed=seed, keep=0.75, fast=fast)


def board_cut(back, seed, fast=False):
    """The notice-board place at the village entrance: a low platform of earth faced with stones, two posts, a little
    roof, a row of boards dense with writing (pattern: columns of short dashes, never characters). The Kirishitan
    board is among them. The roof's shadow lies along the top of the boards."""
    L = Wet(SHAPE)
    rng = np.random.default_rng(seed)
    bz = BOARD["z"]
    bx = street_x(bz) + BOARD["off"]
    hw = BOARD["w"] / 2
    ax, az = bx - 0.514 * hw, bz - 0.857 * hw                        # along the street
    cx_, cz_ = bx + 0.514 * hw, bz + 0.857 * hw
    k = kz(bz)
    post_h = BOARD["post"]
    # the platform
    f0, f1 = gp(*inland(ax, az, 60)), gp(*inland(cx_, cz_, 60))
    L.poly([f0, f1, gp(*inland(cx_, cz_, 60), 22), gp(*inland(ax, az, 60), 22)], thin(STONE_C, 0.25), lerp(STONE_C, PRUSSIAN, 0.2))
    L.poly([gp(*inland(ax, az, 60), 22), gp(*inland(cx_, cz_, 60), 22), gp(*inland(cx_, cz_, -40), 22), gp(*inland(ax, az, -40), 22)], thin(lerp(SAND, OCHRE, 0.12), 0.45))
    for u in np.linspace(0.08, 0.92, 7):                                 # the facing stones' joints
        q0 = (f0[0] + (f1[0] - f0[0]) * u, f0[1] + (f1[1] - f0[1]) * u)
        L.line([q0, (q0[0], q0[1] - 22 * k)], PRUSSIAN, 0.5, 0.3)
    # the boards' shadow on the platform's top
    L.glaze([gp(ax, az, 22), gp(cx_, cz_, 22), gp(cx_ + SUN[0] * 40, cz_ + SUN[1] * 40, 22), gp(ax + SUN[0] * 40, az + SUN[1] * 40, 22)], SHADE, 0.8)
    # the posts: lit on the left
    for px_, pz_ in ((ax, az), (cx_, cz_)):
        L.line([gp(px_, pz_, 22), gp(px_, pz_, post_h)], WOOD_SHADE, max(1.2, 14 * k), 1.0)
        L.line([add_px(gp(px_, pz_, 22), -1.6, 0), add_px(gp(px_, pz_, post_h), -1.6, 0)], thin(mixp(OCHRE, SIENNA, 0.4), 0.3), max(0.6, 4 * k), 0.9)
    # the rail the boards hang from, and the boards: five pale planks, the writing in columns
    L.line([gp(ax, az, 212), gp(cx_, cz_, 212)], WOOD_SHADE, max(0.9, 6 * k), 1.0)
    n = 5
    for i in range(n):
        u0, u1 = (i + 0.08) / n, (i + 0.92) / n
        p00 = gp(ax + (cx_ - ax) * u0, az + (cz_ - az) * u0, 120)
        p10 = gp(ax + (cx_ - ax) * u1, az + (cz_ - az) * u1, 120)
        p11 = gp(ax + (cx_ - ax) * u1, az + (cz_ - az) * u1, 205)
        p01 = gp(ax + (cx_ - ax) * u0, az + (cz_ - az) * u0, 205)
        L.poly([p00, p10, p11, p01], thin(mixp(OCHRE, NAPLES, 0.5), 0.62), thin(mixp(OCHRE, COBALT, 0.12), 0.42), g=(p01, p00))
        cols = 3 if i != 2 else 4
        for c in range(cols):
            v = (c + 0.5) / cols
            q0 = lerp(np.array(p01), np.array(p11), v)
            q1 = lerp(np.array(p00), np.array(p10), v)
            yy = 0.08
            while yy < 0.92:
                ln = rng.uniform(0.03, 0.09)
                a_ = lerp(q0, q1, yy)
                b_ = lerp(q0, q1, min(0.95, yy + ln))
                L.line([tuple(a_), tuple(b_)], PRUSSIAN, 0.7, 0.72)
                yy += ln + rng.uniform(0.02, 0.05)
        L.line([p10, p00, p01], PRUSSIAN, 0.5, 0.4)
    # the roof's shadow along the top of the boards
    L.glaze([gp(ax, az, 213), gp(cx_, cz_, 213), gp(cx_, cz_, 188), gp(ax, az, 186)], SHADE_WARM, 0.75)
    # the roof: a little gabled roof of boards over the row: its seaward slope takes the sun
    ends = ((ax - 0.514 * 20, az - 0.857 * 20), (cx_ + 0.514 * 20, cz_ + 0.857 * 20))
    for (da, db, c0, c1) in ((55, 5, lerp(SHINGLE_SHADE, SIENNA, 0.1), lerp(SHINGLE_SHADE, PRUSSIAN, 0.2)), (-55, -5, thin(SHINGLE_LIT, 0.42), thin(SHINGLE_LIT, 0.12))):
        q = [gp(*inland(*ends[0], da), post_h), gp(*inland(*ends[1], da), post_h), gp(*inland(*ends[1], db), post_h + 30), gp(*inland(*ends[0], db), post_h + 30)]
        L.poly(q, c0, c1, g=(q[3], q[0]))
    L.line([gp(*inland(*ends[0], -55), post_h - 2), gp(*inland(*ends[1], -55), post_h - 2)], lerp(SHINGLE_SHADE, PRUSSIAN, 0.4), max(0.7, 4 * k), 0.9)   # the eave's edge
    keyline(L, [gp(*inland(*ends[0], 55), post_h), gp(*inland(*ends[0], 5), post_h + 30), gp(*inland(*ends[1], 5), post_h + 30), gp(*inland(*ends[1], 55), post_h)], gp(bx, bz)[1], seed=seed)
    keyline(L, [f0, f1], f0[1], seed=seed + 1)
    c, a = hand(*L.done(), seed, amount=0.5)
    return painted(c, a, under_of(back, a), seed=seed, keep=0.8, fast=fast)


STONE_C = thin(lerp(PRUSSIAN, OCHRE, 0.16), 0.52)


def fence_cut(back, seed, fast=False):
    """The hen yard's low bamboo fence: posts and three level poles, tied where they cross; the poles' tops in the sun.
    The hens behind it are the engine's."""
    L = Wet(SHAPE)
    Y = YARD
    h = Y["fence"]
    pole, pole_l, pole_d = lerp(OCHRE, PRUSSIAN, 0.34), thin(mixp(OCHRE, NAPLES, 0.45), 0.32), lerp(OCHRE, PRUSSIAN, 0.55)
    runs = [((Y["x0"], Y["z1"]), (Y["x1"], Y["z1"])), ((Y["x0"], Y["z0"]), (Y["x0"], Y["z1"]))]
    for (a_, b_) in runs:
        n = max(2, int(math.hypot(b_[0] - a_[0], b_[1] - a_[1]) / 110))
        for v in (0.3, 0.6, 0.92):
            pts = [gp(a_[0] + (b_[0] - a_[0]) * u, a_[1] + (b_[1] - a_[1]) * u, h * v) for u in np.linspace(0, 1, 6)]
            kk = kz((a_[1] + b_[1]) / 2)
            L.line([(p[0], p[1] + max(0.6, 1.5 * kk)) for p in pts], pole_d, max(0.9, 3.2 * kk), 0.9)
            L.line(pts, pole_l, max(1.0, 3.6 * kk), 1.0)
        for i in range(n + 1):
            u = i / n
            px_, pz_ = a_[0] + (b_[0] - a_[0]) * u, a_[1] + (b_[1] - a_[1]) * u
            kk = kz(pz_)
            L.line([gp(px_, pz_), gp(px_, pz_, h + 6)], pole, max(1.2, 6 * kk), 1.0)
            L.line([add_px(gp(px_, pz_), -max(0.6, 1.6 * kk), 0), add_px(gp(px_, pz_, h + 6), -max(0.6, 1.6 * kk), 0)], pole_l, max(0.6, 2.2 * kk), 0.9)
            for v in (0.3, 0.6, 0.92):                                      # the ties
                q = gp(px_, pz_, h * v)
                L.line([(q[0] - 2.4 * kk, q[1] - 2.0 * kk), (q[0] + 2.4 * kk, q[1] + 2.4 * kk)], mixp(SIENNA, PRUSSIAN, 0.55), max(0.6, 1.6 * kk), 0.8)
    c, a = hand(*L.done(), seed)
    return painted(c, a, under_of(back, a), seed=seed, keep=0.8, fast=fast)


def noren_cut(back, seed, fast=False):
    """Kihei's noren in the shop's open front: indigo cloth in three panels, a white fish on the middle one (our own
    mark), its hem free (it sways: fx noren-sway). A graded wash of indigo: deep under the eave's shadow at the top,
    the sun on the rest, the folds a little lighter."""
    L = Wet(SHAPE)
    z0 = SHOP["z0"]
    x0 = front_x(z0)
    ix, iz = inland(x0, z0, 25)
    jx, jz = inland(x0, z0, 25 + 185)
    top, drop = 183.0, 92.0
    deep, sunlit = lerp(INDIGO, PRUSSIAN, 0.25), thin(lerp(INDIGO, COBALT, 0.30), 0.10)
    for i in range(3):
        u0, u1 = i / 3 + 0.015, (i + 1) / 3 - 0.015
        q = [gp(ix + (jx - ix) * u0, iz + (jz - iz) * u0, top), gp(ix + (jx - ix) * u1, iz + (jz - iz) * u1, top),
             gp(ix + (jx - ix) * u1, iz + (jz - iz) * u1, top - drop), gp(ix + (jx - ix) * u0, iz + (jz - iz) * u0, top - drop)]
        L.poly(q, deep, sunlit, g=(q[0], (q[0][0], q[0][1] + (q[3][1] - q[0][1]) * 0.42)))
        for f in (0.30, 0.68):                                              # a fold down each panel: a lighter thread
            a_ = (q[0][0] + (q[1][0] - q[0][0]) * f, q[0][1] + (q[1][1] - q[0][1]) * f + 6)
            b_ = (q[3][0] + (q[2][0] - q[3][0]) * f, q[3][1] + (q[2][1] - q[3][1]) * f - 1)
            L.line([a_, b_], thin(lerp(INDIGO, COBALT, 0.5), 0.25), 1.4, 0.35)
        keyline(L, [q[1], q[2], q[3]], q[3][1], seed=seed + i, alpha=0.5)
    # the rod it hangs from
    L.line([gp(ix, iz, top + 2), gp(jx, jz, top + 2)], WOOD_SHADE, max(1.0, 5 * kz(iz)), 1.0)
    # a white fish on the middle panel: a plain shape of our own, the paper left bare
    mx_, mz_ = ix + (jx - ix) * 0.5, iz + (jz - iz) * 0.5
    c0 = gp(mx_, mz_, top - drop * 0.5)
    k = kz(mz_)
    L.ellipse(c0[0], c0[1], 22 * k, 9 * k, WPAPER)
    L.poly([(c0[0] + 20 * k, c0[1]), (c0[0] + 32 * k, c0[1] - 9 * k), (c0[0] + 32 * k, c0[1] + 9 * k)], WPAPER)
    L.ellipse(c0[0] - 12 * k, c0[1] - 2 * k, 1.6 * k, 1.6 * k, PRUSSIAN)
    c, a = hand(*L.done(), seed, amount=0.6)
    return painted(c, a, INDIGO, seed=seed, keep=0.8, fast=fast)


def ship_cut(back, seed, fast=False):
    """Gonroku's freighter at anchor far out in the bay (a benzaisen): a high stern, one mast, the yard lowered with the
    great sail furled along it, the stays running from the masthead down to stem and stern. Small, and paled by the air
    between: it rides at anchor (fx ship-bob)."""
    L = Wet(SHAPE)
    cx_, cy_ = SHIP_AT
    Ln = 26.0
    hull_ = thin(lerp(SIENNA, PRUSSIAN, 0.58), 0.20)
    wood = thin(lerp(OCHRE, PRUSSIAN, 0.30), 0.30)
    L.poly([(cx_ - Ln * 0.5, cy_), (cx_ + Ln * 0.5, cy_), (cx_ + Ln * 0.56, cy_ - 4.5), (cx_ + Ln * 0.42, cy_ - 7.5), (cx_ - Ln * 0.3, cy_ - 5.5), (cx_ - Ln * 0.52, cy_ - 2.5)],
           hull_, lerp(hull_, PRUSSIAN, 0.3), g=((cx_ - Ln * 0.5, cy_ - 7), (cx_ + Ln * 0.5, cy_)))
    L.poly([(cx_ + Ln * 0.36, cy_ - 7.5), (cx_ + Ln * 0.56, cy_ - 4.5), (cx_ + Ln * 0.6, cy_ - 11), (cx_ + Ln * 0.38, cy_ - 12)], wood, lerp(wood, PRUSSIAN, 0.3))       # the high stern's castle
    L.line([(cx_ - Ln * 0.50, cy_ - 2.4), (cx_ + Ln * 0.40, cy_ - 7.3)], thin(wood, 0.3), 0.7, 0.8)                # the sun along its rail
    mast_top = (cx_ - 2, cy_ - 38)
    L.line([(cx_ - 2, cy_ - 5), mast_top], hull_, 1.3, 1.0)                                                       # the mast
    for (ex, ey) in ((cx_ - Ln * 0.52, cy_ - 3.0), (cx_ + Ln * 0.50, cy_ - 11.5), (cx_ + Ln * 0.30, cy_ - 7.0)):   # the stays
        L.line([mast_top, (ex, ey)], hull_, 1.0, 1.0)
    # the sail furled on the yard, the yard lowered and cocked (one end down by the bow), as a ship at anchor carries it
    L.poly([(cx_ - 15, cy_ - 14.5), (cx_ + 12, cy_ - 22.0), (cx_ + 12.6, cy_ - 17.8), (cx_ - 14.4, cy_ - 10.3)], thin(OCHRE, 0.62), thin(mixp(OCHRE, COBALT, 0.25), 0.45))
    L.line([(cx_ - 15.5, cy_ - 10.0), (cx_ + 13.5, cy_ - 18.0)], hull_, 0.8, 0.9)
    c, a = L.done()
    return painted(c, a, COBALT, seed=seed, sizes=(3, 2), keep=0.8, fast=fast)


# ================================================================ the numbers
def layout(planes, info):
    import edo_village_layout as Lay
    return Lay.layout(planes, info, SHOP, YARD, BOARD, WELL, RACKS, BIGBOAT, TENDER, SHIP_AT)


def to_file(picture, name, colors=128, alpha=None, seed=7, speckle=0.010, amount=0.010):
    """Pigment grain (little: the wash has its own granulation), then a limited palette with speckle: an 8-bit PNG."""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def finish_all(pic, planes, order, info, out=OUT):
    """THE WATERCOLOUR FINISH (DEPTH.md): the backdrop washed (watercolor.wash), every cut-out washed over the unwashed
    backdrop with the same seed (wash_cut), so the paper is one sheet; then the palette.
      soft   WET = wet_mask(info): 1 in the sky, less on Fuji (0.65), on the far shore and capes (0.5) and on the headland
             (0.55, its near spur 0.33), the open water 0.75 at the horizon falling to 0.19 at the shore; 0 on everything
             that stands in the play. For a
             cut-out the mask is cut away where the cut-out itself is (and 2 px round it), so its own edge stays crisp.
      amount 1.0 (daylight), lift 0.07 (the library's)."""
    soft = wet_mask(info)
    back_washed = WC.wash(pic, seed=SEED, soft=soft)
    sizes = {"back": to_file(back_washed, out + "/back.png", 250)}
    for name, n in order:
        c, a = planes[name]
        hard = np.clip(blur((a > 0.3).astype(F32), 1.2) * 2.0, 0, 1)
        washed = WC.wash_cut(c, (a > 0.5).astype(F32), pic, seed=SEED, soft=soft * (1 - hard))
        planes[name] = (washed, a)
        sizes[name] = to_file(washed, out + f"/{name}.png", n, a)
    return back_washed, sizes


if __name__ == "__main__":
    import edo_village_near as NEAR
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = "fast" in sys.argv
    base, info = under()
    info["shadow"] = cast_shadows(base, info["ground"], SEED, ground_shadows_of_details())
    Image.fromarray((base * 255).astype(np.uint8)).save(OUT + "-1-under.png")
    print("under", round(time.time() - t0, 1))
    if fast:
        pic = base.copy()
    else:
        # the brush pass, light: the far plane stays as the wet washes left it, the ground is half brushed
        x_, y_ = grid(SHAPE)
        brushed_ = strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.02, keep=0.0)
        keep = np.clip(0.50 + 0.38 * wet_mask(info), 0, 0.92)
        pic = lerp(brushed_, base, keep[..., None]).astype(F32)
    print("brushed", round(time.time() - t0, 1))
    details(pic, info, fast=fast)
    print("details", round(time.time() - t0, 1))
    planes = {}
    planes["ship"] = ship_cut(pic, 11, fast)
    planes["racks"] = racks_cut(pic, 12, fast)
    planes["tender"] = boat_cut(pic, TENDER, 13, fast)
    planes["board"] = board_cut(pic, 14, fast)
    planes["noren"] = noren_cut(pic, 15, fast)
    planes["boat"] = boat_cut(pic, BIGBOAT, 16, fast)
    planes["fence"] = fence_cut(pic, 17, fast)
    planes["front"] = NEAR.front_cut(pic, 18, info, fast)
    planes["near"] = NEAR.near_cut(pic, 19, info, fast)
    ORDER = ["ship", "racks", "tender", "board", "noren", "boat", "fence", "front", "near"]
    whole = pic.copy()
    for name in ORDER:
        c, a = planes[name]
        over(whole, c, (a > 0.5).astype(F32))
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-all.png")
    lay_ = layout(planes, info)
    with open(OUT + "/layout.json", "w") as f:
        json.dump(lay_, f, indent=1)
    print("painted", round(time.time() - t0, 1))
    if "wash" in sys.argv or not fast:                                  # (fast wash: the composition with the paper's finish, no brush pass)
        counts = (("ship", 48), ("racks", 96), ("tender", 64), ("board", 96), ("noren", 64), ("boat", 96), ("fence", 64), ("front", 64), ("near", 128))
        target = OUT if not fast else OUT + "-fast"
        os.makedirs(target, exist_ok=True)
        back_washed, sizes = finish_all(pic, planes, counts, info, target)
        print(sizes)
        comp = Image.open(target + "/back.png").convert("RGBA")
        for name in ORDER:
            comp.alpha_composite(Image.open(f"{target}/{name}.png").convert("RGBA"))
        comp.convert("RGB").save(OUT + ("-comp.png" if not fast else "-fast-comp.png"))
    print("done", round(time.time() - t0, 1))

"""PAINT-21D: edo-theatre, the Inari puppet theatre in the grounds of Naniwa Shrine, Osaka, an afternoon in late April
1830 (S/briefs/out/edo2-design.md, section 5 and #31), in the act's manner (S/work-20-paintA/style.md: flats, one fine
contour round the silhouettes, few paints, the blue leading), keyed `edo-lamp` (PAINT-20F's; untouched).

    python3 edo_theatre.py fast      the under-painting with the contours, no brush pass, both states (seconds)
    python3 edo_theatre.py           everything: out/edo-theatre/ (back, show, the cut-outs and their show twins, the
                                     daylight's light pictures, layout.json), and the comps

ONE CAMERA (room.View, edo_theatre_model.VIEW): backstage, upstage of the stage's left end, turned to the right, looking
diagonally across the stage toward the house. The hall in centimetres: edo_theatre_model.py.

THE PICTURE. Left: the wing, backstage: its far wall of dark planks (the back door in it, open a hand's breadth on the
alley's daylight; the peg with the two black robes and hoods; the shelf of heads over two wicker boxes; the puppets
hanging on their rail by their heads, quiet as coats), the lamp on its stand, the boy puppet on his. The masking curtain,
black, at the stage's left end. Right: the stage's polished boards; the village gate near the rail at stage left; the
house front at stage right, raked toward the house; the rail, black, along the stage's front; beyond it the audience on
their mats, row behind row of heads, facing the stage (toward us); the chanter's dais at the right, out in the house,
with its lectern and book; the high lattice windows. The rafters over all; the backstage ceiling's dark edge across the
top.

LIGHT (keep to it). Day: daylight through the high lattice windows of the house (its far wall and its right wall),
falling on the audience in flat lit patches; the backstage dim, warmed by the lamp's pool (naples) and a blade of
daylight from the back door's crack. TWO STATES of the stage: before the show the stage's own high shutter (in the right
wall over the stage) is shut and the stage and the set are in the half light; in the show it is open and the set and
the boards are in the lit flat (the paper and naples), and the audience's heads are all turned to the stage. The flats:
lit (the paint warmed toward naples or the paper), half (the paint), shade (pulled toward cobalt/ultramarine), deep
(toward prussian blue). No gradient crosses a plane. The flames are the engine's (fx), the shafts of daylight in the air
are light pictures for the live layer (shaft-*.png).

PAINT-21D."""

import json
import math
import os
import sys
import time

import numpy as np

from brush import F32, lerp, noise, blur, mask_poly, mask_ellipse, mask_line, over, vary
from room import View
from edo_keep_kit import (Passes, boards, finish_scene, save_rgba, to_image, ipt, col, shade_of, dark_of, tint_of,
                          boundary, _hull, W, H, SHAPE, P, PAPER, NAPLES, OCHRE, SIENNA, PRUSSIAN, COBALT, ULTRA, CERULEAN)
import edo_theatre_model as M
from edo_theatre_kit import FastRoom as Room

OUT = "out/edo-theatre"
WORK = "out/edo-theatre-work"
V = View(**M.VIEW)

VERMILION, LAKE, VIRIDIAN, VERONESE = P("vermilion"), P("geranium-lake"), P("viridian"), P("veronese-green")
FLESH, FLESH_S = P("flesh-light"), P("flesh-shadow")

# ---- the act's paints, mixed by name (style.md section 2)
PLANK = lerp(SIENNA, OCHRE, 0.35)                 # planks where the light that is left reaches them
PLANK_S = lerp(lerp(SIENNA, OCHRE, 0.18), PRUSSIAN, 0.50)   # planks in the backstage dim
PLANK_D = lerp(SIENNA, PRUSSIAN, 0.66)            # the deepest wood
LAMPLIT = lerp(lerp(OCHRE, NAPLES, 0.55), PAPER, 0.1)   # the lamp's pool on wood: naples
STAGE_B = lerp(lerp(OCHRE, SIENNA, 0.45), PRUSSIAN, 0.34)   # the stage's polished boards in the half light
STAGE_LIT = lerp(lerp(NAPLES, OCHRE, 0.35), PAPER, 0.18)    # ...in the shaft of day (the show)
BACKFLOOR = lerp(lerp(SIENNA, OCHRE, 0.25), PRUSSIAN, 0.42)  # backstage boards
MAT = lerp(lerp(OCHRE, PAPER, 0.5), VERONESE, 0.10)        # straw mats in the house's light
MAT_S = shade_of(MAT, 0.42)
WALLH = lerp(lerp(OCHRE, SIENNA, 0.35), PAPER, 0.18)       # the house's plank walls in daylight
WALLH_S = shade_of(WALLH, 0.40)
ROOFW = lerp(lerp(SIENNA, OCHRE, 0.25), PRUSSIAN, 0.45)    # the roof's underside, the windows' light on it
RAFTER = lerp(SIENNA, PRUSSIAN, 0.74)
DAY = lerp(PAPER, CERULEAN, 0.10)                          # daylight in a window
LACQUER = lerp(PRUSSIAN, ULTRA, 0.18)                      # black lacquer (the rail, the lectern)
LACQUER_L = lerp(LACQUER, COBALT, 0.45)                    # its lit edge
CURT = lerp(ULTRA, PRUSSIAN, 0.62)                         # the masking curtain
CURT_L = lerp(ULTRA, PRUSSIAN, 0.40)
INDIGO = lerp(ULTRA, PRUSSIAN, 0.32)
BLACK_ROBE = lerp(PRUSSIAN, ULTRA, 0.10)
PLASTER_SET = lerp(PAPER, NAPLES, 0.12)                    # the house front's plaster (painted scenery)
POST_SET = lerp(SIENNA, PRUSSIAN, 0.2)
TILE = lerp(PAPER, PRUSSIAN, 0.58)                         # a roof's grey-blue
HAIR = lerp(PRUSSIAN, SIENNA, 0.12)
WICKER = lerp(OCHRE, PAPER, 0.18)

SUN = M.SUN_WIN                                             # daylight from the right wall's windows: toward -X, down


def plit(c, k=0.35):
    """A flat in the light: the paint warmed toward naples and the paper."""
    return lerp(col(c), lerp(NAPLES, PAPER, 0.4), k)


# ================================================================ helpers: things through the camera
def quad_wall_z(X0, X1, Y0, Y1, Z):
    return [(X0, Y0, Z), (X1, Y0, Z), (X1, Y1, Z), (X0, Y1, Z)]


def quad_wall_x(Z0, Z1, Y0, Y1, X):
    return [(X, Y0, Z0), (X, Y0, Z1), (X, Y1, Z1), (X, Y1, Z0)]


def boxflats(R, X0, X1, Y0, Y1, Z0, Z1, color, grp=None, alpha=0.85, lit=("top", "right", "front"), shade_k=0.38, amount=0.03,
             colors=None, thing=True):
    """A box as flats: the faces in `lit` the colour, the others its shade (or `colors` by face); one silhouette contour."""
    m = np.zeros(SHAPE, F32)
    for name, pp, n in R.V.box(X0, X1, Y0, Y1, Z0, Z1):
        c = (colors or {}).get(name)
        if c is None:
            c = color if name in lit else shade_of(color, shade_k)
        m = np.maximum(m, R.flat2d(pp, c, grp, amount=amount, cell=60))
    if thing:
        R.thing(m, alpha)
    return m


def cyl(R, X, Z, r, Y0, Y1, color, grp=None, lit_side=1.0, lit_share=0.3, shade_k=0.42, alpha=0.85, n=24):
    """A round upright (a post, a jar) as two flats: the shade, and a lit sliver on the side toward the light."""
    ring = lambda Y: [V.pt(X + r * math.cos(q), Y, Z + r * math.sin(q)) for q in np.linspace(0, 2 * math.pi, n, endpoint=False)]
    pp = _hull(ring(Y0) + ring(Y1))
    m = mask_poly(SHAPE, pp)
    R.fill(m, shade_of(color, shade_k), amount=0.03, cell=(12, 90))
    xs = [p[0] for p in pp]
    xl, xr = min(xs), max(xs)
    w = (xr - xl) * lit_share
    xx = np.mgrid[0:H, 0:W][1]
    lm = m * ((xx >= xr - w) if lit_side > 0 else (xx <= xl + w))
    R.fill(lm, color, amount=0.03, cell=(12, 90))
    R.add_mask(grp, m)
    R.thing(m, alpha)
    return m


def flat3(R, pts, color, grp=None, alpha=0.85, amount=0.03, thing=True, cell=60):
    m = R.flat(pts, color, grp, amount=amount, cell=cell)
    if thing:
        R.thing(m, alpha)
    return m


def flat2(R, pp, color, grp=None, alpha=0.85, amount=0.03, thing=True, cell=60):
    m = R.flat2d(pp, color, grp, amount=amount, cell=cell)
    if thing:
        R.thing(m, alpha)
    return m


def ell(R, cx, cy, rx, ry, color, grp=None, alpha=0.85, thing=True):
    m = mask_ellipse(SHAPE, cx, cy, max(rx, 0.6), max(ry, 0.6))
    R.fill(m, color, amount=0.02, cell=20)
    R.add_mask(grp, m)
    if thing:
        R.thing(m, alpha)
    return m


def floor_shadow(R, pts, k=0.35, floor=None, toward=None):
    """A cast shadow on the floor: the floor's polygon (room points at Y = 0) pulled toward the shade, hard-edged."""
    pp = V.poly([(x, 0.0, z) for x, z in pts])
    if len(pp) < 3:
        return
    m = mask_poly(SHAPE, pp)
    if floor is not None:
        m = m * floor
    R.shade(m, k, toward)


def sun_patch(R, pts3, color, floor_mask, k=0.85, sun=None):
    """Where daylight through a window lands on the floor: the window's corners laid along the light to Y = 0 -> a flat."""
    sun = SUN if sun is None else sun
    land = []
    for x, y, z in pts3:
        t = y / -sun[1]
        land.append((x + sun[0] * t, 0.0, z + sun[2] * t))
    pp = V.poly(land)
    if len(pp) < 3:
        return np.zeros(SHAPE, F32), land
    m = mask_poly(SHAPE, pp) * floor_mask
    R.fill(m, color, amount=0.02, cell=60, alpha=k)
    return m, land


# ================================================================ the hall
def shell(R, show):
    """The roof, the walls and the floors, far to near."""
    hx0, hx1, hz0, hz1 = M.HOUSE
    # ---- the roof over the house and the stage: plank underside and rafters running away from us (along Z)
    X, Z, okc, fpc = R.floor_uv(M.ROOF)
    roof_m = okc * (X >= hx0 - 5) * (X <= M.HALL_X1 + 5) * (Z >= -5) * (Z <= M.WING[3] + 10)
    R.fill(roof_m, ROOFW, amount=0.03, cell=90)
    xr = -60.0
    while xr < M.HALL_X1:
        pp = V.poly([(xr, M.ROOF, 0.0), (xr + 16, M.ROOF, 0.0), (xr + 16, M.ROOF, M.WING[3]), (xr, M.ROOF, M.WING[3])])
        if len(pp) >= 3:
            mk = R.flat2d(pp, RAFTER, amount=0.03) * roof_m
            R.thing(mk, 0.45)
        xr += 120.0
    # a tie beam across the hall over the stage's front
    for zb in (60.0, 770.0):
        mk = flat3(R, [(hx0, M.ROOF - 26, zb), (M.HALL_X1, M.ROOF - 26, zb), (M.HALL_X1, M.ROOF, zb), (hx0, M.ROOF, zb)], RAFTER, alpha=0.5)
    # ---- the house's far wall (Z = 0), its right wall (X = 900), its left wall (X = -100): planks in daylight
    u, v, okw, fpw = R.wall_uv("Z", 0.0)
    far_m = okw * (u >= hx0) * (u <= M.HALL_X1) * (v >= 0) * (v <= M.ROOF)
    R.fill(far_m, WALLH, amount=0.03, cell=90)
    R.thing(far_m, 0.4)
    ur, vr, okr, fpr = R.wall_uv("X", M.HALL_X1)
    right_m = okr * (ur >= 0) * (ur <= M.WING[3] + 10) * (vr >= 0) * (vr <= M.ROOF)
    R.fill(right_m, WALLH_S, amount=0.03, cell=90)
    R.thing(right_m, 0.45)
    ul, vl, okl, fpl = R.wall_uv("X", M.HOUSE_LEFT_X)
    left_m = okl * (ul >= 0) * (ul <= hz1) * (vl >= 0) * (vl <= M.ROOF)
    R.fill(left_m, lerp(WALLH, WALLH_S, 0.5), amount=0.03, cell=90)
    R.thing(left_m, 0.45)
    # plank joints, upright, on the far wall and the right wall (drawn texture)
    for (mm, uu, period) in ((far_m, u, 34.0), (right_m, ur, 34.0), (left_m, ul, 34.0)):
        f = np.mod(uu, period)
        f = np.minimum(f, period - f)
        ln = np.clip(1.2 - f / 0.9, 0, 1) * mm
        R.lines(mm, ln, 0.18)
    # the hall's posts: dark uprights in the plank walls, every 180 cm (the far wall and the right wall)
    xp = hx0 + 8.0
    while xp < M.HALL_X1 - 10:
        flat3(R, quad_wall_z(xp, xp + 16, 0.0, M.ROOF, 0.3), lerp(SIENNA, PRUSSIAN, 0.45), alpha=0.5)
        xp += 180.0
    zp = 20.0
    while zp < M.WING[3]:
        flat3(R, quad_wall_x(zp, zp + 16, 0.0, M.ROOF, M.HALL_X1 - 0.3), lerp(SIENNA, PRUSSIAN, 0.55), alpha=0.5)
        zp += 180.0
    # a rail (nageshi) round the walls under the windows
    for (pts) in (quad_wall_z(hx0, M.HALL_X1, 360, 372, 0.0),):
        flat3(R, pts, lerp(SIENNA, PRUSSIAN, 0.35), alpha=0.5)
    flat3(R, quad_wall_x(0.0, M.WING[3], 360, 372, M.HALL_X1), lerp(SIENNA, PRUSSIAN, 0.5), alpha=0.5)
    # ---- the high lattice windows: daylight, the lattice bars dark
    wins = []
    for (x0, x1) in M.WINDOWS_FAR:
        wins.append(("far", quad_wall_z(x0, x1, M.WIN_Y[0], M.WIN_Y[1], 0.0), "Z", 0.0, (x0, x1)))
    for (z0, z1) in M.WINDOWS_RIGHT:
        wins.append(("right", quad_wall_x(z0, z1, M.WIN_Y[0], M.WIN_Y[1], M.HALL_X1), "X", M.HALL_X1, (z0, z1)))
    for side, pts, axis, at, (a0, a1) in wins:
        mw = flat3(R, pts, DAY, alpha=0.6, amount=0.01)
        # lattice: upright bars every 14 cm
        a = a0 + 10.0
        while a < a1 - 4:
            bar = quad_wall_z(a, a + 4, M.WIN_Y[0], M.WIN_Y[1], 0.4) if axis == "Z" else quad_wall_x(a, a + 4, M.WIN_Y[0], M.WIN_Y[1], M.HALL_X1 - 0.4)
            pp = V.poly(bar)
            if len(pp) >= 3:
                R.flat2d(pp, lerp(SIENNA, PRUSSIAN, 0.55), amount=0.02)
            a += 14.0
    # ---- the house's floor: mats
    Xf, Zf, okf, fpf = R.floor_uv()
    house_floor = okf * (Xf >= hx0) * (Xf <= M.HALL_X1) * (Zf >= hz0) * (Zf <= hz1)
    R.fill(house_floor, lerp(PLANK, PRUSSIAN, 0.15), amount=0.03, cell=90)
    mx0, mx1, mz0, mz1 = M.MATS
    mats = house_floor * (Xf >= mx0) * (Xf <= mx1) * (Zf >= mz0) * (Zf <= mz1)
    R.fill(mats, MAT_S, amount=0.03, cell=60)
    # mat edges: a seam every 90 cm along X and every 180 along Z
    for (uu, period) in ((Xf, 90.0), (Zf, 180.0)):
        f = np.mod(uu - 5.0, period)
        f = np.minimum(f, period - f)
        ln = np.clip(1.0 - f / (fpf * 0.8 + 1e-6), 0, 1) * mats
        R.lines(mats, ln, 0.25)
    # ---- the stage's boards and the backstage floor (one level)
    sx0, sx1, sz0_, sz1_ = M.STAGE
    stage_m = okf * (Xf >= sx0) * (Xf <= sx1) * (Zf >= M.RAIL[3] - 1) * (Zf <= sz1_)
    wx0, wx1, wz0, wz1 = M.WING
    bx0, bx1, bz0, bz1 = M.BACKSTAGE
    back_m = okf * np.clip(((Xf >= wx0) & (Xf <= wx1) & (Zf >= wz0) & (Zf <= wz1)).astype(F32)
                           + ((Xf >= bx0) & (Xf <= bx1) & (Zf >= bz0) & (Zf <= bz1)).astype(F32)
                           + ((Xf > sx1) & (Xf <= M.HALL_X1) & (Zf >= M.DAIS[3]) & (Zf <= bz0)).astype(F32), 0, 1) * (1 - stage_m)
    boards(R, back_m, BACKFLOOR, along="X", width=28.0, offset=4.0, seed=31, line_alpha=0.26)
    boards(R, stage_m, STAGE_B, along="X", width=30.0, offset=12.0, seed=33, line_alpha=0.22, per_board=0.02)
    return dict(house_floor=house_floor, mats=mats, stage=stage_m, back=back_m, far=far_m, right=right_m, left=left_m, roof=roof_m)


def daylight(R, info, show):
    """The day through the high windows, laid as flats: patches on the mats (the audience's heads are lit there too, in
    audience()), and in the show the stage window's patch across the boards."""
    lit_m = np.zeros(SHAPE, F32)
    lands = []
    for (z0, z1) in M.WINDOWS_RIGHT:
        pts = quad_wall_x(z0, z1, M.WIN_Y[0], M.WIN_Y[1], M.HALL_X1)
        m, land = sun_patch(R, pts, plit(MAT, 0.55), info["mats"], 0.9)
        lit_m = np.maximum(lit_m, m)
        lands.append(land)
    if show:
        x0, x1, z0, z1 = M.SKYLIGHT
        pts = [(x0, M.ROOF, z0), (x1, M.ROOF, z0), (x1, M.ROOF, z1), (x0, M.ROOF, z1)]
        m, land = sun_patch(R, pts, STAGE_LIT, info["stage"], 0.95, sun=M.SUN_SKY)
        lit_m = np.maximum(lit_m, m)
        info["stage_land"] = land
    info["lit"] = lit_m
    info["lands"] = lands
    return lit_m


def in_sun(X, Y, Z, lands_xz):
    """Is a point (on a person or a thing) in a window's daylight? (Its shadow-free line to the window, as a flat test:
    the point laid along SUN to the floor falls inside one of the window patches.)"""
    t = Y / -SUN[1]
    px, pz = X + SUN[0] * t, Z + SUN[2] * t
    for land in lands_xz:
        poly = [(p[0], p[2]) for p in land]
        n = len(poly)
        ok = False
        for i in range(n):
            x0, z0 = poly[i]
            x1, z1 = poly[(i + 1) % n]
            if (z0 > pz) != (z1 > pz):
                xi = x0 + (pz - z0) * (x1 - x0) / (z1 - z0)
                if px < xi:
                    ok = not ok
        if ok:
            return True
    return False


# ================================================================ the audience
CLOTHES = [INDIGO, lerp(SIENNA, OCHRE, 0.3), lerp(PAPER, PRUSSIAN, 0.45), lerp(OCHRE, SIENNA, 0.15), lerp(INDIGO, PAPER, 0.25),
           lerp(VIRIDIAN, PRUSSIAN, 0.25), lerp(SIENNA, PRUSSIAN, 0.3), lerp(LAKE, SIENNA, 0.45), lerp(VERMILION, SIENNA, 0.35)]


def audience(R, info, show, seed=7):
    """Row behind row of seated people on the mats, facing the stage (toward us), the far rows first. Each: shoulders (a
    flat of their clothes), a head (hair; the face a flesh flat, set toward where they look). Before the show they look
    about and talk; in the show every face is turned to the boy on the rail. Room at the front for Mom and Tatsu."""
    rng = np.random.default_rng(seed)
    people = []
    rows = [705.0, 628.0, 551.0, 474.0, 397.0, 320.0, 243.0, 166.0, 92.0]
    puppet = V.pt(M.PUPPET_AT[0], M.PUPPET_FEET_Y + 50, M.PUPPET_AT[1])
    for ri in range(len(rows) - 1, -1, -1):
        z = rows[ri]
        x = -66.0 + (ri % 2) * 26.0
        while x < 575.0:
            gap = ri == 0 and 104.0 <= x <= 240.0
            if not gap:
                people.append((ri, x + rng.normal(0, 6), z + rng.normal(0, 5), rng.random(), rng.integers(len(CLOTHES)), rng.random()))
            x += 56.0 + rng.normal(0, 4)
    for (ri, x, z, r1, ci, r2) in people:
        sc = V.scale_at(x, z)
        tall = 84.0 + 10.0 * r1 * (1 if r2 > 0.15 else 0) - (22.0 if r2 < 0.08 else 0.0)        # a few children
        cloth = CLOTHES[ci]
        head_y = tall - 12.0
        hp = V.pt(x, head_y, z)
        hr = 10.0 * sc
        lit = in_sun(x, head_y, z, info["lands"])
        # shoulders: a rounded trapezoid from 0.62 of the height up to the neck
        sw = 23.0
        pts = [(x - sw, tall * 0.25, z), (x + sw, tall * 0.25, z), (x + sw * 0.86, tall * 0.70, z), (x + sw * 0.35, tall * 0.80, z),
               (x - sw * 0.35, tall * 0.80, z), (x - sw * 0.86, tall * 0.70, z)]
        cc = plit(cloth, 0.30) if lit else cloth
        m_body = R.flat(pts, shade_of(cc, 0.22), amount=0.02, cell=30)
        # the lit side of the shoulders: toward the right windows
        pts_l = [(x + sw * 0.15, tall * 0.25, z), (x + sw, tall * 0.25, z), (x + sw * 0.86, tall * 0.70, z), (x + sw * 0.35, tall * 0.80, z), (x + sw * 0.15, tall * 0.80, z)]
        R.flat(pts_l, cc, amount=0.02, cell=30)
        # where they look: in the show, at the boy; before, about them
        away = False
        if show:
            look = np.clip((puppet[0] - hp[0]) / 240.0, -0.75, 0.75)
        else:
            look = [-0.75, -0.4, 0.0, 0.3, 0.7, 0.75, -0.7][int(r2 * 7) % 7]
            away = r1 > 0.72                                                    # turned round to talk behind them
        hair = HAIR if r1 > 0.12 else lerp(PAPER, PRUSSIAN, 0.45)          # a few grey heads
        m_head = ell(R, hp[0], hp[1], hr * 0.95, hr * 1.12, hair, alpha=0.0, thing=False)
        # the face: a flesh flat inside the head, offset toward the look (0: straight at us)
        fx = hp[0] + look * hr * 0.42
        face = FLESH if lit else lerp(FLESH_S, COBALT, 0.12)
        if away:                                                                  # the back of the head: an ear's sliver of face
            fm = mask_ellipse(SHAPE, hp[0] + (hr * 0.8 if look > 0 else -hr * 0.8), hp[1] + hr * 0.25, hr * 0.22, hr * 0.42) * m_head
        else:
            fm = mask_ellipse(SHAPE, fx, hp[1] + hr * 0.18, hr * (0.62 - 0.18 * abs(look)), hr * 0.8) * m_head
        R.fill(fm, face, amount=0.02, cell=20)
        # a topknot or a woman's bun on top
        if r2 > 0.5:
            ell(R, hp[0] - look * hr * 0.3, hp[1] - hr * 0.95, hr * 0.32, hr * 0.22, hair, thing=False)
        else:
            ell(R, hp[0] - look * hr * 0.25, hp[1] - hr * 0.75, hr * 0.62, hr * 0.42, hair, thing=False)
        both = np.maximum(m_body, m_head)
        R.thing(both, 0.5 if ri > 2 else 0.7)
    return len(people)


# ================================================================ the dais, the rail, the curtain, the set
def dais(R, show):
    """The chanter's dais at stage right, out into the house: a low platform of dark lacquered wood, two cushions, the
    lectern with the book on it (the chanter's: nobody touches it)."""
    X0, X1, Z0, Z1, top = M.DAIS
    m = boxflats(R, X0, X1, 0.0, top, Z0, Z1, lerp(SIENNA, PRUSSIAN, 0.42), lit=("top", "right"), shade_k=0.45)
    # its top: a flat of tatami-like matting
    flat3(R, [(X0 + 6, top + 0.5, Z0 + 6), (X1 - 6, top + 0.5, Z0 + 6), (X1 - 6, top + 0.5, Z1 - 6), (X0 + 6, top + 0.5, Z1 - 6)],
          plit(MAT, 0.2) if show else MAT, alpha=0.4)
    for (cx, cz) in M.CUSHIONS:
        boxflats(R, cx - 28, cx + 28, top, top + 8, cz - 26, cz + 26, lerp(VERMILION, SIENNA, 0.45), lit=("top",), shade_k=0.4, alpha=0.6)
    a0, a1, b0, b1, y0, y1 = M.LECTERN
    # the lectern: a slanted top on a column
    boxflats(R, (a0 + a1) / 2 - 4, (a0 + a1) / 2 + 4, y0, y1 - 8, (b0 + b1) / 2 - 4, (b0 + b1) / 2 + 4, LACQUER, lit=("right",), shade_k=0.3, alpha=0.6)
    top_pts = [(a0, y1 - 10, b0), (a1, y1 - 10, b0), (a1, y1, b1), (a0, y1, b1)]
    flat3(R, top_pts, LACQUER_L, alpha=0.7)
    # the book on it: pale pages, open, its spine dark (a big book: the chanter reads it from the dais)
    bk = [(a0 - 4, y1 - 9, b0 + 1), (a1 + 4, y1 - 9, b0 + 1), (a1 + 4, y1 + 2.5, b1 - 1), (a0 - 4, y1 + 2.5, b1 - 1)]
    mb = flat3(R, bk, lerp(PAPER, NAPLES, 0.08), grp="book", alpha=0.75, amount=0.01)
    pp = V.poly([((a0 + a1) / 2 - 0.8, y1 - 9, b0 + 1), ((a0 + a1) / 2 + 0.8, y1 - 9, b0 + 1), ((a0 + a1) / 2 + 0.8, y1 + 2.5, b1 - 1), ((a0 + a1) / 2 - 0.8, y1 + 2.5, b1 - 1)])
    if len(pp) >= 3:
        R.flat2d(pp, PRUSSIAN, amount=0.01)
    return m


def rail(R, show, grp="stagerail"):
    """The rail along the stage's front: a low partition of black lacquer, a cap along its top (its lit edge)."""
    X0, X1, Z0, Z1, h = M.RAIL
    m = boxflats(R, X0, X1, 0.0, h - 4, Z0, Z1, LACQUER, grp=grp, lit=("right",), shade_k=0.15, colors={"back": lerp(LACQUER, PRUSSIAN, 0.3), "front": LACQUER})
    cap = boxflats(R, X0 - 2, X1 + 2, h - 4, h, Z0 - 2, Z1 + 2, LACQUER, grp=grp, colors={"top": LACQUER_L if not show else lerp(LACQUER_L, PAPER, 0.25),
                                                                                          "front": lerp(LACQUER, COBALT, 0.2)})
    return np.maximum(m, cap)


def curtain(R, grp="curtain"):
    """The masking curtain at the stage's left end: black cloth hung from a rod under the rafters, in folds (each fold two
    flats: its lit face toward the stage's light, its shade)."""
    X, z0, z1, foot = M.CURTAIN
    m = np.zeros(SHAPE, F32)
    n = 7
    top = M.ROOF - 30
    for i in range(n):
        za, zb = z0 + (z1 - z0) * i / n, z0 + (z1 - z0) * (i + 1) / n
        zm = (za + zb) / 2
        d = 7.0 if i % 2 == 0 else -5.0
        f1 = [(X, foot, za), (X + d, foot, zm), (X + d, top, zm), (X, top, za)]
        f2 = [(X + d, foot, zm), (X, foot, zb), (X, top, zb), (X + d, top, zm)]
        m = np.maximum(m, R.flat(f1, CURT_L, grp, amount=0.02, cell=(12, 90)))
        m = np.maximum(m, R.flat(f2, CURT, grp, amount=0.02, cell=(12, 90)))
    # the rod and its rings
    pp = V.poly([(X - 3, top, z0 - 10), (X + 3, top, z0 - 10), (X + 3, top + 5, z1 + 10), (X - 3, top + 5, z1 + 10)])
    if len(pp) >= 3:
        m = np.maximum(m, R.flat2d(pp, PLANK_D, grp, amount=0.02))
    R.thing(m, 0.85)
    return m


def gate(R, show, grp="gate"):
    """The village gate, painted scenery at stage left near the rail: two plain posts, a beam, a little roof of grey-blue
    shingles; a flat each face, the lit faces toward the light that is on the stage."""
    g = M.GATE
    z = g["z"]
    p = g["post"]
    wood = plit(lerp(lerp(OCHRE, SIENNA, 0.4), PAPER, 0.12), 0.3) if show else lerp(lerp(OCHRE, SIENNA, 0.45), PRUSSIAN, 0.12)
    m = np.zeros(SHAPE, F32)
    for x in g["x"]:
        m = np.maximum(m, boxflats(R, x - p / 2, x + p / 2, 0.0, g["h"], z - p / 2, z + p / 2, wood, grp=grp, lit=("right", "front"), shade_k=0.42))
    y0, y1 = g["beam"]
    xa, xb = g["x"][0] - 16, g["x"][1] + 16
    m = np.maximum(m, boxflats(R, xa, xb, y0, y1, z - 8, z + 8, wood, grp=grp, lit=("front", "bottom", "right"), shade_k=0.42))
    r0, r1 = g["roof"]
    o = g["over"]
    # the roof: two slopes, toward us (lit by the stage's light only in the show) and away
    near = [(xa - o, r0, z + 30), (xb + o, r0, z + 30), (xb + o, r1, z), (xa - o, r1, z)]
    far = [(xa - o, r0, z - 30), (xb + o, r0, z - 30), (xb + o, r1, z), (xa - o, r1, z)]
    m = np.maximum(m, flat3(R, far, lerp(TILE, PRUSSIAN, 0.2), grp, alpha=0.0, thing=False))
    m = np.maximum(m, flat3(R, near, plit(TILE, 0.25) if show else TILE, grp, alpha=0.0, thing=False))
    # the shingles' lines, across the near slope
    for k in range(1, 4):
        t = k / 4
        a = V.pt(xa - o, r0 + (r1 - r0) * t, z + 30 - 30 * t)
        b = V.pt(xb + o, r0 + (r1 - r0) * t, z + 30 - 30 * t)
        R.lines(np.zeros(SHAPE, F32), mask_line(SHAPE, [a, b], 0.8), 0.35)
    # the ridge
    m = np.maximum(m, boxflats(R, xa - o, xb + o, r1 - 2, r1 + 5, z - 4, z + 4, lerp(TILE, PRUSSIAN, 0.45), grp=grp, alpha=0.0, thing=False))
    R.add_mask(grp, m)
    R.thing(m, 0.85)
    return m


def housefront(R, show, grp="housefront"):
    """The house front, painted scenery at stage right, raked toward the house: white plaster panels between dark posts,
    a door at the puppets' height (on the rail's line) with an indigo noren (a plain white ring: our own mark), a lattice
    window, a tiled eave. Its face is turned toward the house and the wing; we see it at about fifty degrees."""
    h = M.HOUSEFRONT
    (x0, z0), (x1, z1) = h["p0"], h["p1"]
    L = math.hypot(x1 - x0, z1 - z0)
    ux, uz = (x1 - x0) / L, (z1 - z0) / L
    nx, nz = uz, -ux                 # the face's normal: toward the house and the wing (-X, -Z here: rotate u by -90)
    if nx > 0:
        nx, nz = -nx, -nz
    at = lambda s, y, d=0.0: (x0 + ux * L * s + nx * d, y, z0 + uz * L * s + nz * d)
    lit = show
    plaster = plit(PLASTER_SET, 0.4) if lit else lerp(PLASTER_SET, COBALT, 0.18)
    post_c = plit(POST_SET, 0.2) if lit else POST_SET
    m = np.zeros(SHAPE, F32)
    # the flat's back is backstage (we see its face): the whole face, plaster
    m = np.maximum(m, flat3(R, [at(0, 0), at(1, 0), at(1, h["h"]), at(0, h["h"])], plaster, grp, alpha=0.0, thing=False))
    # the sill along its foot (dark) up to the rail's height: the puppets' floor line
    m = np.maximum(m, flat3(R, [at(0, 0, 0.5), at(1, 0, 0.5), at(1, 86, 0.5), at(0, 86, 0.5)], lerp(post_c, PRUSSIAN, 0.25), grp, alpha=0.0, thing=False))
    # posts at its ends and between the panels
    for s in (0.0, 0.29, 0.57, 0.95):
        m = np.maximum(m, flat3(R, [at(s, 0, 1), at(s + 0.05, 0, 1), at(s + 0.05, h["eave"][0], 1), at(s, h["eave"][0], 1)], post_c, grp, alpha=0.0, thing=False))
    # the door: dark inside, the noren hanging in it
    d0, d1 = h["door"]
    dy0, dy1 = h["door_y"]
    m = np.maximum(m, flat3(R, [at(d0 + 0.01, dy0, 1.5), at(d1, dy0, 1.5), at(d1, dy1, 1.5), at(d0 + 0.01, dy1, 1.5)], lerp(SIENNA, PRUSSIAN, 0.72), grp, alpha=0.0, thing=False))
    nor = INDIGO if not lit else lerp(INDIGO, COBALT, 0.25)
    for k in range(2):
        s0 = d0 + 0.015 + (d1 - d0 - 0.02) * k / 2
        s1 = d0 + 0.005 + (d1 - d0 - 0.02) * (k + 1) / 2
        m = np.maximum(m, flat3(R, [at(s0, dy1 - 52, 2.5), at(s1, dy1 - 52, 2.5), at(s1, dy1, 2.5), at(s0, dy1, 2.5)], nor, grp, alpha=0.0, thing=False))
    # the white ring on the noren (our own mark, no lettering)
    c = V.pt(*at((d0 + d1) / 2, dy1 - 24, 3.0))
    sc = V.scale_at(at((d0 + d1) / 2, 0)[0], at((d0 + d1) / 2, 0)[2])
    ring = mask_ellipse(SHAPE, c[0], c[1], 7.5 * sc, 8.5 * sc) - mask_ellipse(SHAPE, c[0], c[1], 4.5 * sc, 5.5 * sc)
    R.fill(np.clip(ring, 0, 1), lerp(PAPER, CERULEAN, 0.15), amount=0.01, cell=10)
    # the lattice window
    w0, w1 = h["window"]
    wy0, wy1 = h["window_y"]
    m = np.maximum(m, flat3(R, [at(w0, wy0, 1.5), at(w1, wy0, 1.5), at(w1, wy1, 1.5), at(w0, wy1, 1.5)], lerp(SIENNA, PRUSSIAN, 0.6), grp, alpha=0.0, thing=False))
    for k in range(1, 6):
        s = w0 + (w1 - w0) * k / 6
        flat3(R, [at(s - 0.004, wy0, 2), at(s + 0.004, wy0, 2), at(s + 0.004, wy1, 2), at(s - 0.004, wy1, 2)], post_c, grp, alpha=0.0, thing=False)
    # the eave: a band of tiles leaning out over the face
    e0, e1 = h["eave"]
    eave = [at(-0.03, e0, 26), at(1.03, e0, 26), at(1.03, e1, 0), at(-0.03, e1, 0)]
    m = np.maximum(m, flat3(R, eave, plit(TILE, 0.25) if lit else TILE, grp, alpha=0.0, thing=False))
    for k in range(1, 3):
        t = k / 3
        a = V.pt(*at(-0.03, e0 + (e1 - e0) * t, 26 - 26 * t))
        b = V.pt(*at(1.03, e0 + (e1 - e0) * t, 26 - 26 * t))
        R.lines(np.zeros(SHAPE, F32), mask_line(SHAPE, [a, b], 0.8), 0.35)
    # its props behind (seen at its back edge): two braces to the floor
    for s in (0.1, 0.85):
        a = at(s, 150, -2)
        b = (a[0] - nx * 70, 0.0, a[2] - nz * 70)
        pp = V.poly([a, (a[0], a[1] + 6, a[2]), (b[0], 6.0, b[2]), b])
        if len(pp) >= 3:
            m = np.maximum(m, R.flat2d(pp, PLANK_S, grp, amount=0.02))
    R.add_mask(grp, m)
    R.thing(m, 0.85)
    return m


# ================================================================ the wing: its wall and the troupe's things
def wing_wall(R, info):
    """The wing's far wall (the building's outer wall, Z = 770, X -820..-100): dark planks, the lamp's warm pool on them;
    the back door open a hand's breadth on the alley's day."""
    X0, X1 = M.WALL_WING_X
    u, v, ok, fp = R.wall_uv("Z", 770.0)
    m = ok * (u >= X0) * (u <= X1) * (v >= 0) * (v <= M.ROOF_BACK)
    R.fill(m, PLANK_S, amount=0.03, cell=90)
    # the lamp's pool on the wall: a flat (an ellipse round the lamp, on the wall)
    lx, lz, lh = M.LAMP
    pool = m * ((((u - lx) / 105.0) ** 2 + ((v - lh - 10) / 78.0) ** 2) < 1.0)
    R.fill(pool, lerp(PLANK_S, lerp(PLANK, NAPLES, 0.25), 0.45), amount=0.03, cell=60)
    inner = m * ((((u - lx) / 52.0) ** 2 + ((v - lh - 10) / 40.0) ** 2) < 1.0)
    R.fill(inner, lerp(LAMPLIT, PLANK_S, 0.45), amount=0.02, cell=60)
    # plank joints, upright
    f = np.mod(u, 30.0)
    f = np.minimum(f, 30.0 - f)
    R.lines(m, np.clip(1.2 - f / 0.9, 0, 1) * m, 0.3)
    # a sill along the foot and a beam at the top
    flat3(R, quad_wall_z(X0, X1, 0, 14, 770.4), PLANK_D, alpha=0.5)
    flat3(R, quad_wall_z(X0, X1, M.ROOF_BACK - 30, M.ROOF_BACK, 770.4), PLANK_D, alpha=0.5)
    R.thing(m, 0.6)
    # the back door: its opening (the alley's daylight in the gap), the door slid nearly shut, its frame
    d0, d1, y0, y1 = M.BACKDOOR
    gap = flat3(R, quad_wall_z(d1 - M.DOOR_OPEN, d1, y0, y1, 770.5), DAY, alpha=0.0, thing=False)
    flat3(R, quad_wall_z(d0, d1 - M.DOOR_OPEN, y0, y1, 771.0), lerp(PLANK, PRUSSIAN, 0.3), alpha=0.7)
    for k in range(1, 4):
        xx = d0 + (d1 - M.DOOR_OPEN - d0) * k / 4
        pp = V.poly(quad_wall_z(xx - 0.6, xx + 0.6, y0 + 4, y1 - 4, 771.3))
        if len(pp) >= 3:
            R.flat2d(pp, PLANK_D, amount=0.01)
    for (a0, a1, b0, b1) in ((d0 - 8, d0, y0, y1 + 8), (d1, d1 + 8, y0, y1 + 8), (d0 - 8, d1 + 8, y1, y1 + 8)):
        flat3(R, quad_wall_z(a0, a1, b0, b1, 771.5), PLANK_D, alpha=0.6)
    # the day through the gap lies on the floor in a blade toward us
    xs = (d1 - M.DOOR_OPEN, d1)
    blade = [(xs[0], 771.0), (xs[1], 771.0), (xs[1] + 30, 900.0), (xs[0] + 10, 900.0)]
    pp = V.poly([(x, 0.0, z) for x, z in blade])
    if len(pp) >= 3:
        bm = mask_poly(SHAPE, pp) * info["back"]
        R.fill(bm, lerp(DAY, PLANK, 0.35), amount=0.02, cell=40, alpha=0.9)
    info["wing_wall"] = m
    info["doorgap"] = gap
    return m


def wing_things(R, info, include):
    """The troupe's things on the wing's wall and floor, far to near: the shelf of heads over two wicker boxes, the
    puppets hanging on their rail, the peg with the black robes and hoods (a cut-out: the girls take them), the lamp on
    its stand, the boy puppet on his stand (a cut-out: he goes to the stage)."""
    out = {}
    # ---- the shelf of heads: a plank on two brackets; four carved heads on their grips (white faces, black hair; one
    # an old man's, white-haired; one under a cloth)
    s0, s1, sy = M.SHELF
    flat3(R, [(s0, sy, 770.5), (s1, sy, 770.5), (s1, sy, 794.0), (s0, sy, 794.0)], lerp(PLANK, NAPLES, 0.2), alpha=0.7)
    flat3(R, quad_wall_z(s0, s1, sy - 4, sy, 794.0), PLANK_D, alpha=0.7)
    for bx in (s0 + 10, s1 - 14):
        flat3(R, [(bx, sy - 20, 771), (bx + 4, sy - 20, 771), (bx + 4, sy - 4, 790), (bx, sy - 4, 790)], PLANK_D, alpha=0.6)
    heads = []
    for k, kind in enumerate(("boy", "woman", "old", "cloth")):
        hx = s0 + 14 + k * (s1 - s0 - 24) / 3.0
        hz = 783.0
        base = V.pt(hx, sy, hz)
        sc = V.scale_at(hx, hz)
        hr = 7.5 * sc
        # the grip (a short stick) and the head on it
        R.fill(mask_line(SHAPE, [base, (base[0], base[1] - 7 * sc)], max(1.0, 2.5 * sc)), PLANK_D, amount=0.01, cell=10)
        cy = base[1] - 7 * sc - hr * 1.05
        if kind == "cloth":
            mh = ell(R, base[0], cy - hr * 0.1, hr * 1.15, hr * 1.25, lerp(INDIGO, PAPER, 0.15), alpha=0.6)
            continue
        hair = lerp(PAPER, PRUSSIAN, 0.25) if kind == "old" else HAIR
        mh = ell(R, base[0], cy, hr, hr * 1.18, hair, alpha=0.0, thing=False)
        face = mask_ellipse(SHAPE, base[0] + hr * 0.12, cy + hr * 0.2, hr * 0.72, hr * 0.88) * mh
        R.fill(face, lerp(PAPER, NAPLES, 0.12), amount=0.01, cell=10)
        if kind == "woman":
            ell(R, base[0] - hr * 0.1, cy - hr * 1.0, hr * 0.85, hr * 0.5, HAIR, thing=False)
        if kind == "boy":
            ell(R, base[0], cy - hr * 0.95, hr * 0.3, hr * 0.25, HAIR, thing=False)
        # the eyes: two small strokes, closed (a carved head at rest)
        for dx in (-0.25, 0.42):
            R.fill(mask_line(SHAPE, [(base[0] + hr * (dx - 0.12), cy + hr * 0.12), (base[0] + hr * (dx + 0.12), cy + hr * 0.12)], 0.8), PRUSSIAN, amount=0.0, cell=10)
        R.thing(mh, 0.6)
        heads.append([int(base[0]), int(cy)])
    out["heads"] = heads
    # ---- two wicker boxes under the shelf
    for (x0, x1, y0, y1, z0, z1) in M.BOXES:
        mb = boxflats(R, x0, x1, y0, y1, z0, z1, WICKER, lit=("top", "front"), shade_k=0.42)
        for t in (0.25, 0.75):                                        # dark bands round them
            xx = x0 + (x1 - x0) * t
            pp = V.poly([(xx - 2.5, y0, z1 + 0.3), (xx + 2.5, y0, z1 + 0.3), (xx + 2.5, y1 + 0.3, z1 + 0.3), (xx + 2.5, y1 + 0.3, z0), (xx - 2.5, y1 + 0.3, z0), (xx - 2.5, y1 + 0.3, z1 + 0.3)])
            if len(pp) >= 3:
                R.flat2d(pp, lerp(SIENNA, PRUSSIAN, 0.4), amount=0.01)
    # ---- the puppets hanging on their rail by their heads, quiet as coats
    r0, r1, ry = M.PUPPET_RAIL
    flat3(R, [(r0, ry, 772), (r1, ry, 772), (r1, ry + 5, 790), (r0, ry + 5, 790)], PLANK_D, alpha=0.7)
    for bx in (r0 + 8, (r0 + r1) / 2, r1 - 6):
        flat3(R, [(bx, ry - 30, 771), (bx + 4, ry - 30, 771), (bx + 4, ry, 788), (bx, ry, 788)], PLANK_D, alpha=0.6)
    kimono = {"indigo": INDIGO, "vermilion": lerp(VERMILION, SIENNA, 0.2), "ochre": lerp(OCHRE, SIENNA, 0.15), "green": lerp(VIRIDIAN, VERONESE, 0.25),
              "indigo2": lerp(INDIGO, PAPER, 0.3), "lake": lerp(LAKE, SIENNA, 0.25)}
    for (px, kind) in M.PUPPETS:
        z = 790.0
        sc = V.scale_at(px, z)
        c = kimono[kind]
        lampk = 0.5 * max(0.0, 1.0 - abs(px - M.LAMP[0]) / 200.0)
        cl = lerp(c, lerp(c, NAPLES, 0.35), lampk)
        top = ry - 4.0
        head_c = V.pt(px, top - 14, z)
        hr = 7.0 * sc
        # the cord from the rail to the head
        R.fill(mask_line(SHAPE, [V.pt(px, ry, z), V.pt(px, top - 6, z)], 0.8), PLANK_D, amount=0.0, cell=10)
        mh = ell(R, head_c[0], head_c[1], hr, hr * 1.15, HAIR, alpha=0.0, thing=False)
        R.fill(mask_ellipse(SHAPE, head_c[0], head_c[1] + hr * 0.25, hr * 0.7, hr * 0.85) * mh, lerp(PAPER, NAPLES, 0.12), amount=0.0, cell=10)
        # the kimono hanging limp: shoulders, sleeves, the long fall to the hem (no feet: the costume hangs empty)
        sh = top - 24.0
        body = [(px - 16, sh, z), (px + 16, sh, z), (px + 13, sh - 74, z + 1), (px - 13, sh - 74, z + 1)]
        mk = flat3(R, body, shade_of(cl, 0.25), alpha=0.0, thing=False)
        R.flat([(px + 1, sh, z + 0.5), (px + 16, sh, z + 0.5), (px + 13, sh - 74, z + 1.5), (px + 1, sh - 74, z + 1.5)], cl, amount=0.02)
        for sgn in (-1, 1):
            sl = [(px + sgn * 16, sh, z + 1), (px + sgn * 26, sh - 6, z + 2), (px + sgn * 24, sh - 40, z + 2), (px + sgn * 15, sh - 36, z + 1)]
            mk = np.maximum(mk, flat3(R, sl, shade_of(cl, 0.32) if sgn < 0 else cl, alpha=0.0, thing=False))
        # the sash: a band across the waist
        R.flat([(px - 14, sh - 30, z + 2), (px + 14, sh - 30, z + 2), (px + 14, sh - 38, z + 2), (px - 14, sh - 38, z + 2)], lerp(OCHRE, NAPLES, 0.3) if kind != "ochre" else INDIGO, amount=0.01)
        R.thing(np.maximum(mk, mh), 0.7)
    # ---- the peg with the two black robes and hoods (the cut-out `robes`; the peg itself stays in the backdrop)
    px, py = M.PEG
    flat3(R, [(px - 2, py - 2, 771), (px + 2, py - 2, 771), (px + 2, py + 2, 784), (px - 2, py + 2, 784)], PLANK_D, alpha=0.6)
    if "robes" in include:
        x0, x1, y0, y1 = M.ROBES
        m = np.zeros(SHAPE, F32)
        for k, (a, b, low) in enumerate(((x0, x0 + 44, y0 + 6), (x1 - 46, x1, y0))):
            z = 776.0 + k * 4
            robe = [(px - 3, y1, z), ((a + b) / 2 + 3, y1 - 2, z), (b, y1 - 22, z), (b + 2, low, z + 1), (a - 1, low + 3, z + 1), (a, y1 - 20, z)]
            m = np.maximum(m, R.flat(robe, BLACK_ROBE if k == 0 else lerp(BLACK_ROBE, ULTRA, 0.12), "robes", amount=0.02, cell=(12, 60)))
            # a fold: the lit edge of the robe toward the lamp
            fold = [((a + b) / 2, y1 - 10, z + 0.5), ((a + b) / 2 + 5, y1 - 10, z + 0.5), ((a + b) / 2 + 7, low + 4, z + 1.5), ((a + b) / 2 + 1, low + 4, z + 1.5)]
            R.flat(fold, lerp(BLACK_ROBE, COBALT, 0.3), "robes", amount=0.01)
        # the two hoods, hung over the peg: soft black cloths
        for k, dx in enumerate((-9.0, 7.0)):
            hood = [(px + dx - 9, py + 4, 786 + k), (px + dx + 9, py + 4, 786 + k), (px + dx + 11, py - 30, 787 + k), (px + dx - 11, py - 30, 787 + k)]
            m = np.maximum(m, R.flat(hood, lerp(BLACK_ROBE, PRUSSIAN, 0.2) if k == 0 else lerp(BLACK_ROBE, ULTRA, 0.2), "robes", amount=0.02, cell=(12, 60)))
        R.thing(m, 0.8)
        out["robes"] = m
    # ---- the lamp on its stand: a square foot, a post, the oil dish at the top (its flame is the engine's: fx)
    lx, lz, lh = M.LAMP
    if "lamp" in include:
        boxflats(R, lx - 14, lx + 14, 0, 5, lz - 14, lz + 14, PLANK_D, grp="lamp", lit=("top",), alpha=0.6)
        cyl(R, lx, lz, 2.6, 5.0, lh, lerp(PLANK, NAPLES, 0.2), grp="lamp", lit_side=1.0, lit_share=0.35, alpha=0.7)
        cyl(R, lx, lz, 8.0, lh, lh + 3.0, lerp(OCHRE, NAPLES, 0.3), grp="lamp", alpha=0.7)
    out["flame"] = ipt(V.pt(lx + 3.0, lh + 7.0, lz))
    # its pool on the floor: a flat round its foot
    pool = [(lx + 80 * math.cos(q), lz + 52 * math.sin(q)) for q in np.linspace(0, 2 * math.pi, 28, endpoint=False)]
    pp = V.poly([(x, 0.0, z) for x, z in pool])
    pm = mask_poly(SHAPE, pp) * info["back"]
    R.fill(pm, lerp(BACKFLOOR, LAMPLIT, 0.30), amount=0.02, cell=60, alpha=0.95)
    floor_shadow(R, [(lx - 3, lz), (lx + 3, lz), (lx + 14, lz + 60), (lx + 6, lz + 64)], 0.3, info["back"])
    # ---- the boy puppet's stand (a post on a cross foot, a bar at its top) and the boy hung on it (the cut-out)
    sx, sz = M.STAND
    for dx, dz in ((-24, 0), (0, -24)):
        boxflats(R, sx - 24 if dx else sx - 3, sx + 24 if dx else sx + 3, 0, 5, sz - 3 if dx else sz - 24, sz + 3 if dx else sz + 24, PLANK_S, alpha=0.6)
    cyl(R, sx, sz, 3.0, 5.0, M.STAND_H, PLANK, lit_side=-1.0, lit_share=0.35, alpha=0.7)
    boxflats(R, sx - 22, sx + 22, M.STAND_H, M.STAND_H + 5, sz - 3, sz + 3, PLANK, alpha=0.7)
    floor_shadow(R, [(sx - 24, sz), (sx + 24, sz), (sx + 40, sz + 46), (sx - 8, sz + 50)], 0.28, info["back"])
    if "boypuppet" in include:
        out["boypuppet"] = boy_puppet(R, sx, sz + 6.0)
    return out


def boy_puppet(R, sx, sz, grp="boypuppet"):
    """The boy puppet on his stand: 0.9 m, hung from the bar by his shoulders, his feet a little off the floor: a carved
    head (a boy's forelock), an indigo kimono with a pale splash pattern (our own), an ochre sash, white socks."""
    m = np.zeros(SHAPE, F32)
    top = M.STAND_H + 2.0
    z = sz
    lampk = 0.35
    kim = lerp(INDIGO, lerp(INDIGO, NAPLES, 0.3), lampk)
    # legs and feet: white socks, dangling
    for dx in (-5.0, 5.0):
        m = np.maximum(m, R.flat([(sx + dx - 3, top - 82, z), (sx + dx + 3, top - 82, z), (sx + dx + 3, top - 64, z), (sx + dx - 3, top - 64, z)], lerp(PAPER, NAPLES, 0.15), grp, amount=0.01))
        m = np.maximum(m, R.flat([(sx + dx - 3, top - 87, z + 2), (sx + dx + 4, top - 87, z + 2), (sx + dx + 4, top - 82, z + 1), (sx + dx - 3, top - 82, z + 1)], lerp(PAPER, NAPLES, 0.2), grp, amount=0.01))
    # the kimono: shoulders on the bar, a short fall (a boy's, to the shins)
    sh = top - 14.0
    body = [(sx - 13, sh, z + 3), (sx + 13, sh, z + 3), (sx + 12, sh - 52, z + 4), (sx - 12, sh - 52, z + 4)]
    m = np.maximum(m, R.flat(body, shade_of(kim, 0.2), grp, amount=0.02, cell=(12, 60)))
    m = np.maximum(m, R.flat([(sx - 13, sh, z + 3.5), (sx - 1, sh, z + 3.5), (sx - 1, sh - 52, z + 4.5), (sx - 12, sh - 52, z + 4.5)], kim, grp, amount=0.02, cell=(12, 60)))
    # sleeves hanging, the hands (white) at their ends
    for sgn in (-1, 1):
        sl = [(sx + sgn * 13, sh, z + 4), (sx + sgn * 21, sh - 4, z + 4), (sx + sgn * 20, sh - 30, z + 4), (sx + sgn * 12, sh - 28, z + 4)]
        m = np.maximum(m, R.flat(sl, kim if sgn < 0 else shade_of(kim, 0.25), grp, amount=0.02))
        hand = V.pt(sx + sgn * 17, sh - 33, z + 4)
        sc = V.scale_at(sx, z)
        m = np.maximum(m, ell(R, hand[0], hand[1], 2.6 * sc, 3.0 * sc, lerp(PAPER, NAPLES, 0.15), grp, alpha=0.0, thing=False))
    # the splash pattern: small pale crosses on the kimono (our own pattern)
    sc = V.scale_at(sx, z)
    for (dx, dy) in ((-7, -12), (5, -20), (-3, -33), (8, -42), (-9, -46)):
        c = V.pt(sx + dx, sh + dy, z + 5)
        R.fill(mask_line(SHAPE, [(c[0] - 1.6 * sc, c[1]), (c[0] + 1.6 * sc, c[1])], 0.9) * m, lerp(PAPER, CERULEAN, 0.2), amount=0.0, cell=10)
        R.fill(mask_line(SHAPE, [(c[0], c[1] - 1.6 * sc), (c[0], c[1] + 1.6 * sc)], 0.9) * m, lerp(PAPER, CERULEAN, 0.2), amount=0.0, cell=10)
    # the sash
    m = np.maximum(m, R.flat([(sx - 12.5, sh - 20, z + 5), (sx + 12.5, sh - 20, z + 5), (sx + 12.5, sh - 26, z + 5), (sx - 12.5, sh - 26, z + 5)], lerp(OCHRE, NAPLES, 0.35), grp, amount=0.01))
    # the head: a carved boy's head (white face, black hair, a forelock), over the bar
    hc = V.pt(sx, top + 2, z + 3)
    hr = 7.0 * sc
    mh = ell(R, hc[0], hc[1], hr, hr * 1.15, HAIR, grp, alpha=0.0, thing=False)
    R.fill(mask_ellipse(SHAPE, hc[0] - hr * 0.1, hc[1] + hr * 0.25, hr * 0.72, hr * 0.85) * mh, lerp(PAPER, NAPLES, 0.15), amount=0.01, cell=10)
    ell(R, hc[0] - hr * 0.2, hc[1] - hr * 0.95, hr * 0.42, hr * 0.3, HAIR, grp, thing=False)
    for dx in (-0.35, 0.2):
        R.fill(mask_line(SHAPE, [(hc[0] + hr * (dx - 0.12), hc[1] + hr * 0.18), (hc[0] + hr * (dx + 0.12), hc[1] + hr * 0.18)], 0.8), PRUSSIAN, amount=0.0, cell=10)
    m = np.maximum(m, mh)
    R.add_mask(grp, m)
    R.thing(m, 0.8)
    return m


def front(R, info, grp="front"):
    """The front plane: the troupe's wicker boxes stacked at the bottom right (behind the stage), cut by the picture's
    edge, darker and warmer than the middle of the room."""
    m = np.zeros(SHAPE, F32)
    for (x0, x1, y0, y1, z0, z1) in ((300, 420, 0, 50, 1240, 1320), (312, 410, 50, 92, 1248, 1312), (430, 600, 0, 44, 1236, 1316),
                                     (450, 570, 44, 84, 1244, 1306), (190, 290, 0, 40, 1300, 1370)):
        m = np.maximum(m, boxflats(R, x0, x1, y0, y1, z0, z1, lerp(WICKER, SIENNA, 0.25), grp=grp, lit=("top", "front"), shade_k=0.45))
        for t in (0.2, 0.8):
            xx = x0 + (x1 - x0) * t
            pp = V.poly([(xx - 3, y0, z1 + 0.3), (xx + 3, y0, z1 + 0.3), (xx + 3, y1 + 0.3, z1 + 0.3), (xx + 3, y1 + 0.3, z0), (xx - 3, y1 + 0.3, z0), (xx - 3, y1 + 0.3, z1 + 0.3)])
            if len(pp) >= 3:
                m = np.maximum(m, R.flat2d(pp, lerp(SIENNA, PRUSSIAN, 0.5), grp, amount=0.01))
    R.add_mask(grp, m)
    return m


def stage_back(R, info):
    """The stage's back edge, where the polished boards meet the backstage floor: a dark sill across it; at its right end a
    post up to the backstage ceiling, with a black curtain (drawn back for the day) bunched against it."""
    x0, x1, z0, z1 = M.STAGE
    flat3(R, [(x0, 0.6, z1 - 6), (x1, 0.6, z1 - 6), (x1, 0.6, z1 + 6), (x0, 0.6, z1 + 6)], PLANK_D, alpha=0.6)
    cyl(R, x1 + 14, z1 + 10, 9.0, 0.0, M.ROOF_BACK, PLANK_S, lit_side=-1.0, lit_share=0.3, alpha=0.8)
    m = np.zeros(SHAPE, F32)
    for k in range(5):
        xa = x1 - 8 - k * 9.0
        d = 6.0 if k % 2 == 0 else -4.0
        m = np.maximum(m, R.flat([(xa, 4.0, z1 + 12 + d), (xa - 9, 4.0, z1 + 12 - d), (xa - 9, M.ROOF_BACK - 30, z1 + 12 - d), (xa, M.ROOF_BACK - 30, z1 + 12 + d)],
                                CURT if k % 2 else CURT_L, amount=0.02, cell=(12, 90)))
    R.thing(m, 0.8)
    floor_shadow(R, [(x1 - 50, z1 + 10), (x1 + 20, z1 + 10), (x1 + 40, z1 + 70), (x1 - 60, z1 + 70)], 0.3, info["back"])


def backstage_ceiling(R):
    """The backstage room's lower ceiling of boards on joists, over our heads: its dark edge across the top of the
    picture, where the hall's higher roof begins."""
    X, Z, ok, fp = R.floor_uv(M.ROOF_BACK)
    m = ok * (X >= M.WING[0]) * (X <= M.HALL_X1) * (Z >= M.WING[3]) * (Z <= 2000.0)
    m2 = ok * (X >= M.WING[0]) * (X <= -100.0) * (Z >= 770.0) * (Z <= M.WING[3])
    m = np.clip(m + m2, 0, 1)
    R.fill(m, lerp(SIENNA, PRUSSIAN, 0.7), amount=0.03, cell=90)
    # its edge: a deep beam (the head of the opening onto the stage)
    zb = M.WING[3]
    flat3(R, [(-100.0, M.ROOF_BACK - 34, zb), (M.HALL_X1, M.ROOF_BACK - 34, zb), (M.HALL_X1, M.ROOF_BACK, zb), (-100.0, M.ROOF_BACK, zb)], PLANK_D, alpha=0.7)
    flat3(R, [(-100.0, M.ROOF_BACK - 34, 770.0), (-100.0, M.ROOF_BACK - 34, zb), (-100.0, M.ROOF_BACK, zb), (-100.0, M.ROOF_BACK, 770.0)], PLANK_D, alpha=0.7)
    R.thing(m, 0.5)
    return m


# ================================================================ the whole picture
CUTS = ("curtain", "stagerail", "gate", "housefront", "robes", "lamp", "boypuppet", "front")


def render(show=False, include=CUTS, seed=1):
    R = Room(V, seed=seed, base=lerp(SIENNA, PRUSSIAN, 0.8))
    info = shell(R, show)
    daylight(R, info, show)
    info["audience"] = audience(R, info, show)
    dais(R, show)
    # the stage: shadows of the rail's foot (a thin dark flat along it on the stage side)
    floor_shadow(R, [(0, 782), (M.RAIL[1], 782), (M.RAIL[1], 798), (0, 798)], 0.35, info["stage"])
    if "stagerail" in include:
        rail(R, show)
    wing_wall(R, info)
    things = wing_things(R, info, include)
    info.update(things)
    if "curtain" in include:
        curtain(R)
    # the set's shadows on the boards (laid away from the stage window's light: toward -X)
    g = M.GATE
    for x in g["x"]:
        floor_shadow(R, [(x - 6, g["z"] - 6), (x + 6, g["z"] - 6), (x - 60, g["z"] + 40), (x - 72, g["z"] + 34)], 0.3 if show else 0.18, info["stage"])
    if "gate" in include:
        gate(R, show)
    if "housefront" in include:
        housefront(R, show)
    stage_back(R, info)
    backstage_ceiling(R)
    if "front" in include:
        front(R, info)
    return R, info


PASS = Passes(seed=21)
# the cut-outs, in the order they are drawn (far to near where they could overlap): each is taken where it shows
ORDER = ["stagerail", "robes", "lamp", "boypuppet", "curtain", "gate", "housefront", "front"]
SHOW_TWINS = ["gate", "housefront"]          # the set, lit in the show (the rail, the curtain and the rest do not change)


def paint(R, fast):
    pic = R.img.copy()
    if not fast:
        pic = PASS.paint(pic, keep=0.30)
    pic = R.contours(pic)
    return np.clip(pic, 0, 1)


def visible(R_all, R_back, names):
    """Each cut-out's alpha: where it is drawn (its group's mask) and the picture with it differs from the one without
    any (so a nearer thing of the backdrop hides it), less where a nearer cut-out lies over it."""
    diff = np.abs(R_all.img - R_back.img).sum(axis=2) > 1e-4
    out = {}
    nearer = np.zeros(SHAPE, bool)
    for n in reversed(ORDER):
        m = R_all.masks.get(n, np.zeros(SHAPE, F32)) >= 0.5
        if n in names:
            out[n] = (m & (diff | (n == "front")) & ~nearer).astype(F32)
        nearer |= m
    return out


def dilate(m, r):
    import cv2
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return cv2.dilate(m.astype(np.uint8), k) > 0


def relayout():
    """layout.json again from the painted files in out/edo-theatre/ (their alphas) and the model, without painting."""
    import edo_theatre_layout as L
    from PIL import Image
    pictures = {"back": (None, None)}
    for n in ORDER + ["show"] + [t + "-show" for t in SHOW_TWINS]:
        pictures[n] = (None, np.asarray(Image.open(f"{OUT}/{n}.png").convert("RGBA"), np.float32)[..., 3] / 255.0)
    lx, lz, lh = M.LAMP
    info = {"flame": ipt(V.pt(lx + 3.0, lh + 7.0, lz))}
    with open(f"{OUT}/layout.json", "w") as f:
        json.dump(L.layout(V, pictures, info, info, None), f, indent=1)
    print("layout.json written")


def main():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "relayout":
        relayout()
        return
    fast = mode == "fast"
    if fast:
        Rb, info_b = render(show=False)
        Rs, info_s = render(show=True)
        to_image(paint(Rb, True)).save(f"{WORK}/before.png")
        to_image(paint(Rs, True)).save(f"{WORK}/show.png")
        print("fast", round(time.time() - t0, 1), "s; audience", info_b["audience"])
        return
    from edo_theatre_kit import strokes_shared, finish_shared
    import edo_theatre_layout as L
    rooms = {}
    for show in (False, True):
        for whole in (True, False):
            R, info = render(show=show, include=CUTS if whole else ())
            rooms[(show, whole)] = (R, info)
    print("rendered", round(time.time() - t0, 1))
    keys = [(False, True), (False, False), (True, True), (True, False)]
    brushed = strokes_shared([rooms[k][0].img for k in keys], sizes=(9, 5, 2), seed=21, density=1.4, jitter=0.025, keep=0.30)
    pics = {k: np.clip(rooms[k][0].contours(b), 0, 1) for k, b in zip(keys, brushed)}
    print("brushed", round(time.time() - t0, 1))
    (RA, iA), (RB, iB) = rooms[(False, True)], rooms[(False, False)]
    (RAs, iAs), (RBs, iBs) = rooms[(True, True)], rooms[(True, False)]
    cut = visible(RA, RB, ORDER)
    cut_s = visible(RAs, RBs, SHOW_TWINS)
    # the show: the backdrop in the show's light, where it differs from the backdrop before it, and a wide margin round
    # that (the paints' marks read the forms within about a hundred pixels: past that the two are the same)
    changed = np.abs(RB.img - RBs.img).sum(axis=2) > 0.01
    show_a = dilate(changed, 60).astype(F32)
    pictures = {"back": (pics[(False, False)], None)}
    for n in ORDER:
        pictures[n] = (pics[(False, True)], cut[n])
    pictures["show"] = (pics[(True, False)], show_a)
    for n in SHOW_TWINS:
        # the twin covers its first state wholly: the union of the two alphas
        a = np.maximum(cut_s[n], cut[n])
        pictures[n + "-show"] = (pics[(True, True)], a)
        pictures[n] = (pics[(False, True)], a)
    # the daylight in the air: light pictures for the live layer (RGBA, soft), keyed as frames
    lights = L.shafts(V, iA, iAs)
    sizes = finish_shared(OUT, pictures, colors=160, seed=9)
    for name, (rgb_, a, hulls) in lights.items():
        save_rgba(f"{OUT}/{name}.png", rgb_, a)
    lay = L.layout(V, pictures, iA, iAs, rooms)
    with open(f"{OUT}/layout.json", "w") as f:
        json.dump(lay, f, indent=1)
    # comps to look at: before, and the show
    from PIL import Image
    for label, names in (("before", ["back"] + ORDER), ("show", ["back", "show"] + [n + "-show" if n in SHOW_TWINS else n for n in ORDER])):
        im = Image.open(f"{OUT}/{names[0]}.png").convert("RGBA")
        for n in names[1:]:
            im.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
        im.convert("RGB").save(f"{WORK}/comp-{label}.png")
    print("done", round(time.time() - t0, 1), "s;", {k: v // 1024 for k, v in sizes.items()}, "KB")


if __name__ == "__main__":
    main()

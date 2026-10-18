"""Everything in the ceiling space over the Office's ground floor, built in its own centimetres (office_ducts.py,
OFFICE-17B; drawn again as a section in OFFICE-17B2).

Each function puts one group of things on the Stage (office_ducts_kit.Stage): boxes, rods, round things and flat
pieces, each with a material that paints it in ITS OWN measurements (the duct's seams every so many centimetres, the
tiles' grid two feet square, the cinder blocks' courses), so that every line runs to the one vanishing point. All the
measurements are the model's (office_ducts_model.py), so the skeleton, the picture and layout.json agree.

Groups (grp): "back" is the backdrop; "fan" is the B-7 fan's blades and hub, a cut-out of its own (four frames turning,
one stopped).

OFFICE-17B2: THE CUT IS DRAWN AS A SECTION IS. Every wall of the duct, the intake run and the B-7 shaft is a double skin
(office_ducts_model.SHELL): where the section plane (Z = CUT) cuts it, its face toward us shows the cut sheet bright on
both sides of a thin hatched core, painted as drawn (the kit's flag 4: no lamp changes it), so that the cut is one clean
outline round the tube: down the run's wall, along the duct's top, up and down the shaft's wall, along the duct's floor.
The joists, the deck, the tiles, the light fittings and the insulation are cut by the same plane and show their cut
faces (end grain, fibre, the fittings' tubes alight in section, pink fluff). Below the tiles' cut line the rooms are not
drawn: the light of the fittings falls into them, soft, from the line."""

import math

import numpy as np

from brush import F32
import office_ducts_model as M
import office_letters as LT
from office_ducts_kit import col, mixc, fbm, hashf, band, lay, sstep

# ---------------------------------------------------------------- the colours of things, before any light falls on them
GALV = "#a9afb3"             # galvanized sheet: a cool light grey with its crystals
GALV_D = "#5d636a"           # its seams, the dark of a joint
DUST = "#b8b2a6"             # the dust along the floor: a warm pale grey
STENCIL = "#26262c"          # black stencil paint
STENCIL_RED = "#a8382c"      # the B-7 stencil: a worn red
TILE_BACK = "#aaa190"        # the backs of the ceiling tiles: fibre board, grey-buff
TBAR = "#e4e2dc"             # the grid's tees, white enamel
FIXTURE = "#d6d4cc"          # a light fitting's housing, white enamel gone dusty
PINK = "#e0909f"             # the insulation
PINK_D = "#b8607c"
BLOCK = "#8e8984"            # cinder block
MORTAR = "#6e6a66"
WOOD = "#98764e"             # the joists and the deck: fir
WOOD_D = "#7a5434"
COPPER = "#c4834e"           # the water pipe, a little tarnished
COPPER_D = "#6e5446"
RED = "#b33a2c"              # the valve's handwheel
CONDUIT = "#9a9ea2"
ROD = "#6a6e74"
CUP = "#ece8de"
CUP_BAND = "#3c5a8a"
COFFEE = "#3a2418"
PENCIL = "#e8b432"
PENCIL_WOOD = "#d8b48a"
ERASER = "#d88a8a"
FERRULE = "#c8c0a0"
WRAP = "#ddd6c2"             # a sandwich wrapper, waxed paper with a faded print
WRAP_PRINT = "#b85a3a"
FLUO = "#f2f2d2"             # fluorescent light: warm white with a little green in it
DAYLIGHT = "#fff2d6"
BELOW = "#1e1b34"            # under the tiles' cut line: the rooms, not drawn (their light falls into them from the line)
FAN = "#b2b8be"              # the fans' blades, painted grey steel
FAN_D = "#4e545c"
HUB = "#6c7278"
# the section's own colours: what the plane cuts, painted as drawn
CUT_SHEET = "#e9edf0"        # a cut sheet's edge on the inside of a tube: fresh bright metal, catching the tube's light
CUT_OUT = "#4c505a"          # the outer sheet's cut edge, toward the dark of the ceiling space
CUT_CORE = "#23242e"         # the core between the skins
CUT_HATCH = "#6c717c"        # its hatching
CUT_LIT = "#fbfbe8"          # a cut edge over a grille, where the room's light catches it

CUT_FLAG = {"front": 4, "*": 0}                         # a cut face is painted as drawn; every other face is lit


def P3(X, Y, Z):
    return (float(X), float(Y), float(Z))


def gq(c, *names):
    """The softness (a picture pixel's worth) of each named measurement on this surface."""
    return [getattr(c, "g" + n) * c.ss for n in names]


def is_cut(c):
    """A face of a box that lies on the section plane, facing us: cut."""
    return c.face == "front" and abs(c.box[5] - M.CUT) < 0.01


def ones(c):
    return np.ones((len(c.X), 1), F32)


def spangle(u, v, seed=0):
    """Galvanizing's crystals: flat patches a few centimetres across, each a shade lighter or darker."""
    cells = np.floor(fbm(u / 7.0, v / 7.0, seed, 2) * 7.0)
    return (hashf(cells.astype(np.int64) + seed * 13, seed) - 0.5).astype(F32)


def rivets(X, Y, xs=None, ys=None, step=6.0, r=1.05, g=0.5, along="y"):
    """Round rivet heads in a row on a wall: (highlight, shadow) coverage. A row up a line X = x (along "y") or along a
    line Y = y (along "x"), one every `step` cm."""
    hi = np.zeros(X.shape, F32)
    lo = np.zeros(X.shape, F32)
    lines = xs if along == "y" else ys
    for v0 in lines:
        if along == "y":
            u, w = X - v0, Y
        else:
            u, w = Y - v0, X
        k = np.round(w / step)
        dw = w - k * step
        d = np.hypot(u, dw)
        head = np.clip((r - d) / g + 0.5, 0, 1)
        hi = np.maximum(hi, head * np.clip(0.6 - (u + dw) / (r * 1.4), 0, 1))                 # lit from the upper left
        lo = np.maximum(lo, np.clip((r * 1.25 - np.hypot(u - 0.5, dw + 0.5)) / g + 0.5, 0, 1) * (1 - head))   # its shadow
    return hi, lo


# ---------------------------------------------------------------- stencils (textures on the walls, in centimetres)
def _stencils():
    out = {}
    for gid, label, gx in M.GRILLES:
        cap = M.STENCIL_Y[1] - M.STENCIL_Y[0]
        w = LT.width(label, cap, 0.34, 1.25) + 8.0
        tex, texel = LT.stencil_texture([label], cap, 1.9, (w, cap + 6.0), texel=6.0, seed=hash(gid) % 97)
        out[gid] = (tex, texel, gx - w / 2.0 + 14.0, M.STENCIL_Y[1] + 3.0)     # (its top left: X, Y measured down from here)
    # the airflow arrows between the grilles, small
    tex, texel = LT.stencil_texture(["AIR →"], 6.0, 1.1, (40.0, 12.0), texel=6.0, seed=5)
    out["air"] = (tex, texel, None, None)
    # the B-7 shaft's stencil, on its back wall beside the duct's mouth (OFFICE-17B2: where it is seen from the duct)
    lines = ["B-7 EXHAUST", "· SOUNDPROOFED ·", "AUTHORIZED", "AIR ONLY"]
    tex, texel = LT.stencil_texture(lines, 9.0, 1.8, (134.0, 70.0), texel=5.0, seed=11, line_gap=1.62)
    out["b7"] = (tex, texel, M.B7_STENCIL["X"], M.B7_STENCIL["Y"])
    return out


STENCILS = _stencils()
AIR_AT = [(273.0, 30.0), (537.0, 30.0)]                # where the small AIR arrows are (X of their left end, Y of their top)


def stencil_on(c, X, Y):
    """The stencils' paint on a back wall at (X, Y): (coverage, which colour)."""
    cov = np.zeros(X.shape, F32)
    for gid, _, gx in M.GRILLES:
        tex, texel, x0, y0 = STENCILS[gid]
        cov = np.maximum(cov, LT.sample_texture(tex, texel, X, y0 - Y, x0, 0.0))
    tex, texel, _, _ = STENCILS["air"]
    for ax, ay in AIR_AT:
        cov = np.maximum(cov, LT.sample_texture(tex, texel, X, ay - Y, ax, 0.0) * 0.8)
    return cov


# ---------------------------------------------------------------- the section: cut faces, painted as drawn
def lit_over_grille(X, gX, pad=4.0):
    """How much a cut edge at X is in a grille's light (the bars rise from the grille and catch the duct's top)."""
    out = np.zeros(X.shape, F32)
    for _, _, gx in M.GRILLES:
        out = np.maximum(out, band(X, gx - M.GRILLE_L / 2 - pad, gx + M.GRILLE_L / 2 + pad, gX * 6.0))
    return out


def m_cut_skin(c, lit=False, outer=False):
    """A skin of galvanized sheet where the plane cuts it: on the inside of a tube a fresh bright edge (over a grille the
    room's light catches it, on the duct's inside top); on the outside a dark one, so that the bright line runs round
    the inside of every tube and the ceiling space is not framed in light. Painted as drawn."""
    n = fbm(c.X / 9.0, c.Y / 9.0, 151, 2)
    if outer:
        return col(CUT_OUT) * (0.94 + 0.08 * n[..., None])
    if lit:                                                            # the duct's top: its inner edge lit over the grilles
        gX = gq(c, "X")[0]
        base = col(mixc(CUT_SHEET, "#9ca2aa", 0.35)) * (0.94 + 0.08 * n[..., None])
        return lay(base, CUT_LIT, lit_over_grille(c.X, gX))
    return col(CUT_SHEET) * (0.94 + 0.08 * n[..., None])


def joint_lines(c):
    """Where a band of the cut crosses one of the tube's joints: (distance, softness). A band along X (the duct's top and
    floor) meets the transverse joints; a band up Y (the run's wall, the shaft's) meets the flanged rings every metre and
    a half."""
    x0, x1, y0, y1, _, _ = c.box
    gX, gY = gq(c, "X", "Y")
    if (x1 - x0) >= (y1 - y0):
        d = np.min(np.abs(c.X[..., None] - np.asarray(M.JOINTS, F32)[None, :]), axis=1)
        return d, gX
    if x0 >= M.SHAFT_X[0] - M.SHELL - 0.5:
        jy = (c.Y + 40.0) / 150.0
    else:
        jy = (c.Y - M.DUCT_H) / 150.0
    return np.abs(jy - np.round(jy)) * 150.0, gY


def m_cut_core(c):
    """The core between the skins, cut: dark, hatched at 45 degrees (a section's sign for what is cut through); where
    the band crosses one of the tube's joints, the flange's two plates, bright, across it."""
    gX, gY = gq(c, "X", "Y")
    g = np.maximum(gX, gY)
    u = (c.X + c.Y) / 3.1
    d = np.abs(u - np.round(u)) * 3.1
    hatch = np.clip((0.55 - d) / (g * 1.0) + 0.5, 0, 1)
    base = col(CUT_CORE) * (0.95 + 0.1 * fbm(c.X / 6.0, c.Y / 6.0, 153, 2)[..., None])
    base = lay(base, CUT_HATCH, hatch * 0.85)
    dj, gj = joint_lines(c)
    return lay(base, "#c8ccd2", band(dj, 0.0, 1.5, gj) * 0.9)


def skin_mat(face_mat, lit=False, outer=False):
    """A skin of the double wall: its face toward the inside (or the outside) painted by `face_mat`, its cut edge bright
    (the inner skin) or dark (the outer)."""
    def f(c):
        if is_cut(c):
            return m_cut_skin(c, lit, outer)
        return face_mat(c)
    return f


def m_core(c):
    if is_cut(c):
        return m_cut_core(c)
    return col("#8a9096") * ones(c)                                    # (never seen but at a grille's opening: its collar)


def shell(st, x0, x1, y0, y1, z0, z1, axis, inside_high, face_in, face_out, name, lit=False, shadow=True, ends=(False, False)):
    """A wall of the double skin as three layers across `axis` ("x": a wall standing up, its length up Y; "y": a wall
    lying along X): the inner skin (its face toward the inside painted by face_in), the core, the outer skin (face_out).
    inside_high: the inside is on the high side of the axis. ends: at the low / the high end of the wall's length, does
    it turn a corner? There the core and the outer skin stop short, so that the inner skins meet the inner skins and the
    outer the outer, and the cut's outline runs round the corner unbroken. One shadow box for the three."""
    S = M.SKIN
    lo, hi = (x0, x1) if axis == "x" else (y0, y1)
    if inside_high:
        layers = [(hi - S, hi, skin_mat(face_in, lit), "in"), (lo + S, hi - S, m_core, "core"), (lo, lo + S, skin_mat(face_out, outer=True), "out")]
    else:
        layers = [(lo, lo + S, skin_mat(face_in, lit), "in"), (lo + S, hi - S, m_core, "core"), (hi - S, hi, skin_mat(face_out, outer=True), "out")]
    for a, b, mat, which in layers:
        if axis == "x":
            ya, yb = (y0, y1) if which == "in" else _trim(y0, y1, ends, which)
            st.box(a, b, ya, yb, z0, z1, mat, name=name, shadow=False, flag=CUT_FLAG)
        else:
            xa, xb = (x0, x1) if which == "in" else _trim(x0, x1, ends, which)
            st.box(xa, xb, a, b, z0, z1, mat, name=name, shadow=False, flag=CUT_FLAG)
    if shadow:
        st.occ.append((x0, x1, y0, y1, z0, z1)); st.occ_grp.append("back")


def _trim(a, b, ends, which):
    """The core stops a skin's thickness short of a corner's inner line, the outer skin a whole shell's less a skin."""
    S, K = M.SKIN, M.SHELL
    d = S if which == "core" else K - S
    return a + (d if ends[0] else 0.0), b - (d if ends[1] else 0.0)


# ---------------------------------------------------------------- the duct's sheet metal
def m_sheet(c):
    """Galvanized sheet, any face seen from outside: its crystals, a little grime."""
    u = c.X + c.Z * 0.7
    v = c.Y + c.Z * 0.3
    s = spangle(u, v, 3)
    g = fbm(u / 40.0, v / 40.0, 5, 3)
    return col(GALV) * (0.93 + 0.10 * s[..., None]) * (0.86 + 0.16 * g[..., None])


def tube_out(kind):
    """The outside of the run's wall or the shaft's, the face toward the ceiling space (seen going back from the cut):
    galvanized, a flanged ring every metre and a half with its rivets, so that each reads as a tube standing in the
    ceiling space."""
    def f(c):
        if is_cut(c):
            return m_cut_skin(c, outer=True)
        Y, Z = c.Y, c.Z
        gY, gZ = gq(c, "Y", "Z")
        s = spangle(Z, Y, 43)
        base = col(GALV) * (0.93 + 0.09 * s[..., None]) * (0.88 + 0.16 * fbm(Z / 40, Y / 60, 45, 2)[..., None])
        jy = ((Y + 40.0) if kind == "shaft" else (Y - M.DUCT_H)) / 150.0
        d = np.abs(jy - np.round(jy)) * 150.0
        on = (Y > M.DUCT_H + M.SHELL + 6.0) | (Y < -M.SHELL - 6.0)
        base = lay(base, GALV_D, band(d, 0, 1.6, gY) * 0.85 * on)
        base = lay(base, "#d6dadd", band(d, 1.6, 3.0, gY) * 0.6 * on)
        rings = (np.arange(-6, 7) * 150.0 - 40.0) if kind == "shaft" else (np.arange(0, 6) * 150.0 + M.DUCT_H)
        hi, lo = rivets(Z, Y, ys=[float(v + o) for v in rings for o in (-4.0, 4.0)], step=9.0, g=np.maximum(gY, gZ), along="x")
        return lay(lay(base, "#30343a", lo * 0.5 * on), "#eef0f0", hi * 0.8 * on)
    return f


def _crossbreak(X, Y, x0, x1, y0, y1, depth=0.07):
    """A cross-break: the panel creased corner to corner so it bows a little, as big duct panels are. -> normal tilt
    (dx, dy) for each ray: each of the four triangles of the X leans its own way."""
    u = (X - x0) / max(1e-3, x1 - x0) - 0.5
    v = (Y - y0) / max(1e-3, y1 - y0) - 0.5
    side = np.abs(u) > np.abs(v)
    dx = np.where(side, np.sign(u) * depth, 0.0)
    dy = np.where(side, 0.0, np.sign(v) * depth)
    return dx.astype(F32), dy.astype(F32)


def m_back(c):
    """The duct's back wall, inside (and the intake run's): galvanized panels between the flanged joints, each panel
    cross-broken; a row of rivets each side of every joint and along the seams at the floor and the top; the stencils
    over the grilles; a little dust settled on the lowest few centimetres; a rust run under the pipe's leak, long dry."""
    X, Y = c.X, c.Y
    gX, gY = gq(c, "X", "Y")
    g = np.maximum(gX, gY)
    s = spangle(X, Y, 7)
    grime = fbm(X / 60.0, Y / 50.0, 9, 3)
    base = col(GALV) * (0.93 + 0.10 * s[..., None]) * (0.90 + 0.14 * grime[..., None])
    duct = (Y <= M.DUCT_H)
    # the panels and their cross-breaks
    edges = [M.RUN_X[0]] + M.JOINTS + [M.SHAFT_X[0]]
    nx = np.zeros(X.shape, F32)
    ny = np.zeros(X.shape, F32)
    for a, b in zip(edges[:-1], edges[1:]):
        inp = (X >= a) & (X < b) & duct
        dx, dy = _crossbreak(X, Y, a, b, 0.0, M.DUCT_H, 0.11)
        nx = np.where(inp, dx, nx)
        ny = np.where(inp, dy, ny)
    # above the duct's top (the intake run's back wall): panels a metre and a half high
    run = Y > M.DUCT_H
    for k in range(4):
        y0, y1 = M.DUCT_H + k * 150.0, M.DUCT_H + (k + 1) * 150.0
        inp = run & (Y >= y0) & (Y < y1)
        dx, dy = _crossbreak(X, Y, M.RUN_X[0], M.RUN_X[1], y0, y1, 0.05)
        nx = np.where(inp, dx, nx)
        ny = np.where(inp, dy, ny)
    n = np.stack([nx, ny, np.ones(X.shape, F32)], axis=1)
    c.nrm = (n / np.linalg.norm(n, axis=1, keepdims=True)).astype(F32)
    # a crease is a line a shade lighter on one side
    for a, b in zip(edges[:-1], edges[1:]):
        inp = (X >= a) & (X < b) & duct
        u = (X - a) / (b - a)
        v = Y / M.DUCT_H
        d1 = np.abs(u - v) * (b - a)
        d2 = np.abs(u - (1 - v)) * (b - a)
        crease = (band(d1, 0, 0.7, g) + band(d2, 0, 0.7, g)) * inp
        base = base * (1 + 0.16 * crease[..., None])
    # up the intake run: a flanged joint every metre and a half, riveted
    jy = (Y - M.DUCT_H) / 150.0
    dj = np.abs(jy - np.round(jy)) * 150.0
    up_ = (Y > M.DUCT_H + 10).astype(F32)
    base = lay(base, GALV_D, band(dj, 0, 0.9, gY) * 0.8 * up_)
    base = lay(base, "#d6dadd", band(dj, 0.9, 2.0, gY) * 0.5 * up_)
    ry = [M.DUCT_H + 150.0 * k + o for k in range(1, 4) for o in (-3.4, 3.4)]
    hi, lo = rivets(X, Y, ys=ry, step=7.0, g=g, along="x")
    base = lay(lay(base, "#30343a", lo * 0.5 * up_), "#eef0f0", hi * 0.8 * up_)
    # the joints: a flange's dark gap with a lit bead each side, and a row of rivets each side of it
    for jx in M.JOINTS:
        d = np.abs(X - jx)
        base = lay(base, GALV_D, band(d, 0, 0.9, gX) * 0.85 * duct)
        base = lay(base, "#d6dadd", band(d, 0.9, 2.0, gX) * 0.55 * duct)
    hi, lo = rivets(X, Y, xs=[j + o for j in M.JOINTS for o in (-3.6, 3.6)], step=6.5, g=g, along="y")
    inside_ = duct & (Y > 2.0) & (Y < M.DUCT_H - 2.0)
    base = lay(lay(base, "#30343a", lo * 0.55 * inside_), "#f2f4f4", hi * 0.85 * inside_)
    # the seams where the wall meets the floor and the top: a folded lock, riveted every 8 cm
    for ys in (0.0, M.DUCT_H):
        d = np.abs(Y - ys)
        base = lay(base, GALV_D, band(d, 0.0, 1.2, gY) * 0.55)
        base = lay(base, "#cfd3d6", band(d, 1.2, 2.4, gY) * 0.35)
    hi, lo = rivets(X, Y, ys=[3.4, M.DUCT_H - 3.4], step=8.0, g=g, along="x")
    inx = (X > M.RUN_X[1] + 1.0) | (Y < 10.0)
    base = lay(lay(base, "#30343a", lo * 0.5 * inx), "#f2f4f4", hi * 0.85 * inx)
    # dust settled along the foot of the wall
    foot = np.clip(1 - Y / 7.0, 0, 1) ** 1.5 * duct
    base = lay(base, DUST, foot * 0.45)
    # a long-dry rust run from a seam, under where the pipe once dripped (left of BREAK)
    run_ = band(np.abs(X - 430.0 - 0.02 * Y), 0, 1.8, gX) * np.clip(1 - np.abs(Y - 80.0) / 50.0, 0, 1) * 0.25
    base = lay(base, "#8a5a3a", run_ * (0.6 + 0.4 * fbm(X / 3, Y / 9, 4, 2)))
    # the stencils
    cov = stencil_on(c, X, Y) * duct
    base = lay(base, STENCIL, cov * 0.92)
    return base


def m_floor(c):
    """The duct's floor, seen from above: galvanized, a film of dust that is thicker toward the back wall and in the
    corners, a few soft rolls of dust (no prints in it: nothing to hide), the joints across it, a flange round each
    grille with a screw at each corner."""
    X, Z = c.X, c.Z
    gX, gZ = gq(c, "X", "Z")
    g = np.maximum(gX, gZ)
    s = spangle(X, Z, 13)
    base = col(GALV) * (0.93 + 0.10 * s[..., None])
    dust = 0.26 + 0.32 * np.clip(1 - (Z - M.DUCT_Z[0]) / 40.0, 0, 1) + 0.12 * fbm(X / 30.0, Z / 18.0, 15, 3)
    base = lay(base, DUST, np.clip(dust, 0, 0.8))
    for (bx, bz, br) in ((58.0, 232.0, 3.4), (300.0, 212.0, 2.6), (418.0, 226.0, 3.0), (512.0, 218.0, 2.2), (570.0, 264.0, 2.8)):
        dd = np.hypot((X - bx) / br, (Z - bz) / (br * 1.3))
        base = lay(base, "#c8c2b6", np.clip(1.2 - dd, 0, 1) * 0.8)
        base = lay(base, "#8e8a84", np.clip(1.0 - np.hypot((X - bx - br * 0.3) / br, (Z - bz + br * 0.4) / br), 0, 1) * 0.25)
    for jx in M.JOINTS:
        d = np.abs(X - jx)
        base = lay(base, GALV_D, band(d, 0, 0.8, gX) * 0.7)
        base = lay(base, "#d8dcdf", band(d, 0.8, 1.8, gX) * 0.4)
    for _, _, gx in M.GRILLES:
        hx, z0, z1 = M.GRILLE_L / 2, M.GRILLE_Z[0], M.GRILLE_Z[1]
        dx = np.maximum(np.abs(X - gx) - hx, 0)
        dz = np.maximum(np.maximum(z0 - Z, Z - z1), 0)
        ring = band(np.maximum(dx, dz), 0.0, 3.2, g) * ((dx > 0) | (dz > 0))
        base = lay(base, "#babfc2", ring * 0.75)
        base = lay(base, "#3c4046", band(np.maximum(dx, dz), 3.2, 3.9, g) * 0.6)
        for sx in (gx - hx - 1.6, gx + hx + 1.6):
            for sz in (z0 - 1.6, z1 + 1.6):
                base = lay(base, "#30343a", np.clip((0.75 - np.hypot(X - sx, Z - sz)) / g + 0.5, 0, 1))
    return base


def m_runside(c):
    """The intake run's far side wall, inside: galvanized, a flanged joint every metre and a half up it, riveted."""
    Y, Z = c.Y, c.Z
    gY, gZ = gq(c, "Y", "Z")
    s = spangle(Z, Y, 37)
    base = col(GALV) * (0.93 + 0.09 * s[..., None]) * (0.9 + 0.14 * fbm(Z / 40, Y / 60, 39, 2)[..., None])
    jy = (Y - M.DUCT_H) / 150.0
    up_ = (Y > M.DUCT_H + 10)
    d = np.abs(jy - np.round(jy)) * 150.0
    base = lay(base, GALV_D, band(d, 0, 0.9, gY) * 0.8 * up_)
    base = lay(base, "#d6dadd", band(d, 0.9, 2.0, gY) * 0.5 * up_)
    return base


def m_slat(c):
    """A grille's slat: galvanized, its top in the duct's light, dusty."""
    if is_cut(c):
        return m_cut_skin(c)
    s = spangle(c.X, c.Z, 21)
    return col(mixc(GALV, DUST, 0.3)) * (0.9 + 0.12 * s[..., None])


def m_boot(c):
    """Inside a grille's boot: galvanized, alight from the room below: brightest down at the diffuser, dimming up toward
    the grille. Painted as it glows (the kit's flag 4: no lamp changes it)."""
    if is_cut(c):
        return m_cut_skin(c), None
    s = spangle(c.X + c.Z, c.Y, 23)
    up = np.clip((c.Y - M.TILE_Y) / (-M.SHELL - M.TILE_Y), 0, 1)
    glow = 0.20 + 0.62 * np.exp(-up * 3.0)
    if c.face == "front":                                              # the back of the boot faces us: a little less
        glow = glow * 0.85
    base = col(mixc(GALV, FLUO, 0.5)) * (glow * (0.94 + 0.08 * s))[..., None]
    return base, base * 0.0


def m_shaft(c):
    """The B-7 shaft's walls inside: clean galvanized, big panels, a flanged joint every metre and a half with a row of
    rivets each side of it; the stencil on its back wall beside the duct's mouth."""
    if is_cut(c):
        return m_cut_skin(c)
    X, Y, Z = c.X, c.Y, c.Z
    gX, gY = gq(c, "X", "Y")
    g = np.maximum(gX, gY)
    u = X + Z
    s = spangle(u, Y, 31)
    base = col(GALV) * (0.96 + 0.07 * s[..., None]) * (0.95 + 0.07 * fbm(u / 80, Y / 80, 33, 2)[..., None])
    jy = (Y + 40.0) / 150.0
    d = np.abs(jy - np.round(jy)) * 150.0
    base = lay(base, GALV_D, band(d, 0, 1.3, gY) * 0.85)
    base = lay(base, "#dfe3e6", band(d, 1.3, 2.8, gY) * 0.6)
    ry = [150.0 * k - 40.0 + o for k in range(-5, 6) for o in (-3.4, 3.4)]
    if c.face == "front":                                              # the back wall: rivets along X, and the stencil
        hi, lo = rivets(X, Y, ys=ry, step=8.0, g=g, along="x")
        base = lay(lay(base, "#30343a", lo * 0.45), "#f2f4f4", hi * 0.8)
        tex, texel, x0, y0 = STENCILS["b7"]
        cov = LT.sample_texture(tex, texel, X, y0 - Y, x0, 0.0)
        base = lay(base, STENCIL_RED, cov * 0.92)
    else:                                                              # a side wall: rivets along Z
        hi, lo = rivets(Z, Y, ys=ry, step=8.0, g=np.maximum(gq(c, "Z")[0], gY), along="x")
        base = lay(lay(base, "#30343a", lo * 0.4), "#f2f4f4", hi * 0.7)
    return base


def m_cheek(c):
    """The elbow's mitred corner at the foot of the intake run."""
    s = spangle(c.U, c.V, 41)
    base = col(GALV) * (0.92 + 0.1 * s[..., None])
    return lay(base, DUST, np.full(len(c.X), 0.25, F32))


# ---------------------------------------------------------------- the ceiling: tiles, grid, fittings, boots, the rooms below
def m_tile(c):
    """The ceiling's tiles from above: buff fibre board in a white-enamelled grid of two-foot squares (only the tees'
    bulbs show on this side), dust, a water stain; under each grille its diffuser, alight with the room's light. Cut,
    a tile is a pale band, the grid's tees under it."""
    X, Z = c.X, c.Z
    if is_cut(c):
        gX = gq(c, "X")[0]
        n = fbm(X / 3.0, c.Y * 2.0, 51, 2)
        base = col("#ddd5c4") * (0.92 + 0.1 * n[..., None])
        gx = (X - M.TILE_X0) / M.TILE
        tee = band(np.abs(gx - np.round(gx)) * M.TILE, 0, 1.4, gX)
        return lay(base, "#f4f2ea", tee), None
    gX, gZ = gq(c, "X", "Z")
    n = fbm(X / 9.0, Z / 9.0, 53, 3)
    base = col(TILE_BACK) * (0.86 + 0.24 * n[..., None])
    speck = sstep(0.72, 0.8, fbm(X / 1.4, Z / 1.4, 55, 2))
    base = lay(base, "#7c7468", speck * 0.4)
    gx = (X - M.TILE_X0) / M.TILE
    gz = (Z - M.TILE_Z0) / M.TILE
    dx = np.abs(gx - np.round(gx)) * M.TILE
    dz = np.abs(gz - np.round(gz)) * M.TILE
    base = lay(base, TBAR, np.maximum(band(dx, 0, 1.1, gX), band(dz, 0, 1.1, gZ)) * 0.9)
    base = lay(base, "#8c8a84", np.maximum(band(dx, 1.1, 1.8, gX), band(dz, 1.1, 1.8, gZ)) * 0.5)
    rr = np.hypot((X - 438.0) / 26.0, (Z - 150.0) / 20.0)
    base = lay(base, "#8a6e4e", band(np.abs(rr - 1.0), 0, 0.08, 0.04) * 0.5)
    base = base * (1 - 0.08 * np.clip(1 - rr, 0, 1))[..., None]
    emi = np.zeros(base.shape, F32)
    for _, _, gxx in M.GRILLES:
        inx = np.abs(X - gxx) < M.GRILLE_L / 2 - 1.0
        inz = (Z > M.BOOT_Z[0] + 1.0) & (Z < M.CUT)
        m = (inx & inz).astype(F32)
        slot = (np.abs(((Z - 2.0) / 6.0) - np.round((Z - 2.0) / 6.0)) * 6.0 > 1.4).astype(F32)
        base = lay(base, "#d8dad6", m)
        emi = emi + (m * slot)[..., None] * col(FLUO)[None, :] * 0.85
    lt = M.LIFTED
    crack = band(np.abs(Z - lt["Z"][1] - 0.6), 0, 1.0, gZ) * band(X, lt["X"][0] + 2.0, lt["X"][1] - 2.0, gX)
    near = band(X, lt["X"][0] + 2.0, lt["X"][1] - 2.0, gX) * np.exp(-np.maximum(Z - lt["Z"][1], 0) / 10.0) * (Z > lt["Z"][1])
    base = lay(base, "#f2f2de", crack)
    emi = emi + (crack * 1.2 + near * 0.08)[..., None] * col(FLUO)[None, :]
    for (x0, x1, z0, z1) in M.FITTINGS:
        ddx = np.maximum(np.maximum(x0 - X, X - x1), 0)
        ddz = np.maximum(np.maximum(z0 - Z, Z - min(z1, M.CUT)), 0)
        d = np.hypot(ddx, ddz)
        out_ = (ddx > 0) | (ddz > 0)
        emi = emi + (np.exp(-d / 3.0) * out_ * 0.55 + np.exp(-d / 16.0) * out_ * 0.12)[..., None] * col(FLUO)[None, :]
    return base, emi


def m_tile_lifted(c):
    """The lifted tile's back, a shade lighter at its raised edge."""
    n = fbm(c.X / 9.0, c.Z / 9.0, 57, 3)
    return col(TILE_BACK) * (0.9 + 0.22 * n[..., None])


def m_fixture(c):
    """A light fitting's housing, seen from above: white enamel, dusty; a ballast cover down its middle, knockouts, the
    seam round its lip; light leaking round its edge. Cut (OFFICE-17B2): its section, as drawn: the housing's sheet, its
    two tubes alight, the lens under them glowing."""
    X, Z = c.X, c.Z
    x0, x1, y0, y1, z0, z1 = c.box
    gX, gZ = gq(c, "X", "Z")
    g = np.maximum(gX, gZ)
    if is_cut(c):
        Y = c.Y
        gY = gq(c, "Y")[0]
        inner = band(X, x0 + 1.2, x1 - 1.2, gX) * band(Y, y0 + 1.6, y1 - 1.2, gY)
        base = lay(col(FIXTURE) * ones(c), "#3a3c48", inner)                      # the housing's sheet round its dark inside
        emi = np.zeros(base.shape, F32)
        cx = (x0 + x1) / 2
        for tx in (cx - 14.0, cx + 14.0):
            tube = np.clip((1.6 - np.hypot(X - tx, Y - (y0 + 5.0))) / gX + 0.5, 0, 1)
            halo = np.exp(-np.hypot(X - tx, Y - (y0 + 5.0)) / 4.0) * inner
            base = lay(base, "#fbfdf0", tube)
            base = lay(base, "#c8ccb8", halo * 0.55)
        lens = band(Y, y0, y0 + 1.6, gY) * band(X, x0 + 1.0, x1 - 1.0, gX)
        base = lay(base, "#f6f8e6", lens)
        return base, emi
    n = fbm(X / 12.0, Z / 12.0, 61, 2)
    base = col(FIXTURE) * (0.88 + 0.14 * n[..., None])
    base = lay(base, DUST, np.full(len(X), 0.3, F32))
    emi = np.zeros(base.shape, F32)
    if c.face == "top":
        cx = (x0 + x1) / 2
        base = lay(base, "#b6b4ae", band(np.abs(X - cx), 0, 6.0, gX) * band(Z, z0 + 10, z1 - 10, gZ) * 0.8)
        base = lay(base, "#6e6c68", band(np.abs(np.abs(X - cx) - 6.0), 0, 0.5, gX) * band(Z, z0 + 10, z1 - 10, gZ) * 0.6)
        for kz in (z0 + 22.0, z1 - 22.0):
            base = lay(base, "#7a7872", np.clip((1.6 - np.hypot(X - (x0 + 9.0), Z - kz)) / g + 0.5, 0, 1) * 0.7)
        edge = np.minimum(np.minimum(X - x0, x1 - X), np.minimum(Z - z0, z1 - Z))
        base = lay(base, "#ffffff", band(edge, 0.3, 1.4, g) * 0.35)
        for sx in (x0 + 12.0, x1 - 12.0):
            sl = band(np.abs(X - sx), 0, 2.2, gX) * band(Z, z0 + 8, z1 - 8, gZ)
            sl = sl * (np.abs(((Z - z0) / 7.0) - np.round((Z - z0) / 7.0)) * 7.0 > 1.6)
            base = lay(base, "#f4f4e0", sl)
            emi = emi + (sl * 0.95)[..., None] * col(FLUO)[None, :]
    else:
        lip = np.clip(1 - (c.Y - y0) / 3.0, 0, 1)
        emi = emi + (lip ** 2 * 0.55)[..., None] * col(FLUO)[None, :]
    return base, emi


def m_below(c):
    """Under the tiles' cut line: the rooms, not drawn (they are seen only through the grilles). A deep colour as a
    section leaves what it does not show, but not flat: the rooms' light falls into it from the line, softest far down,
    in a wide soft fan under each fitting the plane cuts, and a little all along under the tiles."""
    X, Y = c.X, c.Y
    n = fbm(X / 50.0, Y / 30.0, 71, 2)
    base = col(BELOW) * (0.94 + 0.12 * n[..., None])
    depth = np.clip(M.TILE_Y - M.TILE_T - Y, 0, None)                   # cm under the tiles' underside
    glow = 0.20 * np.exp(-depth / 26.0)                                  # the rooms' light just under the ceiling
    for (x0, x1, z0, z1) in M.CUT_FITTINGS:
        cx, hw = (x0 + x1) / 2, (x1 - x0) / 2
        w = hw + 0.85 * depth
        across = np.clip(1 - np.maximum(np.abs(X - cx) - (w - 26.0), 0) / 26.0, 0, 1)
        across = across * across * (3 - 2 * across)
        glow = glow + 0.62 * np.exp(-depth / 70.0) * across * (hw / np.maximum(w, 1e-3)) ** 0.35
    # the diffusers too let a little of their room's light be seen at the line
    for _, _, gx in M.GRILLES:
        glow = glow + 0.10 * np.exp(-depth / 18.0) * np.clip(1 - np.abs(X - gx) / 40.0, 0, 1)
    glow = glow * (0.9 + 0.2 * fbm(X / 20.0, Y / 40.0, 73, 2))
    out = base + col(mixc(FLUO, "#c8d0b8", 0.3))[None, :] * glow[..., None]
    return out, out * 0.0


# ---------------------------------------------------------------- the ceiling space: wall, joists, deck, insulation, services
def m_block(c):
    """The far wall: cinder block in running bond, its mortar joints, the blocks' open texture."""
    X, Y = c.X, c.Y
    gX, gY = gq(c, "X", "Y")
    course = np.floor(Y / M.WALL_COURSE)
    off = (course % 2) * (M.WALL_BLOCK / 2)
    bx = (X + off) / M.WALL_BLOCK
    bid = np.floor(bx).astype(np.int64) * 7919 + course.astype(np.int64) * 104729
    shade_ = (hashf(bid, 3) - 0.5) * 0.08
    tex = fbm(X / 2.2, Y / 2.2, 81, 2)
    base = col(BLOCK) * (0.9 + shade_[..., None] + 0.12 * (tex[..., None] - 0.5))
    dy = np.abs(Y / M.WALL_COURSE - np.round(Y / M.WALL_COURSE)) * M.WALL_COURSE
    dx = np.abs(bx - np.round(bx)) * M.WALL_BLOCK
    joint = np.maximum(band(dy, 0, 0.9, gY), band(dx, 0, 0.9, gX))
    return lay(base, MORTAR, joint * 0.55)                             # (OFFICE-17B2: quieter: it is far, and in the dark)


def m_wood(c):
    """Fir: the joists. Grain along the length; cut, a joist shows its end grain (rings) in a darker outline, as drawn."""
    X, Y, Z = c.X, c.Y, c.Z
    if is_cut(c):
        x0, x1, y0, y1, _, _ = c.box
        gX, gY = gq(c, "X", "Y")
        cx, cy = (x0 + x1) / 2 + 3.0, y0 - 8.0
        r = np.hypot(X - cx, Y - cy)
        rings = 0.5 + 0.5 * np.sin(r * 2.0 + fbm(X / 2, Y / 2, 91, 2) * 3.0)
        base = col(mixc(WOOD, "#c8a070", 0.25)) * (0.62 + 0.16 * rings[..., None])
        edge = np.minimum(np.minimum(X - x0, x1 - X), np.minimum(Y - y0, y1 - Y))
        return lay(base, "#3a2618", band(edge, 0.0, 0.9, np.maximum(gX, gY)))
    along = Z if c.face in ("bottom", "left", "right") else X
    across = X + Y if c.face == "bottom" else Y
    grain = fbm(along / 40.0, across / 0.9, 93, 3)
    base = col(WOOD) * (0.62 + 0.24 * grain[..., None])                # (up in the dark under the deck)
    return lay(base, WOOD_D, sstep(0.68, 0.8, fbm(along / 12.0, across / 0.5, 95, 2)) * 0.4)


def m_deck(c):
    """The roof deck's underside, planks across the joists; cut, the planks and the roofing over them, hatched."""
    if is_cut(c):
        gX, gY = gq(c, "X", "Y")
        u = (c.X - c.Y) / 3.0
        d = np.abs(u - np.round(u)) * 3.0
        base = col("#5e4636") * ones(c)
        base = lay(base, "#9a7656", np.clip((0.5 - d) / gX + 0.5, 0, 1) * 0.7)
        base = lay(base, "#3a2c26", band(np.abs(c.Y - (M.DECK_Y[0] + 6.0)), 0.0, 0.5, gY))           # the planks' faces
        return lay(base, "#2a2230", band(c.Y, M.DECK_Y[0] + 12.0, M.DECK_Y[1] + 10, gY))  # the roofing over the planks
    Z = c.Z
    gZ = gq(c, "Z")[0]
    plank = np.floor(Z / 14.0)
    k = hashf(plank.astype(np.int64), 7) * 0.18
    grain = fbm(c.X / 50.0, Z / 0.8, 97, 3)
    base = col(mixc(WOOD, WOOD_D, 0.35)) * (0.82 + k[..., None] + 0.16 * grain[..., None])
    d = np.abs(Z / 14.0 - np.round(Z / 14.0)) * 14.0
    return lay(base, "#2e2018", band(d, 0, 0.6, gZ) * 0.7)


def lumpy_top(X, y_top, thick, seed):
    """The top of a batt lying on something: soft, uneven, as insulation lies."""
    f = fbm(X / 11.0, np.full(X.shape, seed * 1.7, F32), seed, 3)
    puff = fbm(X / 3.5, np.full(X.shape, seed * 0.9, F32), seed + 5, 2)
    return y_top - thick * (0.30 * (1 - f) + 0.10 * (1 - puff))


def m_pink(seed=0):
    """Pink fibreglass insulation, lying: fluffy, its top uneven (its box is as high as its highest lump: the rays over
    its top are not there), its paper backing showing at the bottom edge here and there; cut, the same fluff seen in
    its thickness, a shade deeper, as drawn."""
    def f(c):
        X, Y, Z = c.X, c.Y, c.Z
        x0, x1, y0, y1, z0, z1 = c.box
        top = lumpy_top(X, y1, y1 - y0, seed)
        if c.face == "top":
            keep = (top >= y1 - 0.35 * (y1 - y0))
        else:
            keep = Y <= top
        u = X + Z * 0.5
        v = Y + Z * 0.3
        f1 = fbm(u / 3.0, v / 3.0, 101 + seed, 3)
        f2 = fbm(u / 0.9, v / 0.9, 103 + seed, 2)
        base = col(PINK) * (0.80 + 0.24 * f1[..., None] + 0.12 * f2[..., None])
        base = lay(base, PINK_D, sstep(0.6, 0.85, f1) * 0.45)
        backing = band(Y, y0, y0 + 0.9, 0.4) * sstep(0.45, 0.6, fbm(X / 14.0, Z / 14.0, 105 + seed, 2))
        base = lay(base, "#d8c8a0", backing * 0.7)
        if is_cut(c):
            under = np.clip((top - Y) / 2.5, 0, 1)                         # the fluff's edge lighter where it rounds over
            base = base * (0.86 + 0.1 * (1 - under))[..., None]
            base = lay(base, "#f2b8c4", np.clip(1 - (top - Y) / 1.2, 0, 1) * 0.6)
            return base, None, keep
        nrm = np.stack([(f1 - 0.5) * 0.6, np.ones(len(X), F32) * (1.0 if c.face == "top" else 0.0),
                        (f2 - 0.5) * 0.6], axis=1).astype(F32)
        nrm += np.asarray(c.n, F32)[None, :]
        c.nrm = (nrm / (np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-6)).astype(F32)
        return base, None, keep
    return f


def m_copper(c):
    """The water pipe: copper gone a little brown, a green bloom at a joint."""
    tarn = fbm(c.X / 25.0 + c.Z / 25.0, c.ang * 3.0 if hasattr(c, "ang") else c.Y, 111, 3)
    base = col(COPPER) * (0.82 + 0.28 * tarn[..., None])
    base = lay(base, COPPER_D, sstep(0.62, 0.8, tarn) * 0.5)
    joint = np.abs(((c.X + 40.0) / 300.0) - np.round((c.X + 40.0) / 300.0)) * 300.0
    base = lay(base, "#7aa08a", np.clip(1 - joint / 4.0, 0, 1) * sstep(0.4, 0.7, fbm(c.X / 2, c.Y / 2, 113, 2)) * 0.6)
    return base


def m_jacket(c):
    """A pipe's white canvas jacket, a little grey with dust, a band round it every metre."""
    n = fbm(c.X / 20.0, c.ang * 2.0, 115, 3)
    base = col("#d8d6ce") * (0.86 + 0.14 * n[..., None])
    d = np.abs(((c.X + 20.0) / 100.0) - np.round((c.X + 20.0) / 100.0)) * 100.0
    return lay(base, "#9a9890", np.clip(1 - d / 1.2, 0, 1) * 0.8)


def plain(color, amt=0.10, s=18.0, seed=0):
    """One paint, a little patchy as a brush leaves it."""
    k = col(color)

    def f(c):
        n = fbm((c.X + 0.37 * c.Y) / s, (c.Z + 0.61 * c.Y) / s, seed, 3)
        return k * (1 + amt * 2 * (n[..., None] - 0.5))
    return f


def cut_plain(color, cut_color, amt=0.10):
    """One paint; cut, another, as drawn."""
    p = plain(color, amt)
    q = col(cut_color)

    def f(c):
        if is_cut(c):
            return q * ones(c)
        return p(c)
    return f


# ---------------------------------------------------------------- the forgotten things
def m_cup(c):
    """A white enamel mug with a blue band, the dregs of coffee long dried in the bottom."""
    base = col(CUP) * ones(c)
    if c.face == "round":
        h = c.Y - M.TILE_Y
        base = lay(base, CUP_BAND, band(h, 7.0, 8.2, 0.25))
        inner = c.kind == 2
        dreg = inner & (h < 2.4)
        base = np.where(inner[..., None], base * 0.82, base)
        base = lay(base, COFFEE, dreg.astype(F32) * 0.95)
        ring = inner & (np.abs(h - 2.6) < 0.35)
        base = lay(base, "#5a3a22", ring.astype(F32) * 0.8)
        chip = (c.kind == 1) & (np.abs(h - 9.6) < 0.5) & (np.cos(c.ang - 0.6) > 0.96)
        base = lay(base, "#8a8478", chip.astype(F32))
    return base


def m_cup_handle(c):
    return col(CUP) * ones(c)


def m_pencil(c):
    """A yellow pencil, its paint rubbed at the middle, a pink eraser in its ferrule, its point sharpened."""
    t = c.along
    base = np.tile(col(PENCIL), (len(t), 1))
    base = lay(base, ERASER, (t < 0.07).astype(F32))
    base = lay(base, FERRULE, ((t >= 0.07) & (t < 0.12)).astype(F32))
    base = lay(base, PENCIL_WOOD, (t > 0.88).astype(F32))
    base = lay(base, "#3a3a40", (t > 0.97).astype(F32))
    facet = (np.abs(np.sin(c.side * 3.0)) > 0.8) & (t > 0.12) & (t < 0.88)
    return np.where(facet[..., None], base * 0.88, base)


def m_wrapper(c):
    """A sandwich wrapper from about 1983: waxed paper, a faded red-orange print of little diamonds and a band."""
    U, V = c.U, c.V
    base = col(WRAP) * (0.92 + 0.12 * fbm(U / 2.0, V / 2.0, 121, 2)[..., None])
    d = (np.abs(((U + V) / 3.2) - np.round((U + V) / 3.2)) < 0.12) | (np.abs(((U - V) / 3.2) - np.round((U - V) / 3.2)) < 0.12)
    base = lay(base, WRAP_PRINT, d.astype(F32) * 0.45)
    return lay(base, WRAP_PRINT, ((V > 4.0) & (V < 5.4)).astype(F32) * 0.6)


# ---------------------------------------------------------------- fans
def m_blade(c):
    """A fan blade: grey enamel on steel, a little worn."""
    s = fbm(c.U / 6.0, c.V / 6.0, 131, 2)
    return col(FAN) * (0.86 + 0.18 * s[..., None])


def m_hub(c):
    base = col(HUB) * ones(c)
    if hasattr(c, "kind"):
        top = c.kind >= 3
        base = np.where(top[..., None], base * 1.15, base)
    return base


def m_shroud(c):
    """The fan's ring: galvanized, a row of bolts round its lip."""
    s = spangle(c.X, c.Y * 3.0 + c.Z, 141)
    base = col(GALV) * (0.95 + 0.1 * s[..., None])
    if hasattr(c, "ang"):
        bolt = (np.abs((c.ang / (2 * math.pi) * 24) - np.round(c.ang / (2 * math.pi) * 24)) < 0.12) & (np.abs(c.Y - (M.SHROUD["h"][1] - 3.0)) < 0.9)
        base = lay(base, "#33373d", bolt.astype(F32) * 0.9)
    return base


def m_plate(c):
    """The plate across the shaft that holds the fan: galvanized, a ring of bolts round its hole, the hole cut out."""
    cx, cz = M.FAN["at"][0], M.FAN["at"][2]
    r = np.hypot(c.X - cx, c.Z - cz)
    ring = r < M.FAN["r"] + 9.0                                         # the ring round the hole
    lip = c.Z > M.CUT - 7.0                                             # the lip along the front
    keep = (r > M.FAN["r"] + 2.0) & (ring | lip)
    s = spangle(c.X, c.Z, 141)
    base = col(GALV) * (0.95 + 0.1 * s[..., None])
    ring = np.abs(r - (M.FAN["r"] + 6.0)) < 0.9
    ang = np.arctan2(c.Z - cz, c.X - cx)
    bolts = ring & (np.abs((ang / (2 * math.pi) * 16) - np.round(ang / (2 * math.pi) * 16)) < 0.18)
    base = lay(base, "#33373d", bolts.astype(F32))
    base = lay(base, "#c8ccd0", (np.abs(r - (M.FAN["r"] + 2.6)) < 0.6).astype(F32) * 0.6)
    return base, None, keep


# ---------------------------------------------------------------- building it
def blade_pts(cx, cy, cz, r0, r1, a, half0, half1, pitch, n=10):
    """A broad fan blade as a flat convex polygon, from the hub (r0) to its rounded tip (r1), its middle at angle `a`
    (radians) round a vertical axis; `half0`/`half1` its half-widths at the root and the tip; tilted by `pitch`."""
    pts = []
    ca, sa = math.cos(a), math.sin(a)
    rx, rz = ca, sa
    tx, tz = -sa, ca
    tip = []
    for k in range(n + 1):
        th = -math.pi / 2 + math.pi * k / n
        tip.append((r1 - half1 * 0.35 + math.cos(th) * half1 * 0.35, math.sin(th) * half1))
    outline = [(r0, -half0)] + tip + [(r0, half0)]
    for rr, w in outline:
        x = cx + rx * rr + tx * w
        z = cz + rz * rr + tz * w
        y = cy + w * math.tan(pitch)
        pts.append((x, y, z))
    return pts


def fan_blades(st, at, r, hub, angle_deg, blades, grp, pitch=0.30, name="fan", upward=True, broad=0.36):
    cx, cy, cz = at
    for k in range(blades):
        a = math.radians(angle_deg) + 2 * math.pi * k / blades
        pts = blade_pts(cx, cy, cz, hub * 0.9, r, a, hub * 0.75, r * broad, pitch)
        st.poly(pts, m_blade, name=name, grp=grp, shadow=False)
    if upward:
        st.cyl((cx, cz), hub, cy - 3.0, cy + 5.0, m_hub, axis="y", name=name + "-hub", grp=grp)
        st.ball((cx, cy + 5.0, cz), hub * 0.55, m_hub, name=name + "-hub", grp=grp)
    else:
        st.cyl((cx, cz), hub, cy - 4.0, cy + 2.5, m_hub, axis="y", name=name + "-hub", grp=grp)


def floor_layers(st, xa, xb, za, zb, name="floor", ends=(False, False), shadow=True):
    """A piece of the duct's floor, its three layers (the inner skin up, Y = 0)."""
    shell(st, xa, xb, -M.SHELL, 0.0, za, zb, "y", True, m_floor, m_sheet, name, shadow=shadow, ends=ends)


def duct(st):
    """The long run, the intake run at its left end, and the four grilles with their slats and boots; its walls cut
    as a section is (office_ducts_model: a double skin)."""
    S, K = M.SKIN, M.SHELL
    xL, xR = M.DUCT_X
    zb, zc = M.DUCT_Z
    rx0, rx1 = M.RUN_X
    sx0 = M.SHAFT_X[0]
    # the back wall (inside face at Z = 200; never cut), the intake run's back wall going on up, with the daylight's
    # opening in it at the rooftop unit
    io = M.INTAKE_OPEN
    st.box(xL - K, sx0, -K, M.DUCT_H + K, zb - K, zb, m_back, name="duct-back")
    box_without(st, rx0 - K, rx1 + K, M.DUCT_H + K, M.RUN_TOP, zb - K, zb, [(io["X"][0], io["X"][1], io["Y"][0], io["Y"][1])],
                m_back, name="run-back")
    # the floor, in pieces round the grilles' openings (its inner skin runs on through the shaft's wall to the mouth)
    hx = M.GRILLE_L / 2
    cuts = [xL - K] + [v for _, _, gx in M.GRILLES for v in (gx - hx, gx + hx)] + [sx0]
    for i, (a, b) in enumerate(zip(cuts[0::2], cuts[1::2])):
        floor_layers(st, a, b, zb - K, zc, ends=(False, i == len(M.GRILLES)))       # (its far left corner is out of the picture)
    for gid, _, gx in M.GRILLES:
        floor_layers(st, gx - hx, gx + hx, zb - K, M.GRILLE_Z[0])
        floor_layers(st, gx - hx, gx + hx, M.GRILLE_Z[1], zc)
        # its slats, along the run: 4.6 cm of louvre and 3.4 of gap
        z = M.GRILLE_Z[0] + 1.6
        while z + 4.6 <= M.GRILLE_Z[1] - 1.0:
            st.box(gx - hx, gx + hx, -1.3, -0.1, z, z + 4.6, m_slat, name="slats-" + gid, flag=CUT_FLAG)
            z += 8.0
        # its boot, from the floor's opening down to the diffuser in the tiles: back and sides (its front cut away)
        bz0 = M.BOOT_Z[0]
        st.box(gx - hx - S, gx + hx + S, M.TILE_Y, -S, bz0 - S, bz0, m_boot, name="boot-" + gid, flag=4)
        st.box(gx - hx - S, gx - hx, M.TILE_Y, -S, bz0, zc, m_boot, name="boot-" + gid, flag=4)
        st.box(gx + hx, gx + hx + S, M.TILE_Y, -S, bz0, zc, m_boot, name="boot-" + gid, flag=4)
    # the top, from the intake run's right wall to the shaft's wall (its inner skin on through the shaft's wall too)
    shell(st, rx1, sx0, M.DUCT_H, M.DUCT_H + K, zb - K, zc, "y", False, lambda c: m_sheet(c), m_sheet, "top", lit=True,
          ends=(True, True))
    # the intake run's walls: the far one (left, out of the picture at the cut, its inside seen going back), and the
    # one toward the middle of the picture, down to the duct's top: it is cut, and the cut turns into the top's
    shell(st, rx0 - K, rx0, 0.0, M.RUN_TOP, zb - K, zc, "x", True, m_runside, m_sheet, "run-left")
    shell(st, rx1, rx1 + K, M.DUCT_H, M.RUN_TOP, zb - K, zc, "x", False, m_sheet, tube_out("run"), "run-right", ends=(True, False))
    # the elbow's mitred corner at the run's foot, in the floor's far left corner
    k = M.CHEEK
    st.poly([P3(rx0, k, zb), P3(rx0 + k, 0.0, zb), P3(rx0 + k, 0.0, zc - 0.2), P3(rx0, k, zc - 0.2)], m_cheek, name="cheek", shadow=True)
    # the girth angles round the duct at each joint (outside it: seen over its top and under its floor)
    for jx in M.JOINTS:
        st.box(jx - 1.8, jx + 1.8, M.DUCT_H + K, M.DUCT_H + K + 3.6, zb - K - 3.6, zc, cut_plain(GALV, "#a4aab2"), name="girth", flag=CUT_FLAG)
        st.box(jx - 1.8, jx + 1.8, -K - 3.6, -K, zb - K - 3.6, zc, cut_plain(GALV, "#a4aab2"), name="girth", flag=CUT_FLAG)


def box_without(st, x0, x1, y0, y1, z0, z1, holes, mat, **kw):
    """A box with rectangular holes through it in X-Y (each (hx0, hx1, hy0, hy1)): the pieces round them."""
    xs = sorted({x0, x1} | {h[0] for h in holes} | {h[1] for h in holes})
    ys = sorted({y0, y1} | {h[2] for h in holes} | {h[3] for h in holes})
    for xa, xb in zip(xs[:-1], xs[1:]):
        for ya, yb in zip(ys[:-1], ys[1:]):
            if xa < x0 or xb > x1 or ya < y0 or yb > y1:
                continue
            mx, my = (xa + xb) / 2, (ya + yb) / 2
            if any(h[0] <= mx <= h[1] and h[2] <= my <= h[3] for h in holes):
                continue
            st.box(xa, xb, ya, yb, z0, z1, mat, **kw)


def shaft(st):
    """The B-7 shaft at the right end: a big clean vertical tube, cut as the duct is. Its back wall, its right wall
    (cut out of the picture), its left wall cut above and below the duct's mouth; the plate across it under the duct's
    floor, with the fan's hole; rungs down its back wall; a caged bulb over the mouth, the stencil beside it."""
    S, K = M.SKIN, M.SHELL
    sx0, sx1 = M.SHAFT_X
    sz0, sz1 = M.SHAFT_Z
    y0, y1 = M.SHAFT_Y
    st.box(sx0 - K, sx1 + K, y0, y1, sz0 - K, sz0, m_shaft, name="shaft-back")
    st.box(sx1, sx1 + K, y0, y1, sz0, sz1, m_shaft, name="shaft-right", flag=CUT_FLAG)
    zb = M.DUCT_Z[0]
    # the left wall: over the duct's top and under its floor, cut; behind the duct's back wall, whole
    shell(st, sx0 - K, sx0, M.DUCT_H, y1, sz0, sz1, "x", True, m_shaft, tube_out("shaft"), "shaft-left", ends=(True, False))
    shell(st, sx0 - K, sx0, y0, 0.0, sz0, sz1, "x", True, m_shaft, tube_out("shaft"), "shaft-left", ends=(False, True))
    st.box(sx0 - K, sx0, -K, M.DUCT_H + K, sz0, zb - K, m_shaft, name="shaft-left")
    # the fan's ring plate, on three struts to the walls, a lip along its front: round it the shaft is open, going on
    # down (the way down). (Its front lip hides the blades' front edges just where the old full plate did, so the fan's
    # frames keep their size.)
    fy = M.FAN["at"][1]
    fx, _, fz = M.FAN["at"]
    sh = M.SHROUD
    st.poly([P3(sx0, fy, sz0), P3(sx1, fy, sz0), P3(sx1, fy, sz1), P3(sx0, fy, sz1)], m_plate, name="plate", shadow=False)
    st.box(sx0, sx1, fy - M.FAN["plate"], fy, sz1 - 0.8, sz1, skin_mat(m_sheet), name="plate-edge", shadow=False, flag=CUT_FLAG)
    st.cyl((fx, fz), sh["r"], sh["h"][0], fy - 0.2, m_shroud, axis="y", name="plate", hollow=True, shadow=False)
    r_ = sh["r"] + 1.0
    strut = plain("#7e848c", 0.06)
    sy0, sy1 = sh["h"][0] + 2.0, sh["h"][0] + 8.0
    st.box(sx0, fx - r_, sy0, sy1, fz - 2.0, fz + 2.0, strut, name="plate", shadow=False)                  # to the left wall
    st.box(fx + r_, sx1, sy0, sy1, fz - 2.0, fz + 2.0, strut, name="plate", shadow=False)                  # to the right wall
    st.box(fx - 2.0, fx + 2.0, sy0, sy1, sz0, fz - r_, strut, name="plate", shadow=False)                  # to the back wall
    # the caged bulb on the back wall over the mouth: a porcelain socket, the bulb, a wire cage round it
    bx, by, bz = M.BULB["at"]
    st.box(bx - 3.5, bx + 3.5, by + 2.0, by + 9.0, sz0, sz0 + 5.0, plain("#e6e0d0", 0.05), name="bulb", shadow=False)
    st.ball((bx, by, bz + 2.0), M.BULB["r"], lambda c: (col("#fff6d8") * ones(c), col("#fff2c8") * ones(c) * 0.9),
            name="bulb", shadow=False, flag=4)
    for k in range(4):
        a = k * math.pi / 2 + math.pi / 4
        p0 = P3(bx + 6.0 * math.cos(a), by + 6.0, bz + 2.0 + 6.0 * math.sin(a))
        p1 = P3(bx + 6.0 * math.cos(a), by - 5.0, bz + 2.0 + 6.0 * math.sin(a))
        st.stick(p0, p1, 0.35, plain("#3a3e44", 0.05), name="bulb")
    st.stick(P3(bx - 6.0, by - 5.0, bz + 2.0), P3(bx + 6.0, by - 5.0, bz + 2.0), 0.35, plain("#3a3e44", 0.05), name="bulb")
    st.stick(P3(bx, by - 5.0, bz - 4.0), P3(bx, by - 5.0, bz + 8.0), 0.35, plain("#3a3e44", 0.05), name="bulb")
    # rungs: steel bars standing off the back wall every 30 cm, from just under the mouth down out of the picture
    ra, rb = M.RUNG_X
    rung = plain("#6e747c", 0.06)
    y = -18.0
    while y > y0 + 20:
        st.stick(P3(ra, y, sz0 + 10.0), P3(rb, y, sz0 + 10.0), 1.6, rung, name="rungs")
        st.stick(P3(ra, y, sz0), P3(ra, y, sz0 + 10.0), 1.3, rung, name="rungs")
        st.stick(P3(rb, y, sz0), P3(rb, y, sz0 + 10.0), 1.3, rung, name="rungs")
        y -= M.RUNG_STEP


def ceiling(st):
    """The tiles and their grid, cut at the front; the light fittings' housings (two cut); the rooms below (not drawn:
    their light falling from the line)."""
    sx0, sx1 = M.SHAFT_X
    K = M.SHELL
    ty = M.TILE_Y
    for xa, xb in ((-1200.0, sx0 - K), (sx1 + K, 1800.0)):
        st.box(xa, xb, ty - M.TILE_T, ty, -40.0, M.CUT, m_tile, name="tiles", shadow=False, flag=CUT_FLAG)
        st.box(xa, xb, ty - 900.0, ty - M.TILE_T - 0.01, -40.0, M.CUT, m_below, name="below", shadow=False, flag=4)
    for i, (x0, x1, z0, z1) in enumerate(M.FITTINGS):
        st.box(x0 + 1.0, x1 - 1.0, ty, ty + M.FITTING_H, z0 + 1.0, min(z1 - 1.0, M.CUT), m_fixture, name=f"fitting-{i}",
               shadow=False, flag=CUT_FLAG)
        cx = (x0 + x1) / 2
        zm = (z0 + min(z1, M.CUT)) / 2
        st.rope([P3(cx, ty + M.FITTING_H, zm), P3(cx + 6, ty + M.FITTING_H + 6, zm - 10),
                 P3(cx + 4, ty + M.FITTING_H + 14, zm - 28)], 0.9, plain("#8e9296", 0.08), name=f"whip-{i}")
    lt = M.LIFTED
    st.poly([P3(lt["X"][0], ty + 0.5, lt["Z"][0]), P3(lt["X"][1], ty + 0.5, lt["Z"][0]),
             P3(lt["X"][1], ty + lt["lift"] + 0.4, lt["Z"][1]), P3(lt["X"][0], ty + lt["lift"] + 0.4, lt["Z"][1])], m_tile_lifted, name="lifted", shadow=False)
    for i, (x0, x1, z0, z1, t) in enumerate(M.BATTS):
        st.box(x0, x1, ty, ty + t, z0, z1, m_pink(i), name="batts", flag=CUT_FLAG)


def things_on_tiles(st):
    ty = M.TILE_Y
    cx, cz = M.CUP["at"]
    r, h = M.CUP["r"], M.CUP["h"]
    st.cyl((cx, cz), r, ty, ty + h, m_cup, axis="y", name="cup", hollow=True)
    st.cyl((cx, cz), r - 0.5, ty, ty + 0.6, m_cup, axis="y", name="cup")
    hx = cx + r + 0.2
    st.rope([P3(hx - 0.4, ty + 8.0, cz), P3(hx + 2.0, ty + 7.6, cz + 0.6), P3(hx + 2.8, ty + 5.0, cz + 0.8),
             P3(hx + 2.0, ty + 2.6, cz + 0.6), P3(hx - 0.4, ty + 2.4, cz)], 0.55, m_cup_handle, name="cup")
    a, b = M.PENCIL["a"], M.PENCIL["b"]
    st.stick(P3(a[0], ty + 0.45, a[1]), P3(b[0], ty + 0.45, b[1]), M.PENCIL["r"], m_pencil, name="pencil", min_px=0.9)
    wx, wz = M.WRAPPER["at"]
    w, d = M.WRAPPER["w"], M.WRAPPER["d"]
    facets = [
        [P3(wx - w / 2, ty + 0.4, wz - d / 2), P3(wx, ty + 2.6, wz - d / 2 + 1), P3(wx, ty + 3.2, wz), P3(wx - w / 2 + 1, ty + 0.6, wz)],
        [P3(wx, ty + 2.6, wz - d / 2 + 1), P3(wx + w / 2, ty + 0.5, wz - d / 2 + 2), P3(wx + w / 2 - 1, ty + 1.4, wz + 1), P3(wx, ty + 3.2, wz)],
        [P3(wx - w / 2 + 1, ty + 0.6, wz), P3(wx, ty + 3.2, wz), P3(wx + 1, ty + 1.8, wz + d / 2), P3(wx - w / 2 + 2, ty + 0.4, wz + d / 2 - 1)],
        [P3(wx, ty + 3.2, wz), P3(wx + w / 2 - 1, ty + 1.4, wz + 1), P3(wx + w / 2 - 3, ty + 4.6, wz + d / 2), P3(wx + 1, ty + 1.8, wz + d / 2)],
    ]
    for f in facets:
        st.poly(f, m_wrapper, name="wrapper", shadow=True)


def above(st):
    """The ceiling space over the duct: the far wall, the joists and the deck (cut at the top of the picture), the
    insulation lying along the duct's top, the water pipe with its valve, the bundled wires on their hooks, a conduit
    and its box, the duct's hangers."""
    st.box(-1500.0, 2000.0, M.TILE_Y - 2.0, 900.0, M.FAR - 30.0, M.FAR, m_block, name="farwall", shadow=False)
    j0, j1 = M.JOIST_Y
    rx0, rx1 = M.RUN_X
    sx0, sx1 = M.SHAFT_X
    K = M.SHELL
    for jx in M.JOIST_X:
        a, b = jx - M.JOIST_W / 2, jx + M.JOIST_W / 2
        if b > rx0 - K - 14 and a < rx1 + K + 14:
            continue
        if b > sx0 - K - 14 and a < sx1 + K + 14:
            continue
        st.box(a, b, j0, j1, M.FAR, M.CUT, m_wood, name="joists", flag=CUT_FLAG)
    # the headers behind the run and the shaft (the joists cut short round them end on them)
    st.box(rx0 - K - 12.0, rx1 + K + 12.0, j0, j1, M.DUCT_Z[0] - K - 9.0, M.DUCT_Z[0] - K - 4.0, m_wood, name="joists")
    st.box(sx0 - K - 12.0, sx1 + K + 12.0, j0, j1, M.SHAFT_Z[0] - K - 9.0, M.SHAFT_Z[0] - K - 4.0, m_wood, name="joists")
    d0, d1 = M.DECK_Y
    for (xa, xb, za, zb) in ((-1500.0, rx0 - K - 12.0, M.FAR, M.CUT), (rx0 - K - 12.0, rx1 + K + 12.0, M.FAR, M.DUCT_Z[0] - K - 9.0),
                             (rx1 + K + 12.0, sx0 - K - 12.0, M.FAR, M.CUT), (sx0 - K - 12.0, sx1 + K + 12.0, M.FAR, M.SHAFT_Z[0] - K - 9.0),
                             (sx1 + K + 12.0, 2000.0, M.FAR, M.CUT)):
        st.box(xa, xb, d0, d1, za, zb, m_deck, name="deck", flag=CUT_FLAG)
    # pink insulation lying along the duct's top (cut with it), lumpy
    top = M.DUCT_H + K
    for i, (xa, xb, t) in enumerate(M.BLANKET):
        st.box(xa, xb, top, top + t, M.DUCT_Z[0] - K + 2.0, M.CUT, m_pink(11 + i), name="insulation", flag=CUT_FLAG)
    # the water pipe along the far wall on clamps, behind the run and the shaft; a gate valve, its red handwheel toward us
    p = M.PIPE
    xa, xb = p["X"]
    st.cyl((p["Y"], p["Z"]), p["r"], xa, xb, m_copper, axis="x", name="pipe")
    for k in range(-1, 5):
        x = 240.0 + 260.0 * k
        st.cyl((p["Y"], p["Z"]), p["r"] + 0.7, x - 2.0, x + 2.0, m_copper, axis="x", name="pipe")                  # couplings
    for bx_ in M.BRACKETS:
        st.box(bx_ - 1.2, bx_ + 1.2, p["Y"] - 1.0, p["Y"] + 1.0, M.FAR, p["Z"] - p["r"], plain(ROD, 0.05), name="pipe-clamps")
        st.cyl((p["Y"], p["Z"]), p["r"] + 1.1, bx_ - 1.1, bx_ + 1.1, plain("#5a5e64", 0.05), axis="x", name="pipe-clamps")
    vx = M.VALVE_X
    st.box(vx - 5.0, vx + 5.0, p["Y"] - 4.8, p["Y"] + 4.8, p["Z"] - 4.0, p["Z"] + 4.0, plain("#9a7a46", 0.1), name="valve")
    st.cyl((vx, p["Y"]), 1.4, p["Z"] + 4.0, p["Z"] + 12.0, plain("#8a7a5a", 0.1), axis="z", name="valve")
    st.cyl((vx, p["Y"]), 6.4, p["Z"] + 12.0, p["Z"] + 13.8, plain(RED, 0.1), axis="z", name="valve", hollow=True)
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        st.stick(P3(vx, p["Y"], p["Z"] + 12.9), P3(vx + 6.0 * math.cos(a), p["Y"] + 6.0 * math.sin(a), p["Z"] + 12.9), 0.7, plain(RED, 0.1), name="valve")
    st.ball((vx, p["Y"], p["Z"] + 13.6), 1.6, plain(RED, 0.1), name="valve", shadow=False)
    # a hot-water line in its white jacket, banded, on the same brackets; the sprinkler main under the joists, red
    hl = M.HOTLINE
    st.cyl((hl["Y"], hl["Z"]), hl["r"], p["X"][0], p["X"][1], m_jacket, axis="x", name="hotline")
    for bx_ in M.BRACKETS:
        st.box(bx_ - 1.2, bx_ + 1.2, hl["Y"] - 1.0, hl["Y"] + 1.0, M.FAR, hl["Z"] - hl["r"], plain(ROD, 0.05), name="hotline")
    sp = M.SPRINKLER
    st.cyl((sp["Y"], sp["Z"]), sp["r"], p["X"][0], p["X"][1], plain("#a8382c", 0.10), axis="x", name="sprinkler")
    for jx in M.JOIST_X:
        st.stick(P3(jx, sp["Y"] + sp["r"], sp["Z"]), P3(jx, M.JOIST_Y[0], sp["Z"]), 0.45, plain(ROD, 0.05), name="sprinkler")
    for hx_ in sp["heads"]:
        st.cyl((hx_, sp["Z"]), 1.2, sp["Y"] - 6.0, sp["Y"], plain("#b8a070", 0.08), axis="y", name="sprinkler")
        st.cyl((hx_, sp["Z"]), 2.6, sp["Y"] - 7.2, sp["Y"] - 6.0, plain("#c8b080", 0.08), axis="y", name="sprinkler")
    # a conduit coming down the wall from the joists to a junction box, and on from it along the wall to the left
    cdt = M.CONDUIT
    bx = cdt["box"]
    st.cyl((bx, cdt["Z"]), cdt["r"], cdt["Y"] + 6.0, M.JOIST_Y[0], plain(CONDUIT, 0.08), axis="y", name="conduit")
    st.cyl((cdt["Y"], cdt["Z"]), cdt["r"], cdt["X"][0], bx - 6.0, plain(CONDUIT, 0.08), axis="x", name="conduit")
    st.box(bx - 6.0, bx + 6.0, cdt["Y"] - 6.0, cdt["Y"] + 6.0, M.FAR, cdt["Z"] + 3.5, plain("#8e9296", 0.08), name="junction")
    for jx in M.BRACKETS[:3]:
        st.box(jx - 1.0, jx + 1.0, cdt["Y"] - 2.4, cdt["Y"] + 2.4, M.FAR, cdt["Z"] + 2.2, plain(ROD, 0.05), name="conduit")
    for yy in (cdt["Y"] + 40.0, cdt["Y"] + 85.0):
        st.box(bx - 2.4, bx + 2.4, yy - 1.0, yy + 1.0, M.FAR, cdt["Z"] + 2.2, plain(ROD, 0.05), name="conduit")
    # the duct's trapeze hangers: a strut under the floor (cut at the front), a rod up behind the duct to the joists
    for x in M.HANGERS:
        st.box(x - 2.4, x + 2.4, -K - 4.2, -K, M.DUCT_Z[0] - K - 6.0, M.CUT, cut_plain("#7a7e84", "#9aa0a8", 0.05), name="rods", flag=CUT_FLAG)
        st.stick(P3(x, -K - 4.2, M.DUCT_Z[0] - K - 3.0), P3(x, j0, M.DUCT_Z[0] - K - 3.0), 0.6, plain(ROD, 0.05), name="rods")
        for yy in (-K + 0.5, M.DUCT_H + K + 1.5):
            st.box(x - 1.8, x + 1.8, yy - 1.2, yy + 1.2, M.DUCT_Z[0] - K - 4.8, M.DUCT_Z[0] - K - 1.2, plain("#4a4e54", 0.05), name="rods")
    wires(st)


def wires(st):
    """The bundled wires: five cables tied together, along the far wall in shallow curves between J-hooks screwed to
    it, passing behind the run and the shaft."""
    w = M.WIRES
    cols = ["#5c5e64", "#2a2a30", "#d6d2c8", "#a8382c", "#2f4f8a"]
    offs = [(0.0, 0.0), (2.4, 0.7), (-2.2, 1.1), (0.7, -2.3), (-0.6, 2.4)]
    step = M.BRACKETS[1] - M.BRACKETS[0]
    hooks = [M.BRACKETS[0] - step * k for k in range(4, 0, -1)] + list(M.BRACKETS) + [M.BRACKETS[-1] + step * k for k in range(1, 5)]
    for a, b in zip(hooks[:-1], hooks[1:]):
        n = 12
        for ci, (dy, dz) in enumerate(offs):
            pts = []
            for k in range(n + 1):
                t = k / n
                x = a + (b - a) * t
                sag = w["sag"] * 4 * t * (1 - t)
                tw = math.sin(t * math.pi * 6 + ci * 1.3) * 0.5
                pts.append(P3(x, w["Y"] - sag + dy + tw, w["Z"] + dz - tw))
            st.rope(pts, 1.3, plain(cols[ci], 0.08, seed=ci), name="wires")
        for t in (0.25, 0.5, 0.75):
            x = a + (b - a) * t
            sag = w["sag"] * 4 * t * (1 - t)
            st.cyl((w["Y"] - sag + 0.2, w["Z"] + 0.2), 3.1, x - 0.5, x + 0.5, plain("#1e1e22", 0.05), axis="x", name="wires")
    for hx_ in hooks:                                                    # the J-hooks, screwed to the wall
        st.stick(P3(hx_, w["Y"] + 3.6, M.FAR), P3(hx_, w["Y"] + 3.6, w["Z"] - 3.8), 0.55, plain(ROD, 0.05), name="wires")
        st.stick(P3(hx_, w["Y"] - 3.8, w["Z"] - 3.8), P3(hx_, w["Y"] - 3.8, w["Z"] + 3.8), 0.55, plain("#3e4248", 0.05), name="wires")
        st.stick(P3(hx_, w["Y"] - 3.8, w["Z"] + 3.8), P3(hx_, w["Y"] + 1.0, w["Z"] + 4.4), 0.55, plain("#3e4248", 0.05), name="wires")


def intake(st):
    """The intake: the daylight's opening at the top of the run, at the rooftop unit, and the intake fan in the run,
    still, seen from below (its back: the motor's can under the hub, the struts that hold it)."""
    io = M.INTAKE_OPEN
    st.box(io["X"][0] - 0.5, io["X"][1] + 0.5, io["Y"][0] - 0.5, io["Y"][1] + 0.5, M.DUCT_Z[0] - M.SHELL - 6.0, M.DUCT_Z[0] - M.SHELL - 2.0,
           lambda c: (col(DAYLIGHT) * ones(c), col(DAYLIGHT) * 0.0), name="daylight", shadow=False, flag=4)
    cx, cy, cz = M.INTAKE_FAN["at"]
    r = M.INTAKE_FAN["r"]
    fan_blades(st, (cx, cy, cz), r, M.INTAKE_FAN["hub"], 17.0, 4, "back", pitch=0.22, name="intakefan", upward=False, broad=0.42)
    st.cyl((cx, cz), 9.0, cy - 22.0, cy - 4.0, m_hub, axis="y", name="intakefan-motor")
    for k in range(3):
        a = math.radians(30 + 120 * k)
        ex = cx + math.cos(a) * 60.0
        ez = cz + math.sin(a) * 60.0
        ex = min(max(ex, M.RUN_X[0] + 0.5), M.RUN_X[1] - 0.5)
        ez = min(max(ez, M.DUCT_Z[0] + 0.5), M.CUT - 0.5)
        st.stick(P3(cx + math.cos(a) * 8.0, cy - 14.0, cz + math.sin(a) * 8.0), P3(ex, cy - 8.0, ez), 0.8, plain("#5e646a", 0.05), name="intakefan-struts")
    st.cyl((cx, cz), r + 2.0, cy - 1.5, cy + 2.5, plain("#7e848a", 0.06), axis="y", name="intakefan-shroud", hollow=True)


def ghosts(st):
    """The walls the cut takes away, kept as shadows only (group "ghost", never drawn): a cut-away is lit as if they were
    still there, so the daylight stays in the intake run, the grilles' light in the duct, the shaft's in the shaft."""
    S, C, K = M.SKIN, M.CUT, M.SHELL
    rx0, rx1 = M.RUN_X
    sx0, sx1 = M.SHAFT_X
    gm = lambda c: col("#808080") * ones(c)
    st.box(M.DUCT_X[0] - K, M.SHAFT_X[0], -K - 3.0, M.DUCT_H + K + 3.0, C + 0.5, C + K, gm, grp="ghost")       # the duct's near wall
    st.box(rx0 - K, rx1 + K, M.DUCT_H, M.RUN_TOP, C + 0.5, C + K, gm, grp="ghost")                             # the run's front
    st.box(sx0 - K, sx1 + K, M.SHAFT_Y[0], M.SHAFT_Y[1], C + 0.5, C + K, gm, grp="ghost")                      # the shaft's front
    hx = M.GRILLE_L / 2
    for _, _, gx in M.GRILLES:
        st.box(gx - hx - S, gx + hx + S, M.TILE_Y, -K, C + 0.5, C + S + 0.5, gm, grp="ghost")                   # each boot's front


def build(st, fan_angle=None, fan_only=False):
    """Everything. `fan_angle`: the B-7 fan's blades at that angle (degrees), in the group "fan"; None: no blades (the
    backdrop shows the plate's empty hole and the shaft going down through it)."""
    if not fan_only:
        ghosts(st)
        duct(st)
        shaft(st)
        ceiling(st)
        things_on_tiles(st)
        above(st)
        intake(st)
    if fan_angle is not None:
        fan_blades(st, M.FAN["at"], M.FAN["r"], M.FAN["hub"], fan_angle, M.FAN["blades"], "fan", pitch=0.32, name="fan", upward=True, broad=0.31)

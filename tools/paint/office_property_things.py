"""Everything in Property & Effects (office_property.py), built in the room's own centimetres: the shell, the hall seen
through Opal's window and her door, the window, her counter and what is on it, her stool and her knitting, the door,
the shelving and every tagged thing on it, the banjo, the ceiling's fittings, and the cart and boxes near us.
OFFICE-17C.

Groups (`grp`) are the cut-outs: "banjo", "receipt", "vent", "door", "wall" (the counter, the window's frame, the
door's casing, the sign: with the far wall round them it is the cut-out `wall`), "front"; everything else is the
backdrop ("back"). All measurements come from office_property_model.py. Every word is the Office's own; no brand, no
logo, nobody's typeface; every thing drawn for this picture."""

import math
import zlib

import numpy as np

from brush import F32, lerp
import office_property_model as M
from office_room_kit import (col, fbm, hashf, grad_of, px_of, lines_aa, band, lay, normals, rm, rect_uv, disc_uv, plain, painted_steel,
                             chrome, molded, laminate, obox, m_carpet, block_wall, ceiling_paint, m_troffer, vent, sprinkler,
                             smoke_detector, ceiling_speaker, curve3, OUTSIDE, PAPER, STEEL, STEEL_D)

H = M.H
SHELF_STEEL = "#8d978f"          # the shelving: regulation gray with a little green in it
CARD = "#b8935f"                 # archive boxes: brown card
TAG = "#a8794a"                  # a property tag: brown card on a string


# ---------------------------------------------------------------- small geometry
def nrm(v):
    v = np.asarray(v, dtype=np.float64)
    return v / (np.linalg.norm(v) + 1e-12)


def frame_box(st, o, ax, ay, az, sx, sy, sz, mat, name, grp="back", shadow=False, flag=0):
    """A box in any attitude: `o` the middle of its bottom face, ax/ay/az its own axes (unit vectors), sx/sy/sz its
    sizes along them (sy is its height, from o up along ay)."""
    o, ax, ay, az = (np.asarray(v, dtype=np.float64) for v in (o, ax, ay, az))

    def P(a, b, c):
        return tuple(o + ax * a + ay * b + az * c)
    hx, hz = sx / 2, sz / 2
    faces = [
        [P(-hx, 0, hz), P(hx, 0, hz), P(hx, sy, hz), P(-hx, sy, hz)], [P(hx, 0, -hz), P(-hx, 0, -hz), P(-hx, sy, -hz), P(hx, sy, -hz)],
        [P(-hx, 0, -hz), P(-hx, 0, hz), P(-hx, sy, hz), P(-hx, sy, -hz)], [P(hx, 0, hz), P(hx, 0, -hz), P(hx, sy, -hz), P(hx, sy, hz)],
        [P(-hx, sy, hz), P(hx, sy, hz), P(hx, sy, -hz), P(-hx, sy, -hz)], [P(-hx, 0, -hz), P(hx, 0, -hz), P(hx, 0, hz), P(-hx, 0, hz)],
    ]
    if shadow:
        pts = [p for f in faces for p in f]
        xs, ys, zs = zip(*pts)
        st.occ.append((min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))
    for f in faces:
        st.poly(f, mat, name, grp=grp, flag=flag)


def ring(st, c, n, r, depth, mat, name, grp="back", sides=28, r_in=None):
    """A short round band (a banjo's rim, a lid's edge) about the axis `n` through `c`: its outside, `depth` deep."""
    c, n = np.asarray(c, dtype=np.float64), nrm(n)
    up = np.array([0.0, 1.0, 0.0]) if abs(n[1]) < 0.9 else np.array([1.0, 0.0, 0.0])
    u = nrm(np.cross(up, n))
    v = np.cross(n, u)
    for i in range(sides):
        a0, a1 = 2 * math.pi * i / sides, 2 * math.pi * (i + 1) / sides
        p0 = c + r * (u * math.cos(a0) + v * math.sin(a0))
        p1 = c + r * (u * math.cos(a1) + v * math.sin(a1))
        q = n * depth / 2
        st.poly([tuple(p0 - q), tuple(p1 - q), tuple(p1 + q), tuple(p0 + q)], mat, name, grp=grp)


# ---------------------------------------------------------------- the shell
CARPET = m_carpet(seed=15, stains=((150.0, 160.0, 11.0),), paths=(((200.0, 300.0), (190.0, 90.0), 40.0), ((190.0, 90.0), (340.0, 50.0), 30.0)))


def m_back(c):
    return block_wall(c, c.X, c.Y, grad_of(c.X) * c.ss, grad_of(c.Y) * c.ss, seed=11)


def m_left(c):
    return block_wall(c, c.Z, c.Y, grad_of(c.Z) * c.ss, grad_of(c.Y) * c.ss, seed=12)


def m_right(c):
    return block_wall(c, c.Z, c.Y, grad_of(c.Z) * c.ss, grad_of(c.Y) * c.ss, seed=13)


CEILING = ceiling_paint(grid=M.GRID, origin=(M.GRID_X0, M.GRID_Z0), seed=14, stains=((300.0, 430.0, 22.0),))


def holes():
    wx0, wx1, wy0, wy1 = M.WINDOW
    dx0, dx1, dy0, dy1 = M.DOOR
    vx0, vx1, vz0, vz1 = M.VENT
    return {
        "back": lambda X, Y, Z: ((X > wx0) & (X < wx1) & (Y > wy0) & (Y < wy1)) | ((X > dx0) & (X < dx1) & (Y < dy1)),
        "ceiling": lambda X, Y, Z: (X > vx0 + 3.5) & (X < vx1 - 3.5) & (Z > vz0 + 3.5) & (Z < vz1 - 3.5),
    }


def shell(st):
    st.shell(M.W, H, dict(floor=CARPET, back=m_back, left=m_left, right=m_right, ceiling=CEILING), holes=holes())


# ---------------------------------------------------------------- the hall (self-lit: brighter than the room)
HALL_GLOW = 1.14


def hall(st, G="back"):
    """What the window and the door show: the hall's vinyl floor, its far wall (a corkboard, a drinking fountain, a sign
    pointing the way to the interview rooms), its ceiling with a tube; the reveals of both openings; the hall's ledge
    under the glass with the bell on it (RING FOR SERVICE)."""
    zf = -M.HALL_D
    x0, x1 = -120.0, M.W + 160.0

    def lit(base, k=1.0):
        def f(c):
            out = base(c)
            g = HALL_GLOW * k * (0.86 + 0.14 * np.clip(1 - np.abs(c.Z + M.HALL_D * 0.5) / M.HALL_D, 0, 1))
            return out * 0.10, out * np.asarray(g)[..., None]
        return f

    def m_vinyl(c):
        T = 30.0
        ix, iz = np.floor(c.X / T), np.floor(c.Z / T)
        chk = ((ix + iz) % 2) == 0
        base = np.where(chk[..., None], col("#d6d0bc"), col("#c4bea8"))
        base = base * (0.95 + 0.08 * fbm(c.X / 9, c.Z / 9, 161, 2))[..., None]
        g = px_of(c, 3.0)
        seam = np.maximum(lines_aa(c.X, T, 0.6, g), lines_aa(c.Z, T, 0.6, g))
        return base * (1 - 0.12 * seam[..., None])

    def m_far(c):
        X, Y = c.X, c.Y
        g = px_of(c, 1.2)
        out = block_wall(c, X, Y, g, g, seed=17)
        # a corkboard behind the window, a few notices pinned on it
        cork = rect_uv(X, Y, 120.0, 230.0, 100.0, 170.0, g)
        out = lay(out, "#a87a4a", cork)
        out = lay(out, "#6a5a48", (rect_uv(X, Y, 118.0, 232.0, 98.0, 172.0, g) - cork).clip(0, 1))
        for i, (px, py, w, h, cc) in enumerate(((128, 132, 22, 30, "#ece6d4"), (156, 122, 20, 26, "#e8e0a0"), (184, 136, 24, 22, "#ece6d4"),
                                                 (212, 118, 14, 40, "#d8e0e8"))):
            out = lay(out, cc, rect_uv(X, Y, px, px + w, py, py + h, g))
        # a sign beyond the door: INTERVIEW ROOMS (its words are laid later), and a red fire extinguisher
        out = lay(out, "#3c4a5e", rect_uv(X, Y, 296.0, 396.0, 150.0, 172.0, g) * 0.95)
        out = lay(out, "#b8382c", rect_uv(X, Y, 404.0, 418.0, 40.0, 92.0, g))
        # a drinking fountain's back plate, left of the corkboard
        out = lay(out, "#c8ccd0", rect_uv(X, Y, 40.0, 84.0, 70.0, 110.0, g))
        return out

    def m_hceil(c):
        out = col("#d8d4c4") * (0.95 + 0.06 * fbm(c.X / 30, c.Z / 30, 163, 2))[..., None]
        tube = np.exp(-((c.Z + M.HALL_D * 0.5) / 9.0) ** 2)
        return out * (1 + 1.4 * tube[..., None])

    st.poly([(x0, 0, zf), (x1, 0, zf), (x1, 0, -M.WALL_T), (x0, 0, -M.WALL_T)], lit(m_vinyl), "hall", grp=G, flag=OUTSIDE)
    st.poly([(x0, 0, zf), (x1, 0, zf), (x1, H, zf), (x0, H, zf)], lit(m_far), "hall", grp=G, flag=OUTSIDE)
    st.poly([(x0, H, zf), (x1, H, zf), (x1, H, -M.WALL_T), (x0, H, -M.WALL_T)], lit(m_hceil, 0.9), "hall", grp=G, flag=OUTSIDE)
    # the fountain's basin
    st.box(46.0, 78.0, 76.0, 82.0, zf, zf + 30.0, lit(plain("#d0d4d8", 0.05, seed=164), 0.9), "hall", grp=G, flag=OUTSIDE)
    # the reveals: the wall's thickness round both openings
    rev = lit(plain("#c8b994", 0.06, seed=165), 0.62)
    wx0, wx1, wy0, wy1 = M.WINDOW
    for a0 in (wx0, wx1):
        st.poly([(a0, wy0, 0), (a0, wy0, -M.WALL_T), (a0, wy1, -M.WALL_T), (a0, wy1, 0)], rev, "reveal", grp=G, flag=OUTSIDE)
    st.poly([(wx0, wy1, 0), (wx1, wy1, 0), (wx1, wy1, -M.WALL_T), (wx0, wy1, -M.WALL_T)], rev, "reveal", grp=G, flag=OUTSIDE)
    dx0, dx1, dy0, dy1 = M.DOOR
    for X in (dx0, dx1):
        st.poly([(X, 0, 0), (X, 0, -M.WALL_T), (X, dy1, -M.WALL_T), (X, dy1, 0)], rev, "reveal", grp=G, flag=OUTSIDE)
    st.poly([(dx0, dy1, 0), (dx1, dy1, 0), (dx1, dy1, -M.WALL_T), (dx0, dy1, -M.WALL_T)], rev, "reveal", grp=G, flag=OUTSIDE)
    # the hall's ledge under the glass (laminate on the hall's side), and the bell on it
    lx0, lx1, ly0, ly1, lz0, lz1 = M.LEDGE
    st.box(lx0, lx1, ly0, ly1, lz0, lz1 + 0.5, lit(laminate("#bca27a", seed=166, grain_dir="x"), 0.85), "ledge", grp=G, shadow=False, flag=OUTSIDE)
    st.box(lx0, lx1, 0.0, ly0, lz0 + 3.0, lz1, lit(plain("#a8a090", 0.05, seed=167), 0.7), "ledge", grp=G, shadow=False, flag=OUTSIDE)
    bx, bz, br = M.BELL

    def m_bell(c):
        n = normals(c)
        k = col("#d8dade") * (0.55 + 0.55 * np.clip(n[..., 1], 0, 1) + 0.25 * np.clip(n[..., 2], 0, 1))[..., None]
        return k * 0.10, k * HALL_GLOW
    st.cyl((bx, bz), br * 1.25, ly1, ly1 + 1.4, lit(plain("#202024", 0.04, seed=168), 0.8), name="bell", grp=G, flag=OUTSIDE, shadow=False)
    st.ball((bx, ly1 + 1.4, bz), br, m_bell, name="bell", grp=G, squash=(1.0, 0.72, 1.0), flag=OUTSIDE, shadow=False)
    st.cyl((bx, bz), 0.6, ly1 + 1.4 + br * 0.72 - 0.3, ly1 + 1.4 + br * 0.72 + 1.0, lit(plain("#c8cacc", 0.03, seed=169)), name="bell", grp=G, flag=OUTSIDE, shadow=False)
    # its little card, standing beside it: RING FOR SERVICE faces the hall (we see the back of it, through the glass)
    st.poly([(bx - 16, ly1, bz + 1), (bx - 8, ly1, bz - 3), (bx - 8, ly1 + 6, bz - 3), (bx - 16, ly1 + 6, bz + 1)],
            lit(plain("#e8e2d0", 0.04, seed=170), 0.8), "bell", grp=G, flag=OUTSIDE)


# ---------------------------------------------------------------- Opal's window
ALU = "#b4b8b8"


def window(st, G="wall"):
    """A sliding glass window in an aluminium frame: two panes, the left sliding behind the right, a latch where they meet,
    a slot under the glass for passing papers. The glass itself is not a surface here (the hall is seen through it): its
    sheen is laid over it afterwards (office_property.glass_sheen)."""
    wx0, wx1, wy0, wy1 = M.WINDOW
    m = painted_steel(ALU, seed=171, amt=0.04)
    fw = 3.0
    st.box(wx0, wx1, wy0 - 1.0, wy0 + fw - 1.0, -4.0, 1.2, m, "window", grp=G, shadow=False)          # the sill's frame
    st.box(wx0, wx1, wy1 - fw, wy1, -4.0, 1.2, m, "window", grp=G, shadow=False)
    st.box(wx0, wx0 + fw, wy0, wy1, -4.0, 1.2, m, "window", grp=G, shadow=False)
    st.box(wx1 - fw, wx1, wy0, wy1, -4.0, 1.2, m, "window", grp=G, shadow=False)
    mid = (wx0 + wx1) / 2
    # the two sashes' frames: the right pane on the near track, the left on the far one, meeting a little overlapped
    for (a0, a1, z0, z1) in ((wx0 + fw, mid + 2.0, -3.2, -2.0), (mid - 2.0, wx1 - fw, -1.4, -0.2)):
        st.box(a0, a1, wy0 + fw - 1.0, wy0 + fw + 0.6, z0, z1, m, "window", grp=G, shadow=False)
        st.box(a0, a1, wy1 - fw - 1.6, wy1 - fw, z0, z1, m, "window", grp=G, shadow=False)
        st.box(a0, a0 + 1.8, wy0 + fw - 1.0, wy1 - fw, z0, z1, m, "window", grp=G, shadow=False)
        st.box(a1 - 1.8, a1, wy0 + fw - 1.0, wy1 - fw, z0, z1, m, "window", grp=G, shadow=False)
    st.box(mid - 1.2, mid + 1.6, wy0 + 40.0, wy0 + 44.0, -0.2, 1.4, col("#5a5e62"), "window", grp=G, shadow=False)    # the latch
    # the sign hung over it: THIS WINDOW CLOSES AT 1700 (its words laid later)
    sx0, sx1, sy0, sy1 = M.SIGN

    def m_sign(c):
        g = px_of(c, 1.2)
        out = col("#ece4cc") * (0.97 + 0.04 * fbm(c.X / 6, c.Y / 6, 172, 2))[..., None]
        edge = 1 - rect_uv(c.X, c.Y, sx0 + 0.8, sx1 - 0.8, sy0 + 0.8, sy1 - 0.8, g)
        return lay(out, "#4a5a6e", edge * 0.9)
    st.box(sx0, sx1, sy0, sy1, 0.0, 0.6, m_sign, "sign", grp=G, shadow=False)


# ---------------------------------------------------------------- Opal's counter, and what is on it
def counter(st, G="wall"):
    """Opal's counter along the window: a wood-grain top with a rounded front edge, a steel cabinet under it (two drawers
    and a cupboard), a black rubber kick at its foot. On it: her date stamp on its ink pad, a stack of claim forms, a
    pencil cup, a wire tray; and a slot under the glass."""
    x0, x1, y0, y1, z0, z1 = M.COUNTER
    top = laminate("#b8955e", seed=181, grain_dir="x")
    st.box(x0, x1, y0, y1, z0, z1, top, "counter", grp=G)
    st.box(x0 - 0.4, x1 + 0.4, y0 - 0.2, y0 + 1.6, z1 - 0.2, z1 + 0.8, col("#3a3028"), "counter", grp=G, shadow=False)     # its edge band
    m_cab = painted_steel("#8c938e", seed=182, amt=0.05)
    st.box(x0 + 2.0, x1 - 2.0, 8.0, y0, z0, z1 - 4.0, m_cab, "counter", grp=G)
    st.box(x0 + 3.0, x1 - 3.0, 0.0, 8.0, z0, z1 - 7.0, col("#2c2a2a"), "counter", grp=G, shadow=False)                    # the kick
    # the cabinet's doors and drawers: lines and handles on its front (facing us)
    zf = z1 - 4.0
    for k, (a0, a1) in enumerate(((x0 + 4, x0 + 72), (x0 + 74, x0 + 148), (x0 + 150, x1 - 4))):
        st.box(a0, a1, 12.0, y0 - 3.0, zf, zf + 0.6, painted_steel("#959c97", seed=183 + k, amt=0.05), "counter", grp=G, shadow=False)
        st.box((a0 + a1) / 2 - 5.0, (a0 + a1) / 2 + 5.0, y0 - 14.0, y0 - 12.0, zf + 0.6, zf + 2.2, chrome(), "counter", grp=G, shadow=False)
    # the date stamp on its ink pad (a black handle, a band of dates, a base), at her right hand
    sx, sz = M.STAMP
    st.box(sx - 6.0, sx + 6.0, y1, y1 + 1.6, sz - 4.0, sz + 4.0, col("#2a2c34"), "stamp", grp=G, shadow=False)            # the pad's tin
    st.box(sx - 5.0, sx + 5.0, y1 + 1.6, y1 + 1.8, sz - 3.0, sz + 3.0, col("#3a3070"), "stamp", grp=G, shadow=False)       # the ink
    st.box(sx + 9.0, sx + 15.0, y1, y1 + 3.0, sz - 3.0, sz + 3.0, col("#3a3a40"), "stamp", grp=G, shadow=False)            # the stamp's base
    st.box(sx + 9.6, sx + 14.4, y1 + 3.0, y1 + 6.0, sz - 2.4, sz + 2.4, col("#8a8e94"), "stamp", grp=G, shadow=False)      # its band of dates
    st.cyl((sx + 12.0, sz), 1.6, y1 + 6.0, y1 + 12.0, col("#1c1c20"), name="stamp", grp=G, shadow=False)
    st.ball((sx + 12.0, y1 + 12.6, sz), 2.4, col("#1c1c20"), name="stamp", grp=G, shadow=False, squash=(1, 0.8, 1))
    # a stack of claim forms, a wire tray, a pencil cup
    st.box(196.0, 222.0, y1, y1 + 3.5, 10.0, 30.0, lambda c: col(PAPER) * (0.9 + 0.1 * (0.5 + 0.5 * np.sin(c.Y * 30.0)))[..., None],
           "forms", grp=G, shadow=False)
    st.box(196.0, 222.0, y1 + 3.5, y1 + 3.6, 10.0, 30.0, col("#efeadb"), "forms", grp=G, shadow=False)
    for (a0, a1, b0, b1) in ((236.0, 268.0, 8.0, 9.0), (236.0, 268.0, 33.0, 34.0), (236.0, 237.0, 8.0, 34.0), (267.0, 268.0, 8.0, 34.0)):
        st.box(a0, a1, y1, y1 + 6.0, b0, b1, chrome("#b8bcc0"), "tray", grp=G, shadow=False)
    st.box(238.0, 266.0, y1 + 0.5, y1 + 2.0, 10.0, 32.0, col("#e6e0cc"), "tray", grp=G, shadow=False)
    st.cyl((276.0, 18.0), 3.4, y1, y1 + 10.0, painted_steel("#6a7a8a", seed=185), name="pencils", grp=G, shadow=False)
    for i, (dx, dz, c_) in enumerate(((-1.0, 0.5, "#e8b030"), (0.8, -0.6, "#e8b030"), (0.2, 1.2, "#c03028"))):
        st.stick((276.0 + dx * 0.6, y1 + 6.0, 18.0 + dz * 0.6), (276.0 + dx * 2.2, y1 + 17.0, 18.0 + dz * 2.0), 0.35, col(c_), "pencils", grp=G)
    # the slot under the glass, for passing papers: a dark gap in the counter's back edge
    st.box(140.0, 220.0, y1 - 0.1, y1 + 0.05, -1.0, 3.0, col("#20201e"), "counter", grp=G, shadow=False)


def receipt(st, G="receipt"):
    """The receipt, as it lands on the counter: a slip of thin paper (it has been in a bib pocket), come to rest at the
    counter's front edge with its near half hanging over it, so that from among the shelves (we see the counter's top
    almost edge on) its printed face shows: a line or two of print and a stamp-box."""
    rx, rz, ang = M.RECEIPT
    y = M.COUNTER[3]
    z1 = M.COUNTER[5]
    a = math.radians(ang)
    ux, uz = math.cos(a), -math.sin(a)                     # along the slip (it lies a little askew)
    L, top, hang = 15.0, 4.0, 5.0                          # its length; how much of its width lies on the top, how much hangs

    def m(c):
        g = px_of(c, 1.6)
        out = col("#f6f2e6") * (0.96 + 0.04 * fbm(c.X / 2, (c.Y + c.Z) / 2, 191, 2))[..., None]
        s_ = (c.X - rx) * ux + (c.Z - rz) * uz
        w_ = (z1 - c.Z) + (y - c.Y)                         # across the slip, from its fold at the edge
        lines = lines_aa(w_, 1.4, 0.35, g) * band(s_, -L / 2 + 1.5, L / 2 - 4.0, g)
        out = out * (1 - 0.25 * lines[..., None])
        return lay(out, "#7a3a48", rect_uv(s_, w_, L / 2 - 3.6, L / 2 - 1.0, -4.0, -1.0, g) * 0.6)

    def P(s_, dz, dy):
        return (rx + ux * s_, y + dy, z1 + dz + uz * s_)
    # on the top: from `top` cm in from the edge to the edge, lifted a hair; over the edge: down its front, curling out
    st.poly([P(-L / 2, -top, 0.25), P(L / 2, -top, 0.25), P(L / 2, 0.3, 0.25), P(-L / 2, 0.3, 0.25)], m, "receipt", grp=G)
    st.poly([P(-L / 2, 0.3, 0.25), P(L / 2, 0.3, 0.25), P(L / 2, 0.6, -hang * 0.55), P(-L / 2, 0.6, -hang * 0.55)], m, "receipt", grp=G)
    st.poly([P(-L / 2, 0.6, -hang * 0.55), P(L / 2, 0.6, -hang * 0.55), P(L / 2, 1.4, -hang), P(-L / 2, 1.4, -hang)], m, "receipt", grp=G)


# ---------------------------------------------------------------- Opal's stool, her knitting, her filing cabinet
def stool(st, G="back"):
    """Her stool: a round seat in dark green vinyl, buttoned, on four chrome legs with a foot ring."""
    sx, sz, sh, sr = M.STOOL

    def m_seat(c):
        n = normals(c)
        out = col("#4a6a5a") * (0.80 + 0.30 * np.clip(n[..., 1], 0, 1))[..., None]
        return out * (0.95 + 0.08 * fbm(c.X / 3, c.Z / 3, 201, 2))[..., None]
    st.cyl((sx, sz), sr, sh - 5.0, sh - 1.2, m_seat, name="stool", grp=G)
    st.ball((sx, sh - 1.2, sz), sr * 0.98, m_seat, name="stool", grp=G, squash=(1.0, 0.16, 1.0))
    for i in range(4):
        a = math.pi / 4 + i * math.pi / 2
        p0 = (sx + math.cos(a) * sr * 1.05, 0.5, sz + math.sin(a) * sr * 1.05)
        p1 = (sx + math.cos(a) * sr * 0.55, sh - 5.0, sz + math.sin(a) * sr * 0.55)
        st.stick(p0, p1, 1.1, col("#c4c8ce"), "stool", grp=G)
    pts = [(sx + math.cos(t) * sr * 0.86, 26.0, sz + math.sin(t) * sr * 0.86) for t in np.linspace(0, 2 * math.pi, 17)]
    st.rope(pts, 0.8, col("#c4c8ce"), name="stool", grp=G)
    st.feet["stool"] = (sx - sr, sx + sr, sz - sr, sz + sr)


def knitting(st, G="back"):
    """Her knitting basket on the floor by the stool: round wicker, two balls of gray wool and the needles in it, and the
    scarf she has been knitting since about 1990 in the regulation colour, trailing out over its rim and away across the
    carpet, a very long way."""
    bx, bz, br, bh = M.BASKET

    def m_wicker(c):
        ang = np.arctan2(c.X - bx, c.Z - bz)
        g = px_of(c, 1.0)
        weave = 0.5 + 0.5 * np.sin(ang * br * 1.6) * np.sin(c.Y * 1.6)
        out = col("#b48a52") * (0.82 + 0.25 * weave)[..., None]
        rows = lines_aa(c.Y, 3.2, 0.5, g)
        return out * (1 - 0.18 * rows[..., None])
    st.cyl((bx, bz), br * 0.86, 0, bh, m_wicker, r1=br, name="basket", grp=G, hollow=True)
    st.cyl((bx, bz), br * 0.90, 0, 1.0, col("#5a4a36"), name="basket", grp=G, shadow=False)              # its floor, inside
    st.cyl((bx, bz), br * 1.03, bh - 1.5, bh, col("#9a7444"), name="basket", grp=G, shadow=False, hollow=True)
    st.occ.append(("c", bx, bz, br * 0.78, 0.0, bh - 2.0))
    wool = col("#8e9092")
    st.ball((bx - 4.0, bh - 5.0, bz - 3.0), 6.5, wool, name="basket", grp=G, shadow=False)
    st.ball((bx + 5.0, bh - 6.0, bz + 2.0), 6.0, wool * 0.92, name="basket", grp=G, shadow=False)
    st.stick((bx - 2.0, bh - 4.0, bz), (bx + 8.0, bh + 16.0, bz - 6.0), 0.35, col("#c8b070"), "basket", grp=G)
    st.stick((bx - 1.0, bh - 4.0, bz + 1.0), (bx + 3.0, bh + 17.0, bz - 9.0), 0.35, col("#c8b070"), "basket", grp=G)
    st.feet["basket"] = (bx - br, bx + br, bz - br, bz + br)

    # the scarf: a knitted band 16 cm wide, out over the rim nearest the aisle, down to the carpet and away in long loops
    path = curve3([(bx - 6.0, bh + 2.0, bz + 6.0), (bx - 14.0, bh - 2.0, bz + 14.0), (bx - 20.0, 8.0, bz + 24.0), (bx - 24.0, 0.8, bz + 44.0),
                   (bx - 62.0, 0.8, bz + 92.0), (bx - 34.0, 0.8, bz + 150.0), (bx - 84.0, 0.8, bz + 210.0), (bx - 50.0, 0.8, bz + 280.0),
                   (bx - 96.0, 0.8, bz + 350.0), (bx - 70.0, 0.8, bz + 430.0), (bx - 104.0, 0.8, bz + 520.0)], 6)
    wdt = 16.0

    def m_scarf(c):
        g = px_of(c, 1.4)
        rib = 0.5 + 0.5 * np.sin((c.U if hasattr(c, "U") else c.X) * 2.4)
        row = 0.5 + 0.5 * np.sin((c.V if hasattr(c, "V") else c.Z) * 1.9)
        out = col("#6e7276") * (0.80 + 0.16 * rib[..., None] + 0.06 * row[..., None])
        return out
    for a, b in zip(path[:-1], path[1:]):
        a, b = np.asarray(a), np.asarray(b)
        d = b - a
        side = nrm(np.cross(d, [0.0, 1.0, 0.0])) * wdt / 2
        if abs(d[1]) > abs(np.hypot(d[0], d[2])):                       # (over the rim: hanging, its face toward us)
            side = nrm(np.cross(d, [0.0, 0.0, 1.0])) * wdt / 2
        st.poly([tuple(a - side), tuple(b - side), tuple(b + side), tuple(a + side)], m_scarf, "scarf", grp=G)
    # its end: a fringe
    end = np.asarray(path[-1])
    for k in range(7):
        q = end + nrm(np.cross(np.asarray(path[-1]) - np.asarray(path[-2]), [0, 1, 0])) * (-wdt / 2 + wdt * k / 6)
        st.stick(tuple(q + [0, 0.4, 0]), tuple(q + [-4.0, 0.4, -1.0]), 0.35, col("#7e8285"), "scarf", grp=G)


def cabinet(st, G="back"):
    """A four-drawer filing cabinet in the corner left of the counter (Opal's: forty-one statements of nothing, filed)."""
    x0, x1, y0, y1, z0, z1 = M.CABINET
    m = painted_steel("#8a918c", seed=211, amt=0.05, chips=0.2)
    st.box(x0, x1, y0, y1, z0, z1, m, "cabinet", grp=G)
    step = (y1 - 4.0) / 4
    for i in range(4):
        b0 = 2.0 + step * i + 1.0
        b1 = b0 + step - 2.0
        st.box(x0 + 1.5, x1 - 1.5, b0, b1, z1, z1 + 0.6, painted_steel("#929a94", seed=212 + i, amt=0.05), "cabinet", grp=G, shadow=False)
        st.box((x0 + x1) / 2 - 6.0, (x0 + x1) / 2 + 6.0, b1 - 9.0, b1 - 7.0, z1 + 0.6, z1 + 2.4, chrome(), "cabinet", grp=G, shadow=False)
        st.box((x0 + x1) / 2 - 4.0, (x0 + x1) / 2 + 4.0, b1 - 5.5, b1 - 2.5, z1 + 0.6, z1 + 0.9, col("#ece6d0"), "cabinet", grp=G, shadow=False)


# ---------------------------------------------------------------- the door: its casing, the leaf shut, the leaf open
DOOR_GRAY = "#7f8891"


def door_casing(st, G="wall"):
    dx0, dx1, dy0, dy1 = M.DOOR
    fw, fd = M.DOOR_FRAME, 1.6
    m = painted_steel(DOOR_GRAY, seed=221, chips=0.4)
    st.box(dx0 - fw, dx0, 0, dy1 + fw, 0, fd, m, "doorcasing", grp=G)
    st.box(dx1, dx1 + fw, 0, dy1 + fw, 0, fd, m, "doorcasing", grp=G)
    st.box(dx0 - fw, dx1 + fw, dy1, dy1 + fw, 0, fd, m, "doorcasing", grp=G)


def door_leaf(st, open_=False, G="door"):
    """The leaf: gray steel, a narrow wired-glass slit (the hall's light through it), a lever handle on the left, the
    hinges on the right; a little card in a holder: PROPERTY & EFFECTS: STAFF. It opens OUT into the hall: open, it stands
    swung away into the hall on its right hinges, seen past the jamb."""
    dx0, dx1, dy0, dy1 = M.DOOR
    sx0, sx1, sy0, sy1 = M.DOOR_SLIT
    wleaf = dx1 - dx0 - 0.6

    def m_leaf(c, along):
        u, v = along(c), c.Y
        g = px_of(c, 1.2)
        base = col(DOOR_GRAY) * (0.94 + 0.08 * fbm(u / 20, v / 20, 231, 3))[..., None]
        scuff = np.clip((fbm(u / 4, v / 2, 232, 3) - 0.62) * 4, 0, 1) * np.clip((40 - v) / 30, 0, 1)
        base = lay(base, "#6c7178", scuff * 0.6)
        su0, su1 = sx0 - dx0, sx1 - dx0
        slit = rect_uv(u, v, su0, su1, sy0, sy1, g)
        bead = rect_uv(u, v, su0 - 1.6, su1 + 1.6, sy0 - 1.6, sy1 + 1.6, g) - slit
        wires = np.maximum(lines_aa(u - su0, 2.6, 0.5, g, fade=False), lines_aa(v, 2.6, 0.5, g, fade=False))
        glass = col("#e6efe0") * (0.85 + 0.15 * fbm(u / 6, v / 6, 233, 2))[..., None]
        glass = glass * (1 - 0.14 * wires[..., None])
        out = lay(base, "#6a7078", np.clip(bead, 0, 1) * 0.9)
        card = rect_uv(u, v, 22.0, 52.0, 148.0, 160.0, g)
        out = lay(out, "#e4ddc8", card)
        out = out * (1 - slit[..., None]) + glass * slit[..., None] * 0.15
        e = glass * (slit * 1.25)[..., None]
        return out, e

    if not open_:
        z = 0.8

        def m_face(c):
            return m_leaf(c, lambda c_: c_.X - dx0)
        st.poly([(dx0 + 0.3, 0.5, z), (dx1 - 0.3, 0.5, z), (dx1 - 0.3, dy1 - 0.3, z), (dx0 + 0.3, dy1 - 0.3, z)], m_face, "door", grp=G)
        hx, hy = dx0 + 9.0, 102.0
        st.cyl((hx, hy), 2.8, z, z + 1.2, chrome(), axis="z", name="door", grp=G, shadow=False)
        st.stick((hx, hy, z + 3.5), (hx + 11.0, hy - 0.8, z + 3.8), 0.9, col("#c8ccd2"), "door", grp=G)
        st.stick((hx, hy, z + 0.8), (hx, hy, z + 3.6), 0.8, col("#c8ccd2"), "door", grp=G)
        for hy2 in (24.0, 102.0, 182.0):
            st.box(dx1 - 2.4, dx1 - 0.2, hy2, hy2 + 10, z, z + 1.0, painted_steel("#7a8088", 222), "door", grp=G, shadow=False)
    else:
        ang = math.radians(72.0)
        ax, az = dx1 - 0.5, -M.WALL_T
        ex, ez = ax - wleaf * math.cos(ang), az - wleaf * math.sin(ang)

        def m_open(c):
            return m_leaf(c, lambda c_: wleaf - np.hypot(c_.X - ax, c_.Z - az))
        st.poly([(ex, 0.5, ez), (ax, 0.5, az), (ax, dy1 - 0.5, az), (ex, dy1 - 0.5, ez)], m_open, "door", grp=G, flag=OUTSIDE)


# ---------------------------------------------------------------- the shelving and what is on it
def m_shelf_steel(seed=0):
    return painted_steel(SHELF_STEEL, seed=seed, amt=0.07, chips=0.25)


def unit(st, side, z0, z1, shelves, seed=0, G="back"):
    """One shelving unit: four angle-iron posts with their rows of holes, the shelves (each a steel pan with a turned-
    down lip), braced at the back with an X of flat bar."""
    x0, x1 = M.LEFT_X if side == "L" else M.RIGHT_X
    xf = x1 if side == "L" else x0                             # the face toward the aisle
    xb = x0 if side == "L" else x1
    m = m_shelf_steel(seed)

    def m_post(c):
        out = m(c)
        g = px_of(c, 1.0)
        holes = lines_aa(c.Y, 2.6, 0.45, g, fade=False)
        return out * (1 - 0.35 * holes[..., None])
    for (zp, xp) in ((z0, xf), (z1, xf), (z0, xb), (z1, xb)):
        sx = -1 if (xp == xf) == (side == "L") else 1
        a0, a1 = (xp - 3.2, xp) if xp == x1 else (xp, xp + 3.2)
        b0, b1 = (zp, zp + 3.2) if zp == z0 else (zp - 3.2, zp)
        st.box(a0, a1, 0.0, M.UNIT_H, b0, b1, m_post, f"shelfpost-{side}", grp=G, shadow=False)
    for y in shelves:
        st.box(x0 + 0.5, x1 - 0.5, y - 0.8, y, z0 + 0.4, z1 - 0.4, m, f"shelf-{side}", grp=G, shadow=True)
        lip0, lip1 = (xf - 0.8, xf) if side == "L" else (xf, xf + 0.8)
        st.box(lip0, lip1, y - 3.2, y, z0 + 0.4, z1 - 0.4, m, f"shelflip-{side}", grp=G, shadow=False)
    # the X brace across the back
    for (ya, yb) in ((4.0, M.UNIT_H - 6.0), (M.UNIT_H - 6.0, 4.0)):
        st.stick((xb + (1.0 if side == "L" else -1.0), ya, z0 + 2.0), (xb + (1.0 if side == "L" else -1.0), yb, z1 - 2.0), 0.6, col("#7a827c"),
                 f"shelf-{side}", grp=G)


def archive_box(st, side, y, zc, w=31.0, h=26.0, d=39.0, seed=0, label=True, G="back", lid=True, turn=0.0):
    """An archive box on a shelf, its end (a white label, a hand hole) to the aisle."""
    x0, x1 = M.LEFT_X if side == "L" else M.RIGHT_X
    xf = (x1 - 2.0) if side == "L" else (x0 + 2.0)
    xc = xf - d / 2 if side == "L" else xf + d / 2
    rng = np.random.default_rng(seed)
    tone = 0.92 + 0.12 * rng.random()
    face_sign = 1.0 if side == "L" else -1.0

    def m(c):
        n = normals(c)
        out = col(CARD) * tone * (0.92 + 0.10 * fbm(c.X / 6 + seed, (c.Y + c.Z) / 6, 241, 2))[..., None]
        if label:
            end = (n[..., 0] * face_sign) > 0.7
            g = px_of(c, 1.6)
            lab = rect_uv(c.Z, c.Y, zc - w * 0.32, zc + w * 0.32, y + h * 0.34, y + h * 0.74, g) * end
            out = lay(out, "#e2d8bc", lab)
            out = lay(out, "#5a4a3a", lines_aa(c.Y - y, 2.6, 0.5, g) * band(c.Y, y + h * 0.40, y + h * 0.70, g) * band(c.Z, zc - w * 0.24, zc + w * 0.24, g) * end * 0.55)
            hole = rect_uv(c.Z, c.Y, zc - 5.0, zc + 5.0, y + h * 0.84, y + h * 0.84 + 2.4, g) * end
            out = lay(out, "#2a2420", hole * 0.9)
        return out
    obox(st, (xc, y, zc), (d, h - 2.0, w), turn, m, "boxes-" + side, grp=G, faces=("front", "back", "left", "right", "top"))
    if lid:
        obox(st, (xc, y + h - 3.0, zc), (d + 1.0, 3.0, w + 1.0), turn, m, "boxes-" + side, grp=G, shadow=False, faces=("front", "back", "left", "right", "top"))


def tag(st, side, y_shelf, zc, seed=0, name="tags", G="back", hang=9.0, item=None):
    """A brown property tag on a string, hanging over the shelf's lip in front of its thing (a date on it in pencil)."""
    x0, x1 = M.LEFT_X if side == "L" else M.RIGHT_X
    xl = (x1 + 0.9) if side == "L" else (x0 - 0.9)
    rng = np.random.default_rng(seed)
    dz = rng.uniform(-3.0, 3.0)
    tw, th = 4.6, 8.0
    top = y_shelf - 1.0 - rng.uniform(0.0, hang - 8.0 if hang > 8 else 0.0)

    def m(c):
        g = px_of(c, 1.4)
        out = col(TAG) * (0.92 + 0.10 * fbm(c.Z / 2, c.Y / 2, 251 + seed, 2))[..., None]
        ring_ = np.clip(1 - np.abs(np.hypot(c.Z - (zc + dz), c.Y - (top - 1.3)) - 0.8) / (g * 0.8 + 0.2), 0, 1)
        out = lay(out, "#dccaa0", ring_)
        writing = lines_aa(c.Y - top, 1.9, 0.35, g) * band(c.Y, top - th + 1.2, top - 3.0, g) * band(c.Z, zc + dz - tw / 2 + 0.8, zc + dz + tw / 2 - 0.8, g)
        return lay(out, "#4a3a2c", writing * 0.7)
    lean = rng.uniform(-0.6, 0.6)
    st.poly([(xl, top, zc + dz - tw / 2), (xl, top, zc + dz + tw / 2), (xl + lean, top - th, zc + dz + tw / 2 + 0.6), (xl + lean, top - th, zc + dz - tw / 2 + 0.6)],
            m, name, grp=G)
    # the string: up over the lip to the thing
    if item is not None:
        st.stick((xl, top - 1.3, zc + dz), (xl - (1.2 if side == "L" else -1.2), y_shelf + 0.4, zc + dz * 0.5), 0.12, col("#e8dcc0"), name, grp=G, min_px=0.4)
        st.stick((xl - (1.2 if side == "L" else -1.2), y_shelf + 0.4, zc + dz * 0.5), item, 0.12, col("#e8dcc0"), name, grp=G, min_px=0.4)


# ---- the tagged things themselves (each in its own measurements, standing on a shelf at (x, y, z))
def thing_sandal(st, x, y, z, G="back"):
    """A Roman sandal (1951): a thick leather sole the shape of a foot and a lattice of straps over it, its laces hanging,
    propped against the back of the bay so that its strapped top faces the aisle."""
    a = math.radians(60.0)
    along = np.array([-math.cos(a), math.sin(a), 0.0])     # heel on the shelf, toe up against the back of the bay
    ax = np.array([0.0, 0.0, 1.0])                        # across the sole
    up = nrm(np.cross(ax, along))                         # out of the sole's top: toward the aisle and up
    if up[0] < 0:
        up = -up
    L, Wd = 27.0, 11.0
    o = np.array([x + 12.0, y + 0.2, z - Wd / 2])        # the heel's corner

    def half(u):                                          # the foot's half width along it: a narrow heel, a broad ball, a round toe
        t = np.clip(u / L, 0, 1)
        return 3.2 + 2.2 * np.sin(np.clip(t * 1.25, 0, 1) * math.pi / 2) ** 1.2 - 3.0 * np.clip((t - 0.86) / 0.14, 0, 1) ** 2

    def foot(c):
        return (c.U >= 0) & (c.U <= L) & (np.abs(c.V - Wd / 2) <= half(c.U))

    def m_sole(c):
        out = col("#6a3e22") * (0.85 + 0.2 * fbm(c.U / 2, c.V / 2, 261, 2))[..., None]
        g = px_of(c, 1.2)
        edge = np.clip(1 - (half(c.U) - np.abs(c.V - Wd / 2)) / (g + 0.6), 0, 1)
        return lay(out, "#3a2214", edge * 0.7), None, foot(c)

    def m_straps(c):
        u, v = c.U, c.V - Wd / 2
        lattice = (np.abs(((u + v * 1.1) / 4.2) % 1 - 0.5) > 0.36) | (np.abs(((u - v * 1.1) / 4.2) % 1 - 0.5) > 0.36)
        band_ = (np.abs(u - 5.0) < 1.0) | (np.abs(v) < 0.7)
        keep = foot(c) & (lattice | band_) & (u > 2.5) & (u < L - 3.0)
        out = col("#8a5432") * (0.85 + 0.25 * fbm(c.U / 1.5, c.V / 1.5, 262, 2))[..., None]
        return out, None, keep
    P = lambda s_, t_, h_: tuple(o + along * s_ + ax * t_ + up * h_)
    st.poly([P(0, 0, 0.0), P(L, 0, 0.0), P(L, Wd, 0.0), P(0, Wd, 0.0)], m_sole, "sandal", grp=G)
    st.poly([P(0, 0, 1.6), P(L, 0, 1.6), P(L, Wd, 1.6), P(0, Wd, 1.6)], m_sole, "sandal", grp=G)
    st.poly([P(0, 0, 2.8), P(L, 0, 2.8), P(L, Wd, 2.8), P(0, Wd, 2.8)], m_straps, "sandal", grp=G)
    # the laces, hanging loose over the sole's heel
    for k, dv in enumerate((-2.0, 2.0)):
        st.rope([P(6.0, Wd / 2 + dv, 3.0), P(3.0, Wd / 2 + dv * 1.6, 4.0), P(0.5, Wd / 2 + dv * 2.2, 5.5), (o[0] + 5.0, y + 0.5, z + dv * 3.0)],
                0.25, col("#5a3018"), name="sandal", grp=G)
    return P(3.0, Wd / 2, 1.0)


def thing_lamp(st, x, y, z, G="back"):
    """A clay oil lamp: a round body with a filling hole, a nozzle black with soot, a little ring handle."""
    clay = "#b8643a"
    st.ball((x, y + 2.6, z), 4.6, col(clay), name="oillamp", grp=G, squash=(1.0, 0.55, 1.15), shadow=False)
    st.ball((x, y + 4.6, z), 1.0, col("#4a2a1a"), name="oillamp", grp=G, shadow=False)
    st.stick((x + 3.0, y + 3.0, z + 3.6), (x + 5.4, y + 3.4, z + 7.0), 1.4, col(clay), "oillamp", grp=G, r1=1.0)
    st.ball((x + 5.6, y + 3.6, z + 7.4), 1.0, col("#2a1a14"), name="oillamp", grp=G, shadow=False)
    st.rope([(x - 2.0, y + 3.2, z - 4.6), (x - 2.6, y + 6.0, z - 6.4), (x - 2.0, y + 4.0, z - 8.0)], 0.6, col(clay), name="oillamp", grp=G)
    return (x + 2.0, y + 2.0, z + 2.0)


def thing_cup(st, x, y, z, G="back"):
    """A tin cup, dented, with a wire handle."""
    tin = "#a4a8a4"
    st.cyl((x, z), 4.4, y, y + 9.0, painted_steel(tin, seed=271, amt=0.12), name="cup", grp=G, r1=4.8, hollow=True, shadow=False)
    st.cyl((x, z), 4.3, y, y + 0.6, col("#6a6e6c"), name="cup", grp=G, shadow=False)
    st.rope([(x + 4.0, y + 7.5, z + 1.0), (x + 7.0, y + 6.5, z + 2.0), (x + 7.0, y + 2.5, z + 2.0), (x + 4.0, y + 2.0, z + 1.0)], 0.4, col("#8a8e8c"),
            name="cup", grp=G)
    return (x + 4.0, y + 4.0, z)


def thing_hat(st, x, y, z, G="back"):
    """A cowboy hat bleached white by years of sun, sitting on its shelf just under our eye and turned to face us, so
    that it shows its own outline: the brim rolled up hard at both sides, dipping in front, the crown tall and creased,
    a thin band."""
    felt = "#e6e0cc"

    def m(c):
        return col(felt) * (0.90 + 0.12 * fbm(c.X / 4, (c.Y + c.Z) / 4, 281, 2))[..., None]
    cx_, cz_ = M.VIEW["cam"]
    look = nrm([cx_ - x, 0.0, cz_ - z])                 # toward us, on the floor plan
    side = nrm(np.cross([0.0, 1.0, 0.0], look))         # the hat's left-right, square to our line of sight
    c0 = np.array([x + 2.0, y, z])
    st.ball(tuple(c0 + [0, 1.4, 0]), 14.0, m, name="hat", grp=G, squash=(1.0, 0.08, 1.0), shadow=False)          # the brim's flat middle
    for s_ in (-1, 1):                                  # its sides, rolled up steep
        for k in range(6):
            t = k / 5.0
            for d in (-7.0, -4.5, -1.5, 1.5, 4.5, 7.0):
                q = c0 + side * s_ * (11.0 + t * 6.0) + look * d * (1.0 - 0.35 * t) + np.array([0, 2.0 + t * 6.5 + 0.04 * d * d, 0])
                st.ball(tuple(q), 2.7 - t * 0.5, m, name="hat", grp=G, shadow=False)
    for d in (-1, 1):                                   # the brim's front and back, dipped a little
        st.ball(tuple(c0 + look * d * 12.0 + [0, 1.0, 0]), 5.0, m, name="hat", grp=G, squash=(1.0, 0.22, 1.0), shadow=False)
    st.cyl((c0[0], c0[2]), 8.0, y + 1.6, y + 13.5, m, name="hat", grp=G, r1=7.0, shadow=False)                  # the crown
    st.ball(tuple(c0 + [0, 13.5, 0]), 7.0, m, name="hat", grp=G, squash=(1.0, 0.36, 1.0), shadow=False)
    st.stick(tuple(c0 + look * 4.5 + [0, 16.2, 0]), tuple(c0 - look * 4.5 + [0, 16.0, 0]), 0.9, col("#c4bca4"), "hat", grp=G)   # the crease
    st.cyl((c0[0], c0[2]), 8.1, y + 2.0, y + 4.4, col("#5a4232"), name="hat", grp=G, shadow=False)                  # the band
    return tuple(c0 + look * 7.0 + [0, 2.0, 0])


def thing_feather(st, x, y, z, G="back"):
    """A goose feather, white and gray, standing in a small glass jar."""
    st.cyl((x, z), 3.6, y, y + 9.0, lambda c: (col("#b8c8c4") * 0.35, col("#c8d8d4") * 0.10 * np.ones((len(c.X), 3), F32)), name="feather", grp=G,
           hollow=True, shadow=False)
    st.cyl((x, z), 3.8, y + 8.4, y + 9.4, col("#9aa8a6"), name="feather", grp=G, hollow=True, shadow=False)
    p0 = np.array([x, y + 2.0, z])
    tipp = np.array([x + 4.0, y + 38.0, z + 5.0])
    st.stick(tuple(p0), tuple(tipp), 0.35, col("#e8e4d8"), "feather", grp=G)
    ax = nrm(tipp - p0)
    side = nrm(np.cross(ax, [1.0, 0.0, 0.0]))

    def m_vane(c):
        t = (c.U) / 30.0                                 # 0 at the vane's foot, 1 at its tip
        w = np.clip(np.sin(np.clip(t, 0, 1) * math.pi) ** 0.6 * 3.4 - np.abs(c.V - 3.4), -1, 4)
        keep = (w > 0) & (t > 0) & (t < 1.02)
        barbs = 0.5 + 0.5 * np.sin(c.U * 5.0 + np.abs(c.V - 3.4) * 2.0)
        out = col("#ece8de") * (0.86 + 0.12 * barbs)[..., None]
        out = lay(out, "#9a9c9a", np.clip((t - 0.55) * 2, 0, 1) * np.clip((np.abs(c.V - 3.4) - 1.2) / 2, 0, 1) * 0.6)
        return out, None, keep
    a = p0 + ax * 8.0 - side * 3.4
    b = a + ax * 30.0
    st.poly([tuple(a), tuple(b), tuple(b + side * 6.8), tuple(a + side * 6.8)], m_vane, "feather", grp=G)
    return (x + 3.0, y + 4.0, z)


def thing_cassette(st, x, y, z, G="back"):
    """A cassette tape in its clear case, standing on edge like a book, its paper label to the aisle (somebody wrote on it)."""
    def m(c):
        n = normals(c)
        g = px_of(c, 1.6)
        face = np.abs(n[..., 0]) > 0.7
        out = col("#4a4e56") * np.ones((len(c.X), 3), F32)
        lab = rect_uv(c.Z, c.Y, z - 4.6, z + 4.6, y + 1.2, y + 5.6, g) * face
        out = lay(out, "#e8e2cc", lab)
        reel = (disc_uv(c.Z, c.Y, z - 2.4, y + 3.4, 0.9, g) + disc_uv(c.Z, c.Y, z + 2.4, y + 3.4, 0.9, g)) * face
        out = lay(out, "#1c1c20", np.clip(reel, 0, 1))
        scrawl = lines_aa(c.Y - y, 1.3, 0.3, g) * band(c.Y, y + 4.4, y + 5.4, g) * band(c.Z, z - 4.0, z + 4.0, g) * face
        return lay(out, "#2a3a8a", scrawl * 0.8)
    st.box(x - 0.8, x + 0.8, y, y + 7.0, z - 5.5, z + 5.5, m, "cassette", grp=G, shadow=False)
    return (x, y + 3.0, z)


def thing_horseshoe(st, x, y, z, G="back"):
    """A horseshoe, rusty, stood up on its heels against the back of the bay, open end down."""
    iron = col("#6a4434")
    pts = []
    for t in np.linspace(-1.15, 1.15, 13):
        pts.append((x - 3.0, y + 1.0 + 6.0 + 6.0 * math.cos(t), z + 6.0 * math.sin(t)))
    pts = [(x - 3.0, y + 0.6, z - 6.0 * math.sin(1.15) * 0.95)] + pts[::-1][::-1] + [(x - 3.0, y + 0.6, z + 6.0 * math.sin(1.15) * 0.95)]
    st.rope(pts, 1.0, iron, name="horseshoe", grp=G)
    for t in (-0.7, 0.0, 0.7):
        st.ball((x - 2.0, y + 7.0 + 6.0 * math.cos(t), z + 6.0 * math.sin(t)), 0.5, col("#3a2a20"), name="horseshoe", grp=G, shadow=False)
    return (x - 2.0, y + 2.0, z)


def thing_gnome(st, x, y, z, G="back"):
    """A garden gnome (nobody knows): a blue coat, a white beard, a pointed red hat, a little shovel, facing the aisle."""
    st.cyl((x, z), 6.4, y, y + 3.0, col("#6a5040"), name="gnome", grp=G, shadow=False)                         # boots
    st.cyl((x, z), 5.6, y + 3.0, y + 15.0, col("#3a5aa8"), name="gnome", grp=G, r1=4.2, shadow=False)           # coat
    st.cyl((x, z), 4.4, y + 12.0, y + 13.4, col("#4a3020"), name="gnome", grp=G, shadow=False)                  # belt
    st.ball((x + 1.5, y + 18.6, z), 3.6, col("#e8b090"), name="gnome", grp=G, shadow=False)                      # face
    st.ball((x + 2.6, y + 15.6, z), 3.4, col("#f0eee6"), name="gnome", grp=G, squash=(0.8, 1.2, 1.0), shadow=False)   # beard
    st.ball((x + 4.6, y + 18.4, z), 0.9, col("#e08a74"), name="gnome", grp=G, shadow=False)                      # nose
    st.cyl((x, z), 4.0, y + 20.0, y + 31.0, col("#c8302a"), name="gnome", grp=G, r1=0.3, shadow=False)           # hat
    st.stick((x + 4.0, y + 4.0, z + 4.0), (x + 4.5, y + 15.0, z + 6.0), 0.4, col("#7a5a3a"), "gnome", grp=G)
    st.box(x + 3.0, x + 6.0, y + 1.0, y + 5.0, z + 4.5, z + 7.5, col("#8a8e94"), "gnome", grp=G, shadow=False)
    return (x + 4.0, y + 6.0, z - 3.0)


def thing_lantern(st, x, y, z, G="back"):
    """A kerosene lantern: a tin fount, a glass globe in its wire guard, a bail handle."""
    tin = painted_steel("#8a3a2a", seed=291, amt=0.10, chips=0.3)
    st.cyl((x, z), 7.0, y, y + 6.0, tin, name="lantern", grp=G, shadow=False)
    st.cyl((x, z), 4.4, y + 6.0, y + 19.0, lambda c: (col("#c8d4c0") * 0.5, col("#d8e4cc") * 0.12 * np.ones((len(c.X), 3), F32)),
           name="lantern", grp=G, shadow=False)
    for k in range(4):
        a = k * math.pi / 2 + 0.4
        st.stick((x + math.cos(a) * 5.4, y + 6.0, z + math.sin(a) * 5.4), (x + math.cos(a) * 5.0, y + 19.0, z + math.sin(a) * 5.0), 0.25,
                 col("#5a3a2a"), "lantern", grp=G)
    st.cyl((x, z), 5.6, y + 19.0, y + 22.0, tin, name="lantern", grp=G, r1=3.0, shadow=False)
    st.rope([(x, y + 6.0, z - 7.0), (x + 0.0, y + 24.0, z - 4.0), (x, y + 27.0, z), (x, y + 24.0, z + 4.0), (x, y + 6.0, z + 7.0)], 0.3,
            col("#4a4a4a"), name="lantern", grp=G)
    return (x + 6.0, y + 3.0, z)


def thing_ball(st, x, y, z, G="back"):
    """A bowling ball, dark blue with a marbled swirl, its three holes up."""
    def m(c):
        sw = fbm(c.X / 3, (c.Y + c.Z) / 3, 301, 3)
        out = lerp(col("#22305a") * np.ones((len(c.X), 3), F32), col("#5a6aa8") * np.ones((len(c.X), 3), F32), np.clip((sw - 0.45) * 3, 0, 1)[..., None])
        return out
    st.ball((x, y + 10.8, z), 10.8, m, name="ball", grp=G, shadow=False)
    for (dz, dx) in ((-2.0, 1.8), (2.0, 1.8), (0.0, -2.6)):
        st.ball((x + dx + 1.5, y + 20.0, z + dz), 1.1, col("#0c0c14"), name="ball", grp=G, shadow=False)
    return (x + 8.0, y + 4.0, z)


def thing_cone(st, x, y, z, G="back"):
    """A traffic cone, orange, a white reflective band."""
    st.box(x - 17.0, x + 17.0, y, y + 3.0, z - 17.0, z + 17.0, col("#c0501e"), "cone", grp=G, shadow=False)
    st.cyl((x, z), 12.0, y + 3.0, y + 40.0, lambda c: lay(col("#e2662a") * np.ones((len(c.X), 3), F32), "#ecece4",
                                                       band(c.Y, y + 20.0, y + 27.0, px_of(c, 1.0))), name="cone", grp=G, r1=2.2, shadow=False)
    return (x - 6.0, y + 4.0, z)


THINGS = {"sandal": thing_sandal, "lamp": thing_lamp, "cup": thing_cup, "hat": thing_hat, "feather": thing_feather, "cassette": thing_cassette,
          "horseshoe": thing_horseshoe, "gnome": thing_gnome, "lantern": thing_lantern, "skate": thing_ball}
THING_NAME = {"sandal": "sandal", "lamp": "oillamp", "cup": "cup", "hat": "hat", "feather": "feather", "cassette": "cassette",
              "horseshoe": "horseshoe", "gnome": "gnome", "lantern": "lantern", "skate": "ball"}


def shelving(st):
    """Both runs: the units, the archive boxes (FORM 7, by decade), the tagged things and their tags. Seeded: the same
    every time."""
    rng = np.random.default_rng(31)
    taken = {}
    for kind, ui, ys, zc in M.LEFT_THINGS:
        taken.setdefault((ui, ys), []).append(zc)
    for i, (z0, z1) in enumerate(M.LEFT_Z):
        shelves = M.LEFT_SHELVES.get(i, M.SHELF_YS)
        unit(st, "L", z0, z1, shelves, seed=40 + i)
        for k, ys in enumerate(shelves):
            if i == 3 and ys == 222.0:                      # left-3's top: Ranger's landing, under the grille (one box at its far end)
                archive_box(st, "L", ys, z0 + 18.0, seed=900, label=True)
                continue
            if i == 2 and ys == 8.0:                        # the banjo's bay: the banjo alone in it
                continue
            busy = taken.get((i, ys), [])
            zz = z0 + 18.0
            while zz < z1 - 15.0:
                if not any(abs(zz - b) < 30.0 for b in busy) and rng.random() < 0.82:
                    archive_box(st, "L", ys, zz, seed=int(rng.integers(1e6)), label=True, turn=float(rng.uniform(-3, 3)))
                zz += 31.5 + rng.uniform(0.0, 2.0)
    for kind, ui, ys, zc in M.LEFT_THINGS:
        x = 24.0
        at = THINGS[kind](st, x, ys, zc)
        tag(st, "L", ys, zc, seed=zlib.crc32(kind.encode()) % 997, name=THING_NAME[kind] + "-tag", item=at)     # (a steady seed: never hash())
    for i, (z0, z1) in enumerate(M.RIGHT_Z):
        unit(st, "R", z0, z1, M.SHELF_YS, seed=60 + i)
        for ys in M.SHELF_YS:
            if i == 0 and ys == 92.0:                       # right-0, at the height of a hand: a traffic cone, tagged
                at = thing_cone(st, M.RIGHT_X[0] + 22.0, ys, z0 + 50.0)
                tag(st, "R", ys + 0.0, z0 + 34.0, seed=77, name="cone-tag", item=at)
                continue
            zz = z0 + 18.0
            while zz < z1 - 15.0:
                if rng.random() < 0.8:
                    archive_box(st, "R", ys, zz, seed=int(rng.integers(1e6)), label=True, turn=float(rng.uniform(-3, 3)))
                zz += 31.5 + rng.uniform(0.0, 2.0)


# ---------------------------------------------------------------- the banjo (tag No. 3117)
def banjo_frame():
    """The banjo's own axes: (the middle of its pot, the face's normal, up the neck, across)."""
    bx, bz = M.BANJO
    cx, cz = M.VIEW["cam"]
    lean = math.radians(13.0)
    h = nrm([cx - bx, 0.0, cz - bz])
    n = nrm([h[0] * math.cos(lean), math.sin(lean), h[2] * math.cos(lean)])
    up = nrm(np.array([0.0, 1.0, 0.0]) - n * n[1])
    across = nrm(np.cross(up, n))
    r = M.BANJO_POT / 2
    c = np.array([bx, M.LEFT_SHELVES[2][0] + 0.6, bz]) + up * r
    return c, n, up, across


def banjo(st, G="banjo"):
    """Grandpa Joe's banjo, damaged: standing on the lowest shelf of the tall bay, leaning back, its pot turned to face us.
    A nickel rim with its brackets, the head broken right through (a ragged hole: Jed's head went through it), the rim,
    the neck and the five strings whole; a maple neck, a dark fingerboard with its frets, the fifth string's peg partway
    up, the headstock and its four pegs; a brown tag on a string: No. 3117."""
    c, n, up, across = banjo_frame()
    r = M.BANJO_POT / 2
    depth = 6.5
    nickel = chrome("#c8c4b8", seed=311)
    # the rim, and the brackets round it
    ring(st, c - n * (depth / 2 - 0.5), n, r, depth, nickel, "banjo", grp=G, sides=30)
    ring(st, c + n * 0.4, n, r - 0.8, 0.8, col("#d8d4c8"), "banjo", grp=G, sides=30)
    for k in range(16):
        a = 2 * math.pi * k / 16
        p = c + (up * math.cos(a) + across * math.sin(a)) * (r + 0.3) - n * 1.2
        q = p - n * 3.4
        st.stick(tuple(p), tuple(q), 0.35, col("#d8d8d0"), "banjo", grp=G)
    # the open back, inside: dark wood, and the dowel stick running through the pot
    st.disc3(tuple(c - n * (depth - 0.6)), r - 0.6, tuple(-n), col("#3a2418"), name="banjo", grp=G)
    st.stick(tuple(c - n * 3.0 - up * (r - 1.0)), tuple(c - n * 3.0 + up * (r - 1.0)), 1.1, col("#8a5a32"), "banjo", grp=G)

    # the head: frosted white, broken through
    rng = np.random.default_rng(3117)
    harm = [(k, rng.uniform(0.15, 0.55), rng.uniform(0, 2 * math.pi)) for k in (3, 5, 7, 11)]
    hc_u, hc_v = 0.8, -1.4                                     # the hole's middle, a little off the head's middle

    def m_head(c_):
        u, v = c_.U, c_.V
        ang = np.arctan2(v - hc_v, u - hc_u)
        rad = 7.6 + sum(a * np.sin(k * ang + p) for k, a, p in harm) * 1.6
        d = np.hypot(u - hc_u, v - hc_v)
        keep = d > rad
        g = px_of(c_, 1.2)
        out = col("#ece8dc") * (0.92 + 0.06 * fbm(u / 2, v / 2, 312, 2))[..., None]
        torn = np.clip(1 - (d - rad) / 2.2, 0, 1)
        out = lay(out, "#b8b0a0", torn * 0.8)                   # the torn edge: grubby, curled back
        cracks = np.clip(1 - np.abs(np.sin(ang * 5.0 + 0.6)) * 12, 0, 1) * np.clip(1 - (d - rad) / 6.0, 0, 1) * (d > rad)
        out = lay(out, "#8a8478", cracks * 0.7)
        return out, None, keep
    st.disc3(tuple(c + n * 0.25), r - 0.8, tuple(n), m_head, name="banjo", grp=G, sides=36)
    # the tailpiece at the foot of the head, the bridge hanging on the strings over the hole
    tail = c - up * (r - 2.6) + n * 0.9
    frame_box(st, tail - up * 1.0, across, up, n, 3.4, 5.0, 0.8, col("#b8b4a8"), "banjo", grp=G)
    # the neck: maple, its heel on the rim at the top
    neck_len = M.BANJO_LEN - M.BANJO_POT - 16.0
    n0 = c + up * (r - 1.0)
    maple = laminate("#c48a4a", seed=313, grain_dir="z")
    frame_box(st, n0 - n * 1.6, across, up, n, 4.6, neck_len, 2.6, lambda c_: col("#b87a3e") * (0.9 + 0.12 * fbm(c_.X / 2, c_.Y / 9, 314, 2))[..., None],
              "banjo", grp=G)

    def m_board(c_):
        out = col("#3a2620") * (0.9 + 0.1 * fbm(c_.X / 2, c_.Y / 5, 315, 2))[..., None]
        s = (np.asarray(c_.X) - n0[0]) * up[0] + (np.asarray(c_.Y) - n0[1]) * up[1] + (np.asarray(c_.Z) - n0[2]) * up[2]
        g = px_of(c_, 1.0)
        fr = np.zeros_like(s)
        for k in range(1, 22):
            pos = neck_len * (1 - 2 ** (-k / 12.0)) * 1.7
            fr = np.maximum(fr, np.clip(1 - np.abs(s - pos) / (g * 0.6 + 0.12), 0, 1))
        out = lay(out, "#c8c8c0", fr * 0.8)
        dots = sum(np.clip(1 - np.hypot(s - neck_len * (1 - 2 ** (-k / 12.0)) * 1.7, 0) / 0.5, 0, 1) for k in (5, 7, 10))
        return lay(out, "#e8e2d0", np.clip(dots, 0, 1) * 0.0)
    frame_box(st, n0 + n * 1.0, across, up, n, 4.4, neck_len, 0.7, m_board, "banjo", grp=G)
    # the headstock and its four pegs
    h0 = n0 + up * neck_len
    frame_box(st, h0 - n * 1.2, across, up, n, 7.0, 15.0, 1.8, lambda c_: col("#3a2620") * np.ones((len(c_.X), 3), F32), "banjo", grp=G)
    for k, (sa, sh) in enumerate(((-1, 4.0), (-1, 10.0), (1, 4.0), (1, 10.0))):
        p = h0 + up * sh + across * sa * 3.5 - n * 0.6
        st.stick(tuple(p), tuple(p + across * sa * 3.6 - n * 1.6), 0.45, col("#e8e2d0"), "banjo", grp=G)
        st.ball(tuple(p + across * sa * 4.2 - n * 1.8), 1.0, col("#ece6d6"), name="banjo", grp=G, squash=(1.0, 1.0, 1.0), shadow=False)
    peg5 = n0 + up * (neck_len * 0.30) + across * 2.6
    st.stick(tuple(peg5), tuple(peg5 + across * 3.0 - n * 0.8), 0.4, col("#e8e2d0"), "banjo", grp=G)
    # the five strings: from the tailpiece over the hole, up the fingerboard to the nut (the fifth from its own peg)
    nut = h0 + n * 1.9
    for k in range(5):
        off = (k - 2) * 0.85
        a_ = tail + across * off * 0.8 + n * 0.6
        b_ = (nut + across * off) if k > 0 else (peg5 + n * 1.9 + across * 0.2)
        if k == 0:
            a_ = tail + across * (-1.8) + n * 0.6
        st.stick(tuple(a_), tuple(c + up * (r * 0.2) + across * off * 0.9 + n * 1.9), 0.11, col("#d8d8d4"), "banjo", grp=G, min_px=0.45)
        st.stick(tuple(c + up * (r * 0.2) + across * off * 0.9 + n * 1.9), tuple(b_), 0.11, col("#d8d8d4"), "banjo", grp=G, min_px=0.45)
    # the bridge, hanging on the strings over the hole
    bp = c + up * (r * 0.2) + n * 1.5
    frame_box(st, bp - up * 0.6, across, up, n, 5.6, 1.4, 0.6, col("#c8a070"), "banjo", grp=G)
    # its tag, on a string from the neck: No. 3117
    tp = n0 + up * (neck_len * 0.45)
    tag_c = tp + across * 1.0 + n * 3.2 - up * 8.0

    def m_tag(c_):
        g = px_of(c_, 1.4)
        out = col(TAG) * (0.94 + 0.08 * fbm(c_.X / 2, c_.Y / 2, 316, 2))[..., None]
        s = (np.asarray(c_.Y) - tag_c[1])
        writing = lines_aa(s, 2.0, 0.4, g) * band(s, -2.5, 2.5, g)
        return lay(out, "#3a2a20", writing * 0.75)
    tw, th = 5.0, 9.0
    st.poly([tuple(tag_c + across * (-tw / 2) + up * (th / 2)), tuple(tag_c + across * (tw / 2) + up * (th / 2)),
             tuple(tag_c + across * (tw / 2) - up * (th / 2)), tuple(tag_c + across * (-tw / 2) - up * (th / 2))], m_tag, "banjo-tag", grp=G)
    st.stick(tuple(tp + n * 1.4), tuple(tag_c + up * (th / 2 - 1.0)), 0.13, col("#e8dcc0"), "banjo-tag", grp=G, min_px=0.45)
    return c, n, up, across


# ---------------------------------------------------------------- the ceiling's fittings
def ceiling_things(st, eyes=False, G_vent="vent"):
    for i, t in enumerate(M.TROFFERS):
        st.poly([(t[0], H - 0.4, t[2]), (t[1], H - 0.4, t[2]), (t[1], H - 0.4, t[3]), (t[0], H - 0.4, t[3])], m_troffer(t, H, seed=i), f"troffer{i}")
    vx0, vx1, vz0, vz1 = M.VENT
    vent(st, vx0, vx1, vz0, vz1, H, name="vent", grp=G_vent, eyes=None, slats=5, along="z", seed=17, slat_h=2.2)
    if eyes:
        ranger_eyes(st, ((vx0 + vx1) / 2 + 4.0, H + 2.6, (vz0 + vz1) / 2 + 2.0), G=G_vent)
    sx, sz, sr = M.SPEAKER
    ceiling_speaker(st, sx, sz, sr, H, name="speaker")
    mx, mz, mr = M.SMOKE
    smoke_detector(st, mx, mz, mr, H, name="smoke")
    for (px, pz) in M.SPRINKLERS:
        sprinkler(st, px, pz, H, name="sprinkler")


def ranger_eyes(st, at, G="vent"):
    """Ranger's face pressed to the grille, looking down: a band of his face, the black mask across it and two eyes
    shining in it, just above the slats and turned to us (we see it through the gaps, from far to one side)."""
    cx_, cz_ = M.VIEW["cam"]
    eye_y = (M.VIEW["full"] - M.VIEW["horizon"]) * 175.0 / 160.0
    c = np.asarray(at, dtype=np.float64)
    look = nrm([cx_ - c[0], eye_y - c[1], cz_ - c[2]])
    right = nrm(np.cross([0.0, 1.0, 0.0], look))
    upv = np.cross(look, right)
    hw, hh = 19.0, 6.0

    def m(c_):
        u, v = c_.U - hw, c_.V - hh                        # from the face's middle: u across, v up
        face = col("#8c8c92") * (0.8 + 0.3 * fbm(c_.U / 1.5, c_.V / 1.5, 331, 2))[..., None]
        mask = np.clip((1 - np.abs(v / 4.2)) * 3, 0, 1) * np.clip((1.15 - np.abs(u / 15.0)) * 4, 0, 1)
        out = lay(face, "#101014", mask)
        e = np.zeros_like(out)
        for sx in (-7.0, 7.0):
            d = np.hypot(u - sx, v * 1.1)
            eye = np.clip((4.2 - d) * 1.2, 0, 1)
            glint = np.clip((1.4 - np.hypot(u - sx - 1.0, v * 1.1 - 1.0)) * 2.0, 0, 1)
            out = lay(out, "#e8d868", eye)
            out = lay(out, "#141410", np.clip((1.5 - d) * 2.0, 0, 1))
            e = e + col("#f0e488") * (eye * 1.5)[..., None] + col("#ffffff") * (glint * 1.6)[..., None]
        out = out * np.clip(1.25 - np.abs(u / hw) * 0.5, 0.3, 1.2)[..., None]
        return out, e
    P = lambda a, b: tuple(c + right * a + upv * b)
    st.poly([P(-hw, -hh), P(hw, -hh), P(hw, hh), P(-hw, hh)], m, "vent-eyes", grp=G)


# ---------------------------------------------------------------- near us: the cart, and boxes on the floor
def front(st, G="front"):
    """A gray steel utility cart parked by the right run (two shelves, a push handle, casters), an archive box and a
    clipboard on it, another box below; and two boxes stacked on the floor by the left run."""
    x0, x1, z0, z1 = M.CART
    m = painted_steel("#87908b", seed=321, amt=0.06, chips=0.3)
    for ys in (22.0, 84.0):
        st.box(x0, x1, ys, ys + 2.0, z0, z1, m, "cart", grp=G)
        for (a0, a1, b0, b1) in ((x0, x0 + 1.0, z0, z1), (x1 - 1.0, x1, z0, z1), (x0, x1, z0, z0 + 1.0), (x0, x1, z1 - 1.0, z1)):
            st.box(a0, a1, ys + 2.0, ys + 5.0, b0, b1, m, "cart", grp=G, shadow=False)
    for xp in (x0 + 1.5, x1 - 1.5):
        for zp in (z0 + 1.5, z1 - 1.5):
            st.box(xp - 1.4, xp + 1.4, 10.0, 86.0, zp - 1.4, zp + 1.4, m, "cart", grp=G, shadow=False)
            st.cyl((zp, 5.0), 5.0, xp - 1.2, xp + 1.2, col("#2a2a2c"), axis="x", name="cart", grp=G, shadow=False)
    st.stick((x0 + 2.0, 86.0, z1 - 1.0), (x0 + 2.0, 100.0, z1 + 4.0), 1.2, col("#9aa0a4"), "cart", grp=G)
    st.stick((x1 - 2.0, 86.0, z1 - 1.0), (x1 - 2.0, 100.0, z1 + 4.0), 1.2, col("#9aa0a4"), "cart", grp=G)
    st.stick((x0 + 2.0, 100.0, z1 + 4.0), (x1 - 2.0, 100.0, z1 + 4.0), 1.4, col("#2a2a2e"), "cart", grp=G)

    def m_box(c):
        return col(CARD) * (0.93 + 0.10 * fbm(c.X / 6, (c.Y + c.Z) / 6, 322, 2))[..., None]
    obox(st, ((x0 + x1) / 2, 89.0, z0 + 30.0), (38.0, 25.0, 31.0), 4.0, m_box, "cartbox", grp=G)
    obox(st, ((x0 + x1) / 2, 89.0 + 22.0, z0 + 30.0), (39.0, 3.0, 32.0), 4.0, m_box, "cartbox", grp=G, shadow=False)
    obox(st, ((x0 + x1) / 2, 24.0, z1 - 34.0), (38.0, 25.0, 31.0), -3.0, m_box, "cartbox", grp=G)

    def m_clip(c):
        g = px_of(c, 1.6)
        out = col("#9a7a52") * np.ones((len(c.X), 3), F32)
        paper = rect_uv(c.X, c.Z, x0 + 9.0, x0 + 30.0, z1 - 42.0, z1 - 14.0, g)
        out = lay(out, "#efeadb", paper)
        lines = lines_aa(c.Z, 1.8, 0.35, g) * paper
        return out * (1 - 0.2 * lines[..., None])
    st.box(x0 + 7.0, x0 + 32.0, 89.0, 89.6, z1 - 46.0, z1 - 12.0, m_clip, "clipboard", grp=G, shadow=False)
    st.box(x0 + 14.0, x0 + 25.0, 89.6, 90.8, z1 - 46.0, z1 - 42.0, chrome(), "clipboard", grp=G, shadow=False)
    for i, (a0, a1, b0, b1, y0, y1) in enumerate(M.FLOORBOXES):
        obox(st, ((a0 + a1) / 2, y0, (b0 + b1) / 2), (a1 - a0, y1 - y0 - 2.0, b1 - b0), 6.0 - 9.0 * i, m_box, "floorbox", grp=G)
        obox(st, ((a0 + a1) / 2, y1 - 3.0, (b0 + b1) / 2), (a1 - a0 + 1.0, 3.0, b1 - b0 + 1.0), 6.0 - 9.0 * i, m_box, "floorbox", grp=G, shadow=False)
    # a round kick stool on its casters, in the aisle near us (gray steel, two black rubber treads)
    kx, kz, kr, kh = M.KICKSTOOL
    m_k = painted_steel("#8a918c", seed=323, amt=0.06, chips=0.3)
    st.cyl((kx, kz), kr, 1.0, kh - 1.0, m_k, name="kickstool", grp=G, r1=kr * 0.66)
    st.cyl((kx, kz), kr * 0.68, kh - 1.0, kh, col("#2a2a2c"), name="kickstool", grp=G, shadow=False)
    st.ball((kx, kh, kz), kr * 0.66, col("#2c2c2e"), name="kickstool", grp=G, shadow=False, squash=(1.0, 0.10, 1.0))
    st.cyl((kx, kz), kr * 1.02, 0.0, 2.0, col("#2a2a2c"), name="kickstool", grp=G, shadow=False)
    st.cyl((kx, kz), kr * 0.86, 17.0, 20.0, col("#2a2a2c"), name="kickstool", grp=G, shadow=False)
    st.feet["kickstool"] = (kx - kr, kx + kr, kz - kr, kz + kr)
    st.feet["cart"] = (x0, x1, z0, z1)
    st.feet["floorbox"] = (M.FLOORBOXES[0][0], M.FLOORBOXES[0][1], M.FLOORBOXES[0][2], M.FLOORBOXES[0][3])

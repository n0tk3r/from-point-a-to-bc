"""The shell of the store and its openings, built in the room's own centimetres (nevada_store.py): the linoleum,
the boarded walls, the tin ceiling; the front window with the porch and the road outside it and the sun shade in
it; the back door with the hen yard, the fence and the desert beyond; the front door at the picture's edge.

Each function puts one group of things on the Stage (nevada_store_kit.Stage) with a paint that colours it in ITS
OWN measurements, so every line runs to its vanishing point by itself. What is outside the room (the porch, the
yard, the sky) is painted self-lit (`emi`) with the morning sun already in it, and flagged OUTSIDE so the room's
lamps leave it alone. All measurements come from nevada_store_model.py."""

import math

import numpy as np

from brush import F32, lerp
import nevada_store_model as M
from nevada_store_kit import (normals, col, mixc, vnoise, fbm, hashf, grad_of, lines_aa, band, rect, disc, lay, sstep, curve3, Ctx,
                              text_card, card_paint)

OUTSIDE = 4                      # the flag: beyond the walls (self-lit, the lamps leave it alone)
DAY = 1.7                        # how much brighter the sunlit world outside is than the room (what is seen through the openings)

# ---------------------------------------------------------------- the colours of things (before any light falls on them)
WALL = "#9cc4b4"                 # the boards: a mint green painted in 1974 and never since
WALL_D = "#86ad9e"
TRIM = "#e2d2a8"                 # painted trim, cream gone to yellow
CEIL = "#bcae8e"                 # pressed tin, painted cream long ago, gone to nicotine and dust
LINO_A, LINO_B = "#c8b896", "#a8826a"      # the linoleum's two tiles: a buff and a faded brick, worn toward each other
RED = "#b8342a"                  # the counter's edge, the register's keys
PAPER = "#f1ead6"
WOODY = "#a07040"


def sh(c):
    return c.X.shape


def patch(c, s=22.0, seed=0):
    return fbm((c.X + 0.37 * c.Y) / s, (c.Z + 0.61 * c.Y) / s, seed, 3)


def plain(color, amt=0.12, s=22.0, seed=0):
    """One paint, a little patchy as a brush leaves it."""
    k = col(color)

    def f(c):
        return k * (1 + amt * 2 * (patch(c, s, seed)[..., None] - 0.5))
    return f


def wood(color, seed=0, grain="x", amt=0.2, fine=2.6, long=38.0):
    """Wood with its grain running along one of the room's directions."""
    k = col(color)

    def f(c):
        g = {"x": c.X, "y": c.Y, "z": c.Z}[grain]
        o = c.X + c.Y + c.Z - g
        n = fbm(o / fine, g / long, seed, 3)
        return k * (1 + amt * 2 * (n[..., None] - 0.5))
    return f


def metal(color, seed=0, amt=0.1):
    """Painted or enamelled metal: smooth, a little mottled, chipped at random."""
    k = col(color)

    def f(c):
        n = fbm(c.X / 9, (c.Y + c.Z) / 9, seed, 2)
        chip = np.clip((fbm(c.X / 2.5, (c.Y + c.Z * 0.5) / 2.5, seed + 7, 2) - 0.78) * 9, 0, 1)
        out = k * (1 + amt * 2 * (n[..., None] - 0.5))
        return lay(out, "#5a4a40", chip * 0.8)
    return f


def rm(u, lo, hi, fp):
    """A soft-edged band lo..hi along u (fp: cm per ray)."""
    return np.clip((u - lo) / fp + 0.5, 0, 1) * np.clip((hi - u) / fp + 0.5, 0, 1)


def rect_uv(u, v, u0, u1, v0, v1, fp):
    return rm(u, u0, u1, fp) * rm(v, v0, v1, fp)


def disc_uv(u, v, cu, cv, r, fp):
    return np.clip((r - np.hypot(u - cu, v - cv)) / fp + 0.5, 0, 1)


# ---------------------------------------------------------------- the shell
def m_floor(c):
    """Linoleum tiles 30 cm square, two colours, laid in 1974: worn pale along the paths, lifted at a few corners,
    a doormat inside the front door."""
    X, Z = c.X, c.Z
    gX, gZ = grad_of(X) * c.ss, grad_of(Z) * c.ss
    T = 30.0
    ix, iz = np.floor(X / T), np.floor(Z / T)
    chk = ((ix + iz) % 2) == 0
    base = np.where(chk[..., None], col(LINO_A), col(LINO_B))
    tn = 0.9 + 0.2 * hashf(ix * 131 + iz, 3)                                  # every tile its own tone
    base = base * tn[..., None]
    mottle = fbm(X / 6, Z / 6, 21, 3)
    base = base * (0.9 + 0.2 * mottle[..., None])
    # the worn paths: from the door to the counter, and to the back door
    path = np.exp(-((X - 300 - (Z - 260) * 0.3) / 120.0) ** 2) * np.clip((Z - 150) / 120, 0, 1) * np.clip((460 - Z) / 120, 0, 1)
    path2 = np.exp(-((X - 420 - (Z - 180) * 0.9) / 70.0) ** 2) * np.clip((Z - 20) / 80, 0, 1) * np.clip((280 - Z) / 120, 0, 1)
    path3 = np.exp(-((Z - 230) / 60.0) ** 2) * np.clip((X - 150) / 100, 0, 1) * np.clip((500 - X) / 150, 0, 1)
    worn = np.clip(path * 0.7 + path2 * 0.6 + path3 * 0.5, 0, 1) * (0.5 + 0.5 * fbm(X / 40, Z / 40, 8, 2))
    base = lerp(base, lerp(base, col("#dcc9a4"), 0.6), (worn * 0.7)[..., None])
    # the seams between tiles, and a few tiles lifting at a corner
    seam = np.maximum(lines_aa(X, T, 0.9, gX), lines_aa(Z, T, 0.9, gZ))
    dark = np.clip(seam * 0.45, 0, 0.6)
    out = base * (1 - dark[..., None]) + col("#4a3826") * dark[..., None]
    lift = (hashf(ix * 77 + iz * 3, 9) > 0.93)
    cu, cv = X - ix * T, Z - iz * T
    curl = lift & (cu + cv > T * 1.5)
    out = lay(out, "#3a2c20", curl * 0.35)
    # the doormat: coir, a red border, inside the front door
    x0, x1, z0, z1 = M.MAT
    inm = band(X, x0, x1, gX) * band(Z, z0, z1, gZ)
    mat = col("#8c6a3c") * (0.85 + 0.3 * fbm(X / 1.5, Z / 1.5, 5, 2)[..., None])
    border = inm - band(X, x0 + 7, x1 - 7, gX) * band(Z, z0 + 7, z1 - 7, gZ)
    mat = lay(mat, "#8a2c24", np.clip(border, 0, 1) * 0.8)
    out = out * (1 - inm[..., None]) + mat * inm[..., None]
    return out


def boards_wall(c, along, Y, gA, gY, seed=0, dark_up=0.0):
    """Painted boards, tongue and groove, running along the wall; the paint patchy, a chalk line of dust on
    each groove, a skirting below."""
    bh = 11.0
    ib = np.floor(Y / bh)
    tone = 0.9 + 0.2 * hashf(ib + seed * 50, 4)
    base = lerp(col(WALL), col(WALL_D), (0.4 + 0.6 * fbm(along / 70, Y / 25, seed + 3, 3))[..., None]) * tone[..., None]
    base = base * (0.95 + 0.1 * fbm(along / 3, Y / 30, seed + 9, 2)[..., None])
    groove = lines_aa(Y, bh, 1.0, gY)
    out = base * (1 - 0.34 * groove[..., None])
    lit = lines_aa(Y, bh, 0.9, gY, phase=1.3) * 0.5
    out = out * (1 + 0.08 * lit[..., None])
    # old nail holes and a water stain or two
    stain = np.clip((fbm(along / 60, Y / 40, seed + 21, 3) - 0.62) * 4, 0, 1)
    out = lerp(out, out * col("#c8b088"), (stain * 0.45)[..., None])
    if dark_up:
        out = out * (1 - dark_up * np.clip((Y - 300) / 90, 0, 1))[..., None]
    sk = band(Y, -1, 14, gY)
    skirt = col("#7a5a3a") * (0.85 + 0.3 * fbm(along / 30, Y / 3, seed + 5, 2)[..., None])
    out = lerp(out, skirt, sk[..., None])
    line = band(Y, 12.4, 14.0, gY)
    return lerp(out, col("#a07a4a") * 1.3, (line * 0.5)[..., None])


def m_back(c):
    X, Y = c.X, c.Y
    gX, gY = grad_of(X) * c.ss, grad_of(Y) * c.ss
    out = boards_wall(c, X, Y, gX, gY, 1, dark_up=0.12)
    # behind the counter the boards are hidden by a sheet of pegboard, painted the same green, where the hubcaps hang
    pb = band(X, 140, 760, gX) * band(Y, 96, 350, gY)
    holes = (lines_aa(X, 5.0, 0.7, gX, fade=False) * lines_aa(Y, 5.0, 0.7, gY, fade=False)) * np.clip((5.0 / gX - 1.5) / 2, 0, 1)
    out = lerp(out, out * 0.96, pb[..., None])
    out = out * (1 - 0.35 * (holes * pb)[..., None])
    return out


def m_left(c):
    Z, Y = c.Z, c.Y
    gZ, gY = grad_of(Z) * c.ss, grad_of(Y) * c.ss
    return boards_wall(c, Z, Y, gZ, gY, 2, dark_up=0.1)


def m_right(c):
    Z, Y = c.Z, c.Y
    gZ, gY = grad_of(Z) * c.ss, grad_of(Y) * c.ss
    return boards_wall(c, Z, Y, gZ, gY, 3, dark_up=0.14)


def m_ceiling(c):
    """Pressed tin panels, 60 cm square, a rosette in each, painted cream and stained where the roof has leaked."""
    X, Z = c.X, c.Z
    gX, gZ = grad_of(X) * c.ss, grad_of(Z) * c.ss
    T = 60.0
    ix, iz = np.floor(X / T), np.floor(Z / T)
    u, v = X - ix * T - T / 2, Z - iz * T - T / 2
    base = col(CEIL) * (0.92 + 0.16 * hashf(ix * 17 + iz, 2))[..., None]
    base = base * (0.94 + 0.12 * fbm(X / 30, Z / 30, 41, 3)[..., None])
    r = np.hypot(u, v)
    g = np.maximum(gX, gZ)
    ring = np.clip(1 - np.abs(r - 11) / g * 0.8, 0, 1) * np.clip((T / gX - 6) / 6, 0, 1)
    ring2 = np.clip(1 - np.abs(r - 4) / g * 0.8, 0, 1) * np.clip((T / gX - 8) / 6, 0, 1)
    border = np.clip(1 - np.abs(np.maximum(np.abs(u), np.abs(v)) - 24) / g * 0.8, 0, 1) * np.clip((T / gX - 6) / 6, 0, 1)
    seam = np.maximum(lines_aa(X, T, 1.0, gX), lines_aa(Z, T, 1.0, gZ))
    out = base * (1 - 0.10 * (ring + ring2 + border)[..., None]) * (1 - 0.22 * seam[..., None])
    stain = np.clip((fbm(X / 120, Z / 140, 44, 3) - 0.56) * 3.5, 0, 1)
    out = lerp(out, out * col("#b89060"), (stain * 0.5)[..., None])
    rust = np.clip((fbm(X / 10, Z / 10, 45, 2) - 0.8) * 8, 0, 1) * stain
    return lay(out, "#7a4a2a", rust * 0.6)


SHELL = dict(floor=m_floor, back=m_back, left=m_left, right=m_right, ceiling=m_ceiling)


def holes():
    wz0, wz1, wy0, wy1 = M.WINDOW
    bx0, bx1, by0, by1 = M.BACKDOOR
    dz0, dz1, dy0, dy1 = M.FRONTDOOR
    return {
        "left": lambda X, Y, Z: ((Z > wz0) & (Z < wz1) & (Y > wy0) & (Y < wy1)) | ((Z > dz0) & (Z < dz1) & (Y > dy0) & (Y < dy1)),
        "back": lambda X, Y, Z: (X > bx0) & (X < bx1) & (Y > by0) & (Y < by1),
    }


def shell(st):
    st.shell(M.W, M.H, SHELL, holes=holes())


# ---------------------------------------------------------------- what is outside: the sky, the desert, the sun on things
SKY_TOP, SKY_LOW = "#3f7fc6", "#cfe3f1"
SAND, SAND_SHADE = "#e7c793", "#b58a5e"
MESA = "#b87a62"


def sky_at(u, v, seed=0):
    """The morning sky by height v (cm above the ground, far away) with a few small clouds. u runs along."""
    f = np.clip(v / 2600.0, 0, 1)
    out = lerp(col(SKY_LOW), col(SKY_TOP), (f ** 0.8)[..., None])
    cloud = fbm(u / 900 + seed, v / 260, 61, 4)
    puff = np.clip((cloud - 0.56) * 5, 0, 1) * np.clip((v - 500) / 400, 0, 1)
    out = lerp(out, col("#fbf4e6"), (puff * 0.9)[..., None])
    shade_ = np.clip((cloud - 0.56) * 5, 0, 1) * np.clip((fbm(u / 500, v / 120, 63, 2) - 0.5) * 2, 0, 1)
    return lerp(out, col("#c9b8c8"), (shade_ * 0.5 * puff)[..., None])


def far_view(u, v, seed=0, haze=0.0):
    """The far desert seen past the shack: the sky, a row of mesas, the ochre plain, all paler with the air."""
    out = sky_at(u, v, seed)
    top = 240 + 90 * fbm(u / 700, u * 0 + 1, 71 + seed, 3) + 40 * np.clip((np.sin(u / 380) + 0.5) * 2, 0, 1)
    mesa = sstep(top + 4, top - 4, v)
    mc = lerp(col(MESA), col("#d8a68a"), (0.5 + 0.5 * fbm(u / 60, v / 40, 72, 3))[..., None])
    mc = lerp(mc, col("#8c6a80"), np.clip((top - v) / 400, 0, 1)[..., None] * 0.5)
    out = lerp(out, mc, mesa[..., None])
    plain_ = sstep(62, 50, v)
    pc = lerp(col(SAND), col("#d9b27c"), (0.5 + 0.5 * fbm(u / 120, v / 30, 73, 3))[..., None])
    scrub = np.clip((fbm(u / 25, v / 9, 74, 3) - 0.66) * 6, 0, 1) * np.clip((50 - v) / 50, 0, 1)
    pc = lerp(pc, col("#7a8a5a"), (scrub * 0.7)[..., None])
    out = lerp(out, pc, plain_[..., None])
    return lerp(out, col("#cfd8e8"), haze)


def m_far(c):
    """The far plane at the horizon: the desert and the sky, self-lit."""
    out = far_view(c.U, c.V, 0, 0.18)
    return out * 0.0, out


# ---------------------------------------------------------------- the front window: the porch, the road, the sun shade
def window(st, G_shade="shade"):
    """The window in the left wall: two sashes side by side, the frame and sill, the glass with the porch and the road
    beyond; the folding sun shade standing in the far sash (G_shade: its own cut-out); the DISPLAY ONLY card propped
    on the sill in front of it (the backdrop's: it stays when the shade goes)."""
    z0, z1, y0, y1 = M.WINDOW
    tw = plain(TRIM, 0.1, 9, 2)
    depth = -M.WALL_T
    # the opening's reveals (the wall is 12 cm thick), the sill, the apron, the casing
    st.poly([(0, y0, z0), (depth, y0, z0), (depth, y1, z0), (0, y1, z0)], tw, "window")
    st.poly([(0, y0, z1), (depth, y0, z1), (depth, y1, z1), (0, y1, z1)], tw, "window")
    st.poly([(0, y1, z0), (depth, y1, z0), (depth, y1, z1), (0, y1, z1)], tw, "window")
    st.box(depth - 2, 18, y0 - 4, y0, z0 - 7, z1 + 7, tw, "window", shadow=False)                     # the sill: a display ledge
    st.box(0, 3, y0 - 14, y0 - 4, z0 - 4, z1 + 4, tw, "window", shadow=False)                         # the apron under it
    for zz in (z0 - 9, z1):
        st.box(0, 2.6, y0 - 4, y1 + 9, zz, zz + 9, tw, "window", shadow=False)
    st.box(0, 2.6, y1, y1 + 9, z0 - 9, z1 + 9, tw, "window", shadow=False)
    # the glass, and the world beyond painted into it
    zg = depth + 4
    st.poly([(zg, y0, z0), (zg, y0, z1), (zg, y1, z1), (zg, y1, z0)], m_glass, "window", flag=OUTSIDE)
    bar = plain("#d8c89c", 0.1, 5, 3)
    zm = M.MULLION
    st.box(zg - 1.8, zg + 2.2, y0, y1, zm - 3.0, zm + 3.0, bar, "window", shadow=False)                 # the post between the sashes
    for zz in (z0, z1 - 4.0):
        st.box(zg - 1.5, zg + 1.5, y0, y1, zz, zz + 4.0, bar, "window", shadow=False)
    st.box(zg - 1.5, zg + 1.5, y0, y0 + 4.5, z0, z1, bar, "window", shadow=False)
    st.box(zg - 1.5, zg + 1.5, y1 - 4.0, y1, z0, z1, bar, "window", shadow=False)
    # on the sill: a cactus in a coffee can at the near end, a dead fly, the card
    st.cyl((depth + 3, z1 - 18), 5.0, y0, y0 + 11, metal("#c84a30", 1), name="window", shadow=False)
    st.ball((depth + 3, y0 + 17, z1 - 18), 5.2, plain("#5a8a4c", 0.2, 3), "window", shadow=False, squash=(1.0, 1.25, 1.0))
    st.ball((depth + 2, y0 + 23, z1 - 16), 2.4, plain("#6a9a58", 0.2, 3), "window", shadow=False)
    displaycard(st)
    sunshade(st, G_shade)


DISPLAY_CARD = dict(w=68.0, h=32.0, at=132.0, turn=25.0, lean=8.0, x=3.0)  # the card on the sill: its size, where, how far turned toward the room


def card_quad(lift=0.0):
    """The DISPLAY ONLY card's four corners in the room (TL, TR, BR, BL): standing on the sill in front of the shade,
    turned toward the room and leaning back a little."""
    z0, z1, y0, y1 = M.WINDOW
    d = DISPLAY_CARD
    a = math.radians(d["turn"])                         # 0: flat to the wall; 90: square to it
    nx, nz = math.cos(a), math.sin(a)                    # its face's normal (into the room, and toward us)
    ux, uz = nz, -nx                                     # along the card, left to right as we see it
    bx, bz = d["x"], d["at"]                             # its middle, at the foot
    lean = math.radians(d["lean"])
    def P(su, sv):
        back = math.sin(lean) * sv
        return (bx + ux * su - nx * back + nx * lift, y0 + 0.4 + math.cos(lean) * sv, bz + uz * su - nz * back + nz * lift)
    hw = d["w"] / 2
    return [P(-hw, d["h"]), P(hw, d["h"]), P(hw, 0), P(-hw, 0)]


def displaycard(st):
    """A card of stiff white board on the sill, propped on a little easel: its words go on afterwards, crisp."""
    q = card_quad()
    def m_card(c):
        k = col("#f6efdc") * (0.94 + 0.08 * fbm(c.U / 4, c.V / 4, 17, 2))[..., None]
        edge = (c.U < 1.2) | (c.V < 1.2) | (c.U > DISPLAY_CARD["w"] - 1.2) | (c.V > DISPLAY_CARD["h"] - 1.2)
        return np.where(edge[..., None], col("#c8342a"), k)
    st.poly([q[3], q[2], q[1], q[0]], m_card, "displaycard", flag=1, shadow=True)
    foot = [(a + b) / 2 for a, b in zip(q[2], q[3])]
    st.stick((foot[0] - 3, foot[1], foot[2]), (foot[0] - 1, foot[1] + 14, foot[2] + 2), 0.5, col("#8a6a48"), "displaycard")


PORCH = dict(floor=0.0, edge=-220.0, roof=238.0, post_r=6.0, posts=(-40.0, -205.0), chair=(-96.0, 150.0), road=(-640.0, -1010.0))   # outside the window, X < 0


def m_glass(c):
    """What is seen through the window, painted into the glass: the porch boards and its two posts, the back of
    the rocking chair, the lot, the road with its yellow line, the far mesas and the sky; the sun from the right.
    (A view through a pane is drawn here by casting the pane's own rays on, pixel by pixel.)"""
    # each ray's direction in the room, carried on past the glass
    n = len(c.X)
    C = np.asarray(_CAM[0], dtype=np.float64)
    dX, dY, dZ = c.X - C[0], c.Y - C[1], c.Z - C[2]
    L = np.sqrt(dX * dX + dY * dY + dZ * dZ) + 1e-9
    dX, dY, dZ = dX / L, dY / L, dZ / L
    P = PORCH
    out = np.zeros((n, 3), dtype=F32)
    done = np.zeros(n, dtype=bool)
    depth = np.full(n, 1e9, dtype=F32)

    def put(m, color, t):
        nonlocal out, done, depth
        m = m & (t < depth)
        out[m] = color[m] if isinstance(color, np.ndarray) and color.ndim == 2 else col(color)
        done |= m
        depth[m] = t[m]

    # the sky and the far desert: a plane far to the left (X = -2600)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (-2600.0 - c.X) / dX
    ok = (dX < 0) & (t > 0)
    u, v = c.Z + t * dZ, c.Y + t * dY
    far = far_view(u * 1.0, np.maximum(v, 0) * 1.0, 0, 0.22)
    put(ok, far, np.where(ok, t, 1e9))
    # the lot: sand from the porch's edge out to the road, the road, more sand beyond
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (-42.0 - c.Y) / dY                                                    # the lot is 42 cm below the floor
    ok = (dY < 0) & (t > 0)
    gx, gz = c.X + t * dX, c.Z + t * dZ
    ok &= gx < P["edge"]
    sand = lerp(col(SAND), col("#d9ad78"), (0.5 + 0.5 * fbm(gx / 40, gz / 40, 81, 3))[..., None])
    sand = sand * (1 + 0.1 * (fbm(gx / 4, gz / 4, 82, 2) - 0.5))[..., None]
    far_t = np.clip((-gx - 300) / 2200, 0, 1)
    sand = lerp(sand, col("#dcd0c0"), (far_t * 0.5)[..., None])
    road = sstep(P["road"][0], P["road"][0] - 30, gx) * sstep(P["road"][1], P["road"][1] + 30, gx)
    asphalt = col("#5e5c64") * (0.9 + 0.2 * fbm(gx / 30, gz / 30, 83, 2))[..., None]
    mid = (P["road"][0] + P["road"][1]) / 2
    line = sstep(mid + 8, mid + 3, gx) * sstep(mid - 8, mid - 3, gx) * (np.abs(((gz / 300.0) % 1) - 0.5) < 0.3)
    asphalt = lay(asphalt, "#e8c050", line * 0.9)
    sand = lerp(sand, asphalt, road[..., None])
    stone = np.clip((fbm(gx / 7, gz / 7, 84, 2) - 0.7) * 8, 0, 1) * (1 - road) * (1 - far_t)
    sand = lay(sand, "#f4e4c4", stone * 0.6)
    shadow = sstep(P["edge"] - 120, P["edge"] - 40, gx) * 0.5 * (1 - road)                       # the porch roof's shadow on the sand
    sand = lerp(sand, sand * col("#8a7cb0"), shadow[..., None])
    put(ok, sand, np.where(ok, t, 1e9))
    # the porch floor: boards running out from the wall, in the roof's shade
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (P["floor"] - c.Y) / dY
    ok = (dY < 0) & (t > 0)
    px_, pz = c.X + t * dX, c.Z + t * dZ
    ok &= (px_ > P["edge"]) & (px_ <= 0)
    ib = np.floor(pz / 14.0)
    boards = col("#a08060") * (0.8 + 0.3 * hashf(ib, 6))[..., None] * (0.9 + 0.2 * fbm(px_ / 40, pz / 2, 85, 2))[..., None]
    gap = np.clip(1.4 - np.abs(pz / 14.0 - np.round(pz / 14.0)) * 14.0 / 1.2, 0, 1)
    boards = lay(boards, "#4a3020", gap * 0.6)
    boards = boards * col("#b8aed0") * 0.95                                          # in the roof's shade: cool
    lit = sstep(P["edge"] + 70, P["edge"] + 20, px_)                                   # the sun reaches the outer edge
    boards = lerp(boards, boards * col("#f8e0b0") * 1.9, (lit * 0.8)[..., None])
    put(ok, boards, np.where(ok, t, 1e9))
    # the porch roof's underside and its fascia (seen at the top of the window)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (P["roof"] - c.Y) / dY
    ok = (dY > 0) & (t > 0)
    rx, rz = c.X + t * dX, c.Z + t * dZ
    ok &= (rx > P["edge"] - 10) & (rx <= 0)
    roofc = col("#6a5a50") * (0.85 + 0.3 * fbm(rx / 30, rz / 6, 86, 2))[..., None]
    put(ok, roofc, np.where(ok, t, 1e9))
    # the posts and the rail
    def box_(ax, bx, ay, by, az, bz, color, seed=0, k0=0.85):
        tn = np.full(n, 0.0, dtype=F32)
        tf = np.full(n, 1e9, dtype=F32)
        for lo, hi, o, d in ((ax, bx, c.X, dX), (ay, by, c.Y, dY), (az, bz, c.Z, dZ)):
            with np.errstate(divide="ignore", invalid="ignore"):
                ta, tb = (lo - o) / d, (hi - o) / d
            tn = np.maximum(tn, np.minimum(ta, tb))
            tf = np.minimum(tf, np.maximum(ta, tb))
        ok = (tn < tf) & (tn > 0)
        k = col(color) * (k0 + 0.3 * fbm((c.Y + tn * dY) / 12, (c.Z + tn * dZ) / 12, seed, 2))[..., None]
        put(ok, k, np.where(ok, tn, 1e9))
    # the porch posts (in the porch roof's shade, their sunny side toward the lot), the rail between them
    for pz0 in P["posts"]:
        box_(P["edge"] - 7, P["edge"] + 7, -2, P["roof"], pz0 - 7, pz0 + 7, "#9a8a70", 87)
        box_(P["edge"] - 7.5, P["edge"] - 6.8, -2, P["roof"], pz0 - 7, pz0 + 7, "#f0dcb0", 88, 1.0)      # the edge the sun catches
    box_(P["edge"] - 4, P["edge"] + 4, 88, 96, P["posts"][1], P["posts"][0], "#8a7a62", 89)
    # the rocking chair, its back to us, in the porch's shade: a curved top rail, spindles with the lot between them,
    # its arms, and the rockers on the boards
    cx, cz = P["chair"]
    for i in range(6):
        zz = cz - 24 + i * 9.6
        top = 104 + 10 * math.cos((i - 2.5) / 2.5 * 1.2)
        box_(cx - 1.2, cx + 1.2, 48, top, zz - 1.1, zz + 1.1, "#5a3420", 90 + i, 0.8)
    for i in range(9):                                                               # the top rail, arched
        z_a = cz - 28 + i * 6.4
        y_a = 104 + 10 * math.cos((z_a - cz) / 30 * 1.2)
        box_(cx - 2.2, cx + 2.2, y_a - 3, y_a + 3, z_a - 3.4, z_a + 3.4, "#5a3420", 96, 0.8)
    box_(cx - 3, cx + 3, 44, 50, cz - 30, cz + 30, "#4a2a18", 97, 0.8)               # the seat's back rail
    for zz in (cz - 30, cz + 30):
        box_(cx - 40, cx + 4, 64, 68, zz - 2.5, zz + 2.5, "#4a2a18", 98, 0.8)           # the arms
        box_(cx - 48, cx + 10, 0, 5, zz - 2.2, zz + 2.2, "#3a2014", 99, 0.8)            # the rockers
        box_(cx - 2, cx + 2, 0, 66, zz - 2.2, zz + 2.2, "#4a2a18", 100, 0.8)
    # haze over all of it, a little, and the light on the glass itself
    out = lerp(out, col("#dfe6ec"), 0.05)
    # the pane: a faint reflection of the room's dimness in the lower panes, and dust in the corners
    dust = np.clip((fbm(c.Z / 12, c.Y / 12, 99, 2) - 0.6) * 3, 0, 1) * 0.15
    out = lerp(out, col("#cfc4a8"), dust[..., None])
    alb = np.zeros_like(out)
    return alb, out * DAY


_CAM = [None]


def set_camera(C):
    _CAM[0] = C


def sunshade(st, G="shade"):
    """The folding silver windshield shade, standing in the far sash on the sill, leaning back on the glass, its
    bright side toward the room (its mirror shows a little of the room: the warm dim of it, a glint off a hubcap);
    pleated like a fan; a dark strap round its middle. Its own cut-out (G)."""
    z0, z1, y0, y1 = M.WINDOW
    za, zb = z0 + 4.5, M.MULLION - 3.5
    H_ = 86.0
    lean = 5.5
    n = 12
    for i in range(n):
        u0, u1 = za + (zb - za) * i / n, za + (zb - za) * (i + 1) / n
        fold = 1.4 if i % 2 == 0 else -0.6                                           # the pleats zigzag
        fold2 = -0.6 if i % 2 == 0 else 1.4
        def m_panel(c, i=i, u0=u0, u1=u1):
            u = np.clip(c.U / (u1 - u0), 0, 1)
            v = np.clip(c.V / H_, 0, 1)
            lit = 1.0 if i % 2 == 0 else 0.78                                          # the pleats facing the window catch more
            k = lerp(col("#c8ccd4"), col("#eef0f2"), (0.5 + 0.5 * np.sin(u * math.pi))[..., None]) * lit
            room = lerp(col("#b8946a"), col("#6a7480"), np.clip(v * 1.4 - 0.2, 0, 1)[..., None])   # the room, dim, in the mirror
            k = lerp(k, room, 0.35)
            k = k * (0.94 + 0.1 * fbm(c.U / 3, c.V / 9, 31 + i, 2))[..., None]
            glint = np.clip(1 - np.abs(v - (0.62 - i * 0.02)) * 22, 0, 1) * ((i % 4) == 1)
            mirror = (0.30 + 0.14 * np.sin(u * math.pi)) * lit                             # the bright side: it gives back the lit room
            e = k * mirror[..., None] + col("#fff6e2") * (glint * 0.9)[..., None]
            crease = np.clip(1 - u * 12, 0, 1) + np.clip(1 - (1 - u) * 12, 0, 1)
            k = lerp(k, col("#5a6070") if i % 2 == 0 else col("#f8f8f6"), (crease * 0.35)[..., None])
            return k, e
        pts = [(-1.0 + fold, y0 + 0.5, u0), (-1.0 + fold2, y0 + 0.5, u1), (-1.0 - lean + fold2, y0 + 0.5 + H_, u1), (-1.0 - lean + fold, y0 + 0.5 + H_, u0)]
        st.poly(pts, m_panel, "windowshade", grp=G, flag=1, shadow=True)
    # the strap round its middle
    st.box(-4.6, 1.2, y0 + 50, y0 + 56, za - 0.5, zb + 0.5, plain("#26282e", 0.1), "windowshade", grp=G, shadow=False)
    st.box(-5.0, 1.6, y0 + 49, y0 + 57, (za + zb) / 2 - 4, (za + zb) / 2 + 4, plain("#c8342a", 0.1), "windowshade", grp=G, shadow=False)


# ---------------------------------------------------------------- the back door, and the hen yard beyond it
FENCE = dict(z=M.FENCE_Z, h=150.0, posts=(560.0, 680.0, 800.0))


def yard_ground(gx, gz, seed=0):
    """Packed dirt, in the morning sun, the shack's shadow across the first strides of it."""
    dirt = lerp(col("#c8955c"), col("#a87444"), (0.5 + 0.5 * fbm(gx / 50, gz / 50, 101 + seed, 3))[..., None])
    dirt = dirt * (1 + 0.22 * (fbm(gx / 3, gz / 3, 102, 2) - 0.5))[..., None]
    tracks = np.clip((fbm(gx / 8, gz / 30, 105, 2) - 0.62) * 4, 0, 1)                   # the hens' paths, scratched pale
    dirt = lay(dirt, "#e0c49a", tracks * 0.35)
    pebble = np.clip((fbm(gx / 5, gz / 5, 103, 2) - 0.72) * 8, 0, 1)
    dirt = lay(dirt, "#f0dcb8", pebble * 0.5)
    scratch = np.clip((fbm(gx / 12, gz / 4, 104, 2) - 0.68) * 6, 0, 1) * np.clip((-gz - 150) / 100, 0, 1)
    dirt = lay(dirt, "#9a7048", scratch * 0.4)
    shade_ = sstep(-150 + (gx - 600) * 0.25, -90 + (gx - 600) * 0.25, gz)              # the shack's shadow: cool, with the eave's slant
    dirt = lerp(dirt, dirt * col("#8a86c0") * 0.9, (shade_ * 0.7)[..., None])
    return dirt


def m_outside_back(c):
    """What is seen through the back door, painted into a plane just outside it: the step, the dirt, the water pan,
    the fence, the desert and the sky."""
    n = len(c.X)
    C = np.asarray(_CAM[0], dtype=np.float64)
    dX, dY, dZ = c.X - C[0], c.Y - C[1], c.Z - C[2]
    L = np.sqrt(dX * dX + dY * dY + dZ * dZ) + 1e-9
    dX, dY, dZ = dX / L, dY / L, dZ / L
    out = np.zeros((n, 3), dtype=F32)
    depth = np.full(n, 1e9, dtype=F32)

    def put(m, color, t):
        nonlocal out, depth
        m = m & (t < depth)
        out[m] = color[m] if isinstance(color, np.ndarray) and color.ndim == 2 else col(color)
        depth[m] = t[m]

    # the far desert and the sky: a plane far beyond the fence
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (-3200.0 - c.Z) / dZ
    ok = (dZ < 0) & (t > 0)
    u, v = c.X + t * dX, c.Y + t * dY
    put(ok, far_view(u + 900, np.maximum(v, 0), 3, 0.2), np.where(ok, t, 1e9))
    # the ground of the yard, a step down
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (M.STEP - c.Y) / dY
    ok = (dY < 0) & (t > 0)
    gx, gz = c.X + t * dX, c.Z + t * dZ
    ok &= (gz < 0)
    ground = yard_ground(gx, gz)
    farg = np.clip((-gz + FENCE["z"]) / 1200, 0, 1)                                  # past the fence the ground pales to the plain
    ground = lerp(ground, col("#e2cfa8"), (farg * 0.6)[..., None])
    put(ok, ground, np.where(ok, t, 1e9))
    # the water pan: a shallow galvanized pan on the dirt, near the left jamb
    px, pz, pr = 612.0, -118.0, 22.0
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (M.STEP + 5 - c.Y) / dY
    ok = (dY < 0) & (t > 0)
    qx, qz = c.X + t * dX, c.Z + t * dZ
    inpan = np.hypot(qx - px, qz - pz) < pr
    water = lerp(col("#5a7ea0"), col("#9ab8d0"), (0.5 + 0.5 * fbm(qx / 8, qz / 8, 111, 2))[..., None])
    rim = (np.hypot(qx - px, qz - pz) > pr - 2.0)
    water = np.where(rim[..., None], col("#9a9ca0"), water)
    put(ok & inpan, water, np.where(ok & inpan, t, 1e9))
    # its side: a short cylinder
    A = dX * dX + dZ * dZ
    B = 2 * ((c.X - px) * dX + (c.Z - pz) * dZ)
    Cq = (c.X - px) ** 2 + (c.Z - pz) ** 2 - pr * pr
    dsc = B * B - 4 * A * Cq
    okc = dsc > 0
    tc = (-B - np.sqrt(np.where(okc, dsc, 0))) / (2 * np.where(np.abs(A) < 1e-9, 1e-9, A))
    yc = c.Y + tc * dY
    okc &= (tc > 0) & (yc > M.STEP) & (yc < M.STEP + 5)
    ang = np.arctan2(c.Z + tc * dZ - pz, c.X + tc * dX - px)
    tub = col("#8a8e94") * (0.7 + 0.3 * np.clip(np.cos(ang - 2.3), 0, 1))[..., None]
    put(okc, tub, np.where(okc, tc, 1e9))
    # the fence: posts, a top rail, and the mesh as a tone laid over what is behind it
    fz, fh = FENCE["z"], FENCE["h"]
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (fz - c.Z) / dZ
    ok = (dZ < 0) & (t > 0)
    fx, fy = c.X + t * dX, c.Y + t * dY
    onf = ok & (fy > M.STEP) & (fy < M.STEP + fh)
    mesh_u, mesh_v = fx / 5.2, (fy - M.STEP) / 5.2
    dia = np.abs(((mesh_u + mesh_v) % 1) - 0.5) < 0.16
    dia |= np.abs(((mesh_u - mesh_v) % 1) - 0.5) < 0.16
    tone = np.where(dia, 0.62, 0.0).astype(F32) + 0.22
    behind = out.copy()
    fencec = lerp(behind, col("#6a6e76"), tone[..., None])
    out[onf] = fencec[onf]
    depth[onf] = t[onf]
    rail = ok & (fy > M.STEP + fh - 3) & (fy < M.STEP + fh + 1.5)
    out[rail] = col("#7a8088")
    for pxp in FENCE["posts"]:
        post = ok & (np.abs(fx - pxp) < 3.5) & (fy > M.STEP) & (fy < M.STEP + fh + 6)
        out[post] = col("#7a8088") * (0.8 + 0.4 * np.clip((pxp - fx) / 7 + 0.5, 0, 1))[..., None][post] if False else col("#7a8088")
    # a little dust in the air over the yard: the far things paler
    alb = np.zeros_like(out)
    return alb, out * DAY


def backdoor(st, G="backdoor"):
    """The back door: the opening in the back wall with its frame, the sill, the concrete step down into the yard,
    the screen door standing open against the wall inside, and the yard painted beyond."""
    x0, x1, y0, y1 = M.BACKDOOR
    tw = plain(TRIM, 0.1, 9, 5)
    depth = -12.0
    # what is beyond: a plane in the opening, just outside the wall, painted with the yard
    zy = depth - M.STEP_DEPTH - 1.0
    st.poly([(x0 - 60, M.STEP, zy), (x1 + 60, M.STEP, zy), (x1 + 60, y1 + 60, zy), (x0 - 60, y1 + 60, zy)], m_outside_back, "yard", flag=OUTSIDE)
    # the reveals and the sill
    st.poly([(x0, y0, 0), (x0, y0, depth), (x0, y1, depth), (x0, y1, 0)], tw, "backdoor")
    st.poly([(x1, y0, 0), (x1, y0, depth), (x1, y1, depth), (x1, y1, 0)], tw, "backdoor")
    st.poly([(x0, y1, 0), (x0, y1, depth), (x1, y1, depth), (x1, y1, 0)], tw, "backdoor")
    st.box(x0, x1, -2, 1.5, depth - 2, 4, wood("#8a6a44", 3, "x", 0.2), "backdoor", shadow=False)        # the sill
    st.box(x0 - 4, x1 + 4, M.STEP - 2, 0.0, depth - M.STEP_DEPTH, depth, m_step, "step", shadow=False, flag=OUTSIDE)   # the concrete step
    # the casing round the opening, inside
    for xx in (x0 - 9, x1):
        st.box(xx, xx + 9, y0, y1 + 9, 0, 2.2, tw, "backdoor", shadow=False)
    st.box(x0 - 9, x1 + 9, y1, y1 + 9, 0, 2.2, tw, "backdoor", shadow=False)
    # the screen door, standing open against the wall to the left of the opening (its hinges at the left jamb)
    screen_door(st, x0, y0, y1, G)


def m_step(c):
    """The concrete step: grey, chipped at its edge, in the shack's shadow (cool), its top lit by the sky."""
    k = col("#b4aca0") * (0.86 + 0.24 * fbm(c.X / 6, c.Z / 6, 141, 3))[..., None]
    if c.face == "top":
        k = k * col("#c8d0e8") * 1.05
    else:
        k = k * col("#a8a8c8") * 0.8
    chip = np.clip((fbm(c.X / 3, c.Y / 3, 142, 2) - 0.7) * 5, 0, 1)
    k = lay(k, "#8a8478", chip * 0.4)
    return k * 0.0, k * DAY * 0.8


def screen_door(st, x0, y0, y1, G):
    """A wooden screen door, hooked open flat against the wall: stiles and rails, the mesh, a spring, a push bar."""
    w = 86.0
    xa, xb = x0 - 9 - w, x0 - 9
    zf = 3.0
    fr = plain("#c9b48c", 0.12, 7, 8)
    for (ax, bx) in ((xa, xa + 8), (xb - 8, xb)):
        st.box(ax, bx, y0 + 1, y1, zf, zf + 3.2, fr, "screendoor", grp=G, shadow=False)
    for (ay, by) in ((y0 + 1, y0 + 12), (y1 - 9, y1), (y0 + 92, y0 + 100)):
        st.box(xa, xb, ay, by, zf, zf + 3.2, fr, "screendoor", grp=G, shadow=False)

    def m_mesh(c):
        u, v = c.U, c.V
        g = c.fp
        wire = np.maximum(lines_aa(u, 1.6, 0.5, g, fade=False), lines_aa(v, 1.6, 0.5, g, fade=False))
        rip = fbm(u / 10, v / 10, 121, 2)
        tone = lerp(col("#6a6e68"), col("#4a4e4a"), (wire * 0.6)[..., None]) * (0.9 + 0.2 * rip)[..., None]
        return tone
    for (ay, by) in ((y0 + 12, y0 + 92), (y0 + 100, y1 - 9)):
        st.poly([(xa + 8, ay, zf + 1.2), (xb - 8, ay, zf + 1.2), (xb - 8, by, zf + 1.2), (xa + 8, by, zf + 1.2)], m_mesh, "screendoor", grp=G, flag=1)
    st.box(xa + 10, xb - 10, y0 + 96, y0 + 99, zf + 3.2, zf + 5.5, metal("#b8b8b0", 2), "screendoor", grp=G, shadow=False)       # the push bar
    st.stick((xb - 4, y1 - 14, zf + 3), (x0 + 2, y1 - 20, 1.0), 0.9, col("#8a8a84"), "screendoor", grp=G)                        # the spring
    st.stick((xb - 1, y0 + 100, zf + 2), (x0 - 2, y0 + 100, 0.5), 1.1, col("#444444"), "screendoor", grp=G)                         # a hinge


# ---------------------------------------------------------------- the front door, at the picture's left edge (front plane)
def frontdoor(st, G="back"):
    """The front door in the left wall, nearest us, shut behind the family: its frame, a panelled leaf with a glass
    pane in its top half (the porch's light in it, and a hanging card that says CLOSED on our side: the OPEN side
    faces the lot), the knob, a kick plate, and the bell on its coiled spring over the top."""
    z0, z1, y0, y1 = M.FRONTDOOR
    tw = plain("#dcc8a0", 0.12, 8, 11)
    depth = -M.WALL_T
    for zz in (z0 - 10, z1):
        st.box(0, 3.5, y0, y1 + 10, zz, zz + 10, tw, "door", grp=G, shadow=False)
    st.box(0, 3.5, y1, y1 + 10, z0 - 10, z1 + 10, tw, "door", grp=G, shadow=False)
    st.poly([(0, y0, z0), (depth, y0, z0), (depth, y1, z0), (0, y1, z0)], tw, "door", grp=G)
    st.poly([(0, y1, z0), (depth, y1, z0), (depth, y1, z1), (0, y1, z1)], tw, "door", grp=G)
    st.box(depth, 2.0, -1.0, 1.5, z0, z1, wood("#8a6a44", 12, "z", 0.2), "door", grp=G, shadow=False)          # the threshold
    xl = -4.0                                                                                                 # the leaf's face
    lf = wood("#b0885a", 13, "y", 0.22, 2.4, 50.0)
    def m_leaf(c):
        k = lf(c)
        u, v = c.Z - z0, c.Y - y0
        w, h = z1 - z0, y1 - y0
        panel = rect_uv(u, v, 10, w - 10, 14, 92, c.fp) - rect_uv(u, v, 12, w - 12, 16, 90, c.fp)
        k = lay(k, "#6a4a2a", np.clip(panel, 0, 1) * 0.7)
        kick = rect_uv(u, v, 2, w - 2, 1, 12, c.fp)
        k = lay(k, "#c8b070", kick * 0.85)
        worn = np.clip((fbm(u / 6, v / 10, 14, 3) - 0.55) * 3, 0, 1) * np.clip((u - w * 0.6) / (w * 0.4), 0, 1) * np.clip((130 - v) / 60, 0, 1)
        return lerp(k, col("#d8b890"), (worn * 0.5)[..., None])
    st.box(xl - 4, xl, y0 + 0.5, y1 - 0.5, z0 + 0.5, z1 - 0.5, m_leaf, "door", grp=G)
    # the pane, the porch's light in it
    st.poly([(xl + 0.3, y0 + 104, z0 + 12), (xl + 0.3, y0 + 104, z1 - 12), (xl + 0.3, y1 - 14, z1 - 12), (xl + 0.3, y1 - 14, z0 + 12)], m_pane, "door", grp=G, flag=OUTSIDE)
    for (a0, a1, b0, b1) in ((z0 + 12, z1 - 12, y0 + 102, y0 + 105), (z0 + 12, z1 - 12, y1 - 15, y1 - 12), (z0 + 10, z0 + 13, y0 + 102, y1 - 12), (z1 - 13, z1 - 10, y0 + 102, y1 - 12)):
        st.box(xl, xl + 1.4, b0, b1, a0, a1, plain("#9a7048", 0.1), "door", grp=G, shadow=False)
    # the card hanging in the pane on a string: CLOSED, on our side
    cz, cy = (z0 + z1) / 2, y0 + 150
    m = _CLOSED["mask"]
    def m_card(c):
        tx = np.clip(c.Z - (cz - 13), 0, 26) / 26 * (m.shape[1] - 1.001)
        ty = np.clip((cy + 4.5 - c.Y), 0, 9) / 9 * (m.shape[0] - 1.001)
        ink = m[ty.astype(np.intp), tx.astype(np.intp)]
        return lerp(col("#f2ead2"), col("#b8302a"), ink[..., None])
    st.box(xl + 1.6, xl + 2.2, cy - 4.5, cy + 4.5, cz - 13, cz + 13, m_card, "door", grp=G, shadow=False)
    st.stick((xl + 1.9, cy + 4.5, cz - 8), (xl + 1.9, cy + 12, cz), 0.2, col("#e8e0c8"), "door", grp=G)
    st.stick((xl + 1.9, cy + 4.5, cz + 8), (xl + 1.9, cy + 12, cz), 0.2, col("#e8e0c8"), "door", grp=G)
    # the knob (on the latch side, nearer us), its plate
    st.box(xl, xl + 0.8, y0 + 86, y0 + 106, z1 - 16, z1 - 10, m_brass_flat, "door", grp=G, shadow=False)
    st.ball((xl + 3.5, y0 + 96, z1 - 13), 3.0, m_brass, "door", grp=G, shadow=False)
    # the bell, on a coiled spring bracket over the leaf's top corner
    bz = z1 - 18
    st.stick((0.5, y1 + 6, bz), (9, y1 + 2, bz - 2), 0.6, col("#3a3a3a"), "bell", grp=G)
    for k in range(5):
        st.ball((9 + k * 0.6, y1 + 1 - k * 1.2, bz - 2), 1.0, col("#5a5a5a"), "bell", grp=G, shadow=False)
    st.cyl((12, bz - 2), 5.5, y1 - 12, y1 - 5, m_brass_c, r1=2.2, name="bell", grp=G, shadow=False, hollow=False)
    st.ball((12, y1 - 13, bz - 2), 1.2, m_brass, "bell", grp=G, shadow=False)


_CLOSED = {"mask": None}


def _closed_mask():
    from nevada_store_kit import pen_mask
    _CLOSED["mask"] = pen_mask(["CLOSED"], 26, 9, 5.0, res=12, seed=9)


_closed_mask()


def m_brass_flat(c):
    return col("#c8a048") * (0.8 + 0.3 * fbm(c.Y / 3, c.Z / 3, 15, 2))[..., None]


def m_brass_c(c):
    n = normals(c)
    k = col("#c8a048")[None, :] * (0.6 + 0.6 * np.clip(n[:, 1] * 0.4 + n[:, 0] * 0.6 + 0.3, 0, 1))[:, None]
    return k, col("#fff0c0")[None, :] * (np.clip(n[:, 0] - 0.6, 0, 1) * 1.2)[:, None]


def m_brass(c):
    n = normals(c)
    k = col("#c8a048")[None, :] * (0.7 + 0.5 * np.clip(n[:, 1] * 0.5 + n[:, 0] * 0.6 + 0.3, 0, 1))[:, None]
    return k, col("#fff0c0")[None, :] * (np.clip(n[:, 0] * 0.8 + n[:, 1] * 0.4 - 0.7, 0, 1) * 1.5)[:, None]


def m_pane(c):
    """The porch's light in the door's pane: a bright pale blur of sand and sky, the posts' shadows."""
    u, v = c.U, c.V
    k = lerp(col("#ead8b0"), col("#cfe0ee"), np.clip((v - 20) / 50, 0, 1)[..., None])
    k = k * (0.94 + 0.12 * fbm(u / 10, v / 10, 131, 2))[..., None]
    k = lay(k, "#9a8a70", np.clip(1 - np.abs(u - 22) / 4, 0, 1) * 0.5)
    return k * 0.0, k * DAY

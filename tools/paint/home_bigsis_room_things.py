"""Everything in The Retreat, built in the room's own centimetres (home_bigsis_room.py puts it together).

Each function puts one group of things on the Stage (home_bigsis_room_kit.Stage). All the measurements come from
the model (home_bigsis_room_model.py), so the skeleton, the picture and layout.json agree."""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, lerp, sample
import home_bigsis_room_model as M
from home_bigsis_room_kit import (col, mixc, vnoise, fbm, hashf, grad_of, lines_aa, band, rect, disc, lay, sstep, curve3, Ctx)

K, R = float(M.KNEE), float(M.RISE)
Q = math.sqrt(1 + R * R)                    # centimetres of slope for each centimetre of Z
RAFT_W, RAFT_D = 4.5, 16.0                  # a rafter: half its width, and how far it stands down from the boards
SKY_D = 13.0                                # how deep the skylights' linings are (measured upright)

# ---------------------------------------------------------------- the colors of things (before any light falls on them)
WALL = "#dfb2ac"            # the plaster she painted: a pale blush
TRIM = "#efe6d6"            # white paint, a little warm
ROOFB = "#e2d3c0"           # the roof's boards, whitewashed
RAFT = "#c8a47e"            # the rafters: pale wood, limed
FLOOR_A, FLOOR_B, FLOOR_C = "#b98452", "#cf9d66", "#a97648"
CREAM = "#f1e8d6"
LINEN = "#f4eee2"
ROSE = "#d49a94"
SAGE = "#8fae98"
INDIGO = "#39416e"
PINE = "#d8b587"


def roof(Z):
    return K + R * Z


def sh(c):
    return c.X.shape


def patch(c, s=22.0, seed=0):
    return fbm((c.X + 0.37 * c.Y) / s, (c.Z + 0.61 * c.Y) / s, seed, 3)


def plain(color, amt=0.10, s=22.0, seed=0):
    """One paint, a little patchy as a brush leaves it."""
    k = col(color)

    def f(c):
        return k * (1 + amt * 2 * (patch(c, s, seed)[..., None] - 0.5))
    return f


def wood(color, seed=0, grain="x", amt=0.18, fine=2.4, long=36.0):
    """Wood with its grain running along one of the room's directions."""
    k = col(color)

    def f(c):
        g = {"x": c.X, "y": c.Y, "z": c.Z}[grain]
        o = c.X + c.Y + c.Z - g
        n = fbm(o / fine, g / long, seed, 3)
        return k * (1 + amt * 2 * (n[..., None] - 0.5))
    return f


def full(c, color):
    return np.zeros(sh(c) + (3,), dtype=F32) + col(color)


# ---------------------------------------------------------------- the shell
def m_floor(c):
    X, Z = c.X, c.Z
    gX, gZ = grad_of(X) * c.ss, grad_of(Z) * c.ss
    bw = 12.0
    ib = np.floor(X / bw)
    Lb = 150 + 150 * hashf(ib, 5)
    zj = (Z + 400 * hashf(ib, 9)) / Lb
    seg = np.floor(zj)
    tn = hashf(ib * 37 + seg, 11)
    base = lerp(col(FLOOR_A), col(FLOOR_B), tn[..., None])
    base = lerp(base, col(FLOOR_C), ((hashf(ib * 13 + seg, 4) > 0.8) * 0.7)[..., None])
    gr = fbm(X / 2.2, Z / 60.0, 31, 3)
    base = base * (0.86 + 0.28 * gr[..., None])
    wear = fbm(X / 90, Z / 120, 8, 3)                                        # where bare feet have polished it
    w = np.clip((wear - 0.5) * 2.0, 0, 1)
    base = lerp(base, base * col("#f4e6d2") * 1.08, (w * 0.35)[..., None])
    seam = lines_aa(X, bw, 1.0, gX)
    dz = np.abs(zj - np.round(zj)) * Lb
    butt = np.clip(1.0 - dz / gZ, 0, 1) * np.clip((Lb / gZ - 2) / 3, 0, 1)
    nail = np.clip(1.2 - np.hypot((np.abs(dz) - 2.5) / gZ, (np.abs(X - (ib + 0.5) * bw) - 3.2) / gX), 0, 1) * np.clip((bw / gX - 5) / 4, 0, 1)
    dark = np.clip(seam * 0.46 + butt * 0.44 + nail * 0.3, 0, 0.7)
    out = base * (1 - dark[..., None]) + col("#3a2216") * dark[..., None]
    f = X / bw - np.floor(X / bw)
    edge = np.clip(1 - np.abs(f * bw - 1.6) / gX, 0, 1) * np.clip((bw / gX - 4) / 4, 0, 1)
    out = out * (1 + 0.09 * edge[..., None])

    # ---- the round rug: braided, cream, with rings of rose and ochre and a flower in the middle
    rx, rz, rr = M.RUG
    dx, dzr = X - rx, Z - rz
    d = np.hypot(dx, dzr)
    ang = np.arctan2(dzr, dx)
    g = np.maximum(gX, gZ)
    wob = (fbm(ang * 2.5, d / 40, 77, 2) - 0.5) * 2.2                         # it is hand-made: not quite round
    de = d + wob
    inr = np.clip((rr - de) / g + 0.5, 0, 1)
    cream, rose, ochre, plum = col("#eadcc4"), col("#c2787a"), col("#d2a258"), col("#75506e")
    rug = np.empty(X.shape + (3,), dtype=F32)
    rug[...] = rose
    for (a, b, k_) in ((rr - 8.5, rr - 2.5, plum), (rr - 13.5, rr - 10.5, cream), (rr - 33, rr - 30, ochre), (30.5, 33, cream)):
        m = band(de, a, b, g)
        rug = rug * (1 - m[..., None]) + k_ * m[..., None]
    lobes = (rr - 22) + 5.5 * np.cos(ang * 16)                                # a scalloped garland near the edge
    m = np.clip(1.8 - np.abs(d - lobes) / g, 0, 1)
    rug = rug * (1 - m[..., None]) + cream * m[..., None]
    dots = np.clip((2.2 - np.hypot(d - (rr - 22), (np.mod(ang * 16 / (2 * math.pi) + 0.5, 1.0) - 0.5) * 2 * math.pi * (rr - 22) / 16)) / g + 0.5, 0, 1)
    rug = rug * (1 - dots[..., None]) + ochre * dots[..., None]
    pet = 19 + 9.5 * np.cos(ang * 8)                                          # eight petals in the middle
    m = np.clip((pet - d) / g + 0.5, 0, 1)
    rug = rug * (1 - m[..., None]) + cream * m[..., None]
    pet2 = 12 + 5 * np.cos(ang * 8 + math.pi)
    m = np.clip((pet2 - d) / g + 0.5, 0, 1)
    rug = rug * (1 - m[..., None]) + plum * m[..., None]
    m = np.clip((5.0 - d) / g + 0.5, 0, 1)
    rug = rug * (1 - m[..., None]) + ochre * m[..., None]
    ray = np.clip(1.3 - np.abs(np.mod(ang * 8 / (2 * math.pi), 1.0) - 0.5) * 2 * math.pi * d / 8 / g, 0, 1) * band(d, 36, 54, g)   # a spoke between the petals
    rug = rug * (1 - 0.8 * ray[..., None]) + cream * 0.8 * ray[..., None]
    braid = lines_aa(de, 3.1, 1.0, g) * 0.13 + (fbm(ang * 40, de / 2.5, 5, 2) - 0.5) * 0.14
    rug = rug * (1 - braid[..., None])
    rug = rug * (0.94 + 0.12 * fbm(X / 30, Z / 30, 19, 2)[..., None])
    rim = np.clip((de - (rr - 2.2)) / 2.2, 0, 1) * inr
    rug = rug * (1 - 0.25 * rim[..., None])
    shadow = np.clip(1 - (de - rr) / 4.0, 0, 1) * (1 - inr)                  # it lies a finger thick on the boards
    out = out * (1 - 0.34 * shadow[..., None])
    out = out * (1 - inr[..., None]) + rug * inr[..., None]
    return out


def skirt(out, along, Y, gY, seed=5):
    sk = band(Y, -5, 10.5, gY)
    wd = col(TRIM) * (0.9 + 0.2 * fbm(along / 40, Y / 3, seed, 2)[..., None])
    out = lerp(out, wd, sk[..., None])
    line = band(Y, 9.2, 11.0, gY)
    return lerp(out, col(TRIM) * 0.62, (line * 0.6)[..., None])


def plaster(a, b, seed):
    n = fbm(a / 55, b / 55, seed, 4)
    base = col(WALL) * (0.91 + 0.18 * n[..., None])
    return base * (0.975 + 0.05 * fbm(a / 7, b / 26, seed + 6, 2)[..., None])


def m_far(c):
    X, Y = c.X, c.Y
    gY = grad_of(Y) * c.ss
    base = plaster(X, Y, 3)
    base = base * (1 - 0.10 * np.clip((Y - 112) / 22, 0, 1)[..., None])       # dimmer up under the ledge
    return skirt(base, X, Y, gY)


def m_end(c):
    Z, Y = c.Z, c.Y
    gY, gZ = grad_of(Y) * c.ss, grad_of(Z) * c.ss
    base = plaster(Z, Y, 14 if c.face == "endL" else 21)
    up = np.clip((Y - (roof(Z) - 30)) / 30, 0, 1)                             # a little grey gathers under the roof line
    base = base * (1 - 0.10 * up[..., None])
    out = skirt(base, Z, Y, gY, 6)
    if c.face == "endL":                                                      # the round window's painted casing
        wz, wy, wr = M.ROUND_WINDOW
        d = np.hypot(Z - wz, Y - wy)
        g = np.maximum(gY, gZ)
        ring = band(d, wr - 0.5, wr + 8.5, g)
        out = lerp(out, col(TRIM) * (0.93 + 0.1 * fbm(Z / 9, Y / 9, 4, 2)[..., None]), ring[..., None])
        line = band(d, wr + 7.2, wr + 9.2, g)
        out = out * (1 - 0.3 * line[..., None])
    return out


def m_slope(c):
    X, S = c.X, c.S
    gX, gS = grad_of(X) * c.ss, grad_of(S) * c.ss
    bw = 14.0
    ib = np.floor(S / bw)
    Lb = 225.0                                                                # the boards' ends meet on a rafter
    xj = (X - 5 - 75 * np.floor(hashf(ib, 2) * 3)) / Lb
    seg = np.floor(xj)
    base = col(ROOFB) * (0.88 + 0.18 * hashf(ib * 17 + seg, 5)[..., None])
    base = base * (0.92 + 0.16 * fbm(X / 70, S / 3.5, 12, 3)[..., None])
    thin = fbm(X / 30, S / 9, 41, 3)                                          # where the whitewash is thin, the wood shows warm
    base = lerp(base, col("#d9b790"), (np.clip((thin - 0.60) * 4, 0, 1) * 0.5)[..., None])
    knot = fbm(X / 6, S / 6, 47, 2)
    base = base * (1 - 0.18 * np.clip((knot - 0.80) * 8, 0, 1)[..., None])
    f = S / bw
    d = np.abs(f - np.round(f)) * bw
    seam = np.clip((0.3 - d) / gS + 0.6, 0, 1) * np.clip((bw / gS - 1.6) / 2.4, 0.15, 1)
    dx = np.abs(xj - np.round(xj)) * Lb
    butt = np.clip((0.3 - dx) / gX + 0.6, 0, 1) * np.clip((Lb / gX - 2) / 3, 0, 1)
    dark = np.clip(seam * 0.5 + butt * 0.4, 0, 0.7)
    out = base * (1 - dark[..., None]) + col("#5a4638") * dark[..., None]
    lit = np.clip((0.9 - np.abs(d - 1.0)) / gS, 0, 1) * np.clip((bw / gS - 5) / 5, 0, 1)   # the lower edge of each board catches a little light
    return out * (1 + 0.07 * lit[..., None])


def m_rafter(seed):
    def f(c):
        S = c.Z * Q
        across = c.X if c.face == "bottom" else c.Yp
        n = fbm(S / 70.0 + seed * 3.1, across / 1.3 + seed * 3.7, 17, 3)
        k = col(RAFT)[None, :] * ((0.86 + 0.2 * hashf(seed, 3)) * (0.78 + 0.44 * n))[..., None]
        streak = fbm(S / 140.0 + seed, across / 0.5 + seed * 1.3, 29, 2)
        k = k * (1 - 0.22 * np.clip((streak - 0.62) * 4, 0, 1)[..., None])
        ks = S - (50 + 380 * hashf(seed, 8))
        knot = np.clip(1 - np.hypot(ks / 5.0, (across - (c.box[0] + 4 if c.face == "bottom" else c.box[2] + 7)) / 2.2), 0, 1)
        k = k * (1 - 0.4 * knot[..., None])
        if c.face in ("left", "right"):
            low = np.clip((c.box[2] + 1.6 - c.Yp) / 1.6, 0, 1)                # the worn lower arris catches the light
            k = k * (1 + 0.35 * low[..., None])
        return k
    return f


def sky_in(c, i):
    """The night in a skylight's glass: u across the pane, v up the slope, both 0..1; and the sash and its bar.
    A painted sky: deep overhead, paler low down, thin cloud drifting across with the moon in it."""
    x0, x1, z0, z1 = M.SKYLIGHTS[i]
    u, v = (c.X - x0) / (x1 - x0), (c.Z - z0) / (z1 - z0)
    wcm, hcm = (x1 - x0), (z1 - z0) * Q
    U, V = u * wcm, v * hcm
    fp = c.fp
    Ug = U + i * 300.0                                                        # the two panes look out on one sky
    sky = lerp(col("#2f438a"), col("#0d1546"), np.clip(v * 1.15, 0, 1)[..., None])       # deeper toward the top of the sky
    sky = sky + col("#5674b4") * (np.exp(-V / 40.0) * 0.34)[..., None]
    mx, my, mr = wcm * 0.62 + 300.0, hcm * 0.50, 11.5                         # where the moon is (in the right-hand pane)
    dm = np.hypot(Ug - mx, V - my)
    near_moon = np.exp(-dm / 70.0)
    cloud = fbm(Ug / 46 + V / 90, V / 15 + Ug / 160, 51, 4)                   # long thin bars of cloud, a little aslant
    cl = np.clip((cloud - 0.50) * 3.2, 0, 1)
    edge = np.clip((cloud - 0.56) * 6.0, 0, 1) * np.clip((0.72 - cloud) * 6.0, 0, 1)
    sky = sky * (1 - 0.30 * cl[..., None]) + col("#7f93cc") * (cl * (0.20 + 0.50 * near_moon))[..., None]
    sky = sky + col("#c9d6f4") * (edge * near_moon * 0.30)[..., None]         # the moon silvers their edges
    cu, cv = np.floor(Ug / 6.0), np.floor(V / 6.0)
    h1 = hashf(cu * 31 + cv * 57, 3)
    sx, sy = (cu + 0.25 + 0.5 * hashf(cu * 13 + cv * 7, 5)) * 6.0, (cv + 0.25 + 0.5 * hashf(cu * 5 + cv * 11, 6)) * 6.0
    star = (h1 > 0.80) * np.clip((0.55 + 0.5 * (h1 > 0.95) + fp * 0.55 - np.hypot(Ug - sx, V - sy)) / fp, 0, 1)
    sky = sky + col("#e6ecff") * (star * (0.50 + 0.50 * hashf(cu * 3 + cv, 9)) * (1 - 0.85 * cl) * (1 - 0.7 * np.exp(-dm / 26.0)))[..., None]
    if i == 1:                                                                # the moon, not quite full
        sky = sky + col("#a9bfee") * (np.exp(-dm / 16.0) * 0.55)[..., None]
        moon = np.clip((mr - dm) / fp + 0.5, 0, 1)
        lit = np.clip((mr - np.hypot(Ug - mx - 3.0, V - my - 0.9)) / (fp * 1.6) + 0.5, 0, 1)      # a sliver of it is in shadow
        moon = moon * (0.16 + 0.84 * lit)
        mare = fbm(Ug / 3.4, V / 3.4, 5, 2)
        sky = sky * (1 - moon[..., None]) + col("#fbf6e0") * (1.18 - 0.20 * mare)[..., None] * moon[..., None]
    else:                                                                     # in the other, the top of the tree by the house
        black = np.zeros(U.shape, dtype=bool)
        twigs = [((-4, 2), (30, 30), 1.6), ((30, 30), (58, 44), 1.1), ((30, 30), (40, 62), 1.0), ((12, 15), (20, 48), 1.0),
                 ((58, 44), (74, 46), 0.8), ((40, 62), (52, 82), 0.7), ((20, 48), (12, 72), 0.8), ((46, 38), (60, 66), 0.7)]
        for (a_, b_, wd) in twigs:
            ax, ay = a_
            bx, by = b_
            t_ = np.clip(((U - ax) * (bx - ax) + (V - ay) * (by - ay)) / ((bx - ax) ** 2 + (by - ay) ** 2), 0, 1)
            d_ = np.hypot(U - (ax + t_ * (bx - ax)), V - (ay + t_ * (by - ay)))
            black |= d_ < wd * (1.0 - 0.45 * t_) + fp * 0.3
            leaves = fbm(U / 5.0, V / 5.0, 23, 3)                             # leaves gather along each twig
            black |= (d_ < 7.5 - 3.0 * t_) & (leaves > 0.56 + 0.03 * d_)
        sky = np.where(black[..., None], col("#080d28"), sky)
    bar = 1 - band(U, 3.2, wcm - 3.2, fp) * band(V, 3.2, hcm - 3.2, fp) * (1 - band(U, wcm / 2 - 1.4, wcm / 2 + 1.4, fp))
    alb = np.zeros(U.shape + (3,), dtype=F32) + col(TRIM) * bar[..., None]
    return alb, sky * (1 - bar[..., None])


def skylight_bars(i, u, v, w):
    """1 where the moon comes through the glass, 0 behind the sash and its middle bar."""
    x0, x1, z0, z1 = M.SKYLIGHTS[i]
    wcm = x1 - x0
    return 1 - sstep(1.4 + w * 0.5, 1.4 - w * 0.5, np.abs(u - 0.5) * wcm) * 0.85


def m_skylight(i):
    lining = plain(TRIM, 0.06, 9, 2)

    def f(c):
        if c.face == "top":
            return sky_in(c, i)
        return lining(c)
    return f


def shell(st):
    wz, wy, wr = M.ROUND_WINDOW
    hx0, hx1, hz0, hz1 = M.HATCH
    holes = {
        "slope": lambda X, Y, Z: np.logical_or.reduce([(X > x0) & (X < x1) & (Z > z0) & (Z < z1) for x0, x1, z0, z1 in M.SKYLIGHTS]),
        "endL": lambda X, Y, Z: np.hypot(Z - wz, Y - wy) < wr,
        "floor": lambda X, Y, Z: (X > hx0) & (X < hx1) & (Z > hz0) & (Z < hz1),
    }
    st.room(M.W, K, R, dict(floor=m_floor, far=m_far, endL=m_end, endR=m_end, slope=m_slope), holes)
    # ---- rafters, every 75 cm; two are cut short above and below each skylight and carried on trimmers
    cut = {230: M.SKYLIGHTS[0], 530: M.SKYLIGHTS[1]}
    for i, xc in enumerate(M.RAFTERS):
        mat = m_rafter(i + 1)
        if xc in cut:
            _, _, z0, z1 = cut[xc]
            st.box(xc - RAFT_W, xc + RAFT_W, K - RAFT_D * Q, K, 0, z0 - 12, mat, "rafter", shear=R, shadow=False)
            st.box(xc - RAFT_W, xc + RAFT_W, K - RAFT_D * Q, K, z1 + 12, 420, mat, "rafter", shear=R, shadow=False)
        else:
            st.box(xc - RAFT_W, xc + RAFT_W, K - RAFT_D * Q, K, 0, 420, mat, "rafter", shear=R, shadow=False)
    for i, (x0, x1, z0, z1) in enumerate(M.SKYLIGHTS):
        xa, xb = x0 - 15 + RAFT_W, x1 + 15 - RAFT_W
        tm = m_rafter(20 + i)
        st.box(xa, xb, K - RAFT_D * Q, K, z0 - 12, z0 - 5, wood(RAFT, 3 + i, "x", 0.2), "rafter", shear=R, shadow=False)     # trimmers
        st.box(xa, xb, K - RAFT_D * Q, K, z1 + 5, z1 + 12, wood(RAFT, 5 + i, "x", 0.2), "rafter", shear=R, shadow=False)
        # the lining of the opening (seen from inside), with the glass at its top
        st.box(x0, x1, K, K + SKY_D * Q, z0, z1, m_skylight(i), "skylight", shear=R, inside=True, flag=2)
        # a painted casing round the opening, lying on the boards
        tw = plain(TRIM, 0.06, 9, 3)
        for (a, b, c_, d) in ((x0 - 6, x0, z0 - 5, z1 + 5), (x1, x1 + 6, z0 - 5, z1 + 5), (x0, x1, z0 - 5, z0), (x0, x1, z1, z1 + 5)):
            st.box(a, b, K - 1.8 * Q, K, c_, d, tw, "skylight", shear=R, shadow=False)
    # ---- the low wall's ledge, just under the roof
    lx0, lx1, ly0, ly1, lz0, lz1 = M.LEDGE
    st.box(lx0, lx1, ly0, ly1, lz0, lz1, wood(PINE, 7, "x", 0.16), "ledge", shadow=False)
    st.box(lx0, lx1, ly1, ly1 + 8, 0, 1.2, plain(TRIM, 0.05), "ledge", shadow=False)
    # ---- the round window in the left end wall: its deep reveal, the glass, a cross of glazing bars
    def m_round(c):
        return col(TRIM) * (0.9 + 0.1 * fbm(c.Z / 8, c.Y / 8, 3, 2))[..., None]      # the reveal

    def m_pane(c):
        v_ = (c.Y - (wy - wr)) / (2 * wr)
        sky = lerp(col("#35488e"), col("#131c56"), np.clip(v_, 0, 1)[..., None])
        sky = sky + col("#5a78b8") * (np.clip(0.42 - v_, 0, 1) * 0.5)[..., None]
        tr = fbm(c.Z / 11, c.Y / 9, 23, 4)
        crown = np.clip(1.2 - np.hypot((c.Z - (wz + 26)) / 42.0, (c.Y - (wy - 6)) / 44.0), 0, 1)
        black = ((tr + crown * 0.72) > 0.98) | (c.Y < wy - wr + 14 + 6 * fbm(c.Z / 14, c.Y * 0, 9, 2))
        sky = np.where(black[..., None], col("#0a1030"), sky)
        cz, cy = np.floor(c.Z / 6.0), np.floor(c.Y / 6.0)
        star = (hashf(cz * 31 + cy * 57, 4) > 0.86) & (np.hypot(c.Z - (cz + 0.5) * 6, c.Y - (cy + 0.5) * 6) < 0.7 + c.fp * 0.5) & ~black
        sky = sky + col("#e6ecff") * (star * 0.8)[..., None]
        bars = (np.abs(c.Z - wz) < 1.6) | (np.abs(c.Y - wy) < 1.6) | (np.hypot(c.Z - wz, c.Y - wy) > wr - 3.5)
        alb = np.where(bars[..., None], col(TRIM), 0.0).astype(F32)
        return alb, np.where(bars[..., None], 0.0, sky).astype(F32), np.hypot(c.Z - wz, c.Y - wy) < wr + 0.5
    st.cyl((wy, wz), wr, -22, 0, m_round, axis="x", name="window", hollow=True, shadow=False)
    st.poly([(-16, wy - wr - 1, wz - wr - 1), (-16, wy - wr - 1, wz + wr + 1), (-16, wy + wr + 1, wz + wr + 1), (-16, wy + wr + 1, wz - wr - 1)],
            m_pane, "window", flag=2)


# ---------------------------------------------------------------- the strings of tiny lights, looped from rafter to rafter
def _hang(hooks, sags, step=11.0):
    """Places of the bulbs along a string hung from hook to hook, sagging between them. -> (bulbs, the whole line)"""
    bulbs, line = [], []
    for k, (a, b) in enumerate(zip(hooks[:-1], hooks[1:])):
        a, b = np.asarray(a, float), np.asarray(b, float)
        n = max(int(np.linalg.norm(b - a) / step), 2)
        for j in range(n):
            f = j / n
            p = a + (b - a) * f
            p[1] -= sags[k % len(sags)] * 4 * f * (1 - f)
            line.append(tuple(p))
            if j > 0 or k == 0:
                bulbs.append((p[0], p[1] - 0.8, p[2]))
    line.append(tuple(hooks[-1]))
    return bulbs, line


def _under(x, z, drop=1.5):
    return (x, roof(z) - RAFT_D * Q - drop, z)


_S1 = _hang([_under(x, 90 + 7 * (i % 2)) for i, x in enumerate(M.RAFTERS)], [9, 12, 8, 11, 10, 13, 9, 11, 12, 8])
_S2 = _hang([_under(x, 292 if i % 2 == 0 else 346) for i, x in enumerate(M.RAFTERS)], [13, 10, 15, 11, 12, 14, 10, 13, 11, 14], step=12.0)
STRINGS = [_S1[0], _S2[0]]
_LINES = [_S1[1], _S2[1]]


def strings(st):
    for line in _LINES:
        st.rope(line, 0.22, col("#b8a890"), name="strings", min_px=0.5, flag=2, shade=False)
    for bulbs in STRINGS:
        for i, p in enumerate(bulbs):
            st.ball(p, 1.15, col("#fff0d0"), "strings", shadow=False, flag=2, emi=col("#ffd9a0") * 3.0)



# ---------------------------------------------------------------- small makers used again and again
def candle(st, x, y, z, name="candle", grp="back", r=3.3, h=8.5, power=1.0):
    """A flameless candle in a glass: the wax glows from inside, brightest at the little lamp in its top."""
    def m(c):
        f = np.clip(c.along / h, 0, 1)
        e = lerp(col("#f07a20"), col("#ffc060"), (f ** 1.5)[:, None]) * (0.55 + 1.9 * f ** 1.5)[:, None] * power
        return full(c, "#f4d8a8"), e
    st.cyl((x, z), r, y, y + h, m, name=name, grp=grp, shadow=False, flag=2, cap=col("#fff0c8"))
    st.ball((x, y + h + 0.6, z), 1.0, col("#fff6dc"), name, grp, shadow=False, flag=2, emi=col("#ffe2a0") * 3.4 * power)


def pot(st, x, z, y, r, h, color, name, grp="back", foot=False, soil="#3a2a20", flare=1.15, seed=0):
    k = col(color)

    def m(c):
        v = 1 - 0.10 * np.clip(1 - c.along / 2.0, 0, 1) + 0.06 * (fbm(c.ang * 3 + seed, c.along / 4.0, 3, 2) - 0.5)
        return k[None, :] * v[:, None]
    st.cyl((x, z), r, y, y + h, m, r1=r * flare, name=name, grp=grp, foot=foot, cap=col(soil))


def legs(st, pts, radius, color, name, grp, splay=0.0, top=None, r1=None):
    """Legs standing on the floor at the places pts [(X, Z)], up to height `top`, each leaning in by `splay` cm."""
    cx = sum(p[0] for p in pts) / len(pts)
    cz = sum(p[1] for p in pts) / len(pts)
    for (x, z) in pts:
        dx, dz = (cx - x), (cz - z)
        l = math.hypot(dx, dz) + 1e-6
        st.stick((x, 0.2, z), (x + dx / l * splay, top, z + dz / l * splay), radius, col(color), name, grp, r1=r1)
        st.occ.append((x - radius, x + radius, 0, top, z - radius, z + radius))


def leaf_color(base, k, seed=0, amt=0.22):
    b = col(base)
    h = float(hashf(k, seed))
    h2 = float(hashf(k * 7 + 3, seed + 1))
    return np.clip(b * (0.80 + amt * 2 * h) + np.array([0.05, 0.03, -0.02], dtype=F32) * (h2 - 0.4), 0, 1)


def frond(st, base, az, length, rise, droop, name, grp="back", color="#4a7a52", pairs=13, leaf=15.0, width=2.6, seed=0, stem="#5a7a48", lean=0.0):
    """A palm frond: a rib that climbs, arches over and droops at its tip, with leaflets down both sides."""
    ca, sa = math.cos(az), math.sin(az)
    px, pz = -sa, ca                                             # level, square to the rib
    rib = []
    n = 12
    for i in range(n + 1):
        s = i / n
        out = length * (s ** 1.25)
        y = base[1] + rise * s * (2 - s) - droop * s ** 3.2
        rib.append((base[0] + ca * out + px * lean * s * s, y, base[2] + sa * out + pz * lean * s * s))
    for a, b in zip(rib[:-1], rib[1:]):
        st.stick(a, b, 0.55, col(stem), name, grp, min_px=0.5)
    R = np.asarray(rib)
    for k in range(pairs):
        s = 0.16 + 0.82 * k / max(pairs - 1, 1)
        f = s * n
        i = min(int(f), n - 1)
        p = R[i] + (R[i + 1] - R[i]) * (f - i)
        d = R[i + 1] - R[i]
        d = d / (np.linalg.norm(d) + 1e-9)
        size = leaf * (0.45 + 0.75 * math.sin(math.pi * min(s * 1.08, 1.0)) ** 0.7)
        for side in (-1, 1):
            j = float(hashf(k * 2 + (side > 0), seed + 11))
            tip = p + (np.array([px, 0, pz]) * side * 0.80 + d * 0.50) * size + np.array([0, -size * (0.18 + 0.30 * j) + 0.25 * size * (1 - s), 0])
            a_ = p - d * width * 0.5
            b_ = p + d * width * 0.5
            st.poly([tuple(a_), tuple(b_), tuple(tip)], leaf_color(color, k * 2 + (side > 0), seed), name, grp, flag=1)


def blade(st, base, az, length, rise, droop, name, grp="back", color="#4f8456", width=5.0, seed=0, n=7, lean=0.0):
    """A fern's frond (or any long drooping leaf) as a tapering ribbon with a darker rib."""
    ca, sa = math.cos(az), math.sin(az)
    px, pz = -sa, ca
    k = leaf_color(color, seed, 5)
    pts = []
    for i in range(n + 1):
        s = i / n
        out = length * (s ** 1.15)
        y = base[1] + rise * s * (2 - s) - droop * s ** 2.6
        w = width * (0.25 + 0.75 * math.sin(math.pi * min(0.12 + s * 0.88, 1.0)) ** 0.8) * (1 - 0.6 * s * s)
        c0 = np.array([base[0] + ca * out + px * lean * s * s, y, base[2] + sa * out + pz * lean * s * s])
        pts.append((c0 - np.array([px, 0.12, pz]) * w / 2, c0 + np.array([px, -0.12, pz]) * w / 2, c0))
    for i in range(n):
        (l0, r0, c0), (l1, r1, c1) = pts[i], pts[i + 1]
        kk = k * (0.86 + 0.28 * float(hashf(seed * 13 + i, 2)))
        st.poly([tuple(l0), tuple(l1), tuple(c1), tuple(c0)], kk * 0.92, name, grp, flag=1)
        st.poly([tuple(c0), tuple(c1), tuple(r1), tuple(r0)], kk * 1.06, name, grp, flag=1)


def strand(st, start, length, name, grp="back", color="#4f8a58", seed=0, swing=3.0, leaf=4.6, drift=(0.0, 0.0), step=5.5):
    """A trailing strand of ivy: it hangs, wandering a little, with a leaf every few centimetres on alternate sides."""
    pts = []
    n = max(int(length / step), 2)
    ph = float(hashf(seed, 3)) * 6.28
    for i in range(n + 1):
        s = i / n
        pts.append((start[0] + drift[0] * s + swing * math.sin(ph + s * 5.0) * s, start[1] - length * s, start[2] + drift[1] * s + swing * 0.7 * math.cos(ph * 1.7 + s * 4.0) * s))
    st.rope(pts, 0.3, col("#4a6a40"), name=name, grp=grp, min_px=0.45)
    for i in range(1, n + 1):
        p = np.asarray(pts[i])
        side = 1 if i % 2 else -1
        j = float(hashf(seed * 31 + i, 4))
        a = ph + i * 2.4
        dx, dz = math.cos(a) * side, math.sin(a) * side
        sz = leaf * (0.7 + 0.6 * j) * (1.0 - 0.3 * i / n)
        tip = p + np.array([dx * sz, -sz * 0.55, dz * sz])
        l = p + np.array([-dz * sz * 0.42 + dx * sz * 0.4, -sz * 0.12, dx * sz * 0.42 + dz * sz * 0.4])
        r = p + np.array([dz * sz * 0.42 + dx * sz * 0.4, -sz * 0.12, -dx * sz * 0.42 + dz * sz * 0.4])
        st.poly([tuple(p), tuple(l), tuple(tip), tuple(r)], leaf_color(color, seed * 17 + i, 6), name, grp, flag=1)


# ---------------------------------------------------------------- the far wall: bookcase, timeline, sound table, cushions
RAINBOW = [(0.00, "#c23a36"), (0.10, "#dd6a32"), (0.20, "#e8a53a"), (0.30, "#e6cf5a"), (0.40, "#8cb85a"), (0.50, "#3f9a7c"),
           (0.60, "#3f86b8"), (0.70, "#4558a8"), (0.79, "#7a4fa0"), (0.87, "#c06a9c"), (0.93, "#eac6c8"), (1.00, "#f2ece0")]


def rainbow(t):
    pos = [p for p, _ in RAINBOW]
    cols = [col(c) for _, c in RAINBOW]
    out = np.zeros(t.shape + (3,), dtype=F32)
    for i in range(3):
        out[..., i] = np.interp(t, pos, [c[i] for c in cols])
    return out


def m_books(x0, x1, y0, hmax, row):
    """A shelf of books seen spine-on, sorted by color from one end of the bookcase to the other."""
    bx0, bx1 = M.BOOKCASE[0] + 3, M.BOOKCASE[1] - 3

    def f(c):
        if c.face != "front":
            return full(c, "#4a3c38")
        u, v, fp = c.X - x0, c.Y - y0, c.fp
        idx = np.floor(u / 3.1 + 0.24 * np.sin(u * 0.9 + row * 2.0))
        fr = (u / 3.1 + 0.24 * np.sin(u * 0.9 + row * 2.0)) - idx
        key = idx + row * 97
        t = np.clip(((x0 + (idx + 0.5) * 3.1) - bx0) / (bx1 - bx0), 0, 1)
        t = np.clip(t + (hashf(key, 3) - 0.5) * 0.035, 0, 1)
        k = rainbow(t)
        k = k * (0.78 + 0.36 * hashf(key, 5))[..., None]
        k = lerp(k, col("#efe6d6"), ((hashf(key, 6) > 0.9) * 0.55)[..., None])        # the odd pale spine among the colors
        hgt = hmax * (0.62 + 0.36 * hashf(key, 7))
        there = (v < hgt)
        gap = np.clip(1 - fr * 3.1 / np.maximum(fp, 0.3), 0, 1) * 0.55 + np.clip(1 - (1 - fr) * 3.1 / np.maximum(fp, 0.3), 0, 1) * 0.25
        k = k * (1 - np.clip(gap, 0, 0.6))[..., None]
        lab = (np.abs(v - hgt * (0.68 + 0.12 * hashf(key, 8))) < 1.6) & (hashf(key, 9) > 0.45)      # a band where the title is
        k = np.where(lab[..., None], k * 0.55 + col("#f0e6c8") * 0.45, k)
        foot = (np.abs(v - 2.4) < 0.8) & (hashf(key, 10) > 0.6)
        k = np.where(foot[..., None], k * 0.7, k)
        k = k * (1 - 0.25 * np.clip((v - (hgt - 1.2)) / 1.2, 0, 1))[..., None]                 # the top of each spine turns away
        dark = col("#3c2f2e") * (0.7 + 0.3 * np.clip(v / hmax, 0, 1))[..., None]
        return np.where(there[..., None], k, dark)
    return f


def bookcase(st):
    x0, x1, y0, y1, z0, z1 = M.BOOKCASE
    wp = plain(TRIM, 0.06, 12, 4)
    st.box(x0, x1, y1 - 4, y1, z0, z1, wp, "bookcase", foot=False)
    st.box(x0, x1, 0, 7, z0, z1 - 2, wp, "bookcase", foot=True)
    st.box(x0, x0 + 3, 7, y1 - 4, z0, z1, wp, "bookcase")
    st.box(x1 - 3, x1, 7, y1 - 4, z0, z1, wp, "bookcase")
    xm = (x0 + x1) / 2
    st.box(xm - 1.5, xm + 1.5, 7, y1 - 4, z0, z1 - 1, wp, "bookcase", shadow=False)
    ym = 47.0
    st.box(x0 + 3, x1 - 3, ym - 1.3, ym + 1.3, z0, z1 - 1, wp, "bookcase", shadow=False)
    st.box(x0 + 3, x1 - 3, 7, y1 - 4, z0, z0 + 1.5, col("#4a3c38"), "bookcase", shadow=False)
    for row, (ya, yb) in enumerate(((ym + 1.3, y1 - 4), (7, ym - 1.3))):
        for bay, (xa, xb) in enumerate(((x0 + 3, xm - 1.5), (xm + 1.5, x1 - 3))):
            st.box(xa, xb, ya, yb - 2.0, z0 + 2, z1 - 4.5, m_books(xa, xb, ya, yb - ya - 2.5, row), "bookcase", shadow=False)
    st.feet["bookcase"] = (x0, x1, z0, z1)
    # ---- on top of it: two candles, a few books lying flat with a bowl on them, a photograph, her metronome, a pothos
    candle(st, x0 + 20, y1, 12)
    candle(st, x0 + 142, y1, 15, r=2.8, h=6.5)
    for i, (kc, dh) in enumerate((("#7a4fa0", 3.2), ("#e6cf5a", 2.6), ("#3f86b8", 3.4))):
        yb = y1 + sum(h for _, h in (("", 3.2), ("", 2.6), ("", 3.4))[:i])
        st.box(x0 + 50 + i * 1.2, x0 + 76 - i, yb, yb + dh, 4 + i, 22 - i, m_flatbook(kc), "bookcase", shadow=False)
    st.cyl((x0 + 63, 13), 4.2, y1 + 9.2, y1 + 13.2, plain("#9fc0c4", 0.08), r1=6.4, name="bookcase", shadow=False, cap=col("#6f9aa0"))
    st.poly([(x0 + 96, y1, 15), (x0 + 118, y1, 15), (x0 + 118, y1 + 17, 10), (x0 + 96, y1 + 17, 10)], m_photo, "bookcase")
    mx = x0 + 176                                                             # the metronome: she plays the piano
    st.cyl((mx, 13), 5.0, y1, y1 + 17, wood("#8a5a34", 3, "y", 0.2), r1=1.6, name="bookcase", shadow=False)
    st.stick((mx, y1 + 3, 16.5), (mx + 2.6, y1 + 21, 16.5), 0.28, col("#d8c8a0"), "bookcase", min_px=0.5)
    px_ = x1 - 20                                                             # the pothos, trailing over the end
    pot(st, px_, 13, y1, 6.5, 10, "#e9e2d4", "bookcase")
    for k in range(9):
        a = k * 0.7 + 0.3
        blade(st, (px_ + math.cos(a) * 3, y1 + 10, 13 + math.sin(a) * 3), a, 9 + 4 * (k % 3), 7, 6 + 2 * (k % 2), "bookcase", color="#5f9a5a", width=5.5, seed=40 + k, n=4)
    strand(st, (px_ + 7, y1 + 9, 18), 38, "bookcase", seed=3, drift=(9, 9), swing=2.5)
    strand(st, (px_ + 3, y1 + 9, 20), 27, "bookcase", seed=5, drift=(2, 7), swing=2.0)
    strand(st, (px_ - 6, y1 + 9, 19), 17, "bookcase", seed=8, drift=(-3, 6), swing=2.0)


def m_flatbook(color):
    k = col(color)

    def f(c):
        if c.face in ("front", "right", "left"):
            pages = (c.Y > c.box[2] + 0.5) & (c.Y < c.box[3] - 0.5) & (c.face != "left")
            return np.where(pages[..., None], col("#eee4cc"), k * 0.9)
        return full(c, color) * (0.92 + 0.14 * patch(c, 6, 2)[..., None])
    return f


def m_photo(c):
    u, v, fp = c.U, c.V, c.fp
    out = full(c, "#e8dcc0")
    inner = rect(u, v, 2.2, 19.8, 2.2, 15.5, fp)
    pic = lerp(col("#c89a6a"), col("#7fa0c4"), np.clip((v - 7) / 5.0, 0, 1)[..., None])
    ppl = ((np.abs(u - 8) < 1.8) & (v < 11) & (v > 3)) | ((np.abs(u - 12.5) < 1.5) & (v < 9.5) & (v > 3)) | ((np.abs(u - 16) < 1.2) & (v < 8) & (v > 3))
    pic = np.where(ppl[..., None], col("#a04a40"), pic)
    return out * (1 - inner[..., None]) + pic * inner[..., None]


def m_timeline(c):
    """Her timeline: one long strip of paper, a ruled line with ticks, small drawings and lettering; three quarters
    of the way along, a RED mark, and beyond it the lettering and the drawings change sides."""
    x0, x1, y0, y1 = M.TIMELINE
    u, v, fp = c.X - x0, c.Y - y0, np.maximum(c.fp, 0.5)
    w, h = x1 - x0, y1 - y0
    out = np.zeros(u.shape + (3,), dtype=F32) + col("#f4edda")
    out = out * (0.95 + 0.07 * fbm(u / 20, v / 8, 3, 2)[..., None])
    sheet = 57.0                                                              # sheets taped end to end
    js = np.abs(u / sheet - np.round(u / sheet)) * sheet
    out = out * (1 - 0.22 * np.clip(1 - js / fp, 0, 1) * (u > 4) * (u < w - 4))[..., None]
    red = w * M.TIMELINE_RED
    mid = h * 0.5
    ink = col("#33385e")
    line = band(v, mid - 0.55, mid + 0.55, fp) * band(u, 5, w - 5, fp)
    out = lay(out, ink, line * 0.9)
    tk = 9.6
    it = np.round((u - 8) / tk)
    du = np.abs((u - 8) - it * tk)
    long_ = (np.mod(it, 5) == 0)
    tick = np.clip(0.9 - du / fp, 0, 1) * band(v, mid - np.where(long_, 4.6, 2.6), mid + np.where(long_, 4.6, 2.6), fp) * (u > 6) * (u < w - 6)
    out = lay(out, ink, tick * 0.85)
    after = u > red
    # the lettering: short lines of small writing, under the line before the red mark and over it after
    cell = np.floor((u - 8) / tk)
    lv = np.where(after, v - (mid + 4.2), (mid - 4.2) - v)                      # distance from the line, on the lettering's side
    wr = (np.mod(u - 8, tk) > 1.6) & (np.mod(u - 8, tk) < 1.6 + 3.0 + 4.2 * hashf(cell, 3)) & (((lv > 0.6) & (lv < 1.9)) | ((lv > 3.2) & (lv < 4.5) & (hashf(cell, 4) > 0.4)))
    wr &= (u > 8) & (u < w - 8) & (hashf(cell, 5) > 0.18)
    out = np.where(wr[..., None], out * 0.35 + ink * 0.65, out)
    # the drawings: one small picture every so often, on the other side
    dcell = np.floor((u - 12) / 19.2)
    cu = 12 + (dcell + 0.5) * 19.2
    dv = np.where(after, (mid - 6.2) - v, v - (mid + 6.2))                      # 0 at the middle of the drawing, on its side
    du_ = u - cu
    kind = np.floor(hashf(dcell, 7) * 6)
    pal = [col("#d0a040"), col("#8a8aa0"), col("#b0603a"), col("#3f86b8"), col("#5a9a5a"), col("#c06a9c")]
    shape = np.zeros(u.shape, dtype=bool)
    shape |= (kind == 0) & (np.abs(du_) < (3.6 - dv) * 0.9) & (dv > -3.0) & (dv < 3.6)                 # a pyramid
    shape |= (kind == 1) & (((np.abs(du_) < 1.3) & (np.abs(dv) < 3.4)) | ((np.abs(du_) < 2.6) & (np.abs(np.abs(dv) - 3.0) < 0.7)))   # a column
    shape |= (kind == 2) & (((np.abs(du_) < 4.0) & (dv > -3.2) & (dv < -1.4)) | ((du_ > -0.4) & (du_ < 3.0 - (dv + 1.4) * 0.7) & (dv >= -1.4) & (dv < 3.2)))   # a ship
    shape |= (kind == 3) & (np.hypot(du_, dv) < 3.0) & (np.hypot(du_ - 1.2, dv - 0.6) > 2.2)           # a moon
    shape |= (kind == 4) & (((np.abs(du_) < 0.7) & (dv < 0.5) & (dv > -3.4)) | (np.hypot(du_, dv - 1.4) < 2.6))   # a tree
    shape |= (kind == 5) & (np.abs(du_) < 3.2) & (np.abs(dv) < 2.6) & ~((np.abs(du_) < 1.1) & (dv < 0.8))   # a gate
    shape &= (u > 10) & (u < w - 10) & (np.abs(u - red) > 7)
    for k in range(6):
        out = np.where((shape & (kind == k))[..., None], pal[k], out)
    # the red mark
    rm = band(u, red - 0.9, red + 0.9, fp) * band(v, 1.6, h - 1.6, fp)
    out = lay(out, "#d02a24", rm)
    out = lay(out, "#d02a24", disc(u, v, red, h - 3.2, 2.6, fp))
    # paper tape at the corners and along the top
    tp = np.abs(np.mod(u + 20, 76.0) - 38.0) < 3.4
    tape = tp & (v > h - 2.6)
    out = np.where(tape[..., None], col("#d9a0a0") * 0.95, out)
    return out


def far_wall(st):
    bookcase(st)
    x0, x1, y0, y1 = M.TIMELINE
    st.poly([(x0, y0, 0.5), (x1, y0, 0.5), (x1, y1, 0.5), (x0, y1, 0.5)], m_timeline, "timeline")
    for x in M.CANDLES:
        candle(st, x, M.LEDGE[3], 6.5, r=3.0, h=7.0)
    # a little jar of dried grasses on the ledge, and a row of smooth stones
    st.cyl((300, 6), 2.6, M.LEDGE[3], M.LEDGE[3] + 6.5, plain("#b9cfd0", 0.06), name="ledge", shadow=False)
    for k, (dx, dy) in enumerate(((-3, 9), (-1, 12), (1.5, 10), (3.5, 8), (0.5, 13))):
        st.stick((300, M.LEDGE[3] + 6, 6), (300 + dx, M.LEDGE[3] + 6 + dy * 0.75, 6.5), 0.3, col("#d8c088"), "ledge", min_px=0.5)
    for k, x in enumerate((536, 545, 553, 560)):
        st.ball((x, M.LEDGE[3] + 1.6 - 0.2 * k, 6), 3.4 - 0.5 * k, plain(["#9a9490", "#b8b0a6", "#847e7c", "#c9c0b4"][k], 0.1, 4), "ledge", shadow=False, squash=(1, 0.5, 0.8))
    sound_table(st)
    # ---- a spare mat, rolled and strapped, stood on end between the bookcase and the sound table
    st.cyl((313, 14), 7.2, 0, 64, lambda c: col("#a88cb8")[None, :] * (0.86 + 0.14 * np.cos(c.ang * 1.0 + 0.6) + 0.06 * (fbm(c.ang * 4, c.along / 6.0, 3, 2) - 0.5))[:, None] * (1 - 0.3 * ((np.abs(c.along - 18) < 1.3) | (np.abs(c.along - 46) < 1.3)))[:, None],
           name="sparemat", foot=True, cap=lambda c: col("#a88cb8")[None, :] * (0.7 + 0.3 * (np.sin(c.rad * 4.2 + c.ang) * 0.5 + 0.5))[:, None])
    # ---- floor cushions stacked between the sound table and the desk
    for i, (kc, hh) in enumerate(((ROSE, 11), ("#e8dcc4", 10), ("#8a6a98", 10))):
        yb = sum(h for _, h in ((0, 11), (0, 10), (0, 10))[:i])
        m_c = m_cushion(kc, i)
        st.ball((469 + (i % 2) * 2, yb + hh / 2, 31 + i), 26 - i * 1.5, m_c, "cushions", squash=(1, hh / 2 / (26 - i * 1.5) * 1.25, 0.92), foot=(i == 0))
    desk_wall(st)


def m_cushion(color, seed=0, piping=None):
    k = col(color)

    def f(c):
        tex = 0.92 + 0.14 * fbm(c.X / 3.0, c.Z / 3.0 + c.Y / 2.0, 11 + seed, 2)
        v = k[None, :] * tex[:, None]
        seamline = np.clip(1 - np.abs(c.lat) / 0.10, 0, 1)                      # the seam round its middle
        v = v * (1 - 0.22 * seamline[:, None])
        if piping is not None:
            v = lerp(v, col(piping)[None, :], (np.clip(1 - np.abs(c.lat) / 0.05, 0, 1) * 0.8)[:, None])
        return v
    return f


def sound_table(st):
    x0, x1, y0, y1, z0, z1 = M.SOUNDTABLE
    wd = wood(PINE, 9, "x", 0.16)
    st.box(x0, x1, y1 - 3.2, y1, z0, z1, wd, "soundtable", foot=False)
    st.box(x0 + 5, x1 - 5, 17, 19.5, z0 + 4, z1 - 4, wd, "soundtable", shadow=False)
    legs(st, [(x0 + 5, z0 + 4), (x1 - 5, z0 + 4), (x0 + 5, z1 - 4), (x1 - 5, z1 - 4)], 2.0, "#c9a070", "soundtable", "back", splay=0, top=y1 - 3)
    st.feet["soundtable"] = (x0 + 2, x1 - 2, z0 + 2, z1 - 2)
    # under it: a basket, and her spare batteries in a tin
    st.cyl((x0 + 30, 28), 14, 19.5, 36, m_weave("#c8a474", 2), r1=15.5, name="soundtable", shadow=False, cap=col("#e9dfcc"))
    st.box(x1 - 44, x1 - 14, 19.5, 30, 16, 40, plain("#7fa4a8", 0.08, 6), "soundtable", shadow=False)
    # ---- the sound machine: a small rounded box, a round speaker grille, a dial
    mx0, mx1, my0, my1, mz0, mz1 = M.MACHINE

    def m_machine(c):
        body = col("#efe4d0") * (0.95 + 0.08 * patch(c, 8, 3)[..., None])
        if c.face == "front":
            u, v, fp = c.X - mx0, c.Y - my0, c.fp
            w, h = mx1 - mx0, my1 - my0
            rnd = np.clip((np.minimum(np.minimum(u, w - u), np.minimum(v, h - v)) + 0.4) / 3.0, 0.55, 1)      # its corners turn away
            body = body * rnd[..., None]
            gx, gy, gr = w * 0.36, h * 0.52, h * 0.37
            d = np.hypot(u - gx, v - gy)
            g = disc(u, v, gx, gy, gr, fp)
            holes = ((np.mod(u, 2.4) < 1.2) ^ (np.mod(v, 2.4) < 1.2))
            grille = np.where(holes[..., None], col("#5a4a40"), col("#8a6a50"))
            body = body * (1 - g[..., None]) + grille * g[..., None]
            ring = band(d, gr - 0.4, gr + 1.3, fp)
            body = lay(body, "#b88a50", ring)
            dx_, dy_, dr = w * 0.80, h * 0.60, h * 0.19
            body = lay(body, "#e0863a", disc(u, v, dx_, dy_, dr, fp))
            body = lay(body, "#fff0d8", band(u, dx_ - 0.55, dx_ + 0.55, fp) * band(v, dy_, dy_ + dr, fp))
            body = lay(body, "#7a6a5a", disc(u, v, dx_ - 2.2, h * 0.2, 1.3, fp))
            body = lay(body, "#7a6a5a", disc(u, v, dx_ + 2.2, h * 0.2, 1.3, fp))
        elif c.face == "top":
            u, v = c.X - mx0, c.Z - mz0
            body = body * 1.04
            body = lay(body, "#b88a50", rect(u, v, (mx1 - mx0) * 0.28, (mx1 - mx0) * 0.72, (mz1 - mz0) * 0.42, (mz1 - mz0) * 0.58, c.fp) * 0.8)   # its carrying handle
        return body
    st.box(mx0, mx1, my0, my1, mz0, mz1, m_machine, "machine")
    st.box(mx0 + 3, mx0 + 6, my0 - 0.01, my0 + 0.01, mz0, mz1, col("#000000"), "machine", shadow=False)
    # ---- the little fountain: a glazed bowl, river stones, a bamboo spout, water running over
    fx, fz, fr = M.FOUNTAIN

    def m_bowl(c):
        gl = col("#6f9c9a") * (0.9 + 0.2 * fbm(c.ang * 2.0, c.along / 3.0, 5, 2))[:, None]
        rim = np.clip((c.along - 8.6) / 1.4, 0, 1)
        return gl * (1 - rim[:, None]) + col("#cfe0d8") * rim[:, None]

    def m_water(c):
        d = c.rad / fr
        k = lerp(col("#2c4a58"), col("#4f7a86"), np.clip(d, 0, 1)[:, None])
        rip = np.clip(np.sin(c.rad * 2.6) * 0.5 + 0.5, 0, 1) ** 4
        return k + col("#a8c8d8")[None, :] * (rip * 0.28)[:, None]
    st.cyl((fx, fz), fr * 0.72, y1, y1 + 10, m_bowl, r1=fr, name="fountain", cap=m_water)
    for k, (dx, dz, r_, dy, kc) in enumerate(((-5, 1, 6.6, 2.0, "#a09a92"), (5, -1, 5.8, 2.2, "#c0b6a8"), (0, 5, 5.0, 1.6, "#8a8482"), (-1, -3, 5.4, 6.8, "#d0c6b6"), (3, 2, 4.0, 7.4, "#989088"), (-6, -4, 3.8, 3.0, "#b4aca0"))):
        st.ball((fx + dx, y1 + 9.5 + dy, fz + dz), r_, plain(kc, 0.12, 3, k), "fountain", shadow=False, squash=(1, 0.72, 0.9))
    st.stick((fx + 14, y1 + 8, fz - 10), (fx + 13, y1 + 36, fz - 11), 1.7, col("#c2aa5e"), "fountain")                     # bamboo upright
    st.stick((fx + 15.5, y1 + 30, fz - 11), (fx + 1.0, y1 + 24.5, fz - 4), 1.45, col("#cfb768"), "fountain")               # and the spout
    st.rope([(fx + 0.8, y1 + 24, fz - 3.8), (fx - 0.4, y1 + 21, fz - 3.0), (fx - 1.0, y1 + 16.5, fz - 2.4)], 0.55, col("#d6e8f2"), name="fountain", min_px=0.7, flag=2, emi=col("#9fbcd2") * 0.5)


def m_weave(color, seed=0):
    k = col(color)

    def f(c):
        w = np.sin(c.ang * 22 + np.floor(c.along / 2.2) * 3.14159) * 0.5 + 0.5
        rows = np.clip(1 - np.abs(np.mod(c.along, 2.2) - 1.1) / 1.1, 0, 1)
        v = 0.74 + 0.26 * w * (0.5 + 0.5 * rows) + 0.08 * (fbm(c.ang * 5, c.along / 3, 7 + seed, 2) - 0.5)
        return k[None, :] * v[:, None]
    return f


# ---------------------------------------------------------------- the writing desk (its own cut-out), and her novel on the wall
def desk_wall(st):
    cx0, cx1, cy0, cy1 = M.CARDS

    def m_cards(c):
        u, v, fp = c.X - cx0, c.Y - cy0, np.maximum(c.fp, 0.45)
        w, h = cx1 - cx0, cy1 - cy0
        out = np.zeros(u.shape + (3,), dtype=F32) + col("#c9a880") * (0.9 + 0.2 * fbm(u / 2.0, v / 2.0, 6, 2)[..., None])     # a cork strip
        cw, ch = w / 6.0, h / 3.0
        iu, iv = np.floor(u / cw), np.floor(v / ch)
        fu, fv = u - iu * cw, v - iv * ch
        card = rect(fu, fv, 1.2, cw - 1.2, 1.3, ch - 1.3, fp)
        key = iu * 5 + iv * 17
        paper = np.zeros(u.shape + (3,), dtype=F32) + col("#f6f0e0")
        stripe = fv > ch - 3.6
        tints = [col("#d98a8a"), col("#8fb39a"), col("#e2c070"), col("#8aa6d0"), col("#b79ac8")]
        tk = np.floor(hashf(key, 3) * 5)
        for i, t_ in enumerate(tints):
            paper = np.where((stripe & (tk == i))[..., None], t_, paper)
        ln = (np.mod(fv - 2.0, 2.3) < 0.8) & (fv > 1.8) & (fv < ch - 4.2) & (fu > 2.2) & (fu < cw - 2.4 - 4 * hashf(key + np.floor((fv - 2.0) / 2.3), 4))
        paper = np.where(ln[..., None], col("#5a5a78"), paper)
        out = out * (1 - card[..., None]) + paper * card[..., None]
        pin = disc(fu, fv, cw / 2, ch - 2.2, 0.95, fp)
        return lay(out, "#c8322c", pin)
    st.box(cx0 - 2, cx1 + 2, cy0 - 2, cy1 + 2, 0, 1.4, lambda c: m_cards(c) if c.face == "front" else full(c, "#8a6a48"), "cards", shadow=False)


def desk(st, G="desk"):
    x0, x1, y0, y1, z0, z1 = M.DESK
    top = wood(PINE, 2, "x", 0.16)
    wp = plain(TRIM, 0.06, 10, 5)
    st.box(x0 - 2, x1 + 2, y1 - 3.4, y1, z0 - 2, z1 + 2, top, "desk", G, foot=False)

    def m_apron(c):
        k = wp(c)
        if c.face == "front":
            u, v, fp = c.X - x0, c.Y - (y1 - 13), c.fp
            w = x1 - x0
            dr = rect(u, v, w * 0.30, w * 0.70, 1.2, 8.4, fp) - rect(u, v, w * 0.30 + 0.9, w * 0.70 - 0.9, 2.1, 7.5, fp)
            k = k * (1 - 0.35 * np.clip(dr, 0, 1)[..., None])
            k = lay(k, "#c9a25a", disc(u, v, w * 0.5, 4.8, 1.5, fp))
        return k
    st.box(x0 + 3, x1 - 3, y1 - 13, y1 - 3.4, z0 + 2, z1 - 3, m_apron, "desk", G)
    legs(st, [(x0 + 5, z0 + 5), (x1 - 5, z0 + 5), (x0 + 5, z1 - 6), (x1 - 5, z1 - 6)], 2.4, "#d2ac7c", "desk", G, splay=0, top=y1 - 12, r1=2.8)
    st.feet["desk"] = (x0 + 2, x1 - 2, z0 + 2, z1 - 3)
    # ---- on it: the manuscript, squared up; a jar of pencils, all one length; a small lamp turned low; a notebook
    def m_pages(c):
        if c.face == "top":
            u, v = c.X - c.box[0], c.Z - c.box[4]
            k = full(c, "#f6f0e0")
            ln = (np.mod(v - 3.0, 2.6) < 0.9) & (v > 6.5) & (v < c.box[5] - c.box[4] - 3) & (u > 3) & (u < c.box[1] - c.box[0] - 3 - 6 * hashf(np.floor((v - 3) / 2.6), 3))
            k = np.where(ln[..., None], col("#6a6a88"), k)
            head = (v > 2.6) & (v < 4.6) & (u > 6) & (u < c.box[1] - c.box[0] - 6)
            return np.where(head[..., None], col("#3a3a60"), k)
        pg = (np.mod(c.Y * 2.4, 1.0) < 0.35)
        return np.where(pg[..., None], col("#d8ceb8"), col("#f2ead8"))
    st.box(x0 + 52, x0 + 82, y1, y1 + 6.5, z0 + 20, z0 + 52, m_pages, "desk", G, shadow=False)
    st.stick((x0 + 58, y1 + 7.0, z0 + 46), (x0 + 76, y1 + 7.0, z0 + 40), 0.5, col("#2c3160"), "desk", G, min_px=0.6)      # her pen, across the top sheet
    jx, jz = x0 + 30, z0 + 22
    st.cyl((jx, jz), 4.0, y1, y1 + 10, plain("#c7dbe0", 0.06), name="desk", grp=G, shadow=False, cap=col("#3a3a40"))
    for i, (dx, dz) in enumerate(((1.8, 0.6), (-1.6, 1.0), (0.3, -1.9), (-0.6, 1.9), (2.2, -1.2), (-2.3, -0.8), (0, 0))):
        st.stick((jx + dx * 0.5, y1 + 9, jz + dz * 0.5), (jx + dx * 1.5, y1 + 19.5, jz + dz * 1.5), 0.42, col("#e8b830"), "desk", G, min_px=0.5)
        st.ball((jx + dx * 1.55, y1 + 20.2, jz + dz * 1.55), 0.55, col("#3a3028"), "desk", G, shadow=False)
    lx, lz = x1 - 26, z0 + 22                                                 # the lamp: a little dome on a turned foot
    st.cyl((lx, lz), 5.5, y1, y1 + 1.6, plain("#b88a50", 0.1), name="desk", grp=G, shadow=False)
    st.stick((lx, y1 + 1.5, lz), (lx, y1 + 13, lz), 1.0, col("#b88a50"), "desk", G)

    def m_dome(c):
        f = np.clip(-c.lat / 1.2 + 0.3, 0, 1)
        return full(c, "#f2d8b0"), col("#ffac58")[None, :] * (0.5 + 0.9 * f)[:, None]
    st.ball((lx, y1 + 15, lz), 8.5, m_dome, "desk", G, shadow=False, flag=2, squash=(1, 0.72, 1))
    st.box(x0 + 92, x0 + 110, y1, y1 + 1.6, z0 + 30, z0 + 54, m_flatbook(INDIGO), "desk", G, shadow=False)
    st.cyl((x0 + 14, z0 + 44), 3.6, y1, y1 + 5.2, plain("#e9e2d4", 0.06), name="desk", grp=G, shadow=False, cap=col("#5a3a26"))          # her cup of tea, forgotten
    # ---- the stool
    sx, sz, sr, sh_ = M.STOOL
    st.cyl((sx, sz), sr, sh_ - 4, sh_, wood(PINE, 4, "x", 0.16), name="stool", grp=G, foot=False)
    st.ball((sx, sh_ + 2.5, sz), sr - 1.5, m_cushion(ROSE, 3), "stool", G, shadow=False, squash=(1, 0.28, 1))
    legs(st, [(sx + math.cos(a) * (sr + 1), sz + math.sin(a) * (sr + 1)) for a in (0.6, 2.7, 4.8)], 1.7, "#c9a070", "stool", G, splay=6, top=sh_ - 3)
    st.feet["stool"] = (sx - sr * 0.7, sx + sr * 0.7, sz - sr * 0.7, sz + sr * 0.7)


# ---------------------------------------------------------------- the bed, under its gauze
def m_duvet(c):
    x0, x1, y0, y1, z0, z1 = c.box
    k = col(LINEN)
    fold = fbm(c.X / 26.0, c.Z / 34.0, 3, 3)
    crease = fbm(c.X / 9.0 + c.Y / 5.0, c.Z / 15.0, 8, 2)
    v = 0.86 + 0.20 * fold + 0.08 * (crease - 0.5)
    out = k[None, :] * v[:, None]
    if c.face == "top":
        u, w = c.X - x0, c.Z - z0
        edge = np.minimum(np.minimum(u, (x1 - x0) - u), (z1 - z0) - w)
        out = out * (0.80 + 0.20 * np.clip(edge / 9.0, 0, 1))[:, None]          # it rounds over at its edges
        sheet = band(w, 54, 70, c.fp)                                           # turned back below the pillows
        out = lay(out, "#e3e6ee", sheet * 0.85)
        out = out * (1 - 0.22 * band(w, 69, 72, c.fp))[:, None]
        # a knitted throw across the foot
        th = band(w, (z1 - z0) - 62, (z1 - z0) - 6, c.fp)
        rib = 0.80 + 0.20 * (np.sin(u * 1.5) * 0.5 + 0.5) * (0.6 + 0.4 * (np.sin(w * 1.1 + np.floor(u / 4.2) * 3.14) * 0.5 + 0.5))
        throw = col("#c98a8e")[None, :] * (rib * (0.9 + 0.2 * fold))[:, None]
        out = out * (1 - th[:, None]) + throw * th[:, None]
        out = out * (1 - 0.25 * (band(w, (z1 - z0) - 64.5, (z1 - z0) - 62, c.fp) + band(w, (z1 - z0) - 6, (z1 - z0) - 4, c.fp)))[:, None]
    else:
        drop = np.clip((y1 - c.Y) / (y1 - y0), 0, 1)
        out = out * (0.96 - 0.20 * drop)[:, None]
        if c.face == "left":
            w = c.Z - z0
            th = band(w, (z1 - z0) - 62, (z1 - z0) - 6, c.fp) * (c.Y > y0 + 6)
            throw = col("#c98a8e")[None, :] * (0.84 + 0.2 * fold)[:, None]
            out = out * (1 - th[:, None]) + throw * th[:, None]
            fr = band(w, (z1 - z0) - 62, (z1 - z0) - 6, c.fp) * (c.Y <= y0 + 6) * (np.mod(w, 2.2) < 1.1)       # its fringe
            out = lay(out, "#c98a8e", fr * 0.8)
    return out


def bed(st):
    x0, x1, y0, y1, z0, z1 = M.BED
    st.box(x0 + 13, x1, 0, 9, z0 + 13, z1 - 13, col("#3a2c2c"), "bed", foot=True, shadow=False)          # the plinth it floats on
    st.box(x0, x1, 9, 19, z0, z1, wood(PINE, 11, "z", 0.16), "bed")
    st.box(x0 + 5, x1, 19, y1, z0 + 6, z1 - 5, m_duvet, "bed")
    st.box(x0, x1, 9, 92, z0 - 5, z0 + 1, m_headboard, "bed")
    st.feet["bed"] = (x0 + 13, x1, z0 + 13, z1 - 13)
    # ---- many pillows
    zh = z0 + 1
    for (cx, kc, sd) in ((x0 + 44, "#f6f1e6", 1), (x0 + 112, "#f1ebe0", 2)):                               # two big square ones against the headboard
        st.ball((cx, y1 + 27, zh + 9), 31, m_pillow(kc, sd), "pillows", squash=(1, 0.86, 0.26), shadow=False)
    for (cx, kc, sd) in ((x0 + 40, "#ece6da", 3), (x0 + 110, "#f4efe4", 4)):                               # two to sleep on
        st.ball((cx, y1 + 9, zh + 31), 33, m_pillow(kc, sd), "pillows", squash=(1, 0.30, 0.60), shadow=False)
    st.ball((x0 + 62, y1 + 17, zh + 46), 17, m_pillow(ROSE, 5), "pillows", squash=(1, 0.82, 0.42), shadow=False)
    st.ball((x0 + 97, y1 + 15, zh + 49), 15, m_pillow("#8fa8a0", 6), "pillows", squash=(1, 0.84, 0.44), shadow=False)
    st.ball((x0 + 128, y1 + 12, zh + 52), 12.5, m_pillow("#b9a0c8", 7), "pillows", squash=(1, 0.86, 0.6), shadow=False)
    st.cyl((y1 + 8, zh + 62), 7.5, x0 + 62, x0 + 118, m_pillow_cyl("#e6dccb"), axis="x", name="pillows", shadow=False)        # a bolster
    # ---- a book on the pillow, her place kept with a ribbon
    bx, bz = x0 + 22, zh + 30

    def m_cover(c):
        k = full(c, "#3a4276") * (0.92 + 0.14 * patch(c, 5, 3)[..., None])
        if c.face == "top":
            u, v = c.X - c.box[0], c.Z - c.box[4]
            k = lay(k, "#e8dcb8", rect(u, v, 3.5, 14.5, 5, 10.5, c.fp))
            k = lay(k, "#d0a84a", rect(u, v, 3.5, 14.5, 19, 20.2, c.fp))
        elif c.face in ("front", "left"):
            pages = (c.Y > c.box[2] + 0.6) & (c.Y < c.box[3] - 0.6)
            k = np.where(pages[..., None], col("#eee4cc"), k)
        return k
    st.box(bx, bx + 18, y1 + 17.5, y1 + 21, bz, bz + 25, m_cover, "book", shadow=False)
    st.rope(curve3([(bx + 11, y1 + 19.5, bz + 25), (bx + 12, y1 + 16, bz + 28), (bx + 11, y1 + 13, bz + 31)], 4), 0.5, col("#c8322c"), name="book", min_px=0.6)
    # ---- in the corner behind the bed's head: a tall jar of dried pampas grass
    gx, gz = M.PAMPAS
    st.cyl((gx, gz), 8.5, 0, 44, plain("#e6dccb", 0.06, 8), r1=11.5, name="pampas", foot=True, cap=col("#4a3a30"))
    for k in range(11):
        az = 1.2 + k * 0.57
        blade(st, (gx + math.cos(az) * 3, 43, gz + math.sin(az) * 3), az, 10 + 22 * float(hashf(k, 23)), 86 + 34 * float(hashf(k, 24)), 6 + 16 * float(hashf(k, 25)),
              "pampas", color="#e3d2ae", width=8.5, seed=90 + k, n=6)
    # ---- a little shelf on the end wall over the pillows: two candles and a small plant
    sx0, sx1, sy0, sy1, sz0, sz1 = M.BEDSHELF
    st.box(sx0 - 6, sx1, sy0, sy1, sz0, sz1, wood(PINE, 13, "z", 0.14), "bedshelf", shadow=False)
    candle(st, sx0 - 1, sy1, sz0 + 14, "bedshelf")
    candle(st, sx0 - 1.5, sy1, sz0 + 30, "bedshelf", r=2.8, h=6.2)
    pot(st, sx0 - 1, sz0 + 56, sy1, 4.2, 6, "#e9e2d4", "bedshelf")
    for k in range(7):
        blade(st, (sx0 - 1, sy1 + 6, sz0 + 56), k * 0.9, 6 + (k % 3), 9, 3, "bedshelf", color="#5a9460", width=3.2, seed=70 + k, n=3)
    # ---- two candle lanterns on the floor at its foot
    for i, (lx, lz) in enumerate(M.FOOTLAMPS):
        hh = 30 - 7 * i
        r_ = 8.5 - 1.5 * i
        st.cyl((lx, lz), r_, 0, 1.6, col("#3c3432"), name="footlamps", foot=True)
        for a in range(4):
            ang = a * math.pi / 2 + 0.6
            st.stick((lx + math.cos(ang) * r_ * 0.9, 1.5, lz + math.sin(ang) * r_ * 0.9), (lx + math.cos(ang) * r_ * 0.9, hh, lz + math.sin(ang) * r_ * 0.9), 0.5, col("#3c3432"), "footlamps", min_px=0.6)
        st.cyl((lx, lz), r_, hh, hh + 1.5, col("#3c3432"), name="footlamps", shadow=False)
        st.cyl((lx, lz), 3.0, hh + 1.5, hh + 4.5, col("#3c3432"), r1=0.8, name="footlamps", shadow=False)
        candle(st, lx, 1.6, lz, "footlamps", r=3.4, h=10 - 2 * i, power=1.0)


def m_headboard(c):
    k = col("#d9ccb8") * (0.90 + 0.16 * patch(c, 18, 9)[..., None])
    if c.face == "front":
        u, v = c.X - c.box[0], c.Y - c.box[2]
        cane = (np.mod(u + v, 3.4) < 0.9) | (np.mod(u - v, 3.4) < 0.9)                                    # a caned panel in a pale frame
        inner = rect(u, v, 8, (c.box[1] - c.box[0]) - 8, 30, (c.box[3] - c.box[2]) - 7, c.fp)
        panel = np.where(cane[..., None], col("#c7a878"), col("#8a6a4c"))
        k = k * (1 - inner[..., None]) + panel * inner[..., None]
    return k


def m_pillow(color, seed=0):
    k = col(color)

    def f(c):
        tex = 0.90 + 0.14 * fbm(c.lon * 2.2 + seed, c.lat * 2.6, 13 + seed, 3)
        seam = np.clip(1 - np.abs(np.abs(c.u[:, 2]) - 0.0) / 0.16, 0, 1) * 0.0
        dent = 1 - 0.10 * np.clip(1 - np.hypot(c.u[:, 0], c.u[:, 1] - 0.1) / 0.5, 0, 1)                   # where a head has lain
        return k[None, :] * (tex * dent)[:, None]
    return f


def m_pillow_cyl(color):
    k = col(color)

    def f(c):
        return k[None, :] * (0.88 + 0.14 * fbm(c.along / 5.0, c.ang * 2.0, 4, 2) - 0.10 * (np.mod(c.along, 9.0) < 0.9))[:, None]
    return f


CAN_Y_LOW, CAN_R_LOW = 22.0, 88.0
CAN_OPEN, CAN_HALF = math.radians(118), math.radians(64)


def canopy_bulbs():
    """A short string of the tiny lights wound down each parted edge of the gauze."""
    cx, cy, cz, cr = M.CANOPY
    out = []
    for side in (-1, 1):
        for i in range(9):
            f = 0.10 + 0.10 * i
            y = cy - f * (cy - CAN_Y_LOW)
            r = cr + (CAN_R_LOW - cr) * f + 1.6
            half = CAN_HALF * min(max((f - 0.06) / 0.5, 0), 1) ** 0.6
            a = CAN_OPEN + side * (half + 0.07 + 0.05 * math.sin(i * 2.1))
            out.append((cx + math.cos(a) * r, y + 1.5 * math.sin(i * 1.7), cz + math.sin(a) * r))
    return out


def canopy(st):
    """The gauze: a hoop hung from the roof over the pillows, and the cloth falling from it in a cone, parted
    toward the foot of the bed. It goes on the veil, so the bed and the wall show through it."""
    cx, cy, cz, cr = M.CANOPY
    top = roof(cz) - 1.0
    for a in (0.5, 2.6, 4.7):
        st.stick((cx + math.cos(a) * cr, cy, cz + math.sin(a) * cr), (cx, top - 6, cz), 0.3, col("#e8dcc8"), "canopy", min_px=0.5)
    st.stick((cx, top - 6, cz), (cx, top, cz), 0.35, col("#e8dcc8"), "canopy", min_px=0.5)
    n = 18
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        st.stick((cx + math.cos(a0) * cr, cy, cz + math.sin(a0) * cr), (cx + math.cos(a1) * cr, cy, cz + math.sin(a1) * cr), 0.9, col("#e9dcc6"), "canopy", min_px=0.7)
    v = st.gauze
    y_low, r_low = CAN_Y_LOW, CAN_R_LOW
    C = np.array(st.C)
    open_at, open_half = CAN_OPEN, CAN_HALF
    bl = canopy_bulbs()
    for k in (0, 9):
        st.rope(bl[k:k + 9], 0.2, col("#c8b8a0"), name="canopy", min_px=0.45, flag=2, shade=False)
    for p_ in bl:
        st.ball(p_, 1.1, col("#fff0d0"), "canopy", shadow=False, flag=2, emi=col("#ffd9a0") * 3.0)

    def m_gauze(c):
        f = np.clip((cy - c.Y) / (cy - y_low), 0, 1)                           # 0 at the hoop, 1 at the hem
        da = np.abs(np.angle(np.exp(1j * (c.ang - open_at))))
        half = open_half * np.clip((f - 0.06) / 0.5, 0, 1) ** 0.6
        keep = da > half
        pleat = np.abs(np.sin(c.ang * 15 + 2.0 * fbm(c.ang * 3, f * 3, 3, 2)))
        gathered = np.clip(1 - (da - half) / 0.30, 0, 1) * (f > 0.08)          # the cloth bunches along the parted edges
        a = 0.26 + 0.22 * pleat + 0.30 * gathered + 0.32 * (1 - f) ** 2
        vx, vy, vz = C[0] - c.X, C[1] - c.Y, C[2] - c.Z
        vl = np.sqrt(vx * vx + vy * vy + vz * vz)
        nv = np.abs(c.n[:, 0] * vx + c.n[:, 1] * vy + c.n[:, 2] * vz) / vl
        a = 1 - (1 - np.clip(a, 0, 0.93)) ** (1.0 / np.clip(nv, 0.30, 1.0))    # seen edge-on, more cloth lies along the eye's way
        hem = np.clip(1 - (c.Y - y_low) / 3.0, 0, 1)
        a = np.clip(a + 0.25 * hem, 0, 0.95)
        k = col("#f6efe2")[None, :] * (0.86 + 0.16 * pleat)[:, None]
        return k, None, keep, a.astype(F32)
    v.cyl((cx, cz), r_low, y_low, cy, m_gauze, r1=cr, name="canopy", shadow=False, flag=1, hollow=True, walls="far")
    v.cyl((cx, cz), r_low, y_low, cy, m_gauze, r1=cr, name="canopy", shadow=False, flag=1, hollow=True, walls="near")


# ---------------------------------------------------------------- the left end: palm, salt lamp, diffuser, plants, robe, towels
def m_bark(color, seed=0):
    k = col(color)

    def f(c):
        fur = fbm(c.ang * 7.0 + seed, c.along / 26.0, 5, 3)
        v = 0.62 + 0.62 * fur
        return k[None, :] * v[:, None]
    return f


def m_rings(c):
    r_ = c.rad
    ring = np.sin(r_ * 2.1 + 1.5 * fbm(c.ang * 1.5, r_ / 6.0, 3, 2)) * 0.5 + 0.5
    k = col("#d9b888")[None, :] * (0.80 + 0.24 * ring)[:, None]
    crack = np.clip(1 - np.abs(np.angle(np.exp(1j * (c.ang - 0.8)))) / 0.05, 0, 1) * (r_ > 4)
    return k * (1 - 0.4 * crack[:, None])


def left_end(st):
    # ---- the small palm in the far corner
    px_, pz_ = M.PALM
    pot(st, px_, pz_, 0, 13, 25, "#e6ddd0", "palm", foot=True)
    fr = [(0.25, 62, 78, 24), (0.95, 70, 92, 30), (1.45, 54, 104, 20), (-0.25, 58, 88, 26), (0.62, 44, 112, 12), (1.9, 46, 84, 30),
          (-0.7, 40, 96, 20), (1.15, 30, 118, 8), (0.05, 34, 108, 10), (2.5, 30, 92, 22)]
    for k, (az, ln, rs, dr) in enumerate(fr):
        frond(st, (px_ + math.cos(az) * 3, 24, pz_ + math.sin(az) * 3), az, ln, rs, dr, "palm", color="#4a7c50", pairs=12, leaf=15, seed=k)
    # ---- the salt lamp on its stump
    sx, sz, sr, sh_ = M.STUMP
    st.cyl((sx, sz), sr, 0, sh_, m_bark("#7a5a44", 1), r1=sr * 0.93, name="saltlamp", foot=True, cap=m_rings)
    lx, lz, ly0, ly1 = M.SALTLAMP
    st.cyl((lx, lz), 10.5, ly0, ly0 + 3.2, wood("#8a5a34", 2, "x", 0.2), name="saltlamp", shadow=False)

    def m_salt(seed):
        def f(c):
            n = fbm(c.lon * 2.6 + seed, c.lat * 3.0, 21 + seed, 3)
            facet = np.floor(n * 5) / 5
            core = np.clip(1 - np.abs(c.lat - 0.1) / 1.5, 0, 1)
            e = lerp(col("#d83c10"), col("#ff9238"), np.clip(0.10 + 0.9 * facet * core, 0, 1)[:, None]) * (0.66 + 0.5 * n)[:, None]
            return full(c, "#c8704a"), e * 1.7
        return f
    st.ball((lx, ly0 + 15, lz), 13, m_salt(0), "saltlamp", shadow=False, flag=2, squash=(0.88, 1.12, 0.82))
    st.ball((lx - 5, ly0 + 9, lz + 4), 9.5, m_salt(3), "saltlamp", shadow=False, flag=2, squash=(1, 0.9, 0.9))
    st.ball((lx + 4, ly0 + 23, lz - 2), 7.0, m_salt(5), "saltlamp", shadow=False, flag=2, squash=(0.9, 1.1, 0.9))
    # ---- a smaller stump, and the diffuser on it
    dx, dz, dr, dh = M.STUMP2
    st.cyl((dx, dz), dr, 0, dh, m_bark("#806048", 4), r1=dr * 0.95, name="diffuser", foot=True, cap=m_rings)
    st.cyl((dx, dz), 6.5, dh, dh + 3.5, wood("#b98a58", 3, "x", 0.16), name="diffuser", shadow=False)
    st.ball((dx, dh + 11.5, dz), 8.8, plain("#f2ece2", 0.05, 6), "diffuser", shadow=False, squash=(0.84, 1.05, 0.84))
    st.cyl((dx, dz), 1.5, dh + 19.5, dh + 21.5, col("#d8d0c4"), name="diffuser", shadow=False, cap=col("#5a5a60"))
    # ---- the stand of plants: three steps against the wall, ferns below, ivy from the top
    x0, x1, _, y1, z0, z1 = M.PLANTSTAND
    wd = wood(PINE, 15, "z", 0.16)
    tiers = [(x0 + 4, x1 - 2, 28), (x0 + 2, x1 - 18, 62), (x0, x1 - 32, 96)]
    for (a, b, y) in tiers:
        st.box(a, b, y - 2.4, y, z0, z1, wd, "plants", foot=False)
    for z in (z0 + 1.5, z1 - 1.5):
        st.stick((x1, 0.5, z), (x0 + 4, y1 + 4, z), 1.6, col("#cfa878"), "plants")
        st.stick((x0 + 3, 0.5, z), (x0 + 3, y1 + 4, z), 1.5, col("#cfa878"), "plants")
    st.occ.append((x0, x1 - 6, 0, 96, z0, z1))
    st.feet["plants"] = (x0, x1, z0, z1)
    # the lowest step: a big fern and a snake plant
    fx_, fz_ = x1 - 20, z0 + 16
    pot(st, fx_, fz_, 28, 8.5, 12, "#e9e2d4", "plants")
    for k in range(17):
        az = k * 0.72 + 0.2
        blade(st, (fx_ + math.cos(az) * 2, 39, fz_ + math.sin(az) * 2), az, 27 + 12 * float(hashf(k, 3)), 17 + 7 * float(hashf(k, 4)), 18 + 12 * float(hashf(k, 5)), "plants", color="#4f8a52", width=7.0, seed=k, n=6)
    gx_, gz_ = x1 - 22, z1 - 14
    pot(st, gx_, gz_, 28, 7.5, 11, "#c98a6a", "plants")
    for k in range(7):
        az = k * 0.9
        blade(st, (gx_ + math.cos(az) * 2.5, 38, gz_ + math.sin(az) * 2.5), az, 5 + 2 * (k % 2), 26 + 4 * (k % 3), 0, "plants", color="#5c8c5a", width=4.4, seed=20 + k, n=3)
    # the middle step: a drooping fern
    mx_, mz_ = x0 + 20, (z0 + z1) / 2
    pot(st, mx_, mz_, 62, 8, 11, "#8fa8a0", "plants")
    for k in range(18):
        az = k * 0.61 + 0.1
        blade(st, (mx_ + math.cos(az) * 2, 72, mz_ + math.sin(az) * 2), az, 25 + 12 * float(hashf(k, 13)), 12 + 6 * float(hashf(k, 14)), 24 + 16 * float(hashf(k, 15)), "plants", color="#5a9a58", width=6.4, seed=30 + k, n=6)
    # the top step: ivy, trailing down both ends and the front
    tx_, tz_ = x0 + 12, (z0 + z1) / 2
    pot(st, tx_, tz_, 96, 8, 10, "#e9e2d4", "plants")
    for k in range(8):
        az = k * 0.8
        blade(st, (tx_ + math.cos(az) * 2, 105, tz_ + math.sin(az) * 2), az, 9, 7, 5, "plants", color="#4f8a58", width=5, seed=60 + k, n=3)
    for k, (ddx, ddz, ln) in enumerate(((8, 6, 58), (7, -5, 44), (3, 9, 70), (4, -9, 36), (9, 1, 30), (2, 12, 50), (1, -12, 62))):
        strand(st, (tx_ + ddx, 104, tz_ + ddz), ln, "plants", seed=11 + k, drift=(ddx * 1.2, ddz * 0.9), swing=2.4)
    # ---- her robe on its hook, and her slippers set side by side under it
    rz0, rz1, ry0, ry1 = M.ROBE
    st.stick((0.5, ry1 + 2, (rz0 + rz1) / 2), (7, ry1 + 3.5, (rz0 + rz1) / 2), 0.9, col("#c9a070"), "robe")

    zc = (rz0 + rz1) / 2

    def m_robe(c):
        f = fbm(c.Z / 4.2, c.Y / 46.0, 5, 3)                                    # long soft folds
        k = col("#f3ede3")[None, :] * (0.76 + 0.34 * f)[:, None]
        w = c.Z - zc
        lap = np.clip(1 - np.abs(w - (ry1 - c.Y) * 0.045) / np.maximum(c.fp, 0.6), 0, 1) * (c.Y < ry1 - 26)      # where one front crosses the other
        k = k * (1 - 0.28 * lap[:, None])
        collar = (np.abs(np.abs(w) - (ry1 - 8 - c.Y) * 0.42) < 1.7) & (c.Y > ry1 - 34)
        k = np.where(collar[:, None], k * 0.78, k)
        belt = band(c.Y, ry0 + 50, ry0 + 55.5, c.fp)
        k = k * (1 - 0.18 * belt[:, None])
        tail = band(w, 4, 7.5, c.fp) * band(c.Y, ry0 + 20, ry0 + 51, c.fp)
        k = k * (1 - 0.18 * tail[:, None])
        hem = np.clip((ry0 + 4 - c.Y) / 4.0, 0, 1)
        return k * (1 - 0.18 * hem[:, None]), None, c.Y > ry0
    st.ball((5.0, ry0 + 30, zc), 1.0, m_robe, "robe", squash=(7.0, ry1 - ry0 - 26, 21.5))
    for sg in (-1, 1):                                                         # the sleeves hang at its sides
        st.ball((4.5, ry0 + 58, zc + sg * 21.5), 1.0, m_robe, "robe", shadow=False, squash=(4.6, 38, 6.2))
    sx0, sx1, sz0, sz1 = M.SLIPPERS
    for i in range(2):
        xc = sx0 + 6 + i * 14
        zc = (sz0 + sz1) / 2
        st.ball((xc, 2.4, zc), 1.0, plain("#e896a8", 0.1, 3, i), "slippers", shadow=False, squash=(5.6, 2.8, 12.5), foot=True)       # the sole
        st.ball((xc, 4.6, zc - 5.5), 1.0, plain("#f8ece8", 0.1, 3, i + 2), "slippers", shadow=False, squash=(5.9, 4.4, 7.0))         # the soft toe
    # ---- a candle in a tall glass on the floor between the plants and the towels
    cxf, czf = M.FLOORCANDLE
    st.cyl((cxf, czf), 6.2, 0, 1.2, col("#4a3c36"), name="floorcandle", foot=True)
    candle(st, cxf, 1.2, czf, "floorcandle", r=4.6, h=15)
    # ---- the basket of rolled towels
    bx_, bz_, br, bh = M.BASKET
    st.cyl((bx_, bz_), br * 0.86, 0, bh, m_weave("#c39c68", 1), r1=br, name="towels", foot=True, cap=col("#5a4636"))
    rolls = [(0, 0, "#f3eee4"), (11, 5, "#dfe7df"), (-10, 7, "#f3eee4"), (3, -12, SAGE), (-8, -9, "#ead0cc"), (13, -8, "#f3eee4"), (2, 13, "#e9dcc2")]
    for k, (ddx, ddz, kc) in enumerate(rolls):
        st.cyl((bx_ + ddx, bz_ + ddz), 7.6, bh - 12, bh + 5 + 2.5 * float(hashf(k, 3)), m_towel(kc, k), name="towels", shadow=False, cap=m_towel_end(kc, k))


def m_towel(color, seed):
    k = col(color)

    def f(c):
        return k[None, :] * (0.84 + 0.16 * fbm(c.ang * 3 + seed, c.along / 3.0, 9, 2))[:, None]
    return f


def m_towel_end(color, seed):
    k = col(color)

    def f(c):
        sp = np.sin(c.rad * 3.6 + c.ang + seed) * 0.5 + 0.5                    # the roll, seen end-on: a spiral
        return k[None, :] * (0.72 + 0.30 * sp)[:, None]
    return f


# ---------------------------------------------------------------- on the floor, and under the slope
def floor_things(st):
    x0, x1, z0, z1 = M.MAT

    def m_mat(c):
        k = col("#6a9084") * (0.92 + 0.12 * fbm(c.X / 14, c.Z / 14, 6, 2)[..., None])
        if c.face == "top":
            u, v, fp = c.X - x0, c.Z - z0, c.fp
            w, l = x1 - x0, z1 - z0
            tex = (np.mod(u, 1.6) < 0.8) ^ (np.mod(v, 1.6) < 0.8)
            k = k * (0.965 + 0.05 * tex[..., None])
            bd = rect(u, v, 3.2, w - 3.2, 3.2, l - 3.2, fp) - rect(u, v, 4.2, w - 4.2, 4.2, l - 4.2, fp)
            k = lay(k, "#b9d2c6", np.clip(bd, 0, 1) * 0.7)
            # a lotus printed at the far end
            cu, cv = w / 2, 26.0
            d, a = np.hypot(u - cu, v - cv), np.arctan2(v - cv, u - cu)
            pet = 8.5 + 4.5 * np.cos(a * 8)
            lot = np.clip((pet - d) / fp + 0.5, 0, 1) * (1 - np.clip((3.2 - d) / fp + 0.5, 0, 1))
            k = lay(k, "#b9d2c6", lot * 0.75)
            wear = np.clip((fbm(u / 20, v / 30, 9, 2) - 0.55) * 3, 0, 1)
            k = k * (1 - 0.10 * wear[..., None])
        return k
    st.box(x0, x1, 0, 1.3, z0, z1, m_mat, "mat", shadow=False)
    st.feet["mat"] = (x0, x1, z0, z1)


def m_lantern(seed):
    def f(c):
        rib = np.abs(np.sin(c.lat * 11.0))                                      # the paper is stretched over thin hoops
        seam = np.clip(1 - rib / 0.16, 0, 1)
        low = np.clip(0.62 - 0.38 * np.sin(c.lat), 0, 1)                        # the little lamp is low inside it
        pap = 0.88 + 0.14 * fbm(c.lon * 2 + seed, c.lat * 2, 5, 2)
        e = lerp(col("#f0965a"), col("#ffdca8"), np.clip(low * 1.25 - 0.25, 0, 1)[:, None]) * (low * pap * (1 - 0.22 * seam))[:, None] * 2.5
        return full(c, "#f2dcc0"), e
    return f


def overhead(st):
    strings(st)
    for i, (x, z, y, r) in enumerate(M.LANTERNS):
        st.ball((x, y, z), r, m_lantern(i), "lantern", shadow=False, flag=2, squash=(1, 0.90, 1))
        st.cyl((x, z), r * 0.30, y + r * 0.86, y + r * 0.90 + 1.2, col("#c8b08a"), name="lantern", shadow=False)
        st.stick((x, y + r * 0.9, z), (x, roof(z) - 1, z), 0.28, col("#d8ccb8"), "lantern", min_px=0.5)
        st.stick((x, y - r * 0.88, z), (x, y - r * 0.88 - 9, z), 0.9, col(ROSE if i != 1 else "#c9a25a"), "lantern", r1=0.35, min_px=0.6)   # a tassel
    # ---- a hanging plant, from the rafter by the round window
    hx, hz, hy = M.HANGPLANT
    topy = roof(hz) - RAFT_D * Q
    st.stick((hx, hy + 36, hz), (hx, topy, hz), 0.3, col("#e0d4c0"), "hangplant", min_px=0.5)
    for a in (0.3, 2.4, 4.5):
        st.stick((hx + math.cos(a) * 10.5, hy, hz + math.sin(a) * 10.5), (hx, hy + 36, hz), 0.3, col("#e0d4c0"), "hangplant", min_px=0.5)
    st.cyl((hx, hz), 8.0, hy - 13, hy, plain("#e9e2d4", 0.06), r1=11, name="hangplant", shadow=True, cap=col("#3a2a20"))
    for k in range(12):
        az = k * 0.55
        blade(st, (hx + math.cos(az) * 3, hy, hz + math.sin(az) * 3), az, 12 + 5 * (k % 3), 8, 9 + 3 * (k % 2), "hangplant", color="#5a9a5c", width=5.5, seed=80 + k, n=4)
    for k, (ddx, ddz, ln) in enumerate(((9, 4, 46), (-8, 6, 34), (4, 9, 58), (-3, -9, 28), (10, -4, 22), (-9, -3, 40), (1, 11, 30))):
        strand(st, (hx + ddx, hy - 1, hz + ddz), ln, "hangplant", seed=31 + k, drift=(ddx * 0.5, ddz * 0.5), swing=2.2, color="#58985a")
    # ---- a small weaving on the right end wall, toward the front
    def m_weaving(c):
        u, v = c.Z - 286, 232 - c.Y
        k = np.zeros(c.Z.shape + (3,), dtype=F32) + col("#eadfca")
        bands_ = [(8, 14, ROSE), (20, 23, "#c9a25a"), (30, 40, "#8fa8a0"), (46, 49, ROSE)]
        for a, b, kc in bands_:
            k = np.where(((v > a) & (v < b))[..., None], col(kc), k)
        k = k * (0.86 + 0.18 * (np.mod(u, 2.0) < 1.0))[..., None]
        tri = v < 56 + 16 * (1 - np.abs(np.mod(u, 12.0) - 6.0) / 6.0)          # a fringe cut in points
        return k, None, tri & (v > 0)
    st.poly([(M.W - 1.0, 232, 286), (M.W - 1.0, 232, 334), (M.W - 1.0, 158, 334), (M.W - 1.0, 158, 286)], m_weaving, "weaving")
    st.stick((M.W - 1.5, 233, 283), (M.W - 1.5, 233, 337), 1.0, col("#b88a58"), "weaving")


# ---------------------------------------------------------------- the foreground (front plane): hatch, notice, tea, pouf
GL = {
    "A": [[(0, 0), (2, 6), (4, 0)], [(0.8, 2.2), (3.2, 2.2)]],
    "C": [[(4, 5), (3, 6), (1.2, 6), (0, 4.8), (0, 1.2), (1.2, 0), (3, 0), (4, 1)]],
    "D": [[(0, 0), (0, 6), (2.2, 6), (4, 4.4), (4, 1.6), (2.2, 0), (0, 0)]],
    "E": [[(4, 6), (0, 6), (0, 0), (4, 0)], [(0, 3.1), (3, 3.1)]],
    "F": [[(4, 6), (0, 6), (0, 0)], [(0, 3.1), (3, 3.1)]],
    "H": [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3.1), (4, 3.1)]],
    "I": [[(2, 0), (2, 6)]],
    "K": [[(0, 0), (0, 6)], [(4, 6), (0, 2.5)], [(1.5, 3.6), (4, 0)]],
    "N": [[(0, 0), (0, 6), (4, 0), (4, 6)]],
    "O": [[(1.2, 0), (0, 1.3), (0, 4.7), (1.2, 6), (2.8, 6), (4, 4.7), (4, 1.3), (2.8, 0), (1.2, 0)]],
    "R": [[(0, 0), (0, 6), (2.6, 6), (4, 5), (4, 3.9), (2.6, 3), (0, 3)], [(2.2, 3), (4, 0)]],
    "S": [[(4, 5), (3, 6), (1, 6), (0, 5), (0, 3.9), (1, 3.1), (3, 2.9), (4, 2.1), (4, 1), (3, 0), (1, 0), (0, 1)]],
    "T": [[(0, 6), (4, 6)], [(2, 6), (2, 0)]],
    "V": [[(0, 6), (2, 0), (4, 6)]],
    "W": [[(0, 6), (1, 0), (2, 4.2), (3, 0), (4, 6)]],
    "1": [[(1, 4.8), (2.4, 6), (2.4, 0)]],
    "2": [[(0, 4.8), (1, 6), (3, 6), (4, 4.9), (4, 3.8), (0, 0), (4, 0)]],
    "3": [[(0, 5), (1, 6), (3, 6), (4, 5), (4, 3.9), (3, 3.1), (1.6, 3.1)], [(3, 3.1), (4, 2.2), (4, 1), (3, 0), (1, 0), (0, 1)]],
    ".": [[(0.6, 0.1), (0.6, 0.5)]],
}
ADV = {"I": 1.9, "1": 3.4, ".": 1.6, " ": 2.6, "W": 5.4, "N": 5.0, "H": 5.0, "O": 5.0, "D": 5.0, "C": 4.9}


def notice_texture(res=8):
    """Her notice, in her best lettering: -> (picture, (wide, high) in cm). `res` pixels to the centimetre."""
    x0, x1, y0, y1, _ = M.SIGN
    wide, high = x1 - x0, y1 - y0
    ss = 3
    Wp, Hp = int(wide * res), int(high * res)
    im = Image.new("RGB", (Wp * ss, Hp * ss), (243, 234, 212))
    d = ImageDraw.Draw(im)
    k = res * ss

    def P(x, y):
        return (x * k, (high - y) * k)

    def pen(pts, color, width):
        q = [P(x, y) for x, y in pts]
        wd = max(1, int(round(width * k)))
        d.line(q, fill=color, width=wd, joint="curve")
        for (x, y) in q:
            d.ellipse([x - wd / 2, y - wd / 2, x + wd / 2, y + wd / 2], fill=color)

    def words(text, yb, cap, color, width, x_left=None, track=1.0, squeeze=0.80):
        unit = cap / 6.0
        sx = unit * squeeze
        total = sum(ADV.get(ch, 4.9) for ch in text) * sx * track
        x = (wide - total) / 2 if x_left is None else x_left
        for ch in text:
            adv = ADV.get(ch, 4.9) * sx * track
            if ch in GL:
                off = 0.0 if ch not in ("I", "1", ".") else {"I": -1.1, "1": -0.5, ".": 0.0}[ch]
                for stroke in GL[ch]:
                    pen([(x + (px + off) * sx, yb + py * unit) for px, py in stroke], color, width)
            x += adv
        return x
    ink, rose, red = (44, 48, 96), (190, 110, 112), (200, 44, 40)
    # a wooden frame, a ruled border
    fw = 3.0
    d.rectangle([0, 0, Wp * ss, Hp * ss], fill=(176, 132, 88))
    d.rectangle([fw * k, fw * k, (wide - fw) * k, (high - fw) * k], fill=(244, 236, 214))
    d.rectangle([(fw + 1.6) * k, (fw + 1.6) * k, (wide - fw - 1.6) * k, (high - fw - 1.6) * k], outline=rose, width=max(1, int(0.55 * k)))
    words("THE RETREAT", high - 20.6, 10.4, ink, 1.32, track=1.06, squeeze=0.70)
    yl = high - 25.0                                                           # a flourish under the title: a line, a leaf at each end
    pen([(13, yl), (wide - 13, yl)], rose, 0.6)
    for sx_ in (-1, 1):
        cxl = wide / 2 + sx_ * (wide / 2 - 11)
        d.ellipse([P(cxl - 2.2, yl + 1.5)[0], P(cxl - 2.2, yl + 1.5)[1], P(cxl + 2.2, yl - 1.5)[0], P(cxl + 2.2, yl - 1.5)[1]], fill=(120, 160, 120))
    d.ellipse([P(wide / 2 - 1.6, yl + 1.6)[0], P(wide / 2 - 1.6, yl + 1.6)[1], P(wide / 2 + 1.6, yl - 1.6)[0], P(wide / 2 + 1.6, yl - 1.6)[1]], fill=rose)
    cap, xl = 7.2, 8.6
    for i, text in enumerate(("SHOES OFF", "VOICES DOWN", "NO CHICKENS")):
        yb = high - 37.2 - i * 11.7
        xe = words(f"{i + 1}.", yb, cap, red, 1.15, x_left=xl)
        words(text, yb, cap, ink, 1.12, x_left=xe + 1.5, track=1.07)
    # under the last rule, by way of illustration: a chicken, crossed out
    cxk, cyk, rk = wide - 12.5, 9.2, 4.5
    d.ellipse([P(cxk - 2.6, cyk + 1.0)[0], P(cxk - 2.6, cyk + 1.0)[1], P(cxk + 2.2, cyk - 2.8)[0], P(cxk + 2.2, cyk - 2.8)[1]], fill=(250, 246, 236), outline=ink, width=max(1, int(0.3 * k)))
    d.ellipse([P(cxk + 0.6, cyk + 3.0)[0], P(cxk + 0.6, cyk + 3.0)[1], P(cxk + 3.2, cyk + 0.6)[0], P(cxk + 3.2, cyk + 0.6)[1]], fill=(250, 246, 236), outline=ink, width=max(1, int(0.3 * k)))
    d.polygon([P(cxk + 3.1, cyk + 2.0), P(cxk + 4.6, cyk + 1.6), P(cxk + 3.1, cyk + 1.2)], fill=(226, 150, 40))
    d.polygon([P(cxk + 1.2, cyk + 3.0), P(cxk + 1.9, cyk + 4.2), P(cxk + 2.6, cyk + 3.0)], fill=red)
    d.ellipse([P(cxk - rk, cyk + rk)[0], P(cxk - rk, cyk + rk)[1], P(cxk + rk, cyk - rk)[0], P(cxk + rk, cyk - rk)[1]], outline=red, width=max(1, int(1.0 * k)))
    pen([(cxk - rk * 0.70, cyk + rk * 0.70), (cxk + rk * 0.70, cyk - rk * 0.70)], red, 1.0)
    pen([(8.6, 8.4), (wide - 21, 8.4)], rose, 0.5)
    return np.asarray(im.resize((Wp, Hp), Image.LANCZOS), dtype=F32) / 255, (wide, high)


_NOTICE = {}


def m_notice(c):
    if "tex" not in _NOTICE:
        _NOTICE["tex"] = notice_texture()
    tex, (wide, high) = _NOTICE["tex"]
    res = tex.shape[1] / wide
    k = sample(tex, np.clip(c.U, 0, wide - 0.01) * res, np.clip(high - c.V, 0.01, high) * res - 0.5)
    return k * (0.97 + 0.05 * fbm(c.U / 14, c.V / 14, 5, 2)[..., None])


def front(st, G="front"):
    hx0, hx1, hz0, hz1 = M.HATCH
    rh = M.RAIL_H
    wd = wood(PINE, 21, "z", 0.16)
    # ---- the well of the hatch, the landing far below, the top of the ladder
    def m_well(c):
        along = c.X if c.face in ("back", "front") else c.Z
        k = col("#c8a478") * (0.86 + 0.2 * fbm(along / 3.0, c.Y / 30.0, 6, 3)[..., None])
        k = k * (1 - 0.25 * (np.mod(c.Y + 34, 11.5) < 0.8))[..., None]
        return k, None, np.full(c.X.shape, c.face != "bottom")                # it has no floor: the landing is below

    def m_below(c):
        if c.face == "bottom":                                                # the landing's runner, a long way down
            return lerp(col("#7a4034"), col("#8a2a26"), band(c.X, hx0 + 20, hx1 - 10, 2.0)[..., None])
        along = c.X if c.face in ("back", "front") else c.Z
        st_ = (np.mod(along, 18.0) < 9.0)
        return np.where(st_[..., None], col("#6f8f86"), col("#86a79c")) * (0.9 + 0.1 * (c.Y > -160))[..., None]
    st.box(hx0, hx1, -34, 0.0, hz0, hz1, m_well, "well", "back", inside=True, shadow=False, flag=2)
    st.box(hx0 - 150, hx1 + 150, -285, -34, hz0 - 260, hz1 + 140, m_below, "well", "back", inside=True, shadow=False, flag=2)
    lz0, lz1 = hz0 + 3, hz0 + 3 + 96                                           # the ladder leans down and toward us
    xa, xb = hx0 + 38, hx1 - 38
    for x in (xa, xb):
        st.stick((x, 26, lz0 - 8), (x, -285, lz1 + 2), 2.7, col("#d2ac78"), "hatch", G)
        st.ball((x, 27.5, lz0 - 8.5), 3.2, col("#d8b480"), "hatch", G, shadow=False)
    for i in range(1, 9):
        y = 8 - i * 27
        z = lz0 + (26 - y) / 311.0 * 98 - 8
        st.box(xa, xb, y - 1.6, y + 1.6, z - 4.5, z + 4.5, wood("#d8b684", 30 + i, "x", 0.14), "hatch", G, shadow=False)
    # ---- the rail round it: posts at the corners, a top rail and a middle rail on three sides (open where you step off)
    for (px_, pz_) in ((hx0 - 3, hz0 - 3), (hx1 + 3, hz0 - 3), (hx0 - 3, hz1 + 3), (hx1 + 3, hz1 + 3)):
        st.box(px_ - 3, px_ + 3, 0, rh, pz_ - 3, pz_ + 3, wd, "hatch", G, foot=True)
        st.ball((px_, rh + 2.2, pz_), 3.8, plain("#dcb888", 0.08), "hatch", G, shadow=False)
    for y in (rh - 6, rh * 0.48):
        st.box(hx0 - 5.4, hx0 - 0.6, y - 2.2, y + 2.2, hz0, hz1, wd, "hatch", G)
        st.box(hx1 + 0.6, hx1 + 5.4, y - 2.2, y + 2.2, hz0, hz1, wd, "hatch", G)
        st.box(hx0, hx1, y - 2.2, y + 2.2, hz1 + 0.6, hz1 + 5.4, wd, "hatch", G)
    st.box(hx0 - 7, hx1 + 7, 0, 1.2, hz0 - 7, hz0, plain(TRIM, 0.06), "hatch", G, shadow=False)            # the painted edge of the opening
    # ---- her notice, on a little easel beside it
    x0, x1, y0, y1, z = M.SIGN
    lean = 13.0
    st.poly([(x0, y0, z + 2), (x1, y0, z + 2), (x1, y1, z + 2 - lean), (x0, y1, z + 2 - lean)], m_notice, "rules", G, flag=2)
    st.box(x0 - 2, x1 + 2, y0 - 3.2, y0, z - 1, z + 4.5, wd, "easel", G, shadow=False)
    xm = (x0 + x1) / 2

    def zb(y, back=2.6):                                                       # the easel's legs lie just behind the board
        return z + 2 - lean * (y - y0) / (y1 - y0) - back
    for sgn in (-1, 1):
        st.stick((xm + sgn * (x1 - x0) * 0.56, 0.3, zb(0)), (xm + sgn * 9, y1 + 1.5, zb(y1 + 1.5)), 1.5, col("#c9a070"), "easel", G)
    st.stick((xm, 0.3, z - 44), (xm, y1 + 1.5, zb(y1 + 1.5)), 1.4, col("#b89060"), "easel", G)
    st.stick((xm - 8, y1 + 3.0, z - lean + 8), (xm + 8, y1 + 3.0, z - lean + 8), 1.2, col("#c9a25a"), "easel", G, flag=2, emi=col("#ffd9a0") * 0.5)   # its little picture-light
    st.stick((xm, y1 + 0.5, zb(y1)), (xm, y1 + 3.0, z - lean + 8), 0.5, col("#8a6a40"), "easel", G, min_px=0.6)
    st.occ.append((x0, x1, 0, y1, z - lean, z + 3))
    st.feet["rules"] = (x0 + 3, x1 - 3, z - 2, z + 9)
    # ---- shoes off: hers, side by side on a little mat, just beyond the notice
    mx0, mz0 = x1 + 14, 520
    st.box(mx0, mx0 + 40, 0, 1.0, mz0, mz0 + 36, lambda c: col("#8a7a90") * (0.86 + 0.2 * ((np.mod(c.X + c.Z, 3.0) < 1.5) ^ (np.mod(c.X - c.Z, 3.0) < 1.5)))[..., None], "shoes", G, shadow=False)
    for i in range(2):
        xs = mx0 + 9 + i * 13
        st.ball((xs, 4.6, mz0 + 18), 5.6, plain("#f1ece4", 0.06, 3, i), "shoes", G, shadow=False, squash=(1.0, 0.86, 2.3), foot=True)
        st.ball((xs, 7.2, mz0 + 9), 5.0, plain("#f1ece4", 0.06, 3, i), "shoes", G, shadow=False, squash=(1.0, 0.92, 1.25))
        st.cyl((xs, mz0 + 9), 3.4, 9.6, 11.4, col("#3a3440"), name="shoes", grp=G, shadow=False, cap=col("#2a2630"))
        st.box(xs - 3.2, xs + 3.2, 7.2, 8.0, mz0 + 16, mz0 + 24, col(ROSE), "shoes", G, shadow=False)
    # ---- a flat floor cushion with her tea tray on it
    tx0, tx1, tz0, tz1 = M.TEA

    def m_square(c):
        k = col(INDIGO) * (0.9 + 0.16 * fbm(c.X / 3.0, c.Z / 3.0 + c.Y / 2, 7, 2)[..., None])
        if c.face == "top":
            u, v = c.X - tx0, c.Z - tz0
            w, l = tx1 - tx0, tz1 - tz0
            e = np.minimum(np.minimum(u, w - u), np.minimum(v, l - v))
            k = k * (0.78 + 0.22 * np.clip(e / 7.0, 0, 1))[..., None]
            sash = (np.abs(np.mod(u + v, 15.0) - 7.5) < 0.9) | (np.abs(np.mod(u - v, 15.0) - 7.5) < 0.9)       # stitched in white, as she saw in a book
            k = np.where((sash & (e > 5))[..., None], k * 0.5 + col("#e8e0d0") * 0.5, k)
        else:
            k = k * (0.78 + 0.22 * np.clip(c.Y / 6.0, 0, 1))[..., None]
        return k
    st.box(tx0, tx1, 0, 11, tz0, tz1, m_square, "tea", G, foot=True)
    cx_, cz_ = (tx0 + tx1) / 2, (tz0 + tz1) / 2 - 4
    st.cyl((cx_, cz_), 27, 11, 13.2, wood("#b98a58", 8, "x", 0.16), name="tea", grp=G, shadow=False, cap=lambda c: col("#c79a66")[None, :] * (0.86 + 0.2 * fbm(c.X / 2.4, c.Z / 30.0, 4, 2))[:, None] * (1 - 0.3 * (c.rad > 24.5))[:, None])
    st.ball((cx_ - 7, 21.5, cz_ - 3), 9.0, plain("#4a6f78", 0.10, 4, 2), "tea", G, shadow=False, squash=(1, 0.80, 1))          # the teapot
    st.cyl((cx_ - 7, cz_ - 3), 4.4, 27.6, 29.2, col("#3f6068"), name="tea", grp=G, shadow=False)
    st.ball((cx_ - 7, 30.6, cz_ - 3), 1.5, col("#c9a25a"), "tea", G, shadow=False)
    st.stick((cx_ + 0.5, 21, cz_ - 3), (cx_ + 8, 26.5, cz_ - 3), 1.4, col("#4a6f78"), "tea", G, r1=0.9)                         # its spout
    st.rope(curve3([(cx_ - 13.5, 27, cz_ - 3), (cx_ - 12, 35, cz_ - 3), (cx_ - 2, 35, cz_ - 3), (cx_ - 0.5, 27, cz_ - 3)], 5), 0.6, col("#8a6a40"), name="tea", grp=G, min_px=0.7)   # a cane handle
    st.cyl((cx_ + 12, cz_ + 9), 3.0, 13.2, 18.4, plain("#efe6d6", 0.05), r1=4.4, name="tea", grp=G, shadow=False, cap=col("#9a6a3a"))  # her cup, with tea in it
    st.cyl((cx_ + 1, cz_ + 14), 5.4, 13.2, 14.0, col("#efe6d6"), name="tea", grp=G, shadow=False)                               # a saucer with two biscuits
    st.cyl((cx_ + 0, cz_ + 13.5), 2.3, 14.0, 14.9, col("#d0a060"), name="tea", grp=G, shadow=False)
    st.cyl((cx_ + 2.6, cz_ + 15), 2.3, 14.0, 15.3, col("#c8944e"), name="tea", grp=G, shadow=False)
    # ---- the pouf, a folded blanket on it, three library books beside it
    px_, pz_, pr, ph = M.POUF

    def m_knit(c):
        rows = np.sin(c.lat * 30.0) * 0.5 + 0.5
        st_ = np.sin(c.lon * 34.0 + np.floor(c.lat * 30.0 / math.pi) * 1.57) * 0.5 + 0.5
        v = 0.74 + 0.20 * rows * (0.45 + 0.55 * st_) + 0.10 * (fbm(c.lon * 3, c.lat * 3, 9, 2) - 0.5)
        return col("#d9cab0")[None, :] * v[:, None]
    st.ball((px_, ph * 0.52, pz_), pr, m_knit, "pouf", G, squash=(1, ph * 0.54 / pr, 1), foot=True)

    def m_blanket(c):
        u, v = c.X - c.box[0], c.Z - c.box[4]
        plaid = ((np.mod(u, 9.0) < 2.4) * 0.5 + (np.mod(v, 9.0) < 2.4) * 0.5)
        k = lerp(col("#b9788a"), col("#f0e2d4"), (plaid * 0.8)[..., None]) * (0.9 + 0.14 * fbm(c.X / 6, c.Z / 6, 4, 2)[..., None])
        if c.face != "top":
            fold = (np.mod(c.Y - c.box[2], 2.9) < 0.6)
            k = lerp(col("#b9788a"), col("#f0e2d4"), ((np.mod(c.X + c.Z, 9.0) < 2.4) * 0.6)[..., None]) * (0.78 - 0.2 * fold)[..., None]
        return k
    st.box(px_ - 22, px_ + 20, ph + 0.5, ph + 9.5, pz_ - 20, pz_ + 16, m_blanket, "pouf", G, shadow=False)
    for i, (kc, dh) in enumerate((("#3f86b8", 3.6), ("#e8a53a", 2.8), ("#c23a36", 3.2))):
        yb = sum(h for _, h in ((0, 3.6), (0, 2.8), (0, 3.2))[:i])
        st.box(px_ + 50 + i * 1.5, px_ + 72 - i, yb, yb + dh, pz_ - 8 + i * 1.5, pz_ + 22 - i, m_flatbook(kc), "books", G, shadow=False, foot=(i == 0))


def everything(st):
    st.gauze = st.veil()
    far_wall(st)
    desk(st)
    bed(st)
    left_end(st)
    floor_things(st)
    overhead(st)
    canopy(st)
    front(st)

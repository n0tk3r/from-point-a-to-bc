"""Everything that stands, hangs or lies in Dad's study, built in the room's own centimetres (home_study.py).

Each function puts one group of things on the Stage (home_study_kit.Stage): boxes, rods, round things and flat
sheets, each with a material that paints it in ITS OWN measurements. All measurements come from the model
(home_study_model.py), so the skeleton, the picture and the layout agree."""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, lerp, sample
import home_study_model as M
from home_study_kit import col, mixc, vnoise, fbm, hashf, grad_of, lines_aa, band_aa, Attic

ATTIC = Attic(M.W, M.KNEE, M.RIDGE, rafter=(30.0, 60.0, 2.8, 12.0, 1115.0))
SLOPE = (M.RIDGE - M.KNEE) / (M.W / 2)                 # rise of the roof per cm across

# ---------------------------------------------------------------- the colors of things (before any light falls on them)
WALL = "#84ac98"            # sage plaster
WALL2 = "#7ea492"           # the boarded low walls, the same paint a little dirtier
TRIM = "#8a5a34"            # skirting and plates
TRIMW = "#e6dcc2"           # painted window frame, door
ROOFB = "#d9cdb0"           # the boards of the roof, painted cream long ago
RAFT = "#7d5030"            # rafters and ridge
FLOOR_A, FLOOR_B, FLOOR_C = "#b67c46", "#d09a5a", "#a26c3a"
DESK_C = "#7c4a26"
BEIGE = "#d6cdb0"
PAPER = "#f1ead6"


def roof_y(X):
    return M.KNEE + SLOPE * (M.W / 2 - abs(X - M.W / 2))


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


def rm(u, lo, hi, fp):
    """A soft-edged band lo..hi along u (fp: cm per ray)."""
    return np.clip((u - lo) / fp + 0.5, 0, 1) * np.clip((hi - u) / fp + 0.5, 0, 1)


def rect(u, v, u0, u1, v0, v1, fp):
    return rm(u, u0, u1, fp) * rm(v, v0, v1, fp)


def disc(u, v, cu, cv, r, fp):
    return np.clip((r - np.hypot(u - cu, v - cv)) / fp + 0.5, 0, 1)


def lay(base, color, m):
    return base * (1 - m[..., None]) + col(color) * m[..., None]


def curve3(points, steps=10):
    """A smooth line through a few places in the room (Catmull-Rom)."""
    p = [np.asarray(q, dtype=float) for q in points]
    p = [p[0] * 2 - p[1]] + p + [p[-1] * 2 - p[-2]]
    out = []
    for i in range(1, len(p) - 2):
        for s in range(steps):
            t = s / steps
            q = 0.5 * ((2 * p[i]) + (-p[i - 1] + p[i + 1]) * t + (2 * p[i - 1] - 5 * p[i] + 4 * p[i + 1] - p[i + 2]) * t * t
                       + (-p[i - 1] + 3 * p[i] - 3 * p[i + 1] + p[i + 2]) * t ** 3)
            out.append(tuple(float(v) for v in q))
    out.append(tuple(float(v) for v in p[-2]))
    return out


# ---------------------------------------------------------------- the shell
def m_floor(c):
    X, Z = c.X, c.Z
    gX, gZ = grad_of(X) * c.ss, grad_of(Z) * c.ss
    bw = 12.0
    ib = np.floor(X / bw)
    Lb = 140 + 150 * hashf(ib, 5)
    zj = (Z + 400 * hashf(ib, 9)) / Lb
    seg = np.floor(zj)
    tn = hashf(ib * 37 + seg, 11)
    base = lerp(col(FLOOR_A), col(FLOOR_B), tn[..., None])
    base = lerp(base, col(FLOOR_C), ((hashf(ib * 13 + seg, 4) > 0.78) * 0.8)[..., None])
    gr = fbm(X / 2.2, Z / 60.0, 31, 3)
    base = base * (0.84 + 0.32 * gr[..., None])
    wear = fbm(X / 90, Z / 120, 8, 3)                                        # where feet have taken the varnish off
    path = np.exp(-((X - 330) / 150.0) ** 2) * np.clip((Z - 60) / 200, 0, 1)
    w = np.clip((wear - 0.52) * 2.2 + path * 0.35, 0, 1)
    base = lerp(base, base * col("#f0e2cc") * 1.1, (w * 0.42)[..., None])
    seam = lines_aa(X, bw, 1.0, gX)
    dz = np.abs(zj - np.round(zj)) * Lb
    butt = np.clip(1.0 - dz / gZ, 0, 1) * np.clip((Lb / gZ - 2) / 3, 0, 1)
    nail = np.clip(1.3 - np.hypot((np.abs(dz) - 2.5) / gZ, (np.abs(X - (ib + 0.5) * bw) - 3.2) / gX), 0, 1) * np.clip((bw / gX - 5) / 4, 0, 1)
    dark = np.clip(seam * 0.52 + butt * 0.5 + nail * 0.35, 0, 0.75)
    out = base * (1 - dark[..., None]) + col("#2e1a0e") * dark[..., None]
    # the lit edge of each board, beside its seam (a varnished floor catches the light there)
    f = X / bw - np.floor(X / bw)
    edge = np.clip(1 - np.abs(f * bw - 1.6) / gX, 0, 1) * np.clip((bw / gX - 4) / 4, 0, 1)
    out = out * (1 + 0.10 * edge[..., None])

    # ---- the rug: a worn flat-woven one, bands and diamonds
    x0, x1, z0, z1 = M.RUG
    u, v = X - x0, Z - z0
    Lx, Lz = x1 - x0, z1 - z0
    # its edges wander a little (it has been walked crooked)
    wob = (fbm(X / 60, Z / 60, 77, 2) - 0.5) * 5
    inr = band_aa(X + wob * 0.5, x0, x1, gX) * band_aa(Z + wob, z0, z1, gZ)
    red, cream, teal, brown, gold = col("#a8442c"), col("#dccaa0"), col("#2f6a6c"), col("#4a2a1c"), col("#c8923a")
    rug = np.empty(X.shape + (3,), dtype=F32)
    rug[...] = red
    band = np.zeros(X.shape, dtype=F32)
    for (a, b, k) in ((34, 46, cream), (50, 56, teal), (Lx - 46, Lx - 34, cream), (Lx - 56, Lx - 50, teal), (Lx / 2 - 60, Lx / 2 - 54, gold), (Lx / 2 + 54, Lx / 2 + 60, gold)):
        zig = np.abs(((v / 9.0) % 2) - 1) * 3.0                              # the bands' edges are stepped
        m = band_aa(u + zig, a, b, gX)
        rug = rug * (1 - m[..., None]) + k * m[..., None]
        band = np.maximum(band, m)
    for cu in (Lx / 2, Lx / 2 - 100, Lx / 2 + 100):                          # diamonds down the middle
        d = np.abs(u - cu) / 34.0 + np.abs(v - Lz / 2) / 58.0
        m = np.clip((1 - d) * 34 / gX + 0.5, 0, 1)
        rug = rug * (1 - m[..., None]) + cream * m[..., None]
        m = np.clip((0.66 - d) * 34 / gX + 0.5, 0, 1)
        rug = rug * (1 - m[..., None]) + teal * m[..., None]
        m = np.clip((0.3 - d) * 34 / gX + 0.5, 0, 1)
        rug = rug * (1 - m[..., None]) + gold * m[..., None]
    edge = 1 - band_aa(u, 9, Lx - 9, gX) * band_aa(v, 9, Lz - 9, gZ)
    rug = rug * (1 - edge[..., None]) + brown * edge[..., None]
    line = band_aa(u, 13, Lx - 13, gX) * band_aa(v, 13, Lz - 13, gZ) - band_aa(u, 15.5, Lx - 15.5, gX) * band_aa(v, 15.5, Lz - 15.5, gZ)
    rug = rug * (1 - np.clip(line, 0, 1)[..., None]) + cream * np.clip(line, 0, 1)[..., None]
    weave = lines_aa(v, 2.2, 0.9, gZ) * 0.10 + (fbm(u / 4, v / 4, 5, 2) - 0.5) * 0.16
    rug = rug * (1 - weave[..., None])
    worn = np.clip((fbm(u / 50, v / 45, 91, 3) - 0.45) * 2.4, 0, 1) * 0.42
    rug = lerp(rug, rug * 0.6 + col("#b89c7c") * 0.4, worn[..., None])
    out = out * (1 - inr[..., None]) + rug * inr[..., None]
    # the fringe at its two short ends
    for side, xe in ((-1, x0), (1, x1)):
        du = (X - xe) * side
        fr = band_aa(du, 0, 7.5, gX) * band_aa(Z + wob, z0 + 2, z1 - 2, gZ) * (0.35 + 0.65 * lines_aa(Z, 2.4, 1.0, gZ, fade=False))
        fr = fr * np.clip((2.4 / gZ - 0.6) / 1.2, 0.45, 1)
        out = out * (1 - fr[..., None] * 0.85) + cream * 0.95 * fr[..., None] * 0.85
    return out


def skirt(out, along, Y, gY, seed=5):
    sk = band_aa(Y, -5, 13, gY)
    wd = col(TRIM) * (0.85 + 0.3 * fbm(along / 40, Y / 3, seed, 2)[..., None])
    out = lerp(out, wd, sk[..., None])
    line = band_aa(Y, 11.6, 13.4, gY)
    return lerp(out, col(TRIM) * 1.5, (line * 0.55)[..., None])


def m_gable(c):
    X, Y = c.X, c.Y
    gX, gY = grad_of(X) * c.ss, grad_of(Y) * c.ss
    n = fbm(X / 55, Y / 55, 3, 4)
    base = col(WALL) * (0.90 + 0.2 * n[..., None])
    base = base * (0.97 + 0.06 * fbm(X / 8, Y / 30, 9, 2)[..., None])
    # dust and age gather under the roof line and in the low corners
    up = np.clip((Y - (ATTIC.roof_y(X) - 26)) / 26, 0, 1)
    base = base * (1 - 0.16 * up[..., None])
    # a paler patch where a picture used to hang, and the old nail
    old = band_aa(X, 226, 272, gX) * band_aa(Y, 216, 262, gY)
    base = base * (1 + 0.06 * old[..., None])
    for k, (xa, ya, xb, yb) in enumerate(((412, 296, 452, 372), (286, 300, 262, 348), (604, 20, 640, 96), (132, 214, 96, 236))):   # cracks in the old plaster
        t_ = np.clip(((X - xa) * (xb - xa) + (Y - ya) * (yb - ya)) / ((xb - xa) ** 2 + (yb - ya) ** 2), 0, 1)
        wand = (fbm(t_ * 9 + k * 3, t_ * 0 + k, 61, 3) - 0.5) * 9
        d = np.abs((X - xa) * (yb - ya) - (Y - ya) * (xb - xa)) / math.hypot(xb - xa, yb - ya) + 0 * wand
        d = np.abs(((X - xa) * (yb - ya) - (Y - ya) * (xb - xa)) / math.hypot(xb - xa, yb - ya) + wand)
        crack = np.clip(0.8 - d / np.maximum(gX, gY), 0, 1) * (t_ > 0.01) * (t_ < 0.99) * (1 - t_ * 0.6)
        base = base * (1 - 0.42 * crack[..., None])
    return skirt(base, X, Y, gY)


def m_knee(c):
    Z, Y = c.Z, c.Y
    gZ, gY = grad_of(Z) * c.ss, grad_of(Y) * c.ss
    ib = np.floor(Z / 9.0)
    base = col(WALL2) * (0.92 + 0.16 * hashf(ib, 3)[..., None]) * (0.94 + 0.12 * fbm(Z / 3, Y / 50, 4, 2)[..., None])
    groove = lines_aa(Z, 9.0, 1.0, gZ)
    out = base * (1 - 0.36 * groove[..., None])
    return skirt(out, Z, Y, gY, 6)


def m_roof(c):
    S, Z = c.S, c.Z
    gS, gZ = grad_of(S) * c.ss, grad_of(Z) * c.ss
    bw = 15.0
    side = 1000 if c.face == "roofR" else 0
    ib = np.floor(S / bw) + side
    Lb = 220 + 200 * hashf(ib, 2)
    zj = (Z + 500 * hashf(ib, 6)) / Lb
    seg = np.floor(zj)
    base = col(ROOFB) * (0.84 + 0.24 * hashf(ib * 17 + seg, 5)[..., None])
    base = base * (0.90 + 0.2 * fbm(S / 3.5, Z / 70, 12 + side, 3)[..., None])
    stain = fbm(S / 70, Z / 90, 14 + side, 3)
    base = lerp(base, base * col("#c9a878"), (np.clip((stain - 0.58) * 3, 0, 1) * 0.7)[..., None])     # old water stains
    bare = fbm(S / 9, Z / 30, 41 + side, 2)                                                           # paint gone from the wood
    base = lerp(base, col("#b08a5a"), (np.clip((bare - 0.70) * 5, 0, 1) * 0.6)[..., None])
    # the joints between boards are real gaps: near the lens they are several pixels wide
    f = S / bw
    d = np.abs(f - np.round(f)) * bw
    seam = np.clip((0.32 - d) / gS + 0.6, 0, 1) * np.clip((bw / gS - 1.6) / 2.4, 0.12, 1)
    dz = np.abs(zj - np.round(zj)) * Lb
    butt = np.clip((0.3 - dz) / gZ + 0.6, 0, 1) * np.clip((Lb / gZ - 2) / 3, 0, 1)
    nailz = np.abs(((Z - ATTIC.z0) / ATTIC.gap) - np.round((Z - ATTIC.z0) / ATTIC.gap)) * ATTIC.gap     # nail heads in a row along each rafter
    nail = np.clip((0.55 - np.hypot(nailz, np.abs(d - bw / 2) - 3.5)) / np.maximum(gS, gZ) + 0.5, 0, 1)
    dark = np.clip(seam * 0.62 + butt * 0.5 + nail * 0.5, 0, 0.8)
    out = base * (1 - dark[..., None]) + col("#3a2c22") * dark[..., None]
    lit = np.clip((0.9 - np.abs(d - 0.9)) / gS, 0, 1) * np.clip((bw / gS - 6) / 6, 0, 1)                # the edge of each board beside its gap
    return out * (1 + 0.10 * lit[..., None])


def m_rafter(c):
    A = c.attic
    i = np.round((c.Z - A.z0) / A.gap) + 40 * c.sd                             # which rafter this is: each its own piece of wood
    tone = 0.80 + 0.34 * hashf(i, 3)
    Xs = c.X if c.sd == 0 else A.W - c.X
    q = (A.rise * Xs - A.run * c.Y + A.run * A.K) / A.len                      # how far below the boards (0 at the boards, 12 at its lower edge)
    across = q if c.face == "side" else (c.Z - A.z0)                           # the measurement across the grain on the face we see
    off = hashf(i, 5) * 9
    n = fbm(c.S / 70.0 + off, across / 1.3 + i * 3.7, 17, 4)                   # the grain runs up the slope
    k = col(RAFT)[None, None, :] * (tone * (0.72 + 0.56 * n))[..., None]
    streak = fbm(c.S / 140.0 + off, across / 0.42 + i * 1.3, 29, 2)            # darker checks along the grain, seen in the near ones
    k = k * (1 - 0.30 * np.clip((streak - 0.62) * 4, 0, 1)[..., None])
    ks = c.S - (60 + 330 * hashf(i, 8))
    knot = np.clip(1 - np.hypot(ks / 5.0, (across - 6.0) / 2.2), 0, 1)
    k = k * (1 - 0.5 * knot[..., None])
    if c.face == "side":                                     # worn paler along its lower edge, darker up under the boards
        k = k * (0.86 + 0.26 * np.clip(q / A.deep, 0, 1) ** 2)[..., None]
        k = k * (1 + 0.55 * np.clip((q - (A.deep - 1.3)) / 1.3, 0, 1) ** 1.5)[..., None]       # the worn arris along its lower edge catches the light
    else:                                                    # the underside is planed smoother and catches more light
        k = k * 1.14
    return k


SHELL = dict(floor=m_floor, gable=m_gable, kneeL=m_knee, kneeR=m_knee, roofL=m_roof, roofR=m_roof, rafter=m_rafter)


def shell(st):
    x0, x1, y0, y1 = M.WINDOW
    ATTIC.draw(st, SHELL, holes={"gable": [(x0, x1, y0, y1)]})
    # the ridge beam and the plates on top of the low walls
    st.box(342, 358, 386, 421, 0, 1190, wood(mixc(RAFT, "#3a2416", 0.25), 3, "z", 0.3, 2.0, 60.0), "ridge", shadow=False)   # deeper than the rafters, so it shows below them all the way
    st.box(0, 9, 122, 131, 0, 1210, wood(RAFT, 4, "z", 0.25), "plate", shadow=False)
    st.box(691, 700, 122, 131, 0, 1210, wood(RAFT, 5, "z", 0.25), "plate", shadow=False)


# ---------------------------------------------------------------- the window, and the night in it
def window_bars(Qx, Qy):
    """1 where there is glass, 0 where there is a bar of the sash (for the moonlight that comes through)."""
    x0, x1, y0, y1 = M.WINDOW
    u, v = Qx - x0, Qy - y0
    w, h = x1 - x0, y1 - y0
    bar = (np.abs(u - w / 2) < 2.0) | (np.abs(v - h / 3) < 1.8) | (np.abs(v - 2 * h / 3) < 1.8) | (u < 4) | (u > w - 4) | (v < 4) | (v > h - 4)
    return np.where(bar, 0.0, 1.0).astype(F32)


def m_glass(c):
    x0, x1, y0, y1 = M.WINDOW
    U, V, fp = c.U, c.V, c.fp
    w, h = x1 - x0, y1 - y0
    f = np.clip(V / h, 0, 1)
    sky = lerp(col("#2b4688"), col("#0b1440"), f[..., None])
    sky = sky + col("#4a6da2") * (np.exp(-V / 30.0) * 0.55)[..., None]
    sky = sky * (0.9 + 0.2 * fbm(U / 26, V / 14, 51, 3)[..., None])           # thin cloud
    mx, my, mr = w * 0.70, h * 0.66, 7.0
    d = np.hypot(U - mx, V - my)
    sky = sky + col("#9fb6e6") * (np.exp(-d / 13.0) * 0.55)[..., None]
    moon = np.clip((mr - d) / fp + 0.5, 0, 1)
    bite = np.clip((mr * 0.92 - np.hypot(U - mx - 3.6, V - my - 1.4)) / fp + 0.5, 0, 1)      # not quite full
    moon = moon * (1 - bite * 0.82)
    sky = sky * (1 - moon[..., None]) + col("#fbf6dc") * 1.25 * moon[..., None]
    cell_u, cell_v = np.floor(U / 5.0), np.floor(V / 5.0)
    star = (hashf(cell_u * 31 + cell_v * 57, 3) > 0.9) & (np.hypot(U - (cell_u + 0.5) * 5, V - (cell_v + 0.5) * 5) < 0.75 + fp * 0.5) & (V > 40)
    sky = sky + col("#dfe8ff") * (star * 0.8)[..., None]
    # the tree by the house: a black shape, trunk at the left, boughs across
    tr = fbm(U / 15, V / 13, 23, 4)
    crown = np.clip(1.1 - np.hypot((U - w * 0.20) / (w * 0.50), (V - h * 0.50) / (h * 0.50)), 0, 1)
    leaf = (tr + crown * 0.62) > 0.92
    trunk = np.abs(U - (w * 0.16 + V * 0.05)) < 3.2 - V * 0.012
    bough = (np.abs(V - (h * 0.34 + (U - w * 0.16) * 0.42)) < 1.3) & (U > w * 0.16) & (U < w * 0.62)
    bough |= (np.abs(V - (h * 0.58 + (U - w * 0.2) * 0.2)) < 1.0) & (U > w * 0.18) & (U < w * 0.5)
    hill = V < 17 + 7 * fbm(U / 22, V * 0 + 3, 9, 3)
    black = leaf | trunk | bough | hill
    sky = np.where(black[..., None], col("#060a18"), sky)
    lit = (np.abs(U - w * 0.80) < 1.3) & (np.abs(V - 10) < 1.1)                 # one neighbour is still up
    sky = np.where(lit[..., None], col("#ffb84a") * 1.2, sky)
    bars = 1 - window_bars(U + x0, V + y0)
    alb = np.zeros(U.shape + (3,), dtype=F32) + col(TRIMW) * bars[..., None]
    return alb, sky * (1 - bars[..., None])


def window(st):
    x0, x1, y0, y1 = M.WINDOW
    zg = -7.0
    tw = plain(TRIMW, 0.08, 9, 2)
    st.poly([(x0, y0, zg), (x1, y0, zg), (x1, y1, zg), (x0, y1, zg)], m_glass, "window")
    st.poly([(x0, y0, zg), (x0, y0, 0), (x0, y1, 0), (x0, y1, zg)], tw, "window")       # the reveals
    st.poly([(x1, y0, zg), (x1, y0, 0), (x1, y1, 0), (x1, y1, zg)], tw, "window")
    st.poly([(x0, y0, zg), (x1, y0, zg), (x1, y0, 0), (x0, y0, 0)], tw, "window")
    st.poly([(x0, y1, zg), (x1, y1, zg), (x1, y1, 0), (x0, y1, 0)], tw, "window")
    st.box(x0 - 9, x0, y0, y1, 0, 2.5, tw, "window", shadow=False)                       # casing
    st.box(x1, x1 + 9, y0, y1, 0, 2.5, tw, "window", shadow=False)
    st.box(x0 - 11, x1 + 11, y1, y1 + 10, 0, 3.2, tw, "window", shadow=False)
    st.box(x0 - 13, x1 + 13, y0 - 4.5, y0, 0, 10, tw, "window", shadow=False)            # the sill
    st.box(x0 - 9, x1 + 9, y0 - 14, y0 - 4.5, 0, 2.0, tw, "window", shadow=False)
    # on the sill: a cactus that has survived him, and a little tin car
    st.cyl((x0 + 16, 5), 4.2, y0, y0 + 7, plain("#b0603a", 0.1), r1=5.0, name="window", shadow=False)
    st.ball((x0 + 16, y0 + 12.5, 5), 4.6, plain("#4d7a44", 0.2, 3), "window", shadow=False)
    st.ball((x0 + 19.5, y0 + 16, 5), 2.4, plain("#5a8a4c", 0.2, 3), "window", shadow=False)
    st.box(x1 - 30, x1 - 16, y0 + 1.2, y0 + 5, 3, 8.5, plain("#c8402c", 0.1), "window", shadow=False)
    st.box(x1 - 27, x1 - 20, y0 + 5, y0 + 7.6, 3.4, 8.1, plain("#d8dce0", 0.1), "window", shadow=False)
    # a roller blind, up, and its cord
    st.cyl((y1 - 3, 2.6), 2.4, x0 - 2, x1 + 2, plain("#c9b98e", 0.1), axis="x", name="window", shadow=False)
    st.stick((x1 - 14, y1 - 4, 4.6), (x1 - 14, y1 - 30, 4.6), 0.25, col("#e8dfc8"), "window")
    st.ball((x1 - 14, y1 - 31.5, 4.6), 1.4, col("#e8dfc8"), "window", shadow=False)


# ---------------------------------------------------------------- flat things on the far wall
def m_cork(c):
    x0, x1, y0, y1 = M.CORK
    if c.face != "front":
        return col("#7a5632") * (0.9 + 0.2 * patch(c, 6, 3)[..., None])
    u, v, fp = c.X - x0, c.Y - y0, c.fp
    w, h = x1 - x0, y1 - y0
    out = col("#c09664") * (0.82 + 0.36 * fbm(u / 1.3, v / 1.3, 6, 2)[..., None])
    papers = [  # u0, v0, wide, high, lean, kind, color
        (7, 40, 20, 27, 0.05, "list", PAPER), (30, 46, 25, 19, -0.04, "car", "#f6f0dc"), (58, 44, 19, 26, 0.03, "list", "#f4e9b8"),
        (80, 49, 17, 22, -0.06, "photo", "#e8e2d0"), (9, 8, 26, 20, -0.03, "car2", "#f3ecd6"), (38, 6, 17, 24, 0.06, "list", "#dce8f0"),
        (58, 10, 22, 15, 0.02, "card", "#f0d8a8"), (82, 7, 15, 20, -0.02, "list", PAPER), (44, 30, 14, 10, 0.1, "ticket", "#f0a0a0")]
    pins = ["#d83a2c", "#2c64c8", "#e8c030", "#2c9a50", "#d83a2c", "#f0f0f0", "#2c64c8", "#e8c030", "#2c9a50"]
    for i, (pu, pv, pw, ph, lean, kind, pc) in enumerate(papers):
        uu = u - pu - (v - pv) * lean
        vv = v - pv + (u - pu) * lean
        m = rect(uu, vv, 0, pw, 0, ph, fp)
        sheet = np.zeros(u.shape + (3,), dtype=F32) + col(pc)
        if kind == "list":
            ln = (((vv - 2.5) % 3.4) < 1.0) & (vv > 2) & (vv < ph - 5) & (uu > 2.5) & (uu < pw - 3 - 6 * hashf(np.floor((vv - 2.5) / 3.4), i))
            sheet = np.where(ln[..., None], col("#3c4660"), sheet)
            head = (vv > ph - 4.6) & (vv < ph - 2.4) & (uu > 3) & (uu < pw - 5)
            sheet = np.where(head[..., None], col("#b4322a"), sheet)
        elif kind in ("car", "car2"):                         # the boy's drawings of the station wagon
            sky = vv > ph * 0.62
            sheet = np.where(sky[..., None], col("#9cc8ec"), sheet)
            ground = vv < ph * 0.24
            sheet = np.where(ground[..., None], col("#8cb85c") if kind == "car" else col("#e8c878"), sheet)
            body = (uu > pw * 0.14) & (uu < pw * 0.88) & (vv > ph * 0.26) & (vv < ph * 0.52)
            top = (uu > pw * 0.34) & (uu < pw * 0.86) & (vv >= ph * 0.52) & (vv < ph * 0.72)
            sheet = np.where((body | top)[..., None], col("#d83828"), sheet)
            wd = (uu > pw * 0.2) & (uu < pw * 0.84) & (vv > ph * 0.33) & (vv < ph * 0.42)
            sheet = np.where(wd[..., None], col("#9a6a36"), sheet)
            win = (uu > pw * 0.4) & (uu < pw * 0.8) & (vv > ph * 0.56) & (vv < ph * 0.67) & (np.abs(uu - pw * 0.6) > 0.8)
            sheet = np.where(win[..., None], col("#cfe6f4"), sheet)
            for cu in (pw * 0.3, pw * 0.72):
                wh = np.hypot(uu - cu, vv - ph * 0.25) < ph * 0.11
                sheet = np.where(wh[..., None], col("#22222a"), sheet)
            sun = np.hypot(uu - pw * 0.14, vv - ph * 0.84) < ph * 0.1
            sheet = np.where(sun[..., None], col("#f8d030"), sheet)
        elif kind == "photo":
            inner = (uu > 1.5) & (uu < pw - 1.5) & (vv > 4) & (vv < ph - 1.5)
            pic = lerp(col("#6a8ec0"), col("#c89868"), np.clip(1 - (vv - 4) / (ph - 6), 0, 1)[..., None])
            ppl = (np.abs(uu - pw * 0.4) < 2.2) & (vv > 5) & (vv < 13) | (np.abs(uu - pw * 0.64) < 1.6) & (vv > 5) & (vv < 10.5)
            pic = np.where(ppl[..., None], col("#a03c30"), pic)
            sheet = np.where(inner[..., None], pic, sheet)
        elif kind == "card":
            sheet = lerp(col("#e89040"), col("#5a9cc8"), np.clip((vv - ph * 0.35) * 0.4, 0, 1)[..., None])
            mesa = (vv < ph * 0.5) & (np.abs(uu - pw * 0.5) < pw * 0.3 - (vv - ph * 0.2) * 0.5)
            sheet = np.where(mesa[..., None], col("#a8482c"), sheet)
        elif kind == "ticket":
            st_ = ((uu % 3.2) < 0.9) & (vv > 2) & (vv < ph - 2)
            sheet = np.where(st_[..., None], col("#a03030"), sheet)
        sheet = sheet * (0.93 + 0.1 * fbm(uu / 6, vv / 6, 40 + i, 2)[..., None])
        shd = rect(uu - 0.9, vv + 0.9, 0, pw, 0, ph, fp)                         # each sheet lifts a little off the cork
        out = out * (1 - 0.3 * np.clip(shd - m, 0, 1)[..., None])
        out = out * (1 - m[..., None]) + sheet * m[..., None]
        pm = disc(uu, vv, pw * 0.5, ph - 1.6, 1.25, fp)
        out = lay(out, pins[i], pm)
    string = rm(v, h * 0.36 + (u - 30) * 0.02, h * 0.36 + (u - 30) * 0.02 + 0.8, fp) * rm(u, 28, 60, fp)   # a bit of red wool between two pins
    out = lay(out, "#c0281c", string * 0.9)
    fr = 1 - rect(u, v, 3.5, w - 3.5, 3.5, h - 3.5, fp)
    frame = col("#8a5c30") * (0.85 + 0.3 * fbm(u / 2.0 + v / 30, v / 2.0 + u / 30, 8, 2)[..., None])
    out = out * (1 - fr[..., None]) + frame * fr[..., None]
    inner = rect(u, v, 3.5, w - 3.5, 3.5, h - 3.5, fp) - rect(u, v, 4.3, w - 4.3, 4.3, h - 4.3, fp)
    return out * (1 - 0.45 * np.clip(inner, 0, 1)[..., None])


# the trip on the map: pins, and the wool between them (u, v on the map, cm from its lower left corner)
ROUTE = [(150, 112), (121, 106), (113, 74), (82, 62), (61, 71)]
SHORT = [(121, 106), (86, 80), (61, 71)]


def m_map(c):
    x0, x1, y0, y1 = M.MAP
    if c.face != "front":
        return col("#d8ccb0")
    u, v, fp = c.X - x0, c.Y - y0, c.fp
    w, h = x1 - x0, y1 - y0
    land = col("#efe4c2") * (0.95 + 0.08 * fbm(u / 30, v / 30, 3, 3)[..., None])
    # the states: mostly ruled lines out west, each tinted a little differently
    cu = np.floor((u - 34 + 6 * np.sin(v / 37.0)) / 31.0)
    cv = np.floor((v + 11 * hashf(cu, 3)) / 33.0)
    tint = hashf(cu * 7 + cv * 13, 5)
    tints = [col("#f2e2a8"), col("#e4eac0"), col("#f3d9c0"), col("#e9e2cf"), col("#dfe8d4")]
    for i, t in enumerate(tints):
        land = np.where(((tint * 5).astype(np.int32) == i)[..., None], land * 0.35 + t * 0.65, land)
    bu = np.abs(((u - 34 + 6 * np.sin(v / 37.0)) / 31.0) % 1 - 0.5) * 31.0
    bv = np.abs(((v + 11 * hashf(cu, 3)) / 33.0) % 1 - 0.5) * 33.0
    border = np.clip(1 - (15.5 - bu) / fp * 1.2, 0, 1) + np.clip(1 - (16.5 - bv) / fp * 1.2, 0, 1)
    land = land * (1 - 0.5 * np.clip(border, 0, 1)[..., None]) + col("#8a7a9a") * 0.5 * np.clip(border, 0, 1)[..., None]
    # mountains: a spine of hatching down the middle and another near the coast
    mt = np.clip((fbm(u / 9, v / 14, 13, 3) - 0.5) * 3, 0, 1) * (np.exp(-((u - 78 - v * 0.12) / 16.0) ** 2) + 0.8 * np.exp(-((u - 44 - 6 * np.sin(v / 20)) / 7.0) ** 2))
    land = land * (1 - 0.4 * np.clip(mt, 0, 1)[..., None]) + col("#a8885a") * 0.4 * np.clip(mt, 0, 1)[..., None]
    # roads: thin red and grey lines wandering between the towns
    for k, (a, b, f1, kc) in enumerate(((0.52, 30, 23.0, "#c0483a"), (-0.28, 118, 31.0, "#c0483a"), (0.1, 76, 17.0, "#6a6a78"), (1.9, -120, 41.0, "#6a6a78"), (-1.3, 250, 29.0, "#c0483a"))):
        dline = np.abs(v - (a * u + b + 5 * np.sin(u / f1 + k))) / math.sqrt(1 + a * a)
        land = lay(land, kc, np.clip(0.9 - dline / fp, 0, 1) * 0.7)
    # the ocean down the left side, with a coast that wanders
    coast = 26 + 9 * np.sin(v / 31.0 + 0.6) + 10 * (fbm(v / 16, u * 0 + 2, 7, 3) - 0.5) - np.clip((v - 100) * 0.16, 0, 9)
    sea = np.clip((coast - u) / fp + 0.5, 0, 1)
    water = col("#9cc4d6") * (0.94 + 0.1 * fbm(u / 12, v / 5, 4, 2)[..., None])
    shore = np.clip(1 - np.abs(coast - u) / 2.2, 0, 1)
    out = land * (1 - sea[..., None]) + water * sea[..., None]
    out = out * (1 - 0.28 * shore[..., None]) + col("#5c8ea8") * 0.28 * shore[..., None]
    # a title box in the sea, bottom left, and a compass star
    tb = rect(u, v, 4, 24, 6, 26, fp)
    out = lay(out, "#f4ecd4", tb)
    tl = rect(u, v, 6, 22, 19, 22.5, fp) + rect(u, v, 6, 19, 14, 16, fp) + rect(u, v, 6, 21, 9.5, 11.5, fp)
    out = lay(out, "#4a3a5a", np.clip(tl, 0, 1) * 0.8)
    edge = tb - rect(u, v, 4.8, 23.2, 6.8, 25.2, fp)
    out = lay(out, "#4a3a5a", np.clip(edge, 0, 1) * 0.8)
    star = np.clip((5.5 - (np.abs(u - 12) + np.abs(v - 118) + 2.4 * np.minimum(np.abs(u - 12), np.abs(v - 118)))) / fp + 0.5, 0, 1)
    out = lay(out, "#b03a2c", star * 0.85)
    # it has been folded many times: the folds show as light and dark lines
    for k in range(1, 4):
        f = np.clip(1 - np.abs(u - w * k / 4) / fp * 0.9, 0, 1)
        out = out * (1 - 0.22 * f[..., None]) + 0.06 * f[..., None]
    for k in range(1, 3):
        f = np.clip(1 - np.abs(v - h * k / 3) / fp * 0.9, 0, 1)
        out = out * (1 - 0.22 * f[..., None]) + 0.06 * f[..., None]
    bd = 1 - rect(u, v, 2.2, w - 2.2, 2.2, h - 2.2, fp)
    out = lay(out, "#f6f0dc", bd)
    return out


def wall_things(st):
    x0, x1, y0, y1 = M.CORK
    st.box(x0, x1, y0, y1, 0, 3.2, m_cork, "corkboard", shadow=False)
    x0, x1, y0, y1 = M.MAP
    st.box(x0, x1, y0, y1, 0, 0.8, m_map, "wallmap", shadow=False)
    for k, (pu, pv) in enumerate(ROUTE):                                       # pins
        st.ball((x0 + pu, y0 + pv, 2.6), 2.3, col(["#e8c030", "#f0f0f0", "#f0f0f0", "#f0f0f0", "#2c9a50"][k]), "wallmap", shadow=False)
    st.rope([(x0 + pu, y0 + pv, 2.0) for pu, pv in ROUTE], 0.55, col("#d8281c"), name="wallmap", min_px=0.62)
    st.rope([(x0 + pu, y0 + pv - (1.5 if 0 < i < 2 else 0), 2.4) for i, (pu, pv) in enumerate(SHORT)], 0.5, col("#f0b428"), name="wallmap", min_px=0.6)
    for cx, cy in ((x0 + 6, y1 - 5), (x1 - 6, y1 - 5), (x0 + 6, y0 + 5), (x1 - 6, y0 + 5)):   # tape at the corners
        st.box(cx - 5, cx + 5, cy - 2.2, cy + 2.2, 0.8, 1.0, col("#e6d8a0"), "wallmap", shadow=False)
    # the boy's additions to the map: sticky notes at two of the pins, and his own heading taped over the top of it
    st.box(x0 + 126, x0 + 136, y0 + 119, y0 + 129, 0.8, 1.1, lambda c: lay(np.zeros(sh(c) + (3,), F32) + col("#ffe24a"), "#5a5030", rm(c.Y, y0 + 122.5, y0 + 124, c.fp) * 0.6), "wallmap", shadow=False)
    st.box(x0 + 40, x0 + 50, y0 + 56, y0 + 66, 0.8, 1.1, col("#f6a0b8"), "wallmap", shadow=False)

    def m_heading(c):
        u, v, fp = c.X - (x0 + 18), c.Y - (y1 + 4), c.fp
        out = np.zeros(sh(c) + (3,), dtype=F32) + col("#f3eedc")
        kcs = ["#d83a2c", "#2c64c8", "#2c9a50", "#f08a20", "#8a3ac8", "#d83a2c", "#2c64c8", "#f08a20", "#2c9a50"]
        for i, kc in enumerate(kcs):                                   # felt-tip capitals, too small to read: one blob of color each
            cu = 5 + i * 7.2 + (2.5 if i > 3 else 0)
            out = lay(out, kc, rect(u, v, cu - 2.2, cu + 2.2, 3.2, 12.4, fp) * (1 - rect(u, v, cu - 0.7, cu + 0.9, 5.4, 8.2 + (i % 2) * 2, fp)))
        return out
    st.box(x0 + 18, x0 + 92, y1 + 4, y1 + 20, 0, 0.6, m_heading, "wallmap", shadow=False)
    # a framed photograph in the low corner left of the corkboard
    st.box(60, 98, 116, 146, 0, 2.0, lambda c: lay(np.zeros(sh(c) + (3,), F32) + col("#6a4426"), "#c9b08a", rect(c.X, c.Y, 64, 94, 120, 142, c.fp)) if c.face == "front" else col("#5a3a20"), "photo", shadow=False)
    st.box(66, 92, 122, 140, 2.0, 2.2, lambda c: lerp(col("#7aa0c8"), col("#b88a58"), np.clip((131 - c.Y) / 6.0, 0, 1)[..., None]), "photo", shadow=False)
    # a calendar between the board and the window
    cx0, cx1, cy0, cy1 = M.CALENDAR

    def m_cal(c):
        u, v, fp = c.X - cx0, c.Y - cy0, c.fp
        w, h = cx1 - cx0, cy1 - cy0
        out = np.zeros(u.shape + (3,), dtype=F32) + col("#f2ecda")
        pic = rect(u, v, 2, w - 2, h * 0.5, h - 2, fp)
        land = lerp(col("#e8a050"), col("#6aa0d0"), np.clip((v - h * 0.62) / (h * 0.2), 0, 1)[..., None])
        mesa = (v < h * 0.75) & (np.abs(u - w * 0.42) < w * 0.22)
        land = np.where(mesa[..., None], col("#b8532c"), land)
        out = out * (1 - pic[..., None]) + land * pic[..., None]
        grid = (lines_1(u, 2.5, w - 2.5, 7) | lines_1(v, 3, h * 0.44, 5)) & (v < h * 0.45) & (v > 2.5) & (u > 2) & (u < w - 2)
        out = np.where(grid[..., None], col("#8a8aa0"), out)
        today = rect(u, v, w * 0.5, w * 0.5 + 4, h * 0.2, h * 0.2 + 4.5, fp)
        return lay(out, "#d83a2c", today * 0.7)
    st.box(cx0, cx1, cy0, cy1, 0, 0.7, m_cal, "calendar", shadow=False)
    st.ball(((cx0 + cx1) / 2, cy1 + 1.5, 1.2), 1.1, col("#3a3a40"), "calendar", shadow=False)
    # his best fish, on a board, high in the gable
    def m_fish(c):
        u, v, fp = c.X - 318, c.Y - 352, c.fp
        out = wood("#7a5230", 5, "x", 0.25)(c)
        if c.face != "front":
            return out
        oval = np.clip((1 - np.hypot((u - 32) / 31.0, (v - 11.5) / 11.0)) * 11 / fp + 0.5, 0, 1)
        out = out * (0.55 + 0.45 * oval[..., None])
        body = np.clip((1 - np.hypot((u - 30) / 19.0, (v - 11.5) / 5.6)) * 5.6 / fp + 0.5, 0, 1)
        tail = np.clip((6.5 - np.abs(v - 11.5) - (53.5 - u) * 1.1) / fp + 0.5, 0, 1) * (u > 46) * (u < 54.5)
        fishc = lerp(col("#dfe6d8"), col("#4d7f78"), np.clip((v - 9.5) / 4.0, 0, 1)[..., None])
        fishc = np.where((np.hypot(u - 16.5, v - 12.6) < 1.1)[..., None], col("#101418"), fishc)
        m = np.clip(body + tail, 0, 1)
        return out * (1 - m[..., None]) + fishc * m[..., None]
    st.box(318, 382, 352, 375, 0, 2.2, m_fish, "fish", shadow=False)
    # a felt pennant over the globe, right-hand end of the wall
    st.poly([(612, 138, 0.6), (612, 160, 0.6), (676, 143, 0.6)], lambda c: lay(np.zeros(sh(c) + (3,), dtype=F32) + col("#a03028"), "#f0d890", rm(c.V, 0, 3.5, c.fp)), "pennant")


def lines_1(u, lo, hi, n):
    """Thin ruled lines: n of them between lo and hi (hard edged, for tiny things)."""
    step = (hi - lo) / n
    return (np.abs(((u - lo) / step) % 1) < 0.14) & (u >= lo - 0.2) & (u <= hi + 0.2)


# ---------------------------------------------------------------- the desk, the mainframe, the chair
def m_drawers(n, gap=1.0, pull="#d8b060", seed=0, base=DESK_C):
    """A front of n drawers, one above another, each with a brass pull."""
    wd = wood(base, seed, "x", 0.22)

    def f(c):
        out = wd(c)
        if c.face != "front":
            return out
        x0, x1, y0, y1 = c.box[0], c.box[1], c.box[2], c.box[3]
        u, v, fp = c.X - x0, c.Y - y0, c.fp
        w, h = x1 - x0, y1 - y0
        dh = (h - 4) / n
        k = np.floor((v - 2) / dh)
        fv = (v - 2) - k * dh
        groove = (np.clip(1 - np.abs(fv - 0.5) / fp, 0, 1) + np.clip(1 - np.abs(u - 2.5) / fp, 0, 1) + np.clip(1 - np.abs(u - (w - 2.5)) / fp, 0, 1)) * (v > 1.5) * (v < h - 1.5)
        out = out * (1 - 0.6 * np.clip(groove, 0, 1)[..., None])
        hi = np.clip(1 - np.abs(fv - (dh - 1.0)) / fp, 0, 1) * (u > 3) * (u < w - 3)                 # each drawer's top edge is lit
        out = out * (1 + 0.25 * hi[..., None])
        pm = rect(u, fv, w / 2 - 6, w / 2 + 6, dh * 0.5 - 0.9, dh * 0.5 + 1.1, fp) * (k >= 0) * (k < n)
        out = lay(out, pull, pm)
        return out
    return f


def m_keys(c):
    k = col(BEIGE) * 0.96
    if c.face != "top":
        return k * (0.92 + 0.1 * patch(c, 5, 1)[..., None])
    x0, x1, z0, z1 = c.box[0], c.box[1], c.box[4], c.box[5]
    u, v = c.X - x0, c.Z - z0
    keys = (((u - 1.5) % 2.9) < 2.2) & (((v - 1.2) % 2.9) < 2.2) & (u > 1.2) & (u < x1 - x0 - 1.2) & (v > 1) & (v < z1 - z0 - 1)
    out = np.zeros(u.shape + (3,), dtype=F32) + k * 0.74
    return np.where(keys[..., None], col("#e9e2cc"), out)


def m_case(c):
    k = col(BEIGE) * (0.94 + 0.1 * patch(c, 14, 4)[..., None])
    if c.face == "front":
        x0, y0 = c.box[0], c.box[2]
        u, v, fp = c.X - x0, c.Y - y0, c.fp
        w, h = c.box[1] - x0, c.box[3] - y0
        k = k * (1 - 0.14 * rect(u, v, 0, w, 0, 2.2, fp)[..., None])
        slot = rect(u, v, w * 0.52, w * 0.9, h * 0.56, h * 0.72, fp)
        k = lay(k, "#cfc6aa", slot)
        k = lay(k, "#2a2826", rect(u, v, w * 0.56, w * 0.86, h * 0.615, h * 0.665, fp))
        k = lay(k, "#2a2826", rect(u, v, w * 0.52, w * 0.9, h * 0.24, h * 0.3, fp) * 0.8)               # a second drive, never used
        k = lay(k, "#b8ae92", rect(u, v, w * 0.07, w * 0.3, h * 0.5, h * 0.78, fp))                       # the maker's plate, blank
        vent = (((u - w * 0.07) % 1.9) < 0.9) & (u > w * 0.07) & (u < w * 0.42) & (v > h * 0.16) & (v < h * 0.38)
        k = np.where(vent[..., None], k * 0.62, k)
    return k


def m_monitor(c):
    k = col(BEIGE) * (0.95 + 0.1 * patch(c, 14, 7)[..., None])
    if c.face == "front":
        x0, y0 = c.box[0], c.box[2]
        u, v, fp = c.X - x0, c.Y - y0, c.fp
        w, h = c.box[1] - x0, c.box[3] - y0
        sx0, sx1, sy0, sy1 = M.SCREEN
        well = rect(c.X, c.Y, sx0 - 1.6, sx1 + 1.6, sy0 - 1.6, sy1 + 1.6, fp)                            # the bezel steps in toward the glass
        k = k * (1 - 0.3 * well[..., None])
        k = lay(k, "#b0a78c", rect(u, v, w * 0.72, w * 0.94, 1.6, 4.4, fp))                              # the row of knobs under the glass
        k = lay(k, "#5a5648", rect(u, v, w * 0.08, w * 0.14, 2.0, 4.0, fp))
    if c.face == "top":
        z0 = c.box[4]
        vent = (((c.Z - z0) % 2.6) < 1.1) & (c.X > c.box[0] + 5) & (c.X < c.box[1] - 5) & (c.Z < c.box[5] - 3)
        k = np.where(vent[..., None], k * 0.6, k)
    return k


def m_screen_dark(c):
    sx0, sx1, sy0, sy1 = M.SCREEN
    u, v = (c.X - sx0) / (sx1 - sx0), (c.Y - sy0) / (sy1 - sy0)
    g = col("#141c1c") * (0.8 + 0.5 * v[..., None])
    shine = np.clip(1 - np.hypot((u - 0.26) / 0.2, (v - 0.74) / 0.16), 0, 1)                             # the lamp, in the glass
    return g, col("#40484a") * (shine * 0.5)[..., None] + col("#0c1212")


def lamp_head(st, tip, mouth, r0, r1, outside, inside, glow, name, grp, n=12):
    """A cone shade from `tip` (small end) to `mouth` (open end), as flat pieces: the ones we see from outside are
    painted metal, the ones we see into are lit."""
    a, b = np.asarray(tip, float), np.asarray(mouth, float)
    ax = (b - a) / np.linalg.norm(b - a)
    p = np.cross(ax, [0, 1, 0])
    p /= np.linalg.norm(p)
    q = np.cross(ax, p)
    C = np.asarray(st.C)
    ring = lambda c, r: [c + r * (math.cos(2 * math.pi * i / n) * p + math.sin(2 * math.pi * i / n) * q) for i in range(n)]
    A, B = ring(a, r0), ring(b, r1)
    for i in range(n):
        j = (i + 1) % n
        quad = [A[i], A[j], B[j], B[i]]
        mid = sum(quad) / 4
        outward = mid - (a + b) / 2
        outward -= ax * np.dot(outward, ax)
        nq = np.cross(A[j] - A[i], B[i] - A[i])
        if np.dot(nq, outward) < 0:
            nq = -nq
        seen_outside = np.dot(nq, C - mid) > 0
        if seen_outside:
            st.poly([tuple(v) for v in quad], outside, name, grp)
        else:
            st.poly([tuple(v) for v in quad], col("#fff0c8"), name, grp, emi=col(glow) * 1.9, flag=2)
    st.poly([tuple(v) for v in A], outside, name, grp)                                                  # the cap at the small end


def desk_group(st, G="desk"):
    x0, x1, y0, y1, z0, z1 = M.DESK
    top = wood("#8a5630", 2, "x", 0.2)
    st.box(x0, x1, y1 - 5, y1, z0, z1, top, "desk", G, foot=False)
    st.box(x0 + 4, x0 + 62, 0, y1 - 5, z0 + 6, z1 - 4, m_drawers(3, seed=4), "desk", G, foot=True)
    st.box(x1 - 62, x1 - 4, 0, y1 - 5, z0 + 6, z1 - 4, m_drawers(3, seed=5), "desk", G, foot=True)
    st.box(x0 + 62, x1 - 62, 24, y1 - 5, z0 + 6, z0 + 10, wood("#5a3418", 6, "x"), "desk", G)
    st.box(x0 + 62, x1 - 62, y1 - 13, y1 - 5, z1 - 8, z1 - 5, m_drawers(1, seed=7), "desk", G, shadow=False)   # the pencil drawer
    st.feet["desk"] = (x0, x1, z0, z1)
    # ---- the mainframe
    cx0, cx1, cy0, cy1, cz0, cz1 = M.PC_CASE
    st.box(cx0, cx1, cy0, cy1, cz0, cz1, m_case, "computer", G)
    mx0, mx1, my0, my1, mz0, mz1 = M.MONITOR
    st.box((mx0 + mx1) / 2 - 12, (mx0 + mx1) / 2 + 12, cy1, my0, mz0 + 4, mz1 - 6, col(BEIGE) * 0.8, "computer", G, shadow=False)    # the neck it turns on
    st.box(mx0, mx1, my0, my1, mz0, mz1, m_monitor, "computer", G)
    st.box(mx0 + 7, mx1 - 7, my0 + 4, my1 - 5, mz0 - 22, mz0, lambda c: col(BEIGE) * (0.86 + 0.08 * patch(c, 9, 2)[..., None]), "computer", G)
    sx0, sx1, sy0, sy1 = M.SCREEN
    st.poly([(sx0, sy0, mz1 + 0.3), (sx1, sy0, mz1 + 0.3), (sx1, sy1, mz1 + 0.3), (sx0, sy1, mz1 + 0.3)], m_screen_dark, "screen", G, flag=2)
    st.box(cx0 + 5, cx1 - 9, y1, y1 + 3.2, cz1 + 3, z1 - 2.5, m_keys, "computer", G, shadow=False)
    st.box(cx1 - 4, cx1 + 3, y1, y1 + 2.6, cz1 + 6, cz1 + 16, col("#ded6bc"), "computer", G, shadow=False)        # the mouse
    st.rope(curve3([(cx1, y1 + 1.5, cz1 + 6), (cx1 + 3, y1 + 0.6, cz1 - 4), (cx1 - 2, y1 + 0.6, cz1 - 16)], 5), 0.3, col("#bdb49a"), name="computer", grp=G)
    # ---- on the desk
    st.box(x0 + 14, x0 + 54, y1, y1 + 2.4, z0 + 46, z1 - 10, m_atlas, "desk", G, shadow=False)                    # the road atlas, open
    st.box(x0 + 60, x0 + 82, y1, y1 + 1.0, z0 + 58, z1 - 6, lambda c: lay(np.zeros(sh(c) + (3,), F32) + col("#f2dc6a"), "#8a8a60", lines_1(c.Z, c.box[4] + 3, c.box[5], 8) * (c.face == "top") * 0.6), "desk", G, shadow=False)   # a legal pad
    def m_bible(c):                                               # his Bible, by the lamp where he reads it: worn leather, gilt edges
        k = np.zeros(sh(c) + (3,), dtype=F32) + col("#3a2218") * (0.9 + 0.3 * patch(c, 5, 2)[..., None])
        if c.face in ("front", "right"):
            pages = (c.Y > c.box[2] + 0.7) & (c.Y < c.box[3] - 0.7)
            k = np.where(pages[..., None], col("#d8b45a") * (0.85 + 0.15 * ((c.Y * 2.7) % 1 > 0.5))[..., None], k)
        return k
    st.box(x0 + 55, x0 + 77, y1, y1 + 5.4, z0 + 26, z0 + 56, m_bible, "bible", G, shadow=False)
    st.rope(curve3([(x0 + 68, y1 + 3.0, z0 + 56), (x0 + 69, y1 + 1.6, z0 + 59), (x0 + 70, y1 + 0.5, z0 + 64)], 4), 0.5, col("#b02a22"), name="bible", grp=G, min_px=0.6)
    st.cyl((x0 + 88, z0 + 40), 4.2, y1, y1 + 10, plain("#b03a2c", 0.1), name="desk", grp=G, shadow=False, cap=col("#3a2418"))   # his mug
    st.stick((x0 + 92, y1 + 6, z0 + 40), (x0 + 95, y1 + 5, z0 + 40), 0.8, col("#b03a2c"), "desk", G)
    for i, (dh, kc) in enumerate(((4.5, "#3a5a8a"), (4, "#c86a2c"), (3.2, "#d8d0b8"), (5, "#5a7a4a"))):          # manuals, half read
        yb = y1 + sum(h for h, _ in ((4.5, 0), (4, 0), (3.2, 0), (5, 0))[:i])
        st.box(x1 - 50 + i * 1.5, x1 - 12 + i * 2 - (i % 2) * 4, yb, yb + dh, z0 + 26 + (i % 2) * 3, z0 + 58 + i, m_book(kc, i), "desk", G, shadow=(i == 0))
    st.cyl((x1 - 60, z0 + 34), 4.0, y1, y1 + 11, plain("#4a6a8a", 0.1), name="desk", grp=G, shadow=False, cap=col("#1a1a22"))  # pencils in a tin
    for i, (dx, dz, kc) in enumerate(((1.5, 1, "#e8b830"), (-2, 0.5, "#d84030"), (0.5, -2, "#e8b830"), (-1, -1.5, "#3a8a4a"))):
        st.stick((x1 - 60 + dx * 0.6, y1 + 9, z0 + 34 + dz * 0.6), (x1 - 60 + dx * 2.2, y1 + 19 + i, z0 + 34 + dz * 2), 0.42, col(kc), "desk", G)
    st.box(x1 - 44, x1 - 35, y1, y1 + 0.5, z1 - 22, z1 - 13, col("#2a2a32"), "desk", G, shadow=False)                # floppy disks
    st.box(x1 - 34, x1 - 25, y1, y1 + 0.5, z1 - 19, z1 - 10, col("#3a62b0"), "desk", G, shadow=False)
    st.poly([(x1 - 24, y1, z0 + 22), (x1 - 8, y1, z0 + 22), (x1 - 8, y1 + 20, z0 + 16), (x1 - 24, y1 + 20, z0 + 16)], m_photo, "desk", G)   # a photograph in a frame
    st.box(x1 - 26, x1 - 5, y1, y1 + 5.5, z1 - 30, z1 - 7, plain("#a8281e", 0.1, 6, 2), "desk", G, shadow=False)     # the telephone
    st.stick((x1 - 27, y1 + 8.2, z1 - 18), (x1 - 4, y1 + 8.2, z1 - 18), 2.3, col("#b02c22"), "desk", G)
    st.cyl((x1 - 15.5, z1 - 18), 4.6, y1 + 5.5, y1 + 6.3, col("#e8e0cc"), name="desk", grp=G, shadow=False)
    st.rope(curve3([(x1 - 27, y1 + 7, z1 - 18), (x1 - 31, y1 + 2, z1 - 12), (x1 - 29, y1 + 0.8, z1 - 5), (x1 - 22, y1 + 0.8, z1 - 3)], 5), 0.45, col("#8a2018"), name="desk", grp=G, min_px=0.5)
    # ---- the lamp: a jointed arm and a green cone
    bx, bz = x0 + 22, z0 + 26
    st.cyl((bx, bz), 8.5, y1, y1 + 2.4, plain("#2c5a48", 0.1), name="lamp", grp=G, shadow=False)
    j1, j2 = (bx - 6, y1 + 34, bz - 4), (bx + 14, y1 + 58, bz + 8)
    st.stick((bx, y1 + 2, bz), j1, 0.9, col("#c8b070"), "lamp", G)
    st.stick(j1, j2, 0.9, col("#c8b070"), "lamp", G)
    st.ball(j1, 1.6, col("#3a3a3a"), "lamp", G, shadow=False)
    tip, mouth = (j2[0] + 2, j2[1] + 1, j2[2] + 1), (j2[0] + 13.5, j2[1] - 15.8, j2[2] + 5.2)
    lamp_head(st, tip, mouth, 3.2, 11.5, plain("#2f6650", 0.15, 6, 3), None, "#ffe2a0", "lamp", G)
    # ---- his chair, pushed in, with the cardigan he did not take
    hx0, hx1, _, hy1, hz0, hz1 = M.CHAIR
    oak = wood("#a8743c", 9, "x", 0.2)
    st.box(hx0 + 2, hx1 - 2, 43, 48, hz0 + 2, hz1 - 4, oak, "chair", G, foot=True)
    st.box(hx0 + 4, hx1 - 4, 48, 51, hz0 + 4, hz1 - 7, plain("#7a2a22", 0.14, 5), "chair", G, shadow=False)          # a leather pad
    mid_x, mid_z = (hx0 + hx1) / 2, (hz0 + hz1) / 2 - 1
    st.cyl((mid_x, mid_z), 3.2, 11, 43, col("#3a3632"), name="chair", grp=G, shadow=False)
    st.box(hx0 + 1, hx1 - 1, 6, 11, mid_z - 3, mid_z + 3, col("#4a3020"), "chair", G, shadow=False)
    st.box(mid_x - 3, mid_x + 3, 6, 11, hz0, hz1 - 2, col("#4a3020"), "chair", G, shadow=False)
    for cx, cz in ((hx0 + 2, mid_z), (hx1 - 2, mid_z), (mid_x, hz0 + 1), (mid_x, hz1 - 3)):
        st.ball((cx, 3, cz), 3, col("#1c1a1a"), "chair", G, shadow=False)
    zb = hz1 - 2
    for cx in (hx0 + 3, hx1 - 3):
        st.stick((cx, 48, zb - 2), (cx + (-1 if cx < mid_x else 1), hy1 - 5, zb), 1.7, col("#a8743c"), "chair", G)
        st.box(cx - 2, cx + 2, 63.5, 66, hz0 + 10, zb, oak, "chair", G, shadow=False)
        st.stick((cx, 48, hz0 + 12), (cx, 64, hz0 + 12), 1.2, col("#a8743c"), "chair", G)
    for i in range(5):
        cx = hx0 + 9 + i * (hx1 - hx0 - 18) / 4
        st.stick((cx, 48, zb - 2), (cx, hy1 - 6, zb), 0.95, col("#a8743c"), "chair", G)
    st.box(hx0, hx1, hy1 - 8, hy1, zb - 2, zb + 2, oak, "chair", G)
    knit = lambda c: col("#c89a2e") * (0.8 + 0.3 * fbm(c.X / 1.1, c.Y / 5.0, 3, 2)[..., None]) * (1 - 0.25 * (np.abs(c.X - (mid_x + 1)) < 0.9)[..., None])
    st.box(hx0 + 1, mid_x + 6, 54, hy1 + 1.5, zb + 2, zb + 4.2, knit, "chair", G, shadow=False)                       # the cardigan over one corner of the back
    st.box(hx0 + 1, mid_x + 6, hy1, hy1 + 1.5, zb - 3, zb + 4.2, knit, "chair", G, shadow=False)
    st.box(hx0 - 3, hx0 + 4, 40, 82, zb + 2, zb + 4, knit, "chair", G, shadow=False)                                  # a sleeve hangs down
    st.feet["chair"] = (hx0, hx1, hz0, hz1)


def m_atlas(c):
    k = np.zeros(sh(c) + (3,), dtype=F32) + col("#efe6c8")
    if c.face != "top":
        return k * 0.85
    u, v = c.X - c.box[0], c.Z - c.box[4]
    w, d = c.box[1] - c.box[0], c.box[5] - c.box[4]
    k = np.where((np.abs(u - w / 2) < 0.7)[..., None], k * 0.6, k)                                       # the gutter
    road = (np.abs(v - (d * 0.3 + 6 * np.sin(u / 5.0))) < 0.7) | (np.abs(u - (w * 0.7 + 3 * np.sin(v / 4.0))) < 0.6)
    k = np.where(road[..., None], col("#c0483a"), k)
    blue = np.hypot(u - w * 0.22, v - d * 0.7) < 4.5
    return np.where(blue[..., None], col("#9cc4d6"), k)


def m_book(color, i=0):
    k = col(color)

    def f(c):
        out = np.zeros(sh(c) + (3,), dtype=F32) + k * (0.92 + 0.14 * patch(c, 6, i)[..., None])
        if c.face in ("front", "left", "right"):                                      # the pages show on the sides we see
            pages = (c.Y > c.box[2] + 0.5) & (c.Y < c.box[3] - 0.5)
            if c.face != "left":
                out = np.where(pages[..., None], col("#e8dfc6") * (0.85 + 0.15 * ((c.Y * 3.1) % 1 > 0.5))[..., None], out)
        return out
    return f


def m_photo(c):
    u, v, fp = c.U, c.V, c.fp
    out = np.zeros(u.shape + (3,), dtype=F32) + col("#7a5230")
    inner = rect(u, v, 1.6, 14.4, 1.6, 19.2, fp)
    pic = lerp(col("#c8a070"), col("#7aa4cc"), np.clip((v - 8) / 6, 0, 1)[..., None])
    folk = ((np.abs(u - 5) < 1.6) & (v > 3) & (v < 12)) | ((np.abs(u - 8.4) < 1.5) & (v > 3) & (v < 11)) | ((np.abs(u - 11.2) < 1.1) & (v > 3) & (v < 8))
    pic = np.where(folk[..., None], col("#3a4a6a"), pic)
    heads = (np.hypot(u - 5, v - 13) < 1.5) | (np.hypot(u - 8.4, v - 12) < 1.4) | (np.hypot(u - 11.2, v - 9) < 1.1)
    pic = np.where(heads[..., None], col("#e8c0a0"), pic)
    return out * (1 - inner[..., None]) + pic * inner[..., None]


# ---------------------------------------------------------------- the sticky note, and the three things the screen can show
def note(st, G="note"):
    x0, x1, y0, y1 = M.NOTE
    z = M.MONITOR[5] + 0.6

    def m(c):
        w_ = x1 - x0
        u, v, fp = c.U * 16.0 / w_, c.V * 16.0 / w_, c.fp          # (drawn on a 16 cm square, whatever size it is painted)
        out = np.zeros(u.shape + (3,), dtype=F32) + col("#ffe24a")
        ln = (rm(v, 10.6, 12.2, fp) * rm(u, 2.5, 13.0, fp) + rm(v, 7.3, 8.8, fp) * rm(u, 2.5, 11.0, fp) + rm(v, 4.0, 5.5, fp) * rm(u, 2.5, 12.5, fp))
        out = lay(out, "#4a4030", np.clip(ln, 0, 1) * 0.62)
        curl = np.clip((u - v - 9.5) / 2.5, 0, 1) * (v < 4.5)                                        # the corner that has come unstuck
        out = out * (1 - 0.3 * curl[..., None])
        out = out * (1 - 0.14 * rm(v, 13.6, 16.5, fp)[..., None])                                    # the strip of gum along the top
        return out, col("#ffe24a") * 0.16
    st.poly([(x0 + 0.6, y0, z), (x1, y0 + 1.0, z), (x1 - 0.6, y1, z), (x0, y1 - 1.0, z)], m, "note", G, flag=2)


def m_screen(kind):
    sx0, sx1, sy0, sy1 = M.SCREEN

    def f(c):
        u, v = (c.X - sx0) / (sx1 - sx0), (c.Y - sy0) / (sy1 - sy0)
        fpu, fpv = c.fp / (sx1 - sx0), c.fp / (sy1 - sy0)
        r = lambda a, b, cc, d: rm(u, a, b, fpu) * rm(v, cc, d, fpv)
        if kind == "offline":                                 # grey: a window that says there is no connection
            out = np.zeros(u.shape + (3,), dtype=F32) + col("#8e969c")
            out = lay(out, "#c9cdd0", r(0.14, 0.86, 0.2, 0.82))
            out = lay(out, "#5a6470", r(0.14, 0.86, 0.72, 0.82))
            out = lay(out, "#7a8088", r(0.42, 0.58, 0.44, 0.62))                                    # a broken-link sign: a block with a slash
            sl = np.clip(1 - np.abs((u - 0.5) * 1.1 + (v - 0.53)) / (fpu * 2.2), 0, 1) * r(0.38, 0.62, 0.4, 0.66)
            out = lay(out, "#b8322c", sl)
            out = lay(out, "#8a9096", r(0.24, 0.76, 0.29, 0.34))
        elif kind == "login":                                 # blue, with a sign-in box
            out = np.zeros(u.shape + (3,), dtype=F32) + col("#2f62b4") * (0.85 + 0.3 * v[..., None])
            out = lay(out, "#e8ecf2", r(0.2, 0.8, 0.22, 0.8))
            out = lay(out, "#3c58a0", r(0.2, 0.8, 0.68, 0.8))
            out = lay(out, "#ffffff", r(0.28, 0.72, 0.46, 0.57))
            out = lay(out, "#8894a8", r(0.28, 0.72, 0.46, 0.57) - r(0.3, 0.7, 0.475, 0.555))
            out = lay(out, "#4a9a58", r(0.52, 0.72, 0.29, 0.39))
            out = lay(out, "#30384a", r(0.31, 0.33, 0.485, 0.545))
        else:                                                 # the map: pale land, a road, one red dot
            out = np.zeros(u.shape + (3,), dtype=F32) + col("#dfe6cc")
            out = lay(out, "#a8cce0", np.clip((0.2 + 0.08 * np.sin(v * 7.0) - u) / fpu + 0.5, 0, 1))
            road = np.clip(1 - np.abs(v - (0.34 + 0.34 * u + 0.05 * np.sin(u * 9))) / (fpv * 1.6), 0, 1)
            out = lay(out, "#b0a890", road * 0.9)
            road2 = np.clip(1 - np.abs(u - (0.56 + 0.1 * np.sin(v * 6))) / (fpu * 1.4), 0, 1)
            out = lay(out, "#c8c0a8", road2 * 0.7)
            d = np.hypot((u - 0.66) * (sx1 - sx0), (v - 0.58) * (sy1 - sy0))
            out = lay(out, "#f08070", np.clip((5.2 - d) / c.fp + 0.5, 0, 1) * 0.45)
            out = lay(out, "#e01c14", np.clip((2.7 - d) / c.fp + 0.5, 0, 1))
            out = lay(out, "#3c58a0", r(0.0, 1.0, 0.9, 1.0))
        return out * 0.06, out * 0.98
    return f


def screen(st, kind, G="screen"):
    sx0, sx1, sy0, sy1 = M.SCREEN
    z = M.MONITOR[5] + 0.3
    st.poly([(sx0, sy0, z), (sx1, sy0, z), (sx1, sy1, z), (sx0, sy1, z)], m_screen(kind), "screen", G, flag=2, bias=0.2)


# ---------------------------------------------------------------- the filing cabinet and the answering machine
def m_cabinet(c):
    k = col("#4f6a5c") * (0.9 + 0.2 * patch(c, 16, 9)[..., None])
    if c.face == "front":
        x0, y0 = c.box[0], c.box[2]
        u, v, fp = c.X - x0, c.Y - y0, c.fp
        w, h = c.box[1] - x0, c.box[3] - y0
        dh = (h - 5) / 3
        kk = np.floor((v - 3) / dh)
        fv = (v - 3) - kk * dh
        gap = (np.clip(1 - np.abs(fv - 0.6) / fp, 0, 1) + np.clip(1 - np.abs(u - 2.2) / fp, 0, 1) + np.clip(1 - np.abs(u - (w - 2.2)) / fp, 0, 1)) * (v > 2) * (v < h - 1)
        k = k * (1 - 0.6 * np.clip(gap, 0, 1)[..., None])
        hi = np.clip(1 - np.abs(fv - (dh - 0.9)) / fp, 0, 1) * (u > 3) * (u < w - 3)
        k = k * (1 + 0.3 * hi[..., None])
        ok = (kk >= 0) & (kk < 3)
        k = lay(k, "#e2e0d8", rect(u, fv, w / 2 - 9, w / 2 + 9, dh * 0.72, dh * 0.72 + 2.2, fp) * ok)             # handles
        k = lay(k, "#3a4a42", rect(u, fv, w / 2 - 9, w / 2 + 9, dh * 0.72 - 1.2, dh * 0.72, fp) * ok * 0.7)
        k = lay(k, "#efe8d0", rect(u, fv, w / 2 - 7, w / 2 + 7, dh * 0.34, dh * 0.34 + 5.2, fp) * ok)             # label holders
        k = lay(k, "#5a5a6a", rect(u, fv, w / 2 - 5, w / 2 + 3, dh * 0.34 + 2, dh * 0.34 + 3.2, fp) * ok * 0.7)
        dent = np.clip(1 - np.hypot((u - w * 0.78) / 7, (v - h * 0.2) / 5), 0, 1)
        k = k * (1 - 0.12 * dent[..., None])
    if c.face == "top":
        k = k * 0.92
    return k


def m_machine_top(c):
    """The sloping face of the answering machine: U across, V up the slope from its front edge (drawn on a 42 x 37 face)."""
    w_, d_ = M.MACHINE[1] - M.MACHINE[0], math.hypot(M.MACHINE[5] - M.MACHINE[4], M.MACHINE[3] - M.MACHINE[2] - 4.0)
    u, v, fp = c.U * 42.0 / w_, c.V * 37.2 / d_, c.fp
    out = np.zeros(u.shape + (3,), dtype=F32) + col("#a4a6a4") * (0.95 + 0.1 * fbm(u / 6, v / 6, 3, 2)[..., None])
    out = lay(out, "#16161a", rect(u, v, 3.5, 26, 15, 33, fp))                                           # the tape window
    out = lay(out, "#3a3028", rect(u, v, 5, 24.5, 16.5, 31.5, fp) * 0.9)
    for cu in (10.3, 19.4):
        out = lay(out, "#e6e2d6", disc(u, v, cu, 24, 4.1, fp))
        out = lay(out, "#2a2622", disc(u, v, cu, 24, 1.5, fp))
    out = lay(out, "#5a3a22", rect(u, v, 12.5, 17.2, 26.2, 28.0, fp))                                    # tape between the reels
    for i, kc in enumerate(("#c83a2c", "#e4e0d2", "#e4e0d2", "#e4e0d2")):                                # big buttons
        out = lay(out, "#4a4c4e", rect(u, v, 3.2 + i * 7.6, 9.8 + i * 7.6, 3.2, 11.6, fp))
        out = lay(out, kc, rect(u, v, 3.8 + i * 7.6, 9.2 + i * 7.6, 4.2, 11.0, fp))
    grille = (((v - 15.5) % 2.6) < 1.2) & (u > 29.5) & (u < 39) & (v > 15) & (v < 33)
    out = np.where(grille[..., None], col("#3c3e40"), out)
    out = lay(out, "#2a2c2e", rect(u, v, 34, 39, 4.2, 8.6, fp))                                          # the counter (its light is the game's)
    edge = 1 - rect(u, v, 0.7, 41.3, 0.7, 36.4, fp)
    return out * (1 - 0.3 * edge[..., None])


def cabinet(st):
    x0, x1, y0, y1, z0, z1 = M.CABINET
    st.box(x0, x1, y0, y1, z0, z1, m_cabinet, "cabinet", foot=True)
    # behind the machine: telephone books, and a jar of pens
    st.box(x0 + 3, x0 + 34, y1, y1 + 4.5, z0 + 2, z0 + 24, m_book("#e6c84a", 3), "cabinet", shadow=False)
    st.box(x0 + 5, x0 + 35, y1 + 4.5, y1 + 8, z0 + 3, z0 + 24, m_book("#d8d8dc", 4), "cabinet", shadow=False)
    st.cyl((x1 - 9, z0 + 12), 4.2, y1, y1 + 10, plain("#8a4a2a", 0.1), name="cabinet", shadow=False, cap=col("#1a1a1a"))
    for dx, dz, kc in ((1, 1, "#2c64c8"), (-1.5, 0, "#d83a2c"), (0.5, -1.2, "#1a1a1a")):
        st.stick((x1 - 9 + dx * 0.5, y1 + 8, z0 + 12 + dz * 0.5), (x1 - 9 + dx * 2.2, y1 + 17, z0 + 12 + dz * 2.2), 0.4, col(kc), "cabinet")
    machine(st)


def machine(st):
    x0, x1, y0, y1, z0, z1 = M.MACHINE
    grey = plain("#8e9090", 0.1, 8, 4)
    yf = y0 + 4.0
    st.poly([(x0, yf, z1), (x1, yf, z1), (x1, y1, z0), (x0, y1, z0)], m_machine_top, "machine")
    st.poly([(x0, y0, z1), (x1, y0, z1), (x1, yf, z1), (x0, yf, z1)], grey, "machine")
    st.poly([(x1, y0, z1), (x1, y0, z0), (x1, y1, z0), (x1, yf, z1)], grey, "machine")
    st.poly([(x0, y0, z1), (x0, y0, z0), (x0, y1, z0), (x0, yf, z1)], grey, "machine")
    st.occ.append((x0, x1, y0, y0 + 10, z0, z1))
    # its cord, going down behind
    st.rope(curve3([(x1 - 4, y0 + 8, z0), (x1 + 2, y0 + 1, z0 - 6), (x1 + 5, y0 - 14, z0 - 10), (x1 + 6, y0 - 60, z0 - 4)], 6), 0.35, col("#2a2a2a"), name="cabinet")


def tape(st, G="tape"):
    """The loop of tape the machine has thrown out: over its front edge and down the cabinet's top drawer."""
    x0, x1, y0, y1, z0, z1 = M.MACHINE
    cz = M.CABINET[5]
    brown = lambda c: col("#6a3c1c") * (0.75 + 0.9 * np.abs(np.sin(c.along * 3.1 + c.t * 0.02)))[..., None]
    a = [(x0 + 13, y0 + 15.5, z0 + 8), (x0 + 14, y0 + 8, z1 - 6), (x0 + 15, y0 + 4.6, z1 + 0.6), (x0 + 13, y0 - 0.5, z1 + 5), (x0 + 12, y0 - 2, cz + 0.8),
         (x0 + 10, y0 - 17, cz + 1.2), (x0 + 16, y0 - 33, cz + 1.4), (x0 + 28, y0 - 40, cz + 1.4), (x0 + 37, y0 - 30, cz + 1.4), (x0 + 33, y0 - 14, cz + 1.2),
         (x0 + 27, y0 - 2, cz + 0.9), (x0 + 25, y0 - 0.5, z1 + 5), (x0 + 22, y0 + 4.6, z1 + 0.6), (x0 + 20, y0 + 8, z1 - 6), (x0 + 19, y0 + 15.5, z0 + 8)]
    st.rope(curve3(a, 7), 0.5, brown, name="tape", grp=G, min_px=0.72, flag=2)
    b = [(x0 + 25, y0 - 1, cz + 1.0), (x0 + 31, y0 - 9, cz + 1.5), (x0 + 43, y0 - 15, cz + 1.5), (x0 + 47, y0 - 6, cz + 1.3), (x0 + 40, y0 - 1.5, cz + 1.0), (x0 + 32, y0 - 4, cz + 1.2)]
    st.rope(curve3(b, 7), 0.45, brown, name="tape", grp=G, min_px=0.66, flag=2)


# ---------------------------------------------------------------- the shelves, the lamp on them, the family vault
BOOKC = ["#8a3a2c", "#2f5a7a", "#c8a84a", "#4a6a4a", "#d8d0b8", "#6a3a5a", "#c86a2c", "#3a3a48", "#a8a8a0", "#7a5a3a", "#3a7a7a", "#b84a3a"]


def shelves(st):
    x0, x1, y0, y1, z0, z1 = M.SHELVES
    pine = wood("#b88a50", 12, "z", 0.2)
    st.box(x0, x1, 0, 6, z0, z1, pine, "shelves", foot=True)
    st.box(x0 - 1.5, x1, y1 - 4, y1, z0 - 2, z1 + 2, pine, "shelves")
    st.box(x0 + 1, x1, 44.5, 47.5, z0, z1, pine, "shelves", shadow=False)
    st.box(x1 - 2, x1, 6, y1 - 4, z0, z1, wood("#8a6438", 13, "z"), "shelves")
    for zz in (z0, z0 + 82, z0 + 165, z1 - 3):
        st.box(x0 + 1, x1, 6, y1 - 4, zz, zz + 3, pine, "shelves", shadow=False)
    st.occ.append((x0, x1, 0, y1, z0, z1))
    rng = np.random.default_rng(31)
    for lv, (ya, yb) in enumerate(((6, 44.5), (47.5, y1 - 4))):
        for bay, (za, zb) in enumerate(((z0 + 3, z0 + 82), (z0 + 85, z0 + 165), (z0 + 168, z1 - 3))):
            kind = [["binders", "books", "toolbox"], ["books", "jars", "books"]][lv][bay]
            if kind == "jars":
                z = za + 8
                while z < zb - 7:
                    r = 5.0 + rng.random() * 1.2
                    jar(st, x0 + 9 + rng.random() * 3, z, ya, 12 + rng.random() * 5, r, int(rng.integers(0, 4)))
                    z += 2 * r + 1.5 + rng.random() * 3
                st.box(x0 + 22, x1 - 3, ya, ya + 22, za + 4, zb - 20, m_book("#7a8a9a", 7), "shelves", shadow=False)        # boxes of slides behind
                continue
            if kind == "toolbox":
                st.box(x0 + 5, x1 - 4, ya, ya + 22, za + 8, za + 56, plain("#b8322a", 0.12, 9, 5), "shelves", shadow=False)
                st.box(x0 + 5, x1 - 4, ya + 22, ya + 24.5, za + 7, za + 57, plain("#8a241e", 0.1), "shelves", shadow=False)
                st.stick((x0 + 4.5, ya + 26, za + 20), (x0 + 4.5, ya + 26, za + 44), 0.9, col("#d8d8d0"), "shelves")
                st.box(x0 + 6, x1 - 6, ya, ya + 14, za + 60, zb - 2, plain("#c8a060", 0.15, 5, 8), "shelves", shadow=False)     # a carton
                continue
            z = za + 0.5
            while z < zb - 2.5:
                th = (5.5 + rng.random() * 4.5) if kind == "binders" else (2.6 + rng.random() * 3.4)
                th = min(th, zb - z - 0.3)
                hh = (yb - ya) * ((0.80 + 0.14 * rng.random()) if kind == "binders" else (0.55 + 0.38 * rng.random()))
                kc = BOOKC[int(rng.integers(0, len(BOOKC)))] if kind == "books" else ["#2a2a30", "#5a2a2a", "#2a3a5a", "#8a8a88"][int(rng.integers(0, 4))]
                if rng.random() < 0.07 and kind == "books":           # a gap where one has been taken out, the next one leaning
                    z += 5
                    continue
                st.box(x0 + 3 + rng.random() * 4, x1 - 3, ya, ya + hh, z, z + th, spine(kc, int(rng.integers(0, 99)), kind == "binders"), "shelves", shadow=False)
                z += th + 0.25
    # ---- on top
    ty = y1
    lx, lz = M.SHELF_LAMP
    st.cyl((lx, lz), 7.5, ty, ty + 3, plain("#7a5a2a", 0.15), name="shelflamp", shadow=False)
    st.cyl((lx, lz), 1.5, ty + 3, ty + 20, col("#c8a050"), name="shelflamp", shadow=False)
    st.ball((lx, ty + 9, lz), 4.4, plain("#3a6a78", 0.15), "shelflamp", shadow=False)

    def m_shade(c):
        inside = c.kind == 2
        a = np.zeros(sh(c) + (3,), dtype=F32) + col("#c8a468") * 0.5
        glow = np.where(inside[..., None], col("#fff2c8") * 1.9, (col("#ffac48") * 1.5)[None, :] * (0.55 + 0.45 * np.clip(1 - c.along / 24.0, 0, 1))[..., None])
        pleat = 0.9 + 0.1 * np.cos(c.ang * 14)
        return a, glow * pleat[..., None]
    st.cyl((lx, lz), 15.5, ty + 17, ty + 41, m_shade, r1=9.5, name="shelflamp", shadow=False, hollow=True, flag=2)
    st.ball((lx, ty + 27, lz), 3.6, col("#fff8e0"), "shelflamp", shadow=False, emi=col("#fff6d8") * 2.4, flag=2)
    st.box(x0 + 6, x1 - 8, ty, ty + 3, lz + 26, lz + 60, m_book("#2f5a7a", 2), "shelves", shadow=False)          # road atlases, stacked
    st.box(x0 + 8, x1 - 10, ty + 3, ty + 5.5, lz + 28, lz + 58, m_book("#b84a3a", 3), "shelves", shadow=False)
    st.box(x0 + 7, x1 - 12, ty + 5.5, ty + 7.5, lz + 27, lz + 56, m_book("#d8c890", 4), "shelves", shadow=False)
    for i, zz in enumerate((lz + 74, lz + 88, lz + 101)):                                                        # jars of screws
        jar(st, x0 + 12 + (i % 2) * 4, zz, ty, 13 + i, 5.6, i)
    st.box(x0 + 8, x1 - 8, ty, ty + 17, lz + 112, lz + 128, m_radio, "shelves", shadow=False)                    # the old radio
    st.stick((x1 - 12, ty + 17, lz + 126), (x1 - 4, ty + 46, lz + 122), 0.35, col("#d0d0d0"), "shelves")
    st.cyl((x0 + 16, M.SHELVES[4] + 22), 4.6, ty, ty + 12, plain("#c8c0a8", 0.1), name="shelves", shadow=False, cap=col("#2a2a2a"))   # brushes in a pot
    for dx, dz in ((1, 1), (-1.3, 0.4), (0.4, -1.4)):
        st.stick((x0 + 16 + dx * 0.5, ty + 10, M.SHELVES[4] + 22 + dz * 0.5), (x0 + 16 + dx * 2.5, ty + 22, M.SHELVES[4] + 22 + dz * 2.5), 0.45, col("#b0703a"), "shelves")
    # on the low wall over the shelves: a tin number plate, postcards, a pennant
    xw = M.W - 0.5
    st.poly([(xw, 104, lz + 60), (xw, 104, lz + 92), (xw, 120, lz + 92), (xw, 120, lz + 60)],
            lambda c: lay(np.zeros(sh(c) + (3,), F32) + col("#e8e2c8"), "#2c5a9a", rect(c.U, c.V, 3, 29, 3.5, 12.5, c.fp) * (((c.U * 0.42) % 1) < 0.62)), "plate2")
    for i, (za, kc) in enumerate(((lz + 102, "#e89040"), (lz + 122, "#6aa0d0"), (lz + 16, "#c8d8a0"))):
        st.poly([(xw, 100 + i * 4, za), (xw, 100 + i * 4, za + 15), (xw, 111 + i * 4, za + 15.6), (xw, 111 + i * 4, za + 0.6)], col(kc), "cards")
    st.poly([(xw, 98, lz + 150), (xw, 122, lz + 150), (xw, 110, lz + 205)], lambda c: lay(np.zeros(sh(c) + (3,), F32) + col("#2a5a8a"), "#f0d890", rm(c.U, 0, 3.5, c.fp)), "pennant")
    # a drawing taped to the end of the shelves that faces us
    st.poly([(x0 + 12, 40, z1 + 0.3), (x0 + 38, 41.5, z1 + 0.3), (x0 + 37, 74.5, z1 + 0.3), (x0 + 11, 73, z1 + 0.3)], m_kid_drawing(2), "shelves")


def spine(color, seed, binder):
    k = col(color)

    def f(c):
        out = np.zeros(sh(c) + (3,), dtype=F32) + k * (0.9 + 0.2 * hashf(np.floor(c.Y / 3.0), seed))[..., None]
        if c.face == "left":                                   # the spine, toward the room
            y0, y1 = c.box[2], c.box[3]
            v = (c.Y - y0) / (y1 - y0)
            if binder:
                lab = (v > 0.52) & (v < 0.8)
                out = np.where(lab[..., None], col("#e8e2d0"), out)
                ring = (v > 0.16) & (v < 0.24)
                out = np.where(ring[..., None], col("#c8c8c8"), out)
            else:
                band = ((v > 0.78) & (v < 0.86)) | ((v > 0.12) & (v < 0.17) & (seed % 3 == 0))
                out = np.where(band[..., None], col("#e8d8a0") if seed % 2 else k * 0.55, out)
        if c.face == "top":
            out = np.zeros(sh(c) + (3,), dtype=F32) + col("#e4dcc6") * (0.8 + 0.2 * ((c.Z * 2.3) % 1 > 0.4))[..., None]
        return out
    return f


def jar(st, x, z, y, h, r, kind):
    stuff = [col("#7a7c84"), col("#a88448"), col("#7a4a32"), col("#5a6a7a")][kind % 4]

    def m(c):
        f = c.along / h
        glass = col("#b9cdc8") * (0.8 + 0.25 * np.cos(c.ang * 2 + 1.0))[..., None]
        fill = stuff[None, :] * (0.7 + 0.5 * vnoise(c.ang * 5 + kind, c.along * 0.9, kind))[..., None]
        out = np.where((f < 0.62)[..., None], fill * 0.75 + glass * 0.25, glass)
        shine = np.clip(1 - np.abs(c.ang - 2.4) / 0.22, 0, 1) * (f > 0.08) * (f < 0.9)
        return out + (shine * 0.3)[..., None]
    st.cyl((x, z), r, y, y + h, m, name="shelves", shadow=False, cap=col("#9a9ca0"))
    st.cyl((x, z), r * 0.92, y + h, y + h + 1.8, col(["#b8322a", "#3a5a9a", "#c8c8c8", "#d8b040"][kind % 4]), name="shelves", shadow=False)


def m_radio(c):
    k = col("#6a4a30") * (0.9 + 0.2 * patch(c, 8, 3)[..., None])
    if c.face in ("left", "front"):
        a = c.Z if c.face == "left" else c.X
        lo = c.box[4] if c.face == "left" else c.box[0]
        hi = c.box[5] if c.face == "left" else c.box[1]
        u = (a - lo) / (hi - lo)
        v = (c.Y - c.box[2]) / (c.box[3] - c.box[2])
        cloth = (u > 0.1) & (u < 0.6) & (v > 0.15) & (v < 0.85)
        k = np.where(cloth[..., None], col("#b8a070") * (0.8 + 0.2 * ((c.Y * 1.3) % 1 > 0.5))[..., None], k)
        dial = np.hypot((u - 0.8) * 1.4, v - 0.6) < 0.16
        k = np.where(dial[..., None], col("#e8e0c8"), k)
    return k


def m_vault(open_):
    def f(c):
        k = col("#8f989e") * (0.92 + 0.14 * patch(c, 12, 11)[..., None])
        x0, x1, y0, y1, z0, z1 = M.VAULT
        if c.face == "front":
            u, v, fp = c.X - x0, c.Y - y0, c.fp
            w = x1 - x0
            k = k * (1 - 0.18 * rm(v, -1, 1.6, fp)[..., None])
            k = lay(k, "#f4eed8", rect(u, v, 3, 24, 5.0, 17.0, fp))                                      # the label, in his capitals
            k = lay(k, "#c0362c", rect(u, v, 3, 24, 14.4, 17.0, fp))
            k = lay(k, "#3a3a4a", (rect(u, v, 5, 22, 10.4, 12.3, fp) + rect(u, v, 5, 18, 7.0, 8.9, fp)) * 0.85)
            for cu in (2.0, w - 2.0):
                for cv in (2.2, 17.5):
                    k = lay(k, "#5a6268", disc(u, v, cu, cv, 0.8, fp))
        if c.face == "top" and open_:                            # looking down into it
            u, v, fp = c.X - x0, c.Z - z0, c.fp
            w, d = x1 - x0, z1 - z0
            inside = rect(u, v, 2, w - 2, 2, d - 2, fp)
            dark = np.zeros(sh(c) + (3,), dtype=F32) + col("#33383c")
            dark = lay(dark, "#e8e0c8", rect(u, v, 6, 27, 9, 31, fp))                                    # papers
            dark = lay(dark, "#c83228", rect(u, v, 30, 41, 20, 28, fp))                                  # a ketchup packet (it is his vault)
            dark = lay(dark, "#e8c040", disc(u, v, 34, 11, 3.4, fp))                                     # the spare key's fob
            dark = lay(dark, "#d0d0d0", rect(u, v, 33.2, 34.8, 13, 19, fp))
            wall_sh = np.clip(1 - v / 12.0, 0, 1)
            dark = dark * (1 - 0.5 * wall_sh[..., None])
            k = k * (1 - inside[..., None]) + dark * inside[..., None]
        return k
    return f


def vault(st, open_=False, G="back"):
    x0, x1, y0, y1, z0, z1 = M.VAULT
    name = "vault"
    body_top = y1 - 4.5
    st.box(x0, x1, y0, body_top, z0, z1, m_vault(open_), name, G, shadow=not open_)
    steel = plain("#7f888e", 0.12, 9, 12)
    dial_c = (x1 - 11, y0 + 9.5)

    def m_dial(c):
        if c.face != "round":
            return col("#2a2c30")
        k = np.zeros(sh(c) + (3,), dtype=F32) + col("#1e2024")
        cap = c.kind >= 3
        tick = (np.abs(((c.ang * 12 / math.pi) % 1) - 0.5) > 0.3) & (c.rad > 4.2)
        k = np.where((cap & tick)[..., None], col("#f0f0e8"), k)
        k = np.where((cap & (c.rad < 3.0))[..., None], col("#c8ccd0"), k)
        return k
    st.cyl(dial_c, 6.4, z1, z1 + 2.2, m_dial, axis="z", name=name, grp=G, shadow=False)
    st.cyl(dial_c, 2.4, z1 + 2.2, z1 + 4.6, col("#d6dade"), axis="z", name=name, grp=G, shadow=False)
    if not open_:
        st.box(x0 - 0.8, x1 + 0.8, body_top, y1, z0 - 0.8, z1 + 0.8, steel, name, G)
        hx = (x0 + x1) / 2
        zc = (z0 + z1) / 2
        st.rope([(hx - 9, y1, zc), (hx - 8, y1 + 3.6, zc), (hx + 8, y1 + 3.6, zc), (hx + 9, y1, zc)], 0.9, col("#d8dce0"), name=name, grp=G)
    else:                                                         # the lid thrown back: we see its inside
        tilt = 9.0
        lh = z1 - z0 - 1.0                                          # the lid is as deep as the box
        lid = [(x0 - 0.8, body_top, z0 - 0.5), (x1 + 0.8, body_top, z0 - 0.5), (x1 + 0.8, body_top + lh, z0 - 0.5 - tilt), (x0 - 0.8, body_top + lh, z0 - 0.5 - tilt)]

        def m_lid(c):
            u, v, fp = c.U, c.V, c.fp
            k = np.zeros(u.shape + (3,), dtype=F32) + col("#77828a") * (0.92 + 0.14 * fbm(u / 9, v / 9, 4, 2)[..., None])
            inner = rect(u, v, 2.5, x1 - x0 - 0.9, 2.5, lh - 2.5, fp)
            k = k * (1 - inner[..., None]) + col("#a8b2b6") * inner[..., None] * (0.92 + 0.1 * fbm(u / 9, v / 9, 4, 2)[..., None])
            k = lay(k, "#f0e8c8", rect(u, v, 9, 33, 12, 32, fp) * 0.9)                                   # a card taped inside the lid
            k = lay(k, "#5a5a6a", (rect(u, v, 12, 30, 26, 28, fp) + rect(u, v, 12, 27, 21, 23, fp) + rect(u, v, 12, 29, 16, 18, fp)) * 0.7)
            return k
        st.poly(lid, m_lid, name, G)
        st.poly([(x1 + 0.8, body_top, z0 - 0.5), (x1 + 0.8, body_top, z0 - 5), (x1 + 0.8, body_top + lh, z0 - 5 - tilt), (x1 + 0.8, body_top + lh, z0 - 0.5 - tilt)], steel, name, G)
        st.poly([(x0 - 0.8, body_top + lh, z0 - 0.5 - tilt), (x1 + 0.8, body_top + lh, z0 - 0.5 - tilt), (x1 + 0.8, body_top + lh, z0 - 5 - tilt), (x0 - 0.8, body_top + lh, z0 - 5 - tilt)], steel, name, G)


# ---------------------------------------------------------------- the globe
def globe(st):
    gx, gz, gy, r = M.GLOBE
    dark = wood("#5a3a22", 3, "y", 0.25)
    st.cyl((gx, gz), 17, 0, 3.5, dark, name="globe", shadow=True)
    st.feet["globe"] = (gx - 17, gx + 17, gz - 17, gz + 17)
    st.cyl((gx, gz), 2.6, 3.5, gy - r - 6, dark, name="globe", shadow=False)
    st.cyl((gx, gz), 5, gy - r - 8, gy - r - 2, dark, r1=9, name="globe", shadow=False)

    def m(c):
        tilt = 0.4
        nx, ny, nz = c.n[:, 0], c.n[:, 1], c.n[:, 2]
        ny2 = ny * math.cos(tilt) - nx * math.sin(tilt)
        nx2 = nx * math.cos(tilt) + ny * math.sin(tilt)
        lon = np.arctan2(nx2, nz)
        lat = np.arcsin(np.clip(ny2, -1, 1))
        n = fbm(lon * 1.5 + 4, lat * 2.2 + 2, 33, 4)
        land = n > 0.53
        sea = col("#3d7190") * (0.85 + 0.3 * fbm(lon * 3, lat * 3, 7, 2)[..., None])
        earth = lerp(col("#c8a85a"), col("#7a9a52"), np.clip((fbm(lon * 4, lat * 4, 9, 2) - 0.35) * 2.5, 0, 1)[..., None])
        out = np.where(land[..., None], earth, sea)
        out = np.where((np.abs(lat) > 1.25)[..., None], col("#e8ece8"), out)
        grid = (np.abs(((lon * 6 / math.pi) % 1) - 0.5) > 0.47) | (np.abs(((lat * 6 / math.pi) % 1) - 0.5) > 0.47)
        out = np.where(grid[..., None], out * 0.78, out)
        shine = np.clip(nx * 0.09 + ny * 0.23 + nz * 0.97, 0, 1) ** 70                 # the shelf lamp, caught in its varnish
        return out, col("#fff0d0") * (shine * 0.8)[..., None]
    st.ball((gx, gy, gz), r, m, "globe")
    brass = col("#c89a40")
    ring = [(gx + (r + 2.2) * math.cos(a) * 0.42, gy + (r + 2.2) * math.sin(a), gz + (r + 2.2) * math.cos(a) * 0.9) for a in np.linspace(-1.75, 1.95, 15)]
    st.rope(ring, 0.8, brass, name="globe")


# ---------------------------------------------------------------- odds and ends on the floor at the far end
def far_floor(st):
    x1 = M.DESK[1]
    # a radiator under the window, between the desk and the map
    rx0, rx1 = 334, 410
    for i in range(9):
        st.cyl((rx0 + 4 + i * (rx1 - rx0 - 8) / 8, 11), 3.4, 10, 62, plain("#d8ceb4", 0.1, 6, i), name="radiator", shadow=False)
    st.box(rx0, rx1, 58, 64, 6, 16, plain("#d8ceb4", 0.08), "radiator", shadow=False)
    st.box(rx0, rx1, 8, 13, 6, 16, plain("#cfc4a8", 0.08), "radiator", shadow=False)
    st.occ.append((rx0, rx1, 0, 64, 5, 17))
    # the waste basket, and what missed it
    st.cyl((351, 62), 12, 0, 30, lambda c: col("#3f5a4c") * (0.7 + 0.5 * (np.abs(((c.ang * 9 / math.pi) % 1) - 0.5) > 0.2))[..., None] * np.where(c.kind == 2, 0.55, 1.0)[..., None],
           r1=15, name="basket", hollow=True)
    st.cyl((351, 62), 11, 0, 20, col("#e8e2d2"), name="basket", shadow=False)
    for bx, by, bz, br in ((349, 23, 60, 5.5), (356, 22, 66, 4.5), (372, 4, 84, 4.6), (338, 3.6, 92, 3.8)):
        st.ball((bx, by, bz), br, plain("#efe9d8", 0.2, 3, int(bx)), "basket", shadow=False)
    st.feet["basket"] = (336, 366, 47, 77)
    # in the low corner on the left: a tub of rolled maps and a carton
    st.cyl((66, 40), 13, 0, 44, wood("#8a6a3a", 4, "y", 0.3), r1=15, name="rolls", hollow=True)
    st.cyl((66, 40), 12.5, 0, 30, col("#3a2c1c"), name="rolls", shadow=False)
    for i, (dx, dz, hh, kc) in enumerate(((-5, -3, 88, "#e8e0c8"), (4, -5, 96, "#d8e4ea"), (6, 4, 82, "#efe6cc"), (-3, 5, 74, "#e4d8b8"), (0, 0, 102, "#f0ead8"))):
        st.stick((66 + dx, 6, 40 + dz), (66 + dx * 2.3, hh, 40 + dz * 2.2), 2.4, col(kc), "rolls")
    st.feet["rolls"] = (51, 81, 25, 55)
    st.box(18, 58, 0, 28, 62, 104, m_carton, "carton", foot=True)
    st.box(22, 52, 28, 33, 66, 98, m_book("#3a5a8a", 5), "carton", shadow=False)
    st.box(26, 50, 33, 36.5, 68, 96, m_book("#c8a84a", 6), "carton", shadow=False)
    # under the map: an old chest with more of the trip on it
    st.box(446, 566, 0, 40, 6, 52, m_chest, "chest", foot=True)
    st.box(444, 568, 40, 45, 4, 54, wood("#6a4426", 8, "x", 0.25), "chest")
    st.box(456, 500, 45, 48.5, 14, 44, m_book("#d8c890", 9), "chest", shadow=False)       # folded maps
    st.box(460, 498, 48.5, 51, 16, 42, m_book("#9cc4d6", 10), "chest", shadow=False)
    st.box(512, 552, 45, 58, 12, 40, plain("#c8a060", 0.15, 5, 2), "chest", shadow=False)  # a shoe box of slides
    st.box(511, 553, 58, 60.5, 11, 41, plain("#b08a4a", 0.12, 5, 3), "chest", shadow=False)
    st.cyl((530, 47), 6, 60.5, 75, lambda c: col("#3a3c40") * (0.8 + 0.4 * (c.along > 9))[..., None], name="chest", shadow=False)     # binoculars, on end
    st.cyl((543, 47), 6, 60.5, 75, lambda c: col("#3a3c40") * (0.8 + 0.4 * (c.along > 9))[..., None], name="chest", shadow=False)
    # cables from the mainframe down to a strip of sockets on the floor, and its lead along the skirting
    st.box(324, 352, 0, 4.5, 20, 30, plain("#d8d2c0", 0.06), "cables", shadow=False)
    for i, (xa, kc) in enumerate(((300, "#2a2a2e"), (308, "#c8c0a8"), (316, "#2a2a2e"))):
        st.rope(curve3([(xa, 60 - i * 6, 9), (xa + 6, 30, 12), (xa + 14 + i * 4, 6, 20), (330 + i * 8, 4.6, 25)], 6), 0.55, col(kc), name="cables", min_px=0.5)
    st.rope(curve3([(352, 2.5, 25), (372, 1.2, 30), (392, 1.0, 24), (414, 1.0, 12), (430, 6, 2)], 6), 0.5, col("#2a2a2e"), name="cables", min_px=0.5)
    # crayons he left on the rug, and the tin they came in
    rx0, rx1, rz0, rz1 = M.RUG
    st.box(rx1 - 46, rx1 - 28, 0.4, 3.4, rz0 + 26, rz0 + 38, plain("#e8c83a", 0.1), "crayons", shadow=False)
    rngc = np.random.default_rng(4)
    for i, kc in enumerate(("#d83a2c", "#2c64c8", "#2c9a50", "#f08a20", "#8a3ac8", "#e8c030", "#20a0a8")):
        cx, cz, an = rx1 - 62 + rngc.random() * 44, rz0 + 44 + rngc.random() * 26, rngc.random() * 3.14
        st.stick((cx, 1.0, cz), (cx + 8 * math.cos(an), 1.0, cz + 8 * math.sin(an)), 0.55, col(kc), "crayons", min_px=0.6)
    st.poly([(rx1 - 88, 0.7, rz0 + 62), (rx1 - 60, 0.7, rz0 + 64), (rx1 - 58, 0.7, rz0 + 30), (rx1 - 86, 0.7, rz0 + 28)], m_kid_drawing(0), "crayons")   # and what he was drawing
    # a manual left face down by the desk, his slippers, and paper darts that did not make it across the room
    st.box(122, 150, 0, 0.9, 108, 128, m_book("#3a6a5a", 2), "floorbits", shadow=False)
    st.box(123, 136, 0.9, 2.6, 109, 127, m_book("#3a6a5a", 2), "floorbits", shadow=False)
    st.box(137, 149, 0.9, 2.2, 109, 127, m_book("#3a6a5a", 3), "floorbits", shadow=False)
    for sx in (272, 284):
        st.box(sx, sx + 9, 0, 4.5, 96, 118, lambda c: np.where((((c.X * 0.5) % 1 < 0.5) ^ ((c.Z * 0.4) % 1 < 0.5))[..., None], col("#7a3028"), col("#3a4a38")), "floorbits", shadow=False)
    for (dx, dz, an) in ((455, 300, 0.6), (188, 300, 2.4), (566, 470, 1.2), (118, 356, 4.0)):
        ca, sa = math.cos(an), math.sin(an)
        nose, l_, r_, tail = (dx + 11 * ca, 0.6, dz + 11 * sa), (dx - 8 * ca - 5.5 * sa, 0.6, dz - 8 * sa + 5.5 * ca), (dx - 8 * ca + 5.5 * sa, 0.6, dz - 8 * sa - 5.5 * ca), (dx - 8 * ca, 3.4, dz - 8 * sa)
        st.poly([nose, l_, r_], col("#f4f0e2"), "darts")
        st.poly([nose, tail, (dx - 8 * ca, 0.6, dz - 8 * sa)], col("#d8d2c0"), "darts")
    # a stack of magazines beside the desk, and the toy wagon on the rug
    for i in range(6):
        st.box(338 + (i % 2) * 2, 372 - (i % 3), i * 2.6, i * 2.6 + 2.6, 86 + (i % 2) * 1.5, 112 - (i % 2), m_book(BOOKC[(i * 5) % len(BOOKC)], i), "magazines", shadow=(i == 0), foot=(i == 0))
    st.box(404, 424, 1.8, 6.8, 92, 101, plain("#c8322a", 0.08), "toycar", shadow=False)
    st.box(408, 422, 6.8, 10.4, 92.5, 100.5, plain("#c8322a", 0.08), "toycar", shadow=False)
    st.box(404.5, 423.5, 3, 5.4, 101, 101.3, col("#a87840"), "toycar", shadow=False)
    for wx in (408, 420):
        st.cyl((wx, 2.2), 2.2, 100.4, 101.8, col("#1a1a1a"), axis="z", name="toycar", shadow=False)


def m_carton(c):
    k = col("#c09a62") * (0.88 + 0.22 * patch(c, 10, 2)[..., None])
    if c.face in ("front", "right"):
        a = c.X if c.face == "front" else c.Z
        tape_ = np.abs(a - (c.box[0] + 20 if c.face == "front" else c.box[4] + 21)) < 2.4
        k = np.where(tape_[..., None], col("#d8c08a"), k)
        flute = (c.Y > c.box[3] - 2.2)
        k = np.where(flute[..., None], k * 0.8, k)
    return k


def m_chest(c):
    k = wood("#7a4e2a", 3, "x", 0.25)(c)
    if c.face == "front":
        u, v, fp = c.X - c.box[0], c.Y - c.box[2], c.fp
        w, h = c.box[1] - c.box[0], c.box[3] - c.box[2]
        for a in (10, w / 2, w - 10):                             # iron straps
            k = lay(k, "#3a3430", rm(u, a - 2.6, a + 2.6, fp))
        k = lay(k, "#c8a040", rect(u, v, w / 2 - 3.5, w / 2 + 3.5, h - 12, h - 3, fp))       # the hasp
        plank = np.clip(1 - np.abs(v - h * 0.5) / fp, 0, 1)
        k = k * (1 - 0.4 * plank[..., None])
    return k


# ---------------------------------------------------------------- overhead: the banner, the aeroplane, things kept in the roof
GL = {  # each letter as pen strokes on a grid 4 wide and 6 high
    "T": [[(0, 6), (4, 6)], [(2, 6), (2, 0)]],
    "R": [[(0, 0), (0, 6), (2.8, 6), (4, 5.2), (4, 4), (2.8, 3.1), (0, 3.1)], [(2, 3.1), (4, 0)]],
    "I": [[(2, 0), (2, 6)], [(0.9, 6), (3.1, 6)], [(0.9, 0), (3.1, 0)]],
    "P": [[(0, 0), (0, 6), (2.8, 6), (4, 5.2), (4, 3.9), (2.8, 3), (0, 3)]],
    "H": [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3.1), (4, 3.1)]],
    "E": [[(4, 6), (0, 6), (0, 0), (4, 0)], [(0, 3.1), (3, 3.1)]],
    "A": [[(0, 0), (2, 6), (4, 0)], [(0.9, 2.1), (3.1, 2.1)]],
    "D": [[(0, 0), (0, 6), (2.3, 6), (3.6, 5), (4, 3), (3.6, 1), (2.3, 0), (0, 0)]],
    "Q": [[(1.2, 0), (0.3, 1), (0, 3), (0.3, 5), (1.2, 6), (2.8, 6), (3.7, 5), (4, 3), (3.7, 1), (2.8, 0), (1.2, 0)], [(2.4, 1.6), (4.3, -0.6)]],
    "U": [[(0, 6), (0, 1.6), (0.6, 0.5), (1.5, 0), (2.5, 0), (3.4, 0.5), (4, 1.6), (4, 6)]],
    "M": [[(0, 0), (0, 6), (2, 2.4), (4, 6), (4, 0)]],
    "S": [[(3.9, 5), (3.2, 5.8), (2.2, 6), (1.2, 5.9), (0.3, 5.2), (0.2, 4.2), (0.9, 3.4), (2, 3.05), (3.2, 2.6), (3.9, 1.8), (3.8, 0.8), (3, 0.15), (2, 0), (0.9, 0.2), (0.1, 1)]],
}



def label_texture(words, wide, high, res=6, ink=(34, 40, 70), paper=(240, 232, 208), pen_w=1.5, seed=3):
    """A few words in marker capitals on a slip of paper -> picture (float), `res` pixels to the centimetre."""
    ss = 3
    W, H = int(wide * res), int(high * res)
    im = Image.new("RGB", (W * ss, H * ss), paper)
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(seed)
    unit = high * 0.62 / 6.0
    adv = (wide - 3.0) / len(words)
    x = 1.5
    for ch in words:
        if ch != " ":
            for stroke in GL[ch]:
                q = [((x + (adv - 4 * unit * 0.8) / 2 + (px * 0.8 + rng.normal(0, 0.05)) * unit) * res * ss, (high - (high * 0.19 + (py + rng.normal(0, 0.05)) * unit)) * res * ss) for px, py in stroke]
                wd = max(1, int(pen_w * res * ss))
                d.line(q, fill=ink, width=wd, joint="curve")
                for (qx, qy) in q:
                    d.ellipse([qx - wd / 2, qy - wd / 2, qx + wd / 2, qy + wd / 2], fill=ink)
        x += adv
    return np.asarray(im.resize((W, H), Image.LANCZOS), dtype=F32) / 255


def letters_texture(res=5):
    """TRIP HEADQUARTERS on paper, in two hands: TRIP in a father's ruled capitals, HEADQUARTERS in a boy's felt-tips.
    -> (picture, coverage) as floats, `res` pixels to the centimetre, and the banner's size in cm."""
    wide, high = M.BANNER[1] - M.BANNER[0], M.BANNER[3] - M.BANNER[2]
    W, H = int(wide * res), int(high * res)
    ss = 3
    im = Image.new("RGBA", (W * ss, H * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(12)
    # the paper: sheets taped side by side, none of them quite level
    n = 6
    sw = wide / n
    for i in range(n):
        dy = rng.normal(0, 0.35)
        tone = 236 + int(rng.integers(-5, 6))
        x0, x1 = i * sw - 0.4, (i + 1) * sw + 0.4
        d.polygon([(x0 * res * ss, (0.8 + dy) * res * ss), (x1 * res * ss, (0.8 + dy + rng.normal(0, 0.25)) * res * ss),
                   (x1 * res * ss, (high - 0.5 + dy) * res * ss), (x0 * res * ss, (high - 0.5 + dy + rng.normal(0, 0.25)) * res * ss)],
                  fill=(tone + 6, tone, tone - 22, 255))
    for i in range(1, n):                                     # the tape over each join
        x = i * sw
        d.rectangle([(x - 1.1) * res * ss, 3 * res * ss, (x + 1.1) * res * ss, 9 * res * ss], fill=(222, 208, 160, 255))
        d.rectangle([(x - 1.1) * res * ss, (high - 8) * res * ss, (x + 1.1) * res * ss, (high - 2.5) * res * ss], fill=(222, 208, 160, 255))
    def pen(pts, color, width):
        q = [(x * res * ss, (high - y) * res * ss) for x, y in pts]
        wd = max(1, int(width * res * ss))
        d.line(q, fill=color, width=wd, joint="curve")
        for (x, y) in (q[0], q[-1]):
            d.ellipse([x - wd / 2, y - wd / 2, x + wd / 2, y + wd / 2], fill=color)
        for (x, y) in q[1:-1]:
            d.ellipse([x - wd / 2, y - wd / 2, x + wd / 2, y + wd / 2], fill=color)

    # TRIP: ruled, even, navy marker
    cap = high * 0.60
    unit = cap / 6.0
    x = 7.0
    base = high * 0.17
    for ch in "TRIP":
        wch = 4 * unit * (0.62 if ch == "I" else 0.86)
        for stroke in GL[ch]:
            pen([(x + px * unit * (0.62 if ch == "I" else 0.86), base + py * unit) for px, py in stroke], (30, 44, 110, 255), 1.75)
        x += wch + 2.6
    x += 5.0
    # HEADQUARTERS: felt-tips, every letter its own color and its own idea of straight
    felt = [(214, 48, 36), (36, 140, 70), (40, 86, 200), (236, 130, 20), (150, 50, 160), (214, 48, 36), (20, 150, 160), (236, 130, 20), (40, 86, 200), (36, 140, 70), (214, 48, 36), (150, 50, 160)]
    word = "HEADQUARTERS"
    room = wide - 6.0 - x
    adv = room / len(word)
    for i, ch in enumerate(word):
        sc = unit * (0.92 + 0.16 * rng.random())
        wch = 4 * sc * 0.74
        lift = rng.normal(0, 0.55)
        lean = rng.normal(0, 0.07)
        for stroke in GL[ch]:
            pts = []
            for px, py in stroke:
                jx, jy = rng.normal(0, 0.12), rng.normal(0, 0.12)
                pts.append((x + (adv - wch) / 2 + (px * 0.74 + py * lean + jx) * sc, base + lift + (py + jy) * sc))
            pen(pts, felt[i] + (255,), 2.05)
        x += adv
    # the boy's own additions: a star at the start, a wagon and a wiggly road underneath
    sx, sy, sr = 3.6, high * 0.73, 2.6
    star = [(sx + (sr if k % 2 == 0 else sr * 0.42) * math.sin(k * math.pi / 5), sy + (sr if k % 2 == 0 else sr * 0.42) * math.cos(k * math.pi / 5)) for k in range(10)]
    d.polygon([(px * res * ss, (high - py) * res * ss) for px, py in star], fill=(240, 190, 30, 255))
    road = [(6 + t * (wide - 12) / 40, high * 0.075 + 0.55 * math.sin(t * 0.9)) for t in range(41)]
    pen(road, (120, 120, 130, 255), 0.5)
    cx, cy = wide - 15.0, high * 0.105
    d.rectangle([(cx - 5) * res * ss, (high - cy - 3.2) * res * ss, (cx + 5) * res * ss, (high - cy) * res * ss], fill=(214, 48, 36, 255))
    d.rectangle([(cx - 2) * res * ss, (high - cy - 5.4) * res * ss, (cx + 4.6) * res * ss, (high - cy - 3.2) * res * ss], fill=(214, 48, 36, 255))
    for wx in (cx - 3, cx + 3):
        d.ellipse([(wx - 1.3) * res * ss, (high - cy - 0.6) * res * ss, (wx + 1.3) * res * ss, (high - cy + 2.0) * res * ss], fill=(30, 30, 36, 255))
    a = np.asarray(im.resize((W, H), Image.LANCZOS), dtype=F32) / 255
    return np.clip(a[..., :3], 0, 1), np.clip(a[..., 3], 0, 1), (wide, high)


_BANNER = {}


def banner(st):
    if "tex" not in _BANNER:
        _BANNER["tex"] = letters_texture()
    tex, cov, (wide, high) = _BANNER["tex"]
    res = tex.shape[1] / wide
    x0, x1, y0, y1, z = M.BANNER
    sag = 4.5

    def hang(u):                                              # how far the string has dropped at u cm along it
        f = u / wide
        return sag * 4 * f * (1 - f)

    def m(c):
        u = c.U - 6.0
        v = c.V - 8.0 + hang(np.clip(u, 0, wide)) + 0.5 * np.sin(u / 9.0)        # the paper waves a little along its lower edge
        tx, ty = u * res, (high - v) * res
        inside = (u >= 0) & (u <= wide - 0.01) & (v >= 0) & (v <= high - 0.01)
        a = sample(cov, tx, ty) * inside
        k = sample(tex, tx, ty)
        k = k * (0.94 + 0.1 * fbm(u / 12, v / 12, 5, 2)[..., None])
        k = k * (1 - 0.1 * np.clip(np.sin(u / wide * 6 * math.pi * 2) * 0.5 + 0.3, 0, 1) * (v < 6))[..., None]
        return k, k * col("#ffe6bc") * 0.40, a > 0.5               # (paper lets the room's light through, and it is the room's title)
    st.poly([(x0 - 6, y0 - 8, z), (x1 + 6, y0 - 8, z), (x1 + 6, y1 + 3, z), (x0 - 6, y1 + 3, z)], m, "banner", flag=3)
    # the string it hangs on, nailed to the faces of the two rafters behind it
    pts = []
    for i in range(13):
        f = i / 12
        u = f * wide
        pts.append((x0 + u, y1 - 0.4 - hang(u), z + 0.4))
    st.rope([(x0 - 4, y1 + 0.6, z - 1.5)] + pts + [(x1 + 4, y1 + 0.6, z - 1.5)], 0.38, col("#d8cfb0"), name="banner", min_px=0.55, flag=2)
    for f in (0.02, 0.2, 0.4, 0.6, 0.8, 0.98):                 # clothes pegs hold the paper on the string
        u = f * wide
        st.box(x0 + u - 0.9, x0 + u + 0.9, y1 - 4.2 - hang(u), y1 + 1.2 - hang(u), z + 0.3, z + 1.3, col("#d8b070"), "banner", shadow=False, flag=2)


def m_kid_drawing(kind):
    def f(c):
        u, v, fp = c.U, c.V, c.fp
        w = np.max(u) + 0.01
        h = np.max(v) + 0.01
        out = np.zeros(u.shape + (3,), dtype=F32) + col("#f3eedc")
        if kind == 0:                                           # the tent, the sun, five of them
            out = np.where((v < h * 0.25)[..., None], col("#7ab85a"), out)
            tent = (v > h * 0.25) & (v < h * 0.7) & (np.abs(u - w * 0.3) < (h * 0.7 - v) * 0.6)
            out = np.where(tent[..., None], col("#e88a2c"), out)
            sun = np.hypot(u - w * 0.82, v - h * 0.8) < h * 0.12
            out = np.where(sun[..., None], col("#f8d030"), out)
            for i in range(5):
                fx = w * (0.5 + i * 0.09)
                hh = h * (0.3 - i * 0.03)
                body = (np.abs(u - fx) < 0.7) & (v > h * 0.2) & (v < h * 0.2 + hh)
                out = np.where(body[..., None], col(["#3a5ac8", "#c83a8a", "#3a9a5a", "#8a3ac8", "#c8502a"][i]), out)
        elif kind == 1:                                         # a plan: boxes and arrows in red
            for (a, b, cc, dd) in ((0.1, 0.4, 0.6, 0.85), (0.55, 0.9, 0.55, 0.8), (0.3, 0.7, 0.15, 0.4)):
                bx = rect(u, v, w * a, w * b, h * cc, h * dd, fp) - rect(u, v, w * a + 1.2, w * b - 1.2, h * cc + 1.2, h * dd - 1.2, fp)
                out = lay(out, "#c8322a", np.clip(bx, 0, 1))
            arrow = (np.abs((v - h * 0.5) - (u - w * 0.5) * 0.3) < 0.8) & (u > w * 0.3) & (u < w * 0.7)
            out = np.where(arrow[..., None], col("#2c64c8"), out)
        else:                                                   # the wagon again, bigger, with flames
            body = (u > w * 0.15) & (u < w * 0.88) & (v > h * 0.3) & (v < h * 0.5)
            top = (u > w * 0.35) & (u < w * 0.84) & (v >= h * 0.5) & (v < h * 0.66)
            out = np.where((body | top)[..., None], col("#d83828"), out)
            for cu in (w * 0.3, w * 0.72):
                out = np.where((np.hypot(u - cu, v - h * 0.3) < h * 0.09)[..., None], col("#22222a"), out)
            flame = (u < w * 0.15) & (u > w * 0.02) & (np.abs(v - h * 0.4) < (u - w * 0.02) * 0.6)
            out = np.where(flame[..., None], col("#f8a020"), out)
            out = np.where((v < h * 0.2)[..., None], col("#b8b8c0"), out)
        return out * (0.94 + 0.08 * fbm(u / 7, v / 7, 3 + kind, 2)[..., None])
    return f


def seen(x, y, z=None, lift=0.3):
    """The place in the room that a picture point shows: on the upright plane at depth z, or (z None) on the
    right-hand slope of the roof, `lift` cm inside it. For putting a thing exactly where the eye wants it."""
    from room import View
    v = View(**M.VIEW)
    a, u = (x - v.cx) / v.F, (v.hz - y) / v.F
    d = (a * v.rx + v.fx, u, a * v.rz + v.fz)
    C = (v.cam_x, v.eye, v.cam_z)
    if z is not None:
        t = (z - C[2]) / d[2]
    else:
        f0 = (ATTIC.rise * (ATTIC.W - C[0]) - ATTIC.run * C[1] + ATTIC.run * ATTIC.K) / ATTIC.len
        df = (-ATTIC.rise * d[0] - ATTIC.run * d[1]) / ATTIC.len
        t = (lift - f0) / df
    return tuple(C[i] + t * d[i] for i in range(3))


def on_slope(side, s, z, lift=0.6):
    """A place on the underside of the roof boards: `s` cm up the slope from the plate, at depth z."""
    f = s / ATTIC.len
    x = f * ATTIC.run if side == "L" else M.W - f * ATTIC.run
    y = M.KNEE + f * ATTIC.rise
    nx = (ATTIC.rise / ATTIC.len) * (1 if side == "L" else -1)
    ny = -ATTIC.run / ATTIC.len
    return (x + nx * lift, y + ny * lift, z)


def overhead(st):
    banner(st)
    # ---- the model aeroplane on its thread, over the wall map: a yellow biplane with red wings, banking toward us
    px, py, pz = M.PLANE
    k = 1.35
    yaw, roll, pitch = math.radians(158), math.radians(-34), math.radians(5)

    def T(p):
        x, y, z = (q * k for q in p)                            # the model's own measurements: x along the body (nose +), y up, z along the wings
        y, z = y * math.cos(roll) - z * math.sin(roll), y * math.sin(roll) + z * math.cos(roll)
        x, y = x * math.cos(pitch) - y * math.sin(pitch), x * math.sin(pitch) + y * math.cos(pitch)
        x, z = x * math.cos(yaw) - z * math.sin(yaw), x * math.sin(yaw) + z * math.cos(yaw)
        return (px + x, py + y, pz + z)

    def m_wing(c):
        u, v = c.U, c.V
        w = np.max(u) + 1e-3
        kk = np.zeros(u.shape + (3,), dtype=F32) + col("#d83a28") * (0.9 + 0.2 * fbm(u / 6, v / 6, 3, 2)[..., None])
        tip = (u < w * 0.1) | (u > w * 0.9)
        kk = np.where(tip[..., None], col("#f4ead0"), kk)
        ribs = (np.abs((u / (w / 12.0)) % 1 - 0.5) > 0.42)
        return np.where(ribs[..., None], kk * 0.82, kk)
    st.stick(T((16, 0, 0)), T((-6, 0, 0)), 3.6 * k, col("#f0c020"), "aeroplane", r1=3.0 * k)
    st.stick(T((-6, 0, 0)), T((-25, 1, 0)), 3.0 * k, col("#f0c020"), "aeroplane", r1=1.2 * k)
    st.ball(T((17, 0, 0)), 3.0 * k, col("#c83428"), "aeroplane", shadow=False)
    st.stick(T((19.6, -7, 0)), T((19.6, 7, 0)), 0.6, col("#5a4030"), "aeroplane")
    for wy, c0, c1, sp in ((7.5, 13, 2, 31), (-2.5, 11, 1, 27)):
        st.poly([T((c0, wy, -sp)), T((c0, wy, sp)), T((c1, wy, sp)), T((c1, wy, -sp))], m_wing, "aeroplane", flag=1)
    for wz in (-20, 20):
        st.stick(T((10, -2.5, wz)), T((10, 7.5, wz)), 0.5, col("#5a4030"), "aeroplane")
        st.stick(T((3.5, -2.5, wz)), T((4.5, 7.5, wz)), 0.5, col("#5a4030"), "aeroplane")
    st.poly([T((-19, 1, -11)), T((-19, 1, 11)), T((-27, 1, 9)), T((-27, 1, -9))], col("#d83a28"), "aeroplane", flag=1)
    st.poly([T((-19, 1, 0)), T((-27, 1, 0)), T((-27.5, 10, 0)), T((-23, 9, 0))], col("#f0c020"), "aeroplane", flag=1)
    for wz in (-6, 6):
        st.stick(T((9, -2, wz)), T((10, -8, wz)), 0.5, col("#5a4030"), "aeroplane")
        st.ball(T((10, -8.5, wz * 1.15)), 2.3 * k, col("#2a2a2a"), "aeroplane", shadow=False)
    top = T((5, 8, 0))
    st.stick(top, (top[0], roof_y(top[0]) - 15, top[2]), 0.2, col("#d8d0c0"), "aeroplane", min_px=0.5)
    # ---- a storm lantern on a nail in a left-hand rafter
    hk = on_slope("L", 190, 392, 12.5)
    lx_, lz_ = hk[0], hk[2] + 3.4
    st.rope([(lx_, hk[1], lz_), (lx_ - 3.6, hk[1] - 9, lz_), (lx_ - 4.6, hk[1] - 16, lz_)], 0.3, col("#6a6a68"), name="lantern", min_px=0.5)
    st.rope([(lx_, hk[1], lz_), (lx_ + 3.6, hk[1] - 9, lz_), (lx_ + 4.6, hk[1] - 16, lz_)], 0.3, col("#6a6a68"), name="lantern", min_px=0.5)
    yb = hk[1] - 34
    st.cyl((lx_, lz_), 5.4, yb, yb + 5, plain("#8a3a2a", 0.15), name="lantern", shadow=False)
    st.cyl((lx_, lz_), 4.2, yb + 5, yb + 15, lambda c: col("#b9cdd0") * (0.7 + 0.4 * np.cos(c.ang * 2 + 0.6))[..., None], name="lantern", shadow=False)
    st.cyl((lx_, lz_), 5.6, yb + 15, yb + 19.5, plain("#8a3a2a", 0.15), r1=2.2, name="lantern", shadow=False)
    # ---- flags on a string along the left-hand rafters, left over from a birthday
    fa, fb = on_slope("L", 236, 318, 14.5), on_slope("L", 236, 600, 14.5)
    n = 13
    pts = []
    for i in range(n + 1):
        f = i / n
        pts.append((fa[0], fa[1] - 5.0 * 4 * f * (1 - f) - 0.8 * math.sin(f * 19), fa[2] + (fb[2] - fa[2]) * f))
    st.rope([on_slope("L", 236, 318, 12.2)] + pts + [on_slope("L", 236, 600, 12.2)], 0.25, col("#d8d0b8"), name="flags", min_px=0.5)   # tied to a rafter at each end
    for i in range(n):
        (x_a, y_a, z_a), (x_b, y_b, z_b) = pts[i], pts[i + 1]
        kc = ["#d83a2c", "#f0c020", "#2c8a50", "#2c64c8", "#e8862a"][i % 5]
        st.poly([(x_a, y_a, z_a + 2), (x_b, y_b, z_b - 2), (x_a + 1.5, (y_a + y_b) / 2 - 15, (z_a + z_b) / 2)], col(kc), "flags", flag=1)
    # ---- and a big one close above us, in the angle between the nearest rafter and the boards
    zf = ATTIC.z0 + ATTIC.gap * round((1110 - ATTIC.z0) / ATTIC.gap) + ATTIC.half + 0.15
    anchors = [seen(628, 84, zf), seen(660, 112, zf), seen(698, 146, zf), seen(742, 132), seen(728, 84), seen(686, 52), seen(650, 60)]
    hub = seen(676, 100, lift=3.5)
    web = col("#7c88a4")
    rw = np.random.default_rng(5)
    for e in anchors:
        st.stick(hub, e, 0.02, web, "cobweb", min_px=0.34, emi=web * 0.30, flag=2)
    for f in (0.2, 0.36, 0.55, 0.78):
        ring = [tuple(hub[i] + (e[i] - hub[i]) * f * (0.82 + 0.36 * rw.random()) for i in range(3)) for e in anchors]
        st.rope(ring + [ring[0]], 0.02, web, name="cobweb", min_px=0.3, emi=web * 0.24, flag=2)
    for k_ in range(2):                                         # old threads hanging loose from it
        e = anchors[2 + k_ * 2]
        st.rope([e, (e[0] - 0.6, e[1] - 4, e[2] - 0.5), (e[0] - 0.2, e[1] - 9 - 3 * k_, e[2] - 1.2)], 0.02, web, name="cobweb", min_px=0.3, emi=web * 0.3, flag=2)
    # ---- a cobweb where the ridge meets the gable
    ap = (350, 397, 1.2)
    ends = [(322, 386, 1.0), (334, 376, 1.0), (350, 372, 1.0), (366, 376, 1.0), (378, 386, 1.0)]
    for e in ends:
        st.stick(ap, e, 0.12, col("#9aa4b4"), "cobweb", min_px=0.34)
    for f in (0.45, 0.75, 1.0):
        ring = [tuple(ap[i] + (e[i] - ap[i]) * f for i in range(3)) for e in ends]
        st.rope(ring, 0.1, col("#8a94a6"), name="cobweb", min_px=0.3)
    # ---- an old pair of skis kept on hooks under the left-hand rafters, pointing down the room
    for i in range(2):
        a, b = on_slope("L", 196 + i * 10, 430, 15), on_slope("L", 196 + i * 10, 640, 15)
        st.box(a[0] - 3.6, a[0] + 3.6, a[1] - 1.2, a[1] + 0.8, a[2], b[2], wood("#a83a2a" if i == 0 else "#b04434", 3 + i, "z", 0.2), "skis", shadow=False)
        st.box(a[0] - 3.6, a[0] + 3.6, a[1] - 1.2, a[1] + 0.8, a[2] + 86, a[2] + 112, col("#3a3a40"), "skis", shadow=False)       # the bindings
    for zz in (450, 620):                                       # the hooks they lie in
        a = on_slope("L", 190, zz, 12.5)
        b = on_slope("L", 214, zz, 12.5)
        st.stick(a, (a[0], a[1] - 5, zz), 0.5, col("#3a3a3a"), "skis")
        st.stick(b, (b[0], b[1] - 5.5, zz), 0.5, col("#3a3a3a"), "skis")
        st.stick((a[0], a[1] - 5, zz), (b[0], b[1] - 5.5, zz), 0.5, col("#3a3a3a"), "skis")


# ---------------------------------------------------------------- the foreground: the door, and what would not fit in the car
def m_wallpaper(c):
    """The landing's wall, seen through the doorway: its blue-green striped paper over a white dado (as the landing's
    own picture has it)."""
    u = c.X
    k = col("#a4cbc6") * (0.88 + 0.14 * (np.floor(u / 4.5) % 2))[..., None]
    k = np.where((c.Y < 92)[..., None], col("#e2d8c2") * (0.92 + 0.08 * (np.floor(u / 22) % 2))[..., None], k)
    rail = (np.abs(c.Y - 94) < 2.6)
    return np.where(rail[..., None], col("#efe6d0"), k)


def m_leaf(c):
    """The study door's landing side, which faces us now it stands open: six panels, and his notice."""
    u, v, fp = c.U, c.V, c.fp
    w, h = M.LEAF[1], M.DOORWAY[2] - 1.5
    k = np.zeros(u.shape + (3,), dtype=F32) + col(TRIMW) * (0.92 + 0.12 * fbm(u / 4, v / 40, 6, 3)[..., None])
    for (a, b) in ((10, 39), (46, 75)):
        for (cc, dd) in ((14, 72), (84, 142), (152, 190)):
            pm = rect(u, v, a, b, cc, dd, fp)
            k = k * (1 - 0.13 * pm[..., None])
            k = k * (1 - 0.5 * np.clip(rect(u, v, a, b, dd - 2.0, dd, fp) + rect(u, v, a, a + 1.8, cc, dd, fp), 0, 1)[..., None])     # the shaded step of each panel
            k = k * (1 + 0.2 * np.clip(rect(u, v, a, b, cc, cc + 1.8, fp) + rect(u, v, b - 1.7, b, cc, dd, fp), 0, 1)[..., None])
    # the notice, taped up with four bits of tape; five lines in block capitals
    nm = rect(u - (v - 118) * 0.03, v, 27, 58, 112, 150, fp)
    k = lay(k, "#f6f1e0", nm)
    for i, (a, b, th) in enumerate(((30, 55, 2.6), (31, 54, 1.4), (30, 55, 1.4), (31, 52, 1.4), (38, 55, 1.4))):
        yy = 143.5 - i * 6.0
        ln = rect(u - (v - 118) * 0.03, v, a, b, yy - th, yy, fp) * (0.55 + 0.45 * (((u * 0.9) % 1.7) < 1.25))
        k = lay(k, "#22283a", ln * (0.9 if i == 0 else 0.8))
    for (a, cc) in ((27, 148), (56, 148), (27, 112), (56, 112)):
        k = lay(k, "#e2d6a6", rect(u, v, a - 1.2, a + 3.2, cc - 1, cc + 2.4, fp) * 0.9)
    k = k * (1 - 0.25 * np.clip(1 - v / 16.0, 0, 1)[..., None])                                             # scuffed along the bottom
    return k


def door(st, G="front"):
    px, pz0 = M.PARTITION
    dz0, dz1, dh = M.DOORWAY
    top = roof_y(px) + 1
    wall = plain(WALL, 0.14, 40, 9)

    def m_part(c):
        k = wall(c)
        if c.face == "right":
            sk = (c.Y < 13)
            k = np.where(sk[..., None], col(TRIM) * (0.85 + 0.3 * fbm(c.Z / 40, c.Y / 3, 5, 2)[..., None]), k)
        return k
    st.box(px - 12, px, 0, top, pz0, dz0, m_part, "partition", G)
    st.box(px - 12, px, dh, top, dz0, dz1, m_part, "partition", G)
    st.box(px - 12, px, 0, top, dz1, 1300, m_part, "partition", G)
    tw = plain(TRIMW, 0.1, 9, 3)
    st.box(px, px + 2.2, 0, dh + 9, dz0 - 9, dz0, tw, "door", G, shadow=False)                               # the casing round the opening
    st.box(px, px + 2.2, dh, dh + 9, dz0 - 9, dz1 + 9, tw, "door", G, shadow=False)
    st.box(px, px + 2.2, 0, dh + 9, dz1, dz1 + 9, tw, "door", G, shadow=False)
    st.box(px - 12, px, 0, dh, dz0 - 1.5, dz0, tw, "door", G, shadow=False)                                  # the jamb's edge
    # what is seen through it: the landing's papered wall in the hall lamp's light, a picture on it
    st.box(0, px - 12, 0, 240, pz0 - 14, pz0 - 2, m_wallpaper, "landing", G, shadow=False)
    st.box(30, 70, 120, 168, pz0 - 2, pz0 - 0.4, lambda c: lay(np.zeros(sh(c) + (3,), F32) + col("#6a4426"), "#c8b48a", rect(c.X, c.Y, 34, 66, 124, 164, c.fp)), "landing", G, shadow=False)
    st.poly([on_slope("L", 0, pz0 - 2, 13.2), on_slope("L", 118, pz0 - 2, 13.2), on_slope("L", 118, 1300, 13.2), on_slope("L", 0, 1300, 13.2)],
            plain("#e2d6b4", 0.1, 30, 4), "landing", G)                                                      # its sloping ceiling, plastered
    st.box(18, px - 14, 0, 1.2, pz0 - 2, 1300, lambda c: col("#8a2a2a") * (0.85 + 0.3 * fbm(c.X / 3, c.Z / 3, 4, 2)[..., None]), "landing", G, shadow=False)   # the runner
    # the leaf, standing open into the room
    ang, lw = math.radians(M.LEAF[0]), M.LEAF[1]
    hx, hz = px + 1.0, dz0 + 1.0
    ex, ez = hx + lw * math.cos(ang), hz + lw * math.sin(ang)
    nx, nz = -math.sin(ang), math.cos(ang)                       # the side toward us
    th = 4.2
    st.poly([(hx, 0.8, hz), (ex, 0.8, ez), (ex, dh - 1.5, ez), (hx, dh - 1.5, hz)], m_leaf, "door", G, flag=2)
    st.poly([(ex, 0.8, ez), (ex - nx * th, 0.8, ez - nz * th), (ex - nx * th, dh - 1.5, ez - nz * th), (ex, dh - 1.5, ez)], tw, "door", G, flag=2)
    st.poly([(hx, dh - 1.5, hz), (ex, dh - 1.5, ez), (ex - nx * th, dh - 1.5, ez - nz * th), (hx - nx * th, dh - 1.5, hz - nz * th)], tw, "door", G, flag=2)
    kx, kz = hx + (lw - 7) * math.cos(ang), hz + (lw - 7) * math.sin(ang)
    st.cyl((kx + nx * 1.2, 97), 3.6, kz + nz * 0.4, kz + nz * 0.4 + 1.0, col("#b8923c"), axis="z", name="door", grp=G, shadow=False, flag=2)
    st.ball((kx + nx * 4.6, 97, kz + nz * 4.6), 3.4, plain("#d8ac48", 0.15, 3), "door", G, shadow=False, flag=2)
    for i in range(5):                                           # its shadow: the slanting leaf as a stair of thin boxes
        fa, fb = i / 5, (i + 1) / 5
        st.occ.append((hx + (ex - hx) * fa - 1, hx + (ex - hx) * fb + 1, 0, dh, hz + (ez - hz) * fa - 4.5, hz + (ez - hz) * fb - 0.5))
    st.occ.append((px - 12, px + 3, 0, dh, dz0 - 3, dz0 + 3))                                               # no light gets past the hinges
    st.feet["door"] = (px - 12, ex, dz0, ez + 2)


def m_cooler(c):
    k = col("#bf3528") * (0.9 + 0.2 * patch(c, 14, 4)[..., None])
    if c.face == "front":
        u, v, fp = c.X - c.box[0], c.Y - c.box[2], c.fp
        w, h = c.box[1] - c.box[0], c.box[3] - c.box[2]
        k = lay(k, "#f2ead6", rect(u, v, 0, w, h * 0.56, h * 0.72, fp))                                    # a white stripe round it
        k = k * (1 - 0.25 * rm(v, -1, 3.5, fp)[..., None])
    if c.face == "right":
        v, fp = c.Y - c.box[2], c.fp
        h = c.box[3] - c.box[2]
        k = lay(k, "#f2ead6", rm(v, h * 0.56, h * 0.72, fp))
    return k


_LABELS = {}


def m_maps_box(c):
    k = col("#b98f56") * (0.86 + 0.24 * patch(c, 10, 6)[..., None])
    if c.face == "front":
        u, v, fp = c.X - c.box[0], c.Y - c.box[2], c.fp
        w, h = c.box[1] - c.box[0], c.box[3] - c.box[2]
        lw, lh = 40.0, 15.0                                   # the label: MAPS, in his marker
        if "maps" not in _LABELS:
            _LABELS["maps"] = label_texture("MAPS", lw, lh)
        tex = _LABELS["maps"]
        res = tex.shape[1] / lw
        lu, lv = u - (w - lw) / 2, v - (h - lh) / 2 + 1.5
        m = rect(lu, lv, 0, lw, 0, lh, fp)
        lab = sample(tex, np.clip(lu, 0, lw - 0.01) * res, np.clip(lh - lv, 0, lh - 0.01) * res)
        k = k * (1 - m[..., None]) + lab * m[..., None]
        k = k * (1 - 0.3 * rm(v, h - 2.5, h + 1, fp)[..., None])
    return k


def m_tent(c):
    k = col("#2f6a48") * (0.82 + 0.3 * fbm(c.X / 3.0, c.ang * 2.0, 3, 3)[..., None])
    strap = (np.abs(c.along - 18) < 2.6) | (np.abs(c.along - 62) < 2.6)
    k = np.where(strap[..., None], col("#e8862a"), k)
    end = c.kind >= 3
    k = np.where(end[..., None], col("#27563c") * (0.8 + 0.4 * (c.rad < 5))[..., None], k)
    return k


def m_bag(color, stripe):
    def f(c):
        k = col(color) * (0.84 + 0.3 * fbm(c.along / 4.0, c.ang * 2.0, 5, 3)[..., None])
        band = (np.abs(c.along - 14) < 1.8) | (np.abs(c.along - (np.max(c.along) - 14)) < 1.8)
        k = np.where(band[..., None], col(stripe), k)
        end = c.kind >= 3
        spiral = ((c.rad * 0.45 + c.ang / (2 * math.pi)) % 1) < 0.5
        k = np.where(end[..., None], np.where(spiral[..., None], col(color) * 0.9, col("#c84a3a")), k)
        return k
    return f


def heap(st, G="front"):
    """What would not fit in the car, left in the middle of the floor at our feet."""
    # the big cooler, and the tent in its bag across it
    st.box(322, 396, 0, 39, 552, 604, m_cooler, "heap", G, foot=True)
    st.box(320, 398, 39, 47, 550, 606, plain("#eee6d2", 0.08, 14, 3), "heap", G)
    st.box(326, 334, 22, 30, 604, 607, col("#e6dec8"), "heap", G, shadow=False)
    st.cyl((60, 577), 12.5, 316, 404, m_tent, axis="x", name="heap", grp=G)
    st.stick((404, 60, 577), (411, 55, 580), 0.6, col("#e8dcc0"), "heap", G)
    # the box of maps
    st.box(412, 478, 0, 36, 566, 626, m_maps_box, "heap", G, foot=True)
    rng = np.random.default_rng(8)
    kcs = ["#efe6c8", "#9cc4d6", "#e4a44a", "#dfe8d4", "#d05a3a", "#efe6c8", "#5a8ab0", "#f0d890", "#c8dca8"]
    x = 415.0
    for i in range(9):
        th = 4.0 + rng.random() * 3.6
        st.box(x, x + th, 30, 41 + rng.random() * 9, 570 + rng.random() * 3, 622 - rng.random() * 4, m_book(kcs[i], i), "heap", G, shadow=False)
        x += th + 0.5
        if x > 472:
            break
    for (a, b, kc) in (((468, 30, 584), (489, 80, 568), "#f3ecd6"), ((460, 30, 598), (474, 86, 588), "#e9e0c4"), ((471, 30, 606), (496, 70, 600), "#f6f0de")):   # rolled maps stick out
        st.stick(a, b, 2.0, col(kc), "heap", G, emi=col(kc) * 0.2)      # (paper shows pale even in this corner)
        st.ball(b, 2.1, col("#b8ae92"), "heap", G, shadow=False)
        mid = tuple((a[i] + b[i]) / 2 for i in range(3))
        st.ball(mid, 2.25, col("#c8463a"), "heap", G, shadow=False)                                           # a rubber band round each
    # a sleeping bag, rolled; the lantern; the flask; a ball
    st.cyl((286, 15.5), 15.5, 548, 606, m_bag("#2f4f8a", "#e8dcc0"), axis="z", name="heap", grp=G)
    st.feet["heap2"] = (270, 302, 548, 606)
    st.cyl((500, 598), 8.0, 0, 6, plain("#2f6a50", 0.1), name="heap", grp=G, shadow=False)
    st.cyl((500, 598), 6.2, 6, 21, lambda c: col("#cfe0dc") * (0.75 + 0.35 * np.cos(c.ang * 2 + 0.8))[..., None], name="heap", grp=G)
    st.cyl((500, 598), 8.4, 21, 25.5, plain("#2f6a50", 0.1), r1=5, name="heap", grp=G, shadow=False)
    st.rope([(493, 24, 598), (492, 33, 598), (500, 37, 598), (508, 33, 598), (507, 24, 598)], 0.45, col("#b8bcc0"), name="heap", grp=G)
    st.feet["heap3"] = (492, 508, 590, 606)
    st.cyl((520, 556), 5.2, 0, 27, lambda c: np.where((((c.along * 0.4) % 1 < 0.5) ^ ((c.ang * 2.2) % 1 < 0.5))[..., None], col("#b8322a"), col("#2a2a30")), name="heap", grp=G)
    st.cyl((520, 556), 4.4, 27, 31, col("#d8dadc"), name="heap", grp=G, shadow=False)
    st.feet["heap4"] = (515, 525, 551, 561)
    st.ball((246, 11.5, 582), 11.5, lambda c: np.where((np.abs(np.sin(c.lon * 2)) < 0.07)[..., None] | (np.abs(c.lat) < 0.05)[..., None], col("#2a1a14"), col("#d8762a") * (0.85 + 0.2 * fbm(c.lon * 9, c.lat * 9, 3, 2))[..., None]), "heap", G)
    st.feet["heap5"] = (238, 254, 574, 590)
    # a duffel right at our feet, cut by the picture's edge
    st.cyl((17, 644), 17, 498, 604, m_bag("#6a5a3a", "#3a2c1c"), axis="x", name="heap", grp=G)
    # one map has slid off and lies open on the boards
    st.box(540, 590, 0, 0.6, 506, 544, lambda c: m_atlas(c) if c.face == "top" else col("#e8dfc6"), "floorbits", "back", shadow=False)


def pile(st, G="front"):
    """More of it by the end of the shelves: a suitcase on end, a rolled mat, the tackle box."""
    x0, x1, _, _, z0, z1 = M.PILE

    def m_case(c):
        k = col("#a87a44") * (0.86 + 0.26 * patch(c, 12, 5)[..., None])
        if c.face in ("front", "left"):
            a = (c.X - c.box[0]) if c.face == "front" else (c.Z - c.box[4])
            w = (c.box[1] - c.box[0]) if c.face == "front" else (c.box[5] - c.box[4])
            v, fp = c.Y - c.box[2], c.fp
            for s in (w * 0.24, w * 0.76):
                k = lay(k, "#5a3418", rm(a, s - 2.2, s + 2.2, fp))
            if c.face == "front":
                k = lay(k, "#e8dcc0", rect(a, v, w * 0.34, w * 0.62, 30, 44, fp))                           # labels from other holidays
                k = lay(k, "#3a7a9a", rect(a, v, w * 0.4, w * 0.7, 12, 24, fp))
                k = lay(k, "#d0483a", disc(a, v, w * 0.5, 52, 5.5, fp))
        return k
    st.box(x0 + 2, x0 + 22, 0, 66, z0 + 14, z0 + 62, m_case, "pile", G, foot=True)
    st.rope([(x0 + 12, 66, z0 + 30), (x0 + 12, 71, z0 + 32), (x0 + 12, 71, z0 + 44), (x0 + 12, 66, z0 + 46)], 0.9, col("#5a3418"), name="pile", grp=G)
    st.cyl((x0 + 42, z0 + 44), 11.5, 0, 62, lambda c: col("#2f7a7a") * (0.8 + 0.3 * fbm(c.ang * 3, c.along / 6.0, 4, 2)[..., None]) * np.where(c.kind >= 3, 0.8 + 0.3 * ((c.rad * 0.6) % 1 > 0.5), 1.0)[..., None],
           name="pile", grp=G)
    st.feet["pile2"] = (x0 + 30, x0 + 54, z0 + 32, z0 + 56)
    st.box(x0 + 26, x0 + 58, 0, 19, z0 + 62, z0 + 84, plain("#5a6a3a", 0.14, 8, 2), "pile", G, foot=True)   # the tackle box
    st.box(x0 + 26, x0 + 58, 19, 21, z0 + 62, z0 + 84, plain("#4a5830", 0.1), "pile", G, shadow=False)
    st.rope([(x0 + 36, 21, z0 + 73), (x0 + 37, 25, z0 + 73), (x0 + 47, 25, z0 + 73), (x0 + 48, 21, z0 + 73)], 0.7, col("#d8d8d0"), name="pile", grp=G)
    st.stick((x0 + 60, 0, z0 + 4), (x0 + 62, 150, z0 - 26), 0.75, col("#3a2a1c"), "pile", G, r1=0.3)        # a fishing rod against the shelves
    st.stick((x0 + 54, 0, z0 + 8), (x0 + 62, 136, z0 - 30), 0.7, col("#6a4426"), "pile", G, r1=0.3)

"""Everything in the room under the storehouse, built in the room's own centimetres (edo_chapel.py): the earth shell
(five planes and the hatch cut through the ceiling), the beams and props, the mats, the closet altar and what is in
it, the mirror on its stand, the lamps in their niches, the ladder, the trapdoor in its three states, the foreground.
PAINT-20F. The ray-caster is the study's (home_study_kit.Stage): each function puts one group of things on it, with a
material that paints it in its own measurements, so the skeleton, the picture and layout.json agree."""

import math

import numpy as np

from brush import F32, lerp
import edo_chapel_model as M
from home_study_kit import col, vnoise, fbm, hashf, grad_of, lines_aa, band_aa, NEAR

# ---------------------------------------------------------------- the colours of things (before any light falls on them)
EARTH = "#b48c4e"            # the dug walls: a dry loam, yellow-brown
EARTH_D = "#8a6a3c"          # its darker clods and the corners
EARTH_C = "#9a7a46"          # the ceiling's earth, dirtier
FLOOR = "#a07e4c"            # the trodden floor
MAT_A, MAT_B = "#cfae66", "#b8964e"      # straw mats, old gold
MAT_EDGE = "#3a3230"         # their cloth-bound edges
TIMBER = "#a06c38"           # the props and beams: rough timber, bark half on
TIMBER_D = "#6e3a22"
BOARD = "#a87c44"            # the ceiling boards between the beams
ALTAR_W = "#c09a5c"          # the cupboard: plain wood, newer than the room
ALTAR_IN = "#6c4a2c"         # its inside
CLOTH = "#b8402c"            # the cloth under the Kannon (a dark red)
KANNON_W = "#f0ebe2"         # white porcelain
LAMP_CLAY = "#b07c48"        # the clay lamps
BRONZE = "#c89a52"           # the mirror's face
STRAW = "#c2a060"


def patch(c, s=22.0, seed=0):
    return fbm((c.X + 0.37 * c.Y) / s, (c.Z + 0.61 * c.Y) / s, seed, 3)


def plain(color, amt=0.12, s=22.0, seed=0):
    k = col(color)

    def f(c):
        return k * (1 + amt * 2 * (patch(c, s, seed)[..., None] - 0.5))
    return f


def wood(color, seed=0, grain="x", amt=0.22, fine=2.4, long=40.0, dark=None):
    """Wood with its grain running along one of the room's directions; `dark` deepens the troughs of the grain."""
    k = col(color)
    kd = col(dark) if dark else k * 0.6

    def f(c):
        g = {"x": c.X, "y": c.Y, "z": c.Z}[grain]
        o = c.X + c.Y + c.Z - g
        n = fbm(o / fine, g / long, seed, 3)
        base = k * (1 + amt * 2 * (n[..., None] - 0.5))
        deep = np.clip((0.36 - n) * 3.0, 0, 1)
        return lerp(base, kd, (deep * 0.5)[..., None])
    return f


def earth(color, dark=EARTH_D, seed=0, s=16.0):
    """Dug earth as a print has it: one flat with the paper's tooth, a few darker clods drawn as flat shapes, a stone or two."""
    k, kd = col(color), col(dark)

    def f(c):
        n = fbm(c.X / (s * 3) + c.Y / (s * 6), c.Z / (s * 3) + c.Y / (s * 2.5), seed, 3)
        base = k * (0.95 + 0.10 * n)[..., None]
        clod = (fbm(c.X / 9.0 + c.Y / 12.0, c.Z / 9.0 + c.Y / 7.0, seed + 5, 2) > 0.66).astype(F32)
        base = lerp(base, kd, (clod * 0.55)[..., None])
        stone = (fbm(c.X / 3.5 + c.Y / 4.0, c.Z / 3.5 + c.Y / 3.0, seed + 11, 2) > 0.90).astype(F32)
        return lerp(base, col("#c8b890"), (stone * 0.6)[..., None])
    return f


def rm(u, lo, hi, fp):
    return np.clip((u - lo) / fp + 0.5, 0, 1) * np.clip((hi - u) / fp + 0.5, 0, 1)


# ---------------------------------------------------------------- the shell: five planes, the hatch cut out of the ceiling
def shell(st, state):
    """The floor, the back wall, the two side walls and the ceiling, each a plane the rays meet; the hatch is left
    out of the ceiling and drawn as a shaft (hatch())."""
    C, dX, dY, dZ = st.C, st.dX, st.dY, st.dZ
    big = np.float32(1e9)

    def plane(num, den):
        with np.errstate(divide="ignore", invalid="ignore"):
            t = num / den
        return np.where((den < 0) & (t > 0), t, big).astype(F32)

    tF = plane(-C[1], dY)                      # floor Y = 0 (f = Y)
    tC = plane(-(M.H - C[1]), -dY)             # ceiling Y = H (f = H - Y)
    tB = plane(-C[2], dZ)                      # back wall Z = 0
    tL = plane(-C[0], dX)                      # left wall X = 0
    tR = plane(-(M.W - C[0]), -dX)             # right wall X = W
    ts = np.stack([tF, tC, tB, tL, tR])
    which = ts.argmin(axis=0)
    t = ts.min(axis=0)
    X, Y, Z = C[0] + t * dX, C[1] + t * dY, C[2] + t * dZ
    normals = [(0, 1, 0), (0, -1, 0), (0, 0, 1), (1, 0, 0), (-1, 0, 0)]
    keys = ["floor", "ceiling", "back", "left", "right"]
    mats = {"floor": m_floor, "ceiling": m_ceiling, "back": m_back, "left": m_side, "right": m_side}
    hx0, hx1, hz0, hz1 = M.HATCH
    full = (slice(None), slice(None))
    for k, key in enumerate(keys):
        m = (which == k) & (t > NEAR) & (t < st.t)
        if key == "ceiling":
            m &= ~((X > hx0) & (X < hx1) & (Z > hz0) & (Z < hz1))
        if not m.any():
            continue
        r = mats[key](Ctx(m=m, face=key, n=normals[k], X=X, Y=Y, Z=Z, t=t, ss=st.ss, F=st.v.F, state=state))
        a, e = r if isinstance(r, tuple) else (r, None)
        st._put(full, m, t, normals[k], a[m] if isinstance(a, np.ndarray) and a.ndim == 3 else a,
                (e[m] if isinstance(e, np.ndarray) and e.ndim == 3 else e), key, "back", 0)


class Ctx:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def m_floor(c):
    X, Z = c.X, c.Z
    gX, gZ = grad_of(X) * c.ss, grad_of(Z) * c.ss
    base = earth(FLOOR, "#5e4430", 3, 20.0)(c)
    # the floor is trodden smooth in the middle and dusty at the walls
    base = base * (0.92 + 0.12 * np.clip((Z - 20) / 200, 0, 1))[..., None]
    # ---- the straw mats, laid in strips along Z, each bound with dark cloth along its long edges
    x0, x1, z0, z1 = M.MATS
    wob = (fbm(X / 70, Z / 70, 77, 2) - 0.5) * 3
    inr = band_aa(X + wob, x0, x1, gX) * band_aa(Z + wob * 0.6, z0, z1, gZ)
    u = X - x0
    strip = np.floor(u / M.MAT_W)
    tone = hashf(strip, 21)
    mat = lerp(col(MAT_A), col(MAT_B), tone[..., None])
    weave = lines_aa(Z, 1.9, 0.8, gZ) * 0.14 + lines_aa(u, 0.9, 0.5, gX) * 0.06 + (fbm(u / 3.0, Z / 9.0, 9, 2) - 0.5) * 0.14
    mat = mat * (1 - weave[..., None])
    # darker where it is sat and walked on, by the altar's foot and the middle
    worn = np.clip((fbm(X / 60, Z / 50, 91, 3) - 0.4) * 1.8, 0, 1)
    mat = lerp(mat, mat * col("#b89a74") * 1.05, (worn * 0.4)[..., None])
    fu = u - strip * M.MAT_W
    edge = np.clip(1 - np.minimum(fu, M.MAT_W - fu) / 2.6, 0, 1) * np.clip((M.MAT_W / gX - 6) / 6, 0, 1)
    mat = lerp(mat, col(MAT_EDGE), (edge * 0.9)[..., None])
    ends = 1 - band_aa(Z, z0 + 2.4, z1 - 2.4, gZ)
    mat = lerp(mat, col(MAT_EDGE) * 1.2, (ends * 0.8)[..., None])
    frayed = np.clip((fbm(X / 5, Z / 5, 33, 2) - 0.5) * 2, 0, 1) * (1 - band_aa(Z, z0 + 6, z1 - 6, gZ)) * (1 - ends)
    mat = lerp(mat, col(STRAW), (frayed * 0.35)[..., None])
    out = lerp(base, mat, inr[..., None])
    return out


def m_back(c):
    X, Y = c.X, c.Y
    base = earth(EARTH, EARTH_D, 1)(c)
    # soot above each lamp's niche, and a sooted halo on the ceiling line
    for name, (lx, ly, lz, wall) in M.LAMPS.items():
        if wall != "back":
            continue
        soot = (np.exp(-((X - lx) / 16.0) ** 2) * np.clip((Y - ly) / 30.0, 0, 1) * np.exp(-np.clip(Y - ly - 20, 0, 1e4) / 40.0) > 0.3).astype(F32)
        base = base * (1 - 0.3 * soot)[..., None]
    base = base * (1 - 0.18 * np.clip((Y - M.H + 18) / 18, 0, 1))[..., None]
    base = base * (1 - 0.22 * np.exp(-Y / 8.0))[..., None]
    return base


def m_side(c):
    Z, Y = c.Z, c.Y
    base = earth(EARTH, EARTH_D, 2, 15.0)(c)
    for name, (lx, ly, lz, wall) in M.LAMPS.items():
        if wall == "left" and c.face == "left":
            soot = (np.exp(-((Z - lz) / 16.0) ** 2) * np.clip((Y - ly) / 30.0, 0, 1) * np.exp(-np.clip(Y - ly - 20, 0, 1e4) / 40.0) > 0.3).astype(F32)
            base = base * (1 - 0.3 * soot)[..., None]
    base = base * (1 - 0.18 * np.clip((Y - M.H + 18) / 18, 0, 1))[..., None]
    base = base * (1 - 0.22 * np.exp(-Y / 8.0))[..., None]
    return base


def m_ceiling(c):
    """Rough boards laid along Z between the beams, resting on them, earth showing in the gaps."""
    X, Z = c.X, c.Z
    gX, gZ = grad_of(X) * c.ss, grad_of(Z) * c.ss
    soil = earth(EARTH_C, "#4e3826", 4, 14.0)(c)
    bw = 21.0
    ib = np.floor((X + 7 * hashf(np.floor(Z / 140.0), 3)) / bw)
    tone = hashf(ib + np.floor(Z / 140.0) * 97, 8)
    brd = wood(BOARD, 6, "z", 0.2, 2.2, 55.0)(c) * (0.84 + 0.3 * tone)[..., None]
    gap = lines_aa(X, bw, 1.6 + 2.0 * hashf(ib, 4), gX)
    missing = (hashf(ib * 7 + np.floor(Z / 140.0), 13) > 0.86).astype(F32)
    board = lerp(brd, soil, np.maximum(gap, missing)[..., None])
    # dark between the boards' ends and a sooted patch over each lamp
    for name, (lx, ly, lz, wall) in M.LAMPS.items():
        if wall == "stand":
            continue
        px = lx if wall != "left" else 10.0
        pz = lz if wall != "back" else 10.0
        soot = (np.exp(-(((X - px) / 34.0) ** 2 + ((Z - pz) / 34.0) ** 2)) > 0.4).astype(F32)
        board = board * (1 - 0.32 * soot)[..., None]
    return board


# ---------------------------------------------------------------- the timber: beams and props
def beams(st):
    for z in M.BEAMS_Z:
        st.box(0, M.W, M.BEAM_Y, M.H + 2, z - M.BEAM_T / 2, z + M.BEAM_T / 2, wood(TIMBER, 12, "x", 0.24, 2.6, 60.0, TIMBER_D), "beam", "back")
    for (x, z) in M.POSTS:
        st.cyl((x, z), M.POST_R, 0, M.BEAM_Y + 1, wood(TIMBER, 13, "y", 0.28, 2.0, 50.0, TIMBER_D), name="post", grp="props" if z > 150 else "back")
        st.box(x - 10, x + 10, M.BEAM_Y - 4, M.BEAM_Y + 1, z - 9, z + 9, wood(TIMBER_D, 14), "post", "props" if z > 150 else "back")   # the cap it carries the beam on
    fx, fz = M.FRONT_POST
    st.cyl((fx, fz), M.POST_R + 1.5, 0, M.BEAM_Y + 1, wood(TIMBER, 15, "y", 0.3, 2.0, 50.0, TIMBER_D), name="frontpost", grp="front")
    st.box(fx - 12, fx + 12, M.BEAM_Y - 5, M.BEAM_Y + 1, fz - 10, fz + 10, wood(TIMBER_D, 16), "frontpost", "front")


# ---------------------------------------------------------------- the closet altar
def altar(st, doors_open=False):
    x0, x1, y0, y1, z0, z1 = M.ALTAR
    ph = M.PLINTH_H
    carcass = wood(ALTAR_W, 21, "y", 0.16, 2.6, 44.0, "#7a5636")
    st.box(x0 - 3, x1 + 3, 0, ph, z0, z1 + 2, wood("#8a6640", 22, "x"), "altar", "altar", foot=True)           # the plinth
    st.box(x0, x1, ph, ph + 2.5, z0, z1 - M.DOOR_T, carcass, "altar", "altar")                                  # the bottom board
    st.box(x0, x0 + 3, ph, y1, z0, z1 - M.DOOR_T, carcass, "altar", "altar")                                    # the sides
    st.box(x1 - 3, x1, ph, y1, z0, z1 - M.DOOR_T, carcass, "altar", "altar")
    st.box(x0 - 2, x1 + 2, y1 - 3.5, y1, z0, z1 + 1.5, carcass, "altar", "altar")                               # the top board, a little proud
    st.box(x0 + 3, x1 - 3, ph, y1 - 3.5, z0, z0 + 1.6, plain(ALTAR_IN, 0.1, 10, 23), "altar", "altar", shadow=False)   # the back board
    st.box(x0 + 3, x1 - 3, M.SHELF_Y - 2.2, M.SHELF_Y, z0 + 1.6, z1 - M.DOOR_T - 2, carcass, "altar", "altar")  # the shelf
    # ---- inside: the cloth, the Kannon with the child, the calendar sheet, the bowl of water
    kx, kh, kr = M.KANNON
    st.box(kx - 15, kx + 15, M.SHELF_Y, M.SHELF_Y + 0.8, z0 + 4, z1 - M.DOOR_T - 5, plain(CLOTH, 0.14, 6, 24), "cloth", "altar", shadow=False)
    kz = (z0 + z1 - M.DOOR_T) / 2 + 1
    white = plain(KANNON_W, 0.03, 5, 25)
    kemi = col("#f6eed8") * 0.14
    st.cyl((kx, kz), kr, M.SHELF_Y + 0.8, M.SHELF_Y + kh * 0.66, white, r1=3.6, name="kannon", grp="altar", emi=kemi)        # the robe: wide at the hem, the shoulders narrow
    st.cyl((kx, kz), 3.6, M.SHELF_Y + kh * 0.66, M.SHELF_Y + kh * 0.78, white, r1=2.0, name="kannon", grp="altar", emi=kemi)  # the shoulders to the neck
    st.ball((kx, M.SHELF_Y + kh * 0.84, kz), 3.4, white, "kannon", "altar", emi=kemi)                                          # the head
    st.cyl((kx, kz), 3.0, M.SHELF_Y + kh * 0.9, M.SHELF_Y + kh, white, r1=1.6, name="kannon", grp="altar", emi=kemi)          # the high hair and hood
    st.ball((kx - 1.2, M.SHELF_Y + kh * 0.5, kz + 4.2), 2.3, white, "kannon", "altar", emi=kemi)                               # the child, held at her breast
    st.ball((kx - 1.6, M.SHELF_Y + kh * 0.58, kz + 5.2), 1.3, white, "kannon", "altar", emi=kemi)
    cx0, cx1, cy0, cy1 = M.CALENDAR
    st.poly([(cx0, cy0, z0 + 8), (cx1, cy0, z0 + 8), (cx1, cy1, z0 + 2.4), (cx0, cy1, z0 + 2.4)], calendar_mat, "calendar", "altar")
    bx, bz, br, bh = M.BOWL
    st.cyl((bx, bz), br * 0.7, M.SHELF_Y, M.SHELF_Y + bh, wood("#6a4a30", 26, "y", 0.14), r1=br, name="bowl", grp="altar", hollow=False)
    st.cyl((bx, bz), br - 0.8, M.SHELF_Y + bh - 0.6, M.SHELF_Y + bh - 0.2, water_mat, name="bowl", grp="altar", shadow=False, emi=col("#2a3a50") * 0.08)
    # ---- the doors: shut, two leaves meeting in the middle; open, each swung out on its hinge edge
    dw = (x1 - x0) / 2
    dmat = wood(ALTAR_W, 27, "y", 0.16, 2.6, 44.0, "#7a5636")
    if not doors_open:
        for k, (a, b) in enumerate(((x0, x0 + dw), (x0 + dw, x1))):
            st.box(a + 0.6, b - 0.6, ph + 2.5, y1 - 3.5, z1 - M.DOOR_T, z1, dmat, "doors", "altar")
            st.box(a + 2.4, b - 2.4, ph + 8, y1 - 9, z1, z1 + 0.5, door_panel(k), "doors", "altar", shadow=False)   # a raised panel's line
        st.box(x0 + dw - 1.2, x0 + dw + 1.2, ph + 3, y1 - 4, z1 - 0.2, z1 + 0.3, plain("#4a3222", 0.1), "doors", "altar", shadow=False)   # the meeting line
        st.box(x0 + dw - 4.5, x0 + dw + 4.5, (y1 + ph) / 2 - 1.2, (y1 + ph) / 2 + 1.2, z1, z1 + 1.2, plain("#5a4a3a", 0.1), "doors", "altar", shadow=False)   # the wooden turn-latch
    else:
        a = math.radians(M.DOORS_OPEN)
        for k, hx in enumerate((x0, x1)):
            sgn = -1 if k == 0 else 1
            ex, ez = hx + sgn * (-dw * math.cos(a)), z1 + dw * math.sin(a)          # the free edge, swung out into the room
            pts = [(hx, ph + 2.5, z1), (ex, ph + 2.5, ez), (ex, y1 - 3.5, ez), (hx, y1 - 3.5, z1)]
            st.poly(pts, dmat, "doors", "altar")
            occ_box(st, min(hx, ex), max(hx, ex), ph + 2.5, y1 - 3.5, min(z1, ez), max(z1, ez), steps=4)


def occ_box(st, x0, x1, y0, y1, z0, z1, steps=4):
    """A slanted flat thing's shadow, as a few small boxes along its diagonal."""
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        st.occ.append((x0 + (x1 - x0) * t0, x0 + (x1 - x0) * t1, y0, y1, z0 + (z1 - z0) * t0, z0 + (z1 - z0) * t1))


def door_panel(k):
    def f(c):
        return col(ALTAR_W) * 0.86 * (1 + 0.1 * (fbm(c.X / 2.4, c.Y / 44, 40 + k, 2)[..., None] - 0.5))
    return f


def calendar_mat(c):
    """A folded sheet of soft paper, written in columns (marks, not letters), gone brown at the folds."""
    k = col("#e8dcc0") * (0.92 + 0.12 * fbm(c.U / 3, c.V / 3, 44, 2)[..., None])
    fold = np.exp(-((c.V - 9.0) / 0.9) ** 2) * 0.35
    cols = np.zeros(c.U.shape, dtype=F32)
    for cu in (3.0, 6.2, 9.4, 12.2):
        cols += np.clip(1 - np.abs(c.U - cu) / 0.45, 0, 1) * (fbm(c.V / 1.2, c.U, 45, 1) > 0.42)
    cols *= band_aa(c.V, 1.5, 16.5, 0.6)
    return lerp(k * (1 - fold)[..., None], col("#3a2a20"), np.clip(cols, 0, 0.8)[..., None])


def water_mat(c):
    return col("#4a5a70") * (0.9 + 0.2 * fbm(c.X / 2, c.Z / 2, 46, 2)[..., None])


# ---------------------------------------------------------------- the mirror on its stand
def mirror(st, with_mirror=True):
    x0, x1, y0, y1, z0, z1 = M.STAND
    wd = wood("#9a7446", 31, "x", 0.18, 2.4, 30.0, "#5e4228")
    st.box(x0, x1, 0, 3, z0 - 2, z1 + 2, wd, "stand", "back", foot=True)                        # its foot
    st.box(x0 + 6, x1 - 6, 3, y1 - 6, z0 + 6, z1 - 6, wd, "stand", "back")                      # the post
    st.box(x0, x1, y1 - 6, y1, z0, z1, wd, "stand", "back")                                     # the ledge the mirror rests on
    st.box(x0 + 3, x1 - 3, y1, y1 + 14, z0, z0 + 2.4, wd, "stand", "back")                      # the back rest (the mirror leans on it)
    if with_mirror:
        mx, my, mz, mr = M.MIRROR
        bronze = plain(BRONZE, 0.1, 4, 32)
        st.cyl((mx, my), mr, mz - 1.4, mz, bronze, axis="z", name="mirror", grp="mirror", emi=col("#ffd090") * 0.12)
        st.cyl((mx, my), mr - 1.0, mz, mz + 0.3, mirror_face, axis="z", name="mirror", grp="mirror", shadow=False, emi=col("#ffe0b0") * 0.22)


def mirror_face(c):
    """The polished face: it gives back the lamplight as a soft bright centre and the room's dark round it."""
    r = np.hypot(c.X - M.MIRROR[0], c.Y - M.MIRROR[1]) / (M.MIRROR[3] - 1.0)
    return lerp(col("#e8c070"), col("#6a4a30"), np.clip(r * 1.2 - 0.1, 0, 1)[..., None])


# ---------------------------------------------------------------- the lamps in their niches
def lamp_places():
    """The flame of each lamp: (name, (X, Y, Z))."""
    out = {}
    nw, nh, nd = M.NICHE
    for name, (lx, ly, lz, wall) in M.LAMPS.items():
        if wall == "back":
            out[name] = (lx, ly + M.LAMP_H + 1.5, nd * 0.45)
        elif wall == "left":
            out[name] = (nd * 0.45, ly + M.LAMP_H + 1.5, lz)
        else:
            out[name] = (lx, ly + M.LAMP_H + 1.5, lz)
    return out


def lamps(st, lit=True):
    nw, nh, nd = M.NICHE
    for name, (lx, ly, lz, wall) in M.LAMPS.items():
        # a niche: a hollow cut into the earth with a board on its floor (drawn as a dark box behind the wall's plane)
        if wall == "back":
            st.box(lx - nw / 2, lx + nw / 2, ly - 2.5, ly + nh, -nd, 0.5, niche_mat, "niche", "back", shadow=False, flag=2)
            st.box(lx - nw / 2 - 1, lx + nw / 2 + 1, ly - 2.5, ly, -nd, 1.0, wood("#8a6436", 51, "x"), "niche", "back", shadow=False)
            cx, cz = lx, nd * 0.45
        elif wall == "left":
            st.box(-nd, 0.5, ly - 2.5, ly + nh, lz - nw / 2, lz + nw / 2, niche_mat, "niche", "back", shadow=False, flag=2)
            st.box(-nd, 1.0, ly - 2.5, ly, lz - nw / 2 - 1, lz + nw / 2 + 1, wood("#8a6436", 52, "z"), "niche", "back", shadow=False)
            cx, cz = nd * 0.45, lz
        else:                                                                      # the lamp stand: a post and a top board
            pw, tw = M.LAMP_STAND
            wd = wood("#9a7446", 55, "y", 0.16, 2.0, 30.0, "#6e3a22")
            st.box(lx - tw / 2, lx + tw / 2, 0, 2.5, lz - tw / 2, lz + tw / 2, wd, "lampstand", "back", foot=True)
            st.box(lx - pw / 2, lx + pw / 2, 2.5, ly - 2.0, lz - pw / 2, lz + pw / 2, wd, "lampstand", "back")
            st.box(lx - tw / 2, lx + tw / 2, ly - 2.0, ly, lz - tw / 2, lz + tw / 2, wd, "lampstand", "back")
            cx, cz = lx, lz
        clay = plain(LAMP_CLAY, 0.08, 4, 53)
        st.cyl((cx, cz), M.LAMP_R * 0.7, ly, ly + M.LAMP_H, clay, r1=M.LAMP_R, name=name, grp="lamps", shadow=False,
               emi=(col("#f4d88e") * 0.16 if lit else None))
        st.cyl((cx, cz), M.LAMP_R - 1.2, ly + M.LAMP_H - 0.5, ly + M.LAMP_H, (lambda c: col("#f2b42e")) if lit else plain("#4a3a30", 0.1), name=name, grp="lamps", shadow=False,
               emi=(col("#f2b42e") * 0.9 if lit else None))                                     # the oil's surface, alight: the one chrome yellow
        # the spout toward the room, and the wick's black tip
        sx = cx + (0 if wall != "left" else M.LAMP_R + 1.5)
        sz = cz + (M.LAMP_R + 1.5 if wall != "left" else 0)
        st.ball((sx, ly + M.LAMP_H - 0.5, sz), 1.8, clay, name, "lamps", shadow=False, emi=(col("#f4d88e") * 0.2 if lit else None))
        st.ball((sx, ly + M.LAMP_H + 0.8, sz), 0.8, "#1a2846", name, "lamps", shadow=False)


def niche_mat(c):
    return col(EARTH_D) * 0.7 * (0.9 + 0.2 * fbm(c.X / 4 + c.Z / 4, c.Y / 4, 54, 2)[..., None])


# ---------------------------------------------------------------- the ladder and the trapdoor
def ladder(st):
    L = M.LADDER
    xa, xb = L["x"]
    p0, p1 = (0.0, L["foot_z"]), (L["top_y"], L["top_z"])
    rail = wood("#8a6640", 61, "y", 0.22, 2.0, 40.0, "#4e3620")
    for x in (xa, xb):
        st.stick((x, p0[0], p0[1]), (x, p1[0], p1[1]), L["rail"], rail, "ladder", "ladder")
        n = 10
        for i in range(n):                                                   # the rails' shadows, as small boxes along them
            t0, t1 = i / n, (i + 1) / n
            st.occ.append((x - L["rail"], x + L["rail"], p0[0] + (p1[0] - p0[0]) * t0, p0[0] + (p1[0] - p0[0]) * t1,
                           min(p0[1] + (p1[1] - p0[1]) * t0, p0[1] + (p1[1] - p0[1]) * t1) - 1, max(p0[1] + (p1[1] - p0[1]) * t0, p0[1] + (p1[1] - p0[1]) * t1) + 1))
    y, k = L["rung"] * 0.8, 0
    while y < M.H + 6:
        t = y / p1[0]
        z = p0[1] + (p1[1] - p0[1]) * t
        st.stick((xa - 1, y, z), (xb + 1, y, z), 1.9, wood("#9a7446", 62 + k, "x", 0.2, 1.6, 20.0), "ladder", "ladder")
        st.occ.append((xa, xb, y - 1.9, y + 1.9, z - 1.9, z + 1.9))
        y += L["rung"]
        k += 1


def hatch(st, trap="shut"):
    """The shaft through the earth and the boards above, and what is at its top: the leaf shut; open, the dark of the
    storehouse by lamplight; open, the morning's daylight."""
    hx0, hx1, hz0, hz1 = M.HATCH
    top = M.H + M.HATCH_T
    soil = earth(EARTH_C, "#4e3826", 71, 10.0)
    brd = wood(BOARD, 72, "x", 0.2, 2.2, 50.0)
    # the shaft's four sides: earth below, the storehouse floor's boards cut through above
    for (pts) in (
        [(hx0, M.H, hz0), (hx1, M.H, hz0), (hx1, top, hz0), (hx0, top, hz0)],        # the far side (faces us)
        [(hx0, M.H, hz1), (hx1, M.H, hz1), (hx1, top, hz1), (hx0, top, hz1)],        # the near side (faces away: not seen)
        [(hx0, M.H, hz0), (hx0, M.H, hz1), (hx0, top, hz1), (hx0, top, hz0)],        # the left side
        [(hx1, M.H, hz0), (hx1, M.H, hz1), (hx1, top, hz1), (hx1, top, hz0)],        # the right side
    ):
        st.poly(pts, shaft_mat(soil, brd), "hatch", "hatch", emi=(col("#9ab8d8") * 0.10 if trap == "day" else None))
    # the hatch's wooden rim on the room's side (a frame the leaf closes on)
    for (a, b, c_, d) in ((hx0 - 7, hx0, hz0 - 7, hz1 + 7), (hx1, hx1 + 7, hz0 - 7, hz1 + 7), (hx0, hx1, hz0 - 7, hz0), (hx0, hx1, hz1, hz1 + 7)):
        st.box(a, b, M.H - 3.5, M.H + 0.5, c_, d, wood("#c09050", 73, "x" if d - c_ > b - a else "z", 0.2, 2.0, 40.0, "#6e3a22"), "hatch", "hatch", shadow=False)
    if trap == "shut":
        # the leaf: the hole's own size less a finger's gap all round, resting on the rim above; through the gap the storehouse's
        # lantern shows as a line of light round its edge
        g = 1.8
        st.box(hx0 + g, hx1 - g, top - 3.5, top + 0.5, hz0 + g, hz1 - g, wood("#8a6a44", 74, "z", 0.26, 2.2, 40.0, "#4e3620"), "trapdoor", "hatch", shadow=False)
        for z in (hz0 + 14, hz1 - 14):                                                 # the two battens on its underside
            st.box(hx0 + g + 2, hx1 - g - 2, top - 6.5, top - 3.5, z - 3, z + 3, wood("#5a3e24", 75, "x"), "trapdoor", "hatch", shadow=False)
        st.poly([(hx0 - 3, top + 0.6, hz0 - 3), (hx1 + 3, top + 0.6, hz0 - 3), (hx1 + 3, top + 0.6, hz1 + 3), (hx0 - 3, top + 0.6, hz1 + 3)],
                (lambda c: col("#f4d88e")), "trapdoor", "hatch", emi=col("#f4d88e") * 1.6)   # the lit storehouse floor over the gap
        # the lantern's light through the gap falls on the top of the shaft's far side and its two sides: the line of light at the leaf's edge
        glow = col("#f4d88e") * 1.3
        st.box(hx0 + 0.2, hx1 - 0.2, top - 3.2, top - 0.2, hz0 + 0.1, hz0 + 0.7, (lambda c: col("#f6eed8")), "trapdoor", "hatch", shadow=False, emi=glow)
        st.box(hx0 + 0.1, hx0 + 0.7, top - 3.2, top - 0.2, hz0, hz1, (lambda c: col("#f6eed8")), "trapdoor", "hatch", shadow=False, emi=glow)
        st.box(hx1 - 0.7, hx1 - 0.1, top - 3.2, top - 0.2, hz0, hz1, (lambda c: col("#f6eed8")), "trapdoor", "hatch", shadow=False, emi=glow)
    elif trap == "lamp":
        st.poly([(hx0 - 2, top + 0.5, hz0 - 2), (hx1 + 2, top + 0.5, hz0 - 2), (hx1 + 2, top + 0.5, hz1 + 2), (hx0 - 2, top + 0.5, hz1 + 2)],
                storehouse_dark, "trapdoor", "hatch", emi=col("#5a3a22") * 0.10)
    else:
        st.poly([(hx0 - 2, top + 0.5, hz0 - 2), (hx1 + 2, top + 0.5, hz0 - 2), (hx1 + 2, top + 0.5, hz1 + 2), (hx0 - 2, top + 0.5, hz1 + 2)],
                daylight, "trapdoor", "hatch", emi=col("#dceeff") * 1.9)


def shaft_mat(soil, brd):
    def f(c):
        s = soil(c)
        b = brd(c)
        k = np.clip((c.Y - M.H - 1.0) / 1.5, 0, 1)                                       # the boards begin at once (the shaft is 8 cm: boards on boards)
        out = lerp(s, b * 0.8, k[..., None])
        return out
    return f


def storehouse_dark(c):
    return col("#2a1c14") * (0.9 + 0.3 * fbm(c.X / 6, c.Z / 6, 81, 2)[..., None])


def daylight(c):
    return col("#e6f2ff")


# ---------------------------------------------------------------- the foreground
def foreground(st):
    bx, bz, br, bh = M.BASKET
    st.cyl((bx, bz), br * 0.8, 0, bh, basket_mat, r1=br, name="basket", grp="back")
    st.cyl((bx, bz), br - 1.5, bh - 1.5, bh + 3.5, plain("#1c1612", 0.2, 3, 91), name="charcoal", grp="back", shadow=False)   # the charcoal heaped in it
    jx, jz, jr, jh = M.JAR
    st.cyl((jx, jz), jr * 0.6, 0, jh * 0.55, plain("#8a5a36", 0.08, 6, 92), r1=jr, name="jar", grp="back")
    st.cyl((jx, jz), jr, jh * 0.55, jh, plain("#8a5a36", 0.08, 6, 93), r1=jr * 0.55, name="jar", grp="back")
    st.cyl((jx, jz), jr * 0.55, jh, jh + 2.5, plain("#9a6a40", 0.08, 6, 94), name="jar", grp="back", shadow=False)
    sx0, sx1, sy0, sy1, sz0, sz1 = M.SACK
    st.cyl(((sy0 + sy1) / 2 * 0.9, (sz0 + sz1) / 2), (sy1 - sy0) / 2 * 1.15, sx0, sx1, sack_mat, axis="x", name="sack", grp="back")
    st.cyl(((sy0 + sy1) / 2 * 0.9, (sz0 + sz1) / 2), (sy1 - sy0) / 2 * 0.9, sx1, sx1 + 7, plain("#6e5a44", 0.1, 4, 96), r1=3.0, axis="x", name="sack", grp="back")   # its tied neck


def basket_mat(c):
    """Woven bamboo: the weave as crossing bands round it."""
    a = (c.ang + math.pi) / (2 * math.pi) * 36.0
    w = np.abs(((a + c.along / 2.6) % 2) - 1) * 0.5 + np.abs(((a - c.along / 2.6) % 2) - 1) * 0.5
    return col("#b89050") * (0.8 + 0.35 * w)[..., None]


def sack_mat(c):
    return col("#8c7c5c") * (0.9 + 0.2 * fbm(c.X / 3, (c.Y + c.Z) / 3, 95, 3)[..., None]) * (0.7 + 0.3 * np.clip(c.n[..., 1] if hasattr(c.n, "ndim") and c.n.ndim == 2 else 1.0, 0, 1))[..., None]


# ---------------------------------------------------------------- the whole room
def build(st, doors_open=False, trap="shut", lit=True, with_mirror=True):
    shell(st, trap)
    beams(st)
    hatch(st, trap)
    altar(st, doors_open)
    mirror(st, with_mirror)
    lamps(st, lit)
    ladder(st)
    foreground(st)

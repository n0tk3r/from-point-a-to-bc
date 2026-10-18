"""The shell of the break room and what is built into it, in the room's own centimetres (office_breakroom.py): the
vinyl tiles, the painted block walls, the ceiling of tiles in their grid with its two fluorescent fittings, the speaker
and the return grille over the fridge (and the duct's dark mouth behind it); the door to the hall, shut or standing
open, and the hall beyond it; the calendar on the left wall. OFFICE-17D.

Each function puts one group of things on the Stage (office_breakroom_kit.Stage) with a paint that colours it in ITS
OWN measurements, so every line runs to its vanishing point by itself. The hall beyond the door is lit by its own
tubes: it is painted self-lit (`emi`) and flagged OUTSIDE, so that the room's lamps leave it alone. Every word is a
plain word; nothing here is anybody's brand."""

import math

import numpy as np

from brush import F32, lerp
import office_breakroom_model as M
from office_breakroom_kit import (normals, col, mixc, vnoise, fbm, hashf, grad_of, lines_aa, band, rect, disc, lay, sstep,
                                  curve3, Ctx)

OUTSIDE = 4                      # the flag: beyond the room's walls (self-lit, the room's lamps leave it alone)

# ---------------------------------------------------------------- the colours of things (before any light falls on them)
WALL = "#d9d7b2"                 # painted block: an eggshell beige, gone a little green under forty years of tubes
WALL_LOW = "#cbc8a2"             # the same paint, scuffed and a shade darker where chairs and elbows have been
BASE = "#4a3c34"                 # the rubber cove base
TILE_A, TILE_B, TILE_C = "#dcd4ba", "#b4bca0", "#b8a890"     # the vinyl tiles: cream, a sage and a taupe
CEIL = "#dedcd0"                 # the ceiling's tiles
GRID = "#ecebe2"                 # the grid they lie in
PAPER = "#f4efe0"


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
    """Wood (or a wood-grain veneer) with its grain running along one of the room's directions."""
    k = col(color)

    def f(c):
        g = {"x": c.X, "y": c.Y, "z": c.Z}[grain]
        o = c.X + c.Y + c.Z - g
        n = fbm(o / fine, g / long, seed, 3)
        return k * (1 + amt * 2 * (n[..., None] - 0.5))
    return f


def metal(color, seed=0, amt=0.1):
    """Painted or enamelled metal: smooth, a little mottled, chipped here and there."""
    k = col(color)

    def f(c):
        n = fbm(c.X / 9, (c.Y + c.Z) / 9, seed, 2)
        chip = np.clip((fbm(c.X / 2.5, (c.Y + c.Z * 0.5) / 2.5, seed + 7, 2) - 0.8) * 9, 0, 1)
        out = k * (1 + amt * 2 * (n[..., None] - 0.5))
        return lay(out, "#6a5e52", chip * 0.6)
    return f


def chrome(tint="#c8ccd2", glint=0.5, seed=0):
    """Chrome or steel: mostly the room it shows, a mid grey that takes the light, bright where it faces up toward the
    tubes, dark where it faces the floor."""
    k = col(tint)

    def f(c):
        if hasattr(c, "n"):
            n = normals(c)
            up = np.clip(n[:, 1] * 0.8 + n[:, 2] * 0.35, 0, 1)
            down = np.clip(-n[:, 1] * 0.9, 0, 1)
        else:                                                    # a rod (Stage.stick): lit along its middle, dark at its sides
            sd = np.abs(np.asarray(c.side, dtype=F32))
            up = np.clip(0.95 - sd * 0.9, 0, 1)
            down = np.clip(sd - 0.55, 0, 1)
        out = k[None, :] * (0.55 + 0.55 * up - 0.3 * down)[:, None]
        out = out * (0.92 + 0.16 * fbm(c.X / 3 + seed, (c.Y + c.Z) / 3, 7 + seed, 2))[:, None]
        e = col("#f4f8ec")[None, :] * (np.clip(up - 0.7, 0, 1) * glint * 1.8)[:, None]
        return out, e
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
    """Vinyl tiles a foot square, cream and sage in a check, chips of colour in them as such tiles have; waxed, so the
    light lies on them as a sheen (added with the light); worn pale on the way from the door to the coffee."""
    X, Z = c.X, c.Z
    gX, gZ = grad_of(X) * c.ss, grad_of(Z) * c.ss
    T = 30.5
    ix, iz = np.floor(X / T), np.floor(Z / T)
    pick = hashf(ix * 57 + iz * 911, 11)                         # laid as such floors are: mostly cream, sage and taupe here and there
    base = np.where((pick < 0.24)[..., None], col(TILE_B), np.where((pick > 0.88)[..., None], col(TILE_C), col(TILE_A)))
    base = base * (0.94 + 0.10 * hashf(ix * 131 + iz, 3))[..., None]
    base = base * (0.94 + 0.12 * fbm(X / 7, Z / 7, 21, 3)[..., None])
    chips = fbm(X / 1.3, Z / 1.3, 22, 2)
    base = lay(base, "#8a8470", np.clip((chips - 0.72) * 5, 0, 1) * 0.45)
    base = lay(base, "#f2ecd8", np.clip((0.26 - chips) * 5, 0, 1) * 0.40)
    # worn: from the door to the counter's right end, and along the counter
    path = np.exp(-((Z - 120 - (X - 690) * 0.25) / 55.0) ** 2) * np.clip((X - 300) / 120, 0, 1) * np.clip((760 - X) / 60, 0, 1)
    path2 = np.exp(-((Z - 92) / 30.0) ** 2) * np.clip((X - 150) / 60, 0, 1) * np.clip((520 - X) / 60, 0, 1)
    worn = np.clip(path * 0.6 + path2 * 0.5, 0, 1) * (0.5 + 0.5 * fbm(X / 40, Z / 40, 8, 2))
    base = lerp(base, lerp(base, col("#e4dcc4"), 0.5), (worn * 0.6)[..., None])
    seam = np.maximum(lines_aa(X, T, 0.7, gX), lines_aa(Z, T, 0.7, gZ))
    out = base * (1 - (seam * 0.20)[..., None]) + col("#5a5444") * (seam * 0.05)[..., None]
    # a few scuffs from chair legs, black heel marks
    scuff = np.clip((fbm(X / 4, Z / 9, 31, 3) - 0.74) * 6, 0, 1) * (fbm(X / 60, Z / 60, 32, 2) > 0.5)
    out = lay(out, "#4a4238", scuff * 0.35)
    # the rubber mat in front of the sink: dark green-grey, ribbed, its edges bevelled
    mx0, mx1, mz0, mz1 = M.MAT
    inm = band(X, mx0, mx1, gX) * band(Z, mz0, mz1, gZ)
    rib = lines_aa(X, 2.2, 0.8, gX)
    mat = col("#4a5048") * (0.9 + 0.12 * fbm(X / 6, Z / 6, 33, 2))[..., None] * (1 - 0.18 * rib[..., None])
    rim = inm - band(X, mx0 + 2.5, mx1 - 2.5, gX) * band(Z, mz0 + 2.5, mz1 - 2.5, gZ)
    mat = lay(mat, "#6a7068", np.clip(rim, 0, 1) * 0.6)
    return out * (1 - inm[..., None]) + mat * inm[..., None]


def block_wall(c, along, Y, gA, gY, seed=0):
    """Concrete block, painted: courses 20 cm high, blocks 40 long in a running bond, the joints filled with paint
    and still showing; a rubber cove base 10 cm high; scuffed lower down."""
    ch, bl = 20.3, 40.6
    course = np.floor(Y / ch)
    off = (course % 2) * (bl / 2)
    ib = np.floor((along + off) / bl)
    base = lerp(col(WALL), col(WALL_LOW), np.clip((110 - Y) / 110, 0, 1)[..., None] * 0.5)
    base = base * (0.95 + 0.07 * hashf(course * 97 + ib, seed + 4))[..., None]
    base = base * (0.95 + 0.08 * fbm(along / 9, Y / 9, seed + 9, 3)[..., None])
    pits = fbm(along / 0.9, Y / 0.9, seed + 11, 2)
    base = base * (1 - (np.clip((pits - 0.7) * 3, 0, 1) * 0.10)[..., None])
    bed = lines_aa(Y, ch, 1.0, gY)                                       # the joints: a shadow under each course's lip
    lip = lines_aa(Y, ch, 0.8, gY, phase=-0.9)
    head = lines_aa(along + off, bl, 1.0, gA) * (1 - bed)
    out = base * (1 - 0.20 * bed[..., None] - 0.14 * head[..., None]) * (1 + 0.05 * lip[..., None])
    scuff = np.clip((fbm(along / 5, Y / 3, seed + 21, 3) - 0.66) * 4, 0, 1) * np.clip((40 - Y) / 30, 0, 1)
    out = lay(out, "#8a8068", scuff * 0.3)
    sk = band(Y, -1, 10, gY)
    skirt = col(BASE) * (0.85 + 0.25 * fbm(along / 30, Y / 3, seed + 5, 2)[..., None])
    out = lerp(out, skirt, sk[..., None])
    top = band(Y, 9.0, 10.4, gY)
    return lerp(out, col("#7a6a5a"), (top * 0.6)[..., None])


def m_back(c):
    X, Y = c.X, c.Y
    gX, gY = grad_of(X) * c.ss, grad_of(Y) * c.ss
    return block_wall(c, X, Y, gX, gY, 1)


def m_left(c):
    Z, Y = c.Z, c.Y
    gZ, gY = grad_of(Z) * c.ss, grad_of(Y) * c.ss
    return block_wall(c, Z, Y, gZ, gY, 2)


def m_right(c):
    Z, Y = c.Z, c.Y
    gZ, gY = grad_of(Z) * c.ss, grad_of(Y) * c.ss
    return block_wall(c, Z, Y, gZ, gY, 3)


def m_ceiling(c):
    """Acoustic tiles two feet square in a white grid: each tile its own off-white, with the fissures and pinholes
    such tiles have; a water stain or two where the roof has leaked onto them since about 1983."""
    X, Z = c.X, c.Z
    gX, gZ = grad_of(X) * c.ss, grad_of(Z) * c.ss
    T = M.TILE
    ix, iz = np.floor(X / T), np.floor(Z / T)
    base = col(CEIL) * (0.94 + 0.08 * hashf(ix * 17 + iz, 2))[..., None]
    pick = hashf(ix * 29 + iz * 7, 46)                           # a few tiles put in newer, whiter; a few gone yellow
    base = np.where((pick > 0.90)[..., None], col("#ecebe4") * (0.97 + 0.03 * hashf(ix + iz * 3, 47))[..., None], base)
    base = np.where((pick < 0.07)[..., None], base * col("#f0e0b8"), base)
    base = base * (0.95 + 0.07 * fbm(X / 14, Z / 14, 41, 3)[..., None])
    fis = fbm(X / 1.6 + Z / 7, Z / 1.6, 43, 2)
    base = base * (1 - (np.clip((fis - 0.66) * 4, 0, 1) * 0.12)[..., None])
    stain = np.clip((fbm(X / 70, Z / 90, 44, 3) - 0.66) * 4, 0, 1) * ((ix == 9) & (iz == 2) | (ix == 2) & (iz == 5))
    base = lerp(base, base * col("#c8a878"), (stain * 0.55)[..., None])
    grid = np.maximum(lines_aa(X, T, 2.4, gX, fade=False), lines_aa(Z, T, 2.4, gZ, fade=False))
    grid = grid * np.clip((T / np.maximum(gX, gZ) - 2.0) / 3.0, 0.35, 1)
    out = lerp(base, col(GRID), (grid * 0.85)[..., None])
    edge = np.maximum(lines_aa(X, T, 0.7, gX, phase=1.6), lines_aa(Z, T, 0.7, gZ, phase=1.6))
    return out * (1 - 0.10 * edge[..., None])


SHELL = dict(floor=m_floor, back=m_back, left=m_left, right=m_right, ceiling=m_ceiling)


def holes():
    dx0, dx1, dy0, dy1 = M.DOOR
    vx0, vx1, vz0, vz1 = M.VENT
    return {
        "back": lambda X, Y, Z: (X > dx0) & (X < dx1) & (Y > dy0) & (Y < dy1),
        "ceiling": lambda X, Y, Z: (X > vx0) & (X < vx1) & (Z > vz0) & (Z < vz1),
    }


def shell(st):
    st.shell(M.W, M.H, SHELL, holes=holes())


# ---------------------------------------------------------------- the ceiling's fittings
def troffers(st):
    """Two fluorescent fittings in the grid: a white steel pan, and a ribbed plastic lens glowing, the tubes' bars
    brighter behind it. The near one has two of its three tubes out, as such fittings do for months (it is greyer, and
    lights the near floor less). They are lights: their lens is self-lit (the lamps that light the room are in
    office_breakroom: `lamps`)."""
    for i, (x0, x1, z0, z1) in enumerate(M.TROFFERS):
        y = M.H - 0.4
        st.box(x0, x1, y - 2.0, M.H, z0, z1, plain("#e8e8e0", 0.05, 8, 60 + i), "troffer", shadow=False)
        dead = M.TUBES_OUT if i == 1 else ()

        def m_lens(c, i=i, x0=x0, x1=x1, z0=z0, z1=z1, dead=dead):
            u, v = c.X - x0, c.Z - z0
            rib = 0.5 + 0.5 * np.cos(u * 2.6)
            tubes = sum(np.exp(-((v - (z1 - z0) * f) / 5.0) ** 2) * (0.0 if k in dead else 1.0) for k, f in enumerate((0.25, 0.5, 0.75)))
            lit = 1.0 - 0.6 * len(dead) / 3.0
            edge = np.clip(np.minimum(np.minimum(u, (x1 - x0) - u), np.minimum(v, (z1 - z0) - v)) / 6.0, 0, 1)
            k = col("#eef4e4") * ((0.82 + 0.10 * rib) * lit + 0.22 * tubes)[..., None] * (0.70 + 0.30 * edge)[..., None]
            return k * 0.25, k * 0.95
        st.poly([(x0 + 3, y - 2.2, z0 + 3), (x1 - 3, y - 2.2, z0 + 3), (x1 - 3, y - 2.2, z1 - 3), (x0 + 3, y - 2.2, z1 - 3)], m_lens, "troffer", bias=0.3)


def speaker(st):
    """The building's speaker, high in the far right corner over the door: an old steel box across the corner, painted
    the walls' beige, its face tipped down at the room, a round grille in it (Houston's voice comes out of it)."""
    X1 = M.W
    sx, sy0, sy1, sd = M.SPEAKER_BOX
    top_in, bot_out = sd * 0.62, sd
    A = (X1 - top_in, sy1, 0.0)
    B = (X1, sy1, top_in)
    C = (X1, sy0, bot_out)
    D = (X1 - bot_out, sy0, 0.0)

    def m_face(c):
        U, V = c.U, c.V
        Wd = np.hypot(top_in, top_in)
        cu, cv = Wd / 2, (sy1 - sy0) * 0.5
        r = np.hypot(U - cu, (V - cv) * 1.0)
        k = col("#d6ceb0") * (0.94 + 0.06 * fbm(U / 3, V / 3, 70, 2))[..., None]
        grille = r < 10.5
        holes_ = grille & (np.abs((U % 1.8) - 0.9) < 0.42) & (np.abs((V % 1.8) - 0.9) < 0.42)
        k = np.where(grille[..., None], col("#8a8676"), k)
        k = np.where(holes_[..., None], col("#2a2a28"), k)
        ring = np.abs(r - 11.2) < 0.9
        return np.where(ring[..., None], col("#b8b29a"), k)
    st.poly([A, B, C, D], m_face, "speaker")
    st.poly([D, C, (X1, sy0, 0.0)], plain("#beb698", 0.05, 4, 69), "speaker")              # its underside
    st.stick(((A[0] + B[0]) / 2, sy1, (A[2] + B[2]) / 2), ((A[0] + B[0]) / 2 + 2, M.H, (A[2] + B[2]) / 2 - 2), 0.6, col("#4a4844"), "speakerwire")


def vent(st, G="vent", eyes=False):
    """The return grille over the fridge, a two-by-four in the grid: a white steel frame, and slats across it with the
    duct's dark between them. From below and this far off it is seen nearly edge-on, so it is painted as a painter
    would show it: a bright frame and five bold slats, the dark of the duct between them (a louvred grille of fine
    blades would read as nothing). Behind it, the duct's dark mouth (the backdrop: what is seen if the grille is not
    there). With `eyes`, Ranger is lying over it in the duct: his masked face down at a gap, and two eyes shining."""
    x0, x1, z0, z1 = M.VENT
    y = M.H
    st.box(x0 + 1, x1 - 1, y, y + 40, z0 + 1, z1 - 1, metal("#5a5c5a", 71, 0.15), "duct", inside=True, shadow=False)
    n = M.VENT_SLATS
    fw = 7.0                                                     # the frame's width

    def m_grille(c):
        u, v = c.X - x0, c.Z - z0
        L, Wd = z1 - z0, x1 - x0
        frame = (u < fw) | (u > Wd - fw) | (v < fw) | (v > L - fw)
        period = (L - 2 * fw) / n
        f = ((v - fw) % period) / period
        slat = (f > 0.06) & (f < 0.56)
        light = col("#f6f6f0") * (0.95 + 0.05 * fbm(c.X / 4, c.Z / 4, 72, 2))[..., None]
        dark = col("#1e2026") * (0.9 + 0.2 * fbm(c.X / 3, c.Z / 3, 73, 2))[..., None]
        k = np.where((frame | slat)[..., None], light, dark)
        lip = (~frame) & (f > 0.56) & (f < 0.64)                                 # each slat's edge, catching the light
        k = np.where(lip[..., None], col("#ffffff"), k)
        lit = (frame | slat | lip)[..., None]
        return k, np.where(lit, col("#eef2e4") * 0.22, 0.0)                     # (white enamel: it holds the light)
    st.poly([(x0, y - 0.6, z0), (x1, y - 0.6, z0), (x1, y - 0.6, z1), (x0, y - 0.6, z1)], m_grille, "vent", grp=G, bias=0.2)
    def m_gap(c):                                                                # the shadow line between the grille and the tiles
        return col("#5a5a58")
    for (a0, a1, b0, b1) in ((x0 - 1.4, x1 + 1.4, z0, z0 + 0.1), (x0 - 1.4, x1 + 1.4, z1, z1 + 1.4), (x0 - 1.4, x0, z0, z1), (x1, x1 + 1.4, z0, z1)):
        st.poly([(a0, y - 0.3, b0), (a1, y - 0.3, b0), (a1, y - 0.3, b1), (a0, y - 0.3, b1)], m_gap, "ventgap", bias=0.1)
    if eyes:
        # Ranger, lying over the grille in the duct, his masked face down at the gap nearest us: the mask a dark band
        # across the gap, the grey of his face round it, two eyes shining (they catch the room's light)
        period = (z1 - z0 - 2 * fw) / n
        gz = z0 + fw + period * (n - 1) + period * 0.83                         # the middle of the last gap, nearest us
        fx = (x0 + x1) / 2 + 1.5
        def m_fur(c):
            return col("#8a8494") * (0.85 + 0.2 * fbm(c.X / 1.5, c.Z / 1.5, 74, 2))[..., None]
        st.ball((fx, y - 1.4, gz - 1.0), 1.0, m_fur, "vent", grp=G, shadow=False, squash=(11.0, 3.4, 6.0))
        def m_mask(c):
            return col("#141218")
        st.ball((fx, y - 2.4, gz), 1.0, m_mask, "vent", grp=G, shadow=False, squash=(9.0, 2.6, 4.0))
        for dx in (-3.9, 3.9):
            st.ball((fx + dx, y - 3.6, gz + 1.0), 2.3, col("#f2ecc0"), "vent", grp=G, shadow=False, emi=col("#fff4c8") * 1.1)
            st.ball((fx + dx + 0.5, y - 4.3, gz + 2.2), 0.9, col("#141218"), "vent", grp=G, shadow=False)
        st.ball((fx, y - 3.2, gz + 3.4), 1.3, col("#1a1416"), "vent", grp=G, shadow=False)                  # the tip of his nose


# ---------------------------------------------------------------- the door, and the hall beyond it
def door(st, open_=False, G="door"):
    """A painted steel door in a steel frame: a lever handle each side, a kick plate, a narrow window of wired glass at
    eye height; on its room side a gray jacket on a hook (somebody's: they all have one), on its hall side a small plate,
    BREAK ROOM. Shut, it fills the doorway; open, it stands into the room on its hinges at the right jamb, and what we
    see of it is its hall side. The frame belongs to the wall (the backdrop)."""
    dx0, dx1, dy0, dy1 = M.DOOR
    t = 4.5                                                      # the leaf's thickness
    fr = 5.0                                                     # the frame's width round the opening
    frame = metal("#9a9a84", 75, 0.08)
    st.box(dx0 - fr, dx0, 0, dy1 + fr, 0, 1.6, frame, "doorframe", shadow=False)
    st.box(dx1, dx1 + fr, 0, dy1 + fr, 0, 1.6, frame, "doorframe", shadow=False)
    st.box(dx0 - fr, dx1 + fr, dy1, dy1 + fr, 0, 1.6, frame, "doorframe", shadow=False)
    st.box(dx0 - 0.6, dx0 + 0.2, 0, dy1, -12, 0, frame, "doorframe", shadow=False)          # the reveals, in the wall's thickness
    st.box(dx1 - 0.2, dx1 + 0.6, 0, dy1, -12, 0, frame, "doorframe", shadow=False)
    st.box(dx0, dx1, dy1 - 0.2, dy1 + 0.6, -12, 0, frame, "doorframe", shadow=False)
    w = dx1 - dx0 - 1.0
    hx, hz = dx1 - 0.5, -1.0                                    # the hinges' line (the leaf's room face, at the right jamb)
    ang = M.DOOR_OPEN if open_ else 0.0
    a = math.radians(ang)
    ux, uz = -math.cos(a), math.sin(a)                           # along the leaf, from the hinges toward the latch
    nx, nz = math.sin(a), math.cos(a)                            # the way its room face looks
    grp = "door-open" if open_ else G

    def P(s_, y, d):
        """A place on the leaf: s_ along it from the hinges, y up, d out from its room face (the hall face is d = -t)."""
        return (hx + ux * s_ + nx * d, y, hz + uz * s_ + nz * d)

    top = dy1 - 0.6
    corners = [P(s_, y, d) for s_ in (0, w) for y in (0, top) for d in (0, -t)]
    xs, ys, zs = zip(*corners)
    st.occ.append((min(xs), max(xs), 0, top, min(zs), max(zs)))
    st.feet["doorleaf"] = (min(xs), max(xs), min(zs), max(zs))

    def m_leaf(c):
        return col("#b6b89c") * (0.93 + 0.08 * fbm(c.X / 18, c.Y / 18 + c.Z / 18, 76, 3))[..., None]
    edge = plain("#9c9e84", 0.06, 6, 77)
    st.poly([P(0, 0, 0), P(w, 0, 0), P(w, top, 0), P(0, top, 0)], m_leaf, "doorleaf", grp=grp)              # room face
    st.poly([P(w, 0, -t), P(0, 0, -t), P(0, top, -t), P(w, top, -t)], m_leaf, "doorleaf", grp=grp)          # hall face
    st.poly([P(w, 0, 0), P(w, 0, -t), P(w, top, -t), P(w, top, 0)], edge, "doorleaf", grp=grp)              # the latch edge
    st.poly([P(0, top, 0), P(w, top, 0), P(w, top, -t), P(0, top, -t)], edge, "doorleaf", grp=grp)          # its top

    def on(s0, s1, y0, y1, d, mat, name="doorleaf", bias=0.25):
        st.poly([P(s0, y0, d), P(s1, y0, d), P(s1, y1, d), P(s0, y1, d)], mat, name, grp=grp, bias=bias)
    kick = metal("#a8a890", 78, 0.12)
    for d in (0.15, -t - 0.15):
        on(4, w - 4, 1, 26, d, kick)                                                          # the kick plates
    # the window: wired glass with the light of the far side in it, and its little steel frame
    def m_wire(c):
        u, v = c.U, c.V
        wire = (np.abs(((u + v) % 2.6) - 1.3) < 0.18) | (np.abs(((u - v) % 2.6) - 1.3) < 0.18)
        k = np.where(wire[..., None], col("#6a6a60"), col("#d8e0d0"))
        return k * 0.3, np.where(wire[..., None], col("#2a2a28"), col("#e2ead8") * 0.85)
    wf = metal("#8a8c78", 79, 0.1)
    for d, sgn in ((0.0, 1), (-t, -1)):
        on(w - 31.5, w - 12.5, 116.5, 187.5, d + sgn * 0.12, wf, bias=0.2)
        on(w - 30, w - 14, 118, 186, d + sgn * 0.3, m_wire, "doorglass", bias=0.35)
    # a lever handle each side, at 100 cm, near the latch
    hs = w - 9.0
    for d, sgn in ((0.0, 1), (-t, -1)):
        rose = P(hs, 100, d + sgn * 0.4)
        st.ball(rose, 2.6, chrome("#c8ccce", 0.6, 80), "doorhandle", grp=grp, shadow=False, squash=(1.0, 1.0, 1.0))
        st.stick(P(hs, 100, d + sgn * 2.6), P(hs - 12, 99, d + sgn * 3.0), 1.1, chrome("#c8ccce", 0.6, 81), "doorhandle", grp=grp)
    if not open_:
        # the gray jacket on its hook, high on the room side
        jx, jy = M.JACKET_HOOK
        js = (dx1 - 0.5) - jx
        st.stick(P(js, jy - 2, 0), P(js, jy, 2.2), 0.5, chrome("#b8bcbe", 0.5, 82), "jacket", grp=grp)

        def m_jacket(c):
            return col("#7d8088") * (0.86 + 0.2 * fbm(c.X / 3, c.Y / 5 + c.Z / 3, 83, 3))[..., None]
        st.poly([P(js + 22, jy - 10, 4.0), P(js - 22, jy - 10, 4.0), P(js - 20, jy - 66, 3.0), P(js + 20, jy - 66, 3.0)], m_jacket, "jacket", grp=grp, bias=0.2)
        st.poly([P(js + 6, jy - 2, 4.4), P(js - 6, jy - 2, 4.4), P(js - 22, jy - 10, 4.4), P(js + 22, jy - 10, 4.4)], m_jacket, "jacket", grp=grp, bias=0.3)
        st.poly([P(js + 1.5, jy - 10, 4.6), P(js - 1.5, jy - 10, 4.6), P(js - 1.0, jy - 60, 4.6), P(js + 1.0, jy - 60, 4.6)],
                col("#4a4c54"), "jacket", grp=grp, bias=0.35)                                 # where it closes
        for sx in (-1, 1):                                                                     # its sleeves hang down its sides
            st.poly([P(js + sx * 23, jy - 12, 4.8), P(js + sx * 20, jy - 12, 4.8), P(js + sx * 17, jy - 62, 4.8), P(js + sx * 22, jy - 62, 4.8)],
                    col("#6a6c74"), "jacket", grp=grp, bias=0.4)
    else:
        # the hall side's plate: BREAK ROOM (its letters are laid afterwards, crisp: see office_breakroom.words)
        on(12, 38, 148, 158, -t - 0.25, plain("#e8e2c8", 0.04, 4, 84), "doorplate", bias=0.3)


def door_plate_quad():
    """The corners (top left, top right, bottom right, bottom left) of the plate on the open door's hall side."""
    dx0, dx1, dy0, dy1 = M.DOOR
    t, w = 4.5, dx1 - dx0 - 1.0
    hx, hz = dx1 - 0.5, -1.0
    a = math.radians(M.DOOR_OPEN)
    ux, uz, nx, nz = -math.cos(a), math.sin(a), math.sin(a), math.cos(a)

    def P(s_, y, d):
        return (hx + ux * s_ + nx * d, y, hz + uz * s_ + nz * d)
    d = -t - 0.6
    return [P(38, 158, d), P(12, 158, d), P(12, 148, d), P(38, 148, d)]


def hall(st):
    """What is seen through the doorway: the hall, lit by its own tubes, cool and even: the same tiles, its far wall the
    same painted block, a rubber base, a light switch, and the edge of a notice on the wall."""
    dx0, dx1, dy0, dy1 = M.DOOR
    far = -230.0

    def m_hfloor(c):
        X, Z = c.X, c.Z
        T = 30.5
        chk = ((np.floor(X / T) + np.floor(Z / T)) % 2) == 0
        k = np.where(chk[..., None], col(TILE_A), col(TILE_B)) * (0.95 + 0.08 * fbm(X / 8, Z / 8, 90, 2))[..., None]
        k = k * (0.86 + 0.14 * np.clip(-Z / 200, 0, 1))[..., None]
        return k * 0.2, k * 0.66
    st.box(dx0 - 160, dx1 + 160, -2, 0, far, -12, m_hfloor, "hall", flag=OUTSIDE, shadow=False)

    def m_hwall(c):
        X, Y = c.X, c.Y
        k = col(WALL) * (0.94 + 0.07 * fbm(X / 9, Y / 9, 91, 3))[..., None]
        ch = 20.3
        bed = (np.abs(((Y) % ch) - ch / 2) > ch / 2 - 0.6)
        k = k * np.where(bed[..., None], 0.86, 1.0)
        k = np.where((Y < 10)[..., None], col(BASE), k)
        sw = (np.abs(X - (dx0 + 14)) < 4.5) & (np.abs(Y - 118) < 6.5)                       # a light switch
        k = np.where(sw[..., None], col("#ece8da"), k)
        notice = (X > dx1 - 10) & (X < dx1 + 40) & (Y > 120) & (Y < 168)                     # the edge of a notice
        k = np.where(notice[..., None], col(PAPER), k)
        line = notice & (np.abs(((Y - 124) % 6) - 3) < 0.9) & (X > dx1 - 6) & (X < dx1 + 36)
        k = np.where(line[..., None], col("#5a5a64"), k)
        glow = 0.82 + 0.18 * np.exp(-((X - (dx0 + dx1) / 2) / 140) ** 2)
        k = k * (0.86 + 0.14 * np.clip((180 - Y) / 180, 0, 1))[..., None]             # the hall's wall falls off upward too
        return k * 0.2, k * (0.62 * glow)[..., None]
    st.box(dx0 - 160, dx1 + 160, 0, dy1 + 60, far - 2, far, m_hwall, "hall", flag=OUTSIDE, shadow=False)
    # a red fire extinguisher on its hook on the far wall, and its little sign over it: where the doorway shows the far
    # wall from here (x about 770 to 874: the eye is well to the left of the door, so it sees the hall's right-hand part)
    ex, ez = dx1 + 80, far + 10
    def m_ext(c):
        k = col("#c8302a") * (0.85 + 0.2 * fbm(c.X / 2, c.Y / 2, 93, 2))[..., None]
        return k * 0.2, k * 0.75
    st.cyl((ex, ez), 7.0, 52, 102, m_ext, name="hall", flag=OUTSIDE, shadow=False, cap=col("#9a2420"))
    st.cyl((ex, ez), 2.2, 102, 110, lambda c: (col("#3a3a3a") * 0.2, col("#3a3a3a") * 0.7), name="hall", flag=OUTSIDE, shadow=False)
    st.box(ex - 6, ex + 6, 118, 132, far, far + 0.4, lambda c: (col("#c8302a") * 0.2, col("#d84038") * 0.75), "hall", flag=OUTSIDE, shadow=False)

    def m_hceil(c):
        k = col(CEIL) * 0.75
        return k * 0.2, k * 0.8
    st.box(dx0 - 160, dx1 + 160, dy1 + 52, dy1 + 56, far, -12, m_hceil, "hall", flag=OUTSIDE, shadow=False)


# ---------------------------------------------------------------- on the left wall
def calendar(st):
    """A wall calendar over the couch: a picture of the desert at the top (a mesa, a sky; nobody's photograph), the month
    under it, OCTOBER, every day crossed off in red but the last."""
    z0, z1, y0, y1 = M.CALENDAR
    x = 0.4
    split = y0 + (y1 - y0) * 0.5

    def m_cal(c):
        u, v = c.Z - z0, c.Y - y0
        W_, H_ = z1 - z0, y1 - y0
        top = v > H_ * 0.5
        sky = lerp(col("#d8b48a"), col("#7aa8d0"), np.clip((v - H_ * 0.5) / (H_ * 0.5), 0, 1)[..., None])
        mesa = (v < H_ * 0.5 + 9 + 4 * np.sin(u / 7)) & (u > W_ * 0.25) & (u < W_ * 0.8)
        pic = np.where(mesa[..., None], col("#b8704c"), sky)
        pic = np.where(((v < H_ * 0.5 + 4))[..., None], col("#d8a874"), pic)
        page = col(PAPER) * (0.95 + 0.05 * fbm(u / 4, v / 4, 92, 2))[..., None]
        # the month: a band with the name (marks), and a grid of days
        name = (v > H_ * 0.40) & (v < H_ * 0.47) & (np.abs(u - W_ / 2) < W_ * 0.22)
        page = np.where(name[..., None], col("#3a3a48"), page)
        cu, cv = (u - 3) / ((W_ - 6) / 7), (H_ * 0.37 - v) / (H_ * 0.33 / 5)
        cell = (cu > 0) & (cu < 7) & (cv > 0) & (cv < 5)
        day = np.floor(cu) + 7 * np.floor(cv)
        gridl = cell & ((np.abs(cu - np.round(cu)) < 0.05) | (np.abs(cv - np.round(cv)) < 0.07))
        page = np.where(gridl[..., None], col("#9a9aa4"), page)
        xed = cell & (day >= 2) & (day <= 31) & ((np.abs((cu % 1) - (cv % 1)) < 0.09) | (np.abs((cu % 1) + (cv % 1) - 1) < 0.09))
        page = np.where(xed[..., None], col("#c8302a"), page)
        return np.where(top[..., None], pic, page)
    st.poly([(x, y0, z0), (x, y0, z1), (x, y1, z1), (x, y1, z0)], m_cal, "calendar", bias=0.2)
    st.stick((0.6, y1 + 3, (z0 + z1) / 2), (1.6, y1 + 3, (z0 + z1) / 2), 0.4, col("#8a8a8a"), "calendar")

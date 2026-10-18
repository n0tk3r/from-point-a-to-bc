"""The Office's own painting kit (OFFICE-17C): what the Comfortable Room (office_room.py) and Property & Effects
(office_property.py) are both made with. The ray-caster itself is the store's (nevada_store_kit.Stage, Lamp, shade:
every pixel a ray from the scene's camera, met by what it meets in the room's own centimetres); this file adds what
the Office has and the store has not:

  - FLUORESCENT LIGHT. Recessed light panels (troffers) in a suspended ceiling, each two tubes behind a prismatic lens:
    each tube a long soft lamp aimed down (several small lamps along it, so its shadows are soft along its length), a
    little light leaking sideways onto the walls, and the bounce of a pale room. Pale, a little green; what no tube
    reaches goes lilac and violet when the paints are put on, never grey.
  - THE OFFICE'S SURFACES. Gray carpet tiles, painted concrete block with a vinyl cove base, an acoustic tile ceiling on
    its T-bar grid, regulation gray steel, molded plastic, wood-grain laminate.
  - THE OFFICE'S FITTINGS. The return-air grille (and the same grille with two eyes in a black mask shining between its
    slats), light panels, the stacking chair, sprinkler heads, a smoke detector, the building's ceiling speaker.
  - THE PASSES. under (render), strokes (paint), details, finish: the store's own, here with the Office's grading.

Measurements as in room.py: X across, Y up, Z out from the back wall toward us, in centimetres. Nothing here is
anybody's: every word is the Office's, every shape drawn for this picture."""

import math
import os

import numpy as np
from PIL import Image

from brush import F32, blur, lerp, noise, sample, strokes, grain, to_palette, save
from nevada_store_kit import (Stage, Lamp, shade, col, mixc, vnoise, fbm, hashf, grad_of, lines_aa, band, rect, disc, lay, sstep,
                              curve3, Ctx, pen_mask, pen_width, lay_on, floor_contact, LUM, normals, text_card, card_paint)

W_PIC, H_PIC = 800, 600

# ---------------------------------------------------------------- the Office's colours (before any light falls on them)
BLOCK = "#cdc3a8"               # painted concrete block: a beige the regulations call "Desert Tan No. 2"
BLOCK_D = "#bfb59a"
COVE = "#5e5650"                # the vinyl cove base along every wall: a brown-gray
CEIL_TILE = "#d0d6ca"           # acoustic tile, fissured, gone a little yellow
TBAR = "#eeece4"                # the grid's white enamel
CARPET_A, CARPET_B = "#585c6c", "#5f6170"     # gray carpet tiles, laid quarter-turned, so they read as a faint checker
STEEL = "#8e959c"               # regulation gray steel
STEEL_D = "#737a82"
PLASTIC = "#7a8a9c"             # the stacking chairs' molded seats: a gray-blue
LAMINATE = "#c9b28a"            # wood-grain laminate (no wood was harmed)
PAPER = "#f2eee2"
TUBE = "#eaf8e0"                # a lit tube, through its lens
LIGHT = "#e2efd4"               # the tubes' light: pale, a little green

OUTSIDE = 4                     # the flag: beyond the room (lit by its own light; this room's lamps leave it alone)


# ---------------------------------------------------------------- small helpers
def px_of(c, k=1.0):
    """Centimetres per pixel at each place a paint colours (on a flat piece, a box or a round thing, whose places come
    as a list: `grad_of` is for the shell's whole-picture fields). `k` > 1 for a surface seen at a slant."""
    return np.asarray(c.fp, dtype=F32) * k


def rm(u, lo, hi, fp):
    """A soft-edged band lo..hi along u (fp: cm per ray)."""
    return np.clip((u - lo) / fp + 0.5, 0, 1) * np.clip((hi - u) / fp + 0.5, 0, 1)


def rect_uv(u, v, u0, u1, v0, v1, fp):
    return rm(u, u0, u1, fp) * rm(v, v0, v1, fp)


def disc_uv(u, v, cu, cv, r, fp):
    return np.clip((r - np.hypot(u - cu, v - cv)) / fp + 0.5, 0, 1)


def patch(c, s=22.0, seed=0):
    return fbm((c.X + 0.37 * c.Y) / s, (c.Z + 0.61 * c.Y) / s, seed, 3)


def plain(color, amt=0.10, s=22.0, seed=0):
    """One paint, a little patchy as a brush leaves it."""
    k = col(color)

    def f(c):
        return k * (1 + amt * 2 * (patch(c, s, seed)[..., None] - 0.5))
    return f


def painted_steel(color=STEEL, seed=0, amt=0.08, chips=0.0):
    """Painted steel: smooth, a little mottled; scuffed where hands and feet have been."""
    k = col(color)

    def f(c):
        n = fbm(c.X / 9, (c.Y + c.Z) / 9, seed, 2)
        out = k * (1 + amt * 2 * (n[..., None] - 0.5))
        if chips:
            chip = np.clip((fbm(c.X / 2.2, (c.Y + c.Z * 0.5) / 2.2, seed + 7, 2) - 0.80) * 9, 0, 1)
            out = lay(out, "#5a5c62", chip * chips)
        return out
    return f


def chrome(tint="#c4c8ce", seed=0):
    """Chrome: it shows the room, so it is a mid gray that takes the light: bright where it faces up toward the tubes,
    dark where it faces the carpet."""
    k = col(tint)

    def f(c):
        n = normals(c)
        up = np.clip(n[..., 1], -1, 1)
        out = k * (0.62 + 0.42 * up + 0.12 * n[..., 2])[..., None]
        out = out * (0.94 + 0.12 * fbm(c.X / 3 + seed, (c.Y + c.Z) / 3, 7 + seed, 2))[..., None]
        return np.clip(out, 0, 1.4)
    return f


def molded(color=PLASTIC, seed=0):
    """Molded plastic: an even colour with a faint satin sheen where it faces the tubes."""
    k = col(color)

    def f(c):
        n = normals(c)
        sheen = np.clip(n[..., 1], 0, 1) ** 4 * 0.10
        return k * (0.97 + 0.06 * fbm(c.X / 6, (c.Y + c.Z) / 6, seed, 2))[..., None] + sheen[..., None]
    return f


def laminate(color=LAMINATE, seed=0, grain_dir="z"):
    """Wood-grain laminate: a printed grain, very regular, a little glossy."""
    k = col(color)

    def f(c):
        g = c.Z if grain_dir == "z" else c.X
        o = c.X if grain_dir == "z" else c.Z
        n = fbm(o / 1.6, g / 40.0, seed, 3)
        stripe = 0.5 + 0.5 * np.sin(o * 1.9 + 4.0 * fbm(o / 9, g / 60, seed + 3, 2))
        out = k * (0.90 + 0.12 * n[..., None] + 0.05 * stripe[..., None])
        return out
    return f


def obox(st, c, size, ang, mat, name=None, grp="back", flag=0, shadow=True, faces=("left", "right", "top", "front", "back", "bottom")):
    """A box turned about the upright through its middle by `ang` degrees (positive turns its front toward +X).
    c: the middle of its foot (X, Y0, Z). size: (width along its own x, height, depth along its own z)."""
    w, h, dpt = size
    a = math.radians(ang)
    ux, uz = math.cos(a), -math.sin(a)
    vx, vz = math.sin(a), math.cos(a)
    X0, Y0, Z0 = c

    def P(sx, sy, sz):
        return (X0 + ux * sx + vx * sz, Y0 + sy, Z0 + uz * sx + vz * sz)
    hw, hd = w / 2, dpt / 2
    F = {
        "front": [P(-hw, 0, hd), P(hw, 0, hd), P(hw, h, hd), P(-hw, h, hd)],
        "back": [P(hw, 0, -hd), P(-hw, 0, -hd), P(-hw, h, -hd), P(hw, h, -hd)],
        "left": [P(-hw, 0, -hd), P(-hw, 0, hd), P(-hw, h, hd), P(-hw, h, -hd)],
        "right": [P(hw, 0, hd), P(hw, 0, -hd), P(hw, h, -hd), P(hw, h, hd)],
        "top": [P(-hw, h, hd), P(hw, h, hd), P(hw, h, -hd), P(-hw, h, -hd)],
        "bottom": [P(-hw, 0, -hd), P(hw, 0, -hd), P(hw, 0, hd), P(-hw, 0, hd)],
    }
    if shadow:
        pts = [p for f in F.values() for p in f]
        xs, ys, zs = zip(*pts)
        st.occ.append((min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))
    for k in faces:
        m = mat[k] if isinstance(mat, dict) else mat
        if m is None:
            continue
        st.poly(F[k], m, name, grp=grp, flag=flag)
    return P


# ---------------------------------------------------------------- the shell's surfaces
def m_carpet(seed=0, stains=(), paths=()):
    """Carpet tiles 50 cm square, two grays, laid quarter-turned (a faint checker of pile direction); a fine fleck; the
    seams just showing; stains (X, Z, r) and worn paths [((X0, Z0), (X1, Z1), width)]."""
    def f(c):
        X, Z = c.X, c.Z
        gX, gZ = grad_of(X) * c.ss, grad_of(Z) * c.ss
        T = 50.0
        ix, iz = np.floor(X / T), np.floor(Z / T)
        chk = ((ix + iz) % 2) == 0
        base = np.where(chk[..., None], col(CARPET_A), col(CARPET_B))
        base = base * (0.95 + 0.10 * hashf(ix * 131 + iz * 7, seed + 3))[..., None]
        # the pile: a fine fleck, and its direction (stripes along X on one tile, along Z on the next)
        u = np.where(chk, X, Z)
        fleck = fbm(X / 0.9, Z / 0.9, seed + 11, 2)
        rib = 0.5 + 0.5 * np.sin(u * 2.6)
        rib_k = np.clip(2.6 / np.maximum(np.where(chk, gX, gZ), 1e-3) / 8.0, 0, 1)      # only where the ribs can be seen
        base = base * (0.82 + 0.32 * fleck[..., None] + 0.05 * (rib * rib_k)[..., None])
        base = base * (0.94 + 0.12 * fbm(X / 60, Z / 60, seed + 21, 3)[..., None])
        out = base
        for (sx, sz, r) in stains:
            d = np.hypot(X - sx, (Z - sz) * 1.2) / r
            ring = np.clip(1 - np.abs(d - 0.9) * 5, 0, 1) * 0.25 + np.clip(1 - d, 0, 1) * 0.18
            ring = ring * (0.6 + 0.8 * fbm(X / 4, Z / 4, seed + 31, 2))
            out = lerp(out, out * col("#8a6a48"), np.clip(ring, 0, 1)[..., None])
        for (p0, p1, w) in paths:
            ax, az = p1[0] - p0[0], p1[1] - p0[1]
            L2 = ax * ax + az * az
            t = np.clip(((X - p0[0]) * ax + (Z - p0[1]) * az) / L2, 0, 1)
            dd = np.hypot(X - (p0[0] + t * ax), Z - (p0[1] + t * az))
            worn = np.exp(-(dd / w) ** 2) * (0.5 + 0.5 * fbm(X / 30, Z / 30, seed + 41, 2))
            out = lerp(out, out * 1.10 + 0.015, (worn * 0.6)[..., None])
        seam = np.maximum(lines_aa(X, T, 0.5, gX), lines_aa(Z, T, 0.5, gZ))
        return out * (1 - 0.20 * seam[..., None])
    return f


def block_wall(c, along, Y, gA, gY, seed=0, base_h=10.0):
    """Painted concrete block, 40 x 20 in running bond: the paint fills the joints but not quite, so each joint is a
    soft line a little darker under a little lighter; the paint is patchy, scuffed low down; a vinyl cove base."""
    BW, BH = 40.0, 20.0
    row = np.floor(Y / BH)
    off = (row % 2) * (BW / 2)
    base = lerp(col(BLOCK), col(BLOCK_D), (0.35 + 0.65 * fbm(along / 80, Y / 60, seed + 3, 3))[..., None])
    # each block its own tone, and the block's own pits under the paint
    ib = np.floor((along + off) / BW)
    base = base * (0.965 + 0.06 * hashf(ib * 37 + row * 11, seed + 5))[..., None]
    pits = np.clip((fbm(along / 0.8, Y / 0.8, seed + 9, 2) - 0.70) * 5, 0, 1)
    base = base * (1 - 0.06 * pits[..., None])
    jy = lines_aa(Y, BH, 1.0, gY)
    jx = lines_aa(along + off, BW, 1.0, gA) * (1 - jy)
    joint = np.maximum(jy, jx)
    lit = lines_aa(Y, BH, 0.8, gY, phase=1.1)
    out = base * (1 - 0.13 * joint[..., None]) * (1 + 0.04 * lit[..., None])
    # scuffs low down, where chairs and feet have been
    scuff = np.clip((fbm(along / 7, Y / 3, seed + 15, 3) - 0.66) * 4, 0, 1) * np.clip((60 - Y) / 40, 0, 1)
    out = lerp(out, out * col("#b0a080"), (scuff * 0.5)[..., None])
    # the cove base: dark vinyl, a lighter top lip
    cb = band(Y, -1, base_h, gY)
    cove = col(COVE) * (0.92 + 0.12 * fbm(along / 20, Y / 2, seed + 17, 2)[..., None])
    out = lerp(out, cove, cb[..., None])
    lip = band(Y, base_h - 1.2, base_h, gY)
    return lerp(out, cove * 1.45, (lip * 0.6)[..., None])


def ceiling_paint(grid=(60.0, 120.0), origin=(0.0, 0.0), seed=0, holes=(), stains=()):
    """The suspended ceiling seen from below: acoustic tiles (fissured: little dark worm-marks), a little uneven in tone,
    on a white T-bar grid 2.4 cm wide. `holes`: [(X0, X1, Z0, Z1)] where something else is set in the grid (light panels,
    the grille): the grid's runners still frame them. `stains`: [(X, Z, r)] where the roof once leaked."""
    gx, gz = grid
    ox, oz = origin

    def f(c):
        X, Z = c.X, c.Z
        gX, gZ = grad_of(X) * c.ss, grad_of(Z) * c.ss
        ix, iz = np.floor((X - ox) / gx), np.floor((Z - oz) / gz)
        base = col(CEIL_TILE) * (0.95 + 0.08 * hashf(ix * 53 + iz * 19, seed + 2))[..., None]
        base = base * (0.96 + 0.08 * fbm(X / 40, Z / 40, seed + 4, 3)[..., None])
        worm = np.clip((fbm(X / 1.1, Z / 1.6, seed + 6, 3) - 0.64) * 6, 0, 1)
        fine = np.clip(1.4 / np.maximum(np.maximum(gX, gZ), 1e-3), 0, 1)           # the worm-marks fade where they are too small to see
        base = base * (1 - (0.22 * worm * fine)[..., None])
        out = base
        for (sx, sz, r) in stains:
            d = np.hypot(X - sx, Z - sz) / r * (0.8 + 0.4 * fbm(X / 14, Z / 14, seed + 8, 2))
            st_ = np.clip(1 - d, 0, 1)
            edge = np.clip(1 - np.abs(d - 0.95) * 9, 0, 1)
            out = lerp(out, out * col("#c8b48a"), (st_ * 0.35 + edge * 0.35)[..., None])
        # the grid: 2.4 cm white runners, a hair of shadow on the tile beside each
        tb = np.maximum(lines_aa(X - ox, gx, 2.4 / 1.0, gX, fade=False), lines_aa(Z - oz, gz, 2.4 / 1.0, gZ, fade=False))
        tbs = np.maximum(lines_aa(X - ox - 1.9, gx, 1.2, gX, fade=False), lines_aa(Z - oz - 1.9, gz, 1.2, gZ, fade=False))
        out = out * (1 - 0.10 * tbs[..., None])
        out = lerp(out, col(TBAR), np.clip(tb * 1.4, 0, 1)[..., None])
        return out
    return f


# ---------------------------------------------------------------- fluorescent light
def troffer_lamps(t, H, power=1.0, color=LIGHT, n=3, name="tube", samples=6, reach=170.0):
    """The lamps of one light panel (X0, X1, Z0, Z1) in a ceiling H high: its two tubes run along its long side, each
    a row of `n` small lamps aimed down, so that a tube's shadow is soft along its length and sharp across it."""
    X0, X1, Z0, Z1 = t
    out = []
    long_z = (Z1 - Z0) >= (X1 - X0)
    for k, frac in enumerate((0.3, 0.7)):
        for i in range(n):
            s = (i + 0.5) / n
            if long_z:
                p = (X0 + (X1 - X0) * frac, H - 3, Z0 + (Z1 - Z0) * s)
            else:
                p = (X0 + (X1 - X0) * s, H - 3, Z0 + (Z1 - Z0) * frac)
            out.append(Lamp(p, color, power / (2 * n), reach=reach, aim=(0, -1, 0), spread=0.18, soft=1.4, back=0.05,
                            size=18.0, wrap=0.45, samples=samples, name=f"{name}{k}{i}", core=0.9, fill=0.0))
    return out


def m_troffer(t, H, lit=1.0, seed=0, flicker_tube=None):
    """A light panel seen from below: a white steel frame, and the prismatic lens with the two tubes glowing behind it
    (brightest along each tube, the lens's little pyramids making a fine grain). Self-lit."""
    X0, X1, Z0, Z1 = t
    long_z = (Z1 - Z0) >= (X1 - X0)

    def f(c):
        X, Z = c.X, c.Z
        g = px_of(c, 2.5)
        u = (X - X0) / (X1 - X0) if long_z else (Z - Z0) / (Z1 - Z0)        # across the panel, 0..1
        across = (X1 - X0) if long_z else (Z1 - Z0)
        frame = 1 - rect_uv(X, Z, X0 + 3.0, X1 - 3.0, Z0 + 3.0, Z1 - 3.0, g)
        tubes = np.zeros_like(u)
        for k, fr in enumerate((0.3, 0.7)):
            w = 0.16
            tub = np.exp(-((u - fr) / w) ** 2)
            if flicker_tube is not None and k == flicker_tube:
                tub = tub * 0.35
            tubes = tubes + tub
        prism = 0.5 + 0.5 * np.sin(X * 3.1) * np.sin(Z * 3.1)
        prism_k = np.clip(3.0 / np.maximum(g, 1e-3) / 6.0, 0, 1)
        glow = (0.55 + 0.45 * np.clip(tubes, 0, 1.2)) * (0.96 + 0.06 * prism * prism_k)
        lens = col(TUBE)[None, :] * glow[..., None]
        emi = lens * (2.6 * lit)
        alb = lerp(col("#e8e6de") * np.ones_like(lens), col("#f0eee8") * np.ones_like(lens), 0.0)
        a = lerp(lens * 0.2, alb, frame[..., None])
        e = emi * (1 - frame[..., None])
        return a, e
    return f


# ---------------------------------------------------------------- fittings
def vent(st, X0, X1, Z0, Z1, H, name="vent", grp="back", eyes=None, slats=6, along="z", seed=0, slat_h=4.5):
    """The return-air grille in the ceiling: a white steel frame 3.5 cm wide, recessed slats running `along` one way
    (so that, looking along them, the duct's dark shows between), the duct's dark above. `eyes`: (X, Z) where the
    raccoon's face is, just above the slats: two eyes shining in a black mask, seen between two slats. `slat_h`: how
    deep the slats are (shallower where the grille is seen from far to one side, so that the eyes still show)."""
    fw = 3.5
    m_frame = painted_steel("#e6e4dc", seed=seed + 1, amt=0.05)
    # the frame: four flat strips just under the ceiling
    y = H - 0.6
    for (a0, a1, b0, b1) in ((X0, X1, Z0, Z0 + fw), (X0, X1, Z1 - fw, Z1), (X0, X0 + fw, Z0, Z1), (X1 - fw, X1, Z0, Z1)):
        st.poly([(a0, y, b0), (a1, y, b0), (a1, y, b1), (a0, y, b1)], m_frame, name, grp=grp)
    # the inner lip of the frame (2 cm deep), seen inside its edges
    lip = 2.0
    st.box(X0 + fw - 0.6, X0 + fw, H - lip, H, Z0 + fw, Z1 - fw, m_frame, name, grp=grp, shadow=False)
    st.box(X1 - fw, X1 - fw + 0.6, H - lip, H, Z0 + fw, Z1 - fw, m_frame, name, grp=grp, shadow=False)
    st.box(X0 + fw, X1 - fw, H - lip, H, Z0 + fw - 0.6, Z0 + fw, m_frame, name, grp=grp, shadow=False)
    st.box(X0 + fw, X1 - fw, H - lip, H, Z1 - fw, Z1 - fw + 0.6, m_frame, name, grp=grp, shadow=False)
    # the slats: thin blades on edge, recessed a little, running along Z (or X)
    m_slat = painted_steel("#d8d6ce", seed=seed + 2, amt=0.06)
    ix0, ix1, iz0, iz1 = X0 + fw, X1 - fw, Z0 + fw, Z1 - fw
    for i in range(slats):
        if along == "z":
            sx = ix0 + (ix1 - ix0) * (i + 0.5) / slats
            st.box(sx - 0.45, sx + 0.45, H - 1.0 - slat_h, H - 1.0, iz0, iz1, m_slat, name + "-slats", grp=grp, shadow=False)
        else:
            sz = iz0 + (iz1 - iz0) * (i + 0.5) / slats
            st.box(ix0, ix1, H - 1.0 - slat_h, H - 1.0, sz - 0.45, sz + 0.45, m_slat, name + "-slats", grp=grp, shadow=False)
    # the duct's dark above: a dark box (its inside: we look up into it)
    def m_duct(c):
        n = fbm(c.X / 8, c.Z / 8, seed + 5, 2)
        return col("#2a2e36") * (0.8 + 0.3 * n[..., None])
    st.box(X0 + fw, X1 - fw, H, H + 30, Z0 + fw, Z1 - fw, m_duct, name + "-duct", grp=grp, shadow=False, inside=True)
    if eyes is not None:
        # Ranger's face pressed to the grille, looking down into the room: a black mask, the gray of his face round it, two
        # eyes catching the light. His face is turned a little toward the room's middle (toward us), so that between the
        # slats the eyes show: a plane just above the slats' lower edges, tipped toward the lens.
        ex, ez = eyes
        tip = math.radians(72.0)                          # how far the face is tipped up from lying flat, toward us (+Z)
        hw, hh = 22.0, 15.0                               # half its width (along X) and half its height (along its own up)
        yc = H - 2.0

        def P(u, v):                                      # u across (X), v up the face (toward -Z and up)
            return (ex + u, yc + v * math.sin(tip) * 0.35, ez - v * math.cos(tip))

        def m_face(c):
            u = c.X - ex
            v = (ez - c.Z) / max(math.cos(tip), 1e-3)
            r = np.hypot(u / (hw * 0.95), v / (hh * 0.95))
            face = col("#8c8c92") * (0.8 + 0.3 * fbm(c.X / 1.5, c.Z / 1.5, seed + 13, 2))[..., None]
            mask = np.clip((1 - np.abs((v - 1.0) / 6.0)) * 3, 0, 1) * np.clip((1.15 - np.abs(u / 18.0)) * 4, 0, 1)
            out = lay(face, "#101014", mask)
            e = np.zeros_like(out)
            for sx in (-7.6, 7.6):
                d = np.hypot(u - sx, (v - 1.0) * 1.1)
                eye = np.clip((4.0 - d) * 1.2, 0, 1)
                glint = np.clip((1.3 - np.hypot(u - sx - 1.0, (v - 1.0) * 1.1 - 0.9)) * 2.0, 0, 1)
                out = lay(out, "#e8d868", eye)
                out = lay(out, "#141410", np.clip((1.5 - d) * 2.0, 0, 1))
                e = e + col("#f0e488") * (eye * 1.3)[..., None] + col("#ffffff") * (glint * 1.5)[..., None]
            nose = np.clip((2.4 - np.hypot(u, (v + 8.0) * 1.2)) * 1.5, 0, 1)
            out = lay(out, "#1a1a1e", nose)
            out = out * np.clip(1.25 - r * 0.40, 0.25, 1.2)[..., None]
            return out, e
        st.poly([P(-hw, -hh), P(hw, -hh), P(hw, hh), P(-hw, hh)], m_face, name + "-eyes", grp=grp)


def face_at_grille(st, at, view, grp="vent", name="vent-eyes", hw=19.0, hh=6.0, eye_r=4.2, glow=1.5):
    """Ranger's face pressed to a grille from above, looking down: a band of his face, the black mask across it and two
    eyes shining in it, just above the slats and turned square to the lens (`view`), so that the eyes show between the
    slats however the grille is seen. `at`: the middle of the band (X, Y, Z), a centimetre or so above the ceiling."""
    c = np.asarray(at, dtype=np.float64)
    look = np.array([view.cam_x - c[0], view.eye - c[1], view.cam_z - c[2]])
    look = look / np.linalg.norm(look)
    right = np.cross([0.0, 1.0, 0.0], look)
    right = right / np.linalg.norm(right)
    upv = np.cross(look, right)

    def m(c_):
        u, v = c_.U - hw, c_.V - hh                        # from the band's middle: u across, v up
        face = col("#8c8c92") * (0.8 + 0.3 * fbm(c_.U / 1.5, c_.V / 1.5, 331, 2))[..., None]
        mask = np.clip((1 - np.abs(v / (eye_r + 0.4))) * 3, 0, 1) * np.clip((1.15 - np.abs(u / 15.0)) * 4, 0, 1)
        out = lay(face, "#101014", mask)
        e = np.zeros_like(out)
        for sx in (-7.0, 7.0):
            d = np.hypot(u - sx, v * 1.1)
            eye = np.clip((eye_r - d) * 1.2, 0, 1)
            glint = np.clip((1.4 - np.hypot(u - sx - 1.0, v * 1.1 - 1.0)) * 2.0, 0, 1)
            out = lay(out, "#e8d868", eye)
            out = lay(out, "#141410", np.clip((1.5 - d) * 2.0, 0, 1))
            e = e + col("#f0e488") * (eye * glow)[..., None] + col("#ffffff") * (glint * 1.6)[..., None]
        out = out * np.clip(1.25 - np.abs(u / hw) * 0.5, 0.3, 1.2)[..., None]
        return out, e

    def P(a, b):
        return tuple(c + right * a + upv * b)
    st.poly([P(-hw, -hh), P(hw, -hh), P(hw, hh), P(-hw, hh)], m, name, grp=grp)


def sprinkler(st, X, Z, H, name="sprinkler", grp="back"):
    """A sprinkler head: a small chrome escutcheon and the head hanging under it."""
    st.cyl((X, Z), 3.2, H - 0.8, H, chrome(), name=name, grp=grp, shadow=False)
    st.cyl((X, Z), 0.9, H - 4.0, H - 0.8, chrome(), name=name, grp=grp, shadow=False)
    st.cyl((X, Z), 1.8, H - 4.6, H - 4.0, col("#b8463a"), name=name, grp=grp, shadow=False)        # its red glass bulb's cap


def smoke_detector(st, X, Z, r, H, name="smoke", grp="back"):
    """A round smoke detector: an off-white puck with a little green light."""
    def m(c):
        u, v = c.X - X, c.Z - Z
        rr = np.hypot(u, v)
        g = px_of(c, 2.5)
        ring = np.clip(1 - np.abs(rr - r * 0.7) / g, 0, 1) * 0.12
        out = col("#e6e2d6") * (1 - ring)[..., None]
        led = np.clip((1.0 - np.hypot(u - r * 0.45, v)) / g + 0.5, 0, 1)
        e = col("#60ff90") * (led * 0.8)[..., None]
        return out, e
    st.cyl((X, Z), r, H - 3.0, H, m, name=name, grp=grp, shadow=False)


def ceiling_speaker(st, X, Z, r, H, name="speaker", grp="back"):
    """The building's speaker in the ceiling: a round grille of fine holes in a white rim (Houston's voice comes out of it)."""
    def m(c):
        u, v = c.X - X, c.Z - Z
        rr = np.hypot(u, v)
        g = px_of(c, 2.5)
        holes = lines_aa(c.X, 1.6, 0.55, g) * lines_aa(c.Z, 1.6, 0.55, g)
        inner = np.clip((r * 0.80 - rr) / g + 0.5, 0, 1)
        out = col("#e8e6de") * (1 - inner[..., None]) + col("#b8b6ae") * inner[..., None]
        return out * (1 - 0.35 * (holes * inner)[..., None])
    st.cyl((X, Z), r, H - 1.2, H, m, name=name, grp=grp, shadow=False)


def stacking_chair(st, X, Z, face, name, grp="back", seat=46.0, back_top=86.0, w=44.0, dpt=44.0, shell=PLASTIC, seed=0, ang=None):
    """A stacking chair: a molded seat and back in gray-blue plastic on a chrome frame of four legs. `face`: which way
    its sitter faces: "+x", "-x", "+z" (toward us), "-z"; or `ang` in degrees (0: toward us, 90: toward +X)."""
    if ang is None:
        ang = {"+z": 0.0, "+x": 90.0, "-x": -90.0, "-z": 180.0}[face]
    a = math.radians(ang)
    ux, uz = math.cos(a), -math.sin(a)          # the chair's own right (as its sitter has it, facing +its z)
    vx, vz = math.sin(a), math.cos(a)           # the way the sitter faces

    def P(sx, sy, sz):
        return (X + ux * sx + vx * sz, sy, Z + uz * sx + vz * sz)
    hw, hd = w / 2, dpt / 2
    frame = col("#b8bcc4")                  # (a rod is shaded round by the stage itself)
    # four legs, splayed a little, and the side rails
    for sx in (-hw + 2.5, hw - 2.5):
        for sz in (-hd + 3, hd - 3):
            p0 = P(sx * 1.05, 0.5, sz * 1.08)
            p1 = P(sx, seat - 3, sz)
            st.stick(p0, p1, 1.05, frame, name, grp=grp)
        st.stick(P(sx, seat - 3, -hd + 3), P(sx, seat - 3, hd - 3), 0.9, frame, name, grp=grp)
        st.stick(P(sx, seat - 3, -hd + 3), P(sx, back_top - 6, -hd - 1.5), 0.95, frame, name, grp=grp)       # the back's uprights
    st.feet[name] = (X - hw, X + hw, Z - hd, Z + hd) if abs(ux) > 0.5 else (X - hd, X + hd, Z - hw, Z + hw)
    # the seat: a molded pan, its front edge rolled; the back: a curved panel leaning back a little
    m = molded(shell, seed)
    obox(st, (X + vx * 1.0, seat - 3.0, Z + vz * 1.0), (w - 2, 3.0, dpt - 4), ang, m, name, grp=grp)
    for i in range(4):                      # the back, in four slices so that it curves round the sitter
        s0, s1 = -hw + 1 + (w - 2) * i / 4, -hw + 1 + (w - 2) * (i + 1) / 4
        bend = 1.6 * (((s0 + s1) / 2) / hw) ** 2
        y0, y1 = seat + 14, back_top
        zb = -hd - 1.5 + bend
        pts = [P(s0, y0, zb), P(s1, y0, zb), P(s1, y1, zb - 2.5), P(s0, y1, zb - 2.5)]
        st.poly(pts, m, name, grp=grp)
        pts2 = [P(s0, y0, zb - 1.6), P(s1, y0, zb - 1.6), P(s1, y1, zb - 4.1), P(s0, y1, zb - 4.1)]
        st.poly(pts2, m, name, grp=grp)
    st.occ.append((min(P(-hw, 0, -hd)[0], P(hw, 0, hd)[0]), max(P(-hw, 0, -hd)[0], P(hw, 0, hd)[0]), seat - 3, seat,
                   min(P(-hw, 0, -hd)[2], P(hw, 0, hd)[2]), max(P(-hw, 0, -hd)[2], P(hw, 0, hd)[2])))
    return P


# ---------------------------------------------------------------- the passes
_Y, _X = np.mgrid[0:H_PIC, 0:W_PIC].astype(F32)


def wobble_field(seed):
    dx = (noise((H_PIC, W_PIC), 30, seed + 3, 3) - 0.5) * 2 * 0.7
    dy = (noise((H_PIC, W_PIC), 30, seed + 4, 3) - 0.5) * 2 * 0.7
    return dx, dy


class Passes:
    """The four passes for one scene: its wobble field (nothing a hand rules is perfectly straight: every picture and
    mask is pushed about by the same slow field, under a pixel, so all the cut-outs still fit one another exactly), the
    grading, the brush pass, the details and the finish."""

    def __init__(self, seed=12, grade_fn=None):
        self.dx, self.dy = wobble_field(seed)
        self.grade_fn = grade_fn

    def wob(self, a, rect=None):
        if rect is None:
            return sample(a, _X + self.dx, _Y + self.dy)
        x0, y0, x1, y1 = rect
        return sample(a, _X[y0:y1, x0:x1] - x0 + self.dx[y0:y1, x0:x1], _Y[y0:y1, x0:x1] - y0 + self.dy[y0:y1, x0:x1])

    def wob_near(self, a):
        yy = np.clip(np.round(_Y + self.dy), 0, H_PIC - 1).astype(np.intp)
        xx = np.clip(np.round(_X + self.dx), 0, W_PIC - 1).astype(np.intp)
        return a[yy, xx]

    def grade(self, pic, rect=None):
        return self.grade_fn(pic, rect) if self.grade_fn else pic

    @staticmethod
    def paint(crisp, seed=2, keep=0.32):
        """The brush pass, and then the built things said again crisply over it."""
        b = strokes(crisp, sizes=(9, 5, 2), seed=seed, density=1.5, jitter=0.04, keep=keep)
        hf = np.abs(crisp - blur(crisp, 1.4)).sum(axis=2)
        w = np.clip(hf * 7.0 - 0.05, 0, 1)
        w = np.maximum(w, blur(w, 0.7))
        out = lerp(b, crisp, (0.14 + 0.84 * w)[..., None])
        return np.clip(out + 0.45 * (out - blur(out, 0.9)), 0, 1)

    def maps_of(self, st):
        return self.wob(st.pick(np.minimum(st.t, 5000.0))), self.wob(st.pick(st.N[..., 1])), self.wob_near(st.pick(st.oid)), \
            [st.names.get(n, -9) for n in ("floor", "ceiling")]

    @staticmethod
    def details(pic, maps):
        """Small crisp accents: the lit front edge of every top, and a dark line where a thing stands in front of
        another far behind it."""
        t, ny, oid, skip = maps
        below_same = (np.roll(oid, -1, axis=0) == oid) & (np.roll(ny, -1, axis=0) < 0.5) & (ny > 0.9)
        below_same[-1] = False
        edge = below_same & ~np.isin(oid, skip)
        out = pic.copy()
        out[edge] = np.clip(out[edge] * 1.18 + 0.03, 0, 1)
        for ax, sh_ in ((0, 1), (0, -1), (1, 1), (1, -1)):
            tn = np.roll(t, sh_, axis=ax)
            behind = (t - tn > 14.0) & (t - tn > 0.02 * t)
            if ax == 0:
                behind[0 if sh_ == 1 else -1] = False
            else:
                behind[:, 0 if sh_ == 1 else -1] = False
            out[behind] = out[behind] * 0.80
        return out


def palette_for(px, colors, seed=3, rounds=14):
    """A palette for the picture: half the sample drawn toward the coloured and the light pixels (the small bright
    things matter most: letters, the button, the clock's hand), the first choices spread far apart."""
    rng = np.random.default_rng(seed)
    px = px.reshape(-1, 3).astype(F32)
    mx, mn = px.max(axis=1), px.min(axis=1)
    w = 0.2 + (mx - mn) * 2.2 + mx * 0.6
    n = len(px)
    take = min(n, 26000)
    cum = np.cumsum(w.astype(np.float64))
    drawn = np.minimum(np.searchsorted(cum, rng.random(take) * cum[-1]), n - 1)
    pick = np.concatenate([rng.choice(n, size=take, replace=n < take), drawn])
    sm = px[pick]
    colors = min(colors, len(np.unique((sm * 255).astype(np.uint8), axis=0)))
    centers = np.empty((colors, 3), dtype=F32)
    centers[0] = sm[rng.integers(len(sm))]
    d = ((sm - centers[0]) ** 2).sum(axis=1)
    for k in range(1, colors):
        i = int(d.argmax())
        centers[k] = sm[i]
        d = np.minimum(d, ((sm - centers[k]) ** 2).sum(axis=1))
    for _ in range(rounds):
        dist = ((sm[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        near = dist.argmin(axis=1)
        for k in range(colors):
            mine = sm[near == k]
            if len(mine):
                centers[k] = centers[k] * 0.25 + mine.mean(axis=0) * 0.75
    return centers


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.007, amount=0.011, pal=None):
    g = grain(picture, seed, amount)
    if pal is None:
        sample_of = g if alpha is None else g[alpha > 0.5]
        pal = palette_for(sample_of, colors)
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def to_image(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def tones(a, label=""):
    lum = (np.clip(a, 0, 1) * 255) @ LUM
    print(label, "mean", (a.mean(axis=(0, 1)) * 255).round(0), "lum 5/25/50/75/95:", np.percentile(lum, [5, 25, 50, 75, 95]).round(0))


def cover(st, grp=None, name=None):
    """The share of each picture pixel that a group (or named things) fills."""
    if grp is not None:
        gs = [grp] if isinstance(grp, str) else list(grp)
        m = np.isin(st.grp, [st.groups[g] for g in gs if g in st.groups])
    else:
        m = st.mask_of(*([name] if isinstance(name, str) else name))
    return st.down(m.astype(F32))


def bbox(mask, pad=0):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max()) + 1 + pad, int(ys.max()) + 1 + pad]


def clamp_rect(r, pad=6):
    return (max(0, r[0] - pad), max(0, r[1] - pad), min(W_PIC, r[2] + pad), min(H_PIC, r[3] + pad))


def letters(pic, view, words, groups=None, rect=None, clips=None):
    """Lay words through the camera, crisp, over the painted picture: (mask, quad in the room, ink, amount, group). The
    ink takes the light of the paper it is on (sampled under the quad's middle). `clips`: {group: picture-size mask}
    where the words of that group may show (a sign seen through a doorway is not laid on the door in front of it)."""
    covered = np.zeros(pic.shape[:2], F32)
    for mask, quad, ink, amount, grp in words:
        if groups is not None and grp not in groups:
            continue
        if clips is not None and grp in clips:
            keep = pic.copy()
        cx = sum(q[0] for q in quad) / 4
        cy = sum(q[1] for q in quad) / 4
        cz = sum(q[2] for q in quad) / 4
        px, py = view.pt(cx, cy, cz)
        if rect:
            px, py = px - rect[0], py - rect[1]
        iy, ix = int(min(max(py, 0), pic.shape[0] - 1)), int(min(max(px, 0), pic.shape[1] - 1))
        here = pic[max(iy - 2, 0):iy + 3, max(ix - 2, 0):ix + 3].reshape(-1, 3)
        k = np.clip(np.percentile(here.max(axis=1), 80) / 0.88, 0.3, 1.1)
        tone = col(ink) * k
        cov = lay_on(pic, view, quad, mask, tone, amount=amount, sub=4, crisp=0.6, rect=rect)
        if clips is not None and grp in clips:
            c = clips[grp][..., None]
            pic[...] = keep * (1 - c) + pic * c
            cov = cov * clips[grp]
        covered = np.maximum(covered, cov)
    return covered


def wall_quad(wall, u0, u1, v0, v1, at=0.0, lift=0.25):
    """The four corners (top left, top right, bottom right, bottom left, as one looks at it) of a flat thing on a wall:
    "back" (the wall Z = at, u is X), "left" (X = at, u is Z, seen from +X: u runs toward us), "right" (X = at, seen from
    -X: u runs away from us). `lift`: cm off the wall, toward the room."""
    if wall == "back":
        z = at + lift
        return [(u0, v1, z), (u1, v1, z), (u1, v0, z), (u0, v0, z)]
    if wall == "left":
        x = at + lift
        return [(x, v1, u1), (x, v1, u0), (x, v0, u0), (x, v0, u1)]
    x = at - lift
    return [(x, v1, u0), (x, v1, u1), (x, v0, u1), (x, v0, u0)]


# ---------------------------------------------------------------- the layout's measuring tools
def hull(points):
    """Convex hull (monotone chain) of [(x, y)]."""
    pts = sorted(set(map(tuple, points)))
    if len(pts) <= 2:
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


def simplify(poly, most=12):
    """Drop the points of a closed outline that bend it least, until `most` are left."""
    p = list(poly)
    while len(p) > most:
        best, bi = 1e18, 0
        for i in range(len(p)):
            a, b, c = p[i - 1], p[i], p[(i + 1) % len(p)]
            area = abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]))
            if area < best:
                best, bi = area, i
        p.pop(bi)
    return p


def inside(pt, poly):
    x, y = pt
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1:
            c = not c
    return c


def poly_of_mask(m, most=12, pad=1.0):
    """A convex outline (at most `most` points) round the pixels of a mask, a pixel of air round it."""
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    pts = np.stack([xs, ys], 1)
    corners = np.concatenate([pts + [0, 0], pts + [1, 0], pts + [0, 1], pts + [1, 1]])
    h = hull([tuple(p) for p in corners.tolist()])
    h = simplify(h, most)
    cx, cy = np.mean([p[0] for p in h]), np.mean([p[1] for p in h])
    out = []
    for x, y in h:
        d = math.hypot(x - cx, y - cy) + 1e-6
        out.append([int(round(min(max(x + (x - cx) / d * pad, 0), W_PIC))), int(round(min(max(y + (y - cy) / d * pad, 0), H_PIC)))])
    return out


def rect_of_mask(m, pad=1):
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    x0, y0, x1, y1 = int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max()) + 1 + pad, int(ys.max()) + 1 + pad
    x0, y0 = max(x0, 0), max(y0, 0)
    x1, y1 = min(x1, W_PIC), min(y1, H_PIC)
    return [x0, y0, x1 - x0, y1 - y0]

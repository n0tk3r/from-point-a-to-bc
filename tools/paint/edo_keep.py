"""PAINT-20E: edo-keep, inside Himeji's keep, a lower floor (the second floor, where the weapon racks line the wall
gallery), late afternoon, spring 1830 (S/briefs/out/edo-design.md, section 5, #29), in the act's manner
(S/work-20-paintA/style.md: flats, one contour round the silhouettes, the blue leading).

    python3 edo_keep.py fast      the under-painting with the contours, no brush pass (seconds)
    python3 edo_keep.py           everything: out/edo-keep/ (back, the cut-outs, the beams' light pictures, layout.json)

ONE CAMERA (room.View): horizon 180, full 440 (the lens 284 cm up), standing at X 430, Z 1000 in a room 760 wide,
1000 deep and 380 high (the floor above's joists are the ceiling), looking square at the back wall. The room is
measured in centimetres: X across (left to right along the back wall), Y up, Z out toward us.

THE PICTURE. Back wall: lime-plastered panels between dark posts on a sill beam, a nageshi rail and a lintel; in it, at
head height and above, the three gun ports, round, triangular and square (left to right), each a bright shape of the
sun's paper. Left: the steep ladder-stair up (51 degrees, a rail on its open side), its foot toward us, its top in an
opening of the ceiling; the young warden's post at its foot. Left of centre: the great pillar, one enormous trunk,
floor to ceiling, through both, lit along its right edge by the ports' light. Right wall, receding: the weapon racks
(spears standing in a row on a long rack, their heads up, guns racked below: dim flats). The stone-drop flap at the
back wall's foot in the right corner. Near us at the right: the plasterers' tubs and the stack of lime by the way in
(the doorway in the right wall, at the picture's right edge). Front plane: a plank on two buckets and a bundle of
brushes, cut by the picture's edge.

LIGHT (keep to it). The sun is low in the west, behind the back wall: it comes through the three ports as three
beams, down and toward us and a little to the left (elevation 33 degrees, 20 degrees left of the wall's normal), each
landing on the floor in its own shape stretched along the beam. THE BEAMS ARE LIGHT AND ARE NOT IN THE BACKDROP: each
is its own light picture (beam-round.png, beam-tri.png, beam-square.png: the beam in the dusty air and its patch on
the floor, RGBA with a soft alpha, for the live layer), and layout.json gives its polygons. The backdrop is the room
in the light that is left, as a print lays it: flats. The panels nearest the ports are the lit flats (the paper), the
rest of the plaster a step into the blue shade; the floor one flat of sienna wood; the ceiling, the side walls and the
foreground the darks (prussian in the wood). Cast shadows are hard-edged flats pulled toward cobalt.

PAINT-20E."""

import json
import math
import os
import sys
import time

import numpy as np

from brush import F32, lerp, noise, blur, mask_poly, mask_ellipse, mask_line, Sheet, over, vary
from room import View
from edo_keep_kit import (Room, Passes, boards, panels, joists, post, box, finish_scene, save_rgba, to_image, ipt, col,
                          stand_in, shade_of, dark_of, tint_of, boundary, _hull, W, H, SHAPE, P, PAPER, NAPLES, OCHRE, SIENNA,
                          PRUSSIAN, COBALT, ULTRA)

ID = "edo-keep"
OUT = "out/edo-keep"
WORK = "out/edo-keep-work"
VIEW = dict(horizon=180, full=440, cam=(430.0, 1000.0), yaw=0.0, focal=600.0)
RW, RD, RH = 760.0, 1000.0, 380.0                      # the room: width, depth, the ceiling (the floor above)
V = View(**VIEW)

# the sun: through the back wall (Z = 0), coming toward us (+Z), down, and a little to the left (-X)
EL, AZ = 33.0, 20.0
SUN = (-math.sin(math.radians(AZ)) * math.cos(math.radians(EL)), -math.sin(math.radians(EL)), math.cos(math.radians(AZ)) * math.cos(math.radians(EL)))

# the ports in the back wall: (kind, X of the middle, Y of the middle, half size)
PORTS = [("round", 440.0, 205.0, 22.0), ("tri", 560.0, 205.0, 27.0), ("square", 680.0, 205.0, 23.0)]
PILLAR = (250.0, 200.0, 48.0)                           # X, Z, radius: the great pillar
STAIR = dict(X0=110.0, X1=210.0, z_foot=400.0, z_top=100.0, steps=14, rise=RH)
RACK = (60.0, 500.0)                                    # along the right wall, Z from..to
DOOR = (380.0, 470.0)                                   # the way in: a doorway in the right wall, Z from..to
DROP = (690.0, 750.0, 0.0, 62.0)                        # the stone-drop flap: X0, X1, Z0, Z1 (hinged at the wall)
TUBS = [(600.0, 490.0, 30.0, 34.0), (664.0, 520.0, 27.0, 30.0), (560.0, 560.0, 33.0, 26.0)]     # X, Z, radius, height
LIME = (690.0, 745.0, 470.0, 540.0, 48.0)               # the stack of lime (bags): X0, X1, Z0, Z1, height

# where people stand (X, Z), facing
MARKS = {
    "enter": ((700.0, 430.0), "W"), "pillar": ((250.0, 310.0), "N"), "racks": ((690.0, 260.0), "E"), "ports": ((560.0, 400.0), "N"),
    "tubs": ((500.0, 444.0), "E"), "stairs": ((165.0, 446.0), "N"), "shinnosuke": ((282.0, 436.0), "W"), "drop": ((690.0, 130.0), "N"),
    "mid": ((400.0, 330.0), "S"),
}

# the act's paints, mixed by name (style.md, section 2): wood ochre lit and sienna in shade, darks by prussian, the
# plaster the paper, the sun's warmth naples
WOOD = lerp(SIENNA, OCHRE, 0.25)                        # a post, a tread, where the light that is left reaches it
WOOD_S = lerp(SIENNA, PRUSSIAN, 0.4)                    # wood in shade
WOOD_D = lerp(SIENNA, PRUSSIAN, 0.65)                   # the deepest wood
FLOOR = lerp(lerp(SIENNA, OCHRE, 0.3), PRUSSIAN, 0.38)   # the floor: sienna wood in the keep's dim
PLASTER = lerp(PAPER, PRUSSIAN, 0.2)                    # the paper in the keep's dim
CEIL = lerp(SIENNA, PRUSSIAN, 0.65)
CEIL_D = lerp(SIENNA, PRUSSIAN, 0.82)
SUN_C = lerp(NAPLES, PAPER, 0.35)                       # the beams and their patches: naples with lead white
SKY = lerp(NAPLES, PAPER, 0.55)                         # the sun's paper in the ports
STEEL = lerp(PAPER, PRUSSIAN, 0.45)                     # a spearhead's grey: a blue


def port_pts(kind, X, Y, s):
    """The port's outline in the back wall (room points, Z = 0)."""
    if kind == "round":
        return [(X + s * math.cos(a), Y + s * math.sin(a), 0.0) for a in np.linspace(0, 2 * math.pi, 20, endpoint=False)]
    if kind == "tri":
        return [(X, Y + s * 1.1, 0.0), (X + s * 1.05, Y - s * 0.75, 0.0), (X - s * 1.05, Y - s * 0.75, 0.0)]
    return [(X - s, Y - s, 0.0), (X + s, Y - s, 0.0), (X + s, Y + s, 0.0), (X - s, Y + s, 0.0)]


def land(p):
    """Where a point of a port lands on the floor along the sun's direction."""
    t = p[1] / -SUN[1]
    return (p[0] + SUN[0] * t, 0.0, p[2] + SUN[2] * t)


# ---------------------------------------------------------------- the room
def shell(R):
    """Floor, walls, ceiling: flats in depth order, far to near."""
    X, Z, okf, fp = R.floor_uv()
    floor_m = okf * (X >= -5) * (X <= RW + 5) * (Z >= -5) * (Z <= RD)
    u, v, okw, fpw = R.wall_uv("Z", 0.0)
    back_m = okw * (u >= 0) * (u <= RW) * (v >= 0) * (v <= RH)
    ul, vl, okl, fpl = R.wall_uv("X", 0.0)
    left_m = okl * (ul >= 0) * (ul <= RD) * (vl >= 0) * (vl <= RH)
    ur, vr, okr, fpr = R.wall_uv("X", RW)
    right_m = okr * (ur >= 0) * (ur <= RD) * (vr >= 0) * (vr <= RH)
    Xc, Zc, okc, fpc = R.floor_uv(RH)
    ceil_m = okc * (Xc >= -5) * (Xc <= RW + 5) * (Zc >= -5) * (Zc <= RD)
    # the back wall: the panels nearest the ports are the lit ones (a step), the rest in the blue shade
    centre = sum(p[1] for p in PORTS) / 3.0

    def lit(uu):
        return (np.abs(uu - centre) < 290).astype(F32) * 0.8 + 0.2
    panels(R, back_m, "Z", 0.0, PLASTER, WOOD_S, WOOD_D, RW, RH, post_every=190.0, post_w=24.0, offset=-7.0, sill_h=30.0,
           lintel_h=26.0, nageshi=(285.0, 301.0), seed=4, alpha=0.55, lit=lit)
    # the ports: the sun's paper, with a dark reveal round each
    for kind, px, py, s in PORTS:
        pts = port_pts(kind, px, py, s)
        rev = [(x + (x - px) * 0.18, y + (y - py) * 0.18, z) for x, y, z in pts]
        mr = R.flat(rev, WOOD_D, amount=0.02)
        R.thing(mr, 0.6)
        R.flat(pts, SKY, amount=0.02, cell=12)
    # the side walls, in shade (the left deeper: nothing lights it)
    panels(R, left_m, "X", 0.0, PLASTER, WOOD_S, WOOD_D, RD, RH, post_every=190.0, post_w=24.0, offset=10.0, sill_h=30.0,
           lintel_h=26.0, nageshi=(285.0, 301.0), seed=5, alpha=0.5, shade_k=0.78)
    panels(R, right_m, "X", RW, PLASTER, WOOD_S, WOOD_D, RD, RH, post_every=190.0, post_w=24.0, offset=10.0, sill_h=30.0,
           lintel_h=26.0, nageshi=(285.0, 301.0), seed=6, alpha=0.55, shade_k=0.62)
    # the doorway in the right wall: a dark opening, its jamb a post
    d0, d1 = DOOR
    md = R.flat([(RW, 0, d0), (RW, 0, d1), (RW, 200, d1), (RW, 200, d0)], dark_of(SIENNA, 0.85), amount=0.02)
    R.thing(md, 0.7)
    mj = R.flat([(RW, 0, d0), (RW, 0, d0 + 12), (RW, 200, d0 + 12), (RW, 200, d0)], WOOD_S, amount=0.03)
    R.thing(mj, 0.7)
    # the ceiling: the boards of the floor above and its joists, running toward us
    joists(R, ceil_m, RH, CEIL, CEIL_D, along="Z", every=95.0, width=26.0, offset=20.0, X0=0, X1=RW, Z0=0, Z1=RD, seed=6, alpha=0.45)
    s = STAIR
    mo = R.flat([(s["X0"], RH, 0.0), (s["X1"] + 10, RH, 0.0), (s["X1"] + 10, RH, s["z_top"] + 70), (s["X0"], RH, s["z_top"] + 70)], dark_of(SIENNA, 0.9), amount=0.02)
    R.thing(mo, 0.5)
    # the floor: one flat of boards, its joints drawn
    boards(R, floor_m, FLOOR, along="Z", width=30.0, offset=7.0, seed=3, line_alpha=0.3)
    # the floor's cast shadows: hard-edged flats toward cobalt. The stairs' shadow (the ports' light from behind-right
    # lays it to the left of the flight), the pillar's contact, the tubs'
    sh = mask_poly(SHAPE, R.V.poly([(s["X0"] - 90, 0, s["z_top"] + 60), (s["X0"], 0, s["z_top"] + 60), (s["X0"], 0, s["z_foot"] + 20), (s["X0"] - 40, 0, s["z_foot"] + 20)]))
    R.shade(sh * floor_m, 0.4)
    X0, Z0, r = PILLAR
    foot = mask_poly(SHAPE, R.V.poly([(X0 - r - 60, 0, Z0 - r), (X0 + r + 10, 0, Z0 - r), (X0 + r + 10, 0, Z0 + r + 30), (X0 - r - 60, 0, Z0 + r + 30)]))
    R.shade(foot * floor_m, 0.35)
    for (tx, tz, tr, th) in TUBS:
        e = mask_poly(SHAPE, R.V.poly([(tx - tr - 30, 0, tz - tr * 0.3), (tx + tr * 0.6, 0, tz - tr * 0.3), (tx + tr * 0.6, 0, tz + tr * 0.9), (tx - tr - 30, 0, tz + tr * 0.9)]))
        R.shade(e * floor_m, 0.35)
    X0, X1, Z0, Z1, h = LIME
    e = mask_poly(SHAPE, R.V.poly([(X0 - 40, 0, Z0), (X0, 0, Z0), (X0, 0, Z1 + 10), (X0 - 40, 0, Z1 + 10)]))
    R.shade(e * floor_m, 0.35)
    return floor_m, back_m, right_m


def stairs(R, grp="stairs"):
    """The steep ladder-stair up along the left wall: the flight as one dark side flat with its treads and risers as
    flats, the far ones first; its rail on the open side."""
    s = STAIR
    X0, X1, zf, zt, n, rise = s["X0"], s["X1"], s["z_foot"], s["z_top"], s["steps"], s["rise"]
    m = np.zeros(SHAPE, F32)
    # the closed side (the stringer and the boards under the flight), one flat
    side = R.V.poly([(X1, 0, zf), (X1, 0, zt + (zf - zt) / n), (X1, rise, zt), (X1, rise, zt), (X1, rise - rise / n, zt)])
    side = R.V.poly([(X1, 0, zf), (X1, rise, zt), (X1, rise, zt + (zf - zt) / n * 0.0), (X1, 0, zf)])
    # treads and risers, the farthest first
    boxes = R.V.stairs(X0, X1, zf, zt, rise, n)
    for (bX0, bX1, bY0, bY1, bZ0, bZ1) in boxes:
        for name, pp, nrm in R.V.box(bX0, bX1, bY0, bY1, bZ0, bZ1):
            c = {"top": WOOD, "front": WOOD_S, "right": WOOD_D, "left": WOOD_D, "back": WOOD_S, "bottom": WOOD_D}[name]
            m = np.maximum(m, R.flat2d(pp, c, grp, amount=0.03, cell=60))
    R.thing(m, 0.85)
    # the treads' nosings: the edge where a tread turns down into its riser is a built edge (a line, 0.7)
    for (bX0, bX1, bY0, bY1, bZ0, bZ1) in boxes:
        r = R.V.line((bX0, bY1, bZ1), (bX1, bY1, bZ1))
        if r:
            ln = mask_line(SHAPE, [r[0], r[1]], 1.0)
            R.things.append((np.zeros(SHAPE, F32), ln * m, PRUSSIAN, 0.5))
    # the rail: three posts and the rail, each a flat with its contour
    for (z, y0, y1) in ((zf - 2, 0, 95), (zf - (zf - zt) * 0.5, rise * 0.5, rise * 0.5 + 95), (zt + 4, rise - 20, rise + 75)):
        pp = R.V.poly([(X1, y0, z - 4), (X1 + 6, y0, z - 4), (X1 + 6, y1, z + 4), (X1, y1, z + 4)])
        if len(pp) >= 3:
            mk = R.flat2d(pp, WOOD_D, grp, amount=0.03)
            m = np.maximum(m, mk)
            R.thing(mk, 0.85)
    pp = R.V.poly([(X1 + 3, 95, zf - 2), (X1 + 3, rise + 75, zt + 4), (X1 + 3, rise + 83, zt + 4), (X1 + 3, 103, zf - 2)])
    mk = R.flat2d(pp, WOOD, grp, amount=0.03)
    m = np.maximum(m, mk)
    R.thing(mk, 0.85)
    return [ipt(R.V.pt(X1 + 6, 0, zf)), ipt(R.V.pt(X1 + 6, 0, zt))]


def pillar(R, grp="pillar"):
    """The great pillar: one trunk, two flats (its shade toward us, a lit edge on the right where the ports' light
    strikes it), one contour round its silhouette."""
    X, Z, r = PILLAR
    m, (xl, xr, top, bot) = post(R, X, Z, r, -2.0, RH + 2.0, lerp(OCHRE, SIENNA, 0.5), lit_from=(1.0, -0.4), lit_share=0.22, grp=grp, alpha=0.85, shade_k=0.45)
    return [int(round(R.V.pt(X, 0, Z + r)[1]))]


def racks(R, grp="racks"):
    """The weapon racks along the right wall: a long rack (two rails on posts), spears standing in a row against it,
    each shaft a flat with its contour and its head a pale leaf; guns racked below as dark lengths. Dim: the flats are
    pulled into the shade."""
    z0, z1 = RACK
    V_ = R.V
    sh = lambda c, k=0.3: shade_of(c, k)
    # the rack's rails: two long flats along the wall, on short posts
    for y, h in ((205.0, 10.0), (58.0, 9.0)):
        pp = V_.poly([(RW - 26, y, z0), (RW - 26, y, z1), (RW - 26, y + h, z1), (RW - 26, y + h, z0)])
        if len(pp) >= 3:
            mk = R.flat2d(pp, sh(WOOD_S), grp, amount=0.03)
            R.thing(mk, 0.6)
    for z in (z0, (z0 + z1) / 2, z1):
        pp = V_.poly([(RW - 30, 0, z - 4), (RW - 22, 0, z - 4), (RW - 22, 218, z + 4), (RW - 30, 218, z + 4)])
        if len(pp) >= 3:
            mk = R.flat2d(pp, sh(WOOD_D), grp, amount=0.03)
            R.thing(mk, 0.6)
    # spears: a shaft 3.5 cm wide leaning a little, a head 26 cm long
    z = z0 + 14
    k = 0
    while z < z1 - 10:
        lean = 1.5 + 2.5 * ((k * 7919) % 11) / 10.0
        top = 236.0 + ((k * 31) % 5) * 4
        pp = V_.poly([(RW - 23 - lean, 12.0, z), (RW - 23 - lean, 12.0, z + 5.0), (RW - 32, top, z + 5.0), (RW - 32, top, z)])
        if len(pp) >= 3:
            mk = R.flat2d(pp, sh(lerp(OCHRE, SIENNA, 0.45), 0.3), grp, amount=0.03)      # (no contour: thinner than the line)
        hd = V_.poly([(RW - 32, top, z + 2.5), (RW - 33, top + 9, z + 7.0), (RW - 34, top + 28, z + 2.5), (RW - 33, top + 9, z - 2)])
        if len(hd) >= 3:
            mk = R.flat2d(hd, sh(STEEL, 0.2), grp, amount=0.02)
            R.thing(mk, 0.4)
        z += 40
        k += 1
    # guns racked below: dark lengths lying across the lower rail, their stocks up
    z = z0 + 24
    k = 0
    while z < z1 - 24:
        pp = V_.poly([(RW - 36, 40.0, z), (RW - 36, 40.0, z + 5), (RW - 12, 96.0, z + 19), (RW - 12, 96.0, z + 14)])
        if len(pp) >= 3:
            mk = R.flat2d(pp, sh(WOOD_D, 0.3), grp, amount=0.03)
            R.thing(mk, 0.6)
        z += 46
        k += 1
    return [ipt(V_.pt(RW - 30, 0, z1)), ipt(V_.pt(RW - 30, 0, z0))]


def drop(R):
    """The stone-drop: a hinged flap in the floor against the back wall's foot, its boards across, an iron ring."""
    X0, X1, Z0, Z1 = DROP
    m = R.flat([(X0, 1, Z0), (X1, 1, Z0), (X1, 1, Z1), (X0, 1, Z1)], shade_of(FLOOR, 0.25), amount=0.03)
    R.thing(m, 0.6)
    ln = np.zeros(SHAPE, F32)
    for z in np.linspace(Z0 + 14, Z1 - 14, 3):
        r = R.V.line((X0 + 2, 1, z), (X1 - 2, 1, z))
        if r:
            ln = np.maximum(ln, mask_line(SHAPE, [r[0], r[1]], 1.0))
    R.things.append((np.zeros(SHAPE, F32), ln * m, PRUSSIAN, 0.3))
    ring = R.V.pt((X0 + X1) / 2, 2, Z1 - 12)
    rm = mask_ellipse(SHAPE, ring[0], ring[1], 4.0, 2.2)
    R.fill(rm, dark_of(SIENNA, 0.8), amount=0.02)
    R.thing(rm, 0.6)
    return [ipt(R.V.pt(X0, 0, Z0)), ipt(R.V.pt(X1, 0, Z0)), ipt(R.V.pt(X1, 0, Z1)), ipt(R.V.pt(X0, 0, Z1))]


def tubs(R, grp="tubs"):
    """The plasterers' tubs (wooden, hooped, lime slurry in them) and the stack of lime bags by the way in."""
    base_row = 0
    for (X, Z, r, h) in sorted(TUBS, key=lambda t: t[1]):
        m, (xl, xr, top, bot) = post(R, X, Z, r, 0.0, h, lerp(OCHRE, SIENNA, 0.45), lit_from=(1.0, -0.4), lit_share=0.3, grp=grp, alpha=0.85, shade_k=0.4)
        # the rim: the inside seen from above as the paper (the slurry), with a dark inner edge
        rim = [(X + r * math.cos(a), h, Z + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 18, endpoint=False)]
        mr = R.flat(rim, WOOD_D, grp, amount=0.03)
        inner = [(X + r * 0.82 * math.cos(a), h - 1, Z + r * 0.82 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 18, endpoint=False)]
        mi = R.flat(inner, lerp(PAPER, PRUSSIAN, 0.1), grp, amount=0.02)
        R.thing(mr, 0.85)
        R.thing(mi, 0.6)
        # two hoops: flats across the body
        for y in (h * 0.3, h * 0.75):
            hp = [(X + (r + 1) * math.cos(a), y, Z + (r + 1) * math.sin(a)) for a in np.linspace(math.pi, 2 * math.pi, 10)]
            pp = R.V.poly(hp + [(X + (r + 1) * math.cos(a), y + 2.5, Z + (r + 1) * math.sin(a)) for a in np.linspace(2 * math.pi, math.pi, 10)])
            if len(pp) >= 3:
                mh = R.flat2d(pp, dark_of(SIENNA, 0.8), grp, amount=0.02)
                R.thing(mh, 0.5)
        base_row = max(base_row, R.V.pt(X, 0, Z + r)[1])
    # the lime: bags stacked, the paper's colour in the shade
    X0, X1, Z0, Z1, h = LIME
    for i, (y0, y1) in enumerate(((0, h * 0.5), (h * 0.5, h))):
        dx = 6 * i
        box(R, X0 + dx, X1 - dx, y0, y1, Z0 + dx, Z1 - dx, lerp(PAPER, PRUSSIAN, 0.25), grp=grp, alpha=0.85, lit=("top",), shade_k=0.35, wobble=1.0)
    base_row = max(base_row, R.V.pt(X0, 0, Z1)[1])
    return int(round(base_row))


def front(R, grp="front"):
    """The front plane at the bottom left: a plasterer's plank on two buckets and a bundle of brushes, cut by the edge."""
    for X in (90, 300):
        post(R, X, 595, 22, 0, 38, lerp(OCHRE, SIENNA, 0.6), lit_from=(1.0, -0.4), lit_share=0.3, grp=grp, alpha=0.85, shade_k=0.45)
    box(R, 40, 330, 38, 44, 570, 620, lerp(OCHRE, SIENNA, 0.4), grp=grp, alpha=0.85, lit=("top",), shade_k=0.4)
    for i, x in enumerate((140, 165, 190)):
        pp = R.V.poly([(x, 44, 580), (x + 8, 44, 580), (x + 26, 44, 616), (x + 18, 44, 616)])
        if len(pp) >= 3:
            mk = R.flat2d(pp, lerp(PAPER, OCHRE, 0.4) if i != 1 else lerp(OCHRE, SIENNA, 0.5), grp, amount=0.03)
            R.thing(mk, 0.85)
    return "front"


# ---------------------------------------------------------------- the beams (light pictures)
def beam_picture(kind, X, Y, s):
    """One beam's light: the port's outline at the wall and its patch on the floor (a hard-edged flat of the sun's
    paper), the air between as a soft volume. -> (rgb, alpha, port poly, patch poly, air poly) in picture pixels."""
    pts = port_pts(kind, X, Y, s)
    floor = [land(p) for p in pts]
    pp_port = V.poly(pts)
    pp_patch = V.poly(floor)
    hull = _hull(pp_port + pp_patch)
    rgb_ = np.zeros((H, W, 3), F32) + SUN_C[None, None, :]
    patch = mask_poly(SHAPE, pp_patch, soft=0.6)
    halo = blur(patch, 6.0)
    air = mask_poly(SHAPE, hull, soft=2.5)
    y, x = np.mgrid[0:H, 0:W].astype(F32)
    ytop = min(p[1] for p in pp_port)
    ybot = max(p[1] for p in pp_patch)
    grad = np.clip((y - ytop) / max(1.0, ybot - ytop), 0, 1)
    airk = air * (0.20 + 0.14 * grad)
    n = noise(SHAPE, (4, 40), 31 + len(kind), 3)
    airk = airk * (0.75 + 0.5 * n)
    alpha = np.clip(airk + halo * 0.3 + patch * 0.72, 0, 0.95)
    rgb_ = lerp(rgb_, lerp(PAPER, NAPLES, 0.25)[None, None, :], patch[..., None] * 0.5)
    rgb_ = lerp(rgb_, lerp(NAPLES, OCHRE, 0.3)[None, None, :], (airk * 2.5).clip(0, 1)[..., None] * 0.3)
    return rgb_, alpha, [ipt(p) for p in pp_port], [ipt(p) for p in pp_patch], [ipt(p) for p in hull]


# ---------------------------------------------------------------- the whole picture
def render(include=("stairs", "pillar", "racks", "tubs", "front"), seed=1):
    R = Room(V, seed=seed, base=dark_of(SIENNA, 0.8))
    info = {}
    floor_m, back_m, right_m = shell(R)
    info["drop"] = drop(R)
    if "racks" in include:
        info["racks_base"] = racks(R)
    if "stairs" in include:
        info["stairs_base"] = stairs(R)
    if "pillar" in include:
        info["pillar_base"] = pillar(R)
    if "tubs" in include:
        info["tubs_base"] = tubs(R)
    if "front" in include:
        front(R)
    return R, info


PASS = Passes(seed=11)


def paint(R, fast):
    pic = R.img.copy()
    if not fast:
        pic = PASS.paint(pic, keep=0.28)
    pic = R.contours(pic)
    return np.clip(pic, 0, 1)


def layout(info, beams):
    V_ = V
    pt = lambda X, Z: [min(799, max(0, ipt(V_.pt(X, 0, Z))[0])), min(599, max(0, ipt(V_.pt(X, 0, Z))[1]))]      # (clipped to the stage)
    marks = {k: {"at": pt(*xz), "face": f} for k, (xz, f) in MARKS.items()}
    s = STAIR
    X, Z, r = PILLAR
    walk = [pt(30, 20), pt(100, 20), pt(100, s["z_foot"] + 40), pt(s["X1"] + 20, s["z_foot"] + 40), pt(s["X1"] + 20, 20),
            pt(RW - 40, 20), pt(RW - 40, 440), pt(520, 440), pt(520, 450), pt(30, 450)]
    blocked = [
        {"id": "pillar", "poly": [pt(X - r, Z - r), pt(X + r, Z - r), pt(X + r, Z + r), pt(X - r, Z + r)]},
        {"id": "stairs", "poly": [pt(s["X0"] - 10, s["z_top"] - 10), pt(s["X1"] + 14, s["z_top"] - 10), pt(s["X1"] + 14, s["z_foot"] + 10), pt(s["X0"] - 10, s["z_foot"] + 10)]},
        {"id": "tubs", "poly": [pt(520, 455), pt(RW, 455), pt(RW, 600), pt(520, 600)]},
    ]
    things = {
        "pillar": {"poly": "the cut-out pillar's silhouette", "stand": marks["pillar"]["at"]},
        "stairs": {"poly": "the cut-out stairs' silhouette", "stand": marks["stairs"]["at"]},
        "racks": {"poly": "the cut-out racks' silhouette", "stand": marks["racks"]["at"]},
        "drop": {"poly": info["drop"], "stand": marks["drop"]["at"]},
        "tubs": {"poly": "the cut-out tubs' silhouette", "stand": marks["tubs"]["at"]},
        "floor": {"stand": marks["mid"]["at"]},
        "ceiling": {"poly": [ipt(V_.pt(0, RH, 0)), ipt(V_.pt(RW, RH, 0)), [800, 0], [0, 0]]},
        "crew": {"stand": marks["enter"]["at"], "note": "the plasterers work by the tubs and the wall at the right"},
        "shinnosuke": {"stand": marks["shinnosuke"]["at"]},
    }
    for b in beams:
        things["port" + b["kind"]] = {"poly": b["port"], "stand": marks["ports"]["at"]}
    things["ports"] = {"poly": _hull([tuple(p) for b in beams for p in b["port"]]), "stand": marks["ports"]["at"]}
    things["beams"] = {"poly": [list(p) for p in _hull([tuple(p) for b in beams for p in b["air"]])], "stand": marks["ports"]["at"]}
    things["ports"]["poly"] = [list(p) for p in things["ports"]["poly"]]
    out = {
        "scene": ID, "size": [W, H], "view": VIEW, "horizon": VIEW["horizon"], "full": VIEW["full"],
        "room_cm": {"X": [0, RW], "Z": [0, RD], "H": RH, "note": "X across the back wall, Y up, Z toward us; the camera at (430, 1000), the lens 284 cm up"},
        "walk": walk, "blocked": blocked,
        "marks": marks,
        "stands": {k: {"at": v["at"], "grownup_px": int(round(V_.person(*MARKS[k][0])[2] * 160 / 175))} for k, v in marks.items()},
        "planes": [
            {"id": "racks", "src": "racks.png", "base": info.get("racks_base"), "note": "on the right wall: nobody passes behind it; a cut-out so that it can be dimmed or lit apart"},
            {"id": "stairs", "src": "stairs.png", "base": info.get("stairs_base"), "note": "the flight and its rail: people on the floor beyond its open side (toward the left wall) are drawn behind it"},
            {"id": "pillar", "src": "pillar.png", "base": info.get("pillar_base", [0])[0]},
            {"id": "tubs", "src": "tubs.png", "base": info.get("tubs_base")},
            {"id": "front", "src": "front.png", "plane": "front"},
        ],
        "things": things,
        "sun": {"elevation_deg": EL, "azimuth_off_wall_deg": -AZ, "direction_room": [round(c, 3) for c in SUN],
                "note": "through the back wall, toward us, down, and to the left; the patches creep toward the wall about 2.5 cm (2 px) a minute as the sun sinks"},
        "beams": beams,
        "fx": [
            {"id": "beam-" + b["kind"], "type": "beam", "src": "beam-" + b["kind"] + ".png", "layer": "live", "blend": "screen", "air": b["air"], "patch": b["patch"], "port": b["port"],
             "dust": {"count": 18, "size": [1, 2], "drift": [-2, 6], "opacity": 0.5}, "travel": {"dx": -0.4, "dy": 1.6, "per_minute": True},
             "note": "PROPOSED: the light picture laid on the live layer (screen), dust motes drifting inside `air`, the whole creeping by `travel`; ENGINE-20/SCENES-20 choose the kind"}
            for b in beams
        ] + [{"id": "moth", "type": "birds", "lanes": [[[300, 240], [520, 300]], [[560, 260], [380, 330]]], "every": [20, 50], "group": [1, 1], "size": 3, "speed": 30, "color": "#c8b890",
              "note": "a moth crossing the beams now and then: the flyer kind, small and pale"}],
        "notes": "The beams are light and are not in back.png: beam-round/-tri/-square.png are RGBA light pictures (the beam in the air and its patch on the floor), keyed as frames; lay them on the live layer. The racks are on the right wall. The door the crew came in by is the doorway in the right wall at the right edge (enter). PAINT-20E.",
    }
    return out


def compose(pic, lights):
    comp = pic.copy()
    for kind, (rgb_, a) in lights.items():
        comp = comp * (1 - a[..., None]) + (1 - (1 - comp) * (1 - rgb_)) * a[..., None]
    return comp


def main():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    fast = mode == "fast"
    beams = []
    lights = {}
    for kind, X, Y, s in PORTS:
        rgb_, a, port, patch, air = beam_picture(kind, X, Y, s)
        beams.append({"kind": kind, "port": port, "patch": patch, "air": air, "src": f"beam-{kind}.png"})
        lights[kind] = (rgb_, a)
    Rw, info = render()
    pic_with = paint(Rw, fast)
    if fast:
        to_image(compose(pic_with, lights)).save(f"{WORK}/fast.png")
        to_image(pic_with).save(f"{WORK}/fast-nobeams.png")
        json.dump(layout(info, beams), open(f"{WORK}/layout-fast.json", "w"), indent=1)
        print("fast", round(time.time() - t0, 1), "s")
        return
    Rb, _ = render(include=())
    pic_back = paint(Rb, fast)
    pictures = {"back": (pic_back, None)}
    for name in ("racks", "stairs", "pillar", "tubs", "front"):
        m = Rw.masks.get(name, np.zeros(SHAPE, F32))
        pictures[name] = (pic_with, (m >= 0.5).astype(F32))
    finish_scene(OUT, pictures, colors=160, seed=9)
    for kind, (rgb_, a) in lights.items():
        save_rgba(f"{OUT}/beam-{kind}.png", rgb_, a)
    json.dump(layout(info, beams), open(f"{OUT}/layout.json", "w"), indent=1)
    to_image(compose(pic_with, lights)).save(f"{WORK}/composed.png")
    print("full", round(time.time() - t0, 1), "s:", ", ".join(sorted(pictures)), "+ 3 beams, layout.json")


if __name__ == "__main__":
    main()

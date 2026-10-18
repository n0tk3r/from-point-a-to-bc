"""The things of the Office's lot (OFFICE-17A), each drawn through the scene's one camera (office_lot_kit.CAM) on clear
sheets, as the roadside's things are (nevada_roadside_kit: Paper, Solid): flat colours a face, lit by where the face
turns to the sun, the crisp lines on a second sheet. office_lot.py lays them on the backdrop, or cuts them out.

Every function here takes (d, dl): two Solid drafts (the body, to be brushed; the lines, laid crisply after), placed at
the lot's own origin, so every point is given in the lot's measurements (x, y, z: see office_lot_kit)."""

import math

import numpy as np

from brush import F32, lerp, rgb
from nevada_roadside_kit import Paper, Solid
import office_lot_kit as K
from office_lot_kit import (AWNING, BLD, CAN, DOOR, DUCTS, FAN, FENCE, FLAG, FRONT, GATE, GRILLE, KEYPAD, LEFT, NUTS, PIPE,
                            RIGHT, SCUPPER, SIGN, SWITCH, TOP, UNIT, WINDOW, col, lit)

# ---- the colours of things (before the light)
BEIGE = "#d3c4a6"            # the cinder block, painted
DOOR_C = "#cdb790"           # the steel door, a shade off the wall
STEEL = "#a2a8ae"            # galvanized: the can, the pipe, the ducts
UNIT_C = "#b9bbb5"           # the rooftop unit's casing
DECK = "#a39a8c"             # the roof: gravel on tar
COPE = "#c8cbcc"             # the metal cap along the roof's edge
POLE = "#d9dde2"             # the flagpole, aluminium
LINE = "#2a2632"             # the dark lines round made things
NAVY = "#1d2a52"             # the sign's letters


def drafts(shape, z_ref=0.0):
    """Two clear sheets and their drafts at depth z_ref (so that line widths are right for what is drawn there):
    -> (body sheet, line sheet, d, dl). Points are lot measurements, z relative to z_ref."""
    a, b = Paper(shape), Paper(shape)
    return a, b, Solid(a, (0.0, z_ref), 0.0, cam=K.CAM), Solid(b, (0.0, z_ref), 0.0, cam=K.CAM)


def face(base, f, **kw):
    return lit(base, f, **kw)


def round_thing(d, cx, cz, r, y0, y1, base, n=8, r1=None, alpha=1.0, glint=None):
    """An upright round thing (a pipe, a pole, a post, a can, a shroud) from y0 up to y1, drawn as Solid.tube draws one
    (strips across it, its round foot sagging as we look down on it), but lit by this scene's sun: each strip by how
    squarely the sun meets it, so the light falls a little left of its middle and its right side turns into shade.
    `glint`: a colour for the brightest strip."""
    r1 = r if r1 is None else r1
    (bx, by), (tx, ty) = d.pt(cx, y0, cz), d.pt(cx, y1, cz)
    kb, kt = d.kat(cx, y0, cz), d.kat(cx, y1, cz)
    D = d.cam.Z0 + d.world(cx, y0, cz)[2]
    eb = r * kb * max(0.0, d.cam.eye - d.world(cx, y0, cz)[1]) / D
    et = r1 * kt * max(0.0, d.cam.eye - d.world(cx, y1, cz)[1]) / D
    for i in range(n):
        u0, u1 = -1 + 2 * i / n, -1 + 2 * (i + 1) / n
        um = (u0 + u1) / 2
        f = max(0.0, float(K.TOWARD[0]) * um - float(K.TOWARD[2]) * math.sqrt(max(0.0, 1 - um * um)) * 1.0)
        c = lit(base, f)
        if glint is not None and abs(um + 0.38) < 1.0 / n:
            c = col(glint)
        pts = [(bx + u0 * r * kb, by + math.sqrt(max(0.0, 1 - u0 * u0)) * eb), (bx + u1 * r * kb, by + math.sqrt(max(0.0, 1 - u1 * u1)) * eb),
               (tx + u1 * r1 * kt, ty + math.sqrt(max(0.0, 1 - u1 * u1)) * et), (tx + u0 * r1 * kt, ty + math.sqrt(max(0.0, 1 - u0 * u0)) * et)]
        d.s.poly(pts, c, alpha)


# ---------------------------------------------------------------- shadows on the ground, a wall, the roof
def onto(p, plane):
    """Where the sun throws a point (x, y, z): onto the ground ("ground"), the roof's deck ("roof"), or the building's
    front wall ("wall"). -> the lot place it lands on."""
    x, y, z = p
    D = -K.TOWARD                                                # the way the light goes
    if plane == "ground":
        t = y / -D[1]
    elif plane == "roof":
        t = (y - BLD["deck"]) / -D[1]
    elif plane == "wall":
        t = (BLD["z"][0] - z) / D[2]
    else:
        raise ValueError(plane)
    return (x + D[0] * t, y + D[1] * t, z + D[2] * t)


def shadow_poly(points, plane):
    """A shadow polygon in the picture: the given lot points thrown onto a plane, then seen."""
    return [K.P(*onto(p, plane)) for p in points]


# ---------------------------------------------------------------- the trash can
def can_standing(d, dl, at, lid=True):
    """The steel can upright, its foot's middle at `at` (x, z): ribs round it, a domed lid with a handle, the lid's
    handle chained to the side handle, REGULATION stencilled on its front (lettered by office_lot.py)."""
    cx, cz = at
    r, hb, ht = CAN["r"], CAN["body"], CAN["top"]
    zr = cz - d.wz                                               # (the drafts sit at their own depth)
    round_thing(d, cx, zr, r, 0.0, hb, STEEL, n=12, glint="#f2f4f6")
    # the ribs: three bands round it, a little proud, each lit along its top
    for yb in (14.0, 34.0, 54.0):
        dl.line(d.hring(cx, yb, zr, r + 0.6, a0=200, a1=340, n=10), "#6c727c", 1.6, 0.9)
        dl.line(d.hring(cx, yb + 1.6, zr, r + 0.6, a0=215, a1=280, n=8), "#eef0f2", 0.9, 0.8)
    # the rim, and the lid: a shallow dome, its top lit by the sun
    dl.line(d.hring(cx, hb, zr, r + 0.8, a0=180, a1=360, n=14), "#5c626c", 1.4, 0.95)
    if lid:
        d.hdisc(cx, hb + 0.5, zr, r + 1.6, face(STEEL, TOP * 0.9))
        d.hdisc(cx, hb + 3.6, zr, r * 0.8, face(STEEL, min(1.0, TOP * 1.15)))
        d.hdisc(cx, ht - 1.2, zr, r * 0.42, face("#c4c8cc", 1.0))
        # the lid's handle: a bent strap over the top
        dl.line([(cx - 7, ht - 1, zr), (cx - 6, ht + 2.6, zr), (cx + 6, ht + 2.6, zr), (cx + 7, ht - 1, zr)], "#4a505a", 1.5, 0.95)
        # the chain: from the lid's handle down over the rim to the can's side handle (on the left, in the sun)
        chain = [(cx - 6, ht + 1.5, zr - 2), (cx - 15, hb + 2, zr - 18), (cx - 22, hb - 6, zr - 13), (cx - r - 0.5, hb - 13, zr - 4)]
        dl.line(chain, "#5a5e66", 1.0, 0.95)
        for i in range(len(chain) - 1):                              # its links catch the light
            a, b = chain[i], chain[i + 1]
            m = tuple((a[j] + b[j]) / 2 for j in range(3))
            dl.ball(*m, 0.9, "#e8eaee", 0.9)
    # the side handles
    dl.line([(cx - r - 1.0, hb - 15, zr - 2), (cx - r - 4.0, hb - 13, zr - 2), (cx - r - 1.0, hb - 9, zr - 2)], "#4a505a", 1.6, 0.95)
    dl.line([(cx + r + 1.0, hb - 15, zr - 2), (cx + r + 3.6, hb - 13, zr - 2), (cx + r + 1.0, hb - 9, zr - 2)], "#3e434c", 1.4, 0.9)
    # the dark line round it where it meets the gravel
    dl.line(d.hring(cx, 0.4, zr, r + 0.4, a0=180, a1=360, n=14), "#3a3640", 1.2, 0.7)


def can_tipped(d, dl, at, lid_off=True, turn=34.0):
    """The can on its side on the gravel, where it fell (over to our right): turned `turn` degrees so that its open
    mouth looks toward us and to the right, its foot away to the left; the lid off beside the mouth, still on its chain.
    `at`: the middle of its body on the ground."""
    r, hb = CAN["r"], CAN["body"]
    a_, b_ = Solid(d.s, at, turn, cam=K.CAM), Solid(dl.s, at, turn, cam=K.CAM)      # its own draft: x along it, the mouth at +x
    ca, sa = math.cos(math.radians(turn)), math.sin(math.radians(turn))
    x0, x1 = -hb / 2, hb / 2

    def world_n(nx, ny, nz):                                                     # a normal in the can's draft -> in the lot
        return (nx * ca + nz * sa, ny, -nx * sa + nz * ca)
    # the round side, from the far top round to where it rests: far bands first
    ts = np.linspace(2 * math.pi + 0.7, math.pi, 13)
    for t0, t1 in zip(ts[:-1], ts[1:]):
        tm = (t0 + t1) / 2
        f = K.lambert(world_n(0.0, math.cos(tm), math.sin(tm)))
        q = [(x0, r + r * math.cos(t0), r * math.sin(t0)), (x1, r + r * math.cos(t0), r * math.sin(t0)),
             (x1, r + r * math.cos(t1), r * math.sin(t1)), (x0, r + r * math.cos(t1), r * math.sin(t1))]
        a_.poly(q, face(STEEL, f))
    for xb in (x0 + 14.0, x0 + 34.0, x0 + 54.0):                                # the ribs round its girth
        b_.line([(xb, r + r * math.cos(t), r * math.sin(t)) for t in np.linspace(math.pi, 2 * math.pi + 0.6, 9)], "#6c727c", 1.4, 0.85)
    # the open mouth (the +x end, toward us): dark inside, its rim lit
    mouth = [(x1, r + r * math.cos(t), r * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 20, endpoint=False)]
    a_.poly(mouth, face(STEEL, 0.25))
    a_.poly([(x1 + 0.2, r + (r - 2.2) * math.cos(t), (r - 2.2) * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 20, endpoint=False)], "#2c2a32")
    b_.line(mouth + [mouth[0]], "#dfe2e6", 1.1, 0.9)
    if lid_off:
        # the lid on the gravel past the mouth, and its chain back to where the handle was
        lx, lz = x1 + 30.0, -12.0
        a_.hdisc(lx, 1.2, lz, r + 1.6, face(STEEL, TOP))
        a_.hdisc(lx, 3.6, lz, r * 0.8, face(STEEL, min(1.0, TOP * 1.2)))
        b_.line([(lx - 6, 6.2, lz), (lx + 6, 6.2, lz)], "#4a505a", 1.5, 0.95)
        b_.line([(lx - 8, 5.0, lz - 4), (x1 + 6, 2.0, -r * 0.9), (x1 - 6, r * 0.5, -r * 0.98)], "#5a5e66", 1.0, 0.95)
    b_.line([(x0, 0.4, -r * 0.2), (x1, 0.4, -r * 0.2)], "#3a3640", 1.2, 0.6)    # where it rests on the gravel


# ---------------------------------------------------------------- the flagpole
def flagpole(d, dl):
    """The pole, aluminium, tapering, on a round concrete foot; a ball on top; its rope down the sunny side to a cleat."""
    x, z, h, r = FLAG["x"], FLAG["z"] - d.wz, FLAG["h"], FLAG["r"]
    round_thing(d, x, z, 26.0, 0.0, 9.0, "#b8b0a4", n=10)                       # the concrete foot
    d.hdisc(x, 9.0, z, 26.0, face("#b8b0a4", TOP))                               # its top in the sun
    round_thing(d, x, z, r, 9.0, h, POLE, n=6, r1=r * 0.55, glint="#ffffff")
    d.ball(x, h + 4.0, z, 5.5, face("#e8d6a0", 0.9))                             # the ball
    dl.ball(x - 1.6, h + 5.6, z, 1.8, "#fff8e8", 0.95)
    dl.line([(x - 1.6, h - 2.0, z - 2.0), (x - 1.8, 130.0, z - 2.0)], "#efe8dc", 0.7, 0.85)      # the rope
    dl.line([(x - 4.2, 118.0, z - 1.0), (x + 0.0, 118.0, z - 3.0)], "#6a6e78", 1.6, 0.9)         # the cleat


def pennant_points(phase, h=None):
    """The pennant's outline, flying to the right from the top of the pole, stirring: phase 0..1 rolls a gentle wave
    along it. -> (top edge, bottom edge) as lot points (x, y, z), hoist to tip."""
    x, z = FLAG["x"], FLAG["z"]
    top = (h or FLAG["h"]) - 4.0
    L, hoist = FLAG["pennant"], 40.0
    n = 9
    up, dn = [], []
    for i in range(n + 1):
        u = i / n
        wave = math.sin(2 * math.pi * (u * 1.1 - phase)) * 5.5 * u ** 0.8
        droop = 7.0 * u * u
        half = hoist / 2 * (1 - u) + 1.0 * u
        cy = top - hoist / 2 - droop + wave
        cz = z + math.sin(2 * math.pi * (u * 0.9 - phase) + 1.0) * 6.0 * u
        up.append((x + 2.0 + u * L, cy + half, cz))
        dn.append((x + 2.0 + u * L, cy - half, cz))
    return up, dn


def pennant(d, dl, phase):
    """O.O.P.S. in white on gray, on a triangular pennant at the top of the pole (lettered by office_lot.py)."""
    up, dn = pennant_points(phase)
    zr = lambda pts: [(p[0], p[1], p[2] - d.wz) for p in pts]
    up, dn = zr(up), zr(dn)
    outline = up + list(reversed(dn))
    d.poly(outline, face("#8b909c", FRONT))
    # the folds: the far side of each wave in shade
    for i in range(len(up) - 1):
        s = math.sin(2 * math.pi * ((i + 0.5) / (len(up) - 1) * 1.1 - phase))
        if s < -0.15:
            d.poly([up[i], up[i + 1], dn[i + 1], dn[i]], face("#8b909c", FRONT * 0.45), 0.85)
        elif s > 0.55:
            d.poly([up[i], up[i + 1], dn[i + 1], dn[i]], face("#a4a9b4", min(1.0, FRONT * 1.3)), 0.8)
    dl.line([up[0], dn[0]], "#5a5e68", 1.2, 0.9)                                 # the hoist, its tape
    return outline


# ---------------------------------------------------------------- the awning, the door
def awning(d, dl):
    """A small flat awning over the door: a sheet-metal slab, its top seen from above (we are higher than it), its
    front edge lit. It is held from inside the wall (no rods: rods up to the wall would run into the sign, and at this
    size they break into specks when the cut-out is cut hard)."""
    x0, x1 = AWNING["x"]
    y0, y1 = AWNING["y"]
    zw, zo = BLD["z"][0] - d.wz, BLD["z"][0] - AWNING["out"] - d.wz
    d.poly([(x0, y1, zo), (x1, y1, zo), (x1, y1, zw), (x0, y1, zw)], face("#c9c6bd", TOP))          # its top, in the sun
    d.poly([(x0, y0, zo), (x1, y0, zo), (x1, y1, zo), (x0, y1, zo)], face("#c9c6bd", FRONT))        # its front edge
    dl.line([(x0, y1, zo), (x1, y1, zo)], "#fbf6ea", 1.6, 0.95)
    dl.line([(x0, y0, zo), (x1, y0, zo)], "#4a4650", 1.6, 0.8)


def door_shut(d, dl):
    """The steel door, shut: beige, a shade off the wall, in its frame; a lever handle on the right (the hinges on
    the left), a kick plate, a small plate with its words too small to read."""
    x0, x1 = DOOR["x"]
    h, j = DOOR["h"], DOOR["jamb"]
    z = BLD["z"][0] - 0.6 - d.wz
    d.poly([(x0, 0, z), (x1, 0, z), (x1, h, z), (x0, h, z)], face(DOOR_C, FRONT))
    d.poly([(x0 + 3, 2, z - 0.1), (x1 - 3, 2, z - 0.1), (x1 - 3, 26, z - 0.1), (x0 + 3, 26, z - 0.1)], face("#b9b4aa", FRONT * 1.05))   # kick plate
    dl.line([(x0 + 3, 26, z - 0.2), (x1 - 3, 26, z - 0.2)], "#8a8478", 0.8, 0.8)
    # the lever handle, on the right
    hx = x1 - 12.0
    dl.line([(hx, 104, z - 3.0), (hx - 13, 104, z - 3.0)], "#4c4a52", 2.2, 0.95)
    dl.line([(hx, 105, z - 3.4), (hx - 12, 105, z - 3.4)], "#eef0f2", 0.8, 0.9)
    dl.ball(hx, 104, z - 1.5, 2.6, "#7a7880", 0.95)
    # the hinges, on the left
    for yh in (30.0, 105.0, 180.0):
        dl.line([(x0 + 1.0, yh, z - 0.5), (x0 + 1.0, yh + 10.0, z - 0.5)], "#6c6870", 1.4, 0.9)
    # a small plate at eye height (its words too small to read)
    d.poly([(x0 + 30, 148, z - 0.2), (x1 - 30, 148, z - 0.2), (x1 - 30, 160, z - 0.2), (x0 + 30, 160, z - 0.2)], face("#e8e4d8", FRONT))
    for yl in (151.5, 155.5):
        dl.line([(x0 + 34, yl, z - 0.3), (x1 - 34, yl, z - 0.3)], "#3a3f5a", 0.7, 0.7)
    # the crack round it, dark
    dl.line([(x0, 0, z), (x0, h, z), (x1, h, z), (x1, 0, z)], LINE, 1.0, 0.85)


def door_open(d, dl):
    """The door swung in (it opens inward, its hinges on the left): the leaf seen edge on against the left of the
    opening, and the hall inside lit by tubes: beige walls, gray floor tiles, a mat that says (again) WIPE."""
    x0, x1 = DOOR["x"]
    h = DOOR["h"]
    zw = BLD["z"][0] - d.wz
    # the inside: the floor going back, the far wall, the right wall (lit by the tubes, a cool greenish white)
    depth = 260.0
    d.poly([(x0, 0, zw), (x1, 0, zw), (x1, 0, zw + depth), (x0, 0, zw + depth)], "#8e9088")                     # the floor
    d.poly([(x0, 0, zw + depth), (x1, 0, zw + depth), (x1, h, zw + depth), (x0, h, zw + depth)], "#c8c2a6")     # the far wall
    d.poly([(x1, 0, zw), (x1, 0, zw + depth), (x1, h, zw + depth), (x1, h, zw)], "#b4ae94")                     # the right wall
    d.poly([(x0, h, zw), (x1, h, zw), (x1, h, zw + depth), (x0, h, zw + depth)], "#e6e8dc")                     # the ceiling (a tube's glow)
    for zz in (60.0, 120.0, 180.0, 240.0):                                                                       # the floor's tiles
        dl.line([(x0, 0.2, zw + zz), (x1, 0.2, zw + zz)], "#7a7c76", 0.7, 0.6)
    dl.line([(x0 + 50, 0.2, zw), (x0 + 50, 0.2, zw + depth)], "#7a7c76", 0.7, 0.5)
    d.poly([(x0 + 24, 0.4, zw + 30), (x1 - 24, 0.4, zw + 30), (x1 - 24, 0.4, zw + 80), (x0 + 24, 0.4, zw + 80)], "#5c5650")   # a mat inside
    # a door at the end of the hall (the elevator's: plain, two leaves)
    d.poly([(x0 + 20, 0, zw + depth - 0.5), (x1 - 20, 0, zw + depth - 0.5), (x1 - 20, 190, zw + depth - 0.5), (x0 + 20, 190, zw + depth - 0.5)], "#a8aaa4")
    dl.line([((x0 + x1) / 2, 0, zw + depth - 1), ((x0 + x1) / 2, 190, zw + depth - 1)], "#6a6c68", 0.8, 0.8)
    # the leaf, swung in against the left of the opening: we see its edge and a sliver of its inner face
    sw = math.radians(78.0)
    ex, ez = x0 + (x1 - x0) * math.cos(sw), zw + (x1 - x0) * math.sin(sw)
    d.poly([(x0, 0, zw), (ex, 0, ez), (ex, h, ez), (x0, h, zw)], face(DOOR_C, 0.35))
    dl.line([(ex, 0, ez), (ex, h, ez)], "#fff4dc", 1.0, 0.8)
    dl.line([(x0, 0, zw), (x0, h, zw), (x1, h, zw), (x1, 0, zw)], LINE, 1.0, 0.7)


# ---------------------------------------------------------------- the grille, its wing nuts, the switch
def grille(d, dl):
    """The intake grille on the unit's side toward us: a big louvred panel in a frame, the louvres slanting down (we
    see their lit tops and, between them, slits of dark where the fan is). Its four wing nuts are cut-outs of their own."""
    x0, x1 = GRILLE["x"]
    y0, y1 = GRILLE["y"]
    z = UNIT["z"][0] - GRILLE["proud"] - d.wz
    frame_c = face("#7c8084", FRONT)
    d.poly([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], frame_c)
    b = 6.0
    n = 11
    for i in range(n):                                                          # the louvres
        ya = y0 + b + (y1 - y0 - 2 * b) * i / n
        yb = ya + (y1 - y0 - 2 * b) / n
        d.poly([(x0 + b, ya, z - 0.2), (x1 - b, ya, z - 0.2), (x1 - b, yb, z - 0.2), (x0 + b, yb, z - 0.2)], face("#9a9d9c", FRONT * 0.75))
        d.poly([(x0 + b, yb - 2.6, z - 0.4), (x1 - b, yb - 2.6, z - 0.4), (x1 - b, yb, z - 0.4), (x0 + b, yb, z - 0.4)], face("#c4c7c6", min(1.0, TOP * 1.1)))
        dl.line([(x0 + b, ya + 1.0, z - 0.6), (x1 - b, ya + 1.0, z - 0.6)], "#34363c", 1.2, 0.95)          # the slit under each
    dl.line([(x0, y0, z - 0.8), (x1, y0, z - 0.8), (x1, y1, z - 0.8), (x0, y1, z - 0.8), (x0, y0, z - 0.8)], "#3c3e44", 1.0, 0.9)
    dl.line([(x0 + 1, y1 - 1, z - 1.0), (x1 - 1, y1 - 1, z - 1.0)], "#eef0ee", 0.9, 0.8)
    for (nx, ny) in NUTS:                                                       # the studs the wing nuts go on
        dl.ball(nx, ny, z - 1.2, 1.6, "#5a5c62", 0.95)


def grille_off(d, dl):
    """The grille taken off and leaned against the unit to the left of its opening, its foot on the roof, the four wing
    nuts set out on the roof beside it in a neat row (he is tidy)."""
    w, h = GRILLE["x"][1] - GRILLE["x"][0], GRILLE["y"][1] - GRILLE["y"][0]
    xr = GRILLE["x"][0] - 14.0                                                  # its right edge, a hand left of the opening
    zt = UNIT["z"][0] - 2.0 - d.wz                                              # its top rests on the unit's face
    zb = UNIT["z"][0] - 30.0 - d.wz                                             # its foot on the roof, 30 cm out
    yb = BLD["deck"]
    yt = yb + math.sqrt(max(1.0, h * h - 28.0 ** 2))
    q = [(xr - w, yb, zb), (xr, yb, zb), (xr, yt, zt), (xr - w, yt, zt)]
    d.poly(q, face("#a6a9a8", 0.75))
    b, n = 6.0, 11
    for i in range(n):
        ta, tb = (b + (h - 2 * b) * i / n) / h, (b + (h - 2 * b) * (i + 1) / n) / h
        def at(xx, t):
            return (xx, yb + (yt - yb) * t, zb + (zt - zb) * t)
        d.poly([at(xr - w + b, ta), at(xr - b, ta), at(xr - b, tb), at(xr - w + b, tb)], face("#9a9d9c", 0.6))
        d.poly([at(xr - w + b, tb - 2.6 / h), at(xr - b, tb - 2.6 / h), at(xr - b, tb), at(xr - w + b, tb)], face("#c4c7c6", 0.9))
        dl.line([at(xr - w + b, ta + 1.0 / h), at(xr - b, ta + 1.0 / h)], "#34363c", 1.2, 0.9)
    dl.line(q + [q[0]], "#3c3e44", 1.0, 0.9)
    # OFFICE-17A: the four wing nuts in a row on the roof in front of the grille's foot (he is tidy), out of the way of
    # the intake, where whoever looks at the grille sees them
    for i in range(4):
        wing_nut(d, dl, (xr - w / 2 - 48.0 + i * 32.0, yb, UNIT["z"][0] - 44.0 - d.wz), flat=True)


# A wing nut's two wings, seen from the front (the right one; the left is its mirror), in cm from the middle of the boss:
# each flares up and out to a broad rounded tip. The outline is the same shape a little bigger, laid dark under it.
WING = [(2.0, 1.5), (6.5, 3.0), (11.0, 6.5), (12.5, 10.5), (10.5, 12.5), (7.0, 10.0), (2.5, 5.5)]
WING_LINE = [(1.0, -0.2), (7.4, 1.4), (12.8, 5.6), (14.4, 11.0), (11.0, 14.4), (6.0, 11.8), (0.8, 6.6)]


def wing_nut(d, dl, at, flat=False):
    """A wing nut, drawn big enough to read as one at this distance (a cartoon's wing nut: 26 cm from wing tip to wing
    tip, some 12 px): a round boss and two broad wings flaring up and out, outlined dark, the sun on the left wing.
    Solid shapes only, never hairlines, so that it keeps its shape when its cut-out is cut hard. On its stud (upright,
    facing us), or set down on the roof (`flat`: `at` is then the roof under it; set down on its face, a wing nut's
    wings stand up, so from here it is the same shape, its boss on the roof; the roof itself is seen so nearly edge on
    that anything lying flat on it would be lost)."""
    x, y, z = at
    if flat:
        y = y + 5.6
    mirror = lambda pts, s: [(x + s * px, y + py, z - 0.3) for px, py in pts]
    for s in (-1.0, 1.0):                                                          # the outline, dark, a little bigger
        d.poly(mirror(WING_LINE, s), "#2c2e36")
    d.disc(x, y, 5.6, "#2c2e36", z=z - 0.2)
    d.poly(mirror(WING, -1.0), face("#e4e6ea", min(1.0, FRONT * 1.35)))              # the left wing, toward the sun
    d.poly(mirror(WING, 1.0), face("#cfd2d6", FRONT * 0.7))                          # the right wing, turned from it
    d.disc(x, y, 4.2, face("#c4c8cc", FRONT), z=z - 0.4)                             # the boss
    d.disc(x, y, 1.9, "#2e3036", z=z - 0.5)                                          # the stud's end
    d.disc(x - 7.4, y + 7.0, 1.7, "#ffffff", z=z - 0.6)                              # a glint on the left wing


def switch_lever(d, dl, on=True):
    """The maintenance switch's lever, on the left side of its gray box (the box is the backdrop's): its handle up
    (on) or pulled down (off). The handle is where Ranger's hands are in his pull frames (office_lot_kit.SWITCH)."""
    px_, py_ = SWITCH["pivot"]
    hx, hy = SWITCH["up"] if on else SWITCH["down"]
    z = UNIT["z"][0] - SWITCH["proud"] - 1.0 - d.wz
    d.poly([(px_ - 2.4, py_ - 3.0, z + 0.5), (px_ + 1.0, py_ - 3.0, z + 0.5), (px_ + 1.0, py_ + 3.0, z + 0.5), (px_ - 2.4, py_ + 3.0, z + 0.5)], face("#5c5e64", FRONT))
    dl.line([(px_ - 1.0, py_, z), (hx, hy, z)], "#2e3036", 2.6, 0.98)                       # the lever
    dl.line([(px_ - 1.0, py_ + 0.6, z - 0.2), (hx + 0.4, hy + 0.6, z - 0.2)], "#9ea2aa", 1.0, 0.9)
    dl.line([(hx + (hx - px_) * 0.12, hy + (hy - py_) * 0.12, z - 0.5), (hx - (hx - px_) * 0.10, hy - (hy - py_) * 0.10, z - 0.5)], "#c83a2e", 4.4, 0.98)   # its red grip
    dl.line([(hx + (hx - px_) * 0.08, hy + (hy - py_) * 0.08 + 1.0, z - 0.8), (hx - (hx - px_) * 0.06, hy - (hy - py_) * 0.06 + 1.0, z - 0.8)], "#f08070", 1.0, 0.9)


# ---------------------------------------------------------------- the fence and its gate
def fence_post(d, dl, x, z, h=FENCE["h"], r=3.4, cap=True):
    zr = z - d.wz
    round_thing(d, x, zr, r, 0.0, h, STEEL, n=4)
    if cap:
        d.ball(x, h + 1.0, zr, r * 1.2, face(STEEL, TOP))


def gate_leaf_points():
    """The open leaf's four corners (lot points: hinge foot, free foot, free top, hinge top), and its unit vector."""
    hx = GATE["x"][1]
    w = GATE["x"][1] - GATE["x"][0]
    a = math.radians(GATE["swing"])
    fx, fz = hx - w * math.cos(a), FENCE["z"] - w * math.sin(a)
    h = FENCE["h"] - 8.0
    return [(hx, 4.0, FENCE["z"]), (fx, 4.0, fz), (fx, h, fz), (hx, h, FENCE["z"])], ((fx - hx) / w, (fz - FENCE["z"]) / w)


# ---------------------------------------------------------------- the rooftop unit
def unit_body(d, dl):
    """The rooftop unit, as the backdrop has it: the curb, the casing's face toward us in panels, the louvred coil
    panels, the intake opening (dark, the fan still inside it), the switch box and its sticker, the ducts out of its
    left end down into the roof, the fan housings standing up off its top. (The grille, the wing nuts, the lever and
    the turning fan are cut-outs and frames of their own.)"""
    x0, x1 = UNIT["x"]
    z0 = UNIT["z"][0] - d.wz
    yc, yt = UNIT["curb"], UNIT["top"]
    yd = BLD["deck"]
    casing = face(UNIT_C, FRONT)
    d.poly([(x0 - 4, yd, z0 + 2), (x1 + 4, yd, z0 + 2), (x1 + 4, yc, z0 + 2), (x0 - 4, yc, z0 + 2)], face("#8e8a84", FRONT * 0.8))    # the curb
    d.poly([(x0, yc, z0), (x1, yc, z0), (x1, yt, z0), (x0, yt, z0)], casing)
    # the coil panels left of the grille: two louvred panels side by side, the coil's dark between their slats
    left_end = GRILLE["x"][0] - 24.0
    mid = (x0 + 16.0 + left_end) / 2
    for (a, b) in ((x0 + 16.0, mid - 5.0), (mid + 5.0, left_end)):
        d.poly([(a, yc + 22, z0 - 0.2), (b, yc + 22, z0 - 0.2), (b, yt - 30, z0 - 0.2), (a, yt - 30, z0 - 0.2)], face("#7e8284", FRONT * 0.9))
        yy = yc + 25.0
        while yy < yt - 32:
            d.poly([(a + 2, yy + 1.4, z0 - 0.3), (b - 2, yy + 1.4, z0 - 0.3), (b - 2, yy + 5.0, z0 - 0.3), (a + 2, yy + 5.0, z0 - 0.3)], face("#b2b5b2", min(1.0, FRONT * 1.2)))
            dl.line([(a + 2, yy + 5.0, z0 - 0.4), (b - 2, yy + 5.0, z0 - 0.4)], "#e8eae6", 0.7, 0.55)
            yy += 6.5
        dl.line([(a, yc + 22, z0 - 0.5), (b, yc + 22, z0 - 0.5), (b, yt - 30, z0 - 0.5), (a, yt - 30, z0 - 0.5), (a, yc + 22, z0 - 0.5)], "#4e5256", 1.0, 0.9)
    # an access panel at the right end: two handles, a blank plate (no name on it: nobody's make)
    ax0, ax1 = SWITCH["box"][1] + 6.0, x1 - 5.0
    if ax1 - ax0 > 14:
        dl.line([(ax0, yc + 14, z0 - 0.5), (ax1, yc + 14, z0 - 0.5), (ax1, yt - 14, z0 - 0.5), (ax0, yt - 14, z0 - 0.5), (ax0, yc + 14, z0 - 0.5)], "#6a6e72", 0.9, 0.85)
        for yh in (yc + 50.0, yt - 50.0):
            dl.line([((ax0 + ax1) / 2 - 4, yh, z0 - 1.5), ((ax0 + ax1) / 2 + 4, yh, z0 - 1.5)], "#3c3e44", 1.6, 0.95)
        d.poly([(ax0 + 3, yt - 40, z0 - 0.6), (ax1 - 3, yt - 40, z0 - 0.6), (ax1 - 3, yt - 30, z0 - 0.6), (ax0 + 3, yt - 30, z0 - 0.6)], face("#d8dad4", FRONT))
    # the intake opening behind the grille: dark inside, the fan still in it (the turning fan is a frame over this)
    gx0, gx1 = GRILLE["x"]
    gy0, gy1 = GRILLE["y"]
    d.poly([(gx0 + 3, gy0 + 3, z0 - 0.3), (gx1 - 3, gy0 + 3, z0 - 0.3), (gx1 - 3, gy1 - 3, z0 - 0.3), (gx0 + 3, gy1 - 3, z0 - 0.3)], "#26252c")
    fan(d, dl, 0.0, still=True)
    dl.line([(gx0 + 3, gy0 + 3, z0 - 0.4), (gx1 - 3, gy0 + 3, z0 - 0.4), (gx1 - 3, gy1 - 3, z0 - 0.4), (gx0 + 3, gy1 - 3, z0 - 0.4), (gx0 + 3, gy0 + 3, z0 - 0.4)], "#5e6064", 1.2, 0.9)
    # the panels' seams and screws, the casing's top lip and its foot
    for xs in (x0 + 8.0, gx0 - 14.0, gx1 + 10.0, SWITCH["box"][1] + 4.0, x1 - 6.0):
        dl.line([(xs, yc + 4, z0 - 0.5), (xs, yt - 4, z0 - 0.5)], "#7c8082", 0.9, 0.8)
    dl.line([(x0, yt - 2, z0 - 0.6), (x1, yt - 2, z0 - 0.6)], "#eef0ec", 1.2, 0.85)
    dl.line([(x0, yt - 7, z0 - 0.6), (x1, yt - 7, z0 - 0.6)], "#7c8082", 0.9, 0.8)
    dl.line([(x0, yc + 2, z0 - 0.6), (x1, yc + 2, z0 - 0.6)], "#5c5e62", 1.0, 0.8)
    for xs in np.arange(x0 + 20.0, x1 - 10.0, 34.0):
        dl.ball(xs, yt - 4.5, z0 - 0.7, 0.9, "#6a6e72", 0.8)
    # the fan housings standing up off its top: round shrouds with their guards (we are lower than its top: their fronts
    # show against the sky)
    for (fx, fr) in ((x0 + 120.0, 56.0), (x0 + 290.0, 56.0)):
        zc = z0 + 120.0
        round_thing(d, fx, zc, fr, yt, yt + 26, UNIT_C, n=10)
        for j in range(1, 10):
            t = -1 + 2 * j / 10
            dl.line([(fx + t * fr, yt + 26, zc - fr * math.sqrt(1 - t * t)), (fx + t * fr * 0.9, yt + 31, zc - fr * 0.9 * math.sqrt(max(0.0, 1 - t * t)))],
                    "#6e7276", 0.7, 0.7)
        dl.line([(fx - fr, yt + 26, zc), (fx + fr, yt + 26, zc)], "#eceee8", 0.9, 0.7)
    # the switch box (the lever is a cut-out): gray, on the unit's face, a sticker on its front
    bx0, bx1, by0, by1 = SWITCH["box"]
    zb = z0 - SWITCH["proud"]
    d.poly([(bx0, by0, zb), (bx1, by0, zb), (bx1, by1, zb), (bx0, by1, zb)], face("#8e9196", FRONT))
    d.poly([(bx0, by1, zb), (bx1, by1, zb), (bx1, by1, z0), (bx0, by1, z0)], face("#8e9196", TOP))          # its top
    d.poly([(bx0, by0, zb), (bx0, by0, z0), (bx0, by1, z0), (bx0, by1, zb)], face("#8e9196", LEFT))         # its left side, where the lever is
    dl.line([(bx0, by0, zb - 0.1), (bx1, by0, zb - 0.1), (bx1, by1, zb - 0.1), (bx0, by1, zb - 0.1), (bx0, by0, zb - 0.1)], "#3e4046", 0.9, 0.9)
    # the sticker: white, a fan with a line through it, TURN OFF BEFORE SERVICING. THIS MEANS YOU, WENDELL. (too
    # small to read here: its words are in the look; the picture of the fan is what Ranger reads)
    sx0, sx1, sy0, sy1 = bx0 + 3.0, bx1 - 3.0, by0 + 3.0, by1 - 3.0
    d.poly([(sx0, sy0, zb - 0.2), (sx1, sy0, zb - 0.2), (sx1, sy1, zb - 0.2), (sx0, sy1, zb - 0.2)], "#f2f0e8")
    cx_, cy_ = (sx0 + sx1) / 2, sy1 - 10.5
    for a in (90.0, 210.0, 330.0):                                              # the fan: three blades
        t = math.radians(a)
        dl.line([(cx_, cy_, zb - 0.3), (cx_ + math.cos(t) * 6.2, cy_ + math.sin(t) * 6.2, zb - 0.3)], "#2a2a34", 2.0, 0.95)
    dl.line([(cx_ - 7.0, cy_ - 7.0, zb - 0.4), (cx_ + 7.0, cy_ + 7.0, zb - 0.4)], "#d23a2c", 1.6, 0.98)   # the line through it
    dl.line([(cx_ - 7.8, cy_, zb - 0.35)] + [(cx_ + 7.8 * math.cos(t), cy_ + 7.8 * math.sin(t), zb - 0.35) for t in np.linspace(math.pi, -math.pi, 17)], "#d23a2c", 1.2, 0.95)
    for yl in (sy0 + 3.0, sy0 + 6.0, sy0 + 9.0):                               # the words, as lines
        dl.line([(sx0 + 2.5, yl, zb - 0.3), (sx1 - 2.5, yl, zb - 0.3)], "#3a3a48", 0.8, 0.75)
    # the ducts: out of its left end, and bent down into the roof through their curbs (the far one first)
    for dct in reversed(DUCTS):
        ax0, ax1 = dct["x"]
        ay0, ay1 = dct["y"]
        az0, az1 = dct["z"][0] - d.wz, dct["z"][1] - d.wz
        hh = 40.0                                                                # the run's depth
        d.poly([(ax0 - 4, ay0, az0 - 4), (ax1 - 10, ay0, az0 - 4), (ax1 - 10, ay0 + 12, az0 - 4), (ax0 - 4, ay0 + 12, az0 - 4)], face("#8e8a84", FRONT))   # the curb
        d.poly([(ax0 - 4, ay0 + 12, az0 - 4), (ax1 - 10, ay0 + 12, az0 - 4), (ax1 - 10, ay0 + 12, az1 + 4), (ax0 - 4, ay0 + 12, az1 + 4)], face("#8e8a84", TOP))
        d.poly([(ax0, ay0 + 12, az0), (ax1 - 14, ay0 + 12, az0), (ax1 - 14, ay1, az0), (ax0, ay1, az0)], face(STEEL, FRONT))              # down into the roof
        d.poly([(ax0, ay1 - hh, az0), (x0, ay1 - hh, az0), (x0, ay1, az0), (ax0, ay1, az0)], face(STEEL, FRONT * 1.05))                    # out of the unit
        d.poly([(ax0, ay1, az0), (x0, ay1, az0), (x0, ay1, az1), (ax0, ay1, az1)], face(STEEL, TOP))                                        # its top
        dl.line([(ax0, ay1, az0), (x0, ay1, az0)], "#f6f8f6", 1.0, 0.85)
        dl.line([(ax0 + 0.5, ay0 + 12, az0), (ax0 + 0.5, ay1, az0)], "#f0f2f0", 0.8, 0.7)
        for yy in (ay0 + 30.0, ay0 + 52.0):
            if yy < ay1 - hh:
                dl.line([(ax0, yy, az0 - 0.2), (ax1 - 14, yy, az0 - 0.2)], "#6c7072", 0.8, 0.8)                                       # its seams
        dl.line([(ax0 + 22, ay1 - hh, az0 - 0.2), (ax0 + 22, ay1, az0 - 0.2)], "#6c7072", 0.8, 0.8)
        dl.line([(ax1 - 14, ay0 + 12, az0), (ax1 - 14, ay1 - hh, az0)], "#4c5054", 0.9, 0.8)


def fan(d, dl, angle, still=False, blur_amount=0.0):
    """The big fan behind the grille: a hub and three broad blades, at `angle` degrees. (In the backdrop it is still;
    its turning frames are painted by office_lot.py with the same drawing.)"""
    cx, cy = FAN["x"], FAN["y"]
    r = FAN["r"]
    z = UNIT["z"][0] + 18.0 - d.wz
    d.disc(cx, cy, r + 2.0, "#34333a", z=z + 2.0)                               # the ring it turns in
    for k in range(3):
        a = math.radians(angle + k * 120.0)
        ca, sa = math.cos(a), math.sin(a)
        ta = a + math.radians(26.0)
        blade = [(cx + ca * 7.0, cy + sa * 7.0, z), (cx + math.cos(a - 0.36) * r * 0.94, cy + math.sin(a - 0.36) * r * 0.94, z),
                 (cx + math.cos(a + 0.05) * r, cy + math.sin(a + 0.05) * r, z), (cx + math.cos(ta) * r * 0.86, cy + math.sin(ta) * r * 0.86, z),
                 (cx + math.cos(ta + 0.2) * 8.0, cy + math.sin(ta + 0.2) * 8.0, z)]
        d.poly(blade, "#8a8e94" if still else "#7c8086")
        dl.line([blade[1], blade[2], blade[3]], "#c8ccd0", 0.9, 0.7)
    d.disc(cx, cy, 8.0, "#5a5c62", z=z - 0.5)
    dl.ball(cx - 1.5, cy + 1.5, z - 1.0, 2.0, "#a8acb2", 0.9)

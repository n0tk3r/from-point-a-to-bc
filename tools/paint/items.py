"""The pictures of the things a player can carry: one small still-life each, 64 x 64 on a clear ground.

Each is a few bold shapes in three or four tones, lit from the upper left, brushed lightly, with its
small crisp marks put on afterwards and a darker edge all down its shadow side.

    python3 items.py            paints them all into out/items/ and makes out/items-sheet.png
    python3 items.py coin map   paints only those (and the sheet)"""

import math
import os
import sys

import numpy as np
from PIL import Image

from brush import *
from solid import mix

S = 64


def rot(points, deg, c=(32.0, 32.0)):
    """Turn points about a middle (degrees, clockwise as we look at the picture)."""
    ca, sa = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in points]


def loop(points, steps=6):
    """A closed smooth outline through the points."""
    pts = [tuple(p) for p in points]
    return curve(pts[-1:] + pts + pts[:2], steps)[steps:steps + len(pts) * steps]


def oval(cx, cy, rx, ry, deg=0.0, n=28):
    return rot([(cx + math.cos(i / n * 2 * math.pi) * rx, cy + math.sin(i / n * 2 * math.pi) * ry) for i in range(n)], deg, (cx, cy))


def rrect(cx, cy, hw, hh, r, deg=0.0, n=6):
    """A rectangle with rounded corners, as a polygon, turned about its middle."""
    pts = []
    for (sx, sy, a0) in ((1, -1, -90), (1, 1, 0), (-1, 1, 90), (-1, -1, 180)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + sx * (hw - r) + math.cos(a) * r, cy + sy * (hh - r) + math.sin(a) * r))
    return rot(pts, deg, (cx, cy))


# ---------------------------------------------------------------- the things
def reed(b, l):
    """A cut reed: a green stalk, two long leaves, a feathery brown head."""
    green = ("#3a5a24", "#6f9638", "#b4cc62")
    stalk = curve([(9, 60), (19, 46), (29, 32.5), (38, 21)], 8)
    for (pts, w0, w1) in ((curve([(18, 47.5), (31, 50), (44, 46), (57, 50)], 6), 5.6, 1.0), (curve([(27, 35.5), (19.5, 26), (15.5, 15), (18, 6)], 6), 5.0, 1.0)):
        b.taper(pts, green[0], w0, w1)                       # a leaf: dark, then its lit face
        b.taper([(x - 0.5, y - 0.8) for x, y in pts], green[1], w0 * 0.62, w1 * 0.6)
        l.taper([(x - 0.4, y - 1.0) for x, y in pts[1:-2]], green[2], 0.9, 0.6)
    b.taper(stalk, green[0], 6.6, 4.4)
    b.taper([(x - 0.8, y - 0.7) for x, y in stalk], green[1], 4.8, 3.2)
    l.taper([(x - 1.6, y - 1.4) for x, y in stalk], green[2], 1.5, 1.0)
    for t in (9, 17):                                        # the joints of the stalk
        (x, y), (x2, y2) = stalk[t], stalk[t + 1]
        nx, ny = -(y2 - y), (x2 - x)
        n = math.hypot(nx, ny)
        l.line([(x - nx / n * 3.1, y - ny / n * 3.1), (x + nx / n * 3.1, y + ny / n * 3.1)], green[0], 1.3, 0.9)
    head = ("#6a4020", "#a8743a", "#e2bc7c")
    for k, a in enumerate(np.linspace(0.0, 1.0, 11)):        # the plume: a fan of soft brown strokes
        ang = -0.92 + (a - 0.5) * 1.25
        length = 23 - abs(a - 0.5) * 13
        tip = (38 + math.cos(ang) * length, 21 + math.sin(ang) * length)
        mid = (38 + math.cos(ang) * length * 0.5 + 1.2, 21 + math.sin(ang) * length * 0.5 - 0.4)
        b.taper(curve([(38, 21), mid, tip], 4), head[0] if k % 3 == 2 else head[1], 4.4, 1.2)
    for a in (-1.3, -1.0, -0.72, -0.45):
        l.line([(39.5 + math.cos(a) * 5, 19.5 + math.sin(a) * 5), (38.5 + math.cos(a) * 18, 20 + math.sin(a) * 18)], head[2], 1.0, 0.95)
    l.poly(oval(8.6, 60.4, 3.1, 2.3, -38), green[0])        # where it was cut
    l.poly(oval(8.4, 60.2, 2.1, 1.5, -38), "#eee6ae")


def _map_print(l, quad, shade=0.0, seed=0):
    """Roads, a river and a patch of green on one panel of the map (its four corners given)."""
    (ax, ay), (bx, by), (cx, cy), (dx, dy) = quad             # top left, top right, bottom right, bottom left

    def at(u, v):
        tx, ty = lerp(ax, bx, u), lerp(ay, by, u)
        ux, uy = lerp(dx, cx, u), lerp(dy, cy, u)
        return (lerp(tx, ux, v), lerp(ty, uy, v))
    dim = lambda c: mix(c, "#6a6078", shade)
    l.poly([at(0.12, 0.52), at(0.5, 0.44), at(0.9, 0.56), at(0.84, 0.78), at(0.4, 0.86), at(0.1, 0.74)], dim("#bcd69a"), 0.9)
    l.line([at(0.0, 0.2), at(0.3, 0.3), at(0.55, 0.22), at(1.0, 0.34)], dim("#58a0d8"), 1.6)                    # a river
    l.line([at(0.1, 1.0), at(0.3, 0.7), at(0.62, 0.6), at(0.8, 0.3), at(0.74, 0.0)], dim("#d84a34"), 1.5)       # the highway
    l.line([at(0.0, 0.62), at(0.3, 0.7), at(0.7, 0.92), at(1.0, 0.86)], dim("#e8a030"), 1.1)
    for (u, v) in ((0.3, 0.7), (0.62, 0.6), (0.8, 0.3)):
        px, py = at(u, v)
        l.ellipse(px, py, 1.3, 1.3, dim("#2a2630"))


def map_(b, l):
    """A road map, folded like a fan: its blue cover, and two panels of roads behind."""
    paper = ("#fbf4dc", "#d8ccb0", "#8a7c66")
    c = (32, 33)
    p0 = rot([(8, 13), (24, 9), (24, 53), (8, 57)], -9, c)
    p1 = rot([(24, 9), (40, 14), (40, 58), (24, 53)], -9, c)
    p2 = rot([(40, 14), (56, 9), (56, 53), (40, 58)], -9, c)
    b.poly(p2, paper[0])
    b.poly(p1, paper[1])
    b.poly(p0, "#3f7fb8")                                    # the cover
    _map_print(l, p1, shade=0.28)
    _map_print(l, p2, seed=1)
    band = lambda v0, v1: [(lerp(p0[0][0], p0[3][0], v0), lerp(p0[0][1], p0[3][1], v0)), (lerp(p0[1][0], p0[2][0], v0), lerp(p0[1][1], p0[2][1], v0)),
                           (lerp(p0[1][0], p0[2][0], v1), lerp(p0[1][1], p0[2][1], v1)), (lerp(p0[0][0], p0[3][0], v1), lerp(p0[0][1], p0[3][1], v1))]
    b.poly(band(0.0, 0.16), "#d84a34")
    b.poly(band(0.26, 0.60), paper[0])
    q = band(0.26, 0.60)
    l.line([lerp_pt(q[0], q[3], 0.75), lerp_pt(lerp_pt(q[0], q[1], 0.35), lerp_pt(q[3], q[2], 0.35), 0.3), lerp_pt(lerp_pt(q[0], q[1], 0.7), lerp_pt(q[3], q[2], 0.7), 0.7), lerp_pt(q[1], q[2], 0.25)], "#d84a34", 1.7)
    l.line([lerp_pt(q[0], q[3], 0.3), lerp_pt(q[1], q[2], 0.75)], "#3f7fb8", 1.1, 0.9)
    q = band(0.70, 0.76)
    l.poly(q, "#f6e7b0")
    q = band(0.82, 0.86)
    l.poly([q[0], lerp_pt(q[0], q[1], 0.6), lerp_pt(q[3], q[2], 0.6), q[3]], "#f6e7b0")
    l.line([p0[1], p0[2]], "#2a5684", 1.2, 0.9)              # the folds: a dark valley, a bright ridge
    l.line([p1[1], p1[2]], "#fffdf0", 1.1, 0.95)
    l.line([p2[1], p2[2]], paper[2], 1.3, 0.9)
    l.line([p0[3], p0[2], p1[2], p2[2]], paper[2], 1.1, 0.75)


def lerp_pt(a, b, t):
    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t))


def pass_(b, l):
    """The same map folded small: on its blank back, a scribe's quick dark signs."""
    paper = ("#fbf4dc", "#e2d6b6", "#8a7c66")
    c = (32, 33)
    T = lambda pts: rot(pts, 11, c)
    b.poly(T([(19, 11), (51, 11), (51, 57), (19, 57)]), "#3f7fb8")                   # the cover shows along one edge
    face = T([(13, 9), (46, 9), (46, 55), (13, 55)])
    b.poly(face, paper[0])
    b.poly(T([(13, 32), (46, 32), (46, 55), (13, 55)]), paper[1])                    # folded once across
    l.line(T([(13, 32), (46, 32)]), paper[2], 0.9, 0.6)
    l.poly(T([(46, 43), (46, 55), (35, 55)]), "#fffdf0")                             # a corner turned back shows the roads
    l.line(T([(37.5, 54.2), (42, 49.5), (45.4, 47.6)]), "#d84a34", 1.2)
    l.line(T([(40.6, 54.4), (45.4, 51.2)]), "#58a0d8", 1.1)
    l.line(T([(46, 43), (35, 55)]), paper[2], 1.0, 0.8)
    ink = "#2e1c14"
    pen = lambda pts, w=1.8: l.line(T(pts), ink, w)
    # above the fold: a reed leaf, water, a mouth, the sun
    pen([(17.4, 28.4), (18.2, 13.6)], 1.9)
    l.poly(T([(18.2, 13.6), (22.6, 16.4), (21.8, 21.6), (18.0, 19.4)]), ink)
    pen([(24.4, 17.4), (26.8, 14.2), (29.2, 17.4), (31.6, 14.2), (34.0, 17.4), (36.4, 14.2), (38.8, 17.4)], 1.6)
    lens = oval(31.4, 24.6, 5.6, 2.5)
    pen(lens + lens[:1], 1.4)
    sun = oval(41.2, 24.4, 2.9, 2.9)
    pen(sun + sun[:1], 1.4)
    # below it: a small bird, a loaf, three strokes for "many", a bolt
    pen(curve([(23.6, 38.6), (21.0, 36.8), (18.6, 38.6), (17.8, 43.0), (20.6, 46.4), (25.0, 46.6)], 5), 1.7)
    pen([(23.6, 38.6), (26.0, 39.4)], 1.5)
    pen(curve([(21.4, 41.2), (24.4, 43.4), (25.0, 46.6)], 4), 1.5)
    pen([(20.4, 46.6), (19.8, 50.6)], 1.4)
    pen([(23.2, 46.8), (23.6, 50.6)], 1.4)
    l.poly(T([(28.4, 50.2)] + [(32.4 + math.cos(a) * 4.0, 50.2 - math.sin(a) * 3.8) for a in np.linspace(math.pi, 0, 9)] + [(36.4, 50.2)]), ink)
    for x in (30.4, 33.8, 37.2):
        pen([(x, 36.4), (x + 0.3, 42.0)], 1.7)
    pen([(39.6, 46.2), (43.4, 46.4)], 1.5)
    pen([(41.6, 44.2), (41.4, 50.6)], 1.5)
    l.line([face[1], face[2]], paper[2], 1.0, 0.8)
    l.line([face[3], face[2]], paper[2], 1.0, 0.7)


def flashlight(b, l):
    """A yellow flashlight with a black grip and a wide chrome head."""
    ax, ay, ux, uy = 9.0, 51.5, 0.762, -0.648                # its tail, and the way it points
    nx, ny = -uy, ux                                         # across it, toward the shadow side

    def at(t, w):
        return (ax + ux * t + nx * w, ay + uy * t + ny * w)

    def slab(t0, t1, w0, w1, color, w0b=None, w1b=None):
        b.poly([at(t0, -w0), at(t1, -w1), at(t1, w1b if w1b is not None else w1), at(t0, w0b if w0b is not None else w0)], color)

    b.poly(loop([at(-1.5, -4.6), at(1, -6.4), at(3, -6.4), at(3, 6.4), at(1, 6.4), at(-1.5, 4.6)], 4), "#c0881c")     # the cap on its tail
    slab(2, 26, 6.4, 6.4, "#f8cc34")
    slab(2, 26, 6.4, 6.4, "#ffe872", -2.2, -2.2)             # the top of the barrel, in the sun
    slab(2, 26, -2.6, -2.6, "#c0881c", 6.4, 6.4)             # and its underside
    slab(26, 33, 6.8, 6.8, "#2a2a32")                        # the grip
    slab(26, 33, 6.8, 6.8, "#4a4a56", -2.6, -2.6)
    slab(33, 40, 6.8, 11.6, "#aab4c0")                       # the head flares
    slab(33, 40, 6.8, 11.6, "#f0f4f6", -1.4, -2.6)
    slab(33, 40, -3.4, -6.4, "#6a7480", 6.8, 11.6)
    slab(40, 46, 11.6, 11.6, "#aab4c0")
    slab(40, 46, 11.6, 11.6, "#f0f4f6", -2.6, -2.6)
    slab(40, 46, -6.4, -6.4, "#6a7480", 11.6, 11.6)
    cx, cy = at(46, 0)
    ang = math.degrees(math.atan2(uy, ux))
    b.poly(oval(cx, cy, 4.2, 11.6, ang), "#7a8490")          # the rim of the lens
    l.poly(oval(cx + ux * 0.5, cy + uy * 0.5, 3.2, 9.6, ang), "#fff4b8")
    l.poly(oval(cx + ux * 0.6 + nx * 2.6, cy + uy * 0.6 + ny * 2.6, 2.0, 5.4, ang), "#f4d470")
    l.poly(oval(cx + ux * 0.6 - nx * 4.2, cy + uy * 0.6 - ny * 4.2, 1.2, 2.6, ang), "#ffffff")
    for t in (27.5, 29.5, 31.5):                             # ribs on the grip
        l.line([at(t, -6.4), at(t, 6.4)], "#14141a", 0.8, 0.8)
    l.line([at(4, -4.4), at(24, -4.4)], "#fffbd0", 1.3, 0.95)
    l.poly(loop([at(11, -5.0), at(17, -5.0), at(17, -1.4), at(11, -1.4)], 3), "#d83a2c")      # the switch
    l.line([at(11.6, -4.4), at(16.4, -4.4)], "#ff8a70", 0.9)
    l.line([at(33, -6.8), at(33, 6.8)], "#5a6470", 0.9, 0.9)
    l.line([at(40, -11.6), at(40, 11.6)], "#ffffff", 0.9, 0.7)


def rootbeer(b, l):
    """A brown bottle, cold, with a plain cream label and a gold cap."""
    c = (32, 34)
    glass = ("#431f0e", "#7a4220", "#b86c2c", "#f8c884")
    body = [(22, 58.5), (21.6, 36), (22.6, 31), (26.6, 25), (28.2, 20), (28.2, 10), (35.8, 10), (35.8, 20), (37.4, 25), (41.4, 31), (42.4, 36), (42, 58.5), (39, 60.4), (25, 60.4)]
    b.poly(rot(body, 9, c), glass[1])
    b.poly(rot([(22, 58.5), (21.6, 36), (22.6, 31), (26.6, 25), (28.2, 20), (28.2, 10), (31, 10), (31, 20), (29.4, 26), (26, 31.6), (25.4, 37), (25.6, 60.4), (25, 60.4)], 9, c), glass[2])
    b.poly(rot([(42, 58.5), (42.4, 36), (41.4, 31), (37.4, 25), (35.8, 20), (35.8, 10), (33.8, 10), (33.8, 20), (35.4, 26), (38.6, 31.6), (39.2, 37), (39, 60.4)], 9, c), glass[0])
    b.poly(rot([(21.7, 38.5), (42.3, 38.5), (42.2, 52), (21.9, 52)], 9, c), "#f6ecc8")        # the label: no words on it
    b.poly(rot([(38.4, 38.5), (42.3, 38.5), (42.2, 52), (38.6, 52)], 9, c), "#cdbf98")
    l.poly(rot(rrect(30.6, 46.6, 3.9, 3.4, 1.0), 9, c), "#7a4220")                          # a little mug of it, with a head of foam
    l.line(rot(curve([(34.2, 44.8), (37.4, 45.6), (37.2, 48.0), (34.2, 48.8)], 4), 9, c), "#7a4220", 1.3)
    foam = rot(loop([(26.2, 43.4), (27.6, 41.4), (30.0, 42.0), (32.2, 41.2), (34.6, 42.2), (35.0, 43.8), (30.6, 44.4)], 4), 9, c)
    l.poly(foam, "#fffdf2")
    l.line(foam + foam[:1], "#a8763c", 0.8, 0.9)
    l.line(rot([(28.4, 45.4), (28.4, 48.6)], 9, c), "#b8742c", 0.9, 0.9)
    l.line(rot([(22.6, 40.2), (41.6, 40.2)], 9, c), "#c8402c", 1.0, 0.95)
    l.line(rot([(22.6, 50.4), (41.6, 50.4)], 9, c), "#c8402c", 1.0, 0.95)
    b.poly(rot([(26.8, 4.6), (37.2, 4.6), (37.8, 10.4), (26.2, 10.4)], 9, c), "#e6b838")       # the cap
    l.poly(rot([(26.8, 4.6), (31.6, 4.6), (31.2, 10.4), (26.2, 10.4)], 9, c), "#fde27c")
    l.line(rot([(26.4, 10.4), (37.6, 10.4)], 9, c), "#8a6418", 1.2)
    l.line(rot([(23.6, 34.6), (24.0, 30.6), (27.6, 25.4), (29.2, 20.4), (29.2, 12)], 9, c), glass[3], 1.3, 0.95)       # the light down its shoulder
    l.line(rot([(23.6, 54), (23.6, 58)], 9, c), glass[3], 1.2, 0.9)
    for (x, y, r) in ((36.6, 30.4, 1.0), (34.6, 34.6, 0.8), (37.4, 56, 1.0), (30.4, 56.6, 0.8), (33.6, 16, 0.8)):      # beads of cold
        px, py = rot([(x, y)], 9, c)[0]
        l.ellipse(px, py, r, r * 1.25, "#e6b47a", 0.95)
        l.ellipse(px - 0.3, py - 0.4, r * 0.45, r * 0.5, "#fff0d0")


def shade(b, l):
    """A silver windshield shade, folded like a fan and held with a strap."""
    c = (32, 32)
    silver = ("#ffffff", "#e4edf4", "#aebccc", "#6e7e94")
    n = 6
    xs = [lerp(7, 57, i / n) for i in range(n + 1)]
    top = [13 if i % 2 == 0 else 17.5 for i in range(n + 1)]
    bot = [49 if i % 2 == 0 else 53.5 for i in range(n + 1)]
    for i in range(n):
        quad = rot([(xs[i], top[i]), (xs[i + 1], top[i + 1]), (xs[i + 1], bot[i + 1]), (xs[i], bot[i])], -7, c)
        b.poly(quad, silver[1] if i % 2 == 0 else silver[2])
        if i % 2 == 0:                                       # the sky lies in the panels that face up
            b.poly(rot([(xs[i], top[i]), (xs[i + 1], top[i + 1]), (xs[i + 1], top[i + 1] + 11), (xs[i], top[i] + 15)], -7, c), "#cfe6f8")
    for i in range(n + 1):
        l.line(rot([(xs[i], top[i]), (xs[i], bot[i])], -7, c), silver[0] if i % 2 == 0 else silver[3], 1.2, 0.95 if i % 2 == 0 else 0.85)
    l.line(rot([(xs[i], bot[i]) for i in range(n + 1)], -7, c), silver[3], 1.3, 0.9)
    l.line(rot([(xs[i], top[i]) for i in range(n + 1)], -7, c), silver[0], 1.0, 0.9)
    strap = [(xs[i], lerp(top[i], bot[i], 0.56)) for i in range(n + 1)]
    l.line(rot(strap, -7, c), "#1e222c", 4.4)                # the strap round it
    l.line(rot([(x, y - 1.2) for x, y in strap], -7, c), "#4a5262", 1.0, 0.9)
    bx, by = rot([lerp_pt(strap[2], strap[3], 0.5)], -7, c)[0]
    l.poly(rot([(bx - 3.4, by - 3.4), (bx + 3.4, by - 3.4), (bx + 3.4, by + 3.4), (bx - 3.4, by + 3.4)], -7, (bx, by)), "#d83a2c")
    l.line([(bx - 2.2, by - 2.0), (bx + 1.0, by - 2.0)], "#ff9a84", 0.9)
    for (i, v0, v1) in ((0, 0.12, 0.44), (2, 0.66, 0.9), (4, 0.1, 0.36)):                     # the sun in it
        a = (lerp(xs[i], xs[i + 1], 0.25), lerp(top[i], bot[i], v0))
        z = (lerp(xs[i], xs[i + 1], 0.7), lerp(top[i], bot[i], v1))
        l.line(rot([a, z], -7, c), silver[0], 1.7, 0.95)


def carmirror(b, l):
    """The wagon's door mirror: a chrome shell on a short arm and a foot, the sky and the sand in its glass."""
    chrome = ("#ffffff", "#e2e8ee", "#a2acb8", "#5c6672")
    c, deg = (37.0, 25.5), -11
    b.poly(loop([(2.6, 50.6), (15.6, 44.6), (22.6, 55.6), (8.6, 61.6)], 4), chrome[3])        # the foot that bolts to the door
    b.poly(loop([(2.6, 49.6), (15.4, 43.8), (21.6, 54.2), (8.2, 60.2)], 4), chrome[2])
    b.poly(loop([(3.4, 49.6), (15.0, 44.4), (17.4, 48.4), (5.6, 53.8)], 4), chrome[1])
    b.taper([(13.6, 50.6), (19.6, 42.6), (26.4, 37.0)], chrome[3], 10.4, 9.4)                 # the arm: short and thick
    b.taper([(12.8, 49.6), (18.8, 41.6), (25.6, 36.2)], chrome[2], 7.6, 6.8)
    b.taper([(11.8, 48.4), (17.8, 40.4), (24.6, 35.0)], chrome[1], 3.4, 3.0)
    b.poly(rrect(c[0] + 1.3, c[1] + 1.4, 24.6, 17.0, 8.6, deg), chrome[3])                    # the shell: its dark edge first
    b.poly(rrect(c[0], c[1], 24.2, 16.6, 8.4, deg), chrome[2])
    b.poly(rrect(c[0] - 1.3, c[1] - 1.3, 22.4, 14.8, 7.6, deg), chrome[1])
    T = lambda pts: rot(pts, deg, c)
    gx, gy, hw, hh = c[0] + 0.4, c[1] + 0.4, 18.6, 11.2
    b.poly(rrect(gx, gy, hw, hh, 5.4, deg), "#86bcec")                                        # the glass: sky ...
    b.poly(T([(gx - hw + 0.6, gy - 0.6), (gx + hw - 0.6, gy - 0.6), (gx + hw - 0.6, gy + 4.4), (gx - hw + 0.6, gy + 4.4)]), "#c4e0f6")
    b.poly(T([(gx - hw + 0.6, gy + 3.6), (gx + hw - 0.6, gy + 3.6), (gx + hw - 0.6, gy + hh - 3.6), (gx + hw - 4.0, gy + hh - 0.5), (gx - hw + 4.0, gy + hh - 0.5), (gx - hw + 0.6, gy + hh - 3.6)]), "#e4b472")   # ... and sand
    b.poly(T([(gx + 2, gy + 3.6), (gx + 9, gy - 1.6), (gx + 13.4, gy + 3.6)]), "#f4dca4")     # a far pyramid in it
    b.poly(T([(gx + 9, gy - 1.6), (gx + 13.4, gy + 3.6), (gx + 10.4, gy + 3.6)]), "#b9a0b4")
    l.poly(T(loop([(gx - 13, gy - 3.6), (gx - 10, gy - 7.4), (gx - 5.4, gy - 6.4), (gx - 2, gy - 8.6), (gx + 2, gy - 5.6), (gx - 1, gy - 2.6), (gx - 8, gy - 2.0)], 4)), "#ffffff")     # a cloud
    rim = rrect(gx, gy, hw, hh, 5.4, deg)
    l.line(rim + rim[:1], chrome[3], 1.3, 0.9)
    outer = rrect(c[0] - 1.3, c[1] - 1.3, 22.4, 14.8, 7.6, deg)
    l.line(outer[14:28] + outer[:1], chrome[0], 1.6, 0.95)                                    # the sun along its top and left
    l.line(T([(gx - 14.6, gy + 6.6), (gx - 9.6, gy - 8.6)]), "#ffffff", 1.6, 0.55)            # a streak across the glass
    l.line(T([(gx - 11.6, gy + 7.6), (gx - 7.2, gy - 5.6)]), "#ffffff", 0.9, 0.45)
    for (x, y) in ((7.6, 55.6), (16.0, 51.6)):                                                # two screws
        l.ellipse(x, y, 1.5, 1.5, chrome[3])
        l.ellipse(x - 0.4, y - 0.4, 0.6, 0.6, chrome[0])
    l.line([(22.6, 55.6), (8.6, 61.6)], chrome[3], 1.2, 0.8)


def sunglasses(b, l):
    """Dad's sunglasses: gold wire, big dark-green lenses."""
    gold = ("#fbe28a", "#d8a838", "#8a641c")
    lens = [(-11.6, -6.4), (-3, -8.6), (7, -8.2), (12, -4.6), (12.4, 2.6), (8, 9), (0, 10.6), (-7.6, 8), (-11.6, 2)]
    c = (32, 33)
    for k, (cx, cy, flip) in enumerate(((19.6, 34.6, 1), (45.2, 31.8, -1))):
        pts = rot([(cx + px * flip, cy + py) for px, py in lens], -6, c)
        b.poly(loop(pts, 5), "#24302c")
        inner = rot([(cx + px * flip * 0.9, cy + 1.4 + py * 0.62 + 2.6) for px, py in lens], -6, c)
        b.poly(loop(inner, 5), "#48604e")                    # the lens is lighter toward the bottom
        low = rot([(cx + px * flip * 0.72, cy + 5.6 + py * 0.3) for px, py in lens], -6, c)
        b.poly(loop(low, 5), "#7c9a78")
        ring = loop(pts, 5)
        l.line(ring + ring[:1], gold[2], 2.3)
        l.line(ring + ring[:1], gold[1], 1.3)
        gx, gy = rot([(cx - 5.6, cy - 3.6)], -6, c)[0]
        l.line([(gx - 2.4, gy + 2.6), (gx + 3.0, gy - 2.6)], "#eaf6ff", 2.0, 0.95)      # the sky in each lens
        l.line([(gx + 1.6, gy + 4.0), (gx + 5.4, gy + 0.4)], "#bcd6e6", 1.2, 0.9)
    l.line(rot([(28.6, 28.4), (32.4, 26.4), (36.4, 27.0)], -6, c), gold[2], 2.2)        # the bridge, and the bar over it
    l.line(rot([(28.6, 28.4), (32.4, 26.4), (36.4, 27.0)], -6, c), gold[0], 1.1)
    l.line(rot([(27.4, 33.6), (32.4, 31.6), (37.6, 32.4)], -6, c), gold[2], 1.9)
    l.line(rot([(27.4, 33.6), (32.4, 31.6), (37.6, 32.4)], -6, c), gold[1], 1.0)
    arm = rot(curve([(56.6, 27.6), (60.4, 23.4), (61.6, 18), (59.4, 13.6)], 5), -6, c)   # one arm folds away behind
    l.line(arm, gold[2], 2.2)
    l.line(arm, gold[1], 1.2)
    arm2 = rot(curve([(8.2, 31.4), (4.6, 28.6), (3.4, 24)], 4), -6, c)
    l.line(arm2, gold[2], 2.2)
    l.line(arm2, gold[0], 1.1)


def coppermirror(b, l):
    """The goldsmith's hand mirror: a disc of polished copper on a short handle of blue-green faience
    shaped like a papyrus stem."""
    c = (32, 32)
    T = lambda pts: rot(pts, -13, c)
    copper = ("#fff0d2", "#f8bc88", "#e08650", "#a8522c", "#6e3018")
    blue = ("#9ae0d2", "#3fa69c", "#1f6c6c", "#123f48")
    stem = [(23.6, 39.6), (40.4, 39.6), (37.2, 45.6), (35.4, 48.6), (35.0, 57.0), (37.6, 59.4), (37.6, 62.6), (26.4, 62.6), (26.4, 59.4), (29.0, 57.0), (28.6, 48.6), (26.8, 45.6)]
    b.poly(T([(x + 1.0, y + 1.0) for x, y in stem]), blue[3])
    b.poly(T(stem), blue[1])                                 # the handle: the flower of the papyrus spreads under the disc
    b.poly(T([(23.6, 39.6), (31.0, 39.6), (30.6, 48.6), (31.0, 57.0), (29.6, 62.6), (26.4, 62.6), (26.4, 59.4), (29.0, 57.0), (28.6, 48.6), (26.8, 45.6)]), blue[0])
    b.poly(T([(36.0, 39.6), (40.4, 39.6), (37.2, 45.6), (35.4, 48.6), (35.0, 57.0), (37.6, 59.4), (37.6, 62.6), (34.6, 62.6), (33.6, 57.0), (33.8, 48.6)]), blue[2])
    b.poly(T([(28.0, 47.8), (36.0, 47.8), (35.6, 51.2), (28.4, 51.2)]), "#e6bc48")              # a band of gold
    b.poly(T(oval(32.8, 22.6, 22.6, 19.6)), copper[4])       # the disc: its dark edge first
    b.poly(T(oval(32, 21.8, 22.2, 19.2)), copper[3])
    b.poly(T(oval(31.2, 21.0, 20.6, 17.6)), copper[2])
    b.poly(T(loop([(12.4, 20), (17.2, 9.4), (28, 4.2), (40.4, 5.6), (32.6, 10.4), (24, 16.4), (19, 25), (15.2, 30.6)], 5)), copper[1])        # the light sweeps across it
    l.poly(T([(20.0, 24.6), (33.4, 8.4), (39.0, 9.4), (24.8, 27.4)]), copper[0], 0.95)
    l.poly(T([(29.6, 30.4), (44.0, 13.4), (46.4, 15.4), (32.4, 32.4)]), copper[1], 0.9)
    ring = T(oval(32, 21.8, 22.2, 19.2))
    l.line(ring[1:13], copper[4], 1.6, 0.85)                 # the shadow-side edge
    l.line(ring[15:25], copper[0], 1.2, 0.85)
    sx, sy = T([(19.8, 11.6)])[0]
    l.poly([(sx, sy - 5.0), (sx + 1.1, sy - 1.1), (sx + 5.0, sy), (sx + 1.1, sy + 1.1), (sx, sy + 5.0), (sx - 1.1, sy + 1.1), (sx - 5.0, sy), (sx - 1.1, sy - 1.1)], "#ffffff")
    l.line(T([(28.4, 51.4), (35.6, 51.4)]), "#8a6418", 1.0)
    l.line(T([(28.2, 48.0), (31.4, 48.0)]), "#fff2b0", 1.0)
    for x in (27.6, 32.0, 36.4):                             # the petals, cut into the flare
        l.line(T([(x, 40.4), (lerp(x, 32, 0.5), 45.8)]), blue[2], 0.9, 0.9)
    l.line(T([(23.8, 39.9), (40.2, 39.9)]), blue[0], 0.9, 0.9)
    for y in (54.0, 56.4):
        l.line(T([(29.2, y), (34.8, y)]), blue[2], 0.8, 0.8)


def _folded(b, l, a, u, v, drop, tones, layers=3):
    """A folded cloth seen from above and in front: its top (far left corner `a`, edges `u` going right and
    back, `v` coming right and toward us), and the two edges of the pile toward us, `drop` deep, with the folds
    showing. -> a function giving places on the top."""
    top = lambda s, t, d=0.0: (a[0] + u[0] * s + v[0] * t, a[1] + u[1] * s + v[1] * t + d)
    b.poly(loop([top(0, 0), top(0, 1), top(0, 1, drop), top(0, 0.5, drop + 0.8), top(0, 0, drop)], 3), tones[1])            # the edge to the left, in half light
    b.poly(loop([top(0, 1), top(1, 1), top(1, 1, drop), top(0.5, 1, drop + 1.2), top(0, 1, drop)], 3), tones[2])            # the edge to the right, in shade
    b.poly(loop([top(0, 0), top(0.5, -0.03), top(1, 0), top(1.03, 0.5), top(1, 1), top(0.5, 1.03), top(0, 1), top(-0.03, 0.5)], 4), tones[0])
    for k in range(1, layers):                               # the folds of the pile
        d = drop * k / layers
        l.line([top(0, 0.02, d), top(0, 0.5, d + 0.5), top(0, 1, d)], tones[3], 0.9, 0.6)
        l.line([top(0, 1, d), top(0.5, 1, d + 0.8), top(0.98, 1, d)], tones[3], 1.0, 0.8)
    l.line([top(0, 1, 0.4), top(0, 1, drop)], tones[3], 0.9, 0.6)
    l.line([top(0, 0), top(0, 1), top(1, 1)], "#ffffff", 0.9, 0.55)
    return top


def toga(b, l):
    """The senator's toga, folded: white wool with a purple stripe along its edge."""
    tones = ("#fdf9ee", "#dfd9d2", "#b4adc4", "#8a84a2")
    top = _folded(b, l, (6, 24), (26, -12), (27, 14), 15, tones)
    purple = ("#8a44a4", "#5c2876", "#b876cc")
    s0, s1 = 0.56, 0.78
    b.poly([top(s0, 0), top(s1, 0), top(s1, 1), top(s0, 1)], purple[0])                    # the stripe across the top ...
    b.poly([top(s0, 1), top(s1, 1), top(s1, 1, 15.3), top(s0, 1, 15.9)], purple[1])        # ... and down over the edge
    l.line([top(s0, 0), top(s0, 1), top(s0, 1, 15.8)], purple[1], 0.9, 0.8)
    l.line([top(s1, 0.02), top(s1, 1)], purple[2], 0.9, 0.9)
    for d in (5, 10):
        l.line([top(s0, 1, d + 0.5), top(s1, 1, d + 0.3)], "#3c1650", 0.9, 0.7)
    b.poly(loop([top(0.06, 0.16), top(0.46, 0.1), top(0.48, 0.5), top(0.28, 0.86), top(0.05, 0.8)], 4), "#ffffff")       # the light on the top fold
    l.line([top(0.06, 0.55), top(0.5, 0.5)], tones[1], 1.0, 0.8)                           # a soft crease


def tunic(b, l):
    """A small plain tunic of undyed wool, folded with its sleeves across its front and tied with its rope belt."""
    c = (32, 33)
    T = lambda pts: rot(pts, -8, c)
    wool = ("#f4e4bc", "#dcc594", "#b39a6a", "#7c6440")
    b.poly(T(rrect(33.4, 36.4, 22.6, 22.6, 4)), wool[3])                                    # the pile's shadow side
    b.poly(T(rrect(32, 35, 22, 22, 4)), wool[1])
    b.poly(T([(11, 15), (32, 15), (30, 34), (11, 36)]), wool[0])                           # the half toward the sun
    b.poly(T([(10.6, 50), (53.4, 50), (53.4, 55.4), (50, 57), (14, 57), (10.6, 55.4)]), wool[2])     # the fold along the bottom
    for (x0, x1, x2, x3, tone) in ((10.4, 21.6, 26.6, 12.4, wool[0]), (53.6, 42.4, 37.4, 51.6, wool[2])):                 # the sleeves, folded across
        b.poly(T([(x0, 13.4), (x1, 13.4), (x2, 33.6), (x3, 36.6)]), tone)
        l.line(T([(x1, 13.6), (x2, 33.6), (x3, 36.6)]), wool[3], 1.0, 0.8)
    l.poly(T([(24.6, 12.8)] + [(32 + math.cos(a) * 7.4, 13.0 + math.sin(a) * 6.6) for a in np.linspace(math.pi, 0, 9)] + [(39.4, 12.8)]), "#5c4830")       # the neck
    l.line(T([(32 + math.cos(a) * 7.4, 13.0 + math.sin(a) * 6.6) for a in np.linspace(math.pi, 0, 9)]), wool[0], 1.2, 0.95)
    l.line(T([(32, 19.8), (32, 26.6)]), wool[3], 1.0, 0.8)
    l.line(T([(10.6, 50), (53.4, 50)]), wool[3], 1.0, 0.75)
    belt = [(10.2, 42.4), (20, 41.6), (32, 42.6), (44, 41.6), (53.8, 42.4)]
    l.line(T(belt), "#4a3018", 3.4)                          # the belt: a cord, twisted
    l.line(T(belt), "#b88a4a", 2.0)
    for x in range(12, 53, 3):
        l.line(T([(x, 41.2), (x + 1.4, 43.4)]), "#4a3018", 0.8, 0.9)
    l.poly(T(oval(32, 42.4, 3.4, 2.9)), "#8a6030")           # its knot, and the two ends
    l.line(T([(31, 44.6), (28.4, 53.6)]), "#4a3018", 2.6)
    l.line(T([(31, 44.6), (28.4, 53.6)]), "#b88a4a", 1.4)
    l.line(T([(33.4, 44.6), (36.4, 52.4)]), "#4a3018", 2.6)
    l.line(T([(33.4, 44.6), (36.4, 52.4)]), "#9a7038", 1.4)


def breakfast(b, l):
    """The soothsayer's breakfast: a round loaf and a sausage, in a cloth twisted shut at the top."""
    cloth = ("#f6f0e0", "#d2cabc", "#a39cae", "#74708a")
    b.poly(loop([(5, 47), (10, 36), (22, 31), (40, 31), (54, 36), (59, 47), (53, 57), (36, 61.4), (17, 60), (8, 55)], 5), cloth[1])        # the cloth, open
    b.poly(loop([(41, 33), (54, 36.6), (59, 47), (53, 57), (40, 60.6), (45, 48)], 5), cloth[2])
    b.poly(loop([(8.6, 37), (15, 24.6), (30, 19.6), (41, 25), (43, 37), (34, 46), (18, 46.6), (10, 43)], 5), "#8a5420")                    # the loaf: its crust
    b.poly(loop([(10.4, 35.6), (16, 25.4), (29.6, 21), (39.6, 25.6), (41, 34), (33, 40.6), (19, 41.4), (12, 39)], 5), "#d99a44")
    b.poly(loop([(12.6, 33.4), (17.6, 26.4), (29, 22.6), (36.6, 25.6), (30, 29), (20, 31.4), (15, 35.4)], 5), "#f6cc7a")
    for (x0, y0, x1, y1) in ((25.6, 31.4, 15.6, 27.6), (25.6, 31.4, 30.4, 22.4), (25.6, 31.4, 38.6, 30.6), (25.6, 31.4, 20, 39.6), (25.6, 31.4, 32, 38.6)):
        l.line([(x0, y0), (x1, y1)], "#8a5420", 1.2, 0.8)    # scored into wedges
    saus = curve([(33, 49.6), (40, 45), (48, 38), (55.6, 29)], 7)
    b.taper(saus, "#5a2018", 10.4, 9.0)                      # the sausage
    b.taper([(x - 0.7, y - 0.9) for x, y in saus], "#a84434", 7.4, 6.2)
    l.taper([(x - 1.9, y - 2.3) for x, y in saus[2:-3]], "#e8846a", 1.9, 1.3)
    for (px, py), (qx, qy) in ((saus[0], saus[1]), (saus[-1], saus[-2])):                  # its tied ends
        l.line([(px, py), (px + (px - qx) * 1.3, py + (py - qy) * 1.3)], "#5a2018", 2.2)
    b.poly(loop([(6, 49), (16, 44.6), (30, 47.6), (44, 50.6), (57, 46.4), (53, 57), (36, 61.4), (17, 60), (8, 55)], 5), cloth[0])          # the near fold of the cloth, over them
    b.poly(loop([(34, 52.6), (46, 51.4), (57, 46.6), (53, 57), (40, 60.8)], 4), cloth[1])
    for run in ([(10, 51), (20, 49.6), (30, 52.6)], [(14, 56.6), (26, 56), (36, 58.6)], [(42, 54.6), (50, 53.4)]):
        l.line(curve(run, 4), cloth[2], 1.0, 0.85)
    for x in (14, 22, 30, 46):                               # a blue stripe woven in
        l.line([(x, 46.8 + (x - 30) * 0.02), (x + 0.8, 60)], "#5a86c4", 1.1, 0.5)
    b.poly(loop([(46, 28), (49, 18.6), (53.6, 13.4), (56.6, 16.6), (54, 23), (55, 30), (50, 33.6)], 4), cloth[1])                          # the corners twisted together
    b.poly(loop([(46.6, 27.6), (49, 19), (52.6, 15), (51.6, 22), (51, 30)], 4), cloth[0])
    l.line([(47, 27.6), (54.6, 30.4)], cloth[3], 1.9, 0.9)
    l.line([(47, 26.6), (54.6, 29.4)], "#5a86c4", 0.9, 0.9)


def incense(b, l):
    """A little wooden box with a lid and a bronze knob; a few tears of the resin beside it."""
    wood = ("#e6b470", "#c08848", "#8a5a2e", "#553218")
    a, u, v = (7, 22), (24, -10), (24, 13)
    top = lambda s, t, d=0.0: (a[0] + u[0] * s + v[0] * t, a[1] + u[1] * s + v[1] * t + d)
    drop = 23
    b.poly([top(0, 0), top(0, 1), top(0, 1, drop), top(0, 0, drop)], wood[1])              # the side to the left, in half light
    b.poly([top(0, 1), top(1, 1), top(1, 1, drop), top(0, 1, drop)], wood[2])              # the side to the right, in shade
    e = 0.05                                                                               # the lid stands out a little all round
    b.poly([top(-e, -e), top(-e, 1 + e), top(-e, 1 + e, 6), top(-e, -e, 6)], wood[1])
    b.poly([top(-e, 1 + e), top(1 + e, 1 + e), top(1 + e, 1 + e, 6), top(-e, 1 + e, 6)], wood[2])
    b.poly([top(-e, -e), top(1 + e, -e), top(1 + e, 1 + e), top(-e, 1 + e)], wood[0])
    b.poly([top(0.1, 0.1), top(0.9, 0.1), top(0.9, 0.9), top(0.1, 0.9)], "#f2cc88")
    l.line([top(0.1, 0.1), top(0.9, 0.1), top(0.9, 0.9), top(0.1, 0.9), top(0.1, 0.1)], wood[2], 0.9, 0.75)
    l.line([top(-e, -e, 6.5), top(-e, 1 + e, 6.5), top(1 + e, 1 + e, 6.5)], wood[3], 1.4, 0.9)       # the dark line under the lid
    l.line([top(-e, -e), top(-e, 1 + e), top(1 + e, 1 + e)], "#fbdca0", 0.9, 0.85)
    for d in (12.0, 17.5):                                   # the grain of the wood
        l.line([top(0, 0.05, d), top(0, 0.96, d + 0.3)], wood[3], 0.8, 0.4)
        l.line([top(0.04, 1, d + 0.3), top(0.96, 1, d)], wood[3], 0.8, 0.5)
    l.line([top(0, 1, 6.6), top(0, 1, drop)], wood[3], 1.0, 0.7)
    l.line([top(0, 0, drop), top(0, 1, drop), top(1, 1, drop)], wood[3], 1.2, 0.8)
    l.poly([top(0.36, 1, 12), top(0.64, 1, 12), top(0.64, 1, 17), top(0.36, 1, 17)], "#d8a43c")       # a bronze plate on the front
    l.poly([top(0.36, 1, 12), top(0.64, 1, 12), top(0.64, 1, 13.2), top(0.36, 1, 13.2)], "#fff0b0")
    kx, ky = top(0.5, 0.5)
    l.ellipse(kx + 0.7, ky - 1.4, 3.9, 3.4, "#6a4a16")       # the knob
    l.ellipse(kx, ky - 2.1, 3.3, 2.9, "#d8a43c")
    l.ellipse(kx - 1.0, ky - 3.1, 1.2, 1.0, "#fff0b0")
    for (x, y, r) in ((48.6, 56.6, 2.9), (55.4, 53.0, 2.3), (56.0, 59.6, 2.0), (42.6, 60.0, 1.9)):       # the incense itself: tears of amber resin
        l.poly(loop([(x - r, y + r * 0.2), (x - r * 0.4, y - r * 0.9), (x + r * 0.7, y - r * 0.7), (x + r, y + r * 0.4), (x, y + r * 0.9)], 3), "#a8641c")
        l.poly(loop([(x - r * 0.9, y), (x - r * 0.4, y - r * 0.8), (x + r * 0.5, y - r * 0.6), (x + r * 0.2, y + r * 0.2)], 3), "#f6c458")
        l.ellipse(x - r * 0.35, y - r * 0.4, r * 0.3, r * 0.25, "#fff4c8")


def coin(b, l):
    """A new silver coin. The stern man on it is nobody: a heavy brow, a set jaw, hair cropped short."""
    silver = ("#ffffff", "#e6ebf0", "#aab4c0", "#7c8796", "#4a5260")
    b.poly(oval(33.4, 33.6, 26, 25.4, -8), silver[4])        # its thickness shows on the shadow side
    b.poly(oval(32, 32, 26, 25.4, -8), silver[1])            # the raised rim
    b.poly(oval(32, 32, 22.6, 22.0, -8), silver[2])          # the field, a tone down, so the head stands off it
    b.poly(loop([(42, 12.6), (51, 20), (54.2, 32), (50.4, 44), (42, 52), (47.6, 41), (48.6, 30), (46, 20)], 5), silver[3])      # the field falls away from the sun
    b.poly(loop([(12, 30), (14.6, 20), (22, 12.6), (30, 10.6), (22, 17), (17, 25), (15.6, 36)], 5), "#c6ced8")
    head = [(24.6, 52.6), (23.4, 46.0), (20.6, 39.4), (19.8, 31.0), (21.8, 23.6), (26.6, 18.6), (33.0, 17.0), (38.6, 19.0), (41.0, 23.6), (41.4, 27.0),
            (43.2, 27.8), (42.2, 30.0), (46.6, 35.2), (43.6, 36.6), (44.2, 38.2), (42.8, 39.2), (43.8, 40.8), (42.6, 42.4), (43.2, 45.4), (40.6, 47.8),
            (37.0, 47.6), (36.6, 50.0), (39.8, 53.6), (32, 55.2)]
    b.poly([(x + 1.5, y + 1.6) for x, y in head], silver[4])  # the relief throws a small shadow
    b.poly(head, "#f6f8fa")
    hair = [(21.8, 23.6), (26.6, 18.6), (33.0, 17.0), (38.6, 19.0), (40.2, 22.0), (36.0, 23.4), (31.4, 23.8), (28.8, 27.6), (28.2, 33.6), (25.4, 37.6), (24.0, 44.4), (20.6, 39.4), (19.8, 31.0)]
    b.poly(hair, silver[3])                                  # the cropped hair
    b.poly([(33.6, 46.6), (37.0, 47.6), (36.6, 50.0), (39.8, 53.6), (32, 55.2), (26.6, 54.0), (28.6, 49.6)], "#cdd5dd")       # the neck, under the jaw
    l.line(head[9:21], silver[4], 1.1, 0.75)                 # the profile itself, cut crisp
    l.line([(38.4, 28.2), (43.0, 28.0)], silver[4], 1.6)     # the brow, low over the eye
    l.line([(39.4, 30.5), (41.6, 30.5)], silver[4], 1.3, 0.95)
    l.line([(40.0, 39.8), (42.8, 39.3)], silver[4], 1.2)     # the mouth, shut tight
    l.line([(39.0, 41.4), (40.0, 39.8)], silver[4], 0.9, 0.8)
    l.line(curve([(31.6, 31.0), (29.6, 33.4), (31.2, 36.8), (33.4, 35.0)], 4), silver[4], 1.1, 0.9)       # the ear
    l.line([(33.6, 46.0), (36.6, 44.4), (38.6, 41.0)], silver[3], 1.0, 0.85)                               # the line of the jaw
    l.line([(43.6, 36.6), (41.8, 36.2)], silver[3], 0.9, 0.8)                                              # the nostril
    for (x0, y0, x1, y1) in ((24.6, 23.6, 22.4, 29.0), (28.6, 20.4, 25.6, 26.0), (33.0, 19.2, 30.4, 22.6), (37.4, 20.2, 35.4, 22.4), (22.0, 32.6, 24.6, 37.0), (25.6, 29.0, 26.4, 33.6)):
        l.line([(x0, y0), (x1, y1)], silver[4], 0.9, 0.75)   # hair: short strokes
        l.line([(x0 + 1.2, y0 + 0.3), (x1 + 1.2, y1 + 0.3)], silver[1], 0.7, 0.6)
    for i in range(26):                                      # beads round the rim
        ang = i / 26 * 2 * math.pi
        x, y = rot([(32 + math.cos(ang) * 24.2, 32 + math.sin(ang) * 23.6)], -8)[0]
        lit = math.cos(ang - math.radians(225))
        l.ellipse(x, y, 1.15, 1.15, silver[0] if lit > 0.25 else (silver[2] if lit > -0.4 else silver[3]))
    ring = oval(32, 32, 26, 25.4, -8)
    l.line(ring[13:24], silver[0], 1.3, 0.9)                 # the rim, bright toward the sun
    l.line(ring[0:9], silver[4], 1.2, 0.7)
    inner = oval(32, 32, 22.6, 22.0, -8)
    l.line(inner[13:24], silver[3], 0.9, 0.6)
    l.line(inner[0:9], silver[0], 0.9, 0.7)
    sx, sy = 14.6, 13.6                                      # it is new: it glints
    l.poly([(sx, sy - 6.4), (sx + 1.3, sy - 1.3), (sx + 6.4, sy), (sx + 1.3, sy + 1.3), (sx, sy + 6.4), (sx - 1.3, sy + 1.3), (sx - 6.4, sy), (sx - 1.3, sy - 1.3)], "#ffffff")


def note(b, l):
    """A yellow sticky note with a quick scribble in blue pen, one corner curling up."""
    c = (32, 32)
    yellow = ("#fff6a8", "#fbe45c", "#e4c63c", "#b8962a")
    sq = [(9, 9), (55, 9), (55, 44), (44, 56), (9, 56)]
    b.poly(rot(sq, -7, c), yellow[1])
    b.poly(rot([(9, 9), (55, 9), (55, 17), (9, 17)], -7, c), yellow[2])                    # the gummed strip along the top
    b.poly(rot([(9, 17), (30, 17), (22, 44), (9, 50)], -7, c), mix(yellow[1], yellow[0], 0.6))       # it bows a little: lighter toward the sun
    b.poly(rot([(40, 44), (55, 30), (55, 44), (44, 56), (30, 56)], -7, c), mix(yellow[1], yellow[2], 0.55))   # and darker where the corner lifts
    curl = rot([(55, 44), (44, 56), (42.6, 45.4)], -7, c)    # the curling corner: its pale underside, its shadow
    l.poly(rot([(55, 44), (44, 56), (46.6, 57.4), (57, 46.6)], -7, c), yellow[3], 0.9)
    l.poly(curl, "#fffbd0")
    l.line([curl[0], curl[2], curl[1]], yellow[3], 1.0, 0.8)
    pen = "#2a48a4"
    rows = [(15, 25, 47, 4.4, 0.0), (15, 33, 44, 5.0, 1.3), (15, 41, 33, 4.6, 2.2)]
    for (x0, y0, x1, wave, phase) in rows:                   # writing nobody can read
        pts = []
        steps = int((x1 - x0) * 1.5)
        for i in range(steps + 1):
            x = lerp(x0, x1, i / steps)
            y = y0 + math.sin(x * 1.45 + phase) * 2.1 * (0.55 + 0.45 * math.sin(x * 0.37 + phase * 2)) + (x - x0) * 0.02
            pts.append((x + math.cos(x * 1.45 + phase) * 0.9, y))
        l.line(rot(pts, -7, c), pen, 1.5)
    l.line(rot(curve([(14.6, 48.6), (24, 47.4), (33, 49.6), (38, 47.2)], 5), -7, c), pen, 1.3)        # and underlined
    l.line(rot([(55, 9), (55, 44)], -7, c), yellow[3], 1.0, 0.7)


def phone(b, l):
    """The boy's phone, dead: a dark blank screen in a silver frame, one small crack in a corner of the glass."""
    c, deg = (32.0, 32.0), 13
    T = lambda pts: rot(pts, deg, c)
    metal = ("#f2f5f8", "#b9c2cc", "#7c8794", "#3c424e")
    b.poly(T(rrect(33.5, 33.6, 16.4, 27.6, 6.0)), metal[3])                       # its thickness, on the shadow side
    b.poly(T(rrect(32, 32, 16.4, 27.6, 6.0)), metal[1])                           # the frame
    b.poly(T(rrect(31.3, 31.3, 15.6, 26.8, 5.6)), metal[0])
    b.poly(T(rrect(32, 32, 14.2, 25.4, 4.4)), "#14161d")                          # the glass, black to its edge
    b.poly(T(rrect(32, 32.6, 12.6, 21.4, 2.2)), "#1b2434")                        # the screen: nothing on it
    b.poly(T([(19.6, 11.4), (33.6, 11.4), (19.6, 39.6)]), "#2b3a54")              # the sky in the glass
    b.poly(T([(19.6, 43.6), (37.6, 11.4), (41.0, 11.4), (19.6, 49.6)]), "#232f45")
    l.line(T([(27.6, 8.4), (36.4, 8.4)]), "#05060a", 1.5)                         # the slot it speaks through
    l.line(T([(27.8, 9.3), (36.2, 9.3)]), "#4a5262", 0.7, 0.8)
    px, py = T([(39.6, 8.4)])[0]
    l.ellipse(px, py, 1.1, 1.1, "#3b5078")
    l.line(T([(48.5, 22.0), (48.5, 31.0)]), metal[2], 1.7)                        # a button on its edge
    l.line(T([(48.0, 22.2), (48.0, 30.8)]), metal[0], 0.7, 0.9)
    crack = "#dfe8f2"                                                             # one small crack, in from the corner
    l.line(T([(44.4, 53.6), (41.4, 50.0), (38.4, 49.0), (36.2, 46.0)]), crack, 1.0)
    l.line(T([(41.4, 50.0), (41.8, 46.2)]), crack, 0.8, 0.9)
    edge = T(rrect(32, 32, 14.2, 25.4, 4.4))
    l.line(edge + edge[:1], "#05060a", 0.8, 0.8)
    rim = T(rrect(31.3, 31.3, 15.6, 26.8, 5.6))
    l.line(rim[14:28] + rim[:1], "#ffffff", 1.1, 0.9)                             # the sun along its top and left


def quarter(b, l):
    """A quarter out of a pocket: a plain grey coin lying at a tilt, its milled edge toward us, a plain man's head
    on it and marks round the rim that are not letters."""
    grey = ("#e2e2dd", "#c0c0ba", "#a6a6a1", "#85857f", "#55555a")              # a duller, warmer grey than the Roman silver
    cx, cy, rx, ry, deg, thick = 32.0, 28.6, 27.4, 21.4, -9, 5.4
    T = lambda pts: rot(pts, deg, (cx, cy))
    face = oval(cx, cy, rx, ry, deg, 40)
    b.poly([(x, y + thick) for x, y in face], grey[3])                            # the edge of it
    b.poly(face, grey[1])                                                         # the raised rim
    b.poly(oval(cx, cy, rx - 3.4, ry - 2.8, deg, 40), grey[2])                    # the field
    b.poly(T(loop([(cx + 6, cy - 15), (cx + 17, cy - 9), (cx + 22, cy + 1), (cx + 17, cy + 11), (cx + 6, cy + 16), (cx + 13, cy + 8), (cx + 15, cy - 1), (cx + 12, cy - 9)], 5)), grey[3])
    k = ry / rx                                                                   # the head lies in the coin's own tilt
    H = lambda pts: T([(cx + x, cy + y * k) for x, y in pts])
    head = [(9.6, 19.0), (10.2, 10.0), (13.0, 2.0), (12.6, -7.0), (8.6, -14.0), (1.0, -17.0), (-6.4, -15.0), (-9.6, -10.0), (-10.4, -5.4), (-9.6, -3.6),
            (-14.4, 2.0), (-11.4, 3.2), (-12.0, 5.0), (-10.6, 6.0), (-11.4, 7.8), (-10.6, 11.2), (-6.6, 13.4), (-3.6, 12.8), (-3.2, 16.0), (-8.0, 21.0), (1.0, 23.0)]
    b.poly(H([(x + 1.0, y + 1.3) for x, y in head]), grey[3])                     # low relief: a thin shadow under it
    b.poly(H(head), mix(grey[1], grey[2], 0.35))
    b.poly(H([(12.6, -7.0), (8.6, -14.0), (1.0, -17.0), (-6.4, -15.0), (-4.0, -11.0), (0.6, -9.6), (2.6, -4.6), (6.0, -1.0), (7.0, 6.0), (10.2, 10.0), (13.0, 2.0)]), mix(grey[2], grey[3], 0.7))      # his hair, brushed back
    l.line(H(head[4:8]), grey[0], 0.9, 0.9)                                       # the light along the crown
    l.line(H(head[7:18]), grey[4], 1.0, 0.85)                                     # the profile itself: the one firm line on it
    l.line(H([(-9.6, -5.2), (-6.6, -5.6)]), grey[4], 1.2, 0.9)                    # brow, eye, mouth: plain marks
    l.line(H([(-8.2, -3.2), (-6.6, -3.2)]), grey[4], 1.0, 0.9)
    l.line(H([(-10.6, 6.0), (-8.0, 6.4)]), grey[4], 1.0, 0.9)
    l.line(H(curve([(2.6, -1.6), (4.6, 0.6), (3.4, 3.6), (1.6, 2.2)], 4)), grey[4], 0.9, 0.8)
    for (x0, y0, x1, y1) in ((2.0, -14.6, 6.0, -8.6), (7.6, -11.6, 9.0, -4.0), (5.4, -5.0, 9.6, 3.0)):
        l.line(H([(x0, y0), (x1, y1)]), grey[3], 0.8, 0.8)
    for a in list(range(200, 341, 14)) + list(range(66, 115, 12)):                # where the words and the year would be: blank blocks
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        p0 = (cx + ca * (rx - 4.6), cy + sa * (ry - 3.8))
        p1 = (cx + ca * (rx - 7.4), cy + sa * (ry - 6.2))
        l.line(T([p0, p1]), grey[4], 1.5, 0.75)
    for i in range(27):                                                           # the milling of the edge
        a = math.radians(8 + i * 164 / 26)
        x, y = T([(cx + math.cos(a) * rx, cy + math.sin(a) * ry)])[0]
        l.line([(x, y + 0.6), (x, y + thick - 0.3)], grey[4] if i % 2 else grey[1], 0.9, 0.9)
    l.line(face[0:21], grey[4], 1.0, 0.6)                                         # the rim's near lip
    l.line(face[21:36], grey[0], 1.2, 0.9)                                        # and its far one, in the light
    inner = oval(cx, cy, rx - 3.4, ry - 2.8, deg, 40)
    l.line(inner[21:36], grey[3], 0.9, 0.7)
    l.line(inner[1:19], grey[0], 0.8, 0.6)


def gum(b, l):
    """Half a pack of chewing gum: a green paper sleeve torn open, the foil inside it, two sticks pushed up out of the end."""
    ax, ay, ux, uy = 6.0, 55.5, 0.74, -0.673                 # the closed end of the pack, and the way it points
    nx, ny = -uy, ux                                         # across it, toward the shadow side
    ex, ey = 0.8, 5.2                                        # how its thickness shows

    def at(t, w, down=0.0):
        return (ax + ux * t + nx * w + ex * down, ay + uy * t + ny * w + ey * down)

    foil = ("#ffffff", "#e9eef3", "#bcc7d2", "#8996a6", "#5d6878")
    green = ("#9be6b0", "#48b874", "#2e8a52", "#1f6a3e")
    W = 8.6
    # the far stick, then the near one: each a flat strip of foil with a pinked end
    for (t0, t1, w0, w1, half, tone, lit) in ((22, 55.0, -3.4, -5.2, 5.2, foil[2], foil[1]), (22, 48.5, 3.2, 5.0, 5.2, foil[1], foil[0])):
        teeth = [at(t1 + (1.6 if i % 2 else 0.0), lerp(w1 - half, w1 + half, i / 6)) for i in range(7)]
        b.poly([at(t0, w0 - half, 0.34), at(t1, w1 - half, 0.34)] + [(x + ex * 0.34, y + ey * 0.34) for x, y in teeth] + [at(t0, w0 + half, 0.34)], foil[4])      # its thin edge
        b.poly([at(t0, w0 - half), at(t1, w1 - half)] + teeth + [at(t0, w0 + half)], tone)
        b.poly([at(t0, w0 - half), at(t1, w1 - half), at(t1, w1 - half + 3.4), at(t0, w0 - half + 3.4)], lit)
        l.line([at(t0 + 14, w0 + half - 1.4), at(t1 - 1.0, w1 + half - 1.6)], foil[3], 0.9, 0.7)
        l.line([at(t0 + 12, w0 - half + 1.2), at(t1 - 1.5, w1 - half + 1.2)], foil[0], 1.0, 0.95)
        l.line(teeth, foil[3], 0.8, 0.8)
        for t in (t1 - 7.0, t1 - 13.0):                                           # the creases of its wrapping
            l.line([at(t, w1 - half + 1.0), at(t + 1.2, w1 + half - 1.0)], foil[3], 0.7, 0.55)
    # the foil the pack is lined with, torn and crumpled at the open end
    b.poly([at(26, -W + 0.8), at(37.0, -W + 1.4), at(35.0, -W * 0.45), at(38.4, -0.6), at(35.6, W * 0.4), at(37.6, W - 0.6), at(26, W - 0.8)], foil[2])
    b.poly([at(26, -W + 0.8), at(37.0, -W + 1.4), at(35.0, -W * 0.45), at(36.4, -1.6), at(26, -1.6)], foil[1])
    for (t, w) in ((33.6, -5.4), (34.6, 2.4), (33.0, 5.6)):
        l.line([at(t, w), at(t + 2.6, w + 1.4)], foil[3], 0.8, 0.7)
    # the paper sleeve: its end toward us, its side, its top
    b.poly([at(0, -W), at(0, W), at(0, W, 1), at(0, -W, 1)], green[3])
    b.poly([at(0, W), at(31.0, W), at(31.0, W, 1), at(0, W, 1)], green[2])
    tear = [at(30.0, -W), at(32.6, -W * 0.62), at(30.6, -W * 0.24), at(33.0, W * 0.16), at(30.8, W * 0.58), at(32.4, W)]
    b.poly([at(0, -W)] + tear + [at(0, W)], green[1])
    b.poly([at(0, -W), at(30.0, -W), at(30.6, -W + 3.0), at(0, -W + 3.0)], green[0])                               # the top's far edge, in the sun
    b.poly(loop([at(5.0, -3.6), at(9.0, -5.2), at(22.0, -5.2), at(26.0, -3.6), at(26.0, 3.6), at(22.0, 5.2), at(9.0, 5.2), at(5.0, 3.6)], 3), "#f6fbf2")     # a blank white patch where a name would be
    for (t, w, turn) in ((12.6, -0.6, 1), (18.4, 0.6, -1)):                                                        # two mint leaves on it, and no word
        leaf = [at(t - 3.4, w - 1.6 * turn), at(t, w - 2.8 * turn), at(t + 3.4, w - 0.4 * turn), at(t, w + 1.2 * turn)]
        l.poly(loop(leaf, 3), green[1])
        l.line([at(t - 3.0, w - 1.4 * turn), at(t + 3.0, w - 0.4 * turn)], green[3], 0.7, 0.8)
    l.line([at(2.6, -W + 0.4), at(2.6, W - 0.4)], green[3], 1.1, 0.75)                                             # a dark band at the closed end
    l.line(tear, "#f6fbf2", 1.0, 0.9)                                                                              # the torn edge shows the paper's white
    l.line([at(0, W), at(31.4, W)], green[0], 0.8, 0.7)
    l.line([at(0, W, 1), at(31.0, W, 1)], green[3], 1.0, 0.8)
    l.line([at(0, -W), at(0, W), at(0, W, 1)], green[3], 0.9, 0.6)


def _hole(b, points):
    """Cut a hole right through what is on the base sheet (a keyhole for a ring, the eye of a tag)."""
    b.poly(points, "#000000", 0.0)


def _cord(l, points, light, dark, width=1.3):
    """A string or cord: its darker edge first, then its lit middle."""
    l.line(points, dark, width + 1.0)
    l.line(points, light, width)


def studykey(b, l):
    """The key to Dad's study: an ordinary brass door key on a loop of white string, with a little paper tag
    that somebody has pencilled something on."""
    brass = ("#fbe894", "#dfb244", "#a97c26", "#6a4a14")
    ox, oy, dx, dy = 10.6, 11.6, 0.788, 0.616                # the round end of the key, and the way it points
    K = lambda pts: [(ox + dx * x - dy * y, oy + dy * x + dx * y) for x, y in pts]
    bow = [(0.6, 0), (2.2, -7.4), (8.2, -10.6), (15.4, -9.8), (20.2, -5.8), (22.0, -4.8), (22.0, 4.8), (20.2, 5.8), (15.4, 9.8), (8.2, 10.6), (2.2, 7.4)]
    cuts = [(51.6, 1.4), (49.4, 4.0), (47.0, 1.0), (44.6, 4.6), (41.6, 0.2), (38.6, 4.6), (36.2, 2.0), (33.6, 4.6), (30.6, 0.6), (27.6, 4.6), (25.5, 4.6)]
    blade = [(20.6, -4.8), (25.5, -4.6), (50.2, -4.6), (53.4, -1.2)] + cuts + [(20.6, 4.8)]
    b.poly(K(blade), brass[1])
    b.poly(K([(20.6, -4.8), (25.5, -4.6), (50.2, -4.6), (52.0, -2.7), (25.5, -2.6), (20.6, -2.8)]), brass[0])       # the back of the blade catches the light
    b.poly(K([(25.5, 1.4), (51.6, 1.4)] + cuts), brass[2])                                                            # the cut edge is in shade
    b.poly(loop(K(bow), 5), brass[1])
    b.poly(loop(K([(0.6, 0), (2.2, -7.4), (8.2, -10.6), (15.4, -9.8), (12.0, -6.4), (7.6, -5.6), (4.6, -1.6), (4.4, 3.4), (2.2, 7.4)]), 5), brass[0])     # the bow's rim, toward the sun
    b.poly(loop(K([(15.4, 9.8), (20.2, 5.8), (22.0, 4.8), (22.0, -1.0), (18.6, 3.2), (14.0, 6.8), (8.2, 8.2), (8.2, 10.6)]), 5), brass[2])               # and away from it
    hole = K(oval(6.6, 0.0, 3.2, 3.2))
    _hole(b, hole)
    l.line(K([(24.6, -0.9), (50.4, -0.9)]), brass[3], 1.2, 0.85)                                                      # the groove down the blade
    l.line(K([(24.6, -2.0), (50.0, -2.0)]), brass[0], 0.8, 0.9)
    l.line(K([(21.6, -4.8), (21.6, 4.8)]), brass[3], 1.0, 0.7)                                                        # the shoulder
    l.line(K([(25.5, 4.6)] + cuts[::-1]), brass[3], 0.8, 0.7)                                                         # the cuts, crisp
    l.line(K([(12.6, -2.6), (17.4, -2.6)]), brass[3], 1.0, 0.6)                                                       # two worn marks where a maker's name was
    l.line(K([(12.6, 0.6), (16.0, 0.6)]), brass[3], 1.0, 0.6)
    ring = loop(K(bow), 5)
    l.line(ring[38:] + ring[:12], brass[0], 1.0, 0.9)
    l.line(hole[8:20], brass[3], 0.9, 0.8)                                                                            # the near wall of the hole is in its own shade
    # the tag, of buff paper, its corners clipped, an eyelet at the top
    ex, ey = 13.6, 40.4
    Tg = lambda pts: rot([(ex + x, ey + y) for x, y in pts], -11, (ex, ey))
    paper = ("#fdf3d2", "#efdcaa", "#c9b27e", "#8c7650")
    tag = [(-4.2, -3.4), (4.2, -3.4), (7.6, 0.6), (7.6, 18.4), (-7.6, 18.4), (-7.6, 0.6)]
    b.poly(Tg(tag), paper[1])
    b.poly(Tg([(-4.2, -3.4), (4.2, -3.4), (5.6, -1.8), (-7.6, 12.0), (-7.6, 0.6)]), paper[0])
    b.poly(Tg([(7.6, 9.0), (7.6, 18.4), (-2.0, 18.4)]), paper[2])
    b.poly(Tg(oval(0, 0.4, 2.7, 2.7)), "#b0703a")            # the eyelet's patch
    _hole(b, Tg(oval(0, 0.4, 1.2, 1.2)))
    for (y, x0, x1, ph) in ((7.4, -4.8, 4.8, 0.0), (11.4, -4.8, 2.4, 1.7)):                                           # what is pencilled on it: not to be read
        pts = [(lerp(x0, x1, i / 12), y + math.sin(i * 1.9 + ph) * 1.0) for i in range(13)]
        l.line(Tg(pts), "#5c554e", 1.0, 0.9)
    l.line(Tg([(-5.0, 15.0), (1.0, 14.6)]), "#5c554e", 0.9, 0.7)
    l.line(Tg([(7.6, 0.6), (7.6, 18.4), (-7.6, 18.4)]), paper[3], 0.9, 0.7)
    # the string: a loop through the key and through the tag, knotted
    eye = Tg([(0, 0.4)])[0]
    hx, hy = K([(6.6, 0.0)])[0]
    string = ("#fff3d0", "#a58c5e")                          # kitchen string: soft, a little yellow, never quite straight
    _cord(l, curve([(hx - 0.6, hy + 0.4), (9.6, 20.6), (7.0, 25.6), (8.6, 31.0), (10.6, 35.4), (eye[0] - 1.0, eye[1] - 0.6)], 5), *string, width=1.2)
    _cord(l, curve([(hx + 0.8, hy + 0.6), (15.4, 21.6), (17.6, 26.4), (16.4, 31.4), (17.2, 35.6), (eye[0] + 0.8, eye[1] - 0.4)], 5), *string, width=1.2)
    l.poly(oval(eye[0] + 0.3, eye[1] - 3.3, 2.6, 2.2), string[1])                                                    # the knot, and its two ends
    l.poly(oval(eye[0], eye[1] - 3.7, 1.8, 1.5), string[0])
    _cord(l, curve([(eye[0] + 1.2, eye[1] - 3.6), (eye[0] + 4.4, eye[1] - 6.4), (eye[0] + 6.6, eye[1] - 5.4)], 4), *string, width=1.0)
    _cord(l, curve([(eye[0] - 1.2, eye[1] - 3.2), (eye[0] - 4.2, eye[1] - 2.6), (eye[0] - 5.6, eye[1] - 0.2)], 4), *string, width=1.0)


def lilflash(b, l):
    """Little Sister's flashlight: short and fat, pink, with a yellow head, a big rubber button, a wrist cord,
    and the stickers she has put on it."""
    c, deg = (32.0, 33.0), -17
    T = lambda pts: rot(pts, deg, c)
    pink = ("#ffc0dc", "#f67fb6", "#c44e8e", "#8c2f64")
    yellow = ("#fff39a", "#ffd43c", "#dc9a2a", "#9a6618")
    teal = ("#a2f4ea", "#34c4be", "#1d8c8e", "#12585e")
    # the wrist cord, from the tail
    cord = T(curve([(7.4, 34.0), (3.4, 37.6), (2.8, 45.0), (7.4, 50.4), (12.6, 49.0), (12.4, 43.6), (9.0, 38.6), (7.6, 34.6)], 6))
    l.line(cord, teal[3], 3.2)
    l.line(cord, teal[1], 2.0)
    l.line([(x - 0.5, y - 0.5) for x, y in cord[4:20]], teal[0], 0.8, 0.9)
    # the barrel
    barrel = [(11, 21.5), (37.5, 21.5), (37.5, 44.5), (11, 44.5)]
    tail = loop([(11.4, 21.5), (11.4, 44.5), (7.6, 41.8), (6.0, 33), (7.6, 24.2)], 5)
    b.poly(T(tail), pink[1])
    b.poly(T(barrel), pink[1])
    b.poly(T([(8.6, 23.4), (11, 21.5), (37.5, 21.5), (37.5, 27.4), (10, 27.4), (7.2, 28.6)]), pink[0])               # the top of it, in the light
    b.poly(T([(7.2, 38.6), (10, 39.4), (37.5, 39.4), (37.5, 44.5), (11, 44.5), (8.4, 42.6)]), pink[2])               # its underside
    # the head: yellow, flaring to a wide rim
    b.poly(T([(37.5, 21.5), (45.5, 17.0), (51.5, 17.0), (51.5, 49.0), (45.5, 49.0), (37.5, 44.5)]), yellow[1])
    b.poly(T([(37.5, 21.5), (45.5, 17.0), (51.5, 17.0), (51.5, 23.6), (45.5, 23.6), (37.5, 27.4)]), yellow[0])
    b.poly(T([(37.5, 39.4), (45.5, 42.6), (51.5, 42.6), (51.5, 49.0), (45.5, 49.0), (37.5, 44.5)]), yellow[2])
    b.poly(T(oval(51.6, 33.0, 4.3, 16.0)), yellow[2])        # the rim, and the lens in it
    l.poly(T(oval(52.2, 33.0, 3.2, 13.4)), "#fffadc")
    l.poly(T(oval(52.6, 35.4, 2.0, 8.6)), "#ffe49a")
    l.poly(T(oval(51.6, 26.0, 1.3, 3.6)), "#ffffff")
    rim = T(oval(51.6, 33.0, 4.3, 16.0))
    l.line(rim[10:24], yellow[3], 1.0, 0.8)
    l.line(T([(45.5, 17.2), (45.5, 48.8)]), yellow[3], 1.0, 0.6)
    l.line(T([(37.5, 21.6), (37.5, 44.4)]), pink[3], 1.1, 0.8)                                                       # where the head screws on
    l.line(T([(12.6, 22.6), (36.0, 22.6)]), "#ffffff", 1.1, 0.75)                                                    # a shine along the top
    l.line(T([(13.0, 21.8), (13.0, 44.2)]), pink[2], 1.0, 0.6)
    # the button: big, round, rubbery, standing well up out of the barrel
    b.poly(T(loop([(15.6, 23.0), (16.6, 16.8), (23.0, 13.8), (29.4, 16.8), (30.4, 23.0), (23.0, 24.6)], 5)), teal[1])
    b.poly(T(loop([(17.0, 20.6), (18.0, 16.8), (22.6, 14.6), (26.6, 15.8), (22.6, 17.6), (19.6, 21.4)], 5)), teal[0])
    b.poly(T(loop([(26.4, 23.6), (30.2, 22.6), (29.4, 17.6), (27.6, 20.6)], 4)), teal[2])
    l.line(T(curve([(15.4, 23.4), (23.0, 25.4), (30.6, 23.4)], 5)), teal[3], 1.2, 0.9)
    l.ellipse(*T([(20.2, 17.2)])[0], 1.3, 1.0, "#ffffff")
    # her stickers: a star and a heart
    star = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        r = 5.2 if i % 2 == 0 else 2.2
        star.append((20.6 + math.cos(a) * r, 34.2 + math.sin(a) * r))
    l.poly(T(rot(star, 12, (20.6, 34.2))), "#b86a1a")
    l.poly(T(rot([(20.6 + (x - 20.6) * 0.8, 34.2 + (y - 34.2) * 0.8) for x, y in star], 12, (20.6, 34.2))), "#fff6a8")
    heart = [(31.0, 38.4), (27.2, 34.4), (27.4, 31.8), (29.4, 30.8), (31.0, 32.4), (32.6, 30.8), (34.6, 31.8), (34.8, 34.4)]
    l.poly(T(rot(loop(heart, 4), -10, (31.0, 34.4))), "#e2364c")
    l.ellipse(*T([(29.2, 32.6)])[0], 0.9, 0.8, "#ffb4be")
    for run in ([(40.6, 30.4), (44.0, 28.6)], [(41.6, 38.0), (43.6, 39.6)], [(15.0, 30.0), (16.6, 31.4)]):          # scuffs: it has been everywhere with her
        l.line(T(run), "#fff8e0", 0.8, 0.7)


def pencil(b, l):
    """Dad's crossword pencil: yellow, six-sided, bitten ragged below the metal, the pink eraser worn to a slant."""
    ax, ay, ux, uy = 7.6, 57.4, 0.700, -0.714                # its point, and the way it lies
    nx, ny = -uy, ux                                         # across it, toward the shadow side
    at = lambda t, w: (ax + ux * t + nx * w, ay + uy * t + ny * w)
    H = 5.5
    yellow = ("#fff07a", "#f9cb36", "#c9941e", "#8a6212")
    wood = ("#f6dcb0", "#dfb884", "#b08a5c")
    facets = ((-H, -H + 3.6, 0), (-H + 3.6, H - 3.4, 1), (H - 3.4, H, 2))
    # the sharpened end: bare wood, and the lead
    b.poly([at(3.2, -1.2), at(14.4, -H), at(14.4, H), at(3.2, 1.2)], wood[1])
    b.poly([at(3.2, -1.2), at(14.4, -H), at(14.4, -H + 3.6), at(3.2, -0.3)], wood[0])
    b.poly([at(3.2, 0.4), at(14.4, H - 3.4), at(14.4, H), at(3.2, 1.2)], wood[2])
    b.poly([at(-0.6, 0.1), at(3.6, -1.4), at(3.6, 1.4)], "#33333c")
    l.line([at(0.6, -0.3), at(3.2, -1.0)], "#8a8a96", 0.7, 0.9)
    # the six sides, of which we see three
    for (w0, w1, k) in facets:
        b.poly([at(14.2, w0), at(55.2, w0), at(55.2, w1), at(14.2, w1)], yellow[k])
        b.poly(loop([at(14.6, w0), at(13.0, lerp(w0, w1, 0.25)), at(11.0, (w0 + w1) / 2), at(13.0, lerp(w0, w1, 0.75)), at(14.6, w1)], 3), yellow[k])   # the paint runs to a point on each
    l.line([at(14.4, -H + 3.6), at(55.0, -H + 3.6)], yellow[2], 0.8, 0.6)
    l.line([at(14.4, H - 3.4), at(55.0, H - 3.4)], yellow[3], 0.8, 0.5)
    l.line([at(14.6, -H + 0.7), at(37.0, -H + 0.7)], "#fffbd2", 0.9, 0.9)
    for t in (21.0, 23.8, 26.4, 29.4):                       # what is left of the gilt stamp
        l.line([at(t, -0.8), at(t + 1.4, -0.8)], "#6f6a3c", 1.6, 0.55)
    # the metal band and the eraser
    b.poly([at(55.0, -H - 0.4), at(62.4, -H - 0.4), at(62.4, H + 0.4), at(55.0, H + 0.4)], "#b9c0a8")
    b.poly([at(55.0, -H - 0.4), at(62.4, -H - 0.4), at(62.4, -H + 3.2), at(55.0, -H + 3.2)], "#f2f5e6")
    b.poly([at(55.0, H - 3.0), at(62.4, H - 3.0), at(62.4, H + 0.4), at(55.0, H + 0.4)], "#7c846c")
    for t in (56.3, 57.9, 59.8, 61.3):
        l.line([at(t, -H - 0.4), at(t, H + 0.4)], "#565c4a", 0.8, 0.85)
    rubber = ("#ffc2cc", "#f08ca0", "#b95c74")
    b.poly(loop([at(62.2, -H + 0.2), at(67.0, -H + 0.2), at(69.8, -2.8), at(70.2, 0.8), at(67.8, 4.2), at(65.4, H - 0.2), at(62.2, H - 0.2)], 4), rubber[1])
    b.poly(loop([at(62.2, -H + 0.2), at(67.0, -H + 0.2), at(69.0, -3.4), at(66.0, -1.8), at(62.2, -1.8)], 4), rubber[0])
    b.poly(loop([at(62.2, 2.4), at(67.2, 2.2), at(67.8, 4.2), at(65.4, H - 0.2), at(62.2, H - 0.2)], 4), rubber[2])
    b.poly(loop([at(68.2, -3.8), at(69.8, -2.8), at(70.2, 0.8), at(68.6, 3.0), at(68.0, 0.0)], 4), "#9a7880")        # rubbed grey with graphite
    # he chews it while he thinks: the paint bitten off in dents, the wood showing
    for (t, w, r, turn) in ((40.4, -3.6, 2.2, 20), (45.4, -0.8, 2.6, -15), (50.6, -3.8, 2.0, 35), (43.0, 3.0, 2.2, 10), (48.6, 2.0, 2.4, -30), (52.6, -0.6, 1.8, 15), (37.4, 0.6, 1.6, 0)):
        cx, cy = at(t, w)
        ang = math.degrees(math.atan2(uy, ux)) + turn
        l.poly(oval(cx + 0.6, cy + 0.6, r * 1.25, r * 0.74, ang, 10), yellow[3])
        l.poly(oval(cx, cy, r * 1.15, r * 0.62, ang, 10), wood[0] if w < 1 else wood[1])
    for (t, w, d) in ((43.6, -H, 1.9), (49.6, -H, 1.7), (46.6, H, 1.9), (52.2, H, 1.6), (39.6, H, 1.4)):                # and nicked all along its edges
        s = 1 if w > 0 else -1
        _hole(b, [at(t - 1.9, w + s * 1.5), at(t, w - s * d), at(t + 1.9, w + s * 1.5)])
    l.line([at(55.8, -2.0), at(57.6, 1.6)], "#565c4a", 1.3, 0.8)                                                      # a tooth mark in the metal too


def carkey(b, l):
    """The spare key to the wagon: a black plastic head, a steel blade with a groove milled down it, a plain split
    ring, and a small red tag with a paper label nobody can read."""
    ox, oy, dx, dy = 41.6, 15.6, -0.738, 0.675               # the top of its head, and the way the blade points
    K = lambda pts: [(ox + dx * x - dy * y, oy + dy * x + dx * y) for x, y in pts]       # (across the key, +y is the side toward the sun)
    black = ("#9298a6", "#535763", "#2b2d36", "#131419")
    steel = ("#ffffff", "#d3dae1", "#98a2ae", "#58616d")
    # the blade
    b.poly(K([(20.0, -3.5), (47.4, -3.5), (50.8, -1.5), (51.4, 0.7), (49.6, 2.9), (47.4, 3.5), (20.0, 3.5)]), steel[1])
    b.poly(K([(20.0, 1.6), (48.4, 1.6), (49.6, 2.9), (47.4, 3.5), (20.0, 3.5)]), steel[0])
    b.poly(K([(20.0, -3.5), (47.4, -3.5), (50.0, -2.0), (20.0, -1.8)]), steel[2])
    groove = curve([(22.6, 0.2), (27.0, -0.9), (31.0, 0.7), (35.0, -0.9), (39.0, 0.6), (43.0, -0.8), (47.4, 0.0)], 5)
    l.line(K(groove), steel[3], 1.3, 0.9)                                                                             # milled, not cut: a modern key
    l.line(K([(x, y + 0.9) for x, y in groove]), steel[0], 0.7, 0.9)
    # the head: a lug at the top for the ring, then the grip
    lug = loop(K([(2.0, -4.6), (-2.6, -4.0), (-4.6, 0.0), (-2.6, 4.0), (2.0, 4.6)]), 4)
    b.poly(lug, black[1])
    head = [(0.4, -7.4), (3.0, -11.0), (9.0, -11.6), (17.0, -9.4), (22.4, -6.6), (22.4, 6.6), (17.0, 9.4), (9.0, 11.6), (3.0, 11.0), (0.4, 7.4)]
    b.poly(loop(K(head), 5), black[1])
    b.poly(loop(K([(0.4, 7.4), (3.0, 11.0), (9.0, 11.6), (17.0, 9.4), (22.4, 6.6), (22.4, 3.6), (16.6, 6.2), (9.0, 8.0), (4.4, 7.4), (2.8, 3.8)]), 5), black[0])    # the edge toward the sun
    b.poly(loop(K([(0.4, -7.4), (3.0, -11.0), (9.0, -11.6), (17.0, -9.4), (22.4, -6.6), (22.4, -4.0), (16.6, -6.6), (9.0, -8.4), (4.4, -7.8), (2.8, -3.8)]), 5), black[2])
    b.poly(loop(K([(6.6, -4.8), (16.4, -4.4), (19.6, -2.4), (19.6, 2.4), (16.4, 4.4), (6.6, 4.8)]), 4), black[3])                                                  # a grip moulded in it
    for x in (8.6, 11.6, 14.6, 17.4):
        l.line(K([(x, -3.6), (x, 3.6)]), black[0], 1.1, 0.75)
    l.line(K([(5.0, 8.4), (15.0, 9.0)]), "#e6eaf2", 1.0, 0.8)                                                         # a shine on its shoulder
    hole = K(oval(-1.6, 0.0, 1.9, 1.9))
    _hole(b, hole)
    l.line(K([(22.4, -6.4), (22.4, 6.4)]), black[3], 1.1, 0.8)
    l.line(lug[14:], black[0], 0.9, 0.8)
    # the ring, through the lug, and the tag on it
    hx, hy = K([(-1.6, 0.0)])[0]
    rx, ry = hx + 6.6, hy + 6.2
    ring = oval(rx, ry, 8.8, 9.0, 0, 32)
    l.line(ring + ring[:1], steel[3], 2.6)
    l.line(ring + ring[:1], steel[1], 1.4)
    l.line(ring[16:27], steel[0], 0.9, 0.95)
    ex, ey = rx + 0.6, ry + 9.6
    Tg = lambda pts: rot([(ex + x, ey + y) for x, y in pts], 8, (ex, ey))
    red = ("#f58a78", "#d9463c", "#9a2a2c", "#5e1a1e")
    b.poly(Tg(rrect(0, 8.8, 7.0, 11.0, 2.6)), red[1])
    b.poly(Tg([(-7.0, 0.4), (-4.4, -2.2), (2.0, -2.2), (-7.0, 9.0)]), red[0])
    b.poly(Tg([(7.0, 9.4), (7.0, 17.2), (4.4, 19.8), (-2.0, 19.8)]), red[2])
    b.poly(Tg(rrect(0, 10.8, 4.9, 6.8, 1.0)), "#fbf6e6")                                                              # the paper in its window
    _hole(b, Tg(oval(0, 0.4, 1.3, 1.3)))
    for (y, x0, x1, ph) in ((7.8, -3.3, 3.3, 0.6), (10.8, -3.3, 3.3, 2.0), (13.8, -3.3, 0.8, 0.9)):                   # ballpoint: nothing anyone could read
        pts = [(lerp(x0, x1, i / 9), y + math.sin(i * 2.1 + ph) * 0.8) for i in range(10)]
        l.line(Tg(pts), "#3a4a7c", 0.9, 0.9)
    edge = Tg(rrect(0, 10.8, 4.9, 6.8, 1.0))
    l.line(edge + edge[:1], red[2], 0.8, 0.8)
    l.line(ring[4:12], steel[3], 2.6)                                                                                 # the ring again where it comes through the tag
    l.line(ring[4:12], steel[1], 1.4)


def chicken(b, l):
    """GENERAL FEATHERS: Little Sister's favourite stuffed hen, sitting up very straight. White and plump, soft and
    well worn (five times through the wash), a red felt comb gone floppy on one side, an orange felt beak and a red
    wattle, two button eyes of which one is blue (sewn back on, a little too high), and on a ribbon round her neck
    the paper medal she got for bravery. Her head is cocked: she is a little lopsided, and entirely dignified."""
    white = ("#fffdf4", "#f0e9dc", "#d6cdc6", "#aea4ba", "#7e7596")        # wool-white in the sun, going cool and violet in shade
    red = ("#ff7c64", "#e0342c", "#a62028", "#5e1220")
    orange = ("#ffd47c", "#f7a12a", "#c86e18", "#80440e")
    # her tail, pinched up behind
    b.poly(loop([(52.0, 30.0), (56.4, 18.0), (59.6, 12.4), (61.6, 14.6), (61.6, 26.0), (59.8, 37.0), (54.0, 38.0)], 4), white[2])      # two felt feathers: the far one ...
    tail = loop([(44.6, 31.6), (48.0, 20.6), (51.6, 11.6), (55.2, 6.6), (57.8, 9.0), (57.6, 18.0), (58.8, 28.0), (57.6, 37.6), (53.0, 40.6)], 5)
    b.poly(tail, white[1])                                                                                       # ... and the near one
    b.poly(loop([(47.0, 29.6), (50.0, 19.6), (53.2, 11.0), (55.4, 8.0), (55.0, 16.0), (53.6, 26.6), (50.8, 33.0)], 4), white[0])
    # her body: a plump loaf of a hen, lit across the top and the breast
    body = loop([(14.0, 29.0), (9.6, 37.0), (8.6, 45.6), (11.6, 53.4), (19.6, 59.0), (32.0, 61.0), (44.4, 59.4), (53.0, 54.4), (58.2, 46.0), (59.0, 37.0), (56.0, 30.6),
                 (49.0, 28.2), (41.0, 28.6), (32.0, 26.4), (23.0, 26.4)], 5)
    b.poly(body, white[1])
    b.poly(loop([(14.0, 29.0), (9.8, 37.0), (9.2, 44.6), (12.0, 47.8), (16.6, 42.0), (23.0, 36.4), (32.6, 32.4), (44.0, 31.8), (52.6, 33.4), (56.0, 30.6), (49.0, 28.2),
                 (41.0, 28.6), (32.0, 26.4), (23.0, 26.4)], 5), white[0])
    b.poly(loop([(11.8, 53.6), (19.6, 59.0), (32.0, 61.0), (44.4, 59.4), (53.0, 54.4), (58.2, 46.0), (59.0, 38.0), (55.4, 45.6), (48.0, 51.6), (38.0, 54.6), (26.4, 55.4),
                 (17.6, 53.2)], 5), white[2])
    b.poly(loop([(17.0, 58.2), (32.0, 60.6), (44.4, 59.2), (53.0, 54.2), (57.8, 47.0), (52.0, 53.8), (43.0, 57.4), (31.0, 58.2)], 4), white[3])
    b.poly(loop([(15.6, 31.0), (24.0, 28.4), (32.0, 29.6), (27.0, 33.4), (19.0, 36.0), (14.0, 35.0)], 4), white[2], 0.55)                  # the shade her head throws
    # the wing: a felt patch sewn on her side, standing off it a little
    wing = loop([(27.6, 40.4), (30.6, 35.2), (37.4, 33.2), (45.6, 35.0), (52.6, 39.6), (56.4, 47.0), (52.6, 47.4), (50.6, 49.4), (46.6, 48.0), (43.6, 50.0), (39.6, 48.4),
                 (35.6, 49.0), (32.6, 46.8), (29.2, 45.0)], 4)
    b.poly([(x + 0.8, y + 1.8) for x, y in wing], white[3])
    b.poly(wing, white[1])
    b.poly(loop([(28.4, 39.6), (31.2, 35.6), (37.6, 33.8), (45.4, 35.6), (52.0, 39.8), (44.0, 39.2), (36.0, 39.8), (31.0, 42.0)], 4), white[0])
    # her head, cocked a little
    hc = (22.0, 17.6)
    H = lambda pts: rot([(x, y + 0.9) for x, y in pts], 8, (hc[0], hc[1] + 0.9))
    b.poly(H(oval(hc[0], hc[1], 10.8, 10.0, 0, 32)), white[1])
    b.poly(H(loop([(11.6, 17.6), (13.4, 11.2), (19.0, 8.0), (26.2, 8.2), (30.6, 11.2), (24.0, 11.8), (18.0, 14.2), (14.6, 20.6)], 5)), white[0])
    b.poly(H(loop([(32.0, 15.6), (32.6, 21.0), (29.8, 25.4), (23.0, 27.8), (16.4, 26.4), (24.0, 24.2), (29.2, 20.6)], 4)), white[2])
    # the comb: three upright lobes of red felt sewn along her crown, and a fourth that has gone floppy
    lobes = ((16.6, 6.6, 2.5, 3.0, -20), (21.8, 4.8, 2.7, 3.3, -4), (26.9, 5.6, 2.5, 3.0, 14))
    for (x, y, rx, ry, turn) in lobes:
        l.poly(H(oval(x + 0.5, y + 0.5, rx, ry, turn, 20)), red[3])
    l.poly(H(oval(31.2, 9.0, 2.0, 3.2, 58, 20)), red[3])
    l.poly(H(oval(30.8, 8.6, 1.9, 3.0, 58, 20)), red[2])                                                           # the floppy one hangs over in shade
    l.poly(H([(14.8, 9.0), (29.6, 7.6), (29.8, 10.2), (15.2, 11.2)]), red[1])                                      # its base, sewn along the crown
    for (x, y, rx, ry, turn) in lobes:
        l.poly(H(oval(x, y, rx, ry, turn, 20)), red[1])
        l.poly(H(oval(x - 0.7, y - 1.0, rx * 0.5, ry * 0.42, turn, 14)), "#f8604a", 0.85)                          # the felt is matt: only a soft light on each
    l.line(H([(15.2, 10.8), (29.6, 9.8)]), red[3], 0.9, 0.8)
    for (x0, y0, x1, y1) in ((19.2, 6.2, 19.4, 8.2), (24.4, 5.6, 24.4, 7.8)):
        l.line(H([(x0, y0), (x1, y1)]), red[3], 0.8, 0.85)                                                          # the dips between the lobes
    # the ribbon round her neck, and the medal on it: a paper disc cut out with pinking shears, coloured gold in crayon, a star on it
    rib = ("#86e6dc", "#26aaa6", "#167276", "#0e464c")
    for strand in (curve([(12.8, 25.6), (14.0, 30.4), (17.0, 33.8), (20.6, 35.0)], 5), curve([(31.6, 24.0), (30.0, 29.6), (25.8, 33.6), (22.0, 35.0)], 5)):
        l.line(strand, rib[3], 2.6)
        l.line(strand, rib[1], 1.5)
        l.line([(x - 0.4, y - 0.4) for x, y in strand[1:-3]], rib[0], 0.7, 0.7)
    mx, my = 21.2, 39.2
    edge = [(mx + math.cos(a) * (5.0 if i % 2 == 0 else 4.3), my + math.sin(a) * (5.0 if i % 2 == 0 else 4.3)) for i, a in enumerate(np.linspace(0, 2 * math.pi, 24, endpoint=False))]
    l.poly([(x + 0.7, y + 0.9) for x, y in edge], white[4], 0.8)                                                    # it hangs a little off her breast
    l.poly(edge, "#e9a62c")
    l.poly(oval(mx, my, 3.9, 3.9), "#ffd23e")
    l.poly(oval(mx - 1.0, my - 1.1, 2.2, 1.8, -30), "#fff29c")
    star = []
    for i in range(10):
        a = math.radians(-76 + i * 36)                       # drawn in crayon, not quite straight
        star.append((mx + 0.2 + math.cos(a) * (2.6 if i % 2 == 0 else 1.1), my + 0.3 + math.sin(a) * (2.6 if i % 2 == 0 else 1.1)))
    l.poly(star, "#d0542a", 0.95)
    # her face: the orange felt beak, the wattle, and the two buttons
    l.poly(H([(20.0, 18.8), (25.2, 19.6), (23.0, 22.6), (16.0, 23.4)]), orange[1])
    l.poly(H([(20.0, 18.8), (25.2, 19.6), (21.0, 20.8), (16.4, 23.0)]), orange[0])
    l.line(H([(16.6, 23.2), (22.8, 21.8)]), orange[3], 0.8, 0.85)
    wat = H(loop([(20.8, 22.8), (23.2, 23.0), (23.8, 26.4), (22.2, 28.6), (20.2, 27.2), (19.8, 24.4)], 3))
    l.poly(wat, red[1])
    l.poly(H(loop([(20.6, 23.4), (22.0, 23.4), (21.6, 26.0), (20.6, 26.0)], 3)), red[0])
    ex, ey = H([(17.2, 15.8)])[0]                                                                                   # the black one, her own
    l.ellipse(ex, ey, 2.0, 2.1, "#141018")
    l.ellipse(ex - 0.6, ey - 0.7, 0.7, 0.7, "#ffffff")
    bx, by = H([(26.6, 14.0)])[0]                                                                                   # the blue one: a bigger button, sewn on a little high
    l.ellipse(bx + 0.3, by + 0.4, 2.7, 2.7, "#16285e")
    l.ellipse(bx, by, 2.3, 2.3, "#3a74e0")
    l.ellipse(bx - 0.8, by - 0.8, 0.8, 0.7, "#d4e6ff")
    l.line([(bx - 0.4, by + 0.6), (bx + 1.0, by - 0.6)], "#efe8da", 0.6, 0.85)                                       # the thread it was sewn back on with
    # her feet: orange felt, sticking out in front
    for (x, y, turn) in ((14.4, 58.6, -16), (25.2, 59.8, 10)):
        F = lambda pts: rot([(x + px, y + py) for px, py in pts], turn, (x, y))
        l.poly(F([(-3.0, -2.4), (3.0, -2.4), (5.4, 1.4), (3.8, 2.8), (1.4, 2.0), (0.0, 4.0), (-1.4, 2.0), (-3.8, 2.8), (-5.4, 1.2)]), "#ff9418")     # three fat felt toes
        l.poly(F([(-3.0, -2.4), (3.0, -2.4), (4.2, 0.0), (-4.2, 0.0)]), "#ffbe3c")
        for px in (-1.6, 1.4):
            l.line(F([(px * 0.5, 0.6), (px, 2.0)]), orange[2], 0.8, 0.85)
    # the wash: a mended seam on her side, the stitches of the wing, the fluff gone to little pills
    for i in range(4):
        px, py = lerp(41.0, 48.2, i / 3), lerp(53.0, 50.6, i / 3)
        l.line([(px - 0.8, py - 0.8), (px + 0.8, py + 0.8)], "#8a90b4", 0.6, 0.7)
        l.line([(px - 0.8, py + 0.8), (px + 0.8, py - 0.8)], "#8a90b4", 0.6, 0.7)
    w = wing[22:52]
    for i in range(0, len(w) - 2, 3):
        l.line(w[i:i + 2], white[3], 0.8, 0.8)
    l.line(curve([(50.6, 30.6), (52.4, 20.0), (54.6, 11.0)], 4), white[2], 0.8, 0.8)                             # the stitched feathers of her tail
    l.line(curve([(57.6, 9.6), (57.4, 18.0), (58.6, 28.0), (57.8, 36.0)], 4), white[3], 0.9, 0.85)
    for (x, y) in ((33.6, 30.0), (40.0, 30.8), (46.0, 31.6), (13.0, 41.0), (17.4, 47.6), (12.4, 49.4)):
        l.line(curve([(x - 1.8, y - 0.6), (x, y + 0.8), (x + 1.8, y - 0.6)], 3), white[2], 0.7, 0.6)                # a few feathers stitched on her breast and back
    for (x, y) in ((36.2, 51.4), (29.4, 56.2), (50.2, 44.0), (44.0, 55.4), (21.6, 50.4)):
        l.ellipse(x, y, 0.6, 0.55, white[0], 0.8)


def _battery(b, l, c, deg, flip=False, L=35.0, R=4.6):
    """One AA battery lying on its side, middle `c`, its + end pointing `deg` (or the other way if flipped)."""
    ux, uy = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    nx, ny = -uy, ux                                         # across it, toward the shadow side
    s = -1.0 if flip else 1.0
    at = lambda t, w: (c[0] + ux * t * s + nx * w, c[1] + uy * t * s + ny * w)
    wrap = ("#a6c6f4", "#5088dc", "#2f5eb2", "#1d4086", "#112656")              # a plain blue wrapper ...
    band = ("#ffffff", "#eef2f6", "#c2cad4", "#8a95a4", "#525c6a")              # ... silver toward the + end
    metal = ("#ffffff", "#dfe4ea", "#a8b0bc", "#6c7682", "#3c434e")
    h, k0 = L / 2, L / 2 - 10.0
    bands = ((-R, -0.62 * R, 1), (-0.62 * R, -0.18 * R, 0), (-0.18 * R, 0.4 * R, 2), (0.4 * R, 0.78 * R, 3), (0.78 * R, R, 4))
    for (w0, w1, k) in bands:                                # the round of it, in five bands, which the brush softens
        b.poly([at(-h + 0.8, w0), at(k0, w0), at(k0, w1), at(-h + 0.8, w1)], wrap[k])
        b.poly([at(k0, w0), at(h - 1.6, w0), at(h - 1.6, w1), at(k0, w1)], band[k])
    # the ends are made of metal and cut square: restated crisp
    l.poly([at(-h, -R + 0.6), at(-h + 1.0, -R + 0.3), at(-h + 1.0, R - 0.3), at(-h, R - 0.6)], metal[2])       # the flat - end
    l.line([at(-h + 0.3, -R + 0.9), at(-h + 0.3, 0.0)], metal[0], 0.8, 0.9)
    l.poly([at(h - 1.8, -R + 0.2), at(h - 0.3, -R + 0.3), at(h, -R + 0.7), at(h, R - 0.7), at(h - 0.3, R - 0.3), at(h - 1.8, R - 0.2)], metal[2])     # the + end: its shoulder ...
    l.poly([at(h - 1.8, -R + 0.2), at(h - 0.3, -R + 0.3), at(h, -R + 0.7), at(h, -0.5 * R), at(h - 1.8, -0.5 * R)], metal[0])
    l.poly([at(h - 1.8, 0.45 * R), at(h, 0.45 * R), at(h, R - 0.7), at(h - 0.3, R - 0.3), at(h - 1.8, R - 0.2)], metal[3])
    l.poly([at(h - 0.3, -1.9), at(h + 2.2, -1.7), at(h + 2.2, 1.7), at(h - 0.3, 1.9)], metal[2])               # ... and the nub
    l.poly([at(h - 0.3, -1.9), at(h + 2.2, -1.7), at(h + 2.2, -0.5), at(h - 0.3, -0.5)], metal[0])
    l.poly([at(h - 0.3, 0.9), at(h + 2.2, 0.8), at(h + 2.2, 1.7), at(h - 0.3, 1.9)], metal[4])
    l.line([at(k0, -R + 0.3), at(k0, R - 0.3)], wrap[4], 0.8, 0.75)                                              # where the silver meets the blue
    l.line([at(h - 1.7, -R + 0.4), at(h - 1.7, R - 0.4)], metal[4], 0.8, 0.85)
    l.line([at(-h + 2.4, -0.42 * R), at(k0 - 1.4, -0.42 * R)], wrap[0], 1.0, 0.9)                                # the shine along it
    l.line([at(k0 + 1.2, -0.42 * R), at(h - 2.6, -0.42 * R)], band[0], 1.0, 0.95)


def batteries(b, l):
    """Four AA batteries out of Big Sister's sound machine, loose, lying together, one of them turned round: plain
    blue wrappers with a silver end, no name and no words on them."""
    for (cx, cy, deg, flip) in ((23.6, 17.6, -36, False), (27.6, 28.4, -30, False), (34.4, 37.4, -25, True), (40.8, 47.2, -32, False)):
        _battery(b, l, (cx, cy), deg, flip)


ITEMS = dict(reed=reed, map=map_, flashlight=flashlight, rootbeer=rootbeer, shade=shade, carmirror=carmirror, sunglasses=sunglasses,
             coppermirror=coppermirror, toga=toga, tunic=tunic, breakfast=breakfast, incense=incense, coin=coin, note=note)
ITEMS["pass"] = pass_
ITEMS.update(phone=phone, quarter=quarter, gum=gum)
ITEMS.update(studykey=studykey, lilflash=lilflash, pencil=pencil, carkey=carkey)
ITEMS.update(chicken=chicken, batteries=batteries)
ORDER = ["reed", "map", "pass", "flashlight", "rootbeer", "shade", "carmirror", "sunglasses", "coppermirror", "toga", "tunic", "breakfast", "incense", "coin", "note",
         "phone", "quarter", "gum", "studykey", "lilflash", "pencil", "carkey", "chicken", "batteries"]


# ---------------------------------------------------------------- painting one
def paint(name, seed=None, brush=True):
    """-> the picture as floats (64, 64, 4): color and coverage."""
    seed = (sum(ord(ch) for ch in name) if seed is None else seed)
    b, l = Sheet((S, S), ss=6), Sheet((S, S), ss=6)
    ITEMS[name](b, l)
    bc, ba = b.done()
    lc, la = l.done()
    alpha = np.maximum(ba, la)
    inside = bc[ba > 0.9]
    flat = np.empty((S, S, 3), dtype=F32)
    flat[...] = inside.mean(axis=0) if len(inside) else 0.5  # (the brush must not drag a strange color in at the edges)
    solid = bc * ba[..., None] + flat * (1 - ba[..., None])
    for _ in range(3):                                       # spread the thing's own edge colors outward a little
        grown = blur(solid * (ba[..., None] > 0.02), 1.2) / np.maximum(blur((ba > 0.02).astype(F32), 1.2), 1e-3)[..., None]
        solid = np.where(ba[..., None] > 0.5, solid, grown * 0.85 + flat * 0.15)
    pic = strokes(solid.astype(F32), sizes=(4, 2), seed=seed, density=1.7, jitter=0.028, keep=0.58) if brush else solid.copy()
    over(pic, lc, la)
    x, y = grid((S, S))
    soft = blur(alpha, 0.5)
    lee = np.clip(alpha - sample(soft, x + 1.5, y + 1.5), 0, 1)        # the edge away from the light: darker and cooler, and crisp
    sun = np.clip(alpha - sample(soft, x - 1.3, y - 1.3), 0, 1)        # the edge toward it: a touch lighter
    tint(pic, "#3a2a4a", np.clip(lee * 0.85, 0, 1))
    glow(pic, "#fff4d8", np.clip(sun * 0.22, 0, 1))
    pic = grain(np.clip(pic, 0, 1), seed + 3, 0.014)
    return np.dstack([pic, np.clip(alpha, 0, 1)])


def save(name, folder="out/items"):
    rgba = paint(name)
    Image.fromarray((np.clip(rgba, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA").save(f"{folder}/{name}.png", optimize=True)
    return rgba


def sheet(folder="out/items", out="out/items-sheet.png", k=4):
    """Every picture at 4x on a dark and a light ground, and at its real size and at half size underneath."""
    cols = 5 if len(ORDER) <= 20 else 6
    rows = (len(ORDER) + cols - 1) // cols
    cell = S * k + 16
    per = len(ORDER) if len(ORDER) <= 22 else (len(ORDER) + 1) // 2        # how many to a row in the strips underneath
    lines = (len(ORDER) + per - 1) // per
    band = lines * (S + 14 + 32 + 12)
    strip = 2 * band + 8
    im = Image.new("RGB", (cols * cell + 16, rows * (cell + 14) + strip + 16), (40, 34, 44))
    from PIL import ImageDraw
    dr = ImageDraw.Draw(im)
    small_y = rows * (cell + 14) + 12
    grounds = [(40, 34, 44), (222, 204, 164)]
    for g, ground in enumerate(grounds):
        dr.rectangle([0, small_y + g * band, im.size[0], small_y + (g + 1) * band], fill=ground)
    for i, name in enumerate(ORDER):
        pic = Image.open(f"{folder}/{name}.png").convert("RGBA")
        cx, cy = 16 + (i % cols) * cell, 12 + (i // cols) * (cell + 14)
        ground = (58, 50, 62) if (i + i // cols) % 2 == 0 else (212, 196, 160)
        dr.rectangle([cx, cy, cx + S * k - 1, cy + S * k - 1], fill=ground)
        big = pic.resize((S * k, S * k), Image.NEAREST)
        im.paste(big, (cx, cy), big)
        dr.text((cx + 2, cy + S * k + 1), name, fill=(230, 224, 210))
        for g in range(len(grounds)):                        # at real size, and at half size under it, on the dark bar and on a light ground
            y0 = small_y + g * band + (i // per) * (S + 14 + 32 + 12) + 6
            x0 = 12 + (i % per) * ((im.size[0] - 24) // per)
            im.paste(pic, (x0, y0), pic)
            half = pic.resize((32, 32), Image.LANCZOS)
            im.paste(half, (x0 + 16, y0 + S + 6), half)
    im.save(out)
    return out


if __name__ == "__main__":
    os.makedirs("out/items", exist_ok=True)
    names = [n for n in sys.argv[1:] if n in ITEMS] or ORDER
    for n in names:
        save(n)
    if all(os.path.exists(f"out/items/{n}.png") for n in ORDER):
        print(sheet())
    print("painted", ", ".join(names))

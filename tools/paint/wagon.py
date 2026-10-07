"""The family wagon: red, with wood down its sides and a rack on the roof. Here it is as it came down
in Egypt: nose in the sand, front wheel buried, the holiday luggage still tied on top.

Measurements run from the nose (x = 0) to the tail (x = 300); y is up from the ground; z is across
the car, from the driver's side (0, the side we see) to the far side (D)."""

import math

import numpy as np

from brush import *
from solid import Draft, mix

D = 70.0                                                    # how wide the car is
RED = dict(top="#f29478", shine="#ffd0b4", side="#cf5a42", low="#a84330", front="#e67a5a", dark="#70291f")
WOOD = dict(frame="#e2bc80", field="#a87444", grain="#7e5230", dark="#5c3a20")
GLASS = dict(dark="#182238", mid="#34466c", sky="#8fb6de", shine="#e4f2ff")
CHROME = dict(shine="#ffffff", light="#d8dde2", mid="#9aa2aa", dark="#565c66")
RUBBER = dict(lit="#4c4852", mid="#2a2730", dark="#141218")
LEATHER = dict(top="#d99a5c", end="#e8b070", front="#b4733e", dark="#6e4426", strap="#4a2c18")
TRUNK = dict(top="#5f8a80", end="#6c988c", front="#3f625a", dark="#243a36", slat="#c89c5e", brass="#f0c860")
COOLER = dict(top="#fbf6e8", end="#7fb2e6", front="#4a84c8", dark="#2c5690", lid="#e2dccb", lidend="#fffdf4")
RACK_Y = 99.0


def profile():
    """The outline of the side of the body, clockwise from the bottom of the front bumper."""
    d = Draft(None, (0, 0))
    pts = [(6, 20), (2, 24), (0, 34), (4, 52), (10, 57), (104, 61), (132, 91), (140, 94), (270, 95), (282, 92), (294, 62), (298, 56), (299, 30), (296, 20), (262, 18)]
    pts += d.arc(232, 22, 28, 0, 180, 12)[1:-1] + [(204, 18), (82, 18)] + d.arc(52, 22, 28, 0, 180, 12)[1:-1] + [(22, 18)]
    return pts


def luggage(base, lines, d, take=()):
    """What is tied on the roof: a suitcase, a trunk and a cooler. `take` names any that are gone."""
    y = RACK_Y + 1
    if "suitcase" not in take:                               # lying flat, handle toward us, stickers from other holidays on its lid
        x0, x1, h, z0, z1 = 150, 200, 15, 14, 56
        d.box(x0, x1, y, y + h, z0, z1, LEATHER["front"], LEATHER["top"], LEATHER["end"])
        for sx in (x0 + 9, x1 - 12):                         # two straps right round it
            d.poly([(sx, y, z0), (sx + 4, y, z0), (sx + 4, y + h, z0), (sx, y + h, z0)], LEATHER["strap"])
            d.poly([(sx, y + h, z0), (sx + 4, y + h, z0), (sx + 4, y + h, z1), (sx, y + h, z1)], LEATHER["dark"])
        lines.poly(d.pts([(x0 + 20, y + h, 22), (x0 + 30, y + h, 22), (x0 + 30, y + h, 34), (x0 + 20, y + h, 34)]), "#e8e0c4")     # stickers
        lines.poly(d.pts([(x0 + 22, y + h, 40), (x0 + 31, y + h, 38), (x0 + 32, y + h, 48), (x0 + 23, y + h, 50)]), "#5aa0d0")
        lines.poly(d.pts([(x0 + 28, y + h, 26), (x0 + 36, y + h, 28), (x0 + 35, y + h, 36), (x0 + 27, y + h, 34)]), "#e0584a")
        lines.line(d.pts([(x0 + 20, y + h * 0.55, z0), (x0 + 21, y + h * 0.95, z0 - 3), (x0 + 30, y + h * 0.95, z0 - 3), (x0 + 31, y + h * 0.55, z0)]), LEATHER["dark"], 1.6 * d.k)   # the handle
        for cx in (x0, x1):                                  # brass corners
            lines.line(d.pts([(cx, y + h, z0), (cx + (2 if cx == x0 else -2), y + h, z0), ]), TRUNK["brass"], 1.2 * d.k)
        lines.line(d.pts([(x0, y + h, z0), (x1, y + h, z0)]), "#f6c890", 0.8 * d.k, 0.7)
    if "trunk" not in take:                                  # a proper old trunk: wooden slats, brass corners, a hasp
        x0, x1, h, z0, z1 = 204, 250, 31, 8, 62
        d.box(x0, x1, y, y + h, z0, z1, TRUNK["front"], TRUNK["top"], TRUNK["end"])
        for sx in (x0 + 2, x0 + 21, x1 - 6):                 # slats up the front and over the lid
            d.poly([(sx, y, z0), (sx + 4, y, z0), (sx + 4, y + h, z0), (sx, y + h, z0)], TRUNK["slat"])
            d.poly([(sx, y + h, z0), (sx + 4, y + h, z0), (sx + 4, y + h, z1), (sx, y + h, z1)], "#e0b878")
        for sz in (z0 + 3, z1 - 7):
            d.poly([(x0, y, sz), (x0, y, sz + 4), (x0, y + h, sz + 4), (x0, y + h, sz)], "#e0b878")
        lines.line(d.pts([(x0, y + h * 0.66, z0), (x1, y + h * 0.66, z0)]), TRUNK["dark"], 1.2 * d.k)          # where the lid shuts
        lines.line(d.pts([(x0, y + h * 0.66, z0), (x0, y + h * 0.66, z1)]), TRUNK["dark"], 1.0 * d.k)
        lines.poly(d.pts([(x0 + 11, y + h * 0.52, z0), (x0 + 16, y + h * 0.52, z0), (x0 + 16, y + h * 0.74, z0), (x0 + 11, y + h * 0.74, z0)]), TRUNK["brass"])   # the hasp
        for cx, cy in ((x0, y), (x1, y), (x0, y + h), (x1, y + h)):
            sgn = 1 if cx == x0 else -1
            up = 1 if cy == y else -1
            lines.poly(d.pts([(cx, cy, z0), (cx + sgn * 5, cy, z0), (cx, cy + up * 5, z0)]), TRUNK["brass"])
        lines.line(d.pts([(x0, y + h, z0), (x1, y + h, z0)]), "#a8d0c4", 0.8 * d.k, 0.6)
    if "cooler" not in take:                                 # blue, with a white lid that has seen better picnics
        x0, x1, h, z0, z1 = 254, 281, 23, 18, 52
        d.box(x0, x1, y, y + h - 5, z0, z1, COOLER["front"], COOLER["top"], COOLER["end"])
        d.box(x0 - 1, x1 + 1, y + h - 5, y + h, z0 - 1, z1 + 1, COOLER["lid"], COOLER["top"], COOLER["lidend"])
        lines.line(d.pts([(x0 + 3, y + 5, z0), (x1 - 3, y + 5, z0)]), COOLER["dark"], 1.0 * d.k, 0.8)
        lines.line(d.pts([(x0 + 6, y + (h - 5) * 0.62, z0), (x1 - 6, y + (h - 5) * 0.62, z0)]), "#d8ecff", 1.6 * d.k)          # a white stripe
        lines.line(d.pts([(x0, y + (h - 5) * 0.8, z0 + 8), (x0 - 2, y + (h - 5) * 0.55, z0 + 8), (x0 - 2, y + (h - 5) * 0.55, z1 - 8), (x0, y + (h - 5) * 0.8, z1 - 8)]), "#f4f0e4", 1.2 * d.k)   # handle
    # cord over the lot, hooked to the near rail (the far side of each cord is out of sight)
    cord = "#b8322c"
    if "suitcase" not in take:
        lines.line(d.pts([(176, RACK_Y, 4), (176, y, 14), (176, y + 15, 14), (176, y + 15, 56)]), cord, 1.1 * d.k)
    if "trunk" not in take:
        lines.line(d.pts([(232, RACK_Y, 4), (232, y, 8), (232, y + 31, 8), (232, y + 31, 62)]), cord, 1.1 * d.k)
        lines.line(d.pts([(240, RACK_Y, 4), (240, y, 8), (240, y + 31, 8), (240, y + 31, 62)]), "#e8d8a0", 0.9 * d.k)
    if "cooler" not in take:
        lines.line(d.pts([(268, RACK_Y, 4), (268, y, 17), (268, y + 23, 17), (268, y + 23, 53)]), cord, 1.1 * d.k)


# ---------------------------------------------------------------- the luggage, standing open
PIECES = ("suitcase", "trunk", "cooler")                    # in the order they are painted: each one hides the one before
SHIRTS = [("#f45c98", "#b9386c", "#ffe873"),                # loud shirts: cloth, its shaded folds, its flowers
          ("#2fc0c8", "#1c8690", "#fff8e0"),
          ("#ffd638", "#d8962a", "#e8402c"),
          ("#ff8c2e", "#c85c1e", "#fff8e0"),
          ("#9460d8", "#623c9c", "#ffd638")]
LINING = dict(suitcase=("#f2e2ae", "#c9b07a", "#a88c56"), trunk=("#b05e4e", "#733a3c", "#d89a7c"))
SILVER = dict(shine="#ffffff", light="#e6eef4", mid="#b4c2d0", dark="#73839a")
ROPE = dict(light="#ecd092", mid="#c9a25a", dark="#7c5a2e")
ICE = dict(shine="#ffffff", light="#e4f2fb", mid="#b6d4ec", dark="#7ba6d0")
BOTTLE = dict(dark="#4a2412", mid="#7c4420", lit="#b9722e", shine="#f6c684", cap="#f0c850")


def _loop(points, steps=5):
    """A closed smooth outline through the points."""
    pts = [tuple(p) for p in points]
    return curve(pts[-1:] + pts + pts[:2], steps)[steps:steps + len(pts) * steps]


def _lid(d, x0, x1, yh, zh, depth, thick, deg, wall, lip, lining):
    """A lid thrown open. It is hinged along its far edge (y = yh, z = zh), is `depth` from hinge to
    front and `thick` deep, and has turned through `deg` degrees from shut. We look into it: the lining,
    the inside of its right wall, the outside of its left wall, and what was its front, now on top.
    -> a function (x, along, down) giving places in the lid: `along` from the hinge toward its front
    edge, `down` from its rim (0) to its panel (`thick`)."""
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))

    def at(x, along, down):
        return (x, yh + along * s + down * c, zh - along * c + down * s)

    d.poly([at(x0, 0, thick), at(x1, 0, thick), at(x1, depth, thick), at(x0, depth, thick)], lining[0])       # the lining
    d.poly([at(x0, 0, 0), at(x1, 0, 0), at(x1, 0, thick), at(x0, 0, thick)], mix(lining[0], lining[1], 0.45))  # the wall by the hinge
    d.poly([at(x1, 0, 0), at(x1, depth, 0), at(x1, depth, thick), at(x1, 0, thick)], lining[1])               # inside of the right wall
    d.poly([at(x0, depth, 0), at(x1, depth, 0), at(x1, depth, thick), at(x0, depth, thick)], lip)             # the front, now on top
    d.poly([at(x0, 0, 0), at(x0, depth, 0), at(x0, depth, thick), at(x0, 0, thick)], wall)                    # outside of the left wall
    return at


def _lid_edges(d, lines, at, x0, x1, depth, thick, light, dark):
    """Say a thrown-back lid's edges again, crisply, over the brushwork: light where the sun catches
    them (left and top), dark on the shadow side (right) and where the lining meets its walls."""
    k = d.k
    lines.line(d.pts([at(x1, 0, thick), at(x1, depth, thick)]), dark, 0.9 * k, 0.75)                 # lining to right wall
    lines.line(d.pts([at(x0, 0, thick), at(x0, depth, thick)]), dark, 0.8 * k, 0.55)                 # left wall to lining
    lines.line(d.pts([at(x0, depth, thick), at(x1, depth, thick)]), dark, 0.8 * k, 0.6)              # lining to lip
    lines.line(d.pts([at(x1, 0, 0), at(x1, depth, 0)]), dark, 1.0 * k, 0.85)                         # the shadow-side edge
    lines.line(d.pts([at(x0, depth, 0), at(x1, depth, 0)]), light, 0.8 * k, 0.8)                     # the lip, in the sun
    lines.line(d.pts([at(x0, 0, 0), at(x0, depth, 0)]), light, 0.7 * k, 0.6)


def suitcase_open(d, lines):
    """The suitcase with its lid up: loud flowered shirts heaped in it and spilling over the front."""
    y = RACK_Y + 1
    x0, x1, z0, z1 = 150, 200, 14, 56
    yb = y + 9                                               # the lower shell; the lid was the other 6
    k = d.k
    lin = LINING["suitcase"]
    at = _lid(d, x0, x1, yb, z1, z1 - z0, 6.0, 104, LEATHER["end"], LEATHER["top"], lin)
    d.poly([at(x0 + 4, 5, 6), at(x1 - 4, 5, 6), at(x1 - 4, 19, 6), at(x0 + 4, 19, 6)], mix(lin[0], lin[1], 0.5))     # a gathered pocket in the lid
    lines.line(d.pts([at(x0 + 4, 19, 6), at(x1 - 4, 19, 6)]), lin[2], 0.9 * k, 0.9)
    lines.line(d.pts([at(x0 + 6, 0.6, 6), at(x1 - 2, 0.6, 6)]), lin[2], 0.8 * k, 0.6)
    _lid_edges(d, lines, at, x0, x1, 42, 6.0, "#f8cf9a", LEATHER["dark"])
    for sx in (x0 + 9, x1 - 12):                             # the straps, undone, hang from the lid's edge
        lines.line(d.pts([at(sx + 2, 42, 0), at(sx + 2.5, 36, -0.4), at(sx + 1.5, 31, -0.6)]), LEATHER["strap"], 1.5 * k)
        lines.ellipse(*d.pt(*at(sx + 1.5, 31, -0.6)), 1.1 * k, 1.1 * k, TRUNK["brass"])
    d.poly([(x0, yb, z0), (x1, yb, z0), (x1, yb, z1), (x0, yb, z1)], "#5a3a24")                                # it is dark inside

    def shirt(n, pts, fold=None, flowers=(), steps=4):
        cloth, shade, flower = SHIRTS[n]
        d.s.poly(_loop(d.pts(pts), steps), cloth)
        if fold:
            d.s.poly(_loop(d.pts(fold), steps), shade)
        for f in flowers:
            cx, cy = d.pt(*f[:3])
            r = (f[3] if len(f) > 3 else 1.25) * k
            lines.ellipse(cx, cy, r, r * 0.9, flower)

    # the heap, far shirts first
    shirt(0, [(150, 116, 55), (150, 117, 38), (157, 121, 30), (171, 122.5, 33), (178, 121.5, 50), (167, 123, 57)],
          fold=[(165, 121.5, 40), (171, 122.5, 33), (178, 121.5, 50), (171, 122.5, 55)],
          flowers=[(155, 119, 47), (161, 121.5, 38), (166, 122.5, 51), (158, 121, 54, 1.0)])
    shirt(1, [(176, 122, 57), (174, 121.5, 38), (185, 120.5, 30), (200, 118, 32), (201, 117.5, 54), (190, 121.5, 58)],
          fold=[(190, 120, 32), (200, 118, 32), (201, 117.5, 54), (194, 120.5, 50)],
          flowers=[(180, 121.5, 50), (187, 121, 40), (184, 121.5, 56, 1.0), (193, 120, 46, 1.0)])
    shirt(4, [(160, 120.5, 35), (165, 119.5, 23), (180, 119.5, 22), (187, 120.5, 31), (174, 122.5, 37)],
          fold=[(175, 120.5, 24), (180, 119.5, 22), (187, 120.5, 31), (178, 121.8, 33)],
          flowers=[(168, 121, 30), (176, 121.5, 31, 1.0)])
    # the lower shell: its end and its front
    d.poly([(x0, y, z0), (x0, y, z1), (x0, yb, z1), (x0, yb, z0)], LEATHER["end"])
    d.poly([(x0, y, z0), (x1, y, z0), (x1, yb, z0), (x0, yb, z0)], LEATHER["front"])
    for sx in (x0 + 9, x1 - 12):
        d.poly([(sx, y, z0), (sx + 4, y, z0), (sx + 4, yb, z0), (sx, yb, z0)], LEATHER["strap"])
    lines.line(d.pts([(x0 + 20, y + 3.2, z0), (x0 + 21, y + 7.4, z0 - 3), (x0 + 30, y + 7.4, z0 - 3), (x0 + 31, y + 3.2, z0)]), LEATHER["dark"], 1.6 * k)   # the handle
    for cx in (x0, x1):
        lines.line(d.pts([(cx, y, z0), (cx + (2 if cx == x0 else -2), y, z0)]), TRUNK["brass"], 1.2 * k)
    lines.line(d.pts([(x0, yb, z0), (x1, yb, z0)]), "#f6c890", 0.8 * k, 0.7)
    lines.line(d.pts([(x0, yb, z0), (x0, yb, z1)]), "#fbd9a4", 0.7 * k, 0.6)
    lines.line(d.pts([(x0, y, z0), (x1, y, z0)]), LEATHER["dark"], 0.9 * k, 0.7)                                # its foot, in shadow
    lines.line(d.pts([(x0, y, z0), (x0, yb, z0)]), "#f6c890", 0.7 * k, 0.5)
    # one shirt has slid over the left end, and one hangs down the front with a sleeve over the rail
    shirt(3, [(149, 116.5, 40), (149, 115.5, 17), (158, 117, 14.5), (165, 119.5, 23), (160, 120.5, 35)],
          fold=[(156, 117.5, 16), (158, 117, 14.5), (165, 119.5, 23), (161, 120, 31)],
          flowers=[(153, 117.5, 30), (158, 118.5, 22, 1.0)])
    shirt(0, [(149.6, 117, 57), (149.6, 109.5, 56.5), (149.6, 107.6, 49), (149.6, 108.6, 40), (149.6, 117, 37)],
          flowers=[(149.6, 112.5, 49, 1.0)])
    shirt(3, [(149.6, 116.5, 41), (149.6, 108.4, 40), (149.6, 106.4, 30), (149.6, 108.2, 20), (149.6, 115.5, 15.5)],
          fold=[(149.6, 110, 39), (149.6, 106.4, 30), (149.6, 108.2, 20), (149.6, 110.5, 26)],
          flowers=[(149.6, 112.5, 33, 1.0), (149.6, 112, 22, 1.0)])
    shirt(2, [(166, 119.5, 23), (164, 116, 14), (197, 115.5, 14), (199.5, 117.5, 30), (187, 120.5, 31), (180, 119.5, 22)],
          flowers=[(172, 118, 19), (183, 118.5, 21), (193, 118, 24), (178, 119.5, 26, 1.0)])
    zf = z0 - 0.6
    hang = [(167, 116.2, zf), (197, 115.6, zf), (197.5, 107, zf), (193, 102, zf), (187, 100.6, zf), (184.5, 96, zf - 3), (180.5, 93.6, zf - 5),
            (177, 94.4, zf - 5), (177.5, 99, zf - 2), (176, 104, zf), (171, 107.5, zf)]
    for sheet in (d.s, lines):                               # (again on the top sheet, so that it lies over the rail)
        sheet.poly(_loop(d.pts(hang), 4), SHIRTS[2][0])
        sheet.poly(_loop(d.pts([(186, 115.8, zf), (197, 115.6, zf), (197.5, 107, zf), (193, 102, zf), (189, 101.5, zf), (191, 108, zf)]), 4), SHIRTS[2][1])
    lines.line(d.pts([(178, 115.8, zf), (181, 110.5, zf), (184, 115.7, zf)]), SHIRTS[2][1], 0.9 * k)             # its collar
    for f in [(172.5, 112, zf), (179, 106, zf), (187, 109.5, zf), (182, 101, zf, 1.0), (193.5, 110.5, zf, 1.0), (180, 96, zf - 4, 1.0)]:
        cx, cy = d.pt(*f[:3])
        r = (f[3] if len(f) > 3 else 1.3) * k
        lines.ellipse(cx, cy, r, r * 0.9, SHIRTS[2][2])
    for f in [(176, 109.5, zf), (184, 105.5, zf), (190, 105, zf)]:                                               # and leaves
        cx, cy = d.pt(*f)
        lines.ellipse(cx, cy, 0.9 * k, 0.8 * k, "#3c9a48")


def trunk_open(d, lines):
    """The old trunk with its lid thrown back. In it: a silver windshield shade folded like a fan, a
    flashlight, a coil of rope hung over the front, a folded lawn chair, an old blanket."""
    y = RACK_Y + 1
    x0, x1, z0, z1, h = 204, 250, 8, 62, 31
    yb = y + h * 0.66                                        # where the lid shut
    k = d.k
    lin = LINING["trunk"]
    at = _lid(d, x0, x1, yb, z1, z1 - z0, h * 0.34, 101, TRUNK["end"], TRUNK["top"], lin)
    t = h * 0.34
    for sx in (x0 + 2, x0 + 21, x1 - 6):                     # the slats come over the edge of the lid
        d.poly([at(sx, 54, 0), at(sx + 4, 54, 0), at(sx + 4, 54, t), at(sx, 54, t)], "#e0b878")
    for sz in (3, 47):                                       # and down its side
        d.poly([at(x0, sz, 0), at(x0, sz + 4, 0), at(x0, sz + 4, t), at(x0, sz, t)], "#e0b878")
    d.poly([at(x0 + 5.2, 54, t), at(x1, 54, t), at(x1, 48.5, t), at(x0 + 5.2, 48.5, t)], mix(lin[0], lin[1], 0.6))     # the lip's shadow
    d.poly([at(x1 - 9, 0, t), at(x1, 0, t), at(x1, 54, t), at(x1 - 5, 54, t)], mix(lin[0], lin[1], 0.35))
    for sx in range(x0 + 9, x1 - 2, 6):                      # striped paper inside it
        lines.line(d.pts([at(sx, 1.5, t), at(sx, 52.5, t)]), lin[2], 0.8 * k, 0.42)
    _lid_edges(d, lines, at, x0, x1, 54, t, "#a8d0c4", TRUNK["dark"])
    for cx in (x0, x1):
        sgn = 1 if cx == x0 else -1
        lines.poly(d.pts([at(cx, 54, 0), at(cx + sgn * 5, 54, 0), at(cx, 49, 0)]), TRUNK["brass"])
    lines.poly(d.pts([at(x0 + 11.5, 54, -0.4), at(x0 + 15.5, 54, -0.4), at(x0 + 15.5, 50, -0.4), at(x0 + 11.5, 50, -0.4)]), TRUNK["brass"])   # the hasp, hanging
    # inside the box
    d.poly([(x0, yb, z0), (x1, yb, z0), (x1, yb, z1), (x0, yb, z1)], "#2c2628")
    d.poly([(x0, yb, z1), (x1, yb, z1), (x1, yb - 7, z1), (x0, yb - 7, z1)], lin[0])
    d.poly([(x1, yb, z0), (x1, yb, z1), (x1, yb - 9, z1), (x1, yb - 9, z0)], lin[1])
    d.poly([(x0 + 1, yb - 2.5, z0 + 1), (x1 - 1, yb - 2.5, z0 + 1), (x1 - 1, yb - 2.5, z1 - 1), (x0 + 1, yb - 2.5, z1 - 1)], "#6f6a42")       # an army blanket
    d.poly([(x0 + 1, yb - 2.5, z0 + 1), (x1 - 1, yb - 2.5, z0 + 1), (x1 - 1, yb - 2.5, z0 + 17), (x0 + 1, yb - 2.5, z0 + 17)], "#8d8652")
    lines.line(d.pts([(x0 + 2, yb - 2.5, z0 + 17), (x1 - 2, yb - 2.5, z0 + 17)]), "#4c4830", 0.8 * k, 0.8)
    # the windshield shade stands at the back: silver, folded like a fan
    folds = 6
    xs = [lerp(213.5, 251.0, i / folds) for i in range(folds + 1)]
    zs = [lerp(59.0, 32.5, i / folds) + (2.2 if i % 2 else -1.2) for i in range(folds + 1)]
    top = [yb + 22.5 + (1.4 if i % 2 else 0.0) for i in range(folds + 1)]
    for i in range(folds):
        tone = SILVER["light"] if i % 2 == 0 else SILVER["mid"]
        d.poly([(xs[i], yb - 3, zs[i]), (xs[i + 1], yb - 3, zs[i + 1]), (xs[i + 1], top[i + 1], zs[i + 1] + 2), (xs[i], top[i], zs[i] + 2)], tone)
    for i in range(folds + 1):
        lines.line(d.pts([(xs[i], yb - 1, zs[i]), (xs[i], top[i], zs[i] + 2)]), SILVER["dark"] if i % 2 else SILVER["shine"], 0.8 * k, 0.6 if i % 2 else 0.95)
    lines.line(d.pts([(xs[i], top[i], zs[i] + 2) for i in range(folds + 1)]), SILVER["shine"], 0.8 * k, 0.9)
    lines.line(d.pts([(xs[-1], yb - 1, zs[-1]), (xs[-1], top[-1], zs[-1] + 2)]), SILVER["dark"], 1.0 * k, 0.9)   # its shadow-side edge
    lines.line(d.pts([(xs[0] + 1.5, yb + 9, zs[0] + 0.6), (xs[1] - 1.2, yb + 17, zs[1] + 1.2)]), SILVER["shine"], 1.3 * k, 0.9)                 # the sun in it
    lines.line(d.pts([(xs[2] + 1.5, yb + 5, zs[2] + 0.6), (xs[3] - 1.2, yb + 13, zs[3] + 1.2)]), SILVER["shine"], 1.1 * k, 0.8)
    # a folded lawn chair stands along the left wall: aluminium tube, green and white webbing woven over and under
    xc = x0 + 1.2
    rows = [yb - 3, yb + 2.4, yb + 6.0, yb + 9.6, yb + 13.2]
    cols = [lerp(z0 + 4.5, z1 - 4.5, i / 7) for i in range(8)]
    for r in range(4):
        for c in range(7):
            tone = "#3f9a5a" if (r + c) % 2 == 0 else "#f6f2e0"
            for sheet in (d.s, lines) if r else (d.s,):      # (the rows above the rim again on the top sheet, to keep the weave crisp)
                sheet.poly(d.pts([(xc, rows[r], cols[c]), (xc, rows[r], cols[c + 1]), (xc, rows[r + 1], cols[c + 1]), (xc, rows[r + 1], cols[c])]), tone)
    frame = [(xc, yb - 2, z0 + 3.5), (xc, yb + 12.4, z0 + 3.5), (xc, yb + 14.4, z0 + 6), (xc, yb + 14.4, z1 - 6), (xc, yb + 12.4, z1 - 3.5), (xc, yb - 2, z1 - 3.5)]
    lines.line(d.pts(frame), "#7f8c98", 1.9 * k)
    lines.line(d.pts(frame), "#e4eaee", 1.1 * k)
    lines.line(d.pts([(xc + 2.6, yb + 9, z0 + 2.5), (xc + 2.6, yb + 16.4, z0 + 5), (xc + 2.6, yb + 16.4, z0 + 24), (xc + 2.6, yb + 14.6, z0 + 27)]), "#7f8c98", 1.7 * k)   # the legs, folded against it
    lines.line(d.pts([(xc + 2.6, yb + 9, z0 + 2.5), (xc + 2.6, yb + 16.4, z0 + 5), (xc + 2.6, yb + 16.4, z0 + 24), (xc + 2.6, yb + 14.6, z0 + 27)]), "#f4f8fa", 0.9 * k)
    # the box itself: its end, its front, the slats, the brass
    d.poly([(x0, y, z0), (x0, y, z1), (x0, yb, z1), (x0, yb, z0)], TRUNK["end"])
    d.poly([(x0, y, z0), (x1, y, z0), (x1, yb, z0), (x0, yb, z0)], TRUNK["front"])
    for sx in (x0 + 2, x0 + 21, x1 - 6):
        d.poly([(sx, y, z0), (sx + 4, y, z0), (sx + 4, yb, z0), (sx, yb, z0)], TRUNK["slat"])
    for sz in (z0 + 3, z1 - 7):
        d.poly([(x0, y, sz), (x0, y, sz + 4), (x0, yb, sz + 4), (x0, yb, sz)], "#e0b878")
    lines.line(d.pts([(x0, yb, z0), (x1, yb, z0)]), "#a8d0c4", 0.8 * k, 0.75)
    lines.line(d.pts([(x0, yb, z0), (x0, yb, z1)]), "#b8dcd0", 0.7 * k, 0.6)
    lines.line(d.pts([(x0, y, z0), (x1, y, z0)]), TRUNK["dark"], 0.9 * k, 0.7)
    lines.line(d.pts([(x0, y, z0), (x0, yb, z0)]), "#a8d0c4", 0.7 * k, 0.5)
    for cx in (x0, x1):
        sgn = 1 if cx == x0 else -1
        lines.poly(d.pts([(cx, y, z0), (cx + sgn * 5, y, z0), (cx, y + 5, z0)]), TRUNK["brass"])
    lines.poly(d.pts([(x0 + 12, yb - 5.2, z0), (x0 + 15, yb - 5.2, z0), (x0 + 15, yb - 2.2, z0), (x0 + 12, yb - 2.2, z0)]), TRUNK["brass"])       # the staple the hasp shut on
    # a coil of rope hangs over the front edge
    cx, cy, zc = x0 + 13.0, yb - 8.5, z0 - 0.8
    ring = [(cx + math.cos(a) * 6.0, cy + math.sin(a) * 7.2 - 0.6 * math.cos(a), zc) for a in np.linspace(0, 2 * math.pi, 22)]
    lines.line(d.pts([(cx - 1.5, yb + 1.5, z0 + 3), (cx - 0.5, yb + 0.2, zc), (cx, cy + 7.0, zc)]), ROPE["mid"], 2.0 * k)
    lines.line(d.pts(ring), ROPE["dark"], 4.6 * k)
    lines.line(d.pts(ring), ROPE["mid"], 3.4 * k)
    lines.line(d.pts(ring[11:20]), ROPE["light"], 1.4 * k)                                                       # the turns of it, lit from the left
    lines.line(d.pts([(px - 0.9, py + 0.2, pz) for px, py, pz in ring[9:21]]), ROPE["light"], 0.8 * k, 0.9)
    lines.line(d.pts([(px + 0.5, py - 0.5, pz) for px, py, pz in ring[0:9]]), ROPE["dark"], 0.8 * k, 0.8)
    lines.line(d.pts([(cx - 2.2, cy + 7.6, zc), (cx + 2.2, cy + 6.4, zc)]), ROPE["dark"], 1.6 * k)               # where it is tied
    lines.line(d.pts([(cx + 4.5, cy - 5.5, zc), (cx + 6.0, cy - 10.5, zc), (cx + 5.2, cy - 12.0, zc)]), ROPE["mid"], 1.2 * k)   # the loose end
    # the flashlight lies on the blanket: yellow, with a black grip and a chrome head
    a, b = (214.5, yb + 1.0, 15.0), (237.0, yb + 4.2, 21.0)
    along = lambda u: tuple(lerp(a[i], b[i], u) for i in range(3))
    lines.line(d.pts([along(0.0), along(0.70)]), "#a87a18", 5.0 * k)
    lines.line(d.pts([along(0.0), along(0.70)]), "#f8ce34", 3.6 * k)
    lines.line(d.pts([(p[0], p[1] + 1.0, p[2]) for p in (along(0.04), along(0.52))]), "#fff3a4", 1.0 * k, 0.95)
    lines.line(d.pts([along(0.56), along(0.70)]), "#26262c", 4.2 * k, 1.0)
    lines.line(d.pts([along(0.73), along(0.97)]), CHROME["dark"], 6.6 * k)
    lines.line(d.pts([along(0.75), along(0.96)]), CHROME["light"], 5.0 * k)
    hx, hy = d.pt(*along(1.0))
    lines.ellipse(hx, hy, 2.0 * k, 3.2 * k, "#fff6c8")
    lines.line(d.pts([(p[0], p[1] + 1.5, p[2]) for p in (along(0.77), along(0.93))]), CHROME["shine"], 0.9 * k)
    sx, sy = d.pt(*along(0.30))
    lines.ellipse(sx, sy - 0.2 * k, 1.7 * k, 1.0 * k, "#e8402c")                                                 # its switch


def cooler_open(d, lines):
    """The cooler with its white lid stood beside it: brown bottles, and ice going to water."""
    y = RACK_Y + 1
    x0, x1, z0, z1, h = 254, 281, 18, 52, 23
    yb = y + h - 5
    k = d.k
    # the lid stands on its edge at the right-hand end, leaning on the rim: we see the inside of it
    foot, lean = (288.0, y - 0.5), (-0.3085, 0.951)
    up = lambda u, out=0.0: (foot[0] + lean[0] * u + lean[1] * out, foot[1] + lean[1] * u - lean[0] * out)
    d.poly([up(0) + (z0 - 1,), up(0) + (z1 + 1,), up(29) + (z1 + 1,), up(29) + (z0 - 1,)], "#f6f2e4")
    d.poly([up(4) + (z0 + 3,), up(4) + (z1 - 3,), up(25) + (z1 - 3,), up(25) + (z0 + 3,)], COOLER["lid"])       # the plug that fits the opening
    d.poly([up(29) + (z0 - 1,), up(29) + (z1 + 1,), up(29, 5) + (z1 + 1,), up(29, 5) + (z0 - 1,)], COOLER["lidend"])
    d.poly([up(0) + (z0 - 1,), up(0, 5) + (z0 - 1,), up(29, 5) + (z0 - 1,), up(29) + (z0 - 1,)], "#d6cfbc")     # its edge, toward us
    lines.line(d.pts([up(29) + (z0 - 1,), up(29) + (z1 + 1,)]), "#ffffff", 0.8 * k, 0.9)
    lines.line(d.pts([up(0, 5) + (z0 - 1,), up(29, 5) + (z0 - 1,)]), "#a8a290", 0.8 * k, 0.8)
    lines.line(d.pts([up(25) + (z0 + 3,), up(25) + (z1 - 3,)]), "#fffdf4", 0.7 * k, 0.8)
    lines.line(d.pts([up(0) + (z0 - 1,), up(29) + (z0 - 1,)]), "#fffdf4", 0.7 * k, 0.8)
    lines.line(d.pts([up(29, 5) + (z0 - 1,), up(29, 5) + (z1 + 1,)]), "#b9b29e", 0.8 * k, 0.7)
    # the box: a thick white rim, and the well full of ice
    d.poly([(x0, yb, z0), (x1, yb, z0), (x1, yb, z1), (x0, yb, z1)], "#f4f0e2")
    d.poly([(x0 + 2.2, yb, z0 + 2.5), (x1 - 2.2, yb, z0 + 2.5), (x1 - 2.2, yb, z1 - 2.5), (x0 + 2.2, yb, z1 - 2.5)], ICE["dark"])
    heap = [(254.6, yb + 1.2, 20.5), (253.2, yb + 5.6, 27), (253.0, yb + 7.0, 39), (254.0, yb + 7.2, 51.5), (262, yb + 7.4, 53.5), (272, yb + 7.2, 54),
            (281.0, yb + 6.4, 53.5), (281.6, yb + 3.6, 40), (280.4, yb + 1.4, 22), (272, yb + 0.6, 19.5), (263, yb + 1.0, 19.5)]
    d.s.poly(_loop(d.pts(heap), 4), ICE["light"])
    d.s.poly(_loop(d.pts([(254.2, yb + 4.6, 24), (253.6, yb + 6.4, 38), (256, yb + 7.0, 50), (266, yb + 7.0, 52), (271, yb + 5.6, 45), (264, yb + 3.4, 30), (258, yb + 3.0, 23)]), 4), ICE["shine"])
    d.s.poly(_loop(d.pts([(270, yb + 3.2, 34), (279.6, yb + 4.6, 50), (281.0, yb + 3.4, 40), (279.8, yb + 1.6, 24), (273, yb + 1.2, 23)]), 4), ICE["mid"])
    d.s.poly(_loop(d.pts([(266, yb + 0.9, 20.5), (279.5, yb + 1.3, 22.5), (279.8, yb + 2.0, 31), (272, yb + 1.8, 28)]), 4), ICE["dark"])       # where it has gone to water
    # bottles stand in it: the far one first
    def bottle(base, top, wide=5.2, tone=1.0):
        bx, by, bz = base
        tx, ty, tz = top
        p = lambda u, off=0.0: (lerp(bx, tx, u) + off, lerp(by, ty, u), lerp(bz, tz, u))
        lines.line(d.pts([p(0.0), p(0.50)]), BOTTLE["dark"], wide * k)                    # the body
        lines.line(d.pts([p(0.0, -0.5), p(0.48, -0.5)]), BOTTLE["mid"], (wide - 1.6) * k)
        lines.line(d.pts([p(0.46), p(0.66)]), BOTTLE["dark"], (wide * 0.72) * k)          # the shoulder
        lines.line(d.pts([p(0.46, -0.3), p(0.64, -0.3)]), BOTTLE["mid"], (wide * 0.72 - 1.2) * k)
        lines.line(d.pts([p(0.60), p(0.93)]), BOTTLE["dark"], 2.6 * k)                    # the neck
        lines.line(d.pts([p(0.60, -0.3), p(0.92, -0.3)]), BOTTLE["mid"], 1.5 * k)
        lines.line(d.pts([p(0.04, -1.3), p(0.44, -1.3)]), BOTTLE["lit"], 1.0 * k)         # the light down its left side
        lines.line(d.pts([p(0.10, -1.5), p(0.30, -1.5)]), BOTTLE["shine"], 0.7 * k, 0.95)
        lines.line(d.pts([p(0.93), p(1.0)]), "#8a6a1c", 3.4 * k)                          # the cap
        lines.line(d.pts([p(0.94, -0.2), p(1.0, -0.2)]), BOTTLE["cap"], 2.6 * k)
    bottle((268.5, yb + 0.5, 44), (268.9, yb + 15.0, 44))
    bottle((259.0, yb + 0.5, 34), (256.4, yb + 14.0, 34))
    bottle((274.5, yb - 0.5, 26), (277.6, yb + 12.5, 26))
    for (ix, iy, iz, r) in [(262.5, yb + 5.6, 44, 1.5), (256.0, yb + 5.8, 42, 1.3), (264.0, yb + 3.4, 30, 1.6), (270.5, yb + 3.0, 36, 1.4),
                            (256.6, yb + 3.4, 25, 1.3), (268.0, yb + 1.6, 23, 1.3), (276.5, yb + 3.0, 44, 1.4), (279.0, yb + 2.0, 31, 1.1)]:
        cx, cy = d.pt(ix, iy, iz)                                                          # lumps of ice: a lit top, a blue side
        lines.poly([(cx - r * k, cy - r * 0.7 * k), (cx + r * k, cy - r * 0.9 * k), (cx + r * 1.1 * k, cy + r * 0.7 * k), (cx - r * 0.8 * k, cy + r * 0.9 * k)], ICE["dark"])
        lines.poly([(cx - r * k, cy - r * 0.7 * k), (cx + r * k, cy - r * 0.9 * k), (cx + r * 0.5 * k, cy + r * 0.1 * k), (cx - r * 0.9 * k, cy + r * 0.3 * k)], ICE["shine"])
    # the box's end and front
    d.poly([(x0, y, z0), (x0, y, z1), (x0, yb, z1), (x0, yb, z0)], COOLER["end"])
    d.poly([(x0, y, z0), (x1, y, z0), (x1, yb, z0), (x0, yb, z0)], COOLER["front"])
    lines.line(d.pts([(x0 + 3, y + 5, z0), (x1 - 3, y + 5, z0)]), COOLER["dark"], 1.0 * k, 0.8)
    lines.line(d.pts([(x0 + 6, y + (h - 5) * 0.62, z0), (x1 - 6, y + (h - 5) * 0.62, z0)]), "#d8ecff", 1.6 * k)
    lines.line(d.pts([(x0, y + (h - 5) * 0.8, z0 + 8), (x0 - 2, y + (h - 5) * 0.55, z0 + 8), (x0 - 2, y + (h - 5) * 0.55, z1 - 8), (x0, y + (h - 5) * 0.8, z1 - 8)]), "#f4f0e4", 1.2 * k)
    lines.line(d.pts([(x0, yb, z0), (x1, yb, z0)]), "#ffffff", 0.9 * k, 0.9)
    lines.line(d.pts([(x0, yb, z0), (x0, yb, z1)]), "#ffffff", 0.8 * k, 0.8)
    lines.line(d.pts([(x1, y, z0), (x1, yb, z0)]), COOLER["dark"], 0.9 * k, 0.8)
    for (dx, drop) in ((8.0, 7.0), (20.5, 4.5)):                                           # melt water runs down the front
        lines.line(d.pts([(x0 + dx, yb - 0.5, z0), (x0 + dx + 0.3, yb - drop, z0)]), "#cfe6fb", 0.9 * k, 0.9)
        cx, cy = d.pt(x0 + dx + 0.3, yb - drop - 0.6, z0)
        lines.ellipse(cx, cy, 0.9 * k, 1.1 * k, "#e8f4ff")


OPEN = dict(suitcase=suitcase_open, trunk=trunk_open, cooler=cooler_open)


def piece(shape, origin, which, opened=False, scale=1.0, tilt=7.0):
    """One piece of the luggage alone on clear sheets, exactly where it sits on the wagon, shut or open.
    -> (color, alpha, line color, line alpha)."""
    base, lines = Sheet(shape), Sheet(shape)
    d = Draft(base, (origin[0] - 232 * scale, origin[1]), scale, tilt, pivot=(232, 0), depth=(-0.50, 0.30))
    if opened:
        OPEN[which](d, lines)
    else:
        luggage(d, lines, d, take=tuple(p for p in PIECES if p != which))
    return base.done() + lines.done()


def wagon(shape, origin, scale=1.0, tilt=7.0, take=(), mirror=True, buried=True, seed=4):
    """-> (color, alpha) of the wagon on a clear sheet the size of the picture. `origin` is where its
    rear wheel meets the ground."""
    base, lines = Sheet(shape), Sheet(shape)
    d = Draft(base, (origin[0] - 232 * scale, origin[1]), scale, tilt, pivot=(232, 0), depth=(-0.50, 0.30))
    dl = Draft(lines, d.o, scale, tilt, pivot=(232, 0), depth=(-0.50, 0.30))
    P = profile()

    # ---- under the car it is dark
    d.poly([(70, 6), (210, 6), (214, 20), (66, 20)], "#2a1c22")
    d.poly([(70, 6, D), (210, 6, D), (214, 20, D), (66, 20, D)], "#2a1c22")
    # ---- the far front wheel shows under the nose
    d.disc(52, 22, 22, RUBBER["dark"], z=D - 8)

    # ---- the front: bumper, grille, headlamps
    front = [(6, 20), (2, 24), (0, 34), (4, 52), (10, 57)]
    d.side(front, 0, D, RED["front"])
    d.side([(1.4, 37), (4, 51)], 13, D - 13, "#2c2a30")                                   # the grille
    for i in range(1, 6):
        yy = 37 + i * 2.3
        xx = 1.4 + (yy - 37) / 14 * 2.6
        dl.line([(xx, yy, 13), (xx, yy, D - 13)], CHROME["light"], 0.8, 0.9)
    for zc in (7, D - 7):                                                                 # headlamps: a chrome ring, a pale lens
        c = dl.pt(2.8, 44, zc)
        lines.ellipse(c[0], c[1], 4.4 * scale, 5.2 * scale, CHROME["mid"])
        lines.ellipse(c[0], c[1], 3.2 * scale, 4.0 * scale, "#fbf6dc")
        lines.ellipse(c[0] - 1.0 * scale, c[1] - 1.2 * scale, 1.2 * scale, 1.4 * scale, "#ffffff")
    d.side([(-1.5, 33), (-2.5, 25), (0, 22)], -2, D + 2, CHROME["light"])                 # the bumper
    dl.line([(-1.5, 33, -2), (-1.5, 33, D + 2)], CHROME["shine"], 1.0)
    dl.line([(-2.2, 26, -2), (-2.2, 26, D + 2)], CHROME["dark"], 1.0, 0.8)
    d.side([(-2.2, 31), (-2.4, 26)], 26, 44, "#f4efdc")                                   # number plate

    # ---- hood, windshield, roof: the faces that look up at the sky
    d.side([(10, 57), (104, 61)], 0, D, RED["top"])
    d.poly([(18, 57.6, 10), (96, 60.8, 10), (96, 60.8, 30), (18, 57.6, 30)], RED["shine"], 0.55)     # the sun slides along the hood
    dl.line([(10, 57, 0), (10, 57, D)], RED["shine"], 0.9, 0.8)
    dl.line([(58, 59, 0), (58, 59, D)], RED["low"], 0.7, 0.5)                             # a seam across the hood
    d.side([(104, 61), (132, 91)], 0, D, RED["side"])                                     # the windshield's frame
    d.side([(106.5, 64), (130, 89)], 5, D - 5, GLASS["sky"])
    d.poly([(106.5, 64, 5), (130, 89, 5), (130, 89, 24), (106.5, 64, 30)], GLASS["shine"], 0.75)      # the sky in the glass
    d.poly([(106.5, 64, 44), (118, 76, 46), (118, 76, D - 5), (106.5, 64, D - 5)], GLASS["mid"], 0.9)   # the dashboard's shadow
    dl.line([(107, 64.5, 30), (114, 71, 31)], "#20242c", 1.3, 0.9)                        # the wipers
    dl.line([(107, 64.5, 56), (114, 71, 57)], "#20242c", 1.3, 0.9)
    d.poly([(10, 57.2, 8), (30, 58, 4), (38, 58.4, 30), (26, 58, 52), (10, 57.2, 60)], "#f0c888", 0.8)   # sand thrown up over the hood
    d.side([(132, 91), (140, 94), (270, 95), (282, 92)], 0, D, RED["top"])
    d.poly([(146, 94.2, 6), (270, 95, 6), (270, 95, 20), (146, 94.2, 20)], RED["shine"], 0.45)
    # ---- the rack, and what is on it
    d.line([(146, RACK_Y, D - 4), (284, RACK_Y, D - 4)], CHROME["mid"], 1.5)             # the far rail and the cross bars go under the luggage
    for px in (148, 214, 282):
        d.line([(px, RACK_Y, D - 4), (px, 94.6, D - 4)], CHROME["dark"], 1.4)
    for px in (148, 192, 238, 282):
        d.line([(px, RACK_Y, 4), (px, RACK_Y, D - 4)], CHROME["mid"], 1.3)
    luggage(d, lines, d, take)
    dl.line([(146, RACK_Y, 4), (284, RACK_Y, 4)], CHROME["light"], 1.6)                   # the near rail goes over it
    dl.line([(146, RACK_Y + 0.6, 4), (284, RACK_Y + 0.6, 4)], CHROME["shine"], 0.6, 0.9)
    for px in (148, 214, 282):
        dl.line([(px, RACK_Y, 4), (px, 94.6, 4)], CHROME["mid"], 1.5)

    # ---- the side we see
    d.poly(P, RED["side"])
    d.poly([(6, 20), (2, 24), (0, 30), (299, 30), (296, 20), (262, 18), (204, 18), (82, 18), (22, 18)], RED["low"], 0.75)     # the lower body turns from the sky
    d.poly([(10, 57), (104, 61), (104, 57), (10, 53)], RED["top"], 0.6)                   # the shoulder catches the light
    d.poly([(134, 91), (140, 94), (270, 95), (282, 92), (280, 90), (270, 92.6), (140, 91.6)], RED["top"], 0.7)
    # wood down the side: a pale frame round a darker panel
    wood = [(16, 30), (14, 50), (104, 53), (292, 53), (296, 30)]
    d.poly(wood, WOOD["frame"])
    d.poly([(20, 33), (18.5, 47), (104, 49.6), (289, 49.6), (292, 33)], WOOD["field"])
    for k in range(7):                                                                    # the grain
        yy = 34.5 + k * 2.2
        dl.line([(22, yy), (120, yy + 0.4), (290, yy)], WOOD["grain"], 0.6, 0.45)
    for px in (136, 180, 226):
        d.poly([(px - 2, 30), (px + 2, 30), (px + 2, 53), (px - 2, 53)], WOOD["frame"])
    d.poly([(200, 33), (292, 33), (289, 49.6), (200, 49.6)], WOOD["dark"], 0.22)
    d.poly([(6, 20), (112, 18), (126, 30), (70, 44), (12, 42), (2, 30)], "#e6b676", 0.38)   # dust thrown up by the landing
    d.poly([(6, 20), (70, 18), (60, 32), (10, 34), (2, 28)], "#e6b676", 0.35)
    # wheel arches and wheels
    for cx in (52, 232):
        d.poly(d.arc(cx, 22, 30, -6, 186, 16), RED["side"])
        dl.line(d.arc(cx, 22, 30, 0, 180, 16), RED["top"], 0.9, 0.7)
        d.poly(d.arc(cx, 22, 27, -10, 190, 16), "#1c1418")
        d.disc(cx, 22, 22, RUBBER["mid"])
        d.poly(d.arc(cx, 22, 22, 200, 340, 10) + [(cx, 22)], RUBBER["dark"])
        d.poly(d.arc(cx, 22, 22, 60, 150, 8) + list(reversed(d.arc(cx, 22, 18.5, 60, 150, 8))), RUBBER["lit"])
        d.disc(cx, 22, 12.5, CHROME["mid"])
        d.disc(cx - 0.8, 22.8, 10.5, CHROME["light"])
        d.disc(cx, 22, 5.0, CHROME["mid"])
        d.disc(cx - 1.6, 24.0, 2.2, CHROME["shine"])
        for a in range(0, 360, 45):
            dl.line([(cx + math.cos(math.radians(a)) * 6, 22 + math.sin(math.radians(a)) * 6), (cx + math.cos(math.radians(a)) * 10, 22 + math.sin(math.radians(a)) * 10)], CHROME["dark"], 0.8, 0.7)
    # glass
    wins = ([(138, 64), (147, 88), (176, 89), (176, 64)], [(181, 64), (181, 89), (222, 89.3), (222, 64)], [(227, 64), (227, 89.3), (268, 89.6), (280, 64)])
    for w in wins:
        d.poly(w, GLASS["dark"])
        x0, x1 = min(p[0] for p in w), max(p[0] for p in w)
        d.poly([(x0 + 3, 72), (x1 - 2, 72), (x1 - 2, 86), (x0 + 9, 86)], GLASS["mid"])                # the far windows, seen through
        d.poly([(x0 + 4, 66), (x0 + 12, 66), (x0 + 24, 87), (x0 + 16, 87)], GLASS["sky"], 0.55)       # a slant of sky
        dl.line([w[0], w[1], w[2], w[3], w[0]], CHROME["light"], 0.9, 0.9)
    d.poly([(194, 64), (212, 64), (212, 76), (208, 80), (198, 80), (194, 76)], "#0e1422")             # a seat back
    # seams, handles, the long bright line under the windows
    for px, y0 in ((136, 20), (179, 20), (225, 30)):
        dl.line([(px, y0), (px, 62)], RED["dark"], 0.8, 0.75)
    for px in (166, 211):
        dl.line([(px, 57), (px + 9, 57)], CHROME["shine"], 1.6)
        dl.line([(px, 56), (px + 9, 56)], CHROME["dark"], 0.7, 0.8)
    dl.line([(12, 58.4), (104, 62.2), (292, 62.2)], CHROME["light"], 1.0, 0.85)
    dl.line([(8, 19.5), (22, 18), (82, 18)], RED["dark"], 1.2, 0.8)
    dl.line([(204, 18), (262, 18), (296, 20)], RED["dark"], 1.2, 0.8)
    d.poly([(293, 40), (298.4, 40), (298.2, 55), (294, 60)], "#d83a2c")                   # the tail lamp wraps round the corner
    d.poly([(296, 20), (300.5, 21), (300.5, 30), (298, 31)], CHROME["mid"])               # and the end of the rear bumper
    if mirror:                                                                             # the door mirror stands out toward us
        dl.line([(139, 65, 0), (140, 66, -9)], CHROME["dark"], 1.6)
        c = dl.pt(141, 68, -10)
        lines.ellipse(c[0], c[1], 5.2 * scale, 3.8 * scale, CHROME["mid"])
        lines.ellipse(c[0] - 0.8 * scale, c[1] - 0.6 * scale, 3.6 * scale, 2.4 * scale, "#cfe6f6")
    dl.line([(112, 62, 2), (110, 86, 2), (104, 104, 2)], "#30303a", 0.8)                  # the aerial, bent

    color, alpha = base.done()
    lc, la = lines.done()
    return color, alpha, lc, la


def drift(shape, origin, scale=1.0):
    """The sand the nose ploughed up: a low heap round the bumper and the front wheel, and a wave of it
    pushed out ahead. -> (multiplier, mask), to be multiplied into the ground it lies on."""
    import land
    ox, oy = origin[0] - 232 * scale, origin[1]
    outline = [(-120, -8), (-96, 10), (-66, 26), (-34, 38), (0, 40), (30, 33), (56, 27), (84, 24), (108, 14), (128, 0), (136, -12), (60, -16), (-40, -16)]
    pts = [(ox + x * scale, oy - u * scale) for x, u in outline]
    return land.mound(shape, pts, soft=6.0 * scale)


def render(shape, origin, scale=1.0, take=(), mirror=True, seed=4, back=None):
    """The finished cut-out: brushed, with its crisp lines put back on top. -> (color, alpha).
    `back` is the picture it will stand on: the heap of sand at its nose is made out of that ground."""
    color, alpha, lc, la = wagon(shape, origin, scale, take=take, mirror=mirror, seed=seed)
    flat = np.empty(shape + (3,), dtype=F32)
    flat[...] = rgb("#cf9456") if back is None else np.median(back[int(origin[1]) - 30:int(origin[1]) + 10].reshape(-1, 3), axis=0)
    over(flat, color, alpha)
    painted = strokes(flat, sizes=(7, 4, 2), seed=seed, density=1.8, jitter=0.03, keep=0.42)
    over(painted, lc, la)
    alpha = np.maximum(alpha, la)
    x, y = grid(shape)
    alpha = alpha * (y < origin[1] + 3 * scale)               # nothing shows below the ground
    mult, da = drift(shape, origin, scale)
    ground = flat.copy() if back is None else back
    heap = np.clip(ground * mult[..., None], 0, 1)
    over(painted, heap, da)
    alpha = np.maximum(alpha, da)
    return painted, np.clip(alpha, 0, 1)


def _ground(shape, origin, back):
    flat = np.empty(shape + (3,), dtype=F32)
    flat[...] = rgb("#cf9456") if back is None else np.median(back[int(origin[1]) - 30:int(origin[1]) + 10].reshape(-1, 3), axis=0)
    return flat


def _inside(mask):
    """A mask less its outermost ring of pixels."""
    m = np.pad(mask, 1, mode="constant")
    out = np.ones(mask.shape, dtype=bool)
    for dy in (0, 1, 2):
        for dx in (0, 1, 2):
            out &= m[dy:dy + mask.shape[0], dx:dx + mask.shape[1]]
    return out


def thin(shape, origin, scale=1.0, take=()):
    """Places inside the car where the paint is laid on so thinly (the shine along the roof, the dusty
    rear panels) that a cut-out with hard edges comes out clear there, and the ground shows through.
    -> (mask of those places, mask of everything the cut-out does cover)."""
    color, alpha, lc, la = wagon(shape, origin, scale, take=take)
    x, y = grid(shape)
    laid = np.maximum(alpha, la) * (y < origin[1] + 3 * scale)
    mult, da = drift(shape, origin, scale)
    solid = np.maximum(laid, da) >= 0.5
    return ((laid > 0.15) & ~solid & _inside((laid > 0.15) | solid)), solid


def render_pair(shape, origin, scale=1.0, seed=4, back=None):
    """The wagon from one brushing, with its door mirror and without it: render() done twice over, so the
    two pictures differ only where the mirror is. -> (with, without, alpha, mask of the mirror)."""
    color, alpha, lc, la = wagon(shape, origin, scale, mirror=True, seed=seed)
    _, _, lc0, la0 = wagon(shape, origin, scale, mirror=False, seed=seed)
    flat = _ground(shape, origin, back)
    over(flat, color, alpha)
    painted = strokes(flat, sizes=(7, 4, 2), seed=seed, density=1.8, jitter=0.03, keep=0.42)
    without = painted.copy()
    over(painted, lc, la)
    over(without, lc0, la0)
    alpha = np.maximum(alpha, la)
    x, y = grid(shape)
    alpha = alpha * (y < origin[1] + 3 * scale)
    mult, da = drift(shape, origin, scale)
    ground = flat.copy() if back is None else back
    heap = np.clip(ground * mult[..., None], 0, 1)
    over(painted, heap, da)
    over(without, heap, da)
    alpha = np.clip(np.maximum(alpha, da), 0, 1)
    return painted, without, alpha, (np.abs(painted - without).sum(axis=2) > 0) & (alpha >= 0.5)


def open_state(shape, origin, which, scale=1.0, seed=4, back=None, fast=False):
    """One piece of the luggage standing open, as a cut-out to lay over the wagon that render() paints.

    It is painted where it stands, among the other pieces shut, and brushed like the wagon. Its mask is
    its own shape (less whatever a later-painted piece hides of it) together with every place the shut
    piece showed, so that nothing of the shut piece is left to see. The three are laid in the order of
    PIECES. -> (color, alpha, notes). In the notes, `bare` counts places where the shut piece showed and
    the open one leaves nothing of the wagon to see: there must be none."""
    i = PIECES.index(which)
    c0, a0, lc0, la0 = wagon(shape, origin, scale, take=(which,))
    ca, aa, lca, laa = wagon(shape, origin, scale)
    ground = _ground(shape, origin, back)
    shut, gone = ground.copy(), ground.copy()
    over(over(shut, ca, aa), lca, laa)
    over(over(gone, c0, a0), lc0, la0)
    seen = (np.abs(shut - gone).sum(axis=2) > 0.004) & (np.maximum(aa, laa) > 0.5)      # every place the shut piece shows
    cx, ax, lcx, lax = piece(shape, origin, which, True, scale)
    later = [piece(shape, origin, p, False, scale) for p in PIECES[i + 1:]]
    canvas = ground.copy()
    over(canvas, c0, a0)
    over(canvas, cx, ax)
    clear = np.ones(shape, dtype=F32)                                                    # where no later piece is in the way
    for (cy, ay, lcy, lay) in later:
        over(canvas, cy, ay)
        clear *= 1 - np.maximum(ay, lay)
    own = np.maximum(ax, lax) * clear
    alpha = np.maximum(own, seen.astype(F32))
    ys, xs = np.nonzero(alpha > 0.02)
    y0, y1, x0, x1 = max(ys.min() - 24, 0), min(ys.max() + 24, shape[0]), max(xs.min() - 24, 0), min(xs.max() + 24, shape[1])
    painted = canvas.copy()
    if not fast:                                                                         # only its own corner of the picture needs the brush
        painted[y0:y1, x0:x1] = strokes(canvas[y0:y1, x0:x1], sizes=(7, 4, 2), seed=seed + 11 + i, density=1.8, jitter=0.03, keep=0.42)
    over(painted, lc0, la0)
    over(painted, lcx, lax * clear)
    for (cy, ay, lcy, lay) in later:
        over(painted, lcy, lay)
    rest = seen & (own <= 0.5)                                                           # places where we now see past it
    under = np.maximum(a0, la0)
    faint = rest & (under <= 0.5) & (under > 0.15)                                       # ... to thin paint: the ground shows there (see thin())
    if back is not None:
        painted[faint] = back[faint]
    bare = rest & (under <= 0.15)                                                        # ... or to nothing at all
    return painted, np.clip(alpha, 0, 1), dict(seen=seen, own=own > 0.5, rest=rest, faint=faint, bare=bare)


if __name__ == "__main__":
    from PIL import Image
    shape = (260, 440)
    c, a = render(shape, (330, 200), 1.0)
    bg = np.empty(shape + (3,), dtype=F32)
    bg[...] = rgb("#d39a58")
    over(bg, c, (a > 0.5).astype(F32))
    Image.fromarray((np.clip(bg, 0, 1) * 255).astype(np.uint8)).resize((880, 520), Image.NEAREST).save("out/wagon-try.png")
    print("ok")

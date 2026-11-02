"""PAINT-21C: the Dojima shore's cut-outs and the frames of its moving things (edo-dojima). Drawn through the scene's
camera (edo_dojima.CAM), in its light; each returned as (colour, coverage) for edo_dojima.py to brush and save.

  the stall (O-Natsu's alms, before her house):  `sandals` (a heap of straw sandals on a mat; `sandals-few` smaller),
      `pot` (a portable clay hearth and the great rice pot on it, its lid off: the steam is the engine's smoke), `stall`
      (the trestle table and the tub of pickled radish on it), `tray` (the rice balls, bale-shaped, in rows: full;
      `tray-half` emptying, `tray-empty` empty), `kettle` (the tea kettle on its little brazier)
  `noren`    O-Natsu's house-name noren in her doorway (indigo, a white mark of our own: a rice bale in a ring)
  `lighter`  a lighter moored at the foot of the steps, loaded with rice bales under mats (it rides: fx bob)
  `market`   the rice dealers who will not stop, in the road at the right with their hands up, and the two water men
             with their buckets at their left end
  `front`    rice bales on a board and a bucket at the very front, bottom right
  frames     lighters going by on the river (two sizes: a nearer lane and a farther one), the price runner (a run cycle),
             a bucket's splash (the water men's)
"""

import math

import numpy as np

from brush import F32, Sheet, curve, lerp
from edo_dojima_kit import *
import edo_dojima as D

g = D.g
CAM = D.CAM


def sheets():
    return Paper(SHAPE), Paper(SHAPE)


# ---------------------------------------------------------------- the stall
SANDALS = dict(X0=-808.0, X1=-738.0, Z0=-1300.0, Z1=-1235.0)
HEARTH = dict(X0=-698.0, X1=-606.0, Z0=-1302.0, Z1=-1228.0, h=52.0)
TABLE = dict(X0=-592.0, X1=-418.0, Z0=-1292.0, Z1=-1232.0, h=72.0)
TRAY = dict(X0=-584.0, X1=-498.0, Z0=-1282.0, Z1=-1242.0)
TUB = dict(X=-452.0, Z=-1262.0, r=22.0, h=30.0)
KETTLE = dict(X=-382.0, Z=-1262.0)


def sandals(n_rows=4):
    """A heap of new straw sandals on a dark straw mat on the ground: pairs piled in rows (pale new straw, a red thong's
    knot on each), the heap's top lit; `n_rows` 4 full, 2 when fewer are left."""
    s, l = sheets()
    S = SANDALS
    mat = [g(S["X0"] - 14, S["Z1"] + 12), g(S["X1"] + 14, S["Z1"] + 12), g(S["X1"] + 14, S["Z0"] - 10), g(S["X0"] - 14, S["Z0"] - 10)]
    s.poly(mat, lerp(STRAW_SH, SIENNA, 0.45))
    for i in range(1, 5):                                    # the mat's weave
        u = i / 5
        a_ = (mat[0][0] + (mat[3][0] - mat[0][0]) * u, mat[0][1] + (mat[3][1] - mat[0][1]) * u)
        b_ = (mat[1][0] + (mat[2][0] - mat[1][0]) * u, mat[1][1] + (mat[2][1] - mat[1][1]) * u)
        l.line([a_, b_], lerp(STRAW_SH, PRUSSIAN, 0.3), 0.6, 0.5)
    for row in range(n_rows):
        Y = 3.5 + row * 4.0
        inset = row * 7.0
        nx = max(1, 4 - row)
        for i in range(nx):
            for j in range(2):
                X = S["X0"] + inset + 8 + i * (S["X1"] - S["X0"] - 2 * inset - 16) / max(nx - 1, 1) if nx > 1 else (S["X0"] + S["X1"]) / 2
                Z = S["Z0"] + inset * 0.6 + 16 + j * 30
                p = g(X, Z, Y)
                k = CAM.k(X, Z)
                rx, ry = 9.0 * k, 3.6 * k
                c = lerp(STRAW_LIT, NAPLES, 0.35) if (row + i + j) % 2 else lerp(STRAW_LIT, WHITE, 0.15)
                s.ellipse(p[0], p[1], rx, ry, c)
                l.line([(p[0] - rx * 0.8, p[1] + ry * 0.3), (p[0] + rx * 0.8, p[1] + ry * 0.3)], STRAW_SH, 0.7, 0.75)
                s.ellipse(p[0] + rx * 0.55, p[1] - ry * 0.2, 1.5 * k, 1.2 * k, VERMILION)        # the thong's knot
    CAM.line(l, mat[:2], CAM.depth(S["X0"], S["Z1"]))
    return s, l


def pot():
    """The portable hearth (a squat clay stove, its fire mouth toward us dark: the embers are the engine's) and the great
    flanged rice pot on it, its wooden lid off and leaning against the hearth's side; the rice white in its mouth."""
    s, l = sheets()
    Hh = HEARTH
    X0, X1, Z0, Z1, h = Hh["X0"], Hh["X1"], Hh["Z0"], Hh["Z1"], Hh["h"]
    clay_lit, clay_sh = lerp(tintw(OCHRE, 0.3), SIENNA, 0.25), lerp(SIENNA, PRUSSIAN, 0.32)
    faces = CAM.box(s, X0, X1, 0, h, Z0, Z1, clay_lit, clay_sh, top=lerp(clay_lit, PRUSSIAN, 0.15))
    # the fire mouth, dark, an arch in the front face
    cx = (X0 + X1) / 2
    mouth = [g(cx - 16, Z1, 2), g(cx + 16, Z1, 2), g(cx + 16, Z1, 20), g(cx, Z1, 27), g(cx - 16, Z1, 20)]
    s.poly(mouth, lerp(PRUSSIAN, SIENNA, 0.25))
    # the pot: a flange (a ring) on the hearth's top, the belly below it, the mouth with the rice
    pc = (cx, h, (Z0 + Z1) / 2)
    k = CAM.k(cx, pc[2])
    top = g(cx, pc[2], h + 26)
    flange = g(cx, pc[2], h + 12)
    iron, iron_lit = lerp(PRUSSIAN, SIENNA, 0.18), lerp(tintw(PRUSSIAN, 0.35), OCHRE, 0.1)
    s.ellipse(flange[0], flange[1], 48 * k, 13 * k, iron)                   # the flange
    s.ellipse(flange[0] + 10 * k, flange[1] - 1 * k, 30 * k, 7 * k, iron_lit)
    s.poly([(top[0] - 33 * k, top[1]), (top[0] + 33 * k, top[1]), (flange[0] + 36 * k, flange[1] - 2 * k), (flange[0] - 36 * k, flange[1] - 2 * k)], iron)
    s.poly([(top[0] + 12 * k, top[1]), (top[0] + 33 * k, top[1]), (flange[0] + 36 * k, flange[1] - 2 * k), (flange[0] + 14 * k, flange[1] - 2 * k)], iron_lit)
    s.ellipse(top[0], top[1], 33 * k, 9 * k, lerp(iron, PRUSSIAN, 0.3))      # the rim
    s.ellipse(top[0], top[1] + 0.8 * k, 29 * k, 7.2 * k, lerp(WHITE, NAPLES, 0.18))   # the rice
    s.ellipse(top[0] - 6 * k, top[1] + 1.5 * k, 12 * k, 3 * k, PLASTER_SH)
    # the wooden lid leaning against the hearth's front, at its right corner
    lid_a, lid_b = g(X1 - 10, Z1 + 12, 0), g(X1 - 16, Z1 + 2, 62)
    s.line([lid_a, lid_b], WOOD_LIT, max(1.5, 7 * k))
    s.ellipse((lid_a[0] + lid_b[0]) / 2 - 2, (lid_a[1] + lid_b[1]) / 2, 22 * k, 30 * k, lerp(WOOD_LIT, NAPLES, 0.15))
    l.line([(lid_b[0] - 12 * k, lid_b[1] + 10 * k), (lid_a[0] - 12 * k, lid_a[1] - 4 * k)], PRUSSIAN, 0.7, 0.5)
    for name, pp in faces.items():
        CAM.line(l, list(pp) + [pp[0]], CAM.depth(cx, Z1), warm=(name == "right"))
    l.line([(top[0] - 33 * k, top[1]), (flange[0] - 36 * k, flange[1] - 2 * k)], PRUSSIAN, 0.8, 0.6)
    info = dict(mouth=g(cx, pc[2], h + 27), fire=g(cx, Z1, 10))
    return s, l, info


def stall_table():
    """The trestle table (a plank on two trestles) and the tub of pickled radish on it, its yellow slices on top."""
    s, l = sheets()
    T = TABLE
    top_c = lerp(WOOD_LIT, NAPLES, 0.12)
    # the plank: its top (lit), its front edge (shade), its west end (lit)
    CAM.box(s, T["X0"], T["X1"], T["h"] - 6, T["h"], T["Z0"], T["Z1"], top_c, WOOD_SH, top=top_c)
    for X in (T["X0"] + 14, T["X1"] - 14):                 # the trestles: two splayed legs each, a cross bar
        for dz in (-20, 20):
            Zc = (T["Z0"] + T["Z1"]) / 2 + dz
            l.line([g(X - 8, Zc, 0), g(X, Zc, T["h"] - 6)], WOOD_SH, max(1.0, 5 * CAM.k(X, Zc)), 1.0)
            l.line([g(X + 8, Zc, 0), g(X, Zc, T["h"] - 6)], WOOD_SH, max(1.0, 5 * CAM.k(X, Zc)), 1.0)
        l.line([g(X, T["Z1"] - 10, 30), g(X, T["Z0"] + 10, 30)], WOOD_SH, max(0.8, 4 * CAM.k(X, T["Z1"])), 1.0)
    CAM.line(l, [g(T["X0"], T["Z1"], T["h"] - 6), g(T["X1"], T["Z1"], T["h"] - 6), g(T["X1"], T["Z1"], T["h"]), g(T["X0"], T["Z1"], T["h"]), g(T["X0"], T["Z1"], T["h"] - 6)], CAM.depth(T["X1"], T["Z1"]))
    # the tub: a wooden tub bound with hoops, the pickled radish showing yellow over its rim
    U = TUB
    k = CAM.k(U["X"], U["Z"])
    bot, topp = g(U["X"], U["Z"] + U["r"], T["h"]), g(U["X"], U["Z"] + U["r"], T["h"] + U["h"])
    w = U["r"] * k
    s.poly([(bot[0] - w, bot[1]), (bot[0] + w, bot[1]), (topp[0] + w * 1.05, topp[1]), (topp[0] - w * 1.05, topp[1])], WOOD_LIT)
    s.poly([(bot[0] + w * 0.3, bot[1]), (bot[0] + w, bot[1]), (topp[0] + w * 1.05, topp[1]), (topp[0] + w * 0.3, topp[1])], lerp(WOOD_LIT, NAPLES, 0.2))
    rim = g(U["X"], U["Z"], T["h"] + U["h"])
    s.ellipse(rim[0], rim[1], w * 1.05, w * 0.32, WOOD_SH)
    radish = lerp(NAPLES, OCHRE, 0.35)
    s.ellipse(rim[0], rim[1] + 0.5, w * 0.92, w * 0.26, radish)
    for i in range(5):
        a = i * 1.3
        s.ellipse(rim[0] + math.cos(a) * w * 0.45, rim[1] + math.sin(a) * w * 0.1, w * 0.22, w * 0.09, lerp(NAPLES, WHITE, 0.25))
    for v in (0.3, 0.75):
        l.line([(bot[0] - w + (topp[0] - bot[0]) * v - w * 0.05 * v, bot[1] + (topp[1] - bot[1]) * v), (bot[0] + w + w * 0.05 * v, bot[1] + (topp[1] - bot[1]) * v)], WOOD_DARK, max(0.7, 2.4 * k), 0.9)
    CAM.line(l, [(bot[0] - w, bot[1]), (topp[0] - w * 1.05, topp[1])], CAM.depth(U["X"], U["Z"]))
    return s, l, dict(tub=[rim[0] - w, rim[1] - w * 0.4, 2 * w, bot[1] - rim[1] + w * 0.4])


def tray(count=15):
    """A shallow wooden tray on the table, and in it the alms rice balls, bale-shaped (the Kansai shape, shaped with
    salted hands; no seaweed), in rows. `count` of them (15 full, 6 emptying, 0 empty)."""
    s, l = sheets()
    R = TRAY
    h0 = TABLE["h"]
    CAM.box(s, R["X0"], R["X1"], h0, h0 + 5, R["Z0"], R["Z1"], lerp(WOOD_LIT, NAPLES, 0.3), WOOD, top=lerp(WOOD, SIENNA, 0.2))
    spots = []
    for row in range(3):
        for i in range(5):
            X = R["X0"] + 11 + i * (R["X1"] - R["X0"] - 22) / 4
            Z = R["Z0"] + 9 + row * 11
            spots.append((X, Z))
    order = sorted(range(15), key=lambda i: (-spots[i][1], spots[i][0]))[:count] if count else []
    for i in sorted(order, key=lambda i: spots[i][1]):
        X, Z = spots[i]
        p = g(X, Z, h0 + 8)
        k = CAM.k(X, Z)
        s.ellipse(p[0], p[1], 5.2 * k, 3.4 * k, lerp(WHITE, NAPLES, 0.12))                     # the ball: a short bale, lying
        s.ellipse(p[0] + 1.6 * k, p[1] + 0.8 * k, 3.0 * k, 2.0 * k, PLASTER_SH)
        l.line([(p[0] - 5 * k, p[1] + 2.6 * k), (p[0] + 5 * k, p[1] + 2.6 * k)], PRUSSIAN, 0.5, 0.35)
    e = [g(R["X0"], R["Z1"], h0 + 5), g(R["X1"], R["Z1"], h0 + 5)]
    l.line(e, PRUSSIAN, 0.7, 0.55)
    return s, l


def kettle():
    """The tea: a small square brazier on the ground and an iron kettle on it (its steam is the engine's smoke), two cups."""
    s, l = sheets()
    K = KETTLE
    X, Z = K["X"], K["Z"]
    CAM.box(s, X - 22, X + 22, 0, 34, Z - 22, Z + 22, lerp(WOOD_LIT, NAPLES, 0.1), WOOD_SH, top=lerp(PRUSSIAN, SIENNA, 0.4), lines=l)
    k = CAM.k(X, Z)
    c = g(X, Z, 34)
    iron, iron_lit = lerp(PRUSSIAN, SIENNA, 0.15), lerp(tintw(PRUSSIAN, 0.35), OCHRE, 0.1)
    s.ellipse(c[0], c[1] - 12 * k, 17 * k, 13 * k, iron)
    s.ellipse(c[0] + 5 * k, c[1] - 14 * k, 8 * k, 8 * k, iron_lit)
    s.line([(c[0] + 15 * k, c[1] - 14 * k), (c[0] + 25 * k, c[1] - 22 * k)], iron, max(1.0, 3.5 * k))          # the spout
    s.line(curve([(c[0] - 12 * k, c[1] - 20 * k), (c[0], c[1] - 33 * k), (c[0] + 12 * k, c[1] - 20 * k)], 8), WOOD_SH, max(0.8, 2.5 * k))   # the handle
    for dx in (-30, -48):
        p = g(X + dx, Z + 10, 34)
        s.ellipse(p[0], p[1], 4 * k, 2.4 * k, lerp(WHITE, CERULEAN, 0.2))
    return s, l, dict(spout=(c[0] + 25 * k, c[1] - 23 * k))


# ---------------------------------------------------------------- the house's noren
def noren(door):
    """O-Natsu's noren in her doorway: three panels of indigo, a white mark of our own (a rice bale in a ring) across
    the middle seam; its hem free (it stirs: fx sway). Whoever goes in passes behind it."""
    s, l = sheets()
    d0, d1 = door
    Zf = D.HOUSE["Zf"] + 3
    top, drop = 204.0, 82.0
    for i in range(3):
        u0, u1 = i / 3 + 0.012, (i + 1) / 3 - 0.012
        a0, a1 = d0 + (d1 - d0) * u0, d0 + (d1 - d0) * u1
        q = [g(a0, Zf, top), g(a1, Zf, top), g(a1, Zf, top - drop), g(a0, Zf, top - drop)]
        s.poly(q, INDIGO)
        l.line([q[3], q[0], q[1], q[2]], PRUSSIAN, 0.8, 0.7)
    l.line([g(d0 - 6, Zf, top + 2), g(d1 + 6, Zf, top + 2)], WOOD_SH, max(1.0, 4 * CAM.k(d0, Zf)), 1.0)
    # the mark: a ring and a rice bale in it, white, across the middle panel
    mx = (d0 + d1) / 2
    c = g(mx, Zf, top - drop * 0.48)
    k = CAM.k(mx, Zf)
    s.ellipse(c[0], c[1], 17 * k, 17 * k, lerp(WHITE, CERULEAN, 0.12))
    s.ellipse(c[0], c[1], 13 * k, 13 * k, INDIGO)
    s.ellipse(c[0], c[1], 9 * k, 5.5 * k, lerp(WHITE, CERULEAN, 0.12))
    for dx in (-4.5, 4.5):
        s.line([(c[0] + dx * k, c[1] - 5 * k), (c[0] + dx * k, c[1] + 5 * k)], INDIGO, max(0.6, 1.4 * k))
    return s, l


# ---------------------------------------------------------------- the lighter at the steps
def lighter_shape(sheet, lines, at, length, k, facing=1, cargo=True, poler=True, rng=None, alpha=1.0):
    """A lighter (a shallow cargo boat, poled), side on: (at) the waterline's middle, `length` px, `k` px per cm.
    Hull: a long low flat in shade with its lit upper strake, the bow rising a little; the cargo: rice bales under
    straw mats; the boatman at the stern with his pole."""
    x, y = at
    L = length
    f = facing
    hh = 55 * k                                            # freeboard
    sheer = lambda u: y - hh - (8 * k) * max(0, (u - 0.75) / 0.25) ** 2 - 2 * k * max(0, (0.15 - u) / 0.15)
    xs = lambda u: x + f * (u - 0.5) * L
    hull = [(xs(0.0), y - hh * 0.4), (xs(0.06), y), (xs(0.88), y), (xs(1.0), sheer(1.0))] + [(xs(u), sheer(u)) for u in np.linspace(1.0, 0.0, 12)]
    sheet.poly(hull, WOOD_SH, alpha)
    sheet.poly([(xs(u), sheer(u)) for u in np.linspace(0.02, 0.98, 12)] + [(xs(u), sheer(u) + 14 * k) for u in np.linspace(0.98, 0.02, 12)], lerp(WOOD_LIT, NAPLES, 0.1), alpha)
    lines.line([(xs(u), sheer(u)) for u in np.linspace(0, 1, 14)], SIENNA, max(0.5, min(1.0, k * 3)), 0.6 * alpha)
    lines.line(hull[:4], PRUSSIAN, max(0.5, min(1.0, k * 3)), 0.55 * alpha)
    if cargo:
        # bales under mats, a long low heap amidships
        for i in range(6):
            u = 0.22 + i * 0.09
            cx = xs(u)
            cy = sheer(u) - 18 * k
            sheet.ellipse(cx, cy, 22 * k, 17 * k, STRAW_LIT if i % 2 else lerp(STRAW_LIT, STRAW_SH, 0.3), alpha)
        sheet.poly([(xs(0.18), sheer(0.18) - 4 * k), (xs(0.30), sheer(0.30) - 40 * k), (xs(0.68), sheer(0.68) - 40 * k), (xs(0.76), sheer(0.76) - 4 * k)], lerp(STRAW_SH, NAPLES, 0.25), 0.88 * alpha)
        lines.line([(xs(0.30), sheer(0.30) - 40 * k), (xs(0.68), sheer(0.68) - 40 * k)], PRUSSIAN, max(0.5, min(0.9, k * 3)), 0.45 * alpha)
        for u in (0.36, 0.48, 0.6):
            lines.line([(xs(u), sheer(u) - 38 * k), (xs(u - f * 0.0), sheer(u))], STRAW_SH, max(0.5, k * 2.5), 0.6 * alpha)
    if poler and rng is not None:
        px = xs(0.1)
        figure(sheet, px, sheer(0.1), 150 * k, rng, robe=lerp(tintw(PRUSSIAN, 0.45), OCHRE, 0.2), sleeves="pole", head_cloth=True, alpha=alpha, line=k > 0.2)
    return hull


def lighter_moored():
    """A lighter tied up off the foot of the steps, loaded with bales under mats, nobody aboard (the family's, at the
    landing; or any lighter unloading). It rides (fx bob); the scene may hide it once the family's lighter has gone."""
    s, l = sheets()
    Zw = -2420.0
    a, b = g(-390.0, Zw, D.WATER_Y), g(20.0, Zw, D.WATER_Y)
    k = CAM.k(-185.0, Zw)
    at = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    hull = lighter_shape(s, l, at, b[0] - a[0], k, facing=-1, cargo=True, poler=False)
    # its pole laid along the cargo
    l.line([(at[0] - (b[0] - a[0]) * 0.42, at[1] - 70 * k), (at[0] + (b[0] - a[0]) * 0.36, at[1] - 62 * k)], WOOD_SH, max(0.8, 3.5 * k), 1.0)
    return s, l, dict(waterline=at, length=b[0] - a[0])


# ---------------------------------------------------------------- the market: the dealers, the water men
MARKET_FIGS = [
    # (X, Z, height cm, sleeves, robe, jacket, turn)  the back row first
    (55.0, -1532.0, 158, "up", 2, 0, -0.5), (128.0, -1545.0, 154, "one", 0, None, 0.3), (200.0, -1528.0, 160, "up", 1, 3, 0.0),
    (276.0, -1540.0, 155, "down", 3, 0, 0.6), (345.0, -1522.0, 157, "up", 0, None, -0.4),
    (92.0, -1472.0, 156, "one", 1, 0, 0.5), (168.0, -1458.0, 153, "up", 3, None, -0.3), (246.0, -1468.0, 158, "one", 2, 3, 0.2),
    (318.0, -1452.0, 155, "up", 1, 0, -0.6),
]
WATERMEN = [(-52.0, -1436.0, 150, "bucket"), (2.0, -1492.0, 152, "bucket")]
ROBES = None


def market():
    """The rice dealers who have not stopped after the close, in the road at the right: two rows of men in kimono, some
    in jackets, hands up, calling prices at each other; at their left end the two water men, robes tucked up, bare
    legs, head cloths, buckets in hand (one is about to throw: the splash is frames). Painted figures, flat, as the
    prints have their crowds; the game's own people (Rihei among them) stand in front."""
    s, l = sheets()
    rng = np.random.default_rng(1697)
    robes = [INDIGO, lerp(SIENNA, OCHRE, 0.28), lerp(tintw(PRUSSIAN, 0.42), OCHRE, 0.18), lerp(VIRIDIAN, PRUSSIAN, 0.35)]
    jackets = [lerp(PRUSSIAN, SIENNA, 0.25), INDIGO, lerp(WOOD_DARK, PRUSSIAN, 0.3), lerp(tintw(PRUSSIAN, 0.3), SIENNA, 0.3)]
    out = []
    for (X, Z, cm, sl, ri, ji, turn) in sorted(MARKET_FIGS, key=lambda f: f[1]):
        p = g(X, Z)
        hpx = cm * CAM.k(X, Z)
        figure(s, p[0], p[1], hpx, rng, robe=robes[ri], jacket=(jackets[ji] if ji is not None else None), sleeves=sl, turn=turn)
        out.append((p, hpx))
    for (X, Z, cm, sl) in sorted(WATERMEN, key=lambda f: f[1]):
        p = g(X, Z)
        hpx = cm * CAM.k(X, Z)
        figure(s, p[0], p[1], hpx, rng, robe=lerp(tintw(CERULEAN, 0.3), PRUSSIAN, 0.28), sleeves=sl, head_cloth=True, tucked=True)
        out.append((p, hpx))
    # spare buckets on the ground by the water men
    for (X, Z) in ((-112.0, -1392.0), (-86.0, -1372.0)):
        p = g(X, Z)
        k = CAM.k(X, Z)
        s.poly([(p[0] - 13 * k, p[1] - 26 * k), (p[0] + 13 * k, p[1] - 26 * k), (p[0] + 11 * k, p[1]), (p[0] - 11 * k, p[1])], WOOD_LIT)
        s.ellipse(p[0], p[1] - 26 * k, 13 * k, 4 * k, lerp(lerp(VIRIDIAN, OCHRE, 0.4), CERULEAN, 0.3))
        l.line([(p[0] - 12.5 * k, p[1] - 14 * k), (p[0] + 12.5 * k, p[1] - 14 * k)], WOOD_DARK, max(0.6, 2 * k), 0.9)
        l.line([(p[0] - 11 * k, p[1]), (p[0] - 13 * k, p[1] - 26 * k)], PRUSSIAN, 0.7, 0.5)
    # where the thrower's bucket is (the splash's origin): his right hand, as figure() places it
    X, Z, cm, _ = WATERMEN[0]
    p = g(X, Z)
    hp = cm * CAM.k(X, Z)
    sho_y = p[1] - hp * 0.845 + hp * 0.045
    hand = (p[0] + hp * 0.150 * 0.92 + hp * 0.05, sho_y + hp * 0.33)
    return s, l, dict(figs=out, bucket=(hand[0] + hp * 0.04, hand[1] - hp * 0.01))


# ---------------------------------------------------------------- the front plane
def front():
    """At the very front, bottom right: rice bales stacked on a straw mat, their round straw ends toward us (two below,
    one on top), bound at the ends, and a wooden bucket beside them: the nearest things in the picture."""
    s, l = sheets()
    X0, Z0 = 150.0, -900.0
    s.poly([g(X0 - 60, Z0 + 60), g(X0 + 220, Z0 + 60), g(X0 + 220, Z0 - 60), g(X0 - 60, Z0 - 60)], lerp(STRAW_LIT, STRAW_SH, 0.3))
    for (dx, y_) in ((0.0, 27.0), (58.0, 27.0), (116.0, 27.0), (29.0, 76.0), (87.0, 76.0)):
        X = X0 + dx
        p = g(X, Z0 + 40, y_)
        kk = CAM.k(X, Z0)
        rx, ry = 27 * kk, 25 * kk
        s.ellipse(p[0], p[1], rx, ry, STRAW_LIT if dx % 2 == 0 else lerp(STRAW_LIT, NAPLES, 0.2))
        s.ellipse(p[0] + rx * 0.16, p[1] + ry * 0.1, rx * 0.56, ry * 0.52, lerp(STRAW_LIT, STRAW_SH, 0.42))
        s.ellipse(p[0] + rx * 0.16, p[1] + ry * 0.1, rx * 0.22, ry * 0.2, STRAW_SH)
        for k_ in range(10):                                  # the straw ends, short strokes round the cap
            a_ = k_ / 10 * 2 * math.pi
            l.line([(p[0] + math.cos(a_) * rx * 0.6, p[1] + math.sin(a_) * ry * 0.6), (p[0] + math.cos(a_) * rx * 0.95, p[1] + math.sin(a_) * ry * 0.95)], STRAW_SH, max(0.6, 1.6 * kk), 0.5)
        l.line([(p[0] - rx * 0.78, p[1] - ry * 0.55), (p[0] - rx * 0.78, p[1] + ry * 0.55)], STRAW_SH, max(0.8, 3 * kk), 0.9)      # the binding
        l.line([(p[0] + rx * 0.78, p[1] - ry * 0.55), (p[0] + rx * 0.78, p[1] + ry * 0.55)], STRAW_SH, max(0.8, 3 * kk), 0.9)
        l.line([(p[0] + rx * math.cos(t_), p[1] + ry * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 24)], SIENNA, 0.9, 0.55)
    X, Z = X0 - 85.0, Z0 + 60.0
    p = g(X, Z)
    kk = CAM.k(X, Z)
    s.poly([(p[0] - 16 * kk, p[1] - 34 * kk), (p[0] + 16 * kk, p[1] - 34 * kk), (p[0] + 13 * kk, p[1]), (p[0] - 13 * kk, p[1])], WOOD_LIT)
    s.poly([(p[0] + 4 * kk, p[1] - 34 * kk), (p[0] + 16 * kk, p[1] - 34 * kk), (p[0] + 13 * kk, p[1]), (p[0] + 3 * kk, p[1])], lerp(WOOD_LIT, NAPLES, 0.2))
    s.ellipse(p[0], p[1] - 34 * kk, 16 * kk, 5 * kk, lerp(lerp(VIRIDIAN, OCHRE, 0.4), CERULEAN, 0.3))
    for v in (8, 26):
        l.line([(p[0] - 14.5 * kk, p[1] - v * kk), (p[0] + 14.5 * kk, p[1] - v * kk)], WOOD_DARK, max(0.8, 2.5 * kk), 0.9)
    l.line([(p[0] - 13 * kk, p[1]), (p[0] - 16 * kk, p[1] - 34 * kk)], PRUSSIAN, 0.9, 0.6)
    return s, l


# ---------------------------------------------------------------- frames of moving things (small cropped pictures)
def lighter_frame(length, k, seed, variant=0):
    """A lighter going by on the river, facing right (east on the stage... the engine turns it for the other way):
    -> (colour, coverage) on the stage-sized sheet, and its foot (the waterline's middle)."""
    s, l = sheets()
    rng = np.random.default_rng(seed)
    at = (400.0, 300.0)
    lighter_shape(s, l, at, length, k, facing=1, cargo=(variant != 1), poler=True, rng=rng)
    # the little bow wave and the wake: a few white marks at the waterline (they go with it)
    x, y = at
    s.line([(x + length * 0.48, y - 1), (x + length * 0.54, y + 1)], lerp(WHITE, CERULEAN, 0.2), max(0.8, 3 * k), 0.8)
    s.line([(x - length * 0.55, y + 1), (x - length * 0.40, y + 1)], lerp(WHITE, CERULEAN, 0.3), max(0.7, 2 * k), 0.6)
    return s, l, at


def runner_frames(height=74.0, n=4):
    """The price runner: a lad sprinting off with the day's price (a folded paper in his fist), robe tucked up, head
    cloth; a run cycle of `n` frames facing right."""
    out = []
    for i in range(n):
        s, l = sheets()
        ph = i / n * 2 * math.pi
        x, y = 400.0, 300.0
        h = height
        rng = np.random.default_rng(3)
        robe = lerp(tintw(OCHRE, 0.25), SIENNA, 0.4)
        lean = 0.16 * h
        hip = (x + lean * 0.3, y - h * 0.48)
        neck = (x + lean, y - h * 0.84)
        # legs: thigh and shin, swinging
        for side in (0, 1):
            a = ph + side * math.pi
            kx = hip[0] + math.sin(a) * h * 0.20
            ky = hip[1] + h * 0.22 - max(0, math.sin(a)) * h * 0.05
            fx_ = kx + math.sin(a - 0.9) * h * 0.18 - h * 0.04
            fy_ = min(y, ky + h * 0.24 + max(0, -math.cos(a)) * -h * 0.06)
            c = FLESH_SH if side == 0 else lerp(FLESH_SH, SIENNA, 0.25)
            s.line([hip, (kx, ky), (fx_, fy_)], c, max(1.2, h * 0.055))
        # the body: the tucked robe as a wedge from the neck to the hips
        body = [(neck[0] - h * 0.10, neck[1] + h * 0.02), (neck[0] + h * 0.09, neck[1] + h * 0.03), (hip[0] + h * 0.12, hip[1] + h * 0.06), (hip[0] - h * 0.12, hip[1] + h * 0.07)]
        s.poly(body, robe)
        s.line([(hip[0] - h * 0.12, hip[1] - h * 0.02), (hip[0] + h * 0.12, hip[1] - h * 0.03)], shade(robe, 0.5), max(0.8, h * 0.03))
        # arms pumping; the front fist holds the paper
        for side in (0, 1):
            a = ph + side * math.pi + math.pi
            sx, sy = neck[0] + h * 0.01, neck[1] + h * 0.06
            ex, ey = sx + math.sin(a) * h * 0.14, sy + h * 0.13
            hx, hy = ex + math.sin(a + 0.9) * h * 0.12 + h * 0.05, ey - h * 0.04
            s.line([(sx, sy), (ex, ey), (hx, hy)], robe if side else shade(robe, 0.25), max(1.0, h * 0.045))
            s.ellipse(hx, hy, h * 0.025, h * 0.025, FLESH)
            if side == 0:
                s.poly([(hx + h * 0.01, hy - h * 0.05), (hx + h * 0.07, hy - h * 0.04), (hx + h * 0.06, hy + h * 0.01), (hx, hy)], lerp(WHITE, NAPLES, 0.15))
        hx_, hy_ = neck[0] + h * 0.03, neck[1] - h * 0.075
        s.ellipse(hx_, hy_, h * 0.06, h * 0.07, FLESH)
        s.poly([(hx_ - h * 0.065, hy_ - h * 0.01), (hx_ + h * 0.06, hy_ - h * 0.02), (hx_ + h * 0.05, hy_ - h * 0.07), (hx_ - h * 0.06, hy_ - h * 0.065)], tintw(CERULEAN, 0.65))
        l.line(body + [body[0]], PRUSSIAN, 0.8, 0.5)
        out.append((s, l, (x, y)))
    return out


def splash_frames(origin, n=5):
    """A bucket's splash thrown at the dealers: water leaving the bucket's mouth up and to the right, an arc that opens
    into drops, and falls. `origin` the bucket's mouth (stage px). Lead white and cerulean, flat, a prussian breath."""
    out = []
    ox, oy = origin
    rng = np.random.default_rng(9)
    for i in range(n):
        s, l = sheets()
        t = (i + 1) / n
        reach = 34 + 60 * t
        arc = [(ox + reach * u, oy - 30 * math.sin(math.pi * u * 0.9) * (0.6 + 0.4 * t) + 18 * u * u * t) for u in np.linspace(0, 1, 12)]
        width = 6.0 * (1 - t) + 2.0
        if i < n - 1:
            s.line(arc[: max(3, int(12 * (1.15 - t)))], lerp(WHITE, CERULEAN, 0.30), width, 0.9)
            s.line(arc[: max(3, int(12 * (1.15 - t)))], lerp(WHITE, NAPLES, 0.15), max(1.0, width * 0.4), 0.95)
        for j in range(int(6 + 10 * t)):
            u = rng.uniform(0.3, 1.0)
            px = ox + reach * u + rng.uniform(-6, 10) * t
            py = oy - 30 * math.sin(math.pi * u * 0.9) * (0.6 + 0.4 * t) + 18 * u * u * t + rng.uniform(-5, 8) * t + 10 * t * t
            r = rng.uniform(0.9, 2.2)
            s.ellipse(px, py, r, r * 1.2, lerp(WHITE, CERULEAN, 0.25 + 0.2 * rng.random()))
        out.append((s, l, origin))
    return out

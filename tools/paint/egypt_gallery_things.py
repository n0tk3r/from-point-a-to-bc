"""The things people have left about in the gallery: oil jars and spare lamps, rope, a sledge runner, tools,
the builders' red marks; and the two mirrors and the dark things at the front of the picture, which are cut-outs.

Every thing is placed in the world (centimetres) and drawn at the size the perspective gives it there.
`pw(X, Y, Z)` turns a place in the world into a place in the picture."""

import math

import numpy as np

from brush import *
import egypt_gallery_kit as K

TILT = 0.36                                  # how much of a level circle's depth we see from up here, near the foot

CLAY = dict(hi="#ffd08a", lit="#e2904c", mid="#a85c36", shade="#5c3028", deep="#2c1a22", rim="#6f88ac")
ROPE = dict(hi="#f4d490", lit="#c99c5c", mid="#8c6638", shade="#4c3528", deep="#2a1e20")
WOOD = dict(hi="#e8b878", lit="#b88450", mid="#7c5434", shade="#422c24", deep="#241a1c")
LINEN = dict(hi="#fff0cc", lit="#e2cc9c", mid="#a88c68", shade="#5c4a48")


def profile_jar(sheet, cx, by, hgt, wid, col, shape=None, cap=None, light=1, band=None):
    """A pot standing with the middle of its foot at (cx, by), `hgt` tall and `wid` across at its widest
    (picture pixels). `light` is +1 when the lamp is on its right, -1 on its left; the other side takes a
    cool rim from the daylight. `cap`: "linen" for a tied cloth cover, "open" for a dark mouth."""
    shape = shape or [(0.0, 0.34), (0.07, 0.6), (0.28, 0.92), (0.52, 1.0), (0.72, 0.88), (0.86, 0.56), (0.92, 0.44), (0.96, 0.5), (1.0, 0.52)]
    r = wid / 2

    def side(f, k=1.0):                      # the outline at a share `f` of the half width, from foot to lip
        return [(cx + f * r * rad * k, by - t * hgt) for t, rad in shape]
    def strip(f0, f1, color, alpha=1.0):
        sheet.poly(side(f0) + side(f1)[::-1], color, alpha)
    sheet.ellipse(cx, by - 1, r * shape[0][1] * 1.05, r * shape[0][1] * TILT, col["deep"])     # the foot
    strip(-1, 1, col["mid"])
    strip(-1 * light, -0.25 * light, col["shade"])
    strip(-1 * light, -0.72 * light, col["deep"], 0.85)
    strip(0.18 * light, 0.86 * light, col["lit"])
    strip(0.42 * light, 0.66 * light, col["hi"], 0.9)
    strip(-1.0 * light, -0.86 * light, col["rim"], 0.75)                                      # cool light from the way in
    if band:                                 # a rope sling or a painted band round the shoulder
        t = band
        rad = np.interp(t, [p[0] for p in shape], [p[1] for p in shape]) * r
        pts = [(cx + math.cos(a) * rad, by - t * hgt + math.sin(a) * rad * TILT) for a in np.linspace(0, math.pi, 12)]
        sheet.line(pts, "#3a2a22", max(1.0, hgt * 0.035), 0.9)
        sheet.line([(x, y - 0.8) for x, y in pts[2:7]] if light > 0 else [(x, y - 0.8) for x, y in pts[5:10]], "#e8c88a", 0.9, 0.8)
    top_r, ty = r * shape[-1][1], by - hgt
    if cap == "linen":
        dome = [(cx + math.cos(a) * top_r * 1.12, ty - math.sin(a) * top_r * 0.75) for a in np.linspace(0, math.pi, 12)]
        skirt = [(cx - top_r * 1.2, ty + hgt * 0.07), (cx - top_r * 0.6, ty + hgt * 0.085), (cx, ty + hgt * 0.075), (cx + top_r * 0.7, ty + hgt * 0.09), (cx + top_r * 1.2, ty + hgt * 0.065)]
        sheet.poly(dome + skirt, LINEN["mid"])
        lit = [p for p in dome if (p[0] - cx) * light > -top_r * 0.2]
        sheet.poly(lit + [(cx + light * top_r * 1.15, ty + hgt * 0.06), (cx - light * top_r * 0.1, ty + hgt * 0.05)], LINEN["lit"])
        sheet.ellipse(cx + light * top_r * 0.4, ty - top_r * 0.4, top_r * 0.4, top_r * 0.22, LINEN["hi"], 0.9)
        sheet.line([(cx - top_r * 1.05, ty + hgt * 0.03), (cx, ty + hgt * 0.045), (cx + top_r * 1.05, ty + hgt * 0.03)], "#4a3428", max(0.9, hgt * 0.022))   # the cord
    else:
        sheet.ellipse(cx, ty, top_r, top_r * TILT, col["lit"])
        sheet.ellipse(cx, ty + top_r * 0.06, top_r * 0.8, top_r * TILT * 0.74, "#1c1218")
        sheet.line([(cx + math.cos(a) * top_r, ty - math.sin(a) * top_r * TILT) for a in np.linspace(0.2, 2.9, 9)], col["hi"], 0.9, 0.8)
    return sheet


def on_floor(pw, X, Z, Y=0.0):
    """-> (picture x, picture y, pixels per cm) of a place."""
    x, y = pw(X, Y, Z)
    return x, y, K.F / Z


def shadow_on(pic, ground, cx, cy, rx, ry, amount=0.5, color="#3a2c3c", soft=2.0):
    """A soft dark pool under a thing, only where the picture shows `ground`."""
    m = mask_ellipse(pic.shape[:2], cx, cy, rx, max(1.2, ry), soft=soft) * ground
    tint(pic, color, np.clip(m * amount, 0, 1).astype(F32))


def dishes(sheet, cx, by, k, n=5, light=1):
    """Spare lamp dishes, stacked."""
    r = 9.0 * k
    for i in range(n):
        y = by - i * 2.6 * k
        sheet.ellipse(cx + (i % 2) * 0.6, y, r, r * TILT * 1.1, "#4a2820")
        sheet.ellipse(cx + (i % 2) * 0.6, y - 1.6 * k, r, r * TILT, "#b46a3e")
        sheet.ellipse(cx + (i % 2) * 0.6 + light * r * 0.35, y - 1.8 * k, r * 0.5, r * TILT * 0.5, "#eea660", 0.9)
    sheet.ellipse(cx, by - (n - 1) * 2.6 * k - 1.2 * k, r * 0.72, r * TILT * 0.66, "#3a1c1a")
    return sheet


def coil(sheet, cx, by, k, turns=4, light=1, tail=None, seed=0):
    """A coil of thick rope lying on the ground."""
    rng = np.random.default_rng(seed)
    r = 21.0 * k
    for i in range(turns):
        y = by - i * 3.4 * k
        rr_ = r * (1 - 0.05 * i) + rng.normal(0, 0.5)
        ring = [(cx + math.cos(a) * rr_ + rng.normal(0, 0.3), y + math.sin(a) * rr_ * TILT) for a in np.linspace(0, 2 * math.pi, 26)]
        sheet.line(ring, ROPE["shade"], 4.6 * k, 1.0)
        sheet.line(ring, ROPE["mid"], 3.0 * k, 1.0)
        a0 = 3.5 if light < 0 else 4.4
        sheet.line([(cx + math.cos(a) * rr_, y + math.sin(a) * rr_ * TILT - 0.7 * k) for a in np.linspace(a0, a0 + 1.6, 9)], ROPE["lit"], 2.0 * k, 0.95)
        sheet.line([(cx + math.cos(a) * rr_, y + math.sin(a) * rr_ * TILT - 1.0 * k) for a in np.linspace(a0 + 0.5, a0 + 1.1, 5)], ROPE["hi"], 1.1 * k, 0.9)
        for a in np.linspace(0.3, math.pi - 0.3, 9):                                                   # the lay of the rope
            px_, py_ = cx + math.cos(a) * rr_, y + math.sin(a) * rr_ * TILT
            sheet.line([(px_ - 1.2 * k, py_ - 1.6 * k), (px_ + 1.2 * k, py_ + 1.6 * k)], ROPE["deep"], 0.8, 0.55)
    sheet.ellipse(cx, by - (turns - 1) * 3.4 * k, r * 0.5, r * 0.5 * TILT, "#1c1418")                   # the hole in the middle
    if tail:
        pts = curve([(cx + r * 0.9, by)] + list(tail), 8)
        sheet.line(pts, ROPE["shade"], 3.4 * k)
        sheet.line([(x, y - 0.8 * k) for x, y in pts], ROPE["lit"], 1.6 * k, 0.9)
    return sheet


def timber(sheet, pw, a, b, wide, thick, col=WOOD, up=0.0, nose=0.0):
    """A squared baulk of wood lying from world place `a` to `b` (its near lower edge), `wide` across and
    `thick` high. `nose` curls the far end up by that many cm (a sledge runner)."""
    (ax, ay, az), (bx, by, bz) = a, b
    n = 10
    low, high, back = [], [], []
    for i in range(n + 1):
        t = i / n
        lift = nose * max(0.0, (t - 0.72) / 0.28) ** 2
        X, Y, Z = ax + (bx - ax) * t, ay + (by - ay) * t + lift, az + (bz - az) * t
        low.append(pw(X, Y, Z))
        high.append(pw(X, Y + thick, Z))
        back.append(pw(X + wide, Y + thick, Z))
    sheet.poly(low + high[::-1], col["shade"])                                 # the side toward the middle of the gallery
    sheet.poly(high + back[::-1], col["mid"])                                  # the top
    sheet.line(high, col["lit"], 1.1, 0.9)
    for i in range(1, n, 2):                                                   # grain, and the notches where it was lashed
        sheet.line([lerp(np.array(high[i]), np.array(back[i]), 0.25), lerp(np.array(high[i + 1]), np.array(back[i + 1]), 0.3)], col["shade"], 0.8, 0.6)
    for t in (0.2, 0.55):
        i = int(t * n)
        sheet.line([high[i], back[i]], col["deep"], 1.6, 0.8)
        sheet.line([low[i], high[i]], col["deep"], 1.6, 0.8)
    sheet.poly([low[0], high[0], back[0], pw(ax + wide, ay, az)], col["deep"])  # the near end, cut square
    sheet.line([high[0], back[0]], col["hi"], 1.0, 0.8)
    return sheet


def chips(sheet, pw, rng, spots, tones=("#f2dcae", "#c8a678", "#6c5048")):
    """Stone chips and dust swept to the edges: (X, Z, spread across, spread along, how many) on the level floor."""
    for (X, Z, sx, sz, n) in spots:
        for _ in range(n):
            x, y = pw(X + rng.normal(0, sx), 0.0, Z + rng.normal(0, sz))
            r = 0.8 + rng.random() * 1.8
            sheet.ellipse(x + r * 0.5, y + r * 0.3, r * 1.2, r * 0.5, tones[2], 0.55)
            sheet.ellipse(x, y, r, r * 0.6, tones[0] if rng.random() < 0.45 else tones[1], 0.9)
    return sheet


def marks(pic, pw, rng, z0=470.0, z1=612.0, level=166.0, wall=K.HALF, amount=0.78):
    """The builders' marks, daubed in red ochre on the right-hand wall: a levelling line struck along the
    stone with a cord, the little triangle that points to it, tallies, and a gang's sign."""
    s = Sheet(pic.shape[:2])
    red = "#ffffff"

    def at(Z, Y):
        return pw(wall, Y, Z)
    n = 22
    for i in range(n):                                                         # the line, struck with a wet cord: broken and blobbed
        if rng.random() < 0.12:
            continue
        za, zb = lerp(z0, z1, i / n), lerp(z0, z1, (i + 1) / n)
        s.line([at(za, level + rng.normal(0, 0.5)), at(zb, level + rng.normal(0, 0.5))], red, 1.2 + rng.random() * 1.2, 0.6 + 0.4 * rng.random())
    zc = lerp(z0, z1, 0.60)
    s.poly([at(zc - 13, level + 24), at(zc + 13, level + 24), at(zc, level + 3)], red, 0.9)                       # the triangle standing on its point
    s.poly([at(zc - 6, level + 20), at(zc + 6, level + 20), at(zc, level + 10)], "#000000", 0.0)
    for i in range(4):                                                         # tallies
        zt = lerp(z0, z1, 0.20) + i * 9
        s.line([at(zt + rng.normal(0, 1), level + 44), at(zt + 2 + rng.normal(0, 1), level + 18)], red, 2.0, 0.85)
    s.line([at(lerp(z0, z1, 0.18), level + 30), at(lerp(z0, z1, 0.18) + 34, level + 34)], red, 1.6, 0.8)          # struck through
    zg = lerp(z0, z1, 0.86)                                                    # the gang's sign: a ring with a stroke, and a hook
    ring = [at(zg + math.cos(a) * 11, level + 46 + math.sin(a) * 13) for a in np.linspace(0, 2 * math.pi, 14)]
    s.line(ring, red, 2.0, 0.85)
    s.line([at(zg, level + 26), at(zg, level + 66)], red, 1.8, 0.8)
    s.line([at(zg - 26, level + 58), at(zg - 20, level + 30), at(zg - 30, level + 24)], red, 1.8, 0.8)
    for i in range(5):                                                         # cubits ticked off under the line
        zt = lerp(z0, z1, 0.08 + 0.2 * i)
        s.line([at(zt, level - 2), at(zt, level - 9)], red, 1.3, 0.7)
    _, a = s.done()
    a = warp(a, 0.9, 5.0, 31) * (0.6 + 0.5 * noise(pic.shape[:2], 9, 32, 3))    # paint on rough stone: thin in places
    tint(pic, "#c2472c", np.clip(a * amount, 0, 1).astype(F32))
    return a


def basket(sheet, cx, by, k, light=1):
    """A shallow basket of coiled palm leaf with flat loaves in it."""
    r = 17.0 * k
    sheet.poly([(cx - r * 0.72, by), (cx + r * 0.72, by), (cx + r, by - 9 * k), (cx - r, by - 9 * k)], "#6e4c2c")
    sheet.ellipse(cx, by, r * 0.72, r * 0.72 * TILT, "#6e4c2c")
    for i in range(3):
        sheet.line([(cx - r * (0.76 + 0.08 * i), by - (2 + 2.6 * i) * k), (cx + r * (0.76 + 0.08 * i), by - (2 + 2.6 * i) * k)], "#3e2a1e", 0.8, 0.7)
    sheet.ellipse(cx, by - 9 * k, r, r * TILT, "#c69a56")
    sheet.ellipse(cx, by - 9 * k, r * 0.84, r * TILT * 0.8, "#4a3220")
    for (ox, oy, rr_) in ((-0.3, 0.0, 0.5), (0.34, -0.1, 0.46), (0.02, -0.5, 0.42)):                    # the loaves
        sheet.ellipse(cx + ox * r, by - 10 * k + oy * r * TILT - 1.2 * k, rr_ * r, rr_ * r * 0.6, "#b8864a")
        sheet.ellipse(cx + ox * r + light * 1.2 * k, by - 10 * k + oy * r * TILT - 2.0 * k, rr_ * r * 0.7, rr_ * r * 0.36, "#f0cc8a")
    return sheet


def mat(sheet, pw, x0, x1, z0, z1, y):
    """A mat of plaited reed lying on a level place: pale, with the plaiting drawn across it and a frayed end."""
    q = [pw(x0, y, z0), pw(x1, y, z0), pw(x1, y, z1), pw(x0, y, z1)]
    sheet.poly(q, "#c8a868")
    n = 22
    for i in range(1, n):
        t = i / n
        a = (lerp(q[0][0], q[3][0], t), lerp(q[0][1], q[3][1], t))
        b = (lerp(q[1][0], q[2][0], t), lerp(q[1][1], q[2][1], t))
        sheet.line([a, b], "#96783f" if i % 2 else "#e8d08e", 0.8, 0.5)
    for t in (0.33, 0.67):                                                                           # the cords that bind the reeds
        a = (lerp(q[0][0], q[1][0], t), lerp(q[0][1], q[1][1], t))
        b = (lerp(q[3][0], q[2][0], t), lerp(q[3][1], q[2][1], t))
        sheet.line([a, b], "#7a5a30", 1.1, 0.8)
    sheet.line([q[0], q[3]], "#6a5030", 1.2, 0.9)
    sheet.line([q[1], q[2]], "#6a5030", 1.0, 0.7)
    for i in range(9):                                                                               # the frayed near end
        t = (i + 0.5) / 9
        a = (lerp(q[0][0], q[1][0], t), lerp(q[0][1], q[1][1], t))
        sheet.line([a, (a[0] - 1.2, a[1] + 3.6)], "#d8bc7c", 0.9, 0.8)
    return sheet


ALABASTER = dict(hi="#fffaf0", lit="#f2e2c0", mid="#c8b08a", shade="#7c6a62", deep="#44383e", rim="#7088a8")


def chest(sheet, pw, x0, x1, z0, z1, y0, hgt):
    """One of the king's chests, set down on the bench by porters who would go no further: dark wood banded
    with gold, on two carrying poles. We see its end and the side that faces the middle of the gallery."""
    y1 = y0 + hgt
    end = [pw(x0, y0 + 5, z0), pw(x1, y0 + 5, z0), pw(x1, y1, z0), pw(x0, y1, z0)]
    side = [pw(x0, y0 + 5, z0), pw(x0, y0 + 5, z1), pw(x0, y1, z1), pw(x0, y1, z0)]
    for xp in (x0 + 6, x1 - 6):                                                 # the poles, sticking out toward us
        a, b = pw(xp, y0 + 4, z0 - 46), pw(xp, y0 + 4, z0)
        sheet.line([a, b], "#5a3c24", 2.4)
        sheet.line([(a[0], a[1] - 0.8), (b[0], b[1] - 0.8)], "#d8aa6c", 1.0, 0.9)
    sheet.poly(side, "#5c3822")
    sheet.poly(end, "#9a6236")
    lid = lambda t: (lerp(end[3][0], end[2][0], t), lerp(end[3][1], end[2][1], t))
    sheet.poly([end[3], end[2], (lid(0.9)[0], lid(0.9)[1] - hgt * 0.02), (lid(0.5)[0], lid(0.5)[1] - 3.0), (lid(0.1)[0], lid(0.1)[1] - hgt * 0.02)], "#b87a40")   # a low arched lid
    for t in (0.08, 0.92):                                                      # gold at the corners and along the lid
        a = (lerp(end[0][0], end[1][0], t), lerp(end[0][1], end[1][1], t))
        b = (lerp(end[3][0], end[2][0], t), lerp(end[3][1], end[2][1], t))
        sheet.line([a, b], "#ffd768", 1.6)
    sheet.line([end[3], end[2]], "#ffe890", 1.4)
    sheet.line([end[0], end[1]], "#d8a440", 1.3)
    for t in (0.12, 0.5, 0.88):
        a = (lerp(side[0][0], side[1][0], t), lerp(side[0][1], side[1][1], t))
        b = (lerp(side[3][0], side[2][0], t), lerp(side[3][1], side[2][1], t))
        sheet.line([a, b], "#c8963c", 1.2, 0.9)
    sheet.line([side[3], side[2]], "#e8b850", 1.1, 0.9)
    c = ((end[0][0] + end[2][0]) / 2, (end[0][1] + end[2][1]) / 2)
    sheet.ellipse(c[0], c[1], 1.6, 1.6, "#fff2b0")                             # the knob the cord is sealed to
    return sheet


# ---------------------------------------------------------------- the cut-outs
CHROME = dict(shine="#ffffff", light="#d8dde2", mid="#9aa2aa", dark="#565c66", line="#2c2f3a")     # as on the wagon


def _turn(c, pts, deg):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + x * ca - y * sa, c[1] + x * sa + y * ca) for x, y in pts]


def _round_box(w, h, r, n=5):
    """A box with rounded corners, round its own middle."""
    out = []
    for (sx, sy, a0) in ((1, -1, -90), (1, 1, 0), (-1, 1, 90), (-1, -1, 180)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            out.append((sx * (w / 2 - r) + math.cos(a) * r, sy * (h / 2 - r) + math.sin(a) * r))
    return out


def car_mirror(sheet, foot, s=1.0, tilt=-17.0):
    """The wagon's door mirror: a chrome head on a short chrome arm, its mounting plate wedged down into the
    slot at `foot`. It leans, glass toward the way in, and the glass has the daylight in it."""
    fx, fy = foot
    head = (fx - 5.5 * s, fy - 25.0 * s)
    # the arm, from the plate in the slot up to the back of the head
    sheet.poly([(fx - 5 * s, fy + 1.5 * s), (fx + 5 * s, fy + 1.5 * s), (fx + 3 * s, fy - 4 * s), (fx - 1.0 * s, fy - 15 * s), (fx - 6.5 * s, fy - 15 * s), (fx - 4 * s, fy - 4 * s)], CHROME["line"])
    sheet.poly([(fx - 4 * s, fy + 0.5 * s), (fx + 4 * s, fy + 0.5 * s), (fx + 2 * s, fy - 4 * s), (fx - 2.0 * s, fy - 15 * s), (fx - 5.5 * s, fy - 15 * s), (fx - 3 * s, fy - 4 * s)], CHROME["mid"])
    sheet.line([(fx - 3.2 * s, fy - 3 * s), (fx - 5.0 * s, fy - 14 * s)], CHROME["shine"], 1.2 * s)
    sheet.line([(fx + 1.6 * s, fy - 3 * s), (fx - 2.2 * s, fy - 14 * s)], CHROME["dark"], 1.1 * s)
    sheet.line([(fx - 4 * s, fy - 0.3 * s), (fx + 4 * s, fy - 0.3 * s)], "#ffc27a", 1.0 * s, 0.9)          # the lamp below, in the plate
    # the head
    sheet.poly(_turn(head, _round_box(33 * s, 22.5 * s, 6.5 * s), tilt), CHROME["line"])
    sheet.poly(_turn(head, _round_box(30.5 * s, 20 * s, 5.5 * s), tilt), CHROME["mid"])
    sheet.poly(_turn(head, [(-14 * s, -9.5 * s), (13 * s, -9.5 * s), (11 * s, -6.5 * s), (-12.5 * s, -6.5 * s)], tilt), CHROME["shine"])   # the top of the shell
    sheet.poly(_turn(head, [(-13 * s, 7.4 * s), (13 * s, 7.4 * s), (11.5 * s, 9.6 * s), (-11.5 * s, 9.6 * s)], tilt), "#e0a060")           # its underside, in lamplight
    sheet.poly(_turn(head, [(12.2 * s, -7 * s), (14.8 * s, -6 * s), (14.8 * s, 6 * s), (12.2 * s, 7 * s)], tilt), CHROME["dark"])
    # the glass
    sheet.poly(_turn(head, _round_box(24.5 * s, 14.5 * s, 3.6 * s), tilt), "#1c2440")
    sheet.poly(_turn(head, [(-12 * s, -7 * s), (3 * s, -7 * s), (-5 * s, 7 * s), (-12 * s, 7 * s)], tilt), "#8fb6de")                     # daylight from the way in
    sheet.poly(_turn(head, [(-12 * s, -7 * s), (-4 * s, -7 * s), (-10.5 * s, 4 * s), (-12 * s, 4 * s)], tilt), "#e4f2ff")
    sheet.poly(_turn(head, [(5.5 * s, -7 * s), (8.5 * s, -7 * s), (0.5 * s, 7 * s), (-2.5 * s, 7 * s)], tilt), "#4a6a9c", 0.9)
    sheet.poly(_turn(head, [(4 * s, 4.2 * s), (11.8 * s, 4.2 * s), (11.8 * s, 6.8 * s), (2.6 * s, 6.8 * s)], tilt), "#f0a050", 0.95)      # and a lamp, low in it
    return sheet


def hand_mirror(sheet, foot, s=1.0):
    """The goldsmith's mirror: a disc of polished copper, a little wider than it is high, on a short handle
    carved like a papyrus stem. Propped upright on the step with a chip of stone behind its foot."""
    fx, fy = foot
    cx, cy = fx + 1.0 * s, fy - 17.5 * s
    sheet.poly([(fx + 3 * s, fy + 0.5 * s), (fx + 10 * s, fy + 0.5 * s), (fx + 8.5 * s, fy - 4.5 * s), (fx + 4.5 * s, fy - 5 * s)], "#4c4654")   # the chip of stone
    sheet.poly([(fx + 4.5 * s, fy - 5 * s), (fx + 8.5 * s, fy - 4.5 * s), (fx + 7.5 * s, fy - 3 * s), (fx + 4 * s, fy - 3.2 * s)], "#c8ad84")
    sheet.ellipse(cx, cy, 10.6 * s, 9.6 * s, "#3a1c14")                                        # a dark line round the disc
    sheet.ellipse(cx, cy, 9.5 * s, 8.5 * s, "#e58a44")
    sheet.ellipse(cx - 1.5 * s, cy + 2.0 * s, 7.2 * s, 5.6 * s, "#b8602c", 0.85)               # the lower part gives back the dark stair
    sheet.ellipse(cx + 1.5 * s, cy - 2.2 * s, 6.6 * s, 4.8 * s, "#ffbe72")
    sheet.ellipse(cx + 3.0 * s, cy - 3.6 * s, 3.2 * s, 2.2 * s, "#fff2d0")
    sheet.poly([(cx - 5.2 * s, cy + 8.2 * s), (cx + 5.2 * s, cy + 8.2 * s), (cx + 2.2 * s, cy + 12 * s), (cx - 2.2 * s, cy + 12 * s)], "#3a2418")   # the flower of the papyrus, under the disc
    sheet.poly([(cx - 4.2 * s, cy + 8.6 * s), (cx + 4.2 * s, cy + 8.6 * s), (cx + 1.6 * s, cy + 11.4 * s), (cx - 1.6 * s, cy + 11.4 * s)], "#f0deb0")
    sheet.poly([(fx - 2.6 * s, fy + 0.5 * s), (fx + 2.6 * s, fy + 0.5 * s), (cx + 2.2 * s, cy + 11.4 * s), (cx - 2.2 * s, cy + 11.4 * s)], "#3a2418")
    sheet.poly([(fx - 1.6 * s, fy), (fx + 1.6 * s, fy), (cx + 1.3 * s, cy + 11.4 * s), (cx - 1.3 * s, cy + 11.4 * s)], "#dcc694")
    sheet.line([(fx - 1.6 * s, fy - 3 * s), (fx + 1.8 * s, fy - 3 * s)], "#8a5a30", 1.0 * s)
    return sheet


def front_left(sheet, P):
    """At the very front on the left: a ladder leaning in the corner (for whoever trims the lamps high up) and
    a tall oil jar behind its foot: dark against the daylight, with the cold light along their edges."""
    x, y = P(-212.0, 0.0, 345.0)
    k = K.F / 345.0
    dark = dict(hi="#6a84ac", lit="#3c3c58", mid="#2a2232", shade="#1c1622", deep="#120e18", rim="#141018")
    profile_jar(sheet, x, y, 100 * k, 44 * k, dark, cap="linen", band=0.62, light=1)
    rails = (((-203.0, 0.0, 330.0), (-218.5, 318.0, 368.0)), ((-168.0, 0.0, 346.0), (-218.5, 318.0, 404.0)))
    ends = [(P(*a), P(*b)) for a, b in rails]
    for i in range(1, 9):                                                                                # the rungs, lashed on
        t = i / 9.2 + 0.02
        l = (lerp(ends[0][0][0], ends[0][1][0], t), lerp(ends[0][0][1], ends[0][1][1], t))
        r = (lerp(ends[1][0][0], ends[1][1][0], t), lerp(ends[1][0][1], ends[1][1][1], t))
        sheet.line([l, r], "#15101a", 5.0)
        sheet.line([(l[0] + 3, l[1] - 1.8), (r[0] - 3, r[1] - 1.8)], "#4a4460", 1.3, 0.9)
        for q in (l, r):
            sheet.line([(q[0] - 3.2, q[1] - 3.2), (q[0] + 3.2, q[1] + 3.2)], "#5c5870", 1.4, 0.9)          # the lashing
            sheet.line([(q[0] - 3.2, q[1] + 3.2), (q[0] + 3.2, q[1] - 3.2)], "#5c5870", 1.4, 0.9)
    for (p0, p1) in ends:
        w = 8.5
        sheet.line([p0, p1], "#17121a", w)
        sheet.line([(p0[0] + w * 0.30, p0[1]), (p1[0] + w * 0.30, p1[1])], "#372e40", w * 0.36)
        sheet.line([(p0[0] + w * 0.44, p0[1]), (p1[0] + w * 0.44, p1[1])], "#8fa8cc", 1.2, 0.9)           # daylight on the edge
    return sheet


def front_right(sheet, P, lamp):
    """At the very front on the right, on the level bench: the boy's water jar, a cup, and a lamp burning."""
    x, y = P(210.0, K.BENCH, 392.0)
    k = K.F / 392.0
    profile_jar(sheet, x, y, 44 * k, 30 * k, CLAY, cap="open", light=-1, band=0.7)
    x, y = P(183.0, K.BENCH, 386.0)
    k = K.F / 386.0
    profile_jar(sheet, x, y, 13 * k, 13 * k, CLAY, cap="open", light=1, shape=[(0.0, 0.5), (0.3, 0.8), (0.7, 0.95), (1.0, 1.0)])
    return lamp(198.0, K.BENCH, 424.0)

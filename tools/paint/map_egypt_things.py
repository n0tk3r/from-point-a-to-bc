"""The drawings on the map of Egypt (MAP-15E): what the scribe put on the papyrus, one pen to a layer.

    back      the lie of the land: the river (zigzag water between two lines, fish and lotus in it), the edge of the
              desert, the far small pyramids, and the Horizon's outline seen from the river, its inside left blank
    river     the wagon nose down among the reeds and palms at the water's edge, and Lot's donkey drinking
    site      the works at the pyramid's foot: the stone yard, the scribe's awning, the sledge with its block, the
              scaffold on the face, and the stair up the face to the entrance
    gallery   inside the outline: the long passage climbing steeply, its lamps as small red dots
    chamber   the room at the top of the gallery, the king's furniture as small shapes, its far wall plain
    ways      the track up from the river (red, with small footprints); the way up the stair and in at the entrance;
              the ramp up to the doorway at the top

Drawn as an Egyptian draws: everything stands upright on its own ground line and is seen from its most telling
side, water as zigzags, reeds as upright strokes with heads, a building as its outline. The wagon is a thing the
scribe had no word for, so it is drawn neat and a little wrong: all four wheels in a row, its luggage tied on top
like a donkey's load. No people (the portraits are the engine's), no light, and nothing that says anything."""

import math

import numpy as np

from brush import curve
import map_egypt_kit as K
from map_egypt_kit import (APEX, BASE_Y, CHAMBER, ENTRANCE, GALLERY_FOOT, GALLERY_TOP, GOLD, GREEN, JOIN, LEFT, LOTUS,
                           RIGHT, RIVER_BOTTOM, RIVER_TOP, WAGON, WATER, Pen, left_x, path, right_x)


def rot(points, deg, about):
    ca, sa = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    ax, ay = about
    return [(ax + (x - ax) * ca - (y - ay) * sa, ay + (x - ax) * sa + (y - ay) * ca) for x, y in points]


def ring(cx, cy, rx, ry, n=18, start=0.0):
    return [(cx + math.cos(start + 2 * math.pi * i / n) * rx, cy + math.sin(start + 2 * math.pi * i / n) * ry) for i in range(n + 1)]


def along(points, x):
    """The y of a polyline (given left to right) at x."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return float(np.interp(x, xs, ys))


def wavy(points, amp, period, seed, step=3.0):
    """A line through the points with a gentle hand-made wave in it."""
    rng = np.random.default_rng(seed)
    pts = path(points, step)
    ph = rng.uniform(0, 6.28)
    out = []
    for i, (x, y) in enumerate(pts):
        out.append((x, y + amp * math.sin(ph + x / period * 6.283) + rng.normal(0, amp * 0.12)))
    return out


# ================================================================ the lie of the land


def fish(pen, x, y, size, facing, seed):
    """A fish of the river, side on, as the Egyptians drew them: an oval body, a long fin along the back, a tail."""
    s, f = size, facing
    body = [(x - f * s * 0.5, y), (x - f * s * 0.25, y - s * 0.24), (x + f * s * 0.15, y - s * 0.26), (x + f * s * 0.42, y - s * 0.08),
            (x + f * s * 0.5, y + s * 0.02), (x + f * s * 0.36, y + s * 0.16), (x - f * s * 0.05, y + s * 0.22), (x - f * s * 0.38, y + s * 0.10), (x - f * s * 0.5, y)]
    pen.wash(body, K.mix(("cerulean", 3), ("lilac", 2), ("lead-white", 3)), amount=0.42, rim=0.25, seed=seed, brush=3, soft=0.5)
    pen.stroke(body, 1.05, smooth_it=True, step=1.0, wobble=0.15, fade=0.1)
    pen.stroke([(x - f * s * 0.5, y), (x - f * s * 0.74, y - s * 0.20), (x - f * s * 0.70, y), (x - f * s * 0.75, y + s * 0.17), (x - f * s * 0.5, y)], 0.95, step=1.0, wobble=0.1)
    pen.stroke([(x - f * s * 0.30, y - s * 0.20), (x - f * s * 0.05, y - s * 0.38), (x + f * s * 0.25, y - s * 0.30), (x + f * s * 0.32, y - s * 0.14)], 0.8, smooth_it=True, step=1.0, wobble=0.1)
    pen.dot(x + f * s * 0.30, y - s * 0.04, 0.9)
    for k in range(3):                                     # the fin's rays
        u = -0.18 + k * 0.17
        pen.stroke([(x + f * s * u, y - s * 0.24), (x + f * s * (u + 0.05), y - s * 0.33)], 0.55, taper=(0, 0.5), wobble=0.05, dark=0.8)
    pen.stroke([(x + f * s * 0.05, y + s * 0.18), (x - f * s * 0.08, y + s * 0.30)], 0.7, wobble=0.05)


def lotus(pen, x, y, size, seed):
    """A lotus of the river floating open, side on: a fan of pointed petals on a short stem from the water."""
    rng = np.random.default_rng(seed)
    s = size
    pen.stroke([(x, y + s * 0.95), (x + rng.normal(0, 0.5), y + s * 0.5), (x, y + s * 0.18)], 0.8, smooth_it=True, step=1.0, wobble=0.08, dark=0.85)
    cup = [(x - s * 0.36, y + s * 0.05), (x, y + s * 0.24), (x + s * 0.36, y + s * 0.05), (x, y - s * 0.05)]
    pen.wash(cup, GREEN, amount=0.55, rim=0.3, seed=seed, brush=2, soft=0.3, body=0.5)
    petals = []
    for a, ln in ((-44, 0.86), (0, 1.0), (44, 0.86)):
        ca, sa = math.cos(math.radians(a - 90)), math.sin(math.radians(a - 90))
        tip = (x + ca * s * ln, y + sa * s * ln)
        side = (-sa * s * 0.24, ca * s * 0.24)
        petals.append([(x, y + s * 0.08), (x + ca * s * 0.45 * ln + side[0], y + sa * s * 0.45 * ln + side[1]), tip,
                       (x + ca * s * 0.45 * ln - side[0], y + sa * s * 0.45 * ln - side[1]), (x, y + s * 0.08)])
    for p in petals:
        pen.wash(p, LOTUS, amount=0.75, rim=0.3, seed=seed + int(p[2][0] * 10), brush=2, soft=0.25, body=0.75)
    for p in petals:
        pen.stroke(p, 0.62, step=0.7, wobble=0.05, fade=0.1, dark=0.8, smooth_it=True)
    pen.stroke([(x - s * 0.40, y + s * 0.02), (x, y + s * 0.24), (x + s * 0.40, y + s * 0.02)], 0.75, smooth_it=True, step=0.8, wobble=0.05, dark=0.85)


def small_pyramid(pen, cx, foot, h, seed):
    hw = h / K.SLOPE
    pen.stroke([(cx - hw - 1, foot), (cx, foot - h), (cx + hw + 1, foot)], 1.25, dark=0.8, wobble=0.25, taper=(0.3, 0.4))
    pen.stroke([(cx - hw - 3, foot + 0.5), (cx + hw + 3, foot)], 1.0, dark=0.7, wobble=0.25)
    for k in range(1, int(h / 3.2)):                                   # the face away from the river, in shade: hatched
        yy = foot - k * 3.2
        xa = cx + (foot - yy) / K.SLOPE * 0.05
        xb = cx + hw * (yy - (foot - h)) / h - 0.8
        if xb - xa > 1.5:
            pen.stroke([(xa + 0.8, yy + 1.2), (xb, yy - 0.2)], 0.55, dark=0.55, wobble=0.1, taper=(0.2, 0.4))


def back(seed=101):
    pen = Pen(seed)
    rng = np.random.default_rng(seed)

    # the river along the bottom: a thin wash, two lines, rows of zigzags, fish and lotus in it
    water = [(x, y + 1) for x, y in path(RIVER_TOP, 6)] + [(x, y - 1) for x, y in path(RIVER_BOTTOM, 6)][::-1]
    pen.wash(water, WATER, amount=0.42, rim=0.30, seed=seed + 1, brush=9, soft=1.2, body=0.35)
    for line, sd in ((RIVER_TOP, 2), (RIVER_BOTTOM, 3)):
        pts = wavy(line, 1.0, 140, seed + sd)
        n = len(pts)
        cuts = [0, int(n * 0.27), int(n * 0.55), int(n * 0.8), n - 1]
        for a, b in zip(cuts[:-1], cuts[1:]):
            pen.stroke(pts[max(0, a - 2):b + 1], 2.0, fade=0.25, wobble=0.25, taper=(0.3, 0.5))
    things_in_water = [("fish", 452.0, 529.0, 21.0, -1), ("fish", 640.0, 530.0, 19.0, 1), ("lotus", 372.0, 523.0, 9.5, 0),
                       ("lotus", 566.0, 522.0, 10.0, 0), ("lotus", 712.0, 524.0, 9.0, 0)]
    for row in range(3):                                   # three rows of zigzags, broken where something is in the water
        z = []
        x = 56.0 + row * 2.5
        up = 1
        while x < 746:
            y_row = along(RIVER_TOP, x) + 11.0 + row * 11.5
            z.append(None if _hits(things_in_water, x, y_row) else (x, y_row - up * 2.9 * rng.uniform(0.8, 1.15)))
            x += 4.6 * rng.uniform(0.85, 1.15)
            up = -up
        run = []
        for p in z + [None]:
            if p is None:
                if len(run) > 2:
                    for a in range(0, len(run) - 1, 26):                 # the pen is dipped every so often
                        pen.stroke(run[a:a + 27], 1.15, fade=0.3, wobble=0.12, taper=(0.2, 0.3), swell=0.12, step=1.2)
                run = []
            else:
                run.append(p)
    for kind, x, y, s, f in things_in_water:
        if kind == "fish":
            fish(pen, x, y, s, f, int(x))
        else:
            lotus(pen, x, y, s, int(x))

    # the edge of the desert: a low wavering rim in thin black, little hummocks along it, and the desert's sand as a
    # scatter of red dots above it
    rim = wavy(K.DESERT_EDGE, 1.2, 60, seed + 5, 4.0)
    for a in range(0, len(rim) - 1, 38):
        pen.stroke(rim[a:a + 40], 0.95, fade=0.35, wobble=0.25, dark=0.62, swell=0.35)
    P = np.array(rim)
    Ls = np.concatenate([[0], np.cumsum(np.hypot(*(P[1:] - P[:-1]).T))])
    s = 9.0
    while s < Ls[-1] - 9:
        x, y = float(np.interp(s, Ls, P[:, 0])), float(np.interp(s, Ls, P[:, 1]))
        w_ = rng.uniform(5.0, 8.0)
        pen.stroke([(x - w_ / 2, y - 0.3), (x, y - rng.uniform(2.2, 3.4)), (x + w_ / 2, y - 0.3)], 0.6, dark=0.5, smooth_it=True, step=0.8, wobble=0.05, taper=(0.4, 0.4))
        s += rng.uniform(16.0, 30.0)
    for _ in range(420):
        x = rng.uniform(52, 750)
        edge_y = along(K.DESERT_EDGE, x)
        depth = rng.exponential(16.0) if rng.random() < 0.7 else rng.uniform(0, 300)
        y = edge_y - 3 - depth
        if y < 150 or y > edge_y - 2:
            continue
        if left_x(y) - 6 < x < right_x(y) + 6 and y < BASE_Y + 6:          # not inside the Horizon, nor on its faces
            continue
        if y < 290 and rng.random() < 0.75:                                 # sparser far off
            continue
        pen.dot(x, y, rng.uniform(0.55, 0.95), ink="red", dark=rng.uniform(0.55, 0.9))

    # the far small pyramids
    for cx, foot, h in K.SMALL_PYRAMIDS:
        small_pyramid(pen, cx, foot, h, seed + int(cx))
    pen.stroke([(70, 263.0), (122, 262.5), (168, 263.2), (210, 262.4)], 0.9, ink="red", dark=0.6, wobble=0.3, fade=0.4)

    # the Horizon, seen from the river: its outline only, the inside blank
    pen.stroke([(APEX[0] + 0.8, APEX[1] - 1.5), (LEFT[0] - 0.5, LEFT[1] + 0.6)], 2.5, fade=0.28, wobble=0.45, taper=(0.25, 0.35), step=1.4)
    pen.stroke([(APEX[0] - 1.2, APEX[1] - 0.6), (RIGHT[0] + 1.0, RIGHT[1] + 0.4)], 2.5, fade=0.30, wobble=0.45, taper=(0.25, 0.35), step=1.4)
    pen.stroke([(LEFT[0] - 4.0, BASE_Y + 0.4), ((LEFT[0] + RIGHT[0]) / 2, BASE_Y + 1.2), (RIGHT[0] + 3.5, BASE_Y + 0.2)], 2.2, fade=0.3, wobble=0.4, taper=(0.3, 0.4))

    # a scribe's few strokes in the margin, trying his pen
    for x, y in ((62.0, 154.0), (67.0, 153.5), (72.0, 154.5)):
        pen.stroke([(x, y), (x + 0.6, y + 7.5)], 1.1, dark=0.75, wobble=0.1, taper=(0.2, 0.6))
    pen.stroke([(78.0, 158.0), (90.0, 157.0)], 1.0, ink="red", dark=0.8, wobble=0.1)
    return pen


def _hits(things, x, y_row):
    """Whether a row of water at (x, y_row) would run into a fish or a lotus: the zigzags stop short of them."""
    for kind, tx, ty, s, f in things:
        if kind == "fish":
            half, top, bot = s * 0.80, ty - s * 0.42, ty + s * 0.34
        else:
            half, top, bot = s * 0.62, ty - s * 1.05, ty + s * 0.95
        if tx - half - 2.5 <= x <= tx + half + 2.5 and top - 3.6 <= y_row <= bot + 3.6:
            return True
    return False


# ================================================================ the places


def palm(pen, x, foot, height, lean, seed, wash=True):
    """A date palm as an Egyptian draws one: a trunk of overlapping scales, a crown of fronds falling outward with
    their leaflets drawn as fine strokes underneath, and the dates hanging in red."""
    rng = np.random.default_rng(seed)
    top = (x + lean, foot - height)
    trunk = curve([(x, foot), (x + lean * 0.35 + rng.normal(0, 0.6), foot - height * 0.5), top], 10)
    # the fronds: a fan over the top, the outer ones falling away, two hanging down at the sides
    fronds = []
    for a in (-166, -144, -122, -101, -80, -58, -36, -14, 152, 28):
        a = math.radians(a + rng.normal(0, 4))
        ca, sa = math.cos(a), math.sin(a)
        ln = height * rng.uniform(0.27, 0.34) * (0.8 if sa > 0 else 1.0)
        flat = 1 - abs(sa) if sa < 0 else 0.3
        droop = ln * (0.10 + 0.55 * flat)
        p1 = (top[0] + ca * ln * 0.50, top[1] + sa * ln * 0.50 - ln * 0.06 * (1 - flat))
        tip = (top[0] + ca * ln, top[1] + sa * ln * 0.80 + droop)
        fronds.append((curve([top, p1, tip], 9), ln))
    if wash:
        for rib, ln in fronds:                                # green laid along each frond, as a brush follows it
            R = np.array(rib)
            tg = np.gradient(R, axis=0)
            tg /= np.maximum(np.hypot(tg[:, 0], tg[:, 1]), 1e-9)[:, None]
            nr = np.stack([-tg[:, 1], tg[:, 0]], 1)
            wdt = (ln * 0.17 * np.linspace(1.0, 0.35, len(R)))[:, None]
            poly = [tuple(p) for p in R + nr * wdt] + [tuple(p) for p in (R - nr * wdt)[::-1]]
            pen.wash(poly, GREEN, amount=0.42, rim=0.30, seed=seed + int(ln * 10), brush=3, soft=0.5, body=0.35)
    pen.stroke(trunk, 2.0, fade=0.15, wobble=0.25, taper=(0.0, 0.5), swell=0.1)
    for i in range(3, len(trunk) - 1, 1):                     # the scales: little v's up the trunk
        px, py = trunk[i]
        pen.stroke([(px - 2.3, py - 1.8), (px, py), (px + 2.3, py - 1.8)], 0.7, dark=0.85, wobble=0.05, taper=(0.3, 0.3))
    for rib, ln in fronds:
        pen.stroke(rib, 1.05, wobble=0.10, taper=(0.1, 0.8), fade=0.1)
        R = np.array(rib)
        for j in range(2, len(R) - 1):                       # the leaflets, both sides, swept toward the tip
            px, py = R[j]
            tx, ty = R[j + 1] - R[j - 1]
            nl = math.hypot(tx, ty) or 1.0
            tx, ty = tx / nl, ty / nl
            ll = ln * 0.19 * (1 - j / len(R) * 0.55)
            for side in (-1, 1):
                ex, ey = px + (tx * 0.55 - ty * side * 0.85) * ll, py + (ty * 0.55 + tx * side * 0.85) * ll
                pen.stroke([(px, py), (ex, ey + ll * 0.15)], 0.5, dark=0.72, wobble=0.03, taper=(0.1, 0.6))
    for dx in (-2.6, 2.4):                                    # the dates
        for k in range(4):
            pen.dot(top[0] + dx + rng.normal(0, 0.9), top[1] + 3.5 + k * 1.6 + rng.random(), 0.85, ink="red")


def reeds(pen, x0, x1, foot, seed, count=9, tall=(18, 32), wash=True):
    """Papyrus at the water's edge: upright stalks, each with its head, a few with a bud."""
    rng = np.random.default_rng(seed)
    xs = np.sort(rng.uniform(x0, x1, count))
    heads = []
    for i, x in enumerate(xs):
        hgt = rng.uniform(*tall)
        lean = rng.normal(0, 1.4)
        top = (x + lean, foot - hgt)
        heads.append(top)
        pen.stroke([(x, foot + 1), (x + lean * 0.4, foot - hgt * 0.5), top], 0.95, smooth_it=True, step=1.2, wobble=0.15, taper=(0, 0.3), dark=0.95)
        if rng.random() < 0.75:                              # an open head: a fan of rays
            if wash:
                pen.wash([(top[0], top[1] + 0.5), (top[0] - 4.2, top[1] - 4.6), (top[0] + 4.2, top[1] - 4.6)], GREEN, amount=0.45, rim=0.3, seed=seed + i, brush=2, soft=0.3, body=0.3)
            for a in (-55, -30, -10, 10, 30, 55):
                ca, sa = math.sin(math.radians(a)), -math.cos(math.radians(a))
                pen.stroke([top, (top[0] + ca * 5.0, top[1] + sa * 5.0)], 0.6, wobble=0.04, taper=(0.1, 0.4), dark=0.9)
            pen.stroke([(top[0] - 4.4, top[1] - 4.5), (top[0] + 4.4, top[1] - 4.6)], 0.55, wobble=0.1, dark=0.75, smooth_it=False)
        else:                                                # a bud
            pen.stroke([(top[0], top[1] + 1), (top[0] - 1.4, top[1] - 2.5), (top[0], top[1] - 4.2), (top[0] + 1.4, top[1] - 2.5), (top[0], top[1] + 1)], 0.7, step=0.7, wobble=0.04)
    return heads


def wagon(pen, nose, tilt, seed):
    """The family's wagon, as the scribe drew a thing he had no word for: a long red box with windows, all four
    wheels in a row underneath, the luggage tied on the roof. `nose` is the bottom of its front; it lies with its
    nose down at `tilt` degrees."""
    nx, ny = nose

    def T(pts):
        return rot([(nx + u, ny - v) for u, v in pts], tilt, (nx, ny))

    body = [(1.5, 0), (103, 0), (105, 4), (105, 20), (102, 31), (42, 31), (31, 17), (4, 15), (0.5, 11), (0, 4), (1.5, 0)]
    pen.wash(T(body), WAGON, amount=0.62, rim=0.30, seed=seed, brush=6, soft=0.6, body=0.45)
    panel = [(33, 4.5), (101, 4.5), (101, 12.5), (33, 12.5)]                   # the wooden side
    pen.wash(T(panel), K.mix(("yellow-ochre", 5), ("burnt-sienna", 1.5), ("naples-yellow", 2)), amount=0.55, rim=0.25, seed=seed + 1, brush=4, soft=0.4, body=0.5)
    pen.stroke(T(body), 1.45, step=1.2, wobble=0.25, fade=0.2, taper=(0.2, 0.2))
    pen.stroke(T([(33, 4.5), (101, 4.5)]), 0.8, wobble=0.15, dark=0.85)
    pen.stroke(T([(33, 12.5), (101, 12.5)]), 0.8, wobble=0.15, dark=0.85)
    for u in (48, 66, 84):
        pen.stroke(T([(u, 4.8), (u, 12.2)]), 0.6, wobble=0.05, dark=0.7)
    for u0, u1 in ((44, 57), (60, 74), (77, 90), (93, 100)):                     # the windows: neat, all alike
        win = [(u0, 18), (u1, 18), (u1, 27.5), (u0 + (1.5 if u0 == 44 else 0), 27.5), (u0, 18)]
        pen.wash(T(win), K.mix(("cerulean", 3), ("lead-white", 3), ("lilac", 1)), amount=0.40, rim=0.2, seed=seed + u0, brush=2, soft=0.3, body=0.5)
        pen.stroke(T(win), 0.8, step=1.0, wobble=0.08, dark=0.9)
    pen.stroke(T([(31.5, 17.2), (41, 18), (43, 27.5)]), 0.8, wobble=0.08)                 # the windscreen's edge
    pen.stroke(T([(4.5, 15.2), (31, 16.8)]), 0.7, wobble=0.1, dark=0.7)                   # the bonnet's line
    pen.dot(*T([(3.2, 9.0)])[0], 1.2)                                                     # a headlamp
    pen.stroke(T([(42, 31.5), (102, 31.5)]), 0.9, wobble=0.1)                             # the rack
    # the luggage, tied on
    loads = [((45, 31.5), (61, 40.5)), ((62, 31.5), (79, 42.5)), ((80, 31.5), (96, 39.0)), ((51, 40.5), (67, 46.5))]
    tints = [K.mix(("emerald-green", 2), ("yellow-ochre", 2), ("lead-white", 2)), K.mix(("burnt-sienna", 2), ("yellow-ochre", 3)),
             K.mix(("cobalt-blue", 2), ("lead-white", 3)), K.mix(("yellow-ochre", 3), ("lead-white", 1))]
    for ((a0, b0), (a1, b1)), tint in zip(loads, tints):
        box = [(a0, b0), (a1, b0), (a1, b1), (a0, b1), (a0, b0)]
        pen.wash(T(box), tint, amount=0.48, rim=0.25, seed=seed + int(a0), brush=3, soft=0.3, body=0.45)
        pen.stroke(T(box), 0.95, step=1.0, wobble=0.12)
    pen.stroke(T([(70, 37.5), (73, 37.5)]), 1.0, wobble=0.0)                             # a handle
    pen.stroke(T([(44, 31.5), (52, 46.8), (60, 33), (68, 46.8), (79, 34), (88, 39.5), (97, 32)]), 0.6, ink="red", wobble=0.15, dark=0.9)   # the rope
    # all four wheels, in a row
    for u in (12, 30, 72, 90):
        cx, cy = T([(u, 0.5)])[0]
        pen.wash(ring(cx, cy, 6.6, 6.6, 16), K.mix(("prussian-blue", 2), ("burnt-sienna", 1), ("lead-white", 2)), amount=0.55, rim=0.2, seed=seed + u, brush=2, soft=0.3, body=0.5)
        pen.stroke(ring(cx, cy, 6.6, 6.6, 18, 0.4), 1.25, step=0.9, wobble=0.12, fade=0.15)
        pen.stroke(ring(cx, cy, 2.2, 2.2, 10), 0.8, step=0.6, wobble=0.04)


def donkey(pen, x, foot, seed):
    """Lot's donkey, side on, its head down to the water: long ears, a cloth on its back."""
    back_ = [(x, foot - 18.5), (x + 6, foot - 20.5), (x + 15, foot - 20.0), (x + 19.5, foot - 19.0)]
    neck_top = [(x + 19.5, foot - 19.0), (x + 25, foot - 14.5), (x + 29.5, foot - 7.5)]
    head = [(x + 29.5, foot - 7.5), (x + 33.5, foot - 3.0), (x + 34.5, foot - 0.6), (x + 31.8, foot + 0.2), (x + 28.0, foot - 3.5), (x + 25.0, foot - 7.5), (x + 21.5, foot - 11.5), (x + 18.5, foot - 12.5)]
    belly = [(x + 18.5, foot - 12.5), (x + 12, foot - 11.0), (x + 4, foot - 11.5), (x + 0.5, foot - 13.0), (x, foot - 18.5)]
    outline = back_ + neck_top[1:] + head[1:] + belly[1:]
    pen.wash(outline, K.mix(("lilac", 2), ("lead-white", 2), ("yellow-ochre", 1)), amount=0.42, rim=0.25, seed=seed, brush=3, soft=0.4, body=0.4)
    pen.stroke(outline, 1.1, smooth_it=True, step=1.0, wobble=0.12, fade=0.15)
    for lx, ly in ((x + 2.0, foot - 12.5), (x + 5.0, foot - 11.6), (x + 14.0, foot - 11.2), (x + 17.0, foot - 12.2)):
        pen.stroke([(lx, ly), (lx + 0.3, foot - 5), (lx - 0.2, foot + 0.4)], 0.95, wobble=0.06, taper=(0, 0.2))
    pen.stroke([(x + 0.5, foot - 18.0), (x - 2.2, foot - 13.0), (x - 2.6, foot - 9.0)], 0.75, smooth_it=True, step=0.8, wobble=0.06)   # tail
    pen.stroke([(x + 22.5, foot - 15.5), (x + 21.0, foot - 22.0)], 0.9, wobble=0.04, taper=(0, 0.6))   # the long ears
    pen.stroke([(x + 24.0, foot - 15.0), (x + 23.8, foot - 21.5)], 0.9, wobble=0.04, taper=(0, 0.6))
    pen.dot(x + 30.3, foot - 4.6, 0.6)
    cloth = [(x + 5.5, foot - 20.3), (x + 14.5, foot - 20.1), (x + 13.5, foot - 13.0), (x + 6.0, foot - 13.2)]
    pen.wash(cloth, K.RED, amount=0.5, rim=0.3, seed=seed + 2, brush=2, soft=0.3, body=0.4)
    pen.stroke(cloth + [cloth[0]], 0.7, step=0.8, wobble=0.05, dark=0.9)
    for k in (8.5, 11.5):
        pen.stroke([(x + k, foot - 20.0), (x + k - 0.2, foot - 13.2)], 0.6, ink="red", wobble=0.04)


def river(seed=201):
    pen = Pen(seed)
    bank = lambda x: along(RIVER_TOP, x)
    palm(pen, 84.0, bank(84) + 1, 94.0, -2.0, seed + 1)
    palm(pen, 112.0, bank(112) + 1, 80.0, 3.5, seed + 2)
    reeds(pen, 58.0, 72.0, bank(64) + 1, seed + 6, count=6, tall=(15, 27))
    wagon(pen, (124.0, bank(124) - 1.5), -11.0, seed + 3)
    reeds(pen, 97.0, 131.0, bank(114) + 1, seed + 4, count=11, tall=(16, 31))
    donkey(pen, 236.0, bank(250) - 0.5, seed + 5)
    return pen


def stair_profile():
    """The stair up the face in section: from the ground in front of the face to a ledge at the entrance's sill."""
    x_foot, x_top = K.STAIR_FOOT, ENTRANCE[0] - 4.5
    y_foot, y_top = BASE_Y, ENTRANCE[1] + 0.5
    n = 8
    rise, run = (y_foot - y_top) / n, (x_top - x_foot) / n
    pts = [(x_foot, y_foot)]
    for k in range(n):
        x, y = pts[-1]
        pts.append((x, y - rise))
        pts.append((x + run, y - rise))
    pts.append((ENTRANCE[0] + 0.5, y_top))
    return pts


def site(seed=301):
    pen = Pen(seed)
    g = BASE_Y
    # the ground the works stand on
    pen.stroke([(244.0, g + 0.6), (298.0, g + 1.2), (348.0, g + 0.4), (LEFT[0] + 1.0, g + 0.5)], 1.3, fade=0.3, wobble=0.3)
    # water jars by the road from the river
    for jx, jh in ((250.0, 11.0), (259.5, 9.5)):
        jar = [(jx - 1.6, g - jh), (jx + 1.6, g - jh), (jx + 3.6, g - jh * 0.62), (jx + 2.6, g - 1.2), (jx, g), (jx - 2.6, g - 1.2), (jx - 3.6, g - jh * 0.62), (jx - 1.6, g - jh)]
        pen.wash(jar, K.mix(("burnt-sienna", 2), ("yellow-ochre", 2), ("lead-white", 1)), amount=0.5, rim=0.3, seed=int(jx), brush=2, soft=0.3, body=0.4)
        pen.stroke(jar, 0.9, smooth_it=True, step=0.8, wobble=0.08)
    # the stone yard: blocks waiting their turn
    for (a, b, c, d) in ((267.0, g - 12.5, 284.0, g), (285.0, g - 14.0, 301.0, g), (272.0, g - 25.5, 294.0, g - 12.5)):
        blk = [(a, b), (c, b), (c, d), (a, d), (a, b)]
        pen.wash(blk, K.mix(("naples-yellow", 3), ("lead-white", 2), ("lilac", 0.6)), amount=0.32, rim=0.2, seed=int(a), brush=3, soft=0.3, body=0.3)
        pen.stroke(blk, 1.05, step=1.0, wobble=0.15)
        pen.stroke([(c - 0.5, b + 2.5), (c - 0.5, d - 1.0)], 0.5, dark=0.5, wobble=0.04)
    # the scribe's awning: a cloth on four poles (two seen), his low table beneath it with his palette and roll
    pen.wash([(306.0, g - 33.0), (338.0, g - 34.5), (338.5, g - 30.0), (306.5, g - 29.0)], K.mix(("lead-white", 4), ("naples-yellow", 2)), amount=0.4, rim=0.3, seed=seed + 4, brush=3, soft=0.3, body=0.6)
    pen.stroke([(304.5, g - 33.0), (322.0, g - 31.5), (339.5, g - 34.5)], 1.1, smooth_it=True, step=1.0, wobble=0.12)
    pen.stroke([(305.5, g - 29.5), (322.0, g - 28.0), (339.0, g - 30.5)], 0.75, smooth_it=True, step=1.0, wobble=0.1)
    for px in (308.0, 336.0):
        pen.stroke([(px, g - 31.0), (px + 0.3, g)], 1.0, wobble=0.1, taper=(0.1, 0.2))
    for tx in np.linspace(307.0, 338.0, 6):                                        # its fringe
        pen.stroke([(tx, g - 29.0 + (tx - 307) * -0.03), (tx + 0.3, g - 26.5)], 0.55, ink="red", wobble=0.03)
    pen.stroke([(314.0, g - 6.5), (329.0, g - 6.5)], 1.0, wobble=0.08)              # the low table
    for lx in (315.5, 327.5):
        pen.stroke([(lx, g - 6.5), (lx, g)], 0.8, wobble=0.03)
    pen.stroke([(317.0, g - 7.0), (320.0, g - 9.0), (324.0, g - 9.0)], 0.6, dark=0.8, wobble=0.04)
    # the sledge, its block lashed on, its runners curled up at the front, the hauling rope put down
    blk = [(347.0, g - 22.5), (370.0, g - 22.5), (370.0, g - 6.0), (347.0, g - 6.0), (347.0, g - 22.5)]
    pen.wash(blk, K.mix(("naples-yellow", 3), ("lead-white", 3), ("lilac", 0.6)), amount=0.32, rim=0.2, seed=seed + 7, brush=3, soft=0.3, body=0.3)
    pen.stroke(blk, 1.15, step=1.0, wobble=0.15)
    pen.stroke([(344.0, g - 9.5), (341.0, g - 4.5), (344.5, g - 1.8), (373.0, g - 1.8)], 1.3, smooth_it=True, step=1.0, wobble=0.12)
    pen.stroke([(345.0, g - 5.8), (373.0, g - 5.8)], 1.0, wobble=0.1)
    for lx in (354.0, 364.0):                                                        # the lashings
        pen.stroke([(lx, g - 22.8), (lx + 0.5, g - 5.8)], 0.7, ink="red", wobble=0.05)
    pen.stroke([(341.5, g - 5.0), (332.0, g - 3.0), (326.0, g - 2.0)], 0.8, ink="red", smooth_it=True, step=1.0, wobble=0.1)
    # the stair up the face to the entrance, built against the face
    prof = stair_profile()
    pen.wash(prof + [(LEFT[0], BASE_Y), prof[0]], K.mix(("naples-yellow", 3), ("lead-white", 2), ("lilac", 0.5)), amount=0.28, rim=0.2, seed=seed + 8, brush=3, soft=0.3, body=0.3)
    pen.stroke(prof, 1.1, step=0.8, wobble=0.06, fade=0.2, taper=(0.1, 0.1))
    # the entrance: a dark doorway in the face with its pitched stones over it
    ex, ey = ENTRANCE
    dh = K.DOOR_H
    door = [(ex - 0.5, ey + 0.5), (left_x(ey - dh) + 0.2, ey - dh), (left_x(ey - dh) + 5.5, ey - dh + 2.0), (ex + 5.8, ey + 1.2)]
    pen.fill(door, dark=0.92)
    gx_, gy_ = left_x(ey - dh - 3.5), ey - dh - 3.5
    pen.stroke([(gx_ - 3.5, gy_ + 2.0), (gx_ + 1.0, gy_ - 3.2), (gx_ + 5.5, gy_ + 2.0)], 1.1, wobble=0.04, taper=(0.1, 0.1))
    pen.stroke([(gx_ - 1.8, gy_ + 2.2), (gx_ + 1.0, gy_ - 1.0), (gx_ + 3.8, gy_ + 2.2)], 0.7, wobble=0.04, dark=0.8)
    # the scaffold on the face above the entrance: two poles leaning on it, rungs, a brace
    u = np.array([APEX[0] - LEFT[0], APEX[1] - LEFT[1]], float)
    u /= np.hypot(*u)
    nrm = np.array([u[1], -u[0]])                                                   # out of the face

    def on_face(y, off):
        x = left_x(y)
        return (x + nrm[0] * off, y + nrm[1] * off)
    y_lo, y_hi = ey - 18.0, ey - 62.0
    for off in (3.0, 10.0):
        pen.stroke([on_face(y_lo, off), on_face(y_hi, off)], 0.95, wobble=0.12, taper=(0.1, 0.3))
    for k in range(6):
        y = y_lo - 3.0 - k * 7.6
        pen.stroke([on_face(y, 1.0), on_face(y + 0.5, 12.0)], 0.75, wobble=0.04, dark=0.9)
    pen.stroke([on_face(y_lo - 2, 10.0), on_face(y_hi + 6, 3.0)], 0.6, dark=0.8, wobble=0.04)
    return pen


def gallery_frame():
    """The great gallery in section: (floor, roof, bench) as lines from its foot to its top step, and its height."""
    fx, fy = GALLERY_FOOT
    tx, ty = GALLERY_TOP
    hgt = 26.0
    floor = [(fx, fy), (tx, ty)]
    roof = [(fx - 0.5, fy - hgt), (tx - 1.0, ty - hgt)]
    bench = [(fx + 3.0, fy - 5.0), (tx - 2.0, ty - 5.0)]
    return floor, roof, bench, hgt


def gallery(seed=401):
    pen = Pen(seed)
    floor, roof, bench, hgt = gallery_frame()
    (fx, fy), (tx, ty) = floor
    # the level floor at the foot, where the way in arrives, and the foot wall above the way in
    pen.stroke([(fx - 19.0, fy + 0.5), (fx, fy)], 1.25, wobble=0.1)
    pen.stroke([(fx - 0.5, fy - hgt - 1.0), (fx - 0.3, passage()[1][1][1])], 1.3, wobble=0.1)
    # the ramp's floor, and the high roof above it, its walls stepping in course over course (the laps)
    pen.stroke(floor, 1.6, fade=0.2, wobble=0.25, step=1.2)
    pen.stroke(roof, 1.5, fade=0.22, wobble=0.25, step=1.2)
    (rx0, ry0), (rx1, ry1) = roof
    for k in range(1, 8):
        t = k / 8.0
        x = rx0 + (rx1 - rx0) * t
        y = ry0 + (ry1 - ry0) * t
        for drop in (3.2, 6.4):
            pen.stroke([(x - 1.2 - drop * 0.25, y + drop), (x + 3.0 - drop * 0.25, y + drop - 3.0)], 0.5, dark=0.55, wobble=0.03, taper=(0.2, 0.2))
    pen.stroke(bench, 0.8, dark=0.75, wobble=0.15)
    # the top step, and the lintel of the doorway into the chamber
    pen.stroke([(tx, ty + 0.5), (tx, ty - 4.5), (tx + 5.0, ty - 4.5)], 1.25, wobble=0.06)
    pen.stroke([(rx1 - 0.5, ry1), (tx + 5.5, ry1 - 0.5)], 1.1, wobble=0.06)
    # the lamps up the ramp: small red dots, each in its dish on the bench
    for k in range(6):
        t = 0.10 + k * 0.16
        x = bench[0][0] + (bench[1][0] - bench[0][0]) * t
        y = bench[0][1] + (bench[1][1] - bench[0][1]) * t
        pen.stroke([(x - 1.6, y - 0.2), (x + 1.6, y - 0.2)], 0.6, dark=0.75, wobble=0.02)
        pen.dot(x, y - 2.1, 1.3, ink="red")
    return pen


def chamber(seed=501):
    pen = Pen(seed)
    x0, y0, x1, y1 = CHAMBER
    # the room: granite walls, the roof of great beams, the doorway low in its left wall
    door_top = y1 - 14.0
    pen.stroke([(x0, door_top), (x0, y0), (x1, y0), (x1, y1), (x0 + 0.5, y1)], 1.6, step=1.2, wobble=0.25, fade=0.25, taper=(0.15, 0.2))
    pen.stroke([(x0 + 1.0, y0 - 3.5), (x1 - 1.0, y0 - 3.5)], 0.9, wobble=0.15, dark=0.8)
    for bx in np.linspace(x0 + 14, x1 - 14, 6):                                     # the beams' ends
        pen.stroke([(bx, y0 - 3.4), (bx, y0)], 0.6, dark=0.7, wobble=0.02)
    pen.stroke([(x0 - 3.0, door_top), (x0 + 2.0, door_top)], 1.0, wobble=0.04)    # the doorway's lintel
    # the king's furniture, side on, standing on the floor, from the doorway in (the far wall left plain)
    gold = GOLD
    f = y1
    b0 = x0 + 50.0
    bed = [(b0, f - 8.0), (b0 + 18.0, f - 8.0), (b0 + 18.0, f - 6.0), (b0, f - 6.0)]       # a bed on lion's legs
    pen.wash(bed + [bed[0]], gold, amount=0.55, rim=0.25, seed=seed + 1, brush=2, soft=0.3, body=0.5)
    pen.stroke([(b0 - 1.5, f - 13.0), (b0, f - 8.0), (b0 + 18.5, f - 8.0), (b0 + 19.5, f - 10.5)], 1.0, wobble=0.08)
    pen.stroke([(b0, f - 6.0), (b0 + 18.0, f - 6.0)], 0.8, wobble=0.06)
    for lx in (b0 + 2.0, b0 + 16.5):
        pen.stroke([(lx, f - 6.0), (lx + 0.4, f - 2.0), (lx - 1.2, f - 0.4), (lx + 1.2, f - 0.4)], 0.85, wobble=0.04)
    h0 = b0 + 21.5                                                                      # two chests, one on the other
    for (a, b, c, d) in ((h0, f - 9.0, h0 + 10.5, f), (h0 + 1.5, f - 15.0, h0 + 9.0, f - 9.0)):
        box = [(a, b), (c, b), (c, d), (a, d), (a, b)]
        pen.wash(box, gold, amount=0.5, rim=0.25, seed=int(a + b), brush=2, soft=0.3, body=0.5)
        pen.stroke(box, 0.9, step=0.8, wobble=0.05)
        pen.stroke([(a + 1, b + 2), (c - 1, b + 2)], 0.5, dark=0.7, wobble=0.02)
    k0 = h0 + 13.5                                                                      # the stone coffin, plain
    cof = [(k0, f - 11.5), (k0 + 12.0, f - 11.5), (k0 + 12.0, f), (k0, f), (k0, f - 11.5)]
    pen.wash(cof, K.mix(("burnt-sienna", 1), ("lilac", 2), ("lead-white", 2)), amount=0.38, rim=0.25, seed=seed + 6, brush=2, soft=0.3, body=0.4)
    pen.stroke(cof, 1.05, step=0.8, wobble=0.06)
    pen.stroke([(k0 + 0.5, f - 9.5), (k0 + 11.5, f - 9.5)], 0.6, dark=0.75, wobble=0.04)
    return pen


# ================================================================ the ways


def footprint(pen, x, y, ang, side):
    """A small sneaker print: a rounded mark and a smaller one for the heel."""
    ca, sa = math.cos(ang), math.sin(ang)
    ox, oy = -sa * side * 2.0, ca * side * 2.0
    for (d, r1, r2) in ((1.2, 1.25, 0.85), (-1.6, 0.95, 0.8)):
        cx, cy = x + ox + ca * d, y + oy + sa * d
        pts = [(cx + ca * r1 * math.cos(t) - sa * r2 * math.sin(t), cy + sa * r1 * math.cos(t) + ca * r2 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 9)]
        pen.fill(pts, dark=0.9)


def track(seed=601):
    """river - site: the track up from the river, in red, a pair of lines as a road is drawn, with the boy's
    small prints going up between them."""
    pen = Pen(seed)
    route = curve(K.TRACK, 10)
    P = np.array(route)
    L = np.concatenate([[0], np.cumsum(np.hypot(*(P[1:] - P[:-1]).T))])
    tang = np.gradient(P, axis=0)
    tang /= np.hypot(tang[:, 0], tang[:, 1])[:, None]
    nrm = np.stack([-tang[:, 1], tang[:, 0]], 1)
    for side, sd in ((-1, 1), (1, 2)):
        edge = P + nrm * 4.2 * side
        keep = (L > 7) & (L < L[-1] - 6)
        e = [tuple(p) for p in edge[keep]]
        half = len(e) // 2
        pen.stroke(e[:half + 2], 1.15, ink="red", fade=0.25, wobble=0.35, taper=(0.4, 0.4))
        pen.stroke(e[half:], 1.15, ink="red", fade=0.25, wobble=0.35, taper=(0.4, 0.4))
    total = L[-1]
    s, side = 14.0, 1
    while s < total - 10:
        x = float(np.interp(s, L, P[:, 0]))
        y = float(np.interp(s, L, P[:, 1]))
        i = int(np.searchsorted(L, s))
        ang = math.atan2(tang[min(i, len(tang) - 1), 1], tang[min(i, len(tang) - 1), 0])
        footprint(pen, x, y, ang, side * 0.55)
        s += 9.5
        side = -side
    pen.stroke([(JOIN["river"][0] - 1.0, JOIN["river"][1] + 0.5), tuple(P[int(np.searchsorted(L, 9.0))])], 0.9, ink="red", wobble=0.1, dark=0.7)
    pen.stroke([tuple(P[int(np.searchsorted(L, L[-1] - 8.0))]), (JOIN["site"][0], JOIN["site"][1])], 0.9, ink="red", wobble=0.1, dark=0.7)
    return pen, [tuple(map(float, p)) for p in route]


def dotted(pen, pts, every=4.2, r=0.95, ink="red", start=0.0):
    P = np.array(path(pts, 0.5))
    L = np.concatenate([[0], np.cumsum(np.hypot(*(P[1:] - P[:-1]).T))])
    s = start
    while s <= L[-1] + 0.01:
        pen.dot(float(np.interp(s, L, P[:, 0])), float(np.interp(s, L, P[:, 1])), r, ink=ink, dark=0.95)
        s += every


def passage():
    """The low passage in, from the doorway in the face down to the foot of the gallery: (floor, roof)."""
    ex, ey = ENTRANCE
    dh, fall = K.DOOR_H, K.PASSAGE_FALL
    f0 = (ex + 5.8, ey + 1.2)
    r0 = (left_x(ey - dh) + 5.5, ey - dh + 2.0)
    x_floor, x_roof = GALLERY_FOOT[0] - 19.0, GALLERY_FOOT[0] - 0.3
    floor = [f0, (x_floor, f0[1] + fall * (x_floor - f0[0]))]
    roof = [r0, (x_roof, r0[1] + fall * (x_roof - r0[0]))]
    return floor, roof


def way_in(seed=701):
    """site - gallery: up the stair in front of the face, in at the entrance, and along the low passage to the
    foot of the gallery: a red dotted way, the passage drawn as a pair of thin red lines through the stone."""
    pen = Pen(seed)
    sx, sy = JOIN["site"]
    prof = stair_profile()
    foot0 = (prof[0][0] - 4.0, prof[0][1] - 3.6)          # just above the treads: the line a foot follows up the stair
    top = (prof[-2][0] + 0.5, prof[-2][1] - 3.6)
    ex, ey = ENTRANCE
    gx, gy = JOIN["gallery"]
    (f0, f1), (r0, r1) = passage()
    mid = lambda x: (f0[1] + K.PASSAGE_FALL * (x - f0[0])) - K.DOOR_H * 0.45
    inside = (ex + 7.0, mid(ex + 7.0))
    route = [(sx, sy), (foot0[0] - 3.0, foot0[1] + 7.0), foot0, top, inside, (gx - 8.0, mid(gx - 8.0)), (gx, gy)]
    dotted(pen, route[:4], every=4.3, r=0.95)
    dotted(pen, route[3:], every=4.0, r=0.95, start=2.0)
    pen.stroke([f0, f1], 0.85, ink="red", wobble=0.06, dark=0.9)
    pen.stroke([r0, r1], 0.85, ink="red", wobble=0.06, dark=0.9)
    return pen, [tuple(map(float, p)) for p in route]


def ramp(seed=801):
    """gallery - chamber: the ramp up the gallery to the doorway at the top: a red dotted way up its middle,
    over the top step and in at the door."""
    pen = Pen(seed)
    floor, roof, bench, hgt = gallery_frame()
    (fx, fy), (tx, ty) = floor
    gx, gy = JOIN["gallery"]
    cx, cy = JOIN["chamber"]
    up = 11.0
    route = [(gx, gy), (fx + 1.0, fy - up + 1.5), (tx - 3.0, ty - up), (tx + 3.0, ty - up - 1.5), (cx, cy)]
    dotted(pen, route, every=4.2, r=1.0)
    return pen, [tuple(map(float, p)) for p in route]


PLACES = {"river": river, "site": site, "gallery": gallery, "chamber": chamber}
WAYS = {("river", "site"): track, ("site", "gallery"): way_in, ("gallery", "chamber"): ramp}

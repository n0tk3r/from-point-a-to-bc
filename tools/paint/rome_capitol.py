"""Rome, the Ides of March, 44 B.C.: the top of the Capitol, the walled precinct before the temple of Jupiter Best and
Greatest, on the same fine morning as the steps of Saturn's temple below (rome_steps.py) and the street (rome_street.py).

PLAN
  Light     The sun low in the east-south-east, on our right and a little behind us (rome_capitol_kit.SUN, about 33
            degrees up). Everything facing right is warm and bright, fronts are lit at a slant, left sides are cool
            blue-violet shade; shadows on the paving run to the LEFT and a little away, 1.45 times as long as a thing
            is tall. The temple's front and the right side of every column are lit; its porch is deep in shade.
  Depth     horizon 275, full 590 (the master brief's, fixed). The lens is 3.45 m above the paving and looks level, so
            a temple this tall must stand far off for its pediment and the chariot on its peak to be in the picture:
            its steps begin some 55 m away (rows 320 to 325), and the precinct before it is deep.
  Tones     LIGHT  the temple's lit front, the sunlit paving, the cloud.
            DARK   the porch behind the columns, the bronze kings against the pale city, the hut's thatch.
            MIDDLE the sky, the city in its haze, the shade of the left flank and of the near paving.
            The eye goes from the boy's base in the row of kings to the altar's smoke and up the steps to the temple.
  Places    the temple: x 425 to 790, its steps' foot at rows 320 to 325, the chariot on its peak at row 10.
            the kings: a row across the middle (x 218 to 454), the broad low base in the middle (x 300 to 371, rows
            387 to 447) is the keeper's boy's seat; the geese stand round its foot.
            the view: over the parapet at the left (x 0 to 210): the Janiculum, Pompey's theater, the river and the
            island, the city below.  the hut: at the left edge.  the pen: in front of the parapet, left of the kings.
            the statue on the world: x 500.  the altar: centred under the pediment (x 545 to 681).  the chariot: to the
            altar's right.  the tablets: bottom right, running away from us.

The picture is a backdrop and cut-outs (people pass behind each): the altar, the statue on the world, the chariot,
the hut, the pen's fence (its near side and its gate side), the parapet, the row of tablets.

Not painted, on purpose: the portico of the precinct (wherever it stood on the left it would hide the view, or stand
as a blank wall behind the kings: the precinct's west side is its parapet here); Juno Moneta's temple on the other
summit (it would be behind the temple's right side, which runs out of the picture); the temple of Jupiter the
Thunderer, the Capitol as Michelangelo made it, columns of Athenian marble (all later or unlikely). The dictator
himself is nowhere: only his statues, which the Senate voted (no likeness of anyone). The gate of the precinct is
behind us at the bottom: we see only the long shadow of its right-hand pier on the near paving. The geese are the game's
(rome_capitol_geese.py paints their frames); so are the altar's smoke and embers, the kites, the city's smoke and the
light on the river (layout.json "fx").

  python3 rome_capitol.py         paints everything into out/rome-capitol/ and lays it together as out/rome-capitol-comp.png
  python3 rome_capitol.py fast    skips the brush pass and the palette: out/rome-capitol-2-all.png only
  (rome_capitol_kit.py holds the measurements, rome_capitol_temple.py the temple, rome_capitol_things.py the rest;
  rome_capitol_check.py draws layout.json over the picture.)"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
import land
import sky
from rome_capitol_kit import *
from rome_steps_kit import Canvas, Frame, col, courses, hash2, holes, mix, source_key, sunless, tex
import rome_capitol_temple as RT
import rome_capitol_things as TH

KEEP = "out/rome-capitol-kept"


def kept(name, make, *sources):
    """Paint a layer, or fetch it from the last run if nothing that paints it has changed."""
    os.makedirs(KEEP, exist_ok=True)
    key = source_key("rome_capitol_kit.py", *sources)
    path = f"{KEEP}/{name}-{key}.npz"
    if os.path.exists(path):
        z = np.load(path)
        return [z[k] for k in sorted(z.files, key=lambda s: int(s[1:]))]
    out = make()
    for f in os.listdir(KEEP):
        if f.startswith(name + "-"):
            os.remove(f"{KEEP}/{f}")
    np.savez_compressed(path, **{f"a{i}": o for i, o in enumerate(out)})
    return out


def hand(a, amount=1.0):
    """A hand does not rule its lines: push a picture or mask about a little (always the same push)."""
    return warp(warp(a, 0.6 * amount, 26, 5), 0.9 * amount, (150, 70), 6)


def handed(layer, amount=1.0):
    out = Canvas(layer.shape)
    both = hand(np.dstack([layer.c, layer.a]), amount)
    out.c, out.a = both[..., :3].astype(F32), np.clip(both[..., 3], 0, 1).astype(F32)
    return out


def layer_of(name, make, *sources):
    def mk():
        c = make()
        return [c.c, c.a]
    cc, ca = kept(name, mk, *sources)
    out = Canvas(SHAPE)
    out.c, out.a = cc, ca
    return out


# ---------------------------------------------------------------- far away: the haze of the morning
HAZE_COOL, HAZE_WARM = "#cddbe8", "#f2e6cc"


def far(color, d, most=1.0):
    """A colour as it looks through the morning air at d cm: paler, and bluer unless it is warm and sunlit."""
    t = float(np.clip(d / 260000.0, 0, 1)) ** 0.55 * 0.62 * most
    c = col(color)
    warm = float(np.clip((c[0] - c[2]) * 4, 0, 1))
    return mix(color, mix(HAZE_COOL, HAZE_WARM, warm), t * (1 - 0.3 * warm))


def sky_layer(seed=11):
    def make():
        pic = sky.field(SHAPE, HZ, [(0.0, "#2c6ec2"), (0.32, "#4790d8"), (0.60, "#7ebbe6"), (0.84, "#c4dde4"), (1.0, "#f2e6c8")], seed, haze="#f6ead0", patch=0.03)
        sky.wisps(pic, HZ, seed + 3, "#fdf2dc", top=0.55, amount=0.45)
        sky.paint_clouds(pic, [(128, 182, 250, 96, 26), (290, 126, 110, 40, 9), (742, 52, 150, 38, 9)], seed + 22,
                         tones=("#80a0d6", "#b8cce8", "#fbf3df", "#fffdf2"), light=SKY_LIGHT, ragged=11)
        return [pic]
    return kept("sky", make, repr(seed))[0].copy()


# ---------------------------------------------------------------- the view west over the parapet
RIDGE = [(-10, 263), (22, 255), (52, 249), (88, 250), (120, 246), (160, 250), (205, 255), (250, 258), (300, 262), (360, 266), (420, 270)]
RIVER_FAR = [(-10, 300), (60, 299), (140, 300), (230, 302), (300, 301), (380, 300)]
RIVER_NEAR = [(236, 302), (218, 310), (196, 321), (166, 331), (120, 337), (60, 341), (-10, 344)]


def river_widths(pts):
    """How wide the near reach is along its course (px): it widens where the island lies in it."""
    return [float(np.interp(p[0], [-10, 90, 120, 160, 200, 220, 236], [12, 13, 20, 22, 18, 9, 6])) for p in pts]


ISLAND = [(108, 339), (126, 334), (152, 330), (176, 327), (196, 323), (210, 319), (214, 321), (206, 328), (186, 333), (160, 337), (132, 341), (112, 342)]


def city(seed=31):
    """The view: the long ridge of the Janiculum with its pines across the river; the low roofs and gardens on the far
    bank; the Tiber's bend in a band of blue-green with the island and its temple and its two bridges; the plain beside
    the river with Pompey's great curved theater, the temple at the top of its seats and the long colonnades beside it;
    and below us the roofs of the city by the river. Painted crisply on a clear sheet: -> (colour, coverage)."""
    rng = np.random.default_rng(seed)
    s = Sheet(SHAPE, ss=3)
    ridge = curve(RIDGE, 6)
    # the Janiculum: green and hazy, darker where the woods are
    s.poly(ridge + [(420, 304), (-10, 304)], far("#7a9262", 180000))
    for i in range(140):                                     # woods and gardens on its face
        px = rng.uniform(-10, 420)
        top = np.interp(px, [q[0] for q in ridge], [q[1] for q in ridge])
        py = rng.uniform(top + 2, 300)
        r = rng.uniform(2.0, 5.5)
        tone = far(mix("#4f6a40", "#9aae6a", rng.random() ** 1.4), 170000)
        s.ellipse(px, py, r * 1.6, r * 0.7, tone, 0.8)
    for i in range(26):                                      # villas and farms: a pale wall, a red roof
        px = rng.uniform(0, 400)
        top = np.interp(px, [q[0] for q in ridge], [q[1] for q in ridge])
        py = rng.uniform(top + 8, 296)
        w, h = rng.uniform(3, 7), rng.uniform(2, 3.5)
        s.poly([(px, py), (px + w, py), (px + w, py - h), (px, py - h)], far(mix("#f6e6c4", "#e8cfa0", rng.random()), 160000))
        s.poly([(px - 0.6, py - h), (px + w + 0.6, py - h), (px + w * 0.5, py - h - 1.6)], far("#c8704a", 160000))

    def pine(px, py, hgt, d):
        s.line([(px, py), (px + hgt * 0.05, py - hgt * 0.6), (px - hgt * 0.02, py - hgt)], far("#5a4a40", d, 0.9), max(0.7, hgt * 0.05))
        for (dx, dy, rx, ry, tone) in ((-0.22, -1.02, 0.36, 0.14, "#3f5a3a"), (0.20, -1.05, 0.36, 0.15, "#4a6a40"), (0.0, -1.12, 0.30, 0.12, "#5d7e48")):
            s.ellipse(px + dx * hgt, py + dy * hgt, rx * hgt, ry * hgt, far(tone, d, 0.9))

    for i in range(22):                                      # umbrella pines along the skyline
        px = rng.uniform(-5, 410)
        top = np.interp(px, [q[0] for q in ridge], [q[1] for q in ridge])
        pine(px, top + rng.uniform(1, 4), rng.uniform(7, 12), 175000)
    for i in range(10):                                      # and cypresses
        px = rng.uniform(0, 400)
        top = np.interp(px, [q[0] for q in ridge], [q[1] for q in ridge])
        py, hgt = top + rng.uniform(4, 16), rng.uniform(8, 13)
        s.poly([(px - hgt * 0.1, py), (px, py - hgt), (px + hgt * 0.1, py)], far("#3a5238", 170000))
    # the far bank: low roofs and gardens down to the water
    for i in range(170):
        px = rng.uniform(-10, 420)
        py = rng.uniform(288, 300)
        w, h = rng.uniform(2, 6), rng.uniform(1.2, 2.6)
        if rng.random() < 0.3:
            s.ellipse(px, py, w * 0.7, h * 0.7, far(mix("#5f7a48", "#8aa060", rng.random()), 140000))
        else:
            s.poly([(px, py), (px + w, py), (px + w, py - h), (px, py - h)], far(mix("#e9d4ac", "#c87a50", rng.random() ** 2), 140000))
    # the river: the far reach, the bend, the near reach
    far_band = curve(RIVER_FAR, 6)
    s.poly([(p[0], p[1] - 2.6) for p in far_band] + [(p[0], p[1] + 2.4) for p in reversed(far_band)], far("#7fb6ac", 120000))
    near = curve(RIVER_NEAR, 6)
    widths = river_widths(near)
    up = [(p[0], p[1] - w * 0.55) for p, w in zip(near, widths)]
    dn = [(p[0], p[1] + w * 0.55) for p, w in zip(near, widths)]
    s.poly(up + list(reversed(dn)), far("#79b0a8", 70000))
    s.line(up, far("#c8e4d8", 70000), 0.9, 0.7)                                             # light along the far edge
    # the plain inside the bend (the Campus): fields, gardens, roofs, temples and colonnades
    plain = [(-10, 303)] + [(p[0], p[1] - 4) for p in near] + [(236, 300), (420, 302), (420, 304), (-10, 304)]
    for i in range(240):
        px = rng.uniform(-10, 236)
        lo = np.interp(px, [q[0] for q in reversed(near)], [q[1] for q in reversed(near)]) - 5
        py = rng.uniform(303, max(304, lo))
        d = 90000 - (py - 303) * 900
        w, h = rng.uniform(2, 6), rng.uniform(1.4, 3.4)
        r_ = rng.random()
        if r_ < 0.25:
            s.ellipse(px, py, w * 0.6, h * 0.6, far(mix("#5a7a44", "#90a868", rng.random()), d))
        elif r_ < 0.32:                                      # a small temple: pale front, a pediment
            s.poly([(px, py), (px + w, py), (px + w, py - h * 1.5), (px, py - h * 1.5)], far("#f4ead4", d))
            s.poly([(px - 0.5, py - h * 1.5), (px + w + 0.5, py - h * 1.5), (px + w / 2, py - h * 2.1)], far("#e8d8b8", d))
        else:
            s.poly([(px, py), (px + w, py), (px + w, py - h), (px, py - h)], far(mix("#efdcb6", "#d08a5c", rng.random() ** 2), d))
            s.line([(px, py - h), (px + w, py - h)], far("#b86a44", d), 0.8, 0.8)
    # the Circus of Flaminius: a long low enclosure on the plain near the bend
    cf = [(128, 318), (200, 313), (203, 316), (131, 321)]
    s.poly(cf, far("#d8c49a", 75000))
    s.line([(128, 318), (200, 313)], far("#f6ecd2", 75000), 0.9)
    # Pompey's theater: the great curved wall of its seats, three storeys of arches, the temple at the top of the seats,
    # the stage building, and the long colonnades running out from it toward us
    tx, ty, tw = 66.0, 312.0, 64.0                           # the middle of its foot, half its width (px)
    d = 85000
    rows_ = 28.0
    arc = [(tx + tw * math.cos(a), ty - rows_ - 6 * math.sin(a)) for a in np.linspace(math.pi, 0, 30)]
    s.poly([(tx - tw, ty)] + arc + [(tx + tw, ty)], far("#e8d6b0", d))                       # the curved outer wall, lit
    s.poly([(tx - tw, ty)] + arc[:8] + [(tx - tw * 0.72, ty)], far("#b9a69a", d))           # its left end turning into shade
    for st in range(3):                                      # three storeys of arches
        yy = ty - 4 - st * 8.5
        for j in range(16):
            a = math.pi * (j + 0.5) / 16
            ax = tx - tw * math.cos(a) * (0.98 - st * 0.01)
            s.poly([(ax - 1.1, yy), (ax + 1.1, yy), (ax + 1.1, yy - 5), (ax, yy - 6), (ax - 1.1, yy - 5)], far("#8f7e78", d), 0.85)
        s.line([(tx - tw, yy + 1.5), (tx + tw, yy + 1.5)], far("#fff2d8", d), 0.8, 0.7)
    tp = (tx + 2, ty - rows_ - 6)                            # the temple at the very top of the seats
    s.poly([(tp[0] - 7, tp[1]), (tp[0] + 7, tp[1]), (tp[0] + 7, tp[1] - 8), (tp[0] - 7, tp[1] - 8)], far("#f8eed8", d))
    s.poly([(tp[0] - 8.5, tp[1] - 8), (tp[0] + 8.5, tp[1] - 8), (tp[0], tp[1] - 12)], far("#e2d2b2", d))
    for j in range(4):
        s.line([(tp[0] - 5 + j * 3.4, tp[1]), (tp[0] - 5 + j * 3.4, tp[1] - 8)], far("#a89a96", d), 0.7, 0.8)
    s.poly([(tx - tw * 0.70, ty + 1), (tx + tw * 0.75, ty + 1), (tx + tw * 0.75, ty - 13), (tx - tw * 0.70, ty - 13)], far("#d9c6a0", d))     # the stage building
    s.line([(tx - tw * 0.70, ty - 13), (tx + tw * 0.75, ty - 13)], far("#fff4dc", d), 0.9)
    for j in range(18):
        ax = tx - tw * 0.66 + j * tw * 1.38 / 17
        s.line([(ax, ty), (ax, ty - 11)], far("#9a8a84", d), 0.7, 0.7)
    for (y0, x0, x1) in ((ty + 3, tx + tw * 0.70, tx + tw * 1.9), (ty + 8, tx + tw * 0.4, tx + tw * 1.7)):   # the colonnades of the portico, toward us
        s.poly([(x0, y0), (x1, y0 + 2), (x1, y0 - 4), (x0, y0 - 6)], far("#e4d2ac", 78000))
        for j in range(int((x1 - x0) / 2.4)):
            ax = x0 + j * 2.4
            s.line([(ax, y0 + j * 0.02), (ax, y0 - 5 + j * 0.02)], far("#9a8a84", 78000), 0.6, 0.7)
    # the island in the river: long, its banks built up, the temple of healing with its colonnade, a few houses and
    # trees, and its two stone bridges, one to each bank
    s.poly(ISLAND, far("#cdb894", 60000))
    s.line(ISLAND[:7], far("#efe2c4", 60000), 0.9, 0.9)                                   # its bank in the sun
    s.poly([(150, 331), (172, 328), (172, 320), (150, 323)], far("#f6ecd6", 60000))        # the temple of Aesculapius
    s.poly([(148, 323), (174, 320), (161, 316)], far("#e2d0ae", 60000))
    for j in range(5):
        s.line([(152 + j * 4.5, 330.5 - j * 0.6), (152 + j * 4.5, 323 - j * 0.6)], far("#a89aa0", 60000), 0.7, 0.8)
    for (px, py, w, h) in ((182, 327, 7, 5), (192, 324, 6, 4), (130, 335, 8, 4), (138, 333, 6, 4)):
        s.poly([(px, py), (px + w, py - 1), (px + w, py - 1 - h), (px, py - h)], far("#efdcb6", 60000))
        s.poly([(px - 0.5, py - h), (px + w + 0.5, py - 1 - h), (px + w + 0.3, py - 2.5 - h), (px - 0.3, py - 1.5 - h)], far("#c8704a", 60000))
    for (px, py, r) in ((120, 336, 3.4), (142, 333, 3.0), (178, 329, 3.0), (204, 322, 2.6)):
        s.ellipse(px, py, r * 1.3, r, far("#4f6a40", 60000))
    s.poly([(190, 326), (204, 322), (212, 311), (217, 312), (209, 324), (193, 330)], far("#e6d6b4", 66000))    # the bridge to the far bank
    s.poly([(150, 336), (157, 336), (150, 348), (142, 348)], far("#e6d6b4", 52000))                          # the new stone bridge to the near bank
    for (bx, by) in ((206, 316), (211, 314), (148, 343), (151, 340)):
        s.ellipse(bx, by + 1, 1.3, 1.0, far("#6a7a84", 60000))                              # its arches, the water under them
    # below us: the roofs of the city by the river (the plain lies some 35 m below the precinct), built through the
    # camera as blocks: walls lit where they face the sun, red-tiled roofs we look down on, temples among them
    city_roofs(s, rng, near)
    cliff = [(-10, 404), (40, 398), (90, 402), (140, 396), (190, 400), (230, 398), (230, 440), (-10, 440)]       # the edge of the hill, below the parapet
    s.poly(cliff, "#9a8a6a")
    for i in range(60):
        px, py = rng.uniform(-10, 230), rng.uniform(398, 440)
        s.ellipse(px, py, rng.uniform(3, 8), rng.uniform(2, 5), ["#5a6a3a", "#7a8a4a", "#a89870", "#8a7a5a"][int(rng.integers(4))], 0.9)
    # tiny people far below, a dab each, on the bridges and by the river
    for (px, py) in ((122, 346), (126, 346.5), (208, 333), (90, 360), (96, 361), (150, 357), (60, 366)):
        s.line([(px, py), (px, py - 1.6)], far(["#f4ead8", "#c8553a", "#7d94b8"][int(rng.integers(3))], 40000), 0.8)
    return s.done()


PLAIN = -3500.0                                              # the plain by the river, below the precinct (cm)


def city_roofs(s, rng, near):
    """Houses, blocks of flats and temples on the plain below, far ones first, kept off the river."""
    river_x = [q[0] for q in reversed(near)]
    river_y = [q[1] for q in reversed(near)]
    houses = []
    for i in range(520):
        Z = rng.uniform(24000.0, 46000.0)
        X = rng.uniform(-0.62, -0.02) * Z
        w, d, h = rng.uniform(900, 2000), rng.uniform(800, 1600), rng.uniform(500, 1200)
        houses.append((Z, X, w, d, h))
    for (Z, X, w, d, h) in sorted(houses, key=lambda t: -t[0]):
        foot = P(X + w / 2, PLAIN, Z)
        if foot[0] > 236 or foot[0] < -40:
            continue
        lim = np.interp(foot[0], river_x, river_y) + 6
        top = P(X + w / 2, PLAIN + h + min(w, d) * 0.22, Z)[1]
        if foot[1] < lim or top < lim:                       # (nothing in front of the river and the island)
            continue
        dd = Z
        y0, y1 = PLAIN, PLAIN + h
        roof = rng.random()
        wall = mix("#f4e4c2", "#e2be8c", rng.random())
        tile = mix("#c8643a", "#e09a62", rng.random())
        # the side toward the sun (it faces +X: we see it when the house stands left of us) and the front
        s.poly([P(X + w, y0, Z), P(X + w, y0, Z + d), P(X + w, y1, Z + d), P(X + w, y1, Z)], far(mix(wall, "#fff4dc", 0.25), dd))
        s.poly([P(X, y0, Z), P(X + w, y0, Z), P(X + w, y1, Z), P(X, y1, Z)], far(mix(wall, "#b8a6b8", 0.18), dd))
        for j in range(int(w / 400)):                        # windows, small and dark
            wx = X + 200 + j * 400
            a, b = P(wx, y0 + h * 0.55, Z - 1), P(wx + 80, y0 + h * 0.55 + 120, Z - 1)
            if b[0] - a[0] > 0.5:
                s.poly([(a[0], a[1]), (b[0], a[1]), (b[0], b[1]), (a[0], b[1])], far("#6a5a6a", dd), 0.8)
        ridge = y1 + min(w, d) * 0.22
        if roof < 0.6:                                       # a ridge running away from us: two slopes, the right one in the sun
            s.poly([P(X, y1, Z), P(X + w / 2, ridge, Z), P(X + w / 2, ridge, Z + d), P(X, y1, Z + d)], far(mix(tile, "#7a3c2c", 0.25), dd))
            s.poly([P(X + w / 2, ridge, Z), P(X + w, y1, Z), P(X + w, y1, Z + d), P(X + w / 2, ridge, Z + d)], far(mix(tile, "#ffd0a0", 0.15), dd))
        else:                                                # a ridge across: the front slope toward us
            s.poly([P(X, y1, Z), P(X + w, y1, Z), P(X + w, ridge, Z + d / 2), P(X, ridge, Z + d / 2)], far(tile, dd))
            s.poly([P(X + w, y1, Z), P(X + w, y1, Z + d), P(X + w, ridge, Z + d / 2)], far(mix(tile, "#ffd0a0", 0.2), dd))
        if rng.random() < 0.12:                              # a garden tree or a cypress beside it
            t = P(X - 300, PLAIN, Z + d * 0.5)
            r = 500 * FOC / Z
            s.ellipse(t[0], t[1] - r * 0.9, r * 0.9, r * 0.75, far(mix("#4f6a40", "#7a9454", rng.random()), dd))
    for (X, Z, w) in ((-9000.0, 33000.0, 1600.0), (-6500.0, 36000.0, 1500.0), (-4200.0, 39000.0, 1500.0)):    # three temples by the river market
        d, hc = 2600.0, 1100.0
        s.poly([P(X, PLAIN, Z), P(X + w, PLAIN, Z), P(X + w, PLAIN + hc, Z), P(X, PLAIN + hc, Z)], far("#a89aa8", Z))          # the porch in shade
        s.poly([P(X + w, PLAIN, Z), P(X + w, PLAIN, Z + d), P(X + w, PLAIN + hc, Z + d), P(X + w, PLAIN + hc, Z)], far("#efe0c2", Z))
        s.poly([P(X - 60, PLAIN + hc, Z), P(X + w + 60, PLAIN + hc, Z), P(X + w / 2, PLAIN + hc + 380, Z)], far("#ead8b8", Z))
        s.poly([P(X + w / 2, PLAIN + hc + 380, Z), P(X + w + 60, PLAIN + hc, Z), P(X + w + 60, PLAIN + hc, Z + d), P(X + w / 2, PLAIN + hc + 380, Z + d)], far("#d88a5a", Z))
        for j in range(6):
            cx = X + 120 + j * (w - 240) / 5
            s.line([P(cx, PLAIN, Z - 2), P(cx, PLAIN + hc, Z - 2)], far("#ece0c6", Z), max(0.7, 60 * FOC / Z), 0.9)


# ---------------------------------------------------------------- the paving
def ground(seed=17):
    """The paved precinct in its own colours, no light yet: -> (picture, joint mask, X, Z)."""
    x, y = grid(SHAPE)
    yy = np.maximum(y, HZ + 0.5)
    Z = EYE * FOC / (yy - HZ)
    X = (x - CAM.vx) * Z / FOC
    ppc = FOC / Z
    tone, jm, above = courses(X, Z, long=172.0, high=118.0, seed=seed, joint=1.8, ppc=ppc, vary_len=0.34)
    c = col("#e6dcc4")[None, None, :] * (1 + (tone[..., None] - 0.5) * 0.10)
    warm = (hash2(np.floor(tone * 811), 5, seed) - 0.5) * 0.06
    c = c + np.stack([warm, warm * 0.2, -warm * 1.2], axis=-1)
    old = (hash2(np.floor(tone * 577), 9, seed) > 0.9)
    c = c * np.where(old[..., None], np.array([0.91, 0.89, 0.90], dtype=F32), 1.0)
    c = c * (1 + (tex(X, Z, 520, seed + 1)[..., None] - 0.5) * 0.18 + (tex(X, Z, 70, seed + 2)[..., None] - 0.5) * 0.08)
    path = np.exp(-((X - 300 - (Z - 900) * 0.08) / 380.0) ** 2)            # worn pale where everyone walks from the gate to the temple
    c = c * (1 + 0.05 * path[..., None])
    return np.clip(c, 0, 1).astype(F32), jm, X, Z


def ground_shadow():
    """Where the sun does not reach the paving: the things in the precinct, and the temple."""
    def make():
        x, y = grid(SHAPE)
        yy = np.maximum(y, HZ + 0.5)
        Z = EYE * FOC / (yy - HZ)
        X = (x - CAM.vx) * Z / FOC
        a = sunless(TH.ground_solids(), X, Z, 0.0, TH.SUNW, spread=0.012)
        u, v, _ = T.on_floor(0.0)
        RT.SOL = RT.solids()
        b = sunless(RT.SOL, u, v, 0.0, (RT.SU, RT.SV, RT.SH), spread=0.012)
        return [np.maximum(a, b).astype(F32)]
    return kept("shadow", make, "rome_capitol_things.py", "rome_capitol_temple.py", repr((KINGS, WORLD, CHARIOT, ALTAR, HUT, PEN, WALL, TABLETS, tuple(SUN))))[0]


def precinct_mask():
    """Where the paving is: below the horizon, but not beyond the parapet at the left (the drop), nor west of the
    precinct's side behind the kings."""
    x, y = grid(SHAPE)
    wall_foot = P(0, 0, WALL["Z"] + WALL["t"])[1]
    Xe = TH.wall_end_X()
    xe = P(Xe, 0, WALL["Z"])[0]
    m = (y > HZ + 0.5).astype(F32)
    left = (x < xe) & (y < wall_foot)
    m[left] = 0
    # west of the precinct's side, behind the kings, there is no paving either (the hill drops away)
    Z = EYE * FOC / np.maximum(y - HZ, 0.5)
    X = (x - CAM.vx) * Z / FOC
    m[(X < -560.0) & (Z > WALL["Z"])] = 0
    return m


def under(seed=11):
    """Everything broad and soft: the sky, the view in its haze, the paving with its shadows."""
    x, y = grid(SHAPE)
    info = {}
    pic = sky_layer(seed)
    cc, ca = kept("city", lambda: list(city()), city, far, city_roofs, river_widths, repr((RIVER_NEAR, RIVER_FAR, RIDGE, ISLAND, PLAIN, HAZE_COOL, HAZE_WARM)))
    over(pic, blur(cc, 1.2), blur(ca, 0.8))
    own, jm, X, Z = ground()
    gmask = precinct_mask()
    near = np.clip((y - HZ) / (H - HZ), 0, 1) ** 1.2
    own = own * (1 - near[..., None] * (1 - np.array([1.0, 0.94, 0.80], dtype=F32)) * 0.8)
    cut = ground_shadow() * gmask
    lit = LIT.on(own, TH.SUNW[2], cut, up=1, deep=0.08 * cut, bounce=0.25)
    drift = (noise(SHAPE, 150, seed + 12, 3) - 0.5) * 0.10
    lit = np.clip(lit * (1 + (cut[..., None] * np.stack([drift, drift * 0.3, -drift], axis=-1))), 0, 1)
    over(pic, lit, gmask)
    land.haze(pic, HZ, "#f3ead2", 0.55, 0.12, gmask)
    glow(pic, "#fff0c8", (np.clip(1 - np.abs(y - (HZ + 8)) / 30, 0, 1) * 0.10).astype(F32))
    corner = np.clip(((x - 400) / 400) ** 2 * 0.40 + ((y - 470) / 130).clip(0, 2) ** 2 * 0.5, 0, 1)
    tint(pic, "#cba27a", (corner * 0.18 * gmask).astype(F32))
    info.update(X=X, Z=Z, joints=jm, ground=gmask, cut=cut, city=(cc, ca))
    return np.clip(pic, 0, 1), info


# ---------------------------------------------------------------- over the brushwork: the crisp things again, and the small ones
def details(pic, info, temple, kings, pen_back, seed=11):
    x, y = grid(SHAPE)
    rng = np.random.default_rng(seed + 5)
    cc, ca = info["city"]
    over(pic, cc, ca * 0.80)
    land.haze(pic, HZ, "#f3ead2", 0.18, 0.08, ca)
    # joints of the paving: thin, broken, fainter far off; the near edge of each slab catches the sun
    jm = hand(info["joints"]) * info["ground"] * (0.6 + 0.5 * noise(SHAPE, 110, seed + 21, 3))
    tint(pic, "#8a6f5c", np.clip(jm * 0.55, 0, 1).astype(F32))
    lip = np.roll(info["joints"], 1, axis=0) * info["ground"] * (1 - info["cut"]) * (1 - np.clip(info["joints"] * 2, 0, 1))
    glow(pic, "#fff2d0", np.clip(lip * 0.15, 0, 1).astype(F32))
    # the temple, the kings and the back of the pen, crisp again over the brushwork
    crisp = pic.copy()
    temple.onto(crisp)
    kings.onto(crisp)
    pen_back.onto(crisp)
    pic[...] = lerp(pic, crisp, 0.86)
    s = Sheet(SHAPE)

    def tuft(px, py, r, tones=("#55662e", "#7f9440", "#b4bf60")):
        for j in range(int(5 + r)):
            a = math.pi * rng.uniform(0.15, 0.85)
            l = r * rng.uniform(0.5, 1.1)
            s.line([(px + rng.normal(0, r * 0.25), py), (px + math.cos(a) * l * 0.8, py - math.sin(a) * l)], tones[int(rng.random() ** 1.4 * 3)], max(0.8, r * 0.14))
    # grass in the joints, more toward the edges of the precinct; cracks across a slab or two; grit
    for i in range(46):
        gx_, gy_ = rng.uniform(0, 800), rng.uniform(HZ + 60, 598)
        if info["ground"][int(gy_), int(gx_)] > 0.5:
            tuft(gx_, gy_, 1.0 + 4.0 * scale_at(gy_) * rng.uniform(0.6, 1.2))
    for (cx_, cy_, l_) in ((330, 575, 36), (560, 592, 26), (470, 520, 20), (720, 455, 22), (600, 430, 16), (120, 520, 26)):
        pts_ = [(cx_, cy_)]
        ang = rng.uniform(-0.5, 0.5)
        for j in range(5):
            ang += rng.normal(0, 0.5)
            pts_.append((pts_[-1][0] + math.cos(ang) * l_ / 5, pts_[-1][1] + math.sin(ang) * l_ / 9))
        s.line(pts_, "#8a6c50", 0.9, 0.6)
        s.line([(q[0], q[1] + 1) for q in pts_], "#fff0c8", 0.7, 0.3)
    for i in range(40):
        gx_, gy_ = rng.uniform(120, 800), rng.uniform(470, 598)
        r_ = 0.5 + 1.1 * scale_at(gy_) * rng.random()
        s.ellipse(gx_ - r_ * 1.2, gy_ + 0.3, r_ * 1.6, r_ * 0.5, "#8f7c98", 0.45)
        s.ellipse(gx_, gy_, r_ * 1.2, r_ * 0.8, ["#f4e2bc", "#cbb089", "#a48a70"][int(rng.integers(3))])
    # by the pen: grain spilled from the goose-keeper's basket, a feather or two, a wet patch by its gate
    X0, X1 = PEN["X"]
    Z0, Z1 = PEN["Z"]
    for i in range(60):
        Xp, Zp = rng.normal(X1 + 60, 70), rng.normal((Z0 + Z1) / 2 - 60, 60)
        p = P(Xp, 0, Zp)
        s.ellipse(p[0], p[1], 0.7, 0.5, ["#e8cc70", "#d4b058", "#f4dc8a"][int(rng.integers(3))], 0.9)
    for i in range(9):
        Xp, Zp = rng.normal(X1 + 120, 160), rng.normal(Z0 - 40, 90)
        p = P(Xp, 0, Zp)
        ang = rng.uniform(0, math.pi)
        ln = rng.uniform(4, 7) * k_at(Zp)
        s.line([p, (p[0] + math.cos(ang) * ln, p[1] - abs(math.sin(ang)) * ln * 0.4)], "#f8f4ec", max(1.0, 1.6 * k_at(Zp)))
    # by the altar: laurel leaves and petals blown about, a wine stain where the morning's libation was poured
    AX0, AX1 = ALTAR["X"]
    AZ0, AZ1 = ALTAR["Z"]
    spill = mask_poly(SHAPE, [P(AX0 + 40, 0, AZ0 - 60), P(AX0 + 200, 0, AZ0 - 70), P(AX0 + 260, 0, AZ0 - 30), P(AX0 + 80, 0, AZ0 - 32)], soft=1.5, wobble=3, seed=seed + 31)
    tint(pic, "#a8766e", (spill * (0.5 + 0.5 * noise(SHAPE, 12, seed + 32, 3)) * 0.40).astype(F32))
    for i in range(30):
        Xp, Zp = rng.normal((AX0 + AX1) / 2, 260), rng.normal(AZ0 - 120, 80)
        p = P(Xp, 0, Zp)
        tone = ["#f6ead8", "#e8a09a", "#7c9044", "#f0dcc0", "#c85a48", "#4f7a30"][int(rng.integers(6))]
        s.ellipse(p[0], p[1], rng.uniform(0.6, 1.2), rng.uniform(0.4, 0.7), tone, 0.85)
    # before old Brutus's base the paving is still wet where his base was scrubbed this morning; feathers by the boy's base
    bx0, bx1, bz0, bz1, bh_ = base_box(KINGS[1])
    wet = mask_poly(SHAPE, [P(bx0 - 30, 0, bz0 - 20), P(bx1 + 40, 0, bz0 - 24), P(bx1 + 70, 0, bz0 - 120), P(bx0 + 10, 0, bz0 - 150), P(bx0 - 50, 0, bz0 - 90)], soft=1.2, wobble=3, seed=seed + 41)
    wet = wet * (0.55 + 0.45 * noise(SHAPE, 9, seed + 42, 3))
    tint(pic, "#8a8a9c", (wet * 0.38).astype(F32))
    glow(pic, "#f4f0e0", (wet * step(0.78, 0.95, noise(SHAPE, 4, seed + 43, 2)) * 0.25).astype(F32))
    for i in range(12):
        sx0, sx1, sz0, sz1, sh_ = base_box(KINGS[2])
        Xp, Zp = rng.uniform(sx0 - 80, sx1 + 120), rng.uniform(sz0 - 280, sz0 - 20)
        p = P(Xp, 0, Zp)
        ang = rng.uniform(0, math.pi)
        ln = rng.uniform(4, 8) * k_at(Zp)
        s.line([p, (p[0] + math.cos(ang) * ln, p[1] - abs(math.sin(ang)) * ln * 0.35)], "#fbf8f0", max(1.0, 1.8 * k_at(Zp)))
        s.line([(p[0] + 0.5, p[1] + 0.6), (p[0] + math.cos(ang) * ln + 0.5, p[1] - abs(math.sin(ang)) * ln * 0.35 + 0.6)], "#b8b4c4", max(0.6, 0.7 * k_at(Zp)), 0.6)
    # weeds where the paving meets the kings' bases and the parapet
    for kg in KINGS:
        X0_, X1_, Z0_, Z1_, h_ = base_box(kg)
        for side in (X0_ - 4, X1_ + 4):
            if rng.random() < 0.6:
                p = P(side, 0, Z0_ - 6)
                tuft(p[0], p[1], 2.5 + 2 * rng.random(), tones=("#34452c", "#4a6238", "#6f8850"))
    s.onto(pic)
    # dark lines where things stand on the paving (under the cut-outs too: the backdrop is complete under each)
    s = Sheet(SHAPE)
    for kg in KINGS:
        X0_, X1_, Z0_, Z1_, h_ = base_box(kg)
        s.line([P(X0_ - 6, 0, Z0_ - 6), P(X1_ + 6, 0, Z0_ - 6)], "#6a5a50", 1.2, 0.55)
    s.onto(pic)
    return pic


def brushed(layer, ground_, seed, sizes=(6, 3, 2), keep=0.40, restate=0.62):
    """A cut-out, repainted with a small brush on the ground it stands against, then said again crisply.
    -> (colour, hard coverage)."""
    c, a = layer.straight()
    ys, xs = np.where(a > 0.02)
    if len(xs) == 0:
        return c, a
    x0, x1, y0, y1 = max(0, xs.min() - 12), min(W, xs.max() + 13), max(0, ys.min() - 12), min(H, ys.max() + 13)
    flat = ground_[y0:y1, x0:x1].copy()
    over(flat, c[y0:y1, x0:x1], a[y0:y1, x0:x1])
    painted = strokes(flat, sizes=sizes, seed=seed, density=1.8, jitter=0.03, keep=keep)
    painted = lerp(painted, flat, (restate * a[y0:y1, x0:x1])[..., None])
    out = c.copy()
    out[y0:y1, x0:x1] = painted
    return out, (a > 0.5).astype(F32)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02, palette=None):
    """Grain, then a limited palette with speckle, written as a PNG-8. -> (file size, palette)"""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette if palette is not None else palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name), pal


CUTS = ["altar", "chariot", "world", "parapet", "hut", "pen", "tablets"]     # back to front, as the scene lists them


def cut_layers():
    """Every cut-out, crisp, at picture size. -> {name: Canvas}"""
    pb = kept("pen", lambda: [q for cv in TH.pen_layers() for q in (cv.c, cv.a)], "rome_capitol_things.py")
    pen_front = Canvas(SHAPE)
    pen_front.c, pen_front.a = pb[2], pb[3]
    things = "rome_capitol_things.py"                        # (each kept layer is painted again when anything in that file changes)
    return {
        "altar": layer_of("altar", TH.altar_layer, things),
        "chariot": layer_of("chariot", TH.chariot_layer, things),
        "world": layer_of("world", TH.world_layer, things),
        "parapet": layer_of("parapet", TH.wall_layer, things),
        "hut": layer_of("hut", TH.hut_layer, things),
        "pen": pen_front,
        "tablets": layer_of("tablets", TH.tablets_layer, things),
    }


def temple_layer():
    return layer_of("temple", RT.temple, "rome_capitol_temple.py", "letter.py")


def kings_layer():
    return layer_of("kings", TH.kings_layer, "rome_capitol_things.py")


def pen_back_layer():
    pb = kept("pen", lambda: [q for cv in TH.pen_layers() for q in (cv.c, cv.a)], "rome_capitol_things.py")
    c = Canvas(SHAPE)
    c.c, c.a = pb[0], pb[1]
    return c


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(f"{OUT}-work", exist_ok=True)
    fast = len(sys.argv) > 1 and sys.argv[1] == "fast"
    temple_l = handed(temple_layer(), 0.5)
    kings_l = handed(kings_layer(), 0.4)
    pen_b = pen_back_layer()
    print("layers", round(time.time() - t0, 1))
    base, info = under()
    soft = Canvas(SHAPE)
    for L in (temple_l, kings_l, pen_b):
        soft.c, soft.a = blur(L.c, 1.6), blur(L.a, 1.1)
        soft.onto(base)
    Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8)).save(f"{OUT}-work/1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else strokes(base, sizes=(12, 6, 3), seed=2, density=1.5, jitter=0.03, keep=0.24)
    ground_ = pic.copy()
    details(pic, info, temple_l, kings_l, pen_b)
    print("details", round(time.time() - t0, 1))
    cuts = cut_layers()
    whole = pic.copy()
    cut = {}
    for i, name in enumerate(CUTS):
        layer = cuts[name]
        if fast:
            c, a = layer.straight()
            a = (a > 0.5).astype(F32)
        else:
            c, a = brushed(layer, ground_, seed=20 + i)
        cut[name] = (c, a)
        over(whole, c, a)
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(f"{OUT}-2-all.png")
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    size, pal = finish(pic, f"{OUT}/back.png", 160)
    print("back", size)
    for name, (c, a) in cut.items():
        print(name, finish(c, f"{OUT}/{name}.png", 64, a)[0])
    import rome_capitol_layout as LY
    LY.write(f"{OUT}/layout.json")
    import rome_capitol_geese as GE
    GE.paint_all(OUT, pal)
    comp = Image.open(f"{OUT}/back.png").convert("RGBA")
    for name in CUTS:
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(f"{OUT}-comp.png")
    print("done", round(time.time() - t0, 1))

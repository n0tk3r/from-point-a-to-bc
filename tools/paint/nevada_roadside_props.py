"""The things that stand at the Nevada roadside. Each is drawn in its own measurements, in centimetres
(x along it, y up, z back), on two drafts: `d` for the flat shapes that will be brushed, `dl` for the
crisp lines and small things that go on top afterwards. Lettering is asked for through `notes` and
put on by `letter_on` once the thing has been turned into a picture."""

import math

import numpy as np

from brush import *
from solid import mix
import letter
from nevada_roadside_kit import *

# the direction the sunlight comes FROM, as a unit vector (x right, y up, z away)
_n = math.sqrt(SUN[0] ** 2 + 1 + SUN[1] ** 2)
TO_SUN = (-SUN[0] / _n, 1 / _n, -SUN[1] / _n)


def facing(nx, ny, nz):
    """How squarely a surface with this normal faces the sun: 0 (edge-on or turned away) to 1."""
    l = math.sqrt(nx * nx + ny * ny + nz * nz) + 1e-9
    return max(0.0, (nx * TO_SUN[0] + ny * TO_SUN[1] + nz * TO_SUN[2]) / l)


def lit(shade, light, f):
    """Between a thing's shade color and its sunlit color."""
    return mix(shade, light, min(1.0, max(0.0, f)))


# ---------------------------------------------------------------- lettering on a finished sheet
def say(notes, d, words, at, size, color, hand=True, anchor="mm", slant=0.0, rough=0.35, amount=0.95, seed=0, spacing=0, squash=1.0):
    """Ask for words at a place on the thing (`at` in its own measurements, `size` in cm)."""
    if notes is None or d.shade:
        return
    px, py = d.pt(*at)
    notes.append(dict(words=words, at=(px, py), size=size * d.kat(*at), color=color, hand=hand, anchor=anchor, slant=slant, rough=rough, amount=amount, seed=seed, spacing=spacing, squash=squash))


def letter_on(lc, la, notes):
    """Paint the words asked for onto a line layer (color, alpha). The hand face has no dollar sign, so a
    '$' is painted the way a sign painter does it: an S with a stroke through it."""
    shape = la.shape
    for n in notes:
        words, strokes_ = n["words"], []
        if n["hand"] and "$" in words:
            f = letter.face(n["size"] * 3, True)
            from PIL import Image, ImageDraw
            dr = ImageDraw.Draw(Image.new("L", (8, 8)))
            plain = words.replace("$", "S")
            total = dr.textlength(plain, font=f) / 3
            x0 = n["at"][0] - (total / 2 if n["anchor"][0] == "m" else (total if n["anchor"][0] == "r" else 0))
            for i, ch in enumerate(words):
                if ch == "$":
                    xs = x0 + dr.textlength(plain[:i], font=f) / 3 + dr.textlength("S", font=f) / 6
                    strokes_.append(xs)
            words = plain
        m = letter.mask(shape, words, n["at"], n["size"], hand=n["hand"], anchor=n["anchor"], rough=n["rough"], slant=n["slant"], seed=n["seed"], spacing=n["spacing"], squash=n["squash"])
        for xs in strokes_:
            dy = 0.0 if n["anchor"][1] == "m" else -n["size"] * 0.36
            m = np.maximum(m, mask_line(shape, [(xs + 0.3, n["at"][1] + dy - n["size"] * 0.52), (xs - 0.3, n["at"][1] + dy + n["size"] * 0.50)], max(0.8, n["size"] * 0.10)))
        m = np.clip(m * n["amount"], 0, 1)
        over(lc, n["color"], m)
        la[...] = np.maximum(la, m)
    return lc, la


def render(shape, draw, at, yaw=0.0, unit=1.0, lift=0.0):
    """A thing on its two layers, lettered: -> (color, alpha, line color, line alpha)."""
    notes = []
    c, a, lc, la = stand_up(shape, lambda d, dl: draw(d, dl, notes), at, yaw, unit, lift)
    letter_on(lc, la, notes)
    return c, a, lc, la


def shade_of(shape, draw, at, yaw=0.0, unit=1.0, lift=0.0, soft=1.0):
    return shadow_of(shape, lambda d, dl: draw(d, dl, None), at, yaw, unit, lift, soft)


# ---------------------------------------------------------------- the old-timer's stand
WOOD = dict(top="#e2c594", top2="#d4b480", front="#a8855c", end="#f0d6a6", dark="#5e4634", leg="#b89a70", leg_lit="#e4c898", leg_dark="#7a6048")
UMB = dict(red=("#8f4f64", "#cf6f5e", "#f29a7e"), cream=("#a9a2c0", "#eadcc0", "#fff6dc"), pole=("#7c8098", "#b9bcc8", "#f4f4f0"), rib="#7a5560")
STAND_AT = (126.7, 424.5)                                   # the middle of the table's front edge, on the ground
UMB_TILT = 10.0


def umbrella_points(joint=(8.0, 156.0, 86.0), tilt=UMB_TILT, radius=120.0, rise=54.0, drop=58.0):
    """-> (apex, rim points round the canopy (16, counter-clockwise from the right), axis, rim middle)."""
    t = math.radians(tilt)
    ax = (math.sin(t), math.cos(t), 0.0)                   # the pole's upper half leans toward the sun
    e1 = (math.cos(t), -math.sin(t), 0.0)
    mid = tuple(joint[i] + ax[i] * drop for i in range(3))
    apex = tuple(mid[i] + ax[i] * rise for i in range(3))
    rim = []
    for i in range(16):
        a = math.radians(i * 22.5)
        sag = 1.0 if i % 2 == 0 else 0.965                  # the cloth dips a little between the ribs
        rim.append(tuple(mid[j] + (math.cos(a) * e1[j] + (math.sin(a) if j == 2 else 0.0)) * radius * sag for j in range(3)))
    return apex, rim, ax, mid


def draw_stand(d, dl, notes=None):
    """A board on two trestles with a painted price board hung on the front; lemonade, glasses and rocks
    on it; a cooler and a crate beneath; and a beach umbrella that has seen every summer since 1985."""
    # ---- the umbrella: its foot (an old tire rim full of concrete) and pole stand behind the table
    joint = (8.0, 156.0, 86.0)
    d.tube(8, 86, 17, 0, 9, ("#4a4450", "#7c7078", "#b0a49c"), cap="#8c8484")
    d.tube(8, 86, 2.2, 0, 156, UMB["pole"], n=3)
    apex, rim, ax, mid = umbrella_points(joint)
    d.line([joint, mid], UMB["pole"][1], 4.2)
    dl.line([(joint[0] - 1.2, joint[1], joint[2]), (mid[0] - 1.2, mid[1], mid[2])], UMB["pole"][0], 1.4, 0.8)
    dl.line([(joint[0] + 1.2, joint[1], joint[2]), (mid[0] + 1.2, mid[1], mid[2])], UMB["pole"][2], 1.2, 0.9)
    dl.ball(joint[0], joint[1], joint[2], 3.4, "#5a5a6a")                                  # the tilt joint
    order = sorted(range(8), key=lambda g: -math.sin(math.radians(g * 45 + 22.5)))          # far gores first
    for g in order:
        a0, am, a1 = rim[(2 * g) % 16], rim[(2 * g + 1) % 16], rim[(2 * g + 2) % 16]
        ang = math.radians(g * 45 + 22.5)
        t = math.radians(UMB_TILT)
        out = (math.cos(ang) * math.cos(t), -math.cos(ang) * math.sin(t), math.sin(ang))
        nrm = (out[0] * 0.42 + ax[0] * 0.91, out[1] * 0.42 + ax[1] * 0.91, out[2] * 0.42)
        f = facing(*nrm) * 1.15
        tones = UMB["red"] if g % 2 == 0 else UMB["cream"]
        c = mix(tones[0], tones[1], min(1.0, f * 2.2)) if f < 0.45 else mix(tones[1], tones[2], min(1.0, (f - 0.45) / 0.45))
        d.poly([apex, a0, am, a1], c)
        # the valance: a strip of the same cloth hanging from the rim, scalloped
        fv = facing(*out) * 0.9 + 0.12
        cv = mix(tones[0], tones[1], min(1.0, fv * 2.0)) if fv < 0.5 else mix(tones[1], tones[2], min(1.0, (fv - 0.5) / 0.5))
        lo = lambda p, k: (p[0] - ax[0] * k, p[1] - ax[1] * k, p[2])
        mid0 = tuple((a0[i] + am[i]) / 2 for i in range(3))
        mid1 = tuple((am[i] + a1[i]) / 2 for i in range(3))
        d.poly([a0, am, a1, lo(a1, 5), lo(mid1, 11), lo(am, 6), lo(mid0, 11), lo(a0, 5)], cv)
        if math.sin(ang) < 0.3:                                                             # the ribs that face us
            dl.line([apex, a0], UMB["rib"], 0.9, 0.55)
            dl.line([a0, am, a1], mix(tones[0], "#40304a", 0.3), 0.9, 0.5)
    dl.line([apex, (apex[0] + ax[0] * 9, apex[1] + ax[1] * 9, apex[2])], "#e8e4d8", 3.0)   # the knob on top
    dl.ball(apex[0] + ax[0] * 10, apex[1] + ax[1] * 10, apex[2], 2.6, "#fff8e4")

    # ---- under the table: a cooler and a crate of rocks not yet priced
    d.box(-52, -6, 0, 30, 22, 54, "#3f74b8", "#7fb0e4", "#5f98dc")
    d.box(-54, -4, 30, 37, 20, 56, "#d8d4cc", "#fbf8ee", "#f2eee2")
    d.line([(-52, 30, 22), (-6, 30, 22)], "#2c5690", 1.0, 0.8)
    d.line([(-40, 14, 22), (-18, 14, 22)], "#e4f0ff", 2.6, 0.9)
    d.box(14, 56, 0, 24, 16, 50, "#9a7a54", "#5a4638", "#d8b888")
    for yy in (8, 16):
        d.line([(14, yy, 16), (56, yy, 16)], "#5e4634", 1.0, 0.8)
    for k, (rx, rz, rr, col) in enumerate([(22, 24, 6, "#b8b0a8"), (34, 30, 7, "#c88468"), (46, 26, 6, "#e8e0e4"), (30, 40, 6, "#9a9088"), (44, 40, 7, "#d09a78")]):
        d.ball(rx, 26 + rr * 0.3, rz, rr, mix(col, "#5a4a58", 0.25))
        d.ball(rx + 1.5, 27 + rr * 0.5, rz, rr * 0.55, tone(col, 1.25, 0.03))

    # ---- the trestles: two sawhorses
    for tx in (-64, 64):
        for zz, col, wd in ((66, WOOD["leg_dark"], 4.5), (6, WOOD["leg"], 5.0)):          # back pair, then front pair
            for sgn in (-1, 1):
                foot = (tx + sgn * 17, 0, zz + (12 if zz > 30 else -12))
                head = (tx + sgn * 4, 72, zz)
                d.line([foot, head], col, wd)
                if zz < 30:
                    dl.line([(foot[0] + 1.6, foot[1], foot[2]), (head[0] + 1.6, head[1], head[2])], WOOD["leg_lit"], 1.3, 0.9)
                    dl.line([(foot[0] - 2.0, foot[1], foot[2]), (head[0] - 2.0, head[1], head[2])], WOOD["dark"], 1.0, 0.6)
        d.line([(tx - 11, 30, 2), (tx + 11, 30, 2)], WOOD["leg"], 4.0)                    # the brace across the front legs
        dl.line([(tx - 11, 31.5, 2), (tx + 11, 31.5, 2)], WOOD["leg_lit"], 1.0, 0.8)
        d.box(tx - 5, tx + 5, 70, 76, 2, 68, WOOD["front"], WOOD["top2"], WOOD["end"])

    # ---- the board they carry: three planks, grey with weather, bowed a little in the middle
    d.box(-97, 97, 76, 81, 0, 72, WOOD["front"], WOOD["top"], WOOD["end"])
    for zz in (24, 48):
        dl.line([(-97, 81, zz), (97, 81, zz)], "#8a6c4c", 0.9, 0.7)
    dl.line([(-97, 81, 0), (97, 81, 0)], "#fff0cc", 1.0, 0.85)                             # the near edge catches the light
    dl.line([(-97, 76, 0), (97, 76, 0)], WOOD["dark"], 1.0, 0.7)
    for xx in (-70, -20, 34, 78):
        dl.line([(xx, 81, 3), (xx + 9, 81, 3)], "#8a6c4c", 0.8, 0.5)

    # ---- on the table, left to right. A checked cloth under the lemonade.
    d.poly([(-93, 81.3, 6), (-34, 81.3, 6), (-34, 81.3, 64), (-93, 81.3, 64)], "#f4ead8")
    d.poly([(-92, 81.3, 0), (-35, 81.3, 0), (-36, 66, -0.5), (-64, 62, -0.5), (-91, 67, -0.5)], "#e4d8c8")
    for i in range(1, 9):
        xx = -93 + i * 6.6
        dl.line([(xx, 81.4, 6), (xx, 81.4, 64)], "#d06050", 2.2, 0.55)
        dl.line([(xx, 81, 0), (xx + 0.4, 66, -0.5)], "#c05848", 2.2, 0.55)
    for zz in (14, 26, 38, 50, 60):
        dl.line([(-93, 81.4, zz), (-34, 81.4, zz)], "#d06050", 2.4, 0.5)
    for yy in (70, 76):
        dl.line([(-91, yy, -0.5), (-36, yy, -0.5)], "#c05848", 2.2, 0.5)
    # the jug: glass, lemonade to the shoulder, slices of lemon, the low sun right through it
    jx, jz = -66, 36
    d.tube(jx, jz, 9.5, 81.5, 104, ("#c79a30", "#f6d850", "#fff6a8"), n=7, r1=8.5)
    d.tube(jx, jz, 8.5, 104, 110, ("#b9c8cc", "#e2eeee", "#ffffff"), n=5, cap="#f2f8f4", r1=9.0)
    dl.hdisc(jx, 104, jz, 8.3, "#fff0a0", 0.9)
    dl.ball(jx - 3, 98, jz - 9, 3.0, "#fff9c8", 0.95)
    dl.ball(jx + 3.5, 91, jz - 9, 2.8, "#ffec8a", 0.9)
    dl.line([(jx + 6.2, 85, jz - 7), (jx + 5.6, 102, jz - 7)], "#ffffff", 1.3, 0.9)        # the sun on the glass
    dl.line([(jx - 9.5, 101, jz), (jx - 16, 99, jz), (jx - 16, 90, jz), (jx - 9.5, 87, jz)], "#e4f0ee", 1.8, 0.9)   # the handle
    # glasses: one poured, two waiting upside down
    for gx, gz, full in ((-45, 22, True), (-37, 40, False), (-29, 26, False)):
        if full:
            d.tube(gx, gz, 3.4, 81.5, 90, ("#c79a30", "#f6d850", "#fff6a8"), n=3, r1=3.8)
            d.tube(gx, gz, 3.8, 90, 93, ("#b9c8cc", "#e2eeee", "#ffffff"), n=3, cap="#f4faf6", r1=4.0)
        else:
            d.tube(gx, gz, 4.0, 81.5, 92.5, ("#a9b8c8", "#dce8ec", "#ffffff"), n=3, cap="#eef6f4", r1=3.3)
        dl.line([(gx + 2.2, 83, gz - 3), (gx + 2.2, 91, gz - 3)], "#ffffff", 0.9, 0.9)
    # the jar the money goes in
    d.tube(-17, 30, 5.0, 81.5, 94, ("#8fa6a0", "#cfe0d8", "#f4fff8"), n=4, cap="#b8b0a0", r1=4.6)
    dl.line([(-20, 85, 25), (-14, 85, 25)], "#6a9a60", 2.0, 0.85)
    # rocks for sale: quartz, sandstone, a geode sawn in half, and one that is just a rock
    d.poly([(0, 81.5, 30), (4, 97, 30), (7.5, 83, 30)], "#d8d2e4")
    d.poly([(5, 81.5, 28), (11, 101, 28), (15, 82, 28)], "#f6f2fa")
    d.poly([(12, 81.5, 30), (19, 93, 30), (22, 81.5, 30)], "#c4bcd8")
    dl.line([(11, 101, 28), (13.6, 83, 28)], "#ffffff", 1.0, 0.9)
    dl.line([(4, 97, 30), (5.2, 83, 30)], "#ffffff", 0.8, 0.8)
    d.poly([(28, 81.5, 26), (27, 89, 27), (33, 93, 28), (48, 92, 28), (52, 87, 27), (51, 81.5, 26)], "#b8603e")      # sandstone, in layers
    d.poly([(27, 89, 27), (33, 93, 28), (48, 92, 28), (52, 87, 27), (44, 89.5, 27), (34, 90, 27)], "#e8946a")
    dl.line([(28.5, 85.5, 26), (51, 84.5, 26)], "#8a4630", 0.9, 0.7)
    dl.line([(29, 87.6, 26), (50, 86.8, 26)], "#f0b088", 0.8, 0.7)
    d.ball(63, 87.5, 34, 7.2, "#7a6a70", squash=0.82)                                       # the geode: grey rind, violet crystal
    dl.ball(63.4, 87.6, 33, 5.0, "#a070c8", squash=0.8)
    dl.ball(64.2, 88.4, 33, 2.6, "#e4c8f8", squash=0.8)
    d.ball(80, 86.5, 30, 6.6, "#8c847c", squash=0.75)                                       # just a rock
    dl.ball(81.6, 88, 30, 3.6, "#c8beb0", squash=0.7)
    for px_, pz_ in ((10, 12), (40, 10), (63, 14), (81, 12)):                              # price tags
        dl.poly([(px_ - 2.6, 81.6, pz_ - 3), (px_ + 2.6, 81.6, pz_ - 3), (px_ + 2.6, 81.6, pz_ + 3), (px_ - 2.6, 81.6, pz_ + 3)], "#fffaf0")
    # his father's Geiger counter, at the far end, in case anybody asks
    d.box(84, 96, 81.5, 90, 44, 62, "#5c6a44", "#8a9a68", "#a4b47c")
    dl.ball(90, 86, 44, 2.4, "#f4f0dc")
    dl.line([(85, 90, 53), (87, 95, 53), (93, 95, 53), (95, 90, 53)], "#3a3a34", 1.2, 0.9)

    # ---- the price board, hung from the front edge on two twists of wire, not quite level
    bx0, bx1, by0, by1, bz = -60, 62, 17, 69, -3.5
    quad = [(bx0, by1 - 3, bz), (bx1, by1, bz), (bx1 + 1, by0 + 2, bz), (bx0 + 1, by0, bz)]
    d.poly([(q[0] - 1.5, q[1] - 2.0, q[2]) for q in quad], "#4a3a34", 0.55)                # its shadow on the legs behind
    d.poly(quad, "#f3e9cf")
    d.poly([(bx0 + 1, by0, bz), (bx0 + 30, by0 + 0.5, bz), (bx0 + 18, by0 + 9, bz), (bx0 + 1, by0 + 12, bz)], "#dccfb2", 0.8)     # weathering in a corner
    d.poly([(bx1 - 26, by1 - 0.5, bz), (bx1, by1, bz), (bx1 + 0.5, by1 - 14, bz)], "#fff8e6", 0.8)
    dl.line(quad + [quad[0]], "#6e5840", 1.0, 0.7)
    dl.line([quad[0], quad[1]], "#fffdf0", 1.0, 0.8)
    for wx in (bx0 + 12, bx1 - 12):
        dl.line([(wx, by1 - 2, bz), (wx + 1, 78, -0.5)], "#4a4040", 0.8, 0.9)
    slant = (d.pt(bx1, by1, bz)[1] - d.pt(bx0, by1 - 3, bz)[1]) / (d.pt(bx1, by1, bz)[0] - d.pt(bx0, by1 - 3, bz)[0]) if not d.shade else 0.0
    say(notes, d, "LEMONADE $1", (1, 57.5, bz), 13.5, "#b63a2a", slant=-slant, seed=3)
    say(notes, d, "ROCKS $2", (1, 42.0, bz), 13.5, "#33405c", slant=-slant, seed=4)
    say(notes, d, "STORIES EXTRA", (1, 27.0, bz), 10.5, "#b63a2a", slant=-slant, seed=5)
    return d


# ---------------------------------------------------------------- the pump
RUST = dict(shade="#7c3528", front="#c2603e", lit="#f08a5c", dark="#4c2018", worn="#d9a07c", cream="#f1e6cc")
PUMP_AT = (-105.0, 808.0)
ISLAND = (-150, 110, -62, 62, 12)                           # the slab it stands on: x0, x1, z0, z1 (about the pump), and its height


def draw_island(d, dl, notes=None):
    x0, x1, z0, z1, h = ISLAND
    d.box(x0, x1, 0, h, z0, z1, "#b9a996", "#e4d6c0", "#f2e4cc")
    dl.line([(x0, h, z0), (x1, h, z0)], "#fff6e2", 0.9, 0.7)
    dl.line([(x0, 0, z0), (x1, 0, z0)], "#6e6058", 1.0, 0.6)
    dl.line([(-60, h, z0), (-52, h, -20), (-64, h, 10), (-58, h, z1)], "#8a7a6c", 0.9, 0.7)          # it has cracked across
    dl.line([(-56, h, z0), (-55, 0, z0)], "#6e6058", 0.9, 0.7)
    dl.line([(52, h, z0), (60, h, -30), (54, h, 0)], "#8a7a6c", 0.8, 0.6)
    return d


def draw_pump(d, dl, notes=None):
    """A gas pump from long ago: a tall rust-red cabinet with a clock face, and a white glass globe on top."""
    d.box(-27, 27, 0, 9, -19, 19, "#4c4850", "#8a8690", "#a8a4ac")
    d.box(-24, 24, 9, 128, -16, 16, RUST["front"], RUST["lit"], RUST["lit"])
    d.box(-22, 22, 128, 135, -14, 14, RUST["front"], RUST["worn"], RUST["lit"])
    d.box(-17, 17, 135, 140, -11, 11, "#8a3c2c", RUST["worn"], RUST["front"])
    d.tube(0, 0, 6.5, 140, 151, ("#6a6a78", "#b4b6c0", "#f4f4ee"), n=4)
    # the globe
    d.ball(0, 170, 0, 20, "#cfc8dc")
    d.ball(2.5, 171.5, 0, 17.5, "#f6eedc")
    dl.ball(6.5, 175, 0, 10.5, "#fffcf0")
    dl.line([(-15.5, 168.2, 0), (-8, 166.4, 0), (4, 165.8, 0), (12, 166.6, 0), (16.0, 168.2, 0)], "#c2503c", 5.4, 0.8)       # a faded red band round it
    dl.ball(9.5, 178.5, 0, 3.2, "#ffffff")
    dl.line([(-12, 152, -6), (12, 152, -6)], "#5a5a66", 2.0)
    # the front: a cream face with the dials, a blank plate, a door with a lock
    d.poly([(-18, 88, -16), (18, 88, -16), (18, 122, -16), (-18, 122, -16)], RUST["cream"])
    dl.line([(-18, 88, -16), (18, 88, -16), (18, 122, -16), (-18, 122, -16), (-18, 88, -16)], "#6a3024", 1.0, 0.8)
    for yy, col in ((113, "#2a2a30"), (103, "#2a2a30")):
        dl.poly([(-13, yy, -16), (13, yy, -16), (13, yy + 6, -16), (-13, yy + 6, -16)], col)
        for xx in (-9, -3, 3, 9):
            dl.line([(xx, yy + 1.5, -16), (xx, yy + 4.5, -16)], "#f4f0e0", 1.6, 0.9)
    dl.poly([(-11, 91, -16), (11, 91, -16), (11, 99, -16), (-11, 99, -16)], "#c2503c", 0.85)
    dl.line([(-7, 95, -16), (7, 95, -16)], "#f1e6cc", 1.2, 0.8)
    d.poly([(-19, 16, -16), (19, 16, -16), (19, 80, -16), (-19, 80, -16)], mix(RUST["front"], RUST["shade"], 0.25))
    dl.line([(-19, 16, -16), (19, 16, -16), (19, 80, -16), (-19, 80, -16), (-19, 16, -16)], RUST["dark"], 1.0, 0.75)
    dl.line([(-19, 80, -16), (19, 80, -16)], RUST["lit"], 0.9, 0.7)
    dl.ball(13, 50, -16, 1.8, "#d8d4cc")
    # forty years of weather: rust blooming up from the foot, paint gone to primer in patches
    d.poly([(-24, 9, -16), (24, 9, -16), (24, 20, -16), (10, 28, -16), (-4, 21, -16), (-16, 30, -16), (-24, 24, -16)], "#6a2c1c", 0.8)
    d.poly([(-8, 60, -16), (2, 66, -16), (6, 58, -16), (-2, 52, -16)], RUST["worn"], 0.7)
    d.poly([(-22, 100, -16), (-18, 112, -16), (-22, 124, -16)], "#8a4a34", 0.8)
    dl.line([(-24, 128, -16), (24, 128, -16)], "#ffc49c", 1.0, 0.8)
    dl.line([(24, 9, -16), (24, 128, -16)], "#ffd0a8", 1.0, 0.75)                          # the corner toward the sun
    dl.line([(-24, 9, -16), (-24, 128, -16)], RUST["dark"], 1.0, 0.6)
    # a card somebody taped to the door long ago
    dl.poly([(-12, 64, -16.3), (9, 66, -16.3), (8.5, 76, -16.3), (-12.5, 74, -16.3)], "#f2ead2")
    dl.line([(-9, 71.5, -16.3), (6, 72.8, -16.3)], "#4a3a34", 1.3, 0.85)
    dl.line([(-9, 67.6, -16.3), (2, 68.6, -16.3)], "#4a3a34", 1.3, 0.85)
    # the hose and the nozzle, on the side toward the sun
    d.box(24, 30, 84, 104, -8, 8, "#5a2a20", "#b05a3c", "#8a4430")
    dl.line([(27, 110, 0), (34, 112, 0), (42, 96, 0), (45, 60, 0), (40, 34, 0), (33, 30, 0), (30, 46, 0), (31, 86, 0)], "#1c1a20", 3.4)
    dl.line([(43, 94, 0), (46, 60, 0), (41, 36, 0)], "#5c5a68", 1.0, 0.8)
    dl.line([(31, 86, -2), (30, 99, -2), (37, 104, -2)], "#c8ccd4", 3.0)
    dl.line([(30, 99, -2), (37, 104, -2)], "#ffffff", 1.0, 0.9)
    return d


# ---------------------------------------------------------------- Mom's car
TEAL = dict(top="#86d0c4", sky="#b8e8e0", shine="#eafcf6", side="#3a998c", side_hi="#5cb6a8", low="#2a766c", front="#8edccc", hood="#9fe2d4", dark="#17463f", seam="#1d564e")
GLASS = dict(dark="#16242e", mid="#2e4a62", sky="#9cc6e6", shine="#f0f8ff")
CHROME = dict(shine="#ffffff", light="#dde2e6", mid="#a0a8b0", dark="#585e68")
RUBBER = dict(lit="#55505c", mid="#2c2932", dark="#141218")
CAR_AT = (-625.0, 12.0)                                     # the rear near corner of the car on the ground; it points along +x
CAR_W = 168.0


def _nose_x(y):
    return float(np.interp(y, [20, 28, 46, 68, 82], [382, 390, 393.5, 391, 384]))


def car_profile(d):
    """The outline of the side of the body, clockwise from the bottom of the rear bumper."""
    pts = [(10, 22), (3, 32), (1, 60), (5, 86), (13, 108), (42, 140), (64, 148.5), (150, 153.5), (205, 152), (230, 147), (306, 106), (342, 101), (370, 93), (384, 82), (391, 68), (393.5, 46), (390, 28), (382, 20), (360, 20)]
    pts += d.arc(322, 31, 35, -18, 198, 14)[1:-1] + [(284, 20), (110, 20)] + d.arc(72, 31, 35, -18, 198, 14)[1:-1] + [(34, 20)]
    return pts


def draw_car(d, dl, notes=None):
    """A small, tidy, modern hatchback, teal, parked parallel to nothing. We see its near side, the top of
    it, and its face, which is turned to the morning sun."""
    D = CAR_W
    # ---- it is dark under the car, and the far wheels stand in that dark
    for z in (D, 0):
        d.poly([(40, 6), (356, 6), (360, 24), (36, 24)], "#1c1a24", z=z)
    for cx in (72, 322):
        d.disc(cx, 31, 30, RUBBER["dark"], z=D - 10)

    # ---- the face: bumper, grille, lamps, plate
    face = [(382, 20), (390, 28), (393.5, 46), (391, 68), (384, 82)]
    d.side(face, 0, D, TEAL["front"])
    d.side([(382, 20), (390, 28), (393, 41)], 0, D, mix(TEAL["front"], TEAL["low"], 0.5))               # the chin turns under, out of the light
    quad = lambda y0, y1, z0, z1: [(_nose_x(y0) + 0.4, y0, z0), (_nose_x(y0) + 0.4, y0, z1), (_nose_x(y1) + 0.4, y1, z1), (_nose_x(y1) + 0.4, y1, z0)]
    dl.poly(quad(27, 41, 28, D - 28), "#1c2026")                                                        # the air intake
    dl.poly(quad(65, 72, 44, D - 44), "#20262c")                                                        # the slot of the grille
    dl.line([quad(68.5, 68.5, 46, D - 46)[0], quad(68.5, 68.5, 46, D - 46)[1]], CHROME["light"], 1.2, 0.9)
    dl.poly(quad(46, 58, 62, D - 62), "#f6f2e2")                                                        # the plate
    dl.line([(_nose_x(52) + 0.6, 52, 70), (_nose_x(52) + 0.6, 52.6, 84), (_nose_x(52) + 0.6, 51.6, 98)], "#3a4a6a", 2.0, 0.8)
    for z0, z1 in ((3, 40), (D - 40, D - 3)):                                                           # head lamps: clear lenses, a point of sun in each
        dl.poly(quad(64, 80, z0, z1), CHROME["mid"])
        dl.poly(quad(66, 78.5, z0 + 3, z1 - 3), "#f4f6ec")
        dl.poly(quad(71, 77, z0 + 6, z0 + 16), "#ffffff")
    for zc in (18, D - 18):
        c = dl.pt(_nose_x(34) + 0.6, 34, zc)
        dl.s.ellipse(c[0], c[1], 4.2 * d.k * 0.5, 4.2 * d.k, "#e8ecd8")
    dl.line([(_nose_x(60) + 0.5, 60, 2), (_nose_x(60) + 0.5, 60, D - 2)], TEAL["seam"], 1.0, 0.5)

    # ---- the faces that look up at the sky: hood, windshield, roof
    hood = [(306, 106), (342, 101), (370, 93), (384, 82)]
    d.side(hood, 0, D, TEAL["hood"])
    d.poly([(310, 105.4, 96), (382, 83.4, 96), (384, 82, D), (306, 106, D)], TEAL["sky"], 0.55)        # its far half holds the pale sky by the horizon
    d.poly([(314, 105, 16), (366, 94.6, 16), (366, 94.6, 46), (314, 105, 40)], TEAL["shine"], 0.6)     # and the morning slides along the near half
    d.poly([(370, 93, 0), (384, 82, 0), (384, 82, D), (370, 93, D)], mix(TEAL["hood"], TEAL["front"], 0.5))
    dl.line([(384, 82, 0), (384, 82, D)], TEAL["shine"], 1.0, 0.7)
    dl.line([(310, 105.6, 6), (310, 105.6, D - 6)], TEAL["seam"], 1.0, 0.55)
    dl.line([(310, 105.4, 34), (380, 84.4, 30)], TEAL["seam"], 0.8, 0.35)
    dl.line([(310, 105.4, D - 34), (380, 84.4, D - 30)], TEAL["seam"], 0.8, 0.35)
    d.side([(230, 147), (306, 106)], 0, D, mix(TEAL["top"], TEAL["dark"], 0.5))                      # the windshield's frame
    d.side([(233, 145), (303, 108)], 7, D - 7, GLASS["sky"])
    d.poly([(233, 145, 7), (303, 108, 7), (303, 108, 36), (233, 145, 50)], GLASS["shine"], 0.75)   # the sky in the glass
    d.poly([(233, 145, 70), (262, 129.7, 64), (262, 129.7, 96), (233, 145, 104)], "#c8e2f4", 0.6)
    d.poly([(278, 121.2, 60), (303, 108, 52), (303, 108, D - 7), (278, 121.2, D - 7)], GLASS["mid"], 0.9)   # the dashboard's shadow
    d.poly([(242, 140.2, 110), (258, 131.8, 108), (258, 131.8, 138), (242, 140.2, 142)], GLASS["dark"], 0.5)       # a head rest inside
    dl.line([(301, 109.2, 64), (280, 120.2, 30)], "#20262c", 1.3, 0.9)                                  # the wipers, parked
    dl.line([(301, 109.2, 122), (280, 120.2, 88)], "#20262c", 1.3, 0.9)
    roof = [(42, 140), (64, 148.5), (150, 153.5), (205, 152), (230, 147)]
    d.side(roof, 0, D, TEAL["top"])
    d.poly([(64, 148.5, 80), (150, 153.5, 80), (205, 152, 86), (230, 147, 92), (230, 147, D), (64, 148.5, D)], TEAL["sky"], 0.6)        # the far half of the roof is full of sky
    d.poly([(70, 149.2, 12), (224, 148.6, 12), (224, 148.6, 34), (70, 149.2, 34)], TEAL["shine"], 0.55)
    d.poly([(100, 151.2, 46), (190, 152.6, 46), (196, 152.3, 62), (104, 151.4, 60)], "#f4c8b8", 0.35)   # and a rose cloud is in the paint
    dl.line([(230, 147, 0), (230, 147, D)], TEAL["seam"], 1.0, 0.6)
    dl.line([(64, 148.5, 0), (150, 153.5, 0), (205, 152, 0), (230, 147, 0)], TEAL["shine"], 1.0, 0.8)
    dl.line([(92, 151, D / 2), (80, 163, D / 2)], "#26282e", 1.2)                                       # the aerial

    # ---- the side we see: it holds the horizon, as polished paint does
    P = car_profile(d)
    d.poly(P, TEAL["side"])
    d.poly([(13, 108), (42, 140), (64, 148.5), (150, 153.5), (205, 152), (230, 147), (306, 106), (301, 102), (238, 105), (60, 106)], TEAL["side_hi"], 0.7)   # above the shoulder it turns to the sky
    d.poly([(5, 86), (13, 104), (150, 104), (300, 102), (370, 91), (382, 82), (388, 70), (300, 80), (150, 82), (6, 80)], TEAL["side_hi"], 0.55)        # the shoulder: sky again
    d.poly([(4, 74), (150, 76), (300, 74), (391, 62), (392, 54), (300, 64), (150, 66), (3, 64)], TEAL["low"], 0.55)                                    # then the dark line of the far land
    d.poly([(2, 58), (150, 60), (300, 58), (393, 48), (392, 40), (2, 40)], "#d0aa80", 0.20)             # then the pale desert floor
    d.poly([(3, 32), (10, 22), (34, 20), (110, 20), (284, 20), (360, 20), (382, 20), (390, 28), (392, 40), (2, 40)], TEAL["low"], 0.85)                # below, it turns under
    d.poly([(10, 22), (382, 20), (383, 26), (10, 28)], "#1e2428")                                       # the sill
    d.poly([(120, 24), (286, 24), (300, 42), (250, 35), (150, 34), (112, 40)], "#d8b890", 0.20)         # dust from thirty-seven miles of it
    # glass: one dark shape, then each window
    d.poly([(66, 105), (46, 135), (60, 146), (228, 146), (301, 106)], "#141a20")
    wins = ([(72, 109), (54, 134), (62, 140.5), (110, 141.5), (115, 109)], [(122, 109), (117, 141.5), (189, 142.5), (189, 108.5)], [(197, 108.5), (197, 143.5), (225, 143), (291, 108)])
    for w in wins:
        d.poly(w, GLASS["dark"])
        x0, x1 = min(p[0] for p in w), max(p[0] for p in w)
        d.poly([(x0 + 10, 119), (x1 - 16, 119), (x1 - 26, 139), (x0 + 8, 139)], GLASS["mid"])          # the far windows, seen through
        d.poly([(x0 + 14, 129), (x1 - 24, 129), (x1 - 28, 139), (x0 + 12, 139)], "#d0bca0", 0.6)       # and the desert beyond them
        d.poly([(x0 + 4, 111), (x0 + 15, 111), (x0 + 34, 140.5), (x0 + 23, 140.5)], GLASS["sky"], 0.55)   # a slant of sky
        d.poly([(x0 + 20, 111), (x0 + 24, 111), (x0 + 43, 140.5), (x0 + 39, 140.5)], GLASS["sky"], 0.35)
        dl.line([w[i] for i in range(len(w))] + [w[0]], "#0e1216", 1.4, 0.9)
    d.poly([(204, 109), (222, 109), (223, 125), (218, 131), (208, 131), (203, 125)], "#0c1016")         # the driver's seat
    d.poly([(134, 109), (150, 109), (151, 123), (146, 128), (138, 128), (133, 123)], "#0c1016", 0.9)
    dl.line([(46, 135), (60, 146), (228, 146), (301, 106)], CHROME["light"], 0.9, 0.7)              # a bright line round the glass
    # seams and handles
    dl.line([(193, 142), (193, 28)], TEAL["seam"], 1.2, 0.85)
    dl.line([(118, 141), (116, 78), (110, 62), (104, 54)], TEAL["seam"], 1.2, 0.85)
    dl.line([(300, 105), (302, 72), (297, 58)], TEAL["seam"], 1.2, 0.85)
    for hx in (170, 96):
        dl.line([(hx, 98), (hx + 15, 98)], CHROME["light"], 2.4)
        dl.line([(hx, 96.4), (hx + 15, 96.4)], TEAL["dark"], 1.0, 0.8)
    dl.line([(14, 104.5), (150, 106.5), (300, 104), (370, 92.4), (384, 82)], TEAL["shine"], 1.1, 0.8)   # the shoulder catches the sky
    dl.line([(120, 44), (284, 44)], TEAL["seam"], 2.6, 0.5)                                             # a rubbing strip
    d.poly([(370, 93), (384, 82), (391, 68), (377, 70), (363, 82)], CHROME["mid"])                      # the head lamp wraps round the corner
    d.poly([(373, 89), (383.4, 81), (389, 70), (378, 72), (367, 82)], "#f2f4ea")
    dl.line([(375, 87), (383, 80)], "#ffffff", 1.4, 0.9)
    d.poly([(1, 60), (5, 86), (13, 108), (23, 104), (15, 82), (10, 60)], "#c8362c")                     # and the tail lamp, at the other end
    d.poly([(386, 30), (393, 36), (393.5, 46), (385, 44)], "#2a3036")
    # the wheels: clean, of course
    for cx in (72, 322):
        d.poly(d.arc(cx, 31, 37, -14, 194, 16), TEAL["low"])
        dl.line(d.arc(cx, 31, 37, -8, 188, 16), TEAL["side_hi"], 1.0, 0.7)
        d.poly(d.arc(cx, 31, 33.5, -20, 200, 16), "#101014")
        d.disc(cx, 31, 30, RUBBER["mid"])
        d.poly(d.arc(cx, 31, 30, 200, 340, 10) + [(cx, 31)], RUBBER["dark"])
        d.poly(d.arc(cx, 31, 30, -30, 60, 8) + list(reversed(d.arc(cx, 31, 26, -30, 60, 8))), RUBBER["lit"])
        d.disc(cx, 31, 20, CHROME["mid"])
        d.disc(cx + 0.8, 31.8, 18, CHROME["light"])
        for a in range(18, 378, 72):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            dl.poly([(cx + ca * 5 - sa * 3.4, 31 + sa * 5 + ca * 3.4), (cx + ca * 18 - sa * 4.6, 31 + sa * 18 + ca * 4.6), (cx + ca * 18 + sa * 4.6, 31 + sa * 18 - ca * 4.6), (cx + ca * 5 + sa * 3.4, 31 + sa * 5 - ca * 3.4)], CHROME["dark"], 0.9)
        dl.poly(d.arc(cx, 31, 5.5, 0, 360, 12), CHROME["mid"])
        dl.poly(d.arc(cx + 1.4, 32.6, 2.6, 0, 360, 10), CHROME["shine"])
        dl.line(d.arc(cx, 31, 19, 20, 100, 6), CHROME["shine"], 1.2, 0.8)
    # the door mirror stands out toward us
    dl.line([(284, 112, 0), (282, 114, -9)], TEAL["dark"], 2.4)
    c = dl.pt(280, 117, -13)
    dl.s.ellipse(c[0], c[1], 8.5 * d.k, 6.0 * d.k, TEAL["side"])
    dl.s.ellipse(c[0] + 1.2 * d.k, c[1] - 1.0 * d.k, 6.0 * d.k, 3.8 * d.k, TEAL["side_hi"])
    dl.s.ellipse(c[0] + 2.4 * d.k, c[1] - 2.0 * d.k, 2.6 * d.k, 1.6 * d.k, TEAL["shine"])
    return d


# ---------------------------------------------------------------- the shack
SHACK_YAW = 12.0
SHACK_W, SHACK_D, SHACK_H = 380.0, 300.0, 250.0
SHACK_AT = (-232.6 - SHACK_W * math.cos(math.radians(SHACK_YAW)), 1084.0 + SHACK_W * math.sin(math.radians(SHACK_YAW)))   # its front left corner
PAINTS = ["#86b8ac", "#e6d6b2", "#a89a88", "#c0745a", "#d8c8a0", "#94b0a8", "#b8a890"]      # forty years of whatever was in the can
SHACK = dict(shade="#5a4e78", deck="#d8bc94", deck_front="#8a6e58", roof="#b0705a", roof2="#c9a48c", tin="#b8bcc4", sign="#f4ead0", door="#33282e", frame="#e2cfa8")


def roof_y(z):
    """The height of the shack's tin roof at depth z: low over the porch, rising to the back wall."""
    return 236.0 + (z + 118.0) * (60.0 / 428.0)


def draw_shack(d, dl, notes=None, rng_seed=5):
    """LAST STOP: a board shack with a tin roof and a porch, held together by paint and optimism."""
    rng = np.random.default_rng(rng_seed)
    Wd, Dp, Ht = SHACK_W, SHACK_D, SHACK_H
    # ---- the porch floor and its step
    d.box(-14, Wd + 14, 0, 16, -112, 0, SHACK["deck_front"], SHACK["deck"], "#f0d8ac")
    for zz in (-92, -70, -48, -26):
        dl.line([(-14, 16, zz), (Wd + 14, 16, zz)], "#a08468", 1.0, 0.6)
    dl.line([(-14, 16, -112), (Wd + 14, 16, -112)], "#fff0d0", 1.0, 0.7)
    d.box(196, 300, 0, 8, -136, -112, "#7a6250", "#c8aa84", "#e4c89c")
    # ---- the side wall toward the sun: bare boards gone silver, hot with light
    side = [(Wd, 16, 0), (Wd, 16, Dp), (Wd, roof_y(Dp) - 2, Dp), (Wd, Ht, 0)]
    d.poly(side, "#f2cc9c")
    for zz in np.arange(24, Dp, 24):
        dl.line([(Wd, 16, zz), (Wd, roof_y(zz) - 4, zz)], "#b08a68", 0.9, 0.6)
    d.poly([(Wd, 128, 120), (Wd, 128, 184), (Wd, 190, 184), (Wd, 190, 120)], "#3a3040")
    dl.line([(Wd, 128, 120), (Wd, 128, 184), (Wd, 190, 184), (Wd, 190, 120), (Wd, 128, 120)], "#fff0d0", 1.6, 0.9)
    for zc, yc in ((40, 150), (72, 176), (66, 120)):                    # hub caps he has found along the road
        dl.poly([(Wd + 1, yc + math.sin(a) * 17, zc + math.cos(a) * 17) for a in np.linspace(0, 2 * math.pi, 14)], "#c8ccd4")
        dl.poly([(Wd + 1, yc + 3 + math.sin(a) * 8, zc - 3 + math.cos(a) * 8) for a in np.linspace(0, 2 * math.pi, 10)], "#ffffff")
    # ---- the front: every board a different paint, and the porch roof's shadow slanting across them
    n = 15
    for i in range(n):
        x0, x1 = Wd * i / n, Wd * (i + 1) / n
        c = mix(PAINTS[int(rng.integers(len(PAINTS)))], "#e0c8a0", 0.18 + 0.25 * rng.random())
        top = Ht - rng.random() * 3
        d.poly([(x0, 16, 0), (x1, 16, 0), (x1, top, 0), (x0, top, 0)], c)
        dl.line([(x1, 16, 0), (x1, top, 0)], "#5a4a44", 0.9, 0.55)
        dl.line([(x0 + 1.2, 16, 0), (x0 + 1.2, top, 0)], "#fff4d8", 0.8, 0.35)
        if rng.random() < 0.4:                                          # where the paint has gone and the wood shows
            y0 = 30 + rng.random() * 150
            d.poly([(x0 + 2, y0, 0), (x1 - 2, y0 + 6, 0), (x1 - 3, y0 + 40 + rng.random() * 30, 0), (x0 + 3, y0 + 30, 0)], "#a8947c", 0.7)
    # the door: a screen door, dark behind
    d.poly([(222, 16, 0), (318, 16, 0), (318, 212, 0), (222, 212, 0)], SHACK["frame"])
    d.poly([(230, 18, 0), (310, 18, 0), (310, 204, 0), (230, 204, 0)], SHACK["door"])
    d.poly([(230, 18, 0), (310, 18, 0), (310, 48, 0), (230, 48, 0)], "#8a7460")                         # its kick board
    dl.line([(230, 112, 0), (310, 112, 0)], SHACK["frame"], 2.2, 0.9)
    dl.line([(270, 48, 0), (270, 204, 0)], "#6a5a58", 1.0, 0.6)
    dl.poly([(252, 150, 0), (290, 152, 0), (289, 172, 0), (251, 170, 0)], "#f6efdc")                    # a card in the door: he is open
    dl.line([(258, 161, 0), (284, 162, 0)], "#c0402e", 3.0, 0.9)
    # the hatch he serves through: a shelf, a blind half down, a shutter propped up on a stick
    d.poly([(40, 104, 0), (196, 104, 0), (196, 196, 0), (40, 196, 0)], SHACK["frame"])
    d.poly([(48, 110, 0), (188, 110, 0), (188, 190, 0), (48, 190, 0)], "#2e2632")
    d.poly([(48, 150, 0), (188, 150, 0), (188, 190, 0), (48, 190, 0)], "#7f9cb8")
    dl.line([(48, 150, 0), (188, 150, 0)], "#d8e4ee", 1.2, 0.8)
    for jx, col in ((64, "#e8d47a"), (82, "#c86a50"), (100, "#e8e4f0"), (126, "#8a6ab0"), (150, "#6aa890"), (172, "#d8a070")):     # jars and rocks on the sill inside
        dl.line([(jx, 112, 0), (jx, 124 + (jx % 9), 0)], col, 9.0, 0.95)
    d.box(30, 206, 96, 104, -26, 0, "#b89870", "#ecd4a8", "#f4dcb0")
    d.poly([(36, 198, -2), (200, 198, -2), (200, 168, -62), (36, 168, -62)], "#d8c090")              # the shutter
    dl.line([(36, 168, -62), (200, 168, -62)], "#fff0cc", 1.2, 0.8)
    dl.line([(190, 104, -24), (192, 168, -60)], "#6a5444", 2.0, 0.9)
    # the porch roof's shadow: the sun comes from so far round to the right that only the low right of the wall is lit
    cut = lambda x: Ht - 4 - (-1.0 / SUN[0]) * (Wd + 16 - x)
    d.poly([(0, max(cut(0), 16), -0.5), (Wd, cut(Wd), -0.5), (Wd, Ht, -0.5), (0, Ht, -0.5)], SHACK["shade"], 0.50)
    # ---- on the porch: a bench of rocks, geraniums in coffee cans, an ice chest, a broom
    d.box(24, 150, 16, 22, -84, -52, "#5a4838", "#6a5646", "#8a7058")
    d.box(20, 154, 44, 50, -86, -50, "#9a7c5c", "#e0c498", "#f0d4a8")
    for bx in (30, 142):
        d.line([(bx, 16, -68), (bx, 44, -68)], "#7a6048", 5.0)
    for k, (rx, col) in enumerate([(36, "#c8c0b8"), (52, "#d08868"), (68, "#f0ecf4"), (86, "#a89888"), (102, "#b890d0"), (120, "#d8a880"), (136, "#9aa8a0")]):
        d.ball(rx, 56 + (k % 3), -68, 6.5 + (k % 2) * 1.5, mix(col, "#5a4a60", 0.2), squash=0.8)
        dl.ball(rx + 1.6, 58 + (k % 3), -68, 3.4, tone(col, 1.2, 0.03), squash=0.8)
    for px_, col in ((170, "#b8483a"), (188, "#d8d0c0"), (332, "#3f74b8")):                             # coffee cans
        d.tube(px_, -96, 8, 16, 34, (mix(col, "#40304a", 0.5), col, tone(col, 1.3)), n=4)
        for j in range(7):
            a = rng.uniform(0.3, 2.8)
            l = rng.uniform(10, 22)
            dl.line([(px_, 34, -96), (px_ + math.cos(a) * l * 0.6, 34 + math.sin(a) * l, -96)], "#5a7a3c", 1.6, 0.9)
            if j % 2 == 0:
                dl.ball(px_ + math.cos(a) * l * 0.6, 35 + math.sin(a) * l, -96, 3.2, "#e0483c")
    d.box(328, 376, 16, 62, -70, -28, "#c9c4c0", "#f4f0e8", "#fffaf0")                                   # the ice chest
    d.box(326, 378, 62, 70, -72, -26, "#a8483a", "#d87a60", "#e89478")
    dl.line([(334, 40, -70), (370, 40, -70)], "#8a8690", 1.2, 0.7)
    dl.line([(206, 16, -30), (214, 150, -4)], "#b89a6a", 2.0, 0.9)                                       # the broom
    dl.line([(202, 16, -34), (210, 16, -30), (208, 40, -28)], "#d8b060", 5.0, 0.9)
    # ---- the porch posts and the roof
    for px_ in (-6, Wd + 6):
        d.line([(px_, 16, -108), (px_, roof_y(-108) - 2, -108)], "#b89a78", 9.0)
        dl.line([(px_ + 3, 16, -108), (px_ + 3, roof_y(-108) - 2, -108)], "#fff0cc", 2.0, 0.8)
        dl.line([(px_ - 3.5, 16, -108), (px_ - 3.5, roof_y(-108) - 2, -108)], "#5a4a44", 1.4, 0.6)
    z0, z1 = -118.0, Dp + 10.0
    d.poly([(-18, roof_y(z0), z0), (Wd + 18, roof_y(z0), z0), (Wd + 18, roof_y(z1), z1), (-18, roof_y(z1), z1)], SHACK["roof"])
    sheets = 10                                                         # sheets of tin, some newer than others
    for i in range(sheets):
        x0, x1 = -18 + (Wd + 36) * i / sheets, -18 + (Wd + 36) * (i + 1) / sheets
        c = [SHACK["roof"], SHACK["roof2"], SHACK["tin"], "#9c6450", "#c08a70"][int(rng.integers(5))]
        zb = z1 if rng.random() < 0.7 else z1 - 60
        d.poly([(x0, roof_y(z0), z0), (x1, roof_y(z0), z0), (x1, roof_y(zb), zb), (x0, roof_y(zb), zb)], c, 0.85)
        for j in range(1, 4):
            xx = x0 + (x1 - x0) * j / 4
            dl.line([(xx, roof_y(z0), z0), (xx, roof_y(z1), z1)], "#6a4034", 0.8, 0.35)
        dl.line([(x0, roof_y(z0), z0), (x0, roof_y(z1), z1)], "#ffe0c0", 0.8, 0.45)
    d.poly([(-18, roof_y(z0), z0), (Wd + 18, roof_y(z0), z0), (Wd + 18, roof_y(z0) - 5, z0), (-18, roof_y(z0) - 5, z0)], "#5c3a34")       # the eave, and the dark under it
    dl.line([(-18, roof_y(z0), z0), (Wd + 18, roof_y(z0), z0)], "#ffd8b8", 1.2, 0.85)
    d.poly([(Wd + 18, roof_y(z0), z0), (Wd + 18, roof_y(z1), z1), (Wd + 18, roof_y(z1) - 5, z1), (Wd + 18, roof_y(z0) - 5, z0)], "#e8b890")
    # the stove pipe
    d.tube(316, 190, 7.5, roof_y(190), 352, ("#3c3440", "#6c606c", "#b8a8a0"), n=4)
    d.poly([(302, 352, 190), (330, 352, 190), (316, 366, 190)], "#4a4048")
    # ---- LAST STOP: a board up on the roof, propped from behind, one end lower than the other
    sz = -74.0
    for sx in (86, 300):
        d.line([(sx, roof_y(sz + 60), sz + 60), (sx, 344, sz + 4)], "#6a5444", 5.0)
        d.line([(sx, roof_y(sz), sz), (sx, 296, sz)], "#7a6450", 6.0)
    board = [(52, 286, sz), (336, 292, sz), (337, 354, sz), (51, 347, sz)]
    d.poly(board, SHACK["sign"])
    d.poly([(52, 286, sz), (130, 287.6, sz), (110, 300, sz), (52, 304, sz)], "#e2d4b4", 0.8)
    d.poly([(260, 352.2, sz), (337, 354, sz), (337, 330, sz)], "#fffaea", 0.8)
    dl.line(board + [board[0]], "#7a6450", 1.2, 0.8)
    dl.line([board[3], board[2]], "#fffdf2", 1.0, 0.9)
    if not d.shade:
        a, b = d.pt(52, 316, sz), d.pt(336, 322, sz)
        slant = (b[1] - a[1]) / (b[0] - a[0])
        say(notes, d, "LAST STOP", (195, 319, sz), 47.0, "#b8382a", slant=-slant, seed=11, rough=0.4)
    # ---- a wind sock on a pole at the back corner, hanging slack: there is no wind this morning
    mx, mz = 30.0, 270.0
    d.line([(mx, roof_y(mz), mz), (mx, 468, mz)], "#8a8e9c", 4.0)
    dl.line([(mx + 1.5, roof_y(mz), mz), (mx + 1.5, 468, mz)], "#f0f0ea", 1.2, 0.8)
    sock = [(mx, 468, mz), (mx - 6, 452, mz), (mx - 30, 420, mz), (mx - 44, 380, mz), (mx - 52, 384, mz), (mx - 44, 424, mz), (mx - 22, 456, mz), (mx - 14, 470, mz)]
    d.poly(sock, "#e88a50")
    d.poly([(mx - 13, 444, mz), (mx - 30, 420, mz), (mx - 37, 425, mz), (mx - 20, 450, mz)], "#f8f0e0")
    d.poly([(mx - 40, 392, mz), (mx - 44, 380, mz), (mx - 52, 384, mz), (mx - 47, 396, mz)], "#f8f0e0")
    dl.line([(mx - 6, 452, mz), (mx - 30, 420, mz), (mx - 44, 380, mz)], "#a8582c", 1.2, 0.7)
    return d


def draw_shack_side(d, dl, notes=None):
    """What leans against the sunny side of the shack: a ladder, a gas bottle, two old tires."""
    Wd = SHACK_W
    d.tube(Wd + 26, 34, 15, 0, 96, ("#8a8aa0", "#dcdcdc", "#ffffff"), n=6, cap="#e8e8e4")
    d.tube(Wd + 26, 34, 6, 96, 108, ("#6a6a78", "#a8a8b0", "#e8e8e4"), n=3)
    for zz in (206, 236):                                              # the ladder
        d.line([(Wd + 46, 0, zz), (Wd + 2, 232, zz)], "#c9a070", 4.5)
    for i in range(1, 8):
        t = i / 8.0
        d.line([(Wd + 46 - 44 * t, 232 * t, 206), (Wd + 46 - 44 * t, 232 * t, 236)], "#a8845c", 3.5)
    return d


# ---------------------------------------------------------------- the old sign on its pole, and the mail box
SIGN_AT = (-731.0, 706.0)
MAIL_AT = (-589.0, 797.0)


def draw_signpole(d, dl, notes=None):
    """What is left of the gas station's sign: a tin disc on a tall pipe, hanging by one good chain and
    one bad one, with GAS painted out and two newer boards wired on underneath."""
    d.tube(0, 0, 6.5, 0, 604, ("#5a566c", "#9a96a4", "#e8dcd0"), n=4)
    d.tube(0, 0, 14, 0, 10, ("#5a5560", "#8c8690", "#c8beb8"), n=5, cap="#a09aa0")
    d.line([(0, 590, 0), (148, 590, 0)], "#8a8694", 6.0)
    dl.line([(0, 592.5, 0), (148, 592.5, 0)], "#f0e6da", 1.4, 0.8)
    d.line([(0, 536, 0), (104, 588, 0)], "#7a7684", 4.0)
    # the disc, swung a little out of true
    cx, cy, r, tilt = 78.0, 508.0, 60.0, math.radians(-7)
    ring = lambda rr, n=30: [(cx + math.cos(a) * rr, cy + math.sin(a) * rr, 0) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]
    for hx in (cx - 34, cx + 30):
        dl.line([(hx + 4, 588, 0), (hx, cy + 47, 0)], "#4a4650", 1.6, 0.9)
    d.poly(ring(r), "#b8503c")
    d.poly(ring(r - 6), "#ecdfc2")
    d.poly([(cx - 52, cy - 22, 0), (cx - 20, cy - 50, 0), (cx + 8, cy - 54, 0), (cx - 26, cy - 18, 0)], "#c98a5c", 0.75)          # rust coming through from the rim
    d.poly([(cx + 30, cy + 44, 0), (cx + 50, cy + 22, 0), (cx + 38, cy + 12, 0), (cx + 18, cy + 40, 0)], "#d8a070", 0.6)
    d.poly([(cx - 58, cy - 6, 0), (cx - 40, cy + 40, 0), (cx - 30, cy + 46, 0), (cx - 46, cy - 4, 0)], "#cfc0b0", 0.7)            # and the side away from the sun
    dl.line([(p[0], p[1], 0) for p in ring(r - 1.5, 30)] + [ring(r - 1.5, 30)[0]], "#8a3628", 1.6, 0.6)
    dl.line([(cx + math.cos(a) * (r - 1), cy + math.sin(a) * (r - 1), 0) for a in np.linspace(-0.9, 0.8, 9)], "#ffe8cc", 1.6, 0.9)   # the rim catches the sun
    for (bx_, by_) in ((cx - 18, cy + 30), (cx + 24, cy - 26)):                                                                    # somebody shot at it
        dl.ball(bx_, by_, 0, 3.0, "#2a2028")
        dl.line([(bx_, by_ - 3, 0), (bx_ - 1, by_ - 16, 0)], "#a8623c", 2.0, 0.6)
    say(notes, d, "GAS", (cx, cy - 2, 0), 50.0, "#b4563e", slant=0.12, seed=21, rough=0.5, amount=0.8)
    dl.line([(cx - 44, cy - 24, 0), (cx + 42, cy + 24, 0)], "#2c2c3c", 7.0, 0.9)                                                   # painted out, by hand
    dl.line([(cx - 40, cy - 19, 0), (cx + 38, cy + 23, 0)], "#4a4a60", 2.0, 0.6)
    # two boards wired on below
    y = cy - r - 8
    for words, wd, col, lean, sd in (("ROCKS", 118, "#2f4a7a", 0.02, 23), ("LEMONADE", 150, "#b63a2a", -0.03, 24)):
        x0, x1 = cx - wd / 2 - 4, cx + wd / 2 - 4
        q = [(x0, y - 30 + lean * wd, 0), (x1, y - 30, 0), (x1, y, 0), (x0, y + lean * wd, 0)]
        d.poly(q, "#f1e6c8")
        dl.line(q + [q[0]], "#7a6450", 1.2, 0.8)
        dl.line([(x0 + 14, y + lean * wd, 0), (x0 + 16, y + 9, 0)], "#4a4650", 1.2, 0.9)
        dl.line([(x1 - 14, y, 0), (x1 - 16, y + 9, 0)], "#4a4650", 1.2, 0.9)
        if not d.shade:
            a, b = d.pt(x0, y - 15 + lean * wd, 0), d.pt(x1, y - 15, 0)
            say(notes, d, words, ((x0 + x1) / 2, y - 14.5 + lean * wd / 2, 0), 21.0, col, slant=-(b[1] - a[1]) / (b[0] - a[0]), seed=sd)
        y -= 39
    return d


def draw_mailbox(d, dl, notes=None):
    """A country mail box on a post that gave up standing straight years ago."""
    top = (-15.0, 102.0, 0.0)
    d.line([(0, 0, 0), top], "#9a8a7a", 9.0)
    dl.line([(3.2, 0, 0), (top[0] + 3.2, top[1], 0)], "#f4e4c8", 2.2, 0.85)
    dl.line([(-3.6, 0, 0), (top[0] - 3.6, top[1], 0)], "#5a4e58", 1.6, 0.6)
    lean = math.radians(8)
    ca, sa = math.cos(lean), math.sin(lean)
    at = lambda u, v, z=0.0: (top[0] + u * ca - v * sa, top[1] + u * sa + v * ca, z)                   # the box leans with its post
    d.poly([at(-30, 0, 9), at(22, 0, 9), at(22, 16, 9), at(16, 22, 9), at(-24, 22, 9), at(-30, 16, 9)], "#8a90a0")
    d.poly([at(-30, 0, -9), at(22, 0, -9), at(22, 14, -9), at(17, 21, -9), at(8, 23.5, -9), at(-16, 23.5, -9), at(-25, 21, -9), at(-30, 14, -9)], "#b4bac6")
    d.poly([at(-25, 21, -9), at(-16, 23.5, -9), at(8, 23.5, -9), at(17, 21, -9), at(17, 21, 9), at(-25, 21, 9)], "#e8ecf0")
    d.poly([at(22, 0, -9), at(22, 14, -9), at(17, 21, -9), at(17, 21, 9), at(22, 14, 9), at(22, 0, 9)], "#f6f4ee")
    dl.line([at(-30, 0, -9), at(22, 0, -9)], "#4a4e5c", 1.2, 0.7)
    dl.line([at(-16, 23.5, -9), at(8, 23.5, -9)], "#ffffff", 1.2, 0.9)
    dl.poly([at(-33, -3, -9.5), at(-28, 0, -9.5), at(-28, 14, -9.5), at(-36, 9, -9.5)], "#9aa0ae")     # its door hangs open
    dl.line([at(2, 6, -10), at(2, 13, -10)], "#5a5e6c", 1.6)                                           # the flag is down
    dl.poly([at(2, 4, -10.5), at(15, 3, -10.5), at(15, 9, -10.5), at(2, 9.5, -10.5)], "#c8402f")
    return d


# ---------------------------------------------------------------- the government's fence
FENCE_C = (489.9, 973.5)                                    # the corner post
A_DIR, A_OUT = (0.9510, -0.3093), (-0.3093, -0.9510)        # one side runs to the right and a little toward us ...
B_DIR, B_OUT = (0.1961, 0.9806), (-0.9806, 0.1961)          # ... the other straight away across the desert
FENCE_H, POST_GAP = 240.0, 300.0
A_POSTS = [0.0, 300.0, 600.0]
B_POSTS = [POST_GAP * i for i in range(1, 60)]
NOTICE = (40.0, 180.0, 70.0, 170.0)                         # on the first panel of side A: from, to (cm along), bottom, top
STEEL = ("#6c7088", "#aab0be", "#f2f0ea")
RUTS = (35.0, 185.0)                                        # where the two wheel tracks pass under side A (cm along it)


def fworld(leg, s, out=0.0):
    d, o = (A_DIR, A_OUT) if leg == "A" else (B_DIR, B_OUT)
    return FENCE_C[0] + d[0] * s + o[0] * out, FENCE_C[1] + d[1] * s + o[1] * out


def fpt(leg, s, h=0.0, out=0.0):
    x, z = fworld(leg, s, out)
    return CAM.pt(x, h, z)


def _mesh(sheet, leg, s0, s1, color, alpha):
    """Chain link between two posts: two sets of slanting wires. Far off they are drawn wider apart, so the
    mesh thins to a veil instead of clotting."""
    k = kz(fworld(leg, (s0 + s1) / 2)[1])
    gap = min(max(4.4 / k, 9.0), 80.0)
    top, bot = FENCE_H - 4, 7.0
    span = top - bot
    c = s0 - span
    while c < s1:
        for up in (True, False):
            a0, a1 = max(c, s0), min(c + span, s1)
            if a1 > a0:
                h0, h1 = (bot + a0 - c, bot + a1 - c) if up else (top - (a0 - c), top - (a1 - c))
                sheet.line([fpt(leg, a0, h0), fpt(leg, a1, h1)], color, 0.34, alpha)
        c += gap


def draw_fence(sheet, notes=None):
    """Chain link on steel posts with three strands of barbed wire, put up yesterday in a hurry."""
    # ---- the side that runs away to the horizon, farthest first
    far = [sp for sp in B_POSTS if fpt("B", sp)[1] > HZ + 3.0]
    for i in range(len(far) - 1, -1, -1):
        sp = far[i]
        prev = far[i - 1] if i > 0 else 0.0
        k = kz(fworld("B", sp)[1])
        if k > 0.16:
            _mesh(sheet, "B", prev, sp, "#6a7088", 0.55)
        else:
            sheet.poly([fpt("B", prev, 6), fpt("B", sp, 6), fpt("B", sp, FENCE_H), fpt("B", prev, FENCE_H)], "#8a8ea4", 0.16)
        sheet.line([fpt("B", prev, FENCE_H), fpt("B", sp, FENCE_H)], STEEL[1], max(0.5, 4.5 * k), 0.9)
        sheet.line([fpt("B", prev, 7), fpt("B", sp, 7)], STEEL[0], max(0.4, 2.0 * k), 0.6)
        for j, (hh, oo) in enumerate(((252, 12), (263, 23), (274, 34))):
            sheet.line([fpt("B", prev, hh, oo), fpt("B", (prev + sp) / 2, hh - 3, oo), fpt("B", sp, hh, oo)], "#4c5066", max(0.34, 1.6 * k), 0.75)
        post(sheet, "B", sp, k)
    # ---- the corner, and the side that runs to the right
    for i in range(len(A_POSTS) - 1):
        s0, s1 = A_POSTS[i], A_POSTS[i + 1]
        _mesh(sheet, "A", s0, s1, "#646a82", 0.6)
        k = kz(fworld("A", (s0 + s1) / 2)[1])
        sheet.line([fpt("A", s0, FENCE_H), fpt("A", s1, FENCE_H)], STEEL[1], 4.5 * k, 0.95)
        sheet.line([fpt("A", s0, FENCE_H + 2.2), fpt("A", s1, FENCE_H + 2.2)], STEEL[2], 1.3 * k, 0.8)
        low = []                                                                          # the wire along the foot: where the ruts run under, there is a gap a child could get through
        for t in np.linspace(0, 1, 25):
            ss = s0 + (s1 - s0) * t
            lift = max(0.0, 1 - abs(ss - RUTS[0]) / 26.0, 1 - abs(ss - RUTS[1]) / 26.0) if i == 0 else 0.0
            low.append(fpt("A", ss, 6 + 5 * lift))
            if lift > 0.6:
                gx_, gy_ = fpt("A", ss, 0, 2)
                sheet.ellipse(gx_, gy_ - 0.3, 3.0, 1.3, "#5a4648", 0.5)
        sheet.line(low, STEEL[0], 2.0 * k, 0.8)
        for j, (hh, oo) in enumerate(((252, 12), (263, 23), (274, 34))):
            pts = [fpt("A", s0 + (s1 - s0) * t, hh - 4 * math.sin(math.pi * t), oo) for t in np.linspace(0, 1, 9)]
            sheet.line(pts, "#464a60", 1.7 * k, 0.85)
            for t in np.linspace(0.04, 0.96, 22):                                       # the barbs
                bx, by = fpt("A", s0 + (s1 - s0) * t, hh - 4 * math.sin(math.pi * t), oo)
                sheet.line([(bx - 1.0, by - 1.1), (bx + 1.0, by + 1.1)], "#e8e8f0" if int(t * 50) % 2 else "#34384c", 0.5, 0.9)
    # a diagonal brace at the corner, each way
    kc = kz(FENCE_C[1])
    sheet.line([fpt("A", 0, FENCE_H * 0.55), fpt("A", 150, 8)], STEEL[1], 4.0 * kc, 0.9)
    sheet.line([fpt("B", 0, FENCE_H * 0.55), fpt("B", 150, 8)], STEEL[0], 3.5 * kc, 0.9)
    for sp in A_POSTS:
        post(sheet, "A", sp, kz(fworld("A", sp)[1]), corner=(sp == 0.0))
    # ---- the notice, wired to the mesh
    n0, n1, nb, nt = NOTICE
    q = [fpt("A", n0, nb, 2), fpt("A", n1, nb, 2), fpt("A", n1, nt, 2), fpt("A", n0, nt, 2)]
    sheet.poly([(x - 1.6, y + 1.2) for x, y in q], "#4a4a60", 0.5)
    sheet.poly(q, "#f6f1e4")
    band = nt - 30.0
    sheet.poly([fpt("A", n0, band, 2), fpt("A", n1, band, 2), fpt("A", n1, nt, 2), fpt("A", n0, nt, 2)], "#c8402f")
    sheet.line(q + [q[0]], "#8a8e9c", 0.8, 0.9)
    cx, cy = fpt("A", n0 + 24, band - 30, 2)                                              # the yellow disc with the black blades
    kn = kz(fworld("A", (n0 + n1) / 2)[1])
    sheet.ellipse(cx, cy, 17 * kn, 17 * kn, "#f2c230")
    for a in (90, 210, 330):
        sheet.line([(cx, cy), (cx + math.cos(math.radians(a)) * 13 * kn, cy - math.sin(math.radians(a)) * 13 * kn)], "#1f130a", 7.5 * kn, 1.0, round_ends=False)
    sheet.ellipse(cx, cy, 3.4 * kn, 3.4 * kn, "#f2c230")
    sheet.ellipse(cx, cy, 1.9 * kn, 1.9 * kn, "#1f130a")
    for i, (hh, x0, x1, col, wd) in enumerate(((band - 14, 50, 132, "#1f130a", 5.5), (band - 26, 50, 122, "#1f130a", 5.5), (band - 40, 50, 132, "#1f130a", 4.0),
                                                 (band - 52, 12, 128, "#c8402f", 5.0), (band - 62, 22, 118, "#1f130a", 2.6))):       # lines of small print
        a, b = fpt("A", n0 + x0, hh, 2.2), fpt("A", n0 + x1, hh, 2.2)
        n = max(2, int((x1 - x0) / 13))
        for j in range(n):                                                                    # broken into words
            t0, t1 = j / n + 0.02, (j + 1) / n - 0.035 - 0.03 * ((i + j) % 3)
            sheet.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], col, wd * kn, 0.9, round_ends=False)
    for (ss, hh) in ((n0 + 5, nt - 5), (n1 - 5, nt - 5), (n0 + 5, nb + 5), (n1 - 5, nb + 5)):
        c = fpt("A", ss, hh, 2.4)
        sheet.ellipse(c[0], c[1], 0.9, 0.9, "#5a5e6c")
    if notes is not None:
        a, b = fpt("A", n0, nt - 15, 2.4), fpt("A", n1, nt - 15, 2.4)
        notes.append(dict(words="AREA CLOSED", at=((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.3), size=20.5 * kn, color="#fff8ea", hand=False, anchor="mm",
                          slant=-(b[1] - a[1]) / (b[0] - a[0]), rough=0.0, amount=1.0, seed=0, spacing=0.35, squash=1.0))
    return sheet


def post(sheet, leg, s, k, corner=False):
    """One post: new grey steel, a dark collar of concrete not yet dry, an arm on top leaning out for the wire."""
    x, z = fworld(leg, s)
    d = Solid(sheet, (x, z))
    r = 5.0 if corner else 3.6
    if k > 0.12:
        d.hdisc(0, 0.5, 0, 21 if corner else 17, "#6c6468", 0.92, rz=15 if corner else 13)
        d.hdisc(1.5, 0.8, -1, 13, "#857c80", 0.7, rz=9)
    d.tube(0, 0, r, 0, FENCE_H + 4, STEEL, n=3 if k < 0.3 else 4)
    o = A_OUT if leg == "A" else B_OUT
    sheet.line([CAM.pt(x, FENCE_H, z), CAM.pt(x + o[0] * 36, FENCE_H + 36, z + o[1] * 36)], STEEL[1], max(0.5, 3.0 * k), 0.95)
    if corner:
        o2 = B_OUT
        sheet.line([CAM.pt(x, FENCE_H, z), CAM.pt(x + o2[0] * 36, FENCE_H + 36, z + o2[1] * 36)], STEEL[0], max(0.5, 3.0 * k), 0.95)
        sheet.ellipse(*CAM.pt(x, FENCE_H + 6, z), 5.5 * k, 3.0 * k, STEEL[2])


def fence_shadow(shape):
    """What the fence throws on the ground: a ladder. Each post is a rung, the top rail is the far side of
    it, and the mesh between is a thin veil. -> (mask of the solid parts, mask of the veil)."""
    hard, veil = Paper(shape), Paper(shape)

    def down(leg, s, h):                                                                   # where a point on the fence throws its shadow
        x, z = fworld(leg, s)
        return CAM.pt(x + SUN[0] * h, 0.0, z + SUN[1] * h)
    for leg, posts in (("B", [0.0] + B_POSTS[:26]), ("A", A_POSTS)):
        for i, sp in enumerate(posts):
            k = kz(fworld(leg, sp)[1])
            hard.line([fpt(leg, sp), down(leg, sp, FENCE_H)], "#000000", max(0.5, 7.0 * k * 0.55))
            if i:
                prev = posts[i - 1]
                hard.line([down(leg, prev, FENCE_H), down(leg, sp, FENCE_H)], "#000000", max(0.4, 4.0 * k * 0.5))
                veil.poly([fpt(leg, prev), fpt(leg, sp), down(leg, sp, FENCE_H), down(leg, prev, FENCE_H)], "#000000")
    n0, n1, nb, nt = NOTICE
    hard.poly([down("A", n0, nb), down("A", n1, nb), down("A", n1, nt), down("A", n0, nt)], "#000000")
    return blur(hard.done()[1], 0.6), blur(veil.done()[1], 0.8)


# ---------------------------------------------------------------- at the very front: an oil drum
DRUM_AT = (392.0, -44.0)


def draw_drum(d, dl, notes=None):
    """A rusty oil drum, its lid long gone, standing where somebody left it when the gas ran out."""
    r, h = 29.0, 88.0
    tones = ("#4a2a2c", "#a5563a", "#e89a66")
    d.tube(0, 0, r, 0, h, tones, n=12)
    for yy in (h * 0.34, h * 0.67):                                    # the two hoops pressed into it
        d.tube(0, 0, r + 1.4, yy - 1.6, yy + 1.6, ("#3a2024", "#8a4630", "#f4b480"), n=12)
    d.tube(0, 0, r + 1.2, h - 2.5, h, ("#3a2024", "#94503a", "#f8be8c"), n=12)
    d.hdisc(0, h, 0, r, "#f2c090")
    d.hdisc(0, h - 0.5, 0, r - 2.6, "#2a1a1e")                          # we look down into it: dark, and a rim of light
    d.poly(d.hring(0, h - 0.5, 0, r - 2.6, n=20, a0=200, a1=340) + d.hring(0, h - 14, 0, r - 2.6, n=20, a0=340, a1=200), "#6a3a30", 0.9)
    # what weather and time have done to its paint: a band of old blue-green, mostly gone to rust
    d.tube(0, 0, r + 0.3, h * 0.39, h * 0.62, ("#34484c", "#5c8484", "#a8ccc0"), n=12, alpha=0.6)
    k = d.k
    c = d.pt(0, h * 0.5, 0)
    for (ux, uy, rw, rh, col, al) in [(-0.45, 0.02, 0.30, 0.10, "#7a3c2c", 0.85), (0.30, -0.06, 0.22, 0.07, "#b86a44", 0.8), (0.05, 0.08, 0.16, 0.05, "#5c2c26", 0.8),
                                      (-0.05, -0.36, 0.5, 0.05, "#6a3028", 0.6), (0.55, 0.30, 0.2, 0.08, "#d08a58", 0.5)]:
        d.s.ellipse(c[0] + ux * r * k, c[1] - uy * h * k, rw * r * k, rh * h * k, col, al)
    dl.line([(r * 0.62, 4, -r * 0.78), (r * 0.62, h - 3, -r * 0.78)], "#ffd0a0", 1.4, 0.55)       # the edge toward the sun
    dl.line([(-r * 0.2, h * 0.67, -r), (-r * 0.26, h * 0.34, -r)], "#3a2024", 1.2, 0.5)           # a dent
    for (hx, hy) in ((-8, 60), (6, 44), (12, 70)):                                                # somebody has used it for target practice
        c2 = dl.pt(hx, hy, -r)
        dl.s.ellipse(c2[0], c2[1], 2.2 * k, 2.2 * k, "#1a1014")
        dl.s.ellipse(c2[0] + 0.8 * k, c2[1] + 0.8 * k, 1.0 * k, 1.0 * k, "#f8c090")
    return d


# ---------------------------------------------------------------- a quick look at each thing, enlarged
if __name__ == "__main__":
    import sys
    from PIL import Image
    shape = (H, W)
    bg = np.empty(shape + (3,), dtype=F32)
    bg[...] = rgb("#e2bf98")
    what = sys.argv[1] if len(sys.argv) > 1 else "stand"
    jobs = {"stand": (draw_stand, STAND_AT, 0.0, 0.0), "pump": (draw_pump, PUMP_AT, 0.0, ISLAND[4]), "car": (draw_car, CAR_AT, 0.0, 0.0), "drum": (draw_drum, DRUM_AT, 0.0, 0.0),
            "shack": (draw_shack, SHACK_AT, SHACK_YAW, 0.0), "side": (draw_shack_side, SHACK_AT, SHACK_YAW, 0.0), "sign": (draw_signpole, SIGN_AT, 0.0, 0.0), "mail": (draw_mailbox, MAIL_AT, 0.0, 0.0)}
    names = list(jobs) if what == "all" else [what]
    box = None
    for name in names:
        draw, at, yaw, lift = jobs[name]
        sh = shade_of(shape, draw, at, yaw, lift=lift)
        tint(bg, SHADOW, sh * 0.5)
        c, a, lc, la = render(shape, draw, at, yaw, lift=lift)
        pc, pa = brushed(c, a, lc, la, "#e2bf98", fast="fast" in sys.argv)
        over(bg, pc, (pa > 0.5).astype(F32))
        ys, xs = np.where(np.maximum(pa, sh) > 0.3)
        b = (xs.min(), ys.min(), xs.max(), ys.max())
        box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
    x0, y0, x1, y1 = max(box[0] - 10, 0), max(box[1] - 10, 0), min(box[2] + 10, W), min(box[3] + 10, H)
    im = Image.fromarray((np.clip(bg[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8))
    z = 3 if (x1 - x0) < 300 else 2
    im.resize(((x1 - x0) * z, (y1 - y0) * z), Image.NEAREST).save(f"out/nevada-roadside-prop-{what}.png")
    print(what, (x0, y0, x1, y1))

"""The flat things of the landing, each painted face-on in its own centimetres (home_landing_kit.Tex) and
then laid on its wall, floor or ceiling through the room's one camera: doors, Dad's notice, the tall
window and the night in it, photographs, the mirror, the attic hatch, the rug, and what hangs on the
walls of the living room below."""

import math

import numpy as np
from PIL import Image

from brush import F32, blur, lerp, noise, ramp, rgb, smooth, step
from home_landing_kit import GLYPHS, Tex, scribble, width_of

INK = "#1c2140"                     # Dad's felt-tip
NOTICE = ["TRIP HEADQUARTERS", "AUTHORIZED PERSONNEL ONLY", "LOST YOUR KEY? IT IS WITH", "THE OTHER EIGHTY-EIGHT.", "- THE MANAGEMENT"]


# ---------------------------------------------------------------- doors
def door(kind="plain", leaf="#e7dec9", casing="#ece4d2", open_=False):
    """A six-panel door (85 x 205) in its casing (10 cm all round): 105 x 216. The knob is on the right."""
    t = Tex(105, 216, res=4, color=None)
    t.rect(0, 0, 105, 216, casing)
    t.line([(2.6, 0), (2.6, 213.4), (102.4, 213.4), (102.4, 0)], "#b9ae96", 0.7)
    t.line([(7.6, 0), (7.6, 208.2), (97.4, 208.2), (97.4, 0)], "#a2977e", 0.8)
    t.line([(5.2, 0), (5.2, 210.8), (99.8, 210.8), (99.8, 0)], "#f8f2e4", 0.9)
    if open_:
        t.rect(10, 0, 95, 205, "#000000")
        from PIL import ImageDraw
        t.da.polygon([t._p(10, 0), t._p(95, 0), t._p(95, 205), t._p(10, 205)], fill=0)
        return t
    t.rect(10, 0, 95, 205, leaf)
    t.line([(10.3, 0), (10.3, 204.7), (94.7, 204.7), (94.7, 0)], "#5d533f", 0.8)
    for x0, x1 in ((17, 49), (56, 88)):
        for y0, y1 in ((12, 62), (74, 146), (158, 196)):
            t.rect(x0, y0, x1, y1, "#d9cdb5")
            t.rect(x0 + 4.5, y0 + 4.5, x1 - 4.5, y1 - 4.5, "#e3d9c3")
            t.line([(x0, y0), (x0, y1), (x1, y1)], "#8f846c", 0.9)
            t.line([(x0, y0), (x1, y0), (x1, y1)], "#f7f0e0", 0.8)
            t.line([(x0 + 4.5, y0 + 4.5), (x1 - 4.5, y0 + 4.5), (x1 - 4.5, y1 - 4.5)], "#a79c84", 0.6)
            t.line([(x0 + 4.5, y0 + 4.5), (x0 + 4.5, y1 - 4.5), (x1 - 4.5, y1 - 4.5)], "#f7f0e0", 0.6)
    for hy in (26, 178):                                   # hinges
        t.rect(10.2, hy, 12.4, hy + 9, "#9a7a3a")
    t.ellipse(88.6, 99, 4.4, 4.4, "#7c5c26")              # the knob and its rose
    t.ellipse(88.6, 99, 3.1, 3.1, "#c79c44")
    t.ellipse(87.7, 100, 1.2, 1.2, "#f8e6a8")
    t.rect(87.6, 87, 89.6, 92, "#4a3a1c")                 # keyhole
    return t


def keep_out(t):
    """The sign's first words (the picture as first delivered, and as round two left it)."""
    t.write("KEEP", 53.5, 158.5, 18.0, "#16131a", weight=0.2, wide=0.72, gap=0.22, anchor="m", seed=3, wobble=0.07)
    t.write("OUT", 53.5, 135.0, 18.0, "#b3281e", weight=0.21, wide=0.78, gap=0.24, anchor="m", seed=4, wobble=0.07)


# ---- round three (briefs/PAINT-3.md, B): the same card now says NO GIRLS ALLOWED, in a ten-year-old's best capitals.
# The card is 75 x 54 cm and a little crooked (its bottom edge falls 4 cm to the right), and on the landing it is
# only about 37 x 32 px, so the words are as big as the card allows and black, the ink that reads best on yellow in
# the dim end of the landing; only NO, the shout, is in his red. The alarm's wire comes up out of its box and runs up
# over the card's lower right corner to the contact on the frame (it is drawn after the card): the stem of the D of
# ALLOWED is drawn right under it, so that the wire disappears into the D instead of cutting a letter in two.
KID_INK, KID_RED = "#16131a", "#b3281e"
CARD_ANGLE = math.atan2(129.3 - 133.0, 88.6 - 17.0)        # the card's red border, along its bottom edge: -2.96 degrees
CARD_AT = (17.0, 133.0)                                     # that border's bottom left corner (the middle of its line)
KID_WIDTH = {"I": 0.25, "L": 0.78, "E": 0.78, "W": 1.42, "D": 0.94, "N": 1.12, "O": 1.08}     # each letter's width, as a part of an ordinary one


def card_pt(s, n):
    """A place on the Son's card: `s` cm along its bottom border from its left end, `n` cm up from it -> door cm."""
    ca, sa = math.cos(CARD_ANGLE), math.sin(CARD_ANGLE)
    return (CARD_AT[0] + s * ca - n * sa, CARD_AT[1] + s * sa + n * ca)


def card_s(u, v):
    """Door cm -> (s, n) on the card (the inverse of card_pt)."""
    ca, sa = math.cos(CARD_ANGLE), math.sin(CARD_ANGLE)
    du, dv = u - CARD_AT[0], v - CARD_AT[1]
    return (du * ca + dv * sa, -du * sa + dv * ca)


def kid_word(t, word, s0, n0, cap, color, width, gap, weight, seed, wobble=0.05, at=None):
    """One word in block capitals along the card (its baseline from (s0, n0), `width` an ordinary letter's width in
    cm, `gap` the space between letters), each letter a little off its line as a boy's hand leaves it. `at` may
    fix where one letter's left stroke stands: {index: s}. -> the s where each letter starts."""
    rng = np.random.default_rng(seed)
    starts, s = [], s0
    for i, ch in enumerate(word):
        if at and i in at:
            s = at[i]
        w = width * KID_WIDTH.get(ch, 1.0)
        dn = rng.normal(0, wobble) * cap * 0.5                    # a little above or below the line
        lean = rng.normal(0, wobble) * 0.5                        # and leaning a little
        c = cap * (1.0 + rng.normal(0, wobble * 0.3))
        starts.append(s)
        for st in GLYPHS[ch]:
            pts = []
            for gx, gy in st:
                if ch == "I":                                     # a boy's I: one stroke, no bars
                    if gx != 2:
                        continue
                    px = s + w / 2
                else:
                    px = s + gx / 4 * w
                hy = (6 - gy) / 6 * c
                pts.append(card_pt(px + lean * hy, n0 + hy + dn))
            if len(pts) >= 2:
                t.line(pts, color, cap * weight, solid=False)
        s += w + gap
    return starts


WIRE = ((80.5, 119.0), (81.0, 150.0))        # the alarm's wire where it runs up over the card (as sons_door draws it)


def wire_s(n):
    """Where the wire crosses the card's line `n` cm up from its bottom border: the s there."""
    (u0, v0), (u1, v1) = WIRE
    s = 63.0
    for _ in range(12):
        u, v = card_pt(s, n)
        s = card_s(u0 + (u1 - u0) * (v - v0) / (v1 - v0), v)[0]
    return s


def no_girls_allowed(t, cap=(11.6, 11.2, 11.2), width=(9.8, 6.6, 6.4), gap=(5.6, 4.4, 4.1), weight=(0.27, 0.19, 0.19),
                     base=(35.3, 19.0, 3.1), red=(True, False, False), d_at=None):
    """NO / GIRLS / ALLOWED, three lines on the Son's card. The D of ALLOWED stands with its stem under the wire."""
    if d_at is None:                                              # the wire, halfway up the line of ALLOWED
        d_at = wire_s(base[2] + cap[2] / 2)
    out = {}
    for k, word in enumerate(("NO", "GIRLS", "ALLOWED")):
        w = sum(width[k] * KID_WIDTH.get(ch, 1.0) for ch in word) + gap[k] * (len(word) - 1)
        if word == "ALLOWED":                                     # ending with the D's stem on the wire, the rest to its left
            s0 = d_at - (w - width[k] * KID_WIDTH["D"])
            at = {6: d_at}
        else:
            s0, at = 35.0 - w / 2, None
        out[word] = kid_word(t, word, s0, base[k], cap[k], KID_RED if red[k] else KID_INK, width[k], gap[k], weight[k], seed=60 + k, at=at)
    return out


LETTERING = {"KEEP OUT": keep_out, "NO GIRLS ALLOWED": no_girls_allowed}


def sons_door(sign="KEEP OUT"):
    """Covered in a boy's notices: a home-made sign (KEEP OUT; from round three NO GIRLS ALLOWED), warning tape,
    drawings, and his alarm by the handle."""
    t = door()
    rng = np.random.default_rng(5)
    # warning tape, corner to corner under the sign
    for a, b in (((10, 58), (95, 112)), ((10, 120), (95, 70))):
        (ax, ay), (bx, by) = a, b
        n = 15
        for i in range(n):
            f0, f1 = i / n, (i + 1) / n
            p0, p1 = (lerp(ax, bx, f0), lerp(ay, by, f0)), (lerp(ax, bx, f1), lerp(ay, by, f1))
            t.poly([(p0[0], p0[1] - 4), (p1[0], p1[1] - 4), (p1[0], p1[1] + 4), (p0[0], p0[1] + 4)], "#e9c832" if i % 2 else "#1c1a1e")
    # the sign: a sheet of yellow card, a little crooked
    t.poly([(15, 131), (90, 127), (91.5, 181), (16.5, 185)], "#f2d23a")
    t.poly([(15, 131), (90, 127), (90.2, 129.5), (15.2, 133.5)], "#c79f22")
    t.line([(17, 133), (88.6, 129.3), (89.8, 179), (18.3, 182.8), (17, 133)], "#b3281e", 1.6, solid=False)
    LETTERING[sign](t)
    # other notices and drawings
    t.poly([(14, 189), (38, 190.5), (37.4, 203.6), (13.4, 202.4)], "#202028")           # a black flag with a white skull, more or less
    t.ellipse(26, 197, 3.6, 3.2, "#e9e6dc", solid=False)
    t.line([(20.5, 193), (31.5, 200.6)], "#e9e6dc", 1.1, solid=False)
    t.line([(20.5, 200.6), (31.5, 193)], "#e9e6dc", 1.1, solid=False)
    t.poly([(60, 187.5), (88, 186), (88.8, 203.4), (60.6, 204.4)], "#dfe8f2")           # a rocket, in felt-tip
    t.poly([(70, 189.5), (78, 189.5), (78, 198), (74, 202.8), (70, 198)], "#d0463a", solid=False)
    t.poly([(67, 189.5), (70, 189.5), (70, 193.5)], "#3f6fb0", solid=False)
    t.poly([(81, 189.5), (78, 189.5), (78, 193.5)], "#3f6fb0", solid=False)
    t.poly([(13.5, 76), (36, 78), (35, 100), (12.5, 98)], "#cfe6c2")                    # a list of rules
    for k in range(5):
        scribble(t, 15.5, 33.5, 80.5 + k * 3.6, 1.9, "#2a3a2a", seed=20 + k, weight=0.3)
    t.poly([(16, 22), (44, 20), (45, 44), (17, 46)], "#f4efe2")                         # a map of somewhere, with an X
    t.line([(20, 27), (27, 37), (34, 30), (41, 40)], "#4a7ab0", 1.0, solid=False)
    t.line([(36, 24), (40, 28)], "#c8322a", 1.2, solid=False)
    t.line([(40, 24), (36, 28)], "#c8322a", 1.2, solid=False)
    t.ellipse(72, 34, 9, 9, "#d8362c")                                                  # a red disc with a white bar: no entry
    t.rect(65.5, 32.3, 78.5, 35.7, "#f4efe2", solid=False)
    for k in range(9):                                                                  # stars and stickers
        sx, sy = 14 + rng.random() * 76, 8 + rng.random() * 112
        t.ellipse(sx, sy, 1.6, 1.6, ["#f2d23a", "#4a8ad0", "#d8362c", "#5aa85a"][k % 4], solid=False)
    # the alarm: a small grey box with a keypad, a wire to a contact on the frame
    t.line([(80.5, 119), (81, 150), (96, 150), (99, 150)], "#3a3a44", 0.8, solid=False)
    t.rect(96.5, 146, 101.5, 154, "#dcdad2")
    t.rect(69, 104, 82.5, 122, "#5c6270")
    t.rect(69, 120.6, 82.5, 122, "#8a909c")
    t.rect(70.6, 115.6, 80.9, 119.6, "#22282c")                                         # its little window
    for r in range(3):
        for c in range(3):
            t.rect(70.9 + c * 3.5, 105.6 + r * 3.2, 73.3 + c * 3.5, 107.9 + r * 3.2, "#d6d8dc")
    t.ellipse(80.6, 113.9, 0.9, 0.9, "#5a1612")                                         # its lamp (the game lights it)
    return t


def girls_door():
    """Two name-plates with no names: one tidy, one buried in stickers."""
    t = door()
    rng = np.random.default_rng(9)
    # Big Sister's: a white card in a dark blue frame, ruled, exact, dead level
    t.rect(22, 166, 62, 181, "#27305a")
    t.rect(23.6, 167.6, 60.4, 179.4, "#f3efe4")
    t.line([(27, 172), (57, 172)], "#27305a", 0.7, solid=False)
    t.line([(27, 175.4), (57, 175.4)], "#9aa2c4", 0.4, solid=False)
    t.rect(25.4, 169.4, 27.4, 171.4, "#27305a")
    # Little Sister's: pink, crooked, and stickers on it, round it and wandering off down the door
    t.poly([(36, 142), (78, 146.5), (76.6, 160), (34.6, 155.4)], "#f09ab8")
    t.poly([(38, 144.4), (76, 148.4), (75, 157.8), (37, 153.6)], "#fbe3ea")
    cols = ["#f2d23a", "#e2463c", "#4aa0e0", "#62b65e", "#f08a2e", "#b06ad0", "#f2d23a", "#ffffff", "#e2463c"]
    for k in range(34):
        a = rng.random() * math.tau
        r = rng.random() ** 0.6 * 30
        sx, sy = 56 + math.cos(a) * r * 1.15, 150 + math.sin(a) * r * 0.9 - (8 if k % 3 == 0 else 0)
        if not (12 < sx < 93 and 70 < sy < 200):
            continue
        s = 1.5 + rng.random() * 1.6
        if k % 3 == 0:
            t.poly([(sx, sy + s * 1.3), (sx + s * 0.4, sy + s * 0.4), (sx + s * 1.3, sy + s * 0.3), (sx + s * 0.6, sy - s * 0.3), (sx + s * 0.8, sy - s * 1.2), (sx, sy - s * 0.7),
                    (sx - s * 0.8, sy - s * 1.2), (sx - s * 0.6, sy - s * 0.3), (sx - s * 1.3, sy + s * 0.3), (sx - s * 0.4, sy + s * 0.4)], cols[k % len(cols)], solid=False)
        else:
            t.ellipse(sx, sy, s, s, cols[k % len(cols)], solid=False)
    for k in range(7):                                    # a trail of them down toward a seven-year-old's reach
        t.ellipse(40 + rng.random() * 34, 86 + k * 8 + rng.random() * 4, 1.8, 1.8, cols[(k * 2) % len(cols)], solid=False)
    # a drawing taped on at her height: a house, a sun
    t.poly([(20, 84), (45, 82.6), (46, 104), (21, 105.6)], "#f6f2e6")
    t.line([(25, 88), (25, 96), (33, 101), (41, 96), (41, 88), (25, 88)], "#c8463a", 1.0, solid=False)
    t.ellipse(41.6, 101.4, 2.2, 2.2, "#f0b82a", solid=False)
    t.line([(22, 86.6), (44, 85.6)], "#4a9a4a", 1.2, solid=False)
    return t


def sticker_chicken(t, x, y, s, kind=0):
    """One chicken sticker, about 2s cm across: a round body, a head, a comb, a beak. kind: 0 a yellow chick,
    1 a white hen, 2 a brown hen, 3 a rooster with a tail."""
    body, head = [("#f4d23c", "#f7dc5c"), ("#f6f2e8", "#ffffff"), ("#a8642c", "#bb7636"), ("#c8482c", "#d8683c")][kind % 4]
    if kind % 4 == 3:
        t.poly([(x - s * 0.5, y + s * 0.2), (x - s * 1.7, y + s * 1.3), (x - s * 1.3, y + s * 0.2), (x - s * 1.8, y + s * 0.5), (x - s * 1.1, y - s * 0.4)], "#2f5a46", solid=False)
    t.ellipse(x, y, s, s * 0.82, body, solid=False)
    t.ellipse(x + s * 0.72, y + s * 0.7, s * 0.52, s * 0.52, head, solid=False)
    if kind % 4:
        t.ellipse(x + s * 0.72, y + s * 1.28, s * 0.34, s * 0.3, "#d8261e", solid=False)       # the comb
    t.poly([(x + s * 1.18, y + s * 0.86), (x + s * 1.72, y + s * 0.62), (x + s * 1.18, y + s * 0.46)], "#ee8a1c", solid=False)
    t.ellipse(x + s * 0.86, y + s * 0.82, max(0.3, s * 0.12), max(0.3, s * 0.12), "#1a1410", solid=False)


def lilsis_door():
    """Little Sister's door, hers alone now: one name-plate buried in chicken stickers, her crayon drawing of a hen
    taped up where she can reach, and her own sign, which has to be read: BEWARE OF CHICKENS."""
    t = door()
    rng = np.random.default_rng(12)
    # ---- the name-plate (no name can be seen: the chickens have it), up where the old plates were
    t.poly([(27, 174.5), (77, 176.5), (76.4, 191), (26.4, 189)], "#f09ab8")
    t.poly([(29, 176.6), (75, 178.4), (74.6, 188.8), (28.6, 187)], "#fbe3ea")
    spots = [(30, 180, 0), (37, 186, 1), (44, 179, 2), (50, 185, 0), (57, 180, 1), (64, 186, 3), (71, 180, 0), (46, 191, 1), (60, 191, 0), (33, 190, 2), (72, 189, 1),
             (24, 184, 0), (80, 184, 2), (38, 173, 1), (55, 173, 0), (68, 174, 3), (22, 194, 1), (84, 193, 0), (40, 197, 0), (63, 198, 2), (18, 176, 0), (88, 177, 1)]
    for sx, sy, kind in spots:
        sticker_chicken(t, sx + rng.normal(0, 0.5), sy + rng.normal(0, 0.5), 2.3 + rng.random() * 0.7, kind)
    # ---- her sign: a sheet of yellow sugar paper, a little crooked, in her best capitals with a fat crayon
    w, h, x0, y0 = 75.0, 52.0, 15.0, 116.0
    t.poly([(x0, y0 + 0.8), (x0 + w, y0 - 0.9), (x0 + w + 0.8, y0 + h - 0.6), (x0 + 0.6, y0 + h + 1.0)], "#f7ecae")
    t.line([(x0 + 1.6, y0 + 2.2), (x0 + w - 1.2, y0 + 0.8), (x0 + w - 0.6, y0 + h - 2.2), (x0 + 2.0, y0 + h - 0.8), (x0 + 1.6, y0 + 2.2)], "#e08a1c", 1.3, solid=False)
    for cx, cy, a in ((x0 + 3.5, y0 + h - 1.2, 0.5), (x0 + w - 3.2, y0 + h - 2.6, -0.5), (x0 + 3.0, y0 + 1.6, -0.45), (x0 + w - 3.0, y0 + 0.4, 0.5)):
        ca, sa = math.cos(a), math.sin(a)
        t.poly([(cx + (ex * ca - ey * sa), cy + (ex * sa + ey * ca)) for ex, ey in ((-4.2, -1.4), (4.2, -1.4), (4.2, 1.4), (-4.2, 1.4))], "#d9c693")
    mid = x0 + w / 2 + 0.5
    t.write("BEWARE", mid, y0 + 33.6, 13.6, "#b81f1a", weight=0.2, wide=0.56, gap=0.19, anchor="m", seed=31, wobble=0.07)
    t.write("OF", mid, y0 + 21.8, 8.4, "#2b2d52", weight=0.24, wide=0.62, gap=0.26, anchor="m", seed=32, wobble=0.08)
    t.write("CHICKENS", mid, y0 + 4.6, 13.6, "#23202c", weight=0.2, wide=0.50, gap=0.165, anchor="m", seed=33, wobble=0.07)
    # ---- her drawing, taped on at her own height: a hen, an egg, the sun
    px, py, pw, ph = 21.0, 60.0, 40.0, 44.0
    t.poly([(px, py + 1), (px + pw, py - 0.8), (px + pw + 1, py + ph), (px + 0.6, py + ph + 1.4)], "#f8f5ea")
    t.poly([(px + pw / 2 - 5, py + ph - 0.6), (px + pw / 2 + 5, py + ph - 0.8), (px + pw / 2 + 5, py + ph + 2.6), (px + pw / 2 - 5, py + ph + 2.8)], "#d9c693")
    for k in range(7):                                    # grass
        gx = px + 3 + k * 5.4
        t.line([(gx, py + 3), (gx + 1.2, py + 7.5), (gx + 2.6, py + 3.2)], "#4f9a42", 1.2, solid=False)
    hx, hy = px + 17.0, py + 20.0
    t.poly([(hx - 9, hy + 3), (hx - 17, hy + 12), (hx - 13, hy + 2), (hx - 18, hy + 5), (hx - 12, hy - 2)], "#8a4a22", solid=False)       # her tail
    t.ellipse(hx, hy, 10.5, 8.2, "#c8742c", solid=False)                                                           # her body
    t.ellipse(hx - 2, hy - 0.5, 5.2, 3.6, "#a85a1e", solid=False)                                                  # a wing
    t.ellipse(hx + 8.5, hy + 8.5, 5.0, 5.0, "#d8843a", solid=False)                                                # her head
    for k in range(3):                                                                                             # the comb
        t.ellipse(hx + 6.2 + k * 2.4, hy + 13.8 + (0.9 if k == 1 else 0), 1.7, 1.9, "#d8261e", solid=False)
    t.ellipse(hx + 11.0, hy + 4.6, 1.5, 2.2, "#d8261e", solid=False)                                               # her wattle
    t.poly([(hx + 13.0, hy + 9.8), (hx + 18.4, hy + 8.0), (hx + 13.0, hy + 6.4)], "#f0a21c", solid=False)          # her beak
    t.ellipse(hx + 9.6, hy + 9.6, 0.9, 0.9, "#1a1410", solid=False)
    for lx in (hx - 3.0, hx + 3.0):                                                                                # legs and feet
        t.line([(lx, hy - 7.6), (lx, hy - 15.0)], "#f0a21c", 1.1, solid=False)
        t.line([(lx - 2.6, hy - 16.6), (lx, hy - 15.0), (lx + 2.6, hy - 16.6)], "#f0a21c", 1.0, solid=False)
    t.ellipse(px + pw - 7.5, py + 7.5, 3.2, 4.0, "#fbf7ee", solid=False)                                           # the egg
    t.line([(px + pw - 10.6, py + 4.4), (px + pw - 4.2, py + 4.2)], "#b9b3a0", 0.6, solid=False)
    t.ellipse(px + pw - 7.0, py + ph - 8.0, 4.0, 4.0, "#f6c81e", solid=False)                                      # the sun
    for k in range(8):
        a = k / 8 * math.tau
        t.line([(px + pw - 7.0 + math.cos(a) * 5.2, py + ph - 8.0 + math.sin(a) * 5.2), (px + pw - 7.0 + math.cos(a) * 7.4, py + ph - 8.0 + math.sin(a) * 7.4)], "#f6c81e", 0.8, solid=False)
    # ---- and a few more chickens walking down the door, as far as a seven-year-old can reach
    for k, (sx, sy, kind) in enumerate(((70, 104, 0), (76, 92, 1), (68, 80, 0), (75, 66, 2), (66, 52, 0), (74, 40, 1), (30, 48, 0), (44, 40, 3))):
        sticker_chicken(t, sx + rng.normal(0, 0.8), sy + rng.normal(0, 0.8), 2.5 + rng.random() * 0.6, kind)
    return t


BEWARE = (15.0, 116.0, 91.0, 169.0)        # where her sign is on that painting (x0, y0, x1, y1), for keeping its letters crisp


def retreat_card():
    """The card Big Sister has hung on the attic ladder, in a thirteen-year-old's best lettering: 50 x 29 cm."""
    w, h = 50.0, 29.0
    t = Tex(w, h, res=12, color="#f4eedd")
    t.line([(1.3, 1.3), (1.3, h - 1.3), (w - 1.3, h - 1.3), (w - 1.3, 1.3), (1.3, 1.3)], "#2b3160", 0.75, solid=False)
    t.write("THE", w / 2, 17.4, 8.6, "#232a5c", weight=0.17, wide=0.56, gap=0.24, anchor="m", seed=41, wobble=0.012)
    t.write("RETREAT", w / 2, 4.2, 9.6, "#232a5c", weight=0.17, wide=0.50, gap=0.175, anchor="m", seed=42, wobble=0.012)
    for hx in (w / 2 - 14.0, w / 2 + 14.0):               # two punched holes for its ribbon
        t.ellipse(hx, h - 2.6, 0.9, 0.9, "#6a5a48")
    return t


def hatch_trim(w=76.0, d=78.0, m=6.0):
    """The white frame round the open hatch, on the ceiling: only the frame is painted, the hole is the hole."""
    t = Tex(w + 2 * m, d + 2 * m, res=4, color=None)
    t.frame(0, 0, w + 2 * m, d + 2 * m, m, "#e4dccb")
    t.line([(m, m), (m, d + m), (w + m, d + m), (w + m, m), (m, m)], "#5a4a34", 1.4)
    t.line([(0.5, 0.5), (0.5, d + 2 * m - 0.5), (w + 2 * m - 0.5, d + 2 * m - 0.5), (w + 2 * m - 0.5, 0.5), (0.5, 0.5)], "#8a7f68", 1.0)
    return t


def notice():
    """Dad's notice: a big sheet of chart paper taped across the study door, in his block capitals."""
    w, h = 78.0, 64.0
    t = Tex(w, h, res=10, color="#f3ecd8")
    t.poly([(0, 0), (w, 0), (w, 1.2), (0, 1.6)], "#d9cfb6")
    for cx, cy, a in ((3.4, h - 2.6, 0.5), (w - 3.4, h - 2.8, -0.45), (3.2, 2.8, -0.5), (w - 3.4, 2.6, 0.55)):       # masking tape at the corners
        ca, sa = math.cos(a), math.sin(a)
        t.poly([(cx + (ex * ca - ey * sa), cy + (ex * sa + ey * ca)) for ex, ey in ((-4.5, -1.5), (4.5, -1.5), (4.5, 1.5), (-4.5, 1.5))], "#d6c391")
    t.write(NOTICE[0], w / 2, 46.6, 11.2, INK, weight=0.17, wide=0.298, gap=0.114, anchor="m", seed=1, wobble=0.025)
    t.line([(6, 43.2), (w - 6, 43.6)], INK, 0.8, solid=False)
    for s, y in zip(NOTICE[1:], (33.6, 25.2, 16.8, 7.2)):
        t.write(s, w / 2, y, 5.1, INK, weight=0.2, wide=0.36, gap=0.16, anchor="m", seed=5, wobble=0.03)
    return t


# ---------------------------------------------------------------- the tall window and the night in it
def night(w=160.0, h=270.0, res=3.0, seed=4):
    """The night seen through the stair window: a painted sky with moonlit cloud, the moon, the black tree.
    -> (color h x w x 3, branches mask) with the room side's left at column 0."""
    W_, H_ = int(w * res), int(h * res)
    yy, xx = np.mgrid[0:H_, 0:W_].astype(F32)
    u, v = xx / W_, yy / H_                                   # v: 0 at the top
    sky = ramp(v, [(0.0, "#0a1232"), (0.35, "#12205a"), (0.7, "#1f3a7c"), (1.0, "#3a5c94")])
    mx, my, mr = 0.60 * W_, 0.20 * H_, 10.5 * res
    d = np.hypot(xx - mx, yy - my)
    sky += (np.exp(-(d / (mr * 5.0)) ** 2) * 0.22)[..., None] * rgb("#9fc0ff")          # the moon's breath on the sky
    cl = noise((H_, W_), (150, 46), seed, 4)
    body = step(0.52, 0.72, cl + 0.10 * np.exp(-((v - 0.42) / 0.3) ** 2))
    lit = step(0.50, 0.9, cl) * np.exp(-(d / (W_ * 0.9)) ** 2)
    cloud = lerp(rgb("#23346a"), rgb("#8fa6d6"), lit[..., None])
    sky = lerp(sky, cloud, (body * 0.8)[..., None])
    rng = np.random.default_rng(seed)
    for _ in range(46):                                      # stars, where the cloud lets them through
        sx, sy = int(rng.random() * W_), int(rng.random() ** 1.5 * H_ * 0.8)
        if body[sy, sx] < 0.25:
            b = 0.5 + rng.random() * 0.5
            sky[max(0, sy - 1):sy + 1, max(0, sx - 1):sx + 1] = lerp(sky[sy, sx], rgb("#e8f0ff"), b)
    moon = np.clip((mr - d) / 1.5 + 0.5, 0, 1)
    face = lerp(rgb("#fbf6dc"), rgb("#d6d9c8"), step(0.45, 0.62, noise((H_, W_), 22, seed + 3, 3))[..., None])
    sky = lerp(sky, face, moon[..., None])
    # far roofs and a neighbour's lit window, low down
    roofs = (yy > H_ * (0.93 - 0.035 * (noise((H_, W_), (90, 400), seed + 5, 2) > 0.5) - 0.02 * np.sin(xx / 37.0)))
    sky[roofs] = rgb("#0b1020")
    sky[int(H_ * 0.955):int(H_ * 0.972), int(W_ * 0.30):int(W_ * 0.335)] = rgb("#f2c05a")
    # the tree: a trunk up the far side and branches reaching across the moon
    im = Image.new("L", (W_, H_), 0)
    from PIL import ImageDraw
    dr = ImageDraw.Draw(im)

    def limb(x, y, ang, length, wide, depth):
        n = 6
        px, py = x, y
        for i in range(n):
            a = ang + rng.normal(0, 0.16)
            nx, ny = px + math.cos(a) * length / n, py - math.sin(a) * length / n
            dr.line([px, py, nx, ny], fill=255, width=max(1, int(wide * (1 - 0.6 * i / n))))
            px, py = nx, ny
            if depth > 0 and i in (2, 4):
                limb(px, py, a + rng.choice([-1, 1]) * (0.5 + rng.random() * 0.5), length * 0.55, wide * 0.5, depth - 1)
        if depth > 0:
            limb(px, py, ang + rng.normal(0, 0.4), length * 0.6, wide * 0.45, depth - 1)
    limb(W_ * 0.24, H_ * 1.02, math.radians(86), H_ * 0.62, 9 * res, 3)
    limb(W_ * 0.26, H_ * 0.62, math.radians(40), W_ * 0.8, 4.2 * res, 3)
    limb(W_ * 0.25, H_ * 0.42, math.radians(24), W_ * 0.85, 3.4 * res, 3)
    limb(W_ * 0.24, H_ * 0.80, math.radians(14), W_ * 0.7, 3.0 * res, 2)
    limb(W_ * 0.25, H_ * 0.52, math.radians(150), W_ * 0.3, 2.6 * res, 2)
    limb(W_ * 1.02, H_ * 0.74, math.radians(152), W_ * 0.4, 2.6 * res, 2)
    tree = np.asarray(im, dtype=F32) / 255
    sky = lerp(sky, rgb("#070a16"), tree[..., None])
    return np.clip(sky, 0, 1).astype(F32), tree


def curtains():
    """Long curtains at the stair window, tied back: 204 cm of wall wide (the window and 22 cm each side), 312 high.
    Only the cloth and the rod are painted; the rest is clear."""
    w, h = 204.0, 312.0
    t = Tex(w, h, res=3, color=None)
    cloth, fold, deep, lit = "#9e803d", "#bb9a50", "#6a5426", "#d8c07a"
    for side in (0, 1):
        def X(x):
            return x if side == 0 else w - x
        outer, tie_y = 5.0, 76.0
        shape = [(outer, 6), (outer, 300), (44, 300), (43, 240), (39, 170), (30, 110), (20, tie_y + 4), (20, tie_y - 4), (24, 50), (27, 24), (28, 6)]
        t.poly([(X(x), y) for x, y in shape], cloth)
        for k in range(7):                                 # the folds: gathered at the rod, drawn in at the tie, then falling straight
            f = k / 6
            top = lerp(outer + 2, 42, f)
            mid = lerp(outer + 1.5, 19, f)
            bot = lerp(outer + 2, 27.5, f)
            c = fold if k % 2 else deep
            t.line([(X(top), 299), (X(lerp(top, mid, 0.5)), 190), (X(mid), tie_y + 3)], c, 1.5 if k % 2 else 1.1, solid=False)
            t.line([(X(mid), tie_y - 3), (X(lerp(mid, bot, 0.5)), 42), (X(bot), 8)], c, 1.5 if k % 2 else 1.1, solid=False)
        t.line([(X(43.5), 298), (X(42.5), 240), (X(38.5), 170), (X(29.5), 110), (X(20), tie_y + 4)], lit, 1.0, solid=False)      # the edge the moon finds
        t.line([(X(20.5), tie_y - 4), (X(24.5), 50), (X(27.5), 24), (X(28.5), 8)], lit, 0.9, solid=False)
        t.poly([(X(outer - 1), tie_y - 4.5), (X(21.5), tie_y - 3.5), (X(21.5), tie_y + 3.5), (X(outer - 1), tie_y + 4.5)], "#b8963e")    # the tie-back
        t.poly([(X(outer), 6), (X(29), 6), (X(29.6), 2.5), (X(outer), 3)], deep)
    t.rect(0, 301.5, w, 305.5, "#5c3420")                                                   # the pole, its rings and its knobs
    t.line([(0, 304.6), (w, 304.6)], "#8a5a38", 0.9, solid=False)
    for k in range(8):
        for side in (0, 1):
            x = 6 + k * 5.2
            t.ellipse(x if side == 0 else w - x, 301.5, 1.9, 2.4, "#c9a24c")
    for x in (1.5, w - 1.5):
        t.ellipse(x, 303.5, 3.4, 3.4, "#5c3420")
    return t


def window(glass):
    """-> (the casing and glazing bars as a painting with the panes cut out, the panes of night)."""
    w, h, m = 160.0, 270.0, 11.0
    res = glass.shape[1] / w
    t = Tex(w + 2 * m, h + 2 * m, res=res, color=None)
    t.rect(0, 0, w + 2 * m, h + 2 * m, "#e9e1cf")
    t.line([(3, 3), (3, h + 2 * m - 3), (w + 2 * m - 3, h + 2 * m - 3), (w + 2 * m - 3, 3), (3, 3)], "#b5aa92", 0.9)
    t.rect(-3, -1, w + 2 * m + 3, 5.5, "#f1ead9")                                         # the sill
    t.line([(0, 5.6), (w + 2 * m, 5.6)], "#8f856e", 0.8)
    frame = t.array()
    H_, W_ = glass.shape[:2]
    pane = np.zeros((H_, W_), dtype=F32)
    yy, xx = np.mgrid[0:H_, 0:W_].astype(F32)
    u, v = (W_ - 1 - xx) / W_, (H_ - 1 - yy) / H_           # as the light sees it: u along Z from z0, v up
    ok = (u > 0.035) & (u < 0.965) & (v > 0.02) & (v < 0.98)
    cu = np.abs(u * 3 - np.round(u * 3)) * w / 3
    cv = np.abs(v * 5 - np.round(v * 5)) * h / 5
    pane[ok & (cu > 2.2) & (cv > 2.2)] = 1.0
    # put the sash (white bars) into the frame painting where the glass is not
    fh, fw = frame.shape[:2]
    y0, x0 = int(round(m * res)), int(round(m * res))
    inner = frame[y0:y0 + H_, x0:x0 + W_]
    bars = np.empty((H_, W_, 4), dtype=F32)
    bars[..., :3] = rgb("#e4dcc9")
    bars[..., 3] = 1.0
    edge = blur(pane, 1.2)
    bars[..., :3] = lerp(bars[..., :3], rgb("#9c937c"), (np.clip(edge * 2.2, 0, 1) * (1 - pane))[..., None] * 0.6)
    inner[...] = bars
    inner[..., 3] = 1.0 - pane
    night_rgba = np.dstack([glass, pane]).astype(F32)
    return frame, night_rgba


# ---------------------------------------------------------------- photographs (blobs of the right colors, nobody's face)
def photograph(t, x0, y0, x1, y1, frame, kind, seed=0, mat="#efe8d8"):
    rng = np.random.default_rng(seed)
    fw = max(1.4, (x1 - x0) * 0.09)
    t.rect(x0, y0, x1, y1, frame)
    t.line([(x0, y0), (x1, y0), (x1, y1)], "#1e140c", 0.5)
    t.rect(x0 + fw, y0 + fw, x1 - fw, y1 - fw, mat)
    mw = fw * 0.9
    a0, b0, a1, b1 = x0 + fw + mw, y0 + fw + mw, x1 - fw - mw, y1 - fw - mw
    grounds = {"group": ("#7fa07a", "#a9c0d6"), "car": ("#c9b48a", "#9cc0e0"), "kids": ("#8aa46a", "#bcd2e2"), "wedding": ("#6d7f6a", "#cfd6d2"),
               "baby": ("#d8c8a8", "#e6dccb"), "sea": ("#d8c79a", "#7fb4d8"), "old": ("#8a7a66", "#b8a890")}
    g, s = grounds[kind]
    t.rect(a0, b0, a1, b1, s)
    t.rect(a0, b0, a1, b0 + (b1 - b0) * 0.42, g)
    cx, w, h = (a0 + a1) / 2, a1 - a0, b1 - b0

    def person(px, tall, shirt, hair="#4a3222"):
        r = tall * 0.13
        t.poly([(px - r * 1.3, b0), (px + r * 1.3, b0), (px + r * 1.1, b0 + tall * 0.72), (px - r * 1.1, b0 + tall * 0.72)], shirt)
        t.ellipse(px, b0 + tall * 0.84, r, r * 1.12, "#e3b590")
        t.poly([(px - r, b0 + tall * 0.88), (px + r, b0 + tall * 0.88), (px + r * 0.8, b0 + tall), (px - r * 0.8, b0 + tall)], hair)
    if kind == "group":
        for k, (dx, tall, shirt, hair) in enumerate(((-0.30, 0.86, "#3c5a8a", "#3a2a1c"), (-0.08, 0.80, "#2f8a66", "#6a4426"), (0.12, 0.62, "#c8463a", "#4a3222"), (0.28, 0.70, "#5a56b0", "#7a4a2a"), (0.40, 0.44, "#f08ab0", "#e0c060"))):
            person(cx + dx * w, h * tall, shirt, hair)
    elif kind == "car":
        t.poly([(a0 + w * 0.12, b0 + h * 0.2), (a0 + w * 0.88, b0 + h * 0.2), (a0 + w * 0.88, b0 + h * 0.42), (a0 + w * 0.7, b0 + h * 0.44), (a0 + w * 0.62, b0 + h * 0.62), (a0 + w * 0.3, b0 + h * 0.62), (a0 + w * 0.22, b0 + h * 0.44), (a0 + w * 0.12, b0 + h * 0.4)], "#c8463a")
        t.rect(a0 + w * 0.2, b0 + h * 0.24, a0 + w * 0.8, b0 + h * 0.34, "#b98a52")
        for wx in (0.28, 0.72):
            t.ellipse(a0 + w * wx, b0 + h * 0.2, w * 0.07, w * 0.07, "#22201e")
    elif kind == "kids":
        person(cx - w * 0.2, h * 0.7, "#5a56b0", "#7a4a2a")
        person(cx + w * 0.05, h * 0.6, "#c8463a")
        person(cx + w * 0.27, h * 0.46, "#f6e27a", "#e0c060")
    elif kind == "wedding":
        person(cx - w * 0.14, h * 0.86, "#26262e", "#3a2a1c")
        person(cx + w * 0.14, h * 0.80, "#f4f0e6", "#6a4426")
    elif kind == "baby":
        t.ellipse(cx, b0 + h * 0.45, w * 0.3, h * 0.28, "#f4f0e6")
        t.ellipse(cx, b0 + h * 0.62, w * 0.14, h * 0.14, "#e3b590")
    elif kind == "sea":
        t.rect(a0, b0 + h * 0.42, a1, b0 + h * 0.6, "#3f86b8")
        person(cx - w * 0.1, h * 0.5, "#e0823a")
        person(cx + w * 0.16, h * 0.4, "#f08ab0", "#e0c060")
    else:
        person(cx - w * 0.14, h * 0.8, "#4a4238", "#2a221c")
        person(cx + w * 0.14, h * 0.76, "#6a6052", "#8a8274")
    t.line([(a0, b1), (a1 - (a1 - a0) * 0.35, b0)], "#ffffff", 0.5, alpha=0.18, solid=False)       # glass


def landing_photos():
    """The family's photographs between the Son's door and the girls': 100 x 80 cm of wall."""
    t = Tex(100, 80, res=6, color=None)
    photograph(t, 3, 40, 37, 78, "#4a2e1a", "group", 1)
    photograph(t, 41, 50, 69, 76, "#b08a3a", "car", 2)
    photograph(t, 73, 42, 97, 77, "#1e1a18", "kids", 3)
    photograph(t, 8, 6, 33, 34, "#e9e2d2", "baby", 4, mat="#d9d0bc")
    photograph(t, 38, 10, 68, 44, "#6a3a22", "wedding", 5)
    photograph(t, 72, 8, 96, 36, "#8a6a34", "sea", 6)
    return t


def stair_photos(z0=415.0, z1=600.0, y0=130.0, y1=416.0, pitch=0.7125, foot=575.0, step=17.8):
    """Photographs climbing the stair wall of the living room, as that room hangs them: each about 118 cm above
    the woodwork, which climbs with the steps. The painting covers the wall from Z = z1 (its left edge, by the foot
    of the stairs) to Z = z0, and from y0 to y1 above the living-room floor."""
    w, h = z1 - z0, y1 - y0
    t = Tex(w, h, res=4, color=None)
    kinds = [("old", "#3a2416", 22, 28, 0), ("group", "#8a6a34", 30, 24, 16), ("sea", "#1e1a18", 22, 26, -2), ("kids", "#5a3a22", 26, 30, 20),
             ("wedding", "#e2dac8", 22, 28, 2), ("car", "#6a3a22", 28, 22, 24), ("baby", "#b08a3a", 20, 24, 6)]
    n = len(kinds)
    for k, (kind, fr, fw, fh, up) in enumerate(kinds):
        zc = z1 - 12.0 - k * (w - 26.0) / (n - 1)           # the middle of this frame along the wall
        base = min(max((foot - zc) * pitch + step, 0.0), 285.0)
        x0 = (z1 - zc) - fw / 2
        b0 = base + 118.0 + up - y0
        if 1 < x0 and x0 + fw < w - 1 and 1 < b0 and b0 + fh < h - 1:
            photograph(t, x0, b0, x0 + fw, b0 + fh, fr, kind, 10 + k)
    return t


def landscape(w=96.0, h=70.0, m=8.0):
    """The landscape in a gilt frame that hangs high on the stair wall (the living room's picture has it): hills,
    a lake, an evening sky, one dark pine."""
    t = Tex(w + 2 * m, h + 2 * m, res=4, color="#c29436")
    t.line([(1, 1), (1, h + 2 * m - 1), (w + 2 * m - 1, h + 2 * m - 1), (w + 2 * m - 1, 1), (1, 1)], "#7a5a1c", 1.4)
    t.rect(m - 4, m - 4, w + m + 4, h + m + 4, "#8a6a22")
    t.line([(m - 4, m - 4), (m - 4, h + m + 4), (w + m + 4, h + m + 4)], "#e8c868", 0.9)
    for i in range(12):                                    # the sky: peach low down, blue-green above
        f = i / 11.0
        c = lerp(np.array([0.90, 0.66, 0.42]), np.array([0.30, 0.46, 0.56]), f)
        t.rect(m, m + h * (0.42 + 0.58 * f), m + w, m + h, c)
    t.rect(m, m, m + w, m + h * 0.44, (0.82, 0.62, 0.40))
    t.poly([(m, m + h * 0.42), (m + w * 0.18, m + h * 0.60), (m + w * 0.34, m + h * 0.50), (m + w * 0.52, m + h * 0.70), (m + w * 0.74, m + h * 0.48), (m + w, m + h * 0.58),
            (m + w, m + h * 0.30), (m, m + h * 0.30)], (0.30, 0.34, 0.46))
    t.poly([(m, m + h * 0.36), (m + w * 0.3, m + h * 0.44), (m + w * 0.62, m + h * 0.38), (m + w, m + h * 0.46), (m + w, m + h * 0.2), (m, m + h * 0.2)], (0.18, 0.28, 0.24))
    t.rect(m, m, m + w, m + h * 0.26, (0.50, 0.56, 0.60))                                    # the lake
    t.rect(m + w * 0.2, m + h * 0.14, m + w * 0.7, m + h * 0.17, (0.86, 0.72, 0.56))
    t.poly([(m, m), (m, m + h * 0.20), (m + w * 0.22, m + h * 0.12), (m + w * 0.36, m)], (0.12, 0.18, 0.14))
    t.line([(m + w * 0.84, m + h * 0.10), (m + w * 0.84, m + h * 0.56)], (0.10, 0.12, 0.10), 1.2)        # one dark pine
    t.poly([(m + w * 0.76, m + h * 0.26), (m + w * 0.84, m + h * 0.62), (m + w * 0.92, m + h * 0.26)], (0.10, 0.16, 0.12))
    return t


def chart():
    """The long strip of paper pinned up over the hall table: Dad and the Son's countdown to the trip. A line of
    days, most of them crossed off, and at the end of the line a small red car."""
    w, h = 95.0, 38.0
    t = Tex(w, h, res=8, color="#ddd2b4")
    t.rect(1.5, 1.5, w - 1.5, h - 1.5, "#ece2c6")
    t.line([(5, 15), (w - 5, 15)], "#28325a", 0.9, solid=False)
    for k in range(10):                                    # a tick for every day, and a box over it
        x = 7 + k * 8.2
        t.line([(x, 12), (x, 18)], "#28325a", 0.7, solid=False)
        t.line([(x - 2.6, 20.5), (x + 2.6, 20.5), (x + 2.6, 25.7), (x - 2.6, 25.7), (x - 2.6, 20.5)], "#28325a", 0.45, solid=False)
        if k < 9:                                          # crossed off: every day but the last
            t.line([(x - 2.2, 21), (x + 2.2, 25.2)], "#c8322a", 0.7, solid=False)
            t.line([(x - 2.2, 25.2), (x + 2.2, 21)], "#c8322a", 0.7, solid=False)
    cx = w - 9.5                                           # the car at the end of the line
    t.poly([(cx - 6.5, 17), (cx + 6.5, 17), (cx + 6.5, 21), (cx + 3.5, 21.4), (cx + 2.4, 24.6), (cx - 4.2, 24.6), (cx - 5.2, 21.2), (cx - 6.5, 20.8)], "#c8463a", solid=False)
    for wx in (cx - 3.8, cx + 3.8):
        t.ellipse(wx, 16.8, 1.5, 1.5, "#22201e", solid=False)
    scribble(t, 6, 60, 29.5, 3.2, "#28325a", seed=3, weight=0.2)
    scribble(t, 8, 70, 5.5, 2.0, "#5a5648", seed=4, weight=0.25, alpha=0.8)
    for px_, py_ in ((3, h - 3), (w - 3, h - 3), (3, 3), (w - 3, 3)):
        t.ellipse(px_, py_, 1.1, 1.1, "#c8322a")
    return t


def corner_photos():
    """Two photographs on the short piece of wall between the head of the stairs and the Son's door: 64 x 64 cm."""
    t = Tex(64, 64, res=6, color=None)
    photograph(t, 6, 4, 40, 30, "#4a2e1a", "sea", 21)
    photograph(t, 38, 34, 58, 60, "#b08a3a", "old", 22)
    return t


def hatch():
    """The attic hatch: a square wooden door in the ceiling in a white frame, with a ring for its cord at the
    near edge. (It is seen from far off and almost edge-on, so it is drawn boldly.)"""
    t = Tex(78, 78, res=4, color="#f2ecdc")
    t.rect(0, 0, 78, 78, "#efe8d6")
    t.line([(1, 1), (1, 77), (77, 77), (77, 1), (1, 1)], "#6a5c44", 2.0)
    t.rect(8, 8, 70, 70, "#8f6a40")
    for k in range(1, 5):
        t.line([(8 + k * 12.4, 8), (8 + k * 12.4, 70)], "#5a4026", 1.2)
    t.line([(8, 8), (8, 70), (70, 70), (70, 8), (8, 8)], "#3a2816", 2.4)
    for hx in (20, 58):
        t.rect(hx - 4, 66, hx + 4, 72, "#3a3a40")          # hinges, on the far side
    t.ellipse(39, 12.5, 3.2, 3.2, "#d8c088")
    return t


# ---------------------------------------------------------------- the living room's things
def rug(w=320.0, d=250.0):
    """The big worn rug, as it lies in the living room's own picture: a red field, a navy border with a running
    pattern, cream and gold lines, a great lozenge in the middle and quarter ones in the corners."""
    red, navy, cream, gold = (0.494, 0.124, 0.105), (0.137, 0.189, 0.357), (0.79, 0.727, 0.57), (0.68, 0.51, 0.204)
    t = Tex(w, d, res=2, color=navy)
    t.rect(5, 5, w - 5, d - 5, cream)
    t.rect(8, 8, w - 8, d - 8, navy)
    t.rect(26, 26, w - 26, d - 26, gold)
    t.rect(29, 29, w - 29, d - 29, red)
    n = 15
    for i in range(n):
        for (u, v) in ((26 + (w - 52) * (i + 0.5) / n, 17), (26 + (w - 52) * (i + 0.5) / n, d - 17)):
            t.poly([(u - 7, v), (u, v + 6), (u + 7, v), (u, v - 6)], cream if i % 2 else gold)
            t.poly([(u - 3.5, v), (u, v + 3), (u + 3.5, v), (u, v - 3)], (0.52, 0.13, 0.11))
    m = 11
    for i in range(m):
        for (u, v) in ((17, 26 + (d - 52) * (i + 0.5) / m), (w - 17, 26 + (d - 52) * (i + 0.5) / m)):
            t.poly([(u - 6, v), (u, v + 7), (u + 6, v), (u, v - 7)], cream if i % 2 else gold)
            t.poly([(u - 3, v), (u, v + 3.5), (u + 3, v), (u, v - 3.5)], (0.52, 0.13, 0.11))
    for (u, v) in ((17, 17), (w - 17, 17), (17, d - 17), (w - 17, d - 17)):
        t.rect(u - 6, v - 6, u + 6, v + 6, gold)
        t.rect(u - 3, v - 3, u + 3, v + 3, navy)
    cu, cv = w / 2, d / 2
    for k, c in ((1.0, navy), (0.86, cream), (0.80, (0.17, 0.234, 0.44)), (0.56, gold), (0.50, (0.546, 0.137, 0.116)), (0.26, cream), (0.2, navy)):
        t.poly([(cu - 92 * k, cv), (cu, cv + 66 * k), (cu + 92 * k, cv), (cu, cv - 66 * k)], c)
    for (u, v) in ((29, 29), (w - 29, 29), (29, d - 29), (w - 29, d - 29)):
        su, sv = (1 if u < cu else -1), (1 if v < cv else -1)
        t.poly([(u, v), (u + su * 46, v), (u, v + sv * 34)], navy)
        t.poly([(u, v), (u + su * 36, v), (u, v + sv * 26)], gold)
    a = t.array()
    H_, W_ = a.shape[:2]
    worn = step(0.5, 0.86, noise((H_, W_), 70, 12, 4)) * 0.30       # where five people have walked for years
    a[..., :3] = lerp(a[..., :3], rgb("#a8806a"), worn[..., None])
    a[..., :3] *= (0.93 + 0.14 * noise((H_, W_), 6, 13, 2))[..., None]
    return a


def preamble():
    """The framed print in the living room: a parchment sheet with three large words and close lines under them."""
    t = Tex(44, 62, res=8, color="#4a2e1a")
    t.frame(0, 0, 44, 62, 1.2, "#2a1a0e")
    t.rect(4, 4, 40, 58, "#ded09e")
    t.rect(5.4, 5.4, 38.6, 56.6, "#e6d9aa")
    t.line([(8, 49.4), (10, 53), (12.4, 49.4), (14.4, 53), (16.4, 49.6)], "#2a2016", 1.3, solid=False)        # the three big words, as a pen would sweep them
    t.line([(19, 50), (22.5, 50.4), (22.5, 52.6), (19.5, 52.6), (19.5, 49.6), (23.5, 49.4)], "#2a2016", 1.0, solid=False)
    t.line([(26, 49.6), (26, 53.4), (28.6, 53), (28.6, 51.2), (26, 51.2)], "#2a2016", 1.2, solid=False)
    t.line([(30.4, 49.6), (33, 49.6), (33, 52.4), (30.4, 52.4), (30.4, 49.6), (36.2, 49.4)], "#2a2016", 1.0, solid=False)
    for k in range(13):
        scribble(t, 8, 36.5, 44.6 - k * 2.9, 1.3, "#4a3a26", seed=30 + k, weight=0.3, alpha=0.8)
    return t


def clock():
    """The round wall clock, at twenty to ten."""
    t = Tex(35, 35, res=10, color=None)
    t.ellipse(17.5, 17.5, 17.5, 17.5, "#4a2e1a")
    t.ellipse(17.5, 17.5, 15.6, 15.6, "#7a5230")
    t.ellipse(17.5, 17.5, 14.2, 14.2, "#efe6cf")
    for k in range(12):
        a = math.radians(k * 30)
        r0 = 11.2 if k % 3 else 10.2
        t.line([(17.5 + math.sin(a) * r0, 17.5 + math.cos(a) * r0), (17.5 + math.sin(a) * 13.0, 17.5 + math.cos(a) * 13.0)], "#2a2016", 1.0 if k % 3 else 1.5, solid=False)
    ah, am = math.radians((9 + 40 / 60) * 30), math.radians(240)
    t.line([(17.5, 17.5), (17.5 + math.sin(ah) * 7.4, 17.5 + math.cos(ah) * 7.4)], "#1a1410", 1.7, solid=False)
    t.line([(17.5, 17.5), (17.5 + math.sin(am) * 11.4, 17.5 + math.cos(am) * 11.4)], "#1a1410", 1.2, solid=False)
    t.ellipse(17.5, 17.5, 1.4, 1.4, "#8a6428")
    return t


def front_door():
    """The front door of the house: solid, painted dark green, a brass handle and letter flap. 124 x 224."""
    t = Tex(124, 224, res=3, color="#e7dfcc")
    t.line([(3, 0), (3, 221), (121, 221), (121, 0)], "#b3a890", 0.9)
    t.rect(10, 0, 114, 214, "#85211c")
    t.line([(10.4, 0), (10.4, 213.6), (113.6, 213.6), (113.6, 0)], "#3a0e0c", 1.0)
    for x0, x1 in ((19, 57), (67, 105)):
        for y0, y1 in ((14, 84), (118, 200)):
            t.rect(x0, y0, x1, y1, "#761c18")
            t.line([(x0, y0), (x0, y1), (x1, y1)], "#4a100e", 1.0)
            t.line([(x0, y0), (x1, y0), (x1, y1)], "#a8423a", 0.9)
    for k in range(13):                                    # a fanlight in the head of the door: night in it
        a0, a1 = math.radians(k * 15), math.radians((k + 1) * 15)
        t.poly([(62, 168), (62 + math.cos(a0) * 34, 168 + math.sin(a0) * 30), (62 + math.cos(a1) * 34, 168 + math.sin(a1) * 30)], "#e7dfcc")
    for k in range(12):
        a0, a1 = math.radians(k * 15 + 1), math.radians((k + 1) * 15 - 1)
        if k % 3 == 0:
            a0 += math.radians(1.5)
        t.poly([(62, 170), (62 + math.cos(a0) * 30, 170 + math.sin(a0) * 26), (62 + math.cos(a1) * 30, 170 + math.sin(a1) * 26)], "#1e2c5a")
    for k in (3, 6, 9):
        a0 = math.radians(k * 15)
        t.line([(62, 170), (62 + math.cos(a0) * 30, 170 + math.sin(a0) * 26)], "#e7dfcc", 1.4, solid=False)
    t.rect(44, 95, 80, 104, "#b08a3a")
    t.rect(46, 97, 78, 102, "#6a5220")
    t.ellipse(20, 104, 4.2, 4.2, "#c79c44")
    t.rect(10, 0, 114, 5, "#4a4034")
    return t


def closet_door():
    """The low cupboard door in the panelling under the stairs, ajar the width of a hand: 80 x 108."""
    t = Tex(80, 108, res=4, color="#d3c9b2")
    t.rect(0, 0, 9, 108, "#0c0a10")                                                         # the dark inside, at the edge nearest us
    t.rect(9, 0, 11.4, 108, "#efe8d6")                                                      # the edge of the door, catching light
    t.rect(11.4, 0, 80, 108, "#d9cfb9")
    t.line([(11.4, 0), (11.4, 107.5), (79.5, 107.5), (79.5, 0)], "#6d634e", 1.0)
    t.rect(19, 10, 72, 98, "#cdc2aa")
    t.line([(19, 10), (19, 98), (72, 98)], "#857b64", 0.9)
    t.line([(19, 10), (72, 10), (72, 98)], "#efe8d6", 0.8)
    t.ellipse(16, 56, 2.2, 2.2, "#b08a3a")
    return t


def fridge_drawings(seed=3):
    """Children's drawings held on the fridge with magnets."""
    t = Tex(56, 120, res=3, color="#e9e6da")
    rng = np.random.default_rng(seed)
    t.line([(0, 78), (56, 78)], "#a8a698", 1.0)
    t.rect(3, 84, 6, 110, "#c9c7ba")
    sheets = [((8, 40, 28, 66), "#f6f2e6"), ((30, 34, 52, 58), "#fbe7a8"), ((12, 8, 34, 32), "#dfeaf4"), ((36, 86, 52, 108), "#f6f2e6"), ((14, 88, 30, 106), "#f9d6e0")]
    for (x0, y0, x1, y1), c in sheets:
        t.rect(x0, y0, x1, y1, c)
        for _ in range(4):
            col = ["#d8463a", "#3f78c8", "#4a9a4a", "#f0a82a", "#8a4ab0"][int(rng.integers(0, 5))]
            ax, ay = x0 + 2 + rng.random() * (x1 - x0 - 4), y0 + 2 + rng.random() * (y1 - y0 - 4)
            t.line([(ax, ay), (ax + rng.normal(0, 4), ay + rng.normal(0, 4)), (ax + rng.normal(0, 5), ay + rng.normal(0, 5))], col, 1.3, solid=False)
        t.ellipse((x0 + x1) / 2, y1 - 1.5, 1.6, 1.6, ["#d8463a", "#3f78c8", "#f0a82a"][int(rng.integers(0, 3))])
    return t


def switch():
    t = Tex(9, 13, res=8, color="#ece6d6")
    t.line([(0.3, 0.3), (0.3, 12.7), (8.7, 12.7), (8.7, 0.3), (0.3, 0.3)], "#8f866f", 0.6)
    t.rect(3.4, 4, 5.6, 9, "#cfc8b6")
    t.rect(3.4, 6.6, 5.6, 9, "#f8f4e8")
    return t


def picture(kind="hills"):
    """A small framed picture for the wall at the head of the stairs."""
    t = Tex(46, 38, res=5, color="#5a3a22")
    t.frame(0, 0, 46, 38, 1.0, "#2a1a0e")
    t.rect(4, 4, 42, 34, "#ece4d0")
    t.rect(7, 7, 39, 31, "#a9c6dc")
    t.poly([(7, 7), (39, 7), (39, 15), (30, 19), (22, 14), (14, 18), (7, 13)], "#6f9a62")
    t.poly([(7, 13), (14, 18), (22, 14), (22, 7), (7, 7)], "#587e4e")
    t.ellipse(31, 25, 3, 3, "#f6e9b0")
    t.poly([(18, 12), (21, 12), (21, 16.5), (19.5, 18.5), (18, 16.5)], "#f4f0e6")           # a white church with a little spire
    t.line([(19.5, 18.5), (19.5, 22)], "#f4f0e6", 0.6, solid=False)
    return t

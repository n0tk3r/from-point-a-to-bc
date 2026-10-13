"""Lettering for signs, boards and inscriptions. Words are set with a font, then roughened so they
look painted or cut by hand, and laid down through a mask like any other paint.

Fonts: the game's own Koine Road (fonts/KoineRoad-Regular.ttf) for anything ancient or hand-written,
and the plain face that comes with Pillow for modern signs. No other font files are used."""

import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from brush import F32, blur, over, warp

HERE = os.path.dirname(os.path.abspath(__file__))
KOINE = next((p for p in (os.path.join(HERE, "..", "..", "fonts", "KoineRoad-Regular.ttf"),
                          os.path.join(HERE, "..", "game", "fonts", "KoineRoad-Regular.ttf")) if os.path.exists(p)), None)


def face(size, hand=False):
    if hand and KOINE:
        return ImageFont.truetype(KOINE, int(size))
    return ImageFont.load_default(int(size))


def mask(shape, words, at, size, hand=False, anchor="mm", rough=0.5, spacing=0, slant=0.0, squash=1.0, seed=0, ss=3):
    """Words as a mask the size of the picture. `at` is where the anchor goes ("mm" middle, "lt" left top,
    "ls" left baseline...). `rough` wobbles the edges by that many pixels; `slant` leans the line
    (rise per pixel across, for a sign seen at an angle); `squash` narrows it."""
    h, w = shape
    im = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(im)
    f = face(size * ss, hand)
    if spacing:
        x = at[0] * ss
        total = sum(d.textlength(ch, font=f) + spacing * ss for ch in words) - spacing * ss
        x -= total / 2 if anchor[0] == "m" else (total if anchor[0] == "r" else 0)
        for ch in words:
            d.text((x, at[1] * ss), ch, fill=255, font=f, anchor="l" + anchor[1])
            x += d.textlength(ch, font=f) + spacing * ss
    else:
        d.text((at[0] * ss, at[1] * ss), words, fill=255, font=f, anchor=anchor)
    m = np.asarray(im.resize((w, h), Image.BOX), dtype=F32) / 255
    if slant or squash != 1.0:
        from brush import grid, sample
        x, y = grid(shape)
        m = sample(m, at[0] + (x - at[0]) / squash, y + (x - at[0]) * slant)
    if rough:
        m = warp(m, rough, 5.0, seed)
    return np.clip(m, 0, 1)


def paint(picture, words, at, size, color, amount=0.95, **how):
    """Letter straight onto a picture. Returns the mask used."""
    m = mask(picture.shape[:2], words, at, size, **how)
    over(picture, color, m * amount)
    return m


def carve(picture, words, at, size, dark="#5a4a44", light="#fff6dc", amount=0.8, **how):
    """Letters cut into stone: a dark cut with a lit lower-right edge."""
    m = mask(picture.shape[:2], words, at, size, **how)
    lit = np.roll(np.roll(m, 1, axis=0), 1, axis=1)
    over(picture, light, np.clip(lit - m, 0, 1) * amount * 0.7)
    over(picture, dark, m * amount)
    return m


# ---------------------------------------------------------------- the sign-painter's capitals (round twelve)
# Painted notices on a Roman street were a trade: tall, narrow capitals laid on with a broad brush, so the verticals
# are thick and the horizontals thin, each letter the same height on a straight line, with a little hook where the
# brush landed and left. These are the game's own letters for that (nobody's typeface): each a few strokes in a box
# 60 wide and 140 tall, the baseline at 140. Drawn by roman_mask().
ROMAN = {
    "A": [[(4, 140), (30, 0), (56, 140)], [(13, 96), (47, 96)]],
    "B": [[(8, 0), (8, 140)], [(8, 0), (40, 0), (54, 16), (54, 50), (40, 66), (8, 66)], [(8, 66), (42, 66), (56, 84), (56, 122), (42, 140), (8, 140)]],
    "C": [[(54, 24), (44, 6), (24, 0), (10, 16), (6, 70), (10, 124), (24, 140), (44, 134), (54, 116)]],
    "D": [[(8, 0), (8, 140)], [(8, 0), (36, 0), (54, 20), (58, 70), (54, 120), (36, 140), (8, 140)]],
    "E": [[(54, 0), (8, 0), (8, 140), (54, 140)], [(8, 68), (44, 68)]],
    "F": [[(54, 0), (8, 0), (8, 140)], [(8, 68), (42, 68)]],
    "G": [[(54, 24), (44, 6), (24, 0), (10, 16), (6, 70), (10, 124), (24, 140), (46, 134), (54, 112), (54, 84), (34, 84)]],
    "H": [[(8, 0), (8, 140)], [(52, 0), (52, 140)], [(8, 70), (52, 70)]],
    "I": [[(30, 0), (30, 140)]],
    "J": [[(50, 0), (50, 110), (44, 134), (26, 140), (10, 126)]],
    "K": [[(8, 0), (8, 140)], [(52, 0), (10, 84)], [(24, 66), (56, 140)]],
    "L": [[(8, 0), (8, 140), (54, 140)]],
    "M": [[(6, 140), (6, 0), (30, 100), (54, 0), (54, 140)]],
    "N": [[(8, 140), (8, 0), (52, 140), (52, 0)]],
    "O": [[(30, 0), (12, 10), (5, 70), (12, 130), (30, 140), (48, 130), (55, 70), (48, 10), (30, 0)]],
    "P": [[(8, 140), (8, 0), (42, 0), (56, 18), (56, 52), (42, 70), (8, 70)]],
    "Q": [[(30, 0), (12, 10), (5, 70), (12, 130), (30, 140), (48, 130), (55, 70), (48, 10), (30, 0)], [(36, 112), (58, 146)]],
    "R": [[(8, 140), (8, 0), (42, 0), (56, 18), (56, 52), (42, 68), (8, 68)], [(34, 68), (58, 140)]],
    "S": [[(52, 22), (40, 4), (20, 2), (8, 18), (10, 44), (28, 64), (46, 80), (54, 104), (50, 128), (34, 140), (14, 136), (6, 118)]],
    "T": [[(4, 0), (56, 0)], [(30, 0), (30, 140)]],
    "U": [[(8, 0), (8, 110), (16, 134), (30, 140), (44, 134), (52, 110), (52, 0)]],
    "V": [[(4, 0), (30, 140), (56, 0)]],
    "W": [[(2, 0), (16, 140), (30, 40), (44, 140), (58, 0)]],
    "X": [[(6, 0), (54, 140)], [(54, 0), (6, 140)]],
    "Y": [[(4, 0), (30, 72), (56, 0)], [(30, 72), (30, 140)]],
    "Z": [[(6, 0), (54, 0), (6, 140), (54, 140)]],
    "·": [[(30, 66), (30, 74)]],                                      # the point between words
}
ROMAN_ADVANCE = {"I": 36, "J": 56, "M": 66, "W": 66, "·": 30}


def roman_size(words, cap, spacing=0.30):
    """How wide and high a line of ROMAN capitals is, in pixels: (width, height)."""
    k = cap / 140.0
    adv = lambda ch: (ROMAN_ADVANCE.get(ch, 62) if ch != " " else 36) * k + spacing * cap
    return sum(adv(ch) for ch in words) - spacing * cap, cap


def roman_mask(shape, words, at, cap, anchor="mm", thick=0.17, thin=0.065, tilt=22.0, spacing=0.30, rough=0.22, seed=0, ss=3, hook=True):
    """Words in the sign-painter's capitals (ROMAN) as a mask the size of the picture. `cap` is the letter height in
    pixels; `at` is where the anchor goes, as in mask(); `thick` and `thin` the brush's widest and narrowest stroke as
    a share of `cap`; `tilt` the brush's angle in degrees (which strokes are thick); `spacing` the gap between letters
    as a share of `cap`; `rough` wobbles the edges a little, as a brush does. A space is half a letter."""
    import math
    h, w = shape
    im = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(im)
    k = cap / 140.0
    adv = lambda ch: (ROMAN_ADVANCE.get(ch, 62) if ch != " " else 36) * k + spacing * cap
    total = sum(adv(ch) for ch in words) - spacing * cap
    x0 = at[0] - (total / 2 if anchor[0] == "m" else total if anchor[0] == "r" else 0)
    y0 = at[1] - (cap / 2 if anchor[1] == "m" else cap if anchor[1] in "sb" else 0)
    t = math.radians(tilt)
    wide, narrow = thick * cap, thin * cap

    def width_at(ax, ay, bx, by):
        a = math.atan2(by - ay, bx - ax)
        return narrow + (wide - narrow) * abs(math.sin(a - t)) ** 0.8

    def seg(ax, ay, bx, by, wd):
        a = math.atan2(by - ay, bx - ax)
        nx, ny = -math.sin(a) * wd / 2, math.cos(a) * wd / 2
        d.polygon([(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)], fill=255)
        for px, py in ((ax, ay), (bx, by)):
            d.ellipse([px - wd / 2, py - wd / 2, px + wd / 2, py + wd / 2], fill=255)

    x = x0
    for ch in words:
        if ch == " ":
            x += adv(ch)
            continue
        strokes_ = ROMAN.get(ch.upper())
        if strokes_:
            for pts in strokes_:
                P = [((x + px * k) * ss, (y0 + py * k) * ss) for px, py in pts]
                for (ax, ay), (bx, by) in zip(P, P[1:]):
                    seg(ax, ay, bx, by, width_at(ax, ay, bx, by) * ss)
                if hook and len(pts) >= 2:                                     # where the brush landed and left: a short thin pull along the line
                    for (ax, ay), (bx, by), sgn in (((P[0]), (P[1]), 1), ((P[-1]), (P[-2]), 1)):
                        a = math.atan2(by - ay, bx - ax)
                        hx, hy = ax - math.cos(a + math.pi / 2) * narrow * ss * 1.6, ay - math.sin(a + math.pi / 2) * narrow * ss * 1.6
                        seg(ax, ay, hx, hy, narrow * ss * 0.9)
        x += adv(ch)
    m = np.asarray(im.resize((w, h), Image.BOX), dtype=F32) / 255
    if rough:
        m = warp(m, rough, 4.0, seed)
    return np.clip(m, 0, 1)

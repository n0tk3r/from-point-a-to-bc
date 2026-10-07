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

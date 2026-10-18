"""The Office's lettering (OFFICE-17B): one set of single-stroke capitals, figures and signs, drawn two ways.

  drafting   the draughtsman's lettering on the blueprint (map_office*.py): even, thin strokes, as a lettering guide
             and a technical pen leave them
  stencil    sprayed through a stencil onto sheet metal (office_ducts*.py): thick strokes, broken where a stencil's
             bridges hold its islands in (the O's, the B's), a little overspray round them

The letters are the game's own sign-painter's capitals (letter.ROMAN: a few strokes in a box 60 wide and 140 tall,
the baseline at 140), and the figures and signs added here in the same box: nobody's typeface. Each is laid out in
the box and drawn by `draw()` into a mask the caller gives (a picture's, or a texture laid on a wall)."""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, blur
from letter import ROMAN, ROMAN_ADVANCE

# ---------------------------------------------------------------- the figures and signs, in ROMAN's box (60 x 140)
EXTRA = {
    "0": [[(30, 0), (12, 10), (6, 70), (12, 130), (30, 140), (48, 130), (54, 70), (48, 10), (30, 0)]],
    "1": [[(14, 26), (32, 0), (32, 140)], [(14, 140), (50, 140)]],
    "2": [[(8, 26), (18, 6), (32, 0), (48, 8), (54, 30), (46, 58), (8, 140), (56, 140)]],
    "3": [[(8, 14), (26, 0), (46, 6), (52, 28), (44, 56), (24, 66)], [(24, 66), (46, 76), (54, 104), (46, 132), (26, 140), (6, 128)]],
    "4": [[(42, 140), (42, 0), (4, 100), (58, 100)]],
    "5": [[(52, 0), (12, 0), (8, 60), (28, 54), (46, 62), (54, 92), (48, 128), (28, 140), (8, 130)]],
    "6": [[(48, 8), (30, 0), (12, 14), (6, 70), (10, 122), (28, 140), (46, 130), (54, 100), (46, 74), (28, 68), (8, 82)]],
    "7": [[(6, 0), (56, 0), (24, 140)], [(18, 70), (46, 70)]],
    "8": [[(30, 66), (12, 54), (10, 22), (28, 0), (48, 10), (50, 40), (30, 66), (8, 86), (10, 126), (30, 140), (50, 126), (52, 88), (30, 66)]],
    "9": [[(52, 58), (32, 72), (12, 62), (6, 32), (14, 8), (30, 0), (48, 10), (54, 60), (48, 120), (30, 140), (10, 132)]],
    "&": [[(54, 140), (14, 52), (12, 22), (26, 2), (42, 8), (44, 30), (30, 52), (8, 90), (10, 126), (28, 140), (46, 128), (56, 92)]],
    "-": [[(12, 76), (48, 76)]],
    "·": [[(30, 68), (30, 74)]],
    ".": [[(30, 134), (30, 140)]],
    ",": [[(32, 128), (32, 140), (24, 156)]],
    ":": [[(30, 40), (30, 46)], [(30, 128), (30, 134)]],
    "/": [[(52, 0), (8, 140)]],
    "'": [[(30, 0), (28, 34)]],
    '"': [[(20, 0), (20, 34)], [(40, 0), (40, 34)]],
    "=": [[(10, 52), (50, 52)], [(10, 92), (50, 92)]],
    "#": [[(20, 10), (14, 130)], [(44, 10), (38, 130)], [(4, 46), (56, 46)], [(4, 94), (56, 94)]],
    ">": [[(8, 24), (52, 70), (8, 116)]],
    "→": [[(4, 70), (56, 70)], [(34, 44), (58, 70), (34, 96)]],
    "↑": [[(30, 140), (30, 4)], [(6, 34), (30, 2), (54, 34)]],
    "↓": [[(30, 0), (30, 136)], [(6, 106), (30, 138), (54, 106)]],
}
ADVANCE = dict(ROMAN_ADVANCE)
ADVANCE.update({"1": 52, "·": 30, ".": 28, ",": 28, ":": 28, "'": 24, '"': 36, "-": 52, "→": 70, "↑": 62, "↓": 62})
GLYPHS = dict(ROMAN)
GLYPHS["·"] = EXTRA["·"]
GLYPHS.update(EXTRA)

# where a stencil holds its islands in: (x0, y0, x1, y1) gaps cut through the strokes, in the box's units
BRIDGES = {
    "O": [(26, -10, 34, 14), (26, 126, 34, 150)],
    "0": [(26, -10, 34, 14), (26, 126, 34, 150)],
    "D": [(2, 64, 16, 76)],
    "B": [(2, 26, 16, 36), (2, 100, 16, 110)],
    "P": [(2, 26, 16, 36)],
    "R": [(2, 26, 16, 36)],
    "A": [(26, -12, 34, 10)],
    "&": [(20, 44, 30, 56)],
    "8": [(22, 60, 38, 72)],
    "6": [(2, 90, 14, 100)],
    "9": [(46, 40, 58, 50)],
    "4": [(28, 92, 40, 108)],
}


def advance(ch):
    return 36 if ch == " " else ADVANCE.get(ch, 62)


def width(text, cap, spacing=0.30, stretch=1.0):
    """How wide a line is, in the units `cap` is in."""
    k = cap / 140.0
    return sum(advance(ch) * k * stretch + spacing * cap for ch in text) - spacing * cap


def strokes_of(text, x0, y0, cap, spacing=0.30, stretch=1.0, slant=0.0):
    """Every stroke of a line, laid out: [(points, char)] with the line's top left at (x0, y0) and `cap` the capitals'
    height. `stretch` widens the letters; `slant` leans them (a draughtsman's lettering often leans a little)."""
    k = cap / 140.0
    out = []
    x = x0
    for ch in text:
        g = GLYPHS.get(ch) or GLYPHS.get(ch.upper())
        if g:
            for pts in g:
                out.append(([(x + (px + (140 - py) * slant) * k * stretch, y0 + py * k) for px, py in pts], ch, x))
        x += advance(ch) * k * stretch + spacing * cap
    return out


def draw(d, text, at, cap, width_px, anchor="ls", spacing=0.30, stretch=1.0, slant=0.0, fill=255, ss=1, stencil=False, bridge=None):
    """Draw a line of capitals with an ImageDraw `d` (on a picture `ss` times the size of the coordinates): strokes
    `width_px` wide, round at their ends and joints. `anchor` as Pillow's: "ls" left baseline, "ms" middle baseline,
    "mm" middle, "rs" right baseline, "lt" left top. With `stencil`, the bridges are cut (drawn in `bridge`, the ground)."""
    w = width(text, cap, spacing, stretch)
    x0 = at[0] - (w / 2 if anchor[0] == "m" else (w if anchor[0] == "r" else 0))
    y0 = at[1] - (cap if anchor[1] in "sb" else (cap / 2 if anchor[1] == "m" else 0))
    r = width_px * ss / 2
    for pts, ch, lx in strokes_of(text, x0, y0, cap, spacing, stretch, slant):
        P = [(px * ss, py * ss) for px, py in pts]
        if len(P) == 1 or (len(P) == 2 and P[0] == P[1]):
            d.ellipse([P[0][0] - r, P[0][1] - r, P[0][0] + r, P[0][1] + r], fill=fill)
            continue
        d.line(P, fill=fill, width=max(1, int(round(width_px * ss))), joint="curve")
        for px, py in (P[0], P[-1]):
            d.ellipse([px - r, py - r, px + r, py + r], fill=fill)
    if stencil:
        k = cap / 140.0
        x = x0
        for ch in text:
            for (bx0, by0, bx1, by1) in BRIDGES.get(ch.upper(), []):
                d.rectangle([(x + bx0 * k * stretch) * ss, (y0 + by0 * k) * ss, (x + bx1 * k * stretch) * ss, (y0 + by1 * k) * ss], fill=bridge)
            x += advance(ch) * k * stretch + spacing * cap
    return w


def mask(shape, text, at, cap, width_px, ss=3, **kw):
    """A line of capitals as a float mask the size of `shape` (soft at its edges: drawn `ss` times larger and averaged)."""
    h, w = shape
    im = Image.new("L", (w * ss, h * ss), 0)
    draw(ImageDraw.Draw(im), text, at, cap, width_px, ss=ss, bridge=0, **kw)
    return np.asarray(im.resize((w, h), Image.BOX), dtype=F32) / 255


def stencil_texture(lines, cap, width_cm, size_cm, texel=4.0, spacing=0.34, stretch=1.25, line_gap=1.55, seed=3,
                    align="middle"):
    """A stencil sprayed on a wall, as a texture in the wall's own centimetres: `lines` of capitals `cap` cm high,
    strokes `width_cm` thick, stacked (`line_gap` caps apart), in a panel `size_cm` (w, h) wide and high, centred.
    -> (paint coverage 0..1 as an array, texels a centimetre). The paint is a little uneven and has a soft overspray."""
    W_, H_ = int(round(size_cm[0] * texel)), int(round(size_cm[1] * texel))
    im = Image.new("L", (W_, H_), 0)
    d = ImageDraw.Draw(im)
    n = len(lines)
    top = (size_cm[1] - (cap + (n - 1) * cap * line_gap)) / 2
    for i, t in enumerate(lines):
        y = top + i * cap * line_gap + cap
        if align == "middle":
            draw(d, t, (size_cm[0] / 2 * texel, y * texel), cap * texel, width_cm * texel, anchor="ms", spacing=spacing,
                 stretch=stretch, stencil=True, bridge=0)
        else:
            draw(d, t, (0.0, y * texel), cap * texel, width_cm * texel, anchor="ls", spacing=spacing, stretch=stretch,
                 stencil=True, bridge=0)
    m = np.asarray(im, dtype=F32) / 255
    rng = np.random.default_rng(seed)
    spray = blur(m, 0.9 * texel) * 0.22                                   # the overspray, a soft haze round the strokes
    uneven = 0.78 + 0.22 * blur(rng.random(m.shape).astype(F32), 1.2 * texel) / 0.5
    out = np.clip(np.maximum(m * np.clip(uneven, 0.6, 1.0), spray), 0, 1)
    return out.astype(F32), texel


def sample_texture(tex, texel, u, v, u0, v0):
    """Read a texture laid on a surface: (u, v) in the surface's centimetres, the texture's top left at (u0, v0), v
    running down the texture as it runs down the wall (so pass v as the height measured downward). Bilinear; 0 outside."""
    h, w = tex.shape
    x = (u - u0) * texel - 0.5
    y = (v - v0) * texel - 0.5
    inside = (x >= 0) & (x <= w - 1) & (y >= 0) & (y <= h - 1)
    xc, yc = np.clip(x, 0, w - 1.001), np.clip(y, 0, h - 1.001)
    x0, y0 = np.floor(xc).astype(np.intp), np.floor(yc).astype(np.intp)
    fx, fy = (xc - x0).astype(F32), (yc - y0).astype(F32)
    a = tex[y0, x0] * (1 - fx) + tex[y0, x0 + 1] * fx
    b = tex[y0 + 1, x0] * (1 - fx) + tex[y0 + 1, x0 + 1] * fx
    return np.where(inside, a * (1 - fy) + b * fy, 0).astype(F32)

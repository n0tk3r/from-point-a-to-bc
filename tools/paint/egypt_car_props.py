"""The wagon's small printed and drawn things, as flat pictures in their own centimetres (egypt_car_things.py lays them on
the things they belong to, through the camera, so they lie in perspective and take the car's light):

    the two dials       the speedometer (its needle at 0, the odometer showing 200006) and the fuel and temperature
                        dial (fuel at a quarter, the temperature needle hard in the red, a small red lamp lit)
    the PRNDL strip     between the dials, the pointer at P
    the drawing         Little Sister's crayon drawing, tucked under the driver's visor's strap: five stick people in a
                        row, Dad the biggest in blue, Mom in purple, a green one and a small pink one, a yellow sun, the
                        red car with the white hen on its roof (drawn again for Dad's car: the same subject as the one
                        on her wall at home, not line for line)
    the registration    the car's registration card beside it: printed lines, a stamp; nothing that can be read

All of them are the painter's own: no maker's mark anywhere, no real document's layout, no lettering but the dial's
figures, the odometer's six digits and P R N D L."""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, blur

PPC = 12.0                                                  # picture pixels to a centimetre, as the props are drawn


class Tex:
    """A flat picture laid out in centimetres: `origin` is the centimetre place of its top left corner, `flip` True when
    its centimetres run up (a dial's Y) rather than down the picture. sample(u, v) -> (colour, coverage)."""

    def __init__(self, rgba, origin=(0.0, 0.0), ppc=PPC, flip=False):
        self.rgb = rgba[..., :3].astype(F32)
        self.a = rgba[..., 3].astype(F32)
        self.o, self.ppc, self.flip = origin, ppc, flip

    def sample(self, u, v):
        h, w = self.a.shape
        px = (np.asarray(u) - self.o[0]) * self.ppc - 0.5
        py = ((self.o[1] - np.asarray(v)) if self.flip else (np.asarray(v) - self.o[1])) * self.ppc - 0.5
        inside = (px >= -0.5) & (px <= w - 0.5) & (py >= -0.5) & (py <= h - 0.5)
        px, py = np.clip(px, 0, w - 1.001), np.clip(py, 0, h - 1.001)
        x0, y0 = np.floor(px).astype(np.intp), np.floor(py).astype(np.intp)
        fx, fy = (px - x0).astype(F32), (py - y0).astype(F32)

        def bil(a):
            if a.ndim == 3:
                fx_, fy_ = fx[..., None], fy[..., None]
            else:
                fx_, fy_ = fx, fy
            t = a[y0, x0] * (1 - fx_) + a[y0, x0 + 1] * fx_
            b = a[y0 + 1, x0] * (1 - fx_) + a[y0 + 1, x0 + 1] * fx_
            return t * (1 - fy_) + b * fy_
        return bil(self.rgb), bil(self.a) * inside


def _canvas(w_cm, h_cm, k=PPC, ss=3):
    W, H = int(round(w_cm * k)), int(round(h_cm * k))
    im = Image.new("RGBA", (W * ss, H * ss), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im), (lambda x, y: (x * k * ss, y * k * ss)), ss


def _done(im, ss):
    W, H = im.size[0] // ss, im.size[1] // ss
    a = np.asarray(im.resize((W, H), Image.BOX), dtype=F32) / 255.0
    return a


# ---------------------------------------------------------------- figures for the dials, in strokes (no font needed)
SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg"}


def _digit(dr, P, ch, x, y, w, h, fill, width):
    """A figure drawn as a seven-segment shape (x, y its top left, w by h centimetres)."""
    pts = {"a": [(x, y), (x + w, y)], "b": [(x + w, y), (x + w, y + h / 2)], "c": [(x + w, y + h / 2), (x + w, y + h)], "d": [(x, y + h), (x + w, y + h)],
           "e": [(x, y + h / 2), (x, y + h)], "f": [(x, y), (x, y + h / 2)], "g": [(x, y + h / 2), (x + w, y + h / 2)]}
    for s in SEG[ch]:
        dr.line([P(*p) for p in pts[s]], fill=fill, width=width)


def dial(kind, r=6.6):
    """A dial's face, square, centred on its middle; its centimetres run right and UP (the dial's own X and Y)."""
    k, ss = PPC, 3
    im, dr, P, ss = _canvas(2 * r, 2 * r)
    C = lambda dx, dy: P(r + dx, r - dy)
    W = (238, 236, 226, 255)
    lw = max(1, int(round(0.14 * k * ss)))
    dr.ellipse([*C(-r, r), *C(r, -r)], fill=(33, 30, 36, 255))
    if kind == "speed":
        a0, a1 = 225.0, -45.0                                         # 0 at the lower left, round over the top to 120 at the lower right
        for i in range(25):
            a = math.radians(a0 + (a1 - a0) * i / 24)
            long = i % 4 == 0
            r0 = r * (0.74 if long else 0.82)
            dr.line([C(r0 * math.cos(a), r0 * math.sin(a)), C(r * 0.92 * math.cos(a), r * 0.92 * math.sin(a))], fill=W, width=lw * (2 if long else 1))
        for i, v in enumerate(("0", "20", "40", "60", "80", "100", "120")):
            a = math.radians(a0 + (a1 - a0) * i / 6)
            cx, cy = r * 0.56 * math.cos(a), r * 0.56 * math.sin(a)
            fw, fh = 0.38, 0.62
            x = r + cx - (fw * len(v) + 0.12 * (len(v) - 1)) / 2
            for j, ch in enumerate(v):
                _digit(dr, P, ch, x + j * (fw + 0.12), r - cy - fh / 2, fw, fh, W, lw)
        # the odometer: six figures in a little window, white on black
        ow, oh = 3.9, 0.95
        dr.rectangle([*P(r - ow / 2 - 0.12, r + 1.45 - 0.12), *P(r + ow / 2 + 0.12, r + 1.45 + oh + 0.12)], fill=(120, 116, 110, 255))
        dr.rectangle([*P(r - ow / 2, r + 1.45), *P(r + ow / 2, r + 1.45 + oh)], fill=(14, 12, 14, 255))
        for j, ch in enumerate("200006"):
            _digit(dr, P, ch, r - ow / 2 + 0.16 + j * 0.62, r + 1.6, 0.36, 0.62, W, lw)
        # the needle, resting at 0
        a = math.radians(a0 - 4)
        dr.line([C(-0.5 * math.cos(a), -0.5 * math.sin(a)), C(r * 0.86 * math.cos(a), r * 0.86 * math.sin(a))], fill=(240, 104, 40, 255), width=lw * 2)
    else:
        # fuel in the top half: its own pivot just above the middle, empty at the left, full at the right, the needle at a quarter
        # (no letters: at the size the picture shows the dial they would only be specks)
        fy = 1.0

        for i in range(5):
            a = math.radians(155 - 130 * i / 4)
            dr.line([C(r * 0.58 * math.cos(a), r * 0.58 * math.sin(a) + fy), C(r * 0.78 * math.cos(a), r * 0.78 * math.sin(a) + fy)], fill=W, width=lw * (2 if i in (0, 4) else 1))
        a = math.radians(155 - 130 * 0.25)
        dr.line([C(0, fy), C(r * 0.6 * math.cos(a), r * 0.6 * math.sin(a) + fy)], fill=(240, 104, 40, 255), width=lw * 2)
        dr.ellipse([*C(-0.4, fy + 0.4), *C(0.4, fy - 0.4)], fill=(24, 22, 26, 255))
        # temperature in the bottom half: its own pivot just below the middle, cold at the left, hot at the right, the last
        # stretch red, the needle hard in the red
        ty = -1.0
        for i in range(5):
            a = math.radians(205 + 130 * i / 4)
            dr.line([C(r * 0.58 * math.cos(a), r * 0.58 * math.sin(a) + ty), C(r * 0.78 * math.cos(a), r * 0.78 * math.sin(a) + ty)],
                    fill=(222, 52, 40, 255) if i >= 3 else W, width=lw * (2 if i in (0, 4) else 1))
        a = math.radians(205 + 130 * 0.97)
        dr.line([C(0, ty), C(r * 0.6 * math.cos(a), r * 0.6 * math.sin(a) + ty)], fill=(240, 104, 40, 255), width=lw * 2)
        dr.ellipse([*C(-0.4, ty + 0.4), *C(0.4, ty - 0.4)], fill=(24, 22, 26, 255))
        # the warning lamp, lit: a small red light at the left, between the two
        lx = -r * 0.42
        dr.ellipse([*C(lx - 0.6, 0.6), *C(lx + 0.6, -0.6)], fill=(255, 64, 44, 255))
        dr.ellipse([*C(lx - 0.3, 0.35), *C(lx + 0.15, -0.05)], fill=(255, 196, 170, 255))
    if kind == "speed":                                               # the needle's hub
        dr.ellipse([*C(-0.62, 0.62), *C(0.62, -0.62)], fill=(24, 22, 26, 255))
    return _done(im, ss)


def prndl(w=14.0, h=1.6):
    """The gear strip under the dials: P R N D L, white on black, the orange pointer under P."""
    k, ss = PPC, 3
    im, dr, P, ss = _canvas(w, h)
    dr.rectangle([*P(0, 0), *P(w, h)], fill=(20, 18, 22, 255))
    lw = max(1, int(round(0.12 * k * ss)))
    W_ = (236, 234, 224, 255)
    xs = [1.4 + i * (w - 2.8) / 4 for i in range(5)]
    y0, y1 = 0.25, 1.0
    for ch, x in zip("PRNDL", xs):
        x0, x1 = x - 0.25, x + 0.25
        ym = (y0 + y1) / 2
        if ch == "P":
            dr.line([P(x0, y1), P(x0, y0), P(x1, y0), P(x1, ym), P(x0, ym)], fill=W_, width=lw)
        elif ch == "R":
            dr.line([P(x0, y1), P(x0, y0), P(x1, y0), P(x1, ym), P(x0, ym), P(x1, y1)], fill=W_, width=lw)
        elif ch == "N":
            dr.line([P(x0, y1), P(x0, y0), P(x1, y1), P(x1, y0)], fill=W_, width=lw)
        elif ch == "D":
            dr.line([P(x0, y0), P(x0, y1), P(x1 - 0.1, y1), P(x1, ym), P(x1 - 0.1, y0), P(x0, y0)], fill=W_, width=lw)
        else:
            dr.line([P(x0, y0), P(x0, y1), P(x1, y1)], fill=W_, width=lw)
    dr.polygon([P(xs[0] - 0.35, h), P(xs[0] + 0.35, h), P(xs[0], y1 + 0.12)], fill=(240, 110, 40, 255))
    return _done(im, ss)


# ---------------------------------------------------------------- her drawing, and the registration card
CRAYON = {"blue": (40, 82, 196), "purple": (126, 62, 164), "green": (52, 150, 64), "pink": (232, 98, 152), "red": (214, 48, 40),
          "yellow": (246, 196, 36), "black": (34, 30, 34), "white": (252, 250, 244), "grass": (70, 160, 70), "brown": (130, 84, 46)}
PAPER = (246, 240, 226)


def drawing(w=17.0, h=12.0, seed=4):
    """Little Sister's drawing for Dad's car: crayon on a sheet of her school paper. The family in a row on a green line,
    tallest to smallest (Dad, in blue; Mom, in purple, a skirt; Big Sister; her brother, in green; herself, small and
    pink), the yellow sun up in the corner, and the red car with General Feathers riding on its roof."""
    k, ss = PPC, 3
    rng = np.random.default_rng(seed)
    im, dr, P, ss = _canvas(w, h)
    dr.rectangle([*P(0, 0), *P(w, h)], fill=PAPER + (255,))
    lw = int(round(0.24 * k * ss))

    def crayon(pts, color, width=lw):
        q = [P(x + rng.normal(0, 0.05), y + rng.normal(0, 0.05)) for x, y in pts]
        dr.line(q, fill=color + (255,), width=width, joint="curve")
        for p in (q[0], q[-1]):
            dr.ellipse([p[0] - width / 2, p[1] - width / 2, p[0] + width / 2, p[1] + width / 2], fill=color + (255,))

    base = h - 1.4
    crayon([(0.4, base + 0.15), (w * 0.5, base - 0.05), (w - 0.4, base + 0.1)], CRAYON["grass"], int(lw * 1.3))
    sx, sy, sr = 2.0, 1.9, 1.05                                       # the sun, its rays
    dr.ellipse([*P(sx - sr, sy - sr), *P(sx + sr, sy + sr)], fill=CRAYON["yellow"] + (255,))
    for a in range(0, 360, 45):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        crayon([(sx + ca * (sr + 0.3), sy + sa * (sr + 0.3)), (sx + ca * (sr + 0.95), sy + sa * (sr + 0.95))], CRAYON["yellow"], int(lw * 0.8))

    def person(x, hgt, color, skirt):
        hd = hgt * 0.19
        top = base - hgt
        dr.ellipse([*P(x - hd, top), *P(x + hd, top + 2 * hd)], outline=color + (255,), width=int(lw * 0.9))
        neck, hip = top + 2 * hd, base - hgt * 0.36
        crayon([(x, neck), (x, hip)], color)
        crayon([(x - hgt * 0.26, neck + hgt * 0.16), (x, neck + hgt * 0.06), (x + hgt * 0.26, neck + hgt * 0.16)], color)
        if skirt:
            dr.polygon([P(x, neck + hgt * 0.12), P(x - hgt * 0.22, hip + hgt * 0.06), P(x + hgt * 0.22, hip + hgt * 0.06)], fill=color + (255,))
        crayon([(x - hgt * 0.17, base), (x, hip), (x + hgt * 0.17, base)], color)
        dr.ellipse([*P(x - hd * 0.45, top + hd * 0.7), *P(x - hd * 0.15, top + hd * 1.0)], fill=CRAYON["black"] + (255,))     # two dots for eyes
        dr.ellipse([*P(x + hd * 0.15, top + hd * 0.7), *P(x + hd * 0.45, top + hd * 1.0)], fill=CRAYON["black"] + (255,))
        dr.arc([*P(x - hd * 0.5, top + hd * 0.6), *P(x + hd * 0.5, top + hd * 1.55)], 20, 160, fill=CRAYON["red"] + (255,), width=max(1, int(lw * 0.5)))
    person(2.3, 7.4, CRAYON["blue"], False)                           # Dad, the biggest
    person(4.8, 6.6, CRAYON["purple"], True)                          # Mom
    person(7.0, 5.7, CRAYON["blue"], True)                            # Big Sister
    person(8.9, 4.7, CRAYON["green"], False)                          # her brother
    person(10.5, 3.7, CRAYON["pink"], True)                           # herself
    # the red car, wheels as round as she could make them, and General Feathers on the roof
    cx0, cx1 = 11.6, 16.5
    dr.polygon([P(cx0, base - 0.9), P(cx0, base - 2.3), P(cx0 + 1.0, base - 2.5), P(cx0 + 1.6, base - 3.8), P(cx1 - 1.0, base - 3.8),
                P(cx1 - 0.5, base - 2.5), P(cx1, base - 2.3), P(cx1, base - 0.9)], fill=CRAYON["red"] + (255,))
    dr.polygon([P(cx0 + 1.9, base - 3.5), P(cx0 + 2.8, base - 3.5), P(cx0 + 2.8, base - 2.6), P(cx0 + 1.5, base - 2.6)], fill=(206, 230, 250, 255))
    dr.polygon([P(cx0 + 3.1, base - 3.5), P(cx1 - 1.2, base - 3.5), P(cx1 - 0.8, base - 2.6), P(cx0 + 3.1, base - 2.6)], fill=(206, 230, 250, 255))
    for wx in (cx0 + 1.1, cx1 - 1.1):
        dr.ellipse([*P(wx - 0.7, base - 1.5), *P(wx + 0.7, base - 0.1)], fill=CRAYON["black"] + (255,))
        dr.ellipse([*P(wx - 0.25, base - 1.05), *P(wx + 0.25, base - 0.55)], fill=(214, 214, 214, 255))
    hx, hy = (cx0 + cx1) / 2, base - 3.8                               # the hen, sitting, facing left: white, a red comb, a yellow beak
    dr.ellipse([*P(hx - 1.1, hy - 1.3), *P(hx + 1.1, hy + 0.05)], fill=CRAYON["white"] + (255,), outline=CRAYON["black"] + (255,), width=max(1, int(lw * 0.45)))
    dr.ellipse([*P(hx - 1.45, hy - 2.0), *P(hx - 0.45, hy - 1.0)], fill=CRAYON["white"] + (255,), outline=CRAYON["black"] + (255,), width=max(1, int(lw * 0.45)))
    dr.polygon([P(hx - 1.4, hy - 1.95), P(hx - 1.0, hy - 2.45), P(hx - 0.7, hy - 1.95)], fill=CRAYON["red"] + (255,))
    dr.polygon([P(hx - 1.45, hy - 1.6), P(hx - 1.95, hy - 1.45), P(hx - 1.45, hy - 1.3)], fill=CRAYON["yellow"] + (255,))
    a = _done(im, ss)
    wax = rng.random(a.shape[:2]).astype(F32)                          # crayon is waxy: the paper's tooth shows through it
    ink = (np.abs(a[..., :3] - np.array(PAPER, F32) / 255).sum(axis=2) > 0.1)
    a[..., :3] = np.where((ink & (wax < 0.16))[..., None], np.array(PAPER, F32) / 255 * 0.97, a[..., :3])
    return a


def registration(w=9.5, h=6.0, seed=6):
    """The car's registration card: pale card, a band of colour along its top, rows of tiny print (lines, nothing to
    read), a round stamp at its corner."""
    k, ss = PPC, 3
    im, dr, P, ss = _canvas(w, h)
    dr.rectangle([*P(0, 0), *P(w, h)], fill=(240, 236, 220, 255))
    dr.rectangle([*P(0, 0), *P(w, 1.0)], fill=(176, 196, 214, 255))
    lw = max(1, int(round(0.07 * k * ss)))
    rng = np.random.default_rng(seed)
    for i in range(6):
        y = 1.6 + i * 0.7
        x1 = w - 0.8 - rng.random() * 3.0
        dr.line([P(0.6, y), P(x1, y)], fill=(120, 116, 112, 255), width=lw)
    dr.ellipse([*P(w - 2.6, h - 2.6), *P(w - 0.6, h - 0.6)], outline=(170, 70, 64, 255), width=lw * 2)
    return _done(im, ss)

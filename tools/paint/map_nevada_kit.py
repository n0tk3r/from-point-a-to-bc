"""The Nevada map's own tools (MAP-15N): its measurements, its inks, the printing plates, and the paper they are printed
on. map_nevada.py paints with these; map_nevada_layout.py and map_nevada_check.py read the same measurements.

THE THING ITSELF. A free road map of the kind a filling station once gave away, opened out flat: thin paper gone a
little yellow, folded in a grid (six panels across, two down: an accordion of six, then once across the middle), the
folds worn pale where they cross and split a short way at one edge. It is printed in a few flat inks, each from its own
plate and each a little out of register with the others: a cream for the land, a tan for the high ground (and, screened,
the lot), a faint red-orange for the grid of sections, a blue-grey for the dry lakes, a brown for the hachures of the
ranges, a red for the highway, and a blue-black (the key plate) for the lines and the lettering; some of them screened to
a paler tint as well (the `_tint` inks). Every ink is mixed from the game's paint box by name (postimp_paints.PAINTS)
with the kit's own mixing (brush.rgb, lerp). Ink is printed ON the paper: it multiplies the paper's colour, so the
paper's grain, its yellowing and the creases show through every printed thing, the places' too.

THE LIGHT. The sheet lies flat under a light from the upper left: the panels of the accordion tilt a little toward it
and away from it in turn, each valley fold is a fine shadow and each mountain fold a fine light line.
"""

import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from brush import F32, blur, grid, lerp, noise, rgb, sample
import letter
from postimp_paints import PAINTS

W, H = 800, 600
SS = 3                                                      # the plates are drawn at three times the picture's size

# ---------------------------------------------------------------- the sheet and its folds
SHEET = (40, 134, 760, 566)                                 # the paper's box (its edge wanders a little within it)
NEAT = (52, 146, 748, 554)                                  # the printed map's border (the neat line)
FOLDS_X = (160, 280, 400, 520, 640)                         # the accordion's creases, left to right
VALLEY_X = (True, False, True, False, True)                 # which of them is a valley (the others are mountains)
FOLDS_Y = (350,)                                            # the one crease across the middle
VALLEY_Y = (True,)
SPLIT = dict(fold="y", at=350, edge="left", length=24.0, gape=3.2)    # the one split: along the middle crease, in from the left edge

# ---------------------------------------------------------------- the printed furniture
COVER = (54, 148, 156, 344)                                 # the cover panel (top left): the title, compliments of the store
LEGEND = (54, 448, 222, 552)                                # the legend, the scale of miles, the north arrow (bottom left)
INSET = (436, 148, 746, 450)                                # the detail panel (top right): the Last Stop, in detail
INSET_TITLE = "DETAIL · 37 MILES PAST LAST GAS"

# ---------------------------------------------------------------- the land
# The highway, west to east: in at the left edge between the cover and the legend, through Last Gas, over a pass, and
# on past the Last Stop until it runs off the sheet toward NOTHING. Smoothed through these points.
HIGHWAY = [(50.0, 388.0), (92.0, 391.0), (140.0, 394.5), (186.0, 398.5), (220.0, 402.0), (258.0, 409.0), (292.0, 420.0),
           (318.0, 432.0), (346.0, 446.0), (378.0, 462.0), (410.0, 476.0), (440.0, 488.0), (470.0, 497.0), (510.0, 503.0),
           (560.0, 507.0), (612.0, 510.0), (660.0, 512.0), (705.0, 513.0), (750.0, 514.0)]
LAST_GAS_T = 220.0                                          # where Last Gas is: the x on the highway
LAST_STOP_T = 444.0                                         # where the Last Stop is: the x on the highway (37 miles on)
STRETCH = (478.0, 616.0)                                    # the stretch beyond the Last Stop that `road` picks out (x)
MILES = 37.0                                                # Last Gas to the Last Stop, along the road (the act's own number)

# The ranges: each a crest line (north to south), its half-width along it (how far the slopes reach), how many spurs
# branch off it, and a seed. Basin and range: they run north and south, the valleys between them hold the dry lakes, and
# the highway goes over between them. relief() turns them into a height field; the hachures follow its slopes.
RANGES = [
    # the west range: three ridges overlapping, as such ranges break
    dict(crest=[(205, 150), (200, 182), (196, 216)], reach=[5, 11, 9], spurs=1, seed=11),
    dict(crest=[(190, 206), (196, 240), (194, 276)], reach=[6, 13, 8], spurs=1, seed=19),
    dict(crest=[(197, 266), (189, 304), (183, 348)], reach=[8, 11, 4], spurs=1, seed=20),
    # the big range the highway goes over (its pass between the north part and the south part)
    dict(crest=[(322, 148), (316, 180), (312, 214)], reach=[6, 12, 10], spurs=1, seed=12),
    dict(crest=[(303, 200), (308, 236), (306, 272), (300, 300)], reach=[7, 15, 14, 8], spurs=2, seed=21),
    dict(crest=[(312, 286), (304, 322), (299, 360)], reach=[9, 13, 8], spurs=1, seed=22),
    dict(crest=[(292, 350), (297, 382), (294, 410)], reach=[6, 10, 4], spurs=0, seed=23),
    dict(crest=[(303, 452), (305, 478), (299, 504)], reach=[4, 10, 9], spurs=1, seed=13),
    dict(crest=[(292, 496), (294, 526), (290, 552)], reach=[6, 11, 8], spurs=0, seed=24),
    # the east range, by the detail
    dict(crest=[(411, 154), (407, 190), (404, 228)], reach=[4, 9, 8], spurs=0, seed=14),
    dict(crest=[(398, 218), (404, 262), (403, 300)], reach=[6, 12, 8], spurs=1, seed=25),
    dict(crest=[(396, 290), (392, 340), (386, 380), (384, 410)], reach=[7, 11, 8, 3], spurs=1, seed=26),
    # hills
    dict(crest=[(84, 360), (93, 372), (99, 380)], reach=[3, 6, 3], spurs=0, seed=15),
    dict(crest=[(684, 530), (689, 552)], reach=[6, 11], spurs=0, seed=16),
    dict(crest=[(632, 536), (636, 552)], reach=[4, 7], spurs=0, seed=17),
    dict(crest=[(266, 178), (270, 190)], reach=[3, 4], spurs=0, seed=18),
]
# The dry lakes: a rough ellipse each (middle, half sizes, a seed), and where its printed name goes.
LAKES = [
    dict(c=(252, 262), r=(26, 15), seed=21, name=(252, 232)),
    dict(c=(372, 520), r=(22, 11), seed=22, name=None),
]
LAST_GAS_ROAD = [(220, 402), (228, 360), (240, 318), (248, 280)]        # a dirt road from Last Gas north to the dry lake
SOUTH_ROAD = [(346, 446), (352, 482), (350, 520), (356, 554)]          # a dirt road off the highway, south, off the sheet

# ---------------------------------------------------------------- the inks (the paint box, mixed by name)
def paint(name):
    return rgb(PAINTS[name]["hex"])


def mixp(a, b, t):
    a = paint(a) if isinstance(a, str) else np.asarray(a, F32)
    b = paint(b) if isinstance(b, str) else np.asarray(b, F32)
    return lerp(a, b, t).astype(F32)


WHITE = paint("lead-white")
PAPER = mixp("lead-white", "naples-yellow", 0.20)                          # the paper, new
PAPER_OLD = mixp(mixp("lead-white", "naples-yellow", 0.50), "yellow-ochre", 0.30)   # the paper where it has aged most
SHADE = mixp("lilac", "cobalt-violet", 0.35)                               # the colour a fold's shadow goes to

INK = {                                                                    # the colour each ink prints on lead white
    "cream": mixp("lead-white", "naples-yellow", 0.42),
    "tan": mixp(mixp("naples-yellow", "yellow-ochre", 0.42), "lead-white", 0.50),
    "brown": mixp("burnt-sienna", "deep-violet", 0.10),
    "blue": mixp(mixp("cerulean", "cobalt-blue", 0.35), "lilac", 0.30),
    "red": mixp("vermilion", "chrome-orange", 0.08),
    "key": mixp("prussian-blue", "ultramarine", 0.18),
    "grid": mixp(mixp("chrome-orange", "geranium-lake", 0.25), "lead-white", 0.62),
}
INK.update({                                                               # the screens: the same inks, printed paler
    "red_tint": mixp(INK["red"], "lead-white", 0.66),
    "key_tint": mixp(INK["key"], "lead-white", 0.55),
    "blue_tint": mixp(mixp(INK["blue"], "cerulean", 0.35), "lead-white", 0.50),
    "brown_tint": mixp(INK["brown"], "lead-white", 0.72),
    "tan_tint": mixp(INK["tan"], "lead-white", 0.45),
})
INK_ORDER = ("cream", "tan_tint", "tan", "grid", "blue_tint", "blue", "brown_tint", "brown", "red_tint", "red",
             "key_tint", "key")                                            # the order the plates went through the press
REGISTER = {                                                               # how far each plate is off register (px)
    "cream": (0.0, 0.0), "tan": (0.9, -0.7), "grid": (0.5, 0.4), "blue": (-1.1, 0.9),
    "brown": (-0.6, -0.9), "red": (1.4, 0.8), "key": (0.0, 0.0),
}
for _k in ("red", "key", "blue", "brown", "tan"):
    REGISTER[_k + "_tint"] = REGISTER[_k]                                  # a screen is printed from its ink's own plate


def filt(ink):
    """An ink as a filter: what it does to whatever paper it is printed on (its colour on lead white, over lead white)."""
    return np.clip(INK[ink] / WHITE, 0, 1).astype(F32)


def hexof(c):
    c = np.clip(np.asarray(c, F32) * 255 + 0.5, 0, 255).astype(int)
    return "#%02x%02x%02x" % tuple(c)


# ---------------------------------------------------------------- the plates
PLAIN = None


def face(size, koine=False):
    if koine and letter.KOINE:
        return ImageFont.truetype(letter.KOINE, int(round(size)))
    return ImageFont.load_default(int(round(size)))


class Press:
    """The printing plates of one layer of the map (the sheet's own printing, or one place's, or one way's), each ink a
    plate of its own, drawn at SS times the picture's size. 255 is ink, 0 is none: drawing with value=0 knocks out."""

    def __init__(self, ss=SS):
        self.ss = ss
        self.plates = {}

    def plate(self, ink):
        if ink not in self.plates:
            self.plates[ink] = Image.new("L", (W * self.ss, H * self.ss), 0)
        return self.plates[ink]

    def _d(self, ink):
        return ImageDraw.Draw(self.plate(ink))

    def _p(self, pts):
        s = self.ss
        return [(float(x) * s, float(y) * s) for x, y in pts]

    # shapes
    def poly(self, ink, pts, value=255):
        self._d(ink).polygon(self._p(pts), fill=value)
        return self

    def line(self, ink, pts, width, value=255, round_ends=True):
        s = self.ss
        p = self._p(pts)
        wd = max(1, int(round(width * s)))
        d = self._d(ink)
        d.line(p, fill=value, width=wd, joint="curve")
        if round_ends and wd > 2:
            r = wd / 2
            for px, py in (p[0], p[-1]):
                d.ellipse([px - r, py - r, px + r, py + r], fill=value)
        return self

    def taper(self, ink, pts, w0, w1, value=255):
        n = len(pts)
        for i in range(n - 1):
            self.line(ink, [pts[i], pts[i + 1]], lerp(w0, w1, i / max(n - 2, 1)), value)
        return self

    def dashed(self, ink, pts, width, on, off, phase=0.0, value=255):
        """A dashed line along a polyline: `on` pixels drawn, `off` left, from `phase` along."""
        for a, b in dashes(pts, on, off, phase):
            self.line(ink, [a, b], width, value, round_ends=False)
        return self

    def dotted(self, ink, pts, r, every, phase=0.0, value=255):
        for (x, y) in along(pts, every, phase):
            self.ellipse(ink, x, y, r, r, value)
        return self

    def ellipse(self, ink, cx, cy, rx, ry, value=255):
        s = self.ss
        self._d(ink).ellipse([(cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s], fill=value)
        return self

    def ring(self, ink, cx, cy, rx, ry, width, value=255):
        s = self.ss
        self._d(ink).ellipse([(cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s], outline=value,
                             width=max(1, int(round(width * s))))
        return self

    def rect(self, ink, x0, y0, x1, y1, value=255):
        return self.poly(ink, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], value)

    def frame(self, ink, x0, y0, x1, y1, width, value=255):
        h = width / 2
        for (a, b) in (((x0 - h, y0), (x1 + h, y0)), ((x1, y0), (x1, y1)), ((x1 + h, y1), (x0 - h, y1)), ((x0, y1), (x0, y0))):
            self.line(ink, [a, b], width, value, round_ends=False)
        return self

    # lettering
    def text(self, ink, words, at, size, anchor="ls", koine=False, spacing=0.0, bold=0.0, slant=0.0, value=255):
        """Set a line of type. `size` in picture pixels; `spacing` extra pixels between letters; `bold` thickens the
        strokes by that many picture pixels; `slant` leans it (as italic: x moves right by slant per pixel up).
        Returns the box it took (x0, y0, x1, y1) in picture pixels."""
        s = self.ss
        f = face(size * s, koine)
        tmp = Image.new("L", (int(W * s), int(H * s)), 0)
        d = ImageDraw.Draw(tmp)
        widths = [d.textlength(ch, font=f) for ch in words]
        total = sum(widths) + spacing * s * (len(words) - 1)
        x = at[0] * s - (total / 2 if anchor[0] == "m" else total if anchor[0] == "r" else 0)
        y = at[1] * s
        sw = int(round(bold * s))
        for ch, wch in zip(words, widths):
            d.text((x, y), ch, fill=255, font=f, anchor="l" + anchor[1], stroke_width=sw, stroke_fill=255)
            x += wch + spacing * s
        bb = tmp.getbbox()
        if bb is None:
            return None
        if slant:
            # lean about the baseline: a pixel h above it moves right by slant*h
            base = at[1] * s
            tmp = tmp.transform(tmp.size, Image.AFFINE, (1, slant, -slant * base, 0, 1, 0), resample=Image.BILINEAR)
            bb = tmp.getbbox()
        pl = self.plate(ink)
        if value == 255:
            pl.paste(255, mask=tmp)
        else:
            pl.paste(value, mask=tmp)
        return tuple(v / s for v in bb)

    def text_size(self, words, size, koine=False, spacing=0.0):
        f = face(size * self.ss, koine)
        return (sum(f.getlength(ch) for ch in words) + spacing * self.ss * (len(words) - 1)) / self.ss

    def paste_mask(self, ink, m, value=255):
        """Print (or knock out, value=0) wherever a boolean mask at the picture's size is true."""
        im = Image.fromarray((np.asarray(m) > 0).astype(np.uint8) * 255, "L").resize((W * self.ss, H * self.ss), Image.NEAREST)
        self.plate(ink).paste(value, mask=im)
        return self

    def knock(self, inks, pts):
        """Knock a polygon out of the given plates (a panel printed in paper colour over the map)."""
        for ink in inks:
            if ink in self.plates:
                self.poly(ink, pts, 0)
        return self

    # out
    def cover(self, ink):
        """The plate as coverage at the picture's size (0 to 1)."""
        if ink not in self.plates:
            return None
        s = self.ss
        im = self.plates[ink].resize((W, H), Image.BOX)
        return np.asarray(im, dtype=F32) / 255

    def inks(self):
        return [k for k in INK_ORDER if k in self.plates]

    def footprint(self):
        """Every pixel any of this layer's plates covers (0 to 1)."""
        out = np.zeros((H, W), F32)
        for ink in self.inks():
            out = np.maximum(out, self.cover(ink))
        return out


# ---------------------------------------------------------------- lines along a path
def smooth_path(points, steps=10):
    """A smooth curve through the points (Catmull-Rom), as a dense polyline."""
    from brush import curve
    return curve(points, steps)


def path_length(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts[:-1], pts[1:]))


def cut(pts, x0, x1):
    """The part of a polyline (running left to right) between x0 and x1."""
    out = []
    for a, b in zip(pts[:-1], pts[1:]):
        if b[0] < x0 or a[0] > x1:
            continue
        pa = a if a[0] >= x0 else (x0, a[1] + (b[1] - a[1]) * (x0 - a[0]) / max(1e-6, b[0] - a[0]))
        pb = b if b[0] <= x1 else (x1, a[1] + (b[1] - a[1]) * (x1 - a[0]) / max(1e-6, b[0] - a[0]))
        if not out:
            out.append(pa)
        out.append(pb)
    return out


def at_x(pts, x):
    """The point of a left-to-right polyline at x, and the direction there (unit vector)."""
    for a, b in zip(pts[:-1], pts[1:]):
        if a[0] <= x <= b[0]:
            t = (x - a[0]) / max(1e-6, b[0] - a[0])
            dx, dy = b[0] - a[0], b[1] - a[1]
            n = math.hypot(dx, dy) or 1.0
            return (a[0] + dx * t, a[1] + dy * t), (dx / n, dy / n)
    a, b = pts[-2], pts[-1]
    n = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    return b, ((b[0] - a[0]) / n, (b[1] - a[1]) / n)


def along(pts, every, phase=0.0):
    """Points every `every` pixels along a polyline."""
    out, carry = [], phase
    for a, b in zip(pts[:-1], pts[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        t = carry
        while t <= seg:
            k = t / max(seg, 1e-6)
            out.append((a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k))
            t += every
        carry = t - seg
    return out


def dashes(pts, on, off, phase=0.0):
    """The dashes of a dashed line along a polyline, as (start, end) pairs."""
    out = []
    pos = -phase
    period = on + off
    total = 0.0
    segs = []
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        segs.append((a, b, total, L))
        total += L

    def point(d):
        for a, b, t0, L in segs:
            if t0 <= d <= t0 + L:
                k = (d - t0) / max(L, 1e-6)
                return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
        return segs[-1][1]
    while pos < total:
        d0, d1 = max(pos, 0.0), min(pos + on, total)
        if d1 > d0:
            out.append((point(d0), point(d1)))
        pos += period
    return out


# ---------------------------------------------------------------- the paper
def sheet_mask(seed=5):
    """The paper's outline: SHEET with its edge wandering a little, its corners rounded and worn, a nick or two, and
    the one split along a crease. -> mask (H, W) of 0 or 1."""
    x0, y0, x1, y1 = SHEET
    xx, yy = grid((H, W))
    wob = (noise((H, W), 70, seed, 3) - 0.5) * 3.0 + (noise((H, W), 9, seed + 1, 2) - 0.5) * 0.7
    dx = np.minimum(xx - x0, x1 - xx)
    dy = np.minimum(yy - y0, y1 - yy)
    inside = np.minimum(dx, dy) + wob
    m = inside > 0
    for (cx, cy, r) in ((x0 + 7, y0 + 7, 7.0), (x1 - 8, y0 + 6, 6.0), (x1 - 9, y1 - 9, 9.0), (x0 + 6, y1 - 6, 6.0)):
        near = (np.abs(xx - cx) <= r + 1) & (np.abs(yy - cy) <= r + 1)
        corner = ((xx - cx) * np.sign(cx - (x0 + x1) / 2) > 0) & ((yy - cy) * np.sign(cy - (y0 + y1) / 2) > 0)
        m &= ~(near & corner & (np.hypot(xx - cx, yy - cy) + wob * 0.6 > r))
    rng = np.random.default_rng(seed)
    for (ex, ey, r) in ((x0 + 300 + rng.random() * 40, y1, 2.2), (x1, y0 + 170, 1.8), (x0 + 520, y0, 1.6)):
        m &= np.hypot(xx - ex, yy - ey) > r + wob * 0.3
    # the split: a narrow wedge along the crease, open at the edge, closing to nothing
    if SPLIT["fold"] == "y":
        at, L, g = SPLIT["at"], SPLIT["length"], SPLIT["gape"]
        ex = x0 if SPLIT["edge"] == "left" else x1
        d = np.abs(xx - ex)
        half = np.clip(1 - d / L, 0, 1) ** 1.3 * g / 2
        jag = (noise((H, W), (4, 2), seed + 9, 2) - 0.5) * 0.9
        m &= ~((d < L) & (np.abs(yy - at - jag) < half))
    return m.astype(F32)


def edge_distance(alpha):
    """Roughly how far each pixel is inside the paper (pixels), from the mask blurred at several sizes (smooth)."""
    out = np.zeros_like(alpha)
    for r in (1.0, 2.0, 4.0, 8.0, 16.0, 32.0):
        out += np.clip((blur(alpha, r * 0.6) - 0.5) * 2.0, 0, 1) * r
    return out * alpha


def folds_height(seed=3):
    """The sheet's small hills and valleys: the accordion's zigzag, each panel bowed a little, the middle fold."""
    xx, yy = grid((H, W))
    x0, y0, x1, y1 = SHEET
    edges = [x0] + list(FOLDS_X) + [x1]
    h = np.zeros((H, W), F32)
    heights = []
    level = 0.0
    for i, v in enumerate(VALLEY_X):                         # a valley is low, a mountain high
        heights.append(-1.0 if v else 1.0)
    hx = [heights[0] * -0.6] + heights + [heights[-1] * -0.6]
    for i in range(len(edges) - 1):
        a, b = edges[i], edges[i + 1]
        t = np.clip((xx - a) / (b - a), 0, 1)
        inside = (xx >= a) & (xx < b)
        bow = np.sin(np.pi * t) * 0.35 * (1 if i % 2 else -1)
        h = np.where(inside, hx[i] + (hx[i + 1] - hx[i]) * t + bow, h)
    # the middle fold: the two halves meet in a valley
    ty = np.clip(np.abs(yy - FOLDS_Y[0]) / ((y1 - y0) / 2), 0, 1)
    h += (ty * 0.9 - 0.45) * (1 if VALLEY_Y[0] else -1)
    h += (noise((H, W), 160, seed, 3) - 0.5) * 0.8          # the paper never quite lies flat
    return h * 3.0


def shading(h):
    """Light on the sheet's hills and valleys, from the upper left: 1 is flat."""
    gy, gx = np.gradient(blur(h, 1.0))
    L = np.array([-0.55, -0.45, 0.70], F32)
    nz = 1.0 / np.sqrt(gx * gx + gy * gy + 1.0)
    nx, ny = -gx * nz, -gy * nz
    lit = nx * L[0] + ny * L[1] + nz * L[2]
    return (lit / L[2]).astype(F32)


def crease_lines():
    """For each crease: a mask of its line (soft, a pixel or two), and which way it folds. -> list of (mask, valley, axis)."""
    xx, yy = grid((H, W))
    out = []
    jx = (noise((H, W), (3, 40), 31, 3) - 0.5) * 1.4         # a crease is pressed by hand: it wanders a little
    jy = (noise((H, W), (40, 3), 32, 3) - 0.5) * 1.4
    for x, v in zip(FOLDS_X, VALLEY_X):
        d = np.abs(xx - x - jx)
        out.append((np.clip(1.2 - d, 0, 1).astype(F32), v, "x", x))
    for y, v in zip(FOLDS_Y, VALLEY_Y):
        d = np.abs(yy - y - jy)
        out.append((np.clip(1.2 - d, 0, 1).astype(F32), v, "y", y))
    return out


def wear_mask(seed=41):
    """Where the printing is rubbed thin: along every crease, most of all where two cross, a little along the edges and
    over the cover (the outside of the map when it is folded). 0 is as printed, 1 is gone."""
    xx, yy = grid((H, W))
    n = noise((H, W), (5, 5), seed, 3)
    streak_x = noise((H, W), (2, 14), seed + 1, 3)
    streak_y = noise((H, W), (14, 2), seed + 2, 3)
    wear = np.zeros((H, W), F32)
    for x in FOLDS_X:
        d = np.abs(xx - x)
        wear = np.maximum(wear, np.exp(-(d / 1.7) ** 2) * (0.25 + 0.55 * streak_x))
    for y in FOLDS_Y:
        d = np.abs(yy - y)
        wear = np.maximum(wear, np.exp(-(d / 1.7) ** 2) * (0.25 + 0.55 * streak_y))
    for x in FOLDS_X:
        for y in FOLDS_Y:
            r = np.hypot(xx - x, yy - y)
            wear = np.maximum(wear, np.exp(-(r / 6.5) ** 2) * (0.55 + 0.45 * n))
    # the edges, and the cover panel (the outside of the folded map, handled every time)
    x0, y0, x1, y1 = SHEET
    de = np.minimum(np.minimum(xx - x0, x1 - xx), np.minimum(yy - y0, y1 - yy))
    wear = np.maximum(wear, np.exp(-np.clip(de, 0, None) / 4.0) * 0.45 * n)
    cx0, cy0 = SHEET[0], SHEET[1]
    on_cover = ((xx < FOLDS_X[0]) & (yy < FOLDS_Y[0])).astype(F32)
    rub = noise((H, W), (30, 22), seed + 5, 4)
    wear = np.maximum(wear, on_cover * np.clip(rub - 0.55, 0, 1) * 0.55)
    return np.clip(wear, 0, 0.95).astype(F32)


def register(cov, ink):
    """A plate's coverage moved by its own error of register."""
    dx, dy = REGISTER.get(ink, (0.0, 0.0))
    if not dx and not dy:
        return cov
    xx, yy = grid(cov.shape)
    return sample(cov, xx - dx, yy - dy).astype(F32)


class Lie:
    """How the paper lies: a small displacement of everything printed on it (the panels are not quite flat, and each
    crease kinks a printed line a hair). Applied to a plate's coverage."""

    def __init__(self, seed=61):
        xx, yy = grid((H, W))
        self.dx = (noise((H, W), 150, seed, 3) - 0.5) * 1.0
        self.dy = (noise((H, W), 150, seed + 1, 3) - 0.5) * 1.0
        for i, x in enumerate(FOLDS_X):
            k = 0.35 * (1 if i % 2 else -1)
            self.dy += np.tanh((xx - x) / 1.5) * k * 0.5
        self.xx, self.yy = xx, yy

    def __call__(self, cov):
        return sample(cov, self.xx - self.dx, self.yy - self.dy).astype(F32)


_MOTTLE = {}


def mottle(ink):
    """How evenly an ink lay on the paper: a press never lays a flat ink quite flat (a little thinner here and there,
    the same for every layer printed in that ink, as one plate would be)."""
    if ink not in _MOTTLE:
        seed = 900 + sum(ord(c) for c in ink)
        k = 0.04 if ink == "key" else 0.10                                   # the lines and lettering print solid
        _MOTTLE[ink] = (1 - k + k * noise((H, W), 24, seed, 4) * 0.7 + k * noise((H, W), 3, seed + 1, 2) * 0.3).astype(F32)
    return np.clip(_MOTTLE[ink], 0, 1)


def print_layer(picture, press, wear, lie, density=None, plain=None):
    """Print one layer's plates onto a picture (in the press's order): each ink multiplies what is under it, as much as
    its coverage (moved by the paper's lie and its register, thinned where the print is worn). A layer's "paper" plate,
    if it has one, is where its plates were cut so that nothing else printed there (a knockout): there the picture goes
    back to the plain paper (`plain`) before this layer's inks. Returns the layer's footprint (0 to 1)."""
    foot = np.zeros((H, W), F32)
    if "paper" in press.plates and plain is not None:
        cov = np.clip(lie(press.cover("paper")), 0, 1)
        picture[...] = lerp(picture, plain, cov[..., None])
        foot = np.maximum(foot, cov)
    for ink in press.inks():
        cov = press.cover(ink)
        cov = register(lie(cov), ink)
        cov = np.clip(cov, 0, 1) * (1 - wear) * mottle(ink)
        if density and ink in density:
            cov = cov * density[ink]
        f = filt(ink)
        picture[...] = picture * (1 - cov[..., None] * (1 - f[None, None, :]))
        foot = np.maximum(foot, cov)
    return foot


# ---------------------------------------------------------------- the ranges: a height field, and its hachures
def ridges(r):
    """A range's ridges: its crest, and spurs branching off it down its flanks. -> list of (points, reaches)."""
    from brush import curve
    rng = np.random.default_rng(r["seed"])
    crest = curve(r["crest"], 8)
    reach = np.interp(np.linspace(0, 1, len(crest)), np.linspace(0, 1, len(r["reach"])), r["reach"])
    wander = np.convolve(rng.random(len(crest) + 4), np.ones(5) / 5, mode="valid")[:len(crest)]
    reach = reach * (0.62 + 0.75 * wander)
    out = [(crest, reach)]
    for k in range(r.get("spurs", 0)):
        i = int(rng.uniform(0.15, 0.85) * (len(crest) - 1))
        (ax, ay), (bx, by) = crest[max(i - 1, 0)], crest[min(i + 1, len(crest) - 1)]
        dx, dy = bx - ax, by - ay
        n = math.hypot(dx, dy) or 1.0
        side = 1 if rng.random() < 0.5 else -1
        ang = math.atan2(dy, dx) + side * math.radians(rng.uniform(45, 80))
        L = reach[i] * rng.uniform(1.1, 1.8)
        bend = rng.uniform(-0.35, 0.35)
        p0 = crest[i]
        pts = [(p0[0] + math.cos(ang + bend * t) * L * t, p0[1] + math.sin(ang + bend * t) * L * t) for t in np.linspace(0, 1, 7)]
        rs = np.linspace(reach[i] * 0.66, reach[i] * 0.2, 7)
        out.append((pts, rs))
    return out


def relief(ranges, seed=71):
    """The height of the land: 0 on the valley floors, up to 1 on the crests. Each ridge a rounded hump as wide as its
    reach, the crests rising toward their middles, roughened so no slope is smooth."""
    xx, yy = grid((H, W))
    h = np.zeros((H, W), F32)
    for r in ranges:
        for pts, rs in ridges(r):
            pts = np.asarray(pts, F32)
            x0, y0 = pts[:, 0].min() - rs.max() - 4, pts[:, 1].min() - rs.max() - 4
            x1, y1 = pts[:, 0].max() + rs.max() + 4, pts[:, 1].max() + rs.max() + 4
            sl = (slice(max(int(y0), 0), min(int(y1) + 1, H)), slice(max(int(x0), 0), min(int(x1) + 1, W)))
            X, Y = xx[sl], yy[sl]
            best = np.full(X.shape, 1e9, F32)
            reach_at = np.zeros(X.shape, F32)
            for (a, b, ra, rb) in zip(pts[:-1], pts[1:], rs[:-1], rs[1:]):
                d = b - a
                L2 = float(d @ d) or 1e-6
                t = np.clip(((X - a[0]) * d[0] + (Y - a[1]) * d[1]) / L2, 0, 1)
                px, py = a[0] + d[0] * t, a[1] + d[1] * t
                dist = np.hypot(X - px, Y - py)
                rr = ra + (rb - ra) * t
                closer = dist / np.maximum(rr, 0.5) < best / np.maximum(reach_at, 0.5)
                best = np.where(closer, dist, best)
                reach_at = np.where(closer, rr, reach_at)
            hump = np.clip(1 - best / np.maximum(reach_at, 0.5), 0, 1) ** 1.25 * np.clip(reach_at / 14.0, 0.35, 1.0)
            h[sl] = np.maximum(h[sl], hump)
    rough = noise((H, W), 16, seed, 3) - 0.5
    h = np.where(h > 0, np.clip(h * (1 + 0.22 * rough), 0, 1), 0).astype(F32)
    return blur(h, 0.9)


def hachures(press, h, ink="brown", step=0.19, spacing=2.5, seed=73, box=None):
    """Hachures: short strokes straight down the slope, in rows along the contours (a row for each `step` of height),
    each as long as the slope takes to fall one step, heavier where the slope is steep and on the side away from the
    light (the east). Strokes start `spacing` apart along each row."""
    rng = np.random.default_rng(seed)
    hs = blur(h, 0.8)
    gy, gx = np.gradient(hs)
    taken = {}
    ys, xs = np.nonzero(hs > 0.07)
    order = rng.permutation(len(xs))
    for j in order:
        x, y = float(xs[j]) + rng.random() - 0.5, float(ys[j]) + rng.random() - 0.5
        if box and not (box[0] <= x <= box[2] and box[1] <= y <= box[3]):
            continue
        v = float(sample_at(hs, x, y))
        band = int(v / step)
        f = v / step - band
        if f < 0.62 or v > 0.9:
            continue                                          # strokes start only near the top of each band (not on the crest)
        cell = (band, int(x / spacing), int(y / spacing))
        if cell in taken:
            continue
        near = False
        for ddx in (-1, 0, 1):
            for ddy in (-1, 0, 1):
                q = taken.get((band, cell[1] + ddx, cell[2] + ddy))
                if q and (q[0] - x) ** 2 + (q[1] - y) ** 2 < spacing * spacing:
                    near = True
        if near:
            continue
        taken[cell] = (x, y)
        pts = [(x, y)]
        target = band * step - step * 0.1
        px, py = x, y
        steep = 0.0
        for k in range(16):
            ggx, ggy = float(sample_at(gx, px, py)), float(sample_at(gy, px, py))
            g = math.hypot(ggx, ggy)
            if g < 1e-4:
                break
            steep = max(steep, g)
            px, py = px - ggx / g * 0.6, py - ggy / g * 0.6
            pts.append((px, py))
            if sample_at(hs, px, py) <= target:
                break
        if len(pts) < 3:
            continue
        # the slopes that face the light (the upper left) are drawn light and open, those turned away dark and close
        ddx, ddy = pts[-1][0] - pts[0][0], pts[-1][1] - pts[0][1]
        n = math.hypot(ddx, ddy) or 1.0
        facing = -(ddx * -0.72 + ddy * -0.69) / n * -1                       # +1: the slope faces the light
        if facing > 0.3 and rng.random() < 0.18 * facing:
            continue
        w0 = min(1.0, 0.44 + steep * 3.4) * (1.0 - 0.30 * facing)
        press.taper(ink, [pts[0], pts[len(pts) // 2], pts[-1]], w0, w0 * 0.4)
    return press


def sample_at(a, x, y):
    xi = min(max(int(x), 0), a.shape[1] - 2)
    yi = min(max(int(y), 0), a.shape[0] - 2)
    fx, fy = x - xi, y - yi
    return (a[yi, xi] * (1 - fx) * (1 - fy) + a[yi, xi + 1] * fx * (1 - fy) + a[yi + 1, xi] * (1 - fx) * fy
            + a[yi + 1, xi + 1] * fx * fy)

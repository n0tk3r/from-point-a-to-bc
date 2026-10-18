"""The Office's map, its own tools (OFFICE-17B): a blueprint, a draughtsman's pen, and a rubber stamp.

Pen      the lines of one picture file, in four weights (wall: the walls' heavy lines; line: things, doors, the title
         block; thin: annotation, dimension lines, the scale bar's ticks; faint: what is overhead, drawn dashed or
         dotted). Each weight is a coverage canvas drawn at four times the size and boxed down. A draughtsman's lines are
         ruled and even, a hair past their corners; the furniture is drawn with templates (true circles, true
         rectangles). Lettering is the Office's own single-stroke capitals (office_letters.py).
prints   turns a Pen into the print: a blueprint is a contact print, so a line is the paper left white where the
         drawing kept the light off it, a little soft at its edges, with a faint bloom round the heavy ones.
paper    the sheet: the print's blue (prussian blue with cobalt), developed a little unevenly, paler and greyer toward
         its handled edges, a crease where it was folded in four, the top right corner dog-eared.
stamp    a rubber stamp in red ink over the print, a little crooked, the ink uneven.

Colours are mixed from the paint box by name (postimp_paints.PAINTS), with the kit's own mixing (brush.rgb, lerp); the
map is the interface's and is never keyed. (The Pen is made after the house map's pencil, map_home_kit.Lead, kept here
so that nothing is imported from another painter's files.)"""

import math

import numpy as np
from PIL import Image, ImageChops, ImageDraw

from brush import F32, blur, grid, lerp, mask_poly, noise, over, rgb, tint, warp
import office_letters as LT
from postimp_paints import PAINTS

SS = 4


def paint(name):
    return rgb(PAINTS[name]["hex"])


def mixp(a, b, t):
    A = paint(a) if isinstance(a, str) else np.asarray(a, F32)
    B = paint(b) if isinstance(b, str) else np.asarray(b, F32)
    return (A + (B - A) * t).astype(F32)


# ---------------------------------------------------------------- the colours of the print
BLUE = mixp(mixp("prussian-blue", "cobalt-blue", 0.42), "ultramarine", 0.12)      # the print's ground
BLUE_DEEP = mixp(BLUE, "prussian-blue", 0.45)
BLUE_PALE = mixp(mixp(BLUE, "cerulean", 0.30), "lead-white", 0.10)                 # faded at the handled edges
WHITE_LINE = mixp("lead-white", "cerulean", 0.16)                                  # a line: the paper left white
WHITE_SOFT = mixp(WHITE_LINE, BLUE, 0.35)
SHADE = mixp(BLUE, "deep-violet", 0.35)
STAMP_RED = mixp("vermilion", "geranium-lake", 0.30)
LABEL = mixp("lead-white", "cerulean", 0.10)                                       # the engine's names
HALO = mixp(BLUE, "prussian-blue", 0.15)

WEIGHT = {"wall": 1.0, "line": 0.94, "thin": 0.78, "faint": 0.62}


def _resample(points, step=1.5):
    out = [np.asarray(points[0], float)]
    for a, b in zip(points[:-1], points[1:]):
        a, b = np.asarray(a, float), np.asarray(b, float)
        n = max(1, int(math.ceil(np.hypot(*(b - a)) / step)))
        for k in range(1, n + 1):
            out.append(a + (b - a) * k / n)
    return out


class Pen:
    """The lines of one picture file (see the module's notes). Every method takes picture pixels."""

    def __init__(self, shape, seed=0):
        self.shape = shape
        h, w = shape
        self.can = {k: Image.new("L", (w * SS, h * SS), 0) for k in WEIGHT}
        self.draw = {k: ImageDraw.Draw(v) for k, v in self.can.items()}
        self.seed = seed
        self.n = 0

    def _next(self):
        self.n += 1
        return self.seed * 1000 + self.n

    def _line(self, pts, width, weight):
        d = self.draw[weight]
        wd = max(1, int(round(width * SS)))
        q = [(x * SS, y * SS) for x, y in pts]
        d.line(q, fill=255, width=wd, joint="curve")
        r = wd / 2
        for px, py in (q[0], q[-1]):
            d.ellipse([px - r, py - r, px + r, py + r], fill=255)

    def rule(self, p, q, width=1.0, weight="line", over=0.6):
        """A ruled line, a hair past both ends."""
        p, q = np.asarray(p, float), np.asarray(q, float)
        d = q - p
        L = float(np.hypot(*d))
        if L < 1e-6:
            return self
        u = d / L
        self._line([tuple(p - u * over), tuple(q + u * over)], width, weight)
        return self

    def poly(self, points, width=1.0, weight="line", closed=True, over=0.6):
        pts = list(points)
        segs = list(zip(pts, pts[1:] + pts[:1])) if closed else list(zip(pts[:-1], pts[1:]))
        for a, b in segs:
            self.rule(a, b, width, weight, over)
        return self

    def rect(self, x0, y0, x1, y1, width=1.0, weight="line"):
        return self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], width, weight)

    def polyline(self, points, width=1.0, weight="line"):
        self._line(_resample(points, 1.0), width, weight)
        return self

    def dashed(self, points, width=0.9, weight="faint", on=5.0, off=3.0, closed=False):
        pts = list(points) + ([points[0]] if closed else [])
        pts = _resample(pts, 0.5)
        run, piece, drawing = 0.0, [pts[0]], True
        for a, b in zip(pts[:-1], pts[1:]):
            run += float(np.hypot(b[0] - a[0], b[1] - a[1]))
            piece.append(b)
            if run >= (on if drawing else off):
                if drawing and len(piece) > 1:
                    self._line(piece, width, weight)
                piece, run, drawing = [b], 0.0, not drawing
        if drawing and len(piece) > 1:
            self._line(piece, width, weight)
        return self

    def dots(self, points, r=0.8, gap=4.0, weight="faint", closed=False, start=0.0):
        pts = list(points) + ([points[0]] if closed else [])
        pts = _resample(pts, 0.25)
        d = self.draw[weight]
        run, nxt = 0.0, start
        for a, b in zip(pts[:-1], pts[1:]):
            run += float(np.hypot(b[0] - a[0], b[1] - a[1]))
            if run >= nxt:
                rr = r * SS
                d.ellipse([b[0] * SS - rr, b[1] * SS - rr, b[0] * SS + rr, b[1] * SS + rr], fill=255)
                nxt += gap
        return self

    def circle(self, c, r, width=1.0, weight="line", ry=None):
        ry = r if ry is None else ry
        d = self.draw[weight]
        wd = max(1, int(round(width * SS)))
        d.ellipse([(c[0] - r) * SS, (c[1] - ry) * SS, (c[0] + r) * SS, (c[1] + ry) * SS], outline=255, width=wd)
        return self

    def arc(self, c, r, a0, a1, width=0.8, weight="thin"):
        d = self.draw[weight]
        wd = max(1, int(round(width * SS)))
        d.arc([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], a0, a1, fill=255, width=wd)
        return self

    def dot(self, c, r, weight="line"):
        d = self.draw[weight]
        d.ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], fill=255)
        return self

    def fill(self, points, weight="line"):
        self.draw[weight].polygon([(x * SS, y * SS) for x, y in points], fill=255)
        return self

    def hatch(self, points, angle=45.0, spacing=3.0, width=0.6, weight="thin"):
        """Parallel ruled lines across a polygon (a section's poché, a wall's hatch)."""
        h, w = self.shape
        xs, ys = [p[0] for p in points], [p[1] for p in points]
        x0, y0 = max(int(min(xs)) - 2, 0), max(int(min(ys)) - 2, 0)
        x1, y1 = min(int(max(xs)) + 3, w), min(int(max(ys)) + 3, h)
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        R = math.hypot(max(xs) - min(xs), max(ys) - min(ys)) / 2 + 2
        a = math.radians(angle)
        ux, uy = math.cos(a), math.sin(a)
        vx, vy = -uy, ux
        tmp = Image.new("L", ((x1 - x0) * SS, (y1 - y0) * SS), 0)
        td = ImageDraw.Draw(tmp)
        k = -R
        while k <= R:
            p = (cx + vx * k - ux * R, cy + vy * k - uy * R)
            q = (cx + vx * k + ux * R, cy + vy * k + uy * R)
            td.line([((p[0] - x0) * SS, (p[1] - y0) * SS), ((q[0] - x0) * SS, (q[1] - y0) * SS)], fill=255,
                    width=max(1, int(round(width * SS))))
            k += spacing
        clip = Image.new("L", tmp.size, 0)
        ImageDraw.Draw(clip).polygon([((x - x0) * SS, (y - y0) * SS) for x, y in points], fill=255)
        tmp = ImageChops.multiply(tmp, clip)
        region = self.can[weight].crop((x0 * SS, y0 * SS, x1 * SS, y1 * SS))
        self.can[weight].paste(ImageChops.lighter(region, tmp), (x0 * SS, y0 * SS))
        return self

    def arrowhead(self, tip, toward, size=4.5, weight="line", filled=True):
        a = math.atan2(tip[1] - toward[1], tip[0] - toward[0])
        p1 = (tip[0] + size * math.cos(a + math.pi - 0.42), tip[1] + size * math.sin(a + math.pi - 0.42))
        p2 = (tip[0] + size * math.cos(a + math.pi + 0.42), tip[1] + size * math.sin(a + math.pi + 0.42))
        if filled:
            return self.fill([tip, p1, p2], weight)
        self.rule(tip, p1, 0.9, weight, 0)
        return self.rule(tip, p2, 0.9, weight, 0)

    def text(self, words, at, cap, weight="thin", anchor="ls", width=None, spacing=0.30, slant=0.0, stretch=1.0):
        """The draughtsman's capitals (office_letters), `cap` pixels high, strokes `width` (a tenth of the cap if not
        said, never under 0.7)."""
        wd = width if width is not None else max(0.7, cap * 0.11)
        LT.draw(self.draw[weight], words, at, cap, wd, anchor=anchor, spacing=spacing, slant=slant, stretch=stretch, ss=SS)
        return LT.width(words, cap, spacing, stretch)

    def clear(self, points):
        for d in self.draw.values():
            d.polygon([(x * SS, y * SS) for x, y in points], fill=0)
        return self

    def done(self):
        h, w = self.shape
        return {k: np.asarray(im.resize((w, h), Image.BOX), dtype=F32) / 255 for k, im in self.can.items()}


def coverage(cov):
    total = np.zeros_like(next(iter(cov.values())))
    for c in cov.values():
        total = np.maximum(total, c)
    return total


def prints(picture, cov, grain_):
    """Lay a Pen's lines on the print (in place): the paper left white where each line is, the weights' whites a shade
    apart, a little soft at the edges, a faint bloom round the heavy ones, the grain of the paper in it. Returns how much
    of each pixel is line."""
    keep = np.ones(picture.shape[:2], F32)
    for k, c in cov.items():
        keep *= 1 - WEIGHT[k] * c
    a = 1 - keep
    soft = blur(a, 0.45)
    a = np.maximum(a * 0.85, soft)
    bloom = blur(cov["wall"] + cov["line"] * 0.5, 1.8) * 0.20
    tint_ = lerp(WHITE_SOFT[None, None, :], WHITE_LINE[None, None, :], np.clip(a * 1.2, 0, 1)[..., None])
    over(picture, WHITE_SOFT, np.clip(bloom, 0, 0.25))
    over(picture, tint_, np.clip(a * (0.86 + 0.14 * grain_), 0, 1))
    return a


# ---------------------------------------------------------------- the sheet
def sheet_outline(box, seed, ear=None):
    """The sheet's edge: a rectangle whose sides wander a pixel or so, less the dog-eared corner (ear: (corner, size)).
    -> (outline, flap triangle or None, fold line or None)."""
    x0, y0, x1, y1 = box
    rng = np.random.default_rng(seed)
    pts = []
    for (ax, ay), (bx, by) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        n = int(max(abs(bx - ax), abs(by - ay)) / 9)
        walk = np.cumsum(rng.normal(0, 0.25, n + 1))
        walk -= np.linspace(walk[0], walk[-1], n + 1)
        for k in range(n):
            t = k / n
            px, py = ax + (bx - ax) * t, ay + (by - ay) * t
            if ay == by:
                py += walk[k] * 0.7
            else:
                px += walk[k] * 0.7
            pts.append((px, py))
    flap = fold = None
    if ear:
        (cx, cy), size = ear
        sx = 1 if cx == x0 else -1
        sy = 1 if cy == y0 else -1
        a = (cx + sx * size, cy)
        b = (cx, cy + sy * size * 0.9)
        keep = []
        for p in pts:
            side = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
            ref = (b[0] - a[0]) * (cy - a[1]) - (b[1] - a[1]) * (cx - a[0])
            if side * ref <= 0:
                keep.append(p)
        out = []
        for i, p in enumerate(keep):
            out.append(p)
            q = keep[(i + 1) % len(keep)]
            if math.hypot(q[0] - p[0], q[1] - p[1]) > 30:
                out += [a, b] if math.hypot(p[0] - a[0], p[1] - a[1]) < math.hypot(p[0] - b[0], p[1] - b[1]) else [b, a]
        pts = out
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        t = ((cx - a[0]) * dx + (cy - a[1]) * dy) / L2
        fx, fy = a[0] + dx * t, a[1] + dy * t
        rc = (2 * fx - cx, 2 * fy - cy)
        rc = (fx + (rc[0] - fx) * 0.94, fy + (rc[1] - fy) * 0.94)
        flap = [a, b, rc]
        fold = (a, b)
    return pts, flap, fold


def paper_under(shape, outline, flap, creases, seed):
    """The print, broad and soft: the blue developed a little unevenly (a slow mottle and the wash's tide marks),
    paler and greyer toward the handled edges, each crease's facets a shade apart (the light from the top left), the
    shadow the dog-ear throws. -> (picture, sheet mask)."""
    h, w = shape
    x, y = grid(shape)
    m = mask_poly(shape, outline, ss=3)
    mott = noise(shape, 150, seed, 4)
    tide = noise(shape, (300, 60), seed + 1, 3)
    pic = np.zeros((h, w, 3), F32) + BLUE
    pic = lerp(pic, BLUE_DEEP[None, None, :], ((mott - 0.5) * 0.55 + 0.12)[..., None].clip(0, 1))
    pic = lerp(pic, BLUE_PALE[None, None, :], (np.clip(tide - 0.62, 0, 1) * 0.5)[..., None])
    pic = pic * (1 + (noise(shape, 9, seed + 2, 3) - 0.5)[..., None] * 0.05)
    inner = blur(m, 16.0)
    edge = np.clip(1 - inner * 1.5, 0, 1) ** 1.4 * m
    pic = lerp(pic, BLUE_PALE[None, None, :], (edge * 0.55)[..., None])
    for (kind, at, tilt) in creases:
        d = ((x - at) if kind == "v" else (y - at)) / 70.0
        face = np.clip(np.abs(d), 0, 1)
        shade_ = np.where(d > 0, tilt, -tilt) * (1 - face) ** 2 * 0.06
        pic = np.clip(pic * (1 - shade_[..., None]), 0, 1)
    if flap is not None:
        sh = mask_poly(shape, [(px - 2.5, py + 3.0) for px, py in flap], soft=2.6)
        tint(pic, mixp("lead-white", SHADE, 0.6), sh * m * 0.8)
    return np.clip(pic, 0, 1), m


def crease_lines(pic, creases, sheet, seed):
    """The creases' own lines: a pale worn ridge, the blue rubbed thin along it, and a darker valley beside it."""
    shape = pic.shape[:2]
    x, y = grid(shape)
    for i, (kind, at, tilt) in enumerate(creases):
        wv = (noise(shape, (400, 400), seed + i, 2) - 0.5) * 2.0
        d = ((x - at) if kind == "v" else (y - at)) - wv
        fade = 0.55 + 0.45 * noise(shape, (90, 90), seed + 10 + i, 2)
        ridge = np.clip(1 - np.abs(d + 0.5) / 1.2, 0, 1) * fade * sheet
        valley = np.clip(1 - np.abs(d - 0.9) / 1.0, 0, 1) * fade * sheet
        over(pic, BLUE_PALE, ridge * 0.55)
        tint(pic, mixp("lead-white", SHADE, 0.45), valley * 0.6)
    return pic


def flap_paint(pic, flap, fold, seed):
    """The back of the dog-ear: the paper's own back, greyish white, a little darker toward the fold."""
    shape = pic.shape[:2]
    fm = mask_poly(shape, flap, ss=3)
    x, y = grid(shape)
    (ax, ay), (bx, by) = fold
    L = math.hypot(bx - ax, by - ay)
    dist = np.abs((bx - ax) * (y - ay) - (by - ay) * (x - ax)) / L
    col = np.zeros_like(pic) + mixp(mixp("lead-white", "cerulean", 0.22), "lilac", 0.12)
    col = col * (1 - np.clip(1 - dist / 12.0, 0, 1)[..., None] * 0.10)
    col = np.clip(col * (1 + (noise(shape, 30, seed, 3) - 0.5)[..., None] * 0.04), 0, 1)
    over(pic, col, fm)
    return fm


def stamp(shape, centre, lines, cap, angle, seed, pad=(7.0, 5.0)):
    """A rubber stamp: a ruled frame round lines of capitals, turned `angle` degrees, the ink uneven (heavier where the
    stamp was pressed, thin and broken at one side, a speck or two). -> coverage of ink (0..1)."""
    h, w = shape
    big = 4
    widths = [LT.width(t, cap, 0.28, 1.08) for t in lines]
    tw = max(widths)
    gap = cap * 1.55
    th = cap + gap * (len(lines) - 1)
    W_, H_ = int(tw + 2 * pad[0] + 8), int(th + 2 * pad[1] + 8)
    im = Image.new("L", (W_ * big, H_ * big), 0)
    d = ImageDraw.Draw(im)
    fw = max(1, int(round(1.6 * big)))
    d.rectangle([4 * big, 4 * big, (W_ - 4) * big, (H_ - 4) * big], outline=255, width=fw)
    d.rectangle([(4 + 2.6) * big, (4 + 2.6) * big, (W_ - 4 - 2.6) * big, (H_ - 4 - 2.6) * big], outline=255, width=max(1, int(0.8 * big)))
    for i, t in enumerate(lines):
        yb = 4 + pad[1] + cap + i * gap
        LT.draw(d, t, (W_ / 2 * big, yb * big), cap * big, max(1.1, cap * 0.16) * big, anchor="ms", spacing=0.28, stretch=1.08)
    im = im.rotate(angle, resample=Image.BICUBIC, expand=True)
    sw, sh = im.size[0] / big, im.size[1] / big
    small = np.asarray(im.resize((int(round(sw)), int(round(sh))), Image.BOX), dtype=F32) / 255
    out = np.zeros(shape, F32)
    x0, y0 = int(round(centre[0] - small.shape[1] / 2)), int(round(centre[1] - small.shape[0] / 2))
    ya, yb_ = max(y0, 0), min(y0 + small.shape[0], h)
    xa, xb = max(x0, 0), min(x0 + small.shape[1], w)
    out[ya:yb_, xa:xb] = small[ya - y0:yb_ - y0, xa - x0:xb - x0]
    press = 0.55 + 0.45 * noise(shape, (40, 40), seed, 3)
    tilt_ = np.clip(1.15 - (grid(shape)[0] - (centre[0] - tw / 2)) / max(1.0, tw) * 0.5, 0.55, 1.0)
    pores = np.clip(noise(shape, 2.2, seed + 1, 2) * 1.6 - 0.25, 0, 1)
    return np.clip(out * press * tilt_ * (0.55 + 0.45 * pores), 0, 1)

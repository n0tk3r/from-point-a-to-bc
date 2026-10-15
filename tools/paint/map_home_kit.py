"""The map of the house, its own tools (MAP-15H): a sheet of squared paper, and a pencil.

Plan     turns one floor's centimetres (map_home_house.py) into the picture: one scale for the whole sheet, the house
         turned half round, as a plan is usually drawn, with the street at the bottom and the garden at the top.
Lead     the pencil marks of one picture file, in four weights (hard: the walls; firm: things; soft: doors' swings,
         rugs, lettering; faint: what is overhead, and dotted ways). Each weight is a coverage canvas drawn at four
         times the size and boxed down. Ruled lines are straight with a little overshoot at their ends, as a ruler
         leaves them; freehand lines wander by a fraction of a pixel; a dashed or dotted line is laid in pieces.
graphite turns a Lead into darkness and colour on the paper: the weights stack as strokes do, the pressure comes and
         goes along a line, and the paper's tooth breaks the grey up a little. Graphite is a cool dark grey with a faint
         sheen where it was pressed hard (prussian blue let down with lead white, and a touch of deep violet).
paper    the sheet: lead white, warmer and darker toward its handled edges, its squares (pale blue-grey, a heavier line
         every fifth), the two creases of being folded into a pocket, a corner turned over, an eraser smudge or two.

Colours are mixed from the paint box by name (postimp_paints.PAINTS), with the kit's own mixing (brush.rgb, lerp)."""

import math

import numpy as np
from PIL import Image, ImageChops, ImageDraw

from brush import F32, blur, grid, lerp, mask_poly, noise, over, rgb, tint, warp
import letter
from postimp_paints import PAINTS

SS = 4                                            # the pencil's canvases are drawn at four times the size


def paint(name):
    return rgb(PAINTS[name]["hex"])


def mixp(a, b, t):
    """Two paints (or colours) mixed: t of the second."""
    A = paint(a) if isinstance(a, str) else np.asarray(a, F32)
    B = paint(b) if isinstance(b, str) else np.asarray(b, F32)
    return (A + (B - A) * t).astype(F32)


# ---------------------------------------------------------------- the colours of the sheet
WHITE = paint("lead-white")
PAPER = mixp("lead-white", mixp("lead-white", "cerulean", 0.5), 0.10)            # the sheet: lead white, a breath cooler
PAPER_EDGE = mixp("lead-white", "naples-yellow", 0.30)                           # where hands have held it
PAPER_BACK = mixp(mixp("lead-white", "naples-yellow", 0.16), "lilac", 0.10)      # the back of the turned corner
GRID = mixp(mixp("lead-white", "cerulean", 0.62), "cobalt-blue", 0.10)           # the squares
GRID_HEAVY = mixp(mixp("lead-white", "cerulean", 0.85), "cobalt-blue", 0.22)     # every fifth line
SHADE = mixp("lilac", "cobalt-violet", 0.35)                                     # the paper's own shadow (folds, the corner)
LEAD_DARK = mixp(mixp("prussian-blue", "deep-violet", 0.18), "lead-white", 0.14) # graphite pressed hard
LEAD_LIGHT = mixp(mixp("prussian-blue", "deep-violet", 0.10), "lead-white", 0.52)
SHEEN = mixp("lead-white", "cerulean", 0.35)
SMUDGE = mixp("prussian-blue", "lead-white", 0.62)                               # graphite rubbed into the paper

WEIGHT = {"hard": 0.92, "firm": 0.86, "soft": 0.60, "faint": 0.44}


# ---------------------------------------------------------------- a floor's plan in the picture
class Plan:
    """X across and Z out from the back wall, in centimetres, to picture pixels: at `s` pixels a centimetre, the
    corner (X1, Z1) of the floor's box at (ox, oy) when turned half round (rot=180), or (X0, Z0) at (ox, oy) if not."""

    def __init__(self, xr, zr, s, ox, oy, rot=180):
        self.x0, self.x1 = xr
        self.z0, self.z1 = zr
        self.s, self.ox, self.oy, self.rot = s, ox, oy, rot

    def __call__(self, X, Z):
        if self.rot == 180:
            return self.ox + (self.x1 - X) * self.s, self.oy + (self.z1 - Z) * self.s
        return self.ox + (X - self.x0) * self.s, self.oy + (Z - self.z0) * self.s

    def pts(self, poly):
        return [self(X, Z) for X, Z in poly]

    def rect(self, x0, x1, z0, z1):
        return self.pts([(x0, z0), (x1, z0), (x1, z1), (x0, z1)])

    def box(self):
        a, b = self(self.x0, self.z0), self(self.x1, self.z1)
        return min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])

    def angle(self, deg):
        """An angle measured in the plan (degrees, from +X toward +Z) as an angle in the picture."""
        return deg + 180.0 if self.rot == 180 else deg


# ---------------------------------------------------------------- the pencil
def _resample(points, step=1.5):
    out = [np.asarray(points[0], float)]
    for a, b in zip(points[:-1], points[1:]):
        a, b = np.asarray(a, float), np.asarray(b, float)
        n = max(1, int(math.ceil(np.hypot(*(b - a)) / step)))
        for k in range(1, n + 1):
            out.append(a + (b - a) * k / n)
    return out


def _wobble(points, amount, seed, cell=22.0):
    """Push a resampled line sideways by a slow random amount (a hand drawing it)."""
    if amount <= 0 or len(points) < 2:
        return [tuple(p) for p in points]
    rng = np.random.default_rng(seed)
    n = len(points)
    knots = rng.normal(0, 1, max(4, int(n * 1.5 / cell) + 4))
    t = np.linspace(0, len(knots) - 3, n)
    off = np.interp(t, np.arange(len(knots)), knots) * amount
    out = []
    for i, p in enumerate(points):
        a = points[max(i - 1, 0)]
        b = points[min(i + 1, n - 1)]
        d = np.asarray(b, float) - np.asarray(a, float)
        L = np.hypot(*d) or 1.0
        nx, ny = -d[1] / L, d[0] / L
        out.append((p[0] + nx * off[i], p[1] + ny * off[i]))
    return out


class Lead:
    """The pencil marks of one picture file (see the module's notes). Every method takes picture pixels."""

    def __init__(self, shape, seed=0, bold=1.0):
        self.shape = shape
        self.bold = bold                          # every line this much wider (a softer pencil, or pressed harder)
        h, w = shape
        self.can = {k: Image.new("L", (w * SS, h * SS), 0) for k in WEIGHT}
        self.draw = {k: ImageDraw.Draw(v) for k, v in self.can.items()}
        self.text_masks = {k: np.zeros(shape, F32) for k in WEIGHT}
        self.seed = seed
        self.n = 0

    def _next(self):
        self.n += 1
        return self.seed * 1000 + self.n

    def _line(self, pts, width, weight):
        d = self.draw[weight]
        wd = max(1, int(round(width * self.bold * SS)))
        q = [(x * SS, y * SS) for x, y in pts]
        d.line(q, fill=255, width=wd, joint="curve")
        r = wd / 2
        for px, py in (q[0], q[-1]):
            d.ellipse([px - r, py - r, px + r, py + r], fill=255)

    # ---- lines
    def rule(self, p, q, width=1.4, weight="hard", over=1.2, wob=0.12):
        """A ruled line from p to q, a little past both ends (over, in pixels)."""
        p, q = np.asarray(p, float), np.asarray(q, float)
        d = q - p
        L = np.hypot(*d)
        if L < 1e-6:
            return self
        u = d / L
        a, b = p - u * over, q + u * over
        pts = _wobble(_resample([a, b], 2.0), wob, self._next(), cell=60.0)
        self._line(pts, width, weight)
        return self

    def free(self, points, width=1.1, weight="firm", wob=0.35, closed=False, cell=18.0):
        """A freehand line through the points (or round them, closed)."""
        pts = list(points) + ([points[0]] if closed else [])
        pts = _wobble(_resample(pts, 1.5), wob, self._next(), cell)
        self._line(pts, width, weight)
        return self

    def dashed(self, points, width=1.0, weight="faint", on=4.0, off=3.0, wob=0.2, closed=False):
        pts = list(points) + ([points[0]] if closed else [])
        pts = _resample(pts, 0.5)
        run, piece, drawing = 0.0, [pts[0]], True
        for a, b in zip(pts[:-1], pts[1:]):
            run += float(np.hypot(b[0] - a[0], b[1] - a[1]))
            piece.append(b)
            if run >= (on if drawing else off):
                if drawing and len(piece) > 1:
                    self._line(_wobble(piece, wob, self._next(), 30.0), width, weight)
                piece, run, drawing = [b], 0.0, not drawing
        if drawing and len(piece) > 1:
            self._line(piece, width, weight)
        return self

    def dots(self, points, r=0.9, gap=4.0, weight="soft", closed=False, start=0.0):
        """A dotted line: small round dots every `gap` pixels, pressed a little unevenly."""
        pts = list(points) + ([points[0]] if closed else [])
        pts = _resample(pts, 0.25)
        rng = np.random.default_rng(self._next())
        d = self.draw[weight]
        run, nxt = 0.0, start
        for a, b in zip(pts[:-1], pts[1:]):
            run += float(np.hypot(b[0] - a[0], b[1] - a[1]))
            if run >= nxt:
                rr = r * self.bold * (0.85 + 0.3 * rng.random()) * SS
                x, y = b[0] * SS + rng.normal(0, 0.15) * SS, b[1] * SS + rng.normal(0, 0.15) * SS
                d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=255)
                nxt += gap
        return self

    def poly(self, points, width=1.1, weight="firm", ruled=False, wob=0.3, over=0.8, sketch=True):
        """A closed outline: ruled (each side a ruled line, crossing at the corners), or freehand: each side its own
        stroke, a little past the corners where the hand ran on (sketch), or one closed stroke (sketch=False)."""
        if ruled:
            for a, b in zip(points, points[1:] + points[:1]):
                self.rule(a, b, width, weight, over=over, wob=0.1)
            return self
        if sketch and len(points) <= 8:
            rng = np.random.default_rng(self._next())
            for a, b in zip(points, points[1:] + points[:1]):
                a, b = np.asarray(a, float), np.asarray(b, float)
                L = float(np.hypot(*(b - a)))
                if L < 1e-6:
                    continue
                u = (b - a) / L
                o0, o1 = rng.uniform(-0.2, 1.1), rng.uniform(-0.2, 1.1)          # ran on, or stopped a hair short
                self.free([tuple(a - u * o0), tuple(b + u * o1)], width, weight, wob=wob, cell=30.0)
            return self
        return self.free(points, width, weight, wob=wob, closed=True)

    def arc(self, c, r, a0, a1, width=0.9, weight="soft", wob=0.25, n=None):
        n = n or max(6, int(abs(a1 - a0) / 6))
        pts = [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
                c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
        return self.free(pts, width, weight, wob=wob)

    def circle(self, c, r, width=1.0, weight="firm", wob=0.25, ry=None):
        ry = r if ry is None else ry
        n = max(12, int(2 * math.pi * max(r, ry) / 2.0))
        pts = [(c[0] + r * math.cos(2 * math.pi * k / n), c[1] + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]
        return self.free(pts, width, weight, wob=wob, closed=True)

    def dot(self, c, r, weight="firm"):
        d = self.draw[weight]
        d.ellipse([(c[0] - r) * SS, (c[1] - r) * SS, (c[0] + r) * SS, (c[1] + r) * SS], fill=255)
        return self

    def fill(self, points, weight="hard"):
        self.draw[weight].polygon([(x * SS, y * SS) for x, y in points], fill=255)
        return self

    def hatch(self, points, angle=45.0, spacing=2.6, width=0.7, weight="soft", wob=0.15):
        """Parallel strokes across a polygon, as a pencil shades: each stroke freehand, cut to the shape."""
        h, w = self.shape
        xs, ys = [p[0] for p in points], [p[1] for p in points]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        R = math.hypot(max(xs) - min(xs), max(ys) - min(ys)) / 2 + 2
        a = math.radians(angle)
        ux, uy = math.cos(a), math.sin(a)
        vx, vy = -uy, ux
        x0, y0 = max(int(min(xs)) - 2, 0), max(int(min(ys)) - 2, 0)
        x1, y1 = min(int(max(xs)) + 3, w), min(int(max(ys)) + 3, h)
        tmp = Image.new("L", ((x1 - x0) * SS, (y1 - y0) * SS), 0)
        td = ImageDraw.Draw(tmp)
        k = -R
        while k <= R:
            p = (cx + vx * k - ux * R, cy + vy * k - uy * R)
            q = (cx + vx * k + ux * R, cy + vy * k + uy * R)
            pts = _wobble(_resample([p, q], 2.0), wob, self._next(), 40.0)
            td.line([((x - x0) * SS, (y - y0) * SS) for x, y in pts], fill=255, width=max(1, int(round(width * self.bold * SS))))
            k += spacing
        clip = Image.new("L", tmp.size, 0)
        ImageDraw.Draw(clip).polygon([((x - x0) * SS, (y - y0) * SS) for x, y in points], fill=255)
        tmp = ImageChops.multiply(tmp, clip)
        region = self.can[weight].crop((x0 * SS, y0 * SS, x1 * SS, y1 * SS))
        self.can[weight].paste(ImageChops.lighter(region, tmp), (x0 * SS, y0 * SS))
        return self

    def arrowhead(self, tip, toward, size=5.0, width=1.1, weight="firm", spread=26.0):
        """Two short strokes back from the tip, away from `toward` (the point the arrow came from)."""
        a = math.atan2(tip[1] - toward[1], tip[0] - toward[0])
        for s in (-1, 1):
            b = a + math.pi + s * math.radians(spread)
            self.free([tip, (tip[0] + size * math.cos(b), tip[1] + size * math.sin(b))], width, weight, wob=0.15)
        return self

    def text(self, words, at, size, weight="firm", anchor="mm", rough=0.25, spacing=0, slant=0.0, seed=None):
        """Hand lettering in the game's own face (Koine Road), at least 9 pixels high."""
        m = letter.mask(self.shape, words, at, size, hand=True, anchor=anchor, rough=rough, spacing=spacing,
                        slant=slant, seed=self._next() if seed is None else seed)
        self.text_masks[weight] = np.maximum(self.text_masks[weight], m)
        return m

    def clear(self, points):
        """Rub out the pencil inside a polygon (where two drawings must not overlap)."""
        for d in self.draw.values():
            d.polygon([(x * SS, y * SS) for x, y in points], fill=0)
        for k in self.text_masks:
            self.text_masks[k] *= 1 - mask_poly(self.shape, points)
        return self

    def done(self):
        """{weight: coverage} at picture size."""
        h, w = self.shape
        out = {}
        for k, im in self.can.items():
            c = np.asarray(im.resize((w, h), Image.BOX), dtype=F32) / 255
            out[k] = np.clip(np.maximum(c, self.text_masks[k]), 0, 1)
        return out


def coverage(cov):
    """All the weights together, as how much of each pixel the pencil touched (0 to 1)."""
    total = np.zeros_like(next(iter(cov.values())))
    for c in cov.values():
        total = np.maximum(total, c)
    return total


def darkness(cov, tooth, pressure):
    """How dark the graphite is at each pixel: the weights stack as strokes do; the pressure comes and goes along a
    line; the paper's tooth breaks the grey up a little."""
    keep = np.ones_like(tooth)
    for k, c in cov.items():
        keep *= 1 - WEIGHT[k] * c
    a = 1 - keep
    return np.clip(a * (0.70 + 0.30 * pressure) * (0.82 + 0.18 * tooth), 0, 1)


def graphite(picture, cov, tooth, pressure, sheen):
    """Lay pencil marks on a picture (in place). Returns the darkness laid."""
    a = darkness(cov, tooth, pressure)
    col = lerp(LEAD_LIGHT[None, None, :], LEAD_DARK[None, None, :], np.clip(a * 1.15, 0, 1)[..., None])
    over(picture, col, a)
    s = np.clip((a - 0.62) * 2.2, 0, 1) * np.clip((sheen - 0.62) * 3.0, 0, 1) * 0.28    # a faint sheen where it is pressed hard
    over(picture, SHEEN, s)
    return a


# ---------------------------------------------------------------- the paper
def sheet_outline(box, seed, turned=None):
    """The sheet's edge: a rectangle whose sides wander a pixel or so, less the turned corner (turned: (corner, size)).
    Returns (outline polygon, flap triangle or None, fold line or None)."""
    x0, y0, x1, y1 = box
    rng = np.random.default_rng(seed)
    pts = []
    for (ax, ay), (bx, by) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        n = int(max(abs(bx - ax), abs(by - ay)) / 9)
        walk = np.cumsum(rng.normal(0, 0.28, n + 1))
        walk -= np.linspace(walk[0], walk[-1], n + 1)
        for k in range(n):
            t = k / n
            px, py = ax + (bx - ax) * t, ay + (by - ay) * t
            if ay == by:
                py += walk[k] * 0.8
            else:
                px += walk[k] * 0.8
            pts.append((px, py))
    flap = fold = None
    if turned:
        (cx, cy), size = turned
        sx = 1 if cx == x0 else -1
        sy = 1 if cy == y0 else -1
        a = (cx + sx * size, cy)                        # where the fold meets the top (or bottom) edge
        b = (cx, cy + sy * size * 0.86)                 # ... and the side
        keep = []
        for p in pts:
            # drop the points beyond the fold line (in the corner)
            side = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
            ref = (b[0] - a[0]) * (cy - a[1]) - (b[1] - a[1]) * (cx - a[0])
            if side * ref <= 0:
                keep.append(p)
        # put the fold's two ends into the outline where the corner was cut
        out = []
        for i, p in enumerate(keep):
            out.append(p)
            q = keep[(i + 1) % len(keep)]
            if math.hypot(q[0] - p[0], q[1] - p[1]) > 30:
                out += [a, b] if math.hypot(p[0] - a[0], p[1] - a[1]) < math.hypot(p[0] - b[0], p[1] - b[1]) else [b, a]
        pts = out
        # the flap: the corner folded over the line a-b (the corner point reflected in it), a little short of true
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        t = ((cx - a[0]) * dx + (cy - a[1]) * dy) / L2
        fx, fy = a[0] + dx * t, a[1] + dy * t
        rc = (2 * fx - cx, 2 * fy - cy)
        rc = (fx + (rc[0] - fx) * 0.93, fy + (rc[1] - fy) * 0.93)
        flap = [a, b, rc]
        fold = (a, b)
    return pts, flap, fold


def paper_under(shape, outline, flap, fold, creases, seed):
    """The sheet, broad and soft: its tone, warmer toward the handled edges, the facets of the creases a shade apart,
    the shadow the turned corner throws. Returns (picture, sheet mask)."""
    h, w = shape
    x, y = grid(shape)
    m = mask_poly(shape, outline, ss=3)
    pic = np.zeros((h, w, 3), F32) + PAPER
    pic = np.clip(pic * (1 + (noise(shape, 120, seed, 4) - 0.5)[..., None] * 0.035), 0, 1)
    pic = lerp(pic, pic * (1 + (noise(shape, 26, seed + 1, 3) - 0.5)[..., None] * 0.03), 1.0)
    # handled edges: distance in from the edge, warmer and a little darker
    inner = blur(m, 14.0)
    edge = np.clip(1 - inner * 1.6, 0, 1) ** 1.5 * m
    pic = lerp(pic, PAPER_EDGE[None, None, :] * 0.985, (edge * 0.55)[..., None])
    # the creases: each facet tilted a little toward or away from the light (from the top left)
    for (kind, at, tilt) in creases:
        if kind == "v":
            d = (x - at) / 60.0
        else:
            d = (y - at) / 60.0
        face = np.clip(np.abs(d), 0, 1)
        shade = np.where(d > 0, tilt, -tilt) * (1 - face) ** 2 * 0.045
        pic = np.clip(pic * (1 - shade[..., None]), 0, 1)
    if flap is not None:
        # the shadow of the turned corner, thrown down and to the right of its edge
        sh = mask_poly(shape, [(px + 2.5, py + 3.0) for px, py in flap], soft=2.6)
        tint(pic, mixp(WHITE, SHADE, 0.55), sh * m * 0.75)
    return pic, m


def flap_paint(pic, flap, fold, seed):
    """The back of the turned corner, laid over the sheet: no squares, a little darker toward the fold, a crisp edge."""
    shape = pic.shape[:2]
    fm = mask_poly(shape, flap, ss=3)
    x, y = grid(shape)
    (ax, ay), (bx, by) = fold
    L = math.hypot(bx - ax, by - ay)
    dist = np.abs((bx - ax) * (y - ay) - (by - ay) * (x - ax)) / L
    col = np.zeros_like(pic) + PAPER_BACK
    col = col * (1 - np.clip(1 - dist / 14.0, 0, 1)[..., None] * 0.07)
    col = np.clip(col * (1 + (noise(shape, 40, seed, 3) - 0.5)[..., None] * 0.03), 0, 1)
    over(pic, col, fm)
    return fm


def grid_masks(shape, origin, pitch, every=5):
    """The printed squares: thin lines every `pitch` pixels, a heavier line every fifth, as masks (crisp, ruled)."""
    h, w = shape
    thin = Image.new("L", (w * SS, h * SS), 0)
    heavy = Image.new("L", (w * SS, h * SS), 0)
    dt, dh = ImageDraw.Draw(thin), ImageDraw.Draw(heavy)
    ox, oy = origin
    k0 = int(math.floor((0 - ox) / pitch)) - 1
    for k in range(k0, k0 + int(w / pitch) + 4):
        x = (ox + k * pitch) * SS
        (dh if k % every == 0 else dt).line([(x, 0), (x, h * SS)], fill=255, width=SS if k % every == 0 else max(1, int(SS * 0.8)))
    k0 = int(math.floor((0 - oy) / pitch)) - 1
    for k in range(k0, k0 + int(h / pitch) + 4):
        y = (oy + k * pitch) * SS
        (dh if k % every == 0 else dt).line([(0, y), (w * SS, y)], fill=255, width=SS if k % every == 0 else max(1, int(SS * 0.8)))
    t = np.asarray(thin.resize((w, h), Image.BOX), dtype=F32) / 255
    hv = np.asarray(heavy.resize((w, h), Image.BOX), dtype=F32) / 255
    return t, hv


def crease_lines(pic, creases, sheet, seed):
    """The creases' own crisp lines: a light ridge and a darker valley beside it, a little wavy, fading out in places."""
    shape = pic.shape[:2]
    x, y = grid(shape)
    for i, (kind, at, tilt) in enumerate(creases):
        wv = (noise(shape, (400, 400), seed + i, 2) - 0.5) * 2.4
        d = ((x - at) if kind == "v" else (y - at)) - wv
        fade = 0.55 + 0.45 * noise(shape, (90, 90), seed + 10 + i, 2)
        ridge = np.clip(1 - np.abs(d + 0.6) / 0.9, 0, 1) * fade * sheet
        valley = np.clip(1 - np.abs(d - 0.7) / 0.9, 0, 1) * fade * sheet
        over(pic, mixp(WHITE, "lead-white", 0.0), ridge * 0.55)
        tint(pic, mixp(WHITE, SHADE, 0.35), valley * 0.85)
    if len(creases) >= 2:
        # where the two creases cross, the paper is worn pale and soft
        vx = [c[1] for c in creases if c[0] == "v"][0]
        hy = [c[1] for c in creases if c[0] == "h"][0]
        wear = np.exp(-(((x - vx) / 7.0) ** 2 + ((y - hy) / 6.0) ** 2)) * sheet
        over(pic, mixp(WHITE, PAPER_EDGE, 0.2), wear * 0.5)
    return pic


def smudge(pic, centre, size, angle, amount, seed, ghost=None, shape_=None):
    """An eraser smudge: graphite rubbed into the paper in a soft smear along the eraser's strokes; `ghost` is a
    polyline (picture pixels) of a line that was rubbed out, left faintly showing."""
    shape = pic.shape[:2]
    x, y = grid(shape)
    a = math.radians(angle)
    u = (x - centre[0]) * math.cos(a) + (y - centre[1]) * math.sin(a)
    v = -(x - centre[0]) * math.sin(a) + (y - centre[1]) * math.cos(a)
    blob = np.exp(-((u / size[0]) ** 2 + (v / size[1]) ** 2) * 1.6)
    streak = 0.65 + 0.35 * warp(noise(shape, (18, 3), seed, 3), 2.0, 12.0, seed + 1)
    m = np.clip(blob * streak, 0, 1) * amount
    if shape_ is not None:
        m *= shape_
    tint(pic, mixp(WHITE, SMUDGE, 0.5), m)
    if ghost:
        lead = Lead(shape, seed=seed + 7)
        lead.free(ghost, 1.2, "soft", wob=0.4)
        g = coverage(lead.done()) * np.clip(blob * 1.4, 0, 1) * 0.30
        if shape_ is not None:
            g *= shape_
        over(pic, LEAD_LIGHT, g)
    return pic

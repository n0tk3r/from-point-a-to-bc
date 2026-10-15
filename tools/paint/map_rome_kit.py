"""The map of Rome (round fifteen, MAP-15R): the tablet's measurements, its paints, and the stylus.

The map is a Roman writing tablet: a raised frame of plain wood round a sunk panel of dark beeswax, and the plan
scratched into the wax with a stylus's point. A scratch shows pale (the wood, or the lighter wax, at its bottom),
crisp, of an even width, with a tiny burr of pushed-up wax along both sides of it. This file holds everything that the
painting (map_rome.py), the drawings (map_rome_places.py), the layout (map_rome_layout.py) and the check
(map_rome_check.py) share.

Light: from the upper left (a window over the boy's left shoulder), as everywhere on the tablet: a groove's upper-left
wall is in shade and its lower-right wall lit; the burr is lit on the upper-left side of a line and dark on the
lower-right side; the frame's inner walls at the top and the left are in shade and throw a little shadow on the wax.

Every colour is mixed from the game's paint box by name (postimp_paints.PAINTS), with brush.rgb and lerp, or laid
with the kit's own tint (a paint multiplied in, as a shadow is)."""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, blur, curve, lerp, rgb
from postimp_paints import PAINTS

W, H = 800, 600
SHAPE = (H, W)
OUT = "out/map-rome"
CHECK = "out/map-rome-check"

# ---------------------------------------------------------------- the tablet, in pixels of the 800 x 600 frame
SHEET = (40, 136, 760, 564)          # the board's outer edge (layout.json "sheet")
WAX = (64, 160, 736, 540)            # the sunk panel of wax, inside the frame
RADIUS = 13                          # the board's corners, rounded by years of hands
LIGHT = np.array([-0.70710678, -0.70710678], dtype=F32)     # toward the light, in picture x and y


def paint(name):
    """A paint of the box, as an rgb array."""
    return rgb(PAINTS[name]["hex"])


def darker(color, dark="prussian-blue", amount=0.4):
    """A colour with a dark paint multiplied in (the kit's tint, as for a shadow)."""
    return (np.asarray(color, F32) * lerp(np.ones(3, F32), paint(dark), amount)).astype(F32)


def hexof(color):
    c = np.clip(np.asarray(color, F32) * 255 + 0.5, 0, 255).astype(int)
    return "#%02x%02x%02x" % tuple(c)


# ---------------------------------------------------------------- the paints of the tablet
BS, PB, DV = paint("burnt-sienna"), paint("prussian-blue"), paint("deep-violet")
YO, NY, LW = paint("yellow-ochre"), paint("naples-yellow"), paint("lead-white")
CV, LI = paint("cobalt-violet"), paint("lilac")

WAX_THIN = darker(lerp(lerp(BS, PB, 0.58), DV, 0.18), amount=0.48)      # where the wax is thin: near black
WAX_MID = darker(lerp(lerp(BS, PB, 0.45), DV, 0.12), amount=0.34)
WAX_THICK = darker(lerp(BS, DV, 0.22), amount=0.22)                      # thick: warmer, a deep red-brown
WAX_SHEEN = lerp(LI, NY, 0.5)                                            # the soft shine of smoothed wax

WOOD = lerp(lerp(YO, BS, 0.40), LI, 0.10)
WOOD_DARK = lerp(BS, DV, 0.18)
WOOD_LIGHT = lerp(lerp(YO, NY, 0.38), LI, 0.08)
WOOD_SHADE = darker(lerp(YO, CV, 0.35), "deep-violet", 0.25)              # wood in shadow: cobalt violet in it

GROOVE = lerp(NY, YO, 0.22)            # the bottom of a deep scratch: the pale wood
GROOVE_LIT = lerp(NY, LW, 0.55)        # its lit lower-right wall
GROOVE_SHADE = lerp(YO, BS, 0.42)      # its shaded upper-left wall
GROOVE_SHALLOW = lerp(YO, BS, 0.30)    # a shallow scratch only reaches the lighter wax: amber
BURR_LIT = lerp(WAX_THICK, NY, 0.35)   # the burr's lit side (mixed over the wax it is pushed up from)
BURR_DARK = PB                         # its shaded side (multiplied in)

LABEL = {"color": hexof(lerp(LW, NY, 0.4)), "halo": hexof(WAX_THIN), "upper": True, "spacing": 0.08, "size": 15}


# ---------------------------------------------------------------- the stylus
class Stylus:
    """Scratches in the wax. Each stroke is laid on two masks at four times the picture's size: how much of each pixel
    is cut (coverage) and how deep (depth: 1 reaches the wood, less only the lighter wax), then cut() turns them into
    the picture of the scratches, burr and all, on any picture of the tablet.

    A line is a hand's line: it is resampled and wobbled a little along its length (`amp`, pixels), its corners run a
    hair past where they turn, and a line gone over twice (`twice`) is a little wider and its edge doubled."""

    def __init__(self, seed=0, ss=4):
        self.ss = ss
        self.cov = Image.new("L", (W * ss, H * ss), 0)
        self.dep = Image.new("L", (W * ss, H * ss), 0)
        self.dc, self.dd = ImageDraw.Draw(self.cov), ImageDraw.Draw(self.dep)
        self.rng = np.random.default_rng(seed)
        self.paths = []                    # every stroke as drawn (picture points), for measuring later

    # ---- the hand
    def hand(self, pts, amp=0.45, step=1.5):
        """The polyline resampled every `step` pixels and wobbled sideways by a smooth wave of `amp` pixels."""
        p = np.asarray(pts, dtype=float)
        if len(p) < 2:
            return [tuple(q) for q in p]
        seg = np.hypot(*np.diff(p, axis=0).T)
        s = np.concatenate([[0], np.cumsum(seg)])
        total = s[-1]
        if total < 1e-6:
            return [tuple(p[0])]
        n = max(2, int(total / step) + 1)
        t = np.linspace(0, total, n)
        x, y = np.interp(t, s, p[:, 0]), np.interp(t, s, p[:, 1])
        if amp > 0:
            r = self.rng
            l1, l2 = r.uniform(26, 60), r.uniform(8, 14)
            ph1, ph2 = r.uniform(0, 2 * math.pi, 2)
            off = amp * (0.75 * np.sin(2 * math.pi * t / l1 + ph1) + 0.35 * np.sin(2 * math.pi * t / l2 + ph2))
            off *= np.clip(np.minimum(t, total - t) / 3.0, 0.25, 1)          # the ends stay where they were put
            gx, gy = np.gradient(x), np.gradient(y)
            g = np.hypot(gx, gy) + 1e-9
            x, y = x - gy / g * off, y + gx / g * off
        return list(zip(x.tolist(), y.tolist()))

    def _put(self, pts, width, depth):
        s = self.ss
        q = [(x * s, y * s) for x, y in pts]
        wd = max(1, int(round(width * s)))
        val = int(np.clip(depth, 0, 1) * 255)
        for d, v in ((self.dc, 255), (self.dd, val)):
            if len(q) > 1:
                d.line(q, fill=v, width=wd, joint="curve")
            r = wd / 2
            for px, py in (q[0], q[-1]) if len(q) > 1 else (q[0],):
                d.ellipse([px - r, py - r, px + r, py + r], fill=v)

    def line(self, pts, w=1.7, depth=0.9, amp=0.45, twice=False, smooth=False, run=0.0):
        """A scratch along the points. `smooth` draws a curve through them; `run` carries the stylus that far past the
        last point (a hand that overshoots)."""
        pts = [tuple(map(float, p)) for p in pts]
        if smooth and len(pts) > 2:
            pts = curve(pts, 12)
        if run and len(pts) > 1:
            (ax, ay), (bx, by) = pts[-2], pts[-1]
            d = math.hypot(bx - ax, by - ay) + 1e-9
            pts = pts + [(bx + (bx - ax) / d * run, by + (by - ay) / d * run)]
        p = self.hand(pts, amp)
        self._put(p, w, depth)
        self.paths.append(p)
        if twice:
            dx, dy = self.rng.normal(0, 0.35, 2)
            p2 = self.hand([(x + dx, y + dy) for x, y in pts], amp * 0.8)
            self._put(p2, w * 0.92, min(1.0, depth + 0.08))
        return p

    def poly(self, pts, closed=True, over=1.0, **how):
        """A shape drawn side by side, each side its own stroke running a little past its corner."""
        pts = list(pts) + ([pts[0]] if closed else [])
        for a, b in zip(pts[:-1], pts[1:]):
            self.line([a, b], run=over * self.rng.uniform(0.2, 1.0), **how)

    def rect(self, x0, y0, x1, y1, **how):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **how)

    def ellipse(self, cx, cy, rx, ry, a0=0.0, a1=360.0, n=None, **how):
        """An ellipse (or an arc of one, degrees clockwise from 3 o'clock), in one stroke that closes a little past
        where it began."""
        if n is None:
            n = max(10, int((abs(a1 - a0) / 360) * 2 * math.pi * max(rx, ry) / 2.5))
        closed = abs(a1 - a0) >= 359.9
        end = a1 + (self.rng.uniform(6, 22) if closed else 0)
        t = np.radians(np.linspace(a0, end, n + 1))
        self.line([(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in t], **how)

    def dot(self, x, y, r=1.25, depth=0.95):
        """A prick of the point: a little round pit."""
        s = self.ss
        for d, v in ((self.dc, 255), (self.dd, int(depth * 255))):
            d.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=v)
        self.paths.append([(x, y)])

    def dotted(self, pts, gap=6.5, r=1.2, smooth=False, depth=0.95, first=0.5):
        """Pricks along a line, every `gap` pixels (a path walked)."""
        pts = [tuple(map(float, p)) for p in pts]
        if smooth and len(pts) > 2:
            pts = curve(pts, 16)
        p = np.asarray(pts)
        seg = np.hypot(*np.diff(p, axis=0).T)
        s = np.concatenate([[0], np.cumsum(seg)])
        k = first * gap
        out = []
        while k <= s[-1] + 1e-6:
            x, y = np.interp(k, s, p[:, 0]), np.interp(k, s, p[:, 1])
            jx, jy = self.rng.normal(0, 0.3, 2)
            self.dot(x + jx, y + jy, r * self.rng.uniform(0.85, 1.15), depth)
            out.append((x, y))
            k += gap * self.rng.uniform(0.9, 1.1)
        self.paths.append([tuple(map(float, q)) for q in pts])
        return out

    def arrow(self, tip, toward, size=6.0, spread=32.0, **how):
        """An arrowhead at `tip`, for a line that comes to it from `toward`."""
        ang = math.atan2(tip[1] - toward[1], tip[0] - toward[0])
        for sgn in (-1, 1):
            a = ang + math.pi - sgn * math.radians(spread)
            self.line([tip, (tip[0] + size * math.cos(a), tip[1] + size * math.sin(a))], amp=0.1, **how)

    def hatch(self, a, b, n, length, angle=90.0, **how):
        """`n` short ticks spaced along a to b, each `length` long at `angle` degrees to the line (a palisade, a
        fence, the steps of a landing)."""
        ax, ay = a
        bx, by = b
        base = math.atan2(by - ay, bx - ax)
        t = math.radians(angle)
        for i in range(n):
            f = (i + 0.5) / n
            x, y = ax + (bx - ax) * f, ay + (by - ay) * f
            dx, dy = math.cos(base + t) * length / 2, math.sin(base + t) * length / 2
            self.line([(x - dx, y - dy), (x + dx, y + dy)], amp=0.1, **how)

    # ---- what was cut
    def masks(self):
        """-> (coverage, depth), floats at picture size."""
        h, w = SHAPE
        c = np.asarray(self.cov.resize((w, h), Image.BOX), dtype=F32) / 255
        dsum = np.asarray(self.dep.resize((w, h), Image.BOX), dtype=F32) / 255
        depth = np.where(c > 1e-3, dsum / np.maximum(c, 1e-3), 0).astype(F32)
        return c, np.clip(depth, 0, 1)


def cut(picture, cov, depth, seed=0, burr=1.0):
    """Cut the scratches into a picture of the tablet. -> (the picture with them, the mask of what they changed).

    The groove shows the wood where deep and the lighter wax where shallow, its upper-left wall shaded and its lower-
    right wall lit; round it a ring of pushed-up wax (the burr), lit on the side toward the light and dark on the
    other. The changed mask covers the groove and the ring: everything a place's picture has to carry."""
    from brush import noise
    pic = picture.copy()
    B = blur(cov, 0.75)
    gy, gx = np.gradient(B)
    mag = np.hypot(gx, gy) + 1e-6
    facing = (-gx / mag) * LIGHT[0] + (-gy / mag) * LIGHT[1]          # >0: this side of the line faces the light
    grown = np.clip(blur(cov, 0.95) * 3.2, 0, 1)
    ring = np.clip(grown - cov, 0, 1) * burr
    core = np.clip((blur(cov, 0.6) - 0.62) * 4.0, 0, 1)                # the groove's middle
    edge = np.clip(cov - core, 0, 1)
    # the groove's colour: deeper is paler (wood), a little uneven along the line
    n = noise(SHAPE, 18, seed + 401, 3)
    d = np.clip(depth * (0.88 + 0.24 * n), 0, 1)[..., None]
    bottom = lerp(GROOVE_SHALLOW, GROOVE, np.clip((d - 0.35) / 0.55, 0, 1))
    shade = np.clip(facing, 0, 1)[..., None] * edge[..., None]
    lit = np.clip(-facing, 0, 1)[..., None] * edge[..., None]
    col = lerp(bottom, lerp(GROOVE_SHADE, bottom, 0.35), shade * 0.75)
    col = lerp(col, GROOVE_LIT, lit * 0.6 * d)
    # the burr
    bl = (ring * np.clip(facing, 0, 1))[..., None]
    bd = (ring * np.clip(-facing, 0, 1))[..., None]
    pic = lerp(pic, lerp(pic, BURR_LIT, 0.55), bl * 0.75)
    pic = pic * lerp(np.ones(3, F32), BURR_DARK, (bd * 0.62))
    pic = lerp(pic, col, cov[..., None])
    changed = np.clip(cov + ring * 1.4, 0, 1)
    return np.clip(pic, 0, 1).astype(F32), changed

"""Tools for the Rome street: the planes of the world as the camera sees them, sun and shade,
world-sized noise for plaster, polygonal paving, and a sheet whose edges wander like a hand's.

World measurements are centimetres, as in persp.py: x to the right of the middle of the street,
y up from the roadway, z away from us."""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import *
from persp import Camera
import letter

W, H = 800, 600
SHAPE = (H, W)
HZ, FULL = 230, 590
cam = Camera(HZ, FULL)
PX, PY = grid(SHAPE)
PX = PX + 0.5                                               # the middle of each pixel
PY = PY + 0.5
EYE, F, Z0 = cam.eye, cam.F, cam.Z0


# ---------------------------------------------------------------- places
def P(x, y, z):
    return cam.pt(x, y, z)


def Q(points):
    return [cam.pt(*p) for p in points]


def kz(z):
    """picture pixels per centimetre at depth z"""
    return F / (Z0 + z)


def row_of(y, z):
    return cam.vy + (EYE - y) * kz(z)


def col_of(x, z):
    return cam.vx + x * kz(z)


# ---------------------------------------------------------------- planes, per pixel
def wall_x(x0):
    """A wall that runs away from us at x = x0. -> (z, y, k, ok) for every pixel that looks at it."""
    k = (PX - cam.vx) / x0
    ok = k > 2e-3
    kk = np.where(ok, k, 2e-3)
    return (F / kk - Z0).astype(F32), (EYE - (PY - cam.vy) / kk).astype(F32), kk.astype(F32), ok


def wall_z(z0):
    """A wall that faces us at depth z0. -> (x, y, k)"""
    k = kz(z0)
    return ((PX - cam.vx) / k).astype(F32), (EYE - (PY - cam.vy) / k).astype(F32), k


def level(y0):
    """A level surface at height y0. -> (x, z, k, ok)"""
    k = (PY - cam.vy) / (EYE - y0)
    ok = k > 2e-3
    kk = np.where(ok, k, 2e-3)
    return ((PX - cam.vx) / kk).astype(F32), (F / kk - Z0).astype(F32), kk.astype(F32), ok


def slope(a, b):
    """A surface that climbs away from us: y = a + b * z (a roof, an awning). -> (x, z, k, ok)"""
    k = (PY - cam.vy + b * F) / (EYE - a + b * Z0)
    ok = k > 2e-3
    kk = np.where(ok, k, 2e-3)
    return ((PX - cam.vx) / kk).astype(F32), (F / kk - Z0).astype(F32), kk.astype(F32), ok


def band(v, lo, hi, px=1.0):
    """1 where lo < v < hi, with an edge one pixel soft. `px` is how much v changes across a pixel."""
    return (np.clip((v - lo) / px + 0.5, 0, 1) * np.clip((hi - v) / px + 0.5, 0, 1)).astype(F32)


def above(v, lo, px=1.0):
    return np.clip((v - lo) / px + 0.5, 0, 1).astype(F32)


def quad(points3, wobble=0.0, seed=0, soft=0.0):
    """A flat shape given by its corners in the world, as a mask."""
    return mask_poly(SHAPE, Q(points3), soft=soft, wobble=wobble, seed=seed)


# ---------------------------------------------------------------- noise that belongs to a surface
_tile = {}


def wn(u, v, cell, seed, octaves=4):
    """Cloudy noise measured in centimetres on a surface: `cell` is the size of the biggest blotches."""
    size = 512
    key = (seed, octaves)
    if key not in _tile:
        _tile[key] = noise((size, size), 64, seed, octaves)
    s = 64.0 / cell
    uu = np.abs(((u * s) % (2 * (size - 2))) - (size - 2))   # fold, so there is no seam
    vv = np.abs(((v * s) % (2 * (size - 2))) - (size - 2))
    return sample(_tile[key], uu, vv)


def _hash(a, b, seed):
    h = np.sin(a * 127.1 + b * 311.7 + seed * 74.7) * 43758.5453
    return h - np.floor(h)


def cells(u, v, cell, seed, jitter=0.86):
    """Irregular many-sided cells (paving stones, marble scraps). -> (distance to the nearest joint in the
    same units as u, a random number per cell, another, distance to the cell's middle)."""
    u = u.astype(np.float64)
    v = v.astype(np.float64)
    iu, iv = np.floor(u / cell), np.floor(v / cell)
    best = np.full(u.shape, 1e9)
    second = np.full(u.shape, 1e9)
    r1 = np.zeros(u.shape)
    r2 = np.zeros(u.shape)
    for du in (-1, 0, 1):
        for dv in (-1, 0, 1):
            cu, cv = iu + du, iv + dv
            su = (cu + 0.5 + (_hash(cu, cv, seed) - 0.5) * jitter) * cell
            sv = (cv + 0.5 + (_hash(cu, cv, seed + 17) - 0.5) * jitter) * cell
            d = np.hypot(u - su, v - sv)
            closer = d < best
            second = np.where(closer, best, np.minimum(second, d))
            r1 = np.where(closer, _hash(cu, cv, seed + 31), r1)
            r2 = np.where(closer, _hash(cu, cv, seed + 47), r2)
            best = np.where(closer, d, best)
    return ((second - best) * 0.5).astype(F32), r1.astype(F32), r2.astype(F32), best.astype(F32)


# ---------------------------------------------------------------- light
# Morning sun from the upper right and a little behind us. In the street nearly everything is in the
# shade of the right-hand houses, and what colors the shade is where a surface looks:
SHADE = {
    "up": ((0.44, 0.50, 0.75), (0.27, 0.36, 0.63), 0.22),        # at the sky: the bluest
    "warm": ((0.46, 0.42, 0.62), (0.38, 0.35, 0.58), 0.25),      # at the sunlit wall opposite: mauve, a little warm
    "front": ((0.48, 0.46, 0.67), (0.34, 0.36, 0.62), 0.22),     # toward us
    "deep": ((0.33, 0.27, 0.36), (0.20, 0.14, 0.24), 0.30),      # under things and inside rooms
    "cloth": ((0.62, 0.62, 0.80), (0.30, 0.34, 0.70), 0.12),     # thin cloth, with the sky coming through it
}


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


def in_shade(c, kind="front"):
    """A local color (or a whole picture of local colors) as it looks in the shade of the street."""
    mult, veil, a = SHADE[kind]
    return (col(c) * np.array(mult, dtype=F32)) * (1 - a) + np.array(veil, dtype=F32) * a


def in_sun(c):
    """...and with the low warm sun on it."""
    return np.clip(col(c) * np.array((1.05, 1.0, 0.90), dtype=F32) + np.array((0.02, 0.01, -0.01), dtype=F32), 0, 1)


def lit(c, sun, kind="front"):
    """A flat color for a face: `sun` is 0 (shade) to 1 (full sun)."""
    return lerp(in_shade(c, kind), in_sun(c), float(sun))


def light(local, sun, kind="front"):
    """A whole picture of local colors, lit: `sun` is a mask."""
    return lerp(in_shade(local, kind), in_sun(local), sun[..., None]).astype(F32)


def far(color, z, tint_to="#b9c2dc", reach=7000.0, most=0.75):
    """Air: things pale toward the haze color with distance."""
    t = np.clip(1 - np.exp(-np.maximum(z, 0) / reach), 0, most)
    return lerp(color, col(tint_to), t[..., None] if np.ndim(t) else t)


# ---------------------------------------------------------------- sheets with a hand's wobble
def put(picture, sheet, amount=1.0, wobble=0.0, seed=0, cell=26.0):
    """Lay a sheet on a picture. With `wobble`, every edge on it wanders by about that many pixels."""
    color, alpha = sheet.done() if hasattr(sheet, "done") else sheet
    if wobble:
        both = warp(np.dstack([color, alpha]), wobble, cell, seed)
        color, alpha = both[..., :3], both[..., 3]
    over(picture, color, np.clip(alpha * amount, 0, 1))
    return color, alpha


def join(*layers):
    """Several (color, alpha) layers, first underneath, as one."""
    color = np.zeros(SHAPE + (3,), dtype=F32)
    alpha = np.zeros(SHAPE, dtype=F32)
    for c, a in layers:
        color = color * (1 - a[..., None]) + c * a[..., None]
        alpha = alpha + a * (1 - alpha)
    return np.where(alpha[..., None] > 1e-4, color / np.maximum(alpha[..., None], 1e-4), 0).astype(F32), alpha.astype(F32)


def words_flat(words, size, hand=True, pad=6, rough=0.6, seed=0):
    """Lettering as a small flat mask of its own (for bending onto a wall). -> mask, (width, height)"""
    f = letter.face(size * 3, hand)
    box = f.getbbox(words)
    w, h = int((box[2] - box[0]) / 3 + pad * 2), int((box[3] - box[1]) / 3 + pad * 2)
    m = letter.mask((h, w), words, (w / 2, h / 2), size, hand=hand, anchor="mm", rough=rough, seed=seed)
    return m, (w, h)


# ---------------------------------------------------------------- a sheet that mixes its paint
class Sheet2:
    """Like brush.Sheet, but a half-clear stroke laid over an earlier one MIXES with it (brush.Sheet
    replaces what is underneath, which punches holes in a cut-out). Same strokes, same `done`."""

    def __init__(self, shape, ss=3):
        self.shape, self.ss = shape, ss
        h, w = shape
        self.rgb = Image.new("RGB", (w * ss, h * ss), (0, 0, 0))            # colors, already multiplied by how much is covered
        self.cov = Image.new("L", (w * ss, h * ss), 0)                      # how much is covered
        self.d_rgb, self.d_cov = ImageDraw.Draw(self.rgb), ImageDraw.Draw(self.cov)

    @staticmethod
    def _rgb(color):
        c = rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
        return tuple(int(v) for v in np.clip(c * 255 + 0.5, 0, 255))

    def _lay(self, draw, box, color, alpha):
        fill = self._rgb(color)
        if alpha >= 0.995:
            draw(self.d_rgb, fill, 0, 0)
            draw(self.d_cov, 255, 0, 0)
            return self
        W_, H_ = self.rgb.size
        x0, y0 = max(0, int(math.floor(box[0])) - 2), max(0, int(math.floor(box[1])) - 2)
        x1, y1 = min(W_, int(math.ceil(box[2])) + 3), min(H_, int(math.ceil(box[3])) + 3)
        if x1 <= x0 or y1 <= y0 or alpha <= 0.003:
            return self
        m = Image.new("L", (x1 - x0, y1 - y0), 0)
        draw(ImageDraw.Draw(m), int(alpha * 255 + 0.5), x0, y0)
        self.rgb.paste(fill, (x0, y0, x1, y1), m)
        self.cov.paste(255, (x0, y0, x1, y1), m)
        return self

    def _segments(self, segs, color, alpha):
        """segs: list of (points, width in sheet pixels, round ends?)"""
        xs = [p[0] for pts, wd, _ in segs for p in pts]
        ys = [p[1] for pts, wd, _ in segs for p in pts]
        pad = max(wd for _, wd, _ in segs)
        box = (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)

        def draw(d, fill, ox, oy):
            for pts, wd, rnd in segs:
                q = [(x - ox, y - oy) for x, y in pts]
                d.line(q, fill=fill, width=wd, joint="curve")
                if rnd and wd > 2:
                    r = wd / 2
                    for px, py in (q[0], q[-1]):
                        d.ellipse([px - r, py - r, px + r, py + r], fill=fill)
        return self._lay(draw, box, color, alpha)

    def line(self, points, color, width=1.0, alpha=1.0, round_ends=True):
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        return self._segments([(pts, max(1, int(round(width * s))), round_ends)], color, alpha)

    def taper(self, points, color, w0, w1, alpha=1.0):
        s = self.ss
        n = len(points)
        segs = []
        for i in range(n - 1):
            wd = lerp(w0, w1, i / max(n - 2, 1))
            segs.append(([(float(points[i][0]) * s, float(points[i][1]) * s), (float(points[i + 1][0]) * s, float(points[i + 1][1]) * s)], max(1, int(round(wd * s))), True))
        return self._segments(segs, color, alpha)

    def poly(self, points, color, alpha=1.0):
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        box = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
        return self._lay(lambda d, fill, ox, oy: d.polygon([(x - ox, y - oy) for x, y in pts], fill=fill), box, color, alpha)

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0):
        s = self.ss
        box = ((cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s)
        if box[2] <= box[0] or box[3] <= box[1]:
            return self
        return self._lay(lambda d, fill, ox, oy: d.ellipse([box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy], fill=fill), box, color, alpha)

    def done(self):
        h, w = self.shape
        c = np.asarray(self.rgb.resize((w, h), Image.BOX), dtype=F32) / 255
        a = np.asarray(self.cov.resize((w, h), Image.BOX), dtype=F32) / 255
        return np.where(a[..., None] > 1e-3, c / np.maximum(a[..., None], 1e-3), 0).clip(0, 1).astype(F32), a.astype(F32)

    def onto(self, picture, amount=1.0):
        color, alpha = self.done()
        return over(picture, color, alpha * amount)

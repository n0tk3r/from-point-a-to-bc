"""The painter's tools: noise, soft shapes, light, brush strokes, grain, and the limited palette.

Everything works on float pictures (height x width x 3, values 0 to 1) and float masks
(height x width, 0 to 1). Needs numpy and Pillow, nothing else.

A picture is made in four passes, the way a background painter worked for a 256-color game:

  1. block in   soft forms and their light, with no texture        (the functions in this file)
  2. brush      repaint the whole thing with visible strokes        strokes()
  3. detail     the few crisp things: lettering, wire, window bars  drawn on top afterwards
  4. scan       pigment grain, then a limited palette with speckle  finish()
"""

import math

import numpy as np
from PIL import Image, ImageDraw

F32 = np.float32


# ---------------------------------------------------------------- small helpers
def rgb(text):
    """'#e8b060' -> array([0.91, 0.69, 0.38])"""
    text = text.lstrip("#")
    return np.array([int(text[i:i + 2], 16) / 255 for i in (0, 2, 4)], dtype=F32)


def lerp(a, b, t):
    return a + (b - a) * t


def smooth(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


def step(edge0, edge1, x):
    """0 below edge0, 1 above edge1, smooth between."""
    return smooth((x - edge0) / (edge1 - edge0 + 1e-9))


def grid(shape):
    h, w = shape
    y, x = np.mgrid[0:h, 0:w].astype(F32)
    return x, y


def ramp(t, stops):
    """Color from a list of (position, '#hex' or rgb) stops. t is a mask-shaped array, 0 to 1."""
    pos = [p for p, _ in stops]
    cols = [rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32) for _, c in stops]
    t = np.clip(t, pos[0], pos[-1])
    out = np.zeros(t.shape + (3,), dtype=F32)
    for i in range(3):
        out[..., i] = np.interp(t, pos, [c[i] for c in cols])
    return out


def resize(a, shape, how=Image.BICUBIC):
    """Resize a float array (2D, or 3D with channels) to (h, w)."""
    h, w = shape
    if a.ndim == 2:
        return np.asarray(Image.fromarray(a.astype(F32), "F").resize((w, h), how), dtype=F32)
    return np.dstack([resize(a[..., i], shape, how) for i in range(a.shape[2])])


def blur(a, sigma):
    """Gaussian blur of a float array, any sigma, by multiplying in the frequency domain."""
    if sigma <= 0:
        return a
    if a.ndim == 3:
        return np.dstack([blur(a[..., i], sigma) for i in range(a.shape[2])])
    pad = int(min(3 * sigma + 1, min(a.shape) - 1))
    p = np.pad(a, pad, mode="reflect")
    fy = np.fft.fftfreq(p.shape[0])[:, None]
    fx = np.fft.rfftfreq(p.shape[1])[None, :]
    gain = np.exp(-2 * (math.pi * sigma) ** 2 * (fx * fx + fy * fy))
    out = np.fft.irfft2(np.fft.rfft2(p) * gain, s=p.shape)
    return out[pad:pad + a.shape[0], pad:pad + a.shape[1]].astype(F32)


def sample(a, x, y):
    """Read a float array at fractional places (bilinear). Places outside are clamped to the edge."""
    h, w = a.shape[:2]
    x = np.clip(x, 0, w - 1.001)
    y = np.clip(y, 0, h - 1.001)
    x0 = np.floor(x).astype(np.intp)
    y0 = np.floor(y).astype(np.intp)
    fx = (x - x0).astype(F32)
    fy = (y - y0).astype(F32)
    if a.ndim == 3:
        fx = fx[..., None]
        fy = fy[..., None]
    top = a[y0, x0] * (1 - fx) + a[y0, x0 + 1] * fx
    bottom = a[y0 + 1, x0] * (1 - fx) + a[y0 + 1, x0 + 1] * fx
    return top * (1 - fy) + bottom * fy


# ---------------------------------------------------------------- noise
def noise(shape, cell, seed, octaves=5, gain=0.5):
    """Cloudy noise, 0 to 1. `cell` is the size in pixels of the largest blobs: a number, or (across, down)
    for stretched noise. Each octave halves the size and takes `gain` of the weight."""
    h, w = shape
    cx, cy = (cell, cell) if np.isscalar(cell) else cell
    rng = np.random.default_rng(seed)
    total = np.zeros(shape, dtype=F32)
    weight, norm = 1.0, 0.0
    for _ in range(octaves):
        gw, gh = int(math.ceil(w / cx)) + 3, int(math.ceil(h / cy)) + 3
        lattice = rng.random((gh, gw), dtype=F32)
        big = resize(lattice, (int(round(gh * cy)), int(round(gw * cx))))
        oy, ox = int(cy), int(cx)                      # start one cell in, away from the lattice edge
        total += weight * big[oy:oy + h, ox:ox + w]
        norm += weight
        weight *= gain
        cx, cy = max(cx / 2, 1.0), max(cy / 2, 1.0)
    out = total / norm
    lo, hi = np.percentile(out, (0.5, 99.5))
    return np.clip((out - lo) / (hi - lo + 1e-9), 0, 1).astype(F32)


def warp(a, amount, cell, seed):
    """Push a picture or mask about by a noise field, so straight things become hand-made."""
    h, w = a.shape[:2]
    x, y = grid((h, w))
    dx = (noise((h, w), cell, seed, 3) - 0.5) * 2 * amount
    dy = (noise((h, w), cell, seed + 1, 3) - 0.5) * 2 * amount
    return sample(a, x + dx, y + dy)


# ---------------------------------------------------------------- shapes
def mask_poly(shape, points, soft=0.0, wobble=0.0, seed=0, ss=3):
    """A filled polygon as a mask. `soft` blurs its edge; `wobble` makes the edge wander by that many pixels."""
    h, w = shape
    im = Image.new("L", (w * ss, h * ss), 0)
    ImageDraw.Draw(im).polygon([(float(x) * ss, float(y) * ss) for x, y in points], fill=255)
    m = np.asarray(im.resize((w, h), Image.BOX), dtype=F32) / 255
    if wobble:
        m = warp(m, wobble, max(8.0, wobble * 6), seed)
    if soft:
        m = blur(m, soft)
    return np.clip(m, 0, 1)


def mask_ellipse(shape, cx, cy, rx, ry, soft=0.0, wobble=0.0, seed=0):
    x, y = grid(shape)
    d = np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
    m = np.clip((1 - d) * min(rx, ry) + 0.5, 0, 1).astype(F32)
    if wobble:
        m = warp(m, wobble, max(8.0, wobble * 6), seed)
    if soft:
        m = blur(m, soft)
    return np.clip(m, 0, 1)


def mask_line(shape, points, width, soft=0.0, ss=3):
    """A line through the points, `width` pixels wide (a number, or one per point for a tapering line)."""
    h, w = shape
    im = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(im)
    widths = [width] * len(points) if np.isscalar(width) else list(width)
    for (a, b, wa, wb) in zip(points[:-1], points[1:], widths[:-1], widths[1:]):
        wd = max(1, int(round((wa + wb) / 2 * ss)))
        d.line([a[0] * ss, a[1] * ss, b[0] * ss, b[1] * ss], fill=255, width=wd)
        r = wd / 2
        for px, py in (a, b):
            d.ellipse([px * ss - r, py * ss - r, px * ss + r, py * ss + r], fill=255)
    m = np.asarray(im.resize((w, h), Image.BOX), dtype=F32) / 255
    return np.clip(blur(m, soft) if soft else m, 0, 1)


def curve(points, steps=24):
    """A smooth curve through a few points (Catmull-Rom), as a list of points."""
    p = [np.asarray(q, dtype=float) for q in points]
    p = [p[0] * 2 - p[1]] + p + [p[-1] * 2 - p[-2]]
    out = []
    for i in range(1, len(p) - 2):
        for s in range(steps):
            t = s / steps
            q = 0.5 * ((2 * p[i]) + (-p[i - 1] + p[i + 1]) * t + (2 * p[i - 1] - 5 * p[i] + 4 * p[i + 1] - p[i + 2]) * t * t
                       + (-p[i - 1] + 3 * p[i] - 3 * p[i + 1] + p[i + 2]) * t ** 3)
            out.append((float(q[0]), float(q[1])))
    out.append((float(p[-2][0]), float(p[-2][1])))
    return out


class Sheet:
    """A clear sheet to draw many small strokes on quickly (leaves, planks, wires, lettering), which is then
    laid over the picture in one go. Colors are '#hex' or rgb; sizes are in picture pixels."""

    def __init__(self, shape, ss=3):
        self.shape, self.ss = shape, ss
        h, w = shape
        self.im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    @staticmethod
    def _fill(color, alpha=1.0):
        c = rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
        return tuple(int(v) for v in np.clip(c * 255 + 0.5, 0, 255)) + (int(alpha * 255),)

    def line(self, points, color, width=1.0, alpha=1.0, round_ends=True):
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        wd = max(1, int(round(width * s)))
        fill = self._fill(color, alpha)
        self.d.line(pts, fill=fill, width=wd, joint="curve")
        if round_ends and wd > 2:
            r = wd / 2
            for px, py in (pts[0], pts[-1]):
                self.d.ellipse([px - r, py - r, px + r, py + r], fill=fill)
        return self

    def taper(self, points, color, w0, w1, alpha=1.0):
        """A line that changes width along its length (a trunk, a frond, a brush mark)."""
        n = len(points)
        for i in range(n - 1):
            wd = lerp(w0, w1, i / max(n - 2, 1))
            self.line([points[i], points[i + 1]], color, wd, alpha)
        return self

    def poly(self, points, color, alpha=1.0):
        s = self.ss
        self.d.polygon([(float(x) * s, float(y) * s) for x, y in points], fill=self._fill(color, alpha))
        return self

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0):
        s = self.ss
        self.d.ellipse([(cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s], fill=self._fill(color, alpha))
        return self

    def clear(self, points):
        """Wipe the sheet inside a polygon: whatever was drawn there is gone, and the picture under it will show."""
        s = self.ss
        self.d.polygon([(float(x) * s, float(y) * s) for x, y in points], fill=(0, 0, 0, 0))
        return self

    def done(self):
        """-> (color picture, coverage mask) at picture size."""
        h, w = self.shape
        a = np.asarray(self.im.resize((w, h), Image.BOX), dtype=F32) / 255
        return a[..., :3].astype(F32), a[..., 3].astype(F32)      # (Pillow keeps the colors true where the sheet is half covered)

    def onto(self, picture, amount=1.0):
        color, alpha = self.done()
        return over(picture, color, alpha * amount)


def over(picture, color, mask):
    """Lay color over the picture through a mask. `color` is one color or a whole picture."""
    color = rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
    m = mask[..., None]
    picture[...] = picture * (1 - m) + color * m
    return picture


def tint(picture, color, mask):
    """Multiply the picture toward a color through a mask: for shadows and glazes."""
    color = rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
    m = mask[..., None]
    picture[...] = picture * (1 - m) + picture * color * m
    return picture


def glow(picture, color, mask):
    """Add light through a mask (screen blend): for lamps, haze, sun on dust."""
    color = rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
    m = mask[..., None]
    picture[...] = 1 - (1 - picture) * (1 - color * m)
    return picture


def vary(color, shape, seed, amount=0.06, cell=40, warm=0.0):
    """One color turned into a patchy field of it, as a brush leaves: lighter and darker, a little warmer and cooler."""
    color = rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
    n = noise(shape, cell, seed, 4) - 0.5
    out = np.clip(color[None, None, :] * (1 + 2 * amount * n[..., None]), 0, 1).astype(F32)
    if warm:
        k = (noise(shape, cell * 1.7, seed + 7, 3) - 0.5) * 2 * warm
        out[..., 0] = np.clip(out[..., 0] + k, 0, 1)
        out[..., 2] = np.clip(out[..., 2] - k, 0, 1)
    return out


# ---------------------------------------------------------------- the brush
def strokes(ref, sizes=(16, 8, 4), seed=1, density=1.6, jitter=0.035, flow=None, keep=0.0, detail=None):
    """Repaint a picture with brush strokes, largest brush first.

    Each stroke takes its color from the (slightly blurred) picture under its middle and lies along the
    edges it finds there; where the picture is flat it follows `flow`, an angle field in radians (or
    lies level). Smaller brushes only go where the painting so far is still wrong, which is where the
    detail is. `detail` is an optional mask of places that must be reached by the smallest brush.
    `keep` mixes that much of the untouched picture back in at the end.
    """
    h, w, _ = ref.shape
    rng = np.random.default_rng(seed)
    ss = 2
    under = np.clip(blur(ref, sizes[0] * 0.45), 0, 1)
    canvas = Image.fromarray((under * 255).astype(np.uint8)).resize((w * ss, h * ss), Image.BICUBIC)
    draw = ImageDraw.Draw(canvas)
    lum = ref @ np.array([0.3, 0.55, 0.15], dtype=F32)
    for r in sizes:
        src = np.clip(blur(ref, r * 0.3), 0, 1)
        gy, gx = np.gradient(blur(lum, max(1.0, r * 0.35)))
        along = np.arctan2(gy, gx) + math.pi / 2
        strong = np.hypot(gx, gy)
        n = int(w * h / (r * r) * density)
        xs = rng.integers(0, w, n)
        ys = rng.integers(0, h, n)
        if r != sizes[0]:
            now = np.asarray(canvas.resize((w, h), Image.BOX), dtype=F32) / 255
            wrong = np.abs(now - src).sum(axis=2)
            if detail is not None and r == sizes[-1]:
                wrong = np.maximum(wrong, detail * 0.2)
            want = wrong[ys, xs] > (0.05 if r > sizes[-1] else 0.035)
            xs, ys = xs[want], ys[want]
        level = np.zeros((h, w), dtype=F32) if flow is None else flow
        for x, y in zip(xs.tolist(), ys.tolist()):
            a = along[y, x] if strong[y, x] > 0.004 else level[y, x] + rng.normal(0, 0.25)
            length = r * (1.2 + 2.2 * rng.random())
            dx, dy = math.cos(a) * length / 2, math.sin(a) * length / 2
            c = src[y, x] * (1 + rng.normal(0, jitter)) + rng.normal(0, jitter * 0.4, 3)
            fill = tuple(int(v) for v in np.clip(c * 255, 0, 255))
            wd = max(1, int(r * ss * (0.75 + 0.5 * rng.random())))
            x0, y0, x1, y1 = (x - dx) * ss, (y - dy) * ss, (x + dx) * ss, (y + dy) * ss
            draw.line([x0, y0, x1, y1], fill=fill, width=wd)
            e = wd / 2
            draw.ellipse([x0 - e, y0 - e, x0 + e, y0 + e], fill=fill)
            draw.ellipse([x1 - e, y1 - e, x1 + e, y1 + e], fill=fill)
    out = np.asarray(canvas.resize((w, h), Image.BOX), dtype=F32) / 255
    return lerp(out, ref, keep) if keep else out


# ---------------------------------------------------------------- finishing: grain and the palette
def grain(picture, seed, amount=0.022):
    """Pigment grain: fine light-and-dark speckle, a little coarser in places."""
    h, w, _ = picture.shape
    rng = np.random.default_rng(seed)
    fine = rng.normal(0, 1, (h, w)).astype(F32)
    coarse = blur(rng.normal(0, 1, (h, w)).astype(F32), 0.8) * 1.6
    return np.clip(picture + ((fine * 0.7 + coarse * 0.6) * amount)[..., None], 0, 1)


def palette_of(pictures, colors=160, seed=3, rounds=12):
    """Choose a palette for one or more pictures (k-means on a sample of their pixels)."""
    rng = np.random.default_rng(seed)
    px = np.concatenate([p.reshape(-1, p.shape[-1])[:, :3] for p in pictures])
    px = px[rng.choice(len(px), size=min(len(px), 60000), replace=False)].astype(F32)
    centers = px[rng.choice(len(px), size=colors, replace=False)].copy()
    for _ in range(rounds):
        d = ((px[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        nearest = d.argmin(axis=1)
        for k in range(colors):
            mine = px[nearest == k]
            centers[k] = mine.mean(axis=0) if len(mine) else px[rng.integers(len(px))]
    return centers


def to_palette(picture, palette, seed=5, speckle=0.016):
    """Reduce a picture to the palette. A little noise first, so neighbouring palette colors mingle
    in a speckle (as a scanned painting does) instead of forming bands. Returns palette indexes."""
    h, w, _ = picture.shape
    rng = np.random.default_rng(seed)
    noisy = picture + rng.normal(0, speckle, (h, w, 1)).astype(F32) + rng.normal(0, speckle * 0.35, (h, w, 3)).astype(F32)
    flat = noisy.reshape(-1, 3)
    index = np.empty(len(flat), dtype=np.uint8)
    for start in range(0, len(flat), 40000):
        part = flat[start:start + 40000]
        index[start:start + 40000] = ((part[:, None, :] - palette[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
    return index.reshape(h, w)


def save(path, index, palette, alpha=None):
    """Write a palette picture as a PNG. With `alpha` (a mask), everything under half is transparent."""
    pal = np.clip(palette * 255 + 0.5, 0, 255).astype(np.uint8)
    if alpha is None:
        im = Image.fromarray(index, "P")
        im.putpalette(pal.tobytes())
        im.save(path, optimize=True)
        return
    clear = len(pal)                                     # one more palette entry, for "nothing here"
    idx = index.copy()
    idx[alpha < 0.5] = clear
    im = Image.fromarray(idx, "P")
    im.putpalette(pal.tobytes() + bytes(3))
    im.save(path, optimize=True, transparency=clear)


def show(index, palette):
    """Palette picture back to floats, for looking at."""
    return palette[index]

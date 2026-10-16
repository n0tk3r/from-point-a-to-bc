"""The world outside the limousine (nevada_limo_drive.py, DRIVE-16P): the numbers every part shares, and the tools for
pictures that loop end to end.

THE CAMERA AND THE ROAD (DRIVE-16, fixed for the engine and the painter). The scene's camera is level, its horizon the
stage's row 220, its vanishing point (424, 220), its focal length 345 pixels, the eye 1.83 m above the road. A point X m
out to one side of the line of travel, z m ahead and Y m up is on the stage at x = 424 -/+ 345 X / z (left/right),
y = 220 + 345 (1.83 - Y) / z. On the left: the yellow centre line 4.3 m out, the oncoming lane to its white edge line
at 8.0 m (15 cm wide), gravel to 9.6 m, then the desert; on the right: the edge line at 2.6 m, the shoulder to 4.5 m,
a wire fence about 9.5 m out and telephone poles about 14 m out. The panes see the ground from about 7.4 m out on the
left and 6.8 m on the right; the top of the glass sees 18 cm above the eye at the wall, so 3.3 m up at 14 m out.

THE LIGHT. The same morning as the roadside, a few miles on: the sun low on the RIGHT of the car and a little behind
it, about 27 degrees up. A thing 1 m tall throws its shadow 1.95 m to the car's LEFT and 0.36 m forward (the
roadside's SUN, its camera looking down the road). So through the windows on BOTH sides the light comes from the
screen's right and every shadow falls to the screen's left: on the left the things are lit from behind our shoulder
(their faces in the sun, a sliver of shade on their left), on the right we look toward the sun's side of the sky (their
faces in shade, a bright rim on their right).

THE GLASS. Everything here is seen through the limousine's smoked windows: each picture is painted in the roadside's
colours and then smoked, darker and bluer (SMOKE), as desert-strip.png was.

SEAMLESS. Every picture but the sky repeats along the road: noise is made periodic (pnoise), things are drawn at x and
a picture's width either side (wrap), the brush pass is laid over a wrapped copy and its seam blended (brush_wrapped),
and the grain is periodic too (pgrain)."""

import math

import numpy as np
from PIL import Image

from brush import F32, blur, lerp, palette_of, rgb, save, strokes, to_palette

# ---------------------------------------------------------------- the camera (the scene's, layout.json `view`)
HZ, VX, FOCAL, EYE = 220.0, 424.0, 345.0, 1.83
W, H = 800, 600

# ---------------------------------------------------------------- the road, metres out from the line of travel
LEFT = dict(centre=4.3, edge=8.0, line_w=0.15, gravel=9.6, sees=7.4)
RIGHT = dict(edge=2.6, shoulder=4.5, fence=9.5, poles=14.0, sees=6.8)

# ---------------------------------------------------------------- the pictures' own scales (the contract's numbers)
GROUND_W, GROUND_H, GROUND_PPM, GROUND_FROM = 1024, 512, 16.0, 6.0      # 64 m along the road, 6 m to 38 m out
THINGS_PPM = 24.0
BANDS = {   # file: (width, height, ppm, the distance out it is painted for). The far right is nearer (lower hills).
    "far-l": (2400, 48, 0.07, 6000.0),
    "far-r": (2400, 48, 0.14, 3000.0),
    "mid-l": (2400, 40, 0.5, 850.0),
    "mid-r": (2400, 40, 0.5, 850.0),
}

# ---------------------------------------------------------------- light, air and glass
SUN_EL = math.degrees(math.atan(1.0 / math.hypot(1.95, 0.36)))           # about 26.8 degrees
SHADOW_LEFT, SHADOW_FWD = 1.95, 0.36                                     # per metre of height: to the car's left, forward
SMOKE = np.array([0.80, 0.84, 0.95], dtype=F32)                          # smoked glass: darker, and bluer
AIR = "#e4e2ec"                                                          # the colour of far air, before the glass


def smoke(pic):
    return np.clip(pic * SMOKE[None, None, :], 0, 1).astype(F32)


def smoked(color):
    """A '#hex' colour as it looks through the glass, as '#hex'."""
    c = np.clip(rgb(color) * SMOKE, 0, 1)
    return "#%02x%02x%02x" % tuple(int(v * 255 + 0.5) for v in c)


def haze_amount(d, half):
    """How much of the air lies over something d metres away, when `half` metres covers half (1 - 2^(-d/half))."""
    return 1.0 - np.power(0.5, np.asarray(d, dtype=F32) / float(half))


# ---------------------------------------------------------------- noise that repeats across
def _cubic(t):
    t2, t3 = t * t, t * t * t
    return ((-t3 + 2 * t2 - t) * 0.5, (3 * t3 - 5 * t2 + 2) * 0.5, (-3 * t3 + 4 * t2 + t) * 0.5, (t3 - t2) * 0.5)


def pnoise(shape, cell, seed, octaves=4, gain=0.5, normalise=True):
    """Cloudy noise, 0 to 1, as brush.noise makes it, but repeating exactly every shape[1] pixels across: each octave
    is a lattice a whole number of cells wide, read round its end. `cell` is a size or (across, down)."""
    h, w = shape
    cx, cy = (cell, cell) if np.isscalar(cell) else cell
    rng = np.random.default_rng(seed)
    total = np.zeros(shape, dtype=F32)
    weight, norm = 1.0, 0.0
    for _ in range(octaves):
        nx = max(2, int(round(w / cx)))
        ny = max(1, int(math.ceil(h / cy)))
        lat = rng.random((ny + 3, nx), dtype=F32)
        v = np.arange(h, dtype=F32) / max(cy, 1e-6) + 1.0
        ry = np.floor(v).astype(np.intp)
        wy = _cubic((v - ry).astype(F32))
        rows = sum(wy[k][:, None] * lat[np.clip(ry + k - 1, 0, ny + 2)] for k in range(4))          # (h, nx)
        u = np.arange(w, dtype=F32) * nx / w
        rx = np.floor(u).astype(np.intp)
        wx = _cubic((u - rx).astype(F32))
        total += weight * sum(rows[:, (rx + k - 1) % nx] * wx[k][None, :] for k in range(4))
        norm += weight
        weight *= gain
        cx, cy = max(cx / 2, 1.0), max(cy / 2, 1.0)
    out = total / norm
    if not normalise:
        return out.astype(F32)
    lo, hi = np.percentile(out, (0.5, 99.5))
    return np.clip((out - lo) / (hi - lo + 1e-9), 0, 1).astype(F32)


def pwave(w, cycles, phase=0.0):
    """A sine that goes round a whole number of times across w pixels: for meanders that meet at the seam."""
    x = np.arange(w, dtype=F32)
    return np.sin(x / w * 2 * np.pi * int(cycles) + phase).astype(F32)


def pblur(a, sigma):
    """A Gaussian blur that wraps round across (the picture repeats) and mirrors at the top and bottom."""
    if sigma <= 0:
        return a
    if a.ndim == 3:
        return np.dstack([pblur(a[..., i], sigma) for i in range(a.shape[2])])
    pad = int(min(3 * sigma + 1, a.shape[0] - 1))
    p = np.pad(a, ((pad, pad), (0, 0)), mode="reflect")
    fy = np.fft.fftfreq(p.shape[0])[:, None]
    fx = np.fft.rfftfreq(p.shape[1])[None, :]
    gain = np.exp(-2 * (math.pi * sigma) ** 2 * (fx * fx + fy * fy))
    out = np.fft.irfft2(np.fft.rfft2(p) * gain, s=p.shape)
    return out[pad:pad + a.shape[0]].astype(F32)


def wrap(x, w, pad=60.0):
    """A thing's x and its copies a picture's width away, those that can show (the picture repeats)."""
    return [x + d for d in (-w, 0.0, w) if -pad < x + d < w + pad]


def brush_wrapped(pic, sizes=(7, 4, 2), seed=1, density=1.6, jitter=0.03, keep=0.42, margin=160, blend=48, flow=None):
    """brush.strokes over a picture that repeats across: painted on a copy with a margin of each end on the other, and
    the strokes that cross the seam blended, so the picture still runs on into itself."""
    h, w, _ = pic.shape
    m = min(margin, w // 2)
    ext = np.concatenate([pic[:, -m:], pic, pic[:, :m]], axis=1)
    fl = None if flow is None else np.concatenate([flow[:, -m:], flow, flow[:, :m]], axis=1)
    st = strokes(ext, sizes=sizes, seed=seed, density=density, jitter=jitter, keep=keep, flow=fl)
    out = st[:, m:m + w].copy()
    t = (np.arange(blend, dtype=F32) / blend)[None, :, None]
    out[:, :blend] = st[:, m + w:m + w + blend] * (1 - t) + st[:, m:m + blend] * t
    return out.astype(F32)


def pgrain(pic, seed, amount=0.016):
    """Pigment grain (brush.grain), its coarse part blurred round the seam."""
    h, w, _ = pic.shape
    rng = np.random.default_rng(seed)
    fine = rng.normal(0, 1, (h, w)).astype(F32)
    coarse = pblur(rng.normal(0, 1, (h, w)).astype(F32), 0.8) * 1.6
    return np.clip(pic + ((fine * 0.7 + coarse * 0.6) * amount)[..., None], 0, 1).astype(F32)


def finish(pic, seed, colors, alpha=None, grain=0.016, speckle=0.010, extra=None, where=None):
    """Grain, then a palette of `colors` chosen from the painted pixels (those under `alpha`, if given; `extra`: more
    pixels that must keep their colours, counted again), then the speckle. `where` (0 to 1 a pixel) says how much grain
    and speckle each pixel takes: none where the picture is never seen, or only ever seen averaged (they would only
    cost bytes there). -> (indexes, palette)."""
    if where is None:
        g = pgrain(pic, seed, grain)
    else:
        g = np.clip(pic + (pgrain(pic, seed, grain) - pic) * where[..., None], 0, 1).astype(F32)
    px = g.reshape(-1, 3) if alpha is None else g[alpha >= 0.5]
    if extra is not None and len(extra):
        px = np.concatenate([px, np.asarray(extra, F32).reshape(-1, 3)])
    pal = palette_of([px.reshape(-1, 1, 3)], colors=colors, seed=seed % 97 + 3)
    if where is None:
        idx = to_palette(g, pal, seed=seed + 1, speckle=speckle)
    else:
        idx = to_palette_where(g, pal, seed + 1, speckle * where)
    return idx, pal


def to_palette_where(picture, palette, seed, speckle):
    """brush.to_palette with the speckle given pixel by pixel."""
    h, w, _ = picture.shape
    rng = np.random.default_rng(seed)
    sp = np.asarray(speckle, F32)[..., None]
    noisy = picture + rng.normal(0, 1, (h, w, 1)).astype(F32) * sp + rng.normal(0, 0.35, (h, w, 3)).astype(F32) * sp
    flat = noisy.reshape(-1, 3)
    index = np.empty(len(flat), dtype=np.uint8)
    for start in range(0, len(flat), 40000):
        part = flat[start:start + 40000]
        index[start:start + 40000] = ((part[:, None, :] - palette[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
    return index.reshape(h, w)


def write(path, idx, pal, alpha=None):
    save(path, idx, pal, alpha)
    return path


def seam(pic):
    """How different a picture's last column is from its first, against neighbouring columns anywhere (no worse)."""
    a = np.asarray(pic, F32)
    return float(np.abs(a[:, -1] - a[:, 0]).mean()), float(np.abs(a[:, 1:] - a[:, :-1]).mean())


def to_u8(pic):
    return (np.clip(pic, 0, 1) * 255 + 0.5).astype(np.uint8)


def look(path, pic, k=1, alpha=None, under="#7f8a9a"):
    """Save a float picture to look at (enlarged k times, hard pixels), clear parts on a plain colour."""
    p = np.asarray(pic, F32)
    if alpha is not None:
        p = lerp(rgb(under)[None, None, :], p, (np.asarray(alpha) >= 0.5)[..., None].astype(F32))
    im = Image.fromarray(to_u8(p))
    if k != 1:
        im = im.resize((im.width * k, im.height * k), Image.NEAREST)
    im.save(path)
    return path

"""Himeji town (edo-town): Watamachi on the Saigoku-kaido at midday, about 29 April 1830. The measurements, the camera,
the light and the colours its scripts share, and the small tools PAINT-21E's three scenes use (edo_shosha.py and
edo_lock.py import them from here). PAINT-21E, round twenty-one.

PLAN
  Light     Midday, the sun high in the south, behind us and a little to our left (about 68 degrees up): the house
            fronts face us and are in full light; the deep eaves throw a hard band of shade across the top of every
            front; shadows on the ground are short and fall away from us, a little to the right. The shade is the
            act's blue (cobalt toward ultramarine), never grey.
  Depth     The land camera: horizon 290, full 590 (persp.Camera: the lens 3.28 m above the street, level, focal 800),
            the vanishing point of everything running straight back in the middle of O-Tane's side yard (x 444.5),
            so that the yard is seen straight down to the kitchen at its back. The far side's fronts stand on row
            450 (16.4 m from the lens; a grown-up 85 px there, Mom 80).
  Plan      We stand in the highway (the Saigoku-kaido), broad packed earth, looking north across it. The far side's
            fronts, left to right: the domain's cotton office (two storeys, cut by the frame: its wide doorway, its
            noren, bales of white cloth going in) and the paper-note office beside it; the writing school (its
            shutters propped open: the raised floor, the low desks); O-Tane's side yard, open to the street, and at
            its back the kitchen lean-to facing us with the well before it; O-Tane's house (a weaver's house: a
            lattice front, an indigo noren); Tobei's hut; the ward gate across the lane that runs north to the castle.
            Above the roofs, far up on its hill, the keep (PAINT-20D's drawing, smaller).
  Tones     LIGHT  the keep, the plaster of the upper storeys, the bales, the sky low down, the sunlit street.
            DARK   the tiled roofs, the open school's inside, the side yard's shade, the noren, the gate's posts.
            MIDDLE the sky's blue, the wood of the fronts, the street, the hill.
            The eye comes in along the street to O-Kiku at the school door and the open side yard, and goes up past
            the roofs to the keep.

Everything in centimetres in the world (X across, right positive, 0 on the line of sight; Y up from the street; D the
distance from the lens), drawn in picture pixels through P()."""

import math
import os

import numpy as np
from PIL import Image

from brush import F32, rgb, lerp, Sheet, warp, curve, over, blur, grain, palette_of, to_palette, save, strokes
from rome_steps_kit import Canvas

W, H = 800, 600
SHAPE = (H, W)
HZ, FULL = 290, 590
FOC = 800.0
VX = 444.5                                                   # the middle of O-Tane's side yard: it is seen straight down
S0 = 160.0 / 175.0                                           # picture pixels per cm at the full row
EYE = (FULL - HZ) / S0                                       # 328.1 cm: the lens above the street
OUT = "out/edo-town"


def P(X, Y, D):
    """A place in the world (cm across, cm up, cm from the lens) -> the picture."""
    k = FOC / D
    return (VX + X * k, HZ + (EYE - Y) * k)


def k_at(D):
    """Picture pixels per cm at a distance D."""
    return FOC / D


def D_row(y):
    """How far off the street is at a picture row (cm from the lens)."""
    return EYE * FOC / max(y - HZ, 0.5)


def row_D(D):
    return HZ + EYE * FOC / D


def scale_at(y):
    """The game's size for a person with feet on row y (1 at full)."""
    return (y - HZ) / (FULL - HZ)


def X_at(px, D):
    return (px - VX) * D / FOC


# ---------------------------------------------------------------- the paint box (by name, as the key mixes them)
PAINT = dict(white="#f6eed8", prussian="#1a2846", ultra="#2e3a93", cobalt="#2f63b8", cerulean="#7fb8de", naples="#f4d88e",
             veronese="#9ac77f", viridian="#1e7461", ochre="#d8963a", sienna="#8c3b20", lake="#c9375e", vermilion="#d63f2a",
             orange="#e9772b", chrome="#f2b42e", lilac="#b8a2d8")             # (postimp_paints.PAINTS: chrome-orange, chrome-yellow, lilac)


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


def mix(a, b, t):
    return col(a) + (col(b) - col(a)) * t


PAPER = PAINT["white"]
LINE = PAINT["prussian"]


def shade_of(c, t=0.35):
    """The shade flat of a lit flat: pulled toward the key's blue shade (style.md section 5), never toward grey."""
    return mix(mix(c, PAINT["cobalt"], t), PAINT["prussian"], t * 0.35)


# the town's colours at midday (the box's, mixed by name)
C = dict(
    plaster=mix(PAPER, PAINT["naples"], 0.18), plaster_sh=shade_of(mix(PAPER, PAINT["naples"], 0.1), 0.42),
    wood=mix(PAINT["sienna"], PAINT["ochre"], 0.38), wood_lit=mix(PAINT["ochre"], PAINT["sienna"], 0.30), wood_dark=mix(PAINT["sienna"], PAINT["prussian"], 0.55),
    wood_old=mix(mix(PAINT["sienna"], PAINT["prussian"], 0.35), PAINT["ochre"], 0.2),
    tile=mix(PAINT["prussian"], "#6f7890", 0.42), tile_lit=mix("#6f7890", PAPER, 0.18), tile_edge=mix("#8c96ae", PAPER, 0.2), tile_deep=mix(PAINT["prussian"], "#000000", 0.15),
    street=mix(mix(PAINT["ochre"], PAPER, 0.55), PAINT["cobalt"], 0.10), street_lit=mix(mix(PAINT["ochre"], PAPER, 0.62), PAINT["naples"], 0.2),
    street_sh=shade_of(mix(PAINT["ochre"], PAPER, 0.5), 0.45), rut=mix(mix(PAINT["ochre"], PAPER, 0.4), PAINT["sienna"], 0.15),
    stone=mix(PAPER, PAINT["prussian"], 0.28), stone_lit=mix(PAPER, PAINT["prussian"], 0.14), stone_sh=mix(PAPER, PAINT["prussian"], 0.48),
    indigo=mix(PAINT["prussian"], PAINT["ultra"], 0.35), indigo_lit=mix(PAINT["ultra"], PAINT["cobalt"], 0.45),
    inside=mix(PAINT["prussian"], PAINT["sienna"], 0.25), inside_far=mix(PAINT["prussian"], PAINT["ultra"], 0.3),
    mat=mix(PAINT["naples"], PAINT["veronese"], 0.35), mat_sh=shade_of(mix(PAINT["naples"], PAINT["veronese"], 0.3), 0.4),
    straw=mix(PAINT["ochre"], PAINT["naples"], 0.45), straw_sh=mix(PAINT["ochre"], PAINT["sienna"], 0.35),
    cloth=mix(PAPER, PAINT["naples"], 0.08), cloth_sh=shade_of(PAPER, 0.3),
    pine=mix(PAINT["viridian"], PAINT["prussian"], 0.35), pine_lit=mix(PAINT["viridian"], PAINT["veronese"], 0.35), pine_far=mix(PAINT["viridian"], PAINT["cerulean"], 0.45),
    hill=mix(PAINT["viridian"], PAINT["cerulean"], 0.32), hill_lit=mix(PAINT["veronese"], PAINT["cerulean"], 0.35),
    cast=mix(PAINT["cobalt"], PAINT["ultra"], 0.35),
    bizen=mix(PAINT["sienna"], PAINT["prussian"], 0.25), bizen_lit=mix(PAINT["sienna"], PAINT["ochre"], 0.45),
    clay=mix(PAINT["ochre"], PAINT["sienna"], 0.55), iron=mix(PAINT["prussian"], "#3a3a40", 0.45),
    red=PAINT["vermilion"], line=LINE,
)


# ---------------------------------------------------------------- small tools (after edo_castle.py's: one hand for the act)
def hand(a, amount=1.0):
    """A hand does not rule its lines: push a picture or mask about a little (always the same push)."""
    return warp(warp(a, 0.5 * amount, 24, 5), 0.8 * amount, (140, 60), 6)


def sheet_layer(draw, amount=0.6, ss=3, shape=SHAPE):
    """Draw with a Sheet onto a clear Canvas, the edges pushed a little by hand. -> Canvas"""
    s = Sheet(shape, ss)
    draw(s)
    c, a = s.done()
    out = Canvas(shape)
    if amount:
        both = hand(np.dstack([c * a[..., None], a]), amount)
        out.c, out.a = both[..., :3].astype(F32), np.clip(both[..., 3], 0, 1).astype(F32)
    else:
        out.c, out.a = (c * a[..., None]).astype(F32), a
    return out


def outline(s, pts, width=1.0, alpha=0.6, close=True, color=LINE):
    """The keyblock's contour: a fine even prussian-blue line (style.md section 4)."""
    p = list(pts) + ([pts[0]] if close else [])
    s.line(p, color, width, alpha)


def eave(x0, x1, y, lift=3.0, n=14):
    """The line of a tiled eave: level in the middle, its corners lifted a little."""
    out = []
    cx, half = (x0 + x1) / 2, (x1 - x0) / 2
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        out.append((x, y - lift * (abs(x - cx) / half) ** 3.2))
    return out


def brushed(layer, ground_, seed, sizes=(6, 3, 2), keep=0.45, restate=0.7):
    """A cut-out, repainted with a small brush on the ground it stands against, then said again crisply.
    -> (colour, hard coverage)."""
    c, a = layer.straight()
    ys, xs = np.where(a > 0.02)
    if len(xs) == 0:
        return c, (a > 0.5).astype(F32)
    x0, x1, y0, y1 = max(0, xs.min() - 12), min(W, xs.max() + 13), max(0, ys.min() - 12), min(H, ys.max() + 13)
    flat = ground_[y0:y1, x0:x1].copy()
    over(flat, c[y0:y1, x0:x1], a[y0:y1, x0:x1])
    painted = strokes(flat, sizes=sizes, seed=seed, density=1.8, jitter=0.025, keep=keep)
    painted = lerp(painted, flat, (restate * a[y0:y1, x0:x1])[..., None])
    out = c.copy()
    out[y0:y1, x0:x1] = painted
    return out, (a > 0.5).astype(F32)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.012, amount=0.016, palette=None):
    """A little grain, then a limited palette with speckle, written as a PNG-8. -> (file size, palette)"""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    n = len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0))
    pal = palette if palette is not None else palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, n)))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name), pal


def to_png(pic, path):
    Image.fromarray((np.clip(pic, 0, 1) * 255).astype(np.uint8)).save(path)


def pine(s, x, y, h, tone, lit, rng, pads=None):
    """A pine as the prints draw it: a bent dark trunk showing between flat layered pads, each a lens, narrower going
    up, its top edge toward the sun a shade lighter (after edo_castle.py's)."""
    bend = rng.uniform(-0.12, 0.12)
    trunk = [(x, y), (x + h * bend * 0.5, y - h * 0.45), (x + h * bend, y - h * 0.92)]
    s.line(trunk, mix(tone, "#000000", 0.35), max(0.9, h * 0.05))
    n = pads or (3 if h < 36 else 4)
    for j in range(n):
        f = (j + 0.9) / (n + 0.5)
        cx = x + h * bend * f + rng.uniform(-1, 1)
        cy = y - h * (0.28 + 0.66 * f)
        rx = h * (0.50 - 0.30 * f) * rng.uniform(0.85, 1.15)
        ry = max(2.0, rx * 0.24)
        top = [(cx - rx + 2 * rx * i / 10, cy - ry * (0.55 + 0.45 * math.sin(i / 10 * math.pi))) for i in range(11)]
        bottom = [(cx + rx - 2 * rx * i / 7, cy + ry * 0.45 * rng.uniform(0.4, 1.0)) for i in range(1, 7)]
        s.poly(top + bottom, tone)
        s.poly([(q[0], q[1]) for q in top[3:8]] + [(cx + rx * 0.2, cy - ry * 0.1)], lit, 0.55)


def bands(stops, y0, y1, seed=20, wobble=2.0, soft=2.4, shape=SHAPE, drift=0.10):
    """The graded sky as the prints print it (bokashi): flat bands of the stops, deepest first (row y0), their
    boundaries soft and a little wobbled (style.md section 3). -> picture"""
    from brush import grid, noise, ramp
    x, y = grid(shape)
    n = len(stops)
    dr = (noise(shape, (520, 260), seed, 3) - 0.5) * drift
    t = np.clip((y - y0) / max(1.0, (y1 - y0)) + dr, 0, 0.9999)
    tq = (np.floor(t * n) / max(1, n - 1)).astype(F32)
    tq = warp(blur(tq, soft), wobble, 40, seed + 3)
    pic = ramp(np.clip(tq, 0, 1), [(i / max(1, n - 1), c if isinstance(c, str) else tuple(float(v) for v in c)) for i, c in enumerate(stops)])
    pic *= (1 + (noise(shape, (300, 120), seed + 1, 4) - 0.5)[..., None] * 0.04)
    return np.clip(pic, 0, 1).astype(F32)


def poly_box(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def hull(mask, pad=2.0, most=18):
    """A clickable shape round a painted thing: its convex hull, grown by pad, at most `most` points."""
    from scipy.spatial import ConvexHull
    ys, xs = np.where(mask)
    pts = np.stack([xs, ys], axis=1).astype(float)
    pts = np.concatenate([pts, pts + [1, 0], pts + [0, 1], pts + [1, 1]])
    hv = pts[ConvexHull(pts).vertices]
    c = hv.mean(axis=0)
    hv = c + (hv - c) * (1 + pad / np.maximum(np.linalg.norm(hv - c, axis=1, keepdims=True), 1))
    while len(hv) > most:
        n = len(hv)
        areas = [abs((hv[(i + 1) % n] - hv[i])[0] * (hv[i - 1] - hv[i])[1] - (hv[(i + 1) % n] - hv[i])[1] * (hv[i - 1] - hv[i])[0]) for i in range(n)]
        hv = np.delete(hv, int(np.argmin(areas)), axis=0)
    return [[int(round(min(799, max(0, x)))), int(round(min(599, max(0, y))))] for x, y in hv]


def box_of(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return (0, 0, 0, 0)
    return (int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1))

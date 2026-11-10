"""Watercolour, for Act Six (round twenty-three; tools/paint/DEPTH.md, "Japan in watercolour").

The act's pictures were painted in the manner of woodblock prints: flat colour inside a key line. The author asked for
them "a little more watercolored". A print's colour is flat because it is pressed from a block; a watercolour's never
is, because it is laid wet on paper. What `wash` does to a finished painting, before the palette:

  wet in wet    where the scene says paint was laid wet (`soft`: sky, far land, mist, open water) edges bleed and feather
  blooms        no wash dries even: it is a little darker here, lighter there, warmer and cooler, with a back-run or two
  pooling       pigment gathers at the edge of a wash as it dries: a thin darker rim on the dark side of every edge
  granulation   pigment settles into the pits of the paper: a fine speckle, most in the darks and in the blues and earths
  paper         the paper shows through everything a little, and bare in flecks in the light, rough passages

Everything is seeded and laid by place: the same seed gives the same paper under every picture of a scene, so a cut-out
washed over the backdrop (`wash_cut`) matches the backdrop wherever they show the same thing.

    from watercolor import wash, wash_cut, soft_above
    back = wash(back, seed=SEED, soft=soft_above(SHAPE, HZ))            # the backdrop, just before the palette
    thing = wash_cut(thing_rgb, thing_alpha, back_before_wash, seed=SEED, soft=...)   # every cut-out, the same seed

Needs numpy and Pillow, as the rest of the kit.
"""

import numpy as np

from brush import F32, blur, grid, lerp, noise, rgb, step, warp

PAPER = rgb("#f6f0e1")                                      # cold-pressed paper, a little warm
_LUM = np.array([0.30, 0.55, 0.15], dtype=F32)


_FIELDS = {}


def _noise(shape, cell, seed, octaves=5, gain=0.5):
    """`brush.noise`, kept between calls: a scene washes its backdrop and every cut-out on the same paper, and the
    paper's fields are the same each time."""
    key = (shape, cell, seed, octaves, gain)
    if key not in _FIELDS:
        if len(_FIELDS) > 64:
            _FIELDS.clear()
        _FIELDS[key] = noise(shape, cell, seed, octaves, gain)
    return _FIELDS[key]


def lum(picture):
    return picture @ _LUM


def paper_grain(shape, seed=11):
    """The paper's tooth: small pits and bumps, 0 to 1 (0.5 is level)."""
    fine = _noise(shape, 3.2, seed, 2, 0.6)
    broad = _noise(shape, 9.0, seed + 1, 2, 0.5)
    return np.clip(0.65 * fine + 0.35 * broad, 0, 1).astype(F32)


def edges(picture, r=1.2, gain=9.0):
    """Where one colour meets another, 0 to 1."""
    L = blur(lum(picture), r)
    gy, gx = np.gradient(L)
    return np.clip(np.hypot(gx, gy) * gain, 0, 1).astype(F32)


def soft_above(shape, row, feather=24.0, below=0.0):
    """A `soft` mask: 1 above a row of the picture (the sky and the far land), fading out over `feather` rows; `below`
    is how wet everything under it stays (0: crisp)."""
    x, y = grid(shape)
    m = 1 - step(row - feather, row + feather, y)
    return np.clip(m + below * (1 - m), 0, 1).astype(F32)


def wash(picture, seed=1, amount=1.0, soft=None, keep=None, lift=0.07, wander=3.5, fleck=0.5):
    """A finished painting as a watercolour. `amount` scales everything (1.0 is the act's; 0.6 for a lamplit room,
    where the darks must stay deep). `soft`: a mask of what was laid wet in wet (0 to 1: how wet). `keep`: a mask of
    what must stay as painted (lettering to be read). `lift`: how much of the paper shows through everywhere.
    `wander`: how far wet paint moves, in pixels (3.5 as the pilot painted; 1.0 to 1.5 where thin far layers or
    straight far trunks must feather without bending or running together; 0 only feathers). `fleck`: the bare flecks
    of paper in light, rough passages (0.5; 0 for none: on a mid-tone roof they can read as litter)."""
    h, w, _ = picture.shape
    shape = (h, w)
    src = picture.astype(F32)
    out = src.copy()
    # wet in wet: the paint wanders a little and its edges feather
    if soft is not None and float(np.max(soft)) > 0:
        moved = warp(out, wander * amount, 22, seed + 1) if wander > 0 else out
        wet = blur(moved, 1.5 * amount)
        out = lerp(out, wet, np.clip(soft, 0, 1)[..., None]).astype(F32)
    L = lum(out)
    flat = 1 - np.clip(edges(src, 2.0) * 3, 0, 1)                        # 1 inside a wash, 0 at its edges
    # blooms: a wash is never even
    low = _noise(shape, 110, seed + 2, 3) - 0.5
    mid = _noise(shape, 34, seed + 3, 3) - 0.5
    out *= (1 + (0.075 * low + 0.045 * mid)[..., None] * amount)
    drift = (_noise(shape, 150, seed + 4, 2) - 0.5) * 0.035 * amount       # warmer here, cooler there
    out[..., 0] += drift
    out[..., 2] -= drift
    # back-runs: a thin dark line here and there, where a wet wash ran back into one that was drying
    b = _noise(shape, 70, seed + 5, 4)
    run = blur(np.exp(-((b - 0.5) / 0.016) ** 2), 1.3) * step(0.38, 0.66, _noise(shape, 200, seed + 6, 2))
    out *= (1 - 0.05 * amount * run * flat)[..., None]
    # pooling: a darker rim on the dark side of every edge
    Ls = blur(L, 0.8)
    pool = np.clip((blur(Ls, 2.6) - Ls) * 5.0, 0, 1) * np.clip(edges(src) * 2.5, 0, 1)
    out *= (1 - 0.30 * amount * pool)[..., None]
    # granulation: pigment in the pits of the paper
    g = paper_grain(shape, seed + 7) - 0.5
    dark = np.clip(1.15 - L * 1.1, 0.15, 1.0)
    blue = np.clip((out[..., 2] - out[..., 0]) * 2.0 + 0.6, 0.45, 1.3)
    out *= (1 - (g * 0.17 * amount * dark * blue)[..., None])
    # the paper: through everything a little, and bare in flecks where the light passages are rough
    out = lerp(out, PAPER[None, None, :], lift * amount)
    bare = step(0.80, 0.95, paper_grain(shape, seed + 8)) * step(0.55, 0.85, L) * fleck * amount
    out = lerp(out, PAPER[None, None, :], bare[..., None])
    out = np.clip(out, 0, 1)
    if keep is not None:
        out = lerp(out, src, np.clip(keep, 0, 1)[..., None])
    return out.astype(F32)


def wash_cut(color, alpha, back, seed=1, amount=1.0, soft=None, keep=None, lift=0.07, wander=3.5, fleck=0.5, crisp=False):
    """A cut-out washed as part of the picture it stands in: `color` and `alpha` are the cut-out as painted, `back` the
    backdrop as painted (before its own wash). Returns the cut-out's colours, washed on the same paper as the backdrop
    (same seed): lay them through the same `alpha`. `crisp=True` takes `soft` away under the cut-out itself and a
    little round it, so a thing standing in front of a wet passage (a boat on the bay) keeps its own edge and the
    backdrop does not bleed into it."""
    a = np.clip(alpha, 0, 1)[..., None]
    whole = back * (1 - a) + color * a
    if crisp and soft is not None:
        hard = np.clip(blur((np.asarray(alpha) > 0.3).astype(F32), 1.2) * 2, 0, 1)
        soft = soft * (1 - hard)
    return wash(whole, seed, amount, soft, keep, lift, wander, fleck)


def graded(shape, color, to, a, b, seed=0, wander=0.06):
    """A graded wash: `color` at the point `a` running to `to` at the point `b` (picture points), wandering a little as
    a brush-load does. -> a picture to lay through a mask. (The print's bokashi, laid wet.)"""
    color = rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
    to = rgb(to) if isinstance(to, str) else np.asarray(to, dtype=F32)
    x, y = grid(shape)
    ax, ay = a
    bx, by = b
    d = max((bx - ax) ** 2 + (by - ay) ** 2, 1e-6)
    t = ((x - ax) * (bx - ax) + (y - ay) * (by - ay)) / d
    t = np.clip(t + (noise(shape, 60, seed, 3) - 0.5) * 2 * wander, 0, 1)
    t = t * t * (3 - 2 * t)
    return lerp(color[None, None, :], to[None, None, :], t[..., None]).astype(F32)


def dry_brush(shape, seed, cell=(26, 2.4), cover=0.55):
    """A mask for a dragged, nearly dry brush: broken level streaks (water sparkle, old boards, thatch). Multiply a
    wash's mask by it."""
    n = noise(shape, cell, seed, 2)
    return step(1 - cover - 0.08, 1 - cover + 0.08, n).astype(F32)


if __name__ == "__main__":                                  # python3 watercolor.py in.png out.png [amount]: a picture washed, to look at
    import sys

    from PIL import Image

    src = np.asarray(Image.open(sys.argv[1]).convert("RGB"), dtype=F32) / 255
    amt = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    res = wash(src, seed=7, amount=amt, soft=soft_above(src.shape[:2], src.shape[0] * 0.48))
    Image.fromarray((res * 255 + 0.5).astype(np.uint8)).save(sys.argv[2])

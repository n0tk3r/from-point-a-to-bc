"""The desert going by the limousine's windows (nevada-limo): one long strip, seamless end to end.

    python3 nevada_limo_strip.py          writes out/nevada-limo/desert-strip.png and a look at it behind the panes
                                          (out/nevada-limo-work/strip-look.png, out/nevada-limo-work/strip-seam.png)

The game draws it behind the glass of each window, clipped to the pane's exact polygon (layout.json `windows`), its
bottom edge on the stage row `strip.row`, scrolling past (the engine's `strip` kind). So it is painted in STAGE rows:
its rows are the picture's rows from `strip.top` to `strip.row`, and the far desert's horizon lies on the row of the
eye (the scene's `horizon`, 220), as it does through any window of a car. Above it the morning sky, with the long flat
clouds of the roadside; on the horizon mesas far off; below it the plain coming toward us, sagebrush getting bigger, a
barbed-wire fence along the road with a post now and then (and stretches with none), a white reflector post or two;
and at the bottom the road's own edge rushing by, streaked. Painted with the roadside's colours (nevada_roadside.py
and its kit), then smoked a little, as seen through tinted glass: darker and bluer than the roadside.

SEAMLESS. Its right edge runs on into its left: every noise is made to repeat (a cross-fade over its last stretch),
every bush, post and mesa is drawn at x and at x minus and plus the width, and the brush pass is laid over a wrapped
copy and its seam blended, so the strip can be drawn round and round. It is a frame in the plan (keyed colour by
colour), an 8-bit picture, opaque."""

import math
import os
import sys

import numpy as np
from PIL import Image

from brush import F32, Sheet, blur, glow, grain, lerp, noise, over, palette_of, ramp, rgb, save, strokes, tint, to_palette, vary
from nevada_roadside_kit import sagebrush, tuft
from solid import mix

OUT = "out/nevada-limo"
WORK = "out/nevada-limo-work"
WD = 3200                     # long: at 90 px a second it comes round every 36 seconds
SEED = 47
HZ = 220                      # the stage row of the eye: the far horizon lies on it
SMOKE = np.array([0.80, 0.84, 0.95], dtype=F32)        # smoked glass: darker, and bluer


def rows():
    """(top, row): the stage rows the strip covers (from layout.json if the scene has been painted, else measured)."""
    import json
    p = f"{OUT}/layout.json"
    if os.path.exists(p):
        s = json.load(open(p))["strip"]
        return s["top"], s["row"]
    from nevada_limo_layout import strip_rows
    return strip_rows()


def pnoise(shape, cell, seed, octaves=4, k=360):
    """noise() that repeats every shape[1] pixels across: made wider, and its last stretch faded into its first."""
    h, w = shape
    b = noise((h, w + k), cell, seed, octaves)
    out = b[:, :w].copy()
    t = (np.arange(k, dtype=F32) / k)[None, :]
    out[:, :k] = b[:, w:w + k] * (1 - t) + b[:, :k] * t
    return out


def wrap_x(xs, w=WD, pad=300):
    """A thing's x and its copies a strip's width away, those that can show (so the strip repeats)."""
    return [x + d for x in ([xs] if np.isscalar(xs) else xs) for d in (-w, 0, w) if -pad < x + d < w + pad]


# ---------------------------------------------------------------- the under-painting
def sky(shape, top, seed):
    h, w = shape
    y = np.arange(h, dtype=F32)[:, None] + top                         # stage rows
    t = np.clip((y - top) / max(1.0, HZ - top), 0, 1)
    pic = ramp(np.broadcast_to(t, (h, w)), [(0.0, "#2c5cb0"), (0.35, "#3e80c8"), (0.62, "#6aa8dc"), (0.82, "#a8cee4"), (0.94, "#e4dccc"), (1.0, "#f4dcb8")])
    n = pnoise(shape, (420, 60), seed, 3) - 0.5
    pic = pic * (1 + n[..., None] * 0.05)
    # the long flat clouds of the morning: a few streaks, lit on top, violet underneath
    for i, (cy, thick, amt) in enumerate(((top + 18, 9.0, 0.9), (top + 36, 7.0, 0.75), (HZ - 22, 5.0, 0.6))):
        band = pnoise(shape, (260, 9), seed + 10 + i, 4)
        yy = (y - cy) / thick
        prof = np.exp(-yy * yy * 1.6) * np.broadcast_to(np.ones((1, w), F32), (h, w))
        m = np.clip((band - 0.52) * 3.2, 0, 1) * prof * amt
        lit = np.clip(-yy * 0.8 + 0.4, 0, 1)                             # the top of each cloud in the sun
        col = lerp(rgb("#9c9ccc")[None, None, :], rgb("#ffe0c0")[None, None, :], lit[..., None])
        pic = pic * (1 - m[..., None]) + col * m[..., None]
    return np.clip(pic, 0, 1).astype(F32)


MESAS = [   # middle x, half width at the base, height (px), flat top's share of the width, tone
    (220, 150, 22, 0.55, 0), (560, 60, 12, 0.4, 1), (980, 230, 26, 0.62, 2), (1420, 90, 15, 0.5, 1),
    (1760, 40, 9, 0.3, 0), (2140, 190, 21, 0.58, 2), (2600, 110, 17, 0.45, 1), (2950, 70, 11, 0.5, 0),
]
MESA_TONES = [("#8e86c0", "#eeac8e", "#ffd8b0"), ("#928ac2", "#f0b090", "#ffd8b0"), ("#867cba", "#eea684", "#ffd4a8")]


def mesas(pic, top, seed):
    """Far mesas standing on the horizon, as the roadside paints them: a flat cap catching the sun, under its rim a
    band of cliff (warm where it faces the sun, on the right; violet in shade) broken into buttresses, below that a
    talus slope spreading to the plain, hazy and violet; and a pale band of haze along their feet."""
    h, w = pic.shape[:2]
    rng = np.random.default_rng(seed)
    base = HZ - top
    xs = np.arange(w, dtype=F32)
    ridge = (np.sin(xs / w * 2 * np.pi * 3 + 0.7) * 2.2 + np.sin(xs / w * 2 * np.pi * 7 + 2.1) * 1.4 + np.sin(xs / w * 2 * np.pi * 17) * 0.7 + 3.6)
    y = np.arange(h, dtype=F32)[:, None]
    far = np.clip((y - (base - ridge[None, :])) + 0.5, 0, 1) * (y <= base + 1)
    over(pic, "#b8b0d8", (far * 0.85).astype(F32))                       # the far range: pale violet, low, all along
    for i, (mx, hw, ht, flat, tone) in enumerate(MESAS):
        shade, lit_, cap = MESA_TONES[tone]
        tw = hw * flat                                                   # the half width of the cap
        cliff = ht * 0.45                                                # the cliff band's height under the rim
        rim = base - ht
        for x0 in wrap_x(mx):
            sh = Sheet((h, w), ss=3)
            talus = [(x0 - hw, base + 1), (x0 - tw - ht * 0.6, rim + cliff + 1), (x0 + tw + ht * 0.6, rim + cliff + 1), (x0 + hw, base + 1)]
            sh.poly(talus, mix(shade, "#c8b8d8", 0.25))                  # the talus, hazy
            sh.poly([(x0 - tw - 2, rim + cliff + 1.5), (x0 - tw, rim), (x0 + tw, rim), (x0 + tw + 2, rim + cliff + 1.5)], shade)       # the cliff band
            bx = x0 - tw + rng.uniform(2, 8)
            while bx < x0 + tw - 3:                                      # buttresses, irregular: lit faces toward the sun, gullies between
                bw = rng.uniform(3, 11)
                warm = (bx - (x0 - tw)) / (2 * tw)                       # more of the sun toward the right-hand end
                if rng.random() < 0.75:
                    drop = cliff * rng.uniform(0.6, 1.0)
                    sh.poly([(bx, rim + 1), (bx + bw, rim + 1), (bx + bw * 0.75, rim + drop + 1), (bx + 0.6, rim + drop + 1)], lit_, 0.18 + 0.62 * warm ** 1.3)
                bx += bw + rng.uniform(2, 9)
            for j in range(int(tw // 14)):                                # notches in the rim
                nx = x0 - tw + rng.uniform(4, 2 * tw - 4)
                sh.poly([(nx - 1.5, rim - 0.2), (nx + 1.5, rim - 0.2), (nx, rim + rng.uniform(1.5, 3.5))], mix(shade, "#d8c8e0", 0.3))
            sh.poly([(x0 + tw - 3, rim + 0.5), (x0 + tw, rim), (x0 + tw + 2, rim + cliff + 1.5), (x0 + tw - 1, rim + cliff + 1.5)], lit_, 0.9)   # the sunward end
            sh.line([(x0 - tw, rim + 0.4), (x0 + tw, rim + 0.4)], cap, 1.0, 0.9)                            # the cap in the sun
            sh.line([(x0 - tw - ht * 0.5, rim + cliff + 1.4), (x0 + tw + ht * 0.5, rim + cliff + 1.4)], mix(shade, "#5a5090", 0.4), 0.8, 0.5)
            c, a = sh.done()
            over(pic, c, a)
    y = np.arange(h, dtype=F32)[:, None]
    hz = np.exp(-((y - base + 2) / 5.0) ** 2)
    over(pic, "#f2dccc", np.broadcast_to(hz * 0.40, (h, w)).astype(F32))
    return pic


def ground(pic, top, seed):
    """The plain from the horizon down toward the road: pale far off, warmer and deeper near, blotched."""
    h, w = pic.shape[:2]
    y = np.arange(h, dtype=F32)[:, None] + top
    g = np.clip((y - HZ) / max(1.0, (top + h) - HZ), 0, 1)
    below = (y >= HZ).astype(F32)
    col = ramp(np.broadcast_to(g ** 0.8, (h, w)), [(0.0, "#f4dcc6"), (0.35, "#ecc49c"), (0.7, "#d89a62"), (1.0, "#c07c48")])
    blot = pnoise((h, w), (260, 22), seed, 4) - 0.5
    fine = pnoise((h, w), (40, 6), seed + 1, 3) - 0.5
    col = col * (1 + blot[..., None] * 0.16 + fine[..., None] * 0.08 * g[..., None])
    k = (pnoise((h, w), (500, 80), seed + 2, 3) - 0.5) * 0.06
    col[..., 0] += k
    col[..., 2] -= k * 0.8
    m = np.broadcast_to(below, (h, w))
    pic[...] = pic * (1 - m[..., None]) + np.clip(col, 0, 1) * m[..., None]
    # drifts of paler packed sand and darker gravel, long and level
    d = pnoise((h, w), (340, 7), seed + 3, 3)
    over(pic, "#f6e4cc", (np.clip((d - 0.62) * 3.0, 0, 1) * m * 0.35 * (1 - g * 0.5)).astype(F32))
    tint(pic, "#a87c64", (np.clip((0.36 - d) * 3.0, 0, 1) * m * 0.30 * g).astype(F32))
    return pic


def road(pic, top, seed):
    """The road's own edge at the bottom: a gravel shoulder, the white edge line, the asphalt, all streaked by speed."""
    h, w = pic.shape[:2]
    y = np.arange(h, dtype=F32)[:, None] + top
    yb = top + h
    sh_top, line_y, asph = yb - 22, yb - 13, yb - 10
    streak = pnoise((h, w), (220, 1.2), seed, 3)
    gravel = np.clip((y - sh_top) / 4.0, 0, 1) * np.ones((1, w), F32)
    gcol = lerp(rgb("#b89474")[None, None, :], rgb("#8c7c78")[None, None, :], streak[..., None])
    pic[...] = pic * (1 - gravel[..., None]) + gcol * gravel[..., None]
    a = np.clip((y - asph) / 1.5, 0, 1) * np.ones((1, w), F32)
    acol = lerp(rgb("#6a6478")[None, None, :], rgb("#8a8498")[None, None, :], streak[..., None])
    pic[...] = pic * (1 - a[..., None]) + acol * a[..., None]
    ln = np.clip(1 - np.abs(y - line_y) / 1.6, 0, 1) * np.ones((1, w), F32)
    over(pic, "#f2eee2", (ln * (0.75 + 0.25 * streak)).astype(F32))
    return pic


# ---------------------------------------------------------------- the small crisp things
def scrub_and_fence(shape, top, seed):
    """Sagebrush and dry tufts over the plain (tiny far off, big near the road), the fence with its posts and wires,
    a white reflector post now and then. -> (colour, alpha) of one crisp sheet."""
    h, w = shape
    rng = np.random.default_rng(seed)
    sh = Sheet((h, w), ss=2)
    hz = HZ - top                                                        # (the sheet's rows are the strip's own: stage row minus top)
    near_y = h - 24                                                      # just above the shoulder
    # the bushes, far to near, so the near overlap the far
    items = []
    for i in range(1500):
        g = rng.random() ** 1.7                                          # most of them far off, where there is most plain to see
        yy = hz + 2 + g * (near_y - hz - 2)
        r = 0.6 + g * g * 9.0 + rng.normal(0, 0.25) * g * 2
        if r < 0.5:
            continue
        items.append((yy, rng.uniform(0, w), r, rng.integers(1 << 30), rng.random()))
    items.sort()
    for yy, x, r, sd, kind in items:
        for xx in wrap_x(x, w, pad=30):
            if r < 1.6:
                sh.line([(xx - r, yy - 0.3), (xx + r, yy - 0.3)], mix("#7e8a6c", "#a8ac8c", kind), max(0.6, r * 0.9), 0.85)
                sh.line([(xx - r * 1.6, yy + 0.5), (xx, yy + 0.5)], "#8f84ac", max(0.5, r * 0.4), 0.45)       # its shadow, to the left
            elif kind < 0.75:
                sh.ellipse(xx - r * 0.9, yy + r * 0.1, r * 1.5, max(0.6, r * 0.22), "#8a7ca4", 0.4)
                sagebrush(sh, xx, yy, r, int(sd) % 100000, tones=("#4a5244", "#6e7a62", "#9eaa8c", "#cfd4b4"), tall=0.8)
            else:
                tuft(sh, xx, yy, r * 0.9, int(sd) % 100000)
    # the fence along the road: stretches of it, a post every so often, two strands of wire
    fy = h - 44                                                          # the foot of the fence
    post_h = 30.0
    x = 80.0                                                             # (no post on the seam itself)
    posts = []
    while x < w - 120:
        run = rng.uniform(700, 1300)                                     # a stretch of fence, then none for a while
        gap = rng.uniform(260, 520)
        px = x
        while px < min(w - 60, x + run):
            posts.append((px, rng.normal(0, 0.06)))
            px += rng.uniform(150, 210)
        x = x + run + gap
    for i, (px, lean) in enumerate(posts):
        for xx in wrap_x(px, w, pad=40):
            bx, by = xx, fy + rng.normal(0, 0.5)
            tx, ty = bx + lean * post_h, by - post_h
            sh.line([(bx - 2, by + 1.2), (bx - 9, by + 2.2)], "#8a7ca4", 1.6, 0.45)                       # its shadow
            sh.line([(bx, by), (tx, ty)], "#5c4a44", 2.6)
            sh.line([(bx + 0.9, by - 1), (tx + 0.9, ty + 1)], "#9a8070", 0.9, 0.9)                        # its sunny side
    for j, dy in enumerate((-22.0, -12.0)):                              # the wires, between posts of one stretch
        for (pa, la), (pb, lb) in zip(posts[:-1], posts[1:]):
            if pb - pa > 260:
                continue
            for d in (-w, 0, w):
                xa, xb = pa + d, pb + d
                if xb < -20 or xa > w + 20:
                    continue
                pts = [(xa + la * (-dy), fy + dy), ((xa + xb) / 2, fy + dy + 1.4), (xb + lb * (-dy), fy + dy)]
                sh.line(pts, "#4e4652", 0.7, 0.75)
    # a white reflector post or two, close to the road
    for rx in (520.0, 1890.0, 2710.0):
        for xx in wrap_x(rx, w, pad=20):
            by = h - 25
            sh.line([(xx, by), (xx, by - 17)], "#ecebe4", 2.4)
            sh.line([(xx - 0.9, by - 15), (xx - 0.9, by - 12)], "#e8742c", 2.0)
            sh.line([(xx + 3, by + 0.5), (xx - 6, by + 1.5)], "#8a7ca4", 1.4, 0.4)
    return sh.done()


# ---------------------------------------------------------------- all of it
def paint_strip(top, row, fast=False):
    h, w = row - top, WD
    pic = sky((h, w), top, SEED)
    pic = mesas(pic, top, SEED + 1)
    pic = ground(pic, top, SEED + 2)
    pic = road(pic, top, SEED + 3)
    # the brush pass over a wrapped copy, its seam blended (so the strip repeats)
    M_ = 160
    if not fast:
        ext = np.concatenate([pic[:, -M_:], pic, pic[:, :M_]], axis=1)
        st = strokes(ext, sizes=(7, 4, 2), seed=SEED + 4, density=1.6, jitter=0.03, keep=0.42)
        out = st[:, M_:M_ + w].copy()
        B_ = 48
        t = (np.arange(B_, dtype=F32) / B_)[None, :, None]
        out[:, :B_] = st[:, M_ + w:M_ + w + B_] * (1 - t) + st[:, M_:M_ + B_] * t
        pic = out
    c, a = scrub_and_fence((h, w), top, SEED + 5)
    over(pic, c, a)
    # motion: the nearest band (the shoulder and the road's edge) is streaked along, as the eye sees it at speed
    near = np.clip((np.arange(h, dtype=F32) - (h - 30)) / 30.0, 0, 1)[:, None, None]
    sm = np.concatenate([pic[:, -12:], pic, pic[:, :12]], axis=1)
    k = np.ones(13, F32) / 13
    sm = np.stack([np.apply_along_axis(lambda r: np.convolve(r, k, mode="same"), 1, sm[..., i]) for i in range(3)], axis=-1)[:, 12:12 + w]
    pic = pic * (1 - near * 0.7) + sm * (near * 0.7)
    # smoked glass: darker and bluer than the roadside
    pic = np.clip(pic * SMOKE[None, None, :], 0, 1)
    return pic


def seam_check(pic):
    """How different the strip's last column is from its first, against neighbouring columns anywhere (it should be no worse)."""
    d_seam = np.abs(pic[:, -1] - pic[:, 0]).mean()
    d_any = np.abs(pic[:, 1:] - pic[:, :-1]).mean()
    return float(d_seam), float(d_any)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    top, row = rows()
    fast = "fast" in sys.argv
    pic = paint_strip(top, row, fast)
    g = grain(pic, SEED + 9, 0.016)
    pal = palette_of([g], colors=112, seed=3)
    idx = to_palette(g, pal, speckle=0.010)
    save(f"{OUT}/desert-strip.png", idx, pal)
    shown = pal[idx]
    print("desert-strip.png", shown.shape[1], "x", shown.shape[0], "rows", top, "to", row, "seam vs any", seam_check(shown), os.path.getsize(f"{OUT}/desert-strip.png"), "bytes")
    # look at the seam: the end of the strip, then its beginning
    k = 3
    seam = np.concatenate([shown[:, -200:], shown[:, :200]], axis=1)
    Image.fromarray((seam * 255 + 0.5).astype(np.uint8)).resize((400 * k, seam.shape[0] * k), Image.NEAREST).save(f"{WORK}/strip-seam.png")
    Image.fromarray((shown[:, :1600] * 255 + 0.5).astype(np.uint8)).save(f"{WORK}/strip-a.png")
    Image.fromarray((shown[:, 1600:] * 255 + 0.5).astype(np.uint8)).save(f"{WORK}/strip-b.png")

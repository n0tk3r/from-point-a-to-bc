"""PAINT-23 (round twenty-three, RECOMPOSE and the act's watercolour): the cedar path in the hills north of Osaka, dusk,
spring rain (edo-cedars), painted again from a new place. See edo_cedars_kit.py for the camera, the light and every
measurement, and tools/paint/DEPTH.md for the direction.

THE PICTURE. We stand at the foot of the path under a great cedar and look up the hill. NEAR (front.png): that cedar's
wet trunk up the left edge on its bank, its roots and ferns along the bottom left, a bough of another across the top
right corner, fern fronds in the bottom right corner: the darkest, warmest shapes, with a thin wet edge of light.
MIDDLE (the play): worn stone steps come in at the bottom left and climb in a curve to the yard of a charcoal-burner's
storehouse standing higher up on the right, three-quarters on, seen from below: the thatch heavy over deep eaves, the
floor on posts with the dark under it (and the line of lamplight there: light-on.png), the door in the wall that faces
the light, the high window in the shaded wall (window-lit.png), the kiln of earth up to the left, the cut bank with the
bamboo pipe behind the storehouse's far end, the stone figure in its bib by the lower steps, a cedar either side that
people walk behind (cedar-l.png, cedar-r.png). FAR: rank behind rank of trunks going up the hill into the mist, each
paler and softer toward the colour of the dusk sky between them, laid wet in wet.

In Act Six's manner, laid as a watercolour (watercolor.py): graded washes, the far ranks, the mist and the sky wet in wet,
the paper left for the lightest air, shade as a cool glaze, the key line thin and broken and only on what is near.
Nothing copied from any print or painting. Rain, drips, the puddles' rings and the drifting mist are moving things
(layout.json "fx"): the painting holds only the wet.

    python3 edo_cedars.py          paints out/edo-cedars/ (back, front, cedar-l, cedar-r, light-on, window-lit,
                                   layout.json) and out/edo-cedars-comp.png; writes out/edo-cedars-remap.json (where
                                   round twenty's marks are now) and out/edo-cedars-work/scene-numbers.txt (every
                                   number of the scene file, as it writes them)
    python3 edo_cedars.py fast     skips the brush pass and the palette: out/edo-cedars-work/ only
    python3 edo_cedars_plan.py     the skeleton (before any painting);  python3 edo_cedars_play.py  the scene played"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
from edo_cedars_kit import *
import depth as DEPTH
import edo_cedars_layout as LAY
import watercolor as WC
from postimp_paints import PAINTS

OUT = "out/edo-cedars"
WORK = "out/edo-cedars-work"
SEED = 23                                                       # the paper: one sheet under the backdrop and every cut-out


def paint(name):
    return rgb(PAINTS[name]["hex"])


PRUSSIAN, COBALT, ULTRA, CERULEAN = paint("prussian-blue"), paint("cobalt-blue"), paint("ultramarine"), paint("cerulean")
WHITE, OCHRE, SIENNA, VIRIDIAN, VERONESE, NAPLES, VERMILION = (paint("lead-white"), paint("yellow-ochre"), paint("burnt-sienna"),
                                                              paint("viridian"), paint("veronese-green"), paint("naples-yellow"), paint("vermilion"))
SKYC = lerp(lerp(WHITE, CERULEAN, 0.30), PRUSSIAN, 0.07)       # the dusk sky between the trees, and the mist: what far things go toward
PAPER = lerp(WC.PAPER, SKYC, 0.35)                              # the lightest air: the paper, barely tinted
SHADE = lerp(COBALT, PRUSSIAN, 0.6)                             # the act's shade: a blue, never grey
BARK = lerp(SIENNA, PRUSSIAN, 0.50)                             # wet cedar bark in the light
BARK_DARK = lerp(SIENNA, PRUSSIAN, 0.80)
LEAF = lerp(VIRIDIAN, PRUSSIAN, 0.52)                           # cedar foliage, seen from below
MOSS = lerp(lerp(VIRIDIAN, VERONESE, 0.45), OCHRE, 0.12)
EARTH = lerp(lerp(OCHRE, SIENNA, 0.55), PRUSSIAN, 0.55)         # wet earth
LITTER = lerp(lerp(SIENNA, OCHRE, 0.35), PRUSSIAN, 0.42)        # cedar needles on the ground, rust-brown
STONE = lerp(WHITE, PRUSSIAN, 0.50)                             # wet stone under a pale sky
LUM = np.array([0.3, 0.55, 0.15], dtype=F32)
LIGHT_AT = (236.0, 176.0)                                       # the pale gap in the trees: where the light is


def shade_of(c, t=0.35):
    """A colour in shade: pulled toward the act's blue shade, never toward grey."""
    return lerp(col(c), SHADE, t)


def air(d):
    """How much of the mist lies between us and a thing d cm away: 0 near, toward 1 far."""
    return 0.92 * (1.0 - np.exp(-np.maximum(np.asarray(d, dtype=np.float64) - 900.0, 0.0) / 3000.0))


def far_of(c, t):
    """A colour seen through the mist: toward the sky's own colour (not grey), and a breath bluer."""
    return lerp(lerp(col(c), SKYC, t), CERULEAN, t * (1 - t) * 0.20)


_TILES = {}


def wnoise(x, d, cell, seed, octaves=4):
    """Noise that lies on the hillside: sampled by place (x, d in cm), blobs `cell` cm across, so it comes out big near
    us and small and flattened far off."""
    key = (seed, octaves)
    if key not in _TILES:
        _TILES[key] = noise((1024, 1024), 64, seed, octaves)
    k = 64.0 / cell
    return sample(_TILES[key], (x * k + 300.0) % 1020.0, (d * k + 170.0) % 1020.0)


def box_of(pts, pad=3):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (max(int(min(xs)) - pad, 0), max(int(min(ys)) - pad, 0), min(int(max(xs)) + pad + 1, W), min(int(max(ys)) + pad + 1, H))


# ================================================================ far: the air, the hillside, rank behind rank
def air_layer(seed=11):
    """The paper and the first wash: the last of the day through rain and mist. Lightest in the gap up the hill on the
    left (bare paper, barely tinted), graded deeper and bluer to the right and up under the crowns."""
    x, y = PX, PY
    gap = np.exp(-(((x - LIGHT_AT[0]) / 250.0) ** 2 + ((y - LIGHT_AT[1]) / 210.0) ** 2))
    gap = np.clip(gap + (noise(SHAPE, (240, 110), seed, 3) - 0.5) * 0.30, 0, 1)
    deep = lerp(SKYC, lerp(COBALT, PRUSSIAN, 0.35), 0.34)
    pic = lerp(deep[None, None, :], PAPER[None, None, :], smooth(gap)[..., None]).astype(F32)
    # a second, greyer wash coming in from the right and the top right (the rain's own grey, laid wet)
    right = step(0.25, 1.0, (x / W) * 0.75 + (1 - y / H) * 0.35 + (noise(SHAPE, (300, 160), seed + 1, 3) - 0.5) * 0.3)
    over(pic, lerp(SKYC, lerp(COBALT, PRUSSIAN, 0.5), 0.40), (right * 0.42).astype(F32))
    return np.clip(pic, 0, 1).astype(F32)


def ground_layer(pic, info, seed=21):
    """The hillside, through the camera: wet earth under cedar needles, moss in small drifts, darker and warmer toward
    us, paler and bluer up the hill until it is the mist's own colour. Each patch lies on the ground by its place, so it
    shrinks and flattens with distance."""
    gx, gd, ok = CAM.ground()
    t = air(gd).astype(F32)
    blot = wnoise(gx, gd, 300.0, seed, 4)
    fine = wnoise(gx, gd, 80.0, seed + 1, 4)
    speck = wnoise(gx, gd, 20.0, seed + 2, 3)
    base = lerp(EARTH[None, None, :], LITTER[None, None, :], (step(0.40, 0.64, blot) * 0.8)[..., None])
    moss = step(0.62, 0.72, wnoise(gx, gd, 170.0, seed + 3, 4) * 0.65 + fine * 0.35)
    base = lerp(base, lerp(MOSS, PRUSSIAN, 0.46)[None, None, :], (moss * 0.70)[..., None])
    base = base * (1 + ((fine - 0.5) * 0.20 + (speck - 0.5) * 0.18)[..., None])
    # deeper toward us: the near ground holds the darks (a graded wash, laid from the bottom edge up)
    near = step(1250.0, 640.0, gd)
    base = lerp(base, base * lerp(PRUSSIAN, SIENNA, 0.30)[None, None, :] * 2.6, (near * 0.62)[..., None])
    wet = step(0.60, 0.78, wnoise(gx, gd * 6.0, 200.0, seed + 7, 3)) * step(0.50, 0.30, blot) * np.clip((gd - 600.0) / 700.0, 0.15, 1.0)
    base = lerp(base, lerp(SKYC, PAPER, 0.2)[None, None, :], (wet * 0.22)[..., None])
    ground = far_of_pic(base, np.clip(t * 1.15, 0, 0.97))
    m = ok * step(HZ + 1.0, HZ + 10.0, PY)
    over(pic, np.clip(ground, 0, 1), m.astype(F32))
    info["ground"] = m.astype(F32)
    info["gx"], info["gd"] = gx, gd
    return pic


def far_of_pic(picture, t):
    out = picture * (1 - t[..., None]) + SKYC[None, None, :] * t[..., None]
    out = out + (CERULEAN - out) * (t * (1 - t) * 0.20)[..., None]
    return out.astype(F32)


RANKS = [  # depth from, to (cm); how many trunks; the seed; how high the crowns begin (cm)
    (12500.0, 19000.0, 34, 300, 1500.0), (7600.0, 11500.0, 28, 301, 1450.0), (5100.0, 7000.0, 22, 302, 1400.0),
    (3600.0, 4800.0, 15, 303, 1350.0), (2550.0, 3300.0, 9, 304, 1300.0)]
RANK_PLACES = {}


def rank_places(i):
    """A rank's trunks: [(x, d, r, lean)], the farthest first. Planted cedars, evenly spaced, with a gap where one fell,
    two standing close, one grown thick."""
    if i in RANK_PLACES:
        return RANK_PLACES[i]
    d0, d1, n, seed, _ = RANKS[i]
    rng = np.random.default_rng(seed)
    out = []
    tries = 0
    while len(out) < n and tries < 4000:
        tries += 1
        d = rng.uniform(d0, d1)
        x = rng.uniform(-0.82, 0.82) * d
        if any(abs(x - q[0]) / d < 0.024 and abs(d - q[1]) < 600 for q in out):
            continue
        fx, fy = on(x, d)
        if 150 < fx < 330 and rng.random() < 0.5:              # (the pale gap up the hill stays open)
            continue
        r = rng.uniform(26.0, 40.0) * (1.5 if rng.random() < 0.12 else 1.0)
        out.append((x, d, r, rng.normal(0, 0.4)))
    out.sort(key=lambda q: -q[1])
    RANK_PLACES[i] = out
    return out


def canopy_field(base_row, seed, cell=(74.0, 24.0), depth=150.0, ragged=26.0, holes=0.42):
    """Where a rank's foliage hangs: nothing below its crowns' foot, scattered drooping tufts just above it, closing to a
    mass higher up, with gaps of sky left in it. -> a mask."""
    x, y = PX, PY
    edge = base_row + (noise(SHAPE, (150, 400), seed, 3) - 0.5) * 2 * ragged
    up = np.clip((edge - y) / depth, -0.2, 1.4)                       # 0 at the crowns' foot, 1 well up in them
    n = noise(SHAPE, cell, seed + 1, 4)
    droop = noise(SHAPE, (cell[0] * 0.45, cell[1] * 1.6), seed + 2, 3)
    field = up * 1.25 + (n - 0.5) * 0.95 + (droop - 0.5) * 0.35
    return step(holes, holes + 0.10, field).astype(F32)


def far_ranks(pic, info, seed=31):
    """Rank behind rank of trunks going away up the hill: each a flat wash, paler and nearer the sky's colour than the
    one in front of it, its crowns a ragged mass hanging above with the sky in its gaps, and no line anywhere; mist lying
    along the feet of each before the next is laid. All of it wet in wet: its mask goes to the wash, and its edges bleed."""
    soft = np.zeros(SHAPE, F32)
    far_trunks = np.zeros(SHAPE, F32)
    for i in range(len(RANKS)):
        d0, d1, _, _, crown = RANKS[i]
        dm = (d0 + d1) / 2
        places = rank_places(i)
        t = float(air(dm))
        leaf_c = far_of(lerp(LEAF, COBALT, 0.22), min(t + 0.07, 0.975))
        base_row = on(0, dm, crown)[1]
        can = canopy_field(base_row, seed + 40 + i, cell=(60.0 + 12 * i, 18.0 + 5 * i), depth=110.0 + 30 * i, ragged=14.0 + 6 * i)
        # (the crowns thin out toward the gap, where the hill opens)
        gap = np.exp(-(((PX - LIGHT_AT[0]) / 190.0) ** 2 + ((PY - LIGHT_AT[1]) / 150.0) ** 2))
        can = can * (1 - 0.55 * gap)
        grade = lerp(leaf_c, lerp(leaf_c, SHADE, 0.22), 1.0)             # a little deeper toward the top
        top = np.clip((base_row - PY) / 260.0, 0, 1)[..., None]
        over(pic, lerp(leaf_c[None, None, :], grade[None, None, :], top), (can * 0.86).astype(F32))
        soft = np.maximum(soft, can)
        s = Paper(SHAPE)
        for (x, d, r, lean) in places:
            tt = float(air(d))
            trunk_c = far_of(lerp(BARK, SHADE, 0.40), min(tt + 0.03, 0.97))
            L, R = trunk_edges(None, r, lean, x=x, d=d, top=4600.0)
            s.poly(L + R[::-1], trunk_c, 1.0)
            a, b = on(x - r * 1.9, d), on(x + r * 1.9, d)                 # the foot: a little spread, no drawing
            c, e = on(x - r, d, r * 2.2), on(x + r, d, r * 2.2)
            s.poly([a, b, e, c], trunk_c, 1.0)
        colr, alpha = s.done()
        # a trunk pales as it rises into its own crown and the mist up there
        rise = np.clip((on(0, dm)[1] - PY) / max(on(0, dm)[1] - base_row + 120.0, 1.0), 0, 1) ** 1.3
        feather = 1.25 - 0.18 * i                                         # the farther the rank, the softer its edges
        over(pic, blur(lerp(colr, SKYC[None, None, :], (rise * 0.34)[..., None]), feather), blur(alpha, feather))
        far_trunks = np.maximum(far_trunks, alpha)
        # the mist along this rank's feet and up between it and the next: the paper's colour, laid wet
        row = on(0, dm)[1]
        band = np.exp(-((PY - (row - 22.0 - 5.0 * i)) / (30.0 + 9.0 * i)) ** 2) * (0.5 + 0.5 * noise(SHAPE, (340, 60), seed + 20 + i, 3))
        over(pic, lerp(SKYC, PAPER, 0.55), np.clip(band * (0.58 - 0.07 * i), 0, 1).astype(F32))
    info["soft"] = soft
    info["far_trunks"] = far_trunks
    return pic


# ================================================================ a cedar, through the camera
def trunk_geom(x, d, r, lean=0.0, base=0.0, top=4400.0, flare=1.15, flare_h=175.0, seed=0):
    """A cedar's outline as picture points: its two edges from the ground up (the foot flaring into the roots), and the
    roots that run out over the ground toward us. -> dict(L, R, hs, roots, x, d, r, base)."""
    rng = np.random.default_rng(seed)
    hs = [0.0, 12.0, 30.0, 55.0, 85.0, 120.0, 160.0, 210.0, 300.0, 450.0, 700.0, 1000.0, 1400.0, 1900.0, 2500.0, 3200.0, top]
    L, R = [], []
    wob = rng.normal(0, 0.035, len(hs))
    for i, h in enumerate(hs):
        rr = r * (1 - 0.10 * min(h / 3000.0, 1.3)) * (1 + wob[i] * (h > 200))
        f = flare * r * max(0.0, 1.0 - h / flare_h) ** 2.3
        cx = x + lean * h / 100.0
        L.append(on(cx - rr - f * 1.05, d, base + h))
        R.append(on(cx + rr + f * 0.95, d, base + h))
    # the roots: ridges that leave the trunk at knee height and run out over the ground, mostly toward us and to the sides
    roots = []
    n = int(rng.integers(5, 8))
    for j in range(n):
        a = math.radians(-8.0 + 196.0 * (j + rng.uniform(0.15, 0.85)) / n)           # 0: to the right; 90: straight at us; 180: to the left
        reach = r * rng.uniform(2.3, 3.6)
        h0 = rng.uniform(55.0, 120.0)
        w0 = r * rng.uniform(0.34, 0.5)
        bend = rng.uniform(-0.35, 0.35)
        ridge_l, ridge_r = [], []
        for k in range(7):
            q = k / 6.0
            aa = a + bend * q
            rho = r * 0.72 + (reach - r * 0.72) * q
            hh = h0 * (1 - q) ** 1.7
            wd = w0 * (1 - 0.72 * q)
            px_, pd_ = x + math.cos(aa) * rho, d - math.sin(aa) * rho
            tx, td_ = -math.sin(aa), -math.cos(aa)                                    # across the root, level
            ridge_l.append(on(px_ - tx * wd, pd_ - td_ * wd, base + hh * 0.35))
            ridge_r.append(on(px_ + tx * wd, pd_ + td_ * wd, base + hh * 0.35))
            if k == 0:
                top0 = on(px_, pd_, base + hh)
        spine = [on(x + math.cos(a + bend * q) * (r * 0.72 + (reach - r * 0.72) * q), d - math.sin(a + bend * q) * (r * 0.72 + (reach - r * 0.72) * q),
                    base + h0 * (1 - q) ** 1.7) for q in np.linspace(0, 1, 7)]
        roots.append(dict(poly=ridge_l + ridge_r[::-1], spine=spine, a=a))
    return dict(L=L, R=R, hs=hs, roots=roots, x=x, d=d, r=r, base=base, lean=lean)


def trunk_layer(g, seed, detail=1.0, rim=0.0, moss=0.6, wet=0.5, mist_up=0.3, warm=0.0, with_roots=True, extra_air=0.0, rim_left=0.0, flank=0.0):
    """A cedar painted as a layer of its own: -> (rgb, alpha). A graded wash round the trunk (lighter toward the pale gap
    up on the left, deep on the right), the bark's long fibres running with the trunk and fanning out into the roots,
    moss low down on the weather side, a wet light down the lit side; paler as it rises into the mist; all of it seen
    through the air between us and it (far_of). `detail` 0..1: how much of that is drawn; `rim`: a thin cool light down
    its right edge (the near cedar, against the gap); `rim_left`: the same down its left edge (a trunk that faces the
    gap); `flank`: for the great cedar, of which we see only the right flank: it turns toward the gap's light as it
    goes round to its right edge, so the wash lightens and warms that way."""
    L, R, hs = g["L"], g["R"], g["hs"]
    sh = Paper(SHAPE)
    sh.poly(L + R[::-1], (1, 1, 1), 1.0)
    if with_roots:
        for rt in g["roots"]:
            sh.poly(rt["poly"], (1, 1, 1), 1.0)
    _, alpha = sh.done()
    x0, y0, x1, y1 = box_of(L + R + [q for rt in g["roots"] for q in rt["poly"]] if with_roots else L + R, pad=4)
    if x1 <= x0 or y1 <= y0:
        return np.zeros(SHAPE + (3,), F32), alpha
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(F32)
    rows = np.arange(y0, y1, dtype=F32)
    ly, lx = np.array([q[1] for q in L])[::-1], np.array([q[0] for q in L])[::-1]
    ry, rx = np.array([q[1] for q in R])[::-1], np.array([q[0] for q in R])[::-1]
    xl = np.interp(rows, ly, lx)[:, None]
    xr = np.interp(rows, ry, rx)[:, None]
    wpx = np.maximum(xr - xl, 1.0)
    u = np.clip((xx - xl) / wpx, 0.0, 1.0)
    h = np.interp(rows, ly, np.array(hs)[::-1])[:, None] * np.ones_like(xx)             # cm above its foot
    # the form: a graded wash across (light from the upper left), the shade side a blue-brown
    wander = (noise((y1 - y0, 4), (4, 150.0), seed + 5, 2)[:, :1] - 0.5) * 0.34          # (the turn from light to shade is no ruled line: it wanders up the trunk)
    sn = np.clip(2 * u - 1 + wander, -1, 1)
    lit = np.clip(-sn * 0.62 + np.sqrt(np.clip(1 - sn * sn, 0, 1)) * 0.78, 0, 1)
    lit = smooth((lit - 0.18) / 0.72)
    lit = np.maximum(lit, 0.30 * np.exp(-((1 - u) / 0.045) ** 2))                         # (a little of the wet sky comes back round the shade side's edge)
    t = float(air(g["d"])) + extra_air
    c_lit = lerp(lerp(BARK, OCHRE, 0.10 + warm), SKYC, 0.10)
    c_mid = lerp(BARK, SIENNA, warm)
    c_dark = lerp(BARK_DARK, lerp(PRUSSIAN, SIENNA, 0.3), 0.3)
    colr = lerp(c_dark[None, None, :], c_mid[None, None, :], smooth(lit * 1.6)[..., None])
    colr = lerp(colr, c_lit[None, None, :], (smooth((lit - 0.55) / 0.45) * 0.75)[..., None])
    if flank:
        turn = smooth((u - 0.50) / 0.48) * flank
        colr = lerp(colr, lerp(BARK, SIENNA, 0.18)[None, None, :], turn[..., None])
    # the bark: long fibres that run with the trunk (and fan with the roots)
    r_px = float(np.median(wpx))
    cellx = max(2.0, r_px * 0.085)
    tile = noise((512, 1024), (cellx, 150.0), seed, 3)
    fib = sample(tile, (u * r_px * 1.9 + 37.0) % 1020.0, (yy * 0.9 + seed * 13) % 508.0)
    tile2 = noise((512, 1024), (max(1.4, cellx * 0.45), 70.0), seed + 1, 2)
    fine = sample(tile2, (u * r_px * 1.9 + 11.0) % 1020.0, (yy * 1.3 + seed * 7) % 508.0)
    furrow = step(0.60, 0.72, fib * 0.65 + fine * 0.35)
    colr = colr * (1 + ((fib - 0.5) * 0.30 * detail + (fine - 0.5) * 0.14 * detail)[..., None])
    colr = lerp(colr, colr * lerp(PRUSSIAN, SIENNA, 0.25)[None, None, :] * 2.2, (furrow * 0.50 * detail)[..., None])
    # moss low down, most on the weather side; a paler lichen higher
    if moss:
        mn = noise((y1 - y0, x1 - x0), (max(4.0, r_px * 0.5), max(8.0, r_px * 1.2)), seed + 2, 3)
        low = step(260.0, 30.0, h) * step(0.44, 0.60, mn + (0.5 - u) * 0.30)
        colr = lerp(colr, lerp(MOSS, PRUSSIAN, 0.42)[None, None, :] * (0.8 + 0.4 * fib[..., None]), (low * moss * 0.8)[..., None])
    # the wet: a broken cool light down the lit side
    if wet:
        sheen = np.exp(-((u - 0.20) / 0.07) ** 2) * step(0.50, 0.68, fine) * wet
        colr = lerp(colr, lerp(SKYC, c_lit, 0.35)[None, None, :], (sheen * 0.55)[..., None])
    # deeper at the foot, where it stands in its own shade
    colr = colr * (1 - 0.22 * step(70.0, 0.0, h))[..., None]
    if rim:
        edge = np.exp(-((1 - u) * wpx / 3.2) ** 2) * (0.45 + 0.55 * step(0.35, 0.6, fib))
        colr = lerp(colr, lerp(SKYC, CERULEAN, 0.25)[None, None, :], (edge * rim)[..., None])
    if rim_left:
        edge = np.exp(-(u * wpx / 2.4) ** 2) * (0.5 + 0.5 * step(0.35, 0.6, fine)) * step(40.0, 140.0, h)
        colr = lerp(colr, lerp(SKYC, c_lit, 0.25)[None, None, :], (edge * rim_left)[..., None])
    # the air: the whole trunk seen through the mist between, and paler as it rises into the mist under the crowns
    up = np.clip(h / 2600.0, 0, 1) ** 0.8
    tt = np.clip(t + mist_up * up * (0.4 + t), 0, 0.97)
    colr = colr * (1 - tt[..., None]) + SKYC[None, None, :] * tt[..., None]
    colr = colr + (CERULEAN[None, None, :] - colr) * (tt * (1 - tt) * 0.20)[..., None]
    out = np.zeros(SHAPE + (3,), F32)
    out[y0:y1, x0:x1] = np.clip(colr, 0, 1)
    return out, alpha


def root_marks(s, g, detail=1.0, t=0.0):
    """The drawing on a trunk's roots (laid after the brush): a dark crease down each side of a root, a light on its top."""
    for rt in g["roots"]:
        sp = rt["spine"]
        s.line(sp, far_of(lerp(BARK, SKYC, 0.22), t), max(0.8, g["r"] * 0.03 * CAM.px_cm(g["x"], g["d"]) * 2.2), 0.45 * detail)
        pl = rt["poly"]
        n = len(pl) // 2
        s.line(pl[:n], far_of(lerp(PRUSSIAN, SIENNA, 0.25), t), 0.9, 0.55 * detail)


def trunk_marks(s, g, seed, t=0.0, detail=1.0, stubs=2, near=False):
    """What is drawn on a nearer trunk after the brush, so that it is a tree and not a bar: the bark's long furrows and
    ridges running with it (broken, starting again), a knot or two, the stub of a dead branch standing out from its edge
    with its own little shade below, a dark wet streak down from it."""
    rng = np.random.default_rng(seed)
    L, R, hs = g["L"], g["R"], g["hs"]
    k = CAM.px_cm(g["x"], g["d"], g["base"])
    wpx = abs(R[6][0] - L[6][0])
    furrow = far_of(lerp(PRUSSIAN, SIENNA, 0.25), t)
    ridge = far_of(lerp(BARK, SKYC, 0.20), t)
    n = int(max(6, wpx * 0.5) * detail)
    for j in range(n):
        u = rng.uniform(0.06, 0.96)
        i0 = int(rng.integers(3, len(L) - 3))
        i1 = min(len(L) - 1, i0 + int(rng.integers(1, 4)))
        f0, f1 = rng.uniform(0, 0.6), rng.uniform(0.4, 1.0)
        pts = []
        for i in range(i0, i1 + 1):
            pts.append(lerp_pt(L[i], R[i], u + rng.normal(0, 0.008)))
        # (only a part of the first and last piece, so the lines begin and end anywhere up the trunk)
        pts[0] = lerp_pt(pts[0], pts[1], f0 * 0.8)
        pts[-1] = lerp_pt(pts[-2], pts[-1], f1)
        lit_side = u < 0.42
        if lit_side and j % 2:
            key(s, pts, ridge, max(0.8, wpx * 0.02), 0.40 * detail, seed=seed + j, gaps=0.3, dash=22.0)
        else:
            key(s, pts, furrow, max(0.8, wpx * 0.024), (0.42 if u < 0.6 else 0.28) * detail, seed=seed + j, gaps=0.3, dash=22.0)
    for j in range(stubs):                                        # dead branch stubs, and a knot
        i = int(rng.integers(8, 13))
        q = rng.uniform(0.1, 0.9)
        side = 1 if rng.random() < 0.5 else -1
        a_ = lerp_pt(L[i], L[i + 1], q) if side < 0 else lerp_pt(R[i], R[i + 1], q)
        ln = max(5.0, wpx * rng.uniform(0.35, 0.8))
        tip = (a_[0] + side * ln, a_[1] - ln * rng.uniform(0.25, 0.6))
        s.taper([(a_[0] - side * 2, a_[1] + 1), tip], far_of(lerp(BARK_DARK, PRUSSIAN, 0.25), t), max(1.6, wpx * 0.10), max(0.8, wpx * 0.035), 1.0)
        s.line([(a_[0] - side * 1, a_[1] - 1), (tip[0], tip[1] - 1)], far_of(lerp(BARK, SKYC, 0.25), t), max(0.7, wpx * 0.03), 0.7)
        streak = [(a_[0] - side * wpx * 0.10, a_[1] + 3), (a_[0] - side * wpx * 0.12, a_[1] + ln * 2.5), (a_[0] - side * wpx * 0.10, a_[1] + ln * 5)]
        key(s, streak, furrow, max(1.0, wpx * 0.05), 0.30, seed=seed + 50 + j, gaps=0.1, dash=18.0)
    for j in range(1):
        i = int(rng.integers(6, 12))
        c = lerp_pt(lerp_pt(L[i], R[i], rng.uniform(0.25, 0.75)), lerp_pt(L[i + 1], R[i + 1], 0.5), rng.uniform(0.1, 0.9))
        rr = max(1.6, wpx * 0.05)
        s.ellipse(c[0], c[1], rr, rr * 1.6, furrow, 0.38)


def foot_shade(pic, x, d, r, ground, amount=0.42, base=0.0):
    """The soft shade a trunk stands in: darker close round its foot, running out a little down the hill and to the right
    (away from the pale gap). A glaze over the ground."""
    ring = [on(x + math.cos(a) * r * (3.4 if math.cos(a) > 0 else 2.6), d - math.sin(a) * r * (3.6 if math.sin(a) > 0 else 2.2), base) for a in np.linspace(0, 2 * math.pi, 20, endpoint=False)]
    m = mask_poly(SHAPE, ring, soft=max(1.5, 4.0 * CAM.px_cm(x, d) * r / 30.0))
    tint(pic, SHADE * 1.5, np.clip(m * amount * ground, 0, 1).astype(F32))


def spec_place(spec):
    """(picture x, row of the foot, radius, lean) -> (x, d, r, lean)."""
    px_, py_, r, lean = spec
    x, d = G(px_, py_)
    return x, d, r, lean


def mid_trunks(pic, info, behind, seed=51):
    """The backdrop's own cedars round the play (nobody walks behind these): `behind` True for the ones that stand beyond
    the storehouse's back (painted before it), False for the nearer ones (painted after it)."""
    hd = HOUSE.corner[1] + 200.0
    for i, spec in enumerate(sorted(TRUNKS_MID, key=lambda t: t[1])):
        x, d, r, lean = spec_place(spec)
        if (d > hd) != behind:
            continue
        g = trunk_geom(x, d, r, lean, seed=seed + i)
        foot_shade(pic, x, d, r, info["ground"])
        colr, alpha = trunk_layer(g, seed + 10 * i, detail=0.75 if d > 1500 else 1.0, mist_up=0.42, extra_air=0.14 if behind else 0.0, rim_left=0.0 if behind else 0.45)
        over(pic, colr, alpha)
        info.setdefault("trunks", []).append((g, float(air(d))))
        info["crisp"] = np.maximum(info.get("crisp", np.zeros(SHAPE, F32)), alpha)


# ================================================================ flat faces through the camera
def quad_st(quad):
    """A flat four-cornered face of the world as it lies in the picture: for every pixel, where on the face it is.
    `quad`: the picture points of the face's corners (0,0), (1,0), (1,1), (0,1). -> (s, t): true to the perspective,
    so that boards, courses and joints laid by (s, t) run to their vanishing points by themselves."""
    src = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    A, bb = [], []
    for (sx, sy), (x, y) in zip(src, quad):
        A.append([x, y, 1, 0, 0, 0, -sx * x, -sx * y]); bb.append(sx)
        A.append([0, 0, 0, x, y, 1, -sy * x, -sy * y]); bb.append(sy)
    h = np.linalg.solve(np.array(A, dtype=np.float64), np.array(bb, dtype=np.float64))
    den = h[6] * PX + h[7] * PY + 1.0
    den = np.where(np.abs(den) < 1e-6, 1e-6, den)
    return ((h[0] * PX + h[1] * PY + h[2]) / den).astype(F32), ((h[3] * PX + h[4] * PY + h[5]) / den).astype(F32)


def hand(points, amount=0.7, seed=0):
    """A ruled outline made by hand: each corner off by a hair, each long edge sagging or bowing a little."""
    rng = np.random.default_rng(seed)
    out = []
    n = len(points)
    for i in range(n):
        a, b = points[i], points[(i + 1) % n]
        out.append((a[0] + rng.normal(0, amount * 0.5), a[1] + rng.normal(0, amount * 0.5)))
        ln = math.hypot(b[0] - a[0], b[1] - a[1])
        if ln > 40:
            nx, ny = -(b[1] - a[1]) / ln, (b[0] - a[0]) / ln
            k = rng.normal(0, amount) * min(ln / 120.0, 1.6)
            for q in (0.33, 0.66):
                out.append((a[0] + (b[0] - a[0]) * q + nx * k, a[1] + (b[1] - a[1]) * q + ny * k))
    return out


# ================================================================ the storehouse
BOARD = lerp(lerp(OCHRE, SIENNA, 0.62), PRUSSIAN, 0.60)         # dark wet boards
POST = lerp(lerp(OCHRE, SIENNA, 0.7), PRUSSIAN, 0.70)
THATCH = lerp(lerp(lerp(OCHRE, SIENNA, 0.30), WHITE, 0.10), PRUSSIAN, 0.48)   # old thatch, grey-brown, wet
UNDER = lerp(PRUSSIAN, SIENNA, 0.16)                            # the dark under the floor


def house(pic, info, seed=71):
    """The charcoal-burner's storehouse, three-quarters on and seen from below, every face laid through the camera: the
    dark under the floor with its posts on their stones, the door wall (it faces the pale gap: the lighter wall) and
    the window's wall (the shade side), boards and posts, the plank door up two steps, the small high window, the
    thatch's thick wet cut edge low over the walls with its shade under it, the long slope and the hip going up into
    the mist, the ridge under its bark cap."""
    Hs = HOUSE
    LW, LD, e = Hs.LW, Hs.LD, Hs.eave
    rng = np.random.default_rng(seed)
    t_air = float(air(Hs.corner[1] + 150.0))
    crisp = np.zeros(SHAPE, F32)
    A = lambda c: far_of(c, t_air)

    def flat(pts, colr, wob=0.6, sd=0, alpha=1.0):
        m = mask_poly(SHAPE, hand(pts, wob, seed + sd))
        over(pic, colr, m * alpha)
        return m

    # ---- the whole of it first in one dark tone, so that where two faces meet the seam is a dark line and never the hillside
    (r0u, r0w), (r1u, r1w) = Hs.ridge_at
    sil = [Hs.foot(0, LD), Hs.foot(0, 0), Hs.foot(LW, 0), Hs.pt(LW, 0, Hs.eave_under), Hs.pt(LW + e, -e, Hs.eave_under), Hs.pt(LW + e, -e, Hs.eave_top),
           Hs.pt(r1u, r1w, Hs.ridge), Hs.pt(r0u, r0w, Hs.ridge), Hs.pt(-e, LD + e, Hs.eave_top), Hs.pt(-e, LD + e, Hs.eave_under), Hs.pt(0, LD, Hs.eave_under)]
    over(pic, A(lerp(UNDER, BOARD, 0.25)), mask_poly(SHAPE, sil))
    # ---- under the floor: the dark, the ground going on under it a little way, the posts on their stones
    gapW = [Hs.foot(0, 0), Hs.foot(LW, 0), Hs.pt(LW, 0, 0), Hs.pt(0, 0, 0)]
    gapD = [Hs.foot(0, 0), Hs.foot(0, LD), Hs.pt(0, LD, 0), Hs.pt(0, 0, 0)]
    mW = flat(gapW, A(UNDER), 0.4, 1)
    mD = flat(gapD, A(lerp(UNDER, BOARD, 0.18)), 0.4, 2)
    under = np.maximum(mW, mD)
    # (the dry ground under the house shows a little way in, paler, before the dark takes it)
    for (a, b_, c, d_), k in (((Hs.foot(0, 0), Hs.foot(LW, 0), Hs.foot(LW, 26), Hs.foot(0, 26)), 0.30), ((Hs.foot(0, 0), Hs.foot(0, LD), Hs.foot(26, LD), Hs.foot(26, 0)), 0.38)):
        m = mask_poly(SHAPE, [a, b_, c, d_], soft=1.0) * under
        over(pic, A(lerp(EARTH, OCHRE, 0.20)), m * k)
    info["under_floor"] = under
    gap_front = np.zeros(SHAPE, F32)                      # what stands before the dark under the floor: posts, their stones, the door's steps
    posts = []
    for u in Hs.posts_w:
        posts.append((u, 0.0, 1))
    for w in Hs.posts_d[1:]:
        posts.append((0.0, w, 0))
    for (u, w, side) in posts:
        du, dw = (7.0, 0.0) if side else (0.0, 7.0)
        a, b_ = Hs.foot(u - du, w - dw, 10.0), Hs.foot(u + du, w + dw, 10.0)
        c, d_ = Hs.pt(u + du, w + dw, 0), Hs.pt(u - du, w - dw, 0)
        if abs(a[1] - d_[1]) > 3:
            gap_front = np.maximum(gap_front, flat([a, b_, c, d_], A(lerp(POST, SKYC, 0.10 if side else 0.20)), 0.3, 3))
        st = [Hs.foot(u - 16, w - 16), Hs.foot(u + 16, w - 16 if side else w + 16), Hs.foot(u + 14, w + 4, 12.0), Hs.foot(u - 14, w + 4, 12.0)]
        s0, s1 = Hs.foot(u - du * 2.4, w - dw * 2.4), Hs.foot(u + du * 2.4, w + dw * 2.4)
        top = Hs.foot(u, w, 12.0)
        gap_front = np.maximum(gap_front, flat([(s0[0], s0[1] + 1.5), (s1[0], s1[1] + 1.5), (s1[0] - 1, top[1]), (s0[0] + 1, top[1])], A(lerp(STONE, PRUSSIAN, 0.25)), 0.4, 4))
    # ---- the walls
    wall_top = Hs.eave_under + 26.0                      # (the thatch's edge hides the rest)
    wW = [Hs.pt(0, 0, -16), Hs.pt(LW, 0, -16), Hs.pt(LW, 0, wall_top), Hs.pt(0, 0, wall_top)]
    wD = [Hs.pt(0, 0, -16), Hs.pt(0, LD, -16), Hs.pt(0, LD, wall_top), Hs.pt(0, 0, wall_top)]
    c_lit = lerp(BOARD, SKYC, 0.30)                      # the door wall: toward the gap
    c_shade = shade_of(lerp(BOARD, SIENNA, 0.10), 0.34)   # the window's wall
    for quad, colr, length, name, sd in ((wW, c_shade, LW, "W", 5), (wD, c_lit, LD, "D", 6)):
        m = mask_poly(SHAPE, hand(quad, 0.5, seed + sd))
        s_, t_ = quad_st(quad)
        ucm, ycm = s_ * length, t_ * (wall_top + 16.0) - 16.0
        board = np.floor((ycm + 16.0) / 21.0)
        tone = (np.sin(board * 12.9898 + sd) * 43758.5453) % 1.0
        grainy = noise(SHAPE, (60, 3.2), seed + sd + 20, 3)
        field = colr[None, None, :] * (1 + ((tone - 0.5) * 0.14 + (grainy - 0.5) * 0.16)[..., None])
        # a graded wash: deeper toward the far end and up under the thatch; damp and moss creeping up from the foot
        field = lerp(field, field * (SHADE * 1.7)[None, None, :], (np.clip(s_, 0, 1) * 0.30)[..., None])
        damp = step(55.0, -10.0, ycm + (noise(SHAPE, (40, 20), seed + sd + 21, 3) - 0.5) * 50.0)
        field = lerp(field, lerp(MOSS, PRUSSIAN, 0.55)[None, None, :], (damp * 0.42)[..., None])
        over(pic, far_of_pic(np.clip(field, 0, 1), np.full(SHAPE, t_air, F32)), m)
        crisp = np.maximum(crisp, m)
        info["wall" + name] = (m, quad, ucm, ycm)
    # ---- the door: planks in a frame, up two steps
    d0, d1, dh = Hs.door
    flat([Hs.pt(0, d0 - 8, -4), Hs.pt(0, d1 + 8, -4), Hs.pt(0, d1 + 8, dh + 9), Hs.pt(0, d0 - 8, dh + 9)], A(lerp(POST, PRUSSIAN, 0.15)), 0.4, 8)
    door_m = flat([Hs.pt(0, d0, 0), Hs.pt(0, d1, 0), Hs.pt(0, d1, dh), Hs.pt(0, d0, dh)], A(lerp(lerp(BOARD, OCHRE, 0.16), PRUSSIAN, 0.10)), 0.3, 9)
    info["door"] = [Hs.pt(0, d0, 0), Hs.pt(0, d1, 0), Hs.pt(0, d1, dh), Hs.pt(0, d0, dh)]
    # the steps: a big flat stone on the ground, a wooden step on it
    gd_ = Hs.clear(0, (d0 + d1) / 2)
    stone_h = 30.0
    sw0, sw1 = d0 - 6, d1 + 10
    stone_top = [Hs.foot(-18, sw0, stone_h), Hs.foot(-18, sw1, stone_h), Hs.foot(-78, sw1 - 8, stone_h), Hs.foot(-74, sw0 + 6, stone_h)]
    stone_front = [Hs.foot(-74, sw0 + 6, stone_h), Hs.foot(-78, sw1 - 8, stone_h), Hs.foot(-78, sw1 - 8, 0), Hs.foot(-74, sw0 + 6, 0)]
    stone_side = [Hs.foot(-18, sw0, stone_h), Hs.foot(-74, sw0 + 6, stone_h), Hs.foot(-74, sw0 + 6, 0), Hs.foot(-18, sw0, 0)]
    step_y = -gd_ + stone_h + 24.0                      # the wooden step's top, above the floor (negative: below it)
    wood_top = [Hs.pt(-2, d0 + 2, step_y), Hs.pt(-2, d1 - 2, step_y), Hs.pt(-34, d1 - 2, step_y), Hs.pt(-34, d0 + 2, step_y)]
    wood_front = [Hs.pt(-34, d0 + 2, step_y), Hs.pt(-34, d1 - 2, step_y), Hs.pt(-34, d1 - 2, step_y - 22), Hs.pt(-34, d0 + 2, step_y - 22)]
    wood_side = [Hs.pt(-2, d0 + 2, step_y), Hs.pt(-34, d0 + 2, step_y), Hs.pt(-34, d0 + 2, step_y - 22), Hs.pt(-2, d0 + 2, step_y - 22)]
    for (poly_, colr_, sd_) in ((wood_side, A(lerp(POST, SKYC, 0.16)), 10), (wood_front, A(shade_of(POST, 0.2)), 11), (wood_top, A(lerp(BOARD, SKYC, 0.30)), 12),
                                (stone_side, A(lerp(STONE, PRUSSIAN, 0.34)), 13), (stone_front, A(lerp(STONE, PRUSSIAN, 0.52)), 14), (stone_top, A(lerp(STONE, PRUSSIAN, 0.12)), 15)):
        gap_front = np.maximum(gap_front, flat(poly_, colr_, 0.4, sd_))
    info["gap_front"] = gap_front
    info["door_steps"] = stone_top + stone_front + wood_top
    # ---- the thatch's shade on the walls: a cool glaze, deepest right under the edge
    for name, quad_top in (("W", lambda q: Hs.pt(q * LW, 0, wall_top)), ("D", lambda q: Hs.pt(0, q * LD, wall_top))):
        m, quad, ucm, ycm = info["wall" + name]
        sh = step(Hs.eave_under - 92.0, Hs.eave_under + 6.0, ycm + (noise(SHAPE, (50, 14), seed + 30, 3) - 0.5) * 14.0)
        tint(pic, SHADE * 1.25, (sh * 0.50 * m).astype(F32))
    # ---- the window: a small square opening in a thick frame, dark (the lamp is its own picture)
    w0, w1, ws, wh = Hs.window
    flat([Hs.pt(w0 - 7, 0, ws - 9), Hs.pt(w1 + 7, 0, ws - 9), Hs.pt(w1 + 7, 0, wh + 7), Hs.pt(w0 - 7, 0, wh + 7)], A(lerp(lerp(POST, OCHRE, 0.2), SKYC, 0.30)), 0.3, 16)
    win = [Hs.pt(w0, 0, ws), Hs.pt(w1, 0, ws), Hs.pt(w1, 0, wh), Hs.pt(w0, 0, wh)]
    flat(win, lerp(PRUSSIAN, COBALT, 0.10) * 0.9, 0.2, 17)
    # (the opening's depth: the far jamb and the sill's top seen through it)
    flat([Hs.pt(w1, 0, ws), Hs.pt(w1, 0, wh), Hs.pt(w1 - 5, 12, wh), Hs.pt(w1 - 5, 12, ws)], A(lerp(POST, PRUSSIAN, 0.35)), 0.2, 18)
    info["window"] = win
    # the sill board, standing out from the wall
    flat([Hs.pt(w0 - 10, -7, ws - 5), Hs.pt(w1 + 10, -7, ws - 5), Hs.pt(w1 + 10, 0, ws - 9), Hs.pt(w0 - 10, 0, ws - 9)], A(lerp(BOARD, SKYC, 0.50)), 0.2, 19)
    # ---- the thatch: the cut edge, the long slope, the hip, the ridge
    yu, yt = Hs.eave_under, Hs.eave_top
    A0u, B0u, D0u = Hs.pt(-e, -e, yu), Hs.pt(LW + e, -e, yu), Hs.pt(-e, LD + e, yu)
    A0t, B0t, D0t = Hs.pt(-e, -e, yt), Hs.pt(LW + e, -e, yt), Hs.pt(-e, LD + e, yt)
    (r0u, r0w), (r1u, r1w) = Hs.ridge_at
    R0, R1 = Hs.pt(r0u, r0w, Hs.ridge), Hs.pt(r1u, r1w, Hs.ridge)
    thatch_shade = shade_of(THATCH, 0.30)
    # the long slope (over the window's wall): the shade side, but it looks up at the sky
    longq = [A0t, B0t, Hs.pt(LW + e, r0w, Hs.ridge), Hs.pt(-e, r0w, Hs.ridge)]
    long_poly = [A0t, B0t, R1, R0]
    hipq = [A0t, D0t, Hs.pt(r0u, LD + e, Hs.ridge), Hs.pt(r0u, -e, Hs.ridge)]
    hip_poly = [A0t, D0t, R0]
    for poly, quad, colr, span, rise, name, sd in ((long_poly, longq, lerp(thatch_shade, THATCH, 0.35), LW + 2 * e, (r0w + e), "long", 40),
                                                    (hip_poly, hipq, lerp(THATCH, SKYC, 0.24), LD + 2 * e, (r0u + e), "hip", 41)):
        m = mask_poly(SHAPE, hand(poly, 0.9, seed + sd))
        s_, t_ = quad_st(quad)
        slope_cm = t_ * rise / math.cos(math.radians(Hs.pitch))                 # how far up the slope, cm
        course = (np.sin(slope_cm / 34.0 * 2 * math.pi + (noise(SHAPE, (90, 30), seed + sd + 1, 3) - 0.5) * 3.0) * 0.5 + 0.5)
        comb = noise(SHAPE, (3.0, 26.0), seed + sd + 2, 3)
        blot = noise(SHAPE, (70, 46), seed + sd + 3, 4)
        field = colr[None, None, :] * (1 + ((course - 0.5) * 0.10 + (comb - 0.5) * 0.20 + (blot - 0.5) * 0.18)[..., None])
        # moss where the wet sits: along the foot of the slope and in drifts; the rain-dark streaks down from the ridge
        mossy = step(0.50, 0.66, noise(SHAPE, (18, 60), seed + sd + 4, 4) * 0.65 + blot * 0.35 + (0.30 - np.clip(t_, 0, 1)) * 0.5)
        field = lerp(field, lerp(MOSS, PRUSSIAN, 0.40)[None, None, :] * (0.85 + 0.3 * comb[..., None]), (mossy * 0.55)[..., None])
        streak = step(0.60, 0.80, noise(SHAPE, (7.0, 120.0), seed + sd + 5, 3)) * step(0.15, 0.6, np.clip(t_, 0, 1))
        field = lerp(field, field * (lerp(PRUSSIAN, SIENNA, 0.3) * 2.0)[None, None, :], (streak * 0.34)[..., None])
        worn = step(0.62, 0.80, noise(SHAPE, (40, 26), seed + sd + 6, 3)) * step(0.25, 0.7, np.clip(t_, 0, 1))
        field = lerp(field, lerp(THATCH, SKYC, 0.36)[None, None, :], (worn * 0.34)[..., None])
        # a graded wash up the slope: wet and deep at its foot, paler toward the ridge where the mist has it
        up = np.clip(t_, 0, 1)
        field = lerp(field * (SHADE * 1.7)[None, None, :], field, (0.40 + 0.60 * smooth(up * 2.6))[..., None])
        tt = np.clip(t_air + 0.26 * up ** 1.4, 0, 0.9)
        over(pic, far_of_pic(np.clip(field, 0, 1), tt.astype(F32)), m)
        crisp = np.maximum(crisp, m)
        info["roof_" + name] = (m, quad, poly)
    # the cut edge: the ends of the reeds, dark and wet, a paler lip along its top where the rain runs off
    for (a_u, a_t, b_u, b_t), colr, name, sd in (((A0u, A0t, B0u, B0t), lerp(thatch_shade, PRUSSIAN, 0.34), "W", 44), ((A0u, A0t, D0u, D0t), lerp(THATCH, PRUSSIAN, 0.26), "D", 45)):
        quad = [a_u, b_u, b_t, a_t]
        m = mask_poly(SHAPE, hand(quad, 0.5, seed + sd))
        s_, t_ = quad_st(quad)
        reed = noise(SHAPE, (2.4, 22.0), seed + sd + 1, 2)
        field = colr[None, None, :] * (1 + (reed - 0.5)[..., None] * 0.34)
        field = lerp(field * (SHADE * 1.5)[None, None, :], field, smooth(np.clip(t_, 0, 1) * 1.4)[..., None])
        over(pic, far_of_pic(np.clip(field, 0, 1), np.full(SHAPE, t_air, F32)), m)
        crisp = np.maximum(crisp, m)
        info["edge" + name] = (m, quad)
    # the ridge: a cap of cedar bark held down by bamboo, sagging a little, its ends rounded off
    sag = lambda q: (R0[0] + (R1[0] - R0[0]) * q, R0[1] + (R1[1] - R0[1]) * q + 2.6 * math.sin(math.pi * q))
    qs = np.linspace(-0.07, 1.07, 13)
    hgt = lambda q: 7.5 * (1 - max(0.0, abs(q - 0.5) - 0.46) * 9.0)
    cap_top = [(sag(q)[0], sag(q)[1] - hgt(q)) for q in qs]
    cap_bot = [(sag(q)[0], sag(q)[1] + 4.5) for q in qs]
    m = flat(cap_top + cap_bot[::-1], far_of(lerp(BARK, SKYC, 0.16), t_air + 0.22), 0.4, 46)
    crisp = np.maximum(crisp, m)
    info["ridge"] = (R0, R1, sag)
    info["house_crisp"] = crisp
    info["crisp"] = np.maximum(info.get("crisp", np.zeros(SHAPE, F32)), np.maximum(crisp, under))
    info["eaves"] = dict(A0u=A0u, B0u=B0u, D0u=D0u, A0t=A0t, B0t=B0t, D0t=D0t, R0=R0, R1=R1)
    return pic


# ================================================================ the ground of the play: the yard, the steps
PUDDLES = []                                                    # [(picture x, y, half width, half height)]: measured as they are painted


def lerp_pt(a, b, q):
    return (a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q)


def yard(pic, info, seed=81):
    """The trodden ground before the storehouse's two walls and along to the bank and the kiln: bare wet earth, a shade
    lighter than the needles round it (it holds the sky), its edge lost in them; under the thatch a strip that the rain
    never reaches, dry and pale, and at its edge the line of pebbles where the eaves drip."""
    Hs = HOUSE
    LW, LD, e = Hs.LW, Hs.LD, Hs.eave
    g = info["ground"]
    m = mask_poly(SHAPE, WALK[11:23] + [(700, 520), (640, 524), (560, 540), (470, 548), (400, 548), (350, 530), (330, 512), (268, 508), (262, 484)], soft=5.0, wobble=5.0, seed=seed)
    m = step(0.30, 0.72, m + (noise(SHAPE, (46, 16), seed + 1, 3) - 0.5) * 0.5) * g
    gx, gd = info["gx"], info["gd"]
    t = air(gd).astype(F32)
    earth = lerp(lerp(EARTH, STONE, 0.50), SKYC, 0.30)
    field = earth[None, None, :] * (1 + ((wnoise(gx, gd, 60.0, seed + 2, 4) - 0.5) * 0.24 + (wnoise(gx, gd, 14.0, seed + 3, 3) - 0.5) * 0.14)[..., None])
    over(pic, far_of_pic(np.clip(field, 0, 1), t), (m * 0.86).astype(F32))
    info["yard"] = m
    # the dry strip under the eaves, both walls
    dry = [Hs.foot(-e + 8, LD + 20), Hs.foot(-e + 8, -e + 8), Hs.foot(LW + 20, -e + 8), Hs.foot(LW + 20, 0), Hs.foot(0, 0), Hs.foot(0, LD + 20)]
    dm = mask_poly(SHAPE, dry, soft=1.2, wobble=1.6, seed=seed + 4) * g
    over(pic, far_of(lerp(lerp(EARTH, OCHRE, 0.16), WHITE, 0.26), float(air(Hs.corner[1]))), (dm * 0.70).astype(F32))
    info["dry"] = dm
    return pic


def path(pic, info, seed=91):
    """The stone steps, through the camera: each tread level and worn, of two or three slabs with earth and moss in the
    joints, each riser a low dark wet face; the wet stone holds the sky, most where we see it at a low angle (the far
    treads are the lightest ground in the picture), and a puddle lies on four of them."""
    rng = np.random.default_rng(seed)
    crisp = np.zeros(SHAPE, F32)
    st = steps()
    ft, fy = foot_tread()
    treads = [(ft, fy, None)] + [(s_["tread"], s_["Y"], s_) for s_ in st]
    PUDDLES.clear()
    marks = []
    for i, (outline, Y, riser) in enumerate(treads):
        pts = [level(x, d, Y) for (x, d) in outline]
        dmean = float(np.mean([q[1] for q in outline]))
        t = float(air(dmean))
        # how much sky the wet stone gives back: more where the look is low (far), less at our feet
        look = float(np.clip((dmean - 700.0) / 520.0, 0, 1))
        m = mask_poly(SHAPE, pts, wobble=1.2, seed=seed + i)
        base = lerp(lerp(STONE, PRUSSIAN, 0.40), lerp(STONE, SKYC, 0.60), look ** 0.8)
        blot = noise(SHAPE, (64, 20), seed + 20 + i, 4)
        fine = noise(SHAPE, (9, 4), seed + 40 + i, 3)
        field = base[None, None, :] * (1 + ((blot - 0.5) * 0.24 + (fine - 0.5) * 0.12)[..., None])
        # the sky's own light lying on the wet, in broken level streaks, most toward the gap
        streak = step(0.52, 0.70, noise(SHAPE, (70, 3.2), seed + 60 + i, 3)) * (0.35 + 0.65 * look)
        field = lerp(field, lerp(SKYC, PAPER, 0.25)[None, None, :], (streak * 0.20)[..., None])
        over(pic, far_of_pic(np.clip(field, 0, 1), np.full(SHAPE, t, F32)), m)
        crisp = np.maximum(crisp, m)
        marks.append((pts, Y, outline, t, look))
    # the risers, over the treads below them: each of two to four stones, no two alike
    risers = []
    for i, s_ in enumerate(st):
        t = float(air(s_["D"]))
        n = int(rng.integers(2, 5))
        cuts = sorted([0.0, 1.0] + [float(q) for q in rng.uniform(0.18, 0.82, n - 1)])
        for a, b in zip(cuts[:-1], cuts[1:]):
            pa, pb = lerp_pt(s_["l"], s_["r"], a), lerp_pt(s_["l"], s_["r"], b)
            back = rng.uniform(-7.0, 7.0)                           # this stone sits a little forward or back
            up = rng.uniform(-1.6, 1.6)
            pa, pb = (pa[0], pa[1] + back), (pb[0], pb[1] + back + rng.uniform(-3, 3))
            quad = [level(pa[0], pa[1], s_["Y0"] - 1.0), level(pb[0], pb[1], s_["Y0"] - 1.0), level(pb[0], pb[1], s_["Y"] + up), level(pa[0], pa[1], s_["Y"] + up)]
            colr = far_of(lerp(lerp(STONE, PRUSSIAN, 0.62), SIENNA, 0.06 + 0.08 * rng.random()), t)
            m = mask_poly(SHAPE, quad, wobble=0.7, seed=seed + 100 + i)
            over(pic, colr, m)
            crisp = np.maximum(crisp, m)
            risers.append((quad, t))
    # the puddles: on the treads above the first, third, fourth and sixth risers; level, so they lie as ellipses
    for (i, q, w_cm, d_cm) in ((0, 0.62, 62.0, 30.0), (2, 0.36, 50.0, 24.0), (3, 0.70, 44.0, 20.0), (5, 0.45, 40.0, 18.0)):
        s_ = st[i]
        nxt = st[i + 1] if i + 1 < len(st) else None
        a = lerp_pt(s_["l"], s_["r"], q)
        b = lerp_pt(nxt["l"], nxt["r"], q) if nxt else (a[0], a[1] + 60.0)
        c = lerp_pt(a, b, 0.52)
        ring = [level(c[0] + math.cos(k) * w_cm, c[1] + math.sin(k) * d_cm, s_["Y"]) for k in np.linspace(0, 2 * math.pi, 28, endpoint=False)]
        m = mask_poly(SHAPE, ring, wobble=1.0, seed=seed + 200 + i)
        over(pic, far_of(lerp(lerp(SKYC, PAPER, 0.55), COBALT, 0.06), float(air(s_["D"])) * 0.5), m * 0.92)
        xs, ys = [p_[0] for p_ in ring], [p_[1] for p_ in ring]
        PUDDLES.append(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (max(xs) - min(xs)) / 2, (max(ys) - min(ys)) / 2))
        crisp = np.maximum(crisp, m)
        info.setdefault("puddle_rings", []).append(ring)
    info["treads"] = marks
    info["risers"] = risers
    info["steps_mask"] = crisp
    info["crisp"] = np.maximum(info.get("crisp", np.zeros(SHAPE, F32)), crisp)
    return pic


def stepping_stones(pic, info, seed=95):
    """Flat stones laid from the top of the steps to the stone before the door, and a few along the window's wall: set
    in the earth, level with it, wet."""
    Hs = HOUSE
    places = [G(430, 520), G(445, 511), G(462, 505), Hs.out_window(120.0, 150.0), Hs.out_window(250.0, 150.0), Hs.out_window(390.0, 150.0)]
    rng = np.random.default_rng(seed)
    stones = []
    for i, (x, d) in enumerate(places):
        rx, rd = rng.uniform(26, 36), rng.uniform(18, 26)
        ph = rng.uniform(0, 6.3)
        ring = [on(x + math.cos(k) * rx * (1 + 0.16 * math.sin(3 * k + ph)), d + math.sin(k) * rd * (1 + 0.16 * math.cos(2 * k + ph)), 1.5) for k in np.linspace(0, 2 * math.pi, 14, endpoint=False)]
        t = float(air(d))
        over(pic, far_of(lerp(STONE, PRUSSIAN, 0.22), t), mask_poly(SHAPE, ring, wobble=0.6, seed=seed + i))
        stones.append((ring, t))
    info["stones"] = stones
    return pic


# ================================================================ the kiln, the bank and the pipe, the stone figure
def kiln(pic, info, seed=101):
    """The charcoal kiln, cold: a dome of earth as tall as a man's chest, cracked and mossed, its low mouth half walled
    up with stones, soot above it; cut wood stacked beside it. A graded wash round it (lighter toward the gap)."""
    kx, kd = KILN["at"]
    r, h = KILN["r"], KILN["h"]
    t = float(air(kd))
    dome = [on(kx + r * math.cos(a), kd, h * math.sin(a) ** 0.85) for a in np.linspace(0, math.pi, 22)]
    front = [on(kx - r * math.cos(b), kd - r * 0.92 * math.sin(b)) for b in np.linspace(0, math.pi, 16)]
    poly = dome + front[1:-1]
    m = mask_poly(SHAPE, poly, wobble=1.4, seed=seed)
    x0, y0, x1, y1 = box_of(poly)
    cx, cy = on(kx, kd, h * 0.45)
    lx, ly = (PX - cx) / max((x1 - x0) / 2.0, 1), (PY - cy) / max((y1 - y0) / 2.0, 1)
    lit = np.clip(0.55 - lx * 0.55 - ly * 0.50, 0, 1)
    clay = lerp(lerp(OCHRE, SIENNA, 0.45), PRUSSIAN, 0.42)
    field = lerp(shade_of(clay, 0.52)[None, None, :], lerp(clay, SKYC, 0.28)[None, None, :], smooth(lit)[..., None])
    n1 = noise(SHAPE, (26, 18), seed + 1, 4)
    field = field * (1 + (n1 - 0.5)[..., None] * 0.22)
    mossy = step(0.58, 0.72, noise(SHAPE, (22, 12), seed + 2, 3) + (0.2 - ly) * 0.25)
    field = lerp(field, lerp(MOSS, PRUSSIAN, 0.45)[None, None, :], (mossy * 0.45)[..., None])
    foot_shade(pic, kx + 20, kd - 30, r * 0.62, info["ground"], amount=0.5)
    over(pic, far_of_pic(np.clip(field, 0, 1), np.full(SHAPE, t, F32)), m)
    # the mouth, on the side toward the yard (to the right and toward us): an arch, half walled up
    ma = math.radians(-52.0)
    mx, md = kx + r * 0.98 * math.cos(ma), kd + r * 0.98 * math.sin(ma)
    tx, td_ = -math.sin(ma), math.cos(ma)                                   # along the dome's skin, level
    arch = [on(mx + tx * w, md + td_ * w, hh) for (w, hh) in ((-30, 0), (-30, 34), (-22, 52), (-8, 62), (8, 62), (22, 52), (30, 34), (30, 0))]
    am = mask_poly(SHAPE, arch, wobble=0.5, seed=seed + 3)
    soot = mask_poly(SHAPE, [on(mx + tx * w, md + td_ * w, hh) for (w, hh) in ((-34, 30), (-26, 64), (-6, 96), (14, 92), (30, 62), (36, 30))], soft=3.0)
    tint(pic, SHADE * 0.9, (soot * 0.55 * m).astype(F32))
    over(pic, far_of(lerp(PRUSSIAN, SIENNA, 0.10), t * 0.3), am)
    stones = []
    for j, (w, hh, rr) in enumerate(((-18, 8, 12), (2, 8, 13), (20, 9, 11), (-8, 25, 11), (12, 26, 10))):
        cxy = on(mx + tx * w, md + td_ * w - 6.0, hh)
        k = CAM.px_cm(mx, md)
        stones.append((cxy[0], cxy[1], rr * k * 1.1, rr * k * 0.8))
        over(pic, far_of(lerp(STONE, PRUSSIAN, 0.30 + 0.1 * (j % 2)), t), mask_ellipse(SHAPE, cxy[0], cxy[1], rr * k * 1.1, rr * k * 0.8, wobble=0.5, seed=seed + 4 + j))
    # cut wood stacked to its left: the round ends toward us
    logs = []
    k = CAM.px_cm(kx, kd)
    for row in range(3):
        for j in range(5 - row):
            wx = kx - r * 0.55 - j * 21.0 - row * 10.5
            c = on(wx, kd - r - 40.0, 11.0 + row * 19.0)
            logs.append((c[0], c[1], 10.0 * k))
    for (cx_, cy_, rr) in logs:
        over(pic, far_of(lerp(BARK, PRUSSIAN, 0.25), t), mask_ellipse(SHAPE, cx_, cy_, rr * 1.1, rr * 1.05))
        over(pic, far_of(lerp(lerp(lerp(OCHRE, WHITE, 0.35), SIENNA, 0.15), PRUSSIAN, 0.30), t), mask_ellipse(SHAPE, cx_, cy_, rr * 0.82, rr * 0.80))
    info["kiln"] = dict(poly=poly, arch=arch, mask=m, logs=logs, stones=stones)
    info["crisp"] = np.maximum(info.get("crisp", np.zeros(SHAPE, F32)), m)
    return pic


def bank(pic, info, seed=111):
    """Behind the storehouse's far end the hill has been cut back: a bank of wet earth as high as a man, roots hanging
    out of it, moss and ferns along its lip; the bamboo pipe comes out of it at the height of an ear."""
    poly = BANK_FOOT + BANK_TOP[::-1]
    m = mask_poly(SHAPE, poly, wobble=2.4, seed=seed)
    d = PIPE["at"][1] + 40.0
    t = float(air(d))
    up = np.clip((PY - 372.0) / 110.0, 0, 1)
    earth = lerp(lerp(EARTH, SIENNA, 0.12), PRUSSIAN, 0.18)
    field = lerp(lerp(earth, SKYC, 0.10)[None, None, :], shade_of(earth, 0.30)[None, None, :], up[..., None])
    n1 = noise(SHAPE, (30, 12), seed + 1, 4)
    n2 = noise(SHAPE, (7, 22), seed + 2, 3)
    field = field * (1 + ((n1 - 0.5) * 0.26 + (n2 - 0.5) * 0.14)[..., None])
    mossy = step(0.50, 0.70, n1 * 0.6 + (1 - up) * 0.55)
    field = lerp(field, lerp(MOSS, PRUSSIAN, 0.42)[None, None, :], (mossy * 0.6)[..., None])
    over(pic, far_of_pic(np.clip(field, 0, 1), np.full(SHAPE, t, F32)), m)
    # the shade it stands in at its foot
    tint(pic, SHADE * 1.5, (mask_poly(SHAPE, BANK_FOOT + [(800, 500), (694, 478)], soft=3.0) * 0.36 * info["ground"]).astype(F32))
    info["bank"] = dict(poly=poly, mask=m, t=t)
    info["crisp"] = np.maximum(info["crisp"], m)
    return pic


def pipe_points():
    return pipe_ends()


def pipe(s, t=0.0, alpha=1.0):
    a, b = pipe_points()
    bamboo = far_of(lerp(lerp(lerp(OCHRE, VERONESE, 0.45), WHITE, 0.30), PRUSSIAN, 0.34), t)
    s.line([lerp_pt(a, b, 0.12), b], far_of(lerp(BARK_DARK, PRUSSIAN, 0.3), t), 5.0, alpha, round_ends=False)
    s.line([a, b], bamboo, 3.2, alpha, round_ends=False)
    s.ellipse(a[0] + 1.5, a[1] + 0.5, 4.5, 3.6, far_of(lerp(EARTH, PRUSSIAN, 0.25), t), alpha)
    s.line([(a[0], a[1] - 0.9), (b[0], b[1] - 0.9)], far_of(lerp(bamboo, SKYC, 0.5), t), 0.9, alpha * 0.8)
    for q in (0.34, 0.70):
        c = lerp_pt(a, b, q)
        s.line([(c[0] - 0.6, c[1] - 2.6), (c[0] + 0.6, c[1] + 2.6)], far_of(lerp(SIENNA, PRUSSIAN, 0.4), t), 1.0, alpha)
    s.ellipse(b[0], b[1], 2.3, 2.7, far_of(PRUSSIAN, t * 0.5), alpha)
    return a, b


def figure(pic, info, seed=121):
    """The small stone figure by the lower steps: a roadside Jizo, worn smooth, hands together, in a red bib; on a flat
    stone, three pebbles and a coin before it. Round and simple; nothing on it crosses anything."""
    jx, jd = JIZO["at"]
    h = JIZO["h"]
    t = float(air(jd)) * 0.6
    k = CAM.px_cm(jx, jd)
    fx, fy = on(jx, jd)
    stone = lerp(WHITE, PRUSSIAN, 0.40)
    s = Paper(SHAPE)
    # the base stone
    ring = [on(jx + math.cos(a) * 24.0, jd + math.sin(a) * 15.0, 5.0) for a in np.linspace(0, 2 * math.pi, 14, endpoint=False)]
    foot_shade(pic, jx + 6, jd - 4, 12.0, info["ground"], amount=0.5)
    s.poly([(p_[0], p_[1] + 5.0 * k) for p_ in ring], far_of(lerp(stone, PRUSSIAN, 0.45), t), 1.0)
    s.poly(ring, far_of(lerp(stone, PRUSSIAN, 0.16), t), 1.0)
    top = fy - (h + 5.0) * k
    by = fy - 5.0 * k
    bw = 11.5 * k
    body = [(fx - bw, by), (fx + bw, by), (fx + bw * 0.92, by - h * 0.30 * k), (fx + bw * 0.80, by - h * 0.56 * k), (fx + bw * 0.42, by - h * 0.64 * k),
            (fx - bw * 0.42, by - h * 0.64 * k), (fx - bw * 0.80, by - h * 0.56 * k), (fx - bw * 0.92, by - h * 0.30 * k)]
    s.poly(body, far_of(stone, t), 1.0)
    s.poly([(fx + bw * 0.10, by), (fx + bw, by), (fx + bw * 0.92, by - h * 0.30 * k), (fx + bw * 0.80, by - h * 0.56 * k), (fx + bw * 0.42, by - h * 0.64 * k), (fx + bw * 0.16, by - h * 0.64 * k)],
           far_of(shade_of(stone, 0.34), t), 1.0)
    hr = 8.6 * k
    hc = (fx, by - h * 0.64 * k - hr * 0.80)
    s.ellipse(hc[0], hc[1], hr, hr * 1.06, far_of(stone, t), 1.0)
    s.poly([(hc[0] + hr * 0.18, hc[1] - hr), (hc[0] + hr * 0.80, hc[1] - hr * 0.62), (hc[0] + hr, hc[1]), (hc[0] + hr * 0.78, hc[1] + hr * 0.66), (hc[0] + hr * 0.2, hc[1] + hr * 1.0)],
           far_of(shade_of(stone, 0.34), t), 1.0)
    # the bib: red cloth tied at the neck, hanging to a rounded hem; a darker fold on the shade side
    bib = [(fx - bw * 0.72, by - h * 0.60 * k), (fx + bw * 0.72, by - h * 0.60 * k), (fx + bw * 0.80, by - h * 0.40 * k), (fx + bw * 0.46, by - h * 0.25 * k),
           (fx, by - h * 0.21 * k), (fx - bw * 0.46, by - h * 0.25 * k), (fx - bw * 0.80, by - h * 0.40 * k)]
    s.poly(bib, far_of(lerp(VERMILION, SIENNA, 0.12), t * 0.5), 1.0)
    s.poly([(fx + bw * 0.14, by - h * 0.60 * k), (fx + bw * 0.72, by - h * 0.60 * k), (fx + bw * 0.80, by - h * 0.40 * k), (fx + bw * 0.46, by - h * 0.25 * k), (fx + bw * 0.12, by - h * 0.22 * k)],
           far_of(lerp(VERMILION, PRUSSIAN, 0.30), t * 0.5), 1.0)
    # pebbles and a coin on the base stone before it
    for (dx, dz, rr, c) in ((-12.0, -9.0, 3.2, 0.2), (-5.0, -11.0, 2.8, 0.34), (-9.0, -10.5, 2.2, 0.1)):
        c0 = on(jx + dx, jd + dz, 5.0 + rr * (2.2 if rr < 2.5 else 0.8))
        s.ellipse(c0[0], c0[1], rr * k * 1.1, rr * k * 0.8, far_of(lerp(stone, PRUSSIAN, c), t), 1.0)
    c0 = on(jx + 9.0, jd - 10.0, 5.6)
    s.ellipse(c0[0], c0[1], 1.9 * k, 1.0 * k, far_of(lerp(OCHRE, PRUSSIAN, 0.35), t), 1.0)
    colr, alpha = s.done()
    over(pic, colr, alpha)
    info["figure"] = dict(box=[fx - bw - 4, top - 4, fx + bw + 4, fy + 6], body=body, head=(hc[0], hc[1], hr), bib=bib, k=k, foot=(fx, fy))
    info["crisp"] = np.maximum(info["crisp"], alpha)
    return pic


# ================================================================ what grows: ferns, tufts, boughs
FERN = lerp(lerp(lerp(VIRIDIAN, VERONESE, 0.55), OCHRE, 0.20), PRUSSIAN, 0.22)


def fern(s, x, d, size, seed, t=0.0, base=0.0, n=None, dark=0.0, spread=1.0, lit=0.25):
    """A clump of fern on the hillside at (x, d): fronds that rise from one foot and arch over, each a midrib with its
    leaflets getting shorter to the tip; drawn in the world (so the fronds toward us hang down the picture, the ones
    away stand up behind), `size` cm long. `t`: the air between; `dark`: 0..1 toward the near plane's deep green."""
    rng = np.random.default_rng(seed)
    n = n or int(rng.integers(6, 10))
    k = CAM.px_cm(x, d, base)
    fronds = []
    for j in range(n):
        az = rng.uniform(0, 2 * math.pi)
        L = size * rng.uniform(0.65, 1.1)
        rise = rng.uniform(0.34, 0.62)
        pts3 = []
        for q in np.linspace(0, 1, 9):
            out = L * 0.86 * q * spread
            hh = L * (rise * math.sin(q * math.pi * 0.62) * 1.25 - 0.10 * q * q)
            pts3.append((x + math.cos(az) * out, d - math.sin(az) * out, base + max(hh, 0.0) + 2.0))
        fronds.append((math.sin(az), L, [on(*q) for q in pts3]))
    fronds.sort(key=lambda f: -f[0])                              # the ones that lean away first, the ones toward us last
    for depth_, L, pp in fronds:
        tone = rng.uniform(0, 1)
        c = lerp(lerp(FERN, PRUSSIAN, 0.18 + 0.5 * dark), lerp(FERN, VERONESE, 0.30), lit * tone * (1 - dark * 0.6))
        c = far_of(c, t)
        wmid = max(0.7, 0.012 * L * k)
        s.line(pp, far_of(lerp(FERN, PRUSSIAN, 0.45 + 0.3 * dark), t), wmid, 1.0)
        for i in range(1, len(pp)):
            a, b = pp[i - 1], pp[i]
            dx, dy = b[0] - a[0], b[1] - a[1]
            ln = math.hypot(dx, dy) or 1.0
            nx, ny = -dy / ln, dx / ln
            q = i / (len(pp) - 1)
            reach = L * k * 0.20 * (1 - q) ** 0.7 * (0.55 + 0.45 * min(q * 5, 1))
            if reach < 0.8:
                continue
            steps_ = max(1, int(ln / max(1.6, 0.03 * L * k)))
            for m_ in range(steps_):
                f = (m_ + 0.5) / steps_
                cx_, cy_ = a[0] + dx * f, a[1] + dy * f
                back = 0.35 * reach
                for sgn in (-1, 1):
                    s.line([(cx_, cy_), (cx_ + sgn * nx * reach + dx / ln * back, cy_ + sgn * ny * reach + dy / ln * back)], c, max(0.8, 0.018 * L * k), 1.0)
    return k


def tuft(s, x, d, size, seed, t=0.0, colr=None):
    """A tuft of grass or young fern: a few blades from one foot."""
    rng = np.random.default_rng(seed)
    f = on(x, d)
    k = CAM.px_cm(x, d)
    c = far_of(colr if colr is not None else lerp(FERN, OCHRE, 0.18), t)
    for j in range(int(rng.integers(4, 8))):
        a = rng.uniform(-1.0, 1.0)
        L = size * k * rng.uniform(0.6, 1.1)
        s.line([f, (f[0] + math.sin(a) * L * 0.45, f[1] - L * 0.7), (f[0] + math.sin(a) * L * 0.9, f[1] - L * 0.82)], c, max(0.7, 0.05 * size * k), 1.0)


def ground_dressing(pic, info, seed=131):
    """What lies and grows on the hillside, at a true count for each square metre (depth.scatter: few and large near us,
    many and small far off): stones, fallen twigs, tufts, and ferns in drifts along the path's edges, round the feet of
    the trunks and under the bank. Nothing on the trodden ground or the steps."""
    zone = info["ground"] * (1 - np.clip(info.get("yard", 0) * 1.4, 0, 1)) * (1 - info["steps_mask"]) * (1 - info["house_crisp"]) * (1 - info["under_floor"])
    zone = zone * (1 - info["kiln"]["mask"]) * (1 - info["bank"]["mask"])
    zone = (blur(zone, 1.5) > 0.8).astype(F32)
    pt = lambda X, Z: on(X, Z)
    kk = lambda X, Z: CAM.px_cm(X, Z)
    bounds = (-1500.0, 1500.0, 560.0, 3000.0)
    s = Paper(SHAPE)
    # stones, half sunk and mossed: few, each a broken shape with its light on the side toward the gap
    srng = np.random.default_rng(seed + 9)
    for (x, y, k, r) in DEPTH.scatter(pt, kk, bounds, 0.16, seed, size=(16.0, 9.0), zone=zone):
        X, D_ = G(x, y)
        t = float(air(D_))
        rx, ry = (7.0 + 15.0 * r) * k, (4.0 + 7.0 * r) * k
        ph = srng.uniform(0, 6.3)
        ring = [(x + math.cos(a_) * rx * (1 + 0.22 * math.sin(3 * a_ + ph)), y - ry * 0.45 + math.sin(a_) * ry * (1 + 0.2 * math.cos(2 * a_ + ph))) for a_ in np.linspace(0, 2 * math.pi, 11, endpoint=False)]
        s.ellipse(x + rx * 0.3, y + ry * 0.15, rx * 1.2, ry * 0.8, far_of(lerp(EARTH, PRUSSIAN, 0.55), t), 0.7)
        s.poly(ring, far_of(lerp(STONE, PRUSSIAN, 0.46), t), 1.0)
        s.poly([(x + (px_ - x) * 0.62 - rx * 0.22, (y - ry * 0.45) + (py_ - (y - ry * 0.45)) * 0.5 - ry * 0.28) for (px_, py_) in ring], far_of(lerp(lerp(STONE, PRUSSIAN, 0.22), MOSS, 0.45 * (r > 0.5)), t), 1.0)
    # fallen twigs and strips of bark
    rng = np.random.default_rng(seed + 1)
    for (x, y, k, r) in DEPTH.scatter(pt, kk, bounds, 0.8, seed + 2, size=(30.0, 2.0), zone=zone):
        X, D_ = G(x, y)
        t = float(air(D_))
        a = rng.uniform(-0.5, 0.5) + (math.pi if r > 0.5 else 0)
        L = (14.0 + 30.0 * r) * k
        s.line([(x - math.cos(a) * L / 2, y - math.sin(a) * L * 0.18), (x + math.cos(a) * L / 2, y + math.sin(a) * L * 0.18)], far_of(lerp(BARK, PRUSSIAN, 0.2 + 0.4 * r), t), max(0.7, 1.6 * k), 0.85)
    # tufts
    for (x, y, k, r) in DEPTH.scatter(pt, kk, bounds, 1.6, seed + 3, size=(16.0, 16.0), zone=zone):
        X, D_ = G(x, y)
        if wnoise(np.float32(X), np.float32(D_), 240.0, seed + 4) < 0.45:
            continue
        tuft(s, X, D_, 12.0 + 12.0 * r, seed + int(x * 7 + y), t=float(air(D_)))
    # ferns: in drifts (by a noise that lies on the ground), thick along the steps' edges and under the trunks
    left, right, mid = path_edges(n=10)
    edge_pts = left + right
    places = []
    for (x, y, k, r) in DEPTH.scatter(pt, kk, bounds, 0.9, seed + 5, size=(50.0, 40.0), zone=zone):
        X, D_ = G(x, y)
        near_path = min(math.hypot(X - q[0], D_ - q[1]) for q in edge_pts)
        drift = float(wnoise(np.float32(X), np.float32(D_), 330.0, seed + 6))
        if drift + (0.30 if near_path < 70 else 0.0) < 0.62:
            continue
        places.append((X, D_, r))
    # (and a few set by hand where the picture wants them: beside the figure, along the foot of the bank, at the kiln,
    # down the slope below the yard)
    jx, jd = JIZO["at"]
    for (dx, dz, sz) in ((52.0, 26.0, 46.0), (-44.0, 34.0, 30.0)):
        places.append((jx + dx, jd + dz, sz / 60.0))
    for (px_, py_, sz) in ((708, 474, 34), (776, 488, 40), (262, 474, 30), (176, 520, 40), (640, 562, 50), (560, 570, 44), (492, 560, 36), (604, 536, 30)):
        X, D_ = G(px_, py_)
        places.append((X, D_, sz / 60.0))
    places.sort(key=lambda q: -q[1])
    for i, (X, D_, r) in enumerate(places):
        fx, fy = on(X, D_)
        if not (0 <= fx < W and 0 <= fy < H) or zone[int(fy), int(fx)] < 0.5:
            continue
        fern(s, X, D_, 28.0 + 34.0 * r, seed + 20 + i, t=float(air(D_)), dark=float(np.clip((900.0 - D_) / 500.0, 0, 0.5)))
    a_, b_ = G(452, 590), G(612, 566)
    t_f = float(air(a_[1]))
    spine = [on(a_[0] + (b_[0] - a_[0]) * q, a_[1] + (b_[1] - a_[1]) * q, 4.0 + 5.0 * math.sin(q * 3.1)) for q in np.linspace(0, 1, 9)]
    s.taper(spine, far_of(lerp(BARK_DARK, PRUSSIAN, 0.2), t_f), 4.6, 1.6, 1.0)
    s.taper([(q[0], q[1] - 1.2) for q in spine], far_of(lerp(BARK, SKYC, 0.3), t_f), 1.2, 0.6, 0.7)
    for (i, dx_, dy_) in ((2, 10, -16), (3, -6, 15), (4, 12, -20), (5, -8, 12), (6, 9, -13), (7, 6, 10)):
        c = spine[i]
        s.taper([c, (c[0] + dx_ * 0.6, c[1] + dy_ * 0.55), (c[0] + dx_ * 1.5, c[1] + dy_)], far_of(lerp(BARK_DARK, PRUSSIAN, 0.2), t_f), 1.8, 0.7, 1.0)
    colr, alpha = s.done()
    over(pic, colr, alpha)
    info["dressing"] = alpha
    return pic


def bough(s, foot, tip, colr, wood, seed, thick=30.0, lit=None, fingers=1.0, marks=None):
    """A cedar bough from `foot` (on its trunk) out to `tip` (picture points): an arm that sags and lifts again at its
    end, with twigs leaving it downward; the green sits on arm and twigs in tufts, each a fan of short needles pointing
    down and outward, so that the whole has a body with a bristling, scalloped lower edge (`thick`: how far it hangs,
    px). `lit`: a lighter green for the tufts along its top, toward the sky. `marks`: a second sheet for the needles
    that are drawn (laid again after the brush, crisp)."""
    rng = np.random.default_rng(seed)
    dx, dy = tip[0] - foot[0], tip[1] - foot[1]
    ln = math.hypot(dx, dy) or 1.0
    n = max(7, int(ln / max(7.0, thick * 0.34)))
    sag = ln * rng.uniform(0.02, 0.13)
    hump = ln * rng.uniform(0.0, 0.07)
    spine = [(foot[0] + dx * q, foot[1] + dy * q + sag * math.sin(q * math.pi) - sag * 0.5 * q ** 3 - hump * math.sin(q * math.pi * 0.55)) for q in np.linspace(0, 1, n)]
    full = rng.uniform(0.35, 0.65)
    prof = lambda q: math.sin(math.pi * (0.05 + 0.95 * q)) ** 0.5 * (full + (1 - full) * q)
    needle = max(1.0, thick * 0.045)
    m = marks if marks is not None else s

    def tuft(c, L, spread=1.0, down=1.0, colr_=colr, k=9, sheet=None):
        sheet = sheet or s
        for j in range(k):
            a_ = math.pi / 2 + (j / (k - 1) - 0.5) * 1.9 * spread + rng.normal(0, 0.10)
            ll = L * rng.uniform(0.7, 1.1) * (1.0 - 0.35 * abs(j / (k - 1) - 0.5) * 2)
            e_ = (c[0] + math.cos(a_) * ll, c[1] + math.sin(a_) * ll * down)
            sheet.taper([c, e_], colr_, needle * 1.7, needle * 0.6, 1.0)

    top, bot = [], []
    for i, (px_, py_) in enumerate(spine):
        q = i / (n - 1)
        f = prof(q)
        top.append((px_, py_ - thick * 0.16 * f * rng.uniform(0.5, 1.5)))
        bot.append((px_, py_ + thick * 0.46 * f * rng.uniform(0.8, 1.2)))
    s.poly(top + bot[::-1], colr, 1.0)                           # the body
    for i in range(1, n - 1):                                     # tufts lifting along its top (the same green: the outline bristles above as below)
        px_, py_ = top[i]
        f = prof(i / (n - 1))
        for j in range(4):
            a_ = -math.pi / 2 + rng.normal(0, 0.75)
            ll = thick * 0.30 * f * rng.uniform(0.5, 1.2)
            c0 = (px_ + rng.normal(0, thick * 0.12), py_ + 2.0)
            s.taper([c0, (c0[0] + math.cos(a_) * ll, c0[1] + math.sin(a_) * ll)], colr, needle * 1.8, needle * 0.6, 1.0)
    for i, (px_, py_) in enumerate(spine):
        q = i / (n - 1)
        f = prof(q)
        if f < 0.2:
            continue
        # a twig down from the arm, with a tuft at its end and one half way
        tw = (px_ + rng.normal(0, thick * 0.10), py_ + thick * f * rng.uniform(0.55, 1.0))
        s.line([(px_, py_), tw], colr, max(1.2, thick * 0.20), 1.0)
        tuft(tw, thick * 0.52 * f * fingers)
        tuft(lerp_pt((px_, py_), tw, 0.45), thick * 0.50 * f, spread=1.25)
        tuft((px_, py_ + thick * 0.2 * f), thick * 0.44 * f, spread=1.5, sheet=m)
    if lit is not None:                                           # the top's lighter tufts: short, lifting
        for i in range(1, n - 1):
            px_, py_ = top[i]
            for j in range(3):
                a_ = -math.pi / 2 + rng.normal(0, 0.7)
                ll = thick * 0.20 * rng.uniform(0.6, 1.1)
                m.taper([(px_ + rng.normal(0, 3), py_ + 1.5), (px_ + math.cos(a_) * ll, py_ + math.sin(a_) * ll)], lit, needle * 1.4, needle * 0.5, 1.0)
    s.taper(spine[: max(3, n // 3)], wood, max(1.2, thick * 0.11), max(0.8, thick * 0.05), 1.0)
    return spine


def top_canopy(pic, info, seed=141):
    """Above the storehouse the crowns begin: the nearer cedars' lowest boughs reach in across the top of the picture
    (one lies across the ridge), and at the very top their crowns close. Middle distance: paler than anything near,
    deeper than the ranks behind; the gap on the left stays open."""
    x, y = PX, PY
    base = 30.0 + (x / W) * 46.0 - 46.0 * np.exp(-((x - LIGHT_AT[0]) / 200.0) ** 2)
    can = canopy_field(base, seed, cell=(84.0, 30.0), depth=70.0, ragged=22.0, holes=0.52)
    finger = noise(SHAPE, (9.0, 30.0), seed + 5, 2)
    can = np.clip(can * step(0.25, 0.55, can + (finger - 0.5) * 0.9), 0, 1)
    leaf = far_of(lerp(LEAF, COBALT, 0.10), 0.40)
    deep = far_of(lerp(LEAF, PRUSSIAN, 0.30), 0.28)
    up = np.clip((base - y) / 90.0, 0, 1)
    over(pic, lerp(leaf[None, None, :], deep[None, None, :], smooth(up)[..., None]), (can * 0.88).astype(F32))
    info["soft"] = np.maximum(info["soft"], can * 0.6)
    s = Paper(SHAPE)
    n = 0
    for spec in sorted(TRUNKS_MID, key=lambda t_: t_[1]):
        tx, td_, tr, lean = spec_place(spec)
        if td_ < 1500.0:
            continue                                               # (the nearer ones' boughs begin above the picture)
        tt = float(air(td_)) + 0.12
        k = CAM.px_cm(tx, td_)
        c1 = far_of(lerp(LEAF, PRUSSIAN, 0.20), tt)
        w1 = far_of(lerp(BARK_DARK, SHADE, 0.3), tt)
        lit = far_of(lerp(LEAF, VERONESE, 0.22), tt + 0.05)
        rng = np.random.default_rng(seed + int(spec[0]))
        hgt = rng.uniform(820.0, 980.0)
        tier = 0
        open_left = on(tx, td_)[0] < 330
        while True:
            foot = on(tx + lean * hgt / 100.0, td_, hgt)
            if foot[1] < -30:
                break
            reach = (300.0 - 50.0 * tier) * rng.uniform(0.75, 1.1) * (0.6 if open_left else 1.0)
            for side in (-1, 1):
                if rng.random() < 0.35 or tier > 2:
                    continue
                n += 1
                L = reach * rng.uniform(0.7, 1.1)
                tip = on(tx + lean * hgt / 100.0 + side * L, td_, hgt - L * rng.uniform(0.20, 0.34))
                bough(s, foot, tip, c1, w1, seed + 10 + n, thick=max(9.0, 64.0 * k), lit=lit, fingers=0.9)
            hgt += rng.uniform(260.0, 360.0)
            tier += 1
    # the old cedar left of the path keeps one low bough, reaching out over the gap, and the stump of another
    bx, bd, br, blean = spec_place(TRUNKS_MID[0])
    bg = trunk_geom(bx, bd, br, blean, seed=51)
    tb = float(air(bd)) + 0.10
    foot = (edge_at(bg, 88.0, 1) - 3.0, 88.0)
    bough(s, foot, (foot[0] + 132.0, 124.0), far_of(lerp(LEAF, PRUSSIAN, 0.26), tb), far_of(lerp(BARK_DARK, SHADE, 0.2), tb), seed + 91, thick=32.0,
          lit=far_of(lerp(LEAF, VERONESE, 0.24), tb + 0.04), fingers=1.0)
    foot = (edge_at(bg, 26.0, 1) - 3.0, 26.0)
    bough(s, foot, (foot[0] + 84.0, 44.0), far_of(lerp(LEAF, PRUSSIAN, 0.26), tb), far_of(lerp(BARK_DARK, SHADE, 0.2), tb), seed + 92, thick=26.0,
          lit=far_of(lerp(LEAF, VERONESE, 0.24), tb + 0.04), fingers=1.0)
    colr, alpha = s.done()
    over(pic, colr, alpha)
    info["boughs_mid"] = alpha
    return pic


def foot_ferns(pic, info, seed=151):
    """Ferns at the feet of the backdrop's nearer trunks and of the kiln, in front of them (laid after them)."""
    s = Paper(SHAPE)
    n = 0
    for spec in TRUNKS_MID:
        x, d, r, lean = spec_place(spec)
        if d > HOUSE.corner[1] + 200.0:
            continue
        for (dx, dz, sz) in ((-r * 2.2, -r * 1.4, 40.0), (r * 1.8, -r * 2.0, 48.0), (r * 0.2, -r * 2.8, 34.0)):
            n += 1
            fern(s, x + dx, d + dz, sz, seed + n, t=float(air(d + dz)), dark=float(np.clip((900.0 - d) / 500.0, 0, 0.5)) + 0.15)
    kx, kd = KILN["at"]
    for (dx, dz, sz) in ((KILN["r"] * 0.2, -KILN["r"] * 1.15, 30.0), (-KILN["r"] * 0.7, -KILN["r"] * 1.0, 26.0)):
        n += 1
        fern(s, kx + dx, kd + dz, sz, seed + n, t=float(air(kd)))
    colr, alpha = s.done()
    over(pic, colr, alpha)
    info["dressing"] = np.maximum(info["dressing"], alpha)
    return pic


# ================================================================ under: everything broad, far to near
def under():
    info = {}
    pic = air_layer()
    ground_layer(pic, info)
    far_ranks(pic, info)
    mid_trunks(pic, info, True)
    bank(pic, info)
    kiln(pic, info)
    yard(pic, info)
    path(pic, info)
    stepping_stones(pic, info)
    house(pic, info)
    sp = Paper(SHAPE)
    pipe(sp, info["bank"]["t"])
    colr, alpha = sp.done()
    over(pic, colr, alpha)
    info["crisp"] = np.maximum(info["crisp"], alpha)
    top_canopy(pic, info)
    ground_dressing(pic, info)
    figure(pic, info)
    mid_trunks(pic, info, False)
    foot_ferns(pic, info)
    # the shade the two walk-behind cedars stand in (they are cut-outs: their shade belongs to the ground)
    for spec in CEDAR_L + CEDAR_R:
        x, d, r, lean = spec_place(spec)
        foot_shade(pic, x, d, r, info["ground"], amount=0.40)
    light_and_air(pic, info)
    info["flats"] = pic.copy()
    return np.clip(pic, 0, 1), info


def light_and_air(pic, info):
    """The glazes that hold the picture together: the storehouse's own shade on the ground beside and under it; the deep
    shade of the great cedar over the bottom of the picture, its edge running up the hill from the lower left into the
    picture (the tree itself is behind us and beside us: the front plane); a breath of mist laid over the storehouse's
    far end and the kiln, between them and us."""
    Hs = HOUSE
    g = info["ground"]
    # the storehouse's shade: along the foot of the window's wall and out to the right of the near corner
    sh = [Hs.foot(0, 0), Hs.foot(Hs.LW, 0), Hs.foot(Hs.LW + 40, -120), Hs.foot(120, -150), Hs.foot(-30, -70)]
    tint(pic, SHADE * 1.45, (mask_poly(SHAPE, sh, soft=5.0) * 0.30 * g).astype(F32))
    # the great cedar's shade across the foreground: from off the bottom left, its edge leading in toward the door
    edge = [(0, 470), (120, 505), (250, 548), (400, 574), (560, 584), (800, 566), (800, 600), (0, 600)]
    m = mask_poly(SHAPE, edge, soft=14.0, wobble=10.0, seed=77)
    dapple = 0.72 + 0.28 * step(0.35, 0.65, noise(SHAPE, (90, 30), 78, 3))
    tint(pic, lerp(SHADE, SIENNA, 0.18) * 1.35, np.clip(m * dapple * 0.42, 0, 1).astype(F32))
    # mist between us and the far end of the yard
    veil = np.exp(-((PY - 452.0) / 30.0) ** 2) * (0.4 + 0.6 * noise(SHAPE, (260, 40), 79, 3)) * step(0.0, 1.0, (PX - 80.0) / 200.0)
    over(pic, lerp(SKYC, PAPER, 0.4), np.clip(veil * 0.16 * (1 - info["house_crisp"] * 0.8) * (1 - info["kiln"]["mask"] * 0.8), 0, 1).astype(F32))
    return pic


# ================================================================ the cut-outs
def edge_at(g, row, side):
    """The picture x of a trunk's left (-1) or right (1) edge at a row."""
    pts = g["L"] if side < 0 else g["R"]
    ys, xs = np.array([q[1] for q in pts])[::-1], np.array([q[0] for q in pts])[::-1]
    return float(np.interp(row, ys, xs))


def cedar_cut(spec, seed, info, ferns=(), boughs=()):
    """One of the two cedars people walk behind: the trunk and its roots, a fern or two at its foot, its lowest boughs
    high up, as a layer. `boughs`: (row, side, how far it reaches, how far it hangs), px. -> (rgb, alpha, outline,
    (rgb, alpha) of what is drawn again after the brush)."""
    x, d, r, lean = spec_place(spec)
    g = trunk_geom(x, d, r, lean, seed=seed)
    colr, alpha = trunk_layer(g, seed + 3, detail=1.0, wet=0.7, mist_up=0.38, warm=0.03, rim_left=0.6)
    s, m = Paper(SHAPE), Paper(SHAPE)
    t = float(air(d))
    for sheet in (s, m):
        for i, (dx, dz, sz) in enumerate(ferns):
            fern(sheet, x + dx, d + dz, sz, seed + 30 + i, t=t, dark=0.25)
    leaf = far_of(lerp(LEAF, PRUSSIAN, 0.26), t + 0.10)
    wood = far_of(lerp(BARK_DARK, SHADE, 0.2), t + 0.10)
    lit = far_of(lerp(LEAF, VERONESE, 0.24), t + 0.14)
    for i, (row, side, reach, thick) in enumerate(boughs):
        foot = (edge_at(g, row, side) - side * 3.0, row)
        bough(s, foot, (foot[0] + side * reach, row + reach * 0.30), leaf, wood, seed + 50 + i, thick=thick, lit=lit, fingers=1.0, marks=m)
    fc, fa = s.done()
    out = colr.copy()
    over(out, fc, fa)
    return out, np.maximum(alpha, fa), g, m.done()


def near_plane(info, seed=171):
    """The front plane: the great cedar we stand under, up the left edge and off the top and the bottom, wet, its bark in
    long fibres, a thin cool light down its edge toward the gap; its roots and the ferns at its foot along the bottom
    left; a bough of its neighbour hanging in across the top right corner; fern fronds in the bottom right corner. The
    darkest and warmest shapes in the picture. -> (rgb, alpha, the trunk's outline, (rgb, alpha) of what is drawn on it
    again after the brush: the bark's furrows, the fronds, the needles)."""
    n = NEAR
    g = trunk_geom(n["x"], n["d"], n["r"], 0.6, base=n["bank"], top=2600.0, flare=0.55, flare_h=130.0, seed=seed)
    colr, alpha = trunk_layer(g, seed + 1, detail=1.0, rim=0.7, moss=0.7, wet=0.0, mist_up=0.0, warm=0.06, with_roots=False, extra_air=-float(air(n["d"])), flank=0.45)
    dark = lerp(PRUSSIAN, SIENNA, 0.34)                           # deep and warm: the near plane's tone
    colr = lerp(colr, colr * dark[None, None, :] * 2.5, 0.52)
    out = np.clip(colr, 0, 1)
    s, m = Paper(SHAPE), Paper(SHAPE)
    rng = np.random.default_rng(seed + 2)
    # the bark's furrows and ridges, drawn: long, running with the trunk, breaking and starting again
    L, R = g["L"], g["R"]
    for j in range(54):
        u = rng.uniform(0.22, 0.985)
        i0 = int(rng.integers(0, len(L) - 4))
        i1 = min(len(L) - 1, i0 + int(rng.integers(1, 4)))
        pts = [lerp_pt(L[i], R[i], u + rng.normal(0, 0.006)) for i in range(i0, i1 + 1)]
        pts[0] = lerp_pt(pts[0], pts[1], rng.uniform(0, 0.7))
        pts[-1] = lerp_pt(pts[-2], pts[-1], rng.uniform(0.3, 1.0))
        ridge = j % 3 == 0
        key(m, pts, lerp(lerp(BARK, OCHRE, 0.18), SKYC, 0.10 + 0.25 * (u > 0.8)) if ridge else lerp(PRUSSIAN, SIENNA, 0.20), 1.5 if ridge else 2.0, 0.50 if ridge else 0.62,
            seed=seed + 40 + j, gaps=0.22, dash=30.0)
    for j in range(5):                                            # a plate of bark lifting here and there: a short curved shadow, a light on its edge
        u = rng.uniform(0.45, 0.92)
        i = int(rng.integers(4, len(L) - 6))
        c = lerp_pt(lerp_pt(L[i], R[i], u), lerp_pt(L[i + 1], R[i + 1], u), rng.uniform(0.1, 0.9))
        m.taper([(c[0] - 3, c[1] - 14), (c[0] + 2, c[1]), (c[0] - 2, c[1] + 16)], lerp(PRUSSIAN, SIENNA, 0.18), 3.0, 1.2, 0.7)
        m.line([(c[0] + 1.5, c[1] - 12), (c[0] + 5, c[1]), (c[0] + 1, c[1] + 14)], lerp(BARK, SKYC, 0.3), 1.0, 0.6)
    # the stub of a broken branch high on it
    ex = edge_at(g, 232.0, 1)
    for sheet in (s, m):
        sheet.taper([(ex - 6, 240), (ex + 22, 226), (ex + 44, 208)], lerp(BARK_DARK, PRUSSIAN, 0.35), 11.0, 4.0, 1.0)
        sheet.line([(ex - 2, 234), (ex + 40, 205)], lerp(BARK, SKYC, 0.30), 1.4, 0.8)
    # the roots that run out to the right along the bottom, and the earth they hold
    earth = lerp(lerp(EARTH, PRUSSIAN, 0.50), SIENNA, 0.10)
    s.poly([(0, 546), (70, 554), (118, 570), (150, 588), (168, 604), (0, 604)], earth, 1.0)
    for sheet in (s, m):
        for (pts, wd) in (([(58, 518), (96, 546), (128, 572), (160, 594), (178, 606)], 13.0), ([(40, 546), (70, 572), (104, 594), (120, 606)], 10.0), ([(84, 498), (112, 526), (132, 550)], 7.0)):
            sheet.taper(pts, lerp(BARK_DARK, PRUSSIAN, 0.30), wd, wd * 0.45, 1.0)
            sheet.taper([(q[0] - 1.5, q[1] - wd * 0.28) for q in pts], lerp(BARK, SKYC, 0.16), wd * 0.20, 1.0, 0.8)
    # the ferns at its foot: big fronds, near the lens, their outline against the wet steps
    for sheet in (s, m):
        for i, (px_, py_, sz, sp_) in enumerate(((66, 606, 58.0, 1.0), (118, 612, 48.0, 0.9), (16, 600, 54.0, 1.0), (150, 616, 36.0, 0.8))):
            fern_px(sheet, px_, py_, sz, seed + 10 + i, k=1.9, dark=0.62, spread=sp_)
    # the bough across the top right corner: a neighbour's, hanging in close to the lens
    leaf = lerp(lerp(LEAF, PRUSSIAN, 0.46), SIENNA, 0.05)
    wood = lerp(BARK_DARK, PRUSSIAN, 0.35)
    lit = lerp(lerp(LEAF, VERONESE, 0.26), SKYC, 0.10)
    bough(s, (836, 30), (600, 112), leaf, wood, seed + 20, thick=64.0, lit=lit, fingers=1.1, marks=m)
    bough(s, (830, -14), (676, 26), leaf, wood, seed + 21, thick=46.0, lit=lit, fingers=1.0, marks=m)
    bough(s, (836, 104), (730, 168), leaf, wood, seed + 22, thick=40.0, lit=lit, fingers=1.0, marks=m)
    # fern fronds in the bottom right corner, from below the picture
    for sheet in (s, m):
        for i, (px_, py_, sz, sp_) in enumerate(((748, 618, 56.0, 1.0), (806, 606, 58.0, 0.9), (690, 624, 42.0, 0.8))):
            fern_px(sheet, px_, py_, sz, seed + 30 + i, k=1.7, dark=0.60, spread=sp_)
    fc, fa = s.done()
    over(out, fc, fa)
    a = np.maximum(alpha, fa)
    return out, a, g, m.done()


def fern_px(s, px_, py_, size, seed, k=1.8, dark=0.6, spread=1.0, n=None):
    """A fern near the lens, set by its foot's picture point (it stands nearer than the picture's bottom edge shows
    ground for): fronds `size` cm long at `k` px to the cm, arching up and over."""
    rng = np.random.default_rng(seed)
    n = n or int(rng.integers(7, 11))
    fronds = []
    for j in range(n):
        az = rng.uniform(0.12 * math.pi, 0.88 * math.pi) if j < n - 2 else rng.uniform(-0.1, 1.1) * math.pi
        L = size * k * rng.uniform(0.65, 1.08)
        lean = math.cos(az) * spread
        rise = 0.55 + 0.35 * math.sin(az)
        pts = []
        for q in np.linspace(0, 1, 10):
            ox = lean * L * (0.75 * q + 0.25 * q * q)
            oy = -L * rise * math.sin(q * math.pi * 0.60) * 1.2 + L * 0.10 * q * q
            pts.append((px_ + ox, py_ + oy))
        fronds.append((L, pts))
    for j, (L, pp) in enumerate(fronds):
        tone = j / max(len(fronds) - 1, 1)                          # the first laid lie behind: deeper; the last are in front: lighter
        c = lerp(lerp(FERN, PRUSSIAN, 0.42 + 0.5 * dark), lerp(lerp(FERN, VERONESE, 0.12), PRUSSIAN, 0.70 * dark), tone ** 1.6)
        for i in range(1, len(pp)):
            a, b = pp[i - 1], pp[i]
            dx, dy = b[0] - a[0], b[1] - a[1]
            ln = math.hypot(dx, dy) or 1.0
            nx, ny = -dy / ln, dx / ln
            q = i / (len(pp) - 1)
            reach = L * 0.20 * (1 - q) ** 0.7 * (0.5 + 0.5 * min(q * 5, 1))
            if reach < 1.0:
                continue
            steps_ = max(1, int(ln / max(2.4, 0.034 * L)))
            for m_ in range(steps_):
                f = (m_ + 0.5) / steps_
                cx_, cy_ = a[0] + dx * f, a[1] + dy * f
                back = 0.38 * reach
                for sgn in (-1, 1):
                    s.taper([(cx_, cy_), (cx_ + sgn * nx * reach + dx / ln * back, cy_ + sgn * ny * reach + dy / ln * back)], c, max(1.2, 0.022 * L), 0.6, 1.0)
        s.line(pp, lerp(c, lerp(VERONESE, OCHRE, 0.3), 0.34 * tone ** 2), max(0.9, 0.010 * L), 0.9)


def plane_light(pic, info):
    """The lamp below, seen under the floor: a thin line of it lying on the ground under the storehouse, between the
    posts, along both walls (the light of the room underneath comes up round the trapdoor and out under the boards),
    and what it lights: the ground just inside the posts, the posts' inner sides. A state of the backdrop: the same
    painting with the lamp lit. -> (rgb, alpha): only where the lamp changes anything."""
    Hs = HOUSE
    lit = pic.copy()
    under = info["under_floor"]
    lamp = lerp(NAPLES, paint("chrome-yellow"), 0.35)
    s = Paper(SHAPE)
    lines = []
    for (a, b, wall) in ((0.0, Hs.LW, "W"), (0.0, Hs.LD, "D")):
        cuts = list(Hs.posts_w if wall == "W" else Hs.posts_d)
        for c0, c1 in zip(cuts[:-1], cuts[1:]):
            for (q0, q1) in ((0.09, 0.91),):
                u0, u1 = max(c0 + (c1 - c0) * q0, 142.0), c0 + (c1 - c0) * q1      # (clear of the near corner: the two walls' lines never meet or cross)
                if u1 - u0 < 20.0:
                    continue
                inn = 104.0                                          # this far in under the floor
                if wall == "W":
                    p0, p1 = Hs.foot(u0, inn, 2.0), Hs.foot(u1, inn, 2.0)
                    clear = min(Hs.clear(u0, inn), Hs.clear(u1, inn))
                else:
                    p0, p1 = Hs.foot(inn, u0, 2.0), Hs.foot(inn, u1, 2.0)
                    clear = min(Hs.clear(inn, u0), Hs.clear(inn, u1))
                if clear < 16.0:
                    continue
                lines.append((p0, p1))
    glow_m = np.zeros(SHAPE, F32)
    for (p0, p1) in lines:
        glow_m = np.maximum(glow_m, mask_line(SHAPE, [p0, p1], 6.0, soft=2.6))
    under = under * (1 - np.clip(blur(info["gap_front"], 0.6) * 1.6, 0, 1))             # (the lamp is behind the posts and the steps)
    glow_m = glow_m * under
    glow(lit, lamp * 0.9, (glow_m * 0.50).astype(F32))
    for (p0, p1) in lines:
        s.line([p0, p1], lerp(NAPLES, OCHRE, 0.30), 1.5, 1.0)
        s.line([lerp_pt(p0, p1, 0.08), lerp_pt(p0, p1, 0.92)], lerp(NAPLES, WHITE, 0.50), 0.8, 1.0)
    colr, alpha = s.done()
    over(lit, colr, alpha * (under > 0.3))
    changed = (np.abs(lit - pic).sum(axis=2) > 0.07).astype(F32)
    info["light_lines"] = lines
    return lit, changed


def plane_window_lit(pic, info):
    """The small high window with the lantern lit behind it: warm light in the opening, on its far jamb and along the
    sill. A state of the backdrop. -> (rgb, alpha)."""
    Hs = HOUSE
    w0, w1, ws, wh = Hs.window
    lit = pic.copy()
    s = Paper(SHAPE)
    win = [Hs.pt(w0, 0, ws), Hs.pt(w1, 0, ws), Hs.pt(w1, 0, wh), Hs.pt(w0, 0, wh)]
    s.poly(win, lerp(NAPLES, paint("chrome-yellow"), 0.30), 1.0)
    inner = [Hs.pt(w0 + 9, 0, ws + 8), Hs.pt(w1 - 12, 0, ws + 8), Hs.pt(w1 - 12, 0, wh - 9), Hs.pt(w0 + 9, 0, wh - 9)]
    s.poly(inner, lerp(NAPLES, WHITE, 0.50), 1.0)
    s.poly([Hs.pt(w1, 0, ws), Hs.pt(w1, 0, wh), Hs.pt(w1 - 5, 12, wh), Hs.pt(w1 - 5, 12, ws)], lerp(paint("chrome-orange"), OCHRE, 0.5), 1.0)
    s.poly([Hs.pt(w0 - 10, -7, ws - 5), Hs.pt(w1 + 10, -7, ws - 5), Hs.pt(w1 + 10, 0, ws - 9), Hs.pt(w0 - 10, 0, ws - 9)], lerp(lerp(BOARD, SKYC, 0.28), NAPLES, 0.55), 1.0)
    colr, alpha = s.done()
    over(lit, colr, alpha)
    return lit, (alpha > 0.5).astype(F32)


# ================================================================ details: the crisp things said again, the drawing, the quiet line
LINE = PRUSSIAN


def key(s, pts, colr=None, width=0.8, alpha=0.5, seed=0, gaps=0.20, dash=11.0):
    """The key line, quieter than the print's: thin, and a little broken (it comes and goes along an edge)."""
    rng = np.random.default_rng(seed)
    colr = LINE if colr is None else colr
    for a, b in zip(pts[:-1], pts[1:]):
        ln = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(ln / dash))
        for i in range(n):
            if rng.random() < gaps:
                continue
            q0, q1 = i / n, (i + 1) / n
            s.line([lerp_pt(a, b, q0), lerp_pt(a, b, q1)], colr, width * rng.uniform(0.8, 1.15), alpha * rng.uniform(0.6, 1.0))


def details(pic, info, seed=191):
    """After the brush: the built and grown things restated (the brush leaves its marks, the forms stay), then what is
    drawn: boards, planks, posts, the reeds' ends along the thatch's edge, the courses up the slope, the steps' wet lips
    and joints, the roots' creases; and the key line, thin and broken, on the shade side of what is near and nowhere on
    what is far."""
    Hs = HOUSE
    LW, LD, e = Hs.LW, Hs.LD, Hs.eave
    rng = np.random.default_rng(seed)
    flats = info["flats"]
    crisp = np.clip(blur(info["crisp"], 0.8) * 1.2, 0, 1)
    pic[...] = lerp(pic, flats, (crisp * 0.62)[..., None])
    pic[...] = lerp(pic, flats, (np.clip(blur(info["house_crisp"], 0.6) * 1.2, 0, 1) * 0.6)[..., None])
    pic[...] = lerp(pic, flats, (np.clip(blur(info["far_trunks"], 1.2) * 1.3, 0, 1) * 0.7 * (1 - crisp))[..., None])
    soft_keep = np.clip(info["dressing"] * 0.8, 0, 1)
    pic[...] = lerp(pic, flats, soft_keep[..., None])
    t_h = float(air(Hs.corner[1] + 150.0))
    A = lambda c: far_of(c, t_h)
    s = Paper(SHAPE)
    wall_top = Hs.eave_under + 26.0
    # ---- the storehouse's posts (flats), then its boards and planks (lines)
    for u in Hs.posts_w:
        du = 7.5
        u0, u1 = max(u - du, 0.0), min(u + du, LW)
        s.poly([Hs.pt(u0, 0, -16), Hs.pt(u1, 0, -16), Hs.pt(u1, 0, wall_top), Hs.pt(u0, 0, wall_top)], A(shade_of(POST, 0.25)), 1.0)
    for w in Hs.posts_d:
        dw = 7.5
        w0_, w1_ = max(w - dw, 0.0), min(w + dw, LD)
        s.poly([Hs.pt(0, w0_, -16), Hs.pt(0, w1_, -16), Hs.pt(0, w1_, wall_top), Hs.pt(0, w0_, wall_top)], A(lerp(POST, SKYC, 0.12)), 1.0)
    # the corner post's lit edge: the lightest thing on the house (it faces the gap)
    s.line([Hs.pt(0, 1.5, -14), Hs.pt(0, 1.5, Hs.eave_under - 6)], A(lerp(BOARD, SKYC, 0.55)), 1.1, 0.8)
    # the sill beam under each wall: a lighter top, a dark underside
    for (a_, b_) in ((Hs.pt(0, 0, -16), Hs.pt(LW, 0, -16)), (Hs.pt(0, 0, -16), Hs.pt(0, LD, -16))):
        s.line([a_, b_], A(lerp(PRUSSIAN, SIENNA, 0.2)), 1.6, 0.9)
    s.line([Hs.pt(0, 0, 1), Hs.pt(0, LD, 1)], A(lerp(BOARD, SKYC, 0.42)), 0.9, 0.7)
    s.line([Hs.pt(0, 0, 1), Hs.pt(LW, 0, 1)], A(lerp(BOARD, SKYC, 0.22)), 0.9, 0.6)
    yb = 5.0
    while yb < wall_top:
        key(s, [Hs.pt(0, 0, yb), Hs.pt(LW * 0.5, 0, yb + rng.normal(0, 0.6)), Hs.pt(LW, 0, yb)], LINE, 0.6, 0.30, seed=int(yb), gaps=0.25, dash=17.0)
        key(s, [Hs.pt(0, 0, yb), Hs.pt(0, LD, yb + rng.normal(0, 0.6))], LINE, 0.6, 0.26, seed=int(yb) + 500, gaps=0.25, dash=14.0)
        yb += 21.0
    # the door: its planks, its pull, the frame's shade side
    d0, d1, dh = Hs.door
    for q in (0.25, 0.5, 0.75):
        w = d0 + (d1 - d0) * q
        key(s, [Hs.pt(0, w, 2), Hs.pt(0, w + rng.normal(0, 0.4), dh - 2)], LINE, 0.7, 0.42, seed=int(w), gaps=0.12, dash=16.0)
    key(s, [Hs.pt(0, d1, 0), Hs.pt(0, d1, dh), Hs.pt(0, d0, dh)], LINE, 0.9, 0.6, seed=3, gaps=0.08)
    s.line([Hs.pt(0, d0, 0), Hs.pt(0, d0, dh)], A(lerp(BOARD, SKYC, 0.4)), 0.8, 0.6)
    hp = Hs.pt(0, d0 + 12, 92)
    s.ellipse(hp[0], hp[1], 1.3, 2.4, A(lerp(PRUSSIAN, SIENNA, 0.3)), 0.9)
    # the door's steps
    key(s, info["door_steps"][:4] + [info["door_steps"][0]], LINE, 0.7, 0.45, seed=4)
    # the window: its frame's line; the sill's light
    w0, w1, ws, wh = Hs.window
    key(s, [Hs.pt(w0 - 7, 0, ws - 9), Hs.pt(w0 - 7, 0, wh + 7), Hs.pt(w1 + 7, 0, wh + 7), Hs.pt(w1 + 7, 0, ws - 9)], LINE, 0.8, 0.55, seed=5, gaps=0.1)
    s.line([Hs.pt(w0 - 10, -7, ws - 5), Hs.pt(w1 + 10, -7, ws - 5)], A(lerp(BOARD, SKYC, 0.55)), 0.9, 0.8)
    # ---- charcoal in its straw bales, stacked under the thatch at the far end of the door wall
    straw = lerp(lerp(lerp(OCHRE, WHITE, 0.45), SKYC, 0.25), PRUSSIAN, 0.46)
    for row, (w_a, n_) in enumerate(((236.0, 3), (258.0, 2))):
        for j in range(n_):
            w = w_a + j * 42.0
            yb_ = -Hs.clear(-40, w) + 21.0 + row * 37.0
            c = Hs.pt(-46, w, yb_)
            k = CAM.px_cm(*Hs.xd(-46, w))
            c2 = Hs.pt(-14, w, yb_)
            s.poly([(c[0], c[1] - 19 * k), (c2[0], c2[1] - 19 * k), (c2[0], c2[1] + 19 * k), (c[0], c[1] + 19 * k)], A(lerp(straw, PRUSSIAN, 0.22)), 1.0)
            s.ellipse(c[0], c[1], 16 * k, 19 * k, A(straw), 1.0)
            s.ellipse(c[0], c[1], 4 * k, 5 * k, A(lerp(straw, PRUSSIAN, 0.30)), 1.0)
    # ---- the thatch: the reeds' ends along the cut edge, its wet lip, the courses up the slopes, the hip, the ridge's bindings
    ev = info["eaves"]
    for (a_u, a_t, b_u, b_t), n_, sd in (((ev["A0u"], ev["A0t"], ev["B0u"], ev["B0t"]), 120, 1), ((ev["A0u"], ev["A0t"], ev["D0u"], ev["D0t"]), 70, 2)):
        for i in range(n_):
            q = (i + rng.random()) / n_
            lo, hi = lerp_pt(a_u, b_u, q), lerp_pt(a_t, b_t, q)
            f0, f1 = rng.uniform(0.0, 0.35), rng.uniform(0.55, 1.0)
            s.line([lerp_pt(lo, hi, f0), lerp_pt(lo, hi, f1)], A(lerp(PRUSSIAN, SIENNA, 0.18)), 0.7, 0.32)
        # the ragged lower edge: tufts hanging below it, and drops gathering
        for i in range(int(n_ * 0.5)):
            q = rng.random()
            lo = lerp_pt(a_u, b_u, q)
            s.line([lo, (lo[0] + rng.normal(0, 0.6), lo[1] + rng.uniform(1.5, 4.0))], A(lerp(THATCH, PRUSSIAN, 0.5)), 0.9, 0.8)
        s.line([a_t, lerp_pt(a_t, b_t, 0.5), b_t], A(lerp(THATCH, SKYC, 0.5)), 1.0, 0.55)
        key(s, [a_u, lerp_pt(a_u, b_u, 0.5), b_u], LINE, 0.9, 0.55, seed=10 + sd, gaps=0.15)
    (r0u, r0w), (r1u, r1w) = Hs.ridge_at
    for i in range(1, 9):                                         # courses on the long slope
        q = i / 9.5
        w = -e + q * (r0w + e)
        u_a, u_b = -e + q * (r0u + e), LW + e - q * (LW + e - r1u)
        pts = [Hs.pt(u, w, Hs.roof_long(u, w) + rng.normal(0, 1.5)) for u in np.linspace(u_a, u_b, 7)]
        key(s, pts, far_of(lerp(THATCH, PRUSSIAN, 0.55), t_h + 0.22 * q), 0.7, 0.34 * (1 - 0.6 * q), seed=20 + i, gaps=0.35, dash=13.0)
    for i in range(1, 9):                                         # and on the hip
        q = i / 9.5
        u = -e + q * (r0u + e)
        w_a, w_b = -e + q * (r0w + e), LD + e - q * (LD + e - r0w)
        pts = [Hs.pt(u, w, Hs.roof_hip(u, w) + rng.normal(0, 1.5)) for w in np.linspace(w_a, w_b, 5)]
        key(s, pts, far_of(lerp(THATCH, PRUSSIAN, 0.5), t_h + 0.22 * q), 0.7, 0.30 * (1 - 0.6 * q), seed=40 + i, gaps=0.35, dash=11.0)
    dark_reed, light_reed = lerp(THATCH, PRUSSIAN, 0.55), lerp(THATCH, SKYC, 0.45)
    for i in range(520):                                          # the reeds, combed down the long slope
        w = rng.uniform(-e + 6.0, r0w - 8.0)
        q = (w + e) / (r0w + e)
        u = rng.uniform(-e + q * (r0u + e) + 4.0, LW + e - q * (LW + e - r1u) - 4.0)
        ln_ = rng.uniform(16.0, 46.0)
        a_, b_ = Hs.pt(u, w, Hs.roof_long(u, w)), Hs.pt(u + rng.normal(0, 2.0), w - ln_, Hs.roof_long(u, w - ln_))
        lite = rng.random() < 0.36
        s.line([a_, b_], far_of(light_reed if lite else dark_reed, t_h + 0.24 * q), 0.7, (0.30 if lite else 0.34) * (1 - 0.5 * q))
    for i in range(300):                                          # and down the hip
        u = rng.uniform(-e + 6.0, r0u - 8.0)
        q = (u + e) / (r0u + e)
        w = rng.uniform(-e + q * (r0w + e) + 4.0, LD + e - q * (LD + e - r0w) - 4.0)
        ln_ = rng.uniform(16.0, 46.0)
        a_, b_ = Hs.pt(u, w, Hs.roof_hip(u, w)), Hs.pt(u - ln_, w + rng.normal(0, 2.0), Hs.roof_hip(u - ln_, w))
        lite = rng.random() < 0.45
        s.line([a_, b_], far_of(light_reed if lite else dark_reed, t_h + 0.24 * q), 0.7, (0.32 if lite else 0.30) * (1 - 0.5 * q))
    for (a_t, b_t, n_) in ((ev["A0t"], ev["B0t"], 26), (ev["A0t"], ev["D0t"], 14)):       # moss and seedlings along the top of the cut edge
        for i in range(n_):
            c = lerp_pt(a_t, b_t, rng.random())
            s.ellipse(c[0], c[1] - rng.uniform(0.5, 2.5), rng.uniform(2.5, 7.0), rng.uniform(1.2, 2.6), A(lerp(MOSS, PRUSSIAN, rng.uniform(0.2, 0.5))), 0.85)
    for (a_u, b_u, n_) in ((ev["A0u"], ev["B0u"], 30), (ev["A0u"], ev["D0u"], 16)):       # a longer straw here and there, hanging below the edge
        for i in range(n_):
            c = lerp_pt(a_u, b_u, rng.random())
            s.line([c, (c[0] + rng.normal(0, 1.2), c[1] + rng.uniform(3.0, 8.0))], A(lerp(THATCH, PRUSSIAN, 0.35)), 0.8, 0.75)
    key(s, [ev["A0t"], lerp_pt(ev["A0t"], ev["R0"], 0.5), ev["R0"]], far_of(LINE, t_h + 0.1), 0.8, 0.4, seed=60, gaps=0.2)
    s.line([(ev["A0t"][0] - 1.2, ev["A0t"][1]), (ev["R0"][0] - 1.2, ev["R0"][1])], far_of(lerp(THATCH, SKYC, 0.6), t_h + 0.1), 0.9, 0.42)
    R0, R1, sag = info["ridge"]
    for q in np.linspace(0.02, 0.98, 6):
        c = sag(q)
        s.line([(c[0], c[1] - 7.5), (c[0] + 0.8, c[1] + 4.5)], far_of(lerp(PRUSSIAN, SIENNA, 0.25), t_h + 0.2), 1.4, 0.7)
    # ---- the eaves' drip line on the ground: pebbles, light and dark, along both walls
    for (a_, b_, n_) in ((Hs.xd(-e, -e), Hs.xd(LW + e * 0.6, -e), 70), (Hs.xd(-e, -e), Hs.xd(-e, LD + e * 0.5), 44)):
        for i in range(n_):
            q = rng.random()
            x, d = a_[0] + (b_[0] - a_[0]) * q + rng.normal(0, 7.0), a_[1] + (b_[1] - a_[1]) * q + rng.normal(0, 7.0)
            c = on(x, d, 1.0)
            k = CAM.px_cm(x, d)
            s.ellipse(c[0], c[1], rng.uniform(2.5, 5.0) * k, rng.uniform(1.5, 3.0) * k, far_of(lerp(STONE, PRUSSIAN, rng.uniform(0.1, 0.55)), float(air(d))), 1.0)
    # ---- the steps: each tread's wet lip, the dark where a riser meets the tread below, joints, moss in them
    for (quad, t) in info["risers"]:
        s.line([quad[3], quad[2]], far_of(lerp(SKYC, PAPER, 0.5), t * 0.5), 1.0, 0.75)
        key(s, [quad[0], quad[1]], far_of(LINE, t * 0.6), 1.0, 0.6, seed=int(quad[0][0]), gaps=0.12)
        key(s, [quad[0], quad[3]], far_of(LINE, t), 0.7, 0.4, seed=int(quad[0][1]))
    for (pts, Y, outline, t, look) in info["treads"]:
        xs = [q[0] for q in pts]
        ys = [q[1] for q in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        n_ = int(rng.integers(2, 4))
        for j in range(n_):                                       # joints between the slabs, running up the tread
            q = (j + rng.uniform(0.25, 0.75)) / n_
            xa = x0 + (x1 - x0) * q
            key(s, [(xa - rng.uniform(-6, 6), y1 - 1), (xa + rng.uniform(-8, 8), y0 + 1)], far_of(LINE, t), 0.8, 0.34, seed=int(xa), gaps=0.2, dash=7.0)
            for _ in range(3):
                mx_, my_ = xa + rng.normal(0, 4.0), rng.uniform(y0 + 1, y1 - 1)
                s.ellipse(mx_, my_, rng.uniform(1.5, 4.0), rng.uniform(0.8, 1.6), far_of(lerp(MOSS, PRUSSIAN, 0.4), t), 0.7)
    for ring in info.get("puddle_rings", []):
        near = sorted(ring, key=lambda q: -q[1])[: len(ring) // 2]
        near.sort(key=lambda q: q[0])
        key(s, near, LINE, 0.7, 0.35, seed=int(ring[0][0]), gaps=0.3, dash=6.0)
    for (ring, t) in info["stones"]:
        near = sorted(ring, key=lambda q: -q[1])[: len(ring) // 2]
        near.sort(key=lambda q: q[0])
        key(s, near, far_of(LINE, t), 0.7, 0.4, seed=int(ring[0][0]), gaps=0.2, dash=6.0)
        far = sorted(ring, key=lambda q: q[1])[: len(ring) // 2]
        far.sort(key=lambda q: q[0])
        s.line(far, far_of(lerp(SKYC, PAPER, 0.4), t), 0.8, 0.5)
    # ---- the kiln: cracks in the clay, the mouth's stones, the cut ends of the wood
    K = info["kiln"]
    kx, kd = KILN["at"]
    t_k = float(air(kd))
    dome = K["poly"]
    key(s, dome[:8], far_of(LINE, t_k), 0.8, 0.45, seed=70)       # (its shade side: the right)
    for j in range(4):
        a0 = rng.uniform(0.25, 0.75) * math.pi
        p0 = on(kx + KILN["r"] * 0.86 * math.cos(a0), kd - 20.0, KILN["h"] * math.sin(a0) * 0.92)
        pts = [p0]
        for _ in range(4):
            pts.append((pts[-1][0] + rng.normal(0, 3.0), pts[-1][1] + rng.uniform(3.0, 7.0)))
        key(s, pts, far_of(lerp(PRUSSIAN, SIENNA, 0.3), t_k), 0.7, 0.4, seed=71 + j, gaps=0.15, dash=5.0)
    key(s, K["arch"], far_of(LINE, t_k * 0.6), 0.9, 0.6, seed=75, gaps=0.1)
    for (cx_, cy_, rr) in K["logs"]:
        s.ellipse(cx_, cy_, rr * 0.34, rr * 0.33, far_of(lerp(SIENNA, PRUSSIAN, 0.2), t_k), 0.6)
    # ---- the bank: roots hanging out of the cut earth, ferns and moss along its lip; the pipe said again, and its shade
    t_b = info["bank"]["t"]
    for j in range(9):
        q = (j + rng.random()) / 9
        i0 = min(int(q * (len(BANK_TOP) - 1)), len(BANK_TOP) - 2)
        a_ = lerp_pt(BANK_TOP[i0], BANK_TOP[i0 + 1], q * (len(BANK_TOP) - 1) - i0)
        pts = [(a_[0], a_[1] + 3)]
        for _ in range(int(rng.integers(3, 6))):
            pts.append((pts[-1][0] + rng.normal(0, 4.0), pts[-1][1] + rng.uniform(6.0, 13.0)))
        s.taper(pts, far_of(lerp(BARK_DARK, PRUSSIAN, 0.2), t_b), 1.6, 0.6, 0.8)
    pa, pb = pipe_points()
    tint(pic, SHADE * 1.3, (mask_line(SHAPE, [(pa[0] + 2, pa[1] + 5), (pb[0] + 4, pb[1] + 7)], 4.0, soft=1.2) * 0.45 * info["bank"]["mask"]).astype(F32))
    pipe(s, t_b * 0.5)
    for j, (bx_, by_) in enumerate(BANK_TOP):
        X, D_ = G(bx_, max(by_ + 96, HZ + 20))
        fern_px(s, bx_ + rng.normal(0, 6), by_ + 4, 34.0, seed + 300 + j, k=0.46, dark=0.3, spread=0.9, n=6)
    # ---- the stone figure: its shade side's line, the bib's fold, the worn face (two closed eyes: short level lines)
    Fg = info["figure"]
    hx, hy, hr = Fg["head"]
    key(s, [Fg["body"][1], Fg["body"][2], Fg["body"][3], Fg["body"][4]], LINE, 0.8, 0.55, seed=80, gaps=0.1, dash=5.0)
    arc = [(hx + hr * math.cos(a_), hy + hr * 1.06 * math.sin(a_)) for a_ in np.linspace(-0.5 * math.pi, 0.45 * math.pi, 8)]
    key(s, arc, LINE, 0.8, 0.5, seed=81, gaps=0.1, dash=4.0)
    s.line([(hx - hr * 0.50, hy + hr * 0.05), (hx - hr * 0.16, hy + hr * 0.08)], lerp(PRUSSIAN, WHITE, 0.25), 0.7, 0.7)
    s.line([(hx + hr * 0.10, hy + hr * 0.08), (hx + hr * 0.44, hy + hr * 0.05)], lerp(PRUSSIAN, WHITE, 0.25), 0.7, 0.7)
    bib = Fg["bib"]
    s.line([bib[0], bib[1]], lerp(VERMILION, WHITE, 0.3), 0.8, 0.7)
    key(s, [bib[2], bib[3], bib[4], bib[5], bib[6]], lerp(VERMILION, PRUSSIAN, 0.55), 0.7, 0.6, seed=82, gaps=0.1, dash=4.0)
    # ---- the cedar needles lying on the hillside: short rust-brown strokes, at a true count for each square metre (few
    # and long near us, a fine speckle up the hill), and here and there the pale wet of bare earth between them
    zone = info["ground"] * (1 - np.clip(info.get("yard", 0) * 1.3, 0, 1)) * (1 - info["steps_mask"]) * (1 - np.clip(info["crisp"], 0, 1)) * (1 - np.clip(info["dressing"], 0, 1))
    zone = (blur(zone, 1.0) > 0.85).astype(F32)
    lit_c, dark_c = lerp(lerp(SIENNA, OCHRE, 0.40), PRUSSIAN, 0.30), lerp(PRUSSIAN, SIENNA, 0.35)
    for (x, y, k, r) in DEPTH.scatter(lambda X, Z: on(X, Z), lambda X, Z: CAM.px_cm(X, Z), (-1300.0, 1300.0, 560.0, 1900.0), 16.0, seed + 700, size=(7.0, 1.0), zone=zone, most=5200):
        X, D_ = G(x, y)
        t = float(air(D_))
        a_ = rng.uniform(0, math.pi)
        L_ = (3.0 + 6.0 * r) * k
        s.line([(x - math.cos(a_) * L_, y - math.sin(a_) * L_ * 0.35), (x + math.cos(a_) * L_, y + math.sin(a_) * L_ * 0.35)],
               far_of(lit_c if r > 0.55 else dark_c, t), max(0.8, 1.0 * k), 0.55 if r > 0.55 else 0.50)
    # ---- the backdrop's trunks: the roots' creases; a line down the shade side of the nearer ones, lost as it rises
    for (g, t) in info.get("trunks", []):
        if g["d"] < 2300.0:
            root_marks(s, g, detail=1.0 if g["d"] < 1500 else 0.6, t=t)
        if g["d"] < 1800.0:
            trunk_marks(s, g, 600 + int(g["x"]), t=t, detail=1.0 if g["d"] < 1300 else 0.7, stubs=2)
        if g["d"] < 1500.0:
            R = g["R"]
            for i in range(0, 8):
                key(s, [R[i], R[i + 1]], far_of(lerp(LINE, SIENNA, 0.3), t), 0.9, 0.5 * (1 - i / 9.0), seed=90 + i, gaps=0.2)
    colr, alpha = s.done()
    over(pic, colr, alpha)
    return pic


def contour_cut(c, a, g, t, near=False):
    """The drawing on a cut-out trunk: the roots' creases and lights, the shade side's line (burnt sienna on the near
    cedar, as the act's near contour is), within its own edge."""
    s = Paper(SHAPE)
    if not near:
        root_marks(s, g, detail=1.0, t=t)
        trunk_marks(s, g, 700 + int(g["x"]), t=t, detail=1.0, stubs=3)
    R = g["R"]
    colr = lerp(SIENNA, PRUSSIAN, 0.45) if near else far_of(lerp(LINE, SIENNA, 0.35), t)
    for i in range(0, len(R) - 1):
        key(s, [R[i], R[i + 1]], colr, 1.0 if near else 0.9, (0.55 if near else 0.5 * max(0.15, 1 - i / 11.0)), seed=400 + i, gaps=0.18)
    col_, al = s.done()
    out = c.copy()
    over(out, col_, al * a)
    return out


# ================================================================ finishing
def grade(picture):
    """The last glaze: the darks lifted a little toward prussian blue (there is no black under rain)."""
    lum = (picture @ LUM)[..., None]
    out = picture + 0.035 * np.clip(1 - lum / 0.4, 0, 1) * np.array([0.3, 0.5, 1.2], dtype=F32)
    return np.clip(out, 0, 1).astype(F32)


def soft_mask(info):
    """What was laid wet in wet: the sky, the far ranks, the mist, the far crowns: everything above the hillside's line
    that is not a near, crisp thing; and a breath of it on the far ground."""
    crisp = np.clip(blur(np.maximum(info["crisp"], info.get("boughs_mid", 0) * 0.6), 2.0) * 1.6, 0, 1)
    up = step(HZ + 46.0, HZ - 6.0, PY) * 0.75
    far_ground = step(HZ + 90.0, HZ + 20.0, PY) * 0.3
    straight = np.clip(blur(info["far_trunks"], 1.5) * 1.5, 0, 1)        # (the far trunks were feathered as they were laid: they stay straight)
    return np.clip(np.maximum(up, far_ground) * (1 - crisp) * (1 - straight), 0, 1).astype(F32)


PALETTES = {}


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.012, amount=0.02):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    PALETTES[name] = pal
    return os.path.getsize(name)


def show(picture, name):
    Image.fromarray((np.clip(picture, 0, 1) * 255).astype(np.uint8)).save(name)


def brushed(color, alpha, ground, fast, seed=4, keep=0.45):
    """A cut-out repainted with the brush against the ground it stands on, then restated; its edge stays as it was."""
    if fast or not (alpha > 0.5).any():
        return color
    flat = ground.copy()
    over(flat, color, alpha)
    painted = strokes(flat, sizes=(9, 5, 2), seed=seed, density=1.6, jitter=0.025, keep=0.26)
    return lerp(painted, flat, keep)


def paint_all(fast=False):
    """-> (back, cuts {name: (rgb, alpha)}, info): every picture as painted and washed, before the palette."""
    t0 = time.time()
    base, info = under()
    show(base, f"{WORK}/1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else strokes(base, sizes=(12, 6, 3), seed=2, density=1.5, jitter=0.025, keep=0.30)
    print("brushed", round(time.time() - t0, 1))
    ground = pic.copy()
    DEPTH.frame(pic, amount=0.10, bottom=0.10, color="#22304e")
    details(pic, info)
    pic = grade(pic)
    show(pic, f"{WORK}/2-back.png")
    # the cut-outs, as painted
    raw = {}
    c, a, g, (mc, ma) = cedar_cut(CEDAR_L[0], 211, info, ferns=((-48.0, -42.0, 36.0), (34.0, -60.0, 30.0)),
                                  boughs=((64.0, 1, 96.0, 26.0), (30.0, -1, 80.0, 24.0), (128.0, -1, 62.0, 20.0), (176.0, 1, 118.0, 27.0)))      # (the last lies across the roof's hip, toward the ridge)
    c = brushed(c, a, ground, fast, 21)
    over(c, mc, ma * (a > 0.5))
    raw["cedar-l"] = (grade(contour_cut(c, a, g, float(air(g["d"])))), (a > 0.5).astype(F32), g)
    c, a, g, (mc, ma) = cedar_cut(CEDAR_R[0], 221, info, ferns=((-50.0, -50.0, 40.0), (44.0, -40.0, 34.0)),
                                  boughs=((212.0, -1, 92.0, 28.0), (262.0, 1, 60.0, 22.0)))
    c = brushed(c, a, ground, fast, 22)
    over(c, mc, ma * (a > 0.5))
    raw["cedar-r"] = (grade(contour_cut(c, a, g, float(air(g["d"])))), (a > 0.5).astype(F32), g)
    c, a, g, (mc, ma) = near_plane(info)
    c = brushed(c, a, ground, fast, 23, keep=0.55)
    over(c, mc, ma * (a > 0.5))                                         # (what is drawn on the near plane, crisp, after the brush)
    raw["front"] = (grade(contour_cut(c, a, g, 0.0, near=True)), (a > 0.5).astype(F32), g)
    lit, la = plane_light(pic, info)
    wl, wa = plane_window_lit(pic, info)
    # the watercolour: one sheet of paper under all of it (the same seed), the far things wet in wet
    soft = soft_mask(info)
    info["soft_mask"] = soft
    back = WC.wash(pic, seed=SEED, soft=soft)
    cuts = {}
    for name in ("cedar-l", "cedar-r", "front"):
        c, a, g = raw[name]
        cuts[name] = (WC.wash_cut(c, a, pic, seed=SEED, soft=soft * (1 - a)), a)
        info["geom_" + name] = g
    keep_light = np.clip(blur(la, 1.0) * 1.5, 0, 1) * 0.55             # (the lamp's own light stays clean: the paper does not grey it)
    cuts["light-on"] = (WC.wash(lit, seed=SEED, soft=soft, keep=keep_light), la)
    cuts["window-lit"] = (WC.wash(wl, seed=SEED, soft=soft, keep=np.clip(blur(wa, 0.6), 0, 1) * 0.6), wa)
    print("planes", round(time.time() - t0, 1))
    whole = back.copy()
    for name in ("light-on", "cedar-l", "cedar-r", "front"):
        c, a = cuts[name]
        over(whole, c, a)
    show(back, f"{WORK}/3-back-washed.png")
    show(whole, f"{WORK}/3-all.png")
    lit_all = whole.copy()
    over(lit_all, *cuts["window-lit"])
    show(lit_all, f"{WORK}/3-window-lit.png")
    return back, cuts, info


if __name__ == "__main__":
    t0 = time.time()
    fast = "fast" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    back, cuts, info = paint_all(fast)
    lay = LAY.layout(info, cuts, PUDDLES)
    with open(f"{WORK if fast else OUT}/layout.json", "w") as fh:
        json.dump(lay, fh, indent=1)
    with open("out/edo-cedars-remap.json", "w") as fh:
        json.dump({"points": lay["remap"]["points"]}, fh)
    with open(f"{WORK}/scene-numbers.txt", "w") as fh:
        fh.write(LAY.scene_numbers(lay) + "\n")
    if fast:
        sys.exit()
    print("back", finish(back, f"{OUT}/back.png", 176))
    for name, colors in (("front", 64), ("cedar-l", 48), ("cedar-r", 48), ("light-on", 32), ("window-lit", 16)):
        c, a = cuts[name]
        print(name, finish(c, f"{OUT}/{name}.png", colors, a))
    os.system(f"{sys.executable} comp.py {OUT} back light-on cedar-l cedar-r front")
    print("done", round(time.time() - t0, 1))

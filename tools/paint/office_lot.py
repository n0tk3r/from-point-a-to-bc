"""Outside the Office's field headquarters (scene `office-lot`, OFFICE-17A, round seventeen): a very small beige building
with a very long name, in the Nevada desert, early in the afternoon of 31 October.

    python3 office_lot.py fast       the under-painting only, no brush pass, no cut-outs: for composing (15 s)
    python3 office_lot.py paint      the backdrop with the brush pass and the details, and the cut-outs laid on it
    python3 office_lot.py            everything: out/office-lot/ (back, the cut-outs and their states, the frames,
                                     layout.json) and the look pictures out/office-lot-*.png; then office_lot_check.py
    python3 install.py office-lot    keys it in nevada-morning at 50 and copies it into art/scenes/office-lot/

THE PICTURE'S IDEA. A small, earnest, slightly silly building: one storey of beige cinder block the size of a two-car
garage, flat-roofed, nothing on our side but a steel door with a keypad under a little flat awning, one small high
frosted window, and over the door a sign far too long for it. On its roof an air conditioner the size of a minivan,
much too big for it (it breathes for seven floors underground: that is the joke and the clue). A drainpipe down its
near right corner stops three feet short of the gravel; a steel trash can stands by the wall. The gray limousine is
parked beside it; a flagpole with a small pennant stands at its left corner; a chain-link fence runs across the back
with its gate standing open; then desert, a far range, sky. Nothing frightening: no wire, no cameras, no guard box.

LIGHT   early afternoon: the sun high (49 degrees) and a little behind us to the left (office_lot_kit.SUN). Fronts are
        lit, tops brightest, every shadow short, falling back and to the right; the shade is blue with the sky.
DEPTH   horizon 140, full 588 (the lens 4.9 m up: we look down on the roof). office_lot_kit.CAM; every built thing is
        drawn through it, so the door is the right size for the men who will stand at it.
TONES   light: the sunlit front and its sign, the roof, the gravel near the building. middle: the sky, the unit, the
        desert, the limousine's side. dark: the doorway, the shadows, the limousine's glass and underside, the corners.

HOW THE PICTURE IS MADE (the README's four passes): under() blocks in sky, range, desert, lot, fence and building with
their light and shadows; strokes() brushes it; details() puts every built edge back crisply and adds the small things
and the lettering; finish() grains it and limits the palette. The cut-outs are drawn on their own sheets through the
same camera (office_lot_things.py, office_lot_limo.py), brushed over what is behind them, and cut hard; the backdrop is
painted complete under each, with the shadows of the things that never move (the awning's, the flagpole's) and
without the shadows of the things that do (the can carries its own, as the limousine does)."""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import (F32, blur, curve, grain, grid, lerp, mask_line, mask_poly, noise, over, palette_of, ramp, rgb, sample, save,
                   step, strokes, tint, to_palette)
import sky as SKY
import office_lot_kit as K
from office_lot_kit import (AWNING, BLD, CAN, DOOR, FENCE, FLAG, GATE, GRILLE, KEYPAD, MAT, NUTS, PIPE, SCUPPER, SIGN, SWITCH,
                            UNIT, WINDOW, FRONT, TOP, RIGHT, LEFT, col, lit)
import office_lot_things as T
from nevada_roadside_kit import Paper, Solid, brushed, sagebrush, tuft

OUT = "out/office-lot"
WORK = "out/office-lot-work"
SEED = 17
SHAPE = (K.H, K.W)
FENCE_ROW = K.row_of(FENCE["z"])


# ---------------------------------------------------------------- small helpers
def to_image(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def poly_mask(points, soft=0.0):
    return mask_poly(SHAPE, points, soft=soft)


def lay(pic, sheets, amount=1.0):
    """Lay sheets over the picture, in order."""
    for s in sheets:
        c, a = s.done()
        over(pic, c, a * amount)
    return pic


def wall_rect(x0, x1, y0, y1, z):
    return [K.P(x0, y0, z), K.P(x1, y0, z), K.P(x1, y1, z), K.P(x0, y1, z)]


def shade_ground(pic, m, amount=0.62, tone="#7480b8"):
    """A shadow laid on something in the sun: the colour under the blue sky, never black."""
    cool = pic * col(tone) * 1.15 + col("#1a1830") * 0.05
    pic[...] = lerp(pic, np.clip(cool, 0, 1), (np.clip(m, 0, 1) * amount)[..., None])
    return pic


# ---------------------------------------------------------------- the sky, the range, the desert
def paint_sky():
    """Early afternoon: deep blue overhead going pale and a little warm at the horizon; high thin cloud in long
    streaks and a few hooked tails, combed by a wind up there that is not felt down here; their cores bright, their
    edges thin into the blue."""
    pic = SKY.field(SHAPE, K.HZ, [(0.0, "#2856a6"), (0.32, "#3a70be"), (0.66, "#6f9fd4"), (0.88, "#accbe2"), (1.0, "#e2dccb")], SEED,
                    haze="#eae0ca", patch=0.04)
    x, y = grid(SHAPE)
    tint(pic, "#a8b8e8", (np.clip(1 - x / 700.0, 0, 1) * np.clip(1 - y / 140.0, 0, 1) * 0.10).astype(F32))
    band = step(0.0, 0.22, y / K.HZ) * step(1.0, 0.62, y / K.HZ)
    for (cell, lo, hi, amt, seed, colr) in (((440, 20), 0.58, 0.84, 0.50, SEED + 3, "#eef0f2"), ((240, 8), 0.64, 0.86, 0.55, SEED + 4, "#ffffff"),
                                           ((150, 5), 0.70, 0.90, 0.35, SEED + 5, "#f4f6fa")):
        n = noise(SHAPE, cell, seed, 5)
        slant = sample(n, x, y + (x - 400) * 0.09)
        m = step(lo, hi, slant) * band * amt * (y < K.HZ + 4)
        over(pic, colr, blur(m.astype(F32), 0.7))
    # mares' tails: a few long tapering strokes, each hooked up at its end, brightest along their spine
    from nevada_roadside_kit import Paper
    sh = Paper(SHAPE)
    rng = np.random.default_rng(SEED + 6)
    for i in range(9):
        x0 = rng.uniform(-40, 760)
        y0 = rng.uniform(14, 92)
        L = rng.uniform(90, 210)
        pts = [(x0 + L * t, y0 + 6 * t + math.sin(t * 3.0) * 2.5 - (9 * (t - 0.75) ** 2 if t > 0.75 else 0) * 4) for t in np.linspace(0, 1, 14)]
        sh.taper(pts, "#ffffff", rng.uniform(2.4, 4.2), 0.6, alpha=rng.uniform(0.22, 0.38))
        sh.taper([(px_, py_ + 1.2) for px_, py_ in pts], "#c8d6ea", 1.6, 0.4, alpha=0.25)
    lay(pic, (sh,))
    return pic


def ridge(xs, peaks, base, n_amp, seed, sharp=1.3):
    n1 = noise((1, K.W), (220, 1), seed, 3)[0]
    n2 = noise((1, K.W), (50, 1), seed + 1, 3)[0]
    top = np.zeros(K.W, F32)
    for (px, h, w) in peaks:
        top = np.maximum(top, h * np.clip(1 - np.abs(xs - px) / w, 0, 1) ** sharp)
    return base - (top + n1 * n_amp + n2 * n_amp * 0.35)


def paint_range(pic):
    """The far range on the horizon, in three: the farthest, highest and bluest, its summits faintly lit; a nearer one,
    warmer, lavender going pink, with a flat-topped mesa at the right whose face is in the sun; low brown hills in front.
    Each slope that turns toward the sun (to our left) is a little paler, each gully darker; haze along their feet."""
    xs = np.arange(K.W, dtype=F32)
    x, y = grid(SHAPE)

    def fill(top, lit_c, shade_c, foot_c, depth, seed, amount=1.0):
        slope = np.gradient(blur(top[None, :].astype(F32), 1.5)[0])
        litness = np.clip(0.5 + (-slope) * 0.9, 0, 1)[None, :]          # (a rising edge to the right turns its face to our left)
        gully = noise(SHAPE, (7, 26), seed, 3)
        t = np.clip((y - top[None, :]) / depth, 0, 1)
        c = lit_c * litness[..., None] + shade_c * (1 - litness[..., None])
        c = lerp(c, np.broadcast_to(col(foot_c), c.shape), (t ** 1.2)[..., None])
        c = c * (1 + (gully[..., None] - 0.5) * 0.14)
        m = ((y >= top[None, :]) & (y <= K.HZ + 1)).astype(F32) * amount
        over(pic, np.clip(c, 0, 1), m)
    far = ridge(xs, ((70.0, 26.0, 110.0), (250.0, 16.0, 140.0), (470.0, 30.0, 120.0), (690.0, 22.0, 130.0)), K.HZ - 4.0, 4.0, SEED + 7, 1.15)
    fill(far, col("#b8b8d6"), col("#9497bd"), "#b9b6cc", 30.0, SEED + 8)
    mid = ridge(xs, ((140.0, 12.0, 120.0), (360.0, 9.0, 110.0)), K.HZ - 3.0, 3.0, SEED + 9, 1.4)
    # the mesa: a flat top, steep sides, a band of paler rock under its rim
    mesa = np.where((xs > 584) & (xs < 712), K.HZ - 21.0 - noise((1, K.W), (30, 1), SEED + 12, 2)[0] * 1.6, K.HZ + 10.0)
    side = np.clip(1 - np.minimum(np.abs(xs - 584), np.abs(xs - 712)) / 10.0, 0, 1) * ((xs > 574) & (xs < 722))
    mesa = np.minimum(mesa, np.where((xs > 572) & (xs < 724), K.HZ - 21.0 + side * 14.0 + ((xs < 584) | (xs > 712)) * 6.0, K.HZ + 10.0))
    mid = np.minimum(mid, mesa)
    fill(mid, col("#d3b6bc"), col("#a993b0"), "#c4aeb0", 20.0, SEED + 10)
    rim = (y > mesa[None, :] + 2.0) & (y < mesa[None, :] + 5.0) & (xs[None, :] > 588) & (xs[None, :] < 708)
    over(pic, "#e4cfc4", rim.astype(F32) * 0.6)
    near = ridge(xs, ((40.0, 5.0, 90.0), (520.0, 4.0, 100.0), (770.0, 6.0, 80.0)), K.HZ - 1.5, 2.2, SEED + 11, 1.6)
    fill(near, col("#cdb19e"), col("#b09a98"), "#c9b29a", 8.0, SEED + 13, 0.9)
    hz = np.exp(-((y - K.HZ) / 3.5) ** 2) * (y <= K.HZ + 2)
    over(pic, "#ece2ce", (hz * 0.5).astype(F32))
    return pic


ROAD = [(-1040.0, 1250.0), (-1130.0, 2000.0), (-1560.0, 3200.0), (-2650.0, 5200.0), (-4250.0, 9000.0), (-6050.0, 16000.0)]


def paint_desert(pic):
    """The desert floor from the horizon to the fence: pale and hazed far off, warmer near; blotches of darker ground
    and paler drift; the dirt road from the gate away to the left toward the range."""
    X, Z, below = K.floor_xz(SHAPE)
    x, y = grid(SHAPE)
    t = np.clip((y - K.HZ) / (FENCE_ROW - K.HZ), 0, 1)
    c = ramp(t ** 0.8, [(0.0, "#ddd0b8"), (0.35, "#d8c39c"), (1.0, "#d2b78a")])
    blot = K.ground_noise(SHAPE, 900.0, SEED + 11) - 0.5
    fine = K.ground_noise(SHAPE, 160.0, SEED + 12, calm=1.6) - 0.5
    c = c * (1 + blot[..., None] * 0.14 + fine[..., None] * 0.08)
    # patches: rust-brown flats, pale drifts of sand, a darker stony stretch
    rust = step(0.62, 0.80, K.ground_noise(SHAPE, 2600.0, SEED + 14))
    pale = step(0.66, 0.84, K.ground_noise(SHAPE, 1800.0, SEED + 15))
    c = lerp(c, c * np.array([1.04, 0.90, 0.82], F32), (rust * 0.55)[..., None])
    c = lerp(c, np.clip(c * 1.08 + 0.03, 0, 1), (pale * 0.6)[..., None])
    over(pic, np.clip(c, 0, 1), below)
    # a dry wash winding away across the plain on the right: pale sand, a darker lip on its far bank
    wash = [(2400.0, 1600.0), (1700.0, 2600.0), (2300.0, 4200.0), (1500.0, 6200.0), (2600.0, 9000.0), (1800.0, 14000.0)]
    wpts = curve(wash, 8)
    for half, colr, amt in ((90.0, "#e8dcc0", 0.7), (130.0, "#bfa682", 0.25)):
        left = [(px_ - half, pz) for px_, pz in wpts]
        right = [(px_ + half, pz) for px_, pz in reversed(wpts)]
        m = poly_mask([K.P(px_, 0, pz) for px_, pz in left + right], soft=0.6) * below * (y < FENCE_ROW)
        over(pic, colr, m * amt)
    for half, colr, amt in ((150.0, "#e4d6b8", 0.55), (60.0, "#f0e4c6", 0.35)):
        left = [(px_ - half, pz) for px_, pz in ROAD]
        right = [(px_ + half, pz) for px_, pz in reversed(ROAD)]
        m = poly_mask([K.P(px_, 0, pz) for px_, pz in left + right], soft=0.6) * below
        over(pic, colr, m * amt)
    return pic


def sagebrush_field(pic, seed=SEED + 20, near_only=False, hide=None):
    """Sagebrush dotted over the desert past the fence: gray-green domes, small and many far off, a few big near the
    fence; each with its shadow back and to the right. near_only: only the ones close enough to be crisp (the details)."""
    rng = np.random.default_rng(seed)
    sh, sb = Paper(SHAPE), Paper(SHAPE)
    dens = noise((256, 256), 40.0, seed + 1, 3)
    for i in range(900):
        z = FENCE["z"] + 60 + (rng.random() ** 1.7) * 22000.0
        x = rng.uniform(-1.0, 1.0) * (z + K.CAM.Z0) * 0.62
        u, v = int((x / 60.0) % 256), int((z / 90.0) % 256)
        if rng.random() > dens[v, u] ** 1.6 * 1.3:                       # (in clumps and thin places)
            continue
        rad = rng.uniform(28.0, 60.0)
        seed_i = int(rng.integers(1e6))
        road_x = -1040.0 - (z - 1250.0) * 0.32
        if abs(x - road_x) < 260 + z * 0.012:
            continue
        px_, py_ = K.P(x, 0, z)
        if not (-10 < px_ < K.W + 10):
            continue
        r = rad * K.k_at(z)
        if r < 0.7:
            continue
        big = r >= 2.6
        if near_only != big:
            continue
        sh.ellipse(px_ + r * 0.55, py_ - r * 0.12, r * 1.05, max(0.6, r * 0.32), "#7a6f8c", 0.45)
        if r < 1.6:
            sb.ellipse(px_, py_ - r * 0.4, r * 1.1, r * 0.7, "#8a8c78", 0.85)
        else:
            sagebrush(sb, px_, py_, r, seed_i, tones=("#59604e", "#7b8268", "#a3aa8c", "#cdd0b2"), light=-1, tall=0.75)
    keep = 1.0 if hide is None else (1.0 - hide)
    lay(pic, (sh, sb), amount=keep)
    return pic


# ---------------------------------------------------------------- the lot
def lot_mask():
    x, y = grid(SHAPE)
    return (y > FENCE_ROW - 0.5).astype(F32)


def paint_lot(pic):
    """The graded gravel of the lot: paler and grayer than the desert, speckled, the speckle coarser near us."""
    x, y = grid(SHAPE)
    m = lot_mask()
    near = np.clip((y - FENCE_ROW) / (K.H - FENCE_ROW), 0, 1)
    c = ramp(near, [(0.0, "#cdc5b4"), (0.5, "#c8bea9"), (1.0, "#c0b39c")])
    blot = K.ground_noise(SHAPE, 300.0, SEED + 31) - 0.5
    grit = K.ground_noise(SHAPE, 9.0, SEED + 32, calm=0.9, octaves=2) - 0.5
    grit2 = K.ground_noise(SHAPE, 4.0, SEED + 33, calm=0.7, octaves=1) - 0.5
    c = c * (1 + blot[..., None] * 0.09 + grit[..., None] * 0.15 * (0.4 + near[..., None]) + grit2[..., None] * 0.10 * near[..., None])
    c[..., 2] += (K.ground_noise(SHAPE, 600.0, SEED + 34) - 0.5) * 0.04
    over(pic, np.clip(c, 0, 1), m)
    # the gravel runs out at the fence into the desert's sand: a ragged edge of sand over the gravel's back
    edge = np.exp(-np.clip(y - FENCE_ROW, 0, None) / 3.0) * m * (0.5 + 0.5 * noise(SHAPE, (14, 4), SEED + 35, 2))
    over(pic, "#d4bd94", np.clip(edge * 0.7, 0, 1))
    return pic


def track_paths():
    """The limousine's tracks: in through the gate, across the front of the building, to where it stands. -> its two
    sides' wheels' paths, lot points (x, z)."""
    wheel_z = K.LIMO["z"] + 22.0
    path = [(-1040.0, 1262.0), (-930.0, 900.0), (-660.0, 470.0), (-300.0, 320.0), (60.0, 330.0), (300.0, 420.0),
            (520.0, wheel_z), (900.0, wheel_z)]
    out = []
    for off in (0.0, 156.0):
        pts = []
        for i, (px_, pz) in enumerate(path):
            a, b = path[max(i - 1, 0)], path[min(i + 1, len(path) - 1)]
            dx, dz = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dz) or 1.0
            pts.append((px_ - dz / L * off, pz + dx / L * off))
        out.append(pts)
    return out


def pipe_stain(pic):
    """Where the drainpipe empties on the gravel: a darker, smoother patch (the can stands on it later)."""
    my, mz = PIPE["mouth"]
    pts = [K.P(PIPE["x"] + 30.0 * math.cos(t) + 6.0, 0.0, mz - 18.0 + 22.0 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 18, endpoint=False)]
    m = poly_mask(pts, soft=1.2) * (0.55 + 0.45 * noise(SHAPE, 6, SEED + 71, 2))
    pic[...] = lerp(pic, pic * np.array([0.84, 0.82, 0.86], F32), (m * 0.8)[..., None])
    return pic


def paint_tracks(pic, info=None):
    m_all = np.zeros(SHAPE, F32)
    for side in track_paths():
        pts = curve(side, 10)
        px = [K.P(px_, 0, pz) for px_, pz in pts]
        wd = [max(0.8, 22.0 * K.k_at(pz) * 0.55) for _, pz in pts]
        m_all = np.maximum(m_all, mask_line(SHAPE, px, wd, soft=0.5) * 0.85)
    m_all *= lot_mask()
    smooth_ = blur(pic, 1.2)
    out = lerp(pic, smooth_ * np.array([0.90, 0.89, 0.93], F32), m_all[..., None])
    rim = np.clip(blur(m_all, 1.0) - m_all, 0, 1) * 1.6
    over(out, "#e4d9c4", np.clip(rim * 0.5, 0, 1))
    pic[...] = out
    if info is not None:
        info["tracks"] = m_all
    return pic


# ---------------------------------------------------------------- shadows on the ground
def building_shadow():
    x0, x1 = BLD["x"]
    z0, z1 = BLD["z"]
    h = BLD["cope"]
    pts = [(x1, 0.0, z0), T.onto((x1, h, z0), "ground"), T.onto((x1, h, z1), "ground"), (x1, 0.0, z1)]
    return poly_mask([K.P(*p) for p in pts], soft=0.7)


def flagpole_reach():
    """How high up the pole the part is whose shadow reaches the foot of the wall, and the x on the wall there."""
    h_wall = (BLD["z"][0] - FLAG["z"]) / K.SUN[1]
    return h_wall, FLAG["x"] + K.SUN[0] * h_wall


def flagpole_shadow_ground():
    x, z = FLAG["x"], FLAG["z"]
    h_wall, xw = flagpole_reach()
    a, b = K.P(x, 0, z), K.P(xw, 0, BLD["z"][0])
    return mask_line(SHAPE, [a, b], [3.4, 2.8], soft=0.4)


# ---------------------------------------------------------------- the fence and the gate
def fence_veil(pic, info):
    """The mesh as a fine gray veil with a diamond weave, everywhere on the fence's plane but the gate's opening; its
    shadow on the desert just beyond. (The posts and rails are the details'.)"""
    zf, h = FENCE["z"], FENCE["h"]
    xg0, xg1 = GATE["x"]
    X, Y = K.wall_xy(SHAPE, zf)
    x, y = grid(SHAPE)
    sh_pts = [(FENCE["x"][0], 0.0, zf), (FENCE["x"][1], 0.0, zf), T.onto((FENCE["x"][1], h, zf), "ground"), T.onto((FENCE["x"][0], h, zf), "ground")]
    shm = poly_mask([K.P(*p) for p in sh_pts], soft=0.5) * (0.35 + 0.25 * (np.sin((x + y * 0.6) * 1.9) > 0.3))
    shade_ground(pic, shm, 0.40)
    on = (Y > 4.0) & (Y < h - 3.0) & (X > FENCE["x"][0]) & (X < FENCE["x"][1]) & ~((X > xg0) & (X < xg1))
    weave = (np.abs(((X + Y) / 5.0) % 1.0 - 0.5) < 0.12) | (np.abs(((X - Y) / 5.0) % 1.0 - 0.5) < 0.12)
    over(pic, "#80848a", on.astype(F32) * (0.22 + 0.10 * weave))
    over(pic, "#eceeec", on.astype(F32) * weave * 0.08)
    # the open leaf's mesh, and the white plate of its sign
    q, (ux, uz) = T.gate_leaf_points()
    over(pic, "#80848a", poly_mask([K.P(*p) for p in q]) * 0.28)
    w = GATE["x"][1] - GATE["x"][0]
    t0, t1 = 0.20, 0.20 + 62.0 / w
    hx, hz = q[0][0], q[0][2]
    corner = lambda t, yy: (hx + ux * w * t, yy, hz + uz * w * t - 1.5)
    plate = [corner(t0, 142.0), corner(t1, 142.0), corner(t1, 98.0), corner(t0, 98.0)]
    info["gate_sign"] = plate
    over(pic, "#f2efe6", poly_mask([K.P(*p) for p in plate]))
    return pic


def fence_lines():
    """The posts, rails and wires, and the gate's frame: crisp, for the details. -> sheets."""
    zf, h = FENCE["z"], FENCE["h"]
    xg0, xg1 = GATE["x"]
    s, sl = Paper(SHAPE), Paper(SHAPE)
    d, dl = Solid(s, (0.0, zf), 0.0, cam=K.CAM), Solid(sl, (0.0, zf), 0.0, cam=K.CAM)
    posts = [p for p in np.arange(FENCE["x"][0], FENCE["x"][1] + 1, FENCE["posts"]) if not (xg0 - 40 < p < xg1 + 40)] + [xg0, xg1]
    for (a, b) in ((FENCE["x"][0], xg0), (xg1, FENCE["x"][1])):
        dl.line([(a, h - 2, 0), (b, h - 2, 0)], T.face(T.STEEL, FRONT), 2.6, 0.95)
        dl.line([(a, h - 1, 0), (b, h - 1, 0)], "#eef0ee", 0.8, 0.8)
        dl.line([(a, 6, 0), (b, 6, 0)], "#7a7e84", 1.0, 0.6)
    for px_ in sorted(posts):
        gate_post = px_ in (xg0, xg1)
        T.fence_post(d, dl, float(px_), zf, h=h + (12.0 if gate_post else 0.0), r=4.4 if gate_post else 3.2)
    # the leaf's frame: a pipe round it, a middle rail, a brace; its hinges on the right post; a chain hanging from it
    q, (ux, uz) = T.gate_leaf_points()
    g, gl = Paper(SHAPE), Paper(SHAPE)
    dg = Solid(g, (0.0, 0.0), 0.0, cam=K.CAM)
    frame = T.face(T.STEEL, 0.8)
    for a, b in ((0, 1), (1, 2), (2, 3), (3, 0)):
        dg.line([q[a], q[b]], frame, 3.0, 0.98)
    dg.line([(q[0][0], 92.0, q[0][2]), (q[1][0], 92.0, q[1][2])], frame, 2.2, 0.95)
    dg.line([(q[0][0], 8.0, q[0][2]), (q[2][0], q[2][1] - 4, q[2][2])], frame, 1.6, 0.9)
    dg.line([(q[3][0], q[3][1] - 2, q[3][2]), (q[2][0], q[2][1] - 2, q[2][2])], "#eef0ee", 0.9, 0.9)
    return [s, sl, g, gl]


def gate_sign_lines(info):
    """The plate's small words (PLEASE DO NOT LOOK DIRECTLY AT THE BUILDING): too small to read from here, three lines of
    small dark print and a border; the look says them."""
    plate = info["gate_sign"]
    s = Paper(SHAPE)
    d = Solid(s, (0.0, 0.0), 0.0, cam=K.CAM)
    (ax, ay, az), (bx, by, bz), (cx_, cy_, cz_), (dx_, dy_, dz_) = plate
    for i, frac in enumerate((0.26, 0.50, 0.74)):
        yy = ay + (dy_ - ay) * frac
        words = ((0.10, 0.36), (0.42, 0.56), (0.62, 0.90)) if i == 0 else (((0.14, 0.58), (0.64, 0.86)) if i == 1 else ((0.12, 0.30), (0.36, 0.88)))
        for (u0, u1) in words:
            p0 = (ax + (bx - ax) * u0, yy, az + (bz - az) * u0 - 0.2)
            p1 = (ax + (bx - ax) * u1, yy, az + (bz - az) * u1 - 0.2)
            d.line([p0, p1], "#2a2e4a", 1.6, 0.85)
    d.line([plate[0], plate[1], plate[2], plate[3], plate[0]], "#5a5e6c", 0.8, 0.9)
    return [s]


# ---------------------------------------------------------------- the building: the roof, the unit, the front
def facade_pixels():
    X, Y = K.wall_xy(SHAPE, BLD["z"][0])
    m = (X >= BLD["x"][0]) & (X <= BLD["x"][1]) & (Y >= 0) & (Y <= BLD["cope"])
    return X, Y, m


def paint_roof(pic, info):
    """The roof from above: tar and pea gravel in the sun; the shadows lying on it (the unit's, the ducts', the
    flagpole's and its pennant's)."""
    Xr, Zr, below = K.floor_xz(SHAPE, BLD["deck"])
    x0, x1 = BLD["x"]
    z0, z1 = BLD["z"]
    m = (Xr >= x0) & (Xr <= x1) & (Zr >= z0) & (Zr <= z1) & (below > 0)
    info["roof"] = m
    c = np.empty(SHAPE + (3,), F32)
    c[...] = lit(T.DECK, TOP)
    g = K.ground_noise(SHAPE, 7.0, SEED + 51, y=BLD["deck"], calm=0.8, octaves=2) - 0.5
    b = K.ground_noise(SHAPE, 160.0, SEED + 52, y=BLD["deck"]) - 0.5
    c = c * (1 + g[..., None] * 0.18 + b[..., None] * 0.08)
    over(pic, np.clip(c, 0, 1), m.astype(F32))
    sh = np.zeros(SHAPE, F32)
    ux0, ux1 = UNIT["x"]
    uz0, uz1 = UNIT["z"]
    yt = UNIT["top"]
    unit_sh = [(ux1, BLD["deck"], uz0), T.onto((ux1, yt, uz0), "roof"), T.onto((ux1, yt, uz1), "roof"), (ux1, BLD["deck"], uz1)]
    sh = np.maximum(sh, poly_mask([K.P(*p) for p in unit_sh], soft=0.6))
    for dct in T.DUCTS:
        ax1 = dct["x"][1]
        ay1 = dct["y"][1]
        az0, az1 = dct["z"]
        pts = [(ax1, BLD["deck"], az0), T.onto((ax1, ay1, az0), "roof"), T.onto((ax1, ay1, az1), "roof"), (ax1, BLD["deck"], az1)]
        sh = np.maximum(sh, poly_mask([K.P(*p) for p in pts], soft=0.5))
    h_wall, xw = flagpole_reach()
    lo = h_wall + BLD["cope"]
    a = T.onto((FLAG["x"], lo, FLAG["z"]), "roof")
    b = T.onto((FLAG["x"], FLAG["h"], FLAG["z"]), "roof")
    sh = np.maximum(sh, mask_line(SHAPE, [K.P(*a), K.P(*b)], [2.4, 1.9], soft=0.4))
    up, dn = T.pennant_points(0.25)
    pen = [K.P(*T.onto(p, "roof")) for p in up + list(reversed(dn))]
    sh = np.maximum(sh, poly_mask(pen, soft=0.6) * 0.9)
    ball = K.P(*T.onto((FLAG["x"], FLAG["h"] + 4.0, FLAG["z"]), "roof"))
    sh = np.maximum(sh, poly_mask([(ball[0] + 2.6 * math.cos(t), ball[1] + 1.2 * math.sin(t)) for t in np.linspace(0, 6.28, 12)], soft=0.3))
    sh = sh * m
    info["roof_shadow"] = sh
    shade_ground(pic, sh, 0.62)
    return pic


def paint_facade(pic, info):
    """The front: cinder block painted beige, in the sun, each block a hair different (its joints are the details'); a
    concrete footing; the metal coping; the doorway (the hall inside, which the door's cut-outs cover); the shadows on
    it (the awning's, the flagpole's, the pipe's, the scupper's, the sign's, the keypad's)."""
    X, Y, m = facade_pixels()
    info["facade"] = m
    info["facade_xy"] = (X, Y)
    course = np.floor(Y / 20.0)
    off = (course % 2) * 20.0
    block = np.floor((X + off) / 40.0)
    h = np.sin(block * 12.9898 + course * 78.233) * 43758.5453
    h = h - np.floor(h)
    c = np.empty(SHAPE + (3,), F32)
    c[...] = lit(T.BEIGE, FRONT)
    c = c * (1 + (h[..., None] - 0.5) * 0.035)
    foot = Y < 10.0
    c = np.where(foot[..., None], lit("#bdb6aa", FRONT), c)
    cap = Y > BLD["deck"]
    c = np.where(cap[..., None], lit(T.COPE, FRONT), c)
    grime = np.clip((60 - Y) / 60.0, 0, 1) * 0.07
    streak = (noise(SHAPE, (3, 40), SEED + 41, 3) > 0.74) & (Y > 205) & (Y < BLD["deck"])
    c = c * (1 - grime[..., None]) * np.where(streak[..., None], 0.97, 1.0)
    over(pic, np.clip(c, 0, 1), m.astype(F32))
    a2, b2, d2, dl2 = T.drafts(SHAPE, 0.0)
    _door_hall(d2, dl2)
    hole = doorway_mask()
    hc, ha = a2.done()
    over(pic, hc, ha * hole)
    info["hall_lines"] = b2
    info["doorway"] = hole
    sh = np.zeros(SHAPE, F32)
    zw = BLD["z"][0]
    ax0, ax1 = AWNING["x"]
    ay = AWNING["y"][0]
    zo = zw - AWNING["out"]
    aw = [(ax0, ay, zw), (ax1, ay, zw), T.onto((ax1, ay, zo), "wall"), T.onto((ax0, ay, zo), "wall")]
    sh = np.maximum(sh, poly_mask([K.P(*p) for p in aw], soft=0.5))
    h_wall, xw = flagpole_reach()
    pole_w = FLAG["r"] * 2.0
    sh = np.maximum(sh, poly_mask(wall_rect(xw - pole_w / 2, xw + pole_w / 2, 0.0, BLD["cope"] + 1, zw), soft=0.4) * m)
    dx, dy = 0.416 * (zw - PIPE["z"]), -1.25 * (zw - PIPE["z"])
    sh = np.maximum(sh, poly_mask(wall_rect(PIPE["x"] - PIPE["r"] + dx, PIPE["x"] + PIPE["r"] + dx, PIPE["elbow"] + dy, PIPE["top"] + dy, zw), soft=0.4))
    sx0, sx1 = SCUPPER["x"]
    sy0, sy1 = SCUPPER["y"]
    d_s = 0.416 * 14.0
    sh = np.maximum(sh, poly_mask(wall_rect(sx0 + d_s, sx1 + d_s, sy0 - 17.0, sy1 - 17.0, zw), soft=0.4) * m)
    sgx0, sgx1 = SIGN["x"]
    sgy0, sgy1 = SIGN["y"]
    p_ = SIGN["proud"]
    sh = np.maximum(sh, poly_mask(wall_rect(sgx0 + 0.416 * p_, sgx1 + 0.416 * p_, sgy0 - 1.25 * p_, sgy1 - 1.25 * p_, zw), soft=0.3))
    kx0, kx1 = KEYPAD["x"]
    ky0, ky1 = KEYPAD["y"]
    sh = np.maximum(sh, poly_mask(wall_rect(kx0 + 1.5, kx1 + 1.5, ky0 - 4.0, ky1 - 4.0, zw), soft=0.3))
    sh = sh * m
    info["wall_shadow"] = sh
    shade_ground(pic, sh, 0.66, tone="#7a84c0")
    return pic


def doorway_mask():
    """The doorway in the front wall: all that is seen of the inside is seen through it."""
    return (poly_mask(wall_rect(DOOR["x"][0], DOOR["x"][1], 0.0, DOOR["h"], BLD["z"][0])) > 0.5).astype(F32)


def awning_shadow():
    """The awning's shadow on the wall (and the door): down and to the right of it."""
    zw = BLD["z"][0]
    ax0, ax1 = AWNING["x"]
    ay = AWNING["y"][0]
    zo = zw - AWNING["out"]
    aw = [(ax0, ay, zw), (ax1, ay, zw), T.onto((ax1, ay, zo), "wall"), T.onto((ax0, ay, zo), "wall")]
    return poly_mask([K.P(*p) for p in aw], soft=0.5)


def _door_hall(d, dl):
    """The doorway's inside, as the backdrop has it under the door's cut-outs: a short hall lit by tubes, beige walls,
    gray tiles, a mat (WIPE, again), the elevator's plain doors at the end; no leaf."""
    x0, x1 = DOOR["x"]
    h = DOOR["h"]
    zw = BLD["z"][0]
    depth = 260.0
    d.poly([(x0, 0, zw), (x1, 0, zw), (x1, 0, zw + depth), (x0, 0, zw + depth)], "#8e9088")
    d.poly([(x0, 0, zw + depth), (x1, 0, zw + depth), (x1, h, zw + depth), (x0, h, zw + depth)], "#c8c2a6")
    d.poly([(x1, 0, zw), (x1, 0, zw + depth), (x1, h, zw + depth), (x1, h, zw)], "#b4ae94")
    d.poly([(x0, 0, zw), (x0, 0, zw + depth), (x0, h, zw + depth), (x0, h, zw)], "#a49e86")
    d.poly([(x0, h, zw), (x1, h, zw), (x1, h, zw + depth), (x0, h, zw + depth)], "#e6e8dc")
    for zz in (60.0, 120.0, 180.0, 240.0):
        dl.line([(x0, 0.2, zw + zz), (x1, 0.2, zw + zz)], "#7a7c76", 0.7, 0.6)
    d.poly([(x0 + 24, 0.4, zw + 30), (x1 - 24, 0.4, zw + 30), (x1 - 24, 0.4, zw + 80), (x0 + 24, 0.4, zw + 80)], "#5c5650")
    d.poly([(x0 + 20, 0, zw + depth - 0.5), (x1 - 20, 0, zw + depth - 0.5), (x1 - 20, 190, zw + depth - 0.5), (x0 + 20, 190, zw + depth - 0.5)], "#a8aaa4")
    dl.line([((x0 + x1) / 2, 0, zw + depth - 1), ((x0 + x1) / 2, 190, zw + depth - 1)], "#6a6c68", 0.8, 0.8)


def paint_building(pic, info):
    """The building, back to front: the roof seen from above, the unit and its ducts on it, then the front wall."""
    paint_roof(pic, info)
    a, b, d, dl = T.drafts(SHAPE, 0.0)
    T.unit_body(d, dl)
    lay(pic, (a,))
    info["lines"].append(b)
    info["unit_alpha"] = np.maximum(a.done()[1], b.done()[1])
    paint_facade(pic, info)
    info["building"] = np.clip(info["facade"].astype(F32) + info["roof"].astype(F32) + info["unit_alpha"], 0, 1)
    return pic


# ---------------------------------------------------------------- pass 1: the under-painting
def under():
    info = {"lines": []}
    pic = paint_sky()
    paint_range(pic)
    paint_desert(pic)
    sagebrush_field(pic)
    paint_lot(pic)
    fence_veil(pic, info)
    paint_tracks(pic, info)
    pipe_stain(pic)
    shade_ground(pic, np.clip(building_shadow() + flagpole_shadow_ground(), 0, 1), 0.62)
    paint_building(pic, info)
    # the near corners deeper and warmer, the far desert a little hazier: to hold the eye on the building
    x, y = grid(SHAPE)
    low = np.clip((y - 470) / 130.0, 0, 1) ** 1.4
    side = np.clip(np.abs(x - 330) / 470.0, 0, 1) ** 2
    v = np.clip(low * 0.16 + low * side * 0.18, 0, 0.4)
    pic[...] = pic * (1 - v[..., None]) + pic * col("#6a4a3a")[None, None, :] * 1.3 * v[..., None]
    return np.clip(pic, 0, 1), info


# ---------------------------------------------------------------- pass 2: the brush
def paint(pic, fast=False):
    if fast:
        return pic.copy()
    b = strokes(pic, sizes=(12, 6, 3), seed=2, density=1.5, jitter=0.03, keep=0.30)
    return np.clip(b, 0, 1)


# ---------------------------------------------------------------- pass 3: the details
def facade_joints(pic, info):
    """The blocks' joints, crisp over the brushwork but quiet (the blocks are painted, the joints half filled)."""
    X, Y = info["facade_xy"]
    m = info["facade"] & (Y > 10.0) & (Y < BLD["deck"])
    course = np.floor(Y / 20.0)
    off = (course % 2) * 20.0
    fy = (Y / 20.0) % 1.0
    fx = ((X + off) / 40.0) % 1.0
    k = K.k_at(BLD["z"][0])
    jy = (fy < 1.2 / (20.0 * k)) & m
    jx = (fx < 1.0 / (40.0 * k)) & m
    door = (X > DOOR["x"][0] - 1) & (X < DOOR["x"][1] + 1) & (Y < DOOR["h"] + 1)
    joint = (jy | jx) & ~door
    pic[jy & ~door] = pic[jy & ~door] * np.array([0.92, 0.915, 0.94], F32)
    pic[jx & ~door & ~jy] = pic[jx & ~door & ~jy] * np.array([0.955, 0.95, 0.965], F32)
    lit_edge = np.roll(jy, -1, axis=0) & m & ~door & ~jy
    pic[lit_edge] = np.clip(pic[lit_edge] * 1.025, 0, 1)
    return pic


def building_lines():
    """The crisp edges of the building: the coping (its lit top edge, its shadow line under the lip, its run back along
    the roof's sides and back edge), the footing's top, the wall's corners."""
    s, sl = Paper(SHAPE), Paper(SHAPE)
    d, dl = Solid(s, (0.0, BLD["z"][0]), 0.0, cam=K.CAM), Solid(sl, (0.0, BLD["z"][0]), 0.0, cam=K.CAM)
    x0, x1 = BLD["x"]
    zl = BLD["z"][1] - BLD["z"][0]
    y0, y1 = BLD["deck"], BLD["cope"]
    # the coping along the sides and the back, seen from above: a thin metal edge
    for (xa, xb) in ((x0, x0 + 8.0), (x1 - 8.0, x1)):
        d.poly([(xa, y1, 0), (xb, y1, 0), (xb, y1, zl), (xa, y1, zl)], lit(T.COPE, TOP))
    d.poly([(x0, y1, zl - 8.0), (x1, y1, zl - 8.0), (x1, y1, zl), (x0, y1, zl)], lit(T.COPE, TOP))
    d.poly([(x0, y1, -2.0), (x1, y1, -2.0), (x1, y1, 6.0), (x0, y1, 6.0)], lit(T.COPE, TOP))      # its top along the front, from above
    dl.line([(x0, y1, -2.0), (x1, y1, -2.0)], "#fbfaf4", 1.1, 0.95)                                  # the front edge in the sun
    dl.line([(x0, y0 - 0.5, -2.0), (x1, y0 - 0.5, -2.0)], "#5e5866", 1.0, 0.8)                         # under the lip
    dl.line([(x0, 10.0, -0.2), (x1, 10.0, -0.2)], "#8c857a", 0.8, 0.6)                                # the footing's top
    dl.line([(x0, 0.0, 0.0), (x0, y1, 0.0)], "#6a6070", 1.0, 0.6)                                      # the corners
    dl.line([(x1, 0.0, 0.0), (x1, y1, 0.0)], "#5a5262", 1.2, 0.7)
    dl.line([(x0, 0.6, -0.5), (x1, 0.6, -0.5)], "#4a4450", 1.2, 0.55)                                 # where the wall meets the gravel
    return [s, sl]


def sign_lines():
    """The long sign: a white enamel board with a navy border, its edge lit, its three lines of neat capitals."""
    s, sl = Paper(SHAPE), Paper(SHAPE)
    z = BLD["z"][0] - SIGN["proud"]
    d, dl = Solid(s, (0.0, z), 0.0, cam=K.CAM), Solid(sl, (0.0, z), 0.0, cam=K.CAM)
    x0, x1 = SIGN["x"]
    y0, y1 = SIGN["y"]
    d.poly([(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)], lit("#efede4", FRONT))
    d.poly([(x0, y1, 0), (x1, y1, 0), (x1, y1, SIGN["proud"]), (x0, y1, SIGN["proud"])], lit("#d8d6cc", TOP))
    dl.line([(x0 + 3.5, y0 + 3.5, -0.1), (x1 - 3.5, y0 + 3.5, -0.1), (x1 - 3.5, y1 - 3.5, -0.1), (x0 + 3.5, y1 - 3.5, -0.1), (x0 + 3.5, y0 + 3.5, -0.1)],
            T.NAVY, 1.0, 0.85)
    dl.line([(x0, y1, -0.2), (x1, y1, -0.2)], "#ffffff", 1.0, 0.9)
    dl.line([(x0, y0, -0.2), (x1, y0, -0.2)], "#8a8676", 0.9, 0.8)
    return [s, sl]


LETTERS = None


def pen_glyphs():
    from nevada_store_kit import PEN, NARROW
    pen, narrow = dict(PEN), dict(NARROW)
    pen["·"] = [[(2, 3.3), (2, 2.7)]]
    narrow["·"] = 0.5
    return pen, narrow


def caps_mask(text, cap, track, pen_w, ss=8):
    """One line of neat capitals (the store's PEN letters, drawn steady), crisp: -> (mask, width) in picture pixels."""
    pen, narrow = pen_glyphs()
    from PIL import ImageDraw
    u = cap / 6.0
    w = sum((4 * narrow.get(ch, 1.0) + 6 * track) * u for ch in text) - 6 * track * u
    Wp, Hp = int(math.ceil(w + 4)) * ss, int(math.ceil(cap + 4)) * ss
    im = Image.new("L", (Wp, Hp), 0)
    dr = ImageDraw.Draw(im)
    wd = max(1, int(round(pen_w * ss)))
    x, base = 2.0, 2.0 + cap
    for ch in text:
        k = narrow.get(ch, 1.0)
        for stroke in pen.get(ch, []):
            pts = [((x + ((px - 2) * k + 2 * k) * u) * ss, (base - py * u) * ss) for px, py in stroke]
            if len(pts) == 1:
                pts = pts * 2
            dr.line(pts, fill=255, width=wd, joint="curve")
            for (qx, qy) in (pts[0], pts[-1]):
                dr.ellipse([qx - wd / 2, qy - wd / 2, qx + wd / 2, qy + wd / 2], fill=255)
        x += (4 * k + 6 * track) * u
    a = np.asarray(im.resize((Wp // ss, Hp // ss), Image.BOX), F32) / 255
    return np.clip((a - 0.25) / 0.45, 0, 1), w


SIGN_LINES = [("OFFICE OF PECULIAR SECTORS", 11.0, 0.30, 1.6), ("DESERT FIELD HEADQUARTERS", 7.0, 0.30, 1.15),
              ("AUTHORIZED PERSONNEL ONLY · PLEASE WIPE YOUR FEET", 7.0, 0.20, 1.1)]


def letter_sign(pic, info):
    """The sign's words, laid square on the board (it faces us: no slant), each line centred: the lettering is the
    sign's, readable at 800 x 600 (the smaller lines 7 px high)."""
    z = BLD["z"][0] - SIGN["proud"]
    (lx, ty) = K.P(SIGN["x"][0], SIGN["y"][1], z)
    (rx, by) = K.P(SIGN["x"][1], SIGN["y"][0], z)
    cx = (lx + rx) / 2
    y = ty + 3.0
    ink = col(T.NAVY)
    masks = np.zeros(SHAPE, F32)
    for text, cap, track, pw in SIGN_LINES:
        a, w = caps_mask(text, cap, track, pw)
        x0 = int(round(cx - w / 2)) - 2
        y0 = int(round(y)) - 2
        h, ww = a.shape
        masks[y0:y0 + h, x0:x0 + ww] = np.maximum(masks[y0:y0 + h, x0:x0 + ww], a)
        y += cap + 3.0
    over(pic, ink, masks)
    info["sign_box"] = [round(lx, 1), round(ty, 1), round(rx, 1), round(by, 1)]
    return masks


def small_things():
    """The window, the keypad, the drainpipe with its scupper, straps and elbow: crisp, lit from the left."""
    s, sl = Paper(SHAPE), Paper(SHAPE)
    zw = BLD["z"][0]
    d, dl = Solid(s, (0.0, zw), 0.0, cam=K.CAM), Solid(sl, (0.0, zw), 0.0, cam=K.CAM)
    # the window: frosted glass in an aluminium frame, a little sill under it
    x0, x1 = WINDOW["x"]
    y0, y1 = WINDOW["y"]
    d.poly([(x0 - 3, y0 - 3, -0.5), (x1 + 3, y0 - 3, -0.5), (x1 + 3, y1 + 3, -0.5), (x0 - 3, y1 + 3, -0.5)], lit("#b8bcc0", FRONT))
    d.poly([(x0, y0, -0.2), (x1, y0, -0.2), (x1, y1, -0.2), (x0, y1, -0.2)], "#cfdbe0")
    d.poly([(x0 + 2, y0 + (y1 - y0) * 0.55, -0.3), (x1 - 2, y0 + (y1 - y0) * 0.55, -0.3), (x1 - 2, y1 - 2, -0.3), (x0 + 2, y1 - 2, -0.3)], "#e2eaee")
    dl.line([((x0 + x1) / 2, y0, -0.6), ((x0 + x1) / 2, y1, -0.6)], "#9aa0a6", 1.0, 0.9)
    dl.line([(x0 - 3, y1 + 3, -0.7), (x1 + 3, y1 + 3, -0.7)], "#f4f6f6", 0.9, 0.9)
    d.poly([(x0 - 5, y0 - 3, -5.0), (x1 + 5, y0 - 3, -5.0), (x1 + 5, y0 - 6, -5.0), (x0 - 5, y0 - 6, -5.0)], lit("#c8c2b4", FRONT))
    dl.line([(x0 - 5, y0 - 3, -5.0), (x1 + 5, y0 - 3, -5.0)], "#fbf6ec", 0.8, 0.9)
    # the keypad: a small gray box, twelve buttons, a little light
    kx0, kx1 = KEYPAD["x"]
    ky0, ky1 = KEYPAD["y"]
    d.poly([(kx0, ky0, -2.0), (kx1, ky0, -2.0), (kx1, ky1, -2.0), (kx0, ky1, -2.0)], lit("#8a8e94", FRONT))
    dl.line([(kx0, ky1, -2.1), (kx1, ky1, -2.1)], "#dfe2e6", 0.7, 0.9)
    for i in range(3):
        for j in range(4):
            bx = kx0 + 3.0 + i * 3.6
            by = ky1 - 5.0 - j * 3.4
            dl.ball(bx, by, -2.3, 0.75, "#d8dade", 0.9)
    dl.ball(kx1 - 2.0, ky1 - 1.8, -2.4, 0.8, "#d84a3a", 0.95)
    # the electric meter in its gray box, low by the left corner, and its conduit up the wall to the roof (the unit's)
    mx0, mx1, my0, my1 = -478.0, -446.0, 96.0, 140.0
    d.poly([(mx0, my0, -6.0), (mx1, my0, -6.0), (mx1, my1, -6.0), (mx0, my1, -6.0)], lit("#9a9ea2", FRONT))
    d.poly([(mx0, my1, -6.0), (mx1, my1, -6.0), (mx1, my1, 0.0), (mx0, my1, 0.0)], lit("#9a9ea2", TOP))
    d.disc((mx0 + mx1) / 2, my0 + 24.0, 7.0, "#c8d0d4", z=-6.2)
    dl.line([((mx0 + mx1) / 2 - 3, my0 + 24.0, -6.4), ((mx0 + mx1) / 2 + 3, my0 + 26.0, -6.4)], "#3a3c44", 0.8, 0.9)
    dl.line([(mx0, my1, -6.1), (mx1, my1, -6.1)], "#eef0f0", 0.8, 0.9)
    T.round_thing(d, (mx0 + mx1) / 2, -3.0, 2.0, my1, BLD["deck"] + 2.0, "#a8acb0", n=3)
    for yy in (180.0, 240.0):
        dl.line([((mx0 + mx1) / 2 - 3.2, yy, -5.4), ((mx0 + mx1) / 2 + 3.2, yy, -5.4)], "#6a6e74", 1.2, 0.9)
    # the drainpipe: the scupper box at the roof's edge, the pipe down the corner, its straps, the elbow out toward us
    sx0, sx1 = SCUPPER["x"]
    sy0, sy1 = SCUPPER["y"]
    zp = PIPE["z"] - zw
    r = PIPE["r"]
    d.poly([(sx0, sy0, -14.0), (sx1, sy0, -14.0), (sx1, sy1, -14.0), (sx0, sy1, -14.0)], lit(T.STEEL, FRONT))
    d.poly([(sx0, sy1, -14.0), (sx1, sy1, -14.0), (sx1, sy1, 0.0), (sx0, sy1, 0.0)], lit("#6a6e74", 0.3))
    d.poly([(sx0, sy0, -14.0), (PIPE["x"] - r, sy0 - 8.0, zp), (PIPE["x"] + r, sy0 - 8.0, zp), (sx1, sy0, -14.0)], lit(T.STEEL, FRONT * 0.85))
    dl.line([(sx0, sy1, -14.2), (sx1, sy1, -14.2)], "#f4f6f8", 0.9, 0.9)
    T.round_thing(d, PIPE["x"], zp, r, PIPE["elbow"] + 8.0, sy0 - 8.0, T.STEEL, n=6, glint="#f4f6f8")
    for ys in PIPE["straps"]:
        d.poly([(PIPE["x"] - r - 1.6, ys, zp - r - 0.4), (PIPE["x"] + r + 1.6, ys, zp - r - 0.4), (PIPE["x"] + r + 1.6, ys + 3.2, zp - r - 0.4),
                (PIPE["x"] - r - 1.6, ys + 3.2, zp - r - 0.4)], lit("#8e9298", FRONT))
        dl.line([(PIPE["x"] - r - 1.6, ys + 3.2, zp - r - 0.5), (PIPE["x"] + r + 1.6, ys + 3.2, zp - r - 0.5)], "#e8eaec", 0.7, 0.9)
        dl.ball(PIPE["x"] - r - 1.0, ys + 1.6, zp - r - 0.6, 0.6, "#4a4c52", 0.9)
        dl.ball(PIPE["x"] + r + 1.0, ys + 1.6, zp - r - 0.6, 0.6, "#4a4c52", 0.9)
    # the elbow: the pipe bends out toward us at its foot (a bend of 10 cm), a short spout sloping down, its mouth open
    ys_, R = PIPE["elbow"] + 8.0, 10.0
    my, mz = PIPE["mouth"]
    mzr = mz - zw
    cl = [(ys_ - R * math.sin(f), zp - R + R * math.cos(f)) for f in np.linspace(0, math.pi / 2, 6)]
    cl += [(cl[-1][0] + (my - cl[-1][0]) * t, cl[-1][1] + (mzr - cl[-1][1]) * t) for t in np.linspace(0.25, 1.0, 4)]
    for (ya, za), (yb, zb) in zip(cl[:-1], cl[1:]):
        d.poly([(PIPE["x"] - r, ya + r * 0.8, za), (PIPE["x"] + r, ya + r * 0.8, za), (PIPE["x"] + r, yb + r * 0.8, zb), (PIPE["x"] - r, yb + r * 0.8, zb)], lit(T.STEEL, TOP))
        d.poly([(PIPE["x"] - r, ya - r * 0.6, za - 0.1), (PIPE["x"] - r * 0.2, ya - r * 0.6, za - 0.1), (PIPE["x"] - r * 0.2, yb + r * 0.8, zb - 0.1),
                (PIPE["x"] - r, yb + r * 0.8, zb - 0.1)], lit(T.STEEL, FRONT), 0.6)
    d.disc(PIPE["x"], my, r, lit(T.STEEL, 0.5), z=mzr - 0.2)
    d.disc(PIPE["x"], my, r - 1.4, "#2a2830", z=mzr - 0.3)
    dl.line([(PIPE["x"] - r * math.cos(t), my + r * math.sin(t), mzr - 0.4) for t in np.linspace(0.2, math.pi - 0.2, 7)], "#f4f6f8", 0.8, 0.9)
    dl.line([(PIPE["x"] + r, ys_, zp - r), (PIPE["x"] + r, my + r * 0.6, mzr)], "#5a5e66", 0.8, 0.6)
    return [s, sl]


def mat_words(pic):
    """The mat on the gravel in front of the door, dark rubber, WIPE across it in pale letters (seen from here, lying
    down: the letters are flattened by the distance as the mat is)."""
    X, Z, below = K.floor_xz(SHAPE)
    x0, x1 = MAT["x"]
    z0, z1 = MAT["z"]
    u = (X - x0) / (x1 - x0)
    v = (Z - z0) / (z1 - z0)
    on = (u >= 0) & (u <= 1) & (v >= 0) & (v <= 1) & (below > 0)
    base = np.empty(SHAPE + (3,), F32)
    base[...] = lit("#4c4642", TOP)
    edge = (u < 0.04) | (u > 0.96) | (v < 0.07) | (v > 0.93)
    base = np.where(edge[..., None], lit("#3a3432", TOP), base)
    over(pic, base, on.astype(F32))
    # the word, on the mat's own square (u across it, v toward the door), each pixel the average of the word over the
    # patch of mat it covers (4 x 4 points), so that its thin bars survive the foreshortening
    a, w = caps_mask("WIPE", 40.0, 0.34, 8.5, ss=4)
    H_, W_ = a.shape
    tw = 66.0                                                    # the word's length on the mat, cm
    th = tw * H_ / W_
    px, py = grid(SHAPE)
    acc = np.zeros(SHAPE, F32)
    for oy in (-0.375, -0.125, 0.125, 0.375):
        for ox in (-0.375, -0.125, 0.125, 0.375):
            tt = K.EYE * K.FOCAL / np.maximum(py + oy - K.HZ, 0.5)          # (= Z0 + z on the gravel at that point)
            gz, gx = tt - K.CAM.Z0, (px + ox - K.VX) * tt / K.FOCAL
            uu = (gx - (x0 + x1) / 2) / tw + 0.5
            vv = ((z0 + z1) / 2 - gz) / th + 0.5
            inside = (uu > 0) & (uu < 1) & (vv > 0) & (vv < 1)
            acc += sample(a, np.clip(uu * (W_ - 1), 0, W_ - 1), np.clip(vv * (H_ - 1), 0, H_ - 1)) * inside
    m = np.clip((acc / 16.0 * on - 0.22) / 0.36, 0, 1)
    over(pic, lit("#d8cfb8", TOP), m)
    return pic


def ground_bits(pic, seed=SEED + 60):
    """Stones on the gravel, coarser near us; dry tufts along the wall's foot and round the edges of the lot."""
    rng = np.random.default_rng(seed)
    s, sh = Paper(SHAPE), Paper(SHAPE)
    for i in range(170):
        y = FENCE_ROW + 6 + (rng.random() ** 0.55) * (K.H - FENCE_ROW - 6)
        x = rng.uniform(-10, K.W + 10)
        gx, gz = K.ground_at(x, y)
        if BLD["x"][0] - 10 < gx < BLD["x"][1] + 10 and BLD["z"][0] - 6 < gz < BLD["z"][1] + 10:
            continue
        k = K.k_at(gz)
        r = rng.uniform(1.2, 3.4) * k * (1.0 if rng.random() < 0.9 else 1.8)
        if r < 0.55:
            continue
        tone_ = rng.uniform(0.0, 1.0)
        c = ramp(np.array([[tone_]], F32), [(0.0, "#a4988a"), (0.5, "#c9bea8"), (1.0, "#ddd2bc")])[0, 0]
        sh.ellipse(x + r * 0.5, y + r * 0.15, r * 1.0, max(0.5, r * 0.45), "#6a6488", 0.30)
        s.ellipse(x, y, r, max(0.5, r * 0.62), c, 0.9)
        if r > 1.4:
            s.ellipse(x - r * 0.3, y - r * 0.25, r * 0.4, max(0.4, r * 0.25), "#ece4d2", 0.6)
    for i in range(26):                                                     # tufts along the foot of the wall
        x = rng.uniform(BLD["x"][0] + 10, BLD["x"][1] - 10)
        if DOOR["x"][0] - 40 < x < DOOR["x"][1] + 40 or -60 < x < 100:
            continue
        px_, py_ = K.P(x, 0, BLD["z"][0] - rng.uniform(2, 10))
        tuft(s, px_, py_, rng.uniform(3.0, 6.0), int(rng.integers(1e6)), colors=("#6e6a48", "#a69a66", "#d4c48e"))
    for i in range(18):                                                     # and along the fence
        x = rng.uniform(-1500, 1500)
        if GATE["x"][0] - 40 < x < GATE["x"][1] + 40:
            continue
        px_, py_ = K.P(x, 0, FENCE["z"] - rng.uniform(5, 30))
        tuft(s, px_, py_, rng.uniform(2.0, 4.0), int(rng.integers(1e6)), colors=("#6e6a48", "#a69a66", "#d4c48e"))
    lay(pic, (sh, s))
    return pic


def gravel(pic, info, seed=SEED + 90):
    """The lot's gravel, crisp over the brushwork: small pebbles, light and dark, bigger and more of them near us; none
    in the ruts (pressed smooth) and none on the building or the mat."""
    rng = np.random.default_rng(seed)
    s = Paper(SHAPE)
    keep = (1.0 - np.clip(info["tracks"] * 1.6, 0, 1)) * lot_mask() * (1.0 - info["building"])
    for i in range(5200):
        y = FENCE_ROW + 4 + (rng.random() ** 0.62) * (K.H - FENCE_ROW - 4)
        x = rng.uniform(0, K.W)
        if keep[int(min(y, K.H - 1)), int(min(x, K.W - 1))] < 0.5:
            continue
        near = (y - FENCE_ROW) / (K.H - FENCE_ROW)
        r = (0.35 + 0.75 * near) * rng.uniform(0.7, 1.4)
        light = rng.random() < 0.55
        c = "#ebe2d0" if light else ("#958a7a" if rng.random() < 0.6 else "#a8927c")
        s.ellipse(x, y, r * 1.2, r * 0.8, c, rng.uniform(0.45, 0.85))
    lay(pic, (s,))
    return pic


def details(pic, info, fast=False):
    """Every built edge put back crisply over the brushwork, and the small things."""
    sagebrush_field(pic, near_only=True, hide=info["building"])
    gravel(pic, info)
    lay(pic, fence_lines(), amount=1.0 - info["building"])
    lay(pic, gate_sign_lines(info))
    ground_bits(pic)
    mat_words(pic)
    facade_joints(pic, info)
    lay(pic, info["lines"])
    lay(pic, [info["hall_lines"]], amount=info["doorway"])
    lay(pic, building_lines())
    lay(pic, sign_lines())
    letter_sign(pic, info)
    lay(pic, small_things())
    return pic


# ---------------------------------------------------------------- the cut-outs
def cutout(back, draw, z_ref=0.0, seed=4, sizes=(5, 3, 2), keep=0.45, fast=False, under=None):
    """A thing drawn on its own two sheets through the camera, brushed over the colour under it, its lines on top.
    -> (color, alpha)."""
    a, b, d, dl = T.drafts(SHAPE, z_ref)
    draw(d, dl)
    c, al = a.done()
    lc, la = b.done()
    ys, xs = np.where(al > 0.5)
    under_c = under if under is not None else (np.median(back[ys, xs], axis=0) if len(ys) else col("#c8bea9"))
    return brushed(c, al, lc, la, under_c, seed=seed, sizes=sizes, keep=keep, fast=fast)


def can_shadow(state):
    """The can's own shadow (it goes where the can goes): on the gravel back and to the right, and up the wall where it
    reaches it. -> mask."""
    r, top = CAN["r"], CAN["top"]
    if state == "tipped":
        cx, cz = CAN["tipped"]
        pts = []
        for t in np.linspace(0, 2 * math.pi, 16, endpoint=False):
            p = (cx + math.cos(t) * 38.0, r * 1.7, cz + math.sin(t) * 26.0)
            pts.append(K.P(*T.onto(p, "ground")))
        return poly_mask(pts, soft=0.6)
    cx, cz = CAN["standing"] if state == "standing" else CAN["pipe"]
    m = np.zeros(SHAPE, F32)
    ring = [(cx + math.cos(t) * r, cz + math.sin(t) * r) for t in np.linspace(0, 2 * math.pi, 20, endpoint=False)]
    tops = [T.onto((x, top, z), "ground") for x, z in ring]
    # where the thrown shadow would pass the wall, it climbs it instead
    pts = [K.P(x, 0, z) for x, z in ring] + [K.P(*p) for p in tops]
    hull = _hull(pts)
    m = poly_mask(hull, soft=0.6)
    zw = BLD["z"][0]
    wall_pts = [T.onto((x, top, z), "wall") for x, z in ring]
    wall_pts = [p for p in wall_pts if p[1] > 0]
    if wall_pts:
        base_pts = [(x, 0.0, zw) for x, z in ring]
        wm = poly_mask(_hull([K.P(*p) for p in wall_pts + base_pts]), soft=0.5)
        X, Y, fm = facade_pixels()
        m = np.maximum(m * (1 - fm), wm * fm)
    return m


def _hull(pts):
    """The convex hull of picture points."""
    pts = sorted(set((round(p[0], 3), round(p[1], 3)) for p in pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def can_cut(back, state, fast=False):
    """The can in one of its three places, with its own shadow: the shadow is part of the cut-out (darkened ground and
    wall, cut with it), so that it goes where the can goes."""
    if state == "tipped":
        draw = lambda d, dl: T.can_tipped(d, dl, CAN["tipped"])
        zr = CAN["tipped"][1]
    else:
        at = CAN["standing"] if state == "standing" else CAN["pipe"]
        draw = lambda d, dl: T.can_standing(d, dl, at)
        zr = at[1]
    c, a = cutout(back, draw, z_ref=zr, seed=21 + len(state), sizes=(4, 2), keep=0.5, fast=fast, under=col("#9ea3aa"))
    sm = can_shadow(state)
    shadow = back.copy()
    shade_ground(shadow, np.ones(SHAPE, F32), 0.62)
    hard = (sm > 0.45) & (a < 0.5)
    out_c = np.where(hard[..., None], shadow, c)
    out_a = np.maximum((a > 0.5).astype(F32), hard.astype(F32))
    return out_c, out_a


def lettering_on_can(pic, alpha, state):
    """REGULATION, stencilled across the standing can's front (small at this distance: the look reads it)."""
    if state == "tipped":
        return
    cx, cz = CAN["standing"] if state == "standing" else CAN["pipe"]
    z = cz - CAN["r"]
    a, w = caps_mask("REGULATION", 3.7, 0.04, 0.8, ss=8)                  # OFFICE-17A: narrower, to sit on the can's front
    px_, py_ = K.P(cx, 40.0, z)
    x0, y0 = int(round(px_ - w / 2)) - 2, int(round(py_ - 4.2 / 2)) - 2
    h, ww = a.shape
    region = pic[y0:y0 + h, x0:x0 + ww]
    # only on the can's own front (its cut-out holds its shadow too): within 0.86 of its radius of its middle
    left, right = K.P(cx - CAN["r"] * 0.86, 40.0, cz)[0], K.P(cx + CAN["r"] * 0.86, 40.0, cz)[0]
    cols = np.arange(x0, x0 + ww)[None, :]
    mask = a * (alpha[y0:y0 + h, x0:x0 + ww] > 0.5) * ((cols >= left) & (cols <= right))
    region[...] = region * (1 - mask[..., None] * 0.85) + col("#2a2c34") * mask[..., None] * 0.85


def flag_cut(back, fast=False):
    return cutout(back, T.flagpole, z_ref=FLAG["z"], seed=31, sizes=(3, 2), keep=0.6, fast=fast, under=col("#c8ccd2"))


def awning_cut(back, fast=False):
    return cutout(back, T.awning, z_ref=BLD["z"][0] - AWNING["out"], seed=33, sizes=(3, 2), keep=0.55, fast=fast)


def door_cut(back, open_=False, fast=False, shadow=None):
    """The door, shut or swung in; the awning's shadow lies across its top as it does across the wall."""
    c, a = cutout(back, T.door_open if open_ else T.door_shut, z_ref=BLD["z"][0], seed=35 + open_, sizes=(4, 2), keep=0.55, fast=fast)
    a = a * doorway_mask()                                                       # (the hall and the leaf are seen only through the doorway)
    if shadow is not None:
        shade_ground(c, shadow, 0.66, tone="#7a84c0")
    return c, a


def grille_cut(back, off=False, fast=False):
    """The grille on its studs (its slits cut clear, so that the fan shows through them turning), or off and leaning
    with the wing nuts in a row beside it."""
    if off:
        return cutout(back, T.grille_off, z_ref=UNIT["z"][0], seed=37, sizes=(3, 2), keep=0.6, fast=fast)
    c, a = cutout(back, T.grille, z_ref=UNIT["z"][0], seed=38, sizes=(3, 2), keep=0.6, fast=fast)
    # the slits: clear
    s = Paper(SHAPE)
    d = Solid(s, (0.0, UNIT["z"][0]), 0.0, cam=K.CAM)
    x0, x1 = GRILLE["x"]
    y0, y1 = GRILLE["y"]
    b, n = 6.0, 11
    for i in range(n):
        ya = y0 + b + (y1 - y0 - 2 * b) * i / n
        d.line([(x0 + b + 2, ya + 1.0, -GRILLE["proud"] - 0.7), (x1 - b - 2, ya + 1.0, -GRILLE["proud"] - 0.7)], "#000000", 1.0, 1.0)
    slit = s.done()[1] > 0.5
    a = np.where(slit, 0.0, a)
    return c, a


def nut_cut(back, i, fast=False):
    nx, ny = NUTS[i]
    return cutout(back, lambda d, dl: T.wing_nut(d, dl, (nx, ny, -GRILLE["proud"] - 1.0)), z_ref=UNIT["z"][0], seed=41 + i, sizes=(2,),
                  keep=0.8, fast=True)


def switch_cut(back, on=True, fast=False):
    return cutout(back, lambda d, dl: T.switch_lever(d, dl, on), z_ref=UNIT["z"][0], seed=45 + on, sizes=(2,), keep=0.8, fast=True)


def front_plane(back, fast=False, seed=SEED + 80):
    """Right at the front: sagebrush in the bottom corners, darker and warmer than the middle of the picture (people
    pass behind it)."""
    s = Paper(SHAPE)
    tones = ("#2c342e", "#4c5848", "#7c8a70", "#b4bc9c")
    dark = ("#232a26", "#3e4a3e", "#6c7a64", "#aab494")
    sagebrush(s, -10, 612, 62, seed + 1, tones=tones)
    sagebrush(s, 52, 626, 52, seed + 2, tones=dark)
    sagebrush(s, 786, 616, 58, seed + 3, tones=tones)
    sagebrush(s, 732, 632, 44, seed + 4, tones=dark)
    tuft(s, 104, 602, 16, seed + 5)
    tuft(s, 690, 604, 14, seed + 6)
    c, a = s.done()
    return c, a


# ---------------------------------------------------------------- the frames: the fan turning, the pennant stirring
def fan_frames(back, n=4, fast=False):
    """The fan behind the grille, turning: n frames, a third of a turn between the first and the n+1th (three blades);
    the blades smeared a little along their turn. Cropped to the intake's opening. -> [(color, alpha)] full size."""
    out = []
    for i in range(n):
        ang = i * 120.0 / n
        acc_c, acc_a = None, None
        for j, da in enumerate((-9.0, -4.5, 0.0)):                         # a little smear behind each blade
            a_, b_, d, dl = T.drafts(SHAPE, UNIT["z"][0])
            d.poly([(GRILLE["x"][0] + 3, GRILLE["y"][0] + 3, 17.9), (GRILLE["x"][1] - 3, GRILLE["y"][0] + 3, 17.9),
                    (GRILLE["x"][1] - 3, GRILLE["y"][1] - 3, 17.9), (GRILLE["x"][0] + 3, GRILLE["y"][1] - 3, 17.9)], "#26252c")
            T.fan(d, dl, ang + da, still=False)
            c, al = a_.done()
            lc, la = b_.done()
            over(c, lc, la)
            if acc_c is None:
                acc_c, acc_a = c * 0.0, al * 0.0
            w = (0.25, 0.30, 0.45)[j]
            acc_c = acc_c + c * w
            acc_a = np.maximum(acc_a, al)
        out.append((np.clip(acc_c / 1.0, 0, 1), acc_a))
    return out


def pennant_frames(back, n=4, fast=False):
    """The pennant stirring on its pole: n frames of one slow wave along it, O.O.P.S. in white on it."""
    out = []
    for i in range(n):
        ph = i / n
        a_, b_, d, dl = T.drafts(SHAPE, FLAG["z"])
        T.pennant(d, dl, ph)
        c, al = a_.done()
        lc, la = b_.done()
        over(c, lc, la)
        letter_pennant(c, al, ph)
        out.append((c, al))
    return out


def letter_pennant(c, al, phase):
    """O.O.P.S. on the pennant, following its wave: the word drawn flat (along it, across it) and laid point by point on
    the pennant's surface."""
    a, w = caps_mask("O.O.P.S.", 30.0, 0.22, 4.6, ss=4)
    H_, W_ = a.shape
    up, dn = T.pennant_points(phase)
    n = len(up) - 1
    acc = np.zeros(SHAPE, F32)
    cnt = np.zeros(SHAPE, F32)
    u0, u1 = 0.05, 0.56                                                  # OFFICE-17A: ending where the pennant is still wide enough for the last full stop
    us = np.linspace(u0, u1, 140)
    vs = np.linspace(0.0, 1.0, 40)
    for u in us:
        i = min(int(u * n), n - 1)
        t = u * n - i
        top = tuple(up[i][j] + (up[i + 1][j] - up[i][j]) * t for j in range(3))
        bot = tuple(dn[i][j] + (dn[i + 1][j] - dn[i][j]) * t for j in range(3))
        hu = (u - u0) / (u1 - u0)
        for v in vs:
            p = tuple(top[j] + (bot[j] - top[j]) * v for j in range(3))
            px_, py_ = K.P(*p)
            ix, iy = int(px_), int(py_)
            if 0 <= ix < K.W and 0 <= iy < K.H:
                height = (top[1] - bot[1])
                vv = 0.5 + (v - 0.5) * height / 22.0 + 0.03              # the word is 22 cm high, centred across the pennant (its stops a hair up)
                if 0 <= vv <= 1:
                    acc[iy, ix] += a[int(vv * (H_ - 1)), int(hu * (W_ - 1))]
                cnt[iy, ix] += 1
    m = np.where(cnt > 0, acc / np.maximum(cnt, 1), 0) * (al > 0.5)
    m = np.clip((m - 0.25) / 0.4, 0, 1)
    over(c, "#f6f4ee", m)


# ---------------------------------------------------------------- pass 4: the finish
def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.012, amount=0.016):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    n = len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0))
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, n)))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def crop_frames(names, origin_pad=1):
    """Crop a moving thing's frames (painted full size) to the box that holds all of them; say where the box is and
    where its foot is (the middle of its bottom edge). -> {files, rect, foot, at}"""
    ims = [Image.open(f"{OUT}/{n}") for n in names]
    boxes = [im.convert("RGBA").getchannel("A").getbbox() for im in ims]
    x0 = min(b[0] for b in boxes) - origin_pad
    y0 = min(b[1] for b in boxes) - origin_pad
    x1 = max(b[2] for b in boxes) + origin_pad
    y1 = max(b[3] for b in boxes) + origin_pad
    for im, n in zip(ims, names):
        c = im.crop((x0, y0, x1, y1))
        c.save(f"{OUT}/{n}", optimize=True, transparency=im.info["transparency"]) if "transparency" in im.info else c.save(f"{OUT}/{n}", optimize=True)
    foot = [(x1 - x0) // 2, y1 - y0]
    return {"files": names, "rect": [x0, y0, x1 - x0, y1 - y0], "foot": foot, "at": [x0 + foot[0], y0 + foot[1]]}


# ---------------------------------------------------------------- everything
CUT_ORDER = ["grille", "nut-1", "nut-2", "nut-3", "nut-4", "switch", "door", "awning", "trash", "flagpole", "limo", "front"]
ALTS = {"grille-off": ["grille", "nut-1", "nut-2", "nut-3", "nut-4"], "switch-off": ["switch"], "door-open": ["door"],
        "trash-tipped": ["trash"], "trash-pipe": ["trash"], "limo-door-open": ["limo"]}


def all_cutouts(pic, info, fast=False):
    import office_lot_limo as LM
    cuts = {}
    cuts["grille"] = grille_cut(pic, fast=fast)
    for i in range(4):
        cuts[f"nut-{i + 1}"] = nut_cut(pic, i, fast=fast)
    cuts["switch"] = switch_cut(pic, True, fast=fast)
    cuts["door"] = door_cut(pic, False, fast=fast, shadow=awning_shadow())
    cuts["awning"] = awning_cut(pic, fast=fast)
    cuts["trash"] = can_cut(pic, "standing", fast=fast)
    cuts["flagpole"] = flag_cut(pic, fast=fast)
    cuts["limo"] = LM.car(SHAPE, False, fast=fast)
    cuts["front"] = front_plane(pic, fast=fast)
    cuts["grille-off"] = grille_cut(pic, off=True, fast=fast)
    cuts["switch-off"] = switch_cut(pic, False, fast=fast)
    cuts["door-open"] = door_cut(pic, True, fast=fast, shadow=awning_shadow())
    cuts["trash-tipped"] = can_cut(pic, "tipped", fast=fast)
    cuts["trash-pipe"] = can_cut(pic, "pipe", fast=fast)
    cuts["limo-door-open"] = LM.car(SHAPE, True, fast=fast)
    for name in ("trash", "trash-pipe"):
        c, a = cuts[name]
        lettering_on_can(c, a, "standing" if name == "trash" else "pipe")
    return cuts


def compose(back, cuts, show):
    pic = back.copy()
    for name in show:
        c, a = cuts[name]
        over(pic, c, (a > 0.5).astype(F32))
    return pic


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    fast = mode == "fast"
    base, info = under()
    to_image(base).save(f"{WORK}/1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = paint(base, fast=fast)
    details(pic, info, fast=fast)
    to_image(pic).save(f"{WORK}/2-back.png")
    print("details", round(time.time() - t0, 1))
    cuts = all_cutouts(pic, info, fast=fast)
    first = CUT_ORDER
    to_image(compose(pic, cuts, first)).save(f"{WORK}/3-all.png")
    later = [n for n in CUT_ORDER if n not in ("grille", "nut-1", "nut-2", "nut-3", "nut-4", "switch", "door", "trash", "limo")] + \
            ["grille-off", "switch-off", "door-open", "trash-pipe", "limo-door-open"]
    to_image(compose(pic, cuts, later)).save(f"{WORK}/3-later.png")
    print("cut-outs", round(time.time() - t0, 1))
    if mode in ("fast", "paint"):
        sys.exit()
    import office_lot_out
    office_lot_out.write(pic, info, cuts, t0)

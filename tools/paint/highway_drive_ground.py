"""The road and the desert from straight above (highway_drive.py, ROAD-18P): drive-road.png, drive-desert-l.png,
drive-desert-r.png.

Maps, not views: no perspective, no horizon, nothing standing up (that is the sheet's), no long shadows (the engine lays
the things' shadows), no shine (the low sun's shine down the road moves with the eye: it is light, the engine's or the
merge's). Each repeats end to end every 64 m (highway_drive_kit.py: the strips, their rows and columns, the stop).

THE SAME HAND. Everything is highway.py's: its ground is painted by distance from near to the horizon; here each part
keeps the colour it has close by (highway_drive_kit.BASE: the asphalt, the shoulders' sand, the plain), and its own
textures at the sizes highway.py gives them on the ground (land.texture is laid on the ground: its blotches are 1.3 to
1.7 m across and three times as long along the road), its own colours for every mark, the same brush pass, the same
grade. The road is 3.10 m each side of the middle, its edge wandering a few cm; the sand of the shoulders runs from
the asphalt out to about 4.3 m (3.6 to 5.4); the wheels have polished two tracks in each lane, 0.78 m either side of its
middle (1.55 m), and oil has dripped between them.

THE PAINTING'S ROAD, WHERE THE CAMERA STOPS. The marks highway.details() lays on the road (highway_drive_world.road_marks:
the worn white edge lines at 2.87 to 2.98 m, the yellow dashes, the seven cracks across, the three seams along, the two
mended patches, the old brake marks) are laid here as the painting has them from 8 to 72 m ahead of its lens, at the
place along the loop where that ground is when the camera stops (column = (z + STOP_S) * ppm, mod the loop), and so are
the strip of tire and the green bottle on the left shoulder and the hubcap on the right. The yellow dashes are the
painting's, seven to a loop. The rest of the loop has marks of its own: two tar snakes where the camera stands when it
stops (under it and behind it), and two cracks across and a seam along 46 to 62 m ahead of it, where the painting's road
is bare (there they are a pixel or less across), so that the whole loop has something going by under the wagon.

SEAMS. Along the road every texture is periodic (nevada_limo_drive_kit.pnoise), the brush pass is laid over a wrapped
copy (brush_wrapped), marks near the ends are drawn again a loop away, and the grain is periodic. Across, the three strips
are cut from one set of textures laid over the whole ground from 30 m left to 30 m right, so the plain runs on from one
strip into the next; within 0.3 m of the two seams the brush pass fades out on both sides, so that the strokes of one
strip do not stop short at the other's edge. The desert's last 2 m (out by 30 m) calm down to the plain's own colour, for
the engine carries a strip's outer rows on beyond it."""

import math

import numpy as np

from brush import F32, blur, lerp, over, rgb, step, tint
from highway_kit import Paper, grade, mix
from nevada_limo_drive_kit import brush_wrapped, pnoise
import highway_drive_kit as K

ROAD, LANE = 3.10, 1.55
WORLD_PPM = 24.0                                   # the shared textures: 30 m left to 30 m right, at 24 px a metre
WORLD_ROWS = int(60 * WORLD_PPM)
WORLD_COLS = int(K.LOOP * WORLD_PPM)


# ---------------------------------------------------------------- textures laid on the ground, shared by the strips
def world_textures(seed):
    """Noise over the whole ground (rows: X from -30 to +30 m; columns: w from 0 to 64 m, repeating), at 24 px a metre,
    at highway.py's own sizes on the ground. `cell` is (along, across) in metres."""
    shape = (WORLD_ROWS, WORLD_COLS)

    def n(along, across, s, octaves=4):
        return pnoise(shape, (along * WORLD_PPM, across * WORLD_PPM), seed + s, octaves)

    return {
        "blot": n(4.6, 1.67, 1, 4),                  # land.texture(150): the plain's blotches
        "fine": n(0.92, 0.33, 2, 3),                 # land.texture(30)
        "drift": n(37.0, 12.8, 3, 3),                # the warmer and cooler drifts (noise (340, 90) on the screen)
        "bare": n(16.0, 2.9, 4, 3),                  # land.texture(260, stretch 0.5): the paler flats where nothing grows
        "sandfine": n(0.68, 0.24, 5, 3),             # land.texture(22): the shoulders' sand
        "wob": n(1.85, 0.67, 6, 3),                  # land.texture(60): the wandering of the road's edge and the sand's
        "wob2": n(2.7, 1.7, 7, 3),                   # noise (90, 26): the sand's outer edge, wandering more
        "blown": n(2.5, 0.9, 8, 3),                  # land.texture(80): sand blown in over the road's edge
    }


FAR_WPPM = 8.0                                     # PAINT-18B: the far textures, 150 m left to 150 m right, 8 px a metre
FAR_WROWS = int(300 * FAR_WPPM)
FAR_WCOLS = int(K.LOOP * FAR_WPPM)


def far_textures(seed):
    """The plain's textures (as world_textures) over the whole ground out to 150 m either side, at 8 px a metre: the far
    strips are painted from them, and the near deserts mix into them over their last 3 m (27 to 30 m out), so that the
    plain runs on from one into the other with no seam."""
    shape = (FAR_WROWS, FAR_WCOLS)

    def n(along, across, s, octaves=4):
        return pnoise(shape, (along * FAR_WPPM, across * FAR_WPPM), seed + s, octaves)

    return {"blot": n(4.6, 1.67, 1, 4), "fine": n(0.92, 0.33, 2, 3), "drift": n(37.0, 12.8, 3, 3), "bare": n(16.0, 2.9, 4, 3)}


def sample_world(field, strip, lo=-30.0, ppm=WORLD_PPM):
    """A shared texture as a strip sees it: its rows' X and its columns' w, read bilinearly (wrapping along)."""
    X = K.strip_X(strip)
    w = K.strip_w(strip)
    rows, cols = field.shape
    fr = (X - lo) * ppm - 0.5
    fc = w * ppm - 0.5
    r0 = np.clip(np.floor(fr).astype(np.intp), 0, rows - 1)
    r1 = np.clip(r0 + 1, 0, rows - 1)
    tr = np.clip(fr - np.floor(fr), 0, 1).astype(F32)[:, None]
    c0 = np.floor(fc).astype(np.intp)
    tc = (fc - c0).astype(F32)[None, :]
    c0 %= cols
    c1 = (c0 + 1) % cols
    a = field[r0][:, c0] * (1 - tc) + field[r0][:, c1] * tc
    b = field[r1][:, c0] * (1 - tc) + field[r1][:, c1] * tc
    return (a * (1 - tr) + b * tr).astype(F32)


# ---------------------------------------------------------------- the plain and the shoulders, as highway.under() mixes them
PALE = np.array([1.37, 1.54, 1.22], F32)           # the paler flats against the plain (highway's `pale` ramp over `flat`, near)
# What the textures do to each part's mean, taken back out, so that each strip's parts come out at highway_drive_kit.BASE
# (measured on the finished strips: the paler flats lift the plain, the polished tracks the asphalt, the blown sand...)
TUNE = {"road": np.array([0.970, 0.9745, 0.9925], F32), "shoulder": np.array([1.0355, 1.0409, 1.0183], F32),
        "plain": np.array([0.9623, 0.9136, 0.9597], F32)}


def base_of(part):
    return np.clip(K.ungrade(K.BASE[part]) * TUNE[part], 0, 1).astype(F32)


def plain(T, strip, TF=None):
    """The plain: its colour close by, blotched, drifting warmer and cooler, with paler flats where nothing grows.
    (PAINT-18B: from 27 m out it is painted from the far textures TF, all of it from 30 m.)"""
    lo, hi, _ = K.STRIPS[strip]
    if lo >= -30.0 and hi <= 30.0:
        g = {k: sample_world(v, strip) for k, v in T.items()}
    else:
        g = {}
    if TF is not None and (hi > 27.0 or lo < -27.0):
        gf = {k: sample_world(v, strip, -150.0, FAR_WPPM) for k, v in TF.items()}
        wf = np.clip((np.abs(K.strip_X(strip)) - 27.0) / 3.0, 0, 1).astype(F32)[:, None]
        wf = wf * wf * (3 - 2 * wf)
        for k, v in gf.items():
            g[k] = v if k not in g else (g[k] * (1 - wf) + v * wf).astype(F32)
    base = base_of("plain")
    col = np.broadcast_to(base, g["blot"].shape + (3,)).astype(F32).copy()
    col *= (1 + (g["blot"] - 0.5)[..., None] * 0.22 + (g["fine"] - 0.5)[..., None] * 0.12)
    k = (g["drift"] - 0.5) * 0.07
    col[..., 0] += k
    col[..., 2] -= k * 0.8
    col = lerp(col, np.clip(col * PALE, 0, 1), (step(0.50, 0.85, g["bare"]) * 0.6)[..., None])
    return np.clip(col, 0, 1).astype(F32), g


def shoulders(col, g, X):
    """The sand of the shoulders over the plain: from the asphalt's edge out to about 4.3 m, wandering. -> its mask."""
    side = np.abs(X)[:, None]
    sh_in = ROAD - 0.06 + (g["wob"] - 0.5) * 0.26
    sh_out = ROAD + 1.20 + (g["wob"] - 0.5) * 1.50 + (g["wob2"] - 0.5) * 1.20
    m = np.clip((side - sh_in) / 0.02, 0, 1) * np.clip((sh_out - side) / 0.12, 0, 1)
    sand = base_of("shoulder") * (1 + (g["sandfine"] - 0.5)[..., None] * 0.20)
    over(col, np.clip(sand, 0, 1), (m * 0.92).astype(F32))
    return m.astype(F32), np.clip(sand, 0, 1).astype(F32)


# ---------------------------------------------------------------- the road
ROAD_DARKER = np.array([0.985, 0.975, 0.985], F32)  # PAINT-18B: the painting's road is a little darker and more violet


def asphalt(col, g, sand, seed):
    """The asphalt over the middle 6.2 m, as highway.under() lays it: blotched, two polished wheel tracks in each lane,
    oil dripped between them, sand blown in over its edges. -> its mask."""
    h, w = col.shape[:2]
    X = K.strip_X("road")[:, None]
    side = np.abs(X)
    edge = ROAD + (g["wob"] - 0.5) * 0.09
    road = np.clip((edge - side) * 48.0 + 0.5, 0, 1)                     # its edge one pixel soft
    blot = pnoise((h, w), (3.7 * 48, 1.33 * 48), seed + 1, 4) - 0.5      # land.texture(120)
    fine = pnoise((h, w), (0.49 * 48, 0.18 * 48), seed + 2, 3) - 0.5     # land.texture(16)
    tar = base_of("road") * ROAD_DARKER * (1 + blot[..., None] * 0.16 + fine[..., None] * 0.18)
    # PAINT-18B: the painting's grain and wear (its road is rougher: seen at the painting's distances its brush marks are
    # drawn out along the road): worn streaks along, at three sizes, the aggregate, and darker sealed patches of tar
    st1 = pnoise((h, w), (2.2 * 48, 0.30 * 48), seed + 4, 3) - 0.5
    st2 = pnoise((h, w), (0.7 * 48, 0.10 * 48), seed + 5, 2) - 0.5
    st3 = pnoise((h, w), (6.0 * 48, 0.55 * 48), seed + 6, 3) - 0.5
    agg = np.random.default_rng(seed + 7).normal(0, 1, (h, w)).astype(F32)
    agg = (agg + np.roll(agg, 1, 1)) * 0.5                                    # (two pixels along: the stones in the tar)
    tar = tar * (1 + st1[..., None] * 0.12 + st2[..., None] * 0.25 + st3[..., None] * 0.05 + agg[..., None] * 0.10)
    pn = pnoise((h, w), (5.0 * 48, 1.2 * 48), seed + 8, 3)
    sealed = step(0.62, 0.70, pn) * (0.75 + 0.5 * (pnoise((h, w), (1.2 * 48, 0.4 * 48), seed + 9, 2) - 0.5))
    tar = lerp(tar, tar * np.array([0.88, 0.86, 0.92], F32), np.clip(sealed, 0, 1)[..., None])
    oilnoise = pnoise((h, w), (2.4 * 48, 0.33 * 48), seed + 3, 3)
    for lane in (-LANE, LANE):
        for off in (-0.78, 0.78):
            tar = tar * (1 + (np.exp(-((X - lane - off) / 0.30) ** 2) * 0.10)[..., None])
        tar = tar * (1 - (np.exp(-((X - lane) / 0.26) ** 2) * 0.10 * (0.5 + oilnoise))[..., None])
    over(col, np.clip(tar, 0, 1), road.astype(F32))
    blown = step(0.56, 0.84, g["blown"]) * np.exp(-((side - ROAD) / 0.46) ** 2) * road
    over(col, sand, np.clip(blown * 0.62, 0, 1).astype(F32))
    return road.astype(F32), np.clip(tar, 0, 1).astype(F32)


def road_edges(col, road, seed):
    """highway.details(): the broken lip of the asphalt, a little darker, and a pale line of grit just outside it."""
    h, w = road.shape
    e = blur(road, 1.2)
    n1 = pnoise((h, w), (14 * 3.4, 5 * 3.4), seed + 11, 3)
    n2 = pnoise((h, w), (20 * 3.4, 4 * 3.4), seed + 12, 3)
    lip = np.clip(1 - np.abs(e - 0.5) * 3.2, 0, 1) * (0.45 + 0.75 * n1)
    tint(col, "#6a5478", np.clip(lip * 0.75, 0, 1).astype(F32))
    outer = np.clip(1 - np.abs(e - 0.14) * 7, 0, 1) * n2
    over(col, "#f6cca0", np.clip(outer * 0.5, 0, 1).astype(F32))


def to_map(X, w, strip="road"):
    """A place on the ground (X m across, w m along) -> a strip's picture (x, y)."""
    lo, hi, ppm = K.STRIPS[strip]
    return w * ppm, (X - lo) * ppm


def _loop_copies(xs, width, margin):
    """The shifts (0, and a loop either way) at which a mark spanning picture columns xs shows in the picture."""
    out = [0.0]
    if min(xs) < margin:
        out.append(float(width))
    if max(xs) > width - margin:
        out.append(-float(width))
    return out


FADED = rgb("#fff0b0")


def _unfade_dash(color, z):
    """A dash's colour close by: highway.details() mixes each piece toward #fff0b0 by how far off it is."""
    row = K.HZ + 270.15625 * 800.0 / (z * 100.0)
    f = float(np.clip(1 - (row - K.HZ) / 90.0, 0, 1) ** 1.3)
    c = rgb(color)
    return np.clip((c - FADED * f) / max(1 - f, 1e-3), 0, 1) if f > 0 else c


def painting_marks(marks, sheet, width, seed):
    """Lay highway.details()'s road marks (highway_drive_world.road_marks) in the road's picture where the ground they
    are on is when the camera stops: those from 8 to 72 m ahead of the painting's lens."""
    near, far = 8.0, 8.0 + K.LOOP
    wof = lambda z: (z + K.STOP_S) % K.LOOP

    def clip_line(pts, widths):
        """The parts of a polyline from `near` to `far` (z), as runs of (X, z, width)."""
        runs, cur = [], []
        for (X, z), wd in zip(pts, widths if widths is not None else [None] * len(pts)):
            if near <= z < far:
                cur.append((X, z, wd))
            elif cur:
                runs.append(cur); cur = []
        if cur:
            runs.append(cur)
        return runs

    def lay(run, color, alpha, kind, w0=None):
        # a run's columns: z mapped to the loop, unwrapped so that a run crossing the loop's end stays whole
        zs = [p[1] for p in run]
        base = wof(zs[0]) - zs[0]
        pts = [to_map(p[0], p[1] + base) for p in run]
        xs = [q[0] for q in pts]
        for shift in _loop_copies(xs, width, 60):
            q = [(x + shift, y) for x, y in pts]
            if kind == "poly":
                sheet.poly(q, color, alpha)
            elif kind == "taper":                     # a band as wide as the mark at each point, one shape
                half = [max(0.3, p[2] * 48.0 / 2) for p in run]
                sheet.poly([(x, y - hw) for (x, y), hw in zip(q, half)] + [(x, y + hw) for (x, y), hw in reversed(list(zip(q, half)))], color, alpha)
            else:                                     # (square ends: a crack's pieces join without a darker knot)
                sheet.line(q, color, max(0.6, (w0 if w0 is not None else run[0][2]) * 48.0), alpha, round_ends=False)

    order = {"patch": 0, "patch-edge": 1, "crack": 2, "seam": 2, "brake": 2, "edge-line": 3, "dash": 4}
    joined = []                                       # a crack's segments, laid one by one in the painting, as one line
    for m in marks:
        prev = joined[-1] if joined else None
        if (prev is not None and m["what"] in ("crack", "seam") and prev["what"] == m["what"] and prev["color"] == m["color"]
                and prev["alpha"] == m["alpha"] and np.allclose(prev["pts"][-1], m["pts"][0])):
            prev["pts"] = prev["pts"] + m["pts"][1:]
            prev["width"] = prev["width"] + m["width"][1:]
        else:
            joined.append(dict(m))
    marks = joined
    for m in sorted(marks, key=lambda m: order[m["what"]]):
        what, pts = m["what"], m["pts"]
        if what in ("edge-line", "dash", "patch"):
            zs = [p[1] for p in pts]
            z0, z1 = min(zs), max(zs)
            if z1 <= near or z0 >= far:
                continue
            if what == "edge-line":
                # each worn segment of the white line, cut to the stretch laid here, in its colour close by
                za, zb = max(z0, near), min(z1, far)
                if zb - za < 0.02:
                    continue
                Xs = sorted(p[0] for p in pts)
                a0, a1 = (Xs[0] + Xs[1]) / 2, (Xs[2] + Xs[3]) / 2
                run = [(a0, za, None), (a1, za, None), (a1, zb, None), (a0, zb, None)]
                lay(run, "#cfc4d2", m["alpha"], "poly")
            elif what == "dash":
                run = [(p[0], p[1], None) for p in pts]
                lay(run, _unfade_dash(m["color"], z0), m["alpha"], "poly")
            else:
                run = [(p[0], p[1], None) for p in pts]
                lay(run, m["color"], m["alpha"], "poly")
        else:
            for run in clip_line(pts, m["width"]):
                if len(run) < 2:
                    continue
                if what == "brake":
                    lay(run, m["color"], m["alpha"], "taper")
                else:
                    lay(run, m["color"], m["alpha"], "line", w0=float(np.mean([p[2] for p in run])))


def tar_snakes(sheet, width, seed):
    """Two tar snakes of the loop's own, where the camera stands when it stops (and sees only 64 m off): cracks sealed with
    tar, wandering a little, darker and glossier than the cracks the cold has opened."""
    rng = np.random.default_rng(seed)
    for (X0, w0, length, dirn) in ((-1.1, 1.2, 2.6, 1), (2.0, 4.6, 1.8, -1)):
        pts = []
        X, w = X0, w0
        for i in range(14):
            pts.append(to_map(X, w))
            w += length / 13
            X += dirn * 0.02 + rng.normal(0, 0.035)
        sheet.line(pts, "#2a2440", 0.05 * 48, 0.55)
        sheet.line([(x, y - 0.5) for x, y in pts[2:10]], "#8a7c9c", 0.6, 0.35)
    far_cracks(sheet, seed + 100)


def far_cracks(sheet, seed):
    """The loop's own cracks where the stopped camera sees only far road, 46 to 62 m ahead (the painting has its marks
    nearer): one right across where the cold has opened it, one across the right-hand lane, and a seam along, as
    highway.details() draws them (#3e3456, 2 to 4 cm, broken here and there), so that the whole loop has something going
    by under the wagon. When the camera stops they lie on rows 364 to 377, a pixel or less across."""
    rng = np.random.default_rng(seed)
    for k, (w0, X0, X1) in enumerate(((46.5, -3.1, 3.1), (57.3, 0.2, 3.05))):
        m = max(4, int((X1 - X0) / 0.3))
        pts = []
        for j in range(m + 1):
            w = w0 + rng.normal(0, 0.09) + 0.2 * math.sin(j * 0.5 + k * 2.3)
            pts.append(to_map(X0 + (X1 - X0) * j / m, w))
        for j in range(m):
            if rng.random() < 0.12:
                continue
            sheet.line([pts[j], pts[j + 1]], "#3e3456", (0.022 + 0.02 * rng.random()) * 48, 0.72, round_ends=False)
    pts, X = [], -0.9
    for w in np.geomspace(47.0, 61.5, 30):
        X += rng.normal(0, 0.024)
        pts.append(to_map(X, w))
    for j in range(len(pts) - 1):
        if rng.random() < 0.3:
            continue
        sheet.line([pts[j], pts[j + 1]], "#3e3456", 0.028 * 48, 0.62, round_ends=False)


PEBBLES = [  # the grit of the ground, placed in the world once: (seed, X from, X to, stones a square metre, radius m)
    (1841, -8.0, -3.15, 0.8, (0.015, 0.04)), (1842, 3.15, 8.0, 0.8, (0.015, 0.04)),
    (1843, -30.0, -8.0, 0.5, (0.02, 0.05)), (1844, 8.0, 30.0, 0.5, (0.02, 0.05))]


def pebbles(sheet, strip):
    """Small stones lying about (a stone of the painting's sort, and the bigger ones, are things on the sheet: these are
    the grit of the ground), each lit on its far side, where the sun is, a sliver of shade toward us. Placed in the world
    once (PEBBLES), each strip drawing those it shows, so that at a seam both draw the same stone."""
    lo, hi, ppm = K.STRIPS[strip]
    _, wpx = K.strip_shape(strip)
    for seed, a0, a1, per_m2, size in PEBBLES:
        rng = np.random.default_rng(seed)
        n = rng.poisson(K.LOOP * (a1 - a0) * per_m2)
        Xs, ws, rs, tones = rng.uniform(a0, a1, n), rng.uniform(0, K.LOOP, n), rng.uniform(*size, n), rng.random(n)
        for X, w, r, t in zip(Xs, ws, rs, tones):
            if not (lo - r - 0.05 <= X <= hi + r + 0.05):
                continue
            x, y = to_map(X, w, strip)
            R = r * ppm
            for shift in _loop_copies([x], wpx, R + 3):
                cx = x + shift
                sheet.ellipse(cx - R * 0.25, y, R * 1.05, R * 0.9, "#3e2f52", 0.85)             # its shade, toward us
                sheet.ellipse(cx, y, R * 0.9, R * 0.8, "#66506e" if t < 0.55 else "#7a6478")
                sheet.ellipse(cx + R * 0.55, y, R * 0.28, R * 0.6, "#f6b878" if t < 0.3 else "#c89a86", 0.7)      # lit where the sun is


def litter(sheet, width, seed):
    """What the painting has lying on the shoulders, from straight above, where the painting has it when the camera
    stops: a strip of somebody's tire (13.3 m ahead, 3.82 m left), a green bottle (10.15 m, 3.50 m left), a hubcap (11.9 m,
    3.74 m right). Each lit on its far side, its shade toward us."""
    wof = lambda z: (z + K.STOP_S) % K.LOOP
    # the strip of tire: 74 cm, curved, lying across, its far edge lit
    cx, cy = to_map(-3.82, wof(13.3))
    pts = [(cx + dw * 48, cy + dX * 48) for dX, dw in ((-0.37, 0.0), (-0.15, 0.05), (0.08, 0.02), (0.37, 0.08))]
    from brush import curve
    pts = curve(pts, 5)
    sheet.line([(x - 4, y + 1) for x, y in pts], "#33284a", 0.13 * 48, 0.5)
    sheet.line(pts, "#221a2a", 0.13 * 48)
    for j in range(1, len(pts) - 1, 2):
        sheet.line([(pts[j][0] - 2.5, pts[j][1]), (pts[j][0] + 2.5, pts[j][1])], "#3e3448", 0.9)
    sheet.line([(x + 3.2, y) for x, y in pts[2:]], "#e89c5c", 0.9, 0.85)
    # the bottle: 23 cm long, lying across, green, the sun through it
    cx, cy = to_map(-3.50, wof(10.15))
    ln, wd = 0.23 * 48, 0.062 * 48
    sheet.line([(cx - 3, cy - ln * 0.5 + 1), (cx - 3, cy + ln * 0.5 + 1)], "#33284a", wd * 0.9, 0.55)
    sheet.line([(cx, cy - ln * 0.5), (cx, cy + ln * 0.22)], "#2e6650", wd)
    sheet.line([(cx, cy + ln * 0.22), (cx, cy + ln * 0.5)], "#2e6650", wd * 0.45)
    sheet.line([(cx + wd * 0.35, cy - ln * 0.38), (cx + wd * 0.35, cy + ln * 0.12)], "#b6f0b0", 0.9)
    sheet.line([(cx - wd * 0.1, cy - ln * 0.1), (cx - wd * 0.1, cy + ln * 0.14)], "#5cc08a", 1.0, 0.9)
    # the hubcap: 40 cm across, its rim, its middle, the sun along its far edge
    cx, cy = to_map(3.74, wof(11.9))
    r = 0.20 * 48
    sheet.ellipse(cx - 4, cy + 1.5, r * 1.1, r * 1.05, "#33284a", 0.6)
    sheet.ellipse(cx, cy, r, r, "#8884a2")
    sheet.ellipse(cx, cy, r * 0.62, r * 0.62, "#56506e")
    sheet.ellipse(cx, cy, r * 0.2, r * 0.2, "#a6a2bc")
    sheet.line([(cx + math.sin(a_) * r * 0.97, cy + math.cos(a_) * r * 0.97) for a_ in np.linspace(math.pi * 0.05, math.pi * 0.95, 9)], "#ffdca4", 1.0)


# ---------------------------------------------------------------- PAINT-18B: the brush field, from straight above
CLUMP_FAR_MORE = 0.5                               # (more clumps a square metre beyond 30 m)
CLUMP_DENS = 1.00                                  # clumps a square metre where a drift is thickest (before the drifts thin it)
_CLUMPS = None


def clump_list(seed=1870):
    """Every clump of sagebrush lying flat in the ground, placed in the world once (both sides, 6.3 to 150 m out, along
    the 64 m loop), each strip drawing those it shows. They grow as the painting's bushes do (highway.bushes): in drifts
    with bare ground between (a cell of the drift is about 12 m; a bush is kept with step(0.36, 0.60, drift) * 0.95 +
    0.05), 0.9 to 2.5 m across (a clump is often several bushes grown together); and thinner close to the road, where the upright brush stands (a fifth of it at 6 m, all
    of it from 16 m). -> arrays X, w, D (m), kind (0 sage, 1 rabbitbrush, 2 dry), seed."""
    global _CLUMPS
    if _CLUMPS is not None:
        return _CLUMPS
    rng = np.random.default_rng(seed)
    drift = pnoise((600, 128), (12.0 * 2, 12.0 * 2), seed + 1, 3)      # 2 px a metre, X from -150 to 150 m
    out = []
    for side in (-1, 1):
        n = rng.poisson(K.LOOP * 144.0 * CLUMP_DENS)
        a = 6.3 + rng.random(n) * 144.0
        w = rng.random(n) * K.LOOP
        X = side * a
        d = drift[np.clip(((X + 150.0) * 2).astype(int), 0, 599), (w * 2).astype(int) % 128]
        keep = step(0.36, 0.60, d) * 0.95 + 0.05
        near = 0.2 + 0.8 * step(7.0, 16.0, a)
        D = 0.9 + rng.random(n) ** 1.5 * 1.6                           # (drifts: a clump is often several bushes grown together)
        ok = (rng.random(n) < keep * near) & (a - D / 2 > 6.25)
        kind = np.where(rng.random(n) < 0.16, 1, np.where(rng.random(n) < 0.12, 2, 0))
        out.append((X[ok], w[ok], D[ok], kind[ok], rng.integers(1 << 30, size=n)[ok]))
    # beyond 30 m out, more of them (the painting's field thickens with distance on the screen): a second set, its own seed,
    # each wholly beyond 30 m, so that the near deserts do not change
    for side in (-1, 1):
        n = rng.poisson(K.LOOP * 120.0 * CLUMP_FAR_MORE)
        a = 30.0 + rng.random(n) * 120.0
        w = rng.random(n) * K.LOOP
        X = side * a
        d = drift[np.clip(((X + 150.0) * 2).astype(int), 0, 599), (w * 2).astype(int) % 128]
        keep = step(0.36, 0.60, d) * 0.95 + 0.05
        D = 0.9 + rng.random(n) ** 1.5 * 1.6
        ok = (rng.random(n) < keep) & (a - D * 0.5 * 1.8 > 30.05)
        kind = np.where(rng.random(n) < 0.16, 1, np.where(rng.random(n) < 0.12, 2, 0))
        out.append((X[ok], w[ok], D[ok], kind[ok], rng.integers(1 << 30, size=n)[ok]))
    _CLUMPS = tuple(np.concatenate([o[i] for o in out]) for i in range(5))
    return _CLUMPS


CLUMP_COLORS = {0: ("#241f3a", "#3b4558", "#66787e"), 1: ("#241f3a", "#3d4a4e", "#6c7c62"), 2: ("#3a2a34", "#5a4648", "#8a6a5c")}


def clumps(sheet, strip):
    """Draw the brush field into a strip: each clump a round dark mass of lobes, the silver of its crowns, the gold of the
    sun on its far side (where the sun is: forward, to the right in the strip), and its own small shade toward us."""
    lo, hi, ppm = K.STRIPS[strip]
    _, wpx = K.strip_shape(strip)
    Xs, ws, Ds, kinds, seeds = clump_list()
    sel = (Xs + Ds > lo) & (Xs - Ds < hi)
    order = np.argsort(ws[sel])
    for X, w, D, kind, sd in zip(Xs[sel][order], ws[sel][order], Ds[sel][order], kinds[sel][order], seeds[sel][order]):
        x, y = to_map(X, w, strip)
        R = D * 0.5 * ppm
        dark, mid, lite = CLUMP_COLORS[int(kind)]
        far = float(step(30.0, 40.0, abs(X)))                           # beyond 30 m: drawn out along the road, more gold
        E = 1.0 + 0.8 * far                                              # (seen at a grazing angle a drift keeps its shape)
        pfire = 0.35 + 0.25 * far
        for shift in _loop_copies([x], wpx, R * 2 * E + 4):
            rng = np.random.default_rng(int(sd))                       # (each copy the same clump)
            cx = x + shift
            sheet.ellipse(cx - R * 0.55 * E, y + R * 0.05, R * 1.30 * E, R * 0.95, "#3e2f52", 0.55)  # its shade, toward us
            nl = 3 + int(R / 4)
            for i in range(nl):                                                                   # the lobes
                lx, ly = cx + rng.normal(0, R * 0.28) * E, y + rng.normal(0, R * 0.28)
                r = R * rng.uniform(0.50, 0.72)
                sheet.ellipse(lx, ly, r * E, r * rng.uniform(0.85, 1.05), dark)
            for i in range(2 + int(R * 0.8)):                                                   # the crowns' silver
                a_, rr = rng.uniform(0, 2 * math.pi), R * 0.55 * math.sqrt(rng.random())
                px_, py_ = cx + (math.cos(a_) * rr + R * 0.1) * E, y + math.sin(a_) * rr
                sheet.ellipse(px_, py_, max(0.5, R * 0.14), max(0.5, R * 0.12), mid if rng.random() < 0.6 else lite, 0.85)
            for i in range(3 + int(R * 0.9 * (1 + far))):                                       # the sun on its far side
                t = rng.uniform(-1.35, 1.35)
                rr = R * rng.uniform(0.62, 0.98)
                px_, py_ = cx + math.cos(t) * rr * E, y + math.sin(t) * rr * 0.95
                c = "#ffd98c" if rng.random() < pfire else "#e2924e"
                sheet.ellipse(px_, py_, max(0.55, R * 0.16), max(0.5, R * 0.12), c, 0.9)
            if kind == 1:                                                                         # rabbitbrush in bloom
                for i in range(2 + int(R * 0.6)):
                    a_, rr = rng.uniform(0, 2 * math.pi), R * 0.6 * math.sqrt(rng.random())
                    sheet.ellipse(cx + math.cos(a_) * rr * E, y + math.sin(a_) * rr, max(0.5, R * 0.12), max(0.5, R * 0.12), "#e8c45a", 0.9)


def flaked(col, before, seed):
    """highway.details(): paint flaked off the yellow line lets the road show through (near the middle only)."""
    h, w = col.shape[:2]
    X = K.strip_X("road")[:, None]
    fl = step(0.60, 0.74, pnoise((h, w), (0.28 * 48, 0.10 * 48), seed + 21, 2)) * (np.abs(X) < 0.12)
    col[...] = lerp(col, before, (fl * 0.55)[..., None])


def seam_fade(strip):
    """How much of the brush pass a strip's rows keep: none at a seam with another strip, all from 0.3 m in."""
    X = K.strip_X(strip)
    lo, hi, ppm = K.STRIPS[strip]
    d = np.full(X.shape, 99.0, F32)
    for seam in (-30.0, -6.0, 6.0, 30.0):                 # (PAINT-18B: and at 30 m, the far strips' seam)
        if lo - 0.01 <= seam <= hi + 0.01:
            d = np.minimum(d, np.abs(X - seam))
    return np.clip(d / 0.3, 0, 1).astype(F32)[:, None, None]


def brushed(pic, strip, seed, fast):
    if fast:
        return pic
    lo, hi, ppm = K.STRIPS[strip]
    sizes = (6, 3, 2) if ppm >= 40 else (4, 2, 1)
    out = brush_wrapped(pic, sizes=sizes, seed=seed, density=1.5, jitter=0.03, keep=0.40)
    return lerp(pic, out, seam_fade(strip)).astype(F32)


# ---------------------------------------------------------------- the three strips
def paint_road(T, marks, seed=1801, fast=False):
    h, w = K.strip_shape("road")
    X = K.strip_X("road")
    col, g = plain(T, "road")
    sh, sand = shoulders(col, g, X)
    road, tar = asphalt(col, g, sand, seed)
    col = brushed(col, "road", seed + 5, fast)
    under = col.copy()
    road_edges(col, road, seed)
    sheet = Paper((h, w), ss=3)
    painting_marks([m for m in marks if m["what"] in ("edge-line", "dash")], sheet, w, seed)
    sheet.onto(col)
    flaked(col, under, seed)
    sheet = Paper((h, w), ss=3)
    painting_marks([m for m in marks if m["what"] not in ("edge-line", "dash")], sheet, w, seed)
    tar_snakes(sheet, w, seed + 30)
    sheet.onto(col)
    sheet = Paper((h, w), ss=3)
    pebbles(sheet, "road")
    litter(sheet, w, seed + 50)
    sheet.onto(col)
    return grade(np.clip(col, 0, 1)), dict(road=road, shoulder=sh)


def paint_desert(T, strip, seed, fast=False, TF=None):
    """A near desert strip (6 to 30 m out). PAINT-18B: the brush field lies in it (clumps), and it no longer calms at
    30 m: the far strips carry the plain on (its last 3 m mix into their textures)."""
    X = K.strip_X(strip)
    col, g = plain(T, strip, TF)
    col = brushed(col, strip, seed + 5, fast)
    h, w = col.shape[:2]
    sheet = Paper((h, w), ss=3)
    pebbles(sheet, strip)
    sheet.onto(col)
    sheet = Paper((h, w), ss=3)
    clumps(sheet, strip)
    sheet.onto(col)
    return grade(np.clip(col, 0, 1))


def paint_far(TF, strip, seed, fast=False):
    """PAINT-18B: a far strip (30 to 150 m out, 8 px a metre): the plain from the far textures and the brush field. Its
    last 2 m out calm down to its own colour on average: the engine carries a strip's outer rows on beyond 150 m."""
    X = K.strip_X(strip)
    col, g = plain(None, strip, TF)
    if not fast:
        out = brush_wrapped(col, sizes=(3, 2, 1), seed=seed + 5, density=1.5, jitter=0.03, keep=0.40)
        k = np.clip((np.abs(X) - 30.0) / 0.6, 0, 1).astype(F32)[:, None, None]       # (none at the seam with the near desert)
        col = lerp(col, out, k).astype(F32)
    h, w = col.shape[:2]
    sheet = Paper((h, w), ss=3)
    clumps(sheet, strip)
    sheet.onto(col)
    side = np.abs(X)[:, None]
    mean = col.reshape(-1, 3).mean(0)
    calm = np.clip((side - 146.0) / 4.0, 0, 1) ** 1.2 * 0.95
    col = lerp(col, lerp(blur(col, 1.0), mean[None, None, :], 0.8), calm[..., None])
    return grade(np.clip(col, 0, 1))

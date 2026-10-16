"""The ground beside the road, seen from straight above (nevada_limo_drive.py, DRIVE-16P): drive-ground-l.png and
drive-ground-r.png, 1024 x 512 at 16 pixels a metre.

A map, not a view: no perspective, no horizon, nothing standing up (what stands up is on the things' sheet). Its columns
run along the road, forward to the right, 64 m of it, and repeat end to end; its rows run outward from the road, from
6 m out (the top row) to 38 m (the bottom). The engine reads it under every pixel of the panes below the horizon.

LEFT. From the top row, the outer edge of the oncoming lane: its asphalt, grey and pale with the sun, the white edge line
at 8.0 m (15 cm), a hand's width more of asphalt crumbling into the gravel shoulder, the gravel to 9.6 m, then the
desert. RIGHT. The desert from the top row, a little of the shoulder's gravel thrown up near the road; the fence's line
at 9.5 m, marked only by the dry grass and the litter that collect along it and by the path the cattle keep beside it
(its posts are the engine's, from the sheet, and are not painted here); beyond, a ranch's two-track running along.
Both: warm sand, blotched and drifted, patches of darker desert pavement, stones, a dry rut; sagebrush (grey-green and
silver), creosote (dark and open) and rabbitbrush (in flower, yellow, for October) as round masses with their own short
shadows. The sun is low on the car's right and a little behind it, so here the shadows fall away from the road on the
left (down the picture) and toward it on the right (up the picture), and a little forward; each clump is lit on its
other side.

The last rows calm down to the plain's own colour, for the engine carries the ground on past 38 m with the colour of
the last rows: nothing there may make a streak."""

import math

import numpy as np

from brush import F32, blur, lerp, over, ramp, rgb, tint
from nevada_limo_drive_kit import (GROUND_FROM, GROUND_H, GROUND_PPM, GROUND_W, LEFT, RIGHT, SHADOW_FWD, SHADOW_LEFT,
                                   brush_wrapped, pblur, pnoise, pwave, smoke, wrap)
from nevada_roadside_kit import Paper
from solid import mix

PPM = GROUND_PPM


def row_of(X):
    """The picture row of a distance out from the line of travel (m)."""
    return (X - GROUND_FROM) * PPM


def shadow_px(side, height):
    """Where the shadow of a point `height` m up falls, in picture pixels from its foot: (along, out)."""
    return SHADOW_FWD * height * PPM, (SHADOW_LEFT if side == "L" else -SHADOW_LEFT) * height * PPM


def sun_px(side):
    """The direction toward the sun across the picture (unit, picture x and y)."""
    a, o = shadow_px(side, 1.0)
    n = math.hypot(a, o)
    return -a / n, -o / n


# ---------------------------------------------------------------- the sand
def sand(shape, seed):
    """Warm sand, blotched, drifted, with patches of darker desert pavement. Its big patches are strongest near the road
    and fade out with distance: the far rows are only ever seen squeezed toward the horizon and averaged, where big
    patches along the road would make stripes."""
    h, w = shape
    y = np.arange(h, dtype=F32)[:, None]
    near = np.clip(1.0 - (y - row_of(14.0)) / (row_of(30.0) - row_of(14.0)), 0.3, 1.0)
    blot = (pnoise(shape, (300, 180), seed, 4) - 0.5) * near
    mid = (pnoise(shape, (90, 60), seed + 1, 4) - 0.5) * (0.4 + 0.6 * near)
    fine = pnoise(shape, (14, 10), seed + 2, 3) - 0.5
    col = ramp(np.clip(0.52 + blot * 0.8 + mid * 0.45, 0, 1), [(0.0, "#c48456"), (0.35, "#ce966a"), (0.6, "#d8a87a"), (1.0, "#e4be94")])
    col = col * (1 + fine[..., None] * 0.07)
    k = (pnoise(shape, (420, 260), seed + 3, 3) - 0.5) * 0.05 * near          # warmer and cooler drifts
    col[..., 0] += k
    col[..., 2] -= k * 0.8
    d = pnoise(shape, (160, 40), seed + 4, 4)
    over(col, "#ecd2ac", (np.clip((d - 0.62) * 3.0, 0, 1) * 0.5 * near).astype(F32))
    pav = pnoise(shape, (120, 90), seed + 5, 4)
    pave = np.clip((pav - 0.66) * 4.0, 0, 1) * near
    tint(col, "#9a8a86", (pave * 0.32).astype(F32))
    return np.clip(col, 0, 1).astype(F32), pave


# ---------------------------------------------------------------- what grows: where, and how big
def clumps(side, seed, zones):
    """The bushes and tufts of one side: [(x px, y px, radius m, height m, kind)], kind one of sage, creosote, rabbit,
    tuft. `zones`: [(from m, to m, bushes a square metre, tufts a square metre)]."""
    rng = np.random.default_rng(seed)
    out = []
    length = GROUND_W / PPM
    for x0, x1, nb, nt in zones:
        area = length * (x1 - x0)
        for k in range(rng.poisson(area * nb)):
            X = rng.uniform(x0, x1)
            kind = rng.choice(["sage", "creosote", "rabbit"], p=[0.62, 0.22, 0.16])
            r = {"sage": rng.uniform(0.26, 0.62), "creosote": rng.uniform(0.4, 0.85), "rabbit": rng.uniform(0.28, 0.55)}[kind]
            hgt = {"sage": r * rng.uniform(1.1, 1.5), "creosote": r * rng.uniform(1.2, 1.6), "rabbit": r * rng.uniform(1.2, 1.6)}[kind]
            out.append((rng.uniform(0, GROUND_W), row_of(X), r, hgt, kind))
        for k in range(rng.poisson(area * nt)):
            X = rng.uniform(x0, x1)
            r = rng.uniform(0.08, 0.22)
            out.append((rng.uniform(0, GROUND_W), row_of(X), r, r * 1.4, "tuft"))
    # keep them apart a little: a bush does not grow inside another
    out.sort(key=lambda c: -c[2])
    kept = []
    grid = {}
    for c in out:
        gx, gy = int(c[0] // 24), int(c[1] // 24)
        ok = True
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                for o in grid.get(((gx + i) % (GROUND_W // 24 + 1), gy + j), ()):
                    dx = (c[0] - o[0] + GROUND_W / 2) % GROUND_W - GROUND_W / 2
                    if math.hypot(dx, c[1] - o[1]) < (c[2] + o[2]) * PPM * 0.8:
                        ok = False
        if ok:
            kept.append(c)
            grid.setdefault((gx % (GROUND_W // 24 + 1), gy), []).append(c)
    return kept


def shadows(shape, side, items):
    """The clumps' shadows on the ground, as one soft mask: each bush's round mass laid along the sun's rays."""
    sh = Paper(shape, ss=2)
    for x, y, r, hgt, kind in items:
        ax, ay = shadow_px(side, hgt * 0.85)
        R = r * PPM * {"tuft": 0.7, "creosote": 0.62}.get(kind, 0.92)        # an open bush throws a thinner shadow
        for xx in wrap(x, shape[1], R * 4 + 40):
            for t in np.linspace(0, 1, 7):
                sh.ellipse(xx + ax * t, y + ay * t, R * (1 - 0.28 * t), R * (1 - 0.28 * t), "#000000")
    return blur(sh.done()[1], 0.9)


def bush(sheet, x, y, r, kind, seed, side):
    """One clump seen from above, its middle at (x, y), r m across its half: a dark mass, its sprays or twigs, lit on
    the side toward the sun."""
    rng = np.random.default_rng(seed)
    R = r * PPM
    sx, sy = sun_px(side)
    tones = {"sage": ("#4e5648", "#6e7a62", "#9ca88a", "#ccd2b2"), "creosote": ("#3e4830", "#5a683a", "#82904c", "#b0b86c"),
             "rabbit": ("#5e6846", "#7c8a5e", "#a8b07c", "#cccc94"), "tuft": ("#8a7a56", "#b09c6c", "#d4c08c", "#ece0b4")}[kind]
    if kind == "tuft":
        for k in range(int(5 + R)):
            a = rng.uniform(0, 2 * math.pi)
            l = R * rng.uniform(0.6, 1.2)
            sheet.line([(x, y), (x + math.cos(a) * l, y + math.sin(a) * l)], mix(tones[1], tones[3], rng.random()), 0.8)
        return
    if kind == "creosote":                                                 # open: twigs from the middle, leaves in knots
        for k in range(int(10 + R * 0.8)):
            a = rng.uniform(0, 2 * math.pi)
            d = R * rng.uniform(0.35, 1.0)
            px, py = x + math.cos(a) * d, y + math.sin(a) * d
            lit = 0.5 + 0.5 * (math.cos(a) * sx + math.sin(a) * sy) * min(1.0, d / R)
            sheet.line([(x, y), (px, py)], "#5a4a3a", 0.6)
            sheet.ellipse(px, py, rng.uniform(0.9, 1.8), rng.uniform(0.9, 1.6), mix(tones[0], tones[2], lit))
            if lit > 0.6:
                sheet.ellipse(px + sx * 0.6, py + sy * 0.6, 0.8, 0.8, tones[3])
        return
    # the mass, a little off toward the shade, lobed
    for k in range(int(5 + R * 0.5)):
        a = rng.uniform(0, 2 * math.pi)
        d = rng.uniform(0, R * 0.35)
        rr = R * rng.uniform(0.5, 0.72)
        sheet.ellipse(x + math.cos(a) * d - sx * R * 0.12, y + math.sin(a) * d - sy * R * 0.12, rr, rr, tones[0])
    # sprays: many small marks, the lit ones toward the sun last
    sprays = []
    for k in range(int(14 + R * R * 0.9)):
        a = rng.uniform(0, 2 * math.pi)
        d = R * rng.random() ** 0.55 * 0.95
        px, py = x + math.cos(a) * d, y + math.sin(a) * d
        lit = 0.5 + 0.5 * (math.cos(a) * sx + math.sin(a) * sy) * (d / R) + rng.normal(0, 0.15)
        sprays.append((lit, px, py))
    for lit, px, py in sorted(sprays):
        t = min(1.0, max(0.0, lit))
        c = mix(tones[0], tones[1], t * 2) if t < 0.5 else (mix(tones[1], tones[2], (t - 0.5) * 3.3) if t < 0.8 else mix(tones[2], tones[3], (t - 0.8) * 5))
        rr = rng.uniform(0.7, 1.5)
        sheet.ellipse(px, py, rr, rr * rng.uniform(0.7, 1.0), c)
    if kind == "rabbit":                                                   # in flower: yellow on top, most where the sun is
        for k in range(int(6 + R * 1.2)):
            a = rng.uniform(0, 2 * math.pi)
            d = R * rng.random() ** 0.7 * 0.8
            lit = 0.5 + 0.5 * (math.cos(a) * sx + math.sin(a) * sy)
            sheet.ellipse(x + math.cos(a) * d, y + math.sin(a) * d, rng.uniform(0.8, 1.6), rng.uniform(0.8, 1.4), mix("#d8a830", "#f8e070", lit))


def stones(sheet, shape, side, seed, count, rows=None, size=(0.6, 2.4), tones=("#f4e6cc", "#d6c2a4", "#9c8678", "#6a5a56")):
    """Small stones lying about, each lit toward the sun with a dark edge away from it."""
    h, w = shape
    rng = np.random.default_rng(seed)
    sx, sy = sun_px(side)
    y0, y1 = rows if rows else (0, h)
    for k in range(count):
        x, y = rng.uniform(0, w), y0 + (y1 - y0) * rng.random() ** 1.0
        r = rng.uniform(*size)
        for xx in wrap(x, w, 8):
            sheet.ellipse(xx - sx * r * 0.45, y - sy * r * 0.45, r * 1.15, r * 0.95, tones[3])
            sheet.ellipse(xx, y, r, r * 0.85, tones[2] if rng.random() < 0.5 else mix(tones[1], tones[2], 0.5))
            sheet.ellipse(xx + sx * r * 0.3, y + sy * r * 0.3, r * 0.55, r * 0.45, tones[0] if rng.random() < 0.6 else tones[1])


def rut(shape, side, centre_m, wander_m, seed, width_m=0.34, cycles=(1, 3)):
    """A rut along the road, wandering: (mask of its floor, mask of its sunlit wall, mask of its shaded wall)."""
    h, w = shape
    wave = pwave(w, cycles[0], seed * 0.37) * 0.65 + pwave(w, cycles[1], seed * 1.3) * 0.35
    cy = row_of(centre_m) + wave * wander_m * PPM
    y = np.arange(h, dtype=F32)[:, None]
    d = y - cy[None, :]
    half = width_m * PPM / 2
    floor_ = np.clip(half - np.abs(d) + 0.5, 0, 1)
    sx, sy = sun_px(side)
    # the wall on the side away from the sun's direction across is lit (it faces the sun); the other is in shade
    far_wall = np.clip(1 - np.abs(d - half) / 1.6, 0, 1)
    near_wall = np.clip(1 - np.abs(d + half) / 1.6, 0, 1)
    lit, shade = (far_wall, near_wall) if sy < 0 else (near_wall, far_wall)
    return floor_.astype(F32), lit.astype(F32), shade.astype(F32)


# ---------------------------------------------------------------- the left: the oncoming lane's edge, the shoulder, the desert
def ground_left(fast=False, seed=501):
    h, w = GROUND_H, GROUND_W
    shape = (h, w)
    pic, pave = sand(shape, seed)
    y = np.arange(h, dtype=F32)[:, None]
    x = np.arange(w, dtype=F32)[None, :]
    line_in, line_out = row_of(LEFT["edge"] - LEFT["line_w"] / 2), row_of(LEFT["edge"] + LEFT["line_w"] / 2)
    # the asphalt's own edge, a hand beyond the line, crumbling
    edge = row_of(LEFT["edge"] + 0.32) + (pnoise((1, w), 9, seed + 1, 3)[0] - 0.5) * 3.2 + (pnoise((1, w), 40, seed + 2, 3)[0] - 0.5) * 2.2
    asph = np.clip(edge[None, :] - y + 0.5, 0, 1)
    # the gravel shoulder to 9.6 m, its outer edge ragged, the gravel thinning out into the sand
    g_edge = row_of(LEFT["gravel"]) + (pnoise((1, w), 30, seed + 3, 4)[0] - 0.5) * 9.0
    grav = np.clip((g_edge[None, :] - y) / 5.0 + 0.5, 0, 1) * (1 - asph)
    gcol = ramp(pnoise(shape, (40, 12), seed + 4, 3), [(0.0, "#94887c"), (0.5, "#a89a8a"), (1.0, "#c0ae98")])
    gcol = lerp(gcol, pic, (pnoise(shape, (70, 18), seed + 5, 3) * 0.35)[..., None])          # sand washed in
    pic = lerp(pic, gcol, grav[..., None])
    acol = ramp(pnoise(shape, (200, 30), seed + 6, 3), [(0.0, "#6e687c"), (0.5, "#7a7488"), (1.0, "#878196")])
    wheel = np.exp(-((y - row_of(7.05)) / 7.0) ** 2) * 0.06                  # the outer wheel path, polished a little paler
    acol = acol * (1 + wheel[..., None])
    pic = lerp(pic, acol, asph[..., None])
    # what grows: little near the shoulder (graded), then the desert
    items = clumps("L", seed + 7, [(10.0, 12.5, 0.03, 0.30), (12.5, 38.5, 0.10, 0.22)])
    sm = shadows(shape, "L", items)
    tint(pic, "#6664ac", (sm * 0.40 * (1 - asph)).astype(F32))
    over(pic, "#5c5c9c", (sm * 0.08 * (1 - asph)).astype(F32))
    # a dry rut, wandering along out in the desert
    fl, lw, sw = rut(shape, "L", 15.2, 0.9, seed + 8)
    tint(pic, "#c4a088", fl * 0.30)
    over(pic, "#f2dcbc", lw * 0.45)
    tint(pic, "#8a6c66", sw * 0.45)
    if not fast:
        pic = brush_wrapped(pic, sizes=(6, 3, 2), seed=seed + 9, density=1.5, jitter=0.03, keep=0.42)
    # crisp: the asphalt's grain and its cracks, the white line, the broken edge, the gravel's stones, the bushes, stones
    sheet = Paper(shape, ss=3)
    rng = np.random.default_rng(seed + 10)
    for k in range(int(w * row_of(8.3) * 0.10)):                            # the aggregate in the asphalt, catching the sun
        xx, yy = rng.uniform(0, w), rng.uniform(0, row_of(8.3))
        sheet.ellipse(xx, yy, 0.55, 0.5, "#b2acbc" if rng.random() < 0.6 else "#56526a")
    for k in range(5):                                                       # cracks sealed with tar, across the lane
        cx = rng.uniform(0, w)
        pts = [(cx + rng.normal(0, 2.0), 0.0)]
        while pts[-1][1] < line_in - 1:
            pts.append((pts[-1][0] + rng.normal(0, 1.4), pts[-1][1] + rng.uniform(3, 6)))
        for d in (-w, 0, w):
            sheet.line([(px + d, py) for px, py in pts], "#3a3644", 1.3)
            sheet.line([(px + d + 0.5, py) for px, py in pts], "#9a96aa", 0.5)
    lc = pwave(w, 2, 1.1) * 1.2 + pwave(w, 5, 0.3) * 0.5                     # a long crack along, near the line
    sheet.line([(xx, row_of(7.62) + lc[int(xx) % w]) for xx in range(0, w + 1, 4)], "#4a4656", 0.8)
    # the line: straight, worn a little, its edges true
    wear = pnoise((1, w), 24, seed + 11, 3)[0]
    for xx in range(w):
        c = mix("#f4f0e6", "#c8c4c0", float(np.clip((wear[xx] - 0.6) * 2.2, 0, 0.7)))
        sheet.poly([(xx, line_in), (xx + 1, line_in), (xx + 1, line_out), (xx, line_out)], c)
    for k in range(60):                                                      # chips out of the paint
        xx = rng.uniform(0, w)
        sheet.ellipse(xx, rng.uniform(line_in + 0.4, line_out - 0.4), rng.uniform(0.5, 1.3), 0.5, "#8e889a")
    for k in range(220):                                                     # broken bits of the asphalt's edge in the gravel
        xx = rng.uniform(0, w)
        yy = edge[int(xx) % w] + rng.uniform(0.5, 7)
        r = rng.uniform(0.6, 1.8)
        for x2 in wrap(xx, w, 4):
            sheet.poly([(x2 - r, yy), (x2 - r * 0.2, yy - r * 0.8), (x2 + r, yy - r * 0.2), (x2 + r * 0.4, yy + r * 0.7)], "#6e6878")
    stones(sheet, shape, "L", seed + 12, 2000, rows=(row_of(8.2), row_of(9.9)), size=(0.5, 1.4), tones=("#e2d8c8", "#c0b2a0", "#847668", "#5a4e4a"))
    stones(sheet, shape, "L", seed + 13, 380, rows=(row_of(9.6), row_of(11.0)), size=(0.5, 1.3), tones=("#ece0cc", "#ccb8a0", "#8e7c70", "#64564e"))
    stones(sheet, shape, "L", seed + 14, 420, rows=(row_of(10.0), h), size=(0.5, 2.0), tones=("#f2dcc0", "#d8b894", "#a0806c", "#74605a"))
    for i, (bx, by, r, hgt, kind) in enumerate(sorted(items, key=lambda c: c[1])):
        for xx in wrap(bx, w, r * PPM + 4):
            bush(sheet, xx, by, r, kind, seed + 100 + i, "L")
    c, a = sheet.done()
    over(pic, c, a)
    return finish_ground(pic, seed)


# ---------------------------------------------------------------- the right: the desert, the fence's line, the two-track
def ground_right(fast=False, seed=601):
    h, w = GROUND_H, GROUND_W
    shape = (h, w)
    pic, pave = sand(shape, seed)
    y = np.arange(h, dtype=F32)[:, None]
    # near the road: disturbed ground, paler, with the shoulder's gravel thrown up
    near = np.clip(1 - (y - 0) / row_of(8.0), 0, 1)
    over(pic, "#dcc0a0", (near * 0.30 * (0.6 + 0.4 * pnoise(shape, (50, 20), seed + 1, 3))).astype(F32))
    # the path the cattle keep beside the fence, a little out from it, and the fence's line of dry litter
    pw = pwave(w, 1, seed * 0.1) * 0.4 + pwave(w, 4, seed * 0.7) * 0.2
    path_y = row_of(RIGHT["fence"] + 0.75) + pw * PPM
    dpath = np.abs(y - path_y[None, :])
    path = np.clip((0.32 * PPM - dpath) / 3.0, 0, 1) * (0.5 + 0.5 * pnoise((1, w), 30, seed + 2, 3)[0][None, :])
    over(pic, "#e8cca8", (path * 0.55).astype(F32))
    # what grows: little near the road, more beyond the fence (grazed but standing)
    items = clumps("R", seed + 3, [(6.0, 9.2, 0.025, 0.30), (9.2, 10.0, 0.0, 1.4), (10.4, 38.5, 0.11, 0.20)])
    sm = shadows(shape, "R", items)
    tint(pic, "#6664ac", (sm * 0.40).astype(F32))
    over(pic, "#5c5c9c", (sm * 0.08).astype(F32))
    # the two-track: two ruts 1.6 m apart, wandering together
    tr = []
    for k, off in enumerate((0.0, 1.6)):
        fl, lw, sw = rut(shape, "R", 19.4 + off, 1.4, seed + 4, width_m=0.38, cycles=(1, 2))
        tr.append(fl)
        over(pic, "#ead2b2", fl * 0.55)
        over(pic, "#f6e2c4", lw * 0.4)
        tint(pic, "#8a6c66", sw * 0.42)
    if not fast:
        pic = brush_wrapped(pic, sizes=(6, 3, 2), seed=seed + 5, density=1.5, jitter=0.03, keep=0.42)
    sheet = Paper(shape, ss=3)
    stones(sheet, shape, "R", seed + 6, 1100, rows=(0, row_of(7.4)), size=(0.5, 1.5), tones=("#e6dccc", "#c4b6a2", "#8a7c70", "#5e524e"))
    stones(sheet, shape, "R", seed + 7, 460, rows=(row_of(7.4), h), size=(0.5, 2.0), tones=("#f2dcc0", "#d8b894", "#a0806c", "#74605a"))
    rng = np.random.default_rng(seed + 8)
    for k in range(40):                                                      # litter blown against the fence: dry stems
        xx = rng.uniform(0, w)
        yy = row_of(RIGHT["fence"]) + rng.normal(0, 2.0)
        for x2 in wrap(xx, w, 8):
            for j in range(4):
                a = rng.uniform(-0.6, 0.6)
                l = rng.uniform(2, 6)
                sheet.line([(x2, yy), (x2 + math.cos(a) * l, yy + math.sin(a) * l)], "#c4ac80", 0.6)
    for i, (bx, by, r, hgt, kind) in enumerate(sorted(items, key=lambda c: c[1])):
        for xx in wrap(bx, w, r * PPM + 4):
            bush(sheet, xx, by, r, kind, seed + 100 + i, "R")
    c, a = sheet.done()
    over(pic, c, a)
    return finish_ground(pic, seed)


def finish_ground(pic, seed):
    """The last rows calmed to the plain's own colour (the engine carries them on past 38 m), then the smoked glass."""
    h, w, _ = pic.shape
    y = np.arange(h, dtype=F32)[:, None, None]
    plain = pblur(pic, 18.0)
    plain = np.broadcast_to(plain[-80:].mean(axis=(0, 1))[None, None, :], pic.shape)
    calm = np.clip((y - (h - 110)) / 86.0, 0, 1) ** 1.2 * 0.97
    pic = lerp(pic, lerp(pblur(pic, 1.5), plain, 0.75), calm)
    return smoke(np.clip(pic, 0, 1))

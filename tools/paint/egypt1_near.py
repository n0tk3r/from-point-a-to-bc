"""Where the wagon came down: the near plane (round twenty-three: DEPTH.md), what stands by the lens.

We stand on the high bank, under a young date palm: the next one of the row that runs down the bank toward the
pyramid. Everything here is nearer than the sand at the picture's bottom edge (8.5 m), so it is larger than life,
through the scene's own camera (egypt1_kit): the palm's trunk is 4.2 m from the lens, 1.9 px to a centimetre (its
39 cm are 74 px, and a leaflet of 45 cm is 85); the lip of the bank and its halfa grass are 6 to 7 m off, about 1.2 px
to a centimetre (a tussock 75 cm high is ninety pixels). The sun is on the left and beyond, so all of it is seen against the light: deep,
warm darks, lit along the edges that face the sun, and through the leaves that hang between us and it.

    trunk()     near.png          the palm's trunk, leaning with the river wind across the top left corner and out
                                  through the left edge: old leaf bases, a sunlit strip up its left side
    crest()     near.png          the lip of the bank along the bottom, left and middle: its slip face toward us in
                                  shade, its edge in the sun, two tussocks of halfa grass and wisps of it between,
                                  stones cut by the frame. It dips where Dad first stands and before the rock people
                                  walk round, and the right is bare: the luggage pops out and lies there
    fronds()    near-fronds.png   the palm's fronds across the top, and one frond end of its neighbour's in the top
                                  right corner (a file of their own: they hang, so they can stir)
    papyrus()   front.png         the papyrus at the bottom left, as it always was, a little thinner over the water
                                  (seven tenths of the river stay in sight: depth_check.py allows no less than 65 in
                                  a hundred), and reed blades and two great umbels close to the lens, low over the
                                  bank's sand

Nothing here is a thing a hand would pick up. Each returns (colour, mask) at the stage's size."""

import math

import numpy as np

from brush import F32, Sheet, curve, grid, lerp, mask_poly, noise, over, rgb, step
import flora
import land

W, H = 800, 600
SHAPE = (H, W)

# ---------------------------------------------------------------- the palm's trunk
TRUNK_TOP_X = 66.0                                           # where its axis crosses the stage's top edge
TRUNK_LEAN = 0.232                                           # it goes this many pixels left for each pixel down (13 degrees)
TRUNK_R = 37.0                                               # half its thickness: 39 cm at 4.2 m


def trunk_axis(y):
    """The trunk's middle line: the x of it at the row y. A slight bow: nothing grown is ruled."""
    return TRUNK_TOP_X - TRUNK_LEAN * y + 3.5 * np.sin(np.clip(y, -40, 470) / 470.0 * math.pi)


def trunk(seed=41):
    """The date palm's trunk. A cylinder of old leaf bases: each a blunt wedge pointing up, lapping the one above, in
    spirals; no two alike, some broken off. Lit from the left and beyond: the strip toward the sun is in light, the
    middle is the darkest thing in the picture, and the right side takes a little warm light off the sand."""
    rng = np.random.default_rng(seed)
    x, y = grid(SHAPE)
    n = np.array([1.0, TRUNK_LEAN]) / math.hypot(1.0, TRUNK_LEAN)              # across the trunk, to the right
    up = np.array([TRUNK_LEAN, -1.0]) / math.hypot(1.0, TRUNK_LEAN)             # along it, toward the crown
    dark, bounce, sunlit = rgb("#21150f"), rgb("#4a2d1b"), rgb("#cf9e60")
    cap_cool, cap_warm, cap_sun = rgb("#3e3338"), rgb("#74492a"), rgb("#f4d596")
    s = Sheet(SHAPE)
    # the body under the leaf bases (it shows only in the chinks)
    ys = np.arange(-30, 500, 6.0)
    left = [(trunk_axis(v) - (TRUNK_R - 4) * n[0], v - (TRUNK_R - 4) * n[1]) for v in ys]
    right = [(trunk_axis(v) + (TRUNK_R - 4) * n[0], v + (TRUNK_R - 4) * n[1]) for v in ys]
    s.poly(left + right[::-1], "#130c0b")
    row, i = -44.0, 0
    stubs = []
    while row < 520:
        for j in range(8):
            th = -118.0 + j * 33.0 + (i % 2) * 16.5 + rng.normal(0, 4.5)
            if abs(th) > 102 or rng.random() < 0.05:           # (now and then one has rotted away)
                continue
            stubs.append((row + rng.normal(0, 2.2), th, rng.random(), rng.random(), rng.random()))
        row += 16.0 + rng.normal(0, 0.8)
        i += 1
    for (v, th, r1, r2, r3) in stubs:                         # from the top down: each laps the one above it
        st, ct = math.sin(math.radians(th)), max(0.24, math.cos(math.radians(th)))
        c = np.array([trunk_axis(v), v]) + n * st * (TRUNK_R - 4.0)
        w = (11.0 * ct + 2.0) * (0.86 + 0.3 * r3)
        h = 25.0 * (0.82 + 0.36 * r1)
        out = np.sign(st) * 8.5 * max(0.0, (abs(st) - 0.55) / 0.45) * (0.6 + 0.8 * r2)     # at the outline the tips stand out from the trunk
        skew = (r3 - 0.5) * 0.3 * w
        at = lambda a, b, lean=0.0: tuple(c + n * (a + lean) + up * b)
        sun = float(step(-28.0, -54.0, th))
        bnc = float(step(18.0, 86.0, th))
        tone = lerp(lerp(dark, bounce, bnc), sunlit, sun) * (0.78 + 0.40 * r2)
        cap = lerp(lerp(lerp(tone, cap_cool, 0.34), cap_warm, bnc * 0.5), cap_sun, sun) * (0.9 + 0.2 * r1)
        tipw = 0.34 + 0.2 * r1
        body = [at(-w, -0.46 * h), at(-0.96 * w, 0.14 * h, out * 0.45), at(-tipw * w + skew, 0.56 * h, out), at(tipw * w + skew, 0.56 * h, out), at(0.96 * w, 0.14 * h, out * 0.45), at(w, -0.46 * h)]
        s.poly([at(-w - 1.0, -0.46 * h), at(-0.96 * w - 1.0, 0.16 * h, out * 0.45), at(-tipw * w + skew, 0.64 * h, out), at(tipw * w + skew, 0.64 * h, out), at(0.96 * w + 1.0, 0.16 * h, out * 0.45), at(w + 1.0, -0.46 * h)], "#120b0a")
        s.poly(body, np.clip(tone, 0, 1))
        s.poly([at(-0.92 * w, 0.16 * h, out * 0.45), at(-tipw * w + skew, 0.56 * h, out), at(tipw * w + skew, 0.56 * h, out), at(0.92 * w, 0.16 * h, out * 0.45), at(0.26 * w + skew, 0.33 * h, out * 0.7), at(-0.26 * w + skew, 0.33 * h, out * 0.7)], np.clip(cap, 0, 1))
        if r2 < 0.45:                                          # a split down the old base
            s.line([at((r1 - 0.5) * w, 0.24 * h, out * 0.6), at((r1 - 0.5) * w * 0.5, -0.3 * h)], np.clip(tone * 0.55, 0, 1), 0.9)
    # here and there the stump of a frond cut long ago still stands out from the trunk: its outline is never a ruled edge
    for (v, ln, wd) in ((168, 17, 7.0), (224, 12, 6.0), (281, 19, 7.5), (349, 13, 6.5), (402, 16, 7.0)):
        base = np.array([trunk_axis(v), v]) + n * (TRUNK_R - 3.0)
        d = n * 0.62 + up * 0.78                               # out and up
        d = d / math.hypot(d[0], d[1])
        side = np.array([-d[1], d[0]])
        tip = base + d * ln
        s.poly([tuple(base - side * wd * 0.5 - d * 3), tuple(tip - side * wd * 0.32), tuple(tip + side * wd * 0.32), tuple(base + side * wd * 0.5 - d * 3)], "#2a1a13")
        s.poly([tuple(tip - side * wd * 0.32), tuple(tip + side * wd * 0.32), tuple(tip + side * wd * 0.2 - d * 2.5), tuple(tip - side * wd * 0.2 - d * 2.5)], "#7a4e2c")   # its cut end, in the sand's light
        s.line([tuple(base - side * wd * 0.5 - d * 3), tuple(tip - side * wd * 0.32)], "#553420", 0.9)
    color, alpha = s.done()
    # ---- the fibre between and over them: fine streaks along the trunk, and the round of the trunk said once more
    u = (x - trunk_axis(y)) / TRUNK_R
    streak = noise(SHAPE, (4, 26), seed + 1, 3) - 0.5
    color = color * (1 + streak[..., None] * 0.34)
    blotch = noise(SHAPE, (38, 70), seed + 2, 3) - 0.5
    color = color * (1 + blotch[..., None] * 0.30)
    core = np.clip(1 - np.abs(u + 0.10) / 0.62, 0, 1) * 0.34                    # the darkest of it runs just left of the middle
    color = color * (1 - core[..., None])
    warm = step(0.45, 1.0, u) * 0.10                                           # the sand's light on the right flank
    color = color + warm[..., None] * rgb("#b0662c") * 0.5
    fibres = Sheet(SHAPE)
    for k in range(190):                                      # loose threads of the old sheaths, hanging
        v = rng.uniform(-10, 470)
        th = rng.uniform(-84, 88)
        px = trunk_axis(v) + math.sin(math.radians(th)) * TRUNK_R * 1.0
        ln = rng.uniform(7, 22)
        lit = th < -42
        fibres.line([(px, v), (px + rng.normal(0, 1.5) - TRUNK_LEAN * ln * 0.6, v + ln)], "#e0b676" if lit else ("#3b2616" if th < 35 else "#6e4526"), 0.9)
    fc, fa = fibres.done()
    over(color, fc, fa * 0.85)
    alpha = np.maximum(alpha, fa)
    # a chink a pixel or two wide between two leaf bases would let a spark of sky through the trunk: stop those up
    solid = alpha > 0.5
    for gap in (1, 2, 3):
        for axis in (1, 0):
            before = np.roll(solid, 1, axis=axis)
            after = np.zeros_like(solid)
            for g in range(1, gap + 1):
                after |= np.roll(solid, -g, axis=axis)
            chink = ~solid & before & after
            for g in range(1, gap):                             # (and the rest of a chink that is two or three wide)
                chink |= ~solid & np.roll(chink, g, axis=axis) & after
            color[chink] = rgb("#130c0b")
            solid |= chink
    alpha = np.maximum(alpha, solid.astype(F32))
    return np.clip(color, 0, 1).astype(F32), alpha.astype(F32)


# ---------------------------------------------------------------- the fronds
TITLE = (176, 0, 480, 40)                                    # where the game writes the place's name over the picture (x0, y0, x1, y1)
GREEN = dict(dark=("#141b0d", "#1c2511", "#263216", "#30401b"), rib="#3d3217", rib_lit="#c7a24e",
             glow=("#6f8f28", "#96ae36", "#bec64e"), tip="#e6de7c", edge="#5f7a26")


def frond(sheets, rib, seed, long=84.0, wide=7.0, spread=44.0, sag=0.20, glow=0.22, thick=9.0, start=0.0, pitch=5.4):
    """One frond of the near palm, seen from under it against the light. `rib` is its midrib as a few points, from
    the crown outward. The leaflets stand off the rib in two rows like the barbs of a feather, `spread` degrees toward
    the tip, stiff blades `long` pixels at the most whose own weight bends them down. Most are dark; the blades that
    hang between us and the sun are lit through (`glow` of them, more in the row that stands up and toward the tip).
    `sheets` are (lit behind, dark, lit in front): three clear sheets, laid in that order."""
    behind, dark, front = sheets
    rng = np.random.default_rng(seed)
    pts = curve(rib, 14)
    seg = [math.hypot(pts[k + 1][0] - pts[k][0], pts[k + 1][1] - pts[k][1]) for k in range(len(pts) - 1)]
    total = sum(seg)
    along, k, done = [], 0, 0.0
    d = start * total
    while d < total - 3:
        while k < len(seg) - 1 and done + seg[k] < d:
            done += seg[k]
            k += 1
        f = (d - done) / max(seg[k], 1e-6)
        px = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * f
        py = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * f
        tx, ty = (pts[k + 1][0] - pts[k][0]) / max(seg[k], 1e-6), (pts[k + 1][1] - pts[k][1]) / max(seg[k], 1e-6)
        along.append((d / total, px, py, tx, ty))
        d += pitch * (0.75 + 0.5 * rng.random())
    blades = []
    for (t, px, py, tx, ty) in along:
        size = 1.0 if t < 0.55 else lerp(1.0, 0.36, (t - 0.55) / 0.45)                # shorter toward the tip
        if t < 0.14:
            size *= 0.55 + 0.45 * t / 0.14
        phi = math.atan2(ty, tx)
        for side in (-1, 1):
            if rng.random() < 0.04:                                                    # one missing
                continue
            ln = long * size * (0.8 + 0.36 * rng.random())
            a = phi + side * math.radians(spread * (0.86 + 0.28 * rng.random()))
            if t > 0.9:                                                                # the last ones lie along the rib
                a = lerp(a, phi, (t - 0.9) / 0.1 * 0.75)
            dx, dy = math.cos(a), math.sin(a) + 0.20                                   # its weight
            nrm = math.hypot(dx, dy)
            dx, dy = dx / nrm, dy / nrm
            nx, ny = -dy, dx
            droop = ln * sag * (0.7 + 0.6 * rng.random()) * (1.0 - 0.75 * max(0.0, dy))    # a blade that already hangs bends no more
            c = [(px + dx * ln * q, py + dy * ln * q + droop * q * q) for q in (0, 0.22, 0.48, 0.76, 1.0)]
            wd = wide * (0.8 + 0.4 * rng.random()) * (0.7 + 0.3 * size)
            prof = (0.5, 1.0, 0.9, 0.58, 0.0)
            poly = [(cx + nx * wd * 0.5 * p, cy + ny * wd * 0.5 * p) for (cx, cy), p in zip(c, prof)] + \
                   [(cx - nx * wd * 0.5 * p, cy - ny * wd * 0.5 * p) for (cx, cy), p in reversed(list(zip(c, prof))[:-1])]
            stands = dy < 0.35                                                          # the row that stands up into the light
            chance = glow * ((1.5 if stands else 0.55) + 0.6 * t)
            if TITLE[0] < c[2][0] < TITLE[2] and TITLE[1] < c[2][1] < TITLE[3]:        # the place's name is written here, in cream: dark behind it
                chance = 0.0
            blades.append((rng.random(), poly, c, rng.random() < chance, rng.random(), wd, nx, ny))
    for order, poly, c, shines, r, wd, nx, ny in sorted(blades, key=lambda b: b[0]):
        if shines:
            sheet = front if r < 0.34 else behind
            sheet.poly(poly, GREEN["glow"][min(2, int(rng.random() * 3))])
            if r > 0.5:
                sheet.line(c[2:], GREEN["tip"], 0.9)
        else:
            dark.poly(poly, GREEN["dark"][min(3, int(r * 4))])
            if r > 0.70:                                                                # the sun along a dark blade's upper edge
                sgn = -1.0 if ny > 0 else 1.0
                dark.line([(cx + sgn * nx * wd * 0.36, cy + sgn * ny * wd * 0.36) for cx, cy in c[1:4]], GREEN["edge"], 0.8)
    wid = [lerp(thick, 1.8, q / max(len(pts) - 1, 1)) for q in range(len(pts))]
    for k in range(len(pts) - 1):
        front.line([pts[k], pts[k + 1]], GREEN["rib"], wid[k])
    for k in range(len(pts) - 1):                                                      # the top of the rib takes the sun
        if wid[k] > 2.4:
            front.line([(pts[k][0] - 0.3, pts[k][1] - wid[k] * 0.30), (pts[k + 1][0] - 0.3, pts[k + 1][1] - wid[k + 1] * 0.30)], GREEN["rib_lit"], max(0.9, wid[k] * 0.24))


# Each frond's midrib, from the crown (above the frame, up and to the left) outward. They arch, and then they hang.
FRONDS = [
    # one behind the others and higher: only the ends of its hanging blades come into the picture, a fringe along the top
    dict(rib=[(84, -46), (150, -56), (226, -48), (300, -30), (352, -14)], seed=5, long=84, wide=7.0, spread=62, thick=8.0, start=0.06, glow=0.30, pitch=6.2),
    # the long one: out over the palms' crowns, its end coming down across the sky toward the pyramid
    dict(rib=[(96, -84), (190, -110), (284, -88), (356, -42), (412, 12), (452, 66)], seed=3, long=88, wide=7.4, spread=42, thick=10.0, start=0.40),
    # a shorter one whose end hangs beside the trunk
    dict(rib=[(86, -56), (112, -22), (132, 20), (144, 62), (148, 92)], seed=7, long=70, wide=6.6, spread=40, thick=8.5, start=0.20),
    # and from its neighbour on our right, outside the picture, the end of one frond in the top right corner
    dict(rib=[(868, -74), (822, -40), (788, 2), (766, 44), (756, 76)], seed=13, long=74, wide=6.6, spread=42, thick=8.5, start=0.25),
]


def fronds(seed=0):
    """The near palm's fronds across the top of the picture. -> (colour, mask)"""
    color = np.zeros(SHAPE + (3,), dtype=F32)
    alpha = np.zeros(SHAPE, dtype=F32)
    for f in FRONDS:
        sheets = (Sheet(SHAPE), Sheet(SHAPE), Sheet(SHAPE))
        frond(sheets, f["rib"], f["seed"] + seed, f.get("long", 84), f.get("wide", 7.0), f.get("spread", 44), f.get("sag", 0.20), f.get("glow", 0.22),
              f.get("thick", 9.0), f.get("start", 0.0), f.get("pitch", 5.4))
        for sheet in sheets:
            c, a = sheet.done()
            over(color, c, (a > 0.5).astype(F32))
            alpha = np.maximum(alpha, a)
    return color, alpha.astype(F32)


# ---------------------------------------------------------------- the lip of the bank, its grass and its stones
LIP = [(166, 608), (180, 574), (206, 560), (240, 553), (266, 557), (281, 572), (290, 589), (322, 591), (350, 591), (384, 589), (412, 583), (446, 577), (482, 579), (516, 586), (552, 592), (592, 598), (628, 606)]
GRASS = dict(dark=("#181c0c", "#212711", "#2c3116", "#38381a", "#453d1e"), lit=("#a8983f", "#cdb95c", "#ead78a"), culm="#54481f", head="#7a6a3a")


def tussock(dark, lit, bx, by, spread, height, count, seed, wind=0.10, heads=5):
    """A tussock of halfa grass: coarse blades in a fountain, the dry ones straw, a few flowering stems above them.
    The far blades first. The ones that stand toward the sun are lit along their length (the sheet `lit`)."""
    rng = np.random.default_rng(seed)
    blades = []
    for _ in range(count):
        a = float(np.clip(rng.normal(0, 0.62), -1.35, 1.35)) + wind
        ln = height * (0.5 + 0.55 * rng.random()) * (1 - 0.32 * abs(a) / 1.35)
        x0 = bx + rng.normal(0, spread * 0.30)
        y0 = by + rng.random() * 5
        a2 = a * 1.55 + wind
        p1 = (x0 + math.sin(a) * ln * 0.5, y0 - math.cos(a) * ln * 0.5)
        p2 = (x0 + math.sin(a) * ln * 0.5 + math.sin(a2) * ln * 0.5, y0 - math.cos(a) * ln * 0.5 - math.cos(a2) * ln * 0.5 + ln * 0.10 * abs(a2))
        blades.append((rng.random(), curve([(x0, y0), p1, p2], 6), a, rng.random(), ln))
    for order, c, a, r, ln in sorted(blades, key=lambda b: b[0]):
        wd = max(1.6, height * 0.030) * (0.8 + 0.5 * r)
        tone = GRASS["dark"][min(4, int((0.25 * order + 0.75 * r) * 5))]
        dark.taper(c, tone, wd, 0.8)
        if a < 0.15 and r > 0.84:                                                       # the sun down a blade that leans toward it
            lit.taper([(px - wd * 0.28, py) for px, py in c[1:]], GRASS["lit"][min(2, int(rng.random() * 3))], max(0.9, wd * 0.34), 0.8)
        elif r > 0.95:
            lit.line(c[-3:], GRASS["lit"][0], 0.9)
    for _ in range(heads):                                                              # flowering stems: thin, straight, a narrow head
        a = rng.normal(0, 0.16) + wind
        ln = height * (0.98 + 0.14 * rng.random())
        x0 = bx + rng.normal(0, spread * 0.2)
        top = (x0 + math.sin(a) * ln, by - math.cos(a) * ln)
        dark.line([(x0, by), top], GRASS["culm"], 1.2)
        for q in np.linspace(0.80, 1.0, 7):
            px, py = x0 + math.sin(a) * ln * q, by - math.cos(a) * ln * q
            for sd in (-1, 1):
                dark.line([(px, py), (px + sd * 3.2 * (1.15 - q) * 4 + math.sin(a) * 4, py - 4.5)], GRASS["head"], 1.0)
        lit.line([(top[0] - 0.6, top[1] + 14), (top[0] - 0.6, top[1] - 1)], GRASS["lit"][2], 0.9)


def crest(seed=61):
    """The lip of the bank we stand on, along the bottom of the picture, left and middle: a low dark band, its slip
    face toward us and away from the sun, its edge catching the light; stones bedded in it, cut by the frame; halfa
    grass on it. It is lowest where Dad first stands, and it stops short of the wagon's side of the picture."""
    rng = np.random.default_rng(seed)
    x, y = grid(SHAPE)
    top = curve(LIP, 8)
    m = mask_poly(SHAPE, top + [(628, 616), (166, 616)], wobble=1.0, seed=seed)
    line = np.interp(np.arange(W), [p[0] for p in top], [p[1] for p in top], left=616, right=616).astype(F32)
    down = np.clip((y - line[None, :]) / 30.0, 0, 1)                                    # 0 at its edge, 1 well below it
    color = lerp(rgb("#754a35"), rgb("#3d2620"), down[..., None]) * np.ones(SHAPE + (1,), dtype=F32)
    blot = noise(SHAPE, (46, 12), seed + 1, 4) - 0.5
    color = color * (1 + blot[..., None] * 0.30)
    color = color + ((noise(SHAPE, 3, seed + 2, 2) - 0.5) * 0.05)[..., None]            # grit
    s = Sheet(SHAPE)
    s.line(top[5:-8], "#f8d08c", 1.5)                                                   # the edge of the lip, in the sun
    s.line([(px, py + 1.6) for px, py in top[5:-8]], "#b77648", 1.2)
    lc, la = s.done()
    over(color, lc, la * (noise(SHAPE, (26, 3), seed + 3, 2) > 0.26))                   # (broken here and there: sand is not a kerb)
    alpha = m.copy()
    # stones bedded in the lip, cut by the frame: dark, their tops in the sun
    stones = Sheet(SHAPE)
    tones = ("#e6bc84", "#84634f", "#55403e", "#2f2327")
    # (none before the rock that lies on the sand at (300, 584): people walk round that one, so it shows whole)
    for (sx, sy, rx, ry, sd) in [(376, 611, 23, 17, 1), (410, 607, 11, 9, 2), (522, 608, 21, 15, 3), (196, 603, 16, 12, 4), (578, 607, 10, 8, 5), (258, 605, 12, 10, 6)]:
        land.rock(stones, sx, sy, rx, ry, seed + sd, tones)
    sc, sa = stones.done()
    over(color, sc, sa)
    alpha = np.maximum(alpha, sa)
    # the grass: two tussocks, and wisps along the lip between them (none where Dad first stands)
    dark, lit = Sheet(SHAPE), Sheet(SHAPE)
    tussock(dark, lit, 236, 566, 44, 90, 84, seed + 10, heads=6)                       # (its heads stop short of the place by the river where Dad stands, (240, 470))
    tussock(dark, lit, 458, 586, 34, 58, 52, seed + 11, heads=4)
    tussock(dark, lit, 196, 588, 20, 40, 22, seed + 12, heads=0)
    for k, (gx, gh) in enumerate([(392, 20), (420, 14), (506, 18), (534, 24), (566, 14), (598, 12), (182, 30), (274, 22)]):
        tussock(dark, lit, gx, float(line[gx]) + 4, 8 + gh * 0.4, gh, 7 + gh // 3, seed + 20 + k, heads=0)
    for sheet in (dark, lit):
        c, a = sheet.done()
        over(color, c, (a > 0.5).astype(F32))
        alpha = np.maximum(alpha, a)
    return np.clip(color, 0, 1).astype(F32), alpha.astype(F32)


def near(seed=0):
    """near.png: the trunk and the lip of the bank together. -> (colour, mask)"""
    tc, ta = trunk()
    cc, ca = crest()
    color = np.zeros(SHAPE + (3,), dtype=F32)
    over(color, tc, (ta > 0.5).astype(F32))
    over(color, cc, (ca > 0.5).astype(F32))
    return color, np.maximum(ta, ca).astype(F32)


# ---------------------------------------------------------------- the papyrus and the reeds (front.png)
def umbel(s, cx, cy, R, seed, tones=("#0f1a12", "#182a16", "#24401c", "#6f8f34", "#c6c86c"), rays=84):
    """One great head of papyrus close to the lens: fine rays all round, drooping at their ends, each ending in a
    little fork of spikelets. Dark against the light, the rays toward the sun lit."""
    rng = np.random.default_rng(seed)
    marks = sorted((rng.random(), math.radians(rng.uniform(-28, 208))) for _ in range(rays))
    for depth, a in marks:
        r = R * (0.70 + 0.40 * rng.random())
        dx, up = math.cos(a), math.sin(a)
        droop = r * (0.10 + 0.46 * (1 - max(up, 0)) ** 1.4)
        mid = (cx + dx * r * 0.55, cy - up * r * 0.62)
        tip = (cx + dx * r, cy - up * r * 0.88 + droop)
        sunny = dx < 0.25 and up > -0.1 and depth > 0.45 and rng.random() < 0.6
        tone = tones[3] if sunny else tones[int(depth * 2.99)]
        ray = curve([(cx, cy), mid, tip], 5)
        s.taper(ray, tone, 1.5, 0.9)
        ang = math.atan2(ray[-1][1] - ray[-2][1], ray[-1][0] - ray[-2][0])
        for f in (-0.5, 0.0, 0.5):
            s.line([tip, (tip[0] + math.cos(ang + f) * 5.5, tip[1] + math.sin(ang + f) * 5.5)], tones[4] if sunny and f == 0 else tone, 0.9)
    s.ellipse(cx, cy + 1, 3.2, 2.8, tones[1])


def blade(s, x0, y0, height, lean, seed, tones=("#0f1a12", "#182c16", "#22401c"), lit="#7c9c3a", wide=8.0):
    """A reed's long leaf close to the lens: a wide blade that rises and bends over with the wind."""
    rng = np.random.default_rng(seed)
    a = lean
    p1 = (x0 + math.sin(a) * height * 0.55, y0 - math.cos(a) * height * 0.55)
    a2 = a + 0.5 + 0.5 * rng.random()
    p2 = (p1[0] + math.sin(a2) * height * 0.42, p1[1] - math.cos(a2) * height * 0.42 + height * 0.05)
    c = curve([(x0, y0), p1, p2], 8)
    s.taper(c, tones[int(rng.random() * 2.99)], wide, 0.9)
    if rng.random() < 0.6:
        s.taper([(px - wide * 0.22, py) for px, py in c[2:-2]], lit, wide * 0.22, 0.7)


def papyrus(seed=11):
    """front.png: the papyrus at the very front, bottom left, tall and dark against the bright water with a few heads
    in the sun, as it always was; round twenty-three thins it a little over the water and adds what stands closer
    still: reed blades, and two great umbels low over the bank's sand."""
    s = Sheet(SHAPE)
    # (the cloud's shadow lies over this corner: the clump is in shade, a step deeper than it was, its lit heads fewer)
    flora.papyrus_stand(s, 44, 604, 104, 270, seed + 5, count=9, greens=("#101d15", "#1f3a1c", "#456a2a", "#93a650"))
    flora.papyrus_stand(s, 132, 606, 70, 150, seed + 4, count=7, greens=("#12201a", "#25431f", "#4e722c", "#9aae58"))
    flora.reeds(s, 60, 602, 90, 70, seed + 5, count=40, greens=("#101d15", "#1f3a1c", "#40602a"), heads="#6e4a26")
    # closer: stalks as thick as a wrist coming up out of the corner, and their heads
    for (x0, cx, cy, R, sd) in [(64, 92, 500, 60, 1), (150, 170, 546, 50, 2)]:
        stalk = curve([(x0, 612), ((x0 + cx) / 2 - 4, (612 + cy) / 2), (cx, cy)], 8)
        s.taper(stalk, "#0f1a12", 5.6, 3.4)
        s.taper([(px - 1.5, py) for px, py in stalk], "#3a5c28", 1.3, 0.9)
        umbel(s, cx, cy, R, seed + 20 + sd)
    for k, (x0, hgt, lean) in enumerate([(14, 150, 0.10), (30, 118, 0.26), (52, 96, -0.05), (104, 84, 0.34), (126, 112, 0.16), (176, 66, 0.42), (8, 92, 0.5)]):
        blade(s, x0, 606, hgt, lean, seed + 40 + k)
    return s.done()

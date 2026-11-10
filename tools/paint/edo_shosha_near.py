"""PAINT-23: the NEAR plane of the foot of Mount Shosha (edo-shosha): what stands within a few metres of the lens, between
us and the play. People always pass behind it (`plane: "front"`).

WHERE WE STAND   On the terrace south-west of the hall, under an old red pine; the eye 2.52 m up (the scene's camera). So
what is near us is:

  pine.png    the OLD PINE: its trunk up the left edge, leaning in (rooted below the frame, 4.8 m from the lens, 66 cm
              thick: a hand's breadth of the picture and more), its bark in scales, and its great bough sweeping right
              across the top of the picture, low and long as an old pine's is, its pads of needles hanging into the
              hall's peak: the roof is lost in them. It stirs (the scene's fx `pine`, a sway rooted at its foot).
  near.png    what grows at our feet (still): the pine's surface roots running out into the bottom left, moss on them,
              ferns among them (bracken uncurling, a few hard ferns), and in the bottom right corner the bank's lip where
              the road comes up: tall grass and ferns.

A clear dark mass, the warmest darks of the picture (the pine's own shade), lit only along the edges that face the sun:
in the gold light the tops and the left of the pads and the bough, the trunk's left edge; at sunset a thin red rim on
their left. Outline before inside: needle ends against the sky and the woods, a broken stub; no small gaps of light shut
inside a pad (the game's paints would key them as white specks: round twenty-three's lesson). Nothing near the lens looks
like a thing to pick up."""

import math

import numpy as np

from brush import F32, Sheet, curve, grid, lerp, noise, rgb, step, warp, blur
import depth as DEPTH
import edo_shosha_kit as K
from edo_shosha_kit import *

X_, Y_ = grid(SHAPE)


def colours():
    gold = K.LIGHT == "gold"
    c = dict(
        bark_dark=lerp(mixp(SIENNA, PRUSSIAN, 0.62), rgb("#1c1420"), 0.52),
        bark_mid=lerp(mixp(SIENNA, PRUSSIAN, 0.50), rgb("#1c1420"), 0.30),
        bark_cool=lerp(lerp(mixp(SIENNA, PRUSSIAN, 0.55), rgb("#1c1420"), 0.3), thin(mixp(COBALT, PRUSSIAN, 0.4), 0.3), 0.40),
        bark_red=lerp(mixp(SIENNA, ORANGE, 0.25), PRUSSIAN, 0.30),          # the red pine's bark up high, where it flakes thin
        bark_grey=lerp(thin(mixp(SIENNA, PRUSSIAN, 0.34), 0.30), rgb("#3a2c2c"), 0.22),   # its old plates low down, in the sun
        needle_dark=lerp(mixp(VIRIDIAN, PRUSSIAN, 0.68), rgb("#161a22"), 0.38),
        needle_mid=lerp(mixp(VIRIDIAN, PRUSSIAN, 0.50), rgb("#161a22"), 0.12),
        grass_dark=lerp(mixp(VIRIDIAN, OCHRE, 0.40), PRUSSIAN, 0.52),
        grass_mid=lerp(mixp(VIRIDIAN, OCHRE, 0.48), PRUSSIAN, 0.30),
        fern=lerp(mixp(VERONESE, VIRIDIAN, 0.45), PRUSSIAN, 0.40),
        moss=lerp(mixp(VIRIDIAN, OCHRE, 0.35), PRUSSIAN, 0.38),
        root=lerp(mixp(SIENNA, PRUSSIAN, 0.55), rgb("#1c1420"), 0.25),
    )
    if gold:
        c.update(rim=thin(mixp(OCHRE, NAPLES, 0.45), 0.10), needle_lit=lerp(mixp(VERONESE, OCHRE, 0.30), PRUSSIAN, 0.22),
                 bark_lit=thin(mixp(SIENNA, ORANGE, 0.45), 0.10), fern_lit=lerp(mixp(VERONESE, NAPLES, 0.35), PRUSSIAN, 0.10))
    else:
        c.update(rim=thin(mixp(ORANGE, VERMILION, 0.35), 0.08), needle_lit=lerp(mixp(VIRIDIAN, LAKE, 0.35), PRUSSIAN, 0.30),
                 bark_lit=thin(mixp(VERMILION, ORANGE, 0.45), 0.05), fern_lit=lerp(mixp(VIRIDIAN, LAKE, 0.3), PRUSSIAN, 0.3))
        for k_ in ("bark_dark", "bark_mid", "bark_red", "bark_grey", "needle_dark", "needle_mid", "grass_dark", "grass_mid", "fern", "moss", "root"):
            c[k_] = lerp(c[k_], rgb("#1a1630"), 0.25)
    return c


# the old pine in the world (cm)
def trunk_at(h):
    X = NEAR_PINE["X"] + 0.075 * h + 12.0 * math.sin(h / 140.0)
    D = NEAR_PINE["D"] + 0.03 * h
    p = P(X, h, D)
    return p, 2 * NEAR_PINE["r"] * (1.0 - 0.00028 * h) * F / D


def pad(L, rng, C, cx, cy, rx, ry, lit=0.5, needle=13.0, light=(-1.0, -0.6)):
    """One pad of needles seen from below: a flat dark mass, its edge all needle ends (tufts fanning out and up); only
    the tufts on the rim that faces the light are lighter."""
    L.ellipse(cx, cy + ry * 0.1, rx * 0.92, ry * 0.8, C["needle_dark"])
    n = max(8, int(rx * ry / 7.0))
    ll = math.hypot(*light)
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        rr = math.sqrt(rng.random()) if i % 3 else 1.0
        px_, py_ = cx + math.cos(a) * rx * rr * 0.95, cy + math.sin(a) * ry * rr * 0.9
        out = math.atan2((py_ - cy) / max(ry, 1), (px_ - cx) / max(rx, 1))
        mid = math.atan2(0.55 * math.sin(out) - 0.45 + (0.25 if math.sin(out) > 0.3 else 0), 0.55 * math.cos(out))
        facing = (math.cos(out) * light[0] + math.sin(out) * light[1]) / ll
        is_lit = facing > 0.40 and rr > 0.8 and rng.random() < lit
        tone = C["needle_lit"] if is_lit else (C["needle_mid"] if rng.random() < 0.22 + 0.25 * max(facing, 0) else C["needle_dark"])
        for j in range(int(rng.uniform(9, 14))):
            an = mid + rng.uniform(-1.2, 1.2)
            ln = needle * rng.uniform(0.6, 1.12)
            L.line([(px_, py_), (px_ + math.cos(an) * ln, py_ + math.sin(an) * ln)], tone if (not is_lit or j % 3) else C["needle_mid"], rng.uniform(0.8, 1.3), 0.95)


def limb(L, C, pts, w0, w1, lit=True):
    c = curve(pts, 10)
    L.taper(c, C["bark_dark"], w0, w1)
    if lit:
        L.taper([(px_ - 0.08 * w0, py_ - 0.30 * w0) for px_, py_ in c], C["bark_mid"], w0 * 0.42, w1 * 0.4, alpha=0.8)
        L.taper([(px_ - 0.05 * w0, py_ - 0.42 * w0) for px_, py_ in c], C["bark_lit"], w0 * 0.14, w1 * 0.12, alpha=0.75)
    return c


def trunk(C, seed=41):
    """The trunk, laid pixel by pixel as the round thing it is: a column of old red-pine bark turned in the light (the
    sun's side by the cosine law about its axis, the side away from it dark, its far edge taking a cool breath from the
    open sky), its bark in plates: thick, grey-brown and deeply split low down, smaller, thinner and redder as it rises,
    each plate's edge toward the sun catching a little more of it. -> (colour, cover)."""
    rows = np.arange(H, dtype=F32) + 0.5
    hh = np.arange(-120.0, 760.0, 3.0)
    at_ = [trunk_at(h) for h in hh]
    ys = np.array([p[0][1] for p in at_])
    o = np.argsort(ys)
    ax = np.interp(rows, ys[o], np.array([p[0][0] for p in at_])[o])
    hw = np.interp(rows, ys[o], np.array([p[1] for p in at_])[o]) / 2
    hrow = np.interp(rows, ys[o], hh[o])

    def wob(step_, amp, s):                                                 # the plates break the outline a little
        k = np.arange(-step_, H + 2 * step_, step_)
        return np.interp(rows, k, np.random.default_rng(s).normal(0, amp, len(k))).astype(F32)
    lx = ax - hw + wob(11, 1.1, seed) + wob(4, 0.5, seed + 1)
    rx = ax + hw + wob(11, 1.3, seed + 2) + wob(4, 0.6, seed + 3)
    xc = X_ + 0.5
    cover = np.clip(np.minimum(xc - lx[:, None], rx[:, None] - xc) + 0.5, 0, 1).astype(F32)
    f = np.clip((xc - (ax - hw)[:, None]) / (2 * hw)[:, None], 0.0, 1.0)
    th = np.arcsin(np.clip(1 - 2 * f, -1, 1))                               # round the trunk: 0 facing us, + toward the left
    # the light about the trunk's axis: its normal facing us, its normal at the left edge, the sun's direction
    X0, D0 = NEAR_PINE["X"] + 30.0, NEAR_PINE["D"] + 8.0
    vl = math.hypot(X0, D0)
    n0 = (-X0 / vl, -D0 / vl)
    t0 = (-D0 / vl, X0 / vl)
    sx, sy, sd = K.SUN[K.LIGHT]
    sh_ = math.hypot(sx, sd)
    th_s = math.atan2((sx * t0[0] + sd * t0[1]) / sh_, (sx * n0[0] + sd * n0[1]) / sh_)
    lam = np.clip(sh_ / math.hypot(sh_, sy) * np.cos(th - th_s), 0, 1)
    lam = lam * (0.72 + 0.28 * noise(SHAPE, (40, 70), seed + 5, 3))          # the crowns above break it a little
    # the plates: a jittered grid round the trunk and up it, its cells tall, smaller higher up
    r_cm = NEAR_PINE["r"] * (1 - 0.00028 * np.clip(hrow, 0, None))
    up = np.clip(hrow / 460.0, 0, 1)
    su = (11.0 - 5.0 * up)[:, None]
    hgrid = np.arange(-200.0, 900.0, 1.0)
    vcum = np.cumsum(1.0 / (26.0 - 15.0 * np.clip(hgrid / 460.0, 0, 1)))
    U = th * r_cm[:, None] / su
    V = np.interp(hrow, hgrid, vcum)[:, None] * np.ones_like(U)
    U = U + (noise(SHAPE, (10, 26), seed + 11, 3) - 0.5) * 0.55                  # the plates' edges ragged, not ruled
    V = V + (noise(SHAPE, (14, 18), seed + 12, 3) - 0.5) * 0.45
    rng = np.random.default_rng(seed + 7)
    jit = rng.uniform(-0.38, 0.38, (2, 96, 200)).astype(F32)
    tone_ = rng.uniform(0, 1, (96, 200)).astype(F32)
    iu, iv = np.floor(U).astype(int), np.floor(V).astype(int)
    f1 = np.full(U.shape, 9.0, F32)
    f2 = np.full(U.shape, 9.0, F32)
    du, dv, du2, dv2 = (np.zeros(U.shape, F32) for _ in range(4))
    pt = np.zeros(U.shape, F32)
    for oi in (-1, 0, 1):
        for oj in (-1, 0, 1):
            ci, cj = np.clip(iu + oi + 48, 0, 95), np.clip(iv + oj + 20, 0, 199)
            cu_ = iu + oi + 0.5 + jit[0, ci, cj]
            cv_ = iv + oj + 0.5 + jit[1, ci, cj]
            eu, ev = U - cu_, (V - cv_) * 0.8
            d = np.sqrt(eu * eu + ev * ev)
            closer = d < f1
            second = (~closer) & (d < f2)
            f2 = np.where(closer, f1, np.where(second, d, f2))
            du2 = np.where(closer, du, np.where(second, eu, du2))
            dv2 = np.where(closer, dv, np.where(second, ev, dv2))
            du = np.where(closer, eu, du)
            dv = np.where(closer, ev, dv)
            pt = np.where(closer, tone_[ci, cj], pt)
            f1 = np.where(closer, d, f1)
    # the splits: the long ones up the trunk deep and wide, the cross cracks between plates thin; some lost altogether
    across = np.abs(du - du2) / np.maximum(np.hypot(du - du2, dv - dv2), 1e-3)
    wide = (0.07 + 0.11 * (1 - up))[:, None] * (0.25 + 1.5 * noise(SHAPE, (16, 34), seed + 13, 3) ** 1.4) * (0.45 + 0.85 * across)
    split = np.clip(1 - (f2 - f1) / np.maximum(wide, 0.02), 0, 1) ** 1.3
    bulge = np.clip(1.0 + 1.1 * (du * 0.75 + dv * 0.55), 0.45, 1.5)                      # a plate's edge toward the sun
    red = np.clip((hrow - 200.0) / 260.0, 0, 1)[:, None]
    shade_c = lerp(C["bark_dark"], C["bark_mid"], (0.15 + 0.6 * pt)[..., None])
    lit_c = lerp(C["bark_grey"], C["bark_lit"], (red * (0.75 + 0.25 * pt))[..., None]) * (0.86 + 0.22 * pt)[..., None]
    k = np.clip(np.clip(lam * 1.55, 0, 1) * bulge, 0, 1)
    col = lerp(shade_c, lit_c, k[..., None])
    col = lerp(col, C["bark_cool"], (np.clip((f - 0.80) / 0.20, 0, 1) * 0.5 * (1 - split))[..., None])
    deep = lerp(C["bark_dark"][None, :], rgb("#0c0912")[None, :], (0.55 + 0.3 * (1 - up))[:, None])[:, None, :]
    col = lerp(col, deep, (split * (0.55 + 0.4 * (1 - k * 0.5)))[..., None])
    lich = step(0.70, 0.78, noise(SHAPE, (9, 16), seed + 9, 3)) * np.clip((260.0 - hrow) / 120.0, 0, 1)[:, None] * (1 - split)
    col = lerp(col, lerp(C["moss"], C["bark_cool"], 0.35), (lich * 0.45)[..., None])          # a little lichen low on it
    cover = cover * (hrow > -100.0)[:, None]
    return np.clip(col, 0, 1).astype(F32), cover.astype(F32)


def pine_cut(seed=19):
    """pine.png: the old pine's trunk up the left edge and its great bough across the top. -> (colour, cover)."""
    C = colours()
    L = Wet(SHAPE)
    rng = np.random.default_rng(seed)
    at = lambda h: trunk_at(h)[0]
    # the great bough: out of the trunk at 4.6 m, sweeping right along the top, sagging, its tip lifting; its pads hang
    # from it, the last of them into the hall's peak
    b0 = at(462.0)
    bough = [b0, (b0[0] + 90, b0[1] + 10), (b0[0] + 190, b0[1] + 26), (b0[0] + 290, b0[1] + 38), (b0[0] + 370, b0[1] + 50), (b0[0] + 430, b0[1] + 60), (b0[0] + 476, b0[1] + 58)]
    limb(L, C, bough, 30, 7)
    limb(L, C, [(b0[0] + 190, b0[1] + 26), (b0[0] + 214, b0[1] + 52), (b0[0] + 246, b0[1] + 70), (b0[0] + 270, b0[1] + 76)], 8, 3.5)
    limb(L, C, [(b0[0] + 330, b0[1] + 44), (b0[0] + 356, b0[1] + 18), (b0[0] + 392, b0[1] + 0), (b0[0] + 420, b0[1] - 8)], 9, 3.5)
    limb(L, C, [(b0[0] + 380, b0[1] + 52), (b0[0] + 400, b0[1] + 84), (b0[0] + 418, b0[1] + 112), (b0[0] + 430, b0[1] + 128)], 7, 3.0)
    b2 = at(300.0)
    stub = [b2, (b2[0] + 20, b2[1] - 8), (b2[0] + 34, b2[1] - 18)]                 # the stub of a lost limb
    L.taper(curve(stub, 6), C["bark_dark"], 12, 7)
    L.poly([(stub[2][0] - 4, stub[2][1] - 3), (stub[2][0] + 5, stub[2][1] - 8), (stub[2][0] + 2, stub[2][1] + 1), (stub[2][0] + 7, stub[2][1] + 3), (stub[2][0] - 1, stub[2][1] + 5)], C["bark_dark"])
    L.add(*trunk(C))
    #                     x, y (offsets from the bough's root), half width, half height
    pads = [(-34, -14, 50, 18), (40, -16, 48, 16), (110, -6, 52, 17), (76, 22, 34, 12), (176, 10, 48, 15), (236, 22, 44, 14),
            (206, 58, 34, 12), (268, 70, 30, 10), (300, 34, 44, 14), (356, 46, 38, 12), (404, 26, 38, 12), (420, 74, 32, 11),
            (434, 118, 30, 11), (460, 52, 30, 10), (380, -4, 32, 10), (140, 40, 26, 9), (-10, 20, 30, 12), (330, 6, 30, 10)]
    for (dx, dy, rx, ry) in pads:
        pad(L, rng, C, b0[0] + dx, b0[1] + dy, rx, ry, lit=0.55 if K.LIGHT == "gold" else 0.35)
    c, a = L.done()
    a_hard = (a > 0.5).astype(F32)
    rim = DEPTH.rim(a_hard, light=(-1.0, -0.55), width=2.2)
    lum_ = c @ np.array([0.3, 0.55, 0.15], dtype=F32)
    warm = np.clip(c * 2.2 + (C["rim"] * 0.35), 0, 1)
    c = lerp(c, warm, (np.clip(rim * 1.1, 0, 1) * (lum_ < 0.42) * (0.75 if K.LIGHT == "gold" else 0.9))[..., None])
    c = grade_cut(c, a, 0.93, seed=seed, uneven=0.05)
    return c.astype(F32), np.clip(a, 0, 1)


def near_cut(seed=29):
    """near.png: the pine's surface roots, moss and ferns along the bottom left; the bank's lip with grass and ferns in
    the bottom right corner. -> (colour, cover)."""
    C = colours()
    L = Wet(SHAPE)
    rng = np.random.default_rng(seed)
    # ---- the roots: thick, snaking out from below the frame into the picture, moss on their backs
    roots = [[(-10, 604), (40, 586), (96, 578), (150, 588), (196, 604)], [(-10, 572), (20, 566), (56, 570), (88, 586), (110, 606)],
             [(60, 606), (90, 594), (132, 598), (160, 608)]]
    for i, r in enumerate(roots):
        c_ = curve(r, 8)
        L.taper(c_, C["root"], 26 - i * 7, 9)
        L.taper([(x, y - 4) for x, y in c_], C["moss"], 12 - i * 3, 4, alpha=0.8)
        L.taper([(x - 1, y - 6) for x, y in c_], C["bark_lit"] if K.LIGHT == "gold" else C["rim"], 3, 1, alpha=0.5)
    # the ground between them: needles and moss, dark
    top = [(float(x), 600.0 - (14 + 10 * math.sin(x / 37.0) ** 2) * max(0.0, 1 - x / 270.0)) for x in np.arange(-4, 272, 6)]
    L.poly([(-4, 604)] + top + [(272, 604)], lerp(C["moss"], C["root"], 0.5), lerp(C["root"], rgb("#1c1420"), 0.3))

    def frond(x0, y0, ln, ang, lit, droop=0.35, n=11):
        """A fern frond: a curved rachis with pinnae either side, shorter toward the tip; it arches and droops."""
        pts = []
        for i in range(n + 1):
            t = i / n
            a = ang + droop * t * (1 if math.cos(ang) > 0 else -1)
            pts.append((x0 + math.cos(ang) * ln * t + math.cos(a) * ln * t * 0.1, y0 + math.sin(ang) * ln * t + droop * ln * t * t * 0.5))
        tone = C["fern_lit"] if lit else C["fern"]
        L.line(pts, lerp(tone, C["root"], 0.3), 1.0, 0.95)
        for i in range(1, n):
            t = i / n
            px_, py_ = pts[i]
            qx, qy = pts[i + 1][0] - pts[i - 1][0], pts[i + 1][1] - pts[i - 1][1]
            d = math.hypot(qx, qy) or 1
            nx_, ny_ = -qy / d, qx / d
            pl = ln * 0.22 * (1 - t) ** 0.7 + 1.5
            for s_ in (-1, 1):
                tip = (px_ + nx_ * pl * s_ + qx / d * pl * 0.35, py_ + ny_ * pl * s_ + qy / d * pl * 0.35 + pl * 0.25)
                L.poly([(px_, py_), (px_ + qx / d * 1.6, py_ + qy / d * 1.6), tip], tone if (s_ < 0 or not lit) else lerp(tone, C["fern"], 0.4))
    #           x, y, length, angle (radians: -pi/2 up), lit
    ferns = [(30, 600, 70, -1.9, False), (52, 604, 82, -1.3, True), (96, 606, 66, -2.2, False), (120, 604, 74, -0.9, False), (150, 606, 60, -1.6, True),
             (186, 606, 52, -0.7, False), (214, 608, 46, -2.3, False), (12, 590, 54, -1.1, False), (236, 610, 40, -0.9, False)]
    for (x, y, ln, ang, lit) in ferns:
        frond(x, y, ln, ang, lit)
    for (x, y) in ((70, 592), (176, 600)):                                   # bracken just uncurling: a crozier
        L.line(curve([(x, y + 8), (x + 2, y - 10), (x + 8, y - 20), (x + 14, y - 18), (x + 12, y - 13)], 6), C["fern_lit"], 2.2, 0.95)
    # ---- the bottom right: the bank's lip where the road comes up, tall grass and ferns
    lip = [(float(x), 600.0 - 22.0 * max(0.0, (x - 726) / 74.0) ** 0.7 - 3.0) for x in np.arange(722, 806, 4)]
    L.poly([(722, 604)] + lip + [(806, 604)], lerp(C["grass_dark"], C["root"], 0.4), C["root"])
    for x in np.arange(728.0, 806.0, 2.4):
        y0 = 600.0 - 22.0 * max(0.0, (x - 726) / 74.0) ** 0.7
        ln = rng.uniform(10, 34) * min(1.0, (x - 722) / 30.0)
        lean = rng.uniform(-0.6, 0.3)
        tip = (x + lean * ln, y0 - ln * math.sqrt(max(0.1, 1 - lean * lean)))
        L.taper(curve([(x, y0 + 2), (x + lean * ln * 0.4, y0 - ln * 0.6), tip], 5), C["grass_dark"] if rng.random() < 0.7 else C["grass_mid"], 2.0, 0.5)
    for (x, y, ln, ang, lit) in ((770, 606, 60, -2.0, True), (790, 600, 56, -1.5, False), (752, 608, 44, -2.5, False)):
        frond(x, y, ln, ang, lit)
    c, a = L.done()
    a_hard = (a > 0.5).astype(F32)
    rim = DEPTH.rim(a_hard, light=(-1.0, -0.6), width=1.8)
    c = lerp(c, np.clip(c * 1.7 + C["rim"] * 0.25, 0, 1), (np.clip(rim, 0, 1) * 0.7)[..., None])
    c = grade_cut(c, a, 0.92, seed=seed, uneven=0.05)
    return c.astype(F32), np.clip(a, 0, 1)

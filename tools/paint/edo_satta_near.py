"""PAINT-23 (round twenty-three, DEPTH.md): the NEAR plane of the top of the Satta Pass (edo-satta): what stands within a
few metres of the lens, between us and the play. People always pass behind it (`plane: "front"`).

WHERE WE STAND   The eye is 3.3 m over the road (the scene's camera, unchanged): we stand on the uphill side of the road
of 1655, on the lip of the cutting it was made by, and look down over the road and out over the drop. So what is near
us is:

  near.png    a WIND-BENT BLACK PINE, kin of the bent pine at the edge, growing on the slope at our right: its foot is out
              of the frame below and to the right (about 4.5 m from the lens), its trunk (30 cm: a hand's breadth of the
              picture) comes in from the right edge above Okitsu and climbs out of the top; its limbs and their pads of
              needles stream to the left across the top of the picture, as the wind off the sea has trained them, to just
              short of Fuji's cap of cloud. A broken stub on its windward side. It stirs in the wind (fx near-sway: the
              limbs' tips lift and fall; the trunk at the edge does not move).
  front.png   the LIP OF THE CUTTING along the whole bottom (the scene's own front plane, drawn again and more of it):
              the mountain's rock breaking through the turf, low thickets of sasa (bamboo grass, as on Yui's bank) and
              wiry grass, all swept to the left by the wind; low along the left (the three come up from the climb there,
              and their feet stay in sight) and rising in the bottom right corner into a shoulder of rock with a clump of
              last year's pampas grass (the road under it is a `blocked` patch: edo_satta_kit.BLOCK).

All of it in shade, warm in its darks (the mountainside behind us still keeps the low sun off our side of the road), and
lit only where the morning sun, behind us and to the left, catches an edge: the trunk's upper left side, the left of each
pad, the tips of the grass, the rock's top. Outline before inside: the sky between the pads, the broken stub, blades
against the sunlit road.

Nothing here is clicked or picked up, and nothing clicked or stood on is behind it (depth_check.py): the trunk stays
above Okitsu and the temple (nothing at the right edge below row 256), the limbs end short of the cap of cloud and above
the bent pine's crown, the lip stays under the feet of whoever stands at the marks.
"""

import math

import numpy as np

from brush import *
import depth as D
from edo_satta_kit import *
from edo_village_near import (BARK_DARK, BARK_MID, BARK_LIT, BARK_COOL, NEEDLE_DARK, NEEDLE_MID, NEEDLE_LIT, GRASS_DARK, GRASS_MID,
                              STRAW_DARK, STRAW_LIT, bark, limb)

ROCK_DARK = lerp(mixp(PRUSSIAN, SIENNA, 0.38), rgb("#1a1422"), 0.42)
ROCK_MID = lerp(mixp(PRUSSIAN, OCHRE, 0.30), rgb("#1a1422"), 0.20)
ROCK_LIT = lerp(thin(mixp(OCHRE, NAPLES, 0.40), 0.25), mixp(SIENNA, PRUSSIAN, 0.3), 0.18)
TURF = lerp(GRASS_DARK, BARK_DARK, 0.40)
TURF_DEEP = lerp(GRASS_DARK, BARK_DARK, 0.80)

# the trunk in the world (cm): 4.55 m in front of the lens (z = -420), leaning in from the right and up out of the frame
TZ = -420.0
TK = CAM.scale(TZ)


def tpt(X, Y):
    return CAM.pt(X, Y, TZ)


def trunk_line():
    """The trunk's middle, foot first (picture points), and its thickness there (px)."""
    ys = np.linspace(330.0, 500.0, 16)
    pts, wds = [], []
    for Y in ys:
        u = (Y - 330.0) / 170.0
        X = 252.0 - 80.0 * u - 10.0 * u * u + 5.0 * math.sin(u * 5.0)             # a lean, and the kink the wind has given it
        pts.append(tpt(X, Y))
        wds.append((30.0 - 7.0 * u) * TK)
    return pts, wds


def pad(L, S, rng, cx, cy, rx, ry, light=(-1.0, -0.6), needle=12.0, lit=0.5, wind=0.55):
    """One pad of pine needles seen from below (Yui's pad, combed by the wind): a flat dark mass whose edge is all
    needle ends fanning out, every tuft swept to the left; only the tufts on the rim that faces the sun are lighter."""
    L.ellipse(cx, cy + ry * 0.12, rx * 0.90, ry * 0.78, NEEDLE_DARK)
    n = max(7, int(rx * ry / 7.0))
    ll = math.hypot(*light)
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        rr = math.sqrt(rng.random()) if i % 3 else 1.0
        px_, py_ = cx + math.cos(a) * rx * rr * 0.95, cy + math.sin(a) * ry * rr * 0.9
        out = math.atan2((py_ - cy) / max(ry, 1), (px_ - cx) / max(rx, 1))
        dx_, dy_ = 0.5 * math.cos(out) - wind, 0.5 * math.sin(out) - 0.30 + (0.2 if math.sin(out) > 0.3 else 0)
        mid = math.atan2(dy_, dx_)
        facing = (math.cos(out) * light[0] + math.sin(out) * light[1]) / ll
        is_lit = facing > 0.40 and rr > 0.8 and rng.random() < lit
        tone = NEEDLE_LIT if is_lit else (NEEDLE_MID if rng.random() < 0.22 + 0.25 * max(facing, 0) else NEEDLE_DARK)
        for j in range(int(rng.uniform(9, 14))):
            an = mid + rng.uniform(-0.9, 0.9)
            ln = needle * rng.uniform(0.6, 1.15)
            S.line([(px_, py_), (px_ + math.cos(an) * ln, py_ + math.sin(an) * ln)], tone if (not is_lit or j % 3) else NEEDLE_MID, rng.uniform(0.8, 1.3), 0.95)


def near_cut(back, seed, fast=False):
    """near.png: the wind-bent pine. -> (colour, cover)."""
    L = Wet(SHAPE)
    S = Sheet(SHAPE)
    rng = np.random.default_rng(seed)
    pts, wds = trunk_line()
    at = lambda i: pts[i]
    # ---- the limbs first (they pass behind the trunk where they leave it), streaming left
    a0, b0, c0 = at(8), at(12), at(6)
    A = limb(L, [a0, (a0[0] - 46, a0[1] - 4), (a0[0] - 104, a0[1] - 22), (a0[0] - 160, a0[1] - 34), (a0[0] - 214, a0[1] - 42), (a0[0] - 262, a0[1] - 50)], 22, 6, 1)
    B = limb(L, [b0, (b0[0] - 40, b0[1] - 18), (b0[0] - 92, b0[1] - 30), (b0[0] - 150, b0[1] - 40), (b0[0] - 196, b0[1] - 52)], 17, 5, 2)
    C = limb(L, [c0, (c0[0] - 30, c0[1] + 6), (c0[0] - 64, c0[1] + 8), (c0[0] - 98, c0[1] + 5)], 12, 4, 3)
    T = limb(L, [(A[len(A) // 2][0], A[len(A) // 2][1]), (A[len(A) // 2][0] - 16, A[len(A) // 2][1] + 20), (A[len(A) // 2][0] - 40, A[len(A) // 2][1] + 30)], 6, 2.5, 4)
    limb(L, [(B[len(B) // 3][0], B[len(B) // 3][1]), (B[len(B) // 3][0] - 6, B[len(B) // 3][1] - 22), (B[len(B) // 3][0] - 26, B[len(B) // 3][1] - 40)], 6, 2.5, 5)
    # the stub of a limb the wind took, on the windward side: broken, bare
    s0 = at(10)
    stub = [s0, (s0[0] + 20, s0[1] - 14), (s0[0] + 34, s0[1] - 26)]
    L.taper(curve(stub, 6), BARK_DARK, 13, 8)
    L.poly([(stub[2][0] - 5, stub[2][1] - 2), (stub[2][0] + 3, stub[2][1] - 9), (stub[2][0] + 3, stub[2][1] + 1), (stub[2][0] + 8, stub[2][1] + 2), (stub[2][0] - 1, stub[2][1] + 5)], BARK_DARK)
    L.line([(stub[0][0] + 4, stub[0][1] - 9), (stub[2][0] - 3, stub[2][1] - 4)], BARK_MID, 2.0, 0.8)
    # ---- the trunk: old black-pine bark in scales (Yui's), the sun along its upper left
    bark(L, rng, pts, wds)
    # ---- the pads of needles: on and under the limbs, layered, all swept to the left
    def along(c, f):
        i = min(int(f * (len(c) - 1)), len(c) - 1)
        return c[i]
    pads = []
    for (c, fs, dy, rx0) in ((A, (0.18, 0.40, 0.62, 0.82, 0.98), -10, 40), (B, (0.25, 0.50, 0.75, 0.97), -8, 36), (C, (0.45, 0.80, 1.0), -6, 26)):
        for j, f in enumerate(fs):
            q = along(c, f)
            shrink = 1.0 - 0.25 * f
            pads.append((q[0] - rx0 * 0.15, q[1] + dy, rx0 * shrink * rng.uniform(0.9, 1.15), rx0 * 0.34 * shrink))
            if rng.random() < 0.65:
                pads.append((q[0] + rng.uniform(-14, 6), q[1] + dy + rx0 * 0.42, rx0 * 0.62 * shrink, rx0 * 0.24 * shrink))
    pads += [(at(14)[0] - 22, at(14)[1] + 4, 30, 11), (at(13)[0] + 30, at(13)[1] + 8, 32, 11), (at(11)[0] + 30, at(11)[1] - 6, 22, 9), (T[-1][0] - 6, T[-1][1] + 2, 20, 8)]
    pads = [p for p in pads if p[0] - p[2] > 456 or p[1] - p[3] < -2]            # (never over the cap of cloud)
    for (cx, cy, rx, ry) in sorted(pads, key=lambda p: -p[1]):
        pad(L, S, rng, cx, cy, rx, ry, needle=12.0)
    sc, sa = S.done()
    L.add(sc, sa)
    c, a = L.done()
    # ---- nothing at the right edge below row 262 (Okitsu, the temple, whoever stands at `okitsu`)
    x, y = grid(SHAPE)
    keep = 1 - ((y > 256) * (x > 600)).astype(F32)
    a = a * keep
    # ---- the morning sun along the upper left edges: a warm rim, most on the trunk and the limbs
    a_hard = (a > 0.5).astype(F32)
    rim = D.rim(a_hard, light=(-1.0, -0.6), width=2.2)
    lum_ = c @ np.array([0.3, 0.55, 0.15], dtype=F32)
    warm = np.clip(c * 2.3 + np.array([0.20, 0.13, 0.02], dtype=F32), 0, 1)
    c = lerp(c, warm, (np.clip(rim * 1.1, 0, 1) * (lum_ < 0.42))[..., None])
    c = grade_cut(c, a, 0.94, lightfrom=(-1.0, -0.6), seed=seed, uneven=0.06)
    return c.astype(F32), np.clip(a, 0, 1)          # (no brush pass: it is all needle ends, and a brush would carry the sky into its gaps)


def lip_top(x):
    """The row of the cutting's lip at column x: low along the left (under the feet of the three where they come up),
    higher through the middle, rising in the bottom right corner into the rock shoulder."""
    v = 590.0 - 3.0 * math.sin(x / 37.0 + 0.4) ** 2 - 2.0 * math.sin(x / 13.0) ** 2
    if x > 140:
        v -= 14.0 * min(1.0, (x - 140) / 140.0)
    if x > 590:
        v -= ((x - 590) / 210.0) ** 1.3 * 46.0
    return v


#        middle x, half width, height (px): the mountain's rock breaking through the lip
ROCKS = [(252.0, 30.0, 14.0), (342.0, 15.0, 8.0), (452.0, 30.0, 16.0), (566.0, 18.0, 10.0), (652.0, 24.0, 12.0), (770.0, 56.0, 20.0), (712.0, 26.0, 12.0)]


def rock(L, cx, base, hw, hgt, rng):
    """A rock of the cutting's lip: an angular top in two or three facets, the ones turned up and to the left catching
    a little light, the rest dark; cracks along its bedding and down it."""
    n = 7
    xs_ = np.linspace(cx - hw, cx + hw, n)
    tops = [base - hgt * (0.35 + 0.65 * math.sin(math.pi * (i / (n - 1))) ** 0.7) * rng.uniform(0.8, 1.1) for i in range(n)]
    outline = [(float(xx), float(tt)) for xx, tt in zip(xs_, tops)]
    body = [(cx - hw - 3, base + 10)] + outline + [(cx + hw + 3, base + 10)]
    L.poly(body, ROCK_MID, ROCK_DARK, g=((cx - hw, base - hgt), (cx + hw * 0.5, base + 8)))
    # the facets turned to the light: the left part of the top, a band under each top point
    for i in range(n - 1):
        a_, b_ = outline[i], outline[i + 1]
        if b_[1] < a_[1] or i < n // 2:                                    # rising to the right: it faces up and left
            d = hgt * rng.uniform(0.25, 0.45)
            L.poly([a_, b_, (b_[0] - 1.5, b_[1] + d), (a_[0] - 1.0, a_[1] + d * 0.8)], ROCK_LIT, lerp(ROCK_LIT, ROCK_MID, 0.7), g=(a_, (a_[0], a_[1] + d)), alpha=0.9)
    for j in range(max(2, int(hw / 10))):
        fx_ = cx + rng.uniform(-hw * 0.75, hw * 0.75)
        fy_ = base - hgt * rng.uniform(0.15, 0.6)
        L.line([(fx_, fy_), (fx_ + rng.normal(0, 2.5), fy_ + rng.uniform(5, 12))], lerp(ROCK_DARK, rgb("#0e0a14"), 0.5), rng.uniform(0.8, 1.4), 0.75)
    for v in (0.4, 0.7):
        pts_ = [(cx - hw * 0.85 + 2 * hw * 0.85 * u, base - hgt * v * (0.5 + 0.5 * math.sin(math.pi * u)) + 1.5 * math.sin(u * 7.0)) for u in np.linspace(0, 1, 8)]
        L.line(pts_, lerp(ROCK_DARK, rgb("#0e0a14"), 0.3), 0.9, 0.45)


def sasa(L, cx, top, n, ln0, rng, sun=0.35, spread=26.0):
    """A clump of sasa (bamboo grass) on the lip, near the lens: canes up from below the frame, each with a fan of broad
    pointed leaves at its top, swept to the left by the wind and hanging by their own weight; dark, in the shade, their
    edges bleached pale as they are at the end of winter, now and then a leaf with the sun on it."""
    order = sorted(range(n), key=lambda i: rng.random())
    for i in order:
        x0 = cx + rng.normal(0, spread * 0.45)
        tip_y = top + rng.uniform(-3, 9)
        foot_y = lip_top(x0) + 6                                               # (the cane comes up out of the turf)
        cane = curve([(x0 + rng.normal(0, 2), foot_y), (x0 + rng.normal(0, 1.5), (tip_y + foot_y) / 2), (x0, tip_y)], 5)
        L.taper(cane, GRASS_DARK, 2.4, 1.6)
        for j in range(min(5, len(cane) - 1)):
            at_ = cane[-1 - j]
            an = math.pi + rng.uniform(-0.55, 0.30) if rng.random() < 0.75 else rng.uniform(-0.35, 0.15)     # most of them to the left, with the wind
            ln = ln0 * rng.uniform(0.75, 1.05) * (1 - 0.08 * j)
            leaf(L, at_, an, ln, ln * rng.uniform(0.26, 0.34), rng.random() < sun)
        leaf(L, cane[-1], -math.pi / 2 - 0.9 + rng.uniform(-0.3, 0.3), ln0 * 0.6, ln0 * 0.22, rng.random() < sun)


def leaf(L, base, an, ln, wd, lit):
    """One broad pointed leaf of sasa (Yui's), hanging a little by its own weight."""
    dx, dy = math.cos(an), math.sin(an)
    nx_, ny_ = -dy, dx
    droop = 0.28 * ln * abs(dx)
    tip = (base[0] + dx * ln, base[1] + dy * ln + droop)
    m1 = (base[0] + dx * ln * 0.30, base[1] + dy * ln * 0.30 + droop * 0.08)
    m2 = (base[0] + dx * ln * 0.66, base[1] + dy * ln * 0.66 + droop * 0.42)

    def shape(k_):
        return [base, (m1[0] + nx_ * wd * 0.5 * k_, m1[1] + ny_ * wd * 0.5 * k_), (m2[0] + nx_ * wd * 0.40 * k_, m2[1] + ny_ * wd * 0.40 * k_), tip,
                (m2[0] - nx_ * wd * 0.40 * k_, m2[1] - ny_ * wd * 0.40 * k_), (m1[0] - nx_ * wd * 0.5 * k_, m1[1] - ny_ * wd * 0.5 * k_)]
    L.poly(shape(1.0), STRAW_LIT if lit else lerp(STRAW_LIT, GRASS_DARK, 0.55))
    L.poly(shape(0.70), GRASS_MID if lit else GRASS_DARK, GRASS_DARK, g=(base, tip))
    L.line([base, m1, m2, tip], lerp(GRASS_MID, STRAW_LIT, 0.35) if lit else GRASS_MID, 0.8, 0.7)


def front_cut(back, seed, fast=False):
    """front.png: the lip of the cutting along the bottom: turf, the rock breaking through it, grass flattened by the
    wind, the shoulder of rock and its pampas grass in the bottom right corner. -> (colour, cover)."""
    L = Wet(SHAPE)
    S = Sheet(SHAPE)
    rng = np.random.default_rng(seed)
    xs = np.arange(-4.0, 806.0, 4.0)
    top = [(float(x_), lip_top(x_) + rng.normal(0, 0.8)) for x_ in xs]
    L.poly([(-4, 604)] + top + [(806, 604)], TURF, TURF_DEEP, g=((0, 560), (0, 600)))
    # the rock breaking through the turf
    for (cx, hw, hgt) in ROCKS:
        rock(L, cx, lip_top(cx) + 4, hw, hgt, rng)

    def blade(x0, y0, ln, lean, tone, w=2.0, droop=0.0):
        """One blade, up from (x0, y0) and flattened over to the left by the wind (lean < 0): it leaves the turf at a
        slant, rises to a little under half its length and streams away low, its tip dipping (`droop`)."""
        up = math.sqrt(max(0.05, 1 - lean * lean))
        h_ = ln * (0.20 + 0.55 * up)
        pts_ = curve([(x0, y0), (x0 + lean * ln * 0.30, y0 - h_ * 0.80), (x0 + lean * ln * 0.70, y0 - h_), (x0 + lean * ln, y0 - h_ + droop * ln * 0.22)], 6)
        S.line(pts_, tone, w, 1.0)
        return pts_
    # the turf: short grass all along the lip, flattened to the left
    for x_ in np.arange(-2.0, 804.0, 2.0):
        ln = rng.uniform(4, 11) * (0.6 if x_ < 170 else 1.0)
        lean = rng.uniform(-0.95, -0.35)
        blade(x_ + rng.normal(0, 1), lip_top(x_) + 3, ln, lean, GRASS_DARK if rng.random() < 0.7 else GRASS_MID, w=1.4)
    # sasa in clumps along the lip, near the lens (a leaf is a finger's length of the picture), clear of the three's feet
    # at the left and of Mosuke's stand at (540, 562)
    for (cx, n, rise, ln0) in ((214, 9, 8, 24), (300, 7, 7, 22), (402, 11, 11, 28), (488, 7, 7, 22), (612, 11, 12, 28), (690, 11, 14, 30), (748, 9, 18, 32)):
        sasa(L, cx, lip_top(cx) - rise, n, ln0, rng, spread=34.0)
    # tufts of wiry grass along it: longer, combed flat to the left by the wind, their tips catching the sun
    for (cx, n, tall) in ((180, 8, 20), (256, 10, 24), (350, 9, 22), (446, 9, 22), (536, 10, 20), (580, 8, 22), (652, 10, 28), (30, 6, 11), (110, 7, 12)):
        for i in range(n):
            lean = float(np.clip(rng.normal(-0.86, 0.08), -0.99, -0.62))
            ln = tall * rng.uniform(0.6, 1.0)
            x0 = cx + rng.normal(0, 7)
            q = rng.random()
            tone = STRAW_LIT if q < 0.16 else (STRAW_DARK if q < 0.40 else (GRASS_MID if q < 0.7 else GRASS_DARK))
            blade(x0, lip_top(x0) + 4, ln, lean, tone, w=rng.uniform(1.4, 2.2), droop=0.25)
    # the pampas grass on the rock shoulder: last year's long blades streaming left in the wind, two bleached stalks
    for i in range(34):
        x0 = 770 + rng.normal(0, 16)
        lean = float(np.clip(rng.normal(-0.92, 0.05), -0.99, -0.78))
        q = rng.random()
        blade(x0, lip_top(x0) + 2, 70 * rng.uniform(0.45, 1.0), lean, STRAW_DARK if q < 0.50 else (GRASS_DARK if q < 0.70 else (STRAW_LIT if q < 0.85 else GRASS_MID)), w=rng.uniform(1.6, 2.6), droop=0.2)
    for (x0, ln) in ((770.0, 78.0), (792.0, 66.0)):
        p_ = blade(x0, lip_top(x0) + 4, ln, -0.93, STRAW_LIT, w=1.4, droop=0.4)
        for q in p_[-4:]:
            S.line([q, (q[0] - 5.0, q[1] + 2.0)], STRAW_LIT, 1.0, 0.8)
    sc, sa = S.done()
    L.add(sc, sa)
    c, a = L.done()
    # ---- flecks of sun: on the rock tops and the grass tips along its upper left edges
    a_hard = (a > 0.5).astype(F32)
    rim = D.rim(a_hard, light=(-1.0, -0.6), width=1.8)
    x, y = grid(SHAPE)
    fleck = step(0.55, 0.70, noise(SHAPE, (26, 10), seed + 4, 3))
    c = lerp(c, np.clip(c * 1.9 + np.array([0.16, 0.11, 0.02], dtype=F32), 0, 1), (np.clip(rim, 0, 1) * (0.35 + 0.65 * fleck) * 0.85)[..., None])
    c = grade_cut(c, a, 0.92, lightfrom=(-1.0, -0.8), seed=seed, uneven=0.05)
    return c.astype(F32), np.clip(a, 0, 1)

"""The castle approach at Himeji (edo-castle), round twenty-three (DEPTH.md): the NEAR plane, near.png (`plane: "front"`,
last in the scene's `planes`): what stands within a few metres of the lens, between us and the play. People always pass
behind it.

WHERE WE STAND   The eye is 3.26 m above the road (the scene's camera, unchanged), on the far side of the road from the
castle, at the stone edge of the moat that runs along it. So what is near us is:

  the cherry      the old double cherry is on the bank 10 m off (cherry.png, its trunk and crown as round twenty drew
                  them). An old tree spreads five or six metres: its crown reaches out over the road toward us. One great
                  limb leans in up the left edge (as thick as a trunk there: it is 5 to 7 m from the lens), its lower end
                  lost in a cluster of near blossom; boughs go from it across the top-left, heavy with double blossom, the
                  clusters a hand's breadth of the picture. Seen from under them they are in their own shade: deep rose
                  and mauve, lit only along the edges that face the low sun on the right. They stop short of the keep (its
                  top, x 360, row 34, is where the herons look) and of the cherry's own crown's right side.
  the pine        the old pine on the road's verge beyond the right edge (edo_castle_model.TREE: its shadow lies across the
                  ramp): the tips of its lowest bough reach into the top-right corner, dark pads of needles, high over the
                  gate tower.
  the moat        its stone edge under our feet: the coping's top along the bottom of the frame, granite, petals fallen on
                  it; reeds and rushes up from the water at both corners (last year's straw among the new green), low
                  clumps between them. Never over the road where people stand.

Nothing here is clicked or stood on behind it (depth_check.py). No small holes of sky inside the dark masses (the paints
key a speck of light shut in by darks as a highlight). No brush pass: it is all blades, needles and petals.
"""

import math

import numpy as np

from brush import *
import depth as D
from edo_village_kit import (COBALT, CERULEAN, LAKE, NAPLES, OCHRE, PRUSSIAN, SIENNA, ULTRA, VERONESE, VIRIDIAN, WPAPER, Wet,
                             grade_cut, mixp, thin)
from edo_village_kit import P as PAINT
from edo_castle_kit import H, SHAPE, W
import edo_castle_model as MD

LILAC = PAINT("lilac")
BARK_DARK = lerp(mixp(SIENNA, PRUSSIAN, 0.42), rgb("#24140f"), 0.46)          # the near darks: deep, and frankly warm (the key cools them)
BARK_MID = lerp(mixp(SIENNA, PRUSSIAN, 0.30), rgb("#24140f"), 0.14)
BARK_LIT = lerp(mixp(OCHRE, SIENNA, 0.40), NAPLES, 0.25)
BARK_COOL = lerp(BARK_MID, thin(mixp(COBALT, LILAC, 0.4), 0.3), 0.36)
LILAC_ = PAINT("lilac")
ROSE_DEEP = lerp(lerp(mixp(LAKE, SIENNA, 0.30), rgb("#3a2434"), 0.55), LILAC_, 0.16)   # blossom in its own shade, seen from under it
ROSE = lerp(lerp(thin(LAKE, 0.30), LILAC_, 0.14), rgb("#3a2434"), 0.30)
ROSE_HALF = lerp(lerp(thin(LAKE, 0.52), LILAC_, 0.10), rgb("#3a2434"), 0.08)
ROSE_LIT = lerp(WPAPER, mixp(LAKE, NAPLES, 0.40), 0.30)                        # the rims the low sun reaches
LEAF_BRONZE = lerp(mixp(SIENNA, LAKE, 0.30), rgb("#2a1416"), 0.34)            # the double cherry's young leaves, bronze-red
LEAF_LIT = lerp(mixp(OCHRE, SIENNA, 0.45), NAPLES, 0.25)
NEEDLE_DARK = lerp(mixp(VIRIDIAN, PRUSSIAN, 0.70), rgb("#161a24"), 0.40)
NEEDLE_MID = lerp(mixp(VIRIDIAN, PRUSSIAN, 0.52), rgb("#161a24"), 0.15)
NEEDLE_LIT = lerp(mixp(VERONESE, OCHRE, 0.30), PRUSSIAN, 0.28)
REED_DARK = lerp(mixp(VIRIDIAN, OCHRE, 0.38), rgb("#141820"), 0.50)
REED_MID = lerp(mixp(VIRIDIAN, OCHRE, 0.50), PRUSSIAN, 0.36)
STRAW_DARK = lerp(mixp(OCHRE, SIENNA, 0.40), rgb("#1c1418"), 0.46)
STRAW_LIT = thin(mixp(OCHRE, NAPLES, 0.45), 0.22)
GRANITE = lerp(thin(mixp(COBALT, SIENNA, 0.30), 0.40), rgb("#2a2430"), 0.35)
GRANITE_TOP = lerp(thin(mixp(OCHRE, COBALT, 0.40), 0.45), rgb("#2a2430"), 0.18)
MOSS = lerp(mixp(VIRIDIAN, OCHRE, 0.45), PRUSSIAN, 0.40)
PETAL = thin(LAKE, 0.60)
PETAL_LIT = thin(LAKE, 0.80)


def limb(L, pts, w0, w1, rng, lit=True):
    """A limb of the old cherry: dark, never straight, its bark ringed with pale bands (cherry bark is so), rough, the
    low sun along its right-hand side."""
    c = curve(pts, 14 if w1 > 30 else 10)
    n = len(c)
    L.taper(c, BARK_DARK, w0, w1)
    side = []
    for i in range(n):                                                          # each point's normal, pointing right (toward the sun)
        ax, ay = c[max(i - 1, 0)]
        bx, by = c[min(i + 1, n - 1)]
        d = math.hypot(bx - ax, by - ay) or 1
        nx_, ny_ = -(by - ay) / d, (bx - ax) / d
        if nx_ < 0:
            nx_, ny_ = -nx_, -ny_
        side.append((nx_, ny_, (w0 + (w1 - w0) * i / (n - 1)) / 2))
    if lit:
        L.taper([(px_ + nx_ * w * 0.45, py_ + ny_ * w * 0.45) for (px_, py_), (nx_, ny_, w) in zip(c, side)], BARK_MID, w0 * 0.42, w1 * 0.40, alpha=0.85)
        i = 0
        while i < n - 1:                                                       # the sun along its right side: broken, in short touches
            j = min(n - 1, i + int(rng.integers(2, 5)))
            if rng.random() < 0.6:
                L.line([(c[k][0] + side[k][0] * side[k][2] * 0.84, c[k][1] + side[k][1] * side[k][2] * 0.84) for k in range(i, j + 1)],
                       lerp(BARK_LIT, BARK_MID, rng.uniform(0.2, 0.55)), max(0.8, min(w0, w1) * 0.09), 0.55)
            i = j + int(rng.integers(0, 3))
    step_ = max(1, n // max(4, int(sum(math.hypot(c[i + 1][0] - c[i][0], c[i + 1][1] - c[i][1]) for i in range(n - 1)) / 7)))
    for i in range(1, n - 1, step_):                                            # the lenticels: pale bands across the bark
        nx_, ny_, w = side[i]
        if rng.random() < 0.8:
            f0, f1 = rng.uniform(-0.9, -0.3), rng.uniform(0.2, 0.85)
            L.line([(c[i][0] + nx_ * w * f0, c[i][1] + ny_ * w * f0), (c[i][0] + nx_ * w * f1, c[i][1] + ny_ * w * f1)], BARK_COOL, max(0.6, w * 0.09), 0.6)
    if w1 > 30:                                                                 # a great limb's rough bark: cracks along it
        for k in range(int(n * 1.5)):
            i = int(rng.integers(1, n - 2))
            nx_, ny_, w = side[i]
            f = rng.uniform(-0.7, 0.5)
            p0 = (c[i][0] + nx_ * w * f, c[i][1] + ny_ * w * f)
            p1 = (c[i + 1][0] + nx_ * w * f + rng.normal(0, 1), c[i + 1][1] + ny_ * w * f)
            L.line([p0, p1], lerp(BARK_DARK, rgb("#0e0a14"), 0.5), rng.uniform(0.8, 1.6), 0.7)
    return c


def cluster(L, rng, cx, cy, r, sun=0.5, hang=1.0):
    """A cluster of double blossom seen from under it: first its mass (the flowers crowded together, in their own shade),
    then the flowers that show on it, lighter on the side toward the low sun (right, a little up), each a ruffled round;
    a few young bronze leaves at its edges. No holes of sky inside it."""
    n = max(5, int(r * r / 30))
    discs = []
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        rr = math.sqrt(rng.random())
        fx = cx + math.cos(a) * r * rr * 0.92
        fy = cy + math.sin(a) * r * rr * 0.70 + r * 0.22 * hang * rr * max(math.sin(a), 0)
        discs.append((fx, fy, r * rng.uniform(0.24, 0.36)))
    for (fx, fy, fr) in discs:                                                  # the mass
        L.ellipse(fx, fy, fr * 1.05, fr * 0.95, ROSE_DEEP)
    for j in range(int(rng.integers(1, 3))):                                    # young bronze leaves at its edges
        a = rng.uniform(-math.pi * 0.95, 0.3)
        lx, ly = cx + math.cos(a) * r * 0.70, cy + math.sin(a) * r * 0.50
        ln, wd = r * rng.uniform(0.40, 0.65), r * rng.uniform(0.12, 0.18)
        an = a + rng.uniform(-0.5, 0.5)
        tip = (lx + math.cos(an) * ln, ly + math.sin(an) * ln)
        nx_, ny_ = -math.sin(an), math.cos(an)
        mid = ((lx + tip[0]) / 2, (ly + tip[1]) / 2)
        L.poly([(lx, ly), (mid[0] + nx_ * wd, mid[1] + ny_ * wd), tip, (mid[0] - nx_ * wd, mid[1] - ny_ * wd)],
               LEAF_LIT if (math.cos(an) > 0.3 and rng.random() < sun) else LEAF_BRONZE)
    discs.sort(key=lambda d: (d[1] - cy) * 0.6 - (d[0] - cx))                  # the lit ones last
    for i, (fx, fy, fr) in enumerate(discs):                                    # the flowers that show
        u = ((fx - cx) * 0.85 - (fy - cy) * 0.45) / r                           # toward the sun
        if u < -0.35 and rng.random() < 0.6:
            continue
        tone = ROSE_LIT if (u > 0.45 and rng.random() < sun) else (ROSE_HALF if u > 0.1 else ROSE)
        k = 0.78 if tone is ROSE else 0.86
        ring = [(fx + math.cos(t) * fr * k * (1 + 0.13 * math.sin(6 * t + i)), fy + math.sin(t) * fr * k * 0.88 * (1 + 0.13 * math.sin(6 * t + i))) for t in np.linspace(0, 2 * math.pi, 15)[:-1]]
        L.poly(ring, tone)
        if fr > 2.4:
            arc = [(fx + math.cos(t) * fr * 0.45, fy + 0.2 * fr + math.sin(t) * fr * 0.36) for t in np.linspace(0.2, 2.9, 6)]
            L.line(arc, lerp(tone, ROSE_DEEP, 0.45), max(0.5, fr * 0.12), 0.7)       # the ruffle of the double flower


def pine_pad(L, rng, cx, cy, rx, ry, needle=11.0, lit=0.35):
    L.ellipse(cx, cy + ry * 0.12, rx * 0.9, ry * 0.78, NEEDLE_DARK)
    n = max(7, int(rx * ry / 8.0))
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        rr = math.sqrt(rng.random()) if i % 3 else 1.0
        px_, py_ = cx + math.cos(a) * rx * rr * 0.95, cy + math.sin(a) * ry * rr * 0.9
        out = math.atan2((py_ - cy) / max(ry, 1), (px_ - cx) / max(rx, 1))
        mid = math.atan2(0.55 * math.sin(out) - 0.45, 0.55 * math.cos(out))
        facing = math.cos(out) * 0.9 - math.sin(out) * 0.3
        is_lit = facing > 0.5 and rr > 0.8 and rng.random() < lit
        tone = NEEDLE_LIT if is_lit else (NEEDLE_MID if rng.random() < 0.3 else NEEDLE_DARK)
        for j in range(int(rng.uniform(8, 13))):
            an = mid + rng.uniform(-1.2, 1.2)
            ln = needle * rng.uniform(0.6, 1.1)
            L.line([(px_, py_), (px_ + math.cos(an) * ln, py_ + math.sin(an) * ln)], tone, rng.uniform(0.8, 1.2), 0.95)


def blade(L, x0, y0, ln, lean, tone, w=2.4, droop=0.0):
    tx = x0 + lean * ln
    ty = y0 - ln * math.sqrt(max(0.06, 1 - lean * lean)) + droop * abs(lean) * ln * 0.5
    pts = curve([(x0, y0), (x0 + lean * ln * 0.22, y0 - ln * 0.60), (x0 + lean * ln * 0.70, y0 - ln * 0.93 + droop * abs(lean) * ln * 0.12), (tx, ty)], 6)
    L.taper(pts, tone, w, 0.45)
    return pts


def near_cut(back, info, seed, fast=False):
    """near.png -> (colour, cover)."""
    rng = np.random.default_rng(seed)
    L = Wet(SHAPE)
    # ---------------- the old cherry's great limb, up the left edge (it leans in toward us from the fork behind): bare bark
    # from where it comes out of the near blossom, so that it reads as the trunk it nearly is
    # (it leaves the trunk going left, out of the picture, and comes back in toward us: in at the left edge, up, and out at the top)
    great = [(-34, 480), (-8, 418), (14, 352), (22, 300), (36, 248), (30, 190), (16, 136), (14, 84), (-2, 28), (-20, -16)]
    limb(L, great, 44, 72, rng)
    for (kx, ky, kr) in ((30, 252, 9), (16, 118, 7)):                           # knots where limbs were lost
        L.ellipse(kx + 6, ky, kr, kr * 0.7, lerp(BARK_DARK, rgb("#0e0a14"), 0.4))
        L.ellipse(kx + 7.5, ky - 1, kr * 0.55, kr * 0.38, BARK_COOL, alpha=0.7)
    L.taper(curve([(14, 300), (-6, 284), (-24, 270)], 6), BARK_DARK, 20, 14)                  # a stub of a limb going off to the left
    # boughs from it across the top-left: the near ones heavy, the ones reaching back toward the crown thinner
    b1 = limb(L, [(30, 150), (66, 128), (100, 92), (136, 86), (170, 58), (206, 52), (236, 26), (268, 18), (290, 2), (304, -8)], 30, 10, rng)
    b2 = limb(L, [(10, 70), (44, 54), (70, 30), (108, 30), (140, 8), (172, 4), (196, -8)], 36, 18, rng)
    b3 = limb(L, [(118, 90), (130, 112), (158, 122), (174, 140), (196, 146)], 11, 4, rng)
    b4 = limb(L, [(170, 58), (184, 82), (214, 88), (232, 104), (250, 104)], 9, 3.5, rng)
    b5 = limb(L, [(30, 246), (70, 228), (108, 216), (138, 220)], 16, 5, rng)
    b6 = limb(L, [(206, 48), (232, 62), (258, 70), (276, 70)], 7, 3, rng)
    twigs = []
    for path in (b1, b2, b3, b4, b5, b6):
        for i in range(2, len(path) - 1, 3):
            a = rng.uniform(0.4, 2.5)
            ln = rng.uniform(14, 30)
            p = path[i]
            q = (p[0] + math.cos(a) * ln, p[1] + math.sin(a) * ln)
            L.line([p, ((p[0] + q[0]) / 2 + rng.normal(0, 2), (p[1] + q[1]) / 2), q], BARK_DARK, rng.uniform(1.5, 3.0))
            twigs.append(q)
    # the blossom: clusters hanging along the boughs and at the twigs' ends; the nearest the biggest. The limb's lower
    # length stays bare; its foot is lost in one cluster.
    spots = [(132, 216, 24), (152, 200, 16), (110, 228, 14), (58, 236, 18),
             (92, 124, 28), (136, 98, 26), (182, 70, 28), (226, 46, 24), (262, 28, 20), (290, 12, 15), (198, 132, 20),
             (236, 104, 18), (266, 82, 14), (44, 44, 32), (102, 24, 30), (152, 6, 26), (20, 130, 18), (204, 152, 13)]
    for (cx, cy, r) in spots:
        cluster(L, rng, cx + rng.normal(0, 2), cy + rng.normal(0, 2), r, sun=0.42 if cx > 100 else 0.28)
    for q in twigs:
        if q[0] < 284 and q[1] < 240 and rng.random() < 0.7:
            cluster(L, rng, q[0], q[1] + 4, rng.uniform(10, 15), sun=0.36)
    # ---------------- the pine beyond the right edge: its lowest bough's tips at the top-right corner
    pl = curve([(830, 18), (790, 40), (748, 52), (712, 70), (684, 76)], 8)
    L.taper(pl, BARK_DARK, 14, 4)
    L.taper(curve([(804, 34), (790, 76), (776, 104), (770, 124)], 6), BARK_DARK, 6, 2.5)
    for (cx, cy, rx, ry) in ((790, 22, 46, 16), (742, 40, 38, 13), (700, 64, 30, 11), (668, 80, 22, 8), (778, 96, 26, 10),
                             (760, 128, 20, 8), (726, 16, 30, 10), (800, 64, 24, 10)):
        pine_pad(L, rng, cx, cy, rx, ry, needle=11.0, lit=0.4)
    # ---------------- the moat's stone edge along the bottom: the coping's top, granite, petals on it
    yb = 594.0
    xs = -6.0
    while xs < 806:
        ln = rng.uniform(60, 120)
        top_ = yb + rng.uniform(-0.8, 0.8)
        L.poly([(xs, 602), (xs + ln, 602), (xs + ln - 0.5, top_ + rng.uniform(-0.6, 0.6)), (xs + 0.5, top_)], GRANITE_TOP, GRANITE, g=((xs, top_), (xs, 602)))
        L.line([(xs + ln, top_ + 0.5), (xs + ln, 602)], lerp(GRANITE, rgb("#1a1422"), 0.4), 1.0, 0.9)
        L.line([(xs + 1, top_), (xs + ln - 1, top_ + 0.2)], lerp(GRANITE_TOP, NAPLES, 0.35), 0.7, 0.8)     # its lit lip
        if rng.random() < 0.5:
            L.ellipse(xs + rng.uniform(5, ln - 5), 600, rng.uniform(6, 14), 2.5, MOSS, alpha=0.8)
        xs += ln
    for i in range(70):                                                          # petals fallen on the stones
        px_ = rng.uniform(-4, 804)
        if rng.random() > 0.35 + 0.65 * math.exp(-((px_ - 120) / 260.0) ** 2):
            continue
        L.ellipse(px_, rng.uniform(595.5, 599.5), rng.uniform(1.0, 1.8), rng.uniform(0.6, 1.0), PETAL_LIT if rng.random() < 0.5 else PETAL)
    # ---------------- reeds and rushes up from the water: tall at both corners, low clumps between
    def reed_clump(x0, x1, tall, n, base=604.0, straw=0.35):
        for i in range(n):
            bx = rng.uniform(x0, x1)
            lean = float(np.clip(rng.normal(0, 0.28), -0.75, 0.75))
            ln = tall * rng.uniform(0.45, 1.0)
            is_straw = rng.random() < straw
            tone = (STRAW_LIT if (lean > 0.15 and rng.random() < 0.3) else STRAW_DARK) if is_straw else (REED_MID if rng.random() < 0.22 else REED_DARK)
            blade(L, bx, base, ln, lean, tone, w=rng.uniform(1.6, 3.0) if not is_straw else rng.uniform(1.2, 2.0), droop=0.6 if not is_straw else 0.0)
            if is_straw and rng.random() < 0.25 and ln > 40:                    # a seed head on last year's stalk
                tip = (bx + lean * ln, base - ln * math.sqrt(max(0.06, 1 - lean * lean)))
                L.taper([tip, (tip[0] + lean * 6, tip[1] - 9)], STRAW_DARK, 2.6, 1.0)
    reed_clump(-8, 40, 128, 34, straw=0.40)
    reed_clump(20, 70, 84, 22, straw=0.35)
    reed_clump(60, 92, 34, 10, straw=0.3)
    reed_clump(752, 808, 132, 36, straw=0.40)
    reed_clump(716, 770, 80, 20, straw=0.35)
    reed_clump(690, 724, 30, 8, straw=0.3)
    for (x0, x1) in ((150, 230), (322, 372), (476, 520), (598, 640)):
        reed_clump(x0, x1, 16, 12, base=600.0, straw=0.3)
    c, a = L.done()
    # ---------------- the low sun along the right-hand edges: a warm rim, most on the limbs; the rest stays in shade
    a_hard = (a > 0.5).astype(F32)
    rim = D.rim(a_hard, light=(1.0, -0.35), width=2.0)
    lum_ = c @ np.array([0.3, 0.55, 0.15], dtype=F32)
    warm = np.clip(c * 2.1 + np.array([0.18, 0.11, 0.03], dtype=F32), 0, 1)
    c = lerp(c, warm, (np.clip(rim * 1.05, 0, 1) * (lum_ < 0.42))[..., None])
    c = grade_cut(c, a, 0.92, lightfrom=(1.0, -0.4), seed=seed, uneven=0.06)
    return c.astype(F32), np.clip(a, 0, 1)

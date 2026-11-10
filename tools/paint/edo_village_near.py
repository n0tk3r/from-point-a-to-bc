"""PAINT-23A (round twenty-three, DEPTH.md): the NEAR plane of Yui (edo-village): what stands within a few metres of
the lens, between us and the play. People always pass behind it (`plane: "front"`).

WHERE WE STAND   The eye is 3.2 m above the beach (the scene's camera, unchanged): we are on the grassy bank at the foot
of the hill, on the inland side of the Tokaido at the east end of the village, under the black pines of the shore road.
So what is near us is:

  near.png    the PINE: its trunk leaning in up the left side (rooted on the bank below the frame, about 5.8 m from the
              lens: 46 cm thick there, a hand's breadth of the picture), a broken stub, two limbs and their pads of
              needles across the top left corner, one sprig hanging in front of Fuji's far left flank; a bough of the
              NEXT PINE of the row reaching in at the top right, over the Satta headland; and the BANK'S LIP along the
              bottom from the road's edge to the hen yard's corner: sasa (bamboo grass: canes with broad pointed leaves,
              their edges bleached pale as they are at winter's end), a few blades of last year's pampas grass, two
              stones. The turf is 3 to 4 m from the lens: a leaf is a finger's length of the picture.
  front.png   round twenty's coil of rope and three net floats, bottom left: where they were, drawn again as a coil,
              lying on the bank's turf, which runs on under them to the picture's left edge (and in the pines' shade,
              as the ground beyond them now is).

All of it is a dark mass (the pines' own shade), warm in its darks, and lit only where the morning sun, behind us and to
the left, catches an edge: the trunk's left side, the left of each pad, the grass's tips. Outline before inside: gaps
of sky through the needles, a broken stub, blades against the bright sand; little drawn within.

Nothing here is clicked or picked up, and nothing clicked or stood on is behind it (depth_check.py): the trunk comes into
the frame above the big boat, the boughs lie over open sky and stop well short of Fuji's summit, the sasa stays below the
feet of whoever stands in the play, and runs out at the hen yard so that every hen is in plain sight.

Two things learned (for the scenes that follow): no small gaps of sky INSIDE a dark near mass (the game's paints key a
speck of light shut in by darks as a highlight: the pine came out sprinkled with white), and no brush pass on a cut-out
that is all needle ends and blades (the brush carries the colour behind it into every gap).
"""

import math

import numpy as np

from brush import *
import depth as D
from edo_village_kit import *

SHAPE = (H, W)
BARK_DARK = lerp(mixp(SIENNA, PRUSSIAN, 0.70), rgb("#1a1422"), 0.45)       # the near darks: deep, and warm
BARK_MID = lerp(mixp(SIENNA, PRUSSIAN, 0.56), rgb("#1a1422"), 0.15)
BARK_LIT = lerp(mixp(OCHRE, SIENNA, 0.42), NAPLES, 0.25)
BARK_COOL = lerp(BARK_MID, thin(mixp(COBALT, PRUSSIAN, 0.4), 0.3), 0.42)    # bark in shade that looks at the sky
NEEDLE_DARK = lerp(mixp(VIRIDIAN, PRUSSIAN, 0.70), rgb("#161a24"), 0.40)
NEEDLE_MID = lerp(mixp(VIRIDIAN, PRUSSIAN, 0.52), rgb("#161a24"), 0.15)
NEEDLE_LIT = lerp(mixp(VERONESE, OCHRE, 0.24), PRUSSIAN, 0.34)
GRASS_DARK = lerp(mixp(VIRIDIAN, OCHRE, 0.42), PRUSSIAN, 0.50)
GRASS_MID = lerp(mixp(VIRIDIAN, OCHRE, 0.50), PRUSSIAN, 0.26)
STRAW_DARK = lerp(mixp(OCHRE, SIENNA, 0.35), PRUSSIAN, 0.46)
STRAW_LIT = thin(mixp(OCHRE, NAPLES, 0.45), 0.18)

# the pine's trunk in the world (cm): rooted at ROOT, leaning to the right and a little away as it rises, never straight
ROOT = (-399.0, -300.0)


def trunk_at(hgt):
    """The trunk's middle at a height (cm) -> picture point, and its thickness there in px."""
    X = ROOT[0] + 0.31 * hgt + 9.0 * math.sin(hgt / 85.0)
    Z = ROOT[1] + 0.04 * hgt
    px_, py_ = gp(X, Z, hgt)
    return (px_, py_), (50.0 - 0.022 * hgt) * kz(Z)


def pad(L, S, rng, cx, cy, rx, ry, light=(-1.0, -0.5), needle=12.0, lit=0.5):
    """One pad of pine needles seen from below and behind: a flat dark mass, its edge all needle ends (tufts fanning
    up and out); only the tufts on the rim that faces the sun are a warmer, lighter green."""
    L.ellipse(cx, cy + ry * 0.12, rx * 0.90, ry * 0.78, NEEDLE_DARK)
    n = max(7, int(rx * ry / 7.5))
    ll = math.hypot(*light)
    for i in range(n):
        a = rng.uniform(0, 2 * math.pi)
        rr = math.sqrt(rng.random()) if i % 3 else 1.0                       # every third tuft sits on the rim
        px_, py_ = cx + math.cos(a) * rx * rr * 0.95, cy + math.sin(a) * ry * rr * 0.9
        out = math.atan2((py_ - cy) / max(ry, 1), (px_ - cx) / max(rx, 1))    # outward from the pad's middle
        up = -math.pi / 2
        mid = math.atan2(0.55 * math.sin(out) + 0.45 * math.sin(up) + (0.25 if math.sin(out) > 0.3 else 0), 0.55 * math.cos(out) + 0.45 * math.cos(up))
        facing = (math.cos(out) * light[0] + math.sin(out) * light[1]) / ll   # 1 where the rim faces the sun
        is_lit = facing > 0.45 and rr > 0.8 and rng.random() < lit
        tone = NEEDLE_LIT if is_lit else (NEEDLE_MID if rng.random() < 0.22 + 0.25 * max(facing, 0) else NEEDLE_DARK)
        for j in range(int(rng.uniform(9, 14))):
            an = mid + rng.uniform(-1.2, 1.2)
            ln = needle * rng.uniform(0.6, 1.12)
            S.line([(px_, py_), (px_ + math.cos(an) * ln, py_ + math.sin(an) * ln)], tone if (not is_lit or j % 3) else NEEDLE_MID, rng.uniform(0.8, 1.3), 0.95)
    # (No small gaps of sky are cut inside a pad: the game's paints key a speck of light shut in by darks as a highlight,
    # and the pine came out sprinkled with white. The sky shows between the pads and through the needle ends.)


def limb(L, pts, w0, w1, seed):
    """A limb: dark, never straight, the sun along its upper left."""
    c = curve(pts, 10)
    L.taper(c, BARK_DARK, w0, w1)
    L.taper([(px_ - 0.12 * w0, py_ - 0.22 * w0) for px_, py_ in c], BARK_MID, w0 * 0.42, w1 * 0.4, alpha=0.75)
    return c


def bark(L, rng, pts, widths):
    """The trunk: old black-pine bark in scales, deep cracks between them. One warm dark; only the scales on the
    sunward (left) edge catch the light, broken, never a ruled stripe."""
    n = len(pts)
    left, right = [], []
    for i, ((px_, py_), wd) in enumerate(zip(pts, widths)):
        ax, ay = pts[max(i - 1, 0)]
        bx, by = pts[min(i + 1, n - 1)]
        d = math.hypot(bx - ax, by - ay) or 1.0
        nx_, ny_ = -(by - ay) / d, (bx - ax) / d
        if nx_ > 0:
            nx_, ny_ = -nx_, -ny_                                          # the normal that points left
        left.append((px_ + nx_ * (wd / 2 + rng.normal(0, 1.2)), py_ + ny_ * (wd / 2)))
        right.append((px_ - nx_ * (wd / 2 + rng.normal(0, 1.2)), py_ - ny_ * (wd / 2)))
    L.poly(left + right[::-1], BARK_DARK)

    def at(i, f, g):                                                         # a place on the trunk: segment i, f across (0 left), g along
        lx = left[i][0] + (left[i + 1][0] - left[i][0]) * g
        ly = left[i][1] + (left[i + 1][1] - left[i][1]) * g
        rx_ = right[i][0] + (right[i + 1][0] - right[i][0]) * g
        ry_ = right[i][1] + (right[i + 1][1] - right[i][1]) * g
        return (lx + (rx_ - lx) * f, ly + (ry_ - ly) * f)
    for i in range(n - 1):
        wd = widths[i]
        for _ in range(26):                                                  # the scales: short lozenges, staggered
            f, g = rng.uniform(0.03, 0.97), rng.uniform(0, 1)
            ln = rng.uniform(0.25, 0.55)
            wf = rng.uniform(0.05, 0.10)
            g1 = min(1.0, g + ln)
            a_, b_ = at(i, f, g), at(i, f + rng.normal(0, 0.015), g1)
            mid = at(i, f, (g + g1) / 2)
            if f < 0.16:
                tone, al = lerp(BARK_LIT, BARK_MID, f / 0.16 * 0.7 + rng.uniform(0, 0.3)), 0.92
            elif f < 0.40:
                tone, al = lerp(BARK_MID, BARK_DARK, (f - 0.16) / 0.24), 0.75
            elif f > 0.84:                                                   # its far side turns to the open sky: a cool breath of light
                tone, al = lerp(BARK_DARK, BARK_COOL, (f - 0.84) / 0.16 * rng.uniform(0.6, 1.0)), 0.8
            else:
                tone, al = lerp(BARK_MID, BARK_DARK, 0.55 + 0.3 * rng.random()), 0.5
            w_pl = wd * wf
            L.taper([a_, (mid[0] + rng.normal(0, 0.6), mid[1]), b_], tone, w_pl * 0.45, w_pl, alpha=al)
        for _ in range(5):                                                   # the deep cracks between them
            f, g = rng.uniform(0.1, 0.95), rng.uniform(0, 0.6)
            a_, b_ = at(i, f, g), at(i, f + rng.normal(0, 0.03), min(1.0, g + rng.uniform(0.3, 0.6)))
            L.line([a_, ((a_[0] + b_[0]) / 2 + rng.normal(0, 1.0), (a_[1] + b_[1]) / 2), b_], lerp(BARK_DARK, rgb("#0e0a14"), 0.6), rng.uniform(0.8, 1.7), 0.85)
    return left, right


def near_cut(back, seed, info, fast=False):
    """near.png: the pine, the next pine's bough, the bank's lip. -> (colour, cover)."""
    L = Wet(SHAPE)
    S = Sheet(SHAPE)
    rng = np.random.default_rng(seed)
    # ---------------- the pine at the left: limbs first (they pass behind the trunk), then the trunk, then the pads
    hs = np.arange(150.0, 600.0, 22.0)
    pts = [trunk_at(h_)[0] for h_ in hs]
    wds = [trunk_at(h_)[1] for h_ in hs]
    at = lambda h_: trunk_at(h_)[0]
    t_a, t_b, t_c = at(498.0), at(418.0), at(352.0)
    limb(L, [t_a, (t_a[0] + 44, t_a[1] - 12), (t_a[0] + 92, t_a[1] - 8), (t_a[0] + 128, t_a[1] - 20), (t_a[0] + 148, t_a[1] - 16)], 20, 6, 1)
    limb(L, [(t_a[0] + 70, t_a[1] - 10), (t_a[0] + 100, t_a[1] + 10), (t_a[0] + 136, t_a[1] + 14)], 8, 3.5, 2)
    limb(L, [t_b, (t_b[0] + 40, t_b[1] - 20), (t_b[0] + 78, t_b[1] - 12), (t_b[0] + 108, t_b[1] - 22), (t_b[0] + 136, t_b[1] - 12)], 17, 5, 3)
    limb(L, [(t_b[0] + 62, t_b[1] - 15), (t_b[0] + 78, t_b[1] + 8), (t_b[0] + 100, t_b[1] + 22), (t_b[0] + 108, t_b[1] + 30)], 6, 2.5, 4)
    limb(L, [(t_a[0] - 6, t_a[1] - 30), (t_a[0] - 40, t_a[1] - 58), (t_a[0] - 70, t_a[1] - 62)], 13, 6, 5)       # a limb away to the left, out of the frame
    # the stub of a lost limb, low on the trunk: broken, bare
    stub = [t_c, (t_c[0] + 22, t_c[1] - 10), (t_c[0] + 36, t_c[1] - 20)]
    L.taper(curve(stub, 6), BARK_DARK, 12, 7)
    L.poly([(stub[2][0] - 4, stub[2][1] - 3), (stub[2][0] + 5, stub[2][1] - 8), (stub[2][0] + 2, stub[2][1] + 1), (stub[2][0] + 7, stub[2][1] + 3), (stub[2][0] - 1, stub[2][1] + 5)], BARK_DARK)
    L.line([(stub[0][0] + 6, stub[0][1] - 8), (stub[2][0] - 2, stub[2][1] - 5)], BARK_MID, 2.0, 0.8)
    bark(L, rng, pts, wds)
    #        middle x, y, half width, half height: the pads sit on and over the limbs; the lowest hangs before Fuji's far flank
    pads_left = [(t_a[0] - 52, t_a[1] - 70, 44, 16), (t_a[0] + 8, t_a[1] - 64, 40, 15), (t_a[0] + 66, t_a[1] - 36, 44, 16), (t_a[0] + 122, t_a[1] - 40, 38, 13),
                 (t_a[0] + 30, t_a[1] - 28, 28, 12), (t_a[0] + 118, t_a[1] + 12, 30, 10),
                 (t_a[0] + 70, t_a[1] - 74, 46, 13), (t_a[0] + 132, t_a[1] - 70, 36, 11),                       # hanging in from a limb above the frame
                 (t_b[0] + 52, t_b[1] - 36, 36, 13), (t_b[0] + 96, t_b[1] - 34, 30, 11), (t_b[0] + 132, t_b[1] - 22, 24, 9), (t_b[0] + 18, t_b[1] - 26, 22, 10),
                 (t_b[0] + 104, t_b[1] + 30, 24, 9), (t_b[0] + 74, t_b[1] + 6, 20, 8),
                 (t_a[0] - 78, t_a[1] - 26, 30, 11), (t_b[0] - 52, t_b[1] - 4, 26, 10)]                         # on the limb that goes off to the left
    for (cx, cy, rx, ry) in pads_left:
        pad(L, S, rng, cx, cy, rx, ry, needle=13.0)
    # ---------------- the next pine's bough, reaching in at the top right, over the headland
    limb(L, [(826, 22), (780, 44), (736, 52), (700, 74), (668, 72), (640, 84)], 17, 4, 6)
    limb(L, [(750, 50), (742, 76), (722, 92)], 6, 3, 7)
    limb(L, [(800, 34), (806, 70), (790, 96), (786, 122)], 7, 2.5, 8)
    for (cx, cy, rx, ry) in ((782, 20, 50, 17), (730, 32, 40, 14), (690, 56, 34, 12), (654, 68, 26, 10), (720, 96, 26, 9), (786, 104, 28, 10), (760, 62, 24, 9),
                             (632, 88, 20, 8), (790, 132, 22, 8), (676, 24, 30, 10)):
        pad(L, S, rng, cx, cy, rx, ry, needle=13.0, lit=0.3)
    # ---------------- the bank's lip along the bottom. The turf is 3 to 4 m from the lens and a metre and a half under it,
    # so what comes up into the picture is the top half-metre of last year's pampas grass: big blades, cut off by the
    # frame, arching over. Dark, in the pines' shade; where a fleck of sun falls on a clump its blades are straw.
    def hump(x_):
        u = float(np.clip((x_ - 192.0) / 380.0, 0, 1))
        hgt = 4.0 + 13.0 * max(0.0, math.sin(math.pi * u)) ** 0.55
        if x_ > 546:                                                         # it runs out under the hen yard: every hen stays in sight
            hgt = min(hgt, 3.0 + 8.0 * max(0.0, 1 - (x_ - 546) / 60.0))
        return 600.0 - hgt
    xs = np.arange(190.0, 616.0, 5.0)
    top = [(float(x_), float(hump(x_) + rng.normal(0, 1.4))) for x_ in xs]
    L.poly([(190, 602)] + top + [(616, 602)], lerp(GRASS_DARK, BARK_DARK, 0.40), lerp(GRASS_DARK, BARK_DARK, 0.80))
    for (sx_, sw, sh_) in ((276.0, 28.0, 14.0), (452.0, 20.0, 10.0)):                                      # stones in the turf
        sy = hump(sx_) + 5
        stone = [(sx_ - sw, sy + 6), (sx_ - sw * 0.8, sy - sh_ * 0.6), (sx_ - sw * 0.2, sy - sh_), (sx_ + sw * 0.5, sy - sh_ * 0.8), (sx_ + sw, sy - sh_ * 0.1), (sx_ + sw * 0.9, sy + 6)]
        L.poly(stone, lerp(mixp(PRUSSIAN, OCHRE, 0.22), BARK_DARK, 0.45), lerp(mixp(PRUSSIAN, SIENNA, 0.3), BARK_DARK, 0.8), g=((sx_ - sw, sy - sh_), (sx_ + sw, sy + 6)))
        L.poly([stone[1], stone[2], stone[3], (sx_ + sw * 0.2, sy - sh_ * 0.45), (sx_ - sw * 0.6, sy - sh_ * 0.3)], lerp(thin(mixp(PRUSSIAN, OCHRE, 0.35), 0.30), BARK_DARK, 0.25), alpha=0.9)

    def blade(x0, y0, ln, lean, tone, w=3.0, droop=0.0):
        """One blade: up from (x0, y0), arching over to the side it leans to, its tip drooping if it is long."""
        tx = x0 + lean * ln
        ty = y0 - ln * math.sqrt(max(0.06, 1 - lean * lean)) + droop * abs(lean) * ln * 0.5
        pts_ = curve([(x0, y0), (x0 + lean * ln * 0.22, y0 - ln * 0.60), (x0 + lean * ln * 0.70, y0 - ln * 0.93 + droop * abs(lean) * ln * 0.12), (tx, ty)], 6)
        L.taper(pts_, tone, w, 0.5)
        return pts_
    # turf: short grass all along the lip
    for x_ in np.arange(192.0, 612.0, 2.2):
        ln = rng.uniform(5, 13) * (0.5 if x_ > 552 else 1.0)
        blade(x_ + rng.normal(0, 1), hump(x_) + 2, ln, rng.uniform(-0.55, 0.55), GRASS_DARK if rng.random() < 0.72 else GRASS_MID, w=1.5)
    # sasa (bamboo grass) at our feet: canes coming up from below the frame, each with a fan of broad pointed leaves,
    # dark, their edges bleached pale as they are at the end of winter. Near the lens: a leaf is a finger's length of
    # the picture. Lower and smaller toward the hen yard.
    def leaf(base, an, ln, wd, lit):
        dx, dy = math.cos(an), math.sin(an)
        nx_, ny_ = -dy, dx
        droop = 0.30 * ln * abs(dx)                                         # a broad leaf hangs by its own weight
        tip = (base[0] + dx * ln, base[1] + dy * ln + droop)
        m1 = (base[0] + dx * ln * 0.30, base[1] + dy * ln * 0.30 + droop * 0.08)
        m2 = (base[0] + dx * ln * 0.66, base[1] + dy * ln * 0.66 + droop * 0.42)

        def shape(k_):
            return [base, (m1[0] + nx_ * wd * 0.5 * k_, m1[1] + ny_ * wd * 0.5 * k_), (m2[0] + nx_ * wd * 0.40 * k_, m2[1] + ny_ * wd * 0.40 * k_), tip,
                    (m2[0] - nx_ * wd * 0.40 * k_, m2[1] - ny_ * wd * 0.40 * k_), (m1[0] - nx_ * wd * 0.5 * k_, m1[1] - ny_ * wd * 0.5 * k_)]
        L.poly(shape(1.0), STRAW_LIT if lit else lerp(STRAW_LIT, GRASS_DARK, 0.50))          # the bleached edge
        L.poly(shape(0.70), GRASS_MID if lit else GRASS_DARK, GRASS_DARK, g=(base, tip))
        L.line([base, m1, m2, tip], lerp(GRASS_MID, STRAW_LIT, 0.35) if lit else GRASS_MID, 0.8, 0.7)   # the midrib
    #        cane's top (x, y), leaf length (px), is the sun on it
    canes = [(226.0, 586.0, 36.0, False), (250.0, 574.0, 44.0, False), (272.0, 582.0, 38.0, False), (302.0, 566.0, 50.0, False),      # a thicket,
             (338.0, 558.0, 56.0, True), (358.0, 574.0, 44.0, True), (382.0, 566.0, 48.0, False), (410.0, 584.0, 36.0, False),           # another, a fleck of sun on it,
             (488.0, 574.0, 44.0, False), (510.0, 562.0, 52.0, True), (532.0, 580.0, 38.0, False), (552.0, 592.0, 26.0, False), (586.0, 598.0, 15.0, False)]   # and a third, running out
    for (sx_, sy_, ln0, sun) in canes:
        lean = rng.normal(0, 4)
        cane = curve([(sx_ + lean * 2, 606.0), (sx_ + lean, (sy_ + 606.0) / 2), (sx_, sy_)], 6)
        L.taper(cane, GRASS_DARK, 3.0, 1.8)
        # leaves alternately to left and right down the cane's top, then one standing at its tip
        side = 1 if rng.random() < 0.5 else -1
        for j in range(4):
            at_ = cane[-1 - j]
            an = (-math.pi + rng.uniform(0.18, 0.55)) if side < 0 else -rng.uniform(0.18, 0.55)
            leaf(at_, an, ln0 * rng.uniform(0.78, 1.05) * (1 - 0.08 * j), ln0 * rng.uniform(0.30, 0.38), sun and (side < 0 or rng.random() < 0.4))
            side = -side
        leaf(cane[-1], -math.pi / 2 + rng.uniform(-0.45, 0.45), ln0 * 0.62, ln0 * 0.26, sun)
    # and through them a few long blades of last year's pampas grass, arching over
    for (cx, n, tall) in ((270.0, 5, 50.0), (350.0, 7, 60.0), (436.0, 5, 46.0), (512.0, 6, 54.0)):
        for i in range(n):
            lean = float(np.clip(rng.normal(0, 0.55), -0.93, 0.93))
            ln = tall * rng.uniform(0.6, 1.0) * (1 - 0.22 * abs(lean))
            blade(cx + rng.normal(0, 8), 603.0, ln, lean, STRAW_LIT if (lean < 0 and rng.random() < 0.4) else STRAW_DARK, w=rng.uniform(1.8, 2.6), droop=1.0)
    sc, sa = S.done()
    L.add(sc, sa)
    c, a = L.done()
    # ---------------- the morning sun along the left edges: a warm rim, most on the trunk and the limbs
    a_hard = (a > 0.5).astype(F32)
    rim = D.rim(a_hard, light=(-1.0, -0.45), width=2.2)
    x, y = grid(SHAPE)
    lum_ = c @ np.array([0.3, 0.55, 0.15], dtype=F32)
    warm = np.clip(c * 2.3 + np.array([0.20, 0.13, 0.02], dtype=F32), 0, 1)
    c = lerp(c, warm, (np.clip(rim * 1.1, 0, 1) * (0.55 + 0.45 * (y < 420)) * (lum_ < 0.42))[..., None])
    c = grade_cut(c, a, 0.94, seed=seed, uneven=0.06)
    return c.astype(F32), np.clip(a, 0, 1)          # (no brush pass: it is all needle ends and blades, and a brush would carry the sky's light into its gaps)


def front_cut(back, seed, info, fast=False):
    """front.png (round twenty's, where it was): a coil of rope and three net floats at the very front, bottom left,
    on the road's verge. Drawn again as a coil: the turns of the rope one on another, the twist of its strands; and in
    the pines' shade, as the ground under it is, the sun catching its left edge."""
    L = Wet(SHAPE)
    rng = np.random.default_rng(seed)
    cx_, cy_ = 70.0, 598.0
    rope_l, rope_d = lerp(thin(OCHRE, 0.30), PRUSSIAN, 0.30), lerp(mixp(OCHRE, SIENNA, 0.4), PRUSSIAN, 0.58)
    # the bank's turf runs on under it to the picture's left edge (near.png has the rest of the lip): low, dark, a few blades
    S = Sheet(SHAPE)
    top = [(float(x_), 600.0 - (5.0 + 5.0 * math.sin(x_ / 31.0) ** 2) + rng.normal(0, 0.8)) for x_ in np.arange(-4.0, 204.0, 6.0)]
    L.poly([(-4, 602)] + top + [(204, 602)], lerp(GRASS_DARK, BARK_DARK, 0.40), lerp(GRASS_DARK, BARK_DARK, 0.80))
    for x_ in np.arange(0.0, 200.0, 2.4):
        ln = rng.uniform(4, 11)
        lean = rng.uniform(-0.5, 0.5)
        y0 = 600.0 - (5.0 + 5.0 * math.sin(x_ / 31.0) ** 2) + 2
        S.line([(x_, y0), (x_ + lean * ln * 0.4, y0 - ln * 0.6), (x_ + lean * ln, y0 - ln)], GRASS_DARK if rng.random() < 0.7 else GRASS_MID, 1.5, 1.0)
    sc_, sa_ = S.done()
    L.add(sc_, sa_)
    L.ellipse(cx_ + 5, cy_ + 1, 50, 20, lerp(SAND_SHADE, PRUSSIAN, 0.55), alpha=0.9)                        # where it lies: its own dark
    for i in range(8):
        r = 46 - i * 4.6
        yy = cy_ - i * 1.9
        L.ellipse(cx_, yy, r, r * 0.42, rope_d)
        L.ellipse(cx_ - 0.8, yy - 1.3, r - 1.0, (r - 1.0) * 0.42 - 0.6, rope_l, lerp(rope_l, rope_d, 0.6), g=((cx_ - r, yy), (cx_ + r, yy)))
        for a in np.arange(0.0, 2 * math.pi, 0.22 if r > 20 else 0.4):                                       # the strands' twist
            px_, py_ = cx_ - 0.8 + math.cos(a) * (r - 2.6), yy - 1.3 + math.sin(a) * ((r - 2.6) * 0.42)
            if py_ > 600:
                continue
            L.line([(px_ - 1.2, py_ - 0.9), (px_ + 1.2, py_ + 0.9)], rope_d, 0.8, 0.55)
    L.ellipse(cx_ - 0.8, cy_ - 15.6, 8.5, 3.2, lerp(SAND_SHADE, PRUSSIAN, 0.5))                              # the hollow in its middle
    end = curve([(cx_ + 40, cy_ - 4), (cx_ + 56, cy_ - 10), (cx_ + 66, cy_ - 5), (cx_ + 70, cy_ + 2)], 8)    # its loose end
    L.taper(end, rope_d, 4.6, 4.0)
    L.taper([(px_ - 0.5, py_ - 1.0) for px_, py_ in end], rope_l, 2.4, 2.0)
    for (fx_, fy_, fr) in ((150, 592, 9), (172, 600, 10), (118, 606, 8)):
        L.ellipse(fx_ + 3, fy_ + 2.5, fr * 1.1, fr * 0.6, lerp(SAND_SHADE, PRUSSIAN, 0.45), alpha=0.85)
        L.ellipse(fx_, fy_, fr, fr * 0.9, lerp(thin(OCHRE, 0.35), PRUSSIAN, 0.28), lerp(mixp(OCHRE, SIENNA, 0.4), PRUSSIAN, 0.55), g=((fx_ - fr, fy_ - fr), (fx_ + fr, fy_ + fr)))
        L.line([(fx_ - fr * 0.95, fy_ + 0.5), (fx_ + fr * 0.95, fy_ + 0.5)], rope_d, 0.9, 0.7)             # the groove its line runs in
    c, a = L.done()
    a_hard = (a > 0.5).astype(F32)
    rim = D.rim(a_hard, light=(-1.0, -0.5), width=1.8)
    c = lerp(c, np.clip(c * 1.6 + np.array([0.14, 0.10, 0.02], dtype=F32), 0, 1), (np.clip(rim, 0, 1) * 0.8)[..., None])
    return painted(c.astype(F32), a, SAND * 0.7, seed=seed, keep=0.85, fast=fast)

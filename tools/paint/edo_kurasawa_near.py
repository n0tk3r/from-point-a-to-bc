"""PAINT-23 (round twenty-three, RECOMPOSE: DEPTH.md): the NEAR plane of Nishikurasawa: what hangs or grows between us
and the play. People always pass behind it (`plane: "front"`).

  near.png    the HACKBERRY's crown over the top right corner, the bough that comes out toward us from it across the top
              (the tree on the distance mound, planted for the travellers' shade two centuries since: its fresh April
              leaves, seen from below, in their own shade, the sun catching only the clumps' upper left edges); and at
              the top left the near end of O-KUNI'S EAVE, the thatch's cut edge and its dark underside, with a reed blind
              let down from it in the first bay against the morning sun (the sun is behind us, low on the road from Yui)
  front.png   the ROADSIDE'S BANK along the bottom, on the inland side where we stand: the verge's lip, sasa with broad
              pointed leaves (their edges bleached at winter's end), a few blades of last year's pampas grass, a stone;
              low toward the road, rising to the right edge, in the shade of the hill behind us

All of it a dark mass, warm in its darks, lit only along an edge that faces the sun (behind us and to the left). Outline
before inside: lobed clumps of leaves against the sky, blades and leaves against the bright road; little drawn within.
No small gaps of sky inside a dark mass (the game's paints key a speck of light shut in by darks as a highlight). Nothing
here is clicked but the hackberry itself, nothing that can be stood on or clicked is behind it: the crown stays above the
mound's top and clear of Fuji, the blind above the heads of whoever stands at the bench, the bank below the feet of
whoever stands on the verge.
"""

import math

import numpy as np

from brush import F32, Sheet, blur, curve, grid, lerp, noise, rgb, warp
import depth as D
from edo_village_kit import (WPAPER, Wet, thin, mixp, grade_cut, painted, NAPLES, CERULEAN, COBALT, ULTRA, PRUSSIAN, OCHRE, SIENNA,
                             VERONESE, VIRIDIAN)
import edo_kurasawa_view as V
from edo_kurasawa_view import SHAPE, W, H, HZ, P, k, TEA, MOUND, HACK, U, NL
from edo_kurasawa_things import keyline, THATCH_EDGE, THATCH_UNDER, TIMBER_DARK, TIMBER, EAVE_POSTS, POST_W

DARK = rgb("#1a1422")
LEAF_DARK = lerp(mixp(mixp(VIRIDIAN, OCHRE, 0.15), PRUSSIAN, 0.47), DARK, 0.28)   # the crown's underside: deep, a little warm
LEAF_MID = lerp(mixp(mixp(VIRIDIAN, OCHRE, 0.18), VERONESE, 0.22), PRUSSIAN, 0.30)
LEAF_COOL = lerp(LEAF_MID, thin(mixp(COBALT, VIRIDIAN, 0.5), 0.35), 0.35)  # leaves in shade that look at the sky
LEAF_LIT = lerp(mixp(VERONESE, NAPLES, 0.30), PRUSSIAN, 0.22)            # fresh April leaves where the sun catches them
LEAF_GLOW = thin(mixp(VERONESE, NAPLES, 0.45), 0.10)                     # the sun through the thinnest edge leaves
BOUGH = lerp(mixp(SIENNA, PRUSSIAN, 0.66), DARK, 0.35)
BOUGH_LIT = lerp(mixp(OCHRE, SIENNA, 0.45), NAPLES, 0.20)
GRASS_DARK = lerp(mixp(VIRIDIAN, OCHRE, 0.42), PRUSSIAN, 0.50)
GRASS_MID = lerp(mixp(VIRIDIAN, OCHRE, 0.50), PRUSSIAN, 0.26)
STRAW_DARK = lerp(mixp(OCHRE, SIENNA, 0.35), PRUSSIAN, 0.46)
STRAW_LIT = thin(mixp(OCHRE, NAPLES, 0.45), 0.18)
REED = lerp(mixp(OCHRE, SIENNA, 0.30), PRUSSIAN, 0.38)
REED_DARK = lerp(mixp(SIENNA, PRUSSIAN, 0.55), DARK, 0.2)


def crown_fork():
    """Where the hackberry's limbs leave its trunk (the trunk is the backdrop's: edo_kurasawa_things.hackberry_trunk)."""
    m = MOUND
    from edo_kurasawa_things import FORK_Y
    return P(m["X"] + 30.0 + 14.0, m["Z"] + 10.0, FORK_Y + 30.0)


def limb(L, pts, w0, w1):
    c = curve(pts, 12)
    L.taper(c, BOUGH, w0, w1)
    L.taper([(px - 0.10 * w0, py - 0.22 * w0) for px, py in c], BOUGH_LIT, w0 * 0.30, w1 * 0.30, alpha=0.55)
    return c


def leaf(L, px, py, an, ln, tone, alpha=0.95, wide=0.46):
    """One leaf seen at a slant: a small pointed oval laid along `an` (never a dot)."""
    dx, dy = math.cos(an), math.sin(an)
    nx_, ny_ = -dy, dx
    wd = ln * wide
    tip = (px + dx * ln, py + dy * ln)
    m1 = (px + dx * ln * 0.34, py + dy * ln * 0.34)
    m2 = (px + dx * ln * 0.70, py + dy * ln * 0.70)
    L.poly([(px, py), (m1[0] + nx_ * wd * 0.5, m1[1] + ny_ * wd * 0.5), (m2[0] + nx_ * wd * 0.40, m2[1] + ny_ * wd * 0.40), tip,
            (m2[0] - nx_ * wd * 0.40, m2[1] - ny_ * wd * 0.40), (m1[0] - nx_ * wd * 0.5, m1[1] - ny_ * wd * 0.5)], tone, alpha=alpha)


def crown(L, rng):
    """The hackberry's crown, as it shows under the top of the frame, painted the way Yui's pines are: one broad dark
    mass of leaf in three bodies (the main crown up and to the right, the bough's spread out over the road, a lower hang
    under the fork), each a flat wash graded only across the whole body (a breath lighter to the upper left, the
    underside the darkest), never a ball shaded lobe by lobe; the clumps inside told only by the leaves along their
    upper left rims catching the sun and the dark leaves along their lower rims; the edge all leaf ends and short sprays;
    the sky only between the bodies, never in small holes; the limbs dark where they show between and under them."""
    from brush import mask_ellipse
    from scipy import ndimage
    fx, fy = crown_fork()
    limbs = [
        ([(fx, fy + 4), (fx - 34, fy - 40), (fx - 84, fy - 84), (fx - 140, fy - 122), (fx - 196, fy - 160), (fx - 236, fy - 210)], 26, 7),
        ([(fx, fy + 4), (fx + 22, fy - 70), (fx + 50, fy - 150), (fx + 86, fy - 240)], 28, 10),
        ([(fx, fy + 4), (fx - 6, fy - 90), (fx - 22, fy - 180), (fx - 14, fy - 250)], 24, 9),
        ([(fx, fy + 2), (fx + 54, fy - 20), (fx + 110, fy - 30), (fx + 170, fy - 26)], 22, 8),
    ]
    for pts, w0, w1 in limbs:
        limb(L, pts, w0, w1)
    for (pts, w0) in (([(fx - 84, fy - 84), (fx - 80, fy - 136), (fx - 62, fy - 196)], 10), ([(fx - 140, fy - 122), (fx - 160, fy - 108), (fx - 190, fy - 102)], 7),
                      ([(fx + 50, fy - 150), (fx + 96, fy - 140), (fx + 140, fy - 150)], 9), ([(fx - 196, fy - 160), (fx - 216, fy - 142), (fx - 240, fy - 132)], 5)):
        limb(L, pts, w0, 2.5)
    # the three bodies, as lobes (x, y, rx, ry); the bough's spread kept off Fuji's top and its cloud (x > 430 above row 140)
    bodies = [
        [(fx + 40, fy - 230, 90, 60), (fx + 130, fy - 200, 80, 56), (fx - 40, fy - 220, 70, 46), (fx + 100, fy - 130, 76, 52), (fx + 10, fy - 150, 64, 44),
         (fx + 160, fy - 110, 60, 46), (fx + 150, fy - 40, 56, 40), (fx + 60, fy - 70, 54, 36), (fx - 60, fy - 150, 50, 34), (fx + 30, fy - 30, 40, 26),
         (fx - 30, fy - 90, 44, 30), (fx + 110, fy + 8, 40, 24)],
        [(fx - 130, fy - 186, 54, 34), (fx - 190, fy - 196, 50, 32), (fx - 226, fy - 228, 40, 26), (fx - 160, fy - 140, 44, 28), (fx - 110, fy - 120, 38, 24),
         (fx - 200, fy - 150, 30, 18)],
        [(fx - 60, fy - 40, 34, 20), (fx - 100, fy - 66, 30, 18), (fx + 10, fy - 12, 26, 15)],
    ]
    x, y = grid(SHAPE)
    sun = (-0.8, -0.6)
    deep = lerp(LEAF_DARK, DARK, 0.30)
    upper = lerp(LEAF_DARK, LEAF_MID, 0.50)
    blooms = noise(SHAPE, 30.0, 71, 4)
    for bi, lobes in enumerate(bodies):
        m = np.zeros(SHAPE, dtype=F32)
        for (cx, cy, rx, ry) in lobes:
            m = np.maximum(m, mask_ellipse(SHAPE, cx, cy, rx, ry))
        m = warp(m, 6.0, 15.0, 300 + bi)                                    # the scallops broken: no clean arcs
        inside = ndimage.binary_fill_holes(m > 0.5)
        m = inside.astype(F32)
        if not inside.any():
            continue
        proj = x * sun[0] + y * sun[1]
        p0, p1 = float(proj[inside].min()), float(proj[inside].max())
        ts = np.clip((proj - p0) / max(p1 - p0, 1.0), 0, 1)                 # 1 at the body's sunward (upper left) extreme
        a1 = np.clip(ts / 0.5, 0, 1)[..., None]
        a2 = np.clip((ts - 0.55) / 0.45, 0, 1)[..., None]
        col = lerp(lerp(deep[None, None, :] * np.ones(SHAPE + (3,), F32), LEAF_DARK[None, None, :], a1), upper[None, None, :], a2 * 0.9)
        col = lerp(col, LEAF_COOL[None, None, :], (np.clip(blooms - 0.62, 0, 1) * 0.9)[..., None])      # a wet bloom here and there
        col = lerp(col, deep[None, None, :], (np.clip(0.30 - blooms, 0, 1) * 1.2)[..., None])
        L.add(col.astype(F32), m)

        def ok(px, py):
            return inside[int(np.clip(py, 0, H - 1)), int(np.clip(px, 0, W - 1))]
        # the clumps: top ones first, so a lower (nearer) clump's sunlit rim lies over the dark underside of the one above
        for (cx, cy, rx, ry) in sorted(lobes, key=lambda q: q[1]):
            for j in range(int((rx + ry) * 0.35)):                          # its lower rim: dark leaves hanging
                a_ = rng.uniform(0.12 * math.pi, 0.88 * math.pi)
                rr = rng.uniform(0.86, 1.04)
                px, py = cx + math.cos(a_) * rx * rr, cy + math.sin(a_) * ry * rr
                if ok(px, py):
                    leaf(L, px, py, a_ + rng.uniform(-0.5, 0.5) * 0.8 + 0.25, rng.uniform(4.0, 7.0), deep, alpha=0.9)
            for j in range(int((rx + ry) * 0.80)):                          # its upper left rim: the leaves the sun finds
                a_ = rng.uniform(0.92 * math.pi, 1.85 * math.pi)
                rr = rng.uniform(0.74, 1.0)
                px, py = cx + math.cos(a_) * rx * rr, cy + math.sin(a_) * ry * rr
                if not ok(px, py):
                    continue
                facing = math.cos(a_) * sun[0] + math.sin(a_) * sun[1]
                if facing > 0.72 and rng.random() < 0.55:
                    tone = LEAF_LIT
                elif facing > 0.25:
                    tone = lerp(LEAF_MID, LEAF_LIT, rng.uniform(0.0, 0.35))
                else:
                    tone = lerp(LEAF_MID, LEAF_DARK, rng.uniform(0.2, 0.6))
                leaf(L, px, py, a_ + rng.uniform(-0.7, 0.7), rng.uniform(4.0, 7.5), tone, alpha=0.92)
            for j in range(int((rx + ry) * 0.12)):                          # a few cool leaves inside that look at the sky
                px, py = cx + rng.uniform(-0.55, 0.55) * rx, cy + rng.uniform(-0.55, 0.1) * ry
                if ok(px, py):
                    leaf(L, px, py, rng.uniform(-2.6, -0.5), rng.uniform(3.5, 6.0), LEAF_COOL, alpha=0.55)
        # the edge: leaf ends all round the body's outline, hanging below, sticking out at the sides
        edge = inside & (blur(m, 1.2) < 0.75)
        eys, exs = np.where(edge)
        gy, gx = np.gradient(blur(m, 2.5))
        if len(eys):
            pick = rng.choice(len(eys), size=min(len(eys), int(len(eys) * 0.26)), replace=False)
            for i in pick:
                px, py = float(exs[i]), float(eys[i])
                ox, oy = -gx[eys[i], exs[i]], -gy[eys[i], exs[i]]
                nn = math.hypot(ox, oy) or 1.0
                ox, oy = ox / nn, oy / nn
                if oy > 0.3:                                                # hanging below: they droop
                    ox, oy = ox * 0.5, oy + 0.4
                facing = ox * sun[0] + oy * sun[1]
                tone = LEAF_LIT if (facing > 0.55 and rng.random() < 0.5) else (lerp(LEAF_MID, LEAF_DARK, 0.4) if facing > -0.1 else deep)
                leaf(L, px, py, math.atan2(oy, ox) + rng.uniform(-0.45, 0.45), rng.uniform(4.0, 7.5), tone, alpha=0.95)
            # sprays: a short twig out of the mass with its leaves along it, the sky between them open to the sky
            for i in rng.choice(len(eys), size=min(len(eys), 9 if bi == 0 else (5 if bi == 1 else 3)), replace=False):
                px, py = float(exs[i]), float(eys[i])
                ox, oy = -gx[eys[i], exs[i]], -gy[eys[i], exs[i]]
                nn = math.hypot(ox, oy) or 1.0
                ox, oy = ox / nn, oy / nn
                if py < 4 or px > W - 4:
                    continue
                ln = rng.uniform(10.0, 18.0)
                an = math.atan2(oy, ox) + rng.uniform(-0.35, 0.35)
                tw = [(px - ox * 3, py - oy * 3), (px + math.cos(an) * ln * 0.5, py + math.sin(an) * ln * 0.5 + 1.0), (px + math.cos(an) * ln, py + math.sin(an) * ln + 2.5)]
                L.line(tw, BOUGH, 1.0, 0.85)
                facing = ox * sun[0] + oy * sun[1]
                for f in np.linspace(0.25, 1.0, 5):
                    bx, by = px + math.cos(an) * ln * f, py + math.sin(an) * ln * f + 2.5 * f * f
                    for side in (-1.0, 1.0):
                        tone = LEAF_LIT if (facing > 0.4 and side < 0 and rng.random() < 0.5) else lerp(LEAF_MID, LEAF_DARK, rng.uniform(0.2, 0.7))
                        leaf(L, bx, by, an + side * rng.uniform(0.6, 1.1) + 0.3, rng.uniform(4.0, 6.0), tone, alpha=0.95)
    # the limbs again where they come out under the leaves (dark against the sky between the bodies)
    for pts, w0, w1 in limbs[:1]:
        c = curve(pts, 12)
        L.taper(c[:7], BOUGH, w0, (w0 + w1) / 2, alpha=0.9)
    return limbs


def eave_corner(L, rng):
    """The near end of O-Kuni's eave at the top left: the thatch's cut edge and its dark underside, from the frame's
    left edge, and the reed blind let down from it in the first bay (against the morning sun)."""
    T = TEA
    e, th = T.eave, T.thick
    o = T.over
    q = lambda u, w, y: T.pt(u, w, y)
    u_end = 250.0                                            # the near plane holds the eave this far along the front
    # the cut edge of the thatch (its face toward the road): pale cut ends, layered; its underside dark
    L.poly([q(-T.over_end, -o, e), q(u_end, -o, e), q(u_end, -o, e + th), q(-T.over_end, -o, e + th)], lerp(THATCH_EDGE, PRUSSIAN, 0.22),
           lerp(THATCH_EDGE, DARK, 0.25), g=(q(0, -o, e + th), q(0, -o, e)))
    for f in np.linspace(0.12, 0.9, 5):
        L.line([q(-T.over_end, -o, e + th * f), q(u_end, -o, e + th * f)], lerp(THATCH_EDGE, DARK, 0.45), 0.7, 0.4)
    L.poly([q(-T.over_end, -o, e), q(u_end, -o, e), q(u_end, 0, e + 24), q(-T.over_end, 0, e + 24)], lerp(THATCH_UNDER, DARK, 0.25))
    # the reed blind: from the eave's edge down to a little over a person's head, its slats level (they run to the
    # road's vanishing point), its cords; the sun behind us lights its near edge only
    u0, u1 = -T.over_end + 6, 205.0
    w_ = -o + 6
    bot = 196.0
    L.poly([q(u0, w_, e - 1), q(u1, w_, e - 1), q(u1, w_, bot), q(u0, w_, bot)], REED, REED_DARK, g=(q(u0, w_, e), q(u0, w_, bot)))
    for y_ in np.arange(bot + 3, e - 2, 4.2):
        L.line([q(u0, w_, y_), q(u1, w_, y_)], REED_DARK if rng.random() < 0.7 else lerp(REED, STRAW_LIT, 0.3), 0.7, 0.55)
    for f in (0.22, 0.62):
        uu = u0 + (u1 - u0) * f
        L.line([q(uu, w_ - 1, e - 1), q(uu, w_ - 1, bot - 3)], DARK, 1.0, 0.8)
    L.line([q(u0, w_, bot), q(u1, w_, bot)], lerp(REED_DARK, DARK, 0.4), 1.6, 0.9)
    L.line([q(u0, w_ - 1, e - 1), q(u0, w_ - 1, bot)], lerp(STRAW_LIT, REED, 0.4), 1.2, 0.8)
    keyline(L, [q(-T.over_end, -o, e), q(u_end, -o, e)], 470, seed=31, weight=1.2, alpha=0.5)
    return [q(-T.over_end, -o, e + th), q(u_end, -o, e + th), q(u_end, -o, e), q(u1, w_, bot), q(u0, w_, bot)]


def near_cut(seed, fast=False):
    """near.png: the hackberry's crown and its bough across the top right; the eave's near end and its blind at the
    top left. -> (colour, cover)."""
    L = Wet(SHAPE)
    rng = np.random.default_rng(seed)
    crown(L, rng)
    eave_corner(L, rng)
    c, a = L.done()
    a_hard = (a > 0.5).astype(F32)
    rim = D.rim(a_hard, light=(-1.0, -0.6), width=2.0)
    x, y = grid(SHAPE)
    lum_ = c @ np.array([0.3, 0.55, 0.15], dtype=F32)
    warm = np.clip(c * 2.0 + np.array([0.18, 0.13, 0.02], dtype=F32), 0, 1)
    c = lerp(c, warm, (np.clip(rim * 0.9, 0, 1) * (lum_ < 0.42) * (x > 300))[..., None])
    c = grade_cut(c, a, 0.94, seed=seed, uneven=0.06)
    return c.astype(F32), np.clip(a, 0, 1)                   # (no brush pass: it is all leaf tips and reed slats)


def front_cut(seed, fast=False):
    """front.png: the roadside's bank along the bottom: the inland verge's lip, sasa, pampas blades, a stone. Low at the
    road's edge (the bottom's left part is the road itself), rising to the right edge. -> (colour, cover)."""
    L = Wet(SHAPE)
    S = Sheet(SHAPE)
    rng = np.random.default_rng(seed)

    def hump(x_):
        """The bank's top (picture row) at a column: none over the road, rising to the right."""
        u = float(np.clip((x_ - 250.0) / 550.0, 0, 1))
        hgt = 3.0 + 26.0 * u ** 1.3 + 7.0 * math.sin(x_ / 37.0) ** 2 * u
        return 600.0 - hgt
    xs = np.arange(246.0, 812.0, 4.0)
    top = [(float(x_), float(hump(x_) + rng.normal(0, 1.2))) for x_ in xs]
    L.poly([(246, 603)] + top + [(812, 603)], lerp(GRASS_DARK, DARK, 0.30), lerp(GRASS_DARK, DARK, 0.70))
    for (sx_, sw, sh_) in ((452.0, 22.0, 11.0), (702.0, 30.0, 15.0)):                                      # stones in the turf
        sy = hump(sx_) + 4
        stone = [(sx_ - sw, sy + 7), (sx_ - sw * 0.8, sy - sh_ * 0.6), (sx_ - sw * 0.2, sy - sh_), (sx_ + sw * 0.5, sy - sh_ * 0.8), (sx_ + sw, sy - sh_ * 0.1),
                 (sx_ + sw * 0.9, sy + 7)]
        L.poly(stone, lerp(mixp(PRUSSIAN, OCHRE, 0.22), DARK, 0.40), lerp(mixp(PRUSSIAN, SIENNA, 0.3), DARK, 0.75), g=((sx_ - sw, sy - sh_), (sx_ + sw, sy + 7)))
        L.poly([stone[1], stone[2], stone[3], (sx_ + sw * 0.2, sy - sh_ * 0.45), (sx_ - sw * 0.6, sy - sh_ * 0.3)], lerp(thin(mixp(PRUSSIAN, OCHRE, 0.35), 0.30), DARK, 0.2), alpha=0.9)

    def blade(x0, y0, ln, lean, tone, w=3.0, droop=0.0):
        tx = x0 + lean * ln
        ty = y0 - ln * math.sqrt(max(0.06, 1 - lean * lean)) + droop * abs(lean) * ln * 0.5
        pts_ = curve([(x0, y0), (x0 + lean * ln * 0.22, y0 - ln * 0.60), (x0 + lean * ln * 0.70, y0 - ln * 0.93 + droop * abs(lean) * ln * 0.12), (tx, ty)], 6)
        L.taper(pts_, tone, w, 0.5)
    for x_ in np.arange(248.0, 808.0, 2.0):                                                               # the turf's short grass
        ln = rng.uniform(5, 12) * (0.5 + 0.5 * min(1.0, (x_ - 248) / 200))
        blade(x_ + rng.normal(0, 1), hump(x_) + 2, ln, rng.uniform(-0.55, 0.55), GRASS_DARK if rng.random() < 0.72 else GRASS_MID, w=1.4)

    def leaf(base, an, ln, wd, lit):
        dx, dy = math.cos(an), math.sin(an)
        nx_, ny_ = -dy, dx
        droop = 0.30 * ln * abs(dx)
        tip = (base[0] + dx * ln, base[1] + dy * ln + droop)
        m1 = (base[0] + dx * ln * 0.30, base[1] + dy * ln * 0.30 + droop * 0.08)
        m2 = (base[0] + dx * ln * 0.66, base[1] + dy * ln * 0.66 + droop * 0.42)

        def shape(k_):
            return [base, (m1[0] + nx_ * wd * 0.5 * k_, m1[1] + ny_ * wd * 0.5 * k_), (m2[0] + nx_ * wd * 0.40 * k_, m2[1] + ny_ * wd * 0.40 * k_), tip,
                    (m2[0] - nx_ * wd * 0.40 * k_, m2[1] - ny_ * wd * 0.40 * k_), (m1[0] - nx_ * wd * 0.5 * k_, m1[1] - ny_ * wd * 0.5 * k_)]
        L.poly(shape(1.0), STRAW_LIT if lit else lerp(STRAW_LIT, GRASS_DARK, 0.50))
        L.poly(shape(0.70), GRASS_MID if lit else GRASS_DARK, GRASS_DARK, g=(base, tip))
        L.line([base, m1, m2, tip], lerp(GRASS_MID, STRAW_LIT, 0.35) if lit else GRASS_MID, 0.8, 0.7)
    #        cane's top (x, y), leaf length, the sun on it: sasa in clumps, lower toward the road, bigger to the right
    canes = [(300.0, 592.0, 22.0, False), (338.0, 588.0, 26.0, True), (372.0, 594.0, 20.0, False),
             (520.0, 582.0, 32.0, False), (548.0, 572.0, 38.0, True), (574.0, 580.0, 34.0, False),
             (668.0, 566.0, 40.0, False), (700.0, 556.0, 46.0, True), (734.0, 566.0, 42.0, False), (770.0, 552.0, 48.0, False), (800.0, 560.0, 44.0, True)]
    for (sx_, sy_, ln0, sun) in canes:
        lean = rng.normal(0, 4)
        cane = curve([(sx_ + lean * 2, 606.0), (sx_ + lean, (sy_ + 606.0) / 2), (sx_, sy_)], 6)
        L.taper(cane, GRASS_DARK, 3.0, 1.8)
        side = 1 if rng.random() < 0.5 else -1
        for j in range(4):
            at_ = cane[-1 - j]
            an = (-math.pi + rng.uniform(0.18, 0.55)) if side < 0 else -rng.uniform(0.18, 0.55)
            leaf(at_, an, ln0 * rng.uniform(0.78, 1.05) * (1 - 0.08 * j), ln0 * rng.uniform(0.30, 0.38), sun and (side < 0 or rng.random() < 0.4))
            side = -side
        leaf(cane[-1], -math.pi / 2 + rng.uniform(-0.45, 0.45), ln0 * 0.62, ln0 * 0.26, sun)
    for (cx, n, tall) in ((410.0, 4, 34.0), (612.0, 6, 50.0), (752.0, 6, 58.0)):                          # last year's pampas blades, arching over
        for i in range(n):
            lean = float(np.clip(rng.normal(0, 0.55), -0.93, 0.93))
            ln = tall * rng.uniform(0.6, 1.0) * (1 - 0.22 * abs(lean))
            blade(cx + rng.normal(0, 8), 603.0, ln, lean, STRAW_LIT if (lean < 0 and rng.random() < 0.4) else STRAW_DARK, w=rng.uniform(1.8, 2.6), droop=1.0)
    sc, sa = S.done()
    L.add(sc, sa)
    c, a = L.done()
    a_hard = (a > 0.5).astype(F32)
    rim = D.rim(a_hard, light=(-1.0, -0.5), width=1.8)
    lum_ = c @ np.array([0.3, 0.55, 0.15], dtype=F32)
    c = lerp(c, np.clip(c * 2.2 + np.array([0.18, 0.12, 0.02], dtype=F32), 0, 1), (np.clip(rim, 0, 1) * 0.8 * (lum_ < 0.42))[..., None])
    c = grade_cut(c, a, 0.94, seed=seed, uneven=0.06)
    return c.astype(F32), np.clip(a, 0, 1)

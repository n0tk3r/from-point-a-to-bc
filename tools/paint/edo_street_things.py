"""PAINT-21C: the merchant street's cut-outs (edo-street), drawn through its camera (edo_street.CAM) in its light; each
returned as (colour sheet, line sheet[, info]) for edo_street.py to brush and save.

  `prints-1`, `prints-2`   the lines of prints pegged across the print shop's open front (actor prints: stars on
                           stage and at home, in our own designs; toy prints to cut out and build) (they flutter: sway)
  `bench`                  the printing bench at the edge of the raised floor: the block (its two marks cut at its edge,
                           the corner and the straight one), a stack of paper, the round rubbing pad, brushes, a pot of
                           the new blue; and a little slanted stand at its right end that shows the sheet
  `print`, `print-ghost`, `print-clean`
                           the sheet on that stand: blank; printed with the blue a hair to the left, a ghost of itself
                           beside the outline; clean (an actor at home in a robe of the new blue): #30's three states
  `noren-kelp`, `noren-med`, `noren-comb`   the shops' noren (they stir: sway)
  `sign`                   the medicine shop's big standing signboard: "Uruyusu" in katakana, written in our own hand
  `roadgod`                the small stone road god at the corner, a cup of water before it
  `watervendor`            a water-seller resting his two buckets on their pole by the comb-maker's
"""

import math

import numpy as np

from brush import F32, Sheet, curve, lerp
from edo_dojima_kit import *
import edo_street as S

g = S.g
CAM = S.CAM


def sheets():
    return Paper(SHAPE), Paper(SHAPE)


def lit_here(X, Y, Z=None):
    """Is a point on the far side's fronts in the sun (above the street's shadow line, or in the band)?"""
    Z = S.ZE if Z is None else Z
    return Y >= S.SHADE_Y or S.in_band(X, Z)


def sunlit(c, X, Y, Z=None):
    return c if lit_here(X, Y, Z) else shaded(c, 0.42)


# ---------------------------------------------------------------- prints (our own designs: shapes, never anyone's print)
def actor_print(sheet, lines, x0, y0, w, h, rng, kind=0, blue=None, offset=0.0, faint=False):
    """One print, upright, in picture px: a ground, a figure in a robe (an actor at home, or two on a stage), the
    keyblock's outline. `offset` slides the blue block to the left (misregistered); `faint` makes it paler."""
    grounds = [lerp(NAPLES, WHITE, 0.45), lerp(CERULEAN, WHITE, 0.5), lerp(VERONESE, WHITE, 0.45), lerp(LAKE, WHITE, 0.62), lerp(OCHRE, WHITE, 0.45)]
    robes = [blue if blue is not None else COBALT, VERMILION, INDIGO, lerp(VIRIDIAN, PRUSSIAN, 0.2), lerp(LAKE, SIENNA, 0.3)]
    sheet.poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], grounds[kind % len(grounds)])
    cx = x0 + w * 0.5
    if kind % 3 == 2:                                       # a stage: two figures, a strip of floor
        sheet.poly([(x0, y0 + h * 0.82), (x0 + w, y0 + h * 0.82), (x0 + w, y0 + h), (x0, y0 + h)], lerp(OCHRE, SIENNA, 0.3))
        for (fx, rc) in ((0.32, robes[1]), (0.70, robes[2])):
            px = x0 + w * fx
            sheet.poly([(px - w * 0.16, y0 + h * 0.82), (px + w * 0.16, y0 + h * 0.82), (px + w * 0.1, y0 + h * 0.38), (px - w * 0.1, y0 + h * 0.38)], rc)
            sheet.ellipse(px, y0 + h * 0.3, w * 0.08, w * 0.09, FLESH)
            sheet.line([(px - w * 0.07, y0 + h * 0.24), (px + w * 0.07, y0 + h * 0.24)], PRUSSIAN, max(0.6, w * 0.06))
    else:                                                   # an actor at home: one figure, half length, in a big robe
        rc = robes[0] if kind % 3 == 0 else robes[kind % len(robes)]
        bx = cx - offset
        sheet.poly([(bx - w * 0.36, y0 + h), (bx + w * 0.36, y0 + h), (bx + w * 0.24, y0 + h * 0.42), (bx - w * 0.24, y0 + h * 0.42)], lerp(rc, WHITE, 0.35) if faint else rc)
        if offset:                                          # the ghost: the robe's colour lands beside its outline
            sheet.poly([(bx - w * 0.36 + offset * 0.5, y0 + h), (bx + w * 0.36 + offset * 0.5, y0 + h), (bx + w * 0.24 + offset * 0.5, y0 + h * 0.42), (bx - w * 0.24 + offset * 0.5, y0 + h * 0.42)], lerp(rc, WHITE, 0.55), 0.7)
        sheet.ellipse(cx, y0 + h * 0.3, w * 0.13, w * 0.15, FLESH)
        sheet.poly([(cx - w * 0.15, y0 + h * 0.24), (cx + w * 0.15, y0 + h * 0.24), (cx + w * 0.10, y0 + h * 0.12), (cx - w * 0.10, y0 + h * 0.12)], PRUSSIAN)
        lines.line([(cx - w * 0.36, y0 + h), (cx - w * 0.24, y0 + h * 0.42), (cx + w * 0.24, y0 + h * 0.42), (cx + w * 0.36, y0 + h)], PRUSSIAN, max(0.5, w * 0.04), 0.9)
    lines.line([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h), (x0, y0)], PRUSSIAN, 0.6, 0.55)


def toy_print(sheet, lines, x0, y0, w, h, rng):
    """A toy print to cut out and build: a pale sheet laid out with small pieces (walls, a roof, little figures) in a
    grid, each with its outline."""
    sheet.poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], lerp(WHITE, NAPLES, 0.25))
    cols = [VERMILION, COBALT, VIRIDIAN, OCHRE, LAKE]
    for i in range(2):
        for j in range(3):
            px, py = x0 + w * (0.1 + 0.45 * i), y0 + h * (0.08 + 0.3 * j)
            c = cols[(i + j * 2) % len(cols)]
            if (i + j) % 2:
                sheet.poly([(px, py + h * 0.22), (px + w * 0.36, py + h * 0.22), (px + w * 0.36, py + h * 0.06), (px + w * 0.18, py), (px, py + h * 0.06)], lerp(c, WHITE, 0.25))
            else:
                sheet.poly([(px, py), (px + w * 0.36, py), (px + w * 0.36, py + h * 0.22), (px, py + h * 0.22)], lerp(c, WHITE, 0.25))
            lines.line([(px, py), (px + w * 0.36, py)], PRUSSIAN, 0.5, 0.6)
    lines.line([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h), (x0, y0)], PRUSSIAN, 0.6, 0.55)


def print_line(row, X0, X1, Y, kinds, seed):
    """A line strung across the open front at height Y with prints pegged on it, hanging toward the street."""
    s, l = sheets()
    rng = np.random.default_rng(seed)
    Z = S.ZE + 8
    a, b = g(X0, Z, Y), g(X1, Z, Y)
    sag = 3.0
    l.line(curve([a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + sag), b], 10), lerp(WOOD_SH, PRUSSIAN, 0.2), 0.8, 1.0)
    boxes = []
    n = len(kinds)
    for i, kd in enumerate(kinds):
        u = (i + 0.6) / (n + 0.2)
        X = X0 + (X1 - X0) * u
        k = CAM.k(X, Z)
        top = g(X, Z, Y)
        top = (top[0], top[1] + sag * 4 * u * (1 - u) + 1)
        w, h = (19 * k, 27 * k) if kd != "toy" else (25 * k, 34 * k)
        x0, y0 = top[0] - w / 2, top[1]
        if kd == "toy":
            toy_print(s, l, x0, y0, w, h, rng)
        else:
            actor_print(s, l, x0, y0, w, h, rng, kind=int(kd))
        l.line([(top[0], top[1] - 1.5), (top[0], top[1] + 2)], WOOD_LIT, max(1.0, 2.2 * k), 1.0)        # the peg
        # in the street's shade below the line? (the prints keep their own colours; the shade lies over them)
        if not lit_here(X, Y - 20):
            s.poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], lerp(COBALT, ULTRA, 0.3), 0.30)
        boxes.append([int(x0) - 1, int(y0) - 3, int(w) + 2, int(h) + 4])
    return s, l, dict(boxes=boxes)


# ---------------------------------------------------------------- the bench and the sheet
B = S.BENCH
STAND = dict(X=B["X1"] - 10.0, Z=B["Z1"] - 20.0)


def bench():
    """The printing bench at the front edge of the raised floor (seen across the street, low and long): its top, its
    front; on it, from the left, a stack of paper, the block (cherry wood, the picture cut in it, and at its edge the two
    marks: the corner and the straight one), the round rubbing pad, two brushes, the pot of Berlin blue; at its right end
    the slanted stand that shows the sheet (the sheet itself is `print`)."""
    s, l = sheets()
    X0, X1, Z0, Z1, fl, h = B["X0"], B["X1"], B["Z0"], B["Z1"], B["floor"], B["h"]
    top_y = fl + h
    wood = sunlit(lerp(WOOD_LIT, NAPLES, 0.2), X0 + 40, top_y)
    CAM.box(s, X0, X1, fl, top_y, Z0, Z1, wood, shaded(wood, 0.3), top=lerp(wood, WHITE, 0.08), lines=l)
    k = CAM.k((X0 + X1) / 2, Z1)
    info = {}
    # the paper: a stack of white sheets
    CAM.box(s, X0 + 4, X0 + 36, top_y, top_y + 7, Z0 + 6, Z1 - 6, lerp(WHITE, NAPLES, 0.12), PLASTER_SH, top=lerp(WHITE, NAPLES, 0.18), lines=l)
    # the block: a thick board of cherry wood; the picture cut in it, its edges; the two marks at its near edge
    bx0, bx1 = X0 + 42, X0 + 100
    blk = lerp(OCHRE, SIENNA, 0.45)
    CAM.box(s, bx0, bx1, top_y, top_y + 5, Z0 + 8, Z1 - 4, sunlit(blk, bx0, top_y), shaded(blk, 0.3), top=sunlit(lerp(blk, NAPLES, 0.25), bx0, top_y), lines=l)
    for u in np.linspace(0.25, 0.75, 4):                     # the cut picture: a few dark lines on its face
        p0 = g(bx0 + (bx1 - bx0) * u, Z0 + 16, top_y + 5)
        p1 = g(bx0 + (bx1 - bx0) * (u + 0.06), Z1 - 12, top_y + 5)
        l.line([p0, p1], lerp(SIENNA, PRUSSIAN, 0.4), 0.7, 0.8)
    # the corner mark (an L cut at the near left corner) and the straight mark (a short cut along the near edge, right)
    c0 = g(bx0 + 3, Z1 - 5, top_y + 5.2)
    c1 = g(bx0 + 3, Z1 - 5, top_y + 5.2)
    m = max(3.0, 6.0 * k)
    l.line([(c0[0] + m * 1.6, c0[1]), (c0[0], c0[1]), (c0[0] + m * 0.5, c0[1] - m * 0.8)], PRUSSIAN, max(1.4, 2.0 * k), 1.0)
    info["corner"] = g(bx0 + 4, Z1 - 5, top_y + 5)
    s0 = g(bx0 + 38, Z1 - 5, top_y + 5.2)
    l.line([(s0[0] - m * 0.2, s0[1]), (s0[0] + m * 1.8, s0[1])], PRUSSIAN, max(1.4, 2.0 * k), 1.0)
    info["side"] = g(bx0 + 44, Z1 - 5, top_y + 5)
    # the rubbing pad (baren): a flat round pad in its bamboo sheath, the knot of the sheath on top
    pc = g(X0 + 114, (Z0 + Z1) / 2, top_y + 3)
    s.ellipse(pc[0], pc[1], 10 * k, 4 * k, lerp(STRAW_SH, PRUSSIAN, 0.15))
    s.ellipse(pc[0] - 1.5 * k, pc[1] - 1.4 * k, 7.5 * k, 2.6 * k, sunlit(lerp(STRAW_LIT, NAPLES, 0.2), X0 + 114, top_y))
    l.line([(pc[0] - 2 * k, pc[1] - 2.6 * k), (pc[0] + 2.5 * k, pc[1] - 3.4 * k)], STRAW_SH, max(0.8, 1.6 * k), 1.0)
    info["pad"] = pc
    # two brushes, lying
    for dz in (-6.0, 6.0):
        a = g(X0 + 128, (Z0 + Z1) / 2 + dz, top_y + 1.5)
        b = g(X0 + 140, (Z0 + Z1) / 2 + dz, top_y + 1.5)
        l.line([a, b], WOOD_SH, max(0.8, 1.5 * k), 1.0)
        s.ellipse(b[0] + 1.2, b[1], 2.2 * k, 1.1 * k, PRUSSIAN)
    # the pot of the new blue: a small round bowl, the deep blue in it
    q = g(X0 + 150, (Z0 + Z1) / 2 + 8, top_y)
    s.poly([(q[0] - 5 * k, q[1] - 5 * k), (q[0] + 5 * k, q[1] - 5 * k), (q[0] + 4 * k, q[1]), (q[0] - 4 * k, q[1])], lerp(WHITE, CERULEAN, 0.2))
    s.ellipse(q[0], q[1] - 5 * k, 5 * k, 1.6 * k, lerp(PRUSSIAN, COBALT, 0.25))
    info["pot"] = (q[0], q[1] - 3 * k)
    # the stand at the right end: a small slanted board on a prop, facing the street (it shows the sheet)
    st = g(STAND["X"], STAND["Z"], top_y)
    sw, sh_ = 36 * k, 48 * k
    s.poly([(st[0] - sw / 2, st[1]), (st[0] + sw / 2, st[1]), (st[0] + sw / 2 - 2 * k, st[1] - sh_), (st[0] - sw / 2 + 2 * k, st[1] - sh_)], WOOD_SH)
    l.line([(st[0] + sw / 2 - 1, st[1]), (st[0] + sw / 2 + 4 * k, st[1] + 2 * k)], WOOD_SH, max(0.8, 2 * k), 1.0)
    info["stand"] = (st[0], st[1], sw, sh_)
    return s, l, info


def sheet_on_stand(state, info):
    """The sheet on the stand: 'blank' (fresh paper), 'ghost' (the blue landed a hair to the left: a ghost of the robe
    beside its outline), 'clean' (an actor at home in a robe of the new blue, every colour where it should be)."""
    s, l = sheets()
    st = info["stand"]
    x, y, sw, sh_ = st
    w, h = sw * 0.84, sh_ * 0.86
    x0, y0 = x - w / 2, y - sh_ + (sh_ - h) * 0.4
    rng = np.random.default_rng(5)
    if state == "blank":
        s.poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)], lerp(WHITE, NAPLES, 0.10))
        l.line([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h), (x0, y0)], PRUSSIAN, 0.6, 0.5)
    else:
        newblue = lerp(PRUSSIAN, COBALT, 0.45)                 # Berlin blue: deep and clear
        actor_print(s, l, x0, y0, w, h, rng, kind=0, blue=newblue, offset=(w * 0.16 if state == "ghost" else 0.0), faint=(state == "ghost"))
    return s, l


# ---------------------------------------------------------------- noren, the signboard, the road god, the water-seller
def noren(X0, X1, top, drop, mark, seed, panels=3, c=None):
    """A shop's noren: panels of indigo with a white mark of our own across the middle (no real house's)."""
    s, l = sheets()
    Z = S.ZE + 4
    c = INDIGO if c is None else c
    for i in range(panels):
        u0, u1 = i / panels + 0.01, (i + 1) / panels - 0.01
        a0, a1 = X0 + (X1 - X0) * u0, X0 + (X1 - X0) * u1
        q = [g(a0, Z, top), g(a1, Z, top), g(a1, Z, top - drop), g(a0, Z, top - drop)]
        s.poly(q, sunlit(c, (a0 + a1) / 2, top - drop * 0.3))
        l.line([q[3], q[0], q[1], q[2]], PRUSSIAN, 0.7, 0.65)
    l.line([g(X0 - 5, Z, top + 2), g(X1 + 5, Z, top + 2)], WOOD_SH, max(1.0, 3.5 * CAM.k(X0, Z)), 1.0)
    mx = (X0 + X1) / 2
    cc = g(mx, Z, top - drop * 0.45)
    k = CAM.k(mx, Z)
    wc = lerp(WHITE, CERULEAN, 0.12)
    if mark == "lozenge":
        s.poly([(cc[0], cc[1] - 11 * k), (cc[0] + 9 * k, cc[1]), (cc[0], cc[1] + 11 * k), (cc[0] - 9 * k, cc[1])], wc)
        s.poly([(cc[0], cc[1] - 6 * k), (cc[0] + 5 * k, cc[1]), (cc[0], cc[1] + 6 * k), (cc[0] - 5 * k, cc[1])], c)
    elif mark == "bars":
        for dy in (-6, 0, 6):
            s.line([(cc[0] - 9 * k, cc[1] + dy * k), (cc[0] + 9 * k, cc[1] + dy * k)], wc, max(0.8, 2.6 * k))
    else:                                                    # a ring with a dot
        s.ellipse(cc[0], cc[1], 10 * k, 10 * k, wc)
        s.ellipse(cc[0], cc[1], 7 * k, 7 * k, c)
        s.ellipse(cc[0], cc[1], 2.5 * k, 2.5 * k, wc)
    return s, l


def katakana(sheet, cx, top, size, color, width):
    """ウ ル ユ ス, top to bottom, written in our own plain brush strokes (the signboard's word, a medicine's name):
    each character a few strokes in a box `size` px, the column centred on cx from `top`."""
    def stroke(pts, w=1.0):
        sheet.line(pts, color, width * w, 1.0)
    for i, ch in enumerate("urys"):
        x0, y0 = cx - size / 2, top + i * size * 1.12
        X = lambda u: x0 + size * u
        Y = lambda v: y0 + size * v
        if ch == "u":       # ウ: a tick on top; the short left upright; the top bar turning down and sweeping left
            stroke([(X(0.50), Y(0.02)), (X(0.52), Y(0.20))])
            stroke([(X(0.18), Y(0.26)), (X(0.20), Y(0.50))])
            stroke(curve([(X(0.18), Y(0.27)), (X(0.80), Y(0.25)), (X(0.78), Y(0.55)), (X(0.42), Y(0.96))], 6))
        elif ch == "r":     # ル: a left stroke down and out; a right upright that hooks up to the right
            stroke(curve([(X(0.36), Y(0.10)), (X(0.35), Y(0.55)), (X(0.14), Y(0.92))], 6))
            stroke([(X(0.60), Y(0.06)), (X(0.60), Y(0.84)), (X(0.90), Y(0.56))])
        elif ch == "y":     # ユ: the top bar turning down at its right end; the long bottom bar
            stroke([(X(0.20), Y(0.28)), (X(0.70), Y(0.28)), (X(0.68), Y(0.76))])
            stroke([(X(0.06), Y(0.78)), (X(0.94), Y(0.78))])
        else:               # ス: the bar and the long sweep down to the left; the short stroke down to the right
            stroke(curve([(X(0.20), Y(0.16)), (X(0.78), Y(0.16)), (X(0.56), Y(0.52)), (X(0.12), Y(0.92))], 6))
            stroke([(X(0.50), Y(0.56)), (X(0.86), Y(0.90))])


SIGN = dict(X=1145.0, Z=-1255.0, base=28.0, h=190.0, w=46.0)


def signboard():
    """The medicine shop's big standing signboard: a tall board of black lacquer in a frame with a little gabled cap,
    on a low stand, the medicine's name 'Uruyusu' in white down it (katakana, in our own hand); it stands in the street
    before the shop."""
    s, l = sheets()
    X, Z = SIGN["X"], SIGN["Z"]
    k = CAM.k(X, Z)
    b0, b1 = g(X, Z, SIGN["base"]), g(X, Z, SIGN["base"] + SIGN["h"])
    w = SIGN["w"] * k
    # the stand (two feet), the board, the frame, the cap
    for dx in (-0.4, 0.4):
        l.line([g(X + dx * SIGN["w"], Z, 0), g(X + dx * SIGN["w"], Z, SIGN["base"])], WOOD_SH, max(1.0, 5 * k), 1.0)
    l.line([g(X - SIGN["w"] * 0.6, Z, 2), g(X + SIGN["w"] * 0.6, Z, 2)], WOOD_SH, max(1.0, 6 * k), 1.0)
    board = [(b0[0] - w / 2, b0[1]), (b0[0] + w / 2, b0[1]), (b1[0] + w / 2, b1[1]), (b1[0] - w / 2, b1[1])]
    s.poly(board, sunlit(lerp(SIENNA, PRUSSIAN, 0.55), X, SIGN["base"] + SIGN["h"] * 0.5, Z))
    s.poly([(b1[0] - w * 0.62, b1[1] + 1), (b1[0] + w * 0.62, b1[1] + 1), (b1[0], b1[1] - w * 0.36)], sunlit(TILE_LIT, X, SIGN["base"] + SIGN["h"], Z))
    l.line(board + [board[0]], WOOD_LIT, max(1.0, 3 * k), 1.0)
    size = w * 0.66
    katakana(s, b0[0], b1[1] + w * 0.35, size, lerp(WHITE, NAPLES, 0.15), max(1.3, size * 0.13))
    return s, l, dict(box=[int(b1[0] - w * 0.65) - 2, int(b1[1] - w * 0.4) - 2, int(w * 1.3) + 4, int(b0[1] - b1[1] + w * 0.4 + SIGN["base"] * k) + 4])


ROADGOD = dict(X=318.0, Z=-1252.0)


def roadgod():
    """The road god at the corner: a small rounded stone on a low stone base, a figure carved in it (a little standing
    figure in relief, worn), a cup of water and a sprig before it. Child height. In the band of sun."""
    s, l = sheets()
    X, Z = ROADGOD["X"], ROADGOD["Z"]
    k = CAM.k(X, Z)
    stone_l, stone_s = lerp(STONE_LIT, NAPLES, 0.15), STONE_SH
    CAM.box(s, X - 22, X + 22, 0, 12, Z - 18, Z + 18, stone_l, stone_s, top=stone_l, lines=l)
    p = g(X, Z + 10, 12)
    w, h = 30 * k, 52 * k
    body = [(p[0] - w / 2, p[1])] + [(p[0] - w / 2 * math.cos(t), p[1] - h * 0.62 - h * 0.38 * math.sin(t)) for t in np.linspace(0, math.pi, 12)] + [(p[0] + w / 2, p[1])]
    s.poly(body, stone_l)
    s.poly([(p[0], p[1])] + body[7:], stone_s)
    # the carved figure: an oval niche with a little figure, hands together
    s.ellipse(p[0] - w * 0.04, p[1] - h * 0.48, w * 0.3, h * 0.36, lerp(stone_s, stone_l, 0.4))
    s.ellipse(p[0] - w * 0.04, p[1] - h * 0.66, w * 0.1, w * 0.1, stone_l)
    s.poly([(p[0] - w * 0.18, p[1] - h * 0.18), (p[0] + w * 0.1, p[1] - h * 0.18), (p[0] + w * 0.04, p[1] - h * 0.56), (p[0] - w * 0.12, p[1] - h * 0.56)], stone_l)
    l.line(body, PRUSSIAN, 0.9, 0.65)
    c = g(X - 12, Z + 24, 12)
    s.ellipse(c[0], c[1], 3.2 * k, 1.4 * k, lerp(WHITE, CERULEAN, 0.2))
    l.line([(c[0] + 6 * k, c[1]), (c[0] + 8 * k, c[1] - 8 * k)], VIRIDIAN, max(0.8, 1.4 * k), 1.0)
    return s, l, dict(top=(p[0], p[1] - h))


VENDOR = dict(X=1240.0, Z=-1150.0)


def watervendor():
    """A water-seller resting by the comb-maker's: his pole across his shoulder, a covered bucket hung from each end
    (fresh water was sold in the street); robe tucked up, a head cloth. Painted, as the crowd at the shore is."""
    s, l = sheets()
    X, Z = VENDOR["X"], VENDOR["Z"]
    p = g(X, Z)
    k = CAM.k(X, Z)
    hpx = 156 * k
    rng = np.random.default_rng(8)
    # the buckets either side, on the ground (he has set them down), the pole leaning on his shoulder
    for dx in (-48.0, 48.0):
        q = g(X + dx, Z - 6)
        s.poly([(q[0] - 15 * k, q[1] - 36 * k), (q[0] + 15 * k, q[1] - 36 * k), (q[0] + 13 * k, q[1]), (q[0] - 13 * k, q[1])], sunlit(WOOD_LIT, X + dx, 30, Z))
        s.ellipse(q[0], q[1] - 36 * k, 15 * k, 4 * k, lerp(STRAW_LIT, NAPLES, 0.2))                 # the lid
        l.line([(q[0] - 14 * k, q[1] - 12 * k), (q[0] + 14 * k, q[1] - 12 * k)], WOOD_DARK, max(0.8, 2.2 * k), 0.9)
        l.line([(q[0] - 12 * k, q[1] - 36 * k), (q[0], q[1] - 62 * k), (q[0] + 12 * k, q[1] - 36 * k)], STRAW_SH, max(0.7, 1.2 * k), 0.9)   # the rope
    pa, pb = g(X - 50, Z - 6, 62), g(X + 50, Z - 6, 136)
    figure(s, p[0], p[1], hpx, rng, robe=lerp(tintw(CERULEAN, 0.35), PRUSSIAN, 0.3), sleeves="down", head_cloth=True, tucked=True, turn=0.3)
    l.line([pa, pb], WOOD_LIT, max(1.0, 4 * k), 1.0)
    return s, l, dict(box=[int(p[0] - 70 * k), int(p[1] - hpx - 6), int(140 * k), int(hpx + 8)])

"""PAINT-21B: Gonroku's coaster at sea, the fifth day out, off Daiozaki, noon, about 13 April 1830 (edo-deck). In the
woodblock manner of the act's style sheet (S/work-20-paintA/style.md): flat masses, a graded sky, one fine contour in
prussian blue, few paints, the blue leading; the brightest painting in the act (the key edo-sea).

LIGHT   Noon: the sun high in the south, behind us and a little to the left (edo_deck_kit.SUN3): the sail's face, the
        mats, the planks and every face turned to us are lit; the shadows are short, falling away and a little right,
        flat and blue.
DEPTH   horizon 262, full 590 (persp.Camera; everything standing is drawn through it). The near (port) side is cut away.
TONES   light: the sail (the brightest thing), the sky's paper, the mats in the sun. middle: the deck, the sea's far
        bands, the cape. dark: the sea's near rows (prussian), the boat, the mast, the windlass, the stem, the contour.
        The sail owns the top; the mast leads the eye down to the deck; the hearth box (left of the mast) and the
        compass box (right, by the tiller) are where the puzzles are.
PLACE   (edo_deck_kit: THE SHIP) From the left: the stem rising at the bow; the forward hold under its mats with the
        ship's boat lashed upside down on it, Kota's hearth box in front of it; the mast and its step in the gangway;
        the aft hold, Seijiro's bale; the windlass; the compass box on its post; the long tiller and the stern
        deckhouse. Beyond the far bulwark, the sea in rows and, far off the starboard bow, the grey cape of Daiozaki.

  python3 edo_deck.py fast     the composition without the brush pass (out/edo-deck-1-under.png, -2-all.png)
  python3 edo_deck.py          the full passes: out/edo-deck/ (back.png, the cut-outs, the frames, layout.json)
"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
import land
from edo_deck_kit import *
import edo_deck_kit as K

SEED = 1313
OUT = "out/edo-deck"
SWELL_ROWS = (HZ - 24, HZ + 36)                                  # the swell layer: the cape above the horizon, the far sea below it
SKY_UNDER = 3                                                    # the backdrop's sky runs this far below the horizon, under the swell layer


def segs(colors_rows, shape=SHAPE, soft=5.0, wobble=2.0, seed=0, patch=0.02):
    """Level bands, each [top row, colour], top to bottom (the last runs to the picture's bottom): the act's bands()."""
    rows = [r for r, _ in colors_rows]
    cols = [c for _, c in colors_rows]
    return bands(shape, rows + [shape[0]], [cols[0]] + cols, soft=soft, wobble=wobble, seed=seed, patch=patch)


# ================================================================ pass 1: broad and flat
def paint_sky(seed):
    """The graded band (style.md section 3): cobalt high up (most of it behind the sail), the paper at the horizon;
    seven bands. It runs SKY_UNDER rows below the horizon, under the swell layer."""
    pic = segs([(0, shade(COBALT, 0.26)), (44, mixp(COBALT, ULTRA, 0.12)), (88, COBALT), (132, mixp(COBALT, CERULEAN, 0.5)),
                (172, CERULEAN), (206, tintw(CERULEAN, 0.48)), (234, PAPER), (HZ + SKY_UNDER + 1, PAPER)], soft=6.0, wobble=2.5, seed=seed)
    x, y = grid(SHAPE)
    # the sun is high behind us: the paper is a shade warmer low down on the left
    glow(pic, tintw(NAPLES, 0.55), (np.clip(1 - x / 520.0, 0, 1) * np.clip(1 - np.abs(y - 246) / 60.0, 0, 1) * 0.08).astype(F32))
    return pic


def paint_sea(pic, seed, top):
    """The sea from row `top` down, in bands (style.md section 3): pale at the horizon, cerulean, cobalt, then
    ultramarine and prussian blue toward the ship; and the long swell as rows a step darker (the waves' crests are
    the engine's: fx sea-rows)."""
    x, y = grid(SHAPE)
    sea = segs([(HZ, tintw(CERULEAN, 0.34)), (HZ + 4, tintw(CERULEAN, 0.18)), (HZ + 9, mixp(CERULEAN, COBALT, 0.18)), (HZ + 15, mixp(CERULEAN, COBALT, 0.40)),
                (HZ + 23, mixp(CERULEAN, COBALT, 0.72)), (HZ + 33, COBALT), (HZ + 47, mixp(COBALT, ULTRA, 0.45)), (HZ + 66, ULTRA),
                (HZ + 92, mixp(ULTRA, PRUSSIAN, 0.26)), (HZ + 126, mixp(ULTRA, PRUSSIAN, 0.40))],
               soft=3.0, wobble=0.0, seed=seed + 20, patch=0.012)
    # the swell's rows: long low troughs, a step darker, closer together toward the horizon (laid as pattern, still)
    rows = np.zeros(SHAPE, F32)
    for i in range(1, 40):
        zz = 2600.0 / i ** 1.25 * 22.0                                   # distance of the i-th trough (cm), far to near
        r = sea_row(zz)
        if r < HZ + 6 or r > H:
            continue
        wv = 0.6 + 1.6 * (r - HZ) / 140.0
        band = np.exp(-((y - r - np.sin(x / (60 + 3 * i) + i) * (0.5 + 0.6 * wv)) ** 2) / (2 * (0.6 + 0.9 * wv) ** 2))
        rows = np.maximum(rows, band.astype(F32) * (0.55 if i % 2 else 0.35))
    darker = lerp(sea, PRUSSIAN, 0.22)
    sea = lerp(sea, darker, (rows * np.clip((y - HZ - 6) / 30.0, 0, 1))[..., None])
    m = (y >= top).astype(F32)
    over(pic, sea, m)
    return pic


def cape_mask(seed):
    """Daiozaki and the coast of Shima behind it: far off the starboard bow, a low grey headland on the horizon at the
    left, its tip falling to the sea at about x 238, the coast behind it rising a little to the left edge."""
    pts = [(-10, HZ + 1), (-10, HZ - 17), (30, HZ - 19), (62, HZ - 16), (96, HZ - 18), (130, HZ - 14), (160, HZ - 15), (186, HZ - 11),
           (204, HZ - 12), (218, HZ - 8), (228, HZ - 6), (236, HZ - 2), (241, HZ + 1)]
    return mask_poly(SHAPE, pts, soft=0.6, wobble=0.8, seed=seed + 5)


def paint_cape(pic, seed):
    """The far cape: no contour (beyond a kilometre), two flats pulled well toward the paper and toward blue (style.md
    section 7): the lit face (toward the sun, the south: toward us) and the shade under its brow; a white thread of surf
    at its foot; a far islet off its tip."""
    x, y = grid(SHAPE)
    m = cape_mask(seed)
    lit_c = lerp(tintw(mixp(COBALT, PRUSSIAN, 0.25), 0.50), PAPER, 0.22)
    shade_c = lerp(tintw(mixp(COBALT, ULTRA, 0.40), 0.36), PAPER, 0.18)
    over(pic, flat(lit_c, SHAPE, seed + 6, 0.025, 60), m)
    # the shade: the slopes turned away (to the right, beyond each brow), one flat
    sh = mask_poly(SHAPE, [(96, HZ - 18), (112, HZ - 12), (130, HZ - 6), (140, HZ + 1), (110, HZ + 1)], soft=0.6, seed=seed + 7) \
        + mask_poly(SHAPE, [(204, HZ - 12), (214, HZ - 6), (222, HZ + 1), (206, HZ + 1)], soft=0.6, seed=seed + 8) \
        + mask_poly(SHAPE, [(30, HZ - 19), (44, HZ - 11), (50, HZ + 1), (36, HZ + 1)], soft=0.6, seed=seed + 9)
    over(pic, shade_c, (np.clip(sh, 0, 1) * m).astype(F32))
    # the foot paler (the air over the water), and a thread of surf
    over(pic, PAPER, (m * np.clip((y - (HZ - 6)) / 7.0, 0, 1) * 0.35).astype(F32))
    over(pic, tintw(CERULEAN, 0.85), (mask_poly(SHAPE, [(150, HZ), (240, HZ), (240, HZ + 1.2), (150, HZ + 1.2)], soft=0.4) * 0.7).astype(F32))
    # an islet off the tip
    isl = mask_poly(SHAPE, [(252, HZ + 0.8), (255, HZ - 3), (259, HZ - 3.6), (263, HZ - 1.5), (266, HZ + 0.8)], soft=0.4, seed=seed + 10)
    over(pic, lerp(shade_c, PAPER, 0.1), isl)
    return np.clip(m + isl, 0, 1)


# ---------------------------------------------------------------- the ship, broad
def deck_mask():
    """Where the deck's planks are seen (before anything stands on them): from the near side to the far bulwark,
    closing to the stem at the bow."""
    pts_far = [gp(x_, far_z(x_)) for x_ in np.linspace(BOW_X, STERN_X + 200, 60)]
    poly = [gp(BOW_X, CL)] + pts_far + [(W + 20, H + 20), (-20, H + 20), (-20, gp(-560, 60)[1])]
    return mask_poly(SHAPE, poly, soft=0.6)


def paint_deck(pic, seed):
    """The deck: planks running fore and aft (bow to stern: level lines in the picture), each a flat of weathered ochre
    in the noon sun, a little paler far off; the plank seams drawn in details()."""
    x, y = grid(SHAPE)
    X, Z, below = floor()
    m = deck_mask() * below
    plank = np.floor(Z / 19.0)
    tone = np.sin(plank * 12.9898 + 3.1) * 43758.5453
    tone = (tone - np.floor(tone)) - 0.5
    wood = flat(WOOD_LIT, SHAPE, seed + 30, 0.035, 40)
    wood = wood * (1 + 0.05 * tone[..., None])
    t = np.clip((y - HZ) / (H - HZ), 0, 1)
    wood = lerp(wood, PAPER, ((1 - t) ** 2 * 0.25)[..., None])
    over(pic, np.clip(wood, 0, 1), m)
    return m


def paint_far_bulwark(pic, sheet, seed):
    """The far bulwark: its inner face (toward us: lit), its cap rail, the stanchions; it rises to the stem at the bow and
    a little to the stern. Only the bow's and the stern's stretches show over the cargo."""
    xs = np.linspace(BOW_X, STERN_X + 220, 70)
    top = [gp(x_, far_z(x_), sheer(x_)) for x_ in xs]
    foot = [gp(x_, far_z(x_)) for x_ in xs]
    sheet.poly(top + foot[::-1], lerp(WOOD_MID, SIENNA, 0.12))
    # its shade: the cap rail throws a band of shadow down the face
    cap_sh = [gp(x_, far_z(x_), sheer(x_) - 12) for x_ in xs]
    sheet.poly(top + cap_sh[::-1], lerp(WOOD_MID, COBALT, 0.28))
    # the cap rail: a heavy timber along the top, seen from above (lit), its outer edge a line
    cap_out = [gp(x_, far_z(x_) + 18, sheer(x_) + 2) for x_ in xs]
    sheet.poly(cap_out + top[::-1], tintw(OCHRE, 0.42))
    # stanchions (the frames' heads) every 80 cm
    for x_ in np.arange(BOW_X + 60, STERN_X + 200, 80.0):
        z_ = far_z(x_)
        sheet.line([gp(x_, z_ - 3, 2), gp(x_, z_ - 3, sheer(x_) - 12)], lerp(WOOD_MID, SIENNA, 0.35), max(1.0, 9 * kz(z_)), 1.0)
    contour(sheet, cap_out, row_of(500))
    contour(sheet, top, row_of(500), alpha=0.45)
    return top


def paint_stem(sheet, lines):
    """The stem: the single heavy timber of the bow (facts-21a item 6), rising from the deck at BOW_X and leaning forward
    out of the picture at its left edge, iron-banded; and the last of the near bulwark meeting it (the rest of the near
    side is cut away)."""
    th, lean, top = 46.0, 0.36, 360.0
    base_l, base_r = gp(BOW_X - th / 2, CL), gp(BOW_X + th / 2, CL)
    top_l, top_r = gp(BOW_X - th / 2 - lean * top, CL, top), gp(BOW_X + th / 2 - lean * top, CL, top)
    sheet.poly([base_l, base_r, top_r, top_l], lerp(WOOD_MID, SIENNA, 0.22))
    # its face toward the stern and the picture's middle: away from the sun's side, a shade flat on its right third
    m_b, m_t = gp(BOW_X + th * 0.12, CL), gp(BOW_X + th * 0.12 - lean * top, CL, top)
    sheet.poly([m_b, base_r, top_r, m_t], WOOD_SHADE)
    # iron bands
    for hh in (150.0, 238.0, 300.0):
        a_ = gp(BOW_X - th / 2 - lean * hh - 2, CL, hh - 3)
        b_ = gp(BOW_X + th / 2 - lean * hh + 2, CL, hh + 3)
        lines.line([a_, b_], IRON, 3.0, 1.0)
        lines.line([(a_[0], a_[1] - 1.6), (b_[0], b_[1] - 1.6)], lerp(IRON, CERULEAN, 0.4), 0.8, 0.8)
    contour(lines, [base_l, top_l], row_of(CL), warm=True)
    contour(lines, [base_r, top_r], row_of(CL))
    # the last of the near bulwark, coming in to the stem at the picture's left edge
    xs = np.linspace(BOW_X - 4, -455.0, 12)
    nz = [CL - half_width(x_) for x_ in xs]
    tp = [gp(x_, z_, sheer(x_) + 6) for x_, z_ in zip(xs, nz)]
    ft = [gp(x_, z_) for x_, z_ in zip(xs, nz)]
    inner = [gp(x_, z_ + 18, sheer(x_) + 6) for x_, z_ in zip(xs, nz)]
    sheet.poly(tp + ft[::-1], lerp(WOOD_SHADE, PRUSSIAN, 0.15))       # its inner face, turned from the sun
    sheet.poly(inner + tp[::-1], tintw(OCHRE, 0.36))                   # its cap rail, lit
    contour(lines, tp, row_of(80), warm=True)
    contour(lines, ft, row_of(80))


def paint_coaming_and_cargo(sheet, lines, seed):
    """The two holds: the coaming (a low timber edge), the cargo heaped above the bulwark under straw mat covers lashed
    with ropes, and the forward hold's end toward the gangway (the stacked bales and casks under a hanging mat)."""
    rng = np.random.default_rng(seed)
    out = {}
    for name, (xa, xb) in (("fwd", HOLD_F), ("aft", HOLD_A)):
        xs = np.linspace(xa, xb, 40)
        # the profile across the ship (z, y): the coaming's top, the near slope rounding over, the crown (heaped above
        # the bulwark, as a laden coaster's was: facts-21a item 6), the far side going down behind it
        prof = [(WALK_Z, 34.0), (WALK_Z + 4, 92.0), (WALK_Z + 9, 150.0), (WALK_Z + 22, 186.0), (WALK_Z + 60, 201.0),
                (WALK_Z + 150, CARGO_TOP), (WALK_Z + 270, CARGO_TOP + 2), (WALK_Z + 330, CARGO_TOP - 8)]

        cut_a, cut_b = (0.52, 0.70) if name == "fwd" else (0.56, 0.56)   # how high each end stands (the forward hold's end at the gangway is a stack)

        def at(x_, i, xa=xa, xb=xb, cut_a=cut_a, cut_b=cut_b):
            zf = far_z(x_) - 24
            z_, y_ = prof[i]
            z_ = min(z_, zf - 6 * (len(prof) - i))
            # the cargo is a long heap, its ends steep: the mats drape down over them toward the coaming; at the forward
            # hold's end by the gangway it stands as a stack of bales and casks, only its top edge rounded
            fa = cut_a + (1 - cut_a) * math.sqrt(max(0.0, 1.0 - (1.0 - min(1.0, (x_ - xa) / 42.0)) ** 2))
            fb = cut_b + (1 - cut_b) * math.sqrt(max(0.0, 1.0 - (1.0 - min(1.0, (xb - x_) / 36.0)) ** 2))
            y_ = 34.0 + (y_ - 34.0) * min(fa, fb) if i > 0 else y_
            return (x_, y_, z_)
        # the coaming: front face (lit) and top
        sheet.poly([gp(xa, WALK_Z), gp(xb, WALK_Z), gp(xb, WALK_Z, 34), gp(xa, WALK_Z, 34)], WOOD_MID)
        sheet.poly([gp(xa, WALK_Z, 34), gp(xb, WALK_Z, 34), gp(xb, WALK_Z + 12, 34), gp(xa, WALK_Z + 12, 34)], tintw(OCHRE, 0.40))
        # the mats, strip by strip from the far side to the near slope (back to front): the crown in full sun, the near
        # slope a little less, its foot by the coaming turned down out of the light
        cols = [None, lerp(MAT_LIT, MAT_SHADE, 0.34), lerp(MAT_LIT, MAT_SHADE, 0.22), lerp(MAT_LIT, MAT_SHADE, 0.06), lerp(MAT_LIT, NAPLES, 0.12),
                lerp(MAT_LIT, NAPLES, 0.22), lerp(MAT_LIT, NAPLES, 0.20), lerp(MAT_LIT, MAT_SHADE, 0.2)]
        for i in range(len(prof) - 1, 0, -1):
            a_ = [P3(at(x_, i)) for x_ in xs]
            b_ = [P3(at(x_, i - 1)) for x_ in xs]
            sheet.poly(a_ + b_[::-1], cols[i])
        # each mat about 90 cm along the ship, a hair different in tone, overlapping: their edges as lines over the crown
        # and down the near slope, and the weave as a few short strokes
        edges = np.arange(xa + 30.0 + rng.uniform(0, 25), xb - 15, 88.0)
        for j, x_ in enumerate(edges):
            pts = [P3(at(x_, i)) for i in range(len(prof) - 1, 0, -1)]
            lines.line(pts, lerp(MAT_LIT, SIENNA, 0.5), 0.8, 0.6)
            if j % 2 == 0 and j + 1 < len(edges):
                for i in range(len(prof) - 1, 1, -1):
                    q = [P3(at(x2, i)) for x2 in (x_, edges[j + 1])] + [P3(at(x2, i - 1)) for x2 in (edges[j + 1], x_)]
                    sheet.poly(q, lerp(MAT_LIT, OCHRE, 0.12), 0.35)
        for _ in range(int((xb - xa) / 9)):
            x_ = rng.uniform(xa + 20, xb - 20)
            i = int(rng.integers(2, len(prof) - 1))
            p_ = P3(at(x_, i))
            q_ = P3(at(x_ + rng.uniform(8, 16), i))
            lines.line([p_, q_], lerp(MAT_LIT, OCHRE, 0.55), 0.6, 0.4)
        # the straw's weave: fine level lines across each mat (the near face and the shoulder), a little darker than the mat
        for i in (1, 2, 3):
            for v in np.linspace(0.15, 0.85, 4 if i < 3 else 3):
                pts = []
                for x_ in xs:
                    qa, qb = at(x_, i - 1), at(x_, i)
                    pts.append(P3((x_, qa[1] + (qb[1] - qa[1]) * v, qa[2] + (qb[2] - qa[2]) * v)))
                lines.line(pts, lerp(MAT_LIT, OCHRE, 0.6), 0.6, 0.30)
        # under the mats' hem, along the coaming, the cargo shows: a row of rice-straw bales lying across the ship, their
        # round ends toward us (straw, a dark knot of rope at the middle), a cask's head here and there
        hem_y = 62.0
        for j, x_ in enumerate(np.arange(xa + 26.0, xb - 20.0, 44.0)):
            f_ = min(1.0, (x_ - xa) / 30.0, (xb - x_) / 30.0)
            if f_ < 0.6:
                continue
            c0 = gp(x_, WALK_Z + 8, 51)
            k = kz(WALK_Z + 8)
            if (j + (1 if name == "aft" else 0)) % 4 == 2:
                sheet.ellipse(c0[0], c0[1], 19 * k, 17 * k, lerp(SIENNA, OCHRE, 0.35))
                for rr in (0.55, 0.92):
                    lines.line([(c0[0] + 19 * k * rr * math.cos(t_), c0[1] + 17 * k * rr * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 18)],
                               lerp(OCHRE, VIRIDIAN, 0.15) if rr > 0.9 else WOOD_DARK, 1.0 if rr > 0.9 else 0.6, 0.9)
            else:
                sheet.ellipse(c0[0], c0[1], 20 * k, 17 * k, lerp(MAT_LIT, OCHRE, 0.30))
                sheet.ellipse(c0[0], c0[1] + 1, 8 * k, 7 * k, lerp(OCHRE, SIENNA, 0.35))
                for t_ in np.linspace(0, 2 * math.pi, 10, endpoint=False):
                    lines.line([(c0[0] + 9 * k * math.cos(t_), c0[1] + 8 * k * math.sin(t_)), (c0[0] + 19 * k * math.cos(t_), c0[1] + 16 * k * math.sin(t_))],
                               lerp(OCHRE, SIENNA, 0.25), 0.6, 0.6)
            contour(lines, [(c0[0] + 20 * k * math.cos(t_), c0[1] + 17 * k * math.sin(t_)) for t_ in np.linspace(math.pi * 0.95, math.pi * 2.05, 14)], c0[1], alpha=0.45)
        # the mats' hem over them: a bound edge, a little wavy
        hem = [P3((x_, hem_y + 3 * math.sin(x_ / 23.0), at(x_, 1)[2] - 1)) for x_ in xs]
        lines.line(hem, lerp(SIENNA, PRUSSIAN, 0.2), max(1.4, 3.2 * kz(WALK_Z)), 0.95)
        # the lashings: ropes across the cargo from the coaming over the crown, and one along the shoulder
        for x_ in np.arange(xa + 60.0, xb - 30, 110.0):
            pts = [P3((x_ + 4, at(x_, i)[1] + 2, at(x_, i)[2])) for i in range(len(prof) - 1, 0, -1)] + [gp(x_ + 4, WALK_Z + 1, 26)]
            lines.line(pts, ROPE_DARK, max(1.0, 3.4 * kz(WALK_Z)), 0.95)
        lines.line([P3((x_, at(x_, 3)[1] + 2, at(x_, 3)[2])) for x_ in xs], ROPE_DARK, max(1.0, 3.0 * kz(WALK_Z + 44)), 0.9)
        lines.line([P3((x_, at(x_, 2)[1], at(x_, 2)[2] - 1)) for x_ in xs], lerp(MAT_LIT, SIENNA, 0.5), 0.8, 0.6)
        lines.line([P3((x_, at(x_, 1)[1] - 18, at(x_, 1)[2] - 1)) for x_ in xs], lerp(MAT_LIT, SIENNA, 0.45), 0.7, 0.5)
        # the crown's line against the sea (the contour), the coaming's
        crown = [P3(at(x_, 6)) for x_ in xs]
        contour(lines, crown, row_of(420), alpha=0.6)
        contour(lines, [gp(xa, WALK_Z), gp(xb, WALK_Z)], row_of(WALK_Z))
        contour(lines, [gp(xa, WALK_Z, 34), gp(xb, WALK_Z, 34)], row_of(WALK_Z), alpha=0.5)
        out[name] = (xs, at, prof)
    return out


def paint_hold_end(sheet, lines, seed, hold):
    """The forward hold's end toward the gangway (x = HOLD_F[1], facing the picture's middle and turned from the sun: in
    shade): the cargo stacked from the deck up, bales of straw (their round ends) and casks (their heads, hooped), and
    the mat over the top hanging down a little at its edge."""
    rng = np.random.default_rng(seed)
    xs, at, prof = hold
    xe = HOLD_F[1]
    heads = []
    top = [at(xe, i) for i in range(len(prof))]
    zf = top[-1][2]
    face = [P3(q) for q in top] + [gp(xe, zf), gp(xe, WALK_Z)]
    sheet.poly(face, lerp(lerp(OCHRE, SIENNA, 0.35), COBALT, 0.42))

    def height_at(z_):
        zs = [q[2] for q in top]
        ys = [q[1] for q in top]
        return float(np.interp(z_, zs, ys))
    # the stack: rows of bale ends and cask heads, each 40 cm across, wherever they fit under the top
    for row_y in (26.0, 78.0, 130.0):
        for j, z_ in enumerate(np.arange(WALK_Z + 30 + (row_y % 52) * 0.5, zf - 22, 56.0)):
            if row_y + 25 > height_at(z_) - 6:
                continue
            c = gp(xe, z_, row_y)
            k = kz(z_)
            r = 25.0 * k
            if (j * 3 + int(row_y)) % 5 == 2:                            # a cask lying in the stack: its round head, hooped
                heads.append(c)
                sheet.ellipse(c[0], c[1], r * 0.30, r * 0.96, lerp(lerp(SIENNA, OCHRE, 0.3), COBALT, 0.35))
                lines.line([(c[0], c[1] - r * 0.96), (c[0] + r * 0.30, c[1]), (c[0], c[1] + r * 0.96), (c[0] - r * 0.30, c[1]), (c[0], c[1] - r * 0.96)],
                           lerp(OCHRE, COBALT, 0.25), 0.9, 0.8)
                lines.line([(c[0] - r * 0.06, c[1] - r * 0.5), (c[0] - r * 0.06, c[1] + r * 0.5)], lerp(SIENNA, PRUSSIAN, 0.5), 0.8, 0.8)
            else:                                                        # a bale end: straw, a dark core where it was tied
                sheet.ellipse(c[0], c[1], r * 0.33, r, lerp(lerp(OCHRE, NAPLES, 0.25), COBALT, 0.30))
                sheet.ellipse(c[0] - r * 0.04, c[1], r * 0.14, r * 0.42, lerp(lerp(OCHRE, SIENNA, 0.4), COBALT, 0.32))
            contour(lines, [(c[0], c[1] - r), (c[0] + r * 0.33, c[1]), (c[0], c[1] + r)], c[1], alpha=0.35)
    # the mat over the top, hanging down a hand's breadth at its edge
    hang = [P3((xe + 3, q[1] + 2, q[2])) for q in top[2:]] + [P3((xe + 3, q[1] - 22, q[2])) for q in top[2:][::-1]]
    sheet.poly(hang, lerp(MAT_LIT, MAT_SHADE, 0.75))
    lines.line([P3((xe + 3, q[1] - 22, q[2])) for q in top[2:]], lerp(SIENNA, PRUSSIAN, 0.3), 0.8, 0.7)
    contour(lines, face[:len(top)] + [face[0]], row_of(WALK_Z + 60), alpha=0.5)
    contour(lines, [gp(xe, WALK_Z), P3(top[0])], row_of(WALK_Z), alpha=0.6)
    return heads


def paint_boat(sheet, lines, shadows):
    """The ship's boat (tenma-sen: facts-21a item 6, carried aboard), lashed upside down on the forward hold's mats: its
    flat bottom (now its top) lit by the high sun, its near side's planking lit, its square stern toward the gangway in
    shade, its bow at the left raked down to the mats (upside down, the rise of its bottom runs down)."""
    b = BOAT
    zc, x0, x1, hb = b["z"], b["x0"], b["x1"], b["h"]
    half = b["beam"] * 0.5
    base_y = CARGO_TOP - 4                                              # the gunwales sit down into the mats a little
    n = 22
    near_g, far_g, near_k, far_k = [], [], [], []
    for i in range(n + 1):
        u = i / n
        x_ = x0 + (x1 - x0) * u
        bow = max(0.0, (0.34 - u) / 0.34)                               # 1 at the bow, 0 from a third of the way aft
        hw = half * (0.98 - 0.70 * bow ** 1.6)
        bot = hw * 0.70
        drop = hb * 0.88 * bow ** 1.35                                  # the bottom runs down to the stem at the bow
        near_g.append((x_, base_y + 3 * bow, zc - hw))
        far_g.append((x_, base_y + 3 * bow, zc + hw))
        near_k.append((x_, base_y + hb - drop, zc - bot))
        far_k.append((x_, base_y + hb - drop, zc + bot))
    # its shadow on the mats, beyond and to the right (short: the sun is high)
    shadows.append([gp(q[0] + SUN[0] * 50, q[2] + SUN[1] * 50, base_y) for q in far_k] + [gp(q[0], q[2], base_y) for q in near_g[::-1]])
    # the bottom (upside down: on top), seen from above and lit
    sheet.poly([P3(q) for q in near_k] + [P3(q) for q in far_k[::-1]], lerp(lerp(WOOD_LIT, SIENNA, 0.30), NAPLES, 0.08))
    # the near side, sloping from the bottom down and out to the gunwale: lit, a step darker
    sheet.poly([P3(q) for q in near_g] + [P3(q) for q in near_k[::-1]], lerp(WOOD_MID, SIENNA, 0.38))
    # the square stern at x1 (facing the picture's middle, turned from the sun): shade
    sheet.poly([P3(near_g[-1]), P3(far_g[-1]), P3(far_k[-1]), P3(near_k[-1])], lerp(WOOD_SHADE, PRUSSIAN, 0.2))
    # planks along the near side, the bottom's middle plank, the gunwale's rubbing strake (dark)
    for v in (0.34, 0.67):
        lines.line([P3((a_[0], a_[1] + (c_[1] - a_[1]) * v, a_[2] + (c_[2] - a_[2]) * v)) for a_, c_ in zip(near_g, near_k)], PRUSSIAN, 0.6, 0.38)
    lines.line([P3((q[0], q[1] + 1, q[2] - 1.5)) for q in near_g], WOOD_DARK, 2.0, 1.0)
    lines.line([P3((q[0], q[1], zc)) for q in near_k], lerp(WOOD_SHADE, PRUSSIAN, 0.2), 0.8, 0.6)
    # the lashings over it, down to the mats on the near side
    for u in (0.42, 0.80):
        i = int(u * n)
        lines.line([P3((far_k[i][0], far_k[i][1], far_k[i][2])), P3(near_k[i]), P3(near_g[i]), P3((near_g[i][0] - 4, base_y - 18, near_g[i][2] - 26))], ROPE_DARK, 1.6, 0.95)
    r0 = row_of(zc)
    contour(lines, [P3(q) for q in near_k] + [P3(far_k[-1])], r0, warm=True)
    contour(lines, [P3(q) for q in near_g] + [P3(far_g[-1]), P3(far_k[-1])], r0)
    contour(lines, [P3(near_g[0]), P3(near_k[0]), P3(far_k[0])], r0, alpha=0.6)


def paint_step(sheet, lines, shadows):
    """The mast step at the mast's foot: a heavy block of timber, bound with iron, a square plug in its face (the
    Funadama is sealed in it), nailed."""
    s = STEP
    for name, quad, nrm in box_faces(s["x0"], s["x1"], 0.0, s["h"], s["z0"], s["z1"]):
        col = {"front": WOOD_MID, "top": tintw(OCHRE, 0.32), "right": WOOD_SHADE, "left": WOOD_SHADE}[name]
        sheet.poly([P3(q) for q in quad], col)
    # iron bands round it
    for hh in (10, 38):
        lines.line([gp(s["x0"], s["z0"], hh), gp(s["x1"], s["z0"], hh), gp(s["x1"], s["z1"], hh)], IRON, max(1.0, 4 * kz(s["z0"])), 0.95)
    # the plug: a square of other wood, nailed at its corners (Big Sister: "Also it's nailed.")
    cx_, cy_ = (s["x0"] + s["x1"]) / 2, s["h"] * 0.5
    q = [gp(cx_ - 14, s["z0"] - 0.5, cy_ - 11), gp(cx_ + 14, s["z0"] - 0.5, cy_ - 11), gp(cx_ + 14, s["z0"] - 0.5, cy_ + 11), gp(cx_ - 14, s["z0"] - 0.5, cy_ + 11)]
    sheet.poly(q, lerp(WOOD_LIT, SIENNA, 0.2))
    lines.line(q + [q[0]], WOOD_DARK, 0.8, 0.9)
    for p in q:
        sheet.ellipse(p[0] + (2 if p[0] < gp(cx_, s["z0"])[0] else -2), p[1] + (2 if p[1] < gp(cx_, s["z0"], cy_)[1] else -2), 1.0, 1.0, IRON)
    shadows.append(shadow_pts([(s["x0"], s["h"], s["z1"]), (s["x1"], s["h"], s["z1"]), (s["x1"], s["h"], s["z0"]), (s["x1"], 0, s["z0"]), (s["x1"], 0, s["z1"])]))
    r0 = row_of(s["z0"])
    contour(lines, [gp(s["x0"], s["z0"]), gp(s["x0"], s["z0"], s["h"]), gp(s["x0"], s["z1"], s["h"]), gp(s["x1"], s["z1"], s["h"]), gp(s["x1"], s["z1"]), gp(s["x1"], s["z0"]), gp(s["x0"], s["z0"])], r0)
    contour(lines, [gp(s["x0"], s["z0"], s["h"]), gp(s["x1"], s["z0"], s["h"]), gp(s["x1"], s["z1"], s["h"])], r0, alpha=0.6)
    contour(lines, [gp(s["x1"], s["z0"]), gp(s["x1"], s["z0"], s["h"])], r0, alpha=0.6)


def paint_hearth(sheet, lines, shadows):
    """Kota's hearth box (the game's: the cooking aboard is not in the sources): a wooden box lined with clay, its lid
    hinged at the back and propped open against the mats; the rice pot sits in it (the pot is a cut-out: its states)."""
    h = HEARTH
    x0, x1, z0, z1, hh = h["x0"], h["x1"], h["z0"], h["z1"], h["h"]
    shadows.append(shadow_pts([(x0, hh, z0), (x1, hh, z0), (x1, hh, z1), (x1, 0, z1), (x1, 0, z0)]))
    # the propped lid behind it (hinged at the back edge, leaning back): its inner face toward us, in half shade
    lid = [gp(x0 + 2, z1, hh), gp(x1 - 2, z1, hh), gp(x1 - 4, z1 + 22, hh + 58), gp(x0 + 4, z1 + 22, hh + 58)]
    sheet.poly(lid, lerp(WOOD_MID, COBALT, 0.22))
    lines.line([lid[2], lid[3]], WOOD_DARK, 1.2, 0.9)
    contour(lines, lid + [lid[0]], row_of(z1), alpha=0.7)
    # the box: front (lit), right side (shade), the top rim
    sheet.poly([gp(x0, z0), gp(x1, z0), gp(x1, z0, hh), gp(x0, z0, hh)], WOOD_MID)
    sheet.poly([gp(x1, z0), gp(x1, z1), gp(x1, z1, hh), gp(x1, z0, hh)], WOOD_SHADE)
    rim_o = [gp(x0, z0, hh), gp(x1, z0, hh), gp(x1, z1, hh), gp(x0, z1, hh)]
    rim_i = [gp(x0 + 7, z0 + 7, hh), gp(x1 - 7, z0 + 7, hh), gp(x1 - 7, z1 - 7, hh), gp(x0 + 7, z1 - 7, hh)]
    sheet.poly(rim_o, tintw(OCHRE, 0.38))
    # the clay bed inside, a little below the rim, and the fire's mouth under the pot (the embers are the engine's)
    sheet.poly(rim_i, lerp(lerp(SIENNA, OCHRE, 0.45), COBALT, 0.18))
    px_, pz_ = POT["x"], POT["z"]
    mouth = gp(px_, pz_ - 2, hh - 1)
    sheet.ellipse(mouth[0], mouth[1], POT["r"] * 1.2 * kz(pz_), POT["r"] * 0.45 * kz(pz_), lerp(SIENNA, PRUSSIAN, 0.55))
    # a bundle of kindling and a small water tub beside the pot, on the clay
    for j in range(4):
        a_ = gp(x0 + 14 + j * 3, z0 + 14, hh + 3 + j)
        b_ = gp(x0 + 30 + j * 2, z1 - 12, hh + 3 + j)
        lines.line([a_, b_], lerp(OCHRE, SIENNA, 0.4), 1.3, 0.95)
    # planks on the front, an iron corner
    lines.line([gp(x0, z0, hh * 0.5), gp(x1, z0, hh * 0.5)], PRUSSIAN, 0.6, 0.35)
    r0 = row_of(z0)
    contour(lines, [gp(x0, z0), gp(x1, z0), gp(x1, z1), gp(x1, z1, hh), gp(x0, z1, hh), gp(x0, z0, hh), gp(x0, z0)], r0)
    contour(lines, [gp(x0, z0, hh), gp(x1, z0, hh), gp(x1, z0)], r0)
    contour(lines, rim_i + [rim_i[0]], r0, alpha=0.4)


def paint_bale(sheet, lines, shadows):
    """The bale Seijiro sits on: a rice-straw bale lying along the walkway against the aft hold's coaming, bound with
    three straw ropes; its left end (toward the picture's middle) shows the straw's cut ends."""
    b = BALE
    x0, x1, zc, r = b["x0"], b["x1"], b["z"], b["r"]
    shadows.append(shadow_pts([(x0, 2 * r, zc), (x1, 2 * r, zc), (x1, 0, zc + r), (x0, 0, zc + r)]))
    top = [gp(x_, zc - r * 0.2, r * 1.95) for x_ in np.linspace(x0, x1, 8)]
    front_low = [gp(x_, zc - r * 0.95, r * 0.6) for x_ in np.linspace(x0, x1, 8)]
    foot = [gp(x_, zc - r * 0.5, 0) for x_ in np.linspace(x0, x1, 8)]
    sheet.poly(top + front_low[::-1], lerp(MAT_LIT, OCHRE, 0.25))
    sheet.poly(front_low + foot[::-1], lerp(lerp(MAT_LIT, OCHRE, 0.35), COBALT, 0.25))
    # its left end: an oval of straw ends (lit: it faces left, toward the sun's side)
    c = gp(x0, zc, r)
    sheet.ellipse(c[0], c[1], r * 0.42 * kz(zc), r * 1.0 * kz(zc), lerp(MAT_LIT, NAPLES, 0.2))
    sheet.ellipse(c[0], c[1], r * 0.22 * kz(zc), r * 0.55 * kz(zc), lerp(OCHRE, SIENNA, 0.2))
    for u in (0.18, 0.5, 0.82):
        x_ = x0 + (x1 - x0) * u
        lines.line([gp(x_, zc - r * 0.2, r * 1.95), gp(x_, zc - r * 0.95, r * 0.6), gp(x_, zc - r * 0.5, 0)], ROPE_DARK, 1.4, 0.95)
    r0 = row_of(zc)
    contour(lines, top + [gp(x1, zc, r)] + foot[::-1], r0)
    contour(lines, [gp(x0, zc - r * 0.2, r * 1.95), gp(x0, zc - r * 0.5, 0)], r0, alpha=0.5)


def paint_house(sheet, lines, shadows):
    """The stern deckhouse (tomo-yagura) over the overhang: a low house of planks under a shallow roof of boards,
    against the far bulwark at the stern; we see its forward end (facing the bow: in shade, the sun being left of us?
    no: it faces the picture's middle, -x, toward the sun's side: lit) and its near side (toward us: lit)."""
    h = HOUSE
    x0, x1, z0, z1, hh = h["x0"], h["x1"], h["z0"], h["z1"], h["h"]
    shadows.append(shadow_pts([(x0, hh, z0), (x1, hh, z0), (x1, 0, z0), (x0, 0, z0)]))
    fwd = [gp(x0, z0), gp(x0, z1), gp(x0, z1, hh), gp(x0, z0, hh)]
    near = [gp(x0, z0), gp(x1, z0), gp(x1, z0, hh), gp(x0, z0, hh)]
    sheet.poly(fwd, lerp(WOOD_MID, NAPLES, 0.12))
    sheet.poly(near, WOOD_LIT)
    # planks: level lines on both faces; a door in its near side, a window-hatch in its forward end
    for v in np.arange(18.0, hh, 22.0):
        lines.line([gp(x0, z1, v), gp(x0, z0, v), gp(x1, z0, v)], PRUSSIAN, 0.6, 0.28)
    door = [gp(x0 + 60, z0 - 0.5), gp(x0 + 125, z0 - 0.5), gp(x0 + 125, z0 - 0.5, 168), gp(x0 + 60, z0 - 0.5, 168)]
    sheet.poly(door, lerp(WOOD_SHADE, PRUSSIAN, 0.35))
    lines.line([door[0], door[3], door[2], door[1]], WOOD_DARK, 1.2, 1.0)
    hatch = [gp(x0 - 0.5, z0 + 70, 120), gp(x0 - 0.5, z0 + 150, 120), gp(x0 - 0.5, z0 + 150, 170), gp(x0 - 0.5, z0 + 70, 170)]
    sheet.poly(hatch, lerp(WOOD_SHADE, PRUSSIAN, 0.3))
    # the roof: boards, eaves over both faces; its top lit, its edge's underside dark
    ov = 26.0
    e = [gp(x0 - ov, z0 - ov, hh), gp(x1 + ov, z0 - ov, hh), gp(x1 + ov, z1, hh + 34), gp(x0 - ov, z1, hh + 34)]
    sheet.poly(e, lerp(tintw(PRUSSIAN, 0.55), OCHRE, 0.28))
    sheet.poly([gp(x0 - ov, z0 - ov, hh), gp(x1 + ov, z0 - ov, hh), gp(x1 + ov, z0 - ov, hh - 7), gp(x0 - ov, z0 - ov, hh - 7)], WOOD_DARK)
    sheet.poly([gp(x0 - ov, z0 - ov, hh), gp(x0 - ov, z1, hh + 34), gp(x0 - ov, z1, hh + 27), gp(x0 - ov, z0 - ov, hh - 7)], WOOD_DARK)
    for u in np.linspace(0.1, 0.9, 6):
        lines.line([gp(x0 - ov + (x1 - x0 + 2 * ov) * u, z0 - ov, hh), gp(x0 - ov + (x1 - x0 + 2 * ov) * u, z1, hh + 34)], PRUSSIAN, 0.6, 0.3)
    r0 = row_of(z0)
    contour(lines, [gp(x0, z1), gp(x0, z0), gp(x1, z0)], r0)
    contour(lines, [gp(x0, z0), gp(x0, z0, hh)], r0, alpha=0.6)
    contour(lines, [e[3], e[0], e[1]], r0)


def cast_shadows(pic, deck, shadows, seed):
    """Every standing thing's shadow on the deck and the mats, flat and blue (short: the sun is high)."""
    sh = Paper(SHAPE)
    for poly in shadows:
        sh.poly(poly, DECK_SHADOW, 0.85)
    c, a = sh.done()
    over(pic, c, a.astype(F32))
    return a


def under(seed=SEED):
    """The backdrop (back.png) before the brush: sky, sea, the ship's broad masses. The cape, the swell's far sea, the
    sail, the mast and the other cut-outs are painted onto it later (details) and cut out."""
    info = {}
    pic = paint_sky(seed)
    info["sky"] = pic.copy()
    paint_sea(pic, seed, HZ + SKY_UNDER + 1)
    info["deck"] = paint_deck(pic, seed)
    sheet = Paper(SHAPE)
    shadows = []
    paint_far_bulwark(pic, sheet, seed)
    holds = paint_coaming_and_cargo(sheet, sheet, seed + 40)
    info["cask_heads"] = paint_hold_end(sheet, sheet, seed + 41, holds["fwd"])
    paint_boat(sheet, sheet, shadows)
    paint_house(sheet, sheet, shadows)
    c_, a_ = sheet.done()
    over(pic, c_, a_)
    info["ship_mask"] = a_.copy()                                       # what stands in front of the sea, in the backdrop
    info["ship_sheet"] = (c_.copy(), a_.copy())                         # restated crisply after the brush (details)
    info["holds"] = holds
    shadows += mast_shadow()
    info["shadow"] = cast_shadows(pic, info["deck"], shadows, seed)
    return np.clip(pic, 0, 1), info


def mast_shadow():
    """The mast's short shadow across the gangway (it falls on the step block and away)."""
    m = MAST
    return [shadow_pts([(m["x"] - m["r"], STEP["h"], m["z"]), (m["x"] + m["r"], STEP["h"], m["z"]), (m["x"] + m["r"], 260, m["z"]), (m["x"] - m["r"], 260, m["z"])])]


# ================================================================ pass 3: the crisp things of the backdrop
def details(pic, info, seed=SEED, fast=False):
    x, y = grid(SHAPE)
    deck = info["deck"]
    X, Z, below = floor()
    lines = Paper(SHAPE)
    # ---- the deck's planks: the seams (level lines, closer far off), butt joints, a few nail heads
    for z_ in np.arange(-100.0, FAR_Z, 19.0):
        r = row_of(z_)
        if r <= HZ + 1:
            continue
        lines.line([(-5, r), (W + 5, r)], PRUSSIAN, max(0.5, 0.9 * kz(z_) * 0.75), 0.30)
    rng = np.random.default_rng(seed + 60)
    for z_ in np.arange(-100.0, FAR_Z, 19.0):
        for x_ in np.arange(-700.0 + rng.uniform(0, 200), 900.0, rng.uniform(190, 260)):
            a_, b_ = gp(x_, z_), gp(x_ + 2, z_ + 19)
            lines.line([a_, b_], PRUSSIAN, 0.6, 0.30)
    pic_lines = lines.done()
    # (the deck's lines only where the deck shows: not over the cargo, the boat, the bulwark or the deckhouse)
    c, a = pic_lines
    over(pic, c, (a * deck * (1 - np.clip(info["ship_mask"] * 1.4, 0, 1)) * (1 - info["shadow"] * 0.3)).astype(F32))
    # the ship's broad things said again crisply over their brushing (the bulwark, the cargo and its mats, the boat, the
    # deckhouse), as the act's other paintings restate theirs; a little of the brush left in them
    sc0, sa0 = info["ship_sheet"]
    over(pic, sc0, (sa0 * 0.82).astype(F32))
    sheet = Paper(SHAPE)
    shadows = []
    stem = Paper(SHAPE)
    paint_stem(stem, stem)
    sc_, sa_ = stem.done()
    info["ship_mask"] = np.maximum(info["ship_mask"], sa_)
    info["stem_mask"] = sa_
    paint_step(sheet, sheet, shadows)
    paint_hearth(sheet, sheet, shadows)
    paint_bale(sheet, sheet, shadows)
    # the shadows of the things on the deck (under them): laid first, then the things
    sh = Paper(SHAPE)
    for poly in shadows:
        sh.poly(poly, DECK_SHADOW, 0.85)
    sh.onto(pic)
    over(pic, sc_, sa_)
    sheet.onto(pic)
    return pic


# ================================================================ the cut-outs
def brushed(color, alpha, lc, la, under_c, seed=4, sizes=(6, 3, 2), keep=0.45, fast=False):
    """A cut-out, painted: flats brushed over the colour behind it, its lines put back on top (Yui's way)."""
    whole = np.maximum(alpha, la)
    ys, xs = np.where(whole > 0.02)
    if len(ys) == 0:
        return color, whole
    y0, y1, x0, x1 = max(ys.min() - 12, 0), min(ys.max() + 13, H), max(xs.min() - 12, 0), min(xs.max() + 13, W)
    flat_ = np.empty((y1 - y0, x1 - x0, 3), dtype=F32)
    flat_[...] = np.asarray(under_c, dtype=F32)
    over(flat_, color[y0:y1, x0:x1], alpha[y0:y1, x0:x1])
    painted = flat_ if fast else strokes(flat_, sizes=sizes, seed=seed, density=1.8, jitter=0.025, keep=keep)
    over(painted, lc[y0:y1, x0:x1], la[y0:y1, x0:x1])
    out = np.zeros(SHAPE + (3,), dtype=F32)
    out[y0:y1, x0:x1] = painted
    return out, np.clip(whole, 0, 1)


def swell_cut(info, seed, fast=False):
    """The swell layer: the far sea from the horizon down, and the cape on it (the engine rocks it a pixel or two on a
    long slow cycle: fx swell). Painted whole: the sea's own bands and the cape over the sky."""
    pic = info["sky"].copy()
    paint_sea(pic, seed, HZ)
    m = paint_cape(pic, seed)
    x, y = grid(SHAPE)
    alpha = ((y >= HZ) & (y < SWELL_ROWS[1])).astype(F32)
    alpha = np.maximum(alpha, (m > 0.5).astype(F32))
    if not fast:
        b = strokes(pic, sizes=(6, 3), seed=seed + 1, density=1.4, jitter=0.02, keep=0.55)
        pic = lerp(pic, b, (y >= HZ).astype(F32)[..., None] * 0.6)
        # the cape said again crisply over its brushing
        crisp = info["sky"].copy()
        paint_sea(crisp, seed, HZ)
        paint_cape(crisp, seed)
        pic = lerp(pic, crisp, (m * 0.7)[..., None])
    return pic.astype(F32), alpha


def sail_geometry():
    """The great sail, in the picture (it is above the eye, and seen from under it at an angle: the near end, at the left,
    goes out of the picture; the far end, at the right, comes down into it with the yard). Returns the outline, the yard,
    the foot curve and the leech, and the bolts' seams as lines (u from 0 at the near luff to 1 at the leech)."""
    yard = [(452.0, -9.0), (560.0, 12.0), (660.0, 31.0), (752.0, 47.0)]
    leech = [(738.0, 52.0), (741.0, 92.0), (737.0, 140.0), (726.0, 178.0), (713.0, 200.0)]
    foot = [(713.0, 200.0), (640.0, 199.0), (560.0, 195.0), (470.0, 187.0), (380.0, 175.0), (290.0, 163.0), (200.0, 151.0), (110.0, 140.0), (20.0, 130.0), (-12.0, 126.0)]
    outline = [(-12.0, -12.0), (452.0, -12.0)] + yard[1:3] + [(738.0, 50.0)] + leech[1:] + foot[1:] + [(-12.0, 126.0)]

    def seam_x(u):
        a, b, c = -330.0, 1386.0, 0.483
        return (a + b * u) / (1 + c * u)
    return outline, yard, leech, foot, seam_x


def foot_y(xp, foot):
    xs = [p[0] for p in foot][::-1]
    ys = [p[1] for p in foot][::-1]
    return float(np.interp(xp, xs, ys))


def top_y(xp, yard):
    xs = [p[0] for p in yard]
    ys = [p[1] for p in yard]
    if xp < xs[0]:
        return -12.0
    return float(np.interp(xp, xs, ys)) + 4.0


def sail_cut(info, seed, fast=False):
    """The great sail of woven cotton in vertical bolts on its yard (facts-21a item 6: the Takasago captain's woven
    sail): filling, its face toward us in the noon sun (lead white), the cloth turning away near the leech and along the
    foot a second flat (pale cerulean); the bolts' seams; the mast's shadow on it; the bolt rope; the yard (the
    masthead out of the picture above). The engine stirs it: fx sail-breath."""
    outline, yard, leech, foot, seam_x = sail_geometry()
    sheet = Paper(SHAPE)
    lines = Paper(SHAPE)
    sheet.poly(outline, SAIL_LIT)
    x, y = grid(SHAPE)
    # the shade flat: the cloth turning away toward the leech, and a band along the foot where it curves under
    turn = [(642.0, 30.0), (676.0, 60.0), (690.0, 120.0), (684.0, 170.0), (668.0, 200.0), (713.0, 200.0), (726.0, 178.0), (737.0, 140.0), (741.0, 92.0), (738.0, 52.0)]
    sheet.poly(turn, SAIL_SHADE)
    under_foot = [(p[0], p[1] - (9 if p[0] > 300 else 7)) for p in foot[:-1]] + [p for p in foot[:-1][::-1]]
    sheet.poly(under_foot, SAIL_SHADE)
    # the mast's shadow on the sail: the sun is behind us and to the left, so it lies a little right of the mast
    mx = gp(MAST["x"], MAST["z"])[0]
    mw = MAST["r"] * kz(MAST["z"])
    sh = [(mx + 9 - mw * 0.8, -12), (mx + 9 + mw * 0.8, -12), (mx + 13 + mw * 0.8, foot_y(mx + 13, foot) - 1), (mx + 13 - mw * 0.8, foot_y(mx + 13, foot) - 1)]
    sheet.poly(sh, SAIL_DEEP)
    # the bolts: each a hair of difference in its white (they were woven one by one), their seams as lines
    n = 18
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n
        xa, xb = seam_x(u0), seam_x(u1)
        if xb < -20 or xa > 745:
            continue
        if i % 2 == 0:
            q = [(xa, top_y(xa, yard)), (xb, top_y(xb, yard)), (xb, foot_y(xb, foot)), (xa, foot_y(xa, foot))]
            sheet.poly(q, lerp(WHITE, CERULEAN, 0.05), 0.5)
    for i in range(1, n + 1):
        xs_ = seam_x(i / n)
        if xs_ < -5 or xs_ > 738:
            continue
        t0, f0 = top_y(xs_, yard), foot_y(xs_, foot)
        bow = 3.0 * (1 - abs(2 * i / n - 1))                            # the bellying: the seams bow a little
        pts = [(xs_ + bow * math.sin(math.pi * v) - 2 * v, t0 + (f0 - t0) * v) for v in np.linspace(0, 1, 9)]
        lines.line(pts, PRUSSIAN, 0.7, 0.32)
    # the bolt rope along the foot and the leech, and the cringles where the sheets are made fast
    lines.line(foot[:-1], lerp(OCHRE, SIENNA, 0.2), 1.6, 0.9)
    lines.line(leech, lerp(OCHRE, SIENNA, 0.2), 1.3, 0.85)
    for p in (foot[0], foot[3], foot[6]):
        sheet.ellipse(p[0], p[1] + 1, 2.2, 2.2, ROPE_DARK)
    # the yard: a heavy spar along the head, lashed to the sail; its far arm a little beyond the leech
    lines.line(yard, WOOD_DARK, 9.0, 1.0)
    lines.line([(p[0], p[1] - 3) for p in yard], lerp(WOOD_MID, SIENNA, 0.35), 3.0, 1.0)
    for xp in np.arange(470, 740, 34):
        yy = float(np.interp(xp, [p[0] for p in yard], [p[1] for p in yard]))
        lines.line([(xp, yy - 4), (xp - 3, yy + 6)], ROPE_DARK, 1.0, 0.9)
    contour(lines, leech, 150, pale=True)
    contour(lines, foot[:-1], 150, pale=True)
    c, a = sheet.done()
    lc, la = lines.done()
    pic, alpha = brushed(c, a, lc, la, PAPER, seed=seed, sizes=(10, 5, 2), keep=0.35, fast=fast)
    return pic, alpha


def rigging_cut(info, seed, fast=False):
    """The ropes from the sail and the yard to the deck (the sheets, the brace, a lift going up out of the picture):
    over the sea and the swell, behind everybody."""
    lines = Paper(SHAPE)
    outline, yard, leech, foot, seam_x = sail_geometry()
    rope = lerp(ROPE_DARK, PRUSSIAN, 0.15)
    # the sheet from the clew (the foot's far corner) down to a cleat by the windlass
    cleat = gp(WINDLASS["x"] - 40, WINDLASS["z0"] - 10, 105)
    lines.line([foot[0], ((foot[0][0] + cleat[0]) / 2 + 6, (foot[0][1] + cleat[1]) / 2), cleat], rope, 1.2, 0.95)
    # a second sheet from the foot's middle down to the aft hold's lashing
    mid = foot[3]
    tie = gp(HOLD_A[1] - 30, WALK_Z + 60, 120)
    lines.line([mid, ((mid[0] + tie[0]) / 2 + 3, (mid[1] + tie[1]) / 2), tie], rope, 1.1, 0.9)
    # the forward sheet, down toward the bow
    fm = foot[7]
    tie2 = gp(HOLD_F[0] + 40, WALK_Z + 70, 110)
    lines.line([fm, ((fm[0] + tie2[0]) / 2 - 3, (fm[1] + tie2[1]) / 2), tie2], rope, 1.1, 0.9)
    # the brace from the yard's arm aft, out of the picture at the right
    lines.line([yard[-1], (778.0, 120.0), (812.0, 230.0)], rope, 1.2, 0.95)
    # a lift from the yard's arm up out of the picture
    lines.line([yard[-1], (744.0, 18.0), (736.0, -10.0)], rope, 1.0, 0.9)
    c, a = lines.done()
    return c, a


def mast_cut(info, seed, fast=False):
    """The mast: built up of a core wrapped in staves and bound with iron rings (facts-21a item 6), rising from its step
    out of the top of the picture; its lit left side and its shaded right side two flats; the halyard down its far side."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    m = MAST
    cx = gp(m["x"], m["z"])[0]
    k = kz(m["z"])
    hw = m["r"] * k
    top, bot = -12.0, gp(m["x"], m["z"] - m["r"], STEP["h"])[1]
    taper = 0.88
    L = [(cx - hw * taper, top), (cx - hw, bot)]
    R = [(cx + hw * taper, top), (cx + hw, bot)]
    sheet.poly([L[0], R[0], R[1], L[1]], WOOD_LIT)
    split_t, split_b = cx + hw * taper * 0.25, cx + hw * 0.25
    sheet.poly([(split_t, top), R[0], R[1], (split_b, bot)], lerp(WOOD_SHADE, SIENNA, 0.15))
    # the staves: two lines down its length
    for f in (-0.55, 0.62):
        lines.line([(cx + hw * taper * f, top), (cx + hw * f, bot)], PRUSSIAN, 0.6, 0.30)
    # the iron rings, every 55 cm or so up its height
    for hh in np.arange(STEP["h"] + 34, 2200, 55.0):
        yy = gp(m["x"], m["z"] - m["r"], hh)[1]
        if yy < -6:
            break
        t = (bot - yy) / (bot - top)
        w_ = hw * (1 - (1 - taper) * t) + 1.0
        sag = 1.4 if yy < HZ else -1.0                                   # above the eye a ring is seen from under it
        lines.line([(cx - w_, yy), (cx, yy - sag), (cx + w_, yy)], IRON, 2.6, 1.0)
        lines.line([(cx - w_ + 1, yy - 1.4), (cx - w_ * 0.2, yy - 1.4 - sag)], lerp(IRON, CERULEAN, 0.45), 0.8, 0.8)
    # the halyard coming down its far side to the windlass (seen as a line beside it)
    lines.line([(cx + hw * 0.95, top), (cx + hw * 1.05, gp(m["x"], m["z"], 140)[1]), gp(m["x"] + 30, m["z"] + 20, 60)], ROPE_DARK, 1.2, 0.9)
    contour(lines, [L[0], L[1]], bot, warm=True)
    contour(lines, [R[0], R[1]], bot)
    c, a = sheet.done()
    lc, la = lines.done()
    return brushed(c, a, lc, la, WOOD_MID, seed=seed, sizes=(4, 2), keep=0.55, fast=fast)


def windlass_cut(back, seed, fast=False):
    """The windlass at the stern that hauls the yard up (facts-21a item 6: it took several men): a heavy drum of wood
    athwartships between two cheek posts, its axle through them, the halyard wound on it in turns; two bars in it at
    rest, level, pointing forward, one at the drum's near end and one at its far end, where the two sailors lean."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    w = WINDLASS
    x_, z0, z1, r, ax = w["x"], w["z0"], w["z1"], w["r"], w["axis"]
    # the far cheek post (beyond the drum's far end)
    zc = z1 + 8
    sheet.poly([gp(x_ - 9, zc), gp(x_ + 9, zc), gp(x_ + 9, zc, ax + 12), gp(x_ - 9, zc, ax + 12)], WOOD_MID)
    sheet.poly([gp(x_ - 9, zc, ax + 12), gp(x_ + 9, zc, ax + 12), gp(x_ + 9, zc + 18, ax + 12), gp(x_ - 9, zc + 18, ax + 12)], tintw(OCHRE, 0.35))
    # the far bar (pointing forward, level), behind the drum's body
    fb0, fb1 = gp(x_ - r * 0.5, z1 - 25, ax + 8), gp(x_ - w["bar"] + 35, z1 - 25, ax + 6)
    lines.line([fb0, fb1], lerp(WOOD_MID, SIENNA, 0.3), max(1.2, 7 * kz(z1)), 1.0)
    lines.line([(fb0[0], fb0[1] - 1.1), (fb1[0], fb1[1] - 1.1)], tintw(OCHRE, 0.4), 0.9, 0.9)
    # the drum: its top (lit) and its side toward the bow (lit: the sun's side), its underside (shade)
    n = 12
    zs = np.linspace(z0, z1, n)
    top_ = [gp(x_ - r * 0.15, z, ax + r) for z in zs]
    side = [gp(x_ - r, z, ax) for z in zs]
    low = [gp(x_ - r * 0.65, z, ax - r * 0.75) for z in zs]
    sheet.poly(top_ + side[::-1], lerp(WOOD_LIT, NAPLES, 0.1))
    sheet.poly(side + low[::-1], WOOD_MID)
    sheet.poly(low + [gp(x_ + r * 0.6, z1, ax - r * 0.75), gp(x_ + r * 0.6, z0, ax - r * 0.75)], WOOD_SHADE)
    # the halyard wound on it: a band of turns, the free end going up toward the mast
    # (each turn a ring round the drum: seen as an arc over its top and down its side toward us)
    band = [gp(x_ - r * 0.15, z, ax + r + 1.5) for z in (z0 + 40, z0 + 112)] + [gp(x_ - r * 0.7, z, ax - r * 0.72) for z in (z0 + 112, z0 + 40)]
    sheet.poly([gp(x_ - r * 0.15, z0 + 40, ax + r + 1.5), gp(x_ - r * 0.15, z0 + 112, ax + r + 1.5), gp(x_ - r - 1.5, z0 + 112, ax), gp(x_ - r - 1.5, z0 + 40, ax)],
               lerp(ROPE, NAPLES, 0.15))
    sheet.poly([gp(x_ - r - 1.5, z0 + 40, ax), gp(x_ - r - 1.5, z0 + 112, ax), gp(x_ - r * 0.7, z0 + 112, ax - r * 0.72), gp(x_ - r * 0.7, z0 + 40, ax - r * 0.72)], ROPE)
    for z in np.linspace(z0 + 44, z0 + 108, 9):
        lines.line([gp(x_ + r * 0.2, z, ax + r * 0.98), gp(x_ - r * 0.5, z, ax + r * 0.87), gp(x_ - r - 1.5, z, ax), gp(x_ - r * 0.7, z, ax - r * 0.72)], ROPE_DARK, 0.9, 0.8)
    lines.line([gp(x_ - r * 0.4, z0 + 76, ax + r), gp(x_ - 150, z0 - 40, 260)], ROPE_DARK, 1.2, 0.9)
    # the drum's near end: a disc of end grain, the bar holes; the near bar in it, pointing forward
    e = gp(x_, z0, ax)
    k0 = kz(z0)
    sheet.ellipse(e[0], e[1], r * k0 * 0.98, r * k0, lerp(WOOD_LIT, SIENNA, 0.18))
    sheet.ellipse(e[0], e[1], r * k0 * 0.6, r * k0 * 0.62, lerp(WOOD_MID, SIENNA, 0.25), 0.5)
    for ang in (60, 150, 240):
        hx = e[0] + math.cos(math.radians(ang)) * r * 0.7 * k0
        hy = e[1] - math.sin(math.radians(ang)) * r * 0.7 * k0
        sheet.ellipse(hx, hy, 2.4, 2.4, WOOD_DARK)
    nb0, nb1 = gp(x_ - r * 0.6, z0 + 14, ax + 6), gp(x_ - w["bar"], z0 + 14, ax + 9)
    lines.line([nb0, nb1], lerp(WOOD_MID, SIENNA, 0.3), max(1.2, 7.5 * k0), 1.0)
    lines.line([(nb0[0], nb0[1] - 1.3), (nb1[0], nb1[1] - 1.3)], tintw(OCHRE, 0.42), 1.0, 0.9)
    contour(lines, [(nb0[0], nb0[1] + 2.8), (nb1[0], nb1[1] + 2.8), (nb1[0], nb1[1] - 2.8)], nb1[1], alpha=0.65)
    # the near cheek post, in front of the drum's end, the axle's iron through it
    zc = z0 - 22
    ph = ax + 12
    sheet.poly([gp(x_ - 9, zc), gp(x_ + 9, zc), gp(x_ + 9, zc, ph), gp(x_ - 9, zc, ph)], WOOD_LIT)
    sheet.poly([gp(x_ + 9, zc), gp(x_ + 9, zc + 18), gp(x_ + 9, zc + 18, ph), gp(x_ + 9, zc, ph)], WOOD_SHADE)
    sheet.poly([gp(x_ - 9, zc, ph), gp(x_ + 9, zc, ph), gp(x_ + 9, zc + 18, ph), gp(x_ - 9, zc + 18, ph)], tintw(OCHRE, 0.38))
    a_ = gp(x_, zc - 1, ax)
    sheet.ellipse(a_[0], a_[1], 3.2, 3.2, IRON)
    sheet.ellipse(a_[0] - 0.8, a_[1] - 0.8, 1.2, 1.2, lerp(IRON, CERULEAN, 0.5))
    r0 = row_of(zc)
    contour(lines, [gp(x_ - 9, zc), gp(x_ - 9, zc, ph), gp(x_ + 9, zc, ph), gp(x_ + 9, zc + 18, ph)], r0)
    contour(lines, [gp(x_ + 9, zc), gp(x_ + 9, zc, ph)], r0, alpha=0.6)
    contour(lines, top_, r0, alpha=0.6)
    contour(lines, side, r0, alpha=0.45)
    c, a = sheet.done()
    lc, la = lines.done()
    ys, xs = np.where(a > 0.5)
    return brushed(c, a, lc, la, np.median(back[ys, xs], axis=0) if len(ys) else WOOD_MID, seed=seed, fast=fast)


def tiller_cut(back, seed, fast=False):
    """The long tiller and the rudder's head (facts-21a item 6: a huge rudder with a long tiller): the rudder's stock
    comes up through the stern at the picture's right edge, iron-collared; the tiller runs from it forward over the
    stern deck at hip height, swung a little toward us; its end worn pale where Gonroku holds it."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    t, rd = TILLER, RUDDER
    # the rudder's head: a square timber post (its near face lit, its left face toward the sun's side lit too)
    x0, x1, z0, z1, hh = rd["x0"], rd["x1"], rd["z0"], rd["z1"], rd["h"]
    for name, quad, nrm in box_faces(x0, x1, 0.0, hh, z0, z1):
        col = {"front": lerp(WOOD_MID, SIENNA, 0.18), "top": tintw(OCHRE, 0.30), "left": lerp(WOOD_LIT, SIENNA, 0.12), "right": WOOD_SHADE}[name]
        sheet.poly([P3(q) for q in quad], col)
    for hy in (122.0, 160.0):
        lines.line([gp(x0 - 1, z0 - 1, hy), gp(x1 + 1, z0 - 1, hy)], IRON, 3.0, 1.0)
        lines.line([gp(x0 - 1, z0 - 1, hy), gp(x0 - 1, z1 + 1, hy)], IRON, 2.4, 1.0)
    r0 = row_of(z0)
    contour(lines, [gp(x0, z0), gp(x0, z0, hh), gp(x1, z0, hh), gp(x1, z0)], r0)
    contour(lines, [gp(x0, z0, hh), gp(x0, z1, hh), gp(x1, z1, hh)], r0, alpha=0.6)
    # the tiller, from its end (Gonroku's hand) back into the rudder's head
    n = 9
    us = np.linspace(0, 1, n)
    xs = [t["x0"] + (x0 + 6 - t["x0"]) * u for u in us]
    zs = [t["z0"] + ((z0 + z1) / 2 - t["z0"]) * u for u in us]
    ys = [t["y"] + 20 * u ** 1.4 for u in us]                          # it rises a little toward the head
    th = 13.0
    top_ = [gp(x_, z_, y_ + th / 2) for x_, z_, y_ in zip(xs, zs, ys)]
    bot_ = [gp(x_, z_, y_ - th / 2) for x_, z_, y_ in zip(xs, zs, ys)]
    mid_ = [gp(x_, z_, y_ + th * 0.05) for x_, z_, y_ in zip(xs, zs, ys)]
    sheet.poly(top_ + bot_[::-1], lerp(WOOD_MID, SIENNA, 0.32))
    sheet.poly(top_ + mid_[::-1], tintw(OCHRE, 0.32))                 # its upper face in the sun
    # the hand-worn end; a rope grommet by it
    e0, e1 = gp(xs[0], zs[0], ys[0]), gp(xs[1], zs[1], ys[1])
    k = kz(zs[0])
    lines.line([(e0[0] + 1, e0[1]), ((e0[0] + e1[0]) / 2, (e0[1] + e1[1]) / 2)], tintw(OCHRE, 0.55), th * k * 0.7, 1.0)
    g0 = gp(xs[2], zs[2], ys[2])
    lines.line([(g0[0], g0[1] - th * k * 0.55), (g0[0] + 1.5, g0[1] + th * k * 0.55)], ROPE_DARK, 1.8, 1.0)
    contour(lines, top_, top_[0][1], warm=True)
    contour(lines, [top_[0]] + bot_, bot_[0][1])
    c, a = sheet.done()
    lc, la = lines.done()
    ys_, xs_ = np.where(a > 0.5)
    return brushed(c, a, lc, la, np.median(back[ys_, xs_], axis=0) if len(ys_) else WOOD_MID, seed=seed, fast=fast)


def compass_cut(back, seed, open_=False, fast=False):
    """The compass box (funa-dokei, "the ship's clock": facts-21a item 8, facts-21d item 5) on its post by the helm:
    a square box of worn wood with a lid; shut, or the lid propped open (then the card's white shows, a ring of marks and
    the needle, and the close-up edo-compass opens from it)."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    c = COMPASS
    x_, z_, w_, hh = c["x"], c["z"], c["w"], c["h"]
    hw = w_ / 2
    y0, y1 = hh - 26, hh
    z0, z1 = z_ - hw, z_ + hw
    # its short shadow on the deck, away and a little right
    sheet.poly(shadow_pts([(x_ - hw, y0, z0), (x_ + hw, y0, z0), (x_ + hw, y0, z1), (x_ + 7, 0, z_ + 7), (x_ - 7, 0, z_ + 7)]), DECK_SHADOW, 0.85)
    # a foot block on the deck, the post (front lit, right side shade)
    sheet.poly([gp(x_ - 15, z_ - 15), gp(x_ + 15, z_ - 15), gp(x_ + 15, z_ - 15, 9), gp(x_ - 15, z_ - 15, 9)], WOOD_SHADE)
    sheet.poly([gp(x_ - 15, z_ - 15, 9), gp(x_ + 15, z_ - 15, 9), gp(x_ + 15, z_ + 15, 9), gp(x_ - 15, z_ + 15, 9)], tintw(OCHRE, 0.25))
    sheet.poly([gp(x_ - 7, z_ - 7), gp(x_ + 7, z_ - 7), gp(x_ + 7, z_ - 7, y0), gp(x_ - 7, z_ - 7, y0)], WOOD_MID)
    sheet.poly([gp(x_ + 7, z_ - 7), gp(x_ + 7, z_ + 7), gp(x_ + 7, z_ + 7, y0), gp(x_ + 7, z_ - 7, y0)], WOOD_SHADE)
    contour(lines, [gp(x_ - 7, z_ - 7, 9), gp(x_ - 7, z_ - 7, y0)], row_of(z_))
    contour(lines, [gp(x_ + 7, z_ - 7, 9), gp(x_ + 7, z_ - 7, y0)], row_of(z_), alpha=0.6)
    # the box: its front (lit), its right side (shade: it stands right of the picture's middle, so its left side shows: lit)
    for name, quad, nrm in box_faces(x_ - hw, x_ + hw, y0, y1, z0, z1):
        col = {"front": WOOD_MID, "top": tintw(OCHRE, 0.30), "left": lerp(WOOD_LIT, SIENNA, 0.08), "right": WOOD_SHADE}[name]
        sheet.poly([P3(q) for q in quad], col)
    lines.line([gp(x_ - hw, z0, y0 + 13), gp(x_ + hw, z0, y0 + 13)], PRUSSIAN, 0.6, 0.35)
    for (ca, cb) in (((x_ - hw, z0), (x_ - hw + 5, z0)), ((x_ + hw - 5, z0), (x_ + hw, z0))):
        sheet.poly([gp(ca[0], ca[1] - 0.5, y0), gp(cb[0], cb[1] - 0.5, y0), gp(cb[0], cb[1] - 0.5, y1), gp(ca[0], ca[1] - 0.5, y1)], lerp(IRON, COBALT, 0.2))
    if open_:
        # the bowl's mouth, the white card in it with its ring of marks and the needle; the lid propped up behind it
        inner = [gp(x_ - hw + 5, z0 + 5, y1), gp(x_ + hw - 5, z0 + 5, y1), gp(x_ + hw - 5, z1 - 5, y1), gp(x_ - hw + 5, z1 - 5, y1)]
        sheet.poly(inner, lerp(WOOD_DARK, PRUSSIAN, 0.25))
        cc = gp(x_, z_, y1)
        rx, ry = (hw - 8) * kz(z_), (hw - 8) * kz(z_) * (CAM.eye - y1) / 340.0
        sheet.ellipse(cc[0], cc[1], rx, max(2.2, ry), tintw(NAPLES, 0.62))
        for i in range(12):
            t_ = math.radians(i * 30)
            px_, py_ = cc[0] + math.sin(t_) * rx * 0.78, cc[1] - math.cos(t_) * max(2.2, ry) * 0.78
            sheet.ellipse(px_, py_, 0.6, 0.45, PRUSSIAN, 0.8)
        lines.line([(cc[0] - rx * 0.55, cc[1] - 0.8), (cc[0] + rx * 0.55, cc[1] + 0.8)], PRUSSIAN, 1.0, 1.0)
        lid = [gp(x_ - hw, z1, y1), gp(x_ + hw, z1, y1), gp(x_ + hw, z1 + 10, y1 + w_ * 0.98), gp(x_ - hw, z1 + 10, y1 + w_ * 0.98)]
        sheet.poly(lid, lerp(WOOD_MID, COBALT, 0.18))
        lines.line([lid[2], lid[3]], WOOD_DARK, 1.0, 0.9)
        contour(lines, lid + [lid[0]], row_of(z_), alpha=0.8)
        # the stick that props it
        lines.line([gp(x_ + hw - 4, z1 - 2, y1), gp(x_ + hw - 6, z1 + 8, y1 + w_ * 0.7)], WOOD_DARK, 1.0, 1.0)
    else:
        # the lid shut: a board a little bigger than the box, its edge, a small iron hasp
        lid = [gp(x_ - hw - 1, z0 - 1, y1 + 4), gp(x_ + hw + 1, z0 - 1, y1 + 4), gp(x_ + hw + 1, z1 + 1, y1 + 4), gp(x_ - hw - 1, z1 + 1, y1 + 4)]
        sheet.poly(lid, lerp(tintw(OCHRE, 0.26), SIENNA, 0.12))
        sheet.poly([gp(x_ - hw - 1, z0 - 1, y1), gp(x_ + hw + 1, z0 - 1, y1), gp(x_ + hw + 1, z0 - 1, y1 + 4), gp(x_ - hw - 1, z0 - 1, y1 + 4)], lerp(WOOD_MID, SIENNA, 0.25))
        sheet.poly([gp(x_ + hw + 1, z0 - 1, y1), gp(x_ + hw + 1, z1 + 1, y1), gp(x_ + hw + 1, z1 + 1, y1 + 4), gp(x_ + hw + 1, z0 - 1, y1 + 4)], WOOD_SHADE)
        k = gp(x_, z0 - 3.5, y1 - 3)
        sheet.poly([(k[0] - 1.6, k[1] - 3), (k[0] + 1.6, k[1] - 3), (k[0] + 1.6, k[1] + 2), (k[0] - 1.6, k[1] + 2)], IRON)
        contour(lines, [lid[0], lid[1], lid[2], lid[3], lid[0]], row_of(z_), alpha=0.6)
    r0 = row_of(z_)
    contour(lines, [gp(x_ - hw, z0, y1), gp(x_ - hw, z0, y0), gp(x_ + hw, z0, y0), gp(x_ + hw, z1, y0)], r0)
    contour(lines, [gp(x_ + hw, z0, y0), gp(x_ + hw, z0, y1)], r0, alpha=0.6)
    c_, a = sheet.done()
    lc, la = lines.done()
    ys, xs = np.where(a > 0.5)
    return brushed(c_, a, lc, la, np.median(back[ys, xs], axis=0) if len(ys) else WOOD_MID, seed=seed, sizes=(3, 2), keep=0.7, fast=fast)


def pot_cut(back, seed, state="lid", fast=False):
    """The rice pot in the hearth box (a flanged iron pot with a wooden lid): `lid` the lid on, quiet; `lifted` the lid
    lifted off and leaning on the pot, the rice showing (half raw, as Kota keeps looking); `steam` the lid on and the
    pot boiling: a crust of white starch run down from under the lid (the steam itself is the engine's: fx pot-steam)."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    px_, pz_, r = POT["x"], POT["z"], POT["r"]
    y0 = HEARTH["h"] - 4
    k = kz(pz_)
    # the body: a squat iron pot, its flange (the brim that sits on the hearth's mouth)
    body_top, body_bot = gp(px_, pz_, y0 + 16), gp(px_, pz_, y0)
    sheet.poly([(body_bot[0] - r * k * 0.85, body_bot[1]), (body_bot[0] + r * k * 0.85, body_bot[1]),
                (body_top[0] + r * k, body_top[1]), (body_top[0] - r * k, body_top[1])], lerp(IRON, COBALT, 0.12))
    sheet.poly([(body_bot[0], body_bot[1]), (body_bot[0] + r * k * 0.85, body_bot[1]), (body_top[0] + r * k, body_top[1]), (body_top[0], body_top[1])], lerp(IRON, PRUSSIAN, 0.45))
    fl = gp(px_, pz_, y0 + 6)
    sheet.ellipse(fl[0], fl[1], r * k * 1.35, r * k * 0.36, lerp(IRON, CERULEAN, 0.18))
    lines.line([(fl[0] - r * k * 1.35, fl[1]), (fl[0] + r * k * 1.35, fl[1])], PRUSSIAN, 0.8, 0.8)
    rim = gp(px_, pz_, y0 + 16)
    if state in ("lid", "steam"):
        # the wooden lid: a disc a little wider than the mouth, with a cross-bar handle
        sheet.ellipse(rim[0], rim[1] - 1, r * k * 1.08, r * k * 0.34, tintw(OCHRE, 0.28))
        sheet.ellipse(rim[0], rim[1] + 0.8, r * k * 1.08, r * k * 0.30, lerp(WOOD_MID, SIENNA, 0.2), 0.0)
        lines.line([(rim[0] - r * k * 0.55, rim[1] - 2.5), (rim[0] + r * k * 0.55, rim[1] - 2.0)], WOOD_DARK, 2.2, 1.0)
        lines.line([(rim[0] - r * k * 1.08, rim[1] - 1), (rim[0], rim[1] + r * k * 0.34 - 1), (rim[0] + r * k * 1.08, rim[1] - 1)], PRUSSIAN, 0.7, 0.7)
        if state == "steam":
            # the starch boiled over: white runs down the iron from under the lid's edge
            for dx in (-0.8, -0.3, 0.25, 0.7):
                a_ = (rim[0] + dx * r * k, rim[1] + r * k * 0.25 * (1 - abs(dx)))
                lines.line([a_, (a_[0] + 0.5, a_[1] + 4 + 3 * (1 - abs(dx)))], tintw(CERULEAN, 0.85), 1.6, 0.95)
            lines.line([(rim[0] - r * k * 1.0, rim[1]), (rim[0], rim[1] + r * k * 0.32), (rim[0] + r * k * 1.0, rim[1])], tintw(CERULEAN, 0.85), 1.2, 0.9)
    else:
        # the mouth open: the rice inside (white, a grey patch where it is half raw), the lid leaning on the pot's right
        sheet.ellipse(rim[0], rim[1], r * k * 0.95, r * k * 0.30, lerp(IRON, PRUSSIAN, 0.4))
        sheet.ellipse(rim[0], rim[1] + 0.8, r * k * 0.82, r * k * 0.22, tintw(NAPLES, 0.75))
        sheet.ellipse(rim[0] - 2, rim[1] + 0.8, r * k * 0.3, r * k * 0.1, lerp(tintw(NAPLES, 0.6), COBALT, 0.25))
        lid_c = gp(px_ + r * 1.15, pz_ - 4, y0 + 14)
        sheet.ellipse(lid_c[0], lid_c[1], r * k * 0.36, r * k * 1.02, tintw(OCHRE, 0.25))
        lines.line([(lid_c[0] - r * k * 0.1, lid_c[1] - r * k * 0.5), (lid_c[0] - r * k * 0.1, lid_c[1] + r * k * 0.5)], WOOD_DARK, 2.0, 1.0)
        contour(lines, [(lid_c[0], lid_c[1] - r * k * 1.02), (lid_c[0] + r * k * 0.36, lid_c[1]), (lid_c[0], lid_c[1] + r * k * 1.02)], lid_c[1], alpha=0.7)
    contour(lines, [(body_bot[0] - r * k * 0.85, body_bot[1]), (body_top[0] - r * k, body_top[1])], body_bot[1], alpha=0.8)
    contour(lines, [(body_bot[0] + r * k * 0.85, body_bot[1]), (body_top[0] + r * k, body_top[1])], body_bot[1], alpha=0.8)
    c_, a = sheet.done()
    lc, la = lines.done()
    return brushed(c_, a, lc, la, lerp(SIENNA, OCHRE, 0.45), seed=seed, sizes=(3, 2), keep=0.7, fast=fast)


def front_cut(back, seed, fast=False):
    """The front plane: the nearest things on the walkway at the picture's bottom corners, cut off by its edge: a coil
    of rope and a wooden bucket at the left, a water cask with a ladle on its lid at the right."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    # the coil, bottom left: a flat coil of rope lying on the planks, its turns as rings, a tail of it running off
    cx_, cy_ = gp(-395, -12)
    sheet.ellipse(cx_, cy_, 60, 21, lerp(tintw(OCHRE, 0.20), SIENNA, 0.20))
    sheet.ellipse(cx_ + 1, cy_ - 2, 58, 19, lerp(tintw(OCHRE, 0.28), SIENNA, 0.10))
    for i in range(7):
        rr = 56 - i * 7.0
        lines.line([(cx_ + rr * math.cos(t_), cy_ - 2 - i * 0.6 + rr * 0.34 * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 40)], ROPE_DARK, 0.9, 0.55)
    sheet.ellipse(cx_ + 2, cy_ - 6, 9, 3.2, lerp(SIENNA, PRUSSIAN, 0.4))
    lines.line([(cx_ + 56, cy_ - 4), (cx_ + 90, cy_ + 2), (cx_ + 118, cy_ + 16)], lerp(tintw(OCHRE, 0.2), SIENNA, 0.2), 4.5, 1.0)
    lines.line([(cx_ + 56, cy_ - 6), (cx_ + 90, cy_ + 0), (cx_ + 118, cy_ + 14)], ROPE_DARK, 0.8, 0.6)
    contour(lines, [(cx_ - 60 * math.cos(t_), cy_ + 21 * math.sin(t_)) for t_ in np.linspace(0, math.pi, 24)], 600, warm=True)
    # a bucket beside it
    b0 = gp(-300, -20)
    bw, bh = 34, 40
    sheet.poly([(b0[0] - bw * 0.42, b0[1]), (b0[0] + bw * 0.42, b0[1]), (b0[0] + bw * 0.5, b0[1] - bh), (b0[0] - bw * 0.5, b0[1] - bh)], WOOD_MID)
    sheet.poly([(b0[0] + bw * 0.1, b0[1]), (b0[0] + bw * 0.42, b0[1]), (b0[0] + bw * 0.5, b0[1] - bh), (b0[0] + bw * 0.12, b0[1] - bh)], WOOD_SHADE)
    sheet.ellipse(b0[0], b0[1] - bh, bw * 0.5, bw * 0.16, lerp(ULTRA, PRUSSIAN, 0.3))
    for hy in (0.25, 0.75):
        lines.line([(b0[0] - bw * (0.42 + 0.08 * hy), b0[1] - bh * hy), (b0[0] + bw * (0.42 + 0.08 * hy), b0[1] - bh * hy)], lerp(OCHRE, SIENNA, 0.5), 2.0, 1.0)
    contour(lines, [(b0[0] - bw * 0.42, b0[1]), (b0[0] - bw * 0.5, b0[1] - bh)], b0[1], warm=True)
    contour(lines, [(b0[0] + bw * 0.42, b0[1]), (b0[0] + bw * 0.5, b0[1] - bh)], b0[1])
    # the water cask, bottom right
    k0 = gp(462, -14)
    kw, kh = 66, 64
    sheet.poly([(k0[0] - kw * 0.45, k0[1] + 4), (k0[0] + kw * 0.45, k0[1] + 4), (k0[0] + kw * 0.5, k0[1] - kh), (k0[0] - kw * 0.5, k0[1] - kh)], lerp(WOOD_MID, SIENNA, 0.2))
    sheet.poly([(k0[0] + kw * 0.12, k0[1] + 4), (k0[0] + kw * 0.45, k0[1] + 4), (k0[0] + kw * 0.5, k0[1] - kh), (k0[0] + kw * 0.14, k0[1] - kh)], WOOD_SHADE)
    for j in range(-3, 4):
        lines.line([(k0[0] + j * kw * 0.13, k0[1] + 4), (k0[0] + j * kw * 0.14, k0[1] - kh)], PRUSSIAN, 0.6, 0.3)
    for hy in (0.18, 0.5, 0.82):
        lines.line([(k0[0] - kw * (0.45 + 0.05 * hy), k0[1] - kh * hy), (k0[0] + kw * (0.45 + 0.05 * hy), k0[1] - kh * hy)], lerp(OCHRE, VIRIDIAN, 0.15), 3.0, 1.0)
    sheet.ellipse(k0[0], k0[1] - kh, kw * 0.5, kw * 0.14, tintw(OCHRE, 0.34))
    lines.line([(k0[0] - kw * 0.05, k0[1] - kh - 2), (k0[0] + kw * 0.32, k0[1] - kh - 8)], WOOD_DARK, 2.0, 1.0)
    sheet.ellipse(k0[0] - kw * 0.1, k0[1] - kh - 1, 7, 3.2, WOOD_DARK)
    contour(lines, [(k0[0] - kw * 0.45, k0[1] + 4), (k0[0] - kw * 0.5, k0[1] - kh)], 600, warm=True)
    contour(lines, [(k0[0] + kw * 0.45, k0[1] + 4), (k0[0] + kw * 0.5, k0[1] - kh)], 600)
    c_, a = sheet.done()
    lc, la = lines.done()
    return brushed(c_, a, lc, la, WOOD_LIT, seed=seed, keep=0.5, fast=fast)


# ================================================================ the floating cask (frames)
def cask_frames(seed):
    """The floating cask (nagashi-daru, set adrift for Konpira: facts-21a item 7), bobbing past now and then: three
    frames, 40 x 26, its foot (the waterline's middle) at (20, 19): a small cask with its hoops, riding low, a fleck of
    white wash at its side. Painted at the size it shows on the sea about 25 m off (row 392)."""
    frames = []
    for i, (tilt, wash, dy) in enumerate(((0.0, 0.8, 0.0), (-9.0, 1.15, 1.2), (8.0, 0.55, -1.0))):
        S = (26, 40)
        sheet, lines = Sheet(S, ss=4), Sheet(S, ss=4)
        cx_, cy_ = 20.0, 19.0 + dy
        t = math.radians(tilt)

        def R(px, py):
            dx, dy = px - cx_, py - cy_
            return (cx_ + dx * math.cos(t) - dy * math.sin(t), cy_ + dx * math.sin(t) + dy * math.cos(t))
        body = [R(cx_ - 7, cy_ + 1), R(cx_ + 7, cy_ + 1), R(cx_ + 8, cy_ - 10), R(cx_ - 8, cy_ - 10)]
        sheet.poly(body, lerp(WOOD_MID, SIENNA, 0.2))
        sheet.poly([R(cx_ + 1.5, cy_ + 1), R(cx_ + 7, cy_ + 1), R(cx_ + 8, cy_ - 10), R(cx_ + 2, cy_ - 10)], WOOD_SHADE)
        sheet.ellipse(*R(cx_, cy_ - 10), 8.0, 2.4, tintw(OCHRE, 0.35))
        for hy in (-2.5, -7.5):
            lines.line([R(cx_ - 7.8, cy_ + hy), R(cx_ + 7.8, cy_ + hy)], lerp(OCHRE, VIRIDIAN, 0.1), 1.2, 1.0)
        lines.line(body + [body[0]], PRUSSIAN, 0.8, 0.8)
        # the water at its waist: a dark band, and the wash
        wl = 19.0
        sheet.poly([(cx_ - 14, wl), (cx_ + 14, wl), (cx_ + 16, wl + 5), (cx_ - 16, wl + 5)], mixp(ULTRA, PRUSSIAN, 0.35))
        sheet.ellipse(cx_ - 9, wl + 0.5, 4.5 * wash, 1.3, tintw(CERULEAN, 0.85))
        sheet.ellipse(cx_ + 10, wl + 1.0, 3.0 * wash, 1.0, tintw(CERULEAN, 0.80))
        c, a = sheet.done()
        lc, la = lines.done()
        over(c, lc, la)
        frames.append((c, np.maximum(a, la)))
    return frames


# ================================================================ the numbers
def layout(planes, info):
    import edo_deck_layout as L
    return L.layout(planes, info)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


ORDER = ["swell", "sail", "rigging", "mast", "windlass", "tiller", "compass-shut", "pot", "front"]

if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = "fast" in sys.argv
    base, info = under()
    Image.fromarray((base * 255).astype(np.uint8)).save(OUT + "-1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.26)
    print("brushed", round(time.time() - t0, 1))
    details(pic, info, fast=fast)
    print("details", round(time.time() - t0, 1))
    planes = {}
    planes["swell"] = swell_cut(info, SEED + 11, fast)
    planes["sail"] = sail_cut(info, SEED + 12, fast)
    planes["rigging"] = rigging_cut(info, SEED + 13, fast)
    planes["mast"] = mast_cut(info, SEED + 14, fast)
    planes["windlass"] = windlass_cut(pic, SEED + 15, fast)
    planes["tiller"] = tiller_cut(pic, SEED + 16, fast)
    planes["compass-shut"] = compass_cut(pic, SEED + 17, False, fast)
    planes["compass-open"] = compass_cut(pic, SEED + 17, True, fast)
    planes["pot"] = pot_cut(pic, SEED + 18, "lid", fast)
    planes["pot-lifted"] = pot_cut(pic, SEED + 18, "lifted", fast)
    planes["pot-steam"] = pot_cut(pic, SEED + 18, "steam", fast)
    planes["front"] = front_cut(pic, SEED + 19, fast)
    whole = pic.copy()
    for name in ORDER:
        c, a = planes[name]
        over(whole, c, (a > 0.5).astype(F32))
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-all.png")
    lay_ = layout(planes, info)
    with open(OUT + "/layout.json", "w") as f:
        json.dump(lay_, f, indent=1)
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    print("back", finish(pic, OUT + "/back.png", 152))
    sizes = {"swell": 64, "sail": 64, "rigging": 24, "mast": 48, "windlass": 48, "tiller": 32, "compass-shut": 40, "compass-open": 40,
             "pot": 32, "pot-lifted": 32, "pot-steam": 32, "front": 48}
    for name, n in sizes.items():
        print(name, finish(planes[name][0], OUT + f"/{name}.png", n, planes[name][1]))
    for i, (c, a) in enumerate(cask_frames(SEED + 30)):
        finish(c, OUT + f"/cask-{i + 1}.png", 24, a)
    comp = Image.open(OUT + "/back.png").convert("RGBA")
    for name in ORDER:
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(OUT + "-comp.png")
    print("done", round(time.time() - t0, 1))

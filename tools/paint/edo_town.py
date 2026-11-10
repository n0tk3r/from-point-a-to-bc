"""Himeji, about 29 April 1830, midday: Watamachi on the highway (edo-town). PAINT-21E, round twenty-one; PAINT-23 (round
twenty-three, tools/paint/DEPTH.md): painted again in THREE PLANES, and in WATERCOLOUR. The camera, the placings and every
number of the scene file are round twenty-one's and have not moved (but for the keep's and the roofs' areas, measured again,
and the near plane's patch of `blocked` ground).

The design (S/briefs/out/edo2-design.md, sections 4 and 5; S/briefs/PAINT-21E.md): the game's own painting, composed as the
woodblock landscape prints are (S/work-20-paintA/style.md), now laid as washes on paper. Nothing is copied from any print or
painting: the composition is our own.

What is in it (edo_town_kit.py has the camera and the plan): the broad highway across the bottom; across it, left to
right, the domain's paper-note office and cotton office along the bend of the street (two storeys, white; bales of white
cloth at the cotton office's door), the writing school with its shutters propped open (the raised floor inside, a row of
low desks: the girls and the teacher are the game's people), O-Tane's side yard open to the street with the kitchen
lean-to at its back (the stone-lined well and its pulley and bucket before it; the rice pot, the salt jar, the pickle tub
and its stone, the plum jar, a cloth, the roasting pan drying, the Bizen mortar), O-Tane's house (a lattice front, an
indigo noren), Tobei's hut (straw sandals hung, a jar of sweets, the clappers on a peg, his stool), the ward gate across
the lane north, its doors open by day. Above the roofs, on its hill, the keep. Not painted: people (the game's), smoke
(the kitchen's: fx), the noren's stirring (sway), birds (fx), light.

ROUND TWENTY-THREE
  NEAR    (edo_town_near.py: near.png, near-noren.png, the front plane) we look out from under the eaves of a house on
          our own side of the highway: its eave's underside across the top left, its corner where the house ends, its
          post down the left edge; the hem of the next shop's indigo curtain across the top right corner (it stirs). In
          shade, the warmest darks of the picture, lit only by the sunlit street's light thrown up into them.
  MIDDLE  the true noon (the sun 68 degrees up, behind us, a little left): every front facing us is in its own eave's
          shade from the eave down to a hand's breadth above the ground (the pent roofs: 40 cm; the cotton office's
          deeper eave: 90 cm), the attic walls under the main eaves too: hard-edged cool glazes over the local colour,
          warmed at their feet by the light thrown up from the street (shade()); the roofs, the street, the side yard, the
          bales and the step stone in the sun. The street: its worn tracks, footprints of sandals and clogs and straw
          horseshoes, stones at a true density, the plank-covered drain along the fronts, a sprinkled patch before
          O-Tane's door, and the dappled shade of a big tree behind us on the left lying across its near left part
          (street()). The side yard is the lightest light of the play.
  FAR     (edo_town_far.py) roofs behind roofs climbing toward the castle (a temple's roof, the ward's fire tower, spring
          trees); the castle's hill, its walls and turrets; the keep, larger and turned; two ridges of hills; the sky.
  PAPER   watercolor.wash on the backdrop and wash_cut (the same seed) on every cut-out, just before the palette (WET: the
          sky 1, the haze 0.8, the hills 0.6, the castle's hill 0.4, the far roofs 0.18, the keep 0.08; wander 1.4, fleck
          0.3: the far roofs and the keep must not run together or glitter). The key line is the scene's own quieter one
          (edo_town_wc.keyline); every flat is a graded wash (edo_town_wc.WSheet). The cut-outs keep round twenty-one's
          outlines exactly: the print's drawing gives each one's mask (STYLE["wc"] = False), the washes paint inside it.

  python3 edo_town.py           paints everything into out/edo-town/ (and out/edo-town-comp.png to look at)
  python3 edo_town.py fast      skips the brush pass and the palette: out/edo-town-2-all.png only
  python3 edo_town.py fast wash the same with the paper's finish: out/edo-town-fast-comp.png"""

import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, Sheet, grid, noise, blur, over, tint, glow, lerp, mask_poly, mask_ellipse, strokes, curve, warp, vary, ramp, step, grain, palette_of, to_palette, save
from rome_steps_kit import Canvas
from edo_town_kit import *
import edo_town_kit as KIT
from edo_town_wc import WSheet, wsheet_layer, keyline, thin, deepen, WPAPER, SHADE, SHADE_DEEP, BOUNCE, floor, street_noise, ground_pt, px_per_cm
import watercolor as WC
import depth as DPT
from edo_village_kit import Wet

SEED = 1830
STYLE = {"wc": True}    # False: the print's drawing exactly as round twenty-one drew it (the cut-outs' outlines are taken from it)


def outline(s, pts, width=1.0, alpha=0.6, close=True, color=LINE):
    """The contour: in watercolour the scene's quieter key line (broken, thin, lost on the lit edges); else the print's."""
    if STYLE["wc"]:
        return keyline(s, pts, width, alpha, close, color)
    return KIT.outline(s, pts, width, alpha, close, color)


def sheet_layer(draw, amount=0.6, ss=3, shape=SHAPE):
    """A thing drawn on its own sheet: in watercolour every flat a graded wash (edo_town_wc.WSheet); else the print's."""
    if STYLE["wc"]:
        return wsheet_layer(draw, amount, shape)
    return KIT.sheet_layer(draw, amount, ss, shape)


# the town's colours in watercolour: the kit's paints thinned toward the paper (a step lighter, more transparent), the
# darks kept deep; plaster in the sun is nearly the paper itself
_THIN = dict(plaster=0.62, plaster_sh=0.12, wood=0.12, wood_lit=0.18, wood_dark=0.04, wood_old=0.10, tile=0.16, tile_lit=0.22,
             tile_edge=0.25, tile_deep=0.0, street=0.50, street_lit=0.64, street_sh=0.1, rut=0.15, stone=0.22, stone_lit=0.32,
             stone_sh=0.10, indigo=0.03, indigo_lit=0.10, inside=0.02, inside_far=0.02, mat=0.22, mat_sh=0.10, straw=0.22,
             straw_sh=0.10, cloth=0.55, cloth_sh=0.12, bizen=0.06, bizen_lit=0.14, clay=0.12, iron=0.04, red=0.10)
C = {k: (thin(v, _THIN[k]) if k in _THIN else v) for k, v in KIT.C.items()}


# ---------------------------------------------------------------- the plan, in cm (X across, Y up, D from the lens)
DF = D_row(450)                     # the far row's fronts: 1640.6 cm (row 450)
GUT = DF - 32                       # the street's stone gutter along the fronts
COTTON = (-1322.0, -651.0)          # the domain's cotton office (two storeys; cut by the frame at the left)
NOTE = (-651.0, -432.0)             # the domain's paper-note office beside it
SCHOOL = (-432.0, -140.5)           # the writing school's front
YARD = (-140.5, 140.5)              # O-Tane's side yard, open to the street (the vanishing point in its middle)
TANE = (140.5, 401.0)               # O-Tane's house
HUT = (405.0, 528.0)                # Tobei's hut (its front at DF - 30: the street's edge)
GATE = (540.0, 725.0)               # the ward gate's posts (outer faces), across the lane north
LANE = (532.0, 742.0)
YARD_BACK = DF + 330.0              # the kitchen lean-to's front, at the back of the side yard
EAVE1, PENT_TOP, ATTIC_TOP, EAVE2, RIDGE = 236.0, 276.0, 396.0, 410.0, 520.0   # a townhouse front's heights
RIDGE_BACK = 300.0                  # the ridge's distance behind the front
OFF_EAVE1, OFF_UP0, OFF_UP1, OFF_EAVE2, OFF_RIDGE = 300.0, 330.0, 610.0, 625.0, 760.0   # the offices' (two storeys)


def front_poly(x0, x1, y0, y1, d=None):
    d = DF if d is None else d
    return [P(x0, y0, d), P(x1, y0, d), P(x1, y1, d), P(x0, y1, d)]


SUN_CAST = (0.10, 0.36)             # a shadow on the ground per cm of height: (across, away): the sun high behind us, a little left


# ---------------------------------------------------------------- the townhouse fronts
def roof_band(s, x0, x1, d_front, y_eave, proj, y_top, d_top, tone, lit=None, lift=2.5):
    """A tiled roof slope seen from the street: from its eave (`proj` cm in front of the wall at d_front, height
    y_eave) back to `y_top` at d_top. Flat tile colour, its lit flat toward the sun, the eave's edge light, the
    plastered underside a pale band, the tile rows as faint lines, the contour."""
    a, b = P(x0 - 15, y_eave, d_front - proj), P(x1 + 15, y_eave, d_front - proj)
    c_, d_ = P(x1, y_top, d_top), P(x0, y_top, d_top)
    ev = eave(a[0], b[0], a[1], lift=lift)
    poly = [d_, c_] + ev[::-1]
    # the eave's underside: seen from below when the eave is above the lens (the offices', the attics'), a dark band of
    # rafters between the eave's edge and the wall; under the roof's own top where it is below the lens (it is hidden)
    soffit = [P(x0 - 15, y_eave, d_front - proj), P(x1 + 15, y_eave, d_front - proj), P(x1, y_eave - 6, d_front), P(x0, y_eave - 6, d_front)]
    s.poly(soffit, mix(C["wood_dark"], PAINT["ultra"], 0.25))
    for i in range(1, max(3, int(abs(b[0] - a[0]) / 9))):
        t = i / max(3, int(abs(b[0] - a[0]) / 9))
        s.line([(soffit[0][0] + (soffit[1][0] - soffit[0][0]) * t, soffit[0][1] + (soffit[1][1] - soffit[0][1]) * t),
                (soffit[3][0] + (soffit[2][0] - soffit[3][0]) * t, soffit[3][1] + (soffit[2][1] - soffit[3][1]) * t)], mix(C["wood"], C["wood_dark"], 0.5), 1.0, 0.8)
    s.poly(poly, tone)
    if lit is not None:
        s.poly([d_, c_, (ev[-1][0], ev[-1][1] - (ev[-1][1] - c_[1]) * 0.45), (ev[0][0], ev[0][1] - (ev[0][1] - d_[1]) * 0.45)], lit, 0.5)
    n = max(3, int(abs(b[0] - a[0]) / 7))
    for i in range(1, n):
        t = i / n
        p0 = (ev[0][0] + (ev[-1][0] - ev[0][0]) * t, ev[0][1] + (ev[-1][1] - ev[0][1]) * t)
        p1 = (d_[0] + (c_[0] - d_[0]) * t, d_[1] + (c_[1] - d_[1]) * t)
        s.line([p0, p1], mix(tone, LINE, 0.35), 0.6, 0.35)
    s.line(ev, C["tile_edge"], 1.2, 0.85)
    s.line([(p[0], p[1] + 1.4) for p in ev], mix(PAPER, PAINT["cerulean"], 0.35), 2.0, 0.8)    # the plastered underside
    s.line([d_, c_], mix(tone, PAPER, 0.25), 1.0, 0.6)
    outline(s, poly, 0.8, 0.55)
    # the round eave-tile ends along the edge (the excavated Himeji tiles carried a triple-comma crest: here a dot each)
    for i in range(1, n):
        t = i / n
        q = (ev[0][0] + (ev[-1][0] - ev[0][0]) * t, ev[0][1] + (ev[-1][1] - ev[0][1]) * t)
        s.ellipse(q[0], q[1] + 0.6, 1.2, 1.2, mix(tone, LINE, 0.5), 0.8)
    return poly, ev


def townhouse_upper(s, x0, x1, tone_wall=None):
    """The low attic storey over a front (plastered, a slatted window), the main roof over it, back to the ridge."""
    wall = tone_wall if tone_wall is not None else C["plaster"]
    wp = front_poly(x0, x1, PENT_TOP, ATTIC_TOP, DF + 10)
    s.poly(wp, wall)
    top = P(0, ATTIC_TOP, DF)[1]
    s.poly([P(x0, ATTIC_TOP, DF + 10), P(x1, ATTIC_TOP, DF + 10), P(x1, ATTIC_TOP - 34, DF + 10), P(x0, ATTIC_TOP - 34, DF + 10)], shade_of(wall, 0.45), 0.9)   # the main eave's shade on it
    # the slatted window (plaster slats, the dark between)
    wx0, wx1 = x0 + (x1 - x0) * 0.22, x1 - (x1 - x0) * 0.22
    a, b = P(wx0, PENT_TOP + 22, DF + 8), P(wx1, PENT_TOP + 78, DF + 8)
    s.poly([(a[0], a[1]), (b[0], a[1]), (b[0], b[1]), (a[0], b[1])], C["inside"])
    n = int((b[0] - a[0]) / 5)
    for i in range(1, n):
        xx = a[0] + (b[0] - a[0]) * i / n
        s.line([(xx, a[1]), (xx, b[1])], shade_of(wall, 0.2), 2.2)
    outline(s, [(a[0], a[1]), (b[0], a[1]), (b[0], b[1]), (a[0], b[1])], 0.7, 0.5)
    outline(s, wp, 0.8, 0.5)
    roof_band(s, x0, x1, DF + 10, EAVE2, 50, RIDGE, DF + RIDGE_BACK, C["tile"], C["tile_lit"])


def pent_roof(s, x0, x1, d=None, proj=70.0):
    d = DF if d is None else d
    return roof_band(s, x0, x1, d, EAVE1, proj, PENT_TOP, d + 4, C["tile"], C["tile_lit"], lift=1.8)


# ---------------------------------------------------------------- the offices on the bend
COTTON_DOOR = (-1010.0, -760.0)     # the cotton office's wide doorway (X)
NOTE_DOOR = (-610.0, -520.0)


def office(s, x0, x1, kind):
    """One of the domain's offices on the highway: two storeys, the upper one white plaster with barred windows under
    a deep tiled eave, a pent roof between the storeys, dark wood below; the cotton office's wide doorway (its noren is
    a cut-out: it stirs), the note office's latticed door and its small hanging board (the writing our own marks)."""
    # the upper storey
    up = front_poly(x0, x1, OFF_UP0, OFF_UP1, DF + 12)
    s.poly(up, C["plaster"])
    s.poly(front_poly(x0, x1, OFF_UP1 - 56, OFF_UP1, DF + 12), shade_of(C["plaster"], 0.42), 0.9)        # the eave's shade
    wins = [(-1240.0, -1120.0), (-990.0, -870.0), (-780.0, -680.0)] if kind == "cotton" else [(-600.0, -480.0)]
    for (wa, wb) in wins:
        win = front_poly(wa, wb, 420, 520, DF + 10)
        s.poly(win, C["inside"])
        n = int((wb - wa) / 16)
        for kk in range(1, n):
            xx = wa + (wb - wa) * kk / n
            s.line([P(xx, 420, DF + 10), P(xx, 520, DF + 10)], C["plaster"], 2.0)
        outline(s, win, 0.6, 0.5)
    outline(s, up, 0.8, 0.5)
    # the main roof, back to its ridge; the note office's right end is hipped: its end face shows over the school
    if kind == "note":
        side = [P(x1, OFF_UP0, DF + 12), P(x1, OFF_UP0, DF + 520), P(x1, OFF_UP1, DF + 520), P(x1, OFF_UP1, DF + 12)]
        s.poly(side, shade_of(C["plaster"], 0.38))                                       # its right side wall, over the school's roof
        s.poly([P(x1, OFF_UP1 - 50, DF + 12), P(x1, OFF_UP1 - 50, DF + 520), P(x1, OFF_UP1, DF + 520), P(x1, OFF_UP1, DF + 12)], shade_of(C["plaster"], 0.6), 0.8)
        outline(s, side, 0.7, 0.5)
        e0 = P(x1 + 15, OFF_EAVE2, DF + 12 - 60)
        r0 = P(x1, OFF_RIDGE, DF + 230)
        e1 = P(x1 + 15, OFF_EAVE2, DF + 12 + 520)
        hip = [e0, r0, e1]
        s.poly(hip, mix(C["tile"], PAINT["ultra"], 0.15))
        s.line([e0, r0], C["tile_edge"], 1.4, 0.85)
        s.line([e0, e1], C["tile_edge"], 1.0, 0.7)
        for k in range(1, 6):
            t = k / 6
            s.line([(e0[0] + (e1[0] - e0[0]) * t, e0[1] + (e1[1] - e0[1]) * t), r0], mix(C["tile"], LINE, 0.35), 0.6, 0.45)
        outline(s, hip, 0.7, 0.5)
    roof_band(s, x0, x1, DF + 12, OFF_EAVE2, 60, OFF_RIDGE, DF + 230, C["tile"], C["tile_lit"], lift=3.0)
    # the ground storey: dark wood, a fine lattice, the doorway
    lo = front_poly(x0, x1, 0, OFF_EAVE1 + 4)
    s.poly(lo, C["wood"])
    if kind == "cotton":
        da, db = COTTON_DOOR
        la = [(x0 + 20, da - 20), (db + 20, x1 - 14)]
    else:
        da, db = NOTE_DOOR
        la = [(db + 16, x1 - 14)]
    for (a_, b_) in la:
        if b_ - a_ < 20:
            continue
        s.poly(front_poly(a_, b_, 40, 230, DF - 2), mix(PAPER, C["inside"], 0.4))
        n = int((b_ - a_) / 6.5)
        for i in range(n + 1):
            xx = a_ + (b_ - a_) * i / n
            s.line([P(xx, 40, DF - 4), P(xx, 230, DF - 4)], C["wood_dark"], 1.5, 0.95)
        outline(s, front_poly(a_, b_, 40, 230, DF - 4), 0.6, 0.5)
    door = front_poly(da, db, 0, 250)
    s.poly(door, C["inside"])
    s.poly(front_poly(da - 9, da, 0, 262), C["wood_dark"])
    s.poly(front_poly(db, db + 9, 0, 262), C["wood_dark"])
    if kind == "cotton":
        s.poly(front_poly(da, db, 0, 4, DF + 60), mix(C["inside"], C["street"], 0.35))
        for (xa, h) in ((-990.0, 80.0), (-950.0, 44.0), (-905.0, 80.0), (-860.0, 44.0), (-820.0, 80.0)):      # bales inside, in the dim
            s.poly(front_poly(xa, xa + 38, 4, 4 + h, DF + 140), mix(C["cloth"], C["inside"], 0.5))
    else:
        for k in range(1, 7):
            xx = da + (db - da) * k / 7
            s.line([P(xx, 0, DF - 2), P(xx, 250, DF - 2)], C["wood_dark"], 1.8)
        bd = front_poly(-470.0, -446.0, 120, 230, DF - 6)
        s.poly(bd, mix(C["wood_lit"], PAPER, 0.45))
        for kk in range(4):
            yy = 210 - kk * 24
            s.line([P(-462, yy, DF - 7), P(-462, yy - 12, DF - 7)], C["wood_dark"], 1.3, 0.9)
            s.line([P(-454, yy - 3, DF - 7), P(-452, yy - 14, DF - 7)], C["wood_dark"], 1.1, 0.9)
        outline(s, bd, 0.6, 0.6)
    outline(s, lo, 0.8, 0.55)
    # the pent roof between the storeys
    roof_band(s, x0, x1, DF, OFF_EAVE1, 75, OFF_UP0, DF + 12, C["tile"], C["tile_lit"], lift=2.0)


def offices(s):
    office(s, COTTON[0], COTTON[1], "cotton")
    office(s, NOTE[0], NOTE[1], "note")


BALES = [(-1240.0, 0, 3), (-1180.0, 1, 2), (-740.0, 0, 2), (-700.0, 0, 3), (-720.0, 1, 1)]   # stacks: X, row out from the front, how high


def bales(s):
    """The bales of white cloth going into the cotton office: stacked on the street before its front, either side of
    the doorway (wrapped in straw mats, roped)."""
    for (X, row, n) in BALES:
        d = DF - 30 - row * 46
        for k in range(n):
            y0 = k * 30
            face = front_poly(X, X + 54, y0, y0 + 29, d)
            side = [P(X + 54, y0, d), P(X + 54, y0, d + 40), P(X + 54, y0 + 29, d + 40), P(X + 54, y0 + 29, d)]
            if STYLE["wc"]:                                    # (round twenty-three) its end toward the street, turned from the sun
                s.poly(side, C["cloth"] * SHADE)
            s.poly(face, mix(C["cloth"], C["straw"], 0.32))
            s.poly([P(X, y0 + 29, d), P(X + 54, y0 + 29, d), P(X + 54, y0 + 29, d + 40), P(X, y0 + 29, d + 40)], mix(C["cloth"], PAPER, 0.45))   # its top, lit
            if STYLE["wc"]:                                    # the straw mat's weave, and its rope ties
                for k2 in range(1, 6):
                    yy = y0 + 29 * k2 / 6
                    s.line([P(X + 1, yy, d - 0.4), P(X + 53, yy, d - 0.4)], mix(C["straw"], C["cloth"], 0.4), 0.5, 0.35)
            for xr in (X + 16, X + 38):
                s.line([P(xr, y0, d - 0.5), P(xr, y0 + 29, d - 0.5)], C["straw_sh"], 1.0, 0.8)
            outline(s, face, 0.6, 0.5)


# ---------------------------------------------------------------- the writing school
SCH_FLOOR = 45.0                    # the raised floor inside, cm
SCH_DEPTH = 360.0
DESK_D = DF + 120.0                 # the row of desks: their front edge
DESK_W = 54.0
DESKS = [-414.0, -354.0, -294.0, -234.0]      # each desk's left end X: the girls at the first two; the third free (Little Sister's), the fourth free (O-Kiku's)
ROOM = (-424.0, -148.5)             # the open front's clear width (between the corner posts)


def school_inside(s):
    """What the open front shows (in the backdrop): the room on its raised floor, dim, its matting, its back wall of
    sliding doors and a shelf of practice books, the light of the street on the nearest boards."""
    x0, x1 = SCHOOL
    d0, d1 = DF + 6, DF + SCH_DEPTH
    yf = SCH_FLOOR
    # the back wall
    s.poly([P(x0, yf, d1), P(x1, yf, d1), P(x1, 236, d1), P(x0, 236, d1)], mix(C["inside"], PAPER, 0.18))
    for k in range(5):                                          # sliding doors, paper panes faint in the dim
        xa = x0 + (x1 - x0) * k / 5 + 6
        xb = x0 + (x1 - x0) * (k + 1) / 5 - 6
        s.poly([P(xa, yf + 12, d1), P(xb, yf + 12, d1), P(xb, 200, d1), P(xa, 200, d1)], mix(PAPER, C["inside"], 0.55))
        for j in range(1, 5):
            yy = yf + 12 + (200 - yf - 12) * j / 5
            s.line([P(xa, yy, d1), P(xb, yy, d1)], mix(C["inside"], C["wood"], 0.5), 0.7, 0.8)
        s.line([P((xa + xb) / 2, yf + 12, d1), P((xa + xb) / 2, 200, d1)], mix(C["inside"], C["wood"], 0.5), 0.7, 0.8)
    s.line([P(x0, 200, d1), P(x1, 200, d1)], C["wood_dark"], 1.6)
    # the shelf of practice books on the right (by the teacher)
    sh = [P(x1 - 90, yf, d1 - 4), P(x1 - 8, yf, d1 - 4), P(x1 - 8, yf + 120, d1 - 4), P(x1 - 90, yf + 120, d1 - 4)]
    s.poly(sh, C["wood"])
    for k in range(3):
        yy = yf + 18 + k * 36
        for j in range(5):
            xa = x1 - 86 + j * 15
            s.poly([P(xa, yy, d1 - 6), P(xa + 11, yy, d1 - 6), P(xa + 11, yy + 26, d1 - 6), P(xa, yy + 26, d1 - 6)],
                   mix(PAPER, PAINT["naples"], 0.2) if (j + k) % 3 else mix(PAPER, LINE, 0.55))
    outline(s, sh, 0.6, 0.5)
    # the side walls (the left one shows: it faces the line of sight)
    s.poly([P(x0, yf, d0), P(x0, yf, d1), P(x0, 236, d1), P(x0, 236, d0)], mix(C["inside"], C["plaster"], 0.22))
    # the floor: matting, its joins running back; light from the street on its front edge
    fl = [P(x0, yf, d0), P(x1, yf, d0), P(x1, yf, d1), P(x0, yf, d1)]
    s.poly(fl, mix(C["mat"], C["inside"], 0.45))
    for k in range(1, 4):
        xx = x0 + (x1 - x0) * k / 4
        s.line([P(xx, yf, d0), P(xx, yf, d1)], mix(C["mat_sh"], C["inside"], 0.5), 0.7, 0.7)
    s.line([P(x0, yf, d0 + 180), P(x1, yf, d0 + 180)], mix(C["mat_sh"], C["inside"], 0.5), 0.7, 0.7)
    s.poly([P(x0, yf, d0), P(x1, yf, d0), P(x1, yf, d0 + 70), P(x0, yf, d0 + 70)], mix(C["mat"], PAINT["naples"], 0.25), 0.55)   # the street's light on the near mats
    # the ceiling (the underside of the pent roof's level): dark boards
    s.poly([P(x0, 236, d0), P(x1, 236, d0), P(x1, 236, d1), P(x0, 236, d1)], C["inside_far"])
    # the teacher's low writing table and her brush rest, at the right end, by the shelf
    tx = x1 - 82
    tb = [P(tx, yf, DF + 210), P(tx + 70, yf, DF + 210), P(tx + 70, yf + 28, DF + 210), P(tx, yf + 28, DF + 210)]
    s.poly(tb, C["wood_old"])
    s.poly([P(tx, yf + 28, DF + 210), P(tx + 70, yf + 28, DF + 210), P(tx + 70, yf + 28, DF + 250), P(tx, yf + 28, DF + 250)], C["wood_lit"])
    s.poly([P(tx + 10, yf + 29, DF + 222), P(tx + 30, yf + 29, DF + 222), P(tx + 30, yf + 29, DF + 238), P(tx + 10, yf + 29, DF + 238)], PAPER)   # a sheet of paper on it
    outline(s, tb, 0.6, 0.5)


def desks(s):
    """The row of low desks inside (a cut-out: the girls kneel behind them): plain wood, a practice book open on each
    but the third (Little Sister's, free), an inkstone, a brush."""
    for i, xa in enumerate(DESKS):
        xb = xa + DESK_W
        d0, d1 = DESK_D, DESK_D + 32
        y = SCH_FLOOR + 26
        front = [P(xa, SCH_FLOOR, d0), P(xb, SCH_FLOOR, d0), P(xb, y, d0), P(xa, y, d0)]
        top = [P(xa, y, d0), P(xb, y, d0), P(xb, y, d1), P(xa, y, d1)]
        s.poly(front, C["wood"])
        s.poly([P(xa + 4, SCH_FLOOR, d0), P(xb - 4, SCH_FLOOR, d0), P(xb - 4, y - 6, d0), P(xa + 4, y - 6, d0)], C["wood_dark"], 0.9)   # the open front under the top
        s.poly(top, C["wood_lit"])
        if i < 2:
            s.poly([P(xa + 8, y + 0.5, d0 + 6), P(xa + 40, y + 0.5, d0 + 6), P(xa + 40, y + 0.5, d0 + 26), P(xa + 8, y + 0.5, d0 + 26)], PAPER)     # the practice book, open
            s.line([P(xa + 24, y + 0.6, d0 + 6), P(xa + 24, y + 0.6, d0 + 26)], mix(PAPER, LINE, 0.4), 0.6)
            for k in range(3):                                                                                                       # its inked practice strokes
                s.line([P(xa + 12 + k * 9, y + 0.7, d0 + 10), P(xa + 13 + k * 9, y + 0.7, d0 + 22)], LINE, 1.0, 0.8)
        s.poly([P(xb - 16, y + 0.5, d0 + 8), P(xb - 6, y + 0.5, d0 + 8), P(xb - 6, y + 0.5, d0 + 24), P(xb - 16, y + 0.5, d0 + 24)], mix(LINE, C["wood_dark"], 0.4))   # the inkstone
        s.line([P(xa + 44, y + 1, d0 + 4), P(xa + 50, y + 1, d0 + 28)], C["wood_dark"], 0.9)                                    # the brush
        outline(s, front + [top[3], top[2]][::-1][:0], 0.6, 0.55)
        outline(s, top, 0.6, 0.55)


def school_front(s, shut=False):
    """The school's front (a cut-out, its opening clear): the corner posts and the sill of the raised floor, the upper
    shutters hooked up flat under the eave, the lower ones lifted out and stacked against the left post; at the right
    end the step stone where the pupils leave their sandals and step up; the pent roof. Shut (for the night): the
    shutters down across the whole front."""
    x0, x1 = SCHOOL
    r0, r1 = ROOM
    for xp in (x0, r1):
        s.poly([P(xp, 0, DF), P(xp + 8, 0, DF), P(xp + 8, EAVE1 + 4, DF), P(xp, EAVE1 + 4, DF)], C["wood"])
        s.line([P(xp + 2, 0, DF), P(xp + 2, EAVE1, DF)], C["wood_lit"], 1.0, 0.7)
    s.poly([P(r1 + 8, 0, DF), P(x1, 0, DF), P(x1, EAVE1 + 4, DF), P(r1 + 8, EAVE1 + 4, DF)], C["wood_dark"])      # the corner's board
    s.poly([P(x0, 214, DF), P(x1, 214, DF), P(x1, EAVE1 + 4, DF), P(x0, EAVE1 + 4, DF)], C["wood_dark"])          # the head beam
    # the raised floor's front: its edge board, and the boards closing the space under it
    s.poly([P(r0, 0, DF), P(r1, 0, DF), P(r1, SCH_FLOOR, DF), P(r0, SCH_FLOOR, DF)], C["wood_dark"])
    s.poly([P(r0, SCH_FLOOR - 9, DF), P(r1, SCH_FLOOR - 9, DF), P(r1, SCH_FLOOR, DF), P(r0, SCH_FLOOR, DF)], C["wood_lit"])
    for k in range(7):
        xx = r0 + 10 + k * (r1 - r0 - 20) / 6
        s.line([P(xx, 2, DF), P(xx, SCH_FLOOR - 10, DF)], C["wood"], 1.0, 0.8)
    if not shut:
        a, b = P(r0, 212, DF), P(r1, 212, DF)
        c_, d_ = P(r1, 206, DF - 62), P(r0, 206, DF - 62)
        s.poly([a, b, c_, d_], C["wood_old"])
        s.line([d_, c_], C["wood_lit"], 1.2, 0.8)
        for k in range(1, 6):
            t = k / 6
            s.line([(a[0] + (b[0] - a[0]) * t, a[1]), (d_[0] + (c_[0] - d_[0]) * t, d_[1])], C["wood_dark"], 0.8, 0.7)
        outline(s, [a, b, c_, d_], 0.7, 0.55)
        for xp in (r0 + 24, r1 - 24):                         # the hooks holding them up
            s.line([P(xp, 236, DF), P(xp, 206, DF - 62)], C["iron"], 1.0, 0.9)
        for k in range(3):                                    # the lower shutters, lifted out, stacked against the left post
            sx = P(x0 - 4, 0, DF - 24)[0]
            y0_, y1_ = P(0, 0, DF - 24)[1], P(0, 122, DF - 24)[1]
            pts = [(sx - 9 + k * 3.2, y0_), (sx + 3 + k * 3.2, y0_), (sx + 3 + k * 3.2, y1_), (sx - 9 + k * 3.2, y1_)]
            s.poly(pts, C["wood_old"] if k % 2 else C["wood"])
            outline(s, pts, 0.6, 0.55)
    else:
        sh = [P(r0, SCH_FLOOR, DF - 2), P(r1, SCH_FLOOR, DF - 2), P(r1, 212, DF - 2), P(r0, 212, DF - 2)]
        s.poly(sh, C["wood_old"])
        for k in range(1, 7):
            xx = r0 + (r1 - r0) * k / 7
            s.line([P(xx, SCH_FLOOR, DF - 2), P(xx, 212, DF - 2)], C["wood_dark"], 1.0, 0.8)
        s.line([P(r0, 128, DF - 2), P(r1, 128, DF - 2)], C["wood_dark"], 1.0, 0.8)
        outline(s, sh, 0.7, 0.55)
    # the step stone before the right end, where the pupils step up
    stone = [P(r1 - 70, 0, DF - 52), P(r1 - 6, 0, DF - 52), P(r1 - 8, 16, DF - 42), P(r1 - 68, 16, DF - 42)]
    s.poly(stone, C["stone_lit"])
    s.poly([P(r1 - 70, 0, DF - 52), P(r1 - 6, 0, DF - 52), P(r1 - 6, 4, DF - 52), P(r1 - 70, 4, DF - 52)], C["stone"])
    outline(s, stone, 0.6, 0.5)
    pent_roof(s, x0, x1)
    outline(s, [P(x0, 0, DF), P(x1, 0, DF), P(x1, EAVE1, DF), P(x0, EAVE1, DF)], 0.8, 0.5)


def school_clear(s):
    """The opening wiped clear (the room and the people in it show through)."""
    r0, r1 = ROOM
    s.clear([P(r0 + 1, SCH_FLOOR + 0.5, DF), P(r1 - 1, SCH_FLOOR + 0.5, DF), P(r1 - 1, 205, DF - 60), P(r0 + 1, 205, DF - 60)])


def school_upper(s):
    townhouse_upper(s, SCHOOL[0], SCHOOL[1])


def school_doorway(s):
    """(The pupils' sandals, left on the step stone's ground at the right end: in the backdrop.)"""
    r0, r1 = ROOM
    for k in range(3):
        xx = r1 - 60 + k * 18
        s.ellipse(*P(xx, 1, DF - 64), 3.0, 1.1, C["straw"], 0.9)
        s.ellipse(*P(xx + 4, 1, DF - 64), 3.0, 1.1, C["straw"], 0.9)


# ---------------------------------------------------------------- O-Tane's side yard, the kitchen at its back
WELL = dict(X=88.0, D=DF + 96.0, r=37.0, h=60.0)           # the stone-lined well, at the yard's front right: centre, radius, curb height
FRAME = dict(h=196.0)                                         # the pulley frame over it
KDOOR = (-128.0, -52.0)                                       # the kitchen door in the lean-to's front (X), at the back left
SHELF = dict(x=(-34.0, 128.0), D=YARD_BACK - 4, y=96.0)      # a shelf on the lean-to's wall: the jars, the cloth
THINGS = dict(
    ricepot=dict(X=-4.0, D=YARD_BACK - 36, w=40.0, h=34.0),  # the rice pot on its stand, under the shelf
    saltjar=dict(X=-22.0, D=SHELF["D"] - 10, w=26.0, h=30.0),   # on the shelf
    plumjar=dict(X=14.0, D=SHELF["D"] - 10, w=30.0, h=32.0),
    cloth=dict(X=46.0, D=SHELF["D"] - 26, w=34.0, h=8.0),
    pickletub=dict(X=40.0, D=YARD_BACK - 80, w=46.0, h=38.0),      # on the ground before the shelf, a stone on its lid
    pan=dict(X=-112.0, D=DF + 40, w=40.0),                  # the roasting pan, stood on its rim against the school's wall to dry
    mortar=dict(X=10.0, D=DF + 110, w=38.0, h=14.0),         # the Bizen mortar on the ground by the well
)
BENCH = dict(x=SHELF["x"], D=SHELF["D"] - 26, h=SHELF["y"])   # (the cloth's code reads its height from here)


def yard(s):
    """The side yard (backdrop): its packed earth running back; the school's plastered side wall at its left and
    O-Tane's at its right (each seen a little, as the line of sight runs between them); at its back the kitchen
    lean-to facing us under its own small roof: dark boards, the doorway (the door is a cut-out), a smoke-hole, the
    bench against it; the yard in the sun, the walls' feet in their own shade."""
    x0, x1 = YARD
    d0, d1 = DF, YARD_BACK
    # the floor
    fl = [P(x0, 0, d0), P(x1, 0, d0), P(x1, 0, d1), P(x0, 0, d1)]
    s.poly(fl, C["street"])
    s.poly([P(x0 + 30, 0, d0), P(x1 - 30, 0, d0), P(x1 - 30, 0, d1), P(x0 + 30, 0, d1)], C["street_lit"], 0.5)
    # the two side walls: plaster over a dark board skirting
    for (xw, tone) in ((x0, C["plaster_sh"]), (x1, mix(C["plaster"], C["plaster_sh"], 0.4))):
        wall = [P(xw, 0, d0), P(xw, 0, d1 + 40), P(xw, 380, d1 + 40), P(xw, 380, d0)]
        s.poly(wall, tone)
        s.poly([P(xw, 0, d0), P(xw, 0, d1 + 40), P(xw, 70, d1 + 40), P(xw, 70, d0)], C["wood_dark"], 0.85)
        outline(s, wall, 0.6, 0.45)
    # the lean-to at the back, facing us
    lt = [P(x0, 0, d1), P(x1, 0, d1), P(x1, 210, d1), P(x0, 210, d1)]
    s.poly(lt, C["wood_old"])
    for k in range(1, 12):
        xx = x0 + (x1 - x0) * k / 12
        s.line([P(xx, 0, d1), P(xx, 210, d1)], C["wood_dark"], 0.7, 0.45)
    s.poly([P(KDOOR[0], 0, d1), P(KDOOR[1], 0, d1), P(KDOOR[1], 176, d1), P(KDOOR[0], 176, d1)], C["inside"])   # the doorway (the door is a cut-out)
    s.poly([P(KDOOR[0] + 6, 0, d1 + 60), P(KDOOR[1] - 6, 0, d1 + 60), P(KDOOR[1] - 6, 60, d1 + 60), P(KDOOR[0] + 6, 60, d1 + 60)], mix(C["clay"], C["inside"], 0.35))   # the clay stove inside, dim
    s.ellipse(*P((KDOOR[0] + KDOOR[1]) / 2, 30, d1 + 58), 3.0, 2.0, PAINT["orange"], 0.9)                    # its fire, a coal
    # the smoke-hole under the lean-to's eave
    sh = [P(-40, 186, d1), P(-4, 186, d1), P(-4, 202, d1), P(-40, 202, d1)]
    s.poly(sh, C["inside"])
    for k in range(4):
        xx = -36 + k * 9
        s.line([P(xx, 186, d1), P(xx, 202, d1)], C["wood"], 1.0)
    outline(s, lt, 0.7, 0.5)
    # its little roof, tiled, from 214 up to 252 at the house wall behind
    roof_band(s, x0, x1, d1, 216, 30, 250, d1 + 60, C["tile"], C["tile_lit"], lift=1.2)
    # the shelf on the lean-to's wall, on two brackets
    sx0, sx1 = SHELF["x"]
    sd, sy = SHELF["D"], SHELF["y"]
    s.poly([P(sx0, sy, sd - 30), P(sx1, sy, sd - 30), P(sx1, sy, sd), P(sx0, sy, sd)], C["wood_lit"])
    s.poly([P(sx0, sy - 5, sd - 30), P(sx1, sy - 5, sd - 30), P(sx1, sy, sd - 30), P(sx0, sy, sd - 30)], C["wood"])
    for xl in (sx0 + 10, sx1 - 14):
        s.line([P(xl, sy - 5, sd - 26), P(xl, sy - 30, sd - 1)], C["wood_dark"], 1.4)
    outline(s, [P(sx0, sy - 5, sd - 30), P(sx1, sy - 5, sd - 30), P(sx1, sy, sd), P(sx0, sy, sd)], 0.5, 0.5)
    # the wall's shade at the foot of the right wall and under the lean-to's eave
    s.poly([P(x0, 0, d1 - 40), P(x1, 0, d1 - 40), P(x1, 0, d1), P(x0, 0, d1)], C["cast"], 0.35)
    s.poly([P(x0, 0, d0), P(x0 + 34, 0, d0), P(x0 + 34, 0, d1), P(x0, 0, d1)], C["cast"], 0.30)


KURA = dict(x=(-150.0, 170.0), D=YARD_BACK + 260.0, h=470.0, ridge=600.0)


def kura(s):
    """A storehouse behind the lot (backdrop), seen over the lean-to's roof between the two houses: thick white
    plaster on a dark board skirt, a small barred window with its heavy shutter, a tiled roof."""
    x0, x1 = KURA["x"]
    d, h = KURA["D"], KURA["h"]
    wall = front_poly(x0, x1, 0, h, d)
    s.poly(wall, mix(C["plaster"], PAPER, 0.2))
    s.poly(front_poly(x0, x1, 0, 120, d), C["wood_dark"])
    s.poly(front_poly(x0, x1, h - 40, h, d), shade_of(C["plaster"], 0.4), 0.9)
    win = front_poly(-10.0, 50.0, 330, 400, d)
    s.poly(win, C["inside"])
    for xx in (5.0, 20.0, 35.0):
        s.line([P(xx, 330, d), P(xx, 400, d)], mix(C["plaster"], PAPER, 0.2), 1.6)
    s.poly(front_poly(52.0, 112.0, 330, 400, d - 6), mix(C["plaster"], C["plaster_sh"], 0.3))        # its shutter, swung open
    outline(s, win, 0.5, 0.5)
    outline(s, wall, 0.6, 0.45)
    roof_band(s, x0, x1, d, h + 6, 40, KURA["ridge"], d + 200, C["tile"], C["tile_lit"], lift=1.5)


def well(s):
    """The stone-lined well (a cut-out: Mom stands before it, and goes behind it to the kitchen door): a round curb
    of dressed stones, a wooden frame over it with a crossbar and the pulley, the rope."""
    X, D, r, h = WELL["X"], WELL["D"], WELL["r"], WELL["h"]
    # the curb: a short drum seen from above-front (its top an ellipse, its front face a band of stones)
    n = 28
    top = [P(X + r * math.cos(2 * math.pi * i / n), h, D + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    foot = [P(X + r * math.cos(2 * math.pi * i / n), 0, D + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    front = [foot[i] for i in range(n // 2 - 1, -1, -1)] if False else None
    left = min(range(n), key=lambda i: top[i][0])
    right = max(range(n), key=lambda i: top[i][0])
    body = [P(X - r, 0, D), P(X + r, 0, D), P(X + r, h, D), P(X - r, h, D)]
    lo = [P(X + r * math.cos(math.pi * i / 14), 0, D - r * math.sin(math.pi * i / 14)) for i in range(15)]
    hi = [P(X + r * math.cos(math.pi * i / 14), h, D - r * math.sin(math.pi * i / 14)) for i in range(15)]
    s.poly(lo + hi[::-1], C["stone"])
    s.poly(lo[7:] + hi[7:][::-1], C["stone_sh"], 0.55)
    for k in (1, 2):                                            # the courses of stones
        yy = h * k / 3
        s.line([P(X + r * math.cos(math.pi * i / 14), yy, D - r * math.sin(math.pi * i / 14)) for i in range(15)], C["stone_sh"], 0.7, 0.6)
    for i in range(1, 14, 2):
        a = math.pi * i / 14
        for k in range(3):
            y0, y1 = h * k / 3, h * (k + 1) / 3
            off = 0.5 * (k % 2) * math.pi / 14
            s.line([P(X + r * math.cos(a + off), y0, D - r * math.sin(a + off)), P(X + r * math.cos(a + off), y1, D - r * math.sin(a + off))], C["stone_sh"], 0.6, 0.55)
    s.poly(top, C["stone_lit"])
    inner = [P(X + (r - 8) * math.cos(2 * math.pi * i / n), h, D + (r - 8) * math.sin(2 * math.pi * i / n)) for i in range(n)]
    s.poly(inner, mix(LINE, C["inside"], 0.4))
    outline(s, lo + hi[::-1], 0.7, 0.55)
    outline(s, top, 0.6, 0.5)
    # the frame: two posts and a crossbar, the pulley at its middle
    fh = FRAME["h"]
    for xp in (X - r - 4, X + r - 2):
        s.poly([P(xp, 0, D + 2), P(xp + 6, 0, D + 2), P(xp + 6, fh, D + 2), P(xp, fh, D + 2)], C["wood"])
        s.line([P(xp + 1.5, 0, D + 2), P(xp + 1.5, fh, D + 2)], C["wood_lit"], 0.8, 0.8)
        outline(s, [P(xp, 0, D + 2), P(xp + 6, 0, D + 2), P(xp + 6, fh, D + 2), P(xp, fh, D + 2)], 0.5, 0.5)
    bar = [P(X - r - 12, fh - 2, D + 2), P(X + r + 10, fh - 2, D + 2), P(X + r + 10, fh + 7, D + 2), P(X - r - 12, fh + 7, D + 2)]
    s.poly(bar, C["wood_dark"])
    outline(s, bar, 0.5, 0.55)
    px, py = P(X, fh - 12, D + 2)
    rr = 7 * k_at(D)
    s.ellipse(px, py, rr + 1.2, rr + 1.2, C["wood_dark"])
    s.ellipse(px, py, rr, rr, C["wood_lit"])
    s.line([P(X, fh - 2, D + 2), (px, py)], C["iron"], 1.0)


def bucket_layer(s, down=False):
    """The bucket on its rope: up (hanging under the pulley, above the curb) or down (the rope running down into the
    well, the bucket out of sight)."""
    X, D, fh = WELL["X"], WELL["D"], FRAME["h"]
    px, py = P(X, fh - 12, D + 2)
    rr = 7 * k_at(D)
    if down:
        s.line([(px - rr, py), P(X - 4, WELL["h"] - 2, D + 4)], C["straw_sh"], 1.0)
        s.line([(px + rr, py), P(X + 30, 120, D + 2), P(X + 46, 0, D - 10)], C["straw_sh"], 1.0)   # the free end, to its peg
        return
    by = 104.0
    s.line([(px - rr, py), P(X - 4, by + 30, D + 2)], C["straw_sh"], 1.0)
    s.line([(px + rr, py), P(X + 30, 120, D + 2), P(X + 46, 0, D - 10)], C["straw_sh"], 1.0)
    b = [P(X - 16, by, D), P(X + 8, by, D), P(X + 10, by + 26, D), P(X - 18, by + 26, D)]
    s.poly(b, C["wood"])
    s.poly([b[0], (b[0][0] + 3, b[0][1]), (b[3][0] + 3, b[3][1]), b[3]], C["wood_dark"], 0.6)
    s.line([P(X - 17, by + 6, D), P(X + 9, by + 6, D)], C["iron"], 0.8)
    s.line([P(X - 17.5, by + 20, D), P(X + 9.5, by + 20, D)], C["iron"], 0.8)
    s.line(curve([P(X - 17, by + 26, D), P(X - 4, by + 36, D), P(X + 9, by + 26, D)], 5), C["wood_dark"], 1.0)
    outline(s, b, 0.6, 0.55)


def jar(s, X, D, w, h, body, lid=None, lit=None, rope=False, y0=0.0):
    """A plain jar or crock seen a little from above, standing at height y0: a body, its shade flat, a mouth, a lid."""
    r = w / 2
    pts = []
    for i in range(13):
        t = i / 12
        bulge = 1.0 - 0.25 * (2 * t - 1) ** 2
        pts.append(P(X - r * (0.72 + 0.28 * bulge), y0 + h * t, D))
    pts2 = [P(X + r * (0.72 + 0.28 * (1.0 - 0.25 * (2 * (i / 12) - 1) ** 2)), y0 + h * i / 12, D) for i in range(12, -1, -1)]
    shape_ = pts + pts2
    s.poly(shape_, body)
    s.poly(pts[6:] + [P(X - r * 0.3, y0 + h, D), P(X - r * 0.3, y0 + h * 0.5, D)], lit if lit is not None else mix(body, PAPER, 0.25), 0.55)
    s.poly(pts2[:7] + [P(X + r * 0.35, y0 + h * 0.5, D)], shade_of(body, 0.35), 0.6)
    if lid is not None:
        s.ellipse(*P(X, y0 + h + 1, D), r * 0.8 * k_at(D), max(1.2, r * 0.25 * k_at(D)), lid)
    outline(s, shape_, 0.6, 0.6)
    return shape_


def ricepot(s):
    """The rice pot (cooked: O-Tane's), an iron pot with a heavy wooden lid on a low stand by the kitchen door; the
    paddle across the lid."""
    t = THINGS["ricepot"]
    X, D, w, h = t["X"], t["D"], t["w"], t["h"]
    st = [P(X - 22, 0, D), P(X + 22, 0, D), P(X + 22, 12, D), P(X - 22, 12, D)]
    s.poly(st, C["wood_dark"])
    s.poly([P(X - 24, 12, D - 6), P(X + 24, 12, D - 6), P(X + 24, 12, D + 20), P(X - 24, 12, D + 20)], C["wood"])
    body = [P(X - w / 2, 12, D), P(X + w / 2, 12, D), P(X + w / 2 + 3, 12 + h * 0.55, D), P(X + w / 2 - 2, 12 + h, D), P(X - w / 2 + 2, 12 + h, D), P(X - w / 2 - 3, 12 + h * 0.55, D)]
    s.poly(body, C["iron"])
    s.poly([P(X - w / 2 - 6, 12 + h * 0.55, D), P(X + w / 2 + 6, 12 + h * 0.55, D), P(X + w / 2 + 6, 12 + h * 0.62, D), P(X - w / 2 - 6, 12 + h * 0.62, D)], mix(C["iron"], PAPER, 0.25))   # its flange
    s.poly([P(X - w / 2 + 1, 12 + h, D), P(X + w / 2 - 1, 12 + h, D), P(X + w / 2 - 1, 12 + h + 7, D), P(X - w / 2 + 1, 12 + h + 7, D)], C["wood_lit"])   # the wooden lid
    s.line([P(X - w / 2 - 2, 12 + h + 9, D), P(X + w / 2 + 10, 12 + h + 12, D)], mix(C["wood_lit"], PAPER, 0.3), 2.2)   # the paddle across it
    outline(s, body, 0.6, 0.6)
    outline(s, st, 0.5, 0.5)


def saltjar(s):
    t = THINGS["saltjar"]
    jar(s, t["X"], t["D"], t["w"], t["h"], C["bizen"], lid=C["wood_lit"], lit=C["bizen_lit"], y0=SHELF["y"])


def plumjar(s):
    t = THINGS["plumjar"]
    jar(s, t["X"], t["D"], t["w"], t["h"], mix(C["clay"], PAPER, 0.2), lid=mix(PAPER, PAINT["naples"], 0.3), y0=SHELF["y"])
    X, D, h = t["X"], t["D"], t["h"] + SHELF["y"]
    s.line([P(X - 12, h - 4, D), P(X + 12, h - 4, D)], C["straw_sh"], 1.0)        # the paper over its mouth, tied


def pickletub(s):
    """The pickle tub (pickled radish), a hooped wooden tub on the ground, its drop-lid and the pressing stone."""
    t = THINGS["pickletub"]
    X, D, w, h = t["X"], t["D"], t["w"], t["h"]
    body = [P(X - w / 2, 0, D), P(X + w / 2, 0, D), P(X + w / 2 + 2, h, D), P(X - w / 2 - 2, h, D)]
    s.poly(body, C["wood"])
    s.poly([P(X + w / 4, 0, D), P(X + w / 2, 0, D), P(X + w / 2 + 2, h, D), P(X + w / 4, h, D)], shade_of(C["wood"], 0.3), 0.6)
    for yy in (6, h - 6):
        s.line([P(X - w / 2 - 1, yy, D), P(X + w / 2 + 1, yy, D)], C["straw_sh"], 1.2)
    s.ellipse(*P(X, h, D + 6), (w / 2 + 2) * k_at(D), 2.6, C["wood_lit"])
    s.ellipse(*P(X + 2, h + 6, D + 6), 5.5, 3.6, C["stone_sh"])
    s.ellipse(*P(X + 1, h + 7, D + 6), 4.0, 2.4, C["stone"])
    outline(s, body, 0.6, 0.6)


def cloth(s, bundle=False):
    """A cloth on the bench: folded square (white cotton, indigo-edged) or knotted into a bundle round rice balls."""
    t = THINGS["cloth"]
    X, D = t["X"], t["D"]
    y = BENCH["h"]
    if not bundle:
        top = [P(X - 17, y + 6, D + 4), P(X + 17, y + 6, D + 4), P(X + 17, y + 6, D + 26), P(X - 17, y + 6, D + 26)]
        side = [P(X - 17, y, D + 4), P(X + 17, y, D + 4), P(X + 17, y + 6, D + 4), P(X - 17, y + 6, D + 4)]
        s.poly(side, C["cloth_sh"])
        s.poly(top, C["cloth"])
        s.line([P(X - 17, y + 6.2, D + 8), P(X + 17, y + 6.2, D + 8)], C["indigo_lit"], 1.0, 0.9)
        outline(s, side + [top[2], top[3]], 0.5, 0.55)
    else:
        cx, cy = P(X, y + 12, D + 14)
        k = k_at(D)
        body = [(cx + 18 * k * math.cos(a) * (1 + 0.08 * math.sin(3 * a)), cy + 13 * k * math.sin(a) * 0.9) for a in np.linspace(0, 2 * math.pi, 24, endpoint=False)]
        s.poly(body, C["cloth"])
        s.poly(body[3:12], C["cloth_sh"], 0.6)
        s.poly([(cx - 4, cy - 12 * k), (cx + 4, cy - 12 * k), (cx + 7, cy - 18 * k), (cx - 7, cy - 18 * k)], C["cloth"])   # the knot
        s.line([(cx - 9, cy - 13 * k), (cx + 9, cy - 13 * k)], C["indigo_lit"], 1.0)
        outline(s, body, 0.5, 0.55)


def pan(s):
    """The roasting pan (horoku), unglazed, shallow, with its hollow handle: stood on its rim against the school's side
    wall at the yard's mouth, drying in the sun (seen face on: its hollow toward us)."""
    t = THINGS["pan"]
    X, D, w = t["X"], t["D"], t["w"]
    cx, cy = P(X, w / 2, D)
    k = k_at(D)
    rx, ry = w / 2 * k, w / 2 * k
    s.line([(cx + rx * 0.6, cy - ry * 0.8), (cx + rx * 1.15, cy - ry * 1.5)], C["clay"], 2.6)        # the handle
    s.ellipse(cx, cy, rx, ry, C["clay"])
    s.ellipse(cx + 0.6, cy + 0.6, rx - 2.0, ry - 2.0, mix(C["clay"], C["inside"], 0.25))           # its hollow
    s.ellipse(cx - rx * 0.25, cy - ry * 0.25, rx * 0.35, ry * 0.3, mix(C["clay"], PAPER, 0.25), 0.6)
    outline(s, [(cx + rx * math.cos(a_), cy + ry * math.sin(a_)) for a_ in np.linspace(0, 2 * math.pi, 22, endpoint=False)], 0.5, 0.6)


def mortar(s):
    """The Bizen mortar on the ground by the well: reddish-brown, wide-mouthed, its combed inside."""
    t = THINGS["mortar"]
    X, D, w, h = t["X"], t["D"], t["w"], t["h"]
    body = [P(X - w / 2, h, D), P(X + w / 2, h, D), P(X + w / 4, 0, D), P(X - w / 4, 0, D)]
    s.poly(body, C["bizen"])
    s.poly([P(X + w / 8, h, D), P(X + w / 2, h, D), P(X + w / 4, 0, D), P(X + w / 16, 0, D)], shade_of(C["bizen"], 0.3), 0.6)
    s.ellipse(*P(X, h, D + 8), w / 2 * k_at(D), 3.2, C["bizen_lit"])
    s.ellipse(*P(X, h - 1, D + 8), w / 2 * k_at(D) - 2.4, 2.0, mix(C["bizen"], LINE, 0.25))
    outline(s, body, 0.5, 0.6)


def kitchendoor(s, open_=False):
    """The kitchen door in the lean-to's front: a board door in its frame, shut; or slid open to the left over the
    boards (the doorway dark, the stove's coal beyond)."""
    xa, xb = KDOOR
    d = YARD_BACK - 1
    fr = [P(xa - 6, 0, d), P(xb + 6, 0, d), P(xb + 6, 182, d), P(xa - 6, 182, d)]
    if not open_:
        door = [P(xa, 0, d), P(xb, 0, d), P(xb, 176, d), P(xa, 176, d)]
        s.poly(door, C["wood"])
        for k in range(1, 5):
            xx = xa + (xb - xa) * k / 5
            s.line([P(xx, 2, d), P(xx, 174, d)], C["wood_dark"], 0.7, 0.6)
        s.line([P(xa, 60, d), P(xb, 60, d)], C["wood_dark"], 1.2, 0.8)
        s.line([P(xa, 130, d), P(xb, 130, d)], C["wood_dark"], 1.2, 0.8)
        s.ellipse(*P(xa + 10, 92, d), 1.4, 1.4, C["iron"])
        outline(s, door, 0.6, 0.6)
    else:
        door = [P(xa - 70, 0, d - 4), P(xb - 70, 0, d - 4), P(xb - 70, 176, d - 4), P(xa - 70, 176, d - 4)]
        s.poly(door, C["wood"])
        for k in range(1, 5):
            xx = xa - 70 + (xb - xa) * k / 5
            s.line([P(xx, 2, d - 4), P(xx, 174, d - 4)], C["wood_dark"], 0.7, 0.6)
        outline(s, door, 0.6, 0.6)
    for (a, b) in ((fr[0], fr[3]), (fr[1], fr[2])):
        s.line([a, b], C["wood_dark"], 2.0)
    s.line([fr[3], fr[2]], C["wood_dark"], 2.4)


# ---------------------------------------------------------------- O-Tane's house, the hut, the gate, the lane
def tane_house(s):
    """O-Tane's house front: a weaver's house: a fine lattice across the front room's window, the doorway at the left
    by the side yard (its noren is a cut-out: it stirs), the low attic over it, a narrow bench under the lattice."""
    x0, x1 = TANE
    s.poly(front_poly(x0, x1, 0, EAVE1 + 4), C["wood"])
    door = (x0 + 10, x0 + 92)
    s.poly(front_poly(door[0], door[1], 0, 186), C["inside"])          # the doorway (the noren hangs in it)
    s.poly(front_poly(door[0], door[1], 0, 6, DF + 30), mix(C["inside"], C["street"], 0.35))
    s.poly(front_poly(door[0] - 8, door[0], 0, 214), C["wood_dark"])
    s.poly(front_poly(door[1], door[1] + 8, 0, 214), C["wood_dark"])
    s.poly(front_poly(door[0] - 8, door[1] + 8, 186, 196), C["wood_dark"])
    # the lattice: fine dark slats close together, over a pale paper window behind
    la = (door[1] + 14, x1 - 8)
    s.poly(front_poly(la[0], la[1], 40, 200), mix(PAPER, C["inside"], 0.35))
    n = int((la[1] - la[0]) / 6.5)
    for i in range(n + 1):
        xx = la[0] + (la[1] - la[0]) * i / n
        s.line([P(xx, 40, DF - 4), P(xx, 200, DF - 4)], C["wood_dark"], 1.5, 0.95)
    s.line([P(la[0], 40, DF - 4), P(la[1], 40, DF - 4)], C["wood_dark"], 2.2)
    s.line([P(la[0], 200, DF - 4), P(la[1], 200, DF - 4)], C["wood_dark"], 2.2)
    outline(s, front_poly(la[0], la[1], 40, 200, DF - 4), 0.6, 0.5)
    # the narrow bench below the lattice (a folding bench, let down by day)
    bn = [P(la[0] + 4, 36, DF - 36), P(la[1] - 4, 36, DF - 36), P(la[1] - 4, 36, DF - 4), P(la[0] + 4, 36, DF - 4)]
    s.poly(bn, C["wood_lit"])
    s.line([P(la[0] + 4, 30, DF - 36), P(la[1] - 4, 30, DF - 36)], C["wood_dark"], 1.6)
    for xl in (la[0] + 10, la[1] - 14):
        s.line([P(xl, 0, DF - 32), P(xl, 30, DF - 32)], C["wood_dark"], 1.6)
    outline(s, bn, 0.5, 0.5)
    outline(s, front_poly(x0, x1, 0, EAVE1), 0.8, 0.5)
    pent_roof(s, x0, x1)
    townhouse_upper(s, x0, x1)


def noren(s, x0, x1, top, bottom, d, slits=2, tone=None):
    """An indigo shop curtain hanging in a doorway: two or three panels, a white plain band at the top."""
    tone = C["indigo"] if tone is None else tone
    w = (x1 - x0) / (slits + 1)
    for i in range(slits + 1):
        xa, xb = x0 + i * w + 1, x0 + (i + 1) * w - 1
        p = [P(xa, top, d), P(xb, top, d), P(xb, bottom, d), P(xa, bottom, d)]
        s.poly(p, tone)
        s.poly([P(xa, top, d), P(xb, top, d), P(xb, top - 10, d), P(xa, top - 10, d)], mix(tone, C["indigo_lit"], 0.5))
        outline(s, p, 0.6, 0.6)
    s.line([P(x0 - 4, top + 2, d), P(x1 + 4, top + 2, d)], C["wood_dark"], 1.6)


def tane_noren(s):
    door = (TANE[0] + 10, TANE[0] + 92)
    noren(s, door[0], door[1], 184, 104, DF - 6, slits=1)


def cotton_noren(s):
    """The cotton office's long noren across its doorway: three panels of indigo, each with a plain white ring dyed on
    it (our own mark: no real house's crest)."""
    da, db = COTTON_DOOR
    tone = C["indigo"]
    n = 3
    for i in range(n):
        xa = da + (db - da) * i / n + 2
        xb = da + (db - da) * (i + 1) / n - 2
        p = front_poly(xa, xb, 248, 140, DF - 6)
        s.poly(p, tone)
        s.poly(front_poly(xa, xb, 248, 236, DF - 6), mix(tone, C["indigo_lit"], 0.5))
        outline(s, p, 0.6, 0.6)
        if i == 1:
            cx, cy = P((xa + xb) / 2, 196, DF - 6)
            s.poly([(cx, cy - 7), (cx + 5, cy), (cx, cy + 7), (cx - 5, cy)], PAPER, 0.9)
            s.poly([(cx, cy - 3.5), (cx + 2.5, cy), (cx, cy + 3.5), (cx - 2.5, cy)], tone)
    s.line([P(da - 6, 250, DF - 6), P(db + 6, 250, DF - 6)], C["wood_dark"], 1.6)


def hut(s):
    """Tobei's hut by the ward gate: a little board hut under a shingled pent roof, its front a shutter propped up
    over a counter (a jar of sweets on it), straw sandals hung in pairs from the eave, the clappers on a peg on the
    post, his stool before it. Its front stands at the street's edge (D DF - 30)."""
    x0, x1 = HUT
    d = DF - 30
    body = [P(x0, 0, d), P(x1, 0, d), P(x1, 200, d), P(x0, 200, d)]
    s.poly(body, C["wood_old"])
    for k in range(1, 9):
        xx = x0 + (x1 - x0) * k / 9
        s.line([P(xx, 0, d), P(xx, 200, d)], C["wood_dark"], 0.7, 0.4)
    # the counter opening and the propped shutter over it
    ca, cb = x0 + 16, x1 - 18
    s.poly([P(ca, 82, d), P(cb, 82, d), P(cb, 170, d), P(ca, 170, d)], C["inside"])
    s.poly([P(ca - 4, 76, d - 22), P(cb + 4, 76, d - 22), P(cb + 4, 84, d - 2), P(ca - 4, 84, d - 2)], C["wood_lit"])   # the counter board
    shut = [P(ca - 2, 172, d), P(cb + 2, 172, d), P(cb + 2, 186, d - 48), P(ca - 2, 186, d - 48)]
    s.poly(shut, C["wood"])
    outline(s, shut, 0.6, 0.55)
    s.line([P(cb - 6, 84, d - 18), P(cb - 6, 182, d - 44)], C["wood_dark"], 1.2)          # the prop
    # the jar of sweets on the counter
    jx, jd = ca + 22, d - 12
    jar(s, jx, jd, 22, 24, mix(PAPER, PAINT["cerulean"], 0.15), lid=C["wood_lit"])
    for k in range(5):
        s.ellipse(*P(jx - 6 + k * 3, 90 + (k % 2) * 4, jd - 2), 1.6, 1.6, [PAINT["lake"], PAINT["naples"], PAPER, PAINT["veronese"]][k % 4], 0.85)
    # straw sandals hung in pairs along the shutter's edge: each pair two oval soles side by side, a dark strap on each
    for k in range(4):
        xx = ca + 10 + k * (cb - ca - 20) / 3
        top = P(xx, 170, d - 46)
        s.line([top, (top[0], top[1] + 5)], C["straw_sh"], 0.8)
        for j in (-2.4, 2.4):
            cx_, cy_ = top[0] + j, top[1] + 12
            s.ellipse(cx_, cy_, 2.1, 6.0, C["straw"])
            s.line([(cx_, cy_ - 4), (cx_ - 1.4, cy_ - 1), (cx_ + 1.4, cy_ - 1)], C["straw_sh"], 0.8)
            s.ellipse(cx_, cy_, 2.1, 6.0, LINE, 0.0)
    # the clappers on a peg on the left post
    cx, cy = P(x0 + 6, 120, d - 2)
    s.line([(cx, cy), (cx + 3, cy)], C["wood_dark"], 1.4)
    for j in (0, 3.2):
        s.poly([(cx + 1 + j, cy + 2), (cx + 3.2 + j, cy + 2), (cx + 3.2 + j, cy + 22), (cx + 1 + j, cy + 22)], mix(C["wood_lit"], PAPER, 0.25))
        outline(s, [(cx + 1 + j, cy + 2), (cx + 3.2 + j, cy + 2), (cx + 3.2 + j, cy + 22), (cx + 1 + j, cy + 22)], 0.4, 0.6)
    s.line([(cx + 2, cy), (cx + 2, cy + 3), (cx + 5.4, cy + 3)], C["straw_sh"], 0.7)
    # the pent roof, shingled with stones, and the hut's roof behind
    roof_band(s, x0, x1, d, 206, 40, 236, d + 30, mix(C["wood_old"], C["tile"], 0.5), mix(C["wood_old"], PAPER, 0.25), lift=0.8)
    outline(s, body, 0.8, 0.55)
    # his stool, before the hut at the right
    sx, sd = x1 - 30, d - 60
    seat = [P(sx - 14, 38, sd - 12), P(sx + 14, 38, sd - 12), P(sx + 14, 38, sd + 12), P(sx - 14, 38, sd + 12)]
    for xl in (sx - 10, sx + 8):
        s.line([P(xl, 0, sd - 8), P(xl, 34, sd - 8)], C["wood_dark"], 1.6)
    s.poly(seat, C["wood_lit"])
    s.poly([P(sx - 14, 33, sd - 12), P(sx + 14, 33, sd - 12), P(sx + 14, 38, sd - 12), P(sx - 14, 38, sd - 12)], C["wood"])
    outline(s, seat, 0.5, 0.55)


def lane(s):
    """The lane north, seen through the gate (backdrop): its packed earth going back, the houses on its east side
    showing us their gable ends and plain plastered side walls, one behind another, paler as they go."""
    x0, x1 = LANE
    d0, d1 = DF - 20, DF + 2600
    s.poly([P(x0, 0, d0), P(x1, 0, d0), P(x1, 0, d1), P(x0, 0, d1)], C["street"])
    s.poly([P(x0 + 50, 0, d0), P(x1 - 40, 0, d0), P(x1 - 40, 0, d1), P(x0 + 50, 0, d1)], C["street_lit"], 0.4)
    rng = np.random.default_rng(36)
    d = d0 + 20
    houses = []
    while d < d1:
        w = rng.uniform(560, 760)
        houses.append((d, min(d1, d + w)))
        d += w + rng.uniform(20, 60)
    for (a0, a1) in houses[::-1]:                         # far first
        t = min(1.0, (a0 - d0) / 2600.0)
        wall_c = mix(mix(C["plaster"], C["plaster_sh"], 0.92), PAPER, 0.18 * t)                 # they face west: in shade at noon
        board_c = mix(C["wood_old"], PAPER, 0.15 + 0.3 * t)
        roof_c = mix(C["tile"], PAPER, 0.1 + 0.35 * t)
        # the side wall: boards below, plaster above, up to the eave at 400, then the gable to the ridge at 560
        mid = (a0 + a1) / 2
        wall = [P(x1, 0, a0), P(x1, 0, a1), P(x1, 400, a1), P(x1, 560, mid), P(x1, 400, a0)]
        if STYLE["wc"]:                                  # (round twenty-three) the noon sun grazes these west faces: pale and warm
            lit_c = lerp(thin(mix(C["plaster"], PAINT["naples"], 0.12), 0.25), wall_c, 0.45)
            s.poly(wall, lit_c, c1=thin(lerp(lit_c, wall_c, 0.6), 0.05), g=(P(x1, 560, mid), P(x1, 0, mid)))
            s.poly([P(x1, 400, a0), P(x1, 400, a1), P(x1, 560, mid)], thin(PAINT["cerulean"], 0.62), alpha=0.22)      # the gable sees the sky
        else:
            s.poly(wall, wall_c)
        s.poly([P(x1, 0, a0), P(x1, 0, a1), P(x1, 150, a1), P(x1, 150, a0)], board_c)
        if STYLE["wc"]:
            s.line([P(x1, 400, a0), P(x1, 400, a1)], mix(C["wood_dark"], PAPER, 0.25 + 0.4 * t), 1.0, 0.55)              # the wall plate at the eave
            for k_ in range(1, 4):                                                                                    # posts showing in the plaster
                dd = a0 + (a1 - a0) * k_ / 4
                s.line([P(x1, 150, dd), P(x1, 400, dd)], mix(C["wood"], PAPER, 0.3 + 0.4 * t), 0.8, 0.35)
            s.poly([P(x1, 470, mid - 22), P(x1, 470, mid + 22), P(x1, 500, mid + 22), P(x1, 500, mid - 22)], mix(C["inside"], PAPER, 0.25 + 0.4 * t))   # a vent high in the gable
        # the roof's verge along the gable, and the roof itself beyond it (seen over the edge)
        s.line([P(x1 + 8, 396, a0 - 30), P(x1 + 8, 566, mid), P(x1 + 8, 396, a1 + 30)], roof_c, 3.0)
        outline(s, wall, 0.5, 0.35 + 0.2 * (1 - t))


GATE_D = DF - 24


def gate(s, shut=False):
    """The ward gate across the lane's mouth (a cut-out): two square posts, a tie-beam, a little gabled roof of tiles
    over it, the two door leaves standing open against the posts by day (shut: across the lane, for the night)."""
    x0, x1 = GATE
    d = GATE_D
    h, beam = 252.0, 226.0
    for xp in (x0, x1 - 14):
        p = [P(xp, 0, d), P(xp + 14, 0, d), P(xp + 14, h, d), P(xp, h, d)]
        s.poly(p, C["wood_dark"])
        s.poly([P(xp + 9, 0, d), P(xp + 14, 0, d), P(xp + 14, h, d), P(xp + 9, h, d)], C["wood"], 0.8)
        outline(s, p, 0.7, 0.6)
    tb = [P(x0 - 18, beam, d), P(x1 + 18, beam, d), P(x1 + 18, beam + 14, d), P(x0 - 18, beam + 14, d)]
    s.poly(tb, C["wood_dark"])
    outline(s, tb, 0.6, 0.6)
    # the little roof: gabled, seen from the front (its eave across, its two slopes)
    a, b = P(x0 - 40, h - 4, d - 30), P(x1 + 40, h - 4, d - 30)
    apex = P((x0 + x1) / 2, h + 46, d)
    roof = [a, b, P(x1 + 40, h - 4, d + 30), P((x0 + x1) / 2, h + 46, d + 20), P(x0 - 40, h - 4, d + 30)]
    s.poly([a, b, apex], C["tile"])
    s.poly([apex, b, (b[0] - (b[0] - apex[0]) * 0.1, b[1])], C["tile_lit"], 0.5)
    s.line([a, b], C["tile_edge"], 1.2, 0.85)
    s.line([a, apex, b], C["tile_edge"], 1.0, 0.7)
    s.poly([(a[0] + 6, a[1] + 1), (b[0] - 6, b[1] + 1), (apex[0], apex[1] + 8)], mix(PAPER, PAINT["cerulean"], 0.3), 0.0)
    outline(s, [a, b, apex], 0.7, 0.6)
    s.ellipse(*apex, 2.0, 2.0, C["tile_deep"])
    # the door leaves
    if not shut:
        for (xp, sgn) in ((x0 + 14, 1), (x1 - 14, -1)):
            leaf = [P(xp, 6, d), P(xp, 6, d + 92), P(xp, beam - 6, d + 92), P(xp, beam - 6, d)]
            leaf = [P(xp + sgn * 6, 6, d + 4), P(xp + sgn * 38, 6, d + 86), P(xp + sgn * 38, beam - 8, d + 86), P(xp + sgn * 6, beam - 8, d + 4)]
            s.poly(leaf, C["wood"])
            for k in range(1, 4):
                t = k / 4
                s.line([(leaf[0][0] + (leaf[1][0] - leaf[0][0]) * t, leaf[0][1] + (leaf[1][1] - leaf[0][1]) * t),
                        (leaf[3][0] + (leaf[2][0] - leaf[3][0]) * t, leaf[3][1] + (leaf[2][1] - leaf[3][1]) * t)], C["wood_dark"], 0.8, 0.7)
            outline(s, leaf, 0.6, 0.6)
    else:
        leaf = [P(x0 + 14, 6, d + 2), P(x1 - 14, 6, d + 2), P(x1 - 14, beam - 8, d + 2), P(x0 + 14, beam - 8, d + 2)]
        s.poly(leaf, C["wood"])
        for k in range(1, 7):
            xx = x0 + 14 + (x1 - x0 - 28) * k / 7
            s.line([P(xx, 8, d + 2), P(xx, beam - 10, d + 2)], C["wood_dark"], 0.8, 0.7)
        s.line([P((x0 + x1) / 2, 6, d + 2), P((x0 + x1) / 2, beam - 8, d + 2)], C["wood_dark"], 1.6)
        s.line([P(x0 + 14, 110, d + 2), P(x1 - 14, 110, d + 2)], C["wood_dark"], 2.4)
        outline(s, leaf, 0.6, 0.6)


def right_house(s):
    """The house east of the lane, at the right edge: the start of the next front."""
    x0, x1 = LANE[1], 1100.0
    s.poly(front_poly(x0, x1, 0, EAVE1 + 4), C["wood"])
    s.poly(front_poly(x0 + 16, x1, 40, 200, DF - 2), mix(PAPER, C["inside"], 0.35))
    for i in range(30):
        xx = x0 + 16 + i * 6.5
        s.line([P(xx, 40, DF - 4), P(xx, 200, DF - 4)], C["wood_dark"], 1.5, 0.95)
    pent_roof(s, x0, x1)
    townhouse_upper(s, x0, x1)


# ---------------------------------------------------------------- the street (round twenty-three: the ground in depth)
TRACKS = [(1000.0, 75.0, 0.55), (1185.0, 100.0, 0.80), (1395.0, 85.0, 0.60)]   # a worn track's middle (D), half width, how worn
TREE = dict(X=-470.0, D=470.0, crown=(900.0, 1400.0))          # the big tree behind us on the left (out of the picture): trunk, crown


def street(pic, seed=37):
    """The highway: packed earth in the sun, paler toward the fronts and deeper and warmer toward us; three tracks worn
    smooth and pale by feet and hooves running along it, rougher earth and loose stones between them and at its edges;
    blotches and grit that lie on it in centimetres (so they shrink with distance). -> the street's mask."""
    X, D, below = floor()
    x, y = grid(SHAPE)
    m = ((y >= row_D(GUT) - 1) * below).astype(F32)
    t = np.clip((D - 846.0) / (GUT - 846.0), 0, 1)
    near_c = thin(mix(PAINT["ochre"], PAINT["sienna"], 0.30), 0.27)
    mid_c = thin(mix(PAINT["ochre"], PAINT["naples"], 0.10), 0.46)
    far_c = thin(mix(PAINT["ochre"], PAINT["naples"], 0.20), 0.50)
    earth = ramp(t ** 0.8, [(0.0, tuple(near_c)), (0.40, tuple(mid_c)), (1.0, tuple(far_c))])
    earth *= 1 + ((street_noise(X, D, (170, 70), seed) - 0.5) * 0.14 + (street_noise(X, D, (34, 16), seed + 1) - 0.5) * 0.12)[..., None]
    warm = (street_noise(X, D, (420, 160), seed + 2) - 0.5) * 0.06
    earth[..., 0] += warm
    earth[..., 2] -= warm
    wander = (street_noise(X, D, (900, 300), seed + 3, 2) - 0.5) * 70.0
    worn = np.clip(sum(w_ * np.exp(-((D + wander - c_) / hw) ** 2) for c_, hw, w_ in TRACKS), 0, 1)
    smooth_c = thin(mix(PAINT["ochre"], PAINT["naples"], 0.35), 0.74)
    earth = lerp(earth, lerp(earth, smooth_c[None, None, :], 0.66), (worn * 0.9)[..., None])
    # dust drawn out along the tracks by the traffic: pale streaks running along the highway
    streak = step(0.58, 0.80, street_noise(X, D, (260, 9), seed + 6, 3)) * worn
    earth = lerp(earth, thin(PAINT["naples"], 0.70)[None, None, :], (streak * 0.35)[..., None])
    rough = (1 - worn) * (street_noise(X, D, (11, 6), seed + 4) - 0.5) * 0.30 + (1 - worn) * (street_noise(X, D, (48, 22), seed + 5) - 0.5) * 0.12
    earth *= (1 + rough[..., None])
    # where a track's worn edge meets the rough earth, a low ridge of loose earth: a breath darker
    for c_, hw, w_ in TRACKS:
        for sgn in (-1, 1):
            ridge_ = np.exp(-((D + wander - c_ - sgn * hw * 1.05) / (hw * 0.18)) ** 2) * w_
            earth *= (1 - (ridge_ * 0.07)[..., None])
    # where the lane's traffic turns in at the ward gate, the earth is cut up and rougher
    turn = np.clip(1.0 - np.hypot((X - 560.0) / 260.0, (D - 1480.0) / 120.0), 0, 1)
    earth *= (1 - (turn * (street_noise(X, D, (14, 8), seed + 7) - 0.35) * 0.22)[..., None])
    # the near street deeper and warmer still (what is nearest the lens holds the warm darks of the ground)
    near_b = np.clip((y - 540.0) / 60.0, 0, 1) ** 1.4
    earth = lerp(earth, earth * thin(mix(PAINT["sienna"], PAINT["prussian"], 0.25), 0.55)[None, None, :] * 1.04, (near_b * 0.30)[..., None])
    over(pic, np.clip(earth, 0, 1).astype(F32), m)
    return m, worn


def street_marks(pic, worn, seed=38):
    """What lies on the street, through the camera: stones at a true density (more at the edges, few in the worn tracks),
    footprints (straw sandals and clogs along the highway, a trail into the side yard's mouth and one to the school's step
    stone, straw horseshoes along the middle track), each a small hollow: its near wall in its own shade, its far wall lit."""
    L = Wet(SHAPE)
    rng = np.random.default_rng(seed)
    dark = thin(mix(PAINT["sienna"], PAINT["prussian"], 0.45), 0.30)
    lit = thin(PAINT["naples"], 0.55)
    zone = np.zeros(SHAPE, F32)
    zone[456:600, :] = 1.0
    wn = lambda X_, D_: float(worn[int(np.clip(ground_pt(X_, D_)[1], 0, 599)), int(np.clip(ground_pt(X_, D_)[0], 0, 799))])
    # ---- stones: big and few near us, small and many far off (depth.scatter), fewer where feet have worn the earth
    for (per, size, sd) in ((0.9, (3.0, 7.0), 1), (5.0, (1.0, 2.6), 2)):
        for (px_, py_, k, r) in DPT.scatter(ground_pt, px_per_cm, (-1100.0, 900.0, 860.0, 1600.0), per, seed + sd, size=size, zone=zone):
            X_ = (px_ - VX) * (EYE * FOC / (py_ - HZ)) / FOC
            D_ = EYE * FOC / max(py_ - HZ, 1)
            if rng.random() < wn(X_, D_) * 0.85:
                continue
            cm = size[0] + (size[1] - size[0]) * r
            rx = max(0.5, cm * k * 0.75)
            ry = max(0.35, rx * (py_ - HZ) / FOC * 1.1)
            L.ellipse(px_ + rx * 0.25, py_ - ry * 0.8, rx * 1.0, ry * 0.8, dark, alpha=0.26)        # its shadow, away from us
            L.ellipse(px_, py_, rx, ry, thin(mix(PAINT["prussian"], PAINT["ochre"], 0.35), 0.45 + 0.2 * r), thin(mix(PAINT["prussian"], PAINT["sienna"], 0.3), 0.30))
            L.ellipse(px_ - rx * 0.25, py_ - ry * 0.35, rx * 0.5, ry * 0.4, lit, alpha=0.7)

    def print_(X_, D_, ang, kind, s_=1.0):
        """One footprint at a place on the street, the foot pointing `ang` (radians, 0 along +X)."""
        ca, sa = math.cos(ang), math.sin(ang)
        if kind == "geta":                                    # two teeth, across the foot
            for off in (-4.5 * s_, 4.5 * s_):
                cx_, cz_ = X_ + ca * off, D_ + sa * off
                pts = [ground_pt(cx_ + (-sa) * w_ + ca * l_, cz_ + ca * w_ + sa * l_) for (w_, l_) in ((-5 * s_, -1.2), (5 * s_, -1.2), (5 * s_, 1.2), (-5 * s_, 1.2))]
                L.poly(pts, dark, alpha=0.62)
        else:                                                 # a sole (straw sandal), or a straw horseshoe's round print
            ln, wd = (12.0 * s_, 4.6 * s_) if kind == "sole" else (6.5, 6.0)
            ring = [ground_pt(X_ + ca * ln * math.cos(t_) - sa * wd * math.sin(t_), D_ + sa * ln * math.cos(t_) + ca * wd * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 14)[:-1]]
            L.poly(ring, dark, alpha=0.42 if kind == "sole" else 0.50)
            near_in = [ground_pt(X_ + ca * ln * 0.9 * math.cos(t_) - sa * wd * 0.6 * math.sin(t_), D_ + sa * ln * 0.9 * math.cos(t_) + ca * wd * 0.6 * math.sin(t_)) for t_ in np.linspace(math.pi * 1.1, math.pi * 1.9, 6)]
            far_lip = [ground_pt(X_ + ca * ln * math.cos(t_) - sa * wd * math.sin(t_), D_ + sa * ln * math.cos(t_) + ca * wd * math.sin(t_)) for t_ in np.linspace(math.pi * 0.1, math.pi * 0.9, 6)]
            L.line(near_in, thin(mix(PAINT["prussian"], PAINT["sienna"], 0.4), 0.25), 0.8, 0.5)
            L.line(far_lip, lit, 0.8, 0.55)

    def trail(p0, p1, kind, stride=62.0, gait=9.0, s_=1.0, keep=1.0):
        (x0_, d0_), (x1_, d1_) = p0, p1
        n = int(math.hypot(x1_ - x0_, d1_ - d0_) / stride * 2)
        ang = math.atan2(d1_ - d0_, x1_ - x0_)
        for i in range(n):
            if rng.random() > keep:
                continue
            t_ = i / max(n - 1, 1)
            side = gait * (1 if i % 2 else -1)
            X_ = x0_ + (x1_ - x0_) * t_ - math.sin(ang) * side + rng.normal(0, 2)
            D_ = d0_ + (d1_ - d0_) * t_ + math.cos(ang) * side + rng.normal(0, 2)
            print_(X_, D_, ang + rng.normal(0, 0.12), kind, s_)
    # the traffic of the highway, along its tracks, both ways; and older prints, half trodden out
    for (c_, hw, w_) in TRACKS:
        for j in range(5):
            dd = c_ + rng.uniform(-hw, hw) * 0.8
            xa = rng.uniform(-1300, 300)
            way = 1 if rng.random() < 0.5 else -1
            trail((xa, dd), (xa + way * rng.uniform(350, 700), dd + rng.normal(0, 30)), "geta" if rng.random() < 0.45 else "sole", keep=0.75)
    for j in range(26):                                   # near us: odd prints, half trodden out
        X_, D_ = rng.uniform(-500, 420), rng.uniform(860, 1060)
        print_(X_, D_, rng.uniform(-0.4, 0.4) + (math.pi if rng.random() < 0.5 else 0.0), "sole" if rng.random() < 0.6 else "geta")
    trail((-1000.0, 1185.0), (600.0, 1205.0), "hoof", stride=86.0, gait=14.0, keep=0.9)                      # a packhorse, along the middle
    trail((-90.0, 880.0), (-6.0, 1585.0), "sole", stride=66.0, gait=9.0)                                     # into the side yard's mouth
    trail((260.0, 940.0), (-205.0, 1570.0), "geta", stride=48.0, gait=7.0, s_=0.72)                          # a child's clogs, to the step stone
    trail((-900.0, 1430.0), (-560.0, 1580.0), "sole", stride=64.0, gait=9.0, keep=0.8)                      # to the cotton office's door
    c, a = L.done()
    lay = Canvas(SHAPE)
    lay.c, lay.a = (c * a[..., None]).astype(F32), a.astype(F32)
    lay.onto(pic)
    return lay


def drain(s):
    """The drain along the fronts, covered with planks (each a hand's span, laid across it, grey with weather, a joint
    between each two), a stone kerb on the street's side, flat stones over it at the doorways."""
    plank = thin(mix(PAINT["sienna"], PAINT["prussian"], 0.32), 0.38)
    joint = thin(mix(PAINT["sienna"], PAINT["prussian"], 0.55), 0.10)
    for (xa, xb) in ((-1400.0, LANE[0]), (LANE[1], 1300.0)):
        s.poly([P(xa, 1.5, GUT - 4), P(xb, 1.5, GUT - 4), P(xb, 1.5, GUT + 26), P(xa, 1.5, GUT + 26)], plank)
        X = xa
        rng = np.random.default_rng(int(xa) & 0xFFFF)
        while X < xb:
            s.line([P(X, 1.6, GUT - 4), P(X + rng.normal(0, 0.8), 1.6, GUT + 26)], joint, 0.6, 0.75)
            X += rng.uniform(21.0, 29.0)
        s.poly([P(xa, 0, GUT - 10), P(xb, 0, GUT - 10), P(xb, 2.5, GUT - 4), P(xa, 2.5, GUT - 4)], C["stone_lit"])        # the kerb
        s.line([P(xa, 0, GUT - 10), P(xb, 0, GUT - 10)], joint, 0.6, 0.5)
    for (xa, xb) in ((ROOM[1] - 76, ROOM[1] - 4), (TANE[0] + 8, TANE[0] + 96), (YARD[0] + 40, YARD[1] - 40), (HUT[0] + 20, HUT[1] - 20),
                     (COTTON_DOOR[0] + 10, COTTON_DOOR[1] - 10), (NOTE_DOOR[0], NOTE_DOOR[1])):
        st = [P(xa, 3, GUT - 6), P(xb, 3, GUT - 6), P(xb, 3, GUT + 26), P(xa, 3, GUT + 26)]
        s.poly(st, C["stone_lit"])
        outline(s, st, 0.5, 0.45)


def sprinkled(pic, seed=39, xc=262.0, dc=DF - 105.0, rx=150.0, rz=70.0):
    """Before O-Tane's door the earth is dark where she has sprinkled water against the dust (and before Tobei's hut,
    an hour ago, half dried): a cooler, deeper patch, its edge darker where it is drying, drops flung round it."""
    X, D, below = floor()
    u, v = (X - xc) / rx, (D - dc) / rz
    wob = (street_noise(X, D, (40, 20), seed) - 0.5) * 0.9
    r = np.sqrt(u * u + v * v) + wob
    m = np.clip((1.0 - r) * 6.0, 0, 1) * below * (D < GUT - 8)
    rim = np.clip(1.0 - np.abs(r - 0.92) * 9.0, 0, 1) * below * (D < GUT - 8)
    tint(pic, thin(mix(PAINT["prussian"], PAINT["sienna"], 0.35), 0.62), (m * 0.55).astype(F32))
    tint(pic, thin(mix(PAINT["prussian"], PAINT["sienna"], 0.4), 0.55), (rim * 0.25).astype(F32))
    L = Wet(SHAPE)
    rng = np.random.default_rng(seed)
    for i in range(70):
        a_ = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(1.0, 1.45)
        Xd, Dd = xc + rx * rr * math.cos(a_), dc + rz * rr * math.sin(a_)
        if Dd > GUT - 10:
            continue
        px_, py_ = ground_pt(Xd, Dd)
        k = px_per_cm(Xd, Dd)
        L.ellipse(px_, py_, max(0.5, 1.6 * k), max(0.4, 0.6 * k), thin(mix(PAINT["prussian"], PAINT["sienna"], 0.35), 0.45), alpha=0.6)
    c, a = L.done()
    over(pic, c, a)


def yard_sun(pic):
    """The lightest light of the play: the noon sun poured down into O-Tane's side yard, a slot of light between the
    shaded fronts: its floor (but for the strip in the school wall's shade) and the foot of the kitchen's front."""
    floor_ = mask_poly(SHAPE, [P(YARD[0] + 44, 0, DF - 2), P(YARD[1] - 2, 0, DF - 2), P(YARD[1] - 2, 0, YARD_BACK), P(YARD[0] + 44, 0, YARD_BACK)], soft=1.2)
    front = mask_poly(SHAPE, [P(YARD[0], 0, YARD_BACK - 1), P(YARD[1], 0, YARD_BACK - 1), P(YARD[1], 128, YARD_BACK - 1), P(YARD[0], 128, YARD_BACK - 1)], soft=0.8)
    glow(pic, thin(PAINT["naples"], 0.62), (floor_ * 0.62).astype(F32))
    glow(pic, thin(mix(PAINT["naples"], PAINT["ochre"], 0.3), 0.5), (front * 0.22).astype(F32))


def tree_shade(pic, seed=40):
    """The shade of a big tree behind us on the left, out of the picture (its crown 9 to 15 m up): it lies across the near
    left of the street, its edge in big scallops running in along the light, the sun coming through it in flecks.
    Thin where people walk. -> its mask."""
    X, D, below = floor()
    sx, sd = SUN_CAST
    ln_ = math.hypot(sx, sd)
    ux, uz = sx / ln_, sd / ln_
    rng = np.random.default_rng(seed)
    sl = slice(470, H)
    m = np.zeros((H - 470, W), F32)
    Uw, Vw = X[sl] * ux + D[sl] * uz, -X[sl] * uz + D[sl] * ux
    cx0, cz0 = TREE["X"], TREE["D"]
    for i in range(70):                                     # each mass of leaves throws an oval, lying along the light
        hgt = rng.uniform(*TREE["crown"])
        ox, oz = rng.normal(0, 175.0), rng.normal(0, 62.0)
        cxw, czw = cx0 + ox + sx * hgt, cz0 + oz + sd * hgt
        a_, b_ = rng.uniform(70.0, 150.0), rng.uniform(45.0, 95.0)
        e_ = ((Uw - (cxw * ux + czw * uz)) / a_) ** 2 + ((Vw - (-cxw * uz + czw * ux)) / b_) ** 2
        np.maximum(m, np.clip((1 - e_) * 3.0, 0, 1), out=m)
    fleck = step(0.60, 0.67, street_noise(X, D, (46, 34), seed + 2, 2))[sl]
    shade = np.zeros(SHAPE, F32)
    shade[sl] = np.clip(m * (1 - fleck * 0.92), 0, 1)
    shade = (blur(shade, 0.7) * below).astype(F32)
    return shade


def wall_shade(x0, x1, d, y_eave, proj, y_floor=0.0, slant=True):
    """The shade an eave lays on the wall under it at noon: from the eave down to where the sun gets under it
    (proj / 0.36 below the eave), across the wall's width. -> a picture polygon."""
    y_lo = max(y_floor, y_eave - proj / SUN_CAST[1])
    off = SUN_CAST[0] * (y_eave - y_lo) if slant else 0.0       # (the light from a little left: the shade's end leans right)
    return [P(x0, y_eave, d), P(x1, y_eave, d), P(x1, y_lo, d), P(x0 + off, y_lo, d)]


SHADES = {  # each backdrop layer: the walls under its eaves (x0, x1, the wall's D, the eave's height, how far it projects, how deep)
    "offices": [(COTTON[0], NOTE[1], DF, OFF_EAVE1 - 4, 75.0, 1.35), (COTTON[0], NOTE[1], DF + 12, OFF_EAVE2, 60.0, 1.0)],
    "school_upper": [(SCHOOL[0], SCHOOL[1], DF + 10, EAVE2, 50.0, 1.0)],
    "tane": [(TANE[0], TANE[1], DF, EAVE1 - 4, 70.0, 1.35), (TANE[0], TANE[1], DF + 10, EAVE2, 50.0, 1.0)],
    "right": [(LANE[1], 1300.0, DF, EAVE1 - 4, 70.0, 1.35), (LANE[1], 1300.0, DF + 10, EAVE2, 50.0, 1.0)],
    "hut": [(HUT[0], HUT[1], DF - 30, 202.0, 40.0, 1.25)],
    "yard": [(YARD[0], YARD[1], YARD_BACK, 212.0, 30.0, 1.15)],
    "kura": [(KURA["x"][0], KURA["x"][1], KURA["D"], KURA["h"] + 4, 40.0, 1.0)],
}


def shade_layer(name, lay):
    """Glaze the noon shade over a backdrop layer's walls (a cool thin wash, multiplied; warmer toward its foot, where the
    street's light is thrown up under the eave), in the layer itself, so that what stands in front stays in the sun."""
    if name not in SHADES:
        return lay
    c, a = lay.straight()
    m = np.zeros(SHAPE, F32)
    foot = np.zeros(SHAPE, F32)
    deep = np.zeros(SHAPE, F32)
    x, y = grid(SHAPE)
    for (x0, x1, d, ye, pj, dp) in SHADES[name]:
        poly = wall_shade(x0, x1, d, ye, pj)
        pm = mask_poly(SHAPE, poly, soft=0.5)
        np.maximum(m, pm, out=m)
        np.maximum(deep, pm * (dp - 1.0), out=deep)
        top, bot = poly[0][1], poly[2][1]
        np.maximum(foot, pm * np.clip((y - top) / max(bot - top, 1.0), 0, 1) ** 1.5, out=foot)
    if name == "yard":                                    # the yard's west wall (the school's side) faces east: all in shade
        m = np.maximum(m, mask_poly(SHAPE, [P(YARD[0], 0, DF), P(YARD[0], 0, YARD_BACK + 40), P(YARD[0], 380, YARD_BACK + 40), P(YARD[0], 380, DF)]))
        floor_strip = mask_poly(SHAPE, [P(YARD[0], 0, DF), P(YARD[0] + 42, 0, DF), P(YARD[0] + 42, 0, YARD_BACK), P(YARD[0], 0, YARD_BACK)], soft=0.8)
        m = np.maximum(m, floor_strip * 0.9)
    shaded = c * SHADE[None, None, :]
    shaded = lerp(shaded, shaded * SHADE[None, None, :] ** 0.5, np.clip(deep * 2.0, 0, 1)[..., None])        # deeper under a deep eave
    warmth = np.clip(foot * 0.75, 0, 1)[..., None]
    shaded = lerp(shaded, np.clip(shaded * 1.22 + np.array([0.07, 0.04, -0.01], F32), 0, 1), warmth)
    c = lerp(c, shaded, (m * (a > 0.01))[..., None])
    lay.c = (c * a[..., None]).astype(F32)
    return lay


def ground_shadows():
    """The short noon shadows of what stands in the street and the yard, each falling away from us and a little right,
    as picture polygons: (polygon, strength)."""
    sx, sd = SUN_CAST
    out = []

    def box(x0, x1, d0, d1, h, k=0.85):
        foot = [(x0, d0), (x1, d0), (x1, d1), (x0, d1)]
        top = [(x_ + sx * h, d_ + sd * h) for x_, d_ in foot]
        pts = foot + top
        out.append(([P(x_, 0.2, d_) for x_, d_ in convex(pts)], k))
    def post(x_, d_, w_, h, k=0.8):
        out.append(([P(x_ - w_ / 2, 0.2, d_), P(x_ + w_ / 2, 0.2, d_), P(x_ + w_ / 2 + sx * h, 0.2, d_ + sd * h), P(x_ - w_ / 2 + sx * h, 0.2, d_ + sd * h)], k))
    # the bales of cloth (their shadows go in under the cotton office's eave)
    for (X_, row, n) in BALES:
        d_ = DF - 30 - row * 46
        box(X_, X_ + 54, d_, d_ + 40, n * 30)
    # the hut, its stool's legs, the gate's posts
    box(HUT[0], HUT[1], DF - 30, DF - 4, 200.0, 0.75)
    sxs, sds = HUT[1] - 30, DF - 90
    for xl in (sxs - 10, sxs + 8):
        post(xl, sds - 8, 3.0, 36.0)
    box(sxs - 14, sxs + 14, sds - 12, sds + 12, 38.0, 0.6)
    for xp in (GATE[0], GATE[1] - 14):
        post(xp + 7, GATE_D + 7, 14.0, 252.0, 0.75)
    # the school's step stone; the well, its frame's posts, the rice pot, the pickle tub, the mortar (in the yard)
    box(ROOM[1] - 70, ROOM[1] - 6, DF - 52, DF - 42, 16.0, 0.7)
    W_ = WELL
    ring = [(W_["X"] + W_["r"] * math.cos(t_), W_["D"] + W_["r"] * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 16)[:-1]]
    pts = ring + [(x_ + sx * W_["h"], d_ + sd * W_["h"]) for x_, d_ in ring]
    out.append(([P(x_, 0.2, d_) for x_, d_ in convex(pts)], 0.85))
    for xp in (W_["X"] - W_["r"] - 1, W_["X"] + W_["r"] + 1):
        post(xp, W_["D"] + 2, 6.0, FRAME["h"], 0.7)
    for key in ("ricepot", "pickletub", "mortar"):
        t_ = THINGS[key]
        box(t_["X"] - t_["w"] / 2, t_["X"] + t_["w"] / 2, t_["D"] - t_["w"] / 3, t_["D"] + t_["w"] / 3, t_.get("h", 20.0) + (12.0 if key == "ricepot" else 0.0), 0.8)
    return out


def convex(pts):
    """The convex hull of ground places (x, d)."""
    pts = sorted(set((round(a, 2), round(b, 2)) for a, b in pts))
    if len(pts) < 3:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p_ in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p_) <= 0:
            lower.pop()
        lower.append(p_)
    for p_ in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p_) <= 0:
            upper.pop()
        upper.append(p_)
    return lower[:-1] + upper[:-1]


def shadows(pic, street_m):
    """The noon shadows on the ground: the short shadows of what stands there (glazes), and the big tree's dappled shade
    across the near left of the street. -> the shade mask (all of it)."""
    sh = np.zeros(SHAPE, F32)
    for i, (poly, k) in enumerate(ground_shadows()):
        np.maximum(sh, mask_poly(SHAPE, poly, soft=0.6, wobble=0.5, seed=60 + i) * k, out=sh)
    tint(pic, SHADE, np.clip(sh, 0, 1))
    x_, y_ = grid(SHAPE)
    tree = tree_shade(pic) * street_m * np.clip((430.0 - x_) / 90.0, 0, 1)
    tint(pic, SHADE, np.clip(tree * 0.70, 0, 1))
    # the foot of every front a little darker where it meets the ground (and the drain's planks' shadow line)
    x, y = grid(SHAPE)
    foot = np.exp(-((y - row_D(DF) - 0.5) / 1.4) ** 2) * (y > 300)
    tint(pic, SHADE, (foot * 0.5).astype(F32))
    return np.maximum(sh, tree)


# ---------------------------------------------------------------- the passes
def backdrop_sheets():
    """Everything of the near row (the backdrop's middle plane), far to near, on sheets: a list of (name, draw function)."""
    return [
        ("lane", lane), ("offices", offices), ("bales", bales),
        ("kura", kura), ("yard", yard), ("mortar", mortar), ("pan", pan), ("school_inside", school_inside), ("school_doorway", school_doorway),
        ("school_upper", school_upper), ("tane", tane_house), ("right", right_house), ("hut", hut), ("drain", drain),
    ]


def under(seed=SEED):
    """Pass one: the far plane (edo_town_far.py), the near row's fronts in washes with their noon shade, the street and
    its shadows. -> (picture, the crisp layers, info)"""
    import edo_town_far as FAR
    pic = FAR.paint_sky(seed)
    info = FAR.paint_far(pic, seed)
    info["sky_only"] = (1 - np.clip(info["hills"] + info["hill"] + info["keep"] + info["roofs"], 0, 1)).astype(F32)
    layers = {}
    near_row = np.zeros(SHAPE, F32)
    for name, fn in backdrop_sheets()[:1]:
        lay = shade_layer(name, sheet_layer(fn, 0.3))
        lay.onto(pic)
        layers[name] = lay
        np.maximum(near_row, lay.a, out=near_row)
    street_m, worn = street(pic)
    for name, fn in backdrop_sheets()[1:]:
        lay = shade_layer(name, sheet_layer(fn, 0.25 if name != "drain" else 0.15))
        lay.onto(pic)
        layers[name] = lay
        np.maximum(near_row, lay.a, out=near_row)
    sprinkled(pic)
    sprinkled(pic, 44, xc=520.0, dc=DF - 150.0, rx=105.0, rz=55.0)
    yard_sun(pic)
    layers["marks"] = street_marks(pic, worn)
    info["shade"] = shadows(pic, street_m)
    info["street"], info["near_row"] = street_m, near_row
    return np.clip(pic, 0, 1).astype(F32), layers, info


def details(pic, layers, amount=0.78):
    """Over the brushwork: the built things said again crisply (the brush must not blur a lattice or a tile edge)."""
    crisp = pic.copy()
    for name in ("lane", "offices", "bales", "kura", "yard", "school_inside", "school_doorway", "school_upper", "tane", "right", "hut", "mortar", "pan", "drain", "marks"):
        if name in layers:
            layers[name].onto(crisp)
    pic[...] = lerp(pic, crisp, amount)
    return pic


CUTS = ["noren-cotton", "noren", "desks", "shutters", "kitchendoor", "saltjar", "plumjar", "cloth", "ricepot", "pickletub", "well", "bucket", "gate"]     # back to front, as the scene lists them (postimp_plans.py)
ALTS = ["shutters-shut", "kitchendoor-open", "bucket-down", "cloth-bundle", "gate-shut"]
NEAR = ["near", "near-noren"]                           # the front plane (round twenty-three), last


def cut_layers():
    def shutters_all(s):
        school_front(s)
        school_clear(s)

    def shutters_shut(s):
        school_front(s, shut=True)
    L = {
        "shutters": sheet_layer(shutters_all, 0.25),
        "shutters-shut": sheet_layer(shutters_shut, 0.25),
        "desks": sheet_layer(desks, 0.15),
        "kitchendoor": sheet_layer(lambda s: kitchendoor(s), 0.15),
        "kitchendoor-open": sheet_layer(lambda s: kitchendoor(s, True), 0.15),
        "well": sheet_layer(well, 0.2),
        "bucket": sheet_layer(lambda s: bucket_layer(s), 0.1),
        "bucket-down": sheet_layer(lambda s: bucket_layer(s, True), 0.1),
        "ricepot": sheet_layer(ricepot, 0.1),
        "saltjar": sheet_layer(saltjar, 0.1),
        "pickletub": sheet_layer(pickletub, 0.1),
        "plumjar": sheet_layer(plumjar, 0.1),
        "cloth": sheet_layer(lambda s: cloth(s), 0.1),
        "cloth-bundle": sheet_layer(lambda s: cloth(s, True), 0.1),
        "noren": sheet_layer(tane_noren, 0.2),
        "noren-cotton": sheet_layer(cotton_noren, 0.2),
        "gate": sheet_layer(lambda s: gate(s), 0.25),
        "gate-shut": sheet_layer(lambda s: gate(s, True), 0.25),
    }
    # the school's opening must be clear of everything (the hand's push can leave a sliver): wipe it hard
    r0, r1 = ROOM
    m = mask_poly(SHAPE, [P(r0 + 2, SCH_FLOOR + 1, DF), P(r1 - 2, SCH_FLOOR + 1, DF), P(r1 - 2, 204, DF - 60), P(r0 + 2, 204, DF - 60)])
    L["shutters"].a *= (1 - m)
    L["shutters"].c *= (1 - m)[..., None]
    return L


def old_masks():
    """Round twenty-one's cut-outs' outlines, exactly (the print's drawing, as installed): {name: hard mask}."""
    STYLE["wc"] = False
    try:
        L = cut_layers()
    finally:
        STYLE["wc"] = True
    return {k: (v.a > 0.5).astype(F32) for k, v in L.items()}


def cut_shade(name):
    """Where the noon shade lies on a cut-out (a mask), and how deep (the rooms inside are dimmer than a shaded wall)."""
    x, y = grid(SHAPE)
    if name in ("noren", "noren-cotton"):
        return np.ones(SHAPE, F32), 1.0
    if name == "desks":
        return np.ones(SHAPE, F32), 1.35
    if name in ("shutters", "shutters-shut"):
        m = (y < P(0, 41.0, DF)[1]).astype(F32)
        stack = mask_poly(SHAPE, [(P(SCHOOL[0] - 4, 0, DF - 24)[0] - 14, 600), (P(SCHOOL[0] - 4, 0, DF - 24)[0] + 14, 600),
                                  (P(SCHOOL[0] - 4, 0, DF - 24)[0] + 14, P(0, 108, DF - 24)[1]), (P(SCHOOL[0] - 4, 0, DF - 24)[0] - 14, P(0, 108, DF - 24)[1])])
        return np.clip(m - stack, 0, 1).astype(F32), 1.0
    if name in ("kitchendoor", "kitchendoor-open"):
        return (y < P(0, 133.0, YARD_BACK)[1]).astype(F32), 1.0
    if name in ("gate", "gate-shut"):
        return (y < P(0, 165.0, GATE_D)[1]).astype(F32) * 0.85, 1.0
    return None, 0.0


def fill_out(color, have):
    """Carry a cut-out's new colours out to the old outline's edge: every pixel takes the colour of the nearest one painted."""
    from scipy.ndimage import distance_transform_edt
    if have.all():
        return color
    _, (iy, ix) = distance_transform_edt(~have, return_indices=True)
    return color[iy, ix]


def cut_pictures(back, fast=False, seed=SEED):
    """Every cut-out painted in washes inside its old outline: {name: (colour, hard mask)}."""
    masks = old_masks()
    L = cut_layers()
    out = {}
    for i, name in enumerate(CUTS + ALTS):
        c, a = L[name].straight()
        hard = masks[name]
        c = fill_out(c, a > 0.35)
        edge = (hard > 0.5) & ~(a > 0.35)
        c[edge] = deepen(c[edge], 0.12)                      # (where the print's line was: a soft dark edge)
        m, deep = cut_shade(name)
        if m is not None:
            sh = c * (SHADE if deep <= 1.0 else SHADE_DEEP)[None, None, :]
            if deep > 1.0:
                sh = sh * 0.82
            c = lerp(c, sh, m[..., None])
        from edo_village_kit import grade_cut, painted
        c = grade_cut(c, hard, 0.92, lightfrom=(-0.5, -0.8), seed=seed + i, uneven=0.05)
        if not fast:
            c, _ = painted(c, hard, np.median(back[hard > 0.5], axis=0) if hard.any() else back[300, 400], seed=40 + i, sizes=(4, 2), keep=0.72)
        out[name] = (np.clip(c, 0, 1).astype(F32), hard)
    return out


def wet_mask(info):
    """What was laid wet in wet (watercolor.wash's `soft`): the sky and its clouds 1, the hills 0.6, the castle's hill 0.4,
    the far roofs 0.18, the keep 0.1 (its edges must hold); 0 for the near row, the street and everything near."""
    m = info["sky_only"] * 1.0
    m = np.maximum(m, info["hills"] * 0.6)
    m = np.where(info["hill"] > 0.5, 0.40, m)
    m = np.where(info["roofs"] > 0.5, 0.18, m)
    m = np.where(info["keep"] > 0.3, 0.08, m)
    m = np.maximum(m, info["haze"] * 0.8 * (1 - info["keep"]))
    m = m * (1 - info["near_row"])
    return np.clip(m, 0, 1).astype(F32)


def to_file(picture, name, colors=128, alpha=None, seed=7, speckle=0.010, amount=0.010):
    """Pigment grain (little: the wash has its own granulation), then a limited palette with speckle: an 8-bit PNG."""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


COUNTS = {"noren-cotton": 48, "noren": 32, "desks": 48, "shutters": 64, "kitchendoor": 48, "saltjar": 32, "plumjar": 32, "cloth": 24, "ricepot": 32,
          "pickletub": 32, "well": 48, "bucket": 32, "gate": 64, "shutters-shut": 64, "kitchendoor-open": 48, "bucket-down": 24, "cloth-bundle": 24,
          "gate-shut": 64, "near": 128, "near-noren": 64}
WASH = dict(wander=1.4, fleck=0.30)


def finish_all(pic, cut, info, out=None):
    """THE WATERCOLOUR FINISH (DEPTH.md; Yui's recipe): the backdrop washed (watercolor.wash, soft = wet_mask), every
    cut-out washed over the unwashed backdrop with the same seed (wash_cut, crisp: its own edge stays), so the paper is
    one sheet; then grain and the palette."""
    out = out or OUT
    soft = wet_mask(info)
    back_washed = WC.wash(pic, seed=SEED, soft=soft, **WASH)
    sizes = {"back": to_file(back_washed, out + "/back.png", 250)}
    washed = {}
    for name in CUTS + ALTS + NEAR:
        c, a = cut[name]
        w_ = WC.wash_cut(c, (a > 0.5).astype(F32), pic, seed=SEED, soft=soft, crisp=True, **WASH)
        washed[name] = (w_, a)
        sizes[name] = to_file(w_, out + f"/{name}.png", COUNTS.get(name, 64), a)
    return back_washed, washed, sizes


if __name__ == "__main__":
    import edo_town_near as NEARMOD
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(f"{OUT}-work", exist_ok=True)
    fast = "fast" in sys.argv
    base, layers, info = under()
    to_png(base, f"{OUT}-work/1-under.png")
    print("under", round(time.time() - t0, 1))
    if fast:
        pic = base.copy()
    else:
        # the brush pass, light: the far plane stays as the wet washes left it, the near row and the street half brushed
        brushed_ = strokes(base, sizes=(10, 5, 3), seed=2, density=1.4, jitter=0.02, keep=0.0)
        keep = np.clip(0.52 + 0.36 * wet_mask(info), 0, 0.92)
        pic = lerp(brushed_, base, keep[..., None]).astype(F32)
    details(pic, layers)
    print("details", round(time.time() - t0, 1))
    cut = cut_pictures(pic, fast)
    nc, na = NEARMOD.near_cut()
    cut["near"] = (nc, (na > 0.5).astype(F32))
    nc, na = NEARMOD.noren_cut()
    cut["near-noren"] = (nc, (na > 0.5).astype(F32))
    whole = pic.copy()
    for name in CUTS + NEAR:
        c, a = cut[name]
        over(whole, c, a)
    to_png(whole, f"{OUT}-2-all.png")
    print("painted", round(time.time() - t0, 1))
    if fast and "wash" not in sys.argv:
        sys.exit()
    target = OUT if not fast else OUT + "-fast"
    os.makedirs(target, exist_ok=True)
    back_washed, washed, sizes = finish_all(pic, cut, info, target)
    print(sizes)
    if not fast:
        import edo_town_layout as LY
        LY.write(f"{OUT}/layout.json")
    comp = Image.open(f"{target}/back.png").convert("RGBA")
    for name in CUTS + NEAR:
        comp.alpha_composite(Image.open(f"{target}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(f"{OUT}-comp.png" if not fast else f"{OUT}-fast-comp.png")
    print("done", round(time.time() - t0, 1))

"""Himeji, about 29 April 1830, midday: Watamachi on the highway (edo-town). PAINT-21E, round twenty-one.

The design (S/briefs/out/edo2-design.md, sections 4 and 5; S/briefs/PAINT-21E.md): the game's own painting, composed and
coloured as the woodblock landscape prints are (S/work-20-paintA/style.md): flat masses, a graded sky, one fine prussian
contour, few colours, the blue leading. Nothing is copied from any print: the composition is our own.

What is in it (edo_town_kit.py has the camera and the plan): the broad highway across the bottom; across it, left to
right, the domain's paper-note office and cotton office along the bend of the street (two storeys, white; bales of white
cloth at the cotton office's door), the writing school with its shutters propped open (the raised floor inside, a row of
low desks: the girls and the teacher are the game's people), O-Tane's side yard open to the street with the kitchen
lean-to at its back (the stone-lined well and its pulley and bucket before it; the rice pot, the salt jar, the pickle tub
and its stone, the plum jar, a cloth, the roasting pan drying, the Bizen mortar), O-Tane's house (a lattice front, an
indigo noren), Tobei's hut (straw sandals hung, a jar of sweets, the clappers on a peg, his stool), the ward gate across
the lane north, its doors open by day. Above the roofs, far up on its hill, the keep. Not painted: people (the game's),
smoke (the kitchen's: fx), the noren's stirring (sway), birds (fx), light.

  python3 edo_town.py          paints everything into out/edo-town/ (and out/edo-town-comp.png to look at)
  python3 edo_town.py fast     skips the brush pass and the palette: out/edo-town-2-all.png only"""

import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, Sheet, grid, noise, blur, over, tint, glow, lerp, mask_poly, mask_ellipse, strokes, curve, warp, vary
from rome_steps_kit import Canvas
from edo_town_kit import *

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


# ---------------------------------------------------------------- the sky, the hill, the keep, the far roofs
def sky_layer():
    stops = [mix(PAINT["cobalt"], PAINT["prussian"], 0.42), mix(PAINT["cobalt"], PAINT["prussian"], 0.18), PAINT["cobalt"],
             mix(PAINT["cobalt"], PAINT["cerulean"], 0.5), PAINT["cerulean"], mix(PAINT["cerulean"], PAPER, 0.45), mix(PAINT["cerulean"], PAPER, 0.78), PAPER]
    pic = bands(stops, 0, 250, seed=31, wobble=2.0, soft=2.6)
    s = Sheet(SHAPE)
    for (cx, cy, w, h) in ((150, 70, 240, 13), (250, 92, 130, 8), (700, 46, 170, 10)):
        top = [(cx - w / 2 + w * i / 10, cy - h * (0.5 + 0.5 * math.sin(i * 1.9 + cx) * 0.6) * (1 - ((i - 5) / 5.5) ** 2)) for i in range(11)]
        s.poly(top + [(cx + w / 2, cy), (cx - w / 2, cy)], PAPER, 0.96)
        s.line(top, LINE, 0.9, 0.45)
    s.onto(pic)
    return pic


KEEP_AT = (566.0, 176.0)            # the foot of the keep's stone base on its hill (picture), and its scale
KEEP_K = 0.36


def keep_layer():
    """PAINT-20D's keep (edo_castle.keep: the same drawing, so the act has one castle), drawn at full size on its own
    sheet and laid in small, far up on its hill. Seen from the town it is the same white keep, smaller."""
    import edo_castle as EC
    big = Canvas(SHAPE)
    lay = sheet_layer(EC.keep, 0.3)
    c, a = lay.c, lay.a                                     # premultiplied
    x0, y0, x1, y1 = 236, 20, 486, 340
    crop = np.dstack([c[y0:y1, x0:x1], a[y0:y1, x0:x1]])
    w, h = int(round((x1 - x0) * KEEP_K)), int(round((y1 - y0) * KEEP_K))
    small = np.zeros((h, w, 4), F32)
    for i in range(4):                                       # area-average down (premultiplied, so the edge stays true)
        im = Image.fromarray(crop[..., i].astype(np.float32), "F").resize((w, h), Image.BOX)
        small[..., i] = np.asarray(im, F32)
    # place: the base's foot (row 332 in the castle picture, x 360 its middle) at KEEP_AT
    fx, fy = (360 - x0) * KEEP_K, (332 - y0) * KEEP_K
    ox, oy = int(round(KEEP_AT[0] - fx)), int(round(KEEP_AT[1] - fy))
    out = Canvas(SHAPE)
    out.c[oy:oy + h, ox:ox + w] = small[..., :3]
    out.a[oy:oy + h, ox:ox + w] = small[..., 3]
    # the keep is far: paler and bluer toward the sky's low band, its contour a breath (style.md section 7)
    st, al = out.straight()
    st = lerp(st, mix(PAINT["cerulean"], PAPER, 0.55)[None, None, :], 0.16)
    out.c = st * al[..., None]
    return out


def hill(s):
    """Himeyama, the keep's hill, behind the roofs: a dark flat with pines standing on it in two depths; on its
    shoulders the white of the castle's lower walls; the town's far roofs in rows below it (no contour: the far plane)."""
    rng = np.random.default_rng(32)
    kx, ky = KEEP_AT
    crest = curve([(150, 236), (260, 214), (380, 196), (470, 184), (kx - 44, ky - 1), (kx + 44, ky - 1), (660, 184), (740, 198), (830, 212)], 8)
    s.poly(crest + [(830, 300), (330, 300)], C["hill"])
    s.poly([(p[0], p[1] + 2) for p in crest if p[0] > kx - 30] + [(830, 300), (kx - 30, 300)], mix(C["hill"], C["hill_lit"], 0.5), 0.6)
    for (x0, x1, y) in ((kx - 100, kx - 52, 192), (kx + 54, kx + 110, 194)):      # the lower walls, white, with their dark copings
        s.poly([(x0, y + 8), (x1, y + 8), (x1, y), (x0, y)], mix(PAPER, PAINT["cerulean"], 0.25))
        s.line([(x0 - 1, y - 1), (x1 + 1, y - 1)], mix(C["tile"], PAINT["cerulean"], 0.4), 1.6)
    for depth, (yb, step_, hs, tone, lit) in enumerate(((0, 24, (12, 20), mix(C["pine_far"], PAPER, 0.25), mix(C["pine_far"], PAPER, 0.45)),
                                                        (14, 32, (16, 26), C["pine_far"], mix(C["pine_far"], C["pine_lit"], 0.5)))):
        for px in np.arange(160 + depth * 11, 800, step_):
            if rng.random() < 0.3:
                continue
            cy = np.interp(px, [p[0] for p in crest], [p[1] for p in crest])
            if px > kx - 46 and px < kx + 46:
                continue
            pine(s, px + rng.uniform(-5, 5), cy + 12 + yb + rng.uniform(-2, 2), rng.uniform(*hs), tone, lit, rng, pads=3)


def far_roofs(s):
    """The town's roofs between us and the hill: rows of tiled roofs, far, flat, pale toward the sky (no contour)."""
    rng = np.random.default_rng(33)
    for row, (y, tone, h) in enumerate(((214, mix(C["tile"], PAPER, 0.55), 9), (226, mix(C["tile"], PAPER, 0.48), 11), (240, mix(C["tile"], PAPER, 0.40), 13),
                                        (256, mix(C["tile"], PAPER, 0.32), 15), (274, mix(C["tile"], PAPER, 0.25), 17))):
        x = -20 + rng.uniform(0, 30)
        while x < 820:
            w = rng.uniform(38, 90)
            ridge = y - h * rng.uniform(0.7, 1.0)
            s.poly([(x, y + 6), (x + w, y + 6), (x + w - 6, ridge), (x + 6, ridge)], tone)
            s.line([(x + 6, ridge), (x + w - 6, ridge)], mix(tone, PAPER, 0.3), 1.0, 0.7)
            s.poly([(x + 3, y + 6), (x + w - 3, y + 6), (x + w - 3, y + 14), (x + 3, y + 14)], mix(PAPER, PAINT["cerulean"], 0.3 + row * 0.08))
            x += w + rng.uniform(-6, 10)


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
            s.poly(face, mix(C["cloth"], C["straw"], 0.32))
            s.poly([P(X, y0 + 29, d), P(X + 54, y0 + 29, d), P(X + 54, y0 + 29, d + 40), P(X, y0 + 29, d + 40)], mix(C["cloth"], PAPER, 0.45))   # its top, lit
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
        s.poly(wall, wall_c)
        s.poly([P(x1, 0, a0), P(x1, 0, a1), P(x1, 150, a1), P(x1, 150, a0)], board_c)
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


# ---------------------------------------------------------------- the street
def street(pic):
    """The highway: packed earth, sunlit, flat, a little warmer down the middle where the feet go; the stone gutter
    along the far fronts with its flat bridging stones; the bend's street running off at the left; a few stones."""
    x, y = grid(SHAPE)
    rng = np.random.default_rng(37)
    m = (y >= row_D(GUT) - 1).astype(F32)
    over(pic, vary(C["street"], SHAPE, 38, amount=0.03, cell=60), m)
    worn = mask_poly(SHAPE, [(-10, 520), (810, 506), (810, 566), (-10, 584)], soft=10, wobble=6, seed=39)
    over(pic, C["street_lit"], worn * 0.45 * m)
    s = Sheet(SHAPE)
    # the gutter: a narrow stone channel along the fronts, light edge, dark water-line; stones bridging it at doors
    for (xa, xb) in ((-1400, LANE[0]), (LANE[1], 1300)):
        g0, g1 = P(xa, 0, GUT), P(xb, 0, GUT)
        h0, h1 = P(xa, 0, GUT + 22), P(xb, 0, GUT + 22)
        s.poly([g0, g1, h1, h0], C["stone_sh"])
        s.line([g0, g1], C["stone_lit"], 1.4)
        s.line([h0, h1], mix(C["stone_sh"], LINE, 0.4), 1.0, 0.8)
    for (xa, xb) in ((ROOM[1] - 76, ROOM[1] - 4), (TANE[0] + 8, TANE[0] + 96), (YARD[0] + 40, YARD[1] - 40), (HUT[0] + 20, HUT[1] - 20),
                     (COTTON_DOOR[0] + 10, COTTON_DOOR[1] - 10), (NOTE_DOOR[0], NOTE_DOOR[1])):
        st = [P(xa, 2, GUT - 4), P(xb, 2, GUT - 4), P(xb, 2, GUT + 26), P(xa, 2, GUT + 26)]
        s.poly(st, C["stone_lit"])
        outline(s, st, 0.5, 0.45)
    # small stones and dry ruts across the street
    for i in range(70):
        yy = rng.uniform(row_D(GUT) + 8, 598)
        xx = rng.uniform(0, 800)
        r = rng.uniform(0.8, 2.4) * scale_at(yy)
        s.ellipse(xx, yy, r * 1.5, r * 0.8, [C["stone_sh"], C["rut"], C["stone_lit"]][int(rng.integers(3))], 0.8)
    for k in range(3):
        yy = 540 + k * 18
        s.line([(-10, yy + rng.uniform(-2, 2)), (400, yy + rng.uniform(-2, 2)), (810, yy - 6 + rng.uniform(-2, 2))], C["rut"], 1.2, 0.25)
    # a few bigger flat stones near us, each with its small noon shadow away from us
    for (xx, yy, r) in ((96, 574, 7.0), (640, 588, 6.0), (318, 536, 4.4), (712, 522, 3.6), (500, 566, 5.0)):
        s.ellipse(xx + r * 0.3, yy - r * 0.35, r * 1.5, r * 0.55, C["street_sh"], 0.8)
        s.ellipse(xx, yy, r * 1.4, r * 0.6, C["stone"])
        s.ellipse(xx - r * 0.3, yy - r * 0.15, r * 0.8, r * 0.3, C["stone_lit"])
        s.ellipse(xx, yy, r * 1.4, r * 0.6, LINE, 0.0)
    s.onto(pic)
    # the printmaker's graded band along the bottom edge of the ground: three flat steps, deepening toward us
    for (y0, a) in ((566, 0.10), (582, 0.18), (594, 0.26)):
        band = mask_poly(SHAPE, [(-10, y0), (810, y0 - 4), (810, 610), (-10, 610)], soft=2.0, wobble=1.5, seed=int(y0))
        over(pic, C["street_sh"], band * a)
    return pic


def shadows(pic):
    """The midday shade: the hard band of each deep eave across the top of the fronts is painted with the fronts; on
    the ground, the short shadows of what stands in the street fall away from us (north), a little to the right."""
    s = Sheet(SHAPE)
    # under the pent roofs, a narrow band of shade on the street at the fronts' feet (the eaves overhang 70 cm)
    for (xa, xb) in ((COTTON[0] - 200, NOTE[1]), (SCHOOL[0], SCHOOL[1]), (TANE[0], TANE[1]), (LANE[1], 1300)):
        s.poly([P(xa + 10, 0, DF - 20), P(xb + 10, 0, DF - 20), P(xb, 0, DF), P(xa, 0, DF)], C["cast"], 0.5)
    # the hut's and the gate posts' shadows
    x0, x1 = HUT
    s.poly([P(x0 + 10, 0, DF - 46), P(x1 + 14, 0, DF - 46), P(x1, 0, DF - 30), P(x0, 0, DF - 30)], C["cast"], 0.55)
    for xp in (GATE[0], GATE[1] - 14):
        s.poly([P(xp + 4, 0, GATE_D), P(xp + 18, 0, GATE_D), P(xp + 18 + 25, 0, GATE_D + 90), P(xp + 4 + 25, 0, GATE_D + 90)], C["cast"], 0.5)
    c, a = s.done()
    tint(pic, C["cast"], blur(a, 0.6) * 0.42)
    return pic


# ---------------------------------------------------------------- the passes
def backdrop_sheets():
    """Everything of the backdrop, far to near, on sheets: a list of (name, draw function)."""
    return [
        ("hill", hill), ("far", far_roofs), ("lane", lane), ("offices", offices), ("bales", bales),
        ("kura", kura), ("yard", yard), ("mortar", mortar), ("pan", pan), ("school_inside", school_inside), ("school_doorway", school_doorway),
        ("school_upper", school_upper), ("tane", tane_house), ("right", right_house), ("hut", hut),
    ]


def under(seed=31):
    pic = sky_layer()
    layers = {}
    for name, fn in backdrop_sheets()[:2]:
        lay = sheet_layer(fn, 0.0)
        lay.onto(pic)
    keep_l = keep_layer()
    keep_l.onto(pic)
    layers["keep"] = keep_l
    for name, fn in backdrop_sheets()[2:4]:
        lay = sheet_layer(fn, 0.3)
        lay.onto(pic)
        layers[name] = lay
    street(pic)
    for name, fn in backdrop_sheets()[4:]:
        lay = sheet_layer(fn, 0.25)
        lay.onto(pic)
        layers[name] = lay
    shadows(pic)
    # the noon air: the far things a little paler toward the sky's low band
    x, y = grid(SHAPE)
    haze = np.clip((300 - y) / 220.0, 0, 1) ** 1.6 * (y < 300)
    return np.clip(pic, 0, 1), layers


def details(pic, layers):
    """Over the brushwork: the built things said again crisply (the brush must not blur a lattice or a tile edge)."""
    crisp = pic.copy()
    for name in ("keep", "lane", "offices", "bales", "kura", "yard", "school_inside", "school_doorway", "school_upper", "tane", "right", "hut", "mortar", "pan"):
        if name in layers:
            layers[name].onto(crisp)
    pic[...] = lerp(pic, crisp, 0.80)
    return pic


CUTS = ["noren-cotton", "noren", "desks", "shutters", "kitchendoor", "saltjar", "plumjar", "cloth", "ricepot", "pickletub", "well", "bucket", "gate"]     # back to front, as the scene lists them (postimp_plans.py)
ALTS = ["shutters-shut", "kitchendoor-open", "bucket-down", "cloth-bundle", "gate-shut"]


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


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(f"{OUT}-work", exist_ok=True)
    fast = len(sys.argv) > 1 and sys.argv[1] == "fast"
    base, layers = under()
    to_png(base, f"{OUT}-work/1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else strokes(base, sizes=(10, 5, 3), seed=2, density=1.4, jitter=0.022, keep=0.40)
    ground_ = pic.copy()
    details(pic, layers)
    details(ground_, layers)
    print("details", round(time.time() - t0, 1))
    cuts = cut_layers()
    whole = pic.copy()
    cut = {}
    for i, name in enumerate(CUTS + ALTS):
        layer = cuts[name]
        if fast:
            c, a = layer.straight()
            a = (a > 0.5).astype(F32)
        else:
            c, a = brushed(layer, ground_, seed=40 + i, sizes=(5, 3, 2), restate=0.9)
        cut[name] = (c, a)
        if name in CUTS:
            over(whole, c, a)
    to_png(whole, f"{OUT}-2-all.png")
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    size, pal = finish(pic, f"{OUT}/back.png", 160)
    print("back", size)
    for name, (c, a) in cut.items():
        print(name, finish(c, f"{OUT}/{name}.png", 64, a)[0])
    import edo_town_layout as LY
    LY.write(f"{OUT}/layout.json")
    comp = Image.open(f"{OUT}/back.png").convert("RGBA")
    for name in CUTS:
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(f"{OUT}-comp.png")
    print("done", round(time.time() - t0, 1))

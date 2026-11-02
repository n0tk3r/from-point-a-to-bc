"""PAINT-21C: Osaka, a merchant street (Shinsaibashi-suji) at a crossroads, about 21 April 1830, late afternoon
(edo-street). In the act's woodblock manner (S/work-20-paintA/style.md), keyed in `edo-city`.

LIGHT   The sun low in the west-south-west behind us and to the right (about half past four, 27 degrees up): the shop
        fronts across the street face it and are lit warm from their eaves up; the street floor lies in the shadow of
        the houses on our side, and so do the fronts below about 1.8 m, cool and blue; except where the cross street
        lets the sun through: a band of warm light comes across the street, over the crossroads and the road god, onto
        the print shop's corner and its bench. The shadow side of everything is blue (cobalt to prussian).
DEPTH   horizon 262, full 590 (room.View turned 25 degrees to the right: we look east, a little south, across the
        street; the street goes off to the right, the cross street away to the left beyond the crossroads).
TONES   light: the upper fronts and the eaves in the sun, the band of sun on the street, the sky low down; middle: the
        roofs' grey-blue, the street in shade, the noren; dark: the inside of the open fronts, the contour. The eye goes
        to the band of sun: the crossroads, the road god, the print shop's bench and its prints.
PLACE   (world in cm: X along the main street to the right (south), Z toward us (west), Y up; the far fronts on Z -1300;
        the houses on our side, unseen, on Z -650.) From the left: Senzo's print shop on the corner (its front open:
        prints pegged on lines, toy prints, the raised floor, the printing bench at its edge); the cross street going
        away to the left behind it, a town office's fire-watch tower over its roofs; across it the kelp shop on the
        corner; the medicine shop with its big standing signboard (Uruyusu); the comb-maker's comb-shaped signboard; the
        street going on to the right, and far off over the roofs the drum tower of a theatre (the way there).

  python3 edo_street.py fast     the composition without the brush pass (out/edo-street-1-under.png, -2-all.png)
  python3 edo_street.py          the full passes: out/edo-street/ (back.png, the cut-outs, layout.json)
"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
from edo_dojima_kit import *

SEED = 1676
OUT = "out/edo-street"
HZ, FULL = 262, 590
SUN = (0.231, 0.454, 0.861)                                         # toward the sun: south 0.23, up 0.45, west 0.86 (WSW, 27 degrees up)
CAM = City(HZ, FULL, (0.0, 0.0), 25.0, sun=SUN)

ZE = -1300.0                       # the far (east) side's fronts
ZW = -650.0                        # our (west) side's fronts, behind the picture
ROOF_W = 520.0                     # the height of our side's eaves and roofs, whose shadow lies on the street
CROSS = (330.0, 790.0)             # the cross street's two sides (X)
PRINT = dict(X0=-80.0, X1=330.0, eave=255.0, upper=470.0, ridge=640.0, depth=1100.0)
KELP = dict(X0=790.0, X1=1080.0, eave=250.0, upper=455.0, ridge=610.0, depth=640.0)
MED = dict(X0=1090.0, X1=1330.0, eave=255.0, upper=470.0, ridge=640.0, depth=1000.0)
COMB = dict(X0=1340.0, X1=1640.0, eave=245.0, upper=450.0, ridge=600.0, depth=900.0)
BEYOND = [dict(X0=1650.0, X1=2050.0, eave=250.0, upper=460.0, ridge=620.0, depth=900.0), dict(X0=2060.0, X1=2420.0, eave=250.0, upper=440.0, ridge=600.0, depth=900.0),
          dict(X0=2430.0, X1=2800.0, eave=255.0, upper=465.0, ridge=630.0, depth=900.0)]
BENCH = dict(X0=120.0, X1=310.0, Z0=-1338.0, Z1=-1290.0, floor=45.0, h=26.0)   # the printing bench at the front edge of the raised floor
SHADE_Y = ROOF_W - (ZW - ZE) * SUN[1] / SUN[2]                       # how high the street's shadow climbs the far fronts (cm)


def g(X, Z, Y=0.0):
    return CAM.pt(X, Y, Z)


def in_band(X, Z):
    """Is this place on the far side's floor or fronts lit through the cross street (the gap in our side's houses)?"""
    Xw = X + SUN[0] / SUN[2] * (ZW - Z)
    return CROSS[0] <= Xw <= CROSS[1]


# ================================================================ pass 1: broad and flat
def paint_sky(seed):
    rows = [0, 44, 90, 132, 170, 204, 232, 252, HZ + 40]
    cols = [mixp(COBALT, PRUSSIAN, 0.2), mixp(COBALT, ULTRA, 0.12), COBALT, mixp(COBALT, CERULEAN, 0.5), CERULEAN,
            tintw(CERULEAN, 0.42), lerp(tintw(CERULEAN, 0.66), NAPLES, 0.14), PAPER, PAPER]
    pic = bands(SHAPE, rows, cols, soft=6.0, wobble=2.5, seed=seed, patch=0.02)
    x, y = grid(SHAPE)
    glow(pic, tintw(NAPLES, 0.3), (np.clip(1 - x / 600.0, 0, 1) * np.clip(1 - np.abs(y - 240) / 70.0, 0, 1) * 0.10).astype(F32))
    s = Paper(SHAPE)
    for (cx, cy, w, h) in ((520, 58, 210, 11), (150, 112, 150, 8)):
        top = [(cx - w / 2 + w * i / 12, cy - h * (1 - ((i - 6) / 6.3) ** 2) * (0.75 + 0.25 * math.sin(i * 1.7 + cx))) for i in range(13)]
        s.poly(top + [(cx + w / 2, cy + 1), (cx - w / 2, cy + 1)], lerp(WHITE, NAPLES, 0.12), 0.95)
        s.line(top, PRUSSIAN, 0.8, 0.4)
    s.onto(pic)
    return pic


def far_roofs(pic, seed):
    """The town beyond, far: a band of grey-blue roofs at the horizon, ridge on ridge, paler going away; the drum tower of
    a theatre over them at the right (a square frame tower hung with a curtain: the way to the theatre); no contour."""
    s = Paper(SHAPE)
    rng = np.random.default_rng(seed + 3)
    for (y0, tone, n) in ((246, 0.62, 14), (256, 0.50, 18)):
        x = -20.0
        while x < 820:
            w = rng.uniform(40, 110)
            h = rng.uniform(5, 12)
            s.poly([(x, y0 + 14), (x, y0 - h * 0.4), (x + w * 0.15, y0 - h), (x + w * 0.85, y0 - h), (x + w, y0 - h * 0.4), (x + w, y0 + 14)],
                   lerp(lerp(TILE_SH, CERULEAN, 0.2), PAPER, tone))
            x += w + rng.uniform(-8, 4)
    s.onto(pic)


def drum_tower(sheet):
    """Far off over the roofs at the right: a theatre's drum tower, a square frame of timber on the theatre's roof, hung
    round with a striped curtain (no crest: our own plain stripes), a little roof over it. Far: no contour, two flats."""
    far = lambda c, t=0.35: lerp(lerp(c, PAPER, t), CERULEAN, 0.08)
    X, Z = 3500.0, -3500.0
    base, top = 760.0, 1180.0
    hw = 160.0
    a, b = g(X - hw, Z, base), g(X + hw, Z, top)
    k = CAM.k(X, Z)
    # the theatre's roof under it (a dark broad gable)
    r0, r1 = g(X - 700, Z, 560), g(X + 600, Z, 560)
    sheet.poly([r0, r1, g(X + 420, Z, base), g(X - 520, Z, base)], far(TILE_SH, 0.35))
    # the curtain: vertical stripes of indigo and white, round the frame
    w = b[0] - a[0]
    for i in range(6):
        c = INDIGO if i % 2 == 0 else PLASTER_LIT
        x0, x1 = a[0] + w * i / 6, a[0] + w * (i + 1) / 6
        sheet.poly([(x0, a[1]), (x1, a[1]), (x1, b[1] + 6 * k * 8), (x0, b[1] + 6 * k * 8)], far(c, 0.3))
    sheet.poly([(a[0], b[1] + 6 * k * 8), (b[0], b[1] + 6 * k * 8), (b[0], b[1]), (a[0], b[1])], far(WOOD_SH, 0.3))
    sheet.poly([(a[0] - 4, b[1] + 1), (b[0] + 4, b[1] + 1), (b[0] - 2, b[1] - 6), (a[0] + 2, b[1] - 6)], far(TILE_SH, 0.3))
    for dx in (-0.3, 0.3):                                   # two tall staves standing up from it
        sheet.line([(a[0] + w * (0.5 + dx), b[1] - 6), (a[0] + w * (0.5 + dx * 1.1), b[1] - 26)], far(WOOD_SH, 0.3), 1.0)
    return [int(a[0]) - 6, int(b[1]) - 28, int(w) + 12, int(a[1] - b[1]) + 34]


def fire_tower(sheet, lines):
    """Down the cross street, on the town office's roof: the fire-watch tower, a tall ladder of timber standing on the
    ridge, a small railed platform at its top under a little roof (a fact of the 1830s street: a town office with a
    fire-watch tower on its roof). Middle distance: 0.6 px contour."""
    X, Z = 1000.0, -3000.0
    roof, top = 600.0, 1120.0
    k = CAM.k(X, Z)
    legs = [(X - 70, Z + 60), (X + 70, Z + 60), (X - 70, Z - 60), (X + 70, Z - 60)]
    col = lerp(WOOD_SH, PAPER, 0.15)
    for (lx, lz) in legs:
        sheet.line([g(lx, lz, roof), g(lx * 0.0 + X + (lx - X) * 0.75, Z + (lz - Z) * 0.75, top - 90)], col, max(1.0, 9 * k))
    for yv in np.linspace(roof + 60, top - 120, 7):          # the ladder's rungs and the braces
        f = (yv - roof) / (top - roof)
        sheet.line([g(X - 70 + 17 * f, Z + 60, yv), g(X + 70 - 17 * f, Z + 60, yv)], col, max(0.7, 5 * k))
    for i in range(3):
        y0 = roof + (top - roof) * i / 3
        y1 = roof + (top - roof) * (i + 1) / 3 - 90
        lines.line([g(X - 70, Z + 60, y0), g(X + 70, Z + 60, y1)], col, max(0.6, 4 * k), 0.8)
    # the platform, its rail, and its little roof
    p0, p1 = g(X - 80, Z + 70, top - 90), g(X + 80, Z + 70, top - 90)
    sheet.poly([p0, p1, g(X + 80, Z + 70, top - 40), g(X - 80, Z + 70, top - 40)], lerp(WOOD_LIT, PAPER, 0.1))
    sheet.poly([g(X - 110, Z + 90, top - 30), g(X + 110, Z + 90, top - 30), g(X + 60, Z + 40, top + 25), g(X - 60, Z + 40, top + 25)], lerp(TILE_SH, PAPER, 0.15))
    lines.line([g(X - 110, Z + 90, top - 30), g(X - 60, Z + 40, top + 25), g(X + 60, Z + 40, top + 25), g(X + 110, Z + 90, top - 30)], PRUSSIAN, 0.6, 0.45)
    a, b = g(X - 120, Z, top + 30), g(X + 120, Z, roof)
    return [int(a[0]) - 4, int(a[1]) - 4, int(b[0] - a[0]) + 8, int(b[1] - a[1]) + 8]


def paint_cross(pic, seed):
    """The cross street going away beyond the crossroads (it recedes to the left, behind the print shop): its floor (lit
    along its north side, the rest in its south houses' shade), and its south side's fronts, facing north, in shade:
    house after house, a dark ground storey, a pale upper storey, the eave between, their roofs one long band going away;
    among them the town office, a broader front with a white upper storey, and on its roof the fire-watch tower."""
    s = Paper(SHAPE)
    lines = s
    rng = np.random.default_rng(seed + 7)
    Zfar = -16000.0
    X = CROSS[1]
    Z0 = ZE - KELP["depth"]                                   # where the kelp shop's side ends and the next house begins
    floor_ = [g(CROSS[0], ZE), g(CROSS[1], ZE), g(CROSS[1], Zfar), g(CROSS[0], Zfar)]
    s.poly(floor_, lerp(EARTH, PAPER, 0.12))
    s.poly([g(CROSS[0] + 160, ZE), g(CROSS[1], ZE), g(CROSS[1], Zfar), g(CROSS[0] + 160, Zfar)], lerp(shaded(EARTH, 0.42), PAPER, 0.06))
    # the roofs, one band from the kelp shop's back to the far end: the slope toward the street (north and up: shade)
    pale = lambda Z: float(np.clip((-Z - 1800) / 9000.0, 0, 0.55))
    houses = []
    Zc = Z0
    while Zc > Zfar:
        w = rng.uniform(380, 560) if not houses or abs(Zc + 2800) > 400 else 700.0
        houses.append((Zc, Zc - w, rng.integers(0, 3)))
        Zc -= w
    office = min(houses, key=lambda h: abs((h[0] + h[1]) / 2 + 3000))
    for (Za, Zb, kind) in houses:
        t = pale((Za + Zb) / 2)
        is_off = (Za, Zb, kind) == office
        eave, upper = (250.0, 480.0) if is_off else (240.0 + 10 * kind, 440.0 + 15 * kind)
        s.poly([g(X, Za, 0), g(X, Zb, 0), g(X, Zb, eave), g(X, Za, eave)], lerp(shaded(WOOD, 0.4), PAPER, t))
        s.poly([g(X, Za, eave + 40), g(X, Zb, eave + 40), g(X, Zb, upper), g(X, Za, upper)], lerp(PLASTER_SH if not is_off else lerp(PLASTER_SH, WHITE, 0.25), PAPER, t))
        if kind == 0 or is_off:                                # a doorway with a noren, or the office's broad door
            d0, d1 = Za - (Za - Zb) * 0.3, Za - (Za - Zb) * 0.62
            s.poly([g(X - 2, d0, 200), g(X - 2, d1, 200), g(X - 2, d1, 128), g(X - 2, d0, 128)], lerp(INDIGO if not is_off else WOOD_DARK, PAPER, t))
        elif kind == 1:                                        # a lattice front
            for Zl in np.linspace(Za - 30, Zb + 30, 9):
                s.line([g(X - 2, Zl, 30), g(X - 2, Zl, eave - 30)], lerp(WOOD_LIT, PAPER, t + 0.1), 0.6, 0.6)
        lines.line([g(X, Za, 0), g(X, Za, upper)], lerp(PRUSSIAN, PAPER, t), 0.5, 0.4)
    # the eaves and the main roofs over them, continuous (they face north and up: the shade's grey-blue)
    for (Ya, Yb, dz) in ((230.0, 280.0, (-70.0, 25.0)), (440.0, 620.0, (-60.0, 380.0))):
        band = [g(X + dz[0], Z0 + 40, Ya), g(X + dz[0], Zfar, Ya), g(X + dz[1], Zfar, Yb), g(X + dz[1], Z0 + 40, Yb)]
        s.poly(band, lerp(TILE_SH, PAPER, 0.12))
        lines.line([band[0], band[1]], PRUSSIAN, 0.6, 0.45)
    c, a = s.done()
    over(pic, c, a)
    s2 = Paper(SHAPE)
    fire = fire_tower(s2, s2)
    c, a = s2.done()
    over(pic, c, a)
    return fire


def paint_ground(pic, seed):
    """The main street's floor: packed earth in the shadow of our side's houses (cool, blue), and the band of late sun
    that comes through the cross street across it (warm), its edges hard (a shadow has a hard edge: style.md)."""
    x, y = grid(SHAPE)
    X, Z, m = CAM.floor()
    ground = ((m > 0.5) & (Z > ZE)).astype(F32)
    lit_earth = flat(EARTH, SHAPE, seed + 40, 0.05, 40)
    shade_earth = flat(shaded(EARTH, 0.42), SHAPE, seed + 41, 0.04, 40)
    Xw = X + SUN[0] / SUN[2] * (ZW - Z)
    band = ((Xw >= CROSS[0]) & (Xw <= CROSS[1])).astype(F32)
    band = blur(band, 0.6)
    floor_c = lerp(shade_earth, lit_earth, band[..., None])
    t = np.clip((y - HZ) / (H - HZ), 0, 1)
    floor_c = lerp(floor_c, PAPER, ((1 - t) ** 1.8 * 0.25)[..., None])
    over(pic, floor_c, ground)
    # the gutter along the fronts: a narrow stone-edged drain before the far side's sill (a dark line and its stones)
    s = Paper(SHAPE)
    for X0, X1 in ((-400.0, CROSS[0]), (CROSS[1], 4000.0)):
        s.poly([g(X0, ZE + 45), g(X1, ZE + 45), g(X1, ZE + 15), g(X0, ZE + 15)], lerp(STONE_SH, PRUSSIAN, 0.3))
        s.line([g(X0, ZE + 45), g(X1, ZE + 45)], STONE_LIT, max(0.8, 3.0 * CAM.k(X0 + 400, ZE)), 0.9)
    c, a = s.done()
    over(pic, c, a)
    return ground, band


def shop_front(sheet, lines, S, kind, rng, signs=None):
    """A townhouse on the far side, its front to the street (facing west: toward the sun, which lights it above the
    street's shadow line, and in full where the band of sun comes through the cross street). The ground storey: the
    posts, the sill, what fills the front (`kind`: open (an open shop front: a raised floor and the dark inside),
    lattice, shutters), the eave of tiles at about 2.5 m; the low upper storey of plaster with its slatted windows; the
    main roof. Each face one flat; above the shadow line the lit flat, below it the shade flat."""
    X0, X1 = S["X0"], S["X1"]
    e, u, r = S["eave"], S["upper"], S["ridge"]
    Zf = ZE
    out = {}
    def lit_or_shade(c, Xa, Xb, Ya, Yb):
        """The front's flat from Ya to Yb: the shade flat below the street's shadow line (but in the band), lit above."""
        y_cut = SHADE_Y
        if Yb <= y_cut:
            sheet.poly([g(Xa, Zf, Ya), g(Xb, Zf, Ya), g(Xb, Zf, Yb), g(Xa, Zf, Yb)], shaded(c, 0.42))
        elif Ya >= y_cut:
            sheet.poly([g(Xa, Zf, Ya), g(Xb, Zf, Ya), g(Xb, Zf, Yb), g(Xa, Zf, Yb)], c)
        else:
            sheet.poly([g(Xa, Zf, Ya), g(Xb, Zf, Ya), g(Xb, Zf, y_cut), g(Xa, Zf, y_cut)], shaded(c, 0.42))
            sheet.poly([g(Xa, Zf, y_cut), g(Xb, Zf, y_cut), g(Xb, Zf, Yb), g(Xa, Zf, Yb)], c)
        # the band of sun through the cross street, on the front's lower part
        bx0 = max(Xa, CROSS[0] - SUN[0] / SUN[2] * (ZW - Zf))
        bx1 = min(Xb, CROSS[1] - SUN[0] / SUN[2] * (ZW - Zf))
        if bx1 > bx0 and Ya < y_cut:
            sheet.poly([g(bx0, Zf, Ya), g(bx1, Zf, Ya), g(bx1, Zf, min(Yb, y_cut)), g(bx0, Zf, min(Yb, y_cut))], c)
    front_wood = lerp(WOOD_LIT, NAPLES, 0.12)
    lit_or_shade(front_wood, X0, X1, 0, e)
    if kind == "open":
        # the open front: the dark inside (deep: no sun reaches it), the raised floor's edge and its mats, the shelves
        sheet.poly([g(X0 + 14, Zf, 45), g(X1 - 14, Zf, 45), g(X1 - 14, Zf, e - 25), g(X0 + 14, Zf, e - 25)], lerp(PRUSSIAN, WOOD_DARK, 0.30))
        for yv in (110, 150, 190):
            lines.line([g(X0 + 30, Zf - 300, yv), g(X1 - 30, Zf - 300, yv)], lerp(WOOD_SH, PRUSSIAN, 0.2), max(0.7, 3 * CAM.k(X0, Zf)), 0.8)
        for i in range(14):                                    # books and bundles of prints on the shelves, dim
            Xb = X0 + 40 + (X1 - X0 - 80) * (i + 0.5) / 14
            yb = (110, 150, 190)[i % 3]
            p0, p1 = g(Xb, Zf - 300, yb), g(Xb + 14, Zf - 300, yb + 18)
            sheet.poly([p0, (p1[0], p0[1]), p1, (p0[0], p1[1])], lerp([STRAW_SH, INDIGO, WOOD_SH][i % 3], PRUSSIAN, 0.45))
        sheet.poly([g(X0 + 14, Zf - 4, 45), g(X1 - 14, Zf - 4, 45), g(X1 - 14, Zf - 140, 45), g(X0 + 14, Zf - 140, 45)], lerp(VERONESE, STRAW_LIT, 0.55))   # the mats
        lit_or_shade(WOOD, X0 + 14, X1 - 14, 0, 45)              # the floor's front board
        for X in np.linspace(X0 + 14, X1 - 14, 5)[1:-1]:          # the mats' edges
            lines.line([g(X, Zf - 4, 45), g(X, Zf - 140, 45)], lerp(VERONESE, PRUSSIAN, 0.4), 0.6, 0.5)
    elif kind == "lattice":
        sheet.poly([g(X0 + 20, Zf, 40), g(X1 - 20, Zf, 40), g(X1 - 20, Zf, e - 30), g(X0 + 20, Zf, e - 30)], lerp(PRUSSIAN, WOOD_DARK, 0.30))
        lattice(lines, CAM, X0 + 20, X1 - 20, 40, e - 30, Zf + 2, lerp(WOOD_LIT, ULTRA, 0.18), gap=6.0, bar=3.8)
    elif kind == "kelp":
        sheet.poly([g(X0 + 14, Zf, 50), g(X1 - 14, Zf, 50), g(X1 - 14, Zf, e - 25), g(X0 + 14, Zf, e - 25)], lerp(PRUSSIAN, WOOD_DARK, 0.30))
        lit_or_shade(WOOD, X0 + 14, X1 - 14, 0, 50)
    # posts, the sill, the lintel
    for X in (X0 + 5, X1 - 5):
        lines.line([g(X, Zf + 1, 0), g(X, Zf + 1, e)], WOOD_SH, max(1.0, 12 * CAM.k(X, Zf)), 1.0)
    lines.line([g(X0, Zf + 1, e - 25), g(X1, Zf + 1, e - 25)], WOOD_SH, max(1.0, 10 * CAM.k(X1, Zf)), 1.0)
    # the eave of tiles over the ground storey (it faces up and west: lit), its underside a dark band
    roof_slope(sheet, CAM, lines, (X0 - 30, e - 20, Zf + 95), (X1 + 30, e - 20, Zf + 95), (X0 - 30, e + 50, Zf - 10), (X1 + 30, e + 50, Zf - 10))
    sheet.poly([g(X0 - 30, Zf + 95, e - 20), g(X1 + 30, Zf + 95, e - 20), g(X1 + 30, Zf + 60, e - 32), g(X0 - 30, Zf + 60, e - 32)], TILE_DEEP)
    # the upper storey: plaster in the sun, its slatted windows
    Zu = Zf - 30
    sheet.poly([g(X0, Zu, e + 50), g(X1, Zu, e + 50), g(X1, Zu, u), g(X0, Zu, u)], PLASTER_LIT)
    n_win = 2 if X1 - X0 > 330 else 1
    for i in range(n_win):
        cx = X0 + (X1 - X0) * (i + 1) / (n_win + 1)
        a0, a1 = cx - 70, cx + 70
        sheet.poly([g(a0, Zu + 1, e + 90), g(a1, Zu + 1, e + 90), g(a1, Zu + 1, u - 40), g(a0, Zu + 1, u - 40)], lerp(PLASTER_SH, PRUSSIAN, 0.4))
        lattice(lines, CAM, a0 + 6, a1 - 6, e + 90, u - 40, Zu + 2, PLASTER_LIT, gap=7.0, bar=6.5)
        lines.line([g(a0, Zu + 1, e + 90), g(a1, Zu + 1, e + 90), g(a1, Zu + 1, u - 40), g(a0, Zu + 1, u - 40), g(a0, Zu + 1, e + 90)], PRUSSIAN, 0.7, 0.55)
    # the main roof (its slope toward the street lit), the ridge's cap
    mid = Zf - S["depth"] / 2
    roof_slope(sheet, CAM, lines, (X0 - 40, u - 10, Zu + 70), (X1 + 40, u - 10, Zu + 70), (X0 - 40, r, mid), (X1 + 40, r, mid))
    pa, pb = g(X0 - 40, mid, r), g(X1 + 40, mid, r)
    sheet.line([(pa[0], pa[1] - 3), pa, pb, (pb[0], pb[1] - 3)], TILE_DEEP, max(1.4, 14 * CAM.k(X1, mid)))
    # the contour: the silhouette and the corners
    CAM.line(lines, [g(X0, Zf), g(X0, Zf, e)], CAM.depth(X0, Zf))
    CAM.line(lines, [g(X1, Zf), g(X1, Zf, e)], CAM.depth(X1, Zf))
    CAM.line(lines, [g(X0 - 40, Zu + 70, u - 10), g(X0 - 40, mid, r), g(X1 + 40, mid, r), g(X1 + 40, Zu + 70, u - 10)], CAM.depth(X1, Zf))
    out["front"] = [g(X0, Zf), g(X1, Zf), g(X1, Zf, e), g(X0, Zf, e)]
    out["whole"] = [g(X0, Zf), g(X1, Zf), g(X1 + 40, Zu + 70, u - 10), g(X1 + 40, mid, r), g(X0 - 40, mid, r), g(X0 - 40, Zu + 70, u - 10)]
    return out


def under(seed=SEED):
    info = {}
    pic = paint_sky(seed)
    far_roofs(pic, seed)
    s = Paper(SHAPE)
    info["drum"] = drum_tower(s)
    s.onto(pic)
    info["fire"] = paint_cross(pic, seed)
    info["ground"], info["band"] = paint_ground(pic, seed)
    return np.clip(pic, 0, 1), info


# ================================================================ pass 3: the fronts, crisp, and their things
def corner_side(sheet, lines, S):
    """The kelp shop's north side along the cross street (it faces north: in shade), seen past the corner: boards below,
    plaster above, a small barred window; the eave and the roof's end over it."""
    X = S["X0"]
    Za, Zb = ZE, ZE - S["depth"]
    e, u, r = S["eave"], S["upper"], S["ridge"]
    sheet.poly([g(X, Za, 0), g(X, Zb, 0), g(X, Zb, e), g(X, Za, e)], shaded(WOOD, 0.42))
    sheet.poly([g(X, Za - 30, e + 40), g(X, Zb, e + 40), g(X, Zb, u), g(X, Za - 30, u)], PLASTER_SH)
    mid = Za - S["depth"] / 2
    sheet.poly([g(X, Za - 30, u), g(X, Zb, u), g(X, mid, r - 15)], PLASTER_SH)                      # the gable end
    w0, w1 = Za - 220, Za - 330
    sheet.poly([g(X - 1, w0, e + 90), g(X - 1, w1, e + 90), g(X - 1, w1, e + 150), g(X - 1, w0, e + 150)], lerp(PLASTER_SH, PRUSSIAN, 0.45))
    for Zl in np.linspace(w0 - 15, w1 + 15, 4):
        lines.line([g(X - 2, Zl, e + 90), g(X - 2, Zl, e + 150)], PLASTER_SH, 0.8, 0.9)
    for Z in np.linspace(Za, Zb, 6)[1:-1]:
        lines.line([g(X, Z, 0), g(X, Z, e)], WOOD_DARK, 0.6, 0.4)
    # the eave of tiles along the side, and the roof's verge over the gable
    sheet.poly([g(X - 70, Za + 90, e - 15), g(X - 70, Zb, e - 15), g(X + 20, Zb, e + 45), g(X + 20, Za + 90, e + 45)], TILE_SH)
    sheet.line([g(X - 40, Za + 70, u - 10), g(X - 40, mid, r), g(X - 40, Zb - 40, u - 10)], TILE_DEEP, max(1.2, 12 * CAM.k(X, Za)))
    lines.line([g(X, Za, 0), g(X, Zb, 0)], PRUSSIAN, 0.7, 0.5)
    lines.line([g(X, Za, 0), g(X, Za, u)], PRUSSIAN, 0.9, 0.6)


def kelp_goods(sheet, lines, S, rng):
    """The kelp shop's open front: dried kelp in long dark bundles hung from a rail, folded sheets stacked on the floor's
    edge, a tub; Shinsaibashi-suji was a street of kelp shops."""
    X0, X1 = S["X0"] + 30, S["X1"] - 30
    for X in np.linspace(X0 + 20, X1 - 20, 9):
        top = g(X, ZE - 20, 205)
        bot = g(X + rng.uniform(-6, 6), ZE - 20, 110 + rng.uniform(-15, 10))
        k = CAM.k(X, ZE)
        c = lerp(lerp(VIRIDIAN, SIENNA, 0.45), PRUSSIAN, 0.35 + 0.1 * rng.random())
        sheet.poly([(top[0] - 5 * k, top[1]), (top[0] + 5 * k, top[1]), (bot[0] + 7 * k, bot[1]), (bot[0] - 7 * k, bot[1])], c)
    lines.line([g(X0, ZE - 20, 208), g(X1, ZE - 20, 208)], WOOD_SH, max(0.8, 4 * CAM.k(X0, ZE)), 1.0)
    for i in range(4):                                       # folded kelp, stacked
        X = X0 + 30 + i * 50
        CAM.box(sheet, X, X + 40, 45, 60 + i * 3, ZE - 40, ZE - 10, lerp(lerp(VIRIDIAN, SIENNA, 0.4), NAPLES, 0.1), lerp(VIRIDIAN, PRUSSIAN, 0.45))


def medicine_goods(sheet, lines, S):
    """The medicine shop: boxes of medicines on shelves inside the lattice front (seen dark), a hanging lantern-shaped
    sign; its big standing signboard is a cut-out (`sign`)."""
    X0, X1 = S["X0"], S["X1"]
    for j in range(3):
        for i in range(6):
            X = X0 + 40 + i * (X1 - X0 - 80) / 5
            p = g(X, ZE - 60, 70 + j * 40)
            k = CAM.k(X, ZE)
            sheet.poly([(p[0] - 6 * k, p[1]), (p[0] + 6 * k, p[1]), (p[0] + 6 * k, p[1] - 14 * k), (p[0] - 6 * k, p[1] - 14 * k)], lerp([STRAW_SH, lerp(VERMILION, SIENNA, 0.5), PLASTER_SH][(i + j) % 3], PRUSSIAN, 0.5))


def comb_sign(sheet, lines, S):
    """The comb-maker's signboard: a big wooden comb, hung from a bracket under the eave out over the street (a sign
    shaped like the goods, as a comb-maker's was), its teeth drawn; the bracket and its cords."""
    X = S["X0"] + 70
    Z = ZE + 110
    k = CAM.k(X, Z)
    top = g(X, Z, 238)
    w, hh = 82 * k, 36 * k
    cx, cy = top[0], top[1] + 4
    back = [(cx - w / 2, cy + hh * 0.35)] + [(cx - w / 2 + w * i / 10, cy - hh * 0.3 * math.sin(math.pi * i / 10)) for i in range(11)] + [(cx + w / 2, cy + hh * 0.35)]
    body = back + [(cx + w / 2, cy + hh), (cx - w / 2, cy + hh)]
    sheet.poly(body, lerp(OCHRE, NAPLES, 0.35))
    sheet.poly([(cx - w / 2, cy + hh * 0.35), (cx + w / 2, cy + hh * 0.35), (cx + w / 2, cy + hh * 0.45), (cx - w / 2, cy + hh * 0.45)], lerp(OCHRE, SIENNA, 0.35))
    for i in range(1, 24):                                   # the teeth
        x = cx - w / 2 + w * i / 24
        sheet.line([(x, cy + hh * 0.48), (x, cy + hh)], lerp(OCHRE, SIENNA, 0.55), max(0.6, 1.2 * k), 0.95)
    lines.line(body + [body[0]], PRUSSIAN, 0.9, 0.7)
    br0, br1 = g(S["X0"] + 20, ZE + 10, 248), g(X, Z, 248)
    lines.line([br0, (br1[0], br1[1])], WOOD_SH, max(1.0, 4 * k), 1.0)
    lines.line([(cx - w * 0.35, br1[1]), (cx - w * 0.35, cy - hh * 0.2)], PRUSSIAN, 0.6, 0.8)
    lines.line([(cx + w * 0.35, br1[1]), (cx + w * 0.35, cy - hh * 0.2)], PRUSSIAN, 0.6, 0.8)
    return [int(cx - w / 2) - 3, int(br1[1]) - 3, int(w) + 6, int(cy + hh - br1[1]) + 6]


def hanging_sign(sheet, lines, X, Z, top_y, bot_y, rng, wid=28.0):
    """A shop's hanging signboard under the eave: a long board with its name as the shape of writing (no real name)."""
    a, b = g(X, Z, top_y), g(X, Z, bot_y)
    k = CAM.k(X, Z)
    w = wid * k
    sheet.poly([(a[0] - w / 2, a[1]), (a[0] + w / 2, a[1]), (b[0] + w / 2, b[1]), (b[0] - w / 2, b[1])], lerp(WOOD_LIT, NAPLES, 0.25))
    writing(sheet, (a[0], a[1] + 3), (b[0], b[1] - 2), rng, PRUSSIAN, max(0.7, 1.4 * k), 0.9)
    lines.line([(a[0] - w / 2, a[1]), (a[0] + w / 2, a[1]), (b[0] + w / 2, b[1]), (b[0] - w / 2, b[1]), (a[0] - w / 2, a[1])], PRUSSIAN, 0.8, 0.6)
    return [int(a[0] - w / 2) - 2, int(a[1]) - 2, int(w) + 4, int(b[1] - a[1]) + 4]


def details(pic, info, seed=SEED, fast=False):
    x, y = grid(SHAPE)
    rng = np.random.default_rng(seed + 50)
    sheet = Paper(SHAPE)
    lines = sheet
    # the far fronts, the farthest (right) first
    for S in BEYOND[::-1]:
        shop_front(sheet, lines, S, ["lattice", "shutters", "lattice"][BEYOND.index(S)], rng)
    info["comb"] = shop_front(sheet, lines, COMB, "lattice", rng)
    info["med"] = shop_front(sheet, lines, MED, "lattice", rng)
    medicine_goods(sheet, lines, MED)
    corner_side(sheet, lines, KELP)
    info["kelp"] = shop_front(sheet, lines, KELP, "kelp", rng)
    kelp_goods(sheet, lines, KELP, rng)
    info["print"] = shop_front(sheet, lines, PRINT, "open", rng)
    # the signs: the print shop's (a publisher's name, as the shape of writing), the kelp shop's, the comb-maker's comb
    info["printsign"] = hanging_sign(sheet, lines, PRINT["X1"] - 30, ZE + 30, 236, 120, np.random.default_rng(11), wid=30.0)
    info["kelpsign"] = hanging_sign(sheet, lines, KELP["X1"] - 40, ZE + 30, 236, 130, np.random.default_rng(12), wid=28.0)
    info["combsign"] = comb_sign(sheet, lines, COMB)
    sheet.onto(pic)
    return pic


# ================================================================ the cut-outs and their states
ORDER = ["prints-1", "prints-2", "noren-kelp", "noren-med", "noren-comb", "bench", "print", "sign", "roadgod", "watervendor"]


def cutouts(pic, info, fast=False):
    import edo_street_things as T
    planes, extra = {}, {}

    def made(name, sl, seed, keep=0.5, sizes=(6, 3, 2), under=None):
        s_, l_ = sl[0], sl[1]
        c, a = s_.done()
        lc, la = l_.done()
        planes[name] = brushed(c, a, lc, la, under if under is not None else under_colour(pic, np.maximum(a, la), EARTH), seed=seed, sizes=sizes, keep=keep, fast=fast)

    r = T.print_line(1, PRINT["X0"] + 30, PRINT["X1"] - 24, 212.0, ["1", "0", "toy", "2", "4", "0", "3"], 41)
    made("prints-1", r, 41, keep=0.75, sizes=(3, 2))
    extra["prints-1"] = r[2]
    r = T.print_line(2, PRINT["X0"] + 40, PRINT["X0"] + 230, 176.0, ["toy", "3", "0", "toy"], 42)
    made("prints-2", r, 42, keep=0.75, sizes=(3, 2))
    extra["prints-2"] = r[2]
    made("noren-kelp", T.noren(KELP["X0"] + 20, KELP["X1"] - 20, 228.0, 52.0, "bars", 51, panels=5), 51, keep=0.6)
    made("noren-med", T.noren(MED["X0"] + 26, MED["X0"] + 150, 214.0, 86.0, "lozenge", 52, panels=2), 52, keep=0.6)
    made("noren-comb", T.noren(COMB["X0"] + 120, COMB["X1"] - 30, 214.0, 80.0, "ring", 53, panels=3, c=lerp(INDIGO, VIRIDIAN, 0.25)), 53, keep=0.6)
    r = T.bench()
    made("bench", r, 54, keep=0.7, sizes=(3, 2))
    extra["bench"] = r[2]
    for st, name in (("blank", "print"), ("ghost", "print-ghost"), ("clean", "print-clean")):
        made(name, T.sheet_on_stand(st, extra["bench"]), 55, keep=0.85, sizes=(2,))
    r = T.signboard()
    made("sign", r, 56, keep=0.7, sizes=(3, 2))
    extra["sign"] = r[2]
    r = T.roadgod()
    made("roadgod", r, 57, keep=0.6, sizes=(3, 2))
    extra["roadgod"] = r[2]
    r = T.watervendor()
    made("watervendor", r, 58, keep=0.6, sizes=(3, 2))
    extra["watervendor"] = r[2]
    return planes, extra


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = "fast" in sys.argv or "layout" in sys.argv          # layout: the fast passes (the same geometry and boxes), layout.json only
    base, info = under()
    Image.fromarray((base * 255).astype(np.uint8)).save(OUT + "-1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.26)
    details(pic, info, fast=fast)
    print("details", round(time.time() - t0, 1), "shade line", round(SHADE_Y))
    planes, extra = cutouts(pic, info, fast)
    whole = pic.copy()
    for name in ORDER:
        c, a = planes[name]
        over(whole, c, (a > 0.5).astype(F32))
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-all.png")
    print("cut-outs", round(time.time() - t0, 1))
    if "layout" in sys.argv:
        import edo_street_layout as L
        with open(OUT + "/layout.json", "w") as f:
            json.dump(L.layout(planes, extra, info), f, indent=1)
        print("layout.json only")
        sys.exit()
    if fast:
        sys.exit()
    for f in os.listdir(OUT):
        if f.endswith(".png"):
            os.remove(os.path.join(OUT, f))
    print("back", finish(pic, OUT + "/back.png", 152))
    sizes = {"prints-1": 64, "prints-2": 48, "noren-kelp": 32, "noren-med": 32, "noren-comb": 32, "bench": 48, "print": 24, "print-ghost": 32,
             "print-clean": 32, "sign": 40, "roadgod": 32, "watervendor": 48}
    for name, (c, a) in planes.items():
        print(name, finish(c, f"{OUT}/{name}.png", sizes.get(name, 48), a))
    import edo_street_layout as L
    lay = L.layout(planes, extra, info)
    with open(OUT + "/layout.json", "w") as f:
        json.dump(lay, f, indent=1)
    comp = Image.open(OUT + "/back.png").convert("RGBA")
    for name in ORDER:
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(OUT + "-comp.png")
    print("done", round(time.time() - t0, 1))

"""The foot of Mount Shosha (edo-shosha): the women's hall of Engyo-ji, about 29 April 1830, late afternoon and then
sunset. The measurements, the camera, the two lights and their colours. PAINT-21E, round twenty-one.

PLAN
  The place  The east path's foot, where women stopped: the women's hall (today's Nyoirin-ji; what it looked like in 1830
             is not recorded: a small deep-roofed hall on a low stone base, its double doors latticed, a lattice window in
             its west side, is the game's). The mountain rises behind it and to the left, pines and maples in new leaf, a
             late cherry in the shade; the east path climbs into the trees by stone steps and is gone; at its foot a small
             stone that says women may not pass (such stones stood at many barred mountains; this one is the game's, its
             writing our own marks). O-Ume's thatched hut at the right, a lantern on its hook; the bench where the women
             wait; their failed combs and hairpins in a heap on a cloth. Beyond the terrace's edge at the right, far below,
             the Harima plain, and on its hill, small and white, the castle (it lies south-east of the hall: the picture
             puts the mountain at its left and the plain at its right, a liberty of the prints' kind, said in ready.md).
  Light      Two states, the same geometry. GOLD: the late afternoon sun from the left and a little behind us (about 30
             degrees up): the hall's west side glows, its front takes the light at a slant, the shadows lie to the right
             and a little away. SUNSET: the sun low at the left, going down behind the trees on the mountain's flank (7
             degrees up, a little beyond the hall): the west side red, the front in blue shade, the trees' long shadows
             reaching right and toward us across the terrace, the sky in bands of chrome orange and geranium lake (the
             act's one licence for them), the plain in the blue of the evening.
  Depth      The land camera: horizon 280, full 590 (the lens 3.39 m above the terrace, level, focal 800), its vanishing
             point at x 400. The hall's front corner stands 14.5 m off (row 467), the hall turned 22 degrees so that its
             west side shows. Everything in centimetres in the world (X across, Y up, D from the lens)."""

import math

import numpy as np

from edo_town_kit import (PAINT, PAPER, LINE, mix, shade_of, col)

W, H = 800, 600
SHAPE = (H, W)
HZ, FULL = 280, 590
FOC = 800.0
VX = 400.0
S0 = 160.0 / 175.0
EYE = (FULL - HZ) / S0                                       # 339.1 cm
OUT = "out/edo-shosha"


def P(X, Y, D):
    k = FOC / D
    return (VX + X * k, HZ + (EYE - Y) * k)


def k_at(D):
    return FOC / D


def D_row(y):
    return EYE * FOC / max(y - HZ, 0.5)


def row_D(D):
    return HZ + EYE * FOC / D


def scale_at(y):
    return (y - HZ) / (FULL - HZ)


# ---------------------------------------------------------------- the hall: a square plan turned 22 degrees
THETA = math.radians(22.0)
UX, UD = math.cos(THETA), math.sin(THETA)                    # along the front, left to right (the right end farther)
VXH, VDH = -math.sin(THETA), math.cos(THETA)                 # into the hall, away from us (and to the left)
FL = (-62.0, 1450.0)                                         # the front-left corner of the walls (X, D)
SIDE = 360.0                                                 # the walls: 2 ken square
BASE_H = 40.0                                                # the low stone base
EAVE_Y, EAVE_OUT, APEX_Y, FINIAL_Y = 300.0, 112.0, 540.0, 620.0
DOOR_A = (96.0, 264.0)                                       # the double doors along the front (a), from the floor
DOOR_Y = (52.0, 246.0)
LATTICE_B = (124.0, 236.0)                                   # the west side's lattice window along the side (b)
LATTICE_Y = (118.0, 214.0)


def H_(a, b):
    """A place in the hall's own measure (a along the front from its left corner, b in from the front) -> (X, D)."""
    return (FL[0] + a * UX + b * VXH, FL[1] + a * UD + b * VDH)


def HP(a, b, y):
    X, D = H_(a, b)
    return P(X, y, D)


# ---------------------------------------------------------------- the two lights
SUN = {
    # toward the sun: (across: negative is left, up, depth: negative is toward us)
    "gold": (-0.78, 0.52, -0.34),
    "sunset": (-0.95, 0.12, 0.29),
}


def unit(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def cast_of(light):
    """A shadow on the ground per cm of height: (across, away)."""
    sx, sy, sd = unit(SUN[light])
    return (-sx / sy, -sd / sy)


def lit_of(light, normal):
    """How much a face is lit (0 to 1) by the light's sun, given its outward normal (X, Y, D)."""
    s = unit(SUN[light])
    n = unit(normal)
    return max(0.0, s[0] * n[0] + s[1] * n[1] + s[2] * n[2])


N_FRONT = (math.sin(THETA), 0.0, -math.cos(THETA))           # the hall's front faces us and a little right
N_WEST = (-math.cos(THETA), 0.0, -math.sin(THETA))           # its west side faces left and a little toward us


def palette(light):
    """The colours of each light, mixed from the box by name (style.md section 2)."""
    P_ = PAINT
    if light == "gold":
        sun = mix(P_["naples"], PAPER, 0.35)
        L = dict(
            sky=[mix(P_["cobalt"], P_["prussian"], 0.38), mix(P_["cobalt"], P_["prussian"], 0.12), P_["cobalt"], mix(P_["cobalt"], P_["cerulean"], 0.55),
                 P_["cerulean"], mix(P_["cerulean"], PAPER, 0.5), mix(PAPER, P_["naples"], 0.35), mix(P_["naples"], PAPER, 0.25)],
            sun=sun, light_amt=1.0,
            wood=mix(P_["sienna"], P_["ochre"], 0.42), wood_lit=mix(mix(P_["ochre"], P_["naples"], 0.35), P_["sienna"], 0.12),
            wood_sh=shade_of(mix(P_["sienna"], P_["ochre"], 0.3), 0.40), wood_dark=mix(P_["sienna"], P_["prussian"], 0.55),
            tile=mix(P_["prussian"], "#6f7890", 0.40), tile_lit=mix(mix("#8c96ae", PAPER, 0.25), P_["naples"], 0.25), tile_sh=mix(P_["prussian"], P_["ultra"], 0.25),
            tile_edge=mix("#9aa4bc", PAPER, 0.3),
            stone=mix(PAPER, P_["prussian"], 0.26), stone_lit=mix(mix(PAPER, P_["naples"], 0.35), P_["prussian"], 0.08), stone_sh=shade_of(mix(PAPER, P_["prussian"], 0.25), 0.40),
            ground=mix(mix(P_["ochre"], PAPER, 0.58), P_["naples"], 0.12), ground_lit=mix(P_["naples"], PAPER, 0.38), ground_sh=shade_of(mix(P_["ochre"], PAPER, 0.5), 0.48),
            grass=mix(P_["veronese"], P_["ochre"], 0.25), grass_lit=mix(P_["veronese"], P_["naples"], 0.4), grass_sh=mix(P_["viridian"], P_["veronese"], 0.4),
            pine=mix(P_["viridian"], P_["prussian"], 0.38), pine_lit=mix(P_["viridian"], P_["naples"], 0.30), pine_far=mix(P_["viridian"], P_["cerulean"], 0.42),
            maple=mix(P_["veronese"], P_["naples"], 0.18), maple_lit=mix(P_["veronese"], P_["naples"], 0.55), maple_sh=mix(P_["viridian"], P_["veronese"], 0.45),
            cherry=mix(PAPER, P_["lake"], 0.30), cherry_sh=mix(mix(PAPER, P_["lake"], 0.42), P_["cobalt"], 0.18),
            trunk=mix(P_["sienna"], P_["prussian"], 0.45), trunk_lit=mix(P_["sienna"], P_["ochre"], 0.35),
            mount=mix(P_["viridian"], P_["prussian"], 0.28), mount_far=mix(mix(P_["viridian"], P_["cerulean"], 0.5), PAPER, 0.25),
            mist=mix(PAPER, P_["naples"], 0.30),
            glade=[mix(mix(P_["viridian"], P_["cerulean"], 0.5), PAPER, 0.35), mix(mix(P_["veronese"], PAPER, 0.4), P_["naples"], 0.2), mix(PAPER, P_["naples"], 0.38),
                   mix(PAPER, P_["naples"], 0.5), mix(P_["naples"], PAPER, 0.25), mix(P_["naples"], PAPER, 0.15)],
            plain=[mix(mix(P_["veronese"], P_["cerulean"], 0.5), PAPER, 0.45), mix(mix(P_["veronese"], P_["cerulean"], 0.35), PAPER, 0.3),
                   mix(P_["veronese"], P_["ochre"], 0.25), mix(P_["veronese"], P_["viridian"], 0.25)],
            far_hills=mix(P_["cerulean"], PAPER, 0.48), river=mix(PAPER, P_["cerulean"], 0.35),
            castle=mix(PAPER, P_["naples"], 0.15), castle_roof=mix(P_["prussian"], P_["cerulean"], 0.35),
            paper=mix(PAPER, P_["naples"], 0.12), paper_old=mix(PAPER, P_["ochre"], 0.25), ink=LINE,
            inside=mix(P_["prussian"], P_["sienna"], 0.30), inside_far=mix(P_["prussian"], P_["ultra"], 0.35),
            bar=mix(P_["naples"], PAPER, 0.35),                    # the bars of light inside (seen through the open doors)
            thatch=mix(mix(P_["ochre"], P_["sienna"], 0.55), P_["prussian"], 0.12), thatch_lit=mix(mix(P_["ochre"], P_["sienna"], 0.3), P_["naples"], 0.2),
            thatch_sh=shade_of(mix(P_["ochre"], P_["sienna"], 0.5), 0.42),
            plaster=mix(PAPER, P_["ochre"], 0.22), plaster_sh=shade_of(mix(PAPER, P_["ochre"], 0.2), 0.42),
            cast=mix(P_["cobalt"], P_["ultra"], 0.35), cast_amt=0.42,
            lantern=mix(PAPER, P_["naples"], 0.1), cloth=mix(P_["ultra"], PAPER, 0.35), rice=PAPER, leaf=mix(P_["viridian"], P_["veronese"], 0.35),
            boxwood=mix(P_["ochre"], P_["naples"], 0.35), shell=mix(P_["sienna"], P_["ochre"], 0.25), lacquer=mix(P_["prussian"], "#000000", 0.35), red=P_["vermilion"],
        )
    else:
        red = mix(P_["vermilion"], P_["orange"], 0.45)
        L = dict(
            sky=[mix(P_["ultra"], P_["prussian"], 0.45), P_["ultra"], mix(P_["ultra"], P_["lake"], 0.22), mix(P_["lake"], P_["ultra"], 0.35),
                 mix(P_["lake"], PAPER, 0.25), mix(mix(P_["lake"], P_["orange"], 0.35), PAPER, 0.25), mix(P_["orange"], PAPER, 0.35), mix(P_["naples"], PAPER, 0.35)],
            glade=[mix(P_["lake"], P_["ultra"], 0.25), mix(P_["vermilion"], P_["lake"], 0.35), mix(P_["orange"], P_["vermilion"], 0.35), P_["orange"],
                   mix(P_["orange"], P_["naples"], 0.45), mix(P_["naples"], PAPER, 0.35)],
            sun=red, light_amt=1.0,
            wood=shade_of(mix(P_["sienna"], P_["ochre"], 0.25), 0.55), wood_lit=mix(mix(P_["sienna"], red, 0.55), P_["orange"], 0.25),
            wood_sh=mix(shade_of(mix(P_["sienna"], P_["ochre"], 0.2), 0.62), P_["prussian"], 0.15), wood_dark=mix(P_["prussian"], P_["sienna"], 0.30),
            tile=mix(P_["prussian"], P_["ultra"], 0.30), tile_lit=mix(mix("#8c96ae", P_["lake"], 0.45), P_["orange"], 0.25), tile_sh=mix(P_["prussian"], P_["ultra"], 0.15),
            tile_edge=mix(mix("#9aa4bc", P_["lake"], 0.35), PAPER, 0.15),
            stone=mix(mix(PAPER, P_["prussian"], 0.38), P_["ultra"], 0.20), stone_lit=mix(mix(PAPER, P_["orange"], 0.55), P_["lake"], 0.12),
            stone_sh=mix(mix(P_["ultra"], P_["prussian"], 0.3), mix(PAPER, P_["lake"], 0.3), 0.28),
            ground=mix(mix(P_["ochre"], P_["lake"], 0.25), P_["ultra"], 0.30), ground_lit=mix(mix(P_["orange"], PAPER, 0.35), P_["lake"], 0.15),
            ground_sh=mix(P_["ultra"], P_["cobalt"], 0.35),
            grass=mix(mix(P_["viridian"], P_["veronese"], 0.4), P_["ultra"], 0.25), grass_lit=mix(P_["veronese"], P_["orange"], 0.45), grass_sh=mix(P_["viridian"], P_["prussian"], 0.45),
            pine=mix(P_["prussian"], P_["viridian"], 0.30), pine_lit=mix(mix(P_["viridian"], P_["orange"], 0.45), P_["lake"], 0.15), pine_far=mix(P_["ultra"], P_["lake"], 0.25),
            maple=mix(mix(P_["viridian"], P_["veronese"], 0.4), P_["ultra"], 0.25), maple_lit=mix(P_["veronese"], P_["orange"], 0.55), maple_sh=mix(P_["viridian"], P_["prussian"], 0.40),
            cherry=mix(mix(PAPER, P_["lake"], 0.42), P_["ultra"], 0.20), cherry_sh=mix(mix(PAPER, P_["lake"], 0.45), P_["ultra"], 0.40),
            trunk=mix(P_["prussian"], P_["sienna"], 0.30), trunk_lit=mix(P_["sienna"], red, 0.55),
            mount=mix(P_["prussian"], P_["viridian"], 0.22), mount_far=mix(mix(P_["ultra"], P_["lake"], 0.25), PAPER, 0.25),
            mist=mix(mix(PAPER, P_["lake"], 0.35), P_["orange"], 0.25),
            plain=[mix(mix(P_["lake"], PAPER, 0.5), P_["ultra"], 0.2), mix(mix(P_["lake"], P_["viridian"], 0.45), PAPER, 0.25),
                   mix(mix(P_["viridian"], P_["lake"], 0.3), P_["ultra"], 0.25), mix(mix(P_["viridian"], P_["sienna"], 0.3), P_["ultra"], 0.35)],
            far_hills=mix(mix(P_["lake"], PAPER, 0.5), P_["cobalt"], 0.2), river=mix(mix(PAPER, P_["lake"], 0.35), P_["orange"], 0.15),
            castle=mix(mix(PAPER, P_["lake"], 0.25), P_["orange"], 0.15), castle_roof=mix(P_["ultra"], P_["prussian"], 0.25),
            paper=mix(mix(PAPER, P_["lake"], 0.12), P_["ultra"], 0.22), paper_old=mix(mix(PAPER, P_["ochre"], 0.25), P_["ultra"], 0.28), ink=LINE,
            inside=mix(P_["prussian"], P_["sienna"], 0.22), inside_far=mix(P_["prussian"], P_["ultra"], 0.40),
            bar=mix(mix(P_["orange"], P_["lake"], 0.35), PAPER, 0.15),
            thatch=mix(mix(P_["ochre"], P_["sienna"], 0.3), P_["ultra"], 0.35), thatch_lit=mix(P_["orange"], P_["ochre"], 0.35), thatch_sh=mix(P_["ultra"], P_["sienna"], 0.30),
            plaster=mix(mix(PAPER, P_["lake"], 0.15), P_["ultra"], 0.25), plaster_sh=mix(P_["ultra"], PAPER, 0.25),
            cast=mix(P_["ultra"], P_["prussian"], 0.35), cast_amt=0.50,
            lantern=mix(mix(PAPER, P_["orange"], 0.20), P_["ultra"], 0.15), cloth=mix(P_["ultra"], P_["prussian"], 0.25), rice=mix(PAPER, P_["lake"], 0.12), leaf=mix(P_["viridian"], P_["prussian"], 0.35),
            boxwood=mix(P_["ochre"], P_["lake"], 0.30), shell=mix(P_["sienna"], P_["prussian"], 0.35), lacquer=mix(P_["prussian"], "#000000", 0.35), red=P_["vermilion"],
        )
    L["line"] = LINE
    return L


def face_colour(L, base, base_lit, base_sh, light, normal):
    """A face's flat colour in a light: its lit flat, its shade flat, or between (two flats, never a gradient)."""
    t = lit_of(light, normal)
    if t > 0.55:
        return base_lit
    if t > 0.18:
        return mix(base, base_lit, 0.35)
    if t > 0.0:
        return base
    return base_sh

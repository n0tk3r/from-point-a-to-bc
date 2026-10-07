"""Rome, the Ides of March, 44 B.C.: the steps of the old temple that is also the treasury of the
Roman People, seen from the Forum pavement on a fine morning.

PLAN
  Light     Morning sun from the upper right, a little toward us: SUN below. Everything that faces right
            is warm and bright, every front is dimmer but still warm, every left side is in cool blue-violet
            shade, and shadows on the ground run to the LEFT (1.2 times as long as the thing is tall).
  Depth     horizon 260, full 590 (persp.Camera, so the game's people fit). The temple stands at an angle
            of 18 degrees (Frame T): its front runs away to the right, its left flank away to the left.
            Its porch is 252 cm up (fourteen steps of 18), so we just look down on the porch floor.
  Tones     LIGHT  the sunlit steps, the right side of every column, the cloud.
            DARK   the porch behind the columns and the open doorway in it (darkest); the laurel at the front.
            MIDDLE the blue sky, the golden paving, the temple's violet shadow, the Forum pale in its haze.
            The eye goes up the bright steps to the dark doorway between two lit columns.
  Places    temple: right two thirds; its corner column at x 358, six columns to x 779.
            steps: 14, from the pavement (y 462 at their left end, 433 at the right edge) to the porch (y 300).
            doors: open, seen between the second and third columns, about (477 to 530, 149 to 293).
            Forum, hill and sky: left of x 240.   altar: about (285, 505).   tripod: about (380, 491).
            the soothsayer's cage of hens: on the fourth step, x 446 to 478, y 380 to 410; he sits just right of it.
            boundary stone: about (700, 554).   front plane: statue base and laurel, bottom left.

The picture is a backdrop and five cut-outs: the six columns of the front (people on the porch pass
behind them), the altar, the tripod, the boundary stone, and the statue base and laurel at the very front.

RETOUCHED since it was first finished: a folding stool and a staff stood on the steps by the cage. They
were taken out (the game draws the soothsayer with his own staff, sitting on the step itself). So that
nothing else in the picture moved, the first lay-in under the brushwork is still painted as it was, with
the stool's shadow in it (temple_layers(stool=True)), that shadow is painted out on top (details), and the
backdrop keeps the palette it was first given (rome_steps_palette.py).

  python3 rome_steps.py         paints everything into out/rome-steps/ and lays it together as out/rome-steps-comp.png
  python3 rome_steps.py fast    skips the brush pass and the palette: out/rome-steps-2-all.png only
  (rome_steps_kit.py holds the tools; rome_steps_check.py draws layout.json over the picture.)"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
import land
import letter
import sky
from persp import Camera
from rome_steps_kit import *
from rome_steps_palette import PALETTE

W, H = 800, 600
SHAPE = (H, W)
HZ, FULL = 260, 590
CAM = Camera(HZ, FULL)
OUT = "out/rome-steps"
KEEP = "out/rome-steps-kept"                                 # layers kept between runs while the rest is worked on

T = Frame(CAM, 18.0, 330, 1930)                              # the temple
SUN = unit((0.76, 0.62, -0.10))                              # toward the sun: (to the right, up, away from us)
LIT = Light(SUN)
SU, SV, SH = T.to_frame(SUN)                                 # the same, along the temple's front, into it, and up
SKY_LIGHT = (0.62, -0.78)                                    # toward the sun in the picture, for the clouds
CAST = (-SUN[0] / SUN[1], -SUN[2] / SUN[1])                  # where a shadow falls on the ground, per cm of height: (across, away)

# ---- the temple's measurements, in cm (u along the front, v back into it, h up from the pavement)
HP = 252.0                                                   # the porch floor: fourteen steps of 18
RISE, TREAD, NSTEP = 18.0, 38.0, 14
EDGE = -60.0                                                 # the front edge of the porch floor
GAP = 255.0
COLS = [70.0 + GAP * i for i in range(6)]                    # the six columns of the front stand on v = 0
UW = COLS[-1] + 70.0                                         # the width of the front
SU0, SU1 = 90.0, UW - 90.0                                   # the steps run between these
HC = 610.0                                                   # a column, base to abacus
TOP = HP + HC
DEEP = 520.0                                                 # the wall with the door
BACK = 1900.0
FLANK_COL = (70.0, GAP)
DOOR = (UW / 2 - 95.0, UW / 2 + 95.0, HP + 8.0, HP + 478.0)  # the opening: u0, u1, h0, h1
ARCH, FRIEZE, CORN = 66.0, 56.0, 28.0                        # the beam over the columns, the band above it, the gutter's face
EAVE = 30.0                                                  # how far the gutter stands out
PITCH = math.tan(math.radians(17))
E0, E1, E2, E3 = HP + HC, HP + HC + ARCH, HP + HC + ARCH + FRIEZE, HP + HC + ARCH + FRIEZE + CORN     # the levels of the roof front
FU, FV = 34.0, -36.0                                         # the faces of the beam: on the flank, on the front

STUCCO, RED, DADO = "#f1e4c6", "#a8553c", "#8f4338"
TUFA, TRAV = "#c9b592", "#f2ead8"
PAVE = "#e2d8c4"
NEIGHBOUR = (1900.0, 350.0, 3200.0, 1040.0)                 # the blank side wall of the next building: u, v0, v1, height
CLAY, WOOD = "#cf7a4a", "#8a5a3a"
BRONZE, PATINA = "#a67c3a", "#5d8b78"
P_RED, P_BLACK, P_CREAM, P_BLUE, P_OCHRE = "#a8382b", "#2f2a33", "#f0e2c0", "#3d6f96", "#d9a441"


def VK(k):
    """How far back the riser of step k stands (k = 1 at the pavement, 14 at the porch)."""
    return EDGE - (NSTEP - k) * TREAD


def slabs(u, ppc, seed, long=150.0, joint=1.4):
    """Joints across a single course of stone: -> (a number for each slab, joint mask)."""
    q = u / long + (seed * 0.618) % 1 * 5
    i = np.floor(q)
    j0 = (hash2(i, seed, 11) - 0.5) * 0.4
    j1 = (hash2(i + 1, seed, 11) - 0.5) * 0.4
    fa = q - i
    left, right = fa - j0, 1 + j1 - fa
    block = np.where(left < 0, i - 1, np.where(right < 0, i + 1, i))
    d = np.minimum(np.abs(left), np.abs(right)) * long
    w = np.maximum(joint, 0.8 / np.maximum(ppc, 1e-4))
    jm = np.clip(1.5 - d / (w * 0.5), 0, 1) * np.clip(ppc * joint / 0.55, 0, 1)
    return hash2(block, seed, 13), jm.astype(F32)


def plaster(a, b, ppc, seed, dado=150.0, cream=STUCCO, red=DADO, lost=0.16):
    """Painted plaster in the old manner: a deep red dado, a pale band, and above it big blocks drawn in the
    plaster itself. Rain marks, damp, and patches where it has come away from the rubble wall behind.
    `b` is the height above the floor the wall stands on."""
    tone, jm, above = courses(a, b - dado - 14, long=150, high=66, seed=seed, joint=1.3, ppc=ppc)
    c = col(cream)[None, None, :] * (1 + (tone[..., None] - 0.5) * 0.09)
    c = c * (1 - 0.30 * jm[..., None]) * (1 + 0.07 * above[..., None])
    band = (b > dado) & (b <= dado + 14)
    c = np.where(band[..., None], col(cream) * 1.03, c)
    line = np.clip(1.5 - np.abs(b - dado - 14) / 1.4, 0, 1) + np.clip(1.5 - np.abs(b - dado) / 1.4, 0, 1)
    c = c * (1 - 0.35 * np.clip(line, 0, 1)[..., None])
    low = b <= dado
    panel = np.clip(1.5 - np.abs(((a + 40) % 190.0) - 95.0 - 86) / 1.6, 0, 1) * low     # thin pale lines divide the dado into panels
    r = col(red)[None, None, :] * (1 + (tex(a, b, 70, seed + 9)[..., None] - 0.5) * 0.22)
    r = r * (1 - 0.5 * panel[..., None]) + col(cream) * 0.5 * panel[..., None]
    c = np.where(low[..., None], r, c)
    c = c * (1 + (tex(a, b, 320, seed + 2)[..., None] - 0.5) * 0.16 + (tex(a, b, 45, seed + 3)[..., None] - 0.5) * 0.07)
    rain = step(0.56, 0.88, tex(a * 7.0, b * 0.5, 120, seed + 4)) * np.clip((b - 60) / 300.0, 0, 1)      # marks run down from the top
    c = c * (1 - 0.13 * rain[..., None])
    damp = np.clip(1 - b / 55.0, 0, 1) * (0.5 + tex(a, b, 60, seed + 5))
    c = c * (1 - 0.22 * np.clip(damp, 0, 1)[..., None] * np.array([1.0, 0.9, 0.95], dtype=F32))
    gone = holes(a, b, seed + 7, cell=120.0, amount=lost + 0.10 * np.clip(1 - b / 120.0, 0, 1))
    rubble = mix("#a8927a", "#7c6c62", 0.0)[None, None, :] * (0.78 + 0.5 * tex(a, b, 13, seed + 8, 3)[..., None])
    lip = np.clip(holes(a + 2.2, b + 2.2, seed + 7, cell=120.0, amount=lost) - gone, 0, 1)     # the plaster's own edge, in shadow
    c = c * (1 - gone[..., None]) + rubble * gone[..., None]
    c = c * (1 - 0.35 * lip[..., None])
    return np.clip(c, 0, 1).astype(F32)


def revet(a, b, seed=0):
    """The painted terracotta that covers the beam over the columns: b runs 0 (bottom) to ARCH (top).
    From the bottom: a black band with pale dots, a meander, a chain of palmettes and lotus buds on red,
    and tongues along the top. Plaques 64 cm wide, nailed."""
    c = np.empty(a.shape + (3,), dtype=F32)
    c[...] = col(P_RED)
    # the palmettes: one every 32 cm, standing up, and a dark bud hanging between each two
    cell = np.floor(a / 16.0)
    x = (a % 16.0) - 8.0
    y = b - 19.0
    even = (cell % 2) == 0
    r = np.hypot(x, y - 1.5)
    ang = np.arctan2(x, y - 1.5)
    fan = (r < 27.0 * (0.50 + 0.50 * np.cos(ang * 4.0) ** 2)) & (np.abs(ang) < 1.5) & (r > 3.0) & (y > 0)
    yy = 33.0 - y
    bud = ((x / 3.6) ** 2 + ((yy - 12.0) / 11.0) ** 2 < 1) & (y > 0)
    stalk = (np.abs(x) < 0.9) & (yy < 4) & (y > 0)
    field = (b > 19) & (b < 52)
    c = np.where((field & even & fan)[..., None], col(P_CREAM), c)
    c = np.where((field & ~even & (bud | stalk))[..., None], col(P_BLUE) * 0.9, c)
    heart = field & even & (r < 4.5) & (y > 0)
    c = np.where(heart[..., None], col(P_OCHRE), c)
    # the meander below: a square wave of black on cream
    t = (a % 14.0) / 14.0
    hh = (b - 8.0) / 9.0
    m = (((t < 0.5) & (np.abs(hh - 0.72) < 0.16)) | ((t >= 0.5) & (np.abs(hh - 0.28) < 0.16)) | ((np.abs(t - 0.5) < 0.09) | (t < 0.09) | (t > 0.91)) & (hh > 0.12) & (hh < 0.88))
    c = np.where(((b >= 8) & (b < 17))[..., None], np.where(m[..., None], col(P_BLACK), col(P_CREAM)), c)
    c = np.where(((b >= 17) & (b < 19))[..., None], col(P_BLACK), c)
    dots = (np.hypot((a % 8.0) - 4.0, b - 4.0) < 1.7)
    c = np.where((b < 8)[..., None], np.where(dots[..., None], col(P_CREAM), col(P_BLACK)), c)
    # tongues along the top: red and blue by turns, on cream
    c = np.where(((b >= 52) & (b < 55))[..., None], col(P_CREAM), c)
    tx = (a % 9.0) - 4.5
    ty = (b - 55.0) / 11.0
    tongue = np.abs(tx) < 3.5 * np.sqrt(np.clip(ty * 1.5, 0, 1))
    which = (np.floor(a / 9.0) % 2) == 0
    c = np.where((b >= 55)[..., None], np.where(tongue[..., None], np.where(which[..., None], col(P_RED), col(P_BLUE)), col(P_CREAM)), c)
    # plaque joints and their nails; then what the weather has done
    pj = np.clip(1.5 - np.abs((a % 64.0) - 32.0 - 31.0) / 0.9, 0, 1)
    c = c * (1 - 0.45 * pj[..., None])
    nail = (np.hypot((a % 64.0) - 58.0, (b % 33.0) - 28.0) < 1.6)
    c = np.where(nail[..., None], col(BRONZE) * 0.8, c)
    faded = holes(a, b, seed + 3, cell=60.0, amount=0.22, sharp=0.12)
    c = c * (1 - 0.55 * faded[..., None]) + col("#cf9468") * 0.55 * faded[..., None]
    c = c * (1 + (tex(a, b, 150, seed + 4)[..., None] - 0.5) * 0.18)
    return np.clip(c, 0, 1).astype(F32)


def frieze(a, b, seed=0):
    """The band above the beam: the ends of the roof timbers, each covered by a plaque with three dark bars,
    and between them red panels with a pale rosette. b runs 0 to FRIEZE."""
    period = GAP / 3.0
    x = ((a - 70.0 + period / 2) % period) - period / 2
    c = np.empty(a.shape + (3,), dtype=F32)
    c[...] = col(P_RED) * 0.92
    which = (np.floor((a - 70.0 + period / 2) / period) % 2) == 0
    c = np.where(which[..., None], c, col(P_BLACK) * 1.15)
    px_ = np.abs(x) - period / 2                                            # the rosette sits midway between two beam ends
    r = np.hypot(px_, b - FRIEZE * 0.48)
    ang = np.arctan2(px_, b - FRIEZE * 0.48)
    ros = (r < 15.0 * (0.62 + 0.38 * np.cos(ang * 4.0) ** 2)) & (r > 3.2) | (r < 2.2)
    c = np.where(ros[..., None], np.where(which[..., None], col(P_CREAM), col(P_OCHRE)), c)
    beam = np.abs(x) < 15.0
    bars = np.abs(((x + 15.0) % 10.0) - 5.0) < 2.6
    c = np.where(beam[..., None], np.where((bars & (b < FRIEZE - 8))[..., None], col(P_BLUE) * 0.62, col(P_CREAM) * 0.97), c)
    edge = (b < 3.0) | (b > FRIEZE - 3.5)
    c = np.where(edge[..., None], col(P_CREAM) * 0.93, c)
    faded = holes(a, b, seed + 5, cell=70.0, amount=0.2, sharp=0.12)
    c = c * (1 - 0.5 * faded[..., None]) + col("#c99672") * 0.5 * faded[..., None]
    c = c * (1 + (tex(a, b, 150, seed + 6)[..., None] - 0.5) * 0.16)
    return np.clip(c, 0, 1).astype(F32)


def gutter(a, b, seed=0):
    """The face of the terracotta gutter at the eaves: tongues of red, cream and blue. b runs 0 to CORN."""
    tx = (a % 13.0) - 6.5
    ty = b / CORN
    tongue = np.abs(tx) < 5.2 * np.sqrt(np.clip((ty - 0.12) * 1.5, 0, 1))
    which = np.floor(a / 13.0) % 3
    c = np.empty(a.shape + (3,), dtype=F32)
    c[...] = col(P_CREAM) * 0.95
    tone = np.where((which == 0)[..., None], col(P_RED), np.where((which == 1)[..., None], col(P_BLUE), col(P_OCHRE)))
    c = np.where((tongue & (ty < 0.86))[..., None], tone, c)
    c = np.where((ty >= 0.86)[..., None], col(CLAY) * 0.95, c)
    c = c * (1 + (tex(a, b, 120, seed + 7)[..., None] - 0.5) * 0.2)
    faded = holes(a, b, seed + 8, cell=50.0, amount=0.2, sharp=0.15)
    c = c * (1 - 0.45 * faded[..., None]) + col("#c89068") * 0.45 * faded[..., None]
    return np.clip(c, 0, 1).astype(F32)


def column_paint(seed):
    """The paint on a column: the lower third red, the rest cream plaster; scuffed and chipped where people
    pass, and gone to the bare stone in a few patches."""
    def paint(h, around):
        b = h - HP
        a = around * 251.0                                                  # cm round the shaft
        c = np.empty(h.shape + (3,), dtype=F32)
        c[...] = col(STUCCO)
        c *= (1 + (tex(a, b, 160, seed)[..., None] - 0.5) * 0.14 + (tex(a, b, 30, seed + 1)[..., None] - 0.5) * 0.06)
        third = 34.0 + 186.0
        red = col(RED)[None, None, :] * (1 + (tex(a, b, 60, seed + 2)[..., None] - 0.5) * 0.25)
        wear = holes(a, b, seed + 3, cell=46.0, amount=0.13 + 0.26 * np.clip(1 - np.abs(b - 105) / 85.0, 0, 1), sharp=0.09)
        red = red * (1 - 0.85 * wear[..., None]) + (col(STUCCO) * np.array([0.93, 0.80, 0.70], dtype=F32)) * 0.85 * wear[..., None]
        is_red = (b < third) & (b > 33)
        c = np.where(is_red[..., None], red, c)
        ring = np.clip(1.5 - np.abs(b - third - 3.0) / 1.6, 0, 1)            # a dark line where the red stops
        c = c * (1 - 0.5 * ring[..., None]) + col(P_BLACK) * 0.5 * ring[..., None]
        streak = step(0.6, 0.9, tex(a * 5.0, b * 0.35, 90, seed + 4)) * np.clip((b - 200) / 200.0, 0, 1)
        c = c * (1 - 0.10 * streak[..., None])
        much = 0.07 + 0.11 * ((seed * 0.37) % 1)                             # no two columns have lost the same
        bare = holes(a, b, seed + 5, cell=95.0, amount=much, sharp=0.03) * (b > 36) * (b < 556)
        stone_ = col("#a8957c")[None, None, :] * (0.8 + 0.4 * tex(a, b, 11, seed + 6, 3)[..., None])
        edge = np.clip(holes(a + 2.0, b + 2.5, seed + 5, cell=95.0, amount=much, sharp=0.03) * (b > 36) * (b < 556) - bare, 0, 1)
        lime = step(0.80, 0.90, tex(a * 9.0, b * 0.22, 110, seed + 8)) * step(430 + 90 * ((seed * 0.61) % 1), 560, b) * (b < 562)   # the pigeons' mark
        c = c * (1 - 0.6 * lime[..., None]) + col("#f6f2e6") * 0.6 * lime[..., None]
        c = c * (1 - bare[..., None]) + stone_ * bare[..., None]
        c = c * (1 - 0.3 * edge[..., None])
        base = b <= 33
        c = np.where(base[..., None], col(TRAV) * (0.93 + 0.14 * tex(a, b, 25, seed + 7)[..., None]), c)
        cap = b >= 562
        bands = (np.abs(b - 566) < 2.2) | (np.abs(b - 577) < 1.6)            # painted rings under the capital
        c = np.where((cap & bands)[..., None], col(P_RED), c)
        c = np.where((b > 582)[..., None] & (np.floor(a / 7.0) % 2 == 0)[..., None] & (b < 592)[..., None], col(P_BLUE) * 1.1, c)
        return np.clip(c, 0, 1).astype(F32)
    return paint


def column_profile():
    """(height, radius) up a column, from the porch floor: base, shaft with its slight swelling, capital."""
    p = [(10, 53), (12, 56), (15, 57), (18, 56), (20, 53), (21, 47), (24, 46.5), (25, 49), (27, 51), (29.5, 51), (31, 49), (32, 43), (34, 40)]
    for i in range(1, 13):
        t = i / 12.0
        p.append((34 + 528 * t, 40 - 6.0 * (0.25 * t + 0.75 * t * t)))
    p += [(563, 34.2), (564.5, 36.5), (567, 37), (569, 36), (570, 34), (579, 34), (581, 36), (585, 41), (589, 46), (592, 49), (594, 50)]
    return [(HP + a, b) for a, b in p]


def column(Tf, canvas, u0, v0, seed, shade=None, deep=0.0):
    """A whole column of the temple on a canvas: plinth, turned base, fluted shaft, capital and abacus."""
    sh = 1.0 if deep else 0.0

    def own_at(Wf, v_plane, sd):
        u_, h_, _ = Wf.on_front(v_plane)
        return u_, h_, col(TRAV) * (0.9 + 0.2 * tex(u_, h_, 30, sd)[..., None])
    # plinth: we see its left side, its front and its top
    for Wf, m in Tf.face([(u0 - 56, v0 - 56, HP), (u0 - 56, v0 + 56, HP), (u0 - 56, v0 + 56, HP + 10), (u0 - 56, v0 - 56, HP + 10)]):
        canvas.put(LIT.on(col(TRAV) * 0.94, 0.0, deep=deep, bounce=0.6), m, Wf)
    for Wf, m in Tf.face([(u0 - 56, v0 - 56, HP), (u0 + 56, v0 - 56, HP), (u0 + 56, v0 - 56, HP + 10), (u0 - 56, v0 - 56, HP + 10)]):
        _, _, own = own_at(Wf, v0 - 56, seed + 20)
        canvas.put(LIT.on(own, -SV, sh, deep=deep, bounce=0.6), m, Wf)
    for Wf, m in Tf.face([(u0 - 56, v0 - 56, HP + 10), (u0 + 56, v0 - 56, HP + 10), (u0 + 56, v0 + 56, HP + 10), (u0 - 56, v0 + 56, HP + 10)]):
        canvas.put(LIT.on(col(TRAV), SH, sh, up=1, deep=deep), m, Wf)
    k = Tf.k(u0, v0)
    xc = Tf.pt(u0, v0, HP)[0]
    Wf = Tf.window([(xc - 60 * k, Tf.pt(u0, v0, TOP + 8)[1]), (xc + 60 * k, Tf.pt(u0, v0, HP)[1])])
    if Wf is None:
        return
    c, a = lathe(Wf, LIT, u0, v0, column_profile(), column_paint(seed), flutes=20, flute_from=HP + 34 + 190, flute_to=HP + 560, shadow=shade, deep=deep)
    canvas.put(c, a, Wf)
    # abacus: its underside, then the capital's bowl again where it hides the middle of that, its left side, its front
    for Wa, m in Tf.face([(u0 - 52, v0 - 52, HP + 594), (u0 + 52, v0 - 52, HP + 594), (u0 + 52, v0 + 52, HP + 594), (u0 - 52, v0 + 52, HP + 594)]):
        canvas.put(LIT.on(col(STUCCO) * 0.8, 0.0, deep=0.45 + deep * 0.5, up=-1, bounce=1.1), m, Wa)
    canvas.put(c, a * (Wf.py < Tf.pt(u0, v0, HP + 580)[1]) * (Wf.py > Tf.pt(u0, v0 - 50, HP + 594)[1] - 0.2), Wf)
    for Wa, m in Tf.face([(u0 - 52, v0 - 52, HP + 594), (u0 - 52, v0 + 52, HP + 594), (u0 - 52, v0 + 52, TOP), (u0 - 52, v0 - 52, TOP)]):
        canvas.put(LIT.on(col(STUCCO) * 0.97, 0.0, deep=deep, bounce=0.4), m, Wa)
    for Wa, m in Tf.face([(u0 - 52, v0 - 52, HP + 594), (u0 + 52, v0 - 52, HP + 594), (u0 + 52, v0 - 52, TOP), (u0 - 52, v0 - 52, TOP)]):
        u_, h_, _ = Wa.on_front(v0 - 52)
        own = col(STUCCO) * (0.93 + 0.14 * tex(u_, h_, 40, seed + 21)[..., None])
        own = np.where((np.abs(h_ - (HP + 606)) < 1.6)[..., None], col(P_RED), own)
        canvas.put(LIT.on(own, -SV, sh, deep=deep, bounce=0.4), m, Wa)


def temple(fine=2, seed=5, stool=False):
    """The whole temple, painted crisply on two clear sheets: everything but the six front columns, and
    the six front columns. -> (Canvas, Canvas) at picture size. (`stool`: as it was first laid in, with
    the shadow of a folding stool on the steps.)"""
    Tf = T.finer(fine)
    back, cols = Canvas(Tf.shape), Canvas(Tf.shape)
    FR = -SV                                                 # how squarely a front faces the sun
    e0, e1, e2, e3, fu, fv = E0, E1, E2, E3, FU, FV

    def rise(hh):                                            # 0 at the porch floor, 1 at the top of the columns
        return np.clip((hh - HP) / HC, 0, 1)

    def mouldings(own, h):
        """The plinth course at the podium's foot and the crown under the porch floor."""
        line = np.clip(1.5 - np.abs(h - 36) / 1.6, 0, 1) + np.clip(1.5 - np.abs(h - (HP - 27)) / 2.2, 0, 1)
        return own * (1 - 0.42 * np.clip(line, 0, 1)[..., None]) * np.where(((h < 34) | (h > HP - 24))[..., None], 1.09, 1.0)

    # ================= the flank, in shade
    for Wf, m in Tf.face([(45, DEEP, HP), (45, BACK, HP), (45, BACK, TOP), (45, DEEP, TOP)]):
        v, h, ppc = Wf.on_side(45.0)
        own = plaster(v, h - HP, ppc, seed + 1, lost=0.2)
        pil = (v < DEEP + 66)                                # the pilaster that ends the wall
        own = np.where(pil[..., None], col(STUCCO) * (0.95 + 0.1 * tex(v, h, 60, seed + 30)[..., None]) * np.where((h - HP < 150)[..., None], col(DADO) / col(STUCCO) * 1.05, 1.0), own)
        own = own * (1 - 0.3 * np.clip(1.5 - np.abs(v - DEEP - 66) / 2.0, 0, 1)[..., None])
        under_eave = step(TOP - 190, TOP, h)
        back.put(LIT.on(own, 0.0, deep=0.08 + 0.40 * under_eave, bounce=0.40 * (1 - rise(h)) ** 1.3), m, Wf)
    # the beam, band and gutter along the flank, and the row of upright tiles on the eaves against the sky
    for Wf, m in Tf.face([(fu, fv, e0), (fu, BACK, e0), (fu, BACK, e1), (fu, fv, e1)]):
        v, h, ppc = Wf.on_side(fu)
        back.put(LIT.on(revet(v, h - e0, seed), 0.0, deep=0.15, bounce=0.4), m, Wf)
    for Wf, m in Tf.face([(fu, fv, e1), (fu, BACK, e1), (fu, BACK, e2), (fu, fv, e2)]):
        v, h, ppc = Wf.on_side(fu)
        back.put(LIT.on(frieze(v + 70 + 36, h - e1, seed), 0.0, deep=0.32, bounce=0.35), m, Wf)
    for Wf, m in Tf.face([(fu - EAVE, fv - EAVE, e2), (fu, fv, e2), (fu, BACK + 30, e2), (fu - EAVE, BACK + 30, e2)]):
        u, v, ppc = Wf.on_floor(e2)
        sof = col(CLAY) * (0.8 + 0.25 * ((np.floor(v / 21.0) % 2) == 0))[..., None]
        back.put(LIT.on(sof, 0.0, deep=0.45, up=-1, bounce=1.0), m, Wf)
    for Wf, m in Tf.face([(fu - EAVE, fv - EAVE, e2), (fu - EAVE, BACK + 30, e2), (fu - EAVE, BACK + 30, e3), (fu - EAVE, fv - EAVE, e3)]):
        v, h, ppc = Wf.on_side(fu - EAVE)
        back.put(LIT.on(gutter(v, h - e2, seed), 0.0, deep=0.05, bounce=0.3), m, Wf)
    for Wf, m in Tf.face([(fu - EAVE, fv - EAVE, e3 - 1), (fu - EAVE, BACK + 30, e3 - 1), (fu - EAVE, BACK + 30, e3 + 42), (fu - EAVE, fv - EAVE, e3 + 42)]):
        v, h, ppc = Wf.on_side(fu - EAVE)
        x_ = ((v + 20) % 62.0) - 31.0
        hh = h - e3
        ante = ((x_ / 17.0) ** 2 + (hh / 40.0) ** 2 < 1) & (hh > -1)
        face = ((x_ / 9.0) ** 2 + ((hh - 14) / 15.0) ** 2 < 1)
        own = np.where(face[..., None], col(P_CREAM) * 0.9, col(CLAY) * 0.9)
        own = np.where((np.hypot(np.abs(x_) - 3.5, hh - 18) < 1.8)[..., None] | ((np.abs(x_) < 3.5) & (np.abs(hh - 9) < 1.2))[..., None], col(P_BLACK), own)
        back.put(LIT.on(own, 0.0, deep=0.0, bounce=0.2), ante.astype(F32) * m, Wf)
    # the podium's flank: coursed tufa, a plinth course at the foot and a crown under the porch floor
    for Wf, m in Tf.face([(0, EDGE, 0), (0, BACK, 0), (0, BACK, HP), (0, EDGE, HP)]):
        v, h, ppc = Wf.on_side(0.0)
        own, _ = stone(v, h, ppc, TUFA, seed + 2, long=132, high=54, spread=0.11)
        own = mouldings(own, h)
        moss = np.clip(1 - h / 70.0, 0, 1) * step(0.35, 0.75, tex(v, h, 90, seed + 31))
        own = own * (1 - moss[..., None] * np.array([0.30, 0.16, 0.34], dtype=F32))
        vault = (np.abs(v - 1010) < 52) & (h < 168)                             # the low door to the vault under the temple
        frame_ = (np.abs(v - 1010) < 66) & (h < 184) & ~vault
        own = np.where(frame_[..., None], col(TRAV) * 0.93, own)
        wood = col("#5a4234") * (0.8 + 0.4 * (np.floor((v - 1010) / 17.0) % 2))[..., None]
        wood = np.where((np.abs((h % 56.0) - 28.0) < 4.0)[..., None], col("#3a3438"), wood)
        own = np.where(vault[..., None], wood, own)
        back.put(LIT.on(own, 0.0, deep=0.06, bounce=0.8 * np.clip(1 - h / 300.0, 0, 1)), m, Wf)

    # ================= the porch: ceiling, the wall with the door, the floor
    for Wf, m in Tf.face([(45, -36, TOP), (UW - 45, -36, TOP), (UW - 45, DEEP, TOP), (45, DEEP, TOP)]):
        u, v, ppc = Wf.on_floor(TOP)
        beam = (np.abs(((u - 70 + GAP / 2) % GAP) - GAP / 2) < 20) | (np.abs(((v - 36) % 121.0) - 60.5) > 46)
        cx_ = ((u - 70) % GAP) - GAP / 2
        cy_ = ((v - 36) % 121.0) - 60.5
        own = np.where(beam[..., None], col(WOOD) * (0.85 + 0.3 * tex(u * 0.3, v * 3.0, 40, seed + 3)[..., None]), col("#42707c"))
        own = np.where(((np.abs(cx_) > 92) | (np.abs(cy_) > 36))[..., None] & ~beam[..., None], col(P_RED) * 0.9, own)
        own = np.where((np.hypot(cx_, cy_) < 13)[..., None] & ~beam[..., None], col(P_OCHRE), own)
        back.put(LIT.on(own, 0.0, deep=0.66 + 0.2 * np.clip(v / DEEP, 0, 1), up=-1, bounce=0.9 * np.clip(1.25 - v / 520.0, 0.2, 1.0)), m, Wf)

    d0, d1, dh0, dh1 = DOOR
    for Wf, m in Tf.face([(45, DEEP, HP), (UW - 45, DEEP, HP), (UW - 45, DEEP, TOP), (45, DEEP, TOP)]):
        u, h, ppc = Wf.on_front(DEEP)
        own = plaster(u, h - HP, ppc, seed + 4, lost=0.10)
        pil = (u < 112) | (u > UW - 112)
        own = np.where(pil[..., None], col(STUCCO) * (0.95 + 0.1 * tex(u, h, 60, seed + 32)[..., None]) * np.where((h - HP < 150)[..., None], col(DADO) / col(STUCCO) * 1.05, 1.0), own)
        own = own * (1 - 0.3 * (np.clip(1.5 - np.abs(u - 112) / 2.0, 0, 1) + np.clip(1.5 - np.abs(u - (UW - 112)) / 2.0, 0, 1))[..., None])
        case = (u > d0 - 32) & (u < d1 + 32) & (h < dh1 + 32)                     # the door case, and the shelf on brackets over it
        grooves = 1 - 0.18 * (np.clip(1.5 - np.abs(np.minimum(np.abs(u - d0), np.abs(u - d1)) - 16) / 1.8, 0, 1) * (h < dh1 + 14) + np.clip(1.5 - np.abs(h - dh1 - 16) / 1.8, 0, 1))
        own = np.where(case[..., None], col(TRAV) * (0.95 + 0.12 * tex(u, h, 50, seed + 33)[..., None]) * grooves[..., None], own)
        shelf = (u > d0 - 50) & (u < d1 + 50) & (h >= dh1 + 32) & (h < dh1 + 56)
        own = np.where(shelf[..., None], col(TRAV) * np.where((h > dh1 + 47)[..., None], 1.08, 0.78), own)
        brk = ((np.abs(u - (d0 - 38)) < 9) | (np.abs(u - (d1 + 38)) < 9)) & (h < dh1 + 32) & (h > dh1 - 26)
        own = np.where(brk[..., None], col(TRAV) * 0.84, own)
        for (tu, th, tw, tht) in ((300, HP + 190, 62, 88), (392, HP + 205, 48, 70), (1010, HP + 195, 66, 84), (1100, HP + 188, 44, 96), (228, HP + 215, 44, 58)):   # bronze tablets of the laws
            tab = (np.abs(u - tu) < tw / 2) & (np.abs(h - th - tht / 2) < tht / 2)
            lines_ = (np.abs(((h - th) % 9.0) - 4.5) < 1.3) & (np.abs(u - tu) < tw / 2 - 6) & (h - th > 8) & (h - th < tht - 8)
            tabc = np.where(lines_[..., None], col("#b8e0c8") * 1.5, col("#7fc0a0") * (1.3 + 0.5 * tex(u, h, 30, seed + 34)[..., None]))
            tabc = np.where(((np.abs(u - tu) > tw / 2 - 3) | (np.abs(h - th - tht / 2) > tht / 2 - 3))[..., None], col("#e8b860") * 1.5, tabc)
            own = np.where(tab[..., None], tabc, own)
        hb_ = h - (HP + 508)
        key = (hb_ > 0) & (hb_ < 44) & ~case & ~shelf
        tt = (u % 36.0) / 36.0
        kk_ = (hb_ - 8) / 28.0
        wave = ((tt < 0.5) & (np.abs(kk_ - 0.8) < 0.14)) | ((tt >= 0.5) & (np.abs(kk_ - 0.2) < 0.14)) | (((np.abs(tt - 0.5) < 0.07) | (tt < 0.07) | (tt > 0.93)) & (kk_ > 0.06) & (kk_ < 0.94))
        band_ = np.where(wave[..., None], col(P_RED) * 1.2, col(P_OCHRE) * 1.1)
        band_ = np.where(((hb_ < 5) | (hb_ > 39))[..., None], col(P_BLACK) * 1.6, band_)
        own = np.where(key[..., None], band_ * (0.8 + 0.4 * tex(u, h, 60, seed + 46)[..., None]), own)
        glow = (1 - rise(h)) ** 1.6
        back.put(LIT.on(own, 0.0, deep=0.62 + 0.25 * rise(h), bounce=0.95 * glow), m, Wf)
    # the open doorway: the dark room, and the two bronze leaves swung inward
    hole_pts = [(d0, DEEP, dh0), (d1, DEEP, dh0), (d1, DEEP, dh1), (d0, DEEP, dh1)]
    for Wf, hole in Tf.face(hole_pts):
        u, h, ppc = Wf.on_front(DEEP)
        inside = ramp(np.clip((h - dh0) / (dh1 - dh0), 0, 1), [(0.0, "#3c2226"), (0.22, "#24161c"), (1.0, "#110d15")])
        back.put(inside, hole, Wf)
        for hinge, sgn, open_by in ((d1, -1, 72.0), (d0, 1, 38.0)):                                  # (the left one stands half open, so that we see its face)
            swing = math.radians(open_by)
            far_u, far_v = hinge + sgn * 95 * math.cos(swing), DEEP + 95 * math.sin(swing)
            quad = Wf.mask(Tf.pts([(hinge, DEEP, dh0), (far_u, far_v, dh0), (far_u, far_v, dh1), (hinge, DEEP, dh1)]))
            wx, wz = T.ground(hinge, DEEP)
            L = Frame.at(CAM, T.angle + (180 - open_by if sgn < 0 else open_by), wx, wz, fine=fine).window([(Wf.px.min(), Wf.py.min()), (Wf.px.max(), Wf.py.max())], pad=0)
            a_, h_, ppc_ = L.on_front(0.0)
            a_, h_ = a_[:Wf.shape[0], :Wf.shape[1]], h_[:Wf.shape[0], :Wf.shape[1]]
            a_ = np.abs(a_)
            hp = (h_ - dh0) % 94.0
            rail = (np.abs(hp - 47.0) > 38) | (a_ < 9) | (a_ > 86)                                    # panels between rails
            stud = (np.hypot(((a_ - 9) % 19.25) - 9.6, np.minimum(hp, 94 - hp) - 4.5) < 2.7) & (np.abs(hp - 47.0) > 38)
            own_l = np.where(rail[..., None], col("#d9a44c") * 1.25, col("#b98a3e") * 0.95)
            own_l = own_l * (0.8 + 0.4 * tex(a_, h_, 40, seed + 35)[..., None])
            green = step(0.55, 0.85, tex(a_, h_, 60, seed + 36))
            own_l = own_l * (1 - 0.5 * green[..., None]) + col("#7fb89c") * 0.5 * green[..., None]
            own_l = np.where(stud[..., None], col("#ffe9a8") * 1.6, own_l)
            rr = np.hypot(a_ - 76, h_ - (dh0 + 208))
            own_l = np.where(((np.abs(rr - 8.5) < 2.0) | (np.hypot(a_ - 76, h_ - (dh0 + 220)) < 4.0))[..., None], col("#ffe9a8") * 1.5, own_l)   # a ring to pull it by
            own_l = own_l * (1 + 1.2 * np.clip(1 - a_ / 7.0, 0, 1)[..., None])                         # the edge by the hinge catches the day
            shade_in = np.clip(a_ / 95.0, 0, 1) * (1.0 if sgn < 0 else 0.45)                            # deeper into the room it is darker
            leaf = LIT.on(own_l, 0.0, deep=0.10 + 0.5 * shade_in, bounce=1.8 * (1 - rise(h_)) ** 1.0 * (1 - 0.5 * shade_in) + 0.9)
            back.put(leaf, quad * hole, Wf)
    for Wf, m in Tf.face([(d0, DEEP, HP), (d1, DEEP, HP), (d1, DEEP, dh0), (d0, DEEP, dh0)]):
        back.put(LIT.on(col(BRONZE) * 0.9, 0.0, deep=0.3, bounce=1.4), m, Wf)                          # the bronze sill
    # the porch floor: sunlit along its front, striped by the shadows of the columns
    for Wf, m in Tf.face([(0, EDGE, HP), (UW, EDGE, HP), (UW, DEEP, HP), (0, DEEP, HP)]):
        u, v, ppc = Wf.on_floor(HP)
        own, _ = stone(u, v, ppc, TRAV, seed + 6, long=128, high=86, spread=0.07, joint=1.3)
        shadow = sunless(solids(False), u, v, HP, (SU, SV, SH))
        back.put(LIT.on(own, SH, shadow, up=1, deep=0.45 * step(0, DEEP, v), bounce=0.5), m, Wf)

    block(back, Tf, (868, 1012, DEEP - 46, DEEP, HP + 30, HP + 42), "#9a7448", seed + 44, shadow=1.0, deep=0.45, bounce=1.3)      # the doorkeeper's bench
    for bu in (874, 1000):
        block(back, Tf, (bu, bu + 8, DEEP - 44, DEEP - 4, HP, HP + 30), "#7a5a38", seed + 45, shadow=1.0, deep=0.5, bounce=1.3)

    # ================= the column on the flank, behind the corner one, in the shade of the porch
    column(Tf, back, FLANK_COL[0], FLANK_COL[1], seed + 40, shade=lambda h, s, around: 1.0, deep=0.30)


    # ================= the front of the podium beside the steps, the side of the steps, the steps
    for (a0, a1) in ((0, SU0), (SU1, UW)):
        for Wf, m in Tf.face([(a0, EDGE, 0), (a1, EDGE, 0), (a1, EDGE, HP), (a0, EDGE, HP)]):
            u, h, ppc = Wf.on_front(EDGE)
            own, _ = stone(u, h, ppc, TUFA, seed + 7, long=118, high=54, spread=0.10)
            own = mouldings(own, h)
            own = own * (1 - 0.12 * step(0.55, 0.9, tex(u * 6.0, h * 0.5, 100, seed + 38))[..., None])
            back.put(LIT.on(own, FR, 0.0, bounce=0.7 * np.clip(1 - h / 300.0, 0, 1)), m, Wf)
    zig = [(SU0, VK(1), 0)]
    for k in range(1, NSTEP + 1):
        zig += [(SU0, VK(k), k * RISE)] + ([(SU0, VK(k + 1), k * RISE)] if k < NSTEP else [])
    zig += [(SU0, EDGE, 0)]
    for Wf, m in Tf.face(zig):
        v, h, ppc = Wf.on_side(SU0)
        own, _ = stone(v, h, ppc, TRAV, seed + 8, long=96, high=36, spread=0.08, joint=1.2)
        own = own * (1 - 0.25 * np.clip(1 - h / 50.0, 0, 1)[..., None] * step(0.3, 0.7, tex(v, h, 80, seed + 39))[..., None])
        nook = np.clip(1 - (EDGE - v) / 260.0, 0, 1) * np.clip(1 - h / 260.0, 0, 1)                    # the corner against the podium is dimmer
        back.put(LIT.on(own, 0.0, deep=0.05 + 0.3 * nook, bounce=0.9 * np.clip(1 - h / 260.0, 0, 1)), m, Wf)
    for k in range(NSTEP, 0, -1):
        vk = VK(k)
        for Wf, m in Tf.face([(SU0, vk, (k - 1) * RISE), (SU1, vk, (k - 1) * RISE), (SU1, vk, k * RISE), (SU0, vk, k * RISE)], pad=1):
            u, h, ppc = Wf.on_front(vk)
            tone, jm = slabs(u, ppc, seed + 50 + k, long=150)
            own = col(TRAV)[None, None, :] * (1 + (tone[..., None] - 0.5) * 0.12) * (1 + (tex(u, h + k * 40, 90, seed + 9)[..., None] - 0.5) * 0.14)
            own = own * (1 - 0.5 * jm[..., None])
            hb = h - (k - 1) * RISE
            own = own * (1 - 0.34 * np.clip(1 - hb / 4.0, 0, 1)[..., None])                              # dirt gathers where it meets the tread below
            own = own * (1 - 0.10 * step(0.5, 0.85, tex(u * 2.0, h * 0.8 + k * 30, 80, seed + 10))[..., None])
            chip = step(0.62, 0.72, tex(u, h * 3 + k * 50, 16, seed + 18, 3)) * np.clip((hb - 13.5) / 3.0, 0, 1)   # the arris is chipped
            own = own * (1 - 0.3 * chip[..., None])
            cut = sunless(solids(stool=stool), u, vk - 0.5, h, (SU, SV, SH), spread=0.02)
            back.put(LIT.on(own * 0.97, 0.42, cut, bounce=0.9), m, Wf)                                   # (a little more light than is strictly true: the steps must glow)
        if k < NSTEP:
            hk = k * RISE
            for Wf, m in Tf.face([(SU0, vk, hk), (SU1, vk, hk), (SU1, VK(k + 1), hk), (SU0, VK(k + 1), hk)], pad=1):
                u, v, ppc = Wf.on_floor(hk)
                tone, jm = slabs(u, ppc, seed + 50 + k, long=150)
                own = col(TRAV)[None, None, :] * (1 + (tone[..., None] - 0.5) * 0.10) * (1 + (tex(u, v + k * 60, 110, seed + 11)[..., None] - 0.5) * 0.16)
                own = own * (1 - 0.45 * jm[..., None])
                tv = (v - vk) / TREAD
                trodden = np.exp(-((u - UW / 2) / 330.0) ** 2) * (0.6 + 0.4 * tex(u, v, 140, seed + 12))  # the middle is worn pale and smooth
                own = own * (1 + 0.09 * trodden[..., None])
                grime = step(0.45, 0.8, tex(u, v * 3.0 + k * 90, 260, seed + 19)) * (1 - 0.7 * trodden)
                own = own * (1 - grime[..., None] * np.array([0.13, 0.12, 0.08], dtype=F32))
                own = own * (1 - 0.30 * step(0.70, 1.0, tv + 0.14 * (tex(u, v, 30, seed + 13) - 0.5))[..., None])   # dust along the back of each tread
                own = own * (1 + 0.08 * np.clip(1 - tv / 0.14, 0, 1)[..., None])                         # and its front edge worn bright
                cut = sunless(solids(stool=stool), u, v, hk, (SU, SV, SH), spread=0.02)
                back.put(LIT.on(own, SH, cut, up=1, bounce=0.5), m, Wf)

    # ================= the roof front: beam, band, gutter, and the gable above
    for Wf, m in Tf.face([(fu, fv, e0), (UW - fu, fv, e0), (UW - fu, 36, e0), (fu, 36, e0)]):
        back.put(LIT.on(col(WOOD) * 0.9, 0.0, deep=0.55, up=-1, bounce=1.2), m, Wf)
    drop = EAVE * (SH / -SV)                                                                            # how far down the gutter's shadow comes

    def cast_of(Wf, u, h):
        return step(e2 - drop - 3, e2 - drop + 3, h + (tex(u, h, 90, seed + 14) - 0.5) * 5)
    for Wf, m in Tf.face([(fu, fv, e0), (UW - fu, fv, e0), (UW - fu, fv, e1), (fu, fv, e1)]):
        u, h, ppc = Wf.on_front(fv)
        cast = cast_of(Wf, u, h)
        back.put(LIT.on(revet(u - fu, h - e0, seed), FR, cast, deep=0.1 * cast, bounce=0.6), m, Wf)
    for Wf, m in Tf.face([(fu, fv, e1), (UW - fu, fv, e1), (UW - fu, fv, e2), (fu, fv, e2)]):
        u, h, ppc = Wf.on_front(fv)
        cast = cast_of(Wf, u, h)
        back.put(LIT.on(frieze(u, h - e1, seed), FR, cast, deep=0.15 * cast, bounce=0.6), m, Wf)
    for Wf, m in Tf.face([(fu - EAVE, fv - EAVE, e2), (UW - fu + EAVE, fv - EAVE, e2), (UW - fu, fv, e2), (fu, fv, e2)]):
        u, v, ppc = Wf.on_floor(e2)
        sof = col(CLAY) * (0.8 + 0.25 * ((np.floor(u / 21.0) % 2) == 0))[..., None]
        back.put(LIT.on(sof, 0.0, deep=0.45, up=-1, bounce=1.1), m, Wf)
    for Wf, m in Tf.face([(fu - EAVE, fv - EAVE, e2), (UW - fu + EAVE, fv - EAVE, e2), (UW - fu + EAVE, fv - EAVE, e3), (fu - EAVE, fv - EAVE, e3)]):
        u, h, ppc = Wf.on_front(fv - EAVE)
        back.put(LIT.on(gutter(u, h - e2, seed), FR, 0.0, bounce=0.3), m, Wf)
    half = UW / 2 - fu + EAVE
    apex = e3 + half * PITCH
    for Wf, m in Tf.face([(fu - EAVE, fv + 8, e3), (UW / 2, fv + 8, apex), (UW - fu + EAVE, fv + 8, e3)]):
        u, h, ppc = Wf.on_front(fv + 8)
        slope_h = e3 + (half - np.abs(u - UW / 2)) * PITCH                                              # the height of the gable's edge above each place
        own = col("#6e97a6")[None, None, :] * (1 + (tex(u, h, 200, seed + 15)[..., None] - 0.5) * 0.3)
        own = own * (1 - 0.2 * step(0.5, 0.85, tex(u * 6.0, h * 0.5, 110, seed + 16))[..., None])
        gone = holes(u, h, seed + 17, cell=150.0, amount=0.2)
        own = own * (1 - gone[..., None]) + col("#cbb89a") * gone[..., None]
        under_rake = step(slope_h - 34 - 70, slope_h - 34 - 50, h)
        back.put(LIT.on(own, FR, under_rake, deep=0.2 * under_rake, bounce=0.3), m, Wf)
    for Wf, m in Tf.face([(fu - EAVE - 14, fv - EAVE, e3 - 2), (UW / 2, fv - EAVE, apex + 12), (UW - fu + EAVE + 14, fv - EAVE, e3 - 2)]):
        u, h, ppc = Wf.on_front(fv - EAVE)
        slope_h = e3 + (half + 12 - np.abs(u - UW / 2)) * PITCH
        along = (half - np.abs(u - UW / 2)) / math.cos(math.atan(PITCH))
        own = gutter(along, (h - (slope_h - 36)) * math.cos(math.atan(PITCH)) * (CORN / 34.0), seed + 1)
        rake = (h < slope_h) & (h > slope_h - 36) & (h >= e3 - 2)
        back.put(LIT.on(own, FR, 0.0, bounce=0.3), rake.astype(F32) * m, Wf)

    # ================= the six columns of the front, on their own sheet
    def top_shade(h, s, around):                                                                        # the gutter's shadow reaches the capitals' sides
        ang = around * 2 * math.pi
        vs = 34.0 * (np.cos(ang) * T.ev[0] + np.sin(ang) * T.ev[1])
        return step(-3, 3, h - (e2 - (vs - (fv - EAVE)) * (SH / -SV)))
    for i, cu in enumerate(COLS):
        column(Tf, cols, cu, 0.0, seed + 60 + i * 7, shade=top_shade)
    return back.reduced(fine), cols.reduced(fine)


def hand(a):
    """A hand does not rule its lines: push a picture or mask about a little, in short wobbles and long wanders.
    (Always the same push, so that sheets painted apart still fit one another.)"""
    return warp(warp(a, 0.75, 26, 5), 1.15, (150, 70), 6)


def handed(layer):
    out = Canvas(layer.shape)
    both = hand(np.dstack([layer.c, layer.a]))
    out.c, out.a = both[..., :3].astype(F32), np.clip(both[..., 3], 0, 1).astype(F32)
    return out


def kept(name, make, *sources):
    """Paint a layer, or fetch it from the last run if nothing that paints it has changed."""
    os.makedirs(KEEP, exist_ok=True)
    key = source_key("rome_steps_kit.py", *sources)
    path = f"{KEEP}/{name}-{key}.npz"
    if os.path.exists(path):
        z = np.load(path)
        return [z[k] for k in sorted(z.files)]
    out = make()
    for f in os.listdir(KEEP):
        if f.startswith(name + "-"):
            os.remove(f"{KEEP}/{f}")
    np.savez_compressed(path, **{f"a{i}": o for i, o in enumerate(out)})
    return out


def temple_layers(stool=False):
    def make():
        b, c = temple(stool=stool)
        return [b.c, b.a, c.c, c.a]
    bc, ba, cc, ca = kept("first" if stool else "temple", make, temple, column, column_paint, column_profile, plaster, revet, frieze, gutter, slabs, block, solids,
                          repr((NEIGHBOUR, ALTAR, TRIPOD, STONE, CAGE, STOOL_WAS, stool)),
                          repr((T.angle, T.at_x, T.at_depth, tuple(SUN), HP, RISE, TREAD, NSTEP, EDGE, GAP, HC, DEEP, BACK, DOOR, ARCH, FRIEZE, CORN, EAVE)))
    back, cols = Canvas(SHAPE), Canvas(SHAPE)
    back.c, back.a, cols.c, cols.a = bc, ba, cc, ca
    return back, cols


# ---------------------------------------------------------------- what stands on the pavement (cm, in the temple's measurements)
ALTAR = (-285.0, -175.0, -745.0, -665.0, 104.0)             # u0, u1, v0, v1, height
TRIPOD = (-80.0, -690.0, 134.0)                              # u, v, height
STONE = (178.0, 262.0, -1068.0, -1030.0, 98.0)               # the boundary stone
SEAT = (262.0, 4)                                            # where the soothsayer sits (the game draws him): u, and which step
CAGE = (128.0, 196.0, 4)                                     # his cage of chickens: u0, u1, step
STOOL_WAS = (318.0, 3)                                       # a folding stool stood here when the picture was first laid in: u, step
BASE = Frame.at(CAM, 9.0, -505.0, 700.0)                     # the statue base at the very front, bottom left
BASE_BOX = (0.0, 250.0, 0.0, 130.0, 0.0, 122.0)


def solids(things=True, stool=False):
    """Everything that throws a shadow, as simple blocks. (`stool`: with the folding stool that was there
    at first, for the first lay-in only.)"""
    S = [("box", 0, UW, EDGE, BACK, 0, HP), ("box", 45, UW - 45, DEEP, BACK, HP, TOP),
         ("box", FU, UW - FU, FV, BACK, E0, E2), ("box", FU - EAVE, UW - FU + EAVE, FV - EAVE, BACK + 30, E2, E3),
         ("gable", FU - EAVE, UW - FU + EAVE, FV - EAVE, BACK + 30, E3, PITCH)]
    S += [("box", SU0, SU1, VK(k), EDGE, 0, k * RISE) for k in range(1, NSTEP + 1)]
    S += [("cyl", cu, 0.0, 37.0, HP, TOP) for cu in COLS] + [("cyl", 70.0, GAP, 37.0, HP, TOP)]
    S += [("box", cu - 54, cu + 54, -54, 54, HP, HP + 12) for cu in COLS] + [("box", cu - 52, cu + 52, -52, 52, HP + 594, TOP) for cu in COLS]
    nu, nv0, nv1, nh = NEIGHBOUR
    S += [("box", nu, nu + 2500, nv0, nv1, 0, nh)]
    if things:
        u0, u1, v0, v1, hh = ALTAR
        S += [("box", u0 - 12, u1 + 12, v0 - 12, v1 + 12, 0, 14), ("box", u0, u1, v0, v1, 0, hh), ("box", u0 - 6, u1 + 6, v0 - 6, v1 + 6, hh - 16, hh + 12)]
        tu, tv, th = TRIPOD
        S += [("cyl", tu, tv, 30.0, th - 22, th), ("cyl", tu - 1, tv - 19, 2.6, 0, th - 18), ("cyl", tu - 17, tv + 10, 2.6, 0, th - 18), ("cyl", tu + 17, tv + 10, 2.6, 0, th - 18),
              ("cyl", tu, tv, 15.0, 50, 54)]
        u0, u1, v0, v1, hh = STONE
        S += [("box", u0, u1, v0, v1, 0, hh - 8), ("box", u0 + 12, u1 - 12, v0, v1, hh - 8, hh)]
        cu0, cu1, ck = CAGE
        S += [("box", cu0, cu1, VK(ck) + 2, VK(ck) + 46, ck * RISE, ck * RISE + 52)]
        if stool:
            su_, sk = STOOL_WAS
            S += [("box", su_ - 20, su_ + 20, VK(sk) + 4, VK(sk) + 34, sk * RISE + 34, sk * RISE + 40)]
    return S


def far(color, v, most=0.82):
    """A color as it looks through the morning air at a distance v (cm): paler and bluer."""
    t = np.clip(v / 42000.0, 0, 1) ** 0.6 * most * 0.62
    c = col(color)
    warm = float(np.clip((c[0] - c[2]) * 4, 0, 1))                        # sunlit, warm colors keep their warmth longer
    return mix(color, mix("#c9dcee", "#f4ead4", warm), t * (1 - 0.35 * warm))


def forum(seed=31):
    """The Forum beyond: a speaker's platform, statues on tall columns, a long colonnade, temples at the far
    end and a hill with a great temple on it. Painted crisply on a clear sheet: -> (color, coverage)."""
    rng = np.random.default_rng(seed)
    s = Sheet(SHAPE)
    P = T.pt
    lit, half, shade, dark, roof = "#ffe9b4", "#ecd2a2", "#a3a2c8", "#6a6688", "#dc8a5e"

    # ---- the hill: tufa cliffs, trees, the walls that hold its terraces up
    sky_line = [(-10, 222), (18, 208), (40, 196), (62, 188), (96, 184), (142, 185), (170, 192), (200, 205), (226, 216), (262, 226), (300, 232)]
    hill = curve(sky_line, 6)
    s.poly(hill + [(300, 262), (-10, 262)], far("#b9b08e", 52000, 0.60))
    for i in range(46):                                      # clumps of trees, darkest where the slope turns from the light
        px = rng.uniform(-5, 250)
        top = np.interp(px, [q[0] for q in hill], [q[1] for q in hill])
        py = rng.uniform(top + 5, 258)
        r = rng.uniform(3, 8) * (0.6 + 0.5 * (py - top) / 60)
        tone = far(mix("#5f7a4a", "#8a9a5e", rng.random()), 47000, 0.52)
        s.ellipse(px, py, r * 1.3, r * 0.8, tone, 0.85)
        s.ellipse(px - r * 0.3, py + r * 0.25, r * 0.9, r * 0.45, far("#4a5f52", 47000, 0.5), 0.6)
    for (x0, x1, y0, y1, n) in ((20, 82, 226, 244, 7), (118, 190, 222, 238, 8), (150, 236, 242, 256, 9)):     # terrace walls with blind arches
        s.poly([(x0, y0), (x1, y0 + 2), (x1, y1 + 2), (x0, y1)], far(half, 46000, 0.62))
        s.line([(x0, y0), (x1, y0 + 2)], far(lit, 46000, 0.5), 1.0)
        for j in range(n):
            ax = lerp(x0 + 4, x1 - 4, j / (n - 1))
            s.poly([(ax - 2.2, y1 + 1), (ax - 2.2, y0 + 6), (ax, y0 + 4), (ax + 2.2, y0 + 6), (ax + 2.2, y1 + 1)], far(shade, 46000, 0.55), 0.9)
    for i in range(22):                                      # houses on the slope: a pale wall, a red roof
        px = rng.uniform(0, 240)
        top = np.interp(px, [q[0] for q in hill], [q[1] for q in hill])
        py = rng.uniform(top + 14, 252)
        w, hgt = rng.uniform(6, 13), rng.uniform(4, 8)
        s.poly([(px, py), (px + w, py), (px + w, py - hgt), (px, py - hgt)], far(mix(lit, half, rng.random()), 45000, 0.6))
        s.poly([(px - 1, py - hgt), (px + w + 1, py - hgt), (px + w * 0.5, py - hgt - 2.6)], far(roof, 45000, 0.55))
        s.poly([(px, py), (px + w * 0.3, py), (px + w * 0.3, py - hgt), (px, py - hgt)], far(shade, 45000, 0.6), 0.8)
    def pine(px, py, hgt):                                   # an umbrella pine: a bare leaning trunk and a flat dark crown
        s.line([(px, py), (px + hgt * 0.06, py - hgt * 0.55), (px - hgt * 0.02, py - hgt)], far("#6a5648", 44000, 0.5), max(0.9, hgt * 0.05))
        for (dx, dy, rx, ry, tone) in ((-0.22, -1.02, 0.34, 0.15, "#4f6a48"), (0.20, -1.06, 0.36, 0.16, "#587650"), (0.0, -1.12, 0.30, 0.13, "#6d8a56"), (0.12, -1.16, 0.2, 0.08, "#8aa262")):
            s.ellipse(px + dx * hgt, py + dy * hgt, rx * hgt, ry * hgt, far(tone, 44000, 0.45))

    def cypress(px, py, hgt):
        s.poly([(px - hgt * 0.10, py), (px - hgt * 0.13, py - hgt * 0.45), (px, py - hgt), (px + hgt * 0.13, py - hgt * 0.45), (px + hgt * 0.10, py)], far("#4a6248", 40000, 0.5))
        s.poly([(px + hgt * 0.02, py), (px + hgt * 0.04, py - hgt * 0.5), (px, py - hgt), (px + hgt * 0.13, py - hgt * 0.45), (px + hgt * 0.10, py)], far("#6a8456", 40000, 0.45))
    for (px, py, hgt) in ((208, 212, 20), (223, 219, 17), (34, 203, 18), (18, 211, 15), (190, 204, 13)):
        pine(px, py, hgt)
    for (px, py, hgt) in ((156, 228, 15), (163, 230, 12), (232, 244, 22), (240, 246, 17), (10, 240, 16), (52, 222, 13)):
        cypress(px, py, hgt)
    # ---- the great temple on the hill
    gx0, gx1, gy = 64.0, 134.0, 186.0
    s.poly([(gx0 - 6, gy + 6), (gx1 + 8, gy + 7), (gx1 + 8, gy - 3), (gx0 - 6, gy - 4)], far(half, 50000, 0.66))           # its platform
    s.poly([(gx0 - 14, gy - 6), (gx0, gy - 6), (gx0, gy - 34), (gx0 - 14, gy - 31)], far(shade, 50000, 0.62))             # the flank, in shade
    s.poly([(gx0, gy - 4), (gx1, gy - 3), (gx1, gy - 34), (gx0, gy - 34)], far(dark, 50000, 0.70))                        # the porch
    for j in range(7):
        cx = lerp(gx0 + 3, gx1 - 3, j / 6)
        s.line([(cx, gy - 4), (cx, gy - 33)], far(lit, 50000, 0.52), 2.2)
        s.line([(cx - 1.0, gy - 4), (cx - 1.0, gy - 33)], far(shade, 50000, 0.6), 0.8, 0.8)
    s.poly([(gx0 - 3, gy - 33), (gx1 + 3, gy - 32), (gx1 + 3, gy - 38), (gx0 - 3, gy - 39)], far(half, 50000, 0.58))
    s.poly([(gx0 - 5, gy - 39), (gx1 + 5, gy - 38), ((gx0 + gx1) / 2, gy - 55)], far("#e6c9a6", 50000, 0.6))
    s.line([(gx0 - 6, gy - 39), ((gx0 + gx1) / 2, gy - 56), (gx1 + 6, gy - 38)], far(roof, 50000, 0.5), 1.6)
    s.poly([(gx0 - 16, gy - 31), (gx0 - 5, gy - 39), ((gx0 + gx1) / 2, gy - 56), ((gx0 + gx1) / 2 - 18, gy - 50)], far(roof, 50000, 0.62), 0.9)
    s.line([((gx0 + gx1) / 2, gy - 56), ((gx0 + gx1) / 2, gy - 62)], far("#e8c060", 50000, 0.3), 1.4)                       # something gilded on the ridge
    s.ellipse((gx0 + gx1) / 2, gy - 63, 2.2, 1.6, far("#f0d070", 50000, 0.25))

    # ---- the far end of the square: a temple, an arcaded building with shops, a gate between them
    def block(u0, u1, v0, v1, h0, h1, front, side, a=1.0):
        s.poly([P(u0, v0, h0), P(u0, v1, h0), P(u0, v1, h1), P(u0, v0, h1)], far(side, v0), a)
        s.poly([P(u0, v0, h0), P(u1, v0, h0), P(u1, v0, h1), P(u0, v0, h1)], far(front, v0), a)
    v0 = 31000
    block(-2500, -700, v0, v0 + 3000, 0, 320, half, shade)                                         # temple B: podium
    s.poly([P(-2500, v0 + 300, 320), P(-700, v0 + 300, 320), P(-700, v0 + 300, 1280), P(-2500, v0 + 300, 1280)], far(dark, v0, 0.72))
    s.poly([P(-2500, v0, 320), P(-2500, v0 + 3000, 320), P(-2500, v0 + 3000, 1280), P(-2500, v0, 1280)], far(shade, v0))
    for j in range(6):
        cu = lerp(-2440, -760, j / 5)
        s.line([P(cu, v0, 320), P(cu, v0, 1280)], far(lit, v0, 0.6), 2.0)
        s.line([(P(cu, v0, 320)[0] - 0.9, P(cu, v0, 320)[1]), (P(cu, v0, 1280)[0] - 0.9, P(cu, v0, 1280)[1])], far(shade, v0), 0.7, 0.8)
    block(-2560, -640, v0, v0 + 3000, 1280, 1470, half, shade)
    s.poly([P(-2600, v0, 1470), P(-600, v0, 1470), P(-1600, v0, 1840)], far("#ecd3ac", v0))
    s.poly([P(-2600, v0, 1470), P(-1600, v0, 1840), P(-1600, v0 + 3000, 1840), P(-2600, v0 + 3000, 1470)], far(roof, v0), 0.95)
    s.line([P(-2600, v0, 1470), P(-1600, v0, 1860), P(-600, v0, 1470)], far(roof, v0, 0.7), 1.3)
    block(-80, 2900, v0 + 400, v0 + 2400, 0, 1150, half, shade)                                    # building C: two rows of arches, shops below
    for row, (ha, hb) in enumerate(((60, 440), (560, 980))):
        for j in range(11):
            cu = lerp(60, 2760, j / 10)
            a0, a1, top = P(cu - 78, v0 + 400, ha), P(cu + 78, v0 + 400, ha), P(cu, v0 + 400, hb)
            s.poly([a0, (a0[0], top[1] + 2.5), (top[0], top[1]), (a1[0], top[1] + 2.5), a1], far(dark if row == 0 else shade, v0, 0.7), 0.95)
    s.line([P(-80, v0 + 400, 500), P(2900, v0 + 400, 500)], far(lit, v0, 0.6), 1.0)
    s.poly([P(-140, v0 + 400, 1150), P(2960, v0 + 400, 1150), P(2960, v0 + 1400, 1380), P(-140, v0 + 1400, 1380)], far(roof, v0))
    block(-560, -180, v0 + 900, v0 + 1300, 0, 900, lit, shade)                                     # the gate
    s.poly([P(-470, v0 + 900, 0), P(-470, v0 + 900, 560), P(-370, v0 + 900, 640), P(-270, v0 + 900, 560), P(-270, v0 + 900, 0)], far(dark, v0, 0.7))
    s.line([P(-590, v0 + 900, 900), P(-150, v0 + 900, 900)], far(lit, v0, 0.5), 1.4)

    # ---- the long colonnade down the left side, two storeys, in full sun
    cu = -2750
    for (ha, hb, tone) in ((0, 560, lit), (560, 1060, lit)):
        s.poly([P(cu, 12500, ha), P(cu, 30000, ha), P(cu, 30000, hb), P(cu, 12500, hb)], far(tone, 20000, 0.62))
    s.poly([P(cu, 12500, 1060), P(cu, 30000, 1060), P(cu - 600, 30000, 1260), P(cu - 600, 12500, 1260)], far(roof, 20000, 0.6))
    for j in range(26):
        cv = lerp(12700, 29800, (j / 25) ** 1.0)
        wd = 150
        for (ha, hb) in ((40, 470), (610, 980)):
            a0, a1, a2, a3 = P(cu, cv, ha), P(cu, cv + wd * 2.6, ha), P(cu, cv + wd * 2.6, hb), P(cu, cv, hb)
            s.poly([a0, a1, a2, a3], far(dark, cv, 0.66), 0.92)
    s.line([P(cu, 12500, 560), P(cu, 30000, 560)], far("#fff4d6", 20000, 0.5), 1.1)
    s.line([P(cu, 12500, 1060), P(cu, 30000, 1060)], far("#fff4d6", 20000, 0.5), 1.1)

    # ---- the speaker's platform, with the bronze beaks of old ships along its front
    v0, u0, u1, hp = 7600, -1780, -640, 300
    block(u0, u1, v0, v0 + 700, 0, hp, half, shade)
    s.poly([P(u0, v0, hp), P(u1, v0, hp), P(u1, v0 + 700, hp), P(u0, v0 + 700, hp)], far(lit, v0))
    s.line([P(u0, v0, hp), P(u1, v0, hp)], far("#fff6da", v0, 0.4), 1.2)
    s.line([P(u0, v0, hp - 34), P(u1, v0, hp - 34)], far(shade, v0), 0.9, 0.8)
    s.line([P(u0, v0, 40), P(u1, v0, 40)], far(shade, v0), 0.9, 0.7)
    for j in range(5):                                       # the beaks
        bu = lerp(u0 + 130, u1 - 130, j / 4)
        a0 = P(bu, v0, 190)
        s.poly([(a0[0] - 3.5, a0[1] - 3), (a0[0] + 3.5, a0[1] - 3), (a0[0] + 5.5, a0[1] + 2), (a0[0] + 1, a0[1] + 6), (a0[0] - 3.5, a0[1] + 3)], far("#4f6a5c", v0, 0.5))
        s.line([(a0[0] - 2.5, a0[1] - 2.4), (a0[0] + 3, a0[1] - 2.4)], far("#e8d08a", v0, 0.3), 1.0)
        s.line([(a0[0] - 4, a0[1] + 8), (a0[0] - 9, a0[1] + 9)], far(shade, v0), 1.6, 0.55)                 # and its shadow on the wall
    for j in range(12):                                      # a rail of posts along the top
        bu = lerp(u0 + 30, u1 - 30, j / 11)
        s.line([P(bu, v0 + 30, hp), P(bu, v0 + 30, hp + 95)], far("#c9b594", v0), 1.0)
    s.line([P(u0 + 30, v0 + 30, hp + 95), P(u1 - 30, v0 + 30, hp + 95)], far("#f4e3c0", v0), 1.1)
    for k in range(7):                                       # steps up its right end
        hk = hp * (1 - k / 7)
        s.poly([P(u1, v0 + 80, 0), P(u1 + 34 * (k + 1), v0 + 80, 0), P(u1 + 34 * (k + 1), v0 + 80, hk), P(u1, v0 + 80, hk)], far(mix(lit, half, k / 7), v0))

    # ---- statues on tall columns
    def honour(u, v, hgt, statue=170, seed_=0):
        lit, half, shade = ("#fff0c8", "#e9d6b0", "#9c98c0") if v < 6000 else ("#fbe9c0", "#e8d3ae", "#a9a6c6")
        k = T.k(u, v)
        x, y0 = P(u, v, 0)
        y1 = P(u, v, hgt)[1]
        w = 34 * k
        s.poly([(x - w * 1.9, y0), (x + w * 1.9, y0), (x + w * 1.9, y0 - 150 * k), (x - w * 1.9, y0 - 150 * k)], far(half, v))       # its base
        s.poly([(x - w * 1.9, y0), (x - w * 0.4, y0), (x - w * 0.4, y0 - 150 * k), (x - w * 1.9, y0 - 150 * k)], far(shade, v), 0.85)
        s.poly([(x - w, y0 - 150 * k), (x + w, y0 - 150 * k), (x + w * 0.86, y1), (x - w * 0.86, y1)], far(shade, v))
        s.poly([(x - w * 0.1, y0 - 150 * k), (x + w, y0 - 150 * k), (x + w * 0.86, y1), (x - w * 0.05, y1)], far(lit, v))
        s.poly([(x - w * 1.5, y1), (x + w * 1.5, y1), (x + w * 1.3, y1 - 26 * k), (x - w * 1.3, y1 - 26 * k)], far(half, v))
        top = y1 - 26 * k
        body = far("#3f5a4c", v, 0.45)
        s.poly([(x - 20 * k, top), (x + 22 * k, top), (x + 16 * k, top - statue * k * 0.78), (x - 14 * k, top - statue * k * 0.78)], body)
        s.ellipse(x + 1 * k, top - statue * k * 0.88, 11 * k, 12 * k, body)
        s.line([(x + 14 * k, top - statue * k * 0.66), (x + 44 * k, top - statue * k * 0.92)], body, max(1.0, 9 * k))                # an arm held out
        s.line([(x + 10 * k, top - statue * k * 0.2), (x + 12 * k, top - statue * k * 0.74)], far("#d9c27a", v, 0.3), max(0.8, 5 * k), 0.9)
    honour(-330, 4600, 760, seed_=1)
    honour(-1220, 10800, 820, seed_=2)
    honour(380, 15000, 700, seed_=3)

    # ---- people, far off: a dab of toga or tunic, a darker dab of head, a short shadow to the left
    cloth = ["#fbf2dc", "#f6ead0", "#fbf2dc", "#c8553a", "#7d94b8", "#d9a441", "#b9a084", "#f1e6cc", "#8a6a4e"]
    spots = [(-1500, 9000), (-1350, 9150), (-900, 9900), (-300, 9000), (-180, 9300), (200, 11500), (-700, 13500), (-560, 13700), (-1900, 14500),
             (-1700, 15300), (300, 17000), (-1000, 18500), (-880, 18800), (900, 20000), (-2000, 21000), (-300, 23000), (-150, 23300), (1500, 24000),
             (-1500, 26000), (500, 27000), (-1180, 8350), (-1040, 8350), (-1400, 8380)]
    for i, (u, v) in enumerate(spots):
        k = T.k(u, v)
        up = 300 if v < 8500 else 0                          # three stand on the platform
        x, y = P(u, v, up)
        hgt = (150 + 30 * rng.random()) * k
        s.line([(x - 1, y), (x - 1 - hgt * 0.9, y - 0.5)], far("#8f88a8", v), max(0.8, hgt * 0.16), 0.5)
        s.line([(x, y), (x, y - hgt * 0.84)], far(cloth[i % len(cloth)], v, 0.5), max(1.1, hgt * 0.30))
        s.ellipse(x, y - hgt * 0.92, max(0.7, hgt * 0.10), max(0.7, hgt * 0.10), far("#7a5a48", v, 0.5))
    return s.done()


def ground(seed=17, joints=True):
    """The paved square in its own colors, no light yet: -> (picture, joint mask, u, v, pixels per cm)."""
    u, v, ppc = T.on_floor(0.0)
    tone, jm, above = courses(u, v, long=168.0, high=104.0, seed=seed, joint=1.8, ppc=ppc, vary_len=0.34)
    c = col(PAVE)[None, None, :] * (1 + (tone[..., None] - 0.5) * 0.11)
    warm = (hash2(np.floor(tone * 811), 5, seed) - 0.5) * 0.07                # some slabs are greyer tufa, some yellower
    c = c + np.stack([warm, warm * 0.15, -warm * 1.2], axis=-1)
    old = (hash2(np.floor(tone * 577), 9, seed) > 0.88)                       # a few dark old slabs
    c = c * np.where(old[..., None], np.array([0.90, 0.88, 0.89], dtype=F32), 1.0)
    c = c * (1 + (tex(u, v, 420, seed + 1)[..., None] - 0.5) * 0.20 + (tex(u, v, 60, seed + 2)[..., None] - 0.5) * 0.10)
    trod = np.exp(-((u - 500) / 700.0) ** 2) * np.clip((v + 1500) / 900.0, 0, 1)   # worn pale where everyone walks to the steps
    c = c * (1 + 0.05 * trod[..., None])
    return np.clip(c, 0, 1).astype(F32), jm, u, v, ppc


def next_door(seed=23):
    """The building beyond the temple on the right: all we see of it, between the last columns, is its blank
    side wall in shade (ochre wash over brick and rubble, a red dado, one shuttered window) and the edge of its
    tiled roof. -> Canvas."""
    c = Canvas(SHAPE)
    nu, nv0, nv1, nh = NEIGHBOUR
    for Wf, m in T.face([(nu, nv0, 0), (nu, nv1, 0), (nu, nv1, nh), (nu, nv0, nh)]):
        v, h, ppc = Wf.on_side(nu)
        own = col("#d8a556")[None, None, :] * (1 + (tex(v, h, 260, seed)[..., None] - 0.5) * 0.30 + (tex(v, h, 40, seed + 1)[..., None] - 0.5) * 0.10)
        own = np.where((h < 210)[..., None], col("#7c3a30") * (0.85 + 0.3 * tex(v, h, 60, seed + 2)[..., None]), own)
        own = own * (1 - 0.4 * np.clip(1.5 - np.abs(h - 210) / 2.0, 0, 1)[..., None])
        own = own * (1 - 0.16 * step(0.5, 0.85, tex(v * 7.0, h * 0.45, 130, seed + 3))[..., None] * np.clip(h / 500.0, 0, 1)[..., None])   # rain marks
        gone = holes(v, h, seed + 4, cell=170.0, amount=0.20, sharp=0.03)
        tone, jm, above = courses(v, h, long=34, high=12, seed=seed + 5, joint=1.6, ppc=ppc)
        brick = col("#a8623e")[None, None, :] * (0.8 + 0.4 * tone[..., None]) * (1 - 0.35 * jm[..., None])
        own = own * (1 - gone[..., None]) + brick * gone[..., None]
        win = (np.abs(v - 760) < 46) & (np.abs(h - 640) < 60)                                         # the window: shutters of grey wood, shut
        frame_ = (np.abs(v - 760) < 56) & (np.abs(h - 640) < 70) & ~win
        own = np.where(frame_[..., None], col("#e8d8b8"), own)
        shut = col("#8a6e52") * (0.8 + 0.4 * (np.floor(h / 9.0) % 2))[..., None]
        shut = np.where((np.abs(v - 760) < 2.0)[..., None], col("#2a2a30"), shut)
        own = np.where(win[..., None], shut, own)
        own = own * (1 - 0.25 * step(nh - 160, nh, h)[..., None])
        c.put(LIT.on(own, 0.0, deep=0.16 + 0.25 * np.clip(1 - h / 500.0, 0, 1), bounce=0.3), m, Wf)
    for Wf, m in T.face([(nu - 40, nv0 - 30, nh), (nu - 40, nv1, nh), (nu - 40, nv1, nh + 26), (nu - 40, nv0 - 30, nh + 26)]):
        c.put(LIT.on(col(CLAY) * 0.95, 0.0, deep=0.1, bounce=0.2), m, Wf)
    for Wf, m in T.face([(nu - 40, nv0 - 30, nh + 26), (nu - 40, nv1, nh + 26), (nu + 500, nv1, nh + 190), (nu + 500, nv0 - 30, nh + 190)]):
        u, v, ppc = Wf.on_floor(nh + 26)
        rows = 0.86 + 0.2 * ((np.floor(v / 42.0) % 2) == 0)
        c.put(LIT.on(col(CLAY)[None, None, :] * rows[..., None], 0.5, 0.0, up=0.7), m, Wf)
    return c


def sky_layer(seed=11):
    """Sky: deep blue overhead, pale and warm toward the roofs, one great heap of cloud over the hill."""
    def make():
        pic = sky.field(SHAPE, HZ, [(0.0, "#2a6cc0"), (0.34, "#468fd8"), (0.62, "#7dbce8"), (0.84, "#c6e0e4"), (1.0, "#f4e6c6")], seed, haze="#f8ecd0", patch=0.03)
        sky.wisps(pic, HZ, seed + 3, "#fdf2dc", top=0.5, amount=0.5)
        sky.paint_clouds(pic, [(112, 120, 210, 100, 30), (-4, 200, 124, 52, 11), (270, 190, 110, 34, 8)], seed + 22,
                         tones=("#7f9ed6", "#b6cbe8", "#fbf3df", "#fffdf2"), light=SKY_LIGHT, ragged=11)
        return [pic]
    return kept("sky", make, sky_layer, repr(seed))[0].copy()


def ground_shadow():
    """Where the sun does not reach the pavement."""
    def make():
        u, v, ppc = T.on_floor(0.0)
        return [sunless(solids(), u, v, 0.0, (SU, SV, SH))]
    return kept("shadow", make, solids, repr((T.angle, T.at_x, T.at_depth, tuple(SUN), ALTAR, TRIPOD, STONE, CAGE, NEIGHBOUR, HP, GAP, HC, DEEP, BACK)))[0]


def cloud_shadow(seed=11):
    """A cloud's shadow over the nearest paving, its edge soft and wandering: -> how much to darken (0 to 0.36).
    Beyond it everything stands in full sun, so the steps are the lightest thing in the picture."""
    x, y = grid(SHAPE)
    edge_y = 548 + (noise(SHAPE, (260, 60), seed + 15, 3) - 0.5) * 60 - (x - 400) * 0.02
    return (step(0.0, 1.0, (y - edge_y) / 44.0) * 0.36).astype(F32)


def under(seed=11):
    """Everything broad and soft: the sky and its clouds, the Forum in its haze, the paved square with the
    great shadows lying on it. (The temple is laid on afterwards, as plain masses of light and shade.)"""
    x, y = grid(SHAPE)
    info = {}
    pic = sky_layer(seed)
    fc, fa = forum()
    over(pic, blur(fc, 1.6), blur(fa, 1.2))
    own, jm, u, v, ppc = ground()
    gmask = np.clip(y - HZ - 1.0, 0, 1)
    near = np.clip((y - HZ) / (H - HZ), 0, 1) ** 1.2
    own = own * (1 - near[..., None] * (1 - np.array([1.0, 0.93, 0.76], dtype=F32)) * 0.85)           # near stone is deeper and more golden
    cut = ground_shadow() * gmask
    shade_of_tree = mask_poly(SHAPE, [(-20, 440), (60, 452), (120, 470), (170, 505), (176, 560), (150, 610), (-20, 610)], soft=9, wobble=10, seed=seed + 2)
    dapple = step(0.38, 0.62, noise(SHAPE, 26, seed + 4, 3))
    cut = np.maximum(cut, shade_of_tree * (0.55 + 0.45 * dapple) * 0.9)                               # the laurel at the front corner shades the ground
    near_wall = np.exp(-np.clip(-u, 0, None) / 500.0) * (v > EDGE) * (u < 0)                         # warm light thrown back by the podium... 
    lit = LIT.on(own, SH, cut, up=1, deep=0.10 * cut + 0.10 * near_wall * cut, bounce=0.2 + 0.5 * (1 - near_wall))
    drift = (noise(SHAPE, 150, seed + 12, 3) - 0.5) * 0.10
    lit = np.clip(lit * (1 + (cut[..., None] * np.stack([drift, drift * 0.3, -drift], axis=-1)) + (noise(SHAPE, 60, seed + 13, 3) - 0.5)[..., None] * 0.08 * cut[..., None]), 0, 1)
    over(pic, lit, gmask)
    land.haze(pic, HZ, "#f3ead2", 0.78, 0.10, gmask)
    glow(pic, "#fff0c8", (np.clip(1 - np.abs(y - (HZ + 6)) / 26, 0, 1) * 0.10).astype(F32))         # dust and light over the far square
    tint(pic, "#b48c80", (cloud_shadow() * gmask).astype(F32))                                      # a cloud's shadow lies over the nearest paving
    corner = np.clip(((x - 400) / 400) ** 2 * 0.45 + ((y - 430) / 170).clip(0, 2) ** 2 * 0.55, 0, 1)
    tint(pic, "#cba27a", (corner * 0.22 * gmask).astype(F32))                                      # the near corners deeper and warmer
    info.update(u=u, v=v, ppc=ppc, joints=jm, ground=gmask, cut=cut, forum=(fc, fa), next_door=next_door())
    info["next_door"].onto(pic)
    return np.clip(pic, 0, 1), info


# ---------------------------------------------------------------- things that stand about
def block(canvas, Fm, box, base, seed, grain=0.18, cell=40.0, paint=None, deep=0.0, shadow=0.0, bounce=0.6):
    """A squared block standing on the ground, in the measurements of the frame Fm: whichever side we can
    see, its front, and its top if we look down on it. `paint(face, a, b, own)` may change its own color:
    face is "side" (a = v, b = h), "front" (a = u, b = h) or "top" (a = u, b = v)."""
    u0, u1, v0, v1, h0, h1 = box
    su, sv, sh = Fm.to_frame(SUN)
    cam_u, _ = Fm.find(CAM.vx, 1e7)
    if cam_u < u0 or cam_u > u1:
        us = u0 if cam_u < u0 else u1
        for Wf, m in Fm.face([(us, v0, h0), (us, v1, h0), (us, v1, h1), (us, v0, h1)]):
            v, h, ppc = Wf.on_side(us)
            own = col(base)[None, None, :] * (1 - grain / 2 + grain * tex(v, h, cell, seed)[..., None])
            own = own if paint is None else paint("side", v, h, own)
            canvas.put(LIT.on(own, -su if us == u0 else su, shadow, deep=deep, bounce=bounce * np.clip(1 - (h - h0) / 150.0, 0.2, 1)), m, Wf)
    for Wf, m in Fm.face([(u0, v0, h0), (u1, v0, h0), (u1, v0, h1), (u0, v0, h1)]):
        u, h, ppc = Wf.on_front(v0)
        own = col(base)[None, None, :] * (1 - grain / 2 + grain * tex(u, h, cell, seed + 1)[..., None])
        own = own if paint is None else paint("front", u, h, own)
        canvas.put(LIT.on(own, -sv, shadow, deep=deep, bounce=bounce * np.clip(1 - (h - h0) / 150.0, 0.2, 1)), m, Wf)
    if h1 < CAM.eye:
        for Wf, m in Fm.face([(u0, v0, h1), (u1, v0, h1), (u1, v1, h1), (u0, v1, h1)]):
            u, v, ppc = Wf.on_floor(h1)
            own = col(base)[None, None, :] * (1 - grain / 2 + grain * tex(u, v, cell, seed + 2)[..., None])
            own = own if paint is None else paint("top", u, v, own)
            canvas.put(LIT.on(own, sh, shadow, up=1, deep=deep), m, Wf)


def leaf(sheet, x, y, angle, length, tone, wide=0.26, rib=None):
    """One pointed leaf from its stalk end (x, y)."""
    ca, sa = math.cos(angle), math.sin(angle)
    pts = []
    for t, w in ((0, 0), (0.25, 0.8), (0.5, 1.0), (0.78, 0.62), (1, 0)):
        pts.append((x + ca * length * t - sa * length * wide * w, y + sa * length * t + ca * length * wide * w))
    for t, w in ((0.78, 0.62), (0.5, 1.0), (0.25, 0.8)):
        pts.append((x + ca * length * t + sa * length * wide * w, y + sa * length * t - ca * length * wide * w))
    sheet.poly(pts, tone)
    if rib is not None:
        sheet.line([(x, y), (x + ca * length * 0.92, y + sa * length * 0.92)], rib, max(0.7, length * 0.05), 0.8)


def amphora(sheet, x, y, k, lean, tones):
    """A wine jar with its foot at (x, y): pointed below, two handles at the neck. `lean` tips it over
    (radians; more than 1 and it lies on its side). `tones` are (dark side, body, light edge)."""
    half = [(0, 2), (8, 5.5), (26, 13), (48, 17), (62, 15), (70, 9), (74, 5.5), (86, 5), (88, 7), (90, 7)]
    ca, sa = math.cos(lean), math.sin(lean)

    def at(px, py):
        return (x + (px * ca + py * sa) * k, y - (py * ca - px * sa) * k)
    left = [at(-w, h) for h, w in half]
    right = [at(w, h) for h, w in reversed(half)]
    sheet.poly(left + right, tones[1])
    sheet.poly([at(w * 0.25, h) for h, w in half] + right, tones[0], 0.75)
    sheet.line([at(-w * 0.72, h) for h, w in half[2:6]], tones[2], max(0.8, 2.2 * k), 0.85)
    for sgn in (-1, 1):
        sheet.line([at(sgn * 5, 86), at(sgn * 13, 82), at(sgn * 14, 72), at(sgn * 12, 64)], tones[0] if sgn > 0 else tones[1], max(0.8, 2.4 * k))
    sheet.line([at(-7, 90), at(7, 90)], tones[2], max(0.8, 1.6 * k), 0.9)


def altar_layer(fine=2, seed=71):
    """The altar: a block of grey stone on a step, moulded top and bottom, with two rolls on top, a pan of
    embers between them, and a garland of laurel tied across its front. -> Canvas at picture size."""
    Tf = T.finer(fine)
    c = Canvas(Tf.shape)
    u0, u1, v0, v1, hh = ALTAR
    grey = "#cfc4b2"
    mid_u, mid_h = (u0 + u1) / 2, 26 + (hh - 42) * 0.52

    def die(face, a, b, own):
        if face == "front":                                  # a round dish cut in the stone, and a border line
            r = np.hypot(a - mid_u, b - mid_h)
            ring = np.clip(1.5 - np.abs(r - 15) / 1.6, 0, 1) + np.clip(1.5 - r / 2.4, 0, 1)
            own = own * (1 - 0.30 * np.clip(ring, 0, 1)[..., None])
            lip = np.clip(1.5 - np.abs(r - 17.5) / 1.3, 0, 1) * (b < mid_h)
            own = own * (1 + 0.14 * lip[..., None])
            edge = (np.abs(a - u0) < 7) | (np.abs(a - u1) < 7) | (b < 33) | (b > hh - 23)
            own = own * np.where(edge[..., None], 1.0, 0.95)
            own = own * (1 - 0.12 * step(0.5, 0.85, tex(a * 5.0, b * 0.5, 60, seed + 9))[..., None])
        return own
    block(c, Tf, (u0 - 12, u1 + 12, v0 - 12, v1 + 12, 0, 14), grey, seed)
    block(c, Tf, (u0 - 5, u1 + 5, v0 - 5, v1 + 5, 14, 26), mix(grey, "#ffffff", 0.08), seed + 3, cell=20)
    block(c, Tf, (u0, u1, v0, v1, 26, hh - 16), grey, seed + 6, paint=die)
    block(c, Tf, (u0 - 6, u1 + 6, v0 - 6, v1 + 6, hh - 16, hh), mix(grey, "#ffffff", 0.10), seed + 9, cell=20)
    for Wf, m in Tf.face([(u0 - 6, v0 - 6, hh - 16), (u1 + 6, v0 - 6, hh - 16), (u1 + 6, v0 - 6, hh - 12), (u0 - 6, v0 - 6, hh - 12)]):
        c.tint("#8a7c88", m * 0.6, Wf)                       # the shadow line under the crown
    for Wf, m in Tf.face([(u0 - 5, v0 - 5, 22), (u1 + 5, v0 - 5, 22), (u1 + 5, v0 - 5, 26), (u0 - 5, v0 - 5, 26)]):
        c.tint("#fff4dc", m * 0.0, Wf)
    out = c.reduced(fine)
    # the rolls, the embers, the garland: drawn on top, crisply
    s = Sheet(SHAPE)
    k = T.k(mid_u, v0)
    for side, tone_top, tone_end in ((u0 + 3, "#b9aeb4", "#8f869a"), (u1 - 3, "#f6e8cc", "#d8c8ae")):
        a0, a1 = T.pt(side, v0 - 6, hh + 9), T.pt(side, v1 + 6, hh + 9)
        s.line([a0, a1], tone_top, 18 * k)
        s.ellipse(a0[0], a0[1], 9.5 * k, 9.5 * k, tone_end)
        s.ellipse(a0[0], a0[1], 5.5 * k, 5.5 * k, "#7c7288", 0.8)
        s.ellipse(a0[0] + 0.5, a0[1] - 0.5, 2.2 * k, 2.2 * k, "#e6d6bc")
    f0, f1 = T.pt(mid_u - 26, (v0 + v1) / 2, hh + 3), T.pt(mid_u + 26, (v0 + v1) / 2, hh + 3)
    s.ellipse((f0[0] + f1[0]) / 2, f0[1] - 1, (f1[0] - f0[0]) / 2, 5.0, "#5a4a3c")                 # the bronze pan
    s.ellipse((f0[0] + f1[0]) / 2, f0[1] - 2, (f1[0] - f0[0]) / 2 - 2, 3.4, "#2c2422")
    rng = np.random.default_rng(seed)
    for i in range(9):
        ex, ey = lerp(f0[0] + 4, f1[0] - 4, rng.random()), f0[1] - 2 + rng.normal(0, 1.2)
        s.ellipse(ex, ey, 1.6, 1.1, mix("#ff8a30", "#ffd060", rng.random()))
    s.line([(f0[0] + 6, f0[1] - 3), (f1[0] - 2, f0[1] - 7)], "#4a3a30", 1.6)                        # two charred sticks
    s.line([(f0[0] + 12, f0[1] - 7), (f1[0] - 8, f0[1] - 2)], "#6a5444", 1.4)
    # the garland: a rope of laurel hanging between the top corners, a ribbon at each end
    ga, gb = T.pt(u0 + 6, v0 - 7, hh - 20), T.pt(u1 - 6, v0 - 7, hh - 20)
    sag = 22 * k
    rope = [(lerp(ga[0], gb[0], t), lerp(ga[1], gb[1], t) + sag * math.sin(math.pi * t) ** 0.9) for t in np.linspace(0, 1, 15)]
    s.line([(px, py + 2.5) for px, py in rope], "#6a6078", 5.0 * k + 1, 0.45)                       # its shadow on the stone
    s.line(rope, "#2f4a26", 6.5 * k)
    greens = ["#2c4a24", "#3f6a2c", "#5c8a34", "#8fae48", "#b6c860"]
    for i, (px, py) in enumerate(rope):
        for j in range(4):
            ang = rng.uniform(0, 2 * math.pi)
            tone = greens[min(4, int(rng.random() ** 1.3 * 5))] if math.sin(ang) < 0.3 else greens[int(rng.random() * 2)]
            leaf(s, px + rng.normal(0, 1.2), py + rng.normal(0, 1.2), ang, rng.uniform(6, 9.5) * k * 1.5, tone, rib=None)
        if i % 3 == 1:
            s.ellipse(px + rng.normal(0, 2), py + rng.normal(0, 2), 1.5, 1.5, "#c23a2e")            # berries
    for (px, py), d in ((ga, -1), (gb, 1)):
        s.line([(px, py), (px + d * 2, py + 9 * k * 2), (px + d * 5, py + 30 * k)], "#b8342c", 2.2)
        s.line([(px, py), (px - d * 1, py + 12 * k * 2), (px - d * 3, py + 26 * k)], "#e05a40", 1.8)
        s.ellipse(px, py, 3.0, 3.0, "#d04a36")
    jx, jy = T.pt(u1 + 3, v0 - 9, 14)                         # a small jug and a dish left on the step
    s.poly([(jx - 3.2, jy), (jx + 3.2, jy), (jx + 4.4, jy - 6), (jx + 2, jy - 10.5), (jx + 2.4, jy - 13), (jx - 2.4, jy - 13), (jx - 2, jy - 10.5), (jx - 4.4, jy - 6)], "#b8683c")
    s.line([(jx + 1.6, jy - 2), (jx + 2.6, jy - 6), (jx + 1.2, jy - 10)], "#f0b070", 1.1, 0.9)
    s.line([(jx - 2.2, jy - 11.5), (jx - 6, jy - 9), (jx - 4, jy - 5)], "#8a4a2c", 1.2)
    dx_, dy_ = T.pt(u0 + 22, v0 - 9, 14)
    s.ellipse(dx_, dy_ - 1.5, 7.0, 2.4, "#9a7434")
    s.ellipse(dx_, dy_ - 2.0, 5.2, 1.5, "#e8c874")
    sc, sa = s.done()
    out.put(sc, sa)
    return out


def tripod_layer(seed=73):
    """A bronze tripod: three slender legs on lions' paws, a shelf to brace them, a wide bowl with two ring
    handles. -> Canvas. (Solid paint goes on one sheet and the lights and glazes on another, so that the
    cut-out has no thin places in it.)"""
    s, g = Sheet(SHAPE), Sheet(SHAPE)
    tu, tv, th = TRIPOD
    k = T.k(tu, tv)
    dark, mid, lite, shine, green = "#4a3c2c", "#8a6830", "#c89a48", "#f8e09a", "#5c8a74"
    top = T.pt(tu, tv, th - 20)
    feet = [T.pt(tu - 19, tv + 10, 0), T.pt(tu + 19, tv + 10, 0), T.pt(tu - 1, tv - 21, 0)]          # two behind, one in front
    for i in (0, 1, 2):
        fx, fy = feet[i]
        hx = top[0] + (fx - top[0]) * 0.62
        leg = curve([(hx, top[1] + 2), (lerp(hx, fx, 0.5) + (fx - top[0]) * 0.12, lerp(top[1], fy, 0.5)), (fx, fy - 4 * k)], 8)
        s.taper(leg, dark if i == 0 else mid, 5.0 * k + 0.8, 3.6 * k + 0.8)
        g.taper([(px + 1.0, py) for px, py in leg], lite if i != 0 else mid, 1.8 * k + 0.4, 1.3 * k + 0.4, 0.9)
        s.poly([(fx - 5 * k, fy), (fx + 6 * k, fy), (fx + 3.4 * k, fy - 6.5 * k), (fx - 3.4 * k, fy - 6.5 * k)], dark if i == 0 else mid)   # the paw
        g.line([(fx + 1, fy - 5 * k), (fx + 4.4 * k, fy - 0.5)], lite, 1.0, 0.8)
    ring = T.pt(tu, tv, 54)
    s.ellipse(ring[0], ring[1], 17 * k, 4.6 * k, dark)                                              # the bracing shelf
    s.ellipse(ring[0], ring[1] - 1.0, 14.5 * k, 3.2 * k, mid)
    g.line([(ring[0] - 17 * k, ring[1]), (ring[0], ring[1] + 4.6 * k), (ring[0] + 17 * k, ring[1])], lite, 1.1, 0.9)
    bw, bh = 31 * k, 19 * k
    cx, cy = top[0], top[1] - 2 * k
    bowl = [(cx - bw, cy - bh * 0.55)] + [(cx + bw * math.cos(a), cy - bh * 0.55 + bh * 1.25 * math.sin(a)) for a in np.linspace(math.pi, 0, 14)] + [(cx + bw, cy - bh * 0.55)]
    for d in (-1, 1):                                                                               # ring handles, behind the bowl's edge
        s.ellipse(cx + d * bw * 1.04, cy - bh * 0.12, 3.8 * k, 5.0 * k, dark if d < 0 else lite)
        s.ellipse(cx + d * bw * 1.04, cy - bh * 0.12, 1.8 * k, 2.9 * k, mix(dark, "#000000", 0.4))
    s.poly(bowl, mid)
    g.poly([(cx - bw, cy - bh * 0.55)] + [(cx + bw * 0.99 * math.cos(a) - bw * 0.12, cy - bh * 0.55 + bh * 1.25 * math.sin(a)) for a in np.linspace(math.pi, math.pi * 0.42, 9)] + [(cx - bw * 0.2, cy - bh * 0.55)], dark, 0.85)
    g.poly([(cx + bw * 0.25, cy - bh * 0.5)] + [(cx + bw * 0.9 * math.cos(a), cy - bh * 0.5 + bh * 1.05 * math.sin(a)) for a in np.linspace(math.pi * 0.36, math.pi * 0.08, 6)] + [(cx + bw * 0.86, cy - bh * 0.5)], lite, 0.9)
    for j in range(7):                                                                              # a band of bosses round the bowl
        a = math.pi * (0.12 + 0.76 * j / 6)
        g.ellipse(cx + bw * 0.93 * math.cos(a), cy - bh * 0.30 + bh * 0.42 * math.sin(a), 1.1, 1.1, shine if a < 1.3 else lite, 0.9)
    s.ellipse(cx, cy - bh * 0.55, bw, 4.8 * k, dark)                                                # the mouth of the bowl
    s.ellipse(cx, cy - bh * 0.55 + 0.6, bw * 0.9, 3.5 * k, "#2a221e")
    c = Canvas(SHAPE)
    sc, sa = s.done()
    c.put(sc, sa)
    gc, ga = g.done()
    c.put(gc, ga * (sa > 0.5))
    g2 = Sheet(SHAPE)                                                                               # last, the brightest touches
    g2.ellipse(cx + bw * 0.55, cy + bh * 0.0, bw * 0.10, bh * 0.22, shine, 0.9)
    g2.ellipse(cx - bw * 0.38, cy + bh * 0.12, bw * 0.20, bh * 0.16, green, 0.45)                    # a bloom of green on the shaded side
    g2.line([(cx - bw, cy - bh * 0.55), (cx, cy - bh * 0.55 - 4.8 * k), (cx + bw, cy - bh * 0.55)], shine, 1.0, 0.85)
    gc, ga = g2.done()
    c.put(gc, ga * (c.a > 0.5))
    return c


def stone_layer(fine=2, seed=75):
    """The boundary stone: a squat post of grey stone, round on top, with four letters cut in its face."""
    Tf = T.finer(fine)
    c = Canvas(Tf.shape)
    u0, u1, v0, v1, hh = STONE
    grey = "#d2c8b6"
    block(c, Tf, (u0, u1, v0, v1, 0, hh - 16), grey, seed, grain=0.22, cell=30)
    mid_u, r = (u0 + u1) / 2, (u1 - u0) / 2
    arc = [(mid_u + r * math.cos(a), hh - 16 + 16 * math.sin(a)) for a in np.linspace(0, math.pi, 15)]
    for i in range(len(arc) - 1):                            # the rounded top, a strip at a time: lit toward the right
        (a0, b0), (a1, b1) = arc[i], arc[i + 1]
        tilt = math.atan2(b1 - b0, -(a1 - a0))
        nrm = (math.sin(tilt) if False else (b1 - b0), -(a1 - a0))
        n = unit((nrm[0], 0.0, nrm[1]))                       # in (u, v, h): it faces along u and up
        facing = max(0.0, n[0] * SU + n[2] * SH)
        for Wf, m in Tf.face([(a0, v0, b0), (a1, v0, b1), (a1, v1, b1), (a0, v1, b0)], pad=1):
            c.put(LIT.on(col(grey) * (0.96 + 0.06 * (i % 2)), facing, up=n[2]), m, Wf)
    for Wf, m in Tf.face([(u0, v0, hh - 16)] + [(a_, v0, b_) for a_, b_ in reversed(arc)] + [(u1, v0, hh - 16)]):
        u, h, ppc = Wf.on_front(v0)
        own = col(grey)[None, None, :] * (0.89 + 0.22 * tex(u, h, 30, seed + 1)[..., None])
        c.put(LIT.on(own, -SV, bounce=0.3), m, Wf)
    for Wf, m in Tf.face([(u0, v0, 0), (u1, v0, 0), (u1, v0, 20), (u0, v0, 20)]):
        u, h, ppc = Wf.on_front(v0)
        c.tint("#8f8a72", m * np.clip(1 - h / 20.0, 0, 1) * step(0.3, 0.7, tex(u, h, 24, seed + 2)) * 0.55, Wf)   # green at the foot
    out = c.reduced(fine)
    a0, a1 = T.pt(u0, v0, hh - 40), T.pt(u1, v0, hh - 40)
    slant = -(a1[1] - a0[1]) / (a1[0] - a0[0])
    k = T.k(mid_u, v0)
    pic = out.c.copy()
    cov = np.maximum(out.a, 1e-4)[..., None]
    straight = pic / cov
    letter.carve(straight, "SPQR", ((a0[0] + a1[0]) / 2 + 0.5, (a0[1] + a1[1]) / 2), 19 * k, dark="#4e4244", light="#fffaea", amount=0.96, hand=True, spacing=3.2 * k, slant=slant, rough=0.35, seed=seed)
    b0, b1 = T.pt(u0 + 10, v0, hh - 56), T.pt(u1 - 10, v0, hh - 56)
    s = Sheet(SHAPE)
    s.line([b0, b1], "#7a6c66", 0.9, 0.7)                     # a ruled line under the letters
    s.line([(b0[0], b0[1] + 1), (b1[0], b1[1] + 1)], "#fff6e0", 0.8, 0.5)
    for (du, dh, l) in ((18, 52, 14), (60, 30, 10), (40, 12, 8)):   # chips and a crack
        q = T.pt(u0 + du, v0, dh)
        s.line([q, (q[0] + l * 0.3, q[1] - l * 0.5), (q[0] + l * 0.2, q[1] - l)], "#857870", 0.9, 0.7)
    out.c = straight * cov
    sc, sa = s.done()
    out.put(sc, sa * (out.a > 0.5))
    return out


def front_layer(fine=2, seed=77):
    """Right at the front, bottom left: the top of a statue's base, half in the shade of a laurel, and a
    branch of the laurel itself hanging into the picture. Everyone passes behind it. -> Canvas."""
    Bf = BASE.finer(fine)
    c = Canvas(Bf.shape)
    u0, u1, v0, v1, h0, h1 = BASE_BOX
    tone = "#ded2bc"

    def face(kind, a, b, own):
        if kind != "top":
            own = own * (1 - 0.14 * step(0.5, 0.9, tex(a * 5.0, b * 0.5, 70, seed + 5))[..., None])
            own = own * (1 - 0.5 * step(0.6, 0.75, tex(a, b, 26, seed + 11))[..., None] * step(0.5, 0.8, tex(a, b, 120, seed + 12))[..., None] * np.array([0.5, 0.4, 0.9], dtype=F32))   # lichen
        else:
            own = own * (1 - 0.22 * step(0.55, 0.8, tex(a, b, 50, seed + 6))[..., None] * np.array([0.9, 0.6, 1.0], dtype=F32))
            own = own * (1 - 0.3 * np.clip(1.5 - np.abs(np.hypot(a - 150, b - 70) - 34) / 2.5, 0, 1)[..., None])      # the mark where the statue's foot was set
        return own
    block(c, Bf, (u0, u1, v0, v1, h0, h1 - 26), tone, seed, grain=0.22, cell=45, paint=face, bounce=0.2)
    block(c, Bf, (u0 - 5, u1 + 5, v0 - 5, v1 + 5, h1 - 26, h1 - 18), mix(tone, "#000000", 0.14), seed + 2, grain=0.2, cell=30, bounce=0.2)
    block(c, Bf, (u0 - 10, u1 + 10, v0 - 10, v1 + 10, h1 - 18, h1), mix(tone, "#ffffff", 0.10), seed + 3, grain=0.2, cell=45, paint=face, bounce=0.2)
    out = c.reduced(fine)
    # the laurel's shade lies over most of it; flecks of sun come through, and its near corner stands clear in the light
    x, y = grid(SHAPE)
    shade = mask_poly(SHAPE, [(-10, 440), (70, 452), (118, 472), (128, 500), (108, 528), (96, 560), (104, 610), (-10, 610)], soft=3.5, wobble=7, seed=seed + 7)
    fleck = step(0.50, 0.62, noise(SHAPE, 15, seed + 8, 3)) * step(0.35, 0.6, noise(SHAPE, 60, seed + 9, 2))
    shade = shade * (1 - 0.9 * fleck) * out.a
    out.c = out.c * (1 - shade[..., None] * (1 - np.array([0.46, 0.48, 0.74], dtype=F32)))
    # the branch: it comes in from the left above the base and hangs down across it
    s = Sheet(SHAPE)
    rng = np.random.default_rng(seed)
    greens = ["#132418", "#1d3620", "#2c4e24", "#487630", "#7ea040", "#bccb66"]
    stems = [curve([(-12, 430), (30, 438), (72, 456), (108, 486), (126, 520)], 8),
             curve([(22, 437), (48, 462), (60, 496), (58, 528)], 7),
             curve([(-12, 468), (20, 482), (44, 510), (50, 548), (40, 580)], 8),
             curve([(70, 455), (104, 458), (136, 470), (158, 492)], 7),
             curve([(-12, 512), (8, 530), (20, 560), (22, 596)], 7),
             curve([(-12, 404), (26, 408), (60, 420), (92, 426)], 6)]
    for st in stems:
        s.taper(st, "#3a2c22", 3.2, 1.0)
        s.taper([(px + 0.7, py - 0.5) for px, py in st], "#7a5c40", 1.0, 0.4, 0.8)
    for st in stems:
        n = len(st)
        for i in range(2, n, 2):
            px, py = st[i]
            tx, ty = st[min(i + 1, n - 1)][0] - st[i - 1][0], st[min(i + 1, n - 1)][1] - st[i - 1][1]
            along = math.atan2(ty, tx)
            for side in (-1, 1):
                ang = along + side * rng.uniform(0.5, 1.1)
                length = rng.uniform(13, 21)
                up = -math.sin(ang)                              # leaves that turn up to the sun are bright
                right = math.cos(ang)
                light = 0.22 + 0.45 * max(up, 0) + 0.30 * max(right, 0) + rng.normal(0, 0.14)
                tone_ = greens[int(np.clip(light * 6, 0, 5))]
                leaf(s, px, py, ang, length, tone_, wide=0.24, rib=greens[min(5, int(np.clip(light * 6, 0, 5)) + 1)])
        ex, ey = st[-1]
        leaf(s, ex, ey, math.atan2(st[-1][1] - st[-2][1], st[-1][0] - st[-2][0]), 18, greens[3], rib=greens[4])
    for (bx, by) in ((96, 474), (100, 479), (91, 478), (44, 500), (49, 505), (130, 468), (70, 424), (75, 428)):          # a few dark berries
        s.ellipse(bx, by, 2.4, 2.4, "#2a1c2c")
        s.ellipse(bx + 0.6, by - 0.7, 0.8, 0.8, "#8a7c9c")
    sc, sa = s.done()
    out.put(sc, sa)
    return out


def pigeon(sheet, x, y, size, seed, face=1, pecking=False):
    """A pigeon standing on the ground at (x, y): grey, a darker head and wing bars, a gleam on the neck."""
    rng = np.random.default_rng(seed)
    s = size
    body = mix("#737c90", "#9ea4b4", rng.random())
    dark = mix(body, "#2c3040", 0.6)
    if rng.random() < 0.2:
        body, dark = mix("#f2ece0", "#d8d0c4", rng.random()), "#a8a098"                              # now and then a white one
    f = face
    sheet.line([(x - f * 0.2 * s, y), (x - f * 0.2 * s, y - 0.25 * s)], "#c8605a", max(0.7, s * 0.06))  # legs
    sheet.line([(x + f * 0.1 * s, y), (x + f * 0.1 * s, y - 0.25 * s)], "#c8605a", max(0.7, s * 0.06))
    sheet.poly([(x - f * 0.95 * s, y - 0.30 * s), (x - f * 0.3 * s, y - 0.62 * s), (x - f * 0.2 * s, y - 0.22 * s)], dark)       # tail
    sheet.ellipse(x - f * 0.05 * s, y - 0.47 * s, 0.50 * s, 0.30 * s, body)
    sheet.ellipse(x - f * 0.20 * s, y - 0.50 * s, 0.36 * s, 0.20 * s, mix(body, "#ffffff", 0.18))                               # the wing, lit from above
    sheet.line([(x - f * 0.42 * s, y - 0.42 * s), (x - f * 0.02 * s, y - 0.36 * s)], dark, max(0.7, s * 0.07))
    sheet.line([(x - f * 0.50 * s, y - 0.50 * s), (x - f * 0.12 * s, y - 0.45 * s)], dark, max(0.7, s * 0.06))
    if pecking:
        hx, hy = x + f * 0.62 * s, y - 0.20 * s
    else:
        hx, hy = x + f * 0.45 * s, y - 0.86 * s
    sheet.line([(x + f * 0.28 * s, y - 0.52 * s), (hx, hy)], dark, 0.30 * s)
    sheet.line([(x + f * 0.33 * s, y - 0.56 * s), (lerp(x + f * 0.3 * s, hx, 0.6), lerp(y - 0.52 * s, hy, 0.6))], "#6fa08c", 0.14 * s, 0.9)      # green on the neck
    sheet.ellipse(hx, hy, 0.17 * s, 0.15 * s, dark)
    sheet.line([(hx + f * 0.12 * s, hy + 0.02 * s), (hx + f * 0.32 * s, hy + (0.12 if pecking else 0.05) * s)], "#e8d8b0", max(0.7, s * 0.07))  # beak
    return sheet


def details(pic, info, back, first=None, seed=11):
    """Over the brushwork: say every built thing again, crisply, then the small things. `first` is the temple
    as it was first laid in under the brushwork: wherever it has been changed since, the change is painted
    out at full strength."""
    x, y = grid(SHAPE)
    rng = np.random.default_rng(seed + 5)
    P = T.pt
    fc, fa = info["forum"]
    over(pic, fc, fa * 0.88)
    land.haze(pic, HZ, "#f3ead2", 0.16, 0.07, fa)
    wisp = mask_line(SHAPE, curve([(151, 190), (149, 172), (153, 156), (146, 140), (136, 128)], 6), [0.8 + 0.28 * i for i in range(25)], soft=1.6)
    over(pic, "#f4ecde", (wisp * 0.42 * (0.5 + noise(SHAPE, (8, 24), seed + 22, 3))).clip(0, 1).astype(F32))     # smoke of a sacrifice up on the hill
    # joints of the paving: thin, broken, fainter far away
    jm = hand(info["joints"]) * info["ground"] * (0.62 + 0.5 * noise(SHAPE, 110, seed + 21, 3))
    tint(pic, "#8a6f5c", np.clip(jm * 0.60, 0, 1).astype(F32))
    lip = np.roll(info["joints"], 1, axis=0) * info["ground"] * (1 - info["cut"]) * (1 - np.clip(info["joints"] * 2, 0, 1))
    glow(pic, "#fff2d0", np.clip(lip * 0.16, 0, 1).astype(F32))                                     # the near edge of each slab catches the sun
    # the temple, and the wall of the building next door
    crisp = pic.copy()
    info["next_door"].onto(crisp)
    back.onto(crisp)
    pic[...] = lerp(pic, crisp, 0.84)
    if first is not None:                                    # (the shadow of the stool that was taken away from the steps)
        changed = ((np.abs(first.c - back.c).max(axis=2) + np.abs(first.a - back.a)) > 1e-4).astype(F32)
        out = np.clip(blur(changed, 3.5) * 4, 0, 1)
        out[out < 0.01] = 0                                  # (so that nothing at all is touched away from the place)
        info["painted_out"] = out
        pic[...] = np.where(out[..., None] > 0, lerp(pic, crisp, out[..., None]), pic)

    s = Sheet(SHAPE)
    # ---- the steps: a bright worn edge along every tread, chipped here and there; dark where a tread meets the next riser
    for k in range(1, NSTEP + 1):
        hk, vk = k * RISE, VK(k)
        u = SU0
        while u < SU1:
            run = rng.uniform(40, 190)
            u2 = min(SU1, u + run)
            if rng.random() < 0.84:
                a, b = P(u, vk, hk), P(u2, vk, hk)
                if a[0] < 810:
                    s.line([a, b], "#fff8e2", 1.0, rng.uniform(0.35, 0.75))
            u = u2 + rng.uniform(4, 30)
        for i in range(int(rng.integers(1, 4))):
            cu = rng.uniform(SU0 + 10, SU1 - 10)
            a = P(cu, vk, hk)
            if a[0] < 800:
                w = rng.uniform(1.0, 3.2)
                s.poly([(a[0] - w, a[1] - 0.3), (a[0] + w * rng.uniform(0.5, 1.2), a[1] - 0.3), (a[0] + rng.uniform(-1.5, 1.5), a[1] + rng.uniform(1.0, 2.4))], "#a8947c", rng.uniform(0.35, 0.7))   # a chip out of the edge
    for i in range(9):                                       # cracks across a slab or two, and running down a riser
        k = int(rng.integers(1, NSTEP))
        cu = rng.uniform(SU0 + 40, SU1 - 300)
        a, b = P(cu, VK(k), k * RISE), P(cu + rng.uniform(-18, 18), VK(k + 1), k * RISE)
        mid = ((a[0] + b[0]) / 2 + rng.normal(0, 1.5), (a[1] + b[1]) / 2)
        c0 = P(cu + rng.uniform(-6, 6), VK(k), (k - 1) * RISE)
        s.line([c0, a, mid, b], "#8f7c6c", 0.8, 0.6)
    sc, sa = s.done()                                        # (these lie on the steps, so they take the same wobble as the steps)
    both = hand(np.dstack([sc * sa[..., None], sa]))
    pic[...] = pic * (1 - both[..., 3:4]) + both[..., :3]
    s = Sheet(SHAPE)
    # ---- the plaster of the flank has cracked: two long cracks down from the eaves, a short one over the vault door
    for (cv0, ch0, n_, lean_) in ((900, TOP - 40, 9, 0.5), (1450, TOP - 10, 7, -0.4), (1030, HP + 150, 4, 0.3)):
        pts_, cv, ch = [], cv0, ch0
        for j in range(n_):
            pts_.append(P(45, cv, ch))
            cv += rng.normal(lean_ * 30, 26)
            ch -= rng.uniform(30, 62)
        s.line(pts_, "#4f4a68", 0.8, 0.7)
        s.line([(q[0] + 0.8, q[1]) for q in pts_], "#a9a6c8", 0.6, 0.45)
    # ---- a dark line where the steps and the podium stand on the paving
    u_ = SU0
    while u_ < SU1:
        u2 = min(SU1, u_ + rng.uniform(60, 240))
        q0, q1 = P(u_, VK(1), 0), P(u2, VK(1), 0)
        if q0[0] < 800:
            s.line([(q0[0], q0[1] + 0.6), (q1[0], q1[1] + 0.6)], "#7a6450", 1.1, rng.uniform(0.3, 0.6))
        u_ = u2 + rng.uniform(0, 14)
    s.line([P(0, EDGE, 0), P(0, 700, 0), P(0, BACK, 0)], "#4a4460", 1.0, 0.5)
    s.line([P(0, EDGE, 0), P(SU0, EDGE, 0)], "#6a5a50", 1.0, 0.5)
    # ---- weeds where the paving meets the podium and the steps, and in a joint or two
    def tuft(px, py, r, tones=("#55662e", "#7f9440", "#b4bf60")):
        for j in range(int(5 + r)):
            a = math.pi * rng.uniform(0.15, 0.85)
            l = r * rng.uniform(0.5, 1.1)
            s.line([(px + rng.normal(0, r * 0.25), py), (px + math.cos(a) * l * 0.8, py - math.sin(a) * l)], tones[int(rng.random() ** 1.4 * 3)], max(0.8, r * 0.14))
    for i in range(16):
        v_ = rng.uniform(EDGE + 40, BACK - 500) ** 1.0
        px, py = P(-3, v_, 0)
        if 0 < px < 800 and not (640 < v_ < 1120):
            tuft(px, py + 1, 2.2 + 3.5 * T.k(0, v_) * 4, tones=("#34452c", "#4a6238", "#6f8850"))
    for i in range(7):
        cu = rng.uniform(SU0 + 30, SU1 - 200)
        px, py = P(cu, VK(1) - 3, 0)
        if px < 790 and rng.random() < 0.8:
            tuft(px, py + 1, rng.uniform(2.5, 4.5))
    for i in range(5):
        v_ = rng.uniform(VK(1), EDGE - 40)
        px, py = P(SU0 - 3, v_, 0)
        tuft(px, py + 1, rng.uniform(3, 5), tones=("#34452c", "#4a6238", "#6f8850"))
    # ---- the soothsayer's place: his cage of sacred chickens (the man, and the crooked staff in his hand, are the game's to draw)
    cu0, cu1, ck = CAGE
    hk, vk = ck * RISE, VK(ck)
    kk = T.k((cu0 + cu1) / 2, vk)
    a0, a1 = P(cu0, vk + 4, hk), P(cu1, vk + 4, hk)
    b0, b1 = P(cu0, vk + 34, hk), P(cu1, vk + 34, hk)
    top = 46 * kk
    wood, wood_l, wood_d = "#8a6238", "#c99a58", "#4e3622"
    s.poly([(b0[0], b0[1] - top), (b1[0], b1[1] - top), (b1[0] + 0, b1[1]), (b0[0], b0[1])], "#3a2a26", 0.92)                    # the dark inside
    # two hens in it: a white one, and a brown one pecking
    hx, hy = lerp(a0[0], a1[0], 0.34), a0[1] - 4 * kk
    s.ellipse(hx, hy - 10 * kk, 11 * kk, 8 * kk, "#f4ead8")
    s.ellipse(hx + 8 * kk, hy - 19 * kk, 4.2 * kk, 4.6 * kk, "#f8f0e0")
    s.poly([(hx + 11 * kk, hy - 19 * kk), (hx + 16 * kk, hy - 17.5 * kk), (hx + 11 * kk, hy - 16 * kk)], "#e0a030")
    s.ellipse(hx + 8 * kk, hy - 24 * kk, 2.4 * kk, 1.8 * kk, "#d03a2c")
    s.poly([(hx - 10 * kk, hy - 12 * kk), (hx - 17 * kk, hy - 20 * kk), (hx - 8 * kk, hy - 16 * kk)], "#e6dcc8")
    hx2 = lerp(a0[0], a1[0], 0.72)
    s.ellipse(hx2, hy - 9 * kk, 10 * kk, 7.5 * kk, "#a8683a")
    s.ellipse(hx2 - 8 * kk, hy - 5 * kk, 4 * kk, 4 * kk, "#b87844")
    s.ellipse(hx2 - 9 * kk, hy - 9 * kk, 2.0 * kk, 1.6 * kk, "#c83428")
    s.poly([(hx2 + 8 * kk, hy - 11 * kk), (hx2 + 15 * kk, hy - 19 * kk), (hx2 + 6 * kk, hy - 15 * kk)], "#7a4a2a")
    # the cage itself: a floor, a top, bars all round; a ring to carry it by
    s.poly([a0, a1, b1, b0], wood_l)
    for t in np.linspace(0, 1, 9):
        q0, q1 = (lerp(b0[0], b1[0], t), lerp(b0[1], b1[1], t)), (lerp(a0[0], a1[0], t), lerp(a0[1], a1[1], t))
        s.line([q1, (q1[0], q1[1] - top)], wood_l if t > 0.45 else wood, 1.3)
        s.line([(q1[0] - 0.8, q1[1]), (q1[0] - 0.8, q1[1] - top)], wood_d, 0.7, 0.7)
    s.poly([(a0[0] - 1.5, a0[1] - top), (a1[0] + 1.5, a1[1] - top), (b1[0] + 1.5, b1[1] - top - 1), (b0[0] - 1.5, b0[1] - top - 1)], wood_l)
    s.line([(a0[0] - 1.5, a0[1] - top), (a1[0] + 1.5, a1[1] - top)], wood_d, 1.3)
    s.line([(a0[0] - 1.5, a0[1] - top * 0.5), (a1[0] + 1.5, a1[1] - top * 0.5)], wood, 1.1)
    s.line([(a0[0] - 1.5, a0[1]), (a1[0] + 1.5, a1[1])], wood_d, 1.6)
    mx_, my_ = (a0[0] + a1[0] + b0[0] + b1[0]) / 4, (a0[1] + b0[1]) / 2 - top - 1
    s.line([(mx_ - 5 * kk, my_), (mx_ - 4 * kk, my_ - 7 * kk), (mx_ + 4 * kk, my_ - 7 * kk), (mx_ + 5 * kk, my_)], wood_d, 1.3)
    # a dish of grain by the cage, and what the hens have scattered
    d0 = P(cu1 + 20, vk + 16, hk)
    s.ellipse(d0[0], d0[1] - 1, 6, 2.6, "#b8683c")
    s.ellipse(d0[0], d0[1] - 1.6, 4.6, 1.7, "#e8cf7a")
    for i in range(14):
        gx_, gy_ = d0[0] + rng.normal(4, 9), d0[1] + rng.normal(1, 1.4)
        s.ellipse(gx_, gy_, 0.8, 0.6, "#e0c060")
    # ---- a whitened board of public notices hung on the podium by the steps, written in red and black
    n0, n1, nh0, nh1 = 16.0, 76.0, 96.0, 200.0
    s.poly([P(n0 - 3, EDGE - 2, nh0 - 3), P(n1 + 3, EDGE - 2, nh0 - 3), P(n1 + 3, EDGE - 2, nh1 + 3), P(n0 - 3, EDGE - 2, nh1 + 3)], "#6a4a30")
    s.poly([P(n0, EDGE - 2, nh0), P(n1, EDGE - 2, nh0), P(n1, EDGE - 2, nh1), P(n0, EDGE - 2, nh1)], "#f3ead6")
    s.line([P(n0 + 6, EDGE - 2, nh1 + 3), P((n0 + n1) / 2, EDGE - 2, nh1 + 22), P(n1 - 6, EDGE - 2, nh1 + 3)], "#5a4634", 0.9)
    s.ellipse(*P((n0 + n1) / 2, EDGE - 2, nh1 + 22), 1.3, 1.3, "#3a3030")
    for row in range(9):
        hh = nh1 - 12 - row * 10
        uu = n0 + 6
        ink = "#a8322a" if row in (0, 5) else "#3a3238"
        while uu < n1 - 8:
            run = rng.uniform(4, 13) if row not in (0, 5) else rng.uniform(10, 22)
            u2 = min(n1 - 6, uu + run)
            s.line([P(uu, EDGE - 2, hh + rng.normal(0, 0.6)), P(u2, EDGE - 2, hh + rng.normal(0, 0.6))], ink, 1.3 if row in (0, 5) else 1.0, 0.85)
            uu = u2 + rng.uniform(3, 6)
    s.line([P(n1 + 3, EDGE - 2, nh0 - 3), P(n1 + 3, EDGE - 2, nh1 + 3)], "#3a2a20", 0.9, 0.7)
    # ---- left in the shade of the podium: three wine jars, a basket, and a dog asleep
    for (ju, jv, lean_, hgt) in ((-22, 690, 0.26, 96), (-26, 770, 0.16, 90), (-74, 735, -1.25, 84)):
        amphora(s, *P(ju, jv, 0), T.k(ju, jv) * hgt / 90.0, lean_, ("#553a40", "#7c5650", "#ab8e8c"))
    bq = P(-70, 880, 0)
    kk = T.k(-70, 880)
    s.poly([(bq[0] - 20 * kk, bq[1]), (bq[0] + 20 * kk, bq[1]), (bq[0] + 26 * kk, bq[1] - 30 * kk), (bq[0] - 26 * kk, bq[1] - 30 * kk)], "#6a5648")
    for j in range(4):
        s.line([(bq[0] - 25 * kk, bq[1] - (4 + j * 7) * kk), (bq[0] + 25 * kk, bq[1] - (4 + j * 7) * kk)], "#8a7460", 0.8, 0.8)
    s.ellipse(bq[0], bq[1] - 30 * kk, 26 * kk, 6 * kk, "#4a3c38")
    dq = P(-190, 380, 0)
    kk = T.k(-190, 380)
    fur, fur_l, fur_d = "#8a7260", "#b09a84", "#57463c"
    s.ellipse(dq[0], dq[1] - 12 * kk, 36 * kk, 14 * kk, fur)                                         # the dog, flat out on its side
    s.ellipse(dq[0] - 6 * kk, dq[1] - 17 * kk, 26 * kk, 8 * kk, fur_l)
    s.ellipse(dq[0] - 44 * kk, dq[1] - 9 * kk, 13 * kk, 9 * kk, fur)                                 # head, toward us
    s.poly([(dq[0] - 50 * kk, dq[1] - 16 * kk), (dq[0] - 44 * kk, dq[1] - 27 * kk), (dq[0] - 39 * kk, dq[1] - 16 * kk)], fur_d)
    s.line([(dq[0] - 56 * kk, dq[1] - 6 * kk), (dq[0] - 66 * kk, dq[1] - 3 * kk)], fur_d, 6 * kk)     # muzzle
    for lx in (-22, -8, 16, 28):                                                                      # four legs stretched along the stones
        s.line([(dq[0] + lx * kk, dq[1] - 4 * kk), (dq[0] + (lx - 16) * kk, dq[1] + 4 * kk)], fur_d, 4.5 * kk)
    s.line([(dq[0] + 34 * kk, dq[1] - 12 * kk), (dq[0] + 52 * kk, dq[1] - 2 * kk), (dq[0] + 60 * kk, dq[1] - 6 * kk)], fur, 4 * kk)   # tail
    # ---- by the low door of the vault: a handcart tipped on its shafts, and the sealed sacks it brought
    cu_, cv_ = -215.0, 1000.0
    kk = T.k(cu_, cv_)
    w_d, w_m, w_l = "#4c3f44", "#6f5f5c", "#978a8c"
    bed = [P(cu_ - 75, cv_, 62), P(cu_ + 75, cv_, 78)]                                             # the bed slopes: its shafts rest on the ground
    far_w = P(cu_ + 12, cv_ + 70, 44)
    s.ellipse(far_w[0], far_w[1], 43 * kk, 44 * kk, w_d)                                            # the far wheel
    s.poly([bed[0], bed[1], (bed[1][0], bed[1][1] - 26 * kk), (bed[0][0], bed[0][1] - 26 * kk)], w_m)
    s.line([bed[0], bed[1]], w_d, 1.4)
    s.line([(bed[0][0], bed[0][1] - 26 * kk), (bed[1][0], bed[1][1] - 26 * kk)], w_l, 1.2)
    for t in (0.2, 0.42, 0.64, 0.86):
        q = (lerp(bed[0][0], bed[1][0], t), lerp(bed[0][1], bed[1][1], t))
        s.line([q, (q[0], q[1] - 26 * kk)], w_d, 0.8, 0.8)
    s.line([bed[0], P(cu_ - 200, cv_ - 10, 0)], w_m, 2.2 * kk + 0.8)                                # shafts
    s.line([(bed[0][0], bed[0][1] - 3), P(cu_ - 196, cv_ + 40, 0)], w_d, 2.0 * kk + 0.6)
    hub = P(cu_ + 12, cv_, 44)
    s.ellipse(hub[0], hub[1], 44 * kk, 45 * kk, w_d)                                                # the near wheel: rim, spokes, hub
    s.ellipse(hub[0], hub[1], 37 * kk, 38 * kk, "#8f88a6")
    for a_ in range(0, 180, 30):
        ca_, sa_ = math.cos(math.radians(a_)), math.sin(math.radians(a_))
        s.line([(hub[0] - ca_ * 40 * kk, hub[1] - sa_ * 41 * kk), (hub[0] + ca_ * 40 * kk, hub[1] + sa_ * 41 * kk)], w_m, 1.1)
    s.ellipse(hub[0], hub[1], 8 * kk, 8 * kk, w_d)
    s.line([(hub[0] - 40 * kk, hub[1] - 16 * kk), (hub[0] - 22 * kk, hub[1] - 38 * kk), (hub[0], hub[1] - 44 * kk)], w_l, 1.0, 0.8)
    sack, sack_l, sack_d = "#8c86a2", "#b4aec6", "#5f5a78"
    for (du, dh, r_) in ((-40, 96, 15), (-8, 100, 16), (26, 108, 15), (-22, 118, 13), (10, 124, 12)):   # sacks on the cart
        q = P(cu_ + du, cv_ + 10, dh)
        s.ellipse(q[0], q[1], r_ * kk * 1.25, r_ * kk, sack)
        s.ellipse(q[0] - 1.2, q[1] - r_ * kk * 0.35, r_ * kk * 0.8, r_ * kk * 0.45, sack_l, 0.8)
        s.line([(q[0] + r_ * kk * 0.9, q[1] - r_ * kk * 0.7), (q[0] + r_ * kk * 1.3, q[1] - r_ * kk * 1.2)], sack_d, 1.4)   # the tied neck
    for (du, dv, r_) in ((120, -10, 15), (150, 30, 16), (128, 20, 14)):                               # and three set down by the door
        q = P(cu_ + du, cv_ + dv, r_ * 0.8)
        s.ellipse(q[0], q[1], r_ * kk * 1.25, r_ * kk, sack)
        s.ellipse(q[0] - 1.2, q[1] - r_ * kk * 0.35, r_ * kk * 0.8, r_ * kk * 0.45, sack_l, 0.8)
        s.ellipse(q[0] + r_ * kk * 0.2, q[1] - r_ * kk * 0.1, 1.3, 1.3, "#a8483a")                     # a red seal
    # ---- something green has rooted in the podium's joints
    for (pu, pv, ph, front_) in ((58, EDGE, 110, True), (0, 430, HP - 30, False), (0, 1250, 58, False)):
        px, py = P(pu, pv, ph)
        tn = ("#55702e", "#86a03e", "#c0cc66") if front_ else ("#33452c", "#4a6238", "#6f8850")
        if front_:
            land.shadow(pic, mask_ellipse(SHAPE, px - 6, py + 3, 7, 3), "#8a7c98", 0.45, 1.0)
        for j in range(9):
            a_ = math.pi * rng.uniform(0.9, 2.1)
            l_ = rng.uniform(4, 9)
            s.line([(px, py), (px + math.cos(a_) * l_ * 0.6, py + abs(math.sin(a_)) * l_ * 0.5 + 1), (px + math.cos(a_) * l_, py + l_ * 0.9)], tn[int(rng.random() ** 1.3 * 3)], 1.2)
    # ---- a bronze lamp hangs on its chains from the porch ceiling, before the door
    lu, lv = UW / 2 - 6, 300.0
    hook, bowl = P(lu, lv, TOP), P(lu, lv, TOP - 120)
    for dx in (-3.2, 0, 3.2):
        s.line([hook, (bowl[0] + dx, bowl[1])], "#a08658", 0.6, 0.75)
    s.poly([(bowl[0] - 6.5, bowl[1]), (bowl[0] + 6.5, bowl[1]), (bowl[0] + 4, bowl[1] + 4.5), (bowl[0] - 4, bowl[1] + 4.5)], "#8a6630")
    s.ellipse(bowl[0], bowl[1], 6.5, 1.8, "#3a2a1c")
    s.line([(bowl[0] - 6.5, bowl[1]), (bowl[0] + 6.5, bowl[1])], "#f0c878", 0.9, 0.9)
    s.line([(bowl[0] + 2, bowl[1] + 1.5), (bowl[0] + 4, bowl[1] + 4)], "#e8b860", 0.9, 0.8)
    # ---- laurel tied over the door for the day, and hanging down either side of it
    d0, d1, dh0, dh1 = DOOR
    ga, gb = P(d0 - 26, DEEP - 3, dh1 + 26), P(d1 + 26, DEEP - 3, dh1 + 26)
    swag = [(lerp(ga[0], gb[0], t), lerp(ga[1], gb[1], t) + 9 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 13)]
    drops = [[ga, (ga[0] - 1, ga[1] + 22), (ga[0] + 1, ga[1] + 40)], [gb, (gb[0] + 1, gb[1] + 20), (gb[0] - 1, gb[1] + 36)]]
    for path_ in [swag] + drops:
        s.line(path_, "#22361f", 3.4)
        for (px, py) in path_:
            for j in range(3):
                leaf(s, px + rng.normal(0, 0.8), py + rng.normal(0, 0.8), rng.uniform(0, 2 * math.pi), rng.uniform(3.5, 5.5), ["#2c4a26", "#3d6230", "#567e3a", "#7a9a4a"][int(rng.random() ** 1.5 * 4)])
    for (px, py) in (ga, gb):
        s.ellipse(px, py, 2.2, 2.2, "#b03c30")
        s.line([(px, py), (px + rng.normal(0, 1), py + 12)], "#c8483a", 1.2)
    # ---- left on the steps at the far right: a basket of figs and pomegranates, and a jug
    bq = P(770, VK(2) + 20, 2 * RISE)
    kk = T.k(770, VK(2))
    s.ellipse(bq[0] - 16 * kk, bq[1] + 1, 26 * kk, 5 * kk, "#9a8aa0", 0.6)                             # its shadow
    s.poly([(bq[0] - 20 * kk, bq[1]), (bq[0] + 20 * kk, bq[1]), (bq[0] + 25 * kk, bq[1] - 22 * kk), (bq[0] - 25 * kk, bq[1] - 22 * kk)], "#b08a4c")
    s.poly([(bq[0] - 20 * kk, bq[1]), (bq[0] - 4 * kk, bq[1]), (bq[0] - 6 * kk, bq[1] - 22 * kk), (bq[0] - 25 * kk, bq[1] - 22 * kk)], "#7a6248", 0.8)
    for j in range(3):
        s.line([(bq[0] - 23 * kk, bq[1] - (5 + j * 6) * kk), (bq[0] + 23 * kk, bq[1] - (5 + j * 6) * kk)], "#6a4e2c", 0.8, 0.7)
    for (dx, dy, r_, tone) in ((-14, -26, 7, "#b83a34"), (0, -29, 8, "#d05a3c"), (13, -26, 7, "#6a3a5c"), (-6, -33, 6, "#7a4468"), (8, -34, 6.5, "#c8483a")):
        s.ellipse(bq[0] + dx * kk, bq[1] + dy * kk, r_ * kk, r_ * kk, tone)
        s.ellipse(bq[0] + (dx + 2) * kk, bq[1] + (dy - 2) * kk, r_ * kk * 0.35, r_ * kk * 0.35, "#f4c8a0", 0.8)
    jq = P(826, VK(2) + 22, 2 * RISE)
    amphora(s, jq[0], jq[1], kk * 0.5, 0.0, ("#9a5a3a", "#c87a4a", "#f0b078"))
    # ---- pigeons sit along the gutter in the sun
    for (gu, f) in ((1010, 1), (1042, -1), (1150, 1), (880, -1)):
        gx_, gy_ = P(gu, FV - EAVE, E3)
        if gy_ > 4:
            pigeon(s, gx_, gy_, 5.0, seed + int(gu), f, False)
    # ---- swallows over the square
    for (bx, by, sz, tilt_) in ((206, 58, 5.0, 0.3), (236, 92, 3.6, -0.2), (176, 106, 3.0, 0.5), (36, 150, 2.6, 0.0)):
        s.line([(bx - sz, by - sz * 0.35 + tilt_ * sz * 0.3), (bx - sz * 0.3, by - sz * 0.1), (bx, by + sz * 0.15), (bx + sz * 0.3, by - sz * 0.12), (bx + sz, by - sz * 0.5 - tilt_ * sz * 0.3)], "#34405c", 1.0, 0.9)
    # ---- the near paving: a cracked slab or two, grass in the joints, grit
    for (cx_, cy_, l_) in ((332, 572, 34), (566, 590, 26), (150, 452, 20), (706, 470, 22), (500, 448, 16)):
        pts_ = [(cx_, cy_)]
        ang = rng.uniform(-0.5, 0.5)
        for j in range(5):
            ang += rng.normal(0, 0.5)
            pts_.append((pts_[-1][0] + math.cos(ang) * l_ / 5, pts_[-1][1] + math.sin(ang) * l_ / 9))
        s.line(pts_, "#8a6c50", 0.9, 0.65)
        s.line([(q[0], q[1] + 1) for q in pts_], "#fff0c8", 0.7, 0.35)
    for (gx_, gy_, r_) in ((268, 548, 4.5), (286, 551, 3.5), (612, 577, 5), (88, 462, 3.5), (764, 452, 3.5), (512, 583, 4)):
        tuft(gx_, gy_, r_)
    for i in range(34):
        gx_, gy_ = rng.uniform(150, 800), HZ + (H - HZ) * rng.uniform(0.55, 1.0)
        r_ = 0.6 + 1.2 * (gy_ - 440) / 160 * rng.random()
        s.ellipse(gx_ - r_ * 1.2, gy_ + 0.3, r_ * 1.6, r_ * 0.5, "#8f7c98", 0.5)
        s.ellipse(gx_, gy_, r_ * 1.2, r_ * 0.8, ["#f4e2bc", "#cbb089", "#a48a70"][int(rng.integers(3))])
    # ---- pigeons on the pavement and the steps, each with its shadow lying to the left
    birds = [(552, 512, 11.5, 1, True), (585, 524, 12.5, -1, False), (618, 506, 11, 1, False), (636, 540, 13, -1, True), (598, 552, 14, 1, True),
             (540, 470, 9.5, -1, False), (752, 530, 12.5, -1, False), (436, 566, 15, 1, True), (238, 470, 10, 1, False), (212, 478, 10.5, -1, True)]
    for i, (bx, by, sz, f, peck) in enumerate(birds):
        land.shadow(pic, mask_ellipse(SHAPE, bx - sz * 0.75, by - 0.5, sz * 0.9, sz * 0.22), "#7a6c98", 0.5, 0.6)
        pigeon(s, bx, by, sz, seed + 40 + i, f, peck)
    for (u_, k_, sz, f, peck) in ((610, 1, 9.0, -1, False), (905, 5, 8.0, 1, True), (980, 5, 7.6, -1, False)):       # three on the steps
        bx, by = P(u_, VK(k_) + 20, k_ * RISE)
        land.shadow(pic, mask_ellipse(SHAPE, bx - sz * 0.75, by - 0.5, sz * 0.9, sz * 0.22), "#7a6c98", 0.5, 0.6)
        pigeon(s, bx, by, sz, seed + 60 + int(u_), f, peck)
    # ---- where the wine of the morning's offering was poured out, the stones are stained
    au0, au1, av0, av1, ahh = ALTAR
    spill = mask_poly(SHAPE, [P(au1 + 30, av0 - 40, 0), P(au1 + 96, av0 - 46, 0), P(au1 + 130, av0 - 10, 0), P(au1 + 60, av0 + 6, 0), P(au1 + 22, av0 - 12, 0)], soft=2.0, wobble=5, seed=seed + 31)
    tint(pic, "#a8766e", (spill * (0.5 + 0.5 * noise(SHAPE, 12, seed + 32, 3)) * 0.42).astype(F32))
    # ---- petals and leaves blown about near the altar; an offering left on its step
    au0, au1, av0, av1, ahh = ALTAR
    for i in range(26):
        qu, qv = rng.normal((au0 + au1) / 2 + 30, 110), rng.normal(av0 - 50, 50)
        px, py = P(qu, qv, 0)
        if py > 300:
            tone = ["#f6ead8", "#f6ead8", "#e8a09a", "#7c9044", "#f0dcc0", "#c85a48"][int(rng.integers(6))]
            s.ellipse(px, py, rng.uniform(1.0, 2.0), rng.uniform(0.5, 1.0), tone, 0.8)
    s.onto(pic)
    # ---- a wisp of smoke from the altar, thin and pale, leaning with the morning air
    sx_, sy_ = P((au0 + au1) / 2, (av0 + av1) / 2, ahh + 6)
    path = curve([(sx_, sy_), (sx_ - 3, sy_ - 22), (sx_ + 4, sy_ - 48), (sx_ - 7, sy_ - 78), (sx_ - 2, sy_ - 112), (sx_ - 16, sy_ - 150), (sx_ - 30, sy_ - 196)], 6)
    widths = [lerp(1.6, 15, (i / (len(path) - 1)) ** 1.2) for i in range(len(path))]
    smoke = mask_line(SHAPE, path, widths, soft=2.0)
    smoke = warp(smoke, 4.0, 18, seed + 61) * (0.45 + 0.75 * noise(SHAPE, (9, 30), seed + 62, 3)) * np.clip((sy_ - y) / 26.0, 0, 1) * np.clip(1.25 - (sy_ - y) / 200.0, 0, 1)
    info["smoke"] = np.clip(smoke * 0.62, 0, 1).astype(F32)
    over(pic, "#f6efe2", info["smoke"])
    return pic


def brushed(layer, ground, seed, sizes=(7, 4, 2), keep=0.36, restate=0.6):
    """A cut-out, repainted with a small brush on the ground it stands against, then said again crisply.
    -> (color, hard coverage)."""
    c, a = layer.straight()
    ys, xs = np.where(a > 0.02)
    if len(xs) == 0:
        return c, a
    x0, x1, y0, y1 = max(0, xs.min() - 12), min(W, xs.max() + 13), max(0, ys.min() - 12), min(H, ys.max() + 13)
    flat = ground[y0:y1, x0:x1].copy()
    over(flat, c[y0:y1, x0:x1], a[y0:y1, x0:x1])
    painted = strokes(flat, sizes=sizes, seed=seed, density=1.8, jitter=0.03, keep=keep)
    painted = lerp(painted, flat, (restate * a[y0:y1, x0:x1])[..., None])
    out = c.copy()
    out[y0:y1, x0:x1] = painted
    return out, (a > 0.5).astype(F32)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02, palette=None):
    """Grain, then a limited palette with speckle, written as a PNG-8. `palette` gives the colors to use
    instead of choosing them from the picture."""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette if palette is not None else palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def layout():
    """The numbers the game needs, measured from the picture as painted."""
    P = T.pt
    r = lambda q: [int(round(q[0])), int(round(q[1]))]
    au0, au1, av0, av1, ahh = ALTAR
    tu, tv, th = TRIPOD
    su0, su1, sv0, sv1, shh = STONE
    cu0, cu1, ck = CAGE
    d0, d1, dh0, dh1 = DOOR
    seat_u, seat_k = SEAT

    def u_where(x, v, h):                                    # the place along the front that lies under picture column x
        lo, hi = -3000.0, 6000.0
        for _ in range(50):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if P(mid, v, h)[0] < x else (lo, mid)
        return (lo + hi) / 2
    edge = 797
    foot_r, top_r = P(u_where(edge, VK(1), 0), VK(1), 0), P(u_where(edge, EDGE, HP), EDGE, HP)
    walk = [[0, 597], [edge, 597], r(foot_r), r(top_r),
            r(P(1240, EDGE + 8, HP)), r(P(1240, DEEP - 34, HP)), r(P(150, DEEP - 34, HP)), r(P(150, EDGE + 8, HP)),       # the porch, behind the columns
            r(P(SU0 + 22, EDGE, HP)), r(P(SU0 + 22, VK(1), 0)), [400, 462], [340, 452], [240, 446], [120, 442], [0, 438]]
    blocked = [[r(P(au0 - 22, av0 - 22, 0)), r(P(au1 + 22, av0 - 22, 0)), r(P(au1 + 22, av1 + 22, 0)), r(P(au0 - 22, av1 + 22, 0))],
               [r(P(tu - 30, tv - 30, 0)), r(P(tu + 30, tv - 30, 0)), r(P(tu + 30, tv + 24, 0)), r(P(tu - 30, tv + 24, 0))],
               [r(P(su0 - 12, sv0 - 14, 0)), r(P(su1 + 12, sv0 - 14, 0)), r(P(su1 + 12, sv1 + 14, 0)), r(P(su0 - 12, sv1 + 14, 0))],
               [r(P(cu0 - 10, VK(ck - 1), (ck - 1) * RISE)), r(P(cu1 + 40, VK(ck - 1), (ck - 1) * RISE)), r(P(cu1 + 40, VK(ck + 1), ck * RISE)), r(P(cu0 - 10, VK(ck + 1), ck * RISE))],
               [[0, 500], [150, 484], [158, 600], [0, 600]]]
    for cu in COLS:                                          # nobody walks through a column
        blocked.append([r(P(cu - 60, -58, HP)), r(P(cu + 60, -58, HP)), r(P(cu + 60, 62, HP)), r(P(cu - 60, 62, HP))])
    blocked.append([r(P(868, DEEP - 60, HP)), r(P(1016, DEEP - 60, HP)), r(P(1016, DEEP, HP)), r(P(868, DEEP, HP))])       # the doorkeeper's bench
    c0, c5 = P(COLS[0], 0, HP), P(COLS[5], 0, HP)
    slope = (c5[1] - c0[1]) / (c5[0] - c0[0])
    col_base = [[320, round(c0[1] + slope * (320 - c0[0]), 1)], [800, round(c0[1] + slope * (800 - c0[0]), 1)]]
    door_box = [r(P(d0 - 32, DEEP, dh1 + 56)), r(P(d1 + 32, DEEP, HP))]
    altar_box = [r(P(au0 - 12, av1, ahh + 22)), r(P(au1 + 14, av0 - 12, 0))]
    cage_a, cage_b = P(cu0 - 4, VK(ck) + 30, ck * RISE + 62), P(cu1 + 36, VK(ck), ck * RISE - 6)
    tri_a, tri_b = P(tu - 30, tv, th + 4), P(tu + 30, tv - 20, 0)
    sto_a, sto_b = P(su0, sv0, shh + 2), P(su1 + 8, sv0, 0)
    seat = P(seat_u, VK(seat_k) + 19, seat_k * RISE)         # his hips, on the step the cage stands on, just right of the cage and its dish
    feet = P(seat_u, VK(seat_k - 2) + 19, (seat_k - 2) * RISE)   # his feet, two steps down: clear step
    keeper = (492.0, 295.0)                                  # seen between the second and third columns, before the doorway
    at_door = (517.0, 296.0)
    return {
        "id": "rome-steps", "horizon": HZ, "full": FULL, "light": "morning sun from the upper right; shadows fall to the left",
        "minScale": 0.40,
        "note": ("The porch is 252 cm above the pavement, so its floor is only a narrow strip of the picture (rows 291 to 305). "
                 "In true perspective a grown-up is 94 px tall at the foot of the steps, 68 px at their top and 54 px at the doors: set minScale to "
                 "about 0.40 (64 px) so that people hold that size from row 392 upward instead of shrinking away toward the horizon."),
        "walk": walk,
        "blocked": blocked,
        "planes": [
            {"id": "columns", "file": "columns.png", "base": col_base, "what": "the six columns of the front; people on the porch pass behind them"},
            {"id": "altar", "file": "altar.png", "base": [r(P(au0 - 12, av0 - 12, 0)), r(P(au1 + 12, av0 - 12, 0))]},
            {"id": "tripod", "file": "tripod.png", "base": int(round(P(tu, tv - 19, 0)[1]))},
            {"id": "stone", "file": "stone.png", "base": [r(P(su0, sv0, 0)), r(P(su1, sv0, 0))]},
            {"id": "front", "file": "front.png", "plane": "front"}],
        "things": [
            {"id": "doors", "what": "the bronze doors of the treasury, standing open", "shape": {"rect": [door_box[0][0], door_box[0][1], door_box[1][0] - door_box[0][0], door_box[1][1] - door_box[0][1]]},
             "stand": r(at_door), "face": "N"},
            {"id": "altar", "what": "the altar with its garland and its smoke", "shape": {"rect": [altar_box[0][0], altar_box[0][1], altar_box[1][0] - altar_box[0][0], altar_box[1][1] - altar_box[0][1]]},
             "stand": r(P((au0 + au1) / 2 + 10, av0 - 85, 0)), "face": "N"},
            {"id": "birdcage", "what": "the soothsayer's cage of sacred chickens, and their dish of grain", "shape": {"rect": [int(cage_a[0]), int(cage_a[1]), int(cage_b[0] - cage_a[0]), int(cage_b[1] - cage_a[1])]},
             "stand": r(P(cu1 + 20, VK(1) - 45, 0)), "face": "N"},
            {"id": "tripod", "what": "a bronze tripod", "shape": {"rect": [int(tri_a[0]), int(tri_a[1]), int(tri_b[0] - tri_a[0]), int(tri_b[1] - tri_a[1])]},
             "stand": r(P(tu + 70, tv - 40, 0)), "face": "W"},
            {"id": "stone", "what": "the boundary stone: S P Q R", "shape": {"rect": [int(sto_a[0]), int(sto_a[1]), int(sto_b[0] - sto_a[0]), int(sto_b[1] - sto_a[1])]},
             "stand": r(P(su0 - 75, sv0 - 10, 0)), "face": "E"},
            {"id": "notices", "what": "a board of public notices on the temple's base", "shape": {"rect": [338, 322, 34, 52]}, "stand": [425, 472], "face": "N"},
            {"id": "forum", "what": "the Forum beyond: the speaker's platform, the statues on their columns, the hill and its great temple", "shape": {"rect": [0, 120, 236, 200]},
             "stand": [140, 470], "face": "N"}],
        "exits": [
            {"to": "rome-temple", "shape": {"poly": [r(P(d0, DEEP, dh1)), r(P(d1, DEEP, dh1)), r(P(d1, DEEP, HP)), r(P(d0, DEEP, HP))]}, "stand": r(at_door)},
            {"to": "rome-street", "shape": {"poly": [[0, 438], [40, 440], [40, 500], [0, 500]]}, "stand": [34, 470]}],
        "marks": {"soothsayer": r(seat), "soothsayer_feet": r(feet), "senator": [200, 540], "doorkeeper": r(keeper), "son": [470, 508],
                  "top_of_steps": r(P((COLS[1] + COLS[2]) / 2, EDGE - 19, 13 * RISE)), "foot_of_steps": r(P(UW / 2 - 300, VK(1) - 40, 0))},
        "sizes": {"adult_px_at_foot_of_steps": round(175 * T.k(UW / 2 - 300, VK(1) - 40), 1), "adult_px_at_top_of_steps": round(175 * T.k(UW / 2 - GAP / 2, EDGE), 1),
                  "adult_px_at_doors": round(175 * T.k(UW / 2, DEEP - 70), 1), "step_px": "about 11 at the foot, 6 at the top"},
    }


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = len(sys.argv) > 1
    back, cols = temple_layers()
    first, _ = temple_layers(stool=True)                     # the temple as it was first laid in (see RETOUCHED, at the top)
    back, cols, first = handed(back), handed(cols), handed(first)
    mottle = 1 + (noise(SHAPE, 120, 41, 4) - 0.5)[..., None] * 0.13 + (noise(SHAPE, 34, 42, 3) - 0.5)[..., None] * 0.05
    drift = (noise(SHAPE, 180, 43, 3) - 0.5) * 0.07                                                 # and it drifts warmer and cooler
    mottle = mottle * np.stack([1 + drift, 1 + drift * 0.2, 1 - drift], axis=-1)
    back.c, cols.c, first.c = [np.clip(c * mottle, 0, 1).astype(F32) for c in (back.c, cols.c, first.c)]
    print("temple", round(time.time() - t0, 1))
    base, info = under()
    soft = Canvas(SHAPE)
    soft.c, soft.a = blur(first.c, 1.8), blur(first.a, 1.2)
    soft.onto(base)
    Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8)).save("out/rome-steps-1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.22)
    details(pic, info, back, first)
    print("details", round(time.time() - t0, 1))
    layers = [("columns", cols, 96), ("altar", altar_layer(), 64), ("tripod", tripod_layer(), 32), ("stone", stone_layer(), 32), ("front", front_layer(), 48)]
    whole = pic.copy()
    cut = {}
    for i, (name, layer, ncol) in enumerate(layers):
        if name in ("stone", "front"):                       # these stand in the cloud's shadow at the front
            layer.tint("#b48c80", cloud_shadow() * (0.6 if name == "front" else 1.0))
        if fast:
            c, a = layer.straight()
            a = (a > 0.5).astype(F32)
        else:
            c, a = brushed(layer, pic, seed=20 + i)
        cut[name] = (c, a, ncol)
        over(whole, c, a)
    over(whole, "#f6efe2", info["smoke"] * 0.0)
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save("out/rome-steps-2-all.png")
    print("painted", round(time.time() - t0, 1))
    probe = {"porch wall low": (420, 250), "porch wall high": (420, 130), "flank wall": (285, 180), "column lit": (463, 150), "column shade": (446, 150),
             "tread": (600, 345), "pavement sun": (480, 590), "pavement shade": (150, 380), "sky top": (300, 8), "cloud": (120, 80), "door": (500, 200)}
    for name, (px_, py_) in probe.items():
        c = whole[py_, px_]
        print(f"  {name:16s} #%02x%02x%02x  L {int((c @ np.array([0.3, 0.59, 0.11])) * 100)}" % tuple(int(v * 255) for v in c))
    if fast:
        sys.exit()
    print("back", finish(pic, f"{OUT}/back.png", 160, palette=PALETTE))
    for name, (c, a, ncol) in cut.items():
        print(name, finish(c, f"{OUT}/{name}.png", ncol, a))
    json.dump(layout(), open(f"{OUT}/layout.json", "w"), indent=1)
    os.system(f"{sys.executable} comp.py {OUT} back columns altar tripod stone front")
    print("done", round(time.time() - t0, 1))

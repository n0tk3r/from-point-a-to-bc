"""The limousine of the Office Of Peculiar Sectors (NEVADA-12A, round twelve): a cut-out the game drives into the lot,
as the wagon of the opening is driven (highway_wagon.py): cropped pictures with a foot point, two frames.

A big gray stretch limousine, side view, nose to the RIGHT, 6.3 m long. It is drawn through the roadside's own camera
(nevada_roadside_kit.CAM) exactly as that camera sees it standing at its stop (its foot on [345, 530]), but at the size
it would have with its base on row 590 (575 px long): a camera with the same eye height and the same distance to the
car, with a lens 1.25 times as long (Camera(..., focal=1000)). The game scales it by row (0.8 at row 530), and there
it is the very picture CAM would paint. From there we see the near side and the roof, and neither end.

LIGHT   the roadside's sun, low on the right and a little behind us (nevada_roadside_kit.SUN): the near side takes it
        at a slant and is in half light, holding the sky and the land the way polished paint does; the roof, the trunk
        lid and the hood are in the sun; the right-hand end (the nose, the front wing, the chrome of the bumper) catches
        it; a long cool shadow lies under it and out to the left.
CAR     gray paint; six smoked windows along the side, nothing to be seen in them; four doors on this side (the
        back pair and the front pair, with a fixed panel and its small window between them); chrome along the belt,
        round the glass, along the sill, on both bumpers and the wheel covers; the plate on the rear bumper, O.O.P.S.
        No maker's name, no badge, no emblem anywhere.
FRAMES  limo-side-0.png and limo-side-1.png: in the second the wheels have turned (a quarter of a slot) and the body
        rides one pixel lower (the bounce of the lot). The shadow does not move. Both files are cropped to one box, and
        the foot point is the same in both: the middle of the ground line under the near side, between the wheels.

    python3 nevada_roadside_limo.py     paints out/nevada-roadside-limo-try.png (both frames, and the car laid at its stop) to look at
"""

import math
import os

import numpy as np

from brush import *
from persp import Camera
from solid import mix
import nevada_roadside_kit as K
from nevada_roadside_kit import Paper, Shade, Solid, brushed, tone
import nevada_roadside_props as P

# ---- the car, in its own measurements (cm): x from the rear end to the nose, y up, z from the near side away
L, WID = 629.0, 200.0
R_AX, F_AX, WR = 116.0, 527.0, 35.0                         # the axles, and the wheels' radius
MID = (R_AX + F_AX) / 2                                     # the foot: under the near side, half way between the wheels
ARCH = 42.0                                                 # the wheel arches
BELT, ROOF = 100.0, 140.0
SILL = 21.0                                                 # the bottom of the body, between the wheels

# ---- where it is painted: the roadside's camera at the stop, with a longer lens
STOP = (345, 530)
STOP_X = K.CAM.x_at(*STOP)                                  # the world x of the foot at the stop (-75.2 cm)
SHEET = (420, 1000)                                         # (height, width) of the sheet it is painted on
FOOT = (640.0, 360.0)                                       # where the foot is on that sheet
MAG = Camera(FOOT[1] - (K.FULL - K.HZ), FOOT[1], vanish_x=FOOT[0] - STOP_X * (160.0 / 175.0), focal=800.0 * 1.25,
             size=(SHEET[1], SHEET[0]))
AT = (STOP_X - MID, 0.0)                                    # the car's rear near corner, on the ground, in that camera's world
DROP = 1                                                    # how far the body sits down in the second frame, px
TURN = 9.0                                                  # how far the wheels turn between the frames, degrees (a quarter of a slot)

PAINT = dict(side="#7b7f8a", sky="#b9c1cf", sky2="#a3abbb", land="#5c5e6e", floor="#9b9090", under="#55545f", sill="#3a3a44",
             roof="#a4a8b2", roof_sun="#d3ccc6", roof_sky="#b4bccb", hood="#aaacb3", trunk="#9fa1a8", seam="#383a46", dark="#2a2b34",
             pillar="#6c707c", shoulder="#8e929c", far="#7e8290")
GLASS = dict(dark="#181b23", mid="#232836", sheen="#3a4558", sky="#7f90ab", hot="#e8eef8")
CHROME = dict(shine="#ffffff", light="#e2e6ec", mid="#a6adb7", dark="#4c525e", ground="#c9ae94", sky="#c9d4e4")
RUBBER = dict(lit="#4c4852", mid="#28252e", dark="#141218")


def profile(d):
    """The near side's outline, clockwise from the bottom of the rear bumper: the car's own (x, y)."""
    top = [(6, 25), (0.5, 31), (0, 52), (2, 57), (3.5, 74), (6.5, 89), (12, 95.5), (60, 98), (101, 99.5), (117, 111), (131, 128), (145, 137.5), (162, 140),
           (458, 140), (474, 138.6), (489, 133), (551, 101), (583, 98.6), (612, 93.8), (623.5, 89.5), (628, 81), (629, 66), (629, 50), (627.5, 31), (621, 25)]
    front = d.arc(F_AX, WR + 1.0, ARCH, -20, 200, 20)
    rear = d.arc(R_AX, WR + 1.0, ARCH, -20, 200, 20)
    return top + [(F_AX + ARCH * 0.97, SILL + 0.5)] + front + [(F_AX - ARCH * 0.97, SILL), (R_AX + ARCH * 0.97, SILL)] + rear + [(R_AX - ARCH * 0.97, SILL + 0.5)]


# window openings in the near side, rear to front: the rear quarter (its back edge leaning with the pillar), the back
# pair of doors, the small fixed window between the pairs, the front pair (the front one's edge leaning with the windshield)
WINDOWS = [[(127, 104), (149, 133.5), (160, 133.5), (160, 104)],
           [(168, 104), (168, 133.5), (228, 133.5), (228, 104)],
           [(238, 104), (238, 133.5), (299, 133.5), (299, 104)],
           [(310, 106), (310, 131.5), (340, 131.5), (340, 106)],
           [(351, 104), (351, 133.5), (412, 133.5), (412, 104)],
           [(422, 104), (422, 133.5), (478, 133.5), (535, 104)]]
SEAMS = [(164, 164), (233, 233), (305, 304), (346, 346), (417, 417), (484, 482)]       # the doors' edges: x at the sill, x at the belt
HANDLES = [222, 293, 406, 476]


# ------------------------------------------------------------------------------------------ the body (rides on the springs)
def draw_tops(d, dl, far=False, paint=None):
    """The surfaces that face the sky, from the near edge (rounded) to the far one: the back window (seen edge on), the
    trunk lid, the roof, the windshield and the hood. Each is a little narrower than the car, as a car's sides curve in
    at the top, and the edge toward us is rounded: a band of the side's own gray between the side and the top. `far`:
    mirrored, for the nose-on frames, which see the car's left side (z = WID) instead of the near one."""
    W = WID
    paint = paint or PAINT
    m = (lambda z: W - z) if far else (lambda z: z)
    side = lambda pts, z0, z1, col: d.side(pts, m(z0), m(z1), col)
    poly = lambda pts, col, al=1.0: d.poly([(x, y, m(z)) for x, y, z in pts], col, al)
    side([(101, 99.5), (117, 111), (131, 128), (145, 137.5)], 4, W - 4, GLASS["dark"])                  # the back window (we see it edge on)
    side([(12, 95.5), (60, 98), (101, 99.5)], 0, W - 8, paint["far"])                                     # the trunk lid: its far edge rolls away
    side([(12, 95.5), (60, 98), (101, 99.5)], 0, W - 26, paint["trunk"])
    poly([(12, 95.6, 5), (101, 99.6, 5), (101, 99.6, 46), (12, 95.6, 40)], paint["roof_sun"], 0.6)       # the sun along its near half
    side([(12, 95.5), (60, 98), (101, 99.5)], 0, 5, paint["shoulder"])
    side([(145, 137.5), (162, 140), (458, 140), (474, 138.6)], 10, W - 10, paint["far"])                 # the roof
    side([(145, 137.5), (162, 140), (458, 140), (474, 138.6)], 10, W - 30, paint["roof"])
    poly([(162, 140.1, 16), (458, 140.1, 16), (458, 140.1, 76), (162, 140.1, 82)], paint["roof_sun"], 0.8)         # its near half in the sun
    poly([(176, 140.1, 118), (446, 140.1, 112), (446, 140.1, W - 34), (176, 140.1, W - 34)], paint["roof_sky"], 0.55)    # its far half full of sky
    poly([(232, 140.2, 36), (380, 140.2, 32), (390, 140.2, 50), (226, 140.2, 56)], "#efe6dc", 0.45)      # and a streak of the low sun along it
    side([(145, 137.5), (162, 140), (458, 140), (474, 138.6)], 0, 12, paint["shoulder"])                 # the rounded edge
    side([(474, 138.6), (489, 133), (551, 101)], 0, W, paint["pillar"])                                  # the windshield's frame
    side([(477, 137.6), (489, 132.6), (549, 102)], 12, W - 12, GLASS["sky"])                             # the windshield: the sky in it
    poly([(483, 135.0, 16), (545, 103.6, 16), (545, 103.6, 42), (483, 135.0, 50)], GLASS["hot"], 0.7)    # and the sun
    poly([(486, 133.6, 104), (522, 115.6, 100), (522, 115.6, 132), (486, 133.6, 140)], "#a8b8d0", 0.5)
    side([(551, 101), (583, 98.6), (612, 93.8), (623.5, 89.5)], 0, W - 6, paint["far"])                  # the hood, in the sun
    side([(551, 101), (583, 98.6), (612, 93.8), (623.5, 89.5)], 0, W - 24, paint["hood"])
    poly([(556, 100.8, 6), (618, 92, 6), (618, 92, 44), (556, 100.8, 50)], "#e6dace", 0.75)
    poly([(562, 100.5, 112), (614, 93.4, 112), (614, 93.4, W - 28), (562, 100.5, W - 28)], paint["roof_sky"], 0.45)
    side([(551, 101), (583, 98.6), (612, 93.8), (623.5, 89.5)], 0, 5, paint["shoulder"])
    dl.line([(162, 140, m(0.5)), (458, 140, m(0.5))], "#fff4e2", 1.6, 0.9)                               # the roof's near edge in the sun
    dl.line([(458, 140, m(0.5)), (474, 138.6, m(0.5)), (489, 133, m(0.5))], "#f4e8d8", 1.3, 0.8)
    dl.line([(12, 95.5, m(0.5)), (60, 98, m(0.5)), (101, 99.5, m(0.5))], "#f8ecdc", 1.2, 0.8)
    dl.line([(551, 101, m(0.5)), (583, 98.6, m(0.5)), (612, 93.8, m(0.5)), (623.5, 89.5, m(0.5))], "#fff6e8", 1.5, 0.95)  # the hood's edge
    dl.line([(474, 138.6, m(9)), (474, 138.6, m(W - 9))], paint["seam"], 1.0, 0.6)                      # the top of the windshield
    for zz in (60, 140):                                                                              # the wipers, parked
        dl.line([(548, 102.5, m(zz)), (536, 108.5, m(zz - 30))], "#1c1e26", 1.4, 0.9)


def draw_body(d, dl, notes=None):
    """Everything that rides on the springs, back to front: the tops, then the near side, one gray plate (it holds what
    it faces, as polished paint does). -> its outline."""
    draw_tops(d, dl)
    side = profile(d)
    d.poly(side, PAINT["side"])
    return side


def side_bands(shape, d, side_pts, far=False, paint=None):
    """A side's reflections, laid in level bands and kept inside the side's outline: -> (color, alpha). `far`: the left
    side (z = WID), for the nose-on frames."""
    zs = WID if far else 0
    paint = paint or PAINT
    sm = mask_poly(shape, d.pts([(x, y, zs) for x, y in side_pts]))
    s = Paper(shape)
    x0, x1 = -10.0, L + 10.0
    for (y0, y1, col, al) in ((95.0, 100.5, paint["sky"], 0.9),                  # the shoulder, just under the belt: the sky
                              (86.0, 95.0, paint["sky2"], 0.75),
                              (79.0, 86.0, paint["land"], 0.7),                  # the far land, a dark line
                              (56.0, 79.0, paint["floor"], 0.38),                # the desert floor, warm
                              (38.0, 56.0, paint["under"], 0.5),                 # turning under
                              (SILL - 2.0, SILL + 11.0, paint["sill"], 0.85)):
        s.poly(d.pts([(x0, y0, zs), (x1, y0, zs), (x1, y1, zs), (x0, y1, zs)]), col, al)
    # the right-hand end turns into the sun: the front wing's corner and the nose glow warm
    s.poly(d.pts([(588, 36, zs), (629.5, 42, zs), (629.5, 84, zs), (622, 92, zs), (596, 96, zs)]), "#d8c6b6", 0.55)
    s.poly(d.pts([(612, 52, zs), (629.5, 54, zs), (629.5, 80, zs), (624, 88, zs), (614, 90, zs)]), "#f2dfca", 0.7)
    # and the rear end turns away from it
    s.poly(d.pts([(-1, 24, zs), (14, 24, zs), (20, 96, zs), (-1, 96, zs)]), "#4e505c", 0.45)
    c, a = s.done()
    return c, a * sm


def draw_side_things(d, dl, notes=None, far=False, paint=None, chrome=None):
    """What a side carries: glass, pillars, chrome, seams, handles, lamps (and on the near side the plate and the aerial).
    On the line sheet: crisp. `far`: the car's left side (z = WID), which the nose-on frames see, instead of the near one."""
    zs, out = (WID, 1.0) if far else (0.0, -1.0)
    o = lambda k: zs + out * k if k else zs                                  # k cm out from the side's face
    paint = paint or PAINT
    chrome = chrome or CHROME
    # ---- the glass: one band of smoked glass, the pillars between the windows in body colour
    band = [(122, 102.5), (146, 134.5), (480, 134.5), (538, 102.5)]
    dl.poly([(x, y, o(0.3)) for x, y in band], paint["pillar"])
    for w in WINDOWS:
        dl.poly([(x, y, o(0.4)) for x, y in w], GLASS["dark"])
        xs = [p[0] for p in w]
        a, b = min(xs), max(xs)
        # a slant of sky across each, faint (smoked glass shows nothing of the inside, only a little of the outside)
        q = [(a + 6, 133.0, o(0.5)), (a + 16, 133.0, o(0.5)), (a + 6, 104.5, o(0.5)), (a - 2, 104.5, o(0.5))]
        q = [(max(a + 0.5, min(b - 0.5, x)), y, z) for x, y, z in q]
        dl.poly(q, GLASS["sheen"], 0.55)
        dl.line([(a + 1, 132.6, o(0.5)), (b - 1, 132.6, o(0.5))], GLASS["mid"], 1.0, 0.8)
    dl.line([(x, y, o(0.6)) for x, y in band] + [(band[0][0], band[0][1], o(0.6))], chrome["mid"], 1.5, 0.95)      # chrome round the glass
    dl.line([(146, 134.6, o(0.7)), (480, 134.6, o(0.7))], chrome["light"], 0.8, 0.85)
    dl.line([(480, 134.6, o(0.7)), (538, 102.6, o(0.7))], chrome["shine"], 0.9, 0.9)                             # the edge that faces the sun
    # ---- the belt: a chrome strip the whole length, blazing at the right-hand end
    dl.line([(4, BELT - 1.2, o(0.8)), (624, BELT - 2.4, o(0.8))], chrome["dark"], 1.6, 0.9)
    dl.line([(4, BELT, o(0.9)), (300, BELT, o(0.9)), (624, BELT - 1.2, o(0.9))], chrome["light"], 1.1, 0.95)
    dl.line([(420, BELT + 0.1, o(1.0)), (624, BELT - 1.1, o(1.0))], chrome["shine"], 1.0, 0.95)
    # ---- the doors: their seams, the handles at their back edges
    for (xs_, xb) in SEAMS:
        dl.line([(xs_, SILL + 9, o(0.5)), (xb, BELT - 3, o(0.5))], paint["seam"], 1.0, 0.85)
        dl.line([(xs_ + 1.4, SILL + 10, o(0.5)), (xb + 1.4, BELT - 4, o(0.5))], "#9ca2b0", 0.8, 0.45)
    dl.line([(484, 31, o(0.5)), (486, 60, o(0.5)), (500, 82, o(0.5)), (540, 97, o(0.5))], paint["seam"], 1.0, 0.7)   # the front wing's join, over the wheel
    for hx in HANDLES:
        dl.line([(hx - 9, 88, o(1.2)), (hx, 88, o(1.2))], chrome["dark"], 2.6)
        dl.line([(hx - 9, 88.8, o(1.4)), (hx, 88.8, o(1.4))], chrome["light"], 1.2)
        dl.line([(hx - 3, 89.2, o(1.5)), (hx, 89.2, o(1.5))], chrome["shine"], 0.8)
    # ---- the sill: a chrome strip from arch to arch, holding the ground below and the sky on its top edge
    dl.poly([(R_AX + ARCH + 2, SILL + 2.5, o(0.8)), (F_AX - ARCH - 2, SILL + 2.5, o(0.8)), (F_AX - ARCH - 2, SILL + 8.5, o(0.8)), (R_AX + ARCH + 2, SILL + 8.5, o(0.8))], chrome["ground"])
    dl.line([(R_AX + ARCH + 2, SILL + 8.4, o(0.9)), (F_AX - ARCH - 2, SILL + 8.4, o(0.9))], chrome["sky"], 1.0, 0.95)
    dl.line([(R_AX + ARCH + 2, SILL + 5.5, o(0.9)), (F_AX - ARCH - 2, SILL + 5.5, o(0.9))], chrome["dark"], 0.9, 0.9)
    # ---- the arches: a chrome lip round each
    for ax in (R_AX, F_AX):
        dl.line(d.arc(ax, WR + 1.0, ARCH + 0.6, -18, 198, 22), chrome["mid"], 1.4, 0.9, z=o(0))
        dl.line(d.arc(ax, WR + 1.0, ARCH + 0.8, 15, 75, 8), chrome["shine"], 0.9, 0.9, z=o(0))
    # ---- the bumpers: chrome, the sky along their tops, the ground below a hard line
    for (b0, b1) in ((-1.0, 24.0), (604.0, 630.0)):
        dl.poly([(b0, 30, o(1.5)), (b1, 30, o(1.5)), (b1, 52, o(1.5)), (b0, 52, o(1.5))], chrome["ground"])
        dl.poly([(b0, 41, o(1.6)), (b1, 41, o(1.6)), (b1, 52, o(1.6)), (b0, 52, o(1.6))], chrome["sky"])
        dl.line([(b0, 41, o(1.7)), (b1, 41, o(1.7))], chrome["dark"], 1.1)
        dl.line([(b0, 51.6, o(1.7)), (b1, 51.6, o(1.7))], chrome["shine"], 0.9)
    dl.line([(606, 46, o(1.8)), (630, 46, o(1.8))], chrome["shine"], 1.6, 0.95)                    # the front one blazes
    dl.poly([(624, 31, o(1.8)), (630, 31, o(1.8)), (630, 52, o(1.8)), (624, 52, o(1.8))], "#ffffff", 0.7)
    # ---- the lamps: the tail lamp round the back corner, the head lamp round the front one (on: the suits would have it so)
    dl.poly([(0, 58, o(1.0)), (5.5, 58, o(1.0)), (7, 88, o(1.0)), (2.5, 88, o(1.0))], "#b8302a")
    dl.poly([(1.4, 62, o(1.1)), (4.2, 62, o(1.1)), (5.0, 84, o(1.1)), (2.4, 84, o(1.1))], "#e85a40")
    dl.poly([(12, 64, o(1.0)), (22, 64, o(1.0)), (22, 68, o(1.0)), (12, 68, o(1.0))], "#c83a2c")       # the side marker
    dl.poly([(622, 64, o(1.0)), (629.5, 64, o(1.0)), (629.5, 79, o(1.0)), (624, 79, o(1.0))], "#f8f6e8")
    dl.poly([(625, 66, o(1.1)), (629.5, 66, o(1.1)), (629.5, 77, o(1.1)), (626.5, 77, o(1.1))], "#ffffff")
    dl.poly([(608, 64, o(1.0)), (617, 64, o(1.0)), (617, 68, o(1.0)), (608, 68, o(1.0))], "#f0a030")   # and its marker
    # ---- a little aerial on the rear wing (the near side's), and the mirror on the front door
    if not far:
        dl.line([(70, 99, o(0.5)), (64, 142, 30)], "#2a2c34", 1.1)
    dl.line([(486, 106, o(1.0)), (481, 110, o(9.0))], paint["dark"], 2.4)
    c = dl.pt(477, 113, o(13))
    k = d.k
    dl.s.ellipse(c[0], c[1], 7.5 * k, 5.4 * k, paint["side"])
    dl.s.ellipse(c[0] + 1.0 * k, c[1] - 0.9 * k, 5.2 * k, 3.4 * k, paint["sky2"])
    dl.s.ellipse(c[0] + 2.2 * k, c[1] - 1.6 * k, 2.2 * k, 1.3 * k, "#ffffff")
    if far:
        return
    # ---- the plate, on the rear bumper: O.O.P.S. (the Office Of Peculiar Sectors; every letter pronounced)
    plate = [(-0.5, 32.5, -2.0), (25.0, 32.5, -2.0), (25.0, 49.5, -2.0), (-0.5, 49.5, -2.0)]
    dl.poly(plate, "#2a3a5c")
    dl.poly([(0.6, 33.6, -2.1), (23.9, 33.6, -2.1), (23.9, 48.4, -2.1), (0.6, 48.4, -2.1)], "#f4f1e6")
    dl.line([(0.6, 47.6, -2.2), (23.9, 47.6, -2.2)], "#2a3a5c", 1.0, 0.9)
    say_plate(notes, dl)


def say_plate(notes, d):
    """O.O.P.S. on the plate, in the plain face (a modern plate), as tall as the plate allows and narrowed to fit it."""
    if notes is None or d.shade:
        return
    import letter
    px, py = d.pt(12.25, 41.2, -2.3)
    a, b = d.pt(1.6, 41.2, -2.3), d.pt(22.9, 41.2, -2.3)
    size = 10.5 * d.kat(12, 41, -2.3)
    natural = letter.face(size * 3, False).getlength("O.O.P.S.") / 3
    notes.append(dict(words="O.O.P.S.", at=(px, py), size=size, color="#1e2e52", hand=False, anchor="mm",
                      slant=0.0, rough=0.0, amount=1.0, seed=0, spacing=0, squash=min(1.0, (b[0] - a[0]) / natural)))


# ------------------------------------------------------------------------------------------ the wheels (they turn; they do not ride)
def draw_wheels(d, dl, turn=0.0, far=False):
    """The two wheels of a side, and the dark of the wheel wells round them. `turn`: how far round the covers are, degrees.
    `far`: the left side's (z = WID), for the nose-on frames."""
    zs, out = (WID, 1.0) if far else (0.0, -1.0)
    o = lambda k: zs + out * k if k else zs
    for ax in (R_AX, F_AX):
        d.poly(d.arc(ax, WR + 1.0, ARCH + 1.0, -22, 202, 22), "#16141c", z=o(0))                         # the well
        d.disc(ax, WR, WR, RUBBER["mid"], z=o(1.0))
        d.poly(d.arc(ax, WR, WR, 200, 340, 10) + [(ax, WR)], RUBBER["dark"], z=o(1.05))                 # the tire turns under, into its shadow
        d.poly(d.arc(ax, WR, WR, -40, 70, 10) + list(reversed(d.arc(ax, WR, WR - 4.5, -40, 70, 10))), RUBBER["lit"], z=o(1.1))   # the sun along its edge
        d.disc(ax, WR, 23.5, CHROME["mid"], z=o(1.2))                                                     # the wheel cover
        d.disc(ax + 0.8, WR + 0.8, 21.5, CHROME["light"], z=o(1.25))
        d.disc(ax, WR, 15.5, CHROME["sky"], z=o(1.3))
        for kk in range(10):                                                                              # its slots, which turn
            a = math.radians(turn + kk * 36.0)
            ca, sa = math.cos(a), math.sin(a)
            r0, r1, w = 9.5, 20.5, 2.2
            dl.poly([(ax + ca * r0 - sa * w * 0.6, WR + sa * r0 + ca * w * 0.6, o(1.4)), (ax + ca * r1 - sa * w, WR + sa * r1 + ca * w, o(1.4)),
                     (ax + ca * r1 + sa * w, WR + sa * r1 - ca * w, o(1.4)), (ax + ca * r0 + sa * w * 0.6, WR + sa * r0 - ca * w * 0.6, o(1.4))], "#3a3e4a", 0.95)
        dl.poly(d.arc(ax, WR, 7.0, 0, 360, 14), CHROME["mid"], z=o(1.5))                                  # the middle: a plain cap, no badge
        dl.poly(d.arc(ax + 1.0, WR + 1.2, 4.0, 0, 360, 12), CHROME["shine"], z=o(1.6))
        dl.line(d.arc(ax, WR, 22.6, 10, 80, 8), CHROME["shine"], 1.3, 0.95, z=o(0))                      # the sun on the cover's rim
        dl.line(d.arc(ax, WR, 22.6, 190, 250, 6), CHROME["dark"], 1.0, 0.8, z=o(0))
        a = math.radians(turn + 18.0)                                                                     # the valve, so the turn shows
        dl.ball(ax + math.cos(a) * 24.6, WR + math.sin(a) * 24.6, o(1.6), 1.1, "#c8ccd4")


# ------------------------------------------------------------------------------------------ its shadow (it lies on the ground)
def hull(d, dl, notes=None):
    """The car as a simple solid, for its shadow: both sides, the floor, the roof, and the four wheels."""
    side = profile(d)
    for z in (0.0, WID):
        d.poly([(x, y, z) for x, y in side], "#000000")
    d.poly([(8, SILL, 6), (622, SILL, 6), (622, SILL, WID - 6), (8, SILL, WID - 6)], "#000000")
    d.side([(12, 95.5), (101, 99.5), (145, 137.5), (162, 140), (458, 140), (489, 133), (551, 101), (623.5, 89.5)], 0, WID, "#000000")
    for ax in (R_AX, F_AX):
        for z in (4.0, WID - 4.0):
            d.disc(ax, WR, WR, "#000000", z=z)
    return d


def shadow_layer(shape, ground):
    """The shadow on the ground: the long cool shadow out to the left, and the dark right under the car. -> (color, hard alpha)."""
    sh = Paper(shape)
    hull(Shade(sh, AT, 0.0, cam=MAG), None)
    cast = sh.done()[1]
    x, y = grid(shape)
    under, contact = Paper(shape), Paper(shape)
    u, t = Solid(under, AT, 0.0, cam=MAG), Solid(contact, AT, 0.0, cam=MAG)
    for z0, al in ((1.0, 0.45), (12.0, 0.75), (30.0, 1.0)):                                           # the ground under the car: darker further under
        u.poly([(14, 0, z0), (616, 0, z0), (616, 0, 140), (14, 0, 140)], "#000000", al)
    for ax in (R_AX, F_AX):                                                                            # and where the tires stand on it
        t.poly([(ax - 26, 0, 0.5), (ax + 26, 0, 0.5), (ax + 30, 0, 30), (ax - 30, 0, 30)], "#000000")
    deep, touch = under.done()[1], contact.done()[1]
    tone_ = np.empty(shape + (3,), dtype=F32)
    tone_[...] = rgb(ground)
    tone_ *= (1 + (noise(shape, (60, 14), 71, 3) - 0.5)[..., None] * 0.08)
    over(tone_, "#3c3242", np.clip(deep, 0, 1) * 0.85)
    over(tone_, "#2a2230", np.clip(touch, 0, 1) * 0.9)
    alpha = np.maximum(np.maximum(cast, deep), touch)
    # the far end of the long shadow is stippled, as the wagon's is: a hard cut-out edge, scaled down smoothly, reads soft
    from highway_wagon import stipple
    edge = np.clip(1 - blur((cast > 0.5).astype(F32), 2.0), 0, 1) * (cast > 0.5)
    dens = np.where(edge > 0.25, 0.55 + 0.4 * noise(shape, 6, 72, 2), 1.0)
    hard = (alpha > 0.5) & ((stipple(np.clip(dens, 0, 1), x, y) > 0.5) | (deep > 0.3) | (touch > 0.5))
    return np.clip(tone_, 0, 1), hard.astype(F32)


# ------------------------------------------------------------------------------------------ putting it together
def layers(seed=4, fast=False, ground="#88747c"):
    """The cut-out as the layers it is made of, back to front: (name, color, hard alpha, which frames, rides)."""
    shape = SHEET
    out = []
    sc, sa = shadow_layer(shape, ground)
    out.append(("shadow", sc, sa, (0, 1), False))
    for f, turn in ((0, 0.0), (1, TURN)):
        base, lines = Paper(shape), Paper(shape)
        draw_wheels(Solid(base, AT, 0.0, cam=MAG), Solid(lines, AT, 0.0, cam=MAG), turn)
        c, a = base.done()
        lc, la = lines.done()
        pc, pa = brushed(c, a, lc, la, "#2a2830", seed=seed + 1, sizes=(4, 2), keep=0.55, fast=fast)    # the same strokes in both: only the slots differ
        out.append((f"wheels{f}", pc, (pa > 0.5).astype(F32), (f,), False))
    base, lines = Paper(shape), Paper(shape)
    notes = []
    d, dl = Solid(base, AT, 0.0, cam=MAG), Solid(lines, AT, 0.0, cam=MAG)
    side = draw_body(d, dl, notes)
    c, a = base.done()
    bc, ba = side_bands(shape, d, side)
    over(c, bc, ba)
    draw_side_things(d, dl, notes)
    lc, la = lines.done()
    P.letter_on(lc, la, notes)
    pc, pa = brushed(c, a, lc, la, "#6c6e78", seed=seed, sizes=(6, 3, 2), keep=0.42, fast=fast)
    out.append(("body", pc, (pa > 0.5).astype(F32), (0, 1), True))
    return out


def compose(parts, frame, sheet=SHEET):
    pic = np.zeros(sheet + (3,), dtype=F32)
    alpha = np.zeros(sheet, dtype=F32)
    for name, c, a, fr, rides in parts:
        if frame not in fr:
            continue
        if rides and frame:
            c, a = np.roll(c, DROP, axis=0), np.roll(a, DROP, axis=0)
        over(pic, c, a)
        alpha = np.maximum(alpha, a)
    return pic, alpha


def box_of(alphas):
    both = np.max(alphas, axis=0)
    ys, xs = np.where(both > 0.5)
    return int(xs.min()) - 1, int(xs.max()) + 2, int(ys.min()) - 1, int(ys.max()) + 2


def write(names, parts, colors=96, seed=7, speckle=0.012, amount=0.016, sheet=SHEET, foot=FOOT):
    """Write the two frames as palette PNGs. Each layer gets its grain and its palette colours once, and the frames are
    put together from those, so the body is the very same pixels in both, a pixel apart. -> (foot, (w, h), sizes, box)"""
    grained = [(n, grain(c, seed + i, amount), a, fr, rides) for i, (n, c, a, fr, rides) in enumerate(parts)]
    pal = palette_of([g[a > 0.5].reshape(-1, 1, 3) for n, g, a, fr, rides in grained], colors=colors)
    index = [(n, to_palette(g, pal, seed=5 + i, speckle=speckle), a, fr, rides) for i, (n, g, a, fr, rides) in enumerate(grained)]
    made = []
    for f in (0, 1):
        idx = np.zeros(sheet, dtype=np.uint8)
        alpha = np.zeros(sheet, dtype=F32)
        for n, ix, a, fr, rides in index:
            if f not in fr:
                continue
            if rides and f:
                ix, a = np.roll(ix, DROP, axis=0), np.roll(a, DROP, axis=0)
            idx = np.where(a > 0.5, ix, idx)
            alpha = np.maximum(alpha, a)
        made.append((idx, alpha))
    x0, x1, y0, y1 = box_of([m[1] for m in made])
    sizes = []
    for (idx, alpha), name in zip(made, names):
        save(name, np.ascontiguousarray(idx[y0:y1, x0:x1]), pal, alpha[y0:y1, x0:x1])
        sizes.append(os.path.getsize(name))
    return (foot[0] - x0, foot[1] - y0), (x1 - x0, y1 - y0), sizes, (x0, x1, y0, y1)


def length_px(parts):
    """How long the car is at full size, bumper to bumper, in pixels (the body layer's extent)."""
    body = [a for n, c, a, fr, rides in parts if n == "body"][0]
    xs = np.where(body.max(axis=0) > 0.5)[0]
    ys = np.where(body.max(axis=1) > 0.5)[0]
    return int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)


# ------------------------------------------------------------------------------------------ nose on: coming down the far road
# limo-front-0.png and limo-front-1.png: the same car coming down the far road toward us, before it turns in, its head
# lamps on (the suits would have them on in the morning). The road comes toward us a little to the right (it runs away
# to a point at x 150 on the horizon), and the car keeps to the lane toward us, the road's far half, which is in the
# picture only from the horizon down to about row 351: there the car is drawn at under 0.2 of its full size. So it is
# painted as the roadside's camera sees it at FRONT_Z = 4000 cm in that lane (its front bumper's foot at about [15, 344]),
# at the size it would have with that foot on row 590: nearly square on, a sliver of its left side (in the sun) showing
# on the right. The foot is the ground under the middle of the front bumper.
ROAD_T = (150 - 400) / 800.0                                # as in nevada_roadside.py: the road's line, x per cm of depth
FRONT_Z = 4000.0
FRONT_X = -507.8 + ROAD_T * FRONT_Z - 0.75 * 765.0          # the middle of the lane toward us, there
HEADING = math.degrees(math.atan(-ROAD_T))                  # 17.4 degrees to the right of straight at us
SHEET_F = (300, 720)
FOOT_F = (430.0, 250.0)
MAGF = Camera(FOOT_F[1] - (K.FULL - K.HZ), FOOT_F[1], vanish_x=FOOT_F[0] - FRONT_X * (160.0 / 175.0),
              focal=800.0 * (K.CAM.Z0 + FRONT_Z) / K.CAM.Z0, size=(SHEET_F[1], SHEET_F[0]))
YAW_F = 90.0 - HEADING                                      # the nose (+x) toward us; the car's left side (+z) to the east
_cy, _sy = math.cos(math.radians(YAW_F)), math.sin(math.radians(YAW_F))
AT_F = (FRONT_X - (L * _cy + WID / 2 * _sy), L * _sy - WID / 2 * _cy)      # so that the front bumper's middle stands on the foot
NOSE = [(621, 25), (627.5, 31), (629, 50), (629, 66), (628, 81), (623.5, 89.5)]
SUNLIT = dict(PAINT, side="#aeacb0", sky="#d8dce6", sky2="#c8ccd8", land="#8c8a96", floor="#c6b6a8", under="#7e7a86", sill="#5c5a66",
              pillar="#9c9ea8", shoulder="#c2c0c2", seam="#5c5e6a", dark="#3c3d46")                       # the left side, in the sun
FACE = dict(face="#9a9ca6", corner="#c6c4c4", corner_shade="#6a6c76")
ON_ROAD = dict(CHROME, ground="#9c96a8")                               # its chrome holds the asphalt, not the lot


def draw_front_face(d, dl, chrome=None):
    """The car's face: its front panel rounding into both sides, the bumper, the grille (upright chrome bars, no badge
    and no name), four head lamps, on, and the amber parking lamps under the outer ones."""
    W = WID
    chrome = chrome or CHROME
    d.side(NOSE, 6, W - 6, FACE["face"])
    d.side(NOSE, W - 6, W, FACE["corner"])                                                           # rounding into the sunny side
    d.side(NOSE, 0, 6, FACE["corner_shade"])                                                         # and into the other
    X = 629.6
    d.poly([(X - 1, 25, 4), (X - 1, 25, W - 4), (X - 1, 30, W - 4), (X - 1, 30, 4)], "#2a2a32")     # under the bumper
    d.poly([(X, 30, 1), (X, 30, W - 1), (X, 52, W - 1), (X, 52, 1)], chrome["ground"])                # the bumper: the road below,
    d.poly([(X + 0.1, 41, 1), (X + 0.1, 41, W - 1), (X + 0.1, 52, W - 1), (X + 0.1, 52, 1)], chrome["sky"])   # the sky above
    dl.line([(X + 0.2, 41, 1), (X + 0.2, 41, W - 1)], chrome["dark"], 1.1)
    dl.line([(X + 0.2, 51.4, 1), (X + 0.2, 51.4, W - 1)], chrome["shine"], 1.1)
    dl.line([(X + 0.2, 46, W - 60), (X + 0.2, 46, W - 1)], chrome["shine"], 1.4, 0.9)                 # where the sun is on it
    gz0, gz1, gy0, gy1 = 66.0, 134.0, 55.0, 80.0                                                       # the grille
    d.poly([(X, gy0, gz0), (X, gy0, gz1), (X, gy1, gz1), (X, gy1, gz0)], chrome["mid"])
    d.poly([(X + 0.1, gy0 + 2, gz0 + 2.5), (X + 0.1, gy0 + 2, gz1 - 2.5), (X + 0.1, gy1 - 2, gz1 - 2.5), (X + 0.1, gy1 - 2, gz0 + 2.5)], "#1c1e26")
    for i in range(1, 12):
        zz = gz0 + 2.5 + (gz1 - gz0 - 5) * i / 12
        dl.line([(X + 0.3, gy0 + 2.2, zz), (X + 0.3, gy1 - 2.2, zz)], chrome["light"], 1.1, 0.95)
    dl.line([(X + 0.3, gy1 - 0.4, gz0), (X + 0.3, gy1 - 0.4, gz1)], chrome["shine"], 1.0)
    for z0 in (8.0, 34.0, 146.0, 172.0):                                                               # the head lamps, on
        z1 = z0 + 20.0
        d.poly([(X, 61, z0), (X, 61, z1), (X, 78, z1), (X, 78, z0)], chrome["mid"])
        dl.poly([(X + 0.2, 62.5, z0 + 2), (X + 0.2, 62.5, z1 - 2), (X + 0.2, 76.5, z1 - 2), (X + 0.2, 76.5, z0 + 2)], "#fff4c8")
        dl.poly([(X + 0.3, 65, z0 + 5), (X + 0.3, 65, z1 - 5), (X + 0.3, 74, z1 - 5), (X + 0.3, 74, z0 + 5)], "#ffffff")
    for z0 in (8.0, 172.0):                                                                            # the parking lamps
        dl.poly([(X + 0.2, 54, z0), (X + 0.2, 54, z0 + 20), (X + 0.2, 58.5, z0 + 20), (X + 0.2, 58.5, z0)], "#f2a43a")
    dl.line([(624, 88.6, 6), (624, 88.6, W - 6)], chrome["light"], 1.2, 0.9)                          # the hood's front edge


def draw_front_wheels(d, dl, turn=0.0):
    """Nose on: the left side's two wheels (in the sun) and, under the bumper, the treads of the two front tires."""
    draw_wheels(d, dl, turn, far=True)
    xt = F_AX + WR                                                                                     # the front of each front tire
    for z0, z1 in ((6.0, 30.0), (WID - 30.0, WID - 6.0)):
        d.poly([(xt, 0, z0), (xt, 0, z1), (xt, 27, z1), (xt, 27, z0)], RUBBER["mid"])
        for i in range(7):                                                                             # the tread, which moves as it turns
            yy = 2.0 + ((i * 4.0 + turn * 0.25) % 26.0)
            dl.line([(xt + 0.3, yy, z0 + 1.5), (xt + 0.3, yy, z1 - 1.5)], RUBBER["dark"], 1.2, 0.9)


def shadow_front(shape, ground):
    """Nose on: the long shadow out to the left (the car's right), and the dark under its front. -> (color, hard alpha)."""
    sh = Paper(shape)
    hull(Shade(sh, AT_F, YAW_F, cam=MAGF), None)
    cast = sh.done()[1]
    x, y = grid(shape)
    under, contact = Paper(shape), Paper(shape)
    u, t = Solid(under, AT_F, YAW_F, cam=MAGF), Solid(contact, AT_F, YAW_F, cam=MAGF)
    for x1, al in ((L - 2.0, 0.45), (L - 14.0, 0.75), (L - 34.0, 1.0)):                               # under its front: darker further under
        u.poly([(R_AX, 0, 6), (x1, 0, 6), (x1, 0, WID - 6), (R_AX, 0, WID - 6)], "#000000", al)
    for ax in (R_AX, F_AX):
        for z0, z1 in ((4.0, 34.0), (WID - 34.0, WID - 4.0)):
            t.poly([(ax - 26, 0, z0), (ax + 26, 0, z0), (ax + 26, 0, z1), (ax - 26, 0, z1)], "#000000")
    deep, touch = under.done()[1], contact.done()[1]
    tone_ = np.empty(shape + (3,), dtype=F32)
    tone_[...] = rgb(ground)
    tone_ *= (1 + (noise(shape, (60, 14), 73, 3) - 0.5)[..., None] * 0.08)
    over(tone_, "#3c3242", np.clip(deep, 0, 1) * 0.85)
    over(tone_, "#2a2230", np.clip(touch, 0, 1) * 0.9)
    alpha = np.maximum(np.maximum(cast, deep), touch)
    from highway_wagon import stipple
    edge = np.clip(1 - blur((cast > 0.5).astype(F32), 2.0), 0, 1) * (cast > 0.5)
    dens = np.where(edge > 0.25, 0.55 + 0.4 * noise(shape, 6, 74, 2), 1.0)
    hard = (alpha > 0.5) & ((stipple(np.clip(dens, 0, 1), x, y) > 0.5) | (deep > 0.3) | (touch > 0.5))
    return np.clip(tone_, 0, 1), hard.astype(F32)


def layers_front(seed=4, fast=False, ground="#6e6a94"):
    """The nose-on cut-out as its layers, back to front: (name, color, hard alpha, which frames, rides). (The road it is
    on is the asphalt's gray, so its shadow is the road's in shade.)"""
    shape = SHEET_F
    out = []
    sc, sa = shadow_front(shape, ground)
    out.append(("shadow", sc, sa, (0, 1), False))
    for f, turn in ((0, 0.0), (1, TURN)):
        base, lines = Paper(shape), Paper(shape)
        draw_front_wheels(Solid(base, AT_F, YAW_F, cam=MAGF), Solid(lines, AT_F, YAW_F, cam=MAGF), turn)
        c, a = base.done()
        lc, la = lines.done()
        pc, pa = brushed(c, a, lc, la, "#2a2830", seed=seed + 1, sizes=(4, 2), keep=0.55, fast=fast)
        out.append((f"wheels{f}", pc, (pa > 0.5).astype(F32), (f,), False))
    base, lines = Paper(shape), Paper(shape)
    d, dl = Solid(base, AT_F, YAW_F, cam=MAGF), Solid(lines, AT_F, YAW_F, cam=MAGF)
    draw_tops(d, dl, far=True, paint=dict(PAINT, shoulder=SUNLIT["shoulder"]))
    side = profile(d)
    d.poly([(x, y, WID) for x, y in side], SUNLIT["side"])
    c, a = base.done()
    bc, ba = side_bands(shape, d, side, far=True, paint=SUNLIT)
    over(c, bc, ba)
    base = Paper(shape)                                                                                # the face, over the side's near end
    d2 = Solid(base, AT_F, YAW_F, cam=MAGF)
    draw_side_things(d, dl, None, far=True, paint=SUNLIT, chrome=ON_ROAD)
    draw_front_face(d2, dl, chrome=ON_ROAD)
    fc, fa = base.done()
    over(c, fc, fa)
    a = np.maximum(a, fa)
    lc, la = lines.done()
    pc, pa = brushed(c, a, lc, la, "#7c7e88", seed=seed + 2, sizes=(5, 3, 2), keep=0.45, fast=fast)
    out.append(("body", pc, (pa > 0.5).astype(F32), (0, 1), True))
    return out


def front_lane():
    """The middle of the lane toward us, as picture points from the horizon to where it leaves the picture's left edge:
    where the scene can drive the nose-on frames (their foot), with the scale for each."""
    pts = []
    for z in (60000, 30000, 16000, 9000, 6000, 4000, 3435):
        x = -507.8 + ROAD_T * z - 0.75 * 765.0
        px, py = K.CAM.pt(x, 0, z)
        pts.append([round(px, 1), round(py, 1), round(row_scale(py), 3)])
    return pts


def measure_front(parts):
    box = box_of([compose(parts, 0, SHEET_F)[1], compose(parts, 1, SHEET_F)[1]])
    px, py = K.CAM.pt(FRONT_X, 0, FRONT_Z)
    return {"box": box, "at": [round(px, 1), round(py, 1)], "scale": round(row_scale(py), 3)}


def measure(parts):
    """The numbers layout.json gives: the frames' common crop on the sheet, the length bumper to bumper (px, full size),
    and the columns the body runs between when it stands at its stop."""
    box = box_of([compose(parts, 0)[1], compose(parts, 1)[1]])
    body = [a for n, c, a, fr, rides in parts if n == "body"][0]
    xs = np.where(body.max(axis=0) > 0.5)[0]
    s = row_scale(STOP[1])
    return {"box": box, "length": int(xs.max() - xs.min() + 1),
            "stop_x": [int(round(STOP[0] + (xs.min() - FOOT[0]) * s)), int(round(STOP[0] + (xs.max() + 1 - FOOT[0]) * s))]}


def lay(picture, color, alpha, foot, at, scale):
    """Lay a cropped sprite on a picture with its foot at `at`, at `scale` (smoothly): only for looking."""
    from PIL import Image
    h, w = alpha.shape
    nw, nh = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
    rgba = np.dstack([color * alpha[..., None], alpha])
    small = np.dstack([np.asarray(Image.fromarray(rgba[..., i].astype(F32), "F").resize((nw, nh), Image.LANCZOS), dtype=F32) for i in range(4)])
    x0, y0 = int(round(at[0] - foot[0] * scale)), int(round(at[1] - foot[1] * scale))
    X0, Y0, X1, Y1 = max(x0, 0), max(y0, 0), min(x0 + nw, picture.shape[1]), min(y0 + nh, picture.shape[0])
    if X1 <= X0 or Y1 <= Y0:
        return picture
    part = small[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    a = np.clip(part[..., 3:4], 0, 1)
    picture[Y0:Y1, X0:X1] = picture[Y0:Y1, X0:X1] * (1 - a) + np.clip(part[..., :3], 0, 1)
    return picture


def row_scale(row):
    """How big the cut-out is drawn with its foot on a picture row: 1 on row 590, 0.8 on row 530."""
    return (row - K.HZ) / float(K.FULL - K.HZ)


if __name__ == "__main__":
    import sys, time
    from PIL import Image
    t0 = time.time()
    parts = layers(fast="fast" in sys.argv)
    print("painted", round(time.time() - t0, 1), "length, height", length_px(parts))
    f0, f1 = compose(parts, 0), compose(parts, 1)
    x0, x1, y0, y1 = box_of([f0[1], f1[1]])
    bg = np.empty((y1 - y0 + 20, (x1 - x0) * 2 + 60, 3), dtype=F32)
    bg[...] = rgb("#d2a072")
    for i, (c, a) in enumerate((f0, f1)):
        view = bg[10:10 + y1 - y0, 20 + i * (x1 - x0 + 20):20 + i * (x1 - x0 + 20) + x1 - x0]
        over(view, c[y0:y1, x0:x1], a[y0:y1, x0:x1])
    Image.fromarray((np.clip(bg, 0, 1) * 255).astype(np.uint8)).save("out/nevada-roadside-limo-try.png")
    back = np.asarray(Image.open("out/nevada-roadside-comp.png").convert("RGB"), dtype=F32) / 255
    c, a = f0
    lay(back, c[y0:y1, x0:x1], a[y0:y1, x0:x1], (FOOT[0] - x0, FOOT[1] - y0), STOP, row_scale(STOP[1]))
    Image.fromarray((np.clip(back, 0, 1) * 255).astype(np.uint8)).save("out/nevada-roadside-limo-stop.png")
    print("done", round(time.time() - t0, 1), "box", (x0, x1, y0, y1), "foot in box", (FOOT[0] - x0, FOOT[1] - y0))

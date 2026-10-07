"""The water carrier's donkey: small, grey, patient. It stands square on the bank facing the river
(to the left), a big water jar slung on each side of it in a rope net, a third jar set down in the sand.

Measurements are in centimetres: x along the donkey from under its middle (its head is at minus x),
y up from the ground. The far legs, the far ear and the far jar are the near ones moved a little up the
picture and darkened. Light comes from the upper left, as everywhere in this scene."""

import math

import numpy as np

from brush import *
from solid import mix

GREY = dict(light="#d0c8b8", mid="#a49c90", shade="#78737e", dark="#514c5a")        # the coat: sunlit, plain, in shade, deep shade
PALE = dict(light="#f7f0e0", mid="#dcd2c2", shade="#aea6ae")                         # muzzle, belly, round the eye
INK = dict(mane="#3a3238", hoof="#2c282e", eye="#17131a")
CLAY = dict(shine="#f8cd9a", light="#de9860", mid="#bd6c3e", shade="#8a4630", dark="#57291f")
ROPE = dict(light="#f0d69a", mid="#c9a25a", dark="#7c5a2e")
MAT = dict(light="#e8cc8a", mid="#c6a05c", shade="#8e6c3c")
WOOD = dict(light="#b88a56", mid="#7c5432", dark="#4a2e1c")
FAR = (-6.0, 4.6)                                           # how the far side of the animal sits against the near side
LEGS = 0.86                                                 # the legs are drawn full length below and shortened by this much

# the outline of body, neck and head, clockwise from the withers
BODY = [(-22, 100.5), (-36, 106.5), (-49, 113.5), (-57, 113.5), (-64, 109), (-73, 99.5), (-82, 90), (-88, 84), (-89.5, 79.5), (-87, 75.5),
        (-81, 74.5), (-73, 78), (-65.5, 81.5), (-58, 85.5), (-54, 88.5), (-47, 81), (-42, 71), (-38.5, 60), (-28, 50), (-8, 45.5), (14, 47),
        (28, 53.5), (38, 58.5), (49, 69), (52.5, 82), (49.5, 92.5), (39, 99.5), (22, 98), (2, 96.5), (-12, 98)]
FORE = [(-39, 62), (-36.4, 46), (-35.3, 38), (-35.8, 33), (-34.2, 28), (-33.9, 13), (-34.9, 9.5), (-35.7, 5.5), (-36.4, 0), (-28.2, 0),
        (-28.2, 5.5), (-27.5, 9.5), (-27.9, 13), (-27.3, 28), (-26.0, 33), (-26.2, 38), (-24.4, 46), (-21, 62)]
HIND = [(26, 64), (32.2, 52), (37.2, 43), (39.6, 36.5), (38.4, 28), (38.6, 13), (37.6, 9.5), (36.8, 5.5), (36.2, 0), (44.4, 0), (44.4, 5.5),
        (44.7, 9.5), (44.2, 13), (45.6, 28), (48.6, 34.5), (50.8, 40.5), (48.8, 47.5), (49.8, 58), (51.6, 70), (42, 76)]
# a jar, in its own measurements: 30 across, 46 tall, standing on (7, 62)
JAR = [(7, 62), (-3, 65.5), (-8, 77), (-7.6, 90), (-2.5, 98.5), (2.2, 101.2), (2.6, 104.5), (0.6, 107.6), (13.4, 107.6), (11.4, 104.5),
       (11.8, 101.2), (16.5, 98.5), (21.6, 90), (22, 77), (17, 65.5)]


def _loop(points, steps=5):
    """A closed smooth outline through the points."""
    pts = [tuple(p) for p in points]
    return curve(pts[-1:] + pts + pts[:2], steps)[steps:steps + len(pts) * steps]


def jar(base, lines, at, s, tone=1.0, net=False, neck_rope=False):
    """A big water jar of red Nile clay: egg-shaped, a short neck, a rolled rim. `at` turns the jar's own
    measurements (see JAR) into places in the picture. `tone` under 1 puts it in shade (the far one)."""
    def c(name):
        return mix(CLAY["dark"], CLAY[name], tone) if tone < 1 else CLAY[name]

    def pts(points):
        return [at(p[0], p[1]) for p in points]

    w = lambda v: max(v * s, 0.85)
    base.poly(_loop(pts(JAR), 5), c("mid"))
    base.poly(_loop(pts([(-7.4, 79), (-6.6, 90), (-2.2, 98), (2, 99.6), (3.6, 90), (1.6, 78), (-1, 68), (-5.6, 70)]), 5), c("light"))           # the side to the sun
    base.poly(_loop(pts([(9, 62.6), (17, 65.5), (22, 77), (21.6, 90), (16.5, 98.5), (13, 99.6), (15.6, 90), (15.6, 78), (12, 68)]), 5), c("shade"))    # the side away from it
    base.poly(_loop(pts([(1, 64.6), (7, 62.2), (15, 65), (11, 67.6), (5, 67.6)]), 4), c("dark"))                                               # its round foot, in its own shade
    base.poly(pts([(0.6, 107.6), (13.4, 107.6), (12.2, 109.8), (1.8, 109.8)]), c("dark"))                                                      # the dark of its mouth
    lines.line(pts([(0.8, 107.4), (13.2, 107.4)]), c("light"), w(1.9))                                                                         # the rim
    lines.line(pts([(0.8, 108.0), (7, 108.2)]), c("shine"), w(0.9), 0.9)
    lines.line(pts([(-4.8, 89), (-4.2, 80)]), c("shine"), w(1.7), 0.95 if tone >= 1 else 0.35)                                                 # the sun on its shoulder
    lines.line(pts([(21.8, 77), (21.4, 90), (16.5, 98.5)]), c("dark"), w(1.0), 0.7)                                                            # the shadow-side edge
    if net or neck_rope:
        lines.line(pts([(2.0, 102.6), (12.0, 102.6)]), ROPE["dark"], w(2.4))
        lines.line(pts([(2.0, 103.0), (12.0, 103.0)]), ROPE["light"], w(1.4))
    if net:                                                  # three ropes down it and a girdle round it
        for run in ([(2.6, 101.6), (-5.6, 90), (-6.6, 78), (0, 65.6)], [(7, 101.6), (7.4, 84), (7, 63)], [(11.4, 101.6), (19.4, 90), (20.2, 78), (14, 65.6)]):
            lines.line(pts(curve(run, 5)), ROPE["dark"], w(1.6), 0.9)
            lines.line(pts(curve(run, 5)), ROPE["light"], w(0.9))
        girdle = curve([(-7.8, 82), (0, 79.4), (7, 78.6), (14, 79.4), (21.8, 82)], 5)
        lines.line(pts(girdle), ROPE["dark"], w(1.6), 0.9)
        lines.line(pts(girdle), ROPE["light"], w(0.9))


def donkey(shape, foot, scale, jar_at=(77.0, -30.0)):
    """-> (color, alpha, line color, line alpha) on clear sheets the size of the picture. `foot` is where
    the ground under its middle is, on the line of its near hooves; `scale` is pixels to a centimetre.
    `jar_at` is where the third jar stands: centimetres along, and toward us (minus) across the ground."""
    base, lines = Sheet(shape), Sheet(shape)
    fx, fy = foot
    s = scale

    def P(x, y, far=False):
        dx, dy = (FAR if far else (0.0, 0.0))
        y = y * LEGS if y <= 50 else y - 50 * (1 - LEGS)     # a small donkey: short in the leg
        return (fx + (x + dx) * s, fy - (y + dy) * s)

    def pts(points, far=False):
        return [P(p[0], p[1], far) for p in points]

    def blob(points, color, far=False, steps=5, sheet=None):
        (sheet or base).poly(_loop(pts(points, far), steps), color)

    def stroke(points, color, width, alpha=1.0, far=False, sheet=None):
        (sheet or lines).line(pts(points, far), color, max(width * s, 0.85), alpha)

    def rope(points, width=1.8):
        stroke(points, ROPE["dark"], width)
        stroke(points, ROPE["light"], width * 0.56)

    # ---- the tail hangs behind: a thin dock and a dark tuft
    base.taper(pts(curve([(49.5, 92), (54.5, 82), (56.6, 68), (56.0, 56)], 6)), GREY["shade"], 3.6 * s, 2.6 * s)
    blob([(54.2, 60), (53.0, 49), (55.0, 39), (58.4, 42), (58.8, 53), (57.8, 61)], INK["mane"])
    # ---- the far legs, in shade
    for leg in (FORE, HIND):
        base.poly(pts(leg, far=True), GREY["dark"])
        base.poly(pts([p for p in leg if p[1] <= 5.6], far=True), INK["hoof"])
    # ---- the far ear: we see into it
    blob([(-59, 112.5), (-63.5, 124), (-64.5, 137), (-62, 147), (-58, 138), (-55.5, 125), (-54.5, 113.5)], GREY["shade"])
    blob([(-59.4, 117), (-62.2, 126), (-62.6, 137), (-61.6, 142), (-59.6, 136), (-57.8, 126), (-56.8, 117)], PALE["shade"])
    # ---- the far jar shows over its back
    big = lambda x, y: (7 + (x - 7) * 1.12, 58 + (y - 62) * 1.12)                       # the slung jars are a little bigger than the plan
    jar(base, lines, lambda x, y: P(big(x, y)[0] + 13.0, big(x, y)[1] + 8.0), s, tone=0.5)
    # ---- the body, neck and head in one piece
    blob(BODY, GREY["mid"])
    # shade: the underside and the back of the rump, under the neck, under the jaw, behind the elbow
    blob([(-28, 50), (-8, 45.5), (14, 47), (28, 53.5), (38, 58.5), (49, 69), (52.5, 82), (49.5, 92.5), (46.4, 88), (44.6, 75), (38, 67),
          (27, 61.5), (10, 57), (-8, 56), (-23, 59)], GREY["shade"])
    blob([(-54, 88.5), (-47, 81), (-42, 71), (-40, 78), (-44.5, 87), (-51, 92.5)], GREY["shade"])
    blob([(-80, 75), (-73, 78), (-65.5, 81.5), (-58, 85.5), (-55, 88.4), (-60, 89.5), (-68, 85), (-76, 79.8)], GREY["shade"])
    blob([(-32, 55), (-27.6, 68), (-23.4, 58), (-26, 51)], GREY["shade"])
    # the belly is pale, even in its own shade
    blob([(-26, 51.6), (-8, 46.6), (14, 48), (27, 53.8), (33, 57), (22, 54.6), (8, 51.4), (-10, 50.6), (-22, 53.6)], PALE["shade"])
    # light along the top: the croup and back, the crest of the neck, the brow and nose, the breast
    blob([(49, 92), (39, 99.5), (22, 98), (2, 96.5), (-12, 98), (-22, 100.5), (-21.5, 95), (-11, 92.4), (3, 91), (22, 92.4), (37, 93.5), (46.5, 88)], GREY["light"])
    blob([(-23, 100), (-36, 106), (-49, 113), (-47.5, 106.6), (-35.5, 99.6), (-25, 94.5)], GREY["light"])
    blob([(-50, 113.5), (-57, 113.5), (-64, 109), (-73, 99.5), (-82, 90), (-79.4, 88.6), (-70.6, 96.4), (-62.6, 104), (-56, 108), (-50, 108.6)], GREY["light"])
    blob([(-42, 71), (-47, 81), (-52, 86.4), (-49, 79.6), (-45, 71.6), (-41.4, 63), (-38.5, 60)], GREY["light"])
    blob([(-66, 100), (-58, 99), (-54, 92), (-60, 87.6), (-68, 90), (-70, 95)], mix(GREY["mid"], GREY["light"], 0.5))       # the round of the cheek
    blob([(36, 96), (46, 86), (44, 74), (36, 68), (30, 78), (30, 92)], mix(GREY["mid"], GREY["light"], 0.4))                # and of the haunch
    # the muzzle is nearly white, and so is the ring round the eye
    blob([(-89.5, 79.5), (-88, 84), (-82.4, 90), (-76, 91.6), (-73.4, 84.6), (-75.2, 78.6), (-81, 74.5), (-87, 75.5)], PALE["light"])
    blob([(-89.2, 78.4), (-87, 75.5), (-81, 74.5), (-75.6, 77.8), (-79, 79.2), (-85, 79.6)], PALE["shade"])
    blob([(-70.4, 104.6), (-68, 108.4), (-63, 107.8), (-61.2, 103.6), (-63.6, 100.4), (-68.4, 101)], PALE["mid"])
    # ---- the near legs: a lit front, a shaded back, small dark hooves
    for leg, lit, dark in ((FORE, [(-39, 62), (-36.4, 46), (-35.3, 38), (-35.8, 33), (-34.2, 28), (-33.9, 13), (-34.9, 9.5), (-35.6, 5.6), (-33.2, 5.6), (-32.2, 13),
                                   (-32.4, 28), (-33.4, 37), (-33.2, 47), (-34, 62)],
                            [(-28.2, 5.6), (-27.5, 9.5), (-27.9, 13), (-27.3, 28), (-26.0, 33), (-26.2, 38), (-24.4, 46), (-22.4, 58), (-26.0, 50), (-28.0, 38),
                             (-28.8, 28), (-29.8, 13), (-30.2, 5.6)]),
                           (HIND, [(27, 63), (32.2, 52), (37.2, 43), (39.6, 36.5), (38.4, 28), (38.6, 13), (37.6, 9.5), (36.9, 5.6), (39.3, 5.6), (40.4, 13),
                                   (40.4, 28), (41.6, 36.6), (39.4, 45), (34.6, 55), (31, 64)],
                            [(44.4, 5.6), (44.7, 9.5), (44.2, 13), (45.6, 28), (48.6, 34.5), (50.8, 40.5), (48.8, 47.5), (49.8, 58), (50.8, 68), (47, 60),
                             (45.4, 47.5), (46.4, 40), (43.6, 28), (42.4, 13), (42.6, 5.6)])):
        base.poly(pts(leg), GREY["mid"])
        base.poly(pts(lit), GREY["light"])
        base.poly(pts(dark), GREY["shade"])
        base.poly(pts([p for p in leg if p[1] <= 5.6]), INK["hoof"])
    # ---- the mane: short, dark, upright, from the poll to the withers
    base.poly(pts([(-50.6, 113.4), (-49.8, 117.0), (-43, 114.0), (-36, 110.4), (-29, 106.6), (-23, 103.6), (-21.6, 100.4), (-29, 103.4), (-36, 106.5), (-43, 110)]), INK["mane"])
    # ---- the near ear, long, a little back: grey outside, dark at the tip
    blob([(-55.5, 113), (-57.5, 125), (-55, 138), (-48, 147.5), (-45.5, 138.5), (-46.5, 125), (-49.5, 114.5)], GREY["mid"])
    blob([(-55.2, 114), (-57.0, 125), (-54.6, 137), (-50.6, 143.4), (-52.6, 133), (-53.2, 123), (-52.6, 115)], GREY["light"])
    blob([(-51.4, 141.2), (-48, 147.5), (-46.2, 141), (-47.6, 136.4)], INK["mane"])

    # ================= crisp things, over the brushwork
    # the cross: a dark stripe down the spine and another down over the shoulder
    stroke([(-22.4, 100.6), (-24.6, 92), (-26.8, 83), (-27.8, 75)], INK["mane"], 2.8, 0.92)
    stroke([(-27.8, 75), (-27.8, 70)], INK["mane"], 1.6, 0.7)
    stroke([(-21, 100.4), (-12, 98.2), (2, 96.8), (22, 98.2), (39, 99.6), (49.4, 92.8)], INK["mane"], 1.6, 0.8)
    for i in range(11):                                      # the mane's bristles
        t = i / 10
        x0, y0 = lerp(-49.6, -23.4, t), lerp(116.4, 103.2, t)
        stroke([(x0, y0 - 1.0), (x0 + 1.5, y0 + 1.8)], INK["mane"], 1.6, 0.95)
    # the eye: half shut, heavy-lidded; the nostril; the long line of the mouth
    stroke([(-68.2, 104.0), (-65.6, 105.2), (-63.2, 104.2)], INK["eye"], 2.6)
    stroke([(-69.4, 106.2), (-65.6, 107.6), (-62.2, 105.8)], GREY["dark"], 1.4, 0.9)
    stroke([(-88.0, 82.6), (-86.4, 84.0)], INK["eye"], 2.4, 0.95)
    stroke([(-89.2, 78.6), (-85.6, 77.8), (-81.6, 79.0)], GREY["dark"], 1.2, 0.9)
    stroke([(-55.5, 113), (-57.5, 125), (-55, 138), (-48, 147.5)], GREY["dark"], 0.9, 0.5)
    stroke([(-48, 147.5), (-45.5, 138.5), (-46.5, 125), (-49.5, 114.5)], INK["mane"], 1.3, 0.85)      # the ear's shadow-side edge
    stroke([(-62, 147), (-58, 138), (-55.8, 127)], GREY["dark"], 1.0, 0.7)
    # the dark edge on the shadow side of the whole animal
    stroke([(49.5, 92.5), (52.5, 82), (49, 69), (38, 58.5)], GREY["dark"], 1.3, 0.85)
    stroke([(38, 58.5), (28, 53.5), (14, 47), (-8, 45.5), (-28, 50)], GREY["dark"], 1.3, 0.75)
    stroke([(-81, 74.5), (-73, 78), (-65.5, 81.5), (-58, 85.5), (-54, 88.5), (-47, 81), (-42, 71)], GREY["dark"], 1.1, 0.6)
    for leg in (FORE, HIND):                                 # hooves: a small light on the wall of each
        hx = min(p[0] for p in leg if p[1] <= 0.1)
        stroke([(hx + 1.6, 4.4), (hx + 1.2, 1.2)], "#6c6670", 1.3, 0.9)
        stroke([(hx + 0.4, 5.9), (hx + 7.6, 5.9)], GREY["dark"], 1.0, 0.7)
    for (lx, ly) in ((-35.2, 40), (-35.0, 44), (38.6, 38.4)):    # faint bars on the legs
        stroke([(lx, ly), (lx + 5.0, ly - 0.6)], GREY["dark"], 1.1, 0.6)
    stroke([(50.4, 91.6), (55.0, 82), (56.8, 68)], GREY["dark"], 0.9, 0.6)

    # ---- the rope halter, and its rope let fall to the ground: he is not going anywhere
    rope([(-81.4, 90.6), (-79.6, 84), (-79.4, 76.0)], 2.2)
    rope([(-80.2, 86.5), (-68, 93.5), (-59.5, 100.5), (-54.6, 111)], 1.9)
    rope(curve([(-79.4, 76.4), (-83.5, 60), (-84.0, 38), (-80.5, 15), (-74.5, 3.0), (-66, 0.8), (-57, 1.8)], 6), 2.0)

    # ---- the load: a mat over its back, a pole lashed along it, and a jar hung in a net on each side
    blob([(-17, 100.6), (-4, 98.4), (14, 98.8), (31, 101.4), (32.4, 91), (31.6, 81.4), (8, 79.6), (-17.6, 81.0), (-18.6, 91)], MAT["mid"], steps=4)
    blob([(-17, 100.6), (-4, 98.4), (14, 98.8), (31, 101.4), (31.4, 96.4), (14, 93.6), (-4, 93.2), (-17.4, 95.4)], MAT["light"], steps=4)
    blob([(-18.2, 85.4), (8, 83.8), (32, 85.8), (31.6, 81.4), (8, 79.6), (-17.6, 81.0)], MAT["shade"], steps=4)
    for xx in range(-15, 31, 4):                             # its fringe
        stroke([(xx, 81.2), (xx - 0.6, 77.6)], MAT["mid"], 1.2, 0.9)
    stroke([(-18, 91.4), (-4, 89.6), (14, 89.8), (32, 92.2)], MAT["shade"], 0.9, 0.6)
    base.line(pts([(-15.5, 103.2), (30.0, 104.0)]), WOOD["dark"], 3.6 * s)
    stroke([(-15.5, 103.2), (30.0, 104.0)], WOOD["mid"], 2.8)
    stroke([(-15.5, 104.0), (30.0, 104.8)], WOOD["light"], 1.0, 0.9)
    for bx in (-11.0, 25.5):                                 # lashed to the mat's girth at each end
        rope([(bx, 105.6), (bx + 0.6, 100.2)], 2.6)
    rope([(-13, 81), (-12.6, 62), (-11, 49.6)], 1.9)                                                                     # the girth
    rope([(-16, 92), (-30, 84), (-41.4, 73.4)], 1.8)                                                                     # round the breast
    rope([(30, 92), (42, 86), (51.6, 78.4)], 1.8)                                                                        # and round the rump
    near = lambda x, y: P(*big(x, y))
    jar(base, lines, near, s, tone=1.0, net=True)
    rope([big(2.6, 103.0), (-3.6, 103.6)], 1.3)                                                                          # hung from the pole
    rope([big(11.4, 103.0), (18.6, 104.0)], 1.3)

    # ---- the third jar, set down in the sand beside it
    jx, jz = jar_at
    lean = math.radians(-8)
    ca, sa = math.cos(lean), math.sin(lean)

    def G(x, y):                                             # (it leans a little, and stands on the ground nearer us)
        x, y = (x - 7) * 1.08, (y - 62) * 1.08
        return (fx + (jx + x * ca - y * sa) * s, fy - (y * ca + x * sa - 1.5) * s - jz * s * 0.22)

    jar(base, lines, G, s, tone=1.0, neck_rope=True)
    return base.done() + lines.done()


def shadow(alpha, foot, sun=0.8, toward=0.12, knee=22.0, deep=2):
    """The shadow the animal throws on the ground to its right: its own shape laid over. Its legs throw thin
    streaks; its body, which has some width to it, a thicker band. -> mask."""
    shape = alpha.shape
    x, y = grid(shape)
    fx, fy = foot
    h = (y - fy) / toward                                    # how high the thing is whose shadow falls on this row
    flat = sample(alpha, x - h * sun, fy - h) * (y >= fy) * (h < shape[0])
    def deepen(m, by):
        pad = np.pad(m, ((by + 1, by + 1), (0, 0)))
        out = np.zeros(shape, dtype=F32)
        for dy in range(-by, by + 1):
            out = np.maximum(out, pad[by + 1 + dy:by + 1 + dy + shape[0]])
        return out

    low = deepen(flat * (h <= knee), 1)                      # a leg is a few fingers across
    high = deepen(flat * (h > knee), deep)                   # the body is some way across: its shadow is as deep
    return np.clip(np.maximum(low, high), 0, 1).astype(F32)


def hooves(foot, scale):
    """Where the four hooves stand in the picture: (x, y, half-width in pixels), near pair first."""
    fx, fy = foot
    out = []
    for leg, far in ((FORE, False), (HIND, False), (FORE, True), (HIND, True)):
        xs = [p[0] for p in leg if p[1] <= 0.1]
        dx, dy = FAR if far else (0.0, 0.0)
        out.append((fx + (sum(xs) / len(xs) + dx) * scale, fy - dy * scale, (max(xs) - min(xs)) / 2 * scale))
    return out


def render(shape, foot, scale, back, seed=6, fast=False, tint_color="#62507f", amount=0.5):
    """The finished cut-out, standing on `back` (the painted backdrop): the donkey and the jars brushed and
    made crisp again, and under them their shadow, which is the backdrop's own sand gone darker and cooler.
    -> (color, mask, notes). The shadow thins out at its edge in a speckle, since a cut-out's edge is hard."""
    color, alpha, lc, la = donkey(shape, foot, scale)
    solid = np.maximum(alpha, la)
    ys, xs = np.nonzero(solid > 0.02)
    y0, y1, x0, x1 = max(ys.min() - 20, 0), min(ys.max() + 30, shape[0]), max(xs.min() - 20, 0), min(xs.max() + 90, shape[1])
    sh = shadow(alpha, foot)                                 # the shadow, on the ground (ropes are too thin to throw one)
    sh = np.clip(blur(warp(sh, 1.3, 9.0, seed + 2), 0.9) * 1.5, 0, 1)
    for (hx, hy, r) in hooves(foot, scale):                  # and it is darkest where each hoof stands
        sh = np.maximum(sh, mask_ellipse(shape, hx + r * 0.6, hy + 0.5, r * 1.7, max(1.2, r * 0.6), soft=0.7) * 0.9)
    ground = back.copy()
    tint(ground, tint_color, np.clip(sh * amount, 0, 1))
    canvas = back.copy()                                     # the animal, brushed
    over(canvas, color, alpha)
    painted = canvas.copy()
    if not fast:
        painted[y0:y1, x0:x1] = strokes(canvas[y0:y1, x0:x1], sizes=(6, 3, 2), seed=seed, density=1.9, jitter=0.03, keep=0.46)
    over(painted, lc, la)
    body = (solid > 0.5).astype(F32)
    over(ground, painted, body)
    rng = np.random.default_rng(seed + 1)
    speck = 0.10 + 0.22 * rng.random(shape)                  # the shadow's edge breaks up into the sand's own grain
    mask = np.maximum(body, (sh > speck).astype(F32))
    return ground, mask, dict(body=body > 0.5, shadow=sh, box=(x0, y0, x1, y1))


if __name__ == "__main__":
    import sys
    from PIL import Image
    shape = (150, 220)
    k = 6
    back = np.empty(shape + (3,), dtype=F32)
    back[...] = rgb("#dba25c")
    c, a, notes = render(shape, (100, 110), 0.507, back, fast="fast" in sys.argv)
    pic = back.copy()
    over(pic, c, a)
    Image.fromarray((np.clip(pic, 0, 1) * 255).astype(np.uint8)).resize((shape[1] * k, shape[0] * k), Image.NEAREST).save("out/egypt1-look/donkey-try.png")
    print("ok")

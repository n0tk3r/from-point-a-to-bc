"""What the builders have put up against the pyramid, for egypt_site.py: the mud-brick podium before the
doorway and the flight of steps down from it, the timber scaffold on the shaded face, and the masons'
cradles slung on ropes."""

import math

import numpy as np

from egypt_site_kit import *
from egypt_site_plan import *
import egypt_site_props as props

MUD = dict(lit="#e4bf8c", front="#b99069", top="#f3deb0", riser="#a17a5c", dark="#75584e", joint="#8d6a52", plaster="#d6b488", wood="#d9b47c")
BATTER = 16.0                                               # the podium's walls lean in this much at the top


def podium(sheet, crisp=False, seed=5):
    """The block of mud brick the landing is on: its sunlit left end, its front, the edge of its top."""
    rng = np.random.default_rng(seed)
    s0, s1, q0 = POD_S0, POD_S1, -POD_OUT
    end = [G(s0, q0, 0), G(s0, -BANK, 0), G(s0 + BATTER, 0, CY), G(s0 + BATTER, Q_FACE, LAND_Y), G(s0 + BATTER, q0 + BATTER, LAND_Y)]
    sheet.poly([P(*p) for p in end], MUD["lit"])
    front = [GP(s0, q0, 0), GP(s1, q0, 0), GP(s1, q0 + BATTER, LAND_Y), GP(s0 + BATTER, q0 + BATTER, LAND_Y)]
    sheet.poly(front, MUD["front"])
    sheet.poly([GP(s0 + BATTER, q0 + BATTER, LAND_Y), GP(s1, q0 + BATTER, LAND_Y), GP(s1, Q_FACE, LAND_Y), GP(s0 + BATTER, Q_FACE, LAND_Y)], MUD["top"])
    # the front is darker low down and toward the steps, where their flank shades it a little
    sheet.poly([GP(s0, q0, 0), GP(s1, q0, 0), GP(s1, q0 + 6, 110), GP(s0 + 6, q0 + 6, 70)], MUD["dark"], 0.28)
    if not crisp:
        return sheet

    def fr(s, y):                                            # a place on the front wall
        return GP(s, q0 + BATTER * y / LAND_Y, y)

    def en(q, y):                                            # a place on the left end
        return GP(s0 + BATTER * min(1.0, y / LAND_Y), q, y)

    # courses of brick: every other bed drawn, broken, with a few upright joints
    yy = 14.0
    row = 0
    while yy < LAND_Y - 8:
        sa = s0 + 6
        while sa < s1 - 10:
            run = 60 + rng.random() * 170
            sb_ = min(sa + run, s1 - 6)
            sheet.line([fr(sa, yy + rng.normal(0, 1.0)), fr(sb_, yy + rng.normal(0, 1.0))], MUD["joint"], 0.8, 0.30 + 0.25 * rng.random())
            sa = sb_ + 14 + rng.random() * 50
        for _ in range(7):
            sj = s0 + 12 + rng.random() * (s1 - s0 - 24)
            sheet.line([fr(sj, yy), fr(sj, yy + 13)], MUD["joint"], 0.7, 0.35)
        yy += 26.0 if row % 2 else 13.0
        row += 1
    for q in np.arange(q0 + 20, Q_FACE - 10, 34):            # and on the sunlit end, seen sideways
        pass
    yy = 14.0
    while yy < LAND_Y - 8:
        qa = q0 + 6
        qb = min(Q_FACE - 4, -BANK + (yy / CY) * BANK if yy < CY else (yy - CY) / TAN) - 6      # as far in as the bank or the stone allows
        if qb > qa + 10:
            sheet.line([en(qa, yy), en(qb, yy)], MUD["joint"], 0.8, 0.32)
        yy += 26.0
    # ends of the tie beams built into the brickwork
    for row_y, first in ((205, 55), (92, 100)):
        for sj in np.arange(s0 + first, s1 - 30, 92):
            cx, cy = fr(sj + rng.normal(0, 6), row_y)
            sheet.ellipse(cx, cy, 1.9, 1.9, "#4a3020")
            sheet.ellipse(cx - 0.5, cy - 0.5, 1.0, 1.0, "#9a7448")
            sheet.line([(cx + 0.5, cy + 2), (cx + 1.0, cy + 7 + rng.random() * 6)], "#6a5046", 0.9, 0.3)     # and the stain that runs from each
    # edges: the coping in the sun, the corner between the lit end and the front, the foot
    sheet.line([fr(s0 + BATTER, LAND_Y), fr(s1, LAND_Y)], "#fff0c8", 1.3, 0.9)
    sheet.line([fr(s0 + BATTER, LAND_Y - 5), fr(s1, LAND_Y - 5)], MUD["dark"], 0.8, 0.5)
    sheet.line([GP(s0, q0, 0), GP(s0 + BATTER, q0 + BATTER, LAND_Y)], "#fbe2b4", 1.0, 0.7)
    sheet.line([P(*end[4]), P(*end[3])], "#fff0c8", 1.1, 0.85)
    sheet.line([GP(s0, q0, 0), GP(s1, q0, 0)], MUD["dark"], 1.0, 0.45)
    return sheet


def _profile():
    """The steps in side view: (cm out from the podium, height)."""
    prof = [(0.0, LAND_Y)]
    for i in range(STEPS):
        prof.append((i * TREAD, LAND_Y - (i + 1) * RISE))
        if i < STEPS - 1:
            prof.append(((i + 1) * TREAD, LAND_Y - (i + 1) * RISE))
    return prof


def steps(sheet, crisp=False, seed=6):
    """The flight of steps: brick, each step edged with a timber. We see its flank (in the sun), the
    risers (turned from it) and a sliver of every tread."""
    rng = np.random.default_rng(seed)
    prof = _profile()
    flank = [stairp(a, -1, yy) for a, yy in prof] + [stairp(0, -1, 0)]
    sheet.poly(flank, MUD["lit"])
    for i in range(STEPS):
        h0 = LAND_Y - i * RISE
        h1 = h0 - RISE
        k = 1 + rng.normal(0, 0.035)
        sheet.poly([stairp(i * TREAD, -1, h0), stairp(i * TREAD, 1, h0), stairp(i * TREAD, 1, h1), stairp(i * TREAD, -1, h1)], np.clip(rgb(MUD["riser"]) * k, 0, 1))
        if i < STEPS - 1:
            sheet.poly([stairp(i * TREAD, -1, h1), stairp(i * TREAD, 1, h1), stairp((i + 1) * TREAD, 1, h1), stairp((i + 1) * TREAD, -1, h1)], np.clip(rgb(MUD["top"]) * (1 + rng.normal(0, 0.025)), 0, 1))
    # the flank is a little darker toward its foot and its back corner
    sheet.poly([stairp(0, -1, 0), stairp(RUN - TREAD, -1, 0), stairp(RUN * 0.5, -1, 40), stairp(0, -1, 90)], MUD["front"], 0.35)
    if not crisp:
        return sheet
    # brick beds on the flank, as long as the steps above them allow
    yy = 13.0
    row = 0
    while yy < LAND_Y - 4:
        amax = TREAD * math.floor((LAND_Y - yy) / RISE) - 6
        a0 = 6.0
        while a0 < amax - 12:
            a1 = min(amax, a0 + 50 + rng.random() * 150)
            sheet.line([stairp(a0, -1, yy + rng.normal(0, 0.8)), stairp(a1, -1, yy + rng.normal(0, 0.8))], MUD["joint"], 0.8, 0.28 + 0.22 * rng.random())
            a0 = a1 + 10 + rng.random() * 40
        for _ in range(5):
            aj = rng.random() * max(amax, 1)
            sheet.line([stairp(aj, -1, yy), stairp(aj, -1, yy + 13)], MUD["joint"], 0.7, 0.3)
        yy += 26.0 if row % 2 else 13.0
        row += 1
    # every step: the timber along its edge (light on top, dark beneath), its end showing on the flank
    for i in range(STEPS):
        h0 = LAND_Y - i * RISE
        a = i * TREAD
        l, r = stairp(a, -1, h0), stairp(a, 1, h0)
        wd = max(1.0, 9.0 * FOC / stair(a, 0, 0)[2])
        sheet.line([(l[0], l[1] + wd * 0.9), (r[0], r[1] + wd * 0.9)], "#5c4034", wd * 0.8, 0.75)
        sheet.line([l, r], MUD["wood"], wd, 0.95)
        sheet.line([(l[0] + 1, l[1] - wd * 0.3), (r[0] - 1, r[1] - wd * 0.3)], "#fff0c8", max(0.7, wd * 0.4), 0.7)
        sheet.ellipse(l[0], l[1] + wd * 0.2, wd * 0.75, wd * 0.75, "#4a3020")
        sheet.ellipse(l[0] - 0.3, l[1] + wd * 0.1, wd * 0.4, wd * 0.4, "#b08a58")
        b = stairp(a, -1, h0 - RISE)
        sheet.line([l, b], "#8a6850", 0.8, 0.5)                                       # the riser's corner against the flank
    sheet.line([stairp(0, -1, 0), stairp(RUN - TREAD, -1, 0)], MUD["dark"], 1.0, 0.5)  # where the flank meets the sand
    # a rope rail on the far side: posts and a slack rope from post to post
    tops = []
    for i in (0, 4, 8, 12, 16):
        a = (i + 0.4) * TREAD
        h = LAND_Y - (i + (1 if i else 0)) * RISE
        foot, head = stairp(a, 1, h), stairp(a, 1, h + 92)
        props.log(sheet, foot, head, max(1.3, 8 * FOC / stair(a, 0, 0)[2]))
        props.lash(sheet, head[0], head[1] + 2.5, 1.5, seed=i)
        if i in (0, 16):                                                             # a strip of red linen tied on the end posts
            sheet.poly([(head[0], head[1] + 1), (head[0] + 6, head[1] + 3), (head[0] + 8.5, head[1] + 9), (head[0] + 3.5, head[1] + 7), (head[0], head[1] + 5)], "#b8402c")
        tops.append((head[0], head[1] + 2.5))
    for (a0, b0), (a1, b1) in zip(tops[:-1], tops[1:]):
        sag = [(lerp(a0, a1, t), lerp(b0, b1, t) + math.sin(t * math.pi) * 3.2) for t in np.linspace(0, 1, 7)]
        sheet.line(sag, props.ROPE[0], 1.0, 0.9)
        sheet.line([(px, py - 0.5) for px, py in sag], props.ROPE[2], 0.6, 0.7)
    return sheet


def works_shadow(shape):
    """The shadow the podium and steps throw on the sand to their right."""
    up = [stair(i * TREAD, sd, LAND_Y - i * RISE) for i in range(0, STEPS, 3) for sd in (-1, 1)]
    up += [G(POD_S1, -POD_OUT, LAND_Y), G(POD_S1, Q_FACE, LAND_Y), G(POD_S0, -POD_OUT, LAND_Y)]
    low = [stair(0, 1, 0), stair(RUN - TREAD, 1, 0), stair(RUN - TREAD, -1, 0), G(POD_S1, -POD_OUT, 0), G(POD_S1, -BANK, 0)]
    return mask_poly(shape, hull(shade_of(up) + [P(*p) for p in low]), soft=1.4)


def works_shade(shape):
    """The parts of the podium and the steps that stand in the pyramid's own shadow: all of the podium,
    the top of the flight, and the back of its flank. -> mask"""
    s0, s1, q0 = POD_S0, POD_S1, -POD_OUT
    polys = [[GP(s0, q0, 0), GP(s0, -BANK, 0), GP(s0 + BATTER, 0, CY), GP(s0 + BATTER, Q_FACE, LAND_Y), GP(s0 + BATTER, q0 + BATTER, LAND_Y)],
             [GP(s0, q0, 0), GP(s1, q0, 0), GP(s1, q0 + BATTER, LAND_Y), GP(s0 + BATTER, q0 + BATTER, LAND_Y)],
             [GP(s0 + BATTER, q0 + BATTER, LAND_Y), GP(s1, q0 + BATTER, LAND_Y), GP(s1, Q_FACE, LAND_Y), GP(s0 + BATTER, Q_FACE, LAND_Y)]]

    def cut(height_of):                                      # how far down the flight the shadow reaches, along its near edge
        lo, hi = 0.0, RUN
        for _ in range(30):
            mid = (lo + hi) / 2
            if shaded(*stair(mid, -1, height_of(mid))):
                lo = mid
            else:
                hi = mid
        return lo
    a_top = cut(lambda a: LAND_Y - (math.floor(a / TREAD) + 1) * RISE)
    a_low = cut(lambda a: 0.0)
    prof = [(a, yy) for a, yy in _profile() if a <= a_top]
    polys.append([stairp(a, -1, yy) for a, yy in prof] + [stairp(a_top, -1, prof[-1][1]), stairp(a_low, -1, 0), stairp(0, -1, 0)])
    for i in range(STEPS):
        h0 = LAND_Y - i * RISE
        if shaded(*stair((i + 0.5) * TREAD, 0, h0 - RISE)):
            polys.append([stairp(i * TREAD, -1, h0), stairp(i * TREAD, 1, h0), stairp((i + 1) * TREAD, 1, h0 - RISE), stairp((i + 1) * TREAD, -1, h0 - RISE)])
    out = np.zeros(shape, dtype=F32)
    for poly in polys:
        out = np.maximum(out, mask_poly(shape, poly))
    return out


SCAF_S = (1540.0, 1690.0, 1840.0, 1990.0)                   # the scaffold's uprights, along the foot of the face
SCAF_V = (215.0, 430.0, 645.0, 860.0)                       # its stagings, above the foot
SCAF_OUT = 95.0                                             # how far its uprights stand off the stone


def scaffold(sheet, seed=8):
    """Poles lashed with rope, leaning with the slope of the face, and four stagings of planks on them."""
    rng = np.random.default_rng(seed)
    reach = SCAF_OUT / math.sin(math.radians(BETA))          # the same distance measured level
    k = FOC / 2900.0
    # the stagings, top one first: the under side of the planks if we look up at them, the top if we look down
    for v in reversed(SCAF_V):
        a, b = SCAF_S[0] - 40, SCAF_S[-1] + 45
        if v == SCAF_V[-1]:
            a = SCAF_S[1] - 30
        quad = [P(*SHADE.plumb(a, v, 0)), P(*SHADE.plumb(b, v, 0)), P(*SHADE.plumb(b, v, -reach - 12)), P(*SHADE.plumb(a, v, -reach - 12))]
        above = CY + v > EYE
        sheet.poly(quad, "#54402f" if above else "#cfa874")
        for s in np.arange(a + 55, b, 62 + rng.random() * 20):                          # plank ends
            sheet.line([P(*SHADE.plumb(s, v, 0)), P(*SHADE.plumb(s, v, -reach - 12))], "#3a2a1e" if above else "#8a6844", 0.7, 0.6)
        sheet.line([quad[3], quad[2]], "#e2bc84", 1.3, 0.95)                             # their front edge, in the light
        sheet.line([(quad[3][0], quad[3][1] + 1.3), (quad[2][0], quad[2][1] + 1.3)], "#46301f", 0.9, 0.8)
        for s in SCAF_S:                                                                 # putlogs: short poles from the ledger in to the stone
            if s >= a:
                props.log(sheet, P(*SHADE.plumb(s + 6, v - 8, -reach - 22)), P(*SHADE.plumb(s + 6, v - 8, 0)), 1.5)
    # a brace or two
    props.log(sheet, SHADE.pt(SCAF_S[0], 0, SCAF_OUT), SHADE.pt(SCAF_S[2], SCAF_V[1], SCAF_OUT), 1.4)
    props.log(sheet, SHADE.pt(SCAF_S[3], SCAF_V[1], SCAF_OUT), SHADE.pt(SCAF_S[1], SCAF_V[3], SCAF_OUT), 1.4)
    # ledgers along each staging, then the uprights over them
    for v in SCAF_V:
        a = SCAF_S[0] - 55 if v != SCAF_V[-1] else SCAF_S[1] - 45
        props.log(sheet, SHADE.pt(a, v - 8, SCAF_OUT), SHADE.pt(SCAF_S[-1] + 60, v - 8, SCAF_OUT), 2.0)
    for i, s in enumerate(SCAF_S):
        top = SCAF_V[-1] + 95 + rng.random() * 60 if i else SCAF_V[-2] + 80
        pts = [SHADE.pt(s + rng.normal(0, 4), v, SCAF_OUT) for v in (-(CY + SCAF_OUT * 0.5) + 4, 300, 650, top)]
        for a, b in zip(pts[:-1], pts[1:]):
            props.log(sheet, a, b, 2.4)
        for v in SCAF_V:
            if v < top - 30:
                c = SHADE.pt(s, v - 8, SCAF_OUT)
                props.lash(sheet, c[0], c[1], 2.3, seed=int(s + v))
    # ladders from staging to staging, each leaning in against the one above
    for j, (va, vb, s) in enumerate(((0.0 - CY * 0.2, SCAF_V[0], SCAF_S[0] + 62), (SCAF_V[0], SCAF_V[1], SCAF_S[2] + 50), (SCAF_V[1], SCAF_V[2], SCAF_S[1] + 46), (SCAF_V[2], SCAF_V[3], SCAF_S[2] + 70))):
        for side in (0.0, 34.0):
            foot = P(*SHADE.plumb(s + side, va, -reach + 6)) if j else P(*G(s + side, -BANK - 40, 0))
            head = P(*SHADE.plumb(s + side + 16, vb + 46, -reach - 10))
            sheet.line([foot, head], "#46301f", 1.5)
            sheet.line([(foot[0] - 0.4, foot[1]), (head[0] - 0.4, head[1])], "#b89060", 0.7, 0.9)
            if side == 0.0:
                f0, h0 = foot, head
        n = 8
        for i in range(1, n):
            t = i / n
            sheet.line([(lerp(f0[0], h0[0], t), lerp(f0[1], h0[1], t)), (lerp(foot[0], head[0], t), lerp(foot[1], head[1], t))], "#6a4c30", 0.9, 0.95)
    # a rope down from the top staging with a basket of chips on it, and things left on the planks
    a = P(*SHADE.plumb(SCAF_S[3] - 40, SCAF_V[3] - 4, -reach - 16))
    b = (a[0] + 2, a[1] + 74)
    sheet.line([a, (a[0] + 1.5, a[1] + 36), b], props.ROPE[0], 1.0, 0.95)
    sheet.line([(a[0] - 0.5, a[1]), (b[0] - 0.5, b[1])], props.ROPE[2], 0.5, 0.7)
    props.basket(sheet, b[0], b[1] + 9, 9, 8, shadow=False)
    c = P(*SHADE.plumb(SCAF_S[1] + 70, SCAF_V[1], -reach * 0.6))
    props.jar(sheet, c[0], c[1], 9, "water", shadow=False)
    c = P(*SHADE.plumb(SCAF_S[2] + 20, SCAF_V[2], -reach * 0.6))
    props.basket(sheet, c[0], c[1], 8, 6, shadow=False)
    c = P(*SHADE.plumb(SCAF_S[0] + 30, SCAF_V[0], -reach * 0.5))
    props.jar(sheet, c[0], c[1], 8, "beer", shadow=False, stopper="#8c7c6c")
    return sheet


def cradles(sheet, seed=10):
    """Planks slung on ropes from above, where masons were polishing the casing: one far along the sunlit
    face, one on the shaded face left of the door. Nobody is on them: the work has stopped."""
    rng = np.random.default_rng(seed)
    for face, s, v, wide, lit in ((LIT, 2300.0, 520.0, 170.0, True), (SHADE, 520.0, 610.0, 150.0, False)):
        k = FOC / face.at(s, v)[2]
        rope_dark, rope_light = (props.ROPE[0], props.ROPE[2]) if lit else ("#5a4c5c", "#9c8c98")
        wood = props.WOOD if lit else ("#3a2c2c", "#6a5448", "#9a8474")
        for ds in (-wide * 0.42, wide * 0.42):
            a = P(*face.plumb(s + ds, v, -70))
            b = face.pt(s + ds, v + 260, 4)
            c = face.pt(s + ds, v + 2600, 4)
            if lit:                                                              # the rope's shadow on the sunlit stone beside it
                sheet.line([(b[0] + 3.5, b[1] + 2), (c[0] + 3.5, c[1] + 2)], "#c89a64", max(1.0, 2.4 * k), 0.45)
            sheet.line([a, b, c], rope_dark, max(1.0, 2.6 * k), 0.95)
            sheet.line([(a[0] - 0.5, a[1]), (b[0] - 0.5, b[1]), (c[0] - 0.5, c[1])], rope_light, max(0.5, 1.1 * k), 0.6)
        q = [P(*face.plumb(s - wide / 2, v, 6)), P(*face.plumb(s + wide / 2, v, 6)), P(*face.plumb(s + wide / 2, v, -92)), P(*face.plumb(s - wide / 2, v, -92))]
        if lit:
            sheet.poly([(px + 7, py + 5) for px, py in q], "#c89a64", 0.5)
        sheet.poly(q, wood[0] if CY + v > EYE else wood[2])
        sheet.line([q[3], q[2]], wood[2], max(1.0, 5 * k), 0.95)
        sheet.line([(q[3][0], q[3][1] + max(1.0, 4 * k)), (q[2][0], q[2][1] + max(1.0, 4 * k))], wood[0], max(0.8, 3 * k), 0.8)
        c = P(*face.plumb(s + wide * 0.18, v, -50))
        props.jar(sheet, c[0], c[1], max(4.0, 34 * k), "water", props.POT if lit else ("#4a3038", "#7a5650", "#9a7468", "#b89888"), shadow=False)
    return sheet

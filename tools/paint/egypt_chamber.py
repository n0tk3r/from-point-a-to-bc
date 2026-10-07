"""Egypt, about 2560 B.C.: the king's burial chamber inside the Great Pyramid, nearly ready.
A plain, severe room of dark red granite, and in it the richest things in the world, half unpacked.
An old goldsmith is finishing them by lamplight.

THE PLAN
  Light      Six small oil lamps and nothing else. A: on a tall stand in the back left corner. B: on a tall
             stand behind the treasure. C: on the goldsmith's bench (the key light: it lights the fronts of
             the gold). D: a dish lamp set on the rim of the sarcophagus. E: on the gilded stand at the
             right edge, in front of everything. F: a dish lamp on the floor by the doorway. Each makes a
             warm pool on the stone, yellow at its heart and red at its edge; the ceiling, the upper courses
             and the corners fall away into cool brown-violet. Every lamp throws its own shadows, and the
             other lamps fill them.
  Depth      horizon -200, full 585 (the game's numbers), a long lens. The back wall meets the floor at
             row 400 and the ceiling at row 50; the back corners are at x 150 and x 750.
  Three tones  DARK: ceiling, upper wall, the doorway, the things at the front edge. MIDDLE: lamplit
             granite, cold red-grey. LIGHT: the gold, and with it linen and alabaster: all gathered on the
             left half of the back wall and on the bench, where the eye should go; the sarcophagus's lit rim
             answers it on the right.
  Left       the low square doorway in the left wall (67..135, 330..469): exit to the gallery. Left of it,
             two carrying poles and a rope sling lean on the wall, with lamp F at their feet.
  Back wall  x 140..458 the treasure: lamp A, jars, canopy poles, rolled mats, the carrying-chair, a long
             chest with boxes and jars stood on it, the bed with linen before it, lamp B, the armchair, two
             more chests (the bracelet box on top), basins, a basket. The wall above is dappled with the
             gold's reflections.
             x 460..545 NOTHING: the place that hums (500, 300), and the swept ring on the floor (500, 500).
  Right      the sarcophagus (554..746, 383..500); its lid leans on the back wall behind it, still roped;
             the masons' lever, rollers and rope lie by its right-hand end.
  Front      the goldsmith's bench (250..350, baseline 513) with his lamp, tools and mirror; his water jug,
             the brazier and a basket of charcoal beside it. Bottom left corner: a banded chest and jars.
             Right edge: lamp E on its stand, and an oil jar. (front plane)

  python3 egypt_chamber.py fast      block-in and details, no brush pass (for composing)
  python3 egypt_chamber.py           everything, and the finished files in out/egypt-chamber/
  python3 egypt_chamber.py crop x y w h [times]     enlarge part of the last picture, to look at
"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
from egypt_chamber_kit import *
import egypt_chamber_things as th

OUT = "out/egypt-chamber"
WORK = "out/egypt-chamber-work"

#            name   X      Y     D     power  reach
LAMPS = [Lamp("A", -411, 178, 22, 3.4, 130),
         Lamp("B", -112, 168, 14, 3.6, 132),
         Lamp("C", -236, 88, 318, 2.1, 200),
         Lamp("D", 330, 116, 215, 3.8, 135),
         Lamp("E", 344, 170, 560, 3.2, 215),
         Lamp("F", -478, 9, 318, 1.5, 80)]                # a dish lamp set down on the floor by the doorway
AMB = np.array([0.115, 0.100, 0.220], dtype=F32)          # the cool air of a room with no window
GRANITE = rgb("#8c6868")                                   # red granite, kept on the grey side: the gold is to be the warm thing here
FLOORSTONE = rgb("#96807c")
DUST = rgb("#b8a290")
BACK_JOINTS = {0: [-262, -20, 196, 372], 1: [-340, -118, 150, 330], 2: [-225, -40, 210], 3: [-330, -80, 130, 365], 4: [-190, 60, 290]}       # (none in the place that hums)
DOOR = (30.0, 136.0)                                       # the doorway: from..to along the left wall, cm from the corner
DOOR_H = float(COURSES[1])
BEAMS = np.linspace(-XL, XR, 10)                           # nine beams across the ceiling
SLABS = np.array([-60.0, 70.0, 196.0, 318.0, 446.0, 580.0, 720.0])     # rows of paving, out from the back wall
HUM = (61.0, 307.0)                                        # the floor in front of the place that hums: (X, D)
SARC = dict(x0=135.0, x1=363.0, d0=208.0, d1=307.0, h=105.0, t=15.0)
LID = dict(x0=197.0, x1=425.0, wide=99.0, thick=22.0, lean=16.0)


def expose(albedo, light):
    """Stone under lamplight: never burnt out, never dead black."""
    return (1 - np.exp(-albedo * (AMB + light) * 1.35)).astype(F32)


def stone(base, tone, tone2, mottle, vein, amount=1.0):
    """Granite: every block a little lighter or darker, redder or greyer than its neighbours, and mottled."""
    c = base[None, None, :] * (1 + amount * (0.13 * tone + 0.16 * (mottle - 0.5) + 0.06 * (vein - 0.5)))[..., None]
    c[..., 0] += 0.035 * tone2 * amount
    c[..., 1] -= 0.006 * tone2 * amount
    c[..., 2] -= 0.022 * tone2 * amount
    return np.clip(c, 0, 1).astype(F32)


def lamp_sum(X, Y, D, n, shadows=None, wrap=0.22, only=None):
    """All the lamps' light on a surface, in color. `shadows` is {lamp name: mask} where a lamp is hidden."""
    total = np.zeros(SHAPE + (3,), dtype=F32)
    for l in LAMPS:
        if only is not None and l.name not in only:
            continue
        e = lamplight(l, X, Y, D, n, wrap)
        if shadows and l.name in shadows:
            e = e * (1 - shadows[l.name])
        total += e[..., None] * flame_color(e)
    return total


def door_corners():
    (xf, yfb), (_, yft) = side_pt(True, DOOR[0], 0), side_pt(True, DOOR[0], DOOR_H)
    (xn, ynb), (_, ynt) = side_pt(True, DOOR[1], 0), side_pt(True, DOOR[1], DOOR_H)
    return (xf, yft, yfb), (xn, ynt, ynb)


def doorway(pic, seed):
    """The low square doorway in the left wall, and what can be seen through it: a little of the passage's
    side and floor, lit from the room, going into the dark."""
    (xf, yft, yfb), (xn, ynt, ynb) = door_corners()
    m = mask_poly(SHAPE, [(xf, yft), (xf, yfb), (xn, ynb), (xn, ynt)], wobble=0.5, seed=seed)
    deep = np.clip((xf - X_PIX) / (xf - xn), 0, 1)                          # 0 at the jamb nearest the back wall, 1 at the jamb nearest us
    reach = np.exp(-deep * 2.3) * 1.5
    side = (Y_PIX < yfb).astype(F32)                                        # the passage's side wall; below it, its floor
    grain = 0.85 + 0.3 * noise(SHAPE, 9, seed + 1, 3)
    wall = rgb("#6d4638")[None, None, :] * (reach * grain)[..., None]
    ground = rgb("#8a6654")[None, None, :] * (np.exp(-deep * 2.6) * grain)[..., None]
    inside = rgb("#0c0810")[None, None, :] + np.where(side[..., None] > 0.5, wall, ground)
    over(pic, np.clip(inside, 0, 1), m)
    info = dict(mask=m, far=(xf, yft, yfb), near=(xn, ynt, ynb))
    return info


def room(seed, blocks=()):
    """The bare room and its lamplight. -> (picture, info)."""
    info = {}
    shape = SHAPE
    # ---- the stone, surface by surface
    mottle = noise(shape, 26, seed + 1, 4)
    vein = noise(shape, (90, 9), seed + 2, 3)
    wx, wy = (noise(shape, (70, 30), seed + 11, 3) - 0.5) * 1.6, (noise(shape, (90, 26), seed + 12, 3) - 0.5) * 1.7      # no joint is ruled: each wanders half a pixel
    bt, bt2, bda, bdb, _ = ashlar(WALL_X + wx, WALL_Y + wy, COURSES, seed + 3, joints=BACK_JOINTS)
    back = stone(GRANITE, bt, bt2, mottle, vein, 1.35)
    lt, lt2, lda, ldb, _ = ashlar(LW_U + wx, LW_V + wy, COURSES, seed + 4, joints={0: [DOOR[0], DOOR[1]], 1: [152.0], 2: [58.0], 3: [118.0], 4: [40.0]})
    left = stone(GRANITE, lt, lt2, mottle, vein, 1.35)
    rt, rt2, rda, rdb, _ = ashlar(RW_U + wx, RW_V + wy, COURSES, seed + 5, joints={0: [120.0], 1: [60.0], 2: [150.0], 3: [40.0], 4: [100.0]})
    right = stone(GRANITE, rt, rt2, mottle, vein, 1.35)
    ct, ct2, cda, cdb, _ = ashlar(CEIL_D, CEIL_X + wx * 1.5, BEAMS, seed + 6, lengths=(4000.0, 5000.0))
    ceil = stone(GRANITE * 0.96, ct, ct2, mottle, vein, 1.7)
    ft, ft2, fda, fdb, _ = ashlar(FLOOR_X + wx, FLOOR_D + wy * 2.0, SLABS, seed + 7, lengths=(150.0, 290.0))
    floor = stone(FLOORSTONE, ft * 0.5, ft2 * 0.6, noise(shape, (60, 24), seed + 8, 4), vein)
    # dust lies thick along the walls and thin where people walk
    near_wall = np.exp(-np.clip(Y_PIX - FLOOR_LINE, 0, 400) / 26.0)
    dust = np.clip(0.25 + 0.5 * near_wall + 0.5 * (noise(shape, (120, 40), seed + 9, 4) - 0.5), 0, 1) * FLOOR_MASK
    over(floor, DUST, (dust * 0.42).astype(F32))

    # ---- the lamplight on each, with the shadows of what stands in the room
    def others(l):                                         # a lamp throws no shadow of its own stand
        return [b for b in blocks if not (b.who == "stand" and abs(b.outline[0][0] - l.X) < 12 and abs(b.outline[0][1] - l.D) < 12)]
    fsh = {l.name: soften(floor_shadows(l, others(l)), 1.4, 7.0, l, "floor") for l in LAMPS}
    wsh = {l.name: soften(wall_shadows(l, others(l)), 1.6, 9.0, l, "wall") for l in LAMPS}
    s, c = np.sin(SPLAY), np.cos(SPLAY)
    L_back = lamp_sum(WALL_X, WALL_Y, 0.0, (0, 0, 1), wsh, wrap=0.42)
    L_floor = lamp_sum(FLOOR_X, 0.0, FLOOR_D, (0, 1, 0), fsh, wrap=0.2)
    L_left = lamp_sum(-XL - LW_U * s, LW_V, LW_U * c, (c, 0, s), wrap=0.42)
    L_right = lamp_sum(XR + RW_U * s, RW_V, RW_U * c, (-c, 0, s), wrap=0.42)
    L_ceil = lamp_sum(CEIL_X, HC, CEIL_D, (0, -1, 0), wrap=0.3) * 1.1
    for l in LAMPS[:4]:                                    # a faint blush on the beams above each lamp that stands under them
        cx, cy = ceil_pt(l.X, l.D)
        blush = mask_ellipse(shape, cx, cy + 6, 150, 46, soft=22) * CEIL_MASK
        L_ceil += (blush * 0.34 * l.power / 3.0)[..., None] * WEAK[None, None, :]

    pic = np.zeros(shape + (3,), dtype=F32)
    light = np.zeros(shape + (3,), dtype=F32)
    for alb, lg, m in ((ceil, L_ceil, CEIL_MASK), (back, L_back, BW_MASK), (left, L_left, LW_MASK), (right, L_right, RW_MASK), (floor, L_floor, FLOOR_MASK)):
        over(pic, alb, m)
        over(light, lg, m)
    # the dark gathers overhead and in the corners of the picture: the lamps are low, and small
    up = np.where(FLOOR_MASK > 0.5, 0.0, np.where(X_PIX < LEFT, LW_V, np.where(X_PIX > RIGHT, RW_V, WALL_Y)))
    up = np.where(CEIL_MASK > 0.5, HC, up)
    gloom = 1 - 0.40 * step(180.0, 440.0, up)
    edge = np.clip(((X_PIX - 420) / 520.0) ** 2 + (np.maximum(Y_PIX - 430, 0) / 330.0) ** 2, 0, 1)
    gloom = gloom * (1 - 0.34 * edge ** 1.3)
    gloom = (gloom * (0.93 + 0.14 * noise(shape, 110, seed + 30, 3))).astype(F32)            # and nothing is lit evenly
    light = light * gloom[..., None]
    lum = light @ np.array([0.35, 0.5, 0.15], dtype=F32)
    light = light * (np.clip(lum, 1e-3, 9) ** 0.45 * 1.03)[..., None]        # deepen the dark between the pools: lamplight is all or nothing
    bounce = blur(light, 46) * 0.09                         # light that has already struck stone once: it fills the shadows a little, and is redder
    bounce[..., 1] *= 0.86
    bounce[..., 2] *= 0.74
    pic = expose(pic, light + bounce)
    # ---- where surfaces meet, the dark collects
    below = Y_PIX - FLOOR_LINE
    ao = 0.34 * np.exp(-np.clip(below, 0, 99) / 8.0) * FLOOR_MASK + 0.26 * np.exp(-np.clip(-below, 0, 99) / 7.0) * (1 - FLOOR_MASK)
    ao += 0.30 * np.exp(-np.abs(Y_PIX - TOP_LINE) / 7.0)
    for cx in (LEFT, RIGHT):
        ao += 0.28 * np.exp(-np.abs(X_PIX - cx) / 6.0) * (Y_PIX > TOP) * (Y_PIX < WALL)
    tint(pic, "#22141e", np.clip(ao, 0, 0.6).astype(F32))
    info.update(light=light, joints=dict(back=(bda, bdb), left=(lda, ldb), right=(rda, rdb), ceil=(cda, cdb), floor=(fda, fdb)),
                fsh=fsh, wsh=wsh, door=doorway(pic, seed + 50))
    return pic, info


def stone_marks(pic, seed):
    """Granite is not all one stuff: dark knots where another rock was caught up in it, and pale veins that
    cross a block from side to side. A few of each, so that every great block is itself."""
    rng = np.random.default_rng(seed)
    stone_here = np.clip(BW_MASK + LW_MASK + RW_MASK + CEIL_MASK * 0.6 + FLOOR_MASK * 0.7, 0, 1)
    knots = np.zeros(SHAPE, dtype=F32)
    for i in range(20):
        x, y = rng.uniform(0, W), rng.uniform(20, 590)
        rx = rng.uniform(4, 15)
        ry = rx * rng.uniform(0.3, 0.75)
        if y > 400:                                                         # on the floor they lie flat
            ry *= 0.5
        knots = np.maximum(knots, mask_ellipse(SHAPE, x, y, rx, ry, soft=1.2) * rng.uniform(0.5, 1.0))
    knots = warp(knots, 3.0, 9.0, seed + 1)
    tint(pic, "#6e4a56", (knots * stone_here * 0.32).astype(F32))
    veins = np.zeros(SHAPE, dtype=F32)
    for i in range(11):
        x, y = rng.uniform(20, W - 20), rng.uniform(40, 580)
        a = rng.uniform(-0.9, 0.9) + (0 if rng.random() < 0.5 else math.pi / 2)
        n = int(rng.integers(3, 6))
        pts = [(x, y)]
        for j in range(n):
            a += rng.normal(0, 0.28)
            step_len = rng.uniform(14, 34)
            pts.append((pts[-1][0] + math.cos(a) * step_len, pts[-1][1] + math.sin(a) * step_len * (0.5 if y > 400 else 1.0)))
        veins = np.maximum(veins, mask_line(SHAPE, curve(pts, 5), rng.uniform(0.8, 1.7), soft=0.7) * rng.uniform(0.5, 1.0))
    over(pic, np.clip(pic * 1.3 + 0.025, 0, 1), (veins * stone_here * 0.5).astype(F32))
    return pic


def face(pic, pts, n, albedo, gain=1.0, cuts=None, only=None, wrap=0.22):
    """Paint one flat face of a big stone thing, pixel by pixel, with the lamplight that falls on it."""
    m = mask_poly(SHAPE, [P(*p) for p in pts])
    X, Y, D = hit(pts[0], n)
    lg = lamp_sum(X, Y, D, n, cuts, wrap, only) * gain
    lg = lg + blur(lg * m[..., None], 20) * 0.12
    over(pic, expose(albedo, lg), m)
    return m, (X, Y, D)


def lid_section():
    """The lid in cross-section (D, Y): back top, front top, front bottom, back bottom."""
    l = LID
    a = math.radians(l["lean"])
    bt = (0.0, l["wide"] * math.cos(a))
    ft = (l["thick"] * math.cos(a), bt[1] + l["thick"] * math.sin(a))
    fb = (l["wide"] * math.sin(a) + l["thick"] * math.cos(a), l["thick"] * math.sin(a))
    bb = (l["wide"] * math.sin(a), 0.0)
    return bt, ft, fb, bb, a


def sarcophagus(pic, info, seed):
    """The lid first (it leans on the wall behind), then the great box: plain, massive, of a darker stone."""
    shape = SHAPE
    s, l = SARC, LID
    dark = stone(rgb(th.STUFF["dark"]), noise(shape, 70, seed + 1, 2) - 0.5, noise(shape, 50, seed + 2, 2) - 0.5, noise(shape, 18, seed + 3, 4), noise(shape, (60, 8), seed + 4, 3))
    masks = {}
    bt, ft, fb, bb, a = lid_section()
    x0, x1 = l["x0"], l["x1"]
    wsh = info["wsh"]
    cut = {"E": wsh["E"], "C": wsh["C"], "B": wsh["B"]}
    masks["lid_end"], _ = face(pic, [(x0, bb[1], bb[0]), (x0, fb[1], fb[0]), (x0, ft[1], ft[0]), (x0, bt[1], bt[0])], (-1, 0, 0), dark, 0.8, cut)
    masks["lid_front"], _ = face(pic, [(x0, fb[1], fb[0]), (x1, fb[1], fb[0]), (x1, ft[1], ft[0]), (x0, ft[1], ft[0])], (0, math.sin(a), math.cos(a)), dark, 1.2, cut)
    masks["lid_top"], _ = face(pic, [(x0, ft[1], ft[0]), (x1, ft[1], ft[0]), (x1, bt[1], bt[0]), (x0, bt[1], bt[0])], (0, math.cos(a), -math.sin(a)), dark * 1.15, 2.4, cut, wrap=0.5)
    lp = lid_sheet()
    lc, la = lp.base.done()
    over(pic, lc, la)
    # ---- the box
    X0, X1, D0, D1, Hh, T = s["x0"], s["x1"], s["d0"], s["d1"], s["h"], s["t"]
    none = np.ones(shape, F32)
    masks["end"], _ = face(pic, [(X0, 0, D1), (X0, 0, D0), (X0, Hh, D0), (X0, Hh, D1)], (-1, 0, 0), dark, 0.7, {"E": none, "D": none})
    masks["front"], _ = face(pic, [(X0, 0, D1), (X1, 0, D1), (X1, Hh, D1), (X0, Hh, D1)], (0, 0, 1), dark, 1.05, {"B": none, "A": none, "D": none, "F": none})
    masks["rim"], _ = face(pic, [(X0, Hh, D1), (X1, Hh, D1), (X1, Hh, D0), (X0, Hh, D0)], (0, 1, 0), dark * 1.2, 1.9, wrap=0.45)
    # inside: the far wall, lit only as far down as the near wall lets the front lamp reach, and the right-hand wall
    Xi0, Xi1, Di0, Di1 = X0 + T, X1 - T, D0 + T, D1 - T
    le = [q for q in LAMPS if q.name == "E"][0]
    hole = [(Xi0, Hh, Di1), (Xi1, Hh, Di1), (Xi1, Hh, Di0), (Xi0, Hh, Di0)]
    mh = mask_poly(shape, [P(*p) for p in hole])
    over(pic, rgb("#100a10"), mh)
    Xw, Yw, Dw = hit((Xi0, Hh, Di0), (0, 0, 1))
    reach = Hh - (le.Y - Hh) * (Di1 - Di0) / (le.D - Di1)                  # how far down the far wall lamp E reaches
    cutE = step(reach + 2.0, reach - 2.0, Yw)
    lg = lamp_sum(Xw, Yw, Dw, (0, 0, 1), {"E": cutE}, 0.2, only=("E",)) * 1.5
    inner = expose(dark, lg + np.array([0.06, 0.03, 0.02], dtype=F32))
    over(pic, inner, mh * (Yw <= Hh + 0.5) * (Xw >= Xi0) * (Xw <= Xi1))
    Xw, Yw, Dw = hit((Xi1, Hh, Di0), (-1, 0, 0))
    lg = lamp_sum(Xw, Yw, Dw, (-1, 0, 0), None, 0.3, only=("D", "E")) * 0.8
    over(pic, expose(dark, lg), mh * (Dw >= Di0) * (Dw <= Di1) * (Yw <= Hh + 0.5))
    masks["hole"] = mh
    info["sarc"] = masks
    info["stonework"] = np.clip(sum(masks[k] for k in ("lid_end", "lid_front", "lid_top", "end", "front", "rim")) + la, 0, 1)
    return pic


def casters():
    """Everything that throws a shadow, as plain boxes."""
    s, l, b = SARC, LID, th.BENCH
    bx, bd = th.BRAZIER
    out = [Block([(s["x0"], s["d1"]), (s["x1"], s["d1"]), (s["x1"], s["d0"]), (s["x0"], s["d0"])], 0, s["h"], "sarcophagus"),
           Block([(l["x0"], 48), (l["x1"], 48), (l["x1"], 0), (l["x0"], 0)], 0, 100, "lid"),
           Block([(b["x0"], b["d1"]), (b["x1"], b["d1"]), (b["x1"], b["d0"]), (b["x0"], b["d0"])], b["h"] - 5, b["h"], "bench"),
           Block(box_outline(b["x0"] + 11, (b["d0"] + b["d1"]) / 2, 6, 40), 0, b["h"], "bench"),
           Block(box_outline(b["x1"] - 11, (b["d0"] + b["d1"]) / 2, 6, 40), 0, b["h"], "bench"),
           Block(box_outline(bx, bd, 24, 24), 0, 28, "brazier"),
           Block(box_outline(-262.0, 327.0, 15, 15), 0, 28, "jug"), Block(box_outline(-64.0, 332.0, 26, 26), 0, 15, "charcoal")]
    return out + th.treasure_blocks() + th.stand_blocks(LAMPS[:2])


def things_sheet():
    """The furniture, drawn crisply on a clear sheet. -> pen"""
    pen = th.Pen(LAMPS, AMB)
    for l in LAMPS[:2]:
        th.lamp_stand(pen, l.X, l.D, l.Y - 7.0, stout=1.2)
    th.carrying_poles(pen)
    lf = LAMPS[5]
    th.dish_lamp(pen, lf.X, lf.Y - 5.0, lf.D, r=7.5)
    th.treasure(pen)
    ld = LAMPS[3]
    th.dish_lamp(pen, ld.X, SARC["h"] + 3.0, ld.D)
    th.masons_things(pen, SARC)
    return pen


def lid_sheet():
    """The ropes and billets of the lid: they are behind the sarcophagus, so they are laid before it."""
    pen = th.Pen(LAMPS, AMB)
    th.lid_ropes(pen, LID, lid_section())
    return pen


def bench_sheet():
    """The goldsmith's bench and everything on it, and the brazier beside it: one cut-out."""
    pen = th.Pen(LAMPS, AMB)
    th.bench(pen)
    th.bench_things(pen)
    th.brazier(pen)
    th.bench_floor_things(pen)
    return pen


def mirror_sheet():
    pen = th.Pen(LAMPS, AMB)
    th.mirror(pen)
    return pen


def front_sheet():
    pen = th.Pen(LAMPS, AMB)
    th.front_things(pen)
    le = LAMPS[4]
    th.lamp_stand(pen, le.X, le.D, le.Y - 7.0, gilt=True, stout=1.5)
    return pen


def contact(pic, blocks):
    """Under and close round everything that stands on the floor, the light cannot get in."""
    on_floor = [[P(a, 0, c) for a, c in b.outline] for b in blocks if b.y0 <= 9]
    raised = [[P(a, 0, c) for a, c in b.outline] for b in blocks if b.y0 > 9]
    m = blur(raster(on_floor), 3.0) * 0.5 + blur(raster(on_floor), 9.0) * 0.3 + blur(raster(raised), 5.0) * 0.42
    tint(pic, "#1c1018", np.clip(m * FLOOR_MASK, 0, 0.75).astype(F32))
    return pic


def under(seed=21):
    """Everything broad and soft: the room's planes, the lamplight on them, and the big shapes of what
    stands in it. No small things."""
    blocks = casters()
    pic, info = room(seed, blocks)
    stone_marks(pic, seed + 70)
    doorway(pic, seed + 50)                                # (again: the marks went over it)
    contact(pic, blocks)
    sarcophagus(pic, info, seed + 40)
    pen = things_sheet()
    tc, ta = pen.base.done()
    over(pic, blur(tc, 0.8), blur(ta, 0.8))
    info.update(pen=pen, things=(tc, ta), blocks=blocks)
    return np.clip(pic, 0, 1), info


def joints(pic, info, seed):
    """Joints as fine as a hair: dark, a little broken, with a thread of light on the lit side of each."""
    shape = SHAPE
    light = info["light"] @ np.array([0.35, 0.5, 0.15], dtype=F32)
    wander = 0.55 + 0.45 * noise(shape, (46, 7), seed, 3)
    j = info["joints"]
    door = info["door"]["mask"]
    masks = [np.minimum(j["back"][0], j["back"][1]) * KB * BW_MASK + (1 - BW_MASK) * 9,
             np.minimum(j["left"][0] * LW_KU, j["left"][1] * LW_KV) * LW_MASK + (1 - LW_MASK * (1 - door)) * 9,
             np.minimum(j["right"][0] * RW_KU, j["right"][1] * RW_KV) * RW_MASK + (1 - RW_MASK) * 9,
             j["ceil"][1] * CEIL_K * CEIL_MASK + (1 - CEIL_MASK) * 9,
             np.minimum(j["floor"][0] * FLOOR_K, j["floor"][1] * FLOOR_ROWS) * FLOOR_MASK + (1 - FLOOR_MASK) * 9]
    dist = np.minimum.reduce(masks) + info["cover"] * 9
    line = np.clip(1.1 - dist / 0.6, 0, 1)
    tint(pic, "#2a1822", (line * wander * 0.66).astype(F32))
    lip = np.clip(1.0 - np.abs(dist - 1.5) / 0.7, 0, 1) * np.clip(light * 1.4, 0, 1)        # the arris beside the joint catches the lamp
    glow(pic, "#ffc890", (lip * wander * 0.085).astype(F32))
    chips = np.clip(1.0 - dist / 2.4, 0, 1) * step(0.9, 0.97, noise(shape, 7, seed + 1, 2))   # a chipped edge here and there
    tint(pic, "#2a1822", (chips * 0.5).astype(F32))
    return pic


def grain_of_stone(pic, info, seed, cover):
    """Granite's black and pink flecks, over all the bare stone (not over the things standing on it)."""
    dark, lightf = speckle(SHAPE, seed)
    lum = info["light"] @ np.array([0.35, 0.5, 0.15], dtype=F32)
    lit = np.clip(0.25 + lum, 0, 1)
    bare = (1 - cover) * (1 - info["door"]["mask"])
    tint(pic, "#3a2630", (dark * 0.15 * bare).astype(F32))
    over(pic, "#e0b0a0", (lightf * 0.065 * lit * bare).astype(F32))
    return pic


def floor_marks(pic, info, seed):
    """What the floor remembers: the ring the humming has swept in the dust, the track people have worn from
    the door, scraps of gold leaf under the bench, charcoal by the brazier."""
    shape = SHAPE
    rng = np.random.default_rng(seed)
    clear = 1 - info["cover"]
    floor = pic.copy()
    # ---- the swept ring in front of the place that hums
    r = np.hypot(FLOOR_X - HUM[0], FLOOR_D - HUM[1])
    broken = 0.45 + 0.55 * noise(shape, (14, 6), seed + 1, 3)
    ring = np.exp(-((r - 58.0) / 4.2) ** 2) * broken * FLOOR_MASK
    over(pic, np.clip(pic * 1.55 + 0.05, 0, 1), (ring * 0.6).astype(F32))                   # dust heaped in a ring: paler
    inside = step(56.0, 50.0, r) * FLOOR_MASK
    tint(pic, "#8a7078", (inside * 0.34).astype(F32))                                       # and swept clean within
    faint = np.exp(-((r - 74.0) / 9.0) ** 2) * (noise(shape, (8, 20), seed + 2, 2) > 0.55) * FLOOR_MASK
    over(pic, np.clip(pic * 1.25, 0, 1), (faint * 0.3).astype(F32))
    # ---- a worn track from the doorway to the bench and on to the sarcophagus
    path = curve([(108, 462), (190, 478), (300, 536), (430, 540), (560, 528), (700, 532)], 10)
    trod = mask_line(shape, path, [26 + 10 * math.sin(i * 0.4) for i in range(len(path))], soft=9.0) * FLOOR_MASK
    tint(pic, "#9a8086", (trod * 0.22 * (0.6 + 0.6 * noise(shape, (50, 16), seed + 3, 3))).astype(F32))
    s = Paper(shape)
    for i in range(22):                                                   # footprints in the dust, coming and going
        t = rng.random()
        k = int(t * (len(path) - 2))
        px, py = path[k]
        px += rng.normal(0, 9)
        py += rng.normal(0, 5)
        kk = (py - G.vy) / G.eye
        ang = math.atan2(path[k + 1][1] - path[k][1], path[k + 1][0] - path[k][0]) + rng.normal(0, 0.3)
        ca, sa = math.cos(ang), math.sin(ang) * 0.45
        ln, wd = 12 * kk, 4.2 * kk
        s.poly([(px - ca * ln - sa * wd, py - sa * ln + ca * wd * 0.45), (px + ca * ln - sa * wd, py + sa * ln + ca * wd * 0.45), (px + ca * ln + sa * wd, py + sa * ln - ca * wd * 0.45), (px - ca * ln + sa * wd, py - sa * ln - ca * wd * 0.45)], "#2e1c26", 0.20)
    # ---- two long scrapes where a chest was dragged in
    for off in (0.0, 9.0):
        drag = curve([(140, 470 + off * 0.4), (230, 462 + off), (330, 468 + off)], 8)
        s.line(drag, "#d8bcae", 0.8, 0.22)
        s.line([(a, b + 1.0) for a, b in drag], "#2e1c26", 0.8, 0.22)
    # ---- scraps of gold leaf round the bench, the brightest specks on the floor
    for i in range(26):
        px = 240 + rng.random() * 150
        py = 512 + rng.random() ** 1.5 * 34
        if rng.random() < 0.3:
            py = 486 + rng.random() * 10
            px = 352 + rng.random() * 30
        c = th.HOT if rng.random() < 0.6 else "#c8861f"
        s.poly([(px - 1.5, py), (px - 0.2, py - 0.9), (px + 1.6, py - 0.1), (px + 0.3, py + 0.8)], c, 0.9)
    for i in range(6):                                                    # charcoal spilt by the brazier
        px, py = 386 + rng.random() * 22, 508 + rng.random() * 9
        s.poly([(px - 2.2, py), (px - 0.6, py - 1.6), (px + 2.0, py - 1.0), (px + 1.4, py + 0.6)], "#1c1418", 0.95)
    # ---- wisps of packing straw where the things were unwrapped
    for i in range(34):
        px, py = 170 + rng.random() * 280, 448 + rng.random() * 22
        a = rng.random() * math.pi
        ln = 3 + rng.random() * 5
        s.line([(px, py), (px + math.cos(a) * ln, py + math.sin(a) * ln * 0.4)], "#d8c088", 0.7, 0.5)
    s.onto(pic)
    pic[...] = lerp(floor, pic, (FLOOR_MASK * clear)[..., None])
    return pic


def cracks(pic, seed):
    """A few hairline cracks: the great beams overhead cracked while the pyramid was still being built."""
    rng = np.random.default_rng(seed)
    e = Paper(SHAPE)
    starts = [((338, 50), (-0.35, -1.0), 44), ((566, 50), (0.2, -1.0), 36), ((612, 148), (0.5, 1.0), 46), ((236, 96), (0.7, 0.6), 30),
              ((690, 232), (-0.4, 1.0), 34), ((548, 566), (1.0, 0.22), 56), ((196, 548), (1.0, -0.12), 40), ((30, 150), (0.4, 1.0), 40)]
    for (x, y), (dx, dy), length in starts:
        pts = [(x, y)]
        n = math.hypot(dx, dy)
        dx, dy = dx / n, dy / n
        run = 0.0
        while run < length:
            step_len = 3 + rng.random() * 6
            a = rng.normal(0, 0.5)
            ca, sa = math.cos(a), math.sin(a)
            x, y = x + (dx * ca - dy * sa) * step_len, y + (dx * sa + dy * ca) * step_len
            pts.append((x, y))
            run += step_len
        e.line(pts, "#170c14", 0.8, 0.5)
        e.line([(a + 0.7, b + 0.5) for a, b in pts], "#e8b49c", 0.7, 0.06)
        if rng.random() < 0.6:                                             # a twig off it
            k = len(pts) // 2
            e.line([pts[k], (pts[k][0] + dy * 6 + dx * 3, pts[k][1] - dx * 6 + dy * 3)], "#170c14", 0.7, 0.4)
    e.onto(pic)
    return pic


def stone_edges(pic, info):
    """Say the hard edges of the room and of the sarcophagus again, crisply, over the brushwork."""
    e = Paper(SHAPE)
    (xf, yft, yfb), (xn, ynt, ynb) = door_corners()
    wall_dark, hair = "#1c1018", "#f0b890"
    # the room's own lines
    e.line([(LEFT, TOP), (LEFT, WALL)], wall_dark, 1.2, 0.55)
    e.line([(RIGHT, TOP), (RIGHT, WALL)], wall_dark, 1.2, 0.55)
    e.line([(LEFT, WALL + 0.3), (RIGHT, WALL + 0.3)], wall_dark, 1.3, 0.6)
    e.line([(LEFT, WALL), (0, float(LW_FOOT[0, 0]))], wall_dark, 1.3, 0.6)
    e.line([(RIGHT, WALL), (W, float(RW_FOOT[0, W - 1]))], wall_dark, 1.3, 0.6)
    e.line([(LEFT, TOP), (RIGHT, TOP)], wall_dark, 1.2, 0.6)
    e.line([(LEFT, TOP), (0, float(LW_HEAD[0, 0]))], wall_dark, 1.2, 0.55)
    e.line([(RIGHT, TOP), (W, float(RW_HEAD[0, W - 1]))], wall_dark, 1.2, 0.55)
    # the doorway: dark inside its edges, a thread of light on the lintel and the far jamb
    e.line([(xf, yft), (xn, ynt)], "#0c0810", 1.6, 0.9)
    e.line([(xn, ynt), (xn, ynb)], "#0c0810", 1.4, 0.9)
    e.line([(xf + 0.8, yft), (xf + 0.8, yfb)], hair, 0.9, 0.45)
    e.line([(xf, yft - 1.2), (xn, ynt - 1.2)], hair, 0.8, 0.28)
    e.line([(xf, yfb), (xn, ynb)], "#c8a08a", 1.0, 0.5)                    # the sill, worn pale
    e.line([(xf - 2, yfb - 0.5), (xf - 30, yfb - 0.5)], "#0c0810", 1.0, 0.5)   # where the passage's wall meets its floor
    # the sarcophagus: sharp arrises
    s = SARC
    X0, X1, D0, D1, Hh, T = s["x0"], s["x1"], s["d0"], s["d1"], s["h"], s["t"]
    rim = "#e8b090"
    e.line([P(X0, Hh, D1), P(X1, Hh, D1)], rim, 1.0, 0.55)
    e.line([P(X0, Hh, D1), P(X0, Hh, D0)], rim, 0.9, 0.35)
    e.line([P(X0, Hh, D0), P(X1, Hh, D0)], rim, 0.9, 0.5)
    e.line([P(X1, Hh, D0), P(X1, Hh, D1)], rim, 0.9, 0.6)
    e.line([P(X0 + T, Hh, D1 - T), P(X1 - T, Hh, D1 - T)], "#0a060a", 1.2, 0.85)
    e.line([P(X0 + T, Hh, D1 - T), P(X0 + T, Hh, D0 + T)], "#0a060a", 1.0, 0.8)
    e.line([P(X0 + T, Hh, D0 + T), P(X1 - T, Hh, D0 + T)], rim, 0.9, 0.5)
    e.line([P(X1 - T, Hh, D0 + T), P(X1 - T, Hh, D1 - T)], rim, 0.9, 0.5)
    e.line([P(X0, 0, D1), P(X0, Hh, D1)], "#140c12", 1.1, 0.6)
    e.line([P(X0, 0, D1), P(X1, 0, D1)], "#0c080c", 1.6, 0.75)
    e.line([P(X0, 0, D1), P(X0, 0, D0)], "#0c080c", 1.3, 0.7)
    e.line([P(X1, 0, D1), P(X1, Hh, D1)], "#140c12", 1.0, 0.5)
    e.onto(pic)
    # the lid (where the box does not hide it)
    e = Paper(SHAPE)
    bt, ft, fb, bb, a = lid_section()
    x0, x1 = LID["x0"], LID["x1"]
    e.line([P(x0, ft[1], ft[0]), P(x1, ft[1], ft[0])], rim, 1.0, 0.6)
    e.line([P(x0, bt[1], bt[0]), P(x1, bt[1], bt[0])], "#140c12", 1.0, 0.6)
    e.line([P(x0, ft[1], ft[0]), P(x0, fb[1], fb[0])], "#140c12", 1.0, 0.6)
    e.line([P(x0, ft[1], ft[0]), P(x0, bt[1], bt[0])], rim, 0.8, 0.4)
    m = info["sarc"]
    box = np.clip(m["front"] + m["rim"] + m["end"] + m["hole"], 0, 1)
    lc, la = e.done()
    over(pic, lc, la * (1 - box))
    return pic


def smoke(pic, seed):
    """A thread of smoke stands up from every flame in the still air."""
    rng = np.random.default_rng(seed)
    for l in LAMPS:
        x, y = l.at
        y -= 9
        h = 46 + rng.random() * 30
        pts = curve([(x, y), (x + rng.normal(0, 1.5), y - h * 0.3), (x + rng.normal(2, 3), y - h * 0.65), (x + rng.normal(4, 5), y - h)], 6)
        m = mask_line(SHAPE, pts, [lerp(0.8, 3.4, i / (len(pts) - 1)) for i in range(len(pts))], soft=1.3)
        fade = np.clip((y - Y_PIX) / h, 0, 1)
        over(pic, "#d8c0b8", (m * (1 - fade) ** 1.3 * 0.15).astype(F32))
    return pic


def reflections(pic, info, seed):
    """Gold throws the lamplight back. On the floor before each gilded piece there is a warm light; and the
    wall behind the heap is dappled with small yellow lights, each the picture of a flame thrown by some
    flat of gold: the one place where the cold stone is touched with the gold's own color."""
    rng = np.random.default_rng(seed)
    spots = [  # (outline in the picture, strength)
        ([(152, 250), (158, 244), (160, 372), (154, 380)], 0.20),          # the poles, on the wall beside them
        ([(140, 300), (146, 296), (147, 392), (142, 398)], 0.14),
        ([(214, 452), (300, 458), (296, 468), (210, 461)], 0.13),          # the carrying-chair, on the floor before it
        ([(256, 456), (346, 461), (340, 468), (258, 463)], 0.12),          # the bed's rail
        ([(378, 454), (428, 457), (422, 467), (374, 463)], 0.14),          # the armchair
    ]
    for i, (pts, amount) in enumerate(spots):
        m = mask_poly(SHAPE, pts, soft=2.2, wobble=2.5, seed=seed + i)
        glow(pic, "#ffc860", (m * amount).astype(F32))
    dapple = np.zeros(SHAPE, dtype=F32)
    swarms = [(262, 300, 5), (318, 262, 7), (352, 318, 5), (414, 300, 6), (292, 232, 3)]      # each flat of gold throws its own little swarm
    for (sx, sy, count) in swarms:
        lean = rng.uniform(-0.5, 0.5)
        for i in range(count):                                            # slanting lozenges, none alike
            x, y = sx + rng.normal(0, 17), sy + rng.normal(0, 13)
            w, h = rng.uniform(2.0, 6.5), rng.uniform(1.5, 4.2)
            quad = [(x - w + lean * h, y - h), (x + w + lean * h, y - h * rng.uniform(0.6, 1.2)), (x + w * rng.uniform(0.6, 1.1) - lean * h, y + h), (x - w - lean * h, y + h * rng.uniform(0.5, 1.0))]
            dapple = np.maximum(dapple, mask_poly(SHAPE, quad, soft=0.8) * rng.uniform(0.5, 1.0))
    for i in range(7):                                                    # and thin upright ones from the poles, on the left wall and in the corner
        x, y = rng.uniform(96, 148), rng.uniform(250, 380)
        dapple = np.maximum(dapple, mask_line(SHAPE, [(x, y), (x + rng.normal(0, 1.5), y + rng.uniform(10, 26))], rng.uniform(1.2, 2.4), soft=1.2) * rng.uniform(0.4, 0.9))
    wall = (BW_MASK + LW_MASK) * (1 - info["door"]["mask"]) * (1 - info["cover"])
    over(pic, "#f4c452", (dapple * wall * 0.30).astype(F32))
    glow(pic, "#ffd070", (dapple * wall * 0.16).astype(F32))
    return pic


def flames(pic):
    """The air just round each flame is bright (only just round it: the game draws the glow and flicker),
    and the floor round the brazier is red with its coals."""
    bx, by = P(th.BRAZIER[0], 0, th.BRAZIER[1])
    glow(pic, "#ff5a26", (mask_ellipse(SHAPE, bx + 2, by - 2, 34, 13, soft=6.0) * FLOOR_MASK * 0.2).astype(F32))
    for l in LAMPS:
        x, y = l.at
        glow(pic, "#ffb450", mask_ellipse(SHAPE, x, y - 2, 9, 10, soft=3.0) * 0.5)
        glow(pic, "#ff9440", mask_ellipse(SHAPE, x, y - 2, 18, 18, soft=7.0) * 0.11)
    return pic


def restate(pic, info):
    """The brush has gone over every edge. Say the built edges again: where wall meets floor and ceiling,
    the corners, the doorway, and the whole of the sarcophagus and its lid."""
    under = info["under"]
    near = np.exp(-np.abs(Y_PIX - FLOOR_LINE) / 2.2) + np.exp(-np.abs(Y_PIX - TOP_LINE) / 2.2)
    for cx in (LEFT, RIGHT):
        near += np.exp(-np.abs(X_PIX - cx) / 2.2) * (Y_PIX > TOP) * (Y_PIX < WALL)
    door = np.clip(blur(info["door"]["mask"], 1.5) * 1.6, 0, 1)
    m = np.clip(near * 0.75 + door * 0.85 + info["stonework"] * 0.5 + blur(info["sarc"]["hole"], 1.0) * 0.9, 0, 0.92)
    pic[...] = lerp(pic, under, m[..., None].astype(F32))
    return pic


def details(pic, info, seed=21):
    """Over the brushwork: say the built things again crisply, then the small things."""
    pen = info["pen"]
    tc, ta = info["things"]
    restate(pic, info)
    info["cover"] = np.clip(ta + info["stonework"] + info["sarc"]["hole"], 0, 1)
    joints(pic, info, seed + 60)
    grain_of_stone(pic, info, seed + 61, np.clip(ta + info["sarc"]["hole"], 0, 1))
    floor_marks(pic, info, seed + 62)
    cracks(pic, seed + 65)
    stone_edges(pic, info)
    reflections(pic, info, seed + 63)
    over(pic, tc, ta * 0.94)
    smoke(pic, seed + 64)
    flames(pic)
    pen.fine.onto(pic)
    return pic


def cut_out(pen, back, seed, fast=False, margin=8):
    """A cut-out from a pen's two sheets: brushed like the backdrop, its crisp lines put back, hard edges.
    -> (color picture, mask)."""
    bc, ba = pen.base.done()
    fc, fa = pen.fine.done()
    alpha = np.maximum(ba, (fa > 0.45) * fa)
    ys, xs = np.where(alpha > 0.05)
    y0, y1 = max(ys.min() - margin, 0), min(ys.max() + margin + 1, H)
    x0, x1 = max(xs.min() - margin, 0), min(xs.max() + margin + 1, W)
    flat = back.copy()
    over(flat, bc, ba)
    if not fast:
        part = strokes(flat[y0:y1, x0:x1].copy(), sizes=(4, 2), seed=seed, density=1.8, jitter=0.035, keep=0.5)
        flat[y0:y1, x0:x1] = part
        over(flat, bc, ba * 0.78)                              # say the thing again over its own brushwork: it is small, and must stay crisp
    over(flat, fc, fa)
    return flat, (alpha > 0.5).astype(F32)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.012, amount=0.016, accents=()):
    """Grain, then a limited palette with speckle. `accents` are parts of the picture whose colors must not
    be lost (the few bright lights), given extra weight when the palette is chosen."""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    parts = [sample_of.reshape(-1, 1, 3)]
    for (x, y, w, h, times) in accents:
        parts += [g[y:y + h, x:x + w].reshape(-1, 1, 3)] * times
    n = len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0))
    pal = palette_of(parts, colors=min(colors, max(2, n)))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def footprint(outline, pad=4.0):
    """An outline on the floor (room cm) as picture points, pushed out a little."""
    cx, cd = sum(a for a, _ in outline) / len(outline), sum(c for _, c in outline) / len(outline)
    out = []
    for a, c in outline:
        n = math.hypot(a - cx, c - cd) + 1e-6
        x, y = P(a + (a - cx) / n * pad, 0, c + (c - cd) / n * pad)
        out.append([int(round(x)), int(round(y))])
    return out


def layout(mirror_at):
    """The numbers the game needs, measured from the picture as painted."""
    (xf, yft, yfb), (xn, ynt, ynb) = door_corners()
    b = th.BENCH
    bx, bd = th.BRAZIER
    s = SARC
    base_row = int(round(row_of(b["d1"])))
    hx, hy = P(HUM[0], 0, HUM[1])
    ring = [round(58 * k_of(HUM[1]), 1), round(58 * k_of(HUM[1]) * (row_of(HUM[1]) - G.vy) / G.F, 1)]
    mx, my, mrx, mry = mirror_at
    pts = lambda *q: [[int(round(a)), int(round(c))] for a, c in q]
    lay = {
        "id": "egypt-chamber", "horizon": HZ, "full": FULL,
        "light": "six oil lamps (see lamps): warm pools on the lower walls and floor, the ceiling and corners in cool dark; no daylight",
        "walk": [[86, 470], [120, 461], [160, 467], [456, 467], [465, 440], [546, 440], [550, 509], [752, 509], [757, 529], [792, 529], [792, 594], [150, 594], [72, 584], [72, 498]],
        "blocked": [footprint([(b["x0"] - 72, b["d1"] + 12), (b["x1"] + 76, b["d1"]), (b["x1"] + 76, b["d0"] + 10), (b["x1"], b["d0"]), (b["x0"], b["d0"]), (b["x0"] - 72, b["d0"] + 28)], 5.0)],
        "planes": [{"id": "bench", "file": "bench.png", "base": base_row},
                   {"id": "mirror", "file": "mirror.png", "base": base_row + 1},
                   {"id": "front", "file": "front.png", "plane": "front"}],
        "things": [
            {"id": "treasure", "what": "the king's things along the back wall: canopy poles, rolled mats, alabaster jars, carrying-chair, bed with linen, chests, bracelet box, armchair, copper basins, baskets", "shape": {"rect": [138, 186, 322, 282]}, "stand": [392, 478], "face": "N"},
            {"id": "bench", "what": "the goldsmith's bench: lamp, half-gilded casket, dish of gold leaf, blowpipe, burnisher, hammers, beating stone; his water jug and his dinner on the floor at its left end", "shape": {"rect": [192, 426, 162, 96]}, "stand": [300, 528], "face": "N"},
            {"id": "mirror", "what": "the goldsmith's copper hand mirror, propped against a jar on the bench (cut-out mirror.png)", "shape": {"rect": [int(mx - mrx - 3), int(my - mry - 3), int(2 * mrx + 6), int(2 * mry + 20)]}, "stand": [304, 528], "face": "N"},
            {"id": "hum", "what": "the place that hums: bare wall and air; the dust on the floor before it is swept into a ring", "shape": {"rect": [462, 236, 80, 164]}, "stand": [int(round(hx)), int(round(hy))], "face": "N"},
            {"id": "sarcophagus", "what": "the granite sarcophagus, lidless; a dish lamp and a mallet on its rim", "shape": {"poly": pts(P(s["x0"], 0, s["d1"]), P(s["x1"], 0, s["d1"]), P(s["x1"], s["h"], s["d1"]), P(s["x1"], s["h"], s["d0"]), P(s["x0"], s["h"], s["d0"]), P(s["x0"], s["h"], s["d1"]))}, "stand": [650, 532], "face": "N"},
            {"id": "lid", "what": "the sarcophagus's lid, leaning on the back wall behind it, still roped", "shape": {"rect": [588, 328, 164, 56]}, "stand": [700, 532], "face": "N"},
            {"id": "brazier", "what": "the goldsmith's charcoal brazier, and his basket of charcoal", "shape": {"rect": [356, 478, 54, 38]}, "stand": [434, 524], "face": "W"},
        ],
        "exits": [{"to": "egypt-gallery", "shape": {"poly": pts((xf, yft), (xf, yfb), (xn, ynb), (xn, ynt))}, "stand": [106, 468], "face": "W"}],
        "marks": {"goldsmith": [330, 494], "dad": [150, 484], "talk": [434, 524]},
        "lamps": [{"id": l.name, "flame": [int(round(l.at[0])), int(round(l.at[1] - 3))], "on": {"C": "bench.png", "E": "front.png"}.get(l.name, "back.png")} for l in LAMPS],
        "hum": {"wall": [500, 300], "floor": [int(round(hx)), int(round(hy))], "ring": ring},
        "beam": [[int(round((xf + xn) / 2)), int(round((yft + ynb) / 2 - 8))], [500, 300]],
        "sarcophagus": {"rect": [554, 383, 193, 118]},
        "notes": "The goldsmith sits BEHIND the bench (feet above its baseline). mirror.png lies exactly over bench.png; without it the jar it leaned on is whole. The beam's line from the doorway to the hum passes in front of everything painted along the back wall.",
    }
    return lay


def write_layout(lay, name):
    """layout.json, one thing to a line, so that a person can read it."""
    lines = []
    for key, value in lay.items():
        if isinstance(value, list) and value and isinstance(value[0], (dict, list)) and key not in ("walk", "beam"):
            inner = ",\n".join("    " + json.dumps(v) for v in value)
            lines.append(f'  {json.dumps(key)}: [\n{inner}\n  ]')
        else:
            lines.append(f"  {json.dumps(key)}: {json.dumps(value)}")
    with open(name, "w") as f:
        f.write("{\n" + ",\n".join(lines) + "\n}\n")


def save_rgb(a, name):
    Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)).save(name)


def crop(args):
    x, y, w, h = [int(v) for v in args[:4]]
    times = int(args[4]) if len(args) > 4 else 2
    src = args[5] if len(args) > 5 else f"{WORK}/all.png"
    im = Image.open(src).convert("RGB").crop((x, y, x + w, y + h)).resize((w * times, h * times), Image.NEAREST)
    name = f"{WORK}/crop-{x}-{y}.png"
    im.save(name)
    print(name, im.size)


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "crop":
        crop(sys.argv[2:])
        sys.exit()
    fast = len(sys.argv) > 1 and sys.argv[1] == "fast"
    base, info = under()
    save_rgb(base, f"{WORK}/1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else brushwork(base, room_flow(), sizes=(13, 7, 3), seed=4, density=1.5, jitter=0.07, keep=0.18)
    info["under"] = base
    details(pic, info)
    mp = mirror_sheet()
    mirror_at = th.mirror(th.Pen(LAMPS, AMB))
    bench_c, bench_a = cut_out(bench_sheet(), pic, 5, fast)
    mirror_c, mirror_a = cut_out(mp, bench_c * bench_a[..., None] + pic * (1 - bench_a[..., None]), 6, True)
    front_c, front_a = cut_out(front_sheet(), pic, 7, fast)
    whole = pic.copy()
    for c, a in ((bench_c, bench_a), (mirror_c, mirror_a), (front_c, front_a)):
        over(whole, c, a)
    save_rgb(whole, f"{WORK}/all.png")
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    gold = [(130, 220, 330, 250, 2), (240, 430, 160, 90, 3)]
    print("back", finish(pic, f"{OUT}/back.png", 160, accents=gold))
    print("bench", finish(bench_c, f"{OUT}/bench.png", 72, bench_a))
    print("mirror", finish(mirror_c, f"{OUT}/mirror.png", 32, mirror_a))
    print("front", finish(front_c, f"{OUT}/front.png", 56, front_a))
    write_layout(layout(mirror_at), f"{OUT}/layout.json")
    comp = Image.open(f"{OUT}/back.png").convert("RGBA")              # everything laid together, to look at (as comp.py does)
    for name in ("bench", "mirror", "front"):
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(f"{OUT}-comp.png")
    print("done", round(time.time() - t0, 1))

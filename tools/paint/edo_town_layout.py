"""Himeji town's layout.json: every number the scene file needs, measured from the picture as painted (edo_town.py's
plan through the camera, and the painted layers themselves for the shapes that hug things). PAINT-21E.

  python3 edo_town_layout.py      writes out/edo-town/layout.json (edo_town.py also calls write())"""

import json
import os

import numpy as np

from edo_town_kit import *
import edo_town as ET

r = lambda q: [int(round(q[0])), int(round(q[1]))]


def foot(X, D):
    return r(P(X, 0, D))


def school_pt(X, D):
    """A point on the school's raised floor (45 cm up)."""
    return r(P(X, ET.SCH_FLOOR, D))


DK = ET.DESK_D + 55                    # where a girl kneels behind her desk
MARKS = {
    "east": [772, 556],                          # from the highway, the right edge: arriving (from Akashi, the walk card)
    "house": foot(205, ET.DF - 120),             # before O-Tane's door, in the street
    "tane": [534, 457],                          # O-Tane at her door (on the gutter's bridging stone)
    "well": [466, 450],                          # in the side yard's mouth, before the well (Mom draws water)
    "kitchen": foot(-92, ET.YARD_BACK - 70),     # at the kitchen door, at the yard's back (the rice pot, the salt, the shelf)
    "school": foot(-300, ET.DF - 120),           # before the writing school's open front
    "kiku": [349, 457],                          # O-Kiku outside it, by the step stone, not going in
    "desk": school_pt(ET.DESKS[2] + ET.DESK_W / 2, DK),      # inside, behind the free third desk: Little Sister sits in
    "kikuDesk": school_pt(ET.DESKS[3] + ET.DESK_W / 2, DK),  # inside, behind the fourth: O-Kiku, once she goes in
    "shizu": school_pt(-176, ET.DF + 250),       # O-Shizu kneeling at the right end of the room, by her table and the books
    "pupil1": school_pt(ET.DESKS[0] + ET.DESK_W / 2, DK),
    "pupil2": school_pt(ET.DESKS[1] + ET.DESK_W / 2, DK),
    "gate": [757, 466],                          # before the ward gate, in the street
    "north": [757, 451],                         # in the gate's mouth: the lane north, toward the castle (refuses today)
    "tobei": foot(492, ET.DF - 92),              # old Tobei on his stool before his hut
    "hut": foot(462, ET.DF - 120),               # before the hut's counter (the sandals, the sweets, the clappers)
    "cotton": foot(-760, ET.DF - 96),            # before the cotton office (its doorway, the bales)
    "note": foot(-560, ET.DF - 96),              # before the paper-note office
    "keep": [560, 520],                          # where one stands in the street to look up at the keep
}
FACES = {"east": "W", "house": "N", "tane": "S", "well": "N", "kitchen": "N", "school": "N", "kiku": "S", "desk": "S",
         "kikuDesk": "S", "shizu": "W", "pupil1": "S", "pupil2": "S", "gate": "N", "north": "N", "tobei": "S", "hut": "N",
         "cotton": "N", "note": "N", "keep": "N"}
SCHOOL_MARKS = {"desk", "kikuDesk", "shizu", "pupil1", "pupil2"}


def walk_outline():
    """The ground people stand on: the highway, up to the gutter along the fronts; the side yard back to the kitchen;
    the mouth of the ward gate. Never inside a house, never behind the hut or the bales."""
    yard_r_front = foot(128, ET.DF - 30)
    yard_r_back = foot(128, ET.YARD_BACK - 44)
    yard_l_back = foot(-128, ET.YARD_BACK - 44)
    yard_l_front = foot(-128, ET.DF - 30)
    g0, g1 = foot(ET.GATE[0] + 16, ET.GATE_D - 4), foot(ET.GATE[1] - 16, ET.GATE_D - 4)
    top = 455
    return [[6, 597], [794, 597], [794, top], [796, top], [796, g1[1] - 4], [g0[0] + 2, g0[1] - 4], [g0[0] + 2, top],
            [yard_r_front[0], top], yard_r_back, yard_l_back, [yard_l_front[0], top], [6, top]]


def school_floor():
    """The raised floor of the school's room, seen through its open front: the girls kneel on it (a floor of its own,
    at its own size)."""
    r0, r1 = ET.ROOM
    return [school_pt(r0 + 14, ET.DF + 60), school_pt(r1 - 14, ET.DF + 60), school_pt(r1 - 14, ET.DF + 300), school_pt(r0 + 14, ET.DF + 300)]


def footprint(X, D, rx, rd, n=10):
    import math
    return [foot(X + rx * math.cos(2 * math.pi * i / n), D + rd * math.sin(2 * math.pi * i / n)) for i in range(n)]


def write(path):
    cuts = ET.cut_layers()
    alpha = {k: v.a > 0.5 for k, v in cuts.items()}
    out = {"id": "edo-town", "horizon": HZ, "full": FULL, "minScale": 0.3,
           "light": "midday, 29 April 1830: the sun high in the south, behind us and a little to the left (about 68 degrees up). The fronts face us "
                    "and are in full light; each deep eave lays a hard band of shade across the top of its front; shadows on the ground are short and "
                    "fall away from us, a little to the right (0.36 of a thing's height away, 0.10 across). Key: edo-castle (PAINT-20D's).",
           "note": "The land camera (persp.Camera 290/590, focal 800, lens 3.28 m up), its vanishing point at x 444.5 (the middle of O-Tane's side "
                   "yard, which is seen straight down). The far side's fronts stand on row 450 (16.4 m off: a grown-up 85 px at their feet, Mom 80, "
                   "Little Sister 58); the street runs from there to the bottom edge (8.5 m off at row 600). Looking north: east is the right edge, "
                   "the castle is ahead, above the roofs."}
    out["view"] = {"horizon": HZ, "full": FULL, "focal": FOC, "vanish_x": VX, "eye_cm": round(EYE, 1), "fronts_row": 450, "fronts_cm": round(ET.DF, 1)}
    out["walk"] = walk_outline()
    out["walk_note"] = ("the street floor: the highway up to the gutter along the fronts (row 455), a pocket into the side yard back to the kitchen "
                        "door (row 428), and the ward gate's mouth (to row 448). The school's room is a floor of its own (floors.school).")
    out["floors"] = [
        {"name": "street", "area": out["walk"], "note": "the usual floor"},
        {"name": "school", "area": school_floor(), "scale": round(k_at(ET.DF + 175) / S0, 3), "away": None,
         "note": "the school's raised room (45 cm up), seen through the open front: a floor of its own at its own size (0.482: a girl "
                 "kneeling behind a desk), its people sorted by their feet (no base), so that the desks (base 419) are in front of the girls "
                 "behind them and the school's front (base 450) in front of everybody inside. Little Sister and O-Kiku go up from the step "
                 "stone at the right end (marks kiku -> desk / kikuDesk: g.climbTo with a path [[372, 452], [366, 432]])."},
    ]
    # blocked: the well's curb, the pickle tub, the rice pot's stand, the mortar, the pan, the bales, the hut's stool
    W_ = ET.WELL
    blocked = [footprint(W_["X"], W_["D"], W_["r"] + 8, W_["r"] + 8),
               footprint(ET.THINGS["pickletub"]["X"], ET.THINGS["pickletub"]["D"], 28, 26, 8),
               footprint(ET.THINGS["ricepot"]["X"], ET.THINGS["ricepot"]["D"], 28, 24, 8),
               footprint(ET.THINGS["mortar"]["X"], ET.THINGS["mortar"]["D"], 24, 22, 8),
               footprint(ET.THINGS["pan"]["X"], ET.THINGS["pan"]["D"], 26, 12, 8)]
    for (X, row, n) in ET.BALES:
        d = ET.DF - 30 - row * 46
        blocked.append([foot(X - 4, d - 4), foot(X + 58, d - 4), foot(X + 58, d + 44), foot(X - 4, d + 44)])
    out["blocked"] = blocked
    out["blocked_note"] = "the well's curb, the pickle tub, the rice pot on its stand, the mortar, the pan against the wall, the bales of cloth"
    # ---- the cut-outs, back to front, as the scene lists them
    base_desks = int(round(P(0, ET.SCH_FLOOR, ET.DESK_D)[1]))
    base_front = int(round(row_D(ET.DF)))
    base_back = int(round(row_D(ET.YARD_BACK)))
    planes = [
        {"id": "noren-cotton", "file": "noren-cotton.png", "plane": "back", "what": "the cotton office's long indigo noren across its doorway (it stirs: fx sway)"},
        {"id": "noren", "file": "noren.png", "plane": "back", "what": "O-Tane's indigo noren in her doorway (it stirs: fx sway)"},
        {"id": "desks", "file": "desks.png", "base": base_desks, "what": "the row of four low desks inside the school: the girls (pupil1, pupil2) kneel "
                                                                       "behind the first two, the third is free (Little Sister's: desk), the fourth too (O-Kiku's: kikuDesk)"},
        {"id": "shutters", "file": "shutters.png", "base": base_front, "what": "the writing school's front: the corner posts, the sill, the upper shutters hooked up "
                                                                             "under the eave, the lower ones stacked at the left post, the step stone; its opening clear "
                                                                             "(the room and everybody in it are behind it)",
         "states": {"open": "shutters.png", "shut": "shutters-shut.png"}},
        {"id": "kitchendoor", "file": "kitchendoor.png", "base": base_back, "what": "the kitchen door in the lean-to at the yard's back",
         "states": {"shut": "kitchendoor.png", "open": "kitchendoor-open.png"}},
        {"id": "saltjar", "file": "saltjar.png", "base": base_back + 1, "what": "the salt jar on the shelf (Bizen ware, a wooden lid)"},
        {"id": "plumjar", "file": "plumjar.png", "base": base_back + 1, "what": "the plum jar on the shelf, its mouth papered and tied"},
        {"id": "cloth", "file": "cloth.png", "base": base_back + 1, "what": "a cloth on the shelf: folded; then a bundle of rice balls",
         "states": {"folded": "cloth.png", "bundle": "cloth-bundle.png"}},
        {"id": "ricepot", "file": "ricepot.png", "base": int(round(row_D(ET.THINGS["ricepot"]["D"] - 22))), "what": "the rice pot on its stand under the shelf (cooked), the paddle across the lid",
         "solid": footprint(ET.THINGS["ricepot"]["X"], ET.THINGS["ricepot"]["D"], 26, 22, 8)},
        {"id": "pickletub", "file": "pickletub.png", "base": int(round(row_D(ET.THINGS["pickletub"]["D"] - 24))), "what": "the pickle tub (pickled radish), its drop-lid and pressing stone",
         "solid": footprint(ET.THINGS["pickletub"]["X"], ET.THINGS["pickletub"]["D"], 26, 24, 8)},
        {"id": "well", "file": "well.png", "base": int(round(row_D(W_["D"] - W_["r"]))), "what": "the stone-lined well and its pulley frame: Mom stands before it (mark well), "
                                                                                               "and goes past its left to the kitchen door",
         "solid": footprint(W_["X"], W_["D"], W_["r"] + 6, W_["r"] + 6)},
        {"id": "bucket", "file": "bucket.png", "base": int(round(row_D(W_["D"] - W_["r"]))) + 1, "what": "the bucket on its rope, up (hanging under the pulley)",
         "states": {"up": "bucket.png", "down": "bucket-down.png"}},
        {"id": "gate", "file": "gate.png", "base": int(round(row_D(ET.GATE_D))), "what": "the ward gate across the lane north: two posts, a tie-beam, a little gabled roof, the "
                                                                                      "doors open by day (shut: gate-shut, for the night). Whoever walks into its mouth "
                                                                                      "(mark north, row 451) is behind it.",
         "states": {"open": "gate.png", "shut": "gate-shut.png"},
         "solid": [[foot(ET.GATE[0], ET.GATE_D)[0] - 2, 455], [foot(ET.GATE[0] + 14, ET.GATE_D)[0] + 2, 455], [foot(ET.GATE[0] + 14, ET.GATE_D)[0] + 2, 450], [foot(ET.GATE[0], ET.GATE_D)[0] - 2, 450]]},
    ]
    out["planes"] = planes
    out["cutouts"] = {k: list(box_of(alpha[k])) for k in ET.CUTS + ET.ALTS}
    # ---- the things to click (every one of ROUND-21.md's list for edo-town, and a few more)
    things = []

    def thing(id_, what, shape, stand, face="N", **more):
        d = {"id": id_, "what": what, "shape": {"poly": shape}, "stand": stand, "face": face}
        d.update(more)
        things.append(d)
    M = MARKS
    kx, ky = ET.KEEP_AT
    thing("keep", "the keep, white, roof on roof, far up on its hill above the town's roofs (PAINT-20D's keep, from the town side)",
          [[kx - 44, ky + 4], [kx + 44, ky + 4], [kx + 30, ky - 40], [kx + 14, ky - 110], [kx - 14, ky - 110], [kx - 30, ky - 40]], M["keep"])
    thing("roofs", "the town's tiled roofs, row behind row up to the castle's hill", [[236, 214], [800, 206], [800, 252], [236, 252]], M["keep"])
    co = [foot(-1400, ET.DF), foot(ET.COTTON[1], ET.DF), r(P(ET.COTTON[1], 760, ET.DF + 230)), r(P(-1400, 760, ET.DF + 230))]
    thing("cottonoffice", "the domain's cotton office: a big two-storey front, white above, its wide doorway, an indigo noren, bales of white cloth going in",
          [[0, 452], [co[1][0], 452], [co[1][0], 104], [0, 104]], M["cotton"])
    thing("noteoffice", "the domain's paper-note office beside it: a sober front, a latticed door, a small hanging board",
          [[co[1][0], 452], [foot(ET.NOTE[1], ET.DF)[0], 452], [foot(ET.NOTE[1], ET.DF)[0], 104], [co[1][0], 104]], M["note"])
    bales_m = np.zeros(SHAPE, bool)
    for (X, row, n) in ET.BALES:
        d = ET.DF - 30 - row * 46
        a_, b_ = P(X, 0, d), P(X + 54, n * 30, d)
        bales_m[int(b_[1]) - 4:int(a_[1]) + 2, max(0, int(a_[0])):int(b_[0]) + 1] = True
    thing("bales", "bales of white cotton cloth in straw wrappers, stacked at the cotton office's front, going in", hull(bales_m, 2, 10), M["cotton"])
    th0, th1 = foot(ET.TANE[0], ET.DF), foot(ET.TANE[1], ET.DF)
    thing("house", "O-Tane's house: a weaver's house, a fine lattice over the front room's window, her doorway with its indigo noren, the bench under the lattice",
          [[th0[0], 452], [th1[0], 452], [th1[0], 336], [th0[0], 336]], M["house"])
    y0, y1 = foot(ET.YARD[0], ET.DF), foot(ET.YARD[1], ET.DF)
    thing("passage", "O-Tane's side yard, open to the street: packed earth back to the kitchen lean-to, the well, the jars (the way to the back)",
          [[y0[0], 452], [y1[0], 452], r(P(ET.YARD[1], 0, ET.YARD_BACK)), r(P(ET.YARD[1], 230, ET.YARD_BACK)), r(P(ET.YARD[0], 230, ET.YARD_BACK)), r(P(ET.YARD[0], 0, ET.YARD_BACK))], M["well"])
    thing("well", "the stone-lined well, the pulley frame over it", hull(alpha["well"], 2, 14), M["well"])
    thing("bucket", "the bucket on its rope (up / down)", hull(alpha["bucket"] | alpha["bucket-down"], 3, 10), M["well"])
    thing("kitchendoor", "the kitchen door in the lean-to at the yard's back", hull(alpha["kitchendoor"], 2, 8), M["kitchen"])
    thing("ricepot", "the rice pot on its stand, cooked rice in it, the paddle across the lid", hull(alpha["ricepot"], 3, 10), M["kitchen"])
    thing("saltjar", "the salt jar on the shelf", hull(alpha["saltjar"], 3, 10), M["kitchen"])
    thing("pickletub", "the pickle tub of pickled radish, its stone on the lid", hull(alpha["pickletub"], 3, 10), M["kitchen"])
    thing("plumjar", "the jar of pickled plums on the shelf", hull(alpha["plumjar"], 3, 10), M["kitchen"])
    thing("cloth", "a cotton cloth on the shelf (folded; then knotted round the rice balls)", hull(alpha["cloth"] | alpha["cloth-bundle"], 3, 10), M["kitchen"])
    pn = ET.THINGS["pan"]
    pc = P(pn["X"], pn["w"] / 2, pn["D"])
    pr = pn["w"] / 2 * k_at(pn["D"]) + 3
    thing("pan", "the roasting pan (horoku), stood on its rim against the wall to dry", [[int(pc[0] - pr), int(pc[1] - pr - 4)], [int(pc[0] + pr + 4), int(pc[1] - pr - 4)],
                                                                                         [int(pc[0] + pr + 4), int(pc[1] + pr)], [int(pc[0] - pr), int(pc[1] + pr)]], M["well"])
    mo = ET.THINGS["mortar"]
    m0, m1 = P(mo["X"] - mo["w"] / 2 - 4, mo["h"] + 8, mo["D"]), P(mo["X"] + mo["w"] / 2 + 4, -2, mo["D"])
    thing("mortar", "the Bizen mortar, reddish-brown, combed inside, on the ground by the well", [[int(m0[0]), int(m0[1])], [int(m1[0]), int(m0[1])], [int(m1[0]), int(m1[1])], [int(m0[0]), int(m1[1])]], M["well"])
    s0, s1 = foot(ET.SCHOOL[0], ET.DF), foot(ET.SCHOOL[1], ET.DF)
    thing("school", "the writing school: its shutters propped open, the raised room, the low desks, the girls and their teacher",
          [[s0[0], 452], [s1[0], 452], [s1[0], 336], [s0[0], 336]], M["school"])
    thing("desks", "four low desks: two with practice books open, inkstones, brushes; two free", hull(alpha["desks"], 3, 12), M["school"])
    thing("gate", "the ward gate across the lane north, its doors open by day; the lane goes north toward the castle", hull(alpha["gate"], 2, 12), M["gate"])
    h0, h1 = foot(ET.HUT[0], ET.DF - 30), foot(ET.HUT[1], ET.DF - 30)
    thing("hut", "Tobei's hut by the gate: a little board hut, its shutter propped over a counter", [[h0[0], 454], [h1[0], 454], [h1[0], 335], [h0[0], 335]], M["hut"])
    ca = P(ET.HUT[0] + 16, 160, ET.DF - 76)
    cb = P(ET.HUT[1] - 18, 145, ET.DF - 76)
    thing("hutsandals", "straw sandals hung in pairs from the hut's shutter, for sale", [[int(ca[0]) - 2, int(ca[1]) - 4], [int(cb[0]) + 2, int(ca[1]) - 4], [int(cb[0]) + 2, int(cb[1]) + 22], [int(ca[0]) - 2, int(cb[1]) + 22]], M["hut"])
    jx = P(ET.HUT[0] + 38, 90, ET.DF - 42)
    thing("sweets", "a jar of cheap sweets on the hut's counter", [[int(jx[0]) - 9, int(jx[1]) - 12], [int(jx[0]) + 9, int(jx[1]) - 12], [int(jx[0]) + 9, int(jx[1]) + 6], [int(jx[0]) - 9, int(jx[1]) + 6]], M["hut"])
    cx = P(ET.HUT[0] + 6, 120, ET.DF - 32)
    thing("clappers", "the night man's wooden clappers on a peg on the hut's post", [[int(cx[0]) - 4, int(cx[1]) - 3], [int(cx[0]) + 9, int(cx[1]) - 3], [int(cx[0]) + 9, int(cx[1]) + 26], [int(cx[0]) - 4, int(cx[1]) + 26]], M["hut"])
    thing("highway", "the Saigoku-kaido, the highway through Watamachi: broad packed earth; east the way they came", [[0, 458], [800, 458], [800, 598], [0, 598]], M["east"], "E")
    thing("lane", "the lane north through the gate, toward the castle", [[722, 448], [796, 448], [796, 330], [722, 330]], M["north"])
    thing("storehouse", "a white storehouse behind the lot, over the kitchen's roof", [[r(P(ET.KURA["x"][0], 0, ET.KURA["D"]))[0], 340], [r(P(ET.KURA["x"][1], 0, ET.KURA["D"]))[0], 340],
                                                                                 [r(P(ET.KURA["x"][1], 0, ET.KURA["D"]))[0], 300], [r(P(ET.KURA["x"][0], 0, ET.KURA["D"]))[0], 300]], M["well"])
    # the people (PEOPLE-21B draws them at these marks): the area each one is
    def person(id_, mark, cm, floor="street", what=""):
        x, y = MARKS[mark]
        sc = (y - HZ) / (FULL - HZ) if floor == "street" else k_at(ET.DF + 175) / S0
        h = cm / 181.0 * 160 * sc
        w = max(12, h * 0.36)
        thing(id_, what, [[int(x - w / 2), int(y + 2)], [int(x + w / 2), int(y + 2)], [int(x + w / 2), int(y - h)], [int(x - w / 2), int(y - h)]], MARKS[mark], "N", person=True, mark=mark, floor=floor)
    person("tane", "tane", 146, what="O-Tane, a cotton weaver's wife, at her door")
    person("kiku", "kiku", 115, what="O-Kiku, seven, in her best, outside the school, not going in")
    person("shizu", "shizu", 90, "school", "O-Shizu, the teacher, kneeling at the right end of the room")
    person("pupil1", "pupil1", 80, "school", "a girl at her desk, kneeling")
    person("pupil2", "pupil2", 80, "school", "a girl at her desk, kneeling")
    person("tobei", "tobei", 120, what="old Tobei, the night man of the ward, on his stool by his hut")
    out["things"] = things
    # ---- the marks and the stands
    out["marks"] = dict(MARKS)
    out["faces"] = FACES
    stands = {}
    for k, v in MARKS.items():
        if k in SCHOOL_MARKS:
            sc = k_at(ET.DF + 175) / S0
            stands[k] = {"at": v, "grownup_px": int(round(160 * sc)), "scale": round(sc, 3), "floor": "school",
                         "note": "kneeling on the raised floor (45 cm): the scale of the floor, not of the row"}
        else:
            stands[k] = {"at": v, "grownup_px": int(round(160 * scale_at(v[1]))), "floor": "street"}
    out["stands"] = stands
    out["sizes"] = {"grownup_px_at_fronts": round(160 * scale_at(457), 1), "mom_px_at_house": round(168 / 181 * 160 * scale_at(MARKS["house"][1]), 1),
                    "mom_px_at_well": round(168 / 181 * 160 * scale_at(MARKS["well"][1]), 1), "mom_px_at_kitchen": round(168 / 181 * 160 * scale_at(MARKS["kitchen"][1]), 1),
                    "lilsis_px_at_kiku": round(122 / 181 * 160 * scale_at(MARKS["kiku"][1]), 1), "kiku_115cm_px": round(115 / 181 * 160 * scale_at(MARKS["kiku"][1]), 1),
                    "man_156cm_px_at_tobei": round(156 / 181 * 160 * scale_at(MARKS["tobei"][1]), 1), "school_floor_scale": round(k_at(ET.DF + 175) / S0, 3),
                    "px_per_cm_at_fronts": round(k_at(ET.DF), 4), "px_per_cm_at_kitchen": round(k_at(ET.YARD_BACK), 4)}
    out["exits"] = [
        {"id": "east", "to": None, "name": "the highway east", "edge": "right", "walkTo": MARKS["east"], "band": [[786, 458], [800, 458], [800, 598], [786, 598]],
         "note": "the way they came: refuses (design: 'the highway east (refuses)')"},
        {"id": "north", "to": "edo-castle", "spawn": "enter", "name": "the lane north, toward the castle", "walkTo": MARKS["gate"], "via": MARKS["north"],
         "band": [[722, 448], [796, 448], [796, 458], [722, 458]], "note": "the next day only (Mom: 'Tomorrow. Tonight we go and listen.')"},
    ]
    # ---- the moving things
    sm = P(-22, 196, ET.YARD_BACK)
    out["fx"] = [
        {"id": "kitchen-smoke", "type": "smoke", "what": "smoke from the kitchen's smoke-hole under the lean-to's eave ('Don't let the fire out')",
         "at": [int(round(sm[0])), int(round(sm[1]))], "base": base_back, "height": 90, "width": [3, 16], "lean": [14, -90], "rise": 12, "rate": 2,
         "color": "#e4e6ea", "opacity": 0.28, "behind": [[[236, 0], [380, 0], [380, 330], [236, 330]], [[509, 0], [660, 0], [660, 330], [509, 330]]], "behindOpacity": 0.0,
         "note": "it rises from under the lean-to's eave and drifts up between the two houses, a little to the right (the noon air nearly still); hidden behind the "
                 "houses' upper storeys on either side"},
        {"id": "noren", "type": "sway", "plane": "noren", "anchor": "top", "amount": 1.2, "period": 3.8},
        {"id": "noren-cotton", "type": "sway", "plane": "noren-cotton", "anchor": "top", "amount": 1.0, "period": 4.2},
        {"id": "kite", "type": "birds", "what": "a kite (the bird) wheeling slowly over the castle's hill", "circle": {"at": [600, 110], "r": [70, 24]}, "count": 1,
         "speed": 12, "size": 7, "plane": "back"},
        {"id": "sparrows", "type": "birds", "what": "a few sparrows on the street, pecking; they go up when someone comes near", "area": [[120, 500], [420, 494], [440, 560], [100, 566]],
         "count": 4, "look": "sparrow", "size": 14, "depth": True, "shy": 120},
    ]
    out["fx_note"] = ("Moving: the kitchen's smoke, the two noren stirring, a kite over the castle, sparrows on the street; and the people's own small lives "
                      "(PEOPLE-21B): O-Tane at her door, O-Kiku fidgeting, the girls writing, O-Shizu at her table, Tobei on his stool. The komuso passes "
                      "along the street now and then (the design: he is in Himeji too): left to right along row 520 or so.")
    out["school_note"] = ("The school's front is the cut-out `shutters` (base 450), its opening clear: the room is painted in the backdrop behind it, and the "
                          "girls, the teacher, Little Sister and O-Kiku are the game's people on the floor `school` (scale 0.482), sorted by their feet: "
                          "the `desks` cut-out (base 419) is in front of a girl kneeling behind it (her knees on row 415).")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    return out


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    o = write(f"{OUT}/layout.json")
    print(json.dumps(o["marks"]))
    print(json.dumps(o["sizes"]))

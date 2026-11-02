"""The foot of Mount Shosha's layout.json: every number the scene file needs, measured from the picture as painted
(edo_shosha.py's plan through the camera, and the painted layers for the shapes that hug things). PAINT-21E.

  python3 edo_shosha_layout.py      writes out/edo-shosha/layout.json (edo_shosha.py also calls write())"""

import json
import math
import os

import numpy as np

from edo_shosha_kit import *
from edo_town_kit import hull, box_of
import edo_shosha as ES

r = lambda q: [int(round(q[0])), int(round(q[1]))]


def foot(X, D):
    return r(P(X, 0, D))


def hfoot(a, b):
    X, D = H_(a, b)
    return foot(X, D)


MARKS = {
    "road": [735, 548],                          # from the town: arriving, on the road up at the bottom right
    "stone": foot(ES.STONE[0], 1330),            # before the stone at the path's foot
    "path": [214, 468],                          # the foot of the east path (the way up refuses, for every one of them)
    "ryokai": [236, 456],                        # Ryokai, sitting on the bottom step by the stone
    "hall": hfoot(180, -150),                    # before the doors, a step back
    "lock": hfoot(180, -118),                    # at the lock, close before the step: the close-up opens from here
    "step": hfoot(236, -122),                    # by the step and O-Ume's rice ball on its leaf
    "ume": hfoot(400, -60),                      # O-Ume, by the hall's front corner, between the hall and the bench
    "hut": [62, 466],                            # before O-Ume's hut (its lantern on the hook)
    "bench": foot(360, 1190),                    # before the bench where the women wait
    "tome": foot(330, 1295),                     # Grandmother Tome, seated on the bench
    "wife": foot(400, 1295),                     # the young wife with her baby, seated
    "girl": foot(470, 1295),                     # the girl of eleven with her grandmother's slip, seated
    "view": [690, 455],                          # at the terrace's edge: the plain far below, the castle
    "combs": foot(ES.COMBS[0] - 40, ES.COMBS[1] - 70),   # before the heap of failed combs and pins
}
FACES = {"road": "W", "stone": "N", "path": "N", "ryokai": "E", "hall": "N", "lock": "N", "step": "N", "ume": "W", "hut": "N",
         "bench": "N", "tome": "S", "wife": "S", "girl": "S", "view": "E", "combs": "N"}


def walk_outline():
    """The terrace: from the bottom up to the hall's step and base, round the stone to the path's foot, along the hut's
    front; at the right up toward the shrubs on the edge. Never on the hall's base, never up the path, never over the
    edge."""
    base_fl = hfoot(-30, -30)
    base_fr = hfoot(390, -30)
    step_l = hfoot(66, -100)
    step_r = hfoot(294, -100)
    return [[6, 598], [794, 598], [794, 452], [700, 436], [600, 446], [base_fr[0] + 2, base_fr[1] + 3], [step_r[0] + 2, step_r[1] + 2],
            [step_l[0] - 2, step_l[1] + 2], [base_fl[0] - 2, base_fl[1] + 2], [318, 450], [262, 450], [256, 452], [196, 452], [180, 458],
            [40, 460], [6, 464]]


def write(path):
    ES.set_light("gold")
    cuts = ES.cut_layers()
    alpha = {k: v.a > 0.5 for k, v in cuts.items()}
    out = {"id": "edo-shosha", "horizon": HZ, "full": FULL, "minScale": 0.3,
           "light": "two states, the same geometry. GOLD (back.png and the plain cut-outs): the late afternoon sun from the left and a little behind us, "
                    "about 30 degrees up: the hall's west side lit, its front at a slant, shadows to the right and a little away. SUNSET (sunset.png and "
                    "every cut-out's -sunset twin): the sun low at the left, seen red through the trees of the glade (7 degrees up, a little beyond the "
                    "hall): the hall's west side red, its front in blue shade, the terrace in the trees' long shadow with streaks of red light across "
                    "it to the right and toward us; the sky in bands (the act's licence for chrome orange and geranium lake). Key: edo-sunset.",
           "note": "The land camera (persp.Camera 280/590, focal 800, lens 3.39 m up), its vanishing point at x 400. The hall is turned 22 degrees so its "
                   "west side (with the lattice window) shows; its front corner 14.5 m off (row 467). Mom before the doors (mark hall) is "
                   f"{round(168 / 181 * 160 * scale_at(MARKS['hall'][1]), 1)} px. The castle on the plain is drawn about four times larger than "
                   "the eye would see it 6 km off (the prints' way), and the plain is put at the picture's right though it lies south-east of the hall "
                   "(the mountain is at the left): a painter's liberty."}
    out["view"] = {"horizon": HZ, "full": FULL, "focal": FOC, "vanish_x": VX, "eye_cm": round(EYE, 1), "hall_turn_deg": 22}
    out["walk"] = walk_outline()
    out["walk_note"] = "one floor: the terrace before the hall, the path's foot, the hut's front, the road up at the bottom right"
    X, D = ES.STONE
    blocked = [[foot(X - 24, D - 8), foot(X + 24, D - 8), foot(X + 24, D + 26), foot(X - 24, D + 26)]]
    cx, cd = ES.COMBS
    blocked.append([foot(cx - 44, cd - 34), foot(cx + 50, cd - 34), foot(cx + 50, cd + 34), foot(cx - 44, cd + 34)])
    blocked.append([[0, 598], [52, 598], [50, 556], [0, 556]])                     # the near pine's foot
    blocked.append([foot(-470, 1590), foot(-400, 1590), foot(-400, 1640), foot(-470, 1640)])   # the hut's firewood
    out["blocked"] = blocked
    out["blocked_note"] = "the stone, the heap of combs on its cloth, the near pine's foot, the hut's firewood; the bench gives solid ground of its own"
    # ---- the cut-outs, back to front, as the scene lists them
    bx0, bx1 = ES.BENCH_X
    bench_base = int(round(row_D(ES.BENCH_D + 4)))
    stone_base = int(round(row_D(ES.STONE[1])))
    planes = [
        {"id": "sunset", "file": "sunset.png", "plane": "back", "what": "the whole stage at sunset: a layer the scene fades in over back.png (under everybody and "
                                                                       "under the cut-outs, which take their -sunset twins as it comes): ENGINE-21's layer fade",
         "state": "shown (faded in) once the sun goes low: when the lock opens (the design: the scene changes state when the lock is open)"},
        {"id": "doors", "file": "doors.png", "plane": "back", "what": "the hall's latticed double doors (they part in the middle and swing out toward us)",
         "states": {"shut": "doors.png", "half": "doors-half.png", "open": "doors-open.png", "shut-sunset": "doors-sunset.png", "half-sunset": "doors-half-sunset.png",
                    "open-sunset": "doors-open-sunset.png"},
         "note": "the swing: shut -> half -> open, two or three tenths of a second each; open shows the dim hall inside, its cabinet at the back and the bars "
                 "of light from the west lattice across the floor (painted in the backdrop behind the doors, so the doorway is never empty)"},
        {"id": "lock", "file": "lock.png", "plane": "back", "what": "the shipwright's lock on the hasp (small: the close-up edo-lock is where it is seen)",
         "states": {"shut": "lock.png", "open": "lock-open.png", "shut-sunset": "lock-sunset.png", "open-sunset": "lock-open-sunset.png"},
         "note": "open: the bolt drawn, the lock hanging from the staple. Hide it once the doors swing (it is on the leaves)"},
        {"id": "stepball", "file": "stepball.png", "plane": "back", "what": "O-Ume's rice ball on its leaf on the step",
         "states": {"there": "stepball.png", "there-sunset": "stepball-sunset.png"}, "note": "hidden once it is taken in"},
        {"id": "stone", "file": "stone.png", "base": stone_base, "what": "the small stone at the path's foot (women may not pass: our own marks cut in it)",
         "states": {"gold": "stone.png", "sunset": "stone-sunset.png"}, "solid": blocked[0]},
        {"id": "bench", "file": "bench.png", "base": bench_base, "what": "the bench where the women wait: they sit on it (feet on row 490, in front of it)",
         "states": {"gold": "bench.png", "sunset": "bench-sunset.png"},
         "solid": [foot(bx0, ES.BENCH_D), foot(bx1, ES.BENCH_D), foot(bx1, ES.BENCH_D + 34), foot(bx0, ES.BENCH_D + 34)]},
        {"id": "pine", "file": "pine.png", "plane": "front", "what": "the pine near us at the left edge, its pads over the top-left (it stirs: fx sway)",
         "states": {"gold": "pine.png", "sunset": "pine-sunset.png"}},
    ]
    out["planes"] = planes
    out["cutouts"] = {k: list(box_of(alpha[k])) for k in ES.CUTS + ES.ALTS}
    # ---- the things to click
    things = []

    def thing(id_, what, shape, stand, face="N", **more):
        d = {"id": id_, "what": what, "shape": {"poly": shape}, "stand": stand, "face": face}
        d.update(more)
        things.append(d)
    M = MARKS
    thing("mountain", "Mount Shosha going up into the trees (the temple is up there, out of sight: an hour's climb by the east path)",
          [[0, 0], [180, 0], [300, 52], [400, 124], [480, 190], [560, 244], [620, 288], [420, 200], [270, 200], [0, 190]], M["path"])
    thing("pathup", "the east path: stone steps climbing steeply into the trees, out of sight", [[188, 458], [262, 458], [256, 380], [236, 320], [196, 316], [190, 380]], M["path"])
    thing("stone", "a small upright stone at the path's foot, cut with writing (women may not pass)", hull(alpha["stone"], 3, 10), M["stone"])
    thing("trees", "pines and maples in fresh leaf on the mountain's foot; the glade of trunks at the left", [[0, 186], [270, 200], [266, 352], [0, 356]], M["hut"])
    thing("cherry", "a late cherry in the shade of the slope, still in flower", [[150, 218], [270, 214], [276, 290], [150, 292]], M["path"])
    thing("hall", "the women's hall: small, deep-roofed, on a low stone base, a jewel on its roof's peak",
          [r(ES.HP(-ES.EAVE_OUT, -ES.EAVE_OUT, ES.EAVE_Y)), r(ES.HP(SIDE + ES.EAVE_OUT, -ES.EAVE_OUT, ES.EAVE_Y)), r(ES.HP(SIDE / 2, SIDE / 2, ES.FINIAL_Y)),
           r(ES.HP(-ES.EAVE_OUT, SIDE + ES.EAVE_OUT, ES.EAVE_Y)), r(ES.HP(-30, SIDE + 30, 0)), r(ES.HP(-30, -30, 0)), r(ES.HP(SIDE + 30, -30, 0))], M["hall"])
    thing("doors", "the latticed double doors, shut; dark inside", hull(alpha["doors"], 2, 10), M["hall"],
          open=hull(alpha["doors-open"], 2, 12))
    la = r(ES.HP(ES.LOCK_AT[0] - 26, -5, ES.LOCK_AT[1] - 16))
    lb = r(ES.HP(ES.LOCK_AT[0] + 26, -5, ES.LOCK_AT[1] + 16))
    thing("lock", "on the hasp, a lock: a dark block bound with iron, carved (too small to see from here: Look closer)",
          [[la[0], lb[1]], [lb[0], lb[1]], [lb[0], la[1]], [la[0], la[1]]], M["lock"], note="the close-up edo-lock opens from here (Look closer / Use)")
    da, db = ES.DOOR_A
    thing("slips", "name slips pasted round the doors and up the posts, hundreds: paper and thin wood, old and new",
          [r(ES.HP(4, -3, 70)), r(ES.HP(da - 4, -3, 70)), r(ES.HP(da - 4, -3, 260)), r(ES.HP(4, -3, 260))], M["hall"],
          also=[[r(ES.HP(db + 4, -3, 70)), r(ES.HP(SIDE - 4, -3, 70)), r(ES.HP(SIDE - 4, -3, 260)), r(ES.HP(db + 4, -3, 260))]])
    thing("step", "the step before the doors: one broad dressed stone", [r(ES.HP(66, -100, 0)), r(ES.HP(294, -100, 0)), r(ES.HP(294, -30, 22)), r(ES.HP(66, -30, 22))], M["step"])
    thing("stepball", "a rice ball on a leaf on the step (O-Ume's, each evening)", hull(alpha["stepball"], 5, 8), M["step"])
    lb0, lb1 = ES.LATTICE_B
    ly0, ly1 = ES.LATTICE_Y
    thing("lattice", "the lattice window in the hall's west side", [r(ES.HP(0, lb0 - 8, ly0 - 8)), r(ES.HP(0, lb1 + 8, ly0 - 8)), r(ES.HP(0, lb1 + 8, ly1 + 8)), r(ES.HP(0, lb0 - 8, ly1 + 8))], M["stone"])
    x0, x1 = ES.HUTX
    d0, d1 = ES.HUT_D
    thing("hut", "O-Ume's hut by the path: a little thatched hut, its straw curtain half rolled up",
          [foot(x0 - 50, d0 - 60), foot(x1 + 50, d0 - 60), r(P(x1 + 50, 190, d0 - 60)), r(P(x1 - 40, 330, (d0 + d1) / 2)), r(P(x0 + 40, 330, (d0 + d1) / 2)), r(P(x0 - 50, 190, d0 - 60))], M["hut"])
    lx, ly, ld = ES.HUT_LANTERN
    lp = P(lx, ly, ld)
    thing("lantern", "a paper lantern on a hook by the hut's door, unlit", [[int(lp[0]) - 9, int(lp[1]) - 8], [int(lp[0]) + 9, int(lp[1]) - 8], [int(lp[0]) + 9, int(lp[1]) + 20], [int(lp[0]) - 9, int(lp[1]) + 20]], M["hut"])
    thing("bench", "a long plain bench, worn: the women wait on it", hull(alpha["bench"], 4, 10), M["bench"])
    thing("combs", "a heap of combs and hairpins on a cloth: boxwood, tortoiseshell, lacquer: the ones that failed",
          [foot(cx - 46, cd - 36), foot(cx + 52, cd - 36), r(P(cx + 52, 12, cd + 36)), r(P(cx - 46, 12, cd + 36))], M["combs"])
    thing("plain", "far below, the Harima plain: fields, villages, a river", [[560, 284], [800, 270], [800, 410], [560, 420]], M["view"], "E")
    cxs, cys = ES.CASTLE_AT
    thing("castle", "on its hill on the plain, small and white: the castle", [[int(cxs) - 34, int(cys) - 36], [int(cxs) + 30, int(cys) - 36], [int(cxs) + 30, int(cys) + 4], [int(cxs) - 34, int(cys) + 4]], M["view"], "E")
    thing("sky", "the sky over the plain (gold; then the sunset's bands)", [[300, 0], [800, 0], [800, 262], [640, 262], [470, 160], [300, 40]], M["view"], "E")

    def person(id_, mark, cm, what, seated=False):
        x, y = MARKS[mark]
        sc = scale_at(y)
        h = cm / 181.0 * 160 * sc * (0.72 if seated else 1.0)
        w = max(14, h * 0.4)
        thing(id_, what, [[int(x - w / 2), int(y + 2)], [int(x + w / 2), int(y + 2)], [int(x + w / 2), int(y - h)], [int(x - w / 2), int(y - h)]], MARKS[mark], "N", person=True, mark=mark)
    person("ume", "ume", 136, "O-Ume, the hall's keeper, small and bent")
    person("ryokai", "ryokai", 150, "Ryokai, the novice, sitting on the bottom step by the stone", seated=True)
    person("tome", "tome", 138, "Grandmother Tome, on the bench", seated=True)
    person("wife", "wife", 146, "a young wife with a baby on her back, on the bench", seated=True)
    person("girl", "girl", 138, "a girl of eleven with her grandmother's slip, on the bench", seated=True)
    out["things"] = things
    out["marks"] = dict(MARKS)
    out["faces"] = FACES
    out["stands"] = {k: {"at": v, "grownup_px": int(round(160 * scale_at(v[1]))), "floor": "ground"} for k, v in MARKS.items()}
    out["sizes"] = {"mom_px_at_hall": round(168 / 181 * 160 * scale_at(MARKS["hall"][1]), 1), "lilsis_px_at_lock": round(122 / 181 * 160 * scale_at(MARKS["lock"][1]), 1),
                    "ume_136cm_px": round(136 / 181 * 160 * scale_at(MARKS["ume"][1]), 1), "ryokai_150cm_px_standing": round(150 / 181 * 160 * scale_at(MARKS["ryokai"][1]), 1),
                    "mom_px_at_road": round(168 / 181 * 160 * scale_at(MARKS["road"][1]), 1), "doors_px": [round(P(0, ES.DOOR_Y[1], H_(180, 0)[1])[1]), round(P(0, ES.DOOR_Y[0], H_(180, 0)[1])[1])],
                    "lock_center": r(ES.HP(ES.LOCK_AT[0], -5, ES.LOCK_AT[1]))}
    out["exits"] = [
        {"id": "road", "to": None, "name": "the road back to the town", "edge": "right", "walkTo": MARKS["road"], "band": [[690, 560], [800, 470], [800, 598], [690, 598]],
         "note": "to Himeji by the map ('An hour and a half's walk'), or the cut-scene Mind The Fire after #38"},
        {"id": "path", "to": None, "name": "the path up the mountain", "walkTo": MARKS["path"], "band": [[188, 452], [262, 452], [262, 300], [188, 300]],
         "note": "refuses, for every one of them (Ryokai: 'Women may not climb.')"},
        {"id": "doors", "to": "edo-hall", "spawn": "door", "name": "into the hall", "walkTo": MARKS["hall"], "band": hull(alpha["doors"], 0, 8),
         "note": "once the lock is open and the doors have swung (edo.hallOpen)"},
        {"id": "lock", "to": "edo-lock", "name": "the lock (close-up)", "walkTo": MARKS["lock"], "note": "the close-up; 'Step back.' returns here"},
    ]
    out["fx"] = [
        {"id": "pine", "type": "sway", "plane": "pine", "anchor": "bottom", "amount": 1.0, "period": 4.6, "what": "the near pine's pads stirring in the evening air"},
        {"id": "petals", "type": "petals", "what": "a few petals from the late cherry on the slope, drifting down the slope", "from": [[156, 226], [266, 222], [270, 286], [156, 290]],
         "floor": 470, "count": 4, "wind": 10, "fall": 18, "size": [2, 3], "color": "#f2c9d4", "color2": "#e2a8bc", "plane": "back"},
        {"id": "crows", "type": "birds", "what": "a crow or two going home to the mountain across the evening sky",
         "lanes": [[[830, 150], [260, 40]], [[830, 200], [360, 70]]], "every": [9, 18], "group": [1, 2], "speed": 50, "size": 8, "plane": "back",
         "note": "engine-drawn dark silhouettes; at sunset most of all (the scene's `when`)"},
    ]
    out["fx_note"] = ("Moving: the pine's pads, a few cherry petals, crows going home; the light (the sunset layer fading in over back.png, ENGINE-21); "
                      "the bell from the mountain is a sound (ENGINE-21). The people's own small lives (PEOPLE-21B): O-Ume's rice ball on its leaf, "
                      "Ryokai counting his beads, the women on the bench.")
    out["sunset_note"] = ("The two lights: back.png + the plain cut-outs (gold), sunset.png + the -sunset twins. The engine fades sunset.png in over "
                          "back.png on the back plane (under everybody), and switches each cut-out to its twin as it does (or cross-fades them too, if "
                          "it can). The open doors show the dim hall with its bars of light in both lights (gold bars by day, red at sunset).")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    return out


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    o = write(f"{OUT}/layout.json")
    print(json.dumps(o["marks"]))
    print(json.dumps(o["sizes"]))

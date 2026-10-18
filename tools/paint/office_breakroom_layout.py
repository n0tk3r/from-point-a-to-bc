"""layout.json for office-breakroom: the numbers the scene writer needs, MEASURED from the finished picture. OFFICE-17D.

Every shape is round the pixels that really show that thing (found from what each ray of the picture met), or, for a
flat thing on a wall (a sheet on the board, the machine's buttons), its own corners put through the camera. Places on
the floor (where to stand, the walk outline, the base lines and the ground of the cut-outs) are the model's
centimetres put through the same camera as the picture. Ranger's places off the floor (the fridge's top, the
microwave's, the counter's) are given with the size he is drawn at there, and each level's own `horizon` and `full`:
the two numbers that size a figure standing on that level by its row, as the scene's own two size one on the floor.

    python3 office_breakroom_layout.py check     draws layout.json over the comp: out/office-breakroom-check.png"""

import json
import math
import sys

import numpy as np

from room import View
import office_breakroom_model as M

OUT = "out/office-breakroom"
W, H = 800, 600
RANGER = {"foot": [68, 56], "tall": {"stand": 34, "sit": 49}, "canvas": [124, 58]}     # nevada-roadside/ranger.json (as installed)


def hull(points):
    pts = sorted(set(map(tuple, points)))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def simplify(poly, most=12):
    p = list(poly)
    while len(p) > most:
        best, bi = 1e18, 0
        for i in range(len(p)):
            a, b, c = p[i - 1], p[i], p[(i + 1) % len(p)]
            area = abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]))
            if area < best:
                best, bi = area, i
        p.pop(bi)
    return p


def inside(pt, poly):
    x, y = pt
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1:
            c = not c
    return c


def write(stA, stB, covers, frames, wob=None):
    v = View(**M.VIEW)
    dfull = v.F * v.eye / (v.full - v.hz)

    def fl(X, Z, Y=0.0):
        x, y = v.pt(X, Y, Z)
        return [int(round(x)), int(round(y))]

    def scale_at(X, Y, Z):
        return dfull / v.cam_space(X, Y, Z)[2]

    def mask_of(st, names):
        ids = [st.names[n] for n in names if n in st.names]
        m = np.isin(st.pick(st.oid), ids)
        if wob is not None:
            m = wob(m.astype(np.float32)) > 0.5
        return m

    def rect_of(st, names, pad=1):
        m = mask_of(st, names)
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            return None
        x0, y0, x1, y1 = int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max()) + 1 + pad, int(ys.max()) + 1 + pad
        x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
        return [x0, y0, x1 - x0, y1 - y0]

    def poly_pts(pts, pad=1.0, most=12):
        corners = np.concatenate([pts + [0, 0], pts + [1, 0], pts + [0, 1], pts + [1, 1]])
        h = simplify(hull([tuple(p) for p in corners.tolist()]), most)
        cx, cy = np.mean([p[0] for p in h]), np.mean([p[1] for p in h])
        out = []
        for x, y in h:
            d = math.hypot(x - cx, y - cy) + 1e-6
            out.append([int(round(min(max(x + (x - cx) / d * pad, 0), W))), int(round(min(max(y + (y - cy) / d * pad, 0), H)))])
        return out

    def poly_of(st, names, most=12, pad=1.0):
        m = mask_of(st, names)
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            return None
        return poly_pts(np.stack([xs, ys], 1), pad, most)

    def quad(pts3):
        return [[int(round(c)) for c in v.pt(*p)] for p in pts3]

    mk = M.MARKS
    stand = {k: fl(*p) for k, p in mk.items()}
    size = {k: int(round(v.person(*p)[2])) for k, p in mk.items()}
    walk = [fl(X, Z) for X, Z in M.WALK]
    for k, p in stand.items():
        if k not in ("floyd", "jed") and not inside(p, walk):
            print("layout: the stand place", k, p, "is outside the walk outline")

    things = []

    def thing(id_, what, shape, at, face, **more):
        if shape is None:
            print("layout: nothing found for", id_)
            return
        sh = {"poly": shape} if isinstance(shape[0], list) else {"rect": shape}
        t = {"id": id_, "what": what, "shape": sh, "stand": stand[at] if isinstance(at, str) else at, "face": face}
        t.update(more)
        things.append(t)

    A, B = stA, stB
    up = {k: {"at": fl(X, Z, Y), "scale": round(scale_at(X, Y, Z), 3)} for k, (X, Y, Z) in M.UP.items()}
    # listed back to front: where two shapes overlap, the later one is on top
    thing("vent", "the return grille in the ceiling over the fridge: white slats, the duct's dark between them (Ranger comes down "
          "through it onto the fridge, and goes back up from there; cut-out vent.png, vent-eyes.png)",
          poly_of(A, ["vent", "ventgap"], 8, 2.0), "atfridge", "N", ranger=up["fridge"]["at"],
          note="Ranger's `climb` to the duct (mark `over-break`) is from the fridge's top (mark `fridge`)")
    thing("speaker", "the building's speaker, a beige steel box high in the far right corner, a round grille in its face (Houston)",
          poly_of(A, ["speaker"], 8, 2.0), "door", "NE")
    thing("clock", "the wall clock over the board: ten to two, its red second hand going round (frames clock-0 .. clock-59)",
          poly_of(A, ["clock", "clockhands"], 12, 1.0), "atclock", "N")
    thing("cabinets", "the wall cabinets over the microwave, the rack and the sink: wood-grain doors, chrome pulls (paper towels under them)",
          rect_of(A, ["cabinets", "towels"]), "atsink", "N")
    thing("calendar", "a wall calendar on the left wall: a desert with a mesa (nobody's photograph), OCTOBER, every day crossed off "
          "but the last", poly_of(A, ["calendar"], 8), "atfridge", "W")
    thing("door", "the door to the hall: painted steel, a narrow wired window, a gray jacket on a hook (somebody's); open, it stands "
          "into the room and shows its hall side, BREAK ROOM on a plate, and the hall beyond (cut-outs door.png, door-open.png)",
          poly_of(A, ["doorleaf", "doorglass", "doorhandle", "jacket", "doorframe"], 10), "door", "N")
    thing("fridge", "the fridge: tall, old, almond enamel, magnets of every colour, a takeout menu under two of them; inside, lunches "
          "labelled DALE, MERLE, NOT YOURS (not painted: it is shut)", poly_of(A, ["fridge", "magnet", "fridgemenu"], 10), "atfridge", "N")
    thing("sign", "the sign on the freezer door: LABEL YOUR LUNCH. · MGMT. (printed; readable)", quad(_sign_corners()), "atfridge", "N")
    thing("forks", "on top of the fridge, a box of plastic forks, open (Ranger's step up to the grille)", poly_of(A, ["forks"], 8, 1.5),
          "atfridge", "N", ranger=up["fridge"]["at"])
    thing("plant", "on top of the fridge, a dusty plant, its runners hanging down over the front corner", poly_of(A, ["plant"], 10, 1.5),
          "atfridge", "N", ranger=up["fridge"]["at"])
    thing("microwave", "the microwave at the counter's left end, by the fridge: almond, a smoked window, its clock lit green "
          "(Ranger's step between the fridge and the counter)", poly_of(A, ["micro"], 8), "atmicro", "N", ranger=up["micro"]["at"])
    thing("counter", "the counter: wood-grain cabinets with chrome pulls, a pale speckled top, a backsplash",
          poly_of(A, ["counter", "countertop", "splash"], 10), "atcounter", "N", ranger=up["counter"]["at"])
    thing("rack", "the dish rack: a plate, a red mug, a blue mug", poly_of(A, ["rack"], 8, 1.5), "atsink", "N", ranger=up["sink"]["at"])
    thing("sink", "the sink: a steel basin let into the counter, a gooseneck tap (Ranger washes the tin here)",
          poly_of(A, ["sink", "faucet"], 10, 1.5), "atsink", "N", ranger=up["sink"]["at"])
    thing("board", "the corkboard over the counter, at a raccoon's eye from the counter's top", rect_of(A, ["board"]), "atboard", "N",
          ranger=up["board"]["at"])
    for sid, what in (("form7", "FORM 7 IS NOT OPTIONAL: a printed notice (FORM 7 readable)"),
                      ("found", "an index card gone yellow, pinned with too many pins: FOUND: ONE ROMAN SANDAL (1951) · SEE OPAL "
                                "(written small; the look says it)"),
                      ("bowling", "the bowling league's sheet: a ball and three pins drawn at the top, LEAGUE, a grid of scores"),
                      ("menu", "a menu from somewhere that delivers: a drawing of a cheeseburger, prices")):
        thing(sid, what, quad(_sheet_corners(sid)), "atboard", "N", ranger=up["board"]["at"])
    thing("schedule", "the test schedule: a typed sheet headed LAMPLIGHTER · TEST SCHEDULE, its lines too small to read here (cut-out "
          "schedule.png; when it is gone, a pin and a torn corner of paper are left on the board)",
          quad(_sched_corners()), "atboard", "N", ranger=up["board"]["at"])
    thing("coffee", "the coffee maker: black, its pot full and hot (steam: layout `fx`), its little lamp lit",
          poly_of(A, ["coffee", "pot"], 10, 1.5), "atcoffee", "N", ranger=up["counter-end"]["at"])
    thing("cups", "a stack of paper cups, upside down, and the sugar", poly_of(A, ["cups", "sugar"], 8, 1.5), "atcoffee", "N",
          ranger=up["counter-end"]["at"])
    thing("pie", "Wendell's pie: a whole cherry pie with a lattice top, in a tin with a crimped rim (cut-outs pie.png, pie-eaten.png, "
          "pie-gone.png)", poly_of(A, ["pietin", "piecrust"], 10, 1.5), "atcounter", "N", ranger=up["counter"]["at"])
    thing("card", "the card stood against the tin: HAPPY BIRTHDAY WENDELL in blue, DO NOT EAT and (REGULATIONS) in red (too small to read "
          "here; the look says it)", poly_of(A, ["card"], 6, 1.5), "atcounter", "N", ranger=up["counter"]["at"])
    thing("vending", "the snack machine: no name on it, dark blue steel, five rows of coils with packets in plain colours behind its window "
          "(a pretzel, a cracker, a chip drawn on them), a bowling trophy on top (cut-outs vending.png, vending-peanuts.png, "
          "vending-taken.png)", poly_of(A, ["vending", "trophy"], 10), "vending", "N")
    thing("buttons", "the machine's buttons: a column of them, the coin slot and the return", quad(_panel_corners()), "vending", "N")
    thing("tray", "the machine's tray at the bottom, behind its flap (where a packet comes down to)", quad(_tray_corners()), "vending", "N")
    thing("trash", "a tan kitchen bin with a swing lid, in the gap by the fridge", poly_of(A, ["trash"], 8), "atfridge", "NW")
    thing("couch", "the couch along the left wall: brown tweed, three cushions, an afghan of granny squares over its back, a mustard "
          "cushion (Floyd sleeps on it)", poly_of(A, ["couch", "cushion", "backcushion", "pillow", "afghan"], 12), "atcouch", "W")
    thing("chair", "Jed's chair: orange molded plastic on chrome legs, turned to look along the counter at the pie (cut-out chair.png)",
          poly_of(A, ["chair"], 10, 1.5), "atcoffee", "S")
    thing("table", "a round table in the near right: white laminate, a folded newspaper (no name), a green mug, a napkin holder; an "
          "avocado chair at it (cut-out front.png)", poly_of(A, ["table", "newspaper", "mug", "napkins", "tablechair"], 12), "attable", "SE")
    # OFFICE-17D (resumed): the low table, the near left's foreground
    thing("lowtable", "a low table in front of the couch, in the near left: a game of solitaire laid out and left halfway (Floyd's, "
          "before Regulation 22), the pack beside it, two magazines (a fish on one, a bowling pin on the other: no names), a mug "
          "gone cold (cut-out front.png)", poly_of(A, ["lowtable", "cards", "magazine", "lowmug"], 12), "atcouch", "S")
    thing("cards", "the solitaire: seven columns, the pack face down, a red card turned up from it (nobody has moved since 0500)",
          poly_of(A, ["cards"], 8, 1.5), "atcouch", "S")

    def foot(X0, X1, Z0, Z1):
        return [fl(X0, Z0), fl(X1, Z0), fl(X1, Z1), fl(X0, Z1)]
    vx0, vx1, _, _, vz0, vz1 = M.VENDING
    cx0, cx1, cz0, cz1 = M.CHAIR
    tX, tZ, tR, _ = M.TABLE
    door_open_line = _door_open_line()
    planes = [
        {"id": "vent", "file": "vent.png", "plane": "back", "note": "the grille, plain. Hidden: the duct's dark mouth (the backdrop), for while "
                                                                  "Ranger is going through, if the scene likes"},
        {"id": "vent-eyes", "file": "vent-eyes.png", "alt": True, "replaces": ["vent"], "plane": "back",
         "note": "Ranger over the grille, his eyes shining, his mask and nose at the gap nearest us (while he is at the grille over the "
                 "break room, `over-break`)"},
        {"id": "door", "file": "door.png", "plane": "back", "note": "the door, shut (the hall is painted in the backdrop behind it)"},
        {"id": "door-open", "file": "door-open.png", "alt": True, "replaces": ["door"], "base": [fl(*door_open_line[0]), fl(*door_open_line[1])],
         "solid": [fl(*p) for p in _door_open_foot()], "note": "standing open into the room on its hinges at the right jamb (76 degrees): "
                                                                "its hall side to us, BREAK ROOM on its plate"},
        {"id": "schedule", "file": "schedule.png", "plane": "back", "note": "on the board until Ranger takes it (`when: !g.flag(\"office.schedule\")` "
                                                                          "or the scene's own fact)"},
        {"id": "pie", "file": "pie.png", "plane": "back", "note": "the whole pie and its card (until `office.pieEaten`)"},
        {"id": "pie-eaten", "file": "pie-eaten.png", "alt": True, "replaces": ["pie"], "plane": "back",
         "note": "the empty tin, sticky, the bottle cap in its middle, the card still standing (`office.pieEaten`, until the tin is taken)"},
        {"id": "pie-gone", "file": "pie-gone.png", "alt": True, "replaces": ["pie"], "plane": "back",
         "note": "the tin taken: the card fallen flat, the bottle cap left on it, a sticky ring (`office.tinClean` or once the tin is "
                 "in Ranger's stash: the scene decides)"},
        {"id": "vending", "file": "vending.png", "base": [fl(vx0, vz1), fl(vx1, vz1)], "solid": foot(vx0, vx1, vz0, vz1),
         "note": "the snack machine, full"},
        {"id": "vending-peanuts", "file": "vending-peanuts.png", "alt": True, "replaces": ["vending"], "base": [fl(vx0, vz1), fl(vx1, vz1)],
         "note": "the packet of peanuts lying in the tray, its coil empty"},
        {"id": "vending-taken", "file": "vending-taken.png", "alt": True, "replaces": ["vending"], "state_of": "vending-peanuts",
         "base": [fl(vx0, vz1), fl(vx1, vz1)], "note": "a state of vending-peanuts: the tray empty again, the coil still empty"},
        {"id": "chair", "file": "chair.png", "base": [fl(cx0 - 2, cz0), fl(cx1 + 2, cz0)], "solid": foot(cx0 + 2, cx1 - 2, cz0 + 2, cz1 - 2),
         "note": "Jed's chair. Its base is its FAR edge, so that Jed, sitting in it (his mark is under his hips, in front of that edge), is "
                 "drawn over it, and anyone at the counter behind it is drawn behind it"},
        {"id": "front", "file": "front.png", "plane": "front", "note": "the round table and its chair in the near right, and the low table "
                                                                    "in the near left (OFFICE-17D, resumed): in front of everybody, out "
                                                                    "past the walk's front edge"},
    ]
    seat_note = ("the game draws a seated person with the hips at the seat's height above the mark (the rig's `chair` seat, 0.262 of a "
                 "grown person: 45.9 cm): the couch's cushions and Jed's chair are both at exactly that height")
    seats = {
        "floyd": {"at": stand["floyd"], "face": "E", "seat": "chair", "seat_cm": M.SEAT_H, "seat_row": fl(*mk["floyd"], M.SEAT_H)[1],
                  "grownup_px": size["floyd"], "on": "the couch, at its far end, his back to the back cushions (sitting slumped: PEOPLE-17)",
                  "back_cm": [M.BACK_X, M.COUCH[3] - 3.0], "note": seat_note},
        "jed": {"at": stand["jed"], "face": "W", "seat": "chair", "seat_cm": M.CHAIR_SEAT, "seat_row": fl(*mk["jed"], M.CHAIR_SEAT)[1],
                "grownup_px": size["jed"], "on": "his orange chair at the counter's right end, facing W along the counter at the pie",
                "note": seat_note},
    }
    # Ranger's places off the floor, the levels he walks on, and the paths between them
    levels = {}
    for name, Yl, outline in (("counter", M.COUNTER[3], M.COUNTER_WALK), ("micro", M.MICRO[3], None), ("fridge", M.FRIDGE[3], None)):
        full_l = v.hz + (v.full - v.hz) * (v.eye - Yl) / v.eye
        lv = {"y_cm": Yl, "horizon": round(v.hz, 1), "full": round(full_l, 2),
              "note": "a figure's size on this level is (feet row - horizon) / (full - horizon), as on the floor with the scene's own two"}
        if outline:
            lv["walk"] = [fl(X, Z, Yl) for X, Z in outline]
        levels[name] = lv
    levels["fridge"]["note"] = ("the fridge's top is 5 cm under the eye: seen edge-on, so its rows say almost nothing of size; give Ranger "
                                "the scale of the mark (`ranger_marks.fridge.scale`) there and do not size him by his row")
    ranger_marks = {}
    for k, (X, Y, Z) in M.UP.items():
        s_ = scale_at(X, Y, Z)
        ranger_marks[k] = {"at": fl(X, Z, Y), "scale": round(s_, 3), "drawn_px": {"stand": round(RANGER["tall"]["stand"] * s_, 1),
                                                                                 "sit": round(RANGER["tall"]["sit"] * s_, 1)},
                           "level": "fridge" if Y >= 190 else ("micro" if Y > 100 else "counter")}
    ranger_marks["fridge"]["face"] = "E"
    ranger_marks["counter"]["face"] = "E"
    ranger_marks["sink"]["face"] = "E"
    ranger_marks["board"]["face"] = "E"
    ranger_marks["vending"] = {"at": stand["vending"], "scale": round(v.person(*mk["vending"])[2] / 160.0, 3), "level": "floor", "face": "N"}
    paths = {
        "fridge-counter": {"points": [ranger_marks["fridge"]["at"], ranger_marks["micro"]["at"], ranger_marks["counter-left"]["at"]],
                           "note": "down: from the fridge's top to the microwave's (a hop down), then down to the counter; back up the same way "
                                   "(the `climb` frames for the last step up the fridge's side)"},
        "counter-floor": {"points": [ranger_marks["counter-end"]["at"], fl(492.0, 98.0), stand["vending"]],
                          "note": "the counter's right end, a hop down to the floor in front of the machine's corner, and along to it"},
        "vent-fridge": {"points": [_vent_middle(v), ranger_marks["fridge"]["at"]], "note": "the drop: from the grille's middle straight "
                                                                                          "down onto the fridge's top"},
    }
    tx0, tx1, tz0, tz1 = M.TROFFERS[0]
    px, pz, pr, pf, ptop = M.POT
    fx = [
        {"id": "steam", "what": "steam off the full coffee pot", "type": "smoke", "at": fl(px, pz, ptop + 0.5), "height": 34, "width": [2, 9],
         "lean": [-4, -34], "rise": 7, "rate": 2.2, "gust": 0.25, "color": "#e8ece4", "opacity": 0.26, "base": fl(px, M.COUNTER[5]),
         "note": "small and slow: a cup's worth, rising from the pot's mouth and fading in the cool air"},
    ]
    cf = frames["clock"]
    frames_out = {"clock": {"files": cf["files"], "fps": 1, "at": cf["at"], "foot": cf["foot"], "rect": cf["rect"], "plane": "back",
                            "note": "the second hand alone (the face, the hour and minute hands are in the backdrop): one frame a second, "
                                    "clock-0 at twelve; lay it as the store lays its TV, a plane with frames"}}
    L = {
        "id": M.ID, "horizon": M.VIEW["horizon"], "full": M.VIEW["full"], "view": M.VIEW, "eye_cm": round(v.eye, 1),
        "vanishing": [int(round(v.vanishing()[0][0])), int(round(v.vanishing()[0][1]))],
        "maxScale": 1.2,
        "light": "two fluorescent fittings in the ceiling (the near one has two tubes out): a cool, faintly green white falling straight "
                 "down, the counter's top and the floor the lit planes, the walls falling off upward, shadows soft and violet under "
                 "things; the snack machine glows warm from inside; the hall's tubes light the door's window",
        "fx_note": "The coffee's steam is the engine's (`fx`: smoke). The clock's second hand turns (frames). The tubes do not flicker. "
                   "Floyd's zzz are thoughts (g.think).",
        "walk": walk,
        "walk_note": "the floor in front of the counter, the machine and the door, clear of the couch, Jed's chair and the table; its front "
                     "edge keeps people under about 1.2 of full size. Ranger's own floors (the counter's top; the fridge's and the "
                     "microwave's tops, one place each) are `levels` and `ranger_marks`",
        "blocked": [foot(cx0 + 2, cx1 - 2, cz0 + 2, cz1 - 2)],
        "planes": planes,
        "frames": frames_out,
        "things": things,
        "marks": {"fridge": ranger_marks["fridge"]["at"], "counter": ranger_marks["counter"]["at"], "sink": ranger_marks["sink"]["at"],
                  "board": ranger_marks["board"]["at"], "floyd": stand["floyd"], "jed": stand["jed"], "vending": stand["vending"],
                  "door": stand["door"], "fromHall": [stand["door"], stand["hall2"], stand["hall3"]],
                  "note": "fridge, counter, sink, board: Ranger, off the floor (ranger_marks: his size there); floyd, jed: seated (seats); "
                          "vending: in front of the machine, on the floor; door and fromHall: whoever comes in from the hall"},
        "ranger_marks": ranger_marks,
        "levels": levels,
        "paths": paths,
        "seats": seats,
        "stands": {k: {"at": stand[k], "grownup_px": size[k]} for k in mk},
        "fx": fx,
        "exits": [],
        "exits_note": "no way out at an edge: the door is a thing (`door`; Jed goes out through it by a script, the cheeseburger at the front "
                      "desk), and Ranger's way in and out is the grille over the fridge (a drop onto `fridge`, a climb back to `over-break`)",
        "cutouts": {k: bbox(a) for k, a in covers.items()},
        "lights": {"tubes-over-counter": [int(round(c)) for c in v.pt((tx0 + tx1) / 2, M.H, (tz0 + tz1) / 2)],
                   "vending": [int(round(c)) for c in v.pt((M.VEND_GLASS[0] + M.VEND_GLASS[1]) / 2, 120, M.VENDING[5])],
                   "door-window": [int(round(c)) for c in v.pt(M.DOOR[1] - 22, 152, 0)]},
    }
    json.dump(L, open(f"{OUT}/layout.json", "w"), indent=1)
    return L


def _sign_corners():
    sx0, sy0, sx1, sy1 = M.SIGN
    z = M.FRIDGE[5] + 3.7
    return [(sx0, sy1, z), (sx1, sy1, z), (sx1, sy0, z), (sx0, sy0, z)]


def _sheet_corners(name):
    import office_breakroom_props as P
    return P.sheet_quad(name)


def _sched_corners():
    import office_breakroom_props as P
    return P.schedule_quad()


def _panel_corners():
    px0, px1, py0, py1 = M.VEND_PANEL
    z = M.VENDING[5] + 0.5
    return [(px0, py1, z), (px1, py1, z), (px1, py0, z), (px0, py0, z)]


def _tray_corners():
    tx0, tx1, ty0, ty1 = M.VEND_TRAY
    z = M.VENDING[5] + 0.5
    return [(tx0 - 2, ty1 + 2, z), (tx1 + 2, ty1 + 2, z), (tx1 + 2, ty0 - 2, z), (tx0 - 2, ty0 - 2, z)]


def _door_open_line():
    dx0, dx1, dy0, dy1 = M.DOOR
    w = dx1 - dx0 - 1.0
    a = math.radians(M.DOOR_OPEN)
    hx, hz = dx1 - 0.5, -1.0
    return [(hx, hz), (hx - math.cos(a) * w, hz + math.sin(a) * w)]


def _door_open_foot():
    (ax, az), (bx, bz) = _door_open_line()
    nx, nz = math.sin(math.radians(M.DOOR_OPEN)), math.cos(math.radians(M.DOOR_OPEN))
    t = 4.5
    return [(ax, az), (bx, bz), (bx - nx * t, bz - nz * t), (ax - nx * t, az - nz * t)]


def _vent_middle(v):
    x0, x1, z0, z1 = M.VENT
    return [int(round(c)) for c in v.pt((x0 + x1) / 2, M.H, (z0 + z1) / 2)]


def bbox(a):
    ys, xs = np.nonzero(a > 0.5)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


def check(src="out/office-breakroom-comp.png", out="out/office-breakroom-check.png"):
    """Draw layout.json over the comp, to see that the numbers are where the things are."""
    from PIL import Image, ImageDraw
    L = json.load(open(f"{OUT}/layout.json"))
    im = Image.open(src).convert("RGB")
    d = ImageDraw.Draw(im)
    w = [tuple(p) for p in L["walk"]]
    d.line(w + [w[0]], fill=(120, 255, 160), width=1)
    for b in L["blocked"]:
        q = [tuple(p) for p in b]
        d.line(q + [q[0]], fill=(255, 120, 120), width=1)
    cw = [tuple(p) for p in L["levels"]["counter"]["walk"]]
    d.line(cw + [cw[0]], fill=(120, 200, 255), width=1)
    for t in L["things"]:
        sh = t["shape"]
        if "rect" in sh:
            x, y, ww, hh = sh["rect"]
            d.rectangle([x, y, x + ww, y + hh], outline=(255, 230, 90))
            lx, ly = x, y
        else:
            q = [tuple(p) for p in sh["poly"]]
            d.line(q + [q[0]], fill=(255, 230, 90), width=1)
            lx, ly = min(p[0] for p in q), min(p[1] for p in q)
        d.text((lx + 2, ly + 1), t["id"], fill=(255, 255, 255))
    for p in L["planes"]:
        if isinstance(p.get("base"), list) and not p.get("alt"):
            d.line([tuple(p["base"][0]), tuple(p["base"][1])], fill=(255, 140, 40), width=2)
    for k, m in L["ranger_marks"].items():
        x, y = m["at"]
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 80, 255))
        d.text((x + 4, y - 10), k, fill=(255, 200, 255))
    for name in ("floyd", "jed", "door", "vending"):
        x, y = L["marks"][name]
        d.ellipse([x - 4, y - 4, x + 4, y + 4], outline=(255, 255, 255))
        d.text((x + 6, y - 5), name, fill=(255, 255, 255))
    for k, pth in L["paths"].items():
        d.line([tuple(p) for p in pth["points"]], fill=(255, 80, 255), width=1)
    for f in L["fx"]:
        x, y = f["at"]
        d.ellipse([x - 3, y - 3, x + 3, y + 3], outline=(80, 255, 255))
    d.line([(0, L["horizon"]), (800, L["horizon"])], fill=(255, 80, 80))
    d.line([(0, L["full"]), (800, L["full"])], fill=(255, 220, 80))
    im.save(out)
    return out


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        print(check())

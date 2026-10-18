"""layout.json for office-ducts (OFFICE-17B; OFFICE-17B2): the numbers the scene file and the engine need, MEASURED.

The shapes of things are the pixels that really show each thing (from what each ray of the finished picture met),
outlined; the places on the duct's floor (the marks, Ranger's places to stand, the walk outline) are the model's
centimetres put through the same camera as the picture (office_ducts_model.py)."""

import json
import math

import numpy as np

from brush import F32, blur
from room import View
import office_ducts_model as M
import office_letters as LT

OUT = "out/office-ducts"
W, H = 800, 600
V = View(**M.VIEW)
S0 = 160.0 / 175.0


def fl(X, Z, Y=0.0):
    x, y = V.pt(X, Y, Z)
    return [int(round(x)), int(round(y))]


def scale_at(X, Z):
    """The size the game draws a figure at here, as a share of full size (true perspective)."""
    return V.F / (S0 * V.cam_space(X, 0.0, Z)[2])


def poly_of(pts):
    return [[int(round(x)), int(round(y))] for x, y in pts]


def rect_poly(x0, y0, x1, y1):
    return [[int(x0), int(y0)], [int(x1), int(y0)], [int(x1), int(y1)], [int(x0), int(y1)]]


def band_poly(mask, step=16, pad=5):
    """A long thin thing's outline: its top and bottom edge read every `step` columns, `pad` px outside it."""
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    x0, x1 = int(xs.min()), int(xs.max())
    top, bot = [], []
    cols = list(range(x0, x1 + 1, step))
    if cols[-1] != x1:
        cols.append(x1)
    for x in cols:
        sl = mask[:, max(x - step // 2, 0):x + step // 2 + 1]
        r = np.nonzero(sl.any(axis=1))[0]
        if len(r) == 0:
            continue
        top.append([x, int(r.min()) - pad])
        bot.append([x, int(r.max()) + pad])
    top[0][0] -= pad
    bot[0][0] -= pad
    top[-1][0] += pad
    bot[-1][0] += pad
    return top + bot[::-1]


def write(st, fan_crop, fan_foot):
    """st: the Stage of the backdrop's render; fan_crop: the fan's frames' box on the stage (x0, y0, x1, y1); fan_foot:
    their foot point in the frame."""
    def own(*names, grow=0):
        m = st.down(st.mask_of(*names).astype(F32)) > 0.5
        if grow:
            m = blur(m.astype(F32), grow * 0.5) > 0.02
        return m

    def rect_of(m, grow=0):
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            return None
        return [int(xs.min()) - grow, int(ys.min()) - grow, int(xs.max() - xs.min() + 1) + 2 * grow, int(ys.max() - ys.min() + 1) + 2 * grow]

    marks, stands = {}, {}
    for k, ((X, Z), face) in M.MARKS.items():
        marks[k] = {"at": fl(X, Z), "face": face, "scale": round(scale_at(X, Z), 3)}
    marks["intake"]["note"] = "Ranger just in from the roof: he comes down the intake run and lands here, at its foot, facing along the duct"
    for gid, label, gx in M.GRILLES:
        m = marks["over-" + gid]
        m["grille"] = fl(gx, M.WALK_Z)
        m["note"] = (f"Ranger lying at the grille {label}, looking down through it: this is his foot point, his head over the grille's near "
                     "half (with the peek frames lying facing E, his nose some 42 px ahead of the foot point at full size). If the peek "
                     "frames carry his head further or nearer, move the mark by as much along the row.")
    marks["shaft"]["note"] = ("At the end of the duct's floor, the B-7 shaft and its fan below him (looking down it: on all fours his tail lies "
                              "over the HALL grille's right half; sitting up he fits on the floor's last span). Going down the shaft (the "
                              "cut-scene) is down the rungs on its back wall, past the fan, out of the bottom of the picture.")
    # the things, measured
    things = []

    def thing(id_, what, shape, stand_mark=None, stand=None, face="E", **more):
        if shape is None:
            print("layout: nothing found for", id_)
            return
        t = {"id": id_, "what": what, "shape": shape}
        if stand_mark:
            t["stand"] = marks[stand_mark]["at"]
            t["face"] = marks[stand_mark]["face"]
            t["mark"] = stand_mark
        else:
            t["stand"] = stand
            t["face"] = face
        t.update(more)
        things.append(t)

    def walk_point(x):
        """The place on the walk's middle row nearest a picture column."""
        a = (x - V.cx) / V.F * V.cam_space(0, 0, M.WALK_Z)[2] + V.cam_x
        a = min(max(a, M.WALK_X[0] + 4.0), M.WALK_X[1] - 4.0)
        return fl(a, M.WALK_Z)

    # OFFICE-17B2: the backs of the ceiling tiles in the gap under the duct, first (every thing under the duct lies over
    # them: the grilles' boots, the cup, the pencil, the wrapper, the fitting, the lifted tile)
    band_bot = fl(400.0, M.CUT, -M.SHELL)[1]
    tiles_cut = fl(400.0, M.CUT, M.TILE_Y)[1]
    sh_x = int(round(V.pt(M.SHAFT_X[0] - M.SHELL, 0.0, M.CUT)[0]))
    thing("tiles", "the backs of the ceiling tiles, under the duct: fibre board in its white grid, dusty; the light fittings glow up "
          "between them, and the rooms are under them", {"poly": rect_poly(0, band_bot + 1, sh_x - 1, tiles_cut + 2)},
          stand=walk_point(330), face="S")
    grilles = []
    for gid, label, gx in M.GRILLES:
        hx = M.GRILLE_L / 2
        floor_q = poly_of(V.poly([(gx - hx, 0.0, M.GRILLE_Z[0]), (gx + hx, 0.0, M.GRILLE_Z[0]), (gx + hx, 0.0, M.GRILLE_Z[1]), (gx - hx, 0.0, M.GRILLE_Z[1])]))
        tex, texel, sx0, sy0 = __import__("office_ducts_things").STENCILS[gid]
        tw = tex.shape[1] / texel
        th = tex.shape[0] / texel
        st_box = poly_of(V.poly([(sx0, sy0, M.DUCT_Z[0]), (sx0 + tw, sy0, M.DUCT_Z[0]), (sx0 + tw, sy0 - th, M.DUCT_Z[0]), (sx0, sy0 - th, M.DUCT_Z[0])]))
        boot = own("boot-" + gid)
        # the area to click: from the stencil's top over the grille down through its bars, the grille in the floor and its
        # glowing boot, to the tiles
        xl = min(p[0] for p in floor_q) - 2
        xr = max(p[0] for p in floor_q) + 2
        ytop = min(p[1] for p in st_box) - 2
        ybot = fl(gx, M.CUT, M.TILE_Y)[1]
        shape = {"poly": rect_poly(xl, ytop, xr, ybot)}
        thing("grille-" + gid, f"the grille over {label}: a rectangle of slats in the duct's floor, the room's light coming up through it in bars "
              f"across the duct's back wall, its stencil {label} over it; under it its boot, glowing, down to the room",
              shape, "over-" + gid, grille={"scene": {"room": "office-room", "property": "office-property", "break": "office-breakroom", "hall": None}[gid]})
        grilles.append({"id": gid, "label": label, "mark": "over-" + gid, "floor": floor_q, "stencil": st_box,
                        "boot": rect_of(boot), "centre": fl(gx, M.WALK_Z),
                        "room": {"room": "office-room", "property": "office-property", "break": "office-breakroom", "hall": None}[gid]})
    # the intake: the run, over the duct's left end, the fan and the daylight in it
    run_x1 = int(round(V.pt(M.RUN_X[1] + M.SHELL, 300.0, M.CUT)[0])) + 3     # (the run's wall's cut band and the edge of its outside)
    thing("intake", "the intake: the duct turns up at its left end into the run to the roof; daylight at the top, from the rooftop unit's open "
          "grille; the intake fan's back in it, still (Ranger switched it off)", {"poly": rect_poly(0, 78, run_x1, marks["intake"]["at"][1] - 34)},
          "intake")
    fanr = rect_of(own("intakefan", "intakefan-hub", "intakefan-motor", "intakefan-shroud", "intakefan-struts"), 3)
    thing("intakefan", "the intake fan's back, up the run: still (Ranger switched it off)", {"rect": [max(fanr[0], 0), fanr[1], fanr[2] - max(0, -fanr[0]), fanr[3]]},
          "intake")
    # the shaft, its stencil, its fan
    sh = own("shaft-back", "shaft-right", "shaft-left", "rungs", "plate", "plate-edge", "bulb")
    sr = rect_of(sh)
    top_band = fl(400.0, M.CUT, M.DUCT_H + M.SHELL)[1]
    mouth_x = marks["shaft"]["at"][0] + 1                                # (the HALL grille's area ends at 617)
    tex, texel, bx0, by0 = __import__("office_ducts_things").STENCILS["b7"]
    tw, th = tex.shape[1] / texel, tex.shape[0] / texel
    b7 = poly_of(V.poly([(bx0, by0, M.SHAFT_Z[0]), (bx0 + tw, by0, M.SHAFT_Z[0]), (bx0 + tw, by0 - th, M.SHAFT_Z[0]), (bx0, by0 - th, M.SHAFT_Z[0])]))
    thing("shaft", "the B-7 shaft: a big clean vertical tube of galvanized steel, cut open as the duct is, from the roof down out of the bottom "
          "of the picture; rungs down its back wall, a caged bulb over the duct's mouth, the fan across it in its ring under the duct's floor",
          {"poly": [[sr[0], 78], [W - 1, 78], [W - 1, H - 1], [sh_x, H - 1], [sh_x, fl(400.0, M.CUT, 0.0)[1]], [mouth_x, fl(400.0, M.CUT, 0.0)[1]],
                    [mouth_x, fl(400.0, M.CUT, M.DUCT_H)[1]], [sh_x, fl(400.0, M.CUT, M.DUCT_H)[1]], [sh_x, top_band], [sr[0], top_band]]}, "shaft")
    xs = [p[0] for p in b7]
    ys = [p[1] for p in b7]
    thing("stencil", "the shaft's stencil, in red: B-7 EXHAUST · SOUNDPROOFED · AUTHORIZED AIR ONLY",
          {"poly": rect_poly(min(xs) - 3, min(ys) - 3, max(xs) + 3, max(ys) + 3)}, "shaft")
    fc = fan_crop
    thing("fan", "the B-7 fan across the shaft, in its plate: four broad blades, slow; it turns until the fans are switched off, and is still "
          "from then on", {"poly": rect_poly(fc[0] - 2, fc[1] - 2, fc[2] + 2, fc[3] + 2)}, "shaft", plane=["fan", "fan-stopped"])
    # the ceiling space: the pipe, the wires, the insulation
    pipe = own("pipe", "valve")
    pipe[:, sr[0]:] = False                                             # (it runs on behind the run and the shaft)
    pipe[:, :run_x1] = False
    thing("pipe", "the water pipe: copper gone brown, on hangers, a gate valve with a red handwheel", {"poly": band_poly(pipe, 24, 5)},
          stand=walk_point(400), face="N")
    wires = own("wires")
    wires[:, :run_x1] = False                                           # (it runs on behind the run and the shaft)
    wires[:, sr[0]:] = False
    thing("wires", "the bundled wires: five cables tied together, sagging between their hooks", {"poly": band_poly(wires, 16, 4)},
          stand=walk_point(380), face="N")
    ins = rect_of(own("insulation"), 2)
    thing("insulation", "pink insulation lying along the duct's top, soft and lumpy (and more of it on the tiles under the duct)", {"rect": ins},
          stand=walk_point(400), face="N")
    jx = M.JOINTS[1]
    rx = int(round(V.pt(jx, 0.0, M.DUCT_Z[0])[0]))
    thing("rivets", "the rivets: a row each side of the joint in the duct's back wall, between ROOM C and PROP & EFF (and all along the duct)",
          {"rect": [rx - 7, fl(400.0, M.DUCT_Z[0], M.DUCT_H)[1] + 1, 14, fl(400.0, M.DUCT_Z[0], 0.0)[1] - fl(400.0, M.DUCT_Z[0], M.DUCT_H)[1] - 2]},
          stand=walk_point(rx), face="N")
    batts = own("batts")
    br = rect_of(batts)
    # the forgotten things, on the tiles
    for nm, what in (("cup", "a coffee cup, forgotten on a tile: white enamel, a blue band, the coffee long dried in the bottom"),
                     ("pencil", "a pencil on a tile: yellow, chewed a little, its point sharpened"),
                     ("wrapper", "a sandwich wrapper from about 1983: waxed paper, a faded print, crumpled"),
                     ("fitting-0", "a light fitting's top, set in the tiles: white enamel gone dusty, its vents alight, the room's light round its edge")):
        m = own(nm)
        r = rect_of(m, 3)
        if r is None:
            print("layout: nothing found for", nm)
            continue
        cx = r[0] + r[2] / 2
        thing(nm if nm != "fitting-0" else "fitting", what, {"rect": r}, stand=walk_point(cx), face="S")
    # a few more, for anyone who wants them
    for nm, what, names in (("valve", "the gate valve on the pipe, its red handwheel", ("valve",)),
                            ("bulb", "a caged bulb on the shaft's wall, lit", ("bulb",)),
                            ("lifted", "a ceiling tile lifted at one edge: the room's light in the crack", ("lifted",))):
        r = rect_of(own(*names), 3)
        if r:
            thing(nm, what, {"rect": r}, stand=walk_point(r[0] + r[2] / 2), face="N" if nm != "lifted" else "S")
    # the walk: the floor's middle, from the foot of the intake run to the end of the floor over the shaft
    wx0, wx1 = M.WALK_X
    wz0, wz1 = M.WALK_ZS
    walk = [fl(wx0, wz0), fl(wx1, wz0), fl(wx1, wz1), fl(wx0, wz1)]
    # the fan's frames
    fan_at = [fan_crop[0] + fan_foot[0], fan_crop[1] + fan_foot[1]]
    rim = fl(M.FAN["at"][0], M.FAN["at"][2] + M.FAN["r"], M.FAN["at"][1])
    ifx, ify = V.pt(*M.INTAKE_FAN["at"])
    d = V.cam_space(*M.INTAKE_FAN["at"])[2]
    elev = math.atan2(M.INTAKE_FAN["at"][1] - V.eye, d)
    L = {
        "id": M.ID, "horizon": M.VIEW["horizon"], "full": M.VIEW["full"], "view": M.VIEW, "eye_cm": int(round(V.eye)),
        "vanishing": [int(round(V.vanishing()[0][0])), int(round(V.vanishing()[0][1]))],
        "minScale": 1.0, "maxScale": 1.0,
        "scale_note": ("Ranger walks the middle of the duct's floor on the row 470 = full: scale 1.0, his frames pixel for pixel. The walk "
                       "band is thin (rows 466 to 474: 0.95 to 1.03 by the camera); minScale and maxScale 1.0 hold him at exactly his "
                       "painted size anywhere on it (a frame drawn at 0.97 would lose rows)."),
        "light": ("a cut-away of the ceiling space, drawn as a section: the duct is the brightest thing, the rooms' fluorescent light (warm "
                  "white, a little green) coming up through its four grilles in bars up its back wall to its top, the boots glowing under "
                  "them; daylight down the intake run at the left from the rooftop unit; the light fittings glowing up between the tiles "
                  "(the two the cut passes through show their tubes alight, and their light falls in soft fans into the rooms under the "
                  "tiles' cut line; the ones behind the duct fan up the far wall); the B-7 shaft clean, lit from its cap and more from far "
                  "below (the way down), a caged bulb over the duct's mouth; the ceiling space dim but readable, blue-violet in its shade. "
                  "Light falls as if the cut walls were still there."),
        "fx_note": ("Nothing moves by nature here. The intake fan is painted still in the backdrop (it is never seen turning: the fans are "
                    "off from the first time Ranger is in the duct); if it is ever to turn, it is the ellipse at `intake_fan`. The B-7 fan is "
                    "the cut-out `fan` (four turning frames, then still): see `planes`. The fans' hum is a sound, not paint."),
        "walk": walk,
        "walk_note": ("the middle of the duct's floor, a thin band (Z 229 to 271 cm of its 100), from the foot of the intake run (past the "
                      "elbow's corner) to the end of the floor over the shaft. Nobody else is ever here."),
        "blocked": [],
        "planes": [
            {"id": "fan", "frames": [f"fan-{i}.png" for i in range(len(M.FAN_TURN))], "fps": 3, "at": fan_at, "foot": list(fan_foot),
             "base": rim[1], "when": "turning while the building's air is on: !office.acOff",
             "note": (f"the B-7 fan turning: four frames a sixteenth of a turn apart ({', '.join(str(a) for a in M.FAN_TURN)} degrees; four "
                      "broad blades, so the fourth leads back to the first), slow (3 a second: a quarter turn in 1.3 s). Cropped pictures, "
                      "each with the same box and foot: `at` is the fan's hub on the stage. Its base is the row of its plate's front rim "
                      "(a figure going down the shaft is behind it until below that row).")},
            {"id": "fan-stopped", "src": "fan-stopped.png", "at": fan_at, "foot": list(fan_foot), "base": rim[1],
             "when": "office.acOff (still from the first time Ranger is in the duct)",
             "note": f"the B-7 fan stopped, its blades at {M.FAN['rest']} degrees: the same box and foot as the turning frames"},
        ],
        "things": things,
        "marks": marks,
        "stands": {t["id"]: {"at": t["stand"], "face": t["face"]} for t in things},
        "grilles": grilles,
        "grille_view": {"file": "grille-view.png", "note": "what Ranger sees looking down through a grille (office_ducts_grille.py): "
                        "800 x 600, the slats over the room the engine draws under it; keyed with the Office's key as a frame"},
        "exits": [
            {"id": "intake", "to": "office-lot", "spawn_there": "intake", "how": ("up the intake run to the roof: the area `intake`; Ranger "
             "climbs up out of the top of the picture and comes out at the lot's `intake` mark (in front of the rooftop unit's open "
             "grille). Coming in from the lot he lands here at `intake`."), "stand": marks["intake"]["at"], "face": "N"},
        ],
        "intake_fan": {"at": [int(round(ifx)), int(round(ify))], "rx": int(round(M.INTAKE_FAN["r"] * V.F / d)),
                       "ry": int(round(M.INTAKE_FAN["r"] * V.F / d * math.sin(elev))), "blades": 4, "still": True},
        "lights": {
            "grilles": [fl(gx, M.WALK_Z, 2.0) for _, _, gx in M.GRILLES],
            "intake_daylight": [int(round(v)) for v in V.pt((M.INTAKE_OPEN["X"][0] + M.INTAKE_OPEN["X"][1]) / 2, 540.0, M.DUCT_Z[0] - M.SHELL)],
            "glows": [[int(round(v)) for v in V.pt(gx, 150.0, M.FAR)] for gx, gz in M.GLOWS],
            "bulb": [int(round(v)) for v in V.pt(*M.BULB["at"])],
            "note": "where the light comes from (painted): for a live glow or a flicker if wanted",
        },
        "cutouts": {"fan": [fan_crop[0], fan_crop[1], fan_crop[2] - fan_crop[0], fan_crop[3] - fan_crop[1]]},
        "rows": {"duct_top": fl(400.0, M.CUT, M.DUCT_H)[1], "floor_front": fl(400.0, M.CUT, 0.0)[1], "floor_back": fl(400.0, M.DUCT_Z[0], 0.0)[1],
                 "tiles_cut": fl(400.0, M.CUT, M.TILE_Y)[1], "plate": fl(M.FAN["at"][0], M.CUT, M.FAN["at"][1])[1],
                 "top_band": [fl(400.0, M.CUT, M.DUCT_H + M.SHELL)[1], fl(400.0, M.CUT, M.DUCT_H)[1]],
                 "floor_band": [fl(400.0, M.CUT, 0.0)[1], fl(400.0, M.CUT, -M.SHELL)[1]],
                 "note": ("the duct's inside runs from its ceiling (duct_top, at the cut) to its floor; the cut's bands are its walls seen cut, "
                          "the top's (over it the insulation) and the floor's (under it the gap down to the tiles, whose cut line is tiles_cut); "
                          "plate is the front of the fan's ring plate")},
    }
    json.dump(L, open(f"{OUT}/layout.json", "w"), indent=1)
    return L

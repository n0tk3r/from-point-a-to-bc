"""PAINT-21D: layout.json for edo-akashi, measured through the scene's camera from the same numbers the picture was
painted with (edo_akashi.py's placings), and from the finished cut-outs' pixels."""

import math

import numpy as np

from edo_akashi_kit import *
import edo_akashi as A

BOTTOM = 596


def r(p):
    return [int(round(p[0])), int(round(p[1]))]


def box_of(alpha, pad=0):
    ys, xs = np.where(alpha > 0.5)
    if len(ys) == 0:
        return [0, 0, 0, 0]
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 1 + 2 * pad, int(ys.max() - ys.min()) + 1 + 2 * pad]


def grownup(y):
    return int(round(160 * (y - HZ) / (FULL - HZ)))


def stand(p, face="N"):
    return {"at": r(p), "grownup_px": grownup(p[1]), "face": face}


def clip_frame(poly):
    """Cut a picture polygon to the stage (x 2..797, y <= BOTTOM)."""
    def side(pts, keep, cut):
        out = []
        n = len(pts)
        for i in range(n):
            p, q = pts[i], pts[(i + 1) % n]
            pin, qin = keep(p), keep(q)
            if pin:
                out.append(p)
            if pin != qin:
                out.append(cut(p, q))
        return out
    def cx(at):
        return lambda p, q: (at, p[1] + (q[1] - p[1]) * (at - p[0]) / (q[0] - p[0]))
    def cy(at):
        return lambda p, q: (p[0] + (q[0] - p[0]) * (at - p[1]) / (q[1] - p[1]), at)
    pts = side(poly, lambda p: p[0] >= 2, cx(2))
    pts = side(pts, lambda p: p[0] <= 797, cx(797))
    pts = side(pts, lambda p: p[1] <= BOTTOM, cy(BOTTOM))
    out = []
    for p in pts:
        if not out or math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) > 2.5:
            out.append(p)
    return [r(p) for p in out]


def along_edge(x0, x1, off, n=10):
    """Picture points along the water's edge from x0 to x1 (cm), `off` cm landward (+) or seaward (-)."""
    return [gp(x, edge_z(x) - off) for x in np.linspace(x0, x1, n)]


def layout(planes, info):
    # ---- the floors: the sand and the road (one); the shallows (Little Sister's alone, a step into the water)
    xl, xr = -560.0, 640.0                                                    # beyond the picture's edges at the road
    sand = [gp(xl, -60.0), gp(xr, -60.0), gp(xr, edge_z(xr) - 30.0)] + list(reversed(along_edge(-1500.0, xr, 30.0, 18))) + [gp(-1500.0, 600.0)]
    sand = clip_frame(sand)
    sx0, sx1 = -60.0, 270.0
    shallows = along_edge(sx0, sx1, -8.0, 8) + [gp(sx1, edge_z(sx1) + 150.0), gp(A.LADLE["x"] + 60, A.LADLE["z"] + 40.0), gp(A.LADLE["x"] - 70, A.LADLE["z"] + 50.0), gp(sx0, edge_z(sx0) + 120.0)]
    shallows = clip_frame(shallows)
    # ---- blocked: the pots, Heita's boat, his tub, the rocks, the pines' roots
    P_ = A.POTS
    blocked = [
        {"id": "pots", "poly": [r(gp(P_["x0"] - 20, P_["z0"] - 70)), r(gp(P_["x1"] + 20, P_["z0"] - 70)), r(gp(P_["x1"] + 20, P_["z1"] + 30)), r(gp(P_["x0"] - 20, P_["z1"] + 30))]},
    ]
    b = A.HEITA_BOAT
    (sx, sz), (bx, bz) = b["stern"], b["bow"]
    L_ = math.hypot(bx - sx, bz - sz)
    ux, uz = (bx - sx) / L_, (bz - sz) / L_
    nx, nz = -uz, ux
    w_ = b["beam"] + 30
    blocked.append({"id": "heitaboat", "poly": [r(gp(sx + nx * w_, sz + nz * w_)), r(gp(bx + ux * 30 + nx * w_, bz + uz * 30 + nz * w_)),
                                                 r(gp(bx + ux * 30 - nx * w_, bz + uz * 30 - nz * w_)), r(gp(sx - nx * w_, sz - nz * w_))]})
    t = A.TUB
    blocked.append({"id": "tub", "poly": [r(gp(t["x"] - t["r"] - 20, t["z"] - t["r"] - 15)), r(gp(t["x"] + t["r"] + 20, t["z"] - t["r"] - 15)),
                                           r(gp(t["x"] + t["r"] + 20, t["z"] + t["r"] + 15)), r(gp(t["x"] - t["r"] - 20, t["z"] + t["r"] + 15))]})
    rk = [(rx, rz, rw) for (rx, rz, rw, rh) in A.ROCKS]
    blocked.append({"id": "rocks", "poly": [r(gp(min(x - w for x, z, w in rk) - 15, min(z for x, z, w in rk) - 30)), r(gp(max(x + w for x, z, w in rk) + 15, min(z for x, z, w in rk) - 30)),
                                             r(gp(max(x + w for x, z, w in rk) + 15, max(z for x, z, w in rk) + 40)), r(gp(min(x - w for x, z, w in rk) - 15, max(z for x, z, w in rk) + 40))]})
    for p in A.PINES:
        blocked.append({"id": "pine-" + ("l" if p["x"] < 0 else "r"), "poly": [r(gp(p["x"] - 34, p["z"] - 22)), r(gp(p["x"] + 34, p["z"] - 22)), r(gp(p["x"] + 34, p["z"] + 22)), r(gp(p["x"] - 34, p["z"] + 22))]})
    # ---- marks (ROUND-21's names, and more)
    M = {
        "road": (-340.0, 56.0), "shore": (20.0, 640.0), "fusa": (-40.0, 762.0), "leader": (-232.0, 880.0), "pots": (-320.0, 208.0),
        "heita": (-206.0, 700.0), "tub": (-150.0, 548.0), "shallows": (100.0, 692.0), "ladle": (128.0, 788.0), "rocks": (300.0, 255.0),
        "sato": (-120.0, 72.0), "west": (432.0, 60.0),
        "satosister": (-56.0, 64.0), "road_mom": (-330.0, 50.0), "road_bigsis": (-380.0, 96.0), "road_lilsis": (-286.0, 14.0),
        "shoreLeft": (-560.0, 520.0),
    }
    # places that are not standing marks: where the crab hides, where two pilgrims wade (in the water, on no floor)
    PL = {"crab": (468.0, 318.0), "awapilgrim1": (-60.0, 1160.0), "awapilgrim2": (70.0, 1060.0)}
    faces = {"road": "E", "shore": "N", "fusa": "S", "leader": "S", "pots": "W", "heita": "E", "tub": "N", "shallows": "N", "ladle": "N",
             "rocks": "E", "sato": "W", "west": "W", "satosister": "W", "road_mom": "E", "road_bigsis": "E", "road_lilsis": "E", "shoreLeft": "N"}
    marks = {k: r(gp(x, z)) for k, (x, z) in M.items()}
    stands = {k: stand(gp(x, z), faces[k]) for k, (x, z) in M.items()}
    stands["ladle"]["floor"] = "shallows"
    stands["ladle"]["note"] = "in the shallows, 22 cm of water: Little Sister's boots are in it to their tops (PEOPLE-21B's wading pose or overlay)"
    places = {k: {"at": r(gp(x, z)), "grownup_px": grownup(gp(x, z)[1])} for k, (x, z) in PL.items()}
    places["crab"]["note"] = "under the nearest rock's foot, by the pool: where Mom reaches in (stand at `rocks`)"
    places["awapilgrim1"]["note"] = places["awapilgrim2"]["note"] = "wading ashore from the boat (in the water, on no floor: they wade by script, their legs in the water to the knee)"
    # ---- the cut-outs, back to front with nobody there, their bases and states
    def base_row(x, z):
        return int(round(gp(x, z)[1]))
    pb = A.PBOAT_IN
    pbb = A.PBOAT_BEACHED
    planes_out = [
        {"id": "floats", "file": "floats.png", "plane": "back", "what": "the floats of the octopus pots' lines in the shallows (they bob: fx floats-bob)"},
        {"id": "ladle", "file": "ladle.png", "plane": "back", "what": "O-Fusa's ladle afloat among the pots' lines, its bowl up: the octopus sits in it (PEOPLE-21B's sprite, at `octopus`); hidden once Little Sister has it (it bobs: fx ladle-bob)",
         "states": {"afloat": "ladle.png", "gone": None}},
        {"id": "pilgrimboat", "file": "pilgrimboat.png", "base": base_row(pb["x"], pb["z"] - 10),
         "states": {"coming in": "pilgrimboat.png", "beached": "pilgrimboat-beached.png"},
         "what": "the Awa pilgrims' boat, sail down: coming in (afloat in the strait, where its approach stops: fx boat-approach), then beached (its bow on the sand, at the water's edge further left); the beached one's base is its own",
         "beached_base": base_row(pbb["x"], pbb["z"] - 20)},
        {"id": "heitaboat", "file": "heitaboat.png", "base": [r(gp(sx - nx * 10, sz - nz * 10)), r(gp(bx - nx * 10, bz - nz * 10))],
         "what": "old Heita's boat drawn up on the sand along the shore; whoever is beyond it is behind it"},
        {"id": "tub", "file": "tub.png", "base": base_row(t["x"], t["z"] + t["r"]), "what": "Heita's tub (the octopus goes in it)"},
        {"id": "pots", "file": "pots.png", "base": base_row(P_["x0"], P_["z0"] - 40), "what": "the octopus pots stacked on the sand in rows (clay bells)"},
        {"id": "rocks", "file": "rocks.png", "base": base_row(430.0, 300.0), "what": "the rocks at the water's edge at the right, with pools among them (the crab's place)"},
        {"id": "pine-l", "file": "pine-l.png", "base": base_row(A.PINES[0]["x"], A.PINES[0]["z"]), "what": "a shore pine at the road's edge, bent by the wind (it stirs: fx pine-l-sway)"},
        {"id": "pine-r", "file": "pine-r.png", "base": base_row(A.PINES[1]["x"], A.PINES[1]["z"]), "what": "a shore pine at the road's edge (it stirs: fx pine-r-sway)"},
        {"id": "front", "file": "front.png", "plane": "front", "what": "tufts of shore grass at the road's edge, bottom left and right"},
    ]
    cutouts = {n: box_of(planes[n][1]) for n in list(A.ORDER) + ["pilgrimboat-beached"]}
    # ---- things (ROUND-21's list, each with a shape)
    def person_rect(p, cm):
        px_ = 160 * (p[1] - HZ) / (FULL - HZ) * cm / 175.0
        return [int(round(p[0] - px_ * 0.18)), int(round(p[1] - px_)), int(round(px_ * 0.36)), int(round(px_))]
    lad = info["ladle"]
    awaji = [[212, 262], [236, 258], [320, 248], [440, 238], [560, 236], [690, 234], [800, 226], [800, 263], [212, 263]]
    things = [
        {"id": "strait", "what": "the strait, four kilometres across to Awaji, the tide running hard (lines on the water)", "shape": {"poly": [[160, 263], [800, 263], [800, 480], [600, 470], [420, 436], [300, 418], [200, 398], [140, 380], [100, 330]]},
         "stand": marks["shore"], "face": "N"},
        {"id": "awaji", "what": "Awaji Island across the strait, long and low", "shape": {"poly": awaji}, "stand": marks["shore"], "face": "N"},
        {"id": "castle", "what": "Akashi castle on its hill: white corner turrets, and no keep", "shape": {"rect": info["castle_box"]}, "stand": marks["shoreLeft"], "face": "N"},
        {"id": "pilgrimboat", "what": "the Awa pilgrims' boat, sail down (coming in / beached)", "shape": {"rect": box_of(planes["pilgrimboat"][1], 3)}, "stand": marks["shore"], "face": "N",
         "beached": {"rect": box_of(planes["pilgrimboat-beached"][1], 3)}},
        {"id": "pilgrims", "what": "Awa pilgrims wading ashore with their banners and ladles (drawn by the game)", "shape": {"rect": [places["awapilgrim1"]["at"][0] - 40, places["awapilgrim2"]["at"][1] - 70, 110, 80]}, "stand": marks["shore"], "face": "N"},
        {"id": "banner", "what": "the group's banner, on the leader's pole (the leader's sprite carries it: PEOPLE-21B)", "shape": {"rect": [marks["leader"][0] - 14, marks["leader"][1] - 120, 30, 60]}, "stand": marks["fusa"], "face": "N"},
        {"id": "ladlething", "what": "the ladle afloat among the pots' lines, with the octopus in its bowl (afloat / gone)", "shape": {"rect": box_of(planes["ladle"][1], 6)}, "stand": marks["shallows"], "face": "N",
         "octopus": lad["bowl"]},
        {"id": "pots", "what": "octopus pots stacked on the sand: clay bells", "shape": {"rect": box_of(planes["pots"][1], 2)}, "stand": marks["pots"], "face": "N"},
        {"id": "potlines", "what": "the pots' lines and floats in the shallows", "shape": {"poly": [r(gp(-280.0, 1270.0)), r(gp(340.0, 690.0)), r(gp(360.0, 740.0)), r(gp(-240.0, 1330.0))]}, "stand": marks["shallows"], "face": "N"},
        {"id": "heitaboat", "what": "old Heita's boat drawn up on the sand", "shape": {"rect": box_of(planes["heitaboat"][1], 2)}, "stand": marks["heita"], "face": "W"},
        {"id": "tub", "what": "Heita's tub", "shape": {"rect": box_of(planes["tub"][1], 3)}, "stand": marks["tub"], "face": "N"},
        {"id": "rocks", "what": "the rocks at the water's edge, pools among them", "shape": {"rect": box_of(planes["rocks"][1], 3)}, "stand": marks["rocks"], "face": "E"},
        {"id": "pines", "what": "the shore pines along the road, bent by the wind", "shape": {"poly": [[0, 0], [380, 0], [380, 160], [210, 200], [120, 530], [0, 540]]}, "stand": marks["road"], "face": "N",
         "also": {"rect": box_of(planes["pine-r"][1])}},
        {"id": "sand", "what": "white sand", "shape": {"poly": [[0, 540], [0, 360], [90, 330], [200, 400], [400, 440], [600, 470], [800, 486], [800, 540]]}, "stand": marks["shore"], "face": "S"},
        {"id": "road", "what": "the Saigoku-kaido, behind the pines, east (left) to west (right)", "shape": {"poly": [r(gp(-560, -60)), r(gp(560, -60)), r(gp(560, 150)), r(gp(-560, 150))]}, "stand": marks["sato"], "face": "W"},
    ]
    things = [dict(t, shape={"poly": clip_frame([tuple(p) for p in t["shape"]["poly"]])}) if "poly" in t["shape"] else t for t in things]
    people = [("fusa", 125), ("leader", 156), ("heita", 156), ("sato", 146), ("satosister", 146), ("awapilgrim1", 156), ("awapilgrim2", 146)]
    whats = {"fusa": "O-Fusa, nine, an Awa girl, in tears by the water's edge", "leader": "her group's leader, with the banner", "heita": "old Heita, by his boat",
             "sato": "O-Sato, a Harima woman with a ladle, going east along the road", "satosister": "her sister-in-law, with a ladle",
             "awapilgrim1": "an Awa pilgrim wading ashore", "awapilgrim2": "an Awa pilgrim wading ashore"}
    for k, cm in people:
        at_ = marks[k] if k in marks else places[k]["at"]
        things.append({"id": k, "what": whats[k] + " (drawn by the game)", "shape": {"rect": person_rect(at_, cm)}, "stand": marks["shore"] if k in ("fusa", "leader", "awapilgrim1", "awapilgrim2") else marks["road"] if k in ("sato", "satosister") else marks["heita"], "face": "N"})
    # ---- fx: what moves (the engine draws it)
    edge_band = along_edge(-1500.0, 700.0, -10.0, 16) + list(reversed(along_edge(-1500.0, 700.0, -380.0, 16)))
    edge_band = clip_frame(edge_band)
    bf = info["boat_frame"]
    fx = [
        {"id": "shore-waves", "type": "waves", "what": "small waves running in on the sand at the water's edge (ENGINE-20's waves kind)", "area": edge_band,
         "holes": [box_to_poly(box_of(planes["ladle"][1], 4)), box_to_poly(box_of(planes["pilgrimboat"][1], 2))], "rows": 6, "per": 9, "color": "#f6eed8", "opacity": 0.55, "size": 9, "speed": 7, "toward": "S", "life": 3.0, "plane": "back"},
        {"id": "strait-shimmer", "type": "shimmer", "what": "the afternoon sun on the strait: glints, thickest to the right (the sun's side)", "poly": [[260, 266], [800, 264], [800, 330], [300, 320]],
         "count": 34, "size": 5, "flow": [-6, 0], "life": 1.6, "color": "#f6eed8", "opacity": 0.55, "plane": "back",
         "note": "the tide runs east to west here (flow leftward); the far tide lines are painted still"},
        {"id": "pine-l-sway", "type": "sway", "plane": "pine-l", "anchor": "bottom", "amount": 1.2, "period": 5.5, "wave": 40, "lean": 0.3, "what": "the left pine's crown stirring in the sea wind"},
        {"id": "pine-r-sway", "type": "sway", "plane": "pine-r", "anchor": "bottom", "amount": 1.0, "period": 6.0, "wave": 40, "lean": 0.3, "what": "the right pine's crown stirring"},
        {"id": "ladle-bob", "type": "bob", "plane": "ladle", "amount": 0.5, "period": 4.0, "what": "the ladle riding the little waves (the octopus sprite rides with it: offset it by the same)"},
        {"id": "floats-bob", "type": "bob", "plane": "floats", "amount": 1, "period": 4.5, "what": "the floats of the pots' lines"},
        {"id": "boat-bob", "type": "bob", "plane": "pilgrimboat", "amount": 1, "period": 5.5, "tilt": 0.8, "what": "the Awa boat riding where it has stopped (coming in)"},
        {"id": "gulls", "type": "birds", "kind": "flyers", "plane": "back", "what": "gulls over the strait (the engine's own silhouettes)",
         "lanes": [[[-12, 200], [180, 186], [360, 204], [560, 180], [812, 196]], [[812, 150], [600, 170], [420, 152], [200, 176], [-12, 160]]], "every": [8, 16], "group": [1, 3], "speed": 55, "size": 8, "scale": [0.6, 1.0], "color": "#f6eed8"},
        {"id": "boat-approach", "type": "birds", "kind": "flyers", "what": "PROPOSED: the Awa boat's approach, a flyer that stops: it comes in from far out along the lane, growing with the depth, and stops where the cut-out `pilgrimboat` stands (then the cut-out shows and this goes)",
         "frames": {"foot": bf["foot"], "sizeAt": bf["at"][1], "glide": ["boat-1.png"]}, "lane": [r(gp(-40.0, 9000.0)), bf["at"]], "speed": 6, "stop": bf["at"],
         "note": "ENGINE-21's 'flyer that stops'; boat-1.png is the coming-in cut-out cropped (box " + str(bf["box"]) + "), its foot the point under its bow"},
    ]
    out = {
        "id": "edo-akashi", "horizon": HZ, "full": FULL,
        "view": {"horizon": HZ, "full": FULL, "camera": "persp.Camera(262, 590): eye 359 cm, Z0 875, focal 800, vanishing x 400",
                 "place": "the road z -60..150 (cm from the full row), the pines' roots at z 170; the water's edge from far at the left to z ~420 at the right (edo_akashi_kit.EDGE)"},
        "light": "afternoon, the sun in the west, to the right and a little ahead, 35 degrees up: faces turned to the right are lit; shadows fall to the left and a little toward us, flat and blue",
        "walk": sand,
        "walk_floors": [
            {"name": "sand", "area": sand, "note": "the road and the white sand down to the water's edge"},
            {"name": "shallows", "area": shallows, "note": "the shallows: from the water's edge a step out to the ladle among the pots' lines; Little Sister alone may wade (her yellow boots: 'Boots are for WATER.'); 22 cm of water at the ladle, to her boot tops",
             "away": {"any": "(the scene's line: nobody in sandals wants to wade)"}, "depth_cm": {"at_edge": 0, "at_ladle": 22}},
        ],
        "blocked": blocked,
        "planes": planes_out, "cutouts": cutouts,
        "things": things,
        "marks": marks, "stands": stands, "places": places,
        "octopus": {"at": lad["bowl"], "note": "the octopus sits in the ladle's bowl (PEOPLE-21B's sprite): put its foot here, at the size of the ladle's row; it rides fx ladle-bob"},
        "fx": fx,
        "frames": {"boat-1.png": {"foot": bf["foot"], "box": bf["box"], "what": "the Awa boat coming in, for its approach"}},
        "exits": {"east": {"at": marks["road"], "note": "the road east: refuses ('Three days of that. No.')"}, "west": {"at": marks["west"], "note": "west to Himeji only by the card, once #35 is done"}},
        "heights": {"mom_cm": 168, "bigsis_cm": 160, "lilsis_cm": 122, "man_1830_cm": 156, "woman_1830_cm": 146, "fusa_cm": 125, "grownup_at_full_px": 160},
        "notes": "PAINT-21D. Checked: the castle with no keep (four three-storey corner turrets), the strait about 4 km to Awaji with a fast tide, white sand and green pines, octopus caught in clay pots on lines, Awa pilgrims landing by boat, the ladle, the road behind the pines. Invented: this stretch of shore, the rocks, Heita's boat and tub, the bearings of the view (the castle placed at the far left, Awaji to the right), the Awa boat's look.",
    }
    return out


def box_to_poly(b):
    x, y, w, h = b
    return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]

"""PAINT-21C: layout.json for edo-street, measured through the scene's camera from the numbers the picture was painted
with (edo_street.py, edo_street_things.py), and from the finished cut-outs' pixels."""

import numpy as np

from edo_dojima_kit import rp, box_of, stand, person_rect
import edo_street as S
import edo_street_things as T

CAM, g = S.CAM, S.g


def line_base(X0, X1, Z):
    return [rp(g(X0, Z)), rp(g(X1, Z))]


def poly_xz(pts):
    return [rp(g(X, Z)) for X, Z in pts]


def edge_X(x, Z):
    lo, hi = -6000.0, 8000.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if g(mid, Z)[0] < x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _pad(r, p):
    return [r[0] - p, r[1] - p, r[2] + 2 * p, r[3] + 2 * p]


def layout(planes, extra, info):
    ZE = S.ZE
    Zw = ZE + 55                                               # the walk's far edge: clear of the gutter before the fronts
    bottom_l = CAM.floor_at(0, 596)
    bottom_r = CAM.floor_at(800, 596)
    xl, xr = edge_X(0, Zw), edge_X(800, Zw)
    walk = [[0, 596], [800, 596], [800, int(round(g(xr, Zw)[1]))]]
    walk += poly_xz([(X, Zw) for X in np.linspace(xr, S.CROSS[1] - 20, 5)])
    walk += poly_xz([(S.CROSS[1] - 40, ZE - 30), (S.CROSS[1] - 60, ZE - 650), (S.CROSS[0] + 60, ZE - 650), (S.CROSS[0] + 40, ZE - 30)])
    walk += poly_xz([(X, Zw) for X in np.linspace(S.CROSS[0] + 20, xl, 4)])
    walk += [[0, int(round(g(xl, Zw)[1]))]]
    sg, rg, vd = T.SIGN, T.ROADGOD, T.VENDOR
    blocked = [
        poly_xz([(sg["X"] - 34, sg["Z"] + 14), (sg["X"] + 34, sg["Z"] + 14), (sg["X"] + 34, sg["Z"] - 14), (sg["X"] - 34, sg["Z"] - 14)]),       # the signboard's feet
        poly_xz([(rg["X"] - 30, rg["Z"] + 30), (rg["X"] + 30, rg["Z"] + 30), (rg["X"] + 30, rg["Z"] - 25), (rg["X"] - 30, rg["Z"] - 25)]),       # the road god
        poly_xz([(vd["X"] - 70, vd["Z"] + 22), (vd["X"] + 70, vd["Z"] + 22), (vd["X"] + 70, vd["Z"] - 30), (vd["X"] - 70, vd["Z"] - 30)]),       # the water-seller and his buckets
    ]
    M = {
        "shore": (edge_X(14, -1110), -1110), "crossroads": (560.0, -1175.0), "roadgod": (350.0, -1196.0), "natsu": (418.0, -1214.0),
        "prints": (20.0, -1214.0), "bench": (206.0, -1222.0), "medicine": (1130.0, -1200.0), "combshop": (1345.0, -1125.0),
        "yomiuriFrom": (520.0, -1880.0), "yomiuriTo": (612.0, -1190.0), "yomiuri2From": (640.0, -1925.0), "yomiuri2To": (690.0, -1215.0),
        "kurataFrom": (edge_X(788, -1120), -1120), "kurataTo": (780.0, -1150.0), "tatsuFrom": (edge_X(788, -1060), -1060), "tatsuTo": (850.0, -1110.0),
        "komuso": (935.0, -1222.0), "theatre": (edge_X(786, -1150), -1150),
        "shore_mom": (edge_X(40, -1150), -1150), "shore_bigsis": (edge_X(64, -1100), -1100), "shore_lilsis": (edge_X(30, -1060), -1060),
        "kelpshop": (930.0, -1196.0), "watervendor": (1215.0, -1065.0),
    }
    marks = {k: rp(g(*v)) for k, v in M.items()}
    # Senzo sits on the raised floor behind his bench (45 cm up): his mark is the point under him on that floor; the
    # game's size for him is that of a man standing on the street at his depth (`senzo_scale`), with feet on that floor
    sz = (206.0, -1378.0)
    p_floor = g(sz[0], sz[1], S.BENCH["floor"])
    p_ground = g(sz[0], sz[1])
    marks["senzo"] = rp(p_floor)
    senzo_scale = round((p_ground[1] - S.HZ) / (S.FULL - S.HZ), 3)
    faces = {"shore": "E", "crossroads": "N", "roadgod": "N", "natsu": "N", "prints": "N", "bench": "N", "medicine": "N", "combshop": "N",
             "yomiuriFrom": "S", "yomiuriTo": "S", "yomiuri2From": "S", "yomiuri2To": "S", "kurataFrom": "W", "kurataTo": "W", "tatsuFrom": "W",
             "tatsuTo": "W", "komuso": "N", "theatre": "E", "shore_mom": "E", "shore_bigsis": "E", "shore_lilsis": "E", "kelpshop": "N",
             "watervendor": "N", "senzo": "S"}
    stands = {k: stand(CAM, v, faces[k]) for k, v in marks.items()}
    stands["senzo"] = {"at": marks["senzo"], "grownup_px": int(round(160 * senzo_scale)), "face": "S", "scale": senzo_scale,
                       "note": "on the raised floor, 45 cm up: draw him at `scale` (a man at his depth), feet at `at`, behind the bench (whose base is in front of him)"}
    cut = {k: box_of(v[1]) for k, v in planes.items()}
    front_b = line_base(-120.0, 400.0, ZE + 8)
    bench_b = line_base(S.BENCH["X0"] - 20, S.BENCH["X1"] + 20, S.BENCH["Z1"] + 2)
    planes_out = [
        {"id": "prints-1", "file": "prints-1.png", "base": front_b, "what": "the upper line of prints pegged across the print shop's open front: actor prints (stars at home, a stage scene) and a toy print (it flutters: fx prints-1-sway)"},
        {"id": "prints-2", "file": "prints-2.png", "base": front_b, "what": "the lower line: toy prints to cut out and build, and actor prints (fx prints-2-sway)"},
        {"id": "noren-kelp", "file": "noren-kelp.png", "base": line_base(S.KELP["X0"], S.KELP["X1"], ZE + 6), "what": "the kelp shop's noren across its open front (fx noren-kelp-sway)"},
        {"id": "noren-med", "file": "noren-med.png", "base": line_base(S.MED["X0"], S.MED["X1"], ZE + 6), "what": "the medicine shop's noren in its doorway (fx noren-med-sway)"},
        {"id": "noren-comb", "file": "noren-comb.png", "base": line_base(S.COMB["X0"], S.COMB["X1"], ZE + 6), "what": "the comb-maker's noren (fx noren-comb-sway)"},
        {"id": "bench", "file": "bench.png", "base": bench_b, "what": "the printing bench at the edge of the raised floor: paper, the block with its two marks, the round pad, brushes, the pot of the new blue, the stand at its right end (Senzo sits behind it: mark `senzo`; Big Sister stands before it: mark `bench`)"},
        {"id": "print", "file": "print.png", "base": [[p[0], p[1] + 0.2] for p in bench_b], "states": {"blank": "print.png", "ghost": "print-ghost.png", "clean": "print-clean.png"},
         "what": "the sheet on the bench's stand: blank, then a ghost-blurred blue (the blue a hair to the left), then a clean print (an actor at home in a robe of the new blue): #30's three states", "order": "after bench"},
        {"id": "sign", "file": "sign.png", "base": line_base(T.SIGN["X"] - 40, T.SIGN["X"] + 40, T.SIGN["Z"] + 4), "what": "the medicine shop's big standing signboard: 'Uruyusu' (ウルユス) in our own brush hand, white on black lacquer"},
        {"id": "roadgod", "file": "roadgod.png", "base": line_base(T.ROADGOD["X"] - 30, T.ROADGOD["X"] + 30, T.ROADGOD["Z"] + 20), "what": "the small stone road god at the corner, a cup of water before it, in the band of sun"},
        {"id": "watervendor", "file": "watervendor.png", "base": line_base(T.VENDOR["X"] - 70, T.VENDOR["X"] + 70, T.VENDOR["Z"] + 20), "what": "a water-seller resting his two buckets by the comb-maker's (painted)"},
    ]
    bx = extra["bench"]
    st = bx["stand"]
    pr = S.PRINT
    things = [
        {"id": "roofs", "what": "the roofs of the street, grey-blue tiles, and the town's roofs beyond", "shape": {"rect": [0, 120, 800, 70]}, "stand": marks["crossroads"], "face": "N"},
        {"id": "firetower", "what": "a fire-watch tower on the town office's roof down the cross street", "shape": {"rect": _pad(info["fire"], 2)}, "stand": marks["crossroads"], "face": "N"},
        {"id": "kelpshop", "what": "the kelp shop on the corner across the cross street: dried kelp hung in bundles and stacked", "shape": {"poly": [rp(p) for p in info["kelp"]["front"]]}, "stand": marks["kelpshop"], "face": "N"},
        {"id": "printshop", "what": "Senzo's print shop on the corner, a publisher's: its front open to the street", "shape": {"poly": [rp(p) for p in info["print"]["front"]]}, "stand": marks["prints"], "face": "N"},
        {"id": "printlines", "what": "actor prints pegged on lines across the open front", "shape": {"rect": _pad(cut["prints-1"], 2)}, "stand": marks["prints"], "face": "N"},
        {"id": "toyprints", "what": "toy prints, to cut out and build", "shape": {"rect": _pad(cut["prints-2"], 2)}, "stand": marks["prints"], "face": "N"},
        {"id": "bench", "what": "the printing bench in the open front (its three clicks for #30: the corner mark, the side mark, the pad)", "shape": {"rect": _pad(cut["bench"], 2)}, "stand": marks["bench"], "face": "N"},
        {"id": "blocks", "what": "the block on the bench, cherry wood; at its near edge the two marks: the corner (an L) and the straight one", "shape": {"rect": [int(bx["corner"][0]) - 4, int(bx["corner"][1]) - 10, int(bx["side"][0] - bx["corner"][0]) + 14, 16]}, "stand": marks["bench"], "face": "N"},
        {"id": "cornermark", "what": "the corner mark cut at the block's edge (#30, first click)", "shape": {"rect": [int(bx["corner"][0]) - 6, int(bx["corner"][1]) - 8, 14, 12]}, "stand": marks["bench"], "face": "N"},
        {"id": "sidemark", "what": "the straight mark along the block's edge (#30, second click)", "shape": {"rect": [int(bx["side"][0]) - 7, int(bx["side"][1]) - 8, 14, 12]}, "stand": marks["bench"], "face": "N"},
        {"id": "baren", "what": "the round rubbing pad (#30, the third click: Senzo's rub)", "shape": {"rect": [int(bx["pad"][0]) - 8, int(bx["pad"][1]) - 7, 16, 12]}, "stand": marks["bench"], "face": "N"},
        {"id": "bluepot", "what": "the pot of the new blue (Berlin blue)", "shape": {"rect": [int(bx["pot"][0]) - 6, int(bx["pot"][1]) - 7, 12, 11]}, "stand": marks["bench"], "face": "N"},
        {"id": "printsheet", "what": "the sheet on the bench's stand (blank / ghost-blurred / clean)", "shape": {"rect": [int(st[0] - st[2] / 2) - 2, int(st[1] - st[3]) - 2, int(st[2]) + 4, int(st[3]) + 4]}, "stand": marks["bench"], "face": "N"},
        {"id": "medicine", "what": "the medicine shop's big signboard: 'Uruyusu'", "shape": {"rect": _pad(cut["sign"], 2)}, "stand": marks["medicine"], "face": "N"},
        {"id": "combsign", "what": "the comb-maker's signboard, shaped like a comb", "shape": {"rect": _pad(info["combsign"], 2)}, "stand": marks["combshop"], "face": "N"},
        {"id": "crossroads", "what": "the crossroads: four ways", "shape": {"poly": poly_xz([(S.CROSS[0], ZE + 300), (S.CROSS[1], ZE + 300), (S.CROSS[1], ZE - 500), (S.CROSS[0], ZE - 500)])}, "stand": marks["crossroads"], "face": "N"},
        {"id": "roadgod", "what": "the small stone road god at the corner", "shape": {"rect": _pad(cut["roadgod"], 3)}, "stand": marks["roadgod"], "face": "N"},
        {"id": "noren", "what": "the shops' noren stirring", "shape": {"rect": _pad(cut["noren-kelp"], 2)}, "stand": marks["kelpshop"], "face": "N"},
        {"id": "drumtower", "what": "far off over the roofs at the right, a theatre's drum tower (the way there)", "shape": {"rect": _pad(info["drum"], 2)}, "stand": marks["theatre"], "face": "E"},
        {"id": "watervendor", "what": "a water-seller with his two buckets", "shape": {"rect": _pad(cut["watervendor"], 2)}, "stand": marks["watervendor"], "face": "N"},
    ]
    people = [("natsu", "natsu", 146, "O-Natsu at the crossroads with her boxwood comb"), ("yomiuri1", "yomiuriTo", 156, "the first broadsheet seller (when they come)"),
              ("yomiuri2", "yomiuri2To", 156, "the second broadsheet seller"), ("kurata", "kurataTo", 156, "Kurata, round the other corner"),
              ("tatsu", "tatsuTo", 156, "Tatsu, his thief-taker"), ("komuso", "komuso", 156, "the komuso, playing at a door")]
    for pid, mk, cm, what in people:
        things.append({"id": pid, "what": what + " (drawn by the game)", "shape": {"rect": person_rect(CAM, marks[mk], cm)}, "stand": marks["crossroads"], "face": "N", "height_cm": cm, "mark": mk})
    sc = senzo_scale * 156 / 175 * 160 * 0.72                 # seated: about 0.72 of his standing height shows
    things.append({"id": "senzo", "what": "Senzo at his bench, inside the open front (drawn by the game, seated)", "shape": {"rect": [marks["senzo"][0] - int(sc * 0.25), marks["senzo"][1] - int(sc), int(sc * 0.5), int(sc)]},
                   "stand": marks["bench"], "face": "N", "height_cm": 156, "mark": "senzo"})
    fx = [
        {"id": "prints-1-sway", "type": "sway", "plane": "prints-1", "anchor": "top", "amount": 1.2, "period": 2.6, "wave": 18, "lean": 0.2, "what": "the upper line of prints fluttering"},
        {"id": "prints-2-sway", "type": "sway", "plane": "prints-2", "anchor": "top", "amount": 1.0, "period": 3.1, "wave": 16, "lean": 0.2, "what": "the lower line fluttering"},
        {"id": "noren-kelp-sway", "type": "sway", "plane": "noren-kelp", "anchor": "top", "amount": 1.6, "period": 3.4, "wave": 24, "lean": 0.3, "what": "the kelp shop's noren stirring"},
        {"id": "noren-med-sway", "type": "sway", "plane": "noren-med", "anchor": "top", "amount": 1.8, "period": 3.8, "wave": 24, "lean": 0.3, "what": "the medicine shop's noren stirring"},
        {"id": "noren-comb-sway", "type": "sway", "plane": "noren-comb", "anchor": "top", "amount": 1.6, "period": 3.0, "wave": 22, "lean": 0.3, "what": "the comb-maker's noren stirring"},
        {"id": "birds", "type": "birds", "kind": "flyers", "plane": "back", "what": "two birds wheeling high over the roofs (the engine's own silhouettes)", "circle": {"at": [470, 70], "r": [70, 24]}, "count": 2, "speed": 12, "size": 9, "color": "#3a3a4a"},
    ]
    out = {
        "id": "edo-street", "horizon": S.HZ, "full": S.FULL,
        "view": {"horizon": S.HZ, "full": S.FULL, "camera": "room.View(262, 590, cam=(0, 0), yaw=25, focal=800): eye 358.75 cm; we look east, a little south, across the street",
                 "world": "cm; X along the main street to the right (south), Z toward us (west), Y up; the far fronts Z -1300, our side's (unseen) Z -650; the cross street X 330..790"},
        "light": "about half past four, the sun west-south-west behind us and to the right, 27 degrees up: the far fronts lit from about 1.8 m up; the street and the fronts below that in our side's shadow (cool blue), but for the band of sun that comes through the cross street across the street to the crossroads, the road god and the print shop's corner and bench",
        "walk": walk, "walk_note": "one area: the main street from the bottom to just before the far side's gutter, and the mouth of the cross street; the shops' fronts are hotspots, not walked into",
        "blocked": blocked, "planes": planes_out, "cutouts": cut,
        "states": {"print": ["print", "print-ghost", "print-clean"]},
        "things": things, "marks": marks, "stands": stands, "fx": fx,
        "fx_note": "the two lines of prints and the three noren sway; two birds wheel high; the people's life (passers-by, a few pilgrims with ladles) is the game's",
        "notes": [
            "The shop signs carry the shape of writing in our own hand, never a real shop's name; the medicine signboard reads Uruyusu (ウルユス) in katakana written in our own plain strokes.",
            "Which way is south: the painting does not say; the street goes on to the right, and the drum tower is over the roofs that way (the design's 'the street goes south').",
            "#30's three clicks: things `cornermark`, `sidemark`, `baren` (small: generous hotspots round them are the scene's); the sheet's three states are `print`'s.",
            "The town office with the fire-watch tower is down the cross street (on its south side), its tower over the roofs.",
        ],
        "heights": {"mom_cm": 168, "bigsis_cm": 160, "lilsis_cm": 122, "man_1830_cm": 156, "woman_1830_cm": 146, "grownup_at_full_px": 160},
    }
    return out

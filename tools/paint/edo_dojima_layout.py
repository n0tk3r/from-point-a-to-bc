"""PAINT-21C: layout.json for edo-dojima, measured through the scene's camera from the same numbers the picture was
painted with (edo_dojima.py, edo_dojima_things.py), and from the finished cut-outs' pixels."""

import numpy as np

from edo_dojima_kit import rp, box_of, stand, person_rect
import edo_dojima as D
import edo_dojima_things as T

CAM, g = D.CAM, D.g


def line_base(X0, X1, Z):
    """A slanted base: the line where a thing's front meets the street (lines across the river recede to the left)."""
    return [rp(g(X0, Z)), rp(g(X1, Z))]


def poly_xz(pts):
    return [rp(g(X, Z)) for X, Z in pts]


def edge_X(x, Z):
    """The world X at which a line of constant Z meets picture column x."""
    lo, hi = -6000.0, 6000.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if g(mid, Z)[0] < x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def layout(planes, extra, info, meta):
    H_ = D.HOUSE
    # ---------------------------------------------------------------- the walk: the street, from the bottom to the house
    # fronts and the bank's lip (clear of the coping), one area
    lipZ = D.LIP_Z + 60
    xr = edge_X(800, lipZ)
    walk = [[0, 596], [800, 596]]
    walk += [[800, int(round(g(xr, lipZ)[1]))]]
    walk += poly_xz([(X, lipZ) for X in np.linspace(xr, H_["X1"] + 15, 6)])
    walk += poly_xz([(H_["X1"] + 15, H_["Zf"] + 15), (H_["X0"] - 5, H_["Zf"] + 15), (H_["X0"] - 5, D.NEIGH["Zf"] + 15)])
    xl = edge_X(0, D.NEIGH["Zf"] + 15)
    walk += [[0, int(round(g(xl, D.NEIGH["Zf"] + 15)[1]))]]
    # ---------------------------------------------------------------- blocked ground
    blocked = [
        poly_xz([(-828, -1218), (-350, -1218), (-350, -1314), (-828, -1314)]),                    # the stall: sandals, hearth, table, kettle
        poly_xz([(D.BALES[0] - 10, H_["Zf"]), (D.BALES[1] + 10, H_["Zf"]), (D.BALES[1] + 10, H_["Zf"] + 88), (D.BALES[0] - 10, H_["Zf"] + 88)]),   # the bales
        poly_xz([(-140, -1415), (420, -1415), (420, -1560), (-140, -1560)]),                         # the dealers and the water men
        poly_xz([(-130, -1352), (-68, -1352), (-68, -1415), (-130, -1415)]),                         # the spare buckets
        poly_xz([(30, -820), (390, -820), (390, -980), (30, -980)]),                                 # the front plane's bales and bucket
    ]
    # ---------------------------------------------------------------- marks (ROUND-21's names, and a few more)
    M = {
        "landing": (-160, -1438), "stall": (-640, -1150), "natsu": (-382, -1372), "pot": (-652, -1372), "balls": (-541, -1368), "pickle": (-452, -1364),
        "line1": (-540, -1158), "line2": (-468, -1068), "line3": (-392, -978), "line4": (-308, -888), "kyuhachi": (-212, -938),
        "market": (175, -1290), "rihei": (214, -1392), "watermen": (-36, -1330),
        "kurataFrom": (edge_X(784, -1180), -1180), "kurataTo": (-338, -1162), "town": (edge_X(788, -1090), -1090),
        "landing_mom": (-160, -1438), "landing_bigsis": (-290, -1425), "landing_lilsis": (-230, -1378),
        "tatsuFrom": (edge_X(770, -1105), -1105), "tatsuTo": (-262, -1110), "steps": (-160, -1470),
    }
    marks = {k: rp(g(*v)) for k, v in M.items()}
    faces = {"landing": "S", "stall": "E", "natsu": "S", "pot": "S", "balls": "S", "pickle": "S", "line1": "N", "line2": "N", "line3": "N", "line4": "N",
             "kyuhachi": "W", "market": "N", "rihei": "S", "watermen": "N", "kurataFrom": "W", "kurataTo": "W", "town": "E",
             "landing_mom": "S", "landing_bigsis": "S", "landing_lilsis": "S", "tatsuFrom": "W", "tatsuTo": "W", "steps": "N"}
    stands = {k: stand(CAM, v, faces[k]) for k, v in marks.items()}
    # ---------------------------------------------------------------- the cut-outs, back to front
    cut = {k: box_of(v[1]) for k, v in planes.items()}
    stall_b = line_base(-780, -340, -1228)
    planes_out = [
        {"id": "lighter", "file": "lighter.png", "base": line_base(-420, 60, D.LIP_Z), "what": "a lighter moored off the foot of the steps, loaded with rice bales under mats, nobody aboard: the family's, or any lighter unloading (it rides: fx lighter-bob). The scene may hide it once the family's lighter has gone. Its base is the bank's lip: everyone on the street is in front of it, the lighters going by on the river (flyers, behind everything) behind it"},
        {"id": "market", "file": "market.png", "base": line_base(-140, 420, -1418), "what": "the rice dealers who will not stop, in the road at the right, hands up; the two water men with their buckets at their left end (the splash is frames: `splash`)"},
        {"id": "noren", "file": "noren.png", "base": line_base(D.DOOR[0] - 10, D.DOOR[1] + 10, H_["Zf"] + 2), "what": "O-Natsu's house-name noren in her doorway (it stirs: fx noren-sway); whoever goes in passes behind it"},
        {"id": "sandals", "file": "sandals.png", "base": [[p[0], p[1] + 0] for p in stall_b], "states": {"full": "sandals.png", "few": "sandals-few.png"},
         "what": "a heap of new straw sandals on a mat at the stall's left end (alms): full, then fewer as they are given out"},
        {"id": "pot", "file": "pot.png", "base": [[p[0], p[1]] for p in stall_b], "what": "the portable clay hearth and the great rice pot on it, its lid off and leaning by it (where Mom serves: mark `pot`); its steam is fx pot-steam, its fire fx hearth-embers"},
        {"id": "stall", "file": "stall.png", "base": [[p[0], p[1]] for p in stall_b], "what": "the trestle table, and the tub of pickled radish on it (Little Sister's: mark `pickle`)"},
        {"id": "tray", "file": "tray.png", "base": [[p[0], p[1]] for p in stall_b], "states": {"full": "tray.png", "half": "tray-half.png", "empty": "tray-empty.png"},
         "what": "the tray of rice balls on the table, bale-shaped (Big Sister's: mark `balls`): full, emptying, empty", "order": "after stall (the same base: listed later, drawn over it)"},
        {"id": "kettle", "file": "kettle.png", "base": [[p[0], p[1]] for p in stall_b], "what": "the tea kettle on its little brazier at the stall's right end (O-Natsu's: mark `natsu`); its steam is fx kettle-steam"},
        {"id": "front", "file": "front.png", "plane": "front", "what": "rice bales stacked on a mat, their round ends to us, and a bucket at the very front, bottom right"},
    ]
    sp = {k: v for k, v in meta.items() if k.startswith("splash")}
    sp_names = sorted(sp, key=lambda k: int(k.split("-")[1]))
    bucket = extra["market"]["bucket"]
    splash_plane = {"id": "splash", "frames": [f"{n}.png" for n in sp_names], "fps": 10, "at": rp(bucket), "foot": sp[sp_names[0]]["foot"],
                    "base": line_base(-140, 420, -1417), "size": sp[sp_names[0]]["size"],
                    "what": "a bucket's splash, thrown by the nearer water man at the dealers (five frames: the water leaving the bucket, the arc opening into drops, falling)",
                    "note": "FRAMES, not ENGINE-21's kind: a plane with frames (as egypt-crash's steam). Show it now and then (every 6 to 12 s) for one run of its five frames (half a second), and hide it between: the scene's script, or a plane `when` on a clock flag. Its foot is the bucket's mouth."}
    # ---------------------------------------------------------------- things (ROUND-21's list, each with a shape)
    river_poly = [[432, 300], [800, 300], [800, rp(g(edge_X(800, D.LIP_Z), D.LIP_Z))[1]]] + poly_xz([(X, D.LIP_Z) for X in np.linspace(edge_X(800, D.LIP_Z), D.HOUSE["X1"], 5)]) + [[432, 440]]
    bx = [p[0] for p in info["bridge"]]
    by = [p[1] for p in info["bridge"]]
    bridge_rect = [int(max(0, min(bx))), int(min(by)) - 12, int(800 - max(0, min(bx))), int(min(470, max(by) + 40) - min(by) + 12)]
    house_poly = [rp(p) for p in (info["house"]["front"][0], info["house"]["front"][1], info["house"]["side"][1], info["house"]["side"][2])] + \
                 [rp(info["house"]["roof"][2]), rp(info["house"]["roof"][3]), rp(info["house"]["roof"][0])]
    tub = extra["stall"]["tub"]
    figs = extra["market"]["figs"]
    deal = [f for f in figs[:len(T.MARKET_FIGS)]]
    water = figs[len(T.MARKET_FIGS):]
    def figs_box(fs, pad=4):
        xs0 = min(p[0] - h * 0.28 for p, h in fs); xs1 = max(p[0] + h * 0.28 for p, h in fs)
        ys0 = min(p[1] - h * 1.05 for p, h in fs); ys1 = max(p[1] for p, h in fs)
        return [int(xs0) - pad, int(ys0) - pad, int(xs1 - xs0) + 2 * pad, int(ys1 - ys0) + 2 * pad]
    things = [
        {"id": "river", "what": "the river (the Dojima river): brown-green, the sky in it, lighters going by", "shape": {"poly": river_poly}, "stand": marks["landing"], "face": "S"},
        {"id": "lighters", "what": "lighters poling past on the river, loaded (fx lighters-near, lighters-far)", "shape": {"rect": [440, 330, 250, 90]}, "stand": marks["landing"], "face": "S"},
        {"id": "warehouses", "what": "the domains' white warehouses across the water on the island, with their gates, roof on roof", "shape": {"rect": [576, 192, 224, 150]}, "stand": marks["landing"], "face": "S"},
        {"id": "bridge", "what": "a timber bridge, high-arched, crossing the river at the right; people on it", "shape": {"rect": bridge_rect}, "stand": marks["town"], "face": "S"},
        {"id": "castle", "what": "far off up the river, the castle: stone walls and three corner turrets, and no keep", "shape": {"rect": [418, 196, 186, 72]}, "stand": marks["landing"], "face": "S"},
        {"id": "steps", "what": "the stone steps down to the water at a gap in the bank (where the family landed; the way back is gone with the lighter)", "shape": {"poly": [rp(p) for p in info["steps"]]}, "stand": marks["landing"], "face": "S"},
        {"id": "house", "what": "O-Natsu's house, a rice dealer's: its front to the street (the lattice, the bales stacked, the signboard), its back on the water", "shape": {"poly": house_poly}, "stand": marks["stall"], "face": "N"},
        {"id": "noren", "what": "the house-name noren in her doorway, indigo with a white mark", "shape": {"rect": box_of(planes["noren"][1], 2)}, "stand": marks["stall"], "face": "N"},
        {"id": "stall", "what": "O-Natsu's alms stall: the hearth and pot, the table, the tray, the tub, the sandals, the kettle", "shape": {"rect": _union([cut["sandals"], cut["pot"], cut["stall"], cut["kettle"]])}, "stand": marks["stall"], "face": "E"},
        {"id": "pot", "what": "the great rice pot on its portable hearth, steaming", "shape": {"rect": _pad(cut["pot"], 2)}, "stand": marks["line1"], "face": "N"},
        {"id": "tub", "what": "the tub of pickled radish, yellow slices", "shape": {"rect": [int(tub[0]) - 2, int(tub[1]) - 2, int(tub[2]) + 4, int(tub[3]) + 4]}, "stand": marks["line2"], "face": "N"},
        {"id": "tray", "what": "the tray of rice balls, bale-shaped (full / emptying / empty)", "shape": {"rect": _pad(cut["tray"], 3)}, "stand": marks["line1"], "face": "N"},
        {"id": "sandals", "what": "a heap of straw sandals for the pilgrims", "shape": {"rect": _pad(cut["sandals"], 3)}, "stand": marks["stall"], "face": "N"},
        {"id": "kettle", "what": "the tea kettle on its brazier", "shape": {"rect": _pad(cut["kettle"], 3)}, "stand": marks["kurataTo"], "face": "N"},
        {"id": "market", "what": "the rice market spilling into the road after the close", "shape": {"rect": _pad(cut["market"], 0)}, "stand": marks["market"], "face": "N"},
        {"id": "dealers", "what": "the dealers, hands up, still calling prices", "shape": {"rect": figs_box(deal)}, "stand": marks["market"], "face": "N"},
        {"id": "watermen", "what": "the water men with their buckets", "shape": {"rect": figs_box(water)}, "stand": marks["watermen"], "face": "N"},
        {"id": "bucket", "what": "the water men's buckets, full", "shape": {"rect": [rp(g(-135, -1372))[0], rp(g(-120, -1392, 40))[1], int(80 * CAM.k(-100, -1380)) + 8, int(46 * CAM.k(-100, -1380)) + 8]}, "stand": marks["watermen"], "face": "W"},
        {"id": "runner", "what": "a lad sprinting off with the day's price (now and then: fx runner)", "shape": {"rect": [520, 380, 280, 120]}, "stand": marks["market"], "face": "E"},
    ]
    people = [("natsu", "natsu", 146, "O-Natsu, at her stall (drawn by the game)"), ("rihei", "rihei", 156, "Rihei among the dealers (drawn by the game)"),
              ("kyuhachi", "kyuhachi", 156, "Kyuhachi, going round again (drawn by the game)"), ("kurata", "kurataTo", 156, "Kurata the doshin, walking the shore (drawn by the game)"),
              ("tatsu", "tatsuTo", 156, "Tatsu, his thief-taker (drawn by the game)"), ("awafather", "line1", 156, "the Awa father, first in the line (drawn by the game)"),
              ("awamother", "line2", 146, "the Awa mother with the baby on her back (drawn by the game)"), ("oldpilgrim", "line3", 150, "the old pilgrim from Kii (drawn by the game)"),
              ("ladleboy", "line4", 110, "the boy with a ladle bigger than his face (drawn by the game)")]
    for pid, mk, cm, what in people:
        things.append({"id": pid, "what": what, "shape": {"rect": person_rect(CAM, marks[mk], cm)}, "stand": marks["stall"] if pid in ("natsu", "awafather", "awamother", "oldpilgrim", "ladleboy", "kyuhachi") else marks["market"], "face": "N", "height_cm": cm, "mark": mk})
    # ---------------------------------------------------------------- fx: what moves (the engine draws it)
    lane = lambda Z, x0=-160, x1=960: [rp(g(edge_X(x0, Z), Z, D.WATER_Y)), rp(g(edge_X(x1, Z), Z, D.WATER_Y))]
    window = [[432, 300], [702, 300], [702, 452], [432, 452]]
    fr = lambda n: meta[n]
    runner_list = [f"runner-{i}.png" for i in (1, 2, 3, 4)] * 3
    pot_mouth = extra["pot"]["mouth"]
    fx = [
        {"id": "pot-steam", "type": "smoke", "base": stall_b, "what": "steam from the rice pot", "at": rp(pot_mouth), "height": 74, "width": [5, 30], "lean": [-22, -74],
         "rise": 14, "rate": 3.0, "gust": 0.25, "color": "#f2f0ea", "opacity": 0.34},
        {"id": "kettle-steam", "type": "smoke", "base": stall_b, "what": "a thread of steam from the kettle's spout", "at": rp(extra["kettle"]["spout"]), "height": 28, "width": [1, 6],
         "lean": [-8, -28], "rise": 8, "rate": 2.0, "gust": 0.3, "color": "#f2f0ea", "opacity": 0.28},
        {"id": "hearth-embers", "type": "embers", "base": stall_b, "what": "the charcoal in the hearth's fire mouth", "at": rp(extra["pot"]["fire"]), "size": [5, 2], "glowOpacity": 0.15, "sparks": 0.1},
        {"id": "noren-sway", "type": "sway", "plane": "noren", "anchor": "top", "amount": 2.0, "period": 3.6, "wave": 24, "lean": 0.3, "what": "the noren stirring in the air off the river"},
        {"id": "lighter-bob", "type": "bob", "plane": "lighter", "amount": 1, "period": 5.5, "tilt": 0.8, "what": "the moored lighter riding at the steps"},
        {"id": "river-shimmer", "type": "shimmer", "plane": "back", "what": "the afternoon light moving on the river", "poly": river_poly, "count": 26, "size": 5, "flow": [3, 0], "life": 2.0,
         "color": "#f6eed8", "opacity": 0.42, "note": "the river flows to the right (downstream, west): the glints drift that way"},
        {"id": "lighters-near", "type": "birds", "kind": "flyers", "plane": "back", "what": "a loaded lighter poled past on the river, the nearer lane",
         "lanes": [lane(-3000.0)], "every": [28, 56], "group": [1, 1], "speed": 12, "size": fr("lighter-near")["size"][0],
         "frames": {"glide": ["lighter-near.png"], "foot": fr("lighter-near")["foot"], "face": "E"}, "clip": [window],
         "note": "painted at its size (no sizeAt): 180 px long (about 6.5 m) at about 30 m. Both ways (the engine turns the frame). `clip` keeps it in the river between O-Natsu's house and the bridge (it passes behind the moored lighter and the crowd, which are cut-outs). The engine's flyers lift each crossing up to 7 px off its lane: that is the river's width, not a fault"},
        {"id": "lighters-far", "type": "birds", "kind": "flyers", "plane": "back", "what": "a lighter going back light, the farther lane", "lanes": [lane(-4300.0)], "every": [22, 46],
         "group": [1, 1], "speed": 9, "size": fr("lighter-far")["size"][0], "frames": {"glide": ["lighter-far.png"], "foot": fr("lighter-far")["foot"], "face": "E"}, "clip": [window]},
        {"id": "runner", "type": "birds", "kind": "flyers", "plane": "back", "what": "the price runner sprinting off from the market to the town, now and then",
         "lanes": [[rp(g(-30, -1445)), rp(g(edge_X(820, -1120), -1120))]], "both": False, "every": [26, 50], "group": [1, 1], "speed": 150,
         "size": fr("runner-1")["size"][0], "frames": {"flap": runner_list, "glide": ["runner-2.png", "runner-4.png"], "foot": fr("runner-1")["foot"], "face": "E"},
         "behind": [poly_xz([(-110, -1400), (40, -1400), (40, -1520), (-110, -1520)])],
         "note": "a run cycle (runner-1 to -4) listed three times in `flap`, so that at the flyers' beat it strides about twice a second. The flyers' kind glides between bursts (it would freeze him mid-stride): ENGINE-21's running courier, if it has one, or a flyer that never glides (`flap` only), suits him better. He comes out from behind the water men (`behind`) and is gone off the right edge, toward the bridge and the town; painted at the size of a man at the market (no sizeAt)"},
    ]
    out = {
        "id": "edo-dojima", "horizon": D.HZ, "full": D.FULL,
        "view": {"horizon": D.HZ, "full": D.FULL, "camera": "room.View(262, 590, cam=(0, 0), yaw=-12, focal=800): eye 358.75 cm; we look south-south-east across the river, upstream to the left",
                 "world": "cm; X to the right (west), Z toward us (north), Y up; the bank's lip Z -1550, the river 180 below the street, the island's bank Z -5550; O-Natsu's house X -880..-380, front Z -1450"},
        "light": "about four in the afternoon, the sun west-south-west, 28 degrees up, to our right: faces turned to the right lit warm, the fronts facing us (north) in a luminous blue shade, the street warm; shadows fall to the left and a little toward us",
        "walk": walk, "walk_note": "one area: the shore street, from the bottom to O-Natsu's house front (left) and the stone lip of the bank (clear of its coping); the steps go down beyond the lip (outside it: the family arrives at `landing`, at their top)",
        "blocked": blocked,
        "planes": planes_out + [splash_plane], "cutouts": cut,
        "states": {"tray": ["tray", "tray-half", "tray-empty"], "sandals": ["sandals", "sandals-few"]},
        "frames": {k: v for k, v in meta.items()},
        "things": things, "marks": marks, "stands": stands, "fx": fx,
        "fx_note": "steam (smoke) from the pot and the kettle; embers in the hearth; the noren sways; the moored lighter bobs; the river shimmers; the lighters and the runner are flyers on painted frames; the splash is a plane of frames the scene shows now and then (planes: splash). The pilgrims' line's life (shuffling forward) is the people's",
        "notes": [
            "The view is composed, as the design's plan asks: the castle's walls and turrets show far off up the river at the left; from where we stand it lies further left than the picture's edge. A print would bring it in, and so does this.",
            "The steps are drawn as a print draws them (as if from a little higher): from a street's height a flight going away and down would hide its own treads.",
            "O-Natsu's house stands on the river side of the street, its front to the street and its back on the water (the arrangement is the game's: the facts say only that the rice dealers' quarter is on the river).",
            "Rihei stands in front of the dealers (they are painted); the pilgrims' line runs from the stall toward the bottom right (line1 at the stall).",
        ],
        "heights": {"mom_cm": 168, "bigsis_cm": 160, "lilsis_cm": 122, "man_1830_cm": 156, "woman_1830_cm": 146, "ladleboy_cm": 110, "grownup_at_full_px": 160},
    }
    return out


def _pad(r, p):
    return [r[0] - p, r[1] - p, r[2] + 2 * p, r[3] + 2 * p]


def _union(rs):
    x0 = min(r[0] for r in rs); y0 = min(r[1] for r in rs)
    x1 = max(r[0] + r[2] for r in rs); y1 = max(r[1] + r[3] for r in rs)
    return [x0, y0, x1 - x0, y1 - y0]

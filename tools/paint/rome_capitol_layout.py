"""The Capitol's layout.json: every number the scene file needs, measured from the picture as painted (through the
camera of rome_capitol_kit, and from the painted layers themselves for the shapes that hug things).

  python3 rome_capitol_layout.py      writes out/rome-capitol/layout.json (rome_capitol.py also calls write())"""

import json
import math
import os

import numpy as np

from rome_capitol_kit import *
import rome_capitol_things as TH
import rome_capitol_temple as RT
import rome_capitol_geese as GE

r = lambda q: [int(round(q[0])), int(round(q[1]))]


def hull(mask, pad=2.0, most=18):
    """A polygon hugging a mask: its convex hull, pushed out by `pad` px and thinned to at most `most` corners."""
    from scipy.spatial import ConvexHull
    ys, xs = np.where(mask)
    pts = np.stack([xs, ys], axis=1).astype(float)
    pts = np.concatenate([pts, pts + [1, 0], pts + [0, 1], pts + [1, 1]])
    hv = pts[ConvexHull(pts).vertices]
    c = hv.mean(axis=0)
    hv = c + (hv - c) * (1 + pad / np.maximum(np.linalg.norm(hv - c, axis=1, keepdims=True), 1))
    while len(hv) > most:                                    # drop the corner that changes the outline least
        n = len(hv)
        areas = [abs(np.cross(hv[(i + 1) % n] - hv[i], hv[i - 1] - hv[i])) for i in range(n)]
        hv = np.delete(hv, int(np.argmin(areas)), axis=0)
    return [[int(round(x)), int(round(y))] for x, y in hv]


def ground_poly(pts):
    """World places on the paving (X, Z) -> picture points."""
    return [r(P(X, 0, Z)) for X, Z in pts]


def circle_ground(X, Z, rad, n=12):
    return ground_poly([(X + rad * math.cos(a), Z + rad * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)])


def box_ground(X0, X1, Z0, Z1):
    return ground_poly([(X0, Z0), (X1, Z0), (X1, Z1), (X0, Z1)])


def layer_alpha(name):
    """The alpha of a painted layer, from the scene's kept layers (rome_capitol.py)."""
    import rome_capitol as RC
    if name == "temple":
        return RC.temple_layer().a > 0.5
    if name == "kings":
        return RC.kings_layer().a > 0.5
    return RC.cut_layers()[name].a > 0.5


# ---------------------------------------------------------------- the places, fixed here and checked on the engine's walk map
MARKS = {
    "fromSteps": [540, 560],       # where he arrives from the steps: a step in from the bottom edge, in the gate's way
    "toSteps": [540, 595],         # the bottom way's walkTo: on the floor at the edge (the gate is behind us)
    "default": [500, 520],
    "atbase": [384, 506],          # before the boy's base, facing N: in front of the geese, by its right corner, below Titus (never in front of his face)
    "anser": [146, 458],           # the goose-keeper, behind his pen (its fence before his legs), facing E: his geese, the base
    "view": [202, 439],            # at the parapet, facing W: over the city (reached between the pen's back and the kings)
    "titus_run": [468, 594],       # where Titus runs out at the bottom
    "diodorus": [560, 368],        # (later) the temple keeper, at the foot of the temple's steps by the altar's left end
    "diodorus_brutus": [270, 462], # (later) his spot before old Brutus's base, where he scrubs the scribbles off
}
FACES = {"atbase": "N", "anser": "E", "view": "W", "diodorus": "S", "diodorus_brutus": "N", "fromSteps": "N", "default": "N"}


def kings_blocked():
    out = []
    for kg in KINGS:
        X0, X1, Z0, Z1, h = base_box(kg)
        out.append(box_ground(X0 - 6, X1 + 6, Z0 - 6, Z1 + 6))
    return out


def walk_outline():
    """The paving people can stand on: from the bottom edge up to the temple's lowest step on the right, and to the
    parapet on the left; never behind the row of kings (the boy's base is in the backdrop, so nobody may pass behind
    it: the floor's far line runs along the front of the row)."""
    steps_l = T.pt(RT.CHEEK + 40, -RUN, 0)
    steps_r = T.pt(UW, -RUN, 0)
    yr = steps_r[1] + (797 - steps_r[0]) * (steps_l[1] - steps_r[1]) / (steps_l[0] - steps_r[0]) if steps_r[0] > 797 else steps_r[1]
    kings_front = P(0, 0, KINGS_Z - 6)[1] + 2.5
    k0 = base_box(KINGS[0])
    k4 = base_box(KINGS[-1])
    left_of_row = P(k0[0] - 6, 0, KINGS_Z - 6)
    right_of_row = P(k4[1] + 6, 0, KINGS_Z - 6)
    wall_foot = P(0, 0, WALL["Z"] - 8)[1] + 2.5
    wall_end = P(TH.wall_end_X() + 8, 0, WALL["Z"] - 8)
    xr = right_of_row[0] + 20                                # (a figure there is half its width clear of the last statue)
    return [[0, 597], [797, 597], [797, int(round(yr + 2))], [int(round(steps_l[0])), int(round(steps_l[1] + 2))],
            [int(round(xr + 6)), int(round(steps_l[1] + 8))], [int(round(xr)), int(round(kings_front))],
            [int(round(left_of_row[0])), int(round(kings_front))], [int(round(wall_end[0])), int(round(wall_foot))], [0, int(round(wall_foot))]]


def write(path):
    import rome_capitol as RC
    out = {"id": "rome-capitol", "horizon": HZ, "full": FULL, "minScale": 0.15,
           "light": "the sun low on the right, in the east-south-east (about 33 degrees up): things that face right are lit, shadows fall to the left and a little away"}
    out["note"] = ("The temple stands far off (its lowest step some 55 m away, rows 320 to 326): the lens is 3.45 m up and looks level, so a "
                   "temple this tall can only show its pediment and the chariot on its peak from there. A man at the foot of its steps "
                   "is 23 px tall in true perspective, so minScale is 0.15 (people keep their true size wherever they can walk); at "
                   "the boy's base (row 447) a man is 88 px, at the bottom edge 165.")
    walk = walk_outline()
    out["walk"] = walk
    out["blocked"] = kings_blocked()
    # ---- the cut-outs, back to front, each with its base and the ground it takes up
    X0, X1 = ALTAR["X"]
    Z0, Z1 = ALTAR["Z"]
    ch = CHARIOT
    cbw, cbd, cbh = ch["base"]
    w = WORLD
    wbw, wbd, wbh = w["base"]
    hut_front = P(HUT["X"], 0, HUT["Z"] - HUT["r"])[1]
    PX0, PX1 = PEN["X"]
    PZ0, PZ1 = PEN["Z"]
    posts = TH.tablet_posts()
    pw, pd, ph = TH.POST
    first, last = posts[0], posts[-1]
    out["planes"] = [
        {"id": "altar", "file": "altar.png", "base": [r(P(X0 - 30, 0, Z0 - 30)), r(P(X1 + 30, 0, Z0 - 30))], "solid": box_ground(X0 - 30, X1 + 30, Z0 - 30, Z1 + 30),
         "what": "the great altar of Jupiter, on its step: people pass behind it, and behind its smoke"},
        {"id": "chariot", "file": "chariot.png", "base": [r(P(ch["X"] - cbw / 2 - 6, 0, ch["Z"] - 6)), r(P(ch["X"] + cbw / 2 + 6, 0, ch["Z"] - 6))],
         "solid": box_ground(ch["X"] - cbw / 2 - 6, ch["X"] + cbw / 2 + 6, ch["Z"] - 6, ch["Z"] + cbd + 6), "what": "the dictator's bronze chariot on its base, facing the temple"},
        {"id": "world", "file": "world.png", "base": [r(P(w["X"] - wbw / 2 - 6, 0, w["Z"] - 6)), r(P(w["X"] + wbw / 2 + 6, 0, w["Z"] - 6))],
         "solid": box_ground(w["X"] - wbw / 2 - 6, w["X"] + wbw / 2 + 6, w["Z"] - 6, w["Z"] + wbd + 6), "what": "his statue on the bronze ball of the world, on its tall base"},
        {"id": "parapet", "file": "parapet.png", "base": [r(P(-1200, 0, WALL["Z"] - 8)), r(P(TH.wall_end_X() + 8, 0, WALL["Z"] - 8))],
         "solid": box_ground(-2410, TH.wall_end_X() + 8, WALL["Z"] - 8, WALL["Z"] + WALL["t"] + 8),
         "what": "the parapet over the drop (a cut-out with a base, not the front plane: the boy stands at it to look at the view; the city's smoke rises behind it)"},
        {"id": "hut", "file": "hut.png", "base": int(round(hut_front)), "solid": circle_ground(HUT["X"], HUT["Z"], HUT["r"] + 12), "what": "Romulus's hut"},
        {"id": "pen", "file": "pen.png", "base": [r(P(PX0, 0, PZ0)), r(P(PX1, 0, PZ0))], "solid": box_ground(PX0 - 4, PX1 + 4, PZ0 - 4, PZ1 + 4),
         "what": "the pen's near fence and its gate side, the gate standing open: the geese in the pen stand behind it (its far fence and the trough are in back.png)"},
        {"id": "tablets", "file": "tablets.png", "base": [r(P(first[0] - TH.DESK[0] / 2, 0, first[1] - 6)), r(P(last[0] - TH.DESK[0] / 2, 0, last[1] + pd + 6))],
         "solid": [box_ground(Xp - pw / 2 - 5, Xp + pw / 2 + 5, Zp - 5, Zp + pd + 5) for Xp, Zp in posts],
         "what": "the row of bronze tablets on their posts, running away from us at the front right: people pass behind it (its base runs along the posts' left side)"},
    ]
    # ---- the things to click
    talpha = layer_alpha("temple")
    kalpha = layer_alpha("kings")
    cuts = RC.cut_layers()
    stand_temple = [620, 392]
    things = []

    def thing(id_, what, shape, stand, face="N"):
        things.append({"id": id_, "what": what, "shape": {"poly": shape}, "stand": stand, "face": face})
    thing("temple", "the temple of Jupiter Best and Greatest, on its high base, its broad steps", hull(talpha, 2, 20), stand_temple)
    thing("name", "the one name across the front, in bronze letters: Q LVTATIVS CATVLVS",
          [r(T.pt(RT.UE0 + 300, RT.VE, E1 - 4)), r(T.pt(RT.UE1 - 300, RT.VE, E1 - 4)), r(T.pt(RT.UE1 - 300, RT.VE, E2 + 4)), r(T.pt(RT.UE0 + 300, RT.VE, E2 + 4))], stand_temple)
    peak = T.pt(RT.MID, RT.VC, RT.PEAK + 330)
    thing("roof", "the roof plated in gilt bronze, flashing at its edges, and the bronze chariot of four horses on its peak",
          [r(T.pt(RT.RK0 - 40, RT.VC, E3 - 10)), r((peak[0] - 26, peak[1])), r((peak[0] + 26, peak[1])), r(T.pt(RT.RK1 + 40, RT.VC, E3 - 10)),
           r(T.pt(RT.RK1 + 40, RT.VC, E3 + 70)), r(T.pt(RT.RK0 - 40, RT.VC, E3 + 70))], stand_temple)
    d0, d1 = RT.DOORS[0], RT.DOORS[2]
    thing("doors", "the three doors in the porch, the middle one open: far inside, the dim gleam of the god in gold and ivory",
          [r(T.pt(d0[0] - d0[1] / 2 - 40, RT.DEEP, HP)), r(T.pt(d1[0] + d1[1] / 2 + 40, RT.DEEP, HP)), r(T.pt(d1[0] + d1[1] / 2 + 40, RT.DEEP, HP + 860)),
           r(T.pt(d0[0] - d0[1] / 2 - 40, RT.DEEP, HP + 860))], stand_temple)
    thing("altar", "the great altar of Jupiter, its fire burned low, the last of the morning's smoke", hull(cuts["altar"].a > 0.5, 2), [612, 376])
    thing("chariot", "the dictator's bronze chariot of four horses on its base, facing Jupiter's doors", hull(cuts["chariot"].a > 0.5, 2), [726, 392])
    thing("world", "a bronze man standing on a great bronze ball, the world, on a tall base", hull(cuts["world"].a > 0.5, 2), [500, 398])
    # the kings: each statue's own shape from the layer; the row's area is the old kings', Brutus and the new one have their own
    labels = {}
    from scipy import ndimage
    lab, n = ndimage.label(kalpha)
    rows_ = []
    for kg in KINGS:
        X0_, X1_, Z0_, Z1_, h_ = base_box(kg)
        x0, x1 = P(X0_ - 8, 0, Z0_)[0], P(X1_ + 8, 0, Z0_)[0]
        m = kalpha.copy()
        m[:, :int(x0)] = False
        m[:, int(math.ceil(x1)):] = False
        if kg["kind"] == "brutus":
            m[:, int(x0):int(math.ceil(x1)) + 14] = kalpha[:, int(x0):int(math.ceil(x1)) + 14]       # (his sword reaches to the right)
        labels[kg["kind"]] = m
    oldm = labels["old"] | labels["seat"] | labels["old2"]
    thing("kings", "a row of bronze statues of the old kings of Rome, each on its stone base", hull(oldm, 2, 20), [440, 476])
    thing("brutus", "old Brutus with his sword drawn, who drove the kings out; on his base, scratched words too small to read", hull(labels["brutus"], 2), [272, 468])
    thing("dictator", "a new bright statue among the kings: the dictator's", hull(labels["new"], 2), [404, 478])
    thing("tablets", "bronze tablets of laws, treaties and decrees, on a row of short posts: lines of letters too small to read", hull(cuts["tablets"].a > 0.5, 2), [664, 566], "E")
    geese_shape = geese_area()
    gx = [p[0] for p in geese_shape]
    gy = [p[1] for p in geese_shape]
    thing("geese", "Juno's sacred geese, round the foot of the boy's base (the scene puts the area round them: after the stomp, the pen's)",
          [[min(gx) - 6, min(gy) - 40], [max(gx) + 6, min(gy) - 40], [max(gx) + 6, max(gy) + 4], [min(gx) - 6, max(gy) + 4]], MARKS["atbase"])
    pen_shape = hull((cuts["pen"].a > 0.5) | (RC.pen_back_layer().a > 0.5), 2)
    thing("pen", "the geese's pen: a low wattle fence round a trough, its gate standing open", pen_shape, [272, 505], "W")
    thing("hut", "the hut of Romulus: small, round, wattle and thatch, very old", hull(cuts["hut"].a > 0.5, 2), [52, 497])
    thing("view", "the river and the island, over the parapet", [[112, 336], [126, 326], [196, 318], [236, 300], [236, 312], [214, 330], [180, 346], [124, 352], [112, 346]], MARKS["view"], "W")
    thing("theater", "Pompey's great curved stone theater on the plain, the temple at the top of its seats, its colonnades", [[0, 284], [64, 270], [130, 284], [196, 302], [196, 322], [0, 318]], MARKS["view"], "W")
    thing("janiculum", "across the river: low roofs and gardens, and the long ridge of the Janiculum with its pines", [[0, 246], [120, 238], [236, 250], [236, 296], [130, 292], [0, 294]], MARKS["view"], "W")
    out["things"] = things
    # ---- the marks
    seat = seat_base()
    X0_, X1_, Z0_, Z1_, h_ = base_box(seat)
    at = P((X0_ + X1_) / 2, 0, Z0_)
    out["marks"] = {k: v for k, v in MARKS.items()}
    out["marks"]["faces"] = FACES
    out["marks"]["titus_seat"] = {"at": r(at), "cm": int(seat["h"]), "px": int(round(seat["h"] * k_at(Z0_)))}
    out["marks"]["geese"] = geese_shape
    out["marks"]["pen"] = pen_inside()
    out["marks"]["pen_gate"] = r(P(PEN["gate"][0] + 4, 0, (PEN["gate"][1] + PEN["gate"][2]) / 2))
    out["exits"] = [{"to": "rome-steps", "edge": "S", "id": "to-steps", "name": "down the hill to the steps", "walkTo": MARKS["toSteps"], "spawn": "fromSteps",
                     "band": [[400, 548], [640, 548], [640, 600], [400, 600]],
                     "note": "the precinct's gate is behind us at the bottom (the road from the Forum comes in there): the bottom band from x 400 to 640 is open paving"}]
    out["fx"] = fx_marks(geese_shape)
    out["fx_note"] = ("Nothing that moves by nature is painted: the altar's smoke and its embers, the geese, the kites wheeling over the precinct, "
                      "the threads of smoke from the city below and the light on the river are the game's to draw, from these marks (the engine's own "
                      "fields, docs/DESIGN.md, 'Things that move by nature'). The geese are one flock, 'geese', round the foot of the boy's base; "
                      "after the stomp the scene gives the flock the area marks.pen (its fx a function of rome.geeseGone), and herds it through "
                      "marks.pen_gate. The kites have no frames: the engine draws them. The river's light keeps to the water.")
    out["frames"] = {"geese": dict(GE.frames_block(), files="goose-<n>.png and goose-grey-<n>.png, n 1 to 17", acts=GE.ACTS,
                                   size=[GE.BOX[0], GE.BOX[1]],
                                   note=("White geese, a little grey on the back and wings, facing E (the engine turns them for W); every frame on one canvas "
                                         "with the feet at the foot point; painted at full size (sizeAt 590: a goose with its neck up is 59 px, 36 px at the base). "
                                         "goose-grey-<n> is a second colouring of the same frames (a greyer bird): a flock takes one set, so it is not in the marks; "
                                         "a scene that wants one grey goose among the white gives it a flock of its own and herds both."))}
    out["sizes"] = {"man_px_at_fromSteps": round(160 * scale_at(MARKS["fromSteps"][1]), 1), "man_px_at_atbase": round(160 * scale_at(MARKS["atbase"][1]), 1),
                    "man_px_at_anser": round(160 * scale_at(MARKS["anser"][1]), 1), "goose_px_at_geese": round(59.4 * scale_at(np.mean(gy)), 1),
                    "man_px_at_steps_foot": round(160 * max(0.15, scale_at(324)), 1), "titus_standing_px_at_seat": round(0.78 * 160 * scale_at(at[1]), 1)}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    return out


def geese_area():
    """Where the geese stand guard: round the foot of the boy's base, in front of it, on open paving."""
    seat = seat_base()
    X0_, X1_, Z0_, Z1_, h_ = base_box(seat)
    return ground_poly([(X0_ - 30, Z0_ - 24), (X1_ + 70, Z0_ - 24), (X1_ + 60, Z0_ - 290), (X0_ - 10, Z0_ - 290)])


def pen_inside():
    PX0, PX1 = PEN["X"]
    PZ0, PZ1 = PEN["Z"]
    return ground_poly([(PX0 + 30, PZ0 + 28), (PX1 - 26, PZ0 + 28), (PX1 - 26, PZ1 - 70), (PX0 + 30, PZ1 - 70)])


def river_shapes():
    """The river as it is painted (rome_capitol.RIVER_NEAR, RIVER_FAR and their widths), and the island in it."""
    import rome_capitol as RC
    from brush import curve
    near = curve(RC.RIVER_NEAR, 6)
    widths = RC.river_widths(near)
    up = [(p[0], p[1] - w * 0.55) for p, w in zip(near, widths)]
    dn = [(p[0], p[1] + w * 0.55) for p, w in zip(near, widths)]
    poly = up[::3] + [up[-1]] + [dn[-1]] + dn[::-1][::3] + [dn[0]]
    near_river = [[int(round(x)), int(round(y))] for x, y in poly if -2 <= x <= 238]
    far_ = [p for p in curve(RC.RIVER_FAR, 6) if 132 <= p[0] <= 214]
    far_river = [[int(round(x)), int(round(y - 2.2))] for x, y in far_[::2]] + [[int(round(x)), int(round(y + 2.0))] for x, y in far_[::-2]]
    island = [[int(round(x)), int(round(y))] for x, y in RC.ISLAND] + [[140, 349]]
    island = [[104, 338], [126, 332], [152, 327], [176, 324], [196, 320], [210, 309], [219, 310], [212, 324], [206, 330], [186, 335], [160, 340], [155, 350], [140, 350], [132, 344], [108, 344]]
    return near_river, far_river, island


def fx_marks(geese_shape):
    X0, X1 = ALTAR["X"]
    Z0, Z1 = ALTAR["Z"]
    mid = ((X0 + X1) / 2, (Z0 + Z1) / 2)
    fire = P(mid[0], ALTAR["h"] + 4, mid[1])
    f0, f1 = P(X0 + 120, ALTAR["h"], mid[1]), P(X1 - 120, ALTAR["h"], mid[1])
    altar_base = [r(P(X0 - 30, 0, Z0 - 30)), r(P(X1 + 30, 0, Z0 - 30))]
    near_river, far_river, island = river_shapes()
    return [
        {"id": "altar-smoke", "type": "smoke", "what": "the last of the morning's smoke from the altar, thin and pale, leaning left with the air",
         "at": r(fire), "base": altar_base, "height": 150, "width": [3, 18], "lean": [-38, -150], "rise": 14, "rate": 2.5, "gust": 0.3,
         "color": "#f2ece2", "opacity": 0.40,
         "note": "It rises from the long pan of ash on the altar's top, in front of the temple's steps and columns; its base is the altar's, so "
                 "anyone behind the altar is behind its smoke. The Ides ewe went up at first light: this is all that is left of it."},
        {"id": "altar-embers", "type": "embers", "what": "a few coals still red in the ash", "at": r(((f0[0] + f1[0]) / 2, f0[1] - 1)),
         "size": [round((f1[0] - f0[0]) / 2 - 3, 1), 1.6], "count": 6, "sparks": 0.08, "base": altar_base, "glowOpacity": 0.12,
         "note": "Six coals are painted in altar.png, in grey ash: these breathe over them, quietly."},
        {"id": "geese", "type": "birds", "kind": "flock", "what": "Juno's sacred geese, standing guard round the foot of the boy's base",
         "area": geese_shape, "count": 6, "frames": GE.frames_block(), "shy": 0, "fly": False,
         "moves": {"stand": 4, "look": 1, "peck": 1, "walk": 2, "turn": 1}, "walk": 8,
         "note": "They stand their ground (shy 0, fly false) until the stomp: then the scene herds them into marks.pen through marks.pen_gate "
                 "(open ground all the way: nothing painted between the base and the gate). They sort by their own feet, like people, so the "
                 "pen's near fence (pen.png) stands in front of them once they are inside."},
        {"id": "kites", "type": "birds", "kind": "flyers", "what": "two kites wheeling high over the precinct", "circle": {"at": [250, 96], "r": [120, 34]},
         "count": 2, "speed": 14, "size": 11, "plane": "back",
         "note": "In the open sky left of the temple (the temple and its roof are in back.png: the circle keeps left of x 370)."},
        {"id": "city-smoke-1", "type": "smoke", "what": "a thread of smoke from a chimney in the city below", "at": [150, 364], "plane": "back",
         "height": 34, "width": [1, 6], "lean": [-12, -34], "rise": 5, "rate": 1.5, "gust": 0.2, "color": "#ece6dc", "opacity": 0.26},
        {"id": "city-smoke-2", "type": "smoke", "what": "another, nearer, by the temples of the market", "at": [138, 374], "plane": "back",
         "height": 26, "width": [1, 5], "lean": [-10, -26], "rise": 4, "rate": 1.3, "gust": 0.2, "color": "#ece6dc", "opacity": 0.22, "seed": 2},
        {"id": "city-smoke-3", "type": "smoke", "what": "and one on the plain beyond the river's bend", "at": [182, 306], "plane": "back",
         "height": 18, "width": [1, 4], "lean": [-8, -18], "rise": 3, "rate": 1.2, "gust": 0.2, "color": "#eee8de", "opacity": 0.2, "seed": 3},
        {"id": "river-light", "type": "shimmer", "what": "a faint light on the river's near reach, round the island", "poly": near_river, "holes": [island],
         "count": 6, "size": 3, "flow": [2, 0], "life": 2.2, "color": "#f4fbff", "opacity": 0.32, "plane": "back",
         "note": "The water as painted (its far bank to its near bank); the island and its bridges kept clear. Under the hut's thatch it is "
                 "hidden by the hut's cut-out (glints lie behind every cut-out)."},
        {"id": "river-light-far", "type": "shimmer", "what": "and on its far reach, where it shows between the theater and the kings", "poly": far_river,
         "count": 2, "size": 2, "flow": [1.5, 0], "life": 2.4, "color": "#f4fbff", "opacity": 0.26, "plane": "back",
         "note": "Only from x 132 to 214: left of that the theater stands in front of it, right of it the kings (in back.png) would be drawn under the glints."},
    ]


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    o = write(f"{OUT}/layout.json")
    print(json.dumps(o["marks"], indent=None)[:600])

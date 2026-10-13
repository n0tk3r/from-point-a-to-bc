"""layout.json for nevada-limo: the numbers the game needs, MEASURED from the finished picture.

Every rect is the box round the pixels that really show that thing (from what each ray of the picture met), not a copy
of the brief. Places on the floor (the marks, Ranger's places to stand, the walk outline, the base lines) are the model's
centimetres put through the same camera as the picture. The windows are each pane's exact glass, as polygons: the game
draws the desert strip clipped to them (a pixel is in a window when its middle is in the polygon, as here)."""

import json
import math

import numpy as np

from room import View
import nevada_limo_model as M

OUT = "out/nevada-limo"
W, H = 800, 600
V = View(**M.VIEW)
S0 = 160.0 / 175.0


def fl(X, Z, Y=0.0):
    x, y = V.pt(X, Y, Z)
    return [int(round(x)), int(round(y))]


def scale_at(X, Z):
    """The size the game draws a person at here, as a share of full size (true perspective: right for a seat too)."""
    return V.F / (S0 * V.cam_space(X, 0.0, Z)[2])


def pane_polys():
    """Each pane's glass in the picture, cut to the picture's edges: [(id, side, polygon)]."""
    from nevada_limo import panes
    return [(i, s, q) for i, s, q, _ in panes()]


def strip_rows(margin=6):
    """The rows the desert strip must cover: from above the highest pane to below the lowest. -> (top, row)."""
    ys = [p[1] for _, _, q in pane_polys() for p in q]
    return int(math.floor(min(ys))) - margin, int(math.ceil(max(ys))) + margin


def write(stA, stB, boxes, wins, cover):
    def rect_of(st, names, grow=0):
        m = cover(st, name=tuple(names)) > 0.5
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            return None
        return [int(xs.min()) - grow, int(ys.min()) - grow, int(xs.max() - xs.min() + 1) + 2 * grow, int(ys.max() - ys.min() + 1) + 2 * grow]

    def rect_xywh(b, grow=0):
        return [b[0] - grow, b[1] - grow, b[2] - b[0] + 2 * grow, b[3] - b[1] + 2 * grow]

    def union(*rs):
        rs = [r for r in rs if r]
        x0, y0 = min(r[0] for r in rs), min(r[1] for r in rs)
        x1, y1 = max(r[0] + r[2] for r in rs), max(r[1] + r[3] for r in rs)
        return [x0, y0, x1 - x0, y1 - y0]

    stand = {k: fl(*p) for k, (p, f) in M.STANDS.items()}
    face = {k: f for k, (p, f) in M.STANDS.items()}
    polys = [(i, s, q) for i, s, q, _ in wins]
    rect_poly = lambda side: union(*[[int(min(p[0] for p in q)), int(min(p[1] for p in q)), int(math.ceil(max(p[0] for p in q)) - min(p[0] for p in q)), int(math.ceil(max(p[1] for p in q)) - min(p[1] for p in q))] for i, s, q in polys if s == side])

    things = []

    def thing(id_, what, rect, at, **more):
        if rect is None:
            print("layout: nothing found for", id_)
            return
        t = {"id": id_, "what": what, "shape": {"rect": rect}, "stand": stand[at], "face": face[at]}
        t.update(more)
        things.append(t)

    A, B = stA, stB
    thing("divider", "the divider: smoked glass in a frame (up), or slid down into the seat back with the front of the car seen through it (down): two cut-outs",
          union(rect_xywh(boxes["divider"]), rect_of(B, ["frame"])), "atdivider", plane=["divider-up", "divider-down"])
    thing("ropes", "the ropes beside Grandpa Joe on the long seat: white regulation rope with a red thread, tied off in a bow, the loose end toward us (states 4, 3, 2, 1)",
          union(*[rect_xywh(boxes[f"ropes-{n}"], 2) for n in (4, 3, 2, 1)]), "atropes", plane="ropes")
    thing("bag", "the paper bag on the facing seat: brown, folded over at the top, a grease spot (the cheeseburger)", rect_xywh(boxes["bag-own"], 2), "atbag", plane="bag")
    thing("clipboard", "the clipboard propped on the facing seat: the office's map in pen, three circles (44, 1921, and one under a smudge), a column of empty boxes",
          rect_xywh(boxes["clipboard-own"], 2), "atclipboard", plane="clipboard")
    thing("juice", "a juice box with a straw on the facing seat, a plain apple on its side", rect_xywh(boxes["juice-own"], 3), "atjuice", plane="juice")
    thing("fridge", "the little fridge in the facing seat's base, at its near end: brushed steel, a chrome handle, a little blue light", rect_of(B, ["fridge"]), "atfridge")
    thing("phone", "the car phone: a cream handset in its cradle on the bar under the divider, a coiled cord", rect_of(B, ["phone"], 2), "atphone")
    thing("ashtray", "the ashtray on the bar: cut glass, full of jelly beans", rect_of(B, ["ashtray"], 2), "atashtray")
    thing("window-l", "the windows on the left: long, low, smoked; the desert going by", rect_poly("L"), "atwindow-l", windows=[i for i, s, q in polys if s == "L"])
    thing("window-r", "the windows on the right: long, low, smoked; the desert going by", rect_poly("R"), "atwindow-r", windows=[i for i, s, q in polys if s == "R"])
    from nevada_limo import clip_poly

    def seat_poly(x_wall, x_edge, z0, z1):
        """A seat's outline in the picture: the backrest's top along the wall, the cushion's front edge and its foot."""
        pts = [(x_wall, M.BACK_H, z0), (x_wall, M.BACK_H, z1), (x_edge, M.SEAT_H, z1), (x_edge, 0.0, z1), (x_edge, 0.0, z0), (x_edge, M.SEAT_H, z0)]
        out = []
        for x, y in clip_poly(V.poly(pts)):
            p = [int(round(x)), int(round(y))]
            if not out or p != out[-1]:
                out.append(p)
        return out
    thing("seat", "the long seat: gray leather, along the left side; Grandpa Joe sits at its far end", rect_of(B, ["seat", "seat-back"]), "atjoe",
          poly=seat_poly(0.0, M.SEAT_D, M.LONG_SEAT[4], M.LONG_SEAT[5]))
    thing("facingseat", "the facing seat: gray leather, along the right side", rect_of(B, ["facingseat", "facing-back"]), "atbag",
          poly=seat_poly(M.W, M.W - M.SEAT_D, M.FACING_SEAT[4], M.FACING_SEAT[5]))
    thing("belt", "a spare seatbelt's buckle end lying on the long seat's cushion (the belt round Joe is drawn on him)", rect_of(B, ["belt"], 3), "atbelt")

    joe = M.MARKS["joe"]
    jx, jy = fl(*joe)
    seat_px = jy - fl(joe[0], joe[1], M.SEAT_H)[1]
    rk = M.MARKS["ranger"]
    ro = M.MARKS["ropes"]
    ro_at = fl(ro[0], ro[1], M.SEAT_H)
    ro_floor = fl(ro[0], ro[1])
    marks = {
        "joe": {"at": [jx, jy], "face": "E", "scale": round(scale_at(*joe), 3), "seat_height_px": int(seat_px), "seat_cm": M.SEAT_H,
                "note": "the ground point under his hips: it lies under the long seat's cushion; seated there his hips are seat_height_px above it. He faces E, across the car toward the facing seat."},
        "ranger": {"at": fl(*rk), "face": "W", "scale": round(scale_at(*rk), 3), "note": "on the carpet between the seats, near us, facing Joe"},
        "ropes": {"at": ro_at, "scale": round(scale_at(*ro), 3), "floor": ro_floor, "face": "W",
                  "note": "where Ranger sits to nibble: ON the long seat's cushion beside the bow. Draw him at `scale` (not the row's), "
                          "his feet at `at`, sorted as if standing at `floor` (the carpet under him): in front of the ropes and of Joe."},
    }
    for k, (X, Z) in M.ON_FACING_SEAT.items():
        s = scale_at(X, Z)
        marks[k] = {"at": fl(X, Z, M.SEAT_H), "scale": round(s, 3), "floor": fl(M.W - M.SEAT_D - 4.0, Z), "face": "E",
                    "note": f"the point under the {k} ON the facing seat's cushion: for anything shown at the thing itself (a look, a little "
                            f"effect). Ranger takes it from the carpet, at his stand `at{k}` (reach). `scale`: the size a figure is drawn at "
                            "there; `floor`: the carpet just in front of the seat's edge, to sort a figure on the seat (in front of the "
                            "things on it). " + ("A figure on the seat here is within the engine's 1.25 for painted frames." if s <= 1.25 else
                                                 f"Too near us for Ranger to be drawn on the seat here ({s:.2f}: the engine draws painted "
                                                 "frames at no more than 1.25 of their size).")}
    walk = [fl(X, Z) for X, Z in M.WALK]
    seat_edge_far, seat_edge_near = fl(M.SEAT_D, M.LONG_SEAT[4]), fl(M.SEAT_D, M.LONG_SEAT[5])
    face_edge = [fl(M.W - M.SEAT_D, M.FACING_SEAT[4]), fl(M.W - M.SEAT_D, M.FACING_SEAT[5])]
    top, row = strip_rows()
    L = {
        "id": M.ID, "horizon": M.VIEW["horizon"], "full": M.VIEW["full"], "view": M.VIEW, "eye_cm": int(round(V.eye)),
        "vanishing": [int(round(V.vanishing()[0][0])), int(round(V.vanishing()[0][1]))],
        "light": "daytime, driving: cool daylight through smoked windows on both sides (soft, no sunbeams); the ceiling's five small lights warm; "
                 "the divider dim (smoked glass); the near corners and our own seat the darkest",
        "walk": walk,
        "maxScale": round(max(scale_at(X, Z) for X, Z in M.WALK), 2),
        "blocked": [],
        "planes": [
            {"id": "divider-up", "file": "divider-up.png", "plane": "back", "note": "the glass up: smoked, the headrests dim through it (first state)"},
            {"id": "divider-down", "file": "divider-down.png", "plane": "back", "alt": "divider-up",
             "note": "the glass slid down: the front of the car through the opening; exactly the same pixels as divider-up"},
            {"id": "ropes", "states": {"4": "ropes-4.png", "3": "ropes-3.png", "2": "ropes-2.png", "1": "ropes-1.png"}, "base": jy + 2,
             "note": "the bow on the cushion beside Joe; gone at 0. Its base is a row just in front of Joe's ground point: Joe is behind it, Ranger on the carpet or on the seat (sorted by the carpet under him) in front"},
            {"id": "bag", "file": "bag.png", "base": face_edge, "note": "goes when taken (its shadow with it)"},
            {"id": "juice", "file": "juice.png", "base": face_edge, "note": "goes when taken"},
            {"id": "clipboard", "file": "clipboard.png", "base": face_edge, "note": "goes when taken"},
            {"id": "front", "file": "front.png", "plane": "front", "note": "the seat we sit on (its bolster and cushion) and the two armrests"},
        ],
        "things": things,
        "marks": marks,
        "stands": {k: {"at": stand[k], "face": face[k], "scale": round(scale_at(*M.STANDS[k][0]), 3)} for k in M.STANDS},
        "windows": [{"id": i, "side": s, "poly": [[round(p[0], 1), round(p[1], 1)] for p in q]} for i, s, q in polys],
        "strip": {"file": "desert-strip.png", "row": row, "top": top, "speed": 90,
                  "note": "the strip's bottom edge sits on `row`; it is drawn behind the glass, clipped to `windows`. Driving forward, the "
                          "world goes by outward from the far end on both sides: to the LEFT in the left windows (speed 90) and to the RIGHT in "
                          "the right windows (speed -90): two strip effects, one for each side's windows"},
        "exits": [],
        "lights": {"ceiling": [fl(lx, lz, M.H) for lx, lz in M.LIGHTS], "note": "the ceiling's small lights (painted, warm): for a live glow if wanted"},
        "edges": {"long_seat_front": [seat_edge_far, seat_edge_near], "facing_seat_front": face_edge},
        "cutouts": {k: rect_xywh(b) for k, b in boxes.items() if not k.endswith("-own")},
    }
    json.dump(L, open(f"{OUT}/layout.json", "w"), indent=1)
    return L

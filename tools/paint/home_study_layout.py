"""layout.json for home-study: the numbers the game needs, MEASURED from the finished picture.

Every rect is the box round the pixels that really show that thing (found from what each ray of the picture
met), not a copy of the brief. Places on the floor (where to stand, the walk outline, the base lines of the
cut-outs) are the model's centimetres put through the same camera as the picture."""

import json

import numpy as np

from room import View
import home_study_model as M

OUT = "out/home-study"
W, H = 800, 600


def write(stA, stB, boxes, a_desk, a_front, wob=None):
    v = View(**M.VIEW)

    def fl(X, Z):
        x, y = v.pt(X, 0, Z)
        return [int(round(x)), int(round(y))]

    def rect_of(st, names, extra=None):
        ids = [st.names[n] for n in names if n in st.names]
        m = np.isin(st.pick(st.oid), ids)
        if wob is not None:
            m = wob(m.astype(np.float32)) > 0.5
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            return None
        r = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
        if extra:
            r = [min(r[0], extra[0]), min(r[1], extra[1]), max(r[2], extra[2]), max(r[3], extra[3])]
        return [r[0], r[1], r[2] - r[0], r[3] - r[1]]

    def rect_xywh(b):
        return [b[0], b[1], b[2] - b[0], b[3] - b[1]]

    mk = M.MARKS
    stand = {k: fl(*p) for k, p in mk.items()}
    size = {k: int(round(v.person(*p)[2])) for k, p in mk.items()}

    things = []

    def thing(id_, what, rect, at, face, **more):
        if rect is None:
            print("layout: nothing found for", id_)
            return
        t = {"id": id_, "what": what, "shape": {"rect": rect}, "stand": stand[at], "face": face}
        t.update(more)
        things.append(t)

    A, B = stA, stB
    thing("window", "the gable window, the night and the moon in it", rect_of(B, ["window"]), "atwindow", "N")
    thing("desk", "Dad's big old desk (cut-out desk.png, with the chair and the computer)", rect_of(A, ["desk", "lamp"]), "atdesk", "N")
    thing("computer", "the family computer, \"the mainframe\": a beige case and a fat monitor", rect_of(A, ["computer", "screen"]), "atdesk", "N",
          screen=rect_xywh(boxes["screen"]) if boxes.get("screen") else None)
    thing("note", "the yellow sticky note on the monitor's frame, top right (cut-out note.png)", rect_xywh(boxes["note"]) if boxes.get("note") else None, "atnote", "W",
          click={"rect": [boxes["note"][0] - 4, boxes["note"][1] - 4, boxes["note"][2] - boxes["note"][0] + 8, boxes["note"][3] - boxes["note"][1] + 8]} if boxes.get("note") else None)
    thing("corkboard", "the corkboard: lists, and the boy's drawings of the station wagon pinned over them", rect_of(B, ["corkboard"]), "atcork", "N")
    thing("wallmap", "the road map of the West: pins, red wool for the route, a shorter yellow piece cutting the corner", rect_of(B, ["wallmap"]), "atmap", "N")
    thing("machine", "the answering machine on the filing cabinet: a grey wedge, tape window, big buttons", rect_of(B, ["machine"]), "atmachine", "W",
          tape=rect_xywh(boxes["tape"]) if boxes.get("tape") else None)
    thing("cabinet", "the filing cabinet the machine stands on", rect_of(B, ["cabinet"]), "atmachine", "W")
    thing("shelves", "the low shelves of manuals and jars, with the shaded lamp", rect_of(B, ["shelves", "shelflamp"]), "atshelves", "E")
    thing("vault", "the family vault: a grey cash box with a dial and a label, at the near end of the shelves", rect_of(B, ["vault"]), "atvault", "E",
          open=rect_xywh(boxes["vault-open"]) if boxes.get("vault-open") else None)
    thing("globe", "the floor globe", rect_of(B, ["globe"]), "atglobe", "E")
    thing("banner", "the paper banner on a string between two rafters: TRIP HEADQUARTERS", rect_of(B, ["banner"]), "atbanner", "N")
    thing("door", "the door to the landing: its frame at the left edge, the leaf standing open (front plane)", rect_of(A, ["door", "landing"]), "atdoor", "W")
    thing("chair", "his desk chair, his cardigan over the back", rect_of(A, ["chair"]), "atdesk", "N")
    thing("aeroplane", "the model biplane on a thread, over the map", rect_of(B, ["aeroplane"]), "atmap", "N")
    thing("heap", "what would not fit in the car: the cooler, the tent in its bag, the box of maps (front plane)", rect_of(A, ["heap"]), "front", "S")
    thing("chest", "the old chest under the map", rect_of(B, ["chest"]), "atmap", "N")
    thing("calendar", "the calendar", rect_of(B, ["calendar"]), "atcork", "N")
    thing("rug", "the rug", [fl(M.RUG[0], M.RUG[3])[0], fl(M.RUG[0], M.RUG[2])[1], fl(M.RUG[1], M.RUG[3])[0] - fl(M.RUG[0], M.RUG[3])[0], fl(M.RUG[1], M.RUG[3])[1] - fl(M.RUG[0], M.RUG[2])[1]], "atbanner", "E")

    dz0, dz1, dh = M.DOORWAY
    px_ = M.PARTITION[0]
    door_rect = rect_of(A, ["door", "landing"])
    exit_poly = [[door_rect[0], door_rect[1]], [door_rect[0] + door_rect[2], door_rect[1] + 14], [door_rect[0] + door_rect[2], H], [door_rect[0], H]] if door_rect else []

    def at(X, Y, Z):
        x, y = v.pt(X, Y, Z)
        return [int(round(x)), int(round(y))]
    mx0, mx1, my0, my1, mz0, mz1 = M.MACHINE
    f = 6.4 / 37.2                                           # the machine's little counter window, on its sloping face
    lights = {
        "machine": at(mx0 + 36.5 * (mx1 - mx0) / 42.0, my0 + 4 + f * (my1 - my0 - 4), mz1 - f * (mz1 - mz0)),
        "desk-lamp": at(M.DESK[0] + 49, 76 + 45, M.DESK[4] + 39.5),
        "shelf-lamp": at(M.SHELF_LAMP[0], M.SHELVES[3] + 27, M.SHELF_LAMP[1]),
        "moon": at(M.WINDOW[0] + 0.70 * (M.WINDOW[1] - M.WINDOW[0]), M.WINDOW[2] + 0.66 * (M.WINDOW[3] - M.WINDOW[2]), -7),
        "screen": rect_xywh(boxes["screen"]) if boxes.get("screen") else None,
    }

    def foot(X0, X1, Z0, Z1):
        return [fl(X0, Z0), fl(X1, Z0), fl(X1, Z1), fl(X0, Z1)]
    gx, gz, _, gr = M.GLOBE
    feet = {                                                 # the floor under each thing that stands beside the walk outline (none is inside it)
        "desk": foot(M.DESK[0], M.DESK[1], M.DESK[4], M.DESK[5]), "chair": foot(M.CHAIR[0], M.CHAIR[1], M.CHAIR[4], M.CHAIR[5]),
        "cabinet": foot(M.CABINET[0], M.CABINET[1], M.CABINET[4], M.CABINET[5]), "shelves": foot(M.SHELVES[0], M.SHELVES[1], M.SHELVES[4], M.SHELVES[5]),
        "globe": foot(gx - 17, gx + 17, gz - 17, gz + 17), "chest": foot(444, 568, 4, 54),
        "heap": foot(M.HEAP[0], M.HEAP[1], M.HEAP[4], M.HEAP[5]), "pile": foot(M.PILE[0], M.PILE[1], M.PILE[4], M.PILE[5]),
        "door-leaf": [fl(M.PARTITION[0], M.DOORWAY[0]), fl(M.PARTITION[0] + M.LEAF[1] * 0.906, M.DOORWAY[0] + M.LEAF[1] * 0.423)],
    }

    dx0, dx1, _, _, _, dzf = M.DESK
    cx0, cx1, _, _, _, czf = M.CABINET
    sx0, _, _, _, sz0, sz1 = M.SHELVES
    desk_base = [fl(dx0, dzf), fl(dx1, dzf)]
    over_desk = [[desk_base[0][0], desk_base[0][1] + 1], [desk_base[1][0], desk_base[1][1] + 1]]
    L = {
        "id": M.ID, "horizon": M.VIEW["horizon"], "full": M.VIEW["full"], "view": M.VIEW, "eye_cm": int(round(v.eye)),
        "vanishing": [int(round(v.vanishing()[0][0])), int(round(v.vanishing()[0][1]))],
        "light": "night: desk lamp far left (warm, small), shaded lamp on the shelves at the right (warm), the moon through the gable window "
                 "(pale blue patch on the floor), the landing's lamp through the open door at the front left",
        "walk": [fl(X, Z) for X, Z in M.WALK],
        "blocked": [],                                       # nothing stands inside the outline: it is drawn round the furniture
        "feet": feet,
        "planes": [
            {"id": "desk", "file": "desk.png", "base": desk_base, "solid": foot(M.DESK[0], M.DESK[1], M.DESK[4], M.CHAIR[5]),
             "note": "desk, chair, computer (screen dark), lamp. Nobody can stand behind it; `solid` is the floor under desk and chair."},
            {"id": "screen", "states": {"offline": "screen-offline.png", "login": "screen-login.png", "map": "screen-map.png"}, "base": over_desk,
             "note": "just the lit glass, laid over the dark monitor of desk.png"},
            {"id": "note", "file": "note.png", "base": over_desk, "note": "shown until the note is taken"},
            {"id": "tape", "file": "tape-out.png", "base": [fl(cx0, czf), fl(cx1, czf)], "note": "the spilled loop, shown until it is wound back in"},
            {"id": "vault-open", "file": "vault-open.png", "base": [fl(sx0, sz0), fl(sx0, sz1)], "note": "lid up; covers the shut box of the backdrop exactly"},
            {"id": "front", "file": "front.png", "plane": "front", "note": "the door's wall, frame and open leaf at the left; the heap at the bottom; the suitcase and mat at the right"},
        ],
        "things": things,
        "exits": [{"to": "home-landing", "id": "door", "shape": {"poly": exit_poly}, "stand": stand["atdoor"], "face": "W"}],
        "marks": {"fromLanding": {k: stand[k] for k in ("mom", "bigsis", "lilsis")},
                  "mom": stand["mom"], "bigsis": stand["bigsis"], "lilsis": stand["lilsis"]},
        "stands": {k: {"at": stand[k], "grownup_px": size[k]} for k in mk},
        "cutouts": {k: rect_xywh(b) for k, b in boxes.items() if b},
        "lights": lights,                                    # where the game may draw its live lights (none of them is painted)
    }
    ad = np.nonzero(a_desk > 0.5)
    af = np.nonzero(a_front > 0.5)
    L["cutouts"]["desk"] = [int(ad[1].min()), int(ad[0].min()), int(ad[1].max() - ad[1].min() + 1), int(ad[0].max() - ad[0].min() + 1)]
    L["cutouts"]["front"] = [int(af[1].min()), int(af[0].min()), int(af[1].max() - af[1].min() + 1), int(af[0].max() - af[0].min() + 1)]
    json.dump(L, open(f"{OUT}/layout.json", "w"), indent=1)
    return L

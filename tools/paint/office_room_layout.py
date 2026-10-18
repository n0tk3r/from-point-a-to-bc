"""layout.json for office-room (the Comfortable Room): the numbers the scene writer needs, MEASURED from the finished
picture. OFFICE-17C.

Every shape is round the pixels that really show that thing (found from what each ray of the picture met), not a copy of
the brief. Places on the floor (where to stand, the walk outline, the base lines and the ground of the cut-outs) are the
model's centimetres put through the same camera as the picture.

    python3 office_room_layout.py check     draws layout.json over the comp: out/office-room-check.png"""

import json
import math
import sys

import numpy as np
from PIL import Image, ImageDraw

from room import View
import office_room_model as M
from office_room_kit import hull, simplify, inside, poly_of_mask, rect_of_mask

OUT = "out/office-room"
W, H = 800, 600
V = View(**M.VIEW)
SEAT = M.SEAT


def fl(X, Z, Y=0.0):
    x, y = V.pt(X, Y, Z)
    return [int(round(x)), int(round(y))]


def scale_at(X, Z):
    return round(175.0 * V.scale_at(X, Z) / 160.0, 3)


def write(stA, stB, covers, frames, wob=None):
    def mask_of(st, names):
        ids = [st.names[n] for n in names if n in st.names]
        return np.isin(st.pick(st.oid), ids)

    def rect_of(st, names, pad=1):
        return rect_of_mask(mask_of(st, names), pad)

    def poly_of(st, names, most=12, pad=1.0):
        return poly_of_mask(mask_of(st, names), most, pad)

    def poly_cover(name, most=12):
        return poly_of_mask(covers[name] > 0.5, most, 1.0)

    mk = M.MARKS
    stands = {k: {"at": fl(*p), "grownup_px": int(round(V.person(*p)[2] * 160.0 / 175.0 * 175.0 / 160.0))} for k, p in mk.items()}
    for k, p in mk.items():
        stands[k]["grownup_px"] = int(round(V.person(*p)[2]))
    walk = [fl(X, Z) for X, Z in M.WALK]
    seated = ("joe", "dale", "merle", "chair")
    for k, p in mk.items():
        if k not in seated and not inside(stands[k]["at"], walk):
            print("layout: the stand place", k, stands[k]["at"], "is outside the walk outline")

    things = []

    def thing(id_, what, shape, at, face, **more):
        if shape is None:
            print("layout: nothing found for", id_)
            return
        sh = {"poly": shape} if isinstance(shape[0], list) else {"rect": shape}
        t = {"id": id_, "what": what, "shape": sh, "stand": stands[at]["at"], "face": face}
        t.update(more)
        things.append(t)

    A, B = stA, stB
    # listed back to front: where two shapes overlap, the later one is on top
    thing("mirror", "the one-way mirror along the back wall: dark glass in a steel frame, a faint reflection of the room in it "
          "(the lamp, the cooler, the plant, the tubes). \"Somebody's back there eatin' chips.\"", poly_of(A, ["mirror", "mirrorframe"], 8),
          "atmirror", "N")
    thing("poster", "the poster: PECULIAR? REPORT IT. (a cartoon in two inks: a chain-link fence across the desert, and in the sky behind it a hole)",
          rect_of(A, ["poster"]), "atposter", "N")
    thing("sign", "the sign by the door: INTERVIEW ROOM C / THE COMFORTABLE ROOM / (small) THIS ROOM HAS BEEN RATED COMFORTABLE",
          rect_of(A, ["sign"]), "atsign", "N")
    thing("clock", "the wall clock over the door: twenty to two; its red second hand goes round (frames second-00..59)",
          rect_of(A, ["clock"], 2), "atclock", "N")
    thing("door", "the door: gray steel, a slit of wired glass with the hall's light in it, locked \"for your comfort\" (cut-outs door.png, "
          "door-open.png; the doorway and the hall beyond are painted in the backdrop)", poly_of(A, ["door", "doorcasing"], 10), "door", "N",
          planes=["door", "door-open"])
    thing("thermostat", "the thermostat by the door: a beige box, a small dial, a window with the number in it: 72, 77 or 81 "
          "(cut-outs thermostat-72/77/81)", rect_of(A, ["thermostat"], 3), "thermostat", "N", planes=["thermostat-72", "thermostat-77", "thermostat-81"])
    thing("intercom", "the intercom by the door: a speaker grille, a red button, DISPATCH / PRESS TO TALK (cut-outs intercom, intercom-lit)",
          rect_of(A, ["intercom", "intercombutton"], 3), "intercom", "N", planes=["intercom", "intercom-lit"])
    thing("lamp", "the floor lamp in the far corner: a rose-colored shade with a fringe, unplugged (the Office's idea of comfort; no "
          "unauthorized lighting)", poly_of(A, ["lamp"], 10), "atlamp", "NE", note="an extra: not in the brief's list")
    thing("cooler", "the water cooler: a big blue jug upside down, a red tap and a blue one (a bubble goes up now and then: frames bubble-*)",
          poly_of(A, ["cooler"], 10), "atcooler", "E")
    thing("cones", "the paper cones, in their tube on the cooler's side", rect_of(A, ["cones"], 3), "atcooler", "E")
    thing("chair-corner", "the fourth chair, in the corner under the grille (cut-out chair-corner.png): Grandpa Joe stands on its seat",
          poly_of(A, ["chair-corner"], 10), "atchair", "NW", plane="chair-corner")
    thing("vent", "the grille in the ceiling over the corner: big, slats, the duct's dark behind them (cut-outs vent, vent-eyes: two eyes in "
          "a black mask, when Ranger is up there)", poly_of(A, ["vent", "vent-slats", "vent-duct"], 8), "atchair", "NW",
          planes=["vent", "vent-eyes"])
    thing("speaker", "the building's speaker in the ceiling (Houston's voice)", rect_of(A, ["speaker"], 3), "atmirror", "N",
          note="an extra: not in the brief's list")
    thing("chair-dale", "Dale's chair, across the table: gray-blue plastic on chrome legs", poly_of(A, ["chair-dale"], 10), "atdale", "W")
    thing("chair-merle", "Merle's chair, across the table, the near one", poly_of(A, ["chair-merle"], 10), "atmerle", "W")
    thing("table", "the table: wood-grain laminate (no wood was harmed), a gray steel frame (cut-out table.png)", poly_of(A, ["table", "tableedge"], 12),
          "atjoe", "E", plane="table")
    thing("questionnaire", "the questionnaire on the table before Dale: forty-seven pages and a green one, a binder clip (cut-out "
          "questionnaire.png, while the suits are there)", rect_of(A, ["questionnaire"], 4), "atjoe", "E", plane="questionnaire")
    thing("chair-joe", "Grandpa Joe's chair, on the table's left side", poly_of(A, ["chair-joe"], 10), "atjoe", "N")
    thing("plant", "the plastic plant (cut-outs plant, plant-droop): it cannot droop. It does.", poly_cover("plant", 12), "atplant", "E",
          planes=["plant", "plant-droop"])
    thing("basket", "the wastebasket: steel mesh, crumpled pages of questionnaire in it (front plane)", poly_of(A, ["basket"], 10), "atbasket", "S",
          note="an extra: not in the brief's list")
    thing("filebox", "a box of spare questionnaires on the floor near us: QUESTIONNAIRE / FORM 7-C 47 PP. (front plane)", poly_of(A, ["filebox"], 10),
          "attable", "S", note="an extra: not in the brief's list")

    def foot(X0, X1, Z0, Z1, pad=0.0):
        return [fl(X0 - pad, Z0 - pad), fl(X1 + pad, Z0 - pad), fl(X1 + pad, Z1 + pad), fl(X0 - pad, Z1 + pad)]

    def circle(X, Z, r, n=10):
        return [fl(X + r * math.cos(a), Z + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]

    tx0, tx1, _, _, tz0, tz1 = M.TABLE
    h = M.CHAIR_W / 2
    chair_feet = {k: foot(X - h, X + h, Z - h, Z + h, 2.0) for k, (X, Z, f) in M.CHAIRS.items()}
    ccx, ccz = M.CORNER_CHAIR
    px, pz, pr = M.PLANT
    bx, bz, br, bh = M.BASKET
    table_base = 458
    back_line = [fl(30.0, 0.0), fl(200.0, 0.0)]
    corner_base = [fl(ccx - 24.0, ccz + 24.0), fl(ccx + 24.0, ccz + 24.0)]
    plant_base = [fl(px - pr, pz + pr * 0.6), fl(px + pr * 0.4, pz + pr)]
    planes = [
        {"id": "vent", "file": "vent.png", "plane": "back", "note": "the grille, plain (the backdrop has it too): show it, or vent-eyes"},
        {"id": "vent-eyes", "file": "vent-eyes.png", "plane": "back", "alt": "vent",
         "note": "the same grille with two eyes in a black mask shining between its slats: while Ranger is at the grille over this room"},
        {"id": "thermostat-72", "file": "thermostat-72.png", "plane": "back", "note": "72 (the backdrop has it too); until #16"},
        {"id": "thermostat-77", "file": "thermostat-77.png", "plane": "back", "alt": "thermostat-72", "note": "77: warming (office.heat 73..79)"},
        {"id": "thermostat-81", "file": "thermostat-81.png", "plane": "back", "alt": "thermostat-72", "note": "81, the number red: hot (office.heat 80+)"},
        {"id": "intercom", "file": "intercom.png", "plane": "back", "note": "its button dark (the backdrop has it too)"},
        {"id": "intercom-lit", "file": "intercom-lit.png", "plane": "back", "alt": "intercom", "note": "the button lit, while it is pressed"},
        {"id": "door", "file": "door.png", "base": back_line,
         "note": "the leaf, shut. Hidden, the doorway shows the hall (painted in the backdrop); door-open shows the leaf swung out into the hall"},
        {"id": "door-open", "file": "door-open.png", "base": back_line, "alt": "door", "note": "the leaf swung out into the hall (it opens out), seen past the jamb"},
        {"id": "doorframe", "file": "doorframe.png", "base": back_line,
         "note": "the back wall round the doorway and the steel casing: whoever is in the hall (feet above the wall's line) is behind it, seen only through the opening"},
        {"id": "chair-corner", "file": "chair-corner.png", "base": corner_base,
         "solid": foot(ccx - 22, ccx + 22, ccz - 22, ccz + 22, 3.0),
         "note": "the fourth chair. Grandpa Joe standing on its seat, and Ranger on it, are sorted as if on the floor just in front of it (marks `chair` and `vent`: `base`)"},
        {"id": "table", "file": "table.png", "base": table_base, "solid": foot(tx0, tx1, tz0, tz1, 2.0),
         "note": "a row: whoever's feet (or seated ground point) are above it is behind the table: the three at it (Grandpa Joe's knees go under its top) and anyone between it and the back wall; whoever is in front of it, below"},
        {"id": "questionnaire", "file": "questionnaire.png", "base": table_base, "note": "on the table before Dale: lay it straight after the table; hide it when the suits take it (#17)"},
        {"id": "plant", "file": "plant.png", "base": plant_base, "solid": circle(px, pz, pr + 3, 8),
         "note": "upright (until the room is hot)"},
        {"id": "plant-droop", "file": "plant-droop.png", "base": plant_base, "alt": "plant", "note": "drooping (office.heat 78+, say)"},
        {"id": "front", "file": "front.png", "plane": "front", "note": "the wastebasket near us at the left, and the box of spare questionnaires on the floor"},
    ]
    blocked = [chair_feet["joe"], chair_feet["dale"], chair_feet["merle"], circle(M.LAMP[0], M.LAMP[1], 15, 8)]

    marks = {
        "joe": {"at": fl(*mk["joe"]), "face": "E", "scale": scale_at(*mk["joe"]), "seat_cm": SEAT,
                "seat_height_px": int(round(V.pt(mk["joe"][0], 0, mk["joe"][1])[1] - V.pt(mk["joe"][0], SEAT, mk["joe"][1])[1])),
                "note": "Grandpa Joe seated at the table, facing the two of them: the floor under his hips (his chair's middle); seated there his hips are seat_height_px above it. Behind the table's row (458), so its top covers his knees"},
        "dale": {"at": fl(*mk["dale"]), "face": "W", "scale": scale_at(*mk["dale"]), "seat_cm": SEAT,
                 "seat_height_px": int(round(V.pt(mk["dale"][0], 0, mk["dale"][1])[1] - V.pt(mk["dale"][0], SEAT, mk["dale"][1])[1])),
                 "note": "Dale seated across the table, the far one (he reads the questions); the table covers him below its top"},
        "merle": {"at": fl(*mk["merle"]), "face": "W", "scale": scale_at(*mk["merle"]), "seat_cm": SEAT,
                  "seat_height_px": int(round(V.pt(mk["merle"][0], 0, mk["merle"][1])[1] - V.pt(mk["merle"][0], SEAT, mk["merle"][1])[1])),
                  "note": "Merle seated across the table, the near one (he writes it down); the table covers him below its top"},
        "chair": {"at": fl(ccx, ccz, SEAT), "floor": fl(ccx, ccz), "scale": scale_at(ccx, ccz), "base": fl(ccx, ccz + 30.0)[1], "face": "S",
                  "seat_row": fl(ccx, ccz, SEAT)[1],
                  "note": "Grandpa Joe standing on the corner chair, his feet on its seat: draw him at `scale` (the floor's under him) with his feet at `at`, sorted by `base` (a row just in front of the chair). Reaching up, his hands are at the grille (`vent_hands`). He gets up from `atchair`"},
        "vent": {"at": fl(ccx + 4.0, ccz + 2.0, SEAT), "scale": scale_at(ccx, ccz), "base": fl(ccx, ccz + 30.0)[1], "face": "E",
                 "grille": fl((M.VENT[0] + M.VENT[1]) / 2, (M.VENT[2] + M.VENT[3]) / 2, M.H),
                 "hand_to": fl(ccx + 4.0, ccz + 2.0, 220.0),
                 "note": "under the grille's middle: on the corner chair's SEAT (not the floor, not the table). Ranger comes down onto it (draw his frames at `scale`, sorted by `base`), and climbs back from it; a thing handed down is handed to Grandpa Joe on the chair at `hand_to` (just under the slats); one dropped with nobody there lands on this seat. `grille`: the middle of the grille (where the eyes are)"},
        "vent_hands": fl(ccx + 6.0, ccz + 6.0, M.H - 8.0),
        "door": fl(*mk["door"]), "door_face": "S",
        "opal": fl(*mk["opal"]), "opal_face": "E",
        "intercom": fl(*mk["intercom"]), "intercom_face": "N",
        "thermostat": fl(*mk["thermostat"]), "thermostat_face": "N",
        "hall": fl(109.0, -60.0), "hall_note": "in the hall, just outside the doorway (behind the doorframe: seen through the opening): where Opal and the suits come from and go to",
    }
    fx = []
    if "second" in frames:
        f = frames["second"]
        fx.append({"id": "second", "what": "the clock's red second hand going round", "at": f["at"], "foot": f["foot"], "frames": f["files"],
                   "fps": 1, "plane": "back", "rect": f["rect"], "note": "60 frames, one a second, from twelve"})
    if "bubble" in frames:
        f = frames["bubble"]
        fx.append({"id": "bubble", "what": "a bubble going up in the cooler's jug, now and then", "at": f["at"], "foot": f["foot"],
                   "frames": f["files"], "fps": 6, "plane": "back", "rect": f["rect"],
                   "note": "bubble-0..5 rising, then bubble-none (the jug at rest): list bubble-none twenty or thirty times after the six, so that it is now and then"})
    L = {
        "id": M.ID, "horizon": M.VIEW["horizon"], "full": M.VIEW["full"], "view": M.VIEW, "eye_cm": round(V.eye),
        "vanishing": [[round(c) for c in p] if p else None for p in V.vanishing()],
        "light": "fluorescent: four light panels in the ceiling, two tubes each behind a prismatic lens, pale and a little green; flat and even, "
                 "the brightest pool on the table; soft shadows straight down under the table and the chairs; the corners and the foreground a "
                 "little darker, the far corner cooler; the hall through the doorway a little brighter. The lamp in the corner is unplugged",
        "fx_note": "The clock's second hand turns (frames second-*, 1 fps) and a bubble goes up in the cooler now and then (bubble-*). The light "
                   "panels are painted lit; a live flicker over one of them (`lights.panels`) would suit a room that is getting hot.",
        "walk": walk,
        "walk_note": "one outline: the floor round the table, clear of the corner chair, the lamp, the cooler and the plant; to the corner chair's "
                     "front (atchair), to the door, the thermostat, the intercom and the mirror along the back wall. Its front edge runs on a slant "
                     "where a grown-up is about 195 px tall (the camera is turned); it keeps 14 px or more off the walls",
        "blocked": blocked, "planes": planes, "things": things, "marks": marks,
        "stands": stands, "fx": fx,
        "cutouts": {n: rect_of_mask(c > 0.5, 0) for n, c in covers.items()},
        "lights": {"panels": [[fl(t[0], t[2], M.H), fl(t[1], t[2], M.H), fl(t[1], t[3], M.H), fl(t[0], t[3], M.H)] for t in M.TROFFERS],
                   "note": "the four light panels' corners in the picture (for a live glow or a flicker)"},
        "exits": [],
        "exits_note": "none: the door is locked for his comfort. People come and go through it by script (mark `hall`, outside it; `door`, inside it)",
    }
    json.dump(L, open(f"{OUT}/layout.json", "w"), indent=1)
    print("layout.json:", len(things), "things,", len(planes), "planes")
    return L


def check(folder=None, out="out/office-room-check.png"):
    """Every shape, mark, stand, base and the walk drawn over the comp."""
    folder = folder or OUT
    L = json.load(open(f"{folder}/layout.json"))
    im = Image.open("out/office-room-comp-start.png").convert("RGB")
    d = ImageDraw.Draw(im)
    d.line([tuple(p) for p in L["walk"]] + [tuple(L["walk"][0])], fill=(120, 255, 140), width=1)
    for b in L["blocked"]:
        d.line([tuple(p) for p in b] + [tuple(b[0])], fill=(255, 90, 90), width=1)
    for t in L["things"]:
        sh = t["shape"]
        if "poly" in sh:
            d.line([tuple(p) for p in sh["poly"]] + [tuple(sh["poly"][0])], fill=(255, 220, 90), width=1)
        else:
            x, y, w, h = sh["rect"]
            d.rectangle([x, y, x + w, y + h], outline=(255, 220, 90))
        sx, sy = t["stand"]
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(90, 200, 255))
        d.text((sh["poly"][0][0] if "poly" in sh else sh["rect"][0], (sh["poly"][0][1] if "poly" in sh else sh["rect"][1]) - 10), t["id"], fill=(255, 255, 255))
    for p in L["planes"]:
        b = p.get("base")
        if isinstance(b, list):
            d.line([tuple(b[0]), tuple(b[1])], fill=(255, 120, 255), width=2)
        elif isinstance(b, (int, float)):
            d.line([(0, b), (800, b)], fill=(255, 120, 255), width=1)
    for k, m in L["marks"].items():
        if isinstance(m, dict):
            x, y = m["at"]
            d.ellipse([x - 3, y - 3, x + 3, y + 3], outline=(255, 255, 255))
            d.text((x + 4, y - 4), k, fill=(255, 255, 255))
        elif isinstance(m, list) and len(m) == 2 and isinstance(m[0], int):
            d.ellipse([m[0] - 3, m[1] - 3, m[0] + 3, m[1] + 3], outline=(200, 255, 255))
            d.text((m[0] + 4, m[1] - 4), k, fill=(200, 255, 255))
    im.save(out)
    print(out)


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "check":
    check()

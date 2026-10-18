"""layout.json for office-property (Property & Effects): the numbers the scene writer needs, MEASURED from the finished
picture. OFFICE-17C.

Every shape is round the pixels that really show that thing (found from what each ray of the picture met). Places on the
floor (where to stand, the walk outline, the base lines) are the model's centimetres put through the same camera.

    python3 office_property_layout.py check     draws layout.json over the comp: out/office-property-check.png"""

import json
import math
import sys

import numpy as np
from PIL import Image, ImageDraw

from room import View
import office_property_model as M
import office_property_things as T
from office_room_kit import inside, poly_of_mask, rect_of_mask

OUT = "out/office-property"
W, H = 800, 600
V = View(**M.VIEW)


def fl(X, Z, Y=0.0):
    x, y = V.pt(X, Y, Z)
    return [int(round(x)), int(round(y))]


def scale_at(X, Z):
    return round(175.0 * V.scale_at(X, Z) / 160.0, 3)


def write(stA, stB, covers):
    def mask_of(st, names, where=None):
        ids = [st.names[n] for n in names if n in st.names]
        m = np.isin(st.pick(st.oid), ids)
        if where is not None:
            X, Y, Z = (st.pick(a) for a in st.places())
            m = m & where(X, Y, Z)
        return m

    def rect_of(names, pad=1):
        return rect_of_mask(mask_of(stA, names), pad)

    def poly_of(names, most=12, pad=1.0, where=None):
        return poly_of_mask(mask_of(stA, names, where), most, pad)

    def poly_cover(name, most=12):
        return poly_of_mask(covers[name] > 0.5, most, 1.0)

    mk = M.MARKS
    stands = {k: {"at": fl(*p), "grownup_px": int(round(V.person(*p)[2]))} for k, p in mk.items()}
    walk = [fl(X, Z) for X, Z in M.WALK]
    for k, p in mk.items():
        if k not in ("opal", "counter", "vent") and not inside(stands[k]["at"], walk):
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

    # back to front: where two shapes overlap, the later one is on top
    thing("shelves-left", "the left run of shelving: gray steel, floor to ceiling, every thing on it tagged", poly_of(["shelfpost-L", "shelf-L", "shelflip-L"], 8),
          "atleft1", "W")
    thing("shelves-right", "the right run of shelving, seen along its edge: archive boxes by the decade", poly_of(["shelfpost-R", "shelf-R", "shelflip-R"], 8),
          "atright0", "E")
    thing("boxes", "archive boxes, labelled FORM 7 by the decade (1971-1979, 1980-1989, and so on), on both runs", poly_of(["boxes-R"], 10),
          "atright1", "E", note="the right run's boxes; the left run's are `boxes-left`")
    thing("boxes-left", "archive boxes on the left run: FORM 7 (1971-1979) and the rest", poly_of(["boxes-L"], 10, where=lambda X, Y, Z: Z > 440),
          "atleft3", "W", note="the near unit's (left-4)")
    thing("window", "Opal's window onto the hall: a sliding glass window in an aluminium frame, the hall's light beyond it (its corkboard, "
          "its notices)", poly_of(["window", "hall", "reveal", "ledge"], 8, where=lambda X, Y, Z: (X > M.WINDOW[0] - 4) & (X < M.WINDOW[1] + 4) & (Y > M.WINDOW[2] - 4)),
          "atwindow", "N")
    thing("sign", "the small sign over the window: THIS WINDOW CLOSES AT 1700", rect_of(["sign"], 3), "atsign", "N")
    thing("bell", "the bell, on the hall's side of the glass (RING FOR SERVICE): out of reach from in here", rect_of(["bell"], 4), "atwindow", "N")
    thing("door", "the door to the hall: gray steel, a slit of wired glass, a card: PROPERTY & EFFECTS: STAFF (cut-outs door, door-open)",
          poly_of(["door", "doorcasing"], 10), "door", "N", planes=["door", "door-open"])
    thing("cabinet", "a filing cabinet in the corner: four drawers (forty-one statements of nothing, filed)", poly_of(["cabinet"], 8), "atcabinet", "NW",
          note="an extra: not in the brief's list")
    thing("counter", "Opal's counter along the window: a wood-grain top, a steel cabinet under it; claim forms, a wire tray, a pencil cup",
          poly_of(["counter", "forms", "tray", "pencils"], 10), "atwindow", "N", plane="wall")
    thing("stamp", "her date stamp on its ink pad (THUNK)", rect_of(["stamp"], 3), "atstamp", "N")
    thing("stool", "Opal's stool: a round seat in green vinyl on four chrome legs", poly_of(["stool"], 10), "atstool", "N")
    thing("knitting", "her knitting basket, two balls of gray wool and the needles in it, and the scarf she has been knitting since about 1990 in "
          "the regulation colour, trailing out of it and away down the aisle (all of it is on the floor: people walk over it)",
          poly_of(["basket", "scarf"], 10, where=lambda X, Y, Z: (Z < M.BASKET[1] + 70)), "atbasket", "N")
    for kind, ui, ys, zc in M.LEFT_THINGS:
        nm = T.THING_NAME[kind]
        what = {
            "sandal": "a Roman sandal, tagged 1951 (the first thing ever entered into Property & Effects)",
            "oillamp": "a clay oil lamp, its nozzle black with soot, tagged",
            "cup": "a tin cup, dented, tagged",
            "hat": "a cowboy hat bleached white, tagged",
            "feather": "a goose feather in a small jar, tagged",
            "cassette": "a cassette tape in its case, somebody's writing on the label, tagged",
            "horseshoe": "a horseshoe, rusty, tagged",
            "gnome": "a garden gnome, tagged (nobody knows)",
            "lantern": "a kerosene lantern, tagged (an extra)",
            "ball": "a bowling ball, tagged (an extra)",
        }[nm]
        stand = {1: "atleft1", 2: "atvent", 3: "atleft3", 4: "atleft3"}[ui]
        thing(nm, what, poly_of([nm, nm + "-tag"], 8), stand, "W")
    thing("cone", "a traffic cone on the right run's lowest shelf, tagged (an extra)", poly_of(["cone", "cone-tag"], 8), "atright0", "E")
    thing("banjo", "the banjo (damaged), tagged No. 3117: standing in the tall bay on the lowest shelf, its head broken right through, the rim, "
          "the neck and the strings whole (cut-out banjo.png; gone once Opal takes it)", poly_cover("banjo", 12), "banjo", "W", plane="banjo")
    thing("vent", "the grille in the ceiling over the left run: slats, the duct's dark behind them (cut-outs vent, vent-eyes: two eyes in a "
          "black mask when Ranger is up there)", poly_of(["vent", "vent-slats", "vent-duct"], 8), "atvent", "NW", planes=["vent", "vent-eyes"])
    thing("speaker", "the building's speaker in the ceiling (Houston's voice)", rect_of(["speaker"], 3), "atwindow", "N", note="an extra")
    thing("cart", "a utility cart parked by the right run: an archive box and a clipboard on it (front plane)", poly_cover("front", 12) and
          poly_of(["cart", "cartbox", "clipboard"], 10), "atright1", "SE", note="an extra: the foreground")
    thing("kickstool", "a round kick stool on casters (front plane)", poly_of(["kickstool"], 10), "front", "S", note="an extra: the foreground")
    thing("floorboxes", "two archive boxes on the floor by the left run (front plane)", poly_of(["floorbox"], 10), "atleft3", "SW", note="an extra")

    wall_base = [fl(M.COUNTER[0] - 6.0, 0.0), fl(M.DOOR[1] + 20.0, 0.0)]
    planes = [
        {"id": "vent", "file": "vent.png", "plane": "back", "note": "the grille, plain (the backdrop has it too): show it, or vent-eyes"},
        {"id": "vent-eyes", "file": "vent-eyes.png", "plane": "back", "alt": "vent",
         "note": "the same grille, two eyes in a black mask shining between its slats: while Ranger is at the grille over this room"},
        {"id": "wall", "file": "wall.png", "base": wall_base,
         "note": "the far wall round the window and the door, the window's frame, the counter and everything on it, the door's casing, the sign: "
                 "whoever is in the hall (feet above this line) is behind it, seen through the glass or the doorway; Opal on her stool is in front of it"},
        {"id": "door", "file": "door.png", "base": wall_base, "note": "the leaf, shut. Hidden, the doorway shows the hall (painted in the backdrop)"},
        {"id": "door-open", "file": "door-open.png", "base": wall_base, "alt": "door", "note": "the leaf swung out into the hall (it opens out), seen past the jamb"},
        {"id": "receipt", "file": "receipt.png", "base": wall_base, "alt": True,
         "note": "the receipt lying on the counter where it lands (#18): show it after the wall; absent before, and after Opal picks it up"},
        {"id": "banjo", "file": "banjo.png", "base": [fl(M.LEFT_X[1], M.LEFT_Z[2][0]), fl(M.LEFT_X[1], M.LEFT_Z[2][1])],
         "note": "the banjo in its bay (until Opal takes it: then hide it; the backdrop has the bay empty). Its base is the left run's face along the "
                 "bay: everybody in the aisle is in front of it"},
        {"id": "front", "file": "front.png", "plane": "front", "note": "the cart, the kick stool and the boxes on the floor near us: everybody passes behind"},
    ]
    sx, sz, sh, sr = M.STOOL
    bx, bz, br, bh = M.BASKET

    def circle(X, Z, r, n=10):
        return [fl(X + r * math.cos(a), Z + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]
    blocked = [circle(sx, sz, sr + 4, 8), circle(bx, bz, br + 3, 8)]
    rx, ry, rz = M.RANGER_SHELF
    c, n, up, across = T.banjo_frame()
    vcx, vcz = (M.VENT[0] + M.VENT[1]) / 2, (M.VENT[2] + M.VENT[3]) / 2
    marks = {
        "opal": {"at": fl(sx, sz), "face": "N", "scale": scale_at(sx, sz), "seat_cm": sh, "seat": round(sh / 175.0, 3),
                 "seat_height_px": int(round(V.pt(sx, 0, sz)[1] - V.pt(sx, sh, sz)[1])),
                 "note": "Opal on her stool at the window, her back to the shelves (she faces the window: yaw 180): the floor under her hips. The stool's seat "
                         "is 66 cm, so seat her with the rig's sit pose at `seat` (a share of a grown-up's height: sit(0, {seat: 0.377}))"},
        "vent": {"at": [int(round(v)) for v in V.pt(rx, ry, rz)], "scale": scale_at(rx, rz), "base": fl(rx, rz)[1], "face": "E",
                 "grille": [int(round(v)) for v in V.pt(vcx, M.H, vcz)],
                 "note": "on the left run's top shelf, right under the grille: where Ranger lands if he comes down, and from where he climbs back (draw his "
                         "frames at `scale`, sorted by `base`: he is nearer than anybody in the aisle). `grille`: the grille's middle, where the eyes are, and "
                         "where a thing dropped through it starts"},
        "counter": {"at": [int(round(v)) for v in V.pt(M.RECEIPT[0], M.COUNTER[3], M.RECEIPT[1])], "scale": scale_at(M.RECEIPT[0], M.RECEIPT[1]),
                    "base": wall_base,
                    "note": "where the receipt lands on the counter (#18): at its front edge, left of Opal's place (she is not in front of it), its near half "
                            "hanging over the edge so that it shows (cut-out receipt.png). Dropped through the grille it flutters down the aisle from "
                            "`vent.grille` to here (about four metres along, a metre and a half down)"},
        "banjo": {"at": [int(round(v)) for v in V.pt(*c)], "stand": fl(*mk["banjo"]), "face": "W", "scale": scale_at(*mk["banjo"]),
                  "top": [int(round(v)) for v in V.pt(*(c + up * (M.BANJO_LEN - M.BANJO_POT / 2)))],
                  "note": "`at`: the middle of the banjo's pot, in its bay on the lowest shelf; `top`: its headstock. Opal takes it from `stand` (the aisle in "
                          "front of the bay, as near us as a grown-up walks: 199 px)"},
        "door": fl(*mk["door"]), "door_face": "S",
        "hall": fl(343.0, -70.0), "hall_note": "in the hall, just outside the door (behind the wall's cut-out: seen through the doorway): where Opal goes, and comes back from",
        "hallwindow": fl(180.0, -80.0), "hallwindow_note": "in the hall at the window, on the far side of the glass (behind the wall's cut-out)",
    }
    L = {
        "id": M.ID, "horizon": M.VIEW["horizon"], "full": M.VIEW["full"], "view": M.VIEW, "eye_cm": round(V.eye),
        "vanishing": [[round(v) for v in p] if p else None for p in V.vanishing()],
        "light": "fluorescent: three light panels down the aisle, pale and a little green; the shelves' bays darker under each shelf; the hall beyond "
                 "Opal's window brighter than the room, a little of its light on her counter",
        "walk": walk,
        "walk_note": "the aisle from the window and the door to where a grown-up is about 200 px tall (its front edge slants: the camera is turned); "
                     "clear of both runs of shelving by 17 cm and more, so that nobody needs a shelf's cut-out",
        "blocked": blocked, "planes": planes, "things": things, "marks": marks, "stands": stands, "fx": [],
        "cutouts": {n: rect_of_mask(c_ > 0.5, 0) for n, c_ in covers.items()},
        "lights": {"panels": [[fl(t[0], t[2], M.H), fl(t[1], t[2], M.H), fl(t[1], t[3], M.H), fl(t[0], t[3], M.H)] for t in M.TROFFERS],
                   "note": "the three light panels' corners in the picture (for a live glow or a flicker)"},
        "exits": [],
        "exits_note": "none for the leads: Grandpa Joe is locked in his room and Ranger comes and goes by the grille (mark `vent`). Opal goes by the door "
                      "(`door` inside it, `hall` outside it)",
    }
    json.dump(L, open(f"{OUT}/layout.json", "w"), indent=1)
    print("layout.json:", len(things), "things,", len(planes), "planes")
    return L


def check(folder=None, out="out/office-property-check.png"):
    folder = folder or OUT
    L = json.load(open(f"{folder}/layout.json"))
    im = Image.open("out/office-property-comp-start.png").convert("RGB")
    d = ImageDraw.Draw(im)
    d.line([tuple(p) for p in L["walk"]] + [tuple(L["walk"][0])], fill=(120, 255, 140), width=1)
    for b in L["blocked"]:
        d.line([tuple(p) for p in b] + [tuple(b[0])], fill=(255, 90, 90), width=1)
    for t in L["things"]:
        sh = t["shape"]
        if "poly" in sh:
            d.line([tuple(p) for p in sh["poly"]] + [tuple(sh["poly"][0])], fill=(255, 220, 90), width=1)
            x0, y0 = sh["poly"][0]
        else:
            x, y, w, h = sh["rect"]
            d.rectangle([x, y, x + w, y + h], outline=(255, 220, 90))
            x0, y0 = x, y
        sx, sy = t["stand"]
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(90, 200, 255))
        d.text((x0, y0 - 10), t["id"], fill=(255, 255, 255))
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

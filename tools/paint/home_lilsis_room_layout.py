"""layout.json for Little Sister's room: every number goes through the room's one camera, from the measurements
the picture was painted with (home_lilsis_room_model.py), and the cut-outs' boxes are read off the finished files.

    python3 home_lilsis_room_layout.py            -> out/home-lilsis-room/layout.json"""
import json
import os

import numpy as np
from PIL import Image

import home_lilsis_room_model as M
from room import View

OUT = "out/home-lilsis-room"
v = View(**M.VIEW)


def px(X, Z, Y=0.0):
    x, y = v.pt(X, Y, Z)
    return [int(round(x)), int(round(y))]


def rect3(pts):
    """Picture box [x, y, w, h] round some places in the room, kept inside the picture."""
    q = v.poly(pts)
    xs, ys = [p[0] for p in q], [p[1] for p in q]
    x0, y0, x1, y1 = max(0, min(xs)), max(0, min(ys)), min(800, max(xs)), min(600, max(ys))
    return [int(round(x0)), int(round(y0)), int(round(x1 - x0)), int(round(y1 - y0))]


def box3(b, top=None, grow=0.0):
    X0, X1, Y0, Y1, Z0, Z1 = b
    Y1 = top if top is not None else Y1
    return rect3([(x, y, z) for x in (X0 - grow, X1 + grow) for y in (Y0, Y1) for z in (Z0, Z1)])


def alpha_box(name):
    path = f"{OUT}/{name}.png"
    if not os.path.exists(path):
        return None
    a = np.asarray(Image.open(path).convert("RGBA"))[..., 3]
    ys, xs = np.where(a > 0)
    return [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)] if len(ys) else None


def layout(signs=None):
    walk = [[int(round(x)), int(round(y))] for x, y in v.poly([(X, 0, Z) for X, Z in M.WALK])]
    blocked = [[[int(round(x)), int(round(y))] for x, y in v.poly([(X, 0, Z) for X, Z in poly])] for poly in M.BLOCKED]
    mk = {k: px(*xz) for k, xz in M.MARKS.items()}
    wx0, wx1, wy0, wy1 = M.WINDOW
    cx0, cx1, cy0, cy1 = M.CHART
    dx0, dx1, dy0, dy1 = M.DRAWINGS
    a, b = v.pt(2, 0, 404), v.pt(199, 0, 404)
    fort_base = [[0, int(round(a[1] + (b[1] - a[1]) * (0 - a[0]) / (b[0] - a[0])))], [int(round(b[0])), int(round(b[1]))]]
    tp = M.TEAPARTY
    tea_base = [px(tp[0], tp[5]), px(tp[1], tp[5])]
    door_rect = rect3([(M.DOOR_X, y, z) for y in (0, M.DOOR_H + 8) for z in (M.DOOR_Z[0], M.DOOR_Z[1] + 8)] + [(M.DOOR_X + 40, 0, M.DOOR_Z[1] + 8)])
    door_rect = [door_rect[0], door_rect[1], 800 - door_rect[0], 600 - door_rect[1]]
    fort_rect = alpha_box("fort") or box3(M.FORT)
    flash_rect = alpha_box("flashlight") or rect3([(134, 0, 404), (164, 10, 410)])
    tea_rect = alpha_box("teaparty") or box3(M.TEAPARTY)
    pil = M.PILLOW
    lt = M.LAMPTABLE
    mx, my, mz = M.MOBILE
    nest = M.NEST
    things = [
        dict(id="window", what="the gable window: the night, the tree and the moon; chicken curtains", shape={"rect": rect3([(wx0 - 50, wy0 - 28, 0), (wx1 + 50, wy1 + 24, 0)])}, stand=mk["atwindow"], face="N"),
        dict(id="drawings", what="her drawings on the gable, most of them chickens (the big one: five stick people, a red car, a chicken on its roof)", shape={"rect": rect3([(dx0, dy0, 0), (dx1 - 38, dy1, 0)])}, stand=mk["atflock"], face="N"),
        dict(id="chart", what="THE CHICKEN CHART: a poster she made, rows of chickens in crayon, each different, each labelled; its title reads MY CHICKENS", shape={"rect": rect3([(cx0, cy0, 0), (cx1, cy1, 0)])}, stand=mk["atchart"], face="N"),
        dict(id="flock", what="the flock: a mountain of stuffed animals on her beanbag, the stuffed chickens on top and in front (a rooster with a felt tail, white hens, a speckled one, chicks)", shape={"rect": box3(M.FLOCK, top=126)}, stand=mk["atflock"], face="W"),
        dict(id="bed", what="her bed: a quilt of hens, heaped with stuffed animals", shape={"rect": box3(M.BED, top=112, grow=2)}, stand=mk["atbed"], face="E"),
        dict(id="pillow", what="the pillow: one round place kept free, and propped at the back of it a paper sign that reads RESERVED", shape={"rect": rect3([(pil[0], 46, 250), (pil[1], 46, 250), (pil[0], 92, 208), (pil[1], 92, 208)])}, stand=mk["atbed"], face="E"),
        dict(id="teaparty", what="the tea party: a low table set for tea, and every guest is a chicken (cut-out teaparty.png)", shape={"rect": tea_rect}, stand=mk["atteaparty"], face="E"),
        dict(id="nest", what="the nest: a cardboard box lettered NEST, straw, a stuffed hen sitting, plastic eggs (front plane)", shape={"rect": box3((nest[0] - 14, nest[1] + 14, 0, 76, nest[4], nest[5]))}, stand=mk["atnest"], face="S"),
        dict(id="coop", what="the toy hen house: the dollhouse, lettered HEN HOUSE, a hen at every lit window, a ramp to the front door (front plane)", shape={"rect": box3((M.COOP[0] - 4, M.COOP[1] + 4, 0, M.COOP[3] + 12, M.COOP[4] + 30, M.COOP[5] + 30))}, stand=px(250, 398), face="S"),
        dict(id="fort", what="the blanket fort: two chairs, a clothes-horse, every blanket she owns; NO BIG SISTERS", shape={"rect": fort_rect}, stand=mk["atfort"], face="W"),
        dict(id="flashlight", what="her flashlight, just inside the fort's way in (cut-out flashlight.png; it can be taken)", shape={"rect": flash_rect}, stand=mk["atfort"], face="W"),
        dict(id="door", what="the door to the landing: its open leaf and frame at the right edge (front plane)", shape={"rect": door_rect}, stand=mk["atdoor"], face="E"),
        # things without a place in the brief's list, in case a line wants them
        dict(id="lamp", what="the rooster lamp on her bedside table (lit)", shape={"rect": box3((lt[0] - 14, lt[1] + 14, 0, 128, lt[4], lt[5]))}, stand=mk["atbed"], face="N"),
        dict(id="nightlight", what="the egg-shaped night-light on the floor by the flock (lit)", shape={"rect": rect3([(274, 0, 40), (302, 34, 40)])}, stand=mk["atflock"], face="N"),
        dict(id="mobile", what="a mobile of felt chickens, hung from a rafter (front plane)", shape={"rect": rect3([(mx - 34, my + 4, mz), (mx + 34, my - 68, mz)])}, stand=mk["atbed"], face="N"),
        dict(id="coat", what="her small yellow coat on its peg, her red boots under it", shape={"rect": rect3([(580, 0, 0), (620, 118, 0), (584, 0, 26)])}, stand=mk["atchart"], face="NE"),
        dict(id="rug", what="a rug like a fried egg", shape={"rect": rect3([(M.EGGRUG[0] - M.EGGRUG[2], 0, M.EGGRUG[1] - M.EGGRUG[3]), (M.EGGRUG[0] + M.EGGRUG[2], 0, M.EGGRUG[1] + M.EGGRUG[3]), (M.EGGRUG[0] - M.EGGRUG[2], 0, M.EGGRUG[1] + M.EGGRUG[3]), (M.EGGRUG[0] + M.EGGRUG[2], 0, M.EGGRUG[1] - M.EGGRUG[3])])}, stand=px(M.EGGRUG[0], M.EGGRUG[1] - 72), face="S"),
        dict(id="books", what="picture books in a low crate, one leaning against it with a hen on its cover (front plane)", shape={"rect": box3(M.CRATE, top=38, grow=2)}, stand=mk["atfort"], face="S"),
        dict(id="toybox", what="her toy box (front plane)", shape={"rect": box3(M.TOYBOX, top=70)}, stand=mk["atfort"], face="S"),
    ]
    sign = v.poly([(22, 24, 405), (102, 24, 405), (102, 64, 405), (22, 64, 405)])
    L = {
        "id": M.ID, "horizon": v.hz, "full": v.full, "eye_cm": round(v.eye), "view": M.VIEW,
        "vanishing": [round(v.vanishing()[0][0], 1), round(v.vanishing()[0][1], 1)],
        "light": "night. Warm: the rooster lamp on her bedside table (right), the fort's string of lights (left), the egg night-light by the flock (far left), a little from the landing through the door (front right). Cool: the moon through the gable window, falling down the floor and to the left, across the fried-egg rug.",
        "walk": walk,
        "blocked": blocked,
        "planes": [
            {"id": "fort", "file": "fort.png", "base": fort_base},
            {"id": "flashlight", "file": "flashlight.png", "base": [[fort_base[0][0], fort_base[0][1] + 1], [fort_base[1][0], fort_base[1][1] + 1]], "note": "show until she takes it"},
            {"id": "teaparty", "file": "teaparty.png", "base": tea_base},
            {"id": "front", "file": "front.png", "plane": "front"},
        ],
        "things": things,
        "exits": [{"to": "home-landing", "id": "door", "shape": {"rect": door_rect}, "stand": mk["atdoor"]}],
        "marks": {"mom": mk["mom"], "bigsis": mk["bigsis"], "lilsis": mk["lilsis"],
                  "fromLanding": {"mom": mk["mom"], "bigsis": mk["bigsis"], "lilsis": mk["lilsis"]},
                  "atFort": mk["atfort"], "atBed": mk["atbed"], "atFlock": mk["atflock"], "atNest": mk["atnest"], "atTeaParty": mk["atteaparty"],
                  "atChart": mk["atchart"], "atWindow": mk["atwindow"], "atDoor": mk["atdoor"]},
        "lettering": {"NO BIG SISTERS": {"poly": [[int(round(x)), int(round(y))] for x, y in sign]}},
        "note": "front.png holds, left to right: her toy box, the crate of picture books, the hen house (id coop), the nest (id nest), the door; the mobile of felt chickens that hangs in front of them all is mobile.png now (round four: see the 'cutout' of fx 'mobile'). Lamps and windows are painted lit; nothing here blinks or changes.",
        "fx": [{"type": "sway", "id": "mobile", "plane": "mobile", "anchor": "top", "amount": 1.6, "period": 5.5, "wave": 60, "lean": 0,
                "cutout": {"id": "mobile", "file": "mobile.png", "plane": "front",
                           "note": "NEW cut-out: add it to the scene's planes. It is the mobile lifted out of front.png by its own pixels (front.png + mobile.png "
                                   "is the old front.png exactly): until a scene shows it the room has no mobile. Kept out of 'planes' here only so that the "
                                   "checks stay clean until then"},
                "what": "Little Sister's mobile of felt chickens, stirring in the air of the room: each chicken swings a little on its thread, slowly. "
                        "It hangs from a rafter on the front plane; the bars at the top hardly move (anchor top)"}],
    }
    for k, r in (signs or {}).items():
        name = {"reserved": "RESERVED", "henhouse": "HEN HOUSE", "nest": "NEST", "chart": "MY CHICKENS"}.get(k, k)
        if len(r) == 4 and k != "reserved":
            r = [min(r[0], r[2]), min(r[1], r[3]), abs(r[2] - r[0]), abs(r[3] - r[1])]
        L["lettering"][name] = {"rect": [int(x) for x in r]}
    return L


def write(path=f"{OUT}/layout.json", signs=None):
    if signs is None and os.path.exists(path):                 # keep the lettering boxes the painting run measured
        try:
            old = json.load(open(path)).get("lettering", {})
            signs = {k: val["rect"] for k, val in old.items() if "rect" in val}
            L = layout()
            for k, r in signs.items():
                L["lettering"][k] = {"rect": r}
            json.dump(L, open(path, "w"), indent=1)
            return path
        except Exception:
            signs = None
    json.dump(layout(signs), open(path, "w"), indent=1)
    return path


if __name__ == "__main__":
    print(write())
    L = json.load(open(f"{OUT}/layout.json"))
    print("walk", L["walk"])
    print("blocked", L["blocked"])
    print("marks", L["marks"])
    print("planes", L["planes"])
    for t in L["things"]:
        print(t["id"], t["shape"], t["stand"], t["face"])
    print("lettering", L["lettering"])

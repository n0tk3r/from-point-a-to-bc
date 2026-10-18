"""The air ducts (office-ducts): checks on the finished pictures and layout.json, and the pictures to look at (OFFICE-17B,
OFFICE-17B2).

    python3 office_ducts_check.py [folder] [people-folder] [--ranger FOLDER]
        checks out/office-ducts/ (or the folder: the installed art/scenes/office-ducts/ too); people-folder, if given,
        holds the three stand-in rooms with the game's people standing in them (<scene>.png), to lay the grille's view on;
        --ranger: where Ranger's frames are (ranger-shades-*.png; default the game's art/scenes/nevada-roadside/): with
        his `peek` frames there, he lies at the grilles in them

OFFICE-17B2: the numbers the scenes are written against are checked to be exactly what they were (FIXED below: the
camera, the walk, every mark and its grille point, the grilles' shapes, the fan's frames' box, foot and place).

Writes out/office-ducts-check/:
  layout.png         the backdrop (the fan stopped) with the walk, every mark (a dot and its name), every thing's shape,
                     the grilles' floors and stencils, the fan's box, drawn over it in thin lines
  ranger.png         Ranger at every mark, from his own painted frames in the mirror shades he wears at the Office, laid
                     pixel for pixel by his foot point (the engine draws him at scale 1.0 here): sitting up at `intake`
                     and at `shaft`, lying at the four grilles in his `peek` frames (on all fours instead where the frames
                     folder has no peek frames); the fan stopped
  ranger-turning.png the same with the fan turning (fan-0): the act's opening, before the fans are switched off
  fan.png            the five frames of the fan side by side, enlarged
  grille-<scene>.png the grille's view laid over three of the game's interiors (the store and two rooms of the house)
Prints each check and exits non-zero if one fails."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "..", "..", "art", "scenes")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
RANGER = os.path.join(ART, "nevada-roadside")
if "--ranger" in sys.argv:
    RANGER = sys.argv[sys.argv.index("--ranger") + 1]
    ARGS = [a for a in ARGS if a != RANGER]
FOLDER = ARGS[0] if len(ARGS) > 0 else "out/office-ducts"
PEOPLE = ARGS[1] if len(ARGS) > 1 else None
CHECK = "out/office-ducts-check"
MARKS = ["intake", "over-room", "over-property", "over-break", "over-hall", "shaft"]
THINGS = ["grille-room", "grille-property", "grille-break", "grille-hall", "intake", "shaft", "stencil", "fan", "pipe", "wires",
          "insulation", "cup", "pencil", "wrapper", "fitting", "valve", "bulb", "lifted", "tiles", "rivets", "intakefan"]
# the numbers the scenes are written against (round seventeen's installed layout): they stay exactly (OFFICE-17B2)
FIXED = {
    "horizon": 333, "full": 470, "minScale": 1.0, "maxScale": 1.0,
    "view": {"horizon": 333, "full": 470, "cam": [400.0, 906.25], "yaw": 0.0, "focal": 600.0, "centre_x": 400.0},
    "walk": [[62, 466], [623, 466], [638, 475], [39, 475]],
    "marks": {"intake": [71, 470], "over-room": [175, 470], "over-property": [295, 470], "over-break": [415, 470],
              "over-hall": [535, 470], "shaft": [618, 470]},
    "grille_points": {"over-room": [225, 470], "over-property": [345, 470], "over-break": [465, 470], "over-hall": [585, 470]},
    "grille_shapes": {"grille-room": [[193, 397], [253, 397], [253, 526], [193, 526]],
                      "grille-property": [[320, 397], [367, 397], [367, 526], [320, 526]],
                      "grille-break": [[442, 397], [490, 397], [490, 526], [442, 526]],
                      "grille-hall": [[556, 397], [617, 397], [617, 526], [556, 526]]},
    "grille_floors": {"room": [[217, 463], [251, 463], [234, 478], [195, 478]], "property": [[330, 463], [365, 463], [361, 478], [322, 478]],
                      "break": [[444, 463], [479, 463], [488, 478], [449, 478]], "hall": [[558, 463], [593, 463], [615, 478], [576, 478]]},
    "stencils": {"room": [[221, 399], [277, 399], [277, 414], [221, 414]], "property": [[316, 399], [406, 399], [406, 414], [316, 414]],
                 "break": [[448, 399], [497, 399], [497, 414], [448, 414]], "hall": [[564, 399], [604, 399], [604, 414], [564, 414]]},
    "fan": {"at": [693, 550], "foot": [39, 23], "size": [97, 47], "base": 573, "box": [654, 527, 97, 47]},
}
ROOMS = ("nevada-store", "home-living-room", "home-study")
FAILS = []


def ok(cond, what):
    print(("  ok    " if cond else "  FAIL  ") + what)
    if not cond:
        FAILS.append(what)


def inside(pt, poly, tol=0.0):
    """A point in a polygon (or within `tol` px of its edge)."""
    x, y = pt
    n, hit = len(poly), False
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            hit = not hit
        dx, dy = x1 - x0, y1 - y0
        t = max(0.0, min(1.0, ((x - x0) * dx + (y - y0) * dy) / max(1e-9, dx * dx + dy * dy)))
        if math.hypot(x - (x0 + t * dx), y - (y0 + t * dy)) <= tol:
            return True
    return hit


def shape_box(shape):
    if "poly" in shape:
        xs, ys = [p[0] for p in shape["poly"]], [p[1] for p in shape["poly"]]
        return min(xs), min(ys), max(xs), max(ys)
    x, y, w, h = shape["rect"]
    return x, y, x + w, y + h


def frame(name, face="E"):
    if not os.path.exists(os.path.join(RANGER, f"ranger-shades-{name}.png")):
        name = "stand-0"                                                 # (no peek frames here: on all fours instead)
    im = Image.open(os.path.join(RANGER, f"ranger-shades-{name}.png")).convert("RGBA")
    fx, fy = 68, 56
    if face == "W":
        im, fx = im.transpose(Image.FLIP_LEFT_RIGHT), im.width - fx
    return im, fx, fy


def lay_ranger(im, at, name, face):
    f, fx, fy = frame(name, face)
    im.alpha_composite(f, (int(round(at[0] - fx)), int(round(at[1] - fy))))


def backdrop(lay, which="fan-stopped"):
    im = Image.open(os.path.join(FOLDER, "back.png")).convert("RGBA")
    pl = {p["id"]: p for p in lay["planes"]}
    p = pl["fan-stopped"] if which == "fan-stopped" else pl["fan"]
    src = p["src"] if which == "fan-stopped" else which + ".png"
    im.alpha_composite(Image.open(os.path.join(FOLDER, src)).convert("RGBA"), (p["at"][0] - p["foot"][0], p["at"][1] - p["foot"][1]))
    return im


def main():
    os.makedirs(CHECK, exist_ok=True)
    lay = json.load(open(os.path.join(FOLDER, "layout.json")))
    print(f"checking {FOLDER}")
    # ---- the numbers the scenes are written against: exactly as they were
    for k in ("horizon", "full", "minScale", "maxScale", "view", "walk"):
        ok(lay[k] == FIXED[k], f"fixed: {k} {json.dumps(lay[k])[:80]}")
    for k, at in FIXED["marks"].items():
        m = lay["marks"][k]
        ok(m["at"] == at and m["face"] == "E" and m["scale"] == 1.0, f"fixed: mark {k} at {m['at']}, facing {m['face']}, scale {m['scale']}")
    for k, gp in FIXED["grille_points"].items():
        ok(lay["marks"][k].get("grille") == gp, f"fixed: {k}'s grille point {lay['marks'][k].get('grille')}")
    th = {t["id"]: t for t in lay["things"]}
    for k, poly in FIXED["grille_shapes"].items():
        ok(th[k]["shape"].get("poly") == poly and th[k]["stand"] == FIXED["marks"]["over-" + k[7:]], f"fixed: {k}'s shape and stand")
    for g in lay["grilles"]:
        ok(g["floor"] == FIXED["grille_floors"][g["id"]] and g["stencil"] == FIXED["stencils"][g["id"]]
           and g["centre"] == FIXED["grille_points"]["over-" + g["id"]], f"fixed: grille {g['id']}: its floor, its stencil, its middle")
    fx = FIXED["fan"]
    for p in lay["planes"]:
        ok(p["at"] == fx["at"] and p["foot"] == fx["foot"] and p["base"] == fx["base"], f"fixed: plane {p['id']} at {p['at']}, foot {p['foot']}, base {p['base']}")
    ok(lay["cutouts"]["fan"] == fx["box"], f"fixed: the fan's box {lay['cutouts']['fan']}")
    ok(th["fan"]["shape"]["poly"] == [[652, 525], [753, 525], [753, 576], [652, 576]], "fixed: the fan's area (it did not move)")
    # ---- the click order: what lies under what (the engine's areas are drawn in order: a later one lies over an earlier)
    order = [t["id"] for t in lay["things"]]
    ok(order[0] == "tiles", "click order: the tiles first (under the grilles and the things on them)")
    for a, bs in (("shaft", ("stencil", "fan", "bulb")), ("pipe", ("valve",)), ("intake", ("intakefan",)),
                  ("tiles", ("grille-room", "cup", "pencil", "wrapper", "fitting", "lifted"))):
        ok(all(order.index(a) < order.index(b) for b in bs), f"click order: {a} before {', '.join(bs)}")
    sh = th["shaft"]["shape"]["poly"]
    hall = FIXED["grille_shapes"]["grille-hall"]
    clear = all(not inside(p, sh) for p in [[x, y] for x in range(hall[0][0], hall[1][0] + 1, 4) for y in range(hall[0][1], hall[2][1] + 1, 4)])
    ok(clear, "the shaft's area leaves the HALL grille's clear")
    # ---- the files
    back = Image.open(os.path.join(FOLDER, "back.png"))
    ok(back.size == (800, 600) and back.mode == "P", f"back.png: 800 x 600, a palette ({back.mode})")
    ok(lay["id"] == "office-ducts" and lay["horizon"] == 333 and lay["full"] == 470, "id office-ducts, horizon 333, full 470")
    ok(lay["view"]["horizon"] == lay["horizon"] and lay["view"]["full"] == lay["full"], "the view's camera is the scene's (horizon, full)")
    fx0, fy0, fw, fh = lay["cutouts"]["fan"]
    pl = {p["id"]: p for p in lay["planes"]}
    ok(set(pl) == {"fan", "fan-stopped"}, "planes: fan (turning) and fan-stopped")
    names = pl["fan"]["frames"] + [pl["fan-stopped"]["src"]]
    ok(names == ["fan-0.png", "fan-1.png", "fan-2.png", "fan-3.png", "fan-stopped.png"], "the fan's frames: fan-0 .. fan-3, fan-stopped")
    for n in names:
        im = Image.open(os.path.join(FOLDER, n))
        a = np.asarray(im.convert("RGBA"))[..., 3]
        ok(im.size == (fw, fh), f"{n}: {im.size[0]} x {im.size[1]}, the fan's box")
        ok(a.max() == 255 and a.min() == 0 and len(np.unique(a)) == 2, f"{n}: hard-edged ({len(np.unique(a))} alpha values)")
    for p in pl.values():
        ok([p["at"][0] - p["foot"][0], p["at"][1] - p["foot"][1]] == [fx0, fy0], f"{p['id']}: at - foot = the box's corner ({fx0}, {fy0})")
        ok(0 <= p["foot"][0] < fw and 0 <= p["foot"][1] < fh, f"{p['id']}: its foot {p['foot']} inside its frame")
    ok(pl["fan"]["when"].startswith("turning") and "office.acOff" in pl["fan-stopped"]["when"], "the fan turns until office.acOff, then is still")
    gv = Image.open(os.path.join(FOLDER, "grille-view.png"))
    ga = np.asarray(gv.convert("RGBA"), np.float32) / 255
    cov = float((ga[..., 3] >= 0.5).mean())
    mid = float((ga[60:540, 60:740, 3] >= 0.5).mean())
    ok(gv.size == (800, 600) and gv.mode == "RGBA", f"grille-view.png: 800 x 600 RGBA ({gv.mode})")
    ok(cov <= 1 / 3, f"grille-view.png covers {cov * 100:.1f}% of the picture (alpha at least a half; at most a third)")
    print(f"  note  the slats alone (60 px in from the edges): {mid * 100:.1f}% covered; mean alpha {ga[..., 3].mean():.2f}")
    lum = float((ga[..., :3].mean(-1) * ga[..., 3]).sum() / ga[..., 3].sum())
    ok(lum >= 0.25, f"grille-view.png's alpha-weighted mean {lum:.3f} (at 0.25 or more the paints key it as a picture, not a ground shadow)")
    # ---- the walk, the marks
    walk = lay["walk"]
    rows = lay["rows"]
    wy = [p[1] for p in walk]
    ok(rows["floor_back"] <= min(wy) and max(wy) <= rows["floor_front"], f"the walk (rows {min(wy)}-{max(wy)}) on the duct's floor (rows {rows['floor_back']}-{rows['floor_front']})")
    ok(set(MARKS) <= set(lay["marks"]), "marks: " + ", ".join(MARKS))
    for k in MARKS:
        m = lay["marks"][k]
        ok(inside(m["at"], walk, 1.0), f"{k}: {m['at']} on the walk")
        ok(m["face"] in ("E", "W", "N", "S") and abs(m["scale"] - 1.0) <= 0.05, f"{k}: faces {m['face']}, scale {m['scale']}")
    gx = [lay["marks"]["over-" + g]["at"][0] for g in ("room", "property", "break", "hall")]
    gaps = [b - a for a, b in zip(gx, gx[1:])]
    ok(min(gaps) >= 104, f"the grilles' marks {gaps} px apart: room for Ranger (104 px tail to nose) lying at each")
    for g in lay["grilles"]:
        m = lay["marks"][g["mark"]]
        nose = m["at"][0] + 42
        xs = [p[0] for p in g["floor"]]
        ok(min(xs) <= nose <= max(xs), f"{g['id']}: his nose ({nose}) over the grille ({min(xs)}-{max(xs)}), the mark {m['at'][0]}")
        boot = g["boot"]
        ok(boot[1] >= lay["rows"]["floor_band"][1] - 1 and boot[1] + boot[3] <= lay["rows"]["tiles_cut"] + 2,
           f"{g['id']}: its boot {boot} under the floor's cut band, down to the tiles")
        sy = max(p[1] for p in g["stencil"])
        ok(sy < rows["floor_back"] and min(p[1] for p in g["stencil"]) > rows["duct_top"], f"{g['id']}: its stencil on the back wall, between the duct's top and floor")
    for k, (name, top) in {"intake": ("sit-0", 51), "shaft": ("sit-0", 51), "over-room": ("stand-0", 36)}.items():
        y = lay["marks"][k]["at"][1]
        ok(y - top > rows["duct_top"], f"{k}: Ranger ({name}, {top} px tall) under the duct's top (row {rows['duct_top']})")
    ok(lay["marks"]["intake"]["at"][0] - 61 >= 0, "intake: his tail in the picture")
    # ---- the things
    ids = [t["id"] for t in lay["things"]]
    ok(len(ids) == len(set(ids)), "things: no id twice")
    ok(set(THINGS) <= set(ids), "things: " + ", ".join(THINGS))
    for t in lay["things"]:
        x0, y0, x1, y1 = shape_box(t["shape"])
        ok(0 <= x0 < x1 <= 800 and 0 <= y0 < y1 <= 600, f"{t['id']}: its shape ({x0},{y0})-({x1},{y1}) on the picture")
        ok(inside(t["stand"], walk, 1.5), f"{t['id']}: its stand {t['stand']} on the walk")
    for t in lay["things"]:
        if t["id"].startswith("grille-"):
            ok(t.get("mark") == "over-" + t["id"][7:], f"{t['id']}: stood at over-{t['id'][7:]}")
    ok(lay["exits"] and lay["exits"][0]["to"] == "office-lot", "the way out: up the intake run to the lot's roof")
    # ---- the pictures
    lp = backdrop(lay)
    d = ImageDraw.Draw(lp)
    d.polygon([tuple(p) for p in walk], outline=(80, 255, 120, 255))
    for t in lay["things"]:
        c = (255, 210, 60, 255) if t["id"].startswith("grille") else (90, 200, 255, 255)
        if "poly" in t["shape"]:
            d.polygon([tuple(p) for p in t["shape"]["poly"]], outline=c)
        else:
            x, y, w, h = t["shape"]["rect"]
            d.rectangle([x, y, x + w, y + h], outline=c)
    for g in lay["grilles"]:
        d.polygon([tuple(p) for p in g["floor"]], outline=(255, 120, 60, 255))
    d.rectangle([fx0, fy0, fx0 + fw, fy0 + fh], outline=(255, 80, 200, 255))
    for k, m in lay["marks"].items():
        x, y = m["at"]
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 60, 60, 255))
        d.text((x - 12, y + 6 + (8 if k.startswith("over-") and k != "over-room" and MARKS.index(k) % 2 else 0)), k, fill=(255, 255, 255, 255))
    lp.convert("RGB").save(os.path.join(CHECK, "layout.png"))
    for nm, which in (("ranger.png", "fan-stopped"), ("ranger-turning.png", "fan-0")):
        im = backdrop(lay, which)
        for k in MARKS:
            m = lay["marks"][k]
            lay_ranger(im, m["at"], "sit-0" if k in ("intake", "shaft") else "peek-0", m["face"])
        im.convert("RGB").save(os.path.join(CHECK, nm))
    tiles = [Image.open(os.path.join(FOLDER, n)).convert("RGBA") for n in names]
    sheet = Image.new("RGBA", (len(tiles) * (fw * 4 + 8), fh * 4), (40, 40, 48, 255))
    for i, t in enumerate(tiles):
        sheet.alpha_composite(t.resize((fw * 4, fh * 4), Image.NEAREST), (i * (fw * 4 + 8), 0))
    sheet.convert("RGB").save(os.path.join(CHECK, "fan.png"))
    sys.path.insert(0, HERE)
    from office_ducts_grille import rooms
    for sid, im in rooms():
        base = im
        if PEOPLE and os.path.exists(os.path.join(PEOPLE, sid + ".png")):
            base = Image.open(os.path.join(PEOPLE, sid + ".png")).convert("RGBA")
        comp = base.copy()
        comp.alpha_composite(gv.convert("RGBA"))
        comp.convert("RGB").save(os.path.join(CHECK, f"grille-{sid}.png"))
    print(f"\n{len(FAILS)} failed" if FAILS else "\nall checks passed")
    print("pictures:", ", ".join(os.path.join(CHECK, f) for f in ["layout.png", "ranger.png", "ranger-turning.png", "fan.png"]
                                 + [f"grille-{s}.png" for s in ROOMS]))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())

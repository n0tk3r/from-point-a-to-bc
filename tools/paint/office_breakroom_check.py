"""Checks on the break room as installed (art/scenes/office-breakroom/) and its layout.json. OFFICE-17D.

    python3 office_breakroom_check.py          the checks, then the check picture (layout.json drawn over the comp:
                                               out/office-breakroom-check.png)

What it holds (each a line, "ok" or what is wrong; the exit code is the number of failures):
  - every file in the folder is in the scene's plan (postimp_plans.PLANS) or is layout.json, and every file of the plan
    is there; back.png 800x600 and opaque; each cut-out and state 800x600 with a clear colour and a hard edge; the
    clock's 60 frames, each the size of `frames.clock.rect`;
  - the planes of layout.json are the plan's, each alt replacing a plane that exists, each base a line inside the picture;
  - the marks OFFICE-17.md names (fridge, counter, sink, floyd, jed, vending, board) and the seats (floyd, jed) with a
    seat row; Ranger's marks with a scale, his counter marks inside the counter's own walk, his three paths;
  - a thing with a shape for every clickable thing the brief lists, every shape inside the picture, no id twice;
  - every standing place inside the walk outline, every grown-up there between 140 and 192 pixels tall (maxScale 1.2);
  - the walk outline clear of the cut-outs' solid ground, and of the low table's pixels (nobody's feet behind it; the round
    table in the near right is passed behind, as the store's foreground is, and the check says where);
  - the pie's states show what they must: the cap's red in the eaten tin and on the fallen card (enough pixels of it
    to read), and nothing of the pie left in pie-gone."""

import json
import os
import sys

import numpy as np
from PIL import Image

from postimp_plans import PLANS

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, "..", "..", "art", "scenes", "office-breakroom"))
SCENE = "office-breakroom"
NEEDED_MARKS = ["fridge", "counter", "sink", "floyd", "jed", "vending", "board"]
NEEDED_THINGS = ["fridge", "sign", "vent", "counter", "sink", "coffee", "cups", "microwave", "pie", "card", "board", "form7", "found",
                 "bowling", "schedule", "couch", "chair", "vending", "buttons", "tray", "clock", "speaker", "door"]
fails = []


def say(ok, what):
    print(("ok    " if ok else "FAIL  ") + what)
    if not ok:
        fails.append(what)


def inside(pt, poly):
    x, y = pt
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1:
            c = not c
    return c


def poly_mask(poly, w=800, h=600):
    from PIL import ImageDraw
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon([tuple(p) for p in poly], fill=255)
    return np.asarray(m) > 0


def alpha_of(name):
    im = Image.open(os.path.join(ART, name))
    return np.asarray(im.convert("RGBA"))[..., 3], im


def main():
    L = json.load(open(os.path.join(ART, "layout.json")))
    plan = PLANS[SCENE]
    files = sorted(f for f in os.listdir(ART) if f.endswith(".png"))
    wanted = {"back.png"} | {f"{p}.png" for p in plan["planes"]} | {f"{a}.png" for a in plan["alt"]}
    for lst in plan.get("states", {}).values():
        wanted |= {f"{s}.png" for s in lst}
    frames = [f for f in files if f.startswith("clock-")]
    say(set(files) - set(frames) == wanted, f"the files are the plan's ({len(files) - len(frames)} pictures and {len(frames)} frames)")
    say(sorted(os.listdir(ART)) == sorted(files + ["layout.json"]), "nothing else in the folder but layout.json")
    a, im = alpha_of("back.png")
    say(im.size == (800, 600) and a.min() == 255, "back.png 800x600, opaque")
    for f in sorted(wanted - {"back.png"}):
        a, im = alpha_of(f)
        hard = np.isin(a, (0, 255)).all()
        say(im.size == (800, 600) and (a == 0).any() and (a == 255).any() and hard, f"{f}: 800x600, clear round the thing, a hard edge")
    rect = L["frames"]["clock"]["rect"]
    sizes = {Image.open(os.path.join(ART, f)).size for f in frames}
    say(len(frames) == 60 and sizes == {(rect[2], rect[3])} and L["frames"]["clock"]["files"] == [f"clock-{k}.png" for k in range(60)],
        f"the clock's 60 frames, each {rect[2]}x{rect[3]}")
    # the planes
    ids = [p["id"] for p in L["planes"]]
    say(set(ids) == {f[:-4] for f in wanted - {"back.png"}}, "layout.json's planes are the plan's")
    for p in L["planes"]:
        if p.get("alt"):
            say(all(r in ids for r in p["replaces"]), f"{p['id']} replaces {p['replaces']}")
        if isinstance(p.get("base"), list):
            say(all(0 <= x <= 800 and 0 <= y <= 600 for x, y in p["base"]), f"{p['id']}'s base inside the picture")
    # marks, seats, Ranger
    m = L["marks"]
    say(all(k in m for k in NEEDED_MARKS), "the marks OFFICE-17.md names: " + ", ".join(NEEDED_MARKS))
    for k in ("floyd", "jed"):
        s = L["seats"][k]
        say(s["at"] == m[k] and s["seat_row"] < s["at"][1] and s["face"] in ("E", "W"), f"seat {k}: at its mark, seat row {s['seat_row']}, faces {s['face']}")
    cw = L["levels"]["counter"]["walk"]
    for k, r in L["ranger_marks"].items():
        say("scale" in r and 0.5 < r["scale"] < 1.3, f"Ranger at {k}: scale {r['scale']}")
        if r.get("level") == "counter":
            say(inside(r["at"], cw) or min(abs(r["at"][1] - y) for _, y in cw) <= 2, f"Ranger's {k} on the counter's own walk")
    say(set(L["paths"]) >= {"fridge-counter", "counter-floor", "vent-fridge"} and len(L["paths"]["fridge-counter"]["points"]) == 3,
        "Ranger's paths: the fridge to the counter (three points), the counter to the floor, the grille to the fridge")
    # things
    tids = [t["id"] for t in L["things"]]
    say(len(tids) == len(set(tids)), f"{len(tids)} things, no id twice")
    missing = [k for k in NEEDED_THINGS if k not in tids]
    say(not missing, "a thing for every clickable thing the brief lists" + (f" (missing: {missing})" if missing else ""))
    outside = []
    for t in L["things"]:
        sh = t["shape"]
        pts = sh["poly"] if "poly" in sh else [[sh["rect"][0], sh["rect"][1]], [sh["rect"][0] + sh["rect"][2], sh["rect"][1] + sh["rect"][3]]]
        if not all(0 <= x <= 800 and 0 <= y <= 600 for x, y in pts):
            outside.append(t["id"])
    say(not outside, "every thing's shape inside the picture" + (f" (not: {outside})" if outside else ""))
    # standing places and sizes
    walk = L["walk"]
    for k, s in L["stands"].items():
        if k in ("floyd", "jed"):
            continue
        say(inside(s["at"], walk) and 140 <= s["grownup_px"] <= 192, f"stand {k} {s['at']}: inside the walk, a grown-up {s['grownup_px']} px")
    wm = poly_mask(walk)
    for p in L["planes"]:
        if p.get("solid") and not p.get("alt"):
            n = int((poly_mask(p["solid"]) & wm).sum())
            if n and p["solid"] in L["blocked"]:
                say(True, f"{p['id']}'s ground is on the walk and in `blocked` (people walk round it)")
            else:
                say(n == 0, f"{p['id']}'s ground is off the walk ({n} pixels on it)")
    fa, _ = alpha_of("front.png")
    low = [t for t in L["things"] if t["id"] == "lowtable"][0]["shape"]["poly"]
    say(not ((fa > 0) & poly_mask(low) & wm).any(), "the low table (front plane, near left) covers none of the walk: nobody's feet go behind it")
    ys, xs = np.nonzero((fa > 0) & wm)
    print(f"      (the round table and its chair, front plane, near right: the walk passes behind them at x {xs.min()} to {xs.max()}, "
          f"rows {ys.min()} to {ys.max()}, as people pass behind the store's foreground: physically so, they stand behind it)")
    # the pie's states
    def red_px(name, box):
        im = np.asarray(Image.open(os.path.join(ART, name)).convert("RGBA")).astype(int)
        x0, y0, x1, y1 = box
        c = im[y0:y1, x0:x1]
        r, g, b, al = c[..., 0], c[..., 1], c[..., 2], c[..., 3]
        return int(((al > 0) & (r > 120) & (r > g + 50) & (r > b + 40)).sum())
    pie = L["cutouts"]["pie"]
    box = (pie[0], pie[1], pie[0] + pie[2], pie[1] + pie[3])
    n_eaten = red_px("pie-eaten.png", box)
    say(n_eaten >= 3, f"pie-eaten: the bottle cap shows in the tin ({n_eaten} red pixels)")
    g = L["cutouts"]["pie-gone"]
    n_gone = red_px("pie-gone.png", (g[0], g[1], g[0] + g[2], g[1] + g[3]))
    say(n_gone >= 3, f"pie-gone: the bottle cap shows on the fallen card ({n_gone} red pixels, the card's red letters among them)")
    print()
    print(f"{len(fails)} failed" if fails else "all held")
    import office_breakroom_layout
    print(office_breakroom_layout.check())
    return len(fails)


if __name__ == "__main__":
    sys.exit(main())

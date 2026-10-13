"""Across the Tiber: does the engine lay everybody in the right order? The engine sorts its floor (cut-outs, people,
the hens) back to front by their bases, a person against a cut-out compared where the person stands, two cut-outs
compared at the middle of their two bases (js/engine/cast.js, order()); with slanted base lines that comparison is not
always transitive, and then the order depends on the sort. This emulates the sort exactly (the engine's comparison;
Python's list sort is the same TimSort as V8's) for the scene's cast in each of its states, with the boy at every place
on the walk map in turn, and reports any pair that overlaps on the screen and is laid in the wrong order.

    python3 rome_tiber_order.py [path/to/art/scenes/rome-tiber or out/rome-tiber]"""

import functools
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "rome-tiber")
L = json.load(open(os.path.join(SRC, "layout.json")))
HZ, FULL = L["horizon"], L["full"]
row_k = lambda y: max(0.0, (y - HZ) / (FULL - HZ))


def base_at(base, x, y):
    if base is None:
        return y
    if isinstance(base, (int, float)):
        return base
    (x1, y1), (x2, y2) = base
    t = 0.5 if x2 == x1 else min(1.0, max(0.0, (x - x1) / (x2 - x1)))
    return y1 + (y2 - y1) * t


def mid(s):
    return (s["base"][0][0] + s["base"][1][0]) / 2 if isinstance(s["base"], list) else s["x"]


def depth(a, b):
    """cast.js order(): -> < 0 when a is laid first (farther)."""
    x = a["x"] if a["person"] else b["x"] if b["person"] else a["x"] if a["base"] is None else b["x"] if b["base"] is None else (mid(a) + mid(b)) / 2
    d = base_at(a["base"], x, a["y"]) - base_at(b["base"], x, b["y"])
    return d if d else int(a["person"]) - int(b["person"])


CUTS = []
for pl in L["planes"]:
    if pl.get("plane") == "front":
        continue
    a = np.asarray(Image.open(os.path.join(SRC, pl["file"])).convert("RGBA"))[..., 3] > 127
    CUTS.append({"id": pl["id"], "base": pl.get("base"), "x": 0, "y": 0, "person": False, "mask": a, "rect": None})


def person(pid, x, y, tall, scale=None, wide=0.34):
    """A person (or a hen) as the box the game draws them in."""
    h = 160 * tall * (row_k(y) if scale is None else scale)
    rect = (int(max(0, x - h * wide / 2)), int(max(0, y - h)), int(min(800, x + h * wide / 2 + 1)), int(min(600, y + 1)))
    return {"id": pid, "base": None, "x": x, "y": y, "person": True, "mask": None, "rect": rect}


def overlap(a, b):
    if a["rect"] and b["rect"]:
        (ax0, ay0, ax1, ay1), (bx0, by0, bx1, by1) = a["rect"], b["rect"]
        return ax0 < bx1 and bx0 < ax1 and ay0 < by1 and by0 < ay1
    p, c = (a, b) if a["rect"] else (b, a)
    x0, y0, x1, y1 = p["rect"]
    return bool(c["mask"][y0:y1, x0:x1].any())


def hens():
    out = []
    for f in L["fx"]:
        if str(f.get("id", "")).startswith("hen-"):
            (x1, y1), (x2, y2) = f["perch"]
            for t in (0.0, 0.5, 1.0):                            # each bird stands somewhere along its perch
                out.append(person(f["id"] + f"@{t}", x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, 37 / 160, wide=1.1))
    return out


def walk_points(step=12):
    poly = [tuple(p) for p in L["walk"]]
    im = Image.new("L", (800, 600), 0)
    ImageDraw.Draw(im).polygon(poly, fill=255)
    blk = Image.new("L", (800, 600), 0)
    for b in L["blocked"] + [p["solid"] for p in L["planes"] if p.get("solid")]:
        ImageDraw.Draw(blk).polygon([tuple(q) for q in b], fill=255)
    ok = (np.asarray(im) > 0) & (np.asarray(blk) == 0)
    return [(x, y) for y in range(HZ + 4, 600, step) for x in range(4, 800, step) if ok[y, x]]


def check(state, cast_people, boy_points):
    """Every overlapping pair laid as their own comparison says, with the boy at each point. -> problems"""
    problems = []
    hen_list = hens()
    for bx, by in boy_points:
        boy = person("son", bx, by, 0.74)
        floor = CUTS + hen_list + cast_people + [boy]                # the order things come on the stage: planes, fx, actors, the lead
        laid = sorted(floor, key=functools.cmp_to_key(depth))
        pos = {id(s): i for i, s in enumerate(laid)}
        for i, a in enumerate(floor):
            for b in floor[i + 1:]:
                if not (a["person"] or b["person"]):
                    continue
                if not overlap(a, b):
                    continue
                want = depth(a, b)
                if want == 0:
                    continue
                if (want < 0) != (pos[id(a)] < pos[id(b)]):
                    problems.append((state, (bx, by), a["id"], b["id"]))
    return problems


def main():
    m = L["marks"]
    w = m["window"]
    eleazar = lambda at, scale=None: person("eleazar", at[0], at[1], 0.96, scale)
    mariam = lambda at: person("mariam", at[0], at[1], 0.69)
    felix = lambda at: person("felix", at[0], at[1], 1.03)
    states = {
        "opening: Eleazar at the window": [eleazar(w["at"], w["scale"]), mariam(m["mariam"]["at"]), felix(m["felix"]["at"])],
        "Eleazar on the bench": [person("eleazar", m["bench_seat"]["at"][0], m["bench_seat"]["at"][1], 0.66), mariam(m["mariam_spots"][0]), felix(m["felix_spots"][1])],
        "the prayer": [eleazar(m["pray_eleazar"]), person("son-at-prayer", m["pray_son"][0], m["pray_son"][1], 0.74), mariam(m["mariam_spots"][1]), felix(m["felix_spots"][0])],
        "at his door; Petosiris": [eleazar(m["door"]), mariam(m["mariam"]["at"]), felix(m["felix_spots"][0]), person("petosiris", m["petosiris"][0], m["petosiris"][1], 1.0)],
    }
    pts = walk_points()
    total = []
    for name, folk in states.items():
        pr = check(name, folk, pts)
        total += pr
        print(f"{name}: the boy at {len(pts)} places: {len(pr)} pair{'s' if len(pr) != 1 else ''} laid wrong")
        seen = set()
        for st, at, a, b in pr:
            if (a, b) not in seen:
                seen.add((a, b))
                print(f"   {a} / {b}  (the boy at {at}, and maybe elsewhere)")
    # and the ones whose place is fixed, against what they must be behind or in front of wherever they overlap it
    must = [(eleazar(w["at"], w["scale"]), ["window-wall", "washing"], -1)]
    yard = [mariam(m["mariam"]["at"])] + [mariam(q) for q in m["mariam_spots"]] + hens()
    must += [(p, ["fence", "fence-corner"], -1) for p in yard]
    landing = [felix(m["felix"]["at"])] + [felix(q) for q in m["felix_spots"]] + [person("petosiris", m["petosiris"][0], m["petosiris"][1], 1.0)]
    must += [(p, ["barge", "curb"], 1) for p in landing] + [(p, ["landing-edge"], -1) for p in landing]
    cuts = {c["id"]: c for c in CUTS}
    for p, ids, side in must:
        for cid in ids:
            c = cuts[cid]
            if overlap(p, c) and (depth(p, c) > 0) != (side > 0):
                total.append(("fixed", (p["x"], p["y"]), p["id"], cid))
                print(f"   {p['id']} at {p['x']},{p['y']} should be {'in front of' if side > 0 else 'behind'} {cid}, and is not")
    print(f"the people whose places are fixed, against what they overlap: {sum(1 for t in total if t[0] == 'fixed')} wrong")
    cut_order = [s["id"] for s in sorted(CUTS, key=functools.cmp_to_key(depth))]
    print("the cut-outs alone, back to front:", ", ".join(cut_order))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())

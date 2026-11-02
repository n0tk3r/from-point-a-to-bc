"""PAINT-21C: the checks of Osaka's two scenes (edo-dojima; edo_street_check.py calls this for edo-street): the files in
art/scenes/<id>/ (sizes, palettes, a clear colour in every cut-out, every file in the scene's plan, every state there),
layout.json complete (horizon, full, view, walk, blocked, planes, things with shapes, marks, stands, fx), every mark of
ROUND-21's list there and inside the walk area and clear of blocked ground (but those the list says are elsewhere), every
thing of ROUND-21's list with a shape on the stage; and a check picture with the layout drawn over the scene.

  python3 edo_dojima_check.py          -> out/edo-dojima-check.png, and a line for each check (exit 1 if any fails)
"""

import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "..", "..", "art", "scenes")

DOJIMA = dict(
    marks=["landing", "stall", "natsu", "pot", "balls", "pickle", "line1", "line2", "line3", "line4", "kyuhachi", "market", "rihei", "watermen",
           "kurataFrom", "kurataTo", "town"],
    off_walk=["steps"],
    things=["river", "lighters", "warehouses", "bridge", "castle", "steps", "house", "noren", "stall", "pot", "tub", "tray", "sandals", "kettle", "market",
            "dealers", "watermen", "bucket", "runner", "natsu", "rihei", "kyuhachi", "kurata", "tatsu", "awafather", "awamother", "oldpilgrim", "ladleboy"],
)


def inside(poly, x, y):
    n, c = len(poly), False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-9) + x1:
            c = not c
    return c


def check(scene, want, out_png):
    sys.path.insert(0, HERE)
    import postimp_plans as PP
    folder = os.path.join(ART, scene)
    fails, notes = [], []
    ok = lambda cond, msg: (notes.append("ok   " + msg) if cond else fails.append("FAIL " + msg))
    L = json.load(open(os.path.join(folder, "layout.json")))
    plan = PP.PLANS[scene]
    files = sorted(f[:-4] for f in os.listdir(folder) if f.endswith(".png"))
    import fnmatch
    in_plan = set(plan["planes"]) | set(plan["alt"]) | {s for v in plan.get("states", {}).values() for s in v} | {u for u in plan["union"]}
    frames = [f for f in files if any(fnmatch.fnmatch(f, pat) for pat in plan["frames"])]
    for f in files:
        ok(f == "back" or f in in_plan or f in frames, f"{f}.png is in the plan")
    for n in list(plan["planes"]) + list(plan["alt"]):
        ok(n in files, f"{n}.png exists")
    for f in files:
        im = Image.open(os.path.join(folder, f + ".png"))
        if f in frames:
            ok(im.mode == "P", f"{f}.png (a frame) is a palette picture {im.size}")
        else:
            ok(im.size == (800, 600), f"{f}.png is 800x600")
            ok(im.mode == "P" and len(im.getcolors(256) or []) <= 256, f"{f}.png is a palette of at most 256 colours")
            if f != "back":
                a = np.asarray(im.convert("RGBA"))[..., 3]
                ok(a.min() == 0 and a.max() == 255 and ((a > 0) & (a < 255)).sum() == 0, f"{f}.png has a clear colour and hard edges")
    for key in ("horizon", "full", "view", "walk", "blocked", "planes", "things", "marks", "stands", "fx"):
        ok(key in L, f"layout.json has {key}")
    walk = L["walk"]
    for m in want["marks"]:
        ok(m in L["marks"], f"mark {m} is there")
    for m, (x, y) in L["marks"].items():
        if m in want.get("off_walk", []):
            continue
        ok(inside(walk, x, y), f"mark {m} ({x}, {y}) is inside the walk area")
        ok(not any(inside(b, x, y) for b in L["blocked"]), f"mark {m} is clear of blocked ground")
        st = L["stands"].get(m)
        ok(st is not None and st["at"] == [x, y] and "grownup_px" in st, f"stand {m} has its grownup_px")
    have = {t["id"]: t for t in L["things"]}
    for t in want["things"]:
        ok(t in have and "shape" in have[t], f"thing {t} has a shape")
    for t in L["things"]:
        sh = t["shape"]
        pts = sh.get("poly") or ([[sh["rect"][0], sh["rect"][1]], [sh["rect"][0] + sh["rect"][2], sh["rect"][1] + sh["rect"][3]]] if "rect" in sh else [])
        ok(any(0 <= p[0] <= 800 and 0 <= p[1] <= 600 for p in pts), f"thing {t['id']} is on the stage")
    for p in L["planes"]:
        for st in (p.get("states") or {}).values():
            ok(os.path.exists(os.path.join(folder, st)), f"state {st} of {p['id']} exists")
        for fr in p.get("frames", []):
            ok(os.path.exists(os.path.join(folder, fr)), f"frame {fr} of {p['id']} exists")
    for e in L["fx"]:
        fr = e.get("frames") or {}
        for lst in ("glide", "flap"):
            for n in fr.get(lst, []):
                ok(os.path.exists(os.path.join(folder, n)), f"fx {e['id']}: frame {n} exists")
        if e.get("plane") not in (None, "back", "front") and e["type"] in ("sway", "bob"):
            ok(any(p["id"] == e["plane"] for p in L["planes"]), f"fx {e['id']} moves the cut-out {e['plane']}")
    # the check picture
    im = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    for n in plan["planes"]:
        im.alpha_composite(Image.open(os.path.join(folder, n + ".png")).convert("RGBA"))
    d = ImageDraw.Draw(im)
    d.line([tuple(p) for p in walk] + [tuple(walk[0])], fill=(0, 255, 0, 255), width=1)
    for b in L["blocked"]:
        d.line([tuple(p) for p in b] + [tuple(b[0])], fill=(255, 128, 0, 255), width=1)
    for t in L["things"]:
        sh = t["shape"]
        if "rect" in sh:
            r = sh["rect"]
            d.rectangle([r[0], r[1], r[0] + r[2], r[1] + r[3]], outline=(80, 200, 255, 160))
        else:
            d.line([tuple(p) for p in sh["poly"]] + [tuple(sh["poly"][0])], fill=(80, 200, 255, 160))
    for k, (x, y) in L["marks"].items():
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 255, 255, 255))
        d.text((x + 3, y - 10), k, fill=(255, 255, 255, 255))
    im.convert("RGB").save(out_png)
    for n in notes:
        pass
    print(f"{scene}: {len(notes)} checks passed, {len(fails)} failed")
    for f in fails:
        print(f)
    return not fails


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    sys.exit(0 if check("edo-dojima", DOJIMA, os.path.join(HERE, "out", "edo-dojima-check.png")) else 1)

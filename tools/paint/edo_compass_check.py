"""PAINT-21B: the checks on edo-compass's finished pictures and its layout.json, and the check picture.

    python3 edo_compass_check.py              checks out/edo-compass/ (as painted) -> out/edo-compass-check.png
    python3 edo_compass_check.py --installed  checks art/scenes/edo-compass/ (keyed) -> out/edo-compass-check-keyed.png

What it holds: every picture 800 x 600; every file in the plan and every plane and state present; layout.json complete
(closeup, view, walk, marks, hands with `thumb`, things with a shape, planes, cutouts, fx); ROUND-21's things all there
(box, lid, card, bowmark, needle, the twelve marks) with a shape, each mark's shape big enough to click (at least 2,500
square px, 40 px across) and none overlapping another; the twelve in the ship's order (anticlockwise to a map's): the rat
at the top, then clockwise the boar, the dog, the rooster at the right, the monkey, the sheep, the horse at the bottom,
the snake, the dragon, the hare at the left, the tiger, the ox; the needle's tip inside the monkey's shape; the walk
patch holding the mark `default`."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ["rat", "boar", "dog", "rooster", "monkey", "sheep", "horse", "snake", "dragon", "hare", "tiger", "ox"]
THINGS_21 = ["box", "lid", "card", "bowmark", "needle"] + ORDER


def inside(poly, p):
    x, y = p
    n = len(poly)
    ok = False
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if (y0 > y) != (y1 > y):
            xi = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            if x < xi:
                ok = not ok
    return ok


def area(poly):
    a = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        a += x0 * y1 - x1 * y0
    return abs(a) / 2


def check(folder, out_png):
    problems = []
    from postimp_plans import PLANS
    plan = PLANS.get("edo-compass")
    if plan is None:
        problems.append("no plan for edo-compass in postimp_plans.py")
        plan = {"planes": [], "alt": {}, "frames": []}
    files = sorted(f for f in os.listdir(folder) if f.endswith(".png"))
    for f in files:
        im = Image.open(os.path.join(folder, f))
        if im.size != (800, 600):
            problems.append(f"{f}: {im.size}, not (800, 600)")
        name = f[:-4]
        if not (name == "back" or name in plan["planes"] or name in plan["alt"]):
            problems.append(f"{f}: not in the plan")
    for name in plan["planes"] + list(plan["alt"]):
        if f"{name}.png" not in files:
            problems.append(f"plane {name}: no file")
    lay = json.load(open(os.path.join(folder, "layout.json")))
    for key in ("closeup", "view", "walk", "marks", "hands", "things", "planes", "cutouts", "fx"):
        if key not in lay:
            problems.append(f"layout.json: no {key}")
    if "thumb" not in lay.get("hands", {}):
        problems.append("layout.json: no hand point thumb")
    if not inside(lay["walk"], lay["marks"]["default"]):
        problems.append("the mark default is outside the walk patch")
    ids = {t["id"]: t for t in lay["things"]}
    for t in THINGS_21:
        if t not in ids or not ("rect" in ids[t]["shape"] or "poly" in ids[t]["shape"]):
            problems.append(f"thing {t}: missing, or no shape")
    centre = lay["view"]["card"]["centre"]
    angs = []
    for i, name in enumerate(ORDER):
        if name not in ids:
            continue
        poly = ids[name]["shape"]["poly"]
        a = area(poly)
        xs, ys = [p[0] for p in poly], [p[1] for p in poly]
        if a < 2500 or (max(xs) - min(xs)) < 40 and (max(ys) - min(ys)) < 40:
            problems.append(f"mark {name}: too small to click ({a:.0f} square px)")
        cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
        ang = math.degrees(math.atan2(cx - centre[0], -(cy - centre[1]))) % 360
        angs.append(ang)
        if abs(((ang - i * 30) + 180) % 360 - 180) > 6:
            problems.append(f"mark {name}: at {ang:.0f} degrees clockwise from the top, not {i * 30}")
        for other in ORDER[i + 1:]:
            if other in ids:
                op = ids[other]["shape"]["poly"]
                if any(inside(op, p) for p in poly) or any(inside(poly, p) for p in op):
                    problems.append(f"marks {name} and {other} overlap")
    # the needle's tip: the farthest painted pixel of the still needle from the pin, in the monkey's direction
    nd = np.asarray(Image.open(os.path.join(folder, "needle.png")).convert("RGBA"))[..., 3] > 127
    ys, xs = np.where(nd)
    d = np.hypot(xs - centre[0], (ys - centre[1]) / 0.975)
    ang_px = (np.degrees(np.arctan2(xs - centre[0], -(ys - centre[1]))) % 360)
    sel = np.abs(((ang_px - 120) + 180) % 360 - 180) < 20
    if sel.any():
        k = np.argmax(np.where(sel, d, -1))
        tip = (int(xs[k]), int(ys[k]))
        if "monkey" in ids and not inside(ids["monkey"]["shape"]["poly"], tip):
            problems.append(f"the needle's tip {tip} is not on the monkey")
    else:
        problems.append("the needle points nowhere near the monkey")
    for pl in lay["planes"]:
        for st, fn in pl.get("states", {}).items():
            if fn not in files:
                problems.append(f"plane {pl['id']}: state {st} ({fn}) missing")
    # the check picture
    comp = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    for pl in lay["planes"]:
        comp.alpha_composite(Image.open(os.path.join(folder, pl["file"])).convert("RGBA"))
    ov = Image.new("RGBA", comp.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(ov)
    for t in lay["things"]:
        sh = t["shape"]
        col = (255, 0, 255, 220) if t["id"] in ORDER else (255, 220, 0, 220)
        if "rect" in sh:
            x, y, w, h = sh["rect"]
            dr.rectangle([x, y, x + w, y + h], outline=col)
        else:
            dr.polygon([tuple(p) for p in sh["poly"]], outline=col)
        if t["id"] in ORDER:
            xs_, ys_ = [p[0] for p in sh["poly"]], [p[1] for p in sh["poly"]]
            dr.text((sum(xs_) / len(xs_) - 12, sum(ys_) / len(ys_) - 4), t["id"], fill=(0, 0, 0, 255))
    hx, hy = lay["hands"]["thumb"]
    dr.ellipse([hx - 4, hy - 4, hx + 4, hy + 4], outline=(0, 200, 255, 255), width=2)
    dr.polygon([tuple(p) for p in lay["walk"]], outline=(40, 220, 255, 255))
    comp.alpha_composite(ov)
    comp.convert("RGB").save(out_png)
    return problems


if __name__ == "__main__":
    installed = "--installed" in sys.argv
    folder = os.path.join(HERE, "..", "..", "art", "scenes", "edo-compass") if installed else os.path.join(HERE, "out", "edo-compass")
    out_png = os.path.join(HERE, "out", "edo-compass-check-keyed.png" if installed else "edo-compass-check.png")
    problems = check(folder, out_png)
    for p in problems:
        print("PROBLEM:", p)
    print(f"{'keyed' if installed else 'painted'}: {len(problems)} problem{'s' if len(problems) != 1 else ''}; {out_png}")
    sys.exit(1 if problems else 0)

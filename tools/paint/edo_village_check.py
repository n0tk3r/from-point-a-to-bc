"""PAINT-20A: the checks on edo-village's finished pictures and its layout.json, and the check picture.

    python3 edo_village_check.py              checks out/edo-village/ (as painted) -> out/edo-village-check.png
    python3 edo_village_check.py --installed  checks art/scenes/edo-village/ (keyed) -> out/edo-village-check-keyed.png

What it holds: every picture 800 x 600 (the hens' frames 50 x 46); every file in the plan (postimp_plans) and every
plane of the plan present; layout.json complete (horizon, full, view, walk, blocked, marks, stands with grownup_px,
things with a shape, planes, cutouts, fx, the door); ROUND-20's marks all there and inside the walk outline; ROUND-20's
things all there with a shape; every fx frame file present. The check picture: the composite with the walk outline, the
blocked patches, each thing's shape, each mark, and grey stand-ins of the right heights on the marks (Mom 1.68 m, a man
of 1830 1.56, Sankichi 1.25)."""

import fnmatch
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
HZ, FULL = 300, 590
MARKS_20 = ["arrive", "board", "sankichi", "hens", "shop", "boat", "underboat", "racks", "gonroku", "cherry", "clerkFrom", "clerkTo", "east", "west"]
THINGS_20 = ["fuji", "bay", "ship", "boats", "underboat", "nets", "board", "roofs", "smoke", "hens", "fence", "cherry", "shrinepath", "gulls", "shop",
             "road", "pass", "well", "sand", "netmender", "basketwoman", "sankichi", "tokuzo", "gonroku", "masa", "kihei"]
HEIGHTS = {"mom": 168, "bigsis": 160, "lilsis": 122, "man": 156, "woman": 146, "sankichi": 125}


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


def check(folder, out_png):
    problems = []
    from postimp_plans import PLANS
    plan = PLANS.get("edo-village")
    if plan is None:
        problems.append("no plan for edo-village in postimp_plans.py")
        plan = {"planes": [], "alt": {}, "frames": []}
    files = sorted(f for f in os.listdir(folder) if f.endswith(".png"))
    for f in files:
        im = Image.open(os.path.join(folder, f))
        want = (50, 46) if f.startswith("hen-") else (800, 600)
        if im.size != want:
            problems.append(f"{f}: {im.size}, not {want}")
        name = f[:-4]
        in_plan = name == "back" or name in plan["planes"] or name in plan["alt"] or any(fnmatch.fnmatch(name, pat) for pat in plan["frames"]) \
            or any(name in v for v in plan.get("states", {}).values())
        if not in_plan:
            problems.append(f"{f}: not in the plan")
    for name in plan["planes"] + list(plan["alt"]):
        if f"{name}.png" not in files:
            problems.append(f"plane {name}: no file")
    lay = json.load(open(os.path.join(folder, "layout.json")))
    for key in ("horizon", "full", "view", "walk", "blocked", "marks", "stands", "things", "planes", "cutouts", "fx", "door"):
        if key not in lay:
            problems.append(f"layout.json: no {key}")
    if lay.get("horizon") != HZ or lay.get("full") != FULL:
        problems.append("layout.json: horizon/full are not 300/590")
    walk = lay["walk"]
    for m in MARKS_20:
        if m not in lay["marks"]:
            problems.append(f"mark {m}: missing")
        elif not inside(walk, lay["marks"][m]):
            problems.append(f"mark {m} {lay['marks'][m]}: outside the walk outline")
    for m, p in lay["marks"].items():
        if m not in MARKS_20 and not inside(walk, p):
            problems.append(f"mark {m} {p}: outside the walk outline")
        for b in lay["blocked"]:
            if inside(b, p) and m != "underboat":
                problems.append(f"mark {m} {p}: inside a blocked patch")
    for m, st in lay["stands"].items():
        if "grownup_px" not in st or st["grownup_px"] <= 0:
            problems.append(f"stand {m}: no grownup_px")
    ids = {t["id"]: t for t in lay["things"]}
    for t in THINGS_20:
        if t not in ids:
            problems.append(f"thing {t}: missing")
        elif not ("rect" in ids[t]["shape"] or "poly" in ids[t]["shape"]):
            problems.append(f"thing {t}: no shape")
    for pl in lay["planes"]:
        if f"{pl['file']}" not in files:
            problems.append(f"plane {pl['id']}: {pl['file']} missing")
        if "base" not in pl and "plane" not in pl:
            problems.append(f"plane {pl['id']}: no base or plane")
    for m in lay["fx"]:
        fr = m.get("frames")
        if isinstance(fr, dict):
            for k, v in fr.items():
                for fn in ([v] if isinstance(v, str) else v if isinstance(v, list) else []):
                    if isinstance(fn, str) and fn.endswith(".png") and fn not in files:
                        problems.append(f"fx {m['id']}: frame {fn} missing")
    plane_ids = [pl["id"] for pl in lay["planes"]]
    if plane_ids != plan["planes"]:
        problems.append(f"the plan's planes {plan['planes']} are not layout.json's {plane_ids}")
    # ---- the check picture
    comp = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    for pl in lay["planes"]:
        if pl["file"] in files:
            comp.alpha_composite(Image.open(os.path.join(folder, pl["file"])).convert("RGBA"))
    ov = Image.new("RGBA", comp.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.polygon([tuple(p) for p in walk], outline=(40, 220, 255, 255))
    for b in lay["blocked"]:
        d.polygon([tuple(p) for p in b], outline=(255, 60, 60, 255), fill=(255, 60, 60, 40))
    for t in lay["things"]:
        sh = t["shape"]
        if "rect" in sh:
            x, y, w, h = sh["rect"]
            d.rectangle([x, y, x + w, y + h], outline=(255, 255, 0, 200))
        else:
            d.polygon([tuple(p) for p in sh["poly"]], outline=(255, 255, 0, 200))
    door = lay["door"]
    d.ellipse([door["at"][0] - door["r"], door["at"][1] - door["r"], door["at"][0] + door["r"], door["at"][1] + door["r"]], outline=(57, 230, 224, 255))

    def person(at, cm, col, label=None):
        x, y = at
        hgt = 160.0 * (y - HZ) / (FULL - HZ) * cm / 175.0
        wd = hgt * 0.26
        d.rectangle([x - wd / 2, y - hgt * 0.86, x + wd / 2, y], fill=col)
        d.ellipse([x - hgt * 0.07, y - hgt, x + hgt * 0.07, y - hgt * 0.86], fill=col)
        if label:
            d.text((x + wd / 2 + 2, y - hgt), label, fill=(20, 20, 30, 255))
    for m, p in lay["marks"].items():
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=(255, 0, 255, 255))
        d.text((p[0] + 5, p[1] - 5), m, fill=(0, 0, 0, 255))
    person(lay["marks"]["arrive"], HEIGHTS["mom"], (60, 150, 110, 200), "Mom 1.68")
    person(lay["stands"]["arrive_bigsis"]["at"], HEIGHTS["bigsis"], (110, 110, 200, 200))
    person(lay["stands"]["arrive_lilsis"]["at"], HEIGHTS["lilsis"], (230, 110, 140, 200))
    person(lay["marks"]["shop"], HEIGHTS["mom"], (60, 150, 110, 160), "Mom")
    person(lay["marks"]["kihei_out"], HEIGHTS["man"], (120, 100, 90, 200), "Kihei 1.56")
    person(lay["marks"]["board"], HEIGHTS["mom"], (60, 150, 110, 160), "Mom")
    person(lay["marks"]["sankichi"], HEIGHTS["sankichi"], (120, 100, 90, 200), "Sankichi 1.25")
    person(lay["marks"]["hens"], HEIGHTS["lilsis"], (230, 110, 140, 200), "Little Sister")
    person(lay["marks"]["gonroku"], HEIGHTS["man"], (120, 100, 90, 200), "Gonroku")
    person(lay["marks"]["racks"], HEIGHTS["mom"], (60, 150, 110, 160), "Mom")
    person(lay["marks"]["masa"], HEIGHTS["woman"], (120, 100, 90, 200), "O-Masa 1.46")
    person(lay["marks"]["west"], HEIGHTS["man"], (120, 100, 90, 200), "Tokuzo")
    person(lay["marks"]["underboat"], HEIGHTS["lilsis"], (230, 110, 140, 160))
    for pl in lay["planes"]:
        b = pl.get("base")
        if isinstance(b, (int, float)):
            d.line([0, b, 800, b], fill=(255, 140, 0, 90))
    comp.alpha_composite(ov)
    comp.convert("RGB").save(out_png)
    return problems


if __name__ == "__main__":
    installed = "--installed" in sys.argv
    folder = os.path.join(HERE, "..", "..", "art", "scenes", "edo-village") if installed else os.path.join(HERE, "out", "edo-village")
    out_png = os.path.join(HERE, "out", "edo-village-check-keyed.png" if installed else "edo-village-check.png")
    problems = check(folder, out_png)
    for p in problems:
        print("PROBLEM:", p)
    print(f"{'keyed' if installed else 'painted'}: {len(problems)} problem{'s' if len(problems) != 1 else ''}; {out_png}")
    sys.exit(1 if problems else 0)

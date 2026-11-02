"""PAINT-21A: the checks on the Satta Pass's two scenes (edo-kurasawa, edo-satta): their finished pictures and layout.json,
and a check picture of each.

    python3 edo_kurasawa_check.py [edo-kurasawa|edo-satta|both]              checks out/<scene>/ (as painted)
    python3 edo_kurasawa_check.py [edo-kurasawa|edo-satta|both] --installed  checks art/scenes/<scene>/ (keyed)

What it holds: every picture 800 x 600; every file in the plan (postimp_plans) and every plane and alt of the plan present;
layout.json complete (horizon, full, view, walk, blocked, marks, stands with grownup_px, things with a shape, planes,
cutouts, fx); ROUND-21's marks all there, inside the walk outline and outside every blocked patch; ROUND-21's things all
there with a shape; every state of the cut-outs named; each cut-out hard-edged (no half-clear pixels). The check picture
(out/<scene>-check[-keyed].png): the composite with the walk outline, the blocked patches, each thing's shape, each mark,
each plane's base, and grey stand-ins of the right heights at the marks."""

import fnmatch
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SCENES = {
    "edo-kurasawa": {
        "marks": ["yui", "teahouse", "kuni", "mound", "bearers", "peddler", "komuso", "courierFrom", "courierTo", "climb"],
        "things": ["fuji", "cloud", "bay", "yuishore", "boats", "teahouse", "bench", "grill", "shells", "signboard", "mound", "hackberry",
                   "palanquin", "trunks", "road", "cliffroad", "smoke", "kuni", "sakuji", "tora", "soshichi", "komuso", "courier"],
        "people": [("teahouse", 168, "Mom 1.68"), ("kuni", 146, "O-Kuni 1.46"), ("bearers", 156, "Sakuji 1.56"), ("tora", 156, "Tora"),
                   ("peddler", 156, "Soshichi"), ("komuso", 156, "komuso"), ("mound", 168, "Mom"), ("arrive_lilsis", 122, "Little Sister 1.22"),
                   ("arrive_bigsis", 160, "Big Sister 1.60"), ("climb", 168, "Mom")],
    },
    "edo-satta": {
        "marks": ["below", "jizo", "pine", "view", "stone", "shige", "kyuzo", "mosukeFrom", "mosukeTo", "okitsu"],
        "things": ["fuji", "cloud", "bay", "izu", "oldshore", "pine", "jizo", "jizohat", "pass", "edge", "road", "okitsu", "temple", "gulls",
                   "mosuke", "shige", "kyuzo"],
        "people": [("jizo", 122, "Little Sister 1.22"), ("view", 168, "Mom 1.68"), ("pine", 160, "Big Sister"), ("shige", 146, "O-Shige 1.46"),
                   ("kyuzo", 156, "Kyuzo 1.56"), ("mosukeFrom", 156, "Mosuke"), ("below", 168, "Mom"), ("okitsu", 168, "Mom")],
    },
}


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


def check(scene, folder, out_png):
    want = SCENES[scene]
    problems = []
    from postimp_plans import PLANS
    plan = PLANS.get(scene)
    if plan is None:
        problems.append(f"no plan for {scene} in postimp_plans.py")
        plan = {"planes": [], "alt": {}, "frames": []}
    files = sorted(f for f in os.listdir(folder) if f.endswith(".png"))
    for f in files:
        im = Image.open(os.path.join(folder, f))
        if im.size != (800, 600):
            problems.append(f"{f}: {im.size}, not (800, 600)")
        name = f[:-4]
        in_plan = name == "back" or name in plan["planes"] or name in plan["alt"] or any(fnmatch.fnmatch(name, pat) for pat in plan["frames"]) \
            or any(name in v for v in plan.get("states", {}).values())
        if not in_plan:
            problems.append(f"{f}: not in the plan")
        if name != "back":
            a = np.asarray(im.convert("RGBA"))[..., 3]
            half = ((a > 0) & (a < 255)).sum()
            if half:
                problems.append(f"{f}: {half} half-clear pixels (a cut-out must be hard-edged)")
    for name in plan["planes"] + list(plan["alt"]):
        if f"{name}.png" not in files:
            problems.append(f"plane {name}: no file")
    lay = json.load(open(os.path.join(folder, "layout.json")))
    for key in ("horizon", "full", "view", "walk", "blocked", "marks", "stands", "things", "planes", "cutouts", "fx"):
        if key not in lay:
            problems.append(f"layout.json: no {key}")
    walk = lay["walk"]
    for m in want["marks"]:
        if m not in lay["marks"]:
            problems.append(f"mark {m}: missing")
    for m, p in lay["marks"].items():
        if not inside(walk, p):
            problems.append(f"mark {m} {p}: outside the walk outline")
        for b in lay["blocked"]:
            if inside(b, p):
                problems.append(f"mark {m} {p}: inside a blocked patch")
    for m, st in lay["stands"].items():
        if not isinstance(st, dict):
            continue
        if "grownup_px" not in st or st["grownup_px"] <= 0:
            problems.append(f"stand {m}: no grownup_px")
        else:
            y = st["at"][1]
            exp = round(160 * (y - lay["horizon"]) / (lay["full"] - lay["horizon"]))
            if abs(exp - st["grownup_px"]) > 1:
                problems.append(f"stand {m}: grownup_px {st['grownup_px']} is not the scene's rule ({exp})")
    ids = {t["id"]: t for t in lay["things"]}
    for t in want["things"]:
        if t not in ids:
            problems.append(f"thing {t}: missing")
        elif not ("rect" in ids[t]["shape"] or "poly" in ids[t]["shape"]):
            problems.append(f"thing {t}: no shape")
    for t in lay["things"]:
        if "stand" in t and not inside(walk, t["stand"]):
            problems.append(f"thing {t['id']}: its stand {t['stand']} is outside the walk outline")
    for pl in lay["planes"]:
        if pl["file"] not in files:
            problems.append(f"plane {pl['id']}: {pl['file']} missing")
        if "base" not in pl and "plane" not in pl:
            problems.append(f"plane {pl['id']}: no base or plane")
    plane_ids = [pl["id"] for pl in lay["planes"] if not pl.get("alt")]
    if plane_ids != plan["planes"]:
        problems.append(f"the plan's planes {plan['planes']} are not layout.json's {plane_ids}")
    alts = [pl["id"] for pl in lay["planes"] if pl.get("alt")]
    if sorted(alts) != sorted(plan["alt"]):
        problems.append(f"the plan's alts {sorted(plan['alt'])} are not layout.json's {sorted(alts)}")
    # ---- the check picture
    comp = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    for pl in lay["planes"]:
        if pl["file"] in files and not pl.get("alt"):
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
            d.rectangle([x, y, x + w, y + h], outline=(255, 255, 0, 170))
        else:
            d.polygon([tuple(p) for p in sh["poly"]], outline=(255, 255, 0, 170))
    hz, full = lay["horizon"], lay["full"]

    def person(at, cm, col, label=None):
        x, y = at
        hgt = 160.0 * (y - hz) / (full - hz) * cm / 175.0
        wd = hgt * 0.26
        d.rectangle([x - wd / 2, y - hgt * 0.86, x + wd / 2, y], fill=col)
        d.ellipse([x - hgt * 0.07, y - hgt, x + hgt * 0.07, y - hgt * 0.86], fill=col)
        if label:
            d.text((x + wd / 2 + 2, y - hgt), label, fill=(20, 20, 30, 255))
    for m, p in lay["marks"].items():
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=(255, 0, 255, 255))
        d.text((p[0] + 5, p[1] - 5), m, fill=(0, 0, 0, 255))
    for m, cm, label in want["people"]:
        if m in lay["marks"] or m in lay["stands"]:
            at = lay["marks"].get(m) or lay["stands"][m]["at"]
            person(at, cm, (60, 150, 110, 170) if cm >= 160 else (230, 110, 140, 190) if cm < 130 else (120, 100, 90, 190), label)
    for pl in lay["planes"]:
        b = pl.get("base")
        if isinstance(b, (int, float)):
            d.line([0, b, 800, b], fill=(255, 140, 0, 90))
    comp.alpha_composite(ov)
    comp.convert("RGB").save(out_png)
    return problems


if __name__ == "__main__":
    installed = "--installed" in sys.argv
    names = [a for a in sys.argv[1:] if not a.startswith("--")]
    which = names[0] if names else "both"
    todo = list(SCENES) if which == "both" else [which]
    bad = 0
    for scene in todo:
        folder = os.path.join(HERE, "..", "..", "art", "scenes", scene) if installed else os.path.join(HERE, "out", scene)
        if not os.path.isdir(folder):
            print(f"{scene}: nothing at {folder}")
            bad += 1
            continue
        out_png = os.path.join(HERE, "out", f"{scene}-check{'-keyed' if installed else ''}.png")
        problems = check(scene, folder, out_png)
        for p in problems:
            print(f"PROBLEM {scene}:", p)
        print(f"{scene} {'keyed' if installed else 'painted'}: {len(problems)} problem{'s' if len(problems) != 1 else ''}; {out_png}")
        bad += len(problems)
    sys.exit(1 if bad else 0)

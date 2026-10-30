"""PAINT-20C: checks and check pictures for edo-cedars and edo-storehouse.

    python3 edo_c_check.py [shots-dir]

Checks: every file 800x600 and in the plan; every mark of ROUND-20's list present and inside the walk outline; every
cut-out state file there; every thing of ROUND-20's list with a shape; then writes pictures with stand-in people at
the marks (grown-up 160 px at `full`, the children at their heights; a man of 1.56 m where asked) on the painting as
painted (out/) and as keyed (art/), with a stand-in of rain lines over the cedar path."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

from postimp_plans import PLANS

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "..", "..", "art", "scenes")
SHOTS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "edo-c-shots")
NEED_MARKS = {"edo-cedars": ["enter", "figure", "pipe", "door", "window", "isukeFrom"],
              "edo-storehouse": ["door", "windowIn", "sacks", "mat", "trapdoor", "lantern", "isuke"]}
NEED_THINGS = {"edo-cedars": ["cedars", "steps", "figure", "mist", "pipe", "storehouse", "door", "window", "eaves", "rain", "light", "kiln", "isuke"],
               "edo-storehouse": ["sacks", "mat", "trapdoor", "floorgaps", "door", "bar", "window", "tools", "lantern", "baskets", "straw", "isuke", "jinsuke"]}
STATES = {"edo-cedars": ["light-on", "window-lit"], "edo-storehouse": ["bar", "bar-up", "door", "door-open", "mat", "mat-aside", "trapdoor", "trapdoor-open", "sacks", "sacks-heaped", "floorgaps-on", "lantern", "lantern-lit"]}
PEOPLE = {"mom": (168, (0.16, 0.65, 0.45)), "bigsis": (160, (0.25, 0.25, 0.55)), "lilsis": (122, (0.9, 0.45, 0.6)), "man": (156, (0.6, 0.5, 0.35)), "girl": (118, (0.8, 0.6, 0.4))}


def inside(poly, p):
    x, y = p
    n = len(poly)
    ins = False
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if (y0 > y) != (y1 > y):
            xi = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            if xi > x:
                ins = not ins
    return ins


def check(scene, folder):
    lay = json.load(open(os.path.join(folder, "layout.json")))
    plan = PLANS[scene]
    named = {"back"} | set(plan["planes"]) | set(plan["alt"])
    bad = []
    for f in sorted(os.listdir(folder)):
        if f.endswith(".png"):
            im = Image.open(os.path.join(folder, f))
            if im.size != (800, 600):
                bad.append(f"{f}: {im.size}")
            if f[:-4] not in named:
                bad.append(f"{f}: not in the plan")
    for n in named:
        if not os.path.exists(os.path.join(folder, n + ".png")):
            bad.append(f"{n}.png missing")
    for st in STATES[scene]:
        if not os.path.exists(os.path.join(folder, st + ".png")):
            bad.append(f"state {st}.png missing")
    walk = lay["walk"]
    for m in NEED_MARKS[scene]:
        if m not in lay["marks"]:
            bad.append(f"mark {m} missing")
            continue
        p = lay["marks"][m]
        if m == "windowIn":
            continue                                               # on the sacks, not the floor
        if not inside(walk, p):
            bad.append(f"mark {m} {p} outside the walk")
    ids = {t["id"] for t in lay["things"]}
    for t in NEED_THINGS[scene]:
        if t not in ids:
            bad.append(f"thing {t} has no shape")
    for t in lay["things"]:
        if "shape" not in t or not (t["shape"].get("poly") or t["shape"].get("rect")):
            bad.append(f"thing {t['id']}: no shape")
    if scene == "edo-cedars":
        for p in lay["isukeWay"]:
            if not inside(walk, p) and p[1] < 598:
                bad.append(f"isukeWay point {p} outside the walk")
    print(scene, folder, "OK" if not bad else "PROBLEMS")
    for b in bad:
        print("  -", b)
    return lay, not bad


def standin(d, who, x, y, px, label):
    h, c = PEOPLE[who]
    hp = px * h / 175.0
    col = tuple(int(v * 255) for v in c)
    w = hp * 0.3
    d.rectangle([x - w / 2, y - hp * 0.86, x + w / 2, y], fill=col, outline=(20, 20, 30))
    d.ellipse([x - hp * 0.08, y - hp, x + hp * 0.08, y - hp * 0.84], fill=(240, 200, 170), outline=(20, 20, 30))
    d.ellipse([x - w, y - 3, x + w, y + 3], outline=(255, 255, 0))
    d.text((x + w / 2 + 2, y - hp * 0.5), label, fill=(255, 255, 160))


def grown_px(lay, y):
    return 160.0 * (y - lay["horizon"]) / (lay["full"] - lay["horizon"])


def compose(folder, scene, extra=()):
    plan = PLANS[scene]
    im = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    for n in list(plan["planes"]) + list(extra):
        p = os.path.join(folder, n + ".png")
        if os.path.exists(p):
            im.alpha_composite(Image.open(p).convert("RGBA"))
    return im


def rain(im, lay, seed=1):
    rng = np.random.default_rng(seed)
    d = ImageDraw.Draw(im, "RGBA")
    r = [f for f in lay["fx"] if f["type"] == "rain"][0]
    n = int(800 * 600 * r["density"])
    dx = r["slant"][0] / 100.0
    hide = [[tuple(p) for p in poly] for poly in r.get("behind", [])]
    for i in range(n):
        x, y = rng.uniform(0, 800), rng.uniform(0, 600)
        if any(inside(h, (x, y)) for h in hide):
            continue
        ln = rng.uniform(*r["length"])
        d.line([x, y, x - dx * ln, y + ln], fill=(223, 230, 236, int(255 * r["opacity"])), width=1)
    return im


def shots(scene, lay, label):
    os.makedirs(SHOTS, exist_ok=True)
    for src, tag in ((os.path.join(HERE, "out", scene), "unkeyed"), (os.path.join(ART, scene), "keyed")):
        if not os.path.exists(os.path.join(src, "back.png")):
            continue
        if scene == "edo-cedars":
            im = compose(src, scene, ["light-on"])
            d = ImageDraw.Draw(im)
            M = lay["marks"]
            for who, (dx, dy) in (("mom", (0, 0)), ("bigsis", (-40, 8)), ("lilsis", (34, 10))):
                x, y = M["enter"][0] + dx, M["enter"][1] + dy
                standin(d, who, x, y, grown_px(lay, y), who)
            for who, (dx, dy) in (("mom", (0, 0)), ("bigsis", (-26, 6))):
                x, y = M["door"][0] + dx, M["door"][1] + dy
                standin(d, who, x, y, grown_px(lay, y), who)
            x, y = M["window"]
            standin(d, "lilsis", x, y, grown_px(lay, y), "lilsis")
            x, y = M["figure"]
            standin(d, "lilsis", x, y, grown_px(lay, y), "lilsis@figure")
            for p in lay["isukeWay"][1:4:2]:
                standin(d, "man", p[0], p[1], grown_px(lay, p[1]), "isuke")
            d.polygon([tuple(p) for p in lay["walk"]], outline=(0, 255, 255))
            im.convert("RGB").save(os.path.join(SHOTS, f"cedars-{tag}-people.png"))
            rain(compose(src, scene, ["light-on"]), lay).convert("RGB").save(os.path.join(SHOTS, f"cedars-{tag}-rain.png"))
            compose(src, scene, []).convert("RGB").save(os.path.join(SHOTS, f"cedars-{tag}-light-off.png"))
            compose(src, scene, ["light-on", "window-lit"]).convert("RGB").save(os.path.join(SHOTS, f"cedars-{tag}-window-lit.png"))
        else:
            im = compose(src, scene)
            d = ImageDraw.Draw(im)
            M = lay["marks"]
            x, y = M["isuke"]
            standin(d, "man", x, y, grown_px(lay, y), "isuke 1.56 m")
            for who, m in (("bigsis", "mat"), ("lilsis", "trapdoor"), ("mom", "lantern")):
                x, y = M[m]
                standin(d, who, x, y, grown_px(lay, y), f"{who}@{m}")
            x, y = M["windowIn"]
            px = lay["stands"]["windowIn"]["grownup_px"]
            standin(d, "lilsis", x, y, px, "lilsis@windowIn")
            d.polygon([tuple(p) for p in lay["walk"]], outline=(0, 255, 255))
            im.convert("RGB").save(os.path.join(SHOTS, f"store-{tag}-people.png"))
            alts = compose(src, scene, ["floorgaps-on", "lantern-lit", "sacks-heaped", "door-open", "bar-up", "mat-aside", "trapdoor-open"])
            alts.convert("RGB").save(os.path.join(SHOTS, f"store-{tag}-states.png"))
            compose(src, scene).convert("RGB").save(os.path.join(SHOTS, f"store-{tag}-first.png"))


def beside():
    """The two keyed scenes beside a Rome and a Nevada scene at the same size: a print among paintings, not another game."""
    tiles = []
    for scene in ("rome-tiber", "edo-cedars", "nevada-roadside", "edo-storehouse"):
        folder = os.path.join(ART, scene)
        if not os.path.exists(os.path.join(folder, "back.png")):
            continue
        im = compose(folder, scene).convert("RGB").resize((400, 300), Image.LANCZOS)
        ImageDraw.Draw(im).text((6, 4), scene, fill=(255, 255, 200))
        tiles.append(im)
    sheet = Image.new("RGB", (800, 600), (20, 20, 20))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 2) * 400, (i // 2) * 300))
    os.makedirs(SHOTS, exist_ok=True)
    sheet.save(os.path.join(SHOTS, "beside-rome-nevada.png"))


if __name__ == "__main__":
    ok = True
    beside()
    for scene in ("edo-cedars", "edo-storehouse"):
        for folder in (os.path.join(HERE, "out", scene), os.path.join(ART, scene)):
            if os.path.exists(os.path.join(folder, "layout.json")):
                lay, good = check(scene, folder)
                ok = ok and good
        if os.path.exists(os.path.join(HERE, "out", scene, "layout.json")):
            shots(scene, json.load(open(os.path.join(HERE, "out", scene, "layout.json"))), scene)
    print("ALL OK" if ok else "PROBLEMS")

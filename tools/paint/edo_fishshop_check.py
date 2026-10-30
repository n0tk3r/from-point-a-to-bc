"""Checks on Kihei's shop as installed (art/scenes/edo-fishshop/) and its layout.json. PAINT-20B.

    python3 edo_fishshop_check.py          the checks, then the check picture (layout.json drawn over the comp:
                                           out/edo-fishshop-check.png)

What it holds (each a line, "ok" or what is wrong; the exit code is the number of failures):
  - every picture file in the folder is in the scene's plan (postimp_plans.PLANS) and every file of the plan is there;
    back.png 800x600 and opaque; each cut-out and state 800x600 with a clear colour and a hard edge; the cat's frames
    all one canvas, each with something on it, and cat.json naming every one;
  - the planes of layout.json are the plan's, each alt replacing a plane that exists, each base a row inside the picture
    or "front"/"back"; the sushi box's three states each a file;
  - the marks ROUND-20.md names (door, kihei, press, step, tami, baby, hearth, print, money, godshelf, cat, under), each
    inside the walk outline, every grown-up there between 115 and 196 pixels tall; the three seats with a seat row;
  - a thing with a shape for every thing ROUND-20.md lists for the shop, every shape inside the picture, no id twice;
  - the walk outline clear of the cut-outs' solid ground;
  - every fx mark with a kind the engine has, and a base."""

import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

from postimp_plans import PLANS

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.normpath(os.path.join(HERE, "..", "..", "art", "scenes", "edo-fishshop"))
SCENE = "edo-fishshop"
NEEDED_MARKS = ["door", "kihei", "press", "step", "tami", "baby", "hearth", "print", "money", "godshelf", "cat", "under"]
NEEDED_THINGS = ["kihei", "tami", "baby", "cat", "tubs", "cuttingboard", "sushibox", "hearth", "driedfish", "print", "money", "godshelf",
                 "step", "street", "noren", "sandals", "hats", "chest"]
KINDS = {"smoke", "flame", "embers", "ripples", "stream", "shimmer", "birds", "sway", "bob", "strip", "drive", "portal"}
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
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).polygon([tuple(p) for p in poly], fill=255)
    return np.asarray(m) > 0


def main():
    lo = json.load(open(os.path.join(ART, "layout.json")))
    plan = PLANS[SCENE]
    files = sorted(f for f in os.listdir(ART) if f.endswith(".png"))
    planned = set(plan["planes"]) | set(plan["alt"]) | set(sum(plan["states"].values(), []) if "states" in plan else [])
    cats = [f for f in files if f.startswith("cat-")]
    others = [f[:-4] for f in files if not f.startswith("cat-") and f != "back.png"]
    say(set(others) == planned, f"the plan's files are the folder's: {sorted(set(others) ^ planned) or 'all'}")
    say("back.png" in files, "back.png is there")
    back = Image.open(os.path.join(ART, "back.png"))
    say(back.size == (800, 600) and back.mode == "P" and "transparency" not in back.info, f"back.png 800x600, a palette, opaque ({back.size}, {back.mode})")
    for n in sorted(planned):
        im = Image.open(os.path.join(ART, n + ".png"))
        a = np.asarray(im.convert("RGBA"))[..., 3]
        ok = im.size == (800, 600) and im.mode == "P" and "transparency" in im.info and 0 < (a > 0).sum() < 800 * 600 and set(np.unique(a)) <= {0, 255}
        say(ok, f"{n}.png 800x600, a clear colour, a hard edge, something on it ({(a > 0).sum()} px)")
    cat = json.load(open(os.path.join(ART, "cat.json")))
    named = sorted(sum(cat["frames"].values(), []))
    say(named == sorted(cats), f"cat.json names the cat's frames ({len(cats)})")
    sizes = {Image.open(os.path.join(ART, f)).size for f in cats}
    say(sizes == {tuple(cat["canvas"])}, f"the cat's frames one canvas {cat['canvas']} ({sizes})")
    for f in cats:
        a = np.asarray(Image.open(os.path.join(ART, f)).convert("RGBA"))[..., 3]
        say((a > 0).sum() > 20 and a[cat["foot"][1] + 1:, :].sum() == 0, f"{f}: something on it, nothing below the foot row")
    # planes and states
    ids = [p["id"] for p in lo["planes"]]
    say(len(ids) == len(set(ids)), "no plane twice")
    for p in lo["planes"]:
        pic = p["picture"][:-4]
        say(pic in planned, f"plane {p['id']}: {p['picture']} is in the plan")
        b = p["base"]
        say(b in ("front", "back") or (isinstance(b, (int, float)) and 0 < b < 600), f"plane {p['id']}: base {b}")
        for st, f in (p.get("states") or {}).items():
            say(os.path.exists(os.path.join(ART, f)), f"plane {p['id']} state {st}: {f} exists")
    sb = [p for p in lo["planes"] if p["id"] == "sushibox"][0]
    say(set(sb["states"]) == {"empty", "filled", "cut"}, "the sushi box has its three states")
    # marks
    walk = lo["walk"]
    for k in NEEDED_MARKS:
        m = lo["marks"].get(k)
        say(m is not None, f"mark {k}")
        if not m:
            continue
        at = m["at"]
        say(inside(at, walk), f"mark {k} at {at} inside the walk")
        say(115 <= m["grownup_px"] <= 196, f"mark {k}: a grown-up {m['grownup_px']} px (115..196)")
    for k in ("stepmom", "stepbig", "steplil"):
        s = lo["seats"].get(k)
        say(s is not None and s["seat_row"] < s["at"][1] and s["seat_cm"] == 45, f"seat {k}: seat row {s and s['seat_row']} above the mark, 45 cm")
    # things
    for k in NEEDED_THINGS:
        t = lo["things"].get(k)
        say(t is not None and ("shape" in t or "at" in t), f"thing {k} with a shape (or a place)")
        if t and "shape" in t:
            say(all(0 <= x <= 800 and 0 <= y <= 600 for x, y in t["shape"]), f"thing {k}: shape inside the picture")
    # the walk clear of solid ground
    wm = poly_mask(walk)
    for p in lo["planes"]:
        if "solid" in p:
            sm = poly_mask(p["solid"])
            say(not (wm & sm).any(), f"plane {p['id']}: its solid ground is outside the walk")
    # fx
    for m in lo["fx"]:
        say(m["type"] in KINDS, f"fx {m['id']}: kind {m['type']}")
        say("base" in m or "plane" in m, f"fx {m['id']}: has a base or a plane")
    # the check picture
    comp = back.convert("RGBA")
    for p in lo["planes"]:
        c = Image.open(os.path.join(ART, p["picture"])).convert("RGBA")
        comp.alpha_composite(c)
    d = ImageDraw.Draw(comp)
    d.polygon([tuple(p) for p in walk], outline=(255, 255, 0, 255))
    for k, m in lo["marks"].items():
        x, y = m["at"]
        d.ellipse([x - 3, y - 3, x + 3, y + 3], outline=(255, 60, 60, 255))
        d.text((x + 4, y - 12), k, fill=(255, 60, 60, 255))
    for k, t in lo["things"].items():
        if "shape" in t:
            d.polygon([tuple(p) for p in t["shape"]], outline=(60, 220, 255, 255))
            d.text((t["shape"][0][0] + 2, t["shape"][0][1] + 2), k, fill=(60, 220, 255, 255))
    for p in lo["planes"]:
        if isinstance(p["base"], (int, float)):
            d.line([(0, p["base"]), (800, p["base"])], fill=(255, 140, 0, 120))
        if "solid" in p:
            d.polygon([tuple(q) for q in p["solid"]], outline=(255, 140, 0, 255))
    for m in lo["fx"]:
        if "at" in m:
            x, y = m["at"]
            d.rectangle([x - 2, y - 2, x + 2, y + 2], outline=(255, 255, 255, 255))
    d.line([(0, lo["horizon"]), (800, lo["horizon"])], fill=(255, 255, 255, 120))
    d.line([(0, lo["full"]), (800, lo["full"])], fill=(255, 255, 255, 120))
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    comp.save(os.path.join(HERE, "out", "edo-fishshop-check.png"))
    print(f"{len(fails)} failure{'s' if len(fails) != 1 else ''}; out/edo-fishshop-check.png")
    return len(fails)


if __name__ == "__main__":
    sys.exit(main())

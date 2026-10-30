"""PAINT-20E: the checks on the two rooms of the keep, and their check pictures.

    python3 edo_keep_check.py edo-keep [out|art] [shots_dir]
    python3 edo_keep_check.py edo-keeptop [out|art] [shots_dir]

Checks: every file of the plan is there and 800 x 600, a palette picture with one clear colour for the cut-outs (an RGBA
for the light pictures and the flight frames); layout.json has horizon, full, view, walk, blocked, marks, stands with
grownup_px, things, planes, fx; every mark is on the stage and inside the walk outline (or on a thing's own ground);
every plane's base is on the stage; the keep: three beams, each with a port, a patch and an air polygon, the patch
below the port; the top floor: the hum inside the door's `keep` columns, the door's foot above the hum, the patch's
radius growing from `hum` to `farwest`, the three shutters with their four files each.
Pictures: <scene>-composed-<state>.png (the picture as the game lays it), <scene>-standins-<state>.png (stand-in people
at every mark, the beams or the patch and the door stand-ins), <scene>-layout.png (walk, blocked, bases, marks, shapes
drawn over it)."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

from edo_keep_kit import stand_in, to_image, W, H


def load(folder, name):
    return Image.open(os.path.join(folder, name if name.endswith(".png") else name + ".png"))


def rgb_of(folder, name):
    return np.asarray(load(folder, name).convert("RGB"), np.float32) / 255


def rgba_of(folder, name):
    return np.asarray(load(folder, name).convert("RGBA"), np.float32) / 255


def lay(img, folder, name, screen=False):
    c = rgba_of(folder, name)
    a = c[..., 3:4]
    if screen:
        return img * (1 - a) + (1 - (1 - img) * (1 - c[..., :3])) * a
    return np.where(a >= 0.5, c[..., :3], img)


def inside(pt, poly):
    x, y = pt
    n = len(poly)
    ok = False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xi = x1 + (y - y1) * (x2 - x1) / (y2 - y1 + 1e-9)
            if x < xi:
                ok = not ok
    return ok


def check_common(scene, folder, lay_):
    problems = []
    files = sorted(f for f in os.listdir(folder) if f.endswith(".png"))
    for f in files:
        im = load(folder, f)
        if f.startswith("heron-fly"):
            if im.mode != "RGBA":
                problems.append(f"{f}: a flight frame should be RGBA")
            continue
        if im.size != (W, H):
            problems.append(f"{f}: {im.size}, not {W}x{H}")
        if f.startswith("beam-"):
            if im.mode != "RGBA":
                problems.append(f"{f}: a light picture should be RGBA")
            continue
        if im.mode != "P":
            problems.append(f"{f}: not a palette picture ({im.mode})")
        elif f not in ("back.png", "lit.png") and "transparency" not in im.info:
            problems.append(f"{f}: a cut-out with no clear colour")
    for key in ("horizon", "full", "view", "walk", "blocked", "marks", "stands", "things", "planes", "fx"):
        if key not in lay_:
            problems.append(f"layout.json: no `{key}`")
    walk = lay_["walk"]
    for name, m in lay_["marks"].items():
        x, y = m["at"]
        if not (0 <= x < W and 0 <= y < H):
            problems.append(f"mark {name} off the stage: {m['at']}")
        if not inside((x, y), walk) and name not in ("drop",):
            problems.append(f"mark {name} outside the walk outline: {m['at']}")
        if name not in lay_["stands"] or "grownup_px" not in lay_["stands"][name]:
            problems.append(f"stands: no grownup_px for {name}")
    for p in lay_["planes"]:
        src = p["src"]
        if not os.path.exists(os.path.join(folder, src)):
            problems.append(f"plane {p['id']}: {src} missing")
        for k in ("lit", "open", "open_lit"):
            if k in p and not os.path.exists(os.path.join(folder, p[k])):
                problems.append(f"plane {p['id']}: {p[k]} missing")
        b = p.get("base")
        if isinstance(b, list):
            for q in b:
                if not (0 <= q[0] <= W and 0 <= q[1] <= H):
                    problems.append(f"plane {p['id']}: base off the stage {b}")
        elif isinstance(b, (int, float)) and not (0 <= b <= H):
            problems.append(f"plane {p['id']}: base row {b} off the stage")
    return problems


def check_keep(folder, lay_):
    problems = []
    beams = lay_.get("beams", [])
    if len(beams) != 3:
        problems.append(f"{len(beams)} beams, not 3")
    for b in beams:
        for k in ("port", "patch", "air"):
            if k not in b or len(b[k]) < 3:
                problems.append(f"beam {b.get('kind')}: no {k} polygon")
        if b.get("port") and b.get("patch"):
            if max(p[1] for p in b["port"]) >= min(p[1] for p in b["patch"]):
                problems.append(f"beam {b['kind']}: its patch is not below its port")
        if not os.path.exists(os.path.join(folder, b["src"])):
            problems.append(f"beam {b['kind']}: {b['src']} missing")
    return problems


def check_top(folder, lay_):
    problems = []
    door, hum, patch = lay_["door"], lay_["hum"], lay_["patch"]
    if not (door["keep"][0] <= hum["at"][0] <= door["keep"][1]):
        problems.append(f"the hum {hum['at']} is outside the door's keep columns {door['keep']}")
    if not (door["at"][1] + door["r"] <= door["base"] + 2):
        problems.append(f"the door's foot {door['at'][1] + door['r']} is below its base {door['base']}")
    rs = [patch["at_marks"][k]["radius_px"] for k in ("hum", "m1", "m2", "m3", "farwest")]
    if rs != sorted(rs):
        problems.append(f"the patch does not grow from hum to farwest: {rs}")
    if not (patch["at_marks"]["hum"]["diameter_cm"] <= 30 and patch["at_marks"]["farwest"]["diameter_cm"] >= 190):
        problems.append("the patch is not a hand's breadth at hum and a doorway at farwest")
    for n in ("north", "east", "west"):
        want = [f"{n}shutter.png", f"{n}shutter-open.png", f"{n}shutter-open-lit.png"] + ([f"{n}shutter-lit.png"] if n != "west" else [])
        for f in want:
            if not os.path.exists(os.path.join(folder, f)):
                problems.append(f"{f} missing")
    if not os.path.exists(os.path.join(folder, "lit.png")):
        problems.append("lit.png missing")
    for i in (1, 2, 3):
        if not os.path.exists(os.path.join(folder, f"heron-fly-{i}.png")):
            problems.append(f"heron-fly-{i}.png missing")
    return problems


def standins(img, lay_, names=None, color="#e0d4c0"):
    hz, full = lay_["horizon"], lay_["full"]
    for name, m in lay_["marks"].items():
        if names and name not in names:
            continue
        x, y = m["at"]
        h = 160 * (y - hz) / (full - hz)
        stand_in(img, x, y, h, color)
    return img


def draw_layout(img, lay_):
    im = to_image(img)
    d = ImageDraw.Draw(im)
    d.polygon([tuple(p) for p in lay_["walk"]], outline=(60, 230, 60))
    for b in lay_["blocked"]:
        d.polygon([tuple(p) for p in b["poly"]], outline=(230, 60, 60))
    for p in lay_["planes"]:
        b = p.get("base")
        if isinstance(b, list):
            d.line([tuple(b[0]), tuple(b[1])], fill=(255, 200, 0), width=2)
        elif isinstance(b, (int, float)):
            d.line([(0, b), (W, b)], fill=(255, 200, 0), width=1)
    for name, m in lay_["marks"].items():
        x, y = m["at"]
        d.ellipse([x - 4, y - 4, x + 4, y + 4], outline=(60, 200, 255), width=2)
        d.text((x + 6, y - 12), name, fill=(60, 200, 255))
    for name, t in lay_["things"].items():
        poly = t.get("poly")
        if isinstance(poly, list) and len(poly) >= 3:
            d.polygon([tuple(p) for p in poly], outline=(255, 120, 255))
    if "hum" in lay_:
        x, y = lay_["hum"]["at"]
        r, wd = lay_["door"]["r"], lay_["door"]["wide"]
        d.ellipse([x - r * wd, y - r, x + r * wd, y + r], outline=(57, 230, 224), width=2)
    return im


def main():
    scene = sys.argv[1]
    where = sys.argv[2] if len(sys.argv) > 2 else "out"
    shots = sys.argv[3] if len(sys.argv) > 3 else "out/" + scene + "-check"
    folder = os.path.join("out", scene) if where == "out" else os.path.join("..", "..", "art", "scenes", scene)
    os.makedirs(shots, exist_ok=True)
    lay_ = json.load(open(os.path.join(folder, "layout.json")))
    problems = check_common(scene, folder, lay_)
    if scene == "edo-keep":
        problems += check_keep(folder, lay_)
        img = rgb_of(folder, "back")
        for b in lay_["beams"]:
            img = lay(img, folder, b["src"], screen=True)
        for p in lay_["planes"]:
            img = lay(img, folder, p["src"])
        to_image(img).save(f"{shots}/{scene}-composed-{where}.png")
        to_image(standins(img.copy(), lay_)).save(f"{shots}/{scene}-standins-{where}.png")
        draw_layout(img, lay_).save(f"{shots}/{scene}-layout-{where}.png")
    else:
        problems += check_top(folder, lay_)
        # shut: back + the planes' first state
        img = rgb_of(folder, "back")
        for p in lay_["planes"]:
            img = lay(img, folder, p["src"])
        to_image(img).save(f"{shots}/{scene}-composed-shut-{where}.png")
        to_image(standins(img.copy(), lay_)).save(f"{shots}/{scene}-standins-shut-{where}.png")
        draw_layout(img, lay_).save(f"{shots}/{scene}-layout-{where}.png")
        # lit: lit + every plane's lit twin, the west shutters open
        img = rgb_of(folder, "lit")
        for p in lay_["planes"]:
            src = p.get("open_lit") if p["id"] == "westshutter" else p.get("lit", p["src"])
            img = lay(img, folder, src)
        to_image(img).save(f"{shots}/{scene}-composed-lit-{where}.png")
        # the patch and the door stand-ins at each mark: the patch a disc of its radius on the hum, the door an oval
        hx, hy = lay_["hum"]["at"]
        wd = lay_["door"]["wide"]
        for k in ("hum", "m1", "m2", "m3", "farwest"):
            pic = img.copy()
            r = lay_["patch"]["at_marks"][k]["radius_px"]
            im = to_image(standins(pic, lay_, names=(k,), color="#f0e0c0"))
            d = ImageDraw.Draw(im, "RGBA")
            d.ellipse([hx - r * wd, hy - r, hx + r * wd, hy + r], fill=(255, 244, 216, 200), outline=(57, 230, 224, 255), width=2)
            d.text((hx - 30, hy + r + 6), f"{k}: patch {lay_['patch']['at_marks'][k]['diameter_cm']} cm, r {r} px", fill=(255, 255, 255))
            im.save(f"{shots}/{scene}-patch-{k}-{where}.png")
        # the door wide open, with the family stand-ins before it
        pic = img.copy()
        im = to_image(standins(pic, lay_, names=("hum", "shinnosuke"), color="#f0e0c0"))
        d = ImageDraw.Draw(im, "RGBA")
        r = lay_["door"]["r"]
        d.ellipse([hx - r * wd, hy - r, hx + r * wd, hy + r], fill=(255, 244, 216, 150), outline=(57, 230, 224, 255), width=3)
        im.save(f"{shots}/{scene}-door-{where}.png")
        # the other two bays open, in the dark room
        img = rgb_of(folder, "back")
        for p in lay_["planes"]:
            src = p.get("open") if p["id"] in ("northshutter", "eastshutter") else p["src"]
            img = lay(img, folder, src)
        to_image(img).save(f"{shots}/{scene}-composed-northeast-open-{where}.png")
    print(f"{scene} ({where}): " + ("no problems" if not problems else f"{len(problems)} problem(s)"))
    for p in problems:
        print("  -", p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

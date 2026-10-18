"""Checks on the Office's two rooms as painted (out/) and as installed (art/scenes/): the files, their sizes and edges, the
plan, layout.json against the brief, and the pictures drawn with layout.json over them. OFFICE-17C.

    python3 office_check.py            both rooms
    python3 office_check.py office-room

What it holds (and says, room by room):
  - every picture file is in the scene's plan (postimp_plans.py) and the plan's every file is there; the scene has its key;
  - every picture is 800x600; every cut-out has a clear colour and hard edges (each pixel fully there or not at all), and
    is not empty; an alt lies where the cut-out it replaces lies (their boxes overlap);
  - the frames (the clock's second hand, the cooler's bubble) are cropped to one box, all of them the same size;
  - layout.json has the brief's marks (OFFICE-17.md, "Marks every painter names"), a stand with grownup_px for every
    stand place, the brief's clickable things, a plane for every cut-out, every shape inside the picture, every stand
    place inside the walk outline (but the seated and the perched), and the walk keeps off the picture's edges;
  - installed, each file is the keyed copy postimp_keyed.json says it is (postimp_key.py --check says the same for all)."""

import glob
import json
import os
import sys

import numpy as np
from PIL import Image

from office_room_kit import inside
from postimp_paints import SCENE_KEY
from postimp_plans import PLANS

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "..", "..", "art", "scenes")

BRIEF = {
    "office-room": {
        "marks": ["joe", "chair", "vent", "door", "dale", "merle", "opal", "intercom", "thermostat"],
        "things": ["door", "sign", "table", "questionnaire", "chair-joe", "chair-dale", "chair-merle", "chair-corner", "vent", "mirror", "plant",
                   "cooler", "cones", "clock", "thermostat", "intercom", "poster"],
        "seated": ["joe", "dale", "merle", "chair", "vent"],
    },
    "office-property": {
        "marks": ["opal", "vent", "counter", "banjo", "door"],
        "things": ["sandal", "oillamp", "cup", "horseshoe", "hat", "feather", "cassette", "gnome", "boxes", "banjo", "shelves-left", "shelves-right",
                   "window", "bell", "stamp", "knitting", "sign", "door", "vent"],
        "seated": ["opal", "vent", "counter"],
    },
}


def files_in(folder):
    return sorted(f[:-4] for f in os.listdir(folder) if f.endswith(".png"))


def check(scene):
    bad = []
    out = os.path.join(HERE, "out", scene)
    plan = PLANS.get(scene)
    if plan is None or scene not in SCENE_KEY:
        return [f"{scene}: no plan or no key"]
    named = {"back"} | set(plan["planes"]) | set(plan["alt"]) | set(plan["union"])
    frames = sorted({os.path.basename(f)[:-4] for pat in plan["frames"] for f in glob.glob(os.path.join(out, pat + ".png"))})
    have = files_in(out)
    for f in have:
        if f not in named and f not in frames:
            bad.append(f"{f}.png is not in the plan")
    for f in named:
        if f not in have:
            bad.append(f"{f}.png (in the plan) is missing")
    boxes = {}
    for f in sorted(named & set(have)):
        im = Image.open(os.path.join(out, f + ".png"))
        if im.size != (800, 600):
            bad.append(f"{f}.png is {im.size}, not 800x600")
        if f == "back":
            continue
        a = np.asarray(im.convert("RGBA"))[..., 3]
        if not (a > 0).any():
            bad.append(f"{f}.png is empty")
        soft = ((a > 0) & (a < 255)).sum()
        if soft:
            bad.append(f"{f}.png has {soft} half-clear pixels (a cut-out is hard-edged)")
        boxes[f] = Image.fromarray(a).getbbox()
    for alt, replaces in plan["alt"].items():
        for r in replaces:
            a, b = boxes.get(alt), boxes.get(r)
            if a and b and (a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1]):
                bad.append(f"{alt}.png does not lie where {r}.png does")
    sizes = {}
    for f in frames:
        sizes.setdefault(f.split("-")[0], set()).add(Image.open(os.path.join(out, f + ".png")).size)
    for k, v in sizes.items():
        if len(v) != 1:
            bad.append(f"the frames {k}-* are not all one size: {sorted(v)}")
    L = json.load(open(os.path.join(out, "layout.json")))
    B = BRIEF[scene]
    for k in B["marks"]:
        if k not in L["marks"]:
            bad.append(f"layout.json: no mark `{k}`")
    ids = {t["id"] for t in L["things"]}
    for k in B["things"]:
        if k not in ids:
            bad.append(f"layout.json: no thing `{k}`")
    files = {p["file"][:-4] for p in L["planes"]}
    for f in named - {"back"}:
        if f not in files:
            bad.append(f"layout.json: no plane for {f}.png")
    for t in L["things"]:
        sh = t["shape"]
        pts = sh["poly"] if "poly" in sh else [[sh["rect"][0], sh["rect"][1]], [sh["rect"][0] + sh["rect"][2], sh["rect"][1] + sh["rect"][3]]]
        if any(x < 0 or x > 800 or y < 0 or y > 600 for x, y in pts):
            bad.append(f"layout.json: the shape of {t['id']} goes outside the picture")
    walk = L["walk"]
    for k, s in L["stands"].items():
        if "grownup_px" not in s:
            bad.append(f"layout.json: the stand {k} has no grownup_px")
        if k not in B["seated"] and not inside(s["at"], walk):
            bad.append(f"layout.json: the stand {k} {s['at']} is outside the walk outline")
        if s.get("grownup_px", 0) > 205 and k not in B["seated"]:
            bad.append(f"layout.json: a grown-up at the stand {k} would be {s['grownup_px']} px tall")
    for x, y in walk:
        if x < 14 or x > 786 or y > 590:
            bad.append(f"layout.json: the walk outline comes to the picture's edge at {[x, y]}")
    # installed: the keyed copies the ledger names
    led = json.load(open(os.path.join(HERE, "postimp_keyed.json"))).get(scene)
    dst = os.path.join(ART, scene)
    if not os.path.isdir(dst):
        bad.append("not installed yet (python3 install.py " + scene + ")")
    elif led is None:
        bad.append("installed, but not in postimp_keyed.json")
    else:
        import hashlib
        for f in have:
            e = led["files"].get(f + ".png")
            p = os.path.join(dst, f + ".png")
            if e is None or not os.path.exists(p):
                bad.append(f"art/scenes/{scene}/{f}.png is not installed")
            elif hashlib.sha256(open(p, "rb").read()).hexdigest() != e["keyed"]:
                bad.append(f"art/scenes/{scene}/{f}.png is not the keyed copy")
            elif hashlib.sha256(open(os.path.join(out, f + ".png"), "rb").read()).hexdigest() != e["raw"]:
                bad.append(f"art/scenes/{scene}/{f}.png was keyed from another painting than out/'s")
        lj = os.path.join(dst, "layout.json")
        if not os.path.exists(lj) or open(lj).read() != open(os.path.join(out, "layout.json")).read():
            bad.append(f"art/scenes/{scene}/layout.json is not out/'s")
    print(f"{scene}: {len(have)} pictures ({len(frames)} frames), {len(L['things'])} things, {len(L['planes'])} planes, "
          f"{len(L['stands'])} stand places: " + ("all good" if not bad else f"{len(bad)} problems"))
    for b in bad:
        print("  -", b)
    return bad


if __name__ == "__main__":
    scenes = sys.argv[1:] or ["office-room", "office-property"]
    problems = sum(len(check(s)) for s in scenes)
    sys.exit(1 if problems else 0)

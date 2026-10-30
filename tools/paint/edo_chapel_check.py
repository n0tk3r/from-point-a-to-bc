"""The checks on the finished room under the storehouse (edo-chapel), and the pictures to look at. PAINT-20F.

    python3 edo_chapel_check.py [--installed] [--people PORT]

Checks (out/edo-chapel/, or art/scenes/edo-chapel/ with --installed): every picture 800 x 600, an 8-bit palette, a cut-out
hard-edged (no half-clear pixels); every file of the plan in postimp_plans.py present and every picture in the plan; every
state named in layout.json present; every mark inside the walk outline (a stand on the floor, `wall` a place on the wall);
every thing of ROUND-20's list for this scene with a shape; the alts covering what they replace (the open altar covers the
shut one, each trapdoor state the others, the ladder in the sun the ladder); the sun patch inside the day cut-out; the
people's heights at the marks (a grown-up 0.8 to 1.25 of full). It writes out/edo-chapel-check/layout.png (the picture
with every shape, mark, base line and the walk drawn over it). With --people PORT (the game served on that port, Playwright
installed) it stands stand-ins at every mark in every state, into out/edo-chapel-check/people-*.png."""

import glob
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import postimp_plans
import edo_chapel_model as M

INSTALLED = "--installed" in sys.argv
FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "art", "scenes", "edo-chapel") if INSTALLED else "out/edo-chapel"
CHECK = "out/edo-chapel-check"
# the things ROUND-20.md asks every painter to give a shape (edo-chapel), and the marks it names
THINGS = ["altar", "kannon", "calendar", "bowl", "mirror", "lamps", "wall", "ladder", "mats", "props", "trapdoor", "sei", "jinsuke", "orin"]
MARKS = ["ladder", "altar", "sei", "jinsuke", "orin", "sit", "wall", "sunpatch"]
problems = []


def bad(msg):
    problems.append(msg)
    print("  PROBLEM:", msg)


def inside(pt, poly):
    x, y = pt
    n, ok = len(poly), False
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < x0 + (x1 - x0) * (y - y0) / (y1 - y0):
            ok = not ok
    return ok


def alpha_of(name):
    im = Image.open(os.path.join(FOLDER, name + ".png"))
    return np.asarray(im.convert("RGBA"))[..., 3]


def main():
    os.makedirs(CHECK, exist_ok=True)
    L = json.load(open(os.path.join(FOLDER, "layout.json")))
    plan = postimp_plans.PLANS["edo-chapel"]
    files = sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(FOLDER, "*.png")))
    planned = set(["back"] + plan["planes"] + list(plan["alt"]) + sum(plan["states"].values(), []) if "states" in plan else ["back"] + plan["planes"] + list(plan["alt"]))
    print("files:", files)
    for f in files:
        im = Image.open(os.path.join(FOLDER, f + ".png"))
        if im.size != (800, 600):
            bad(f"{f}.png is {im.size}, not 800 x 600")
        if im.mode != "P":
            bad(f"{f}.png is {im.mode}, not an 8-bit palette")
        if f != "back":
            a = np.asarray(im.convert("RGBA"))[..., 3]
            soft = ((a > 0) & (a < 255)).sum()
            if soft:
                bad(f"{f}.png has {soft} half-clear pixels")
            if (a >= 128).sum() == 0:
                bad(f"{f}.png is empty")
        if f not in planned:
            bad(f"{f}.png is not in the plan")
    for f in planned:
        if f not in files:
            bad(f"the plan's {f}.png is missing")
    # every state named in layout.json
    for p in L["planes"]:
        for st, fn in (p.get("states") or {}).items():
            if fn[:-4] not in files:
                bad(f"plane {p['id']} state {st}: {fn} missing")
        if p.get("file") and p["file"][:-4] not in files:
            bad(f"plane {p['id']}: {p['file']} missing")
    # marks inside the walk
    walk = [tuple(q) for q in L["walk"]]
    for m in MARKS:
        if m not in L["marks"]:
            bad(f"mark {m} missing")
        elif m != "wall" and not inside(L["marks"][m], walk):
            bad(f"mark {m} at {L['marks'][m]} is outside the walk")
    for k, v in L["marks"].items():
        if k in ("wall", "fromLadder"):
            continue
        if not inside(v, walk):
            bad(f"mark {k} at {v} is outside the walk")
    for k, v in L["marks"]["fromLadder"].items():
        if not inside(v, walk):
            bad(f"fromLadder {k} at {v} is outside the walk")
    for k, v in L["stands"].items():
        if not (0.8 * 160 <= v["grownup_px"] <= 1.25 * 160):
            bad(f"stand {k}: a grown-up is {v['grownup_px']} px there (0.8 to 1.25 of 160 wanted)")
    # every thing of the list with a shape
    ids = {t["id"]: t for t in L["things"]}
    for t in THINGS:
        if t not in ids:
            bad(f"thing {t} missing")
        elif not ids[t].get("shape") or not (ids[t]["shape"].get("rect") or ids[t]["shape"].get("poly")):
            bad(f"thing {t} has no shape")
    # the alts cover what they replace
    def covers(a, b):
        A, B = alpha_of(a) >= 128, alpha_of(b) >= 128
        left = (B & ~A).sum()
        return left
    for a, b in (("altar-open", "altar-shut"), ("trapdoor-lamp", "trapdoor-shut"), ("trapdoor-day", "trapdoor-shut"), ("trapdoor-shut", "trapdoor-lamp"),
                 ("ladder-day", "ladder"), ("ladder", "ladder-day"), ("lamps-out", "lamps"), ("lamps", "lamps-out")):
        n = covers(a, b)
        if n > 40:
            bad(f"{a}.png leaves {n} pixels of {b}.png uncovered")
    # the sun patch lies inside the day cut-out
    sr = L["lights"]["sunpatch"]["rect"]
    A = alpha_of("trapdoor-day") >= 128
    share = A[sr[1]:sr[1] + sr[3], sr[0]:sr[0] + sr[2]].mean()
    if share < 0.55:
        bad(f"only {share:.0%} of the sun patch's rect is in trapdoor-day.png (the ladder's shadow is a hole in it: that is right; under 55% is not)")
    ys, xs = np.nonzero(A)
    print("trapdoor-day box:", [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)], "pixels", int(A.sum()))
    # the layout picture
    im = Image.open(os.path.join(FOLDER, "back.png")).convert("RGBA")
    for n in plan["planes"]:
        im.alpha_composite(Image.open(os.path.join(FOLDER, n + ".png")).convert("RGBA"))
    d = ImageDraw.Draw(im)
    d.polygon([tuple(q) for q in L["walk"]], outline=(60, 255, 60))
    d.line([(0, L["horizon"]), (800, L["horizon"])], fill=(255, 80, 80))
    d.line([(0, L["full"]), (800, L["full"])], fill=(255, 160, 80))
    for t in L["things"]:
        sh = t["shape"]
        if sh.get("rect"):
            x, y, w, h = sh["rect"]
            d.rectangle([x, y, x + w, y + h], outline=(255, 230, 60))
            d.text((x + 2, y + 2), t["id"], fill=(255, 230, 60))
        else:
            d.polygon([tuple(q) for q in sh["poly"]], outline=(255, 230, 60))
    for p in L["planes"]:
        if isinstance(p.get("base"), list):
            d.line([tuple(q) for q in p["base"]], fill=(80, 200, 255), width=2)
    for k, v in L["marks"].items():
        if k == "fromLadder":
            for kk, vv in v.items():
                d.ellipse([vv[0] - 4, vv[1] - 4, vv[0] + 4, vv[1] + 4], outline=(255, 120, 255))
                d.text((vv[0] + 5, vv[1] - 5), kk, fill=(255, 120, 255))
            continue
        d.ellipse([v[0] - 4, v[1] - 4, v[0] + 4, v[1] + 4], outline=(255, 255, 255))
        d.text((v[0] + 5, v[1] - 5), k, fill=(255, 255, 255))
    d.polygon([tuple(q) for q in L["lights"]["hatch"]], outline=(120, 220, 255))
    d.rectangle([sr[0], sr[1], sr[0] + sr[2], sr[1] + sr[3]], outline=(200, 240, 255))
    wp = L["lights"]["wall"]["patch"]
    r = L["lights"]["wall"]["patch_px"] // 2
    d.ellipse([wp[0] - r, wp[1] - r, wp[0] + r, wp[1] + r], outline=(255, 255, 200))
    for f in L["fx"]:
        d.ellipse([f["at"][0] - 3, f["at"][1] - 3, f["at"][0] + 3, f["at"][1] + 3], fill=(255, 200, 60))
    im.convert("RGB").save(f"{CHECK}/layout.png")
    print("wrote", f"{CHECK}/layout.png")
    # the people, at every mark, in every state
    if "--people" in sys.argv:
        port = sys.argv[sys.argv.index("--people") + 1]
        people(L, port)
    print("problems:", len(problems))
    return 1 if problems else 0


def people(L, port):
    src = open("people_on.py").read().replace("http://localhost:8765/", f"http://localhost:{port}/")
    open(f"{CHECK}/people_on_port.py", "w").write(src)
    st = {k: v["at"] for k, v in L["stands"].items()}
    # stand-ins by height: lampboy 1.40 (Sei), phyllis 1.54 (Jinsuke), lilsis 1.22 (O-Rin, a hand taller)
    sets = {
        "shut-arrival": (["back", "props", "trapdoor-shut", "altar-shut", "mirror", "lamps", "ladder"],
                         [("mom", "mom", 0), ("bigsis", "bigsis", 0), ("lilsis", "lilsis", 0), ("lampboy", "sei", 0), ("phyllis", "jinsuke", 0), ("lilsis", "orin", 0)]),
        "open-talk": (["back", "props", "trapdoor-lamp", "altar-open", "mirror", "lamps", "ladder"],
                      [("mom", "altar", 180), ("bigsis", "sit3", 0), ("lilsis", "sit1", 0), ("lampboy", "sei", 0), ("phyllis", "jinsuke", 270), ("lilsis", "orin", 0)]),
        "day-mirror": (["back", "props", "trapdoor-day", "altar-open", "lamps", "ladder-day"],
                       [("lampboy", "sunpatch", 180), ("mom", "atwall", 90), ("bigsis", "sit2", 0), ("lilsis", "ladder", 270), ("phyllis", "atmirror", 0)]),
        "lamps-out": (["back", "props", "trapdoor-lamp", "altar-shut", "mirror", "lamps-out", "ladder"],
                      [("mom", "ladder", 0), ("bigsis", "front", 0), ("lilsis", "atlamp", 90)]),
    }
    for label, (names, who) in sets.items():
        im = Image.open(os.path.join(FOLDER, names[0] + ".png")).convert("RGBA")
        for n in names[1:]:
            im.alpha_composite(Image.open(os.path.join(FOLDER, n + ".png")).convert("RGBA"))
        im.convert("RGB").save(f"{CHECK}/nofront.png")
        folk = ";".join(f"{w}|{st[at][0]}|{st[at][1]}|{yaw}" for w, at, yaw in who)
        out = f"{CHECK}/people-{label}.png"
        r = subprocess.run([sys.executable, f"{CHECK}/people_on_port.py", f"{CHECK}/nofront.png", str(L["horizon"]), str(L["full"]), folk, out,
                            os.path.join(FOLDER, "front.png")], capture_output=True, text=True)
        print(r.stdout.strip(), r.stderr.strip()[-200:])
        # a stand-in for the mirror's patch on the wall (the engine draws the real one): a pale disc with a faint cross
        if label == "day-mirror":
            im2 = Image.open(out).convert("RGBA")
            d = ImageDraw.Draw(im2, "RGBA")
            wp, r_ = L["lights"]["wall"]["patch"], L["lights"]["wall"]["patch_px"] // 2
            d.ellipse([wp[0] - r_, wp[1] - r_, wp[0] + r_, wp[1] + r_], fill=(246, 238, 216, 200))
            d.line([(wp[0], wp[1] - r_ * 0.6), (wp[0], wp[1] + r_ * 0.6)], fill=(200, 190, 160, 170), width=2)
            d.line([(wp[0] - r_ * 0.45, wp[1] - r_ * 0.15), (wp[0] + r_ * 0.45, wp[1] - r_ * 0.15)], fill=(200, 190, 160, 170), width=2)
            im2.convert("RGB").save(out)
    os.remove(f"{CHECK}/nofront.png")


if __name__ == "__main__":
    sys.exit(main())

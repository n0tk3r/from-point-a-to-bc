"""Checks on the Office's lot (OFFICE-17A), and the pictures to look at.

    python3 office_lot_check.py               the checks on out/office-lot/ (as painted), and out/office-lot-check.png
                                              (layout.json drawn over the composite: the two floors, what is blocked,
                                              every base, every thing's shape, every mark, the climb)
    python3 office_lot_check.py installed     the same on the installed (keyed) pictures, art/scenes/office-lot/
    python3 office_lot_check.py people [dir]  the game's own figures standing in it, at the size the game draws them
                                              (Ranger from his painted frames, in the shades; the suits, Jed and
                                              Grandpa Joe drawn by the game's rig through tools/sprites.html, which this
                                              painter's copy of the game must be serving on port 8877:
                                              cd ../.. && python3 tools/serve.py 8877); into dir (default out/office-lot-people)

The checks: every file is in the scene's plan (postimp_plans.py) and every file of the plan is there; every full picture
is 800 x 600, every cut-out and state hard-edged; every state of every cut-out is painted; each frame set's frames are one
size; every mark of Ranger's is inside its floor (the gravel's marks in the gravel, the roof's on the roof), clear of what
is blocked; the climb's ends are on their floors; every thing's shape is on the picture; the walk areas are inside the
picture; the limousine's door, the switch's handle and the wing nuts are where layout.json says."""

import asyncio
import base64
import glob
import io
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "office-lot")
ART = os.path.join(HERE, "..", "..", "art", "scenes", "office-lot")
RANGER = os.path.join(HERE, "..", "..", "art", "scenes", "nevada-roadside")
PORT = 8877


def inside(poly, p):
    x, y = p
    n, c = len(poly), False
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1:
            c = not c
    return c


def check(folder):
    sys.path.insert(0, HERE)
    from postimp_plans import PLANS
    plan = PLANS["office-lot"]
    L = json.load(open(os.path.join(folder, "layout.json")))
    problems = []
    files = sorted(f[:-4] for f in os.listdir(folder) if f.endswith(".png"))
    named = {"back"} | set(plan["planes"]) | set(plan["alt"])
    frames = sorted({os.path.basename(f)[:-4] for pat in plan["frames"] for f in glob.glob(os.path.join(folder, pat + ".png"))})
    unknown = [f for f in files if f not in named and f not in frames]
    missing = [f for f in named if f not in files]
    if unknown:
        problems.append(f"not in the plan: {unknown}")
    if missing:
        problems.append(f"in the plan but not painted: {missing}")
    for f in sorted(named & set(files)):
        im = Image.open(os.path.join(folder, f + ".png"))
        if im.size != (800, 600):
            problems.append(f"{f}: {im.size}, not 800 x 600")
        a = np.asarray(im.convert("RGBA"))[..., 3]
        if f != "back" and ((a > 0) & (a < 255)).any():
            problems.append(f"{f}: half-clear pixels")
        if f != "back" and not (a > 0).any():
            problems.append(f"{f}: empty")
    for group in ("fan", "pennant"):
        sizes = {Image.open(os.path.join(folder, f + ".png")).size for f in frames if f.startswith(group + "-")}
        if len(sizes) != 1:
            problems.append(f"{group} frames: sizes {sizes}")
    # every state of every cut-out is painted
    for st in ("trash", "trash-tipped", "trash-pipe", "grille", "grille-off", "switch", "switch-off", "door", "door-open", "limo", "limo-door-open",
               "nut-1", "nut-2", "nut-3", "nut-4", "awning", "flagpole", "front"):
        if st not in files:
            problems.append(f"state {st} is not painted")
    # the floors and the marks
    ground, roof = L["walk_areas"]["ground"]["poly"], L["walk_areas"]["roof"]["poly"]
    for poly, name in ((ground, "ground"), (roof, "roof")):
        for x, y in poly:
            if not (0 <= x <= 800 and 0 <= y <= 600):
                problems.append(f"walk area {name}: point {x, y} off the picture")
    blocked = L["blocked"]
    on_roof = ("roof", "intake", "switch")
    for name, p in L["marks"].items():
        pts = p if isinstance(p, list) and isinstance(p[0], list) else ([v for v in p.values()] if isinstance(p, dict) else [p])
        for q in pts:
            if name in ("jedFrom",):
                continue
            floor = roof if name in on_roof else ground
            if name == "inDoor":
                continue
            if not inside(floor, q):
                problems.append(f"mark {name} {q}: not on its floor ({'roof' if name in on_roof else 'ground'})")
            for b in blocked:
                if inside(b, q):
                    problems.append(f"mark {name} {q}: on blocked ground")
    c = L["climb"]
    if not inside(ground, c[0]["at"]):
        problems.append("the climb does not start on the gravel")
    if not inside(roof, c[-1]["at"]):
        problems.append("the climb does not end on the roof")
    for t in L["things"]:
        sh = t["shape"].get("poly") or []
        for x, y in sh:
            if not (-1 <= x <= 801 and -1 <= y <= 601):
                problems.append(f"thing {t['id']}: shape off the picture at {x, y}")
        if len(sh) > 24:
            problems.append(f"thing {t['id']}: {len(sh)} points")
    # the measured places agree with the pictures: each wing nut's middle is painted in its cut-out; the switch's handle,
    # up and down, is on its lever in switch.png and switch-off.png; the limousine's door (where its leaf differs between
    # limo.png and limo-door-open.png) lies between the opening's columns and the free edge; the two sills
    def alpha(name):
        return np.asarray(Image.open(os.path.join(folder, name + ".png")).convert("RGBA"))[..., 3] > 0

    def near(a, p, r=2):
        x, y = int(round(p[0])), int(round(p[1]))
        return a[max(0, y - r):y + r + 1, max(0, x - r):x + r + 1].any()
    for n in L["nuts"]:
        if not near(alpha(n["id"]), n["at"], 1):
            problems.append(f"{n['id']}: its middle {n['at']} is not on its picture")
    if not near(alpha("switch"), L["switch"]["handle_on"]) or not near(alpha("switch-off"), L["switch"]["handle_off"]):
        problems.append("the switch's handle is not where layout.json says")
    shut = np.asarray(Image.open(os.path.join(folder, "limo.png")).convert("RGBA")).astype(int)
    opened = np.asarray(Image.open(os.path.join(folder, "limo-door-open.png")).convert("RGBA")).astype(int)
    # (the two are finished with palettes of their own, so single pixels differ all along the car: a column has changed
    # where six or more of its pixels have)
    xs = np.nonzero((np.abs(shut - opened).sum(axis=2) > 60).sum(axis=0) >= 6)[0]
    door = L["limo"]["door"]
    lo, hi = min(door["opening"][0], door["free"][0]) - 3, max(door["opening"][1], door["hinge"][0]) + 3
    if len(xs) == 0 or xs.min() < lo or xs.max() > hi:
        problems.append(f"the limousine's door changes outside its columns {lo}..{hi}: {xs.min() if len(xs) else None}..{xs.max() if len(xs) else None}")
    sx = L["limo"]["sill"]["at"][0]
    if not (door["opening"][0] <= sx <= door["opening"][1]):
        problems.append("the limousine's sill is not in its door's opening")
    op = L["intake"]["opening"]
    if not inside(op, [L["intake"]["sill"][0], L["intake"]["sill"][1] - 1]):
        problems.append("the intake's sill is not at its opening")
    print("office-lot:", "all good" if not problems else "")
    for p_ in problems:
        print("  PROBLEM:", p_)
    return L, problems


def comp(folder, L, state="first"):
    """The composite as the game lays it with nobody there (or later: everything changed)."""
    show = {"first": ["grille", "nut-1", "nut-2", "nut-3", "nut-4", "switch", "door", "awning", "trash", "flagpole", "limo", "front"],
            "later": ["grille-off", "switch-off", "door-open", "awning", "trash-pipe", "flagpole", "limo-door-open", "front"],
            "tipped": ["grille", "nut-1", "nut-2", "nut-3", "nut-4", "switch", "door", "awning", "trash-tipped", "flagpole", "limo-door-open", "front"]}[state]
    im = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    fx = {f["id"]: f for f in L["fx"]}

    def put(f, at=None, foot=None):
        top = Image.open(os.path.join(folder, f)).convert("RGBA")
        im.alpha_composite(top, (0, 0) if at is None else (int(at[0] - foot[0]), int(at[1] - foot[1])))
    if state != "later":
        put(fx["fan"]["frames"][0], fx["fan"]["at"], fx["fan"]["foot"])
    for n in show:
        if n == "front":
            continue
        put(n + ".png")
        if n == "flagpole":
            put(fx["pennant"]["frames"][0], fx["pennant"]["at"], fx["pennant"]["foot"])
    return im


def draw_layout(im, L, path):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.polygon([tuple(p) for p in L["walk_areas"]["ground"]["poly"]], outline=(60, 220, 90, 255), fill=(60, 220, 90, 40))
    d.polygon([tuple(p) for p in L["walk_areas"]["roof"]["poly"]], outline=(60, 160, 255, 255), fill=(60, 160, 255, 60))
    for b in L["blocked"]:
        d.polygon([tuple(p) for p in b], outline=(255, 60, 60, 255), fill=(255, 60, 60, 70))
    for p in L["planes"]:
        if isinstance(p.get("base"), (int, float)) and not p.get("alt"):
            d.line([0, p["base"], 800, p["base"]], fill=(255, 150, 0, 90))
        if p.get("solid") and not p.get("alt"):
            d.polygon([tuple(q) for q in p["solid"]], outline=(255, 90, 90, 220))
    for t in L["things"]:
        sh = t["shape"].get("poly")
        if sh:
            d.polygon([tuple(q) for q in sh], outline=(255, 255, 0, 200))
    for name, p in L["marks"].items():
        pts = p if isinstance(p, list) and isinstance(p[0], list) else ([v for v in p.values()] if isinstance(p, dict) else [p])
        for q in pts:
            x, y = q
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 0, 200, 255))
        if not isinstance(p, dict) and not (isinstance(p, list) and isinstance(p[0], list)):
            d.text((p[0] + 4, p[1] - 10), name, fill=(255, 255, 255, 255))
    pts = [tuple(c["at"]) for c in L["climb"]]
    d.line(pts, fill=(0, 255, 255, 255), width=1)
    im = im.copy()
    im.alpha_composite(ov)
    im.convert("RGB").save(path)


# ---------------------------------------------------------------- the game's people standing in it
async def _figures(folk, hz, full):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 900, "height": 700})
        page.on("pageerror", lambda e: print("[pageerror]", e))
        await page.goto(f"http://localhost:{PORT}/tools/sprites.html")
        await page.wait_for_timeout(1500)
        res = await page.evaluate("""([folk, hz, full]) => {
            const L = window.lab; const figs = [];
            for (const [sid, pose, yaw, x, y, f] of folk) {
              try {
                const spec = L.people[sid]; if (!spec) { figs.push({ err: 'nobody called ' + sid }); continue; }
                const px = Math.round(L.BASE * spec.height * (y - hz) / (f - hz));
                const stand = (q) => L.poses.stand(spec, q), walk = (ph) => L.poses.walk(spec, ph);
                const sf = L.drawFigure(spec, eval('(' + pose + ')'), +yaw, px); const cv = sf.toCanvas();
                figs.push({ url: cv.toDataURL(), ox: sf.ox, oy: sf.oy, x, y, px, who: sid });
              } catch (e) { figs.push({ err: String(e) }); }
            }
            return figs; }""", [folk, hz, full])
        await b.close()
    return res


def figures(folk, hz, full):
    """folk: [(who, x, y, yaw[, pose])] -> [(image, left, top, y)] drawn by the game's own rig."""
    F = [[f[0], f[4] if len(f) > 4 else "stand(0)", float(f[3]), float(f[1]), float(f[2]), float(full)] for f in folk]
    res = asyncio.run(_figures(F, hz, full))
    out = []
    for f in res:
        if "err" in f:
            print("skipped:", f["err"])
            continue
        im = Image.open(io.BytesIO(base64.b64decode(f["url"].split(",")[1]))).convert("RGBA")
        out.append((im, int(round(f["x"] - f["ox"])), int(round(f["y"] - f["oy"])), f["y"], f["who"], f["px"]))
    return out


def ranger(set_, i, at, scale, face="E", shades=True):
    """Ranger's painted frame, sized as the engine sizes him (nearest neighbour, in steps of two pixels), its foot on at."""
    side = json.load(open(os.path.join(RANGER, "ranger.json")))
    name = side["frames"][set_][i]
    if shades:
        name = name.replace("ranger-", "ranger-shades-", 1)
    im = Image.open(os.path.join(RANGER, name)).convert("RGBA")
    if face == "W":
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    tall = side["tall"].get(set_, side["tall"]["stand"])
    h_px = max(4, round(tall * scale / 2) * 2)
    k = h_px / tall
    w, h = im.size
    small = im.resize((max(1, round(w * k)), max(1, round(h * k))), Image.NEAREST)
    fx, fy = side["foot"]
    if face == "W":
        fx = w - 1 - fx
    return small, int(round(at[0] - fx * k)), int(round(at[1] - fy * k))


def people(folder, outdir):
    L = json.load(open(os.path.join(folder, "layout.json")))
    os.makedirs(outdir, exist_ok=True)
    m = L["marks"]
    hz, full = L["horizon"], L["full"]
    roof_full = L["walk_areas"]["roof"]["full"]

    def scale_ground(y):
        return (y - hz) / (full - hz)

    def scale_roof(y):
        return (y - hz) / (roof_full - hz)

    def save(im, rangers, folk, front, name):
        im = im.copy()
        items = [(f[3], "fig", f) for f in folk] + [(r[3], "ranger", r) for r in rangers]
        for _, kind, it in sorted(items, key=lambda t: t[0]):
            if kind == "fig":
                im.alpha_composite(it[0], (it[1], it[2]))
            else:
                sm, x, y, _ = it
                im.alpha_composite(sm, (x, y))
        for f in front:
            im.alpha_composite(Image.open(os.path.join(folder, f)).convert("RGBA"))
        im.convert("RGB").save(os.path.join(outdir, name))
        print(os.path.join(outdir, name))

    def rg(set_, i, at, s, face="E"):
        sm, x, y = ranger(set_, i, at, s, face)
        return (sm, x, y, at[1])
    first = comp(folder, L, "first")
    # 1. Ranger at every mark of his, at his size (the roof's by the roof's floor), and the climb
    rangers = [rg("sit", 0, m["fromLimo"], scale_ground(m["fromLimo"][1]), "W"),
               rg("stand", 0, m["trash"], scale_ground(m["trash"][1]), "E"),
               rg("stand", 0, m["pipe"], scale_ground(m["pipe"][1]), "E"),
               rg("stand", 0, m["roof"], scale_roof(m["roof"][1]), "W"),
               rg("sit", 0, m["intake"], scale_roof(m["intake"][1]), "E"),
               rg("pull", 0, m["switch"], scale_roof(m["switch"][1]), "E")]
    save(comp(folder, L, "later"), [rg("sit", 0, m["fromLimo"], scale_ground(m["fromLimo"][1]), "W")], [], ["front.png"], "ranger-fromlimo.png")
    save(first, rangers, [], ["front.png"], "ranger-marks.png")
    c = L["climb"]
    climbers = [rg("stand", 0, c[0]["at"], c[0]["scale"], "E"), rg("sit", 0, c[1]["at"], c[1]["scale"], "E"),
                rg("climb", 0, c[2]["at"], c[2]["scale"], "E"), rg("climb", 2, [c[2]["at"][0], (c[2]["at"][1] + c[3]["at"][1]) / 2], c[2]["scale"], "E"),
                rg("climb", 1, c[3]["at"], c[3]["scale"], "E"), rg("stand", 0, c[4]["at"], c[4]["scale"], "W")]
    later = comp(folder, L, "later")
    # (on the climb he is in front of the can: lay him after it, as the scene must)
    save(later, [], [], [], "_tmp.png")
    im = later.copy()
    for sm, x, y, _ in climbers:
        im.alpha_composite(sm, (x, y))
    im.alpha_composite(Image.open(os.path.join(folder, "front.png")).convert("RGBA"))
    im.convert("RGB").save(os.path.join(outdir, "ranger-climb.png"))
    os.remove(os.path.join(outdir, "_tmp.png"))
    print(os.path.join(outdir, "ranger-climb.png"))
    # the switch close: Ranger's pull frames at the switch, on and off
    for state, i in (("on", 0), ("off", 1)):
        im = comp(folder, L, "first" if state == "on" else "later").copy()
        sm, x, y, _ = rg("pull", i, m["switch"], scale_roof(m["switch"][1]), "E")
        im.alpha_composite(sm, (x, y))
        im.crop((300, 160, 460, 260)).resize((640, 400), Image.NEAREST).convert("RGB").save(os.path.join(outdir, f"ranger-switch-{state}.png"))
    # the tipped can, Ranger in its mouth
    im = comp(folder, L, "tipped").copy()
    mouth = L["cans"]["tipped"]["mouth"]
    sm, x, y, _ = rg("sit", 0, [mouth[0] - 2, mouth[1] + 6], scale_ground(mouth[1] + 6), "E")
    im.alpha_composite(sm, (x, y))
    im.convert("RGB").save(os.path.join(outdir, "ranger-tipped.png"))
    # 2. the arrival: the suits at the car and walking in, Grandpa Joe out of the back, Jed; Wendell at the door
    folk = [("grandpajoe-tied", *m["limoDoor"], 180), ("suit1", *m["dale"], 90), ("suit2", *m["merle"], 270),
            ("suit3", *m["outOfCar"][2], 0), ("suit4", *m["outOfCar"][3], 0), ("agent", 760, 420, 270)]
    save(comp(folder, L, "later"), [rg("sit", 0, m["fromLimo"], scale_ground(m["fromLimo"][1]), "W")], figures(folk, hz, full), ["front.png"], "arrival.png")
    q = m["queue"]
    folk = [("agent", *q["jed"], 180), ("suit1", *q["dale"], 180), ("grandpajoe-tied", *q["joe"], 180), ("suit2", *q["merle"], 180),
            ("suit4", *q["floyd"], 200), ("suit3", *m["door"], 270)]
    save(comp(folder, L, "first"), [], figures(folk, hz, full), ["front.png"], "suits-at-door.png")
    folk = [("suit3", *m["door"], 270)]
    save(first, rangers[:3], figures(folk, hz, full), ["front.png"], "wendell-and-ranger.png")
    # 3. people at the front, the middle and the back of the gravel, for size
    folk = [("suit1", 120, 590, 0), ("suit2", 300, 520, 0), ("grandpajoe-standing", 520, 470, 0), ("suit3", 700, 420, 0), ("agent", 60, 430, 0)]
    save(first, [rg("stand", 0, [400, 560], scale_ground(560), "E")], figures(folk, hz, full), ["front.png"], "sizes.png")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "people":
        people(OUT if len(args) < 2 or args[1] != "installed" else ART, os.path.join(HERE, "out", "office-lot-people"))
        sys.exit()
    folder = ART if args and args[0] == "installed" else OUT
    L, problems = check(folder)
    for state in ("first", "later", "tipped"):
        draw_layout(comp(folder, L, state), L, os.path.join(HERE, "out", f"office-lot-check-{state}{'-installed' if folder == ART else ''}.png"))
    sys.exit(1 if problems else 0)

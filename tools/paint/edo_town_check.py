"""Checks on Himeji town as painted (out/edo-town/) or as installed (art/scenes/edo-town/), and the pictures to look at.
PAINT-21E. (edo_shosha_check.py and edo_lock_check.py use its tools.)

  python3 edo_town_check.py [out|art] [shots_dir]
      the sizes (800 x 600, every file of the plan, nothing not in it), the cut-outs hard-edged, the school's opening
      clear, every mark inside its floor, every thing of ROUND-21.md's list with a shape, the stands' sizes; then writes
      <shots_dir>/town-layout-<which>.png (the layout drawn over the picture) and, with the game served on port 8935 and
      Playwright, <shots_dir>/town-people-<which>.png (the game's own figures standing at the marks: the three of them in
      the street, Mom at the well and at the kitchen door, Little Sister at a desk; O-Tane, O-Kiku, the girls, the
      teacher and Tobei stood in by round twenty's people at their heights)."""

import asyncio
import base64
import fnmatch
import io
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8935
NEEDED = ["keep", "roofs", "cottonoffice", "noteoffice", "bales", "house", "passage", "well", "bucket", "ricepot", "saltjar", "pickletub", "plumjar",
          "cloth", "pan", "mortar", "school", "desks", "gate", "hut", "hutsandals", "sweets", "clappers", "highway", "tane", "kiku", "shizu", "pupil1",
          "pupil2", "tobei"]
MARKS = ["east", "house", "well", "kitchen", "tane", "school", "kiku", "desk", "shizu", "gate", "tobei", "cotton", "north"]


def inside(poly, x, y):
    n = len(poly)
    c = False
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0 + 1e-9) + x0:
            c = not c
    return c


def check_files(scene, folder):
    """Every file of the plan there and nothing else; sizes; hard edges."""
    import postimp_plans as PP
    plan = PP.PLANS[scene]
    bad = []
    files = sorted(f for f in os.listdir(folder) if f.endswith(".png"))
    named = {"back"} | set(plan["planes"]) | set(plan["alt"]) | {n for v in plan.get("states", {}).values() for n in v}
    for f in files:
        name = f[:-4]
        ok = name in named or any(fnmatch.fnmatch(name, p) for p in plan["frames"])
        if not ok:
            bad.append(f"{f}: not in the plan")
        if name in named:
            im = Image.open(os.path.join(folder, f))
            if im.size != (800, 600):
                bad.append(f"{f}: {im.size}")
            if name != "back":
                a = np.asarray(im.convert("RGBA"))[..., 3]
                if ((a > 0) & (a < 255)).any():
                    bad.append(f"{f}: soft alpha")
                if a.max() == 0:
                    bad.append(f"{f}: empty")
    for name in named:
        if f"{name}.png" not in files:
            bad.append(f"{name}.png missing")
    return bad


def check_layout(lay, needed, marks):
    bad = []
    floors = {f["name"]: f for f in lay.get("floors", [])} or {"street": {"area": lay["walk"]}}
    for m in marks:
        if m not in lay["marks"]:
            bad.append(f"mark {m} missing")
    for m, v in lay["marks"].items():
        if isinstance(v[0], list):
            continue
        fl = lay["stands"].get(m, {}).get("floor", "street")
        area = floors[fl]["area"] if fl in floors else lay["walk"]
        if not inside(area, *v):
            bad.append(f"mark {m} {v} outside its floor ({fl})")
        for b in lay.get("blocked", []):
            if inside(b, *v):
                bad.append(f"mark {m} {v} on blocked ground")
    ids = {t["id"] for t in lay["things"]}
    for t in needed:
        if t not in ids:
            bad.append(f"thing {t} has no shape")
    for t in lay["things"]:
        if len(t["shape"]["poly"]) < 3:
            bad.append(f"thing {t['id']}: shape too small")
        xs = [p[0] for p in t["shape"]["poly"]]
        ys = [p[1] for p in t["shape"]["poly"]]
        if (max(xs) - min(xs)) < 8 or (max(ys) - min(ys)) < 8:
            bad.append(f"thing {t['id']}: shape under 8 px ({max(xs) - min(xs)} x {max(ys) - min(ys)})")
    for k, st in lay["stands"].items():
        if st.get("floor", "street") == "street":
            want = int(round(160 * (st["at"][1] - lay["horizon"]) / (lay["full"] - lay["horizon"])))
            if abs(want - st["grownup_px"]) > 1:
                bad.append(f"stand {k}: {st['grownup_px']} px, the camera says {want}")
    return bad


def check(folder):
    bad = check_files("edo-town", folder)
    lay = json.load(open(os.path.join(folder, "layout.json")))
    bad += check_layout(lay, NEEDED, MARKS)
    # the school's opening clear in shutters.png (the room shows through)
    a = np.asarray(Image.open(os.path.join(folder, "shutters.png")).convert("RGBA"))[..., 3]
    if a[358:424, 246:364].max() > 0:
        bad.append("shutters.png: the school's opening is not clear")
    return bad, lay


def composite(scene, folder, extra=(), without=()):
    import postimp_plans as PP
    im = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    for name in PP.PLANS[scene]["planes"]:
        if name in without:
            continue
        im.alpha_composite(Image.open(os.path.join(folder, name + ".png")).convert("RGBA"))
    for name in extra:
        im.alpha_composite(Image.open(os.path.join(folder, name + ".png")).convert("RGBA"))
    return im


def layout_picture(scene, folder, lay, path, extra=(), without=()):
    im = composite(scene, folder, extra, without)
    d = ImageDraw.Draw(im, "RGBA")
    for fl in lay.get("floors", [{"area": lay["walk"]}]):
        d.polygon([tuple(p) for p in fl["area"]], outline=(0, 255, 0, 255))
    for b in lay.get("blocked", []):
        d.polygon([tuple(p) for p in b], outline=(255, 0, 0, 255))
    for t in lay["things"]:
        d.polygon([tuple(p) for p in t["shape"]["poly"]], outline=(255, 200, 0, 170))
    for pl in lay.get("planes", []):
        if isinstance(pl.get("base"), (int, float)):
            d.line([(0, pl["base"]), (800, pl["base"])], fill=(0, 200, 255, 70))
    for k, v in lay["marks"].items():
        pts = v if isinstance(v[0], list) else [v]
        for x, y in pts:
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 0, 255, 255))
        x, y = pts[0]
        d.text((x + 5, y - 10), k, fill=(255, 255, 255, 255))
    im.convert("RGB").save(path)


async def figures(folk, hz, full, port=PORT):
    """The game's own figures (tools/sprites.html's rig): [(who, x, y, yaw, height_cm or 0, scale or 0, sort_row or 0, pose)]"""
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 900, "height": 700})
        page.on("pageerror", lambda e: print("[pageerror]", e))
        await page.goto(f"http://localhost:{port}/tools/sprites.html")
        await page.wait_for_timeout(1200)
        res = await page.evaluate("""([folk, hz, full]) => {
            const L = window.lab; const figs = [];
            for (const [sid, x, y, yaw, cm, sc, sortRow, pose] of folk) {
              try {
                const spec = L.people[sid]; if (!spec) { figs.push({ err: 'nobody called ' + sid }); continue; }
                const h = cm ? cm / 181 : spec.height;
                const k = sc ? sc : (y - hz) / (full - hz);
                const px = Math.round(L.BASE * h * k);
                const P = (L.poses[pose || 'stand'] || L.poses.stand)(spec, 0);
                const sf = L.drawFigure(spec, P, +yaw, px); const cv = sf.toCanvas();
                figs.push({ url: cv.toDataURL(), ox: sf.ox, oy: sf.oy, x, y, px, sort: sortRow || y, who: sid });
              } catch (e) { figs.push({ err: sid + ': ' + String(e) }); }
            }
            return figs; }""", [folk, hz, full])
        await b.close()
    return res


def people_picture(scene, folder, lay, folk, path, extra=(), without=(), planes_base=None):
    """Stand the figures in the composed picture, sorted with the cut-outs by their bases (as the engine does)."""
    import postimp_plans as PP
    res = asyncio.run(figures(folk, lay["horizon"], lay["full"]))
    for f in res:
        if "err" in f:
            print("skipped:", f["err"])
    figs = [f for f in res if "err" not in f]
    im = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    bases = planes_base or {pl["id"]: pl.get("base", -1 if pl.get("plane") == "back" else 10000) for pl in lay.get("planes", [])}
    names = [n for n in PP.PLANS[scene]["planes"] if n not in without] + list(extra)
    files = {}
    for pl in lay.get("planes", []):
        files[pl["id"]] = pl["id"]
    layers = []
    for n in names:
        base_id = n
        for pl in lay.get("planes", []):
            if n in (pl.get("states") or {}).values() or n + ".png" in (pl.get("states") or {}).values():
                base_id = pl["id"]
        layers.append((bases.get(base_id, bases.get(n, -1)), n))
    order = sorted([(b, 0, n) for b, n in layers] + [(f["sort"], 1, f) for f in figs], key=lambda t: (t[0], t[1]))
    for b, kind, what in order:
        if kind == 0:
            im.alpha_composite(Image.open(os.path.join(folder, what + ".png")).convert("RGBA"))
        else:
            fig = Image.open(io.BytesIO(base64.b64decode(what["url"].split(",")[1]))).convert("RGBA")
            im.alpha_composite(fig, (int(round(what["x"] - what["ox"])), int(round(what["y"] - what["oy"]))))
    im.convert("RGB").save(path)
    print(path, [(f["who"], f["px"]) for f in figs])


def town_folk(lay):
    M = lay["marks"]
    sc = lay["stands"]["desk"]["scale"]
    return [
        ("mom-edo", M["house"][0] - 8, M["house"][1] + 2, 0, 0, 0, 0, "stand"), ("bigsis-edo", M["school"][0] + 14, M["school"][1] + 4, 180, 0, 0, 0, "stand"),
        ("lilsis-edo", M["kiku"][0] - 16, M["kiku"][1] + 1, 90, 0, 0, 0, "stand"),
        ("orin", M["kiku"][0] + 6, M["kiku"][1], 270, 115, 0, 0, "stand"),                # O-Kiku, 1.15 m
        ("tami", M["tane"][0], M["tane"][1], 0, 146, 0, 0, "stand"),                      # O-Tane, 1.46 m
        ("mom-edo", M["well"][0], M["well"][1], 180, 0, 0, 0, "stand"),                    # Mom at the well (a second Mom: the look of it)
        ("mom-edo", M["kitchen"][0], M["kitchen"][1], 180, 0, 0, 0, "stand"),              # and at the kitchen door
        ("lilsis-edo", M["desk"][0], M["desk"][1], 0, 0, sc, 0, "kneel"),
        ("orin", M["pupil1"][0], M["pupil1"][1], 0, 118, sc, 0, "kneel"),
        ("orin", M["pupil2"][0], M["pupil2"][1], 0, 118, sc, 0, "kneel"),
        ("masa", M["shizu"][0], M["shizu"][1], 270, 146, sc, 0, "kneel"),                 # O-Shizu
        ("kihei", M["tobei"][0], M["tobei"][1], 0, 156, 0, 0, "sit"),                     # Tobei on his stool
        ("bigsis-edo", M["gate"][0] - 30, M["gate"][1] + 30, 0, 0, 0, 0, "stand"),
        ("lilsis-edo", 160, 560, 90, 0, 0, 0, "stand"), ("mom-edo", 200, 572, 90, 0, 0, 0, "stand"),
        ("kihei", M["cotton"][0], M["cotton"][1], 0, 156, 0, 0, "stand"),
    ]


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "out"
    shots = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "out")
    folder = os.path.join(HERE, "out", "edo-town") if which == "out" else os.path.join(HERE, "..", "..", "art", "scenes", "edo-town")
    os.chdir(HERE)
    bad, lay = check(folder)
    print("CHECK edo-town", which, "OK" if not bad else "")
    for b in bad:
        print("  ", b)
    os.makedirs(shots, exist_ok=True)
    layout_picture("edo-town", folder, lay, os.path.join(shots, f"town-layout-{which}.png"))
    try:
        people_picture("edo-town", folder, lay, town_folk(lay), os.path.join(shots, f"town-people-{which}.png"))
    except Exception as e:
        print("no people shot:", e)

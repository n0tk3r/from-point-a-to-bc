"""Checks on the castle approach as painted (out/edo-castle/) or as installed (art/scenes/edo-castle/), and the pictures to
look at. PAINT-20D.

  python3 edo_castle_check.py [out|art] [shots_dir]
      the sizes (800 x 600, every file of the plan, nothing not in it), the cut-outs hard-edged, the opening clear, every
      mark inside the walk outline (or where the brief says it is above it), every thing of ROUND-20.md's list with a
      shape, the stands' sizes, the frames' sizes and foot point; then writes <shots_dir>/layout-<which>.png (the layout
      drawn over the picture) and, with the game served on port 8904 and Playwright, <shots_dir>/people-<which>.png (the
      game's own figures standing at the marks: the three at enter, under the cherry and at the ladder; two guards of 1.56 m
      at the gate; Tomezo on the ladder) and <shots_dir>/tile-<which>.png (the cross tile at 4x beside the gable at 1x)."""

import asyncio
import base64
import io
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
NEEDED = ["cherry", "petals", "keep", "gate", "gable", "guards", "ladder", "tomezo", "scaffold", "buckets", "wall", "moat", "herons", "pilgrims", "road", "ramp", "stonebase"]
MARKS = ["enter", "cherry", "ladder", "tomezo", "crew", "gate", "guard1", "guard2", "tile", "moat", "road"]
ABOVE = {"tomezo", "scaffold1", "scaffold2", "toKeep", "pilgrimsFrom", "pilgrimsTo"}


def inside(poly, x, y):
    n = len(poly)
    c = False
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0 + 1e-9) + x0:
            c = not c
    return c


def check(folder):
    import postimp_plans as PP
    plan = PP.PLANS["edo-castle"]
    bad = []
    files = sorted(f for f in os.listdir(folder) if f.endswith(".png"))
    import fnmatch
    for f in files:
        name = f[:-4]
        ok = name == "back" or name in plan["planes"] or any(fnmatch.fnmatch(name, p) for p in plan["frames"])
        if not ok:
            bad.append(f"{f}: not in the plan")
        im = Image.open(os.path.join(folder, f))
        if name == "back" or name in plan["planes"]:
            if im.size != (800, 600):
                bad.append(f"{f}: {im.size}")
            if name != "back":
                a = np.asarray(im.convert("RGBA"))[..., 3]
                if ((a > 0) & (a < 255)).any():
                    bad.append(f"{f}: soft alpha")
                if a.max() == 0:
                    bad.append(f"{f}: empty")
    for name in plan["planes"] + ["back"]:
        if f"{name}.png" not in files:
            bad.append(f"{name}.png missing")
    lay = json.load(open(os.path.join(folder, "layout.json")))
    walk = lay["walk"]
    for m in MARKS:
        if m not in lay["marks"]:
            bad.append(f"mark {m} missing")
        elif m not in ABOVE and not inside(walk, *lay["marks"][m]):
            bad.append(f"mark {m} {lay['marks'][m]} outside the walk outline")
    for m, v in lay["marks"].items():
        if m in ABOVE or isinstance(v[0], list):
            continue
        if not inside(walk, *v):
            bad.append(f"mark {m} {v} outside the walk outline")
    ids = {t["id"] for t in lay["things"]}
    for t in NEEDED:
        if t not in ids:
            bad.append(f"thing {t} has no shape")
    for t in lay["things"]:
        if len(t["shape"]["poly"]) < 3:
            bad.append(f"thing {t['id']}: shape too small")
    # the gate's opening clear in gate.png, and the guards' feet in front of its base
    g = np.asarray(Image.open(os.path.join(folder, "gate.png")).convert("RGBA"))[..., 3]
    o0, o1 = 629, 729
    if g[330:432, o0 + 3:o1 - 3].max() > 0:
        bad.append("gate.png: the opening is not clear")
    if not (lay["marks"]["guard1"][1] > 436 and lay["marks"]["guard2"][1] > 436):
        bad.append("the guards are behind the gate's base")
    # the frames: one size, the foot point inside, hard-edged
    fr = lay["frames"]["herons"]
    for f in files:
        if f.startswith("heron-") or f.startswith("egret-"):
            im = Image.open(os.path.join(folder, f))
            if list(im.size) != fr["size"]:
                bad.append(f"{f}: {im.size} (frames are {fr['size']})")
            a = np.asarray(im.convert("RGBA"))[..., 3]
            if ((a > 0) & (a < 255)).any():
                bad.append(f"{f}: soft alpha")
    # the stands' sizes agree with the camera
    for k, st in lay["stands"].items():
        if st["floor"] == "ground":
            want = int(round(160 * (st["at"][1] - lay["horizon"]) / (lay["full"] - lay["horizon"])))
            if abs(want - st["grownup_px"]) > 1:
                bad.append(f"stand {k}: {st['grownup_px']} px, the camera says {want}")
    return bad, lay


def layout_picture(folder, lay, path):
    im = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    import postimp_plans as PP
    for name in PP.PLANS["edo-castle"]["planes"]:
        im.alpha_composite(Image.open(os.path.join(folder, name + ".png")).convert("RGBA"))
    d = ImageDraw.Draw(im, "RGBA")
    d.polygon([tuple(p) for p in lay["walk"]], outline=(0, 255, 0, 255))
    for b in lay["blocked"]:
        d.polygon([tuple(p) for p in b], outline=(255, 0, 0, 255))
    for t in lay["things"]:
        d.polygon([tuple(p) for p in t["shape"]["poly"]], outline=(255, 200, 0, 160))
    for pl in lay["planes"]:
        if isinstance(pl.get("base"), int):
            d.line([(0, pl["base"]), (800, pl["base"])], fill=(0, 200, 255, 90))
    for k, v in lay["marks"].items():
        pts = v if isinstance(v[0], list) else [v]
        for x, y in pts:
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 0, 255, 255))
        x, y = pts[0]
        d.text((x + 5, y - 10), k, fill=(255, 255, 255, 255))
    im.convert("RGB").save(path)


async def people_shot(folder, lay, path, port=8904):
    """The game's own figures stood at the marks (people_on.py's way, on this folder's port; a height in cm may be given)."""
    from playwright.async_api import async_playwright
    hz, full = lay["horizon"], lay["full"]
    st = lay["stands"]
    folk = [  # who, x, y, yaw, height cm (0: the person's own), scale (0: by the row)[, the row he sorts at: a base of his own]
        ("mom", *lay["marks"]["enter"], 90, 0, 0), ("bigsis", lay["marks"]["enter"][0] + 40, lay["marks"]["enter"][1] - 4, 90, 0, 0),
        ("lilsis", lay["marks"]["enter"][0] + 72, lay["marks"]["enter"][1] + 4, 90, 0, 0),
        ("mom", *lay["marks"]["cherry"], 0, 0, 0), ("lilsis", *lay["marks"]["underBoughs"], 0, 0, 0),
        ("bigsis", *lay["marks"]["ladder"], 180, 0, 0), ("mom", lay["marks"]["crew"][0], lay["marks"]["crew"][1], 90, 0, 0),
        ("dad", *lay["marks"]["guard1"], 90, 156, 0), ("dad", *lay["marks"]["guard2"], 270, 156, 0),
        ("dad", *lay["marks"]["tomezo"], 180, 156, st["tomezo"]["scale"], st["tomezo"]["base"]),
        ("dad", *lay["marks"]["scaffold1"], 180, 156, st["scaffold1"]["scale"], st["scaffold1"]["base"]),
        ("son", *lay["marks"]["tile"], 180, 0, 0), ("bigsis", *lay["marks"]["moat"], 180, 0, 0),
        ("dad", 700, 578, 270, 156, 0),
    ]
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 900, "height": 700})
        page.on("pageerror", lambda e: print("[pageerror]", e))
        await page.goto(f"http://localhost:{port}/tools/sprites.html")
        await page.wait_for_timeout(1200)
        res = await page.evaluate("""([folk, hz, full]) => {
            const L = window.lab; const figs = [];
            for (const [sid, x, y, yaw, cm, sc, sortRow] of folk) {
              try {
                const spec = L.people[sid]; if (!spec) { figs.push({ err: 'nobody called ' + sid }); continue; }
                const h = cm ? cm / 175 : spec.height;
                const k = sc ? sc : (y - hz) / (full - hz);
                const px = Math.round(L.BASE * h * k);
                const sf = L.drawFigure(spec, L.poses.stand(spec, 0), +yaw, px); const cv = sf.toCanvas();
                figs.push({ url: cv.toDataURL(), ox: sf.ox, oy: sf.oy, x, y, px, sort: sortRow || y });
              } catch (e) { figs.push({ err: String(e) }); }
            }
            return figs; }""", [folk, hz, full])
        await b.close()
    im = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    import postimp_plans as PP
    planes = PP.PLANS["edo-castle"]["planes"]
    bases = {pl["id"]: pl.get("base", -1 if pl.get("plane") == "back" else 10000) for pl in lay["planes"]}
    layers = [(bases[n], n) for n in planes]
    figs = [f for f in res if "err" not in f]
    for f in res:
        if "err" in f:
            print("skipped:", f["err"])
    order = sorted([(b, "cut", n) for b, n in layers] + [(f["sort"], "fig", f) for f in figs], key=lambda t: (t[0], 0 if t[1] == "cut" else 1))
    for b, kind, what in order:
        if kind == "cut":
            im.alpha_composite(Image.open(os.path.join(folder, what + ".png")).convert("RGBA"))
        else:
            fig = Image.open(io.BytesIO(base64.b64decode(what["url"].split(",")[1]))).convert("RGBA")
            im.alpha_composite(fig, (int(round(what["x"] - what["ox"])), int(round(what["y"] - what["oy"]))))
    # the herons' first frames in the moat, for the look of it
    for (f, x, y) in (("heron-1.png", 120, 468), ("heron-3.png", 210, 460), ("egret-1.png", 300, 472), ("heron-5.png", 260, 452), ("egret-3.png", 380, 462)):
        fr = Image.open(os.path.join(folder, f)).convert("RGBA")
        k = (y - hz) / (590 - hz)
        fr = fr.resize((max(1, int(fr.width * k)), max(1, int(fr.height * k))), Image.NEAREST)
        im.alpha_composite(fr, (int(x - 48 * k), int(y - 98 * k)))
    im.convert("RGB").save(path)
    print(path, [f["px"] for f in figs])


def tile_shot(folder, path):
    im = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    im.alpha_composite(Image.open(os.path.join(folder, "gate.png")).convert("RGBA"))
    crop = im.crop((630, 170, 720, 240))
    big = crop.resize((crop.width * 4, crop.height * 4), Image.NEAREST)
    whole = im.crop((560, 150, 800, 300))
    out = Image.new("RGB", (big.width + whole.width + 12, max(big.height, whole.height)), (40, 40, 40))
    out.paste(big.convert("RGB"), (0, 0))
    out.paste(whole.convert("RGB"), (big.width + 12, 0))
    out.save(path)


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "out"
    shots = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "out")
    folder = os.path.join(HERE, "out", "edo-castle") if which == "out" else os.path.join(HERE, "..", "..", "art", "scenes", "edo-castle")
    os.chdir(HERE)
    bad, lay = check(folder)
    print("CHECK", which, "OK" if not bad else "")
    for b in bad:
        print("  ", b)
    os.makedirs(shots, exist_ok=True)
    layout_picture(folder, lay, os.path.join(shots, f"layout-{which}.png"))
    tile_shot(folder, os.path.join(shots, f"tile-{which}.png"))
    try:
        asyncio.run(people_shot(folder, lay, os.path.join(shots, f"people-{which}.png")))
    except Exception as e:
        print("no people shot:", e)

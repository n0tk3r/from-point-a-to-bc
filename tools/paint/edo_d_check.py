"""PAINT-21D: the checks on edo-theatre's and edo-akashi's finished pictures and layout.json, the check pictures, and the
game's own people stood in them.

    python3 edo_d_check.py edo-theatre                 checks out/edo-theatre/ (as painted) -> out/edo-theatre-check.png
    python3 edo_d_check.py edo-akashi --installed      checks art/scenes/edo-akashi/ (keyed) -> out/edo-akashi-check-keyed.png
    python3 edo_d_check.py edo-theatre --installed --people 8934 [--out DIR]
                                                       and the game's figures at the marks, in every state (the game served
                                                       on that port: python3 -m http.server 8934 from the game's folder)

What it holds: every picture 800 x 600 (frames and light pictures excepted); every file in the plan (postimp_plans) and
every plane of the plan present; layout.json complete (horizon, full, view, walk, walk_floors, blocked, marks, stands
with grownup_px, things with a shape, planes, cutouts, fx); ROUND-21's marks all there and each inside one of the walk
floors (the dais's two on the dais, by design) and in no blocked patch; ROUND-21's things all there with a shape; every
fx frame present. The check picture: the composite with the walk floors, the blocked patches, each thing's shape, each
mark, each cut-out's base, and grey stand-ins of the right heights on the marks."""

import fnmatch
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.normpath(os.path.join(HERE, "..", ".."))

SCENES = {
    "edo-theatre": {
        "marks": ["back", "jubei", "stand", "peg", "rail", "chanter", "shamisen", "wing", "momseat", "tatsuseat"],
        "things": ["puppets", "heads", "boxes", "lamp", "robes", "boypuppet", "set", "stagerail", "dais", "book", "audience", "windows", "rafters",
                   "jubei", "chanter", "shamisen", "tatsu"],
        "raised": ["chanter", "shamisen"],
        "frames": ["shaft-*"],
    },
    "edo-akashi": {
        "marks": ["road", "shore", "fusa", "leader", "pots", "heita", "tub", "shallows", "ladle", "rocks", "sato", "west"],
        "things": ["strait", "awaji", "castle", "pilgrimboat", "pilgrims", "banner", "ladlething", "pots", "potlines", "heitaboat", "tub", "rocks",
                   "pines", "sand", "road", "fusa", "leader", "heita", "sato", "satosister", "awapilgrim1", "awapilgrim2"],
        "raised": [],
        "frames": ["boat-*"],
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


def check(scene, folder):
    cfg = SCENES[scene]
    problems = []
    from postimp_plans import PLANS
    plan = PLANS.get(scene)
    if plan is None:
        problems.append(f"no plan for {scene} in postimp_plans.py")
        plan = {"planes": [], "alt": {}, "frames": []}
    files = sorted(f for f in os.listdir(folder) if f.endswith(".png"))
    for f in files:
        name = f[:-4]
        is_frame = any(fnmatch.fnmatch(name, pat) for pat in plan["frames"])
        im = Image.open(os.path.join(folder, f))
        if not is_frame and im.size != (800, 600):
            problems.append(f"{f}: {im.size}, not (800, 600)")
        in_plan = name == "back" or name in plan["planes"] or name in plan["alt"] or is_frame or any(name in v for v in plan.get("states", {}).values())
        if not in_plan:
            problems.append(f"{f}: not in the plan")
    for name in plan["planes"] + list(plan["alt"]):
        if f"{name}.png" not in files:
            problems.append(f"plane {name}: no file")
    lay = json.load(open(os.path.join(folder, "layout.json")))
    for key in ("horizon", "full", "view", "walk", "walk_floors", "blocked", "marks", "stands", "things", "planes", "cutouts", "fx"):
        if key not in lay:
            problems.append(f"layout.json: no {key}")
    floors = lay["walk_floors"]
    for m in cfg["marks"]:
        if m not in lay["marks"]:
            problems.append(f"mark {m}: missing")
    for m, p in lay["marks"].items():
        on = [f["name"] for f in floors if inside(f["area"], p)]
        if not on and m not in cfg["raised"]:
            problems.append(f"mark {m} {p}: on no walk floor")
        for b in lay["blocked"]:
            if inside(b["poly"], p):
                problems.append(f"mark {m} {p}: inside blocked {b['id']}")
    for m, st in lay["stands"].items():
        if "grownup_px" not in st or st["grownup_px"] <= 0:
            problems.append(f"stand {m}: no grownup_px")
    ids = {t["id"]: t for t in lay["things"]}
    for t in cfg["things"]:
        if t not in ids:
            problems.append(f"thing {t}: missing")
        elif not ("rect" in ids[t]["shape"] or "poly" in ids[t]["shape"]):
            problems.append(f"thing {t}: no shape")
        else:
            sh = ids[t]["shape"]
            if "rect" in sh and (sh["rect"][2] <= 2 or sh["rect"][3] <= 2):
                problems.append(f"thing {t}: a shape too small {sh['rect']}")
    for pl in lay["planes"]:
        if pl["file"] not in files:
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
        if m.get("src") and m["src"] not in files:
            problems.append(f"fx {m['id']}: {m['src']} missing")
    # floors share no pixel
    if len(floors) > 1:
        a = np.zeros((600, 800), np.uint8)
        for i, f in enumerate(floors):
            im = Image.new("L", (800, 600), 0)
            ImageDraw.Draw(im).polygon([tuple(p) for p in f["area"]], fill=1)
            a += np.asarray(im)
        if (a > 1).any():
            problems.append(f"walk floors overlap at {int((a > 1).sum())} pixels")
    return problems, lay, files, plan


def base_y(pl, x):
    b = pl.get("base")
    if isinstance(b, (int, float)):
        return float(b)
    if isinstance(b, list):
        (x0, y0), (x1, y1) = b
        if x1 == x0:
            return float(max(y0, y1))
        t = np.clip((x - x0) / (x1 - x0), -2, 3)
        return float(y0 + (y1 - y0) * t)
    return None


def compose(folder, lay, state, figures=(), extra_planes=None, hide=()):
    """The scene as the game lays it: back, then the back-plane cut-outs, then cut-outs with a base and the people sorted
    together (a person whose feet are above a cut-out's base is behind it), then the front plane. `state`: {plane id:
    file name or None}; `figures`: [(rgba picture, x, y, foot x, foot y)]."""
    im = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    planes = [dict(p) for p in lay["planes"]]
    for p in planes:
        if p["id"] in state:
            p["file"] = state[p["id"]]
    for p in planes:
        if p.get("alt") and p["id"] not in state:                     # an alt layer (the show) shows only in its state
            continue
        if p.get("plane") == "back" and p.get("file") and p["id"] not in hide:
            im.alpha_composite(Image.open(os.path.join(folder, p["file"])).convert("RGBA"))
    based = [p for p in planes if p.get("plane") not in ("back", "front") and p.get("file") and p["id"] not in hide]
    pics = {p["id"]: Image.open(os.path.join(folder, p["file"])).convert("RGBA") for p in based}
    for p in based:
        im.alpha_composite(pics[p["id"]])
    # each person, far to near: drawn, then every cut-out that stands in front of them laid again over them (in their box)
    for fig, x, y, fx_, fy_ in sorted(figures, key=lambda f: f[4]):
        im.alpha_composite(fig, (int(round(x)), int(round(y))))
        box = (max(0, int(x)), max(0, int(y)), min(800, int(x) + fig.size[0] + 1), min(600, int(y) + fig.size[1] + 1))
        for p in based:
            by = base_y(p, fx_)
            if by is not None and fy_ < by:
                im.alpha_composite(pics[p["id"]].crop(box), (box[0], box[1]))
    for p in planes:
        if p.get("plane") == "front" and p.get("file") and p["id"] not in hide:
            im.alpha_composite(Image.open(os.path.join(folder, p["file"])).convert("RGBA"))
    return im


def figures_from_game(port, lay, who_list):
    """The game's own figures (tools/sprites.html on the served game), each at the size the game draws it at its place:
    who_list = [(kind, x, y, yaw, pose, scale or None)]. -> [(RGBA image, left, top, foot x, foot y)]."""
    import asyncio
    import base64
    import io
    from playwright.async_api import async_playwright
    hz, full = lay["horizon"], lay["full"]

    async def run():
        async with async_playwright() as p:
            b = await p.chromium.launch()
            page = await b.new_page(viewport={"width": 900, "height": 700})
            await page.goto(f"http://localhost:{port}/tools/sprites.html")
            await page.wait_for_timeout(1500)
            res = await page.evaluate("""([folk, hz, full]) => {
                const L = window.lab; const figs = [];
                for (const [sid, pose, yaw, x, y, sc] of folk) {
                  try {
                    const spec = L.people[sid]; if (!spec) { figs.push({ err: 'nobody called ' + sid }); continue; }
                    const k = sc === null ? (y - hz) / (full - hz) : sc;
                    const px = Math.round(L.BASE * spec.height * k);
                    let P;
                    try { P = eval('(' + pose + ')'); } catch (e) { P = L.poses.stand(spec, 0); }
                    const sf = L.drawFigure(spec, P, +yaw, px); const cv = sf.toCanvas();
                    figs.push({ url: cv.toDataURL(), ox: sf.ox, oy: sf.oy, x, y, px });
                  } catch (e) { figs.push({ err: String(e) }); }
                }
                return figs; }""", [[[w[0], w[4], w[3], w[1], w[2], w[5]] for w in who_list], hz, full])
            await b.close()
            return res
    res = asyncio.run(run())
    out = []
    for f in res:
        if "err" in f:
            print("skipped:", f["err"])
            continue
        fig = Image.open(io.BytesIO(base64.b64decode(f["url"].split(",")[1]))).convert("RGBA")
        out.append((fig, f["x"] - f["ox"], f["y"] - f["oy"], f["x"], f["y"]))
    return out


def overlay(im, lay):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    cols = [(40, 220, 255, 255), (255, 160, 40, 255), (120, 255, 120, 255)]
    for i, f in enumerate(lay["walk_floors"]):
        d.polygon([tuple(p) for p in f["area"]], outline=cols[i % 3])
    for b in lay["blocked"]:
        d.polygon([tuple(p) for p in b["poly"]], outline=(255, 60, 60, 255), fill=(255, 60, 60, 40))
    for t in lay["things"]:
        sh = t["shape"]
        if "rect" in sh:
            x, y, w, h = sh["rect"]
            d.rectangle([x, y, x + w, y + h], outline=(255, 255, 0, 160))
        else:
            d.polygon([tuple(p) for p in sh["poly"]], outline=(255, 255, 0, 160))
        if "rect" in sh:
            d.text((sh["rect"][0] + 2, sh["rect"][1] + 1), t["id"], fill=(255, 255, 120, 220))
    for pl in lay["planes"]:
        b = pl.get("base")
        if isinstance(b, (int, float)):
            d.line([0, b, 800, b], fill=(255, 140, 0, 90))
        elif isinstance(b, list):
            d.line([tuple(b[0]), tuple(b[1])], fill=(255, 140, 0, 230), width=2)
    for m, p in lay["marks"].items():
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=(255, 0, 255, 255))
        d.text((p[0] + 5, p[1] - 5), m, fill=(255, 255, 255, 255))
    im.alpha_composite(ov)
    return im


if __name__ == "__main__":
    scene = sys.argv[1]
    installed = "--installed" in sys.argv
    folder = os.path.join(GAME, "art", "scenes", scene) if installed else os.path.join(HERE, "out", scene)
    tag = "keyed" if installed else "painted"
    problems, lay, files, plan = check(scene, folder)
    for p in problems:
        print("PROBLEM:", p)
    out_png = os.path.join(HERE, "out", f"{scene}-check-{tag}.png")
    im = compose(folder, lay, {})
    overlay(im, lay).convert("RGB").save(out_png)
    print(f"{scene} ({tag}): {len(problems)} problem{'s' if len(problems) != 1 else ''}; {out_png}")
    if "--people" in sys.argv:
        port = int(sys.argv[sys.argv.index("--people") + 1])
        outdir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(HERE, "out")
        import edo_d_people
        edo_d_people.shots(scene, folder, lay, port, outdir, compose, figures_from_game)
    sys.exit(1 if problems else 0)

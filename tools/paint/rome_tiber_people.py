"""Across the Tiber with people in it: the game's own figures (drawn by the game's figure page, as people_on.py does)
stood at the scene's marks on the installed, keyed pictures, and laid together as the engine lays them: the backdrop,
then the cut-outs and the people back to front by their bases (a person against a cut-out is compared where the
person stands; feet exactly on a base line are in front of it), then the front plane. A man at the window is drawn at
the window's own `scale`, not by his row; a man on the bench with the game's sitting pose. The hens stand in their row
(each flock's first stand frame at the middle of its perch, at the row's size), behind the fence. Into
../looks/people-*.png, with close crops.

    python3 rome_tiber_people.py [http://localhost:8823/] [path/to/art/scenes/rome-tiber]

Needs the game served (it draws the figures with tools/sprites.html) and Playwright."""

import asyncio
import base64
import functools
import io
import json
import os
import sys

from PIL import Image
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8823/"
ART = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "game", "art", "scenes", "rome-tiber")
LOOKS = os.path.join(HERE, "..", "looks")
YAW = {"S": 0, "SE": 45, "E": 90, "NE": 135, "N": 180, "NW": 225, "W": 270, "SW": 315}     # (the engine's compass)
BLESS_STEP = 0.30                                            # the master brief's: the boy a step in front of Eleazar
GROWN_CM = 175.0                                             # a grown man (height 1), as the camera is worked out

FIGURES_JS = """([folk, hz, full]) => {
  const L = window.lab; const out = [];
  for (const f of folk) {
    try {
      const spec = L.people[f.who]; if (!spec) { out.push({ err: 'nobody called ' + f.who }); continue; }
      const k = f.scale != null ? f.scale : (f.y - hz) / (full - hz);
      const px = L.BASE * spec.height * k;
      const pose = f.sit != null ? L.poses.sit(spec, 0, { seat: f.sit }) : L.poses.stand(spec, 0);
      const sf = L.drawFigure(spec, pose, f.yaw, px); const cv = sf.toCanvas();
      out.push({ url: cv.toDataURL(), ox: sf.ox, oy: sf.oy, x: f.x, y: f.y, px, label: f.label || f.who });
    } catch (e) { out.push({ err: String(e) }); }
  }
  return out; }"""


async def draw_all(groups, hz, full):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 900, "height": 700})
        page.on("pageerror", lambda e: print("[pageerror]", e))
        await page.goto(URL.rstrip("/") + "/tools/sprites.html")
        await page.wait_for_function("() => window.lab && window.lab.people && Object.keys(window.lab.people).length > 0", timeout=20000)
        res = {name: await page.evaluate(FIGURES_JS, [folk, hz, full]) for name, folk in groups.items()}
        await b.close()
    return res


def base_at(base, x, y):
    if base is None:
        return y
    if isinstance(base, (int, float)):
        return base
    (x1, y1), (x2, y2) = base
    t = 0.5 if x2 == x1 else min(1.0, max(0.0, (x - x1) / (x2 - x1)))
    return y1 + (y2 - y1) * t


def lay(L, figs, name, back=None):
    """The picture as the engine composes it, people and cut-outs in the engine's order (cast.js, order())."""
    im = (back or Image.open(os.path.join(ART, "back.png"))).convert("RGBA")
    floor, front = [], []
    for pl in L["planes"]:
        pic = Image.open(os.path.join(ART, pl["file"])).convert("RGBA")
        (front if pl.get("plane") == "front" else floor).append({"person": False, "id": pl["id"], "base": pl.get("base"), "pic": pic, "x": 0, "y": 0})
    for f in figs:
        if "err" in f:
            print("skipped:", f["err"])
            continue
        fig = Image.open(io.BytesIO(base64.b64decode(f["url"].split(",")[1]))).convert("RGBA")
        floor.append({"person": True, "id": f["label"], "base": None, "pic": fig, "x": f["x"], "y": f["y"], "ox": f["ox"], "oy": f["oy"]})
    mid = lambda s: (s["base"][0][0] + s["base"][1][0]) / 2 if isinstance(s["base"], list) else s["x"]

    def depth(a, b):
        x = a["x"] if a["person"] else b["x"] if b["person"] else a["x"] if a["base"] is None else b["x"] if b["base"] is None else (mid(a) + mid(b)) / 2
        d = base_at(a["base"], x, a["y"]) - base_at(b["base"], x, b["y"])
        return d if d else int(a["person"]) - int(b["person"])
    floor.sort(key=functools.cmp_to_key(depth))
    for s in floor + front:
        if s["person"]:
            im.alpha_composite(s["pic"], (int(round(s["x"] - s["ox"])), int(round(s["y"] - s["oy"]))))
        else:
            im.alpha_composite(s["pic"])
    im.convert("RGB").save(os.path.join(LOOKS, f"people-{name}.png"))
    print(f"people-{name}.png:", ", ".join(s["id"] for s in floor))
    return im


def with_hens(L):
    """The backdrop with a hen standing at the middle of each hen flock's perch, at the size the game draws it there."""
    hz, full = L["horizon"], L["full"]
    im = Image.open(os.path.join(ART, "back.png")).convert("RGBA")
    for h in [f for f in L["fx"] if str(f.get("id", "")).startswith("hen-")]:
        (x1, y1), (x2, y2) = h["perch"]
        x, y = (x1 + x2) / 2, (y1 + y2) / 2
        fb = h["frames"]
        pic = Image.open(os.path.join(ART, fb["stand"][0])).convert("RGBA")
        k = (y - hz) / (fb["sizeAt"] - hz)
        pic = pic.resize((max(1, round(pic.width * k)), max(1, round(pic.height * k))), Image.LANCZOS)
        im.alpha_composite(pic, (int(round(x - fb["foot"][0] * k)), int(round(y - fb["foot"][1] * k))))
    return im


def main():
    L = json.load(open(os.path.join(ART, "layout.json")))
    hz, full, m = L["horizon"], L["full"], L["marks"]
    P = lambda who, p, face="S", **kw: dict(who=who, x=p[0], y=p[1], yaw=YAW[face], **kw)
    bx, by = m["bless"][:2]
    eleazar_h = 0.96 * 160 * (by - hz) / (full - hz)
    groups = {
        "a-window": [P("dateseller", m["window"]["at"], "W", scale=m["window"]["scale"], label="dateseller@window"),
                     P("son", m["fromBridge"], "N", label="son@fromBridge"), P("son", m["wait"], "W", label="son@wait"),
                     P("lilsis", m["mariam"]["at"], m["mariam"]["face"], label="lilsis@mariam"), P("senator", m["felix"]["at"], m["felix"]["face"], label="senator@felix")],
        "b-prayer": [P("dateseller", m["pray_eleazar"], m["pray_eleazar"][2], label="dateseller@pray_eleazar"), P("son", m["pray_son"], m["pray_son"][2], label="son@pray_son")],
        "c-bless": [P("dateseller", m["bless"], m["bless"][2], label="dateseller@bless"), P("son", [bx + BLESS_STEP * eleazar_h, by], "W", label="son@bless+step")],
        "d-bench": [P("dateseller", m["bench_seat"]["at"], "SW", sit=round(m["bench_seat"]["cm"] / GROWN_CM, 3), label="dateseller@bench_seat"),
                    P("son", m["wait"], "W", label="son@wait"), P("son", m["door"], "S", label="son@door")],
        "e-stands": [P("son", t["stand"], t.get("face", "S"), label=f"son@{t['id']}") for t in L["things"]]
                    + [P("son", m["default"], "S", label="son@default"), P("son", m["toBridge"], "S", label="son@toBridge")],
        "f-yard": [P("lilsis", m["mariam"]["at"], m["mariam"]["face"], label="lilsis@mariam")]
                  + [P("lilsis", s[:2], s[2], label=f"lilsis@spot{i}") for i, s in enumerate(m["mariam_spots"])]
                  + [P("son", m["mariam_talk"], "E", label="son@mariam_talk")],
        "g-landing": [P("senator", m["felix"]["at"], m["felix"]["face"], label="senator@felix")]
                     + [P("senator", s[:2], s[2], label=f"senator@spot{i}") for i, s in enumerate(m["felix_spots"])]
                     + [P("clerk", m["petosiris"], "W", label="clerk@petosiris")],
    }
    os.makedirs(LOOKS, exist_ok=True)
    res = asyncio.run(draw_all(groups, hz, full))
    pics = {}
    for name, figs in res.items():
        pics[name] = lay(L, figs, name, back=with_hens(L) if name == "f-yard" else None)
        print("   sizes (px):", ", ".join(f"{f['label']} {f['px']:.1f}" for f in figs if "err" not in f))

    def crop(name, box, z, out):
        pics[name].crop(box).resize(((box[2] - box[0]) * z, (box[3] - box[1]) * z), Image.LANCZOS).convert("RGB").save(os.path.join(LOOKS, out))
    crop("a-window", (600, 150, 760, 300), 4, "people-a-window-zoom.png")
    crop("d-bench", (430, 330, 640, 470), 3, "people-d-bench-zoom.png")
    crop("c-bless", (380, 330, 560, 450), 3, "people-c-bless-zoom.png")
    crop("f-yard", (480, 330, 800, 520), 3, "people-f-yard-zoom.png")
    crop("g-landing", (0, 330, 260, 600), 3, "people-g-landing-zoom.png")


if __name__ == "__main__":
    main()

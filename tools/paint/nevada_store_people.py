"""The test that matters: the game's own figures standing in the store, at the size the game will draw them there,
sorted with the store's cut-outs by their base lines as the engine sorts them (a figure whose feet are above a
cut-out's base, at the figure's x, is behind it).

    python3 nevada_store_people.py                 the finished room (out/nevada-store/): the three just in from the lot,
                                                   at the counter, Little Sister on the back step, Jolene behind the
                                                   counter (Jed, `agent`, stands in for her until she exists), and the
                                                   far places and the front; writes out/nevada-store-people-*.png
    python3 nevada_store_people.py plan            the same on the skeleton (out/nevada-store-work/plan.png)
    python3 nevada_store_people.py installed       the same on the pictures as installed (keyed) in the game copy
    python3 nevada_store_people.py onstage         the installed pictures again, with the game's people_on.py itself:
                                                   the three at fromLot with Jolene at her first spot; one at the
                                                   counter, Little Sister on the step, a grown-up watching from the
                                                   doorway, Jolene at her second spot (out/nevada-store-onstage-*.png)

The figures are drawn by the game's own code, as people_on.py draws them (the same page, the same calls), from this
painter's copy of the game, served on port 8782:  cd ../../ && python3 -m http.server 8782"""
import asyncio
import base64
import io
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8782
# the scene as installed: beside the game's art/ when this runs from the game's tools/paint, else in the painter's
# copy of the game next to this folder
INSTALLED = next((p for p in (os.path.join(HERE, "..", "..", "art", "scenes", "nevada-store"),
                              os.path.join(HERE, "..", "game", "art", "scenes", "nevada-store")) if os.path.isdir(p)),
                 os.path.join(HERE, "..", "game", "art", "scenes", "nevada-store"))


async def _figures(folk, hz, full):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 900, "height": 700})
        page.on("pageerror", lambda e: print("[pageerror]", e))
        await page.goto(f"http://localhost:{PORT}/tools/sprites.html")
        await page.wait_for_timeout(1200)
        res = await page.evaluate("""([folk, hz, full]) => {
            const L = window.lab; const figs = [];
            for (const [sid, pose, yaw, x, y] of folk) {
              try {
                const spec = L.people[sid]; if (!spec) { figs.push({ err: 'nobody called ' + sid }); continue; }
                const px = Math.round(L.BASE * spec.height * (y - hz) / (full - hz));
                const stand = (f) => L.poses.stand(spec, f), walk = (ph) => L.poses.walk(spec, ph);
                const sf = L.drawFigure(spec, eval('(' + pose + ')'), +yaw, px); const cv = sf.toCanvas();
                figs.push({ url: cv.toDataURL(), ox: sf.ox, oy: sf.oy, x, y, px, who: sid });
              } catch (e) { figs.push({ err: String(e) }); }
            }
            return figs; }""", [folk, hz, full])
        await b.close()
    return res


def figures(folk, hz, full):
    """folk: [(who, x, y, yaw[, pose])] -> [(image, left, top, x, y, px, who)]"""
    F = [[f[0], f[4] if len(f) > 4 else "stand(0)", float(f[3]), float(f[1]), float(f[2])] for f in folk]
    res = asyncio.run(_figures(F, hz, full))
    out = []
    for f in res:
        if "err" in f:
            print("skipped:", f["err"])
            continue
        im = Image.open(io.BytesIO(base64.b64decode(f["url"].split(",")[1]))).convert("RGBA")
        out.append((im, int(round(f["x"] - f["ox"])), int(round(f["y"] - f["oy"])), f["x"], f["y"], f["px"], f["who"]))
    return out


def base_at(base, x):
    """The row of a cut-out's base under the column x (a number, or a line, extended at its ends)."""
    if isinstance(base, (int, float)):
        return float(base)
    (x1, y1), (x2, y2) = base
    if abs(x2 - x1) < 1e-6:
        return max(y1, y2)
    t = (x - x1) / (x2 - x1)
    return y1 + (y2 - y1) * t


def compose(back, cutouts, figs, out):
    """back: picture path. cutouts: [(picture path, base or 'front' or 'back')], in the scene's order. figs: figures().
    Painted as the engine sorts: everything back to front by where it meets the ground."""
    im = Image.open(back).convert("RGBA")
    items = []
    for i, (p, base) in enumerate(cutouts):
        items.append(("c", i, p, base))
    for j, f in enumerate(figs):
        items.append(("f", j, f, None))

    def before(a, b):                                       # True if a is painted before b
        if a[0] == "c" and b[0] == "c":                    # back planes first, front ones last, the others in the scene's order
            rank = lambda c: (0 if c[3] == "back" else 2 if c[3] == "front" else 1, c[1])
            return rank(a) < rank(b)
        if a[0] == "f" and b[0] == "f":
            return a[2][4] < b[2][4]
        if a[0] == "c":
            c, f = a, b
            flip = False
        else:
            c, f = b, a
            flip = True
        base = c[3]
        if base == "front":
            cb = False                                      # the cut-out is painted after the figure
        elif base == "back":
            cb = True
        else:
            cb = f[2][4] >= base_at(base, f[2][3])          # the figure's feet on or below the base: the figure is in front
        return cb if not flip else not cb
    order = []
    rest = items[:]
    while rest:                                             # take, each time, the one that nothing left must precede
        waiting = [sum(1 for o in rest if o is not it and before(o, it)) for it in rest]
        k = min(range(len(rest)), key=lambda k: (waiting[k], k))
        order.append(rest.pop(k))
    for it in order:
        if it[0] == "c":
            im.alpha_composite(Image.open(it[2]).convert("RGBA"))
        else:
            fim, left, top = it[2][0], it[2][1], it[2][2]
            layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
            layer.paste(fim, (left, top), fim)
            im.alpha_composite(layer)
    im.convert("RGB").save(out)
    return out


def hens_layer(folder, L, out_path, state="guard-a"):
    """The five hens laid where the scene lays them (each at her `at`, by her foot point), as one full-size picture."""
    hj = L["hens"]
    im = Image.new("RGBA", (800, 600), (0, 0, 0, 0))
    for h in hj["hens"]:
        f = Image.open(os.path.join(folder, f"hen-{h['n']}-{state}.png")).convert("RGBA")
        im.alpha_composite(f, (int(h["at"][0] - hj["foot"][0]), int(h["at"][1] - hj["foot"][1])))
    im.save(out_path)
    return out_path


def scene_cutouts(folder, L, states=None):
    """The layout's planes as (path, base) in their order, in their first state (or `states` {id: file}), with the
    hens first (they are outside, behind everything of the room)."""
    out = []
    if L.get("hens"):
        rows = [h["at"][1] for h in L["hens"]["hens"]]
        out.append((hens_layer(folder, L, "out/nevada-store-work/hens-layer.png"), max(rows)))
    for p in L["planes"]:
        f = (states or {}).get(p["id"], p.get("file"))
        if not f or p.get("hidden"):
            continue
        path = os.path.join(folder, f)
        if not os.path.exists(path):
            continue
        base = "front" if p.get("plane") == "front" else p.get("base", "back")
        out.append((path, base))
    return out


def tests(L):
    """Who stands where in each test picture."""
    m, S = L["marks"], {k: v["at"] for k, v in L["stands"].items()}
    j = m["jolene"]["spots"]
    return {
        "arrive": [("mom", *m["fromLot"]["mom"], 0), ("bigsis", *m["fromLot"]["bigsis"], 0), ("lilsis", *m["fromLot"]["lilsis"], 0),
                   ("agent", *j[0], 0)],
        "counter": [("mom", *m["counter"], 180), ("bigsis", *S["ateggs"], 200), ("lilsis", *S["atbasket"], 160), ("agent", *j[1], 0)],
        "step": [("lilsis", *m["step"], 180), ("mom", *S["watchleft"], 160), ("bigsis", *S["watchright"], 200), ("agent", *j[0], 20)],
        "about": [("bigsis", *S["atspinner"], 270), ("mom", *S["atrockbins"], 180), ("lilsis", *S["atcooler"], 180),
                  ("mom", *S["atsurvival"], 160), ("bigsis", *S["atwindow"], 270)],
        "front": [("mom", *S["front"], 0), ("bigsis", *S["frontright"], 0), ("lilsis", *S["atdoor"], 90), ("mom", *S["atautoshelf"], 270),
                  ("bigsis", *S["atgrill"], 180)],
    }


def on_stage(folder):
    """The check the brief asks for, made with the game's own people_on.py (a copy of it pointed at this game copy's
    server): the installed back.png with the hens and the back planes laid on it, then the people in passes, each
    pass the people who stand behind the next cut-outs, those cut-outs laid over them (people_on.py's extra
    arguments), the front plane over the last. -> out/nevada-store-onstage-<name>.png"""
    import subprocess
    L = json.load(open(os.path.join(folder, "layout.json")))
    work = os.path.join(HERE, "out", "nevada-store-work")
    tool = os.path.join(work, "people_on_here.py")
    with open(tool, "w") as f:
        f.write(open(os.path.join(HERE, "people_on.py")).read().replace("8765", str(PORT)))
    base = Image.open(os.path.join(folder, "back.png")).convert("RGBA")
    base.alpha_composite(Image.open(hens_layer(folder, L, os.path.join(work, "hens-layer.png"))))
    for p in L["planes"]:
        if p.get("plane") == "back" and p.get("file"):
            base.alpha_composite(Image.open(os.path.join(folder, p["file"])).convert("RGBA"))
    base_path = os.path.join(work, "onstage-base.png")
    base.convert("RGB").save(base_path)
    based = [p for p in L["planes"] if p.get("base") and p.get("file") and p.get("plane") not in ("back", "front")]
    based.sort(key=lambda p: (p["base"][0][1] + p["base"][1][1]) / 2)
    boxes = {p["id"]: Image.open(os.path.join(folder, p["file"])).convert("RGBA").getchannel("A").getbbox() for p in based}
    front = [os.path.join(folder, p["file"]) for p in L["planes"] if p.get("plane") == "front"]

    def layer(who, x, y):
        """The first of the cut-outs (in the order they are laid) that this person stands behind and could overlap."""
        for k, p in enumerate(based):
            x0, y0, x1, y1 = boxes[p["id"]]
            cx = min(max(x, x0), x1)
            if abs(x - cx) < 30 and y > y0 and y < base_at(p["base"], cx):
                return k
        return len(based)
    m, S = L["marks"], {k: v["at"] for k, v in L["stands"].items()}
    j = m["jolene"]["spots"]
    pictures = {
        "arrive": [("mom", m["fromLot"]["mom"], 0), ("bigsis", m["fromLot"]["bigsis"], 0), ("lilsis", m["fromLot"]["lilsis"], 0),
                   ("agent", j[0], 0)],
        "counter": [("mom", m["counter"], 180), ("lilsis", m["step"], 180), ("bigsis", S["watchright"], 200), ("agent", j[1], 0)],
    }
    for name, folk in pictures.items():
        passes = [[] for _ in range(len(based) + 1)]
        for who, (x, y), yaw in folk:
            passes[layer(who, x, y)].append(f"{who}|{x}|{y}|{yaw}")
        pic, k = base_path, 0
        out = os.path.join(HERE, "out", f"nevada-store-onstage-{name}.png")
        steps = []
        people = passes[0]
        lay = []
        for i, p in enumerate(based):
            lay.append(os.path.join(folder, p["file"]))
            if passes[i + 1]:
                steps.append((people, lay))
                people, lay = passes[i + 1], []
        steps.append((people, lay + front))
        for n, (people, lay) in enumerate(steps):
            dst = out if n == len(steps) - 1 else os.path.join(work, f"onstage-{name}-{n}.png")
            r = subprocess.run([sys.executable, tool, pic, str(L["horizon"]), str(L["full"]), ";".join(people), dst] + lay,
                               capture_output=True, text=True)
            print("   ", " ".join(people) or "(nobody)", "| over them:", ", ".join(os.path.basename(f) for f in lay), "->",
                  r.stdout.strip() or r.stderr.strip()[-300:])
            pic = dst
        print(out)


if __name__ == "__main__":
    os.chdir(HERE)
    mode = sys.argv[1] if len(sys.argv) > 1 else "room"
    if mode == "onstage":
        on_stage(INSTALLED)
        sys.exit()
    if mode == "plan":
        import nevada_store_model as M
        from room import View
        v = View(**M.VIEW)

        def at(k):
            x, y = v.pt(M.MARKS[k][0], 0, M.MARKS[k][1])
            return round(x), round(y)
        folk = [("mom", *at("mom"), 0), ("bigsis", *at("bigsis"), 0), ("lilsis", *at("lilsis"), 0), ("agent", *at("jolene"), 0),
                ("agent", *at("jolene2"), 0), ("mom", *at("counter"), 180), ("lilsis", *at("step"), 180), ("bigsis", *at("atrockbins"), 180),
                ("mom", *at("atbackdoor"), 180), ("bigsis", *at("front"), 0), ("lilsis", *at("atdoor"), 90)]
        figs = figures(folk, M.VIEW["horizon"], M.VIEW["full"])
        print(compose("out/nevada-store-work/plan.png", [], figs, "out/nevada-store-work/plan-people.png"), [f[5] for f in figs])
        sys.exit()
    folder = "out/nevada-store" if mode == "room" else INSTALLED
    L = json.load(open(os.path.join(folder, "layout.json")))
    cut = scene_cutouts(folder, L)
    tag = "" if mode == "room" else "-installed"
    for name, folk in tests(L).items():
        figs = figures(folk, L["horizon"], L["full"])
        o = compose(os.path.join(folder, "back.png"), cut, figs, f"out/nevada-store-people{tag}-{name}.png")
        print(o, [(f[6], f[5]) for f in figs])

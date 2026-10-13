"""Stand the game's own people in the Forum, at exactly the size the game draws them, sorted with the scene's cut-outs
as the game sorts them (by their feet and the cut-outs' bases), to look at.

    python3 rome_forum_people.py <out.png> "<who>|<x>|<y>[|<yaw>[|<pose>]];..." [folder] [port]

`folder` holds back.png, layout.json and the cut-outs (default out/rome-forum); the game must be running (default port
8821: this painter's copy; people_on.py is the same tool for port 8765, with front-plane pictures only). The depth rule is
the game's own (walk.js scaleAt): (feet - horizon) / (full - horizon), held between minScale and 1.12."""

import asyncio
import base64
import io
import json
import sys

from PIL import Image
from playwright.async_api import async_playwright


def base_at(base, x):
    if base is None:
        return None
    if isinstance(base, (int, float)):
        return float(base)
    (x1, y1), (x2, y2) = base
    t = 0.5 if x2 == x1 else min(1.0, max(0.0, (x - x1) / (x2 - x1)))
    return y1 + (y2 - y1) * t


async def figures(folk, hz, full, lo, hi, port):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 900, "height": 700})
        page.on("pageerror", lambda e: print("[pageerror]", e))
        await page.goto(f"http://localhost:{port}/tools/sprites.html")
        await page.wait_for_timeout(1200)
        res = await page.evaluate("""([folk, hz, full, lo, hi]) => {
            const L = window.lab; const figs = [];
            for (const [sid, pose, yaw, x, y] of folk) {
              try {
                const spec = L.people[sid]; if (!spec) { figs.push({ err: 'nobody called ' + sid }); continue; }
                const k = Math.min(hi, Math.max(lo, (y - hz) / (full - hz)));
                const px = Math.round(L.BASE * spec.height * k);
                const stand = (f) => L.poses.stand(spec, f), walk = (ph) => L.poses.walk(spec, ph);
                const sit = (f) => L.poses.sit(spec, f, { seat: "stool" });          // (seated on a low stool, which the game draws with her)
                const sf = L.drawFigure(spec, eval('(' + pose + ')'), +yaw, px); const cv = sf.toCanvas();
                figs.push({ url: cv.toDataURL(), ox: sf.ox, oy: sf.oy, x, y, px, who: sid });
              } catch (e) { figs.push({ err: String(e) }); }
            }
            return figs; }""", [folk, hz, full, lo, hi])
        await b.close()
    return res


def main():
    out, folk_s = sys.argv[1], sys.argv[2]
    folder = sys.argv[3] if len(sys.argv) > 3 else "out/rome-forum"
    port = int(sys.argv[4]) if len(sys.argv) > 4 else 8821
    lay = json.load(open(f"{folder}/layout.json"))
    hz, full, lo = lay["horizon"], lay["full"], lay.get("minScale", 0.26)
    folk = []
    for f in folk_s.split(";"):
        if not f.strip():
            continue
        q = f.split("|")
        folk.append([q[0], q[4] if len(q) > 4 else "stand(0)", float(q[3]) if len(q) > 3 else 0, float(q[1]), float(q[2])])
    res = asyncio.run(figures(folk, hz, full, lo, 1.12, port))
    im = Image.open(f"{folder}/back.png").convert("RGBA")
    items = []                                                     # (sort key, kind, payload): people by their feet, cut-outs by their base
    for f in res:
        if "err" in f:
            print("skipped:", f["err"])
            continue
        items.append(("p", f))
    planes = [p for p in lay["planes"] if "file" in p]
    order = []
    for i, p in enumerate(planes):
        order.append(("c", (i, p)))
    order += items

    def mid(p):
        b = p.get("base")
        return (b[0][0] + b[1][0]) / 2 if isinstance(b, list) else 0.0

    def depth(a, b):
        """The engine's own comparison (cast.js order): a person against a cut-out at the person's feet; two cut-outs at the
        middle of their bases; feet exactly on a base are in front of it; ties keep the order they were put on the stage."""
        if a[0] == "p":
            x = a[1]["x"]
        elif b[0] == "p":
            x = b[1]["x"]
        else:
            x = (mid(a[1][1]) + mid(b[1][1])) / 2
        def at(s):
            if s[0] == "p":
                return s[1]["y"]
            p = s[1][1]
            if p.get("plane") == "front":
                return None
            return base_at(p.get("base"), x)
        ya, yb = at(a), at(b)
        fa, fb = (a[0] == "c" and a[1][1].get("plane") == "front"), (b[0] == "c" and b[1][1].get("plane") == "front")
        if fa or fb:
            return (1 if fa else 0) - (1 if fb else 0)
        d = ya - yb
        if d:
            return -1 if d < 0 else 1
        return (a[0] == "p") - (b[0] == "p")
    import functools
    order.sort(key=functools.cmp_to_key(depth))
    for kind, payload in order:
        if kind == "c":
            im.alpha_composite(Image.open(f"{folder}/{payload[1]['file']}").convert("RGBA"))
        else:
            fig = Image.open(io.BytesIO(base64.b64decode(payload["url"].split(",")[1]))).convert("RGBA")
            im.alpha_composite(fig, (int(round(payload["x"] - payload["ox"])), int(round(payload["y"] - payload["oy"]))))
    im.convert("RGB").save(out)
    print(out, [(f["who"], round(f["px"])) for f in res if "err" not in f])


if __name__ == "__main__":
    main()

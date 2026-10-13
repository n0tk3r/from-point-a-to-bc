"""The test that matters for the limousine: the game's own figures in the painted car, at the size the game draws them.

    python3 nevada_limo_people.py [picture.png] [out.png] [port]

Stands the old-timer SEATED on the mark `joe` (facing E, across the car: his lawn chair is drawn with him, which is
wrong here, but his size and his hip point are what we are checking), and a few standing figures on the carpet for
scale. Reads the marks from out/nevada-limo/layout.json when it exists, else from the model through the camera.
Needs the game's server (default port 8783: `cd game && python3 -m http.server 8783`) and Playwright."""
import asyncio, base64, io, json, os, sys

from PIL import Image

from room import View
import nevada_limo_model as M

OUT = "out/nevada-limo"


def marks():
    p = f"{OUT}/layout.json"
    if os.path.exists(p):
        L = json.load(open(p))
        return L["horizon"], L["full"], {k: (v["at"] if isinstance(v, dict) else v) for k, v in L["marks"].items()}
    v = View(**M.VIEW)
    return v.hz, v.full, {k: [round(c) for c in v.pt(X, 0, Z)] for k, (X, Z) in M.MARKS.items()}


async def main():
    pic = sys.argv[1] if len(sys.argv) > 1 else f"{OUT}/back.png"
    out = sys.argv[2] if len(sys.argv) > 2 else "out/nevada-limo-people.png"
    port = sys.argv[3] if len(sys.argv) > 3 else "8783"
    hz, full, mk = marks()
    jx, jy = mk["joe"]
    rx, ry = mk["ranger"]
    folk = [["oldtimer", "L.poses.sit(spec, 0)", 270, jx, jy],            # seated, facing E (the game's E is yaw 270 here)
            ["dad", "stand(0)", 0, rx, ry],                                 # a grown-up where Ranger's mark is, for scale
            ["lilsis", "stand(0)", 0, rx + 90, ry - 20]]
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 900, "height": 700})
        page.on("pageerror", lambda e: print("[pageerror]", e))
        await page.goto(f"http://localhost:{port}/tools/sprites.html")
        await page.wait_for_timeout(1200)
        res = await page.evaluate("""([folk, hz, full]) => {
            const L = window.lab; const figs = [];
            for (const [sid, pose, yaw, x, y] of folk) {
              try {
                const spec = L.people[sid]; if (!spec) { figs.push({ err: 'nobody called ' + sid }); continue; }
                const px = Math.round(L.BASE * spec.height * (y - hz) / (full - hz));
                const stand = (f) => L.poses.stand(spec, f), walk = (ph) => L.poses.walk(spec, ph);
                const sf = L.drawFigure(spec, eval('(' + pose + ')'), +yaw, px); const cv = sf.toCanvas();
                figs.push({ url: cv.toDataURL(), ox: sf.ox, oy: sf.oy, x, y, px, tall: L.tallOf ? L.tallOf(spec, eval('(' + pose + ')'), px) : null });
              } catch (e) { figs.push({ err: String(e) }); }
            }
            return figs; }""", [folk, hz, full])
        await b.close()
    im = Image.open(pic).convert("RGBA")
    for f in sorted([f for f in res if "err" not in f], key=lambda f: f["y"]):
        fig = Image.open(io.BytesIO(base64.b64decode(f["url"].split(",")[1]))).convert("RGBA")
        im.alpha_composite(fig, (int(round(f["x"] - f["ox"])), int(round(f["y"] - f["oy"]))))
    for f in res:
        if "err" in f:
            print("skipped:", f["err"])
    front = f"{OUT}/front.png"
    if os.path.exists(front) and pic.endswith("back.png"):
        im.alpha_composite(Image.open(front).convert("RGBA"))
    im.convert("RGB").save(out)
    print(out, [(round(f["px"]), f.get("tall")) for f in res if "err" not in f])

asyncio.run(main())

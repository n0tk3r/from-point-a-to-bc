"""Stand the game's own people on a picture, at exactly the size the game will draw them there.

    python3 people_on.py <picture.png> <horizon> <full> "<who>|<x>|<y>[|<yaw>[|<pose>]];..." <out.png> [front.png ...]

who: mom, bigsis, lilsis, dad, son, ...   x, y: where the feet are, in picture pixels.
yaw: 0 faces us, 180 faces away, 90 / 270 sideways (default 0).   pose: stand(0), walk(0.3), ... (default stand(0)).
Pictures named after <out.png> are laid over the people (front-plane cut-outs).
The game's server must be running at http://localhost:8765/ (it serves the figure-drawing page)."""
import asyncio, base64, io, sys
from PIL import Image
from playwright.async_api import async_playwright


async def main():
    pic, hz, full, folk, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
    fronts = sys.argv[6:]
    FOLK = []
    for f in folk.split(";"):
        if not f.strip():
            continue
        p = f.split("|")
        FOLK.append([p[0], p[4] if len(p) > 4 else "stand(0)", float(p[3]) if len(p) > 3 else 0, float(p[1]), float(p[2])])
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 900, "height": 700})
        page.on("pageerror", lambda e: print("[pageerror]", e))
        await page.goto("http://localhost:8765/tools/sprites.html")
        await page.wait_for_timeout(1200)
        res = await page.evaluate("""([folk, hz, full]) => {
            const L = window.lab; const figs = [];
            for (const [sid, pose, yaw, x, y] of folk) {
              try {
                const spec = L.people[sid]; if (!spec) { figs.push({ err: 'nobody called ' + sid }); continue; }
                const px = Math.round(L.BASE * spec.height * (y - hz) / (full - hz));
                const stand = (f) => L.poses.stand(spec, f), walk = (ph) => L.poses.walk(spec, ph);
                const sf = L.drawFigure(spec, eval('(' + pose + ')'), +yaw, px); const cv = sf.toCanvas();
                figs.push({ url: cv.toDataURL(), ox: sf.ox, oy: sf.oy, x, y, px });
              } catch (e) { figs.push({ err: String(e) }); }
            }
            return figs; }""", [FOLK, hz, full])
        await b.close()
    im = Image.open(pic).convert("RGBA")
    for f in sorted([f for f in res if "err" not in f], key=lambda f: f["y"]):
        fig = Image.open(io.BytesIO(base64.b64decode(f["url"].split(",")[1]))).convert("RGBA")
        im.alpha_composite(fig, (int(round(f["x"] - f["ox"])), int(round(f["y"] - f["oy"]))))
    for f in res:
        if "err" in f:
            print("skipped:", f["err"])
    for n in fronts:
        im.alpha_composite(Image.open(n).convert("RGBA"))
    im.convert("RGB").save(out)
    print(out, [round(f["px"]) for f in res if "err" not in f])

asyncio.run(main())

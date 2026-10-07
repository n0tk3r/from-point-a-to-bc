"""Stand the game's own people on the finished picture, at the size the game will draw them, to judge the scale.
(Borrows the figure-drawing page the game serves; writes only out/egypt-gallery-mock.png.)"""
import asyncio, base64, io, json, sys
from PIL import Image
from playwright.async_api import async_playwright

L = json.load(open("out/egypt-gallery/layout.json"))
FOLK = [("dad", "stand(0)", 180, 300, 562), ("dad", "walk(0.3)", 0, 462, 452), ("dad", "stand(0)", 0, 400, 330), ("dad", "stand(0)", 0, 400, 231),
        ("dad", "stand(0)", 270, 244, 546), ("lampboy", "sit", int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "boy" else 200, *(([int(v) for v in sys.argv[3:5]]) if len(sys.argv) > 4 and sys.argv[1] == "boy" else L["marks"]["lampboy"]))]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 900, "height": 700})
        page.on("pageerror", lambda e: print("[pageerror]", e))
        await page.goto("http://localhost:8765/tools/sprites.html")
        await page.wait_for_timeout(1200)
        out = await page.evaluate("""([folk, hz, full]) => {
            const L = window.lab; const res = { people: Object.keys(L.people || {}), poses: Object.keys(L.poses || {}), figs: [] };
            for (const [sid, pose, yaw, x, y] of folk) {
              try {
                const spec = L.people[sid]; if (!spec) { res.figs.push(null); continue; }
                const px = Math.round(L.BASE * spec.height * (y - hz) / (full - hz));
                const stand = (f) => L.poses.stand(spec, f), walk = (ph) => L.poses.walk(spec, ph);
                const p = pose === 'sit' ? (L.poses.sit ? L.poses.sit(spec, 0) : L.poses.stand(spec, 0)) : eval('(' + pose + ')');
                const sf = L.drawFigure(spec, p, +yaw, px); const cv = sf.toCanvas();
                res.figs.push({ url: cv.toDataURL(), ox: sf.ox, oy: sf.oy, x, y });
              } catch (e) { res.figs.push({ err: String(e) }); }
            }
            return res; }""", [FOLK, L["horizon"], L["full"]])
        await b.close()
    print("people:", out["people"], "poses:", out["poses"])
    names = ["back", "front"] if (not sys.argv[1:] or sys.argv[1] == "boy") else sys.argv[1:]
    im = Image.open(f"out/egypt-gallery/{names[0]}.png").convert("RGBA")
    for f in out["figs"]:
        if not f or "err" in f:
            print("skipped", f)
            continue
        fig = Image.open(io.BytesIO(base64.b64decode(f["url"].split(",")[1]))).convert("RGBA")
        im.alpha_composite(fig, (int(round(f["x"] - f["ox"])), int(round(f["y"] - f["oy"]))))
    for n in names[1:]:
        im.alpha_composite(Image.open(f"out/egypt-gallery/{n}.png").convert("RGBA"))
    im.convert("RGB").save("out/egypt-gallery-mock.png")
asyncio.run(main())

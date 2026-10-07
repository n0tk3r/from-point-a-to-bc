"""Looking-at tools for the living room. They write beside the scene's folder, not into it:
  python3 home_living_room_check.py cuts      -> out/home-living-room-check-cuts.png      the cut-outs on a loud ground
  python3 home_living_room_check.py layout    -> out/home-living-room-check-layout.png    layout.json drawn over the comp, a figure at every stand place and mark
  python3 home_living_room_check.py people [marks|things]   -> out/home-living-room-check-people-*.png
                                                 the family, drawn by the game's own code, standing in the room (needs the game served on port 8765)"""
import json, sys
from PIL import Image, ImageDraw

OUT = "out/home-living-room"


def cuts():
    names = ["desk", "piano", "table", "armchair", "screen-offline", "screen-login", "screen-map", "note"]
    try:
        Image.open(f"{OUT}/front.png")
        names.append("front")
    except Exception:
        pass
    sheet = Image.new("RGB", (800 * 2, 600 * 2), (255, 0, 255))
    for i, group in enumerate((["desk", "screen-login", "note"], ["piano"], ["table"], ["armchair"] + (["front"] if "front" in names else []))):
        bg = Image.new("RGBA", (800, 600), (255, 0, 255, 255) if i % 2 == 0 else (0, 255, 255, 255))
        for n in group:
            bg.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
        sheet.paste(bg.convert("RGB"), ((i % 2) * 800, (i // 2) * 600))
    sheet.save(f"{OUT}-check-cuts.png")
    print(f"{OUT}-check-cuts.png")


def layout():
    d = json.load(open(f"{OUT}/layout.json"))
    im = Image.open("out/home-living-room-comp.png").convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    g = ImageDraw.Draw(ov)
    g.polygon([tuple(p) for p in d["walk"]], outline=(0, 255, 0, 255))
    for b in d["blocked"]:
        g.polygon([tuple(p) for p in b], fill=(255, 0, 0, 60), outline=(255, 0, 0, 255))
    for p in d["planes"]:
        if isinstance(p.get("base"), (int, float)):
            g.line([(0, p["base"]), (800, p["base"])], fill=(255, 255, 0, 120))
            g.text((4, p["base"] - 10), p["id"], fill=(255, 255, 0, 255))

    def person(x, y, tall, color, label):
        k = (y - d["horizon"]) / (d["full"] - d["horizon"])
        h, w = tall * k, tall * k * 0.26
        g.rectangle([x - w / 2, y - h, x + w / 2, y], outline=color)
        g.ellipse([x - w * 0.3, y - h, x + w * 0.3, y - h + w * 0.6], outline=color)
        g.line([(x - 5, y), (x + 5, y)], fill=color, width=2)
        g.text((x + 3, y - h - 10), label, fill=color)
    for t in d["things"]:
        s = t["shape"]
        if "rect" in s:
            x, y, w, h = s["rect"]
            g.rectangle([x, y, x + w, y + h], outline=(0, 255, 255, 255))
        else:
            g.polygon([tuple(p) for p in s["poly"]], outline=(0, 255, 255, 255))
        person(t["stand"][0], t["stand"][1], 160, (255, 255, 255, 255), t["id"] + ":" + t["face"])
    for name, (x, y) in d["marks"].items():
        tall = {"mom": 160, "bigsis": 142, "lilsis": 108}.get(name, 108)
        person(x, y, tall, (255, 160, 255, 255), name)
    spots = dict(d.get("extras", {}))
    spots.update(d.get("extras", {}).get("scripted", {}))
    for k, v in spots.items():
        if isinstance(v, list) and len(v) == 2:
            g.ellipse([v[0] - 2, v[1] - 2, v[0] + 2, v[1] + 2], outline=(255, 128, 0, 255))
    im.alpha_composite(ov)
    im.convert("RGB").save(f"{OUT}-check-layout.png")
    print(f"{OUT}-check-layout.png")


def people():
    """The family, drawn by the game's own figure code (from the local game server, if it is running),
    standing in the painted room and sorted with the cut-outs by their baselines: to judge sizes.
    Nothing of the game is changed: the pictures are handed to the page as data."""
    import asyncio, base64
    from playwright.async_api import async_playwright
    d = json.load(open(f"{OUT}/layout.json"))
    planes = [["back", -1e9]]
    for p in d["planes"]:
        f = p.get("file") or p["states"]["login"]
        planes.append([f[:-4], 1e9 if p.get("plane") == "front" else p["base"]])
    data = {n: "data:image/png;base64," + base64.b64encode(open(f"{OUT}/{n}.png", "rb").read()).decode() for n, _ in planes}
    spots = sys.argv[2] if len(sys.argv) > 2 else "marks"
    if spots == "marks":
        folk = [["mom", "stand(0)", 20, *d["marks"]["mom"]], ["bigsis", "stand(0)", -30, *d["marks"]["bigsis"]], ["lilsis", "stand(0)", 40, *d["marks"]["lilsis"]]]
    else:                                                    # at the things: behind the table, at the door, the computer, the piano, the closet
        t = {x["id"]: x["stand"] for x in d["things"]}
        folk = [["mom", "stand(0)", 180, *t["door"]], ["lilsis", "stand(0)", 180, *t["window"]], ["bigsis", "stand(0)", 180, *t["piano"]],
                ["mom", "stand(0)", 180, *t["computer"]], ["lilsis", "stand(0)", 150, *t["closet"]], ["bigsis", "stand(0)", -90, *t["table"]], ["mom", "stand(0)", 90, *t["armchair"]],
                ["bigsis", "stand(0)", 180, 220, 430]]

    async def main():
        async with async_playwright() as p:
            b = await p.chromium.launch()
            page = await b.new_page(viewport={"width": 900, "height": 700})
            page.on("pageerror", lambda e: print("[pageerror]", e))
            await page.goto("http://localhost:8765/tools/sprites.html")
            await page.wait_for_timeout(1200)
            await page.evaluate("""async ([planes, data, folk, hz, full]) => {
                const L = window.lab;
                const load = (src) => new Promise((ok, no) => { const im = new Image(); im.onload = () => ok(im); im.onerror = no; im.src = src; });
                const cv = document.createElement('canvas'); cv.width = 800; cv.height = 600; cv.id = 'probe';
                cv.style.cssText = 'position:absolute;left:0;top:0;z-index:99;image-rendering:pixelated;width:800px;height:600px';
                const g = cv.getContext('2d'); g.imageSmoothingEnabled = false;
                const things = [];
                for (const [name, base] of planes) things.push({ y: +base, im: await load(data[name]), x: 0, top: 0 });
                for (const [sid, pose, yaw, x, y] of folk) {
                  const spec = L.people[sid], px = Math.round(L.BASE * spec.height * (y - hz) / (full - hz));
                  const stand = (f) => L.poses.stand(spec, f), walk = (ph) => L.poses.walk(spec, ph);
                  const sf = L.drawFigure(spec, eval('(' + pose + ')'), +yaw, px);
                  things.push({ y: +y, im: sf.toCanvas(), x: Math.round(+x - sf.ox), top: Math.round(+y - sf.oy) });
                }
                things.sort((a, b) => a.y - b.y);
                for (const t of things) g.drawImage(t.im, t.x, t.top);
                document.body.prepend(cv);
            }""", [planes, data, folk, d["horizon"], d["full"]])
            await (await page.query_selector("#probe")).screenshot(path=f"{OUT}-check-people-{spots}.png")
            await b.close()
    asyncio.run(main())
    print(f"{OUT}-check-people-{spots}.png")


if __name__ == "__main__":
    {"cuts": cuts, "layout": layout, "people": people}[sys.argv[1]]()

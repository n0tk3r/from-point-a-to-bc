"""The test that matters for the break room: the game's own people and Ranger's own frames in the room, at the size the
game draws them there, sorted with the room's cut-outs by their base lines as the engine sorts them. OFFICE-17D.

    python3 office_breakroom_people.py <out folder> [port] [art folder]

Draws, over the room as installed (keyed) in each state of the story:
  - Floyd (`suit4`) asleep on the couch (sitting, leaning back, his head down: PEOPLE-17 is making his slumped pose);
  - Jed (`agent-collar`, the banjo's hoop round his neck) in his chair, facing W along the counter at the pie;
  - three of the men in gray just in from the hall (`fromHall`), one at the snack machine, one at the counter;
  - Ranger (his painted frames, in his shades) on the fridge's top under the grille, on the microwave, on the counter by the
    pie (nibbling), at the sink (washing), at the board (sitting up), at the counter's end, and on the floor at the machine.
People are drawn with the game's own code, as people_on.py draws them (tools/sprites.html), from the game served on
`port` (default 8765: `python3 tools/serve.py 8765` from the top of the game)."""

import asyncio
import base64
import io
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.normpath(os.path.join(HERE, "..", ".."))
ART = os.path.join(GAME, "art", "scenes", "office-breakroom")
RANGER_DIR = os.path.join(GAME, "art", "scenes", "nevada-roadside")


async def _figures(folk, hz, full, port):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 900, "height": 700})
        page.on("pageerror", lambda e: print("[pageerror]", e))
        await page.goto(f"http://localhost:{port}/tools/sprites.html")
        await page.wait_for_timeout(1500)
        res = await page.evaluate("""([folk, hz, full]) => {
            const L = window.lab; const figs = [];
            for (const [sid, pose, yaw, x, y] of folk) {
              try {
                const spec = L.people[sid]; if (!spec) { figs.push({ err: 'nobody called ' + sid }); continue; }
                const px = Math.round(L.BASE * spec.height * (y - hz) / (full - hz));
                const stand = (f) => L.poses.stand(spec, f), walk = (ph) => L.poses.walk(spec, ph);
                const sf = L.drawFigure(spec, eval('(' + pose + ')'), +yaw, px); const cv = sf.toCanvas();
                figs.push({ url: cv.toDataURL(), ox: sf.ox, oy: sf.oy, x, y, px, who: sid });
              } catch (e) { figs.push({ err: sid + ': ' + String(e) }); }
            }
            return figs; }""", [folk, hz, full])
        await b.close()
    return res


def figures(folk, hz, full, port):
    """folk: [(who, x, y, yaw, pose)] -> [(image, left, top, x, y, px, who)]"""
    res = asyncio.run(_figures([[f[0], f[4], float(f[3]), float(f[1]), float(f[2])] for f in folk], hz, full, port))
    out = []
    for f in res:
        if "err" in f:
            print("skipped:", f["err"])
            continue
        im = Image.open(io.BytesIO(base64.b64decode(f["url"].split(",")[1]))).convert("RGBA")
        out.append((im, int(round(f["x"] - f["ox"])), int(round(f["y"] - f["oy"])), f["x"], f["y"], f["px"], f["who"]))
    return out


def ranger(set_, i, at, scale, face="E", shades=True):
    """Ranger's painted frame at a place, at the size the engine draws him there (in steps of two pixels of height, never
    more than a quarter over his painted size, hard pixels), mirrored when he faces W. -> (image, left, top)."""
    side = json.load(open(os.path.join(RANGER_DIR, "ranger.json")))
    name = (side["variants"]["shades"]["prefix"] if shades else "ranger-") + f"{set_}-{i}.png"
    im = Image.open(os.path.join(RANGER_DIR, name)).convert("RGBA")
    h = max(4, round(im.height * scale / 2) * 2)
    q = min(1.25, h / im.height)
    w2, h2 = max(1, round(im.width * q)), max(1, round(im.height * q))
    im = im.resize((w2, h2), Image.NEAREST)
    fx, fy = side["foot"][0] * q, side["foot"][1] * q
    if face == "W":
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        fx = w2 - fx
    return im, int(round(at[0] - fx)), int(round(at[1] - fy))


def base_row(base, x):
    if isinstance(base, (int, float)):
        return float(base)
    (x1, y1), (x2, y2) = base
    if abs(x2 - x1) < 1e-6:
        return max(y1, y2)
    t = (x - x1) / (x2 - x1)
    return y1 + (y2 - y1) * t


def scene(states=(), hide=(), people=(), rangers=(), port=8765, out=None, second=0):
    """The room as installed, in a state, with people and Ranger in it, sorted as the engine sorts them: back planes,
    then figures and based cut-outs by their rows, then the front plane."""
    L = json.load(open(os.path.join(ART, "layout.json")))
    im = Image.open(os.path.join(ART, "back.png")).convert("RGBA")
    alts = {p["id"]: p for p in L["planes"] if p.get("alt")}
    replaced = set()
    for s_ in states:
        replaced |= set(alts.get(s_, {}).get("replaces", []))
    shown = [p for p in L["planes"] if not (p.get("alt") and p["id"] not in states) and p["id"] not in replaced and p["id"] not in hide]
    clk = L["frames"]["clock"]
    for p in shown:
        if p.get("plane") == "back":
            im.alpha_composite(Image.open(os.path.join(ART, p["file"])).convert("RGBA"))
    c = Image.open(os.path.join(ART, clk["files"][second])).convert("RGBA")
    im.alpha_composite(c, (clk["at"][0] - clk["foot"][0], clk["at"][1] - clk["foot"][1]))
    figs = figures(people, L["horizon"], L["full"], port) if people else []
    items = []
    for (fim, left, top, x, y, px, who) in figs:
        items.append((y, "fig", (fim, left, top)))
    for (set_, i, at, scale, face, row) in rangers:
        rim, left, top = ranger(set_, i, at, scale, face)
        items.append((row, "fig", (rim, left, top)))
    based = [p for p in shown if isinstance(p.get("base"), list)]
    for p in based:
        pim = Image.open(os.path.join(ART, p["file"])).convert("RGBA")
        items.append((None, "cut", (pim, p["base"])))
    # each figure is behind a based cut-out when its feet are above that cut-out's base at its x
    figs_ = [it for it in items if it[1] == "fig"]
    cuts_ = [it for it in items if it[1] == "cut"]
    order = []
    for cut in cuts_:
        order.append(("cut", cut))
    drawn = []

    def cut_row_for(cut, x):
        return base_row(cut[2][1], x)
    # a simple painter: draw each cut-out after every figure that is behind it, figures in their own row order
    figs_.sort(key=lambda it: it[0])
    pending_cuts = list(cuts_)
    for f in figs_:
        fx = f[2][1] + f[2][0].width / 2
        for cut in list(pending_cuts):
            if f[0] >= cut_row_for(cut, fx):                 # the figure is in front of this cut-out: draw the cut-out first
                im.alpha_composite(cut[2][0])
                pending_cuts.remove(cut)
        fim, left, top = f[2]
        im.alpha_composite(fim, (left, top))
    for cut in pending_cuts:
        im.alpha_composite(cut[2][0])
    for p in shown:
        if p.get("plane") == "front":
            im.alpha_composite(Image.open(os.path.join(ART, p["file"])).convert("RGBA"))
    if out:
        im.convert("RGB").save(out)
    return im


def main(folder, port):
    os.makedirs(folder, exist_ok=True)
    L = json.load(open(os.path.join(ART, "layout.json")))
    mk, rm = L["marks"], L["ranger_marks"]
    floyd, jed = L["seats"]["floyd"], L["seats"]["jed"]
    # the engine's compass (js/engine/cast.js): S 0, E 90, N 180, W 270. Floyd faces E (his back to the couch's back), Jed W
    seated_floyd = ("suit4", floyd["at"][0], floyd["at"][1], 90, "L.poses.sit(spec, 0, { seat: 'chair', lean: -0.22, nod: 0.16 })")
    seated_jed = ("agent-collar", jed["at"][0], jed["at"][1], 270, "L.poses.sit(spec, 0, { seat: 'chair' })")
    hall = [("suit1", *mk["fromHall"][0], 0, "stand(0)"), ("suit2", *mk["fromHall"][1], 0, "stand(0)"), ("suit3", *mk["fromHall"][2], 0, "stand(0)")]

    def R(name, set_="stand", i=0, face=None):
        m = rm[name]
        return (set_, i, m["at"], m["scale"], face or m.get("face", "E"), m["at"][1])
    # 1. the opening of #19 from above: Floyd asleep, Jed watching the pie; Ranger come down onto the fridge
    scene(people=[seated_floyd, seated_jed], rangers=[R("fridge", "sit", 0)], port=port, out=f"{folder}/1-floyd-jed-ranger-on-fridge.png")
    # 2. Jed gone: Ranger on the microwave, then at the pie (nibbling), at the sink (washing), at the board (sitting up)
    scene(people=[seated_floyd], rangers=[R("micro", "stand", 0), R("counter", "nibble", 1), R("sink", "wash", 1), R("board", "sit", 0)],
          states=("pie-eaten",), port=port, out=f"{folder}/2-ranger-at-the-counter.png")
    # 3. the tin taken and washed, the schedule gone: Ranger at the counter's end and on the floor at the machine, the
    #    peanuts in the tray; three men in gray in from the hall
    scene(people=[seated_floyd] + hall, rangers=[R("counter-end", "stand", 0, "W"), R("vending", "sit", 0)], states=("pie-gone", "vending-peanuts", "door-open"),
          hide=("schedule",), port=port, out=f"{folder}/3-later-hall-and-floor.png", second=30)
    # 4. sizes: a man in gray at each place on the floor people use, and Ranger at every one of his
    floor = [("suit1", *L["stands"][k]["at"], 0, "stand(0)") for k in ("atfridge", "atsink", "atcounter", "atboard", "atcoffee", "atcouch", "attable", "vending")]
    scene(people=floor + [seated_floyd, seated_jed], rangers=[R(k, "stand", 0) for k in ("fridge", "micro", "counter-left", "counter", "sink", "board", "counter-end")],
          port=port, out=f"{folder}/4-sizes.png")
    # 5. the vent with Ranger's eyes; the plain room, nobody in it, in every state
    scene(states=("vent-eyes",), people=[seated_floyd, seated_jed], port=port, out=f"{folder}/5-eyes-in-the-vent.png")
    scene(port=port, out=f"{folder}/6-state-first.png")
    scene(states=("pie-eaten", "vent-eyes", "vending-peanuts", "door-open"), port=port, out=f"{folder}/7-state-later.png", second=15)
    scene(states=("pie-gone", "vending-taken"), hide=("schedule",), port=port, out=f"{folder}/8-state-end.png", second=45)
    # 9. Floyd sunk into the cushions at PEOPLE-17's COUCH_SEAT (42 cm: 0.24 of a grown person) instead of on their top
    #    (45.9 cm, as painted), and Jed at BREAK_CHAIR_SEAT (45 cm), to see that both read
    sunk_floyd = ("suit4", floyd["at"][0], floyd["at"][1], 90, "L.poses.sit(spec, 0, { seat: 0.24, lean: -0.22, nod: 0.16 })")
    jed45 = ("agent-collar", jed["at"][0], jed["at"][1], 270, "L.poses.sit(spec, 0, { seat: 45 / 175 })")
    scene(people=[sunk_floyd, jed45], rangers=[R("counter", "nibble", 0)], port=port, out=f"{folder}/9-seats-at-people17s-heights.png")
    print("written into", folder)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "out/office-breakroom-people", int(sys.argv[2]) if len(sys.argv) > 2 else 8765)

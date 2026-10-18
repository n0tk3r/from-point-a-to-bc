"""The game's own people (and Ranger's painted frames) standing, sitting and perching in the Office's rooms, at exactly
the size the game draws them there: the test that matters (README, "The game's people in the picture"). OFFICE-17C.

    python3 office_people.py <picture.png> <spec.json> <out.png> [port]
    python3 office_people.py shots [port] [folder]   both rooms as installed, people at the marks, in each state
                                                     (into out/office-shots/, or the folder given)

spec.json: {"horizon": .., "full": .., "folk": [
    {"who": "suit1", "pose": "sit", "yaw": 270, "at": [x, y]},                  seated: `at` is the floor under the hips
    {"who": "grandpajoe-standing", "pose": "stand(0)", "yaw": 0, "at": [x, y], "scale": 1.08},   a scale of his own
    {"ranger": "peek-0", "at": [x, y], "scale": 1.1, "flip": false},             one of Ranger's painted frames
    ...], "planes": [{"file": "cut-out.png", "base": 458}, {"file": "..", "base": [[x1, y1], [x2, y2]]},
                     {"file": "..", "plane": "back"}, {"file": "..", "plane": "front"}, ...],
    "over": ["cut-out.png", ...], "over_after": {"<index>": ["cut-out.png"]}}
`pose`: "stand(0)", "walk(0.3)", "sit" (the rig's sitPose on a chair), or any expression of the sprites page's `L`
("sit(0, {seat: 0.377})": on a seat that high, a share of a grown-up's height).
`planes` are sorted with the figures as the engine sorts them (docs/DESIGN.md, section 3): a back plane under everybody,
a front plane over everybody, and a cut-out with a base over every figure whose feet (or `sort` row) are above its base
(a row, or a line: which side of it the feet are on), in the order listed. Without `planes`: figures back to front by
`sort` (default: their feet's row), the cut-outs in `over` over everybody, those in `over_after` straight after the
figure of that index.
Needs the game served (python3 tools/serve.py <port>, default 8879) and Playwright with its Chromium."""
import asyncio
import base64
import io
import json
import os
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.normpath(os.path.join(HERE, "..", ".."))
RANGER = os.path.join(GAME, "art", "scenes", "nevada-roadside")


def ranger_frame(name, scale, flip=False):
    meta = json.load(open(os.path.join(RANGER, "ranger.json")))
    im = Image.open(os.path.join(RANGER, f"ranger-{name}.png")).convert("RGBA")
    fx, fy = meta["foot"]
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        fx = im.width - fx
    if abs(scale - 1) > 1e-3:
        w, h = max(1, round(im.width * scale)), max(1, round(im.height * scale))
        im = im.resize((w, h), Image.NEAREST)
        fx, fy = fx * scale, fy * scale
    return im, fx, fy


async def draw_people(folk, hz, full, port):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        page = await b.new_page(viewport={"width": 900, "height": 700})
        page.on("pageerror", lambda e: print("[pageerror]", e))
        await page.goto(f"http://localhost:{port}/tools/sprites.html")
        await page.wait_for_timeout(1500)
        res = await page.evaluate("""([folk, hz, full]) => {
            const L = window.lab; const out = [];
            for (const f of folk) {
              if (f.ranger) { out.push(null); continue; }
              try {
                const spec = L.people[f.who]; if (!spec) { out.push({ err: 'nobody called ' + f.who }); continue; }
                const s = f.scale != null ? f.scale : (f.at[1] - hz) / (full - hz);
                const px = Math.round(L.BASE * spec.height * s);
                const stand = (k) => L.poses.stand(spec, k), walk = (ph) => L.poses.walk(spec, ph);
                const sit = (k = 0, o = {}) => L.poses.sit(spec, k, o);
                const pose = f.pose === 'sit' ? sit(0) : eval('(' + (f.pose || 'stand(0)') + ')');
                const sf = L.drawFigure(spec, pose, +(f.yaw || 0), px); const cv = sf.toCanvas();
                out.push({ url: cv.toDataURL(), ox: sf.ox, oy: sf.oy, px });
              } catch (e) { out.push({ err: String(e) }); }
            }
            return out; }""", [folk, hz, full])
        await b.close()
    return res


def main():
    pic, spec_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    port = sys.argv[4] if len(sys.argv) > 4 else "8879"
    spec = json.load(open(spec_path))
    folk = spec["folk"]
    res = asyncio.run(draw_people(folk, spec["horizon"], spec["full"], port))
    im = Image.open(pic).convert("RGBA")
    order = sorted(range(len(folk)), key=lambda i: folk[i].get("sort", folk[i]["at"][1]))
    after = {int(k): v for k, v in spec.get("over_after", {}).items()}
    sizes = []
    planes = spec.get("planes")
    if planes is not None:
        def behind(f, p):                                     # are this figure's feet above the cut-out's base?
            x, y = f["at"][0], f.get("sort", f["at"][1])
            b = p["base"]
            if isinstance(b, (int, float)):
                return y < b
            (x1, y1), (x2, y2) = b
            t = 0.0 if x2 == x1 else (x - x1) / (x2 - x1)
            return y < y1 + (y2 - y1) * t
        based = [p for p in planes if "base" in p]
        slot = {}
        for i in range(len(folk)):
            k = next((j for j, p in enumerate(based) if behind(folk[i], p)), len(based))
            slot.setdefault(k, []).append(i)
        seq = [("p", p) for p in planes if p.get("plane") == "back" or ("base" not in p and p.get("plane") != "front")]
        for j in range(len(based) + 1):
            seq += [("f", i) for i in sorted(slot.get(j, []), key=lambda i: folk[i].get("sort", folk[i]["at"][1]))]
            if j < len(based):
                seq.append(("p", based[j]))
        seq += [("p", p) for p in planes if p.get("plane") == "front"]
    else:
        seq = [("f", i) for i in order]
    for kind, i in seq:
        if kind == "p":
            im.alpha_composite(Image.open(i["file"]).convert("RGBA"))
            continue
        f, r = folk[i], res[i]
        if f.get("ranger"):
            fr, fx, fy = ranger_frame(f["ranger"], f.get("scale", 1.0), f.get("flip", False))
            im.alpha_composite(fr, (int(round(f["at"][0] - fx)), int(round(f["at"][1] - fy))))
            sizes.append((f["ranger"], round(34 * f.get("scale", 1.0))))
        elif r and "err" not in r:
            fig = Image.open(io.BytesIO(base64.b64decode(r["url"].split(",")[1]))).convert("RGBA")
            im.alpha_composite(fig, (int(round(f["at"][0] - r["ox"])), int(round(f["at"][1] - r["oy"]))))
            sizes.append((f["who"], r["px"]))
        elif r:
            print("skipped:", f.get("who"), r["err"])
        for n in after.get(i, []):
            im.alpha_composite(Image.open(n).convert("RGBA"))
    for n in spec.get("over", []):
        im.alpha_composite(Image.open(n).convert("RGBA"))
    im.convert("RGB").save(out)
    print(out, sizes)


# ---------------------------------------------------------------- the shots: both rooms as installed, people at the marks
def _shot(scene, files, folk, out, port, layout):
    """One picture: the installed back and the named cut-outs (sorted with the people as the layout's planes say),
    the folk at their marks. -> the sizes drawn."""
    folder = os.path.join(GAME, "art", "scenes", scene)
    planes = []
    for p in layout["planes"]:
        name = p["file"][:-4]
        if name not in files:
            continue
        q = {"file": os.path.join(folder, p["file"])}
        if "base" in p:
            q["base"] = p["base"]
        else:
            q["plane"] = p.get("plane", "back")
        planes.append(q)
    spec = {"horizon": layout["horizon"], "full": layout["full"], "folk": folk, "planes": planes}
    tmp = out + ".json"
    json.dump(spec, open(tmp, "w"))
    sys.argv = [sys.argv[0], os.path.join(folder, "back.png"), tmp, out, port]
    main()
    os.remove(tmp)


def shots(port="8879", outdir=None):
    """The test that matters: the game's own people (and Ranger's frames) in both rooms, at the marks, in each state."""
    outdir = outdir or os.path.join(HERE, "out", "office-shots")
    os.makedirs(outdir, exist_ok=True)
    R = json.load(open(os.path.join(GAME, "art", "scenes", "office-room", "layout.json")))
    m, st = R["marks"], R["stands"]
    start = ["vent", "thermostat-72", "intercom", "door", "doorframe", "chair-corner", "table", "questionnaire", "plant", "front"]
    _shot("office-room", start, [
        {"who": "grandpajoe-seat-loose", "pose": "sit", "yaw": 90, "at": m["joe"]["at"]},
        {"who": "suit1", "pose": "sit", "yaw": 270, "at": m["dale"]["at"]},
        {"who": "suit2", "pose": "sit", "yaw": 270, "at": m["merle"]["at"]},
    ], os.path.join(outdir, "room-1-interview.png"), port, R)
    warm = ["vent-eyes", "thermostat-77", "intercom", "door", "doorframe", "chair-corner", "table", "plant", "front"]
    _shot("office-room", warm, [
        {"who": "grandpajoe", "pose": "stand(0)", "yaw": 0, "at": m["chair"]["at"], "scale": m["chair"]["scale"], "sort": m["chair"]["base"]},
    ], os.path.join(outdir, "room-2-on-the-chair-eyes-77.png"), port, R)
    _shot("office-room", ["vent", "thermostat-81", "intercom", "door", "doorframe", "chair-corner", "table", "plant-droop", "front"], [
        {"ranger": "reach-0", "at": m["vent"]["at"], "scale": m["vent"]["scale"], "sort": m["vent"]["base"]},
        {"who": "grandpajoe", "pose": "stand(0)", "yaw": 270, "at": st["thermostat"]["at"]},
    ], os.path.join(outdir, "room-3-ranger-on-the-seat-81-droop.png"), port, R)
    _shot("office-room", ["vent", "thermostat-81", "intercom-lit", "door-open", "doorframe", "chair-corner", "table", "plant-droop", "front"], [
        {"who": "jolene", "pose": "stand(0)", "yaw": 90, "at": m["opal"]},
        {"who": "grandpajoe", "pose": "stand(0)", "yaw": 270, "at": st["atjoe"]["at"]},
        {"who": "suit3", "pose": "stand(0)", "yaw": 0, "at": m["hall"]},
    ], os.path.join(outdir, "room-4-opal-door-open-lit.png"), port, R)
    _shot("office-room", start, [
        {"who": "suit4", "pose": "stand(0)", "yaw": 0, "at": st["front"]["at"]},
        {"who": "suit3", "pose": "stand(0)", "yaw": 0, "at": st["atmirror"]["at"]},
        {"who": "grandpajoe", "pose": "stand(0)", "yaw": 0, "at": st["thermostat"]["at"]},
        {"who": "suit1", "pose": "stand(0)", "yaw": 0, "at": st["atbasket"]["at"]},
        {"who": "jolene", "pose": "stand(0)", "yaw": 0, "at": st["atplant"]["at"]},
        {"who": "suit2", "pose": "stand(0)", "yaw": 0, "at": st["atlamp"]["at"]},
    ], os.path.join(outdir, "room-5-sizes.png"), port, R)

    P = json.load(open(os.path.join(GAME, "art", "scenes", "office-property", "layout.json")))
    m, st = P["marks"], P["stands"]
    seat = m["opal"]["seat"]
    first = ["vent", "door", "wall", "banjo", "front"]
    _shot("office-property", first, [
        {"who": "jolene", "pose": "sit(0, {seat: %s})" % seat, "yaw": 180, "at": m["opal"]["at"]},
    ], os.path.join(outdir, "prop-1-opal-at-her-window.png"), port, P)
    _shot("office-property", ["vent-eyes", "door", "wall", "receipt", "banjo", "front"], [
        {"who": "jolene", "pose": "sit(0, {seat: %s})" % seat, "yaw": 180, "at": m["opal"]["at"]},
        {"ranger": "stand-0", "at": m["vent"]["at"], "scale": m["vent"]["scale"], "sort": m["vent"]["base"], "flip": True},
    ], os.path.join(outdir, "prop-2-receipt-eyes-ranger-on-the-shelf.png"), port, P)
    _shot("office-property", ["vent", "door-open", "wall", "front"], [
        {"who": "jolene", "pose": "stand(0)", "yaw": 270, "at": m["banjo"]["stand"]},
        {"who": "suit3", "pose": "stand(0)", "yaw": 0, "at": m["hallwindow"]},
        {"who": "suit1", "pose": "stand(0)", "yaw": 0, "at": m["hall"]},
    ], os.path.join(outdir, "prop-3-banjo-gone-door-open-hall.png"), port, P)
    _shot("office-property", first, [
        {"who": "suit4", "pose": "stand(0)", "yaw": 0, "at": st["front"]["at"]},
        {"who": "grandpajoe", "pose": "stand(0)", "yaw": 0, "at": st["atright1"]["at"]},
        {"who": "suit2", "pose": "stand(0)", "yaw": 0, "at": st["door"]["at"]},
        {"who": "jolene", "pose": "stand(0)", "yaw": 0, "at": st["atwindow"]["at"]},
        {"who": "suit1", "pose": "stand(0)", "yaw": 0, "at": st["atleft0"]["at"]},
        {"who": "suit3", "pose": "stand(0)", "yaw": 0, "at": st["banjo"]["at"]},
    ], os.path.join(outdir, "prop-4-sizes.png"), port, P)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "shots":
        shots(*(sys.argv[2:4] or ["8879"]))
    else:
        main()

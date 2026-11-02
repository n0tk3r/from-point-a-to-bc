"""PAINT-21F: checks on the women's hall (edo-hall) and its pictures, as painted (out/edo-hall/) or installed
(art/scenes/edo-hall/), and the check pictures.

    python3 edo_hall_check.py out|art [shots_dir]

What it holds (each a line; the exit code is the number of failures): every picture of the plan (postimp_plans.py) is
there and no other, 800 x 600; the backdrops and cut-outs a palette with a clear colour (the cut-outs) and hard edges; the
light pictures RGBA with a soft alpha; layout.json complete (horizon, full, view, walk, blocked, marks, stands with
grownup_px, things, planes, states, bars, hum, door, fx); every mark on the stage and inside the walk (Ryōkai's outside,
behind the lattice, as he must be); every thing of ROUND-21's list for edo-hall with a shape or a stand; the light: the
hum NOT lit at k 0, lit from k_hum to k 1 (the wall's bars slid up as the scene slides them), the floor's bars on the
floor at k 0, inside their clips; the hum on the bare wall between its keep columns, above the wall's foot; nobody at the
marks by the hum hides it (the line of sight from the lens); the lattice's gaps clear in its cut-out, Ryōkai's face
behind them; and the pictures to look at (the layout drawn over the composed hall at k 0, k_hum and k 1)."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

from postimp_plans import PLANS

ID = "edo-hall"
WHERE = sys.argv[1] if len(sys.argv) > 1 else "out"
FOLDER = f"out/{ID}" if WHERE == "out" else f"../../art/scenes/{ID}"
SHOTS = sys.argv[2] if len(sys.argv) > 2 else f"out/{ID}-check"
FAILS = []
THINGS = ["lattice", "bars", "wall", "hum", "cabinet", "lamp", "incense", "flowers", "slips", "posts", "ceiling", "mats", "doorway", "ume", "ryokai"]
MARKS = ["door", "ume", "mats", "hum", "cabinet", "lattice", "ryokai"]


def ok(cond, what):
    print(("ok    " if cond else "FAIL  ") + what)
    if not cond:
        FAILS.append(what)
    return cond


def poly_mask(poly):
    m = Image.new("L", (800, 600), 0)
    ImageDraw.Draw(m).polygon([tuple(p) for p in poly], fill=255)
    return np.asarray(m) > 0


def inside(pt, poly):
    m = poly_mask(poly)
    x, y = int(round(pt[0])), int(round(pt[1]))
    return 0 <= x < 800 and 0 <= y < 600 and bool(m[y, x])


def rgba(name):
    return np.asarray(Image.open(os.path.join(FOLDER, name)).convert("RGBA")).astype(np.float32) / 255


def main():
    os.makedirs(SHOTS, exist_ok=True)
    plan = PLANS[ID]
    L = json.load(open(os.path.join(FOLDER, "layout.json")))
    # the files
    names = ["back"] + plan["planes"] + list(plan["alt"].keys())
    files = sorted(f for f in os.listdir(FOLDER) if f.endswith(".png"))
    frames = [f for f in files if f.startswith("bars-")]
    ok(sorted([n + ".png" for n in names] + frames) == sorted(files), f"the files are the plan's: {len(files)} ({', '.join(files)})")
    ok(sorted(frames) == ["bars-air.png", "bars-floor.png", "bars-wall.png"], "the three light pictures: bars-wall, bars-floor, bars-air")
    for n in names:
        im = Image.open(os.path.join(FOLDER, n + ".png"))
        ok(im.size == (800, 600), f"{n}.png 800 x 600")
        ok(im.mode == "P", f"{n}.png a palette picture")
        if n not in ("back", "dusk"):
            a = np.asarray(im.convert("RGBA"))[..., 3]
            ok("transparency" in im.info and set(np.unique(a)) <= {0, 255}, f"{n}.png: a clear colour, hard edges")
    for f in frames:
        im = Image.open(os.path.join(FOLDER, f))
        a = np.asarray(im.convert("RGBA"))[..., 3]
        ok(im.size == (800, 600) and im.mode == "RGBA" and len(np.unique(a)) > 8, f"{f}: 800 x 600 RGBA, a soft alpha (light)")
    # layout.json
    for k in ("horizon", "full", "view", "walk", "blocked", "marks", "stands", "things", "planes", "states", "bars", "hum", "door", "fx"):
        ok(k in L, f"layout.json has `{k}`")
    walk = L["walk"]
    for m in MARKS:
        ok(m in L["marks"], f"mark `{m}`")
    for m, v in L["marks"].items():
        x, y = v["at"]
        ok(0 <= x < 800 and 0 <= y < 600, f"mark `{m}` on the stage {v['at']}")
        if m != "ryokai":
            ok(inside(v["at"], walk), f"mark `{m}` inside the walk")
    ok(not inside(L["marks"]["ryokai"]["at"], walk), "Ryōkai's mark outside the walk (he is outside the hall, behind the lattice)")
    for k, v in L["stands"].items():
        ok(80 <= v["grownup_px"] <= 215, f"stand `{k}`: a grown-up {v['grownup_px']} px")
    for t in THINGS:
        th = L["things"].get(t)
        ok(th is not None and (isinstance(th.get("poly"), (list, str)) or "stand" in th), f"thing `{t}` with a shape or a stand")
    # the light: the hum dark at k 0, lit from k_hum to k 1
    B = L["bars"]
    wall = rgba(B["wall"]["src"])[..., 3]
    hx, hy = L["hum"]["at"]
    rise = B["wall"]["rise_px"]
    clip = poly_mask(B["wall"]["clip"])

    def lit_at(k):
        # the layer is slid up by k * rise: the hum's pixel shows the layer's pixel k * rise below it
        yy = int(round(hy + k * rise))
        return float(wall[min(599, yy), int(round(hx))]) if clip[int(round(hy)), int(round(hx))] else 0.0
    ok(lit_at(0.0) < 0.1, f"the hum is not in the light at k 0 (alpha {lit_at(0.0):.2f}): the bars climb to it")
    for k in (B["k_hum"], (B["k_hum"] + 1) / 2, 1.0):
        ok(lit_at(k) > 0.5, f"the hum is in a bar of light at k {k:.2f} (alpha {lit_at(k):.2f})")
    fl = rgba(B["floor"]["src"])[..., 3]
    fclip = poly_mask(B["floor"]["clip"])
    ok((fl * fclip).sum() > 2000, f"the floor's bars lie on the floor at k 0 ({int((fl * fclip).sum())} px of light)")
    ok((wall * clip).sum() > 500, f"the wall's bars show on the wall at k 0 ({int((wall * clip).sum())} px of light)")
    # the hum and the door
    D = L["door"]
    ok(D["keep"][0] < hx < D["keep"][1], f"the hum {L['hum']['at']} between the door's keep columns {D['keep']}")
    ok(D["base"] > hy, f"the door's base (the wall's foot, row {D['base']}) below the hum")
    ok(D["r_coin"] < D["r_hand"] and D["keep"][1] - D["keep"][0] > 2 * D["r_hand"] * D["wide"], f"a coin's door {D['r_coin']} px, a hand's {D['r_hand']} px, fits the bare wall")
    # nobody at the marks by the hum hides it: the people's places against the line from the lens to the hum (from the view)
    view = L["view"]
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from room import View
    V = View(**view)
    hum_cm = L["hum"]["room_cm"]
    for m, cm in (("hum", 168), ("big", 160), ("lil", 122), ("humsit", 95)):
        X, Z = V.floor_at(*L["marks"][m]["at"])
        t = (hum_cm[0] - V.cam_x) / (X - V.cam_x)
        zw = V.cam_z + (Z - V.cam_z) * t
        hide = V.eye - (V.eye - cm) * t
        clear = abs(zw - hum_cm[2]) > 30 or hide < hum_cm[1] - 12
        ok(clear, f"`{m}` ({cm} cm tall) does not hide the hum (hides the wall at Z {zw:.0f} up to {hide:.0f} cm; the hum Z {hum_cm[2]:.0f}, {hum_cm[1]:.0f} up)")
    # the lattice: its gaps clear; Ryōkai's face behind them
    lat = rgba("lattice.png")[..., 3]
    fx, fy = L["ryokai_face"]["at"]
    win = lat[int(fy) - 12:int(fy) + 12, int(fx) - 10:int(fx) + 10]
    ok((win < 0.5).sum() > 40, f"the lattice is open (its gaps clear) round Ryōkai's face at {L['ryokai_face']['at']}: {(win < 0.5).sum()} clear px")
    # the pictures: the layout over the composed hall at k 0, k_hum and k 1
    def composed(k):
        back = rgba("back.png")[..., :3]

        def screen(dst, src, op, clipm, dx=0.0, dy=0.0):
            import cv2
            M = np.float32([[1, 0, dx], [0, 1, dy]])
            s = cv2.warpAffine(src, M, (800, 600), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
            a = s[..., 3:4] * op * (clipm[..., None] if clipm is not None else 1)
            return dst * (1 - a) + (1 - (1 - dst) * (1 - s[..., :3])) * a
        pic = screen(back, rgba(B["wall"]["src"]), 1.0, clip, 0, -k * rise)
        if k < B["floor"]["k_floor"]:
            t = k / B["floor"]["k_floor"]
            f0, f1 = B["floor"]["fade"]
            op = 1.0 - np.clip((k - f0) / max(1e-6, f1 - f0), 0, 1)
            pic = screen(pic, rgba(B["floor"]["src"]), op, fclip, B["floor"]["to"][0] * t, B["floor"]["to"][1] * t)
        pic = screen(pic, rgba(B["air"]["src"]), 1.0 if k <= 0.8 else max(0.0, 1 - (k - 0.8) / 0.2), None)
        for p in L["planes"]:
            c = rgba(p["src"])
            a = (c[..., 3:4] >= 0.5).astype(np.float32)
            pic = pic * (1 - a) + c[..., :3] * a
        return pic
    for k, nm in ((0.0, "k0"), (B["k_hum"], "khum"), (1.0, "k1")):
        im = Image.fromarray((np.clip(composed(k), 0, 1) * 255).astype(np.uint8))
        im.save(os.path.join(SHOTS, f"{ID}-{WHERE}-{nm}.png"))
        if nm == "khum":
            d = ImageDraw.Draw(im)
            d.polygon([tuple(p) for p in walk], outline=(255, 230, 60))
            for b in L["blocked"]:
                d.polygon([tuple(p) for p in b["poly"]], outline=(255, 140, 40))
            for t, th in L["things"].items():
                if isinstance(th.get("poly"), list) and len(th["poly"]) >= 3:
                    d.polygon([tuple(p) for p in th["poly"]], outline=(60, 220, 255))
            for m, v in L["marks"].items():
                x, y = v["at"]
                d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 60, 60))
                d.text((x + 4, y - 10), m, fill=(255, 255, 255))
            for r in (D["r_coin"], D["r_hand"]):
                d.ellipse([hx - r * D["wide"], hy - r, hx + r * D["wide"], hy + r], outline=(255, 255, 255))
            d.line([(D["keep"][0], hy - 40), (D["keep"][0], hy + 40)], fill=(255, 0, 255))
            d.line([(D["keep"][1], hy - 40), (D["keep"][1], hy + 40)], fill=(255, 0, 255))
            d.polygon([tuple(p) for p in B["wall"]["clip"]], outline=(255, 120, 200))
            d.polygon([tuple(p) for p in B["floor"]["clip"]], outline=(200, 120, 255))
            fxx, fyy = L["ryokai_face"]["at"]
            d.ellipse([fxx - 6, fyy - 6, fxx + 6, fyy + 6], outline=(255, 255, 0))
            im.save(os.path.join(SHOTS, f"{ID}-{WHERE}-layout.png"))
    print(f"{len(FAILS)} failure{'s' if len(FAILS) != 1 else ''}; pictures in {SHOTS}")
    return len(FAILS)


if __name__ == "__main__":
    sys.exit(main())

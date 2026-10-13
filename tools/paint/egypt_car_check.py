"""Checks on the finished inside of the wagon (python3 egypt_car_check.py [folder] [out prefix]): layout.json drawn over
the picture, and the numbers that must hold. The folder is the raw painting (out/egypt-car, the default) or the keyed
one the game shows (../../art/scenes/egypt-car from the game's tools/paint, say).

  - every shape, mark and line of layout.json drawn over the picture, in the first state (the glovebox shut, the visor
    up) and the later ones (the visor down; the glovebox open, with the map and empty): the things' shapes, the walk
    patch and the mark, the words box, the glass, the fx marks (the river's and the dust's patches, the steam's foot,
    height and lean, the freshener's pin), the band's top -> <prefix>.png, <prefix>-later.png;
  - the band: no shape reaches below row 548 but the door's, the manual's and the key's; the bench's middle (x 380 to
    470) at the bottom is under no shape; (430, 590) is under no shape; the walk patch and the mark are the brief's;
  - nothing overlaps the glovebox, shut or open (the dust, on the front plane, is clear of it too);
  - the cut-outs: 800 x 600 each, as the backdrop, and the backdrop whole (no see-through pixel); under each cut-out the
    backdrop shows what is there without it; the glovebox's two open states have the same door, pixel for pixel (only
    the map goes); with the raw painting, the backdrop and each state's cut-outs laid together give back that state's
    own painting (out/egypt-car-work/2-*.png) round every cut-out's edge, so the cut-outs sit exactly on it;
  - the glass: no pixel of the car (a pillar, the dash, the mirror, the wheel) inside the polygon, and how much glass is
    outside it (from the painting's own record, out/egypt-car-work/masks.npz); the steam's clip is the glass;
  - Dad's words: a long line of his, bold yellow (#ffd34d) with a dark outline, centred on x 400, its bottom edge on row
    150, at most 400 pixels wide, laid over the words box with the visor up and down -> <prefix>-words.png."""

import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from egypt_car_layout import inside_poly

folder = sys.argv[1] if len(sys.argv) > 1 else "out/egypt-car"
prefix = sys.argv[2] if len(sys.argv) > 2 else "out/egypt-car-check"
WORK = "out/egypt-car-work"
W, H = 800, 600
BAND = 548
L = json.load(open(f"{folder}/layout.json"))
problems = []
raw = os.path.abspath(folder) == os.path.abspath("out/egypt-car")


def say(ok, text):
    print(("  ok    " if ok else "  WRONG ") + text)
    if not ok:
        problems.append(text)


def rgba(name):
    return np.asarray(Image.open(f"{folder}/{name}.png").convert("RGBA"))


def alpha(name):
    return rgba(name)[..., 3] > 127


def laid(names):
    im = Image.open(f"{folder}/{names[0]}.png").convert("RGBA")
    for n in names[1:]:
        im.alpha_composite(Image.open(f"{folder}/{n}.png").convert("RGBA"))
    return im


things = {t["id"]: t for t in L["things"]}
shapes = {}                                                   # every clickable shape, by name (the other states' too)
for t in L["things"]:
    shapes[t["id"]] = inside_poly(t["shape"]["poly"])
    for k in ("down", "open"):
        if k in t:
            shapes[f"{t['id']} ({k})"] = inside_poly(t[k]["poly"])

# ---- the fixed numbers
print("the fixed numbers")
order = ["windshield", "visor", "rearview", "freshener", "door", "manual", "seat", "glovebox", "cupholder", "wheel", "radio", "gauges",
         "horn", "gears", "key"]
say([t["id"] for t in L["things"]] == order, f"the things, in the master brief's order: {', '.join(t['id'] for t in L['things'])}")
say(L["walk"] == [[410, 580], [450, 580], [450, 598], [410, 598]], f"walk {L['walk']}")
say(L["marks"] == {"default": [430, 590]}, f"marks {L['marks']}")
say(L["blocked"] == [] and L["exits"] == [], "blocked [] and exits []")
say(all("stand" not in t for t in L["things"]), "no thing has a stand")
say("down" in things["visor"] and "open" in things["glovebox"], "the visor has its 'down' shape, the glovebox its 'open' one")
planes = {p["id"]: p for p in L["planes"]}
say(planes.get("glovebox") == {"id": "glovebox", "file": "glovebox-shut.png", "states": {"shut": "glovebox-shut.png", "map": "glovebox-map.png",
                                                                                       "empty": "glovebox-empty.png"}, "base": 600}, "plane glovebox")
say(planes.get("visor") == {"id": "visor", "file": "visor-up.png", "states": {"up": "visor-up.png", "down": "visor-down.png"}, "base": 600}, "plane visor")
say(planes.get("freshener") == {"id": "freshener", "file": "freshener.png", "plane": "front"}, "plane freshener")
say(L["words"]["box"] == [200, 70, 600, 150] and L["words"]["color"] == "#ffd34d", f"words box {L['words']['box']}")
fx = {m["id"]: m for m in L["fx"]}
say([m["id"] for m in L["fx"]] == ["river", "steam", "freshener", "dust"], f"fx in order: {[m['id'] for m in L['fx']]}")
st = fx["steam"]
say(st["type"] == "smoke" and st["plane"] == "back" and st["clip"] == L["glass"], "steam: smoke, plane back, clip = the glass")
fr = fx["freshener"]
say(fr["type"] == "sway" and fr["plane"] == "freshener" and fr["anchor"] == "top" and isinstance(fr["at"], list), f"freshener: sway from the knot {fr['at']}")
say(fx["dust"]["plane"] == "front" and fx["river"]["plane"] == "back", "dust on the front plane, the river's light on the back one")

# ---- the band, the mark, the bench's middle
print("the band (rows 548 to 600: the way out)")
for name, m in shapes.items():
    rows = np.nonzero(m.any(axis=1))[0]
    low = int(rows.max()) if len(rows) else -1
    allowed = name.split(" ")[0] in ("door", "manual", "key")
    if low >= BAND:
        say(allowed, f"{name}: down to row {low}" + (" (allowed into the band)" if allowed else " (into the band)"))
covered = np.zeros((H, W), bool)
for m in shapes.values():
    covered |= m
say(not covered[590, 430], "(430, 590) is under no shape")
say(not covered[BAND:, 380:471].any(), "the bench's middle at the bottom (x 380 to 470, rows 548 to 600) is under no shape")
band_free = (~covered[BAND:].any(axis=0)).mean()
say(band_free >= 0.30, f"{band_free:.0%} of the band's length has no shape in it from row 548 to the bottom (the way out may be clicked there)")

# ---- each shape goes round what is painted of its thing (the painting's own record of what each ray met)
if os.path.exists(f"{WORK}/masks.npz"):
    print("the shapes round the things as painted")
    z = np.load(f"{WORK}/masks.npz")
    for name, m in shapes.items():
        key = {"visor (down)": "x-visor-down", "glovebox (open)": "x-glovebox-open"}.get(name, "m-" + name)
        if key not in z.files:
            continue
        thing = z[key].copy()
        if name.split(" ")[0] not in ("door", "manual", "key"):
            thing[BAND:] = False
        got = (thing & m).sum() / max(1, thing.sum())
        spill = int((m & ~thing).sum())
        say(got >= 0.95, f"{name}: its shape holds {got:.1%} of its {int(thing.sum())} px ({spill} px of the shape are round it, not on it)")

# ---- the glovebox, alone
print("the glovebox")
for gname in ("glovebox", "glovebox (open)"):
    g = shapes[gname]
    over = {name: int((g & m).sum()) for name, m in shapes.items() if not name.startswith("glovebox") and (g & m).any()}
    say(not over, f"nothing overlaps {gname}" + (f": {over}" if over else ""))
    dust = inside_poly(fx["dust"]["poly"])
    say(not (dust & g).any(), f"the dust is clear of {gname}")
gs = np.nonzero(shapes["glovebox"].any(axis=0))[0], np.nonzero(shapes["glovebox"].any(axis=1))[0]
print(f"        shut: x {gs[0].min()}..{gs[0].max()}, y {gs[1].min()}..{gs[1].max()} (the brief: about x 546 to 736, y 364 to 446)")

# ---- the cut-outs and the backdrop
print("the cut-outs")
back = rgba("back")
say(back.shape[:2] == (H, W) and (back[..., 3] == 255).all(), "back.png: 800 x 600, whole (no see-through pixel)")
cuts = ["glovebox-shut", "glovebox-map", "glovebox-empty", "visor-up", "visor-down", "freshener"]
masks = {}
for n in cuts:
    a = rgba(n)
    masks[n] = a[..., 3] > 127
    ys, xs = np.nonzero(masks[n])
    under = back[masks[n], :3].astype(int)
    own = a[masks[n], :3].astype(int)
    differs = np.abs(under - own).sum(axis=1).mean()
    print(f"        {n}: {a.shape[1]} x {a.shape[0]}, {masks[n].sum()} px, x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()}; the backdrop under it: "
          f"mean {under.mean(axis=0).round(0).astype(int).tolist()}, {differs:.0f} from the cut-out's own")
    say(a.shape[:2] == (H, W), f"{n}: the picture's size")
    say(((a[..., 3] == 0) | (a[..., 3] == 255)).all(), f"{n}: hard edges (alpha 0 or 255 only)")
gm, ge = rgba("glovebox-map"), rgba("glovebox-empty")
door = masks["glovebox-empty"]
say((door & ~masks["glovebox-map"]).sum() == 0, "glovebox-empty's door lies within glovebox-map (only the map goes)")
dd = np.abs(gm[door, :3].astype(int) - ge[door, :3].astype(int))
same = (dd.sum(axis=1) == 0).mean()
if raw:
    say(same == 1.0, f"the glovebox's door is the same in its two open states: {same:.1%} of its pixels")
else:                                                         # (keyed: the key reads each state's picture whole, so a few of the door's
    off = dd[dd.sum(axis=1) > 0]                              #  pixels next to the compartment may fall to a neighbouring paint)
    say(same >= 0.99 and (off.max() if len(off) else 0) <= 24,
        f"the glovebox's door is the same in its two open states: {same:.1%} of its pixels" + (f" (the rest a paint apart: {len(off)} px, "
        f"{off.mean():.1f} a channel on average)" if len(off) else ""))
if raw:
    # the backdrop and each state's cut-outs together give back that state's own painting round each cut-out's edge
    def blur(a, r=2):
        k = np.ones(2 * r + 1) / (2 * r + 1)
        a = np.apply_along_axis(lambda v: np.convolve(v, k, mode="same"), 0, a)
        return np.apply_along_axis(lambda v: np.convolve(v, k, mode="same"), 1, a)

    for state, names, ref in (("first", ["back", "glovebox-shut", "visor-up", "freshener"], "2-first.png"),
                              ("map", ["back", "glovebox-map"], "2-map.png"), ("empty", ["back", "glovebox-empty"], "2-empty.png"),
                              ("visor down", ["back", "visor-down"], "2-down.png")):
        if not os.path.exists(f"{WORK}/{ref}"):
            print(f"        ({ref} is not there: the {state} state's painting is not checked)")
            continue
        got = np.asarray(laid(names).convert("RGB")).astype(np.float32)
        want = np.asarray(Image.open(f"{WORK}/{ref}").convert("RGB")).astype(np.float32)
        d = np.abs(blur(got.mean(axis=2)) - blur(want.mean(axis=2)))
        m = np.zeros((H, W), bool)
        for n in names[1:]:
            m |= masks[n]
        pm = np.pad(m, 3)
        ring = np.zeros((H, W), bool)
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                ring |= pm[3 + dy:3 + dy + H, 3 + dx:3 + dx + W]
        ring &= ~m
        off = int((d[ring] > 24).sum())
        say(off <= 0.01 * ring.sum(), f"{state}: laid together, round the cut-outs' edges ({ring.sum()} px) the picture is its painting but {off} px "
                                      f"(mean difference {d[ring].mean():.1f}; elsewhere {d[~ring & ~m].mean():.1f})")

# ---- the glass
print("the glass")
glass = inside_poly(L["glass"])
if os.path.exists(f"{WORK}/masks.npz"):
    z = np.load(f"{WORK}/masks.npz")
    car = z["solid"] & ~z["glass_view"]
    inside_car = int((glass & car).sum())
    out = int((z["glass_view"] & ~glass).sum())
    say(inside_car == 0, f"{len(L['glass'])} corners: {inside_car} px of the car (pillar, dash, mirror, wheel) inside the glass; {out} px of glass outside it")
else:
    print("        (no masks.npz: the glass is not checked)")
ys, xs = np.nonzero(glass)
print(f"        the glass: x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()}, {glass.sum()} px")
sx, sy = st["at"]
say(glass[sy - 2, sx], f"the steam's foot ({sx}, {sy}) is in the glass")

# ---- the pictures with the numbers over them
COL = {"windshield": (90, 200, 255), "visor": (255, 140, 0), "rearview": (255, 0, 255), "freshener": (255, 60, 60), "door": (0, 255, 120),
       "manual": (255, 255, 0), "seat": (0, 255, 255), "glovebox": (255, 255, 255), "cupholder": (60, 120, 255), "wheel": (255, 0, 120),
       "radio": (180, 255, 0), "gauges": (0, 200, 200), "horn": (255, 200, 120), "gears": (200, 120, 255), "key": (255, 255, 160)}


def draw_numbers(im, later):
    over = Image.new("RGBA", im.size, (0, 0, 0, 0))
    dr = ImageDraw.Draw(over)
    dr.line([(0, BAND), (W, BAND)], fill=(0, 255, 0, 200), width=1)
    dr.text((4, BAND + 2), "548: the band (the way out)", fill=(0, 255, 0, 255))
    dr.line([(0, L["horizon"]), (W, L["horizon"])], fill=(255, 128, 0, 120))
    dr.text((W - 90, L["horizon"] + 2), f"horizon {L['horizon']}", fill=(255, 128, 0, 255))
    x0, y0, x1, y1 = L["words"]["box"]
    dr.rectangle([x0, y0, x1, y1], outline=(255, 211, 77, 255), width=2)
    dr.text((x0 + 3, y0 + 2), "words", fill=(255, 211, 77, 255))
    dr.line([tuple(p) for p in L["glass"]] + [tuple(L["glass"][0])], fill=(120, 220, 255, 230), width=1)
    for t in L["things"]:
        key = "down" if (later and t["id"] == "visor") else "open" if (later and t["id"] == "glovebox") else "shape"
        poly = [tuple(p) for p in (t[key] if key != "shape" else t["shape"])["poly"]]
        c = COL[t["id"]]
        dr.polygon(poly, outline=c + (255,), fill=c + (40,))
        xs_, ys_ = [p[0] for p in poly], [p[1] for p in poly]
        dr.text((min(xs_) + 2, min(ys_) + 1), t["id"] + (f" ({key})" if key != "shape" else ""), fill=c + (255,))
    dr.line([tuple(p) for p in L["walk"]] + [tuple(L["walk"][0])], fill=(0, 255, 255, 255), width=1)
    mx, my = L["marks"]["default"]
    dr.ellipse([mx - 3, my - 3, mx + 3, my + 3], outline=(255, 0, 0, 255), width=2)
    dr.text((mx + 6, my - 12), "default", fill=(255, 0, 0, 255))
    for m in L["fx"]:
        if "poly" in m:
            dr.line([tuple(p) for p in m["poly"]] + [tuple(m["poly"][0])], fill=(255, 255, 255, 200), width=1)
            dr.text(tuple(m["poly"][0]), m["id"], fill=(255, 255, 255, 255))
    ax, ay = st["at"]
    dr.ellipse([ax - 3, ay - 3, ax + 3, ay + 3], outline=(255, 255, 255, 255), width=2)
    dr.line([(ax, ay), (ax + st["lean"][0], ay + st["lean"][1])], fill=(255, 255, 255, 200), width=1)
    dr.line([(ax - 12, ay - st["height"]), (ax + 12, ay - st["height"])], fill=(255, 255, 255, 200), width=1)
    dr.text((ax + 5, ay - 12), "steam", fill=(255, 255, 255, 255))
    px, py = fr["at"]
    dr.line([(px - 8, py), (px + 8, py)], fill=(255, 60, 60, 255), width=1)
    dr.text((px + 10, py - 6), f"pin {py}", fill=(255, 60, 60, 255))
    im.alpha_composite(over)
    return im


draw_numbers(laid(["back", "glovebox-shut", "visor-up", "freshener"]), False).convert("RGB").save(f"{prefix}.png")
draw_numbers(laid(["back", "glovebox-map", "visor-down", "freshener"]), True).convert("RGB").save(f"{prefix}-later.png")

# ---- Dad's words over the box (the game's: bold, its text face at 2.7 per cent of the stage, 1.2 lines, a dark outline)
LINE = "A tape in the deck: a musical my wife taped off the radio, with the traffic report in the big song."
font = None
for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/msttcorefonts/Trebuchet_MS_Bold.ttf"):
    if os.path.exists(f):
        font = ImageFont.truetype(f, 21)
        break
font = font or ImageFont.load_default()


def words(im, text):
    dr = ImageDraw.Draw(im)
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if dr.textlength(t, font=font) <= 400:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    step = 26
    y = 150 - step * len(lines)
    for ln in lines:
        x = 400 - dr.textlength(ln, font=font) / 2
        for ox, oy in ((-1.5, 0), (1.5, 0), (0, -1.5), (0, 1.5), (-1, -1), (1, 1), (-1, 1), (1, -1)):
            dr.text((x + ox, y + oy), ln, font=font, fill=(0, 0, 0))
        dr.text((x, y), ln, font=font, fill=(255, 211, 77))
        y += step
    return len(lines)


up = laid(["back", "glovebox-shut", "visor-up", "freshener"]).convert("RGB")
down = laid(["back", "glovebox-map", "visor-down", "freshener"]).convert("RGB")
LUMW = np.array([0.2126, 0.7152, 0.0722], np.float32)
for label, im in (("visor up", up), ("visor down", down)):
    lum = np.asarray(im).astype(np.float32)[70:150, 200:600] @ LUMW              # the box's own tones (what the words lie on)
    print(f"        the words box, {label}: mean {lum.mean():.0f}, 95th percentile {np.percentile(lum, 95):.0f} (the yellow's "
          f"{np.array([255, 211, 77]) @ LUMW:.0f}); {(lum > 215).mean():.1%} of it lighter than 215")
    say(np.percentile(lum, 95) < 215, f"{label}: no glare in the words box (its 95th percentile under 215)")
n = words(up, LINE)
words(down, LINE)
print(f"        a long line of Dad's: {n} lines, centred on x 400, its bottom edge on row 150")
crop = (150, 40, 650, 180)
a, b = up.crop(crop), down.crop(crop)
sheet = Image.new("RGB", (a.width, a.height * 2 + 6), (255, 255, 255))
sheet.paste(a, (0, 0))
sheet.paste(b, (0, a.height + 6))
sheet.resize((sheet.width * 2, sheet.height * 2), Image.LANCZOS).save(f"{prefix}-words.png")
up.save(f"{prefix}-words-1x.png")

print()
print(f"pictures: {prefix}.png, {prefix}-later.png, {prefix}-words.png, {prefix}-words-1x.png")
print("PROBLEMS:\n  " + "\n  ".join(problems) if problems else "ALL GOOD")
sys.exit(1 if problems else 0)

"""The map of the Office: checks on the finished pictures and layout.json, and the pictures to look at (OFFICE-17B).

    python3 map_office_check.py [folder]      checks out/map-office/ (or the folder: the installed art/maps/office/ too)

Writes out/map-office-check/: all.png (every place and way, the names in the map's label style, a stand-in row of two
grey discs at each pin), none.png (the sheet alone), first.png (the stage's opening: the lot visited, with its name and
one disc; the ducts and the way up to them faint, at 0.28), later.png (Ranger in the ducts and Grandpa Joe in the
Comfortable Room: the lot, the ducts and the room drawn, the way drawn, B-7 faint), layout.png (all.png with every shape,
pin row, name box and via in thin lines). Prints each check and exits non-zero if one fails."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from letter import KOINE

FOLDER = sys.argv[1] if len(sys.argv) > 1 else "out/map-office"
CHECK = "out/map-office-check"
IDS = ["lot", "ducts", "room", "property", "breakroom", "b7"]
NAMES = {"lot": "The lot", "ducts": "The ducts", "room": "The Comfortable Room", "property": "Property & Effects",
         "breakroom": "The break room", "b7": "B-7"}
WAYS = [("lot", "ducts")]
ROW, DISCS = (76, 44), 2
FAILS = []


def ok(cond, what):
    print(("  ok    " if cond else "  FAIL  ") + what)
    if not cond:
        FAILS.append(what)


def load(name):
    return Image.open(os.path.join(FOLDER, name))


def rgba(name):
    return np.asarray(load(name).convert("RGBA"), dtype=np.float32) / 255


def poly_mask(poly):
    im = Image.new("L", (800, 600), 0)
    ImageDraw.Draw(im).polygon([tuple(p) for p in poly], fill=255)
    return np.asarray(im) >= 128


def box_mask(b):
    m = np.zeros((600, 800), bool)
    x0, y0, x1, y1 = [int(round(v)) for v in b]
    m[max(y0, 0):max(y1, 0), max(x0, 0):max(x1, 0)] = True
    return m


def pin_box(p):
    return (p[0] - ROW[0] / 2, p[1] - ROW[1] / 2, p[0] + ROW[0] / 2, p[1] + ROW[1] / 2)


def name_box(p, w):
    return (p[0] - w / 2, p[1] - 20, p[0] + w / 2, p[1] + 5)


def apart(a, b, gap):
    return a[2] + gap <= b[0] or b[2] + gap <= a[0] or a[3] + gap <= b[1] or b[3] + gap <= a[1]


def dilate(m, r):
    im = Image.fromarray((m * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.MaxFilter(2 * r + 1))) >= 128


def text_width(text, lab):
    f = ImageFont.truetype(KOINE, lab["size"])
    t = text.upper() if lab["upper"] else text
    return f.getlength(t) + lab["spacing"] * lab["size"] * (len(t) - 1)


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def draw_name(im, text, at, lab, opacity=1.0):
    """A name as the engine will draw it: Koine Road at the label's size and spacing, its baseline's middle at `at`, with
    the soft halo behind the letters."""
    f = ImageFont.truetype(KOINE, lab["size"])
    t = text.upper() if lab["upper"] else text
    w = text_width(text, lab)
    m = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(m)
    x = at[0] - w / 2
    for ch in t:
        d.text((x, at[1]), ch, font=f, fill=255, anchor="ls")
        x += f.getlength(ch) + lab["spacing"] * lab["size"]
    base = im.convert("RGBA")
    if lab.get("halo"):
        halo = m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.6))
        layer_ = Image.new("RGBA", im.size, hexrgb(lab["halo"]) + (0,))
        layer_.putalpha(halo.point(lambda v: int(min(255, v * 1.3) * 0.85 * opacity)))
        base = Image.alpha_composite(base, layer_)
    layer_ = Image.new("RGBA", im.size, hexrgb(lab["color"]) + (0,))
    layer_.putalpha(m.point(lambda v: int(v * opacity)))
    return Image.alpha_composite(base, layer_)


def discs(im, pin, n=2):
    d = ImageDraw.Draw(im)
    w = n * 36 + (n - 1) * 4
    x0 = pin[0] - w / 2
    for k in range(n):
        cx = x0 + 18 + k * 40
        d.ellipse([cx - 18, pin[1] - 18, cx + 18, pin[1] + 18], fill=(150, 150, 156, 255), outline=(90, 90, 98, 255))
    return im


def layer(im, name, opacity=1.0):
    pic = load(name).convert("RGBA")
    if opacity < 1.0:
        a = np.asarray(pic, dtype=np.float32)
        a[..., 3] *= opacity
        pic = Image.fromarray(a.astype(np.uint8), "RGBA")
    return Image.alpha_composite(im, pic)


def main():
    os.makedirs(CHECK, exist_ok=True)
    lay = json.load(open(os.path.join(FOLDER, "layout.json")))
    print(f"checking {FOLDER}")
    ok(lay["map"] == "office" and lay["size"] == [800, 600], "map 'office', size 800 x 600")
    ok([p["id"] for p in lay["places"]] == IDS, "places: " + ", ".join(p["id"] for p in lay["places"]))
    ok([(w["a"], w["b"]) for w in lay["paths"]] == WAYS, "ways: " + ", ".join(f"{w['a']}-{w['b']}" for w in lay["paths"]))
    files = ["back.png"] + [p["picture"] for p in lay["places"]] + [w["picture"] for w in lay["paths"]]
    ok(files == ["back.png"] + [f"place-{i}.png" for i in IDS] + [f"path-{a}-{b}.png" for a, b in WAYS], "files named as the contract says")
    for f in files:
        im = load(f)
        ok(im.size == (800, 600) and im.mode == "P" and "transparency" in im.info, f"{f}: 800 x 600, a palette with transparency")
    total = sum(os.path.getsize(os.path.join(FOLDER, f)) for f in files + ["layout.json"])
    ok(total <= 1.5 * 1024 * 1024, f"the map's files come to {total / 1024:.0f} KB (at most 1536)")
    pal = {bytes(load(f).getpalette()[:3 * 256]) for f in files}
    ok(len(pal) == 1, f"one palette for the whole map ({len(load('back.png').getpalette()) // 3 - 1} colours and clear)")
    for f in files:
        a = rgba(f)[..., 3]
        ok(a[:128].max() == 0 and a[572:].max() == 0, f"{f}: rows 0-127 and 572-599 clear")
    back_a = rgba("back.png")[..., 3] >= 0.5
    ys, xs = np.nonzero(back_a)
    sb = lay["sheet"]
    ok(32 <= sb[0] and sb[2] <= 768 and 128 <= sb[1] and sb[3] <= 572, f"sheet box {sb} within x 32-768, y 128-572")
    ok(xs.min() >= sb[0] and xs.max() < sb[2] and ys.min() >= sb[1] and ys.max() < sb[3],
       f"the sheet's material ({xs.min()}..{xs.max()}, {ys.min()}..{ys.max()}) inside its box")
    lab = lay["label"]
    ok(13 <= lab["size"] <= 18, f"label size {lab['size']} (13 to 18)")
    drawn = {p["id"]: rgba(p["picture"])[..., 3] >= 0.5 for p in lay["places"]}
    wayd = {(w["a"], w["b"]): rgba(w["picture"])[..., 3] >= 0.5 for w in lay["paths"]}
    smask = {}
    for p in lay["places"]:
        m = poly_mask(p["shape"])
        smask[p["id"]] = m
        inside = (drawn[p["id"]] & m).sum() / max(1, drawn[p["id"]].sum())
        ok(len(p["shape"]) <= 24, f"{p['id']}: shape of {len(p['shape'])} points (at most 24)")
        ok(inside >= 0.90, f"{p['id']}: {inside * 100:.1f}% of its drawing inside its shape (at least 90)")
        ok((m & ~back_a).sum() == 0, f"{p['id']}: shape on the sheet")
    for i, a in enumerate(IDS):
        for b in IDS[i + 1:]:
            ok((smask[a] & smask[b]).sum() == 0, f"shapes of {a} and {b} do not overlap")
    pins = {p["id"]: p["pin"] for p in lay["places"]}
    boxes = {p["id"]: name_box(p["label"], p["label_max"]) for p in lay["places"]}
    for p in lay["places"]:
        pb = pin_box(p["pin"])
        ok(back_a[box_mask(pb)].all(), f"{p['id']}: pin row {[int(v) for v in pb]} on the sheet")
        w = text_width(NAMES[p["id"]], lab)
        ok(w <= p["label_max"], f"{p['id']}: the name ({w:.1f} px) fits its box ({p['label_max']})")
        ok(back_a[box_mask(boxes[p["id"]])].all(), f"{p['id']}: name box on the sheet")
        nb = box_mask(boxes[p["id"]])
        for q in lay["places"]:
            if q["id"] != p["id"]:
                if IDS.index(q["id"]) > IDS.index(p["id"]):
                    ok(apart(pin_box(p["pin"]), pin_box(q["pin"]), 8), f"pin rows of {p['id']} and {q['id']} at least 8 px apart")
                    ok(apart(boxes[p["id"]], boxes[q["id"]], 0), f"names of {p['id']} and {q['id']} apart")
                ok(apart(boxes[p["id"]], pin_box(q["pin"]), 0), f"{p['id']}'s name box clear of {q['id']}'s pin row")
                ok(not (nb & drawn[q["id"]]).any(), f"{p['id']}'s name box over none of {q['id']}'s drawing")
        ok(apart(boxes[p["id"]], pin_box(p["pin"]), 0), f"{p['id']}'s name box clear of its own pin row")
        for k, m in wayd.items():
            ok(not (nb & m).any(), f"{p['id']}'s name box over no line of the way {k[0]}-{k[1]}")
    for w in lay["paths"]:
        m = wayd[(w["a"], w["b"])]
        for p in lay["places"]:
            n = int((m & drawn[p["id"]]).sum())
            joined = p["id"] in (w["a"], w["b"])
            ok(n == 0 or (joined and n <= 12), f"way {w['a']}-{w['b']} over {n} px of {p['id']}'s drawing"
               + (" (a place it joins: at most 12, at its edge)" if joined else " (none allowed)"))
    for i, a in enumerate(IDS):
        for b in IDS[i + 1:]:
            ok(not (drawn[a] & drawn[b]).any(), f"drawings of {a} and {b} do not overlap")
    for w in lay["paths"]:
        via = w["via"]
        ok(via[0] == pins[w["a"]] and via[-1] == pins[w["b"]], f"{w['a']}-{w['b']}: via from {w['a']}'s pin to {w['b']}'s")
        near = dilate(wayd[(w["a"], w["b"])], 6)
        bad, n = 0, 0
        for (x0, y0), (x1, y1) in zip(via[1:-2], via[2:-1]):
            steps = max(1, int(math.hypot(x1 - x0, y1 - y0)))
            for k in range(steps + 1):
                x, y = x0 + (x1 - x0) * k / steps, y0 + (y1 - y0) * k / steps
                n += 1
                bad += 0 if near[int(round(y)), int(round(x))] else 1
        inner = via[1:-1]
        ok(all(near[y, x] for x, y in inner) and bad == 0,
           f"{w['a']}-{w['b']}: its {len(inner)} points and the {n} steps between them within 6 px of its line")
    # how plainly a place not visited yet shows, at 0.28: its lines against the sheet
    bk = np.asarray(load("back.png").convert("RGB"), dtype=np.float32) / 255
    for p in lay["places"]:
        a = rgba(p["picture"])
        m = a[..., 3] >= 0.5
        d = np.abs((a[..., :3] - bk)[m]).sum(-1).mean() * 0.28
        print(f"  note  {p['id']}: at 0.28 its drawing differs from the sheet by {d * 255:.0f} (of 765) on average")
    # ---- the pictures
    base = Image.new("RGBA", (800, 600), (30, 20, 50, 255))
    none = layer(base, "back.png")
    none.save(os.path.join(CHECK, "none.png"))
    allp = none
    for p in lay["places"]:
        allp = layer(allp, p["picture"])
    for w in lay["paths"]:
        allp = layer(allp, w["picture"])
    for p in lay["places"]:
        allp = draw_name(allp, NAMES[p["id"]], p["label"], lab)
    for p in lay["places"]:
        allp = discs(allp, p["pin"], DISCS)
    allp.save(os.path.join(CHECK, "all.png"))
    place = {p["id"]: p for p in lay["places"]}
    first = layer(none, "place-lot.png")
    first = layer(first, "place-ducts.png", 0.28)
    first = layer(first, "path-lot-ducts.png", 0.28)
    first = draw_name(first, NAMES["lot"], place["lot"]["label"], lab)
    first = discs(first, pins["lot"], 1)
    first.save(os.path.join(CHECK, "first.png"))
    later = layer(none, "place-lot.png")
    for nm in ("place-ducts.png", "place-room.png", "path-lot-ducts.png"):
        later = layer(later, nm)
    later = layer(later, "place-b7.png", 0.28)
    for pid in ("lot", "ducts", "room"):
        later = draw_name(later, NAMES[pid], place[pid]["label"], lab)
    later = discs(later, pins["ducts"], 1)
    later = discs(later, pins["room"], 1)
    later.save(os.path.join(CHECK, "later.png"))
    lp = allp.copy()
    d = ImageDraw.Draw(lp)
    cols = {"lot": (220, 60, 60), "ducts": (40, 200, 90), "room": (250, 220, 60), "property": (210, 70, 180), "breakroom": (60, 220, 230),
            "b7": (250, 140, 30)}
    for p in lay["places"]:
        c = cols[p["id"]] + (255,)
        d.line([tuple(q) for q in p["shape"]] + [tuple(p["shape"][0])], fill=c, width=1)
        d.rectangle(pin_box(p["pin"]), outline=c)
        d.rectangle(name_box(p["label"], p["label_max"]), outline=c)
        d.ellipse([p["pin"][0] - 2, p["pin"][1] - 2, p["pin"][0] + 2, p["pin"][1] + 2], fill=c)
    for w in lay["paths"]:
        d.line([tuple(q) for q in w["via"]], fill=(255, 255, 255, 255), width=1)
        for q in w["via"]:
            d.ellipse([q[0] - 1.5, q[1] - 1.5, q[0] + 1.5, q[1] + 1.5], fill=(255, 120, 200, 255))
    lp.save(os.path.join(CHECK, "layout.png"))
    print(f"\n{len(FAILS)} failed" if FAILS else "\nall checks passed")
    print("pictures:", ", ".join(os.path.join(CHECK, f) for f in ("all.png", "none.png", "first.png", "later.png", "layout.png")))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())

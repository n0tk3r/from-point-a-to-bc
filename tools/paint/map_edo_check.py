"""Checks on the map of Japan (out/map-edo/, or art/maps/edo/ if given) and its layout.json, and four pictures to look
at in out/map-edo-check/: all.png (everything, the names in the label's style, grey discs at the pins), none.png (the
sheet alone), first.png (Yui visited, its neighbour faint) and layout.png (all.png with every shape, pin row, name box
and via drawn over it). PAINT-20B, as the README's "Maps" asks.

    python3 map_edo_check.py [folder]

What it holds (each a line; the exit code is the number of failures): exactly the places and ways of js/content/maps.js
(yui, osaka, hills, himeji; yui-osaka, osaka-hills, hills-himeji), every file there, 800x600, a palette with a clear
colour; rows 0..127 and 572..599 clear in every file; the sheet's box within x 32..768, y 128..572; each shape at most
24 points, on the sheet, holding at least 90 per cent of its drawing's pixels, no two overlapping; each pin row (three
portraits: 116 x 36) on the sheet, no two within 8 px; each name's box on the sheet, clear of every pin row, every other
name, every other place's drawing and every way, the name fitting it; each via from a's pin to b's, within 6 px of its
drawing; a map's files 1.5 MB at most."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from letter import KOINE

FOLDER = sys.argv[1] if len(sys.argv) > 1 else "out/map-edo"
CHECK = "out/map-edo-check"
IDS = ["yui", "osaka", "hills", "himeji"]
NAMES = {"yui": "Yui", "osaka": "Osaka", "hills": "The hills", "himeji": "Himeji"}
WAYS = [("yui", "osaka"), ("osaka", "hills"), ("hills", "himeji")]
ROW = (116, 36)
FAILS = []


def ok(cond, what):
    print(("ok    " if cond else "FAIL  ") + what)
    if not cond:
        FAILS.append(what)
    return cond


def rgba(name):
    return Image.open(os.path.join(FOLDER, name)).convert("RGBA")


def alpha(name):
    return np.asarray(rgba(name))[..., 3] >= 128


def poly_mask(poly):
    m = Image.new("L", (800, 600), 0)
    ImageDraw.Draw(m).polygon([tuple(p) for p in poly], fill=255)
    return np.asarray(m) > 0


def box_mask(b):
    m = np.zeros((600, 800), bool)
    m[max(0, int(b[1])):int(math.ceil(b[3])), max(0, int(b[0])):int(math.ceil(b[2]))] = True
    return m


def pin_box(p):
    return (p[0] - ROW[0] / 2, p[1] - ROW[1] / 2, p[0] + ROW[0] / 2, p[1] + ROW[1] / 2)


def name_box(p, w):
    return (p[0] - w / 2, p[1] - 20, p[0] + w / 2, p[1] + 5)


def apart(a, b, gap):
    return a[2] + gap <= b[0] or b[2] + gap <= a[0] or a[3] + gap <= b[1] or b[3] + gap <= a[1]


def dilate(m, r):
    im = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * int(r) + 1))
    return np.asarray(im) > 0


def text_width(text, lab):
    f = ImageFont.truetype(KOINE, lab["size"])
    t = text.upper() if lab["upper"] else text
    return f.getlength(t) + lab["spacing"] * lab["size"] * (len(t) - 1)


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def draw_name(im, text, at, lab, opacity=1.0):
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


def discs(im, pin, n=3):
    d = ImageDraw.Draw(im)
    x = pin[0] - (n * 36 + (n - 1) * 4) / 2
    for i in range(n):
        d.ellipse([x, pin[1] - 18, x + 36, pin[1] + 18], fill=(120, 120, 120, 200), outline=(40, 40, 40, 255))
        x += 40
    return im


def layer(im, name, opacity=1.0):
    pic = rgba(name)
    if opacity < 1:
        a = pic.split()[3].point(lambda v: int(v * opacity))
        pic.putalpha(a)
    return Image.alpha_composite(im, pic)


def main():
    os.makedirs(CHECK, exist_ok=True)
    lay = json.load(open(os.path.join(FOLDER, "layout.json")))
    lab = lay["label"]
    ok([p["id"] for p in lay["places"]] == IDS, "the places are maps.js's, in its order")
    ok([(w["a"], w["b"]) for w in lay["paths"]] == WAYS, "the ways are maps.js's, in its order")
    files = ["back.png"] + [p["picture"] for p in lay["places"]] + [w["picture"] for w in lay["paths"]]
    total = 0
    for fn in files:
        path = os.path.join(FOLDER, fn)
        if not ok(os.path.exists(path), f"{fn} exists"):
            continue
        total += os.path.getsize(path)
        im = Image.open(path)
        ok(im.size == (800, 600) and im.mode == "P" and "transparency" in im.info, f"{fn}: 800x600, a palette with a clear colour")
        a = alpha(fn)
        ok(not a[:128].any() and not a[572:].any(), f"{fn}: rows 0..127 and 572..599 clear")
    ok(total <= 1.5e6, f"the map's files {total / 1e6:.2f} MB (1.5 at most)")
    sx0, sy0, sx1, sy1 = lay["sheet"]
    ok(32 <= sx0 < sx1 <= 768 and 128 <= sy0 < sy1 <= 572, f"the sheet's box {lay['sheet']} within x 32..768, y 128..572")
    back = alpha("back.png")
    sheet = box_mask(lay["sheet"])
    ok((back & ~sheet).sum() < 200, f"the sheet's drawing lies in its box ({int((back & ~sheet).sum())} px outside)")
    draw = {p["id"]: alpha(p["picture"]) for p in lay["places"]}
    ways = {(w["a"], w["b"]): alpha(w["picture"]) for w in lay["paths"]}
    way_any = np.zeros_like(back)
    for m in ways.values():
        way_any |= m
    shapes = {}
    for p in lay["places"]:
        pid = p["id"]
        ok(len(p["shape"]) <= 24, f"{pid}: shape of {len(p['shape'])} points (24 at most)")
        sm = poly_mask(p["shape"])
        shapes[pid] = sm
        ok((sm & ~sheet).sum() == 0, f"{pid}: shape on the sheet")
        held = (draw[pid] & sm).sum() / max(1, draw[pid].sum())
        ok(held >= 0.9, f"{pid}: shape holds {held * 100:.0f}% of its drawing")
        pb = pin_box(p["pin"])
        ok(pb[0] >= sx0 and pb[2] <= sx1 and pb[1] >= sy0 and pb[3] <= sy1, f"{pid}: pin row on the sheet")
        w = text_width(NAMES[pid], lab)
        ok(w + 8 <= p["label_max"] + 1e-6, f"{pid}: the name fits label_max ({w:.0f} + 8 <= {p['label_max']})")
        nb = name_box(p["label"], p["label_max"])
        ok(nb[0] >= sx0 and nb[2] <= sx1 and nb[1] >= sy0 and nb[3] <= sy1, f"{pid}: name box on the sheet")
        nbm = box_mask(nb)
        for q in lay["places"]:
            if q["id"] != pid:
                ok(not (nbm & dilate(draw[q["id"]], 1)).any(), f"{pid}: name clear of {q['id']}'s drawing")
                ok(apart(nb, name_box(q["label"], q["label_max"]), 0), f"{pid}: name clear of {q['id']}'s name")
            ok(apart(nb, pin_box(q["pin"]), 0), f"{pid}: name clear of {q['id']}'s pin row")
        ok(not (nbm & dilate(way_any, 1)).any(), f"{pid}: name clear of every way")
    for i, a in enumerate(IDS):
        for b in IDS[i + 1:]:
            ok(not (shapes[a] & shapes[b]).any(), f"shapes {a} and {b} do not overlap")
            pa, pb = [p["pin"] for p in lay["places"] if p["id"] == a][0], [p["pin"] for p in lay["places"] if p["id"] == b][0]
            ok(not apart(pin_box(pa), pin_box(pb), 8) is False, f"pins {a} and {b} 8 px apart")
    pins = {p["id"]: p["pin"] for p in lay["places"]}
    for w in lay["paths"]:
        via = w["via"]
        ok(via[0] == pins[w["a"]] and via[-1] == pins[w["b"]], f"{w['a']}-{w['b']}: via from a's pin to b's")
        ys, xs = np.nonzero(ways[(w["a"], w["b"])])
        far = 0.0
        for p in via[1:-1]:
            far = max(far, float(np.sqrt(((xs - p[0]) ** 2 + (ys - p[1]) ** 2).min())))
        ok(far <= 6, f"{w['a']}-{w['b']}: via within 6 px of its drawing (farthest {far:.1f})")
    # the four pictures
    base = Image.new("RGBA", (800, 600), (24, 22, 28, 255))
    none = layer(base.copy(), "back.png")
    none.save(os.path.join(CHECK, "none.png"))
    allp = none.copy()
    for w in lay["paths"]:
        allp = layer(allp, w["picture"])
    for p in lay["places"]:
        allp = layer(allp, p["picture"])
    for p in lay["places"]:
        allp = draw_name(allp, NAMES[p["id"]], p["label"], lab)
        discs(allp, p["pin"])
    allp.save(os.path.join(CHECK, "all.png"))
    first = none.copy()
    first = layer(first, "place-yui.png")
    first = layer(first, "path-yui-osaka.png", 0.28)
    first = layer(first, "place-osaka.png", 0.28)
    first = draw_name(first, NAMES["yui"], pins and [p for p in lay["places"] if p["id"] == "yui"][0]["label"], lab)
    first = draw_name(first, NAMES["osaka"], [p for p in lay["places"] if p["id"] == "osaka"][0]["label"], lab, 0.28)
    discs(first, pins["yui"])
    first.save(os.path.join(CHECK, "first.png"))
    lo = allp.copy()
    d = ImageDraw.Draw(lo)
    for p in lay["places"]:
        d.polygon([tuple(q) for q in p["shape"]], outline=(60, 220, 255, 255))
        d.rectangle(pin_box(p["pin"]), outline=(255, 80, 80, 255))
        d.rectangle(name_box(p["label"], p["label_max"]), outline=(255, 220, 60, 255))
    for w in lay["paths"]:
        d.line([tuple(q) for q in w["via"]], fill=(255, 0, 255, 255), width=1)
    lo.save(os.path.join(CHECK, "layout.png"))
    print(f"{len(FAILS)} failure{'s' if len(FAILS) != 1 else ''}; {CHECK}/all.png none.png first.png layout.png")
    return len(FAILS)


if __name__ == "__main__":
    sys.exit(main())

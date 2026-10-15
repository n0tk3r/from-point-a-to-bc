"""The map of Rome (MAP-15R): checks layout.json against the pictures, and draws the four pictures to look at.

  python3 map_rome_check.py      checks out/map-rome/ (prints every check, PASS or FAIL) and writes
                                 out/map-rome-check/all.png, none.png, first.png, layout.png (and each at half size)

The checks (PAINT-15.md, "layout.json"):
  - every place and way of the map, with exactly the ids of MAP-15.md's tables; every file named exists, 800 x 600;
  - each shape (at most 24 points) holds at least 90 per cent of its drawing's painted pixels and lies on the sheet;
    no two shapes overlap; no two places' drawings overlap, and a way's drawing touches only the two places it joins,
    at their edge;
  - each pin row (two discs: 76 x 44) lies on the sheet and on the wax, over no other place's drawing; no two pin rows
    come within 8 pixels; no name's box (label_max wide, 20 above the baseline and 5 below) lies over a pin row, another
    name's box, another place's drawing or any way's; each name's box lies on the wax; each name fits its box (Koine
    Road at the label's size and spacing, in capitals, as Pillow measures it);
  - each way's via starts at a's pin and ends at b's, and wherever it is outside those two places' shapes it lies
    within 6 pixels of the way's drawing;
  - rows 0 to 127 and 572 to 599 clear in every file; the map's files no more than 1.5 MB; every file an 8-bit palette
    picture with transparency, all sharing one palette.
The pictures: all.png (everything drawn, the names in the label style, a stand-in pin row of grey discs at each pin),
none.png (the sheet alone), first.png (Saturn's steps visited with its name and one portrait, its neighbours and the
ways to them faint at 0.28, nothing else), layout.png (all.png with every shape, pin row, name box and via)."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from letter import KOINE
from map_rome_kit import CHECK, OUT, H, W
from map_rome_layout import NAMES, name_width

IDS = ["street", "steps", "treasury", "forum", "capitol", "tiber"]
WAYS = [("steps", "street"), ("steps", "treasury"), ("steps", "forum"), ("steps", "capitol"), ("forum", "tiber")]
FIRST = "steps"
FAINT = 0.28
PIN_W, PIN_H = 76, 44
WAX = (64, 160, 736, 540)

results = []


def check(ok, what):
    results.append((bool(ok), what))
    print(("PASS  " if ok else "FAIL  ") + what)
    return ok


def rgba(name):
    return Image.open(os.path.join(OUT, name)).convert("RGBA")


def poly_mask(points):
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).polygon([tuple(p) for p in points], fill=255)
    return np.asarray(im) > 127


def box_mask(x0, y0, x1, y1):
    m = np.zeros((H, W), bool)
    m[max(0, int(math.floor(y0))):min(H, int(math.ceil(y1))), max(0, int(math.floor(x0))):min(W, int(math.ceil(x1)))] = True
    return m


def gap(a, b):
    """The gap between two boxes (x0, y0, x1, y1): negative when they overlap."""
    dx = max(b[0] - a[2], a[0] - b[2])
    dy = max(b[1] - a[3], a[1] - b[3])
    return max(dx, dy)


def pin_box(pin):
    return (pin[0] - PIN_W / 2, pin[1] - PIN_H / 2, pin[0] + PIN_W / 2, pin[1] + PIN_H / 2)


def name_box(p):
    return (p["label"][0] - p["label_max"] / 2, p["label"][1] - 20, p["label"][0] + p["label_max"] / 2, p["label"][1] + 5)


def numeric(layout):
    sheet = layout["sheet"]
    check(layout.get("map") == "rome" and layout.get("size") == [800, 600], "map is rome, size 800 x 600")
    check(32 <= sheet[0] and 128 <= sheet[1] and sheet[2] <= 768 and sheet[3] <= 572, f"sheet {sheet} within x 32-768, y 128-572")
    lab = layout["label"]
    check(13 <= lab["size"] <= 18 and lab["upper"] in (True, False) and isinstance(lab["spacing"], (int, float)),
          f"label style {lab}")
    places = {p["id"]: p for p in layout["places"]}
    check(sorted(places) == sorted(IDS) and len(layout["places"]) == len(IDS), f"places are exactly {IDS}")
    ways = [(w["a"], w["b"]) for w in layout["paths"]]
    check(ways == WAYS, f"ways are exactly {WAYS}, a and b in the table's order")
    files = ["back.png"] + [p["picture"] for p in layout["places"]] + [w["picture"] for w in layout["paths"]]
    check([p["picture"] for p in layout["places"]] == [f"place-{p['id']}.png" for p in layout["places"]]
          and [w["picture"] for w in layout["paths"]] == [f"path-{a}-{b}.png" for a, b in WAYS], "pictures are named place-<id>, path-<a>-<b>")
    pals = []
    total = 0
    for f in files:
        path = os.path.join(OUT, f)
        if not check(os.path.exists(path), f"{f} exists"):
            continue
        im = Image.open(path)
        total += os.path.getsize(path)
        check(im.size == (800, 600) and im.mode == "P" and "transparency" in im.info,
              f"{f}: 800 x 600, 8-bit palette with transparency ({im.mode}, {len(im.getpalette()) // 3} entries)")
        pals.append(bytes(im.getpalette()[:3 * 255]))
        a = np.asarray(im.convert("RGBA"))[..., 3]
        check(a[:128].max() == 0 and a[572:].max() == 0, f"{f}: rows 0-127 and 572-599 clear")
    check(len(set(pals)) == 1, "every file shares one palette")
    check(total <= 1.5 * 1024 * 1024, f"the map's files come to {total} bytes ({total / 1024 / 1024:.2f} MB, at most 1.5 MB)")
    back = np.asarray(rgba("back.png"))[..., 3] > 0
    ys, xs = np.where(back)
    check(xs.min() >= sheet[0] and ys.min() >= sheet[1] and xs.max() < sheet[2] and ys.max() < sheet[3], "back.png lies within the sheet box")
    drawings = {p: np.asarray(rgba(places[p]["picture"]))[..., 3] > 0 for p in IDS}
    way_draw = {w: np.asarray(rgba(f"path-{w[0]}-{w[1]}.png"))[..., 3] > 0 for w in WAYS}
    shapes = {}
    for p in IDS:
        pl = places[p]
        shp = pl["shape"]
        m = poly_mask(shp)
        shapes[p] = m
        inside = (drawings[p] & m).sum() / max(1, drawings[p].sum())
        check(len(shp) <= 24, f"{p}: shape has {len(shp)} points (at most 24)")
        check(inside >= 0.9, f"{p}: shape holds {inside * 100:.1f}% of its drawing")
        sx = [q[0] for q in shp]
        sy = [q[1] for q in shp]
        check(min(sx) >= sheet[0] and min(sy) >= sheet[1] and max(sx) <= sheet[2] and max(sy) <= sheet[3], f"{p}: shape on the sheet")
        check(drawings[p].sum() > 0 and (drawings[p] & ~back).sum() == 0, f"{p}: drawing lies on the sheet")
    for i, p in enumerate(IDS):
        for q in IDS[i + 1:]:
            check((shapes[p] & shapes[q]).sum() == 0, f"shapes of {p} and {q} do not overlap")
            check((drawings[p] & drawings[q]).sum() == 0, f"drawings of {p} and {q} do not overlap")
    for w in WAYS:
        for p in IDS:
            o = int((way_draw[w] & drawings[p]).sum())
            if p in w:
                check(o <= 40, f"way {w[0]}-{w[1]} runs up to {p}'s drawing ({o} px shared at the edge)")
            else:
                check(o == 0, f"way {w[0]}-{w[1]} lies over no part of {p}'s drawing")
    for i, w in enumerate(WAYS):
        for v in WAYS[i + 1:]:
            check((way_draw[w] & way_draw[v]).sum() == 0, f"ways {w[0]}-{w[1]} and {v[0]}-{v[1]} do not overlap")
    # pins and names
    for p in IDS:
        pb = pin_box(places[p]["pin"])
        check(pb[0] >= sheet[0] and pb[1] >= sheet[1] and pb[2] <= sheet[2] and pb[3] <= sheet[3], f"{p}: pin row {pb} on the sheet")
        check(pb[0] >= WAX[0] and pb[1] >= WAX[1] and pb[2] <= WAX[2] and pb[3] <= WAX[3], f"{p}: pin row on the wax")
        bm = box_mask(*pb)
        others = [q for q in IDS if q != p]
        hit = [q for q in others if (bm & drawings[q]).any()]
        check(not hit, f"{p}: pin row over no other place's drawing {hit if hit else ''}")
        covered = (bm & drawings[p]).sum() / max(1, drawings[p].sum())
        check(covered <= 0.5, f"{p}: pin row covers {covered * 100:.0f}% of the place's own drawing (leaves it readable)")
    for i, p in enumerate(IDS):
        for q in IDS[i + 1:]:
            g = gap(pin_box(places[p]["pin"]), pin_box(places[q]["pin"]))
            check(g >= 8, f"pin rows of {p} and {q} {g:.0f} px apart (at least 8)")
    for p in IDS:
        pl = places[p]
        nb = name_box(pl)
        width = name_width(NAMES[p], layout["label"])
        check(width <= pl["label_max"], f"{p}: name '{NAMES[p].upper()}' {width:.1f} px fits label_max {pl['label_max']}")
        check(nb[0] >= WAX[0] and nb[1] >= WAX[1] and nb[2] <= WAX[2] and nb[3] <= WAX[3], f"{p}: name box {tuple(round(v) for v in nb)} on the wax")
        nm = box_mask(*nb)
        for q in IDS:
            check(gap(nb, pin_box(places[q]["pin"])) > 0, f"{p}: name box clear of {q}'s pin row")
            if q != p:
                check(gap(nb, name_box(places[q])) > 0, f"{p}: name box clear of {q}'s name box")
                check(not (nm & drawings[q]).any(), f"{p}: name box over no part of {q}'s drawing")
        for w in WAYS:
            check(not (nm & way_draw[w]).any(), f"{p}: name box over no part of the way {w[0]}-{w[1]}")
    # the vias
    for w in layout["paths"]:
        a, b = w["a"], w["b"]
        via = w["via"]
        check(via[0] == places[a]["pin"] and via[-1] == places[b]["pin"], f"{a}-{b}: via runs from {a}'s pin to {b}'s")
        ys, xs = np.where(way_draw[(a, b)])
        worst = 0.0
        for (x0, y0), (x1, y1) in zip(via[:-1], via[1:]):
            n = max(2, int(math.hypot(x1 - x0, y1 - y0)) + 1)
            for t in np.linspace(0, 1, n):
                x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
                ix, iy = int(round(x)), int(round(y))
                if shapes[a][iy, ix] or shapes[b][iy, ix]:
                    continue
                worst = max(worst, float(np.sqrt(((xs - x) ** 2 + (ys - y) ** 2).min())))
        check(worst <= 6.0, f"{a}-{b}: via within {worst:.1f} px of its drawing outside the two places (at most 6)")
    return all(ok for ok, _ in results)


# ---------------------------------------------------------------- the pictures to look at
def draw_name(img, text, at, style):
    """A name as the engine writes it: the game's face, its colour, a halo of the wax's dark, letter-spaced."""
    t = text.upper() if style["upper"] else text
    size = style["size"]
    f = ImageFont.truetype(KOINE, size)
    sp = style["spacing"] * size
    total = sum(f.getlength(ch) for ch in t) + sp * (len(t) - 1)
    x = at[0] - total / 2
    halo = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dh = ImageDraw.Draw(halo)
    text_l = Image.new("RGBA", img.size, (0, 0, 0, 0))
    dt = ImageDraw.Draw(text_l)
    hc = tuple(int(style["halo"][i:i + 2], 16) for i in (1, 3, 5)) if style.get("halo") else None
    tc = tuple(int(style["color"][i:i + 2], 16) for i in (1, 3, 5))
    for ch in t:
        if hc:
            dh.text((x, at[1]), ch, font=f, fill=hc + (235,), anchor="ls", stroke_width=3, stroke_fill=hc + (235,))
        dt.text((x, at[1]), ch, font=f, fill=tc + (255,), anchor="ls")
        x += f.getlength(ch) + sp
    from PIL import ImageFilter
    if hc:
        img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(1.0)))
    img.alpha_composite(text_l)


def pins_on(img, pin, n=2, ring=False):
    d = ImageDraw.Draw(img)
    total = n * 36 + (n - 1) * 4
    x = pin[0] - total / 2
    for i in range(n):
        d.ellipse([x, pin[1] - 18, x + 36, pin[1] + 18], fill=(150, 150, 150, 235), outline=(90, 90, 90, 255), width=2)
        if ring and i == 0:
            d.ellipse([x - 3, pin[1] - 21, x + 39, pin[1] + 21], outline=(57, 230, 224, 255), width=3)
        x += 40


def layer(img, name, amount=1.0):
    im = rgba(name)
    if amount < 1:
        a = np.asarray(im).copy()
        a[..., 3] = (a[..., 3].astype(float) * amount).astype(np.uint8)
        im = Image.fromarray(a, "RGBA")
    img.alpha_composite(im)


def pictures(layout):
    os.makedirs(CHECK, exist_ok=True)
    ground = (34, 36, 48, 255)                         # a dark stage behind the sheet, as the map screen's
    places = {p["id"]: p for p in layout["places"]}

    def base():
        img = Image.new("RGBA", (W, H), ground)
        layer(img, "back.png")
        return img
    none = base()
    none.save(f"{CHECK}/none.png")
    allp = base()
    for w in layout["paths"]:
        layer(allp, w["picture"])
    for p in layout["places"]:
        layer(allp, p["picture"])
    for p in layout["places"]:
        draw_name(allp, NAMES[p["id"]], p["label"], layout["label"])
    for p in layout["places"]:
        pins_on(allp, p["pin"], 2)
    allp.save(f"{CHECK}/all.png")
    first = base()
    near = set()
    for w in layout["paths"]:
        if FIRST in (w["a"], w["b"]):
            near.add(w["b"] if w["a"] == FIRST else w["a"])
            layer(first, w["picture"], FAINT)
    for p in layout["places"]:
        if p["id"] in near:
            layer(first, p["picture"], FAINT)
    layer(first, places[FIRST]["picture"])
    draw_name(first, NAMES[FIRST], places[FIRST]["label"], layout["label"])
    pins_on(first, places[FIRST]["pin"], 1, ring=True)
    first.save(f"{CHECK}/first.png")
    lay = allp.copy()
    d = ImageDraw.Draw(lay)
    for p in layout["places"]:
        d.polygon([tuple(q) for q in p["shape"]], outline=(255, 90, 90, 255))
        d.rectangle(pin_box(p["pin"]), outline=(90, 200, 255, 255))
        d.rectangle(name_box(p), outline=(120, 255, 120, 255))
        d.ellipse([p["label"][0] - 2, p["label"][1] - 2, p["label"][0] + 2, p["label"][1] + 2], fill=(120, 255, 120, 255))
    for w in layout["paths"]:
        d.line([tuple(q) for q in w["via"]], fill=(255, 0, 255, 255), width=1)
        for q in w["via"]:
            d.ellipse([q[0] - 1.5, q[1] - 1.5, q[0] + 1.5, q[1] + 1.5], fill=(255, 0, 255, 255))
    d.rectangle(layout["sheet"], outline=(255, 255, 0, 255))
    lay.save(f"{CHECK}/layout.png")
    for n in ("all", "none", "first", "layout"):
        Image.open(f"{CHECK}/{n}.png").resize((400, 300), Image.LANCZOS).save(f"{CHECK}/{n}-half.png")


def main():
    results.clear()
    with open(os.path.join(OUT, "layout.json")) as f:
        layout = json.load(f)
    ok = numeric(layout)
    pictures(layout)
    bad = [w for k, w in results if not k]
    print(f"{len(results) - len(bad)} of {len(results)} checks passed" + (f"; FAILED: {len(bad)}" if bad else ""))
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)

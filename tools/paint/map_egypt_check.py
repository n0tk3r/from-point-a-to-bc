"""Checks on the finished map of Egypt (MAP-15E), and the four pictures to look at.

    python3 map_egypt_check.py                 checks out/map-egypt/ (map_egypt.py runs it after a full run)
    python3 map_egypt_check.py ../game/art/maps/egypt     checks the installed copy instead

What it checks (PAINT-15.md, "layout.json"):
  - every place and way of the map, with exactly the ids of MAP-15.md's table; every file it names exists, is
    800 x 600, and is a palette picture with transparency
  - each shape has at most 24 points, holds at least 90 per cent of its place's painted pixels, and lies on the
    sheet; no two shapes overlap
  - each pin row (two discs: 76 x 44) lies on the sheet; no two come within 8 pixels; no name's box (label_max wide,
    20 above the baseline, 5 below) lies over a pin row, another name's box, another place's drawing or a way's, and
    each lies on the sheet; each name fits its box (Koine Road at label.size, with label.spacing)
  - each way's via starts at its a's pin, ends at its b's, and lies within 6 pixels of its drawing all the way
  - rows 0 to 127 and 572 to 599 are clear in every file; the sheet's box is within x 32 to 768, y 128 to 572;
    label.size is 13 to 18; the files come to no more than 1.5 MB
and it draws, into out/map-egypt-check/: all.png (everything, the names, stand-in pin rows), none.png (the sheet
alone), first.png (the river visited, its neighbour faint), layout.png (all.png with the shapes, pin rows, name
boxes and vias drawn over it)."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import map_egypt_kit as K
import map_egypt_layout as LY

IDS_PLACES = ["river", "site", "gallery", "chamber"]
IDS_WAYS = [("river", "site"), ("site", "gallery"), ("gallery", "chamber")]
FAINT = 0.28
GROUND = (30, 26, 23)          # behind the sheet: the map screen's dark


def load(folder):
    with open(os.path.join(folder, "layout.json")) as f:
        lay = json.load(f)
    pics = {}
    for name in ["back.png"] + [p["picture"] for p in lay["places"]] + [w["picture"] for w in lay["paths"]]:
        pics[name] = Image.open(os.path.join(folder, name))
    return lay, pics


def rgba(im):
    return np.asarray(im.convert("RGBA")).astype(np.float32) / 255


def over(base, top, amount=1.0):
    a = top[..., 3:4] * amount
    return base * (1 - a) + top[..., :3] * a


def label_mask(text, at, label, shape=K.SHAPE, ss=3):
    """The name as the engine sets it: Koine Road at label.size, letter-spaced, centred on the anchor's baseline."""
    h, w = shape
    size = label["size"]
    f = ImageFont.truetype(LY.FONT, size * ss)
    t = text.upper() if label["upper"] else text
    total = LY.text_width(text, label)
    im = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(im)
    x = (at[0] - total / 2) * ss
    for ch in t:
        d.text((x, at[1] * ss), ch, fill=255, font=f, anchor="ls")
        x += f.getlength(ch) + label["spacing"] * size * ss
    return np.asarray(im.resize((w, h), Image.BOX)).astype(np.float32) / 255


def draw_name(pic, text, at, label):
    m = label_mask(text, at, label)
    if label.get("halo"):
        halo = Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.3))
        hm = np.clip(np.asarray(halo).astype(np.float32) / 255 * 1.15, 0, 0.92)
        pic = pic * (1 - hm[..., None]) + np.array(K.rgb(label["halo"]))[None, None, :] * hm[..., None]
    col = np.array(K.rgb(label["color"]))
    return pic * (1 - m[..., None]) + col[None, None, :] * m[..., None]


def discs(pic, pin, count, grey=0.55):
    img = Image.fromarray((np.clip(pic, 0, 1) * 255 + 0.5).astype(np.uint8))
    d = ImageDraw.Draw(img, "RGBA")
    xs = [pin[0]] if count == 1 else [pin[0] - 20, pin[0] + 20]
    for x in xs:
        d.ellipse([x - 18, pin[1] - 18, x + 18, pin[1] + 18], fill=(int(grey * 255),) * 3 + (235,), outline=(70, 70, 70, 255), width=1)
    return np.asarray(img).astype(np.float32) / 255


def compose(lay, pics, visited, faint, names=True, pins=True, one_pin=False):
    base = np.ones(K.SHAPE + (3,), np.float32) * np.array(GROUND, np.float32) / 255
    pic = over(base, rgba(pics["back.png"]))
    for w in lay["paths"]:
        a, b = w["a"], w["b"]
        if a in visited and b in visited:
            pic = over(pic, rgba(pics[w["picture"]]))
        elif (a in visited and b in faint) or (b in visited and a in faint):
            pic = over(pic, rgba(pics[w["picture"]]), FAINT)
    for p in lay["places"]:
        if p["id"] in visited:
            pic = over(pic, rgba(pics[p["picture"]]))
        elif p["id"] in faint:
            pic = over(pic, rgba(pics[p["picture"]]), FAINT)
    if names:
        for p in lay["places"]:
            if p["id"] in visited:
                pic = draw_name(pic, LY.NAMES[p["id"]], p["label"], lay["label"])
    if pins:
        for p in lay["places"]:
            if p["id"] in visited:
                pic = discs(pic, p["pin"], 1 if one_pin else 2)
    return np.clip(pic, 0, 1)


def save(pic, path):
    Image.fromarray((np.clip(pic, 0, 1) * 255 + 0.5).astype(np.uint8)).save(path)


def main(folder=K.OUT, out=K.CHECK):
    lay, pics = load(folder)
    os.makedirs(out, exist_ok=True)
    problems, notes = [], []

    def ok(cond, what):
        (notes if cond else problems).append(what)

    # the ids and the files
    ok([p["id"] for p in lay["places"]] == IDS_PLACES, f"places are {IDS_PLACES}")
    ok([(w["a"], w["b"]) for w in lay["paths"]] == IDS_WAYS, f"ways are {IDS_WAYS}")
    ok(lay["map"] == "egypt" and lay["size"] == [800, 600], "map egypt, 800 x 600")
    for name, im in pics.items():
        ok(im.size == (800, 600), f"{name} is 800 x 600")
        ok(im.mode == "P" and "transparency" in im.info, f"{name} is a palette picture with transparency")
    files = ["back.png"] + [p["picture"] for p in lay["places"]] + [w["picture"] for w in lay["paths"]]
    for f in files:
        ok(os.path.exists(os.path.join(folder, f)), f"{f} exists")
    total = sum(os.path.getsize(os.path.join(folder, f)) for f in files + ["layout.json"])
    ok(total <= 1.5 * 1024 * 1024, f"the map's files come to {total / 1024:.0f} KB (at most 1536)")
    A = {name: np.asarray(im.convert("RGBA"))[..., 3] > 127 for name, im in pics.items()}
    for name, a in A.items():
        ok(not a[:128].any() and not a[572:].any(), f"{name}: rows 0-127 and 572-599 clear")
    sheet = A["back.png"]
    sx0, sy0, sx1, sy1 = lay["sheet"]
    ok(sx0 >= 32 and sy0 >= 128 and sx1 <= 768 and sy1 <= 572, f"sheet {lay['sheet']} within x 32-768, y 128-572")
    ys, xs = np.nonzero(sheet)
    ok(xs.min() >= sx0 and xs.max() < sx1 and ys.min() >= sy0 and ys.max() < sy1, "the papyrus lies within the sheet's box")
    ok(13 <= lay["label"]["size"] <= 18, f"label size {lay['label']['size']} (13 to 18)")

    # shapes
    rasters = {}
    for p in lay["places"]:
        poly = p["shape"]
        ok(len(poly) <= 24, f"{p['id']}: shape has {len(poly)} points (at most 24)")
        r = LY.raster(poly)
        rasters[p["id"]] = r
        drawn = A[p["picture"]]
        share = (drawn & r).sum() / max(1, drawn.sum())
        ok(share >= 0.90, f"{p['id']}: shape holds {share * 100:.1f}% of the drawing (at least 90)")
        ok(all(sx0 <= x <= sx1 and sy0 <= y <= sy1 for x, y in poly) and (r & ~sheet).sum() == 0, f"{p['id']}: shape on the sheet")
    for i, a in enumerate(IDS_PLACES):
        for b in IDS_PLACES[i + 1:]:
            ok(not (rasters[a] & rasters[b]).any(), f"shapes {a} and {b} do not overlap")

    # pin rows and names
    rows = {p["id"]: LY.row_box(p["pin"]) for p in lay["places"]}
    for k, b in rows.items():
        bx = [int(math.floor(b[0])), int(math.floor(b[1])), int(math.ceil(b[2])), int(math.ceil(b[3]))]
        on = sheet[bx[1]:bx[3], bx[0]:bx[2]]
        ok(on.size and on.all(), f"{k}: pin row {[round(v) for v in b]} on the sheet")
    for i, a in enumerate(IDS_PLACES):
        for b in IDS_PLACES[i + 1:]:
            ok(not LY.boxes_meet(rows[a], rows[b], 8), f"pin rows {a} and {b} at least 8 apart")
    nboxes = {p["id"]: LY.name_box(p["label"], p["label_max"]) for p in lay["places"]}
    ways_all = np.zeros(K.SHAPE, bool)
    for w in lay["paths"]:
        ways_all |= A[w["picture"]]
    for p in lay["places"]:
        k = p["id"]
        nb = nboxes[k]
        width = LY.text_width(LY.NAMES[k], lay["label"])
        ok(width <= p["label_max"], f"{k}: the name is {width:.1f} wide in a box of {p['label_max']}")
        ix = [int(math.floor(nb[0])), int(math.floor(nb[1])), int(math.ceil(nb[2])), int(math.ceil(nb[3]))]
        on = sheet[ix[1]:ix[3], ix[0]:ix[2]]
        ok(on.size and on.all(), f"{k}: name box on the sheet")
        for j, rb in rows.items():
            ok(not LY.boxes_meet(nb, rb), f"{k}: name box clear of {j}'s pin row")
        for j, ob in nboxes.items():
            if j != k:
                ok(not LY.boxes_meet(nb, ob), f"{k}: name box clear of {j}'s name")
        others = np.zeros(K.SHAPE, bool)
        for q in lay["places"]:
            if q["id"] != k:
                others |= A[q["picture"]]
        cut = (others | ways_all)[ix[1]:ix[3], ix[0]:ix[2]]
        ok(not cut.any(), f"{k}: name box clear of the other places' drawings and of the ways")

    # vias
    pins = {p["id"]: p["pin"] for p in lay["places"]}
    for w in lay["paths"]:
        via = w["via"]
        ok(via[0] == pins[w["a"]] and via[-1] == pins[w["b"]], f"{w['a']}-{w['b']}: via runs from {w['a']}'s pin to {w['b']}'s")
        m = A[w["picture"]]
        ys, xs = np.nonzero(m)
        P = np.stack([xs, ys], 1).astype(float)
        worst = 0.0
        for (x0, y0), (x1, y1) in zip(via[:-1], via[1:]):
            n = max(2, int(math.hypot(x1 - x0, y1 - y0)))
            for t in np.linspace(0, 1, n):
                q = (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
                worst = max(worst, float(np.min(np.hypot(P[:, 0] - q[0], P[:, 1] - q[1]))))
        ok(worst <= 6.0, f"{w['a']}-{w['b']}: via within {worst:.1f} px of its drawing (at most 6)")

    # the pictures
    allv = set(IDS_PLACES)
    pic_all = compose(lay, pics, allv, set())
    save(pic_all, os.path.join(out, "all.png"))
    save(compose(lay, pics, set(), set(), names=False, pins=False), os.path.join(out, "none.png"))
    save(compose(lay, pics, {"river"}, {"site"}, one_pin=True), os.path.join(out, "first.png"))
    img = Image.fromarray((pic_all * 255 + 0.5).astype(np.uint8))
    d = ImageDraw.Draw(img)
    colours = {"river": (0, 110, 200), "site": (200, 0, 160), "gallery": (0, 150, 60), "chamber": (220, 110, 0)}
    for p in lay["places"]:
        c = colours[p["id"]]
        d.line([tuple(q) for q in p["shape"]] + [tuple(p["shape"][0])], fill=c, width=1)
        d.rectangle(rows[p["id"]], outline=c)
        d.rectangle(nboxes[p["id"]], outline=(220, 0, 0))
        d.ellipse([p["pin"][0] - 2, p["pin"][1] - 2, p["pin"][0] + 2, p["pin"][1] + 2], fill=c)
    for w in lay["paths"]:
        d.line([tuple(q) for q in w["via"]], fill=(0, 200, 220), width=1)
    d.rectangle(lay["sheet"], outline=(120, 120, 120))
    img.save(os.path.join(out, "layout.png"))

    print(f"  checks: {len(notes)} passed, {len(problems)} failed")
    for p in problems:
        print("  FAILED:", p)
    return not problems, notes, problems


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    folder = args[0] if args else K.OUT
    good, notes, problems = main(folder)
    if "-v" in sys.argv:
        for n in notes:
            print("  ok:", n)
    sys.exit(0 if good else 1)

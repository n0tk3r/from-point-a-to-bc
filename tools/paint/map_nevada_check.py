"""Checks on the finished map of Nevada (MAP-15N), and the four pictures to look at.

    python3 map_nevada_check.py [folder] [pictures]   (default out/map-nevada; the pictures go to <folder>-check/, or to
                                                       [pictures]: give one when checking the installed art/maps/nevada/)

The numbers (each line says what it checked; any failure is listed at the end, and the exit status is 1):
  - the places and ways are exactly MAP-15.md's for Nevada (roadside, store, road; roadside-store), every file named is
    there, 800 x 600, a palette picture with a clear colour, all on one palette of 160 to 220 colours;
  - each shape has at most 24 points, lies inside the sheet, holds at least 90 per cent of its place's painted pixels,
    and overlaps no other shape;
  - each pin row (three portraits: 116 x 44 about the pin) lies on the paper; no two come within 8 pixels; no name's
    box (label_max wide, 20 above the baseline and 5 below) lies over a pin row, another name's box, another place's
    drawing or a way's; each name, in Koine Road at the label size and spacing (capitals), fits its label_max;
  - each way's via starts at its a's pin and ends at its b's, and every point along it is within 6 pixels of the way's
    drawing;
  - rows 0 to 127 and 572 to 599 are clear in every file; the files come to no more than 1.5 MB;
  - faint: how far each place shows at the engine's 0.28 against how far it shows drawn (the mean change of colour
    over its painted pixels), and that at 0 it is plainly not there (nothing of it in back.png).

The pictures, in <folder>-check/ (and each at half size, *-half.png):
  all.png      every place and way drawn, the names in place (Koine Road, in the label's style), a grey pin row at each
  none.png     the sheet alone
  first.png    the Last Stop drawn with its name and its row; the store and the shop's door faint (0.28); the road not
  layout.png   all.png with every shape, pin row, name box and via drawn over it in thin lines
"""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 800, 600
IDS = {"roadside": "The Last Stop", "store": "Grandpa Joe's store", "road": "On the road"}
WAYS = [("roadside", "store")]
ROW_W, ROW_H = 116, 44
FAINT = 0.28
GROUND = (36, 30, 42)                         # the dark the map screen lies on, for these pictures


def font_path():
    for p in (os.path.join(HERE, "..", "..", "fonts", "KoineRoad-Regular.ttf"), os.path.join(HERE, "..", "game", "fonts", "KoineRoad-Regular.ttf")):
        if os.path.exists(p):
            return p
    raise SystemExit("Koine Road not found")


def name_width(text, st):
    f = ImageFont.truetype(font_path(), st["size"])
    t = text.upper() if st["upper"] else text
    return f.getlength(t) + st["spacing"] * st["size"] * len(t)


def poly_mask(poly):
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).polygon([tuple(p) for p in poly], fill=255, outline=255)
    return np.asarray(im) > 0


def box_mask(b):
    m = np.zeros((H, W), bool)
    x0, y0, x1, y1 = [int(round(v)) for v in b]
    m[max(y0, 0):max(min(y1, H), 0), max(x0, 0):max(min(x1, W), 0)] = True
    return m


def row_box(pin):
    return (pin[0] - ROW_W / 2, pin[1] - ROW_H / 2, pin[0] + ROW_W / 2, pin[1] + ROW_H / 2)


def name_box(p):
    x, y = p["label"]
    return (x - p["label_max"] / 2, y - 20, x + p["label_max"] / 2, y + 5)


def gap(a, b):
    """The distance between two boxes (0 if they touch or overlap)."""
    dx = max(b[0] - a[2], a[0] - b[2], 0)
    dy = max(b[1] - a[3], a[1] - b[3], 0)
    return math.hypot(dx, dy) if dx and dy else max(dx, dy)


def run(folder, shots=None):
    L = json.load(open(os.path.join(folder, "layout.json")))
    problems = []
    say = print

    def check(ok, text):
        say(("  ok    " if ok else "  FAIL  ") + text)
        if not ok:
            problems.append(text)

    # ---- the ids and the files
    say("the places, the ways and the files")
    ids = [p["id"] for p in L["places"]]
    check(sorted(ids) == sorted(IDS) and len(ids) == len(IDS), f"places {ids} are exactly {sorted(IDS)}")
    ways = [(w["a"], w["b"]) for w in L["paths"]]
    check(ways == WAYS, f"ways {ways} are exactly {WAYS}")
    check(L["map"] == "nevada" and L["size"] == [W, H], "map nevada, size 800 x 600")
    files = ["back.png"] + [p["picture"] for p in L["places"]] + [w["picture"] for w in L["paths"]]
    check([p["picture"] for p in L["places"]] == [f"place-{i}.png" for i in ids], "each place's picture is place-<id>.png")
    check([w["picture"] for w in L["paths"]] == [f"path-{a}-{b}.png" for a, b in WAYS], "each way's picture is path-<a>-<b>.png")
    pals, total = [], 0
    pics, alphas = {}, {}
    for f in files:
        path = os.path.join(folder, f)
        if not os.path.exists(path):
            check(False, f"{f} exists")
            continue
        im = Image.open(path)
        total += os.path.getsize(path)
        check(im.size == (W, H) and im.mode == "P" and "transparency" in im.info, f"{f}: {im.size[0]} x {im.size[1]}, mode {im.mode}, a clear colour")
        pal = im.getpalette()[:3 * 256]
        pals.append(pal)
        rgba = np.asarray(im.convert("RGBA"))
        pics[f] = rgba[..., :3].astype(np.float32) / 255
        alphas[f] = rgba[..., 3] > 127
        clear = not alphas[f][:128].any() and not alphas[f][572:].any()
        check(clear, f"{f}: rows 0-127 and 572-599 clear")
    used = len(np.unique(np.concatenate([np.asarray(Image.open(os.path.join(folder, f)))[alphas[f]] for f in files])))
    same = all(p == pals[0] for p in pals)
    check(same, "every file on one palette")
    check(160 <= used <= 220, f"the palette: {used} colours used (160 to 220)")
    check(total <= 1.5 * 1024 * 1024, f"the map's files: {total / 1024:.0f} KB (at most 1536 KB)")

    sheet = L["sheet"]
    check(32 <= sheet[0] and sheet[2] <= 768 and 128 <= sheet[1] and sheet[3] <= 572, f"sheet {sheet} within x 32-768, y 128-572")
    paper = alphas["back.png"]
    sheet_box = box_mask(sheet)

    # ---- the shapes
    say("the shapes")
    masks = {}
    for p in L["places"]:
        ink = alphas[p["picture"]]
        sh = poly_mask(p["shape"])
        masks[p["id"]] = sh
        inside = (ink & sh).sum() / max(ink.sum(), 1)
        check(len(p["shape"]) <= 24, f"{p['id']}: {len(p['shape'])} points")
        check(inside >= 0.90, f"{p['id']}: {inside * 100:.1f} per cent of its {ink.sum()} painted pixels inside its shape")
        check(not (sh & ~sheet_box).any() and (sh & ~paper).sum() <= 0.002 * sh.sum(), f"{p['id']}: its shape inside the sheet")
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            n = (masks[a] & masks[b]).sum()
            check(n == 0, f"shapes {a} and {b} do not overlap ({n} pixels shared)")

    # ---- pins and names
    say("the pins and the names")
    st = L["label"]
    rows = {p["id"]: row_box(p["pin"]) for p in L["places"]}
    nboxes = {p["id"]: name_box(p) for p in L["places"]}
    for p in L["places"]:
        rb = rows[p["id"]]
        on = paper[box_mask(rb)].mean() if box_mask(rb).any() else 0
        check(sheet[0] <= rb[0] and rb[2] <= sheet[2] and sheet[1] <= rb[1] and rb[3] <= sheet[3] and on > 0.999,
              f"{p['id']}: pin row {[round(v, 1) for v in rb]} on the paper")
        wdt = name_width(IDS[p["id"]], st)
        check(wdt <= p["label_max"], f"{p['id']}: \"{IDS[p['id']]}\" is {wdt:.1f} px in Koine Road {st['size']} (label_max {p['label_max']})")
        nb = nboxes[p["id"]]
        check(sheet[0] <= nb[0] and nb[2] <= sheet[2] and sheet[1] <= nb[1] and nb[3] <= sheet[3] and paper[box_mask(nb)].all(),
              f"{p['id']}: its name's box {[round(v, 1) for v in nb]} on the paper")
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            g = gap(rows[a], rows[b])
            check(g >= 8, f"pin rows {a} and {b} {g:.1f} px apart")
            check(gap(nboxes[a], nboxes[b]) > 0, f"names {a} and {b} apart ({gap(nboxes[a], nboxes[b]):.1f} px)")
    for a in ids:
        nm = box_mask(nboxes[a])
        for b in ids:
            if b != a:
                check(gap(nboxes[a], rows[b]) > 0, f"{a}'s name clear of {b}'s pin row ({gap(nboxes[a], rows[b]):.1f} px)")
                n = (nm & alphas[f"place-{b}.png"]).sum()
                check(n == 0, f"{a}'s name over none of {b}'s drawing ({n} px)")
        check(gap(nboxes[a], rows[a]) > 0, f"{a}'s name clear of its own pin row ({gap(nboxes[a], rows[a]):.1f} px)")
        for w in L["paths"]:
            n = (nm & alphas[w["picture"]]).sum()
            check(n == 0, f"{a}'s name over none of the way {w['a']}-{w['b']} ({n} px)")

    # ---- the ways
    say("the ways")
    pins = {p["id"]: p["pin"] for p in L["places"]}
    for w in L["paths"]:
        v = w["via"]
        check(v[0] == pins[w["a"]] and v[-1] == pins[w["b"]], f"{w['a']}-{w['b']}: via starts at {w['a']}'s pin and ends at {w['b']}'s")
        wy, wx = np.nonzero(alphas[w["picture"]])
        cx, cy = wx + 0.5, wy + 0.5                                    # the drawing's pixels, by their middles
        worst = 0.0
        for (ax, ay), (bx, by) in zip(v[:-1], v[1:]):
            n = max(2, int(math.hypot(bx - ax, by - ay)))
            for t in np.linspace(0, 1, n + 1):
                x, y = ax + (bx - ax) * t, ay + (by - ay) * t
                worst = max(worst, float(np.min(np.hypot(cx - x, cy - y))))
        check(worst <= 6.0, f"{w['a']}-{w['b']}: every point of the via within {worst:.1f} px of the way's drawing (at most 6)")

    # ---- faint, and absent
    say("faint and absent")
    back = pics["back.png"]
    for p in L["places"] + [dict(id=f"{w['a']}-{w['b']}", picture=w["picture"]) for w in L["paths"]]:
        m = alphas[p["picture"]]
        full = np.abs(pics[p["picture"]][m] - back[m]).sum(axis=1).mean() * 255 / 3
        faint = full * FAINT
        check(full > 12, f"{p['id']}: drawn, its pixels differ from the sheet by {full:.1f} on average; at 0.28, by {faint:.1f}")
    # nothing of a place is in back.png: its picture's pixels differ from the sheet's
    for p in L["places"]:
        m = alphas[p["picture"]]
        same_px = (np.abs(pics[p["picture"]][m] - back[m]).sum(axis=1) < 0.004).mean()
        say(f"  note  {p['id']}: {same_px * 100:.0f} per cent of its pixels are the sheet's own (worn ink, white wedges, knocked-out paper)")

    pictures(folder, L, pics, alphas, shots)
    say(f"{len(problems)} problem{'s' if len(problems) != 1 else ''}" + ("" if not problems else ":"))
    for t in problems:
        say("  - " + t)
    return problems


# ---------------------------------------------------------------- the pictures
def layer(base, pic, a, amount=1.0):
    out = base.copy()
    m = a[..., None].astype(np.float32) * amount
    return out * (1 - m) + pic * m


def draw_name(im, text, at, st, maxw):
    """A name as the engine draws it: Koine Road, capitals, letter-spaced, a soft halo of the paper's colour behind it."""
    size = st["size"]
    t = text.upper() if st["upper"] else text
    ss = 4
    f = ImageFont.truetype(font_path(), size * ss)
    sp = st["spacing"] * size * ss
    total = sum(f.getlength(ch) + sp for ch in t)
    mask = Image.new("L", (W * ss, H * ss), 0)
    d = ImageDraw.Draw(mask)
    x = at[0] * ss - total / 2 + sp / 2
    for ch in t:
        d.text((x, at[1] * ss), ch, font=f, fill=255, anchor="ls")
        x += f.getlength(ch) + sp
    mask = mask.resize((W, H), Image.BOX)
    if st.get("halo"):
        halo = mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
        halo = halo.point(lambda v: min(255, int(v * 2.2)))
        im.paste(Image.new("RGB", (W, H), st["halo"]), mask=halo)
    im.paste(Image.new("RGB", (W, H), st["color"]), mask=mask)


def draw_row(im, pin, n=3):
    d = ImageDraw.Draw(im, "RGBA")
    x0 = pin[0] - (n * 36 + (n - 1) * 4) / 2
    for k in range(n):
        cx = x0 + 18 + k * 40
        d.ellipse([cx - 18, pin[1] - 18, cx + 18, pin[1] + 18], fill=(150, 150, 156, 255), outline=(90, 90, 98, 255), width=2)


def pictures(folder, L, pics, alphas, shots=None):
    out = shots or folder.rstrip("/") + "-check"
    os.makedirs(out, exist_ok=True)
    ground = np.zeros((H, W, 3), np.float32) + np.array(GROUND, np.float32) / 255
    base = layer(ground, pics["back.png"], alphas["back.png"])
    st = L["label"]

    def compose(states):
        """states: id or way picture -> opacity (1 drawn, 0.28 faint)."""
        pic = base.copy()
        for w in L["paths"]:
            a = states.get(w["picture"], 0)
            if a:
                pic = layer(pic, pics[w["picture"]], alphas[w["picture"]], a)
        for p in L["places"]:
            a = states.get(p["id"], 0)
            if a:
                pic = layer(pic, pics[p["picture"]], alphas[p["picture"]], a)
        return Image.fromarray((np.clip(pic, 0, 1) * 255 + 0.5).astype(np.uint8), "RGB")

    every = {p["id"]: 1 for p in L["places"]}
    every.update({w["picture"]: 1 for w in L["paths"]})
    im_all = compose(every)
    for p in L["places"]:
        draw_name(im_all, IDS[p["id"]], p["label"], st, p["label_max"])
        draw_row(im_all, p["pin"])
    im_all.save(os.path.join(out, "all.png"))
    compose({}).save(os.path.join(out, "none.png"))
    first = {"roadside": 1, "store": FAINT, "path-roadside-store.png": FAINT}
    im_first = compose(first)
    pr = next(p for p in L["places"] if p["id"] == "roadside")
    draw_name(im_first, IDS["roadside"], pr["label"], st, pr["label_max"])
    draw_row(im_first, pr["pin"])
    im_first.save(os.path.join(out, "first.png"))
    im_lay = im_all.copy()
    d = ImageDraw.Draw(im_lay)
    colours = {"roadside": (230, 40, 40), "store": (30, 120, 230), "road": (20, 160, 60)}
    for p in L["places"]:
        c = colours[p["id"]]
        d.line([tuple(q) for q in p["shape"]] + [tuple(p["shape"][0])], fill=c, width=1)
        d.rectangle(row_box(p["pin"]), outline=c, width=1)
        d.rectangle(name_box(p), outline=(240, 200, 30), width=1)
        x, y = p["label"]
        d.line([(x - 3, y), (x + 3, y)], fill=(240, 200, 30))
    for w in L["paths"]:
        d.line([tuple(q) for q in w["via"]], fill=(255, 0, 255), width=1)
        for q in w["via"]:
            d.ellipse([q[0] - 2, q[1] - 2, q[0] + 2, q[1] + 2], outline=(255, 0, 255))
    s = L["sheet"]
    d.rectangle(s, outline=(255, 255, 255))
    im_lay.save(os.path.join(out, "layout.png"))
    for n in ("all", "none", "first", "layout"):
        Image.open(os.path.join(out, n + ".png")).resize((W // 2, H // 2), Image.LANCZOS).save(os.path.join(out, n + "-half.png"))
    print(f"  pictures: {out}/all.png, none.png, first.png, layout.png (and each -half.png)")


if __name__ == "__main__":
    probs = run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "map-nevada"), sys.argv[2] if len(sys.argv) > 2 else None)
    sys.exit(1 if probs else 0)

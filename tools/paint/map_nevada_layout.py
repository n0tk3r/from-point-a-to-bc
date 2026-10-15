"""The Nevada map's layout.json (MAP-15N), every number measured from the finished pictures in out/map-nevada/.

    python3 map_nevada_layout.py [folder]

What it measures, and how:
  sheet      the box of back.png's paper (its alpha).
  label      the names' style: the colour of the key plate's ink and of the paper, both read off back.png (the detail
             panel's printed title, and its empty paper); capitals, a little letter-spacing, 14 pixels.
  shape      each place's outline: its picture's ink, swollen a few pixels so its pieces join, holes filled, traced
             round, and simplified to at most 24 points; the Last Stop's lot is cut back clear of the store's outline
             (the store lies inside the lot, in the shack's walls), so that no two outlines overlap.
  pin        where the portraits stand. The way's arrow runs from the lot in at the shop's door: the Last Stop's pin is
             its tail (on the lot, at the door) and the store's its tip (inside, on the floor). On the road: over the
             middle of the picked-out stretch, a row's half-height and a little more clear of its line.
  label      each name centred on its place: the store's printed on the paper just above the shack, the Last Stop's on
             the lot under the family's row, On the road's under the stretch. label_max is the name's width in Koine
             Road at the label size and spacing, in capitals, and a little room.
  via        the way's line: down the arrow's shaft, from the Last Stop's pin to the store's.
"""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
MAP = "nevada"
W, H = 800, 600
PLACES = [("roadside", "The Last Stop"), ("store", "Grandpa Joe's store"), ("road", "On the road")]
PATHS = [("roadside", "store")]
LABEL = dict(upper=True, spacing=0.06, size=14)
ROW = (116, 44)                                  # a pin row of three portraits: 3 x 36 + 2 x 4 across, 22 above and below
MATERIAL = ("a fold-out road map from a filling station's rack, opened flat: thin yellowed paper creased in a grid of "
            "twelve panels, printed in a few flat inks a little out of register")
NOTE = ("The Last Stop and the store are drawn in the detail panel (top right): the lot in plan, and inside the shack's "
        "walls the store in plan; the store's outline lies inside the lot's, which is cut back round it. The No Gas "
        "sign on the main map's highway is the Last Stop's too (outside its outline: a symbol, not a place to click). "
        "On the road has no way. Names are printed on the paper's colour, as a road map knocks the land out behind "
        "its lettering.")


def font_path():
    for p in (os.path.join(HERE, "..", "..", "fonts", "KoineRoad-Regular.ttf"), os.path.join(HERE, "..", "game", "fonts", "KoineRoad-Regular.ttf")):
        if os.path.exists(p):
            return p
    raise SystemExit("Koine Road not found")


def name_width(text, style=LABEL):
    """How wide a name is drawn: Koine Road at the label size, capitals if asked, with the letter-spacing after each
    letter (as CSS lays it)."""
    f = ImageFont.truetype(font_path(), style["size"])
    t = text.upper() if style["upper"] else text
    return f.getlength(t) + style["spacing"] * style["size"] * len(t)


def alpha(folder, name):
    return np.asarray(Image.open(os.path.join(folder, name)).convert("RGBA"))[..., 3] > 127


def rgb(folder, name):
    return np.asarray(Image.open(os.path.join(folder, name)).convert("RGB")).astype(np.int32)


# ---------------------------------------------------------------- masks and outlines (numpy and Pillow only)
def dilate(m, r):
    """Swell a mask by r pixels (a disc)."""
    out = m.copy()
    rr = int(math.ceil(r))
    for dy in range(-rr, rr + 1):
        for dx in range(-rr, rr + 1):
            if dx * dx + dy * dy <= r * r and (dx or dy):
                sh = np.zeros_like(m)
                ys = slice(max(dy, 0), H + min(dy, 0))
                yd = slice(max(-dy, 0), H + min(-dy, 0))
                xs = slice(max(dx, 0), W + min(dx, 0))
                xd = slice(max(-dx, 0), W + min(-dx, 0))
                sh[ys, xs] = m[yd, xd]
                out |= sh
    return out


def fill_holes(m):
    """Fill every hole of a mask (whatever the outside cannot reach)."""
    im = Image.fromarray(np.pad(m, 1).astype(np.uint8) * 255, "L").copy()          # (a copy: one made from an array is read-only)
    ImageDraw.floodfill(im, (0, 0), 128)
    a = np.asarray(im)[1:-1, 1:-1]
    return a != 128


def components(m):
    """The mask's 8-connected pieces, largest first, each as a mask."""
    lab = np.zeros(m.shape, np.int32)
    n = 0
    sizes = []
    ys, xs = np.nonzero(m)
    for y0, x0 in zip(ys, xs):
        if lab[y0, x0]:
            continue
        n += 1
        stack = [(y0, x0)]
        lab[y0, x0] = n
        count = 0
        while stack:
            y, x = stack.pop()
            count += 1
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < H and 0 <= xx < W and m[yy, xx] and not lab[yy, xx]:
                        lab[yy, xx] = n
                        stack.append((yy, xx))
        sizes.append((count, n))
    sizes.sort(reverse=True)
    return [lab == k for _, k in sizes]


def trace(m):
    """The outer boundary of a mask's one piece, as pixel points in order (Moore-neighbour tracing)."""
    p = np.pad(m, 1)
    ys, xs = np.nonzero(p)
    i = np.lexsort((xs, ys))[0]
    start = (int(xs[i]), int(ys[i]))
    nb = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]       # clockwise from the west
    b0 = (start[0] - 1, start[1])
    c, b = start, b0
    out = [start]
    for _ in range(200000):
        k = nb.index((b[0] - c[0], b[1] - c[1]))
        for j in range(1, 9):
            kk = (k + j) % 8
            q = (c[0] + nb[kk][0], c[1] + nb[kk][1])
            if p[q[1], q[0]]:
                pk = (k + j - 1) % 8
                b = (c[0] + nb[pk][0], c[1] + nb[pk][1])
                c = q
                break
        else:
            break
        if c == start and b == b0:
            break
        if c == start and len(out) > 2 and out[1] == next_of(p, c, b, nb):
            break
        out.append(c)
    return [(x - 1, y - 1) for x, y in out]


def next_of(p, c, b, nb):
    k = nb.index((b[0] - c[0], b[1] - c[1]))
    for j in range(1, 9):
        kk = (k + j) % 8
        q = (c[0] + nb[kk][0], c[1] + nb[kk][1])
        if p[q[1], q[0]]:
            return q
    return None


def dp(points, eps):
    """Douglas-Peucker on an open polyline."""
    if len(points) < 3:
        return list(points)
    a, b = np.asarray(points[0], float), np.asarray(points[-1], float)
    pts = np.asarray(points, float)
    d = b - a
    n = math.hypot(*d)
    if n < 1e-9:
        dist = np.hypot(*(pts - a).T)
    else:
        dist = np.abs(d[0] * (pts[:, 1] - a[1]) - d[1] * (pts[:, 0] - a[0])) / n
    i = int(np.argmax(dist))
    if dist[i] > eps:
        return dp(points[:i + 1], eps)[:-1] + dp(points[i:], eps)
    return [points[0], points[-1]]


def simplify(ring, most=24):
    """A closed outline simplified until it has at most `most` points."""
    pts = np.asarray(ring, float)
    c = pts.mean(axis=0)
    i0 = int(np.argmax(np.hypot(*(pts - c).T)))
    i1 = int(np.argmax(np.hypot(*(pts - pts[i0]).T)))
    a, b = sorted((i0, i1))
    eps = 0.8
    while True:
        half1 = dp(ring[a:b + 1], eps)
        half2 = dp(ring[b:] + ring[:a + 1], eps)
        poly = half1[:-1] + half2[:-1]
        if len(poly) <= most:
            return [[float(x), float(y)] for x, y in poly]
        eps *= 1.15


def poly_mask(poly):
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).polygon([tuple(p) for p in poly], fill=255, outline=255)
    return np.asarray(im) > 0


def outline(m, swell, most=24, keep=None):
    """A place's outline: its ink swollen by `swell`, holes filled, the largest piece (or the piece holding `keep`),
    traced and simplified; pushed out a pixel so that it lies round the ink rather than through it."""
    big = fill_holes(dilate(m, swell))
    parts = components(big)
    part = parts[0] if keep is None else next(p for p in parts if p[keep[1], keep[0]])
    ring = trace(part)
    return simplify(ring, most)


# ---------------------------------------------------------------- the measurements
def write(folder):
    back = alpha(folder, "back.png")
    ys, xs = np.nonzero(back)
    sheet = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    pic = rgb(folder, "back.png")

    # the label style, read off the sheet: the key ink (the detail's printed title), the paper (the detail's paper)
    lot = alpha(folder, "place-roadside.png")
    store = alpha(folder, "place-store.png")
    road = alpha(folder, "place-road.png")
    way = alpha(folder, "path-roadside-store.png")
    lot_parts = components(lot)
    lys, lxs = np.nonzero(lot_parts[0])
    top = int(lys.min())                                                 # the top of the detail's drawing room
    band = pic[top - 18:top - 3, int(lxs.min()):int(lxs.max())].reshape(-1, 3)     # the detail's printed title
    lum = band @ np.array([0.3, 0.55, 0.15])
    ink = np.median(band[lum <= np.percentile(lum, 1.0)], axis=0)
    paper = np.median(band[lum >= np.percentile(lum, 60)], axis=0)
    hexs = lambda c: "#%02x%02x%02x" % tuple(int(round(v)) for v in c)
    label = dict(color=hexs(ink), halo=hexs(paper), upper=LABEL["upper"], spacing=LABEL["spacing"], size=LABEL["size"])

    # the way's arrow: its shaft's column, its tip (inside) and its tail (on the lot)
    wy, wx = np.nonzero(way)
    col = float(np.median(wx))
    tip, tail = float(wy.min()), float(wy.max())
    tail_dot = wy[wy > tail - 6]
    store_pin = [round(col, 1), round(tip + 1.5, 1)]
    lot_pin = [round(col, 1), round(float(np.mean(tail_dot)), 1)]

    # the road: the middle of the picked-out stretch, and the line's middle there
    ry, rx = np.nonzero(road)
    rmid = 0.5 * (rx.min() + rx.max())
    line_here = ry[np.abs(rx - rmid) < 1.5]
    road_line = float(np.median(line_here))
    road_pin = [round(float(rmid), 1), round(road_line - ROW[1] / 2 - 6.0, 1)]

    # the outlines: the store's from its ink; the lot's from its ink in the detail, cut back clear of the store's;
    # the road's from its ink
    store_shape = outline(store, 3.0)
    lot_ink = lot_parts[0]
    store_area = poly_mask(store_shape)
    for margin in (2.5, 3.5, 4.5, 6.0, 8.0):                             # cut the lot back until the outlines part
        lot_shape = outline(lot_ink & ~dilate(store_area, margin), 2.0, keep=(int(lot_pin[0]), int(lot_pin[1]) + 6))
        if not (poly_mask(lot_shape) & store_area).any():
            break
    road_shape = outline(road, 3.0)

    # the names: the store's on the paper just above the shack, the lot's under the family's row, the road's under the
    # stretch; each centred on its place's pin, at a baseline found clear of everything else
    names = {pid: name for pid, name in PLACES}
    sy, sx = np.nonzero(store)
    store_top = float(sy.min())                                          # the highest of its ink (the hen yard's wire)
    store_label = [round(lot_pin[0], 1), round(store_top - 5.5, 1)]
    lot_label = [round(lot_pin[0], 1), round(lot_pin[1] + ROW[1] / 2 + 4.0 + 20.0, 1)]
    road_bottom = float(np.max(ry[np.abs(rx - rmid) < 1.5]))
    road_label = [round(road_pin[0], 1), round(road_bottom + 4.0 + 20.0, 1)]

    def lmax(pid):
        return int(math.ceil(name_width(names[pid]) + 10))

    # each name then slides (up for the store's, down for the others) until its box is clear of every other place's
    # ink, the way's, and every pin row
    inks = {"roadside": lot, "store": store, "road": road}
    rows = {"roadside": lot_pin, "store": store_pin, "road": road_pin}

    def clear(pid, at, step):
        x, y = at
        half = lmax(pid) / 2
        for _ in range(40):
            box = np.zeros((H, W), bool)
            box[int(math.floor(y - 20)):int(math.ceil(y + 5)), int(math.floor(x - half)):int(math.ceil(x + half))] = True
            hit = way[box].any() or any(inks[o][box].any() for o in inks if o != pid)
            for o, pin in rows.items():
                rx0, ry0 = pin[0] - ROW[0] / 2, pin[1] - ROW[1] / 2
                if not (x + half <= rx0 or x - half >= rx0 + ROW[0] or y + 5 <= ry0 or y - 20 >= ry0 + ROW[1]):
                    hit = True
            if not hit:
                return [round(x, 1), round(y, 1)]
            y += step
        raise SystemExit(f"no clear place for {pid}'s name")
    store_label = clear("store", store_label, -0.5)
    lot_label = clear("roadside", lot_label, 0.5)
    road_label = clear("road", road_label, 0.5)

    places = [
        dict(id="roadside", picture="place-roadside.png", shape=lot_shape, pin=lot_pin, label=lot_label, label_max=lmax("roadside")),
        dict(id="store", picture="place-store.png", shape=store_shape, pin=store_pin, label=store_label, label_max=lmax("store")),
        dict(id="road", picture="place-road.png", shape=road_shape, pin=road_pin, label=road_label, label_max=lmax("road")),
    ]
    paths = [dict(a="roadside", b="store", picture="path-roadside-store.png", via=[lot_pin, [round(col, 1), round(0.5 * (lot_pin[1] + store_pin[1]), 1)], store_pin])]
    layout = dict(map=MAP, size=[W, H], sheet=sheet, material=MATERIAL, label=label, places=places, paths=paths, note=NOTE)
    with open(os.path.join(folder, "layout.json"), "w") as f:
        json.dump(layout, f, indent=1)
        f.write("\n")
    print(f"layout.json: sheet {sheet}; label {label['color']} on {label['halo']}; "
          + "; ".join(f"{p['id']} pin {p['pin']} label {p['label']} ({p['label_max']}), {len(p['shape'])} points" for p in places))
    return layout


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "map-nevada"))

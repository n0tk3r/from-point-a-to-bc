"""layout.json for the map of Egypt (MAP-15E), measured from the finished pictures in out/map-egypt/.

    python3 map_egypt_layout.py       (map_egypt.py runs it at the end of a full run)

Nothing here is typed in: the sheet's box is the papyrus's own extent; each place's shape is drawn round its own
painted pixels; each way's via is walked along its own painted line, point by point; each pin is where a place's
ways end on the paint (the portraits stand where the ways arrive); each name is set where the search below finds the
nearest free place for it, clear of every other drawing, way, pin row and name, and of the river, and as clear as can
be of the sheet's own lines."""

import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import map_egypt_kit as K

OUT = K.OUT
PLACES = ["river", "site", "gallery", "chamber"]
WAYS = [("river", "site"), ("site", "gallery"), ("gallery", "chamber")]
NAMES = {"river": "By the river", "site": "The foot of the pyramid", "gallery": "The great gallery", "chamber": "The burial chamber"}
LABEL = {"color": K.hexof(K.darker(K.mix(("prussian-blue", 5), ("burnt-sienna", 4), ("yellow-ochre", 1)), 0.55)),
         "halo": K.hexof(K.HALO), "upper": False, "spacing": 0.03, "size": 15}
ROW = (76, 44)                    # two portraits at most on this map: discs 36 across, 4 between
FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "game", "fonts", "KoineRoad-Regular.ttf")
if not os.path.exists(FONT):
    FONT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "fonts", "KoineRoad-Regular.ttf")


def alpha_of(path):
    return np.asarray(Image.open(path).convert("RGBA"))[..., 3] > 127


def rgb_of(path):
    return np.asarray(Image.open(path).convert("RGBA"))[..., :3].astype(np.float32) / 255


def text_width(text, label=LABEL):
    f = ImageFont.truetype(FONT, label["size"])
    t = text.upper() if label["upper"] else text
    return f.getlength(t) + label["spacing"] * label["size"] * len(t)


# ---------------------------------------------------------------- shapes


def dilate(mask, r):
    if r <= 0:
        return mask
    im = Image.fromarray((mask * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.MaxFilter(2 * r + 1))) > 127


def rdp(points, eps):
    """Douglas-Peucker on an open chain."""
    if len(points) < 3:
        return list(points)
    P = np.array(points, float)
    a, b = P[0], P[-1]
    ab = b - a
    n = math.hypot(*ab)
    if n < 1e-9:
        d = np.hypot(*(P - a).T)
    else:
        d = np.abs(ab[0] * (P[:, 1] - a[1]) - ab[1] * (P[:, 0] - a[0])) / n
    i = int(d.argmax())
    if d[i] > eps:
        return rdp(points[:i + 1], eps)[:-1] + rdp(points[i:], eps)
    return [points[0], points[-1]]


def raster(poly, shape=K.SHAPE):
    im = Image.new("L", (shape[1], shape[0]), 0)
    ImageDraw.Draw(im).polygon([tuple(p) for p in poly], fill=255)
    return np.asarray(im) > 127


def erode(mask, r):
    return ~dilate(~mask, r) if r > 0 else mask


def territories(masks, reach=40):
    """Every pixel near the drawings given to the nearest one, grown out a pixel at a time: {name: its ground}."""
    names = list(masks)
    lab = np.zeros(K.SHAPE, np.int16)
    for i, k in enumerate(names):
        lab[masks[k] & (lab == 0)] = i + 1
    for _ in range(reach):
        claim = np.zeros(K.SHAPE, np.int16)
        for i in range(len(names)):
            grown = dilate(lab == i + 1, 1) & (lab == 0) & (claim == 0)
            claim[grown] = i + 1
        if not claim.any():
            break
        lab[claim > 0] = claim[claim > 0]
    return {k: lab == i + 1 for i, k in enumerate(names)}


def envelope(m, bin_=2):
    """The upper and lower edge of a region, column by column (left to right)."""
    cols = np.nonzero(m.any(axis=0))[0]
    top, bot = [], []
    for x in range(int(cols.min()), int(cols.max()) + 1, bin_):
        col = m[:, x:min(x + bin_, m.shape[1])]
        rows = np.nonzero(col.any(axis=1))[0]
        if len(rows):
            xe = min(x + bin_ - 1, int(cols.max()))
            top += [(x, int(rows.min())), (xe, int(rows.min()))]
            bot += [(x, int(rows.max())), (xe, int(rows.max()))]
    return top, bot


def shape_of(mask, ground, sheet, pad=3, most=24):
    """A polygon of at most `most` points hugging a drawing, a few pixels out from it, kept within the drawing's own
    ground (so that no two places' shapes meet) and on the sheet."""
    for eps in (1.0, 1.3, 1.7, 2.2, 2.8, 3.5, 4.4, 5.5, 7.0):
        allowed = erode(ground, int(math.ceil(eps)) + 2) & erode(sheet, int(math.ceil(eps)) + 2)
        m = dilate(mask, int(round(pad + eps))) & allowed
        top, bot = envelope(m)
        poly = rdp(top, eps) + rdp(bot[::-1], eps)
        clean = [poly[0]]
        for p in poly[1:]:
            if p != clean[-1]:
                clean.append(p)
        if clean[-1] == clean[0]:
            clean.pop()
        if len(clean) <= most:
            return [[int(x), int(y)] for x, y in clean]
    return [[int(x), int(y)] for x, y in clean[:most]]


# ---------------------------------------------------------------- ways


def walk(route, mask, reach=5.0, every=6.0):
    """A way's line, measured: points along its route each moved onto the middle of the paint across it there."""
    ys, xs = np.nonzero(mask)
    pts = np.stack([xs, ys], 1).astype(float)
    P = np.array(route, float)
    seg = np.hypot(*(P[1:] - P[:-1]).T)
    L = np.concatenate([[0], np.cumsum(seg)])
    out = []
    n = max(2, int(L[-1] / every) + 1)
    for s in np.linspace(0, L[-1], n):
        q = np.array([np.interp(s, L, P[:, 0]), np.interp(s, L, P[:, 1])])
        d = np.hypot(*(pts - q).T)
        near = pts[d <= reach]
        out.append(tuple(near.mean(axis=0)) if len(near) else tuple(q))
    return out


def simplify(points, eps=1.5):
    return rdp([tuple(p) for p in points], eps)


# ---------------------------------------------------------------- names


def row_box(pin):
    return (pin[0] - ROW[0] / 2, pin[1] - ROW[1] / 2, pin[0] + ROW[0] / 2, pin[1] + ROW[1] / 2)


def name_box(label, wmax):
    return (label[0] - wmax / 2, label[1] - 20, label[0] + wmax / 2, label[1] + 5)


def boxes_meet(a, b, gap=0.0):
    return not (a[2] + gap <= b[0] or b[2] + gap <= a[0] or a[3] + gap <= b[1] or b[3] + gap <= a[1])


def place_names(drawn, ways, ink, sheet, pins, river_band, inside_pyramid):
    """Set each name where it is nearest its own place, on the sheet, clear of every other place's drawing, every
    way, every pin row and every name already set, off the river, and on the quietest papyrus it can find. The
    gallery's and the chamber's names would rather be inside the Horizon's outline; the others, outside it."""
    order = ["chamber", "gallery", "site", "river"]             # the most hemmed in first
    widths = {k: text_width(NAMES[k]) for k in NAMES}
    sheet_in = erode(sheet, 6)
    placed = {}
    integral = lambda m: np.pad(m.astype(np.int32).cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    def count(I, b):
        x0, y0, x1, y1 = [int(round(v)) for v in b]
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(K.W, x1), min(K.H, y1)
        if x1 <= x0 or y1 <= y0:
            return 0
        return int(I[y1, x1] - I[y0, x1] - I[y1, x0] + I[y0, x0])
    I_sheet_out = integral(~sheet_in)
    I_river = integral(river_band)
    I_ink = integral(ink)
    I_pyr = integral(inside_pyramid)
    result = {}
    for k in order:
        wmax = math.ceil(widths[k] + 10)
        own = drawn[k]
        foreign = ways.copy()
        for j, m in drawn.items():
            if j != k:
                foreign |= m
        I_foreign = integral(dilate(foreign, 3))
        I_own = integral(dilate(own, 2))
        ys, xs = np.nonzero(own)
        cx, cy = xs.mean(), ys.mean()
        own_pts = np.stack([xs[::7], ys[::7]], 1).astype(float)
        best = None
        for by in range(max(150, int(cy) - 150), min(560, int(cy) + 150), 2):
            for bx in range(max(60, int(cx) - 220), min(744, int(cx) + 220), 2):
                b = name_box((bx, by), wmax)
                if b[0] < 44 or b[2] > 756 or b[1] < 140 or b[3] > 558:
                    continue
                if count(I_sheet_out, b) or count(I_foreign, b) or count(I_river, b):
                    continue
                if any(boxes_meet(b, row_box(p), 2) for p in pins.values()):
                    continue
                if any(boxes_meet(b, name_box(placed[j][0], placed[j][1]), 4) for j in placed):
                    continue
                if count(I_own, b):                                      # (not over its own drawing either)
                    continue
                mx, my = bx, by - 7.5
                dmin = float(np.min(np.hypot(own_pts[:, 0] - mx, own_pts[:, 1] - my)))
                pyr = count(I_pyr, b) / ((b[2] - b[0]) * (b[3] - b[1]))
                wants_in = k in ("gallery", "chamber")
                score = dmin + 0.9 * count(I_ink, b) + (40.0 * (1 - pyr) if wants_in else 60.0 * pyr)
                if best is None or score < best[0]:
                    best = (score, (bx, by))
        if best is None:
            raise SystemExit(f"no room for the name of {k}")
        placed[k] = (best[1], wmax)
        result[k] = {"label": [int(best[1][0]), int(best[1][1])], "label_max": int(wmax)}
    return result


# ---------------------------------------------------------------- the whole


def tidy(d):
    lines = []
    for k, v in d.items():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            inner = ",\n".join("    " + json.dumps(e) for e in v)
            lines.append(f"  {json.dumps(k)}: [\n{inner}\n  ]")
        else:
            lines.append(f"  {json.dumps(k)}: {json.dumps(v)}")
    return "{\n" + ",\n".join(lines) + "\n}\n"


def measure(routes):
    sheet = alpha_of(os.path.join(OUT, "back.png"))
    ys, xs = np.nonzero(sheet)
    box = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    drawn = {k: alpha_of(os.path.join(OUT, f"place-{k}.png")) for k in PLACES}
    ways = {w: alpha_of(os.path.join(OUT, f"path-{w[0]}-{w[1]}.png")) for w in WAYS}
    # the ways, walked along their paint; their ends, where they meet at a place, are the pins
    walked = {w: walk(routes[w], ways[w]) for w in WAYS}
    ends = {k: [] for k in PLACES}
    for (a, b), pts in walked.items():
        ends[a].append(pts[0])
        ends[b].append(pts[-1])
    pins = {k: [int(round(np.mean([p[0] for p in v]))), int(round(np.mean([p[1] for p in v])))] for k, v in ends.items()}
    paths = []
    for (a, b), pts in walked.items():
        line = simplify(pts, 1.2)
        via = [pins[a]] + [[int(round(x)), int(round(y))] for x, y in line[1:-1]] + [pins[b]]
        paths.append({"a": a, "b": b, "picture": f"path-{a}-{b}.png", "via": via})
    # the names
    back_rgb = rgb_of(os.path.join(OUT, "back.png"))
    lum = back_rgb @ np.array([0.3, 0.55, 0.15], np.float32)
    ink = (lum < 0.62) & sheet
    for w in WAYS:
        ink |= ways[w]
    xx = np.arange(K.W)
    top = np.interp(xx, [p[0] for p in K.RIVER_TOP], [p[1] for p in K.RIVER_TOP]) - 3
    bot = np.interp(xx, [p[0] for p in K.RIVER_BOTTOM], [p[1] for p in K.RIVER_BOTTOM]) + 3
    yy = np.arange(K.H)[:, None]
    river_band = (yy >= top[None, :]) & (yy <= bot[None, :])
    inside = raster([K.LEFT, K.APEX, K.RIGHT])
    wayall = np.zeros(K.SHAPE, bool)
    for w in WAYS:
        wayall |= ways[w]
    names = place_names(drawn, wayall, ink, sheet, pins, river_band, inside)
    ground = territories(drawn)
    places = []
    for k in PLACES:
        places.append({"id": k, "picture": f"place-{k}.png", "shape": shape_of(drawn[k], ground[k], sheet), "pin": pins[k],
                       "label": names[k]["label"], "label_max": names[k]["label_max"]})
    layout = {
        "map": "egypt",
        "size": [K.W, K.H],
        "sheet": box,
        "material": "a sheet of papyrus drawn with a reed pen: black ink for the places, red ochre for the ways and marks",
        "label": LABEL,
        "places": places,
        "paths": paths,
        "note": ("Painted by tools/paint/map_egypt.py (MAP-15E), every number measured from the pictures by map_egypt_layout.py. "
                 "The Horizon (the pyramid) is drawn in back.png as its outline only, seen from the river; the gallery and the chamber are drawn inside it, "
                 "so they show only once visited (faint once a neighbour is). Pins are where each place's ways end on the paint: "
                 "the river's beside the wagon, the site's in front of the works, the gallery's at its foot inside the entrance, the chamber's at its doorway."),
    }
    return layout


def main(routes=None):
    if routes is None:
        import map_egypt_things as T
        routes = {key: f()[1] for key, f in T.WAYS.items()}
    layout = measure(routes)
    with open(os.path.join(OUT, "layout.json"), "w") as f:
        f.write(tidy(layout))
    print("  layout.json written")
    return layout


if __name__ == "__main__":
    main()

"""The map of the Office: layout.json, measured from the finished pictures (OFFICE-17B).

    python3 map_office_layout.py [folder]     measures out/map-office/ (or the folder) and rewrites its layout.json

Nothing here is typed in pixels but the zones each thing is looked for in (map_office_things.py's plan). Every number is
measured from the pictures in the folder (their alpha: what each file draws):
  shape   each place's outline: its zone (a room below the duct's strip; the duct's strip and the unit; the core; the
          lot), grown to take in every piece its picture draws there (the bell outside Property's window, the trash can
          by the downspout, the stamp's corners), kept clear of the other places' shapes, traced, at most 24 points;
  pin     where the portraits stand, a row of two (76 x 44): searched for in the place's own zone as the row that
          covers the least of the place's drawing, near the zone's middle, clear of every other place's drawing and the
          way (the duct's and the B-7 shaft's in the margin over the building, next to what they name);
  label   the middle of the name's baseline: searched for near the pin as the box that covers the least lines, clear of
          every pin row, every other name, every other place's drawing and the way; label_max is the name's own width
          in Koine Road at the label's size and spacing and a few pixels more;
  via     the way's own line (map_office_things.WAY_LINES), every point moved onto the nearest line of its picture, from
          the lot's pin to the duct's.
The names are the ones the map entry (js/content/maps.js, ENGINE-17's) is expected to give; a longer name is drawn
narrower by the engine to fit its box."""

import json
import math
import os
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import map_office_kit as K
import map_office_things as T
from letter import KOINE

FOLDER = "out/map-office"
PLACES = [("lot", "The lot"), ("ducts", "The ducts"), ("room", "The Comfortable Room"), ("property", "Property & Effects"),
          ("breakroom", "The break room"), ("b7", "B-7")]
WAYS = [("lot", "ducts")]
LABEL = {"size": 13, "spacing": 0.03, "upper": True}
ROW = (76, 44)                                    # two discs of 36 with 4 between; 22 above and below the pin
SHEET = list(T.SHEET_BOX)


def hexof(c):
    return "#" + "".join(f"{int(round(float(v) * 255)):02x}" for v in c)


def name_width(text, size=LABEL["size"], spacing=LABEL["spacing"]):
    f = ImageFont.truetype(KOINE, size)
    t = text.upper() if LABEL["upper"] else text
    return f.getlength(t) + spacing * size * (len(t) - 1)


def alpha(path):
    return np.asarray(Image.open(path).convert("RGBA"))[..., 3] >= 128


def rect_mask(x0, y0, x1, y1, shape=(600, 800)):
    m = np.zeros(shape, bool)
    m[int(round(y0)):int(round(y1)), int(round(x0)):int(round(x1))] = True
    return m


def poly_mask(poly, shape=(600, 800)):
    im = Image.new("L", (shape[1], shape[0]), 0)
    ImageDraw.Draw(im).polygon([tuple(p) for p in poly], fill=255)
    return np.asarray(im) >= 128


def dilate(m, r):
    out = m.copy()
    r = int(r)
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            if dx * dx + dy * dy <= r * r and (dx or dy):
                out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def trace(m):
    """The outer boundary of the largest blob in a mask, as an ordered list of pixel corners (clockwise)."""
    h, w = m.shape
    pad = np.zeros((h + 2, w + 2), bool)
    pad[1:-1, 1:-1] = m
    ys, xs = np.nonzero(pad)
    start = (xs[np.argmin(ys * 10000 + xs)], ys.min())
    x, y = start
    d = 0
    pts = [(x, y)]
    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def filled(px, py):
        return 0 <= py < h + 2 and 0 <= px < w + 2 and pad[py, px]

    for _ in range(400000):
        dx, dy = moves[d]
        if d == 0:
            a, b = (x, y - 1), (x, y)
        elif d == 1:
            a, b = (x, y), (x - 1, y)
        elif d == 2:
            a, b = (x - 1, y), (x - 1, y - 1)
        else:
            a, b = (x - 1, y - 1), (x, y - 1)
        fa, fb = filled(*a), filled(*b)
        if fb and not fa:
            x, y = x + dx, y + dy
        elif fa:
            d = (d - 1) % 4
            continue
        else:
            d = (d + 1) % 4
            continue
        pts.append((x, y))
        if (x, y) == start and len(pts) > 2:
            break
    return [(px - 1, py - 1) for px, py in pts]


def simplify(pts, eps):
    def dp(seg):
        if len(seg) < 3:
            return seg
        a, b = np.asarray(seg[0], float), np.asarray(seg[-1], float)
        ab = b - a
        L = np.hypot(*ab) or 1.0
        d = [abs((p[0] - a[0]) * ab[1] - (p[1] - a[1]) * ab[0]) / L for p in seg[1:-1]]
        i = int(np.argmax(d)) + 1
        if d[i - 1] > eps:
            return dp(seg[:i + 1])[:-1] + dp(seg[i:])
        return [seg[0], seg[-1]]
    far = int(np.argmax([math.hypot(p[0] - pts[0][0], p[1] - pts[0][1]) for p in pts]))
    return dp(pts[:far + 1])[:-1] + dp(pts[far:] + [pts[0]])[:-1]


def shape_of(mask, limit=24):
    pts = trace(mask)
    eps = 0.8
    while True:
        s = simplify(pts, eps)
        if len(s) <= limit:
            return [[int(round(x)), int(round(y))] for x, y in s]
        eps *= 1.25


class Sums:
    def __init__(self, a):
        self.s = np.pad(np.asarray(a, np.float64), ((1, 0), (1, 0))).cumsum(0).cumsum(1)

    def box(self, x0, y0, x1, y1):
        x0, y0 = max(int(math.floor(x0)), 0), max(int(math.floor(y0)), 0)
        x1, y1 = min(int(math.ceil(x1)), self.s.shape[1] - 1), min(int(math.ceil(y1)), self.s.shape[0] - 1)
        if x1 <= x0 or y1 <= y0:
            return 0.0
        return self.s[y1, x1] - self.s[y0, x1] - self.s[y1, x0] + self.s[y0, x0]


def pin_box(p):
    return (p[0] - ROW[0] / 2, p[1] - ROW[1] / 2, p[0] + ROW[0] / 2, p[1] + ROW[1] / 2)


def label_box(p, width):
    return (p[0] - width / 2, p[1] - 20, p[0] + width / 2, p[1] + 5)


def overlaps(a, b, gap=0.0):
    return not (a[2] + gap <= b[0] or b[2] + gap <= a[0] or a[3] + gap <= b[1] or b[3] + gap <= a[1])


def inside(box, sums, need=1.0):
    x0, y0, x1, y1 = box
    return sums.box(x0, y0, x1, y1) >= (x1 - x0) * (y1 - y0) * need - 0.5


def zones():
    """Where each place is: (its zone, where its pin may stand, where its name may go), as masks."""
    R = T.ROOMS
    band_bottom = T.DUCT_Y[1] + 2.0                                    # the rooms' things stand clear of the duct's strip
    z = {}
    for pid in ("room", "property", "breakroom"):
        x0, y0, x1, y1 = R[pid]
        zone = rect_mask(x0, band_bottom, x1, y1)
        if pid == "room":
            ux0, uy0, ux1, uy1 = T.UNIT
            zone &= ~rect_mask(ux0 - 3, 0, 800, uy1 + 3)                  # the unit overhead is the duct's
        hall = rect_mask(x0 - 4, R["hall"][1] + 2, x1 + 4, R["hall"][1] + 34)          # (a name may sit in the corridor just below)
        z[pid] = (zone, zone & ~dilate(~zone, 4), zone | hall)
    duct = rect_mask(T.DUCT_X[0] - 2, T.INNER[1], T.UNIT[2] + 3, band_bottom) | rect_mask(T.UNIT[0] - 3, T.INNER[1], T.UNIT[2] + 3, T.UNIT[3] + 3)
    north = rect_mask(T.BORDER[0] + 6, T.BORDER[1] + 6, T.OUT[2], T.OUT[1] - 2)
    z["ducts"] = (duct, north & rect_mask(300, 0, T.OUT[2], 600), north & rect_mask(220, 0, T.OUT[2], 600))
    core = rect_mask(T.OUT[0], T.OUT[1], T.ROOMS["shaft"][2] + T.PART, T.ROOMS["elevator"][3] + T.PART)
    z["b7"] = (core, north & rect_mask(0, 0, 160, 600), north & rect_mask(0, 0, 300, 600))
    lx0, ly0, lx1, ly1 = T.LOT
    lot = rect_mask(lx0, ly0, lx1, ly1 + 2)
    z["lot"] = (lot, lot & ~dilate(~lot, 3), lot)
    return z


def measure(folder=FOLDER):
    back = alpha(os.path.join(folder, "back.png"))
    draw = {pid: alpha(os.path.join(folder, f"place-{pid}.png")) for pid, _ in PLACES}
    ways = {(a, b): alpha(os.path.join(folder, f"path-{a}-{b}.png")) for a, b in WAYS}
    bk = np.asarray(Image.open(os.path.join(folder, "back.png")).convert("RGB"), dtype=np.float32) / 255
    lum = bk @ np.array([0.3, 0.55, 0.15], np.float32)
    paper = float(np.median(lum[back]))
    lines_back = (lum > paper + 0.18) & back                           # the back's own white lines
    sheet_in = Sums(back)
    way_any = np.zeros_like(back)
    for m in ways.values():
        way_any |= m
    way_sums = Sums(dilate(way_any, 3))
    Z = zones()
    # the shapes first: each zone grown to take in its own drawing, kept clear of the shapes made before it
    shapes, shape_masks = {}, {}
    for pid, _ in PLACES:
        zone = Z[pid][0]
        own = draw[pid]
        m = dilate(zone & back, 1) | (dilate(own, 3) & back)
        for q, qm in shape_masks.items():
            m &= ~dilate(qm, 2)
        # keep only what joins the zone (pieces of the drawing outside it are boxed back to it)
        shapes[pid] = shape_of(m)
        shape_masks[pid] = poly_mask(shapes[pid])
    out_places, taken_pins, taken_labels = [], [], []
    for pid, name in PLACES:
        zone, pzone, lzone = Z[pid]
        own = draw[pid]
        others = np.zeros_like(back)
        for q in draw:
            if q != pid:
                others |= draw[q]
        oth_sums = Sums(dilate(others, 2))
        own_sums = Sums(own)
        lb_sums = Sums(lines_back)
        pz = Sums(pzone)
        ys, xs = np.nonzero(pzone)
        cx, cy = xs.mean(), ys.mean()
        pins = []
        for py in range(int(ys.min()) + 22, int(ys.max()) - 21, 2):
            for px in range(int(xs.min()) + 38, int(xs.max()) - 37, 2):
                box = pin_box((px, py))
                if not inside(box, pz) or not inside(box, sheet_in):
                    continue
                if oth_sums.box(*box) > 0 or way_sums.box(*box) > 0:
                    continue
                if any(overlaps(box, pin_box(q), 8.0) for q in taken_pins) or any(overlaps(box, lb) for lb in taken_labels):
                    continue
                cost = own_sums.box(*box) * 1.0 + lb_sums.box(*box) * 0.25 + 0.03 * math.hypot(px - cx, py - cy)
                pins.append((cost, (px, py)))
        if not pins:
            raise SystemExit(f"{pid}: no room for its row of portraits")
        pins.sort()
        width = name_width(name)
        lmax = int(math.ceil(width)) + 8
        lz = Sums(lzone)
        labels = []
        ys, xs = np.nonzero(lzone)
        for ly in range(int(ys.min()) + 20, int(ys.max()) - 4, 1):
            for lx in range(int(xs.min()) + lmax // 2, int(xs.max()) - lmax // 2 + 1, 2):
                box = label_box((lx, ly), lmax)
                if not inside(box, lz, 0.97) or not inside(box, sheet_in):
                    continue
                if oth_sums.box(*box) > 0 or way_sums.box(*box) > 0:
                    continue
                if any(overlaps(box, pin_box(q), 2.0) for q in taken_pins) or any(overlaps(box, lb, 2.0) for lb in taken_labels):
                    continue
                tb = (lx - width / 2, ly - 11, lx + width / 2, ly + 2)              # the letters themselves
                labels.append((own_sums.box(*tb) * 3.0 + lb_sums.box(*tb) * 1.2, (lx, ly)))
        if not labels:
            raise SystemExit(f"{pid}: no room for its name")
        labels.sort()
        best = None
        for pc, pin_ in pins[:500]:
            for lc, lab_ in labels[:2500]:
                if best is not None and pc + lc >= best[0]:
                    break
                if overlaps(label_box(lab_, lmax), pin_box(pin_), 3.0):
                    continue
                c = pc + lc + 0.05 * math.hypot(lab_[0] - pin_[0], lab_[1] - pin_[1])
                if best is None or c < best[0]:
                    best = (c, pin_, lab_)
        if best is None:
            raise SystemExit(f"{pid}: no room for its people and its name together")
        _, pin, lab = best
        taken_pins.append(pin)
        taken_labels.append(label_box(lab, lmax))
        out_places.append({"id": pid, "picture": f"place-{pid}.png", "shape": shapes[pid], "pin": [int(pin[0]), int(pin[1])],
                           "label": [int(lab[0]), int(lab[1])], "label_max": lmax})
    pins = {p["id"]: p["pin"] for p in out_places}
    T.WAY_LINES.clear()
    for (a, b), fn in T.WAYS.items():
        fn(K.Pen((600, 800), seed=0))
    paths = []
    for a, b in WAYS:
        m = ways[(a, b)]
        ys, xs = np.nonzero(m)
        via = [pins[a]]
        for (x, y) in T.WAY_LINES[(a, b)]:
            d = (xs - x) ** 2 + (ys - y) ** 2
            i = int(np.argmin(d))
            via.append([int(xs[i]), int(ys[i])])
        via.append(pins[b])
        dedup = [via[0]]
        for p in via[1:]:
            if p != dedup[-1]:
                dedup.append(p)
        paths.append({"a": a, "b": b, "picture": f"path-{a}-{b}.png", "via": dedup})
    lay = {
        "map": "office",
        "size": [800, 600],
        "sheet": SHEET,
        "material": ("A blueprint: the ground floor of the Office of Peculiar Sectors' desert field headquarters, sheet 1 of 8, "
                     "white lines on the print's blue, folded in four, a corner dog-eared."),
        "label": {"color": hexof(K.LABEL), "halo": hexof(K.HALO), "upper": LABEL["upper"], "spacing": LABEL["spacing"], "size": LABEL["size"]},
        "places": out_places,
        "paths": paths,
        "note": ("The ground floor in plan, north up, the lot at the bottom (map_office_things.py). The duct runs along the north "
                 "rooms' back wall, dotted (overhead), from the roof's unit at the north-east to the B-7 shaft at the north-west, its "
                 "four grilles small crossed squares: over Interview Room C, Property & Effects, the break room, and the hall where it "
                 "turns up to the elevator; so the rooms' shapes stop short of the duct's strip. The duct's and the shaft's portraits "
                 "stand in the margin over the building, next to what they name. B-7 has no way to it: drawn whenever the map entry "
                 "says it is (it is stamped RESTRICTED). The one way, lot to ducts, is the route up the downspout to the roof and in at "
                 "the unit's intake; its via runs along its dashes between the two pins (the first and last steps go from a pin to the "
                 "way's end)."),
    }
    return lay


def dumps(lay):
    s = json.dumps(lay, indent=2)
    s = re.sub(r"\[\s+(-?\d+),\s+(-?\d+)\s+\]", r"[\1, \2]", s)
    s = re.sub(r"\[\s+((?:\[-?\d+, -?\d+\],?\s*)+)\]", lambda m: "[" + re.sub(r"\s+", " ", m.group(1)).strip() + "]", s)
    s = re.sub(r"\[\s+(-?\d+),\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+\]", r"[\1, \2, \3, \4]", s)
    return s + "\n"


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else FOLDER
    lay = measure(folder)
    with open(os.path.join(folder, "layout.json"), "w") as f:
        f.write(dumps(lay))
    for p in lay["places"]:
        print(p["id"], "pin", p["pin"], "label", p["label"], "label_max", p["label_max"], "shape", len(p["shape"]), "points")

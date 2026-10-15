"""The map of the house: layout.json, measured from the finished pictures (MAP-15H).

    python3 map_home_layout.py [folder]     measures out/map-home/ (or the folder) and rewrites its layout.json

Nothing here is typed in pixels. Every number is measured from the pictures in the folder (their alpha: what each file
draws), with the house's measurements (map_home_house.py, through the plans of map_home_things.py) saying which room
is which:
  shape   the outline of the place's room together with everything its picture draws (a door's swing, a doormat
          outside), traced round and simplified to at most 24 points, a few pixels clear of the drawing;
  pin     where the three portraits stand: searched for over the room's floor, as the place where a row of three
          (116 x 44) covers the least of the room's drawing, a little toward the room's middle; for the landing,
          which is a narrow gallery, in the open over its railing, clear of the ladder's dotted line;
  label   the middle of the name's baseline: searched for in the room, as the place where the name covers the least
          pencil, next to the row of portraits and clear of it; label_max is the name's own width in Koine Road at
          the map's label size and spacing, and a few pixels more;
  via     each way's own line (the line it is drawn along: map_home_things.WAY_LINES), every point moved onto the
          nearest pencil of the way's picture, from the one place's pin to the other's.
The places are placed in turn, each keeping clear of the pins, names, ways and other places already there."""

import json
import math
import os
import sys

import re

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import map_home_house as H
import map_home_kit as K
import map_home_things as T
from letter import KOINE

FOLDER = "out/map-home"
PLACES = [("living", "The living room"), ("landing", "The landing"), ("study", "Dad's study"),
          ("lilsis", "Little Sister's room"), ("bigsis", "The Retreat")]
WAYS = [("living", "landing"), ("landing", "study"), ("landing", "lilsis"), ("landing", "bigsis")]
LABEL = {"size": 14, "spacing": 0.02, "upper": False}
ROW = (116, 44)                                   # three discs of 36 with 4 between; 22 above and below the pin
SHEET = [40, 136, 760, 564]


def label_colour():
    c = K.PAPER + (K.LEAD_DARK - K.PAPER) * 0.84
    return "#" + "".join(f"{int(round(v * 255)):02x}" for v in c)


def halo_colour():
    return "#" + "".join(f"{int(round(v * 255)):02x}" for v in K.PAPER)


def name_width(text, size=LABEL["size"], spacing=LABEL["spacing"]):
    f = ImageFont.truetype(KOINE, size)
    t = text.upper() if LABEL["upper"] else text
    return f.getlength(t) + spacing * size * (len(t) - 1)


def alpha(path):
    return np.asarray(Image.open(path).convert("RGBA"))[..., 3] >= 128


# ---------------------------------------------------------------- the rooms, in the picture
def room_polys():
    U = H.U_ROOMS
    return {"living": T.GF.rect(*H.G_ROOMS["living"]),
            "landing": T.UP.rect(*U["landing"]),
            "study": T.UP.pts(H.U_STUDY),
            "lilsis": T.UP.rect(*U["lilsis"]),
            "bigsis": T.AT.rect(*H.A_ROOM)}


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


# ---------------------------------------------------------------- tracing a mask's outline
def trace(m):
    """The outer boundary of the largest blob in a mask, as an ordered list of (x, y) pixel corners (a square walk)."""
    h, w = m.shape
    pad = np.zeros((h + 2, w + 2), bool)
    pad[1:-1, 1:-1] = m
    ys, xs = np.nonzero(pad)
    start = (xs[np.argmin(ys * 10000 + xs)], ys.min())          # the top-left-most pixel
    # walk the pixel edges with the blob on the right (clockwise): corners are (x, y) of the pixel grid
    x, y = start
    d = 0                                                        # 0 right, 1 down, 2 left, 3 up
    pts = [(x, y)]
    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def filled(px, py):
        return 0 <= py < h + 2 and 0 <= px < w + 2 and pad[py, px]

    for _ in range(200000):
        # the pixels ahead-left and ahead-right of the corner, in the direction d
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
    """Douglas-Peucker, on a closed outline."""
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
    out = dp(pts[:far + 1])[:-1] + dp(pts[far:] + [pts[0]])[:-1]
    return out


def shape_of(mask, limit=24):
    pts = trace(mask)
    eps = 0.8
    while True:
        s = simplify(pts, eps)
        if len(s) <= limit:
            return [[int(round(x)), int(round(y))] for x, y in s]
        eps *= 1.25


# ---------------------------------------------------------------- the search
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


def inside(box, m_sums, area_needed=1.0):
    x0, y0, x1, y1 = box
    return m_sums.box(x0, y0, x1, y1) >= (x1 - x0) * (y1 - y0) * area_needed - 0.5


def darkness_of(path, paper_lum):
    """How dark each painted pixel of a picture is against the paper (0 where it draws nothing)."""
    a = np.asarray(Image.open(path).convert("RGBA"), dtype=np.float32) / 255
    lum = a[..., :3] @ np.array([0.3, 0.55, 0.15], np.float32)
    return np.clip((paper_lum - lum) / paper_lum, 0, 1) * (a[..., 3] >= 0.5)


def blobs(m):
    """The bounding boxes (x0, y0, x1, y1) of a mask's separate pieces (4-connected)."""
    seen = np.zeros_like(m)
    out = []
    for y0, x0 in zip(*np.nonzero(m)):
        if seen[y0, x0]:
            continue
        stack, box = [(y0, x0)], [x0, y0, x0, y0]
        seen[y0, x0] = True
        while stack:
            y, x = stack.pop()
            box = [min(box[0], x), min(box[1], y), max(box[2], x), max(box[3], y)]
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < m.shape[0] and 0 <= xx < m.shape[1] and m[yy, xx] and not seen[yy, xx]:
                    seen[yy, xx] = True
                    stack.append((yy, xx))
        out.append(box)
    return out


def measure(folder=FOLDER):
    back = alpha(os.path.join(folder, "back.png"))
    draw = {pid: alpha(os.path.join(folder, f"place-{pid}.png")) for pid, _ in PLACES}
    paper_lum = float(np.median((np.asarray(Image.open(os.path.join(folder, "back.png")).convert("RGB"), dtype=np.float32) / 255
                                 @ np.array([0.3, 0.55, 0.15], np.float32))[back]))
    dark = {pid: darkness_of(os.path.join(folder, f"place-{pid}.png"), paper_lum) for pid, _ in PLACES}
    ways = {(a, b): alpha(os.path.join(folder, f"path-{a}-{b}.png")) for a, b in WAYS}
    # the back's pencil (its dark pixels): where a name should not sit if it can help it
    bk = np.asarray(Image.open(os.path.join(folder, "back.png")).convert("RGB"), dtype=np.float32) / 255
    lum = bk @ np.array([0.3, 0.55, 0.15], np.float32)
    pencil_back = (lum < 0.62) & back
    # the titles' boxes (painted on the back): no pin or name over them
    titles = []
    for key, (words, at, anchor) in T.TITLES.items():
        lead = K.Lead((600, 800), seed=99)
        m = lead.text(words, at, T.TITLE_SIZE, "firm", anchor=anchor, rough=0.0, seed=1)
        ys, xs = np.nonzero(m > 0.2)
        titles.append((xs.min() - 3, ys.min() - 3, xs.max() + 3, at[1] + 7))
    rooms = room_polys()
    sheet_in = Sums(back)
    out_places, taken_pins, taken_labels, shapes_done = [], [], [], []
    others_drawn = np.zeros_like(back)
    for pid, _ in PLACES:
        others_drawn |= draw[pid]
    way_any = np.zeros_like(back)
    for m in ways.values():
        way_any |= m
    way_sums = Sums(dilate(way_any, 3))
    for pid, name in PLACES:
        own = draw[pid]
        room = poly_mask(rooms[pid])
        others = others_drawn & ~own
        oth_sums = Sums(dilate(others, 2))
        own_sums = Sums(dark[pid])
        pb_sums = Sums(pencil_back)
        # where the row of portraits may stand: on the room's floor (the landing: in the open over its railing)
        if pid == "landing":
            x0, y0, x1, y1 = T.UP(780.0, 175.0) + T.UP(0.0, 175.0)
            zone = np.zeros_like(back)
            zone[int(T.AT.box()[3] + H.WALL_OUT * T.SCALE) + 4:int(T.UP.oy) - 2, int(x0) - 60:int(x1) + 40] = True
            zone &= ~dilate(pencil_back, 2)
        else:
            zone = room & ~dilate(~room, 3)
        zone_sums = Sums(zone)
        cx, cy = np.mean([p[0] for p in rooms[pid]]), np.mean([p[1] for p in rooms[pid]])
        # the row of portraits and the name are chosen together: each candidate row costs the pencil it covers (dark
        # pencil more than light: a rug before a chair), each name the pencil under its letters, three times over,
        # and the back's pencil (walls) under them; the pair that costs least, the two clear of each other, wins
        pins = []
        ys, xs = np.nonzero(zone)
        for py in range(int(ys.min()) + 22, int(ys.max()) - 21, 2):
            for px in range(int(xs.min()) + 58, int(xs.max()) - 57, 2):
                box = pin_box((px, py))
                if not inside(box, zone_sums) or not inside(box, sheet_in):
                    continue
                if oth_sums.box(*box) > 0 or way_sums.box(*box) > 0:
                    continue
                if any(overlaps(box, pin_box(q), 8.0) for q in taken_pins):
                    continue
                if any(overlaps(box, t) for t in titles) or any(overlaps(box, lb) for lb in taken_labels):
                    continue
                pins.append((own_sums.box(*box) + 0.02 * math.hypot(px - cx, py - cy), (px, py)))
        if not pins:
            raise SystemExit(f"{pid}: no room for its row of portraits")
        pins.sort()
        width = name_width(name)
        lmax = int(math.ceil(width)) + 8
        lzone = room | (dilate(room, 6) & ~others) if pid != "landing" else (room | zone)
        lz_sums = Sums(lzone)
        labels = []
        ys, xs = np.nonzero(lzone)
        for ly in range(int(ys.min()) + 20, int(ys.max()) - 4, 1):
            for lx in range(int(xs.min()) + lmax // 2, int(xs.max()) - lmax // 2 + 1, 2):
                box = label_box((lx, ly), lmax)
                if not inside(box, lz_sums, 0.96) or not inside(box, sheet_in):
                    continue
                if oth_sums.box(*box) > 0 or way_sums.box(*box) > 0:
                    continue
                if any(overlaps(box, pin_box(q), 2.0) for q in taken_pins):
                    continue
                if any(overlaps(box, t, 2.0) for t in titles) or any(overlaps(box, lb, 2.0) for lb in taken_labels):
                    continue
                tb = label_box((lx, ly), width)
                tb = (tb[0], ly - 12, tb[2], ly + 3)                     # the letters themselves
                labels.append((own_sums.box(*tb) * 3.0 + pb_sums.box(*tb) * 0.8, (lx, ly)))
        if not labels:
            raise SystemExit(f"{pid}: no room for its name")
        labels.sort()
        best = None
        for pc, pin_ in pins[:400]:
            for lc, lab_ in labels[:1500]:
                if best is not None and pc + lc >= best[0]:
                    break
                if overlaps(label_box(lab_, lmax), pin_box(pin_), 3.0):
                    continue
                c = pc + lc + 0.02 * math.hypot(lab_[0] - pin_[0], lab_[1] - pin_[1])
                if best is None or c < best[0]:
                    best = (c, pin_, lab_)
        if best is None:
            raise SystemExit(f"{pid}: no room for its people and its name together")
        _, pin, lab = best
        taken_pins.append(pin)
        taken_labels.append(label_box(lab, lmax))
        # its shape: the room's outline, with a box round each piece its picture draws outside it (a door's swing, a
        # doormat), kept clear of the other places' rooms and of the shapes already made; traced and simplified
        m = dilate(room, 2)
        ry, rx = np.nonzero(room)
        rx0, ry0, rx1, ry1 = rx.min(), ry.min(), rx.max(), ry.max()
        for (bx0, by0, bx1, by1) in blobs(own & ~m):
            # a piece outside the room (the doormat beyond the front door): its box, reaching back to the room
            bx0, bx1 = min(bx0, rx1) if bx0 > rx1 else bx0, max(bx1, rx0) if bx1 < rx0 else bx1
            by0, by1 = min(by0, ry1) if by0 > ry1 else by0, max(by1, ry0) if by1 < ry0 else by1
            m[max(by0 - 2, 0):by1 + 3, max(bx0 - 2, 0):bx1 + 3] = True
        for qid in rooms:
            if qid != pid:
                m &= ~dilate(poly_mask(rooms[qid]), 3)
        for prev in shapes_done:
            m &= ~dilate(prev, 3)
        shp = shape_of(m)
        shapes_done.append(poly_mask(shp))
        out_places.append({"id": pid, "picture": f"place-{pid}.png", "shape": shp, "pin": [int(pin[0]), int(pin[1])],
                           "label": [int(lab[0]), int(lab[1])], "label_max": lmax})
    pins = {p["id"]: p["pin"] for p in out_places}
    # the ways: each one's own line, every point moved onto its pencil, from pin to pin
    T.WAY_LINES.clear()
    for (a, b), fn in T.WAYS.items():
        fn(K.Lead((600, 800), seed=0))
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
        "map": "home",
        "size": [800, 600],
        "sheet": SHEET,
        "material": "A sheet of squared paper, folded into a pocket, with the house drawn on it in pencil by Dad: three plans, ground floor, upstairs, the attic.",
        "label": {"color": label_colour(), "halo": halo_colour(), "upper": LABEL["upper"], "spacing": LABEL["spacing"], "size": LABEL["size"]},
        "places": out_places,
        "paths": paths,
        "note": ("The house is drawn turned half round, as a plan usually is (the street at the bottom): the ground floor left, "
                 "upstairs right, the attic over it (drawn as one comes up its ladder). Every room is its model "
                 "(tools/paint/home_*_model.py) at one scale; map_home_house.py says how they fit together. Each via runs "
                 "along its way's own pencil between the two pins; the first and last steps go from a pin to the way's end."),
    }
    return lay


def dumps(lay):
    """layout.json with short lists kept on one line."""
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

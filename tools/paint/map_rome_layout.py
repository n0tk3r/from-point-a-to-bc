"""The map of Rome (MAP-15R): layout.json, measured from the finished pictures in out/map-rome/.

Nothing in it is typed: the sheet is the board's own box in back.png; each place's shape is the outline of its
drawing (the convex hull of its painted pixels, simplified to at most 24 points and grown 4 pixels); its pin is the
point of its open ground (map_rome_places.STANDS) farthest from anything scratched, or for the steps the foot of the
temple (the shape takes in the ground the portraits stand on, so that the walk leaves a place from inside it); its name's anchor sits beside its drawing on the side map_rome_places.NAMES gives, its width measured in the
game's face; each way's line runs from a's pin along the middle of its scratches (map_rome_places.WAYS_LINE, each point
moved onto the middle of what was scratched near it) to b's pin.

  python3 map_rome_layout.py        writes out/map-rome/layout.json from the pictures there"""

import json
import math
import os

import numpy as np
from PIL import Image, ImageFont

import map_rome_places as PL
from letter import KOINE
from map_rome_kit import LABEL, OUT, H, W

# the engine's names for the places (MAP-15.md's table): the engine writes them; the layout only measures them
NAMES = {"street": "The street", "steps": "Saturn's steps", "treasury": "The treasury", "forum": "The Forum",
         "capitol": "The Capitol", "tiber": "Across the Tiber"}
ORDER = ["street", "steps", "treasury", "forum", "capitol", "tiber"]
WAY_ORDER = [("steps", "street"), ("steps", "treasury"), ("steps", "forum"), ("steps", "capitol"), ("forum", "tiber")]
PIN_ROW = (76, 44)          # two portraits: discs 36 across with 4 between, and the box 22 above and below the pin
LABEL_UP, LABEL_DOWN = 20, 5


def alpha(name, folder=OUT):
    im = Image.open(os.path.join(folder, name)).convert("RGBA")
    return np.asarray(im, dtype=np.uint8)[..., 3] > 0


def name_width(text, style=LABEL):
    """The name's width in the game's face at the label's size and spacing (capitals if the label says so)."""
    t = text.upper() if style["upper"] else text
    f = ImageFont.truetype(KOINE, style["size"])
    return f.getlength(t) + style["spacing"] * style["size"] * len(t)


def hull(points):
    """Convex hull (monotone chain), counter-clockwise, of (x, y) points."""
    pts = sorted(set(map(tuple, points)))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def simplify(poly, eps):
    """Douglas-Peucker on a closed polygon."""
    def dp(pts):
        if len(pts) < 3:
            return pts
        a, b = np.asarray(pts[0], float), np.asarray(pts[-1], float)
        ab = b - a
        L = np.hypot(*ab) + 1e-9
        d = [abs(ab[0] * (p[1] - a[1]) - ab[1] * (p[0] - a[0])) / L for p in pts[1:-1]]
        i = int(np.argmax(d)) + 1
        if d[i - 1] > eps:
            return dp(pts[:i + 1])[:-1] + dp(pts[i:])
        return [pts[0], pts[-1]]
    far = max(range(len(poly)), key=lambda i: (poly[i][0] - poly[0][0]) ** 2 + (poly[i][1] - poly[0][1]) ** 2)
    first = dp(poly[:far + 1])
    second = dp(poly[far:] + [poly[0]])
    return first[:-1] + second[:-1]


def grow(poly, g):
    """A convex polygon (counter-clockwise in picture coordinates, y down) moved outward by g pixels."""
    n = len(poly)
    P = np.asarray(poly, float)
    area = sum(P[i, 0] * P[(i + 1) % n, 1] - P[(i + 1) % n, 0] * P[i, 1] for i in range(n))
    sgn = 1.0 if area > 0 else -1.0
    lines = []
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        d = b - a
        nrm = np.array([d[1], -d[0]]) * sgn
        nrm /= np.hypot(*nrm) + 1e-9
        lines.append((a + nrm * g, d))
    out = []
    for i in range(n):
        (p1, d1), (p2, d2) = lines[i - 1], lines[i]
        den = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(den) < 1e-9:
            out.append(tuple(p2))
            continue
        t = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / den
        out.append(tuple(p1 + d1 * t))
    return out


def outline(mask, g=4.0, most=24, extra=()):
    """The shape round a drawing: its pixels' hull (with any `extra` points: the corners of the ground its portraits
    stand on), simplified to at most `most` points, grown g pixels."""
    ys, xs = np.where(mask)
    corners = np.concatenate([np.stack([xs + dx, ys + dy], 1) for dx in (0, 1) for dy in (0, 1)])
    if len(extra):
        corners = np.concatenate([corners, np.asarray(extra, dtype=float)])
    h = hull(corners.tolist())
    eps = 0.8
    s = simplify(h, eps)
    while len(s) > most:
        eps *= 1.25
        s = simplify(h, eps)
    return [[round(x, 1), round(y, 1)] for x, y in grow(s, g + eps)]


def bbox(mask):
    ys, xs = np.where(mask)
    return float(xs.min()), float(ys.min()), float(xs.max() + 1), float(ys.max() + 1)


def open_point(box, painted):
    """The point of a box farthest from any painted pixel (nearest the box's middle when it is a tie)."""
    x0, y0, x1, y1 = box
    ys, xs = np.where(painted[max(0, y0 - 60):y1 + 60, max(0, x0 - 60):x1 + 60])
    xs, ys = xs + max(0, x0 - 60), ys + max(0, y0 - 60)
    gx, gy = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
    gx, gy = gx.ravel().astype(float), gy.ravel().astype(float)
    best = np.full(gx.shape, 1e9)
    for k in range(0, len(xs), 4000):
        d = (gx[:, None] - xs[None, k:k + 4000]) ** 2 + (gy[:, None] - ys[None, k:k + 4000]) ** 2
        best = np.minimum(best, d.min(axis=1))
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    score = np.sqrt(best) - 0.02 * np.hypot(gx - mx, gy - my)
    i = int(np.argmax(score))
    return [int(gx[i]), int(gy[i])]


def snap(points, mask, r=7.0):
    """Each point moved onto the middle of what is scratched within r pixels of it."""
    ys, xs = np.where(mask)
    out = []
    for x, y in points:
        d = np.hypot(xs - x, ys - y)
        near = d <= r
        if near.sum() >= 3:
            out.append([round(float(xs[near].mean()), 1), round(float(ys[near].mean()), 1)])
        else:
            out.append([round(float(x), 1), round(float(y), 1)])
    return out


def measure(folder=OUT):
    back = alpha("back.png", folder)
    sx0, sy0, sx1, sy1 = bbox(back)
    places = {p: alpha(f"place-{p}.png", folder) for p in ORDER}
    ways = {w: alpha(f"path-{w[0]}-{w[1]}.png", folder) for w in WAY_ORDER}
    painted = np.zeros((H, W), bool)
    for m in list(places.values()) + list(ways.values()):
        painted |= m
    out_places = []
    pins = {}
    for p in ORDER:
        m = places[p]
        x0, y0, x1, y1 = bbox(m)
        stand = PL.STANDS[p]
        if stand[0] == "below":
            pin = [int(round((x0 + x1) / 2)), int(round(y1 + stand[1]))]
        else:
            pin = open_point(stand, painted)
        pins[p] = pin
        side, gap, ref = PL.NAMES[p][:3]
        along = PL.NAMES[p][3] if len(PL.NAMES[p]) > 3 else 0.5
        width = name_width(NAMES[p])
        label_max = int(math.ceil((width + 6) / 2.0) * 2)
        rx0, ry0, rx1, ry1 = x0, y0, x1, y1
        px0, py0 = pin[0] - PIN_ROW[0] / 2, pin[1] - PIN_ROW[1] / 2
        px1, py1 = pin[0] + PIN_ROW[0] / 2, pin[1] + PIN_ROW[1] / 2
        if ref == "pin":
            rx0, ry0, rx1, ry1 = px0, py0, px1, py1
        elif ref == "both":
            rx0, ry0, rx1, ry1 = min(x0, px0), min(y0, py0), max(x1, px1), max(y1, py1)
        cx, cy = rx0 + (rx1 - rx0) * along, ry0 + (ry1 - ry0) * along
        if side == "below":
            label = [cx, ry1 + gap + LABEL_UP]
        elif side == "above":
            label = [cx, ry0 - gap - LABEL_DOWN]
        elif side == "left":
            label = [rx0 - gap - label_max / 2, cy + (LABEL_UP - LABEL_DOWN) / 2]
        else:
            label = [rx1 + gap + label_max / 2, cy + (LABEL_UP - LABEL_DOWN) / 2]
        stand_corners = [(px0 + 4, py0 + 4), (px1 - 4, py0 + 4), (px1 - 4, py1 - 4), (px0 + 4, py1 - 4)]
        out_places.append({"id": p, "picture": f"place-{p}.png", "shape": outline(m, extra=stand_corners), "pin": pin,
                           "label": [int(round(label[0])), int(round(label[1]))], "label_max": label_max})
    out_paths = []
    for a, b in WAY_ORDER:
        line = snap(PL.WAYS_LINE[(a, b)], ways[(a, b)])
        via = [pins[a]] + line + [pins[b]]
        out_paths.append({"a": a, "b": b, "picture": f"path-{a}-{b}.png", "via": via})
    return {
        "map": "rome",
        "size": [W, H],
        "sheet": [int(sx0), int(sy0), int(sx1), int(sy1)],
        "material": "a Roman writing tablet: a frame of plain wood round dark beeswax, the plan scratched in with a stylus",
        "label": dict(LABEL),
        "places": out_places,
        "paths": out_paths,
        "note": ("Painted by tools/paint/map_rome.py (MAP-15R); every number here is measured from the pictures by "
                 "map_rome_layout.py. Scratches are pale on dark wax, so a place at 0.28 reads as a faint old line "
                 "and is gone at 0. The names are pale scratch-colour capitals with a halo of the wax's own dark. "
                 "Laid out as the act's ways run: the street left of Saturn's steps, the treasury behind them (above), "
                 "the Forum below, the Capitol to the right on its hill, across the Tiber beyond the Forum's left end, "
                 "over the stone bridge."),
    }


def write(path=f"{OUT}/layout.json"):
    data = measure(os.path.dirname(path))
    with open(path, "w") as f:
        json.dump(data, f, indent=1)
        f.write("\n")
    return data


if __name__ == "__main__":
    d = write()
    for p in d["places"]:
        print(p["id"], "pin", p["pin"], "label", p["label"], "max", p["label_max"], "shape", len(p["shape"]))

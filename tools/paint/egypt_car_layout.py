"""layout.json for egypt-car: the numbers the game needs, MEASURED from the finished picture.

Every thing's shape is traced round the pixels that really show it (from what each ray of the picture met, pushed by the
same hand-wobble as the paint), as a polygon; the windshield's glass is traced exactly (OpenCV's contours, a pixel being
inside when its middle is), so that the steam kept inside it never runs over a pillar, the dash, the mirror or the wheel.
The fixed numbers (the walk patch, the mark, the words' box, the bottom band) are the master brief's (egypt_car_model).

The scene lays the areas in the master brief's order, a later one over an earlier one where they touch: windshield,
visor, rearview, freshener, door, manual, seat, glovebox, cupholder, wheel, radio, gauges, horn, gears, key. Each shape
here is the whole of what is seen of its thing, cut off at the top of the bottom band (row 548) but for the door, the
manual and the key's ring, which hang into it."""

import json
import math

import cv2
import numpy as np

from room import View
import egypt_car_model as M

OUT = "out/egypt-car"
W, H = 800, 600
V = View(**M.VIEW)
ORDER = ["windshield", "visor", "rearview", "freshener", "door", "manual", "seat", "glovebox", "cupholder", "wheel", "radio", "gauges", "horn", "gears", "key"]
INTO_BAND = ("door", "manual", "key")


def outline(mask, eps=1.0, most=None):
    """The outline of a mask (its biggest piece) as a polygon of whole pixels, within `eps` pixels of its edge."""
    m = mask.astype(np.uint8)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not cs:
        return []
    c = max(cs, key=cv2.contourArea)
    p = cv2.approxPolyDP(c, eps, True)[:, 0, :]
    pts = [[int(x), int(y)] for x, y in p]
    if most and len(pts) > most:
        return outline(mask, eps * 1.4, most)
    return pts


def edge_poly(mask, eps=0.7):
    """A polygon whose inside (a pixel is in when its middle is) is the mask as nearly as can be: the contour of the mask
    blown up four times, so that the polygon runs along the pixels' edges and not through their middles. Simplified
    as far as it can be with no pixel outside the mask inside it: the tolerance is narrowed until none is (below a
    third of a pixel the polygon can no longer cross a pixel's middle)."""
    k = 4
    big = cv2.resize(mask.astype(np.uint8), (W * k, H * k), interpolation=cv2.INTER_NEAREST)
    cs, _ = cv2.findContours(big, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)
    for e in (eps, 0.5, 0.35, 0.25, 0.15):
        p = cv2.approxPolyDP(c, e * k, True)[:, 0, :].astype(float)
        poly = [[round((x + 0.5) / k, 2), round((y + 0.5) / k, 2)] for x, y in p]
        if not (inside_poly(poly) & ~mask).any():
            break
    return poly


def inside_poly(poly, shape=(H, W)):
    """A pixel is inside when its middle is (as the engine decides): the even-odd rule, crossing by crossing."""
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]].astype(np.float64)
    px, py = xx + 0.5, yy + 0.5
    inside = np.zeros(shape, dtype=bool)
    pts = [(float(a), float(b)) for a, b in poly]
    for i in range(len(pts)):
        (x1, y1), (x2, y2) = pts[i], pts[i - 1]
        if y1 == y2:
            continue
        cond = (y1 > py) != (y2 > py)
        xc = (x2 - x1) * (py - y1) / (y2 - y1) + x1
        inside ^= cond & (px < xc)
    return inside


def hull(mask):
    """The convex outline of all a thing's pieces together (a key and its ring and fob; a lever and its knob)."""
    ys, xs = np.nonzero(mask)
    pts = np.stack([xs, ys], axis=1).astype(np.int32)
    h = cv2.convexHull(pts)[:, 0, :]
    return [[int(x), int(y)] for x, y in h]


def joined(mask, r=6):
    """A thing seen in pieces close together (the glovebox open: its compartment, and its door dropped below the dash's
    lip) joined into one, so that one outline goes round it all."""
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, k) > 0


def from_left(mask):
    """A thing at the picture's left edge seen in pieces (Dad's door: its open window above the dash's end, its panel,
    the armrest's end and the pocket below it) as one: in every row, everything from x 0 to its farthest pixel; across
    the rows where something nearer hides it (the dash's end), as wide as the narrower of the rows above and below."""
    h = mask.shape[0]
    reach = np.array([(np.nonzero(mask[y])[0].max() if mask[y].any() else -1) for y in range(h)])
    rows = np.nonzero(reach >= 0)[0]
    out = np.zeros_like(mask, dtype=bool)
    if not len(rows):
        return out
    for y in range(rows.min(), rows.max() + 1):
        if reach[y] < 0:
            above, below = reach[:y][reach[:y] >= 0], reach[y + 1:][reach[y + 1:] >= 0]
            reach[y] = min(above[-1], below[0])
        out[y, :reach[y] + 1] = True
    return out


def above_band(m):
    out = m.copy()
    out[M.BAND_TOP:] = False
    return out


def wheel_outline():
    """The wheel's rim, its outer edge all round, cut off at the top of the bottom band."""
    pts = [V.pt(*M.wheel_pt(a, M.WHEEL["r"] + M.WHEEL["tube"])) for a in np.linspace(0, 360, 73)[:-1]]
    m = inside_poly(pts)
    return outline(above_band(m), 1.0)


def write(masks, extra):
    """masks: {thing id: boolean mask at picture size}, the first state; extra: the other states' masks (visor down,
    glovebox open), the glass, the cut-out masks, the fx numbers."""
    def shape(tid, m, eps=1.0):
        if tid not in INTO_BAND:
            m = above_band(m)
        if tid in ("key", "gears", "cupholder", "horn", "freshener", "rearview", "radio"):
            return {"poly": hull(m)}
        if tid == "door":
            m = from_left(m)
        return {"poly": outline(m, eps)}

    whats = {
        "windshield": "the windshield, full of the sand the nose ploughed up: a strip of river and sky at its top, the back half of the red hood at its foot",
        "visor": "the driver's sun visor (a cut-out): up, flat against the headliner; down (shape 'down'), hanging over the windshield's top left, "
                 "its strap holding Little Sister's drawing and the registration card",
        "rearview": "the rearview mirror, on its stem from the top of the glass: in it, the sky through the rear window (the tail is up)",
        "freshener": "the air freshener (a cut-out): a little cardboard station wagon, red, on its string from the mirror's stem",
        "door": "Dad's door, at the left: the window rolled down (sand and papyrus outside, a bright sliver of glass at the sill), the lock knob, "
                "the end of the armrest, the window crank, the pocket at its foot",
        "manual": "the owner's manual, standing in the door's pocket, its spine worn at the middle",
        "seat": "the Son's half of the bench: his seat belt lying unbuckled across it, six candy wrappers, one sock",
        "glovebox": "the glovebox (a cut-out): a big rounded door, a push-button latch at its top middle with the keyhole; open (shape 'open'), "
                    "the door dropped on its bottom hinge and the compartment: the road map on a drift of ketchup packets, then the packets alone",
        "cupholder": "the Son's slushie in its clip-on holder on the right-hand vent: a tall blue paper cup, a dome lid, a striped straw",
        "wheel": "the steering wheel: a big thin dark rim, three spokes, the column under it (the gauges, the horn, the gear lever and the key lie over it)",
        "radio": "the radio: a cassette deck with a tape half out of its slot, two knobs, a tuning window",
        "gauges": "the gauges under their hood: the speedometer (needle at 0, the odometer at 200006), fuel at a quarter and the temperature "
                  "hard in the red (its red lamp lit), the strip P R N D L between them, the pointer at P",
        "horn": "the horn pad, plain (no emblem)",
        "gears": "the gear lever: a long stalk from the column's right side, a black knob at its end",
        "key": "the car's key alone in the ignition, on a small plain ring with a plain leather fob",
    }
    things = []
    for tid in ORDER:
        t = {"id": tid, "what": whats[tid]}
        if tid == "wheel":
            t["shape"] = {"poly": wheel_outline()}
        else:
            t["shape"] = shape(tid, masks[tid])
        if tid == "visor":
            t["down"] = shape(tid, extra["visor-down"])
        if tid == "glovebox":                                              # open: the compartment and the dropped door below it, one shape
            t["open"] = {"poly": outline(joined(above_band(extra["glovebox-open"]), 6), 1.0)}
        if tid in ("visor", "glovebox", "freshener"):
            t["plane"] = tid
        things.append(t)
    doc = {
        "id": M.ID,
        "horizon": M.VIEW["horizon"], "full": M.VIEW["full"],
        "view": dict(M.VIEW, cam=list(M.VIEW["cam"])),
        "eye_cm": round(V.eye, 1),
        "vanishing": [int(round(V.cx)), int(round(V.hz))],
        "light": "afternoon: the sun low, ahead of the car and a little to its right, above the windshield's top right corner and out of the "
                 "picture (its glare in the glass's top right corner, its glitter on the river under it); the dash top bleached in it, a shaft "
                 "over the passenger side of the dash onto the Son's cushion; everything that faces Dad in warm half shade; the headliner "
                 "glowing warm; the footwells the darkest",
        "walk": M.WALK,
        "blocked": [],
        "planes": [
            {"id": "glovebox", "file": "glovebox-shut.png", "states": {"shut": "glovebox-shut.png", "map": "glovebox-map.png", "empty": "glovebox-empty.png"}, "base": 600},
            {"id": "visor", "file": "visor-up.png", "states": {"up": "visor-up.png", "down": "visor-down.png"}, "base": 600},
            {"id": "freshener", "file": "freshener.png", "plane": "front"},
        ],
        "things": things,
        "marks": {"default": list(M.MARK)},
        "fx": extra["fx"],
        "glass": extra["glass"],
        "words": {"box": [200, 70, 600, 150], "color": "#ffd34d",
                  "note": "Dad's words (bold yellow, dark outline, centred on x 400, bottom edge on row 150, up to 400 px wide and three lines): "
                          "the box is the sky away from the sun (deep blue), the far bank's dark line and the river below it; the sun's glare and "
                          "the glitter on the river are right of x 600. The rearview mirror and the air freshener hang in it (mid and dark tones); "
                          "the visor, pulled down, covers its left end (x 200 to 300): egypt_car_check.py lays a long line over it, both ways"},
        "exits": [],
        "notes": extra["notes"],
    }
    one = lambda v: json.dumps(v, separators=(", ", ": "))
    rows = []
    for key, value in doc.items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            rows.append(f' "{key}": [\n' + ",\n".join("  " + one(v) for v in value) + "\n ]")
        else:
            rows.append(f' "{key}": {one(value)}')
    with open(f"{OUT}/layout.json", "w") as f:
        f.write("{\n" + ",\n".join(rows) + "\n}\n")
    return json.load(open(f"{OUT}/layout.json"))

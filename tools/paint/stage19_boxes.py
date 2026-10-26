"""STAGE-19O (round nineteen): the Office's small clickable things made big enough to hit (the scene audit's S9: "at
least about a head wide (15-25 px)"). Every Office layout script calls grow() on its things just before it writes
layout.json, so a painter's re-run gives the same areas the scene files hold. Nothing painted moves: only the clickable
box round a thing grows, about its own middle (or by the side named), to at least the size given here, in stage pixels.
"""

# room: {thing: (min width, min height, how)}; how: "mid" grows about the middle; "right" keeps the left edge (the keypad:
# the door is on its left); "left" keeps the right edge (the pie: its card stands on its right and is listed after it)
GROW = {
    "office-lot": {"nut-1": (18, 18, "mid"), "nut-2": (18, 18, "mid"), "nut-3": (18, 18, "mid"), "nut-4": (18, 18, "mid"),
                   "keypad": (18, 18, "right")},
    "office-breakroom": {"pie": (30, 20, "left"), "card": (20, 20, "mid"), "menu": (15, 19, "mid")},
    "office-room": {"cones": (18, 57, "mid")},
    "office-property": {"bell": (24, 18, "mid")},
    "office-ducts": {"pencil": (23, 18, "mid"), "wrapper": (23, 18, "mid"), "rivets": (18, 108, "mid"), "valve": (18, 18, "mid")},
}


def _box(shape):
    if "rect" in shape:
        x, y, w, h = shape["rect"]
        return x, y, x + w, y + h
    pts = shape["poly"]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def _r(v):
    v = round(float(v), 1)
    return int(v) if v == int(v) else v


def grown(shape, minw, minh, how="mid"):
    x0, y0, x1, y1 = _box(shape)
    w, h = x1 - x0, y1 - y0
    if w < minw:
        if how == "right":
            x1 = x0 + minw
        elif how == "left":
            x0 = x1 - minw
        else:
            x0, x1 = x0 - (minw - w) / 2.0, x1 + (minw - w) / 2.0
    if h < minh:
        y0, y1 = y0 - (minh - h) / 2.0, y1 + (minh - h) / 2.0
    x0, y0, x1, y1 = (_r(v) for v in (x0, y0, x1, y1))
    if "rect" in shape:
        return {**shape, "rect": [x0, y0, _r(x1 - x0), _r(y1 - y0)]}
    return {**shape, "poly": [[x0, y1], [x1, y1], [x1, y0], [x0, y0]]}


def grow(things, room):
    """things: the layout's list of things (each with a `shape`); grown in place. Returns the list."""
    want = GROW.get(room, {})
    for t in things:
        if t.get("id") in want and isinstance(t.get("shape"), dict) and not t.get("stage19"):
            minw, minh, how = want[t["id"]]
            t["shape"] = grown(t["shape"], minw, minh, how)
            t["stage19"] = "STAGE-19O: the clickable box grown to at least %dx%d px (S9); the painting is unchanged" % (minw, minh)
    return things

"""Small made things for egypt_site.py, each drawn on a clear Sheet at a picture place and size, lit from
the left: timber, rope, pots, baskets, bread, tools, and people far enough off to be dabs."""

import math

import numpy as np

from brush import *

WOOD = ("#46301f", "#80603c", "#c9a26a")              # dark, body, sunlit edge
ROPE = ("#7d6238", "#c9aa72", "#f2deac")
POT = ("#6a3424", "#b4623c", "#dc9060", "#f8c898")    # dark, body, light, shine
MARL = ("#8c7458", "#d2b88c", "#eedcb4", "#fff4d8")   # pale desert-clay ware
COPPER = ("#7c3c20", "#cf7438", "#f6aa66", "#ffe2b8")
LINEN = ("#9a90b0", "#d9cfb6", "#f6ecd2", "#fffaea")
REED = ("#6c5a30", "#a48c4c", "#cdb670", "#eeda98")
BREAD = ("#8a5a2c", "#c8924c", "#e8bc74")


def _mix(a, b, t):
    a = rgb(a) if isinstance(a, str) else np.asarray(a, dtype=F32)
    b = rgb(b) if isinstance(b, str) else np.asarray(b, dtype=F32)
    return lerp(a, b, t)


def log(sheet, a, b, width, tones=WOOD, light=(-0.6, -0.8), knots=0, seed=0):
    """A pole or beam from a to b: dark, then its body, then a line of light along the side toward the sun."""
    sheet.line([a, b], tones[0], width)
    ox, oy = light[0] * width * 0.22, light[1] * width * 0.22
    sheet.line([(a[0] + ox, a[1] + oy), (b[0] + ox, b[1] + oy)], tones[1], max(0.8, width * 0.58), 1.0, round_ends=False)
    if width >= 1.6:
        ox, oy = light[0] * width * 0.36, light[1] * width * 0.36
        sheet.line([(a[0] + ox, a[1] + oy), (b[0] + ox, b[1] + oy)], tones[2], max(0.7, width * 0.2), 0.85, round_ends=False)
    if knots:
        rng = np.random.default_rng(seed)
        for _ in range(knots):
            t = rng.random()
            px, py = lerp(a[0], b[0], t), lerp(a[1], b[1], t)
            sheet.line([(px - width * 0.3, py), (px + width * 0.3, py)], tones[0], max(0.7, width * 0.18), 0.6)
    return sheet


def lash(sheet, x, y, r, seed=0, color=ROPE[2]):
    """Rope bound round a joint: a few short turns, light on dark."""
    rng = np.random.default_rng(seed + int(x * 7 + y * 13))
    sheet.ellipse(x, y, r * 0.9, r * 0.9, ROPE[0], 0.8)
    for i in range(3):
        a = rng.uniform(-0.5, 0.5) + (0.9 if i % 2 else -0.9)
        dx, dy = math.cos(a) * r, math.sin(a) * r
        sheet.line([(x - dx, y - dy + (i - 1) * r * 0.45), (x + dx, y + dy + (i - 1) * r * 0.45)], color if i != 1 else ROPE[1], max(0.7, r * 0.34), 0.95)
    return sheet


def rope(sheet, points, width=1.6, tones=ROPE, twist=3.2, alpha=1.0):
    """A rope lying along a path: a dark under-edge, the rope, and the light catching each turn of the lay."""
    pts = [(float(a), float(b)) for a, b in points]
    sheet.line([(a + 0.3, b + width * 0.45) for a, b in pts], tones[0], width, 0.75 * alpha)
    sheet.line(pts, tones[1], width, alpha)
    run = 0.0
    for (a0, b0), (a1, b1) in zip(pts[:-1], pts[1:]):
        seg = math.hypot(a1 - a0, b1 - b0)
        n = max(1, int((run + seg) / twist) - int(run / twist))
        for i in range(n):
            t = (i + 0.5) / n
            px, py = lerp(a0, a1, t), lerp(b0, b1, t)
            sheet.line([(px - width * 0.3, py - width * 0.3), (px + width * 0.25, py + width * 0.1)], tones[2], max(0.6, width * 0.42), 0.8 * alpha)
        run += seg
    return sheet


def coil(sheet, x, y, rx, ry, turns=4, width=1.6, tones=ROPE):
    """A coil of rope lying on the ground, and its loose end."""
    sheet.ellipse(x + rx * 0.12, y + ry * 0.25, rx * 1.08, ry * 1.1, "#6e5688", 0.35)
    for i in range(turns):
        k = 1 - i * 0.72 / turns
        ring = [(x + math.cos(a) * rx * k, y - i * width * 0.55 + math.sin(a) * ry * k) for a in np.linspace(0, math.pi * 2, 26)]
        rope(sheet, ring, width, tones, twist=2.6)
    sheet.ellipse(x, y - turns * width * 0.5, rx * 0.2, ry * 0.2, tones[0], 0.9)
    return sheet


def _body(x, y, h, prof, wide=1.0):
    left = [(x - hw * h * wide, y - t * h) for t, hw in prof]
    right = [(x + hw * h * wide, y - t * h) for t, hw in reversed(prof)]
    return left + right


PROFILES = {
    "beer": [(0.0, 0.07), (0.08, 0.14), (0.3, 0.24), (0.55, 0.28), (0.74, 0.24), (0.84, 0.15), (0.90, 0.12), (1.0, 0.15)],
    "water": [(0.0, 0.14), (0.12, 0.30), (0.42, 0.41), (0.68, 0.37), (0.84, 0.22), (0.92, 0.17), (1.0, 0.22)],
    "store": [(0.0, 0.15), (0.15, 0.23), (0.75, 0.25), (0.9, 0.2), (1.0, 0.22)],
    "bowl": [(0.0, 0.3), (0.3, 0.62), (1.0, 0.85)],
}


def jar(sheet, x, y, h, kind="beer", tones=POT, stopper=None, shadow=True, band=None):
    """A pot standing with the middle of its foot at (x, y), `h` tall."""
    prof = PROFILES[kind]
    if shadow:
        wide = max(hw for _, hw in prof) * h
        sheet.ellipse(x + wide * 1.1, y - h * 0.02, wide * 1.5, max(1.2, h * 0.07), "#5e4a7c", 0.42)
    sheet.poly(_body(x, y, h, prof), tones[1])
    lit = [(x - hw * h * 0.92, y - t * h) for t, hw in prof] + [(x - hw * h * 0.30, y - t * h) for t, hw in reversed(prof)]
    sheet.poly(lit, tones[2], 0.9)
    dark = [(x + hw * h * 0.38, y - t * h) for t, hw in prof] + [(x + hw * h, y - t * h) for t, hw in reversed(prof)]
    sheet.poly(dark, tones[0], 0.8)
    shine = [(x - hw * h * 0.62, y - t * h) for t, hw in prof[2:-2]]
    if len(shine) >= 2:
        sheet.line(shine, tones[3], max(0.8, h * 0.035), 0.9)
    if band:
        t0 = 0.6
        hw = np.interp(t0, [t for t, _ in prof], [w for _, w in prof]) * h
        sheet.line([(x - hw, y - t0 * h), (x + hw, y - t0 * h)], band, max(0.8, h * 0.04), 0.9)
    top = prof[-1][1] * h
    sheet.ellipse(x, y - h, top, max(0.9, top * 0.36), tones[0])
    sheet.ellipse(x, y - h - 0.3, top * 0.82, max(0.7, top * 0.26), "#2a1c20" if stopper is None else stopper)
    if stopper is not None:                                   # a cone of mud over the mouth, as beer was sealed
        sheet.poly([(x - top * 0.9, y - h), (x, y - h - top * 1.5), (x + top * 0.9, y - h)], stopper)
        sheet.poly([(x - top * 0.9, y - h), (x, y - h - top * 1.5), (x - top * 0.2, y - h)], _mix(stopper, "#ffffff", 0.35))
    return sheet


def rolls(sheet, x, y, h, n=4, seed=0):
    """A store jar with rolled papyrus standing in it."""
    rng = np.random.default_rng(seed)
    top = y - h
    for i in range(n):
        px = x + (i - (n - 1) / 2) * h * 0.11 + rng.normal(0, h * 0.01)
        lean = rng.normal(0, 0.12)
        tall = h * rng.uniform(0.34, 0.6)
        a, b = (px, top + h * 0.06), (px + lean * tall, top - tall)
        sheet.line([a, b], "#b89a62", max(1.6, h * 0.09))
        sheet.line([(a[0] - h * 0.014, a[1]), (b[0] - h * 0.014, b[1])], "#f6e8c0", max(1.0, h * 0.05))
        sheet.ellipse(b[0], b[1], max(0.9, h * 0.045), max(0.7, h * 0.03), "#fff6dc")
    jar(sheet, x, y, h, "store", MARL)
    return sheet


def basket(sheet, x, y, w, h, tones=REED, loaves=0, seed=0, shadow=True):
    """A woven basket with the middle of its foot at (x, y); `loaves` heaps bread in it."""
    rng = np.random.default_rng(seed)
    if shadow:
        sheet.ellipse(x + w * 0.7, y - h * 0.03, w * 0.75, max(1.2, h * 0.14), "#5e4a7c", 0.42)
    a, b = w * 0.36, w * 0.5
    for i in range(loaves):                                   # round loaves and tall conical ones
        px = x + rng.uniform(-b * 0.7, b * 0.7)
        py = y - h - rng.uniform(0, h * 0.25)
        if i % 3 == 2:
            sheet.poly([(px - w * 0.11, py + h * 0.1), (px, py - h * 0.5), (px + w * 0.11, py + h * 0.1)], BREAD[1])
            sheet.poly([(px - w * 0.11, py + h * 0.1), (px, py - h * 0.5), (px - w * 0.02, py + h * 0.1)], BREAD[2])
        else:
            sheet.ellipse(px, py, w * 0.2, h * 0.17, BREAD[0])
            sheet.ellipse(px - w * 0.03, py - h * 0.04, w * 0.16, h * 0.11, BREAD[1])
            sheet.ellipse(px - w * 0.06, py - h * 0.07, w * 0.08, h * 0.05, BREAD[2])
    sheet.poly([(x - a, y), (x + a, y), (x + b, y - h), (x - b, y - h)], tones[1])
    sheet.poly([(x - a, y), (x - a * 0.2, y), (x - b * 0.2, y - h), (x - b, y - h)], tones[2])
    sheet.poly([(x + a * 0.5, y), (x + a, y), (x + b, y - h), (x + b * 0.5, y - h)], tones[0], 0.8)
    rows = max(3, int(h / 2.6))
    for i in range(1, rows):
        t = i / rows
        hw = lerp(a, b, t)
        sheet.line([(x - hw, y - h * t), (x + hw, y - h * t)], tones[0], 0.7, 0.55)
    sheet.line([(x - b, y - h), (x + b, y - h)], tones[3], max(1.0, h * 0.09))
    return sheet


def loaf(sheet, x, y, r, seed=0):
    sheet.ellipse(x + r * 0.5, y + r * 0.1, r * 1.1, r * 0.4, "#5e4a7c", 0.35)
    sheet.ellipse(x, y - r * 0.45, r, r * 0.55, BREAD[0])
    sheet.ellipse(x - r * 0.12, y - r * 0.55, r * 0.8, r * 0.38, BREAD[1])
    sheet.ellipse(x - r * 0.3, y - r * 0.66, r * 0.4, r * 0.16, BREAD[2])
    return sheet


def sherds(sheet, x, y, w, h, seed=0, count=16):
    """A heap of broken pot used for jotting on: pale and red flakes, a few with ink strokes."""
    rng = np.random.default_rng(seed)
    sheet.ellipse(x + w * 0.35, y, w * 0.75, max(1.2, h * 0.2), "#5e4a7c", 0.4)
    for i in range(count):
        t = i / count
        px = x + rng.normal(0, w * 0.26) * (1 - t * 0.6)
        py = y - t * h * 0.9 - rng.random() * h * 0.1
        r = w * rng.uniform(0.12, 0.2)
        a = rng.uniform(0, math.pi)
        pts = [(px + math.cos(a + k * 2.1 + rng.normal(0, 0.3)) * r, py + math.sin(a + k * 2.1) * r * 0.5) for k in range(3)] + [(px + rng.normal(0, r * 0.3), py + r * 0.5)]
        tone = (MARL[2], POT[2], MARL[1], POT[1])[int(rng.integers(4))]
        sheet.poly(pts, tone)
        sheet.line([pts[0], pts[1]], "#fff6dc", 0.7, 0.6)
        if rng.random() < 0.4:
            for k in range(3):
                sheet.line([(px - r * 0.4 + k * r * 0.35, py - r * 0.2), (px - r * 0.3 + k * r * 0.35, py + r * 0.15)], "#2a2024", 0.7, 0.85)
    return sheet


def dab(sheet, x, y, h, kilt="#fff8ea", skin="#6b3f2a", lean=0.0, load=None):
    """A person far off: brown, with a white kilt. `h` is his height in pixels."""
    wd = max(1.0, h * 0.26)
    sheet.line([(x + lean * h, y - h), (x + lean * h * 0.4, y - h * 0.48)], skin, wd)
    sheet.line([(x + lean * h * 0.4, y - h * 0.5), (x, y - h * 0.12)], kilt, wd * 1.1)
    sheet.line([(x, y - h * 0.14), (x, y)], skin, max(0.8, wd * 0.7))
    if h > 7:
        sheet.ellipse(x + lean * h, y - h, wd * 0.5, wd * 0.5, "#2a1a16")
    if load:
        sheet.ellipse(x + lean * h, y - h * 1.12, wd * 1.1, wd * 0.8, load)
    return sheet


def mallet(sheet, a, b, k, tones=WOOD):
    """A mason's wooden mallet lying from a (the end of its handle) to b (its head): a club with a bell-shaped head."""
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L = math.hypot(dx, dy) + 1e-6
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    sheet.line([(ax + 1.2, ay + 1.4), (bx + 1.2, by + 1.4)], "#5e4a7c", k * 2.2, 0.4)
    log(sheet, a, (ax + dx * 0.55, ay + dy * 0.55), k * 1.5, tones)
    hx, hy = ax + dx * 0.5, ay + dy * 0.5
    head = [(hx + px * k * 1.6, hy + py * k * 1.6), (bx + px * k * 3.0, by + py * k * 3.0), (bx + ux * k * 1.2, by + uy * k * 1.2), (bx - px * k * 3.0, by - py * k * 3.0), (hx - px * k * 1.6, hy - py * k * 1.6)]
    sheet.poly(head, tones[1])
    sheet.poly([head[0], head[1], (bx + ux * k * 0.6 + px * k * 0.8, by + uy * k * 0.6 + py * k * 0.8), (hx + px * k * 0.4, hy + py * k * 0.4)], tones[0], 0.7)
    sheet.poly([head[4], head[3], (bx + ux * k * 0.8 - px * k * 1.4, by + uy * k * 0.8 - py * k * 1.4), (hx - px * k * 0.8, hy - py * k * 0.8)], tones[2], 0.9)
    return sheet


def chisel(sheet, a, b, k, tones=COPPER):
    """A copper chisel lying from a (its struck end) to b (its edge)."""
    sheet.line([(a[0] + 1.0, a[1] + 1.2), (b[0] + 1.0, b[1] + 1.2)], "#5e4a7c", k * 1.3, 0.45)
    sheet.line([a, b], tones[0], k * 1.3)
    sheet.line([(a[0] - k * 0.2, a[1] - k * 0.25), (b[0] - k * 0.2, b[1] - k * 0.25)], tones[1], k * 0.95, 1.0, round_ends=False)
    m = (lerp(a[0], b[0], 0.2), lerp(a[1], b[1], 0.2))
    n = (lerp(a[0], b[0], 0.85), lerp(a[1], b[1], 0.85))
    sheet.line([(m[0] - k * 0.3, m[1] - k * 0.4), (n[0] - k * 0.3, n[1] - k * 0.4)], tones[3], max(0.7, k * 0.32), 0.95, round_ends=False)
    sheet.ellipse(a[0], a[1], k * 0.9, k * 0.7, tones[2])          # the head, burred over by the mallet
    return sheet


"""What stands in the burial chamber: the king's furniture, the goldsmith's bench, the lamps.
Every piece is invented in the plain manner of the Old Kingdom (straight lines, lion's feet, papyrus
buds, gold sheet over wood); none is copied from a museum object.

Things are drawn in the room's own centimetres with a Pen, which knows where the lamps are, so every
face takes its tone from the light that really falls on it.

GOLD is painted the way it looks, not the way it is named: dark warm brown where it mirrors the dark
room, burnt orange where the lamplit stone shows in it, and a few hard yellow-white lights where it
mirrors a flame. The hard lights go on a second sheet (`fine`) that is laid last, at full strength."""

import math

import numpy as np

from brush import *
from egypt_chamber_kit import *

GOLD = [(0.0, "#22120c"), (0.12, "#3e210e"), (0.28, "#693a10"), (0.46, "#955718"), (0.63, "#bd7a1e"), (0.80, "#dca02c"), (1.0, "#f2c446"), (1.4, "#ffe070")]
HOT, WHITE = "#ffd95e", "#fff8cf"
WOODS = {"bench": "#a08a6c", "plank": "#84705a", "cedar": "#7c4632", "ebony": "#3a2a2c", "pale": "#b89468", "pole": "#6a4630"}
STUFF = {"linen": "#efe6d2", "alabaster": "#f1e2c2", "copper": "#d07a48", "pot": "#b0603e", "buff": "#c9a27a", "basket": "#b8904e",
         "reed": "#a89858", "rope": "#b89a66", "soot": "#3a2a26", "leather": "#8a5a3a", "faience": "#3fa7a0", "granite": "#8a6462", "dark": "#56423e"}

# where the big pieces stand: (X of the middle, D of the middle, turn in degrees)
PLACE = dict(chair=(-318.0, 150.0, 10.0), bed=(-208.0, 120.0, 17.0), arm=(-74.0, 128.0, 16.0), long=(-236.0, 30.0, 2.0), chest=(-40.0, 34.0, -4.0), chest2=(-18.0, 33.0, 8.0),
             poles=(-394.0, -354.0), mats=((-338.0, 22.0, 150.0, 9.5), (-320.0, 30.0, 128.0, 8.5)),
             jars=((-424.0, 50.0), (-403.0, 64.0), (-418.0, 82.0), (-1.0, 74.0)), basket=(-8.0, 150.0), basins=(-30.0, 170.0))
BENCH = dict(x0=-241.0, x1=-121.0, d0=292.0, d1=337.0, h=38.0)
BRAZIER = (-96.0, 322.0)


def _c(color):
    return rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)


def mix(a, b, t):
    return lerp(_c(a), _c(b), t)


class Pen:
    def __init__(self, lamps, amb, shape=SHAPE, tongues=False):
        self.base, self.fine = Paper(shape), Paper(shape)
        self.lamps, self.amb = lamps, np.asarray(amb, dtype=F32)
        self.rng = np.random.default_rng(5)
        self.tongues = tongues            # round four: lamp flames are drawn by the game; True paints them in still, as approved
        self.flames = []                  # (x, y, size) of every flame drawn or left to the game, in the order drawn

    # ------------------------------------------------ light
    def light(self, X, Y, D, n, wrap=0.25):
        total = np.zeros(3, dtype=F32)
        for l in self.lamps:
            e = float(lamplight(l, X, Y, D, n, wrap))
            total += e * flame_color(e)
        return total

    def e(self, X, Y, D, n, wrap=0.25):
        return float(self.light(X, Y, D, n, wrap) @ np.array([0.35, 0.5, 0.15]))

    def tone(self, albedo, at, n, gain=1.0, wrap=0.25):
        """A flat color for a face of this material at this place, facing along n."""
        lg = self.light(at[0], at[1], at[2], n, wrap) * gain
        return (1 - np.exp(-_c(albedo) * (self.amb + lg) * 1.35)).astype(F32)

    def gold(self, at, n, gain=1.0, lift=0.0):
        e = self.e(at[0], at[1], at[2], n, 0.4) * gain * 0.5 + lift
        return ramp(np.array([[max(e, 0.0)]], dtype=F32), GOLD)[0, 0]

    def toward(self, X, Y, D):
        """Which way, in the picture, the strongest light comes from at this place -> unit (dx, dy), strength."""
        best, bv = None, 0.0
        here = P(X, Y, D)
        for l in self.lamps:
            d2 = (l.X - X) ** 2 + (l.Y - Y) ** 2 + (l.D - D) ** 2
            v = l.power / (1.0 + (d2 / (l.reach * l.reach)) ** 1.5)
            if v > bv:
                bv, best = v, l
        lx, ly = best.at
        dx, dy = lx - here[0], ly - here[1]
        dy -= (best.D - D) * 0.15                                     # a lamp nearer us than the thing lights its front
        norm = math.hypot(dx, dy) + 1e-6
        return (dx / norm, dy / norm), bv

    # ------------------------------------------------ flat shapes
    def poly(self, pts, color, alpha=1.0, fine=False):
        (self.fine if fine else self.base).poly([P(*p) for p in pts], color, alpha)

    def line(self, pts, color, width=1.0, alpha=1.0, fine=False):
        (self.fine if fine else self.base).line([P(*p) for p in pts], color, width, alpha)

    def spark(self, at, size=1.0, color=WHITE, halo=HOT):
        """A hard point of light where metal mirrors a flame: a little four-pointed star."""
        x, y = P(*at) if len(at) == 3 else at
        r = 1.5 * size
        self.fine.poly([(x - r * 1.5, y), (x - r * 0.35, y - r * 0.35), (x, y - r * 1.5), (x + r * 0.35, y - r * 0.35), (x + r * 1.5, y), (x + r * 0.35, y + r * 0.35), (x, y + r * 1.5), (x - r * 0.35, y + r * 0.35)], halo, 0.92)
        self.fine.ellipse(x, y, 0.85 * size, 0.85 * size, color, 1.0)

    def dash(self, a, b, t0, t1, color=HOT, width=0.9, alpha=0.95):
        """A hard light along part of an edge from a to b (room cm)."""
        pa, pb = np.array(P(*a)), np.array(P(*b))
        self.fine.line([lerp(pa, pb, t0), lerp(pa, pb, t1)], color, width, alpha)

    # ------------------------------------------------ boxes
    def box(self, outline, y0, y1, paint, top=None, sides=(0, 1, 2, 3)):
        """A box on (or above) the floor. `outline` is its four corners on the floor: near-left, near-right,
        far-right, far-left. `paint(at, n)` gives the color of a face. Draws the sides we can see, then
        the top. -> {face name: its four corners in room cm}."""
        faces = {}
        names = ("near", "right", "far", "left")
        for i in sides:
            a, b = outline[i], outline[(i + 1) % 4]
            ex, ed = b[0] - a[0], b[1] - a[1]
            nx, nd = -ed, ex
            norm = math.hypot(nx, nd) + 1e-9
            nx, nd = nx / norm, nd / norm
            mx, md = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            if (0 - mx) * nx + (DCAM - md) * nd <= 0:
                continue
            quad = [(a[0], y0, a[1]), (b[0], y0, b[1]), (b[0], y1, b[1]), (a[0], y1, a[1])]
            self.poly(quad, paint((mx, (y0 + y1) / 2, md), (nx, 0, nd)))
            faces[names[i]] = quad
        if top is not False:
            quad = [(a, y1, d) for a, d in outline]
            cx, cd = sum(a for a, _ in outline) / 4, sum(d for _, d in outline) / 4
            self.poly(quad, (top or paint)((cx, y1, cd), (0, 1, 0)))
            faces["top"] = quad
        return faces

    def on(self, quad, u, v):
        """A place on a four-cornered face: u along its first edge (0..1), v up or back across it (0..1)."""
        a, b, c, d = [np.array(q, dtype=float) for q in quad]
        p = lerp(lerp(a, b, u), lerp(d, c, u), v)
        return (float(p[0]), float(p[1]), float(p[2]))

    def patch(self, quad, u0, u1, v0, v1, color, alpha=1.0, fine=False):
        self.poly([self.on(quad, u0, v0), self.on(quad, u1, v0), self.on(quad, u1, v1), self.on(quad, u0, v1)], color, alpha, fine)

    def stroke(self, quad, u0, v0, u1, v1, color, width=1.0, alpha=1.0, fine=False):
        self.line([self.on(quad, u0, v0), self.on(quad, u1, v1)], color, width, alpha, fine)

    # ------------------------------------------------ round things
    def rod(self, a, b, r, colors, lit=None, alpha=1.0):
        """A pole or leg from a to b (room cm), r cm thick: dark body, a lighter side, and the colors'
        last entry as a thin light along it. `colors` = (dark, middle, light)."""
        pa, pb = P(*a), P(*b)
        ka, kb = k_of(a[2]), k_of(b[2])
        wa, wb = max(1.0, 2 * r * ka), max(1.0, 2 * r * kb)
        dx, dy = pb[0] - pa[0], pb[1] - pa[1]
        norm = math.hypot(dx, dy) + 1e-6
        px, py = -dy / norm, dx / norm                                 # across the rod, in the picture
        if lit is None:
            lit, _ = self.toward((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2)
        side = 1.0 if px * lit[0] + py * lit[1] > 0 else -1.0
        s = self.base
        s.taper([pa, pb], colors[0], wa, wb, alpha)
        o = 0.16 * side
        s.taper([(pa[0] + px * wa * o, pa[1] + py * wa * o), (pb[0] + px * wb * o, pb[1] + py * wb * o)], colors[1], wa * 0.56, wb * 0.56, alpha)
        o = 0.25 * side
        if len(colors) > 2 and max(wa, wb) >= 2.2:
            s.taper([(pa[0] + px * wa * o, pa[1] + py * wa * o), (pb[0] + px * wb * o, pb[1] + py * wb * o)], colors[2], max(0.8, wa * 0.2), max(0.8, wb * 0.2), alpha)
        return (px * side, py * side), (wa, wb)

    def gold_rod(self, a, b, r, gain=1.0, hot=(), dash=True, tone=0.0):
        """A gilded pole: brown, burnt orange, and a broken hard light along the side the lamp is on."""
        mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2)
        lit, strength = self.toward(*mid)
        e = float(np.clip(strength * gain * 0.6 + tone, 0, 1))
        cols = (mix("#22120c", "#4a280e", e), mix("#4e2c0e", "#a3621a", e), mix("#8a5016", "#e2a630", e))
        side, (wa, wb) = self.rod(a, b, r, cols, lit)
        pa, pb = np.array(P(*a)), np.array(P(*b))
        off = np.array(side) * 0.26
        if dash and e > 0.3:
            t = 0.05 + 0.3 * self.rng.random()
            while t < 0.95:
                t1 = min(0.97, t + 0.05 + 0.14 * self.rng.random())
                w = lerp(wa, wb, (t + t1) / 2)
                self.fine.line([lerp(pa, pb, t) + off * w, lerp(pa, pb, t1) + off * w], HOT, max(0.8, w * 0.2), 0.5 + 0.45 * e)
                t = t1 + 0.12 + 0.4 * self.rng.random()
        for t in hot:
            w = lerp(wa, wb, t)
            q = lerp(pa, pb, t) + off * w
            self.spark((q[0], q[1]), max(0.7, w * 0.26))
        return side

    def lathe(self, X, D, profile, colors, y0=0.0, squash=None, lit=None, alpha=1.0, glaze=None):
        """A turned thing (a jar, a dish, a drum) standing at (X, D): `profile` is [(radius, height), ...]
        from the foot up, in cm. `colors` = (shade, body, light, highlight). The light side is the one
        the lamp is on. -> its place in the picture."""
        k = k_of(D)
        x0, yb = P(X, y0, D)
        if lit is None:
            lit, _ = self.toward(X, y0 + profile[-1][1] * 0.6, D)
        side = 1.0 if lit[0] >= 0 else -1.0
        sq = squash if squash is not None else (row_of(D) - G.vy) / G.F          # how round a level circle looks from here
        s = self.base

        def band(a, b, color, al=1.0, lo=0.0, hi=1.0):
            hs = [p for p in profile if lo <= p[1] / profile[-1][1] <= hi]
            if len(hs) < 2:
                return
            pts = [(x0 + r * k * a * side, yb - h * k) for r, h in hs] + [(x0 + r * k * b * side, yb - h * k) for r, h in reversed(hs)]
            s.poly(pts, color, al * alpha)
        r0 = profile[0][0]
        s.ellipse(x0, yb, r0 * k, max(0.6, r0 * k * sq), colors[0], alpha)                                               # the foot rounds toward us
        band(-1, 1, colors[1])
        band(-1, -0.45, colors[0])
        band(-1, -0.78, mix(colors[0], "#1c1016", 0.35), 0.8)
        band(0.15, 0.8, colors[2], 0.85)
        if glaze is not None:                                            # light coming through thin stone, on the side away from the lamp
            band(-0.72, -0.3, glaze, 0.6)
        band(0.42, 0.62, colors[3], 0.9, 0.12, 0.9)
        r_top, h_top = profile[-1]
        s.ellipse(x0, yb - h_top * k, r_top * k, max(0.8, r_top * k * sq), mix(colors[0], colors[1], 0.5), alpha)       # the mouth, seen from above
        return x0, yb, k, side, sq


def turned(profile, steps=4):
    """Smooth a jar's profile a little."""
    pts = curve([(r, h) for r, h in profile], steps)
    return [(max(0.3, r), h) for r, h in pts]


# ================================================================ lamps
def flame(pen, at, size=1.0):
    """A lamp's flame: a small hard tear of light. (The game adds the flicker and the glow.) Round four: the tear is
    only painted when the pen says so (as approved); otherwise its place is noted for the game, which draws it moving."""
    x, y = P(*at)
    pen.flames.append((x, y, size))
    if not pen.tongues:
        return
    f = pen.fine
    f.poly([(x - 1.9 * size, y + 0.6 * size), (x - 1.1 * size, y - 2.6 * size), (x + 0.2 * size, y - 6.8 * size), (x + 1.3 * size, y - 2.4 * size), (x + 1.8 * size, y + 0.6 * size), (x, y + 1.6 * size)], "#ffa436")
    f.poly([(x - 1.2 * size, y + 0.4 * size), (x - 0.6 * size, y - 2.2 * size), (x + 0.2 * size, y - 5.0 * size), (x + 0.9 * size, y - 2.0 * size), (x + 1.1 * size, y + 0.4 * size)], "#ffe488")
    f.ellipse(x, y - 0.8 * size, 0.9 * size, 1.6 * size, "#fffbe6")


def dish_lamp(pen, X, Y, D, r=7.0, wick=1.0):
    """A shallow dish of oil with a floating wick. -> where its flame is."""
    k = k_of(D)
    x, y = P(X, Y, D)
    sq = (row_of(D) - G.vy) / G.F
    s = pen.base
    s.poly([(x - r * k, y - 2.4 * k), (x + r * k, y - 2.4 * k), (x + r * k * 0.45, y + 0.6 * k), (x - r * k * 0.45, y + 0.6 * k)], "#6a3826")      # the dish from the side
    s.ellipse(x, y - 2.4 * k, r * k, max(0.9, r * k * sq), "#a85c3a")
    s.ellipse(x, y - 2.4 * k, r * k * 0.8, max(0.7, r * k * sq * 0.75), "#d0963c")       # oil, full of the flame's light
    pen.fine.line([(x - r * k * 0.95, y - 2.4 * k + 0.6), (x + r * k * 0.95, y - 2.4 * k + 0.6)], "#e8a060", 0.8, 0.8)
    at = (X + wick * r * 0.35, Y + 4.5, D)
    flame(pen, at, max(1.0, k * 1.5))
    return at


def lamp_stand(pen, X, D, height, gilt=False, lit=True, stout=1.0):
    """A tall lamp stand: a round stone foot, a slender shaft that opens at the top like a papyrus flower,
    and a dish lamp sitting in it."""
    k = k_of(D) * stout
    stone = (pen.tone("#6d5a52", (X, 3, D), (0, 0.6, 0.8)), pen.tone("#9a8676", (X, 3, D), (0, 0.6, 0.8)), pen.tone("#c4b09a", (X, 4, D), (0, 1, 0)), pen.tone("#e2d2ba", (X, 4, D), (0, 1, 0)))
    pen.lathe(X, D, [(11 * stout, 0), (11.5 * stout, 2.5), (7 * stout, 5.5), (3.2 * stout, 7.5)], stone)
    top = height - 13 * stout
    if gilt:
        pen.gold_rod((X, 7, D), (X, top, D), 1.5 * stout, 1.2, hot=(0.93, 0.6), tone=0.25)
        for t in (0.82, 0.86):                                           # two rings below the flower
            x, y = P(X, lerp(7, top, t), D)
            pen.base.line([(x - 2.4 * k, y), (x + 2.4 * k, y)], "#3a1f0c", 1.2, 0.9)
    else:
        wood = (pen.tone("#3a2418", (X, height * 0.7, D), (0, 0, 1)), pen.tone("#7a5034", (X, height * 0.7, D), (-0.5, 0, 0.8)), pen.tone("#b88858", (X, height * 0.8, D), (-0.5, 0.3, 0.8)))
        pen.rod((X, 7, D), (X, top, D), 1.5 * stout, wood)
    x, y = P(X, top, D)
    cup = [(x - 1.7 * k, y), (x - 2.2 * k, y - 5 * k), (x - 6.4 * k, y - 11.5 * k), (x - 7.6 * k, y - 13 * k), (x + 7.6 * k, y - 13 * k), (x + 6.4 * k, y - 11.5 * k), (x + 2.2 * k, y - 5 * k), (x + 1.7 * k, y)]
    pen.base.poly(cup, "#4a2a10" if gilt else "#4a2c1c")
    pen.base.poly([(x - 0.4 * k, y), (x - 0.6 * k, y - 5 * k), (x - 3.4 * k, y - 11.5 * k), (x - 5.4 * k, y - 13 * k), (x + 1.5 * k, y - 13 * k), (x + 1.2 * k, y - 5 * k), (x + 0.9 * k, y)], "#b8801e" if gilt else "#8c5a34")
    if gilt:
        pen.base.poly([(x - 0.5 * k, y - 4 * k), (x - 2.6 * k, y - 11.5 * k), (x - 4.6 * k, y - 13 * k), (x - 2.0 * k, y - 13 * k), (x - 0.6 * k, y - 8 * k)], "#f0c040")
    for dx in (-3.6, 0.2, 3.8):                                         # the flower's sepals
        pen.base.line([(x + dx * 0.3 * k, y - 3 * k), (x + dx * k, y - 12 * k)], "#2e1c12", 0.8, 0.7)
    pen.fine.line([(x - 7.4 * k, y - 13 * k), (x + 7.4 * k, y - 13 * k)], HOT if gilt else "#d8a060", 0.9, 0.85)
    return dish_lamp(pen, X, height + 2.5, D, r=8.5 * stout) if lit else None


# ================================================================ a thing's own measurements
class Frame:
    """A piece of furniture is drawn in its own measurements (x along it, y up, d from its middle toward
    its front) and then turned and set down in the room. A positive turn swings its +x end toward us."""

    def __init__(self, cx, cd, turn=0.0, lift=0.0):
        self.cx, self.cd, self.lift = cx, cd, lift
        self.c, self.s = math.cos(math.radians(turn)), math.sin(math.radians(turn))

    def w(self, x, y, d):
        return (self.cx + x * self.c - d * self.s, y + self.lift, self.cd + x * self.s + d * self.c)

    def n(self, nx, ny, nd):
        return (nx * self.c - nd * self.s, ny, nx * self.s + nd * self.c)

    def outline(self, x0, x1, d0, d1):
        """Corners on the floor: near-left, near-right, far-right, far-left (d1 is the near side)."""
        return [self.w(x, 0, d)[::2] for x, d in ((x0, d1), (x1, d1), (x1, d0), (x0, d0))]

    def seen(self, nx, nd, at=(0.0, 0.0)):
        """Can we see a face of this thing whose normal (in its own measurements) is (nx, nd)?"""
        n = self.n(nx, 0, nd)
        p = self.w(at[0], 0, at[1])
        return (0 - p[0]) * n[0] + (DCAM - p[2]) * n[2] > 0


def face_normal(quad):
    """The way a flat face looks, turned to point at the lens."""
    a, b, c = [np.array(q, dtype=float) for q in quad[:3]]
    n = np.cross(b - a, c - a)
    n = n / (np.linalg.norm(n) + 1e-9)
    mid = (a + c) / 2
    cam = np.array([0.0, G.eye, DCAM])
    if n @ (cam - mid) < 0:
        n = -n
    return (float(n[0]), float(n[1]), float(n[2]))


def gold_face(pen, quad, n, gain=1.0, lift=0.0, streaks=1, edge=True, seed=0):
    """A flat sheet of gold. Upright, it mirrors the dark floor low down and the lamplit stone higher up;
    it is lighter toward the lamp, has a slanting gleam or two, and a hard light along its upper edge."""
    rng = np.random.default_rng(seed + 11)
    cen = pen.on(quad, 0.5, 0.5)

    def g(lf):
        return pen.gold(cen, n, gain, lift + lf)
    pen.poly(quad, g(0.0))
    e = pen.e(*cen, n, 0.4) * gain
    es = [pen.e(*pen.on(quad, u, v), n, 0.4) for u, v in ((0, 0.5), (1, 0.5))]
    hi = 1 if es[1] > es[0] else 0
    upright = abs(n[1]) < 0.5
    if upright:
        pen.patch(quad, 0, 1, 0.0, 0.34, g(-0.13), 0.85)                 # the dark floor, mirrored
        pen.patch(quad, 0, 1, 0.52, 0.86, g(0.10), 0.75)                 # the lamplit wall, mirrored
        pen.patch(quad, 0, 1, 0.86, 1.0, g(-0.04), 0.6)
    a0, a1 = (0.62, 1.0) if hi else (0.0, 0.38)                          # lighter on the side the lamp is
    pen.patch(quad, a0, a1, 0, 1, g(0.12), 0.5)
    a0, a1 = (0.0, 0.2) if hi else (0.8, 1.0)
    pen.patch(quad, a0, a1, 0, 1, g(-0.12), 0.55)
    for i in range(streaks):                                            # the sheet is not quite flat: slanting gleams
        if e < 0.3:
            break
        u = 0.12 + 0.62 * rng.random()
        w = 0.04 + 0.07 * rng.random()
        pen.poly([pen.on(quad, u, 0.04), pen.on(quad, u + w, 0.04), pen.on(quad, u + w + 0.14, 0.96), pen.on(quad, u + 0.14, 0.96)], g(0.3), 0.6)
    if edge:
        pen.stroke(quad, 0, 1, 1, 1, g(0.42), 0.9, 0.9)
        pen.stroke(quad, 0, 0, 1, 0, "#1c0f0a", 0.8, 0.75)
    return e


def wood_face(pen, quad, n, wood, gain=1.0, grain=3, seed=0, along=True):
    rng = np.random.default_rng(seed + 5)
    cen = pen.on(quad, 0.5, 0.5)
    base = pen.tone(wood, cen, n, gain)
    pen.poly(quad, base)
    for i in range(grain):
        t = (i + 0.3 + 0.4 * rng.random()) / grain
        if along:
            pen.stroke(quad, 0.02, t, 0.98, t + rng.normal(0, 0.03), base * 0.72, 0.7, 0.55)
        else:
            pen.stroke(quad, t, 0.02, t + rng.normal(0, 0.03), 0.98, base * 0.72, 0.7, 0.55)
    return base


def band(pen, quad, u0, u1, v0, v1, n, gain=1.0, lift=0.0, hot=None):
    """A strip of gold laid on a face."""
    q = [pen.on(quad, u0, v0), pen.on(quad, u1, v0), pen.on(quad, u1, v1), pen.on(quad, u0, v1)]
    cen = pen.on(q, 0.5, 0.5)
    pen.poly(q, pen.gold(cen, n, gain, lift))
    e = pen.e(*cen, n, 0.4) * gain
    wide = abs(u1 - u0) * math.dist(P(*quad[0]), P(*quad[1])) > abs(v1 - v0) * math.dist(P(*quad[0]), P(*quad[3]))
    if wide:                                                            # a light along its upper edge, a dark one under it
        pen.line([q[3], q[2]], pen.gold(cen, n, gain, lift + 0.36), 0.8, 0.9)
        pen.line([q[0], q[1]], "#1c0f0a", 0.7, 0.6)
    else:
        pen.line([q[0], q[3]], pen.gold(cen, n, gain, lift + 0.36), 0.8, 0.9)
        pen.line([q[1], q[2]], "#1c0f0a", 0.7, 0.6)
    if hot is not None and e > 0.3:
        pen.spark(pen.on(q, hot[0], hot[1]), 0.7)
    return q


def gold_box(pen, outline, y0, y1, gain=1.0, lift=0.0, seed=0, streaks=1, top=True):
    """A box sheathed in gold."""
    f = pen.box(outline, y0, y1, lambda at, n: pen.gold(at, n, gain, lift), top=None if top else False)
    for i, (name, q) in enumerate(f.items()):
        gold_face(pen, q, face_normal(q), gain, lift + (0.10 if name == "top" else 0.0), streaks if name != "top" else 0, True, seed + i)
    return f


def wood_box(pen, outline, y0, y1, wood, gain=1.0, seed=0, grain=2, top=True):
    f = pen.box(outline, y0, y1, lambda at, n: pen.tone(wood, at, n, gain), top=None if top else False)
    for i, (name, q) in enumerate(f.items()):
        wood_face(pen, q, face_normal(q), wood, gain * (1.1 if name == "top" else 1.0), grain, seed + i)
    return f


# ================================================================ jars, baskets, cloth
def jar_colors(pen, X, D, h, albedo, dark=0.45, gain=1.0, wrap=0.45):
    at = (X, h * 0.6, D)
    lit, _ = pen.toward(*at)
    sd = 1 if lit[0] >= 0 else -1
    n_l = (0.6 * sd, 0.45, 0.66)
    n_d = (-0.8 * sd, 0.0, 0.6)
    a = _c(albedo)
    return (pen.tone(a * dark, at, n_d, gain, wrap), pen.tone(a * 0.86, at, (0, 0.3, 0.95), gain, wrap), pen.tone(a, at, n_l, gain * 1.15, wrap), pen.tone(mix(a, "#ffffff", 0.5), at, n_l, gain * 1.6, wrap))


ALABASTER_TALL = [(5.5, 0), (6.5, 1.5), (7.5, 8), (8.6, 26), (9.2, 40), (8.6, 47), (6.2, 50), (6.8, 52), (9.6, 53.5), (9.6, 55)]
ALABASTER_CYL = [(7.6, 0), (7.9, 1.2), (6.6, 3), (6.4, 20), (6.9, 34), (8.9, 37), (8.9, 38.2)]
ALABASTER_SHOULDER = [(4.5, 0), (5.2, 1.2), (8.5, 10), (11.5, 24), (11.0, 32), (7.0, 37), (5.6, 38.5), (7.4, 41), (7.4, 42)]
POT_JAR = [(5, 0), (6, 1), (10, 8), (12.5, 18), (11.5, 26), (7.5, 31), (6.8, 33), (8.2, 35), (8.2, 36)]
OIL_JAR = [(6, 0), (7, 1), (13, 10), (17, 24), (16, 36), (10, 44), (8.5, 47), (10.5, 49.5), (10.5, 51)]


def alabaster(pen, X, D, profile, y0=0.0, lid=True, gain=1.5, seed=0):
    """A jar of pale banded stone, thin enough for the lamplight to come a little way through it."""
    rng = np.random.default_rng(seed + 31)
    h = profile[-1][1]
    cols = jar_colors(pen, X, D, y0 + h, STUFF["alabaster"], 0.5, gain, 0.6)
    glaze = mix(cols[1], "#f2a25c", 0.55)
    prof = turned(profile, 3)
    x0, yb, k, side, sq = pen.lathe(X, D, prof, cols, y0=y0, glaze=glaze)
    s = pen.base
    hs, rs = [p[1] for p in prof], [p[0] for p in prof]
    for i in range(3):                                                    # the stone's own bands, level and wavering
        hh = h * (0.2 + 0.55 * rng.random())
        r = float(np.interp(hh, hs, rs))
        s.line([(x0 - r * k * 0.92, yb - hh * k), (x0, yb - hh * k + sq * r * k * 0.6), (x0 + r * k * 0.92, yb - hh * k)], mix(cols[0], cols[1], 0.5), 0.7, 0.4)
    if lid:                                                              # a linen cover tied down with cord, and a lump of mud to seal it
        r, hh = profile[-1]
        s.poly([(x0 - r * k * 1.08, yb - (hh + 0.6) * k), (x0 + r * k * 1.08, yb - (hh + 0.6) * k), (x0 + r * k * 0.96, yb - (hh - 3.4) * k), (x0 - r * k * 0.96, yb - (hh - 3.4) * k)], pen.tone("#cfc3ac", (X, y0 + hh, D), (0, 0.2, 1), gain * 0.8))
        s.ellipse(x0, yb - (hh + 0.8) * k, r * k * 1.08, max(1.0, r * k * sq * 1.1), pen.tone(STUFF["linen"], (X, y0 + hh, D), (0, 1, 0.3), gain))
        s.line([(x0 - r * k * 0.98, yb - (hh - 2.4) * k), (x0 + r * k * 0.98, yb - (hh - 2.4) * k)], "#6a5238", 0.8, 0.9)
        s.ellipse(x0 + side * r * k * 0.2, yb - (hh + 1.2) * k, 1.7 * k, 1.1 * k, "#6e5a48")
    rr = float(np.interp(h * 0.62, hs, rs))
    pen.fine.line([(x0 + side * rr * k * 0.5, yb - h * k * 0.74), (x0 + side * rr * k * 0.5, yb - h * k * 0.5)], "#fffaf0", 0.9, 0.75)
    return x0, yb, k


def pot(pen, X, D, profile, albedo="pot", y0=0.0, gain=1.0, rim=True):
    """A plain pottery jar."""
    h = profile[-1][1]
    cols = jar_colors(pen, X, D, y0 + h, STUFF[albedo] if albedo in STUFF else albedo, 0.42, gain)
    x0, yb, k, side, sq = pen.lathe(X, D, turned(profile, 3), cols, y0=y0)
    r, hh = profile[-1]
    if rim:
        pen.base.ellipse(x0, yb - hh * k, r * k * 0.72, max(0.7, r * k * sq * 0.7), "#1c1014")
    return x0, yb, k, side, sq


def basket(pen, X, D, r=20.0, h=30.0, y0=0.0, lid=True, gain=1.15, seed=0):
    """A coiled basket with bands of dark pattern, and a pointed lid."""
    prof = [(r * 0.72, 0), (r * 0.8, 1), (r, h * 0.55), (r * 0.96, h)]
    cols = jar_colors(pen, X, D, y0 + h, STUFF["basket"], 0.5, gain)
    x0, yb, k, side, sq = pen.lathe(X, D, prof, cols, y0=y0)
    s = pen.base
    for i in range(1, int(h / 3.2)):                                     # the coils
        hh = i * 3.2
        rr = float(np.interp(hh, [p[1] for p in prof], [p[0] for p in prof]))
        dip = sq * rr * k * 0.55
        s.line([(x0 - rr * k, yb - hh * k), (x0 - rr * k * 0.5, yb - hh * k + dip * 0.8), (x0, yb - hh * k + dip), (x0 + rr * k * 0.5, yb - hh * k + dip * 0.8), (x0 + rr * k, yb - hh * k)],
               "#3a2418" if i % 3 == 0 else mix(cols[0], cols[1], 0.3), 1.0 if i % 3 == 0 else 0.7, 0.75 if i % 3 == 0 else 0.5)
    for i in range(7):                                                   # a row of dark red triangles round the belly
        t = (i + 0.5) / 7
        a = (t - 0.5) * 2
        rr = r * 0.98
        bx = x0 + a * rr * k * 0.96
        by = yb - h * 0.52 * k + sq * rr * k * 0.55 * (1 - a * a)
        w = (rr * k * 0.12) * (1 - a * a * 0.7)
        s.poly([(bx - w, by + 2.2 * k), (bx + w, by + 2.2 * k), (bx, by - 3.0 * k)], "#6a2a22", 0.85)
    if lid:
        top = yb - h * k
        s.poly([(x0 - r * k, top + 1), (x0 - r * k * 0.5, top - h * 0.16 * k), (x0, top - h * 0.34 * k), (x0 + r * k * 0.5, top - h * 0.16 * k), (x0 + r * k, top + 1), (x0, top + sq * r * k)], cols[1])
        s.poly([(x0 + side * r * k * 0.1, top - h * 0.31 * k), (x0 + side * r * k * 0.55, top - h * 0.15 * k), (x0 + side * r * k, top + 1), (x0 + side * r * k * 0.3, top + sq * r * k * 0.7)], cols[2], 0.8)
        s.poly([(x0 - side * r * k, top + 1), (x0 - side * r * k * 0.5, top - h * 0.16 * k), (x0 - side * r * k * 0.1, top - h * 0.3 * k), (x0 - side * r * k * 0.35, top + sq * r * k * 0.6)], cols[0], 0.8)
        for j in (0.33, 0.66):
            s.line([(x0 - r * k * (1 - j), top - h * 0.34 * k * j), (x0, top - h * 0.34 * k * j + sq * r * k * (1 - j) * 0.6), (x0 + r * k * (1 - j), top - h * 0.34 * k * j)], "#3a2418", 0.8, 0.6)
        s.ellipse(x0, top - h * 0.36 * k, 1.5 * k, 1.2 * k, cols[0])
    return x0, yb, k


def linen_stack(pen, F, x0, x1, d0, d1, y0, h, folds=4, gain=1.7, seed=0):
    """Folded linen: a soft white block, its folds showing as fine lines along the side."""
    rng = np.random.default_rng(seed + 3)
    o = F.outline(x0, x1, d0, d1)
    f = pen.box(o, y0 + F.lift, y0 + h + F.lift, lambda at, n: pen.tone(STUFF["linen"], at, n, gain * (0.5 if abs(n[1]) < 0.5 else 1.0), 0.45))
    for name in ("near", "right", "left"):
        if name in f:
            q = f[name]
            for i in range(1, folds):
                v = i / folds + rng.normal(0, 0.03)
                pen.stroke(q, 0.0, v, 1.0, v + rng.normal(0, 0.03), "#7c7488", 0.7, 0.7)
            pen.stroke(q, 0, 1, 1, 1, "#fffaf0", 0.8, 0.8)
    if "top" in f:
        q = f["top"]
        pen.patch(q, 0.08, 0.6, 0.15, 0.85, mix(pen.tone(STUFF["linen"], pen.on(q, 0.5, 0.5), (0, 1, 0), gain, 0.45), "#fffdf2", 0.3), 0.7)
        pen.stroke(q, 0.5, 0.0, 0.52, 1.0, "#a39aa6", 0.7, 0.5)
    return f


def drape(pen, pts, shade=0.7, folds=4, gain=1.6, seed=0):
    """A cloth hanging: `pts` (room cm: top left, top right, bottom right, bottom left) outline it; folds run down it."""
    rng = np.random.default_rng(seed)
    cen = tuple(np.mean(np.array(pts), axis=0))
    base = pen.tone(STUFF["linen"], cen, (0, 0.1, 1), gain * shade, 0.45)
    pen.poly(pts, base)
    top = np.array(pts[0]), np.array(pts[1])
    bot = np.array(pts[3]), np.array(pts[2])
    for i in range(1, folds + 1):
        t = i / (folds + 1) + rng.normal(0, 0.03)
        a, b = lerp(top[0], top[1], t), lerp(bot[0], bot[1], t + rng.normal(0, 0.05))
        pen.line([tuple(a), tuple(lerp(a, b, 0.5) + np.array([rng.normal(0, 1.2), 0, 0])), tuple(b)], "#7c7488" if i % 2 else "#fffaf0", 0.9, 0.7)
    return base


def lion_leg(pen, F, x, d, height, facing=-1, gain=1.0, hind=False):
    """A bed's or chair's leg carved as a lion's, standing on a ribbed drum, sheathed in gold. `facing` is
    the way the paw points along the thing (-1 or +1)."""
    s = facing
    H = height
    knee = 4.8 if hind else 3.2
    hock = 0.0 if hind else -1.4
    prof = [(-3.6, 0), (3.6, 0), (3.1, 4.6), (2.6, 5.0), (2.8, 8.4), (2.2, 9.5), (knee, 15), (knee + 1.0, H * 0.78), (4.8, H), (-4.4, H),
            (-4.0, H * 0.78), (hock, 15), (-2.8, 10.2), (-5.6, 8.6), (-5.9, 6.2), (-4.6, 5.0), (-3.1, 4.6)]

    def lx(px):
        return x + (px if s < 0 else -px)
    at = F.w(x, H * 0.5, d)
    n = F.n(0, 0, 1)
    pen.poly([F.w(lx(px), py, d) for px, py in prof], pen.gold(at, n, gain, -0.03))
    lit, strength = pen.toward(*at)
    sd = 1 if lit[0] >= 0 else -1
    front = [(4.8, H), (knee + 1.0, H * 0.78), (knee, 15), (2.2, 9.5)]
    backe = [(-4.4, H), (-4.0, H * 0.78), (hock, 15), (-2.8, 10.2), (-5.6, 8.6)]
    edge = front if (sd > 0) == (s < 0) else backe
    inner = [(px * 0.3, py) for px, py in reversed(edge)]
    pen.poly([F.w(lx(px), py, d) for px, py in edge + inner], pen.gold(at, n, gain, 0.2), 0.9)
    for yy in (1.6, 3.2):
        pen.line([F.w(lx(-3.4), yy, d), F.w(lx(3.4), yy, d)], "#1c0f0a", 0.7, 0.7)
    pen.line([F.w(lx(-3.6), 4.8, d), F.w(lx(3.4), 4.8, d)], pen.gold(at, n, gain, 0.36), 0.8, 0.9)
    if strength * gain > 0.4:
        pen.line([F.w(lx(px), py, d) for px, py in edge], HOT, 0.8, min(0.9, 0.3 + strength * gain * 0.3), fine=True)
    return at


# ================================================================ the king's things
def canopy_poles(pen, seed=3):
    """The poles of a gilded canopy, leaning against the wall in a bundle, tied twice round with cord."""
    x0, x1 = PLACE["poles"]
    rng = np.random.default_rng(seed)
    poles = []
    n = 10
    for i in range(n):
        bx = lerp(x0, x1, i / (n - 1)) + rng.normal(0, 1.2)
        bd = 34 + rng.random() * 22
        thick = i % 3 == 0
        ty = 268 + rng.random() * 40 if thick else 182 + rng.random() * 58
        tx = bx + rng.normal(5, 5)
        poles.append((bd, bx, tx, ty, 2.7 if thick else 1.8, i))
    ends = []
    for bd, bx, tx, ty, r, i in sorted(poles):
        a, b = (bx, 0, bd), (tx, ty, 2.5 + r)
        pen.gold_rod(a, b, r, hot=(0.45 + 0.4 * rng.random(),) if i in (2, 7) else (), tone=rng.normal(-0.08, 0.12))
        pa, pb = np.array(P(*a)), np.array(P(*b))
        u = (pb - pa) / (np.linalg.norm(pb - pa) + 1e-9)
        q = np.array([-u[1], u[0]])
        k = k_of(b[2])
        if r < 2.5:                                                      # a papyrus bud on the end of the slender ones
            bud = [pb + q * 1.1 * k, pb + u * 3 * k + q * 3.6 * k, pb + u * 9 * k + q * 2.4 * k, pb + u * 14 * k, pb + u * 9 * k - q * 2.4 * k, pb + u * 3 * k - q * 3.6 * k, pb - q * 1.1 * k]
            pen.base.poly(bud, "#6a3a10")
            pen.base.poly([pb - q * 0.2 * k, pb + u * 3 * k - q * 3.2 * k, pb + u * 9 * k - q * 2.2 * k, pb + u * 13.4 * k, pb + u * 9 * k - q * 0.2 * k], "#c8861f")
            pen.fine.line([pb + u * 4 * k - q * 2.4 * k, pb + u * 9 * k - q * 1.5 * k], HOT, 0.8, 0.9)
            pen.base.line([pb - q * 2.2 * k, pb + q * 2.2 * k], "#1c0f0a", 1.0, 0.9)
        else:                                                            # the corner posts end in a square tenon
            pen.base.line([pb, pb + u * 6 * k], "#5a3410", 2.4 * k)
            pen.base.line([pb + u * 0.5 * k - q * 2.6 * k, pb + u * 0.5 * k + q * 2.6 * k], "#d9a02c", 1.0, 0.9)
        ends.append((a, b))
    for hgt in (92.0, 160.0):                                            # the lashings
        xs = []
        for a, b in ends:
            t = hgt / b[1]
            xs.append(P(a[0] + (b[0] - a[0]) * t, hgt, a[2] + (b[2] - a[2]) * t))
        lo, hi = min(xs), max(xs)
        for j in range(3):
            pen.base.line([(lo[0] - 1.5, lo[1] + j * 1.5 - 1), ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2 + j * 1.5 + 0.8), (hi[0] + 1.5, hi[1] + j * 1.5 - 1)], mix("#7a5a38", "#d8bc88", j / 2), 1.0, 0.95)
        pen.base.line([(hi[0] + 1, hi[1]), (hi[0] + 3, hi[1] + 7), (hi[0] + 1.5, hi[1] + 12)], "#b89a66", 0.9, 0.9)     # the loose end hangs


def mats(pen):
    """Reed mats, rolled and stood on end."""
    for sd, (X, D, h, r) in enumerate(PLACE["mats"]):
        cols = jar_colors(pen, X, D, h, STUFF["reed"], 0.5)
        x0, yb, k, side, sq = pen.lathe(X, D, [(r, 0), (r, h)], cols)
        s = pen.base
        for i in range(5):                                               # the reeds run up and down it
            a = -0.85 + 1.7 * (i + 0.5) / 5
            s.line([(x0 + a * r * k, yb - 1), (x0 + a * r * k, yb - h * k + 1)], mix(cols[0], cols[1], 0.5), 0.6, 0.45)
        for t in (0.16, 0.5, 0.84):                                      # tied in three places
            yy = yb - h * k * t
            s.line([(x0 - r * k, yy), (x0, yy + sq * r * k * 0.5), (x0 + r * k, yy)], "#4a3220", 1.1, 0.9)
        top = yb - h * k
        s.ellipse(x0, top, r * k, max(1.0, r * k * sq), mix(cols[1], cols[2], 0.5))
        s.ellipse(x0, top, r * k * 0.6, max(0.8, r * k * sq * 0.6), cols[0])        # the roll, seen on end
        s.ellipse(x0, top, r * k * 0.28, max(0.6, r * k * sq * 0.28), cols[1])


def headrest(pen, X, Y, D, gain=1.0):
    """A headrest: a curved cradle on a little column."""
    k = k_of(D)
    x, y = P(X, Y, D)
    s = pen.base
    at = (X, Y + 8, D)
    g0, g1, g2 = pen.gold(at, (0, 0.3, 1), gain, -0.08), pen.gold(at, (0, 0.3, 1), gain, 0.12), pen.gold(at, (0, 0.6, 1), gain, 0.36)
    s.poly([(x - 8 * k, y), (x + 8 * k, y), (x + 7 * k, y - 2.2 * k), (x - 7 * k, y - 2.2 * k)], g0)
    s.poly([(x - 1.8 * k, y - 2.2 * k), (x + 1.8 * k, y - 2.2 * k), (x + 1.5 * k, y - 11 * k), (x - 1.5 * k, y - 11 * k)], g1)
    arc = [(x + a * 9.5 * k, y - (11 + 5.5 * a * a) * k) for a in np.linspace(-1, 1, 9)]
    s.line(arc, g0, 2.6 * k)
    s.line([(px, py - 0.5 * k) for px, py in arc], g2, 1.0, 0.95)
    pen.spark((x - 6.5 * k, y - 14.6 * k), 0.7)


def bed(pen):
    """A bed that slopes down a little toward its foot, on four lion's legs, with a footboard, sheathed
    in gold. Folded linen, a headrest and a basket are piled on it."""
    cx, cd, turn = PLACE["bed"]
    F = Frame(cx, cd, turn)
    L, Wd = 86.0, 39.0

    def top(x):
        return 35.0 - (x + L) / (2 * L) * 5.0

    def rail(d0, d1, seed, gain=1.0):                                    # a side rail: a sloping gold beam
        nd = 1 if d1 > 0 else -1
        if F.seen(0, nd, (0, d1 if nd > 0 else d0)):
            dd = d1 if nd > 0 else d0
            q = [F.w(-L, top(-L) - 7, dd), F.w(L, top(L) - 7, dd), F.w(L, top(L), dd), F.w(-L, top(-L), dd)]
            gold_face(pen, q, F.n(0, 0, nd), gain, 0.0, 2, True, seed)
        q = [F.w(-L, top(-L), d1), F.w(L, top(L), d1), F.w(L, top(L), d0), F.w(-L, top(-L), d0)]
        gold_face(pen, q, (0, 1, 0), gain, 0.12, 0, False, seed + 1)
        return q
    # under the bed it is dark
    pen.poly([F.w(-L, 0, Wd), F.w(L, 0, Wd), F.w(L, top(L) - 7, Wd), F.w(-L, top(-L) - 7, Wd)], "#140c12", 0.8)
    for x, d, hind in ((-78, -34, False), (78, -34, True)):               # the far legs
        lion_leg(pen, F, x, d, top(x) - 7, -1, 0.5, hind)
    rail(-Wd, -Wd + 6, 1, 0.8)
    # the webbing, laced across the frame
    web = [F.w(-L + 5, top(-L) - 1.5, Wd - 6), F.w(L - 2, top(L) - 1.5, Wd - 6), F.w(L - 2, top(L) - 1.5, -Wd + 6), F.w(-L + 5, top(-L) - 1.5, -Wd + 6)]
    wcol = pen.tone("#b79a6c", pen.on(web, 0.5, 0.5), (0, 1, 0), 1.2)
    pen.poly(web, wcol)
    for i in range(1, 12):
        pen.stroke(web, i / 12, 0, i / 12, 1, wcol * 0.7, 0.6, 0.55)
    for j in (0.25, 0.5, 0.75):
        pen.stroke(web, 0, j, 1, j, wcol * 0.74, 0.6, 0.5)
    gold_face(pen, [F.w(-L, top(-L), Wd), F.w(-L + 6, top(-L), Wd), F.w(-L + 6, top(-L), -Wd), F.w(-L, top(-L), -Wd)], (0, 1, 0), 1.0, 0.1, 0, False, 4)
    # what lies on it
    linen_stack(pen, F, -74, -30, -27, 20, top(-52) - 1, 21, folds=6, seed=1)
    st = linen_stack(pen, F, -26, 6, -20, 25, top(-10) - 1, 10, folds=3, seed=2)
    if "top" in st:                                                      # the top cloth is striped with blue
        for u in (0.16, 0.26, 0.74, 0.84):
            pen.stroke(st["top"], u, 0.03, u, 0.97, "#30508e", 1.2, 0.85)
        if "near" in st:
            for u in (0.16, 0.26, 0.74, 0.84):
                pen.stroke(st["near"], u, 0.72, u, 1.0, "#263f74", 1.1, 0.85)
    hx = F.w(-52, top(-52) + 20, -4)
    headrest(pen, hx[0], hx[1], hx[2])
    bx = F.w(38, top(38) - 1, -4)
    basket(pen, bx[0], bx[2], r=15.0, h=21.0, y0=bx[1], seed=4)
    # the footboard: a framed panel with three papyrus stems
    fy0, fy1 = top(L), top(L) + 46.0
    if F.seen(1, 0, (L, 0)):
        q = [F.w(L, fy0, Wd), F.w(L, fy0, -Wd), F.w(L, fy1, -Wd), F.w(L, fy1, Wd)]
        n = F.n(1, 0, 0)
        gold_face(pen, q, n, 1.0, 0.04, 0, True, 6)
        inner = [pen.on(q, 0.14, 0.12), pen.on(q, 0.86, 0.12), pen.on(q, 0.86, 0.86), pen.on(q, 0.14, 0.86)]
        cen = pen.on(q, 0.5, 0.5)
        pen.poly(inner, pen.gold(cen, n, 1.0, -0.16))
        for i in range(3):                                               # three papyrus stems, each with its bud
            u = 0.2 + 0.6 * i / 2
            pen.stroke(inner, u, 0.04, u, 0.7, pen.gold(cen, n, 1.0, 0.24), 0.9, 0.95)
            pen.poly([pen.on(inner, u - 0.1, 0.7), pen.on(inner, u + 0.1, 0.7), pen.on(inner, u, 0.96)], pen.gold(cen, n, 1.0, 0.36))
        pen.dash(q[3], q[2], 0.0, 0.6)
        pen.dash(q[0], q[3], 0.45, 1.0)
        pen.spark(pen.on(q, 0.0, 1.0), 0.9)
    gold_face(pen, [F.w(L - 3, fy1, Wd), F.w(L, fy1, Wd), F.w(L, fy1, -Wd), F.w(L - 3, fy1, -Wd)], (0, 1, 0), 1.0, 0.22, 0, False, 7)
    rail(Wd - 6, Wd, 8)
    pen.dash(F.w(-L, top(-L), Wd), F.w(L, top(L), Wd), 0.3, 0.62)
    pen.dash(F.w(-L, top(-L), Wd), F.w(L, top(L), Wd), 0.7, 0.78)
    for x, d, hind in ((-78, 35, False), (78, 35, True)):                 # the near legs
        lion_leg(pen, F, x, d + 3, top(x) - 7, -1, 1.0, hind)
    return F


def carrying_chair(pen):
    """A carrying-chair: a low seat with a tall back, between two long poles whose ends are gold."""
    cx, cd, turn = PLACE["chair"]
    F = Frame(cx, cd, turn)

    def pole(d, gain):
        a, b = F.w(-98, 6, d), F.w(98, 6, d)
        pen.rod(a, b, 3.2, tuple(pen.tone(c, F.w(0, 6, d), F.n(0, 0.5, 0.8), gain) for c in ("#4a2c20", "#8a5c40", "#c89868")))
        for s in (-1, 1):                                                # gold ends that open like a papyrus flower
            e0, e1 = F.w(s * 76, 6, d), F.w(s * 98, 6, d)
            pen.gold_rod(e0, e1, 3.6, gain, hot=(0.5,) if (s > 0 and gain > 0.8) else ())
            p1, p0 = np.array(P(*e1)), np.array(P(*e0))
            u = (p1 - p0) / (np.linalg.norm(p1 - p0) + 1e-9)
            q = np.array([-u[1], u[0]])
            k = k_of(e1[2])
            pen.base.poly([p1 - q * 3.6 * k, p1 + u * 4 * k - q * 6.0 * k, p1 + u * 5.5 * k, p1 + u * 4 * k + q * 6.0 * k, p1 + q * 3.6 * k], pen.gold(e1, (0, 0.4, 0.9), gain, 0.06))
            pen.fine.line([p1 + u * 3.6 * k - q * 5.0 * k, p1 + u * 5 * k], HOT, 0.9, 0.85 * gain)
            pen.base.line([p0 - q * 3.8 * k, p0 + q * 3.8 * k], "#1c0f0a", 1.0, 0.8)
    pole(-27, 0.6)
    # the seat: a low box of dark wood banded with gold, a rush pad on it
    seat = wood_box(pen, F.outline(-30, 32, -24, 24), 9, 21, WOODS["ebony"], 1.0, 3)
    for name in ("near", "right"):
        if name in seat:
            band(pen, seat[name], 0, 1, 0.72, 1.0, face_normal(seat[name]), 1.0, 0.0)
            band(pen, seat[name], 0, 1, 0.0, 0.2, face_normal(seat[name]), 0.9, -0.06)
    if "top" in seat:
        pen.patch(seat["top"], 0.06, 0.97, 0.08, 0.92, pen.tone("#c9b48c", pen.on(seat["top"], 0.5, 0.5), (0, 1, 0), 1.3))
        for i in range(1, 6):
            pen.stroke(seat["top"], 0.06 + 0.91 * i / 6, 0.08, 0.06 + 0.91 * i / 6, 0.92, "#7a6648", 0.6, 0.5)
    gold_box(pen, F.outline(-30, 32, -24, -21), 21, 40, 0.7, -0.04, 21)
    back = gold_box(pen, F.outline(-31, -27, -24, 24), 21, 68, 1.0, 0.0, 22, streaks=1)
    if "right" in back:
        q = back["right"]
        n = face_normal(q)
        cen = pen.on(q, 0.5, 0.5)
        pen.patch(q, 0.16, 0.84, 0.10, 0.90, pen.gold(cen, n, 1.0, -0.14))
        for v in (0.36, 0.62):
            pen.stroke(q, 0.16, v, 0.84, v, pen.gold(cen, n, 1.0, 0.26), 0.8, 0.9)
        pen.dash(q[3], q[2], 0.0, 1.0)
        pen.spark(pen.on(q, 0.1, 1.0), 0.8)
    arm = gold_box(pen, F.outline(-30, 32, 21, 24), 21, 40, 1.0, 0.0, 23)
    if "near" in arm:
        q = arm["near"]
        n = face_normal(q)
        pen.patch(q, 0.08, 0.92, 0.2, 0.78, "#1c1016", 0.92)             # the arm is open work: stems between two rails
        for u in (0.22, 0.36, 0.5, 0.64, 0.78):
            pen.stroke(q, u, 0.2, u, 0.78, pen.gold(pen.on(q, u, 0.5), n, 1.0, 0.16), 1.1, 1.0)
        pen.dash(q[3], q[2], 0.1, 0.55)
    pole(27, 1.0)
    pen.spark(F.w(98, 9, 27), 0.9)
    return F


def armchair(pen):
    """An armchair: low and square, lion's legs, a tall back, the arms framed in gold."""
    cx, cd, turn = PLACE["arm"]
    F = Frame(cx, cd, turn)
    Wd, Dp, seat, armh, backh = 33.0, 30.0, 34.0, 58.0, 90.0
    for x, d in ((-27, -24), (27, -24)):
        lion_leg(pen, F, x, d, seat - 6, 1, 0.45, True)
    pen.poly([F.w(-Wd, 2, Dp - 2), F.w(Wd, 2, Dp - 2), F.w(Wd, seat - 6, Dp - 2), F.w(-Wd, seat - 6, Dp - 2)], "#140c12", 0.8)       # dark under the seat
    # the back: a tall framed panel
    back = gold_box(pen, F.outline(-Wd, Wd, -Dp, -Dp + 4), seat, backh, 1.0, 0.0, 31, streaks=0)
    if "near" in back:
        q = back["near"]
        n = face_normal(q)
        cen = pen.on(q, 0.5, 0.5)
        pen.patch(q, 0.1, 0.9, 0.06, 0.9, pen.gold(cen, n, 1.0, -0.14))
        pen.patch(q, 0.16, 0.84, 0.12, 0.84, pen.gold(cen, n, 1.0, -0.02))
        pen.poly([pen.on(q, 0.16, 0.5), pen.on(q, 0.5, 0.12), pen.on(q, 0.62, 0.12), pen.on(q, 0.16, 0.66)], pen.gold(cen, n, 1.0, 0.22), 0.7)     # the lamp, mirrored askew
        pen.poly([pen.on(q, 0.2, 0.84), pen.on(q, 0.84, 0.3), pen.on(q, 0.84, 0.42), pen.on(q, 0.36, 0.84)], pen.gold(cen, n, 1.0, 0.12), 0.6)
        pen.poly([pen.on(q, 0.16, 0.58), pen.on(q, 0.34, 0.38), pen.on(q, 0.38, 0.4), pen.on(q, 0.16, 0.64)], HOT, 0.75, fine=True)
        pen.dash(q[3], q[2], 0.0, 0.7)
        pen.dash(q[0], q[3], 0.5, 1.0, HOT, 0.8, 0.8)
        pen.spark(pen.on(q, 0.03, 0.98), 1.0)
    # the far arm (we see its inner side), the seat, the near arm
    for x0, x1, seed, gain in ((-Wd, -Wd + 3, 33, 0.8), (Wd - 3, Wd, 34, 1.0)):
        arm = pen.box(F.outline(x0, x1, -Dp + 4, Dp - 4), seat, armh, lambda at, n: pen.gold(at, n, gain, -0.03))
        for name, q in arm.items():
            n = face_normal(q)
            if name in ("right", "left"):
                pen.patch(q, 0.10, 0.9, 0.12, 0.82, "#1a0f15", 0.93)      # open work: four plain slats under the arm rail
                for u in (0.26, 0.42, 0.58, 0.74):
                    pen.stroke(q, u, 0.12, u, 0.82, pen.gold(pen.on(q, u, 0.5), n, gain, 0.16), 1.2, 1.0)
                pen.stroke(q, 0, 1, 1, 1, pen.gold(pen.on(q, 0.5, 1), n, gain, 0.4), 0.9, 0.9)
            elif name == "top":
                pen.poly(q, pen.gold(pen.on(q, 0.5, 0.5), (0, 1, 0), gain, 0.2))
                pen.dash(q[0], q[3], 0.1, 0.6, HOT, 0.9, 0.85 * gain)
            elif name == "near":
                gold_face(pen, q, n, gain, 0.05, 0, True, seed)
        if x0 < 0:
            sb = gold_box(pen, F.outline(-Wd + 3, Wd - 3, -Dp + 4, Dp), seat - 6, seat, 1.0, 0.0, 35, streaks=0)
            cq = [F.w(-Wd + 5, seat, Dp - 2), F.w(Wd - 5, seat, Dp - 2), F.w(Wd - 5, seat, -Dp + 6), F.w(-Wd + 5, seat, -Dp + 6)]
            cu = pen.box([c[::2] for c in cq], seat, seat + 5, lambda at, n: pen.tone("#e4d8c0" if n[1] > 0.5 else "#a89c8c", at, n, 1.5, 0.45))       # a linen cushion
            if "top" in cu:
                pen.stroke(cu["top"], 0.05, 0.5, 0.95, 0.5, "#9a90a0", 0.7, 0.5)
            if "near" in sb:
                pen.dash(sb["near"][3], sb["near"][2], 0.05, 0.5)
                pen.spark(pen.on(sb["near"], 0.1, 1.0), 0.7)
    for x, d in ((-27, 24), (27, 24)):
        lion_leg(pen, F, x, d, seat - 6, 1, 1.0, False)
    return F


def chest(pen, F, wide, deep, h, wood="cedar", straps=3, lid=7.0, seed=0, gain=1.0, knob=True):
    """A wooden chest bound with gold: straps up the front, a band round the foot, a lid that overhangs."""
    w2, d2 = wide / 2, deep / 2
    body = wood_box(pen, F.outline(-w2, w2, -d2, d2), F.lift, F.lift + h - lid, WOODS[wood], gain, seed, 3, top=False)
    for name, q in body.items():
        n = face_normal(q)
        band(pen, q, 0, 1, 0.0, 0.13, n, gain, -0.05)
        if name == "near":
            for i in range(straps):
                u = (i + 0.5) / straps if straps > 1 else 0.5
                band(pen, q, u - 0.035, u + 0.035, 0.13, 1.0, n, gain, 0.02, hot=(0.3, 0.8) if i == 0 else None)
        else:
            band(pen, q, 0.42, 0.58, 0.13, 1.0, n, gain, 0.0)
    top = wood_box(pen, F.outline(-w2 - 2, w2 + 2, -d2 - 2, d2 + 2), F.lift + h - lid, F.lift + h, WOODS[wood], gain * 1.05, seed + 7, 2)
    for name, q in top.items():
        n = face_normal(q)
        if name == "top":
            for u0, u1 in ((0.0, 0.07), (0.93, 1.0)):
                band(pen, q, u0, u1, 0, 1, n, gain, 0.1)
            band(pen, q, 0, 1, 0.0, 0.12, n, gain, 0.12)
            pen.dash(q[0], q[1], 0.05, 0.5, HOT, 0.9, 0.8 * gain)
            if knob:
                kq = pen.on(q, 0.5, 0.5)
                x, y = P(*kq)
                k = k_of(kq[2])
                pen.base.ellipse(x, y - 2.4 * k, 3.0 * k, 2.6 * k, pen.gold(kq, (0, 0.6, 0.8), gain, 0.1))
                pen.spark((x - 0.8 * k, y - 3.4 * k), 0.6)
        else:
            band(pen, q, 0, 1, 0.0, 1.0, n, gain, 0.04)
    if "near" in body:                                                   # a row of blue-green faience tiles let into the front
        q = body["near"]
        n = face_normal(q)
        tile = pen.tone(STUFF["faience"], pen.on(q, 0.5, 0.8), n, gain * 1.6, 0.45)
        for i in range(straps):
            u0, u1 = i / straps + 0.06, (i + 1) / straps - 0.06
            m = (u0 + u1) / 2
            for a, b in ((u0, m - 0.045), (m + 0.045, u1)):
                if b - a > 0.02:
                    pen.patch(q, a, b, 0.70, 0.80, tile, 0.95)
    if knob and "near" in body:
        q = body["near"]
        kq = pen.on(q, 0.5, 0.86)
        x, y = P(*kq)
        k = k_of(kq[2])
        pen.base.ellipse(x, y, 2.4 * k, 2.4 * k, pen.gold(kq, (0, 0.2, 1), gain, 0.2))
        pen.base.line([(x, y), (x + 0.5 * k, y - 7 * k)], "#c8b890", 0.8, 0.9)      # the cord that ties the lid down
    return body, top


def bracelet_box(pen, F):
    """A small box hooped with gold, its lid off beside it, bracelets in rows inside."""
    f = gold_box(pen, F.outline(-15, 15, -10, 10), F.lift, F.lift + 11, 1.0, 0.04, 61, streaks=0)
    for name, q in f.items():
        if name != "top":
            for u in (0.25, 0.5, 0.75):
                pen.stroke(q, u, 0, u, 1, "#2a180e", 0.8, 0.8)
            pen.dash(q[3], q[2], 0.0, 0.7)
    if "top" in f:
        q = f["top"]
        pen.patch(q, 0.07, 0.93, 0.1, 0.9, "#1a1014")
        for i in range(6):                                               # silver bangles set with turquoise and carnelian, on two rods
            for v in (0.34, 0.68):
                p = pen.on(q, 0.14 + 0.72 * i / 5, v)
                x, y = P(*p)
                pen.base.ellipse(x, y, 1.9, 1.5, "#d8d4cc")
                pen.base.ellipse(x, y + 0.2, 0.9, 0.7, "#2a1c20")
                pen.fine.ellipse(x - 0.8, y - 0.7, 0.65, 0.65, "#40c8bc" if (i + int(v * 10)) % 2 else "#d04a3a")
    return f


def basins(pen):
    """A copper ewer standing in its basin, and a second basin beside it."""
    X, D = PLACE["basins"]
    cu = STUFF["copper"]
    cols = jar_colors(pen, X + 20, D + 6, 12, cu, 0.4, 1.3)
    x0, yb, k, side, sq = pen.lathe(X + 22, D + 9, [(7, 0), (13, 3), (16, 9), (16.5, 10)], cols)
    pen.base.ellipse(x0, yb - 10 * k, 13.5 * k, 13.5 * k * sq, mix(cols[0], "#1a1014", 0.4))
    pen.fine.line([(x0 - 15 * k, yb - 10 * k), (x0 - 6 * k, yb - 10 * k - 15 * k * sq * 0.9)], "#ffd8a8", 0.8, 0.8)
    cols = jar_colors(pen, X, D, 14, cu, 0.4, 1.3)
    x0, yb, k, side, sq = pen.lathe(X, D, [(9, 0), (16, 4), (20.5, 12), (21, 13.5)], cols)
    pen.base.ellipse(x0, yb - 13.5 * k, 18 * k, 18 * k * sq, mix(cols[0], "#1a1014", 0.5))
    ew = jar_colors(pen, X, D, 36, cu, 0.4, 1.4)
    ex, eb, k, side, sq = pen.lathe(X - 1, D - 2, turned([(5.5, 0), (9.5, 6), (10.5, 15), (7.5, 23), (4.2, 28), (5.6, 31), (5.6, 32)], 3), ew, y0=10)
    s = pen.base
    s.poly([(ex + side * 7 * k, eb - 21 * k), (ex + side * 17 * k, eb - 27 * k), (ex + side * 17.5 * k, eb - 25.2 * k), (ex + side * 8 * k, eb - 17.5 * k)], ew[2])      # the spout
    s.line([(ex + side * 7.5 * k, eb - 20.5 * k), (ex + side * 17 * k, eb - 26.6 * k)], "#ffe0b8", 0.8, 0.85)
    pen.fine.line([(x0 - 20 * k, yb - 13.5 * k + 0.5), (x0 + 20 * k, yb - 13.5 * k + 0.5)], "#f8b080", 0.9, 0.7)
    pen.spark((ex + side * 3.5 * k, eb - 17 * k), 0.7, "#fff0dc", "#ffc890")


def long_chest(pen):
    """Against the wall behind the bed: a long chest for the canopy's curtains, with smaller things stood on
    its lid: a pale box, a basket, folded linen, two jars."""
    cx, cd, turn = PLACE["long"]
    F = Frame(cx, cd, turn)
    body, top = chest(pen, F, 150.0, 44.0, 46.0, "cedar", 4, lid=7.0, seed=50, knob=False)
    F2 = Frame(*F.w(-46, 0, 0)[::2], turn - 7.0, lift=46.0)
    chest(pen, F2, 50.0, 30.0, 25.0, "pale", 2, lid=5.0, seed=52, knob=True)
    b = F.w(-48, 71, 0)
    basket(pen, b[0], b[2], r=11.0, h=15.0, y0=71.0, seed=5)
    linen_stack(pen, Frame(*F.w(8, 0, 2)[::2], turn + 12.0), -20, 20, -14, 14, 46.0, 15, folds=5, seed=6)
    j = F.w(46, 46, -4)
    alabaster(pen, j[0], j[2], [(r * 0.8, h * 0.8) for r, h in ALABASTER_TALL], y0=46.0, seed=7)
    j = F.w(62, 46, 6)
    alabaster(pen, j[0], j[2], [(r * 0.8, h * 0.8) for r, h in ALABASTER_CYL], y0=46.0, seed=8)
    g = F.w(30, 46, 10)
    gc = [pen.gold((g[0], 52, g[2]), (0.5, 0.3, 0.5), 1.0, lf) for lf in (-0.1, 0.05, 0.2, 0.4)]
    x0, yb, k, side, sq = pen.lathe(g[0], g[2], [(4.0, 0), (1.6, 2.5), (1.8, 7), (7.0, 14), (7.6, 15.5)], gc, y0=46.0)      # a gold cup
    pen.spark((x0 + side * 4 * k, yb - 13 * k), 0.7)


def treasure(pen):
    """Everything along the back wall, from the corner to the place that hums. Far things first."""
    j = PLACE["jars"]
    canopy_poles(pen)
    mats(pen)
    alabaster(pen, j[0][0], j[0][1], ALABASTER_TALL, seed=1)
    alabaster(pen, j[1][0], j[1][1], ALABASTER_CYL, seed=2)
    # the chests against the wall, right of lamp B
    cx, cd, turn = PLACE["chest"]
    F1 = Frame(cx, cd, turn)
    chest(pen, F1, 96.0, 46.0, 50.0, "cedar", 3, seed=40)
    c2x, c2d, c2t = PLACE["chest2"]
    F2 = Frame(c2x, c2d, c2t, lift=50.0)
    chest(pen, F2, 54.0, 32.0, 27.0, "pale", 2, lid=5.0, seed=44, knob=False)
    bracelet_box(pen, Frame(c2x - 9.0, c2d + 1.0, c2t - 6.0, lift=77.0))
    alabaster(pen, c2x + 19.0, c2d - 3.0, [(r * 0.55, h * 0.5) for r, h in ALABASTER_SHOULDER], y0=77.0, seed=5)
    long_chest(pen)
    drape(pen, [F1.w(22, 50.5, 25.5), F1.w(50.5, 50.5, 25.5), F1.w(51, 22, 26.5), F1.w(26, 15, 26.5)], 0.8, 4, seed=3)       # a dust sheet half pulled off
    pen.poly([F1.w(20, 50.6, 25.5), F1.w(50.5, 50.6, 25.5), F1.w(50.5, 50.6, 8), F1.w(27, 50.6, 4)], pen.tone(STUFF["linen"], F1.w(40, 50, 15), (0, 1, 0), 1.6, 0.45))
    bed(pen)
    alabaster(pen, j[2][0], j[2][1], ALABASTER_SHOULDER, seed=3)
    fa = jar_colors(pen, -392.0, 92.0, 20, STUFF["faience"], 0.45, 1.5, 0.5)
    fx, fy, fk, fside, fsq = pen.lathe(-392.0, 92.0, turned([(3.5, 0), (4.2, 1), (6.4, 8), (6.0, 14), (3.4, 17), (4.4, 19.5), (4.4, 20)], 3), fa)
    pen.fine.line([(fx + fside * 2.6 * fk, fy - 14 * fk), (fx + fside * 2.6 * fk, fy - 9 * fk)], "#d8fff4", 0.8, 0.85)
    carrying_chair(pen)
    armchair(pen)
    alabaster(pen, j[3][0], j[3][1], ALABASTER_TALL, seed=6)
    bk = PLACE["basket"]
    basket(pen, bk[0], bk[1], r=17.0, h=27.0, seed=8)
    basins(pen)


def treasure_blocks():
    """The same things as plain boxes, for the shadows they throw."""
    out = []
    x0, x1 = PLACE["poles"]
    out.append(Block([(x0 - 3, 56), (x1 + 4, 56), (x1 + 8, 2), (x0, 2)], 0, 225, "poles"))
    for X, D, h, r in PLACE["mats"]:
        out.append(Block(box_outline(X, D, 2 * r, 2 * r), 0, h, "mats"))
    for X, D in PLACE["jars"]:
        out.append(Block(box_outline(X, D, 17, 17), 0, 48, "jar"))
    cx, cd, turn = PLACE["bed"]
    F = Frame(cx, cd, turn)
    out.append(Block(F.outline(-86, 86, -39, 39), 24, 36, "bed"))
    out.append(Block(F.outline(83, 86, -39, 39), 0, 76, "bed"))
    out.append(Block(F.outline(-74, -30, -27, 20), 30, 56, "bed"))
    cx, cd, turn = PLACE["chair"]
    F = Frame(cx, cd, turn)
    out.append(Block(F.outline(-30, 32, -27, 27), 0, 40, "chair"))
    out.append(Block(F.outline(-31, -27, -24, 24), 0, 68, "chair"))
    out.append(Block(F.outline(-98, 98, 24, 30), 2, 9, "chair"))
    out.append(Block(F.outline(-98, 98, -30, -24), 2, 9, "chair"))
    cx, cd, turn = PLACE["arm"]
    F = Frame(cx, cd, turn)
    out.append(Block(F.outline(-33, 33, -30, 30), 26, 58, "arm"))
    out.append(Block(F.outline(-33, 33, -30, -26), 0, 90, "arm"))
    cx, cd, turn = PLACE["chest"]
    out.append(Block(Frame(cx, cd, turn).outline(-50, 50, -25, 25), 0, 50, "chest"))
    cx, cd, turn = PLACE["long"]
    out.append(Block(Frame(cx, cd, turn).outline(-76, 76, -23, 23), 0, 46, "chest"))
    out.append(Block(Frame(cx, cd, turn).outline(-72, -20, -16, 16), 46, 84, "chest"))
    out.append(Block(Frame(cx, cd, turn).outline(36, 70, -12, 12), 46, 88, "chest"))
    cx, cd, turn = PLACE["chest2"]
    out.append(Block(Frame(cx, cd, turn).outline(-27, 27, -16, 16), 50, 77, "chest"))
    X, D = PLACE["basket"]
    out.append(Block(box_outline(X, D, 32, 32), 0, 30, "basket"))
    X, D = PLACE["basins"]
    out.append(Block(box_outline(X + 8, D + 3, 56, 40), 0, 14, "basins"))
    out.append(Block(box_outline(X, D, 18, 18), 0, 40, "basins"))
    return out


# ================================================================ the goldsmith's bench
def bench(pen):
    """A low work bench: a thick plank top on two slab legs, grey with age, worn pale on top, dark underneath."""
    b = BENCH
    x0, x1, d0, d1, h = b["x0"], b["x1"], b["d0"], b["d1"], b["h"]
    for lx in (x0 + 8, x1 - 14):                                         # two slab legs
        o = [(lx, d1 - 3), (lx + 6, d1 - 3), (lx + 6, d0 + 3), (lx, d0 + 3)]
        pen.box(o, 0, h - 5, lambda at, n: pen.tone(WOODS["plank"], at, n, 0.5), top=False)
    under = [(x0 + 14, 5, d1 - 4), (x1 - 14, 5, d1 - 4), (x1 - 14, h - 5, d1 - 4), (x0 + 14, h - 5, d1 - 4)]
    pen.poly(under, "#1a1014", 0.9)                                      # it is dark under the bench
    o = [(x0, d1), (x1, d1), (x1, d0), (x0, d0)]
    f = pen.box(o, h - 5, h, lambda at, n: pen.tone(WOODS["plank"], at, n, 0.75), top=lambda at, n: pen.tone(WOODS["bench"], at, n, 1.0))
    top, near = f["top"], f["near"]
    for i in range(8):                                                   # the light of the lamp at its left end runs out along the top
        u0, u1 = i / 8, (i + 1) / 8
        at = pen.on(top, (u0 + u1) / 2, 0.5)
        pen.patch(top, u0, u1, 0, 1, pen.tone(WOODS["bench"], at, (0, 1, 0), 1.0, wrap=0.4))
    for v in (0.34, 0.68):                                               # three planks
        pen.stroke(top, 0.0, v, 1.0, v + 0.01, "#4a3a30", 0.8, 0.7)
    pen.stroke(near, 0, 1, 1, 1, "#eadab8", 0.9, 0.7, fine=True)         # the worn front edge catches the light
    pen.stroke(near, 0, 0, 1, 0, "#24161a", 1.0, 0.8)
    for u in (0.12, 0.31, 0.55, 0.83):                                   # knife cuts and burns
        pen.stroke(top, u, 0.2, u + 0.02, 0.5, "#4a342a", 0.7, 0.6)
    return f


MIRROR = dict(X=-181.0, D=321.0, lean=14.0)                              # where the goldsmith's mirror stands on the bench
BENCH_JAR = (-171.0, 309.0)


def bench_things(pen):
    """What lies on the bench, left to right: his lamp on its little stand, a casket half covered with gold
    leaf, the jar the mirror leans on, a dish of gold leaf, the blowpipe, a burnisher, hammers and the stone
    he beats on. (The mirror itself is a cut-out of its own.)"""
    b = BENCH
    top = b["h"]
    s, f = pen.base, pen.fine
    # ---- the lamp at the left end, on a turned stand
    lx, ld = b["x0"] + 6.0, 318.0
    cols = jar_colors(pen, lx, ld, top + 30, STUFF["pot"], 0.4, 0.8)
    pen.lathe(lx, ld, turned([(5.5, 0), (3.0, 2.5), (1.5, 8), (1.4, 26), (2.4, 34), (6.0, 40)], 3), cols, y0=top)
    flame_at = dish_lamp(pen, lx, top + 43.0, ld, r=6.5)
    # ---- a small casket: the left of it is gilded already, the right still bare wood
    F = Frame(-207.0, 314.0, -8.0, lift=top)
    wood_box(pen, F.outline(-1, 14, -8, 8), top, top + 14, WOODS["pale"], 1.25, 71, 2)
    g = gold_box(pen, F.outline(-14, 2, -8, 8), top, top + 14, 1.15, 0.05, 72, streaks=1)
    if "near" in g:
        q = g["near"]
        pen.poly([pen.on(q, 0.78, 0.0), pen.on(q, 1.16, 0.0), pen.on(q, 1.04, 0.55), pen.on(q, 1.2, 1.0), pen.on(q, 0.8, 1.0)], pen.gold(pen.on(q, 1, 0.5), (0, 0, 1), 1.2, 0.16))      # the ragged edge of the leaf
        pen.dash(q[3], q[2], 0.0, 0.8)
        pen.spark(pen.on(q, 0.2, 0.96), 0.8)
    if "top" in g:
        pen.dash(g["top"][0], g["top"][1], 0.1, 0.9, HOT, 0.8, 0.8)
    # ---- the jar the mirror is propped against
    jx, jd = BENCH_JAR
    pot(pen, jx, jd, [(r * 0.95, h * 0.98) for r, h in POT_JAR], "buff", y0=top, gain=1.15)
    # ---- a dish of gold leaf, crumpled and very bright
    dx, dd = -150.0, 322.0
    x, y = P(dx, top, dd)
    k = k_of(dd)
    sq = (row_of(dd) - G.vy) / G.F
    s.poly([(x - 9 * k, y - 2.6 * k), (x + 9 * k, y - 2.6 * k), (x + 5 * k, y + 0.5 * k), (x - 5 * k, y + 0.5 * k)], "#6a3a28")
    s.ellipse(x, y - 2.6 * k, 9 * k, 9 * k * sq, "#a8603c")
    s.ellipse(x, y - 2.8 * k, 7.4 * k, 7.4 * k * sq * 0.9, "#8a5016")
    f.poly([(x - 6 * k, y - 2.6 * k), (x - 3 * k, y - 5.2 * k), (x + 0.5 * k, y - 3.4 * k), (x + 4 * k, y - 5.6 * k), (x + 6.4 * k, y - 2.8 * k), (x + 2 * k, y - 1.4 * k), (x - 2.5 * k, y - 1.8 * k)], "#e8b23a")
    f.poly([(x - 3 * k, y - 5.2 * k), (x + 0.5 * k, y - 3.4 * k), (x - 2.2 * k, y - 2.8 * k)], HOT)
    f.poly([(x + 4 * k, y - 5.6 * k), (x + 6.4 * k, y - 2.8 * k), (x + 3 * k, y - 3.2 * k)], "#ffe98a")
    pen.spark((x - 1.8 * k, y - 4.2 * k), 0.9)
    # ---- the blowpipe: a long reed with a clay tip, lying along the front
    a, c = (-222.0, top + 1.2, 332.0), (-163.0, top + 1.2, 334.0)
    pen.line([a, c], "#3a2a22", 2.2, 0.5)
    pen.line([(a[0], a[1] + 0.8, a[2]), (c[0], c[1] + 0.8, c[2])], "#d6bc7c", 1.5)
    pen.line([(c[0] - 1, c[1] + 0.8, c[2]), (c[0] + 7, c[1] + 0.8, c[2])], "#8a3a26", 2.0)
    pen.line([(a[0] + 18, a[1] + 1.6, a[2]), (a[0] + 19, a[1] + 1.6, a[2])], "#7a6640", 1.6)
    # ---- a burnisher: a polished red pebble
    x, y = P(-190.0, top + 1.5, 329.0)
    s.ellipse(x, y, 3.6, 2.2, "#6e1f1c")
    f.ellipse(x - 1.0, y - 0.7, 1.2, 0.7, "#ffb8a0")
    # ---- the beating stone, a hammer lying on it, another beside it, and scraps of gold
    A = Frame(-136.0, 312.0, 6.0, lift=top)
    pen.box(A.outline(-8, 8, -7, 7), top, top + 9, lambda at, n: pen.tone("#8c8a88" if n[1] > 0.5 else "#5e5a60", at, n, 1.2, 0.4))
    pen.line([A.w(-7, 9.3, 5), A.w(7, 9.3, 5)], "#d8d4cc", 0.8, 0.7, fine=True)
    pen.line([A.w(-12, 10, 2), A.w(4, 10.4, -2)], "#7a5030", 1.5)          # a hammer: a wooden haft through a stone head
    pen.poly([A.w(3, 9.2, -5), A.w(8, 9.2, -5), A.w(8, 13.5, -5), A.w(3, 13.5, -5)], "#3a3a44")
    pen.line([A.w(3, 13.5, -5), A.w(8, 13.5, -5)], "#b8b8c4", 0.8, 0.9, fine=True)
    pen.line([(-158.0, top + 1.0, 330.0), (-144.0, top + 1.0, 333.0)], "#8a5c38", 1.5)
    pen.poly([(-146.0, top + 0.4, 331.0), (-141.0, top + 0.4, 331.0), (-141.0, top + 4.6, 331.0), (-146.0, top + 4.6, 331.0)], "#c07048")      # a copper-headed one
    pen.line([(-146.0, top + 4.6, 331.0), (-141.0, top + 4.6, 331.0)], "#ffd0a0", 0.8, 0.9, fine=True)
    rng = np.random.default_rng(12)
    for i in range(9):                                                   # scraps of leaf
        px, pd = -228.0 + rng.random() * 100.0, 300.0 + rng.random() * 34.0
        x, y = P(px, top + 0.5, pd)
        f.poly([(x - 1.4, y), (x, y - 1.0), (x + 1.5, y + 0.2), (x + 0.2, y + 0.9)], HOT if i % 3 else WHITE, 0.95)
    return flame_at


def bench_floor_things(pen):
    """On the floor at the ends of the bench: his water jug with a cup upside down on it, his dinner on a
    cloth, and a basket of charcoal for the brazier."""
    x0, yb, k, side, sq = pot(pen, -262.0, 327.0, [(r * 0.9, h * 0.9) for r, h in POT_JAR], "pot", gain=1.2)
    pen.base.poly([(x0 - 5.5 * k, yb - 33 * k), (x0 + 5.5 * k, yb - 33 * k), (x0 + 4 * k, yb - 39 * k), (x0 - 4 * k, yb - 39 * k)], pen.tone(STUFF["buff"], (-262, 36, 327), (0.5, 0.3, 0.7), 1.3))
    pen.fine.line([(x0 + side * 4 * k, yb - 26 * k), (x0 + side * 6.5 * k, yb - 18 * k)], "#f0b890", 0.8, 0.8)
    # his dinner, on a cloth on the floor beyond the jug: a round loaf and two onions
    F = Frame(-298.0, 338.0, -14.0)
    cloth = [F.w(-15, 0.4, 10), F.w(-2, 0.4, 12), F.w(14, 0.4, 9), F.w(16, 0.4, -8), F.w(2, 0.4, -11), F.w(-13, 0.4, -9)]
    pen.poly(cloth, pen.tone("#c9bda6", F.w(0, 0, 0), (0, 1, 0), 0.9, 0.4))
    pen.line([cloth[0], cloth[1], cloth[2]], "#6c6474", 0.8, 0.7)
    pen.line([F.w(-6, 0.5, -9), F.w(-3, 0.5, 9)], "#8c8496", 0.7, 0.5)
    k = k_of(338.0)
    lx, ly = P(*F.w(-5, 0.5, 1))
    pen.base.ellipse(lx, ly - 2.4 * k, 7.5 * k, 4.4 * k, pen.tone("#8a5a30", F.w(-5, 3, 1), (0.3, 0.2, 1), 1.2, 0.4))        # the loaf: a dark crust,
    pen.base.ellipse(lx - 0.6 * k, ly - 3.6 * k, 6.3 * k, 3.0 * k, pen.tone("#c89458", F.w(-5, 5, 1), (0, 1, 0.3), 1.5, 0.4))   # lighter on top,
    pen.base.line([(lx - 3.5 * k, ly - 4.4 * k), (lx + 2.5 * k, ly - 3.4 * k)], "#6a4424", 0.8, 0.8)                         # slashed before baking
    for dx in (7.0, 11.0):
        ox, oy = P(*F.w(dx, 1.6, 4 - dx * 0.5))
        pen.base.line([(ox + 1.0 * k, oy - 0.6 * k), (ox + 7.0 * k, oy - 3.6 * k)], "#527a40", 1.2, 0.95)
        pen.base.ellipse(ox, oy, 2.0 * k, 1.8 * k, "#d8d2c0")
        pen.fine.ellipse(ox - 0.5 * k, oy - 0.6 * k, 0.7 * k, 0.6 * k, "#fffaf0")
    X, D = -64.0, 332.0
    cols = jar_colors(pen, X, D, 16, STUFF["basket"], 0.5, 1.1)
    bx, by, k, side, sq = pen.lathe(X, D, [(9, 0), (10, 1), (13, 9), (13.5, 15)], cols)
    for hh in (4, 8, 12):
        pen.base.line([(bx - 12.5 * k, by - hh * k), (bx, by - hh * k + sq * 12 * k * 0.5), (bx + 12.5 * k, by - hh * k)], "#4a3220", 0.8, 0.6)
    top = by - 15 * k
    pen.base.ellipse(bx, top, 12.6 * k, 12.6 * k * sq, "#20161a")
    rng = np.random.default_rng(8)
    for i in range(9):                                                   # the charcoal heaped in it
        a, r = rng.random() * math.tau, rng.random() ** 0.6 * 10
        cx, cy = bx + math.cos(a) * r * k, top + math.sin(a) * r * k * sq - 1.5 * k
        pen.base.poly([(cx - 2.6 * k, cy + 1 * k), (cx - 1 * k, cy - 2.2 * k), (cx + 2.4 * k, cy - 1.2 * k), (cx + 2 * k, cy + 1.4 * k)], "#17121a" if i % 2 else "#2c2630")
    pen.fine.line([(bx - 6 * k, top - 3 * k), (bx - 3 * k, top - 4 * k)], "#7a7684", 0.8, 0.8)


def brazier(pen):
    """A pottery brazier of glowing charcoal, standing on the floor by the goldsmith's right hand."""
    X, D = BRAZIER
    cols = jar_colors(pen, X, D, 28, "#6a4034", 0.4, 0.9)
    x0, yb, k, side, sq = pen.lathe(X, D, turned([(10, 0), (8, 2), (5.5, 9), (7, 15), (13.5, 21), (15.5, 27), (15.5, 28)], 3), cols)
    s, f = pen.base, pen.fine
    top = yb - 28 * k
    s.ellipse(x0, top, 14.2 * k, 14.2 * k * sq, "#2a1210")
    rng = np.random.default_rng(3)
    for i in range(16):                                                  # the coals: black lumps, red where they touch, yellow at the heart
        a, r = rng.random() * math.tau, rng.random() ** 0.6 * 11.5
        cx, cy = x0 + math.cos(a) * r * k, top + math.sin(a) * r * k * sq
        hot = 1 - r / 13
        s.ellipse(cx, cy, 2.6 * k, 1.9 * k * max(sq, 0.5), mix("#3a0f0a", "#d83a12", hot * rng.random() ** 0.5))
        if rng.random() < 0.5 * hot + 0.2:
            f.ellipse(cx, cy, 1.3 * k, 0.9 * k, mix("#ff7a22", "#ffd060", rng.random() * hot), 0.95)
    f.line([(x0 - 14.4 * k, top + 0.8), (x0 - 6 * k, top + 14.4 * k * sq * 0.86)], "#e0562a", 0.9, 0.7)       # the rim glows from inside
    f.line([(x0 + 14.4 * k, top + 0.8), (x0 + 6 * k, top + 14.4 * k * sq * 0.86)], "#b03a1e", 0.9, 0.6)
    return (X, 30.0, D)


def mirror(pen):
    """The goldsmith's hand mirror: a polished copper disc, a little wider than it is tall, on a handle
    shaped like a papyrus stem. It leans back against the jar."""
    m = MIRROR
    top = BENCH["h"]
    k = k_of(m["D"])
    x, y = P(m["X"], top, m["D"])
    lean = math.radians(m["lean"])
    ux, uy = math.sin(lean) * 0.55, -math.cos(lean)                       # "up the mirror", in the picture: it leans back and a little right
    s, f = pen.base, pen.fine

    def at(a, h):                                                        # a across, h up the mirror, in cm
        return (x + a * k + ux * h * k, y + uy * h * k)
    # the handle: a papyrus stem that opens under the disc
    s.poly([at(-1.7, 0), at(1.7, 0), at(1.5, 9), at(5.2, 14.0), at(5.2, 17), at(-5.2, 17), at(-5.2, 14.0), at(-1.5, 9)], "#5a3418")
    s.poly([at(-0.2, 0), at(1.5, 0), at(1.3, 9), at(4.8, 13.7), at(0.7, 13.7), at(0.0, 9)], "#b07428")
    s.line([at(-1.6, 3), at(1.6, 3)], "#2a180e", 0.8, 0.8)
    s.line([at(-1.5, 7.5), at(1.5, 7.5)], "#e0a83a", 0.9, 0.9)
    # the disc
    cx, cy = at(0, 26.0)
    rx, ry = 14.0 * k, 12.2 * k
    s.ellipse(cx, cy, rx + 0.8, ry + 0.8, "#4a2014")
    s.ellipse(cx, cy, rx, ry, "#c8693a")
    s.ellipse(cx + rx * 0.14, cy + ry * 0.2, rx * 0.8, ry * 0.72, "#8f4226")                 # the dark room, mirrored
    s.ellipse(cx - rx * 0.16, cy - ry * 0.18, rx * 0.72, ry * 0.66, "#e89058")                # the lamp's side of it
    f.poly([(cx - rx * 0.86, cy - ry * 0.1), (cx - rx * 0.62, cy - ry * 0.62), (cx - rx * 0.12, cy - ry * 0.88), (cx + rx * 0.3, cy - ry * 0.84), (cx - rx * 0.1, cy - ry * 0.56), (cx - rx * 0.5, cy - ry * 0.3)], "#ffd2a0", 0.95)
    f.ellipse(cx - rx * 0.42, cy - ry * 0.52, rx * 0.2, ry * 0.15, "#fff8e8")
    f.line([(cx + rx * 0.5, cy + ry * 0.74), (cx + rx * 0.84, cy + ry * 0.3)], "#f0a070", 0.8, 0.8)
    return (cx, cy, rx, ry)


WINE_JAR = [(5, 0), (8, 6), (13, 30), (15.5, 52), (13.5, 66), (8.5, 75), (7, 79), (9.5, 81), (10.5, 85), (8, 88), (3.5, 94)]


def front_things(pen):
    """What stands right at the front edge, where people always pass behind: bottom left a great banded chest
    with jars on it and beside it; at the right edge the oil jar the nearest lamp is filled from. (The lamp
    stand itself is drawn by the caller.) They are close to us and the lamps are beyond them, so they are
    dark, with light along their edges."""
    # ---- left: the chest, turned a little, its lid toward us
    F = Frame(-474.0, 506.0, -16.0)
    body, top = chest(pen, F, 122.0, 62.0, 72.0, "cedar", 3, lid=9.0, seed=90, gain=1.6)
    lid = top.get("top")
    if lid:
        c = pen.on(lid, 0.26, 0.5)
        linen_stack(pen, Frame(c[0], c[2], -30.0), -17, 17, -12, 12, 72.0, 10, folds=3, gain=2.2, seed=9)
        c2 = pen.on(lid, 0.68, 0.6)
        alabaster(pen, c2[0], c2[2], [(r * 0.9, h * 0.9) for r, h in ALABASTER_CYL], y0=72.0, seed=15, gain=2.4)
        c3 = pen.on(lid, 0.88, 0.32)
        gc = [pen.gold((c3[0], 78, c3[2]), (0.5, 0.3, 0.5), 2.0, lf) for lf in (-0.1, 0.05, 0.2, 0.4)]
        pen.lathe(c3[0], c3[2], [(3.2, 0), (1.3, 2), (1.4, 6), (5.6, 13), (6.0, 14)], gc, y0=72.0)
        pen.dash(lid[1], lid[2], 0.0, 1.0, HOT, 1.0, 0.9)                 # the far edge of the lid has the bench lamp behind it
        pen.dash(lid[3], lid[2], 0.3, 1.0, HOT, 1.0, 0.8)
    # a tall wine jar with a mud stopper, a squat oil jar, a small jar of alabaster: lower and lower to the right
    x0, yb, k, side, sq = pot(pen, -388.0, 520.0, WINE_JAR, "pot", gain=1.8, rim=False)
    pen.fine.line([(x0 + 2.0, yb - 80 * k), (x0 + 12.5 * k, yb - 62 * k), (x0 + 14.5 * k, yb - 48 * k)], "#f0a868", 0.9, 0.85)      # light down its shoulder
    pen.base.line([(x0 - 9 * k, yb - 82.5 * k), (x0 + 9 * k, yb - 82.5 * k)], "#2a1810", 1.0, 0.8)
    pot(pen, -340.0, 540.0, OIL_JAR, "#9a5038", gain=1.8)
    x, y = P(-340.0, 51.0, 540.0)
    pen.fine.line([(x - 6, y + 4), (x + 4, y - 0.5), (x + 9.5, y + 2)], "#f0a868", 0.9, 0.85)
    alabaster(pen, -292.0, 556.0, ALABASTER_SHOULDER, seed=14, gain=2.4)
    # ---- right: the oil jar lamp E is filled from, a dipper standing in it
    pot(pen, 296.0, 553.0, OIL_JAR, "#8a4a34", gain=1.15)
    x, y = P(296.0, 51.0, 553.0)
    pen.fine.line([(x - 9, y + 1.5), (x - 2, y - 1), (x + 9, y + 1.5)], "#f0a868", 0.9, 0.85)
    pen.base.line([(x + 3, y - 1), (x + 12, y - 14)], "#7a5030", 1.6)
    pen.fine.line([(x + 3.6, y - 1), (x + 12.6, y - 14)], "#d8a060", 0.7, 0.8)


# ================================================================ what the masons left by the sarcophagus
def rope_coil(pen, X, D, r=17.0, turns=4, y0=0.0, gain=1.0):
    """A coil of palm-fibre rope lying flat."""
    x, y = P(X, y0, D)
    k = k_of(D)
    sq = (row_of(D) - G.vy) / G.F
    cols = [pen.tone(c, (X, y0 + 3, D), (0, 0.8, 0.6), gain) for c in ("#5a4630", "#b0925e", "#e2c890")]
    s = pen.base
    for i in range(turns):
        rr = r * (1 - i * 0.17)
        yy = y - i * 1.5 * k
        s.ellipse(x, yy, rr * k, rr * k * sq, cols[0])
        s.ellipse(x, yy - 0.8 * k, rr * k * 0.96, rr * k * sq * 0.96, cols[1])
        s.ellipse(x, yy - 0.8 * k, rr * k * 0.72, rr * k * sq * 0.72, cols[0])
    s.ellipse(x, y - turns * 1.5 * k, r * 0.3 * k, r * 0.3 * k * sq, "#1c1016")
    pen.fine.line([(x - r * k * 0.8, y - 3.2 * k), (x - r * k * 0.2, y - 3.2 * k - r * k * sq * 0.7)], cols[2], 0.8, 0.7)
    s.line([(x + r * k * 0.9, y), (x + r * k * 1.5, y + 2.5), (x + r * k * 2.0, y + 1.2)], cols[1], 1.6)          # the loose end


def log(pen, a, b, r, wood="#8a6a4a", gain=1.0, end=True):
    """A short log or roller lying on the floor from a to b."""
    mid = ((a[0] + b[0]) / 2, r, (a[2] + b[2]) / 2)
    cols = (pen.tone(_c(wood) * 0.4, mid, (0, 0.2, 1), gain), pen.tone(wood, mid, (0, 0.6, 0.8), gain), pen.tone(mix(wood, "#fff0d0", 0.4), mid, (0, 1, 0.2), gain * 1.2))
    pen.rod(a, b, r, cols, lit=(0.2, -1.0))
    if end:
        e = b if P(*b)[1] > P(*a)[1] else a
        x, y = P(*e)
        k = k_of(e[2])
        pen.base.ellipse(x, y, r * k * 0.75, r * k, cols[1])
        pen.base.ellipse(x, y, r * k * 0.4, r * k * 0.55, cols[0])


def masons_things(pen, sarc):
    """Rollers, a lever and a coil of rope by the right-hand end of the sarcophagus; a mallet left on its rim."""
    X1, D1, D0, Hh = sarc["x1"], sarc["d1"], sarc["d0"], sarc["h"]
    log(pen, (X1 + 14, 6, D1 - 62), (X1 + 30, 6, D1 + 8), 6.0, "#8a6a4a")
    log(pen, (X1 + 34, 6, D1 - 50), (X1 + 56, 6, D1 + 18), 6.0, "#7a5c40")
    # a lever leaning against the end of the box
    a, b = (X1 + 44, 0, D1 + 46), (X1 + 2, Hh + 2, D1 - 30)
    cols = tuple(pen.tone(c, (X1 + 20, 50, D1), (0.6, 0.2, 0.7)) for c in ("#3a2a20", "#8a684a", "#d0a878"))
    pen.rod(a, b, 2.6, cols)
    rope_coil(pen, X1 + 26, D1 + 52, 16.0, 4)
    # a rope left hanging over the near rim, its end frayed
    X0 = sarc["x0"]
    rx = X0 + 84.0
    path = [(rx + 6, Hh + 0.6, D1 - 15), (rx + 3, Hh + 1.2, D1 - 7), (rx, Hh + 0.8, D1 + 0.4), (rx - 1, Hh - 14, D1 + 0.6), (rx + 1.5, Hh - 30, D1 + 0.6), (rx - 0.5, Hh - 44, D1 + 0.6)]
    pen.line([(a - 2.2, b - 1.0, c) for a, b, c in path[2:]], "#150c10", 1.6, 0.45)
    pen.line(path, pen.tone("#7a6040", path[3], (0.3, 0.2, 1), 1.5), 2.0)
    pen.line([(a + 0.5, b, c) for a, b, c in path], pen.tone("#d8bc88", path[3], (0.3, 0.2, 1), 1.6), 0.9)
    for dx in (-2.2, 0.0, 2.0):
        pen.line([path[-1], (path[-1][0] + dx, path[-1][1] - 5, path[-1][2])], pen.tone("#c8ac78", path[-1], (0.3, 0.2, 1), 1.5), 0.7, 0.9)
    # the mallet on the near rim
    m0, m1 = (X1 - 62, Hh + 3, D1 - 6), (X1 - 40, Hh + 3, D1 - 9)
    pen.line([m0, m1], pen.tone("#8a684a", m0, (0, 1, 0), 1.6), 1.8)
    pen.poly([(X1 - 44, Hh, D1 - 4), (X1 - 34, Hh, D1 - 4), (X1 - 34, Hh + 8, D1 - 4), (X1 - 44, Hh + 8, D1 - 4)], pen.tone("#6a5040", m1, (0, 0.3, 1), 1.5))
    pen.poly([(X1 - 44, Hh + 8, D1 - 4), (X1 - 34, Hh + 8, D1 - 4), (X1 - 34, Hh + 8, D1 - 13), (X1 - 44, Hh + 8, D1 - 13)], pen.tone("#a08468", m1, (0, 1, 0), 1.8))


def lid_ropes(pen, lid, section):
    """The ropes the lid was lowered by are still round it, and it stands on two billets of wood."""
    bt, ft, fb, bb, a = section
    x0, x1 = lid["x0"], lid["x1"]
    for u in (0.24, 0.76):
        X = lerp(x0, x1, u)
        top, bot = (X, ft[1], ft[0]), (X, fb[1], fb[0])
        back = (X, bt[1], bt[0])
        for j, c in enumerate(("#5a4630", "#c0a270")):
            o = j * 0.9
            pen.line([(X + o, bot[1], bot[2]), (X + o, top[1], top[2]), (X + o, back[1], back[2])], pen.tone(c, top, (0, 0.5, 0.8), 1.3), 1.5 - j * 0.7)
    for u in (0.1, 0.9):
        X = lerp(x0, x1, u)
        F = Frame(X, fb[0] + 2, 0)
        wood_box(pen, F.outline(-9, 9, -12, 8), 0, 7, "#7a5c40", 1.0, 3, 1)


def carrying_poles(pen):
    """By the doorway, against the left wall: the two poles the chests were slung from, and the sling."""
    wood = ("#2a1c18", "#6a4c36", "#a88460")
    for i, (bx, bd, tx, ty, td) in enumerate(((-486.0, 338.0, -521.0, 208.0, 331.0), (-478.0, 352.0, -529.0, 196.0, 352.0))):
        cols = tuple(pen.tone(c, (bx, 80, bd), (0.8, 0.1, 0.5), 1.0) for c in wood)
        pen.rod((bx, 0, bd), (tx, ty, td), 2.6, cols, lit=(1.0, -0.2))
    a, b = P(-496.0, 86.0, 337.0), P(-492.0, 68.0, 351.0)                  # a rope sling looped over both, hanging slack
    rope = pen.tone(STUFF["rope"], (-490, 60, 345), (0.8, 0.2, 0.5), 1.0)
    pen.base.line(curve([a, (a[0] + 6, a[1] + 34), (a[0] + 15, a[1] + 52), (b[0] + 12, b[1] + 40), b], 6), rope, 1.3)
    pen.base.line(curve([(a[0] + 1, a[1] - 2), (a[0] + 4, a[1] + 3), (a[0] - 2, a[1] + 6)], 4), rope * 0.7, 1.6)


def stand_blocks(lamps):
    """Lamp stands throw thin shadows too."""
    out = []
    for l in lamps:
        out.append(Block(box_outline(l.X, l.D, 4, 4), 0, l.Y - 20, "stand"))
        out.append(Block(box_outline(l.X, l.D, 15, 15), l.Y - 20, l.Y - 6, "stand"))
    return out

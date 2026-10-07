"""The burial chamber's own tools: where things are in the room, how the lamps light it, the shadows
they throw, and squared stone laid in courses. Used by egypt_chamber.py and egypt_chamber_things.py.

THE ROOM IS MEASURED IN CENTIMETRES:  X across (0 is under the vanishing point, picture x 450),
Y up from the floor, D out from the back wall toward us (0 at the wall, about 540 at the bottom edge).

Two ways of seeing are used, as a background painter of the 1990s would:
  * the floor and everything standing on it are drawn through persp.Camera(-200, 585), the game's own
    depth numbers, with a long lens (so a 175 cm person, a 75 cm table and a 105 cm sarcophagus are all
    the right size beside the people the game draws, wherever they stand);
  * that camera is 8.6 m up, higher than the ceiling, so the side walls and the ceiling beams cannot be
    seen through it at all. They are drawn as a stage set is: to a vanishing point of their own inside
    the picture (450, 150). The back wall is the same in both.
"""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import *
from persp import Camera

W, H = 800, 600
SHAPE = (H, W)
HZ, FULL = -200, 585                    # the game's depth numbers for this room
VX = 450.0                              # the vanishing point: a little right of the middle
FOC = 1500.0                            # a long lens: 5.4 m of floor between the back wall and the bottom edge
WALL = 400.0                            # the row where the back wall meets the floor
TOP = 50.0                              # the row where it meets the ceiling
LEFT, RIGHT = 150.0, 750.0              # the two back corners
HR = 150.0                              # the row the side walls and ceiling beams run to

G = Camera(HZ, FULL, vanish_x=VX, focal=FOC)
ZB = G.depth_at(WALL)                   # the camera's z of the back wall
KB = G.scale(ZB)                        # pixels per centimetre on the back wall (0.699)
DCAM = ZB + G.Z0                        # how far the lens is from the back wall
XL, XR = (VX - LEFT) / KB, (RIGHT - VX) / KB          # the corners, in cm either side of the middle (429)
HC = (WALL - TOP) / KB                  # the height of the room (501 cm)
COURSES = np.array([0.0, 112.0, 209.0, 306.0, 403.0, HC])      # five courses: the lowest is the height of the doorway
FSIDE = 440.0                           # the side walls are seen as if through a much wider lens (a stage flat)
SPLAY = math.radians(22)                # and stand a little open, for lighting them

X_PIX, Y_PIX = grid(SHAPE)


# ---------------------------------------------------------------- places
def P(X, Y, D):
    """Room centimetres -> picture pixels."""
    return G.pt(X, Y, ZB - D)


def k_of(D):
    """Pixels per centimetre, D cm out from the back wall."""
    return G.F / (DCAM - D)


def row_of(D):
    """The picture row of the floor D cm out from the back wall."""
    return G.vy + G.eye * G.F / (DCAM - D)


def floor_at(px, py):
    """The place on the floor under a picture point -> (X, D). (For measuring: where to stand a thing.)"""
    k = (py - G.vy) / G.eye
    return (px - VX) / k, DCAM - G.F / k


def hit(Q, n):
    """Where the line of sight through every pixel meets a flat surface through Q with normal n (room cm).
    -> X, Y, D pictures."""
    cx, cy, cd = 0.0, G.eye, DCAM
    rx, ry, rd = (X_PIX - VX), -(Y_PIX - G.vy), -G.F
    den = n[0] * rx + n[1] * ry + n[2] * rd
    den = np.where(np.abs(den) < 1e-6, 1e-6, den)
    t = (n[0] * (Q[0] - cx) + n[1] * (Q[1] - cy) + n[2] * (Q[2] - cd)) / den
    return (cx + t * rx).astype(F32), (cy + t * ry).astype(F32), (cd + t * rd).astype(F32)


_k = np.maximum(Y_PIX - G.vy, 1.0) / G.eye
FLOOR_K = _k.astype(F32)                                   # pixels per cm across, at each pixel of floor
FLOOR_X = ((X_PIX - VX) / _k).astype(F32)
FLOOR_D = (DCAM - G.F / _k).astype(F32)
FLOOR_ROWS = (_k * _k * G.eye / G.F).astype(F32)           # picture rows per cm of depth, at each pixel of floor
WALL_X = ((X_PIX - VX) / KB).astype(F32)
WALL_Y = ((WALL - Y_PIX) / KB).astype(F32)


def _side(left):
    """A side wall, pixel by pixel: -> (u: cm along it from the back corner, v: cm up it, its floor row
    and top row at each column, mask)."""
    edge = LEFT if left else RIGHT
    out = (edge - X_PIX) if left else (X_PIX - edge)                     # pixels outward from the corner
    span = (VX - LEFT) if left else (RIGHT - VX)
    foot = WALL + out * (WALL - HR) / span
    head = TOP + out * (TOP - HR) / span
    v = (foot - Y_PIX) / np.maximum(foot - head, 1.0) * HC
    ks = (span + out) / (XL if left else XR)                              # the wall's own scale at this column
    u = FSIDE / KB - FSIDE / np.maximum(ks, 1e-3)
    m = np.clip(out + 0.5, 0, 1) * np.clip(foot - Y_PIX + 0.5, 0, 1) * np.clip(Y_PIX - head + 0.5, 0, 1)
    return u.astype(F32), v.astype(F32), foot.astype(F32), head.astype(F32), m.astype(F32)


LW_U, LW_V, LW_FOOT, LW_HEAD, LW_MASK = _side(True)
RW_U, RW_V, RW_FOOT, RW_HEAD, RW_MASK = _side(False)
LW_KV = ((LW_FOOT - LW_HEAD) / HC).astype(F32)                               # pixels per cm up the left wall
LW_KU = (XL * ((VX - LEFT + (LEFT - X_PIX)) / XL) ** 2 / FSIDE).astype(F32)   # pixels per cm along it
RW_KV = ((RW_FOOT - RW_HEAD) / HC).astype(F32)
RW_KU = (XR * ((RIGHT - VX + (X_PIX - RIGHT)) / XR) ** 2 / FSIDE).astype(F32)
_inside = np.clip(X_PIX - LEFT + 0.5, 0, 1) * np.clip(RIGHT - X_PIX + 0.5, 0, 1)
BW_MASK = (_inside * np.clip(Y_PIX - TOP + 0.5, 0, 1) * np.clip(WALL - Y_PIX + 0.5, 0, 1)).astype(F32)
_floor_line = np.where(X_PIX < LEFT, LW_FOOT, np.where(X_PIX > RIGHT, RW_FOOT, WALL))
_top_line = np.where(X_PIX < LEFT, LW_HEAD, np.where(X_PIX > RIGHT, RW_HEAD, TOP))
FLOOR_LINE, TOP_LINE = _floor_line.astype(F32), _top_line.astype(F32)      # the row where floor meets wall, and wall meets ceiling, at each column
FLOOR_MASK = np.clip(Y_PIX - _floor_line + 0.5, 0, 1).astype(F32)
CEIL_MASK = np.clip(_top_line - Y_PIX + 0.5, 0, 1).astype(F32)
EYE_R = (WALL - HR) / KB                                                  # how high the stage-set's eye is (358 cm)
_kc = np.maximum(HR - Y_PIX, 1.0) / (HC - EYE_R)
CEIL_K = _kc.astype(F32)
CEIL_X = ((X_PIX - VX) / _kc).astype(F32)
CEIL_D = (FOC / KB - FOC / _kc).astype(F32)


def side_pt(left, u, v):
    """A place on a side wall (u cm from the back corner, v cm up) -> picture pixels."""
    ks = FSIDE / (FSIDE / KB - u)
    span = (VX - LEFT) if left else (RIGHT - VX)
    out = ks * (XL if left else XR) - span
    foot = WALL + out * (WALL - HR) / span
    head = TOP + out * (TOP - HR) / span
    return ((LEFT - out) if left else (RIGHT + out), foot - (foot - head) * v / HC)


def ceil_pt(X, D):
    """A place on the ceiling -> picture pixels (the stage-set's eye)."""
    k = FOC / (FOC / KB - D)
    return (VX + X * k, HR - (HC - EYE_R) * k)


# ---------------------------------------------------------------- lamplight
class Lamp:
    """One flame: where it is in the room (cm), how strong it is, and how far its pool of light reaches
    (the distance, in cm, at which a surface facing it gets half the light)."""

    def __init__(self, name, X, Y, D, power=1.0, reach=110.0):
        self.name, self.X, self.Y, self.D, self.power, self.reach = name, X, Y, D, power, reach

    @property
    def at(self):
        """The flame's place in the picture."""
        return P(self.X, self.Y, self.D)


WEAK, STRONG = np.array([0.96, 0.53, 0.42], dtype=F32), np.array([1.0, 0.84, 0.59], dtype=F32)


def flame_color(e):
    """Lamplight is yellow where it is strong and redder where it is weak: the way a painter mixes it,
    so that every pool of light has a hot heart and a red edge. `e` is a number or a picture."""
    t = step(0.04, 1.25, np.asarray(e, dtype=F32))
    return WEAK + (STRONG - WEAK) * t[..., None]


def lamplight(lamp, X, Y, D, n, wrap=0.22):
    """How much of one lamp's light falls on a surface at (X, Y, D) that faces along n. Works on numbers or
    whole pictures. Lamplight is soft: it wraps a little round a form. It is made to fall away faster than
    real light does (with the cube of distance beyond `reach`), so that each lamp keeps a pool of its own."""
    dx, dy, dd = lamp.X - X, lamp.Y - Y, lamp.D - D
    d2 = dx * dx + dy * dy + dd * dd
    dist = np.sqrt(d2) + 1e-3
    cos = (dx * n[0] + dy * n[1] + dd * n[2]) / dist
    cos = np.clip(cos * (1 - wrap) + wrap, 0, 1)
    return lamp.power * cos / (1.0 + (d2 / (lamp.reach * lamp.reach)) ** 1.5)


def hull(points):
    """The outline that a string pulled tight round a set of points makes."""
    pts = sorted(set((round(float(a), 2), round(float(b), 2)) for a, b in points))
    if len(pts) < 3:
        return pts

    def turn(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and turn(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and turn(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


class Block:
    """Something solid that throws a shadow: an outline on the floor (X, D points) between two heights."""

    def __init__(self, outline, y0, y1, who=""):
        self.outline, self.y0, self.y1, self.who = [(float(a), float(b)) for a, b in outline], float(y0), float(y1), who


def box_outline(cx, cd, wide, deep, turn=0.0):
    """The four corners of a box on the floor, centred at (cx, cd), `wide` across and `deep` front to back,
    turned `turn` degrees. Order: near-left, near-right, far-right, far-left."""
    c, s = math.cos(math.radians(turn)), math.sin(math.radians(turn))
    out = []
    for a, b in ((-0.5, 0.5), (0.5, 0.5), (0.5, -0.5), (-0.5, -0.5)):
        lx, ld = a * wide, b * deep
        out.append((cx + lx * c - ld * s, cd + lx * s + ld * c))
    return out


def _raster(polys, ss=2):
    im = Image.new("L", (W * ss, H * ss), 0)
    d = ImageDraw.Draw(im)
    for pts in polys:
        if len(pts) >= 3:
            d.polygon([(float(a) * ss, float(b) * ss) for a, b in pts], fill=255)
    return np.asarray(im.resize((W, H), Image.BOX), dtype=F32) / 255


raster = _raster


def floor_shadows(lamp, blocks, skip=()):
    """The shadows one lamp throws on the floor: each block's outline pushed away from the flame until it
    reaches the ground. -> a mask (hard: soften it afterwards)."""
    polys = []
    for b in blocks:
        if b.who in skip:
            continue
        pts = []
        for y in (b.y0, b.y1):
            if y <= 0.01:
                pts += b.outline
                continue
            t = lamp.Y / max(lamp.Y - y, lamp.Y / 9.0)                      # a thing taller than the flame throws a shadow without end
            pts += [(lamp.X + (a - lamp.X) * t, lamp.D + (c - lamp.D) * t) for a, c in b.outline]
        pts = [(a, min(c, DCAM - 500.0)) for a, c in pts]
        polys.append([P(a, 0, c) for a, c in hull(pts)])
    return _raster(polys)


def wall_shadows(lamp, blocks, skip=()):
    """The shadows one lamp throws on the back wall."""
    polys = []
    for b in blocks:
        if b.who in skip:
            continue
        pts = []
        for y in (b.y0, b.y1):
            for a, c in b.outline:
                if c >= lamp.D - 2.0:                                        # this corner is nearer us than the flame is
                    continue
                t = min(lamp.D / (lamp.D - c), 30.0)
                pts.append((lamp.X + (a - lamp.X) * t, max(lamp.Y + (y - lamp.Y) * t, -5.0)))
        if len(pts) >= 3:
            polys.append([P(a, c, 0) for a, c in hull(pts)])
    return _raster(polys)


def soften(mask, near=1.6, far=8.0, lamp=None, plane="floor"):
    """Shadows are crisp close to the thing that throws them and loose far away."""
    a, b = blur(mask, near), blur(mask, far)
    if lamp is None:
        return (a + b) / 2
    if plane == "floor":
        dist = np.hypot(FLOOR_X - lamp.X, FLOOR_D - lamp.D)
    else:
        dist = np.hypot(WALL_X - lamp.X, WALL_Y - lamp.Y)
    t = np.clip(dist / 420.0, 0, 1)
    return lerp(a, b, t).astype(F32)


# ---------------------------------------------------------------- squared stone
def ashlar(a, b, edges, seed, lengths=(170.0, 330.0), joints=None, start=-2400.0, stop=2400.0):
    """Stone laid in courses. `a` runs along a course and `b` across the courses (cm pictures); `edges` are
    where one course ends and the next begins. `joints` may give the end joints of a course by hand
    ({course number: [a, a, ...]}). -> (one random number per block, -1 to 1; a second one; cm to the
    nearest end joint; cm to the nearest bed joint; which course)."""
    rng = np.random.default_rng(seed)
    edges = np.asarray(edges, dtype=F32)
    course = np.clip(np.searchsorted(edges, b) - 1, 0, len(edges) - 2)
    db = np.minimum(np.abs(b - edges[course]), np.abs(edges[course + 1] - b))
    tone = np.zeros(a.shape, dtype=F32)
    tone2 = np.zeros(a.shape, dtype=F32)
    da = np.full(a.shape, 1e3, dtype=F32)
    for c in range(len(edges) - 1):
        if joints and c in joints:
            js = [start] + sorted(joints[c]) + [stop]
        else:
            js = [start + rng.random() * lengths[1]]
            while js[-1] < stop:
                js.append(js[-1] + rng.uniform(*lengths))
        js = np.asarray(js, dtype=F32)
        m = course == c
        idx = np.clip(np.searchsorted(js, a[m]), 1, len(js) - 1)
        t1 = rng.uniform(-1, 1, len(js) + 1).astype(F32)
        t2 = rng.uniform(-1, 1, len(js) + 1).astype(F32)
        tone[m] = t1[idx]
        tone2[m] = t2[idx]
        da[m] = np.minimum(np.abs(a[m] - js[idx - 1]), np.abs(js[idx] - a[m]))
    return tone, tone2, da, db.astype(F32), course


def speckle(shape, seed, cell=1.7):
    """Granite's grain: -> (dark flecks, light flecks) as two masks."""
    n = noise(shape, cell, seed, 2, gain=0.6)
    big = noise(shape, cell * 3.2, seed + 1, 2)
    dark = step(0.70, 0.86, n) * (0.55 + 0.45 * big)
    light = step(0.72, 0.9, 1 - n) * (0.5 + 0.5 * (1 - big))
    return dark.astype(F32), light.astype(F32)


# ---------------------------------------------------------------- a sheet that takes glazes
class Paper(Sheet):
    """A clear sheet like brush.Sheet, but thin (half-transparent) paint really lies OVER what is already on
    it. (On the library's Sheet a half-transparent stroke replaces what is under it and leaves the sheet
    half clear there: a hole, once the sheet is cut out with hard edges.)"""

    def _glaze(self, box, draw):
        w, h = self.im.size
        x0, y0, x1, y1 = int(max(0, math.floor(box[0]))), int(max(0, math.floor(box[1]))), int(min(w, math.ceil(box[2]) + 1)), int(min(h, math.ceil(box[3]) + 1))
        if x1 <= x0 or y1 <= y0:
            return self
        tmp = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        draw(ImageDraw.Draw(tmp), x0, y0)
        self.im.alpha_composite(tmp, (x0, y0))
        self.d = ImageDraw.Draw(self.im)
        return self

    def line(self, points, color, width=1.0, alpha=1.0, round_ends=True):
        if alpha >= 0.995:
            return super().line(points, color, width, 1.0, round_ends)
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        wd = max(1, int(round(width * s)))
        fill = self._fill(color, alpha)
        pad = wd + 2

        def draw(d, ox, oy):
            q = [(a - ox, b - oy) for a, b in pts]
            d.line(q, fill=fill, width=wd, joint="curve")
            if round_ends and wd > 2:
                r = wd / 2
                for a, b in (q[0], q[-1]):
                    d.ellipse([a - r, b - r, a + r, b + r], fill=fill)
        return self._glaze((min(p[0] for p in pts) - pad, min(p[1] for p in pts) - pad, max(p[0] for p in pts) + pad, max(p[1] for p in pts) + pad), draw)

    def poly(self, points, color, alpha=1.0):
        if alpha >= 0.995:
            return super().poly(points, color, 1.0)
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        fill = self._fill(color, alpha)
        return self._glaze((min(p[0] for p in pts) - 1, min(p[1] for p in pts) - 1, max(p[0] for p in pts) + 1, max(p[1] for p in pts) + 1),
                           lambda d, ox, oy: d.polygon([(a - ox, b - oy) for a, b in pts], fill=fill))

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0):
        if alpha >= 0.995:
            return super().ellipse(cx, cy, rx, ry, color, 1.0)
        s = self.ss
        fill = self._fill(color, alpha)
        box = ((cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s)
        return self._glaze((box[0] - 1, box[1] - 1, box[2] + 1, box[3] + 1), lambda d, ox, oy: d.ellipse([box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy], fill=fill))


# ---------------------------------------------------------------- the brush, for a built room
def brushwork(ref, flow, sizes=(13, 7, 3), seed=1, density=1.5, jitter=0.06, keep=0.2, edge=0.03, wander=0.28):
    """Repaint a picture with brush strokes, as brush.strokes does, but the strokes lie the way the SURFACE
    runs (`flow`: an angle for every pixel, in radians: along the courses of a wall, along the beams of a
    ceiling), and only turn to follow an edge where the edge is a hard one. In a room lit by lamps the
    library's brush would otherwise sweep round every pool of light in rings."""
    h, w, _ = ref.shape
    rng = np.random.default_rng(seed)
    ss = 2
    under = np.clip(blur(ref, sizes[0] * 0.45), 0, 1)
    canvas = Image.fromarray((under * 255).astype(np.uint8)).resize((w * ss, h * ss), Image.BICUBIC)
    draw = ImageDraw.Draw(canvas)
    lum = ref @ np.array([0.3, 0.55, 0.15], dtype=F32)
    for r in sizes:
        src = np.clip(blur(ref, r * 0.3), 0, 1)
        gy, gx = np.gradient(blur(lum, max(1.0, r * 0.3)))
        along = np.arctan2(gy, gx) + math.pi / 2
        strong = np.hypot(gx, gy)
        n = int(w * h / (r * r) * density)
        xs = rng.integers(0, w, n)
        ys = rng.integers(0, h, n)
        if r != sizes[0]:
            now = np.asarray(canvas.resize((w, h), Image.BOX), dtype=F32) / 255
            wrong = np.abs(now - src).sum(axis=2)
            want = wrong[ys, xs] > (0.05 if r > sizes[-1] else 0.035)
            xs, ys = xs[want], ys[want]
        for x, y in zip(xs.tolist(), ys.tolist()):
            a = along[y, x] if strong[y, x] > edge else flow[y, x] + rng.normal(0, wander)
            length = r * (1.3 + 2.4 * rng.random())
            dx, dy = math.cos(a) * length / 2, math.sin(a) * length / 2
            c = src[y, x] * (1 + rng.normal(0, jitter)) + rng.normal(0, jitter * 0.4, 3)
            fill = tuple(int(v) for v in np.clip(c * 255, 0, 255))
            wd = max(1, int(r * ss * (0.7 + 0.5 * rng.random())))
            x0, y0, x1, y1 = (x - dx) * ss, (y - dy) * ss, (x + dx) * ss, (y + dy) * ss
            draw.line([x0, y0, x1, y1], fill=fill, width=wd)
            e = wd / 2
            draw.ellipse([x0 - e, y0 - e, x0 + e, y0 + e], fill=fill)
            draw.ellipse([x1 - e, y1 - e, x1 + e, y1 + e], fill=fill)
    out = np.asarray(canvas.resize((w, h), Image.BOX), dtype=F32) / 255
    return lerp(out, ref, keep) if keep else out


def room_flow():
    """The way each surface of the room runs, as an angle for the brush: level along the back wall and the
    floor, toward the stage-set's vanishing point along the side walls and the ceiling beams."""
    to_vp = np.arctan2(HR - Y_PIX, VX - X_PIX)
    flow = np.zeros(SHAPE, dtype=F32)
    flow = np.where((LW_MASK > 0.5) | (RW_MASK > 0.5) | (CEIL_MASK > 0.5), to_vp, flow)
    return flow.astype(F32)


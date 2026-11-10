"""PAINT-23 (round twenty-three, RECOMPOSE): the cedar path's camera, its place measured, and its small tools (shared by
edo_cedars.py, edo_cedars_plan.py, edo_cedars_layout.py and the checks). Round twenty's picture (PAINT-20C) was composed
in its own pixels, square-on, from 3.8 m up: trunks like bars, the storehouse a box. This one is seen through one camera.

The hills north of Osaka, about 24 April 1830, dusk, in fine steady spring rain (the research of round twenty holds: a
charcoal-burner's storehouse of dark boards under a thatched roof, its floor on short posts; an earth charcoal kiln,
cold; a bamboo pipe out of the hillside behind it; a small worn stone figure by the path, a roadside Jizo in a red bib;
planted cedars, straight as organ pipes; nothing here reads as a cross).

THE CAMERA (HillCam). We stand at the foot of the path and look up the hill. The ground people walk on is ONE PLANE that
climbs away from us (SLOPE: 19 cm in every metre): a plane that climbs has its own vanishing line, higher in the picture
than eye level, and the game's two numbers are exactly that plane's: `horizon` (HZ) is the row the hillside runs back to,
`full` (FULL) the row where a grown-up standing on it is 160 px tall. So the engine's rule (size falls in a straight line
with the row of the feet) is true perspective for anyone on the hillside, with nothing to adjust. Eye level (TRUE_HZ) is
lower in the picture: the storehouse stands above it, and we see up under its eaves and under its raised floor. The lens
also looks up a little (PITCH), so that upright things lean together toward a vanishing point far above the picture: the
trunks tower. (With the pitch the engine's straight line is off by under 1.5 per cent anywhere people stand: sizes()
prints it.) Everything in the picture goes through this one camera: trunks, storehouse, steps, puddles, people.

    on(x, d, h)      the picture point of a place on the hillside: x cm across from the lens's line, d cm away, h cm above
                     the ground there
    level(x, d, Y)   the same for a true height Y (cm above the datum: the hillside's own level right under the lens):
                     for things that are level (a floor, an eave, a tread, a puddle)
    G(px, py)        the place on the hillside (x, d) that a picture point shows: how the layout is composed

LIGHT. Dusk under rain: little light, all of it cool and soft, from the sky, and most from the open hillside on the left
where the trees stand apart (upper left): forms are a shade lighter on that side, things throw only soft shade under
themselves, and whatever stands between us and that pale gap is a dark shape with a thin wet edge of light. The warm
things are the storehouse's lamp: a line of it under the floor and the high window (cut-outs the scene shows or not)."""

import math

import numpy as np

from brush import F32, Sheet, rgb, lerp, mask_poly, mask_ellipse, mask_line, noise, blur, over, tint, glow, step, grid, curve
from PIL import Image, ImageDraw

W, H = 800, 600
SHAPE = (H, W)
ID = "edo-cedars"
PX, PY = grid(SHAPE)

# ---------------------------------------------------------------- the camera
HZ, FULL = 340, 600          # the scene's `horizon` and `full`: the eye about 2.9 m above the hillside (FULL - HZ = 260)
FOCAL = 660.0                # the lens, in pixels (a little wide: 62 degrees across)
SLOPE = 0.19                 # the hillside climbs 19 cm in every metre away from us (10.8 degrees)
PITCH = 5.0                  # the lens looks up by this many degrees: upright things lean together a little


class HillCam:
    """World: x across (cm), d away along level ground, Y up. The lens is at (0, eye, 0); the hillside is the plane
    Y = slope * d. `hz` and `full` are the game's two rows for that plane; `eye` (the lens's height above the plane's
    foot) follows from them."""

    def __init__(self, hz=HZ, full=FULL, focal=FOCAL, slope=SLOPE, pitch=PITCH, cx=W / 2.0):
        self.F, self.S, self.cx = float(focal), float(slope), float(cx)
        self.b = math.radians(pitch)
        self.cb, self.sb = math.cos(self.b), math.sin(self.b)
        self.hz, self.full = float(hz), float(full)
        self.P = self.hz + self.F * math.tan(math.atan(self.S) - self.b)        # the row the lens points at
        self.true_hz = self.P + self.F * math.tan(self.b)                       # eye level
        self.up = (self.cx, self.P - self.F / math.tan(self.b)) if pitch else None   # where uprights meet, far above
        lo, hi = 50.0, 900.0
        for _ in range(60):                                                     # the eye's height: 160 px at `full`
            self.eye = (lo + hi) / 2
            d = self.depth_at_row(self.full)
            if self.on(0, d)[1] - self.on(0, d, 175.0)[1] > 160.0:
                lo = self.eye
            else:
                hi = self.eye

    def pt(self, x, d, Y):
        yd = self.eye - Y
        y2 = yd * self.cb + d * self.sb
        z2 = max(-yd * self.sb + d * self.cb, 1e-3)
        return (self.cx + self.F * x / z2, self.P + self.F * y2 / z2)

    def on(self, x, d, h=0.0):
        return self.pt(x, d, self.S * d + h)

    def depth_at_row(self, row):
        t = (row - self.P) / self.F
        return self.eye * (self.cb + t * self.sb) / (t * (self.S * self.sb + self.cb) - (self.sb - self.S * self.cb))

    def at(self, px, py):
        """A picture point below the hillside's vanishing line -> the place on the hillside (x, d)."""
        d = self.depth_at_row(py)
        yd = self.eye - self.S * d
        z2 = -yd * self.sb + d * self.cb
        return ((px - self.cx) * z2 / self.F, d)

    def px_cm(self, x, d, h=0.0):
        """Picture pixels per centimetre of height at a place."""
        a, b = self.on(x, d, h), self.on(x, d, h + 100.0)
        return math.hypot(a[0] - b[0], a[1] - b[1]) / 100.0

    def ground(self, shape=SHAPE):
        """For every pixel: the place on the hillside it shows. -> (x, d, mask); the mask is 1 below the vanishing line."""
        px, py = grid(shape)
        t = (py + 0.5 - self.P) / self.F
        den = t * (self.S * self.sb + self.cb) - (self.sb - self.S * self.cb)
        ok = den > 1e-4
        d = np.where(ok, self.eye * (self.cb + t * self.sb) / np.where(ok, den, 1.0), 1e6)
        z2 = -(self.eye - self.S * d) * self.sb + d * self.cb
        x = (px + 0.5 - self.cx) * z2 / self.F
        return x.astype(F32), d.astype(F32), ok.astype(F32)

    def plane_level(self, Y, shape=SHAPE):
        """For every pixel: the place on a LEVEL plane at true height Y it shows. -> (x, d, mask)."""
        px, py = grid(shape)
        t = (py + 0.5 - self.P) / self.F
        # yd = eye - Y; y2 = yd cb + d sb; z2 = -yd sb + d cb; y2 = t z2
        yd = self.eye - Y
        den = t * self.cb - self.sb
        with np.errstate(divide="ignore", invalid="ignore"):
            d = yd * (self.cb + t * self.sb) / den
        ok = np.isfinite(d) & (d > 30.0)
        d = np.where(ok, d, 1e6)
        z2 = -yd * self.sb + d * self.cb
        x = (px + 0.5 - self.cx) * z2 / self.F
        return x.astype(F32), d.astype(F32), ok.astype(F32)


CAM = HillCam()
EYE, TRUE_HZ = CAM.eye, CAM.true_hz


def on(x, d, h=0.0):
    return CAM.on(x, d, h)


def level(x, d, Y):
    return CAM.pt(x, d, Y)


def G(px, py):
    """The place on the hillside under a picture point: (x, d)."""
    return CAM.at(px, py)


def lift(d):
    """The hillside's true height at a depth."""
    return SLOPE * d


def k_at(y):
    """The game's size at a row: 1 on FULL, 0 on HZ (a grown-up is 160 * k px tall)."""
    return (np.asarray(y, F32) - HZ) / float(FULL - HZ)


def grownup_px(y):
    return float(160.0 * k_at(y))


def px_cm_row(y):
    """Picture pixels per centimetre for a thing standing on the hillside at a row (the game's rule)."""
    return 160.0 / 175.0 * float(k_at(y))


def sizes(rows=(600, 588, 560, 530, 500, 485, 470)):
    """The engine's straight line against the camera's truth, at rows people stand on: [(row, true px, game px)]."""
    out = []
    for r in rows:
        x, d = G(400, r)
        out.append((r, on(x, d)[1] - on(x, d, 175.0)[1], grownup_px(r)))
    return out


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, F32)


def mix(a, b, t):
    return lerp(col(a), col(b), t)


class Paper(Sheet):
    """A Sheet whose half-transparent strokes glaze over earlier ones instead of replacing them (as highway_kit.Paper)."""

    def _glaze(self, box, draw):
        w, h = self.im.size
        x0, y0 = max(int(box[0]) - 2, 0), max(int(box[1]) - 2, 0)
        x1, y1 = min(int(box[2]) + 3, w), min(int(box[3]) + 3, h)
        if x1 <= x0 or y1 <= y0:
            return self
        tmp = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        draw(ImageDraw.Draw(tmp), x0, y0)
        self.im.alpha_composite(tmp, (x0, y0))
        return self

    def poly(self, points, color, alpha=1.0):
        if alpha >= 0.999:
            return super().poly(points, color, alpha)
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        fill = self._fill(color, alpha)
        box = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
        return self._glaze(box, lambda d, ox, oy: d.polygon([(px - ox, py - oy) for px, py in pts], fill=fill))

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0):
        if alpha >= 0.999:
            return super().ellipse(cx, cy, rx, ry, color, alpha)
        s = self.ss
        fill = self._fill(color, alpha)
        box = ((cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s)
        return self._glaze(box, lambda d, ox, oy: d.ellipse([box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy], fill=fill))

    def line(self, points, color, width=1.0, alpha=1.0, round_ends=True):
        if alpha >= 0.999:
            return super().line(points, color, width, alpha, round_ends)
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        wd = max(1, int(round(width * s)))
        fill = self._fill(color, alpha)
        box = (min(p[0] for p in pts) - wd, min(p[1] for p in pts) - wd, max(p[0] for p in pts) + wd, max(p[1] for p in pts) + wd)

        def draw(d, ox, oy):
            q = [(px - ox, py - oy) for px, py in pts]
            d.line(q, fill=fill, width=wd, joint="curve")
            if round_ends and wd > 2:
                r = wd / 2
                for px, py in (q[0], q[-1]):
                    d.ellipse([px - r, py - r, px + r, py + r], fill=fill)
        return self._glaze(box, draw)


# ================================================================ the place, measured
# Everything stands on the hillside. A place is composed by the picture point of its foot (G) and then lives in
# centimetres: its size, its perspective and what it hides all follow from the camera.

# ---------------------------------------------------------------- the storehouse
# A box seen three-quarters on, standing higher up on the right. Its near corner (between its two walls that we see)
# points down the hill at us. The door wall runs from that corner to the left and away; the wall with the high window
# runs from it to the right and away (inside, edo-storehouse looks at the window's wall with the door on its right: the
# same building). The floor is level and the ground is not: it stands on posts, 95 cm clear at the near corner, and at
# its far corner is dug into the hill. The thatch is steep and comes down low over the walls: from down here we see the
# wall, the thatch's thick cut edge, and the slope going up; never the underside (we are far outside its plane).
class House:
    corner = G(505, 500)          # the near corner's foot on the hillside
    turn = 54.0                   # the door wall's angle from the picture's plane, degrees
    LW, LD = 600.0, 360.0         # the window wall's length; the door wall's
    gap = 95.0                    # the floor above the ground at the near corner
    wall = 270.0                  # the wall plate above the floor (hidden up under the thatch)
    pitch = 50.0                  # the thatch's slope, degrees: steep, as thatch must be
    eave = 80.0                   # how far the thatch overhangs the walls
    thatch = 50.0                 # the thatch's thickness where it is cut at the eave
    door = (60.0, 150.0, 176.0)   # along the door wall from the near corner: from, to; the lintel above the floor
    window = (178.0, 236.0, 100.0, 152.0)   # along the window wall: from, to; the sill and the head above the floor
    posts_w = (0.0, 150.0, 300.0, 450.0, 600.0)   # the posts of the window wall, and of the door wall
    posts_d = (0.0, 180.0, 360.0)

    def __init__(self):
        t = math.radians(self.turn)
        self.td = (-math.cos(t), math.sin(t))        # along the door wall: left and away
        self.tw = (math.sin(t), math.cos(t))         # along the window wall: right and away
        self.floor = lift(self.corner[1]) + self.gap  # the floor's true height
        k = math.tan(math.radians(self.pitch))
        self.k = k
        self.eave_under = self.wall - self.eave * k   # the thatch's lower edge, above the floor (it comes down over the wall's top)
        self.eave_top = self.eave_under + self.thatch
        self.ridge = self.wall + self.LD / 2 * k + self.thatch      # the ridge above the floor
        self.ridge_at = ((self.LD / 2, self.LD / 2), (self.LW - self.LD / 2, self.LD / 2))   # its two ends (u, w): it runs along the window wall

    def xd(self, u, w):
        """u cm along the window wall and w cm along the door wall from the near corner -> the place (x, d)."""
        return (self.corner[0] + u * self.tw[0] + w * self.td[0], self.corner[1] + u * self.tw[1] + w * self.td[1])

    def pt(self, u, w, Y):
        """...and Y cm above the floor -> the picture point."""
        x, d = self.xd(u, w)
        return level(x, d, self.floor + Y)

    def foot(self, u, w, h=0.0):
        """The picture point of the ground under (u, w) (or h cm above that ground)."""
        return on(*self.xd(u, w), h)

    def clear(self, u, w):
        """How far the floor is above the ground under (u, w), cm (negative: dug in)."""
        return self.floor - lift(self.xd(u, w)[1])

    def out_door(self, w, out):
        """A place `out` cm in front of the door wall, `w` cm along it."""
        return self.xd(-out, w)

    def out_window(self, u, out):
        """A place `out` cm in front of the window's wall, `u` cm along it."""
        return self.xd(u, -out)

    def roof_long(self, u, w):
        """The thatch's top over the window wall (the long slope), above the floor, at (u, w)."""
        return self.eave_top + (w + self.eave) * self.k

    def roof_hip(self, u, w):
        """The thatch's top over the door wall (the hip), above the floor, at (u, w)."""
        return self.eave_top + (u + self.eave) * self.k


HOUSE = House()

# ---------------------------------------------------------------- the path, the yard, and what stands by them
# The path's middle line as picture points on the hillside (bottom first) and its half width in cm at each.
PATH = [(232, 612, 128), (242, 586, 124), (270, 563, 114), (330, 546, 104), (398, 532, 98), (440, 516, 96), (448, 502, 96)]
KILN = dict(at=G(268, 466), r=116.0, h=132.0)                       # the earth kiln: a dome up to the left of the yard
JIZO = dict(at=G(410, 568), h=60.0)                                 # the stone figure, right of the lower steps
# The cut bank behind the storehouse's far end, as picture points: its lip (left to right) and its foot.
BANK_TOP = [(686, 398), (706, 386), (730, 380), (760, 372), (800, 362)]
BANK_FOOT = [(694, 466), (716, 468), (748, 474), (776, 480), (800, 486)]
PIPE = dict(at=G(764, 472), h=136.0, to=(-0.93, -0.36), long=96.0)   # the bamboo pipe: where it leaves the bank, 136 cm up; which way it points (left, and a little toward us); its length


def pipe_ends():
    """The pipe's two ends as picture points: where it leaves the earth, and its mouth."""
    x, d = PIPE["at"]
    return on(x, d + 14.0, PIPE["h"]), on(x + PIPE["to"][0] * PIPE["long"], d + 14.0 + PIPE["to"][1] * PIPE["long"], PIPE["h"] + 5.0)

# The trunks: (picture x and row of the foot's middle, radius in cm at breast height, how far it leans to the right in cm
# per metre of height). `cut`: the two that people walk behind; `mid`: in the backdrop round the play; the far ranks are
# laid by the painter (edo_cedars.py far_ranks).
CEDAR_L = [(332, 513, 26.0, -0.5)]
CEDAR_R = [(676, 540, 28.0, 0.7)]
TRUNKS_MID = [(138, 508, 46.0, 0.5), (190, 452, 32.0, -0.3), (452, 418, 32.0, 0.2), (598, 428, 34.0, -0.4), (806, 506, 48.0, 0.6),
              (734, 430, 30.0, 0.3)]
# The near cedar, on its bank at the left edge: where its middle stands (x, d: beside and a little behind the lens's
# left shoulder), its radius, and how high the bank's top is above the hillside there.
NEAR = dict(x=-236.0, d=345.0, r=64.0, bank=150.0)

# ---------------------------------------------------------------- where people stand (places on the hillside)
MARKS = {
    "enter": G(258, 589), "figure": G(334, 575), "door": HOUSE.out_door(106.0, 128.0), "window": HOUSE.out_window(208.0, 102.0),
    "pipe": G(742, 486), "isukeFrom": G(232, 598),
}
LIFT_AT = HOUSE.out_window(98.0, 86.0)            # Mom, a step to the left of the window's place
ARRIVE = {"enter": [G(318, 586), G(200, 592)], "door": [G(382, 512), G(454, 513)]}
KILN_STAND = G(292, 494)
# the constable's way up the path (places, bottom first), ending at the door
ISUKE_WAY = [G(232, 598), G(252, 580), G(282, 561), G(330, 544), G(386, 529), G(420, 512), MARKS["door"]]


def P(place, h=0.0):
    """A place (x, d) as a rounded picture point."""
    x, y = on(place[0], place[1], h)
    return [int(round(x)), int(round(y))]


# ---------------------------------------------------------------- the path's edges and its steps
def path_world():
    return [G(px, py) + (hw,) for (px, py, hw) in PATH]


def path_edges(n=10):
    """The path's two edges as places, bottom first: (left, right)."""
    pts = path_world()
    mid = curve([(p[0], p[1]) for p in pts], n)
    # half widths along the smoothed line
    hw = np.interp(np.linspace(0, len(pts) - 1, len(mid)), np.arange(len(pts)), [p[2] for p in pts])
    left, right = [], []
    for i, (x, d) in enumerate(mid):
        a = mid[max(i - 1, 0)]
        b = mid[min(i + 1, len(mid) - 1)]
        tx, td = b[0] - a[0], b[1] - a[1]
        nn = math.hypot(tx, td) or 1.0
        nx, nd = td / nn, -tx / nn                       # to the right of the way up
        left.append((x - nx * hw[i], d - nd * hw[i]))
        right.append((x + nx * hw[i], d + nd * hw[i]))
    return left, right, mid


# ---------------------------------------------------------------- a trunk through the camera
def trunk_edges(foot, r, lean=0.0, top=3600.0, taper=0.10, steps=14, x=None, d=None, base=0.0):
    """A cedar's two edges as picture points, foot first: [(left), ...], [(right), ...]. `foot` is the picture point of
    its foot's middle on the hillside (or give the place x, d and `base`, cm above the hillside); `r` its radius in cm;
    `lean` cm to the right per metre of height; it tapers by `taper` over 30 m. The roots are the painter's."""
    if x is None:
        x, d = G(*foot)
    left, right = [], []
    for i in range(steps + 1):
        h = top * (i / steps) ** 1.6
        rr = r * (1 - taper * min(h / 3000.0, 1.2))
        cx = x + lean * h / 100.0
        left.append(on(cx - rr, d, base + h))
        right.append(on(cx + rr, d, base + h))
    return left, right


# ---------------------------------------------------------------- the ground people may stand on (picture points on the hillside)
WALK = [(128, 600), (150, 584), (178, 568), (216, 553), (258, 541), (300, 533), (340, 525), (364, 514), (372, 505), (344, 503), (276, 503),
        (270, 488), (322, 486), (378, 482), (396, 484), (420, 490), (447, 499), (478, 511), (505, 519), (526, 510), (566, 501), (604, 494),
        (638, 488), (670, 483), (708, 478), (772, 485), (778, 494), (730, 500), (700, 508), (660, 512), (610, 520), (556, 532), (500, 540),
        (460, 542), (430, 543), (392, 553), (366, 562), (344, 572), (338, 584), (340, 600)]
# the stone before the door (nobody stands on it)
BLOCKED = [[HOUSE.foot(-12, 50), HOUSE.foot(-12, 164), HOUSE.foot(-84, 158), HOUSE.foot(-80, 56)]]


# ---------------------------------------------------------------- the steps
STEP_RISE = 11.0             # each step lifts this much: broad, low, worn steps (the hillside gains 19 cm a metre)
_STEPS = []


def _at(line, f):
    """A point of a line of places at a fractional index."""
    f = min(max(f, 0.0), len(line) - 1.0)
    i = min(int(f), len(line) - 2)
    q = f - i
    return (line[i][0] + (line[i + 1][0] - line[i][0]) * q, line[i][1] + (line[i + 1][1] - line[i][1]) * q)


def steps():
    """The path's steps, bottom first: each a dict with its riser's two ends (places: `l`, `r`), the level `Y` of the
    tread ABOVE that riser, the level `Y0` of the tread below it, and `tread`: the outline (places) of the tread above
    it, up to the next riser. Each tread is level; its middle lies on the hillside, so whoever the game stands on it
    stands on it. The risers are neither square to the path nor level with the picture: worn, and set by hand."""
    if _STEPS:
        return _STEPS
    rng = np.random.default_rng(8)
    left, right, mid = path_edges(n=14)
    idx = np.arange(len(mid), dtype=float)
    dm, dl, dr = [q[1] for q in mid], [q[1] for q in left], [q[1] for q in right]
    D = dm[0] + 22.0
    rows = []
    while D < dm[-1] - 70.0:
        f = float(np.interp(D, dm, idx))
        fl = float(np.interp(D, dl, idx))
        fr = float(np.interp(D, dr, idx))
        k = 0.42 + rng.uniform(-0.12, 0.12)                     # between level with the picture (0) and square to the path (1)
        rows.append((D, fl + (f - fl) * k + rng.uniform(-0.12, 0.12), fr + (f - fr) * k + rng.uniform(-0.12, 0.12)))
        D += STEP_RISE / SLOPE * rng.uniform(0.80, 1.22)
    for i, (D, fl, fr) in enumerate(rows):
        nxt = rows[i + 1] if i + 1 < len(rows) else (dm[-1], len(mid) - 1.0, len(mid) - 1.0)
        tread = [_at(left, fl), _at(right, fr)]
        tread += [right[j] for j in range(int(math.floor(fr)) + 1, int(math.ceil(nxt[2])))]
        tread += [_at(right, nxt[2]), _at(left, nxt[1])]
        tread += [left[j] for j in range(int(math.ceil(nxt[1])) - 1, int(math.floor(fl)), -1)]
        _STEPS.append(dict(D=D, l=_at(left, fl), r=_at(right, fr), Y=lift(D) + STEP_RISE / 2, Y0=lift(D) - STEP_RISE / 2, tread=tread, fl=fl, fr=fr))
    for i, st in enumerate(_STEPS):                             # (each tread level with its own riser's top; the riser below it drops to the tread before)
        st["Y0"] = _STEPS[i - 1]["Y"] if i else st["Y"] - STEP_RISE
    return _STEPS


def foot_tread():
    """The tread below the first riser (it runs off the bottom of the picture): its outline, and its level."""
    left, right, mid = path_edges(n=14)
    st = steps()[0]
    out = [left[0], right[0]] + [right[j] for j in range(1, int(math.ceil(st["fr"])))] + [st["r"], st["l"]] + [left[j] for j in range(int(math.ceil(st["fl"])) - 1, 0, -1)]
    return out, st["Y0"]


if __name__ == "__main__":
    print(f"eye {EYE:.0f} cm above the hillside's foot; eye level at row {TRUE_HZ:.0f}; the lens points at row {CAM.P:.0f}; uprights meet at {CAM.up}")
    for r, true, game in sizes():
        print(f"  row {r}: a grown-up {true:6.1f} px (the engine draws {game:6.1f}: {100 * (game - true) / true:+.1f}%)")
    for name, place in MARKS.items():
        print(f"  {name:10s} {P(place)}  d {place[1]:.0f}  {grownup_px(P(place)[1]):.0f} px")
    print("  lift", P(LIFT_AT), " house corner", [round(v) for v in HOUSE.corner], " floor above the eye by", round(HOUSE.floor - EYE))

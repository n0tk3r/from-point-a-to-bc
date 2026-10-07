"""Tools for painting architecture, written for the temple steps in Rome (rome_steps.py).

A building is measured in its own centimetres: u along its front (left to right), v back into it,
h up from the pavement. A Frame turns those into places in the picture through the game's own camera
(persp.Camera), so a building may stand at any angle to us and still agree with the people the game
draws. The other way round, `on_floor`, `on_front` and `on_side` say, for every pixel of the picture,
where on a level, front-facing or side-facing plane of the building it looks: that is what lets
stone joints, painted patterns and stains lie on a wall in true perspective.

Also here: a Canvas to build a cut-out on, a lathe (columns and anything else that is round), light,
and a few surfaces (coursed stone, plaster with its wear)."""

import copy
import hashlib
import inspect
import math
import os

import numpy as np
from PIL import Image, ImageDraw

from brush import (F32, Sheet, blur, grid, lerp, mask_ellipse, mask_line, mask_poly, noise, over, ramp, rgb, resize, sample, smooth,
                   step, tint, vary, warp)
from persp import Camera


def unit(v):
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v)


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


def mix(a, b, t):
    return lerp(col(a), col(b), t)


class Frame:
    def __init__(self, cam, angle, at_x, at_depth, size=(800, 600), fine=1):
        """`angle` (degrees) turns the building so that its front looks a little to our right and its left
        flank comes into view. Its corner (u = 0, v = 0) stands `at_depth` cm from the lens, at picture
        column `at_x`. `fine` paints on a sheet that many times finer than the picture (to be reduced after)."""
        self.cam, self.fine = cam, fine
        self.angle, self.at_x, self.at_depth = angle, at_x, at_depth
        w, h = size
        self.shape = (h * fine, w * fine)
        self.whole, self.off = self.shape, (0, 0)            # a window() of a frame covers only part of the sheet
        b = math.radians(angle)
        self.eu = (math.cos(b), math.sin(b))                 # one cm along the front, as (across, away)
        self.ev = (-math.sin(b), math.cos(b))                # one cm back into the building
        self.cx = (at_x - cam.vx) * at_depth / cam.F
        self.cz = float(at_depth)
        gx, gy = grid(self.shape)
        self.px, self.py = (gx + 0.5) / fine - 0.5, (gy + 0.5) / fine - 0.5       # picture coordinates of every sample
        self.dx = (self.px - cam.vx) / cam.F                 # the ray through each sample, per cm of depth
        self.dy = (self.py - cam.vy) / cam.F

    @classmethod
    def at(cls, cam, angle, wx, wz, size=(800, 600), fine=1):
        """A frame whose corner stands at a place in the world (cm across from the middle, cm from the lens)."""
        return cls(cam, angle, cam.vx + wx * cam.F / wz, wz, size, fine)

    def finer(self, fine):
        return Frame(self.cam, self.angle, self.at_x, self.at_depth, (self.whole[1] // self.fine, self.whole[0] // self.fine), fine)

    def window(self, picture_points, pad=3):
        """The same frame, but covering only the box round some picture points (so that painting a small
        piece does not cost a whole sheet). -> a Frame, or None if the box is off the picture."""
        f = self.fine
        xs, ys = [p[0] for p in picture_points], [p[1] for p in picture_points]
        x0, x1 = int(max(0, math.floor((min(xs) - pad) * f))), int(min(self.whole[1], math.ceil((max(xs) + pad) * f) + 1))
        y0, y1 = int(max(0, math.floor((min(ys) - pad) * f))), int(min(self.whole[0], math.ceil((max(ys) + pad) * f) + 1))
        if x1 - x0 < 2 or y1 - y0 < 2:
            return None
        w = copy.copy(self)
        ox, oy = self.off
        sl = (slice(y0 - oy, y1 - oy), slice(x0 - ox, x1 - ox))
        w.off, w.shape = (x0, y0), (y1 - y0, x1 - x0)
        w.px, w.py, w.dx, w.dy = self.px[sl], self.py[sl], self.dx[sl], self.dy[sl]
        return w

    def face(self, points, pad=3):
        """For a flat piece of the building given by its corners (u, v, h): -> [(window, mask)], or [] if it
        is out of the picture. Written to be used as `for w, m in frame.face(...)`."""
        pp = [self.pt(*p) for p in points]
        w = self.window(pp, pad)
        return [] if w is None else [(w, w.mask(pp))]

    # ---- building -> picture
    def ground(self, u, v):
        return (self.cx + u * self.eu[0] + v * self.ev[0], self.cz + u * self.eu[1] + v * self.ev[1])

    def depth(self, u, v):
        return self.cz + u * self.eu[1] + v * self.ev[1]

    def k(self, u, v):
        """Picture pixels per cm at that place."""
        return self.cam.F / self.depth(u, v)

    def pt(self, u, v, h):
        x, z = self.ground(u, v)
        k = self.cam.F / max(z, 1.0)
        return (self.cam.vx + x * k, self.cam.vy + (self.cam.eye - h) * k)

    def pts(self, points):
        return [self.pt(*p) for p in points]

    def poly(self, points, soft=0.0, wobble=0.0, seed=0):
        """A mask for a flat piece of the building given by its corners (u, v, h)."""
        return self.mask([self.pt(*p) for p in points], soft, wobble, seed)

    def mask(self, picture_points, soft=0.0, wobble=0.0, seed=0):
        f = self.fine
        pts = [((x + 0.5) * f - 0.5 - self.off[0], (y + 0.5) * f - 0.5 - self.off[1]) for x, y in picture_points]
        return mask_poly(self.shape, pts, soft=soft * f, wobble=wobble * f, seed=seed, ss=3 if f == 1 else 2)

    # ---- picture -> building: where each sample looks on a plane of the building
    def _uv(self, Z):
        x = self.dx * Z
        rx, rz = x - self.cx, Z - self.cz
        return rx * self.eu[0] + rz * self.eu[1], rx * self.ev[0] + rz * self.ev[1]

    def on_floor(self, h):
        """-> (u, v, pixels per cm) on the level plane at height h."""
        with np.errstate(divide="ignore", invalid="ignore"):
            Z = (self.cam.eye - h) / np.where(np.abs(self.dy) < 1e-6, 1e-6, self.dy)
        Z = np.where((Z > 10) & (Z < 4e5), Z, 4e5)
        u, v = self._uv(Z)
        return u.astype(F32), v.astype(F32), (self.cam.F / Z).astype(F32)

    def on_front(self, v0):
        """-> (u, h, pixels per cm) on the upright plane v = v0 (parallel to the building's front)."""
        den = self.dx * self.ev[0] + self.ev[1]
        Z = (v0 + self.cx * self.ev[0] + self.cz * self.ev[1]) / np.where(np.abs(den) < 1e-6, 1e-6, den)
        Z = np.where((Z > 10) & (Z < 4e5), Z, 4e5)
        u, _ = self._uv(Z)
        return u.astype(F32), (self.cam.eye - self.dy * Z).astype(F32), (self.cam.F / Z).astype(F32)

    def on_side(self, u0):
        """-> (v, h, pixels per cm) on the upright plane u = u0 (parallel to the building's flank)."""
        den = self.dx * self.eu[0] + self.eu[1]
        Z = (u0 + self.cx * self.eu[0] + self.cz * self.eu[1]) / np.where(np.abs(den) < 1e-6, 1e-6, den)
        Z = np.where((Z > 10) & (Z < 4e5), Z, 4e5)
        _, v = self._uv(Z)
        return v.astype(F32), (self.cam.eye - self.dy * Z).astype(F32), (self.cam.F / Z).astype(F32)

    def to_frame(self, world):
        """A direction in the world (across, up, away) as (along u, along v, up)."""
        x, y, z = world
        return (x * self.eu[0] + z * self.eu[1], x * self.ev[0] + z * self.ev[1], y)

    def vanish(self):
        """The two vanishing points on the horizon: (for lines along u, for lines along v)."""
        return (self.cam.vx + self.cam.F * self.eu[0] / self.eu[1], self.cam.vx + self.cam.F * self.ev[0] / self.ev[1])

    def find(self, x, y, h=0.0):
        """The place (u, v) on the level plane at height h that picture point (x, y) looks at."""
        Z = (self.cam.eye - h) * self.cam.F / (y - self.cam.vy)
        wx = (x - self.cam.vx) / self.cam.F * Z
        rx, rz = wx - self.cx, Z - self.cz
        return rx * self.eu[0] + rz * self.eu[1], rx * self.ev[0] + rz * self.ev[1]


class Canvas:
    """A clear sheet to build a painted thing on, piece over piece, keeping a true edge (the color is kept
    multiplied by its coverage, so soft edges do not go dark)."""

    def __init__(self, shape):
        self.shape = shape
        self.c = np.zeros(shape + (3,), dtype=F32)
        self.a = np.zeros(shape, dtype=F32)

    @staticmethod
    def _part(window):
        if window is None:
            return (slice(None), slice(None))
        (x0, y0), (h, w) = window.off, window.shape
        return (slice(y0, y0 + h), slice(x0, x0 + w))

    def put(self, color, mask, window=None):
        """Lay a color (or a picture) on through a mask. With `window` (a Frame.window), both are only the
        size of that window."""
        color = col(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
        sl = self._part(window)
        m = np.clip(mask, 0, 1)[..., None]
        self.c[sl] = self.c[sl] * (1 - m) + color * m
        self.a[sl] = self.a[sl] * (1 - m[..., 0]) + m[..., 0]
        return self

    def tint(self, color, mask, window=None):
        """Multiply what is already there toward a color (a shadow, a stain)."""
        color = col(color)
        sl = self._part(window)
        m = np.clip(mask, 0, 1)[..., None]
        self.c[sl] = self.c[sl] * ((1 - m) + color * m)
        return self

    def lay(self, other):
        """Another canvas on top of this one."""
        self.c = self.c * (1 - other.a[..., None]) + other.c
        self.a = self.a * (1 - other.a) + other.a
        return self

    def reduced(self, fine):
        """-> a canvas `fine` times smaller (box filter)."""
        if fine == 1:
            return self
        h, w = self.shape[0] // fine, self.shape[1] // fine
        out = Canvas((h, w))
        out.c = self.c.reshape(h, fine, w, fine, 3).mean(axis=(1, 3)).astype(F32)
        out.a = self.a.reshape(h, fine, w, fine).mean(axis=(1, 3)).astype(F32)
        return out

    def straight(self):
        """-> (color, coverage) with the color no longer multiplied by its coverage."""
        return (self.c / np.maximum(self.a, 1e-4)[..., None]).clip(0, 1).astype(F32), self.a

    def onto(self, picture, amount=1.0):
        picture[...] = picture * (1 - self.a[..., None] * amount) + self.c * amount
        return picture

    def warped(self, amount, cell, seed):
        out = Canvas(self.shape)
        both = warp(np.dstack([self.c, self.a]), amount, cell, seed)
        out.c, out.a = both[..., :3].astype(F32), np.clip(both[..., 3], 0, 1).astype(F32)
        return out


# ---------------------------------------------------------------- light
class Light:
    """Sunlight with a direction and a warm color; shadows filled with the blue of the open sky and, low
    down, with warm light thrown back up from sunlit ground. `on` gives a surface its lit color."""

    def __init__(self, to_sun, sun=(1.09, 1.0, 0.80), shade=(0.50, 0.55, 0.86), bounce=(0.26, 0.15, 0.03)):
        self.to_sun = unit(to_sun)
        self.sun, self.shade, self.bounce = np.asarray(sun, dtype=F32), np.asarray(shade, dtype=F32), np.asarray(bounce, dtype=F32)

    @staticmethod
    def frac(facing):
        """How lit a surface looks for how squarely it faces the sun: grazing light already counts for a lot."""
        return np.clip(np.asarray(facing, dtype=F32) / 0.72, 0, 1) ** 0.6

    def on(self, own, facing=0.0, shadow=0.0, up=0.0, deep=0.0, bounce=0.3):
        """`own`: the surface's own color (one color or a picture). `facing`: how squarely it faces the sun
        (0 to 1). `shadow`: how much of the sun is cut off. `up`: -1 a ceiling, 0 a wall, 1 a floor.
        `deep`: how shut in it is (0 open to the sky, 1 a deep recess). `bounce`: warm light from below."""
        own = col(own) if isinstance(own, str) else np.asarray(own, dtype=F32)
        f = self.frac(facing) * (1 - np.asarray(shadow, dtype=F32))
        parts = [np.asarray(a, dtype=F32) for a in (f, up, deep, bounce)]
        if own.ndim == 3 or any(p.ndim for p in parts):
            parts = [p[..., None] if p.ndim else p for p in parts]
        f, up, deep, bounce = parts
        shade = self.shade * (1 + 0.10 * up) * (1 - 0.8 * deep) + self.bounce * bounce
        return np.clip(own * (shade * (1 - f) ** 1.6 + self.sun * f), 0, 1).astype(F32)      # a plane the sun only grazes is dim but still warm


# ---------------------------------------------------------------- round things
def lathe(frame, light, u0, v0, profile, paint, flutes=0, flute_from=None, flute_to=None, groove=0.75, shadow=None, deep=0.0, bounce=0.8, wrap=0.30, gain=1.5):
    """Something turned on a lathe, standing upright with its axis at (u0, v0): a column, a base, a jar.

    `profile` is a list of (height, radius) from bottom to top. `paint(h, around)` gives its own color for
    every sample (`around` is the angle round the axis, 0 to 1; both are pictures). `flutes` cuts that many
    grooves down it between the heights flute_from and flute_to. `shadow(h, s, around)` (optional) gives how
    much of the sun is cut off. -> (color picture, coverage mask), both the size of the frame's sheet."""
    cam = frame.cam
    x, y = frame.px, frame.py
    ax, az = frame.ground(u0, v0)
    k = cam.F / az
    xc = cam.vx + ax * k
    hs = np.array([p[0] for p in profile], dtype=float)
    rs = np.array([p[1] for p in profile], dtype=float)
    h_axis = cam.eye - (y - cam.vy) / k                                   # the height the axis has on this row
    r_here = np.interp(h_axis, hs, rs, left=rs[0], right=rs[-1])
    r_px = r_here * k
    s = np.clip((x - xc) / np.maximum(r_px, 1e-3), -0.999, 0.999)
    th = np.arcsin(s)                                                      # round the column from the middle of what we see
    h = cam.eye - (y - cam.vy) * (az - r_here * np.cos(th)) / cam.F        # true height: the front of a ring is nearer, so rings curve
    inside = np.clip((r_px - np.abs(x - xc)) * frame.fine + 0.5, 0, 1) * np.clip((h - hs[0]) * k * frame.fine + 0.5, 0, 1) * np.clip((hs[-1] - h) * k * frame.fine + 0.5, 0, 1)
    h = np.clip(h, hs[0], hs[-1])
    mid = hs[:-1] + np.diff(hs) / 2
    slope = np.interp(h, mid, np.diff(rs) / np.maximum(np.diff(hs), 1e-6))
    tilt = np.arctan(-slope)                                               # how far the surface leans to face up (+) or down (-)
    d = math.hypot(ax, az)                                                 # from the axis toward us, and toward our right, on the ground
    cx_, cz_ = -ax / d, -az / d
    rx_, rz_ = -cz_, cx_
    if rx_ < 0:
        rx_, rz_ = -rx_, -rz_
    nx = np.cos(th) * cx_ + np.sin(th) * rx_
    nz = np.cos(th) * cz_ + np.sin(th) * rz_
    ang = np.arctan2(nz, nx)
    around = (ang / (2 * math.pi)) % 1.0
    S = light.to_sun
    if flutes:
        lo = hs[0] if flute_from is None else flute_from
        hi = hs[-1] if flute_to is None else flute_to
        dlt = ((around * flutes) % 1.0 - 0.5) * 2                          # -1 to 1 across one groove
        ends = step(lo, lo + 10, h) * step(hi, hi - 8, h)                   # grooves run out before the ends
        fl = ends * np.clip((0.92 - np.abs(dlt)) / 0.14, 0, 1)              # 0 on the flat ridge between two grooves
        a2 = ang - dlt * groove * fl                                        # the two sides of a groove face one another
        nx2, nz2 = np.cos(a2), np.sin(a2)
        hollow = fl * (1 - dlt * dlt)
    else:
        nx2, nz2, hollow = nx, nz, 0.0
    ct = np.cos(tilt)
    flat = nx * S[0] + nz * S[2]
    core = (flat + wrap) / (1 + wrap) * ct + np.sin(tilt) * S[1]           # as if it were smooth: this decides the form shadow
    facing = np.clip((((nx2 * S[0] + nz2 * S[2]) + wrap) / (1 + wrap) * ct + np.sin(tilt) * S[1]) * gain, 0, 1) * step(-0.02, 0.16, core)
    cut = 0.0 if shadow is None else shadow(h, s, around)
    own = paint(h, around)
    away = np.clip(-flat, 0, 1)                                             # the side turned from the sun takes light thrown back
    sunny = step(0.0, 0.3, core) * (1 - np.asarray(cut))
    out = light.on(own, facing, cut, up=np.sin(tilt) * 0.8, deep=np.clip(deep + 0.40 * hollow * (1 - sunny), 0, 1),
                   bounce=bounce * (0.35 + 0.9 * away) + 1.5 * hollow * sunny)       # a groove in the sun is filled with warm light from its other side
    rim = np.clip((np.abs(s) - 0.82) / 0.18, 0, 1)                          # the edge that turns away is a touch darker
    out = out * (1 - 0.14 * rim[..., None])
    return out.astype(F32), inside.astype(F32)


# ---------------------------------------------------------------- surfaces
def hash2(i, j, seed=0):
    """A number 0 to 1 for each pair of whole numbers: the same pair always gives the same number."""
    v = np.sin(i * 127.1 + j * 311.7 + seed * 74.7) * 43758.5453
    return (v - np.floor(v)).astype(F32)


_tiles = {}


def tex(a, b, cell, seed, octaves=4):
    """Cloudy noise (0 to 1) that lies ON a surface: `a`, `b` are places on it in cm, `cell` the size in
    cm of its largest blotches."""
    key = (seed, octaves)
    if key not in _tiles:
        _tiles[key] = noise((1024, 1024), 64, seed, octaves)
    n = 1020.0
    ta = np.abs(((a / cell * 64.0 + seed * 37.0) % (2 * n)) - n)          # fold, so there is never a seam
    tb = np.abs(((b / cell * 64.0 + seed * 91.0) % (2 * n)) - n)
    return sample(_tiles[key], ta, tb)


def courses(a, b, long=120.0, high=58.0, seed=0, joint=1.6, ppc=None, vary_len=0.3, bond=0.5):
    """Squared stone laid in level courses, on a plane measured in cm (`a` along, `b` up or back).
    -> (a number 0 to 1 for each block, joint mask 0 to 1, a line just above every bed joint).
    `joint` is the joint's width in cm; give `ppc` (pixels per cm, a number or picture) so that far joints
    grow faint instead of flickering."""
    row = np.floor(b / high)
    fb = b / high - row
    off = hash2(row, 7, seed) * 0.6 + bond * (row % 2)
    q = a / long + off
    i = np.floor(q)
    j0 = (hash2(i, row, seed + 1) - 0.5) * vary_len                         # each upright joint is moved a little
    j1 = (hash2(i + 1, row, seed + 1) - 0.5) * vary_len
    fa = q - i
    left = fa - j0
    right = (1 + j1) - fa
    block = np.where(left < 0, i - 1, np.where(right < 0, i + 1, i))
    tone = hash2(block, row, seed + 2)
    da = np.minimum(np.abs(left), np.abs(right)) * long                     # cm to the nearest upright joint
    db = np.minimum(fb, 1 - fb) * high                                      # cm to the nearest bed joint
    if ppc is not None:
        w = np.maximum(joint, 0.8 / np.maximum(ppc, 1e-4))                  # never thinner than most of a pixel...
        fade = np.clip(ppc * joint / 0.55, 0.0, 1.0)                        # ...but fainter instead
    else:
        w, fade = joint, 1.0
    jm = np.clip(1.5 - np.minimum(da, db) / (w * 0.5), 0, 1) * fade
    above = np.clip(1.5 - np.abs(fb * high - w * 1.2) / (w * 0.5), 0, 1) * fade
    return tone.astype(F32), jm.astype(F32), above.astype(F32)


def stone(a, b, ppc, base, seed, long=120.0, high=58.0, spread=0.10, joint=1.6, joint_color="#6f5c50", blot=0.08, bond=0.5):
    """Coursed stone with its own color: -> picture. Every block a little lighter or darker and warmer or
    cooler than the next; blotches of weather over several blocks; dark joints."""
    tone, jm, above = courses(a, b, long, high, seed, joint, ppc, bond=bond)
    c = col(base)[None, None, :] * (1 + (tone[..., None] - 0.5) * 2 * spread)
    warm = (hash2(np.floor(tone * 977), 3, seed) - 0.5) * 0.06
    c = c + np.stack([warm, warm * 0.2, -warm], axis=-1)
    c = c * (1 + (tex(a, b, 260, seed + 5)[..., None] - 0.5) * 2 * blot + (tex(a, b, 40, seed + 6)[..., None] - 0.5) * blot)
    c = c * (1 - 0.55 * jm[..., None]) + col(joint_color) * 0.55 * jm[..., None]
    c = c * (1 + 0.10 * above[..., None] * (1 - jm[..., None]))             # the arris below a joint catches a little light
    return np.clip(c, 0, 1).astype(F32), jm


def holes(a, b, seed, cell=80.0, amount=0.3, sharp=0.04):
    """Ragged patches on a surface (0 to 1) where a coat of plaster or paint has come away."""
    n = tex(a, b, cell, seed) * 0.72 + tex(a, b, cell / 5.0, seed + 1, 3) * 0.28
    return step(1 - amount - sharp, 1 - amount + sharp, n)


def source_key(*things):
    """A fingerprint of the source of some functions and files, so a kept picture is thrown away when
    what paints it changes."""
    m = hashlib.md5()
    for t in things:
        if isinstance(t, str) and os.path.exists(t):
            m.update(open(t, "rb").read())
        elif isinstance(t, (str, bytes)):
            m.update(t if isinstance(t, bytes) else t.encode())
        else:
            m.update(inspect.getsource(t).encode())
    return m.hexdigest()[:12]


# ---------------------------------------------------------------- cast shadows
def sunless(solids, u, v, h, sun, spread=0.012, eps=1.5):
    """Where the sun cannot reach: for places (u, v, h) in a building's own measurements (pictures or numbers),
    -> 0 to 1 of the sun cut off by the `solids`. `sun` is the direction to the sun as (along u, along v, up).
    Solids are ("box", u0, u1, v0, v1, h0, h1), ("cyl", u, v, radius, h0, h1) and
    ("gable", u0, u1, v0, v1, base, pitch): a roof whose ridge runs along v over the middle of u0..u1.
    The edge of a shadow is made soft, and softer the farther it falls, by looking toward three places on the sun."""
    u, v, h = [np.array(q, dtype=F32) for q in np.broadcast_arrays(u, v, h)]
    total = np.zeros(u.shape, dtype=F32)
    su0, sv0, sh0 = sun
    side = unit((-sv0, su0, 0.0))
    looks = [(0.0, 0.0), (spread, spread * 0.5), (-spread, -spread * 0.5)] if spread else [(0.0, 0.0)]
    for ds, dh in looks:
        su, sv, sh = su0 + side[0] * ds, sv0 + side[1] * ds, sh0 + dh
        a, b = su / sh, sv / sh                                             # how far the ray moves for each cm it climbs
        hit = np.zeros(u.shape, dtype=bool)
        for s in solids:
            kind = s[0]
            if kind == "cyl":
                _, uc, vc, r, h0, h1 = s
                du, dv = u - uc, v - vc
                A = a * a + b * b
                B = 2 * (du * a + dv * b)
                C = du * du + dv * dv - r * r
                disc = B * B - 4 * A * C
                ok = disc > 0
                rt = np.sqrt(np.where(ok, disc, 0))
                ha = np.maximum(np.maximum(h + (-B - rt) / (2 * A), h0), h + eps)
                hb = np.minimum(h + (-B + rt) / (2 * A), h1)
                hit |= ok & (hb > ha)
                continue
            _, u0, u1, v0, v1 = s[:5]
            la, lb = h + (u0 - u) / a, h + (u1 - u) / a
            lo, hi = np.minimum(la, lb), np.maximum(la, lb)
            if abs(b) > 1e-6:
                lc, ld = h + (v0 - v) / b, h + (v1 - v) / b
                lo, hi = np.maximum(lo, np.minimum(lc, ld)), np.minimum(hi, np.maximum(lc, ld))
            else:
                inside = (v >= v0) & (v <= v1)
                lo = np.where(inside, lo, 1e9)
            if kind == "box":
                h0, h1 = s[5], s[6]
                hit |= np.minimum(hi, h1) > np.maximum(np.maximum(lo, h0), h + eps)
            else:
                base, pitch = s[5], s[6]
                mid, half = (u0 + u1) / 2, (u1 - u0) / 2
                A1 = (base + (half - u + h * a + mid) * pitch) / (1 + a * pitch)
                A2 = (base + (half + u - h * a - mid) * pitch) / (1 - a * pitch)
                hit |= np.minimum(np.minimum(hi, A1), A2) > np.maximum(np.maximum(lo, base), h + eps)
        total += hit
    return (total / len(looks)).astype(F32)

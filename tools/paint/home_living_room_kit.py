"""Tools for painting a room by lamplight: a camera, lamps, lit faces, cast shadows, a few materials.

These are the helpers of home_living_room.py (the shared library has only landscape tools). The idea:
every surface is given its LOCAL color (wood, cloth, paper), and the lamps of the room then light it
where it stands, so that each lamp makes one warm pool on floor, wall and furniture alike, and what
no lamp reaches stays cool and dark.

World measurements are centimetres, as in persp.py: x to the right of the middle of the room, y UP
from the floor, z away from us."""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import *
from persp import Camera

W, H = 800, 600
SHAPE = (H, W)
HZ, FULL = -150, 585                       # the game's depth numbers for this room
WALL_Y = 385                               # the picture row where the back wall meets the floor
cam = Camera(HZ, FULL)
VX, VY, FO, EYE, Z0 = cam.vx, cam.vy, cam.F, cam.eye, cam.Z0
ZW = cam.depth_at(WALL_Y)                  # how far away the back wall is (about 327 cm)
KW = cam.scale(ZW)                         # picture pixels per cm on the back wall (about 0.665)
CAM_POS = np.array([0.0, EYE, -Z0])


def P(x, y, z):
    """World -> picture."""
    return cam.pt(x, y, max(z, -Z0 * 0.8))


def on_plane(n, c, px, py):
    """Where the ray through the picture place (px, py) meets the plane n . p = c -> (x, y, z)."""
    den = n[0] * (px - VX) / FO - n[1] * (py - VY) / FO + n[2]
    den = np.where(np.abs(den) < 1e-6, 1e-6, den)
    D = (c - n[1] * EYE + n[2] * Z0) / den
    return (px - VX) * D / FO, EYE - (py - VY) * D / FO, D - Z0


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


# ---------------------------------------------------------------- lamps
class Lamp:
    """A lamp with a shade. `down` and `up` are the cones of bare light out of the bottom and the top of the
    shade: (full inside this angle, nothing outside this one, strength). `side` is what comes through
    the shade itself. `facing` makes a flat light that only shines one way (a screen, a window)."""

    def __init__(self, name, pos, color, power, down=None, up=None, side=0.0, r0=35.0, facing=None, wrap=0.22,
                 bounce=0.0, reach=260.0):
        self.name, self.pos = name, np.asarray(pos, dtype=float)
        self.x, self.y, self.z = pos
        self.color, self.power = col(color), power
        self.down, self.up, self.side, self.r0, self.facing, self.wrap = down, up, side, r0, facing, wrap
        self.bounce, self.reach = bounce, reach

    def at(self, X, Y, Z, n, low=1.0):
        """How much of this lamp's light falls on a surface at (X, Y, Z) that faces along n.
        `low` (0 to 1) thins what comes through and under the shade, for the walls high up."""
        vx, vy, vz = self.x - X, self.y - Y, self.z - Z
        d2 = vx * vx + vy * vy + vz * vz
        d = np.sqrt(d2) + 1e-6
        ux, uy, uz = vx / d, vy / d, vz / d
        cosn = np.clip((n[0] * ux + n[1] * uy + n[2] * uz) * (1 - self.wrap) + self.wrap, 0, 1)
        g = self.side
        if self.down:
            g = g + self.down[2] * step(math.cos(math.radians(self.down[1])), math.cos(math.radians(self.down[0])), uy)
        if self.facing is not None:
            f = self.facing
            g = g * np.clip(-(f[0] * ux + f[1] * uy + f[2] * uz), 0, 1) ** f[3]
        else:
            g = g * low
        if self.up:
            g = g + self.up[2] * step(math.cos(math.radians(self.up[1])), math.cos(math.radians(self.up[0])), -uy)
        return self.power * g * cosn / (d2 / 1e4 + (self.r0 / 100.0) ** 2)

    def fill(self, X, Y, Z):
        """Light of this lamp come back off the floor and walls: soft, from nowhere, dying with distance."""
        d = np.sqrt((self.x - X) ** 2 + (self.y - Y) ** 2 + (self.z - Z) ** 2)
        return self.bounce * np.exp(-d / self.reach)


class Lights:
    def __init__(self, lamps, cool, expo=1.15, high=(190.0, 330.0, 0.80)):
        """`cool` is the light of the night that is everywhere. `high`: above the first height the
        lamplight thins, and by the second only (1 - third) of it is left: shaded lamps leave the
        top of a room dark."""
        self.lamps, self.cool, self.expo, self.high = lamps, col(cool), expo, high

    def lamp(self, name):
        return next(l for l in self.lamps if l.name == name)

    def light(self, X, Y, Z, n, shadows=None, only=None, bounce=1.0):
        """All the light at a place, as color (..., 3). `shadows` maps a lamp's name to a mask (1 = that
        lamp cannot see this place)."""
        X, Y, Z = (np.asarray(v, dtype=F32) for v in (X, Y, Z))
        out = np.zeros(np.broadcast(X, Y, Z).shape + (3,), dtype=F32)
        out += self.cool * (0.80 + 0.20 * n[1])
        low = 1 - self.high[2] * step(self.high[0], self.high[1], Y)
        for l in self.lamps:
            if only is not None and l.name not in only:
                continue
            e = l.at(X, Y, Z, n, low)
            if shadows is not None and l.name in shadows:
                e = e * (1 - shadows[l.name])
            if l.bounce:
                e = e + l.fill(X, Y, Z) * bounce * low
            out += np.asarray(e, dtype=F32)[..., None] * l.color
        return out

    def tone(self, c):
        """Light times local color -> paint. Bright things run toward white instead of clipping, and
        what is left in the dark leans to blue-violet, as night shadows do beside lamplight."""
        t = (1 - np.exp(-self.expo * np.clip(c, 0, None))).astype(F32)
        lum = t @ np.array([0.3, 0.55, 0.15], dtype=F32)
        k = np.clip(1 - lum, 0, 1) ** 2.4
        t = t + np.asarray(k)[..., None] * np.array([-0.030, -0.006, 0.050], dtype=F32)
        return np.clip(t, 0, 1).astype(F32)

    def paint(self, albedo, pos, n, dim=1.0):
        """The color of one small thing of local color `albedo` at `pos` facing `n` (no cast shadows)."""
        return self.tone(col(albedo) * self.light(pos[0], pos[1], pos[2], n) * dim)


# ---------------------------------------------------------------- layers and faces
class Layer:
    """A picture and its coverage: the backdrop (all covered) or a cut-out (clear to begin with).
    `w` is how much paint is on each pixel (rgb holds color times that); `a` is the outline."""

    def __init__(self, rgb_=None):
        if rgb_ is None:
            self.rgb = np.zeros((H, W, 3), dtype=F32)
            self.a = np.zeros((H, W), dtype=F32)
            self.w = np.zeros((H, W), dtype=F32)
        else:
            self.rgb = rgb_
            self.a = np.ones((H, W), dtype=F32)
            self.w = np.ones((H, W), dtype=F32)

    def put(self, color, mask):
        """Lay a whole-picture color (or picture) on through a mask."""
        over(self.rgb, color, mask)
        self.a = np.maximum(self.a, mask)
        self.w = self.w * (1 - mask) + mask

    def sheet(self, sheet, amount=1.0, hide=None):
        c, a = sheet.done()
        a = a * amount
        if hide is not None:
            a = a * (1 - hide)
        self.put(c, a)

    def true(self):
        """The colors themselves (not thinned toward black at the soft edges)."""
        return self.rgb / np.maximum(self.w, 1e-3)[..., None]

    def onto(self, other):
        other.put(self.true(), self.w)


def local_mask(pp, x0, y0, x1, y1, ss=3):
    im = Image.new("L", ((x1 - x0) * ss, (y1 - y0) * ss), 0)
    ImageDraw.Draw(im).polygon([((x - x0) * ss, (y - y0) * ss) for x, y in pp], fill=255)
    return np.asarray(im.resize((x1 - x0, y1 - y0), Image.BOX), dtype=F32) / 255


def grow(pp, by):
    """Push a polygon's corners out from its middle by `by` pixels, so neighbouring faces overlap a hair."""
    cx = sum(p[0] for p in pp) / len(pp)
    cy = sum(p[1] for p in pp) / len(pp)
    out = []
    for x, y in pp:
        d = math.hypot(x - cx, y - cy) + 1e-6
        out.append((x + (x - cx) / d * by, y + (y - cy) / d * by))
    return out


def normal_of(pts):
    a, b, c = (np.asarray(p, dtype=float) for p in pts[:3])
    n = np.cross(b - a, c - a)
    k = np.linalg.norm(n)
    if k < 1e-9:
        return np.array([0.0, 1.0, 0.0])
    n = n / k
    if np.dot(n, CAM_POS - a) < 0:
        n = -n
    return n


def face(L, lights, pts, albedo, n=None, dim=1.0, shadows=None, emit=None, lit=True, alpha=1.0, pad=0.35, only=None, bounce=1.0):
    """Paint one flat face of something (a polygon in the world) with its local color, lit by the lamps.

    `albedo` is a color, or a function (X, Y, Z) -> colors for wood grain and the like. `dim` darkens it
    (a number, or a function (X, Y, Z) -> numbers) where something stands in the light's way.
    Returns (mask, (x0, y0, x1, y1)) of what was painted, or None if it is out of the picture."""
    pp = [P(*p) for p in pts]
    if pad:
        pp = grow(pp, pad)
    x0 = max(0, int(math.floor(min(p[0] for p in pp))) - 1)
    x1 = min(W, int(math.ceil(max(p[0] for p in pp))) + 2)
    y0 = max(0, int(math.floor(min(p[1] for p in pp))) - 1)
    y1 = min(H, int(math.ceil(max(p[1] for p in pp))) + 2)
    if x1 <= x0 or y1 <= y0:
        return None
    m = local_mask(pp, x0, y0, x1, y1) * alpha
    if m.max() <= 0:
        return None
    if n is None:
        n = normal_of(pts)
    n = np.asarray(n, dtype=float)
    c = float(np.dot(n, np.asarray(pts[0], dtype=float)))
    py, px = np.mgrid[y0:y1, x0:x1].astype(F32)
    X, Y, Z = on_plane(n, c, px + 0.5, py + 0.5)
    a = albedo(X, Y, Z) if callable(albedo) else col(albedo)
    if lit:
        sh = None if shadows is None else {k: v[y0:y1, x0:x1] for k, v in shadows.items()}
        light = lights.light(X, Y, Z, n, sh, only=only, bounce=bounce)
        d = dim(X, Y, Z) if callable(dim) else dim
        if not np.isscalar(d):
            d = np.asarray(d, dtype=F32)[..., None]
        c_ = lights.tone(a * light * d)
    else:
        c_ = np.broadcast_to(a, (y1 - y0, x1 - x0, 3)).astype(F32)
    if emit is not None:
        e = emit(X, Y, Z) if callable(emit) else col(emit)
        c_ = np.clip(c_ + e, 0, 1)
    sl = (slice(y0, y1), slice(x0, x1))
    L.rgb[sl] = L.rgb[sl] * (1 - m[..., None]) + c_ * m[..., None]
    L.a[sl] = np.maximum(L.a[sl], m)
    L.w[sl] = L.w[sl] * (1 - m) + m
    return m, (x0, y0, x1, y1)


def turn(cx, cz, x, z, ang):
    """Turn a place on the floor about (cx, cz) by `ang` degrees (positive turns the front to the right)."""
    a = math.radians(ang)
    dx, dz = x - cx, z - cz
    return cx + dx * math.cos(a) - dz * math.sin(a), cz + dx * math.sin(a) + dz * math.cos(a)


def corners(x0, x1, y0, y1, z0, z1, ang=0.0, about=None):
    """The eight corners of a box, turned about a point on the floor if asked: bottom four, then top four."""
    cx, cz = about if about is not None else ((x0 + x1) / 2, (z0 + z1) / 2)
    ring = [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]
    if ang:
        ring = [turn(cx, cz, x, z, ang) for x, z in ring]
    return [(x, y0, z) for x, z in ring] + [(x, y1, z) for x, z in ring]


def box(L, lights, x0, x1, y0, y1, z0, z1, color, top=None, front=None, side=None, ang=0.0, about=None, **kw):
    """A box standing in the room: the faces we can see, each lit where it is. `color` is the local color of
    every face unless `top`, `front` or `side` say otherwise (the front is the face at z0)."""
    c = corners(x0, x1, y0, y1, z0, z1, ang, about)
    b, t = c[:4], c[4:]
    faces = [("front", [b[0], b[1], t[1], t[0]]), ("right", [b[1], b[2], t[2], t[1]]), ("back", [b[2], b[3], t[3], t[2]]),
             ("left", [b[3], b[0], t[0], t[3]]), ("top", [t[0], t[1], t[2], t[3]])]
    mid = np.mean(np.asarray(c, dtype=float), axis=0)
    for name, pts in faces:
        fm = np.mean(np.asarray(pts, dtype=float), axis=0)
        n = normal_of(pts)
        out = fm - mid
        if np.dot(n, out) < 0:
            n = -n
        if np.dot(n, CAM_POS - fm) <= 1e-6:
            continue                                          # it faces away from us
        a = color
        if name == "top" and top is not None:
            a = top
        elif name == "front" and front is not None:
            a = front
        elif name in ("left", "right", "back") and side is not None:
            a = side
        face(L, lights, pts, a, n=n, **kw)
    return c


# ---------------------------------------------------------------- cast shadows
def hull(points):
    pts = sorted(set((round(float(x), 2), round(float(y), 2)) for x, y in points))
    if len(pts) < 3:
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


class Shadows:
    """For each lamp, the places on the floor and on the back wall that it cannot see, because a piece of
    furniture stands in the way. Each piece is given as boxes (their eight corners)."""

    def __init__(self, lamps, ss=2):
        self.lamps, self.ss = lamps, ss
        self.floor = {l.name: Image.new("L", (W * ss, H * ss), 0) for l in lamps}
        self.wall = {l.name: Image.new("L", (W * ss, H * ss), 0) for l in lamps}

    def add(self, cs, reach=5.0, lamps=None, wall=True, strength=1.0):
        s = self.ss
        v = int(255 * strength)
        for l in self.lamps:
            if lamps is not None and l.name not in lamps:
                continue
            if min(c[1] for c in cs) >= l.y:
                continue                                      # the whole thing is above the lamp
            q = []
            for (x, y, z) in cs:
                t = l.y / max(l.y - y, l.y / reach)
                q.append(P(l.x + (x - l.x) * t, 0.0, l.z + (z - l.z) * t))
            hp = hull(q)
            if len(hp) >= 3:
                ImageDraw.Draw(self.floor[l.name]).polygon([(x * s, y * s) for x, y in hp], fill=v)
            if not wall or max(c[2] for c in cs) <= l.z + 2:
                continue
            q = []
            for (x, y, z) in cs:
                t = min((ZW - l.z) / max(z - l.z, (ZW - l.z) / reach), reach)
                q.append(P(l.x + (x - l.x) * t, max(l.y + (y - l.y) * t, -40.0), ZW))
            hp = hull(q)
            if len(hp) >= 3:
                ImageDraw.Draw(self.wall[l.name]).polygon([(x * s, y * s) for x, y in hp], fill=v)

    def done(self, soft):
        """-> two dictionaries of masks (floor, wall). `soft` maps a lamp's name to how blurred its shadows
        are. On the floor a shadow is crisp near the lamp that throws it and loose far away, as real ones are."""
        px, py = grid((H, W))

        def get(im, name, lamp=None):
            m = np.asarray(im.resize((W, H), Image.BOX), dtype=F32) / 255
            s0 = soft.get(name, 3.0)
            if lamp is None:
                return np.clip(blur(m, s0), 0, 1)
            fx, fy = P(lamp.x, 0.0, lamp.z)
            far = np.clip(np.hypot(px - fx, (py - fy) * 1.5) / 260.0, 0, 1)
            return np.clip(lerp(blur(m, s0 * 0.55), blur(m, s0 * 2.6), far), 0, 1)
        by = {l.name: l for l in self.lamps}
        return ({k: get(v, k, by[k]) for k, v in self.floor.items()}, {k: get(v, k) for k, v in self.wall.items()})


# ---------------------------------------------------------------- materials (local color, in world measurements)
_TILES = {}


def wnoise(u, v, cell, seed, octaves=3):
    """Noise laid on a surface: `u`, `v` are places on it in cm, `cell` the size of the blotches in cm
    (a number, or (along u, along v))."""
    key = (cell if np.isscalar(cell) else tuple(cell), seed, octaves)
    if key not in _TILES:
        _TILES[key] = noise((512, 512), cell, seed, octaves)
    t = _TILES[key]
    return sample(t, np.mod(u, 509.0), np.mod(v, 509.0))


def hash01(i, j, seed=0.0):
    """One repeatable random number (0 to 1) for each whole-number place (i, j)."""
    h = np.sin(i * 127.1 + j * 311.7 + seed * 74.7) * 43758.5453
    return (h - np.floor(h)).astype(F32)


def wood(along, across, base, dark, seed, plank=12.0, length=140.0, gap=0.22, tone=0.16, grain=0.10):
    """Boards: `along` runs the length of them and `across` over them (cm). -> colors.
    Each board has its own tone, butt joints at its own places, and a grain that runs along it."""
    i = np.floor(across / plank)
    f = across / plank - i
    shift = hash01(i, 3.0, seed) * length
    j = np.floor((along + shift) / length)
    g = (along + shift) / length - j
    t = hash01(i, j, seed + 1.0) - 0.5
    c = col(base)[None, None, :] * (1 + t[..., None] * 2 * tone)
    c = c * (1 + ((wnoise(along, across * 7.0, (90, 9), int(seed) + 5) - 0.5) * 2 * grain)[..., None])
    warm = (hash01(i, j, seed + 2.0) - 0.5) * 0.05
    c[..., 0] += warm
    c[..., 2] -= warm
    joint = np.maximum(step(1 - gap / plank * 1.6, 1.0, f) + step(gap / plank * 1.6, 0.0, f) * 0.5,
                       step(1 - gap / length * 2.2, 1.0, g))
    return lerp(c, col(dark)[None, None, :], np.clip(joint, 0, 1)[..., None] * 0.75).astype(F32)


def grainy(base, seed, along="x", amount=0.10, cell=(60, 5)):
    """A plain piece of wood (a table top, a panel): its color with grain running along x, y or z."""
    b = col(base)

    def f(X, Y, Z):
        u, v = {"x": (X, Y + Z), "y": (Y, X + Z), "z": (Z, X + Y)}[along]
        n = wnoise(u, v * 3.0, cell, seed) - 0.5
        return b[None, None, :] * (1 + n[..., None] * 2 * amount)
    return f


def mottled(base, seed, amount=0.06, cell=30):
    """A plain painted or plastered surface, a little uneven."""
    b = col(base)

    def f(X, Y, Z):
        n = wnoise(X + Z * 0.7, Y + Z * 0.5, cell, seed) - 0.5
        return b[None, None, :] * (1 + n[..., None] * 2 * amount)
    return f


def edge_weight(crisp, gain=7.0, top=0.9, spread=0.6):
    """Where a picture has hard edges (0 to `top`): used to put the built things back crisply after the
    brush has been over them, while the open surfaces keep their brushwork."""
    lum = crisp @ np.array([0.3, 0.55, 0.15], dtype=F32)
    gy, gx = np.gradient(lum)
    e = np.hypot(gx, gy)
    e = np.maximum(e, blur(e, spread))
    return np.clip(e * gain, 0, top).astype(F32)


def hand(a, amount=0.7, cell=26.0, seed=41):
    """The same slight wander for every layer of the scene, so ruled lines look drawn by hand and the
    cut-outs still fit the backdrop to the pixel."""
    h, w = a.shape[:2]
    x, y = grid((h, w))
    dx = (noise((h, w), cell, seed, 2) - 0.5) * 2 * amount
    dy = (noise((h, w), cell, seed + 1, 2) - 0.5) * 2 * amount
    return sample(a, x + dx, y + dy)

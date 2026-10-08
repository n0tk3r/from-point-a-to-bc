"""The living room painter's own tools.

Everything in the room is laid in as flat pieces (polygons) that stand in the ROOM, in centimetres, and every
piece goes through the one camera (room.View). A piece is filled pixel by pixel: for each pixel we know the
place in the room it shows (X, Y, Z), so its paint (boards, paper, cloth) is laid in its own measurements and
its light is worked out from where the lamps stand. Nearer pieces cover farther ones (a depth sheet), so
nothing has to be sorted by hand and nothing can be drawn "from another place".

    cam   = Cam(view)                       the rays of the picture (painted at twice the size, then reduced)
    lay   = Layer(cam)                      a sheet of paint with its own depth
    lay.poly(points, paint)                 a flat piece; `paint(X, Y, Z, n, iy, ix) -> colors`
    lay.box(...), lay.lathe(...), lay.ribbon(...), lay.disc(...)
    lamps = Lamps(cam)                      the light of the room: warm lamps, the kitchen door, the moon
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, rgb, lerp, blur, noise, resize, grain, palette_of, to_palette, save, strokes, over

SS = 2                                                      # the room is painted at twice the size and reduced


# ---------------------------------------------------------------- small things
def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


def sstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0 + 1e-9), 0, 1)
    return t * t * (3 - 2 * t)


def hash2(i, j, seed=0.0):
    h = np.sin(np.asarray(i, dtype=np.float64) * 127.1 + np.asarray(j, dtype=np.float64) * 311.7 + seed * 74.7) * 43758.5453
    return (h - np.floor(h)).astype(F32)


def vnoise(u, v, seed=0.0):
    """Smooth noise 0..1 at places (u, v): one blob per unit."""
    u = np.asarray(u, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    iu, iv = np.floor(u), np.floor(v)
    fu, fv = u - iu, v - iv
    fu = fu * fu * (3 - 2 * fu)
    fv = fv * fv * (3 - 2 * fv)
    a, b = hash2(iu, iv, seed), hash2(iu + 1, iv, seed)
    c, d = hash2(iu, iv + 1, seed), hash2(iu + 1, iv + 1, seed)
    return (a + (b - a) * fu + (c - a) * fv + (a - b - c + d) * fu * fv).astype(F32)


def fbm(u, v, seed=0.0, octaves=3):
    out, w, tot = 0.0, 1.0, 0.0
    for k in range(octaves):
        out = out + w * vnoise(u * (2 ** k), v * (2 ** k), seed + k * 3.1)
        tot += w
        w *= 0.5
    return out / tot


def rot(pivot, deg):
    """A turn about an upright line through `pivot` (X, Z): -> function of a room point."""
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    px, pz = pivot

    def tf(p):
        x, y, z = p
        dx, dz = x - px, z - pz
        return (px + dx * c - dz * s, y, pz + dx * s + dz * c)
    return tf


def normal_of(pts):
    """Newell's normal of a flat polygon in the room."""
    nx = ny = nz = 0.0
    n = len(pts)
    for i in range(n):
        x0, y0, z0 = pts[i]
        x1, y1, z1 = pts[(i + 1) % n]
        nx += (y0 - y1) * (z0 + z1)
        ny += (z0 - z1) * (x0 + x1)
        nz += (x0 - x1) * (y0 + y1)
    l = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
    return (nx / l, ny / l, nz / l)


# ---------------------------------------------------------------- the camera's rays, and a sheet of paint with depth
class Cam:
    def __init__(self, view, ss=SS, size=(800, 600)):
        self.v, self.ss = view, ss
        self.W, self.H = size[0] * ss, size[1] * ss
        py, px = np.mgrid[0:self.H, 0:self.W].astype(F32)
        a = ((px + 0.5) / ss - view.cx) / view.F
        u = (view.hz - (py + 0.5) / ss) / view.F
        self.rX = (a * view.rx + view.fx).astype(F32)
        self.rY = u.astype(F32)
        self.rZ = (a * view.rz + view.fz).astype(F32)
        self.C = (view.cam_x, view.eye, view.cam_z)

    def plane_points(self, axis, at, step=1):
        """Where every picture pixel (at 1/step of the picture's size... of the DOUBLE size) falls on a plane:
        axis 'Y' (level, height `at`), 'X' or 'Z' (upright). -> X, Y, Z, ok"""
        rX, rY, rZ = self.rX[::step, ::step], self.rY[::step, ::step], self.rZ[::step, ::step]
        C = self.C
        with np.errstate(divide="ignore", invalid="ignore"):
            t = {"X": (at - C[0]) / rX, "Y": (at - C[1]) / rY, "Z": (at - C[2]) / rZ}[axis]
        ok = np.isfinite(t) & (t > 20)
        t = np.where(ok, t, 0).astype(F32)
        return C[0] + rX * t, C[1] + rY * t, C[2] + rZ * t, ok


class Layer:
    def __init__(self, cam):
        self.cam = cam
        self.col = np.zeros((cam.H, cam.W, 3), dtype=F32)
        self.z = np.full((cam.H, cam.W), 1e9, dtype=F32)
        self.a = np.zeros((cam.H, cam.W), dtype=F32)
        self.tag = np.zeros((cam.H, cam.W), dtype=np.uint8)
        self.tf = None                                      # a turn applied to every point laid (see rot)
        self.count = 0

    # ---- one flat piece
    def poly(self, pts, paint, tag=0, bias=0.0, n=None):
        if self.tf is not None:
            pts = [self.tf(p) for p in pts]
        cam, v, ss = self.cam, self.cam.v, self.cam.ss
        pp = v.poly(pts)
        if len(pp) < 3:
            return
        xs = [p[0] * ss for p in pp]
        ys = [p[1] * ss for p in pp]
        x0, x1 = int(max(0, math.floor(min(xs)))), int(min(cam.W, math.ceil(max(xs)) + 1))
        y0, y1 = int(max(0, math.floor(min(ys)))), int(min(cam.H, math.ceil(max(ys)) + 1))
        if x1 <= x0 or y1 <= y0:
            return
        im = Image.new("L", (x1 - x0, y1 - y0), 0)
        ImageDraw.Draw(im).polygon([(x - x0, y - y0) for x, y in zip(xs, ys)], fill=255)
        m = np.asarray(im) > 0
        if not m.any():
            return
        nn = normal_of(pts)
        C = cam.C
        if sum(nn[k] * (C[k] - pts[0][k]) for k in range(3)) < 0:      # light it from the side we see
            nn = (-nn[0], -nn[1], -nn[2])
        d = sum(nn[k] * (pts[0][k] - C[k]) for k in range(3))
        sl = (slice(y0, y1), slice(x0, x1))
        den = nn[0] * cam.rX[sl] + nn[1] * cam.rY[sl] + nn[2] * cam.rZ[sl]
        with np.errstate(divide="ignore", invalid="ignore"):
            t = d / den
        ok = m & np.isfinite(t) & (t > 20) & (t < self.z[sl] + bias)
        if not ok.any():
            return
        iy, ix = np.nonzero(ok)
        tt = t[ok].astype(F32)
        X = C[0] + cam.rX[sl][ok] * tt
        Y = C[1] + cam.rY[sl][ok] * tt
        Z = C[2] + cam.rZ[sl][ok] * tt
        c = paint(X, Y, Z, nn if n is None else n, iy + y0, ix + x0)
        self.col[sl][ok] = c
        self.z[sl][ok] = tt
        self.a[sl][ok] = 1.0
        if tag is not None:
            self.tag[sl][ok] = tag
        self.count += 1

    # ---- solids made of flat pieces
    def box(self, X0, X1, Y0, Y1, Z0, Z1, paint, tag=0, skip=(), paints=None, sh=False):
        """A box. `paints` may give another paint for a face by name: top, bottom, left, right, back, front."""
        faces = {
            "top": [(X0, Y1, Z0), (X1, Y1, Z0), (X1, Y1, Z1), (X0, Y1, Z1)],
            "bottom": [(X0, Y0, Z0), (X1, Y0, Z0), (X1, Y0, Z1), (X0, Y0, Z1)],
            "left": [(X0, Y0, Z0), (X0, Y0, Z1), (X0, Y1, Z1), (X0, Y1, Z0)],
            "right": [(X1, Y0, Z0), (X1, Y0, Z1), (X1, Y1, Z1), (X1, Y1, Z0)],
            "back": [(X0, Y0, Z0), (X1, Y0, Z0), (X1, Y1, Z0), (X0, Y1, Z0)],
            "front": [(X0, Y0, Z1), (X1, Y0, Z1), (X1, Y1, Z1), (X0, Y1, Z1)],
        }
        for name, pts in faces.items():
            if name in skip:
                continue
            self.poly(pts, (paints or {}).get(name, paint), tag)

    def prism(self, outline, Y0, Y1, paint, tag=0, top=None, cap=True):
        """An upright prism: `outline` is its plan [(X, Z), ...]; sides, and the top if `cap`."""
        n = len(outline)
        for i in range(n):
            (xa, za), (xb, zb) = outline[i], outline[(i + 1) % n]
            self.poly([(xa, Y0, za), (xb, Y0, zb), (xb, Y1, zb), (xa, Y1, za)], paint, tag)
        if cap:
            self.poly([(x, Y1, z) for x, z in outline], top or paint, tag)

    def extrude_x(self, profile, xa, xb, paint, tag=0, caps=True, cap_paint=None):
        """A side view drawn as [(Z, Y), ...] and pushed through from X = xa to xb (a seat and its back, a roof)."""
        n = len(profile)
        for i in range(n):
            (za, ya), (zb, yb) = profile[i], profile[(i + 1) % n]
            self.poly([(xa, ya, za), (xb, ya, za), (xb, yb, zb), (xa, yb, zb)], paint, tag)
        if caps:
            for x in (xa, xb):
                self.poly([(x, y, z) for z, y in profile], cap_paint or paint, tag)

    def extrude_z(self, profile, za, zb, paint, tag=0, caps=True, cap_paint=None):
        """A front view drawn as [(X, Y), ...] and pushed through from Z = za to zb (a rolled arm, a moulding)."""
        n = len(profile)
        for i in range(n):
            (xa, ya), (xb, yb) = profile[i], profile[(i + 1) % n]
            self.poly([(xa, ya, za), (xa, ya, zb), (xb, yb, zb), (xb, yb, za)], paint, tag)
        if caps:
            for z in (za, zb):
                self.poly([(x, y, z) for x, y in profile], cap_paint or paint, tag)

    def lathe(self, cx, cz, profile, paint, tag=0, sides=14, smooth=True, a0=0.0, a1=360.0):
        """A turned thing about an upright line: `profile` is [(radius, height), ...] from the bottom up.
        With `smooth` the light is worked out for a round surface, not for its flat facets."""
        for (r0, y0), (r1, y1) in zip(profile[:-1], profile[1:]):
            slope = (r0 - r1) / (abs(y1 - y0) + 1e-6)                    # how much the surface faces up
            for k in range(sides):
                p, q = math.radians(a0 + (a1 - a0) * k / sides), math.radians(a0 + (a1 - a0) * (k + 1) / sides)
                pts = [(cx + math.cos(p) * r0, y0, cz + math.sin(p) * r0), (cx + math.cos(q) * r0, y0, cz + math.sin(q) * r0),
                       (cx + math.cos(q) * r1, y1, cz + math.sin(q) * r1), (cx + math.cos(p) * r1, y1, cz + math.sin(p) * r1)]
                if abs(r0) < 1e-6:
                    pts = [pts[0], pts[2], pts[3]]
                elif abs(r1) < 1e-6:
                    pts = pts[:3]
                if smooth:
                    self.poly(pts, _Round(paint, cx, cz, slope, self.tf), tag)
                else:
                    self.poly(pts, paint, tag)

    def disc(self, centre, r, paint, tag=0, axis="Y", sides=18, squash=1.0):
        cx, cy, cz = centre
        pts = []
        for k in range(sides):
            a = 2 * math.pi * k / sides
            c, s = math.cos(a) * r, math.sin(a) * r * squash
            pts.append({"Y": (cx + c, cy, cz + s), "Z": (cx + c, cy + s, cz), "X": (cx, cy + s, cz + c)}[axis])
        self.poly(pts, paint, tag)

    def ribbon(self, P, Q, w0, w1, paint, tag=0, bias=0.0):
        """A thin thing seen as a strip that always faces us (a cord, a rod, a spindle): widths in cm."""
        if self.tf is not None:
            P, Q = self.tf(P), self.tf(Q)
        v = self.cam.v
        ln = v.line(P, Q)
        if not ln:
            return
        (ax, ay), (bx, by) = ln
        dx, dy = bx - ax, by - ay
        l = math.hypot(dx, dy)
        if l < 1e-6:
            return
        px, py = -dy / l, dx / l                              # across the strip, in the picture
        up = (0.0, 1.0, 0.0)
        right = (v.rx, 0.0, v.rz)
        # picture y runs down: a step of (px, py) in the picture is (px along right, -py along up) in the room
        off = tuple(px * right[k] - py * up[k] for k in range(3))
        a = [tuple(P[k] + off[k] * w0 / 2 for k in range(3)), tuple(P[k] - off[k] * w0 / 2 for k in range(3))]
        b = [tuple(Q[k] - off[k] * w1 / 2 for k in range(3)), tuple(Q[k] + off[k] * w1 / 2 for k in range(3))]
        keep, self.tf = self.tf, None
        self.poly(a + b, paint, tag, bias=bias, n=(-v.fx, 0.25, -v.fz))
        self.tf = keep

    def tube(self, pts, w, paint, tag=0):
        """A bent rod or cord through several room points (each straight piece a ribbon)."""
        for p, q in zip(pts[:-1], pts[1:]):
            self.ribbon(p, q, w, w, paint, tag)

    # ---- the finished sheet at the picture's own size
    def done(self):
        ss = self.cam.ss
        h, w = self.cam.H // ss, self.cam.W // ss
        c = self.col.reshape(h, ss, w, ss, 3)
        a = self.a.reshape(h, ss, w, ss)
        asum = a.sum(axis=(1, 3))
        color = (c * a[..., None]).sum(axis=(1, 3)) / np.maximum(asum, 1e-6)[..., None]
        return color.astype(F32), (asum / (ss * ss)).astype(F32)

    def tags(self):
        return self.tag[::self.cam.ss, ::self.cam.ss]

    def depth(self):
        return self.z[::self.cam.ss, ::self.cam.ss]


class _Round:
    """Paint for a turned surface: the same paint, lit as a round thing."""

    def __init__(self, paint, cx, cz, slope, tf):
        self.paint, self.slope = paint, slope
        self.cx, self.cz = (cx, cz) if tf is None else (tf((cx, 0, cz))[0], tf((cx, 0, cz))[2])

    def __call__(self, X, Y, Z, n, iy, ix):
        dx, dz = X - self.cx, Z - self.cz
        l = np.sqrt(dx * dx + dz * dz) + 1e-6
        k = 1.0 / math.sqrt(1 + self.slope * self.slope)
        return self.paint(X, Y, Z, (dx / l * k, np.full_like(X, self.slope * k), dz / l * k), iy, ix)


# ---------------------------------------------------------------- the light of the room
class Lamps:
    """Warm lamps that stand at places in the room, the kitchen's light coming through its doorway, the moon
    coming through the tall window, and the cool dark that is left where none of them reach."""

    def __init__(self, cam):
        self.cam = cam
        self.lamps = []
        self.boxes = []                                       # things that throw shadows: (X0, X1, Y0, Y1, Z0, Z1)
        self.maps = {}                                        # baked shadows: plane name -> {lamp id: picture-sized sheet}
        self.cool = col((0.085, 0.105, 0.20))                 # the night that fills the room
        self.warm = col((0.20, 0.135, 0.075))                 # lamplight that has bounced about the lower room
        self.moon = None
        self.gain = 1.0

    def lamp(self, id, at, color, power, reach=150.0, down=0.6, up=0.3, side=0.4, fill=0.22, door=None, throws=True):
        """`down`, `up`, `side`: how much of the lamp's light leaves it downward, upward, and through the shade.
        `door` = (axis, at, u0, u1, v0, v1): the light only passes through this opening in a wall."""
        self.lamps.append(dict(id=id, at=tuple(float(a) for a in at), color=col(color), power=power, reach=reach, down=down, up=up,
                               side=side, fill=fill, door=door, throws=throws))

    def set_moon(self, toward, color, power, window):
        """`toward`: the way to the moon from inside the room. `window` = (Z0, Z1, Y0, Y1, bars_z, bars_y, bar) on the wall X = 0."""
        t = np.asarray(toward, dtype=np.float64)
        self.moon = dict(dir=tuple(t / np.linalg.norm(t)), color=col(color), power=power, window=window)

    # ---- is the way from a place to a lamp clear?
    @staticmethod
    def clear(X, Y, Z, L, boxes, lift=1.5):
        dx, dy, dz = L[0] - X, L[1] - Y, L[2] - Z
        vis = np.ones(X.shape, dtype=bool)
        tiny = 1e-5
        dx = np.where(np.abs(dx) < tiny, tiny, dx)
        dy = np.where(np.abs(dy) < tiny, tiny, dy)
        dz = np.where(np.abs(dz) < tiny, tiny, dz)
        d = np.sqrt(dx * dx + dy * dy + dz * dz)
        s0 = lift / d                                          # do not let a surface shade itself
        for (x0, x1, y0, y1, z0, z1) in boxes:
            ta, tb = (x0 - X) / dx, (x1 - X) / dx
            lo, hi = np.minimum(ta, tb), np.maximum(ta, tb)
            ta, tb = (y0 - Y) / dy, (y1 - Y) / dy
            lo, hi = np.maximum(lo, np.minimum(ta, tb)), np.minimum(hi, np.maximum(ta, tb))
            ta, tb = (z0 - Z) / dz, (z1 - Z) / dz
            lo, hi = np.maximum(lo, np.minimum(ta, tb)), np.minimum(hi, np.maximum(ta, tb))
            vis &= ~((hi > np.maximum(lo, s0)) & (lo < 0.985))
        return vis

    @staticmethod
    def through(X, Y, Z, L, door, soft=4.0):
        """How much of the way from a place to a lamp passes through an opening in a wall (0..1, soft edged)."""
        axis, at, u0, u1, v0, v1 = door
        if axis == "Z":
            den = L[2] - Z
            den = np.where(np.abs(den) < 1e-5, 1e-5, den)
            s = (at - Z) / den
            u = X + (L[0] - X) * s
        else:
            den = L[0] - X
            den = np.where(np.abs(den) < 1e-5, 1e-5, den)
            s = (at - X) / den
            u = Z + (L[2] - Z) * s
        w = Y + (L[1] - Y) * s
        inside = sstep(u0 - soft, u0 + soft, u) * sstep(u1 + soft, u1 - soft, u) * sstep(v1 + soft, v1 - soft, w) * (w > v0 - 1)
        same_side = (s <= 0) | (s >= 1)                         # the place is on the lamp's own side of the wall
        return np.where(same_side, 1.0, inside).astype(F32)

    def moonlight(self, X, Y, Z, n):
        """The moon through the window: lit only where the way to the moon passes through a pane."""
        m = self.moon
        if m is None:
            return 0.0
        dx, dy, dz = m["dir"]
        Z0, Z1, Y0, Y1, bars_z, bars_y, bar = m["window"]
        s = -X / dx                                             # the way to the moon meets the wall X = 0 here
        zz, yy = Z + dz * s, Y + dy * s
        soft = 2.0 + s * 0.012
        g = sstep(Z0 - soft, Z0 + soft, zz) * sstep(Z1 + soft, Z1 - soft, zz) * sstep(Y0 - soft, Y0 + soft, yy) * sstep(Y1 + soft, Y1 - soft, yy)
        for b in bars_z:
            g = g * (1 - sstep(bar + soft, bar - soft * 0.5, np.abs(zz - b)) * 0.92)
        for b in bars_y:
            g = g * (1 - sstep(bar + soft, bar - soft * 0.5, np.abs(yy - b)) * 0.92)
        ndl = np.clip(n[0] * dx + n[1] * dy + n[2] * dz, 0, 1)
        return (g * (s > 0) * ndl * m["power"]).astype(F32)

    # ---- shadows worked out once for a whole wall or floor, softened, and kept
    def bake(self, name, axis, at, boxes=None, only=None, soft=1.6, spread=7.0, cache=None):
        import hashlib, pickle
        boxes = self.boxes if boxes is None else boxes
        key = hashlib.md5(pickle.dumps((name, axis, at, boxes, only, soft, spread, [(l["id"], l["at"]) for l in self.lamps],
                                         self.cam.W, self.cam.H, self.cam.C))).hexdigest()[:12]
        path = None if cache is None else os.path.join(cache, f"shade-{name}-{key}.npz")
        if path and os.path.exists(path):
            z = np.load(path)
            self.maps[name] = {k: z[k] for k in z.files}
            return
        step = self.cam.ss * 2                                  # shadows are soft: half the picture's size is plenty
        X, Y, Z, ok = self.cam.plane_points(axis, at, step)
        h1, w1 = self.cam.H // self.cam.ss, self.cam.W // self.cam.ss
        out = {}
        rng = np.random.default_rng(5)
        for l in self.lamps:
            if not l["throws"] or (only is not None and l["id"] not in only):
                continue
            acc = np.zeros(X.shape, dtype=F32)
            offs = [(0, 0, 0), (spread, 0, spread * 0.6), (-spread, 0, -spread * 0.6), (spread * 0.5, spread * 0.5, -spread), (-spread * 0.5, -spread * 0.5, spread)]
            for o in offs:
                L = (l["at"][0] + o[0], l["at"][1] + o[1], l["at"][2] + o[2])
                acc += self.clear(X, Y, Z, L, boxes)
            acc /= len(offs)
            acc = blur(acc, soft)
            out[l["id"]] = np.clip(resize(acc, (h1, w1)), 0, 1).astype(F32)
        self.maps[name] = out
        if path:
            np.savez_compressed(path, **out)

    def bake_moon(self, name, axis, at, boxes, soft=0.45):
        """What stands between a floor (or wall) and the moon: worked out at the picture's own size, and kept sharp,
        because the moon throws the banister's own thin shadows."""
        X, Y, Z, ok = self.cam.plane_points(axis, at, self.cam.ss)
        dx, dy, dz = self.moon["dir"]
        far = (X + dx * 4000.0, Y + dy * 4000.0, Z + dz * 4000.0)
        vis = self.clear(X, Y, Z, far, boxes).astype(F32)
        self.maps.setdefault(name, {})["moon"] = np.clip(blur(vis, soft), 0, 1)

    # ---- the light that reaches a place
    def __call__(self, X, Y, Z, n, iy=None, ix=None, plane=None, boxes=None, warm=1.0, cool=1.0, moon=1.0, skip=()):
        nx, ny, nz = n
        out = np.zeros(X.shape + (3,), dtype=F32)
        ss = self.cam.ss
        maps = self.maps.get(plane) if plane else None
        for l in self.lamps:
            if l["id"] in skip:
                continue
            Lx, Ly, Lz = l["at"][0] - X, l["at"][1] - Y, l["at"][2] - Z
            d2 = Lx * Lx + Ly * Ly + Lz * Lz
            d = np.sqrt(d2) + 1e-6
            ndl = (nx * Lx + ny * Ly + nz * Lz) / d
            diff = np.clip((ndl + 0.18) / 1.18, 0, 1) * (1 - l["fill"]) + l["fill"] * np.clip(0.6 + 0.4 * ndl, 0, 1)
            fall = l["power"] * l["reach"] ** 2 / (l["reach"] ** 2 + d2)
            vy = -Ly / d                                        # the way the light is travelling: -1 straight down
            g = l["side"] + (l["down"] - l["side"]) * sstep(0.25, 0.85, -vy) + (l["up"] - l["side"]) * sstep(0.25, 0.85, vy)
            k = fall * g * diff
            if l["door"] is not None:
                k = k * self.through(X, Y, Z, l["at"], l["door"])
            if maps is not None and l["id"] in maps and iy is not None:
                k = k * maps[l["id"]][iy // ss, ix // ss]
            elif boxes:
                k = k * self.clear(X, Y, Z, l["at"], boxes)
            out += k[..., None] * l["color"]
        if self.moon is not None and moon:
            m = self.moonlight(X, Y, Z, n) * moon
            if maps is not None and "moon" in maps and iy is not None:
                m = m * maps["moon"][iy // ss, ix // ss]
            out += m[..., None] * self.moon["color"]
        # what is left: cool night from above and from the window, warm bounce low in the room
        low = np.clip(1.15 - Y / 300.0, 0.15, 1.0)
        up = np.asarray(ny, dtype=F32) * np.ones(X.shape, dtype=F32)
        out += (0.75 + 0.25 * up)[..., None] * (self.cool * cool)
        out += (low * warm * (0.8 - 0.2 * up))[..., None] * self.warm
        return out * self.gain


def tone(c, k=1.35, keep=0.5):
    """Light on paint -> the color on the picture: bright things roll off softly instead of clipping.
    Half of it is done on the brightness alone, so that a thing in strong light keeps its own color
    (lit leather stays red-brown; it does not bleach to cream)."""
    c = np.clip(c, 0, None)
    each = 1.0 - np.exp(-c * k)
    lum = c @ np.array([0.3, 0.55, 0.15], dtype=F32)
    scale = (1.0 - np.exp(-lum * k)) / np.maximum(lum, 1e-5)
    whole = np.clip(c * scale[..., None], 0, 1)
    return (each * (1 - keep) + whole * keep).astype(F32)


# ---------------------------------------------------------------- paints
def paint_of(lamps, albedo, plane=None, boxes=None, emit=None, warm=1.0, cool=1.0, moon=1.0, skip=(), gloss=None, mott=None, gain=1.0):
    """A paint: its own color (one color, or a function of the place) under the room's light.
    `emit`: light of its own (a lampshade, a window): a color or a function. `mott`: (sheet, amount) patchiness."""
    base = None if callable(albedo) else col(albedo)

    def paint(X, Y, Z, n, iy, ix):
        a = albedo(X, Y, Z, iy, ix) if base is None else base
        c = a * lamps(X, Y, Z, n, iy, ix, plane=plane, boxes=boxes, warm=warm, cool=cool, moon=moon, skip=skip) * gain
        if mott is not None:
            c = c * (1 + (mott[0][iy // lamps.cam.ss, ix // lamps.cam.ss] - 0.5)[..., None] * 2 * mott[1])
        if gloss is not None:
            c = c + gloss(X, Y, Z, n, iy, ix)
        if emit is not None:
            c = c + (emit(X, Y, Z, iy, ix) if callable(emit) else col(emit))
        return c
    return paint


def flat(color):
    """Paint that takes no light: for things that shine by themselves."""
    c = col(color)
    return lambda X, Y, Z, n, iy, ix: np.broadcast_to(c, X.shape + (3,))


# ---------------------------------------------------------------- lettering in whole pixels (needlework, and a clerk's hand)
# A small face of capitals seven pixels high, as a cross-stitch sampler has them: every letter is its own width.
STITCH = {
    "A": [".##.", "#..#", "#..#", "####", "#..#", "#..#", "#..#"],
    "B": ["###.", "#..#", "#..#", "###.", "#..#", "#..#", "###."],
    "C": [".###", "#...", "#...", "#...", "#...", "#...", ".###"],
    "D": ["###.", "#..#", "#..#", "#..#", "#..#", "#..#", "###."],
    "E": ["###", "#..", "#..", "##.", "#..", "#..", "###"],
    "F": ["###", "#..", "#..", "##.", "#..", "#..", "#.."],
    "G": [".###", "#...", "#...", "#.##", "#..#", "#..#", ".###"],
    "H": ["#..#", "#..#", "#..#", "####", "#..#", "#..#", "#..#"],
    "I": ["#", "#", "#", "#", "#", "#", "#"],
    "J": ["..#", "..#", "..#", "..#", "..#", "#.#", ".#."],
    "K": ["#..#", "#.#.", "##..", "#...", "##..", "#.#.", "#..#"],
    "L": ["#..", "#..", "#..", "#..", "#..", "#..", "###"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#..#", "##.#", "##.#", "#.##", "#.##", "#..#", "#..#"],
    "O": [".##.", "#..#", "#..#", "#..#", "#..#", "#..#", ".##."],
    "P": ["###.", "#..#", "#..#", "###.", "#...", "#...", "#..."],
    "R": ["###.", "#..#", "#..#", "###.", "#.#.", "#..#", "#..#"],
    "S": [".###", "#...", "#...", ".##.", "...#", "...#", "###."],
    "T": ["###", ".#.", ".#.", ".#.", ".#.", ".#.", ".#."],
    "U": ["#..#", "#..#", "#..#", "#..#", "#..#", "#..#", ".##."],
    "V": ["#...#", "#...#", "#...#", ".#.#.", ".#.#.", "..#..", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "Y": ["#.#", "#.#", "#.#", ".#.", ".#.", ".#.", ".#."],
    ",": ["..", "..", "..", "..", "..", ".#", "#."],
    " ": ["..", "..", "..", "..", "..", "..", ".."],
}
# and a smaller one, five high, for the chapter and verse
SMALL = {
    "J": ["..#", "..#", "..#", "#.#", ".#."], "O": [".#.", "#.#", "#.#", "#.#", ".#."], "S": [".##", "#..", ".#.", "..#", "##."],
    "H": ["#.#", "#.#", "###", "#.#", "#.#"], "U": ["#.#", "#.#", "#.#", "#.#", "###"], "A": [".#.", "#.#", "###", "#.#", "#.#"],
    "2": ["##.", "..#", ".#.", "#..", "###"], "4": ["#.#", "#.#", "###", "..#", "..#"], "1": [".#", "##", ".#", ".#", ".#"],
    "5": ["###", "#..", "##.", "..#", "##."], ":": [".", "#", ".", "#", "."], " ": ["..", "..", "..", "..", ".."],
}


def stitch_mask(words, face=STITCH, gap=1):
    """Words set in a pixel face -> a small sheet of 0 and 1."""
    rows = len(next(iter(face.values())))
    cols = []
    for ch in words:
        g = face[ch]
        for k in range(len(g[0])):
            cols.append([1 if g[r][k] == "#" else 0 for r in range(rows)])
        for _ in range(gap):
            cols.append([0] * rows)
    cols = cols[:-gap] if gap else cols
    return np.array(cols, dtype=F32).T


def put_mask(pic, m, x, y, color, amount=1.0, drop=None):
    """Lay a small 0/1 sheet onto the picture with its top-left at (x, y). `drop`: every that-many columns the
    line steps down one pixel (lettering on a wall that runs away from us)."""
    h, w = m.shape
    c = col(color)
    for k in range(w):
        yy = y + (int(k / drop) if drop else 0)
        colm = m[:, k]
        seg = pic[yy:yy + h, x + k]
        seg[...] = seg * (1 - colm[:, None] * amount) + c * colm[:, None] * amount
    return pic


# ---------------------------------------------------------------- the last pass
def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02, pal=None):
    g = grain(picture, seed, amount)
    if pal is None:
        sample_of = g if alpha is None else g[alpha > 0.5]
        pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)

"""A painter's kit for one dark room (rome_temple.py): sheets that really glaze, a room shell lit by
real lamps so every plane and every box answers to the same light, and the furniture of a treasury.

World measurements are centimetres, as in persp.py: x to the right of the room's middle line, y up from
the floor, z away from us. Nothing here touches the shared library."""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, lerp, rgb

UP, DOWN, TO_US, AWAY, TO_RIGHT, TO_LEFT = (0, 1, 0), (0, -1, 0), (0, 0, -1), (0, 0, 1), (1, 0, 0), (-1, 0, 0)


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


def mixc(a, b, t):
    return lerp(col(a), col(b), t)


# ---------------------------------------------------------------- sheets
class Paint:
    """A clear sheet like brush.Sheet, except that paint laid on thinly (alpha under 1) glazes what is
    already on the sheet instead of punching a hole in it."""

    def __init__(self, shape, ss=3):
        self.shape, self.ss = shape, ss
        h, w = shape
        self.im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    @staticmethod
    def _ink(color, alpha=1.0):
        c = col(color)
        return tuple(int(v) for v in np.clip(c * 255 + 0.5, 0, 255)) + (int(round(min(max(float(alpha), 0.0), 1.0) * 255)),)

    def _glaze(self, box, draw):
        W, H = self.im.size
        x0, y0 = max(0, int(math.floor(box[0])) - 2), max(0, int(math.floor(box[1])) - 2)
        x1, y1 = min(W, int(math.ceil(box[2])) + 3), min(H, int(math.ceil(box[3])) + 3)
        if x1 <= x0 or y1 <= y0:
            return
        tmp = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        draw(ImageDraw.Draw(tmp), x0, y0)
        self.im.alpha_composite(tmp, (x0, y0))

    def poly(self, points, color, alpha=1.0):
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        if len(pts) < 3:
            return self
        ink = self._ink(color, alpha)
        if alpha >= 0.999:
            self.d.polygon(pts, fill=ink)
        else:
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            self._glaze((min(xs), min(ys), max(xs), max(ys)), lambda d, ox, oy: d.polygon([(x - ox, y - oy) for x, y in pts], fill=ink))
        return self

    def line(self, points, color, width=1.0, alpha=1.0, round_ends=True):
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        if len(pts) < 2:
            return self
        wd = max(1, int(round(width * s)))
        ink = self._ink(color, alpha)

        def draw(d, ox=0, oy=0):
            q = [(x - ox, y - oy) for x, y in pts]
            d.line(q, fill=ink, width=wd, joint="curve")
            if round_ends and wd > 2:
                r = wd / 2
                for px, py in (q[0], q[-1]):
                    d.ellipse([px - r, py - r, px + r, py + r], fill=ink)
        if alpha >= 0.999:
            draw(self.d)
        else:
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            self._glaze((min(xs) - wd, min(ys) - wd, max(xs) + wd, max(ys) + wd), draw)
        return self

    def taper(self, points, color, w0, w1, alpha=1.0):
        n = len(points)
        for i in range(n - 1):
            self.line([points[i], points[i + 1]], color, lerp(w0, w1, i / max(n - 2, 1)), alpha)
        return self

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0):
        s = self.ss
        box = [(cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s]
        ink = self._ink(color, alpha)
        if alpha >= 0.999:
            self.d.ellipse(box, fill=ink)
        else:
            self._glaze(box, lambda d, ox, oy: d.ellipse([box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy], fill=ink))
        return self

    def done(self):
        h, w = self.shape
        a = np.asarray(self.im.resize((w, h), Image.BOX), dtype=F32) / 255
        return a[..., :3].astype(F32), a[..., 3].astype(F32)


class Dual:
    """Two sheets painted together. `B` takes only the big faces of things (what the brush will repaint);
    `L` takes the same faces and every small thing on top of them, in the right order, and stays crisp."""

    def __init__(self, shape, ss=3):
        self.shape = shape
        self.B, self.L = Paint(shape, ss), Paint(shape, ss)

    def poly(self, points, color, alpha=1.0, fine=False):
        if not fine:
            self.B.poly(points, color, alpha)
        self.L.poly(points, color, alpha)
        return self

    def line(self, points, color, width=1.0, alpha=1.0, fine=True, round_ends=True):
        if not fine:
            self.B.line(points, color, width, alpha, round_ends)
        self.L.line(points, color, width, alpha, round_ends)
        return self

    def taper(self, points, color, w0, w1, alpha=1.0, fine=True):
        if not fine:
            self.B.taper(points, color, w0, w1, alpha)
        self.L.taper(points, color, w0, w1, alpha)
        return self

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0, fine=False):
        if not fine:
            self.B.ellipse(cx, cy, rx, ry, color, alpha)
        self.L.ellipse(cx, cy, rx, ry, color, alpha)
        return self

    def done(self):
        """-> (faces color, faces alpha, all color, all alpha, how much `all` differs from `faces`)."""
        bc, ba = self.B.done()
        lc, la = self.L.done()
        diff = np.abs(lc * la[..., None] - bc * ba[..., None]).sum(axis=2) + np.abs(la - ba)
        return bc, ba, lc, la, np.clip(diff * 5.0, 0, 1).astype(F32)


# ---------------------------------------------------------------- the room and its light
class Room:
    """A box of a room seen through a persp.Camera, and the lamps in it. `E` is how much light arrives at
    a place facing a given way; `tone` turns a thing's own color into what we see there."""

    def __init__(self, cam, half, back, height):
        self.cam, self.A, self.ZB, self.HC = cam, float(half), float(back), float(height)
        self.lights = []
        self.ambient = np.array([0.018, 0.016, 0.026], dtype=F32)
        self.fog_near = np.array([0.064, 0.034, 0.036], dtype=F32)     # the dark is never black: warm brown near us,
        self.fog_far = np.array([0.048, 0.058, 0.096], dtype=F32)      # blue dusk at the far end

    def P(self, x, y, z):
        return self.cam.pt(x, y, z)

    def k(self, z):
        return self.cam.scale(z)

    def squash(self, y, z):
        """How flat a level circle looks at height y and depth z (its height over its width in the picture)."""
        return max(0.02, (self.cam.eye - y) * self.cam.scale(z) / self.cam.F)

    def E(self, X, Y, Z, n):
        X, Y, Z = np.asarray(X, dtype=F32), np.asarray(Y, dtype=F32), np.asarray(Z, dtype=F32)
        nx, ny, nz = n
        out = np.zeros(X.shape + (3,), dtype=F32) + self.ambient
        for L in self.lights:
            kind = L["kind"]
            if kind == "point":
                dx, dy, dz = L["at"][0] - X, L["at"][1] - Y, L["at"][2] - Z
                d2 = dx * dx + dy * dy + dz * dz + 1e-3
                c = (dx * nx + dy * ny + dz * nz) / np.sqrt(d2)
                wr = L.get("wrap", 0.2)
                c = np.clip((c + wr) / (1 + wr), 0, 1)
                R = L["reach"]
                f = R * R / (d2 + (R * L.get("core", 0.4)) ** 2)
                ly = L["at"][1]
                for (bx, bz, br, by) in L.get("discs", ()):        # a round thing between (the lamp's own pan): no light straight down
                    t = np.clip((by - Y) / np.maximum(ly - Y, 1e-3), 0, 1)
                    q = np.hypot(X + dx * t - bx, Z + dz * t - bz)
                    f = f * np.where(Y < by, np.clip((q - br * 0.5) / br, 0, 1), 1.0)
                for (x0, x1, z0, z1, by, soft) in L.get("rects", ()):   # a table top between: its shadow, soft at the edge
                    t = np.clip((by - Y) / np.maximum(ly - Y, 1e-3), 0, 1)
                    qx, qz = X + dx * t, Z + dz * t
                    out_by = np.maximum(np.maximum(x0 - qx, qx - x1), np.maximum(z0 - qz, qz - z1))
                    f = f * np.where(Y < by, np.clip(out_by / soft + 0.5, 0, 1), 1.0)
                out = out + L["rgb"] * (L["power"] * c * f)[..., None]
            elif kind == "door":                                   # the open doors behind us: sky and a sunlit square outside
                d = L["dir"]
                wr = L.get("wrap", 0.3)
                c = max((d[0] * nx + d[1] * ny + d[2] * nz + wr) / (1 + wr), 0.0)
                fz = 1.0 / (1.0 + (np.maximum(Z + L["z0"], 0) / L["reach"]) ** 2)
                fx = np.exp(-(X / L["width"]) ** 2)
                fy = 1.0 / (1.0 + (np.maximum(Y - L["top"], 0) / 160.0) ** 2)
                out = out + L["rgb"] * (L["power"] * c * fz * fx * fy)[..., None]
            elif kind == "bounce":                                 # the sunlit patch of floor, throwing its light back up
                R = L["reach"]
                fy = 1.0 / (1.0 + (np.maximum(Y - L.get("top", 300.0), 0) / 200.0) ** 2)
                for (qx, qz) in L["at"]:
                    dx, dy, dz = qx - X, -Y, qz - Z
                    d2 = dx * dx + dy * dy + dz * dz + 1e-3
                    d = np.sqrt(d2)
                    cp = np.clip((dx * nx + dy * ny + dz * nz) / d + 0.12, 0, 1)
                    cq = np.clip((Y + 40.0) / d, 0, 1)
                    f = R * R / (d2 + (R * 0.5) ** 2)
                    out = out + L["rgb"] * (L["power"] * cp * cq * f * fy)[..., None]
        return out

    def air(self, c, z):
        t = np.clip(np.asarray(z, dtype=F32) / self.ZB, 0, 1)
        fog = self.fog_near + (self.fog_far - self.fog_near) * t[..., None]
        return np.clip(1 - (1 - np.clip(c, 0, 1)) * (1 - fog), 0, 1).astype(F32)

    def light(self, pos, n):
        """The light factor (r, g, b) a surface is multiplied by at a place."""
        return np.sqrt(self.E(pos[0], pos[1], pos[2], n))

    def tone(self, albedo, pos, n, gain=1.0):
        return self.air(col(albedo) * self.light(pos, n) * gain, pos[2])

    def maps(self, shape, ss=1):
        """For every pixel: which face of the room it shows (0 floor, 1 left wall, 2 right wall, 3 back
        wall, 4 ceiling) and where on it, in the world. -> (ids, X, Y, Z)"""
        h, w = shape
        cam = self.cam
        py, px = np.mgrid[0:h * ss, 0:w * ss].astype(F32)
        px, py = (px + 0.5) / ss, (py + 0.5) / ss
        sx, sy = (px - cam.vx) / cam.F, (py - cam.vy) / cam.F
        big = 1e9
        t = np.stack([
            np.where(sy > 1e-6, cam.eye / np.maximum(sy, 1e-6), big),
            np.where(sx < -1e-6, -self.A / np.minimum(sx, -1e-6), big),
            np.where(sx > 1e-6, self.A / np.maximum(sx, 1e-6), big),
            np.full_like(px, cam.Z0 + self.ZB),
            np.where(sy < -1e-6, (cam.eye - self.HC) / np.minimum(sy, -1e-6), big),
        ])
        ids = t.argmin(axis=0)
        T = t.min(axis=0)
        return ids, (sx * T).astype(F32), (cam.eye - sy * T).astype(F32), (T - cam.Z0).astype(F32)

    def lightmap(self, ids, X, Y, Z):
        m = np.zeros(ids.shape + (3,), dtype=F32)
        for pid, n in enumerate((UP, TO_RIGHT, TO_LEFT, TO_US, DOWN)):
            sel = ids == pid
            if sel.any():
                m[sel] = np.sqrt(self.E(X[sel], Y[sel], Z[sel], n))
        return m

    def wall(self, side, u, v, off=0.0):
        """A place on a wall: side 'L' or 'R' (u is depth z), or 'B' the back wall (u is x); v is height."""
        if side == "L":
            return (-self.A + off, v, u)
        if side == "R":
            return (self.A - off, v, u)
        return (u, v, self.ZB - off)

    def wall_n(self, side):
        return {"L": TO_RIGHT, "R": TO_LEFT, "B": TO_US}[side]


# ---------------------------------------------------------------- faces of solid things
def bil(c, u, v):
    a = c[0] + (c[1] - c[0]) * u
    b = c[3] + (c[2] - c[3]) * u
    return a + (b - a) * v


class Face:
    """One flat face of a thing in the room, given by its four corners in the world: (u0,v0), (u1,v0),
    (u1,v1), (u0,v1). Things are drawn on it in u, v (0 to 1) and come out in perspective and in the
    room's light."""

    def __init__(self, room, c00, c10, c11, c01, n):
        self.room, self.n = room, n
        self.c = [np.array(c, dtype=float) for c in (c00, c10, c11, c01)]
        self.wu = float(np.linalg.norm(self.c[1] - self.c[0]))         # its size in cm along u and along v
        self.wv = float(np.linalg.norm(self.c[3] - self.c[0]))

    def w(self, u, v):
        return bil(self.c, u, v)

    def at(self, u, v):
        return self.room.P(*self.w(u, v))

    def k(self, u=0.5, v=0.5):
        return self.room.k(self.w(u, v)[2])

    def tone(self, albedo, u=0.5, v=0.5, gain=1.0):
        return self.room.tone(albedo, self.w(u, v), self.n, gain)

    def fill(self, D, albedo, nu=1, nv=1, rng=None, jitter=0.04, gain=1.0, u0=0.0, u1=1.0, v0=0.0, v1=1.0, fine=False, alpha=1.0, rows=None):
        """Paint the face (or a part of it) in nu x nv flat pieces, each with the light of its own place.
        `rows` gives each row of pieces its own tint (boards of a chest)."""
        for j in range(nv):
            row = 1.0 if rows is None else rows[j % len(rows)]
            for i in range(nu):
                a0, a1 = lerp(u0, u1, i / nu), lerp(u0, u1, (i + 1) / nu)
                b0, b1 = lerp(v0, v1, j / nv), lerp(v0, v1, (j + 1) / nv)
                g = gain * row * (1.0 if rng is None else 1.0 + rng.normal(0, jitter))
                c = self.tone(albedo, (a0 + a1) / 2, (b0 + b1) / 2, g)
                D.poly([self.at(a0, b0), self.at(a1, b0), self.at(a1, b1), self.at(a0, b1)], c, alpha, fine=fine)
        return self

    def rect(self, D, u0, u1, v0, v1, albedo, gain=1.0, fine=True, alpha=1.0, flat=False):
        c = col(albedo) if flat else self.tone(albedo, (u0 + u1) / 2, (v0 + v1) / 2, gain)
        D.poly([self.at(u0, v0), self.at(u1, v0), self.at(u1, v1), self.at(u0, v1)], c, alpha, fine=fine)
        return self

    def line(self, D, uv, albedo, width_cm=1.0, alpha=1.0, gain=1.0, flat=False, fine=True, least=0.6):
        pts = [self.at(u, v) for u, v in uv]
        um, vm = sum(p[0] for p in uv) / len(uv), sum(p[1] for p in uv) / len(uv)
        c = col(albedo) if flat else self.tone(albedo, um, vm, gain)
        wd = width_cm * self.k(um, vm)
        D.line(pts, c, max(wd, least), alpha * min(1.0, max(wd / least, 0.35)), fine=fine)
        return self

    def dot(self, D, u, v, r_cm, albedo, gain=1.0, alpha=1.0, flat=False, squash=1.0, fine=True):
        x, y = self.at(u, v)
        r = r_cm * self.k(u, v)
        c = col(albedo) if flat else self.tone(albedo, u, v, gain)
        if r < 0.45:
            alpha, r = alpha * max(r / 0.45, 0.3), 0.45
        D.ellipse(x, y, r * squash, r, c, alpha, fine=fine)
        return self


def lit_line(D, room, pts3, n, albedo, width_cm=1.2, alpha=1.0, gain=1.0, least=0.7, step_cm=40.0, rng=None, breaks=0.0, floor=0.0, fine=True):
    """A painted line on a wall or floor, given in the world: each short piece takes the light of its
    own place, so it glints near a lamp and sinks away in the dark. `floor` is the least it may fade to
    (its own color times that)."""
    a = col(albedo)
    for p, q in zip(pts3[:-1], pts3[1:]):
        p, q = np.array(p, dtype=float), np.array(q, dtype=float)
        n_steps = max(1, int(np.linalg.norm(q - p) / step_cm))
        for i in range(n_steps):
            if rng is not None and breaks and rng.random() < breaks:
                continue
            s0, s1 = p + (q - p) * (i / n_steps), p + (q - p) * ((i + 1) / n_steps)
            mid = (s0 + s1) / 2
            c = np.maximum(room.tone(a, mid, n, gain), a * floor)
            wd = width_cm * room.k(mid[2])
            al = alpha * min(1.0, max(wd / least, 0.3))
            if rng is not None:
                al *= 0.8 + 0.2 * rng.random()
            D.line([room.P(*s0), room.P(*s1)], c, max(wd, least), al, fine=fine, round_ends=False)


# ---------------------------------------------------------------- furniture
WOODS = ("#7a5230", "#6b4526", "#80582e", "#5f3d24", "#74502e")
IRON = "#4a4d5a"
BRONZE = "#a47c3c"
VERDIGRIS = "#5f8e78"


def chest(D, room, x0, x1, y0, y1, z0, z1, seed, toward=1, wood=None, metal=IRON, trim=BRONZE, lid=0.70, straps=(0.2, 0.8),
          boards=4, ring=True, lock=True, seal=False, plated=False, gain=1.0, feet=True):
    """A strong chest standing square to the room. `toward` = 1 if the long side we see is its right one
    (a chest along the left wall), -1 for the other. Wood in boards, iron or bronze straps that go up the
    side and over the lid, studs, a lock plate, a ring handle on the end that faces us."""
    rng = np.random.default_rng(seed)
    wood = WOODS[seed % len(WOODS)] if wood is None else wood
    xs = x1 if toward > 0 else x0
    long = Face(room, (xs, y0, z0), (xs, y0, z1), (xs, y1, z1), (xs, y1, z0), (toward, 0, 0))
    end = Face(room, (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), TO_US)
    top = Face(room, (x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1), UP)
    k = room.k(z0)
    rows = [1.0 + rng.normal(0, 0.07) for _ in range(boards)]
    body = metal if plated else wood
    if feet and y0 < 1:                                            # it stands on two battens: a dark gap under it
        for f in (long, end):
            f.rect(D, 0, 1, 0, 5.0 / max(f.wv, 1), "#1c1414", fine=False, flat=True)
    lo = 5.0 / max(end.wv, 1) if (feet and y0 < 1) else 0.0
    long.fill(D, body, 3, boards, rng, 0.05, gain, v0=lo, rows=rows)
    top.fill(D, body, 2, 3, rng, 0.05, gain * 1.04)
    end.fill(D, body, 2, boards, rng, 0.05, gain, v0=lo, rows=rows)
    if not plated:
        for j in range(1, boards):                                 # the gaps between the boards
            v = lo + (1 - lo) * j / boards
            for f in (long, end):
                f.line(D, [(0, v), (1, v)], wood, 0.8, 0.55, gain * 0.45)
        for j in range(1, 3):
            top.line(D, [(0, j / 3), (1, j / 3)], wood, 0.8, 0.5, gain * 0.5)
    # ---- the lid: a shadow line under its lip, and the lip itself catching what light there is
    for f in (long, end):
        f.line(D, [(0, lid), (1, lid)], "#140e0e", 1.6, 0.85, flat=True)
        f.line(D, [(0, lid + 2.2 / max(f.wv, 1)), (1, lid + 2.2 / max(f.wv, 1))], body, 1.0, 0.7, gain * 1.5)
    # ---- straps: up the long side and over the lid
    sw = 7.5 / max(long.wu, 1)
    for s in straps:
        long.rect(D, s - sw / 2, s + sw / 2, lo, 1, metal, gain * 1.0, fine=False)
        top.rect(D, 0, 1, s - sw / 2, s + sw / 2, metal, gain * 1.05, fine=False)
        long.line(D, [(s - sw / 2, lo), (s - sw / 2, 1)], metal, 0.9, 0.7, gain * 1.7)
        top.line(D, [(0, s - sw / 2), (1, s - sw / 2)], metal, 0.9, 0.7, gain * 1.7)
        if k > 0.36:
            for v in np.linspace(lo + 0.1, 0.94, 5 if k > 0.6 else 3):
                long.dot(D, s, v, 1.5, trim if metal == IRON else metal, gain * 1.9)
            for u in np.linspace(0.15, 0.85, 3):
                top.dot(D, u, s, 1.5, trim if metal == IRON else metal, gain * 1.9, squash=1.0)
    # ---- the end we look at: an iron frame round it, and a ring to carry it by
    eu, ev = 6.5 / max(end.wu, 1), 6.5 / max(end.wv, 1)
    for (a0, a1, b0, b1) in ((0, eu, lo, 1), (1 - eu, 1, lo, 1), (0, 1, 1 - ev, 1), (0, 1, lo, lo + ev)):
        end.rect(D, a0, a1, b0, b1, metal, gain, fine=False)
    end.line(D, [(eu, lo + ev), (eu, 1 - ev), (1 - eu, 1 - ev)], metal, 0.9, 0.75, gain * 1.7)
    end.line(D, [(eu, lo + ev), (1 - eu, lo + ev), (1 - eu, 1 - ev)], "#0e0c10", 0.9, 0.6, flat=True)
    if k > 0.36:
        for (u, v) in ((eu / 2, lo + ev / 2), (1 - eu / 2, lo + ev / 2), (eu / 2, 1 - ev / 2), (1 - eu / 2, 1 - ev / 2), (eu / 2, (1 + lo) / 2), (1 - eu / 2, (1 + lo) / 2), (0.5, 1 - ev / 2), (0.5, lo + ev / 2)):
            end.dot(D, u, v, 1.7, trim, gain * 1.9)
    if plated and k > 0.36:                                        # a strongbox: plates and rows of big studs
        for f, nu_, nv_ in ((end, 4, 3), (long, 6, 3)):
            for i in range(1, nu_):
                for j in range(1, nv_ + 1):
                    f.dot(D, i / nu_, lo + (1 - lo) * (j - 0.5) / nv_, 1.8, trim, gain * 1.8)
    if ring:
        cx, cy = end.at(0.5, 0.46)
        r = 6.5 * k
        D.ellipse(cx, cy - r * 0.9, r * 0.5, r * 0.5, end.tone(metal, 0.5, 0.5, gain * 1.2), fine=True)       # its plate
        D.line([(cx + math.cos(a) * r, cy + math.sin(a) * r * 1.05) for a in np.linspace(-0.2, math.pi + 0.2, 12)], end.tone(trim, 0.5, 0.4, gain * 1.5), max(0.9, 1.6 * k))
        D.line([(cx + math.cos(a) * r, cy + math.sin(a) * r * 1.05) for a in np.linspace(0.3, 1.2, 5)], end.tone(trim, 0.5, 0.4, gain * 2.4), max(0.7, 1.0 * k), 0.9)
    if lock:                                                       # the lock plate on the long side, its hasp coming down from the lid
        lu, lv = 8.0 / max(long.wu, 1), 9.0 / max(long.wv, 1)
        c = 0.5
        long.rect(D, c - lu / 2, c + lu / 2, lid - lv, lid - 1.0 / max(long.wv, 1), trim, gain * 1.2)
        long.rect(D, c - lu / 5, c + lu / 5, lid - lv * 0.5, min(1.0, lid + lv * 0.7), trim, gain * 1.6)
        long.dot(D, c, lid - lv * 0.55, 1.4, "#0c0a0c", flat=True)
    if seal:                                                       # a cord across the lid and a blob of red wax
        v = lid
        end.line(D, [(0.62, v + 0.12), (0.66, v - 0.02), (0.70, v - 0.16)], "#d8c8a0", 0.8, 0.9, gain)
        end.dot(D, 0.66, v - 0.02, 2.6, "#c42a22", gain * 1.5)
        end.dot(D, 0.655, v - 0.01, 1.0, "#f07a5a", gain * 1.7)
    # ---- edges: the near top edges catch the light, the foot sits in its own shadow
    top.line(D, [(0, 0), (1, 0)], body, 1.0, 0.75, gain * 1.6)
    long.line(D, [(0, 1), (1, 1)], body, 0.9, 0.6, gain * 1.5)
    for f in (long, end):
        f.line(D, [(0, 0), (1, 0)], "#0c0a0c", 1.6, 0.7, flat=True)
    return dict(long=long, end=end, top=top)


def sack(D, room, x, y, z, w, h, seed, cloth="#bfa26a", lean=0.0, tag=True, gain=1.0, side=1):
    """A sealed sack of coin standing (or slumped: `lean`) at a place: a heavy bottom, a tied neck, a
    lead seal on a cord. `side` = 1 if the light comes from our right of it, -1 from the left."""
    rng = np.random.default_rng(seed)
    cx, cy = room.P(x, y, z)
    k = room.k(z)
    W, Hh = w * k, h * k
    shape = [(-0.46, 0.02), (-0.56, -0.22), (-0.53, -0.52), (-0.36, -0.74), (-0.17, -0.84), (-0.12, -0.90), (0.12, -0.90), (0.17, -0.84), (0.36, -0.74), (0.53, -0.52), (0.56, -0.22), (0.46, 0.02), (0.0, 0.05)]

    def at(u, v):
        return (cx + (u + lean * (-v)) * W + 0, cy + v * Hh)
    pts = [at(u * (1 + rng.normal(0, 0.05)), v * (1 + rng.normal(0, 0.03))) for u, v in shape]
    pos = (x, y + h * 0.5, z)
    n = (0.35 * side, 0.25, -0.9)
    base = room.tone(cloth, pos, n, gain)
    dark = room.tone(cloth, pos, (-0.8 * side, -0.2, -0.3), gain * 0.62)
    lite = room.tone(cloth, pos, (0.6 * side, 0.5, -0.6), gain * 1.3)
    D.poly(pts, base)
    D.poly([at(-0.46 * side, 0.02), at(-0.56 * side, -0.22), at(-0.53 * side, -0.52), at(-0.36 * side, -0.74), at(-0.2 * side, -0.60), at(-0.26 * side, -0.25), at(-0.1 * side, 0.03)], dark, 0.85)
    D.poly([at(0.10 * side, -0.78), at(0.34 * side, -0.70), at(0.47 * side, -0.50), at(0.42 * side, -0.26), at(0.26 * side, -0.42), at(0.16 * side, -0.62)], lite, 0.7)
    D.poly([at(-0.44, 0.03), at(-0.5, -0.1), at(0.5, -0.1), at(0.44, 0.03)], dark, 0.55)          # it sags on the floor
    # the neck, tied, and the ears of cloth above the cord
    D.poly([at(-0.13, -0.86), at(-0.22, -1.06), at(-0.04, -0.98), at(0.07, -1.10), at(0.20, -1.0), at(0.13, -0.86)], base)
    D.poly([at(-0.13, -0.86), at(-0.22, -1.06), at(-0.04, -0.98), at(-0.02, -0.86)], dark, 0.6)
    D.line([at(-0.15, -0.87), at(0.15, -0.87)], room.tone("#4a3424", pos, n, gain), max(0.8, 1.6 * k))
    if k > 0.4:
        for u in (-0.22, 0.05, 0.27):                              # folds running down from the neck
            D.line([at(u * 0.5, -0.82), at(u, -0.5), at(u * 1.1, -0.2)], dark, max(0.6, 0.9 * k), 0.45)
    if tag and k > 0.4:
        tx, ty = at(0.2 * side, -0.80)
        D.line([at(0.1 * side, -0.87), (tx, ty), (tx + 2.0 * k * side, ty + 5.0 * k)], room.tone("#d8c8a0", pos, n, gain), max(0.6, 0.7 * k), 0.9)
        D.ellipse(tx + 2.0 * k * side, ty + 6.5 * k, max(1.0, 2.4 * k), max(1.0, 2.4 * k), room.tone("#b02a20", pos, n, gain * 1.3), fine=True)
    return (cx, cy)


def tablet(D, room, side, u0, u1, v0, v1, seed, gain=1.0, rows=None, color=BRONZE, pediment=False, cords=True):
    """A bronze tablet of law hung flat on a wall: a rim, rows of tiny lettering, nails at the corners, a
    green bloom where the damp has got at it."""
    rng = np.random.default_rng(seed)
    n = room.wall_n(side)
    f = Face(room, room.wall(side, u0, v0, 2.0), room.wall(side, u1, v0, 2.0), room.wall(side, u1, v1, 2.0), room.wall(side, u0, v1, 2.0), n)
    kk = f.k()
    if cords:                                                      # it hangs from a nail by a cord
        peg = room.wall(side, (u0 + u1) / 2, v1 + (v1 - v0) * 0.22, 1.0)
        D.line([f.at(0.12, 1.0), room.P(*peg), f.at(0.88, 1.0)], room.tone("#8a7a5a", peg, n, gain), max(0.6, 0.8 * kk), 0.8)
        px, py = room.P(*peg)
        D.ellipse(px, py, max(0.8, 1.6 * kk), max(0.8, 1.6 * kk), room.tone("#2a2a30", peg, n, gain * 1.4), fine=True)
    f.fill(D, color, 2, 4, rng, 0.07, gain * 0.80)
    if pediment:
        D.poly([f.at(0, 1), f.at(0.5, 1.22), f.at(1, 1)], f.tone(color, 0.5, 1.0, gain * 0.80))
        D.line([f.at(0, 1), f.at(0.5, 1.22), f.at(1, 1)], f.tone(color, 0.5, 1.0, gain * 1.6), max(0.7, 1.0 * kk), 0.8)
    for _ in range(5):                                             # verdigris: green patches that keep inside the plate, and runs below the nails
        u0_, v0_ = rng.random() * 0.7, rng.random() ** 2 * 0.6
        du, dv = 0.12 + 0.2 * rng.random(), 0.06 + 0.14 * rng.random()
        f.rect(D, u0_, min(u0_ + du, 1.0), v0_, min(v0_ + dv, 1.0), VERDIGRIS, gain * 0.9, fine=False, alpha=0.30)
    for u_ in (0.08, 0.92):
        f.line(D, [(u_, 0.92), (u_ + rng.normal(0, 0.02), 0.55 + 0.25 * rng.random())], VERDIGRIS, 2.2, 0.4, gain)
    mu, mv = 5.0 / max(f.wu, 1), 5.0 / max(f.wv, 1)
    f.line(D, [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], color, 1.6, 0.9, gain * 0.5)
    f.line(D, [(mu, mv), (mu, 1 - mv), (1 - mu, 1 - mv)], color, 0.9, 0.8, gain * 1.7)
    f.line(D, [(mu, mv), (1 - mu, mv), (1 - mu, 1 - mv)], color, 0.9, 0.7, gain * 0.45)
    f.line(D, [(0, 1), (1, 1)], color, 1.2, 0.9, gain * 1.9)       # its top edge catches the light
    n_rows = rows or max(3, int(f.wv * kk / 3.2))
    for i in range(n_rows):                                        # lettering: broken rows of tiny marks
        v = 1 - mv * 2.2 - (1 - mv * 4.4) * i / max(n_rows - 1, 1)
        u = mu * 2.0
        while u < 1 - mu * 2.0:
            run = (0.06 + 0.16 * rng.random())
            e = min(u + run, 1 - mu * 2.0)
            f.line(D, [(u, v), (e, v)], color, 1.3, 0.8, gain * (0.26 if rng.random() < 0.8 else 0.4), least=0.55)
            u = e + 0.03 + 0.05 * rng.random()
    for (u, v) in ((mu * 0.9, mv * 0.9), (1 - mu * 0.9, mv * 0.9), (mu * 0.9, 1 - mv * 0.9), (1 - mu * 0.9, 1 - mv * 0.9)):
        f.dot(D, u, v, 1.3, color, gain * 2.2)
    return f


def coals(D, cx, cy, rx, ry, seed, heap=0.5, heat=1.0):
    """A bed of glowing coals seen from above, filling an ellipse: the fire shows in the gaps between
    dark lumps, a few of the lumps are white-hot. `heap` lifts the middle of it."""
    rng = np.random.default_rng(seed)
    D.ellipse(cx, cy, rx, ry, mixc("#8a1e0c", "#d8481a", min(heat, 1.0) * 0.7))
    D.ellipse(cx, cy - ry * heap * 0.3, rx * 0.72, ry * 0.72, mixc("#ff7a1e", "#ffb040", min(heat, 1.2) * 0.5))
    n = int(18 + rx * 1.5)
    lumps = []
    for _ in range(n):
        a, r = rng.random() * math.pi * 2, math.sqrt(rng.random()) * 0.90
        lumps.append((math.sin(a) * r, math.cos(a) * r, rng.random()))
    lumps.sort(key=lambda p: p[0])                                 # far ones first
    for (v, u, t) in lumps:
        px = cx + u * rx
        py = cy + v * ry - (1 - (u * u + v * v)) * heap * ry
        s = max(1.0, rx * (0.10 + 0.10 * rng.random()))
        if t > 0.80:                                               # a lump burning right through
            D.ellipse(px, py, s * 0.8, s * 0.6, "#ffcf6a")
            D.ellipse(px - s * 0.1, py - s * 0.1, s * 0.4, s * 0.3, "#fff4c8", 0.9, fine=True)
            continue
        D.ellipse(px, py, s, s * 0.74, mixc("#5a140c", "#a82c12", t))                       # its glowing underside
        D.ellipse(px + s * 0.05, py - s * 0.22, s * 0.86, s * 0.50, mixc("#1c0c0c", "#3a1612", t))   # its black top
        if t < 0.25:
            D.ellipse(px - s * 0.2, py - s * 0.3, s * 0.3, s * 0.16, "#6a5a58", 0.7, fine=True)     # a flake of grey ash


def brazier(D, room, x, z, h, r, seed, gain=1.0, heat=1.0, bronze="#a8823e"):
    """A bronze brazier on three legs with lions' feet, a shallow pan of coals on top. Its own fire lights
    the inside of the pan and the legs from above."""
    k = room.k(z)
    cx, cy = room.P(x, h, z)
    rx = r * k
    ry = rx * room.squash(h, z)
    ember = np.array([1.0, 0.45, 0.16], dtype=F32)
    dark = room.tone(bronze, (x, h * 0.5, z), (0, 0, -1), gain * 0.55)
    mid = room.tone(bronze, (x, h * 0.5, z), (0, 0, -1), gain * 1.0)
    lite = np.clip(mid * 1.5 + ember * 0.16, 0, 1)
    # ---- legs: two in front (left and right), one behind; each swells at the knee and ends in a paw
    feet = [(x + math.cos(a) * r * 0.86, z + math.sin(a) * r * 0.86) for a in (math.radians(100), math.radians(215), math.radians(325))]
    for i, (fx, fz) in enumerate(feet):
        f0 = room.P(fx, 0, fz)
        knee = room.P(x + (fx - x) * 1.16, h * 0.42, z + (fz - z) * 1.16)
        hip = room.P(x + (fx - x) * 0.72, h * 0.86, z + (fz - z) * 0.72)
        tone_ = dark if i == 0 else mid
        D.taper([hip, knee], tone_, 5.6 * k, 5.0 * k, fine=False)
        D.taper([knee, ((knee[0] + f0[0]) / 2 + (f0[0] - knee[0]) * 0.1, (knee[1] + f0[1]) / 2), f0], tone_, 5.0 * k, 3.2 * k, fine=False)
        D.ellipse(knee[0], knee[1], 3.6 * k, 3.8 * k, tone_)
        D.ellipse(f0[0], f0[1] - 1.6 * k, 5.2 * k, 3.0 * k, tone_)                         # the paw
        if i:
            D.line([hip, knee], lite, max(0.7, 1.0 * k), 0.75)
            D.line([knee, (f0[0], f0[1] - 2.0 * k)], lite, max(0.7, 0.9 * k), 0.55)
            D.ellipse(knee[0], knee[1], 2.6 * k, 2.6 * k, lite, 0.8, fine=True)
            D.line([(f0[0] - 2.4 * k, f0[1] - 0.4 * k), (f0[0] + 2.4 * k, f0[1] - 0.4 * k)], "#140c0c", max(0.6, 0.7 * k), 0.7)
    ring = room.P(x, h * 0.42, z)                                   # a ring that ties the three legs together
    rr = r * 0.70 * 1.16 * k
    D.line([(ring[0] + math.cos(a) * rr, ring[1] + math.sin(a) * rr * room.squash(h * 0.42, z)) for a in np.linspace(0, math.pi * 2, 25)], dark, max(0.8, 1.4 * k))
    D.line([(ring[0] + math.cos(a) * rr, ring[1] + math.sin(a) * rr * room.squash(h * 0.42, z)) for a in np.linspace(0.2, math.pi - 0.2, 12)], mid, max(0.7, 1.0 * k), 0.9)
    # ---- the pan: its outside, its rim, the fire in it
    deep = r * 0.42 * k
    D.poly([(cx - rx, cy)] + [(cx + math.cos(a) * rx * 0.96, cy + math.sin(a) * (ry * 0.5 + deep)) for a in np.linspace(math.pi, 0, 14)] + [(cx + rx, cy)], dark)
    D.poly([(cx + math.cos(a) * rx * 0.94, cy + math.sin(a) * (ry * 0.5 + deep * 0.92)) for a in np.linspace(math.pi * 0.95, math.pi * 0.42, 9)] + [(cx + math.cos(a) * rx * 0.99, cy + math.sin(a) * ry * 0.9) for a in np.linspace(math.pi * 0.42, math.pi * 0.95, 9)], mid, 0.9)
    for a in (math.pi * 0.22, math.pi * 0.78):                    # ring handles hanging at the sides
        hx, hy = cx + math.cos(a) * rx * 0.98, cy + math.sin(a) * ry + deep * 0.5
        D.line([(hx + math.cos(t) * 3.2 * k, hy + math.sin(t) * 3.6 * k) for t in np.linspace(0, math.pi * 2, 13)], lite, max(0.7, 1.1 * k), 0.9)
    D.ellipse(cx, cy, rx, ry, dark)
    D.ellipse(cx, cy, rx * 0.90, ry * 0.88, np.clip(mid * 0.6 + ember * 0.5 * heat, 0, 1))          # the inside of the pan, lit by the fire
    coals(D, cx, cy + ry * 0.06, rx * 0.80, ry * 0.76, seed, heap=0.55, heat=heat)
    D.line([(cx + math.cos(a) * rx * 0.97, cy + math.sin(a) * ry * 0.96) for a in np.linspace(math.pi * 0.05, math.pi * 0.95, 16)], lite, max(0.8, 1.3 * k), 0.95)     # the near rim
    D.line([(cx + math.cos(a) * rx * 0.97, cy + math.sin(a) * ry * 0.96) for a in np.linspace(math.pi * 1.1, math.pi * 1.9, 14)], np.clip(mid * 0.7 + ember * 0.55 * heat, 0, 1), max(0.7, 1.0 * k), 0.9)
    return (cx, cy, rx, ry)

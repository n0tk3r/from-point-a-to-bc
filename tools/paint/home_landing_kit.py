"""The landing's own tools. Everything in the picture goes through ONE camera (room.View):

  Tracer    for every pixel, the first flat surface the line of sight meets (walls, floors, the faces of
            boxes), so that the place in the room (X, Y, Z in cm), the way the surface faces and what it is
            made of are known for every pixel. Lamps then light the room where they really stand, and
            boxes throw true shadows.
  Tex       a flat thing (a door, a notice, a rug) painted face-on in its own centimetres, then laid on
            its wall or floor THROUGH the camera (Tracer.decal), so it converges with the room.
  letters   block capitals made of pen strokes, for notices that have to be read when they are 8 pixels high.
"""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, blur, lerp, resize, rgb, sample

AX = {"X": 0, "Y": 1, "Z": 2}
NORMALS = np.array([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)], dtype=F32)


def c8(color, alpha=1.0):
    c = rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
    return tuple(int(v) for v in np.clip(c * 255 + 0.5, 0, 255)) + (int(round(alpha * 255)),)


def hash2(i, j, seed=0.0):
    """A steady random number 0..1 for every pair of whole numbers (one tone for each board, book, tile)."""
    h = np.sin(i * 127.1 + j * 311.7 + seed * 74.7) * 43758.5453
    return (h - np.floor(h)).astype(F32)


# ====================================================================== the tracer
class Tracer:
    def __init__(self, v, ss=2, window=(0, 0, 800, 600)):
        self.v, self.ss, self.win = v, ss, window
        x0, y0, x1, y1 = window
        W, H = (x1 - x0) * ss, (y1 - y0) * ss
        py, px = np.mgrid[0:H, 0:W].astype(F32)
        a = ((px + 0.5) / ss + x0 - v.cx) / v.F
        u = (v.hz - ((py + 0.5) / ss + y0)) / v.F
        self.d = [(a * v.rx + v.fx).astype(F32), u.astype(F32), (a * v.rz + v.fz).astype(F32)]
        self.C = (v.cam_x, v.eye, v.cam_z)
        self.t = np.full((H, W), 1e9, dtype=F32)
        self.tag = np.zeros((H, W), dtype=np.int32)
        self.nrm = np.zeros((H, W), dtype=np.int8)
        self.names, self.colors, self.mats = ["nothing"], [rgb("#000000")], ["flat"]
        self.boxes = []                                    # everything that can throw a shadow
        self.albedo = None
        self.emit = np.zeros((H, W, 3), dtype=F32)         # things that shine by themselves (the night in a window)
        self.ecov = np.zeros((H, W), dtype=F32)

    # ------------------------------------------------------------ what things are
    def new(self, name, color, mat="flat"):
        self.names.append(name)
        self.colors.append(rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32))
        self.mats.append(mat)
        return len(self.names) - 1

    # ------------------------------------------------------------ flat surfaces
    def _window(self, pts3):
        pp = self.v.poly(pts3)
        if len(pp) < 3:
            return None
        ss = self.ss
        H, W = self.t.shape
        xs, ys = [p[0] - self.win[0] for p in pp], [p[1] - self.win[1] for p in pp]
        x0, x1 = max(0, int(math.floor(min(xs) * ss)) - 1), min(W, int(math.ceil(max(xs) * ss)) + 2)
        y0, y1 = max(0, int(math.floor(min(ys) * ss)) - 1), min(H, int(math.ceil(max(ys) * ss)) + 2)
        if x1 <= x0 or y1 <= y0:
            return None
        return (slice(y0, y1), slice(x0, x1))

    def rect(self, axis, at, a0, a1, b0, b1, tag):
        """A rectangle on the plane axis = at. (a, b) are the other two of X, Y, Z in that order."""
        k = AX[axis]
        o1, o2 = [i for i in range(3) if i != k]

        def P(a, b):
            p = [0.0, 0.0, 0.0]
            p[k], p[o1], p[o2] = at, a, b
            return tuple(p)
        sl = self._window([P(a0, b0), P(a1, b0), P(a1, b1), P(a0, b1)])
        if sl is None:
            return
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (at - self.C[k]) / self.d[k][sl]
        A = self.C[o1] + self.d[o1][sl] * t
        B = self.C[o2] + self.d[o2][sl] * t
        tb = self.t[sl]
        ok = (t > self.v.near) & (t < tb) & (A >= a0) & (A <= a1) & (B >= b0) & (B <= b1)
        if not ok.any():
            return
        tb[ok] = t[ok]
        self.tag[sl][ok] = tag
        self.nrm[sl][ok] = 2 * k + (0 if self.C[k] > at else 1)

    def box(self, X0, X1, Y0, Y1, Z0, Z1, tag, top=None, front=None, side=None, occl=True):
        """A box: only the faces turned to the lens. `top`, `front` (the face toward +Z) and `side` (the face
        toward +X or -X) may be given other tags."""
        C = self.C
        if C[0] > X1:
            self.rect("X", X1, Y0, Y1, Z0, Z1, side or tag)
        elif C[0] < X0:
            self.rect("X", X0, Y0, Y1, Z0, Z1, side or tag)
        if C[1] > Y1:
            self.rect("Y", Y1, X0, X1, Z0, Z1, top or tag)
        elif C[1] < Y0:
            self.rect("Y", Y0, X0, X1, Z0, Z1, tag)
        if C[2] > Z1:
            self.rect("Z", Z1, X0, X1, Y0, Y1, front or tag)
        elif C[2] < Z0:
            self.rect("Z", Z0, X0, X1, Y0, Y1, tag)
        if occl:
            self.boxes.append((X0, X1, Y0, Y1, Z0, Z1))

    # ------------------------------------------------------------ after tracing
    def world(self):
        t = self.t
        return self.C[0] + self.d[0] * t, self.C[1] + self.d[1] * t, self.C[2] + self.d[2] * t

    def normal(self):
        n = NORMALS[self.nrm]
        return n[..., 0], n[..., 1], n[..., 2]

    def base_colors(self):
        self.albedo = np.asarray(self.colors, dtype=F32)[self.tag]
        return self.albedo

    def footprint(self):
        """About how many centimetres of surface one sample covers (for fading out patterns too fine to draw)."""
        return self.t / (self.v.F * self.ss)

    # ------------------------------------------------------------ flat things laid on a surface
    def decal(self, tex, axis, at, u_axis, u0, u1, v_axis, v0, v1, amount=1.0, k=2, tol=2.5, mode="over", emit=False):
        """Lay a flat painting (h, w, 4: color and cover) on the plane axis = at. Its left edge is u = u0, its
        right edge u = u1, its bottom v = v0 and its top v = v1 (either may run backwards). It only shows where
        that plane is what the lens really sees. mode "tint" multiplies instead (for shadows and stains)."""
        ka, ku, kv = AX[axis], AX[u_axis], AX[v_axis]

        def P(u, w):
            p = [0.0, 0.0, 0.0]
            p[ka], p[ku], p[kv] = at, u, w
            return tuple(p)
        sl = self._window([P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1)])
        if sl is None:
            return
        ss, v = self.ss, self.v
        ys, xs = sl
        h, w = ys.stop - ys.start, xs.stop - xs.start
        n = ss * k
        py, px = np.mgrid[0:h * k, 0:w * k].astype(F32)
        a = ((px + 0.5) / n + xs.start / ss + self.win[0] - v.cx) / v.F
        uu = (v.hz - ((py + 0.5) / n + ys.start / ss + self.win[1])) / v.F
        d = [a * v.rx + v.fx, uu, a * v.rz + v.fz]
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (at - self.C[ka]) / d[ka]
        U = self.C[ku] + d[ku] * t
        V = self.C[kv] + d[kv] * t
        th, tw = tex.shape[:2]
        fu = (U - u0) / (u1 - u0)
        fv = (v1 - V) / (v1 - v0)
        inside = (t > v.near) & (fu >= 0) & (fu <= 1) & (fv >= 0) & (fv <= 1)
        if not inside.any():
            return
        # texels per sample: soften the painting first if it is much finer than the lens can see
        tmean = float(np.median(t[inside]))
        per_cm = v.F * n / max(tmean, 1.0)
        ratio = (tw / abs(u1 - u0)) / per_cm
        src = blur(tex, ratio * 0.42) if ratio > 1.4 else tex
        got = sample(src, np.clip(fu, 0, 1) * (tw - 1), np.clip(fv, 0, 1) * (th - 1))
        cover = got[..., 3] * inside
        col = (got[..., :3] * cover[..., None]).reshape(h, k, w, k, 3).mean(axis=(1, 3))
        cov = cover.reshape(h, k, w, k).mean(axis=(1, 3))
        tmid = t.reshape(h, k, w, k).mean(axis=(1, 3))
        seen = np.abs(self.t[sl] - tmid) < tol * np.maximum(1.0, tmid / 400.0)
        cov = cov * seen * amount
        col = col / np.maximum(cover.reshape(h, k, w, k).mean(axis=(1, 3)), 1e-4)[..., None]
        if emit:
            self.emit[sl] = self.emit[sl] * (1 - cov[..., None]) + col * cov[..., None]
            self.ecov[sl] = np.maximum(self.ecov[sl], cov)
            return
        alb = self.albedo[sl]
        self.ecov[sl] = self.ecov[sl] * (1 - cov)             # whatever is laid over a shining thing hides it
        if mode == "tint":
            alb[...] = alb * (1 - cov[..., None]) + alb * col * cov[..., None]
        else:
            alb[...] = alb * (1 - cov[..., None]) + col * cov[..., None]

    def down(self, a):
        """A picture at the tracer's fineness -> at the picture's own."""
        ss = self.ss
        if ss == 1:
            return a
        H, W = a.shape[:2]
        if a.ndim == 3:
            return a.reshape(H // ss, ss, W // ss, ss, a.shape[2]).mean(axis=(1, 3))
        return a.reshape(H // ss, ss, W // ss, ss).mean(axis=(1, 3))


# ====================================================================== light
def lamp(P, N, L, power=1.0, r0=100.0, fall=0.75, wrap=0.12):
    """How strongly a lamp at L lights every pixel: by distance and by the angle the light strikes."""
    vx, vy, vz = L[0] - P[0], L[1] - P[1], L[2] - P[2]
    d2 = vx * vx + vy * vy + vz * vz
    d = np.sqrt(d2) + 1e-3
    ndl = (N[0] * vx + N[1] * vy + N[2] * vz) / d
    ndl = np.clip((ndl + wrap) / (1 + wrap), 0, 1)
    return (power * ndl * (1 + d2 / (r0 * r0)) ** (-fall)).astype(F32)


def shade(P, L, half_height, radius, through=0.5, soft=0.12):
    """A lampshade: light leaves freely above and below it and only dimly through its side."""
    vx, vy, vz = P[0] - L[0], P[1] - L[1], P[2] - L[2]
    flat = np.sqrt(vx * vx + vz * vz) + 1e-3
    steep = np.abs(vy) / flat
    edge = half_height / radius
    return lerp(through, 1.0, np.clip((steep - edge * (1 - soft)) / (edge * 2 * soft), 0, 1)).astype(F32)


def blocked(P, L, boxes, directional=False):
    """True where a box stands between the place P (arrays) and the lamp at L (or, with `directional`, where
    the way out along the direction L is barred within 3000 cm)."""
    ox, oy, oz = P
    if directional:
        dx = np.full(ox.shape, L[0] * 3000.0, dtype=F32)
        dy = np.full(ox.shape, L[1] * 3000.0, dtype=F32)
        dz = np.full(ox.shape, L[2] * 3000.0, dtype=F32)
    else:
        dx, dy, dz = L[0] - ox, L[1] - oy, L[2] - oz
    inv = [1.0 / np.where(np.abs(q) < 1e-4, 1e-4, q) for q in (dx, dy, dz)]
    hit = np.zeros(ox.shape, dtype=bool)
    for (X0, X1, Y0, Y1, Z0, Z1) in boxes:
        s1, s2 = (X0 - ox) * inv[0], (X1 - ox) * inv[0]
        lo, hi = np.minimum(s1, s2), np.maximum(s1, s2)
        s1, s2 = (Y0 - oy) * inv[1], (Y1 - oy) * inv[1]
        lo, hi = np.maximum(lo, np.minimum(s1, s2)), np.minimum(hi, np.maximum(s1, s2))
        s1, s2 = (Z0 - oz) * inv[2], (Z1 - oz) * inv[2]
        lo, hi = np.maximum(lo, np.minimum(s1, s2)), np.minimum(hi, np.maximum(s1, s2))
        hit |= (hi > np.maximum(lo, 2e-3)) & (lo < 0.998)
    return hit


def through_rect(P, L, axis, at, a0, a1, b0, b1, directional=False):
    """Where the straight way from P to the lamp at L crosses the plane axis = at: (inside the rectangle?, a, b)."""
    k = AX[axis]
    o1, o2 = [i for i in range(3) if i != k]
    if directional:
        d = [np.full(P[0].shape, L[i], dtype=F32) for i in range(3)]
    else:
        d = [L[i] - P[i] for i in range(3)]
    den = np.where(np.abs(d[k]) < 1e-5, 1e-5, d[k])
    s = (at - P[k]) / den
    A = P[o1] + d[o1] * s
    B = P[o2] + d[o2] * s
    ok = (s > 0) & (A >= a0) & (A <= a1) & (B >= b0) & (B <= b1)
    if not directional:
        ok &= s < 1
    return ok, A, B


# ====================================================================== flat paintings in centimetres
class Tex:
    """A flat thing painted face-on in its own centimetres: x to the right, y UP from its bottom edge."""

    def __init__(self, w, h, res=4.0, color=None):
        self.w, self.h, self.res = float(w), float(h), float(res)
        size = (max(2, int(round(w * res))), max(2, int(round(h * res))))
        self.im = Image.new("RGB", size, c8(color or "#000000")[:3])
        self.al = Image.new("L", size, 255 if color is not None else 0)
        self.d = ImageDraw.Draw(self.im, "RGBA")
        self.da = ImageDraw.Draw(self.al)

    def _p(self, x, y):
        return (x * self.res, (self.h - y) * self.res)

    def poly(self, pts, color, alpha=1.0, solid=True):
        pp = [self._p(*p) for p in pts]
        self.d.polygon(pp, fill=c8(color, alpha))
        if solid:
            self.da.polygon(pp, fill=255)
        return self

    def rect(self, x0, y0, x1, y1, color, alpha=1.0, solid=True):
        return self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], color, alpha, solid)

    def frame(self, x0, y0, x1, y1, wide, color, alpha=1.0):
        self.rect(x0, y0, x1, y0 + wide, color, alpha)
        self.rect(x0, y1 - wide, x1, y1, color, alpha)
        self.rect(x0, y0, x0 + wide, y1, color, alpha)
        self.rect(x1 - wide, y0, x1, y1, color, alpha)
        return self

    def line(self, pts, color, width, alpha=1.0, solid=True):
        pp = [self._p(*p) for p in pts]
        wd = max(1, int(round(width * self.res)))
        self.d.line(pp, fill=c8(color, alpha), width=wd, joint="curve")
        if solid:
            self.da.line(pp, fill=255, width=wd, joint="curve")
        if wd > 2:
            r = wd / 2
            for x, y in (pp[0], pp[-1]):
                self.d.ellipse([x - r, y - r, x + r, y + r], fill=c8(color, alpha))
                if solid:
                    self.da.ellipse([x - r, y - r, x + r, y + r], fill=255)
        return self

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0, solid=True):
        x, y = self._p(cx, cy)
        box = [x - rx * self.res, y - ry * self.res, x + rx * self.res, y + ry * self.res]
        self.d.ellipse(box, fill=c8(color, alpha))
        if solid:
            self.da.ellipse(box, fill=255)
        return self

    def write(self, words, x, y, cap, color, weight=0.16, wide=0.56, gap=0.22, anchor="l", seed=0, wobble=0.04, alpha=1.0):
        """Block capitals in pen strokes. (x, y) is the left end (or middle, anchor "m") of the BASELINE; `cap`
        is the height of a capital in cm. -> the width written."""
        return write(self, words, x, y, cap, color, weight, wide, gap, anchor, seed, wobble, alpha)

    def array(self, mottle=0.0, cell=14.0, seed=0):
        a = np.asarray(self.im, dtype=F32) / 255
        al = np.asarray(self.al, dtype=F32) / 255
        if mottle:
            from brush import noise
            n = noise(a.shape[:2], cell * self.res / 4, seed, 3) - 0.5
            a = np.clip(a * (1 + 2 * mottle * n[..., None]), 0, 1)
        return np.dstack([a, al]).astype(F32)


# ====================================================================== lettering in pen strokes
# Each letter on a grid 4 wide and 6 high (y DOWN from the top of a capital), as pen strokes.
GLYPHS = {
    "A": [[(0, 6), (0, 2), (2, 0), (4, 2), (4, 6)], [(0, 3.8), (4, 3.8)]],
    "B": [[(0, 0), (0, 6), (3, 6), (4, 5), (4, 4), (3, 3), (0, 3)], [(3, 3), (4, 2.1), (4, 1), (3, 0), (0, 0)]],
    "C": [[(4, 1.1), (3, 0), (1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 4.9)]],
    "D": [[(0, 0), (0, 6), (2.4, 6), (4, 4.5), (4, 1.5), (2.4, 0), (0, 0)]],
    "E": [[(4, 0), (0, 0), (0, 6), (4, 6)], [(0, 3), (3.1, 3)]],
    "F": [[(4, 0), (0, 0), (0, 6)], [(0, 3), (3.1, 3)]],
    "G": [[(4, 1.1), (3, 0), (1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5), (4, 3.2), (2.3, 3.2)]],
    "H": [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3), (4, 3)]],
    "I": [[(2, 0), (2, 6)], [(1, 0), (3, 0)], [(1, 6), (3, 6)]],
    "J": [[(4, 0), (4, 5), (3, 6), (1, 6), (0, 5)]],
    "K": [[(0, 0), (0, 6)], [(4, 0), (0, 3.5)], [(1.3, 2.5), (4, 6)]],
    "L": [[(0, 0), (0, 6), (4, 6)]],
    "M": [[(0, 6), (0, 0), (2, 3.2), (4, 0), (4, 6)]],
    "N": [[(0, 6), (0, 0), (4, 6), (4, 0)]],
    "O": [[(1, 0), (3, 0), (4, 1), (4, 5), (3, 6), (1, 6), (0, 5), (0, 1), (1, 0)]],
    "P": [[(0, 6), (0, 0), (3, 0), (4, 1), (4, 2.3), (3, 3.3), (0, 3.3)]],
    "Q": [[(1, 0), (3, 0), (4, 1), (4, 5), (3, 6), (1, 6), (0, 5), (0, 1), (1, 0)], [(2.3, 4.1), (4.3, 6.4)]],
    "R": [[(0, 6), (0, 0), (3, 0), (4, 1), (4, 2.3), (3, 3.3), (0, 3.3)], [(1.9, 3.3), (4, 6)]],
    "S": [[(4, 1), (3, 0), (1, 0), (0, 1), (0, 2.2), (1, 3), (3, 3), (4, 3.8), (4, 5), (3, 6), (1, 6), (0, 5)]],
    "T": [[(0, 0), (4, 0)], [(2, 0), (2, 6)]],
    "U": [[(0, 0), (0, 5), (1, 6), (3, 6), (4, 5), (4, 0)]],
    "V": [[(0, 0), (2, 6), (4, 0)]],
    "W": [[(0, 0), (1, 6), (2, 2.6), (3, 6), (4, 0)]],
    "X": [[(0, 0), (4, 6)], [(4, 0), (0, 6)]],
    "Y": [[(0, 0), (2, 3), (4, 0)], [(2, 3), (2, 6)]],
    "Z": [[(0, 0), (4, 0), (0, 6), (4, 6)]],
    "-": [[(0.6, 3.2), (3.4, 3.2)]],
    ".": [[(1.7, 5.7), (2.0, 6.0)]],
    ",": [[(2.0, 5.6), (1.5, 6.8)]],
    "'": [[(2.0, 0), (1.7, 1.5)]],
    "!": [[(2, 0), (2, 4.0)], [(2, 5.7), (2, 6.0)]],
    "?": [[(0.2, 1.1), (1.2, 0), (3, 0), (4, 1), (4, 2.2), (2.1, 3.5), (2.1, 4.3)], [(2.1, 5.7), (2.1, 6.0)]],
    ":": [[(2, 2.0), (2, 2.3)], [(2, 5.0), (2, 5.3)]],
}
NARROW = {"I": 0.55, ".": 0.4, ",": 0.4, "'": 0.4, "!": 0.4, ":": 0.4, "-": 0.8, " ": 0.62}


def width_of(words, cap, wide=0.56, gap=0.22):
    return sum(cap * wide * NARROW.get(ch, 1.0) + cap * gap for ch in words) - cap * gap


def write(tex, words, x, y, cap, color, weight=0.16, wide=0.56, gap=0.22, anchor="l", seed=0, wobble=0.04, alpha=1.0):
    rng = np.random.default_rng(seed)
    total = width_of(words, cap, wide, gap)
    if anchor == "m":
        x -= total / 2
    elif anchor == "r":
        x -= total
    for ch in words:
        w = cap * wide * NARROW.get(ch, 1.0)
        dy = rng.normal(0, wobble) * cap * 0.5
        lean = rng.normal(0, wobble) * 0.6
        if ch in GLYPHS:
            for st in GLYPHS[ch]:
                pts = []
                for gx, gy in st:
                    if ch in NARROW:
                        px = x + (gx - 2) / 4 * cap * wide + w / 2
                    else:
                        px = x + gx / 4 * w
                    hy = (6 - gy) / 6 * cap
                    pts.append((px + lean * hy, y + hy + dy))
                if len(pts) == 2 and abs(pts[0][0] - pts[1][0]) + abs(pts[0][1] - pts[1][1]) < cap * 0.12:
                    tex.ellipse(pts[0][0], pts[0][1], cap * weight * 0.62, cap * weight * 0.62, color, alpha, solid=False)
                else:
                    tex.line(pts, color, cap * weight, alpha, solid=False)
        x += w + cap * gap
    return total


def scribble(tex, x0, x1, y, cap, color, seed=0, alpha=0.9, weight=0.2):
    """A line of small writing that is not meant to be read: uneven marks along a baseline."""
    rng = np.random.default_rng(seed)
    x = x0
    while x < x1 - cap * 0.4:
        n = int(rng.integers(2, 8))
        for _ in range(n):
            if x >= x1 - cap * 0.4:
                break
            w = cap * (0.35 + rng.random() * 0.3)
            kind = rng.integers(0, 4)
            if kind == 0:
                tex.line([(x, y), (x, y + cap)], color, cap * weight, alpha, solid=False)
            elif kind == 1:
                tex.line([(x, y + cap), (x + w, y + cap), (x + w, y), (x, y)], color, cap * weight, alpha, solid=False)
            elif kind == 2:
                tex.line([(x, y), (x + w * 0.5, y + cap), (x + w, y)], color, cap * weight, alpha, solid=False)
            else:
                tex.line([(x, y + cap), (x, y), (x + w, y)], color, cap * weight, alpha, solid=False)
            x += w + cap * 0.28
        x += cap * 0.55


# ====================================================================== patterns in a surface's own centimetres
def line_cover(dist, half, fp):
    """How much of a pixel a line covers: `dist` cm from its middle, `half` its half-width, `fp` the size
    of a pixel there in cm. Fine lines fade instead of flickering."""
    return np.clip((half + fp * 0.5 - np.abs(dist)) / np.maximum(fp, 1e-3), 0, 1) * np.clip(2.2 * half / np.maximum(fp, 1e-3) + 0.25, 0, 1)


def boards(along, across, fp, width=12.0, length=170.0, seed=0.0, gap=0.25):
    """Floorboards: -> (a tone 0..1 for every board, how much of each pixel is joint)."""
    i = np.floor(across / width)
    f = (across / width - i) * width
    off = hash2(i, 3.0, seed) * length
    j = np.floor((along + off) / length)
    g = ((along + off) / length - j) * length
    tone = hash2(i, j, seed + 1.0)
    joint = np.maximum(line_cover(np.minimum(f, width - f), gap, fp), line_cover(np.minimum(g, length - g), gap, fp) * 0.8)
    return tone, joint.astype(F32)


def repeat(u, period):
    """-> (which one, how far into it in cm)."""
    i = np.floor(u / period)
    return i, u - i * period

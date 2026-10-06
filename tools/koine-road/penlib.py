"""Reed-pen stroke model: turns centre-line skeletons into inked outlines.

A glyph is a list of strokes. A stroke is a list of points (x, y) or
(x, y, 'c') where 'c' marks a sharp corner. Smooth runs between corners are
interpolated with a centripetal Catmull-Rom spline. The pen is an elliptical
nib whose size swells at the start and end of each stroke (ink pooling) and
tapers slightly along it.
"""
import math
import hashlib
import numpy as np
from shapely.geometry import Polygon, MultiPolygon, MultiPoint
from shapely.ops import unary_union
from shapely import affinity
from shapely.geometry.polygon import orient


def seed_for(*parts):
    h = hashlib.sha256("|".join(str(p) for p in parts).encode()).digest()
    return int.from_bytes(h[:8], "big")


# ---------- path interpolation ----------

def _catmull(P, step=7.0, alpha=0.5):
    P = np.asarray(P, dtype=float)
    if len(P) == 2:
        n = max(2, int(np.linalg.norm(P[1] - P[0]) / step) + 1)
        t = np.linspace(0, 1, n)[:, None]
        return P[0] * (1 - t) + P[1] * t
    # pad ends by reflection so the curve passes through the end points
    first = P[0] + (P[0] - P[1])
    last = P[-1] + (P[-1] - P[-2])
    Q = np.vstack([first, P, last])
    out = []
    for i in range(1, len(Q) - 2):
        p0, p1, p2, p3 = Q[i - 1], Q[i], Q[i + 1], Q[i + 2]
        t0 = 0.0
        t1 = t0 + max(np.linalg.norm(p1 - p0), 1e-6) ** alpha
        t2 = t1 + max(np.linalg.norm(p2 - p1), 1e-6) ** alpha
        t3 = t2 + max(np.linalg.norm(p3 - p2), 1e-6) ** alpha
        n = max(2, int(np.linalg.norm(p2 - p1) / step) + 1)
        ts = np.linspace(t1, t2, n, endpoint=False)
        for t in ts:
            A1 = (t1 - t) / (t1 - t0) * p0 + (t - t0) / (t1 - t0) * p1
            A2 = (t2 - t) / (t2 - t1) * p1 + (t - t1) / (t2 - t1) * p2
            A3 = (t3 - t) / (t3 - t2) * p2 + (t - t2) / (t3 - t2) * p3
            B1 = (t2 - t) / (t2 - t0) * A1 + (t - t0) / (t2 - t0) * A2
            B2 = (t3 - t) / (t3 - t1) * A2 + (t - t1) / (t3 - t1) * A3
            out.append((t2 - t) / (t2 - t1) * B1 + (t - t1) / (t2 - t1) * B2)
    out.append(P[-1])
    return np.array(out)


def build_path(points, step=7.0):
    """Interpolate a stroke skeleton, honouring 'c' corner markers."""
    runs, cur = [], []
    for p in points:
        cur.append((p[0], p[1]))
        if len(p) > 2 and p[2] == "c" and len(cur) > 1:
            runs.append(cur)
            cur = [(p[0], p[1])]
    if len(cur) > 1:
        runs.append(cur)
    pieces = []
    for r in runs:
        seg = _catmull(r, step=step)
        if pieces:
            seg = seg[1:]
        pieces.append(seg)
    return np.vstack(pieces)


# ---------- the pen ----------

def _nib(a, b, theta, n=18):
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    x, y = a * np.cos(ang), b * np.sin(ang)
    c, s = math.cos(theta), math.sin(theta)
    return np.stack([x * c - y * s, x * s + y * c], axis=1)


def stroke_polygon(path, width, rng, start=0.20, end=0.14, taper=0.07,
                   lam=42.0, wobble=2.2, contrast=0.82, nib_angle=math.radians(12),
                   wscale=1.0):
    path = np.asarray(path, dtype=float)
    seg = np.linalg.norm(np.diff(path, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    L = max(s[-1], 1e-6)
    u = s / L
    scale = (1.0 + start * np.exp(-(s / lam) ** 2)
             + end * np.exp(-((L - s) / lam) ** 2) - taper * u) * wscale
    # slow thickness drift, like a pen running dry and being pressed again
    ph = rng.uniform(0, 2 * math.pi)
    scale = scale * (1.0 + 0.035 * np.sin(2 * math.pi * s / 230.0 + ph))
    # gentle lateral wobble of the hand
    if wobble and len(path) > 3:
        d = np.gradient(path, axis=0)
        nrm = np.stack([-d[:, 1], d[:, 0]], axis=1)
        nrm /= np.maximum(np.linalg.norm(nrm, axis=1, keepdims=True), 1e-6)
        p1, p2 = rng.uniform(0, 2 * math.pi, 2)
        off = wobble * (np.sin(2 * math.pi * s / 170.0 + p1) + 0.5 * np.sin(2 * math.pi * s / 71.0 + p2))
        # keep the ends where the skeleton says they are
        off = off * np.sin(np.pi * u) ** 0.5
        path = path + nrm * off[:, None]
    base = _nib(width / 2.0, width / 2.0 * contrast, nib_angle)
    hulls = []
    for i in range(len(path) - 1):
        a = base * scale[i] + path[i]
        b = base * scale[i + 1] + path[i + 1]
        hulls.append(MultiPoint(np.vstack([a, b])).convex_hull)
    if not hulls:  # a dot
        return Polygon(base * scale[0] + path[0])
    return unary_union(hulls)


def dot_polygon(x, y, r, rng):
    """An ink dot: a slightly squashed, slightly irregular blob."""
    n = 22
    ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
    rr = r * (1 + 0.06 * np.sin(2 * ang + rng.uniform(0, 6.28)) + 0.04 * np.sin(3 * ang + rng.uniform(0, 6.28)))
    return Polygon(np.stack([x + rr * np.cos(ang) * 1.06, y + rr * np.sin(ang) * 0.94], axis=1))


# ---------- ink behaviour on papyrus ----------

def _noise_field(rng, scale, octaves=7):
    waves = []
    for _ in range(octaves):
        lam = scale * rng.uniform(0.55, 2.2)
        th = rng.uniform(0, 2 * math.pi)
        k = 2 * math.pi / lam
        waves.append((k * math.cos(th), k * math.sin(th), rng.uniform(0, 2 * math.pi), rng.uniform(0.5, 1.0)))
    norm = sum(w[3] for w in waves)

    def f(x, y):
        v = 0.0
        for kx, ky, ph, amp in waves:
            v = v + amp * np.sin(kx * x + ky * y + ph)
        return v / norm
    return f


def _roughen_ring(coords, field, amp, spacing=5.0):
    pts = np.asarray(coords, dtype=float)[:-1]
    # resample the ring at even spacing
    closed = np.vstack([pts, pts[0]])
    seg = np.linalg.norm(np.diff(closed, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    L = s[-1]
    n = max(8, int(L / spacing))
    t = np.linspace(0, L, n, endpoint=False)
    x = np.interp(t, s, closed[:, 0])
    y = np.interp(t, s, closed[:, 1])
    dx = np.roll(x, -1) - np.roll(x, 1)
    dy = np.roll(y, -1) - np.roll(y, 1)
    ln = np.maximum(np.hypot(dx, dy), 1e-6)
    nx, ny = dy / ln, -dx / ln
    d = amp * field(x, y)
    return np.stack([x + nx * d, y + ny * d], axis=1)


def ink(shape, rng, pool=7.0, rough=2.0, rough_scale=30.0, simplify=0.8):
    """Fill the crotches where strokes meet, roughen the edge, tidy the outline."""
    if pool:
        shape = shape.buffer(pool, join_style=1).buffer(-pool, join_style=1)
    polys = list(shape.geoms) if isinstance(shape, MultiPolygon) else [shape]
    field = _noise_field(rng, rough_scale)
    out = []
    for p in polys:
        if p.is_empty or p.area < 30:
            continue
        ext = _roughen_ring(p.exterior.coords, field, rough)
        holes = [_roughen_ring(h.coords, field, rough) for h in p.interiors if Polygon(h).area > 60]
        q = Polygon(ext, holes)
        if not q.is_valid:
            q = q.buffer(0)
        out.append(q)
    shape = unary_union(out).simplify(simplify, preserve_topology=True)
    return shape


def polygons(shape):
    if shape.is_empty:
        return []
    geoms = list(shape.geoms) if isinstance(shape, MultiPolygon) else [shape]
    return [orient(g, sign=-1.0) for g in geoms if g.area > 20]


def transform(shape, rot_deg=0.0, scale=1.0, dx=0.0, dy=0.0, origin=(250, 300)):
    if rot_deg:
        shape = affinity.rotate(shape, rot_deg, origin=origin)
    if scale != 1.0:
        shape = affinity.scale(shape, scale, scale, origin=(origin[0], 0))
    if dx or dy:
        shape = affinity.translate(shape, dx, dy)
    return shape

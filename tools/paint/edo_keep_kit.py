"""PAINT-20E: the kit the two rooms of Himeji's keep are painted with (edo_keep.py, edo_keeptop.py): a room seen through
one camera (room.View), painted in the act's manner (S/work-20-paintA/style.md): big flat masses with a little grain
(+-3%), a thing modelled by two flats (lit, shade) with a hard edge between, one fine even contour in prussian blue
round the SILHOUETTES only (never inside a flat, never through a solid), few colours, the blue leading; then the kit's
four passes (under, strokes at the indoor sizes, details, finish). Measurements as in room.py: X across, Y up, Z out
from the back wall toward us, in cm.

How the contour is made (style.md section 4, and the round's fix): every thing is painted as flats in depth order, far
to near, and is registered with `Room.thing(mask, alpha)`: its contour is the outer boundary of its own mask (one pixel,
inside the edge), and in `contours()` each thing's line is covered by the fills of every thing painted after it, so a far
thing's line never lies over a near thing's fill, and nothing shows through a solid. Texture that is drawn (floorboard
joints) is registered the same way, with the floor's mask as its fill, so things standing on the floor cover it.

  Room       the picture, its camera, the things (fill, line) in depth order, the masks of the cut-outs (`grp`)
  flat       a polygon in the room laid down flat, with grain
  floor_uv, wall_uv   the place every pixel shows on the floor or a wall, with cm per pixel
  boards, panels, joists, post   the keep's own surfaces and parts, painted in their own centimetres
  Passes     the brush pass (sizes (9, 5, 2), keep 0.28) and the contours; finish_scene: grain, one palette, the PNGs
"""

import math
import os

import numpy as np
from PIL import Image

from brush import (F32, rgb, lerp, noise, blur, mask_poly, mask_ellipse, mask_line, Sheet, over, tint, glow, vary, strokes,
                   grain, palette_of, to_palette, save)
from room import View
from postimp_paints import PAINTS

W, H = 800, 600
SHAPE = (H, W)
LUM = np.array([0.3, 0.55, 0.15], F32)


def P(name):
    """A paint of the box, by name."""
    return rgb(PAINTS[name]["hex"])


PRUSSIAN = P("prussian-blue")
LINE = PRUSSIAN
PAPER = P("lead-white")
NAPLES = P("naples-yellow")
OCHRE = P("yellow-ochre")
SIENNA = P("burnt-sienna")
COBALT = P("cobalt-blue")
ULTRA = P("ultramarine")
CERULEAN = P("cerulean")
SHADE = lerp(ULTRA, PRUSSIAN, 0.45)       # the act's shade, indoors: ultramarine toward prussian (a dark blue, never grey)


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, F32)


def shade_of(c, k=0.35, toward=None):
    """A flat's shade flat: the lit colour pulled `k` toward the act's shade (cobalt to ultramarine), never grey."""
    t = SHADE if toward is None else col(toward)
    return lerp(col(c), t, k)


def dark_of(c, k):
    """Darker by adding prussian blue (never black)."""
    return lerp(col(c), PRUSSIAN, k)


def tint_of(c, k):
    """Lighter with lead white."""
    return lerp(col(c), PAPER, k)


def boundary(m):
    """The outer edge of a mask, one pixel wide, inside it."""
    b = m >= 0.5
    e = b.copy()
    e[1:, :] &= b[:-1, :]
    e[:-1, :] &= b[1:, :]
    e[:, 1:] &= b[:, :-1]
    e[:, :-1] &= b[:, 1:]
    return (b & ~e).astype(F32)


class Room:
    """A picture of a room through one camera. `grp` names the cut-out a thing belongs to: its hard mask is kept."""

    def __init__(self, view, seed=1, base="#1e2438"):
        self.V = view
        self.img = np.zeros((H, W, 3), F32) + col(base)[None, None, :]
        self.masks = {}
        self.seed = seed
        self.things = []                      # (fill mask, line mask, colour, alpha) in depth order, far to near
        self.n = 0

    def _seed(self):
        self.n += 1
        return self.seed * 1000 + self.n

    def mask(self, grp):
        return self.masks.setdefault(grp, np.zeros(SHAPE, F32))

    def add_mask(self, grp, m):
        if grp:
            self.masks[grp] = np.maximum(self.mask(grp), m)

    def flat(self, pts, color, grp=None, amount=0.03, cell=90, warm=0.0, alpha=1.0, wobble=0.0, soft=0.0):
        """A polygon in the room (3-D points) filled flat with grain. -> its mask."""
        pp = self.V.poly(pts)
        if len(pp) < 3:
            return np.zeros(SHAPE, F32)
        return self.flat2d(pp, color, grp, amount, cell, warm, alpha, wobble, soft)

    def flat2d(self, pp, color, grp=None, amount=0.03, cell=90, warm=0.0, alpha=1.0, wobble=0.0, soft=0.0):
        m = mask_poly(SHAPE, pp, wobble=wobble, seed=self._seed(), soft=soft)
        field = vary(color, SHAPE, self._seed(), amount=amount, cell=cell, warm=warm)
        over(self.img, field, m * alpha)
        self.add_mask(grp, m)
        return m

    def fill(self, m, color, amount=0.03, cell=90, warm=0.0, alpha=1.0):
        field = vary(color, SHAPE, self._seed(), amount=amount, cell=cell, warm=warm)
        over(self.img, field, m * alpha)
        return m

    def shade(self, m, k=0.35, toward=None):
        """A cast shadow or a shade: the picture under the mask pulled `k` toward the act's shade (hard-edged, no line)."""
        t = (SHADE if toward is None else col(toward))[None, None, :]
        mm = np.clip(m, 0, 1)[..., None] * k
        self.img[...] = self.img * (1 - mm) + t * mm

    def thing(self, m, alpha=0.85, color=None, line=None):
        """Register a thing painted (its mask) so that its silhouette gets the contour, covered by nearer things."""
        ln = boundary(m) if line is None else line
        self.things.append((np.clip(m, 0, 1), ln, LINE if color is None else col(color), alpha))

    def lines(self, m_fill, m_line, alpha=0.3, color=None):
        """Drawn texture (floorboard joints): lines registered with the surface's own mask as their fill."""
        self.things.append((np.clip(m_fill, 0, 1), np.clip(m_line, 0, 1), LINE if color is None else col(color), alpha))

    def contours(self, pic):
        """Lay every thing's contour, each covered by the fills of the things painted after it (nearer)."""
        cover = np.zeros(SHAPE, bool)
        out = pic.copy()
        layers = []
        for fill, line, color, alpha in reversed(self.things):
            vis = line * (~cover)
            layers.append((vis, color, alpha))
            cover |= fill >= 0.5
        for vis, color, alpha in reversed(layers):
            over(out, color, vis * alpha)
        return out

    # ------------------------------------------------------------ surfaces, pixel by pixel
    def floor_uv(self, Y=0.0):
        X, Z, ok = self.V.floor_xz(SHAPE, Y)
        d = self.V.depth_map(SHAPE, Y)
        fp = np.clip(d / self.V.F, 0.05, 50)             # cm per pixel there
        return X, Z, ok, fp

    def wall_uv(self, axis, at):
        u, v, ok = self.V.plane_uv(SHAPE, axis, at)
        if axis == "Z":
            d = np.abs(self.V.cam_space(u, v, at)[2])
        else:
            d = np.abs(self.V.cam_space(at, v, u)[2])
        fp = np.clip(d / self.V.F, 0.05, 50)
        return u, v, ok, fp


def thin(u, period, fp, offset=0.0):
    """A one-pixel line every `period` cm along u (anti-aliased in cm)."""
    f = np.mod(u - offset, period)
    f = np.minimum(f, period - f)
    return np.clip(1 - f / (fp * 0.7 + 1e-6) + 0.5, 0, 1)


def band_id(u, period, offset=0.0):
    return np.floor((u - offset) / period).astype(np.int64)


def hash01(i, seed=0):
    x = (i * 2654435761 + seed * 97) & 0xFFFFFFFF
    x = (x ^ (x >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((x ^ (x >> 16)) & 0xFFFF).astype(F32) / 65535.0


def boards(room, m, color, along="Z", width=30.0, offset=0.0, amount=0.03, Y=0.0, seed=3, line_alpha=0.3, per_board=0.03):
    """A boarded floor (or any level plane at Y): one flat, each board its own shade by a hair, the joints drawn as
    lines (registered as texture: things standing on the floor cover them)."""
    X, Z, ok, fp = room.floor_uv(Y)
    u, w = (X, Z) if along == "Z" else (Z, X)
    ids = band_id(u, width, offset)
    k = hash01(ids, seed) - 0.5
    base = col(color)[None, None, :] * (1 + per_board * 2 * k[..., None])
    base = base * (1 + 2 * amount * (noise(SHAPE, 90, seed + 11, 3) - 0.5))[..., None]
    mm = m * ok
    over(room.img, np.clip(base, 0, 1), mm)
    j = thin(u, width, fp, offset)
    per = 180.0 + 140.0 * hash01(ids, seed + 5)
    off = per * hash01(ids, seed + 9)
    b = thin(w, per, fp, off)
    room.lines(mm, np.maximum(j, b * 0.8) * mm, line_alpha)
    return mm


def panels(room, m, axis, at, plaster, post, sill, length, height, post_every=190.0, post_w=22.0, offset=0.0, sill_h=28.0,
           lintel_h=22.0, nageshi=None, seed=4, amount=0.03, alpha=0.6, lit=None, shade_k=0.0, posts=True, post_at=None, cut=None):
    """A keep's wall: lime-plastered panels (one flat; `lit(u)` may give each panel's light, 0..1, as a step) between
    dark wooden posts, a sill beam along the foot, a lintel along the top, a nageshi rail: each a flat with its contour."""
    u, v, ok, fp = room.wall_uv(axis, at)
    mm = m * ok
    pl = vary(plaster, SHAPE, seed, amount=amount, cell=90, warm=0.01)
    if lit is not None:
        k = lit(u)
        shade = shade_of(plaster, 0.35)
        pl = lerp(shade[None, None, :], pl, np.clip(k, 0, 1)[..., None])
    if shade_k:
        pl = lerp(pl, shade_of(plaster, 1.0)[None, None, :], shade_k)
    if cut is not None:
        mm = mm * (1 - np.clip(cut, 0, 1))
    over(room.img, np.clip(pl, 0, 1), mm)
    room.thing(mm, alpha)
    V = room.V

    def quad(u0, u1, v0, v1):
        if axis == "Z":
            pts = [(u0, v0, at), (u1, v0, at), (u1, v1, at), (u0, v1, at)]
        else:
            pts = [(at, v0, u0), (at, v0, u1), (at, v1, u1), (at, v1, u0)]
        return V.poly(pts)
    wood = post
    if posts:
        xs = list(post_at) if post_at is not None else list(np.arange(offset, length, post_every))
        for x in xs:
            pp = quad(max(0.0, x), min(length, x + post_w), 0.0, height)
            if len(pp) >= 3:
                mk = room.flat2d(pp, wood, amount=0.03, cell=(12, 90) if axis == "Z" else (90, 12))
                room.thing(mk * mm, alpha)
    for (v0, v1) in ((0.0, sill_h), (height - lintel_h, height)) + ((nageshi,) if nageshi else ()):
        if v1 <= v0:
            continue
        pp = quad(0.0, length, v0, v1)
        if len(pp) >= 3:
            mk = room.flat2d(pp, sill, amount=0.03, cell=90)
            if cut is not None:
                mk = mk * (1 - np.clip(cut, 0, 1))
            room.thing(mk * mm, alpha)
    return mm, (u, v, ok, fp)


def joists(room, m, Y, color, dark, along="Z", every=90.0, width=24.0, offset=0.0, X0=0.0, X1=800.0, Z0=0.0, Z1=1000.0, seed=6, alpha=0.5):
    """The underside of the floor above: one flat of boards, with dark joists every `every` cm as flats of their own."""
    X, Z, ok, fp = room.floor_uv(Y)
    mm = m * ok
    room.fill(mm, color, amount=0.03, cell=90)
    V = room.V
    u = offset
    while u < (X1 if along == "Z" else Z1):
        if along == "Z":
            pts = [(u, Y, Z0), (u + width, Y, Z0), (u + width, Y, Z1), (u, Y, Z1)]
        else:
            pts = [(X0, Y, u), (X1, Y, u), (X1, Y, u + width), (X0, Y, u + width)]
        pp = V.poly(pts)
        if len(pp) >= 3:
            mk = room.flat2d(pp, dark, amount=0.03, cell=90) * mm
            room.thing(mk, alpha)
        u += every
    return mm


def post(room, X, Z, r, Y0, Y1, color, lit_from=(1.0, -0.4), lit_share=0.26, grp=None, alpha=0.85, shade_k=0.4):
    """A round post (the great pillar, a tub) seen from the front: its silhouette through the camera, as TWO flats: the
    shade flat and a lit flat along the side the light comes from (`lit_from`: a direction on the floor plan; the lit
    flat takes `lit_share` of the width, on that side). -> (mask, (xl, xr, top, bottom))."""
    V = room.V
    # the silhouette: the tangent points, seen from the camera; the top and bottom as ellipses' outer edges
    dx, dz = X - V.cam_x, Z - V.cam_z
    d = math.hypot(dx, dz)
    a = math.atan2(dz, dx)
    t = math.asin(min(1.0, r / d))
    pts = []
    for ang in np.linspace(a + math.pi / 2 - t * 0 + t, a + math.pi * 1.5 - t, 12):
        pass
    # the ring of the top and of the foot, projected, and their hull
    ring = lambda Y: [V.pt(X + r * math.cos(q), Y, Z + r * math.sin(q)) for q in np.linspace(0, 2 * math.pi, 28, endpoint=False)]
    pp = _hull(ring(Y0) + ring(Y1))
    m = mask_poly(SHAPE, pp)
    shade = shade_of(color, shade_k)
    room.fill(m, shade, amount=0.03, cell=(12, 90))
    # the lit sliver: the side toward the light
    side = 1.0 if lit_from[0] >= 0 else -1.0
    xs = [p[0] for p in pp]
    xl, xr = min(xs), max(xs)
    w = (xr - xl) * lit_share
    lit_m = m * (np.mgrid[0:H, 0:W][1] >= (xr - w) if side > 0 else np.mgrid[0:H, 0:W][1] <= (xl + w))
    room.fill(lit_m, color, amount=0.03, cell=(12, 90))
    room.add_mask(grp, m)
    room.thing(m, alpha)
    ys = [p[1] for p in pp]
    return m, (xl, xr, min(ys), max(ys))


def _hull(points):
    pts = sorted(set((float(x), float(y)) for x, y in points))
    if len(pts) <= 2:
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


def box(room, X0, X1, Y0, Y1, Z0, Z1, color, grp=None, alpha=0.85, lit=("top", "right"), shade_k=0.35, amount=0.03, wobble=0.0):
    """A box as flats: its lit faces in `color`, the others its shade; one silhouette contour round the whole."""
    m = np.zeros(SHAPE, F32)
    for name, pp, n in room.V.box(X0, X1, Y0, Y1, Z0, Z1):
        c = color if name in lit else shade_of(color, shade_k)
        m = np.maximum(m, room.flat2d(pp, c, amount=amount, cell=60, wobble=wobble))
    room.add_mask(grp, m)
    room.thing(m, alpha)
    return m


class Passes:
    def __init__(self, seed=1):
        self.seed = seed

    def paint(self, pic, keep=0.28, sizes=(9, 5, 2)):
        return np.clip(strokes(pic, sizes=sizes, seed=self.seed, keep=keep, density=1.4, jitter=0.025), 0, 1)


def finish_scene(folder, pictures, colors=160, seed=9, speckle=0.012, amount=0.02):
    """Grain (the paper's tooth), one palette for all the scene's files, and the PNGs. `pictures`: {name: (rgb, alpha or None)}."""
    os.makedirs(folder, exist_ok=True)
    grained = {n: grain(p, seed + i, amount) for i, (n, (p, a)) in enumerate(pictures.items())}
    sample = [grained[n] if a is None else grained[n][a >= 0.5] for n, (p, a) in pictures.items()]
    sample = [s.reshape(-1, 3) for s in sample]
    sample = [s.reshape(-1, 1, 3) for s in sample if len(s)]
    pal = palette_of(sample, colors=colors, seed=seed)
    for n, (p, a) in pictures.items():
        idx = to_palette(grained[n], pal, seed=seed + 1, speckle=speckle)
        save(os.path.join(folder, n + ".png"), idx, pal, alpha=None if a is None else a)


def save_rgba(path, rgb_, alpha):
    """A light picture: RGBA with a soft alpha (a frame for the paints: keyed colour by colour, its alpha kept)."""
    a = np.clip(alpha, 0, 1)
    out = np.dstack([np.clip(rgb_, 0, 1), a])
    Image.fromarray(np.clip(np.round(out * 255), 0, 255).astype(np.uint8), "RGBA").save(path, optimize=True)


def to_image(a):
    return Image.fromarray(np.clip(np.round(a * 255), 0, 255).astype(np.uint8))


def ipt(p):
    return [int(round(p[0])), int(round(p[1]))]


def stand_in(img, x, y, h_px, color="#d8d0c0"):
    """A stand-in person: a plain upright figure, feet at (x, y), `h_px` tall, for the check pictures."""
    sh = Sheet(SHAPE)
    w = h_px * 0.26
    sh.ellipse(x, y - h_px * 0.88, h_px * 0.085, h_px * 0.1, color)
    sh.poly([(x - w / 2, y - h_px * 0.78), (x + w / 2, y - h_px * 0.78), (x + w * 0.4, y - h_px * 0.4), (x + w * 0.3, y), (x - w * 0.3, y), (x - w * 0.4, y - h_px * 0.4)], color)
    sh.line([(x - w * 0.45, y + 1), (x + w * 0.45, y + 1)], "#1a2846", 1.5)
    sh.onto(img)
    return img

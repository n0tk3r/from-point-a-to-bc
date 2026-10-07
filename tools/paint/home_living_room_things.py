"""The furniture that people can walk behind, each one a cut-out: the desk with the family computer, the
piano and its stool, the dining table with its chairs and the lamp over it, Dad's armchair and his lamp.

Every piece is a function (L, fine). With fine=False it lays in the big faces (to be brushed over);
with fine=True it adds the crisp small things on top. Called with a Collector it only reports its boxes.
A piece is made of parts, given from the farthest to the nearest, so that the small things of a part
behind are not drawn over a part in front."""

from home_living_room_plan import *

SEED = 105
DARK, GLINT = "#160e14", "#ffe2a8"
COVER = {}


def run(L, fine, name, parts):
    """`parts`: (lay_in, finish) pairs, farthest first. lay_in(L) paints a part's faces; finish() returns
    the sheets of its crisp small things. Either may be None."""
    if isinstance(L, Collector):
        for lay, _ in parts:
            if lay:
                lay(L)
        return
    if not fine:
        cov = []
        for lay, _ in parts:
            t = Layer()
            if lay:
                lay(t)
            cov.append(t.w.copy())
            t.onto(L)
        COVER[name] = cov
        return
    cov = COVER[name]
    for i, (_, fin) in enumerate(parts):
        if fin is None:
            continue
        hide = np.zeros((H, W), dtype=F32)
        for c in cov[i + 1:]:
            hide = np.maximum(hide, c)
        hide = np.clip(hide * 1.6, 0, 1)
        for s in fin():
            L.sheet(s, hide=hide)


def seg(s, pts, color, width=1.0, alpha=1.0):
    s.line(pts2(pts), color, width, alpha)


def quad(s, pts, color, alpha=1.0):
    s.poly(pts2(pts), color, alpha)


def ring(cx, y, cz, rx, rz, n=20, a0=0.0, a1=360.0):
    """Points round a level circle (or part of one) in the room."""
    return [(cx + math.cos(math.radians(lerp(a0, a1, i / n))) * rx, y, cz + math.sin(math.radians(lerp(a0, a1, i / n))) * rz) for i in range(n + 1)]


def disc(s, cx, y, cz, rx, rz, color, alpha=1.0):
    s.poly(pts2(ring(cx, y, cz, rx, rz)[:-1]), color, alpha)


def shade(s, pos, y0, y1, r0, r1, glow_c, edge_c, top_c=None, ribs=0, fringe=None):
    """A lampshade seen a little from above: a cone cut off at the top (radius r1 at height y1) and open
    at the bottom (r0 at y0). It is lit from inside, so it is brightest down its middle."""
    x, _, z = pos
    lo = [(x + math.cos(math.radians(a)) * r0, y0, z - math.sin(math.radians(a)) * r0 * 0.9) for a in np.linspace(0, 180, 25)]
    hi = [(x + math.cos(math.radians(a)) * r1, y1, z - math.sin(math.radians(a)) * r1 * 0.9) for a in np.linspace(0, 180, 25)]
    s.poly(pts2(lo) + list(reversed(pts2(hi))), edge_c)
    for f, c in ((0.80, lerp(col(edge_c), col(glow_c), 0.5)), (0.56, col(glow_c)), (0.26, lerp(col(glow_c), col("#ffffff"), 0.5))):
        lo2 = [(x + (px_ - x) * f, y, pz) for px_, y, pz in lo]
        hi2 = [(x + (px_ - x) * f, y, pz) for px_, y, pz in hi]
        s.poly(pts2(lo2) + list(reversed(pts2(hi2))), c)
    for k in range(ribs):
        a = math.radians(8 + 164 * (k + 0.5) / ribs)
        s.line(pts2([(x + math.cos(a) * r0, y0, z - math.sin(a) * r0 * 0.9), (x + math.cos(a) * r1, y1, z - math.sin(a) * r1 * 0.9)]), edge_c, 0.7, 0.38)
    if top_c is not None:                                               # the hole at the top, and the light in it
        s.poly(pts2(ring(x, y1, z, r1, r1 * 0.9)[:-1]), edge_c)
        s.poly(pts2(ring(x, y1 - 0.5, z, r1 * 0.78, r1 * 0.7)[:-1]), top_c)
    s.line(pts2(lo), lerp(col(edge_c), col("#3a2414"), 0.4), 1.1, 0.9)
    if fringe:
        for i in range(0, len(lo) - 1):
            a, b = P(*lo[i]), P(*lo[i + 1])
            for t in (0.0, 0.5):
                fx, fy = lerp(a[0], b[0], t), lerp(a[1], b[1], t)
                s.line([(fx, fy), (fx, fy + fringe)], glow_c if (i % 2) else edge_c, 0.8, 0.9)


class Turned:
    """Something standing at (cx, cz) and turned `ang` degrees: gives places and directions in its own
    measurements (lx across it, lz from its front (-) to its back (+))."""

    def __init__(self, cx, cz, ang):
        self.cx, self.cz, self.ang = cx, cz, ang

    def p(self, lx, y, lz):
        x, z = turn(self.cx, self.cz, self.cx + lx, self.cz + lz, self.ang)
        return (x, y, z)

    def n(self, nx, ny, nz):
        x, z = turn(0.0, 0.0, nx, nz, self.ang)
        k = math.sqrt(x * x + ny * ny + z * z) + 1e-9
        return (x / k, ny / k, z / k)

    def local(self, X, Z):
        xx, zz = X - self.cx, Z - self.cz
        ca, sa = math.cos(math.radians(-self.ang)), math.sin(math.radians(-self.ang))
        return xx * ca - zz * sa, xx * sa + zz * ca

    def face(self, L, pts, albedo, n, **kw):
        return Fc(L, [self.p(*q) for q in pts], albedo, n=self.n(*n), **kw)


def rrect(cx, cy, w, h, r, n=4):
    """The outline of a rectangle with rounded corners, as (u, v) points going round counter-clockwise."""
    out = []
    for (sx, sy, a0) in ((1, -1, -90), (1, 1, 0), (-1, 1, 90), (-1, -1, 180)):
        ox, oy = cx + sx * (w / 2 - r), cy + sy * (h / 2 - r)
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            out.append((ox + math.cos(a) * r, oy + math.sin(a) * r))
    return out


def _sees(t, mid, n_local):
    wn = t.n(*n_local)
    return np.dot(np.asarray(wn), CAM_POS - np.asarray(t.p(*mid))) > 0


def prism_y(L, t, outline, y0, y1, side, top=None, cast=True, **kw):
    """Something with the floor plan `outline` ((lx, lz) points) standing from y0 up to y1: the sides we
    can see, then its top."""
    xs, zs = [p[0] for p in outline], [p[1] for p in outline]
    if isinstance(L, Collector):
        if cast:
            L.boxes.append([t.p(x, y, z) for y in (y0, y1) for (x, z) in ((min(xs), min(zs)), (max(xs), min(zs)), (max(xs), max(zs)), (min(xs), max(zs)))])
        return
    cx, cz = sum(xs) / len(xs), sum(zs) / len(zs)
    n = len(outline)
    for i in range(n):
        (xa, za), (xb, zb) = outline[i], outline[(i + 1) % n]
        nx, nz = (zb - za), -(xb - xa)
        if nx * ((xa + xb) / 2 - cx) + nz * ((za + zb) / 2 - cz) < 0:
            nx, nz = -nx, -nz
        if _sees(t, ((xa + xb) / 2, (y0 + y1) / 2, (za + zb) / 2), (nx, 0, nz)):
            t.face(L, [(xa, y0, za), (xb, y0, zb), (xb, y1, zb), (xa, y1, za)], side, (nx, 0, nz), **kw)
    t.face(L, [(x, y1, z) for x, z in outline], top if top is not None else side, (0, 1, 0), **kw)


def prism_z(L, t, outline, z0, z1, face_c, edge_c=None, **kw):
    """Something whose front is `outline` ((lx, y) points), from z0 (toward its own front) back to z1:
    the edges we can see, then whichever of its two faces is turned to us."""
    if isinstance(L, Collector):
        return
    xs, ys = [p[0] for p in outline], [p[1] for p in outline]
    cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
    n = len(outline)
    for i in range(n):
        (xa, ya), (xb, yb) = outline[i], outline[(i + 1) % n]
        nx, ny = (yb - ya), -(xb - xa)
        if nx * ((xa + xb) / 2 - cx) + ny * ((ya + yb) / 2 - cy) < 0:
            nx, ny = -nx, -ny
        if _sees(t, ((xa + xb) / 2, (ya + yb) / 2, (z0 + z1) / 2), (nx, ny, 0)):
            t.face(L, [(xa, ya, z0), (xb, yb, z0), (xb, yb, z1), (xa, ya, z1)], edge_c if edge_c is not None else face_c, (nx, ny, 0), **kw)
    if _sees(t, (cx, cy, z0), (0, 0, -1)):
        t.face(L, [(x, y, z0) for x, y in outline], face_c, (0, 0, -1), **kw)
    else:
        t.face(L, [(x, y, z1) for x, y in outline], face_c, (0, 0, 1), **kw)


# ---------------------------------------------------------------- a dining chair
WALNUT = "#7c4a2a"


def chair_lay(L, cx, cz, ang, toward=1, seed=0):
    """A ladder-back chair with a rush seat, standing at (cx, cz), turned `ang` degrees.
    toward=1: its back is to us; toward=-1: it faces us."""
    kw = dict(ang=ang, about=(cx, cz))
    wd = grainy(WALNUT, SEED + seed, "y", 0.10, (40, 5))
    rush = mottled("#d6b062", SEED + seed + 1, 0.10, 6)
    zb, zf = cz - 18.5 * toward, cz + 18.5 * toward                     # back posts, front legs

    def posts(z, h, cast=False):
        for sx in (-20.5, 15.5):
            B(L, cx + sx, cx + sx + 5, 0, h, z - 2.5, z + 2.5, wd, cast=cast, **kw)

    def back():
        posts(zb, 95, cast=True)
        for y0, y1 in ((55, 62), (69, 76), (83, 92)):
            B(L, cx - 16, cx + 16, y0, y1, zb - 1.3, zb + 1.3, wd, **kw)

    def front():
        posts(zf, 44)
        B(L, cx - 17, cx + 17, 17, 20.5, zf - 1.2, zf + 1.2, wd, cast=False, **kw)

    def seat():
        B(L, cx - 21.5, cx + 21.5, 43, 47, cz - 21, cz + 21, wd, top=rush, **kw)
    for part in ((front, seat, back) if toward > 0 else (back, seat, front)):
        part()


def chair_fine(s, cx, cz, ang, toward=1):
    t = Turned(cx, cz, ang)
    hi = lambda pos, a=1.0: lit("#d89a62", pos, (0, 1, 0), a)
    e = 21.5
    cnr = [t.p(-e, 47.2, -21), t.p(e, 47.2, -21), t.p(e, 47.2, 21), t.p(-e, 47.2, 21)]
    mid = t.p(0, 47.2, 0)
    for c in cnr:                                                        # the rush is woven in four triangles
        seg(s, [c, mid], "#6a4a1c", 0.8, 0.5)
    for f in (0.36, 0.68):
        rr = [tuple(lerp(mid[i], c[i], f) for i in range(3)) for c in cnr]
        seg(s, rr + [rr[0]], "#6a4a1c", 0.6, 0.32)
    seg(s, cnr + [cnr[0]], hi(mid), 0.9, 0.6)
    seg(s, [t.p(-e, 43, -21.2), t.p(e, 43, -21.2)], DARK, 1.0, 0.5)
    zl = -18.5 * toward
    for y0, y1 in ((55, 62), (69, 76), (83, 92)):                        # the slats: light on top, dark beneath
        seg(s, [t.p(-16, y1, zl - 1.3), t.p(16, y1, zl - 1.3)], hi(t.p(0, y1, zl)), 0.9, 0.8)
        seg(s, [t.p(-16, y0, zl - 1.3), t.p(16, y0, zl - 1.3)], DARK, 0.8, 0.5)
    for sx in (-20.5, 20.5):                                             # the posts: a lit edge, a turned knob on top
        seg(s, [t.p(sx, 2, zl - 2.5), t.p(sx, 95, zl - 2.5)], hi(t.p(sx, 60, zl), 0.9), 0.7, 0.45)
        c = P(*t.p(sx * 0.88, 97.5, zl))
        s.ellipse(c[0], c[1], 2.3, 2.1, lit("#a8693c", t.p(sx, 98, zl)))
        s.ellipse(c[0] - 0.6, c[1] - 0.6, 0.9, 0.8, hi(t.p(sx, 98, zl)))


# ---------------------------------------------------------------- the dining table, set for five
def table(L, fine=False):
    t = TABLE
    x0, x1, z0, z1, top = t["x0"], t["x1"], t["z0"], t["z1"], t["top"]
    xm, mid = (x0 + x1) / 2, (z0 + z1) / 2
    far = [(x0 + 34, z1 + 36, 14, 3), (xm + 2, z1 + 43, -9, 4), (x1 - 30, z1 + 31, 24, 5)]      # pushed back as three people left them
    near = [(x0 + 52, z0 - 36, -5, 6), (x1 - 52, z0 - 32, 8, 7)]                               # and two that nobody has sat in
    red = col("#8a3a34") * 0.75

    def cloth(X, Y, Z):                                                  # linen with two woven red lines near its edge
        e = np.minimum(np.minimum(X - (x0 - 1.5), (x1 + 1.5) - X), np.minimum(Z - (z0 - 1.5), (z1 + 1.5) - Z))
        base = col("#7f7a6e")[None, None, :] * (1 + ((wnoise(X, Z, 40, SEED + 10) - 0.5) * 0.06)[..., None])
        line = ((e > 7.0) & (e < 9.6)) | ((e > 11.6) & (e < 12.9))
        return np.where(line[..., None], red[None, None, :], base)

    def fall(X, Y, Z):                                                   # the part that hangs, turned from the lamp
        base = col("#bdb7b4")[None, None, :] * (1 + ((wnoise(X + Z, Y, 30, SEED + 12) - 0.5) * 0.06)[..., None])
        line = ((Y > top - 15.5) & (Y < top - 13.0)) | ((Y > top - 18.6) & (Y < top - 17.4))
        return np.where(line[..., None], col("#9a5a56")[None, None, :], base)
    yt = top + 0.3

    def lay_far(L):
        for (cx, cz, a, sd) in far:
            chair_lay(L, cx, cz, a, toward=-1, seed=sd)

    def fine_far():
        s = Sheet(SHAPE)
        for (cx, cz, a, sd) in far:
            chair_fine(s, cx, cz, a, toward=-1)
        return [s]

    def lay_table(L):
        for (lx, lz) in ((x0 + 9, z1 - 9), (x1 - 9, z1 - 9), (x0 + 9, z0 + 9), (x1 - 9, z0 + 9)):
            B(L, lx - 4.5, lx + 4.5, 0, 54, lz - 4.5, lz + 4.5, grainy(WALNUT, SEED + 11, "y"), cast=False)
        # the cloth: the top in the full light of the lamp; where it hangs, it turns from the light
        B(L, x0 - 1.5, x1 + 1.5, top - 25, top, z0 - 1.5, z1 + 1.5, cloth, front=fall, side=fall)

    def fine_table():
        s = Sheet(SHAPE)
        zf = z0 - 1.7
        hem = lambda X: LIGHTS.paint("#bdb7b4", (X, top - 25, zf), (0, 0, -1))
        # (straight under the lamp everything would bleach to white: the things on the table are painted
        # as if half as pale as they are, the way the cloth is, so that they keep their colors)
        lit = lambda albedo, pos, n=(0, 1, 0), dim=1.0: LIGHTS.paint(albedo, pos, n, dim * 0.52)
        for i in range(20):                                             # the hem, in scallops
            xa = lerp(x0 - 1.5, x1 + 1.5, i / 20)
            xb = lerp(x0 - 1.5, x1 + 1.5, (i + 1) / 20)
            quad(s, [(xa, top - 24.5, zf), (xb, top - 24.5, zf), ((xa + xb) / 2 + 2.6, top - 28.5, zf), ((xa + xb) / 2 - 2.6, top - 28.5, zf)], hem((xa + xb) / 2))
            c = P((xa + xb) / 2, top - 22, zf)
            s.ellipse(c[0], c[1], 0.8, 0.8, "#8a86a0", 0.6)                                  # a little cut-work above each one
        for xx in (x0 + 6, x0 + 60, xm + 34, x1 - 5):                                        # folds where it hangs
            seg(s, [(xx, top - 23, zf), (xx + 1.5, top - 1, zf)], "#6a6680", 1.0, 0.30)
            seg(s, [(xx + 2.5, top - 23, zf), (xx + 4, top - 1, zf)], "#ffffff", 0.8, 0.22)
        seg(s, [(x0 - 1.5, top, zf), (x1 + 1.5, top, zf)], "#fffdf2", 1.1, 0.9)              # the table's edge under the cloth
        seg(s, [(x1 + 1.6, top, z0 - 1.5), (x1 + 1.6, top, z1 + 1.5)], "#fffdf2", 0.9, 0.7)
        seg(s, [(x0 - 1.5, top, z1 + 1.5), (x1 + 1.5, top, z1 + 1.5)], "#8a86a0", 0.8, 0.45)
        seg(s, [(xm, yt, z0), (xm, yt, z1)], "#a8a4b8", 0.8, 0.36)                           # the creases of the iron
        seg(s, [(x0, yt, mid), (x1, yt, mid)], "#a8a4b8", 0.8, 0.30)

        def china(px_, pz, rx, rz, up):
            disc(s, px_ + 2.0, yt, pz - 1.6, rx + 1.2, rz + 0.8, "#57546e", 0.42)            # its shadow on the cloth
            disc(s, px_, yt + 0.5, pz, rx, rz, lit("#fbf8ee", up))
            disc(s, px_, yt + 0.6, pz, rx * 0.86, rz * 0.86, lit("#3f68a8", up))             # a blue band round the rim
            disc(s, px_, yt + 0.6, pz, rx * 0.76, rz * 0.76, lit("#fbf8ee", up))
            disc(s, px_, yt + 0.6, pz, rx * 0.58, rz * 0.58, lit("#e4decc", up))
            seg(s, ring(px_, yt + 0.6, pz, rx, rz, 20, 200, 340), "#ffffff", 0.7, 0.9)

        def place(px_, pz, full, seed, side):
            """One place: plate, knife and fork, glass, napkin. `full` = nobody came to eat it.
            `side` is -1 for the places on our side of the table, 1 for the far side."""
            rng = np.random.default_rng(SEED + seed)
            up = (px_, yt, pz)
            china(px_, pz, 14.5, 12.5, up)
            if full:                                                    # cold chicken, potatoes, peas: untouched
                disc(s, px_ - 3.6, yt + 1.4, pz + 1.8, 6.6, 4.6, lit("#a8642c", up))
                disc(s, px_ - 4.6, yt + 2.4, pz + 2.6, 4.2, 2.8, lit("#d89850", up))
                seg(s, [(px_ - 8.5, yt + 1.6, pz + 0.5), (px_ - 11.5, yt + 1.6, pz - 1.5)], lit("#f6eedc", up), 1.3)
                for k in range(3):
                    disc(s, px_ + 3.2 + k * 2.6 - 1.5, yt + 1.4, pz + 3.8 - k * 2.6, 3.0, 2.5, lit("#f6d870", up))
                    disc(s, px_ + 2.6 + k * 2.6 - 1.5, yt + 2.0, pz + 4.2 - k * 2.6, 1.3, 1.0, lit("#fff0b0", up))
                disc(s, px_ + 1.5, yt + 0.9, pz - 4.6, 5.2, 3.0, lit("#4f8a30", up), 0.9)
                for k in range(12):
                    disc(s, px_ + 1.5 + rng.normal(0, 2.4), yt + 1.2, pz - 4.6 + rng.normal(0, 1.4), 1.1, 1.0, lit("#7fbc4a", up))
            else:                                                       # eaten: a bone, a smear of gravy, a pea or two
                disc(s, px_ + 2, yt + 0.8, pz - 1, 5.5, 3.6, lit("#b89264", up), 0.45)
                seg(s, [(px_ - 5, yt + 1, pz + 3), (px_ + 0.5, yt + 1, pz + 0.5)], lit("#f4ecd8", up), 1.3)
                for k in range(2):
                    disc(s, px_ + 5 + rng.normal(0, 2), yt + 1.0, pz + rng.normal(0, 2), 1.0, 0.9, lit("#7fbc4a", up))
            silver = lit("#9aa4b0", up)
            if full:                                                    # knife and fork laid straight, the napkin still folded
                seg(s, [(px_ + 18.5, yt + 0.6, pz - 10), (px_ + 18.5, yt + 0.6, pz + 10)], silver, 1.1)
                seg(s, [(px_ - 18.5, yt + 0.6, pz - 10), (px_ - 18.5, yt + 0.6, pz + 10)], silver, 1.1)
                quad(s, [(px_ - 30, yt + 0.5, pz - 8), (px_ - 22, yt + 0.5, pz - 8), (px_ - 22, yt + 0.5, pz + 8), (px_ - 30, yt + 0.5, pz + 8)], lit("#c8473c", up))
                seg(s, [(px_ - 30, yt + 0.6, pz), (px_ - 22, yt + 0.6, pz)], lit("#8a2c28", up), 0.7, 0.8)
            else:                                                       # left across the plate, the napkin thrown down
                seg(s, [(px_ - 8, yt + 1.2, pz - 6), (px_ + 9, yt + 1.2, pz + 5)], silver, 1.1)
                seg(s, [(px_ - 4, yt + 1.2, pz - 8), (px_ + 12, yt + 1.2, pz + 2)], silver, 1.1)
                cr = [(px_ - 29 + rng.normal(0, 1.5), yt + 0.5, pz - 6 + rng.normal(0, 2)), (px_ - 19, yt + 0.5, pz - 9), (px_ - 17 + rng.normal(0, 1.5), yt + 0.5, pz + 2), (px_ - 23, yt + 0.5, pz + 9), (px_ - 31, yt + 0.5, pz + 3)]
                quad(s, [(x + 1.5, y - 0.2, z - 1.5) for x, y, z in cr], "#57546e", 0.35)
                quad(s, cr, lit("#c8473c", up))
                seg(s, [cr[0], cr[2]], lit("#8a2c28", up), 0.7, 0.8)
                seg(s, [cr[1], cr[3]], lit("#e8786a", up), 0.7, 0.7)
            # the glass: full for the two, drained for the three
            gx, gz = px_ + 18, pz + 13 * side
            a, b = P(gx, yt, gz), P(gx, yt + 12, gz)
            s.ellipse(a[0] + 1.5, a[1] + 0.6, 3.6, 1.6, "#57546e", 0.35)
            s.poly([(a[0] - 2.4, a[1]), (a[0] + 2.4, a[1]), (b[0] + 3.0, b[1]), (b[0] - 3.0, b[1])], lit("#b8d0dc", up), 0.6)
            if full:
                m = P(gx, yt + 9, gz)
                s.poly([(a[0] - 2.4, a[1]), (a[0] + 2.4, a[1]), (m[0] + 2.8, m[1]), (m[0] - 2.8, m[1])], lit("#e09a38", up), 0.92)
            s.line([(a[0] - 2.4, a[1]), (b[0] - 3.0, b[1])], "#ffffff", 0.8, 0.9)
            s.ellipse(b[0], b[1], 3.0, 1.3, "#ffffff", 0.6)
        zn, zfar = z0 + 22, z1 - 22
        place(x0 + 34, zfar, False, 21, 1)
        place(xm + 2, zfar, False, 22, 1)
        place(x1 - 30, zfar, False, 23, 1)
        # ---- in the middle: the roast chicken on its dish (carved on one side), potatoes, gravy, a jug, bread
        up = (xm, yt, mid)
        disc(s, xm + 2.5, yt, mid - 2, 28, 16.5, "#57546e", 0.42)
        disc(s, xm, yt + 0.6, mid, 27, 15.5, lit("#aab4c0", up))
        disc(s, xm, yt + 0.8, mid, 23.5, 13, lit("#dfe6ea", up))
        seg(s, ring(xm, yt + 0.8, mid, 27, 15.5, 20, 200, 340), "#ffffff", 0.8, 0.9)
        disc(s, xm - 2, yt + 4, mid, 15, 10, lit("#7a4420", up))
        disc(s, xm - 2.5, yt + 6, mid + 0.5, 13.5, 8.6, lit("#a8642e", up))
        disc(s, xm - 4, yt + 9.5, mid + 1, 9.5, 6, lit("#c98440", up))
        disc(s, xm - 6, yt + 12, mid + 1.5, 4.5, 2.8, lit("#f0bc6c", up))
        for sgn in (-1, 1):                                                                                 # its legs, tied
            seg(s, [(xm + 7, yt + 6, mid + sgn * 4), (xm + 15, yt + 9.5, mid + sgn * 2.2)], lit("#b87838", up), 3.0)
            seg(s, [(xm + 15, yt + 9.5, mid + sgn * 2.2), (xm + 17.5, yt + 11, mid + sgn * 1.6)], lit("#f6eedc", up), 1.4)
        for q in range(3):                                                                                  # a sprig of parsley, roast potatoes round it
            disc(s, xm - 15 + q * 2, yt + 2, mid - 9 + q * 0.6, 1.8, 1.3, lit("#5a9a3c", up))
        for (dx, dz) in ((-17, 4), (-14, 8), (8, 9), (14, -9)):
            disc(s, xm + dx, yt + 2.2, mid + dz, 3.0, 2.3, lit("#e8b858", up))
        quad(s, [(xm + 5, yt + 1.5, mid - 8), (xm + 17, yt + 1.5, mid - 7), (xm + 16, yt + 1.5, mid - 1.5), (xm + 6, yt + 1.5, mid - 2.5)], lit("#f0d8b8", up))    # slices laid by
        seg(s, [(xm + 11, yt + 1.6, mid - 7.5), (xm + 10.5, yt + 1.6, mid - 2)], lit("#c8a880", up), 0.7, 0.8)
        seg(s, [(xm + 28, yt + 1.2, mid - 14), (xm + 45, yt + 1.2, mid - 10)], lit("#9aa4b0", up), 1.2)     # the carving knife
        seg(s, [(xm + 45, yt + 1.2, mid - 10), (xm + 53, yt + 1.2, mid - 8.5)], lit("#3a2a20", up), 1.8)
        bx = xm - 54                                                                                        # a bowl of potatoes
        disc(s, bx + 2, yt, mid + 4, 14.5, 10, "#57546e", 0.42)
        quad(s, [(bx - 12, yt + 8, mid + 6), (bx + 12, yt + 8, mid + 6), (bx + 8, yt, mid + 6), (bx - 8, yt, mid + 6)], lit("#4a78a8", (bx, yt + 4, mid), (0, 0.3, -1)))
        disc(s, bx, yt + 8, mid + 6, 12, 7.6, lit("#6c98c4", up))
        for k, (dx, dz) in enumerate(((-4.5, 0), (2, 1.6), (-1, -2.8), (5.5, -1.6), (-6.5, 2.8), (1, 3.6))):
            disc(s, bx + dx, yt + 9.6, mid + 6 + dz, 3.5, 2.7, lit("#f2d680", up))
            disc(s, bx + dx - 0.8, yt + 10.2, mid + 6.4 + dz, 1.5, 1.1, lit("#fbeeb0", up))
        jx, jz = xm + 50, mid + 14                                                                          # the water jug
        a, b = P(jx, yt, jz), P(jx, yt + 26, jz)
        s.ellipse(a[0] + 2.5, a[1] + 1, 7.5, 3.0, "#57546e", 0.42)
        s.poly([(a[0] - 6, a[1]), (a[0] + 6, a[1]), (b[0] + 4.6, b[1]), (b[0] - 4.6, b[1])], lit("#9cc4de", (jx, yt + 12, jz), (0, 0.2, -1)), 0.85)
        m = P(jx, yt + 16, jz)
        s.poly([(a[0] - 6, a[1]), (a[0] + 6, a[1]), (m[0] + 5.2, m[1]), (m[0] - 5.2, m[1])], lit("#5a90c0", (jx, yt + 8, jz), (0, 0.2, -1)), 0.9)
        s.line([(a[0] - 5.4, a[1] - 1), (b[0] - 4.2, b[1] + 1)], "#ffffff", 1.0, 0.9)
        s.line([(b[0] + 4.6, b[1] + 2), (b[0] + 9.5, b[1] + 5), (b[0] + 9, b[1] + 13), (a[0] + 5.6, a[1] - 6)], lit("#9cc4de", (jx, yt + 12, jz)), 1.3, 0.9)
        s.ellipse(b[0], b[1], 4.6, 1.7, "#ffffff", 0.6)
        gx, gz = xm - 30, mid - 17                                                                          # the gravy boat
        disc(s, gx + 1.5, yt, gz - 1, 10, 5.4, "#57546e", 0.4)
        disc(s, gx, yt + 0.5, gz, 9.5, 5.0, lit("#fbf8ee", up))
        disc(s, gx + 0.5, yt + 3.5, gz, 7.8, 4.0, lit("#7a4a26", up))
        seg(s, [(gx - 9, yt + 3, gz), (gx - 13.5, yt + 6, gz)], lit("#fbf8ee", up), 1.8)
        for k, (dx, c) in enumerate(((66, "#fbf8ee"), (72, "#3a3438"))):                                    # salt and pepper
            a, b = P(x0 + dx + 4, yt, mid - 6 + k * 4), P(x0 + dx + 4, yt + 8, mid - 6 + k * 4)
            s.line([a, b], lit(c, (x0 + dx, yt + 4, mid)), 2.6)
            s.ellipse(b[0], b[1], 1.5, 0.9, lit("#9aa4b0", up))
        bx, bz = x1 - 66, mid + 4                                                                           # the bread basket
        disc(s, bx + 2, yt, bz - 1, 14.5, 9.5, "#57546e", 0.4)
        quad(s, [(bx - 13, yt + 6, bz), (bx + 13, yt + 6, bz), (bx + 10, yt, bz), (bx - 10, yt, bz)], lit("#9a6a30", (bx, yt + 3, bz), (0, 0.3, -1)))
        disc(s, bx, yt + 6, bz, 13, 8.2, lit("#c08a44", up))
        disc(s, bx, yt + 6.5, bz, 10.5, 6.2, lit("#f2eee4", up))
        for (dx, dz) in ((-3.5, 0.5), (4, -0.5), (0, 2.6)):
            disc(s, bx + dx, yt + 8.6, bz + dz, 4.8, 3.2, lit("#c8904a", up))
            disc(s, bx + dx - 0.8, yt + 9.2, bz + dz + 0.4, 2.6, 1.6, lit("#e8bc78", up))
        place(x0 + 52, zn, True, 24, -1)
        place(x1 - 52, zn, True, 25, -1)
        return [s]

    def lay_near(L):
        for (cx, cz, a, sd) in near:
            chair_lay(L, cx, cz, a, toward=1, seed=sd)

    def fine_near():
        s = Sheet(SHAPE)
        for (cx, cz, a, sd) in near:
            chair_fine(s, cx, cz, a, toward=1)
        return [s]
    run(L, fine, "table", [(lay_far, fine_far), (lay_table, fine_table), (lay_near, fine_near), (None, lamp_over_table)])


def lamp_over_table():
    """The pendant: a wide shade of milky glass on a chain, hanging from the ceiling rose."""
    x, y, z = PENDANT
    s = Sheet(SHAPE)
    shade(s, (x, y, z), y - 15, y + 12, 33, 9, "#ffeab0", "#e8a850", ribs=11)
    cap = P(x, y + 12, z)
    s.poly([(cap[0] - 6.5, cap[1] + 1), (cap[0] + 6.5, cap[1] + 1), (cap[0] + 3, cap[1] - 6.5), (cap[0] - 3, cap[1] - 6.5)], "#a8802e")
    s.line([(cap[0] - 6.5, cap[1] + 1), (cap[0] + 6.5, cap[1] + 1)], "#f0d078", 0.9)
    s.line([(cap[0] - 3, cap[1] - 6.5), (cap[0] - 6.5, cap[1] + 1)], "#f0d078", 0.7, 0.8)
    return [s]


# ---------------------------------------------------------------- the desk, the family computer, its chair
def desk(L, fine=False):
    d = DESK
    x0, x1, z0, top = d["x0"], d["x1"], d["z0"], d["top"]
    oak = grainy("#b47c46", SEED + 30, "x", 0.10, (60, 5))
    oak_v = grainy("#a06c3a", SEED + 31, "y", 0.10, (60, 5))
    mz = MON["z"]
    mx = (MON["x0"] + MON["x1"]) / 2
    ch = Turned(-58.0, z0 - 52.0, 26.0)                                 # the chair: pushed back and turned, as someone left it
    ckw = dict(ang=ch.ang, about=(ch.cx, ch.cz))
    blue, blue_l = "#4f6f98", "#6485ae"
    tz = z0 + 13.8
    tx0, tx1 = x1 - 36, x1 - 14

    def lay_desk(L):
        Fc(L, [(x0 + 2, 0, ZW - 6), (x1 - 2, 0, ZW - 6), (x1 - 2, top - 4, ZW - 6), (x0 + 2, top - 4, ZW - 6)], "#3a2418", n=(0, 0, -1), dim=0.45)   # the dark under it
        B(L, tx0, tx1, 0, 44, z0 + 14, ZW - 10, "#cfc8b4", top="#ded8c6", cast=False)               # the computer itself: a beige tower, on the floor
        B(L, x0 + 2, x0 + 52, 0, top - 4, z0 + 2, ZW, oak_v)                                        # the drawers
        B(L, x1 - 6, x1 - 2, 0, top - 4, z0 + 2, ZW, oak_v, cast=False)
        B(L, x0, x1, top - 4, top, z0, ZW, oak_v, top=oak)
        # the monitor: foot, neck, and the flat black case
        B(L, mx - 17, mx + 17, top, top + 1.6, mz - 6, mz + 14, "#34343e", cast=False)
        B(L, mx - 4, mx + 4, top + 1.6, MON["y0"] + 6, mz + 3, mz + 7, "#2a2a32", cast=False)
        B(L, MON["x0"], MON["x1"], MON["y0"], MON["y1"], mz, mz + 6, "#2c2c36", top="#4a4a56", cast=False)
        Fc(L, [(SCR["x0"], SCR["y0"], mz - 0.2), (SCR["x1"], SCR["y0"], mz - 0.2), (SCR["x1"], SCR["y1"], mz - 0.2), (SCR["x0"], SCR["y1"], mz - 0.2)], "#10161f", n=(0, 0, -1), lit=False)
        B(L, mx - 24, mx + 22, top, top + 2.2, z0 + 7, z0 + 23, "#d6cfbb", top="#e2dccb", cast=False)   # keyboard

    def fine_desk():
        s = Sheet(SHAPE)
        zf = z0 + 1.8
        # ---- drawers: three, each with its shadow line and a brass pull
        for (ya, yb) in ((6, 26), (28, 48), (50, 70)):
            quad(s, [(x0 + 6, ya, zf), (x0 + 48, ya, zf), (x0 + 48, yb, zf), (x0 + 6, yb, zf)], lit("#b88048", (x0 + 27, (ya + yb) / 2, z0), (0, 0, -1)), 0.75)
            seg(s, [(x0 + 6, ya, zf), (x0 + 48, ya, zf), (x0 + 48, yb, zf)], DARK, 0.9, 0.5)
            seg(s, [(x0 + 6, ya, zf), (x0 + 6, yb, zf), (x0 + 48, yb, zf)], lit("#e8b878", (x0 + 27, yb, z0)), 0.8, 0.6)
            seg(s, [(x0 + 22, (ya + yb) / 2 + 1, zf - 1), (x0 + 32, (ya + yb) / 2 + 1, zf - 1)], lit("#e8c060", (x0 + 27, (ya + yb) / 2, z0), (0, 0.5, -1)), 1.6)
        seg(s, [(x0, top, z0), (x1, top, z0)], lit("#f0c890", (mx, top, z0)), 1.0, 0.85)                  # the front edge of the top
        seg(s, [(x0, top - 4.2, z0), (x1, top - 4.2, z0)], DARK, 1.1, 0.55)
        seg(s, [(x1, top, z0), (x1, top, ZW)], lit("#f0c890", (x1, top, z0 + 30)), 0.9, 0.6)
        # ---- the tower: drive doors, a button, a green lamp
        for yy in (36, 30):
            quad(s, [(tx0 + 3, yy, tz), (tx1 - 3, yy, tz), (tx1 - 3, yy + 4.5, tz), (tx0 + 3, yy + 4.5, tz)], lit("#b8b09a", (tx0, yy, tz), (0, 0, -1)))
            seg(s, [(tx0 + 3, yy, tz), (tx1 - 3, yy, tz)], DARK, 0.7, 0.5)
        seg(s, [(tx0 + 5, 24, tz), (tx0 + 12, 24, tz)], DARK, 1.0, 0.6)
        b = P(tx1 - 6, 14, tz)
        s.ellipse(b[0], b[1], 1.6, 1.6, lit("#a8a08a", (tx0, 14, tz), (0, 0, -1)))
        b = P(tx0 + 6, 14, tz)
        s.ellipse(b[0], b[1], 1.0, 1.0, "#7cf08a")
        for yy in (4, 8):
            seg(s, [(tx0 + 4, yy, tz), (tx1 - 4, yy, tz)], DARK, 0.7, 0.4)
        # ---- the monitor: its dark glass, the bezel's lit edges, a small blue lamp
        quad(s, [(SCR["x0"], SCR["y0"], mz - 0.3), (SCR["x1"], SCR["y0"], mz - 0.3), (SCR["x1"], SCR["y1"], mz - 0.3), (SCR["x0"], SCR["y1"], mz - 0.3)], "#10161f")
        quad(s, [(SCR["x0"], SCR["y1"], mz - 0.3), (SCR["x0"] + 26, SCR["y1"], mz - 0.3), (SCR["x0"] + 8, SCR["y0"], mz - 0.3), (SCR["x0"], SCR["y0"], mz - 0.3)], "#27344a", 0.55)   # the room in the dark glass
        seg(s, [(MON["x0"], MON["y1"], mz), (MON["x1"], MON["y1"], mz)], lit("#8a8a98", (mx, MON["y1"], mz)), 0.9, 0.9)
        seg(s, [(MON["x0"], MON["y0"], mz), (MON["x0"], MON["y1"], mz)], lit("#6a6a78", (mx, 110, mz), (-1, 0, 0)), 0.8, 0.7)
        b = P(MON["x1"] - 5, MON["y0"] + 2, mz - 0.3)
        s.ellipse(b[0], b[1], 0.9, 0.9, "#8fd0ff")
        # ---- the keyboard's rows, the mouse on its mat, Dad's mug, papers, a jar of pens
        ky = top + 2.3
        for k in range(4):
            zz = z0 + 9.5 + k * 3.6
            seg(s, [(mx - 22, ky, zz), (mx + 20, ky, zz)], "#6a6458", 0.8, 0.55)
        seg(s, [(mx - 24, ky, z0 + 7), (mx + 22, ky, z0 + 7)], lit("#fff8e8", (mx, ky, z0)), 0.8, 0.7)
        quad(s, [(mx + 28, top + 0.3, z0 + 6), (mx + 50, top + 0.3, z0 + 6), (mx + 50, top + 0.3, z0 + 26), (mx + 28, top + 0.3, z0 + 26)], lit("#3a5a8a", (mx + 40, top, z0 + 16)))
        disc(s, mx + 38, top + 1.5, z0 + 15, 3.4, 5.0, lit("#e2dccb", (mx + 38, top + 2, z0 + 15)))
        seg(s, [(mx + 38, top + 1.5, z0 + 20), (mx + 34, top + 0.5, z0 + 36), (mx + 20, top + 0.5, z0 + 44)], "#3a3438", 0.7, 0.8)
        mgx, mgz = x1 - 14, z0 + 20                                                                        # the mug: red, his
        a, b = P(mgx, top, mgz), P(mgx, top + 10, mgz)
        s.poly([(a[0] - 3.2, a[1]), (a[0] + 3.2, a[1]), (b[0] + 3.4, b[1]), (b[0] - 3.4, b[1])], lit("#c8402f", (mgx, top + 5, mgz), (-0.3, 0.2, -0.9)))
        s.ellipse(b[0], b[1], 3.4, 1.5, lit("#e87a66", (mgx, top + 10, mgz)))
        s.ellipse(b[0], b[1], 2.4, 1.0, lit("#3a2018", (mgx, top + 10, mgz)))
        s.line([(a[0] + 3.2, a[1] - 2), (a[0] + 6.0, a[1] - 3.5), (b[0] + 3.4, b[1] + 2)], lit("#c8402f", (mgx, top + 5, mgz)), 1.2)
        for k, (dx, dz, a_) in enumerate(((10, 30, 0.2), (16, 26, -0.25), (6, 12, 0.5))):                   # papers on the left
            ca, sa = math.cos(a_), math.sin(a_)
            cx_, cz_ = x0 + dx + 10, z0 + dz + 6
            pts = [(cx_ + ux * ca - uz * sa, top + 0.3 + k * 0.3, cz_ + ux * sa + uz * ca) for ux, uz in ((-10, -13), (10, -13), (10, 13), (-10, 13))]
            quad(s, pts, lit(("#f4f0e2", "#e8e2d0", "#f0e4a8")[k], (cx_, top, cz_)))
            seg(s, [pts[0], pts[1]], DARK, 0.6, 0.25)
        jx, jz = x0 + 22, z0 + 54                                                                          # the pen jar
        a, b = P(jx, top, jz), P(jx, top + 11, jz)
        s.poly([(a[0] - 3, a[1]), (a[0] + 3, a[1]), (b[0] + 3, b[1]), (b[0] - 3, b[1])], lit("#4a7a6a", (jx, top + 5, jz), (0, 0.2, -1)))
        for k, c in enumerate(("#e8c84a", "#d85a4a", "#4a7ab8")):
            s.line([(b[0] - 1.5 + k * 1.5, b[1]), (b[0] - 3 + k * 3, b[1] - 6)], lit(c, (jx, top + 14, jz)), 0.9)
        return [s]

    seat_o = rrect(0, 0, 46, 44, 10)
    back_o = [(-19, 60), (19, 60), (22, 70), (21, 92), (14, 99), (-14, 99), (-21, 92), (-22, 70)]

    def lay_chair(L):
        # a blue office chair on five castors, turned half away from us
        for k in range(5):
            a_ = math.radians(72 * k + 20)
            ex, ez = ch.cx + math.cos(a_) * 27, ch.cz + math.sin(a_) * 27
            Fc(L, [(ch.cx - 2 * math.sin(a_), 9, ch.cz + 2 * math.cos(a_)), (ch.cx + 2 * math.sin(a_), 9, ch.cz - 2 * math.cos(a_)), (ex + 1.6 * math.sin(a_), 5, ez - 1.6 * math.cos(a_)), (ex - 1.6 * math.sin(a_), 5, ez + 1.6 * math.cos(a_))], "#3c3c48", n=(0, 1, 0))
        B(L, ch.cx - 3, ch.cx + 3, 8, 41, ch.cz - 3, ch.cz + 3, "#2a2a32", cast=False)
        prism_y(L, ch, seat_o, 41, 49, blue, blue_l)
        for sx in (-1, 1):                                                # the arms: a post and a pad
            ch_b = ch.p(sx * 25.5, 0, 2)
            B(L, ch_b[0] - 1.5, ch_b[0] + 1.5, 47, 66, ch_b[2] - 2, ch_b[2] + 2, "#2a2a32", cast=False)
            prism_y(L, ch, [(sx * 25.5 - 3.5, -13), (sx * 25.5 + 3.5, -13), (sx * 25.5 + 3.5, 13), (sx * 25.5 - 3.5, 13)], 66, 69, "#34343e", "#4a4a58", cast=False)
        prism_z(L, ch, [(-3, 44), (3, 44), (3, 64), (-3, 64)], -27, -23, "#2a2a32")                        # the bar that carries the back
        prism_z(L, ch, back_o, -31, -24, blue, blue_l)

    def fine_chair():
        s = Sheet(SHAPE)
        for k in range(5):
            a_ = math.radians(72 * k + 20)
            ex, ez = ch.cx + math.cos(a_) * 28, ch.cz + math.sin(a_) * 28
            c = P(ex, 2.5, ez)
            s.ellipse(c[0], c[1], 2.4, 2.4, "#16161c")
            s.ellipse(c[0] - 0.6, c[1] - 0.6, 0.8, 0.8, "#6a6a78")
        hi = lambda pos, n=(0, 1, 0): lit("#a8c0dc", pos, n)
        top_edge = [ch.p(x, y, -31) for x, y in back_o[2:7]]
        seg(s, top_edge, hi(ch.p(0, 99, -31)), 1.0, 0.75)                                                   # the light along the top of the back
        seg(s, [ch.p(x, y, -31.2) for x, y in (back_o[6:] + back_o[:3])], DARK, 0.9, 0.45)
        seg(s, [ch.p(x * 0.72, 79 + (y - 79) * 0.72, -31.3) for x, y in back_o] + [ch.p(back_o[0][0] * 0.72, 79 + (back_o[0][1] - 79) * 0.72, -31.3)], DARK, 0.7, 0.25)   # a seam round its pad
        seg(s, [ch.p(x, 49.2, z) for x, z in seat_o[:6]], hi(ch.p(0, 49, 0)), 0.8, 0.5)
        seg(s, [ch.p(x, 41, z) for x, z in seat_o[:11]], DARK, 1.0, 0.4)
        return [s]
    run(L, fine, "desk", [(lay_desk, fine_desk), (lay_chair, fine_chair)])


# ---------------------------------------------------------------- the piano
def piano(L, fine=False):
    p = PIANO
    x0, x1, z0, top, kz = p["x0"], p["x1"], p["z0"], p["top"], p["keys"]
    xm = (x0 + x1) / 2
    eb = grainy("#4e3028", SEED + 40, "x", 0.10, (70, 6))
    eb_top = grainy("#5c3a30", SEED + 41, "x", 0.10, (70, 6))
    sx0, sx1, sz0, sz1 = xm - 36, xm + 34, z0 - 92, z0 - 58                                             # the stool
    zf = z0 - 0.3
    hi = lambda pos, n=(0, 1, 0), a=1.0: lit("#c08a68", pos, n, a)

    def lay_piano(L):
        B(L, x0, x1, 0, top, z0, ZW, eb, top=eb_top)
        Fc(L, [(x0 + 11, 9, z0 - 0.2), (x1 - 11, 9, z0 - 0.2), (x1 - 11, 58, z0 - 0.2), (x0 + 11, 58, z0 - 0.2)], "#3a231e", n=(0, 0, -1))
        for dx in (-9, 0, 9):                                                                           # the pedals
            Fc(L, [(xm + dx - 1.6, 3.5, z0 - 1), (xm + dx + 1.6, 3.5, z0 - 1), (xm + dx + 1.6, 2.5, z0 - 10), (xm + dx - 1.6, 2.5, z0 - 10)], "#e8c060", n=(0, 1, 0))
        for xa in (x0 + 1, x1 - 8):                                                                     # the legs under the key bed
            B(L, xa, xa + 7, 0, 62, kz + 2, kz + 9, eb, cast=False)
        B(L, x0, x1, 62, 71, kz, z0, eb, top=eb_top)                                                    # the key bed
        for xa in (x0, x1 - 9):                                                                         # its cheeks
            B(L, xa, xa + 9, 71, 80, kz, z0, eb, top=eb_top, cast=False)
        Fc(L, [(x0 + 9.5, 71.3, kz + 2), (x1 - 9.5, 71.3, kz + 2), (x1 - 9.5, 71.3, z0 - 3), (x0 + 9.5, 71.3, z0 - 3)], "#f2ecda", n=(0, 1, 0))
        B(L, xm - 31, xm + 31, 86, 88.5, z0 - 6, z0, eb_top, cast=False)                                # the music desk

    def fine_piano():
        s = Sheet(SHAPE)
        # ---- the case: lid edge, the upper panel with its moulding, the lower panel, polish
        seg(s, [(x0, top, z0), (x1, top, z0)], hi((xm, top, z0)), 1.1, 0.9)
        seg(s, [(x0, top - 3.5, zf), (x1, top - 3.5, zf)], DARK, 1.0, 0.6)
        seg(s, [(x0, top, z0), (x0, top, ZW)], hi((x0, top, z0 + 30)), 0.9, 0.7)
        for (xa, xb, ya, yb) in ((x0 + 10, x1 - 10, 92, 118), (x0 + 12, x1 - 12, 11, 56)):
            seg(s, [(xa, ya, zf), (xa, yb, zf), (xb, yb, zf)], DARK, 0.9, 0.55)
            seg(s, [(xa, ya, zf), (xb, ya, zf), (xb, yb, zf)], hi((xm, ya, z0), (0, 0.4, -0.9)), 0.8, 0.5)
        for k in range(3):                                                                              # the lamp's light sliding on the varnish
            xa = xm + 34 + k * 9
            quad(s, [(xa, 93, zf), (xa + 4, 93, zf), (xa - 3, 117, zf), (xa - 7, 117, zf)], "#ffd8a0", 0.12)
        # ---- the fall board, and the keys: white ones, the black ones in twos and threes
        quad(s, [(x0 + 9, 71.5, z0 - 2.8), (x1 - 9, 71.5, z0 - 2.8), (x1 - 9, 82, z0 - 0.5), (x0 + 9, 82, z0 - 0.5)], lit("#4e3028", (xm, 77, z0), (0, 0.5, -0.8)))
        seg(s, [(x0 + 9, 82, z0 - 0.5), (x1 - 9, 82, z0 - 0.5)], hi((xm, 82, z0)), 0.8, 0.7)
        ka, kb = x0 + 9.5, x1 - 9.5
        ky = 71.5
        nw = 40
        for i in range(1, nw):
            xx = lerp(ka, kb, i / nw)
            seg(s, [(xx, ky, kz + 2), (xx, ky, z0 - 3)], "#7a7468", 0.6, 0.6)
        for i in range(nw - 1):
            if i % 7 in (2, 6):
                continue
            xx = lerp(ka, kb, (i + 1) / nw)
            quad(s, [(xx - 1.0, ky + 0.6, kz + 11), (xx + 1.0, ky + 0.6, kz + 11), (xx + 1.0, ky + 0.6, z0 - 3), (xx - 1.0, ky + 0.6, z0 - 3)], "#17120f")
        seg(s, [(ka, ky, kz + 2), (kb, ky, kz + 2)], "#fffdf0", 0.9, 0.9)
        quad(s, [(ka, 68, kz - 0.2), (kb, 68, kz - 0.2), (kb, 71.2, kz - 0.2), (ka, 71.2, kz - 0.2)], lit("#e2dcc8", (xm, 70, kz), (0, 0, -1)))
        seg(s, [(x0, 62, kz - 0.2), (x1, 62, kz - 0.2)], DARK, 1.0, 0.5)
        # ---- music on the desk: two open pages, staves and notes too small to read
        for (xa, xb, lean) in ((xm - 25, xm - 1, -1.5), (xm + 1, xm + 25, 1.5)):
            pg = [(xa, 88.5, z0 - 4.5), (xb, 88.5, z0 - 4.5), (xb + lean * 0.3, 119, z0 - 1), (xa + lean * 0.3, 119, z0 - 1)]
            quad(s, pg, lit("#f6f2e4", ((xa + xb) / 2, 104, z0 - 3), (0, 0.3, -0.95)))
            for r in range(5):
                yy = 93 + r * 5.2
                seg(s, [(xa + 2.5, yy, z0 - 4), (xb - 2.5, yy, z0 - 4)], "#4a4650", 0.6, 0.55)
                for q in range(4):
                    c = P(xa + 4 + q * 5.2 + (r % 2), yy + 1.0 + ((q * 7 + r * 3) % 3) - 1, z0 - 4)
                    s.ellipse(c[0], c[1], 0.8, 0.7, "#2a2630", 0.8)
        # ---- on the lid: the metronome, a pile of music, a photograph in a silver frame, the lamp
        ly = top
        mxx, mzz = x0 + 22, z0 + 26
        quad(s, [(mxx - 6, ly, mzz), (mxx + 6, ly, mzz), (mxx + 2.2, ly + 22, mzz), (mxx - 2.2, ly + 22, mzz)], lit("#9a6436", (mxx, ly + 10, mzz), (0, 0.2, -1)))
        seg(s, [(mxx, ly + 3, mzz - 0.5), (mxx + 2.6, ly + 20, mzz - 0.5)], lit("#e8c060", (mxx, ly + 12, mzz)), 0.9)
        quad(s, [(mxx - 4.6, ly + 1.5, mzz - 0.3), (mxx + 4.6, ly + 1.5, mzz - 0.3), (mxx + 3.4, ly + 8, mzz - 0.3), (mxx - 3.4, ly + 8, mzz - 0.3)], lit("#3a2418", (mxx, ly + 5, mzz), (0, 0, -1)), 0.8)
        bx_, bz_ = x0 + 52, z0 + 30
        for k, c in enumerate(("#e8dcc0", "#b5483a", "#e2d8c0", "#3f6f8f")):
            quad(s, [(bx_ - 14 + k, ly + k * 2.2, bz_ - 14), (bx_ + 14 + k * 0.5, ly + k * 2.2, bz_ - 14), (bx_ + 14 + k * 0.5, ly + k * 2.2 + 2.2, bz_ - 14), (bx_ - 14 + k, ly + k * 2.2 + 2.2, bz_ - 14)], lit(c, (bx_, ly + 4, bz_), (0, 0, -1)))
        quad(s, [(bx_ - 11, ly + 9, bz_ - 14), (bx_ + 15, ly + 9, bz_ - 14), (bx_ + 15, ly + 9, bz_ + 14), (bx_ - 11, ly + 9, bz_ + 14)], lit("#5a86a8", (bx_, ly + 9, bz_)))
        fx_, fz_ = xm + 12, z0 + 34
        quad(s, [(fx_ - 8, ly, fz_), (fx_ + 8, ly, fz_), (fx_ + 8, ly + 20, fz_ + 3), (fx_ - 8, ly + 20, fz_ + 3)], lit("#cfd6dc", (fx_, ly + 10, fz_), (0, 0.2, -1)))
        quad(s, [(fx_ - 5.6, ly + 2.6, fz_ - 0.2), (fx_ + 5.6, ly + 2.6, fz_ - 0.2), (fx_ + 5.6, ly + 17.4, fz_ + 2.6), (fx_ - 5.6, ly + 17.4, fz_ + 2.6)], lit("#8fa8b8", (fx_, ly + 10, fz_), (0, 0.2, -1)))
        c = P(fx_, ly + 9, fz_)
        s.ellipse(c[0], c[1] - 1.5, 1.6, 1.6, lit("#e8c0a0", (fx_, ly + 10, fz_), (0, 0.2, -1)))
        s.ellipse(c[0], c[1] + 2.4, 2.6, 2.4, lit("#f0f0f0", (fx_, ly + 10, fz_), (0, 0.2, -1)))
        lx_, ly_, lz_ = PIANOLAMP
        disc(s, lx_, top + 0.4, lz_, 8, 6, lit("#c9a050", (lx_, top, lz_ - 8)))
        s.line([P(lx_, top, lz_), P(lx_, ly_ - 12, lz_)], lit("#c9a050", (lx_ - 6, top + 14, lz_ - 6), (-0.6, 0, -0.8)), 1.8)
        s.line([P(lx_ - 0.6, top, lz_), P(lx_ - 0.6, ly_ - 12, lz_)], "#fff0b0", 0.7, 0.8)
        shade(s, (lx_, ly_, lz_), ly_ - 13, ly_ + 9, 15, 7.5, "#ffe6a8", "#e09a48", top_c="#fff8dc", ribs=7)
        return [s]

    def lay_stool(L):
        for (lx, lz) in ((sx0 + 3, sz1 - 3), (sx1 - 3, sz1 - 3), (sx0 + 3, sz0 + 3), (sx1 - 3, sz0 + 3)):
            B(L, lx - 2.5, lx + 2.5, 0, 44, lz - 2.5, lz + 2.5, eb, cast=False)
        B(L, sx0, sx1, 44, 49, sz0, sz1, eb, top=eb_top)
        B(L, sx0 + 1.5, sx1 - 1.5, 49, 54, sz0 + 1.5, sz1 - 1.5, "#a83c3c", top="#c04a48", cast=False)

    def fine_stool():
        s = Sheet(SHAPE)
        xa, xb, za, zb, yy = sx0 + 1.5, sx1 - 1.5, sz0 + 1.5, sz1 - 1.5, 54.2
        seg(s, [(xa, yy, za), (xb, yy, za), (xb, yy, zb), (xa, yy, zb), (xa, yy, za)], lit("#e88a80", (xm, yy, za)), 0.8, 0.6)
        for i in range(3):
            c = P(lerp(xa, xb, (i + 0.5) / 3), yy, (za + zb) / 2)
            s.ellipse(c[0], c[1], 1.0, 0.8, lit("#7a2428", (xm, yy, za)))
        seg(s, [(sx0, 49, sz0), (sx1, 49, sz0)], hi((xm, 49, sz0)), 0.9, 0.7)
        seg(s, [(sx0, 44, sz0 - 0.2), (sx1, 44, sz0 - 0.2)], DARK, 0.9, 0.5)
        for lx in (sx0 + 3, sx1 - 3):
            seg(s, [(lx - 2.5, 0, sz0 + 0.5), (lx - 2.5, 44, sz0 + 0.5)], hi((lx, 22, sz0), (-1, 0, 0)), 0.8, 0.5)
        return [s]
    run(L, fine, "piano", [(lay_piano, fine_piano), (lay_stool, fine_stool)])


# ---------------------------------------------------------------- Dad's armchair and his reading lamp
def armchair(L, fine=False):
    a = ARM
    t = Turned(a["cx"], a["cz"], a["ang"])
    cord = "#93a274"

    def ribbed(axis, base=cord, seed=0, amount=0.10):                    # corduroy: fine ribs of light and dark
        b = col(base)

        def f(X, Y, Z):
            lx, lz = t.local(X, Z)
            u = {"x": lx, "y": Y, "z": lz}[axis]
            rib = 0.5 + 0.5 * np.sin(u * 2 * np.pi / 3.4)
            n = wnoise(lx + Y, lz + Y * 0.5, 26, SEED + 50 + seed) - 0.5
            return b[None, None, :] * (1 - amount * 0.5 + amount * rib + 0.16 * n)[..., None]
        return f
    BACK = [(-38, 30), (38, 30), (38, 88), (32, 100), (12, 106), (-12, 106), (-32, 100), (-38, 88)]      # the back, from the front
    CUSH = [(-27, 44), (27, 44), (27, 86), (22, 96), (-22, 96), (-27, 86)]                               # its cushion
    ARMP = [(27, 7), (47, 7), (47, 54), (44, 60), (37, 63), (30, 60), (27, 54)]                          # an arm, from the front (the right one)
    tx, tz = t.p(72, 0, -8)[0], t.p(72, 0, -8)[2]                                                        # the little table at his right hand

    def strips(L, outline, za, zb, albedo, from_y):
        """The top of something whose front has `outline`: bands from the front edge (za) back to zb."""
        n = len(outline)
        for i in range(n):
            (xa, ya), (xb, yb) = outline[i], outline[(i + 1) % n]
            if min(ya, yb) < from_y or (xa == xb):
                continue
            nx, ny = (yb - ya), -(xb - xa)
            if ny < 0:
                nx, ny = -nx, -ny
            t.face(L, [(xa, ya, za), (xb, yb, za), (xb, yb, zb), (xa, ya, zb)], albedo, (nx, ny, 0))

    def arm(L, sgn, seed):
        prof = [(x * sgn, y) for x, y in ARMP]
        if sgn > 0:
            t.face(L, [(47, 7, -40), (47, 7, 36), (47, 54, 36), (47, 54, -40)], ribbed("z", seed=seed), (1, 0, 0))     # its outer flank
        else:
            t.face(L, [(-27, 44, -40), (-27, 44, 10), (-27, 54, 10), (-27, 54, -40)], ribbed("z", seed=seed), (1, 0, 0), dim=0.7)
        strips(L, prof, -40, 36, ribbed("x", "#a3b284", seed), 54)
        t.face(L, [(x, y, -40) for x, y in prof], ribbed("x", "#9aa97a", seed), (0, 0, -1))

    def lay_lamp_foot(L):
        fx, fy, fz = FLOORLAMP
        B(L, fx - 12, fx + 12, 0, 3, fz - 10, fz + 10, "#8a6a28")
        B(L, fx - 1.4, fx + 1.4, 3, fy - 14, fz - 1.4, fz + 1.4, "#a8802e", cast=False)

    def lay_body(L):
        for (lx, lz) in ((-40, 36), (40, 36), (-40, -34), (40, -34)):
            q = t.p(lx, 0, lz)
            B(L, q[0] - 3.5, q[0] + 3.5, 0, 7, q[2] - 3.5, q[2] + 3.5, "#5a3820", cast=False)
        # the back: its face, the roll of its top, the side we can see
        t.face(L, [(x, y, 20) for x, y in BACK], ribbed("x", seed=1), (0, 0, -1), dim=0.9)
        t.face(L, [(38, 30, 20), (38, 30, 44), (38, 88, 44), (38, 88, 20)], ribbed("z", seed=1), (1, 0, 0))
        strips(L, BACK, 20, 44, ribbed("x", "#a3b284", 1), 88)
        t.face(L, [(x, y, 8) for x, y in CUSH], ribbed("x", "#9dac7e", 2), (0, 0, -1))
        t.face(L, [(27, 44, 8), (27, 44, 20), (27, 86, 20), (27, 86, 8)], ribbed("z", "#9dac7e", 2), (1, 0, 0))
        strips(L, CUSH, 8, 20, ribbed("x", "#a9b88a", 2), 86)
        arm(L, -1, 3)                                                                                    # the far arm
        t.face(L, [(-27, 7, -42), (27, 7, -42), (27, 31, -42), (-27, 31, -42)], ribbed("x", seed=4), (0, 0, -1), dim=0.85)   # under the seat
        t.face(L, [(-27, 31, -44), (27, 31, -44), (27, 42, -44), (-27, 42, -44)], ribbed("x", "#9dac7e", 5), (0, 0, -1))  # the seat cushion
        t.face(L, [(-27, 42, -44), (27, 42, -44), (27, 46, -40), (-27, 46, -40)], ribbed("x", "#a9b88a", 5), (0, 0.7, -0.7))
        t.face(L, [(-27, 46, -40), (27, 46, -40), (27, 46, 8), (-27, 46, 8)], ribbed("x", "#a6b488", 5), (0, 1, 0),
               dim=lambda X, Y, Z: 0.62 + 0.38 * step(4.0, -22.0, t.local(X, Z)[1]))                    # darker where the back overhangs it
        for cs in (corners(a["cx"] - 40, a["cx"] + 40, 0, 46, a["cz"] - 40, a["cz"] + 40, a["ang"]), corners(a["cx"] - 36, a["cx"] + 36, 30, 104, a["cz"] + 20, a["cz"] + 44, a["ang"], (a["cx"], a["cz"]))):
            if isinstance(L, Collector):
                L.boxes.append(cs)

    def fine_body():
        s = Sheet(SHAPE)
        pale = lambda pos, n=(0, 1, 0): lit("#cbd6a8", pos, n)
        seam = lambda pts_, a_=0.5, wd=1.0: seg(s, [t.p(*q) for q in pts_], DARK, wd, a_)
        pipe = lambda pts_, a_=0.7, wd=0.9: seg(s, [t.p(*q) for q in pts_], pale(t.p(*pts_[0])), wd, a_)
        pipe([(x, y, 20) for x, y in BACK[2:]] + [(-38, 30, 20)], 0.75)                                  # piping round the back
        pipe([(x, y, 44) for x, y in BACK[2:]], 0.45)
        pipe([(x, y, 8) for x, y in CUSH[2:]] + [(-27, 44, 8)], 0.7)
        seam([(-27, 44.3, 8.2), (27, 44.3, 8.2)], 0.55, 1.2)                                             # where the cushions meet
        seam([(-27, 46.2, -40), (-27, 46.2, 8)], 0.45, 1.1)
        seam([(27, 46.2, -40), (27, 46.2, 8)], 0.4, 1.0)
        pipe([(-27, 46.2, -40), (27, 46.2, -40)], 0.7, 1.0)                                              # the seat cushion's front edge
        pipe([(-27, 42, -44.2), (27, 42, -44.2)], 0.35)
        seam([(-27, 31, -44.3), (27, 31, -44.3)], 0.5, 1.1)
        seam([(-27, 7.2, -42.2), (27, 7.2, -42.2)], 0.5, 1.2)
        pipe([(x * -1, y, -40) for x, y in ARMP[2:]], 0.6)                                               # the far arm's front
        pipe([(-37, 63.2, -40), (-37, 63.2, 20)], 0.4)
        # ---- it has kept his shape: the hollow in the seat, and the one his shoulders made in the back
        dent = [t.p(math.cos(q) * 15 - 3, 46.3, -16 + math.sin(q) * 12) for q in np.linspace(0, 6.28, 18)]
        s.poly(pts2(dent), "#2c3824", 0.26)
        dent2 = [t.p(math.cos(q) * 9.5 - 3, 46.4, -15 + math.sin(q) * 7.5) for q in np.linspace(0, 6.28, 14)]
        s.poly(pts2(dent2), "#2c3824", 0.20)
        seg(s, [t.p(-18, 46.4, -19), t.p(-14, 46.4, -6), t.p(-3, 46.4, -3), t.p(8, 46.4, -6)], pale(t.p(0, 46, -10)), 0.8, 0.42)
        hol = [t.p(math.cos(q) * 14, 70 + math.sin(q) * 14, 7.7) for q in np.linspace(0, 6.28, 16)]
        s.poly(pts2(hol), "#2c3824", 0.20)
        for k in range(2):                                                                               # two buttons in the back
            c = P(*t.p(-11 + k * 22, 82, 7.6))
            s.ellipse(c[0], c[1], 1.4, 1.4, lit("#56643e", t.p(0, 82, 8), (0, 0, -1)))
            s.ellipse(c[0] - 0.4, c[1] - 0.4, 0.5, 0.5, pale(t.p(0, 82, 8)))
        # ---- a knitted blanket over the far corner of the back, hanging down in front
        wool = lambda y, n=(0, 0.5, -0.8), c="#c8643c": lit(c, t.p(-20, y, 14), n)
        s.poly(pts2([t.p(-31, 101, 44), t.p(-9, 106.6, 44), t.p(-9, 106.6, 20), t.p(-31, 101, 20)]), wool(104, (0, 1, 0)))
        s.poly(pts2([t.p(-31, 101, 20), t.p(-9, 106.6, 20), t.p(-9, 97, 7.6), t.p(-28, 97, 7.6)]), wool(100, (0, 0.8, -0.6)))
        s.poly(pts2([t.p(-28, 97, 7.5), t.p(-9, 97, 7.5), t.p(-9.5, 66, 7.5), t.p(-18, 61, 7.5), t.p(-27, 64, 7.5)]), wool(80, (0, 0, -1)))
        for k in range(7):
            yy = 95 - k * 4.6
            seg(s, [t.p(-27.6, yy, 7.4), t.p(-9.3, yy, 7.4)], wool(yy, (0, 0, -1), ("#f0d8a0", "#7a3a2a", "#e8a850")[k % 3]), 1.3, 0.9)
        for k in range(6):
            xx = -26 + k * 3.2
            seg(s, [t.p(xx, 64 - abs(k - 2.5) * 0.8, 7.4), t.p(xx, 59 - abs(k - 2.5) * 0.8, 7.4)], wool(60, (0, 0, -1), "#f0d8a0"), 0.8)
        return [s]

    def lay_near_arm(L):
        arm(L, 1, 6)

    def fine_near_arm():
        s = Sheet(SHAPE)
        pale = lambda pos, n=(0, 1, 0): lit("#cbd6a8", pos, n)
        seg(s, [t.p(x, y, -40) for x, y in ARMP[2:]] + [t.p(27, 7, -40)], pale(t.p(37, 60, -40)), 0.9, 0.7)
        seg(s, [t.p(47, 54, -40), t.p(47, 54, 36)], pale(t.p(47, 54, 0)), 0.9, 0.55)
        seg(s, [t.p(27, 7.2, -40.2), t.p(47, 7.2, -40.2), t.p(47, 7.2, 36)], DARK, 1.2, 0.5)
        seg(s, [t.p(47.1, 7, -40), t.p(47.1, 54, -40)], DARK, 0.9, 0.35)
        c = P(*t.p(37, 50, -40.2))                                                                       # the worn roll at the front of the arm
        r = 8.0 * cam.scale(t.p(37, 50, -40)[2])
        s.ellipse(c[0], c[1], r, r, "#dce4bc", 0.20)
        s.ellipse(c[0], c[1], r * 0.2, r * 0.2, lit("#56643e", t.p(37, 50, -40), (0, 0, -1)))
        # ---- the crossword folded on the arm, his pencil across it
        ay = 63.5
        np_ = [t.p(29.5, ay - 1.2, -30), t.p(45, ay - 1.5, -31), t.p(45.5, ay - 1.5, -4), t.p(30, ay - 1.2, -3)]
        s.poly(pts2(np_), lit("#efe9d8", t.p(37, ay, -16)))
        s.poly(pts2([t.p(32, ay, -17), t.p(42, ay, -18), t.p(42.5, ay, -6), t.p(32.5, ay, -5.5)]), "#3a3640", 0.6)
        for k in range(1, 4):
            seg(s, [t.p(32 + k * 2.6, ay + 0.1, -17.2), t.p(32.4 + k * 2.6, ay + 0.1, -5.6)], "#efe9d8", 0.6, 0.8)
            seg(s, [t.p(32, ay + 0.1, -17 + k * 3), t.p(42.5, ay + 0.1, -17.5 + k * 3)], "#efe9d8", 0.6, 0.8)
        for k in range(3):
            seg(s, [t.p(32, ay, -28 + k * 3), t.p(43, ay, -29 + k * 3)], "#5a5660", 0.6, 0.6)
        seg(s, [t.p(31, ay + 0.6, -24), t.p(44, ay + 0.6, -10)], lit("#e8b83a", t.p(37, ay, -16)), 1.2)
        seg(s, np_ + [np_[0]], DARK, 0.6, 0.3)
        return [s]

    def lay_table(L):
        B(L, tx - 2.5, tx + 2.5, 0, 50, tz - 2.5, tz + 2.5, WALNUT, cast=False)
        Fc(L, ring(tx, 52, tz, 20, 18)[:-1], grainy("#a8703c", SEED + 58, "x"), n=(0, 1, 0))
        if isinstance(L, Collector):
            L.boxes.append(corners(tx - 17, tx + 17, 50, 52, tz - 15, tz + 15))

    def fine_table():
        s = Sheet(SHAPE)
        seg(s, ring(tx, 52.2, tz, 20, 18), lit("#e8b878", (tx, 52, tz - 18)), 0.9, 0.7)
        seg(s, ring(tx, 50, tz, 20, 18, 12, 180, 360), DARK, 1.2, 0.5)
        for k in range(3):
            a_ = math.radians(210 + k * 60)
            seg(s, [(tx, 14, tz), (tx + math.cos(a_) * 15, 0, tz + math.sin(a_) * 13)], lit(WALNUT, (tx, 6, tz)), 1.8)
        mgx, mgz = tx - 7, tz - 2                                                                        # his mug, and a book face-down
        a_, b_ = P(mgx, 52.3, mgz), P(mgx, 62, mgz)
        s.poly([(a_[0] - 3.2, a_[1]), (a_[0] + 3.2, a_[1]), (b_[0] + 3.5, b_[1]), (b_[0] - 3.5, b_[1])], lit("#e8e2d0", (mgx, 57, mgz), (-0.3, 0.2, -0.9)))
        s.ellipse(b_[0], b_[1], 3.5, 1.5, lit("#f6f2e6", (mgx, 62, mgz)))
        s.ellipse(b_[0], b_[1], 2.5, 1.0, lit("#4a2c1c", (mgx, 62, mgz)))
        bk = [(tx + 1, 52.6, tz - 9), (tx + 15, 52.6, tz - 6), (tx + 13, 52.6, tz + 9), (tx - 1, 52.6, tz + 6)]
        quad(s, bk, lit("#3f6f8f", (tx + 7, 53, tz)))
        seg(s, [((bk[0][0] + bk[1][0]) / 2, 53.6, (bk[0][2] + bk[1][2]) / 2), ((bk[2][0] + bk[3][0]) / 2, 53.6, (bk[2][2] + bk[3][2]) / 2)], lit("#8fb6d0", (tx + 7, 54, tz)), 1.0)
        gx, gz = tx - 4, tz - 11                                                                          # his reading glasses
        for sx in (-1, 1):
            c = P(gx + sx * 3.0, 52.8, gz)
            s.ellipse(c[0], c[1], 2.2, 1.3, "#2a2024", 0.85)
            s.ellipse(c[0], c[1], 1.4, 0.7, lit("#cfe0e8", (gx, 53, gz)), 0.9)
        # yesterday's papers on the floor under the little table
        for k in range(3):
            pp_ = [(tx - 12 + k * 2, 0.4 + k * 0.8, tz + 6 + k), (tx + 12 + k, 0.4 + k * 0.8, tz + 3 - k), (tx + 14 - k, 0.4 + k * 0.8, tz + 20), (tx - 10, 0.4 + k * 0.8, tz + 23 - k)]
            quad(s, pp_, lit(("#d8d2c0", "#e8e2d0", "#cfc8b4")[k], (tx, 1, tz + 12)))
            seg(s, [pp_[0], pp_[1]], DARK, 0.6, 0.35)
        # ---- his slippers, waiting in front of the chair
        for k, (lx, lz, an) in enumerate(((-13, -66, -0.25), (5, -62, 0.12))):
            c = t.p(lx, 0, lz)
            an += math.radians(a["ang"])
            ca, sa = math.cos(an), math.sin(an)
            sole = [(c[0] + ux * ca - uz * sa, 1.0, c[2] + ux * sa + uz * ca) for ux, uz in ((-5, -13), (5, -13), (6, 6), (4, 13), (-4, 13), (-6, 6))]
            quad(s, [(x + 2, 0.1, z - 1) for x, y, z in sole], DARK, 0.35)
            quad(s, sole, lit("#7a4a30", c))
            topp = [(c[0] + ux * ca - uz * sa, 5.0, c[2] + ux * sa + uz * ca) for ux, uz in ((-5, -2), (5, -2), (5.5, 7), (3.5, 13), (-3.5, 13), (-5.5, 7))]
            quad(s, topp, lit("#a8423a", (c[0], 5, c[2])))
            seg(s, [topp[0], topp[1]], lit("#e8d8c0", (c[0], 5, c[2])), 1.2)
        return [s]
    run(L, fine, "armchair", [(lay_lamp_foot, reading_lamp), (lay_body, fine_body), (lay_near_arm, fine_near_arm), (lay_table, fine_table)])


def reading_lamp():
    x, y, z = FLOORLAMP
    s = Sheet(SHAPE)
    disc(s, x, 3.2, z, 12, 9.5, lit("#c9a050", (x, 3, z - 10)))
    disc(s, x - 2, 3.4, z - 1, 5, 3.5, lit("#f0d078", (x, 3, z - 10)), 0.8)
    a, b = P(x, 3, z), P(x, y - 14, z)
    s.line([(a[0] - 0.7, a[1]), (b[0] - 0.7, b[1])], lit("#f0d078", (x - 8, 80, z - 8), (-0.8, 0, -0.6)), 0.9, 0.9)
    for yy in (40, 96):
        c = P(x, yy, z)
        s.ellipse(c[0], c[1], 2.4, 1.6, lit("#e8c060", (x - 6, yy, z - 6), (-0.5, 0.3, -0.8)))
    s2 = Sheet(SHAPE)
    shade(s2, (x, y, z), y - 15, y + 15, 25, 13, "#ffe2a0", "#dc9442", top_c="#fff8dc", ribs=9, fringe=3.2)
    c = P(x + 9, y - 15, z - 10)
    s2.line([(c[0], c[1]), (c[0], c[1] + 14)], "#f0d078", 0.7, 0.9)                                     # the pull chain
    s2.ellipse(c[0], c[1] + 15, 1.2, 1.2, "#f0d078")
    return [s, s2]


def front_plane():
    """Right at the front, bottom left: the old aspidistra in its pot. People always pass behind it.
    -> (color, coverage). It stands between us and the lamp, so it is mostly dark, with light along the
    edges of the leaves that lean toward the table."""
    rng = np.random.default_rng(SEED + 90)
    X, Z = -416.0, -10.0
    s = Sheet(SHAPE)
    k = cam.scale(Z)
    a, b = P(X, 0, Z), P(X, 32, Z)
    # the pot: glazed, blue-green, on a saucer
    s.ellipse(a[0], a[1] + 1, 18 * k, 6.5 * k, lit("#5a3a28", (X, 0, Z)))
    s.poly([(a[0] - 13 * k, a[1]), (a[0] + 13 * k, a[1]), (b[0] + 18 * k, b[1]), (b[0] - 18 * k, b[1])], lit("#3f8078", (X, 16, Z), (0.5, 0.2, -0.8)))
    s.poly([(a[0] + 2 * k, a[1]), (a[0] + 13 * k, a[1]), (b[0] + 18 * k, b[1]), (b[0] + 5 * k, b[1])], lit("#56a096", (X + 14, 16, Z), (0.9, 0.2, -0.4)))
    s.ellipse(a[0], a[1], 13 * k, 4.6 * k, lit("#3f8078", (X, 2, Z), (0.5, 0.2, -0.8)))
    s.ellipse(b[0], b[1], 18 * k, 6.2 * k, lit("#6ab0a4", (X, 34, Z)))
    s.ellipse(b[0], b[1] + 0.6, 15.5 * k, 5.0 * k, lit("#2a1c14", (X, 34, Z)))
    s.line([(b[0] + 10 * k, b[1] + 4), (a[0] + 8 * k, a[1] - 2)], "#c8f0e4", 1.0, 0.4)
    base = (b[0], b[1])
    dark, mid = "#0e1c18", "#17352a"
    light = lit("#2a5230", (X + 30, 80, Z), (0.7, 0.5, -0.5), 0.8)
    rim = lit("#7a9c4c", (X + 40, 90, Z), (0.8, 0.5, -0.3), 1.0)
    leaves = [(-1.15, 62, 10, 0.60), (-0.86, 84, 12, 0.46), (-0.58, 76, 11, 0.36), (-0.32, 96, 12, 0.20), (-0.06, 84, 11, 0.06), (0.16, 100, 13, -0.10),
              (0.40, 82, 11, -0.22), (0.62, 92, 12, -0.34), (0.86, 70, 10, -0.50), (-0.72, 52, 9, 0.7), (0.30, 58, 9, -0.1), (1.10, 54, 10, -0.70), (-0.14, 64, 10, 0.2)]
    order = sorted(range(len(leaves)), key=lambda i: -abs(leaves[i][0]))
    for i in order:
        ang, ln, wd, bend = leaves[i]
        ang += rng.normal(0, 0.05)
        spine = []
        x, y = base[0] + rng.normal(0, 3), base[1] - 1
        n = 14
        for q in range(n + 1):
            t = q / n
            a_ = ang - bend * t ** 1.6 * 1.35
            spine.append((x, y, a_, t))
            x += math.sin(a_) * ln / n
            y -= math.cos(a_) * ln / n
        left, right = [], []
        for (x, y, a_, t) in spine:
            w = wd * 0.16 if t < 0.22 else wd * math.sin(math.pi * (t - 0.22) / 0.78) ** 0.75 * (1.0 - 0.25 * t)
            left.append((x - math.cos(a_) * w, y - math.sin(a_) * w))
            right.append((x + math.cos(a_) * w, y + math.sin(a_) * w))
        mid_pts = [(x, y) for x, y, _, _ in spine]
        toward = ang > -0.2                                              # this leaf leans toward the lamp
        s.poly(left + right[::-1], dark)
        s.poly(mid_pts + right[::-1], light if toward else mid)
        if toward:
            s.line(right[4:], rim, 1.0, 0.9)
        else:
            s.line(right[5:12], light, 0.9, 0.6)
        s.line(mid_pts[2:], "#0c1c12" if not toward else "#2c5630", 0.9, 0.8)
        for q in range(4, n - 1):                                        # the ribs along it
            s.line([mid_pts[q], (lerp(mid_pts[q + 1][0], right[q + 1][0], 0.85), lerp(mid_pts[q + 1][1], right[q + 1][1], 0.85))], dark, 0.6, 0.30)
            s.line([mid_pts[q], (lerp(mid_pts[q + 1][0], left[q + 1][0], 0.85), lerp(mid_pts[q + 1][1], left[q + 1][1], 0.85))], "#000000", 0.6, 0.16)
        if i % 4 == 1:                                                   # an old leaf, yellowing at the tip
            s.poly([mid_pts[-4], right[-3], mid_pts[-1], left[-3]], "#8a8a3a", 0.5)
    return s.done()


def chain(rgb, alpha):
    """The pendant's chain: one plumb column of pixels from the ceiling rose down to the lamp, put on after
    everything else so that it stays whole in a cut-out with hard edges."""
    x, y, z = PENDANT
    top = P(x, y + 17, z)
    rose = ceil_pt(x, z)
    cx = int(round(top[0] - 0.5))
    y0, y1 = int(round(rose[1])) + 2, int(round(top[1])) + 1
    for yy in range(y0, y1):
        link = (yy - y0) % 4
        rgb[yy, cx] = col("#b08a44") * 0.55 if link == 1 else col("#1c1418")
        alpha[yy, cx] = 1.0


PIECES = (desk, piano, table, armchair)

"""The castle approach at Himeji (edo-castle), round twenty-three (DEPTH.md): what stands beyond the walked ground,
measured in the world and seen through the scene's own camera (edo_castle_kit: horizon 290, full 588, the lens 3.26 m
above the road, looking level).

Centimetres: X to the right of the lens's axis, Y up from the road, Z away from the lens. Every point goes through
proj(), so every line runs to its vanishing point on the horizon (row 290) and every upright stays upright.

THE KEEP. The main keep of Himeji as it stood in 1830 (finished 1609): five roofs outside, six floors inside, white
plaster on every wall and under every eave, grey tile roofs with white-plastered ridges and hips, gables on the roof
slopes (triangular chidori gables, a great hip-and-gable on the second roof, curved kara gables), the top roof's ridge
with a fish at each end, on a tall stone base whose sides curve out toward the foot. The plan and the gables' places
are our own simplification, not any drawing's.

It stands 100 m off, turned forty degrees: its long face (toward us and the low sun in the west) is lit, its short face
is in shade. The middle of its top ridge is where the old keep's top was (x 360, row 34): every heron in the moat still
faces it. From its right-hand side a corridor turret runs on along the keep's line, behind the gate tower: the castle's
buildings are joined, and the keep is not a model standing alone in the sky.

THE TREE BEYOND THE RIGHT EDGE. Not in the picture: an old pine on the road's verge 9.5 m off and 8 m to the right of
the lens's axis. Through the sun (edo_castle_kit.SUN) its trunk throws a long shadow in from the right across the
ramp's foot to the near bank, and its crown a dappled shade over the moat and the bank under the cherry.

  python3 edo_castle_model.py      the skeleton: the faces flat-shaded over the old picture (out/edo-castle-skeleton.png)
"""

import math

import numpy as np

from edo_castle_kit import EYE, FOC, HZ, SUN

VX = 400.0


def proj(X, Y, Z):
    """A place in the world (cm) -> the picture."""
    k = FOC / Z
    return (VX + X * k, HZ + (EYE - Y) * k)


def unproj_x(x, Z):
    return (x - VX) * Z / FOC


def unit(v):
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v)


S3 = unit(SUN)                                               # toward the sun: right, up, toward us


class Frame:
    """A building's own axes on the ground: u along its long face (to the right and away), v across it (away)."""

    def __init__(self, X, Z, theta_deg):
        t = math.radians(theta_deg)
        self.X, self.Z = X, Z
        self.u = np.array([math.cos(t), 0.0, math.sin(t)])
        self.v = np.array([-math.sin(t), 0.0, math.cos(t)])

    def w(self, a, y, b):
        """Local (a along u, y up, b along v) -> world (X, Y, Z)."""
        return (self.X + a * self.u[0] + b * self.v[0], y, self.Z + a * self.u[2] + b * self.v[2])

    def p(self, a, y, b):
        return proj(*self.w(a, y, b))

    def normal(self, na, ny, nb):
        return unit(na * self.u + np.array([0.0, ny, 0.0]) + nb * self.v)

    def k(self, a, b):
        """Pixels per cm at a place of the building."""
        return FOC / self.w(a, 0, b)[2]


def lit_of(n):
    """How squarely a face looks at the sun (negative: it is in shade)."""
    return float(np.dot(n, S3))


# ---------------------------------------------------------------- the main keep, measured
THETA = 40.0
KEEP_Z = 10000.0
TOP_ROW = 34.0                                              # the middle of the top ridge: where the herons look
STOREYS = [  # half size along u, along v; the wall's height; the eave's reach; the roof's rise to the next storey's foot
    (1180, 960, 470, 260, 300),
    (1000, 800, 390, 240, 260),
    (830, 660, 350, 220, 230),
    (680, 540, 310, 200, 200),
    (540, 430, 300, 190, 400),                              # the top: its ridge 4 m over the eave
]
#        roof, face, place along it (-1 left end .. 1 right end), width, height (cm), kind, how far up the slope it stands
GABLES = [
    (0, "front", -0.46, 560, 330, "chidori", 0.08),
    (0, "front", 0.46, 560, 330, "chidori", 0.08),
    (0, "left", 0.02, 520, 310, "chidori", 0.08),
    (1, "front", 0.0, 1180, 470, "irimoya", 0.0),
    (1, "left", 0.0, 520, 170, "kara", 0.0),
    (2, "front", -0.42, 420, 250, "chidori", 0.10),
    (2, "front", 0.42, 420, 250, "chidori", 0.10),
    (2, "left", 0.0, 400, 240, "chidori", 0.10),
    (3, "front", 0.0, 480, 170, "kara", 0.0),
    (3, "left", 0.0, 330, 200, "chidori", 0.12),
]
WINDOWS = [(6, 4), (5, 4), (4, 3), (3, 3), (3, 2)]          # on each storey: the long face, the short face
BASE_FLARE = 700.0                                          # how far the stone base reaches out at its foot (cm)
BASE_HEIGHT = 1600.0


def storey_rows(yb):
    """Each storey's numbers from the base's top yb: dict(A, B, y0, y1, e, ye, lift, y2, A2, B2, top)."""
    out, y = [], yb
    for i, (A, B, h, e, rise) in enumerate(STOREYS):
        y0, y1 = y, y + h
        d = dict(i=i, A=A, B=B, y0=y0, y1=y1, e=e, ye=y1 - 12, lift=48 + 4 * i, top=(i == len(STOREYS) - 1))
        if d["top"]:
            d.update(ridge_a=A - B * 0.62, yr=y1 + rise)
        else:
            d.update(y2=y1 + rise, A2=STOREYS[i + 1][0], B2=STOREYS[i + 1][1])
        out.append(d)
        y = y1 + rise
    return out


def keep_frame():
    """The keep's frame and its base's top: placed so that the middle of the top ridge is at x 360, row TOP_ROW."""
    rows = storey_rows(0.0)
    top_y = rows[-1]["yr"]
    Y_top = EYE + (HZ - TOP_ROW) * KEEP_Z / FOC
    yb = Y_top - top_y
    return Frame(unproj_x(360.0, KEEP_Z), KEEP_Z, THETA), yb


def eave_pts(fr, d, side, n=18, out=0.0):
    """An eave edge with its corners lifted (the sori): the left eave from the back corner to the near corner, the
    front eave from the near corner to the right-hand corner. `out` reaches a little further (the tiles' ends)."""
    Ae, Be = d["A"] + d["e"] + out, d["B"] + d["e"] + out
    pts = []
    for j in range(n + 1):
        t = j / n
        c = abs(2 * t - 1) ** 3.2
        y = d["ye"] + d["lift"] * c
        if side == "left":
            pts.append(fr.p(-Ae, y, Be - 2 * Be * t))
        else:
            pts.append(fr.p(-Ae + 2 * Ae * t, y, -Be))
    return pts


def slope_at(d, side, f):
    """The skirt roof's front or left slope: (its b or a coordinate, its height) a fraction f of the way up."""
    if side == "front":
        b0, b1 = -(d["B"] + d["e"]), -d["B2"]
    else:
        b0, b1 = -(d["A"] + d["e"]), -d["A2"]
    return b0 + (b1 - b0) * f, d["ye"] + (d["y2"] - d["ye"]) * f


# ---------------------------------------------------------------- the corridor turret, on from the keep's right side
WING = dict(a0=900.0, a1=5200.0, b0=-520.0, b1=380.0, h=400.0, e=170.0, rise=220.0, drop=330.0)


def wing_rows(yb):
    """The corridor turret: one storey of white wall (a row of windows), a hip roof; its floor a little under the
    keep's base top (its stone platform steps down)."""
    y0 = yb - WING["drop"]
    return dict(A0=WING["a0"], A1=WING["a1"], B0=WING["b0"], B1=WING["b1"], y0=y0, y1=y0 + WING["h"], e=WING["e"],
                ye=y0 + WING["h"] - 10, yr=y0 + WING["h"] + WING["rise"], lift=40.0)


# ---------------------------------------------------------------- the pine beyond the right edge (only its shadow is seen)
TREE = dict(X=780.0, Z=980.0, trunk=46.0, crown=(330.0, 760.0), spread=300.0)


def tree_blobs(seed=5):
    """The pine's crown as clumps of needles (each a ball: X, Y, Z, radius) with gaps between them, and its trunk."""
    rng = np.random.default_rng(seed)
    out = []
    X, Z = TREE["X"], TREE["Z"]
    lo, hi = TREE["crown"]
    for i in range(46):
        h = rng.uniform(lo, hi)
        r = TREE["spread"] * (1.0 - 0.55 * (h - lo) / (hi - lo)) * rng.uniform(0.3, 1.0)
        a = rng.uniform(0, 2 * math.pi)
        out.append((X + math.cos(a) * r - 120.0 * (h - lo) / (hi - lo), h, Z + math.sin(a) * r * 0.8, rng.uniform(50, 105)))
    return out


def ground_shadow_of(X, Y, Z):
    """Where the sun throws the shadow of a point onto the road's level: (X, Z)."""
    return (X - S3[0] / S3[1] * Y, Z - S3[2] / S3[1] * Y)


if __name__ == "__main__":
    import os
    from PIL import Image, ImageDraw
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    fr, yb = keep_frame()
    rows = storey_rows(yb)
    im = Image.open("out/edo-castle-before.png").convert("RGB")
    d = ImageDraw.Draw(im, "RGBA")
    for st in rows:
        A, B = st["A"], st["B"]
        for side, pts, n in (("left", [fr.p(-A, st["y0"], B), fr.p(-A, st["y0"], -B), fr.p(-A, st["y1"], -B), fr.p(-A, st["y1"], B)], fr.normal(-1, 0, 0)),
                             ("front", [fr.p(-A, st["y0"], -B), fr.p(A, st["y0"], -B), fr.p(A, st["y1"], -B), fr.p(-A, st["y1"], -B)], fr.normal(0, 0, -1))):
            L = max(lit_of(n), 0) * 0.5 + 0.5
            d.polygon(pts, fill=(int(245 * L), int(238 * L), int(220 * L), 255), outline=(20, 30, 60, 255))
        for side in ("left", "front"):
            ev = eave_pts(fr, st, side)
            if st["top"]:
                ra, yr = st["ridge_a"], st["yr"]
                top = [fr.p(ra, yr, 0), fr.p(-ra, yr, 0)] if side == "front" else [fr.p(-ra, yr, 0)]
            else:
                top = [fr.p(st["A2"], st["y2"], -st["B2"]), fr.p(-st["A2"], st["y2"], -st["B2"])] if side == "front" else [fr.p(-st["A2"], st["y2"], -st["B2"]), fr.p(-st["A2"], st["y2"], st["B2"])]
            d.polygon(ev + top, fill=(70, 80, 110, 255), outline=(20, 30, 60, 255))
    w = wing_rows(yb)
    d.polygon([fr.p(w["A0"], w["y0"], w["B0"]), fr.p(w["A1"], w["y0"], w["B0"]), fr.p(w["A1"], w["y1"], w["B0"]), fr.p(w["A0"], w["y1"], w["B0"])], fill=(240, 232, 214, 255), outline=(20, 30, 60, 255))
    d.line([(0, HZ), (800, HZ)], fill=(255, 0, 255, 120))
    d.ellipse([356, TOP_ROW - 4, 364, TOP_ROW + 4], outline=(255, 0, 0, 255))
    for (X, Y, Z, r) in tree_blobs():
        gx, gz = ground_shadow_of(X, Y, Z)
        if gz > 900:
            x, y = proj(gx, 0, gz)
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(0, 0, 0, 160))
    for h in range(0, 330, 30):
        gx, gz = ground_shadow_of(TREE["X"], h, TREE["Z"])
        x, y = proj(gx, 0, gz)
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(200, 0, 0, 200))
    im.save("out/edo-castle-skeleton.png")
    print("base top", round(yb), "cm; the base's top row", round(fr.p(-1180, yb, -960)[1]), "; frame", round(fr.X), round(fr.Z))

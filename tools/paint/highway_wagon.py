"""The family wagon seen from behind, driving away from us into the sunset: the cut-out the game moves
up the highway in the opening movie.

It is the same car as example/wagon.py (which shows it from the side): the same red, the same wood down
its flanks and across its tailgate, the same rack with the same three things tied on it, in the same
order from the back of the car forward: the blue cooler, the green trunk, the tan suitcase. Heights are
wagon.py's own (bumper 20-31, wood 30-53, belt line 62, glass 64-89, roof 95, rack 99); across, the
car is 128 of the same units wide. One liberty: in wagon.py the three things lie in a line down the
middle of the roof, and from dead behind the trunk would hide the suitcase altogether, so here they
are stowed a little askew (cooler to the right, suitcase out to the left) and all three can be seen.

Measurements: u across the car from its middle (left is the driver's side), v UP from the road,
q forward from the tail. We stand behind and a little above, so things further forward show a little
higher and a little smaller (RISE, SHRINK).

LIGHT: the sun is low and dead ahead of the car. The back of it, which is all we see, is in warm
shadow; the sky behind us puts a little violet into the chrome and the glass; and everything that
faces up or stands against the sky carries a rim of gold: the roof, the top of each piece of luggage,
the rails, the shoulders of the body, the hair of the two heads against the windshield.

Two frames: in the second the body rides 3 px lower on its springs. The wheels, the shadow and the
ground do not move (and the body is the very same pixels in both: see write()). The shadow and the
dust are stippled, because a cut-out's edge is hard: scaled down smoothly they read as soft.

    python3 highway_wagon.py     paints out/highway-wagon-try.png (both frames) to look at
"""

import math

import numpy as np

from brush import *
from highway_kit import Paper, grade

# The car's own colors, word for word from example/wagon.py (copied, not imported, so that this file does not
# change under us if somebody is at work on wagon.py):
RED = dict(top="#f29478", shine="#ffd0b4", side="#cf5a42", low="#a84330", front="#e67a5a", dark="#70291f")
WOOD = dict(frame="#e2bc80", field="#a87444", grain="#7e5230", dark="#5c3a20")
GLASS = dict(dark="#182238", mid="#34466c", sky="#8fb6de", shine="#e4f2ff")
CHROME = dict(shine="#ffffff", light="#d8dde2", mid="#9aa2aa", dark="#565c66")
RUBBER = dict(lit="#4c4852", mid="#2a2730", dark="#141218")
LEATHER = dict(top="#d99a5c", end="#e8b070", front="#b4733e", dark="#6e4426", strap="#4a2c18")
TRUNK = dict(top="#5f8a80", end="#6c988c", front="#3f625a", dark="#243a36", slat="#c89c5e", brass="#f0c860")
COOLER = dict(top="#fbf6e8", end="#7fb2e6", front="#4a84c8", dark="#2c5690", lid="#e2dccb", lidend="#fffdf4")

K = 3.0                                                     # pixels per unit at full size (the body is 128 units: 384 px; with bumper and mirror about 420)
RISE, SHRINK = 0.105, 0.0011
SHEET = (560, 560)
DROP = 3                                                    # how far the body sits down in the second frame, px
ORIGIN = (282.0, 470.0)                                     # where the middle of the rear axle meets the road, on the sheet

# the back of the car is in shadow: wagon.py's colors, each taken down and warmed
SHADE = dict(hi="#ac4636", mid="#93382d", low="#722927", dark="#4e1a1e", rim="#ffb46e", fire="#ffe4a4", roof="#ee8458", roof_hi="#ffc48c")
WOOD_S = dict(frame="#c69c66", frame_hi="#e6c084", field="#8c5c38", grain="#683f26", dark="#4a2d1a")
CHROME_S = dict(sky="#7c7aa8", pale="#c9bfd2", line="#35304a", road="#857a94", hot="#fff0d0", edge="#ffd49a")
GLASS_S = dict(dark="#141628", mid="#232a48", seat="#1c1a2e", glow_top="#e86c58", glow_mid="#ffa052", glow_low="#ffe08c", sheen="#8f86c8")


def shade(color, by=0.72, warm=0.04):
    """A lit color from wagon.py as it is on the side away from the sun."""
    c = rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
    c = c * by
    return np.clip(c + np.array([warm, 0.0, warm * 0.4], dtype=F32), 0, 1)


class Rear:
    """Draws in the car's own measurements onto a sheet. Give the sheet of flat color `hide` (the sheet of
    crisp lines that will be laid over it) and every solid shape drawn also rubs out the lines it covers,
    so that a line on a far thing does not show through a near one."""

    def __init__(self, sheet, origin=ORIGIN, k=K, hide=None):
        self.s, self.o, self.k, self.hide = sheet, origin, k, hide

    def pt(self, u, v, q=0.0):
        f = 1.0 - q * SHRINK
        return (self.o[0] + u * f * self.k, self.o[1] - (v + q * RISE) * self.k)

    def pts(self, points):
        return [self.pt(*p) for p in points]

    def poly(self, points, color, alpha=1.0):
        p = self.pts(points)
        self.s.poly(p, color, alpha)
        if self.hide is not None and alpha >= 0.999:
            Sheet.poly(self.hide, p, "#000000", 0.0)
        return self

    def line(self, points, color, width=1.0, alpha=1.0):
        self.s.line(self.pts(points), color, width * self.k / 3.0, alpha)
        return self

    def taper(self, points, color, w0, w1, alpha=1.0):
        self.s.taper(self.pts(points), color, w0 * self.k / 3.0, w1 * self.k / 3.0, alpha)
        return self

    def oval(self, u, v, ru, rv, color, alpha=1.0, q=0.0):
        c = self.pt(u, v, q)
        self.s.ellipse(c[0], c[1], ru * self.k, rv * self.k, color, alpha)
        if self.hide is not None and alpha >= 0.999:
            Sheet.ellipse(self.hide, c[0], c[1], ru * self.k, rv * self.k, "#000000", 0.0)
        return self

    def rect(self, u0, u1, v0, v1, color, alpha=1.0, q=0.0):
        return self.poly([(u0, v0, q), (u1, v0, q), (u1, v1, q), (u0, v1, q)], color, alpha)

    def box(self, u0, u1, v0, v1, q0, q1, face, top, alpha=1.0):
        """A box on the roof: the face toward us, and its top running away forward."""
        self.poly([(u0, v1, q0), (u1, v1, q0), (u1, v1, q1), (u0, v1, q1)], top, alpha)
        self.poly([(u0, v0, q0), (u1, v0, q0), (u1, v1, q0), (u0, v1, q0)], face, alpha)
        return self


def rounded(u0, u1, v0, v1, r, n=4):
    """A rectangle with round corners, as points."""
    out = []
    for (cu, cv, a0) in ((u1 - r, v1 - r, 0), (u0 + r, v1 - r, 90), (u0 + r, v0 + r, 180), (u1 - r, v0 + r, 270)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            out.append((cu + math.cos(a) * r, cv + math.sin(a) * r))
    return out


# ------------------------------------------------------------------------------------------ what does not move
def running_gear(base, lines):
    """The wheels, the axle between them, and the dark under the car."""
    d, dl = Rear(base, hide=lines), Rear(lines)
    # under the car it is dark, and darkest on the road itself
    d.poly([(-60, 0), (60, 0), (58, 26), (-58, 26)], "#1e1524")
    d.poly([(-66, -1.5), (66, -1.5), (62, 3), (-62, 3)], "#1a1322")
    # the back axle: a tube, the lump of the differential in the middle of it, a spring and a damper each side
    d.line([(-46, 17.5), (46, 17.5)], "#2c2734", 7.5)
    dl.line([(-44, 18.6), (44, 18.6)], "#4a4458", 1.0, 0.8)
    d.oval(2, 17.5, 8.5, 7.5, "#2e2836")
    d.oval(1.2, 18.6, 5.2, 4.4, "#484256")
    dl.oval(0.4, 19.6, 1.6, 1.3, "#6a647a")
    for sgn in (-1, 1):
        d.line([(sgn * 33, 15), (sgn * 27, 28)], "#3a3444", 3.4)
        dl.line([(sgn * 39, 13), (sgn * 39, 26)], "#252030", 2.2)
    # the tank hangs under the floor, and the tail pipe comes out on the driver's side
    d.poly([(-22, 13), (26, 13), (30, 24), (-26, 24)], "#261e2c")
    dl.line([(-20, 13.4), (24, 13.4)], "#3c3648", 0.9, 0.8)
    d.line([(-36, 15.2), (-36, 15.2, -14)], CHROME_S["road"], 6.6)
    dl.oval(-36, 13.9, 2.6, 2.3, CHROME_S["pale"], q=-14)
    dl.oval(-36, 13.9, 1.6, 1.4, "#17121c", q=-14)
    dl.line([(-38.4, 15.6, -14), (-36.4, 16.2, -14)], CHROME_S["hot"], 0.9)
    # the tires: seen from behind, two tall dark slabs with the tread running up them
    for sgn in (-1, 1):
        u0, u1 = sgn * 43.0, sgn * 60.5
        lo, hi = min(u0, u1), max(u0, u1)
        d.poly(rounded(lo, hi, 0, 44, 4.5), RUBBER["mid"])
        d.poly(rounded(lo + 1.2, hi - 1.2, 0, 10, 3.2), RUBBER["dark"])                     # it turns under, into its own shadow
        d.rect(lo + 2, hi - 2, 11, 30, RUBBER["lit"])
        for g in (0.24, 0.5, 0.76):                                                           # the grooves of the tread
            gu = lerp(lo, hi, g)
            dl.line([(gu, 1.5), (gu + sgn * 0.3, 26)], RUBBER["dark"], 1.3, 0.9)
        for b in range(8):                                                                    # and the blocks across it
            bv = 2.5 + b * 3.0
            dl.line([(lo + 1.5, bv), (hi - 1.5, bv + 0.6)], RUBBER["dark"], 0.8, 0.55)
        # the outer edge of each tire catches the light that comes round the car
        dl.line([(sgn * 60.3, 4), (sgn * 60.4, 22)], SHADE["rim"], 1.1, 0.85)
        dl.line([(sgn * 43.4, 5), (sgn * 43.4, 16)], "#5c5870", 0.9, 0.6)


BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], dtype=F32) / 16.0 + 1 / 32.0


def stipple(dens, x, y):
    """A soft amount (0..1) as a hard yes or no, by an ordered pattern: the old way to make a thing half there."""
    return (dens > BAYER[(y.astype(int)) % 4, (x.astype(int)) % 4]).astype(F32)


def ground_shadow(shape, origin=ORIGIN, k=K):
    """The car's shadow on the road. It lies toward us, because the sun is ahead. -> (color, alpha): the
    alpha is stippled, thinner and thinner as the shadow runs out, so that the edge of a hard cut-out
    still looks like a shadow."""
    x, y = grid(shape)
    u = (x - origin[0]) / k
    v = (origin[1] - y) / k                                           # negative below the axle (toward us)
    reach = 25.0 + (noise(shape, (60, 400), 90, 2) - 0.5) * 9.0        # its far end is not ruled
    half = 65.0 + np.clip(-v, 0, 40) * 0.20
    side = np.clip((half - np.abs(u)) / 6.0, 0, 1)
    along = np.clip(1 - (-v) / reach, 0, 1) * (v < 2.0)
    dens = side * along ** 0.7
    dens = np.where((v > -5.0) & (v < 2.0) & (np.abs(u) < 63), np.maximum(dens, side), dens)       # right under the tail it is solid
    dens *= 0.82 + 0.36 * noise(shape, (26, 5), 91, 2)
    color = np.empty(shape + (3,), dtype=F32)
    color[...] = rgb("#2a2342")
    color *= (1 + (noise(shape, 12, 92, 2) - 0.5)[..., None] * 0.12)
    return np.clip(color, 0, 1), stipple(dens * 0.96, x, y)


def dust(shape, frame, origin=ORIGIN, k=K):
    """A little dust behind each back wheel, low on the road and lit from beyond: pale along its top, mauve
    inside. Stippled at the edges, like the shadow. The two frames differ a little, so that it stirs."""
    rng = np.random.default_rng(40)
    x, y = grid(shape)
    dens = np.zeros(shape, dtype=F32)
    for sgn in (-1, 1):
        for i in range(6):
            cu = sgn * (59 + i * 3.6 + rng.random() * 2.5) + (1.6 if frame else 0.0) * sgn * (i / 5.0)
            cv = 2.2 + rng.random() * 2.6 + (0.9 if (frame and i % 2) else 0.0) + i * 0.25
            r = (4.6 - i * 0.42) * (0.85 + 0.3 * rng.random())
            cx, cy = origin[0] + cu * k, origin[1] - cv * k
            d2 = ((x - cx) / (r * 1.55 * k)) ** 2 + ((y - cy) / (r * 0.95 * k)) ** 2
            dens = np.maximum(dens, np.clip(1 - d2, 0, 1) ** 0.8 * (1.0 - i * 0.11))
    dens *= np.clip((origin[1] + 1.2 * k - y) / (1.6 * k), 0, 1)       # it lies on the road
    dens = np.clip(dens * (0.72 + 0.56 * noise(shape, 11, 50 + frame, 3)), 0, 1)
    gy, gx = np.gradient(blur(dens, 2.2))
    top = np.clip(gy * 26, 0, 1)                                       # the upper edges, where the light comes through
    color = ramp(np.clip(top, 0, 1), [(0.0, "#8c6c80"), (0.35, "#b0868a"), (0.7, "#dcaa8c"), (1.0, "#ffd9a2")])
    return np.clip(color, 0, 1), stipple(np.clip(dens * 1.15 - 0.06, 0, 1), x, y)


# ------------------------------------------------------------------------------------------ what rides on the springs
def luggage(d, dl):
    """The three things on the rack, furthest forward first: suitcase, trunk, cooler. The sun is beyond
    them: every lid is bright and every far edge burns; the faces toward us are in shade."""
    v0 = 100.0
    cord, cord2 = shade("#b8322c", 0.90), shade("#e8d8a0", 0.84)

    # ---- the suitcase: flat on its back, its handle over the driver's side, straps right round it
    u0, u1, h, q0, q1 = -50.0, 12.0, 15.0, 82.0, 132.0
    d.box(u0, u1, v0, v0 + h, q0, q1, shade(LEATHER["front"], 0.74), shade(LEATHER["top"], 1.08, 0.06))
    for su in (u0 + 8, u0 + 44):                                                           # the straps
        d.rect(su, su + 3.4, v0, v0 + h, shade(LEATHER["strap"], 0.8), q=q0)
        d.poly([(su, v0 + h, q0), (su + 3.4, v0 + h, q0), (su + 3.4, v0 + h, q1), (su, v0 + h, q1)], shade(LEATHER["dark"], 0.9))
    dl.poly([(u0 + 13, v0 + h, q0 + 8), (u0 + 22, v0 + h, q0 + 8), (u0 + 22, v0 + h, q0 + 34), (u0 + 13, v0 + h, q0 + 34)], shade("#e8e0c4", 0.98))      # stickers from other holidays
    dl.poly([(u0 + 25, v0 + h, q0 + 14), (u0 + 34, v0 + h, q0 + 12), (u0 + 35, v0 + h, q0 + 42), (u0 + 26, v0 + h, q0 + 44)], shade("#5aa0d0", 0.98))
    dl.poly([(u0 + 16, v0 + h, q0 + 28), (u0 + 24, v0 + h, q0 + 30), (u0 + 23, v0 + h, q0 + 48), (u0 + 15, v0 + h, q0 + 46)], shade("#e0584a", 0.98))
    dl.line([(u0, v0 + h * 0.5, q0 + 14), (u0 - 3.4, v0 + h * 0.9, q0 + 16), (u0 - 3.4, v0 + h * 0.9, q0 + 30), (u0, v0 + h * 0.5, q0 + 32)], shade(LEATHER["dark"], 0.8), 1.8)      # the handle
    for cu in (u0, u1):                                                                    # brass corners
        sg = 1 if cu == u0 else -1
        dl.poly([(cu, v0 + h, q0), (cu + sg * 3.6, v0 + h, q0), (cu, v0 + h - 3.6, q0)], shade(TRUNK["brass"], 0.9))
    dl.line([(u0, v0 + h, q1), (u1, v0 + h, q1)], SHADE["fire"], 1.6)                       # the far edge of its lid is in the sun
    dl.line([(u0, v0 + h, q0), (u0, v0 + h, q1)], SHADE["rim"], 1.2, 0.95)
    dl.line([(u0 + 1, v0 + h, q0), (u1, v0 + h, q0)], "#eab070", 1.0, 0.8)
    d.line([(u0 + 27, v0 + h, q0), (u0 + 27, v0 + h, q1)], cord, 1.3)                       # the cord over it
    dl.line([(u0 + 27, v0, q0), (u0 + 27, v0 + h, q0)], cord, 1.3)

    # ---- the trunk: a proper old one, wooden slats, brass corners, a leather handle on the end
    u0, u1, h, q0, q1 = -27.0, 46.0, 31.0, 32.0, 78.0
    d.box(u0, u1, v0, v0 + h, q0, q1, shade(TRUNK["front"], 0.80), shade(TRUNK["top"], 1.16, 0.10))
    d.rect(u0, u1, v0, v0 + 4.5, shade(TRUNK["front"], 0.62), q=q0)                                                                # it is darkest low down, where the roof shades it
    for su in (u0 + 2, u0 + 34, u1 - 6.5):                                                  # slats up the end and over the lid
        d.rect(su, su + 4.5, v0, v0 + h, shade(TRUNK["slat"], 0.74), q=q0)
        d.poly([(su, v0 + h, q0), (su + 4.5, v0 + h, q0), (su + 4.5, v0 + h, q1), (su, v0 + h, q1)], shade("#e0b878", 1.08, 0.06))
    dl.line([(u0, v0 + h * 0.66, q0), (u1, v0 + h * 0.66, q0)], shade(TRUNK["dark"], 0.8), 1.3)       # where the lid shuts
    dl.poly([(u0 + 17, v0 + h * 0.54, q0), (u0 + 22, v0 + h * 0.54, q0), (u0 + 22, v0 + h * 0.76, q0), (u0 + 17, v0 + h * 0.76, q0)], shade(TRUNK["brass"], 0.92))      # the hasp
    dl.line([(u0 + 19.5, v0 + h * 0.72, q0), (u0 + 19.5, v0 + h * 0.58, q0)], SHADE["fire"], 0.8, 0.8)
    dl.line([(u0 + 7, v0 + h * 0.42, q0), (u0 + 8.5, v0 + h * 0.30, q0), (u0 + 14.5, v0 + h * 0.30, q0), (u0 + 16, v0 + h * 0.42, q0)], shade(LEATHER["dark"], 0.8), 1.8)       # the handle hangs
    for (cu, cv) in ((u0, v0), (u1, v0), (u0, v0 + h), (u1, v0 + h)):
        sg = 1 if cu == u0 else -1
        up = 1 if cv == v0 else -1
        dl.poly([(cu, cv, q0), (cu + sg * 5.5, cv, q0), (cu, cv + up * 5.5, q0)], shade(TRUNK["brass"], 0.9))
    dl.line([(u0, v0 + h, q1), (u1, v0 + h, q1)], SHADE["fire"], 1.7)                       # sun along the far edge of the lid
    dl.line([(u0, v0 + h, q0), (u0, v0 + h, q1)], SHADE["rim"], 1.3, 0.95)
    dl.line([(u1, v0 + h, q0), (u1, v0 + h, q1)], SHADE["rim"], 1.1, 0.8)
    dl.line([(u0 + 1, v0 + h, q0), (u1, v0 + h, q0)], "#b6dccc", 1.0, 0.7)
    for cu, cq, col in ((-9.0, 50.0, cord2), (30.0, 60.0, cord)):                          # the cords over it: an old cream one, and a red
        dl.line([(cu, v0 + h, q0), (cu + 1.0, v0 + h, q1)], col, 1.3)
        dl.line([(cu - 0.4, v0, q0), (cu, v0 + h, q0)], col, 1.3)

    # ---- the cooler: blue, with a white lid that has seen better picnics. Nearest the tail.
    u0, u1, h, q0, q1 = -2.0, 48.0, 23.0, 1.0, 28.0
    d.box(u0, u1, v0, v0 + h - 5, q0, q1, shade(COOLER["front"], 0.78, 0.03), shade(COOLER["top"], 0.9))
    d.rect(u0, u1, v0, v0 + 3.6, shade(COOLER["dark"], 0.86), q=q0)
    d.box(u0 - 1, u1 + 1, v0 + h - 5, v0 + h, q0 - 1, q1 + 1, shade(COOLER["lid"], 0.78, 0.03), shade(COOLER["top"], 1.02, 0.04))
    dl.line([(u0 + 5, v0 + (h - 5) * 0.60, q0), (u1 - 5, v0 + (h - 5) * 0.60, q0)], shade("#d8ecff", 0.86), 2.0)                # the white stripe
    dl.line([(u0 - 1, v0 + h - 5, q0 - 1), (u1 + 1, v0 + h - 5, q0 - 1)], shade(COOLER["dark"], 0.7), 0.9, 0.8)                 # under the lip of the lid
    dl.poly([(u0 + 20, v0 + h - 5.2, q0 - 1), (u0 + 30, v0 + h - 5.2, q0 - 1), (u0 + 29, v0 + h - 8.4, q0 - 1), (u0 + 21, v0 + h - 8.4, q0 - 1)], shade("#f4f0e4", 0.8))      # the catch
    dl.line([(u0 - 1, v0 + h, q1 + 1), (u1 + 1, v0 + h, q1 + 1)], SHADE["fire"], 1.7)       # sun along the far edge of the lid
    dl.line([(u0 - 1, v0 + h, q0 - 1), (u0 - 1, v0 + h, q1 + 1)], SHADE["rim"], 1.2, 0.95)
    dl.line([(u1 + 1, v0 + h, q0 - 1), (u1 + 1, v0 + h, q1 + 1)], SHADE["rim"], 1.1, 0.8)
    dl.line([(u0, v0 + h, q0 - 1), (u1 + 1, v0 + h, q0 - 1)], "#fff6e0", 1.0, 0.8)
    dl.line([(36.0, v0 + h, q0 - 1), (36.6, v0 + h, q1 + 1)], cord, 1.3)                    # and the cord over that
    dl.line([(35.8, v0 + 0.5, q0), (36.0, v0 + h, q0 - 1)], cord, 1.3)
    dl.line([(u1 + 0.8, v0 + h * 0.5, 14), (50, 99.4, 8)], cord, 1.1)                       # a turn of it round the rail


def body(base, lines, aboard=True):
    """Everything that rides on the springs: bumper, tailgate, glass, roof, rack, luggage."""
    d, dl = Rear(base, hide=lines), Rear(lines)

    # ---- the roof, seen from a little above: it runs away from us and the low sun lies along it
    d.poly([(-53, 92.5), (53, 92.5), (53, 95, 142), (-53, 95, 142)], SHADE["roof"])
    d.poly([(-50, 95, 60), (50, 95, 60), (51, 95, 142), (-51, 95, 142)], SHADE["roof_hi"], 0.85)
    d.poly([(-34, 95, 96), (8, 95, 96), (12, 95, 142), (-40, 95, 142)], "#ffe0b0", 0.6)
    dl.line([(-53, 95, 142), (53, 95, 142)], SHADE["fire"], 1.4)
    # ---- the aerial on the front wing, and the driver's door mirror, both far forward
    dl.line([(-62, 62, 172), (-61.4, 104, 178)], "#2a2030", 1.0)
    dl.line([(-61.5, 96, 177), (-61.4, 104, 178)], SHADE["rim"], 0.9, 0.9)
    dl.oval(-61.4, 104.6, 0.7, 0.7, SHADE["fire"], q=178)
    dl.line([(-63, 65.4, 141), (-70, 66.6, 141)], CHROME_S["line"], 2.6)
    dl.oval(-72.4, 67.6, 5.0, 3.8, CHROME_S["line"], q=141)
    dl.oval(-72.4, 67.6, 3.9, 2.8, "#5c5a8a", q=141)
    dl.oval(-73.2, 68.3, 2.0, 1.2, "#9a94c0", q=141)
    dl.line([(-75.6, 70.8, 141), (-69.4, 71.0, 141)], SHADE["fire"], 0.9, 0.9)
    # ---- the rack: far rail and bars first; they go under the luggage
    d.line([(-50, 99, 134), (50, 99, 134)], CHROME_S["road"], 1.5)
    for cq in (44.0, 90.0):
        d.line([(-50, 99, cq), (50, 99, cq)], CHROME_S["line"], 1.4)
    for sgn in (-1, 1):
        d.line([(sgn * 50, 99, 0), (sgn * 50, 99, 134)], CHROME_S["road"], 1.6)
        for cq in (2.0, 66.0, 132.0):
            d.line([(sgn * 50, 95, cq), (sgn * 50, 99, cq)], CHROME_S["line"], 1.6)
    luggage(d, dl)
    for sgn in (-1, 1):                                                                    # the side rails catch the sun along their tops
        dl.line([(sgn * 50, 99.5, 0), (sgn * 50, 99.5, 134)], SHADE["rim"], 0.9, 0.85)
    dl.line([(-50, 99, 0), (50, 99, 0)], CHROME_S["pale"], 1.7)                             # the rail across the tail goes over the cooler's foot
    dl.line([(-50, 99.6, 0), (50, 99.6, 0)], CHROME_S["hot"], 0.7, 0.9)
    for su in (-50, 50):
        dl.line([(su, 94.5, 0), (su, 99, 0)], CHROME_S["road"], 1.8)

    # ---- the cabin: two pillars and the tailgate window between them
    d.poly([(-62.5, 61), (-53.5, 92), (-50, 94.6), (50, 94.6), (53.5, 92), (62.5, 61)], SHADE["mid"])
    d.poly([(-53.5, 91), (-50, 94.6), (50, 94.6), (53.5, 91)], SHADE["hi"])                # the roof turns over toward us
    dl.line([(-52, 93.6), (52, 93.6)], SHADE["rim"], 1.0, 0.9)
    for sgn in (-1, 1):                                                                    # the pillars: a little sky down their outer edge
        d.poly([(sgn * 62.5, 61), (sgn * 53.5, 92), (sgn * 51.5, 92), (sgn * 59.5, 63)], SHADE["hi"], 0.7)
        dl.line([(sgn * 62.6, 62), (sgn * 53.8, 91.6)], SHADE["rim"], 1.0, 0.75)
    win = [(-55.5, 66.5), (-56, 68), (-49.6, 88.2), (-47.6, 89.6), (47.6, 89.6), (49.6, 88.2), (56, 68), (55.5, 66.5), (53.5, 65), (-53.5, 65)]
    d.poly(win, GLASS_S["dark"])
    # through the glass: the windshield, far forward, full of the sky the car is driving into
    wsh = [(-41, 72.2), (-37, 85.4), (37, 85.4), (41, 72.2)]
    d.poly(wsh, GLASS_S["glow_mid"])
    d.poly([(-41, 72.2), (-39.4, 77.4), (39.4, 77.4), (41, 72.2)], GLASS_S["glow_low"])
    d.poly([(-38.2, 81.6), (-37, 85.4), (37, 85.4), (38.2, 81.6)], GLASS_S["glow_top"])
    d.poly([(-6, 72.2), (6, 72.2), (9, 76.4), (-9, 76.4)], "#fff6c8", 0.8)                  # the sun itself is in the middle of it
    d.poly([(-41, 72.2), (-6, 72.2), (-12, 73.8), (-40.6, 73.6)], "#8a5a78", 0.75)           # far mesas, through the glass
    d.poly([(41, 72.2), (9, 72.2), (16, 73.4), (40.6, 73.9)], "#8a5a78", 0.75)
    dl.line([(-5, 85.4), (-4.6, 82.6), (5.4, 82.6), (5.8, 85.4)], GLASS_S["dark"], 1.0)      # the mirror hangs from the top of it
    d.rect(-4.8, 5.6, 82.4, 84.6, GLASS_S["dark"])
    for sgn in (-1, 1):                                                                    # the side glass: slivers of dusk
        d.poly([(sgn * 44.5, 73), (sgn * 49.2, 73), (sgn * 45.4, 85.2), (sgn * 41.6, 85.2)], "#6a4a86", 0.9)
    d.poly([(-56, 66.5), (56, 66.5), (53.2, 71.2), (-53.2, 71.2)], GLASS_S["seat"])          # the back of the back seat
    dl.line([(-52.6, 71.2), (52.6, 71.2)], "#4a4470", 1.0, 0.8)
    d.poly([(-43, 71.0), (-42, 76.2), (-40, 77.2), (40, 77.2), (42, 76.2), (43, 71.0)], "#191628")   # the front seat's back, against the light
    if aboard:
        # Dad at the wheel: his head and shoulders against the windshield, the sun in his hair
        d.poly([(-33, 71.0), (-32, 75.6), (-27.4, 78.0), (-17.6, 78.0), (-13, 75.6), (-12, 71.0)], "#1a1526")
        d.oval(-22.5, 80.6, 5.3, 6.2, "#1c1624")
        d.oval(-22.5, 82.0, 5.5, 5.0, shade("#4d301a", 0.62))
        dl.line([(-27.4, 84.2), (-25.2, 86.6), (-22.2, 87.4), (-19.4, 86.6), (-17.4, 84.4)], SHADE["rim"], 1.2, 0.95)
        dl.line([(-24.4, 87.1), (-21.0, 87.3)], SHADE["fire"], 0.9)
        dl.line([(-28.2, 80.0), (-28.3, 82.6)], SHADE["rim"], 0.9, 0.6)                    # an ear
        dl.line([(-16.8, 80.0), (-16.7, 82.6)], SHADE["rim"], 0.9, 0.6)
        dl.line([(-31, 77.4), (-27.4, 78.2)], SHADE["rim"], 0.8, 0.5)                      # a shoulder
        # the Son beside him, smaller, his red cap turned to the window
        d.poly([(11, 71.0), (12, 74.2), (15.6, 75.8), (24, 75.8), (27.6, 74.2), (28.6, 71.0)], "#1a1526")
        d.oval(19.6, 77.6, 4.4, 4.8, "#1c1624")
        d.poly([(15.0, 78.4), (15.6, 81.6), (18.0, 83.2), (21.4, 83.2), (23.8, 81.6), (24.4, 78.4)], shade("#de4a33", 0.60))       # the cap
        d.poly([(23.6, 78.2), (30.4, 77.4), (30.6, 78.6), (24.0, 79.8)], shade("#a93224", 0.6))                                     # and its peak
        dl.line([(15.8, 81.2), (18.0, 83.2), (21.4, 83.2), (23.6, 81.4)], "#ff8e62", 1.2, 0.95)
        dl.line([(24.4, 79.6), (30.4, 78.6)], SHADE["rim"], 0.9, 0.85)
        dl.oval(19.7, 83.5, 0.8, 0.6, SHADE["fire"])                                         # the button on top
        # the steering wheel, in front of Dad
        dl.line([(-28.6, 76.6), (-26, 78.4), (-19, 78.4), (-16.4, 76.6)], "#0f0c18", 1.4)
    # things heaped in the back: a rolled sleeping bag, a grocery sack, the corner of a kite
    d.poly(rounded(-49, -34, 66.8, 73.6, 3.2), "#2a2a4c")
    dl.line([(-46.5, 73.2), (-36.5, 73.2)], "#5a5a8c", 0.9, 0.8)
    dl.line([(-41.6, 66.8), (-41.6, 73.4)], "#191830", 1.0)
    d.poly([(30.5, 66.8), (31.2, 75.0), (33.4, 76.0), (41.2, 75.6), (42.4, 66.8)], "#3a2c36")
    dl.line([(31.4, 75.0), (33.6, 76.0), (41.0, 75.6)], "#8a6a5c", 0.9, 0.85)
    d.poly([(44.6, 67), (50.6, 79.6), (52.8, 68.4)], "#5a2c4a")
    dl.line([(44.8, 67.2), (50.6, 79.6)], "#c06a70", 0.8, 0.8)
    # the glass itself: a slant of the sky behind us, the wires of the heater, a chrome frame
    d.poly([(-51, 67), (-41.5, 67), (-27.5, 89), (-36.5, 89)], GLASS_S["sheen"], 0.20)
    d.poly([(-37, 67), (-33.5, 67), (-19.5, 89), (-23, 89)], GLASS_S["sheen"], 0.14)
    for i in range(5):
        hv = 68.6 + i * 1.5
        dl.line([(-54.4 + i * 0.5, hv), (54.4 - i * 0.5, hv)], "#c8845c", 0.5, 0.26)
    dl.line(win + [win[0]], CHROME_S["road"], 1.2, 0.95)
    dl.line([(-47.4, 89.8), (47.4, 89.8)], CHROME_S["hot"], 0.8, 0.85)
    dl.line([(-56.2, 68), (-49.8, 88.2)], CHROME_S["pale"], 0.8, 0.6)
    dl.oval(40.5, 68.9, 2.6, 1.7, shade("#e8e0c4", 0.9))                                    # a parking sticker in the corner of the glass
    dl.oval(40.5, 68.9, 1.4, 0.9, shade("#5aa0d0", 0.9))

    # ---- the tailgate and the back ends of the wings
    d.poly([(-64, 22), (-65.2, 40), (-64.6, 56), (-62.5, 62), (62.5, 62), (64.6, 56), (65.2, 40), (64, 22)], SHADE["mid"])
    d.poly([(-64.4, 53), (-62.5, 62), (62.5, 62), (64.4, 53)], SHADE["hi"], 0.75)           # under the window it leans back and takes more sky
    d.poly([(-64, 22), (-64.8, 34), (64.8, 34), (64, 22)], SHADE["low"])                    # low down it turns under
    for sgn in (-1, 1):                                                                    # the shoulders of the wings: the sun reaches over them
        d.poly([(sgn * 56.5, 62), (sgn * 62.5, 62), (sgn * 64.2, 58.6), (sgn * 60, 60.6)], SHADE["roof"])
        dl.line([(sgn * 57, 62.1), (sgn * 62.6, 61.9), (sgn * 64.4, 58.4)], SHADE["fire"], 1.1, 0.95)
        dl.line([(sgn * 65.1, 36), (sgn * 65.2, 55)], SHADE["rim"], 0.9, 0.55)
    # wood across the tailgate: a pale frame round a darker panel, the same as down the sides
    d.poly([(-49, 33), (-49, 54), (49, 54), (49, 33)], WOOD_S["frame"])
    d.poly([(-45.4, 36.4), (-45.4, 50.8), (45.4, 50.8), (45.4, 36.4)], WOOD_S["field"])
    d.poly([(-45.4, 36.4), (-45.4, 41.5), (45.4, 41.5), (45.4, 36.4)], WOOD_S["dark"], 0.28)
    for i in range(7):                                                                    # the grain
        gv = 37.6 + i * 2.0
        dl.line([(-44, gv), (-12, gv + 0.5), (20, gv - 0.2), (44, gv + 0.2)], WOOD_S["grain"], 0.7, 0.5)
    for su in (-16.0, 16.0):                                                              # the frame's uprights
        d.rect(su - 1.8, su + 1.8, 33, 54, WOOD_S["frame"])
    dl.line([(-49, 54), (49, 54)], WOOD_S["frame_hi"], 0.9, 0.8)
    dl.line([(-49, 33), (49, 33)], WOOD_S["dark"], 0.9, 0.7)
    dl.line([(-45.4, 50.8), (45.4, 50.8)], WOOD_S["dark"], 0.7, 0.6)
    for sgn in (-1, 1):                                                                   # the wood on the wings comes round the corner
        d.poly([(sgn * 63.2, 33), (sgn * 64.9, 33), (sgn * 65.2, 40), (sgn * 64.7, 53), (sgn * 63.0, 53)], WOOD_S["frame"])
    # seams: the tailgate is a door
    for sgn in (-1, 1):
        dl.line([(sgn * 50.6, 31.5), (sgn * 50.6, 62)], SHADE["dark"], 1.0, 0.85)
    dl.line([(-62.4, 62.3), (62.4, 62.3)], CHROME_S["pale"], 1.1, 0.9)                      # the bright line under the glass
    dl.line([(-62.4, 61.5), (62.4, 61.5)], SHADE["dark"], 0.8, 0.7)
    # the handle, the maker's name in chrome that nobody can read at this distance, a sticker from somewhere
    d.rect(-7, 7, 55.6, 59.2, CHROME_S["road"])
    dl.line([(-6.6, 58.8), (6.6, 58.8)], CHROME_S["hot"], 0.8)
    dl.line([(-6.6, 56.0), (6.6, 56.0)], CHROME_S["line"], 0.8)
    dl.oval(0, 57.4, 1.0, 1.0, CHROME_S["line"])
    sq = [(28 + i * 1.6, 57.4 + (1.1 if i % 2 else -0.6) + (0.8 if i in (0, 5) else 0)) for i in range(10)]
    dl.line(sq, CHROME_S["pale"], 0.9, 0.9)
    dl.poly([(-44, 55.6), (-31, 55.9), (-31.2, 59.4), (-44.2, 59.1)], shade("#e8e0c4", 0.86))
    dl.poly([(-44, 55.6), (-31, 55.9), (-31.1, 57.2), (-44.1, 56.9)], shade("#5aa0d0", 0.9))
    dl.oval(-40.6, 58.2, 1.1, 0.9, shade("#e0584a", 0.95))
    # the tail lamps: lit, because it is dusk. A chrome frame, three lenses, the lowest one white.
    for sgn in (-1, 1):
        a, b = sgn * 51.8, sgn * 62.6
        lo, hi = min(a, b), max(a, b)
        d.poly(rounded(lo, hi, 35.4, 59.6, 1.6), CHROME_S["road"])
        d.rect(lo + 1.1, hi - 1.1, 43.4, 58.4, "#e2301f")
        d.rect(lo + 2.0, hi - 2.0, 45.0, 57.0, "#ff5a34")
        d.rect(lo + 3.2, hi - 3.2, 47.4, 55.0, "#ff9a5c")
        d.rect(lo + 1.1, hi - 1.1, 36.6, 42.2, shade("#f4ecd8", 0.72))
        dl.line([(lo + 1.1, 50.9), (hi - 1.1, 50.9)], "#8a1c18", 0.8, 0.9)
        dl.line([(lo + 1.1, 42.8), (hi - 1.1, 42.8)], CHROME_S["line"], 0.9)
        dl.line([(lo + 0.6, 59.7), (hi - 0.6, 59.7)], CHROME_S["hot"], 0.8, 0.9)
        dl.oval((lo + hi) / 2, 51.4, 1.3, 2.0, "#ffe0a0", 0.95)

    # ---- the bumper: chrome, so it shows the road below and the dusk behind us, with a hard line between
    d.poly(rounded(-67.5, 67.5, 19.6, 31.4, 3.4), CHROME_S["road"])
    d.poly([(-66.6, 25.8), (66.6, 25.8), (66.9, 30.4), (-66.9, 30.4)], CHROME_S["sky"])
    d.poly([(-66.6, 25.8), (66.6, 25.8), (66.8, 27.6), (-66.8, 27.6)], CHROME_S["pale"])
    for sgn in (-1, 1):                                                                   # the lamps redden the chrome under them
        d.poly([(sgn * 50, 27.6), (sgn * 64.5, 27.6), (sgn * 65.5, 30.4), (sgn * 49, 30.4)], "#e8604a", 0.55)
    dl.line([(-67, 25.5), (67, 25.5)], CHROME_S["line"], 1.1)
    dl.line([(-66.4, 31.2), (66.4, 31.2)], CHROME_S["hot"], 1.0)                            # its top edge looks up at the glow
    dl.line([(-66.6, 20.2), (66.6, 20.2)], CHROME_S["line"], 0.9, 0.8)
    for sgn in (-1, 1):                                                                   # the over-riders, with their rubber faces
        d.poly(rounded(sgn * 19 - 3.3, sgn * 19 + 3.3, 18.6, 35.8, 1.8), CHROME_S["pale"])
        d.rect(sgn * 19 - 1.5, sgn * 19 + 1.5, 20.8, 33.6, "#231d2a")
        dl.line([(sgn * 19 - 2.8, 35.4), (sgn * 19 + 2.8, 35.4)], CHROME_S["hot"], 0.9)
        dl.line([(sgn * 19 + 3.2, 19.4), (sgn * 19 + 3.2, 34.8)], CHROME_S["line"], 0.8, 0.8)
        dl.line([(sgn * 67.2, 22), (sgn * 67.4, 29.5)], SHADE["rim"], 1.0, 0.8)
    # the number plate between them: something was written on it once
    d.rect(-12.4, 12.4, 20.9, 30.3, CHROME_S["line"])
    d.rect(-11.6, 11.6, 21.6, 29.6, shade("#f4efdc", 0.80))
    sq = [(-8.6, 24.2), (-7.2, 27.4), (-5.6, 24.4), (-4.0, 27.2), (-2.4, 24.6), (-0.6, 27.4), (1.2, 24.4), (3.0, 27.0), (4.6, 24.6), (6.4, 27.4), (8.2, 24.6)]
    dl.line(sq, "#3c3654", 1.3, 0.9)
    dl.line([(-9.8, 22.6), (9.8, 22.6)], "#8a5a4a", 0.7, 0.7)
    dl.rect(7.6, 10.4, 27.4, 29.0, shade("#e0584a", 0.9))
    dl.line([(-11.6, 29.6), (11.6, 29.6)], "#fff6e2", 0.7, 0.7)
    # a sticker on the bumper, too: a holiday, years ago
    dl.poly([(-54, 21.6), (-33, 21.8), (-33.2, 25.0), (-54.2, 24.8)], shade("#f0e6c8", 0.82))
    dl.poly([(-54, 21.6), (-46, 21.7), (-46.2, 24.9), (-54.2, 24.8)], shade("#e0584a", 0.9))
    dl.line([(-44.4, 23.3), (-35, 23.4)], "#4a6a8a", 0.9, 0.85)


def sheets(aboard=True, seed=4):
    """Paint the parts once each. -> a dict of (color, alpha) pairs on the common sheet."""
    out = {}
    for name, draw in (("gear", lambda b, l: running_gear(b, l)), ("body", lambda b, l: body(b, l, aboard))):
        base, lines = Paper(SHEET), Paper(SHEET)
        draw(base, lines)
        color, alpha = base.done()
        lc, la = lines.done()
        flat = np.empty(SHEET + (3,), dtype=F32)
        flat[...] = rgb("#6a4a52") if name == "body" else rgb("#241a28")           # what the brush picks up at the edges
        over(flat, color, alpha)
        painted = strokes(flat, sizes=(7, 4, 2), seed=seed, density=1.8, jitter=0.03, keep=0.45)
        over(painted, lc, la)
        out[name] = (grade(painted), np.clip(np.maximum(alpha, la), 0, 1))           # the same last glaze as the picture it drives through
    out["shadow"] = ground_shadow(SHEET)
    return out


def layers(aboard=True, seed=4):
    """The cut-out as the layers it is made of, back to front: (name, color, hard alpha, which frames, rides on the springs)."""
    parts = sheets(aboard, seed)
    out = [("shadow",) + parts["shadow"] + ((0, 1), False), ("gear",) + parts["gear"] + ((0, 1), False), ("body",) + parts["body"] + ((0, 1), True)]
    for f in (0, 1):
        out.append((f"dust{f}",) + dust(SHEET, f) + ((f,), False))
    return [(n, c, (a > 0.5).astype(F32), fr, rides) for n, c, a, fr, rides in out]


def box_of(made):
    both = np.maximum(made[0], made[1])
    ys, xs = np.where(both > 0.5)
    return xs.min() - 1, xs.max() + 2, ys.min() - 1, ys.max() + 2


def frames(aboard=True, seed=4, parts=None):
    """-> ([frame 0, frame 1] as (color, alpha) cropped to one common box, foot (x, y) in that box)."""
    parts = parts or layers(aboard, seed)
    made = []
    for f in (0, 1):
        pic = np.zeros(SHEET + (3,), dtype=F32)
        alpha = np.zeros(SHEET, dtype=F32)
        for name, c, a, fr, rides in parts:
            if f not in fr:
                continue
            if rides and f:
                c, a = np.roll(c, DROP, axis=0), np.roll(a, DROP, axis=0)          # the body sits down on its springs
            over(pic, c, a)
            alpha = np.maximum(alpha, a)
        made.append((pic, alpha))
    x0, x1, y0, y1 = box_of([m[1] for m in made])
    foot = (float(ORIGIN[0] - x0), float(ORIGIN[1] - y0))
    return [(p[y0:y1, x0:x1], a[y0:y1, x0:x1]) for p, a in made], foot


def write(names, colors=96, parts=None, seed=7, speckle=0.012, amount=0.016):
    """Write the two frames as palette PNGs. Each layer is given its grain and its palette colors ONCE and
    the frames are then put together from those, so the body is the very same pixels in both frames,
    3 px apart, and nothing shimmers but the dust. -> (foot, (width, height), file sizes)"""
    import os
    parts = parts or layers()
    grained = [(n, grain(c, seed + i, amount), a, fr, rides) for i, (n, c, a, fr, rides) in enumerate(parts)]
    pal = palette_of([g[a > 0.5].reshape(-1, 1, 3) for n, g, a, fr, rides in grained], colors=colors)
    index = [(n, to_palette(g, pal, seed=5 + i, speckle=speckle), a, fr, rides) for i, (n, g, a, fr, rides) in enumerate(grained)]
    made = []
    for f in (0, 1):
        idx = np.zeros(SHEET, dtype=np.uint8)
        alpha = np.zeros(SHEET, dtype=F32)
        for n, ix, a, fr, rides in index:
            if f not in fr:
                continue
            if rides and f:
                ix, a = np.roll(ix, DROP, axis=0), np.roll(a, DROP, axis=0)
            idx = np.where(a > 0.5, ix, idx)
            alpha = np.maximum(alpha, a)
        made.append((idx, alpha))
    x0, x1, y0, y1 = box_of([m[1] for m in made])
    sizes = []
    for (idx, alpha), name in zip(made, names):
        save(name, np.ascontiguousarray(idx[y0:y1, x0:x1]), pal, alpha[y0:y1, x0:x1])
        sizes.append(os.path.getsize(name))
    return (float(ORIGIN[0] - x0), float(ORIGIN[1] - y0)), (int(x1 - x0), int(y1 - y0)), sizes


if __name__ == "__main__":
    import sys, time
    from PIL import Image
    t0 = time.time()
    fr, foot = frames()
    print("painted", round(time.time() - t0, 1), fr[0][0].shape, "foot", foot)
    h, w = fr[0][1].shape
    bg = np.empty((h + 40, w * 2 + 60, 3), dtype=F32)
    bg[...] = rgb("#7c7090")
    bg[:, : w + 30] = rgb("#8a7a94")
    for i, (c, a) in enumerate(fr):
        view = bg[20:20 + h, 20 + i * (w + 20):20 + i * (w + 20) + w]
        over(view, c, a)
    Image.fromarray((np.clip(bg, 0, 1) * 255).astype(np.uint8)).save("out/highway-wagon-try.png")
    small = Image.fromarray((np.clip(bg[:, : w + 30], 0, 1) * 255).astype(np.uint8)).resize(((w + 30) // 5, (h + 40) // 5), Image.LANCZOS)
    small.save("out/highway-wagon-fifth.png")
    print("ok")

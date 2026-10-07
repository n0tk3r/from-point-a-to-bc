"""Solid things drawn in their own measurements: x along the thing, y UP from the ground, z away from us.
Depth is shown the way a draughtsman's cabinet drawing shows it: the far side is the near side moved
up and to the right. That keeps every side face true to shape, which is what a painted prop wants."""

import math

import numpy as np

from brush import F32, Sheet, lerp, rgb


def mix(a, b, t):
    a = rgb(a) if isinstance(a, str) else np.asarray(a, dtype=F32)
    b = rgb(b) if isinstance(b, str) else np.asarray(b, dtype=F32)
    return lerp(a, b, t)


class Draft:
    def __init__(self, sheet, origin, scale=1.0, tilt=0.0, pivot=(0.0, 0.0), depth=(0.50, 0.30)):
        """`origin` is where the thing's (0, 0, 0) lands on the sheet. `tilt` turns it about `pivot`
        (degrees; positive drops the low-x end). `depth` is how far one unit of z moves right and up."""
        self.s, self.o, self.k = sheet, origin, scale
        self.ca, self.sa = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
        self.pv, self.dz = pivot, depth

    def pt(self, x, y, z=0.0):
        dx, dy = x - self.pv[0], y - self.pv[1]
        X = self.pv[0] + dx * self.ca - dy * self.sa
        Y = self.pv[1] + dx * self.sa + dy * self.ca
        return (self.o[0] + (X + z * self.dz[0]) * self.k, self.o[1] - (Y + z * self.dz[1]) * self.k)

    def pts(self, points, z=0.0):
        return [self.pt(p[0], p[1], p[2] if len(p) > 2 else z) for p in points]

    def poly(self, points, color, alpha=1.0, z=0.0):
        self.s.poly(self.pts(points, z), color, alpha)
        return self

    def line(self, points, color, width=1.0, alpha=1.0, z=0.0):
        self.s.line(self.pts(points, z), color, width * self.k, alpha)
        return self

    def disc(self, x, y, r, color, alpha=1.0, z=0.0, squash=1.0, n=28):
        self.poly([(x + math.cos(i / n * 2 * math.pi) * r * squash, y + math.sin(i / n * 2 * math.pi) * r) for i in range(n)], color, alpha, z)
        return self

    def arc(self, x, y, r, a0, a1, n=14):
        """Points round part of a circle, angles in degrees, counter-clockwise from the right."""
        return [(x + math.cos(math.radians(lerp(a0, a1, i / n))) * r, y + math.sin(math.radians(lerp(a0, a1, i / n))) * r) for i in range(n + 1)]

    def side(self, points, z0, z1, color, alpha=1.0):
        """The band that joins a line at depth z0 to the same line at depth z1 (a top, an end, a lid)."""
        a = [(p[0], p[1], z0) for p in points]
        b = [(p[0], p[1], z1) for p in reversed(points)]
        self.poly(a + b, color, alpha)
        return self

    def box(self, x0, x1, y0, y1, z0, z1, front, top, end, alpha=1.0):
        """A box: its near face, its top, and whichever end the depth lets us see."""
        xe = x0 if self.dz[0] < 0 else x1
        self.poly([(xe, y0, z0), (xe, y0, z1), (xe, y1, z1), (xe, y1, z0)], end, alpha)
        self.poly([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], top, alpha)
        self.poly([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], front, alpha)
        return self

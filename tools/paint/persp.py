"""Rooms and streets in true perspective. A Camera turns places in the world into places in the picture,
so floors, walls and furniture all run to the same vanishing point.

World measurements are in centimetres: x to the right, y UP from the floor, z away from us (z = 0 is
where the picture's bottom edge meets the floor, roughly). A grown-up is about 175 tall."""

import math

import numpy as np

from brush import F32, Sheet, grid, lerp, rgb


class Camera:
    def __init__(self, horizon, full, vanish_x=400.0, focal=800.0, adult=160.0, size=(800, 600)):
        """The camera a scene is seen through, worked out from the two numbers the game uses for depth:
        `horizon` (the picture row the floor runs back to) and `full` (the row where a grown-up, 175 cm,
        is drawn `adult` pixels tall). People drawn by the game then match what is painted here.
        `focal` is the lens in pixels: 800 is a normal lens; smaller is wider and makes depth steeper."""
        self.w, self.h = size
        self.vx, self.vy, self.full, self.F = float(vanish_x), float(horizon), float(full), float(focal)
        self.s0 = adult / 175.0                             # pixels per cm at the `full` row
        self.eye = (self.full - self.vy) / self.s0          # how high the lens is above the floor, cm
        self.Z0 = self.F / self.s0                          # how far the lens is from the floor at the `full` row, cm

    def pt(self, x, y, z):
        """World (x across from the middle, y up, z away from the `full` row) -> picture (x, y)."""
        k = self.F / (self.Z0 + z)
        return (self.vx + x * k, self.vy + (self.eye - y) * k)

    def scale(self, z):
        """Picture pixels per centimetre at depth z."""
        return self.F / (self.Z0 + z)

    def depth_at(self, row):
        """How far away (z) the floor is at a picture row below the horizon."""
        return self.eye * self.F / max(row - self.vy, 1e-3) - self.Z0

    def x_at(self, col, row):
        """The world x of a place on the floor, given where it is in the picture."""
        return (col - self.vx) / self.scale(self.depth_at(row))

    def quad(self, sheet, pts, color, alpha=1.0):
        sheet.poly([self.pt(*p) for p in pts], color, alpha)

    def line(self, sheet, pts, color, width=1.0, alpha=1.0):
        sheet.line([self.pt(*p) for p in pts], color, width, alpha)

    def box(self, sheet, x0, x1, y0, y1, z0, z1, front, top, side, alpha=1.0):
        """A box standing in the room. Draws the faces we can see: the top if it is below the eye, whichever
        side faces the middle of the picture, and the front (z0). `side` may be (left color, right color)."""
        left, right = side if isinstance(side, (tuple, list)) else (side, side)
        if x0 > 0:
            self.quad(sheet, [(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)], left, alpha)
        if x1 < 0:
            self.quad(sheet, [(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)], right, alpha)
        if y1 < self.eye:
            self.quad(sheet, [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], top, alpha)
        self.quad(sheet, [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], front, alpha)

    def floor_grid(self, shape):
        """For every pixel below the horizon: where on the floor it is. -> (x in cm, z in cm, mask)."""
        px, py = grid(shape)
        below = py > self.vy + 0.5
        Z = self.eye * self.F / np.maximum(py - self.vy, 0.5)
        return ((px - self.vx) * Z / self.F).astype(F32), (Z - self.Z0).astype(F32), below.astype(F32)


def tiles(cam, shape, size=(60, 60), seed=0, gap=0.035, jitter=0.06):
    """A paved floor seen in perspective: -> (which-tile noise 0..1, joint mask), to tint a floor with.
    `size` is a tile's width and depth in cm."""
    x, z, below = cam.floor_grid(shape)
    u, v = x / size[0], z / size[1]
    iu, iv = np.floor(u), np.floor(v)
    fu, fv = u - iu, v - iv
    h = np.sin(iu * 127.1 + iv * 311.7 + seed) * 43758.5453
    tone = (h - np.floor(h)).astype(F32)
    edge = np.minimum(np.minimum(fu, 1 - fu) * size[0], np.minimum(fv, 1 - fv) * size[1])      # cm to the nearest joint
    width = gap * min(size) * (cam.scale(0) / np.maximum(cam.F / (cam.Z0 + z), 1e-3)) ** 0.5       # far joints fatten so they do not flicker
    joint = np.clip(1 - edge / np.maximum(width, 1e-3), 0, 1) * below
    return tone * below, joint.astype(F32)

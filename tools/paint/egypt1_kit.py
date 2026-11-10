"""Where the wagon came down (egypt1.py): the scene's own measures and tools for depth (round twenty-three: DEPTH.md).

One camera for everything, small things and shadows included: `persp.Camera(262, 590)`, the scene file's own two
numbers behind a normal lens. The eye is 3.59 m above the sand. The sand at the picture's bottom edge is 8.5 m from the
lens, the near palm's foot 20.8 m, the far palm's 51 m. A ground place is (X, Z) in centimetres: X to the right of the
lens's axis, Z away from the row `full` (the Camera's own z: a thing nearer than the bottom edge has Z under -26).

The sun is on the left and a little beyond the picture. A thing h tall throws its shadow 0.70 h to the right and 0.48 h
toward us: measured from the first painting, where the middle of the near palm's crown falls on the place Lot sits
(the scene file seats him in that shade). Every shadow new in round twenty-three is laid with those two numbers
through the camera, so near shadows slant more than far ones."""

import numpy as np

from brush import F32, noise, rgb, sample
from persp import Camera

W, H = 800, 600
HZ, FULL = 262, 590
CAM = Camera(HZ, FULL)
SUN = (0.70, -0.476)                                         # a shadow's run for each cm of height: across, away


def pt(X, Z, Y=0.0):
    """The picture point of a ground place (or of a point Y cm above it)."""
    return CAM.pt(X, Y, Z)


def k_at(X, Z):
    """Picture pixels to a centimetre there."""
    return CAM.scale(Z)


def place(x, y):
    """The ground place under a picture point below the horizon. -> (X, Z)"""
    Z = CAM.depth_at(y)
    return (x - CAM.vx) / CAM.scale(Z), Z


def ground(shape=(H, W)):
    """For every pixel: the ground place it shows. -> (X, Z, below the horizon)"""
    return CAM.floor_grid(shape)


_TILES = {}


def field(X, Z, cell, seed, octaves=3, size=768):
    """Cloudy noise that lies on the ground, 0 to 1: `cell` is the size of its largest blobs in cm (a number, or
    (across, away) for blobs drawn out along the wind). After thirty-two blobs it runs back the other way, which
    nobody sees in sand."""
    cx, cz = (cell, cell) if np.isscalar(cell) else cell
    px = 24.0                                                # a blob is this many pixels of the tile
    key = (seed, octaves, size)
    if key not in _TILES:
        _TILES[key] = noise((size, size), px, seed, octaves)
    tile = _TILES[key]
    span = size - 2.0
    fold = lambda t: span - np.abs((t % (2 * span)) - span)   # back and forth across the tile: no seam where it starts again
    return sample(tile, fold(X / cx * px + span * 0.37), fold(Z / cz * px + span * 0.11))


def stone_shadow(picture, x, y, rx, ry, amount=0.42, color="#6a5884", ground_mask=None):
    """A stone's shadow: to the right and a little toward us, as every shadow here. (Worked in its own corner of the
    picture: there are hundreds.)"""
    cx, cy, ax, ay = x + rx * 0.95, y + ry * 0.16, rx * 1.25, max(1.1, ry * 0.46)
    x0, x1 = int(max(0, cx - ax - 2)), int(min(picture.shape[1], cx + ax + 3))
    y0, y1 = int(max(0, cy - ay - 2)), int(min(picture.shape[0], cy + ay + 3))
    if x1 <= x0 or y1 <= y0:
        return picture
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(F32)
    d = np.sqrt(((xx + 0.5 - cx) / ax) ** 2 + ((yy + 0.5 - cy) / ay) ** 2)
    m = np.clip((1 - d) * min(ax, ay) * 0.8 + 0.5, 0, 1) * amount
    if ground_mask is not None:
        m = m * ground_mask[y0:y1, x0:x1]
    c = rgb(color)
    part = picture[y0:y1, x0:x1]
    part[...] = part * (1 - m[..., None]) + part * c * m[..., None]
    return picture


def cracks(X, Z, cell=22.0, seed=7):
    """Dried mud by the river, cracked into plates: for every ground place, how near it is to a crack (1 on the crack,
    0 in the middle of a plate) and a number 0 to 1 for the plate it is on. Plates are about `cell` cm across."""
    gx, gz = np.floor(X / cell), np.floor(Z / cell)
    best = np.full(X.shape, 1e9, dtype=F32)
    second = np.full(X.shape, 1e9, dtype=F32)
    tone = np.zeros(X.shape, dtype=F32)
    for dj in (-1, 0, 1):
        for di in (-1, 0, 1):
            cx, cz = gx + di, gz + dj
            h1 = np.sin(cx * 127.1 + cz * 311.7 + seed) * 43758.5453
            h2 = np.sin(cx * 269.5 + cz * 183.3 + seed * 1.7) * 43758.5453
            px = (cx + 0.5 + 0.72 * ((h1 - np.floor(h1)) - 0.5)) * cell
            pz = (cz + 0.5 + 0.72 * ((h2 - np.floor(h2)) - 0.5)) * cell
            d = np.hypot(X - px, Z - pz).astype(F32)
            nearer = d < best
            second = np.where(nearer, best, np.minimum(second, d))
            tone = np.where(nearer, (h1 - np.floor(h1)).astype(F32), tone)
            best = np.where(nearer, d, best)
    return np.clip(1 - (second - best) / (cell * 0.10), 0, 1).astype(F32), tone

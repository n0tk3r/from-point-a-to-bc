"""Tools for painting across the Tiber (rome_tiber.py): the scene's planes as its camera sees them, pixel by pixel,
the morning light and the shadows things throw in it, and the surfaces (plaster, stone, earth, water).

World measurements are centimetres (rome_tiber_model.py): x across, y up from the lane, z away. A wall is any upright
plane, given by a point on its foot and a direction along it (in plan); `wall()` says, for every pixel that looks at
it, where on it that pixel lands (s along it, h up it) and how far off it is. Shadows are worked out by sending a ray
from each place toward the sun past simple solids (boxes in a building's own frame, cylinders), as rome_steps_kit's
`sunless` does for the temple."""

import math

import numpy as np

from brush import F32, blur, grid, lerp, mask_poly, noise, over, ramp, rgb, sample, smooth, step, tint
from rome_steps_kit import Light, col, hash2, mix, sunless, tex, unit
from rome_street_kit import Sheet2, cells, wn
import rome_tiber_model as M

W, H = M.W, M.H
SHAPE = (H, W)
_gx, _gy = grid(SHAPE)
PX, PY = _gx + 0.5, _gy + 0.5                                 # the middle of every pixel
DX = (PX - M.VX) / M.F                                       # the ray through each pixel, per cm of depth (Z = Z0 + z)
DY = (PY - M.HZ) / M.F

LIGHT = Light(M.SUN, sun=(1.10, 1.0, 0.80), shade=(0.50, 0.56, 0.88), bounce=(0.28, 0.17, 0.05))


def P(x, y, z):
    return M.P(x, y, z)


def Q(points3):
    return [M.P(*p) for p in points3]


# ---------------------------------------------------------------- planes, per pixel
def level(y0):
    """The level plane at height y0. -> (x, z, k (px per cm), ok: the pixels that see it, in front of the lens)."""
    with np.errstate(divide="ignore", invalid="ignore"):
        Z = (M.EYE - y0) / np.where(np.abs(DY) < 1e-7, 1e-7, DY)
    ok = (Z > 1.0) & (Z < 4e6)
    Z = np.where(ok, Z, 4e6)
    return (DX * Z).astype(F32), (Z - M.Z0).astype(F32), (M.F / Z).astype(F32), ok


def wall(p0, d):
    """The upright plane through plan point p0 = (x, z), running along the plan direction d = (dx, dz) (a unit
    vector). -> (s: cm along it from p0, h: height, Z: depth from the lens, k: px per cm, ok)."""
    nx, nz = d[1], -d[0]
    den = DX * nx + nz
    with np.errstate(divide="ignore", invalid="ignore"):
        Z = (p0[0] * nx + (M.Z0 + p0[1]) * nz) / np.where(np.abs(den) < 1e-7, 1e-7, den)
    ok = (Z > 1.0) & (Z < 4e6)
    Z = np.where(ok, Z, 4e6)
    x, z = DX * Z, Z - M.Z0
    s = (x - p0[0]) * d[0] + (z - p0[1]) * d[1]
    h = M.EYE - DY * Z
    return s.astype(F32), h.astype(F32), Z.astype(F32), (M.F / Z).astype(F32), ok


def front(s0=None):
    """The front of the two near houses (the line through FRONT0 along D): (s, h, Z, k, ok)."""
    return wall(M.FRONT0, M.D)


def world_of_front(s, h, d=0.0):
    """A place on (or d cm out from) the front: -> (x, y, z)."""
    x, z = M.out(M.along(s), d)
    return (x, h, z)


def front_pt(s, h, d=0.0):
    return M.P(*world_of_front(s, h, d))


def front_poly(pts, d=0.0):
    """Picture points of a shape given as (s, h) on the front (or d cm out from it)."""
    return [front_pt(s, h, d) for s, h in pts]


def band(v, lo, hi, px=1.0):
    return (np.clip((v - lo) / px + 0.5, 0, 1) * np.clip((hi - v) / px + 0.5, 0, 1)).astype(F32)


# ---------------------------------------------------------------- the building's own frame, for shadows
def to_front_frame(x, z):
    """World plan -> the front's frame: u along it (= s), v back into the houses (away from the square)."""
    rx, rz = x - M.FRONT0[0], z - M.FRONT0[1]
    return (rx * M.D[0] + rz * M.D[1]).astype(F32) if np.ndim(rx) else rx * M.D[0] + rz * M.D[1], \
           (-(rx * M.N[0] + rz * M.N[1])).astype(F32) if np.ndim(rx) else -(rx * M.N[0] + rz * M.N[1])


SUN_FRONT = (M.SUN[0] * M.D[0] + M.SUN[2] * M.D[1], -(M.SUN[0] * M.N[0] + M.SUN[2] * M.N[1]), M.SUN[1])   # (along, into, up)
SUN_WORLD = (M.SUN[0], M.SUN[2], M.SUN[1])                                                             # (x, z, up)


def shade_front(x, y, z, solids, spread=0.012):
    """Sun cut off at world places (x, y, z) by solids given in the front's frame (u, v, h)."""
    u, v = to_front_frame(x, z)
    return sunless(solids, u, v, y, SUN_FRONT, spread=spread)


def shade_world(x, y, z, solids, spread=0.012):
    """...by solids given in world plan coordinates (x, z, y): boxes ("box", x0, x1, z0, z1, y0, y1), cylinders."""
    return sunless(solids, x, z, y, SUN_WORLD, spread=spread)


def facing(nx, ny, nz):
    """How squarely a surface with this normal (world) faces the sun, 0 to 1."""
    return max(0.0, nx * M.SUN[0] + ny * M.SUN[1] + nz * M.SUN[2])


FACE_FRONT = facing(M.N[0], 0.0, M.N[1])                     # the near houses' fronts: lit at a slant
FACE_ROAD = facing(-1.0, 0.0, 0.0)                           # the fronts along the road, facing the river
FACE_US = facing(0.0, 0.0, -1.0)                             # anything facing straight at us: in shade
FACE_UP = facing(0.0, 1.0, 0.0)                              # the ground


# ---------------------------------------------------------------- air
def far(color, z, tint_to="#c8d2e4", reach=9000.0, most=0.78):
    """Things pale toward the morning haze with distance (z in cm, a number or a picture)."""
    t = np.clip(1 - np.exp(-np.maximum(z, 0) / reach), 0, most)
    c = col(color) if isinstance(color, str) else color
    return lerp(c, col(tint_to), t[..., None] if np.ndim(t) else t)


# ---------------------------------------------------------------- surfaces
def plaster(u, y, base, seed, patch=0.10, streak=0.05, mend=0.0):
    """A plastered wall in its own measurements (u along, y up, cm): uneven washes, runs of dirt, warmer and cooler
    places, and (with `mend`) squarish patches made good with newer, paler plaster. (After the street's.)"""
    c = np.empty(u.shape + (3,), dtype=F32)
    c[...] = col(base)
    big = wn(u, y, 190, seed, 4) - 0.5
    mid = wn(u, y, 46, seed + 1, 3) - 0.5
    run = wn(u * 5.0, y, 170, seed + 2, 3) - 0.5
    c *= (1 + big * 2.6 * patch + mid * patch * 1.1 + run * 2 * streak)[..., None]
    k = (wn(u, y, 260, seed + 3, 3) - 0.5) * 0.09
    c[..., 0] += k
    c[..., 2] -= k
    if mend:
        gu, gv = np.floor(u / 150.0), np.floor(y / 110.0)
        pick = hash2(gu, gv, seed + 5) < mend
        fu, fv = u / 150.0 - gu, y / 110.0 - gv
        a0, a1, b0, b1 = (0.10 + 0.25 * hash2(gu, gv, seed + q) for q in (6, 7, 8, 9))
        inside = (fu > a0) & (fu < 1 - a1) & (fv > b0) & (fv < 1 - b1) & pick
        soft = step(0.30, 0.42, wn(u, y, 22, seed + 4, 3))
        c = lerp(c, np.clip(c * 1.10 + 0.03, 0, 1), (inside * soft * 0.8)[..., None])
    return np.clip(c, 0, 1).astype(F32)


def bare(u, y, seed, much=0.5, cell=120.0):
    """Where the plaster has fallen and the wall shows through: ragged patches (0 to 1)."""
    n = wn(u, y, cell, seed, 4) + (wn(u, y, cell * 0.2, seed + 1, 3) - 0.5) * 0.3
    return step(1.0 - much * 0.42, 1.03 - much * 0.42, n)


def tufa_blocks(u, y, ppc, seed, base="#c9b48e", long=62.0, high=31.0):
    """The squared tufa of a wall where the plaster has gone (or the landing's stone), in courses."""
    tone, jm, above = _courses(u, y, long, high, seed, ppc)
    c = col(base)[None, None, :] * (0.84 + 0.30 * tone[..., None])
    c = c * (1 - 0.45 * jm[..., None]) + col("#6f5c50") * 0.45 * jm[..., None]
    return np.clip(c, 0, 1).astype(F32), jm


def _courses(u, y, long, high, seed, ppc):
    from rome_steps_kit import courses
    return courses(u, y, long, high, seed, 1.4, ppc)


def tiles(u, v, ppc, seed, base="#c8643e"):
    """A roof of Roman tiles seen from below its eave or on its slope: flat tiles with round cover tiles over the
    joints, in rows down the slope. `u` runs along the eave, `v` up the slope (cm). -> (color, mask of the cover tiles)."""
    pitch = 40.0                                                         # one row of cover tiles every 40 cm along the eave
    fu = (u / pitch) % 1.0
    row = np.floor(v / 48.0)
    cover = np.clip(1 - np.abs(fu - 0.5) / 0.16, 0, 1)                   # the round cover tile over each joint
    tone = hash2(np.floor(u / pitch), row, seed)
    c = col(base)[None, None, :] * (0.82 + 0.30 * tone[..., None])
    lip = np.clip(1 - np.abs((v / 48.0) % 1.0 - 0.04) / 0.06, 0, 1)      # the lower edge of each row of tiles
    c = c * (1 - 0.22 * lip[..., None])
    c = lerp(c, c * 1.18 + 0.02, (cover * 0.9)[..., None])
    side = np.clip((fu - 0.5) / 0.16, -1, 1) * cover                      # the cover tile is round: lit on one side
    c = c * (1 + 0.12 * side[..., None])
    fade = np.clip(ppc * pitch / 6.0, 0, 1)[..., None]                    # far off the rows run together
    c = lerp(col(base)[None, None, :] * 0.95, c, fade)
    return np.clip(c, 0, 1).astype(F32), (cover * fade[..., 0]).astype(F32)


def earth(x, z, k, seed):
    """The beaten earth of the lane: dust, grit, wheel and foot wear, a few old stones. -> local color."""
    c = np.empty(x.shape + (3,), dtype=F32)
    c[...] = col("#b9a68a")
    big = wn(x, z * 0.8, 260, seed, 4) - 0.5
    mid = wn(x, z, 60, seed + 1, 3) - 0.5
    fine = wn(x, z, 14, seed + 2, 2) - 0.5
    seen = np.clip(k / 0.25, 0, 1)                                       # far off the grit runs together
    c *= (1 + big * 0.22 + mid * 0.12 + fine * 0.10 * seen)[..., None]
    warm = (wn(x, z, 330, seed + 3, 3) - 0.5) * 0.08
    c[..., 0] += warm
    c[..., 2] -= warm * 1.2
    return np.clip(c, 0, 1).astype(F32)


# ---------------------------------------------------------------- fronts and roofs in a building's own frame
def frame_of(origin, d):
    """A building's frame: its front runs along d (plan) through origin; `out` points from its front to the street."""
    out_ = (-d[1], d[0])
    return dict(o=origin, d=d, out=out_)


def in_frame(fr, x, z):
    """World plan -> (u along the front, v back into the building from its front)."""
    rx, rz = x - fr["o"][0], z - fr["o"][1]
    return rx * fr["d"][0] + rz * fr["d"][1], -(rx * fr["out"][0] + rz * fr["out"][1])


def from_frame(fr, u, v, h):
    """(u, v, h) in a building's frame -> world (x, y, z)."""
    x = fr["o"][0] + u * fr["d"][0] - v * fr["out"][0]
    z = fr["o"][1] + u * fr["d"][1] - v * fr["out"][1]
    return (x, h, z)


def fpt(fr, u, v, h):
    return M.P(*from_frame(fr, u, v, h))


def fpoly(fr, pts):
    """Picture points of a shape given as (u, v, h) in a building's frame."""
    return [fpt(fr, *p) for p in pts]


def sun_in(fr):
    """The direction to the sun in a building's frame: (along u, along v, up)."""
    return (M.SUN[0] * fr["d"][0] + M.SUN[2] * fr["d"][1], -(M.SUN[0] * fr["out"][0] + M.SUN[2] * fr["out"][1]), M.SUN[1])


def shade_in(fr, x, y, z, solids, spread=0.012):
    """Sun cut off at world places by solids given in a building's frame (u, v, h)."""
    u, v = in_frame(fr, x, z)
    return sunless(solids, np.asarray(u, dtype=F32), np.asarray(v, dtype=F32), y, sun_in(fr), spread=spread)


def plane_at(fr, v0):
    """The upright plane parallel to a building's front, v0 cm back from it (negative: out in front). -> (u, h, Z, k, ok)."""
    o = from_frame(fr, 0.0, v0, 0.0)
    s, h, Z, k, ok = wall((o[0], o[2]), fr["d"])
    return s, h, Z, k, ok


def side_at(fr, u0):
    """The upright plane square to the front at u = u0 (a building's end wall). -> (v back from the front, h, Z, k, ok)."""
    o = from_frame(fr, u0, 0.0, 0.0)
    back = (-fr["out"][0], -fr["out"][1])
    s, h, Z, k, ok = wall((o[0], o[2]), back)
    return s, h, Z, k, ok


def roof_at(fr, eave, v0, pitch):
    """A roof rising back from its eave (height `eave`, at v = v0, which is negative where the eave stands out over the
    street) at `pitch` degrees. -> (u, v, h, Z, k, ok) for every pixel that looks at that sloping plane."""
    t = math.tan(math.radians(pitch))
    ox, oz = fr["o"]
    a_v = -(DX * fr["out"][0] + fr["out"][1])
    b_v = ox * fr["out"][0] + (M.Z0 + oz) * fr["out"][1]
    den = DY + a_v * t
    with np.errstate(divide="ignore", invalid="ignore"):
        Z = (M.EYE - eave - (b_v - v0) * t) / np.where(np.abs(den) < 1e-7, 1e-7, den)
    ok = (Z > 1.0) & (Z < 4e6)
    Z = np.where(ok, Z, 4e6)
    x, z = DX * Z, Z - M.Z0
    u, v = in_frame(fr, x, z)
    h = M.EYE - DY * Z
    return u.astype(F32), v.astype(F32), h.astype(F32), Z.astype(F32), (M.F / Z).astype(F32), ok


def level_in(fr, y0):
    """A level plane at height y0, in a building's frame. -> (u, v, Z, k, ok)."""
    x, z, k, ok = level(y0)
    u, v = in_frame(fr, x, z)
    return u.astype(F32), v.astype(F32), (z + M.Z0).astype(F32), k, ok


def soft_edges(a):
    """cm per pixel of a coordinate picture, across and down: for edges one pixel soft."""
    gy, gx = np.gradient(a)
    return np.maximum(np.hypot(gx, gy), 1e-3).astype(F32)

"""Depth, for any scene (round twenty-three; DEPTH.md): small tools for the three planes that work with either camera
(`persp.Camera`, `room.View`) through two functions the scene gives:

    pt(X, Z) -> (x, y)      the picture point of a place on the ground (X across, Z away, in cm)
    px_per_cm(X, Z) -> k    how many picture pixels a centimetre is there

For `persp.Camera` c:  pt = lambda X, Z: c.pt(X, 0, Z);   px_per_cm = lambda X, Z: c.scale(Z)
For `room.View` v:     pt = lambda X, Z: v.pt(X, 0, Z);   px_per_cm = lambda X, Z: v.scale_at(X, Z)
"""

import numpy as np

from brush import F32, blur, grid, lerp, mask_poly, rgb, step


def scatter(pt, px_per_cm, bounds, per_m2, seed, size=(1.0, 1.0), zone=None, keep=None, most=6000):
    """Places for small things lying on the ground at a true density: `per_m2` of them to each square metre of ground
    inside `bounds` (X0, X1, Z0, Z1, cm), so they come out few and large near us, many and small far off, with no
    arithmetic in the scene. -> a list of (x, y, k, r): the picture point, the pixels per centimetre there, and a
    random number 0 to 1 for each (vary the thing with it). `size` is the thing's size in cm (across, up or along):
    anything smaller than a third of a pixel is left out. `zone`: a mask of the picture where they may lie; `keep`: a
    function (X, Z) -> bool for the ground's own shape (a road, a bank)."""
    X0, X1, Z0, Z1 = bounds
    rng = np.random.default_rng(seed)
    n = int(min((X1 - X0) * (Z1 - Z0) / 10000.0 * per_m2, most * 4))
    out = []
    h, w = zone.shape if zone is not None else (600, 800)
    for X, Z, r in zip(rng.uniform(X0, X1, n), rng.uniform(Z0, Z1, n), rng.random(n)):
        if keep is not None and not keep(X, Z):
            continue
        k = px_per_cm(X, Z)
        if k * max(size) < 0.34:
            continue
        x, y = pt(X, Z)
        if not (0 <= x < w and 0 <= y < h):
            continue
        if zone is not None and zone[int(y), int(x)] < 0.5:
            continue
        out.append((float(x), float(y), float(k), float(r)))
        if len(out) >= most:
            break
    out.sort(key=lambda p: p[1])                                    # far to near: lay them in that order
    return out


def air(picture, far, sky, amount=0.55, power=1.0, mask=None):
    """Air between us and far things: the picture moves toward `sky` (the sky's colour at the horizon) by how far away
    each pixel is. `far` is 0 for near to 1 for the farthest (a mask-shaped array: from a depth map, or painted by
    hand for layers of hills). Never grey: the sky's own colour."""
    sky = rgb(sky) if isinstance(sky, str) else np.asarray(sky, dtype=F32)
    m = np.clip(far, 0, 1) ** power * amount
    if mask is not None:
        m = m * mask
    picture[...] = picture * (1 - m[..., None]) + sky * m[..., None]
    return picture


def far_of_rows(shape, horizon, bottom=None, power=0.7):
    """A `far` map for level ground: 0 at the bottom edge (or the row `bottom`), 1 at the horizon; above the horizon 1."""
    h, w = shape
    x, y = grid(shape)
    b = float(h if bottom is None else bottom)
    t = np.clip((b - y) / max(b - horizon, 1.0), 0, 1) ** power
    return t.astype(F32)


def frame(picture, amount=0.16, bottom=0.22, color="#2a2440"):
    """The frame's corners and bottom edge a little deeper, so the eye stays in the middle of the picture (lay it on
    the backdrop before the details; never on a cut-out)."""
    h, w, _ = picture.shape
    x, y = grid((h, w))
    u, v = (x - w / 2) / (w / 2), (y - h / 2) / (h / 2)
    corner = np.clip((u * u + v * v - 0.75) / 1.25, 0, 1) ** 1.5 * amount
    low = step(h * 0.80, h, y) * bottom
    m = np.clip(corner + low, 0, 0.6)
    c = rgb(color)
    picture[...] = picture * (1 - m[..., None]) + picture * c * m[..., None] * 1.6
    return np.clip(picture, 0, 1, out=picture)


def ground_poly(pt, places):
    """Ground places [(X, Z), ...] as picture points: for a shadow's outline, a path, a patch of other earth."""
    return [pt(X, Z) for X, Z in places]


def shadow_on_ground(picture, pt, places, color="#4a4470", amount=0.42, soft=1.6, wobble=1.2, seed=0, ground=None):
    """A shadow lying on the ground, given by its outline in ground places (cm): a glaze (multiply), soft-edged. For
    the large shadow of something outside the picture, give places that run off the frame. `ground` masks it to the
    ground (so it does not climb a wall painted there)."""
    h, w, _ = picture.shape
    m = mask_poly((h, w), ground_poly(pt, places), soft=soft, wobble=wobble, seed=seed) * amount
    if ground is not None:
        m = m * ground
    c = rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
    picture[...] = picture * (1 - m[..., None]) + picture * (c * 1.5) * m[..., None]
    return np.clip(picture, 0, 1, out=picture)


def near_tone(color, shade="#241c30", k=0.55, warm=0.06):
    """A local colour as it is on the near plane in shade: deep, and a little warm. (Light its rim separately.)"""
    c = rgb(color) if isinstance(color, str) else np.asarray(color, dtype=F32)
    out = lerp(c, rgb(shade), k)
    out[0] = min(out[0] + warm, 1.0)
    return out.astype(F32)


def rim(alpha, light=(-1.0, -0.5), width=2.0):
    """The lit edge of a near thing: a mask of the thin strip just inside a cut-out's outline on the side the light
    comes from (`light`: the direction TO the light in the picture, x right, y down). Lay a warm light through it."""
    gy, gx = np.gradient(blur(alpha.astype(F32), width * 0.6))
    lx, ly = light
    n = max((lx * lx + ly * ly) ** 0.5, 1e-6)
    facing = np.clip(-(gx * lx + gy * ly) / n * 6.0, 0, 1)        # the alpha falls away toward the light on the lit side
    return (facing * np.clip(alpha, 0, 1)).astype(F32)

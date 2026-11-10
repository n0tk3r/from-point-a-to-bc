"""Property & Effects (office-property): the depth pass (round twenty-three; DEPTH.md). Works over the painting as it is
(out/office-property-orig/, the full run of office_property.py) and writes the scene's set back into out/office-property/,
every file as before plus near.png.

    python3 office_property_depth.py

THE CAMERA is the scene's own (room.View, office_property_model.VIEW); every pixel's ray is followed into the room's
shell (the floor, the ceiling, the far wall, the two shelf runs' faces, the side walls) to know how far off it is.
THE LIGHT: three light panels down the aisle, overhead (pale, a little green); nothing else lit.

- near.png, the front plane: the end upright of the left run's nearest unit, by the lens on our left (gray steel angle,
  its slotted face, two shelf lips and their brackets), in deep warm shade with its edge toward the aisle lit; and the
  near cut-out we had (front.png: the cart, the boxes, the bin) deeper and warmer, lit along its tops.
- back.png: carpet tiles laid on the floor in perspective (50 cm, quarter-turned, their seams), the light pooling under
  the panels and falling off toward the shelves and between the panels, the lower shelves dimmer, the near shelves and
  the near ceiling deeper and warmer, the far end of the room (the far wall, the counter, the door) cooler and paler.
- The far-wall cut-outs (wall, door, door-open, receipt) get exactly the same air as the backdrop behind them, pixel by
  pixel, so no seam shows; their outlines are kept exactly. vent, vent-eyes and banjo are copied byte for byte.
"""
import os
import shutil

import numpy as np
from PIL import Image

from brush import F32, blur, grain, lerp, mask_poly, rgb, palette_of, to_palette, save
from room import View
import depth
import office_property_model as M

SRC = os.environ.get("OP_SRC", "out/office-property-orig")
OUT = os.environ.get("OP_OUT", "out/office-property")
W, H = 800, 600
V = View(**M.VIEW)
SEED = 23


def load(name):
    a = np.asarray(Image.open(f"{SRC}/{name}.png").convert("RGBA")).astype(F32) / 255.0
    return a[..., :3].copy(), a[..., 3].copy()


def finish(pic, name, colors, alpha=None, seed=7):
    """The scene's own finish (office_room_kit.finish), with a lighter grain: the picture has its grain already."""
    g = grain(np.clip(pic, 0, 1), seed, 0.004)
    sample = g if alpha is None else g[alpha > 0.5]
    colors = max(2, min(colors, len(sample.reshape(-1, 3)) // 3))
    pal = palette_of([sample.reshape(-1, 1, 3)], colors)
    idx = to_palette(g, pal, speckle=0.004)
    save(f"{OUT}/{name}.png", idx, pal, alpha)


# ---------------------------------------------------------------- the room, ray by ray
def hits():
    """For every pixel: what of the shell its ray meets first and where: (kind, X, Y, Z). kind: 0 floor, 1 ceiling,
    2 far wall, 3 left run's face, 4 right run's face, 5 left wall, 6 right wall."""
    dX, dY, dZ = V._rays((H, W))
    ex, ey, ez = V.cam_x, V.eye, V.cam_z
    best = np.full((H, W), 1e9, F32)
    kind = np.full((H, W), -1, np.int16)
    with np.errstate(divide="ignore", invalid="ignore"):
        planes = [
            (0, (0.0 - ey) / dY, None),
            (1, (M.H - ey) / dY, None),
            (2, (0.0 - ez) / dZ, None),
            (3, (M.LEFT_X[1] - ex) / dX, ("L",)),
            (4, (M.RIGHT_X[0] - ex) / dX, ("R",)),
            (5, (0.0 - ex) / dX, None),
            (6, (M.W - ex) / dX, None),
        ]
        for k, t, run in planes:
            ok = np.isfinite(t) & (t > 1.0)
            X, Y, Z = ex + dX * t, ey + dY * t, ez + dZ * t
            if run == ("L",):
                ok &= (Z > M.LEFT_Z[0][0]) & (Z < M.LEFT_Z[-1][1]) & (Y < M.UNIT_H + 30)
            elif run == ("R",):
                ok &= (Z > M.RIGHT_Z[0][0]) & (Z < M.RIGHT_Z[-1][1]) & (Y < M.UNIT_H + 30)
            ok &= (Y > -1) & (Y < M.H + 1) & (X > -1) & (X < M.W + 1) & (Z > -1)
            closer = ok & (t < best)
            best = np.where(closer, t, best)
            kind = np.where(closer, k, kind)
    t = np.where(best < 1e8, best, 0)
    return kind, (ex + dX * t).astype(F32), (ey + dY * t).astype(F32), (ez + dZ * t).astype(F32)


KIND, HX, HY, HZ = hits()
FLOOR = (KIND == 0).astype(F32)
RUNS = ((KIND == 3) | (KIND == 4)).astype(F32)
# where things stand on the floor (Opal's stool, her basket and the scarf, the counter): no seams over them
THINGS = np.zeros((H, W), F32)
for poly in ([[421, 363], [428, 361], [443, 361], [448, 362], [452, 364], [452, 368], [449, 416], [446, 421], [423, 420], [421, 368]],
             [[428, 429], [465, 396], [485, 381], [491, 382], [498, 395], [497, 419], [496, 420], [459, 430], [449, 432], [436, 432]]):
    THINGS = np.maximum(THINGS, mask_poly((H, W), [tuple(p) for p in poly], soft=2.0))
THINGS = np.maximum(THINGS, ((HZ < M.COUNTER[5] + 4) & (HX > M.COUNTER[0] - 4) & (HX < M.COUNTER[1] + 4)).astype(F32))
THINGS = np.maximum(THINGS, ((HZ < M.CABINET[5] + 4) & (HX < M.CABINET[1] + 4)).astype(F32))


def seams_of(picture):
    """Carpet tiles, 50 cm, laid quarter-turned: each tile a touch lighter or darker by its pile's way, and the seams
    between them, thin, in perspective, fading out where the tiles grow too small to see."""
    s = 50.0
    u, v = HX / s, HZ / s
    gu = np.hypot(*np.gradient(u)) + 1e-6
    gv = np.hypot(*np.gradient(v)) + 1e-6
    du = np.abs(u - np.round(u)) / gu
    dv = np.abs(v - np.round(v)) / gv
    line = np.maximum(np.clip(1.0 - du / 0.85, 0, 1) * np.clip((0.30 - gu) / 0.18, 0, 1),
                      np.clip(1.0 - dv / 0.85, 0, 1) * np.clip((0.30 - gv) / 0.18, 0, 1))
    iu, iv = np.floor(u).astype(np.int32), np.floor(v).astype(np.int32)
    turn = ((iu + iv) & 1).astype(F32) * 2 - 1                       # quarter-turned: a checker of pile
    rng = np.random.default_rng(SEED)
    jit = rng.uniform(-1, 1, 4096).astype(F32)[(iu * 31 + iv * 17) & 4095]
    ok = FLOOR * (1 - np.clip(THINGS * 1.5, 0, 1))
    # an object painted on the floor (the scarf, a shadow's edge) differs from the carpet round it: leave it
    lum = picture @ np.array([0.30, 0.59, 0.11], F32)
    local = blur(lum, 6.0)
    ok = ok * np.clip(1.0 - (np.abs(lum - local) - 0.06) / 0.06, 0, 1)
    far = np.clip((gu + gv) / 0.5, 0, 1)
    tone = 1.0 + (0.014 * turn + 0.010 * jit) * (1 - far)
    picture *= (1 + (tone - 1) * ok)[..., None]
    picture *= (1 - 0.13 * line * ok)[..., None]
    return picture


def light_of_panels():
    """How much of the panels' light reaches the floor and the shelves: pools under the three panels, falling off
    toward the shelves and between the panels; the lower shelves dimmer than the upper."""
    xc = 210.0
    lat = np.clip(np.abs(HX - xc) / 175.0, 0, 1)
    pool = np.zeros((H, W), F32)
    for x0, x1, z0, z1 in M.TROFFERS:
        zc = (z0 + z1) / 2
        pool = np.maximum(pool, np.exp(-((HZ - zc) / 125.0) ** 2))
    floor = 1.0 - 0.20 * lat ** 1.4 - 0.09 * (1 - pool)
    low = np.clip((150.0 - HY) / 150.0, 0, 1)
    runs = 1.0 - 0.12 * low ** 1.2 - 0.05 * (1 - pool)
    f = np.ones((H, W), F32)
    f = np.where(KIND == 0, floor, f)
    f = np.where(RUNS > 0, runs, f)
    return blur(f.astype(F32), 1.2)


def near_of_shell():
    """0 to 1: how near us a pixel's surface is: the near bays of both runs (the left run's nearest bay in the picture
    stands about 5 m in, at Z 450 to 540), the near ceiling, the floor at our feet (below the walk's front edge)."""
    n = np.clip((HZ - 400.0) / 110.0, 0, 1) ** 1.2
    n = np.where(KIND == 1, np.clip((HZ - 380.0) / 140.0, 0, 1) * 0.55, n)
    n = np.where(KIND == 0, np.clip((HZ - 330.0) / 120.0, 0, 1) * 0.6, n)
    return blur(n.astype(F32), 2.0)


def far_of_shell():
    """0 to 1: how far off: the far wall and what stands at it 1, nothing nearer than the middle of the room."""
    f = np.clip((260.0 - HZ) / 230.0, 0, 1) ** 1.1
    return blur(f.astype(F32), 2.0)


NEAR_SHELL = near_of_shell()
FAR_SHELL = far_of_shell()
COOL = rgb("#c9d6dc")
DEEP = rgb("#2c2226")


def air(picture, alpha=None):
    """The far end of the room cooler and paler (the same, pixel by pixel, on the backdrop and the far cut-outs); the
    hall's light through the glass and the door's slit kept as they are."""
    lum = picture @ np.array([0.30, 0.59, 0.11], F32)
    keep = np.clip((lum - 0.80) / 0.12, 0, 1)
    m = (0.20 * FAR_SHELL * (1 - keep))[..., None]
    picture[...] = picture * (1 - m) + COOL * m
    cool = (0.05 * FAR_SHELL * (1 - keep))
    picture[..., 0] *= 1 - cool
    picture[..., 2] *= 1 + cool * 0.6
    return np.clip(picture, 0, 1, out=picture)


def deepen_back(back):
    back *= light_of_panels()[..., None]
    seams_of(back)
    lum = back @ np.array([0.30, 0.59, 0.11], F32)
    nn = NEAR_SHELL * (1 - np.clip((lum - 0.72) / 0.12, 0, 1))        # (the light panels stay lights)
    n = nn[..., None]
    back[...] = back * (1 - 0.55 * n) + back * DEEP * 1.9 * (0.55 * n)
    back[..., 0] += 0.012 * nn
    air(back)
    return np.clip(back, 0, 1, out=back)


# ---------------------------------------------------------------- the front plane
def warm_near(pic, alpha, k=0.52, light=(0.0, -1.0), rim_amt=0.55):
    """A near cut-out deeper and warmer, and lit along the side its light comes from."""
    shade = rgb("#2a1f24")
    out = lerp(pic, pic * 0.45 + shade * 0.55, k)
    out[..., 0] = np.clip(out[..., 0] + 0.025 * k, 0, 1)
    r = depth.rim(alpha, light=light, width=2.0)
    lit = rgb("#e6ecd8")                                         # the panels' light: pale, a little green
    out = out * (1 - (r * rim_amt)[..., None]) + lerp(out, lit, 0.55) * (r * rim_amt)[..., None]
    return np.clip(out, 0, 1)


def paint_post():
    """The end upright of the nearest unit of the left run, by the lens on our left: a steel angle, its slotted face,
    the ends of two shelves and their brackets running off the frame. -> (colour, alpha)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(F32)
    col = np.zeros((H, W, 3), F32)
    a = np.zeros((H, W), F32)
    steel = depth.near_tone("#8a9496", shade="#22181a", k=0.80, warm=0.045)
    edge = depth.near_tone("#a7b0ae", shade="#22181a", k=0.66, warm=0.05)
    rng = np.random.default_rng(SEED + 1)
    # the post: 0 .. 20 px, a little wobble to its edge (hand painted), its flange toward the aisle (the lit edge)
    wob = blur(rng.normal(0, 1, (H, 1)).astype(F32), 6.0)[:, 0] * 0.6
    right = 19.0 + wob[:, None]
    post = np.clip(right - xx + 0.5, 0, 1)
    a = np.maximum(a, post)
    t = np.clip(xx / np.maximum(right, 1), 0, 1)
    face = lerp(steel, steel * 0.78, t[..., None] ** 2)
    col = np.where(post[..., None] > 0, face, col)
    # the flange: a narrower strip at the post's aisle edge, a shade lighter
    fl = np.clip(right - xx + 0.5, 0, 1) * np.clip(xx - (right - 5.0) + 0.5, 0, 1)
    col = lerp(col, edge, (fl * 0.6)[..., None])
    # the slots up its face (teardrop holes, dark), every 5 cm of steel
    for y0 in np.arange(6.0, H, 17.0):
        sl = np.clip(1.0 - np.hypot((xx - 8.5) / 1.6, (yy - y0) / 4.0), 0, 1)
        col = lerp(col, rgb("#140e12"), (np.clip(sl * 3, 0, 1) * 0.85 * post)[..., None])
    # two shelves' ends with their brackets: thin lips coming off the post toward us (off the left edge), a little slant
    for yc, h in ((92.0, 9.0), (468.0, 11.0)):
        lip = np.clip(1 - np.abs(yy - (yc - 0.12 * (20 - xx))) / (h / 2), 0, 1) * np.clip(26.0 - xx, 0, 1)
        lip = np.clip(lip * 2.2, 0, 1)
        a = np.maximum(a, lip)
        col = np.where(lip[..., None] > post[..., None], lerp(steel * 0.9, edge, 0.25), col)
        # the bracket's gusset, a small triangle under the lip at the post
        gus = np.clip((yc + h / 2 + 10 - yy) / 2.0, 0, 1) * np.clip((yy - (yc + h / 2 - 1)) / 1.0, 0, 1) \
            * np.clip((24.0 - xx - (yy - yc - h / 2) * 0.8), 0, 1)
        a = np.maximum(a, gus)
        col = np.where(gus[..., None] > np.maximum(post, lip)[..., None], steel * 0.85, col)
    a = np.clip(a, 0, 1)
    # in shade it is not flat: darker low down (nearer the floor, out of the panels' light)
    col *= (1 - 0.18 * np.clip((yy - 300) / 300, 0, 1))[..., None]
    r = depth.rim(a, light=(1.0, -0.35), width=1.6)
    lit = rgb("#dfe6d2")
    col = col * (1 - (r * 0.7)[..., None]) + lerp(col, lit, 0.6) * (r * 0.7)[..., None]
    return np.clip(col, 0, 1), a


def main():
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back")
    deepen_back(back)
    finish(back, "back", 160)

    for name, colors in (("wall", 72), ("door", 48), ("door-open", 48), ("receipt", 48)):
        p, a = load(name)
        air(p)
        finish(p, name, colors, a)

    for name in ("vent", "vent-eyes", "banjo"):
        shutil.copyfile(f"{SRC}/{name}.png", f"{OUT}/{name}.png")
    for f in os.listdir(SRC):
        if not f.endswith(".png") and os.path.isfile(f"{SRC}/{f}"):
            shutil.copyfile(f"{SRC}/{f}", f"{OUT}/{f}")

    p, a = load("front")
    xx = np.mgrid[0:H, 0:W][1].astype(F32)
    left = warm_near(p, a, light=(0.45, -1.0))
    right = warm_near(p, a, light=(-0.45, -1.0))
    side = np.clip((xx - 330) / 140, 0, 1)[..., None]
    finish(lerp(left, right, side), "front", 64, a)

    c, na = paint_post()
    na = na * (1 - np.clip(a * 1.0, 0, 1))                      # (the old near cut-out keeps its own pixels)
    finish(c, "near", 40, np.where(na > 0.02, na, 0).astype(F32))

    # a look: everything laid together, and twice its size
    im = Image.open(f"{OUT}/back.png").convert("RGBA")
    for f in ("vent", "wall", "door", "banjo", "front", "near"):
        im.alpha_composite(Image.open(f"{OUT}/{f}.png").convert("RGBA"))
    im.convert("RGB").save("out/office-property-depth-comp.png")
    print("near share", round(float((np.maximum(na, a) > 0.5).mean()) * 100, 1), "%; new", round(float((na > 0.5).mean()) * 100, 1), "%")


if __name__ == "__main__":
    main()

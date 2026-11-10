"""Inside the wagon (egypt-car), the depth pass (round twenty-three; DEPTH.md): worked over the painting as egypt_car.py
paints it, not painted again.

    python3 egypt_car_depth.py          reads out/egypt-car-orig/ (the full run's files, kept as they were) and the masks
                                        that run kept (out/egypt-car-work/masks.npz); writes the full set to out/egypt-car/

THE NEAR PLANE (near.png): the frame of the car nearest the lens, in shade: the headliner over Dad's head and the roof's
edge along the top of the picture, the windshield's two pillars down its sides (the Son's at the right edge, Dad's thin
one at the left). Through the scene's own camera (room.View): the pillars as egypt_car_things.shell builds them, the
ceiling everything above the glass that no clickable thing covers. The light is the low sun ahead and to the right,
beyond the glass: the pillars are lit only along their right-hand edges (backlit by the glass, the glare at its top
right), the roof's edge only along the header over the glass, by the light the sunlit dash throws up. The driver's
visor (up or down), the rearview mirror and the air freshener hang in front of the roof: near.png has holes where they
are, and the backdrop carries the same deepened roof under them, so that either state of the visor shows it whole.

THE BACKDROP, deepened: the roof and pillars as on near.png (under the holes); the steering wheel's rim and spokes the
nearest dark of the picture, warm, with a thin lit edge toward the sunlit dash; the world through the glass a step
paler in the air (the far bank and the sky most, the river less, the mound of sand on the hood least), with the glass's
own reflections faint over it; the dashboard's shadows: the shade under the padded lip on the dash's face, the darks of
the face and the footwells deeper toward us. Nothing that is clicked moves or is drawn again.

THE CUT-OUTS as they were (copied byte for byte); layout.json as it was."""

import os
import shutil

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, blur, lerp, noise, rgb, grain, palette_of, to_palette, save, grid
import depth
import egypt_car_model as M
from room import View

W, H = 800, 600
V = View(**M.VIEW)
ORIG = "out/egypt-car-orig"
OUT = "out/egypt-car"
MASKS = "out/egypt-car-work/masks.npz"
CUTS = ("glovebox-shut", "glovebox-map", "glovebox-empty", "visor-up", "visor-down", "freshener")

SHADE = "#301c12"            # the near plane's shade: frankly warm, so that the key keeps it warm
RIM_SUN = "#f4d29c"          # the low sun's light round the pillars' edges
RIM_BOUNCE = "#e8bf8a"       # the light the sunlit dash throws up onto the roof's edge over the glass
_Y, _X = np.mgrid[0:H, 0:W].astype(F32)


def load(name):
    im = Image.open(f"{ORIG}/{name}.png").convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def poly(points, grow=0.0):
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in points], fill=255)
    m = np.asarray(im, dtype=F32) / 255
    return blur(m, grow) > 0.02 if grow else m > 0.5


def dilate(m, r=1):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def pillars():
    """The windshield's two pillars as egypt_car_things.shell builds them, through the camera: (left, right) masks."""
    W_, B, R, T = M.W, M.BELT, M.ROOF, M.TUMBLE
    out = []
    for side in (-1, 1):
        foot = (0.0 if side < 0 else W_, B, M.GLASS["z0"])
        top = (T if side < 0 else W_ - T, R, M.GLASS["z1"])
        wid, inward = 10.5, (6.0 if side < 0 else 3.2)
        a = (foot[0] - side * inward, foot[1], foot[2] + wid)
        b = (top[0] - side * inward * 0.8, top[1], top[2] + wid * 0.85)
        pts = [V.pt(*p) for p in (foot, top, b, a)]
        # run the pillar on up past the roof's edge, off the top of the frame (it meets the roof rail there)
        (x0, y0), (x1, y1) = pts[0], pts[1]
        (x3, y3), (x2, y2) = pts[3], pts[2]
        ext = lambda xa, ya, xb, yb: (xb + (xb - xa) * (yb + 20) / max(ya - yb, 1e-3), -20.0)
        pts = [pts[0], ext(x0, y0, x1, y1), ext(x3, y3, x2, y2), pts[3]]
        out.append(poly(pts, grow=1.6))
    return out


def regions(z, cut_alpha):
    """R: the roof and the pillars (everything of the car there that no clickable thing covers); the holes in near.png
    where the visor (up or down), the mirror and the air freshener hang in front of the roof."""
    hot = np.zeros((H, W), bool)
    for k in z.files:
        if k.startswith("m-"):
            hot |= z[k]
    hot |= z["x-visor-down"]
    world = z["escaped_b"] > 0.5
    glass = z["glass_view"]
    door = z["m-door"] | z["m-manual"]
    pl, pr = pillars()
    # the top of the glass, column by column (the roof is everything of the car above it)
    gtop = np.full(W, 70, int)
    for x in range(W):
        ys = np.where(glass[:, x])[0]
        if len(ys):
            gtop[x] = min(ys.min(), 70)
    ceiling = _Y < gtop[None, :]
    roof = ceiling & ~glass & ~door & ~world
    side = (pl | pr) & ~glass & ~door & ~world & (_Y < 312)
    R = roof | side
    # the holes: what hangs in front of the roof (exact cut-out outlines, and the mirror's own shape, a pixel wider)
    holes = dilate(z["m-rearview"] | z["m-freshener"], 1)
    for n in ("visor-up", "visor-down", "freshener"):
        holes |= cut_alpha[n] > 0.5
    return R, roof, side & ~roof, holes, hot


def near_paint(back, R, roof, side):
    """The roof and pillars in deep warm shade, the cloth's own texture kept under it; lit along the edges that face the
    light."""
    nearness = np.clip(1 - _Y / 70.0, 0, 1)                         # the roof: nearest at the top of the frame
    k = np.where(roof, 0.64 + 0.14 * nearness, 0.0)
    down = np.clip((_Y - 60) / 240.0, 0, 1)                          # the pillars: a little less deep toward their feet, by the sunlit dash
    k = np.where(side, 0.74 - 0.10 * down, k).astype(F32)
    k = k * (1 + 0.10 * (noise((H, W), 26, 1830, 3) - 0.5))         # a brush's unevenness
    shade = rgb(SHADE)
    out = back * (1 - k[..., None]) + shade * k[..., None]
    out[..., 0] = np.clip(out[..., 0] + 0.045 * (k > 0), 0, 1)       # the near plane's warm note
    a = R.astype(F32)
    rs = depth.rim(a, light=(1.0, -0.35), width=2.6) * side         # backlit by the glass: the right-hand edges
    rb = depth.rim(a, light=(0.1, 1.0), width=2.0) * roof * (_Y > 30)    # the header over the glass, from below
    for m, c, amt in ((rs, RIM_SUN, 0.72), (rb, RIM_BOUNCE, 0.50)):
        m = np.clip(m, 0, 1)[..., None] * amt
        out = out * (1 - m) + rgb(c) * m
    return np.clip(out, 0, 1).astype(F32)


def world_air(pic, z):
    """The world through the glass a step paler in the air (toward the haze at the horizon), and the glass's own
    reflections faint over it."""
    world = (z["escaped_b"] > 0.5) & z["glass_view"] & ~z["hood"]
    w = blur(world.astype(F32), 0.7)
    hz = 120.0
    band = world & (np.abs(_Y - (hz - 8)) < 4)
    haze = pic[band].mean(axis=0) if band.any() else rgb("#d8c8c8")
    haze = lerp(haze, rgb("#f0e2d0"), 0.35)                          # the sky's colour at the horizon, warmed by the afternoon
    far = np.clip((188.0 - _Y) / 64.0, 0, 1) ** 1.2                   # the far bank and the sky 1, the river half, the mound 0
    amount = (0.06 + 0.17 * far) * w
    out = pic * (1 - amount[..., None]) + haze * amount[..., None]
    # the glass's reflections: the pale ghost of the sunlit dash in the lower glass, and two soft diagonal sheens
    gl = blur(z["glass_view"].astype(F32), 0.7)
    low = np.clip((_Y - 200) / 85.0, 0, 1) ** 1.5
    u = (_X * 0.62 + _Y)
    sheen = np.exp(-((u - 560) / 26.0) ** 2) * 0.6 + np.exp(-((u - 640) / 12.0) ** 2) * 0.45
    sheen = sheen * np.clip((_X - 420) / 200.0, 0, 1)
    refl = np.clip(low * 0.08 + sheen * 0.07, 0, 0.12) * gl
    refl = refl * (0.75 + 0.5 * noise((H, W), 40, 1831, 3))
    out = 1 - (1 - out) * (1 - rgb("#fff4e0") * refl[..., None])
    return np.clip(out, 0, 1).astype(F32)


def wheel_dark(pic, z):
    """The steering wheel's rim and spokes: the nearest dark of the picture, warm; a thin lit edge where they face the
    sunlit dash and the glass."""
    m = z["m-wheel"]
    a = blur(m.astype(F32), 0.5) * m
    k = 0.40
    out = pic.copy()
    deep = pic * (1 - k) + rgb("#2a1810") * k
    deep[..., 0] = np.clip(deep[..., 0] + 0.02, 0, 1)
    out = np.where(m[..., None], deep, out)
    edge = np.clip(depth.rim(m.astype(F32), light=(0.55, -1.0), width=1.6), 0, 1) * m * 0.30
    out = out * (1 - edge[..., None]) + rgb("#d8a878") * edge[..., None]
    return np.clip(out, 0, 1).astype(F32)


def dash_shadows(pic, z, R):
    """The dashboard's shadows: the shade the padded lip throws on the dash's face; the face's darks and the footwells
    deeper toward us (lower in the picture), the near floor deepest."""
    world = z["escaped_b"] > 0.5
    keep = ~(world | R | z["m-wheel"])
    out = pic.copy()
    # the lip's shade on the face: a soft band under the dash top's edge, from the gauges' hood to the glovebox
    lum = pic @ np.array([0.30, 0.55, 0.15], F32)
    top = np.zeros(W, F32)
    for x in range(W):                                               # the dash top's lower edge: where its sunlit band ends going down
        col = lum[284:380, x]
        lit = np.where(col > 0.62)[0]
        top[x] = 284 + (lit.max() + 1 if len(lit) else 46)
    top = blur(top[None, :].repeat(3, 0), 6)[1]
    under = np.clip(1 - (_Y - top[None, :]) / 16.0, 0, 1) * (_Y >= top[None, :])
    under = blur(under.astype(F32), 1.2) * keep * ~(z["m-cupholder"] | z["m-gauges"] | z["m-radio"])
    m = under * 0.30
    out = out * (1 - m[..., None]) + out * rgb("#7a5034")[None, None, :] * 1.15 * m[..., None]
    # deeper toward us: the lower picture's darks, a warm glaze growing to the bottom edge
    low = np.clip((_Y - 430) / 170.0, 0, 1) ** 1.3
    dark = np.clip((0.50 - lum) / 0.30, 0, 1)
    m = (low * (0.10 + 0.22 * dark)) * keep
    out = out * (1 - m[..., None]) + out * rgb("#5a3420")[None, None, :] * 1.2 * m[..., None]
    return np.clip(out, 0, 1).astype(F32)


def finish(picture, name, colors, alpha=None, seed=7, speckle=0.008, amount=0.012):
    """As egypt_car.py finishes it: grain, a palette of the picture's own with a little speckle, an 8-bit PNG."""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 3)], colors=colors)
    save(name, to_palette(g, pal, speckle=speckle), pal, alpha)
    return os.path.getsize(name)


def main():
    os.makedirs(OUT, exist_ok=True)
    z = np.load(MASKS)
    back, _ = load("back")
    cut_alpha = {n: load(n)[1] for n in CUTS}
    R, roof, side, holes, hot = regions(z, cut_alpha)
    paint = near_paint(back, R, roof, side)
    b = np.where(R[..., None], paint, back)
    b = world_air(b, z)
    b = wheel_dark(b, z)
    b = dash_shadows(b, z, R)
    nearA = (R & ~holes).astype(F32)
    sizes = {"back": finish(b, f"{OUT}/back.png", 160)}
    sizes["near"] = finish(np.where(R[..., None], paint, back), f"{OUT}/near.png", 64, nearA)
    for n in CUTS:
        shutil.copyfile(f"{ORIG}/{n}.png", f"{OUT}/{n}.png")
    shutil.copyfile(f"{ORIG}/layout.json", f"{OUT}/layout.json")
    print("near share", round(float(nearA.mean()) * 100, 1), "%;", "hot under near", int((nearA > 0.5)[hot].sum()), "px;", sizes)
    # a comp to look at: the first state, and the later one
    for tag, names in (("", ["glovebox-shut", "visor-up", "freshener", "near"]), ("-later", ["glovebox-map", "visor-down", "freshener", "near"])):
        im = Image.open(f"{OUT}/back.png").convert("RGBA")
        for n in names:
            im.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
        im.convert("RGB").save(f"out/egypt-car-depth-comp{tag}.png")


if __name__ == "__main__":
    main()

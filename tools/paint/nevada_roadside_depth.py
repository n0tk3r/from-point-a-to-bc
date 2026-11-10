"""nevada-roadside, round twenty-three: the depth pass, over the painting as it is (DEPTH.md; LITE.md).

Reads out/nevada-roadside-orig/ (nevada_roadside.py's full run, never changed) and writes the scene's set back into
out/nevada-roadside/: every file as it was, back.png deepened, and near.png, the front plane.

near.png  We stand in the shade of a lean-to at the right, out of the picture: the edge of its tin awning across the
          top right (the fascia board, the tin's ribs and the rafters seen from below, running to the picture's one
          vanishing point), its post at the right edge with a knee brace up to the awning, and a lip of gravel with
          sagebrush along the bottom right corner, where nobody walks. Deep warm shade; the sun's rim on the right,
          the warm light bounced up from the sunlit lot along the undersides.
back.png  The morning shadows of the store, the pump, the sign, the stand and the car deepened (the painter's own
          `shadows`, the same sun); the long shadow of a telephone pole off the right edge, leading in across the
          lot; old tire ruts swinging in to the pump; stones and tufts on the lot through the camera (few and large
          near, many and small far); the mesas and the far plain moved toward the sky's colour at the horizon.
"""

import math, os, shutil, sys
import numpy as np
from PIL import Image
from brush import *
import depth
from nevada_roadside_kit import *
import nevada_roadside as R

SCENE = "nevada-roadside"
ORIG = f"out/{SCENE}-orig"
OUT = f"out/{SCENE}"
SHAPE = (H, W)


def load(name):
    a = np.asarray(Image.open(os.path.join(ORIG, name)).convert("RGBA"), dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def pt(X, Z):
    return CAM.pt(X, 0, Z)


def kk(X, Z):
    return CAM.scale(Z)


def warm_shade(color, k=0.56):
    """A local colour on the near plane in shade: deep, frankly warm (the key turns warm darks violet)."""
    return depth.near_tone(color, shade="#2a1a18", k=k, warm=0.07)


# ---------------------------------------------------------------- the front plane
VX, VY = 400.0, float(HZ)                     # the picture's one vanishing point


def fascia_y(x):
    """The lower edge of the awning's fascia board: level, and sagging a little between its posts."""
    return 80.0 + 4.0 * math.sin(math.pi * (x - 340.0) / 460.0) + 1.2 * math.sin(x / 23.0)


def away(x, y, to_y):
    """Along a line that runs straight away from us (through the vanishing point): the point at row `to_y`."""
    return x + (x - VX) * (to_y - y) / (y - VY)


def near_plane(seed=23):
    s = Paper(SHAPE)
    rng = np.random.default_rng(seed)
    XL = 340.0                                                     # the awning's left end, at the fascia
    xs = np.linspace(XL, 806, 60)
    under = "#a8835e"                                              # the tin's underside, the rafters, the boards
    # the underside of the awning: from the fascia toward us (up and off the top of the frame)
    top_left = away(XL, fascia_y(XL) - 14, 0.0)
    body = [(top_left, -4), (806, -4), (806, fascia_y(806) - 14)] + [(x, fascia_y(x) - 14) for x in xs[::-1]]
    s.poly(body, warm_shade(under, 0.60))
    # the warm light bounced up off the lot, strongest by the fascia, fading toward us
    for i in range(8):
        f = i / 8.0
        band = [(away(x, fascia_y(x) - 14, (fascia_y(x) - 14) * (1 - f * 0.55)), (fascia_y(x) - 14) * (1 - f * 0.55)) for x in xs]
        band2 = [(away(x, fascia_y(x) - 14, (fascia_y(x) - 14) * (1 - (f + 0.13) * 0.55)), (fascia_y(x) - 14) * (1 - (f + 0.13) * 0.55)) for x in xs]
        s.poly(band + band2[::-1], warm_shade("#d8a272", 0.50), 0.10 * (1 - f))
    # the tin's ribs, running away from us: alternate light and dark
    x = XL + 3
    while x < 806:
        y0 = fascia_y(x) - 14
        c = warm_shade("#c09878", 0.55) if int((x - XL) / 5.0) % 2 == 0 else warm_shade("#6a5040", 0.62)
        s.line([(x, y0), (away(x, y0, -4), -4)], c, 1.3, 0.55)
        x += 5.0 + rng.normal(0, 0.4)
    # a purlin across, near us (level: parallel to the picture), and the rafters running away
    for yy, w in ((26.0, 7.0), (52.0, 5.0)):
        x0 = away(XL, fascia_y(XL) - 14, yy)
        s.line([(x0, yy + rng.normal(0, 0.6)), (806, yy + 1.5)], warm_shade("#7a5a40", 0.66), w)
        s.line([(x0, yy + w * 0.5), (806, yy + w * 0.5 + 1.5)], warm_shade("#c89a6c", 0.5), 1.0, 0.45)     # its lower edge catches the bounce
    for xr in (XL + 2, 452, 566, 682, 790):
        y0 = fascia_y(xr) - 14
        s.taper([(xr, y0), (away(xr, y0, y0 * 0.5), y0 * 0.5), (away(xr, y0, -4), -4)], warm_shade("#6e5038", 0.68), 6.0, 11.0)
    # the fascia board: its back face to us, weathered planks
    face = [(x, fascia_y(x) - 15) for x in xs] + [(x, fascia_y(x) + 1) for x in xs[::-1]]
    s.poly(face, warm_shade("#8c6a48", 0.58))
    for x0 in np.arange(XL, 806, 3.0):
        if rng.random() < 0.35:
            l = rng.uniform(8, 40)
            yy = fascia_y(x0) - 15 + rng.uniform(2, 13)
            s.line([(x0, yy), (x0 + l, yy + rng.normal(0, 0.4))], warm_shade("#5a3e2c", 0.62), 0.8, 0.6)
    s.line([(x, fascia_y(x) + 0.5) for x in xs], warm_shade("#e0aa78", 0.42), 1.4, 0.8)                # bounce along its lower edge
    # the tin's edge over it, ragged, two nails' rust
    s.line([(x, fascia_y(x) - 15 + 0.8 * math.sin(x / 2.5)) for x in np.linspace(XL, 806, 240)], warm_shade("#b8b0a4", 0.5), 1.5)
    # the left end of the awning: the end rafter, running away from us
    y0 = fascia_y(XL)
    s.taper([(XL - 1, y0 + 1), (away(XL - 1, y0, y0 * 0.5), y0 * 0.5), (away(XL - 1, y0, -4), -4)], warm_shade("#5e4230", 0.66), 7.0, 12.0)

    # the post at the right edge, 2.7 m from the lens: its right half off the frame; it leans a hair
    def post_x(y):
        return 774.0 - (y - 80.0) * 0.004
    post = [(post_x(fascia_y(780)), fascia_y(780)), (812, fascia_y(780)), (812, 606), (post_x(606), 606)]
    s.poly(post, warm_shade("#866446", 0.60))
    for i in range(6):                                              # checks and grain down the wood
        xg = post_x(300) + 3 + i * 4.2 + rng.normal(0, 0.8)
        y1 = rng.uniform(90, 300)
        s.line([(xg, y1), (xg + rng.normal(0, 1.0), y1 + rng.uniform(80, 260))], warm_shade("#4a3226", 0.64), rng.uniform(0.7, 1.3), 0.7)
    s.line([(post_x(y), y) for y in (fascia_y(780), 606)], warm_shade("#3a281e", 0.66), 1.6)            # its shadowed left arris
    # the knee brace, from the post up to the fascia
    b0, b1 = (post_x(196) + 1, 196.0), (690.0, fascia_y(690) - 2)
    s.taper([b0, ((b0[0] + b1[0]) / 2, (b0[1] + b1[1]) / 2 + 1), b1], warm_shade("#8a6848", 0.58), 11.0, 10.0)
    s.line([(b0[0] - 2, b0[1] - 6), (b1[0] + 3, b1[1] - 1)], warm_shade("#5a3e2c", 0.62), 1.0, 0.7)

    # the lip of the gravel along the bottom right corner (where nobody walks), and its sagebrush
    lip = [(636, 606), (640, 596)]
    for x in np.arange(646, 812, 6.0):
        lip.append((x, 592 - (x - 640) * 0.035 + rng.normal(0, 1.2)))
    lip += [(812, 606)]
    s.poly(lip, warm_shade("#9a6a44", 0.58))
    for x in np.arange(644, 806, 5.0):                               # stones standing proud on the lip's edge
        if rng.random() < 0.55:
            yy = 592 - (x - 640) * 0.035 + rng.normal(0, 0.8)
            r = rng.uniform(1.6, 3.6)
            s.ellipse(x, yy, r * 1.3, r, warm_shade("#b08060", 0.54))
    dark = tuple(warm_shade(c, 0.45) for c in ("#3e4a3e", "#6c7a64", "#9aa486", "#c8cca8"))
    sagebrush(s, 676, 610, 30, seed + 1, tones=dark)
    sagebrush(s, 742, 612, 42, seed + 2, tones=dark)
    tuft(s, 708, 598, 14, seed + 3, colors=tuple(warm_shade(c, 0.4) for c in ("#6a6a48", "#a89c64", "#d8c88c")))
    c, a = s.done()
    # the sun's rim on the edges that face it (low on the right), and a touch of bounce from below
    r = depth.rim(a, light=(1.0, -0.25), width=2.0) * 0.85
    over(c, rgb("#f2b878"), r)
    a = np.where(a > 0.02, a, 0).astype(F32)
    return c, a


# ---------------------------------------------------------------- the backdrop, deepened
def lot_zone():
    x, y = grid(SHAPE)
    z = (y >= 455).astype(F32)
    z = np.maximum(z, ((y >= 302) & (x > 380) & (x < 556)).astype(F32))
    z *= 1 - mask_ellipse(SHAPE, 648, 536, 104, 30, soft=4)           # the glass lies clean, in the sun
    return z


def deepen(back):
    x, y = grid(SHAPE)
    ground = step(HZ, HZ + 6, y)
    # 1. the morning shadows of everything standing, deeper and bluer (the painter's own shadows, the same sun)
    sh, _ = R.shadows(SHAPE)
    m = sh * 0.24 * ground
    c = rgb(SHADOW) * 1.5
    back[...] = back * (1 - m[..., None]) + back * c * m[..., None]
    # 2. the long shadow of a telephone pole off the right edge, leading in across the lot, its crossarm at the end
    Xp, Zp, Hp = 830.0, 700.0, 640.0
    tip = (Xp + SUN[0] * Hp, Zp + SUN[1] * Hp)
    line = mask_line(SHAPE, [gp(Xp, Zp), gp(*tip)], 3.2, soft=0.7)
    arm_at = (Xp + SUN[0] * (Hp - 40), Zp + SUN[1] * (Hp - 40))
    arm = mask_line(SHAPE, [gp(arm_at[0], arm_at[1] - 110), gp(arm_at[0], arm_at[1] + 110)], 2.6, soft=0.6)
    pole = np.maximum(line, arm) * ground * (1 - mask_ellipse(SHAPE, 648, 536, 104, 30, soft=4))
    m = pole * 0.46
    back[...] = back * (1 - m[..., None]) + back * c * m[..., None]
    # 3. old tire ruts swinging in from the bottom to the pump island
    sheet = Paper(SHAPE)
    mid = curve([(170.0, -40.0), (120.0, 200.0), (20.0, 460.0), (-90.0, 700.0)], 30)
    for side in (-78.0, 78.0):
        pts = [gp(X + side, Z) for X, Z in mid]
        for (x0, y0), (x1, y1), (X, Z) in zip(pts[:-1], pts[1:], mid[:-1]):
            k = kz(Z)
            sheet.line([(x0, y0), (x1, y1)], "#8a5a3c", max(0.8, 22 * k), 0.12)
            sheet.line([(x0 - 9 * k, y0 + 2 * k), (x1 - 9 * k, y1 + 2 * k)], "#f0d0a8", max(0.6, 5 * k), 0.16)   # the rut's sunny wall
    sheet_c, sheet_a = sheet.done()
    sheet_a *= lot_zone() * step(440, 452, y)
    over(back, sheet_c, sheet_a)
    # 4. stones and tufts on the lot, at a true density through the camera
    zone = lot_zone()
    sheet = Paper(SHAPE)
    for (px_, py_, k, r) in depth.scatter(pt, kk, (-1400, 1400, -40, 2600), 0.9, seed=2311, size=(7, 4, 7), zone=zone):
        rx = max(0.5, (3 + 6 * r) * k)
        ry = max(0.4, rx * 0.5)
        sheet.ellipse(px_ - rx * 1.2, py_ + ry * 0.2, rx * 1.6, ry * 0.8, "#6a5a86", 0.30)     # its shadow, to the left
        sheet.ellipse(px_, py_, rx, ry, mix("#b98c64", "#e6c8a0", r), 0.85)
        if rx > 1.4:
            sheet.ellipse(px_ + rx * 0.3, py_ - ry * 0.35, rx * 0.5, ry * 0.4, "#f6e2c0", 0.7)   # its sunny top
    for (px_, py_, k, r) in depth.scatter(pt, kk, (-1400, 1400, -40, 2000), 0.05, seed=2312, size=(30, 20, 30), zone=zone):
        tuft(sheet, px_, py_, max(1.5, (10 + 10 * r) * k), int(r * 1000))
    sc, sa = sheet.done()
    over(back, sc, sa * zone)
    # 5. air: the mesas and the far plain toward the sky's colour at the horizon, layer by layer
    sky_h = np.median(back[214:222, :, :].reshape(-1, 3), axis=0)
    band = step(206, 228, y) * (1 - step(298, 340, y))
    far = 0.22 + 0.14 * step(540, 640, x)                           # the farther mesas, right, deeper in the air
    keep = np.zeros(SHAPE, dtype=F32)
    for x0, y0, x1, y1 in ((16, 136, 140, 440), (122, 228, 352, 456), (296, 256, 312, 310), (330, 340, 380, 450),
                           (404, 306, 562, 500), (552, 284, 800, 450)):
        keep[y0:y1, x0:x1] = 1
    keep = np.clip(blur(keep, 2.0) * 1.4, 0, 1)
    depth.air(back, band * far, sky_h, amount=1.0, mask=1 - keep)
    # 6. the ground deepens toward us, and the bottom corners
    depth.frame(back, amount=0.10, bottom=0.10, color="#3a2630")
    return np.clip(back, 0, 1)


def finish(picture, path, colors, alpha=None, seed=7, speckle=0.014, amount=0.02, grained=True):
    g = grain(picture, seed, amount) if grained else picture
    sample = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample.reshape(-1, 1, 3)], colors=colors)
    idx = to_palette(g, pal, speckle=speckle)
    save(path, idx, pal, alpha)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(ORIG):                                       # every file as it was
        if f != "back.png":
            shutil.copyfile(os.path.join(ORIG, f), os.path.join(OUT, f))
    back, _ = load("back.png")
    back = deepen(back)
    finish(back, os.path.join(OUT, "back.png"), 152, speckle=0.008, grained=False)
    nc, na = near_plane()
    finish(nc, os.path.join(OUT, "near.png"), 40, na)
    comp = Image.open(os.path.join(OUT, "back.png")).convert("RGBA")
    for name in ("pump", "stand", "car", "front", "near"):
        comp.alpha_composite(Image.open(os.path.join(OUT, name + ".png")).convert("RGBA"))
    comp.convert("RGB").save(f"out/{SCENE}-depth-comp.png")
    print("near share", round(float((na > 0.5).mean()) * 100, 1), "%")

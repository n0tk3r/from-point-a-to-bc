#!/usr/bin/env python3
"""ROUND 23, the depth pass over the back of the limousine (nevada-limo): worked over the painting as it is.

Reads the full run of nevada_limo.py as kept in out/nevada-limo-orig/ and writes the scene's set back into out/nevada-limo/
(every file as before, plus near.png). The desert going by the windows is the engine's (drive-*.png: not touched here).

  NEAR   our own seat and its two armrests (front.png, its outline exactly as it was) made the nearest, deepest and
         warmest dark of the picture, with a lit rim along their tops where the window light catches them; and near.png,
         what was missing: the near corners of the cabin right over our heads, where the quilted headliner curves down
         into the pillars behind the side windows (off the top edge and a side edge each, a padded roll for an edge).
  BACK   the carpet's nap (the pile brushed lengthwise, lighter and darker where it lies differently, shrinking with
         distance) and its seams in perspective (two lengthwise, one across, lines that lead in to the divider); the sun,
         low on the car's right and a little behind (the drive's own: 0.36 m ahead and 1.95 m left for a metre of drop),
         falling through the two right panes onto the carpet's left half and the long seat's base, the pillar's shadow
         between; the soft light of the opposite panes along each seat's backrest and cushion; the near floor deeper and
         the far end of the cabin (the bar, the divider's frame, the far ends of the seats and the headliner) a step
         cooler and paler. Nothing clicked moves; nothing changes under the cut-outs on the seats.

    python3 nevada_limo_depth.py
"""
import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import F32, blur, lerp, rgb, grain, palette_of, to_palette, save
from room import View
import nevada_limo_model as M
import depth

SRC, OUT = os.environ.get("LIMO_SRC", "out/nevada-limo-orig"), os.environ.get("LIMO_OUT", "out/nevada-limo")
H, W = 600, 800
V = View(**M.VIEW)
LUM = np.array([0.299, 0.587, 0.114], F32)
F = V.F
SUN = (1.95, 0.36)                     # a centimetre's drop carries the light this far to the car's left (-X) and ahead (-Z)


def load(name):
    a = np.asarray(Image.open(f"{SRC}/{name}").convert("RGBA"), dtype=F32) / 255.0
    return a[..., :3].copy(), a[..., 3].copy()


def smooth(d, soft):
    """0 to 1 across a soft edge: d the signed distance inside, `soft` the half width (same units)."""
    t = np.clip(d / (2.0 * soft) + 0.5, 0, 1)
    return t * t * (3 - 2 * t)


def field(seed, sx, sz, X, Z, x0=40.0, z0=0.0):
    """Value noise laid on a level plane: cells `sx` across and `sz` along the car (cm), smoothly joined. 0 to 1."""
    rng = np.random.default_rng(seed)
    nx, nz = int(340 / sx) + 3, int(520 / sz) + 3
    g = rng.random((nz, nx)).astype(F32)
    u = np.clip((X - x0) / sx, 0, nx - 1.001)
    v = np.clip((Z - z0) / sz, 0, nz - 1.001)
    i, j = np.floor(u).astype(int), np.floor(v).astype(int)
    fu, fv = u - i, v - j
    fu, fv = fu * fu * (3 - 2 * fu), fv * fv * (3 - 2 * fv)
    return ((g[j, i] * (1 - fu) + g[j, i + 1] * fu) * (1 - fv) + (g[j + 1, i] * (1 - fu) + g[j + 1, i + 1] * fu) * fv).astype(F32)


def line_px(dist_cm, px_per_cm, width_cm):
    """A thin line on a plane, antialiased: as wide as it really is, never thinner than a pixel (then only fainter)."""
    wpx = width_cm * px_per_cm
    return (np.clip(1.0 - dist_cm * px_per_cm / np.maximum(wpx, 1.0), 0, 1) * np.minimum(wpx, 1.0)).astype(F32)


def panes_lit(Zw, Yw, soft=1.6, y_lo=None):
    """How much of a window point (Z along the wall, Y up it) is glass: the two panes, the pillar between them dark."""
    y0, y1 = M.WINDOW_Y
    if y_lo is not None:
        y0 = max(y0, y_lo)
    m = smooth(Yw - y0, soft) * smooth(y1 - Yw, soft)
    z = np.zeros_like(Zw)
    for z0, z1 in M.PANES["R"]:
        z = np.maximum(z, smooth(Zw - z0, soft) * smooth(z1 - Zw, soft))
    return (m * z).astype(F32)


# ---------------------------------------------------------------- the back
def deepen_back(back, keep):
    pic = back.copy()
    X, Z, okf = V.floor_xz((H, W))
    D = np.maximum(V.depth_map((H, W)), 1.0)
    k = F / D                                                         # pixels to a centimetre across, at that depth
    kz = V.eye * F / (D * D)                                          # pixels to a centimetre along the car, on the floor
    seat_d, wd = M.SEAT_D, M.W
    carpet = okf * smooth(X - (seat_d + 1.0), 0.6) * smooth((wd - seat_d - 1.0) - X, 0.6) \
        * smooth(Z - 45.0, 0.6) * smooth(395.0 - Z, 0.6)
    carpet = (carpet * (1 - keep)).astype(F32)

    # the nap: the pile brushed along the car lies lighter and darker in long soft drifts, and finer streaks in it
    far_px = D / F                                                    # centimetres a pixel spans across
    drift = field(41, 9.0, 30.0, X, Z) - 0.5
    drift2 = field(42, 4.0, 13.0, X, Z) - 0.5
    fine = field(43, 1.1, 5.0, X, Z) - 0.5
    fine_amt = np.clip(1.4 - far_px / 1.0, 0.2, 1.0)
    nap = 1.0 + 0.16 * drift + 0.10 * drift2 + 0.10 * fine * fine_amt
    # the seams: two lengthwise (where the runner meets the side pieces), one across, under the long pillar between the panes
    seams = np.zeros((H, W), F32)
    ridge = np.zeros((H, W), F32)
    for xs in (104.0, 262.0):
        seams = np.maximum(seams, line_px(np.abs(X - xs), k, 0.9))
        ridge = np.maximum(ridge, line_px(np.abs(X - (xs + (1.4 if xs < 182 else -1.4))), k, 1.0))
    zs = 232.0
    seams = np.maximum(seams, line_px(np.abs(Z - zs), kz, 0.9))
    ridge = np.maximum(ridge, line_px(np.abs(Z - (zs + 1.5)), kz, 1.0))
    tone = nap * (1 - 0.42 * seams) * (1 + 0.16 * ridge * (1 - seams))
    # the near floor deeper, the far floor paler (it was nearly flat from end to end)
    near = np.clip((Z - 200.0) / 195.0, 0, 1)
    tone = tone * (1 - 0.16 * near ** 1.3)
    pic = pic * lerp(np.ones_like(tone), tone, carpet)[..., None]

    # the sun through the two right panes: onto the carpet's left half, and low on the long seat's base. The facing
    # seat's backrest (its inner top edge, X = W - BACK_T, Y = BACK_H) cuts the lowest light off the panes.
    sx, sz = SUN
    y_clear = M.BACK_H + (M.BACK_T) / sx                              # the lowest window height whose light clears it
    Yw = (wd - X) / sx
    Zw = Z + sz * Yw
    sun_floor = panes_lit(Zw, Yw, y_lo=y_clear) * carpet * smooth(X - seat_d, 0.8)
    Xu, Yv, okw = V.plane_uv((H, W), "X", seat_d)                    # the long seat's base, toward the carpet
    Zf, Yf = Xu, Yv
    face = okw * smooth(Yf - 1.0, 0.8) * smooth(M.SEAT_H - 8.0 - Yf, 1.5) * smooth(Zf - 32.0, 1.0) * smooth(392.0 - Zf, 1.0)
    face = face * (X < seat_d + 0.5) * (1 - keep)                     # only where the floor behind it is under the seat
    Ywf = Yf + (wd - seat_d) / sx
    Zwf = Zf + sz * (wd - seat_d) / sx
    sun_face = panes_lit(Zwf, Ywf, y_lo=y_clear) * face
    sun = np.clip(blur(np.maximum(sun_floor, sun_face), 0.7), 0, 1)
    warm = rgb("#ffd6a0")
    pic = pic * (1 + 1.25 * sun[..., None] * warm) + 0.05 * sun[..., None] * warm
    # the sun's patch is bright: a little of it is thrown back up onto the long seat's base and the carpet round it
    glow = blur(sun, 14.0) * (1 - sun)
    pic = pic * (1 + 0.22 * glow[..., None] * rgb("#ffcf9c"))

    # the soft light of the opposite panes along each seat (the sky low over the desert, a broad light): bands on the
    # backrests' faces and on the cushions, each pane's own, the pillar's dark between
    soft_light = np.zeros((H, W), F32)
    for side in ("L", "R"):
        xb = M.BACK_T if side == "L" else wd - M.BACK_T
        Bu, Bv, okb = V.plane_uv((H, W), "X", xb)
        z_lo = 32.0 if side == "L" else 60.0
        back_face = okb * smooth(Bv - M.SEAT_H - 2.0, 2.0) * smooth(M.BACK_H - 2.0 - Bv, 2.0) * smooth(Bu - z_lo, 2.0) * smooth(392.0 - Bu, 2.0)
        X42, Z42, ok42 = V.floor_xz((H, W), Y=M.SEAT_H)
        if side == "L":
            cushion = ok42 * smooth(X42 - xb, 1.0) * smooth(seat_d - 1.0 - X42, 1.0)
            back_face = back_face * (X42 < xb + 0.5)
        else:
            cushion = ok42 * smooth(X42 - (wd - seat_d + 1.0), 1.0) * smooth(xb - X42, 1.0)
            back_face = back_face * (X42 > xb - 0.5)
        cushion = cushion * smooth(Z42 - z_lo, 2.0) * smooth(392.0 - Z42, 2.0)
        travel_b = (wd - 2 * M.BACK_T)
        acc = np.zeros((H, W), F32)
        for s in (0.06, 0.12, 0.18, 0.24):                           # the light from a little above the horizon, soft
            Ywb = Bv + travel_b * s
            acc += panes_lit(Bu - 0.1 * travel_b * s, Ywb, soft=9.0) * back_face
            travel_c = np.abs((wd - M.BACK_T if side == "L" else M.BACK_T) - X42)
            Ywc = M.SEAT_H + travel_c * (s + 0.18)
            acc += panes_lit(Z42 - 0.1 * travel_c * s, Ywc, soft=9.0) * cushion
        soft_light = np.maximum(soft_light, acc / 4.0 * (0.85 if side == "L" else 1.0))
    soft_light = blur(soft_light, 2.5) * (1 - keep)
    pic = pic * (1 + 0.34 * soft_light[..., None] * rgb("#f4ecff"))

    # the far end of the cabin a step cooler and paler: how far each ray goes inside the cabin's box before a wall
    dX, dY, dZ = V._rays((H, W))
    with np.errstate(divide="ignore", invalid="ignore"):
        ts = [np.where(dY < 0, (0.0 - V.eye) / dY, np.inf), np.where(dY > 0, (M.H - V.eye) / dY, np.inf),
              np.where(dX < 0, (0.0 - V.cam_x) / dX, np.inf), np.where(dX > 0, (wd - V.cam_x) / dX, np.inf),
              np.where(dZ < 0, (0.0 - V.cam_z) / dZ, np.inf)]
    t = np.minimum.reduce([np.where(np.isfinite(a) & (a > 0), a, np.inf) for a in ts])
    t = np.where(np.isfinite(t), t, 600.0).astype(F32)
    far = np.clip((t - 300.0) / 230.0, 0, 1) ** 1.2
    far = blur(far, 3.0) * (1 - 0.6 * keep)
    pic = depth.air(pic, far, "#aab4dc", amount=0.20)
    return np.clip(pic, 0, 1).astype(F32), carpet, sun


# ---------------------------------------------------------------- the near plane
def near_seats(col, a):
    """Our seat and its armrests: the nearest dark, deep and warm, their tops caught by the window light."""
    lum = col @ LUM
    base = depth.near_tone(np.array([0.30, 0.27, 0.30], F32), shade="#1e1618", k=0.66, warm=0.035)
    # keep the painter's modelling (the folds, the piping) but deeper and warmer
    rel = (lum / max(float(lum[a > 0.5].mean()), 1e-3))[..., None]
    out = lerp(col, base * rel, 0.72)
    out = out * np.array([1.03, 0.98, 0.93], F32)
    r = np.maximum(depth.rim(a, light=(0.5, -1.0), width=2.2), depth.rim(a, light=(-0.5, -1.0), width=2.2))
    r = np.clip(r * 1.4, 0, 1)
    out = lerp(out, rgb("#e6b88c") * np.clip(rel * 1.1, 0.7, 1.3), 0.5 * r[..., None])
    return np.clip(out, 0, 1).astype(F32)


def near_corners(back):
    """The near corners of the cabin over our heads: the headliner curving down into the pillars behind the side
    windows, quilted as the headliner is (nearer, so larger), with a padded roll along the inner edge."""
    py, px = np.mgrid[0:H, 0:W].astype(F32)
    a = np.zeros((H, W), F32)
    inner = np.zeros((H, W), F32)                                     # 0 at the outline, growing inward (px)
    shades = np.zeros((H, W), F32)
    for side in (0, 1):
        x = px if side == 0 else (W - 1 - px)
        ax, ay = (215.0, 160.0)
        f = np.sqrt(np.clip(x / ax, 0, None)) + np.sqrt(np.clip(py / ay, 0, None))
        m = smooth(1.0 - f, 0.004)
        # a rough distance inside the outline, in pixels (the gradient of f)
        gx = 0.5 / np.sqrt(np.maximum(x, 0.5) * ax)
        gy = 0.5 / np.sqrt(np.maximum(py, 0.5) * ay)
        dist = (1.0 - f) / np.sqrt(gx * gx + gy * gy)
        a = np.maximum(a, m)
        inner = np.where(m > 0.5, dist, inner)
    a = (a > 0.5).astype(F32)
    hl = back[4:70, 330:470].reshape(-1, 3).mean(axis=0)              # the headliner's own colour
    deep = depth.near_tone(hl, shade="#1e1618", k=0.70, warm=0.03)
    # the quilting, nearer than the headliner behind it: diamonds about 34 px, the stitching sunk, each diamond puffed
    u = (px + py) / 34.0
    v = (px - py) / 34.0
    du, dv = np.abs(u - np.round(u)), np.abs(v - np.round(v))
    stitch = np.clip(1 - np.minimum(du, dv) / 0.06, 0, 1)
    puff = np.minimum(du, dv) * 2.0                                   # 0 at a stitch, 1 in a diamond's middle
    tone = 0.80 + 0.30 * puff - 0.30 * stitch
    col = deep[None, None, :] * tone[..., None]
    # the padded roll along the inner edge: a lighter cylinder some 12 px across, its piping a thin dark line inside it
    roll = np.clip(1 - np.abs(inner - 7.0) / 7.0, 0, 1) * (inner < 15)
    col = col * (1 + 0.30 * roll[..., None]) * np.where((inner > 14) & (inner < 16.5), 0.75, 1.0)[..., None]
    # its rim: the light from the windows and the warm ground outside catch the roll's lower edge
    r = np.maximum(depth.rim(a, light=(1.0, 1.1), width=2.4), depth.rim(a, light=(-1.0, 1.1), width=2.4))
    col = lerp(col, rgb("#d8aa86"), np.clip(0.75 * r, 0, 0.75)[..., None])
    return np.clip(col, 0, 1).astype(F32), a


# ---------------------------------------------------------------- finishing, as the painter's own `finish`
def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.007, amount=0.008):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    n = min(colors, max(8, len(np.unique((sample_of.reshape(-1, 3) * 255).astype(np.uint8), axis=0))))
    pal = palette_of([sample_of.reshape(-1, 3)], colors=n)
    save(name, to_palette(g, pal, speckle=speckle), pal, alpha)


def main():
    os.makedirs(OUT, exist_ok=True)
    names = sorted(f for f in os.listdir(SRC) if f.endswith(".png"))
    back, _ = load("back.png")
    keep = np.zeros((H, W), F32)
    for n in names:
        if n.startswith(("ropes-", "bag", "juice", "clipboard")):
            _, al = load(n)
            keep = np.maximum(keep, al)
    keep = np.clip(blur((blur(keep, 2.0) > 0.02).astype(F32), 1.5) * 1.3, 0, 1)

    pic, carpet, sun = deepen_back(back, keep)
    finish(pic, f"{OUT}/back.png", 160)

    col, a = load("front.png")
    finish(near_seats(col, a), f"{OUT}/front.png", 64, a)

    ncol, na = near_corners(back)
    finish(ncol, f"{OUT}/near.png", 40, na)

    for n in names:                                                   # the other cut-outs, exactly as they were
        if n not in ("back.png", "front.png"):
            shutil.copyfile(f"{SRC}/{n}", f"{OUT}/{n}")
    for n in os.listdir(SRC):
        if not n.endswith(".png") and os.path.isfile(f"{SRC}/{n}"):
            shutil.copyfile(f"{SRC}/{n}", f"{OUT}/{n}")
    print("near share (near.png alone): %.1f%%" % (na.mean() * 100))
    if "--look" in sys.argv:
        comp = Image.open(f"{OUT}/back.png").convert("RGBA")
        for n in ("divider-up", "ropes-4", "bag", "juice", "clipboard", "front", "near"):
            comp.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
        comp.convert("RGB").save("out/nevada-limo-depth-look.png")


if __name__ == "__main__":
    main()

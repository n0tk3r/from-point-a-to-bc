"""The ducts, the fast depth pass (round twenty-three): over the painting as it is (out/office-ducts-orig/, the full run of
office_ducts.py, never changed), a front plane in the section's own manner and a deeper backdrop.

  near.png   the nearest, darkest things, cut by the section plane as an architect draws them: the floor deck above cut
             across the whole top of the frame (concrete topping over plywood, the cut hatched), the joists' cut ends
             under it (a crossed box each, the convention for a member cut through), the batt insulation between them
             cut along its edge (the batt's loop line), and at both sides a laminated girder cut deeper, the joists
             bearing on it. Warm deep shade; a lit rim on the side the light comes from (up from the duct and the rooms).
  back.png   the ceiling space falling into dark away from the duct (up toward the deck, down past the tiles, out into the
             shaft), the duct's inside lifted to be the brightest thing, its back wall a touch cooler and paler, its
             near lip deeper. Nothing clicked is moved or redrawn.
  fan-*      as they were (copied), and layout.json.

    python3 office_ducts_depth.py          -> out/office-ducts/ (then install.py office-ducts)
"""
import os
import shutil
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brush import F32, Sheet, blur, grain, lerp, noise, palette_of, rgb, save, to_palette  # noqa: E402
import depth  # noqa: E402

SRC = "out/office-ducts-orig"
OUT = "out/office-ducts"
H, W = 600, 800
YY, XX = np.mgrid[0:H, 0:W].astype(F32)


def load(name):
    a = np.asarray(Image.open(f"{SRC}/{name}.png").convert("RGBA"), dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def box(x0, y0, x1, y1, soft=6.0):
    """A soft-edged rectangle mask."""
    m = ((XX >= x0) & (XX < x1) & (YY >= y0) & (YY < y1)).astype(F32)
    return np.clip(blur(m, soft), 0, 1) if soft else m


# ============================================================== the front plane
DECK_B = 32          # the deck's underside, all across the top
JOIST_B = 90         # the joists' cut ends hang to here (78 over the intake and the shaft: their areas start there)
JOISTS = [65, 125, 186, 246, 306, 367, 427, 487, 548, 608, 668, 728]   # on the painted joists' own lines
GIRDER_L = (0, 38, 214)      # x0, x1, bottom
GIRDER_R = (760, 800, 250)


def near_plane():
    SH = "#2b1c12"       # a frankly warm shade: the key turns warm darks violet, so the near plane leans brown
    wood = depth.near_tone("#6a4c34", shade=SH, k=0.63, warm=0.06)
    wood_d = depth.near_tone("#4a3424", shade=SH, k=0.55, warm=0.05)
    conc = depth.near_tone("#5e5650", shade=SH, k=0.60, warm=0.05)
    batt = depth.near_tone("#b7717f", shade=SH, k=0.60, warm=0.04)
    batt_d = depth.near_tone("#8a5260", shade=SH, k=0.64, warm=0.03)
    rng = np.random.default_rng(1823)

    S = Sheet((H, W), ss=3)
    # -- the batt between the joists, against the deck: its cut edge ragged below (fibres), never holes
    pts = [(0, DECK_B - 2)]
    x = 0.0
    while x < W:
        x += rng.uniform(1.5, 4)
        pts.append((min(x, W), DECK_B + 17 + rng.uniform(-3.0, 3.0) + 1.5 * np.sin(x / 61.0)))
    pts += [(W, DECK_B - 2)]
    S.poly(pts, batt)
    # -- the deck: concrete topping over plywood, cut straight across the top
    S.poly([(0, 0), (W, 0), (W, 14), (0, 14)], conc)
    S.poly([(0, 14), (W, 14), (W, DECK_B), (0, DECK_B)], wood_d)
    # -- the joists' cut ends and the girders
    for jx in JOISTS:
        b = JOIST_B if 140 < jx < 640 else 77
        S.poly([(jx - 6, DECK_B - 1), (jx + 6, DECK_B - 1), (jx + 6, b), (jx - 6, b)], wood)
    for x0, x1, b in (GIRDER_L, GIRDER_R):
        S.poly([(x0, 0), (x1, 0), (x1, b), (x0, b)], wood_d)
    col, a = S.done()

    # -- the section's marks, drawn on a second sheet inside the cut shapes: hatching, crossed boxes, laminations, the loop
    M = Sheet((H, W), ss=3)
    hatch = lerp(conc, rgb("#9a8a78"), 0.35)
    for k in range(-20, W + 20, 6):                         # the topping: a fine 45-degree hatch with a little stipple
        M.line([(k, 0), (k + 14, 14)], hatch, 0.6, 0.55)
    for k in range(0, W, 3):
        if rng.random() < 0.5:
            M.ellipse(k + rng.uniform(0, 3), rng.uniform(2, 12), 0.6, 0.6, hatch, 0.6)
    ply = lerp(wood_d, rgb("#a07850"), 0.35)
    for yy in (18.5, 22.5, 26.5, 30.0):                            # the plywood's plies
        M.line([(0, yy), (W, yy)], ply, 0.5, 0.5)
    xline = lerp(wood, rgb("#b08860"), 0.50)
    for jx in JOISTS:
        b = JOIST_B if 140 < jx < 640 else 77
        M.line([(jx - 5, DECK_B + 1), (jx + 5, b - 1)], xline, 0.7, 0.75, round_ends=False)
        M.line([(jx + 5, DECK_B + 1), (jx - 5, b - 1)], xline, 0.7, 0.75, round_ends=False)
    lam = lerp(wood_d, rgb("#a07850"), 0.35)
    for x0, x1, b in (GIRDER_L, GIRDER_R):                   # the girders' laminations
        for yy in np.arange(DECK_B + 7, b - 3, 7.0):
            M.line([(x0 + 2, yy), (x1 - 2, yy)], lam, 0.6, 0.6, round_ends=False)
    fib = [lerp(batt, rgb("#d89aa4"), 0.30), batt_d]         # the batt's cut edge: fibres, light and dark, every way
    for _ in range(5200):
        fx, fy = rng.uniform(0, W), rng.uniform(DECK_B, DECK_B + 19)
        if fx < GIRDER_L[1] + 1 or fx > GIRDER_R[0] - 1 or min(abs(fx - j) for j in JOISTS) < 8:
            continue
        ang, ln = rng.uniform(0, np.pi), rng.uniform(1.5, 4.5)
        M.line([(fx, fy), (fx + ln * np.cos(ang), fy + ln * np.sin(ang))], fib[int(rng.random() < 0.5)], 0.5, 0.55,
               round_ends=False)
    mcol, ma = M.done()
    ma = ma * a
    col = col * (1 - ma[..., None]) + mcol * ma[..., None]

    # -- a little life in the dark: a soft fall of tone, darker up at the frame's very top and at its edges
    n = noise((H, W), 26, 1830)
    col = col * (0.92 + 0.12 * n[..., None])
    col = col * (1 - 0.18 * np.clip(1 - YY / 40.0, 0, 1))[..., None]
    # -- the lit rim: the light comes up from the duct's inside and the rooms (from below, a little from the left: the intake)
    r = depth.rim(a, light=(-0.35, 1.0), width=2.0)
    warm = rgb("#d8b48a")
    col = col * (1 - 0.42 * r[..., None]) + warm * 0.42 * r[..., None]
    return np.clip(col, 0, 1).astype(F32), np.clip(a, 0, 1).astype(F32)


# ============================================================== the backdrop
def deepen(back):
    pic = back.copy()
    inside = np.clip(blur(((XX >= 128) & (XX < 644) & (YY >= 353) & (YY < 484)).astype(F32), 5), 0, 1)
    # -- the ceiling space over the duct, falling into dark up toward the deck (away from the duct's top at 346)
    over = ((XX >= 125) & (XX < 646) & (YY < 346)).astype(F32)
    up = np.clip((346 - YY) / 346.0, 0, 1) ** 0.9
    dark = over * (0.32 * up)
    # -- under the duct: the tiles' backs and the rooms, a little darker the farther down
    down = np.clip((YY - 492) / 108.0, 0, 1) ** 1.2 * (XX < 646)
    dark = dark + 0.16 * down
    # -- the shaft at the right: darker out toward the frame's edge (away from the duct)
    side = np.clip((XX - 650) / 150.0, 0, 1) ** 1.3
    dark = dark + 0.14 * side
    dark = blur(dark, 4) * (1 - inside)
    shade = rgb("#1c1828")
    pic = pic * (1 - dark[..., None]) + shade * dark[..., None] * 0.35 + pic * dark[..., None] * 0.65 * 0.55
    # -- the duct's inside: the brightest thing (a lift, warm a little, most in its middle)
    pool = inside * (0.65 + 0.35 * np.exp(-(((XX - 390) / 260.0) ** 2) - (((YY - 420) / 90.0) ** 2)))
    lift = rgb("#fff4e0")
    pic = pic + (lift - pic) * (0.13 * pool)[..., None]
    # -- its back wall a touch cooler and paler; its near lip (the floor's front edge) deeper
    wall = inside * np.clip((462 - YY) / 20.0, 0, 1)
    pic = pic + (rgb("#dfe6ea") - pic) * (0.05 * wall)[..., None]
    lip = np.clip(blur(((XX >= 0) & (XX < 646) & (YY >= 478) & (YY < 494)).astype(F32), 2), 0, 1)
    pic = pic * (1 - 0.10 * lip[..., None])
    return np.clip(pic, 0, 1).astype(F32)


def finish_back(pic, path):
    g = grain(pic, 7, 0.004)
    pal = palette_of([g.reshape(-1, 3)], colors=160)
    save(path, to_palette(g, pal, speckle=0.005), pal)


def finish_cut(col, alpha, path, colors=48):
    g = grain(col, 7, 0.011)
    sample = g[alpha > 0.5]
    pal = palette_of([sample.reshape(-1, 3)], colors=colors)
    save(path, to_palette(g, pal, speckle=0.007), pal, alpha)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back")
    finish_back(deepen(back), f"{OUT}/back.png")
    col, a = near_plane()
    finish_cut(col, a, f"{OUT}/near.png")
    for nm in os.listdir(SRC):                                   # the fan's frames and layout.json, as they were
        if nm != "back.png":
            shutil.copyfile(f"{SRC}/{nm}", f"{OUT}/{nm}")
    print("near share", round(float((a > 0.5).mean()) * 100, 1), "%; files", sorted(os.listdir(OUT)))

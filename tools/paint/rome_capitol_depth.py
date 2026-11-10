"""The Capitol's depth pass (round twenty-three, wave two: DEPTH.md, "The three planes"). It works over the painting as
rome_capitol.py makes it (copied, unchanged, to out/rome-capitol-orig/) and writes the scene's full set back into
out/rome-capitol/, every file as before plus near.png.

  near.png   the front plane. The end column of the portico by the gate, on our right, 3.2 m off and 1.7 m to the
             right of the lens: the left half of its plain stuccoed shaft up the right edge of the frame, its Tuscan
             capital and the end of its architrave in the top right corner, over the temple's corner; in the gate's
             shade, a warm rim on its left edge where the sunlit paving throws light back at it. And a bough of a
             stone pine that stands outside the picture on our left, across the top left corner over the sky: dark
             tufts of needles, their tips caught by the sun (on our right, low in the east-south-east).
  back.png   the paving deepened toward us and paled toward the temple, worn patches, chips and a few spring tufts in
             the joints scattered through the camera (few and large near, many and small far off), the long shadow of
             an honorary statue standing off the right edge laid across the far paving the way the scene's shadows
             run (to the left and a little away: rome_capitol_kit.CAST), and the city over the parapet moved toward the
             sky's colour, layer by layer, the hill across the river most.
  the rest   the cut-outs, the geese's frames and layout.json, as they were.

    python3 rome_capitol_depth.py      (light: a few seconds)
"""

import os
import shutil

import numpy as np
from PIL import Image
from scipy import ndimage

from brush import F32, Sheet, blur, grain, grid, lerp, mask_poly, noise, palette_of, rgb, save, to_palette
import depth
from rome_capitol_kit import CAST, EYE, FOC, P, SHAPE, k_at

ORIG, OUT = "out/rome-capitol-orig", "out/rome-capitol"
H, W = SHAPE
SEED = 1830


def load(name):
    a = np.asarray(Image.open(f"{ORIG}/{name}").convert("RGBA"), dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


# ---------------------------------------------------------------- the backdrop, deepened
PAVING = [(0, 600), (800, 600), (800, 322), (478, 326), (483, 332), (477, 450), (214, 450), (228, 431), (0, 431)]   # the walk, to the frame
VIEW = [(-4, 196), (212, 196), (212, 434), (-4, 434)]                                                             # the city over the parapet
HORIZON_SKY = "#b7ccd9"                                                                                           # the sky low over the hills


def hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def block_shadow(X0, X1, Z0, Z1, h0, h1):
    """The shadow on the paving of an upright block (world cm) from height h0 to h1: its corners pushed along CAST."""
    pts = [(X + CAST[0] * h, Z + CAST[1] * h) for X in (X0, X1) for Z in (Z0, Z1) for h in (h0, h1)]
    return hull(pts)


def deepen_back(back):
    x, y = grid(SHAPE)
    pave = mask_poly(SHAPE, PAVING, soft=2.0)
    t = np.clip((y - 322.0) / (600.0 - 322.0), 0, 1)
    # the paving: deeper and warmer toward us, paler toward the temple
    near_k = (0.50 * t ** 1.5 * pave)[..., None]
    back[...] = lerp(back, back * np.array([0.80, 0.71, 0.63], dtype=F32), near_k)
    depth.air(back, (1 - t) ** 2.2, rgb("#f1e6cf"), amount=0.16, mask=pave)

    # worn patches, chips and tufts on the paving, through the camera
    zone = blur((pave > 0.99).astype(F32), 1.0)
    pt = lambda X, Z: P(X, 0.0, Z)
    kk = lambda X, Z: k_at(Z)
    dark, light = Sheet(SHAPE), Sheet(SHAPE)
    for (px, py, k, r) in depth.scatter(pt, kk, (-2600, 2600, 860, 6200), 0.45, SEED, size=(30, 30), zone=zone):
        fore = EYE * k / FOC                                         # how flat a round thing lies on the paving here
        rx = (10 + 24 * r) * k
        (dark if r < 0.62 else light).ellipse(px, py, rx, max(rx * fore, 0.5), "#ffffff", 0.35 + 0.35 * (r % 0.3) / 0.3)
    back[...] = back * (1 - 0.13 * dark.done()[1][..., None])
    back[...] = lerp(back, np.clip(back * 1.07 + 0.015, 0, 1), 0.8 * light.done()[1][..., None])
    chips = Sheet(SHAPE)
    for (px, py, k, r) in depth.scatter(pt, kk, (-2600, 2600, 860, 6200), 0.5, SEED + 1, size=(4, 4), zone=zone):
        s = max((1.4 + 2.4 * r) * k, 0.45)
        chips.ellipse(px - s * 0.45, py + s * 0.2, s, s * 0.55, "#6a5560", 0.40)        # its shadow side, away from the sun
        chips.ellipse(px + s * 0.25, py - s * 0.1, s * 0.6, s * 0.40, "#f3e3bf", 0.45)  # lit on the right
    chips.onto(back, 0.7)
    tufts = Sheet(SHAPE)
    for (px, py, k, r) in depth.scatter(pt, kk, (-2600, 2600, 860, 4200), 0.05, SEED + 2, size=(10, 10), zone=zone):
        hgt = (6 + 8 * r) * k
        for i in range(5):
            a = -0.9 + 0.45 * i + (r - 0.5) * 0.3
            tufts.line([(px + (i - 2) * 0.6 * k, py), (px + (i - 2) * 0.6 * k + a * hgt * 0.5, py - hgt * (0.7 + 0.3 * ((i * 7 + r * 10) % 1)))],
                       "#7e8a45" if i % 2 else "#a3a456", max(0.9 * k * 2, 0.6), 0.85)
        tufts.ellipse(px - 1.2 * k * 4, py + 0.4, 3.2 * k * 4, 0.9 * k * 4 * EYE * k / FOC + 0.4, "#4c3f52", 0.35)
    tufts.onto(back)

    # an honorary statue off the right edge, on its base: its long shadow across the far paving, in front of the chariot
    X, Z = 1135.0, 2204.0
    for poly, amt in ((block_shadow(X - 110, X + 110, Z - 95, Z + 95, 0, 190), 0.46),     # the base
                      (block_shadow(X - 34, X + 34, Z - 22, Z + 22, 190, 400), 0.46),     # the figure
                      (block_shadow(X - 16, X + 16, Z - 14, Z + 14, 400, 434), 0.46),     # the head
                      (block_shadow(X + 22, X + 40, Z - 8, Z + 8, 300, 420), 0.40)):      # a raised arm
        depth.shadow_on_ground(back, pt, poly, color="#5d5a8c", amount=amt, soft=1.2, wobble=0.6, seed=SEED, ground=pave)

    # the city below, layer on layer toward the sky: the far hill most
    view = mask_poly(SHAPE, VIEW, soft=3.0)
    far = np.clip((434.0 - y) / (434.0 - 232.0), 0, 1) ** 0.9
    depth.air(back, far, HORIZON_SKY, amount=0.30, mask=view)
    return back


# ---------------------------------------------------------------- the front plane
SHADE = "#2e2129"                                  # the near plane's shade: deep and warm
STONE = "#e8dcc4"                                  # the column's stucco (the temple's, near)
BOUNCE = "#ffdcaa"                                 # light thrown back off the sunlit paving
XA = 842.0                                         # the column's axis in the picture (its foot is below the frame: 3.2 m off)


def near_col(c, k=0.62, warm=0.07):
    return depth.near_tone(c, SHADE, k, warm)


def column():
    """The portico's end column: the shaft (its left half, up the right edge), the capital, the end of the architrave."""
    x, y = grid(SHAPE)
    col = np.zeros((H, W, 3), F32)
    a = np.zeros(SHAPE, F32)
    r = np.where(y > 150, 74.0 + 10.0 * np.clip((y - 150) / 450.0, 0, 1), 74.0)          # the shaft tapers a little upward
    u = (x - XA) / r                                                                        # -1 at its left limb
    shaft = (u > -1.0) & (y >= 146)
    core, mid, limb = rgb("#3e2924"), rgb("#684738"), rgb("#94694f")                     # the stucco in the gate's shade: frankly warm
    stone = mid
    mott = (noise(SHAPE, 34, SEED + 3, 4) - 0.5) * 0.12 + (noise(SHAPE, 9, SEED + 4, 3) - 0.5) * 0.06
    streak = np.clip((noise((H, W), 60, SEED + 5, 3) - 0.55) * 3.0, 0, 1) * 0.10
    side = np.clip((-u - 0.40) / 0.60, 0, 1)                                                # 0 toward its front (off the frame), 1 at the limb
    c = lerp(core[None, None, :], mid[None, None, :], (side ** 1.4)[..., None])
    c = lerp(c, limb[None, None, :], (side ** 7)[..., None]) * (1 + mott - streak)[..., None]
    c = lerp(c, np.clip(c * np.array([1.30, 1.06, 0.86], F32) + 0.03, 0, 1), (0.55 * np.clip((y - 430) / 170.0, 0, 1) * side ** 2)[..., None])   # warm light from the paving, low down
    col = np.where(shaft[..., None], c, col)
    a = np.where(shaft, 1.0, a)
    # the capital: a necking band, the echinus swelling out, the square abacus; then the architrave's end above
    for (y0, y1, half, t) in ((140, 146, 75.0, 0.62), (134, 140, 77.0, 1.18), (110, 134, None, 0.95), (92, 110, 101.0, 1.0)):
        rows = (y >= y0) & (y < y1)
        if half is None:
            hw = 77.0 + 22.0 * np.clip((134.0 - y) / 24.0, 0, 1) ** 1.6
        else:
            hw = half
        m = rows & (x > XA - hw)
        under = np.clip((y - y0) / max(y1 - y0, 1), 0, 1)
        cc = stone[None, None, :] * (t * (1 - 0.35 * under) * (1 + mott))[..., None]
        col = np.where(m[..., None], cc, col)
        a = np.where(m, 1.0, a)
    arch = (y < 92) & (x > XA - 96.0)
    fasc = 1.0 - 0.10 * ((y > 54) & (y < 92)) - 0.05 * ((y > 26) & (y < 54))
    shadow_line = 1.0 - 0.35 * (np.abs(y - 54) < 1.6) - 0.25 * (np.abs(y - 26) < 1.4)
    soffit = 1.0 - 0.30 * ((y >= 84) & (y < 92))                                           # its underside, seen from below
    end = 1.0 + 0.10 * (x < XA - 84.0)                                                     # the end face turns to the open precinct
    cc = lerp(core, mid, 0.55)[None, None, :] * (fasc * shadow_line * soffit * end * (1 + mott))[..., None]
    col = np.where(arch[..., None], cc, col)
    a = np.where(arch, 1.0, a)
    return col, a


TUFTS = [(-8, 140, 40), (-6, 96, 44), (8, 44, 46), (40, 120, 38), (60, 80, 42), (66, 24, 40), (104, 98, 34), (118, 52, 40),
         (126, 8, 34), (156, 74, 32), (176, 24, 34), (210, 56, 28), (226, 14, 30), (268, 36, 24), (300, 8, 24), (336, 22, 18),
         (360, 0, 18), (20, 172, 26)]
LIMB = [(-14, 70), (40, 58), (96, 44), (150, 34), (210, 22), (270, 12), (330, 4), (390, -2)]


def pine():
    """A bough of a stone pine standing outside the picture on our left: its limb along the top, tufts of long needles
    hanging from it, dark (we see their shaded undersides), the sun on the tips that face it (right and above)."""
    rng = np.random.default_rng(SEED + 7)
    sh = Sheet(SHAPE)
    bark = near_col("#6e5040", 0.62, 0.03)                         # the plated bark, in shade
    sh.taper(LIMB, bark, 15.0, 5.0)
    for (tx, ty, R) in TUFTS:                                         # twigs from the limb to every tuft
        lx = min(max(tx, LIMB[0][0]), LIMB[-1][0])
        ly = float(np.interp(lx, [p[0] for p in LIMB], [p[1] for p in LIMB]))
        sh.taper([(lx, ly), ((lx + tx) / 2 + 4, (ly + ty) / 2 - 3), (tx, ty)], bark, 5.0, 2.4)
    deep_, mid_ = near_col("#264429", 0.40, 0.04), near_col("#4f773e", 0.28, 0.04)
    for (tx, ty, R) in TUFTS:                                         # the dark body of each tuft
        sh.ellipse(tx, ty + R * 0.12, R * 0.80, R * 0.62, deep_)
    for (tx, ty, R) in TUFTS:                                         # the needles, hanging and spreading
        for i in range(int(R * 2.6)):
            ang = rng.uniform(0.15, np.pi - 0.15) if rng.random() < 0.75 else rng.uniform(-np.pi, 0)
            L = R * rng.uniform(0.80, 1.25)
            x0, y0 = tx + rng.normal(0, R * 0.12), ty + rng.normal(0, R * 0.10)
            toward = np.cos(ang) * 0.85 - np.sin(ang) * 0.30           # needles pointing right are the ones nearer the sun
            tone = mid_ if rng.random() < 0.18 + 0.30 * max(toward, 0) else deep_
            sh.line([(x0, y0), (x0 + np.cos(ang) * L, y0 + np.sin(ang) * L * 0.9)], tone, rng.uniform(1.0, 1.8))
    c, a = sh.done()
    solid = a > 0.5
    closed = ndimage.binary_closing(solid, structure=np.ones((5, 5)), iterations=1)          # no small holes of sky inside
    filled = ndimage.binary_fill_holes(closed)
    gap = filled & ~solid
    c = np.where(gap[..., None], deep_[None, None, :], c)
    a = np.where(gap, 1.0, a)
    # the sun on the tips facing it (right and above), and a little bark lit along the limb's upper edge
    rimm = depth.rim(a, light=(0.85, -0.55), width=3.2)
    lit = rgb("#d6cc6c")
    tex = noise(SHAPE, 6, SEED + 8, 3)
    c = lerp(c, lit[None, None, :], (np.clip(rimm * 2.2, 0, 1) * (0.40 + 0.60 * tex))[..., None] * 0.80)
    return c, a


def near_plane():
    cc, ca = column()
    pc, pa = pine()
    rimm = depth.rim(ca, light=(-1.0, -0.15), width=2.4)
    cc = lerp(cc, rgb(BOUNCE)[None, None, :] * 0.92, (np.clip(rimm * 1.5, 0, 1) * 0.75)[..., None])
    a = np.maximum(ca, pa)
    c = np.where((pa > ca)[..., None], pc, cc)
    return np.clip(c, 0, 1).astype(F32), a.astype(F32)


# ---------------------------------------------------------------- finish
def finish(picture, path, colors, alpha=None, seed=7, amount=0.02, speckle=0.014):
    g = grain(picture, seed, amount)
    sample = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample.reshape(-1, 1, 3)], colors=colors)
    save(path, to_palette(g, pal, speckle=speckle), pal, alpha)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name in os.listdir(ORIG):                                      # the cut-outs, the geese, layout.json: as they were
        if name not in ("back.png", "near.png"):
            shutil.copy2(f"{ORIG}/{name}", f"{OUT}/{name}")
    back, _ = load("back.png")
    back = deepen_back(back)
    finish(back, f"{OUT}/back.png", 160, amount=0.010)
    nc, na = near_plane()
    finish(nc, f"{OUT}/near.png", 64, (na > 0.5).astype(F32), seed=11)
    print("near covers", round(float((na > 0.5).mean()) * 100, 1), "% of the picture")
    comp = Image.open(f"{OUT}/back.png").convert("RGBA")
    for name in ("altar", "chariot", "world", "parapet", "hut", "pen", "tablets", "near"):
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(f"{OUT}-depth-comp.png")

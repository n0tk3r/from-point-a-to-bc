"""home-study, the depth pass (round twenty-three): Dad's study under the roof at night, worked over its own painting.

    python3 home_study_depth.py      reads out/home-study-orig/ (the full run of home_study.py, unkeyed), writes
                                     out/home-study/ again: every file as before, plus near.png

One camera: the room's own (room.View with home_study_model.VIEW), so the near rafters are where the painting has them.

  near.png   the front plane that was missing: the two nearest rafters of each slope, cut off by the top corners of the
             frame (within a metre or two of the lens, above our heads), in deep warm shade with the lamps' light along
             their under edges; and the floor at the bottom of the frame in the heap's own shadow (the lamps are beyond
             the heap, so its shade falls toward us). Nobody stands on that floor (it is below the walk).
  front.png  the door's wall, frame and leaf and the heap of trip things: the same outline exactly, made to count:
             darker and warmer, a lit rim on the side the room's lamps are.
  back.png   the far gable wall a little cooler and paler (air), the lamps' pools warmer, the near floor deeper.
  the rest   copied as they were.
"""
import math, os, shutil
import numpy as np
from PIL import Image

from brush import F32, blur, lerp, rgb, mask_poly, to_palette, save, grain
import depth
from room import View
import home_study_model as M
from home_study import palette_for

SRC, OUT = "out/home-study-orig", "out/home-study"
H, W = 600, 800
V = View(**M.VIEW)

DEEP = rgb("#2c1a10")           # the near plane's shade: a frankly warm deep brown (install.py turns warm darks violet)
LAMP = rgb("#ffb866")           # the lamps' light on a near edge
AIR = rgb("#a9b6d2")            # the night's cool at the far end (the window's blue, paled)

# the walk's near edge, (226, 473) to (718, 497): nobody's feet are below it
def walk_edge(x):
    return 473 + (np.asarray(x, dtype=F32) - 226) * (24 / 492)

HEAP = [[262, 530], [296, 522], [304, 500], [352, 498], [362, 466], [477, 466], [480, 505], [492, 500], [565, 458],
        [602, 462], [604, 512], [630, 512], [636, 524], [710, 524], [710, 558], [640, 600], [262, 600]]


def load(name):
    im = Image.open(os.path.join(SRC, name)).convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255.0
    return a[..., :3].copy(), (a[..., 3] > 0.5).astype(F32)


def rafter_mask(side, z):
    """The picture shape of one rafter (12 cm deep, 5.6 cm thick) of the roof's `side` slope at Z = z."""
    Wd, K, R = M.W, M.KNEE, M.RIDGE
    run, rise = Wd / 2, R - K
    L = math.hypot(run, rise)
    if side == "L":
        a, b, n = (0.0, K), (run, R), (rise / L, -run / L)
    else:
        a, b, n = (Wd, K), (run, R), (-rise / L, -run / L)
    m = np.zeros((H, W), dtype=F32)
    for dz in (-2.8, 2.8):                                   # its two faces and its under side, each a polygon
        for quad in ([(a[0], a[1], z + dz), (b[0], b[1], z + dz), (b[0] + 12 * n[0], b[1] + 12 * n[1], z + dz),
                      (a[0] + 12 * n[0], a[1] + 12 * n[1], z + dz)],
                     [(a[0] + 12 * n[0], a[1] + 12 * n[1], z - 2.8), (b[0] + 12 * n[0], b[1] + 12 * n[1], z - 2.8),
                      (b[0] + 12 * n[0], b[1] + 12 * n[1], z + 2.8), (a[0] + 12 * n[0], a[1] + 12 * n[1], z + 2.8)]):
            p = V.poly(quad)
            if len(p) >= 3:
                m = np.maximum(m, mask_poly((H, W), p))
    return (m > 0.5).astype(F32)


def finish(pic, name, colors, alpha=None, amount=0.0):
    if amount:
        pic = grain(pic, 7, amount)
    sample = pic if alpha is None else pic[alpha > 0.5]
    pal = palette_for(sample, colors)
    idx = to_palette(np.clip(pic, 0, 1), pal, speckle=0.007)
    save(name, idx, pal, alpha)


def main():
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back.png")
    front, fa = load("front.png")
    y, x = np.mgrid[0:H, 0:W].astype(F32)

    # ------------------------------------------------------------------ back: air at the far end, the pools, the near floor
    gable = [(0, 0, 0), (M.W, 0, 0), (M.W, M.KNEE, 0), (M.W / 2, M.RIDGE, 0), (0, M.KNEE, 0)]
    far = blur(mask_poly((H, W), V.poly(gable)), 3.0)
    win = mask_poly((H, W), [(399, 172), (488, 172), (488, 272), (399, 272)], soft=4)
    far = far * (1 - 0.6 * win)                                            # the moonlit window keeps its night
    vp = np.hypot((x - 400) / 1.3, (y - 230)) / 260.0                     # the far ends of the slopes and the floor
    far = np.maximum(far, np.clip(1 - vp, 0, 1) ** 2 * 0.6)
    b = lerp(back, AIR, (far * 0.13)[..., None])
    b = b * (1 + 0.06 * far[..., None])                                   # paler, a little
    # the lamps' pools: the desk lamp on the wall and corkboard, the shelf lamp on the floor and the shelves' end
    def pool(cx, cy, rx, ry, k):
        r = np.hypot((x - cx) / rx, (y - cy) / ry)
        return (np.clip(1 - r, 0, 1) ** 1.6 * k)[..., None]
    p = pool(300, 262, 95, 70, 0.20) + pool(668, 410, 170, 62, 0.20) + pool(330, 410, 150, 45, 0.12)
    b = b + (LAMP * b * 0.9 + LAMP * 0.05) * p                            # warm light laid on the lit colour
    # the near floor deeper and warmer
    t = np.clip((y - 455) / 145.0, 0, 1) ** 1.2
    b = lerp(b, b * np.array([0.78, 0.66, 0.58], F32), (t * 0.75)[..., None])
    back2 = np.clip(b, 0, 1).astype(F32)

    # ------------------------------------------------------------------ front.png: the same outline, darker and warmer
    lum = front @ np.array([0.3, 0.55, 0.15], F32)
    k = np.clip(0.52 + (lum - 0.35) * 0.3, 0.46, 0.68)                   # the light leaf keeps some of its light
    f = lerp(front, DEEP, k[..., None])
    f[..., 0] = np.clip(f[..., 0] * 1.06, 0, 1)
    rim_f = depth.rim(fa, light=(0.35, -1.0), width=2.2) * 0.75
    f = lerp(f, np.clip(front * 0.6 + LAMP * 0.55, 0, 1), rim_f[..., None])
    front2 = f

    # ------------------------------------------------------------------ near.png: the rafters and the heap's shadow
    rafters = {}
    for side, z in (("R", 1110), ("L", 990)):
        rafters[(side, z)] = rafter_mask(side, z)
    raf = np.zeros((H, W), F32)
    for m in rafters.values():
        raf = np.maximum(raf, m)
    na = raf.copy()
    nrgb = lerp(back2, DEEP, 0.68)
    nrgb[..., 0] = np.clip(nrgb[..., 0] * 1.08, 0, 1)
    # the grain of the wood along them, a little: keep the painting's own marks
    nrgb = nrgb + (back2 - blur(back2, 2.0)) * 0.5
    for (side, z), m in rafters.items():
        lit = depth.rim(m, light=(-0.55, 1.0) if side == "R" else (0.55, 1.0), width=3.0)
        nrgb = lerp(nrgb, np.clip(back2 * 0.5 + LAMP * 0.6, 0, 1), (lit * 0.7)[..., None])

    # the floor in the heap's shadow, below the walk: seamless at its top (it starts as the backdrop itself)
    heap = mask_poly((H, W), HEAP)
    for y0 in range(598, 497, -2):                         # only as much of it as makes the heap read as one near mass
        top = np.maximum(walk_edge(x) + 10, y0)
        if (heap * np.maximum(fa, (y >= top) * heap)).sum() / heap.sum() >= 0.74:
            break
    below = (y >= top).astype(F32)
    floor = heap * below * (1 - fa)
    deep = np.clip((y - top) / 34.0, 0, 1)
    shade = lerp(back2, back2 * np.array([0.42, 0.34, 0.30], F32) + DEEP * 0.25, (deep * 0.85)[..., None])
    nrgb = np.where(floor[..., None] > 0.5, shade, nrgb)
    na = np.maximum(na, floor)

    # ------------------------------------------------------------------ measure, as depth_check will
    allnear = np.maximum(fa, na)
    print("near share %.1f%%" % (allnear.mean() * 100), " heap covered %.0f%%" % ((heap * allnear).sum() / heap.sum() * 100))

    # ------------------------------------------------------------------ back to palettes
    finish(back2, f"{OUT}/back.png", 160)
    finish(front2, f"{OUT}/front.png", 96, fa)
    finish(np.clip(nrgb, 0, 1), f"{OUT}/near.png", 96, na, amount=0.006)
    for n in os.listdir(SRC):
        if n not in ("back.png", "front.png", "near.png"):
            shutil.copy(os.path.join(SRC, n), os.path.join(OUT, n))
    print("written", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()

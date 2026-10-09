"""Round four, the proof: back.png before and after the moving things were taken out differ only where they were.

  python3 rome_steps_check4.py OLD_DIR NEW_DIR [OUT.png]

Every changed pixel must lie inside the place of one of the things taken out (each pigeon with its shadow, each
swallow, the hens inside their cage, the altar's smoke, the hill's smoke). Prints what changed where, and draws the
changes (red) over the new picture with the places (green) to look at. Every other file must be byte for byte the
same, except the new ones (cage.png and the frames) and layout.json."""

import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

import rome_steps as R
from brush import curve, mask_line

old_dir, new_dir = sys.argv[1], sys.argv[2]
out_png = sys.argv[3] if len(sys.argv) > 3 else None
P = R.T.pt
H, W = 600, 800

places = []                                                   # (name, x0, y0, x1, y1)
for i, (bx, by, sz, f, pk) in enumerate(R.PAVEMENT_PIGEONS):
    places.append((f"pigeon {i + 1}", bx - 1.8 * sz - 3, by - 1.2 * sz - 2, bx + 1.2 * sz + 2, by + sz * 0.3 + 3))
for (u_, k_, sz, f, pk) in R.STEP_PIGEONS:
    bx, by = P(u_, R.VK(k_) + 20, k_ * R.RISE)
    places.append((f"step pigeon u{u_}", bx - 1.8 * sz - 3, by - 1.2 * sz - 2, bx + 1.2 * sz + 2, by + sz * 0.3 + 3))
for gu, f in R.GUTTER_PIGEONS:
    gx, gy = P(gu, R.FV - R.EAVE, R.E3)
    places.append((f"gutter pigeon u{gu}", gx - 8, gy - 8, gx + 8, gy + 2))
for (bx, by, sz, t) in R.SWALLOWS:
    places.append((f"swallow {bx},{by}", bx - sz - 2, by - sz - 2, bx + sz + 2, by + sz * 0.4 + 2))
cu0, cu1, ck = R.CAGE
a0, a1 = P(cu0, R.VK(ck) + 4, ck * R.RISE), P(cu1, R.VK(ck) + 4, ck * R.RISE)
places.append(("hens in the cage", a0[0] - 8, a0[1] - 28, a1[0] + 4, a0[1] + 2))

au0, au1, av0, av1, ahh = R.ALTAR
sx, sy = P((au0 + au1) / 2, (av0 + av1) / 2, ahh + 6)
smoke = mask_line((H, W), curve([(sx + dx, sy + dy) for dx, dy in R.ALTAR_SMOKE], 6), 28, soft=0) > 0.01      # (generously wide: the
hill = mask_line((H, W), curve(R.HILL_SMOKE, 6), 16, soft=0) > 0.01                                          #  painted wisps wander)

ok = smoke | hill
for name, x0, y0, x1, y1 in places:
    ok[max(0, int(math.floor(y0))):min(H, int(math.ceil(y1)) + 1), max(0, int(math.floor(x0))):min(W, int(math.ceil(x1)) + 1)] = True

moved_png = os.path.join(os.path.dirname(new_dir.rstrip("/")), "rome-steps-moved.png")
moved = np.asarray(Image.open(moved_png)) > 0 if os.path.exists(moved_png) else None   # written by rome_steps.py: every pixel the
                                                                                        # moving things touched, before the finish
old = np.asarray(Image.open(f"{old_dir}/back.png"))
new = np.asarray(Image.open(f"{new_dir}/back.png"))
same_palette = Image.open(f"{old_dir}/back.png").getpalette() == Image.open(f"{new_dir}/back.png").getpalette()
changed = old != new
stray = changed & ~ok
print(f"palette the same: {same_palette}")
print(f"pixels changed: {int(changed.sum())}; outside the boxes round the things taken out: {int(stray.sum())}")
if moved is not None:
    stray = changed & ~moved
    print(f"changed where the moving things never touched the picture (must be 0): {int(stray.sum())}  (they touched {int(moved.sum())} px)")
for name, x0, y0, x1, y1 in places:
    box = changed[max(0, int(y0)):int(y1) + 1, max(0, int(x0)):int(x1) + 1]
    print(f"  {name:22s} {int(box.sum()):5d} px changed")
print(f"  {'altar smoke':22s} {int((changed & smoke).sum()):5d} px changed")
print(f"  {'hill smoke':22s} {int((changed & hill).sum()):5d} px changed")

for f in sorted(os.listdir(old_dir)):
    if f in ("back.png", "layout.json") or not f.endswith(".png"):
        continue
    a, b = open(f"{old_dir}/{f}", "rb").read(), open(f"{new_dir}/{f}", "rb").read() if os.path.exists(f"{new_dir}/{f}") else None
    print(f"  {f:14s} {'byte for byte the same' if a == b else 'CHANGED'}")

if out_png:
    im = Image.open(f"{new_dir}/back.png").convert("RGB")
    px = np.asarray(im).copy()
    px[changed] = (px[changed] * 0.3 + np.array([255, 0, 0]) * 0.7).astype(np.uint8)
    im = Image.fromarray(px)
    d = ImageDraw.Draw(im)
    for name, x0, y0, x1, y1 in places:
        d.rectangle([x0, y0, x1, y1], outline=(0, 255, 0))
    im.save(out_png)
sys.exit(0 if stray.sum() == 0 and same_palette else 1)

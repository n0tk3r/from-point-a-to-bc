"""Where would a cut-out hide somebody's feet? For every stand place and mark in layout.json, and along the near
edge of the walk outline:    python3 home_lilsis_room_feet.py"""
import json

import numpy as np
from PIL import Image

OUT = "out/home-lilsis-room"
L = json.load(open(f"{OUT}/layout.json"))
alpha = {n: np.asarray(Image.open(f"{OUT}/{n}.png").convert("RGBA"))[..., 3] > 0 for n in ("front", "teaparty", "fort")}
planes = {q["id"]: q for q in L["planes"]}


def inside(pt, poly):
    x, y = pt
    c = False
    for i in range(len(poly)):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % len(poly)]
        if (y0 > y) != (y1 > y) and x < x0 + (x1 - x0) * (y - y0) / (y1 - y0):
            c = not c
    return c


def base_y(base, x):
    (x0, y0), (x1, y1) = base
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


pts = {k: val for k, val in L["marks"].items() if isinstance(val, list)}
for t in L["things"]:
    pts["stand:" + t["id"]] = t["stand"]
bad = 0
for k, (x, y) in pts.items():
    s = (y - L["horizon"]) / (L["full"] - L["horizon"])
    hw = int(11 * s)
    box = (slice(max(0, y - int(12 * s)), y + 1), slice(max(0, x - hw), x + hw + 1))
    hid = {"front": alpha["front"][box].mean()}
    hid["teaparty"] = alpha["teaparty"][box].mean() if y < base_y(planes["teaparty"]["base"], x) else 0.0
    hid["fort"] = alpha["fort"][box].mean() if (x <= 203 and y < base_y(planes["fort"]["base"], x)) else 0.0
    ok = inside((x, y), L["walk"]) and not any(inside((x, y), b) for b in L["blocked"])
    worst = max(hid.values())
    if worst > 0.03 or not ok:
        bad += 1
        print(f"{k:18s} {x:4d},{y:4d}  in walk {ok}  hidden: " + ", ".join(f"{n} {val:.2f}" for n, val in hid.items()))
print("stand places and marks with hidden feet or outside the walk:", bad, "of", len(pts))
worst = []
for x in range(200, 640, 2):
    ys = [y for y in range(340, 500) if inside((x + 0.5, y + 0.5), L["walk"])]
    if not ys:
        continue
    low = max(ys)
    tops = np.where(alpha["front"][380:, x])[0]
    top = 380 + int(tops[0]) if len(tops) else None
    worst.append((low - top + 1 if (top is not None and top <= low) else 0, x, low, top))
print("along the near edge of the walk, the front plane hides at most", max(worst)[0], "rows of a foot (at x =", max(worst)[1], ")")
print("columns with more than 8 rows hidden:", [w[1] for w in worst if w[0] > 8])

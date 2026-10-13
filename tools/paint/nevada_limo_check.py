"""Checks on the finished limousine (python3 nevada_limo_check.py [folder]): layout.json drawn over the picture, and the
numbers that must hold.

  - the walk outline, the things' rects and their places to stand, the marks, the base lines, the windows' polygons and
    the strip's rows, drawn over the comp -> out/nevada-limo-check.png;
  - every pane's polygon is exactly the plain glass painted in back.png (a pixel is in it when its middle is): no glass
    outside a polygon, no frame inside one;
  - divider-up and divider-down have exactly the same pixels; every cut-out lies on the backdrop's pixels (no cut-out
    pixel is off the picture);
  - the strip covers every window's rows, and runs on from its right edge into its left;
  - Joe's and Ranger's scales against the brief's."""

import json
import sys

import numpy as np
from PIL import Image, ImageDraw

from nevada_limo import inside_poly

folder = sys.argv[1] if len(sys.argv) > 1 else "out/nevada-limo"
L = json.load(open(f"{folder}/layout.json"))
problems = []


def alpha(name):
    return np.asarray(Image.open(f"{folder}/{name}.png").convert("RGBA"))[..., 3] > 127


# ---- the glass, pane by pane
back = np.asarray(Image.open(f"{folder}/back.png").convert("RGB")).astype(np.int32)
glass_rgb = np.median(np.concatenate([back[inside_poly(w["poly"])] for w in L["windows"]]), axis=0)
for w in L["windows"]:
    m = inside_poly(w["poly"])
    d = np.abs(back[m] - glass_rgb).sum(axis=1)
    off = (d > 60).sum()
    pm = np.pad(m, 1)
    ring = (pm[:-2, 1:-1] | pm[2:, 1:-1] | pm[1:-1, :-2] | pm[1:-1, 2:]) & ~m          # the pixels just outside the glass
    lum_ring = back[ring].mean(axis=1) if ring.any() else np.array([0])
    bright_out = (lum_ring > back[m].mean(axis=1).mean() - 25).sum()
    print(f"{w['id']}: {m.sum()} px of glass; {off} not the plain glass inside; {bright_out} of {ring.sum()} just outside as light as the glass")
    if off > 0.01 * m.sum() or bright_out > 0.02 * max(1, ring.sum()):
        problems.append(f"{w['id']}: the polygon and the painted glass differ")

# ---- the divider's two states, and the cut-outs on the picture
up, down = alpha("divider-up"), alpha("divider-down")
print("divider-up / divider-down: same pixels" if (up == down).all() else f"divider-up / divider-down DIFFER in {(up != down).sum()} px")
if not (up == down).all():
    problems.append("the divider's two cut-outs differ")
for n in ("bag", "juice", "clipboard", "ropes-4", "ropes-3", "ropes-2", "ropes-1", "front"):
    a = alpha(n)
    print(f"{n}: {a.sum()} px")

# ---- the strip
strip = np.asarray(Image.open(f"{folder}/desert-strip.png").convert("RGB")).astype(np.int32)
top, row = L["strip"]["row"] - strip.shape[0], L["strip"]["row"]
ys = [p[1] for w in L["windows"] for p in w["poly"]]
print(f"strip: {strip.shape[1]} x {strip.shape[0]}, rows {top}..{row}; the windows' rows {min(ys):.0f}..{max(ys):.0f}")
if min(ys) < top or max(ys) > row:
    problems.append("the strip does not cover every window's rows")
seam = np.abs(strip[:, -1] - strip[:, 0]).mean()
nb = np.abs(strip[:, 1:] - strip[:, :-1]).mean()
print(f"strip seam {seam:.1f} against any two neighbouring columns {nb:.1f}")
if seam > 1.5 * nb:
    problems.append("the strip's seam shows")

# ---- the sizes
hz, full = L["horizon"], L["full"]
for k in ("joe", "ranger"):
    m = L["marks"][k]
    print(f"{k}: at {m['at']}, scale {m['scale']} (by its row {(m['at'][1] - hz) / (full - hz):.3f})")
if not 0.75 <= L["marks"]["joe"]["scale"] <= 0.85:
    problems.append("Joe is not drawn at 0.75 to 0.85")
if not 0.9 <= L["marks"]["ranger"]["scale"] <= 1.0:
    problems.append("Ranger's mark is not at 0.9 to 1")
print("ropes mark:", L["marks"]["ropes"])

# ---- the picture with the numbers over it
im = Image.open(f"{folder}/back.png").convert("RGBA")
for n in ("divider-up", "ropes-4", "bag", "juice", "clipboard", "front"):
    im.alpha_composite(Image.open(f"{folder}/{n}.png").convert("RGBA"))
im = im.convert("RGB")
d = ImageDraw.Draw(im)
w_ = [tuple(p) for p in L["walk"]]
d.line(w_ + [w_[0]], fill=(120, 255, 160), width=1)
for w in L["windows"]:
    q = [tuple(p) for p in w["poly"]]
    d.line(q + [q[0]], fill=(80, 200, 255), width=1)
for t in L["things"]:
    x, y, ww, hh = t["shape"]["rect"]
    d.rectangle([x, y, x + ww, y + hh], outline=(255, 230, 90))
    d.text((x + 2, y + 1), t["id"], fill=(255, 255, 255))
    sx, sy = t["stand"]
    d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], outline=(90, 220, 255))
for p in L["planes"]:
    b = p.get("base")
    if isinstance(b, list):
        d.line([tuple(b[0]), tuple(b[1])], fill=(255, 140, 40), width=2)
    elif isinstance(b, (int, float)):
        d.line([(250, b), (340, b)], fill=(255, 140, 40), width=1)
for k, m in L["marks"].items():
    x, y = m["at"]
    d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 255, 255))
    d.text((x + 5, y - 5), k, fill=(255, 255, 255))
d.line([(0, hz), (800, hz)], fill=(255, 80, 80))
d.line([(0, full), (800, full)], fill=(255, 220, 80))
d.line([(0, row), (800, row)], fill=(80, 200, 255))
d.line([(0, top), (800, top)], fill=(80, 200, 255))
out = "out/nevada-limo-check.png"
im.save(out)
print(out)
print("problems:", problems or "none")

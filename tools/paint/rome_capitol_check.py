"""Draws layout.json over the finished picture: the walk outline (green), blocked ground and the cut-outs' solid ground
(red), every cut-out's base (orange), every thing's shape (cyan) and stand (a dot), the marks (magenta), the geese's
place and the pen (yellow), the pen's gate, Titus's seat, and the rows horizon and full.

  python3 rome_capitol_check.py      -> out/rome-capitol-check.png"""

import json

from PIL import Image, ImageDraw

L = json.load(open("out/rome-capitol/layout.json"))
im = Image.open("out/rome-capitol-comp.png").convert("RGB")
big = im.resize((1600, 1200), Image.NEAREST)
d = ImageDraw.Draw(big, "RGBA")
S = 2
P = lambda pts: [(x * S, y * S) for x, y in pts]
d.line([(0, L["horizon"] * S), (1600, L["horizon"] * S)], fill=(255, 0, 0, 120), width=1)
d.line([(0, L["full"] * S), (1600, L["full"] * S)], fill=(255, 0, 0, 120), width=1)
d.polygon(P(L["walk"]), outline=(40, 220, 60, 255))
for b in L["blocked"]:
    d.polygon(P(b), outline=(230, 40, 40, 255), fill=(230, 40, 40, 50))
for p in L["planes"]:
    sol = p.get("solid")
    sols = sol if sol and isinstance(sol[0][0], list) else ([sol] if sol else [])
    for s in sols:
        d.polygon(P(s), outline=(230, 40, 40, 255), fill=(230, 40, 40, 40))
    b = p.get("base")
    if isinstance(b, list):
        d.line(P(b), fill=(255, 150, 0, 255), width=3)
        d.text((b[0][0] * S + 4, b[0][1] * S + 2), p["id"], fill=(255, 150, 0, 255))
    elif b is not None:
        d.line([(0, b * S), (1600, b * S)], fill=(255, 150, 0, 120), width=1)
        d.text((4, b * S + 2), p["id"] + " (row)", fill=(255, 150, 0, 255))
for t in L["things"]:
    d.polygon(P(t["shape"]["poly"]), outline=(0, 230, 255, 255))
    x, y = t["stand"]
    d.ellipse([x * S - 4, y * S - 4, x * S + 4, y * S + 4], fill=(0, 230, 255, 255))
    xs = [q[0] for q in t["shape"]["poly"]]
    ys = [q[1] for q in t["shape"]["poly"]]
    d.text((min(xs) * S + 3, min(ys) * S + 3), t["id"], fill=(0, 240, 255, 255))
M = L["marks"]
d.polygon(P(M["geese"]), outline=(255, 230, 0, 255), fill=(255, 230, 0, 50))
d.polygon(P(M["pen"]), outline=(255, 230, 0, 255), fill=(255, 230, 0, 50))
gx, gy = M["pen_gate"]
d.ellipse([gx * S - 5, gy * S - 5, gx * S + 5, gy * S + 5], outline=(255, 230, 0, 255), width=2)
ts = M["titus_seat"]
ax, ay = ts["at"]
d.line([(ax * S, ay * S), (ax * S, (ay - ts["px"]) * S)], fill=(255, 60, 200, 255), width=3)
for k, v in M.items():
    if isinstance(v, list) and len(v) == 2 and isinstance(v[0], (int, float)):
        x, y = v
        d.ellipse([x * S - 5, y * S - 5, x * S + 5, y * S + 5], fill=(255, 40, 220, 255))
        d.text((x * S + 7, y * S - 6), k, fill=(255, 60, 230, 255))
for e in L["exits"]:
    d.polygon(P(e["band"]), outline=(255, 255, 255, 200))
    x, y = e["walkTo"]
    d.rectangle([x * S - 5, y * S - 5, x * S + 5, y * S + 5], outline=(255, 255, 255, 255), width=2)
big.save("out/rome-capitol-check.png")
print("out/rome-capitol-check.png")

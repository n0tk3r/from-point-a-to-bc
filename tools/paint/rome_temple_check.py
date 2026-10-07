"""Lay the numbers of layout.json over a picture, with stand-in people, to check them by eye:
rome_temple_check.py [picture] -> out/rome-temple-check.png"""
import json
import sys
from PIL import Image, ImageDraw

src = sys.argv[1] if len(sys.argv) > 1 else "out/rome-temple-2-all.png"
L = json.load(open("out/rome-temple/layout.json"))
im = Image.open(src).convert("RGBA")
ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
d.polygon([tuple(p) for p in L["walk"]], outline=(80, 255, 120, 255), fill=(80, 255, 120, 30))
for b in L["blocked"]:
    d.polygon([tuple(p) for p in b], outline=(255, 80, 80, 255), fill=(255, 80, 80, 40))


def person(x, y, tall=1.0, color=(120, 200, 255, 150), seated=False):
    s = (y - L["horizon"]) / (L["full"] - L["horizon"]) * 160 * tall
    h = s * (0.78 if seated else 1.0)
    d.rectangle([x - s * 0.15, y - h, x + s * 0.15, y], fill=color, outline=(255, 255, 255, 255))
    d.ellipse([x - s * 0.07, y - h - s * 0.02, x + s * 0.07, y - h + s * 0.13], fill=(255, 220, 180, 220))


for t in L["things"]:
    sh = t["shape"]
    if "rect" in sh:
        x, y, w, h = sh["rect"]
        d.rectangle([x, y, x + w, y + h], outline=(255, 230, 80, 255))
    else:
        d.polygon([tuple(p) for p in sh["poly"]], outline=(255, 230, 80, 255))
    sx, sy = t["stand"]
    d.ellipse([sx - 3, sy - 2, sx + 3, sy + 2], fill=(255, 230, 80, 255))
    d.text((sx + 4, sy - 10), t["id"], fill=(255, 255, 255, 255))
for e in L["exits"]:
    d.polygon([tuple(p) for p in e["shape"]["poly"]], outline=(255, 120, 255, 255))
person(*L["marks"]["son"], tall=0.72, color=(255, 160, 80, 150))
person(*L["marks"]["clerk"], seated=True)
for t in L["things"]:
    if t["id"] in ("hum", "statue"):
        person(*t["stand"], tall=0.72 if t["id"] == "hum" else 1.0, color=(200, 255, 120, 120))
hx, hy = [t for t in L["things"] if t["id"] == "hum"][0]["at"]
d.line([L["marks"]["son"][0] - 12, L["marks"]["son"][1] - 70, hx, hy], fill=(255, 255, 160, 255), width=1)
im.alpha_composite(ov)
im.convert("RGB").save("out/rome-temple-check.png")
print("ok", L["marks"], [t["stand"] for t in L["things"][:3]])

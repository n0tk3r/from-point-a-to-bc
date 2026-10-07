"""Draw the layout numbers over the picture, with people-sized bars, to check them by eye."""
import json, sys
from PIL import Image, ImageDraw
src = sys.argv[1] if len(sys.argv) > 1 else "out/rome-steps-comp.png"
L = json.load(open("out/rome-steps/layout.json"))
im = Image.open(src).convert("RGB")
d = ImageDraw.Draw(im, "RGBA")
d.polygon([tuple(p) for p in L["walk"]], fill=(0, 255, 0, 40), outline=(0, 160, 0, 255))
for b in L["blocked"]:
    d.polygon([tuple(p) for p in b], fill=(255, 0, 0, 70), outline=(200, 0, 0, 255))
for pl in L["planes"]:
    b = pl.get("base")
    if isinstance(b, list):
        d.line([tuple(b[0]), tuple(b[1])], fill=(255, 255, 0, 255), width=1)
    elif b is not None:
        d.line([(0, b), (800, b)], fill=(255, 255, 0, 120), width=1)
ms = L.get("minScale", 0.3)
def person(x, y, c):
    sc = max(ms, min(1.2, (y - L["horizon"]) / (L["full"] - L["horizon"])))
    h = 160 * sc
    d.rectangle([x - h * 0.14, y - h, x + h * 0.14, y], outline=c, width=1)
    d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=c)
for t in L["things"]:
    x, y, w, h = t["shape"]["rect"]
    d.rectangle([x, y, x + w, y + h], outline=(0, 200, 255, 255))
    d.text((x + 2, y + 2), t["id"], fill=(0, 60, 120, 255))
    person(t["stand"][0], t["stand"][1], (0, 120, 255, 255))
for e in L["exits"]:
    d.polygon([tuple(p) for p in e["shape"]["poly"]], outline=(255, 0, 255, 255))
    person(e["stand"][0], e["stand"][1], (255, 0, 255, 255))
for k, (x, y) in L["marks"].items():
    person(x, y, (255, 255, 255, 255))
    d.text((x + 4, y - 12), k, fill=(255, 255, 255, 255))
im.save("out/rome-steps-check.png")

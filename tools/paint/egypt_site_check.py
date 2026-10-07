"""Draw layout.json over the comp, to check the numbers against the picture: -> out/egypt-site-check.png"""
import json
from PIL import Image, ImageDraw
L = json.load(open("out/egypt-site/layout.json"))
im = Image.open("out/egypt-site-comp.png").convert("RGBA")
ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
d.polygon([tuple(p) for p in L["walk"]], fill=(40, 200, 80, 70), outline=(0, 120, 40, 255))
for b in L["blocked"]:
    d.polygon([tuple(p) for p in b], fill=(220, 40, 40, 110), outline=(160, 0, 0, 255))
for t in L["things"]:
    sh = t["shape"]
    if "rect" in sh:
        x, y, w, h = sh["rect"]
        d.rectangle([x, y, x + w, y + h], outline=(40, 60, 220, 255))
    else:
        d.polygon([tuple(p) for p in sh["poly"]], outline=(40, 60, 220, 255))
    sx, sy = t["stand"]
    d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(40, 60, 220, 255))
    d.text((sx + 4, sy - 10), t["id"], fill=(10, 20, 120, 255))
for e in L["exits"]:
    d.polygon([tuple(p) for p in e["shape"]["poly"]], outline=(230, 120, 0, 255))
for name, (mx, my) in L["marks"].items():
    d.line([mx - 4, my, mx + 4, my], fill=(0, 0, 0, 255))
    d.line([mx, my - 4, mx, my + 4], fill=(0, 0, 0, 255))
    d.text((mx + 3, my + 2), name, fill=(0, 0, 0, 255))
for pl in L["planes"]:
    b = pl.get("base")
    if isinstance(b, list):
        d.line([tuple(b[0]), tuple(b[1])], fill=(255, 0, 255, 255), width=2)
    elif b is not None:
        d.line([0, b, 60, b], fill=(255, 0, 255, 255), width=2)
d.line([tuple(p) for p in L["stair"]] + [tuple(p) for p in L["landing"]], fill=(255, 255, 0, 255), width=1)
d.line([tuple(L["beam"][0]), tuple(L["beam"][1])], fill=(255, 255, 255, 255), width=1)
im.alpha_composite(ov)
im.convert("RGB").save("out/egypt-site-check.png")
print("ok")

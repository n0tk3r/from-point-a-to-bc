"""Draw the layout over the picture, to see that the numbers sit where the paint is: python3 home_lilsis_room_check.py [picture]"""
import json
import sys
from PIL import Image, ImageDraw
src = sys.argv[1] if len(sys.argv) > 1 else "out/home-lilsis-room-comp.png"
L = json.load(open("out/home-lilsis-room/layout.json"))
im = Image.open(src).convert("RGB")
d = ImageDraw.Draw(im)
d.line([tuple(p) for p in L["walk"]] + [tuple(L["walk"][0])], fill=(120, 255, 160), width=1)
for b in L["blocked"]:
    d.line([tuple(p) for p in b] + [tuple(b[0])], fill=(255, 120, 120), width=1)
for t in L["things"]:
    r = t["shape"].get("rect")
    if r:
        d.rectangle([r[0], r[1], r[0] + r[2], r[1] + r[3]], outline=(255, 255, 120))
        d.text((r[0] + 2, r[1] + 1), t["id"], fill=(255, 255, 255))
    x, y = t["stand"]
    d.ellipse([x - 3, y - 3, x + 3, y + 3], outline=(255, 80, 255))
for pl in L["planes"]:
    if "base" in pl:
        d.line([tuple(pl["base"][0]), tuple(pl["base"][1])], fill=(80, 200, 255), width=2)
for k, v in L["marks"].items():
    if isinstance(v, list):
        d.ellipse([v[0] - 2, v[1] - 2, v[0] + 2, v[1] + 2], fill=(255, 255, 255))
d.line([(0, L["horizon"]), (800, L["horizon"])], fill=(255, 80, 80))
d.line([(0, L["full"]), (800, L["full"])], fill=(255, 220, 80))
vx, vy = L["vanishing"]
d.ellipse([vx - 4, vy - 4, vx + 4, vy + 4], outline=(255, 80, 80))
im.save("out/home-lilsis-room-check.png")
print("out/home-lilsis-room-check.png")

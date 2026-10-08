"""Draw layout.json over the finished picture, to see that the numbers are where the things are:
python3 home_bigsis_room_check.py -> out/home-bigsis-room-check.png"""
import json
from PIL import Image, ImageDraw
OUT = "out/home-bigsis-room"
L = json.load(open(f"{OUT}/layout.json"))
im = Image.open("out/home-bigsis-room-comp.png").convert("RGB")
d = ImageDraw.Draw(im)
w = [tuple(p) for p in L["walk"]]
d.line(w + [w[0]], fill=(120, 255, 160), width=1)
for t in L["things"]:
    x, y, ww, hh = t["shape"]["rect"]
    d.rectangle([x, y, x + ww, y + hh], outline=(255, 230, 90))
    d.text((x + 2, y + 1), t["id"], fill=(255, 255, 255))
    sx, sy = t["stand"]
    d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], outline=(90, 220, 255))
for e in L["exits"]:
    q = [tuple(p) for p in e["shape"]["poly"]]
    d.line(q + [q[0]], fill=(255, 90, 220), width=1)
for p in L["planes"]:
    if isinstance(p.get("base"), list):
        d.line([tuple(p["base"][0]), tuple(p["base"][1])], fill=(255, 140, 40), width=2)
for k, (x, y) in L["marks"]["fromLadder"].items():
    d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 255, 255))
    d.text((x + 6, y - 5), k, fill=(255, 255, 255))
d.line([(0, L["horizon"]), (800, L["horizon"])], fill=(255, 80, 80))
d.line([(0, L["full"]), (800, L["full"])], fill=(255, 220, 80))
vx, vy = L["vanishing"]
d.ellipse([vx - 4, vy - 4, vx + 4, vy + 4], outline=(255, 80, 80))
im.save("out/home-bigsis-room-check.png")
print("out/home-bigsis-room-check.png")

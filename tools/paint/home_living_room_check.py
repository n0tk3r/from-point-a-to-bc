"""Check the finished room by eye: python3 home_living_room_check.py

  out/home-living-room-check.png   the layout drawn over the comp (walk outline green, blocked red, each thing's shape
                                   yellow with its id, stand places as crosses, base lines cyan, marks as rings)
  out/home-living-room-cuts.png    the cut-outs side by side on grey
  out/home-living-room-people.png  the game's own figures (people_on.py; the game's server must be up on port 8765)
                                   standing at nine of the layout's places, from the front door to the foot of the table"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw

L = json.load(open("out/home-living-room/layout.json"))
im = Image.open("out/home-living-room-comp.png").convert("RGB")
d = ImageDraw.Draw(im)
w = [tuple(p) for p in L["walk"]]
d.line(w + [w[0]], fill=(90, 255, 140), width=1)
for b in L["blocked"]:
    b = [tuple(p) for p in b]
    d.line(b + [b[0]], fill=(255, 80, 80), width=1)
for t in L["things"]:
    s = t["shape"]
    if "rect" in s:
        x, y, ww, hh = s["rect"]
        d.rectangle([x, y, x + ww, y + hh], outline=(255, 230, 90))
        d.text((x + 2, y + 1), t["id"], fill=(255, 255, 255))
    else:
        p = [tuple(q) for q in s["poly"]]
        d.line(p + [p[0]], fill=(255, 230, 90), width=1)
        d.text((p[0][0] + 2, p[0][1] - 12), t["id"], fill=(255, 255, 255))
    for key in ("stand", "stand2"):
        if key in t:
            x, y = t[key]
            d.line([x - 4, y, x + 4, y], fill=(255, 255, 255))
            d.line([x, y - 4, x, y + 4], fill=(255, 255, 255))
for p in L["planes"]:
    if "base" in p:
        d.line([tuple(q) for q in p["base"]], fill=(90, 230, 255), width=1)
m = L["marks"]
for name in ("mom", "bigsis", "lilsis"):
    x, y = m["default"][name]
    d.ellipse([x - 3, y - 3, x + 3, y + 3], outline=(255, 120, 220))
for x, y in [m["fromLanding"]["lead"]] + m["fromLanding"]["others"]:
    d.ellipse([x - 3, y - 3, x + 3, y + 3], outline=(120, 220, 255))
im.save("out/home-living-room-check.png")

names = ["piano", "piano-open", "armchair", "pencil", "table"]
sheet = Image.new("RGB", (800 * 3, 600 * 2), (128, 128, 128))
for i, n in enumerate(names):
    c = Image.open(f"out/home-living-room/{n}.png").convert("RGBA")
    sheet.paste(c, (800 * (i % 3), 600 * (i // 3)), c)
sheet.save("out/home-living-room-cuts.png")
print("out/home-living-room-check.png", "out/home-living-room-cuts.png")


# ---- the game's people, at the layout's own stand places
T = {t["id"]: t for t in L["things"]}
under = Image.open("out/home-living-room/back.png").convert("RGBA")
under.alpha_composite(Image.open("out/home-living-room/piano.png").convert("RGBA"))      # everyone here stands in front of the piano
under.convert("RGB").save("out/home-living-room-under-people.png")
folk = [("mom", T["door"]["stand"], 180), ("lilsis", T["piano"]["stand"], 180), ("bigsis", T["piano"]["stand2"], 180), ("bigsis", T["books"]["stand"], 180),
        ("mom", m["default"]["mom"], 0), ("lilsis", T["closet"]["stand"], 270), ("bigsis", m["fromLanding"]["lead"], 90),
        ("mom", T["table"]["stand"], 90), ("lilsis", m["fromLanding"]["others"][1], 0)]
who = ";".join(f"{w}|{p[0]}|{p[1]}|{yaw}" for w, p, yaw in folk)
try:
    subprocess.run([sys.executable, "people_on.py", "out/home-living-room-under-people.png", str(L["horizon"]), str(L["full"]), who,
                    "out/home-living-room-people.png", "out/home-living-room/armchair.png", "out/home-living-room/pencil.png",
                    "out/home-living-room/table.png"], check=True)
finally:
    os.remove("out/home-living-room-under-people.png")

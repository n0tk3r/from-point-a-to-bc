"""Draw layout.json over the comp, to check it by eye: walk outline, blocked, shapes, stand points with a figure-sized box."""
import json
from PIL import Image, ImageDraw
L = json.load(open("out/egypt-gallery/layout.json"))
im = Image.open("out/egypt-gallery-comp.png").convert("RGB")
d = ImageDraw.Draw(im)
d.polygon([tuple(p) for p in L["walk"]], outline=(0, 255, 0))
for b in L["blocked"]:
    d.polygon([tuple(p) for p in b], outline=(255, 0, 0))
def person(x, y, col):
    s = (y - L["horizon"]) / (L["full"] - L["horizon"])
    d.rectangle((x - 20 * s, y - 160 * s, x + 20 * s, y), outline=col)
    d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=col)
for t in L["things"] + L["exits"]:
    sh = t["shape"]
    if "rect" in sh:
        x, y, w, h = sh["rect"]
        d.rectangle((x, y, x + w, y + h), outline=(255, 255, 0))
    else:
        d.polygon([tuple(p) for p in sh["poly"]], outline=(255, 255, 0))
    person(*t["stand"], (0, 255, 255))
    d.text((t["stand"][0] + 5, t["stand"][1] - 10), t.get("id", t.get("to")), fill=(255, 255, 255))
for k, v in L["marks"].items():
    d.ellipse((v[0] - 3, v[1] - 3, v[0] + 3, v[1] + 3), fill=(255, 0, 255))
    d.text((v[0] + 5, v[1] - 4), k, fill=(255, 160, 255))
for k, v in L["beam"].items():
    d.ellipse((v[0] - 2, v[1] - 2, v[0] + 2, v[1] + 2), fill=(255, 255, 255))
pts = [tuple(L["beam"][k]) for k in ("gate", "mirror-foot", "mirror-top", "door")]
d.line(pts, fill=(255, 255, 200), width=1)
for x, y, k in L["lamps"]:
    d.rectangle((x - 2, y - 2, x + 2, y + 2), outline=(255, 128, 0))
im.save("out/egypt-gallery-check.png")
print(json.dumps(L["marks"]), json.dumps(L["beam"]))
for t in L["things"] + L["exits"]:
    print(t.get("id", t.get("to")), t["shape"], t["stand"], t["face"])
print("walk", L["walk"])
print("planes", L["planes"])


def inside(p, poly):
    x, y = p
    n, c = len(poly), False
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            c = not c
    return c
bad = 0
for t in L["things"] + L["exits"]:
    ok = inside(t["stand"], L["walk"]) and not any(inside(t["stand"], b) for b in L["blocked"])
    bad += not ok
    if not ok:
        print("STAND OUTSIDE WALK:", t.get("id", t.get("to")), t["stand"])
for k in ("dad-from-site", "dad-from-chamber"):
    if not inside(L["marks"][k], L["walk"]):
        bad += 1
        print("MARK OUTSIDE WALK:", k)
print("stand points checked;", bad, "bad")

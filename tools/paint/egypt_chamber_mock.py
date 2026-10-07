"""A rough check of sizes: stand plain dummy people on the finished planes, sorted as the game will sort them.
(Only for looking at; the game draws the real people.)   python3 egypt_chamber_mock.py [work|out]"""
import json
import sys

from PIL import Image, ImageDraw

HZ, FULL = -200, 585


def person(d, x, y, shirt, seated=False, ss=1):
    s = (y - HZ) / (FULL - HZ) * 160 / 160.0
    h = 160 * s * (0.62 if seated else 1.0)
    w = 46 * s
    skin, hair, legs = (196, 140, 100), (60, 40, 30), (70, 70, 110)
    top = y - h
    d.ellipse([x - 9 * s, top, x + 9 * s, top + 21 * s], fill=skin)
    d.pieslice([x - 9.5 * s, top - 1.5 * s, x + 9.5 * s, top + 16 * s], 180, 360, fill=hair)
    d.rectangle([x - w / 2, top + 22 * s, x + w / 2, top + 22 * s + 56 * s], fill=shirt)
    d.rectangle([x - w / 2 - 6 * s, top + 24 * s, x - w / 2, top + 76 * s], fill=skin)
    d.rectangle([x + w / 2, top + 24 * s, x + w / 2 + 6 * s, top + 76 * s], fill=skin)
    if seated:
        d.rectangle([x - w / 2, top + 78 * s, x + w / 2 + 20 * s, y - 14 * s], fill=legs)
        d.rectangle([x + w / 2 + 6 * s, y - 30 * s, x + w / 2 + 20 * s, y], fill=skin)
    else:
        d.rectangle([x - w / 2 + 2 * s, top + 78 * s, x - 2 * s, y], fill=legs)
        d.rectangle([x + 2 * s, top + 78 * s, x + w / 2 - 2 * s, y], fill=legs)


def main(which="out"):
    folder = "out/egypt-chamber"
    lay = json.load(open(f"{folder}/layout.json"))
    back = Image.open(f"{folder}/back.png").convert("RGBA")
    people = [(lay["marks"]["goldsmith"], (150, 120, 90), True), ((426, 520), (200, 60, 50), False), ((106, 468), (60, 120, 190), False),
              ((500, 500), (70, 150, 90), False), ((650, 532), (190, 170, 60), False), ((392, 478), (150, 90, 170), False), ((230, 575), (220, 220, 220), False)]
    items = []
    for p in lay["planes"]:
        im = Image.open(f"{folder}/{p['file']}").convert("RGBA")
        items.append((1e9 if p.get("plane") == "front" else p["base"], "plane", im))
    for (xy, col, seated) in people:
        items.append((xy[1], "person", (xy, col, seated)))
    out = back.copy()
    for base, kind, what in sorted(items, key=lambda t: t[0]):
        if kind == "plane":
            out.alpha_composite(what)
        else:
            layer = Image.new("RGBA", out.size, (0, 0, 0, 0))
            person(ImageDraw.Draw(layer), what[0][0], what[0][1], what[1], what[2])
            out.alpha_composite(layer)
    d = ImageDraw.Draw(out)
    walk = [tuple(p) for p in lay["walk"]]
    d.line(walk + [walk[0]], fill=(80, 255, 120, 255), width=1)
    for b in lay["blocked"]:
        pts = [tuple(p) for p in b]
        d.line(pts + [pts[0]], fill=(255, 80, 80, 255), width=1)
    for t in lay["things"] + lay["exits"]:
        sh = t["shape"]
        if "rect" in sh:
            x, y, w, h = sh["rect"]
            d.rectangle([x, y, x + w, y + h], outline=(255, 230, 80, 255))
        else:
            pts = [tuple(p) for p in sh["poly"]]
            d.line(pts + [pts[0]], fill=(255, 230, 80, 255), width=1)
        sx, sy = t["stand"]
        d.ellipse([sx - 3, sy - 2, sx + 3, sy + 2], outline=(80, 255, 255, 255))
    b0, b1 = lay["beam"]
    d.line([tuple(b0), tuple(b1)], fill=(255, 255, 200, 255), width=2)
    out.convert("RGB").save("out/egypt-chamber-work/mock.png")
    print("out/egypt-chamber-work/mock.png")


if __name__ == "__main__":
    main(*sys.argv[1:])

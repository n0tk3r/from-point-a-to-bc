"""Across the Tiber, checked: layout.json drawn over the finished pictures (the walk outline green, blocked ground red,
each cut-out's base magenta, every thing's shape yellow with its place to stand, the marks blue, the window's man and
the bench's seat, the hens' row), into out/rome-tiber-check.png; then every place to stand walked on the engine's own
walk map (rome_tiber_walk.mjs), and the engine's back-to-front order tried with the boy everywhere (rome_tiber_order.py).

    python3 rome_tiber_check.py"""

import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw

OUT = "out/rome-tiber"


def draw(path_in=f"{OUT}-comp.png", path_out="out/rome-tiber-check.png"):
    lay = json.load(open(f"{OUT}/layout.json"))
    hz, full = lay["horizon"], lay["full"]
    im = Image.open(path_in).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.polygon([tuple(p) for p in lay["walk"]], fill=(60, 255, 120, 46), outline=(60, 255, 120, 255))
    for bl in lay["blocked"]:
        d.polygon([tuple(p) for p in bl], fill=(255, 60, 60, 90), outline=(255, 60, 60, 255))
    for pl in lay["planes"]:
        if pl.get("solid"):
            d.polygon([tuple(p) for p in pl["solid"]], fill=(255, 60, 60, 90), outline=(255, 60, 60, 255))
        b = pl.get("base")
        if isinstance(b, (int, float)):
            d.line([0, b, 799, b], fill=(255, 0, 255, 150))
        elif b:
            d.line([tuple(b[0]), tuple(b[1])], fill=(255, 0, 255, 255), width=2)
    for t in lay["things"]:
        sh = t["shape"]
        if "rect" in sh:
            x, y, w, h = sh["rect"]
            d.rectangle([x, y, x + w, y + h], outline=(255, 255, 0, 255))
        else:
            d.polygon([tuple(p) for p in sh["poly"]], outline=(255, 255, 0, 200))
        sx, sy = t["stand"]
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 255, 0, 255))
        d.text((sx + 4, sy - 4), t["id"], fill=(255, 255, 160, 255))
    m = lay["marks"]

    def man(x, y, tall, color, label, scale=None):
        k = scale if scale is not None else (y - hz) / (full - hz)
        h = 160 * tall * k
        d.rectangle([x - h * 0.13, y - h, x + h * 0.13, y], outline=color, width=1)
        d.text((x - 8, y + 2), label, fill=color)
    for name in ("fromBridge", "toBridge", "default", "door", "wait", "petosiris", "mariam_talk"):
        x, y = m[name][:2]
        man(x, y, 1.0 if name in ("petosiris",) else 0.74, (90, 200, 255, 255), name)
    man(*m["felix"]["at"], 1.0, (90, 200, 255, 255), "felix")
    for i, p in enumerate(m["felix_spots"]):
        man(p[0], p[1], 1.0, (90, 160, 255, 200), f"f{i}")
    man(*m["mariam"]["at"], 0.69, (255, 160, 220, 255), "mariam")
    for i, p in enumerate(m["mariam_spots"]):
        man(p[0], p[1], 0.69, (255, 140, 200, 200), f"m{i}")
    man(*m["pray_eleazar"][:2], 0.96, (255, 220, 120, 255), "pray_e")
    man(*m["pray_son"][:2], 0.74, (255, 220, 120, 255), "pray_s")
    man(*m["bless"][:2], 0.96, (255, 200, 90, 255), "bless")
    w = m["window"]
    man(w["at"][0], w["at"][1], 0.96, (255, 90, 90, 255), "window", scale=w["scale"])
    d.polygon([tuple(p) for p in m["window_opening"]], outline=(255, 90, 90, 255))
    bs = m["bench_seat"]
    d.line([bs["at"][0] - 8, bs["at"][1], bs["at"][0] + 8, bs["at"][1]], fill=(255, 90, 90, 255), width=2)
    d.line([bs["at"][0], bs["at"][1], bs["at"][0], bs["at"][1] - bs["px"]], fill=(255, 90, 90, 255), width=2)
    d.line([tuple(m["hens"][0]), tuple(m["hens"][1])], fill=(255, 255, 255, 255), width=2)
    for f in lay["fx"]:
        if f.get("perch"):
            d.line([tuple(f["perch"][0]), tuple(f["perch"][1])], fill=(255, 120, 0, 255), width=3)
        if f.get("type") == "shimmer":
            d.polygon([tuple(p) for p in f["poly"]], outline=(120, 220, 255, 160))
        if f.get("type") in ("ripples", "smoke"):
            x, y = f["at"]
            d.ellipse([x - 4, y - 2, x + 4, y + 2], outline=(120, 220, 255, 255))
    d.line([0, hz, 799, hz], fill=(255, 0, 0, 120))
    d.line([0, full, 799, full], fill=(255, 0, 255, 120))
    d.line([0, 545, 399, 545], fill=(255, 255, 255, 90))
    Image.alpha_composite(im, ov).convert("RGB").save(path_out)
    print(path_out)


if __name__ == "__main__":
    draw()
    here = os.path.dirname(os.path.abspath(__file__))
    res = subprocess.run(["node", os.path.join(here, "rome_tiber_walk.mjs")], capture_output=True, text=True)
    print(res.stdout.strip() or res.stderr.strip())
    res = subprocess.run([sys.executable, os.path.join(here, "rome_tiber_order.py"), os.path.join(here, OUT)], capture_output=True, text=True)
    print(res.stdout.strip() or res.stderr.strip())

"""A mock screenshot to check sizes and places: stand-in people at the brief's marks, sorted with the cut-outs.
egypt_site_mock.py [min scale]  ->  out/egypt-site-mock.png   (reads the pictures the last run left)"""
import sys, json
import numpy as np
from PIL import Image, ImageDraw
from egypt_site_plan import *
import egypt_site_things as things

MIN = float(sys.argv[1]) if len(sys.argv) > 1 else 0.33
back = Image.open("out/egypt-site-2-back.png").convert("RGBA")


def figure(d, x, y, col, sit=False):
    k = max(MIN, (y - HZ) / (FULL - HZ))
    h = 160 * k * (0.56 if sit else 1.0)
    w = 160 * k * 0.13
    d.rectangle([x - w, y - h * 0.88, x + w, y], fill=col)
    d.ellipse([x - w * 0.8, y - h, x + w * 0.8, y - h * 0.84], fill=(120, 80, 60, 255))
    d.rectangle([x - w, y - h * 0.50, x + w, y - h * 0.3], fill=(240, 236, 220, 255))


folk = [(150, 448, (60, 90, 160, 255), True), (360, 430, (150, 60, 60, 255), False), (300, 400, (90, 110, 70, 255), False), (270, 390, (90, 110, 70, 255), False),
        (240, 382, (90, 110, 70, 255), False), (690, 420, (110, 70, 130, 255), False), (330, 520, (200, 120, 40, 255), False), (120, 580, (30, 120, 150, 255), False)]
for t in (0.0, 0.33, 0.66, 1.0):
    fx, fy = stair_walk(t)
    folk.append((fx, fy, (30, 120, 150, 255), False))
dx, dy = backp(DOOR_OFF, 0)
folk.append((dx + 14, dy + 2, (30, 120, 150, 255), False))
planes = []
shape = (H, W)
for name, base in (("awning", 474.0), ("sledge", 473.0), ("shade", 521.0), ("front", 9999.0)):
    fn = getattr(things, name + "_plane")
    c, a = fn(shape, True) if name != "front" else fn(shape, True, None)
    im = np.dstack([np.clip(c, 0, 1) * 255, (a > 0.5) * 255.0]).astype(np.uint8)
    planes.append((base, Image.fromarray(im, "RGBA")))
items = [(y, "f", (x, y, col, sit)) for x, y, col, sit in folk] + [(b, "p", im) for b, im in planes]
for _, kind, what in sorted(items, key=lambda i: i[0]):
    if kind == "p":
        back.alpha_composite(what)
    else:
        figure(ImageDraw.Draw(back), *what)
back.convert("RGB").save("out/egypt-site-mock.png")
print("ok")

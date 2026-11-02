#!/usr/bin/env python3
"""ENGINE-21: the engine's own proof pictures for round twenty-one's moving things and its close-up, drawn as they are (never
keyed), plain shapes in a few colours, so that the engine can be proved before the painters' Act Six is in:

    python3 proof_sea.py            (in tools/paint) writes, in art/proof/:
        sail.png       800 x 600: a great square sail of vertical bolts on its yard, for `sway` with anchor "belly" (breathing)
        far.png        800 x 600: a band of far sea with a grey cape at its left, for `bob` (the swell: a pixel or two, tilting)
        bars.png       800 x 600: three slanting bars of warm light, for `slide` (the sunset sliding up a wall, and fading)
        cloud-on.png   800 x 600: a white cap of cloud on a far mountain; cloud-off.png: the same place, a wisp left (two
                       states of one cut-out, for g.fadePlane's cross-fade)
        near.png       800 x 600: a strongbox's face seen close, a latch with three parts (a backdrop for the close-up proof,
                       proof-near.js)
"""

import os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "art", "proof")
W, H = 800, 600
CLEAR = (0, 0, 0, 0)


def blank():
    return Image.new("RGBA", (W, H), CLEAR)


def sail():
    im = blank(); d = ImageDraw.Draw(im)
    d.rectangle([236, 52, 584, 62], fill=(118, 82, 52, 255))                         # the yard
    poly = [(250, 62), (570, 62), (582, 330), (238, 330)]
    d.polygon(poly, fill=(238, 233, 220, 255), outline=(150, 140, 120, 255))
    for i in range(1, 8):                                                              # the bolts' seams
        x0 = 250 + (320 * i) / 8; x1 = 238 + (344 * i) / 8
        d.line([(x0, 62), (x1, 330)], fill=(198, 190, 172, 255), width=2)
    d.line([(238, 330), (582, 330)], fill=(150, 140, 120, 255), width=3)
    return im


def far():
    im = blank(); d = ImageDraw.Draw(im)
    d.rectangle([0, 236, 800, 300], fill=(54, 88, 140, 255))                          # the far sea
    d.line([(0, 236), (800, 236)], fill=(30, 52, 92, 255), width=2)                    # the horizon
    d.polygon([(0, 214), (60, 206), (150, 220), (210, 236), (0, 236)], fill=(120, 124, 132, 255))      # a grey cape
    return im


def bars():
    im = blank(); d = ImageDraw.Draw(im)
    for x in (470, 560, 650):
        d.polygon([(x, 120), (x + 46, 120), (x + 6, 420), (x - 40, 420)], fill=(255, 176, 112, 96))
    return im


def cloud(on):
    im = blank(); d = ImageDraw.Draw(im)
    if on:
        for (x, y, r) in ((560, 96, 30), (600, 86, 38), (646, 98, 30), (604, 106, 34)):
            d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=(250, 250, 252, 255))
    else:
        d.ellipse([616, 70, 676, 84], fill=(250, 250, 252, 150))
    return im


def near():
    im = Image.new("RGBA", (W, H), (58, 40, 30, 255)); d = ImageDraw.Draw(im)
    for y in range(0, H, 46):                                                          # the planks of the box's face
        d.line([(0, y), (W, y)], fill=(44, 30, 22, 255), width=3)
    d.rounded_rectangle([250, 170, 550, 430], radius=14, fill=(92, 92, 98, 255), outline=(28, 28, 32, 255), width=4)      # the iron plate
    d.ellipse([292, 214, 352, 274], fill=(66, 66, 72, 255), outline=(24, 24, 28, 255), width=3)       # the knob (left)
    d.rectangle([380, 300, 420, 340], fill=(66, 66, 72, 255), outline=(24, 24, 28, 255), width=3)     # the square post
    d.rectangle([440, 210, 520, 230], fill=(40, 40, 46, 255))                                         # the slot (right)
    d.rectangle([270, 380, 530, 400], fill=(130, 110, 60, 255), outline=(60, 48, 24, 255), width=2)   # the bolt
    return im


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, im in (("sail", sail()), ("far", far()), ("bars", bars()), ("cloud-on", cloud(True)), ("cloud-off", cloud(False)), ("near", near())):
        im.save(os.path.join(OUT, name + ".png"), optimize=True)
        print("wrote art/proof/" + name + ".png")

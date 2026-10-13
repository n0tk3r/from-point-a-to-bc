#!/usr/bin/env python3
"""The proof's painted creature: a cat-sized animal drawn as painted frames, in the format the master brief fixes for
Ranger (NEVADA-12, "Ranger, painted"), so that the engine's painted figure can be built and proved before the raccoon
is painted. Four colours, hard edges, every set the format names, a shades variant of every frame, and a 64x64 portrait.

    python3 proof_critter.py            (in tools/paint) writes art/proof/critter-*.png, art/proof/critter.json, strip.png and
                                        window.png: the engine's own proof pictures, drawn as they are (never keyed)

Every frame faces E on one canvas (48 x 40), feet at one point (24, 38). The sets: stand (2, on all fours, breathing),
sit (2, sitting up, a blink), walk (6), run (4), nibble (4, sitting up, a thing at the mouth), wash (4, sitting up, a
thing turned in both hands), reach (2, both hands out in front), look (1, sitting up, head turned to us).
It also paints the proof's strip (strip.png, 480 x 80, seamless end to end) and the window cut-out (window.png, 800 x
600, a panel with two holes) for the strip that scrolls behind a window.
"""

import json, os, math
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "art", "proof")
W, H = 48, 40
FOOT = (24, 38)
DARK = (52, 46, 44, 255)          # outline, the mask, feet, the tail's rings
BODY = (142, 136, 120, 255)       # fur
LIGHT = (222, 214, 190, 255)      # belly, muzzle, the thing he holds
PINK = (214, 120, 110, 255)       # nose, the inside of the ears
CLEAR = (0, 0, 0, 0)


def canvas():
    im = Image.new("RGBA", (W, H), CLEAR)
    return im, ImageDraw.Draw(im)


def blob(d, box, fill, edge=DARK):
    """A filled ellipse with a one-pixel dark edge (hard: PIL's shapes are not smoothed)."""
    x0, y0, x1, y1 = box
    d.ellipse([x0, y0, x1, y1], fill=edge)
    d.ellipse([x0 + 1, y0 + 1, x1 - 1, y1 - 1], fill=fill)


def head(d, cx, cy, r=7, facing="E", shades=False, blink=False, down=0):
    """The head: a round skull, two ears, the dark mask across the eyes, a light muzzle and a pink nose."""
    for ex in ((-4, 3) if facing == "S" else (-3, 2)):
        d.polygon([(cx + ex, cy - r + 1), (cx + ex + 3, cy - r - 4), (cx + ex + 5, cy - r + 1)], fill=DARK)
        d.polygon([(cx + ex + 1, cy - r + 1), (cx + ex + 3, cy - r - 2), (cx + ex + 4, cy - r + 1)], fill=PINK)
    blob(d, (cx - r, cy - r, cx + r, cy + r), BODY)
    if facing == "S":                                   # to us: both eyes in the mask
        d.rectangle([cx - r + 1, cy - 2 + down, cx + r - 1, cy + 2 + down], fill=DARK)
        if shades:
            d.rectangle([cx - r + 1, cy - 2 + down, cx + r - 1, cy + 1 + down], fill=DARK)
            d.point([(cx - 4, cy - 1 + down), (cx + 2, cy - 1 + down)], fill=LIGHT)
        elif not blink:
            d.rectangle([cx - 4, cy - 1 + down, cx - 2, cy + 1 + down], fill=LIGHT); d.rectangle([cx + 2, cy - 1 + down, cx + 4, cy + 1 + down], fill=LIGHT)
            d.point([(cx - 3, cy + down), (cx + 3, cy + down)], fill=DARK)
        d.ellipse([cx - 3, cy + 2 + down, cx + 3, cy + r - 1 + down], fill=LIGHT)
        d.rectangle([cx - 1, cy + 3 + down, cx + 1, cy + 4 + down], fill=PINK)
        return
    # side on, facing E: one eye in the mask, the muzzle forward
    d.rectangle([cx - 2, cy - 2 + down, cx + r - 1, cy + 1 + down], fill=DARK)
    if shades: d.point([(cx + 2, cy - 1 + down)], fill=LIGHT)
    elif not blink: d.rectangle([cx + 1, cy - 1 + down, cx + 3, cy + down], fill=LIGHT); d.point([(cx + 2, cy + down)], fill=DARK)
    d.ellipse([cx + 2, cy + 1 + down, cx + r + 2, cy + r - 1 + down], fill=LIGHT)
    d.rectangle([cx + r, cy + 2 + down, cx + r + 1, cy + 3 + down], fill=PINK)


def tail(d, x, y, up=1, rings=3):
    """A ringed tail curling up and back from the rump at (x, y)."""
    pts = [(x - i * 2, y - int(math.sin(i / 7 * math.pi) * 9 * up) - i) for i in range(8)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=DARK, width=5)
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=DARK if (i // 2) % 2 else BODY, width=3)


def leg(d, x, y0, y1, fwd=0):
    d.line([(x, y0), (x + fwd, y1)], fill=DARK, width=3)
    d.rectangle([x + fwd - 2, y1 - 1, x + fwd + 1, y1], fill=DARK)


def stand(bob=0, legs=(0, 0, 0, 0), stretch=0, shades=False):
    """On all fours, facing E. legs: forward offsets of the four feet (front near, front far, hind near, hind far)."""
    im, d = canvas()
    by = 18 + bob
    tail(d, 11 - stretch, by + 6)
    leg(d, 15 - stretch, by + 10, 38, legs[3]); leg(d, 31 + stretch, by + 10, 38, legs[1])        # the far legs
    blob(d, (9 - stretch, by, 37 + stretch, by + 14 - stretch // 2), BODY)
    d.ellipse([16, by + 7, 32 + stretch, by + 13 - stretch // 2], fill=LIGHT)                      # the belly
    leg(d, 13 - stretch, by + 10, 38, legs[2]); leg(d, 33 + stretch, by + 10, 38, legs[0])        # the near legs
    head(d, 37 + stretch, 15 + bob, shades=shades)
    return im


def sitting(hands="fold", blink=False, headdown=0, thing=None, facing="E", shades=False):
    """Sitting up on the haunches, facing E (or to us for `look`). hands: fold, up (at the mouth), turn (in front, a
    thing between them), out (reaching forward, half or whole)."""
    im, d = canvas()
    tail(d, 15, 30, up=1)
    blob(d, (15, 12, 33, 37), BODY)
    d.ellipse([20, 20, 30, 35], fill=LIGHT)                        # the belly
    d.rectangle([17, 35, 23, 37], fill=DARK); d.rectangle([27, 35, 33, 37], fill=DARK)      # hind feet
    cx, cy = 26, 9 + headdown
    if hands == "fold":
        d.rectangle([24, 22, 31, 25], fill=DARK)
    elif hands == "up":                                            # both hands at the mouth, a thing between them
        d.line([(27, 22), (33, cy + 5)], fill=DARK, width=3); d.line([(25, 22), (31, cy + 6)], fill=DARK, width=3)
        if thing: d.ellipse([32, cy + 4, 36, cy + 8], fill=LIGHT)
    elif hands == "turn":                                          # a thing turned over in front of the chest
        dx = thing or 0
        d.line([(26, 22), (31 + dx, 19)], fill=DARK, width=3); d.line([(26, 24), (33 - dx, 23)], fill=DARK, width=3)
        d.ellipse([31, 18, 36, 23], fill=LIGHT); d.point([(33 + dx // 2, 20)], fill=DARK)
    elif hands == "out":                                           # both hands out flat in front, holding something up
        k = thing or 1
        d.line([(27, 22), (33 + 4 * k, 17 - 2 * k)], fill=DARK, width=3); d.line([(27, 25), (33 + 4 * k, 19 - 2 * k)], fill=DARK, width=3)
        d.ellipse([33 + 4 * k, 14 - 2 * k, 38 + 4 * k, 19 - 2 * k], fill=LIGHT)
    head(d, cx, cy, facing=facing, blink=blink, shades=shades)
    return im


def portrait(shades=False):
    """64 x 64, head and shoulders, facing us: for the team bar."""
    im = Image.new("RGBA", (64, 64), CLEAR)
    d = ImageDraw.Draw(im)
    blob(d, (6, 44, 58, 70), BODY)                                 # the shoulders
    d.ellipse([20, 50, 44, 66], fill=LIGHT)
    for ex in (8, 36):
        d.polygon([(ex, 26), (ex + 8, 4), (ex + 18, 24)], fill=DARK); d.polygon([(ex + 3, 24), (ex + 8, 9), (ex + 14, 23)], fill=PINK)
    blob(d, (10, 12, 54, 52), BODY)
    d.rectangle([12, 25, 52, 36], fill=DARK)                      # the mask
    if shades:
        d.rectangle([12, 24, 52, 37], fill=DARK)
        d.rectangle([17, 27, 20, 28], fill=LIGHT); d.rectangle([43, 27, 46, 28], fill=LIGHT)
        d.rectangle([30, 29, 34, 30], fill=BODY)
    else:
        for ex in (17, 39):
            d.ellipse([ex, 27, ex + 8, 34], fill=LIGHT); d.rectangle([ex + 3, 29, ex + 5, 32], fill=DARK)
    d.ellipse([22, 36, 42, 50], fill=LIGHT)                        # the muzzle
    d.polygon([(28, 39), (36, 39), (32, 44)], fill=PINK)
    d.line([(32, 44), (32, 47)], fill=DARK)
    return im


def shaded(im):
    return im


def frames(shades):
    out = {}
    out["stand"] = [stand(0, shades=shades), stand(1, shades=shades)]
    out["sit"] = [sitting(shades=shades), sitting(blink=True, shades=shades)]
    # six walking frames: the near front and far hind legs go together, the others against them; the body bobs
    swing = [4, 2, 0, -3, -1, 1]
    out["walk"] = [stand(bob=(1 if i in (1, 4) else 0), legs=(swing[i], swing[(i + 3) % 6], swing[(i + 3) % 6], swing[i]), shades=shades) for i in range(6)]
    # a scamper: the body stretches with the legs flung out, then bunches
    out["run"] = [stand(bob=0, legs=(6, 5, -6, -5), stretch=3, shades=shades), stand(bob=2, legs=(0, -1, 1, 0), stretch=-2, shades=shades),
                  stand(bob=0, legs=(5, 6, -5, -6), stretch=3, shades=shades), stand(bob=1, legs=(-1, 0, 0, 1), stretch=-2, shades=shades)]
    out["nibble"] = [sitting(hands="up", thing=True, headdown=h, shades=shades) for h in (0, 1, 2, 1)]
    out["wash"] = [sitting(hands="turn", thing=t, shades=shades) for t in (0, 1, 0, -1)]
    out["reach"] = [sitting(hands="out", thing=0, shades=shades), sitting(hands="out", thing=1, shades=shades)]
    out["look"] = [sitting(facing="S", shades=shades)]
    return out


def strip():
    """The desert going by: 480 wide, 80 high, its right edge continuing into its left (every shape is periodic in x)."""
    SW, SH = 480, 80
    im = Image.new("RGBA", (SW, SH), (255, 255, 255, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, SW, 30], fill=(176, 206, 232, 255))
    d.rectangle([0, 30, SW, 44], fill=(206, 222, 236, 255))
    far = [(x, 46 - int(8 * math.sin(x / SW * 2 * math.pi * 3) + 5 * math.sin(x / SW * 2 * math.pi * 7 + 1))) for x in range(0, SW + 1, 4)]
    d.polygon([(0, SH), *far, (SW, SH)], fill=(150, 130, 160, 255))
    near = [(x, 56 - int(5 * math.sin(x / SW * 2 * math.pi * 5 + 2) + 3 * math.sin(x / SW * 2 * math.pi * 11))) for x in range(0, SW + 1, 4)]
    d.polygon([(0, SH), *near, (SW, SH)], fill=(196, 150, 104, 255))
    d.rectangle([0, 62, SW, SH], fill=(222, 186, 124, 255))
    d.rectangle([0, 61, SW, 62], fill=(170, 130, 90, 255))
    for cx in (40, 150, 260, 300, 410):                              # cacti: a post with two arms, well in from the edges
        d.rectangle([cx - 2, 46, cx + 2, 64], fill=(86, 128, 76, 255))
        d.rectangle([cx - 7, 50, cx - 3, 53], fill=(86, 128, 76, 255)); d.rectangle([cx - 7, 50, cx - 5, 56], fill=(86, 128, 76, 255))
        d.rectangle([cx + 3, 52, cx + 7, 55], fill=(86, 128, 76, 255)); d.rectangle([cx + 5, 48, cx + 7, 55], fill=(86, 128, 76, 255))
    for rx in (90, 210, 350, 450):
        d.ellipse([rx - 6, 64, rx + 6, 70], fill=(160, 120, 90, 255))
    return im


def window():
    """A cut-out the size of the stage: a panel with two window holes, laid over the sand (its base is row 372)."""
    im = Image.new("RGBA", (800, 600), CLEAR)
    d = ImageDraw.Draw(im)
    d.rectangle([440, 300, 640, 372], fill=(96, 92, 104, 255))
    d.rectangle([443, 303, 637, 369], fill=(132, 128, 140, 255))
    d.rectangle([440, 366, 640, 372], fill=(72, 68, 78, 255))
    for x0 in (452, 550):
        d.rectangle([x0 - 3, 315, x0 + 81, 365], fill=(60, 56, 64, 255))
        d.rectangle([x0, 318, x0 + 78, 362], fill=CLEAR)                 # the hole: the strip shows through it
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    names = {}
    for variant, prefix in ((False, "critter-"), (True, "critter-shades-")):
        for setname, pics in frames(variant).items():
            files = []
            for i, pic in enumerate(pics):
                name = f"{prefix}{setname}-{i}.png"
                pic.save(os.path.join(OUT, name))
                files.append(name)
            if not variant: names[setname] = files
        portrait(variant).save(os.path.join(OUT, f"{prefix}face.png"))
    sidecar = {
        "id": "critter", "face": "E",
        "foot": list(FOOT),
        "tall": {"stand": 30, "sit": 38},
        "stride": 40, "pace": 120,
        "frames": names,
        "fps": {"stand": 1.5, "sit": 1.5, "walk": 8, "run": 10, "nibble": 6, "wash": 5, "reach": 2, "look": 1},
        "fidgets": ["look", "wash"],
        "portrait": "critter-face.png",
        "variants": {"shades": {"prefix": "critter-shades-", "portrait": "critter-shades-face.png"}},
    }
    with open(os.path.join(OUT, "critter.json"), "w") as f:
        json.dump(sidecar, f, indent=2)
    strip().save(os.path.join(OUT, "strip.png"))
    window().save(os.path.join(OUT, "window.png"))
    print(f"wrote {len(os.listdir(OUT))} files to {OUT}")


if __name__ == "__main__":
    main()

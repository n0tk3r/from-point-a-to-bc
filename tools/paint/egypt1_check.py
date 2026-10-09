"""Checks on the finished pictures of egypt1 (run after egypt1.py): python3 egypt1_check.py

  1. palms.png and front.png are pixel for pixel what they were (out/egypt1-before/); back.png too, except in the
     two places round three repainted (the reed clump where the donkey now drinks, and Lot's bundle); every other
     picture but donkey.png is pixel for pixel the round-two delivery (out/egypt1-before/round2/).
  2. wagon.png with mirror.png laid on it is the old wagon.png wherever that was solid; where the old one was
     clear inside the car (thin paint) the new one shows exactly the backdrop.
  3. Each open piece of luggage covers every pixel where the shut piece shows, and no open piece leaves
     a pixel with nothing behind it.
  4. Every combination of states is laid together into out/egypt1-look/states.png, to look at.
  5. The donkey drinks: its muzzle is in the river, its hooves on the sand, its rings on the water, and it is clear
     of the wagon and the boy's prints. Every standing place is open floor even with the margin the game keeps
     round blocked ground, and the place to talk to Lot is clear of the ground he sits on."""
import itertools, sys
import numpy as np
from PIL import Image
from brush import *
import wagon

NEW, OLD, R2 = "out/egypt1", "out/egypt1-before", "out/egypt1-before/round2"
WAGON = (722, 540)
REPAINTED = {"the reed clump where the donkey drinks": (120, 375, 200, 440), "Lot's bundle": (360, 410, 412, 440)}   # x0, y0, x1, y1
ok = True


def rgba(path):
    return np.asarray(Image.open(path).convert("RGBA")).astype(np.int16)


def say(good, text):
    global ok
    ok = ok and bool(good)
    print(("ok    " if good else "WRONG ") + text)


for name in ("palms", "front"):
    a, b = rgba(f"{NEW}/{name}.png"), rgba(f"{OLD}/{name}.png")
    same = a.shape == b.shape and not np.any(a != b)
    say(same, f"{name}.png is pixel-identical to the approved copy" if same else f"{name}.png differs in {int(np.any(a != b, axis=2).sum())} pixels")
a, b = rgba(f"{NEW}/back.png"), rgba(f"{OLD}/back.png")
differ = np.any(a != b, axis=2)
allowed = np.zeros_like(differ)
for x0, y0, x1, y1 in REPAINTED.values():
    allowed[y0:y1, x0:x1] = True
say(not np.any(differ & ~allowed), f"back.png is pixel-identical to the approved copy except in the places repainted in round three "
    f"({', '.join(f'{k}: {int(differ[y0:y1, x0:x1].sum())} pixels' for k, (x0, y0, x1, y1) in REPAINTED.items())}; elsewhere {int((differ & ~allowed).sum())})")
same = []
for name in sorted(n[:-4] for n in __import__("os").listdir(R2) if n.endswith(".png")):
    if name in ("back", "donkey"):
        continue
    a, b = rgba(f"{NEW}/{name}.png"), rgba(f"{R2}/{name}.png")
    if a.shape == b.shape and not np.any(a != b):
        same.append(name)
    else:
        say(False, f"{name}.png has changed since round two")
say(len(same) == 14, f"{len(same)} pictures are pixel-identical to the round-two delivery: {', '.join(same)}")

old, new, mir, back = rgba(f"{OLD}/wagon.png"), rgba(f"{NEW}/wagon.png"), rgba(f"{NEW}/mirror.png"), rgba(f"{NEW}/back.png")
both = np.where(mir[..., 3:] > 0, mir, new)
was = old[..., 3] > 0
say(not np.any(both[was] != old[was]), f"wagon.png + mirror.png = the approved wagon on all {int(was.sum())} of its pixels")
extra = (both[..., 3] > 0) & ~was
say(not np.any(both[extra][:, :3] != back[extra][:, :3]), f"the {int(extra.sum())} pixels now filled in the wagon (thin paint: it was see-through) show exactly the backdrop")
gone = (mir[..., 3] > 0)
ys, xs = np.nonzero(gone)
print(f"      mirror.png: {int(gone.sum())} pixels, x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()}")
say(not np.any((new[..., 3] == 0) & gone), "wagon.png is solid under the mirror")
changed = np.any(new != old, axis=2) & was
say(not np.any(changed & ~gone), f"wagon.png differs from the approved one only under the mirror ({int(changed.sum())} pixels) and in the filled places")

shape = old.shape[:2]
ca, aa, lca, laa = wagon.wagon(shape, WAGON)
shut = np.zeros(shape + (3,), dtype=F32)
over(over(shut, ca, aa), lca, laa)
cuts = {}
for p in wagon.PIECES:
    c0, a0, lc0, la0 = wagon.wagon(shape, WAGON, take=(p,))
    gone_ = np.zeros(shape + (3,), dtype=F32)
    over(over(gone_, c0, a0), lc0, la0)
    seen = (np.abs(shut - gone_).sum(axis=2) + np.abs(np.maximum(aa, laa) - np.maximum(a0, la0)) > 0.004) & was     # (the filled places show only backdrop)
    cut = rgba(f"{NEW}/{p}-open.png")
    cuts[p] = cut
    left = seen & (cut[..., 3] == 0)
    ys, xs = np.nonzero(cut[..., 3] > 0)
    say(not left.any(), f"{p}-open.png covers all {int(seen.sum())} pixels of the shut {p} ({int((cut[..., 3] > 0).sum())} pixels, x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()})")
for a, b in itertools.combinations(wagon.PIECES, 2):
    print(f"      {a}-open and {b}-open share {int(((cuts[a][..., 3] > 0) & (cuts[b][..., 3] > 0)).sum())} pixels (the later one is laid on top)")

# every combination, to look at
box, k = (575, 336, 775, 462), 3
tiles = []
for combo in itertools.product((0, 1), repeat=3):
    im = Image.open(f"{NEW}/back.png").convert("RGBA")
    im.alpha_composite(Image.open(f"{NEW}/wagon.png").convert("RGBA"))
    for on, p in zip(combo, wagon.PIECES):
        if on:
            im.alpha_composite(Image.open(f"{NEW}/{p}-open.png").convert("RGBA"))
    tiles.append(im.crop(box).resize(((box[2] - box[0]) * k, (box[3] - box[1]) * k), Image.NEAREST))
w, h = tiles[0].size
sheet = Image.new("RGB", (w * 2, h * 4))
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % 2) * w, (i // 2) * h))
sheet.save("out/egypt1-look/states.png")
# the palms cut into three
whole = rgba(f"{NEW}/palms.png")
parts = [rgba(f"{NEW}/palm-{i}.png") for i in (1, 2, 3)]
together = np.zeros_like(whole)
count = np.zeros(whole.shape[:2], dtype=int)
for p in parts:
    together = np.where(p[..., 3:] > 0, p, together)
    count += p[..., 3] > 0
say(not np.any(together != whole) and count.max() == 1, "palm-1.png + palm-2.png + palm-3.png = palms.png, and no pixel is in two of them")

# the steam, the layout
import json, os
frames = [Image.open(f"{NEW}/steam-{i}.png") for i in range(4)]
say(all(f.mode == "RGBA" and f.size == frames[0].size for f in frames), f"four steam frames, RGBA, each {frames[0].size[0]} x {frames[0].size[1]}")
doc = json.load(open(f"{NEW}/layout.json"))


def inside(pt, poly):
    x, y = pt
    hit = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            hit = not hit
    return hit


spots = [(t["id"], t["stand"]) for t in doc["things"] + doc["exits"]] + list(doc["marks"].items())
bad = [name for name, pt in spots if not inside(pt, doc["walk"]) or any(inside(pt, b) for b in doc["blocked"])]
say(not bad, f"all {len(spots)} standing places and marks are on open floor" if not bad else f"not on open floor: {bad}")


def floor(doc, more=()):
    """Where the game lets a figure stand, worked out as its WalkMap does: inside the walk outline, and not within
    12 pixels across or 5 up or down of any blocked outline (a pixel counts when its middle is inside)."""
    import math
    ok = np.zeros((600, 800), dtype=bool)

    def rows(poly, fill):
        ys = [p[1] for p in poly]
        for y in range(max(0, math.floor(min(ys))), min(599, math.ceil(max(ys))) + 1):
            py, xs = y + 0.5, []
            for (xi, yi), (xj, yj) in zip(poly, poly[-1:] + poly[:-1]):
                if (yi > py) != (yj > py):
                    xs.append(xi + (py - yi) / (yj - yi) * (xj - xi))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                a, b = max(0, math.ceil(xs[k] - 0.5)), min(799, math.ceil(xs[k + 1] - 0.5) - 1)
                if a <= b:
                    fill(y, a, b)
    rows(doc["walk"], lambda y, a, b: ok[y].__setitem__(slice(a, b + 1), True))

    def block(y, a, b):
        ok[max(0, y - 5):min(599, y + 5) + 1, max(0, a - 12):min(799, b + 12) + 1] = False
    for poly in list(doc["blocked"]) + list(more):
        rows(poly, block)
    return ok


lot = doc["lot"]
lx, ly = lot["hips"]
s = (ly - doc["horizon"]) / (doc["full"] - doc["horizon"])
seat = [[lx - 32 * s, ly - 12], [lx + 32 * s, ly - 12], [lx + 32 * s, ly + 8], [lx - 32 * s, ly + 8]]     # what the game blocks round a person on his mark
ok_floor = floor(doc, [seat, lot["solid"]])
stands = [(t["id"], t["stand"]) for t in doc["things"] + doc["exits"]] + [("talkToLot", doc["marks"]["talkToLot"]), ("dad", doc["marks"]["dad"])]
bad = [name for name, (x, y) in stands if not ok_floor[int(y), int(x)]]
say(not bad, f"all {len(stands)} standing places are open floor as the game works it out (12 px across and 5 up or down clear of blocked ground, "
    f"Lot sitting on his mark)" if not bad else f"the game would move Dad off: {bad}")
say(inside(lot["hips"], doc["walk"]) and not any(inside(lot["hips"], b) for b in doc["blocked"]) and lot["hips"] == doc["marks"]["lot"],
    f"Lot's mark {lot['hips']} is on the sand, and nothing painted stands on it")

# the donkey drinks
import egypt1 as E, egypt1_donkey as D
water = E.river() > 0.5
mx, my = D.muzzle(E.DONKEY, E.DONKEY_SCALE)
hooves = D.hooves(E.DONKEY, E.DONKEY_SCALE)
dk = rgba(f"{NEW}/donkey.png")[..., 3] > 0
_, da, _, dla = D.donkey((600, 800), E.DONKEY, E.DONKEY_SCALE, jar_at=None, drink=D.DRINK)
body = (da > 0.5) | (dla > 0.5)
say(water[int(round(my)), int(round(mx))] and all(not water[int(round(hy)), int(round(hx))] for hx, hy, r in hooves),
    f"the donkey's muzzle ({mx:.1f}, {my:.1f}) is in the river and its four hooves are on the sand (x {min(h[0] for h in hooves):.1f}..{max(h[0] for h in hooves):.1f})")
ys, xs = np.nonzero(dk & ~body & water)                     # on the water, and not the animal: the rings
say(len(xs) and xs.min() > mx - 22 and xs.max() < mx + 22 and ys.min() > my - 6 and ys.max() < my + 6,
    f"besides the animal itself, all the cut-out has on the water is the rings round its muzzle and its head's shadow at the edge ({len(xs)} pixels, x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()})")
plane = [p for p in doc["planes"] if p["id"] == "donkey"][0]
say(plane["base"] == int(round(hooves[0][1])), f"the donkey plane's base {plane['base']} is the line of its near hooves")
keep_clear = {"the wagon": [p for p in doc["planes"] if p["id"] == "wagon"][0]["solid"],
              "the boy's prints": [t for t in doc["things"] if t["id"] == "footprints"][0]["shape"]["poly"], "the track": doc["exits"][0]["shape"]["poly"]}
hit = [k for k, poly in keep_clear.items() if any(inside((x + 0.5, y + 0.5), poly) for y, x in zip(*np.nonzero(dk)))]
say(not hit, "the donkey is clear of the wagon, the boy's prints and the track" if not hit else f"the donkey overlaps {hit}")
wanted = ["river", "reeds", "footprints", "pyramid", "boat", "wagon", "hood", "glovebox", "mirror", "suitcase", "trunk", "cooler", "donkey", "block"]
have = [t["id"] for t in doc["things"]]
say(all(w in have for w in wanted) and doc["exits"][0]["id"] == "track", "layout.json names every thing in the brief, and the track as an exit")
files = [p["file"] for p in doc["planes"] if "file" in p] + [f for p in doc["planes"] for f in p.get("frames", [])] + [p["file"] for p in doc["palms_split"]["planes"]]
say(all(os.path.exists(f"{NEW}/{f}") for f in files), f"every picture named in layout.json exists ({len(files)} files)")

# the things to carry
ITEMS = ["reed", "map", "pass", "flashlight", "rootbeer", "shade", "carmirror", "sunglasses", "coppermirror", "toga", "tunic", "breakfast", "incense", "coin", "note",
         "phone", "quarter", "gum"]
good = True
for n in ITEMS:
    p = f"out/items/{n}.png"
    if not os.path.exists(p):
        good = False
        continue
    im = Image.open(p)
    a = np.asarray(im.convert("RGBA"))[..., 3]
    corners = [a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]]
    good = good and im.mode == "RGBA" and im.size == (64, 64) and max(corners) == 0 and (a > 128).mean() > 0.12
say(good, f"{len(ITEMS)} inventory pictures, each 64 x 64 RGBA on a clear ground")
print("all checks passed" if ok else "SOMETHING IS WRONG")
sys.exit(0 if ok else 1)

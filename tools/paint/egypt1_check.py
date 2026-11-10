"""Checks on the finished pictures of egypt1 (run after egypt1.py): python3 egypt1_check.py

Round twenty-three (DEPTH.md) painted the backdrop and the papyrus again and added the near plane, the camera and
every number of the scene as they were. So the first two checks no longer ask for the same pixels: they ask that every
cut-out is WHERE it was and the SHAPE it was. The reference is the painting as it was before the round, in
out/egypt1-before/ (run the script at that revision into it); without that folder, the pictures installed in the game
(whose outlines are the painting's own: the paints keep every edge), which says something only before installing.

  1. Every cut-out that was there before has its outline, pixel for pixel: the palms (whole and split), the donkey,
     the wagon, its mirror, the three open pieces of luggage and the trunk's two emptier pictures. The steam's frames
     are the same pixels. The near palm is the same pixels; the two farther palms differ only by the air before them.
     layout.json's walk, blocked ground, things, exits, marks, Lot and steam are what they were.
  2. wagon.png with mirror.png laid on it is the old wagon: the same outline, and the car itself the same painting
     (it is still brushed on the first painting's sand: egypt1.WAGON_SAND), but for the sand heaped at its nose and
     the thin places, which are made of the ground and show exactly the backdrop.
  3. Each open piece of luggage covers every pixel where the shut piece shows, and no open piece leaves
     a pixel with nothing behind it.
  4. Every combination of states is laid together into out/egypt1-look/states.png, to look at.
  5. The donkey drinks: its muzzle is in the river, its hooves on the sand, its rings on the water, and it is clear
     of the wagon and the boy's prints. Every standing place is open floor even with the margin the game keeps
     round blocked ground, and the place to talk to Lot is clear of the ground he sits on.
  6. The near plane (round twenty-three): its three files are there, they cover 12 to 25 per cent of the picture
     together, nothing of them stands where the luggage pops out and lies, the fronds hang from the top (their sway is
     anchored there), the papyrus is as tall as it was (so is its sway), and Lot's seat is in the near palm's shade.
     (What the near plane hides of each clickable thing: `python3 depth_check.py egypt-crash --art out/egypt1`.)"""
import itertools, json, os, sys
import numpy as np
from PIL import Image
from brush import *
import wagon

NEW = "out/egypt1"
PAINTED_BEFORE = os.path.isdir("out/egypt1-before")
OLD = "out/egypt1-before" if PAINTED_BEFORE else "../../art/scenes/egypt-crash"
WAGON = (722, 540)
ok = True


def rgba(path):
    return np.asarray(Image.open(path).convert("RGBA")).astype(np.int16)


def say(good, text):
    global ok
    ok = ok and bool(good)
    print(("ok    " if good else "WRONG ") + text)


print(f"      compared with {OLD}" + ("" if PAINTED_BEFORE else " (the installed pictures: no out/egypt1-before/)"))
CUTS = ["palms", "palm-1", "palm-2", "palm-3", "donkey", "wagon", "mirror", "suitcase-open", "trunk-open", "trunk-open-1", "trunk-open-2", "cooler-open"]
moved = [n for n in CUTS if not np.array_equal(rgba(f"{NEW}/{n}.png")[..., 3] > 0, rgba(f"{OLD}/{n}.png")[..., 3] > 0)]
say(not moved, f"all {len(CUTS)} cut-outs that were there before round twenty-three keep their outline, pixel for pixel: {', '.join(CUTS)}" if not moved
    else f"these cut-outs have changed their outline: {', '.join(moved)}")
steam = [i for i in range(4) if not np.array_equal(rgba(f"{NEW}/steam-{i}.png"), rgba(f"{OLD}/steam-{i}.png"))]
say(not steam, "the steam's four frames are pixel for pixel what they were" if not steam else f"steam frames changed: {steam}")
if PAINTED_BEFORE:
    def moved_by(i):
        a, b = rgba(f"{NEW}/palm-{i}.png"), rgba(f"{OLD}/palm-{i}.png")
        return float(np.abs(a - b)[a[..., 3] > 0][:, :3].mean())
    d1, d2, d3 = moved_by(1), moved_by(2), moved_by(3)
    say(d1 < 4 and d1 < d2 < d3 < 40, f"the near palm is the painting it was (mean difference {d1:.1f} levels: the palette's), and the two farther palms differ only by the air "
        f"before them, the farthest most ({d2:.1f} and {d3:.1f} levels)")
    was_doc, now_doc = json.load(open(f"{OLD}/layout.json")), json.load(open(f"{NEW}/layout.json"))
    kept = [k for k in ("horizon", "full", "walk", "blocked", "things", "exits", "marks", "lot", "steam") if was_doc[k] == now_doc[k]]
    say(len(kept) == 9, f"layout.json's {', '.join(kept)} are what they were (its planes have gained near.png and near-fronds.png, its fx the fronds' sway)")
    gained = [p["id"] for p in now_doc["planes"] if p["id"] not in [q["id"] for q in was_doc["planes"]]] + [f["id"] for f in now_doc["fx"] if f["id"] not in [g["id"] for g in was_doc["fx"]]]
    same_fx = all(f == g for f in was_doc["fx"] for g in now_doc["fx"] if f["id"] == g["id"] and f["id"] != "papyrus")
    say(sorted(gained) == ["near", "near", "near-fronds", "near-fronds"][1:] or sorted(gained) == ["near", "near-fronds", "near-fronds"], f"what layout.json has gained: {', '.join(gained)}; every fx that was there is as it was: {same_fx}")

old, new, mir, back = rgba(f"{OLD}/wagon.png"), rgba(f"{NEW}/wagon.png"), rgba(f"{NEW}/mirror.png"), rgba(f"{NEW}/back.png")
both = np.where(mir[..., 3:] > 0, mir, new)
was = old[..., 3] > 0
window = np.zeros(was.shape, dtype=bool)                    # CAR-13P: round thirteen rolled the driver's window down: only inside this box
window[455:493, 618:663] = True
mult, heap = wagon.drift(was.shape, WAGON)                  # the sand heaped at its nose: made of the ground it lies on
faint, _ = wagon.thin(was.shape, WAGON)                     # and the thin places, filled with the ground that showed there
car = was & ~(heap > 0.5) & ~faint
if PAINTED_BEFORE:
    diff = np.abs(both - old)[car][:, :3]
    say(diff.mean() < 5 and (diff.max(axis=1) > 40).mean() < 0.01, f"wagon.png + mirror.png = the approved wagon on the {int(car.sum())} pixels that are the car itself "
        f"(the same brushing: mean difference {diff.mean():.1f} levels, {(diff.max(axis=1) > 40).mean() * 100:.2f}% of them over 40: its palette now holds the new sand's colours)")
say(not np.any(new[faint][:, :3] != back[faint][:, :3]), f"the {int(faint.sum())} pixels filled in the wagon (thin paint: it was see-through) show exactly the backdrop")
gone = (mir[..., 3] > 0)
ys, xs = np.nonzero(gone)
print(f"      mirror.png: {int(gone.sum())} pixels, x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()}")
say(not np.any((new[..., 3] == 0) & gone), "wagon.png is solid under the mirror")
say(np.array_equal(new[..., 3] > 0, was) and np.array_equal(mir[..., 3] > 0, rgba(f"{OLD}/mirror.png")[..., 3] > 0), "the wagon and its mirror are where they were: the same outlines")

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
wanted = ["river", "reeds", "footprints", "pyramid", "boat", "wagon", "hood", "inside", "mirror", "suitcase", "trunk", "cooler", "donkey", "block"]     # CAR-13P: "inside" (was "glovebox")
have = [t["id"] for t in doc["things"]]
say(all(w in have for w in wanted) and doc["exits"][0]["id"] == "track", "layout.json names every thing in the brief, and the track as an exit")
files = [p["file"] for p in doc["planes"] if "file" in p] + [f for p in doc["planes"] for f in p.get("frames", [])] + [p["file"] for p in doc["palms_split"]["planes"]]
say(all(os.path.exists(f"{NEW}/{f}") for f in files), f"every picture named in layout.json exists ({len(files)} files)")

# the near plane (round twenty-three)
near_files = ["front", "near", "near-fronds"]
have = [n for n in near_files if os.path.exists(f"{NEW}/{n}.png") and Image.open(f"{NEW}/{n}.png").size == (800, 600) and Image.open(f"{NEW}/{n}.png").mode == "P"]
say(have == near_files, f"the near plane's three files are there, each 800 x 600 with a palette and a clear colour: {', '.join(have)}")
masks = {n: rgba(f"{NEW}/{n}.png")[..., 3] > 0 for n in near_files}
together = masks["front"] | masks["near"] | masks["near-fronds"]
share = together.mean()
say(0.12 <= share <= 0.25, f"together they cover {share * 100:.1f}% of the picture (12 to 25): the papyrus {masks['front'].mean() * 100:.1f}, the trunk and the lip {masks['near'].mean() * 100:.1f}, the fronds {masks['near-fronds'].mean() * 100:.1f}")
pop = int(together[540:600, 640:800].sum())
say(pop == 0, f"nothing of the near plane stands where the luggage pops out and lies (x 640.., y 540..: {pop} pixels)")
rows = np.nonzero(masks["near-fronds"].any(axis=1))[0]
say(rows.min() == 0 and rows.max() < 150, f"the fronds hang from the top edge: rows {rows.min()} to {rows.max()} (their sway is anchored at the top row)")
top_now = int(np.nonzero(masks["front"].any(axis=1))[0].min())
top_was = int(np.nonzero((rgba(f"{OLD}/front.png")[..., 3] > 0).any(axis=1))[0].min())
say(abs(top_now - top_was) <= 24, f"the papyrus reaches row {top_now} (it was {top_was}): its sway, rooted at the bottom, moves it as it did")
lum = (back[..., :3] / 255.0) @ np.array([0.30, 0.55, 0.15])
lx, ly = doc["marks"]["lot"]
seat, sun = lum[ly - 6:ly + 6, lx - 20:lx + 20].mean(), lum[ly - 6:ly + 6, lx - 110:lx - 80].mean()
say(seat < sun * 0.86, f"Lot's seat {doc['marks']['lot']} is in the near palm's shade: the sand there is {(1 - seat / sun) * 100:.0f}% darker than the sunlit sand beside it")

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

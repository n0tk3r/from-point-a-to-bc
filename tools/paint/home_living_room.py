"""The living room at 9:40 at night (scene `home-living-room`).

    python3 home_living_room.py          everything: the backdrop, the cut-outs, layout.json, the comp
    python3 home_living_room.py fast     no brush pass (to compose); `draft` as well: at the picture's own size, quicker still
    python3 home_living_room_check.py    afterwards: the layout drawn over the comp, and the cut-outs on grey

HOW IT IS SEEN. One camera (room.View, the numbers in home_living_room_model.py): we stand at the front right of
a two-storey room, 3.3 m up, turned a little left. Lines running back meet at (621, 150); lines running across
meet far off to the left. Every surface and every thing is laid in the room's own centimetres through that
camera (home_living_room_kit.py), so floor, walls, stairs, furniture, light and shadows agree.

LIGHT. Night. Warm: the leaded-glass pendant low over the dinner table (front right), the reading lamp by Dad's
armchair (front left), the lamp on the piano (back right), the kitchen's light coming through its doorway and
across the rug, a lamp left on upstairs. Cool: the moon through the tall stair window, falling down the upper
stairs and across the floor between the rug and the armchair as the window's own shape, slanted, with the stairs'
stepped shadow and the banister's bars cut into its near edge. Everything no lamp reaches goes blue-violet.
(The moon's light is worked out with the stairs and the rail in its way: see Lamps.bake_moon in the kit.)

THREE TONES. Light: the tablecloth under the pendant, the kitchen, the lampshades, the moon and its patch.
Middle: the rug and the floor round it, the woodwork, the wall under the landing. Dark: the upper walls and the
ceiling, the under-stairs end, and the two near corners (the armchair's back, the chairs against the cloth).

WHERE THINGS ARE (left to right, back to front): tall window and family photographs up the stair wall; stairs
with a red runner and white banister; panelled side with the low cupboard door ajar; bookcase; kitchen doorway;
the framed "We the People"; clock (twenty to ten); piano with lamp, hymnal and bench; red front door with a fan
of night-blue glass, the sampler over it, coats on the right-hand wall. Upstairs: three doors behind a white
railing, a lamp on the hall table. Over the rug an unlit brass chandelier. Front left: Dad's leather armchair
seen from behind, crossword and pencil on its arm, reading lamp, basket of newspapers, slippers. Front right:
the table running away from us, white cloth, five places (two untouched), Dad's chair at the head facing us,
the open Bible beside his plate.
"""
import json
import os
import subprocess
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, over, lerp, blur, strokes, warp, noise, palette_of, tint
import letter
import home_living_room_model as M
from home_living_room_kit import Layer, tone, finish, stitch_mask, put_mask, STITCH, SMALL, col
from home_living_room_room import Room, BX, FL, TAG, V, G
from home_living_room_things import Things

ID = M.ID
OUT = "out/" + ID
W, H = 800, 600
WOBBLE = dict(amount=0.75, cell=30.0, seed=9)               # ruled edges wander by most of a pixel, as a hand's do


def show(pic, name):
    Image.fromarray((np.clip(pic, 0, 1) * 255).astype(np.uint8)).save(name)


def wob(a):
    return warp(a, **WOBBLE)


def atmosphere(pic):
    """Painter's license over the block-in: a bloom of light round each lit shade, and corners that fall away
    (the upper ones into the cool of the night, the lower ones deeper and warmer) to hold the eye in the room."""
    from brush import glow, tint, grid
    x, y = grid((H, W))
    for name, r, k, c in (("pendant", 46, 0.20, (1.0, 0.74, 0.38)), ("reading", 54, 0.24, (1.0, 0.76, 0.42)), ("piano", 30, 0.24, (1.0, 0.78, 0.46)),
                          ("upstairs", 30, 0.26, (1.0, 0.76, 0.44))):
        px_, py_ = V.pt(*M.LIGHTS[name])
        d2 = (x - px_) ** 2 + (y - py_) ** 2
        glow(pic, c, (k * np.exp(-d2 / (2 * r * r)) + k * 0.6 * np.exp(-d2 / (2 * (r * 0.4) ** 2))).astype(F32))
    top = np.clip((230 - y) / 230, 0, 1) ** 1.4 * (0.35 + 0.65 * np.clip(np.abs(x - 430) / 400, 0, 1))
    tint(pic, (0.56, 0.66, 0.92), (top * 0.52).astype(F32))
    low = np.clip((y - 400) / 200, 0, 1) ** 1.5 * (0.25 + 0.75 * np.clip(np.abs(x - 400) / 400, 0, 1) ** 1.3)
    tint(pic, (0.80, 0.56, 0.44), (low * 0.55).astype(F32))
    # no wall is one flat color: patches a little lighter and darker, a little warmer and cooler, as a brush leaves them
    n1, n2 = noise((H, W), 70, 31, 4) - 0.5, noise((H, W), 110, 32, 3) - 0.5
    pic *= (1 + 0.12 * n1)[..., None]
    pic[..., 0] *= 1 + 0.07 * n2
    pic[..., 2] *= 1 - 0.09 * n2
    return np.clip(pic, 0, 1)


def behind(z_here, z_all, reach=(1, 2, 4), weights=(0.45, 0.33, 0.22)):
    """Where the picture shows something lying just behind the edge of a nearer thing (within about a metre of
    it): 0..1. There a painter puts a little dark, to lift the nearer thing off what is behind it."""
    out = np.zeros(z_here.shape, dtype=F32)
    # (a floor or wall that runs away from us changes depth from pixel to pixel by itself: allow for that slope)
    dx = np.minimum(np.abs(np.roll(z_here, 1, 1) - z_here), np.abs(np.roll(z_here, -1, 1) - z_here))
    dy = np.minimum(np.abs(np.roll(z_here, 1, 0) - z_here), np.abs(np.roll(z_here, -1, 0) - z_here))
    slope = np.hypot(dx, dy) * 1.6 + 0.5
    for r, w in zip(reach, weights):
        zmin = z_all.copy()
        for dy_ in (-r, 0, r):
            for dx_ in (-r, 0, r):
                if dy_ or dx_:
                    zmin = np.minimum(zmin, np.roll(np.roll(z_all, dy_, 0), dx_, 1))
        gap = z_here - zmin - slope * r * 1.5
        out += w * np.clip(gap / 4.0, 0, 1) * np.clip(1.0 - (gap - 40.0) / 90.0, 0, 1)
    out[:4], out[-4:], out[:, :4], out[:, -4:] = 0, 0, 0, 0
    return np.clip(blur(out, 0.7), 0, 1)


def firm(pic, amount=0.45, radius=2.6, rich=1.05):
    """Firmer drawing and richer color: edges are stated a little more strongly than they fell, as a painter
    would state them, and color is pushed away from grey."""
    soft = blur(pic, radius)
    out = pic + (pic - soft) * amount
    grey = (out @ np.array([0.3, 0.55, 0.15], dtype=F32))[..., None]
    return np.clip(grey + (out - grey) * rich, 0, 1).astype(F32)


def crisp_mask(ref, base=0.26, gain=14.0):
    """Where the picture has edges and small things: there the brushwork gives way to the crisp drawing."""
    lum = ref @ np.array([0.3, 0.55, 0.15], dtype=F32)
    e = np.abs(lum - blur(lum, 1.6)) + 0.5 * np.abs(ref - blur(ref, 1.6)).sum(axis=2)
    return np.clip(base + blur(e, 0.8) * gain, 0, 0.95).astype(F32)


# ---------------------------------------------------------------- lettering, over the brushwork
def letter_frame(pic):
    """The print's three large words, in a clerk's hand, at the head of the parchment."""
    f = FL["frame"]
    x0, x1, y1 = f[2] + 5, f[3] - 5, f[5] - 5
    a, b = V.pt(x0, y1, 3.6), V.pt(x1, y1, 3.6)
    slope = (b[1] - a[1]) / (b[0] - a[0])
    cx = (a[0] + b[0]) / 2
    cy = (a[1] + b[1]) / 2
    ink = (0.11, 0.065, 0.045)
    letter.paint(pic, "We the", (cx + 0.5, cy + 9.0), 13.6, ink, amount=0.98, hand=True, anchor="mm", rough=0.0, slant=-slope * 0 + slope)
    letter.paint(pic, "People", (cx + 0.5, cy + 21.5), 13.6, ink, amount=0.98, hand=True, anchor="mm", rough=0.0, slant=slope)
    return (a, b)


def letter_sampler(pic):
    """The needlework over the door, in stitched capitals seven pixels high."""
    s = FL["sampler"]
    a, b = V.pt(s[2] + 3, s[5] - 3, 3.2), V.pt(s[3] - 3, s[5] - 3, 3.2)
    c = V.pt(s[2] + 3, s[4] + 3, 3.2)
    slope = (b[1] - a[1]) / (b[0] - a[0])
    drop = 1.0 / slope if abs(slope) > 1e-3 else None
    mid = (a[0] + b[0]) / 2
    top = (a[1] + b[1]) / 2
    high = c[1] - a[1]
    red, blue, green = (0.60, 0.10, 0.12), (0.14, 0.20, 0.44), (0.20, 0.40, 0.22)
    rows = [("AS FOR ME AND MY", STITCH, red), ("HOUSE, WE WILL", STITCH, red), ("SERVE THE LORD", STITCH, red), ("JOSHUA 24:15", SMALL, blue)]
    pitch = [1.0, 9.5, 18.0, 27.0]                           # seven-pixel capitals, a pixel and a half between the rows
    k = min(1.0, (high - 0.5) / 32.5)                        # squeeze the rows a little if the linen is shorter than planned
    for (words, face, color), dy in zip(rows, pitch):
        m = stitch_mask(words, face)
        x = int(round(mid - m.shape[1] / 2))
        y = int(round(top + dy * k + (x - mid) * slope))
        put_mask(pic, m, x, y, color, 0.96, drop)
    # a line of stitches along the foot, and a small house and a heart either side of the chapter and verse
    for i, t in enumerate(np.linspace(0, 1, int((b[0] - a[0]) / 2))):
        x = a[0] + 1.5 + (b[0] - a[0] - 3) * t
        if abs(x - mid) < 28:
            continue
        yy = c[1] + (x - a[0]) * slope - 1.6
        pic[int(round(yy)), int(round(x))] = lerp(pic[int(round(yy)), int(round(x))], col(green if i % 2 else red), 0.85)
    house = ["..#..", ".###.", "#####", ".#.#.", ".###."]
    heart = [".#.#.", "#####", "#####", ".###.", "..#.."]
    for art, dx, cc in ((house, -34, green), (heart, 30, red)):
        m = np.array([[1.0 if ch == "#" else 0.0 for ch in row] for row in art], dtype=F32)
        x = int(round(mid + dx))
        y = int(round(top + pitch[3] * k + (x - mid) * slope))
        put_mask(pic, m, x, y, cc, 0.9)
    return (a, b, c, high)


def details(pic):
    """Over the brushwork: the things that must be read."""
    letter_frame(pic)
    letter_sampler(pic)
    return pic


# ---------------------------------------------------------------- the room, laid in
def lay_in(ss):
    R = Room(cache=None, ss=ss)
    T = Things(R)
    R.occluders(T.shadow_boxes())
    R.bake()
    back = Layer(R.cam)
    R.backdrop(back)
    piano = Layer(R.cam); T.piano(piano); T.bench(piano)
    piano_open = Layer(R.cam); T.piano(piano_open, open_panel=True); T.bench(piano_open)
    chair = Layer(R.cam); T.armchair(chair); T.reading_lamp(chair); T.by_the_chair(chair)
    pencil = Layer(R.cam); pencil.z = chair.z.copy(); T.armchair(pencil, only_pencil=True)
    table = Layer(R.cam); T.table(table); T.chairs(table); T.pendant(table)
    return R, dict(back=back, piano=piano, piano_open=piano_open, armchair=chair, pencil=pencil, table=table)


def brushed(ref, seed, sizes=(12, 6, 3), keep=0.22, density=1.5, base=0.16, jitter=0.055):
    s = strokes(ref, sizes=sizes, seed=seed, density=density, jitter=jitter, keep=keep)
    m = crisp_mask(ref, base)
    return lerp(s, ref, m[..., None])


def cutout(backdrop, color, alpha, fast, seed):
    """A cut-out, brushed where it stands on the finished backdrop, its crisp drawing put back on top."""
    ys, xs = np.nonzero(alpha > 0.02)
    if len(ys) == 0:
        return color, alpha
    y0, y1, x0, x1 = max(0, ys.min() - 12), min(H, ys.max() + 13), max(0, xs.min() - 12), min(W, xs.max() + 13)
    stood = backdrop[y0:y1, x0:x1].copy()
    over(stood, color[y0:y1, x0:x1], alpha[y0:y1, x0:x1])
    stood = firm(stood)
    out = backdrop.copy()
    out[y0:y1, x0:x1] = stood if fast else brushed(stood, seed, sizes=(7, 4, 2), keep=0.30, density=1.7, base=0.24, jitter=0.045)
    return out, alpha


# ---------------------------------------------------------------- layout.json, measured from the picture
def box_of(mask):
    ys, xs = np.nonzero(mask)
    if len(ys) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


def px(X, Z):
    x, y = V.pt(X, 0, Z)
    return [int(round(x)), int(round(y))]


def inside(pt, poly):
    x, y = pt
    n, c = len(poly), False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def layout(layers, tags):
    mk = M.MARKS
    walk = [px(X, Z) for X, Z in M.WALK]
    pn, st = BX["piano"], BX["stool"]
    blocked_room = [[(pn[0] - 6, 42), (pn[1] + 6, 42), (pn[1] + 6, st[5] + 6), (pn[0] - 6, st[5] + 6)]]
    blocked = [[px(X, Z) for X, Z in poly] for poly in blocked_room]

    def rect(name, layer="back", grow=0):
        r = box_of(tags[layer] == TAG[name])
        if r and grow:
            r = [r[0] - grow, r[1] - grow, r[2] + 2 * grow, r[3] + 2 * grow]
        return r

    def thing(id, what, r, stand, face, **more):
        t = {"id": id, "what": what, "shape": {"rect": r}, "stand": px(*mk[stand]) if isinstance(stand, str) else px(*stand), "face": face}
        t.update(more)
        return t

    stairs_poly = [[int(round(p[0])), int(round(p[1]))] for p in
                   (V.pt(0, 0, 577), V.pt(108, 0, 577), V.pt(108, M.G, 177), V.pt(108, M.G + 100, 177), V.pt(0, M.G + 100, 200), V.pt(0, 110, 577))]
    stairs_poly = [[max(0, min(799, x)), max(0, min(599, y))] for x, y in stairs_poly]
    pr = rect("piano", "piano")
    sr = rect("stool", "piano")
    lr = rect("lamp", "piano")
    prr = [min(pr[0], sr[0]), min(pr[1], lr[1]), max(pr[0] + pr[2], sr[0] + sr[2]) - min(pr[0], sr[0]), max(pr[1] + pr[3], sr[1] + sr[3]) - min(pr[1], lr[1])]
    things = [
        thing("door", "the front door (the way out, when they are ready)", rect("door"), "atdoor", "N"),
        thing("sampler", "the needlework sampler over the front door: AS FOR ME AND MY HOUSE, WE WILL SERVE THE LORD. JOSHUA 24:15", rect("sampler"), (712, 104), "N"),
        thing("kitchen", "the way through to the kitchen (look only)", rect("kitchen"), "atkitchen", "N"),
        thing("books", "Mom's bookcase", rect("books"), "atbooks", "N"),
        thing("frame", "the framed print: We the People", rect("frame"), "atframe", "N"),
        thing("clock", "the wall clock, at twenty to ten", rect("clock", grow=2), (482, 108), "N"),
        thing("piano", "the upright piano: lamp, open hymnal, bench", prr, "atpiano", "N", stand2=px(*mk["atpiano2"]),
              panel=rect("panel", "piano"), note="two can stand side by side at `stand` and `stand2`"),
        thing("stairs", "the stairs up to the landing", {"poly": stairs_poly}, "atstairs", "W"),
        thing("closet", "the low cupboard door under the stairs, ajar", rect("closet", grow=2), "atcloset", "W"),
        thing("window", "the tall stair window: the night, the moon, the tree", rect("window"), (176, 548), "W"),
        thing("photos", "family photographs climbing the stair wall", rect("photos"), (170, 590), "W"),
        thing("rug", "the big worn rug", rect("rug"), "mom", "S"),
        thing("chandelier", "the brass chandelier (not lit)", rect("chandelier"), "mom", "N"),
        thing("coats", "coats on hooks by the front door", rect("coats"), (716, 116), "E"),
        thing("table", "the dinner table, set for five", rect("table", "table"), "attable", "E"),
        thing("bible", "the family Bible, open beside Dad's plate", rect("bible", "table", grow=2), "attable", "E"),
        thing("armchair", "Dad's armchair", rect("armchair", "armchair"), "atarmchair", "S"),
        thing("crossword", "the folded crossword on the arm of Dad's chair", rect("crossword", "armchair", grow=3), "atarmchair", "S"),
        thing("pencil", "the yellow pencil on the crossword (pencil.png: it can be taken)", rect("pencil", "pencil", grow=3), "atarmchair", "S"),
    ]
    for t in things:
        if isinstance(t["shape"]["rect"], dict):
            t["shape"] = t["shape"]["rect"]
    base = [px(pn[0] - 6, st[5] + 2), px(pn[1] + 6, st[5] + 2)]
    lay = {
        "id": ID, "horizon": M.VIEW["horizon"], "full": M.VIEW["full"], "view": M.VIEW,
        "light": "night: warm pendant over the table (front right), reading lamp by the armchair (front left), lamp on the piano, "
                 "the kitchen doorway's light across the rug, a lamp upstairs; cool moonlight from the tall stair window, down the upper "
                 "stairs and across the floor between the rug and the armchair (the window's shape, with the banister's shadow in it)",
        "vanishing": [[round(V.vanishing()[0][0]), 150], [round(V.vanishing()[1][0]), 150]],
        "walk": walk,
        "blocked": blocked,
        "planes": [
            {"id": "piano", "file": "piano.png", "base": base, "states": {"shut": "piano.png", "open": "piano-open.png"},
             "solid": blocked[0], "note": "piano-open.png is the whole piano again with the panel by the pedals off and leaning beside it"},
            {"id": "armchair", "file": "armchair.png", "plane": "front"},
            {"id": "pencil", "file": "pencil.png", "plane": "front", "note": "lies on the crossword; show it until it is taken (after armchair)"},
            {"id": "table", "file": "table.png", "plane": "front"},
        ],
        "things": things,
        "exits": [{"to": "home-landing", "id": "stairs", "shape": {"poly": stairs_poly}, "stand": px(*mk["atstairs"]), "face": "W"},
                  {"to": "(the gate: out to Act Four)", "id": "door", "shape": {"rect": rect("door")}, "stand": px(*mk["atdoor"]), "face": "N"}],
        "marks": {
            "default": {"mom": px(*mk["mom"]), "bigsis": px(*mk["bigsis"]), "lilsis": px(*mk["lilsis"]), "face": "S"},
            "fromLanding": {"lead": px(*mk["landing1"]), "others": [px(*mk["landing2"]), px(*mk["landing3"])], "face": "E"},
            "mom": px(*mk["mom"]), "bigsis": px(*mk["bigsis"]), "lilsis": px(*mk["lilsis"]),
        },
        "lamps": {k: [int(round(c)) for c in V.pt(*v)] for k, v in M.LIGHTS.items() if k != "kitchen"},
    }
    # every stand place must be on the floor people may walk, clear of the piano
    bad = []
    for t in things:
        for key in ("stand", "stand2"):
            if key in t and (not inside(t[key], walk) or any(inside(t[key], b) for b in blocked)):
                bad.append((t["id"], key, t[key]))
    for name, p in list(lay["marks"]["default"].items())[:3] + [("lead", lay["marks"]["fromLanding"]["lead"])] + [("other", q) for q in lay["marks"]["fromLanding"]["others"]]:
        if not inside(p, walk):
            bad.append((name, "mark", p))
    tall = max(160.0 * (y - M.VIEW["horizon"]) / (M.VIEW["full"] - M.VIEW["horizon"]) for _, y in walk)
    return lay, bad, tall


if __name__ == "__main__":
    t0 = time.time()
    fast = "fast" in sys.argv or "draft" in sys.argv
    ss = 1 if "draft" in sys.argv else 2
    os.makedirs(OUT, exist_ok=True)
    R, layers = lay_in(ss)
    print("laid in", {k: v.count for k, v in layers.items()}, round(time.time() - t0, 1))
    tags = {k: v.tags() for k, v in layers.items()}

    # ---- the backdrop: block-in, brush, the crisp drawing restated, the lettering
    bc, _ = layers["back"].done()
    zb = layers["back"].depth()
    z_all = zb.copy()
    for name in ("piano", "armchair", "table"):
        z_all = np.minimum(z_all, layers[name].depth())
    block = tone(bc)
    tint(block, (0.46, 0.38, 0.48), behind(zb, z_all) * 0.42)
    far = np.clip((zb - 760.0) / 520.0, 0, 1)                # the far end of the room: a little cooler, paler, closer in value
    over(block, (0.34, 0.40, 0.50), (far * 0.085).astype(F32))
    under = firm(atmosphere(wob(block)))
    show(under, f"out/{ID}-1-under.png")
    pic = under.copy() if fast else brushed(under, 2)
    details(pic)
    print("backdrop", round(time.time() - t0, 1))

    # ---- the cut-outs
    cuts = {}
    for i, name in enumerate(("piano", "piano_open", "armchair", "pencil", "table")):
        c, a = layers[name].done()
        c = tone(c)
        zc = layers[name].depth()
        tint(c, (0.46, 0.38, 0.48), behind(zc, zc) * 0.42)
        c, a = wob(c), wob(a)
        if name == "pencil":
            cuts[name] = (c, a)                              # too small to brush: it stays crisp
        else:
            cuts[name] = cutout(pic, c, a, fast, 20 + i)
    whole = pic.copy()
    for name in ("piano", "armchair", "pencil", "table"):
        c, a = cuts[name]
        over(whole, c, (a > 0.5).astype(F32))
    show(whole, f"out/{ID}-2-all.png")
    alt = pic.copy()
    for name in ("piano_open", "armchair", "table"):
        c, a = cuts[name]
        over(alt, c, (a > 0.5).astype(F32))
    show(alt, f"out/{ID}-2-open.png")
    print("painted", round(time.time() - t0, 1))

    lay, bad, tall = layout(layers, tags)
    if "draft" not in sys.argv:                              # (a draft measures the shapes a pixel coarser: it does not replace the file)
        json.dump(lay, open(f"{OUT}/layout.json", "w"), indent=1)
    print("layout: tallest grown-up on the walk", round(tall), "px;", "PROBLEMS " + str(bad) if bad else "all stand places are on the walk")
    if fast:
        sys.exit()

    # ---- the last pass: grain, a limited palette, PNG-8
    print("back", finish(pic, f"{OUT}/back.png", 156, amount=0.014, speckle=0.011))
    pc, pa = cuts["piano"]
    oc, oa = cuts["piano_open"]
    both = np.concatenate([pc[pa > 0.5], oc[oa > 0.5]]).reshape(-1, 1, 3)
    pal = palette_of([both], colors=88)                      # one palette for both states, so the piano does not change color
    soft = dict(amount=0.014, speckle=0.011)
    print("piano", finish(pc, f"{OUT}/piano.png", 88, pa, pal=pal, **soft), finish(oc, f"{OUT}/piano-open.png", 88, oa, pal=pal, **soft))
    print("armchair", finish(cuts["armchair"][0], f"{OUT}/armchair.png", 80, cuts["armchair"][1], **soft))
    print("pencil", finish(cuts["pencil"][0], f"{OUT}/pencil.png", 12, cuts["pencil"][1], amount=0.0, speckle=0.0))
    print("table", finish(cuts["table"][0], f"{OUT}/table.png", 96, cuts["table"][1], **soft))
    subprocess.run([sys.executable, "comp.py", OUT, "back", "piano", "armchair", "pencil", "table"], check=True)
    print("done", round(time.time() - t0, 1))

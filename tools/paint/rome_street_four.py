"""Round four in the street: what the game needs to draw moving the things that are not painted still any more.
rome_street.py calls everything() at the end of a run with PAINT_MOVING False; it writes, into out/rome-street/:

  laundry-lines.png, laundry-1.png .. laundry-12.png
            the washing, in pieces, each its own cut-out (laundry.png itself stays as it was, byte for byte): the
            lines (and the three sparrows sitting on the far one) and each piece of washing, so that each piece can
            stir on its own from the line it hangs on. Laid together, back to front and the lines last, they are
            laundry.png again, pixel for pixel. Where a piece is hidden by a nearer one it is filled out a few
            pixels from its own edge, so that nothing opens up when the nearer one stirs.
  cat-1.png .. cat-5.png
            the cat on her sill with her tail in five places (1 as painted), cut from the finished back.png (her body,
            pixel for pixel) with each tail painted the way the picture painted the first.
  pigeon-*.png, sparrow-*.png, swallow-*.png
            the birds of the street, painted by rome_steps_birds.py in this picture's palette and light, at their size.

and returns layout.json's new "fx", "frames" and "fx_note". It also writes out/rome-street-moved.png: every pixel
of back.png and fountain.png that the things taken out had touched (rome_street_check4.py proves nothing else
changed)."""

import math
import os

import numpy as np
from PIL import Image
from scipy import ndimage

from brush import F32, grain, lerp, over, save, to_palette
import rome_steps_birds as birds

OUT = "out/rome-street"
r = lambda q: [int(round(float(q[0]))), int(round(float(q[1])))]
r1 = lambda q: [round(float(q[0]), 1), round(float(q[1]), 1)]

CAT_BENDS = [None,                                                                    # 1: as painted
             [(0.26, -0.06), (0.43, 0.12), (0.42, 0.35), (0.52, 0.47)],               # 2, 3: the tip swings out to the right,
             [(0.26, -0.06), (0.44, 0.12), (0.48, 0.33), (0.59, 0.40)],               #       and curls up
             [(0.26, -0.06), (0.41, 0.12), (0.31, 0.36), (0.36, 0.52)],               # 4, 5: and back in under her
             [(0.26, -0.06), (0.40, 0.13), (0.28, 0.34), (0.26, 0.46)]]
CAT_ORDER = [1, 2, 3, 2, 1, 4, 5, 4]
LAUNDRY_WHAT = {"sheet": "a sheet", "tunic": "a tunic", "toga": "a toga", "strip": "a strip of cloth"}


def finished(R, picture, pal):
    """The backdrop's own finish (rome_street.finish) for a picture the size of the stage -> palette indexes."""
    return to_palette(grain(picture, 7, 0.02), pal, speckle=0.014)


def cat_frames(R, ungraded, back_idx, pal):
    k1 = R.kz(85.0)
    cx, cy = R.P(R.WR - 7, 455.0, 96.0)
    h = 36 * k1
    body = R.Sheet2(R.SHAPE)
    R.cat(body, cx, cy, h, tail=False)
    ba = body.done()[1]
    x0, y0, x1, y1 = int(cx - 0.45 * h) - 2, int(cy - 1.15 * h) - 2, int(cx + 0.75 * h) + 3, int(cy + 0.65 * h) + 3
    clear = len(pal)
    files, first = [], None
    for n, bend in enumerate(CAT_BENDS, 1):
        t = R.Sheet2(R.SHAPE)
        R.cat_tail(t, cx, cy, h, bend=bend)
        tc, ta = t.done()
        p = ungraded.copy()
        over(p, tc, ta)
        idx = finished(R, R.grade(p), pal)
        frame = np.full(R.SHAPE, clear, np.uint8)
        frame[ta > 0.25] = idx[ta > 0.25]                                               # (its soft edge too, as painted)
        frame[ba > 0.5] = back_idx[ba > 0.5]
        if n == 1:
            first = frame
        crop = frame[y0:y1, x0:x1]
        save(f"{OUT}/cat-{n}.png", crop, pal, (crop != clear).astype(F32))
        files.append(f"cat-{n}.png")
    at = [int(round(cx)), int(round(cy))]
    return files, {"at": at, "foot": [at[0] - x0, at[1] - y0], "size": [x1 - x0, y1 - y0]}, first


def laundry_pieces(R):
    """laundry.png cut into the lines and each piece of washing (see the top of this file). -> marks for each"""
    im = Image.open(f"{OUT}/laundry.png")
    idx = np.asarray(im)
    clear = im.info["transparency"]
    pal = np.array(im.getpalette()[:3 * clear], dtype=F32).reshape(-1, 3) / 255.0
    opaque = idx != clear
    masks = [R.cloth(item, 5 + 11 * i)[1] for i, item in enumerate(R.WASH)]                 # (the seeds laundry_plane gives them)
    lines = R.laundry_plane(5, items=[])[3] > 0.5
    owner = np.full(R.SHAPE, -1, np.int16)
    for i, m in enumerate(masks):
        owner[m > 0.5] = i
    owner[lines] = -2
    loose = opaque & (owner == -1)                                                           # (none, if the masks are right)
    if loose.any():
        _, (iy, ix) = ndimage.distance_transform_edt(owner == -1, return_indices=True)
        owner[loose] = owner[iy[loose], ix[loose]]
    marks, files = [], []
    out = np.full(R.SHAPE, clear, np.uint8)
    out[opaque & (owner == -2)] = idx[opaque & (owner == -2)]
    save(f"{OUT}/laundry-lines.png", out, pal, (out != clear).astype(F32))
    for i, item in enumerate(R.WASH):
        own = opaque & (owner == i)
        piece = np.full(R.SHAPE, clear, np.uint8)
        piece[own] = idx[own]
        dist, (iy, ix) = ndimage.distance_transform_edt(~own, return_indices=True)
        fill = (masks[i] > 0.5) & ~own & (dist <= 3.0)
        piece[fill] = idx[iy[fill], ix[fill]]
        name = f"laundry-{i + 1}.png"
        save(f"{OUT}/{name}", piece, pal, (piece != clear).astype(F32))
        files.append(name)
        line, t0, t1, length, kind, tone = item
        anchor = [r1(R.P(*R.rope_at(line, t))) for t in np.linspace(t0, t1, 5)]
        ys = np.nonzero(own.any(axis=1))[0]
        marks.append({"id": f"laundry-{i + 1}", "type": "sway", "plane": f"laundry-{i + 1}", "anchor": "top",
                      "amount": 1.5 if length >= 120 else 1.0, "period": round(3.1 + (i % 4) * 0.37, 2), "lean": 0.3,
                      "what": f"{LAUNDRY_WHAT[kind]} ({tone}) on the {line} line ({name})", "rope": anchor,
                      "hangs": int(ys.max() - min(a[1] for a in anchor)) if len(ys) else 0})
    # proof: laid together they are laundry.png
    back_to_front = np.full(R.SHAPE, clear, np.uint8)
    for name in files + ["laundry-lines.png"]:
        a = np.asarray(Image.open(f"{OUT}/{name}"))
        back_to_front = np.where(a != clear, a, back_to_front)
    same = bool((back_to_front == idx).all())
    tunic = {"id": "tunic-sway", "type": "sway", "plane": "tunic", "anchor": "top", "amount": 1.0, "period": 2.9, "lean": 0.3,
             "what": "the small tunic on the low line (the existing cut-out tunic.png, already in the scene)",
             "rope": [r1(R.P(*R.rope_at("low", t))) for t in np.linspace(R.TUNIC[1], R.TUNIC[2], 5)]}
    return marks + [tunic], files, same, int(loose.sum())


def contour(mask, step=6):
    """A rough outline of a mask's biggest blob, as a polygon (for shimmer)."""
    lab, n = ndimage.label(mask)
    if n == 0:
        return None
    big = lab == (1 + int(np.argmax(ndimage.sum(mask, lab, range(1, n + 1)))))
    ys, xs = np.nonzero(big)
    cx, cy = xs.mean(), ys.mean()
    pts = []
    for a in np.linspace(0, 2 * math.pi, 24, endpoint=False):
        d = np.hypot(xs - cx, ys - cy)
        ang = np.arctan2(ys - cy, xs - cx)
        near = np.abs((ang - a + math.pi) % (2 * math.pi) - math.pi) < math.pi / 24
        if near.any():
            j = np.argmax(np.where(near, d, -1))
            pts.append([int(xs[j]), int(ys[j])])
    return pts


def everything(R, pic, pic_was, ungraded, cut, fountain_was, info):
    pal = R.PALETTES[f"{OUT}/back.png"]
    back_idx = np.asarray(Image.open(f"{OUT}/back.png"))
    # what changed, before the finish: every pixel the things taken out had touched
    fnew = cut["fountain"][0]                                                           # (graded already, as fountain_was is)
    moved = (np.abs(pic - pic_was).max(axis=2) > 0) | ((np.abs(fnew - fountain_was[0]).max(axis=2) > 0) & (np.maximum(cut["fountain"][1], fountain_was[1]) > 0.02))
    Image.fromarray(moved.astype(np.uint8) * 255).save("out/rome-street-moved.png")

    cat_files, cat_place, cat1 = cat_frames(R, ungraded, back_idx, pal)
    sway, laundry_files, laundry_same, loose = laundry_pieces(R)

    # the birds, in this picture's palette and light (the sun is high on the right: the same light as the painter's)
    lit = lambda tone, sun=1.0, kind="front": tuple(np.clip(R.lit(tone, sun, kind) * f, 0, 1) for f in (1.0, 1.28, 0.60))
    sets = {}
    for name, tone, sun, kind in (("pigeon", "#8d96ac", 1.0, "front"), ("pigeon-pale", "#e8e4dc", 1.0, "front"), ("pigeon-shade", "#8d96ac", 0.0, "warm")):
        body, wing, dark = lit(tone, sun, kind)
        tones = (body, wing, dark, R.lit("#7a9a8a", sun, kind))
        if sun == 0.0:                                                                     # in the shade its feet, beak and eye are dim too
            tones += (R.lit("#c8605a", sun, kind), R.lit("#d8c8a8", sun, kind), R.lit("#e88838", sun, kind))
        sets[name] = birds.pigeon_frames(OUT, name, pal, 18.8, tones, birds.box_for(birds.PIGEON_BOX, 18.8 / birds.S))
    sh = lambda c, d=1.2: np.clip(R.in_shade(c, "front") * d, 0, 1)
    sets["sparrow"] = birds.pigeon_frames(OUT, "sparrow", pal, 8.0, (sh("#8a6a4a"), sh("#a8845c"), sh("#4a3424"), sh("#d8c0a0"), sh("#8a6a5a"), sh("#5a4a40"), sh("#2a1c18")),
                                          birds.box_for(birds.PIGEON_BOX, 8.0 / birds.S))
    sets["swallow"] = birds.swallow_frames(OUT, "swallow", pal, 3.2, "#1c2a4a", birds.box_for(birds.SWALLOW_BOX, 3.2 / 5.0))

    P, f = R.P, R.FOUNT
    x0, x1, z0, z1 = f["x0"], f["x1"], f["z0"], f["z1"]
    y1 = R.SWH + f["h"]
    w = f["wall"]
    yw = y1 - 4.0
    fbase = int(round(R.row_of(R.SWH, z0)))
    pz0 = z1 - 20.0
    mx, my, mz = (289.0 + 353.0) / 2, R.SWH + 128.0 - 11.0, pz0 - 2
    fall = [r1(P(mx, my - (my - yw) * t * t, mz - 44 * t)) for t in np.linspace(0, 1, 9)]
    land = P(mx, yw, mz - 44)
    water = [r1(P(*q)) for q in ((x0 + w, yw, z0 + w), (x1 - w, yw, z0 + w), (x1 - w, yw, z1 - w), (x0 + w, yw, z1 - w))]
    spill = [r1(P(x0 - 2 - t * 76 + math.sin(t * 9) * 3, R.SWH + 0.3, 298 + t * 14 + math.sin(t * 5) * 5)) for t in np.linspace(0, 1, 12)]
    spill += [r1(P(R.KR, R.SWH - 2, 312)), r1(P(R.KR, 2, 314))] + [r1(P(R.KR - 11, 0.3, zz)) for zz in (330.0, 500.0, 750.0, 1000.0, 1300.0)]
    pud = info["pud"] > 0.5 if "pud" in info else None
    puddle = contour(pud) if pud is not None and pud.any() else None
    kk = R.kz(R.L1["zr"])
    ridge = [r1(P(-700.0, R.L1["ridge"] + 3, R.L1["zr"])), r1(P(R.WL + 40, R.L1["ridge"] + 3, R.L1["zr"]))]
    balc = [r1(P(R.BALC["x"] - 22, R.BALC["top"] + 14, z)) for z in (200.0, 620.0)]
    lx, ly = P(-279.0, 194.0, R.ZF - 1.5)
    sy = R.BAR["top"]
    holes = [r1(P(xx + 2.25, sy + 10, 349.5)) for xx in (-346.0, -338.0, -330.0)]
    px0, py0 = P(-336, sy + 22, 371)
    kp = R.kz(371)
    awbase = int(round(R.row_of(R.SWH, R.ZF)))
    flock = lambda name, box: birds.flock_frames(name, box)
    pbox, sbox = birds.box_for(birds.PIGEON_BOX, 18.8 / birds.S), birds.box_for(birds.PIGEON_BOX, 8.0 / birds.S)
    fx = [
        {"id": "fountain-stream", "type": "stream", "what": "the water falling from the carved face's mouth into the basin (taken out of fountain.png)",
         "path": fall, "width": 1.6, "color": "#b4cdf2", "light": "#ffffff", "opacity": 0.8, "speed": 60, "splash": 4, "base": fbase + 1,
         "note": "As painted: a thin bright fall 1.5 px wide (#e6f0ff) with a darker edge on its right (#9fb8e4), curving out from the mouth "
                 "(606, 396) and down to the water at (613, 428). It falls inside the basin: base one row in front of the fountain's (501)."},
        {"id": "fountain-rings", "type": "ripples", "what": "the rings where the water lands in the basin",
         "at": r1(land), "radius": [3, 22], "flat": 0.26, "every": 0.6, "rings": 1, "speed": 16, "color": "#dfeaff", "opacity": 0.6,
         "clip": water, "base": fbase + 1,
         "note": "Steady: the painting had three rings at once, 8, 14 and 22 px across, fading outward, and a white splash at the middle."},
        {"id": "fountain-water", "type": "shimmer", "what": "the basin's brim-full water",
         "poly": water, "flow": [0, 0], "count": 8, "size": 5, "color": "#eef4ff", "opacity": 0.35, "base": fbase + 1,
         "note": "Very quiet. The water itself, its dark and the sky in it, are painted in fountain.png and stay."},
        {"id": "sparrow", "type": "birds", "kind": "flock", "what": "a sparrow come to drink at the fountain (taken out of fountain.png)",
         "perch": [r1(P(x0 + 40, y1, z0 + 7)), r1(P(x1 - 20, y1, z0 + 7))], "count": 1, "frames": flock("sparrow", sbox), "base": fbase + 2,
         "back": [10, 25], "painted": r1(P(x1 - 40, y1, z0 + 7)),
         "note": "On the basin's near rim, between the bronze jug and the corner: it sips (peck), hops along the rim (walk), looks about, and "
                 "flies off when the boy comes near. It stands ON the fountain, so `base` puts it in front of the fountain's cut-out (501): "
                 "sorted by its feet (row 440) it would be hidden behind the basin."},
        {"id": "spill", "type": "stream", "what": "the water that spills from the basin, across the sidewalk, down the kerb and away along the gutter",
         "path": spill, "width": 1.2, "color": "#8aa4d8", "light": "#d4e4ff", "opacity": 0.45, "speed": 28, "splash": 0, "plane": "back",
         "note": "On the ground, under everyone. Its wet dark is painted and stays; the glints that were painted on it are taken out, "
                 "and this runs light along it instead (the painting's glints faded to a quarter far up the gutter)."},
        {"id": "pigeons-roof", "type": "birds", "kind": "flock", "what": "pigeons on the ridge of the corner house's roof, in the sun",
         "perch": ridge, "count": 3, "frames": flock("pigeon", pbox), "scale": round(34 * kk / 20.4, 2), "plane": "back", "shy": 0,
         "moves": {"stand": 4, "look": 2, "peck": 0.5, "walk": 1.5, "turn": 1},
         "painted": [r1(P(xx, R.L1["ridge"] + 3, R.L1["zr"])) for xx, fc, tone in R.RIDGE_PIGEONS[:3]]},
        {"id": "pigeon-roof-pale", "type": "birds", "kind": "flock", "what": "and a pale one with them", "perch": ridge, "count": 1,
         "frames": flock("pigeon-pale", pbox), "scale": round(34 * kk / 20.4, 2), "plane": "back", "shy": 0, "seed": 2,
         "moves": {"stand": 4, "look": 2, "peck": 0.5, "walk": 1.5, "turn": 1},
         "painted": [r1(P(xx, R.L1["ridge"] + 3, R.L1["zr"])) for xx, fc, tone in R.RIDGE_PIGEONS[3:]]},
        {"id": "pigeon-balcony", "type": "birds", "kind": "flock", "what": "a pigeon on the little roof over the balcony, in the shade",
         "perch": balc, "count": 1, "frames": flock("pigeon-shade", pbox), "plane": "back", "shy": 0,
         "moves": {"stand": 4, "look": 2, "peck": 0, "walk": 1, "turn": 1},
         "painted": r1(P(R.BALC["x"] - 22, R.BALC["top"] + 14, 300.0))},
        {"id": "swallows", "type": "birds", "kind": "flyers", "what": "swallows over the street, high up",
         "lanes": [[[-12, 14], [140, 8], [300, 18], [380, 30], [420, -12]],
                   [[300, -12], [345, 55], [410, 90], [445, 50], [440, -12]],
                   [[455, -12], [400, 50], [330, 82], [298, 40], [280, -12]]],
         "frames": birds.flyer_frames("swallow", birds.box_for(birds.SWALLOW_BOX, 3.2 / 5.0)), "scale": 1, "every": [5, 13], "group": [1, 3],
         "speed": 110, "plane": "back", "painted": [[x, y] for x, y, s in R.SWALLOWS],
         "note": "Only in the sky: above the corner house's roof (y < 25) and down the gap between the houses (x 295 to 465). They pass behind "
                 "the washing (it is in front of everything)."},
        {"id": "shrine-flame", "type": "flame", "what": "the little lamp burning in the crossroads shrine's niche (taken out of back.png)",
         "at": r1((lx + 5.0, ly - 2.2)), "size": 4.8, "width": 2.6, "color": "#fff4b0", "edge": "#ffb040", "glow": 6, "glowOpacity": 0.25,
         "flicker": 0.25, "base": awbase, "note": "Tiny: a white-yellow heart in an orange tongue. Its foot is on the lamp's nozzle."},
        {"id": "stove-embers", "type": "embers", "what": "the snack bar's charcoal stove: the fire through the three holes in its front",
         "at": holes[1], "size": [9, 1.5], "count": 4, "sparks": 0, "glow": 10, "base": awbase + 1, "holes": holes,
         "note": "Painted in awning.png (unchanged), as the coals under the pot are."},
        {"id": "stove-steam", "type": "smoke", "what": "steam from the bronze pot on the stove (the breakfast is hot): none was painted",
         "at": r1((px0, py0 - 17 * kp)), "height": 50, "width": [3, 12], "lean": [5, -50], "rise": 12, "rate": 2, "gust": 0.3,
         "color": "#f4f0f0", "opacity": 0.25, "base": awbase + 1, "note": "Faint wisps from the pot's mouth; the counter is in the shade, so pale on dark."},
    ]
    if puddle:
        fx.append({"id": "puddle", "type": "shimmer", "what": "the water standing where the basin spills into the gutter", "poly": puddle,
                   "flow": [0, 0], "count": 5, "size": 4})
    wet = np.maximum(np.asarray(info["wet"]), np.asarray(info["wet_s"])) > 0.4 if "wet" in info else None
    if wet is not None and wet.any():                                                    # the wet paving: the gutter and the sidewalk by the basin
        rows = np.nonzero(wet.any(axis=1))[0]
        left, right = [], []
        for y in list(range(int(rows.min()) + 2, int(rows.max()), 16)) + [int(rows.max()) - 2]:
            xs = np.nonzero(wet[y])[0]
            if len(xs) > 2:
                left.append([int(xs.min()) - 1, y])
                right.append([int(xs.max()) + 1, y])
        fx.append({"id": "wet-paving", "type": "shimmer", "what": "the wet stones of the gutter and of the sidewalk before the fountain: standing water",
                   "poly": left + right[::-1], "flow": [0, 0], "count": 10, "size": 4, "life": 2.2, "color": "#c8d8ff", "opacity": 0.3,
                   "note": "Quiet glints that come and go on the wet paving; the painted glints and the wet dark stay. On the ground (under everyone)."})
    fx += sway
    frames = {
        "pigeon": {"files": "<set>-<n>.png, n 1 to 18", "sets": ["pigeon", "pigeon-pale", "pigeon-shade"],
                   "size": list(birds.box_for(birds.PIGEON_BOX, 18.8 / birds.S)[:2]), "foot": list(birds.box_for(birds.PIGEON_BOX, 18.8 / birds.S)[2:]),
                   "acts": birds.PIGEON_ACTS, "faces": "right",
                   "note": "The same frames as rome-steps (see its layout.json), painted at the size of the pigeon on the balcony (scale 1) in this "
                           "picture's palette; pigeon-shade for the one in the shade."},
        "sparrow": {"files": "sparrow-<n>.png, n 1 to 18", "size": list(birds.box_for(birds.PIGEON_BOX, 8.0 / birds.S)[:2]),
                    "foot": list(birds.box_for(birds.PIGEON_BOX, 8.0 / birds.S)[2:]), "acts": birds.PIGEON_ACTS, "faces": "right",
                    "note": "A house sparrow, brown, in the fountain's shade; drawn the way the pigeons are (peck = a sip, walk = little hops)."},
        "swallow": {"files": "swallow-<n>.png, n 1 to 4", "size": list(birds.box_for(birds.SWALLOW_BOX, 3.2 / 5.0)[:2]),
                    "foot": list(birds.box_for(birds.SWALLOW_BOX, 3.2 / 5.0)[2:]), "acts": birds.SWALLOW_ACTS, "note": "Symmetric, never mirrored."},
        "cat": {"files": "cat-<n>.png, n 1 to 5", "size": cat_place["size"], "foot": cat_place["foot"], "at": cat_place["at"]},
        "laundry": {"files": ["laundry-lines.png"] + laundry_files,
                    "note": "800x600 cut-outs, plane front. To let the washing stir, the scene shows these instead of laundry.png, in this order: "
                            "laundry-1 .. laundry-12 (back to front), then laundry-lines last (the lines are over everything, as painted). "
                            "Laid together they are laundry.png pixel for pixel" + ("" if laundry_same else " (NOT: see the painter)") + "."},
    }
    note = ("Round four. `fx` is in the engine's own fields (briefs/out/fx-4-ready.md), ready to copy into the scene; `cutouts` are the new "
            "cut-outs (the cat with her tail, and the washing in pieces, which replace the plane `laundry`: the laundry-N sways need them). "
            "Taken out of the painting: the water falling from the fountain's mouth and its rings, and the sparrow drinking "
            "(fountain.png); the four pigeons on the corner house's ridge and the one over the balcony, the four swallows, the cat's "
            "tail, the shrine lamp's flame, and the glints on the water spilling from the basin and running down the gutter (back.png). "
            "Every other pixel of back.png and fountain.png is as it was, and awning.png, front.png, laundry.png and tunic.png are byte for "
            "byte the same. New: the washing in pieces (laundry-*.png) so that it can stir, the cat's frames, the birds' frames. Left as "
            "they are, on purpose: the three sparrows sitting on the far washing line (they sit, like the birds on the highway's wire), "
            "the songbird in its wicker cage (5 px), the strings of garlic, sausages and loaves under the awning, the hanging sign, the pot "
            "plants, the far dabs of people in the square, the clouds.")
    was = "out/rome-street-4-before/back.png"
    print("round four:", {"cat": len(cat_files), "laundry": len(laundry_files), "laundry the same laid together": laundry_same,
                          "loose laundry pixels": loose, "moved px": int(moved.sum()),
                          "cat-1 over the new back differs from the old back in": int(((np.where(cat1 != len(pal), cat1, back_idx)) != np.asarray(Image.open(was))).sum()) if os.path.exists(was) else "?"},
          {k: len(v) for k, v in sets.items()})
    cutouts = [{"id": "cat", "frames": [f"cat-{n}.png" for n in CAT_ORDER], "fps": 2.5, "at": cat_place["at"], "foot": cat_place["foot"], "base": 180,
                "what": "the cat on her sill, her tail swinging slowly: a cut-out with frames (as the steam at the car in Egypt). Her body is "
                        "cut from back.png itself; only the tail moves. The tail is no longer painted in back.png, so until this goes in she "
                        "has none."}]
    cutouts += [{"id": name[:-4], "file": name, "plane": "front"} for name in laundry_files] + [
        {"id": "laundry-lines", "file": "laundry-lines.png", "plane": "front",
         "what": "the washing lines and the three sparrows sitting on the far one: last, over every piece"}]
    return {"fx": fx, "cutouts": cutouts, "frames": frames, "fx_note": note}

"""Egypt, about 2560 B.C.: where the wagon came down. The Nile on the left, the desert on the right,
and on the plateau beyond, the Great Pyramid, nearly finished. Afternoon; the sun is low on the left.

The picture is made of a backdrop and two cut-out planes that people can walk behind:
the palms on the bank, and a clump of papyrus right at the front."""

import os, sys, time
import numpy as np
from PIL import Image
from brush import *
import sky, land, flora, build, wagon

W, H = 800, 600
HZ = 262                                                    # the horizon
LIGHT = (-0.78, -0.62)
BANK = [(346, 263), (322, 276), (296, 300), (262, 336), (214, 384), (150, 440), (84, 492), (20, 530), (-10, 546)]   # where sand meets river
PALMS = [(190, 400, 300, 0.07, 1), (252, 352, 215, -0.05, 2), (300, 318, 150, 0.05, 3)]                              # foot x, foot y, height, lean, seed
GREAT = ((566, 76), (430, 250), (604, 262), (704, 250))    # the Great Pyramid: apex, left, near corner, right
BUILT = 0.90
QUEENS = [(730, 252, 24, 44), (762, 251, 21, 38), (789, 250, 18, 32)]                                                # middle x, base y, half width, height
TRACK = [(380, 670), (420, 580), (462, 490), (490, 410), (486, 340), (492, 300), (520, 270)]
WAGON = (722, 540)                                          # where its rear wheel meets the ground
SUN_UP = 0.8                                                # a shadow is this many times as long as the thing is tall
REEDS = [(300, 302, 18, 16, 16), (272, 330, 22, 22, 18), (238, 366, 26, 30, 20)]                                     # reeds standing in the shallows
REEDS_APPROVED = REEDS + [(170, 428, 34, 44, 22)]           # as first approved: round three took out the clump below the near palm, where the donkey drinks
# Lot (the game draws him) sits on the sand in the near palm's shade: with the sun low on the left its crown's shadow
# lies some way to the right of its foot, and its darkest part is here, a few steps from his donkey at the water.
LOT = (404, 432)                                            # the ground under his hips
LOT_TALK = (448, 444)                                       # where Dad stands to talk with him, facing west (clear of the car's steam)
BUNDLE = (380, 427)                                         # his bundle on the sand at his left hand, behind him
VILLAGE_SMOKE = [(392, 286), (446, 288)]                    # the builders' village's two cooking fires (round four: the game draws the smoke)


def small(q):
    cx, by, hw, hgt = q
    return (cx, by - hgt), (cx - hw, by - 1), (cx + hw * 0.3, by + 2), (cx + hw, by - 1)


def pyramids(pic, seed):
    build.pyramid(pic, *GREAT, seed + 20, built=BUILT, lit=("#fff0c4", "#f4cc86"), shade=("#9c9cc6", "#ac9cb0"), haze="#f6e2bc", haze_amount=0.30)
    for i, q in enumerate(QUEENS):
        build.pyramid(pic, *small(q), seed + 23 + i, courses=16, lit=("#fdeec6", "#f2d298"), shade=("#a8a6c8", "#b4a6b6"), haze="#f6e2bc", haze_amount=0.42)


def under(seed=11):
    """Everything broad and soft: sky, water, sand, the big shapes and their light. No small things."""
    shape = (H, W)
    x, y = grid(shape)
    rng = np.random.default_rng(seed + 9)
    info = {}

    # ---- sky: deep blue overhead, pale and warm at the ground, one big heap of cloud coming over the river
    pic = sky.field(shape, HZ, [(0.0, "#2a72c6"), (0.38, "#4a9ae0"), (0.68, "#86c6ec"), (0.86, "#cfe6e0"), (1.0, "#f8e6be")], seed, haze="#fbeacc", patch=0.03)
    sky.wisps(pic, HZ, seed + 3, "#fdf0d8", top=0.55, amount=0.55)
    sky.paint_clouds(pic, [(250, 200, 390, 132, 36), (64, 240, 200, 34, 9), (742, 196, 150, 44, 10), (486, 238, 150, 22, 6)], seed + 5,
                     tones=("#86a6da", "#bcd0ea", "#fbf2de", "#fffcf0"), light=LIGHT, ragged=13)
    above = pic.copy()                                       # kept, to mirror in the river

    # ---- the hills across the river, where the white stone is quarried, and the green bank below them
    hills, hl = land.ridge(shape, [(0, 244), (70, 238), (150, 245), (230, 250), (300, 256), (350, 261)], HZ + 2, seed + 6, rough=2.0)
    hills *= (x < 356)
    over(pic, ramp(np.clip((y - hl[None, :]) / 20, 0, 1), [(0.0, "#e2c6b8"), (1.0, "#e9d8c8")]), hills)
    tint(pic, "#a79cc0", (hills * step(0.55, 0.8, noise(shape, (16, 30), seed + 61, 3)) * 0.5).astype(F32))
    far, _ = land.ridge(shape, [(0, 255), (120, 256), (260, 259), (350, 262)], HZ + 3, seed + 7, rough=1.6)
    far *= (x < 356)
    over(pic, vary("#7d9c68", shape, seed + 8, 0.14, 26), far)
    land.haze(pic, HZ - 4, "#e8ead6", 0.38, 0.05, np.maximum(far, hills))

    # ---- the Great Pyramid on its plateau, and the three small ones beside it
    pyramids(pic, seed)
    plateau, line = land.ridge(shape, [(330, 264), (372, 258), (420, 252), (470, 249), (540, 247), (620, 249), (700, 246), (800, 243)], 312, seed + 12, rough=2.0)
    up = np.clip((line[None, :] + 40 - y) / 40, 0, 1)                                    # 1 at the skyline, 0 at the cliff's foot
    cliff = ramp(up, [(0.0, "#e2b67a"), (0.35, "#d09c74"), (0.75, "#eac890"), (1.0, "#fbe6b6")])
    beds = noise(shape, (130, 5), seed + 13, 4) - 0.5                                     # level beds of limestone
    gully = noise(shape, (11, 44), seed + 14, 3)                                          # and the gullies that cut down through them
    cliff *= (1 + beds[..., None] * 0.16)
    over(pic, cliff, plateau)
    tint(pic, "#9d8aa6", (plateau * step(0.54, 0.78, gully) * np.clip(up * 2.6, 0, 1) * np.clip(2.3 - up * 2.4, 0, 1) * 0.66).astype(F32))
    land.haze(pic, 262, "#f6e6c6", 0.16, 0.09, plateau)

    # ---- the river, with the sky and the far bank lying in it
    river = mask_poly(shape, [(0, HZ), (350, HZ)] + BANK[1:] + [(0, 546)], wobble=1.5, seed=seed + 30)
    wat = land.water(shape, HZ, seed + 31, far="#cfe6e0", mid="#5caac6", near="#1f6690", streak=0.10, glint=0.55, sun_x=60)
    mirror = sample(above, x + (noise(shape, (40, 4), seed + 32, 3) - 0.5) * 14, HZ - (y - HZ) * 0.82)
    mirror = blur(mirror, 1.5)
    deep = np.clip((y - HZ) / 200, 0, 1)
    wat = lerp(wat, mirror, (0.46 * (1 - deep * 0.7))[..., None])
    green = np.clip(1 - np.abs(y - (HZ + 8)) / 9, 0, 1) * (x < 344)                        # the far bank's reflection
    over(wat, "#5a8f78", (green * 0.5).astype(F32))
    over(pic, wat, river)

    # ---- the sand, far to near, everywhere that is not river, and up to the foot of the cliff
    foot = np.clip((y - (line[None, :] + 34)) / 12.0, 0, 1)                               # the sand runs up the talus
    walk = (np.clip(y - HZ + 0.5, 0, 1) * (1 - river)).astype(F32)                         # anything that is ground, for shadows to fall on
    ground = (walk * np.where(plateau > 0.5, foot, 1.0)).astype(F32)
    sand = land.sand(shape, HZ, seed + 40, far="#f3d6a0", mid="#e8b468", near="#c9823c", patch=0.08, ripple=0.0)
    over(pic, sand, ground)

    # ---- the fields between the river and the desert: thin strips of green, seen almost edge-on
    fields = mask_poly(shape, [(322, 268), (372, 266), (470, 272), (512, 284), (470, 300), (388, 306), (330, 296), (306, 284)], soft=2.2, wobble=3, seed=seed + 35) * walk
    rows = noise(shape, (150, 3.2), seed + 36, 2)
    crop = ramp(rows, [(0.0, "#5c7e40"), (0.35, "#84994e"), (0.6, "#a8ac5e"), (0.8, "#d6c07c"), (1.0, "#748c46")])
    over(pic, crop, fields * 0.92)
    land.haze(pic, HZ, "#f2e6c4", 0.25, 0.07, fields)

    # ---- wet sand along the water, and the bright line where the water ends
    wet = np.clip(blur(river, 5) * 2.2, 0, 1) * (1 - river)
    tint(pic, "#9c7c60", wet * 0.55)
    lipm = np.clip(blur(river, 1.4) * 2 - 0.6, 0, 1) * np.clip(1.6 - blur(river, 1.4) * 2, 0, 1)
    over(pic, "#eef8ee", (lipm * 0.55 * (noise(shape, (30, 4), seed + 41, 3) > 0.42)).astype(F32))

    # ---- low dunes on the right, each with its shaded side toward us
    land.dune(pic, [(430, 342), (520, 326), (620, 316), (720, 318), (800, 326)], [(430, 346), (520, 344), (620, 346), (720, 356), (800, 368)], ground=walk, amount=0.44, shade="#946f86")
    land.dune(pic, [(600, 390), (680, 372), (760, 366), (800, 368)], [(600, 396), (680, 404), (760, 414), (800, 418)], ground=walk, amount=0.42, shade="#946a80")
    land.dune(pic, [(336, 318), (396, 306), (452, 304)], [(336, 321), (396, 319), (452, 320)], ground=walk, amount=0.3, lip_amount=0.3)

    # ---- the track people have worn from the river up to the plateau
    path = curve(TRACK, 16)
    widths = [lerp(60, 5, (i / (len(path) - 1)) ** 0.6) for i in range(len(path))]
    trod = mask_line(shape, path, widths, soft=3.5) * walk
    worn = trod * (0.55 + 0.6 * noise(shape, (60, 14), seed + 45, 3))
    over(pic, vary("#f6dca6", shape, seed + 44, 0.05, 26), (worn * 0.34).astype(F32))
    tint(pic, "#b48c70", (blur(trod, 6) - trod).clip(0, 1) * 0.40)
    for side in (-0.22, 0.22):                               # the grooves the sledges' runners leave
        rut = [(px + side * wd, py) for (px, py), wd in zip(path, widths)]
        groove = mask_line(shape, rut, [max(0.9, wd * 0.045) for wd in widths], soft=0.9) * walk
        tint(pic, "#a67a5c", (groove * (0.35 + 0.5 * noise(shape, (40, 8), seed + 46, 3)) * 0.6).astype(F32))

    # ---- long shadows: each palm's own shape laid along the ground, and the wagon's
    for (px, py, hgt, lean, k) in PALMS:
        one = Sheet(shape)
        flora.palm(one, px, py, hgt, seed + 50 + k, lean=lean, light=-1, fronds=30 if hgt > 200 else 26)
        land.cast(pic, one.done()[1], (px, py), sun=SUN_UP, color="#6e5688", amount=0.36, ground=walk, toward=0.10, flat=0.30, soft=1.0 + hgt / 200)
    _, wa, _, wla = wagon.wagon(shape, WAGON)
    land.cast(pic, np.maximum(wa, wla), WAGON, sun=0.55, color="#5e4a7c", amount=0.55, ground=walk, toward=0.30, soft=2.0, upright=False)
    wx, wy = WAGON
    land.shadow(pic, mask_poly(shape, [(wx - 200, wy - 4), (wx + 60, wy - 8), (wx + 74, wy + 4), (wx - 190, wy + 8)], soft=3) * walk, "#5e4a7c", 0.5, 0)

    # ---- a cloud's shadow lies over the nearest sand; beyond it the plain is in full sun
    edge_y = 508 + (noise(shape, (220, 60), seed + 48, 3) - 0.5) * 70 - (x - 400) * 0.03
    cloud = step(0.0, 1.0, (y - edge_y) / 46.0)
    tint(pic, "#b98a74", (cloud * 0.36 * walk).astype(F32))
    # ---- the corners go deeper and warmer, to hold the eye in the picture
    corner = np.clip(((x - 400) / 400) ** 2 * 0.5 + ((y - 380) / 220).clip(0, 2) ** 2 * 0.5, 0, 1)
    tint(pic, "#c08a5c", (corner * 0.22 * walk).astype(F32))
    glow(pic, "#fff0c8", (np.clip(1 - np.abs(y - (HZ + 8)) / 30, 0, 1) * 0.08 * walk).astype(F32))     # dust in the air over the plain

    land.ripples(pic, HZ, seed + 47, walk * (1 - np.clip(trod * 2, 0, 1)) * (y > 380), amount=0.15)
    info.update(walk=walk, river=river, line=line, plateau=plateau, fields=fields)
    return np.clip(pic, 0, 1), info


def details(pic, info, seed=11, reeds=REEDS, lot=True, smoke=False):
    """The small crisp things, painted over the brushwork: far palms, the works on the pyramid, huts,
    the boat, stones, footprints. (`reeds=REEDS_APPROVED, lot=False, smoke=True` paints the backdrop as first
    approved.) Round four: the village's cooking smoke is no longer painted (`smoke=False`): smoke that stands
    still breaks the illusion, so the game draws it rising and drifting (layout.json "fx")."""
    shape = (H, W)
    x, y = grid(shape)
    rng = np.random.default_rng(seed + 77)
    walk = info["walk"]

    # ---- first, say the big hard things again, crisply, over the brushwork
    crisp = pic.copy()
    pyramids(crisp, seed)
    behind = info["plateau"] + (y > HZ)                      # only the part that stands against the sky
    pic[...] = lerp(pic, crisp, (0.72 * (1 - np.clip(behind, 0, 1)))[..., None])
    edge = Sheet(shape)
    land.strata(edge, info["line"], 334, 800, seed + 15)
    sky_line = [(float(px), float(info["line"][px])) for px in range(334, 800, 6)]
    edge.line(sky_line, "#fff4d0", 1.0, 0.7)                 # the plateau's rim in the sun
    land.crest(edge, curve([(470, 335), (520, 326), (620, 316), (720, 318), (780, 323)], 8), alpha=0.32)
    land.crest(edge, curve([(630, 383), (680, 372), (760, 366), (790, 367)], 8), alpha=0.32)
    edge.line([(0, HZ + 0.5), (348, HZ + 0.5)], "#4f8076", 1.0, 0.55)        # where the far bank meets its reflection
    bank = curve(BANK, 10)
    edge.line([(px - 1.0, py) for px, py in bank], "#f4fbf2", 1.1, 0.55)     # the edge of the water
    edge.line([(px + 1.2, py + 0.6) for px, py in bank], "#8a6850", 1.3, 0.45)
    edge.onto(pic)

    far = Sheet(shape)
    for k in range(30):                                      # palms on the far bank are only dabs
        px = rng.random() * 344
        py = 257 + (px / 344) * 5
        hgt = 6 + rng.random() * 7
        far.line([(px, py), (px + rng.normal(0, 1), py - hgt)], "#6a8a62", 1.0, 0.8)
        far.ellipse(px, py - hgt, 3.2, 2.0, "#5d8a56", 0.9)
    build.works(far, *GREAT, BUILT, seed + 1)
    build.wrap_ramp(far, *GREAT, seed + 2)
    for q in QUEENS:
        a, l, c, r = small(q)
        far.line([a, c], "#fffbe6", 0.9, 0.6)
    # the builders' village under the cliff, and its palms and cooking smoke
    for k, (hx, hy, hw, hh) in enumerate([(352, 292, 12, 7), (368, 289, 9, 6), (384, 293, 13, 7), (404, 290, 10, 6), (421, 294, 12, 7), (441, 291, 9, 6), (372, 297, 11, 6), (455, 296, 10, 6)]):
        build.hut(far, hx, hy, hw, hh, 5, seed + 30 + k)
    for k in range(9):
        px, py = 344 + rng.random() * 130, 286 + rng.random() * 12
        hgt = 12 + rng.random() * 9
        far.line([(px, py), (px + rng.normal(0, 1.5), py - hgt)], "#5a4a38", 1.1, 0.9)
        for a in np.linspace(0.3, 2.84, 6):
            far.line([(px, py - hgt), (px + np.cos(a) * 6, py - hgt - np.sin(a) * 4 + 2.5)], "#3f6a34" if a > 1.4 else "#2f5228", 1.2)
    far.onto(pic)
    for sx, sy in (VILLAGE_SMOKE if smoke else ()):          # smoke: thin, pale, leaning with the wind
        plume = mask_line(shape, curve([(sx, sy), (sx + 5, sy - 14), (sx + 16, sy - 26), (sx + 34, sy - 34)], 6), [1.5, 2.5, 4, 6, 8, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10][:19], soft=2.2)
        over(pic, "#f4ecdc", plume * 0.38)

    # ---- the boat bringing white stone across from the quarries, and what the water shows of it
    bx, by, bl = 132, 322, 92
    refl = Sheet(shape)
    build.boat(refl, bx, by + 1, bl, seed + 5, hull=("#27425a", "#27425a", "#27425a"), cargo="#b9d2d8", folk="#27425a")
    rc, ra = refl.done()
    rc, ra = rc[::-1], ra[::-1]                              # upside down, about the waterline
    shift = int(round(2 * (by + 1) - H))
    rc, ra = np.roll(rc, shift, axis=0), np.roll(ra, shift, axis=0)
    ra = warp(ra, 2.5, (26, 3), seed + 6) * np.clip(1 - (y - by) / 34, 0, 1) * (y > by)
    over(pic, rc, (ra * 0.5).astype(F32))
    b = Sheet(shape)
    build.boat(b, bx, by, bl, seed + 5)
    b.line([(bx - bl * 0.5, by + 1.2), (bx + bl * 0.5, by + 1.2)], "#f2fbf6", 1.0, 0.7)       # the wash along her side
    b.onto(pic)

    # ---- stones, the dropped block and its broken sledge, and tufts of grass
    near = Sheet(shape)
    zone = (walk > 0.5) & (y > 330) & ~((x > 470) & (y > 400))
    land.stones(near, pic, HZ, seed + 90, 70, zone=zone, ground=walk)
    for (rx, ry, r) in [(760, 342, 10), (776, 347, 6), (640, 352, 6), (84, 548, 13), (118, 560, 8), (330, 470, 6), (300, 584, 12), (326, 590, 7)]:
        land.rock_shadow(pic, rx, ry, r * 1.25, r * 0.85, ground=walk)
        land.rock(near, rx, ry, r * 1.25, r * 0.85, seed + rx)
    land.shadow(pic, mask_poly(shape, [(716, 350), (744, 347), (770, 356), (736, 360)], soft=1.5), "#665082", 0.5, 0)
    build.block(near, 708, 350, 22, 16, 15)
    near.line([(700, 353), (734, 356)], "#5a4030", 1.6)                                     # a runner of the sledge it came on
    near.line([(734, 356), (752, 359), (760, 356)], "#c8a878", 0.9, 0.9)                    # and the rope
    for k in range(16):                                      # halfa grass along the bank
        i = int(rng.random() * (len(BANK) - 2))
        gx = lerp(BANK[i][0], BANK[i + 1][0], rng.random()) + 8 + rng.random() * 30
        gy = lerp(BANK[i][1], BANK[i + 1][1], rng.random()) + rng.random() * 8
        flora.scrub(near, gx, gy, 5 + (gy - HZ) / 22, seed + 70 + k, colors=("#55652e", "#8c9c46", "#c8c672"))
    # reeds standing in the shallows, small with distance
    for (rx, ry, rw, rh, n) in reeds:
        flora.reeds(near, rx - 12, ry + 4, rw, rh, seed + rx, count=n)
    # small sneaker prints from the wagon up the track (his son went this way)
    walkway = curve([(470, 562), (472, 520), (486, 474), (496, 430), (494, 388), (487, 350), (486, 322)], 5)
    for i, (px, py) in enumerate(walkway):
        k = lerp(1.0, 0.36, i / len(walkway))
        side = 6 * k * (1 if i % 2 else -1)
        near.ellipse(px + side, py, 5.2 * k, 2.3 * k, "#a87850", 0.75)
        near.ellipse(px + side + 1.5 * k, py + 0.6 * k, 3.6 * k, 1.2 * k, "#7c5840", 0.55)
    near.onto(pic)
    if lot:
        bundle(pic)
    return pic


def bundle(pic):
    """Lot's bundle on the sand beside his place: a mantle of banded wool (madder, ochre and indigo on undyed),
    rolled and corded twice. It lies in the palm's shade, so its colours are shade colours, and its own shadow is
    a soft dark directly under it."""
    shape = (H, W)
    bx, by = BUNDLE
    g = (by - HZ) / (590 - HZ) * 160 / 175                  # pixels to a centimetre on the ground there
    L, D = 44 * g, 19 * g                                   # its length and its thickness
    x0, x1, top = bx - L / 2, bx + L / 2, by - D
    under = mask_ellipse(shape, bx + 1.0, by + 0.3, L * 0.58, D * 0.30, soft=0.8)
    under[under < 0.01] = 0                                  # (the blur leaves a faint haze over the whole picture: not wanted)
    land.shadow(pic, under, "#4c3c66", 0.45, 0)
    s = Sheet(shape)
    roll = [(x0 + D * 0.25, top), (x1 - D * 0.2, top + 0.2), (x1, top + D * 0.5), (x1 - D * 0.2, by), (x0 + D * 0.25, by - 0.2)]
    s.poly(roll, "#a3947f")                                  # undyed wool, in shade
    s.ellipse(x0 + D * 0.25, top + D * 0.5, D * 0.25, D * 0.5, "#b4a48c")        # its rolled end, toward the light
    s.line([(x0 + D * 0.25, top + D * 0.30), (x0 + D * 0.36, top + D * 0.52), (x0 + D * 0.22, top + D * 0.66)], "#6e604e", 0.8, 0.8)   # the turn of the cloth in it
    for at, width, color in ((0.22, 0.10, "#7a2f2c"), (0.40, 0.07, "#2e3858"), (0.50, 0.09, "#97703a"), (0.60, 0.07, "#2e3858"), (0.80, 0.10, "#7a2f2c")):
        cx = lerp(x0 + D * 0.25, x1 - D * 0.1, at)
        w = width * L / 2
        s.poly([(cx - w, top + 0.3), (cx + w, top + 0.4), (cx + w * 0.9, by - 0.3), (cx - w * 1.1, by - 0.4)], color)   # the bands go round the roll
    s.line([(x0 + D * 0.3, top + 0.6), (x1 - D * 0.3, top + 0.7)], "#c8b89c", 0.9, 0.55)       # the top of the roll, where the sky lights it
    s.line([(x0 + D * 0.3, by - 0.7), (x1 - D * 0.3, by - 0.6)], "#5a4a5c", 1.0, 0.5)          # and its underside
    for at in (0.30, 0.70):                                  # the cords, and a knot on the near one
        cx = lerp(x0 + D * 0.25, x1 - D * 0.1, at)
        s.line([(cx - 0.4, top - 0.2), (cx + 0.5, by + 0.1)], "#3e2c22", 0.9)
    s.ellipse(lerp(x0 + D * 0.25, x1 - D * 0.1, 0.30) - 0.3, top + 0.6, 1.0, 0.8, "#3e2c22")
    s.onto(pic)
    return pic


def palms_plane(seed=11):
    """The three palms on the bank, alone on a clear sheet."""
    s = Sheet((H, W))
    for (px, py, hgt, lean, k) in PALMS:
        flora.palm(s, px, py, hgt, seed + 50 + k, lean=lean, light=-1, fronds=30 if hgt > 200 else 26)
    return s.done()


def front_plane(seed=11):
    """Papyrus at the very front, bottom left: tall, dark against the bright water, a few heads in the sun."""
    s = Sheet((H, W))
    flora.papyrus_stand(s, 38, 604, 120, 250, seed + 3, count=13, greens=("#14261a", "#2c5226", "#6f963a", "#c6cc72"))
    flora.papyrus_stand(s, 130, 606, 70, 150, seed + 4, count=7, greens=("#182c1c", "#35602a", "#7fa23e", "#d0d27a"))
    flora.reeds(s, 60, 602, 90, 70, seed + 5, count=40, greens=("#14261a", "#2c5226", "#5f8a36"))
    return s.done()


def wagon_plane(back, take=(), mirror=True):
    """The wagon, painted to stand on this sand."""
    return wagon.render((H, W), WAGON, 1.0, take=take, mirror=mirror, back=back)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def finish_keeping(picture, approved, name, colors, extra=8, seed=7, speckle=0.014, amount=0.02, far=0.06, since=None):
    """finish() for a backdrop changed in a few places since it was approved. The palette is the one the approved
    picture got (worked out from it again, exactly as finish() did), so every pixel that was not changed comes out
    exactly as it was. The changed places may also use up to `extra` colours of their own, added at the end of the
    palette, for colours the approved palette is `far` from. -> (file size, mask of the changed places).
    `since` (round four) is the backdrop as round three left it: its palette, extra colours and all, is worked out
    again exactly as it was, and only where `picture` differs from it is anything reduced again, with that palette."""
    idx, pal, changed = _keeping(since if since is not None else picture, approved, colors, extra, seed, speckle, amount, far)
    if since is not None:
        changed = np.abs(picture - since).max(axis=2) > 0.5 / 255
        idx = np.where(changed, to_palette(grain(picture, seed, amount), pal, speckle=speckle), idx)
    save(name, idx, pal)
    return os.path.getsize(name), changed


def _keeping(picture, approved, colors, extra, seed, speckle, amount, far):
    """What finish_keeping() works out before it saves. -> (indexes, palette, changed)"""
    g0 = grain(approved, seed, amount)
    pal = palette_of([g0.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((g0 * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    g = grain(picture, seed, amount)
    changed = np.abs(picture - approved).max(axis=2) > 0.5 / 255           # (a change too small to show is no change)
    idx = np.where(changed, to_palette(g, pal, speckle=speckle), to_palette(g0, pal, speckle=speckle))
    if changed.any() and extra:
        px = g[changed]
        gap = np.sqrt(((px[:, None, :] - pal[None, :, :]) ** 2).sum(axis=2).min(axis=1))
        odd = px[gap > far]
        if len(odd) >= 2:
            more = palette_of([odd.reshape(-1, 1, 3)], colors=min(extra, len(odd)))
            pal = np.concatenate([pal, more])
            idx = np.where(changed, to_palette(g, pal, speckle=speckle), idx)
    return idx, pal, changed


def finish_keeping_cut(picture, alpha, approved, approved_alpha, name, colors, seed=7, speckle=0.014, amount=0.02):
    """finish() for a cut-out changed in a few places since it was approved (round four: the donkey without its
    painted rings). The palette is the one the approved cut-out got, worked out from it again exactly as finish()
    did, and every pixel that did not change keeps its old index; the new mask may be smaller. -> file size."""
    g0 = grain(approved, seed, amount)
    sample_of = g0[approved_alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    changed = np.abs(picture - approved).max(axis=2) > 0.5 / 255
    idx = np.where(changed, to_palette(grain(picture, seed, amount), pal, speckle=speckle), to_palette(g0, pal, speckle=speckle))
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def reduce(picture, colors, alpha=None, seed=7, speckle=0.014, amount=0.02):
    """What finish() does before it saves: grain, then a palette of the picture's own. -> (indexes, palette)."""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    return to_palette(g, pal, speckle=speckle), pal


def save_cut(name, idx, pal, mask):
    """Save part of a palette picture as a cut-out, with only the colors it uses."""
    used = np.unique(idx[mask])
    remap = np.zeros(256, dtype=np.uint8)
    remap[used] = np.arange(len(used))
    save(name, remap[idx], pal[used], mask.astype(F32))
    return os.path.getsize(name)


def wagon_pictures(pic, back_rgb):
    """The wagon and everything on it that changes: wagon.png (now without its door mirror), mirror.png,
    and the suitcase, the trunk and the cooler standing open.

    The wagon is brushed once and reduced with the palette it always had, so wagon.png and mirror.png laid
    together are, pixel for pixel, the wagon as it was first painted. One fault is mended on the way: where
    its paint is thin (see wagon.thin) the first cut-out was clear, and people behind the car showed
    through the roof and the rear panels. Those places are now filled with exactly the ground that showed
    there, so the picture looks as it did and the car is solid."""
    w1, w0, wa, mirror = wagon.render_pair((H, W), WAGON, 1.0, back=pic)
    idx, pal = reduce(w1, 72, wa)                                    # with the mirror: the picture as approved
    idx0 = to_palette(grain(w0, 7, 0.02), pal, speckle=0.014)        # the same grain and palette, without it
    solid = ~(wa < 0.5)
    mirror = (mirror | (idx != idx0)) & solid
    faint, _ = wagon.thin((H, W), WAGON)
    sand, which = np.unique(back_rgb[faint], axis=0, return_inverse=True)
    out = idx0.copy()
    out[faint] = len(pal) + which.reshape(-1)
    save("out/egypt1/wagon.png", out, np.concatenate([pal, sand.astype(F32) / 255]), (solid | faint).astype(F32))
    sizes = {"wagon": os.path.getsize("out/egypt1/wagon.png"), "mirror": save_cut("out/egypt1/mirror.png", idx, pal, mirror)}
    for name in wagon.PIECES:
        c, a, notes = wagon.open_state((H, W), WAGON, name, back=pic)
        assert not notes["bare"].any(), name + ": the open piece leaves a hole where the shut one was"
        sizes[name + "-open"] = finish(c, f"out/egypt1/{name}-open.png", 56, a)
    # The open trunk as the story empties it (round twelve): Dad takes the flashlight first and the windshield shade
    # later, and each goes out of the picture as it goes out of the trunk (egypt-crash.js reads the facts and shows the
    # right one). The suitcase and the cooler keep their one picture: the sunglasses and General Feathers lie under the
    # shirts, and the cooler is never short of a root beer.
    for name, gone in TRUNK_STATES:
        c, a, notes = wagon.open_state((H, W), WAGON, "trunk", back=pic, take=gone)       # (with the shade gone, a corner of the shut lid's outline shows the sand: open_state paints it)
        sizes[name] = finish(c, f"out/egypt1/{name}.png", 56, a)
    return sizes, (w1, wa)


TRUNK_STATES = (("trunk-open-1", ("flashlight",)), ("trunk-open-2", ("flashlight", "shade")))     # the trunk's emptier pictures: without this


STEAM = (472, 498)                                          # where the steam leaves the front edge of the hood (the bottom middle of its frames)
DONKEY = (198, 420)                                         # where the ground under its middle is: at the water's edge, in front of the near palm
DONKEY_SCALE = 1.1 * (160 / 175) * (DONKEY[1] - HZ) / (590 - HZ)   # pixels to a centimetre there (and he is a big small donkey)


def river(seed=11):
    """The river's mask, as under() lays the water."""
    return mask_poly((H, W), [(0, HZ), (350, HZ)] + BANK[1:] + [(0, 546)], wobble=1.5, seed=seed + 30)


def donkey_plane(back, fast=False, rings=False):
    """Lot's donkey with its two jars, drinking at the water's edge, and its shadow on the sand under it. (`rings=True`:
    with the rings on the water round its muzzle painted in, as approved in round three; round four leaves them to
    the game, which draws them spreading from MUZZLE.)"""
    import egypt1_donkey
    return egypt1_donkey.render((H, W), DONKEY, DONKEY_SCALE, back, fast=fast, jar_at=None, drink=egypt1_donkey.DRINK,
                                water=river(), flat=(DONKEY[1] - HZ) / 800, rings_on=rings)


def lay(names, out, folder="out/egypt1"):
    """Lay finished pictures over one another to look at. A name may be (name, x, y) for a cropped sprite
    whose top left corner goes there."""
    im = Image.open(f"{folder}/{names[0]}.png").convert("RGBA")
    for n in names[1:]:
        n, x, y = n if isinstance(n, tuple) else (n, 0, 0)
        top = Image.open(f"{folder}/{n}.png").convert("RGBA")
        im.alpha_composite(top, (int(x), int(y)))
    im.convert("RGB").save(out)
    return im


def split_palms():
    """palms.png again as three pictures, one palm in each (palm-1.png is the nearest), made from its own
    pixels: laid together in any order they are palms.png exactly. With one base each, somebody standing
    between two palms is sorted rightly with both."""
    alphas = []
    for (px, py, hgt, lean, k) in PALMS:
        one = Sheet((H, W))
        flora.palm(one, px, py, hgt, 11 + 50 + k, lean=lean, light=-1, fronds=30 if hgt > 200 else 26)
        alphas.append(one.done()[1])
    seen = [a.copy() for a in alphas]
    for i in range(len(seen)):                                       # a palm painted later lies over the ones before
        for j in range(i + 1, len(seen)):
            seen[i] *= 1 - alphas[j]
    owner = np.argmax(np.stack(seen), axis=0)
    whole = Image.open("out/egypt1/palms.png")
    pal = whole.getpalette()
    idx = np.asarray(whole)
    clear = whole.info["transparency"]
    for i in range(len(PALMS)):
        part = np.where(owner == i, idx, clear).astype(np.uint8)
        im = Image.fromarray(part, "P")
        im.putpalette(pal)
        im.save(f"out/egypt1/palm-{i + 1}.png", optimize=True, transparency=clear)
    return [py for (px, py, hgt, lean, k) in PALMS]


def hull(mask, most=10):
    """The outline of a mask as a polygon with no dents and at most `most` corners."""
    ys, xs = np.nonzero(mask)
    pts = sorted(set(zip(xs.tolist(), ys.tolist())))

    def half(points):
        out = []
        for p in points:
            while len(out) >= 2 and (out[-1][0] - out[-2][0]) * (p[1] - out[-2][1]) - (out[-1][1] - out[-2][1]) * (p[0] - out[-2][0]) <= 0:
                out.pop()
            out.append(p)
        return out
    ring = half(pts)[:-1] + half(pts[::-1])[:-1]
    while len(ring) > most:                                          # drop the corner that matters least
        def lost(i):
            (ax, ay), (bx, by), (cx, cy) = ring[i - 1], ring[i], ring[(i + 1) % len(ring)]
            return abs((bx - ax) * (cy - ay) - (by - ay) * (cx - ax))
        ring.pop(min(range(len(ring)), key=lost))
    return [[int(x), int(y)] for x, y in ring]


def hug(mask, tol=1.2):
    """A polygon that hugs a mask: down its left edge and back up its right edge, row by row (so it bridges the gaps
    between legs), simplified to within `tol` pixels."""
    rows = [y for y in range(mask.shape[0]) if mask[y].any()]
    left = [(int(np.nonzero(mask[y])[0][0]), y) for y in rows]
    right = [(int(np.nonzero(mask[y])[0][-1]) + 1, y) for y in rows]
    pts = left + [(left[-1][0], rows[-1] + 1), (right[-1][0], rows[-1] + 1)] + right[::-1]

    def simplify(p):
        (x0, y0), (x1, y1) = p[0], p[-1]
        n = max(np.hypot(x1 - x0, y1 - y0), 1e-9)
        d = [abs((y1 - y0) * (x - x0) - (x1 - x0) * (y - y0)) / n for x, y in p[1:-1]]
        if not d or max(d) <= tol:
            return [p[0], p[-1]]
        i = int(np.argmax(d)) + 1
        return simplify(p[:i + 1])[:-1] + simplify(p[i:])
    return [[int(x), int(y)] for x, y in simplify(pts)]


def box(mask, pad=0):
    ys, xs = np.nonzero(mask)
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 1 + 2 * pad, int(ys.max() - ys.min()) + 1 + 2 * pad]


def fx_marks():
    """Round four: everything in this place that moves by nature, for the game to draw moving (layout.json "fx").
    Each mark is in the engine's own terms (js/engine/effects.js): where the thing is, its depth (`base`, as a plane's;
    none for water lying on the ground, which the engine lays under everybody), and how the painting had it."""
    import egypt1_donkey
    r = lambda pts: [[int(round(x)), int(round(y))] for x, y in pts]
    mx, my = egypt1_donkey.muzzle(DONKEY, DONKEY_SCALE, egypt1_donkey.DRINK)
    k = DONKEY_SCALE / 1.1                                           # pixels to a centimetre on the water there, as the rings were painted
    flat = round((DONKEY[1] - HZ) / 800, 3)
    river = r([(0, HZ + 2), (344, HZ + 2)] + [(x - 1, y) for x, y in BANK[1:8]] + [(0, 532)])
    out = []
    for i, (sx, sy) in enumerate(VILLAGE_SMOKE):
        out.append({"type": "smoke", "id": f"village-smoke-{i + 1}", "at": [sx, sy], "base": 296,
                    "color": "#f4ecdc", "opacity": 0.38, "height": 36, "width": [1.5, 10], "lean": [34, -34], "rate": 2,
                    "what": "a cooking fire's smoke over the builders' village, far off under the plateau: a thin pale thread. The painting had it rising "
                            "straight for a few pixels, then bending away to the right with the wind off the river: 36 px up, 34 px over"})
    out.append({"type": "ripples", "id": "donkey-rings", "at": [round(mx, 1), round(my, 1)], "radius": [1.5, round(32 * k, 1)], "flat": flat,
                "every": [0.8, 1.8], "rings": 2, "speed": 9, "color": "#f2fbf8", "trough": "#46809e", "opacity": 0.7, "clip": river,
                "what": "rings spreading on the river from the donkey's muzzle while he drinks. No base: they lie on the water, under everybody (the donkey's "
                        "cut-out covers their middle, under his head). The painting had three at once, 4, 8.4 and 14 px across, each broken twice, "
                        "fainter as they spread. 'clip' is the river: a ring must not run out onto the sand (the bank is a few px right of the muzzle)"})
    out.append({"type": "shimmer", "id": "river", "poly": river,
                "holes": [[84, 280, 98, 62], [280, 287, 22, 24], [249, 308, 24, 33], [214, 335, 27, 41]], "color": "#fff6e2", "opacity": 0.4,
                "what": "the Nile near this bank: light moving on the water, very gently (the painting's own streaks and glints stay). 'holes' (rects x, y, w, h) "
                        "keep it off the boat with its mast and its reflection, and off the three reed beds in the shallows"})
    for i, (px, py, hgt, lean, sd) in enumerate(PALMS):
        out.append({"type": "sway", "id": f"palm-{i + 1}-crown", "plane": f"palm-{i + 1}", "anchor": "bottom", "at": [px, py],
                    "amount": round(0.006 * hgt, 1), "period": 4.5, "wave": 300, "lean": 0.2, "optional": True,
                    "what": "the palm's crown stirring in the warm wind off the river; its foot does not move (anchor bottom, at its foot). Small and slow"})
    out.append({"type": "birds", "kind": "flyers", "id": "kites", "lanes": [[[-20, 46], [820, 22]], [[-20, 120], [820, 64]]], "every": [18, 40], "group": [1, 2],
                "speed": 40, "scale": 0.85, "optional": True, "new": True,
                "frames": {"dir": "art/scenes/egypt-site/", "glide": "kite-0.png", "flap": ["kite-1.png", "kite-0.png", "kite-2.png", "kite-0.png"], "bank": "kite-3.png", "middle": [6.5, 5.0]},
                "what": "NEW (no birds were painted here): now and then a kite or two crossing high over the river and the plateau, gliding, a few beats. "
                        "The frames are the building site's kites (egypt-site). No base: they are behind every cut-out, so they pass behind the palms' crowns"})
    out.append({"type": "sway", "id": "papyrus", "plane": "papyrus", "anchor": "bottom", "amount": 1.0, "period": 3.0, "optional": True,
                "what": "the papyrus and reeds at the very front, bottom left (front.png, the plane the scene calls 'papyrus': nothing but that clump), stirring"})
    return out


def layout(steam_foot):
    """Write layout.json: the numbers the game needs, taken from the finished pictures and from the
    measurements they were painted with."""
    import json
    import egypt1_donkey
    from solid import Draft
    d = Draft(None, (WAGON[0] - 232, WAGON[1]), 1.0, 7.0, pivot=(232, 0), depth=(-0.50, 0.30))
    P = lambda *p: [round(v, 1) for v in d.pt(*p)]
    alpha = lambda name: np.asarray(Image.open(f"out/egypt1/{name}.png").convert("RGBA"))[..., 3] > 0
    r = lambda pts: [[int(round(x)), int(round(y))] for x, y in pts]
    bank = curve(BANK, 6)
    ashore = lambda x, y, by=13: (x + 0.51 * by, y + 0.86 * by)      # a step in from the water's edge
    walk = r([(484, 308), (504, 308), (518, 322), (560, 340), (640, 352), (800, 360), (800, 596), (12, 596), (12, 556)]
             + [ashore(*BANK[i]) for i in (7, 6, 5, 4, 3)] + [(284, 334), (330, 326), (440, 326), (474, 318)])
    # ---- what stands on the ground
    heap = [(372, 549), (394, 530), (424, 514), (456, 502), (490, 499), (522, 506), (552, 512)]
    under_wagon = r(heap + [(757, 516), (797, 536), (793, 549), (640, 553), (550, 558), (450, 558)])
    dc, da, dlc, dla = egypt1_donkey.donkey((H, W), DONKEY, DONKEY_SCALE, jar_at=None, drink=egypt1_donkey.DRINK)
    hoofs = egypt1_donkey.hooves(DONKEY, DONKEY_SCALE)
    hx0, hx1 = min(h[0] - h[2] for h in hoofs), max(h[0] + h[2] for h in hoofs)
    under_donkey = r([(hx0 - 6, DONKEY[1] - 9), (hx1 + 6, DONKEY[1] - 9), (hx1 + 6, DONKEY[1] + 6), (hx0 - 6, DONKEY[1] + 6)])
    blocked = [under_wagon, under_donkey]
    for (px, py, hgt, lean, k) in PALMS:                             # the foot of each palm
        w = hgt * 0.052
        blocked.append(r([(px - w, py - w * 0.7), (px + w, py - w * 0.7), (px + w * 1.2, py + 2), (px - w * 1.2, py + 2)]))
    for (rx, ry, rr) in [(84, 548, 13), (300, 584, 12)]:            # the two big stones in the foreground
        blocked.append(r([(rx - rr * 1.3, ry - 2), (rx - rr * 0.6, ry - rr * 0.9), (rx + rr * 0.8, ry - rr * 0.9), (rx + rr * 1.5, ry - 2), (rx + rr * 1.3, ry + 3), (rx - rr * 1.2, ry + 3)]))
    # ---- the wagon and its parts (measured the way wagon.py draws them)
    y = wagon.RACK_Y + 1
    suitcase = [P(150, y, 56), P(150, y + 15, 56), P(200, y + 15, 56), P(204, y, 62), (671.1, 437.7), P(200, y, 14), P(150, y, 14)]
    trunk = [P(204, y, 62), P(204, y + 31, 62), P(250, y + 31, 62), (708.6, 398.6), P(253, y + 23, 53), P(254, y, 52), P(254, y, 18), P(250, y, 8), P(204, y, 8)]
    cooler = [P(253, y + 23, 53), P(282, y + 23, 53), P(282, y + 23, 17), P(281, y, 18), P(254, y, 18), P(254, y, 52)]
    car = [P(10, 57, 70), P(104, 61, 70), P(132, 91, 70), P(146, 99, 66), P(284, 99, 66), P(284, 99, 4), P(282, 92, 0), P(294, 62, 0), P(300.5, 30, 0), P(296, 20, 0),
           (744, 543), (700, 543), (640, 548), (618, 540), (598, 526), (574, 516), (546, 513), (520, 507), (490, 500)]
    hood = [P(10, 57, 70), P(104, 61, 70), P(104, 61, 0), (574, 516), (546, 513), (520, 507), (490, 500)]
    window = [P(138, 64), P(147, 88), P(176, 89), P(176, 64)]
    mirror = box(alpha("mirror"), 3)
    stand = lambda x: [int(x), 563]                                  # on the sand in front of the car, on our side
    things = [
        {"id": "mirror", "what": "the door mirror", "shape": {"rect": mirror}, "stand": stand(622), "face": "N"},
        {"id": "glovebox", "what": "the glovebox, through the driver's window", "shape": {"poly": r(window)}, "stand": stand(642), "face": "N"},
        {"id": "suitcase", "what": "the suitcase on the roof (left)", "shape": {"poly": r(suitcase)}, "stand": stand(648), "face": "N"},
        {"id": "trunk", "what": "the old trunk on the roof (middle)", "shape": {"poly": r(trunk)}, "stand": stand(692), "face": "N"},
        {"id": "cooler", "what": "the cooler on the roof (right)", "shape": {"poly": r(cooler)}, "stand": stand(730), "face": "N"},
        {"id": "hood", "what": "the hood, nose down in the sand, steaming", "shape": {"poly": r(hood)}, "stand": stand(566), "face": "N"},
        {"id": "wagon", "what": "the family wagon as a whole", "shape": {"poly": r(car)}, "stand": stand(604), "face": "N"},
        {"id": "donkey", "what": "Lot's donkey, head down, drinking at the water's edge, two water jars slung on it", "plane": "donkey",
         "shape": {"poly": hug((da > 0.5) | (dla > 0.5))}, "stand": [244, 440], "face": "W"},
        {"id": "reeds", "what": "the reed bed in the shallows", "shape": {"rect": [212, 334, 30, 42]}, "stand": [244, 392], "face": "W"},
        {"id": "footprints", "what": "small sneaker prints going up the track (following them takes him up it)",
         "shape": {"poly": [[468, 496], [498, 496], [510, 460], [514, 420], [512, 380], [506, 340], [502, 318], [474, 318], [474, 350], [480, 390], [480, 430], [472, 462]]},
         "stand": [424, 502], "face": "NE"},
        {"id": "block", "what": "a dropped block of white stone and its broken sledge, on the far dune", "shape": {"rect": [698, 326, 66, 36]}, "stand": [716, 374], "face": "N"},
        {"id": "boat", "what": "a boat bringing stone across the river", "shape": {"rect": [84, 280, 98, 48]}, "stand": [246, 448], "face": "W"},
        {"id": "pyramid", "what": "the Great Pyramid, nearly finished", "shape": {"poly": r([GREAT[0], GREAT[1], GREAT[2], GREAT[3]])}, "stand": [540, 420], "face": "N"},
        {"id": "river", "what": "the Nile", "shape": {"poly": r([(0, 266), (340, 266)] + [(x - 4, y) for x, y in BANK[1:8]] + [(0, 540)])}, "stand": [240, 470], "face": "W"},
    ]
    g = (BUNDLE[1] - HZ) / (590 - HZ) * 160 / 175
    lot = {"note": "Lot sits on the sand here (the game draws him), in the near palm's shade: with the sun low on the left the crown's shadow lies to the "
                   "right of the palm's foot, and this is its darkest part, a few steps from his donkey at the water",
           "hips": list(LOT), "seated": "ground", "face": "E", "stand": list(LOT_TALK), "standFace": "W",
           "solid": r([(368, 418), (428, 418), (434, 430), (428, 440), (374, 440), (366, 430)]),
           "bundle": {"at": list(BUNDLE), "box": r([(BUNDLE[0] - 22 * g, BUNDLE[1] - 19 * g), (BUNDLE[0] + 22 * g, BUNDLE[1] + 1)]),
                      "what": "his bundle, painted into the backdrop at his left hand, behind him: a mantle of banded wool (madder, ochre, indigo on undyed), rolled and corded"}}
    exits = [{"id": "track", "to": "egypt-site", "what": "the track up to the plateau: a wide band of it, the sand on either side included, so that a click anywhere near it is a click on it", "shape": {"poly": [[452, 286], [532, 284], [544, 330], [540, 380], [530, 420], [512, 420], [506, 380], [500, 340], [496, 318], [480, 318], [480, 350], [486, 390], [486, 420], [470, 420], [460, 380], [454, 330]]}, "stand": [500, 372], "face": "N"}]
    base = [[490, 541], [790, 537]]                                  # the line where the wagon meets the sand
    up = lambda by: [[base[0][0], base[0][1] + by], [base[1][0], base[1][1] + by]]
    frames = [f"steam-{i}.png" for i in range(4)]
    import egypt1_steam
    doc = {
        "id": "egypt-crash", "horizon": HZ, "full": 590, "light": "afternoon sun, low on the left: shadows fall to the right and a little toward us",
        "walk": walk, "blocked": blocked,
        "planes": [
            {"id": "palms", "file": "palms.png", "base": 400},
            {"id": "donkey", "file": "donkey.png", "base": int(DONKEY[1]), "solid": under_donkey, "note": "drinking at the water's edge; its shadow on the sand is painted into this cut-out (round four: the rings on the water are not: see fx 'donkey-rings')"},
            {"id": "wagon", "file": "wagon.png", "base": base, "solid": under_wagon, "note": "painted without the door mirror"},
            {"id": "mirror", "file": "mirror.png", "base": up(0.2), "note": "shown until the mirror is taken"},
            {"id": "suitcase-open", "file": "suitcase-open.png", "base": up(0.4), "note": "shown while the suitcase is open; hides the shut one"},
            {"id": "trunk-open", "file": "trunk-open.png", "base": up(0.6), "note": "shown while the trunk is open; must be laid after suitcase-open",
             "states": {"full": "trunk-open.png", "flashlight-gone": "trunk-open-1.png", "shade-gone": "trunk-open-2.png"},
             "states_note": "round twelve: the same cut-out, pixel for pixel, less the flashlight once Dad has taken it, and less the shade too once he has taken that"},
            {"id": "cooler-open", "file": "cooler-open.png", "base": up(0.8), "note": "shown while the cooler is open; must be laid after trunk-open"},
            {"id": "steam", "frames": frames, "fps": 6, "at": list(steam_foot), "foot": [egypt1_steam.W // 2, egypt1_steam.H], "base": up(1.0), "note": "cropped RGBA frames, placed by the middle of the bottom edge"},
            {"id": "front", "file": "front.png", "plane": "front"},
        ],
        "palms_split": {"note": "palms.png cut into its three palms, pixel for pixel (any order): use these three in place of 'palms' so that somebody standing between two palms is sorted rightly with each",
                        "planes": [{"id": f"palm-{i + 1}", "file": f"palm-{i + 1}.png", "base": int(p[1])} for i, p in enumerate(PALMS)]},
        "things": things, "exits": exits,
        "marks": {"dad": [420, 570], "lot": list(LOT), "talkToLot": list(LOT_TALK), "muzzle": [round(v, 1) for v in egypt1_donkey.muzzle(DONKEY, DONKEY_SCALE, egypt1_donkey.DRINK)]},
        "lot": lot,
        "steam": list(steam_foot),
        "fx": fx_marks(),
        "notes": ["things are listed most particular first: where shapes overlap, the earlier one is meant",
                  "the three open pieces of luggage may be shown in any combination, laid in the order given (suitcase, trunk, cooler)",
                  "wagon.png + mirror.png is the wagon as first approved; three patches of thin paint that were see-through (roof strip, rear panels) are now solid",
                  "round three: the donkey stands at the water's edge in front of the near palm and drinks; the reed clump that stood in the water there is "
                  "gone from back.png, and Lot's bundle is painted at his place; nothing else in back.png moved",
                  "round four: nothing that moves by nature is painted still. The village's two threads of cooking smoke are gone from back.png and the "
                  "rings round the donkey's muzzle from donkey.png (every other pixel of both is as it was); 'fx' says where the game draws them moving, "
                  "and where the river shimmers"],
    }
    one = lambda v: json.dumps(v, separators=(", ", ": "))             # (written so that a person can read it: one thing to a line)
    rows = []
    for key, value in doc.items():
        if isinstance(value, list) and value and isinstance(value[0], (dict, list)) and key != "walk":
            rows.append(f' "{key}": [\n' + ",\n".join("  " + one(v) for v in value) + "\n ]")
        elif isinstance(value, dict) and "planes" in value:
            rows.append(f' "{key}": {{"note": {one(value["note"])},\n  "planes": [\n' + ",\n".join("   " + one(v) for v in value["planes"]) + "\n  ]}")
        else:
            rows.append(f' "{key}": {one(value)}')
    with open("out/egypt1/layout.json", "w") as f:
        f.write("{\n" + ",\n".join(rows) + "\n}\n")
    return json.load(open("out/egypt1/layout.json"))


def check_layout(doc, comp, out):
    """Draw everything in the layout over the finished picture, to check it by eye."""
    from PIL import ImageDraw
    k = 2
    im = Image.open(comp).convert("RGB").resize((W * k, H * k), Image.NEAREST)
    dr = ImageDraw.Draw(im, "RGBA")
    ring = lambda pts, color, width=2: dr.line([(x * k, y * k) for x, y in pts + pts[:1]], fill=color, width=width)
    ring(doc["walk"], (255, 255, 255, 230), 3)
    for b in doc["blocked"]:
        dr.polygon([(x * k, y * k) for x, y in b], fill=(255, 0, 0, 70), outline=(255, 0, 0, 255))
    for t in doc["things"] + doc["exits"]:
        s = t["shape"]
        pts = s["poly"] if "poly" in s else [[s["rect"][0], s["rect"][1]], [s["rect"][0] + s["rect"][2], s["rect"][1]], [s["rect"][0] + s["rect"][2], s["rect"][1] + s["rect"][3]], [s["rect"][0], s["rect"][1] + s["rect"][3]]]
        color = (0, 255, 255, 255) if "to" not in t else (255, 255, 0, 255)
        ring(pts, color)
        sx, sy = t["stand"]
        dr.ellipse([sx * k - 5, sy * k - 5, sx * k + 5, sy * k + 5], fill=color)
        dr.text((min(p[0] for p in pts) * k + 3, min(p[1] for p in pts) * k - 13), t["id"], fill=(255, 255, 255, 255))
        dr.text((sx * k + 7, sy * k - 5), t["id"] + (" " + t["face"] if "face" in t else ""), fill=(0, 0, 0, 255))
    for name, (mx, my) in doc["marks"].items():
        size = 160 * (my - HZ) / (590 - HZ) * (0.55 if name == "lot" else 1.0)      # (Lot is seated)
        dr.rectangle([(mx - size * 0.15) * k, (my - size) * k, (mx + size * 0.15) * k, my * k], outline=(255, 0, 255, 255), width=2)
        dr.text(((mx + size * 0.15) * k + 3, (my - size) * k), name, fill=(255, 0, 255, 255))
    if "lot" in doc:
        dr.polygon([(x * k, y * k) for x, y in doc["lot"]["solid"]], outline=(255, 140, 0, 255))
        sx, sy = doc["lot"]["stand"]
        dr.ellipse([sx * k - 5, sy * k - 5, sx * k + 5, sy * k + 5], fill=(255, 140, 0, 255))
        dr.text((sx * k + 7, sy * k - 5), "talk to Lot " + doc["lot"]["standFace"], fill=(0, 0, 0, 255))
    for p in doc["planes"]:
        if "base" in p:
            b = p["base"]
            line = [(0, b), (W, b)] if not isinstance(b, list) else b
            dr.line([(x * k, y * k) for x, y in line], fill=(0, 255, 0, 200), width=1)
    sx, sy = doc["steam"]
    dr.line([(sx * k - 8, sy * k), (sx * k + 8, sy * k)], fill=(255, 255, 255, 255), width=2)
    dr.line([(sx * k, sy * k - 8), (sx * k, sy * k + 8)], fill=(255, 255, 255, 255), width=2)
    im.save(out)


def whole_picture(pic, planes, name="out/egypt1-2-all.png"):
    """Everything as painted, before the palettes, laid together to look at."""
    whole = pic.copy()
    for color, alpha in planes:
        over(whole, color, (alpha > 0.5).astype(F32))
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(name)


if __name__ == "__main__":
    # python3 egypt1.py          paints everything and writes out/egypt1/
    # python3 egypt1.py fast     skips the brush pass and writes only out/egypt1-2-all.png, to compose by
    # python3 egypt1.py extras   repaints only the changing parts (wagon, luggage, donkey, steam, layout) on the backdrop as last painted
    t0 = time.time()
    os.makedirs("out/egypt1", exist_ok=True)
    os.makedirs("out/egypt1-look", exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "extras":
        pic = np.load("out/egypt1-look/pic.npy")
    else:
        base, info = under()
        Image.fromarray((base * 255).astype(np.uint8)).save("out/egypt1-1-under.png")
        print("under", round(time.time() - t0, 1))
        pic = base.copy() if mode == "fast" else strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.22)
        approved = pic.copy()
        details(approved, info, reeds=REEDS_APPROVED, lot=False, smoke=True)    # the backdrop as first approved, for its palette
        since = pic.copy()
        details(since, info, smoke=True)                                    # and as round three left it, for its extra colours
        details(pic, info)
        pc, pa = palms_plane()
        fc, fa = front_plane()
        if mode == "fast":
            dc, da, notes = donkey_plane(pic, fast=True)
            whole_picture(pic, [(pc, pa), (dc, da), wagon_plane(pic), (fc, fa)])
            print("painted", round(time.time() - t0, 1))
            sys.exit()
        size, changed = finish_keeping(pic, approved, "out/egypt1/back.png", 144, since=since)
        ys, xs = np.nonzero(changed)
        print("back", size, "repainted since round three", int(changed.sum()), "pixels in x", xs.min(), "..", xs.max(), "y", ys.min(), "..", ys.max())
        print("palms", finish(pc, "out/egypt1/palms.png", 40, pa))
        print("front", finish(fc, "out/egypt1/front.png", 32, fa))
        np.save("out/egypt1-look/pic.npy", pic)                      # (kept for `extras`)
    back_rgb = np.asarray(Image.open("out/egypt1/back.png").convert("RGB"))
    sizes, (wc, wa) = wagon_pictures(pic, back_rgb)
    print(sizes)
    dc, da, notes = donkey_plane(pic)
    dc0, da0, _ = donkey_plane(pic, rings=True)                       # the donkey as approved in round three, for its palette
    print("donkey", finish_keeping_cut(dc, da, dc0, da0, "out/egypt1/donkey.png", 72))
    if mode != "extras":
        whole_picture(pic, [(pc, pa), (dc, da), (wc, wa), (fc, fa)])
    import egypt1_steam
    egypt1_steam.save("out/egypt1")
    print("palms split, bases", split_palms())
    doc = layout(STEAM)
    steam = ("steam-0", STEAM[0] - egypt1_steam.W // 2, STEAM[1] - egypt1_steam.H)
    lay(["back", "palms", "donkey", "wagon", "mirror", steam, "front"], "out/egypt1-comp.png")
    lay(["back", "palms", "donkey", "wagon", "suitcase-open", "trunk-open", "cooler-open", steam, "front"], "out/egypt1-open-comp.png")
    check_layout(doc, "out/egypt1-comp.png", "out/egypt1-look/layout-check.png")
    print("done", round(time.time() - t0, 1))

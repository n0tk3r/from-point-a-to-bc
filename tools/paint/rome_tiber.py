"""Rome, the Ides of March, 44 B.C.: across the Tiber. The right bank of the river below the stone bridge, looking
downstream along a lane where a Jewish family lives beside their house of prayer; a landing where a barge is being
loaded; the river sparkling in the morning sun; far down the road, the long wall of Caesar's gardens.

LIGHT. The sun is low, ahead and to the left, over the far bank (rome_tiber_model.SUN: 62 degrees left of straight
ahead, 22 up). So the river shines, the far bank stands against the light in its own soft haze, and everything that
faces us is in shade; the fronts of the two near houses, turned toward the bridge and the river, take the sun at a
slant; shadows fall toward us and to the right, long and soft.

THREE TONES. Light: the river, the sky low over the far bank, the sunlit house fronts. Middle: the far bank in its
haze, the lane, the blue sky. Dark: the barge's hull and its shadowed bales, the doorways, the faces of things turned
to us, the nearest corners.

THE PLACE (rome_tiber_model.py has every measurement). Left: the river, the far bank (the Aventine, its houses and
temples, the long warehouses downstream), the stone landing in front with steps down into the water, the barge moored
off the quay beyond it. Middle: the little square at the bridgehead, the well, the road running on south along the
river to the vanishing point, where Caesar's garden wall and its pines stand small and far. Right: the house of
prayer (plain, a broad door, a stone bench before it) and, nearest, Eleazar's house (its door with the little case
upright on the right-hand post, the open upper window with its shutter folded back, a line of washing between his two
upper windows, the hen yard in front with its wattle fence, a coop, a water dish and a fig tree in first leaf).

Nothing that moves by nature is painted (layout.json "fx"): the river's light and its rings, the hens, the washing,
the smoke of a cooking fire, the birds. People are not painted, but for a few dabs far off across the river. No
statue, picture or carving of any living thing anywhere on this lane, and no lettering.

  python3 rome_tiber.py          paints everything into out/rome-tiber/ (and out/rome-tiber-comp.png)
  python3 rome_tiber.py fast     skips the brush passes and the palette: out/rome-tiber-work/ only, to look at"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
import sky
import rome_tiber_model as M
from rome_tiber_kit import *
from rome_steps_kit import hash2
from rome_street_kit import wn
import rome_tiber_things as T
import rome_tiber_hens as HENS
import rome_tiber_layout as LAY

OUT = "out/rome-tiber"
WORK = "out/rome-tiber-work"
SKY_LIGHT = (-0.88, -0.48)                                   # toward the sun, in the picture (for the clouds)


# ================================================================ the backdrop, broad and soft
def far_waterline(x):
    """The row where the far shore meets the water, at picture column x."""
    Z = -M.FAR_BANK * M.F / np.maximum(M.VX - np.asarray(x, dtype=F32), 1e-3)
    return M.HZ + (M.EYE - M.WATER) * M.F / Z


def sky_layer(seed=11):
    x, y = PX, PY
    pic = sky.field(SHAPE, M.HZ, [(0.0, "#2766bd"), (0.32, "#3f86d2"), (0.60, "#78b2e2"), (0.84, "#c4dceb"), (1.0, "#f6ead0")], seed,
                    haze="#faeed6", patch=0.03)
    # toward the sun (out of the picture to the left, low) the sky is paler and warmer
    sun_glow = np.exp(-(((x + 260) / 520.0) ** 2 + ((y - 230) / 260.0) ** 2))
    glow(pic, "#fff2d0", (sun_glow * 0.55).astype(F32))
    sky.wisps(pic, M.HZ, seed + 3, "#fdf4e2", top=0.45, amount=0.45)
    # clouds: a heap over the far bank, lit from the left and from behind (bright rims, soft shaded bodies), a long
    # bank of fair-weather cloud low over the road, and a few small ones overhead
    sky.paint_clouds(pic, [(170, 160, 330, 118, 30), (-40, 128, 170, 80, 12)], seed + 22,
                     tones=("#86a2d6", "#bccee8", "#fbf3df", "#fffdf2"), light=SKY_LIGHT, ragged=13, reach=46.0)
    sky.paint_clouds(pic, [(520, 210, 360, 46, 16), (700, 176, 200, 40, 10)], seed + 31,
                     tones=("#93abd8", "#c8d4ea", "#f7efe0", "#fffcf2"), light=SKY_LIGHT, ragged=11, reach=32.0)
    return np.clip(pic, 0, 1).astype(F32)


def far_bank(seed=31):
    """Everything across the river, seen against the light through the morning haze: the Aventine with its houses and
    temples, the quays and warehouses along the shore, and far downstream the long warehouses. Painted on a clear
    sheet, in the picture's own measure: -> (color, coverage)."""
    rng = np.random.default_rng(seed)
    s = Sheet2(SHAPE)
    xs = np.arange(0, 401, 4, dtype=F32)
    wl = far_waterline(xs)

    def haze(c, t):
        """t: 0 near (the shore across) to 1 farthest: paler and bluer, the contrast going out of it."""
        return np.clip(lerp(col(c) * 0.86, col("#a9b4d2"), 0.22 + 0.58 * t), 0, 1)

    # ---- the hills beyond, very pale
    back = [(-10, 205), (40, 196), (90, 200), (150, 214), (210, 224), (270, 236), (330, 244), (400, 249)]
    s.poly(curve(back, 6) + [(400, 262), (-10, 262)], haze("#b4b4d0", 0.95))
    # ---- the Aventine: a long hill along the river, its face to us in shade, the light behind it
    crest = [(-10, 158), (30, 150), (80, 156), (130, 170), (175, 186), (215, 203), (250, 220), (285, 236), (320, 246), (360, 250)]
    hill = curve(crest, 8)
    s.poly(hill + [(360, 262), (-10, 272)], haze("#655f8e", 0.48))
    for i in range(9):                                        # the light comes over the crest: a thin glow along it
        s.line([(px, py - 0.6) for px, py in hill], haze("#ffe8c4", 0.5), 1.4 - i * 0.12, 0.10)
    for i in range(70):                                       # gardens and trees on its slopes: darker clumps
        px = rng.uniform(-5, 330)
        top = np.interp(px, [q[0] for q in hill], [q[1] for q in hill])
        py = rng.uniform(top + 3, top + 70)
        if py > np.interp(px, xs, wl) - 12:
            continue
        r = rng.uniform(2.0, 5.5) * (1.2 - px / 600)
        s.ellipse(px, py, r * 1.4, r * 0.8, haze(mix("#4e5a62", "#5c6656", rng.random()), 0.5), 0.75)
    for i in range(46):                                       # houses on the slope: a wall in shade, a roof whose edge catches the light
        px = rng.uniform(0, 300)
        top = np.interp(px, [q[0] for q in hill], [q[1] for q in hill])
        py = rng.uniform(top + 8, top + 64)
        if py > np.interp(px, xs, wl) - 10:
            continue
        w, hgt = rng.uniform(5, 12) * (1.1 - px / 700), rng.uniform(3, 7)
        t = 0.45 + 0.4 * px / 330
        s.poly([(px, py), (px + w, py), (px + w, py - hgt), (px, py - hgt)], haze(mix("#857c98", "#928496", rng.random()), t))
        s.poly([(px - 0.8, py - hgt), (px + w + 0.8, py - hgt), (px + w * 0.45, py - hgt - 2.2)], haze("#a87a74", t))
        s.line([(px - 0.8, py - hgt - 0.2), (px + w * 0.45, py - hgt - 2.3)], haze("#f6dcbc", t * 0.6), 0.7, 0.6)        # the rim of light
        if rng.random() < 0.5:
            s.poly([(px + w * 0.3, py), (px + w * 0.45, py), (px + w * 0.45, py - hgt * 0.5), (px + w * 0.3, py - hgt * 0.5)], haze("#6a5e7a", t), 0.8)

    def temple(cx, base, w, hgt, t, cols=6):
        """A temple on the crest, its front to us in shade, the light along its roof and the edges of its columns."""
        s.poly([(cx - w * 0.56, base), (cx + w * 0.56, base), (cx + w * 0.56, base - hgt * 0.16), (cx - w * 0.56, base - hgt * 0.16)], haze("#b8a8b6", t))
        s.poly([(cx - w * 0.5, base - hgt * 0.16), (cx + w * 0.5, base - hgt * 0.16), (cx + w * 0.5, base - hgt * 0.82), (cx - w * 0.5, base - hgt * 0.82)], haze("#7c7096", t))
        for j in range(cols):
            c = cx - w * 0.44 + w * 0.88 * j / (cols - 1)
            s.line([(c, base - hgt * 0.17), (c, base - hgt * 0.81)], haze("#c9bccc", t), max(1.0, w * 0.06))
            s.line([(c - w * 0.02, base - hgt * 0.17), (c - w * 0.02, base - hgt * 0.81)], haze("#fff0d6", t), 0.7, 0.7)
        s.poly([(cx - w * 0.54, base - hgt * 0.82), (cx + w * 0.54, base - hgt * 0.82), (cx + w * 0.54, base - hgt * 0.9), (cx - w * 0.54, base - hgt * 0.9)], haze("#c4b4c0", t))
        s.poly([(cx - w * 0.56, base - hgt * 0.9), (cx + w * 0.56, base - hgt * 0.9), (cx, base - hgt * 1.18)], haze("#9c8ca8", t))
        s.line([(cx - w * 0.58, base - hgt * 0.9), (cx, base - hgt * 1.19), (cx + w * 0.58, base - hgt * 0.9)], haze("#ffe2b8", t * 0.7), 1.0, 0.9)

    temple(52, 166, 30, 22, 0.42)
    temple(150, 182, 18, 14, 0.5, cols=4)

    def pine(px, py, hgt, t):
        s.line([(px, py), (px + hgt * 0.05, py - hgt * 0.55), (px - hgt * 0.02, py - hgt)], haze("#5a5060", t), max(0.8, hgt * 0.05))
        for (dx, dy, rx, ry, tone) in ((-0.22, -1.02, 0.36, 0.14, "#4c5a5a"), (0.2, -1.06, 0.36, 0.15, "#56645c"), (0.0, -1.12, 0.3, 0.12, "#68725e")):
            s.ellipse(px + dx * hgt, py + dy * hgt, rx * hgt, ry * hgt, haze(tone, t))
        s.line([(px - hgt * 0.36, py - hgt * 1.13), (px + hgt * 0.2, py - hgt * 1.21)], haze("#ffe0b0", t * 0.6), 0.8, 0.8)

    def cypress(px, py, hgt, t):
        s.poly([(px - hgt * 0.1, py), (px - hgt * 0.12, py - hgt * 0.5), (px, py - hgt), (px + hgt * 0.12, py - hgt * 0.5), (px + hgt * 0.1, py)], haze("#465450", t))
        s.line([(px - hgt * 0.11, py - hgt * 0.45), (px - hgt * 0.01, py - hgt * 0.98)], haze("#c8c0a0", t * 0.7), 0.8, 0.7)

    for (px, py, hgt) in ((8, 158, 16), (92, 160, 14), (112, 166, 17), (196, 196, 12), (232, 212, 10)):
        pine(px, py, hgt, 0.45)
    for (px, py, hgt) in ((72, 158, 14), (78, 159, 11), (126, 170, 13), (178, 188, 10), (262, 224, 9), (268, 226, 7)):
        cypress(px, py, hgt, 0.45)

    # ---- the shore: quay walls, warehouses with dark arches, steps down to the water, boats moored
    def wl_at(px):
        return float(np.interp(px, xs, wl))

    x = -6.0
    while x < 330:
        w = rng.uniform(16, 34) * (1.15 - x / 520)
        y0 = wl_at(x + w / 2) - 1.0
        hgt = rng.uniform(7, 13) * (1.2 - x / 480)
        t = 0.2 + 0.6 * max(x, 0) / 330
        s.poly([(x, y0 + 1), (x + w, y0 + 1), (x + w, y0 - hgt), (x, y0 - hgt)], haze(mix("#9a8ca4", "#a8949a", rng.random()), t))
        s.poly([(x - 0.5, y0 - hgt), (x + w + 0.5, y0 - hgt), (x + w + 0.5, y0 - hgt - 2.2), (x - 0.5, y0 - hgt - 2.2)], haze("#a07068", t))
        s.line([(x - 0.5, y0 - hgt - 2.2), (x + w + 0.5, y0 - hgt - 2.2)], haze("#ffe4bc", t * 0.6), 0.8, 0.8)
        n = max(1, int(w / 6))
        for j in range(n):                                    # arches into the warehouses
            ax = x + (j + 0.5) * w / n
            aw = w / n * 0.32
            s.poly([(ax - aw, y0), (ax - aw, y0 - hgt * 0.45), (ax, y0 - hgt * 0.6), (ax + aw, y0 - hgt * 0.45), (ax + aw, y0)], haze("#4a3e58", t), 0.9)
        x += w + rng.uniform(0, 5)
    for (bx, blen) in ((22, 26), (96, 20), (176, 15), (238, 11)):      # boats moored along the far quay
        y0 = wl_at(bx) + 0.6
        s.poly([(bx, y0), (bx + blen, y0), (bx + blen * 1.08, y0 - 2.6), (bx - blen * 0.05, y0 - 2.4)], haze("#3c3448", 0.25 + bx / 600))
        s.line([(bx + blen * 0.4, y0 - 2.4), (bx + blen * 0.42, y0 - 2.4 - blen * 0.5)], haze("#3c3448", 0.3 + bx / 600), 0.7, 0.8)
    for i in range(16):                                       # people on the far quays: dabs
        px = rng.uniform(4, 300)
        y0 = wl_at(px) - 1.0
        hgt = rng.uniform(2.6, 3.6) * (1.15 - px / 500)
        tone = ["#f2e8d6", "#c8553a", "#7d94b8", "#e8d2a8", "#8a6a4e"][i % 5]
        s.line([(px, y0), (px, y0 - hgt)], haze(tone, 0.3), max(0.9, hgt * 0.36), 0.95)
        s.ellipse(px, y0 - hgt - 0.5, 0.6, 0.6, haze("#6a4a3e", 0.3), 0.9)

    # ---- far downstream: the long warehouses on the plain, their many small roofs in a row
    x = 268.0
    while x < 372:
        w = rng.uniform(3, 6) * (1.4 - x / 400)
        y0 = wl_at(x + w / 2) - 0.6
        hgt = 4.2 * (1.25 - x / 420)
        s.poly([(x, y0), (x + w, y0), (x + w, y0 - hgt), (x, y0 - hgt)], haze("#b4a6b4", 0.85))
        s.poly([(x, y0 - hgt), (x + w, y0 - hgt), (x + w * 0.5, y0 - hgt - 1.6)], haze("#c09a90", 0.85))
        s.line([(x, y0 - hgt), (x + w * 0.5, y0 - hgt - 1.6)], haze("#fff0d0", 0.85), 0.6, 0.7)
        x += w
    return s.done()


def river(base, seed=41):
    """The river's face (y = WATER), per pixel: the Tiber's own brown-green in the near water, the sky and the far bank
    mirrored in it farther off, broken by the current into level streaks, and bright where the sun strikes it. ->
    (color, mask of where the water is seen, the water's own place: x, z, k)."""
    x, z, k, ok = level(M.WATER)
    wet = ok & (x < M.Q) & (x > M.FAR_BANK) & (PY > M.HZ + 0.5)
    # the current's surface: long low swells across it, small choppy wavelets on them
    sw = wn(x * 0.35, z * 1.6, 380, seed, 3) - 0.5
    chop = wn(x * 0.8, z * 2.8, 70, seed + 1, 4) - 0.5
    fine = wn(x * 1.2, z * 4.0, 18, seed + 2, 2) - 0.5
    seen = np.clip(k / 0.12, 0, 1)
    slope = (sw * 0.9 + chop * 0.8 + fine * 0.45 * seen)                 # how the wave tips the mirror: up (+) or down
    # the mirror: what lies above, reflected about the far shore, pushed about by the waves and drawn down in streaks
    wl = far_waterline(PX)
    src_y = np.clip(2 * wl - PY - slope * (8 + 40 * k), 0, M.H - 1)
    src_x = np.clip(PX + chop * 12 * k, 0, M.W - 1)
    smear = blur(base, 2.2)
    mirror = sample(smear, src_x, src_y)
    for dy in (3, 6, 10):                                    # a rough river draws its reflections down
        mirror = mirror * 0.7 + sample(smear, src_x, np.clip(src_y - dy * (0.4 + k), 0, M.H - 1)) * 0.3
    # the river's own color: brown and in a hurry, greener in the deep water
    body = np.empty(SHAPE + (3,), dtype=F32)
    body[...] = col("#86734a")
    body *= (1 + (wn(x, z, 600, seed + 3, 3) - 0.5) * 0.16 + chop * 0.10)[..., None]
    body = lerp(body, col("#717650"), (np.clip((wn(x * 0.5, z, 900, seed + 4, 3) - 0.35) * 2, 0, 1) * 0.5)[..., None])
    # how much of the sky it gives back: little looking down into the near water, most of it far off
    dep = (PY - M.HZ) / M.F
    fres = np.clip(0.22 + 0.74 * np.exp(-dep / 0.085), 0, 1) * (0.80 + 0.40 * np.clip(slope + 0.3, 0, 1))
    c = lerp(body, mirror * np.array([0.90, 0.92, 0.96], dtype=F32), np.clip(fres, 0, 0.96)[..., None])
    # the troughs between the wavelets are darker, the crests catch the light
    c = c * (1 + np.clip(slope, -0.6, 0.6)[..., None] * (0.16 + 0.24 * seen)[..., None])
    # the sun on it: a broad shine in the far water under the bright sky, and the glitter away to the left, toward the sun
    shine = np.exp(-((PY - (far_waterline(PX) + 6)) / 18.0) ** 2) * np.exp(-((PX - 120) / 280.0) ** 2)
    left = np.exp(-((PX + 40) / 230.0) ** 2) * np.clip((PY - 268) / 90.0, 0, 1) * np.clip((520 - PY) / 120.0, 0, 1)
    glare = np.clip(left * (0.55 + 0.45 * np.clip(slope + 0.4, 0, 1)), 0, 1)              # the sun's glare on the choppy water
    c = lerp(c, col("#f4e2b4"), (glare * 0.62)[..., None])
    toward = np.clip(shine * 1.1 + left * 0.9, 0, 1.3)
    spark_n = wn(x * 0.9, z * 3.2, 9, seed + 5, 2) * 0.55 + (chop + 0.5) * 0.45
    spark = step(0.80 - 0.16 * toward, 0.85 - 0.16 * toward, spark_n) * np.clip(toward + 0.08, 0, 1.2)
    c = 1 - (1 - c) * (1 - col("#ffe6b4") * (shine * 0.55 + left * 0.25)[..., None])
    c = lerp(c, col("#fff7e2"), np.clip(spark * 0.95, 0, 1)[..., None])
    # the barge: its own dark hull mirrored under it, and the water between it and the quay in its shadow
    Bg = M.BARGE
    zrel = np.clip((z - Bg["z0"]) / (Bg["z1"] - Bg["z0"]), 0, 1)
    under_hull = band(z, Bg["z0"] - 40, Bg["z1"] + 60, 30.0) * band(x, Bg["xp"] - 20, Bg["xs"] + 120, 20.0)
    gap = band(z, Bg["z0"], Bg["z1"], 30.0) * band(x, Bg["xs"], M.Q, 12.0)
    broken = 0.75 + 0.5 * np.clip(chop + 0.5, 0, 1)
    c = lerp(c, col("#3a3236"), np.clip(under_hull * 0.62 * broken, 0, 0.8)[..., None])
    c = lerp(c, col("#4c463e"), np.clip(gap * 0.45 * broken, 0, 0.6)[..., None])
    return np.clip(c, 0, 1).astype(F32), wet.astype(F32), (x, z, k)


info_paved = [None]


def ground(seed=51):
    """The lane, the little square and the landing (y = 0): beaten earth with old paving along the quay and on the
    landing, worn pale where everyone walks off the bridge. -> (local color, mask, x, z, k)."""
    x, z, k, ok = level(0.0)
    L = M.LANDING
    on_land = (x >= L["x0"]) & (x <= L["x1"]) & (z >= L["z0"]) & (z <= L["z1"])
    lane = ok & (x >= M.Q) & (PY > M.HZ + 0.5)
    mask = lane | (ok & on_land)
    c = earth(x, z, k, seed)
    # the path everyone takes off the bridge and down the road: paler, packed
    path = np.exp(-(((x - (-120 + z * 0.02)) / (260 + 0.05 * np.maximum(z, 0))) ** 2))
    c = c * (1 + 0.08 * path[..., None])
    # the quay: big old flags along its edge (3 m wide), and the landing all of stone
    quay = (x < M.Q + 300) | on_land
    from rome_steps_kit import courses
    tone, jm, _ = courses(z, x, long=118.0, high=74.0, seed=seed + 6, joint=1.6, ppc=k, vary_len=0.4)
    e, r1, r2, _ = cells(x * 0.9 + (wn(x, z, 120, seed + 5, 2) - 0.5) * 20, z * 0.75, 62.0, seed + 6)
    slab = col("#c6bca6")[None, None, :] * (0.86 + 0.22 * tone[..., None]) * (1 + (wn(x, z, 90, seed + 8, 3) - 0.5)[..., None] * 0.12)
    seen = np.clip(k / 0.3, 0, 1)
    joint = jm * np.clip(seen * 1.4, 0, 1)
    slab = slab * (1 - 0.40 * joint[..., None]) + col("#6e6058") * 0.40 * joint[..., None]
    coping = band(x, M.Q, M.Q + 42.0, 1.0 / np.maximum(k, 1e-3)) * (~on_land) * ((z > M.LANDING["z1"]) | (z < M.LANDING["z0"]))    # the quay's edge: long coping stones
    slab = lerp(slab, col("#d4cab4")[None, None, :] * (0.9 + 0.16 * hash2(np.floor(z / 150.0), 3, seed)[..., None]), coping[..., None])
    worn = np.clip(1 - (x - M.Q) / 300.0, 0, 1) * (~on_land) + on_land * 1.0
    edge_fade = step(0.15, 0.6, wn(x, z, 70, seed + 7, 3) + worn * 0.6)       # the flags give way to earth unevenly
    c = lerp(c, slab, (quay * edge_fade * np.clip(worn * 1.6, 0, 1))[..., None])
    # the square at the bridgehead: many-sided basalt stones, fitted close and worn round, giving way to the earth
    e2, s1, s2, mid = cells(x * 0.95 + (wn(x, z, 140, seed + 11, 3) - 0.5) * 26, z * 0.86 + (wn(x, z, 140, seed + 12, 3) - 0.5) * 26, 58.0, seed + 13)
    foot = np.maximum(1.0 / np.maximum(k, 1e-3) * 0.55, 1.2)
    seen2 = np.clip(k / 0.22, 0, 1)
    j2 = np.clip((1.2 + s2 * 1.2 - e2) / foot + 0.5, 0, 1) * seen2
    basalt = col("#a49c98")[None, None, :] * (0.88 + 0.18 * s1[..., None] ** 1.2)
    basalt = lerp(basalt, c, 0.35)                                   # dust over it all
    warm = (s2 - 0.5) * 0.05
    basalt[..., 0] += warm
    basalt[..., 2] -= warm * 0.8
    crown = np.clip(e2 / 22.0, 0, 1) ** 0.7 * np.clip(1.2 - mid / 60.0, 0, 1) * seen2
    basalt = basalt * (1 + 0.08 * crown[..., None])
    basalt = basalt * (1 - 0.32 * j2[..., None]) + col("#7a6a5e") * 0.32 * j2[..., None]
    fu, fv = in_frame(FE, x, z)
    by_walls = np.clip((-fv - 40.0) / 80.0, 0, 1)                    # a strip of earth along the foot of the houses
    paved = lane & (x > M.Q + 280) & (z < 1500)
    edge = step(0.20, 0.75, wn(x, z, 90, seed + 14, 3) * 0.6 + np.clip((1500 - z) / 600.0, 0, 1) * 0.5 + np.clip((x - M.Q - 280) / 220.0, 0, 1) * 0.3)
    c = lerp(c, basalt, (paved * edge * by_walls)[..., None])
    info_paved[0] = (paved * edge * by_walls).astype(F32)
    return np.clip(c, 0, 1).astype(F32), mask.astype(F32), x, z, k, on_land


# ================================================================ the houses
FE = frame_of(M.FRONT0, M.D)                                 # the two near houses: u along their front (= s), v back into them
FR = frame_of((M.ROAD_X, 0.0), (0.0, 1.0))                   # the houses along the road: u = z, v back from their fronts (x)
P_OUT = -20.0                                                # the house of prayer stands 20 cm proud of Eleazar's house
E_EAVE, E_OVER, E_PITCH, E_RIDGE = 600.0, 46.0, 24.0, 440.0  # Eleazar's eave (the underside of its rafters), overhang, roof
P_EAVE, P_OVER, P_PITCH, P_RIDGE = 550.0, 40.0, 20.0, 540.0
FASCIA = 16.0                                                # the eave's edge: the tile ends over the rafters
ROAD_HOUSES = [  # along the road beyond: (from z, to z, eave, plaster): a tall house, then lower ones, then garden walls
    (1453.0, 2350.0, 600.0, "#e7c391"), (2350.0, 3300.0, 560.0, "#dcae80"), (3300.0, 4300.0, 420.0, "#efd9b4"),
    (4300.0, 6200.0, 300.0, "#e2cfae")]


def front_solids():
    """What throws shadows on the two near fronts, in their frame (u, v, h)."""
    e0, e1 = M.EL["s0"], M.EL["s1"]
    p0, p1 = M.PR["s0"], M.PR["s1"]
    w = M.WINDOW
    b = M.BENCH
    return [("box", e0 - 100, e1, -E_OVER, 0, E_EAVE, E_EAVE + FASCIA + 30),          # Eleazar's eave
            ("box", p0, p1, P_OUT, 0, 0, M.PR["eave"]),                              # the house of prayer, standing proud
            ("box", p0, p1 + 200, P_OUT - P_OVER, 0, P_EAVE, P_EAVE + FASCIA + 26),  # its eave
            ("box", w["s0"] - 98, w["s0"] - 2, -5, 0, w["sill"] - 2, w["top"] + 2),  # the shutter, folded back against the wall
            ("box", b["s0"], b["s1"], -b["out"] - b["deep"] / 2, -b["out"] + b["deep"] / 2, 0, b["h"]),    # the bench
            ("box", M.DOOR_E["s0"] - 12, M.DOOR_E["s1"] + 12, -14, 0, M.DOOR_E["h"], M.DOOR_E["h"] + 18)]  # the beam over his door


def lit_wall(own, face, cut, deep=0.0, bounce=0.35):
    return LIGHT.on(own, face, cut, up=0, deep=deep, bounce=bounce + 0.35 * cut)


def road_houses(pic, info, seed=71):
    """The houses along the road on its right, beyond the house of prayer: their fronts face the river and take the
    sun full; we see them sharply foreshortened, running away to the vanishing point, their eaves and roofs."""
    u, h, Z, k, ok = plane_at(FR, 0.0)
    su = soft_edges(u)
    for i, (z0, z1, eave, tone) in enumerate(ROAD_HOUSES):
        m = band(u, z0, z1, su) * band(h, 0.0, eave, 1.0 / k) * ok
        own = plaster(u, h, tone, seed + i * 7, 0.08, 0.05, mend=0.12)
        own = own * (1 - 0.18 * band(h, 0, 55, 1 / k)[..., None])                    # its foot, darker
        doors = band((u - z0) % 260.0, 90.0, 190.0, su) * band(h, 0, 210, 1 / k)     # doors and shop openings, dark
        wins = band((u - z0 + 60) % 230.0, 80.0, 150.0, su) * band(h, 380, 470, 1 / k) * (h < eave - 60)
        own = lerp(own, col("#4a3c4c"), (np.maximum(doors, wins) * 0.85)[..., None])
        c = lit_wall(own, FACE_ROAD, 0.0, bounce=0.3)
        c = far(c, Z - M.Z0, "#d6d6e2", 9000.0, 0.75)
        over(pic, c, m.astype(F32))
        # its roof, rising back from the eave over the road
        ru, rv, rh, rZ, rk, rok = roof_at(FR, eave + FASCIA, -38.0, 22.0)
        rm = band(ru, z0, z1, soft_edges(ru)) * band(rv, -38.0, 330.0, soft_edges(rv)) * rok
        tc, cover = tiles(ru, (rv + 38.0) / math.cos(math.radians(22)), rk, seed + i, "#c76a42")
        tc = LIGHT.on(tc, 0.45, 0.0, up=0.6, bounce=0.2)
        over(pic, far(tc, rZ - M.Z0, "#d6d6e2", 9000.0, 0.75), rm.astype(F32))
        # the eave's edge and the dark under it
        em = band(u, z0, z1, su) * band(h, eave, eave + FASCIA, 1 / k) * ok
        over(pic, far(col("#6a4a44"), Z - M.Z0, "#d6d6e2", 9000.0, 0.7), (em * 0.9).astype(F32))
    return pic


def road_gables(pic, info, seed=73):
    """The ends of the road's houses toward us, rising one behind another over the house of prayer: under the eave a
    plastered wall in shade, over it the hipped end of the roof, its tiles toward us. Painted far first, so that the
    nearer hide the farther."""
    for i, (z0, z1, eave, tone) in reversed(list(enumerate(ROAD_HOUSES))):
        depth = 900.0
        if eave <= 320:
            continue                                          # garden walls: no roof
        x1 = M.ROAD_X + depth
        fr = frame_of((x1 + 38.0, z0), (-1.0, 0.0))           # its north end: u from the far corner toward the road, v back (+z)
        s_, h, Z, k, ok = plane_at(fr, 0.0)
        m = band(s_, 38.0, depth + 38.0, soft_edges(s_)) * band(h, 0.0, eave, 1 / k) * ok
        own = plaster(s_, h, tone, seed + i * 5, 0.07, 0.05)
        c = LIGHT.on(own, FACE_US, 0.0, deep=0.05, bounce=0.5)
        over(pic, far(c, Z - M.Z0, "#d6d6e2", 9000.0, 0.75), m.astype(F32))
        ru, rv, rh, rZ, rk, rok = roof_at(fr, eave + FASCIA, -38.0, 22.0)
        rise = depth / 2 + 38.0
        half = np.clip(rise - (rv + 38.0), 0, None)          # the hip narrows as it rises to the ridge
        mid = depth / 2 + 38.0
        rm = band(ru, mid - half, mid + half, soft_edges(ru)) * band(rv, -38.0, rise - 38.0, soft_edges(rv)) * rok
        tc, cover = tiles(ru, (rv + 38.0) / math.cos(math.radians(22)), rk, seed + i + 40, "#c06a44")
        face_hip = math.cos(math.radians(22)) * M.SUN[1] - math.sin(math.radians(22)) * M.SUN[2]
        tc = LIGHT.on(tc, max(0.0, face_hip), 0.0, up=0.6, bounce=0.25)
        over(pic, far(tc, rZ - M.Z0, "#d6d6e2", 9000.0, 0.75), rm.astype(F32))
        em = band(s_, 0.0, depth + 76.0, soft_edges(s_)) * band(h, eave, eave + FASCIA, 1 / k) * ok
        over(pic, far(col("#6a4a44"), Z - M.Z0, "#d6d6e2", 9000.0, 0.7), (em * 0.9).astype(F32))
        win = band(s_, 250.0, 300.0, soft_edges(s_)) * band(h, eave - 150, eave - 95, 1 / k) + band(s_, 560.0, 600.0, soft_edges(s_)) * band(h, eave - 150, eave - 100, 1 / k)
        over(pic, far(col("#4c3e48"), Z - M.Z0, "#d6d6e2", 9000.0, 0.7), (np.clip(win, 0, 1) * m * 0.9).astype(F32))
    return pic


def gardens(pic, seed=81):
    """Far off where the river and the road lead: below the Aventine the Tiber bends away to the right, and across the
    end of the reach the right bank comes into view with the long wall of Caesar's gardens along it, a gateway in it,
    and the dark heads of umbrella pines and the spires of cypresses over it. Small, and pale with distance."""
    rng = np.random.default_rng(seed)
    s = Sheet2(SHAPE)
    t = 0.62
    hz = lambda c, tt=t: np.clip(lerp(col(c), col("#cfd4e2"), tt), 0, 1)
    wl = lambda x_: float(far_waterline(np.asarray([x_]))[0])
    # the bank across the end of the reach: low ground, then the wall along it, turning toward us on the right
    x0, x1 = 300.0, 440.0
    yb = lambda x_: 252.0 + (x_ - 300.0) * 0.012            # the foot of the wall
    hw = lambda x_: 6.0 + (x_ - 300.0) * 0.03                # its height, nearer (taller) toward the road
    s.poly([(x0 - 8, 253.5), (x1, yb(x1) + 1.5), (x1, 262), (x0 - 8, 262)], hz("#9a9a7c", 0.55))
    for i in range(22):                                       # the trees, behind the wall: pines and cypresses
        xx = rng.uniform(x0 + 20, x1)
        base = yb(xx) - hw(xx) * 0.6
        if rng.random() < 0.62:
            hgt = rng.uniform(20, 32) * (0.8 + (xx - 300) / 400)
            s.line([(xx, base), (xx + hgt * 0.05, base - hgt * 0.7)], hz("#4a4040"), max(0.7, hgt * 0.035))
            for (dx, dy, rx, ry, tone) in ((-0.2, -0.80, 0.36, 0.13, "#2e4436"), (0.18, -0.84, 0.34, 0.14, "#3a5040"), (0.0, -0.9, 0.3, 0.11, "#4a5e48")):
                s.ellipse(xx + dx * hgt, base + dy * hgt, rx * hgt, ry * hgt, hz(tone))
            s.line([(xx - 0.32 * hgt, base - 0.92 * hgt), (xx + 0.14 * hgt, base - 0.97 * hgt)], hz("#f2dcb0", 0.45), 0.7, 0.8)
        else:
            hgt = rng.uniform(19, 29) * (0.8 + (xx - 300) / 400)
            s.poly([(xx - hgt * 0.08, base), (xx - hgt * 0.1, base - hgt * 0.5), (xx, base - hgt), (xx + hgt * 0.1, base - hgt * 0.5), (xx + hgt * 0.08, base)], hz("#2c3e36"))
            s.line([(xx - hgt * 0.09, base - hgt * 0.45), (xx - hgt * 0.01, base - hgt * 0.95)], hz("#e4d4a8", 0.5), 0.7, 0.8)
    wall_ = [(x0, yb(x0)), (x1, yb(x1)), (x1, yb(x1) - hw(x1)), (x0, yb(x0) - hw(x0))]
    s.poly(wall_, hz("#e8d6b8", 0.5))
    s.line([(x0, yb(x0) - hw(x0)), (x1, yb(x1) - hw(x1))], hz("#fff0d4", 0.4), 0.9)
    s.line([(x0, yb(x0)), (x1, yb(x1))], hz("#9a8a8a", 0.5), 0.7, 0.8)
    gx = 362.0                                               # the gateway: two piers, the dark of the opening
    s.poly([(gx - 4, yb(gx)), (gx + 4, yb(gx + 4)), (gx + 4, yb(gx + 4) - hw(gx) * 0.8), (gx - 4, yb(gx) - hw(gx) * 0.8)], hz("#5a4c5a", 0.4))
    for px_ in (gx - 6, gx + 6):
        s.poly([(px_ - 1.4, yb(px_) + 0.3), (px_ + 1.4, yb(px_) + 0.3), (px_ + 1.4, yb(px_) - hw(px_) * 1.3), (px_ - 1.4, yb(px_) - hw(px_) * 1.3)], hz("#f4e6c8", 0.4))
    s.onto(pic)
    return s.done()


def near_fronts(pic, info, seed=61):
    """The house of prayer and Eleazar's house: their roofs, eaves and fronts, lit at a slant."""
    e0, e1 = M.EL["s0"], M.EL["s1"]
    p0, p1 = M.PR["s0"], M.PR["s1"]
    sol = front_solids()

    # ---- the house of prayer's roof, then its front and the edge it shows where it stands proud of Eleazar's house
    ru, rv, rh, rZ, rk, rok = roof_at(FE, P_EAVE + FASCIA, P_OUT - P_OVER, P_PITCH)
    hip = ru + (rv - (P_OUT - P_OVER)) - (p1 + P_OVER)                               # its far end is hipped: the roof slopes down to it
    rm = band(ru, p0, p1 + 400, soft_edges(ru)) * np.clip(-hip / soft_edges(ru) + 0.5, 0, 1) * band(rv, P_OUT - P_OVER, P_RIDGE, soft_edges(rv)) * rok
    tc, cover = tiles(ru, (rv - (P_OUT - P_OVER)) / math.cos(math.radians(P_PITCH)), rk, seed + 1, "#c06640")
    face_roof = -math.sin(math.radians(P_PITCH)) * sun_in(FE)[1] + math.cos(math.radians(P_PITCH)) * sun_in(FE)[2]
    tc = LIGHT.on(tc, face_roof, 0.0, up=0.7, bounce=0.15)
    over(pic, far(tc, rZ - M.Z0, "#dcd8e0", 9000.0, 0.7), rm.astype(F32))
    info["roof_p"] = rm

    u, h, Z, k, ok = plane_at(FE, P_OUT)
    su = soft_edges(u)
    m = band(u, p0, p1, su) * band(h, 0.0, P_EAVE, 1 / k) * ok
    x, y, z = from_frame(FE, u, P_OUT, h)
    cut = shade_in(FE, x, h, z, sol)
    own = plaster(u, h, "#ebdfc8", seed + 2, 0.06, 0.04, mend=0.10)
    socle = band(h, 0, 72, 1 / k)                                                   # a plinth of squared travertine
    st, sj = tufa_blocks(u, h, k, seed + 3, "#d6cbb2", 92.0, 36.0)
    own = lerp(own, st, socle[..., None])
    own = own * (1 - 0.10 * np.clip(1 - (h - 72) / 60.0, 0, 1)[..., None] * (h > 72)[..., None])   # splashes over it
    c = lit_wall(own, FACE_FRONT, cut, bounce=0.40)
    over(pic, c, m.astype(F32))
    info.update(p_u=u, p_h=h, p_m=m, p_cut=cut, p_k=k)
    # its edge, where it stands proud of Eleazar's house: square to the front, toward us, in shade
    v, hh, Zs, ks, oks = side_at(FE, p0)
    ms = band(v, P_OUT, 0.0, soft_edges(v)) * band(hh, 0, P_EAVE, 1 / ks) * oks
    over(pic, LIGHT.on(plaster(v * 3, hh, "#ebdfc8", seed + 4, 0.05, 0.04), 0.0, 0.0, deep=0.05, bounce=0.5), ms.astype(F32))

    # ---- Eleazar's roof, its eave, its front
    ru, rv, rh, rZ, rk, rok = roof_at(FE, E_EAVE + FASCIA, -E_OVER, E_PITCH)
    rm = band(ru, e0 - 200, e1, soft_edges(ru)) * band(rv, -E_OVER, E_RIDGE, soft_edges(rv)) * rok
    tc, cover = tiles(ru, (rv + E_OVER) / math.cos(math.radians(E_PITCH)), rk, seed + 5, "#c8653c")
    face_roof = -math.sin(math.radians(E_PITCH)) * sun_in(FE)[1] + math.cos(math.radians(E_PITCH)) * sun_in(FE)[2]
    old = (wn(ru, rv, 180, seed + 6, 3) - 0.5)                                       # lichen and old tiles: darker, browner
    tc = tc * (1 + old[..., None] * 0.22) * np.array([1.0, 0.98, 0.94], dtype=F32)
    tc = LIGHT.on(tc, face_roof, 0.0, up=0.7, bounce=0.15)
    over(pic, tc, rm.astype(F32))
    info["roof_e"] = rm
    # the underside of the eave: rafters' ends in shade, the warm light thrown up from the sunlit lane on them
    lu, lv, lZ, lk, lok = level_in(FE, E_EAVE)
    sm = band(lu, e0 - 200, e1, soft_edges(lu)) * band(lv, -E_OVER, 0.0, soft_edges(lv)) * lok
    raft = band(lu % 55.0, 0.0, 9.0, soft_edges(lu))
    soffit = lerp(col("#8a6a52"), col("#5a4038"), raft[..., None])
    over(pic, LIGHT.on(soffit, 0.0, 0.0, up=-1, deep=0.25, bounce=0.9), sm.astype(F32))
    # the eave's edge: the ends of the cover tiles over the rafters, catching the light
    fu, fh, fZ, fk, fok = plane_at(FE, -E_OVER)
    fm = band(fu, e0 - 200, e1, soft_edges(fu)) * band(fh, E_EAVE, E_EAVE + FASCIA, 1 / fk) * fok
    ends = band((fu % 40.0), 12.0, 28.0, soft_edges(fu))
    fc = lerp(col("#9c4a30"), col("#d27850"), ends[..., None])
    over(pic, LIGHT.on(fc, FACE_FRONT, 0.0, bounce=0.3), fm.astype(F32))

    u, h, Z, k, ok = plane_at(FE, 0.0)
    su = soft_edges(u)
    m = band(u, e0, e1, su) * band(h, 0.0, E_EAVE, 1 / k) * ok
    x, y, z = from_frame(FE, u, 0.0, h)
    cut = shade_in(FE, x, h, z, sol)
    own = plaster(u, h, "#e0b47a", seed + 7, 0.10, 0.06, mend=0.18)
    # the plaster has come off here and there, low down most: squared tufa under it
    gone = bare(u, h, seed + 8, much=0.12 + 0.30 * np.clip(1 - h / 260.0, 0, 1), cell=110.0)
    st, sj = tufa_blocks(u, h, k, seed + 9, "#a8805c", 58.0, 29.0)
    lip = np.clip(bare(u + 2.0, h - 2.0, seed + 8, much=0.12 + 0.30 * np.clip(1 - h / 260.0, 0, 1), cell=110.0) - gone, 0, 1)
    own = lerp(own, st, gone[..., None])
    own = own * (1 - 0.30 * lip[..., None])
    damp = np.clip(1 - h / 70.0, 0, 1) * (0.5 + wn(u, h, 40, seed + 10, 3))                 # rising damp and the splash of the lane
    own = own * (1 - 0.24 * np.clip(damp, 0, 1)[..., None] * np.array([1.0, 0.92, 0.92], dtype=F32))
    under_sill = np.exp(-((u - (M.WINDOW["s0"] + M.WINDOW["s1"]) / 2) / 60.0) ** 2) * np.clip((M.WINDOW["sill"] - h) / 140.0, 0, 1) * (h < M.WINDOW["sill"])
    own = own * (1 - 0.10 * under_sill[..., None] * np.clip(wn(u * 4, h, 60, seed + 11, 3) * 1.6 - 0.3, 0, 1)[..., None])   # rain from the sill
    c = lit_wall(own, FACE_FRONT, cut, bounce=0.40)
    over(pic, c, m.astype(F32))
    info.update(e_u=u, e_h=h, e_m=m, e_cut=cut, e_k=k, e_Z=Z)
    return pic


def openings(pic, info, seed=91):
    """What shows through the openings of the two fronts: Eleazar's upper room through the open window (dim and plain:
    what is seen when he has gone down), the jambs and the lintels of the openings, his open door and the dark inside,
    his small window with its wooden grille, the broad closed door of the house of prayer and its two small windows."""
    W_ = M.WINDOW
    wall_t = 45.0
    u, h, k = info["e_u"], info["e_h"], info["e_k"]
    su = soft_edges(u)
    hole = band(u, W_["s0"], W_["s1"], su) * band(h, W_["sill"], W_["top"], 1 / k) * info["e_m"]
    # through the window: the room's back wall (we look up into it), dim and plain, a beam across, the far jamb's reveal
    bu, bh, bZ, bk, bok = plane_at(FE, wall_t + 360.0)
    room = col("#5a4644")[None, None, :] * (0.90 + 0.18 * wn(bu, bh, 60, seed, 3)[..., None])
    room = lerp(room, col("#4a3a3c"), (band(bh, 548, 566, 1 / bk) * 0.9)[..., None])           # the beam that carries the floor above
    room = lerp(room, col("#6e5850"), (np.clip((bh - 420) / 120, 0, 1) * 0.3)[..., None])
    jv, jh, jZ, jk, jok = side_at(FE, W_["s1"])                                                  # the far jamb's reveal, toward us
    jamb = band(jv, 0.0, wall_t, soft_edges(jv)) * band(jh, W_["sill"], W_["top"], 1 / jk) * jok
    inside = room
    inside = lerp(inside, LIGHT.on(col("#c9a278"), 0.0, 0.0, deep=0.1, bounce=0.45), jamb[..., None])
    lu, lv, lZ, lk, lok = level_in(FE, W_["top"])                                                # the lintel's underside
    lint = band(lu, W_["s0"], W_["s1"], soft_edges(lu)) * band(lv, 0.0, wall_t, soft_edges(lv)) * lok
    inside = lerp(inside, LIGHT.on(col("#a08064"), 0.0, 0.0, up=-1, deep=0.2, bounce=0.6), lint[..., None])
    over(pic, inside, hole)
    info["window_hole"] = hole
    # his small window over the door: dark, a wooden grille across it
    W2 = M.WINDOW2
    hole2 = band(u, W2["s0"], W2["s1"], su) * band(h, W2["sill"], W2["top"], 1 / k) * info["e_m"]
    grille = np.maximum(band((u - W2["s0"]) % 12.5, 0, 2.2, su), band((h - W2["sill"]) % 13.0, 0, 2.2, 1 / k))
    c2 = lerp(col("#3e3036"), LIGHT.on(col("#8a6a4c"), FACE_FRONT * 0.7, 0.0), (grille * 0.9)[..., None])
    over(pic, c2, hole2)
    # his door, open: the floor inside, the far jamb, the door leaf folded back against it, the dark of the room
    D_ = M.DOOR_E
    hole3 = band(u, D_["s0"], D_["s1"], su) * band(h, 0.0, D_["h"], 1 / k) * info["e_m"]
    fu, fv, fZ, fk, fok = level_in(FE, 6.0)                                                      # the threshold, then the floor inside
    floor_in = band(fu, D_["s0"], D_["s1"], soft_edges(fu)) * band(fv, 0.0, 400.0, soft_edges(fv)) * fok
    dark = col("#2c2230")[None, None, :] * np.ones(SHAPE + (1,), dtype=F32)
    dark = lerp(dark, col("#5a463e"), (floor_in * np.clip(1 - (fv - wall_t) / 160.0, 0, 1) * 0.8)[..., None])
    sill_ = band(fv, 0.0, wall_t, soft_edges(fv)) * floor_in
    dark = lerp(dark, LIGHT.on(col("#cfc2a8"), FACE_UP, 0.0, up=1, bounce=0.2), (sill_ * 0.9)[..., None])
    jv, jh, jZ, jk, jok = side_at(FE, D_["s1"])
    jamb = band(jv, 0.0, wall_t, soft_edges(jv)) * band(jh, 0.0, D_["h"], 1 / jk) * jok
    dark = lerp(dark, LIGHT.on(col("#b89670"), 0.0, 0.0, deep=0.25, bounce=0.5), jamb[..., None])
    leaf = band(jv, wall_t, wall_t + 92.0, soft_edges(jv)) * band(jh, 4.0, D_["h"] - 4, 1 / jk) * jok          # the leaf, swung in against the jamb's far side
    planks = band(jv % 23.0, 0.0, 1.6, soft_edges(jv))
    leaf_c = lerp(col("#5c4232"), col("#3a2a24"), planks[..., None])
    dark = lerp(dark, LIGHT.on(leaf_c, 0.0, 0.0, deep=0.4, bounce=0.6), (leaf * 0.95)[..., None])
    over(pic, dark, hole3)
    info["door_hole"] = hole3
    # the house of prayer: its broad door, shut, in a plain frame of stone; two small windows high up
    pu, ph, pk, pm = info["p_u"], info["p_h"], info["p_k"], info["p_m"]
    spu = soft_edges(pu)
    DP = M.DOOR_P
    frame_ = band(pu, DP["s0"] - 16, DP["s1"] + 16, spu) * band(ph, 0, DP["h"] + 18, 1 / pk) * pm
    trav = LIGHT.on(col("#e4dac6") * (0.95 + 0.1 * wn(pu, ph, 40, seed + 3, 3)[..., None]), FACE_FRONT, info["p_cut"], bounce=0.4)
    over(pic, trav, frame_)
    door = band(pu, DP["s0"], DP["s1"], spu) * band(ph, 0, DP["h"], 1 / pk) * pm
    mid = (DP["s0"] + DP["s1"]) / 2
    wood = col("#6a4a34")[None, None, :] * (0.9 + 0.2 * wn(pu * 0.3, ph, 30, seed + 4, 3)[..., None])
    wood = lerp(wood, col("#3a2a26"), (band(pu, mid - 1.5, mid + 1.5, spu) + band(ph % 72.0, 0, 3, 1 / pk) * 0.6 + band((pu - DP["s0"]) % 21.0, 0, 1.2, spu) * 0.35)[..., None].clip(0, 1))
    studs = (band((pu - DP["s0"] - 10) % 42.0, 0, 3.2, spu) * band((ph - 20) % 72.0, 0, 3.2, 1 / pk))
    wood = lerp(wood, col("#2a2024"), (studs * 0.8)[..., None])
    over(pic, LIGHT.on(wood, FACE_FRONT, np.maximum(info["p_cut"], 0.35), deep=0.15, bounce=0.35), door)
    for (a0, a1) in ((680.0, 724.0), (1112.0, 1156.0)):
        wn_ = band(pu, a0, a1, spu) * band(ph, 432, 478, 1 / pk) * pm
        bars = band((pu - a0) % 11.0, 0, 1.8, spu)
        over(pic, lerp(col("#3c3038"), col("#4a4048"), bars[..., None]), wn_)
    return pic


def under(seed=5):
    info = {}
    pic = sky_layer()
    fc, fa = far_bank()
    over(pic, fc, fa)
    info["far"] = (fc, fa)
    snap_far = pic.copy()
    rc, rmask, (rx, rz, rk) = river(pic)
    over(pic, rc, rmask)
    snap_river = pic.copy()
    info.update(river=rmask, rx=rx, rz=rz, rk=rk)
    gc, gmask, gx, gz, gk, on_land = ground()
    lit = LIGHT.on(gc, FACE_UP * 0.8, 0.0, up=1, deep=0.0, bounce=0.25)
    lit = far(lit, gz, "#d8d4d8", 9000.0, 0.7)
    over(pic, lit, gmask)
    info.update(ground=gmask, gx=gx, gz=gz, gk=gk, on_land=on_land.astype(F32))
    info["gardens"] = gardens(pic)
    snap_gardens = pic.copy()
    road_houses(pic, info)
    road_gables(pic, info)
    near_fronts(pic, info)
    openings(pic, info)
    yard_ground(pic, info)
    ground_shadows(pic, info)
    info["steps"] = T.landing_steps(pic, hide=info["ground"] * (1 - info["on_land"]))
    T.landing_stack(pic)
    T.bench(pic)
    T.coop(pic)
    T.dish(pic)
    info["fig_a"] = T.fig_tree(pic)
    cloud_shadow(pic, info)
    same = lambda a: (np.abs(pic - a).max(axis=2) < 1e-6).astype(F32)       # what is still seen of a layer at the end
    info.update(vis_far=same(snap_far), vis_river=same(snap_river) * rmask, vis_gardens=same(snap_gardens))
    return np.clip(pic, 0, 1), info


def yard_ground(pic, info, seed=231):
    """Inside the hen yard: earth scratched bare and darker, straw strewn about, a few feathers."""
    x, z, k = info["gx"], info["gz"], info["gk"]
    u, v = in_frame(FE, x, z)
    yard = (band(u, M.YARD["s0"], M.YARD["s1"], soft_edges(u)) * band(v, -M.YARD["out"], 0.0, soft_edges(v)) * info["ground"]).astype(F32)
    own = np.empty(SHAPE + (3,), dtype=F32)
    own[...] = col("#9c8466")
    own *= (1 + (wn(x, z, 70, seed, 3) - 0.5) * 0.24 + (wn(x, z, 16, seed + 1, 2) - 0.5) * 0.16)[..., None]
    straw = step(0.62, 0.70, wn(x * 2.0, z, 22, seed + 2, 3)) * step(0.3, 0.6, wn(x, z, 90, seed + 3, 3))
    own = lerp(own, col("#d8bc78"), (straw * 0.75)[..., None])
    c = LIGHT.on(own, FACE_UP * 0.8, 0.0, up=1, bounce=0.25)
    over(pic, c, yard)
    info["yard"] = yard
    return pic


def ground_shadows(pic, info):
    """The shadows things throw on the lane, the landing and the yard: long and soft, toward us and to the right."""
    x, z, g = info["gx"], info["gz"], info["ground"]
    cut = shade_world(x, np.zeros_like(x), z, T.thing_solids(), spread=0.02)
    cut = np.maximum(cut, shade_in(FE, x, np.zeros_like(x), z, T.front_thing_solids(), spread=0.02))
    cut = blur(cut * g, 0.8) * g
    tint(pic, (0.56, 0.58, 0.86), (cut * 0.62).astype(F32))
    info["ground_cut"] = cut
    return pic


def cloud_shadow(pic, info, seed=241):
    """A cloud's shadow over the nearest ground, its edge soft and wandering, as on the temple steps: it keeps the
    bottom of the picture quiet and deep."""
    edge_y = 552 + (noise(SHAPE, (300, 60), seed, 3) - 0.5) * 50 + (PX - 400) * 0.03
    m = step(0.0, 1.0, (PY - edge_y) / 40.0) * np.clip(info["ground"] + info["steps"], 0, 1)
    tint(pic, "#a8908c", (m * 0.46).astype(F32))
    return pic


# the cut-outs back to front, as the engine lays them (their bases: rome_tiber_layout.py); window-wall, cut from back.png
# itself, comes between the well and the washing
ORDER = ("well", "washing", "barge", "curb", "fence-corner", "fence", "landing-edge")


def planes(fast, seed=5):
    """Every cut-out but window-wall (which is cut from the finished backdrop). -> {name: (color, coverage)}"""
    fence = T.fence_plane()
    return {"washing": T.washing_plane(), "fence-corner": fence["fence-corner"], "fence": fence["fence"], "well": T.well_plane(),
            "barge": T.barge_plane(), "curb": T.curb_plane(), "landing-edge": T.landing_front_plane()}


# ================================================================ the details: crisp things over the brushwork
def details(pic, info, seed=301):
    """Every hard thing stated again crisply, and the small things: the window's sill and lintel and its shutter folded
    back, the washing line, the door's beam and threshold, the little case upright on the right-hand post of his door,
    the rings on the broad door, cracks, weeds at the foot of the walls, stones and straw on the lane, the light on the
    river."""
    rng = np.random.default_rng(seed)
    s = Sheet2(SHAPE)
    fl = lambda pts, c, w=1.0, a=1.0: s.line(fpoly(FE, pts), c, w, a)
    fp = lambda pts, c, a=1.0: s.poly(fpoly(FE, pts), c, a)
    sh = lambda c, n=(0, -1, 0), **kw: T.shade(c, T.fe_normal(*n), **kw)
    W_, W2, D_ = M.WINDOW, M.WINDOW2, M.DOOR_E
    # ---- Eleazar's window: the shutter, one leaf of boards, folded back flat against the wall on its near side
    s0, s1 = W_["s0"] - 101, W_["s0"] - 3
    h0, h1 = W_["sill"] + 2, W_["top"] - 2
    fp([(s0, -4, h0), (s1, -4, h0), (s1, -4, h1), (s0, -4, h1)], sh("#6e8678"))
    for u in np.linspace(s0, s1, 6)[1:-1]:                    # its boards
        fl([(u, -4.2, h0 + 1), (u, -4.2, h1 - 1)], sh("#3e4c46"), 0.8, 0.85)
    for hh in (h0 + 16, h1 - 16):                             # the two ledges across it, and the brace between
        fp([(s0 + 2, -5.5, hh - 5), (s1 - 2, -5.5, hh - 5), (s1 - 2, -5.5, hh + 5), (s0 + 2, -5.5, hh + 5)], sh("#7e9688"))
        fl([(s0 + 2, -5.6, hh - 5), (s1 - 2, -5.6, hh - 5)], sh("#3a4640"), 0.7, 0.8)
    fl([(s0 + 6, -5.5, h0 + 21), (s1 - 6, -5.5, h1 - 21)], sh("#7e9688"), 2.2, 1.0)
    fl([(s0 + 6, -5.6, h0 + 21), (s1 - 6, -5.6, h1 - 21)], sh("#a8b8a4"), 0.7, 0.7)
    fl([(s0, -4.5, h0), (s0, -4.5, h1)], sh("#c8d0b8", (-1, 0, 0)), 0.8, 0.8)             # its far edge, lit
    for hh in (h0 + 14, h1 - 14):                             # the iron straps of its hinges
        fl([(s1 - 34, -5.8, hh), (s1 + 2, -5.8, hh)], "#2e2a2c", 1.3, 0.95)
    fl([(s0 - 6, -2, h0 + 52), (s0 + 4, -5, h0 + 52)], "#2e2a2c", 1.0, 0.95)               # the hook that holds it open
    # the sill: a slab of travertine, a little proud; the lintel: a timber over the opening
    fp([(W_["s0"] - 10, -5, W_["sill"] - 6), (W_["s1"] + 10, -5, W_["sill"] - 6), (W_["s1"] + 10, -5, W_["sill"]), (W_["s0"] - 10, -5, W_["sill"])], sh("#e8dcc2"))
    fl([(W_["s0"] - 10, -5, W_["sill"] - 6), (W_["s1"] + 10, -5, W_["sill"] - 6)], "#6a5448", 0.9, 0.9)
    fp([(W_["s0"] - 14, -2, W_["top"]), (W_["s1"] + 14, -2, W_["top"]), (W_["s1"] + 14, -2, W_["top"] + 13), (W_["s0"] - 14, -2, W_["top"] + 13)], sh("#7a5a40"))
    fl([(W_["s0"] - 14, -2.2, W_["top"]), (W_["s1"] + 14, -2.2, W_["top"])], "#c8a070", 0.8, 0.7)
    # the small window over the door: a frame, a sill; and the washing line between the two, on two pegs
    for (a, b) in ((W2["s0"] - 6, W2["s0"]), (W2["s1"], W2["s1"] + 6)):
        fp([(a, -2, W2["sill"] - 4), (b, -2, W2["sill"] - 4), (b, -2, W2["top"] + 6), (a, -2, W2["top"] + 6)], sh("#8a6a4c"))
    fp([(W2["s0"] - 8, -4, W2["sill"] - 5), (W2["s1"] + 8, -4, W2["sill"] - 5), (W2["s1"] + 8, -4, W2["sill"]), (W2["s0"] - 8, -4, W2["sill"])], sh("#ddd0b4"))
    fp([(W2["s0"] - 8, -2, W2["top"]), (W2["s1"] + 8, -2, W2["top"]), (W2["s1"] + 8, -2, W2["top"] + 8), (W2["s0"] - 8, -2, W2["top"] + 8)], sh("#7a5a40"))
    wash = M.WASH
    us = np.linspace(wash["s0"], wash["s1"], 14)
    fl([(u, -wash["out"], T.line_h(u)) for u in us], "#4a3e34", 0.9, 0.95)
    for u in (wash["s0"], wash["s1"]):
        fl([(u, 0, T.line_h(u) + 1), (u, -wash["out"], T.line_h(u))], "#3e3430", 1.4, 1.0)
    # ---- his door: the beam over it, the threshold, and the little case on the right-hand post as one goes in
    fp([(D_["s0"] - 16, -14, D_["h"]), (D_["s1"] + 16, -14, D_["h"]), (D_["s1"] + 16, -14, D_["h"] + 18), (D_["s0"] - 16, -14, D_["h"] + 18)], sh("#6a4c36"))
    fp([(D_["s0"] - 16, -14, D_["h"]), (D_["s0"] - 16, 0, D_["h"]), (D_["s0"] - 16, 0, D_["h"] + 18), (D_["s0"] - 16, -14, D_["h"] + 18)], sh("#5a4030", (-1, 0, 0)))
    fl([(D_["s0"] - 16, -14.2, D_["h"]), (D_["s1"] + 16, -14.2, D_["h"])], "#b88a60", 0.8, 0.7)
    fp([(D_["s0"] - 8, -22, 0), (D_["s1"] + 8, -22, 0), (D_["s1"] + 8, -22, 7), (D_["s0"] - 8, -22, 7)], sh("#d4c8ae"))
    fp([(D_["s0"] - 8, -22, 7), (D_["s1"] + 8, -22, 7), (D_["s1"] + 8, 0, 7), (D_["s0"] - 8, 0, 7)], T.shade("#e2d8c0", (0, 1, 0)))
    mz = M.MEZUZAH
    fp([(mz["s0"], -2.5, mz["h0"]), (mz["s1"], -2.5, mz["h0"]), (mz["s1"], -2.5, mz["h1"]), (mz["s0"], -2.5, mz["h1"])], sh("#5a3a2a"))
    fp([(mz["s0"], -2.6, mz["h1"] - 3), (mz["s1"], -2.6, mz["h1"] - 3), (mz["s1"], -2.6, mz["h1"]), (mz["s0"], -2.6, mz["h1"])], sh("#b88a5a"))
    fl([(mz["s1"], -2.7, mz["h0"]), (mz["s1"], -2.7, mz["h1"])], "#a07450", 0.6, 0.8)
    # a broom of twigs leaning by his door
    fl([(D_["s1"] + 34, -6, 0), (D_["s1"] + 26, -3, 128)], "#7a5a3a", 1.4, 1.0)
    fp([(D_["s1"] + 24, -8, 0), (D_["s1"] + 46, -8, 0), (D_["s1"] + 38, -6, 36), (D_["s1"] + 30, -6, 36)], sh("#a08a5c"))
    # ---- the house of prayer's door: two iron rings, the threshold step
    DP = M.DOOR_P
    mid = (DP["s0"] + DP["s1"]) / 2
    for u in (mid - 18, mid + 18):
        pts = [(u + 7 * math.cos(a), P_OUT - 3, 112 + 8 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 14)]
        fl(pts, "#2a2226", 1.0, 0.95)
    fp([(DP["s0"] - 20, P_OUT - 30, 0), (DP["s1"] + 20, P_OUT - 30, 0), (DP["s1"] + 20, P_OUT - 30, 9), (DP["s0"] - 20, P_OUT - 30, 9)], sh("#d0c4a8"))
    fp([(DP["s0"] - 20, P_OUT - 30, 9), (DP["s1"] + 20, P_OUT - 30, 9), (DP["s1"] + 20, P_OUT, 9), (DP["s0"] - 20, P_OUT, 9)], T.shade("#e0d6be", (0, 1, 0)))
    # ---- cracks in the plaster, and a few iron hooks
    for i in range(9):
        u = rng.uniform(M.EL["s0"] + 40, M.EL["s1"] - 20) if i < 6 else rng.uniform(M.PR["s0"] + 20, M.PR["s1"] - 20)
        hh = rng.uniform(60, 560)
        off = 0.0 if i < 6 else P_OUT
        pts = [(u, off - 0.5, hh)]
        for j in range(rng.integers(3, 6)):
            u += rng.normal(0, 8)
            hh -= rng.uniform(6, 16)
            pts.append((u, off - 0.5, hh))
        fl(pts, "#7a5a48", 0.7, 0.6)
    # ---- weeds at the foot of the walls and in the quay's joints; the lane's stones, ruts and straw
    for i in range(70):
        if i < 26:                                            # along the foot of the two fronts, outside the yard
            u = rng.uniform(M.YARD["s1"] + 10, M.PR["s1"] - 10)
            if M.BENCH["s0"] - 10 < u < M.BENCH["s1"] + 10 or M.DOOR_P["s0"] - 30 < u < M.DOOR_P["s1"] + 30 or M.DOOR_E["s0"] - 20 < u < M.DOOR_E["s1"] + 50:
                continue
            x, z = M.out(M.along(u), 2.0 - (20 if u > M.PR["s0"] else 0))
        else:                                                 # in the joints along the quay's edge
            z = rng.uniform(M.LANDING["z1"] + 50, 4000)
            x = M.Q + rng.uniform(4, 60)
        k = M.k_at(z)
        bx, by = M.P(x, 0, z)
        for j in range(rng.integers(3, 7)):
            a = rng.uniform(-2.6, -0.5)
            L_ = rng.uniform(5, 14) * k
            tone = mix("#5e7a3c", "#a4b05c", rng.random())
            s.line([(bx + rng.normal(0, 2 * k), by), (bx + math.cos(a) * L_, by + math.sin(a) * L_)], tone, max(0.7, 1.4 * k), 0.95)
    x, z, g = info["gx"], info["gz"], info["ground"]
    drift = noise(SHAPE, 80, seed + 7, 3)
    for i in range(260):                                      # small stones in drifts, each with its shadow toward us and to the right
        X, Y = rng.uniform(150, 800), M.HZ + (598 - M.HZ) * rng.random() ** 0.6
        if g[int(Y), int(X)] < 0.5 or info.get("yard", np.zeros(SHAPE))[int(Y), int(X)] > 0.5 or drift[int(Y), int(X)] < 0.55 or info_paved[0][int(Y), int(X)] > 0.3:
            continue
        k = (Y - M.HZ) / M.EYE
        r = rng.uniform(1.0, 3.2) * k
        if r < 0.7:
            continue
        s.ellipse(X + r * 1.0, Y + r * 0.15, r * 1.5, r * 0.42, "#6e6070", 0.38)
        s.ellipse(X, Y - r * 0.3, r * 1.2, r * 0.72, mix("#b4a690", "#8e7e6c", rng.random()), 0.95)
        s.ellipse(X - r * 0.35, Y - r * 0.55, r * 0.55, r * 0.3, "#d8ccb2", 0.7)
    for i in range(46):                                       # straw blown out of the yard
        X, Y = rng.uniform(470, 800), rng.uniform(430, 598)
        if g[int(Y), int(X)] < 0.5:
            continue
        k = (Y - M.HZ) / M.EYE
        a = rng.uniform(0, math.pi)
        L_ = rng.uniform(4, 9) * k
        s.line([(X, Y), (X + math.cos(a) * L_, Y - math.sin(a) * L_ * 0.4)], mix("#e0c47c", "#c8a45c", rng.random()), max(0.6, 0.9 * k), 0.9)
    s.onto(pic)
    # ---- the river: crisp glints in the bright water, and a pale line where it meets the quay and the landing
    rx, rz = info["rx"], info["rz"]
    gl = Sheet2(SHAPE)
    for i in range(900):
        X, Y = rng.uniform(0, 380), rng.uniform(254, 470)
        if info["river"][int(Y), int(X)] < 0.5:
            continue
        shine = math.exp(-((Y - (float(far_waterline(np.asarray([X]))[0]) + 6)) / 18.0) ** 2) + 0.6 * math.exp(-((X + 60) / 260.0) ** 2) * min(1.0, max(0.0, (Y - 280) / 160.0))
        if rng.random() > shine * 0.8:
            continue
        k = (Y - M.HZ) / M.EYE
        L_ = rng.uniform(1.5, 6) * (0.4 + k)
        gl.line([(X - L_, Y), (X + L_, Y)], mix("#fff4d8", "#ffffff", rng.random()), max(0.6, 0.9 * (0.4 + k)), 0.9)
    gl.onto(pic)
    return pic


# ================================================================ finishing
def grade(picture, vib=0.6, lift=0.055):
    """The last glaze, the same for the backdrop and every cut-out (as the street's): colors gone dull in the shade made
    richer, a little blue air in the darks."""
    lum = (picture @ np.array([0.3, 0.55, 0.15], dtype=F32))[..., None]
    sat = (picture.max(-1) - picture.min(-1))[..., None]
    out = lum + (picture - lum) * (1 + vib * np.clip(1 - sat / 0.45, 0, 1))
    out = out + lift * np.clip(1 - lum / 0.5, 0, 1) * np.array([0.6, 0.8, 1.4], dtype=F32)
    return np.clip(out, 0, 1).astype(F32)


PALETTES = {}


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02):
    """Grain, then a palette chosen for the picture, with speckle: a PNG-8. -> the size of the file"""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    PALETTES[name] = pal
    return os.path.getsize(name)


def brushed(color, alpha, ground, fast, sizes=(7, 4, 2), keep=0.40, seed=4, restate=0.55):
    """A cut-out repainted with a small brush on the ground it stands against, then said again crisply (as the
    steps'): -> its color. Its edge stays exactly as it was (the coverage is not touched)."""
    if fast or not (alpha > 0.5).any():
        return color
    ys, xs = np.where(alpha > 0.02)
    y0, y1, x0, x1 = max(0, ys.min() - 12), min(H, ys.max() + 13), max(0, xs.min() - 12), min(W, xs.max() + 13)
    flat = ground[y0:y1, x0:x1].copy()
    over(flat, color[y0:y1, x0:x1], alpha[y0:y1, x0:x1])
    painted = strokes(flat, sizes=sizes, seed=seed, density=1.8, jitter=0.03, keep=keep)
    painted = lerp(painted, flat, (restate * alpha[y0:y1, x0:x1])[..., None])
    out = color.copy()
    out[y0:y1, x0:x1] = painted
    return out


def brush_flow(info):
    """Which way the brush runs where the picture gives it nothing to follow: along the two near fronts toward their own
    vanishing point, along the road's houses toward the road's, level on the water and the ground and in the sky."""
    flow = np.zeros(SHAPE, dtype=F32)
    vp_front = M.VX + M.F * M.D[0] / M.D[1]
    fronts = np.clip(info["e_m"] + info["p_m"], 0, 1) > 0.5
    flow = np.where(fronts, np.arctan2(PY - M.HZ, PX - vp_front), flow)
    return flow.astype(F32)


def window_wall_mask(info):
    """The front of Eleazar's house round his window, everything of it within a man's height of the opening on every
    side (the sill and the wall under it, the jambs, the shutter, the wall over the lintel, the eave above it), and the
    fig's twigs in front of it, with the opening itself clear."""
    Wn = M.WINDOW
    reach = 175.0
    u, h, k = info["e_u"], info["e_h"], info["e_k"]
    near = band(u, Wn["s0"] - reach, Wn["s1"] + reach, soft_edges(u)) * band(h, Wn["sill"] - reach, Wn["top"] + reach, 1 / k)
    region = near * info["e_m"]
    hole = info["window_hole"]
    return ((region > 0.5) & (hole < 0.5)).astype(F32)        # (the fig's twigs in front of the wall with it: they hide him too)


def show(picture, name):
    Image.fromarray((np.clip(picture, 0, 1) * 255).astype(np.uint8)).save(name)


if __name__ == "__main__":
    t0 = time.time()
    fast = "fast" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    base, info = under()
    show(base, f"{WORK}/1-under.png")
    print("under", round(time.time() - t0, 1))
    if fast:
        pic = base.copy()
    else:
        pic = strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.22, flow=brush_flow(info))
    print("brushed", round(time.time() - t0, 1))
    if not fast:
        fc, fa = info["far"]
        over(pic, lerp(fc, pic, 0.25), np.clip(fa * 0.85 * info["vis_far"], 0, 1))       # the far bank's houses and temples, crisp again
        gc, ga = info["gardens"]
        over(pic, gc, np.clip(ga * 0.8 * info["vis_gardens"], 0, 1))
        pic = lerp(pic, base, (info["vis_river"] * 0.40)[..., None])                       # the river keeps some of its own streaks
    ground = pic.copy()
    details(pic, info)
    pic = grade(pic)
    show(pic, f"{WORK}/2-back.png")
    print("details", round(time.time() - t0, 1))
    raw = planes(fast)
    bc, ba = raw["barge"]                                        # the landing and the quay are nearer than any of the barge they
    raw["barge"] = (bc, (ba * (1 - info["ground"])).astype(F32))  # overlap: its bow goes down behind the landing's far edge
    cut = {}
    for i, (name, (c, a)) in enumerate(raw.items()):
        cut[name] = (grade(brushed(c, a, ground, fast, seed=20 + i)), (a > 0.5).astype(F32))
    whole = pic.copy()
    for name in ORDER:
        c, a = cut[name]
        over(whole, c, a)
    show(whole, f"{WORK}/2-all.png")
    print("planes", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    print("back", finish(pic, f"{OUT}/back.png", 160))
    for name, colors in (("washing", 40), ("fence-corner", 56), ("fence", 64), ("well", 48), ("barge", 96), ("curb", 40), ("landing-edge", 48)):
        c, a = cut[name]
        print(name, finish(c, f"{OUT}/{name}.png", colors, a))
    # the window wall: cut from the finished backdrop itself, so that laid over it, it changes nothing
    back_im = Image.open(f"{OUT}/back.png")
    back_idx = np.asarray(back_im)
    pal = PALETTES[f"{OUT}/back.png"]
    ww = window_wall_mask(info)
    save(f"{OUT}/window-wall.png", back_idx, pal, ww)
    print("window-wall", os.path.getsize(f"{OUT}/window-wall.png"))
    made = HENS.paint(OUT, pal)                                  # the hens, in the backdrop's own palette
    HENS.sheet(OUT, made, "out/rome-tiber-hens-sheet.png")
    print("hens", {k_: len(v_) for k_, v_ in made.items()})
    lay = LAY.layout(info, cut)
    with open(f"{OUT}/layout.json", "w") as fh:
        json.dump(lay, fh, indent=1)
    os.system(f"{sys.executable} comp.py {OUT} back well window-wall washing barge curb fence-corner fence landing-edge")
    os.system(f"{sys.executable} rome_tiber_check.py")
    print("done", round(time.time() - t0, 1))

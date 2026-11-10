"""PAINT-21A: the top of the Satta Pass, about 8 April 1830, morning, wind (edo-satta). The Tokaido's road of 1655, cut
high on the headland's mountainside between Yui and Okitsu, about 90 m over Suruga Bay. Keyed at 50 in `edo-morning`
(PAINT-20A's key). Our own place on the road and our own view: the road running across the picture, the drop beyond its
bank, the bay spread out below, Fuji across it.
PAINT-23 (round twenty-three, tools/paint/DEPTH.md): painted again in THREE PLANES, and in WATERCOLOUR (the act's drawing
laid in washes on paper, Yui's recipe). The camera, the placings and every number of the scene file are round
twenty-one's and have not moved; so are the outlines of the cut-outs that were (the cap of cloud, the bent pine, the
pass on the Jizo's hat): they are painted again inside them.

LIGHT   The act's sun: in the east, behind us and to the left, about 30 degrees up: faces toward us and to the left are lit,
        shadows fall to the right and away, each a cool glaze over the local colour. The wind off the sea from the right:
        the pines lean left, the grass lies over to the left, the clouds are drawn out to the left.
DEPTH   horizon 288, full 590 (persp.Camera: eye 330 cm, Z0 875, focal 800; edo_satta_kit). The road is level here; at the
        left edge it drops away toward Nishikurasawa (the climb they came up), at the right edge it starts down west to
        Okitsu. We stand on the uphill side of it, on the lip of the cutting it was made by.
NEAR    (edo_satta_near.py) near.png: a wind-bent black pine on the slope at our right, its trunk in from the right edge
        above Okitsu, its limbs and pads streaming left across the top (it stirs: fx near-sway); front.png: the lip of the
        cutting along the bottom, rock, sasa and wind-flattened grass, rising into a rock shoulder in the bottom right
        corner (a `blocked` patch under it). Dark and warm, in the shade of the mountainside behind us; lit rims on the
        left.
MIDDLE  the play, in full sun: the road (a graded wash measured in the world: three worn tracks of feet and hooves, rough
        between them, curving up out of the lower left where the road comes up from the climb; stones and tufts at a true
        density); the bank at its far edge (earth and grass, low, lit, its grass streaming left, wind-pruned shrubs); the
        Jizo before it in its red bib and little straw hat; O-Shige's stone; the bent pine on the bank's top leaning toward
        Fuji. Every shadow one way; the shade of the mountainside behind us lies along the road's near edge, scalloped.
FAR     (edo_satta_far.py) the drop: just past the bank only air, and the bay 90 m down; the near flank falling away at the
        left (woods seen from above, crowns large at its top and small at its foot, white water on rocks at its foot); the
        far stretch of the headland, its cliffs and THE OLD SHORE at their foot, white water on the rocks; capes one behind
        another to the head of the bay; Izu in three ranges; Okitsu's crumbs of roofs and its temple; sails at several
        distances; Fuji as Yui has it, enormous, under its cap of cloud; a sky whose clouds grow smaller toward the horizon.
TONES   the lightest light is the paper: Fuji's snow and its cap of cloud, the white water; in the play the sunlit road and
        bank round the Jizo, whose red bib is the picture's red touch. The near plane is the darkest and warmest.
PLACE   We stand on the road at the top of the pass looking out over its bank (the act's compass: the bay in front, Fuji
        across it, west to the right). Below us at the left the headland's flank falls away to the sea; along its foot the
        old shore, where the road ran before 1655, is only white water and rock now ("forget your parent, forget your
        child"); beyond it the coast curves back toward Kurasawa and Yui and on under Fuji. Across the bay, east, Izu lies
        long and low; far to the right, west, Okitsu's roofs and a temple roof in the haze. On the bank: the Jizo at child
        height in its red bib and little straw hat; the bent pine at the right, leaning toward Fuji. O-Shige's stone at
        the road's far edge, left.
PAPER   watercolor.wash on the backdrop and wash_cut (the same seed, crisp) on every cut-out, just before the palette:
        finish_all(). Laid wet in wet (edo_satta_far.wet_mask): the sky, Fuji, the far land, the far stretch, the water.

  python3 edo_satta.py fast        the composition without the brush pass (out/edo-satta-1-under.png, -2-all.png)
  python3 edo_satta.py fast wash   the same with the paper's finish (out/edo-satta-fast-comp.png)
  python3 edo_satta.py             the full passes: out/edo-satta/ (back.png, the cut-outs, layout.json), -comp.png
  python3 install.py edo-satta     keys it in the game's paints and installs it; then python3 ../stamp.py
"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
import land
import depth as D
import watercolor as WC
from edo_kurasawa_kit import cloud_cap, pine_pads, Paper, STONE_LIT, STONE, STONE_SHADE, RED_BIB, EARTH, GRASS, GRASS_LIT, GRASS_SHADE
from edo_satta_kit import *
import edo_satta_far as FAR
import edo_satta_near as NEAR

SEED = 1655
OUT = "out/edo-satta"
PT = lambda X, Z: CAM.pt(X, 0.0, Z)
PX = lambda X, Z: CAM.scale(Z)
ORDER = ["cloud", "pine", "front", "near"]


# ================================================================ the outlines kept (round twenty-one's cut-outs, exactly)
def old_cloud():
    """The cap of cloud's outline (edo_kurasawa_kit.cloud_cap: the same cloud as at Nishikurasawa). -> (cover, outline)."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    outline = cloud_cap(sheet, lines, FUJI)
    _, a = sheet.done()
    _, la = lines.done()
    return (np.maximum(a, la) >= 0.5).astype(F32), outline


def old_pine():
    """The bent pine's geometry, as round twenty-one drew it (its outline is the scene's `pine` area and its base 475):
    -> (cover, trunk points, its branches, pads), the cover exactly round twenty-one's."""
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    P_ = PINE
    k = kz(P_["z"])
    foot = gp(P_["x"], P_["z"])
    pts = [(0, 0), (-14, 110), (-46, 210), (-104, 300), (-170, 368), (-250, 420), (-330, 452)]
    trunk = [gp(P_["x"] + dx, P_["z"], dy) for dx, dy in pts]
    sheet.taper(trunk, (0, 0, 0), 30 * k, 10 * k)
    sheet.taper([(p[0] - 1.6, p[1] - 1.2) for p in trunk[:-1]], (0, 0, 0), 11 * k, 4 * k)
    branches = []
    for (bx_, by_, ex_, ey_) in ((-46, 210, -40, 345), (-104, 300, -84, 386), (-170, 368, -210, 418), (-250, 420, -300, 468)):
        b = [gp(P_["x"] + bx_, P_["z"], by_), gp(P_["x"] + ex_, P_["z"], ey_)]
        branches.append(b)
        sheet.taper(b, (0, 0, 0), 10 * k, 4 * k)
    stub = [gp(P_["x"] - 10, P_["z"], 150), gp(P_["x"] + 30, P_["z"], 190)]
    sheet.taper(stub, (0, 0, 0), 6 * k, 3 * k)
    pads = []
    rng_ = np.random.default_rng(12)
    for (dx_, dy_, rx_, ry_) in ((-84, 392, 78, 34), (-200, 430, 86, 34), (-300, 472, 76, 30), (-380, 488, 56, 24), (-40, 350, 44, 20)):
        for j in range(3):
            ox = (j - 1) * rx_ * 0.62 + rng_.normal(0, 6)
            oy = (8 if j == 1 else -4) + rng_.normal(0, 4)
            c = gp(P_["x"] + dx_ + ox, P_["z"], dy_ + oy)
            pads.append((c[0], c[1], rx_ * k * (0.62 if j != 1 else 0.78), ry_ * k * (0.85 if j != 1 else 1.0)))
    pine_pads(sheet, lines, [], pads, 12, scale=1.0, lit_side=-1, contour=True, alpha_line=0.55, w_line=0.8)
    V.contour(lines, trunk, foot[1], warm=True, alpha=0.5)
    _, a = sheet.done()
    _, la = lines.done()
    return (np.maximum(a, la) >= 0.5).astype(F32), trunk, branches, stub, pads


def pass_geom():
    """O-Shige's pass on the Jizo's hat, as round twenty-one placed it (pixel-aligned with the hat)."""
    J = JIZO
    k = kz(J["z"])
    p = gp(J["x"] - 16, J["z"] - 9, J["h"] - 22)
    w, h = 22 * k, 13 * k
    ang = -0.35

    def rot(dx, dy):
        return (p[0] + dx * math.cos(ang) - dy * math.sin(ang), p[1] + dx * math.sin(ang) + dy * math.cos(ang))
    quad = [rot(-w / 2, -h / 2), rot(w / 2, -h / 2), rot(w / 2, h / 2), rot(-w / 2, h / 2)]
    sheet, lines = Paper(SHAPE), Paper(SHAPE)
    sheet.poly(quad, (0, 0, 0))
    sheet.poly([rot(-w / 2 + 1, -h / 2 - 1.5), rot(w / 2 - 3, -h / 2 - 1.5), rot(w / 2 - 3, -h / 2), rot(-w / 2 + 1, -h / 2)], (0, 0, 0))
    lines.line(quad + [quad[0]], (0, 0, 0), 0.8, 0.8)
    lines.line([rot(-w / 2, h * 0.18), rot(w / 2, h * 0.18)], (0, 0, 0), 0.6, 0.7)
    _, a = sheet.done()
    _, la = lines.done()
    return (np.maximum(a, la) >= 0.5).astype(F32), quad, rot, w, h


# ================================================================ pass 1: the washes
def paint_ground(pic, seed):
    """The bank (earth and grass, low and lit: it faces us and the sun), the road (packed earth: a graded wash, pale
    and cool at its far edge, deeper and warmer toward us; three tracks worn pale by feet and hooves, rough between
    them, curving up out of the lower left where the road comes up from the climb), the verge. Measured in the world.
    -> (the ground's mask, the road's mask, the bank's mask)."""
    x, y = grid(SHAPE)
    X, Z, below = floor()
    tops, fars = TOPS[None, :], FARS[None, :]
    gm = blur((y >= tops - 0.5).astype(F32), 0.6)
    rm = blur((y >= fars).astype(F32), 0.8)
    # ---- the bank: grass on earth; its top in the sun, its face toward us lit, its foot cooler; earth showing through
    vb = np.clip((y - tops) / np.maximum(fars - tops, 4.0), 0, 1)
    bank = ramp(vb, [(0.0, thin(mixp(VERONESE, NAPLES, 0.22), 0.30)), (0.3, thin(mixp(VERONESE, VIRIDIAN, 0.36), 0.20)),
                     (1.0, lerp(mixp(VIRIDIAN, OCHRE, 0.32), PRUSSIAN, 0.10))])
    bank *= (1 + ((world_noise(X, Z, 60, seed + 30, 3) - 0.5) * 0.16)[..., None])
    soil = step(0.60, 0.74, noise(SHAPE, (34, 10), seed + 31, 3)) * np.clip(vb * 1.6, 0, 1)
    bank = lerp(bank, thin(mixp(OCHRE, SIENNA, 0.25), 0.30), (soil * 0.55)[..., None])
    over(pic, np.clip(bank, 0, 1), gm * (1 - rm))
    # ---- the road
    u = np.clip((y - fars) / np.maximum(600.0 - fars, 6.0), 0, 1)                     # across it: 0 at its far edge, 1 at the frame
    t = np.clip((y - 491.0) / 109.0, 0, 1)
    earth = ramp(t, [(0.0, lerp(thin(EARTH, 0.50), HORIZON_C, 0.10)), (0.30, thin(EARTH, 0.34)), (0.70, thin(lerp(EARTH, SIENNA, 0.08), 0.12)), (1.0, lerp(EARTH, SIENNA, 0.14))])
    wander = (world_noise(X, Z, (900, 60), seed + 34, 2) - 0.5) * 0.14
    width = 0.045 + 0.03 * world_noise(X, Z, (700, 400), seed + 37, 2)
    track = sum(np.exp(-((u - c - wander * (1 + 0.6 * j)) / width) ** 2) * (0.45 + 0.75 * world_noise(X, Z, (500, 300), seed + 40 + j, 2))
                for j, c in enumerate((0.17, 0.46, 0.77)))
    earth = lerp(earth, thin(lerp(EARTH, NAPLES, 0.15), 0.66), (np.clip(track, 0, 1) * 0.60)[..., None])
    earth *= (1 + ((world_noise(X, Z, (420, 26), seed + 35, 3) - 0.5) * 0.14 + (world_noise(X, Z, 70, seed + 38, 2) - 0.5) * 0.10
                   + (world_noise(X, Z, 18, seed + 39, 2) - 0.5) * 0.08)[..., None])
    rough = (1 - np.clip(track, 0, 1)) * 0.11 + np.exp(-((u - 0.02) / 0.05) ** 2) * 0.12 + np.exp(-((u - 0.96) / 0.06) ** 2) * 0.10
    earth *= (1 - rough[..., None])
    k_ = (world_noise(X, Z, 260, seed + 32, 2) - 0.5) * 0.06                      # warmer here (dry ochre), cooler there (stony grey)
    earth[..., 0] += k_
    earth[..., 2] -= k_ * 0.8
    stony = step(0.60, 0.75, world_noise(X, Z, 150, seed + 33, 3)) * (1 - np.clip(track, 0, 1))
    earth = lerp(earth, thin(mixp(PRUSSIAN, OCHRE, 0.35), 0.45), (stony * 0.30)[..., None])
    over(pic, np.clip(earth, 0, 1), rm)
    # the bank's foot along the road: a crumbled lip of earth in the bank's own shade
    foot = np.clip(1 - np.abs(y - (fars - 2.5)) / 3.5, 0, 1)
    tint(pic, thin(mixp(OCHRE, PRUSSIAN, 0.5), 0.45), (foot * 0.6).astype(F32))
    # the verge along the bottom: thin grass coming up in the road's edge
    vg = step(0.86, 0.98, u) * step(0.45, 0.7, world_noise(X, Z, 90, seed + 36, 3))
    tint(pic, thin(mixp(VERONESE, OCHRE, 0.3), 0.40), (vg * 0.5 * rm).astype(F32))
    return gm, rm, gm


def air_over_bank(pic):
    """A breath of air just beyond the bank's top: what lies below the edge (the flank, the bay) is three hundred metres
    off and more, and the bank's crest stands against it."""
    x, y = grid(SHAPE)
    band = np.clip(1 - (TOPS[None, :] - y) / 12.0, 0, 1) * (y < TOPS[None, :] + 1)
    over(pic, HORIZON_C, (band ** 1.6 * 0.20).astype(F32))


def shade_edge(x):
    """The row where the shade of the mountainside behind us ends on the road, at column x: just beyond the lip of the
    cutting (edo_satta_near.lip_top), thin along the left (the three stand there in the sun), wider toward the right;
    never above row 548 (where people stand at the right it stays thin)."""
    v = NEAR.lip_top(x) - 9.0 - 3.0 * math.sin(x / 23.0 + 1.0) - 2.0 * math.sin(x / 9.0)
    if x > 300:
        v -= (x - 300) * 0.035
    if x > 420:                                                            # the slope behind us is higher to the right: its shade comes further in
        v -= ((x - 420) / 380.0) ** 1.2 * 14.0
    return max(v, 546.0)


def cast_shadows(pic, info, seed):
    """Every shadow one way, to the right and away, each a cool glaze (watercolour shadows): the Jizo's and its stone's,
    O-Shige's stone's, the shrubs' on the bank. Then the large shadow from outside the picture: the shade of the
    mountainside behind us along the road's near edge, scalloped by the grass and stones on the lip, flecked with sun.
    -> the shadows' mask."""
    x, y = grid(SHAPE)
    X, Z, below = floor()
    sh = np.zeros(SHAPE, dtype=F32)

    def add(pts, amount=0.9, soft=0.7, wobble=0.8, s=0):
        if len(pts) >= 3:
            np.maximum(sh, mask_poly(SHAPE, pts, soft=soft, wobble=wobble, seed=seed + s) * amount, out=sh)
    j = JIZO
    add(V.shadow_pts([(j["x"] - 18, 0, j["z"]), (j["x"] + 18, 0, j["z"]), (j["x"] + 18, 92, j["z"]), (j["x"] + 22, j["h"], j["z"]), (j["x"] - 22, j["h"], j["z"]), (j["x"] - 18, 92, j["z"])]), 0.95, s=1)
    add(V.shadow_pts([(j["x"] - 26, 0, j["z"] - 18), (j["x"] + 26, 0, j["z"] - 18), (j["x"] + 26, 22, j["z"] + 18), (j["x"] - 26, 22, j["z"] - 18)]), 0.95, s=2)
    s = SEAT
    add(V.shadow_pts([(s["x"] - s["w"] / 2, 0, s["z"] - s["d"] / 2), (s["x"] + s["w"] / 2, 0, s["z"] - s["d"] / 2), (s["x"] + s["w"] / 2, s["h"], s["z"]),
                      (s["x"] - s["w"] / 2, s["h"], s["z"])]) + [gp(s["x"] + s["w"] / 2, s["z"] + s["d"] / 2)], 0.95, s=3)
    for i, (sx_, w_, h_) in enumerate(SHRUBS):
        row = bank_top(sx_) + 3
        add([(sx_ - w_ * 0.2, row + 1), (sx_ + w_ * 0.9, row + 3), (sx_ + w_ * 1.3, row + 6), (sx_ + w_ * 0.2, row + 5)], 0.8, s=10 + i)
    sh = sh * info["ground"]
    glaze(pic, sh, SHADE, 1.0)
    # the mountainside's shade along the near edge of the road: its edge is the lip's own outline laid along the light,
    # so each tuft and stone on the lip throws a long blade of shade in, pointing to the right and away
    edge = np.array([shade_edge(c) for c in range(W)], dtype=F32)
    d = (y - edge[None, :])                                               # rows inside the shade
    blades = np.zeros(SHAPE, dtype=F32)
    rng = np.random.default_rng(seed + 77)
    for i in range(150):
        cx = rng.uniform(-30, 820)
        e = shade_edge(min(max(cx, 0), 799)) + 2.0
        ln = rng.uniform(8, 30) * (1.0 if rng.random() < 0.8 else 1.8)
        tip = (cx + ln * 0.95, e - ln * 0.30)
        w0 = rng.uniform(1.5, 4.0)
        blades = np.maximum(blades, mask_line(SHAPE, [(cx, e), ((cx + tip[0]) / 2, (e + tip[1]) / 2 + 0.6), tip], [w0, w0 * 0.6, 0.6], soft=0.6))
    for (cx, hw, hgt) in NEAR.ROCKS:                                       # the rocks on the lip: broad shade
        e = shade_edge(min(max(cx, 0), 799)) + 1.0
        blades = np.maximum(blades, mask_poly(SHAPE, [(cx - hw, e + 2), (cx - hw * 0.4 + hgt * 0.9, e - hgt * 0.28), (cx + hw * 0.6 + hgt * 1.1, e - hgt * 0.32), (cx + hw + hgt * 0.4, e + 2)], soft=0.8, wobble=1.5, seed=seed + int(cx)))
    fleck = step(0.66, 0.72, world_noise(X, Z, (46, 34), seed + 72, 2)) * np.clip(1.0 - d / 16.0, 0.0, 1)
    mount = np.clip(np.maximum(step(-0.5, 1.5, d), blades) * (1 - fleck * 0.9), 0, 1) * info["road"]
    mount = blur(mount.astype(F32), 0.5)
    glaze(pic, mount, SHADE_PINES, 0.66)
    return np.maximum(sh, mount)


def under(seed=SEED):
    info = {}
    pic = FAR.paint_sky(seed)
    info["clouds"] = FAR.paint_clouds(pic, seed)
    info["fuji"], info["snow"] = FAR.paint_fuji(pic, FAR.YUI_SEED)                   # (Yui's seed: the same gullies, the same snow)
    info["cloud2"] = FAR.paint_fuji_cloud(pic, FAR.YUI_SEED)
    info["farland"], info["farparts"] = FAR.paint_far_land(pic, seed)
    info["water"] = FAR.paint_bay(pic, seed)
    info["yui"], info["okitsu"] = FAR.paint_far_coast(pic, seed, info["water"])
    info["coastland"] = np.maximum(info["yui"], info["okitsu"])
    info["far"], info["spur"] = FAR.paint_far_stretch(pic, seed)
    info["cliff"] = FAR.paint_cliffs(pic, seed)
    info["flank"], info["flank_facing"] = FAR.paint_flank(pic, seed)
    air_over_bank(pic)
    info["foam"] = np.maximum(mask_line(SHAPE, [(p[0], p[1] + 2.0) for p in CLIFF_FOOT], 5.0, soft=1.0),
                              mask_line(SHAPE, [(p[0], p[1] - 1.5) for p in COAST], 4.0, soft=1.0)).astype(F32)
    info["ground"], info["road"], info["bank"] = paint_ground(pic, seed)
    return np.clip(pic, 0, 1), info


# ================================================================ pass 3: the crisp things
SHRUBS = [(96, 26, 14), (138, 16, 9), (468, 22, 11), (560, 30, 15), (622, 18, 10), (770, 24, 12), (212, 14, 8), (520, 12, 7)]


def jizo(L, info):
    """The Jizo by the road (the pass is named for a holy image a fisherman caught in his net): a small grey stone figure
    on a low stone, a round head, the hands together at the breast, a red bib tied at the neck and a little straw hat
    tied under the chin; exactly Little Sister's height at `jizo` (129 cm with its stone, 78 px here). Round twenty-one's
    shape, every measure kept (the scene's `jizo` and `jizohat` areas); painted again in washes: the stone graded, lit
    from the left, the bib a deep wet red, the hat's straw in the sun."""
    J = JIZO
    x, z, h = J["x"], J["z"], J["h"]
    k = kz(z)
    lit_c, mid_c, sh_c = thin(mixp(PRUSSIAN, OCHRE, 0.18), 0.52), thin(mixp(PRUSSIAN, OCHRE, 0.12), 0.36), lerp(thin(PRUSSIAN, 0.30), COBALT, 0.22)
    # the low stone it stands on
    L.poly([gp(x - 26, z - 18, 0), gp(x + 26, z - 18, 0), gp(x + 26, z - 18, 22), gp(x - 26, z - 18, 22)], lit_c, mid_c, g=(gp(x - 26, z - 18, 22), gp(x + 26, z - 18, 0)))
    L.poly([gp(x + 26, z - 18, 0), gp(x + 26, z + 18, 0), gp(x + 26, z + 18, 22), gp(x + 26, z - 18, 22)], sh_c, lerp(sh_c, PRUSSIAN, 0.15))
    L.poly([gp(x - 26, z - 18, 22), gp(x + 26, z - 18, 22), gp(x + 26, z + 18, 22), gp(x - 26, z + 18, 22)], thin(mixp(PRUSSIAN, OCHRE, 0.2), 0.62))
    for (fx_, fy_) in ((-14, 8), (6, 14), (18, 5)):                                     # lichen on the old stone
        q = gp(x + fx_, z - 18, fy_)
        L.ellipse(q[0], q[1], 2.0 * k * 4, 1.2 * k * 4, thin(mixp(OCHRE, VERONESE, 0.4), 0.45), alpha=0.6)
    b0, b1 = 22.0, 22.0 + 62.0
    body = []
    for u in np.linspace(0, 1, 9):
        body.append(gp(x - (19 - 6 * u ** 1.6), z - 6, b0 + (b1 - b0) * u))
    for u in np.linspace(1, 0, 9):
        body.append(gp(x + (19 - 6 * u ** 1.6), z - 6, b0 + (b1 - b0) * u))
    L.poly(body, lit_c, mid_c, g=(gp(x - 19, z - 6, b1), gp(x + 19, z - 6, b0)))
    L.glaze([p for p in body if p[0] >= gp(x + 3, z - 6)[0]] + [gp(x + 3, z - 6, b0)], SHADE, 0.85)
    L.line([gp(x - 3, z - 7, b0 + 36), gp(x + 1, z - 7, b0 + 48)], lerp(sh_c, PRUSSIAN, 0.25), max(1.0, 4.5 * k), 0.85)      # the joined hands
    L.line([gp(x - 14, z - 7, b0 + 4), gp(x + 14, z - 7, b0 + 4)], lerp(sh_c, PRUSSIAN, 0.15), 0.6, 0.5)                     # the robe's hem
    hc = gp(x, z - 6, b1 + 13)
    L.ellipse(hc[0], hc[1], 13 * k, 13.5 * k, lit_c, mid_c, g=((hc[0] - 9 * k, hc[1] - 9 * k), (hc[0] + 9 * k, hc[1] + 9 * k)))
    L.ellipse(hc[0] + 5 * k, hc[1] + 1 * k, 7 * k, 12 * k, sh_c, alpha=0.75)
    L.ellipse(hc[0] - 2 * k, hc[1] + 1 * k, 7 * k, 10 * k, lit_c, alpha=0.8)
    for dx_ in (-4.5, 3.5):
        L.line([(hc[0] + dx_ * k - 1.6 * k, hc[1] + 1.5 * k), (hc[0] + dx_ * k + 1.6 * k, hc[1] + 1.8 * k)], lerp(sh_c, PRUSSIAN, 0.3), 0.6, 0.7)
    bib = [gp(x - 15, z - 8, b1 + 1), gp(x + 15, z - 8, b1 + 1), gp(x + 13, z - 8, b1 - 18), gp(x, z - 8, b1 - 27), gp(x - 13, z - 8, b1 - 18)]
    L.poly(bib, lerp(RED_BIB, VERMILION, 0.15), lerp(RED_BIB, LAKE, 0.15), g=(gp(x - 12, z - 8, b1), gp(x + 10, z - 8, b1 - 22)))
    L.glaze([gp(x + 6, z - 8, b1 + 1), gp(x + 15, z - 8, b1 + 1), gp(x + 13, z - 8, b1 - 18), gp(x + 6, z - 8, b1 - 24)], lerp(rgb("#ffffff"), LAKE, 0.35), 0.8)
    L.line([gp(x - 15, z - 8, b1 + 1), gp(x + 15, z - 8, b1 + 1)], lerp(RED_BIB, PRUSSIAN, 0.45), max(0.8, 2.4 * k), 0.9)
    hat_y = b1 + 24
    hat = [gp(x - 23, z - 6, hat_y - 1), gp(x + 23, z - 6, hat_y - 3), gp(x + 3, z - 6, h)]
    L.poly(hat, thin(mixp(OCHRE, NAPLES, 0.35), 0.35), thin(mixp(OCHRE, SIENNA, 0.2), 0.12), g=(hat[2], hat[1]))
    L.glaze([gp(x + 1, z - 6, hat_y - 2), gp(x + 22, z - 6, hat_y - 3), gp(x + 3, z - 6, h)], SHADE_WARM, 0.9)
    for v in (0.35, 0.65):
        a = gp(x - 22 + 22 * v, z - 6, hat_y - 1 + (h - hat_y) * v)
        b = gp(x + 22 - 19 * v, z - 6, hat_y - 3 + (h - hat_y) * v)
        L.line([a, b], lerp(OCHRE, PRUSSIAN, 0.4), 0.6, 0.5)
    L.line([gp(x - 8, z - 7, hat_y - 2), gp(x - 6, z - 7, b1 + 4)], lerp(OCHRE, PRUSSIAN, 0.3), 0.5, 0.6)              # the tie under the chin
    L.line([gp(x + 7, z - 7, hat_y - 3), gp(x + 5, z - 7, b1 + 4)], lerp(OCHRE, PRUSSIAN, 0.3), 0.5, 0.6)
    row = gp(x, z)[1]
    keyline(L, [hat[0], hat[2]], row, seed=1, alpha=0.32)
    keyline(L, [hat[1]] + body[9:] + [body[0]], row, seed=2, alpha=0.40)
    keyline(L, [gp(x + 26, z - 18, 22), gp(x + 26, z + 18, 22), gp(x + 26, z + 18, 0), gp(x - 26, z - 18, 0)], row, seed=3, alpha=0.4)
    info["jizo_box"] = [int(gp(x - 26, z)[0]) - 2, int(gp(x, z, h)[1]) - 2, int(52 * k) + 4, int(gp(x, z - 18)[1] - gp(x, z, h)[1]) + 4]
    info["hat_box"] = [int(gp(x - 24, z)[0]) - 1, int(gp(x, z - 6, h)[1]) - 2, int(48 * k) + 2, int(gp(x, z - 6, hat_y - 4)[1] - gp(x, z - 6, h)[1]) + 3]
    info["hat_pts"] = hat


def stone(L, info):
    """O-Shige's stone at the road's far edge: a flat-topped boulder travellers rest on (round twenty-one's outline: the
    scene's `blocked` patch), painted again: its worn top in the sun, its front lit, its right side in shade, lichen."""
    S = SEAT
    x, z, w, d, h = S["x"], S["z"], S["w"], S["d"], S["h"]
    k = kz(z)
    c = gp(x, z - d / 2, h * 0.5)
    rx_, ry_ = w / 2 * k, h * 0.55 * k
    outline = []
    for a in np.linspace(0, 2 * math.pi, 28, endpoint=False):
        wob = 1 + 0.06 * math.sin(3 * a + 1.2) + 0.04 * math.sin(5 * a)
        yy = math.sin(a)
        flat_top = 0.78 if yy < -0.55 else 1.0
        outline.append((c[0] + math.cos(a) * rx_ * wob, c[1] + yy * ry_ * wob * flat_top))
    outline = [(px_, min(py_, gp(x, z - d / 2)[1] + 1)) for px_, py_ in outline]
    L.poly(outline, thin(mixp(PRUSSIAN, OCHRE, 0.20), 0.46), thin(mixp(PRUSSIAN, SIENNA, 0.25), 0.22), g=((c[0] - rx_, c[1] - ry_), (c[0] + rx_ * 0.6, c[1] + ry_)))
    L.glaze([(px_, py_) for px_, py_ in outline if px_ >= c[0] + rx_ * 0.25] + [(c[0] + rx_ * 0.25, c[1] + ry_)], SHADE, 0.9)
    top = [(c[0] + math.cos(a) * rx_ * 0.82, c[1] - ry_ * 0.62 + math.sin(a) * ry_ * 0.22) for a in np.linspace(0, 2 * math.pi, 20)]
    L.poly(top, thin(mixp(PRUSSIAN, OCHRE, 0.25), 0.64), thin(mixp(PRUSSIAN, OCHRE, 0.20), 0.50))
    rng = np.random.default_rng(5)
    for i in range(6):
        a = rng.uniform(0.3, 2.8)
        L.ellipse(c[0] - math.cos(a) * rx_ * 0.6, c[1] + math.sin(a) * ry_ * 0.3, rng.uniform(1.5, 3.5), rng.uniform(1.0, 2.0), thin(mixp(OCHRE, VERONESE, 0.45), 0.42), alpha=0.6)
    L.line([(c[0] - rx_ * 0.2, c[1] - ry_ * 0.2), (c[0] + rx_ * 0.1, c[1] + ry_ * 0.6)], lerp(STONE_SHADE, PRUSSIAN, 0.3), 0.7, 0.45)
    row = gp(x, z)[1]
    keyline(L, [p for p in outline if p[1] > c[1] - ry_ * 0.2] + [outline[0]], row, seed=4, alpha=0.4)
    info["stone_box"] = [int(gp(x - w / 2, z)[0]) - 2, int(gp(x, z, h + 2)[1]) - 2, int(w * kz(z)) + 4, int(gp(x, z - d / 2)[1] - gp(x, z, h + 2)[1]) + 4]


def tuft_w(L, px_, py_, k, r, seed, tall=22.0, lean=-0.45, straw=0.12):
    """A tuft of coarse grass at the road's edge: a fan of blades bent over to the left by the wind, darker at the foot,
    the tips lighter on the left, now and then a blade of last year's straw; its little shadow to the right."""
    rng = np.random.default_rng(seed)
    dark = thin(lerp(mixp(VIRIDIAN, OCHRE, 0.36), PRUSSIAN, 0.18), 0.04)
    mid_ = thin(mixp(VIRIDIAN, VERONESE, 0.5), 0.10)
    lit_c = thin(mixp(VERONESE, OCHRE, 0.40), 0.26)
    straw_c = thin(mixp(OCHRE, NAPLES, 0.30), 0.30)
    hgt = tall * (0.6 + 0.8 * r) * k
    if hgt < 1.0:
        return
    L.ellipse(px_ + hgt * 0.6, py_ + 0.4, hgt * 0.8, max(0.5, hgt * 0.15), mixp(PRUSSIAN, COBALT, 0.4), alpha=0.22)
    n = 5 + int(r * 6)
    for j in range(n):
        an = lean + rng.uniform(-0.5, 0.45)
        ln = hgt * rng.uniform(0.55, 1.0)
        tip = (px_ + math.sin(an) * ln, py_ - math.cos(an) * ln * 0.9)
        mid = (px_ + math.sin(an) * ln * 0.40 - 0.4, py_ - math.cos(an) * ln * 0.55)
        q = rng.random()
        c = straw_c if q < straw else (lit_c if (an < -0.25 and q > 0.7) else (mid_ if q > 0.45 else dark))
        L.taper([(px_ + rng.normal(0, hgt * 0.08), py_), mid, tip], c, max(0.6, hgt * 0.09), 0.3, alpha=0.92)


def bank_grass(B, seed):
    """The bank's turf: fine grass all over it, combed to the left by the wind off the sea, green with the spring in it
    and last year's straw low down; thicker and longer along its crest, where the blades stand against the drop; a
    few flowers of the season (a speck of yellow, a speck of violet) at its foot."""
    rng = np.random.default_rng(seed)
    jx = gp(JIZO["x"], JIZO["z"])[0]
    greens = (thin(mixp(VERONESE, VIRIDIAN, 0.45), 0.16), thin(mixp(VERONESE, NAPLES, 0.25), 0.30), lerp(mixp(VIRIDIAN, OCHRE, 0.30), PRUSSIAN, 0.12),
              thin(mixp(VIRIDIAN, VERONESE, 0.3), 0.06))
    straw = thin(mixp(OCHRE, NAPLES, 0.35), 0.34)
    for i in range(5200):
        xx = rng.uniform(-4, 804)
        if abs(xx - jx) < 15 and rng.random() < 0.85:
            continue
        top_ = bank_top(xx)
        far_ = road_far(xx)
        f = rng.random() ** 1.6                                                   # most of them toward the crest
        row = top_ + 1.0 + f * (far_ - top_)
        k = kz(BANK["z1"] - (BANK["z1"] - BANK["z0"]) * f)
        ln = rng.uniform(6, 16) * k * (1.3 if f < 0.12 else 1.0)
        an = rng.uniform(-1.15, -0.25)
        tip = (xx + math.sin(an) * ln, row - math.cos(an) * ln)
        c = straw if rng.random() < 0.10 + 0.25 * f else greens[int(rng.random() * len(greens))]
        B.line([(xx, row), (xx + math.sin(an) * ln * 0.45, row - math.cos(an) * ln * 0.6), tip], c, max(0.6, 1.4 * k), 0.85)
    for i in range(26):                                                           # flowers of the season, very few
        xx = rng.uniform(10, 790)
        if abs(xx - jx) < 20:
            continue
        row = road_far(xx) - rng.uniform(1, 9)
        B.ellipse(xx, row, 0.9, 0.7, thin(NAPLES, 0.05) if i % 3 else thin(mixp(LAKE, ULTRA, 0.5), 0.35), alpha=0.95)


def shrub(B, sx_, row, w_, h_, seed):
    """A low shrub on the bank, pruned flat by the wind and streaming left: a mound of small leaves, dark beneath and
    on the right, the sun on its top and left, a few twigs at its windward end."""
    rng = np.random.default_rng(seed)
    dark, mid_, lit_ = lerp(mixp(VIRIDIAN, PRUSSIAN, 0.50), SIENNA, 0.05), mixp(VIRIDIAN, PRUSSIAN, 0.26), thin(mixp(VERONESE, OCHRE, 0.28), 0.16)
    for j in range(int(w_ * h_ * 0.5) + 12):
        u = rng.random() ** 0.8
        px_ = sx_ + w_ * (0.5 - u * 1.4)
        top = h_ * (1 - (2 * u - 0.6) ** 2 * 0.8)
        py_ = row - rng.random() ** 0.7 * top
        s = rng.uniform(1.0, 2.2)
        hi = (row - py_) / max(h_, 1)
        c = lit_ if (hi > 0.65 and rng.random() < 0.7) else (mid_ if rng.random() < 0.5 else dark)
        B.ellipse(px_, py_, s * 1.3, s * 0.8, c, alpha=0.95)
    for j in range(3):
        a0 = (sx_ + w_ * 0.45, row - rng.uniform(1, h_ * 0.6))
        B.line([a0, (a0[0] + rng.uniform(2, 5), a0[1] - rng.uniform(1, 3))], mixp(SIENNA, PRUSSIAN, 0.5), 0.7, 0.8)
    keyline(B, [(sx_ - w_ * 0.9, row - h_ * 0.2), (sx_ - w_ * 0.2, row + 1), (sx_ + w_ * 0.5, row)], row, seed=seed, alpha=0.3)


def ground_things(pic, info, seed):
    """What lies on the road and grows at its edges, at a true density for each square metre (depth.scatter), big and few
    near us, small and many toward the bank: gravel and stones with their little shadows to the right, the dents of
    straw sandals along the worn tracks, a packhorse's hoofprints, tufts along both edges; the bank's turf combed by
    the wind, and the wind-pruned shrubs on it."""
    x, y = grid(SHAPE)
    X, Z, below = floor()
    road = info["road"] > 0.5
    fars = FARS[None, :]
    u = np.clip((y - fars) / np.maximum(600.0 - fars, 6.0), 0, 1)
    G = Wet(SHAPE)
    dent = thin(mixp(OCHRE, PRUSSIAN, 0.5), 0.40)
    for i, c in enumerate((0.17, 0.46, 0.77)):
        for (px_, py_, k, r) in D.scatter(PT, PX, (-700, 700, -40, 440), 0.9, seed + 10 + i, size=(9, 22), zone=road & (np.abs(u - c) < 0.035), most=260):
            rx = 4.5 * k
            ry = max(0.35, 11.0 * k * squash(py_) * 1.2)
            G.ellipse(px_, py_, rx, ry, dent, alpha=(0.18 + 0.2 * r) * min(1.0, 0.4 + k))
    for (px_, py_, k, r) in D.scatter(PT, PX, (-700, 700, 140, 330), 0.25, seed + 14, size=(13, 13), zone=road & (np.abs(u - 0.33) < 0.06), most=40):
        rx = 6.0 * k
        ry = max(0.4, 7.0 * k * squash(py_) * 1.6)
        G.ellipse(px_, py_, rx, ry, dent, alpha=0.32)
    rough = road & ((np.minimum(np.minimum(np.abs(u - 0.17), np.abs(u - 0.46)), np.abs(u - 0.77)) > 0.06) | (u < 0.05) | (u > 0.92))
    tones = (thin(mixp(PRUSSIAN, OCHRE, 0.34), 0.50), thin(mixp(PRUSSIAN, SIENNA, 0.30), 0.40), thin(mixp(OCHRE, PRUSSIAN, 0.40), 0.36), thin(mixp(PRUSSIAN, OCHRE, 0.20), 0.34))
    for (zone, per, size, sd) in ((road, 2.5, (2.0, 5.0), 20), (rough, 3.5, (3.0, 9.0), 21), (rough & ((u < 0.07) | (u > 0.9)), 2.0, (5.0, 16.0), 22),
                                  (rough & (u > 0.25), 0.35, (8.0, 18.0), 23)):
        for (px_, py_, k, r) in D.scatter(PT, PX, (-700, 700, -40, 440), per, seed + sd, size=(size[1], size[1] * 0.6), zone=zone, most=2400):
            s = (size[0] + (size[1] - size[0]) * r * r) * k * 0.5
            if s < 0.3:
                continue
            ry = s * (0.45 + 0.5 * squash(py_))
            c = tones[int(r * 977) % len(tones)]
            G.ellipse(px_ + s * 0.9, py_ + ry * 0.35, s * 1.25, max(0.4, ry * 0.7), mixp(PRUSSIAN, COBALT, 0.45), alpha=0.30)
            G.ellipse(px_, py_ - ry * 0.5, s, max(0.45, ry), thin(c, 0.36), lerp(c, PRUSSIAN, 0.22), g=((px_ - s, py_ - ry), (px_ + s * 0.5, py_ + ry)))
    over(pic, G.c, G.a * info["ground"])
    # tufts: along the bank's foot and the road's near edge, a few in the rough between the tracks
    R_ = Wet(SHAPE)
    edge_far = road & (u < 0.06)
    edge_near = road & (u > 0.90)
    tufts = D.scatter(PT, PX, (-700, 700, -40, 440), 1.4, seed + 30, size=(24, 30), zone=edge_far, most=300)
    tufts += D.scatter(PT, PX, (-700, 700, -40, 440), 0.8, seed + 31, size=(24, 30), zone=edge_near, most=200)
    tufts += D.scatter(PT, PX, (-700, 700, -40, 440), 0.08, seed + 32, size=(20, 26), zone=rough & (u > 0.08) & (u < 0.9), most=60)
    tufts = [t_ for t_ in tufts if not (350 < t_[0] < 420 and t_[1] < 500)]                  # (clear of the Jizo's feet)
    tufts.sort(key=lambda p: p[1])
    for i, (px_, py_, k, r) in enumerate(tufts):
        tuft_w(R_, px_, py_, k, r, seed + 100 + i)
    R_.onto(pic)
    # the bank: its turf combed by the wind, the shrubs on it
    B = Wet(SHAPE)
    bank_grass(B, seed + 400)
    for i, (sx_, w_, h_) in enumerate(SHRUBS):
        shrub(B, sx_, bank_top(sx_) + 3, w_, h_, seed + 600 + i)
    bc, ba = B.done()
    bc, ba = hand(bc, ba, seed + 7)
    over(pic, bc, np.clip(ba, 0, 1))
    return pic


def details(pic, info, seed=SEED, fast=False):
    """The crisp things of the backdrop, wet on dry, far to near. -> the backdrop."""
    x, y = grid(SHAPE)
    # ================ the far things (still no line: they are a kilometre off and more)
    F = Wet(SHAPE)
    FAR.far_stretch_things(F, info, seed + 50)
    FAR.yui_town(F, seed + 51)
    FAR.okitsu_town(F, seed + 52)
    FAR.flank_things(F, info, seed + 53)
    FAR.old_shore(F, seed + 54)
    FAR.boats(F, seed + 55)
    fc, fa = F.done()
    fc, fa = hand(fc, fa, seed + 3, amount=0.45)
    over(pic, fc, np.clip(fa, 0, 1) * (1 - info["bank"]))
    # ================ the ground and what stands on it
    info["shadow"] = cast_shadows(pic, info, seed)
    ground_things(pic, info, seed + 200)
    L = Wet(SHAPE)
    stone(L, info)
    jizo(L, info)
    lc, la = L.done()
    lc, la = hand(lc, la, seed + 5, amount=0.35)
    over(pic, lc, np.clip(la, 0, 1))
    return pic


# ================================================================ the cut-outs
def cloud_cut(back, seed, fast=False):
    """Fuji's cap of cloud (on / lifted: the scene fades it), round twenty-one's outline exactly (the scene's `cloud`
    area), painted again in washes: bare paper where the sun is on it, a thin grey-blue underneath, and at its edge it
    takes the colour of what is behind it, so its outline melts into the sky as wet paint does."""
    a, outline = old_cloud()
    x, y = grid(SHAPE)
    ys, xs = np.where(a > 0.5)
    top_of = np.full(W, 9999.0, dtype=F32)
    bot_of = np.full(W, -1.0, dtype=F32)
    np.minimum.at(top_of, xs, ys.astype(F32))
    np.maximum.at(bot_of, xs, ys.astype(F32))
    v = np.clip((y - top_of[None, :]) / np.maximum(bot_of - top_of, 1.0)[None, :], 0, 1)
    shade = thin(mixp(COBALT, SIENNA, 0.14), 0.62)
    c = ramp(v, [(0.0, WPAPER), (0.42, WPAPER), (0.70, thin(mixp(COBALT, SIENNA, 0.10), 0.80)), (1.0, shade)])
    c *= (1 + (noise(SHAPE, (26, 9), seed + 1, 3) - 0.5)[..., None] * 0.05)
    inner = blur(a, 2.2)
    feather = np.clip((inner - 0.5) * 2.6, 0, 1) ** 1.2
    c = lerp(back, c, feather[..., None])
    return np.clip(c, 0, 1).astype(F32), a, outline


def pine_cut(back, seed, fast=False):
    """The bent pine on the bank's edge at the right, leaning toward Fuji (bent by the wind off the sea): round
    twenty-one's outline exactly (the scene's `pine` area, its base 475), painted again: the trunk in old bark, warm in
    the sun on its upper left, cool beneath; each pad of needles a graded wash, lit along its top and left, dark and cool
    underneath, combed to the left by the wind; a quiet broken key line only under the pads and on the shaded side. It
    sways (fx pine-sway, rooted at its foot)."""
    a, trunk, branches, stub, pads = old_pine()
    L = Wet(SHAPE)
    rng = np.random.default_rng(seed)
    k = kz(PINE["z"])
    bark_d, bark_m, bark_l = mixp(SIENNA, PRUSSIAN, 0.74), lerp(mixp(SIENNA, PRUSSIAN, 0.62), COBALT, 0.10), lerp(thin(mixp(SIENNA, OCHRE, 0.30), 0.30), PRUSSIAN, 0.12)
    needle_d, needle_m, needle_l = lerp(mixp(VIRIDIAN, PRUSSIAN, 0.60), SIENNA, 0.06), mixp(VIRIDIAN, PRUSSIAN, 0.34), thin(mixp(VERONESE, OCHRE, 0.25), 0.12)
    L.add(np.broadcast_to(needle_d, SHAPE + (3,)).astype(F32), a)                  # (anything of the old outline not drawn again: dark needles)
    L.taper(trunk, bark_m, 30 * k, 10 * k)
    for b in branches:
        L.taper(b, bark_m, 10 * k, 4 * k)
    L.taper(stub, bark_m, 6 * k, 3 * k)
    L.taper([(p[0] + 2.4, p[1] + 1.0) for p in trunk[:-1]], bark_d, 13 * k, 4 * k, alpha=0.9)
    L.taper([(p[0] - 2.2, p[1] - 1.2) for p in trunk[:-1]], bark_l, 7 * k, 2.5 * k, alpha=0.8)
    for i in range(len(trunk) - 1):                                                  # the bark's plates, and the cracks between
        for _ in range(14):
            f = rng.random()
            off = rng.normal(0, 4.5 * k)
            p0 = (trunk[i][0] + (trunk[i + 1][0] - trunk[i][0]) * f + off, trunk[i][1] + (trunk[i + 1][1] - trunk[i][1]) * f)
            c_ = bark_d if off > -1.0 else lerp(bark_l, bark_m, 0.5)
            L.line([p0, (p0[0] + rng.normal(0, 0.8), p0[1] + rng.uniform(2, 5))], c_, rng.uniform(0.6, 1.1), 0.7)
    for (cx, cy, rx, ry) in sorted(pads, key=lambda p: -p[1]):
        top, bot = [], []
        m = 22
        for j in range(m + 1):
            u = j / m
            xx = cx - rx + 2 * rx * u
            s_ = math.sin(math.pi * u)
            top.append((xx, cy - ry * s_ ** 0.6))
            bot.append((xx, cy + ry * 0.35 * s_ ** 1.5))
        L.poly(top + bot[::-1], needle_m, needle_d, g=((cx - rx * 0.4, cy - ry), (cx + rx * 0.3, cy + ry * 0.35)))
        lt = [(px - rx * 0.06, py + (b[1] - py) * 0.10) for (px, py), b in zip(top, bot)]
        md = [(px - rx * 0.06, py + (b[1] - py) * (0.42 + 0.12 * math.sin(px * 0.7))) for (px, py), b in zip(top, bot)]
        L.poly(lt[: m // 2 + 5] + md[: m // 2 + 5][::-1], needle_l, needle_m, g=((cx - rx, cy - ry), (cx, cy)), alpha=0.85)
        for j in range(int(rx * ry / 2.2)):                                         # the needles all over it, combed to the left
            u = rng.random()
            px = cx - rx * 0.95 + 2 * rx * 0.95 * u
            hi = cy - ry * math.sin(math.pi * u) ** 0.6
            lo = cy + ry * 0.33 * math.sin(math.pi * u) ** 1.5
            v_ = rng.random()
            py = hi + (lo - hi) * v_
            c_ = needle_l if (v_ < 0.3 and u < 0.65 and rng.random() < 0.6) else (needle_d if v_ > 0.55 else needle_m)
            L.line([(px, py), (px - rng.uniform(1.6, 3.6), py + rng.uniform(0.3, 1.8))], c_, rng.uniform(0.6, 0.9), 0.9)
        for j in range(int(rx / 1.4)):                                              # the comb of needle ends along its underside
            u = (j + rng.random()) / int(rx / 1.4)
            px = cx - rx * 0.92 + 2 * rx * 0.92 * u
            py = cy + ry * 0.33 * math.sin(math.pi * u) ** 1.5
            L.line([(px, py - 1.2), (px - rng.uniform(1.0, 2.6), py + rng.uniform(1.0, 2.4))], needle_d, 0.8, 0.9)
        keyline(L, bot, cy + ry, seed=int(cx), alpha=0.42)
    keyline(L, [(p[0] + 15 * k, p[1]) for p in trunk], trunk[0][1], seed=7, color=mixp(SIENNA, PRUSSIAN, 0.7), alpha=0.42)
    # the bank's grass in front of its foot, so it stands in the turf and not on it
    foot = gp(PINE["x"], PINE["z"])
    for j in range(22):
        bx = foot[0] + rng.uniform(-12, 12)
        by = foot[1] + rng.uniform(-1, 1.5)
        ln = rng.uniform(5, 10)
        an = rng.uniform(-1.1, -0.3)
        L.line([(bx, by), (bx + math.sin(an) * ln * 0.5, by - math.cos(an) * ln * 0.6), (bx + math.sin(an) * ln, by - math.cos(an) * ln)],
               thin(mixp(VERONESE, VIRIDIAN, 0.45), 0.14) if j % 3 else thin(mixp(OCHRE, NAPLES, 0.35), 0.32), 1.0, 0.95)
    c, la_ = L.done()
    c = grade_cut(c, a, 0.93, seed=seed)
    # the outline stays round twenty-one's exactly, but the pads are needles, not lenses: along their tops the sky shows
    # between the needle tufts (painted inside the outline: the colour behind them), and the tufts that face the sun are
    # lit; at its foot the trunk goes down into the bank's grass (the colour of the bank there, and blades over it)
    x, y = grid(SHAPE)
    ys, xs = np.where(a > 0.5)
    inner = blur(a, 1.3)
    gy = np.gradient(blur(a, 1.0), axis=0)
    upper = np.clip(gy * 3.0, 0, 1)                                                  # the outline's upper edges
    tufts = step(0.48, 0.62, noise(SHAPE, (3.2, 2.0), seed + 21, 2))
    notch = np.clip((1.0 - (inner - 0.5) * 2.2), 0, 1) * upper * tufts * (y < gp(PINE["x"], PINE["z"])[1] - 60)
    lit_t = np.clip((1.0 - (inner - 0.5) * 3.0), 0, 1) * upper * (1 - tufts) * step(0.5, 0.7, noise(SHAPE, (6, 3), seed + 22, 2)) * (x < 640)
    c = lerp(c, np.clip(c * 1.6 + np.array([0.10, 0.12, 0.02], dtype=F32), 0, 1), (lit_t * 0.7)[..., None])
    c = lerp(c, back, (np.clip(notch, 0, 1) * 0.9)[..., None])
    footy = gp(PINE["x"], PINE["z"])[1]
    sink = np.clip((y - (footy - 5)) / 5.0, 0, 1) * (np.abs(x - gp(PINE["x"], PINE["z"])[0]) < 30)
    grassy = step(0.42, 0.58, noise(SHAPE, (1.6, 6.0), seed + 23, 2))
    c = lerp(c, back, (sink * (0.55 + 0.45 * grassy))[..., None])
    return c.astype(F32), a


def pass_cut(back, seed, fast=False):
    """O-Shige's pass, folded in oiled paper, caught on the Jizo's little hat (on / gone): round twenty-one's outline
    exactly, painted again: an amber packet, the oiled paper's sheen on its upper left, the fold across it, a white
    edge of the paper inside showing. -> (colour, cover, its corners)."""
    a, quad, rot, w, h = pass_geom()
    L = Wet(SHAPE)
    L.add(np.broadcast_to(thin(mixp(OCHRE, SIENNA, 0.2), 0.30), SHAPE + (3,)).astype(F32), a)
    L.poly(quad, thin(mixp(OCHRE, NAPLES, 0.35), 0.30), mixp(OCHRE, SIENNA, 0.30), g=(rot(-w / 2, -h / 2), rot(w / 2, h / 2)))
    L.poly([rot(-w / 2, h * 0.18), rot(w / 2, h * 0.18), rot(w / 2, h / 2), rot(-w / 2, h / 2)], mixp(OCHRE, SIENNA, 0.35), mixp(SIENNA, PRUSSIAN, 0.25))
    L.poly([rot(-w / 2 + 1, -h / 2 - 1.5), rot(w / 2 - 3, -h / 2 - 1.5), rot(w / 2 - 3, -h / 2), rot(-w / 2 + 1, -h / 2)], WPAPER)
    L.line([rot(-w / 2 + 2, -h / 2 + 1.2), rot(w / 2 - 4, -h / 2 + 1.0)], WPAPER, 0.7, 0.6)                       # the sheen of the oil
    L.line([rot(-w / 2, h * 0.18), rot(w / 2, h * 0.18)], mixp(SIENNA, PRUSSIAN, 0.45), 0.7, 0.75)
    L.line([rot(w / 2, -h / 2), rot(w / 2, h / 2), rot(-w / 2, h / 2)], mixp(SIENNA, PRUSSIAN, 0.55), 0.6, 0.6)
    c, _ = L.done()
    return c.astype(F32), a, quad


# ================================================================ the finish
def to_file(picture, name, colors=128, alpha=None, seed=7, speckle=0.010, amount=0.010):
    """Pigment grain (little: the wash has its own granulation), then a limited palette with speckle: an 8-bit PNG."""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def finish_all(pic, planes, counts, info, out=OUT):
    """THE WATERCOLOUR FINISH (DEPTH.md; Yui's finish_all): the backdrop washed (watercolor.wash, `soft` the wet map:
    edo_satta_far.wet_mask), every cut-out washed over the unwashed backdrop with the same seed (wash_cut, crisp: the soft
    mask taken away under it and 2 px round it), so the paper is one sheet; then the palette."""
    soft = FAR.wet_mask(info)
    back_washed = WC.wash(pic, seed=SEED, soft=soft, wander=2.0)
    sizes = {"back": to_file(back_washed, out + "/back.png", 250)}
    for name, n in counts:
        c, a = planes[name][:2]
        washed = WC.wash_cut(c, (a > 0.5).astype(F32), pic, seed=SEED, soft=soft, wander=2.0, crisp=True, fleck=0.2 if name in ("near", "front") else 0.5)
        planes[name] = (washed, a) + tuple(planes[name][2:])
        sizes[name] = to_file(washed, out + f"/{name}.png", n, a)
    return back_washed, sizes


def comp_all(pic, planes, order=ORDER):
    whole = pic.copy()
    for name in order:
        c, a = planes[name][:2]
        over(whole, c, (a > 0.5).astype(F32))
    return whole


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = "fast" in sys.argv
    base, info = under()
    Image.fromarray((np.clip(base, 0, 1) * 255).astype(np.uint8)).save(OUT + "-1-under.png")
    print("under", round(time.time() - t0, 1))
    if fast:
        pic = base.copy()
    else:
        # the brush pass, light: the far plane stays as the wet washes left it, the ground is half brushed
        brushed_ = strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.02, keep=0.0)
        keep = np.clip(0.50 + 0.38 * FAR.wet_mask(info), 0, 0.92)
        pic = lerp(brushed_, base, keep[..., None]).astype(F32)
    print("brushed", round(time.time() - t0, 1))
    details(pic, info, fast=fast)
    print("details", round(time.time() - t0, 1))
    planes = {}
    c, a, info["cloud_outline"] = cloud_cut(pic, 11, fast)
    planes["cloud"] = (c, a)
    planes["pine"] = pine_cut(pic, 12, fast)
    c, a, info["pass_quad"] = pass_cut(pic, 13, fast)
    planes["pass"] = (c, a)
    planes["front"] = NEAR.front_cut(pic, 14, fast)
    planes["near"] = NEAR.near_cut(pic, 15, fast)
    Image.fromarray((np.clip(comp_all(pic, planes, ["cloud", "pine", "pass", "front", "near"]), 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-all.png")
    Image.fromarray((np.clip(comp_all(pic, planes, ["pine", "front", "near"]), 0, 1) * 255).astype(np.uint8)).save(OUT + "-3-clear.png")
    import edo_satta_layout
    with open(OUT + "/layout.json", "w") as f:
        json.dump(edo_satta_layout.layout(planes, info), f, indent=1)
    print("painted", round(time.time() - t0, 1))
    if "wash" in sys.argv or not fast:
        counts = (("cloud", 24), ("pine", 64), ("pass", 16), ("front", 96), ("near", 128))
        target = OUT if not fast else OUT + "-fast"
        os.makedirs(target, exist_ok=True)
        if fast:
            with open(target + "/layout.json", "w") as f:
                json.dump(edo_satta_layout.layout(planes, info), f, indent=1)
        back_washed, sizes = finish_all(pic, planes, counts, info, target)
        print(sizes)
        comp = Image.open(target + "/back.png").convert("RGBA")
        for name in ["cloud", "pine", "pass", "front", "near"]:
            comp.alpha_composite(Image.open(f"{target}/{name}.png").convert("RGBA"))
        comp.convert("RGB").save(OUT + ("-comp.png" if not fast else "-fast-comp.png"))
    print("done", round(time.time() - t0, 1))

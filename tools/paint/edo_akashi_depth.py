#!/usr/bin/env python3
"""ROUND 23, the fast depth pass: the Akashi shore (edo-akashi) given its three planes, over its own painting.

Reads edo_akashi.py's pictures as painted (out/edo-akashi-orig/: run the painter once and copy its folder there; never
changed) and writes the scene's whole set again into out/edo-akashi/: every file as before, plus near.png.

NEAR   (near.png, plane "front") A shore pine standing just off the picture at the right, nearer than the road and
       leaning in over us as the pines on this shore do: its trunk up the right edge (cut by the frame), its bough across
       the top with flat pads of needles, one pad over the corner. A bough of another pine hanging in at the top left.
       Along the bottom, the lip of the road's near bank with its grass: low where people walk on the road, higher in the
       two bottom corners. All in shade (the sun is to the right and a little ahead, 35 degrees up): deep warm darks, a
       warm rim on the edges that face the sun. It hides nothing clicked or stood on (depth_check.py).
BACK   The shade of the right pine's crown lying dappled on the road, and the shadow of a pine outside the picture at the
       right: its trunk's shadow leads in from the right edge across the road, its crown's shade beside it. The pots',
       Heita's boat's, the tub's and the rocks' shadows on the sand deepened, with contact shade at their feet. The tide's
       lines on the sand (the wrack line with its weed, an older line further up), shells and pebbles on the sand and
       stones on the road, through the camera (few and large near, many and small far). Awaji, the far shore and the
       castle's hill moved toward the sky's colour at the horizon; the near road a little deeper.
JAPAN  watercolor.wash(back, seed=1830, soft=WET, wander=1.4, fleck=0.3), WET: 1.0 the sky, 0.6 Awaji and the far hill,
       the strait 0.75 at the horizon to 0.2 near, 0 the sand, the road and the castle. Every cut-out and near.png
       wash_cut(..., crisp=True) on the same paper. The Awa boat's frame (boat-1.png) is copied as it was.

    python3 edo_akashi_depth.py         (light: about half a minute)
"""

import json
import math
import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import F32, Sheet, blur, grid, lerp, mask_line, mask_poly, noise, over, rgb, step, tint, grain, palette_of, to_palette, save
import depth
import watercolor
import edo_akashi as A
from edo_akashi_kit import (CAM, HZ, FULL, W, H, SUN, gp, kz, edge_pts, shadow_pts, Paper, PAPER, SAND, SAND_WET, EARTH, PINE, PINE_LIT,
                            PINE_DEEP, SIENNA, VIRIDIAN, VERONESE, PRUSSIAN, COBALT, NAPLES, OCHRE, WHITE, ULTRA)

ORIG = "out/edo-akashi-orig"
OUT = "out/edo-akashi"
SHAPE = (H, W)
WSEED = 1830
CUTS = ["floats", "ladle", "pilgrimboat", "pilgrimboat-beached", "heitaboat", "tub", "pots", "rocks", "pine-l", "pine-r", "front"]
COLORS = dict(A.COLORS)
COLORS["near"] = 64
LIGHT = (1.0, -0.75)                        # toward the sun in the picture: to the right and up


def load(name):
    a = np.asarray(Image.open(f"{ORIG}/{name}.png").convert("RGBA"), np.float32) / 255.0
    return a[..., :3].copy(), a[..., 3].copy()


def smooth_pts(pts, n=8):
    """A Catmull-Rom path through picture points (for a trunk's or a bough's line)."""
    p = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = [np.asarray(q, np.float64) for q in p[i - 1:i + 3]]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)))
    out.append(tuple(pts[-1]))
    return out


def band_poly(path, w0, w1):
    """The outline of a tapered band along a path (w0 wide at its start, w1 at its end)."""
    path = np.asarray(path, np.float64)
    left, right = [], []
    for i in range(len(path)):
        a, b = path[max(i - 1, 0)], path[min(i + 1, len(path) - 1)]
        d = b - a
        d = d / (np.hypot(*d) + 1e-9)
        nx, ny = -d[1], d[0]
        w = (w0 + (w1 - w0) * i / max(len(path) - 1, 1)) / 2
        left.append((path[i][0] + nx * w, path[i][1] + ny * w))
        right.append((path[i][0] - nx * w, path[i][1] - ny * w))
    return left + right[::-1]


# ================================================================ the masks of the place
def masks():
    x, y = grid(SHAPE)
    wm = A.water_region()
    aw, _ = A.awaji_mask(A.SEED)
    mh, _ = A.paint_far_left(np.zeros(SHAPE + (3,), F32), A.SEED, Paper(SHAPE))
    _, _, below = CAM.floor_grid(SHAPE)
    ground = np.clip(below * (1 - wm), 0, 1).astype(F32)
    R = A.ROAD
    road = mask_poly(SHAPE, [gp(-3000, R["z0"]), gp(3000, R["z0"]), gp(3000, R["z1"]), gp(-3000, R["z1"])], soft=1.0)
    sand = np.clip(ground * (1 - road), 0, 1)
    sand = sand * (y < gp(0, R["z1"] + 40)[1])                     # (beyond the grass lip at the road's seaward edge)
    castle = np.zeros(SHAPE, F32)
    castle[196:236, 0:84] = 1.0
    castle = np.clip(blur(castle, 3.0) * 1.6, 0, 1)
    sky = np.clip((1 - aw) * (1 - mh) * (1 - wm) * (1 - ground) * (y < HZ + 3), 0, 1)
    return dict(water=wm.astype(F32), awaji=aw.astype(F32), hill=mh.astype(F32), ground=ground, road=road.astype(F32), sand=sand.astype(F32),
                castle=castle, sky=sky.astype(F32))


def wet_map(m):
    x, y = grid(SHAPE)
    t = np.clip((y - HZ) / (470.0 - HZ), 0, 1)
    water = (0.75 - 0.55 * t) * m["water"]
    far = 0.6 * np.clip(m["awaji"] + m["hill"], 0, 1)
    wet = np.maximum(np.maximum(m["sky"] * 1.0, far), water)
    wet = wet * (1 - m["ground"]) * (1 - m["castle"])
    return np.clip(wet, 0, 1).astype(F32)


# ================================================================ the backdrop, deepened
def glaze(pic, mask, color="#5a5490", amount=1.0):
    """A shadow as a glaze: multiply toward a cool colour (1.5x it, as depth.shadow_on_ground does)."""
    c = rgb(color) * 1.5
    m = np.clip(mask * amount, 0, 1)[..., None]
    pic[...] = pic * (1 - m) + pic * c * m
    np.clip(pic, 0, 1, out=pic)


def disc_shadow(Xc, h, zc, r, squash=0.8, n=28):
    """The shadow on the ground of a flat pad of needles (a disc r cm across, h cm up): picture points."""
    return shadow_pts([(Xc + r * math.cos(t), h, zc + r * squash * math.sin(t)) for t in np.linspace(0, 2 * math.pi, n, endpoint=False)])


def pine_shade(m, seed):
    """The shade of the pines' crowns on the road and the sand: the right pine's own pads, and a pine outside the
    picture at the right (its trunk's shadow leading in from the right edge). Dappled: sun comes through in flecks."""
    crowns = Sheet(SHAPE)
    # the right shore pine's pads (from where they are in the picture: x, y -> X, h at its z)
    z0 = A.PINES[1]["z"]
    k = kz(z0)
    foot_y = gp(0, z0)[1]
    for (px, py, rx) in ((595, 57, 95), (740, 100, 60), (548, 170, 92), (750, 152, 50)):
        X, h, r = (px - 400) / k, (foot_y - py) / k, rx / k
        crowns.poly(disc_shadow(X, h, z0, r), "#000000", 1.0)
    # a pine outside the picture at the right, at the road's seaward edge like the two in it, leaning in
    bx, bz, lean = 760.0, 175.0, -0.25
    trunk = Sheet(SHAPE)
    trunk.poly(shadow_pts([(bx - 18, 0, bz), (bx + 18, 0, bz), (bx + lean * 520 + 13, 520, bz), (bx + lean * 520 - 13, 520, bz)]), "#000000", 1.0)
    for (dx, h, dz, r) in ((-150, 520, 30, 105), (-40, 600, -20, 125), (70, 560, 60, 95), (-250, 470, -40, 80)):
        crowns.poly(disc_shadow(bx + lean * h + dx, h, bz + dz, r), "#000000", 1.0)
    _, ca = crowns.done()
    _, ta = trunk.done()
    ca = blur(ca, 1.4)
    ta = blur(ta, 1.1)
    # flecks of sun through the needles: flattened by the ground's perspective
    fl = noise(SHAPE, (22, 7), seed, 3)
    holes = step(0.58, 0.64, fl)
    inner = step(0.30, 0.36, noise(SHAPE, (60, 18), seed + 1, 2))          # the shade is thinner here and there
    shade = ca * (1 - 0.85 * holes) * (0.75 + 0.25 * inner)
    whole = np.maximum(shade, ta * 0.95) * m["ground"]
    return whole.astype(F32)


def object_shadows(m):
    """The pots', the boats', the tub's and the rocks' shadows as the painter laid them (edo_akashi.cast_shadows):
    the same polygons, to deepen."""
    sh = Sheet(SHAPE)
    P_ = A.POTS
    sh.poly(shadow_pts([(P_["x0"], 0, P_["z0"]), (P_["x1"], 0, P_["z0"]), (P_["x1"], 60, P_["z1"]), (P_["x0"], 60, P_["z1"])]), "#000000", 1.0)
    b = A.HEITA_BOAT
    (sx, sz), (bx, bz) = b["stern"], b["bow"]
    sh.poly(shadow_pts([(sx, 0, sz), (bx, 0, bz), (bx, b["side"] + 20, bz), (sx, b["side"], sz)]), "#000000", 1.0)
    t = A.TUB
    sh.poly(shadow_pts([(t["x"] - t["r"], 0, t["z"]), (t["x"] + t["r"], 0, t["z"]), (t["x"] + t["r"], t["h"], t["z"]), (t["x"] - t["r"], t["h"], t["z"])]), "#000000", 1.0)
    for (rx, rz, rw, rh) in A.ROCKS:
        sh.poly(shadow_pts([(rx - rw, 0, rz), (rx + rw, 0, rz), (rx + rw * 0.4, rh, rz), (rx - rw * 0.5, rh, rz)]), "#000000", 1.0)
    _, a = sh.done()
    return (blur(a, 0.8) * m["ground"]).astype(F32)


def contact(alpha, dx=-3, dy=2, r=2.2):
    """Shade at a cut-out's feet, just outside its outline, on the side away from the sun."""
    a = (alpha > 0.5).astype(F32)
    sh = np.roll(np.roll(a, dy, axis=0), dx, axis=1)
    m = np.clip(blur(sh, r) * 1.4 - a, 0, 1)
    # only round its lower part (where it meets the ground)
    ys = np.where(a.max(axis=1) > 0)[0]
    if len(ys):
        y0, y1 = ys.min(), ys.max()
        x, y = grid(alpha.shape)
        m = m * np.clip((y - (y1 - (y1 - y0) * 0.35)) / 6.0, 0, 1)
    return m.astype(F32)


def tide_lines(pic, m, seed):
    """The tide's lines on the sand, along the water's edge: the wrack line (weed and shell, broken), and an older line
    further up, fainter; each thinner far off."""
    for off, wcm, col, amt, cell in ((165.0, 5.0, lerp(lerp(SIENNA, PRUSSIAN, 0.45), VIRIDIAN, 0.2), 0.42, (9, 3)),
                                     (300.0, 9.0, lerp(SAND_WET, SAND, 0.35), 0.30, (30, 6)),
                                     (420.0, 4.0, lerp(lerp(SIENNA, PRUSSIAN, 0.4), SAND, 0.35), 0.22, (14, 4))):
        pts = edge_pts(160, off)
        zs = [CAM.depth_at(p[1]) if p[1] > HZ + 1 else 1e5 for p in pts]
        ws = [max(0.45, kz(max(z_, -20.0)) * wcm) for z_ in zs]
        line = mask_line(SHAPE, pts, ws, soft=0.6)
        broken = step(0.42, 0.52, noise(SHAPE, cell, seed + int(off), 3))
        over(pic, col, (line * broken * amt * m["sand"]).astype(F32))


def scatter_bits(pic, m, seed):
    """Shells and pebbles on the sand, stones on the road: few and large near us, many and small far off."""
    pt = lambda X, Z: CAM.pt(X, 0, Z)
    px = lambda X, Z: CAM.scale(Z)
    sheet = Sheet(SHAPE)
    shell = lerp(WHITE, NAPLES, 0.25)
    pebble = lerp(lerp(PRUSSIAN, OCHRE, 0.35), SAND, 0.35)
    dark = lerp(SAND, COBALT, 0.5)
    for (x, y, k, r) in depth.scatter(pt, px, (-2600, 2600, -20, 1500), 0.9, seed, size=(5.0, 2.5), zone=m["sand"]):
        s = k * (2.5 + 3.5 * r)
        if r < 0.55:                                                   # a shell: light, its shadow to the left
            sheet.ellipse(x - s * 0.55, y + s * 0.12, s * 0.75, s * 0.35, dark, 0.45)
            sheet.ellipse(x, y, s * 0.7, s * 0.32, shell, 0.9)
        else:                                                          # a pebble
            sheet.ellipse(x, y, s * 0.55, s * 0.3, pebble, 0.75)
    for (x, y, k, r) in depth.scatter(pt, px, (-1200, 1200, -30, 150), 2.4, seed + 1, size=(6.0, 3.0), zone=m["road"]):
        s = k * (2.5 + 4.0 * r)
        sheet.ellipse(x - s * 0.5, y + s * 0.15, s * 0.7, s * 0.3, lerp(EARTH, COBALT, 0.45), 0.5)
        sheet.ellipse(x, y, s * 0.6, s * 0.3, lerp(lerp(EARTH, WHITE, 0.25), OCHRE, 0.15), 0.8)
    c, a = sheet.done()
    over(pic, c, (a * m["ground"]).astype(F32))
    # sand ripples: faint level streaks on the dry sand, closer together far off
    x, y = grid(SHAPE)
    Z = CAM.eye * CAM.F / np.maximum(y - HZ, 2.0) - CAM.Z0
    phase = np.sin((Z / 38.0 + (noise(SHAPE, (80, 30), seed + 3, 2) - 0.5) * 3.0) * 2 * math.pi)
    rip = step(0.75, 0.95, phase) * step(0.35, 0.6, noise(SHAPE, (120, 30), seed + 4, 2)) * np.clip((y - HZ - 30) / 100.0, 0, 1)
    tint(pic, lerp(SAND, COBALT, 0.25) / np.maximum(SAND, 1e-3), (rip * 0.16 * m["sand"]).astype(F32))


def deepen_back(back, cuts, m, seed=WSEED):
    pic = back.copy()
    x, y = grid(SHAPE)
    # air: Awaji, the far shore and its hill, the far strait toward the sky's colour at the horizon
    far = np.clip(m["awaji"] * 1.0 + m["hill"] * 0.75 + m["water"] * np.clip(1 - (y - HZ) / 26.0, 0, 1) * 0.6, 0, 1)
    depth.air(pic, far * (1 - m["castle"] * 0.6), PAPER, amount=0.30)
    # the near road a little deeper, the bottom corners too
    depth.frame(pic, amount=0.10, bottom=0.10)
    # the tide's lines, the shells and pebbles, the ripples
    tide_lines(pic, m, seed)
    scatter_bits(pic, m, seed + 10)
    # the shadows of the things on the sand, deeper; contact shade at their feet
    glaze(pic, object_shadows(m), "#5a5490", 0.38)
    for name in ("pots", "heitaboat", "tub", "rocks"):
        glaze(pic, contact(cuts[name][1]) * m["ground"], "#463c6c", 0.70)
    # the pines' shade
    glaze(pic, pine_shade(m, seed + 20), "#5a5490", 0.36)
    return np.clip(pic, 0, 1).astype(F32)


# ================================================================ the front plane
def pad(sheet, cx, cy, rx, ry, base, top, rim_c, seed):
    """A flat pad of pine needles, as this shore's pines are drawn: a broad mass with a scalloped top and a flatter
    underside, its top a step lighter."""
    rng = np.random.default_rng(seed)
    n = max(4, int(rx / 16))
    for i in range(n):
        t = (i + 0.5) / n
        ex = cx - rx + 2 * rx * t + rng.uniform(-4, 4)
        er = rx / n * 1.25 + rng.uniform(0, 6)
        sheet.ellipse(ex, cy - ry * 0.35 + rng.uniform(-3, 3), er, ry * 0.75, top, 1.0)
    sheet.ellipse(cx, cy + ry * 0.05, rx, ry * 0.75, base, 1.0)
    sheet.poly([(cx - rx * 0.92, cy + ry * 0.2), (cx + rx * 0.92, cy + ry * 0.2), (cx + rx * 0.75, cy + ry * 0.62), (cx - rx * 0.78, cy + ry * 0.6)], base, 1.0)


def near_plane(seed=WSEED + 7):
    x, y = grid(SHAPE)
    bark = depth.near_tone(lerp(SIENNA, PRUSSIAN, 0.40), shade="#1e1416", k=0.70, warm=0.07)
    bark_dk = depth.near_tone(lerp(SIENNA, PRUSSIAN, 0.50), shade="#120c0e", k=0.84, warm=0.04)
    bark_lt = depth.near_tone(lerp(SIENNA, OCHRE, 0.20), shade="#24181a", k=0.46, warm=0.07)
    needles = depth.near_tone(lerp(PINE, PRUSSIAN, 0.15), shade="#141e18", k=0.56, warm=0.05)
    needles_top = depth.near_tone(lerp(PINE, PINE_LIT, 0.50), shade="#141e18", k=0.42, warm=0.06)
    needles_dk = depth.near_tone(PINE_DEEP, shade="#0e1610", k=0.66, warm=0.04)
    earth = depth.near_tone(EARTH, shade="#2a1c1a", k=0.64, warm=0.07)
    grass = depth.near_tone(lerp(VIRIDIAN, VERONESE, 0.35), shade="#141e18", k=0.52, warm=0.05)
    grass_lt = depth.near_tone(lerp(VERONESE, NAPLES, 0.25), shade="#141e18", k=0.36, warm=0.05)
    rimc = lerp(lerp(NAPLES, OCHRE, 0.35), WHITE, 0.15)

    # ---- the near pine at the right: its trunk (from below the frame, off the right edge, leaning in over us)
    trunk_path = smooth_pts([(884, 520), (830, 300), (790, 170), (752, 60), (728, -30)], 10)
    tsheet = Sheet(SHAPE)
    tsheet.poly(band_poly(trunk_path, 150, 96), bark, 1.0)
    # the bough: from the trunk high up, sweeping left along the top and out of the frame
    bough_path = smooth_pts([(752, 52), (700, 40), (640, 46), (580, 34), (520, 18), (470, -12)], 10)
    tsheet.poly(band_poly(bough_path, 30, 12), bark, 1.0)
    # the top-left: another pine's bough reaching in from the left edge
    lb = smooth_pts([(-20, 112), (30, 84), (96, 40), (170, 8), (210, -14)], 10)
    tsheet.poly(band_poly(lb, 26, 12), bark, 1.0)
    tc, ta = tsheet.done()
    # the bark's plates break the trunk's outline a little (no holes: only the edge moves)
    ta = np.clip((blur(ta, 1.6) + (noise(SHAPE, (5, 12), seed + 40, 3) - 0.5) * 0.55 - 0.5) * 6 + 0.5, 0, 1) * (blur(ta, 4.0) > 0.02)
    tc = np.where((ta > 0)[..., None] & (tc.sum(axis=-1) < 0.01)[..., None], bark[None, None, :], tc)
    # bark: plates and cracks across the trunk (darker), the plates' upper edges a step lighter
    plates = noise(SHAPE, (14, 6), seed, 4)
    fiss = np.exp(-((noise(SHAPE, (7, 26), seed + 41, 3) - 0.5) / 0.045) ** 2)          # fissures along the trunk
    cross = step(0.62, 0.70, noise(SHAPE, (26, 5), seed + 42, 3))                       # and across, between plates
    lights = step(0.62, 0.72, plates) * (1 - fiss)
    tc = lerp(tc, bark_dk[None, None, :], (np.clip(fiss * 0.9 + cross * 0.6, 0, 1))[..., None])
    tc = lerp(tc, bark_lt[None, None, :], (lights * 0.45)[..., None])
    # round: the side away from the sun (the trunk's left, in the picture) in deeper shade
    xx, yy = grid(SHAPE)
    first = np.where(ta > 0.5, xx, 9999).min(axis=1)[:, None]
    dleft = np.clip((xx - first) / 34.0, 0, 1) * (yy > -1)
    tc = lerp(tc, bark_dk[None, None, :], ((1 - dleft) * 0.55 * (xx > 600))[..., None])
    # round: the side away from the sun (left) deeper
    side = np.clip(blur(ta, 6.0), 0, 1)
    rimm = depth.rim(ta, light=LIGHT, width=2.5)
    tc = lerp(tc, rimc[None, None, :], (np.clip(rimm * 1.3, 0, 1) * 0.75)[..., None])

    # ---- the pads of needles
    psheet = Sheet(SHAPE)
    pads = [(632, 30, 92, 34, 1), (500, 6, 74, 26, 2), (772, 18, 64, 30, 3), (712, 92, 46, 20, 4), (96, 22, 110, 32, 5), (214, -6, 70, 24, 6), (34, 110, 62, 22, 7)]
    for (cx, cy, rx, ry, s) in pads:
        pad(psheet, cx, cy, rx, ry, needles, needles_top, rimc, seed + s)
    pc, pa = psheet.done()
    rag = blur(pa, 2.6) + (noise(SHAPE, (7, 4), seed + 8, 3) - 0.5) * 0.9
    pa = np.clip((rag - 0.5) * 6 + 0.5, 0, 1) * (blur(pa, 5.0) > 0.05)
    pc = np.where((pa > 0)[..., None] & (psheet.done()[1] < 0.5)[..., None], needles[None, None, :], pc)
    tex = noise(SHAPE, (5, 3), seed + 9, 3)
    pc = lerp(pc, needles_dk[None, None, :], (step(0.45, 0.35, tex) * 0.6 * (y > 8))[..., None])     # the needles' tufts
    # under each pad, deeper (it shades itself)
    under = np.clip(blur(pa, 3.0) - np.roll(blur(pa, 3.0), -6, axis=0), 0, 1)
    pc = lerp(pc, needles_dk[None, None, :], (np.clip(under * 3, 0, 1) * 0.7)[..., None])
    prim = depth.rim(pa, light=LIGHT, width=2.5)
    pc = lerp(pc, lerp(rimc, needles_top, 0.35)[None, None, :], (np.clip(prim * 1.4, 0, 1) * 0.8)[..., None])

    # ---- the bank's lip at the bottom with its grass
    rng = np.random.default_rng(seed + 30)
    xs = np.arange(-10, 811, 10, dtype=np.float64)
    left = np.clip((96 - xs) / 96.0, 0, 1) ** 1.3
    right = np.clip((xs - 712) / 88.0, 0, 1) ** 1.25
    top = 599.0 - left * 52.0 - right * 62.0 + rng.uniform(-1.0, 1.0, len(xs))
    lsheet = Sheet(SHAPE)
    lsheet.poly([(float(a), float(b)) for a, b in zip(xs, top)] + [(810, 610), (-10, 610)], earth, 1.0)
    gsheet = Sheet(SHAPE)
    for i in range(520):
        gx = rng.uniform(-8, 808)
        corner = max(np.clip((110 - gx) / 110.0, 0, 1), np.clip((gx - 700) / 100.0, 0, 1))
        if corner < 0.05 and rng.random() < 0.8:
            continue
        gy = float(np.interp(gx, xs, top)) + rng.uniform(0, 5)
        ln = (rng.uniform(2, 5) if corner < 0.05 else rng.uniform(5, 12)) + corner * rng.uniform(14, 34)
        ang = -math.pi / 2 + rng.uniform(-0.5, 0.5) + 0.12
        tip = (gx + math.cos(ang) * ln, gy + math.sin(ang) * ln)
        mid = (gx + math.cos(ang) * ln * 0.5 + rng.uniform(-2, 2), gy + math.sin(ang) * ln * 0.5)
        col = lerp(grass, grass_lt, rng.uniform(0.0, 0.35))
        gsheet.taper([(gx, gy), mid, tip], col, rng.uniform(2.2, 3.6) + corner * 1.5, 0.6)
    lc, la = lsheet.done()
    gc, ga = gsheet.done()
    lc = lerp(lc, lerp(earth, bark_dk, 0.5)[None, None, :], (step(0.5, 0.3, noise(SHAPE, (8, 4), seed + 31, 3)) * 0.5)[..., None])
    lrim = depth.rim(np.maximum(la, ga), light=(0.6, -1.0), width=2.0)

    # ---- together: the lip, its grass, the trunk and boughs, the pads in front of the boughs
    col = np.zeros(SHAPE + (3,), F32)
    alpha = np.zeros(SHAPE, F32)
    for c_, a_ in ((lc, la), (gc, ga), (tc, ta), (pc, pa)):
        a_ = np.clip(a_, 0, 1)
        col = col * (1 - a_[..., None]) + c_ * a_[..., None]
        alpha = np.maximum(alpha, a_)
    col = lerp(col, lerp(rimc, grass_lt, 0.5)[None, None, :], (np.clip(lrim * 1.2, 0, 1) * 0.55 * (y > 500))[..., None])
    alpha = (alpha > 0.5).astype(F32)
    # no specks of light shut in by the darks: fill any small hole in the mask
    holes = (blur(alpha, 2.0) > 0.75) & (alpha < 0.5)
    alpha = np.maximum(alpha, holes.astype(F32))
    col = np.where(holes[..., None], needles_dk[None, None, :], col)
    return np.clip(col, 0, 1).astype(F32), alpha


# ================================================================ to palettes, as the painter finishes
def finish(picture, name, colors, alpha=None, new=False):
    g = grain(picture, 7, 0.02) if new else picture
    sample_of = g if alpha is None else g[alpha > 0.5]
    n = len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0))
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, n)))
    idx = to_palette(g, pal, speckle=0.014 if new else 0.008)
    save(f"{OUT}/{name}.png", idx, pal, alpha)


def main():
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back")
    cuts = {n: load(n) for n in CUTS}
    m = masks()
    deep = deepen_back(back, cuts, m)
    WET = wet_map(m)
    nc, na = near_plane()
    washed = watercolor.wash(deep, seed=WSEED, soft=WET, wander=1.4, fleck=0.3)
    finish(washed, "back", 152)
    for n in CUTS:
        c, a = cuts[n]
        wc = watercolor.wash_cut(c, a, deep, seed=WSEED, soft=WET, wander=1.4, fleck=0.3, crisp=True)
        finish(wc, n, COLORS[n], a)
    wn = watercolor.wash_cut(nc, na, deep, seed=WSEED, soft=WET, wander=1.4, fleck=0.3, crisp=True)
    finish(wn, "near", COLORS["near"], na, new=True)
    # the frame of the Awa boat, and the numbers, as they were
    for f in ("boat-1.png", "layout.json"):
        shutil.copyfile(f"{ORIG}/{f}", f"{OUT}/{f}")
    # a composite to look at (the boat coming in), with the near plane
    comp = Image.open(OUT + "/back.png").convert("RGBA")
    for n in A.ORDER + ["near"]:
        comp.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
    comp.convert("RGB").save("out/edo-akashi-depth-comp.png")
    print("near share", round(float(na.mean()) * 100, 1), "%")


if __name__ == "__main__":
    main()

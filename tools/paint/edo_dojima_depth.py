"""Round twenty-three's fast depth pass (/home/claude/r23/LITE.md) for the Dojima shore (edo-dojima): Osaka, a late April
afternoon in 1830, the sun low in the west-south-west, to our right. It works over PAINT-21C's finished painting (run
edo_dojima.py as it is, copy out/edo-dojima/ to out/edo-dojima-orig/) and writes the scene's full set back into
out/edo-dojima/, every file as before and near.png. Nothing is repainted: the camera, the places and the outlines stay.

    near.png   OUR SIDE OF THE STREET, behind us to the left: the corner of the timber canopy along a rice warehouse's front,
               over our heads and across the top left (the underside of its rafters, the beam, the tiles' lips, the corner where the warehouse ends) and its post
               down the left edge (a 15 cm timber, its face toward us in shade, its west side in the low sun below the
               eave's shadow); across the top right, the hanging whips of the willow that stands on the bank just beyond
               the right edge (Osaka's river banks were planted with willows). All through the scene's camera
               (edo_dojima.CAM): the eave 4.4 m up and 3.8 m from the lens.
    back.png   the willow's long shadow led in from the right edge across the shore street (its trunk, then its crown's
               thin dappled shade) along the sun, as every shadow here goes (to the left, a little toward us); the
               street's texture through the camera (stones, ruts and foot-worn hollows, rice straw from the bales, dark
               wet splashes by the water men's buckets), big and few near us, small and many far; the far bank, the
               castle and the bridge's far half moved toward the haze's colour, layer by layer; the near street a step
               deeper; then the act's watercolour wash (wet in wet: the sky, the far land, the water).
    cut-outs   as painted, each washed on the same paper as the backdrop (watercolor.wash_cut, crisp); the frames of moving
               things (the lighters poled past, the runner, the splash) byte for byte.

    python3 edo_dojima_depth.py            -> out/edo-dojima/ (and out/edo-dojima-depth-comp.png to look at)
"""

import math
import os
import shutil
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

from brush import F32, rgb, lerp, blur, grid, noise, mask_poly, mask_line, palette_of, to_palette, save, grain, step
import depth as D
import watercolor as WC
from edo_village_kit import Wet
import edo_dojima as S

SEED = 1830
ORIG = "out/edo-dojima-orig"
OUT = "out/edo-dojima"
SHAPE = (600, 800)
H, W = SHAPE
CAM = S.CAM
g = S.g
CUTS = {"lighter": 48, "market": 96, "noren": 32, "sandals": 32, "sandals-few": 32, "pot": 48, "stall": 48, "tray": 32,
        "tray-half": 32, "tray-empty": 32, "kettle": 32, "front": 48}
WASH = dict(seed=SEED, wander=1.4, fleck=0.3)

# the walk outline and the stall's patches (the scene file's): texture goes only where people walk
WALK = [[0, 596], [800, 596], [800, 470], [708, 466], [619, 461], [534, 457], [453, 453], [375, 449], [368, 456], [114, 443], [128, 437], [0, 431]]
BLOCKED = [[[73, 472], [344, 489], [359, 473], [105, 459]], [[120, 441], [178, 444], [155, 455], [94, 451]],
           [[489, 465], [835, 483], [809, 462], [496, 447]], [[491, 475], [528, 477], [530, 467], [495, 465]]]


def load(path):
    a = np.asarray(Image.open(path).convert("RGBA"), dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def fin(pic, path, colors, alpha=None, speckle=0.010):
    """The scene's own finish, lighter (the painting is grained already): grain, its own palette, a fine speckle."""
    g_ = grain(np.clip(pic, 0, 1), 7, 0.010)
    sample = g_ if alpha is None else g_[alpha > 0.5]
    n = min(colors, max(2, len(np.unique((sample * 255).astype(np.uint8).reshape(-1, 3), axis=0))))
    pal = palette_of([sample.reshape(-1, 1, 3)], colors=n)
    idx = to_palette(g_, pal, speckle=speckle)
    save(path, idx, pal, alpha)


def P(X, Y, Z):
    x, y = CAM.pt(X, Y, Z)
    return (float(x), float(y))


# ================================================================ masks of the backdrop
def masks(back):
    """sky, water, far (the island, the castle, the reach), bridge, walk: picture masks 0..1."""
    x, y = grid(SHAPE)
    sky_paint = S.paint_sky(SEED)
    d = blur(np.abs(back - sky_paint).sum(axis=2), 1.5)
    like = ((d < 0.16) & (y < 300)) | (y < 128)                    # (above row 128 nothing stands: only the sky and its clouds)
    sky = np.cumprod(like, axis=0).astype(F32)                     # from the top down until the first thing that is not sky
    sky = blur(sky, 0.8)
    house = mask_poly(SHAPE, [(0, 120), (434, 120), (436, 455), (0, 445)], soft=0.5)
    water = np.clip(S.river_region(), 0, 1).astype(F32)
    water = water * (1 - sky) * (1 - house)
    bridge = mask_poly(SHAPE, [(664, 228), (800, 228), (800, 470), (664, 470)], soft=3.0)
    top_of_water = np.argmax(water > 0.5, axis=0)                  # per column: where the water begins
    top_of_water[water.max(axis=0) < 0.5] = 0
    above_water = (y < top_of_water[None, :]).astype(F32)
    far = above_water * (1 - sky) * (1 - house) * step(425, 440, x) * step(180, 192, y)
    far = blur(far, 1.0)
    walk = mask_poly(SHAPE, WALK)
    for b in BLOCKED:
        walk = walk * (1 - mask_poly(SHAPE, b))
    return dict(sky=sky, water=water, far=far, bridge=bridge, house=house, walk=walk)


# ================================================================ the back: shadows, texture, air
WILLOW = (540.0, -1260.0)              # the willow by the bank just beyond the right edge (X, Z, cm)


def willow_shadow(pic, M):
    """The willow's trunk (it leans a little over the water) and its crown's thin, broken shade, laid along the sun."""
    X0, Z0 = WILLOW
    SH = rgb("#3c3f78")
    walk_soft = np.clip(blur(mask_poly(SHAPE, WALK), 1.0), 0, 1)
    ground = walk_soft * (1 - M["water"])
    # the trunk: 34 cm thick, up to its crown at 3.4 m
    trunk = [(X0 - 30, 0, Z0), (X0 + 30, 0, Z0), (X0 + 18, 360, Z0 + 26), (X0 - 36, 360, Z0 + 26)]
    poly = [P(X0 - 30, 0, Z0), P(X0 + 30, 0, Z0)] + CAM.shadow_poly(trunk[2:])
    m = mask_poly(SHAPE, poly, soft=1.4, wobble=1.0, seed=3) * ground
    # the crown's shade: many soft blots, the whips hanging; thin where the line of pilgrims stands
    rng = np.random.default_rng(SEED + 7)
    crown = np.zeros(SHAPE, F32)
    for i in range(90):
        r = rng.uniform(0, 1) ** 0.7 * 420.0
        a = rng.uniform(0, 2 * math.pi)
        Xc, Zc = X0 - 60 + r * math.cos(a), Z0 + 60 + r * math.sin(a) * 0.8
        Yc = rng.uniform(380, 760)
        sx, sz = CAM.cast(Xc, Yc, Zc, 0.0)
        px, py = P(sx, 0, sz)
        k = CAM.k(sx, sz)
        rx = rng.uniform(70, 150) * k
        ry = rx * rng.uniform(0.22, 0.34)
        crown = np.maximum(crown, mask_ellipse_fast(px, py, rx, ry) * rng.uniform(0.6, 1.0))
    crown = np.clip(blur(crown, 3.0), 0, 1)
    holes = step(0.58, 0.72, noise(SHAPE, 16, SEED + 8, 3))       # flecks of sun through the leaves
    crown = crown * (1 - holes * 0.8)
    people = mask_poly(SHAPE, [(130, 470), (440, 470), (450, 600), (130, 600)], soft=34)
    shade = np.clip(np.maximum(m * 0.78, crown * (0.32 - 0.18 * people)), 0, 1) * ground
    pic[...] = pic * (1 - shade[..., None]) + pic * (SH * 1.55) * shade[..., None]
    return np.clip(pic, 0, 1, out=pic)


def mask_ellipse_fast(cx, cy, rx, ry):
    m = np.zeros(SHAPE, F32)
    x0, x1 = int(max(cx - rx - 2, 0)), int(min(cx + rx + 3, W))
    y0, y1 = int(max(cy - ry - 2, 0)), int(min(cy + ry + 3, H))
    if x0 >= x1 or y0 >= y1:
        return m
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(F32)
    d = ((xx - cx) / max(rx, 0.5)) ** 2 + ((yy - cy) / max(ry, 0.5)) ** 2
    m[y0:y1, x0:x1] = np.clip((1.0 - d) * 3.0, 0, 1)
    return m


def texture(pic, M):
    """The packed earth of the shore street through the camera: stones, foot-worn hollows, rice straw, wet splashes."""
    walk = M["walk"]
    zone = (blur(walk, 1.0) > 0.9).astype(F32)
    pt = lambda X, Z: P(X, 0, Z)
    k_of = lambda X, Z: CAM.k(X, Z)
    bounds = (-2600.0, 1400.0, -1560.0, -880.0)
    EARTH = S.EARTH
    dark = lerp(EARTH, rgb("#3a3050"), 0.45)
    lit = lerp(EARTH, rgb("#fbf3dc"), 0.45)
    straw = rgb("#d9b25a")
    sh = Wet(SHAPE)
    # foot-worn hollows and ruts: long soft flat marks along the street
    for (x, y, k, r) in D.scatter(pt, k_of, bounds, 0.22, SEED + 1, size=(90, 12), zone=zone):
        L = (60 + 90 * r) * k
        t = 3.0 + 4.0 * r
        sh.poly([(x - L, y), (x - L * 0.3, y - t * k * 0.9), (x + L, y - 0.6), (x + L * 0.4, y + t * k * 0.5)], lerp(EARTH, dark, 0.35), alpha=0.32)
    # stones and pebbles: a dark under-side, a lit top toward the sun (right)
    for (x, y, k, r) in D.scatter(pt, k_of, bounds, 3.2, SEED + 2, size=(5, 3), zone=zone):
        s = (2.0 + 5.0 * r ** 2) * k
        sh.ellipse(x, y + s * 0.15, s, s * 0.45, dark, alpha=0.75)
        sh.ellipse(x + s * 0.25, y - s * 0.12, s * 0.62, s * 0.28, lit, alpha=0.8)
    # rice straw dropped from the bales, thin and golden, lying every way
    for (x, y, k, r) in D.scatter(pt, k_of, bounds, 1.6, SEED + 3, size=(14, 1), zone=zone):
        L = (8 + 12 * r) * k
        a = r * 6.283
        sh.line([(x - L * math.cos(a), y - L * math.sin(a) * 0.35), (x + L * math.cos(a), y + L * math.sin(a) * 0.35)], straw, max(0.6, 0.9 * k * 2), alpha=0.7)
    c, a = sh.done()
    a = a * zone
    pic[...] = pic * (1 - a[..., None]) + c * a[..., None]
    # the water men's splashes: dark wet earth by the market, ringed
    wet = np.zeros(SHAPE, F32)
    rng = np.random.default_rng(SEED + 9)
    for i in range(7):
        X, Z = rng.uniform(-100, 600), rng.uniform(-1500, -1330)
        x, y = pt(X, Z)
        k = k_of(X, Z)
        wet = np.maximum(wet, mask_ellipse_fast(x, y, rng.uniform(40, 90) * k, rng.uniform(10, 20) * k))
    wet = blur(wet, 1.2) * zone * 0.30
    pic[...] = pic * (1 - wet[..., None]) + pic * rgb("#6a6a8a")[None, None, :] * 1.15 * wet[..., None]
    return np.clip(pic, 0, 1, out=pic)


def air(pic, M):
    """The far layers toward the haze at the horizon: the island's warehouses, then (farther) the castle and the reach;
    the bridge's far half a little; the far water a little more."""
    x, y = grid(SHAPE)
    sky = M["sky"]
    band = (sky > 0.9) & (y > 200) & (y < 262) & (x > 430)
    hz = np.median(pic[band], axis=0) if band.sum() > 50 else rgb("#efe6cf")
    far = M["far"] * (0.17 + 0.15 * step(560, 430, x) * step(300, 250, y))     # the castle and the reach up the river: farther
    bridge = M["bridge"] * (1 - M["water"]) * step(330, 230, y) * 0.16
    water = M["water"] * np.clip((330 - y) / 70.0, 0, 1) * 0.22
    D.air(pic, np.clip(far + bridge + water, 0, 0.6), hz, amount=1.0)
    # the near street a step deeper toward us (and the frame's bottom), the far street paler
    near = np.clip((y - 470) / 130.0, 0, 1) ** 1.3 * M["walk"]
    pic[...] = pic * (1 - 0.10 * near[..., None]) + pic * rgb("#8a6a5a")[None, None, :] * 0.10 * near[..., None] * 1.25
    return np.clip(pic, 0, 1, out=pic), hz


def wet_map(M):
    """WET for the wash: 1 the sky, 0.55 to 0.62 the far land, the water 0.75 at the horizon to 0.2 near, else 0."""
    x, y = grid(SHAPE)
    water = M["water"] * lerp(0.75, 0.2, np.clip((y - 280) / 175.0, 0, 1))
    far = M["far"] * lerp(0.62, 0.50, np.clip((y - 200) / 110.0, 0, 1)) * (1 - 0.7 * M["bridge"])
    return np.clip(np.maximum(np.maximum(M["sky"], far), water), 0, 1).astype(F32)


# ================================================================ near.png
EAVE_Z, EAVE_Y = -380.0, 440.0        # the eave's edge: 3.8 m in front of the lens, 4.4 m up (the eye is 3.59 m)
CORNER_X = -112.0                     # where the warehouse ends (the corner of its eave)
POST_X, POST_Z, POST_HALF = -290.0, -372.0, 7.5


def lift(X):
    """The eave's edge swept up a little toward the corner."""
    t = max(0.0, 1.0 - (CORNER_X - X) / 80.0)
    return 4.0 * t ** 2


def near_plane():
    """-> (colour, cover) of the eave, its post and the willow's whips."""
    WOOD = rgb("#5a3a24")
    DARK = rgb("#2a1a14")
    WARM = rgb("#a8683a")
    GLOW = rgb("#e0a060")
    TILE = rgb("#2c2c3a")
    TILE_LIT = rgb("#6a7088")
    deep = D.near_tone(WOOD, k=0.55, warm=0.06)
    L = Wet(SHAPE)
    rng = np.random.default_rng(SEED + 31)
    Xs = np.linspace(-1200.0, CORNER_X, 60)
    edge = [P(X, EAVE_Y + lift(X), EAVE_Z) for X in Xs]
    side = [P(CORNER_X, EAVE_Y + 4.0 + 0.35 * (Z - EAVE_Z), Z) for Z in np.linspace(EAVE_Z, -150.0, 20)]
    region = [(-30.0, -30.0), (-30.0, edge[0][1])] + edge + side + [(side[-1][0], -30.0)]
    L.poly(region, lerp(deep, DARK, 0.25), lerp(deep, WARM, 0.25), g=((150, -10), (150, edge[30][1])))
    # the rafters, running back over us toward the wall: their feet (by the edge) warm with the street's light
    for X in np.arange(-1200.0, CORNER_X - 12.0, 28.0):
        a0, a1 = X - 3.5, X + 3.5
        foot = EAVE_Y + lift(X) + 1.0
        q = [P(a0, foot, EAVE_Z + 4), P(a1, foot, EAVE_Z + 4), P(a1, foot + 0.32 * 260, EAVE_Z + 260), P(a0, foot + 0.32 * 260, EAVE_Z + 260)]
        L.poly(q, lerp(WOOD, WARM, 0.22 + 0.12 * rng.random()), lerp(WOOD, DARK, 0.75), g=(q[0], q[3]))
        s_ = [P(a1, foot, EAVE_Z + 4), P(a1 + 2.0, foot, EAVE_Z + 4), P(a1 + 2.0, foot + 0.32 * 260, EAVE_Z + 260), P(a1, foot + 0.32 * 260, EAVE_Z + 260)]
        L.poly(s_, DARK, alpha=0.8)
    # the beam the rafters lie on, just in from the edge
    bm = [P(X, EAVE_Y - 12.0, EAVE_Z + 14.0) for X in np.linspace(-1200.0, CORNER_X - 20.0, 30)]
    bt = [P(X, EAVE_Y + 6.0, EAVE_Z + 26.0) for X in np.linspace(-1200.0, CORNER_X - 20.0, 30)]
    L.poly(bm + bt[::-1], lerp(WARM, WOOD, 0.35), lerp(WOOD, DARK, 0.6), g=(bm[10], bt[10]))
    # the fascia's underside, a warm strip the street lights, then the tiles' lips (dark, the sky on their round ends)
    fo = [P(X, EAVE_Y + lift(X), EAVE_Z) for X in np.linspace(-1200.0, CORNER_X, 70)]
    fi = [P(X, EAVE_Y + lift(X) + 1.5, EAVE_Z + 6.0) for X in np.linspace(-1200.0, CORNER_X, 70)]
    L.poly(fo + fi[::-1], lerp(WARM, GLOW, 0.3), WARM, g=(fo[35], fi[35]))
    lip, outer = [], []
    for X in np.linspace(-1200.0, CORNER_X + 3.0, 260):
        ph = ((X + 4000.0) % 26.0) / 26.0
        lip.append(P(X, EAVE_Y + lift(X) - (2.6 + 1.6 * math.sin(ph * math.pi) ** 0.6), EAVE_Z - 3.0))
        outer.append(P(X, EAVE_Y + lift(X) + 0.5, EAVE_Z - 3.0))
    L.poly(lip + outer[::-1], TILE)
    for X in np.arange(-1200.0 + 13.0, CORNER_X - 2.0, 26.0):
        cx, cy = P(X, EAVE_Y + lift(X) - 2.4, EAVE_Z - 3.0)
        r = 7.0 * 800.0 / 380.0
        L.ellipse(cx, cy + 0.4, r * 0.55, r * 0.2, TILE_LIT, alpha=0.35)
    # the corner's return (the end of the warehouse's eave going back toward us): its barge board, dark, lit below
    so = [P(CORNER_X + 3.0, EAVE_Y + 4.0 + 0.35 * (Z - EAVE_Z), Z) for Z in np.linspace(EAVE_Z, -150.0, 20)]
    si = [P(CORNER_X - 12.0, EAVE_Y - 10.0 + 0.35 * (Z - EAVE_Z), Z) for Z in np.linspace(EAVE_Z, -150.0, 20)]
    L.poly(so + si[::-1], TILE)
    L.line(si, lerp(WARM, GLOW, 0.4), 1.4, 0.75)
    # the post, down the left edge, under the beam: its face toward us in deep shade, its west side in the sun below the
    # eave's shadow (the canopy runs on 1.8 m past it toward the sun: its top 60 cm stays in shade)
    xa, xb = POST_X - POST_HALF, POST_X + POST_HALF
    za, zb = POST_Z + POST_HALF, POST_Z - POST_HALF            # its face toward us (za), its back (zb)
    top = EAVE_Y - 12.0
    front = [P(xa, -200, za), P(xb, -200, za), P(xb, top, za), P(xa, top, za)]
    sidef = [P(xb, -200, za), P(xb, -200, zb), P(xb, top, zb), P(xb, top, za)]
    L.poly(front, lerp(deep, DARK, 0.35), lerp(deep, WARM, 0.12), g=((front[0][0], 0), (front[1][0], 0)))
    L.poly(sidef, lerp(WOOD, WARM, 0.25), lerp(WOOD, DARK, 0.2), g=((0, sidef[2][1]), (0, sidef[2][1] + 60)))
    lit_top = top - 62.0
    sun = [P(xb, -200, za), P(xb, -200, zb), P(xb, lit_top + 10, zb), P(xb, lit_top, za)]
    L.poly(sun, lerp(WARM, GLOW, 0.55), lerp(WARM, GLOW, 0.15), g=((0, sun[3][1]), (0, 600)))
    for i in range(9):                                       # the grain: long checks
        t = rng.uniform(0.15, 0.85)
        f = front if i % 2 else sidef
        xx = f[0][0] + (f[1][0] - f[0][0]) * t
        y0, y1 = rng.uniform(120, 400), rng.uniform(420, 620)
        L.line([(xx, y0), (xx + rng.normal(0, 0.5), (y0 + y1) / 2), (xx + rng.normal(0, 0.8), y1)], lerp(DARK, rgb("#120a08"), 0.4), rng.uniform(0.5, 1.0), rng.uniform(0.35, 0.6))
    # the post's head: a bracket block under the beam
    hd = [P(xa - 2, top - 14, za), P(xb + 10, top - 14, za), P(xb + 10, top + 2, za), P(xa - 2, top + 2, za)]
    L.poly(hd, DARK, lerp(DARK, WARM, 0.45), g=(hd[2], hd[1]))
    c, a = L.done()
    a_hard = (a > 0.5).astype(F32)
    rim = D.rim(a_hard, light=(0.45, 1.0), width=2.0)          # the street's light comes up under it: the lower edges
    c = lerp(c, np.clip(c * 1.6 + np.array([0.10, 0.06, 0.02], F32), 0, 1), (np.clip(rim, 0, 1) * 0.35)[..., None])
    # ---------------- the willow's whips across the top right
    wc, wa = willow()
    c = c * (1 - wa[..., None]) + wc * wa[..., None]
    a = np.maximum(a, wa)
    return c.astype(F32), np.clip(a, 0, 1).astype(F32)


def willow():
    """The willow's whips: a dense bough off the top edge, long whips hanging from it, narrow leaves; in shade on our
    side, the low sun through them on the right (their edges toward it lit yellow-green)."""
    rng = np.random.default_rng(SEED + 41)
    SHADE = rgb("#2c3a20")
    MID = rgb("#4a5a2a")
    LIT = rgb("#b8b850")
    s = Wet(SHAPE)
    # the bough's mass along the top edge (off the frame above): solid, a ragged lower edge
    xs = np.linspace(548, 830, 40)
    low = [(x_, 6 + 26 * ((x_ - 548) / 282) ** 0.8 + 8 * math.sin(x_ * 0.11) + rng.uniform(-3, 3)) for x_ in xs]
    s.poly([(548, -20)] + low + [(830, -20)], SHADE, lerp(SHADE, MID, 0.3), g=((700, -10), (700, 40)))
    # the branch it hangs from, curving down into the corner
    s.line([(830, 30), (760, 18), (690, 10), (630, 4), (590, -6)], rgb("#241a14"), 5.0, 1.0)
    s.line([(830, 26), (760, 15), (690, 7)], rgb("#8a6a3a"), 1.2, 0.7)
    strands = []
    for i in range(46):
        x0 = 556 + 256 * rng.uniform(0, 1) ** 0.75                       # thicker toward the corner
        t = (x0 - 556) / 256.0
        y0 = 4 + 24 * t ** 0.8 + rng.uniform(-4, 4)
        length = (rng.uniform(30, 95) + 105 * t ** 1.3) * rng.uniform(0.55, 1.0)
        if x0 < 600:
            length *= 0.6
        far = rng.random() < 0.35                                         # whips farther in the crown: paler, thinner
        strands.append((x0, y0, length * (0.8 if far else 1.0), rng.uniform(-1, 1), far))
    strands.sort(key=lambda s_: (not s_[4], s_[0]))                     # the farther whips first
    for (x0, y0, length, bend, far) in strands:
        n = 14
        pts = []
        for j in range(n + 1):
            u = j / n
            pts.append((x0 + bend * 6 * u + 9 * u * u, y0 + length * u))
        sh_ = lerp(SHADE, rgb("#8a9a70"), 0.45) if far else SHADE
        s.line(pts, lerp(sh_, MID, 0.4), 1.2, 0.95)
        if far:
            m_ = int(length / 6.0)
            for j in range(m_):
                u = (j + 0.5) / m_
                px, py = x0 + bend * 6 * u + 9 * u * u, y0 + length * u
                side = 1 if j % 2 else -1
                ang = math.radians(rng.uniform(14, 30)) * side
                ln = rng.uniform(5, 8) * (1.0 - 0.35 * u)
                s.line([(px, py), (px + math.sin(ang) * ln, py + math.cos(ang) * ln)], lerp(sh_, MID, rng.uniform(0.1, 0.5)), 1.6, 1.0)
            continue
        # narrow leaves, alternate, pointing down and out
        m_ = int(length / 5.5)
        for j in range(m_):
            u = (j + 0.5) / m_
            px = x0 + bend * 6 * u + 9 * u * u
            py = y0 + length * u
            side = 1 if j % 2 else -1
            ang = math.radians(rng.uniform(14, 32)) * side
            ln = rng.uniform(6, 10) * (1.0 - 0.35 * u)
            ex, ey = px + math.sin(ang) * ln, py + math.cos(ang) * ln
            col = lerp(SHADE, MID, rng.uniform(0.2, 0.9))
            s.line([(px, py), ((px + ex) / 2, (py + ey) / 2), (ex, ey)], col, rng.uniform(1.6, 2.3), 1.0)
            if side > 0:                                              # the sun's side: a lit edge
                s.line([(px + 0.8, py + 0.6), (ex + 0.6, ey)], LIT, 0.7, 0.75)
    c, a = s.done()
    # no sky shut in by leaves (it would key as a speck of light)
    solid = a > 0.5
    filled = ndimage.binary_fill_holes(solid)
    holes = (filled & ~solid).astype(F32)
    c = c * (1 - holes[..., None]) + lerp(SHADE, MID, 0.3)[None, None, :] * holes[..., None]
    a = np.maximum(a, holes)
    return c.astype(F32), a.astype(F32)


# ================================================================ the whole
def main():
    os.makedirs(OUT, exist_ok=True)
    back, _ = load(f"{ORIG}/back.png")
    unwashed = back.copy()
    M = masks(unwashed)
    pic = back.copy()
    willow_shadow(pic, M)
    texture(pic, M)
    pic, hz = air(pic, M)
    WET = wet_map(M)
    Image.fromarray((np.clip(WET, 0, 1) * 255).astype(np.uint8)).save("out/edo-dojima-wet.png")
    base = pic.copy()                                          # the backdrop as painted, before its own wash
    washed = WC.wash(base, soft=WET, **WASH)
    quick = "quick" in sys.argv                                  # (while composing: the cut-outs of the last run kept)
    for f in os.listdir(OUT):
        if f.endswith(".png") and not quick:
            os.remove(os.path.join(OUT, f))
    fin(washed, f"{OUT}/back.png", 152)
    comp = washed.copy()
    order = ["lighter", "market", "noren", "sandals", "pot", "stall", "tray", "kettle", "front"]
    done = {}
    for name, n in CUTS.items():
        if quick:
            continue
        c, a = load(f"{ORIG}/{name}.png")
        cw = WC.wash_cut(c, a, base, soft=WET, crisp=True, **WASH)
        if name == "front":                                     # the bales at the front: a step warmer, as near things are
            cw = lerp(cw, cw * rgb("#f4dcc0") * 1.02, 0.35)
        fin(cw, f"{OUT}/{name}.png", n, a)
        done[name] = (cw, a)
    nc, na = near_plane()
    ncw = WC.wash_cut(nc, na, base, soft=WET, crisp=True, **WASH)
    fin(ncw, f"{OUT}/near.png", 64, (na > 0.5).astype(F32))
    for f in os.listdir(ORIG):                                  # the frames of moving things and the layout, as they were
        if f not in [k + ".png" for k in CUTS] and f != "back.png":
            shutil.copy2(os.path.join(ORIG, f), os.path.join(OUT, f))
    out = Image.open(f"{OUT}/back.png").convert("RGBA")
    for name in order + ["near"]:
        out.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    out.convert("RGB").save("out/edo-dojima-depth-comp.png")
    print("written", sorted(os.listdir(OUT)))


if __name__ == "__main__":
    main()

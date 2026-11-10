"""Gonroku's coaster at sea, noon (edo-deck): the fast depth pass of round twenty-three (DEPTH.md; /home/claude/r23/LITE.md).
It works over the painting as edo_deck.py makes it (copied once, unchanged, to out/edo-deck-orig/) and writes the
scene's full set back into out/edo-deck/: every file as before, and near.png.

    near     the sail's near edge overhead at the top left (the forward part of the great sail, braced toward us: its
             underside in shade, the seams of its cotton strips, the bolt rope lit along its foot), a pair of shrouds
             coming down across the top right corner, and the near bulwark's rail, cut away, left standing only at the
             two bottom corners where nobody walks (over the coil and the bucket; over the water cask)
    back     the near walkway deeper toward us; the planks' butt joints and treenails through the camera
             (depth.scatter: few and large near, many and small far); the shrouds' two thin noon shadows coming in from
             the right edge across the stern deck toward the windlass; the sail's own shadow, short and hard, on the far
             bulwark's inner face; the far sea and the cape (the swell layer) toward the sky at the horizon
    japan    watercolor.wash on the backdrop (wet: the sky, the sea falling from the horizon), wash_cut on every
             cut-out and on near.png (crisp), the swell layer wet; the floating cask's frames as they were

The light is the scene's: noon, the sun high behind us and a little left (edo_deck_kit.SUN, SUN3).

    python3 edo_deck_depth.py        (after python3 edo_deck.py, and cp -a out/edo-deck out/edo-deck-orig once)
"""

import glob
import math
import os
import shutil

import numpy as np
from PIL import Image

import depth
import watercolor
from brush import F32, blur, grain, grid, lerp, mask_line, mask_poly, noise, palette_of, rgb, save, to_palette
from edo_deck_kit import (CAM, HZ, FULL, SHAPE, SUN, NAPLES, OCHRE, SIENNA, PRUSSIAN, COBALT, WHITE, ROPE, WOOD_MID,
                          WOOD_LIT, DECK_SHADOW, gp, kz, far_z, sheer, tintw)

ORIG = "out/edo-deck-orig"
OUT = "out/edo-deck"
SEED = 1830
H, W = SHAPE

# the scene file's shapes (js/content/scenes/edo-deck.js)
SEA = [[0, 263], [799, 263], [799, 319], [672, 319], [668, 397], [556, 404], [528, 404], [496, 360], [492, 356], [480, 353], [396, 355],
       [388, 360], [380, 373], [372, 404], [284, 406], [280, 378], [276, 366], [268, 358], [264, 327], [152, 327], [124, 335], [88, 359],
       [84, 363], [80, 384], [44, 387], [40, 383], [28, 393], [24, 424], [0, 357]]
WALK = [[2, 598], [798, 598], [798, 545], [739, 506], [687, 469], [505, 469], [541, 540], [372, 540], [376, 502], [264, 502], [242, 540],
        [77, 540], [115, 506], [82, 509], [53, 526], [25, 550], [11, 569]]
BLOCKED = [[[260, 532], [359, 532], [363, 507], [273, 507]], [[110, 563], [204, 563], [222, 535], [137, 535]], [[426, 558], [502, 558], [498, 546], [425, 546]],
           [[576, 508], [636, 508], [599, 469], [548, 469]], [[642, 547], [670, 547], [661, 537], [633, 537]], [[695, 538], [781, 525], [798, 525], [797, 514], [765, 514], [689, 532]],
           [[2, 598], [80, 598], [99, 582], [2, 582]], [[91, 598], [139, 598], [146, 592], [100, 592]], [[798, 598], [798, 598], [798, 585], [787, 585]]]

CUTS = {"swell": 64, "sail": 64, "rigging": 24, "mast": 48, "windlass": 48, "tiller": 32, "compass-shut": 40, "compass-open": 40,
        "pot": 32, "pot-lifted": 32, "pot-steam": 32, "front": 48}
LIGHT = (-1.0, -0.75)                                            # toward the sun in the picture: left and up


def load(name):
    im = Image.open(os.path.join(ORIG, name)).convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255.0
    return a[..., :3].copy(), a[..., 3].copy()


def finish(picture, path, colors, alpha=None, seed=7):
    g = grain(picture, seed, 0.006)
    sample = g if alpha is None else g[alpha > 0.5]
    n = len(np.unique((sample * 255).astype(np.uint8).reshape(-1, 3), axis=0))
    pal = palette_of([sample.reshape(-1, 1, 3)], colors=min(colors, max(2, n)))
    save(path, to_palette(g, pal, speckle=0.010), pal, alpha)


# ================================================================ the near plane
def near_plane():
    x, y = grid(SHAPE)
    col = np.zeros((H, W, 3), dtype=F32)
    alpha = np.zeros((H, W), dtype=F32)
    rimc = lerp(tintw(NAPLES, 0.25), WHITE, 0.15)

    def lay(c, m):
        nonlocal col, alpha
        m = np.clip(m, 0, 1)[..., None]
        col = col * (1 - m) + c * m
        alpha = np.maximum(alpha, m[..., 0])

    # --- the sail's near edge, overhead at the top left: its underside in shade, the foot billowing between the sheets
    foot = []
    for t in np.linspace(0.0, 1.0, 60):
        # from the left edge, low, to the top edge: a long curve, scalloped a little where the cloth fills between seams
        px = 286.0 * t ** 1.08
        py = 228.0 * (1 - t) ** 0.82 + 5.0 * math.sin(t * math.pi * 5.0) * (1 - t)
        foot.append((px, py))
    sail_poly = [(-4, -4)] + [(-4, foot[0][1])] + foot + [(foot[-1][0], -4)]
    m_sail = mask_poly(SHAPE, sail_poly, soft=0.6, wobble=0.8, seed=SEED)
    deep = depth.near_tone(lerp(WHITE, NAPLES, 0.40), k=0.70, warm=0.11)
    mid = depth.near_tone(lerp(WHITE, NAPLES, 0.45), k=0.52, warm=0.12)
    # graded: deepest in the corner (into the cloth's own shade), warmer and lighter toward the foot (light off the deck)
    d = np.clip(np.hypot(x / 286.0, y / 228.0), 0, 1.3)
    t = np.clip((d - 0.25) / 0.85, 0, 1) ** 1.3
    cloth = lerp(deep[None, None, :], mid[None, None, :], t[..., None])
    cloth *= (1 + (noise(SHAPE, 40, SEED + 1, 3) - 0.5) * 0.10)[..., None]
    lay(cloth, m_sail)
    # the seams of its cotton strips, running up toward the yard (away to the upper left)
    seam = np.zeros((H, W), dtype=F32)
    vp = (-420.0, -900.0)
    for i in range(1, 9):
        fx, fy = foot[min(59, int(i * 6.6))]
        seam = np.maximum(seam, mask_line(SHAPE, [(fx, fy - 2), (fx + (vp[0] - fx) * 0.35, fy + (vp[1] - fy) * 0.35)], 1.4, soft=0.5))
    lay(depth.near_tone(lerp(SIENNA, PRUSSIAN, 0.2), k=0.55, warm=0.06), seam * m_sail * 0.75)
    # the bolt rope along the foot, lit by the sun from behind us (its upper-left side) and by the deck's light below
    bolt = mask_line(SHAPE, [(px, py - 1.0) for px, py in foot], 4.2, soft=0.6)
    lay(depth.near_tone(ROPE, k=0.42, warm=0.10), bolt)
    lay(rimc * 0.95, mask_line(SHAPE, [(px - 0.6, py + 0.6) for px, py in foot], 1.6, soft=0.4) * 0.85)
    # one sheet from the foot down off the left edge (the sail's foot rope, made fast below)
    sheet_line = [(128, 168), (64, 206), (0, 238)]
    lay(depth.near_tone(ROPE, k=0.45, warm=0.10), mask_line(SHAPE, sheet_line, 3.0, soft=0.5))

    # --- the shrouds: a pair of heavy ropes crossing the top right corner, near us, thick
    def rope(p0, p1, w0, w1, seed):
        n = 40
        pts = [(p0[0] + (p1[0] - p0[0]) * s, p0[1] + (p1[1] - p0[1]) * s) for s in np.linspace(0, 1, n)]
        m = np.zeros((H, W), dtype=F32)
        for i in range(n - 1):
            m = np.maximum(m, mask_line(SHAPE, [pts[i], pts[i + 1]], w0 + (w1 - w0) * i / (n - 2), soft=0.6))
        base = depth.near_tone(ROPE, k=0.50, warm=0.10)
        c = np.broadcast_to(base, (H, W, 3)).copy()
        # the lay of the rope: dark twists across it
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy)
        u = ((x - p0[0]) * dx + (y - p0[1]) * dy) / L
        v = ((x - p0[0]) * -dy + (y - p0[1]) * dx) / L
        twist = (np.sin((u * 0.55 + v * 0.9)) > 0.55).astype(F32)
        c = lerp(c, depth.near_tone(lerp(SIENNA, PRUSSIAN, 0.3), k=0.5, warm=0.05)[None, None, :], (twist * 0.55)[..., None])
        lay(c, m)
        lay(rimc, depth.rim(m, LIGHT, 1.6) * 0.9)
        return m

    rope((636, -6), (806, 298), 11.0, 16.0, SEED + 3)
    rope((684, -6), (806, 214), 10.0, 14.0, SEED + 4)
    # their seizing: a band of small stuff lashing the pair together, where they come nearest
    for k in range(5):
        a0 = (756 + k * 2.6, 140 + k * 4.4)
        lay(depth.near_tone(lerp(SIENNA, PRUSSIAN, 0.35), k=0.45, warm=0.06), mask_line(SHAPE, [(a0[0] - 22, a0[1] + 13), (a0[0] + 18, a0[1] - 10)], 2.0, soft=0.5))

    # --- the near bulwark's rail, left standing only at the two bottom corners (the rest is cut away: the stage's wall)
    def rail(top, bottom_x0, bottom_x1, post_xs):
        poly = top + [(bottom_x1, 606), (bottom_x0, 606)]
        m = mask_poly(SHAPE, poly, soft=0.6, wobble=0.6, seed=SEED + 5)
        wood = depth.near_tone(WOOD_MID, k=0.60, warm=0.12)
        c = lerp(wood[None, None, :], depth.near_tone(WOOD_MID, k=0.72, warm=0.10)[None, None, :], np.clip((y - 560) / 40.0, 0, 1)[..., None])
        c *= (1 + (noise(SHAPE, 18, SEED + 6, 3) - 0.5) * 0.12)[..., None]
        lay(c, m)
        # the cap rail's top: lit by the high sun (a warm strip)
        cap = mask_line(SHAPE, [(px, py + 1.5) for px, py in top], 3.2, soft=0.5) * m
        lay(lerp(tintw(OCHRE, 0.25), NAPLES, 0.35), cap * 0.9)
        # under the cap, a dark line (its shadow), and the planks' seams below it
        lay(depth.near_tone(lerp(SIENNA, PRUSSIAN, 0.4), k=0.6, warm=0.05), mask_line(SHAPE, [(px, py + 5.0) for px, py in top], 1.6, soft=0.5) * m)
        for off in (16, 30):
            lay(depth.near_tone(lerp(SIENNA, PRUSSIAN, 0.4), k=0.6, warm=0.05), mask_line(SHAPE, [(px, py + off) for px, py in top], 1.0, soft=0.5) * m * 0.7)
        for px in post_xs:
            ty = np.interp(px, [p[0] for p in top], [p[1] for p in top])
            pm = mask_poly(SHAPE, [(px - 5, ty - 9), (px + 5, ty - 10), (px + 6, 606), (px - 6, 606)], soft=0.5)
            lay(depth.near_tone(WOOD_MID, k=0.66, warm=0.12), pm)
            lay(lerp(tintw(OCHRE, 0.25), NAPLES, 0.35), mask_line(SHAPE, [(px - 4.5, ty - 9.5), (px + 4.5, ty - 10.5)], 2.0, soft=0.5) * 0.9)
            lay(rimc * 0.9, depth.rim(pm, LIGHT, 1.4) * 0.8)
        lay(rimc * 0.9, depth.rim(m, LIGHT, 1.4) * 0.6)
        return m

    # bottom left: rising with the sheer toward the bow, over the coil and the bucket
    rail([(-4, 516), (40, 528), (90, 546), (130, 562), (168, 576)], -4, 176, [26, 112])
    # bottom right: a short stub over the water cask (a blocked corner)
    rail([(724, 584), (760, 579), (806, 572)], 716, 806, [772])
    # the near plane is in shade: a last warm glaze over all of it, so install's keying keeps it warm
    return np.clip(col, 0, 1), np.clip(alpha, 0, 1)


# ================================================================ the backdrop, deepened
def deepen(back):
    x, y = grid(SHAPE)
    walk = mask_poly(SHAPE, WALK)
    for b in BLOCKED:
        walk *= 1 - mask_poly(SHAPE, b)
    L = back @ np.array([0.299, 0.587, 0.114], dtype=F32)
    plank = walk * (back[..., 0] > back[..., 2] + 0.06) * (L > 0.42)          # open deck, plank-coloured (not shadow, not things)

    # the near walkway deeper toward us (a warm glaze, the bottom rows most)
    near = np.clip((y - 500) / 100.0, 0, 1) ** 1.2 * walk
    glaze = lerp(np.ones(3, dtype=F32), lerp(SIENNA, PRUSSIAN, 0.15) * 1.6, 0.30)
    back[...] = back * (1 - near[..., None]) + back * glaze * near[..., None]

    # the planks: butt joints and treenails through the camera (they run along the ship, x; 24 cm wide)
    marks = np.zeros((H, W), dtype=F32)
    pegs = np.zeros((H, W), dtype=F32)
    pt = lambda X, Z: gp(X, Z)
    for (px, py, k, r) in depth.scatter(pt, lambda X, Z: kz(Z), (-560, 760, -55, 540), 2.2, SEED + 10, size=(24, 1, 1)):
        if plank[int(py), int(px)] < 0.5:
            continue
        X = (px - 400) / k
        Z = 800.0 / k - 875.0
        zb = math.floor(Z / 24.0) * 24.0
        p0, p1 = gp(X, zb), gp(X, zb + 24.0)
        marks = np.maximum(marks, mask_line(SHAPE, [p0, p1], max(0.6, 1.4 * k), soft=0.4) * (0.55 + 0.3 * r))
        for dz in (6.0, 18.0):
            q = gp(X + 4.0, zb + dz)
            rr = max(0.5, 1.3 * k)
            if 0 <= q[0] < W and 0 <= q[1] < H:
                pegs = np.maximum(pegs, np.clip(1.2 - np.hypot(x - q[0], y - q[1]) / rr, 0, 1) * 0.5)
    seamc = lerp(SIENNA, PRUSSIAN, 0.45)
    m = np.clip(marks, 0, 1) * plank
    back[...] = back * (1 - m[..., None] * 0.55) + seamc * (m[..., None] * 0.55)
    p = np.clip(pegs, 0, 1) * plank
    back[...] = back * (1 - p[..., None] * 0.5) + lerp(SIENNA, PRUSSIAN, 0.3) * (p[..., None] * 0.5)

    # the shrouds' noon shadows: two thin hard lines coming in from the right edge across the stern deck toward the
    # windlass (each shroud from the near rail aft, x 700 and 760, to the masthead; its shadow along the sun)
    def shroud_shadow(X0):
        a = (X0 + SUN[0] * 100, -60 + SUN[1] * 100)
        mast = (-120 + SUN[0] * 1500, 240 + SUN[1] * 1500)
        pts = []
        for s in np.linspace(0, 1, 40):
            X, Z = a[0] + (mast[0] - a[0]) * s, a[1] + (mast[1] - a[1]) * s
            if Z > far_z(X) - 4:
                break
            pts.append(gp(X, Z))
        return pts
    sh = np.zeros((H, W), dtype=F32)
    for X0, wd in ((700.0, 3.0), (760.0, 3.2)):
        pts = shroud_shadow(X0)
        if len(pts) > 1:
            sh = np.maximum(sh, mask_line(SHAPE, pts, wd, soft=0.7))
    sh *= walk * (L > 0.30)
    depth_shadow(back, sh * 0.55)

    # the sail's shadow, short and hard, on the far bulwark's inner face (its foot is 4.5 to 5.5 m up: its shadow
    # comes down the bulwark and onto the deck just inside it), where the bulwark shows between the holds and astern
    far = np.zeros((H, W), dtype=F32)
    for px in range(W):
        X = None
        # the bulwark's column: the picture x at the far bulwark's depth
        Z = FAR_Z_AT(px)
        k = kz(Z)
        X = (px - 400) / k
        top = gp(X, far_z(X), sheer(X))[1]
        foot = gp(X, far_z(X) - 70.0)[1]
        far[int(max(top + 6, 0)):int(min(foot, H)), px] = 1.0
    far = blur(far, 0.8) * (1 - mask_poly(SHAPE, SEA)) * (back[..., 0] > back[..., 2]) * (L > 0.35)
    cols = (((x >= 284) & (x <= 372)) | ((x >= 532) & (x <= 668))).astype(F32)   # the gangway and astern, not the holds' mats
    far *= blur(cols, 1.0)
    depth_shadow(back, far * 0.42)

    # air: the far sea toward the sky at the horizon
    sky = back[HZ - 8:HZ - 2].reshape(-1, 3).mean(axis=0)
    sea = mask_poly(SHAPE, SEA) * (y >= HZ)
    farmap = np.clip(1 - (y - HZ) / 120.0, 0, 1) ** 1.6
    depth.air(back, farmap, sky, amount=0.30, mask=sea)
    return back, sky, walk


def FAR_Z_AT(px):
    return 540.0


def depth_shadow(back, m):
    c = DECK_SHADOW
    m = np.clip(m, 0, 1)[..., None]
    back[...] = back * (1 - m) + back * (c * 1.25) * m
    np.clip(back, 0, 1, out=back)


def wet_map():
    x, y = grid(SHAPE)
    wet = np.zeros((H, W), dtype=F32)
    wet[y < HZ - 1] = 1.0
    sea = mask_poly(SHAPE, SEA) * (y >= HZ - 1)
    ramp = 0.75 - 0.55 * np.clip((y - HZ) / (404.0 - HZ), 0, 1)
    wet = np.maximum(wet, sea * ramp)
    # the cape (in the swell layer, above the horizon): far land
    cape = mask_poly(SHAPE, [[0, 236], [130, 236], [250, 250], [272, 262], [0, 262]], soft=4)
    wet = wet * (1 - cape) + cape * 0.6
    return blur(wet, 2.0).astype(F32)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    back0, _ = load("back.png")
    back, sky, walk = deepen(back0.copy())
    WET = wet_map()

    # the swell layer: the cape and the far sea toward the sky (air), before the wash
    sw_c, sw_a = load("swell.png")
    x, y = grid(SHAPE)
    farmap = np.where(y < HZ, 1.0, np.clip(1 - (y - HZ) / 40.0, 0, 1)).astype(F32)
    depth.air(sw_c, farmap, sky, amount=0.32)

    near_c, near_a = near_plane()
    unwashed = back.copy()
    washed = watercolor.wash(back, seed=SEED, soft=WET, wander=1.4, fleck=0.3)
    finish(washed, OUT + "/back.png", 152)
    print("back")

    for name, n in CUTS.items():
        c, a = (sw_c, sw_a) if name == "swell" else load(name + ".png")
        if name == "swell":
            out = watercolor.wash_cut(c, a, unwashed, seed=SEED, soft=WET, wander=1.4, fleck=0.3, crisp=False)
        else:
            out = watercolor.wash_cut(c, a, unwashed, seed=SEED, soft=WET, wander=1.4, fleck=0.3, crisp=True)
        finish(out, OUT + f"/{name}.png", n, a)
        print(name)
    out = watercolor.wash_cut(near_c, near_a, unwashed, seed=SEED, soft=WET, wander=1.4, fleck=0.3, crisp=True)
    finish(out, OUT + "/near.png", 64, near_a)
    print("near", round(float((near_a > 0.5).mean()) * 100, 1), "%")

    # the floating cask's frames and the layout as they were
    for f in glob.glob(ORIG + "/cask-*.png") + [ORIG + "/layout.json"]:
        shutil.copy2(f, OUT + "/" + os.path.basename(f))

    comp = Image.open(OUT + "/back.png").convert("RGBA")
    for name in ["swell", "sail", "rigging", "mast", "windlass", "tiller", "compass-shut", "pot", "front", "near"]:
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(OUT + "-depth-comp.png")
    print("done")

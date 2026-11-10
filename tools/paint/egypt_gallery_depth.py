"""The great gallery, deepened (round twenty-three, the fast depth pass: DEPTH.md).

    python3 egypt_gallery_depth.py

Works over the painting as installed (out/egypt-gallery-orig/: the full, seeded run of egypt_gallery.py, never changed)
and writes the scene's whole set back into out/egypt-gallery/: back.png deepened, the cut-outs as they were, and near.png.

  near.png   The front plane: the near ends of the gallery's two corbelled side walls, each standing in from its wall by
             one lap's breadth more and ending a short way in front of us, so that they are larger than the walls behind
             them and cut off by the frame: their faces and the undersides of their laps in deep warm shade, a rim of the
             gallery's lamplight along their inner edges, a warm bounce from the floor low down. With them, the stretch of
             the left wall the ladder leans on (the ladder over it, exactly as it was in front.png): so the ladder lies on
             the front plane, and nothing that is clicked or stood on is behind it.
  back.png   The floor's joints and the sledges' two worn grooves running up the ramp, grit and chips through the camera
             (few and large near us, many and small far off); the lamplight's pools on floor and benches; the long shadow
             the level bench throws across the foot from the lamp at the front (its edge runs in from the bottom of the
             frame); the far end of the gallery darker and cooler; the near floor deeper.

One camera: everything through egypt_gallery_kit (its own true perspective; the cast of every pixel)."""

import os
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, blur, grid, lerp, noise, rgb, palette_of, to_palette, save, Sheet
import depth as D
import egypt_gallery_kit as K
import egypt_gallery as G

SRC, OUT = "out/egypt-gallery-orig", "out/egypt-gallery"
H, W = 600, 800
SHAPE = (H, W)
CUTS = ("front.png", "mirror-foot.png", "mirror-top.png", "layout.json")

# the front plane's two ends: how much further in each stands than its wall (cm), and where it ends (Z, cm)
NEAR_L = (16.0, 192.0)
NEAR_R = (22.0, 204.0)

# the scene file's areas that lie on the floor or stand on it (nothing new is laid over them)
AREAS = {
    "chest": [[455, 236], [475, 236], [484, 258], [483, 277], [455, 277], [452, 258]],
    "dinner": [[290, 320], [300, 317], [310, 322], [315, 333], [324, 337], [326, 349], [318, 355], [300, 354], [290, 343]],
    "runner": [[465, 299], [479, 297], [497, 410], [484, 413]],
    "low": [[376, 389], [425, 389], [425, 438], [376, 438]],
    "slot": [[518, 396], [553, 394], [557, 415], [562, 422], [560, 452], [528, 452], [522, 422]],
    "jars": [[233, 446], [243, 440], [256, 442], [262, 452], [268, 446], [278, 447], [283, 462], [284, 492], [300, 492], [302, 503], [314, 508], [313, 519], [296, 519], [285, 513], [262, 513], [247, 516], [234, 508], [230, 470]],
    "rope": [[533, 511], [530, 516], [522, 520], [510, 521], [498, 520], [490, 516], [487, 511], [490, 506], [498, 502], [510, 501], [522, 502], [530, 506]],
    "step": [[364, 198], [436, 198], [441, 218], [359, 218]],
    "door": [[381, 152], [419, 152], [419, 197], [381, 197]],
    "marks": [[571, 338], [584, 337], [592, 358], [599, 362], [616, 363], [618, 394], [626, 417], [624, 432], [614, 428], [598, 414], [574, 392], [570, 360]],
}
LADDER = [[97, 241], [108, 241], [131, 243], [138, 247], [157, 600], [92, 600]]
FX = [(282.6, 374.7, 377), (326.1, 252.9, 254), (337, 220.2, 221), (496.2, 299.7, 302), (466.9, 221.2, 222), (309.2, 512.2, 515), (560, 468.3, 472)]


def load(name):
    a = np.asarray(Image.open(f"{SRC}/{name}").convert("RGBA"), dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def poly(points, grow=0):
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    d.polygon([(float(x), float(y)) for x, y in points], fill=255)
    if grow:
        d.line([(float(x), float(y)) for x, y in points] + [tuple(map(float, points[0]))], fill=255, width=int(grow * 2))
    return np.asarray(im, dtype=F32) / 255


def smooth(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return (t * t * (3 - 2 * t)).astype(F32)


def lum(c):
    return c @ np.array([0.3, 0.55, 0.15], dtype=F32)


# ---------------------------------------------------------------- the front plane
def near_end(side, d, zn):
    """The near end of one side wall: the gallery cast again with that wall standing `d` cm further in, kept only where
    it is nearer than `zn`. -> (mask, cast)."""
    h0 = K.HALF
    K.HALF = h0 - d
    try:
        c = K.cast(ss=1)
    finally:
        K.HALF = h0
    sid, Z = c["sid"], c["Z"]
    w0, s0 = (K.WALL_L, K.SOFF_L) if side < 0 else (K.WALL_R, K.SOFF_R)
    m = (((sid >= w0) & (sid <= w0 + K.NCOR)) | ((sid >= s0) & (sid <= s0 + K.NCOR))) & (Z < zn)
    if side < 0:
        m &= c["X"] < 0
    else:
        m &= c["X"] > 0
    return m, c


def paint_near(m, c, side, zn, seed):
    """Deep warm shade, stone by stone: the faces of the laps, the undersides darker, the lamplight of the gallery along
    the inner edge and on the end of each lap, a little warmth bounced up from the floor."""
    sid, X, Y, Z, h = c["sid"], c["X"], c["Y"], c["Z"], c["h"]
    w0, s0 = (K.WALL_L, K.SOFF_L) if side < 0 else (K.WALL_R, K.SOFF_R)
    face = (sid >= w0) & (sid <= w0 + K.NCOR)
    lap = np.where(face, sid - w0, sid - s0).astype(np.int32)
    rows = [-400.0] + [K.LIP0 + K.COURSE * n for n in range(K.NCOR + 1)] + [2000.0]
    tone, da, db = K.blocks(Z.astype(np.float64), h.astype(np.float64), rows, seed, length=(110.0, 210.0), start=-200.0, stop=900.0)
    cpp_z = K.per_px(Z, sid)
    cpp_h = K.per_px(h, sid)
    stone_face = rgb("#5a3e30")
    stone_deep = rgb("#0d0909")
    under = rgb("#0b0708")
    rng = np.random.default_rng(seed)
    lap_tone = (1 + (rng.random(K.NCOR + 2) - 0.5) * 0.16).astype(F32)
    toward = smooth(zn - 120.0, zn, Z)                                   # the end of each lap, toward the lamps
    low = smooth(260.0, 60.0, Y)                                         # near the floor: warmth bounced up
    lo = np.where(lap > 0, K.LIP0 + K.COURSE * (lap - 1), -400.0)          # where each lap starts, above the ramp
    within = np.clip((h - lo) / np.where(lap > 0, K.COURSE, K.LIP0 + 400.0), 0, 1)
    overhang = 1.0 - 0.55 * smooth(0.35, 1.0, within)                      # each lap shades the top of the one below it
    end = smooth(zn - 30.0, zn, Z) ** 2                                     # the very end of the lap, toward the lamps
    k = (0.17 + 0.30 * end + 0.10 * low) * overhang * lap_tone[np.clip(lap, 0, K.NCOR + 1)] * (0.62 + 0.76 * tone)
    k = k * (0.92 + (noise(SHAPE, 9, seed + 3, 3) - 0.5) * 0.22)
    col = lerp(stone_deep, stone_face, np.clip(k, 0, 1.2)[..., None] / 1.0)
    col = np.where(face[..., None], col, under * (0.8 + 0.5 * toward[..., None]))
    joint = np.clip(1.2 - da / np.maximum(cpp_z, 0.2), 0, 1) * face + np.clip(1.2 - db / np.maximum(cpp_h, 0.2), 0, 1) * face
    col = col * (1 - 0.55 * np.clip(joint, 0, 1)[..., None])
    # the lip of each lap: its lower arris catches the light from below
    e = K.edges(sid) * m
    lip = blur(e, 0.6) * face
    col = col + lip[..., None] * rgb("#a8683c") * 0.35 * (0.4 + 0.6 * toward[..., None])
    # the lamplight wrapping round the end of each lap, soft
    col = col + (smooth(zn - 18.0, zn, Z) ** 2 * face * 0.10)[..., None] * rgb("#d08a4c")
    return np.clip(col, 0, 1).astype(F32)


# ---------------------------------------------------------------- the backdrop
def deepen(back, g, quiet):
    sid, X, Y, Z, h = g["sid"], g["X"], g["Y"], g["Z"], g["h"]
    pic = back.copy()
    y, x = np.mgrid[0:H, 0:W].astype(F32)
    floorish = np.isin(sid, [K.LANDING, K.RAMP_S, K.TRENCH, K.LEDGE_TOP, K.PASS_FLOOR]).astype(F32)
    benches = np.isin(sid, [K.BTOP_L, K.BTOP_R, K.STEP_T]).astype(F32)
    ground = np.clip(floorish + benches, 0, 1)

    # -- the long shadow of the level bench across the foot, from the lamp at the front on it (198, 62, 424): a floor
    #    place is in it when the bench's inner edge (X 160, 55 cm up) stands between it and the flame
    lx, ly = 198.0, 62.0
    Xs = np.minimum(X, 159.0)
    t = (160.0 - Xs) / np.maximum(lx - Xs, 1.0)
    over = ly * t + Y * (1 - t)                                          # how high the ray to the flame passes the bench's edge
    shade = smooth(4.0, -16.0, over - 55.0) * (Y < 50) * (Z < 900) * floorish
    shade = blur(shade.astype(F32), 2.2) * (1 - quiet)
    D.shadow_on_ground  # (the same glaze, laid here through the kit's own cast)
    c = rgb("#3a2c44") * 1.5
    a = (shade * 0.30)[..., None]
    pic = pic * (1 - a) + pic * c * a
    lit = (1 - shade) * floorish * smooth(900.0, 420.0, Z) * (Y < 50) * smooth(-40.0, -110.0, X) * (1 - quiet)
    pic = pic + (lit * 0.06)[..., None] * G.WARM

    # -- the lamplight's pools, on the floor and the benches round every lamp
    pool = np.zeros(SHAPE, F32)
    for (LX, LY, LZ, power, kind) in G.LAMPS:
        if kind == "hidden":
            continue
        d2 = (X - LX) ** 2 + (Y - LY) ** 2 + (Z - LZ) ** 2
        pool += power * np.exp(-d2 / (2 * 70.0 ** 2)) * (1.0 * ground + 0.35 * (1 - ground))
    pool = np.clip(pool, 0, 1.2)
    pic = 1 - (1 - pic) * (1 - (pool * 0.30)[..., None] * G.WARM)

    # -- the floor's joints and the sledges' grooves, through the camera: two worn grooves up the middle of the ramp,
    #    beside the cut, from the foot of the frame to the step
    cpp_x = K.per_px(X, sid)
    run = np.isin(sid, [K.LANDING, K.RAMP_S]).astype(F32) * (1 - quiet)
    for gx in (-74.0, 74.0):
        hw = 4.5
        d = np.abs(X - gx) / np.maximum(hw, 0.55 * cpp_x)
        core = np.clip(1.0 - d, 0, 1) ** 0.7 * run * (Z < K.Z_END - 30)
        lipm = np.clip(1.0 - np.abs(d - 1.35) / 0.45, 0, 1) * run * (Z < K.Z_END - 30) * (np.sign(X - gx) == np.sign(gx))
        fade = smooth(1650.0, 900.0, Z) * 0.6 + 0.4
        pic = pic * (1 - (core * 0.42 * fade)[..., None]) + (core * 0.42 * fade)[..., None] * pic * rgb("#3a2a34") * 1.4
        pic = pic + (lipm * 0.10 * fade)[..., None] * rgb("#ffcf8a") * np.clip(lum(pic) * 2.0, 0.2, 1.0)[..., None]
    # cracks: a few hairlines across the slabs, each slab its own
    sl = np.sqrt(1 + K.T ** 2)
    s_along = np.where(Z < K.Z1, Z - K.Z1, (Z - K.Z1) * sl)
    rng = np.random.default_rng(1830)
    crack = np.zeros(SHAPE, F32)
    for i in range(26):
        s0 = rng.uniform(-200, (K.Z_END - K.Z1) * sl)
        x0 = rng.uniform(-110, 110)
        ang = rng.uniform(-0.5, 0.5)
        ln = rng.uniform(30, 70)
        wig = noise(SHAPE, 6, 40 + i, 2) - 0.5
        u = (X - x0) * np.cos(ang) + (s_along - s0) * np.sin(ang)
        v = -(X - x0) * np.sin(ang) + (s_along - s0) * np.cos(ang) + wig * 6.0
        cw = np.maximum(0.9, 0.5 * cpp_x)
        crack += np.clip(1 - np.abs(v) / cw, 0, 1) * (np.abs(u) < ln) * smooth(ln, ln * 0.6, np.abs(u))
    crack = np.clip(crack, 0, 1) * run
    pic = pic * (1 - (crack * 0.35)[..., None])

    # -- grit and chips on the floor, few and large near us, many and small far off
    def pt(Xw, Zw):
        return K.P(Xw, 0.0, Zw) if Zw < K.Z1 else K.Pr(Xw, 0.0, Zw)

    sheet = Sheet(SHAPE)
    zone = (run > 0.5).astype(F32)
    for (px, py, k, r) in D.scatter(pt, lambda Xw, Zw: K.F / Zw, (-215.0, 155.0, 400.0, K.Z_END), 3.0, 1830, size=(3.0, 2.0), zone=zone):
        s = (1.2 + 2.6 * r) * k
        if s < 0.45:
            continue
        if r < 0.72:
            sheet.ellipse(px, py, max(0.5, s * 0.8), max(0.35, s * 0.36), "#2a1c1c", 0.45)
        else:
            sheet.ellipse(px, py - 0.4, max(0.4, s * 0.5), max(0.3, s * 0.22), "#e8c48c", 0.16)
    sc, sa = sheet.done()
    sa = sa * zone * (1 - quiet)
    pic = pic * (1 - sa[..., None]) + sc * sa[..., None]

    # -- the far end of the gallery darker and cooler; the doorway at the top keeps its own light
    far = smooth(760.0, 1820.0, Z) ** 1.1
    door = blur((sid == K.DOOR_IN).astype(F32), 4.0)
    door = np.clip(door * 3.0, 0, 1)
    m = far * 0.42 * (1 - 0.9 * door)
    cool = rgb("#18223f")
    pic = pic * (1 - m[..., None]) + (pic * 0.55 + cool * 0.45) * m[..., None]

    # -- the near floor deeper
    nm = smooth(470.0, 600.0, y) * 0.22 * floorish
    pic = pic * (1 - nm[..., None]) + pic * rgb("#4a3040") * 1.4 * nm[..., None]
    return np.clip(pic, 0, 1).astype(F32)


def finish_near(col, alpha, keep, keep_alpha, path):
    """Back to 8 bits: the painted near ends grained and reduced as the scene's own finish does it; the stretch behind
    the ladder (keep, already final) indexed exactly, without new speckle."""
    painted = alpha > 0.5
    g = G.grained(col, 7, 0.02)
    fin = np.where(keep_alpha[..., None] > 0.5, keep, g)
    sample = fin[painted]
    pal = palette_of([sample.reshape(-1, 1, 3)], colors=120)
    idx_a = to_palette(g, pal, speckle=0.014)
    idx_b = to_palette(keep, pal, speckle=0.0)
    idx = np.where(keep_alpha > 0.5, idx_b, idx_a).astype(np.uint8)
    save(path, idx, pal, painted.astype(F32))


def main():
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back.png")
    fc, fa = load("front.png")
    g = K.cast(ss=1)

    # what is not to be touched in the backdrop: the areas on the floor, the lamps
    quiet = np.zeros(SHAPE, F32)
    for pts in AREAS.values():
        quiet = np.maximum(quiet, poly(pts, grow=3))
    yy, xx = np.mgrid[0:H, 0:W].astype(F32)
    for (fx, fy, base) in FX:
        quiet = np.maximum(quiet, ((xx - fx) ** 2 + ((yy - fy) * 1.4) ** 2 < 14.0 ** 2).astype(F32))
    quiet = np.clip(blur(quiet, 1.2) * 1.5, 0, 1)

    if "near" not in sys.argv[1:] or not os.path.exists(OUT + "/back.png"):
        pic = deepen(back, g, quiet)
        G.finish(pic, OUT + "/back.png", 160, speckle=0.008)
    final_back = np.asarray(Image.open(OUT + "/back.png").convert("RGB"), dtype=F32) / 255

    # the front plane
    ml, cl = near_end(-1, *NEAR_L)
    mr, cr = near_end(1, *NEAR_R)
    col = np.zeros(SHAPE + (3,), F32)
    col = np.where(ml[..., None], paint_near(ml, cl, -1, NEAR_L[1], 21), col)
    col = np.where(mr[..., None], paint_near(mr, cr, 1, NEAR_R[1], 22), col)
    # worn arrises: small chips out of the inner edges
    for mm, lx in ((ml, 1.0), (mr, -1.0)):
        band = D.rim(mm.astype(F32), light=(lx, 0.0), width=2.2) > 0.25
        chip = noise(SHAPE, 7, 77 + int(lx), 2) > 0.80
        mm &= ~(band & chip)
    m = (ml | mr).astype(F32)
    # the rim: the gallery's lamplight along the inner edge of each
    rl = D.rim(ml.astype(F32), light=(1.0, 0.45), width=3.0)              # the lamps stand low, in the gallery
    rr_ = D.rim(mr.astype(F32), light=(-1.0, 0.45), width=3.0)
    rimc = rgb("#e7a058")
    rim_all = np.clip(rl + rr_, 0, 1) * (0.45 + 0.55 * smooth(0.35, 0.65, noise(SHAPE, 10, 91, 2)))
    col = col * (1 - rim_all[..., None] * 0.75) + (rim_all * 0.75)[..., None] * rimc * m[..., None]
    col = np.clip(col, 0, 1)
    # the stretch of wall behind the ladder, with the ladder on it, exactly as it is shown now
    lad = (poly(LADDER) > 0.5) & ~(m > 0.5)
    keep = final_back * (1 - fa[..., None]) + fc * fa[..., None]
    keep = np.round(keep * 255) / 255
    keep_alpha = lad.astype(F32)
    alpha = np.maximum(m, keep_alpha)
    finish_near(col, alpha, keep, keep_alpha, OUT + "/near.png")

    for f in CUTS:
        shutil.copyfile(os.path.join(SRC, f), os.path.join(OUT, f))
    # a look at it all together
    whole = final_back.copy()
    for f in ("front.png", "near.png"):
        c2, a2 = (lambda a: (a[..., :3], a[..., 3]))(np.asarray(Image.open(os.path.join(OUT, f)).convert("RGBA"), dtype=F32) / 255)
        whole = whole * (1 - a2[..., None]) + c2 * a2[..., None]
    Image.fromarray((whole * 255 + 0.5).astype(np.uint8)).save(OUT + "-depth-all.png")
    print("near share %.3f" % float(alpha.mean()))


if __name__ == "__main__":
    main()

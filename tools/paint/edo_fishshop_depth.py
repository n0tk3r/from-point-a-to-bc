"""Kihei's shop at Yui (edo-fishshop), about 8 April 1830, morning: the fast depth pass of round twenty-three (DEPTH.md;
/home/claude/r23/LITE.md). It works over the painting as edo_fishshop.py leaves it (and the cat's frames as
edo_fishshop_cat.py leaves them), copied once to out/edo-fishshop-orig/, and writes the scene's full set back into
out/edo-fishshop/: every file as before, plus near.png.

    python3 edo_fishshop_depth.py        out/edo-fishshop-orig/ -> out/edo-fishshop/ (and out/edo-fishshop-depth-look.png)

ONE CAMERA: edo_fishshop_model.VIEW (room.View: the lens 2.20 m up at the back of the earth floor, turned 6 degrees
right). THE LIGHT: the morning sun low over the bay, in front of us and a little to the right (it comes in through the
open front under the shop's outer eave): it lies across the earth floor in three patches, one to each bay, the posts'
shadows running in from their feet toward us and to the left, the noren's shadow across the middle one; the outer eave
(outside the picture, over the street) ends the patches 4 m in. Beyond them the floor falls away into the shop's own
shade, deepest nearest us.

    near     the eave's beam across the top (the head of the doorway we stand in, 1.1 to 1.3 m from the lens: its face in
             deep warm shade, its underside warmed by the floor's light, the far arris lit), a short noren hung under it
             across the top-left corner (a slit to see through), and round twenty's front.png made to count: the corner
             post and the firewood darker and warmer, each lit along the edge that faces the opening
    back     the sun's patches and every standing thing's shadow in them (through the camera: the tubs, the board on its
             trestles, the stand and box, the hearth, the raised floor, the chest, the money box), the skylight falling
             away inside, the near floor deeper; the tamped earth's own texture (blotches, a worn way from the door, damp
             by the tubs, pebbles and straw through depth.scatter); the view out a step paler in the air
    paper    watercolor.wash on the backdrop (WET: the sky 1.0, Fuji 0.6, the sea 0.75 at the horizon to 0.2 at the
             beach, nothing standing), wash_cut(crisp) on every cut-out and the near plane with the same seed over the
             unwashed backdrop; the cat's frames as they were. Then one palette of 255 for every file, as edo_fishshop.py
             finishes (grain 0.02 before it, speckle 0.014).
"""

import math
import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import F32, rgb, lerp, noise, grid, blur, grain, palette_of, to_palette, save, Sheet, over, tint, mask_poly, step, sample
import depth as D
import watercolor as WC
from room import View
import edo_fishshop_model as M

V = View(**M.VIEW)
SHAPE = (600, 800)
SRC = "out/edo-fishshop-orig"
OUT = "out/edo-fishshop"
SEED = 1830
CUTS = ["noren", "driedfish", "tub-1", "tub-2", "tub-3", "stand", "sushibox-empty", "sushibox-filled", "sushibox-cut",
        "hearth", "basket", "front"]

# the sun: horizontal way its light travels on the floor plan (X across, Z toward us), and its height
SUN_H = np.array([-0.33, 0.944], dtype=F32)
SUN_H /= np.linalg.norm(SUN_H)
TAN_E = math.tan(math.radians(30.0))
EAVE_OUT, EAVE_Y = 90.0, 300.0           # the shop's outer eave over the street (outside the picture)

SKY_LOW = rgb("#dfe8ee")
SUNLIT = rgb("#fff1d6")
GLAZE = rgb("#c9bdb6")                   # a cast shadow: a thin cool wash, multiplied
NEAR_SHADE = "#1a0d04"                   # the near plane's shade: deep and warm (the paper's lift is allowed for)
RIM = rgb("#d9a55e")


def load(name):
    a = np.asarray(Image.open(os.path.join(SRC, name + ".png")).convert("RGBA"), dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


# ---------------------------------------------------------------- the ground through the camera
def floor():
    """X, Z of the earth floor at every pixel, and the mask of the earth floor really seen in the backdrop."""
    X, Z, ok = V.floor_xz(SHAPE, 0.0)
    m = ok * (X > 0.5) * (Z > 0.5) * (Z < 1100)
    m = m * ((X < 419.0) | (Z < 179.0))                                    # the strip before the raised floor too
    m = m * (X < 639.0)
    # the cutting board on its trestles is painted in the backdrop: not floor
    bx0, bx1, by0, by1, bz0, bz1 = M.BOARD
    hull = [V.pt(bx0 - 2, 0, bz0 - 2), V.pt(bx0 - 2, by1 + 1, bz0 - 2), V.pt(bx1 + 2, by1 + 1, bz0 - 2), V.pt(bx1 + 2, by1 + 1, bz1 + 2),
            V.pt(bx1 + 2, 0, bz1 + 2), V.pt(bx0 - 2, 0, bz1 + 2)]
    m = m * (1 - mask_poly(SHAPE, hull))
    return X, Z, m.astype(F32)


def opening_pass(X0, Y0):
    """How much of the sun gets through the open front at a point of the opening plane (Z 0): 0 to 1."""
    ok = (X0 > 0) & (X0 < 640) & (Y0 > 0) & (Y0 < 280)
    for p in M.POSTS:
        ok &= np.abs(X0 - p) > M.POST_T / 2
    t = ok.astype(F32)
    # the outer eave: a ray that left the street under it at Z -EAVE_OUT must pass below EAVE_Y there
    t *= (Y0 + EAVE_OUT / SUN_H[1] * TAN_E < EAVE_Y)
    nx0, nx1, ny0, ny1 = M.NOREN
    t *= np.where((X0 > nx0) & (X0 < nx1) & (Y0 > ny0) & (Y0 < ny1), 0.18, 1.0)        # the noren lets a little through
    return t


BOXES = [M.STAND, M.SUSHIBOX, M.HEARTH, (420, 640, 0, 45, 180, 1000), M.CHEST, M.MONEYBOX,
         (M.BOARD[0], M.BOARD[1], M.BOARD[2], M.BOARD[3], M.BOARD[4], M.BOARD[5]),
         (18, 72, 0, 70, M.TRESTLE_Z[0] - 3, M.TRESTLE_Z[0] + 3), (18, 72, 0, 70, M.TRESTLE_Z[1] - 3, M.TRESTLE_Z[1] + 3)]
CYLS = [(tx, tz, r, 0, h) for tx, tz, r, h in M.TUBS] + [(M.POT[0], M.POT[1], M.POT[2], M.HEARTH[3] - 4, M.HEARTH[3] + M.POT[3])]


def sunlight(X, Z, Y, m):
    """The sun on a level surface at height Y (where m): through the opening, less what stands in its way."""
    lit = np.zeros(SHAPE, F32)
    idx = m > 0
    x, z = X[idx], Z[idx]
    s = z / SUN_H[1]                                                         # back along the ray to the opening
    X0 = x - SUN_H[0] * s
    Y0 = Y + TAN_E * s
    t = opening_pass(X0, Y0) * (z > 0)
    for k in np.linspace(0.0, 1.0, 46) ** 1.6 * 240.0:                     # what stands near: boxes and tubs
        if not np.any(t > 0):
            break
        px_, pz_ = x - SUN_H[0] * k, z - SUN_H[1] * k
        py_ = Y + TAN_E * k
        hit = np.zeros(px_.shape, bool)
        for bx0, bx1, by0, by1, bz0, bz1 in BOXES:
            hit |= (px_ > bx0) & (px_ < bx1) & (py_ > by0) & (py_ < by1) & (pz_ > bz0) & (pz_ < bz1)
        for cx_, cz_, r, y0_, y1_ in CYLS:
            hit |= ((px_ - cx_) ** 2 + (pz_ - cz_) ** 2 < r * r) & (py_ > y0_) & (py_ < y1_)
        t = np.where(hit & (k > 0.5), 0.0, t)
    lit[idx] = t
    return blur(lit, 0.9)


TILE = {}


def ground_noise(X, Z, cell, seed, octaves=3):
    """Noise lying on the floor, its blotches `cell` cm across, fading where a blotch would be under a pixel."""
    tile = TILE.get(seed)
    if tile is None:
        tile = TILE[seed] = noise((1024, 1024), 64, seed, octaves)

    def fold(t):
        mm = np.mod(t, 2 * 1022)
        return np.where(mm > 1022, 2 * 1022 - mm, mm)
    n = sample(tile, fold(X / cell * 64 + 300), fold(Z / cell * 64 + 300))
    k = np.clip(V.F / np.maximum(V.cam_z - Z, 30.0), 0, 20)
    return (0.5 + (n - 0.5) * np.clip((cell * k - 1.0) / 2.5, 0, 1)).astype(F32)


def seg_dist(X, Z, pts):
    d = np.full(X.shape, 1e9, F32)
    for (ax, az), (bx, bz) in zip(pts[:-1], pts[1:]):
        vx, vz = bx - ax, bz - az
        t = np.clip(((X - ax) * vx + (Z - az) * vz) / (vx * vx + vz * vz), 0, 1)
        d = np.minimum(d, np.hypot(X - ax - t * vx, Z - az - t * vz))
    return d


def deepen(back):
    pic = back.copy()
    x, y = grid(SHAPE)
    X, Z, fm = floor()
    # ---- the tamped earth's own texture: blotches, a worn way from the door, damp by the tubs and the board
    n1 = ground_noise(X, Z, 70.0, 11)
    n2 = ground_noise(X, Z, 18.0, 12)
    tex = 1 + (n1 - 0.5) * 0.20 + (n2 - 0.5) * 0.12
    worn = np.exp(-(seg_dist(X, Z, [(300, 30), (320, 140), (380, 240), (400, 300)]) / 38.0) ** 2) * 0.55
    worn += np.exp(-(seg_dist(X, Z, [(300, 30), (250, 200), (220, 360), (230, 420)]) / 34.0) ** 2) * 0.45
    worn *= 0.6 + 0.8 * ground_noise(X, Z, 40.0, 13)
    damp = np.clip((ground_noise(X, Z, 34.0, 14) - 0.42) * 4, 0, 1) * np.exp(-(seg_dist(X, Z, [(60, 40), (120, 110), (90, 200), (110, 300)]) / 45.0) ** 2)
    col = pic * tex[..., None]
    col = lerp(col, np.clip(pic * 1.10 + 0.02, 0, 1), np.clip(worn, 0, 1)[..., None] * 0.8)
    col = col * (1 - 0.22 * damp)[..., None]
    pic = lerp(pic, col, fm[..., None])
    # ---- the morning light: the sun's patches (and every shadow in them), the sky's light falling away inside
    sun = sunlight(X, Z, 0.0, fm) * fm
    Xt, Zt, okt = V.floor_xz(SHAPE, float(M.STEP_Y))
    tm = okt * (Xt > 421) * (Xt < 639) * (Zt > M.BACKWALL_Z + 1) * (Zt < 700)
    # (the tatami seen: where the raised floor's top is nearer than the earth floor behind it)
    tm = tm * (1 - fm) * (y > 330)
    sun_t = sunlight(Xt, Zt, float(M.STEP_Y), tm) * tm
    sky = np.exp(-np.clip(Z, 0, 2000) / 300.0) * fm
    shade_far = step(380.0, 880.0, Z) * fm                                  # the near floor deeper
    for s_, m_ in ((sun, fm), (sun_t, tm)):
        lift = (0.40 * s_)[..., None]
        pic = pic * (1 - lift) + np.clip(pic * SUNLIT * 1.42, 0, 1) * lift
        g = np.clip(m_ - s_, 0, 1) * 0.30
        tint(pic, GLAZE, g)
    pic = pic * (1 + 0.10 * sky)[..., None]
    tint(pic, rgb("#a8907c"), (shade_far * 0.48).astype(F32))
    # ---- what lies on the floor, through the camera: pebbles, straw, a few cracks (few and large near, small far)
    sh = Sheet(SHAPE)
    pt = lambda X_, Z_: V.pt(X_, 0, Z_)
    k_ = lambda X_, Z_: V.scale_at(X_, Z_)
    zone = (fm > 0.5).astype(F32)
    rng = np.random.default_rng(SEED)
    for (px_, py_, k, r) in D.scatter(pt, k_, (0, 640, 0, 900), 14.0, SEED + 1, size=(2.0, 1.5), zone=zone):
        rr = (0.8 + 1.6 * r) * k
        lum = float(pic[int(py_), int(px_)].mean())
        dark = np.clip(pic[int(py_), int(px_)] * 0.62, 0, 1)
        sh.ellipse(px_, py_, max(rr, 0.5), max(rr * 0.45, 0.4), dark, 0.75)
        sh.ellipse(px_ - rr * 0.2, py_ - rr * 0.18, max(rr * 0.6, 0.4), max(rr * 0.25, 0.3), np.clip(pic[int(py_), int(px_)] * 1.25 + 0.04, 0, 1), 0.7 if lum > 0.2 else 0.4)
    for (px_, py_, k, r) in D.scatter(pt, k_, (0, 640, 0, 900), 2.2, SEED + 2, size=(9.0, 0.6), zone=zone):
        ln = (5 + 7 * r) * k
        a = rng.uniform(0, math.pi)
        dx, dy = math.cos(a) * ln, math.sin(a) * ln * 0.45
        sh.line([(px_ - dx / 2, py_ - dy / 2), (px_ + dx / 2, py_ + dy / 2)], rgb("#b49a5c"), max(0.5, 0.6 * k), 0.75)
    for (px_, py_, k, r) in D.scatter(pt, k_, (0, 640, 300, 900), 0.35, SEED + 3, size=(40.0, 0.5), zone=zone):
        pts_ = [(px_, py_)]
        for j in range(4):
            a = rng.uniform(-0.6, 0.6) + (0 if j % 2 else math.pi * 0.1)
            pts_.append((pts_[-1][0] + math.cos(a) * 9 * k, pts_[-1][1] + math.sin(a) * 2.5 * k))
        sh.line(pts_, np.clip(pic[int(py_), int(px_)] * 0.55, 0, 1), max(0.5, 0.35 * k), 0.6)
    c, a = sh.done()
    over(pic, c, a * fm)
    # ---- the view out a step paler in the air (the sky, Fuji, the sea, the beach, the street beyond the posts)
    u, v, ok = V.plane_uv(SHAPE, "Z", 0.0)
    view = ok * (u > 2) * (u < 638) * (v > 1) * (v < 279)
    for p in M.POSTS:
        view = view * (np.abs(u - p) > M.POST_T / 2 + 1.5)
    for r_ in ((553, 279, 110, 95), (410, 318, 86, 39), (40, 300, 112, 60), (270, 158, 147, 56)):
        view = view * (1 - ((x >= r_[0]) & (x < r_[0] + r_[2]) & (y >= r_[1]) & (y < r_[1] + r_[3])))
    view = view * (1 - fm) * (y < 352)
    far = np.where(y < 200, 1.0, np.clip(1 - (y - 200) / 160.0, 0.35, 1.0)).astype(F32)
    D.air(pic, far, SKY_LOW, amount=0.24, mask=blur(view.astype(F32), 0.6))
    return np.clip(pic, 0, 1).astype(F32), view, fm


def wet_map(view):
    """watercolor's `soft`: 1 the sky, 0.6 Fuji, the sea 0.75 at the horizon to 0.2 at the beach; nothing standing."""
    x, y = grid(SHAPE)
    sea = np.clip(0.75 - (y - 200) / 90.0 * 0.55, 0.2, 0.75)
    w = np.where(y < 199, 1.0, np.where(y < 290, sea, 0.0)).astype(F32)
    fuji = ((x > 480) & (x < 650) & (y < 205) & (y > 150)).astype(F32)
    w = w * (1 - fuji) + 0.6 * fuji * (y < 199)
    racks = ((x > 136) & (x < 222) & (y > 160) & (y < 220)).astype(F32)       # the drying racks on the beach: standing
    w = w * (1 - racks)
    return (w * blur(view.astype(F32), 1.0)).astype(F32)


# ---------------------------------------------------------------- the near plane
BEAM = dict(y0=248.0, y1=290.0, z0=862.0, z1=888.0)


def near_plane(back):
    sh_fill = Sheet(SHAPE)
    parts = {}
    b = BEAM
    Xs = (120.0, 560.0)
    # the beam: its face toward us (in its own shade), its underside (warmed by the floor's light), the far arris lit
    face = [V.pt(Xs[0], b["y0"], b["z1"]), V.pt(Xs[1], b["y0"], b["z1"]), V.pt(Xs[1], b["y1"] + 60, b["z1"]), V.pt(Xs[0], b["y1"] + 60, b["z1"])]
    under = [V.pt(Xs[0], b["y0"], b["z0"]), V.pt(Xs[1], b["y0"], b["z0"]), V.pt(Xs[1], b["y0"], b["z1"]), V.pt(Xs[0], b["y0"], b["z1"])]
    wood = D.near_tone(rgb("#5a3d24"), NEAR_SHADE, k=0.85, warm=0.03)
    wood_u = D.near_tone(rgb("#7a5634"), NEAR_SHADE, k=0.70, warm=0.04)
    sh = Sheet(SHAPE)
    sh.poly(face, wood)
    sh.poly(under, wood_u)
    rng = np.random.default_rng(SEED + 20)
    for j in range(7):                                                      # the grain along the face and the underside
        yy = b["y0"] + rng.uniform(2, 40)
        sh.line([V.pt(Xs[0], yy, b["z1"]), V.pt(Xs[1], yy + rng.uniform(-1, 1), b["z1"])], np.clip(wood * 0.78, 0, 1), rng.uniform(0.6, 1.4), 0.55)
    for j in range(4):
        zz = rng.uniform(b["z0"] + 3, b["z1"] - 3)
        sh.line([V.pt(Xs[0], b["y0"], zz), V.pt(Xs[1], b["y0"], zz + rng.uniform(-1, 1))], np.clip(wood_u * 0.82, 0, 1), rng.uniform(0.6, 1.1), 0.5)
    sh.line([V.pt(Xs[0], b["y0"], b["z1"]), V.pt(Xs[1], b["y0"], b["z1"])], np.clip(wood * 0.7, 0, 1), 1.4, 0.8)       # the near arris, dark
    sh.line([V.pt(Xs[0], b["y0"] + 0.4, b["z0"] + 0.6), V.pt(Xs[1], b["y0"] + 0.4, b["z0"] + 0.6)], RIM, 1.8, 0.85)        # the far arris, lit
    bc, ba = sh.done()
    parts["beam"] = (bc, ba)
    # the noren: a short half-noren under the beam, across the top-left corner; two panels, a slit between them
    nz, ytop, yhem = b["z0"] + 4.0, b["y0"] - 1.0, 229.0
    ind = D.near_tone(rgb("#243a6b"), NEAR_SHADE, k=0.62, warm=0.0)
    ind_lt = D.near_tone(rgb("#3a5490"), NEAR_SHADE, k=0.60, warm=0.0)
    sh = Sheet(SHAPE)
    panels = [(200.0, 248.0), (250.5, 269.0)]
    for i, (xa, xb) in enumerate(panels):
        hem = yhem + (1.5 if i else 0.0)
        pts = [V.pt(xa, ytop, nz), V.pt(xb, ytop, nz)]
        # the hem a little uneven (the cloth hangs, it is not cut by a ruler), the inner corner lifted a touch
        for t in np.linspace(1, 0, 9):
            X_ = xa + (xb - xa) * t
            pts.append(V.pt(X_, hem + 0.6 * math.sin(t * 7 + i) + (1.2 if t > 0.92 else 0.0), nz + 0.8 * math.sin(t * 5)))
        sh.poly(pts, ind)
        for f_ in np.linspace(0.15, 0.85, 4):                                # folds: a lighter and a darker run down it
            X_ = xa + (xb - xa) * f_
            sh.line([V.pt(X_, ytop - 1, nz), V.pt(X_ + 0.5, hem + 1, nz)], ind_lt, 3.0, 0.22)
            sh.line([V.pt(X_ + 2.2, ytop - 1, nz), V.pt(X_ + 2.6, hem + 1, nz)], np.clip(ind * 0.75, 0, 1), 1.6, 0.3)
    sh.line([V.pt(190.0, ytop + 0.5, nz), V.pt(275.0, ytop + 0.5, nz)], D.near_tone(rgb("#8a6238"), NEAR_SHADE, 0.45, 0.06), 2.4, 1.0)   # its rod
    ncl, na = sh.done()
    parts["noren"] = (ncl, na)
    return parts


def finish_near(parts, front_c, front_a):
    """near.png: the beam and the noren with their lit rims; and front.png darker and warmer, lit on its edge."""
    bc, ba = parts["beam"]
    ncl, na = parts["noren"]
    x, y = grid(SHAPE)
    # the noren hangs under the beam: lay the beam, then the noren over it
    a = np.clip(na + ba * (1 - na), 0, 1)
    col = (bc * (ba * (1 - na))[..., None] + ncl * na[..., None]) / np.maximum(a, 1e-4)[..., None]
    rim_n = D.rim(na, light=(0.85, 0.55), width=2.0) * na
    rim_b = D.rim(ba, light=(0.0, 1.0), width=1.6) * ba * (1 - na)
    over(col, rgb("#6d7fb0"), np.clip(rim_n * 0.40, 0, 1))                  # the indigo's lit edge: the cloth's own blue, lighter
    over(col, RIM, np.clip(rim_b * 0.5, 0, 1))
    # front.png (round twenty's corner post and firewood): darker and warmer, lit along the side toward the opening
    fc = front_c.copy()
    shade = rgb(NEAR_SHADE)
    fc = lerp(fc, shade, 0.70)
    fc[..., 0] = np.clip(fc[..., 0] + 0.03, 0, 1)
    fc[..., 2] = np.clip(fc[..., 2] - 0.01, 0, 1)
    post = (x > 560).astype(F32)
    rim_p = D.rim(front_a, light=(-1.0, 0.0), width=2.2) * front_a * post
    rim_w = D.rim(front_a, light=(0.6, -0.8), width=1.6) * front_a * (1 - post)
    over(fc, RIM, np.clip(rim_p * 0.6 + rim_w * 0.45, 0, 1))
    return np.clip(col, 0, 1).astype(F32), a.astype(F32), np.clip(fc, 0, 1).astype(F32)


# ---------------------------------------------------------------- the whole set
def main():
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back")
    cuts = {n: load(n) for n in CUTS}
    deep, view, fm = deepen(back)
    parts = near_plane(deep)
    near_c, near_a, front_c = finish_near(parts, *cuts["front"])
    cuts["front"] = (front_c, cuts["front"][1])
    wet = wet_map(view)
    back_w = WC.wash(deep, seed=SEED, soft=wet, wander=1.4, fleck=0.3)
    files = {"back": (back_w, None)}
    for n in CUTS + ["near"]:
        c, a = (near_c, near_a) if n == "near" else cuts[n]
        hard = (a > 0.5).astype(F32)
        w = WC.wash_cut(c, hard, deep, seed=SEED, soft=wet, wander=1.4, fleck=0.3, crisp=True)
        files[n] = (w, a)
    # back to one palette of 255, as edo_fishshop.py finishes (grain, then the palette with its speckle)
    files = {n: (grain(np.clip(c, 0, 1), SEED + (0 if a is None else 7), 0.012), a) for n, (c, a) in files.items()}
    layered = files["back"][0].copy()
    for n in CUTS + ["near"]:
        c, a = files[n]
        layered = over(layered, c, (a > 0.5).astype(F32))
    pal = palette_of([layered, files["back"][0]], colors=255, seed=3)
    for n, (c, a) in files.items():
        idx = to_palette(c, pal, seed=5, speckle=0.014)
        save(f"{OUT}/{n}.png", idx, pal, alpha=None if a is None else (a > 0.5).astype(F32))
    # the cat's frames and the sidecars: as they were
    for f in sorted(os.listdir(SRC)):
        if f.startswith("cat") or f.endswith(".json"):
            shutil.copyfile(os.path.join(SRC, f), os.path.join(OUT, f))
    Image.fromarray((np.clip(layered, 0, 1) * 255 + 0.5).astype(np.uint8)).save(f"{OUT}-depth-look.png")
    print(f"{OUT}: {len(files)} pictures written; near covers {float((near_a > 0.5).mean()) * 100:.1f}%")


if __name__ == "__main__":
    main()

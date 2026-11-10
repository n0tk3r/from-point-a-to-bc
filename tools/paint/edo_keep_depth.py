"""Round twenty-three, the fast depth pass (DEPTH.md; r23 LITE): edo-keep, inside Himeji's keep, a lower floor, late
afternoon. DEEPEN over the painting as it is: reads out/edo-keep-orig/ (edo_keep.py's full run, kept as it was) and
writes the scene's full set back into out/edo-keep/, every file as before, plus near.png.

    python3 edo_keep_depth.py

NEAR (near.png, plane front): the frame of the floor's own timber nearest the lens, a metre in front of the picture's
bottom edge (Z 770 to 800, room.View's own camera): a massive hewn post at the right edge, of which we see its inner face
(the face toward the room) and a sliver of its front, a wooden bracket under the beam at its head, and the great beam
across the top seen from below (its underside, warm with the light the floor throws up, its front face above in the
deepest shade). Lit only along the edges that face the ports' light: the beam's far lower edge, the post's inner edge,
the bracket's curve. The post stands beyond the right wall's foot (no walked ground at the right edge: the floor ends at
the racks), in front of the tubs and the doorway's right jamb. The old front plane (the plasterers' plank on its two
buckets, the brushes) is made to count: deeper and warmer, its top edge lit.

BACK: the floorboards through the camera (each board its own tone, its joints and butt ends darker, the grain along it,
knots and dents by depth.scatter, the way from the doorway to the stairs and round the pillar worn paler and warmer by
feet, grime along the walls' feet), the pillar's, the stairs' and the racks' shadows along the light (to the left and
toward us, as the beams go), the room's front part in the shade (the near floor deeper), the far wall and the far parts
of the side walls and ceiling a little cooler and paler, the room's corners dark. The gun ports (the bright round,
triangular and square shapes in the back wall) are kept exactly as painted; the beams' light pictures (beam-*.png: the
shafts and their patches on the floor, the puzzle's pieces) are copied byte for byte.

JAPAN: watercolor.wash on the backdrop (a dim room: amount 0.6; nothing wet: no sky, no far land), wash_cut on every
cut-out and the near plane with the same seed over the unwashed backdrop, then one palette for all (160, as edo_keep.py).
"""

import json
import math
import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import F32, lerp, noise, blur, mask_poly, mask_line, Sheet, over, tint, grid, rgb, grain, palette_of, to_palette, save, sample
import depth as D
import watercolor as WC
import edo_keep as K                                   # the camera, the room and the paints (its main() does not run)
from edo_keep_kit import band_id, hash01, SIENNA, OCHRE, PRUSSIAN, NAPLES, PAPER, COBALT, ULTRA

SEED = 1830
ORIG = "out/edo-keep-orig"
OUT = "out/edo-keep"
CUTS = ["racks", "stairs", "pillar", "tubs", "front"]
FRAMES = ["beam-round.png", "beam-tri.png", "beam-square.png"]
W, H = 800, 600
SHAPE = (H, W)
V = K.V
AMOUNT = 0.6                                           # the wash, for a dim room: the darks stay deep


def load(name):
    a = np.asarray(Image.open(f"{ORIG}/{name}.png").convert("RGBA"), F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def gpt(X, Z):
    return V.pt(X, 0.0, Z)


def kpc(X, Z):
    return V.scale_at(X, Z)


# ---------------------------------------------------------------- the ports: kept exactly
def ports_keep():
    """The ports in the back wall and the beams' patches on the floor (layout.json beams[].patch): the light shapes the
    puzzle reads, kept exactly as painted (and the floor under each patch, so that the patch is as bright as it was)."""
    m = np.zeros(SHAPE, F32)
    for kind, X, Y, s in K.PORTS:
        pp = V.poly(K.port_pts(kind, X, Y, s * 1.25))
        m = np.maximum(m, mask_poly(SHAPE, pp))
    lay = json.load(open(os.path.join(ORIG, "layout.json")))
    for b in lay["beams"]:
        m = np.maximum(m, np.clip(blur(mask_poly(SHAPE, [tuple(p) for p in b["patch"]]), 2.5) * 3.0, 0, 1))
    return np.clip(blur(m, 1.0) * 2.0, 0, 1)


# ---------------------------------------------------------------- the back
def floor_maps():
    X, Z, ok = V.floor_xz(SHAPE, 0.0)
    X = np.asarray(X, F32)
    Z = np.asarray(Z, F32)
    x, y = grid(SHAPE)
    inside = (ok > 0.5) & (X >= -2) & (X <= K.RW + 2) & (Z >= -2) & (Z <= K.RD) & (y > V.hz + 2)
    return X, Z, inside.astype(F32)


def worn_mask(X, Z):
    """Where feet go: from the doorway (right wall, Z 380..470) across to the stairs' foot, round the pillar, to the
    racks, to the ports' patches. A soft band in the floor's own centimetres."""
    paths = [
        [(760, 425), (620, 430), (470, 440), (330, 445), (200, 450), (150, 440)],
        [(640, 430), (690, 300), (700, 150)],
        [(330, 445), (320, 330), (300, 260)],
        [(470, 440), (480, 330), (520, 200)],
    ]
    m = np.zeros(X.shape, F32)
    for pth in paths:
        for (x0, z0), (x1, z1) in zip(pth[:-1], pth[1:]):
            dx, dz = x1 - x0, z1 - z0
            L2 = dx * dx + dz * dz
            t = np.clip(((X - x0) * dx + (Z - z0) * dz) / L2, 0, 1)
            dist = np.hypot(X - (x0 + t * dx), Z - (z0 + t * dz))
            m = np.maximum(m, np.exp(-(dist / 70.0) ** 2))
    return m


def deepen_back(back):
    pic = back.copy()
    X, Z, fl = floor_maps()
    x, y = grid(SHAPE)
    keep = ports_keep()
    # the drop flap stays exactly (its area is clicked)
    drop = mask_poly(SHAPE, [(548, 340), (600, 340), (614, 370), (556, 370)])
    fl = fl * (1 - drop)
    d = np.maximum(1000.0 - Z, 1.0)
    kx = V.F / d                                                    # px per cm across, on the floor
    kz = V.eye * V.F / (d * d)                                      # px per cm along Z (foreshortened)

    # ---- the boards (as edo_keep.py laid them: along Z, 30 cm, offset 7, seed 3): each its own tone, grain along it
    ids = band_id(X, 30.0, 7.0)
    tone = (hash01(ids, 41) - 0.5) * 0.16
    warm = (hash01(ids, 43) - 0.5) * 0.05
    per = 180.0 + 140.0 * hash01(ids, 3 + 5)
    off = per * hash01(ids, 3 + 9)
    piece = np.floor((Z - off) / per).astype(np.int64)
    tone = tone + (hash01(ids * 131 + piece, 47) - 0.5) * 0.10       # each length of board its own, too
    f = np.ones(SHAPE + (3,), F32)
    f *= (1 + tone)[..., None]
    f[..., 0] *= 1 + warm
    f[..., 2] *= 1 - warm
    # grain: streaks along the board (long in Z, fine across), fading where they would be under a pixel
    tile = noise((512, 512), 24, 7, 3)
    def fold(t):
        m = np.mod(t, 2 * 510)
        return np.where(m > 510, 2 * 510 - m, m)
    gn = sample(tile, fold(X / 1.6 * 4 + 50), fold(Z / 60.0 * 4 + 50)) - 0.5
    vis = np.clip(kx * 1.6 - 0.5, 0, 1)
    f *= (1 + gn * 0.24 * vis)[..., None]
    # joints: the long joints between boards and the butt ends, darker, a pixel or less, through the camera
    fu = np.mod(X - 7.0, 30.0)
    fu = np.minimum(fu, 30.0 - fu) * kx
    joint = np.clip(1.0 - fu / 0.75, 0, 1)
    fz = np.mod(Z - off, per)
    fz = np.minimum(fz, per - fz) * kz
    butt = np.clip(1.0 - fz / 0.6, 0, 1) * np.clip(kz * 3, 0.3, 1)
    f *= (1 - 0.40 * np.maximum(joint, butt * 0.85))[..., None]
    # worn by feet: paler, warmer, the grain rubbed away; grime along the walls' feet and in the corners
    wear = worn_mask(X, Z) * (0.6 + 0.4 * noise(SHAPE, 30, 51, 3))
    f = lerp(f, np.ones_like(f) * np.array([1.10, 1.06, 0.98], F32), (wear * 0.55)[..., None])
    wall = np.minimum(X, K.RW - X)
    grime = np.exp(-np.clip(wall, 0, None) / 45.0) * 0.26 + np.exp(-np.clip(Z, 0, None) / 30.0) * 0.10
    corner = np.exp(-(np.hypot(X - 0, Z - 0) / 140.0) ** 2) + np.exp(-(np.hypot(X - K.RW, Z - 0) / 140.0) ** 2)
    grime = np.clip(grime + corner * 0.20, 0, 0.45)
    f *= (1 - grime)[..., None]
    pic = pic * (1 - fl[..., None]) + np.clip(pic * f, 0, 1) * fl[..., None]

    # ---- knots, dents and the odd peg through the camera: few and large near us, many and small far off
    sh = Sheet(SHAPE)
    knots = D.scatter(gpt, kpc, (5, K.RW - 5, 5, K.RD), 0.9, SEED, size=(3.0, 3.0), zone=fl)
    dark = lerp(SIENNA, PRUSSIAN, 0.62)
    for (px, py, k, r) in knots:
        Xk, Zk = X[int(py), int(px)], Z[int(py), int(px)]
        dd = max(1000.0 - Zk, 1.0)
        rx = (1.6 + 1.6 * r) * k
        ry = max(0.5, rx * V.eye / dd)
        sh.ellipse(px, py, rx, ry, dark, alpha=0.55)
        if rx > 2.2:
            sh.ellipse(px, py, rx * 0.45, ry * 0.45, lerp(SIENNA, PRUSSIAN, 0.8), alpha=0.6)
    pegs = D.scatter(gpt, kpc, (5, K.RW - 5, 5, K.RD), 0.5, SEED + 1, size=(1.6, 1.6), zone=fl)
    for (px, py, k, r) in pegs:
        rx = 0.9 * k + 0.3
        sh.ellipse(px, py, rx, max(0.45, rx * 0.4), lerp(OCHRE, SIENNA, 0.5) if r < 0.6 else dark, alpha=0.6)
    scuffs = D.scatter(gpt, kpc, (5, K.RW - 5, 5, K.RD), 2.2, SEED + 2, size=(12.0, 1.0), zone=fl)
    for (px, py, k, r) in scuffs:
        L = (5 + 10 * r) * k
        a = (r * 7.3) % 1.0 - 0.5
        sh.line([(px - L / 2, py - a * L * 0.15), (px + L / 2, py + a * L * 0.15)], lerp(NAPLES, OCHRE, 0.5) if r > 0.5 else dark,
                max(0.4, 0.5 * k), alpha=0.22)
    c, a = sh.done()
    pic = over(pic, c, a * fl)

    # ---- shadows along the light (to the left and toward us, as the beams go), glazes on the floor only
    sx, sz = K.SUN[0], K.SUN[2]
    n = math.hypot(sx, sz)
    sx, sz = sx / n, sz / n
    px_, pz_ = -sz, sx                                                  # across the light
    def shade(cx, cz, half, length, spread, amount, seed):
        a0 = (cx + px_ * half, cz + pz_ * half)
        a1 = (cx - px_ * half, cz - pz_ * half)
        b1 = (cx - px_ * (half + spread) + sx * length, cz - pz_ * (half + spread) + sz * length)
        b0 = (cx + px_ * (half + spread) + sx * length, cz + pz_ * (half + spread) + sz * length)
        D.shadow_on_ground(pic, gpt, [a0, a1, b1, b0], color="#3a3050", amount=amount, soft=7.0, wobble=1.5, seed=seed, ground=fl)
    shade(K.PILLAR[0], K.PILLAR[1], K.PILLAR[2], 330.0, 70.0, 0.20, 3)          # the great pillar's
    shade(K.PILLAR[0], K.PILLAR[1], K.PILLAR[2] * 0.8, 150.0, 20.0, 0.16, 4)     # (deeper at its foot)
    s = K.STAIR
    for zz in np.linspace(s["z_top"], s["z_foot"], 6):                            # the stairs': the floor behind the flight's open side
        shade((s["X0"] + s["X1"]) / 2, zz, 55.0, 120.0, 25.0, 0.10, int(zz))
    # the racks': a band along the right wall's foot, thrown to the left
    D.shadow_on_ground(pic, gpt, [(K.RW, 50), (K.RW - 75, 80), (K.RW - 95, 520), (K.RW, 520)], color="#3a3050", amount=0.22, soft=6.0, wobble=1.2, seed=6, ground=fl)
    # the room's front part in the shade, its edge running in from the right (the near floor deeper)
    near = np.clip((Z - 60.0) / 540.0, 0, 1) ** 1.1
    edge = np.clip((Z - (380.0 + (X - 300.0) * 0.25)) / 200.0, 0, 1)
    nshade = np.clip(near * 0.75 + edge * 0.35, 0, 1) * 0.42 * fl
    pic = tint(pic, lerp(np.ones(3, F32), rgb("#4a3a58"), 1.0), nshade)

    # ---- the far: the back wall and the far parts of the walls and ceiling a little cooler and paler (the ports kept)
    dm = np.asarray(V.depth_map(SHAPE, 0.0), F32)
    far = np.zeros(SHAPE, F32)
    bw = mask_poly(SHAPE, [V.pt(0, 0, 0), V.pt(K.RW, 0, 0), V.pt(K.RW, K.RH, 0), V.pt(0, K.RH, 0)])
    far = np.maximum(far, bw)
    # the side walls and the ceiling: by how far each pixel is (across the picture toward the back wall's edges)
    left = mask_poly(SHAPE, [V.pt(0, 0, 0), V.pt(0, K.RH, 0), V.pt(0, K.RH, 700), V.pt(0, 0, 700)])
    right = mask_poly(SHAPE, [V.pt(K.RW, 0, 0), V.pt(K.RW, K.RH, 0), V.pt(K.RW, K.RH, 700), V.pt(K.RW, 0, 700)])
    ceil = mask_poly(SHAPE, [V.pt(0, K.RH, 0), V.pt(K.RW, K.RH, 0), V.pt(K.RW, K.RH, 700), V.pt(0, K.RH, 700)])
    bx0, by0 = V.pt(0, K.RH, 0)
    bx1, by1 = V.pt(K.RW, 0, 0)
    dx_ = np.maximum(np.maximum(bx0 - x, x - bx1), 0)
    dy_ = np.maximum(np.maximum(by0 - y, y - by1), 0)
    near_back = np.clip(1 - np.hypot(dx_, dy_) / 170.0, 0, 1)
    far = np.maximum(far, np.clip(left + right + ceil, 0, 1) * near_back * 0.85)
    floor_far = np.clip((V.hz + 260 - y) / 120.0, 0, 1) * fl
    far = np.maximum(far, floor_far * 0.6)
    D.air(pic, far, lerp(rgb("#c9cdd8"), rgb("#8f98b4"), 0.35), amount=0.16, mask=1 - keep)
    # ---- the corners dark: where the back wall meets the walls, the floor and the ceiling
    cm = np.zeros(SHAPE, F32)
    for (cx, cy) in (V.pt(0, 0, 0), V.pt(K.RW, 0, 0), V.pt(0, K.RH, 0), V.pt(K.RW, K.RH, 0)):
        cm = np.maximum(cm, np.exp(-(((x - cx) / 60.0) ** 2 + ((y - cy) / 48.0) ** 2)))
    pic = tint(pic, rgb("#4a3c5c"), cm * 0.30 * (1 - keep))
    D.frame(pic, amount=0.14, bottom=0.10, color="#3a2a40")
    pic = pic * (1 - keep[..., None]) + back * keep[..., None]
    return np.clip(pic, 0, 1), fl


# ---------------------------------------------------------------- the near plane
POST_Z = (770.0, 800.0)                     # the post and the beam: a metre in front of the picture's bottom edge
BEAM_Y = 341.0                              # the beam's underside (the ceiling, the floor above, at 380)


def near_plane():
    """-> (colour, alpha) of near.png: the beam across the top, the post at the right edge, the bracket at its head."""
    zb, zf = POST_Z
    db, df = 1000.0 - zb, 1000.0 - zf
    xb_target = 742.0
    Xl = 430.0 + (xb_target - 400.0) * db / V.F                       # the post's inner face (toward the room)
    xb = V.pt(Xl, 0, zb)[0]
    xa = V.pt(Xl, 0, zf)[0]
    yb = V.pt(0, BEAM_Y, zb)[1]                                        # the beam's underside: its far edge ...
    yf = V.pt(0, BEAM_Y, zf)[1]                                        # ... and its near edge
    rng = np.random.default_rng(SEED)

    WOOD = K.WOOD
    deep = D.near_tone(lerp(SIENNA, PRUSSIAN, 0.35), shade="#1a100e", k=0.80, warm=0.035)
    face = D.near_tone(lerp(SIENNA, OCHRE, 0.2), shade="#1c110e", k=0.72, warm=0.05)
    under = D.near_tone(lerp(SIENNA, OCHRE, 0.3), shade="#1e120e", k=0.68, warm=0.06)
    rimc = lerp(NAPLES, OCHRE, 0.35)

    # the beam's lower edge: hewn, a little uneven, sagging a hair in the middle
    xs = np.linspace(-10, 810, 83)
    sag = 2.2 * np.sin(np.clip(xs, 0, 800) / 800.0 * math.pi) + 2.6 * np.sin(xs / 95.0 + 1.0) + 1.2 * np.sin(xs / 37.0 + 2.0)   # a crooked pine
    wob = np.convolve(rng.normal(0, 0.9, len(xs) + 6), np.ones(7) / 7, mode="valid")[: len(xs)]
    low = yb + sag + wob
    lowf = yf + sag * 0.7 + wob * 0.5

    sh = Sheet(SHAPE)
    # the beam: its front face above, the underside below it
    sh.poly([(-10, -10), (810, -10)] + [(xx, yy) for xx, yy in zip(xs[::-1], lowf[::-1])], deep)
    sh.poly([(xx, yy) for xx, yy in zip(xs, lowf)] + [(xx, yy) for xx, yy in zip(xs[::-1], low[::-1])], under)
    # the post: its inner face (toward the room) and a sliver of its front
    post_top_b, post_top_f = yb + sag[-9] + wob[-9], yf
    sh.poly([(xb, post_top_b), (xa, post_top_f), (xa, 610), (xb, 610)], face)
    sh.poly([(xa, -10), (810, -10), (810, 610), (xa, 610)], deep)
    # the bracket under the beam at the post's head (sashi-hijiki), its underside a curve
    zc = (zb + zf) / 2 + 4
    pts = []
    for t in np.linspace(0, 1, 16):
        Xt = Xl - 30.0 * (1 - t)
        Yt = BEAM_Y - 9.0 - 13.0 * t ** 1.6 - 2.0 * math.sin(t * math.pi)
        pts.append(V.pt(Xt, Yt, zc))
    top0 = V.pt(Xl - 30.0, BEAM_Y, zc)
    top1 = V.pt(Xl, BEAM_Y, zc)
    tip = [(top0[0] - 1.0, top0[1])]
    bracket = tip + [top1] + [V.pt(Xl, BEAM_Y - 24.0, zc)] + pts[::-1]
    sh.poly(bracket, deep)
    col, a = sh.done()

    # the light within, little of it: the underside's far half warmer (the floor's light thrown up), the post's inner face
    # lighter toward the floor and toward its inner edge; grain and the adze's scallops; a check down the post
    x, y = grid(SHAPE)
    beam_u = np.clip((y - lowf.mean()) / max(low.mean() - lowf.mean(), 1), 0, 1) * (y < low.max() + 1)
    col = lerp(col, np.array(col) * 1.3 + np.array([0.025, 0.012, 0.0], F32), (beam_u * 0.6 * (x < xb + 2))[..., None])
    on_face = ((x >= xb - 0.5) & (x <= xa + 0.5) & (y > post_top_b)).astype(F32)
    lift = np.clip(1 - (xa - x) / max(xa - xb, 1), 0, 1)
    lift = (1 - lift) * 0.5 + np.clip((y - 200) / 400.0, 0, 1) * 0.5
    col = lerp(col, np.clip(col * 1.3 + np.array([0.03, 0.015, 0.0], F32), 0, 1), (on_face * lift * 0.6)[..., None])
    g = noise(SHAPE, (3, 60), SEED + 3, 3)                             # the post's grain, along it (up and down)
    col *= (1 + (g - 0.5) * 0.30 * on_face)[..., None]
    gb = noise(SHAPE, (40, 2), SEED + 4, 3)                            # the beam's grain, along it (across)
    col *= (1 + (gb - 0.5) * 0.30 * (y < low.max() + 1) * (x < xb))[..., None]
    sk = Sheet(SHAPE)
    # adze scallops: short strokes toward the vanishing point on the post's inner face, across the beam's underside
    for i in range(70):
        yy = rng.uniform(post_top_b + 15, 600)
        xx = rng.uniform(xb + 3, xa - 3)
        vx, vy = (400 - xx), (180 - yy)
        n_ = math.hypot(vx, vy)
        L = rng.uniform(4, 9)
        sk.line([(xx, yy), (xx + vx / n_ * L, yy + vy / n_ * L)], lerp(deep, face, 0.3), 0.8, alpha=0.5)
    for i in range(90):
        xx = rng.uniform(-5, xb - 4)
        yy0 = float(np.interp(xx, xs, lowf)) + 2
        yy1 = float(np.interp(xx, xs, low)) - 2
        if yy1 <= yy0:
            continue
        yy = rng.uniform(yy0, yy1)
        vx, vy = (400 - xx), (180 - yy)
        n_ = math.hypot(vx, vy)
        L = rng.uniform(3, 7)
        sk.line([(xx, yy), (xx + vx / n_ * L, yy + vy / n_ * L)], lerp(deep, under, 0.35), 0.8, alpha=0.45)
    # a long check (a seasoning crack) down the post, and one along the beam
    cx0 = xb + (xa - xb) * 0.58
    pts_ = [(cx0 + 1.2 * math.sin(t * 7.0) + t * 2.0, post_top_b + 40 + t * 420) for t in np.linspace(0, 1, 30)]
    sk.line(pts_, lerp(deep, PRUSSIAN, 0.3), 1.1, alpha=0.8)
    pts_ = [(40 + t * 520, float(np.interp(40 + t * 520, xs, (lowf + low) / 2)) + 1.5 * math.sin(t * 9)) for t in np.linspace(0, 1, 40)]
    sk.line(pts_, lerp(deep, PRUSSIAN, 0.3), 0.9, alpha=0.7)
    cc, ca = sk.done()
    col = over(col, cc, ca * a)

    # the rims: the beam's far lower edge, the post's inner edge, the bracket's curve: the edges facing the ports' light
    r1 = D.rim(a, light=(-0.25, 1.0), width=1.6) * (x < xb + 30)
    r2 = D.rim(a, light=(-1.0, 0.2), width=1.6) * (x > xb - 4) * (y > post_top_b + 6)
    br = noise(SHAPE, (26, 26), SEED + 5, 3)                          # the light catches the edge here and there
    br = np.clip((br - 0.38) * 3.0, 0, 1)
    r1 = r1 * br * np.clip(1.15 - np.abs(x - 470.0) / 420.0, 0.25, 1)   # most over the floor's lit middle
    r2 = r2 * np.clip(0.35 + (y - 120.0) / 380.0, 0.35, 1) * (0.55 + 0.45 * br)
    rr = np.clip(r1 * 0.85 + r2 * 0.8, 0, 1)
    col = lerp(col, rimc[None, None, :], (rr * 0.8)[..., None])
    return np.clip(col, 0, 1), a


def deepen_front(rgb_, a):
    """The plasterers' plank on its buckets and the brushes: deeper and warmer, their top edges lit."""
    out = lerp(rgb_, rgb("#22140f"), 0.62)
    out[..., 0] = np.clip(out[..., 0] + 0.035, 0, 1)
    rr = D.rim(a, light=(0.4, -1.0), width=1.6)
    out = lerp(out, lerp(NAPLES, OCHRE, 0.35)[None, None, :], (rr * 0.6)[..., None])
    return np.clip(out, 0, 1)


# ---------------------------------------------------------------- the whole set
def main():
    os.makedirs(OUT, exist_ok=True)
    back0, _ = load("back")
    back, fl = deepen_back(back0)
    keep = ports_keep()
    WET = np.zeros(SHAPE, F32)                                          # a room: no sky, no far land, nothing wet
    washed = WC.wash(back, seed=SEED, amount=AMOUNT, soft=WET, keep=keep, wander=1.4, fleck=0.3)
    pictures = {"back": (washed, None)}
    for n in CUTS:
        c, a = load(n)
        if n == "front":
            c = deepen_front(c, a)
        wc = WC.wash_cut(c, a, back, seed=SEED, amount=AMOUNT, soft=WET, wander=1.4, fleck=0.3, crisp=True)
        pictures[n] = (wc, a)
    nc, na = near_plane()
    wn = WC.wash_cut(nc, na, back, seed=SEED, amount=AMOUNT, soft=WET, wander=1.4, fleck=0.3, crisp=True)
    pictures["near"] = (wn, na)
    # back to palettes, as edo_keep.py's finish does it (one palette for the scene's files: 160, seed 9; a little grain)
    grained = {nm: grain(p, 9 + i, 0.010) for i, (nm, (p, al)) in enumerate(pictures.items())}
    sample_ = [grained[nm] if al is None else grained[nm][al >= 0.5] for nm, (p, al) in pictures.items()]
    sample_ = [s.reshape(-1, 1, 3) for s in sample_ if s.size]
    pal = palette_of(sample_, colors=160, seed=9)
    for nm, (p, al) in pictures.items():
        idx = to_palette(grained[nm], pal, seed=10, speckle=0.012)
        save(os.path.join(OUT, nm + ".png"), idx, pal, alpha=None if al is None else al)
    for fn in FRAMES + ["layout.json"]:
        shutil.copyfile(os.path.join(ORIG, fn), os.path.join(OUT, fn))
    # a picture to look at: everything together, the beams laid on as the game lays them
    comp = np.asarray(Image.open(os.path.join(OUT, "back.png")).convert("RGB"), F32) / 255
    for nm in CUTS + ["near"]:
        im = np.asarray(Image.open(os.path.join(OUT, nm + ".png")).convert("RGBA"), F32) / 255
        comp = comp * (1 - im[..., 3:]) + im[..., :3] * im[..., 3:]
        if nm == "tubs":
            for fn in FRAMES:
                b = np.asarray(Image.open(os.path.join(OUT, fn)).convert("RGBA"), F32) / 255
                comp = comp * (1 - b[..., 3:]) + (1 - (1 - comp) * (1 - b[..., :3])) * b[..., 3:]
    Image.fromarray((np.clip(comp, 0, 1) * 255 + 0.5).astype(np.uint8)).save("out/edo-keep-comp.png")
    print("edo-keep depth:", ", ".join(sorted(pictures)), "+", len(FRAMES), "beams copied")


if __name__ == "__main__":
    main()

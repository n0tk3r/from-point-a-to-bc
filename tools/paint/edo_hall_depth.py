"""PAINT-23 (round twenty-three, wave two: the fast depth pass, tools/paint/DEPTH.md): edo-hall, inside the women's hall
at the foot of Mount Shosha at sunset, deepened over its own painting (edo_hall.py is not changed).

    python3 edo_hall.py             first, once: the painting as it is (seeded), then copied to out/edo-hall-orig/
    python3 edo_hall_depth.py       reads out/edo-hall-orig/, writes the scene's full set to out/edo-hall/ + near.png

Through the hall's own camera (edo_hall.V: room.View, the lens 230 cm up just outside the open south doors):

  NEAR (near.png, the front plane): the doorway we look in through. Its east post at the right edge of the frame (20 cm
      square, about 1.8 m from the lens: X 502-522, Z 468-488) and the head beam over the doors across the top (Z 470-492),
      the two joined at the top right; in the evening's shade, a deep warm brown, a thin warm rim where they face the lit
      hall (the post's west face, the beam's underside); a few old slips pasted on them, dim (slips are on every post and
      beam here). Off the top, right and bottom edges; clear of the walked floor (its east corner is x 694), the hum,
      the bars on the east wall and the lattice. The women's desk (front.png, the scene's own front plane) made to count:
      deeper and warmer, its outline and place exactly as painted.
  BACK: the mats' edges in perspective (each heri's lit lip and shaded fold, the short ends' joints, the straw's weave
      lines a step stronger: big and few near us, fine far off); the doorway's light on the floor given the two shadows
      of the doorway's sides (outside the picture), leading in from the bottom corners; contact shade along the walls' feet,
      before the altar stand, behind the cushions and the desk, all falling away from the doors (north) as the step of
      evening light does; the far wall and the far end a little cooler and paler (air toward a cool pale), the near
      floor and the frame's bottom deeper. The sunset seen through the lattice is not touched.
  JAPAN: watercolor.wash (seed 1830, amount 0.7, wander 1.4, fleck 0.3; wet only in the window's sky), every cut-out
      and near.png with wash_cut over the unwashed backdrop (crisp); the light pictures (bars-*.png) copied exactly.
  FINISH: one palette of 160 for the scene's files (as finish_scene), the cut-outs' alpha exactly as painted.

PAINT-23."""

import math
import os
import shutil
import sys

import numpy as np
from PIL import Image

from brush import F32, lerp, blur, mask_poly, mask_ellipse, Sheet, noise, palette_of, to_palette, save, rgb
import depth
import watercolor
from edo_hall import (V, RW, RH, ZFAR, HEAD, STAND, CUSHIONS, DESK, LATTICE, SIENNA, PRUSSIAN, OCHRE, PAPER, NAPLES,
                      SHADE, WOOD, WOOD_D, DUSKY, EVENING, SLIP_TONES, SUN, CERULEAN, COBALT, PLASTER)

SRC = "out/edo-hall-orig"
OUT = "out/edo-hall"
W, H = 800, 600
SHAPE = (H, W)
SEED = 1830
AMOUNT = 0.7                                   # the lead's wash amount for this scene
CUTS = ["lattice", "front", "lattice-dusk", "front-dusk"]
FRAMES = ["bars-wall", "bars-floor", "bars-air"]

POST = (502.0, 522.0, -60.0, 420.0, 468.0, 488.0)      # the doorway's east post: X0, X1, Y0, Y1, Z0, Z1 (cm)
BEAM = (-900.0, 1500.0, 297.0, 420.0, 470.0, 492.0)    # the head beam over the doors


# ---------------------------------------------------------------------------------------------- reading and writing
def load(name):
    im = Image.open(os.path.join(SRC, name + ".png")).convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255.0
    return a[..., :3].copy(), a[..., 3].copy()


def pt(X, Z):
    return V.pt(X, 0.0, Z)


def px_per_cm(X, Z):
    return V.scale_at(X, Z)


# ---------------------------------------------------------------------------------------------- the hall's shell
def shell():
    """For every pixel: which surface of the hall's shell it shows first (0 floor, 1 ceiling, 2 north, 3 west, 4 east)
    and its depth along the lens axis (cm); and the floor places (X, Z)."""
    dX, dY, dZ = V._rays(SHAPE)
    with np.errstate(divide="ignore", invalid="ignore"):
        ts = [(0.0 - V.eye) / dY, (RH - V.eye) / dY, (0.0 - V.cam_z) / dZ, (0.0 - V.cam_x) / dX, (RW - V.cam_x) / dX]
    ts = [np.where(np.isfinite(t) & (t > 1.0), t, 1e6) for t in ts]
    st = np.stack(ts)
    which = np.argmin(st, axis=0)
    d = np.min(st, axis=0).astype(F32)
    X = (V.cam_x + dX * d).astype(F32)
    Z = (V.cam_z + dZ * d).astype(F32)
    return which, d, X, Z


def box_mask(b):
    m = np.zeros(SHAPE, F32)
    for _, pp, _ in V.box(*b):
        m = np.maximum(m, mask_poly(SHAPE, pp, soft=0.6))
    return m


def window_mask():
    z0, z1, y0, y1 = LATTICE
    return mask_poly(SHAPE, V.poly([(0.4, y0, z0), (0.4, y0, z1), (0.4, y1, z1), (0.4, y1, z0)]), soft=0.8)


# ---------------------------------------------------------------------------------------------- the back, deepened
def glaze(pic, m, color, k=1.5):
    c = rgb(color) if isinstance(color, str) else np.asarray(color, F32)
    pic[...] = pic * (1 - m[..., None]) + pic * np.clip(c * k, 0, 1.2) * m[..., None]
    return np.clip(pic, 0, 1, out=pic)


def mats_edges(pic, floor_ok, dark):
    """The tatami's edges in perspective: each heri's lit lip toward the doors and its shaded fold, the short ends'
    joints (running to the vanishing point), the straw's weave a step stronger (fine far off, open near us)."""
    X0, Z0 = 42.0, 75.0
    lit = Sheet(SHAPE, ss=2)
    shd = Sheet(SHAPE, ss=2)
    weave = Sheet(SHAPE, ss=2)
    for i in range(4):
        for j in range(3):
            x0, z0 = X0 + j * 182, Z0 + i * 91
            k = px_per_cm(x0 + 91, z0 + 45)
            for zz in (z0 + 3.2, z0 + 91.0):                       # the lip of each heri toward the doors (lit)
                ln = V.line((x0 + 0.5, 0.7, zz), (x0 + 181.5, 0.7, zz))
                if ln:
                    lit.line([ln[0], ln[1]], "#ffffff", max(0.45, 0.55 * k))
            for zz in (z0, z0 + 87.8):                             # its far fold (shade)
                ln = V.line((x0 + 0.5, 0.7, zz), (x0 + 181.5, 0.7, zz))
                if ln:
                    shd.line([ln[0], ln[1]], "#ffffff", max(0.5, 0.7 * k))
            for xx in (x0, x0 + 182):                              # the short ends' joints
                ln = V.line((xx, 0.6, z0 + 3.2), (xx, 0.6, z0 + 87.8))
                if ln:
                    shd.line([ln[0], ln[1]], "#ffffff", max(0.5, 0.8 * k))
            step = 3.0
            for zz in np.arange(z0 + 6.5, z0 + 86.0, step):         # the weave: one line a rush's width apart
                ln = V.line((x0 + 2, 0.5, zz), (x0 + 180, 0.5, zz))
                if ln:
                    weave.line([ln[0], ln[1]], "#ffffff", max(0.35, 0.42 * k))
    _, a_lit = lit.done()
    _, a_shd = shd.done()
    _, a_wv = weave.done()
    pic[...] = lerp(pic, lerp(pic, lerp(EVENING, PAPER, 0.3)[None, None, :], 0.55), (a_lit * floor_ok * 0.55)[..., None])
    glaze(pic, a_shd * floor_ok * 0.55, dark, 1.0)
    # the weave darkens a little between rushes; shimmering by the noise so no two mats read alike
    sheen = 0.7 + 0.6 * noise(SHAPE, 46, 31, 3)
    glaze(pic, a_wv * floor_ok * 0.20 * sheen, dark, 1.25)
    return pic


def deepen(pic, geo, dusk=False):
    which, d, X, Z = geo["which"], geo["d"], geo["X"], geo["Z"]
    win, stand, cush = geo["win"], geo["stand"], geo["cush"]
    out = pic.copy()
    floor = ((which == 0) & (X >= 0) & (X <= RW) & (Z >= 0)).astype(F32)
    floor = floor * (1 - stand) * (1 - win)
    on_mats = ((X >= 42) & (X <= 588) & (Z >= 75) & (Z <= 439)).astype(F32) * floor * (1 - cush)
    dark = lerp(lerp(SHADE, SIENNA, 0.35), PRUSSIAN, 0.15)
    warm_dark = lerp(SIENNA, PRUSSIAN, 0.55)

    # 1. the mats' edges in perspective
    mats_edges(out, on_mats, dark)

    # 2. shade on the floor, all of it falling north, away from the open doors (the step of evening light's own way)
    # the two sides of the doorway (outside the picture): their shadows frame the light on the floor and lead in
    sh_col = lerp(SHADE, SIENNA, 0.18)
    depth.shadow_on_ground(out, pt, [(533, 610), (1400, 610), (1400, 250), (488, 250)], color=sh_col, amount=0.34,
                           soft=3.0, wobble=1.0, seed=3, ground=floor)
    depth.shadow_on_ground(out, pt, [(-700, 610), (118, 610), (168, 300), (150, 160), (-700, 160)], color=sh_col,
                           amount=0.30, soft=3.0, wobble=1.0, seed=4, ground=floor)
    # the shade broadening beyond the light's far end (a soft second layer)
    depth.shadow_on_ground(out, pt, [(470, 330), (900, 330), (900, 60), (440, 60)], color=sh_col, amount=0.16,
                           soft=14.0, wobble=2.0, seed=5, ground=floor)
    # contact shade along the feet of the three walls
    foot = np.exp(-np.minimum(np.minimum(np.abs(X), np.abs(RW - X)), np.abs(Z)) / 22.0) * floor
    glaze(out, foot * 0.42, dark)
    # before the altar stand, behind the cushions and the desk (each throws its shade north)
    X0, X1, _, _, Z0, Z1 = STAND
    depth.shadow_on_ground(out, pt, [(X0 - 6, Z1), (X1 + 6, Z1), (X1 + 12, Z1 + 16), (X0 - 10, Z1 + 16)], color=dark,
                           amount=0.30, soft=2.5, wobble=0.6, seed=6, ground=floor)
    for n, (cx, cz) in enumerate(CUSHIONS):
        ring = [(cx + 3 + 25 * math.cos(a), cz - 7 + 23 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 28, endpoint=False)]
        depth.shadow_on_ground(out, pt, ring, color=dark, amount=0.36, soft=1.6, wobble=0.4, seed=7 + n,
                               ground=floor * (1 - cush))
    dx0, dx1, _, _, dz0, dz1 = DESK
    depth.shadow_on_ground(out, pt, [(dx0 - 4, dz1 - 6), (dx1 + 4, dz1 - 6), (dx1 + 14, dz0 - 26), (dx0 + 4, dz0 - 30)],
                           color=dark, amount=0.30, soft=4.0, wobble=1.0, seed=9, ground=floor)

    # 3. the near floor deeper, the frame's bottom and corners a little deeper (warm)
    near = np.clip((470.0 - d) / (470.0 - 250.0), 0, 1) ** 1.3 * floor
    glaze(out, near * 0.26, warm_dark, 1.6)
    depth.frame(out, amount=0.12, bottom=0.14, color="#3a2630")

    # 4. the far wall and the far end a little cooler and paler (air toward a cool pale); never the sunset in the window
    far = np.clip((d - 420.0) / (640.0 - 420.0), 0, 1) ** 1.1
    far = far * (1 - geo["beam"]) * (1 - win)
    far = np.where(which == 2, np.maximum(far, 0.85), far) * (1 - geo["beam"]) * (1 - win)
    cool = lerp(lerp(PLASTER, CERULEAN, 0.22), COBALT, 0.10)
    if dusk:
        cool = lerp(cool, SHADE, 0.35)
    depth.air(out, blur(far.astype(F32), 1.2), cool, amount=0.15)
    return np.clip(out, 0, 1)


# ---------------------------------------------------------------------------------------------- the front plane
def near_plane():
    """near.png: the doorway's east post at the right edge and the head beam over the doors across the top."""
    base = lerp(SIENNA, PRUSSIAN, 0.45) * np.array([1.0, 1.0, 0.85], F32)
    c_face = depth.near_tone(base * 0.56, shade="#1c1210", k=0.10, warm=0.02)  # the faces toward us: the evening's shade
    c_side = depth.near_tone(base * 0.70, shade="#1c1210", k=0.08, warm=0.03)  # the post's west face, toward the hall
    c_under = depth.near_tone(lerp(base, SIENNA, 0.12) * 0.74, shade="#1c1210", k=0.06, warm=0.03)  # the beam's underside
    sh = Sheet(SHAPE, ss=3)
    faces = {}
    for nm, pp, _ in V.box(*BEAM):
        if nm in ("front", "bottom"):
            faces["beam-" + nm] = pp
    for nm, pp, _ in V.box(*POST):
        if nm in ("front", "left"):
            faces["post-" + nm] = pp
    col = {"beam-front": c_face, "beam-bottom": c_under, "post-front": c_face, "post-left": c_side}
    order = ["beam-front", "beam-bottom", "post-front", "post-left"]
    rgb_ = np.zeros(SHAPE + (3,), F32)
    alpha = np.zeros(SHAPE, F32)
    for nm in order:
        if nm not in faces:
            continue
        m = mask_poly(SHAPE, faces[nm], soft=0.5)
        c = np.asarray(col[nm], F32)
        rgb_ = rgb_ * (1 - m[..., None]) + c * m[..., None]
        alpha = np.maximum(alpha, m)
    # the post's foot of the bracket: a short tie block where the post meets the beam
    tie = box_mask((497.0, 527.0, 281.0, 297.5, 465.0, 495.0))
    rgb_ = rgb_ * (1 - tie[..., None]) + c_face * tie[..., None]
    alpha = np.maximum(alpha, tie)
    # grade every flat (darker toward the frame's edges: the wash is never even)
    x = np.arange(W, dtype=F32)[None, :]
    y = np.arange(H, dtype=F32)[:, None]
    grade = 1.0 - 0.10 * np.clip((x - 740) / 60.0, 0, 1) - 0.08 * np.clip((60 - y) / 60.0, 0, 1)
    rgb_ = rgb_ * grade[..., None]
    # the grain of the wood: long faint streaks along the post and the beam
    gr = Sheet(SHAPE, ss=2)
    rs = np.random.RandomState(23)
    for _ in range(26):
        xx = rs.uniform(POST[0] + 1, POST[1] - 1)
        zz = rs.uniform(POST[4] + 1, POST[5] - 1)
        y0 = rs.uniform(-60, 200)
        a_ = V.pt(xx if rs.rand() < 0.5 else POST[0], y0, zz if rs.rand() < 0.5 else POST[5])
        b_ = V.pt(xx if rs.rand() < 0.5 else POST[0], y0 + rs.uniform(80, 260), zz if rs.rand() < 0.5 else POST[5])
        gr.line([a_, b_], "#ffffff", rs.uniform(0.5, 1.1))
    for _ in range(18):
        x0 = rs.uniform(-200, 700)
        yy = rs.uniform(BEAM[2] + 3, BEAM[3])
        a_, b_ = V.pt(x0, yy, BEAM[5]), V.pt(x0 + rs.uniform(150, 420), yy, BEAM[5])
        gr.line([a_, b_], "#ffffff", rs.uniform(0.5, 1.0))
    _, a_gr = gr.done()
    dark = depth.near_tone(base, k=0.70, warm=0.04)
    rgb_ = lerp(rgb_, dark[None, None, :], (a_gr * alpha * 0.35)[..., None])
    # a few old slips, pasted on the post's west face and the beam's face toward us: in the shade, dim
    sl = Sheet(SHAPE, ss=3)
    spots_post = [(-0.20, 150.0, 6.0, 22.0), (0.55, 118.0, 5.5, 19.0), (0.30, 182.0, 6.5, 24.0), (0.62, 62.0, 6.0, 20.0)]
    for n, (u, v, w, h) in enumerate(spots_post):
        z = POST[4] + 3 + (POST[5] - POST[4] - 6) * min(max(u, 0.0), 1.0)
        X = POST[0] - 0.4
        q = [V.pt(X, v, z - w / 2), V.pt(X, v, z + w / 2), V.pt(X, v + h, z + w / 2), V.pt(X, v + h, z - w / 2)]
        tone = lerp(SLIP_TONES[(n * 2 + 1) % len(SLIP_TONES)], c_side, 0.74)
        sl.poly(q, tone)
    s_rgb, s_a = sl.done()
    s_a = s_a * alpha
    rgb_ = lerp(rgb_, s_rgb, s_a[..., None])
    # the rim: the edge toward the lit hall (the post's west edge, the beam's lower edge), warm, thin
    r = depth.rim(alpha, light=(-1.0, 0.55), width=2.2)
    rim_c = lerp(lerp(EVENING, SUN, 0.35), SIENNA, 0.15)
    rgb_ = lerp(rgb_, rim_c[None, None, :], (np.clip(r, 0, 1) * 0.55)[..., None])
    # the key line: thin, broken, none along the lit edge
    edge = np.clip(blur(alpha, 0.7) * (1 - blur(alpha, 0.7)) * 4.0, 0, 1) * (1 - np.clip(r * 2, 0, 1))
    broken = (noise(SHAPE, 9, 77, 2) > 0.42).astype(F32)
    rgb_ = lerp(rgb_, lerp(PRUSSIAN, SIENNA, 0.2)[None, None, :], (edge * broken * 0.45)[..., None])
    return np.clip(rgb_, 0, 1), np.clip(alpha, 0, 1)


def front_count(c, a):
    """The desk (the scene's own front plane) made to count: deeper and warmer, a little rim on the lit side."""
    warm = lerp(SIENNA, PRUSSIAN, 0.35)
    out = c * (1 - 0.40) + c * np.clip(warm * 1.55, 0, 1.2) * 0.40
    out[..., 0] = np.clip(out[..., 0] + 0.025, 0, 1)
    r = depth.rim(a, light=(-1.0, -0.6), width=1.6)
    out = lerp(out, lerp(EVENING, SUN, 0.3)[None, None, :], (np.clip(r, 0, 1) * 0.35)[..., None])
    return np.clip(out, 0, 1)


# ---------------------------------------------------------------------------------------------- all of it
def main():
    look = "look" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back")
    dusk, _ = load("dusk")
    cuts = {n: load(n) for n in CUTS}
    which, d, X, Z = shell()
    beam_far = box_mask((0.0, RW, HEAD[0] - 26, HEAD[1], 270.0, 292.0))
    stand = box_mask(STAND)
    cush = np.zeros(SHAPE, F32)
    for (cx, cz) in CUSHIONS:
        cush = np.maximum(cush, mask_poly(SHAPE, V.poly([(cx + 23 * math.cos(t), 0.8, cz + 23 * math.sin(t))
                                                         for t in np.linspace(0, 2 * math.pi, 28, endpoint=False)]), soft=0.8))
    win = window_mask()
    geo = {"which": which, "d": d, "X": X, "Z": Z, "win": win, "stand": stand, "cush": cush, "beam": beam_far}
    back_d = deepen(back, geo)
    dusk_d = deepen(dusk, geo, dusk=True)
    near_c, near_a = near_plane()
    front_c = {n: front_count(*cuts[n]) for n in ("front", "front-dusk")}

    # Japan: the wash; wet only in the window's sky (the far land in its gaps a little less)
    wet = win * 0.9
    wash = dict(seed=SEED, amount=AMOUNT, soft=wet, wander=1.4, fleck=0.3)
    pics = {"back": (watercolor.wash(back_d, **wash), None), "dusk": (watercolor.wash(dusk_d, **wash), None)}
    for n in CUTS:
        c, a = cuts[n]
        c = front_c.get(n, c)
        under = dusk_d if n.endswith("-dusk") else back_d
        pics[n] = (watercolor.wash_cut(c, a, under, crisp=True, **wash), a)
    pics["near"] = (watercolor.wash_cut(near_c, near_a, back_d, crisp=True, **wash), (near_a >= 0.5).astype(F32))

    # back to the palette, as finish_scene: one palette for the scene's files
    sample = [p if a is None else p[a >= 0.5] for p, a in pics.values()]
    sample = [s.reshape(-1, 1, 3) for s in sample if s.size]
    pal = palette_of(sample, colors=160, seed=9)
    for i, (n, (p, a)) in enumerate(pics.items()):
        idx = to_palette(p, pal, seed=10 + i, speckle=0.008)
        save(os.path.join(OUT, n + ".png"), idx, pal, alpha=None if a is None else a)
    for n in FRAMES:
        shutil.copy2(os.path.join(SRC, n + ".png"), os.path.join(OUT, n + ".png"))
    shutil.copy2(os.path.join(SRC, "layout.json"), os.path.join(OUT, "layout.json"))
    if look:
        comp = Image.open(os.path.join(OUT, "back.png")).convert("RGBA")
        for n in ("lattice", "front", "near"):
            comp = Image.alpha_composite(comp, Image.open(os.path.join(OUT, n + ".png")).convert("RGBA"))
        comp.convert("RGB").save("out/edo-hall-depth-look.png")
        compd = Image.open(os.path.join(OUT, "dusk.png")).convert("RGBA")
        for n in ("lattice-dusk", "front-dusk", "near"):
            compd = Image.alpha_composite(compd, Image.open(os.path.join(OUT, n + ".png")).convert("RGBA"))
        compd.convert("RGB").save("out/edo-hall-depth-look-dusk.png")
    print("edo-hall depth: wrote", len(pics), "pictures +", len(FRAMES), "light pictures to", OUT,
          "; near share", round(float((near_a >= 0.5).mean()) * 100, 1), "%")


if __name__ == "__main__":
    main()

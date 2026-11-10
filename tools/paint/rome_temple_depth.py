"""Rome, inside the temple of Saturn (round twenty-three, DEPTH.md): the depth pass over the painting as it is.

Reads out/rome-temple-orig/ (the full run of rome_temple.py, untouched) and writes out/rome-temple/ again, plus near.png.

  near.png    the door's lintel overhead: we look in through the doorway, so its head runs across the top of the frame,
              a dark warm timber in shade with bronze studs, its underside lit from below by the sun on the floor.
  front.png   the two door leaves and the near brazier, as they were, made a clear warm dark (a lit rim on the right
              leaf's inner edge, where the sun comes in past it; a fainter bounce on the left leaf's). Shapes unchanged.
  back.png    the shaft of morning sun from the door to its patch (lit dust, measured through the scene's camera: only the
              air the sun really crosses), the far walls and the god's end cooler and paler, the near floor deeper, the
              corners dark. The sun patch itself (and the blade of sun beside it) keeps every pixel exactly as it was.
  table.png   as it was.
"""

import os
import shutil

import numpy as np
from PIL import Image

from brush import F32, Sheet, blur, grid, lerp, mask_poly, noise, palette_of, rgb, save, to_palette
from persp import Camera
import depth

W, H = 800, 600
SHAPE = (H, W)
SRC, OUT = "out/rome-temple-orig", "out/rome-temple"
cam = Camera(120, 585)
GAMMA = 0.6                                                 # the scene's own finish chooses its palette with the darks stretched

# the sun, as rome_temple.py lays it (sun_edges, SUN_Z, the blade at the hinge)
SUN_Z, SUN_SLANT, SUN_X0, SUN_W, Z_NEAR = 437.0, 0.11, -103.0, 186.0, -70.0
BAND_W, SLIT_W = 52.0, 13.0
TAN_E = 1.1                                                 # the sun's height: it clears a lintel about 5.9 m up, 1 m before the picture


def sun_left(z):
    return SUN_X0 + SUN_SLANT * (z + 27.0)


def load(name):
    im = Image.open(os.path.join(SRC, name)).convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def finish(pic, path, colors, alpha=None, keep=None, seed=7):
    """To 8 bits as the scene's finish does it: the palette chosen in pic**0.6, saved back. `keep`: a mask of pixels
    that keep their exact colour (their colours go into the palette as they are)."""
    q = np.clip(pic, 0, 1) ** GAMMA
    inside = q if alpha is None else q[alpha > 0.5]
    fixed = np.zeros((0, 3), F32)
    if keep is not None:
        kk = keep > 0.5 if alpha is None else (keep > 0.5) & (alpha > 0.5)
        u8 = np.round(np.clip(pic[kk], 0, 1) * 255).astype(np.uint8)
        fixed = (np.unique(u8, axis=0).astype(F32) / 255) ** GAMMA
    rest = colors - len(fixed)
    pal = palette_of([inside.reshape(-1, 1, 3)], colors=max(8, rest), seed=3)
    pal = np.concatenate([fixed, pal]).astype(F32) if len(fixed) else pal
    idx = to_palette(q, pal, speckle=0.010)
    if keep is not None and len(fixed):
        u8all = np.round(np.clip(pic, 0, 1) * 255).astype(np.uint8)
        fx8 = np.round(np.clip(fixed ** (1 / GAMMA), 0, 1) * 255).astype(np.uint8)
        lut = {tuple(c): i for i, c in enumerate(fx8)}
        ys, xs = np.nonzero(kk)
        for y, x in zip(ys, xs):
            i = lut.get(tuple(u8all[y, x]))
            if i is not None:
                idx[y, x] = i
    pal_out = np.clip(pal, 0, 1) ** (1 / GAMMA)
    if keep is not None and len(fixed):
        pal_out[:len(fixed)] = fx8.astype(F32) / 255
    save(path, idx, pal_out, alpha)
    return os.path.getsize(path)


# ------------------------------------------------------------------ where things are, through the camera
def room_depth():
    """For every pixel, how far (z, cm) the room's shell is: floor, ceiling (7 m), side walls (x = +-400), back wall."""
    px, py = grid(SHAPE)
    F, Z0, eye, vx, vy = cam.F, cam.Z0, cam.eye, cam.vx, cam.vy
    big = 1e9
    dy, dx = py - vy, px - vx
    floor = np.where(dy > 0.5, eye * F / np.maximum(dy, 0.5), big)
    ceil = np.where(dy < -0.5, (700.0 - eye) * F / np.maximum(-dy, 0.5), big)
    left = np.where(dx < -0.5, 400.0 * F / np.maximum(-dx, 0.5), big)
    right = np.where(dx > 0.5, 400.0 * F / np.maximum(dx, 0.5), big)
    back = np.full(SHAPE, Z0 + 1260.0)
    zc = np.minimum.reduce([floor, ceil, left, right, back])
    return (zc - Z0).astype(F32), (zc == floor)


def sun_masks():
    """The patch of sun and the blade beside it, on the picture, as rome_temple.py lays them."""
    l0, l1 = sun_left(Z_NEAR), sun_left(SUN_Z)
    P = lambda x, z: cam.pt(x, 0, z)
    patch = mask_poly(SHAPE, [P(l0, Z_NEAR), P(l1, SUN_Z), P(l1 + SUN_W, SUN_Z), P(l0 + SUN_W, Z_NEAR)])
    slit = mask_poly(SHAPE, [P(l0 - BAND_W - SLIT_W, Z_NEAR), P(l1 - BAND_W - SLIT_W, SUN_Z - 3), P(l1 - BAND_W, SUN_Z - 3), P(l0 - BAND_W, Z_NEAR)])
    return patch, slit


def shaft(zmap):
    """How much sunlit air each pixel looks through: march along each pixel's ray, and count the places whose way back
    to the sun lands on the lit floor (the patch, or the blade). -> centimetres of sunlit air."""
    px, py = grid(SHAPE)
    F, Z0, eye, vx, vy = cam.F, cam.Z0, cam.eye, cam.vx, cam.vy
    zc_end = zmap + Z0
    length = np.zeros(SHAPE, F32)
    steps = np.linspace(Z0 - 100.0, Z0 + SUN_Z + 40.0, 72)      # from the door's plane (the lintel's shadow) to the patch
    dz = float(steps[1] - steps[0])
    for zc in steps:
        x = (px - vx) * zc / F
        h = eye - (py - vy) * zc / F
        z = zc - Z0
        zf = z + h / TAN_E                                    # where its way to the sun leaves the floor
        xf = x + SUN_SLANT * h / TAN_E
        l = sun_left(zf)
        on = (h > 0) & (zf >= Z_NEAR) & (zf <= SUN_Z) & (((xf >= l) & (xf <= l + SUN_W)) | ((xf >= l - BAND_W - SLIT_W) & (xf <= l - BAND_W)))
        on &= zc < zc_end
        length += on.astype(F32) * dz * (zc / F)               # (a step in depth is longer along the ray; near enough)
    return length


def main():
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back.png")
    orig = back.copy()
    lum = back @ np.array([0.3, 0.59, 0.11], F32)
    zmap, is_floor = room_depth()
    patch, slit = sun_masks()
    # what keeps every pixel: the patch and the blade, and the brightest of the floor round them, a little wider
    bright = ((lum > 0.62) & (np.arange(H)[:, None] > 420)).astype(F32)
    keep = np.clip(blur(np.maximum.reduce([patch, slit, bright]), 1.2) * 3.0, 0, 1)
    keep = (keep > 0.2).astype(F32)
    px, py = grid(SHAPE)

    # ---- the far end cooler and paler: the doorway's daylight dying up the room, in the air of a dark hall
    far = np.clip((zmap - 300.0) / 960.0, 0, 1)
    far = np.clip(blur(far, 2.0), 0, 1)
    depth.air(back, far, "#6f7f92", amount=0.13, power=1.4)
    # (and its darkest darks lifted toward that air a touch, so the god's end goes away)
    cool = np.clip(far ** 1.5 * 0.06, 0, 1)
    back[...] = back + (rgb("#3e4a5c") - back) * cool[..., None] * (back.mean(axis=2, keepdims=True) < 0.18)

    # ---- the near floor deeper (not the sun): the door's light falls off the stone toward us and the walls
    near_floor = is_floor & (py > 330)
    nf = np.clip((py - 360.0) / 240.0, 0, 1) ** 1.2 * near_floor
    side = np.clip((np.abs(px - 392.0) - 70.0) / 260.0, 0, 1)
    deep = blur((nf * (0.10 + 0.18 * side)).astype(F32), 6.0)
    back[...] = back * (1 - deep[..., None]) + back * rgb("#3a2a3a") * deep[..., None] * 1.4

    # ---- the corners dark: the ceiling's corners and the bottom corners
    depth.frame(back, amount=0.30, bottom=0.0, color="#2a1c26")
    top = np.clip((150.0 - py) / 150.0, 0, 1) ** 1.6 * np.clip((np.abs(px - 400.0) - 120.0) / 280.0, 0, 1) * 0.32
    back[...] = back * (1 - top[..., None]) + back * rgb("#1e1620")[None, None] * 1.5 * top[..., None]

    # ---- the shaft: lit dust in the air the sun crosses, from the lintel down to its patch
    L = shaft(zmap)
    dust = 0.75 + 0.5 * noise(SHAPE, 34, seed=1831, octaves=3)
    streak = 0.85 + 0.3 * blur(noise(SHAPE, 6, seed=1832, octaves=2), 1.0)
    haze = (1 - np.exp(-L / 1900.0)) * dust * streak
    haze = blur(haze.astype(F32), 2.2)
    haze *= np.clip((py - 30.0) / 60.0, 0, 1)                       # it starts under the lintel
    haze *= 0.40 + 0.60 * np.clip((py - 330.0) / 100.0, 0, 1)        # thinner where it lies over the god's end (his altar keeps its red)
    sun = rgb("#ffe2b0")
    back[...] = back + (sun - back) * np.clip(haze * 0.42, 0, 0.14)[..., None]
    motes = Sheet(SHAPE)
    rng = np.random.default_rng(1833)
    for _ in range(260):
        x, y = rng.uniform(250, 560), rng.uniform(60, 440)
        if haze[int(y), int(x)] > 0.06:
            r = rng.uniform(0.35, 0.8)
            motes.ellipse(x, y, r, r, "#fff2d8", alpha=float(min(0.9, haze[int(y), int(x)] * 2.2)))
    mc, ma = motes.done()
    back[...] = back * (1 - ma[..., None] * 0.6) + mc * ma[..., None] * 0.6

    # ---- the sun patch, exactly as it was
    back[...] = np.where(keep[..., None] > 0.5, orig, np.clip(back, 0, 1))
    print("back", finish(back, OUT + "/back.png", 152, keep=keep))

    # ---- the front plane as it was, made a clear warm dark with a lit rim
    fc, fa = load("front.png")
    leafL = (fa > 0.5) & (px < 66)
    leafR = (fa > 0.5) & (px >= 400)
    braz = (fa > 0.5) & (px >= 66) & (px < 400)
    lumf = fc @ np.array([0.3, 0.59, 0.11], F32)
    coals = braz & (fc[..., 0] > 0.55) & (fc[..., 0] > fc[..., 2] * 1.8) & (lumf > 0.38)
    shade = rgb("#170d0c")
    k = np.where(leafL | leafR, 0.58, np.where(coals, 0.0, 0.34)).astype(F32)
    out = fc * (1 - k[..., None]) + shade * k[..., None]
    out[..., 0] = np.clip(out[..., 0] + 0.025 * (k > 0.4), 0, 1)
    out[..., 2] = out[..., 2] * (1 - 0.12 * (k > 0.4))
    frame_in = ((px > 3) & (px < W - 4) & (py > 3) & (py < H - 4)).astype(F32)
    rimR = depth.rim(leafR.astype(F32), light=(-1.0, 0.2), width=2.2) * frame_in
    rimL = depth.rim(leafL.astype(F32), light=(1.0, 0.3), width=1.8) * frame_in
    down = np.clip((py - 120.0) / 380.0, 0, 1)                       # the sun's line runs hottest low down, where it meets the floor
    rimR = rimR * (0.45 + 0.55 * down)
    rimL = rimL * (0.25 + 0.45 * down)
    for r, c in ((rimR, "#ffb46a"), (rimL, "#d98a52")):
        out = out + (rgb(c) - out) * np.clip(r * 0.85, 0, 1)[..., None]
    print("front", finish(out, OUT + "/front.png", 80, alpha=fa))

    # ---- near.png: the door's lintel across the top, the underside lit from below
    s = Sheet(SHAPE)
    xs = np.linspace(-4, W + 4, 41)
    sag = lambda x: 1.2 * np.sin(np.pi * x / W) + 0.6 * np.sin(x / 37.0)
    face_b = [(x, 32.0 + sag(x)) for x in xs]
    soff_b = [(x, 42.5 + sag(x) + 0.5 * np.sin(x / 13.0 + 1.0)) for x in xs]
    timber = rgb("#4a2c1c")
    s.poly([(-4, -4), (W + 4, -4)] + soff_b[::-1], tuple(depth.near_tone(timber, shade="#140b0b", k=0.62, warm=0.03)))
    nc, na = s.done()
    # the underside: warm light thrown up from the sun on the floor, strongest over the patch
    under = mask_poly(SHAPE, face_b + soff_b[::-1])
    glowx = np.exp(-((px - 395.0) / 210.0) ** 2)
    soffit = lerp(rgb("#2a1812"), rgb("#7a4a2a"), glowx[..., None])
    nc = nc * (1 - under[..., None]) + soffit * under[..., None]
    # a fillet under the face and a rim on the underside's lower edge
    fil = Sheet(SHAPE)
    fil.line(face_b, "#120a0a", 1.6)
    fil.line([(x, y - 0.6) for x, y in soff_b], "#c98a4e", 1.1, alpha=0.9)
    fil.line([(x, 9.0 + sag(x) * 0.5) for x in xs], "#26160f", 1.4)
    fil.line([(x, 25.5 + sag(x) * 0.9) for x in xs], "#5a3620", 1.0, alpha=0.7)
    for x in np.arange(30, W, 52):
        y = 17.0 + sag(x) * 0.7
        fil.ellipse(x, y, 3.2, 3.0, "#2a1a10")
        fil.ellipse(x - 0.6, y - 0.7, 2.2, 2.0, "#8a6232")
        fil.ellipse(x - 1.0, y - 1.1, 0.9, 0.8, "#c89a52", alpha=0.8)
    fc2, fa2 = fil.done()
    nc = nc * (1 - fa2[..., None]) + fc2 * fa2[..., None]
    rimN = (fil.done()[1] * 0).astype(F32)
    grainy = 1 + (noise(SHAPE, 9, seed=1834, octaves=3) - 0.5) * 0.18
    nc = np.clip(nc * grainy[..., None], 0, 1)
    nalpha = (na > 0.5).astype(F32)
    nc = nc * nalpha[..., None] + rimN[..., None]
    print("near", finish(nc, OUT + "/near.png", 64, alpha=nalpha))

    shutil.copy(os.path.join(SRC, "table.png"), OUT + "/table.png")
    shutil.copy(os.path.join(SRC, "layout.json"), OUT + "/layout.json")
    comp = Image.open(OUT + "/back.png").convert("RGBA")
    for name in ("table", "front", "near"):
        comp.alpha_composite(Image.open(OUT + "/" + name + ".png").convert("RGBA"))
    comp.convert("RGB").save(OUT + "-comp.png")
    # the proof: the sun patch kept every pixel
    nb = np.asarray(Image.open(OUT + "/back.png").convert("RGB"), dtype=F32) / 255
    pk = patch > 0.5
    print("patch kept exactly:", bool(np.all(np.abs(nb[pk] - orig[pk]) < 1.5 / 255)), "max change", float(np.abs(nb[pk] - orig[pk]).max()))


if __name__ == "__main__":
    main()

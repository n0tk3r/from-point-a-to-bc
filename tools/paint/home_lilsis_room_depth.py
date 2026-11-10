"""Little Sister's room, the fast depth pass (round twenty-three): worked over the finished painting, not repainted.

    python3 home_lilsis_room_depth.py          reads out/home-lilsis-room-orig/, writes out/home-lilsis-room/

- near.png (new, front plane): the nearest rafters of both roof slopes and the boards between them, in the top
  corners, cut along the lower edge of a painted rafter (rafter 18 on the left slope, 16 on the right, through the
  room's own View), so the cut follows a beam that is already there. Deep warm umber, lit along the underside that
  faces the rooster lamp.
- front.png (the toy box, the crate of books, the hen house, the nest, the door): the same outline exactly, made the
  room's near dark mass: deeper and warmer, with a rim of lamplight on the side of each thing that faces the lamp.
- back.png: the lamp's pool of light on the floorboards round the bedside table (laid on the floor through the View);
  the far end (the gable wall and the far boards) a little cooler and paler; the near floor deeper and warmer.
- fort, flashlight, teaparty, mobile, layout.json: byte for byte as they were.
"""
import os
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brush import F32, blur, lerp, palette_of, rgb, save, to_palette   # noqa: E402
from room import View                                                     # noqa: E402
import home_lilsis_room_model as M                                        # noqa: E402

SRC, OUT = "out/home-lilsis-room-orig", "out/home-lilsis-room"
v = View(**M.VIEW)
H, W = 600, 800
WD, KNEE, RIDGE = 720.0, 130.0, 420.0
RUN = (RIDGE - KNEE) / (WD / 2)
NL = np.array([RIDGE - KNEE, -WD / 2]) / np.hypot(KNEE - RIDGE, WD / 2)   # the painter's NL: the left slope's underside normal (x, y)
LAMP_XYZ = (583.0, 80.0, 220.0)                                           # the rooster lamp's bulb, on its table
LAMP_PX = np.array(v.pt(*LAMP_XYZ), dtype=F32)
UMBER = rgb("#2b1a12")                                                    # the room's warm deep shade, near the lens
LAMPLIGHT = np.array([1.0, 0.74, 0.42], dtype=F32)


def load(name):
    im = Image.open(f"{SRC}/{name}").convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255.0
    return a[..., :3].copy(), (a[..., 3] > 0.5).astype(F32)


def soft(mask, sigma):
    """Blur without the frame wrapping round (brush.blur works in the frequency domain)."""
    p = int(sigma * 4) + 2
    big = np.pad(mask, p, mode="edge")
    return blur(big, sigma)[p:-p, p:-p]


def poly_mask(pts):
    im = Image.new("L", (W, H), 0)
    ImageDraw.Draw(im).polygon([tuple(map(float, q)) for q in pts], fill=255)
    return np.asarray(im, dtype=F32) / 255.0


def lamp_rim(alpha, width=2.2, reach=1.0):
    """The strip just inside an outline on the side that faces the lamp (per pixel: the lamp is in the room)."""
    a = soft(alpha, width * 0.6)
    gy, gx = np.gradient(a)
    y, x = np.mgrid[0:H, 0:W].astype(F32)
    lx, ly = LAMP_PX[0] - x, LAMP_PX[1] - y
    n = np.maximum(np.hypot(lx, ly), 1e-3)
    facing = np.clip(-(gx * lx + gy * ly) / n * 10.0 * reach, 0, 1)
    return (facing * alpha).astype(F32)


def toward_lamp(alpha_shape_y, alpha_shape_x, fall=520.0):
    """1 at the lamp, falling to 0 `fall` px away: how much lamplight reaches a near thing's face."""
    d = np.hypot(alpha_shape_x - LAMP_PX[0], alpha_shape_y - LAMP_PX[1])
    return np.clip(1 - d / fall, 0, 1).astype(F32)


def rafter_line(z, side):
    """The lower edge of the rafter whose face is at depth z, in the picture: two points far enough out to cut with."""
    if side < 0:
        K, Rg = np.array([0.0, KNEE]), np.array([WD / 2 - 6, RIDGE - 6 * RUN])
        n = NL
    else:
        K, Rg = np.array([WD, KNEE]), np.array([WD / 2 + 6, RIDGE - 6 * RUN])
        n = np.array([-NL[0], NL[1]])
    k2, r2 = K + n * 13, Rg + n * 13
    return np.array(v.pt(k2[0], k2[1], z), dtype=F32), np.array(v.pt(r2[0], r2[1], z), dtype=F32)


def near_rafters(back):
    """near.png: the nearest rafters and boards of each slope, beyond the lower edge of a painted rafter."""
    a0, b0 = rafter_line(4 + 60 * 19 + 3.5, -1)          # left slope: rafter 19, the nearest
    a1, b1 = rafter_line(4 + 60 * 17 + 3.5, 1)           # right slope: rafter 17
    # half-planes on the corner's side of each line
    y, x = np.mgrid[0:H, 0:W].astype(F32)
    def side_of(a, b, px, py):
        return (b[0] - a[0]) * (py - a[1]) - (b[1] - a[1]) * (px - a[0])
    sl = side_of(a0, b0, x, y) * np.sign(side_of(a0, b0, 0.0, 0.0))
    sr = side_of(a1, b1, x, y) * np.sign(side_of(a1, b1, float(W), 0.0))
    alpha = ((sl > 0) & (x < W / 2)) | ((sr > 0) & (x > W / 2))
    alpha = alpha.astype(F32)
    c = back.copy()
    # deep and warm, a little less so toward the lamp; lit along the underside that faces it
    gl = toward_lamp(y, x, 700.0)
    k = (0.42 - 0.12 * gl)[..., None]
    c = c * (1 - k) + UMBER * k
    c[..., 0] = np.minimum(c[..., 0] + 0.025, 1)
    r = lamp_rim(alpha, width=2.4)
    c = c + r[..., None] * (LAMPLIGHT * 0.34 - c * 0.15)
    return np.clip(c, 0, 1), alpha


def front_dark(c, alpha):
    """The toy box, the crate, the hen house, the nest and the door: the near dark mass, warm, lamp on one side."""
    y, x = np.mgrid[0:H, 0:W].astype(F32)
    gl = toward_lamp(y, x, 560.0)
    # a soft inner falloff: the face of each thing turned to the lamp keeps more of its colour than the far side
    inner = soft(alpha, 14.0)
    k = (1.0 - 0.30 * gl * inner)[..., None]
    deep = np.array([0.50, 0.38, 0.30], dtype=F32)                        # a warm glaze over the near things: deep, not grey
    out = c * (1 - k * (1 - deep))
    out = out * 0.88 + UMBER * 0.12
    out[..., 0] = np.minimum(out[..., 0] + 0.02, 1)                      # a frankly warm note (keying cools darks)
    r = np.maximum(lamp_rim(alpha, width=2.2), 0.55 * lamp_rim(alpha, width=5.0))
    out = out + r[..., None] * (LAMPLIGHT * 0.60 - out * 0.30) * (0.55 + 0.45 * gl)[..., None]
    return np.clip(out, 0, 1)


def floor_pool():
    """The lamp's pool on the floorboards: splatted from the floor itself through the View, then softened."""
    X, Z = np.meshgrid(np.arange(0, WD, 2.0), np.arange(0, 1180, 2.0))
    d = np.hypot(X - LAMP_XYZ[0], Z - LAMP_XYZ[2])
    f = np.exp(-(d / 150.0) ** 2 * 1.2)
    f *= np.clip((WD - 18 - X) / 40.0, 0, 1)
    a_, u_, d_ = v.cam_space(X, np.zeros_like(X), Z)
    px, py = v._proj(a_, u_, np.maximum(d_, 1e-3))
    px, py = np.round(px).astype(int), np.round(py).astype(int)
    ok = (px >= 0) & (px < W) & (py >= 0) & (py < H)
    pool = np.zeros((H, W), F32)
    np.maximum.at(pool, (py[ok], px[ok]), f[ok].astype(F32))
    return np.clip(soft(pool, 3.0), 0, 1)


def deepen_back(c):
    y, x = np.mgrid[0:H, 0:W].astype(F32)
    out = c.copy()
    # the lamp's pool on the boards (warm, and most on the floor near the bedside table)
    pool = floor_pool()
    out = out * (1 + pool[..., None] * 0.55 * LAMPLIGHT)
    # the far end: the gable wall and the far boards, cooler and paler (air of a moonlit room)
    gable = soft(poly_mask([v.pt(0, 0, 0), v.pt(WD, 0, 0), v.pt(WD, KNEE, 0), v.pt(WD / 2, RIDGE, 0), v.pt(0, KNEE, 0)]), 5.0)
    floor_far = np.clip((470.0 - y) / 118.0, 0, 1) ** 1.3
    far = np.maximum(gable * 0.85, floor_far * (y > 300)) * (1 - 0.6 * pool)
    cool = np.array([0.66, 0.70, 0.84], dtype=F32)
    m = (far * 0.16)[..., None]
    out = out * (1 - m) + cool * m
    # the near boards deeper and warmer, toward the lens
    t = np.clip((y - 455.0) / 145.0, 0, 1)[..., None]
    out = out * (1 - t * np.array([0.10, 0.15, 0.22], dtype=F32))
    return np.clip(out, 0, 1)


def to_8bit(pic, path, colors, alpha=None, dear=()):
    parts = [pic if alpha is None else pic[alpha > 0.5][None]]
    for (x0, y0, x1, y1) in dear:
        crop = pic[y0:y1, x0:x1]
        parts += [crop] * 3
    pal = palette_of(parts, colors)
    idx = to_palette(pic, pal, speckle=0.006)
    save(path, idx, pal, alpha)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    back, _ = load("back.png")
    for name in ("fort.png", "flashlight.png", "teaparty.png", "mobile.png", "layout.json"):
        shutil.copyfile(f"{SRC}/{name}", f"{OUT}/{name}")
    nc, na = near_rafters(back)
    fc, fa = load("front.png")
    fd = front_dark(fc, fa)
    nb = deepen_back(back)
    if "fast" in sys.argv:
        Image.fromarray((nb * 255).astype(np.uint8)).save("out/lilsis-depth-back.png")
        sys.exit()
    dear = [(140, 180, 300, 390), (395, 215, 520, 310), (500, 240, 700, 460), (380, 350, 520, 440), (255, 120, 440, 310)]
    to_8bit(nb, f"{OUT}/back.png", 160, dear=dear)
    to_8bit(fd, f"{OUT}/front.png", 96, fa, dear=[(280, 450, 450, 600), (520, 480, 640, 600)])
    to_8bit(nc, f"{OUT}/near.png", 48, na)
    print("near share", round(float(na.mean()) * 100, 1), "front share", round(float(fa.mean()) * 100, 1))

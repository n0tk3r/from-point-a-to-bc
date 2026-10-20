"""drive-things.png and drive-things.json (highway_drive.py, ROAD-18P): the things that stand beside the road, painted as
the painting paints them, on one sheet.

THE LIGHT is the painting's: the sun dead ahead and low, everything seen against it: the faces toward us in violet shade,
a gold rim on top and down the edges toward the sun, the tips of grass and twigs on fire. No thing carries its own long
shadow (the engine lays it on the ground). A thing on the left of the road has the sun on its right, and one on the
right has it on its left: so most things are painted twice, `-l` for the left of the road and `-r` for the right.

TWO KINDS OF PICTURE.

  The painting's own things (set pieces), for where the camera stops (drive-stop.json places them): every bush, tuft and
  stone highway.py paints, its two tumbleweeds, its jackrabbit, its three birds on the wire, its windpump and the sign.
  Each is cut out of the painting itself: highway's details() is run whole, exactly as it paints back.png, and as each
  thing is drawn the picture under its marks is kept (highway_drive_world.details_one_by_one); its sprite is that picture
  wherever the thing itself covers at least CUT of a pixel, graded and finished as back.png is (the same grain, the same
  152 colours, the same speckle, pixel for pixel). Each is at its own pixels a metre, 800 / z for the z it stands at
  when the camera stops (a hair under, so that the engine draws it at k >= 1: its own pixels, hard), and its foot is
  placed by the contract's camera (eye 2.70 m) so that the engine puts every pixel where the painting has it. Where a
  nearer thing covers it in the painting, its sprite still has itself (the nearer one is drawn over it).

  The sign is the painting's board and posts (`sign`, at 800 / 17.3 = 46.2427 px a metre: at 17.3 m its board lands on
  x 599 to 752, y 286 to 378, pixel for pixel), and `sign-bc` is the same with sign-bc.png's board (POINT B.C.) laid in.

  The things of the rows (the merge's seeded rows: poles, reflector posts, fence posts, brush, grass, stones, Joshua
  trees, a tumbleweed, the jackrabbit): painted with highway.py's own functions (pole, sage, tuft, stone, tumbleweed,
  jackrabbit, bird, and its fence posts and reflector posts as details() draws them), in the light close by (no air: the
  engine's haze is for them), at a size good for where they pass the camera. The telephone pole is the painting's own
  nearest (`pole`: at 44.44 px a metre, it is the painting's pole, pixel for pixel, at 18 m). Joshua trees are new to
  the painting: `joshua` here paints them in its manner, with sage's colours.

THE JSON is round sixteen's: { "ppm": 48, "sprites": { name: { "box": [x, y, w, h], "foot": [fx, fy] (in the box's own
pixels), "height": metres above the foot, "ppm": its own when not 48 } } }, and one field more for the merge,
"air": how much of the painting's air the thing takes far off (highway.airy's: things 1, the poles 0.5: they keep dark
against the bright sky as the painting's do; set pieces 0: they carry the painting's own air for where they stand)."""

import json
import math

import numpy as np
from PIL import Image

import highway as HW
from brush import F32, curve, grain, lerp, palette_of, rgb, to_palette
from highway_kit import Paper, grade, mix
import highway_drive_kit as K
import highway_drive_world as Wd

PPM = 48
NEAR, EDGE = 72.0, 96.0                      # the near brush's pixels a metre; the grass', stones', tumbleweed's and rabbit's
CUT = 0.2                                   # how much of a pixel a set piece must cover to be in its sprite
GROUND_AT = 520.0                           # the frame row the generic things are painted standing on (airy: no air there)


# ---------------------------------------------------------------- the painting's finish, pixel for pixel
class Finish:
    """highway.finish() as it was laid on back.png, for any pixel of the frame: grade, the grain at that pixel (seed 7,
    0.02), and the painting's own 152 colours with the speckle at that pixel (seed 5, 0.014)."""

    def __init__(self, palette):
        self.pal = np.asarray(palette, F32)
        rng = np.random.default_rng(7)                                   # brush.grain(picture, 7, 0.02), the field alone
        fine = rng.normal(0, 1, (K.H, K.W)).astype(F32)
        from brush import blur
        coarse = blur(rng.normal(0, 1, (K.H, K.W)).astype(F32), 0.8) * 1.6
        self.grain = ((fine * 0.7 + coarse * 0.6) * 0.02)[..., None]
        rng = np.random.default_rng(5)                                   # brush.to_palette(..., seed=5, speckle=0.014)
        self.speckle = (rng.normal(0, 0.014, (K.H, K.W, 1)).astype(F32) + rng.normal(0, 0.014 * 0.35, (K.H, K.W, 3)).astype(F32))

    def index(self, graded, box):
        """Palette indexes for a graded picture covering `box` of the frame."""
        x0, y0, x1, y1 = box
        g = np.clip(graded + self.grain[y0:y1, x0:x1], 0, 1) + self.speckle[y0:y1, x0:x1]
        d = ((g.reshape(-1, 1, 3) - self.pal[None, :, :]) ** 2).sum(-1)
        return d.argmin(1).reshape(g.shape[:2])


# ---------------------------------------------------------------- set pieces: the painting's own things
def stop_name(rec, n):
    return {"bush": "stop-bush", "tuft": "stop-tuft", "stone": "stop-stone", "weed": "stop-tumbleweed", "rabbit": "stop-jackrabbit",
            "pump": "windpump", "tread": "stop-tread", "bottle": "stop-bottle", "hubcap": "stop-hubcap"}[rec["kind"]] + (
        "" if rec["kind"] in ("rabbit", "pump", "tread", "bottle", "hubcap") else f"-{n:03d}")


def stop_pieces(records, final, fin):
    """Every bush, tuft, stone, tumbleweed, the jackrabbit and the windpump of the painting, cut out of it as it was drawn;
    and the strip of tire, the bottle and the hubcap on the shoulders (run 3: the road strip has them flat, as they lie,
    but the painting paints them thicker than a flat thing at their depth would be, so at the stop they are the
    painting's own cut-outs, laid over the strip's).
    -> [{name, kind, X, z, idx (palette indexes), alpha, foot, ppm, height, side}]"""
    out, count = [], {}
    for rec in records:
        if rec["kind"] not in ("bush", "tuft", "stone", "weed", "rabbit", "pump", "tread", "bottle", "hubcap") or rec["box"] is None:
            continue
        kind, z_cm, what = rec["kind"], rec["z"], rec["what"]
        X = what[0] / 100.0
        z = z_cm / 100.0
        cut = whole_piece(rec, fin)
        if cut is None:
            continue
        idx, alpha, (x0, y0) = cut
        fx, fy = Wd.stage(X, z)                                            # where the engine puts its foot: the contract's camera
        count[kind] = count.get(kind, 0) + 1
        ppm = 800.0 / z * (1 - 2e-6)
        name = stop_name(rec, count[kind])
        out.append({"name": name, "kind": kind, "X": X, "z": z, "idx": idx, "alpha": alpha, "foot": (fx - x0, fy - y0),
                    "ppm": ppm, "height": (fy - y0) / ppm, "order": len(out)})
    return out


def whole_piece(rec, fin, seed=1850):
    """A set piece's picture: within the frame, the painting as it was just after the thing was drawn, finished as
    back.png is, wherever the thing covers at least CUT of a pixel; and where the thing runs off the frame (a big bush in
    a bottom corner), the rest of it drawn alone with the same marks, over the plain, so that it is whole when it is seen
    before the camera stops. -> (indexes into the painting's palette, alpha, the box's top left on the frame) or None."""
    full = Wd.marks_box(rec["marks"], size=None)
    if full is None:
        return None
    color, cover = Wd.replay(rec["marks"], full)
    keep = cover >= CUT
    if not keep.any():
        return None
    fx0, fy0, fx1, fy1 = full
    idx = np.zeros(keep.shape, np.intp)
    inside = np.zeros(keep.shape, bool)
    ix0, iy0, ix1, iy1 = max(0, fx0), max(0, fy0), min(K.W, fx1), min(K.H, fy1)
    if ix1 > ix0 and iy1 > iy0:
        bx0, by0 = rec["box"][:2]
        after = rec["after"][iy0 - by0:iy1 - by0, ix0 - bx0:ix1 - bx0]
        idx[iy0 - fy0:iy1 - fy0, ix0 - fx0:ix1 - fx0] = fin.index(grade(after), (ix0, iy0, ix1, iy1))
        inside[iy0 - fy0:iy1 - fy0, ix0 - fx0:ix1 - fx0] = True
    out = keep & ~inside
    if out.any():                                                          # (off the frame: alone, over the plain)
        c = grade(color) * cover[..., None] + rgb(K.BASE["plain"]) * (1 - cover[..., None])
        g = grain(np.ascontiguousarray(c, dtype=F32), seed + int(rec["z"]) % 1000, 0.02)
        idx[out] = to_palette(g, fin.pal, seed=seed, speckle=0.014)[out]
    ys, xs = np.nonzero(keep)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return idx[y0:y1, x0:x1], keep[y0:y1, x0:x1], (fx0 + x0, fy0 + y0)


def stop_birds(final, fin):
    """The three birds on the top wire between the first two poles, cut out of the painting (nothing is drawn over them)."""
    out = []
    for i, b in enumerate(Wd.birds(), 1):
        tee = Wd._Tee((K.H, K.W))
        Wd._Tee.current = marks = []
        HW.bird(tee, b["at"][0], b["at"][1], b["size_px"], b["facing"])
        Wd._Tee.current = None
        box = Wd.marks_box(marks)
        _, cover = Wd.replay(marks, box)
        keep = cover >= CUT
        ys, xs = np.nonzero(keep)
        x0, y0, x1, y1 = box[0] + xs.min(), box[1] + ys.min(), box[0] + xs.max() + 1, box[1] + ys.max() + 1
        idx = fin.index(grade(final[y0:y1, x0:x1]), (x0, y0, x1, y1))
        alpha = keep[y0 - box[1]:y1 - box[1], x0 - box[0]:x1 - box[0]]
        # its foot is on the ground under it (the contract stands things on their feet), so its box runs down to the
        # ground, clear below the bird
        fx, fy = Wd.stage(b["X"], b["z"])
        ground = int(math.floor(fy)) + 1
        pad = ground - y1
        idx = np.concatenate([idx, np.zeros((pad, idx.shape[1]), idx.dtype)], 0)
        alpha = np.concatenate([alpha, np.zeros((pad, alpha.shape[1]), bool)], 0)
        ppm = 800.0 / b["z"] * (1 - 2e-6)
        out.append({"name": f"stop-bird-{i}", "kind": "bird", "X": b["X"], "z": b["z"], "Y": b["Y"], "idx": idx, "alpha": alpha,
                    "foot": (fx - x0, fy - y0), "ppm": ppm, "height": (fy - y0) / ppm})
    return out


def the_sign_alone(seed=HW.SEED + 400):
    """The sign painted by highway.the_sign() alone, on black and on white: -> (its colour, how much of each pixel it
    covers). (The sign paints straight onto the picture; two grounds tell what is the sign's.)"""
    a = np.zeros((K.H, K.W, 3), F32)
    b = np.ones((K.H, K.W, 3), F32)
    HW.the_sign(a, seed)
    HW.the_sign(b, seed)
    cover = np.clip(1 - (b - a).max(-1), 0, 1)
    color = np.where(cover[..., None] > 1e-3, a / np.maximum(cover[..., None], 1e-3), 0)
    return np.clip(color, 0, 1), cover


def sign_pieces(sign_after, fin, bc_png):
    """`sign` (POINT B, 40) and `sign-bc` (POINT B.C.): the painting's own board and posts, cut out of the painting as it
    was just after the sign was painted, at 800 / 17.3 px a metre. sign-bc lays sign-bc.png's board (its own pixels, as the
    game shows it over back.png) over the board."""
    _, cover = the_sign_alone()
    keep = cover >= CUT
    ys, xs = np.nonzero(keep)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    idx = fin.index(grade(sign_after[y0:y1, x0:x1]), (x0, y0, x1, y1))
    alpha = keep[y0:y1, x0:x1]
    z = Wd.SIGN_M["z"]
    X = (Wd.SIGN_M["posts"][0] + Wd.SIGN_M["posts"][1]) / 2                # its foot: the ground between its two posts
    fx, fy = Wd.stage(X, z)
    ppm = 800.0 / z * (1 - 2e-6)
    base = {"kind": "sign", "X": X, "z": z, "alpha": alpha, "foot": (fx - x0, fy - y0), "ppm": ppm, "height": (fy - y0) / ppm}
    bc = Image.open(bc_png)
    bc_rgb = np.asarray(bc.convert("RGB"), F32)[y0:y1, x0:x1] / 255
    bc_on = (np.asarray(bc.convert("RGBA"))[..., 3] >= 128)[y0:y1, x0:x1]
    base["box_frame"] = (x0, y0, x1, y1)
    return dict(base, name="sign", idx=idx), dict(base, name="sign-bc", idx=idx, over=(bc_rgb, bc_on)), (x0, y0, x1, y1)


# ---------------------------------------------------------------- the things of the rows
def paint_alone(draw, foot_x, foot_y, size, ss=3):
    """Draw one thing with highway's own marks on a clear Paper the size of the frame, standing at (foot_x, foot_y):
    -> (graded colour, coverage) cropped to it, and its foot in the crop."""
    tee = Wd._Tee(size)
    Wd._Tee.current = marks = []
    draw(tee)
    Wd._Tee.current = None
    box = Wd.marks_box(marks, size=size)
    c, a = Wd.replay(marks, box, ss)
    return grade(c), a, (foot_x - box[0], foot_y - box[1])


def matte(color, cover, foot, below, above=None, eye_px=None, cut=0.3):
    """A thing's sprite from its colour and coverage: hard edged, the pixels it covers at least `cut` of, each laid over
    what is usually behind it (`below` the horizon: the plain; `above`: the low sky, for what stands higher than the eye)
    as much as the thing does not cover it. -> (rgb, alpha, foot), cropped."""
    keep = cover >= cut
    ys, xs = np.nonzero(keep)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    bg = np.empty(color.shape, F32)
    bg[...] = rgb(below) if isinstance(below, str) else below
    if above is not None and eye_px is not None:                       # (rows higher than the eye above its foot)
        rows = np.arange(color.shape[0])[:, None]
        bg[(foot[1] - rows[:, 0]) > eye_px] = rgb(above)
    rgb_ = color * cover[..., None] + bg * (1 - cover[..., None])
    return rgb_[y0:y1, x0:x1], keep[y0:y1, x0:x1], (foot[0] - x0, foot[1] - y0)


PLAIN_BEHIND = K.BASE["plain"]
SKY_BEHIND = "#e8946e"


def generic(seed=1830):
    """The things of the rows, in both lights: -> [{name, rgb, alpha, foot, ppm, height}]"""
    out = []
    shape = (K.H * 2, K.W)                                               # (room above for the tall ones)
    fy = GROUND_AT + K.H                                                 # their feet: low on the frame, where highway's air is none

    def add(name, draw, ppm, height_m, above=False, cut=0.3, eye=None):
        c, a, foot = paint_alone(draw, 400.0, fy, shape)
        e = None if eye is None else eye * ppm
        rgb_, alpha, foot = matte(c, a, foot, PLAIN_BEHIND, SKY_BEHIND if above else None, e, cut)
        out.append({"name": name, "rgb": rgb_, "alpha": alpha, "foot": foot, "ppm": ppm, "height": height_m})

    # brush: highway.sage(), sizes in metres, painted at 72 px a metre (a bush at the inner edge of its row, 4.4 m out,
    # passes out of the picture 8.8 m ahead, where it is drawn at 1.26 of that: at 48 its pixels would show, doubled);
    # seeds chosen for sagebrush, rabbitbrush in bloom and a dry one (sage picks its kind from its seed). And the first
    # four again painted small, as the painting paints
    # its brush far off: `-mid` at 24 px a metre, `-far` at 12. Shrunk from 48, a bush is its dark body with a few
    # sparks; painted small, its rim and its flowers are a pixel wide, as the painting's far drifts are, golden. For the
    # rows that are only ever seen far off (12 to 30 m out: never nearer than 24 m ahead, where a `-mid` one is drawn at
    # 1.4 times its size at most; beyond 30 m out, never nearer than 60 m: a `-far` one at 1.1 at most)
    SAGE = [("sage-1", 1.00, 0.66), ("sage-2", 1.35, 0.92), ("sage-3", 1.70, 1.12), ("sage-4", 0.72, 0.46),
            ("sage-5", 1.20, 0.80), ("sage-6", 1.50, 1.00)]
    for i, ((name, wide, tall), k) in enumerate(zip(SAGE, _sage_seeds(seed))):
        for suffix, ppm in (("", NEAR), ("-mid", 24.0), ("-far", 12.0)):
            if suffix and i >= 4:
                continue
            for L, side in (("l", 1), ("r", -1)):
                add(f"{name}{suffix}-{L}", lambda t, wide=wide, tall=tall, k=k, side=side, ppm=ppm: HW.sage(t, 400.0, fy, wide * ppm, tall * ppm, k, side), ppm, tall)
    # grass, stones, the tumbleweed and the jackrabbit at 96 px a metre: they stand at the very edge of the paving, and
    # pass out of the picture from 6.3 m ahead
    for name, r_m, k in (("tuft-1", 0.20, seed + 21), ("tuft-2", 0.32, seed + 22)):
        for L, side in (("l", 1), ("r", -1)):
            add(f"{name}-{L}", lambda t, r_m=r_m, k=k, side=side: HW.tuft(t, 400.0, fy, r_m * EDGE, k, side), EDGE, r_m * 1.2)
    for name, r_m, k in (("stone-1", 0.09, seed + 31), ("stone-2", 0.16, seed + 32), ("stone-3", 0.26, seed + 33)):
        for L, side in (("l", 1), ("r", -1)):
            add(f"{name}-{L}", lambda t, r_m=r_m, k=k, side=side: HW.stone(t, 400.0, fy, r_m * EDGE, r_m * EDGE * 0.62, k, side), EDGE, r_m * 1.24)
    for L, side in (("l", 1), ("r", -1)):
        add(f"tumbleweed-{L}", lambda t, side=side: HW.tumbleweed(t, 400.0, fy, 0.36 * EDGE, seed + 41, side), EDGE, 0.70)
        add(f"jackrabbit-{L}", lambda t, side=side: HW.jackrabbit(t, 400.0, fy, 0.58 * EDGE, side), EDGE, 0.45)
        for name, h_m, k in (("joshua-1", 5.4, seed + 51), ("joshua-2", 4.3, seed + 52)):
            add(f"{name}-{L}", lambda t, h_m=h_m, k=k, side=side: joshua(t, 400.0, fy, h_m * 40.0, k, side), 40.0, h_m, above=True, eye=K.EYE)
        for name, h_m, lean in (("fence-1", 1.14, 0.02), ("fence-2", 1.24, -0.03)):
            add(f"{name}-{L}", lambda t, h_m=h_m, lean=lean, side=side: fence_post(t, 400.0, fy, h_m, lean, -side, PPM), PPM, h_m, cut=0.4)
    add("post", lambda t: marker(t, 400.0, fy, 96.0), 96.0, 1.05, cut=0.4)
    add("bird", lambda t: HW.bird(t, 400.0, fy, 0.20 * PPM, 1), PPM, 0.2, above=True, eye=0.0)
    return out


def _sage_seeds(seed):
    """Seeds for highway.sage() giving, in order: a sagebrush, a sagebrush, a rabbitbrush in bloom, a dry one, a
    sagebrush, a rabbitbrush in bloom."""
    got, k = [], seed
    for kind in ("plain", "plain", "bloom", "dry", "plain", "bloom"):
        while True:
            k += 1
            rng = np.random.default_rng(k)
            bloom = rng.random() < 0.16
            dry = (not bloom) and rng.random() < 0.10
            if kind == ("bloom" if bloom else "dry" if dry else "plain"):
                got.append(k)
                break
    return tuple(got)


def marker(sheet, fx, fy, ppm):
    """A white reflector post, as highway.details() draws its markers: a grey post 6 cm wide, 1.05 m, its top 23 cm white,
    an amber reflector near the top."""
    s = ppm / 100.0
    f, t = (fx, fy), (fx, fy - 105 * s)
    sheet.line([f, t], "#8a8098", max(0.8, s * 6.0))
    sheet.line([(fx, fy - 82 * s), t], "#e8e2e6", max(0.8, s * 7.0))
    sheet.ellipse(t[0], t[1] + s * 12, s * 4.2, s * 4.2, "#ffd27a")


def fence_post(sheet, fx, fy, tall_m, lean, toward_sun, ppm):
    """A fence post as highway.details() draws its fences: weathered dark wood 9 cm wide, the sun along its edge toward
    the road. `toward_sun`: -1 when the sun is to its left (a post on the right of the road), +1 to its right."""
    s = ppm / 100.0
    tall = tall_m * 100
    f, t = (fx, fy), (fx + lean * tall * s, fy - tall * s)
    sheet.line([f, t], "#3a2a40", max(0.8, s * 9.0))
    sheet.line([(f[0] + toward_sun * s * 4, f[1]), (t[0] + toward_sun * s * 4, t[1])], HW.airy("#f0a868", 600, 0.4), 0.7 * max(1.0, s / 0.5), 0.8)


def joshua(sheet, fx, fy, height, seed, side):
    """A Joshua tree seen against the light, in highway.py's manner and with sage's colours: a stout trunk in a skirt of
    dead leaves, arms forking out and up and forking again, every limb shaggy, each tip a ball of stiff spikes. All of it
    dark and cool against the bright west, the sky's violet on the upturned spikes, the sun coming round every edge toward
    it as a broken line of gold, the spikes' tips on fire. `height` in px (the leaf balls' tops); `side` as sage's (+1: the
    sun to its right). The painting has none; the author asked for them (ROAD-18)."""
    rng = np.random.default_rng(seed)
    dark, bark = HW.airy("#241f3a", fy), HW.airy("#2e2234", fy)
    shag_d, shag_m = HW.airy("#3a2a34", fy), HW.airy("#5a4648", fy)
    mid, lite = HW.airy("#3b4558", fy), HW.airy("#66787e", fy)
    rim, fire = HW.airy("#e2924e", fy, 0.5), HW.airy("#ffd98c", fy, 0.3)
    segs, tips = [], []

    def grow(x, y, ang, length, thick, depth):
        bend = ang * rng.uniform(0.35, 0.7)
        mx, my = x + math.sin(math.radians(ang)) * length * 0.5, y - math.cos(math.radians(ang)) * length * 0.5
        ex, ey = mx + math.sin(math.radians(bend)) * length * 0.5, my - math.cos(math.radians(bend)) * length * 0.5
        segs.append(((x, y), (mx, my), thick))
        segs.append(((mx, my), (ex, ey), thick * 0.92))
        if depth > 0 and rng.random() < 0.85:
            n = 2 if rng.random() < 0.75 else 1
            for k in range(n):
                a = bend + (rng.uniform(18, 42) * (-1 if k == 0 else 1) if n == 2 else rng.uniform(-25, 25))
                grow(ex, ey, a, length * rng.uniform(0.62, 0.85), thick * 0.82, depth - 1)
        else:
            tips.append((ex, ey))

    # its skeleton in units of its height, then scaled so that the balls' tops are `height` above the foot
    segs.append(((0.0, 0.0), (0.004, -0.2), 0.07))
    arms = 3 if rng.random() < 0.6 else 2
    spread = [-1.0, 1.0] if arms == 2 else [-1.0, 0.15, 1.0]
    for k in range(arms):
        a = spread[k] * rng.uniform(42, 58) + rng.normal(0, 6)
        grow(0.004, -0.19, a, rng.uniform(0.2, 0.27), 0.048, 2)
    top = -min(ty for tx, ty in tips) + 0.065
    k_ = height / top
    segs = [((fx + a[0] * k_, fy + a[1] * k_), (fx + b[0] * k_, fy + b[1] * k_), t * k_) for a, b, t in segs]
    tips = [(fx + tx * k_, fy + ty * k_) for tx, ty in tips]
    R = 0.065 * k_                                                      # a leaf ball's reach
    # the limbs: dark, a cooler sheen on their upper side where the sky is, gold along the edge toward the sun
    for (a, b, th) in segs:
        sheet.line([a, b], bark, max(1.0, th))
    for (a, b, th) in segs:
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) + 1e-6
        nx, ny = -dy / L, dx / L                                         # across the limb
        if nx * side < 0:
            nx, ny = -nx, -ny                                            # toward the sun's side
        off = th * 0.38
        if rng.random() < 0.9:
            sheet.line([(a[0] + nx * off, a[1] + ny * off), (b[0] + nx * off, b[1] + ny * off)], rim, max(0.8, th * 0.16), 0.85)
        sheet.line([(a[0] - nx * off * 0.6, a[1] - ny * off * 0.6), (b[0] - nx * off * 0.6, b[1] - ny * off * 0.6)], mid, max(0.7, th * 0.12), 0.5)
    # the shag: dead leaves hanging down every limb, dark, a few catching the light on the sun's side
    for (a, b, th) in segs:
        n = int(5 + math.hypot(b[0] - a[0], b[1] - a[1]) * 0.9)
        for j in range(n):
            f = rng.random()
            x, y = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
            sd = rng.choice([-1.0, 1.0])
            x += sd * th * rng.uniform(0.25, 0.55)
            ln = th * rng.uniform(0.5, 1.1)
            tone = shag_d if rng.random() < 0.6 else shag_m
            if sd * side > 0 and rng.random() < 0.35:
                tone = rim
            sheet.line([(x, y), (x + sd * ln * 0.25, y + ln)], tone, max(0.7, th * 0.10), 0.9)
    # the leaf balls: a dark heart, stiff spikes all ways (up most), cool where they face the sky, the tips toward the sun
    # burning
    for (tx, ty) in tips:
        sheet.ellipse(tx, ty, R * 0.55, R * 0.5, dark)
        spikes = []
        for j in range(int(26 + R * 1.2)):
            a = rng.uniform(-0.15 * math.pi, 1.15 * math.pi) if rng.random() < 0.85 else rng.uniform(0, 2 * math.pi)
            ln = R * rng.uniform(0.6, 1.15)
            ux, uy = math.cos(a), -math.sin(a)
            toward = ux * side
            spikes.append((rng.random() + (0.3 if uy < -0.5 else 0), ux, uy, ln, toward))
        for _, ux, uy, ln, toward in sorted(spikes):
            tone = dark if rng.random() < 0.45 else (lite if uy < -0.55 and rng.random() < 0.6 else mid)
            sheet.line([(tx, ty), (tx + ux * ln, ty + uy * ln)], tone, max(0.8, R * 0.09))
            if toward > 0.15 or uy < -0.7:
                if rng.random() < 0.55 + 0.35 * toward:
                    hot = rng.random() < 0.3 + 0.3 * toward
                    sheet.line([(tx + ux * ln * 0.7, ty + uy * ln * 0.7), (tx + ux * ln, ty + uy * ln)], fire if hot else rim, max(0.8, R * 0.08), 0.95)


def pole_piece(records, fin):
    """`pole`: the painting's nearest telephone pole (18 m ahead, 7.5 m left), cut out of the painting as it was drawn: at
    44.44 px a metre it is that pole pixel for pixel when the camera stops; the merge's row of poles draws every pole
    with it."""
    rec = next(r for r in records if r["kind"] == "pole" and r["what"][2] == 0)
    idx, alpha, (x0, y0) = whole_piece(rec, fin)
    X, z = rec["what"][0] / 100.0, rec["z"] / 100.0
    fx, fy = Wd.stage(X, z)
    ppm = 800.0 / z * (1 - 2e-6)
    return {"name": "pole", "kind": "pole", "X": X, "z": z, "idx": idx, "alpha": alpha, "foot": (fx - x0, fy - y0), "ppm": ppm,
            "height": (fy - y0) / ppm}


# ---------------------------------------------------------------- the sheet
def pack(items, width=1024, gap=2):
    """Shelves, tallest first. -> {name: (x, y)}, the sheet's height."""
    order = sorted(items, key=lambda it: (-it["alpha"].shape[0], -it["alpha"].shape[1], it["name"]))
    at, x, y, shelf = {}, gap, gap, 0
    for it in order:
        h, w = it["alpha"].shape
        if x + w + gap > width:
            x, y, shelf = gap, y + shelf + gap, 0
        at[it["name"]] = (x, y)
        x += w + gap
        shelf = max(shelf, h)
    return at, y + shelf + gap


def foot_inside(it):
    """The contract has a thing's foot in its box: where a stone's foot is a pixel under its lowest painted row (its
    edge, under a third of a pixel, was left out), the box gets clear rows (or columns) to take it in."""
    idx, alpha = it["idx"], it["alpha"]
    fx, fy = it["foot"]
    h, w = alpha.shape
    top, bottom = max(0, int(math.ceil(-fy))), max(0, int(math.ceil(fy - h)))
    left, right = max(0, int(math.ceil(-fx))), max(0, int(math.ceil(fx - w)))
    if not (top or bottom or left or right):
        return it
    pad = ((top, bottom), (left, right))
    return dict(it, idx=np.pad(idx, pad), alpha=np.pad(alpha, pad), foot=(fx + left, fy + top))


AIR = {"pole": 0.6}                         # (generic things not named here take the painting's air in full: 1)


def sheet(pieces, generic_items, painting_palette, bc_png, seed=1840, extra_colors=55):
    """Lay every picture on one sheet, with one palette: the painting's own 152 colours (the set pieces are in them,
    index for index), sign-bc.png's 48 (its board, index for index), and `extra_colors` more for the rows' things.
    -> (palette indexes, alpha, palette (255 colours), JSON)."""
    pal_paint = np.asarray(painting_palette, F32)
    bc = Image.open(bc_png)
    pal_bc = np.asarray(bc.getpalette(), np.uint8).reshape(-1, 3)[:48].astype(F32) / 255
    bc_idx = np.asarray(bc)
    # the rows' things: grain as the painting has it, then colours of their own where the painting's are not enough
    gen = []
    for k, it in enumerate(generic_items):
        g = grain(np.ascontiguousarray(it["rgb"]), seed + k, 0.02)
        gen.append(g)
    px = np.concatenate([g[it["alpha"]] for g, it in zip(gen, generic_items)])
    pal_extra = palette_of([px.reshape(-1, 1, 3)], colors=extra_colors, seed=seed % 97 + 3)
    pal = np.concatenate([pal_paint, pal_bc, pal_extra])[:255]
    items = []
    for p in pieces:
        idx = p["idx"].astype(np.uint8).copy()
        if "over" in p:                                               # sign-bc: sign-bc.png's board, its own indexes
            bx0, by0 = p["box_frame"][:2]
            h, w = idx.shape
            on = p["over"][1]
            idx[on] = (len(pal_paint) + bc_idx[by0:by0 + h, bx0:bx0 + w][on]).astype(np.uint8)
        items.append(dict(p, idx=idx))
    for g, it in zip(gen, generic_items):
        idx = to_palette(g, pal, seed=seed + 7, speckle=0.014)
        items.append(dict(it, idx=idx))
    items = [foot_inside(it) for it in items]
    at, H_ = pack(items)
    W_ = 1024
    sheet_idx = np.zeros((H_, W_), np.uint8)
    sheet_alpha = np.zeros((H_, W_), F32)
    sprites = {}
    for it in items:
        x, y = at[it["name"]]
        h, w = it["alpha"].shape
        sheet_idx[y:y + h, x:x + w][it["alpha"]] = it["idx"][it["alpha"]]
        sheet_alpha[y:y + h, x:x + w][it["alpha"]] = 1.0
        e = {"box": [int(x), int(y), int(w), int(h)], "foot": [round(float(it["foot"][0]), 3), round(float(it["foot"][1]), 3)],
             "height": round(float(it["height"]), 3)}
        if abs(it["ppm"] - PPM) > 1e-9:
            e["ppm"] = round(float(it["ppm"]), 6)
        e["air"] = 0 if it["name"].startswith(("stop-", "sign", "windpump")) else AIR.get(it["name"], 1)
        sprites[it["name"]] = e
    meta = {"ppm": PPM, "sprites": dict(sorted(sprites.items()))}
    return sheet_idx, sheet_alpha, pal, meta

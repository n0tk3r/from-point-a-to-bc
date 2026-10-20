"""sky.png, and the painting's light that stays where it is on the stage (highway_drive.py, ROAD-18P).

SKY.PNG is the backdrop, 800 x 600, opaque, still.

  Above the horizon (rows 0 to 329) it is back.png painted again by highway.py's own code, the same seeds and the same
  passes, but for one thing: highway's details() is stopped where it has sorted its things
  (highway_drive_world.details_until_things), so no wire, bird, pole, sign, windpump, fence or bush is drawn, and the
  sky and the mesas are painted where they were behind them. It is graded and finished as back.png is (highway.grade,
  the same grain, the painting's own 152 colours and speckle), so every pixel that nothing stood on is back.png's own,
  index for index.

  Below the horizon (row 330 down) it is the far plain, as a backdrop for a ground that moves: highway.under()'s plain,
  shoulders and road, each in its colours by distance, with the dust burning at the horizon and the glow round the sun's
  place on the plain, brushed and graded as the painting is; but nothing that comes and goes as the camera moves: no long
  shadows (of things no longer there), no road marks (no lines, cracks or patches), no shine down the road and no deeper
  corners (those are the light pictures'). The drive draws its ground over it from row 331 down; row 330, the horizon
  itself, is sky.png's. With the engine's `haze: "backdrop"` the far ground would fade into this one. From row 365 down
  (never seen: always under the drive's ground) it is the same plain in plain paint, without grain and speckle.

THE LIGHT (two pictures, 800 x 600, RGBA, still on the stage while the ground goes by under them: the engine's `light`,
laid in this order, each at opacity 1, over the ground and its shadows, under the things):

  light-shade.png  "multiply", then
  light-glow.png   "screen".

  Together they turn the drive's ground, as the engine draws it with the haze colour and distance of highway_drive_kit
  (HAZE, HAZE_FAR) and as it is on average along the road, into the painting's ground with all its light: the dust on
  fire at the horizon, the glow round the sun's place, the long shine down the road and the polished wheel tracks
  catching it (even, not broken into streaks as the painting's is: those breaks are the road's surface and must go by
  with it), the corners going deeper to hold the eye on the road; and the painting's own colours by distance, which one
  haze (one colour, one distance) can only come near: it leaves the near road about 15 levels too light and the middle
  distance up to 20 too dark, and these put it right. Rows 331 down only (row 330, 4320 m off, is beyond the engine's
  `far` and shows sky.png's own horizon).

  Worked out from: the painting's own light, highway.under() with each light switched on and off, on under()'s ground
  made smooth (every texture and noise of its own at its mean, so that no blotch of the painting's is printed on the
  stage to stand still while the ground goes by), after the grade; the painting's ground by distance, row by row, its
  road, its sand and its plain each as they are on average in the painting (blotched, graded); and the drive's ground on
  average: every row of the three strips over its whole loop, seen through the contract's camera, hazed. Per pixel and
  channel, the multiply darkens where the painting is darker, the screen lightens where it is lighter, so that the
  ground on average comes out the painting's exactly; its own grain and blotches go by under them. (They are made for
  a haze colour. With the engine's `haze: "backdrop"` the far ground is sky.png's, already lit, and the canvas mixes a
  light into the clear part of the pane instead of screening it: an orange line along the horizon. Use a haze colour.)"""

import numpy as np

import highway as HW
from brush import grain, lerp, palette_of, to_palette
from highway_kit import grade
import highway_drive_kit as K
import highway_drive_world as Wd

F32 = np.float32
HZ = 330
PLAIN_PAINT = 365                                            # sky.png's rows from here down: plain paint (never seen)
ALL_LIGHTS = ("glow_horizon", "glow_sun", "shine", "tracks", "shadows", "corners")


def painting(fast=False):
    """highway.py's painting, as its own main() makes it: -> dict(under, info, brushed, back (the finished picture, graded,
    before grain and palette), palette (its 152 colours, as floats))."""
    base, info = HW.under()
    info["under"] = base
    brushed = base.copy() if fast else HW.strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.22)
    back = HW.details(brushed.copy(), info)
    back = grade(back)
    g = grain(back, 7, 0.02)                                                   # (highway.finish: grain, seed 7, 0.02)
    colors = min(152, len(np.unique((g * 255).astype(np.uint8).reshape(-1, 3), axis=0)))
    pal = palette_of([g.reshape(-1, 1, 3)], colors=colors)
    return dict(under=base, info=info, brushed=brushed, back=back, palette=pal)


def finish_as_back(picture, pal):
    """highway.finish's grain and speckle with the painting's own palette: -> palette indexes."""
    g = grain(picture, 7, 0.02)
    return to_palette(g, pal, speckle=0.014)


def far_plain(fast=False):
    """The ground below the horizon as sky.png has it: highway.under() with its plain's two glows and nothing else of its
    light, brushed as the painting is, the horizon said again crisply as details() says it. -> (graded picture, the
    unbrushed one)."""
    base, _ = Wd.under(off=("shine", "tracks", "shadows", "corners"))
    pic = base.copy() if fast else HW.strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.22)
    y = np.arange(pic.shape[0], dtype=F32)[:, None]
    pic = lerp(pic, base, (np.clip(1 - np.abs(y - HZ) / 2.0, 0, 1) * 0.6)[..., None])      # (details: the horizon, level and sharp)
    return grade(pic), base


def paint_sky(P, fast=False):
    """-> (the sky's indexes, its picture graded), from painting()'s parts: the painting above the horizon with nothing
    standing in it, the far plain below."""
    pic, _ = Wd.details_until_things(P["brushed"].copy(), P["info"])
    pic = grade(pic)
    plain, _ = far_plain(fast)
    pic[HZ:] = plain[HZ:]
    idx = finish_as_back(pic, P["palette"])
    # below row PLAIN_PAINT the drive always covers it (its ground is drawn from row 331 to as far as 2000 m: row 331 is
    # 1440 m off): there it is the same far plain in plain paint, without the grain and the speckle, which cost bytes
    idx[PLAIN_PAINT:] = to_palette(pic[PLAIN_PAINT:], P["palette"], speckle=0.0)
    return idx, pic


def painting_light():
    """The painting's own light, as three layers over its ground made smooth (see the top): -> {glow, shine: screen
    amounts L (1 - (1 - p)(1 - L)); shade: multiply factors M}, (H, W, 3) floats, rows 331 down."""
    unlit = grade(Wd.under(off=ALL_LIGHTS, smooth=True)[0])
    with_ = {
        "glow": grade(Wd.under(off=("shine", "tracks", "shadows", "corners"), smooth=True)[0]),
        "shine": grade(Wd.under(off=("glow_horizon", "glow_sun", "shadows", "corners"), smooth=True)[0]),
        "shade": grade(Wd.under(off=("glow_horizon", "glow_sun", "shine", "tracks", "shadows"), smooth=True)[0]),
    }
    below = (np.arange(unlit.shape[0])[:, None] > HZ)[..., None]
    out = {}
    for name in ("glow", "shine"):
        L = 1 - (1 - with_[name]) / np.maximum(1 - unlit, 1.0 / 255)
        out[name] = np.clip(np.where(below, L, 0), 0, 1).astype(F32)
    out["shade"] = np.where(below, np.clip(with_["shade"] / np.maximum(unlit, 1.0 / 255), 0, 1), 1.0).astype(F32)
    return out


def light_painting(base, light):
    """The painting's light laid on a ground as the painting lays it: the glows and the shine (screen), then the corners."""
    p = 1 - (1 - base) * (1 - light["glow"])
    p = 1 - (1 - p) * (1 - light["shine"])
    return p * light["shade"]


STRIP_ORDER = ("desert-l", "road", "desert-r")                # X from -30 to +30 m, at 48 px a metre


def strip_means(folder):
    """The drive's ground as it is on average along the road: each row of the three strips (as they are written, in
    `folder`) over its whole loop, on one line across from -30 m to +30 m at 48 samples a metre. -> (2880, 3)."""
    from PIL import Image
    parts = []
    for name in STRIP_ORDER:
        lo, hi, ppm = K.STRIPS[name]
        m = np.asarray(Image.open(f"{folder}/drive-{name}.png").convert("RGB"), F32).mean(1) / 255
        parts.append(np.repeat(m, int(round(48 / ppm)), 0))
    return np.concatenate(parts, 0)


def drive_mean(M, haze, haze_far):
    """The drive's ground on average as the engine draws it (each pixel the average of the stretch across the road it
    covers, past the strips their outer rows' colour, hazed as far off as the pixel's middle): -> (H, W, 3), its rows
    331 down (nan above), and X of each pixel's middle."""
    n, ppm, X_lo = M.shape[0], 48.0, -30.0
    C = np.concatenate([np.zeros((1, 3)), np.cumsum(M, 0, dtype=np.float64)], 0)
    lo_c, hi_c = M[:16].mean(0), M[-16:].mean(0)

    def S(X):
        r = (X - X_lo) * ppm
        rc = np.clip(r, 0, n)
        k = np.minimum(np.floor(rc).astype(np.intp), n - 1)
        return C[k] + M[k] * (rc - k)[:, None] + np.minimum(r, 0)[:, None] * lo_c + np.maximum(r - n, 0)[:, None] * hi_c

    D = np.full((K.H, K.W, 3), np.nan, F32)
    Xm = np.zeros((K.H, K.W), F32)
    xs = np.arange(K.W, dtype=np.float64)
    hz = _rgb(haze)
    for y in range(HZ + 1, K.H):
        zc = K.FOCAL * K.EYE / (y + 0.5 - HZ)
        X0, X1 = (xs - K.VX) * zc / K.FOCAL, (xs + 1 - K.VX) * zc / K.FOCAL
        avg = (S(X1) - S(X0)) / ((X1 - X0) * ppm)[:, None]
        h = (1 - 0.5 ** (zc * np.sqrt(1 + ((xs + 0.5 - K.VX) / K.FOCAL) ** 2) / haze_far))[:, None]
        D[y] = avg * (1 - h) + hz * h
        Xm[y] = (X0 + X1) / 2
    return D, Xm


def _rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], F32)


def _smooth_rows(v, n, k=2):
    """Per-row means (v, with n pixels each) smoothed over k rows either side, weighted by their pixels; rows with none
    take their nearest neighbour's."""
    out = np.full(v.shape, np.nan, F32)
    rows = len(v)
    for i in range(rows):
        a, b = max(0, i - k), min(rows, i + k + 1)
        w = n[a:b]
        if w.sum() > 0:
            out[i] = (np.nan_to_num(v[a:b]) * w[:, None]).sum(0) / w.sum()
    good = np.nonzero(~np.isnan(out[:, 0]))[0]
    for i in range(rows):
        if np.isnan(out[i, 0]):
            out[i] = out[good[np.argmin(np.abs(good - i))]]
    return out


def class_rows(pic, info, rows):
    """Per row, the mean colour of a ground picture over its road (asphalt, within 2.9 m of the middle), its sand (the
    shoulders, off the asphalt) and its plain (beyond 6.5 m), by `info`'s masks: -> {class: (means, pixels)}."""
    road_m, sh_m, X = info["road"], info["shoulder"], info["across"] / 100.0
    out = {}
    for cls in ("road", "sand", "plain"):
        T, n = np.zeros((len(rows), 3), F32), np.zeros(len(rows), F32)
        for i, y in enumerate(rows):
            if cls == "road":
                sel = (road_m[y] > 0.99) & (np.abs(X[y]) < 2.9)
            elif cls == "sand":
                sel = (sh_m[y] > 0.85) & (road_m[y] < 0.01)
            else:
                sel = (sh_m[y] < 0.01) & (road_m[y] < 0.01) & (np.abs(X[y]) > 6.5)
            n[i] = sel.sum()
            if n[i]:
                T[i] = pic[y][sel].mean(0)
        out[cls] = (T, n)
    return out


def lights(folder, haze=None, haze_far=None):
    """The two light pictures (see the top), for the strips written in `folder` and this haze: -> ({"shade": RGBA,
    "glow": RGBA} (straight floats), what they were made from, to check them)."""
    haze = haze or K.HAZE
    haze_far = haze_far or K.HAZE_FAR
    light = painting_light()
    rows = np.arange(HZ + 1, K.H)
    # the painting's ground by distance, unlit: its ramps as under() paints them made smooth (no blotch to wander from
    # row to row), times what its blotches, pale flats and blown sand do to each part's colour on average (fitted along
    # the rows: a straight line in the square root of the depth on the stage)
    Us, info_s = Wd.under(off=ALL_LIGHTS, smooth=True)
    Ut, info_t = Wd.under(off=ALL_LIGHTS)
    smooth_rows, tex_rows = class_rows(grade(Us), info_s, rows), class_rows(grade(Ut), info_t, rows)
    u = np.sqrt((rows + 0.5 - HZ) / (K.H - HZ))
    D, Xm = drive_mean(strip_means(folder), haze, haze_far)
    ratio, texture = {}, {}
    for cls in ("road", "sand", "plain"):
        Ts, ns = smooth_rows[cls]
        Tt, nt = tex_rows[cls]
        ok = (ns > 0) & (nt > 0)
        k = np.ones((len(rows), 3), F32)
        for c in range(3):
            q = Tt[ok, c] / np.maximum(Ts[ok, c], 1e-3)
            A = np.stack([np.ones(ok.sum()), u[ok]], 1) * np.sqrt(nt[ok])[:, None]
            coef, *_ = np.linalg.lstsq(A, q * np.sqrt(nt[ok]), rcond=None)
            k[:, c] = coef[0] + coef[1] * u
        texture[cls] = k
        T = np.where(ns[:, None] > 0, Ts * k, np.nan)
        T = _smooth_rows(T, ns, 0)
        if cls == "sand":                                                 # (the drive's sand, on average: the shoulder's colour, hazed)
            zc = K.FOCAL * K.EYE / (rows + 0.5 - HZ)
            h = (1 - 0.5 ** (zc / haze_far))[:, None]
            Dv = _rgb(K.BASE["shoulder"]) * (1 - h) + _rgb(haze) * h
        else:
            Dv = np.full((len(rows), 3), np.nan, F32)
            for i, y in enumerate(rows):
                sel = np.abs(Xm[y]) < 2.9 if cls == "road" else np.abs(Xm[y]) > 6.5
                if sel.any():
                    Dv[i] = D[y][sel].mean(0)
            Dv = _smooth_rows(Dv, (~np.isnan(Dv[:, 0])).astype(F32), 0)
        ratio[cls] = np.clip(T / np.maximum(Dv, 1e-3), 0.2, 5.0)
    # each pixel's ratio: the road's on the asphalt; off it, the sand's and the plain's mixed as the drive's sand runs out
    # (its outer edge wanders from 2.95 to 5.65 m)
    A = np.abs(Xm[HZ + 1:])[..., None]
    f = 1 - np.clip((A - 2.95) / 2.7, 0, 1) ** 2 * (3 - 2 * np.clip((A - 2.95) / 2.7, 0, 1))
    off = ratio["sand"][:, None, :] * f + ratio["plain"][:, None, :] * (1 - f)
    r = np.where(A < 3.10, ratio["road"][:, None, :], off)
    target = np.zeros((K.H, K.W, 3), F32)
    target[HZ + 1:] = np.clip(D[HZ + 1:] * r, 0, 1)
    target = light_painting(target, light)                                # the painting's ground on average, lit as it is
    base = np.where(np.isnan(D), 0, D)
    Mf = np.where(target < base, target / np.maximum(base, 1e-4), 1.0)    # darker: multiply
    D2 = base * Mf
    Lf = np.where(target > D2, 1 - (1 - target) / np.maximum(1 - D2, 1.0 / 255), 0.0)     # lighter: screen
    below = (np.arange(K.H)[:, None] > HZ)[..., None]
    Mf = np.clip(np.where(below, Mf, 1.0), 0, 1)
    Lf = np.clip(np.where(below, Lf, 0.0), 0, 1)
    a = (1 - Mf).max(-1, keepdims=True)
    a[a < 0.5 / 255] = 0
    shade = np.concatenate([np.where(a > 0, 1 - (1 - Mf) / np.maximum(a, 1e-6), 1.0), a], -1)
    a = Lf.max(-1, keepdims=True)
    a[a < 0.5 / 255] = 0
    glow = np.concatenate([np.where(a > 0, Lf / np.maximum(a, 1e-6), 1.0), a], -1)
    return {"shade": shade.astype(F32), "glow": glow.astype(F32)}, dict(D=base, target=target, ratio=ratio, light=light, texture=texture)


def to8(rgba):
    return (np.clip(rgba, 0, 1) * 255 + 0.5).astype(np.uint8)


def lay(base, light, blend):
    """A light picture laid over an opaque picture as the canvas lays it: -> picture."""
    c, a = light[..., :3], light[..., 3:4]
    if blend == "screen":
        return 1 - (1 - base) * (1 - a * c)
    return base * (1 - a + a * c)

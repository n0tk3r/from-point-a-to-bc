"""The game's paints: a painted picture, kept as it is, mixed from the Post-Impressionists' paint box in its scene's key.
Used by postimp_key.py (which keys a scene's every picture file) at the game's strength, 50.

    paint(rgb, key, strength, seed) -> rgb

`rgb` is a float picture (h, w, 3), sRGB 0..1; `key` one of paints.KEYS; `strength` 0..100.
Strength 0 returns the picture untouched. Nothing here moves a pixel: every change is to a pixel's own colour, worked
out from the pixel and its neighbourhood, so every shape, edge and detail of today's picture stays where it is.

Two parts, both in OKLab (lightness kept, so today's light, depth and detail are kept):

1. THE KEY (colour). The picture is read for light and shadow: cast shadows (regions much darker than the lit
   surfaces round them), today's own cool shadows (a quiet lilac or blue-grey a little darker than its surroundings),
   and dark values. A shadow moves toward its hue family's shadow paints at that lightness (warm ground and stone:
   lilac, cobalt violet, deep violet in the darkest; greens: viridian; blues: ultramarine), so shadows become a colour
   instead of grey or brown. A thing that is simply dark in its own colour (bronze, wood, a red wall) goes toward its
   own darker paint (burnt sienna for the warm ones) and turns its hue only a little, so it stays itself. A lit warm or
   neutral surface moves toward the key's light (lead white and naples yellow in Rome; chrome yellow in Egypt's sun;
   lamplight at night), and where light turns into shadow it passes through orange. Then every colour moves part way
   toward its nearest paints in the box (weighted toward the key's own paints; the paints set the hue, the chroma
   rises only a little), and paint being purer than a print, the middle tones gain a little chroma. There is no black:
   the darkest darks lean to prussian blue and deep violet.
   The key is worked out on a calm copy of the picture (today's grain smoothed away, edges kept) and the change it
   makes there is added to today's own pixels, so today's grain and detail ride through untouched.

2. THE TOUCH (handling). The picture's own structure (a structure tensor of its lightness) gives at every pixel the
   way its forms run; where the picture is flat the marks lie nearly level. Sparse marks are laid that way. Each is a
   little lighter or darker and a little warmer or cooler along the key's complementary pair (lighter with warmer),
   and under it part of today's grain gives way to the smoother film of the paint (the calm copy: same colour and
   shading, no edge crossed). Between the marks today's surface stays as it is. Fine detail is protected.
"""

import math

import cv2
import numpy as np

from postimp_oklab import F32, chroma, gamut, lab_to_rgb, rgb_to_lab
from postimp_paints import PAINTS, SCENE_PAINTS, paint_at, ramp_at


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return (t * t * (3 - 2 * t)).astype(F32)


def gblur(a, s):
    return cv2.GaussianBlur(a, (0, 0), s, borderType=cv2.BORDER_REFLECT) if s > 0 else a


# ------------------------------------------------------------------ reading the picture
def light_maps(lab, key):
    """How the picture is lit, as maps 0..1:
      cast   a region much darker than the lit surfaces round it (read at a coarse scale too, so a thin dark thing in
             the sun is not one): a cast shadow, or the shadow side of a big form
      cool   today's own cool shadows: a quiet lilac or blue-grey a little darker than the light round it
      dark   a dark value
      shade  all of these together
      lit    a lit, light surface
      turn   the band where light turns into shadow (lit, with shadow close by)"""
    L = lab[..., 0]
    Ls = gblur(L, 1.2)                                                     # (today's grain is not light or shadow)
    Lc = gblur(L, 2.2)
    env = cv2.dilate(np.minimum(Ls, key.get("env_cap", 1.0)), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)))
    env = np.maximum(gblur(env, 10.0), np.minimum(Ls, key.get("env_cap", 1.0)))   # the lit level round each pixel (a lamp or a
    rel_c = np.minimum(Lc / np.maximum(env, 1e-3), 1.0)                          # lit doorway is a light, not a lit surface)
    rel_f = np.minimum(Ls / np.maximum(env, 1e-3), 1.0)
    C = np.hypot(lab[..., 1], lab[..., 2])
    grey = 1 - smoothstep(0.03, 0.10, C)
    cast = smoothstep(0.87, 0.70, rel_c) * smoothstep(0.90, 0.75, rel_f) * smoothstep(0.40, 0.60, env)
    cast = cast * key.get("cast", 1.0) * (0.45 + 0.55 * grey)
    dark = smoothstep(key["shade_hi"], key["shade_lo"], Ls)
    h = np.degrees(np.arctan2(lab[..., 2], lab[..., 1]))
    coolness = np.clip(np.cos(np.radians(np.clip(((h + 55 + 180) % 360 - 180) / 70, -1, 1) * 90)), 0, 1)
    cool = coolness * smoothstep(0.010, 0.025, C) * (1 - smoothstep(0.06, 0.09, C)) * smoothstep(0.97, 0.86, rel_f) * key.get("cool", 1.0)
    shade = gblur(np.clip(np.maximum(np.maximum(dark, cast), cool), 0, 1), 0.8)
    lit = smoothstep(key.get("lit_lo", 0.55), key.get("lit_hi", 0.80), Ls) * smoothstep(0.80, 0.95, rel_f) * (1 - shade)
    near = gblur(np.maximum(cast, cool), 2.5)
    turn = smoothstep(0.08, 0.45, near) * (1 - shade) * smoothstep(0.45, 0.70, Ls)
    return {k: gblur(v, 0.6).astype(F32) for k, v in dict(cast=cast, cool=cool, dark=dark, shade=shade, lit=lit, turn=turn).items()}


def families(lab):
    """Soft membership of each pixel in four hue families (warm/neutral, red, green, blue; violet counts as warm, whose
    shadow is violet). Greys belong to warm/neutral."""
    h = np.degrees(np.arctan2(lab[..., 2], lab[..., 1]))
    C = chroma(lab)

    def bump(center, half):
        d = (h - center + 180) % 360 - 180
        return np.clip(np.cos(np.clip(d / half, -1, 1) * math.pi / 2), 0, 1) ** 2

    warm = bump(75, 62) + bump(-40, 42)
    red = bump(22, 34)
    green = bump(158, 52)
    blue = bump(-112, 62)
    tot = warm + red + green + blue + 1e-6
    gate = smoothstep(0.012, 0.05, C)                                      # a grey has no family: it is neutral
    fam = {k: (v / tot) * gate for k, v in (("warm", warm), ("red", red), ("green", green), ("blue", blue))}
    fam["warm"] = fam["warm"] + (1 - gate)
    return fam


def toward(a, b, ta, tb, w, cap, own=(0.025, 0.075)):
    """Move (a, b) toward (ta, tb) by weight w. A grey moves freely (it only gains the target's colour); a coloured
    pixel's hue turns by at most `cap` radians, so a thing keeps its own colour and only leans toward the target.
    `own`: the chroma from which a colour counts as a thing's own (fully from the second number)."""
    ca, cb = a + w * (ta - a), b + w * (tb - b)                           # the plain move
    C = np.hypot(a, b)
    h0 = np.arctan2(b, a)
    h1 = np.arctan2(cb, ca)
    dh = (h1 - h0 + math.pi) % (2 * math.pi) - math.pi
    dh = np.clip(dh, -cap, cap)
    C1 = np.hypot(ca, cb)
    pa, pb = C1 * np.cos(h0 + dh), C1 * np.sin(h0 + dh)                  # the same move with the turn held back
    k = smoothstep(own[0], own[1], C)
    return ca + k * (pa - ca), cb + k * (pb - cb)


# ------------------------------------------------------------------ 1. the key
def key_colour(lab, key, s, lm, fam=None, sky=None):
    """Move each pixel's hue and chroma toward the key's paints. s = strength 0..1; lm = light_maps(). Lightness is
    kept (save the darkest darks, lifted a little toward prussian blue). `sky`: an optional mask of open sky."""
    L = lab[..., 0]
    a = lab[..., 1].copy()
    b = lab[..., 2].copy()
    C0 = chroma(lab)
    if fam is None:
        fam = families(lab)
    grey = 1 - smoothstep(0.03, 0.10, C0)

    # shadow. A shadow laid on something (cast, or today's own cool shadow) takes its family's shadow paints; a thing
    # that is only dark in its own colour takes them if it is greyish, and its own darker paint if it is coloured.
    laid = np.maximum(lm["cast"], lm["cool"])
    own = lm["dark"] * (1 - laid)
    sa = np.zeros_like(L)
    sb = np.zeros_like(L)
    for f, wt in fam.items():
        ta, tb = ramp_at(key["shadow"][f], L)
        if f == "warm":
            da, db = ramp_at(key["shadow"]["red"], L)                       # bronze, wood, a warm wall: burnt sienna
            q = own / np.maximum(own + laid, 1e-4) * (1 - grey)
            ta, tb = ta + q * (da - ta), tb + q * (db - tb)
        sa += wt * ta
        sb += wt * tb
    shade = lm["shade"]
    # a shadow laid on coloured ground (sand, stone) takes the shadow colour even so; a coloured thing's own dark less
    prot = (laid * (0.70 + 0.30 * grey) + own * (0.35 + 0.65 * grey)) / np.maximum(laid + own, 1e-4)
    w_sh = s * key["shade"] * shade * prot
    if sky is not None:
        w_sh = w_sh * (1 - 0.7 * sky)
    cap = math.radians(key.get("turn", 60)) * s * (laid + 0.5 * own) / np.maximum(laid + own, 1e-4)
    a, b = toward(a, b, sa, sb, w_sh, cap=cap)

    # light: warm, neutral and red surfaces toward the key's light; greens toward the light greens; blues toward the sky
    la_w, lb_w = ramp_at(key["light"], L)
    la_g, lb_g = ramp_at(["veronese-green", "emerald-green", "viridian"], L)
    la_b, lb_b = ramp_at(key["sky"], L)
    fw = fam["warm"] + fam["red"]
    la = fw * la_w + fam["green"] * la_g + fam["blue"] * la_b
    lb = fw * lb_w + fam["green"] * lb_g + fam["blue"] * lb_b
    lc = key.get("light_chroma", 0.5)                                      # how far a coloured lit surface goes too
    grey_l = 1 - smoothstep(0.015, 0.05, C0)                               # (a pale wall's own blue or green counts here)
    w_li = s * key["warm_light"] * lm["lit"] * (lc + (1 - lc) * grey_l) * (0.45 + 0.55 * fw)
    if sky is not None:
        w_li = w_li * (1 - sky) + s * key.get("sky_pull", 0.25) * sky
    Cb = np.hypot(a, b)
    a, b = toward(a, b, la, lb, w_li, cap=math.radians(35) * s, own=(0.010, 0.035))
    Cn = np.hypot(a, b)                                                    # the light warms; it does not repaint a pale wall
    lim = Cb + s * key.get("light_add", 0.04)
    f = np.where(Cn > lim, lim / np.maximum(Cn, 1e-6), 1.0)
    a, b = a * f, b * f

    # where light turns into shadow, it goes through orange
    oa, ob = paint_at(key.get("turn_paint", "chrome-orange"), L)
    w_tu = s * key.get("turn_orange", 0.18) * lm["turn"] * fw
    a, b = toward(a, b, oa, ob, w_tu, cap=math.radians(30) * s)

    # the paint box: a soft pull toward the nearest paints at this lightness (the key's own paints count more)
    num_a = np.zeros_like(L)
    num_b = np.zeros_like(L)
    den = np.zeros_like(L)
    sig2 = 2 * 0.032 ** 2
    for name in SCENE_PAINTS:
        pa, pb = paint_at(name, L)
        Lp = PAINTS[name]["lab"][0]
        d2 = (a - pa) ** 2 + (b - pb) ** 2 + (0.16 * (L - Lp)) ** 2
        w = key["weight"].get(name, 0.8) * np.exp(-d2 / sig2)
        num_a += w * pa
        num_b += w * pb
        den += w
    self_w = 0.12                                                          # far from every paint: stay where it is
    ta = (num_a + self_w * a) / (den + self_w)
    tb = (num_b + self_w * b) / (den + self_w)
    # the paints set the hue; the chroma may rise only a little here (the box's paints are purer than the middle wants)
    Cs, Ct = np.hypot(a, b), np.hypot(ta, tb)
    Cl = np.clip(Ct, 0.85 * Cs, (1 + 0.35 * s) * Cs + 0.010)
    ta, tb = ta * Cl / np.maximum(Ct, 1e-6), tb * Cl / np.maximum(Ct, 1e-6)
    k = s * key["snap"] * smoothstep(0.008, 0.03, Cs)
    a, b = toward(a, b, ta, tb, k, cap=math.radians(25) * s)

    # purer paint: a little more chroma in the middle tones and shadows, least where it is strong already
    C1 = np.hypot(a, b)
    gain = 1 + s * key["chroma"] * (1 - smoothstep(0.08, 0.16, C1)) * smoothstep(0.01, 0.04, C1) * (1 - 0.6 * smoothstep(0.70, 0.92, L))
    a = a * gain
    b = b * gain

    # no black: the darkest darks lean to prussian blue / deep violet, a little lifted
    dk = smoothstep(0.30, 0.08, L)
    pa, pb = paint_at("prussian-blue", L)
    va, vb = paint_at("deep-violet", L)
    kd = s * 0.45 * dk * grey
    a = a + kd * (0.5 * (pa + va) - a)
    b = b + kd * (0.5 * (pb + vb) - b)
    L2 = L + s * key["lift"] * dk * np.clip(0.30 - L, 0, None)
    return np.dstack([L2, a, b]).astype(F32)


# ------------------------------------------------------------------ 2. the touch
def flow(L, default_angle=None, rho=3.5, rho_coarse=12.0, rho_wide=36.0, seed=7):
    """The way the forms run at each pixel: (u, v) unit vectors along the edges (perpendicular to the gradient), and
    how sure we are (coherence 0..1). Where the picture is flat, a gentle, nearly level default decides (today's faint
    mottling does not steer the marks)."""
    h, w = L.shape
    Lb = gblur(L, 1.4)
    gx = cv2.Sobel(Lb, cv2.CV_32F, 1, 0, ksize=3) / 8
    gy = cv2.Sobel(Lb, cv2.CV_32F, 0, 1, ksize=3) / 8
    J = [gx * gx, gx * gy, gy * gy]
    fine = [gblur(j, rho) for j in J]
    coarse = [gblur(j, rho_coarse) for j in J]
    wide = [gblur(j, rho_wide) for j in J]
    if default_angle is None:
        rng = np.random.default_rng(seed)
        wav = gblur(rng.normal(0, 1, (h, w)).astype(F32), 45)
        wav = wav / (np.abs(wav).max() + 1e-6)
        default_angle = (0.25 * wav).astype(F32)                           # nearly level, wandering a little
    gang = default_angle + math.pi / 2                                     # a default stroke at angle t has its gradient at t + 90
    eps = 1.2e-4                                                           # about half today's typical structure
    Jd = [eps * np.cos(gang) ** 2, eps * np.cos(gang) * np.sin(gang), eps * np.sin(gang) ** 2]
    Jxx, Jxy, Jyy = [f + 0.3 * c + 1.5 * wd + d for f, c, wd, d in zip(fine, coarse, wide, Jd)]
    theta = 0.5 * np.arctan2(2 * Jxy, Jxx - Jyy) + math.pi / 2            # along the edge
    tr = Jxx + Jyy
    det = np.sqrt((Jxx - Jyy) ** 2 + 4 * Jxy ** 2)
    coh = (det / (tr + 1e-9)) ** 2
    return np.cos(theta).astype(F32), np.sin(theta).astype(F32), coh.astype(F32)


def lic(img, u, v, n, sigma=None, box=False):
    """Line-integral convolution: average `img` along the flow (u, v), n one-pixel steps each way, Gaussian-weighted
    (or evenly, `box`)."""
    if n <= 0:
        return img.copy()
    h, w = u.shape
    sigma = sigma or max(1.0, n / 2.0)
    X, Y = np.meshgrid(np.arange(w, dtype=F32), np.arange(h, dtype=F32))
    src = img.astype(F32)
    acc = src.copy()
    wsum = np.ones((h, w), F32)
    multi = img.ndim == 3
    for sign in (1.0, -1.0):
        px, py = X.copy(), Y.copy()
        du, dv = u * sign, v * sign
        for k in range(1, n + 1):
            px = px + du
            py = py + dv
            ix = np.clip(np.rint(px), 0, w - 1).astype(np.int32)
            iy = np.clip(np.rint(py), 0, h - 1).astype(np.int32)
            nu, nv = u[iy, ix], v[iy, ix]
            flip = np.where(nu * du + nv * dv < 0, -1.0, 1.0).astype(F32)
            du, dv = nu * flip, nv * flip
            wk = 1.0 if box else math.exp(-k * k / (2 * sigma * sigma))
            smp = cv2.remap(src, px, py, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            acc += wk * smp
            wsum += wk
    return acc / (wsum[..., None] if multi else wsum)


def strokes(u, v, seed, length=5, width=0.9, density=0.03):
    """Brush marks laid along the flow: sparse dabs, each with a value in -1..1, drawn out along (u, v) into marks
    about 2*length+1 pixels long and a couple of pixels wide. Returns (value, coverage): each mark keeps its own value
    where it lies (where marks cross, the one laid more thickly shows), and coverage is how much paint is there (0..1)."""
    h, w = u.shape
    rng = np.random.default_rng(seed)
    n = int(h * w * density)
    ys = rng.integers(0, h, n)
    xs = rng.integers(0, w, n)
    dab = np.zeros((h, w), F32)
    cov = np.zeros((h, w), F32)
    dab[ys, xs] = rng.uniform(-1, 1, n).astype(F32)
    cov[ys, xs] = 1
    dab = gblur(dab, width)
    cov = gblur(cov, width)
    t = lic(dab, u, v, length, box=True)
    c = lic(cov, u, v, length, box=True)
    t = t / np.maximum(c, 1e-5)
    peak = 1.0 / (2 * math.pi * width * width) / (2 * length + 1)        # one mark's coverage along its middle
    cover = np.clip(c / peak, 0, 1)
    return t.astype(F32), cover.astype(F32)


def detail_mask(L):
    """Fine detail (lettering, wires, small bright things): 1 where the marks must keep off."""
    m1 = gblur(L, 0.8)
    m3 = gblur(L, 2.5)
    hp = np.abs(m1 - m3)
    return smoothstep(0.035, 0.085, gblur(hp, 0.8))


def touch(lab, lab_calm, lab_today, key, s, seed, u, v, coh, protect=None):
    """The handling. Sparse marks are laid along the forms over today's surface. Each mark is a little lighter or
    darker and a little warmer or cooler along the key's pair (lighter goes with warmer, as sun on a stroke does), and
    under a mark part of today's grain gives way to the smoother paint of the mark (the calm copy: same colour, same
    shading, no edge crossed). Between the marks today's surface stays as it is. s = strength 0..1.
    `lab` is today's picture in the key, `lab_calm` the calm copy in the key."""
    if s <= 0:
        return lab
    Lt = lab_today[..., 0]
    det = detail_mask(Lt)
    if protect is not None:
        det = np.maximum(det, protect)
    near = gblur(cv2.dilate(det, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))), 1.0)
    calm = (1 - det) * (1 - 0.5 * near)                                    # small things keep crisp: calmer marks round them too
    ln = int(round(key.get("mark_len", 3) + 2 * s))
    t1, c1 = strokes(u, v, seed + 11, length=ln, width=0.8, density=key.get("density", 0.012))
    t2, _ = strokes(u, v, seed + 23, length=ln, width=1.0, density=0.03)
    on = smoothstep(0.30, 0.70, c1) * calm                                 # where a mark lies
    warm = PAINTS[key["pair"][0]]["lab"]
    cool = PAINTS[key["pair"][1]]["lab"]
    axis = warm[1:] - cool[1:]
    axis = axis / (np.linalg.norm(axis) + 1e-9)
    out = lab + (key.get("film", 0.45) * s * on)[..., None] * (lab_calm - lab)     # the mark's smoother paint film
    out[..., 0] += s * key.get("stroke_value", 0.045) * t1 * on * (0.35 + 0.65 * smoothstep(0.12, 0.40, Lt))
    amp = s * key.get("stroke_colour", 0.03) * (0.5 + 0.5 * smoothstep(0.15, 0.5, Lt)) * on
    tc = 0.65 * t1 + 0.35 * t2
    out[..., 1] += amp * tc * axis[0]
    out[..., 2] += amp * tc * axis[1]
    return out


# ------------------------------------------------------------------ the whole
def calm_copy(lab):
    """Today's picture with its grain smoothed and its edges kept (two light bilateral passes)."""
    out = lab.astype(F32)
    for _ in range(2):
        out = cv2.bilateralFilter(out, 7, 0.05, 2.5)
    return out


def read_maps(lab0, key):
    """Everything paint() reads from today's picture before it changes anything."""
    lab_s = calm_copy(lab0)
    lm = light_maps(lab_s, key)
    fam = families(lab_s)
    u, v, coh = flow(lab0[..., 0])
    return {"calm": lab_s, "light": lm, "fam": fam, "u": u, "v": v, "coh": coh}


def paint(rgb, key, strength, seed=1, protect=None, sky=None, maps=None, lab0=None):
    """Today's picture (rgb float) -> the middle ground at `strength` (0..100). `maps`: read_maps() of the picture as
    composed (so the cut-outs and the back read the same light), else read from `rgb` itself."""
    s = float(strength) / 100.0
    if s <= 0:
        return rgb.copy()
    if lab0 is None:
        lab0 = rgb_to_lab(rgb)
    if maps is None:
        maps = read_maps(lab0, key)
    lab_s = maps["calm"]
    # The key is worked out on the calm copy and the change it makes there is added to today's own pixels: the grain
    # rides through as it is, and a region's colour moves as one, instead of neighbouring grains being pulled apart.
    shift = key_colour(lab_s, key, s, maps["light"], maps["fam"], sky) - lab_s
    st = s ** 0.75                                                         # the handling shows a little sooner than the colour
    lab = touch(lab0 + shift, lab_s + shift, lab0, key, st, seed, maps["u"], maps["v"], maps["coh"], protect)
    return lab_to_rgb(gamut(lab))


# ------------------------------------------------------------------ colours without a picture round them
def point_maps(lab, key, lit=None, laid=None):
    """Light maps for colours that have no picture round them (a sprite's palette, a person's ramp, a smoke colour):
    read from each colour alone. `lit` and `laid` (arrays or numbers) override the reading, as a person's ramp says
    which tone is in light and which in shade."""
    L = lab[..., 0]
    C = np.hypot(lab[..., 1], lab[..., 2])
    h = np.degrees(np.arctan2(lab[..., 2], lab[..., 1]))
    coolness = np.clip(np.cos(np.radians(np.clip(((h + 55 + 180) % 360 - 180) / 70, -1, 1) * 90)), 0, 1)
    cool = coolness * smoothstep(0.010, 0.025, C) * (1 - smoothstep(0.06, 0.09, C)) * smoothstep(0.80, 0.55, L)
    dark = smoothstep(key["shade_hi"], key["shade_lo"], L)
    cast = np.zeros_like(L) if laid is None else np.broadcast_to(np.asarray(laid, F32), L.shape).astype(F32)
    shade = np.clip(np.maximum(np.maximum(dark, cast), cool), 0, 1)
    if lit is None:
        lit = smoothstep(key.get("lit_lo", 0.55), key.get("lit_hi", 0.80), L) * (1 - shade)
    else:
        lit = np.broadcast_to(np.asarray(lit, F32), L.shape).astype(F32) * (1 - shade)
    return dict(cast=cast.astype(F32), cool=cool.astype(F32), dark=dark.astype(F32), shade=shade.astype(F32),
                lit=np.asarray(lit, F32), turn=np.zeros_like(L))


def key_points(rgb, key, strength, lit=None, laid=None):
    """The key for colours alone (rgb float, any shape (..., 3)): no handling, no neighbourhood."""
    s = float(strength) / 100.0
    if s <= 0:
        return np.asarray(rgb, F32).copy()
    rgb = np.asarray(rgb, F32)
    shape = rgb.shape
    lab = rgb_to_lab(rgb.reshape(-1, 1, 3))
    lm = point_maps(lab, key, None if lit is None else np.asarray(lit, F32).reshape(-1, 1),
                    None if laid is None else np.asarray(laid, F32).reshape(-1, 1))
    out = key_colour(lab, key, s, lm, families(lab))
    return lab_to_rgb(gamut(out)).reshape(shape)

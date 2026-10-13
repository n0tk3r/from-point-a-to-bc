"""Inside the men in gray's limousine (nevada-limo), driving across the desert. Act Five opens here.

    python3 nevada_limo.py          everything: backdrop, cut-outs and their states, layout.json, the comps (a few minutes)
    python3 nevada_limo.py fast     the under-painting only, one ray per pixel, hard shadows: for composing (20 s)
    python3 nevada_limo.py paint    the same with the brush pass over it: for judging the look

ONE CAMERA. The car is measured in centimetres (nevada_limo_model.py) and every pixel of the picture is a ray from the
game's own camera for this scene (room.View: horizon 220, full 355; the lens at 148 cm, a seated eye and a little
above). What the ray meets, and how the light falls there, is worked out in the car (nevada_limo_kit.py). So the
seats' pleats, the window frames, the headliner's rolls and the carpet all run to the one vanishing point, and the
game's people sit in it at the right size: Grandpa Joe on the long seat near the divider at about 0.79, Ranger on the
carpet near us at about 0.99.

THE VIEW. We sit on the back seat and look down the length of the car at the divider. The long seat runs along the
left wall (Grandpa Joe sits at its far end, by the divider; his ropes lie on the cushion beside him, a spare seatbelt's
buckle beyond them); the facing seat along the right (the paper bag, the juice box and the clipboard on it, the little
fridge in its base at the near end). At the far end a low bar under the divider: the car phone on its cradle, the
ashtray full of jelly beans. Long low windows on both sides, smoked; the headliner overhead with a row of small lights.
Our own seat's cushion and its armrests are the foreground.

LIGHT (keep to it):
  - daylight through the smoked windows from both sides: cool, soft (each pane a broad light outside the glass); the
    left windows light the facing seat and the carpet's right side, the right windows the long seat and Joe;
  - the ceiling's small lights: warm, small, a little glow round each on the headliner;
  - the divider dim: smoked glass, darker than anything but the near corners;
  - what the light does not reach is blue-violet; the near corners (our seat, the armrests) hold the deepest darks.

THREE TONES. Dark: the headliner's near part, the near corners, our seat, the partition. Middle: the seats, the carpet.
Light: the windows (where the desert goes by), the lit tops of the seat cushions, the things on the facing seat, the
ceiling's lights.

THE WINDOWS. The glass is painted a plain pale desert-sky grey: the game draws the desert strip (nevada_limo_strip.py)
behind it, clipped to each pane's exact polygon (layout.json `windows`); the frames, the pillars and the seals are in
the backdrop and are never covered. After every pass, each pane's pixels (a pixel is the glass when its middle is in
the polygon, as the engine decides) are set to the glass and a dark seal is restated just outside, so the two agree.

CUT-OUTS (pixel-aligned, the backdrop complete under each): divider-up, divider-down; ropes-4 .. ropes-1 (the bow
coming undone); bag, juice, clipboard (each goes when taken, with its own shadow, so the seat under it is clean);
front (our seat and the armrests, front plane)."""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, blur, lerp, noise, sample, strokes, grain, to_palette, save, rgb
from room import View
import nevada_limo_model as M
import nevada_limo_things as T
from nevada_limo_kit import Stage, Lamp, shade, col, floor_contact, LUM

W, H = 800, 600
V = View(**M.VIEW)
OUT = "out/nevada-limo"
WORK = "out/nevada-limo-work"
SEED = 31
COOL_BELOW = 0.55            # light weaker than this begins to turn blue-violet
EXPOSE = 0.92
THINGS = ("bag", "juice", "clipboard")


# ---------------------------------------------------------------- the light
SKY, HORIZON, GROUND = "#b8cbec", "#dcdcdc", "#ecc8a2"        # what comes in through smoked glass: the sky, the far desert, the sunlit ground


def lamps(fast=False):
    """Daylight through each pane. A window is a broad light, so each pane has three, twice along its length: the sky
    high outside (cool, falling in and down onto the far side's seat and the carpet), the far desert level with the glass
    (it lights the backrests across the car), and the sunlit ground right outside (warm, low: it lights the headliner
    and the undersides from below). Then the ceiling's five small warm lights."""
    out = []
    n = 1 if fast else 3
    for side, sgn in (("L", -1.0), ("R", 1.0)):
        x0 = 0.0 if side == "L" else M.W
        for (z0, z1) in M.PANES[side]:
            for t in (0.3, 0.7):
                z = z0 + (z1 - z0) * t
                out.append(Lamp((x0 + sgn * 240.0, 330.0, z), SKY, 0.36, reach=560.0, size=50.0, samples=n, wrap=0.3))
                out.append(Lamp((x0 + sgn * 240.0, 205.0, z), HORIZON, 0.24, reach=560.0, size=50.0, samples=n, wrap=0.3))
                out.append(Lamp((x0 + sgn * 200.0, 34.0, z), GROUND, 0.17, reach=520.0, size=50.0, samples=n, wrap=0.3))
    for (lx, lz) in M.LIGHTS:
        out.append(Lamp((lx, M.H - 3.0, lz), "#ffbe72", 0.10, reach=55.0, size=2.0, shadows=False, wrap=0.6))
    return out


def ambient(X, Y, Z, N):
    """The light that is simply in a car with smoked windows: cool, from both sides and from above; less down low,
    under the seats and in the near corners."""
    up = 0.5 + 0.5 * N[..., 1]
    side = np.abs(N[..., 0])
    low = np.clip(Y / 90.0, 0, 1)
    a = col("#5c6a94")[None, None, :] * ((0.15 + 0.07 * up + 0.05 * side) * (0.62 + 0.38 * low))[..., None]
    toward = np.clip(N[..., 2], 0, 1)                                    # what faces us gets a little of the light behind us (the back window)
    a = a + col("#8a7c88")[None, None, :] * (toward * 0.05)[..., None]
    return a


# ---------------------------------------------------------------- putting the car together
def render(ss=1, fast=True, skip=(), rect=None, occ=None, **state):
    """-> (picture, stage). The picture is at picture size (rays averaged)."""
    st = Stage(V, ss=ss, rect=rect)
    st.skip = set(skip)
    T.build(st, **state)
    pic, light = shade(st, lamps(fast), ambient, fast=fast, occ=occ, expose=EXPOSE)
    X, Y, Z = st.places()
    glass = (st.flag & 4) > 0
    # shadows are cool: where little light falls, the colour leans to blue-violet (a painter's shadows, not a camera's)
    lum = light @ LUM
    deep = np.clip(1 - lum / COOL_BELOW, 0, 1) ** 1.2
    pic = np.where(glass[..., None], pic, pic * (1 + deep[..., None] * np.array([-0.10, -0.03, 0.20], dtype=F32)[None, None, :]))
    # things sit on the carpet: a dark line round every foot; and the carpet darkens toward the seats' feet
    carpet = st.mask_of("carpet")
    dark = floor_contact(st, X, Z, list(st.feet.values()), reach=10.0, amount=0.5) * carpet
    under = np.clip(1 - np.minimum(X - M.SEAT_D, M.W - M.SEAT_D - X) / 22.0, 0, 1) * carpet
    dark = dark + under * 0.16
    pic = pic * (1 - np.clip(dark, 0, 0.8))[..., None]
    # depth by tone: the far end a little cooler and closer in value, as through the car's air
    t = np.minimum(st.t, 3000.0)
    air = np.clip((t - 300) / 500.0, 0, 1) * 0.10 * (~glass)
    pic = pic * (1 - air[..., None]) + col("#4a5478")[None, None, :] * air[..., None]
    # the foreground is darker and warmer than the middle of the car (Ranger passes behind it)
    fr = st.grp == st.groups.get("front", -1)
    pic[fr] = pic[fr] * col("#8a7e82")
    return st.down(pic), st


_Y, _X = np.mgrid[0:H, 0:W].astype(F32)
_DX = (noise((H, W), 30, SEED + 3, 3) - 0.5) * 2 * 0.7
_DY = (noise((H, W), 30, SEED + 4, 3) - 0.5) * 2 * 0.7


def wob(a, rect=None):
    """Nothing a hand rules is perfectly straight: every picture and mask is pushed about by the same slow field,
    under a pixel, so all the cut-outs still fit one another exactly. (With `rect`, for a patch of the picture.)"""
    if rect is None:
        return sample(a, _X + _DX, _Y + _DY)
    x0, y0, x1, y1 = rect
    return sample(a, _X[y0:y1, x0:x1] - x0 + _DX[y0:y1, x0:x1], _Y[y0:y1, x0:x1] - y0 + _DY[y0:y1, x0:x1])


def wob_near(a):
    yy = np.clip(np.round(_Y + _DY), 0, H - 1).astype(np.intp)
    xx = np.clip(np.round(_X + _DX), 0, W - 1).astype(np.intp)
    return a[yy, xx]


def grade(pic, rect=None):
    """The whole picture's last adjustments: the near corners deeper and warmer, the top (the headliner near us) deeper,
    to hold the eye on the far end where everything happens."""
    x0, y0, x1, y1 = rect or (0, 0, W, H)
    y, x = np.mgrid[y0:y1, x0:x1].astype(F32)
    cx = ((x - 420) / 420) ** 2
    low = np.clip((y - 470) / 130, 0, 1) ** 1.3
    top = np.clip((170 - y) / 170, 0, 1) ** 1.1
    v = np.clip(cx * 0.28 * (0.4 + 0.6 * low) + low * 0.26 + top * (0.30 + 0.25 * cx), 0, 0.70)
    warm = col("#4a2a2a")
    out = pic * (1 - v[..., None]) + pic * warm[None, None, :] * 1.5 * v[..., None]
    grey = (out @ LUM)[..., None]
    out = grey + (out - grey) * 1.10
    return np.clip(out, 0, 1)


def paint(crisp, seed=2):
    """The brush pass, and then the built things said again crisply over it: where the under-painting has an edge or
    a small thing, most of it comes back; where it is only a broad tone, the brushwork stays."""
    b = strokes(crisp, sizes=(9, 5, 2), seed=seed, density=1.5, jitter=0.04, keep=0.30)
    hf = np.abs(crisp - blur(crisp, 1.4)).sum(axis=2)
    w = np.clip(hf * 7.5 - 0.05, 0, 1)
    w = np.maximum(w, blur(w, 0.7))
    out = lerp(b, crisp, (0.14 + 0.84 * w)[..., None])
    return np.clip(out + 0.45 * (out - blur(out, 0.9)), 0, 1)


def maps_of(st, rect=None):
    return (wob(st.pick(np.minimum(st.t, 5000.0)), rect), wob(st.pick(st.N[..., 1]), rect), st.pick(st.oid), st.names.get("carpet", -1))


def details(pic, maps):
    """Small crisp accents found from what each pixel shows: the lit front edge of every top (a cushion's piping, the
    bar's lip), and a dark line where one thing stands in front of another far behind it."""
    t, ny, oid, floor_id = maps
    below_same = (np.roll(oid, -1, axis=0) == oid) & (np.roll(ny, -1, axis=0) < 0.5) & (ny > 0.9)
    below_same[-1] = False
    edge = below_same & (oid != floor_id)
    out = pic.copy()
    out[edge] = np.clip(out[edge] * 1.22 + 0.03, 0, 1)
    for ax, sh_ in ((0, 1), (0, -1), (1, 1), (1, -1)):
        tn = np.roll(t, sh_, axis=ax)
        behind = (t - tn > 14.0) & (t - tn > 0.03 * t)
        if ax == 0:
            behind[0 if sh_ == 1 else -1] = False
        else:
            behind[:, 0 if sh_ == 1 else -1] = False
        out[behind] = out[behind] * 0.72
    return out


def to_image(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def tones(a, label=""):
    lum = (np.clip(a, 0, 1) * 255) @ LUM
    print(label, "mean", (a.mean(axis=(0, 1)) * 255).round(0), "lum 5/25/50/75/95:", np.percentile(lum, [5, 25, 50, 75, 95]).round(0))


# ---------------------------------------------------------------- shapes in the picture
def inside_poly(poly, shape=(H, W)):
    """A pixel is inside when its middle is (as the engine decides for a window and for the ground): the even-odd
    rule, crossing by crossing."""
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]].astype(np.float64)
    px, py = xx + 0.5, yy + 0.5
    inside = np.zeros(shape, dtype=bool)
    pts = [(float(a), float(b)) for a, b in poly]
    for i in range(len(pts)):
        (x1, y1), (x2, y2) = pts[i], pts[i - 1]
        if y1 == y2:
            continue
        cond = (y1 > py) != (y2 > py)
        xc = (x2 - x1) * (py - y1) / (y2 - y1) + x1
        inside ^= cond & (px < xc)
    return inside


def clip_poly(poly, x0=0.0, y0=0.0, x1=float(W), y1=float(H)):
    """A polygon cut to the picture's edges (Sutherland-Hodgman)."""
    def cut(pts, inside, meet):
        out = []
        for i in range(len(pts)):
            p, q = pts[i], pts[(i + 1) % len(pts)]
            if inside(q):
                if not inside(p):
                    out.append(meet(p, q))
                out.append(q)
            elif inside(p):
                out.append(meet(p, q))
        return out
    pts = [tuple(p) for p in poly]
    for inside, meet in (
        (lambda p: p[0] >= x0, lambda p, q: (x0, p[1] + (q[1] - p[1]) * (x0 - p[0]) / (q[0] - p[0]))),
        (lambda p: p[0] <= x1, lambda p, q: (x1, p[1] + (q[1] - p[1]) * (x1 - p[0]) / (q[0] - p[0]))),
        (lambda p: p[1] >= y0, lambda p, q: (p[0] + (q[0] - p[0]) * (y0 - p[1]) / (q[1] - p[1]), y0)),
        (lambda p: p[1] <= y1, lambda p, q: (p[0] + (q[0] - p[0]) * (y1 - p[1]) / (q[1] - p[1]), y1))):
        pts = cut(pts, inside, meet)
        if not pts:
            break
    return pts


def panes():
    """Each window's glass in the picture: (id, side, polygon cut to the picture, its pixels)."""
    out = []
    y0, y1 = M.WINDOW_Y
    for side, X in (("L", 0.0), ("R", M.W)):
        for i, (z0, z1) in enumerate(M.PANES[side]):
            q = V.poly([(X, y0, z0), (X, y0, z1), (X, y1, z1), (X, y1, z0)])
            q = [(round(px, 1), round(py, 1)) for px, py in clip_poly(q)]
            out.append((f"window-{side.lower()}{'-far' if i == 0 else '-near'}", side, q, inside_poly(q)))
    return out


def restate_glass(pic, wins):
    """Each pane's pixels exactly the plain glass (a little lighter toward the top, as smoked glass against a bright
    sky is), and a dark seal of one or two pixels just outside it, so the strip the game draws behind the glass meets
    the frame painted round it exactly."""
    out = pic.copy()
    yy = _Y
    for _, side, q, m in wins:
        ys = yy[m]
        t = np.clip((ys - ys.min()) / max(1.0, ys.max() - ys.min()), 0, 1)
        out[m] = (col(T.PANE) * (1.02 - 0.05 * t[:, None])).astype(F32)
        ring = (blur(m.astype(F32), 0.8) > 0.02) & ~m
        out[ring] = out[ring] * 0.35 + col(T.TRIM) * 0.65
    return np.clip(out, 0, 1)


# ---------------------------------------------------------------- the divider's two views, painted in picture pixels
def opening():
    """The divider's opening in the picture: its four corners (top left, top right, bottom right, bottom left) on the
    glass, and its pixels (what the ray-caster saw of the glass: exactly the cut-outs' shape)."""
    x0, x1 = M.DIVIDER["x"]
    s0, t0 = M.DIVIDER["sill"], M.DIVIDER["top"]
    return [V.pt(x0, t0, -3.0), V.pt(x1, t0, -3.0), V.pt(x1, s0, -3.0), V.pt(x0, s0, -3.0)]


def quad_map(q):
    """(u, v) in 0..1 (across, down) -> a point in the quad."""
    (ax, ay), (bx, by), (cx, cy), (dx, dy) = q
    def f(u, v):
        tx, ty = ax + (bx - ax) * u, ay + (by - ay) * u
        lx, ly = dx + (cx - dx) * u, dy + (cy - dy) * u
        return tx + (lx - tx) * v, ty + (ly - ty) * v
    return f


def divider_view(which):
    """The picture in the opening, drawn at the picture's own pixels (the opening is nearly square to us): `up`, the
    smoked glass with the headrests dim through it, a broad sheen and our own window faintly in it; `down`, the front
    compartment: the windshield, the road ahead, two men in gray from behind with an earpiece's curl each, two pairs
    of black sunglasses in the rear-view mirror, one of them eating a doughnut. -> (RGB picture the size of the stage)."""
    from PIL import ImageDraw
    q = opening()
    F_ = quad_map(q)
    x0 = int(math.floor(min(p[0] for p in q))) - 2
    y0 = int(math.floor(min(p[1] for p in q))) - 2
    x1 = int(math.ceil(max(p[0] for p in q))) + 2
    y1 = int(math.ceil(max(p[1] for p in q))) + 2
    w, h = x1 - x0, y1 - y0
    k = 4                                                               # drawn 4x, then each pixel the mean of its 16
    im = Image.new("RGB", (w * k, h * k), (0, 0, 0))
    d = ImageDraw.Draw(im)
    P = lambda u, v: ((F_(u, v)[0] - x0) * k, (F_(u, v)[1] - y0) * k)
    box = lambda u0, v0, u1, v1: [P(u0, v0)[0], P(u0, v0)[1], P(u1, v1)[0], P(u1, v1)[1]]
    poly = lambda pts: [P(u, v) for u, v in pts]
    if which == "up":
        d.polygon(poly([(0, 0), (1, 0), (1, 1), (0, 1)]), fill=(34, 38, 48))
        for hu in (0.27, 0.73):                                         # the headrests and the shoulders of the men in front, dim
            d.rounded_rectangle(box(hu - 0.07, 0.42, hu + 0.07, 0.86), radius=5 * k, fill=(50, 55, 68))
            d.rounded_rectangle(box(hu - 0.12, 0.80, hu + 0.12, 1.05), radius=4 * k, fill=(46, 50, 62))
        d.polygon(poly([(0.40, 0.20), (0.60, 0.20), (0.62, 0.62), (0.38, 0.62)]), fill=(44, 50, 62))       # our own back window, faint
        a = np.asarray(im, F32) / 255.0
        a = blur(a, 2.0 * k)
        uu = np.linspace(0, 1, w * k, dtype=F32)[None, :, None]
        vv = np.linspace(0, 1, h * k, dtype=F32)[:, None, None]
        for c0, wd, amt in ((0.15, 0.09, 0.15), (0.28, 0.035, 0.10), (0.80, 0.06, 0.06)):
            u = (uu - c0) + (vv - 0.5) * 0.30
            a = a + np.clip(1 - np.abs(u) / wd, 0, 1) ** 1.6 * amt
        a = a * (1.06 - 0.12 * vv)
    else:
        sky = [(78, 128, 200), (98, 148, 210), (128, 172, 220), (170, 200, 228), (206, 220, 232)]
        hv = 0.50                                                       # the horizon, down the opening
        for i, c in enumerate(sky):
            d.polygon(poly([(0, hv * i / 5), (1, hv * i / 5), (1, hv * (i + 1) / 5), (0, hv * (i + 1) / 5)]), fill=c)
        for (mu, mw, mh, c) in ((0.10, 0.12, 0.05, (156, 128, 170)), (0.34, 0.08, 0.035, (170, 142, 180)), (0.66, 0.15, 0.06, (150, 124, 168)), (0.92, 0.09, 0.04, (164, 136, 176))):
            d.polygon(poly([(mu - mw / 2, hv), (mu - mw / 2 + 0.02, hv - mh), (mu + mw / 2 - 0.02, hv - mh), (mu + mw / 2, hv)]), fill=c)
        d.polygon(poly([(0, hv), (1, hv), (1, 1), (0, 1)]), fill=(224, 186, 136))
        d.polygon(poly([(0, hv + 0.03), (1, hv + 0.03), (1, hv + 0.07), (0, hv + 0.07)]), fill=(234, 202, 156))
        d.polygon(poly([(0.30, 1.0), (0.70, 1.0), (0.505, hv), (0.495, hv)]), fill=(104, 100, 120))     # the road ahead
        for i in range(4):
            va, vb = hv + (1 - hv) * (0.08 + 0.22 * i) ** 1.3, hv + (1 - hv) * (0.08 + 0.22 * i + 0.09) ** 1.3
            wa, wb = 0.002 + 0.010 * (va - hv) / (1 - hv), 0.002 + 0.010 * (vb - hv) / (1 - hv)
            d.polygon(poly([(0.5 - wa, va), (0.5 + wa, va), (0.5 + wb, vb), (0.5 - wb, vb)]), fill=(244, 214, 92))
        d.polygon(poly([(0, 0), (1, 0), (1, 0.07), (0, 0.07)]), fill=(38, 38, 46))                       # the roof's edge
        d.polygon(poly([(0, 0.80), (1, 0.80), (1, 1), (0, 1)]), fill=(42, 40, 48))                       # the dashboard
        d.polygon(poly([(0, 0.78), (1, 0.78), (1, 0.81), (0, 0.81)]), fill=(76, 74, 86))
        # the rear-view mirror on its stalk, two pairs of black sunglasses in it
        d.line([P(0.5, 0.07), P(0.5, 0.16)], fill=(30, 30, 36), width=2 * k)
        d.rounded_rectangle(box(0.405, 0.15, 0.595, 0.40), radius=3 * k, fill=(28, 28, 34))
        d.rounded_rectangle(box(0.415, 0.18, 0.585, 0.37), radius=2 * k, fill=(196, 206, 218))
        for fu in (0.455, 0.545):
            d.ellipse(box(fu - 0.032, 0.19, fu + 0.032, 0.37), fill=(228, 196, 168))                    # a face
            d.chord(box(fu - 0.034, 0.165, fu + 0.034, 0.28), 180, 360, fill=(70, 52, 42))              # its hair
            d.rounded_rectangle(box(fu - 0.028, 0.245, fu - 0.004, 0.30), radius=k, fill=(12, 12, 16))   # black glasses
            d.rounded_rectangle(box(fu + 0.004, 0.245, fu + 0.028, 0.30), radius=k, fill=(12, 12, 16))
            d.line([P(fu - 0.006, 0.255), P(fu + 0.006, 0.255)], fill=(12, 12, 16), width=k)
        # the two heads from behind, over the tops of the front seats
        for hu, big, hair in ((0.26, 1.0, (64, 46, 36)), (0.74, 1.06, (86, 64, 44))):
            r = 0.058 * big
            d.rounded_rectangle(box(hu - 0.13, 0.80, hu + 0.13, 1.05), radius=4 * k, fill=(120, 120, 132))      # gray shoulders
            d.polygon(poly([(hu - 0.025, 0.80), (hu + 0.025, 0.80), (hu + 0.018, 0.86), (hu - 0.018, 0.86)]), fill=(238, 238, 242))   # the white collar
            d.rectangle(box(hu - 0.022, 0.70, hu + 0.022, 0.81), fill=(222, 190, 164))                 # the neck
            d.ellipse(box(hu - r, 0.42, hu + r, 0.78), fill=(222, 190, 164))                           # the head
            d.ellipse(box(hu - r, 0.42, hu + r, 0.72), fill=hair)                                      # the back of it: neat hair
            for eu in (hu - r, hu + r):
                d.ellipse(box(eu - 0.009, 0.57, eu + 0.009, 0.67), fill=(212, 172, 146))               # ears
            eu = hu + (r + 0.006) * (1 if hu > 0.5 else -1)                                            # the earpiece: a clear curl, its wire
            d.arc(box(eu - 0.012, 0.53, eu + 0.012, 0.66), 0, 360, fill=(240, 244, 250), width=k)
            d.line([P(eu, 0.66), P(eu + (0.01 if hu > 0.5 else -0.01), 0.80)], fill=(240, 244, 250), width=k)
            d.line([P(hu - r * 0.6, 0.47), P(hu - r * 0.05, 0.445)], fill=tuple(min(255, c + 34) for c in hair), width=k)    # a combed line
        # the one on the right has a doughnut up beside his head: a bite out of it
        du, dv = 0.86, 0.50
        d.rectangle(box(0.815, 0.62, 0.86, 0.82), fill=(120, 120, 132))                              # his sleeve
        d.ellipse(box(0.81, 0.55, 0.85, 0.66), fill=(222, 190, 164))                                 # his hand
        d.ellipse(box(du - 0.045, dv - 0.11, du + 0.045, dv + 0.11), fill=(210, 146, 86))
        d.ellipse(box(du - 0.04, dv - 0.10, du + 0.04, dv + 0.04), fill=(244, 140, 172))             # pink icing on top
        d.ellipse(box(du - 0.013, dv - 0.03, du + 0.013, dv + 0.03), fill=(170, 200, 228))           # the hole (the sky through it)
        d.ellipse(box(du + 0.025, dv - 0.14, du + 0.065, dv - 0.02), fill=(176, 204, 228))           # the bite
        for (su, sv, c) in ((-0.02, -0.05, (250, 240, 120)), (0.01, -0.07, (120, 210, 240)), (-0.03, -0.01, (250, 250, 250))):
            d.point(P(du + su, dv + sv), fill=c)
        a = np.asarray(im, F32) / 255.0
    small = a.reshape(h, k, w, k, 3).mean(axis=(1, 3))
    out = np.zeros((H, W, 3), dtype=F32)
    out[y0:y1, x0:x1] = small
    return out


# ---------------------------------------------------------------- the clipboard's sheet, set in picture pixels
FONT35 = {"4": ["1.1", "1.1", "111", "..1", "..1"], "1": [".1.", "11.", ".1.", ".1.", "111"], "9": ["111", "1.1", "111", "..1", "11."],
          "2": ["11.", "..1", ".1.", "1..", "111"]}


def sheet_marks(pic, cover_mask):
    """The office's map on the clipboard, crisp, in picture pixels: the paper restated, a pen road, the fence, two
    mesas, three circled sectors (44 and 1921 written beside two of them, upright numerals stepping down the sheet's
    slope; the third under a thumb-sized smudge), a column of empty boxes, a squiggle of a margin note. Only pixels the
    clipboard covers are touched."""
    from PIL import ImageDraw
    o, a, u, n = T.clipboard_frame()
    w, h = M.CLIPBOARD["w"], M.CLIPBOARD["h"]
    C = lambda x, y: V.pt(*(o + a * (x - w / 2) + u * y + n * 0.3))
    # the sheet's own (U, V) in cm: U across from its left edge, V up from its foot
    S = lambda U, V_: C(1.2 + U, 1.2 + V_)
    sw, sh = w - 2.4, h - 4.0
    corners = [S(0, 0), S(sw, 0), S(sw, sh), S(0, sh)]
    paper_m = inside_poly(corners) & cover_mask
    out = pic.copy()
    if not paper_m.any():
        return out
    base = np.median(pic[paper_m], axis=0)
    base = np.maximum(base, col("#d8d4c8") * 0.92)
    yy = _Y[paper_m]
    t = (yy - yy.min()) / max(1.0, yy.max() - yy.min())
    out[paper_m] = base[None, :] * (1.04 - 0.10 * t[:, None])
    ink = (32, 38, 74)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pt = lambda U, V_: tuple(int(round(c)) for c in S(U, V_))
    def line(pts, c=ink):
        d.line([pt(*p) for p in pts], fill=c + (255,), width=1)
    line([(1.0, sh - 1.2), (5.0, sh - 1.2)], (120, 120, 132))                     # the printed heading, unreadable
    line([(7.0, sh - 1.2), (10.0, sh - 1.2)], (120, 120, 132))
    road = [(1.4, 26.6), (3.0, 22.6), (2.4, 18.6), (4.2, 14.2), (6.0, 9.4), (7.0, 4.6)]
    line(road)
    line([(1.0, 16.6), (9.0, 15.8)])                                                # the fence
    for (mu, mv) in ((6.2, 25.2), (11.6, 26.2)):                                   # two mesas: a flat top on short legs
        line([(mu - 1.4, mv - 1.0), (mu - 1.0, mv), (mu + 1.0, mv), (mu + 1.4, mv - 1.0)])
    def circle(cu, cv, r=1.6):
        x, y = S(cu, cv)
        rx = abs(S(cu + r, cv)[0] - x)
        ry = abs(S(cu, cv + r)[1] - y)
        d.ellipse([x - rx, y - ry, x + rx, y + ry], outline=ink + (255,), width=1)
    def number(text, U, V_):
        x, y = S(U, V_)
        x, y = int(round(x)), int(round(y))
        slope = (S(U + 1.0, V_)[1] - S(U, V_)[1]) / max(1e-6, (S(U + 1.0, V_)[0] - S(U, V_)[0]))
        for i, ch in enumerate(text):
            gx = x + i * 4
            gy = y + int(round(i * 4 * slope))
            for r_, row_ in enumerate(FONT35[ch]):
                for c_, on in enumerate(row_):
                    if on == "1":
                        d.point((gx + c_, gy + r_), fill=ink + (255,))
    circle(14.0, 23.2, 1.7)
    number("1921", 10.0, 20.6)
    circle(8.6, 12.2, 1.6)
    number("44", 10.8, 13.6)
    circle(10.6, 5.4, 1.5)
    sx, sy = S(13.6, 5.8)                                                           # the thumb's smudge, where the third number is
    d.ellipse([sx - 3.6, sy - 2.4, sx + 3.6, sy + 2.4], fill=(150, 144, 132, 255))
    d.ellipse([sx - 2.6, sy - 1.6, sx + 2.4, sy + 1.4], fill=(128, 122, 112, 255))
    for i in range(6):                                                              # the column of empty boxes
        bu, bv = sw - 2.6, sh - 3.6 - i * 3.6
        x, y = S(bu, bv)
        d.rectangle([round(x), round(y), round(x) + 2, round(y) + 2], outline=ink + (255,))
    line([(1.0, 2.4), (2.4, 3.0), (3.8, 2.2), (5.2, 3.0), (6.6, 2.2), (8.0, 2.8)])  # the margin note: a squiggle
    m = np.asarray(im, F32)[..., 3] > 127
    m &= cover_mask
    out[m] = (np.asarray(im, F32)[..., :3][m] / 255.0)
    return out


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "fast":
        pic, st = render(ss=1, fast=True)
        g = grade(pic)
        to_image(g).save(f"{WORK}/fast.png")
        tones(g, "tones:")
        print("fast", round(time.time() - t0, 1), "s;", len(st.occ), "shadow boxes;", len(st.names), "things")
        sys.exit()
    if mode == "paint":
        pic, st = render(ss=1, fast=True)
        out = details(paint(grade(wob(pic))), maps_of(st))
        to_image(out).save(f"{WORK}/paint.png")
        tones(out, "tones:")
        print("paint", round(time.time() - t0, 1), "s")
        sys.exit()

    # ================================================================ the full run
    from nevada_limo_layout import write as write_layout
    SS = 2
    GOES = ("ropes", "bag", "juice", "clipboard")
    # ---- everything in the car, in its first state (the cut-outs are taken from this one)
    A, stA = render(ss=SS, fast=False)
    to_image(A).save(f"{WORK}/1-under.png")
    print("all", round(time.time() - t0, 1))
    # ---- the backdrop: the car with the things that go, the ropes and our own seat taken away, and with them their
    #      shadows (a thing that goes takes its shadow with it); the divider's glass stays (the backdrop is complete)
    occB = stA.occ_without(*GOES)
    B, stB = render(ss=SS, fast=False, skip=GOES + ("front",), occ=occB)
    print("back", round(time.time() - t0, 1))
    wA, wB = wob(A), wob(B)
    pA = details(paint(grade(wA), 2), maps_of(stA))
    pB = details(paint(grade(wB), 2), maps_of(stB))
    print("painted", round(time.time() - t0, 1))
    wins = panes()
    pA, pB = restate_glass(pA, wins), restate_glass(pB, wins)
    cover = lambda st, **k: wob(st.down((st.grp == st.groups.get(k["grp"], -99)).astype(F32))) if "grp" in k else wob(st.down(st.mask_of(*k["name"]).astype(F32)))
    hole = cover(stA, name=("divider-up",)) > 0.5                       # the opening: both divider cut-outs are exactly this
    up, down = divider_view("up"), divider_view("down")
    pA[hole], pB[hole] = up[hole], up[hole]
    a_front = cover(stA, grp="front") > 0.5
    masks = {g: cover(stA, grp=g) > 0.5 for g in ("bag", "juice", "clipboard")}
    pA = sheet_marks(pA, masks["clipboard"])
    to_image(pA).save(f"{WORK}/2-all.png")
    tones(pA, "tones:")

    def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.007, amount=0.011):
        g = grain(picture, seed, amount)
        from brush import palette_of
        sample_of = g if alpha is None else g[alpha > 0.5]
        pal = palette_of([sample_of.reshape(-1, 3)], colors=min(colors, max(8, len(np.unique((sample_of.reshape(-1, 3) * 255).astype(np.uint8), axis=0)))))
        idx = to_palette(g, pal, speckle=speckle)
        save(name, idx, pal, alpha)
        return os.path.getsize(name)

    rng = np.random.default_rng(SEED + 5)
    speck = 0.05 + 0.12 * rng.random((H, W)).astype(F32)               # a cut-out's shadow ends in a speckle: its edge is hard
    lumA, lumB = wA @ LUM, wB @ LUM

    def own_shadow(m, others, reach=16):
        """Where the backdrop is darker with this thing in it than without: its shadow, near it, not on the others."""
        near = blur(m.astype(F32), reach * 0.5) > 0.01
        dark = np.clip((lumB - lumA) / np.maximum(lumB, 0.05), 0, 1) * near * ~others * ~m
        return dark

    sizes, boxes = {}, {}
    sizes["back"] = finish(pB, f"{OUT}/back.png", 160)
    sizes["front"] = finish(pA, f"{OUT}/front.png", 64, a_front.astype(F32))
    sizes["divider-up"] = finish(pA, f"{OUT}/divider-up.png", 40, hole.astype(F32))
    pD = pA.copy()
    pD[hole] = down[hole]
    sizes["divider-down"] = finish(pD, f"{OUT}/divider-down.png", 72, hole.astype(F32))
    for g in ("bag", "juice", "clipboard"):
        m = masks[g]
        others = np.zeros((H, W), bool)
        for o in masks:
            if o != g:
                others |= masks[o]
        sh = own_shadow(m, others)
        a = m | (sh > speck)
        pic = np.where(m[..., None], pA, pB * np.clip(lerp(np.ones_like(lumA), lumA / np.maximum(lumB, 1e-3), 1.0), 0, 1)[..., None])
        sizes[g] = finish(pic, f"{OUT}/{g}.png", 48 if g != "clipboard" else 64, a.astype(F32))
        ys, xs = np.nonzero(a)
        boxes[g] = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
        ys, xs = np.nonzero(m)                                           # (the thing itself, without its shadow: for its shape to click)
        boxes[g + "-own"] = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    # ---- the ropes, four states: the bow coming undone, the loose end longer each time. Each painted on its own patch
    #      of the picture; the rope's own pixels from that, and under it a contact shadow on the backdrop's own leather.
    rope_boxes = []
    for nst in (4, 3, 2, 1):
        st0 = Stage(V, ss=1)
        T.ropes(st0, nst)
        rm = st0.mask_of("ropes")
        ys, xs = np.nonzero(rm)
        rope_boxes.append((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    rx0 = max(0, min(b[0] for b in rope_boxes) - 28); ry0 = max(0, min(b[1] for b in rope_boxes) - 28)
    rx1 = min(W, max(b[2] for b in rope_boxes) + 28); ry1 = min(H, max(b[3] for b in rope_boxes) + 28)
    rect = (int(rx0), int(ry0), int(rx1), int(ry1))
    for nst in (4, 3, 2, 1):
        R, stR = render(ss=SS, fast=False, rect=rect, occ=occB, skip=("bag", "juice", "clipboard", "front"), strands=nst)
        wR = wob(R, rect)
        pR = details(paint(grade(wR, rect), 2), maps_of(stR, rect))
        rm = wob(stR.down((stR.grp == stR.groups.get("ropes", -99)).astype(F32)), rect) > 0.5
        x0, y0, x1, y1 = rect
        full = np.zeros((H, W), bool)
        full[y0:y1, x0:x1] = rm
        # the contact shadow: the rope's shape let down a pixel or two onto the cushion, soft, and speckled at its edge
        lay_ = np.roll(full.astype(F32), 1, axis=0) * 0.8 + np.roll(np.roll(full.astype(F32), 2, axis=0), 1, axis=1) * 0.6
        sh = np.clip(blur(lay_, 1.0) * 1.4, 0, 1) * ~full
        a = full | (sh > speck * 2.2)
        pic = pB * (1 - 0.42 * sh)[..., None]
        pic[full] = 0
        patch = np.zeros((H, W, 3), F32)
        patch[y0:y1, x0:x1] = pR
        pic[full] = patch[full]
        sizes[f"ropes-{nst}"] = finish(pic, f"{OUT}/ropes-{nst}.png", 32, a.astype(F32))
        ys, xs = np.nonzero(a)
        boxes[f"ropes-{nst}"] = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    print("cut-outs", round(time.time() - t0, 1), sizes)
    ys, xs = np.nonzero(a_front)
    boxes["front"] = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    ys, xs = np.nonzero(hole)
    boxes["divider"] = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    write_layout(stA, stB, boxes, wins, cover)
    import subprocess
    subprocess.run([sys.executable, "comp.py", OUT, "back", "divider-up", "ropes-4", "bag", "juice", "clipboard", "front"])
    later = Image.open(f"{OUT}/back.png").convert("RGBA")            # and the other state of everything that changes
    for n_ in ("divider-down", "ropes-1", "front"):
        later.alpha_composite(Image.open(f"{OUT}/{n_}.png").convert("RGBA"))
    later.convert("RGB").save("out/nevada-limo-comp-later.png")
    print("done", round(time.time() - t0, 1))

"""Inside Grandpa Joe's Last Stop (scene `nevada-store`): a run-down gas-stop store in the Nevada desert, forty
years in business, one morning in the present.

    python3 nevada_store.py            everything: backdrop, cut-outs, frames, the hens, layout.json, the comp, the people
    python3 nevada_store.py fast       the under-painting only, one ray per pixel, hard shadows: for composing (20 s)
    python3 nevada_store.py paint      the same with the brush pass and the details over it: for judging the look

ONE CAMERA. The room is measured in centimetres (nevada_store_model.py) and every pixel of the picture is a ray from
the game's own camera for this scene (room.View: horizon 158, full 455; the lens 3.25 m up at the room's near end,
turned 12 degrees to the left). What the ray meets, and how the light reaches that place, is worked out in the room
(nevada_store_kit.py, nevada_store_things.py, nevada_store_props.py), so the tiles, the boards, the tin ceiling, the
hubcaps and every piece of furniture run to the same vanishing point, and every shadow falls away from the window.

THE VIEW. We stand just inside the front door, looking along the store at the far wall: the counter in the middle
with Grandma Jolene's place behind it, the hubcaps over it, Harold the cooler in the far left corner, the back door
open at the far right on the hen yard; the front window with the sun shade in it on the left wall, the spinner rack
of sunglasses in front of it; the rock bins out on the floor at the right; the ceiling fan, still since 1979.

LIGHT (keep to it): morning.
  - the SUN, low behind us and to the left, comes in at the near sash of the window (the shade stops it at the far
    one) and lies across the linoleum toward the counter as the sash's own shape, slanting: warm, the brightest
    light in the room after the window itself; it throws the spinner rack's shadow and the counter's edge;
  - the WINDOW is the brightest thing in the picture: the sunlit lot and the road beyond the shaded porch;
  - the BACK DOOR lets in the sky's light, cool, onto the floor and the back wall round it; the yard beyond the
    shack's own shadow is in sun;
  - HAROLD glows a little, cool white, through his glass;
  - nothing else is lit: the corners and the tin ceiling fall away, warm-dark near us, cool-dark far off.

THREE TONES. Light: the window, the sun on the floor and on the counter's front, the yard through the back door.
Middle: the floor, the counter, the green boards, the hubcaps. Dark: the ceiling, the corners, the foreground.

HOW THE PICTURE IS MADE (the four passes of the README):
  1. under:   render() - the room as the camera sees it, lit
  2. strokes: paint()  - brush.strokes over it, interior sizes
  3. details: paint() puts back every edge and small thing crisply; details() adds the lit front edges of tops and
              the dark line behind each near thing; letters() lays every word through the camera, crisp
  4. finish:  finish() - grain, a palette, speckle, PNG-8
The cut-outs are the same pixels as a picture of the whole room (so they fit exactly); the backdrop is the room
painted again WITHOUT them, their shadows still lying where they fall."""

import json
import math
import os
import subprocess
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, blur, lerp, noise, sample, strokes, grain, to_palette, save
from room import View
import nevada_store_model as M
import nevada_store_things as T
import nevada_store_props as P
from nevada_store_kit import Stage, Lamp, Sun, shade, col, floor_contact, LUM, lay_on, pen_mask

W, H = 800, 600
V = View(**M.VIEW)
OUT = "out/nevada-store"
WORK = "out/nevada-store-work"
SEED = 12
EXPOSE = 1.45
COOL_BELOW = 0.55                                    # light weaker than this begins to turn blue-violet

# the groups that are cut-outs (each painted on its own, and left out of the backdrop)
CUTS = ("counter", "cooler", "spinner", "mirror", "rockbins", "doorframe", "shade", "hat-1", "hat-2", "hat-3", "hat-4", "hat-5", "front")


# ---------------------------------------------------------------- the light
def lamps():
    wz0, wz1, wy0, wy1 = M.WINDOW
    bx0, bx1, by0, by1 = M.BACKDOOR
    sky_win = Lamp((-40, (wy0 + wy1) / 2 + 10, (M.MULLION + wz1) / 2 + 10), "#fff0d8", 1.0, reach=230, size=55.0, wrap=0.55, samples=6,
                   inside_only=True, name="window", core=0.7, fill=0.05)
    sky_win2 = Lamp((-40, wy1 - 20, (wz0 + M.MULLION) / 2), "#e8eef4", 0.25, reach=170, size=45.0, wrap=0.55, samples=4,
                    inside_only=True, name="window2", core=0.7)
    door = Lamp(((bx0 + bx1) / 2, 110, -50), "#aec6f0", 1.05, reach=200, size=45.0, wrap=0.5, samples=5, inside_only=True, name="door",
                core=0.6, fill=0.06)
    harold = Lamp(((M.COOLER[0] + M.COOLER[1]) / 2, 110, M.COOLER[5] + 6), "#d8ecf4", 0.45, reach=75, aim=(0, -0.25, 1), spread=0.0, soft=0.9,
                  back=0.15, size=30.0, wrap=0.4, samples=3, inside_only=True, name="harold", core=0.8)
    bounce = Lamp((300, 14, 215), "#ffcc94", 0.95, reach=260, size=90.0, wrap=0.8, shadows=False, inside_only=True, name="bounce", core=1.2)   # the sun's patch on the floor, giving back
    return [sky_win, sky_win2, door, harold, bounce]


def window_bars(i, u, v, w):
    """1 where the sun comes through the window, 0 where the frame or the post between the sashes is."""
    z0, z1, y0, y1 = M.WINDOW
    Z = z0 + u * (z1 - z0)
    Y = y0 + v * (y1 - y0)
    post = np.clip((np.abs(Z - M.MULLION) - 3.0) / np.maximum(w, 0.5), 0, 1)
    return post.astype(F32)


SUN = Sun(M.SUN, "#ffd2a0", 3.4, [("X", -8.0, M.WINDOW[0] + 4, M.WINDOW[1] - 4, M.WINDOW[2] + 4.5, M.WINDOW[3] - 4)], soft=(1.5, 0.012),
          bars=window_bars, size=3.0)


def ambient(X, Y, Z, N, st):
    """The light that is simply in the room on a bright morning: warm from the sunlit floor near the window, cooler
    toward the back door, falling away into the corners and up to the tin ceiling."""
    up = N[..., 1]
    near_win = np.exp(-np.hypot(X, (Z - 200) * 0.7) / 380.0)
    near_door = np.exp(-(np.hypot(X - 640, Z) / 300.0))
    low = np.clip(1 - Y / 420.0, 0.25, 1)
    a = col("#b89070")[None, None, :] * ((0.10 + 0.12 * near_win) * low)[..., None]
    a = a + col("#7088c0")[None, None, :] * (0.04 + 0.08 * near_door)[..., None]
    a = a + col("#a07050")[None, None, :] * (np.clip(-up, 0, 1) * 0.08)[..., None]           # what the floor gives back to undersides
    corner = np.exp(-np.minimum(np.minimum(X, M.W - X), Z) / 70.0) * 0.4
    a = a * (1 - corner)[..., None]
    ceil = np.clip((Y - 280) / 110.0, 0, 1)
    a = a * (1 - 0.45 * ceil)[..., None]
    return a


# ---------------------------------------------------------------- putting the room together
def build(st, roller_phase=None, tv_frame=None):
    T.set_camera(st.C)
    T.shell(st)
    T.window(st, G_shade="shade")
    T.backdoor(st, G="doorframe")
    T.frontdoor(st, G="back")
    P.cooler(st, "cooler")
    P.bulletin(st)
    P.hatrack(st)
    for n in range(1, 6):
        P.hat(st, n)
    P.payphone(st)
    P.chair(st, "doorframe")
    P.survival(st, tv_frame=tv_frame)
    P.hubcaps(st)
    P.counter(st, "counter", roller_phase=roller_phase)
    P.autoshelf(st)
    P.spinner(st, "spinner", True, "mirror")
    P.rockbins(st, "rockbins")
    P.fan(st)
    P.foreground(st, "front")


def render(ss=1, fast=True, skip=(), rect=None, occ=None, sun=True, **state):
    """-> (picture, stage). The picture is at picture size (rays averaged)."""
    st = Stage(V, ss=ss, rect=rect)
    st.skip = set(skip)
    build(st, **state)
    sun_occ = None
    pic, light = shade(st, lamps(), ambient, SUN if sun else None, fast=fast, occ=occ, expose=EXPOSE, sh_step=1 if not fast else 2)
    X, Y, Z = st.places()
    outside = (st.flag & 4) > 0
    lum = light @ LUM
    deep = np.clip(1 - lum / COOL_BELOW, 0, 1) ** 1.3 * (~outside)
    pic = pic * (1 + deep[..., None] * np.array([-0.12, -0.02, 0.22], dtype=F32)[None, None, :])
    floor = st.mask_of("floor")
    # things sit on the floor: a dark line round every foot
    feet = list(st.feet.values())
    dark = floor_contact(X, Z, feet, reach=7.0, amount=0.5) * floor
    dark += floor * (np.exp(-np.clip(Z, 0, 1e4) / 12.0) * 0.30 + np.exp(-np.clip(X, 0, 1e4) / 12.0) * 0.30 + np.exp(-np.clip(M.W - X, 0, 1e4) / 12.0) * 0.28)
    walls = st.mask_of("back", "left", "right")
    dark += walls * np.exp(-np.clip(Y, 0, 1e4) / 8.0) * 0.25
    ceil = st.mask_of("ceiling")
    dark += ceil * 0.0
    pic = pic * (1 - np.clip(dark, 0, 0.8))[..., None]
    # the sun's patch on the floor is warm and bright; the linoleum gives some back as a sheen
    pic = pic + (st.sunlit * floor * 0.06)[..., None] * col("#ffe8c0")[None, None, :]
    # depth by tone: the far end a little paler and cooler, as through the dusty air of the room
    t = np.minimum(st.t, 3000.0)
    air = np.clip((t - 700) / 700.0, 0, 1) * 0.10 * (~outside)
    pic = pic * (1 - air[..., None]) + col("#8a90a8")[None, None, :] * air[..., None]
    # the foreground is darker and warmer than the middle of the room (people pass behind it)
    fr = (st.grp == st.groups.get("front", -1))
    pic[fr] = pic[fr] * col("#c8a890")
    return st.down(pic), st


_Y, _X = np.mgrid[0:H, 0:W].astype(F32)
_DX = (noise((H, W), 30, SEED + 3, 3) - 0.5) * 2 * 0.7
_DY = (noise((H, W), 30, SEED + 4, 3) - 0.5) * 2 * 0.7


def wob(a, rect=None):
    """Nothing a hand rules is perfectly straight: every picture and mask is pushed about by the same slow field,
    under a pixel, so all the cut-outs still fit one another exactly."""
    if rect is None:
        return sample(a, _X + _DX, _Y + _DY)
    x0, y0, x1, y1 = rect
    return sample(a, _X[y0:y1, x0:x1] - x0 + _DX[y0:y1, x0:x1], _Y[y0:y1, x0:x1] - y0 + _DY[y0:y1, x0:x1])


def wob_near(a):
    yy = np.clip(np.round(_Y + _DY), 0, H - 1).astype(np.intp)
    xx = np.clip(np.round(_X + _DX), 0, W - 1).astype(np.intp)
    return a[yy, xx]


def grade(pic, rect=None):
    """The whole picture's last adjustments: the near corners deeper and warmer, the top cooler, to hold the eye in
    the room and on the counter."""
    x0, y0, x1, y1 = rect or (0, 0, W, H)
    y, x = np.mgrid[y0:y1, x0:x1].astype(F32)
    cx = ((x - 420) / 420) ** 2
    low = np.clip((y - 470) / 130, 0, 1) ** 1.3
    top = np.clip((150 - y) / 150, 0, 1) ** 1.1
    v = np.clip(cx * 0.22 * (0.4 + 0.6 * low) + low * 0.22 + top * 0.20 + top * cx * 0.2, 0, 0.6)
    warm = col("#5a3020")
    out = pic * (1 - v[..., None]) + pic * warm[None, None, :] * 1.4 * v[..., None]
    out = out * (1 - top[..., None] * 0.08) + col("#3a4268") * (top * 0.06)[..., None]
    grey = (out @ LUM)[..., None]
    out = grey + (out - grey) * 1.10
    return np.clip(out, 0, 1)


def paint(crisp, seed=2):
    """The brush pass, and then the built things said again crisply over it."""
    b = strokes(crisp, sizes=(9, 5, 2), seed=seed, density=1.5, jitter=0.04, keep=0.30)
    hf = np.abs(crisp - blur(crisp, 1.4)).sum(axis=2)
    w = np.clip(hf * 7.0 - 0.05, 0, 1)
    w = np.maximum(w, blur(w, 0.7))
    out = lerp(b, crisp, (0.14 + 0.84 * w)[..., None])
    return np.clip(out + 0.45 * (out - blur(out, 0.9)), 0, 1)


def maps_of(st):
    return wob(st.pick(np.minimum(st.t, 5000.0))), wob(st.pick(st.N[..., 1])), wob_near(st.pick(st.oid)), st.names.get("floor", -1)


def details(pic, maps):
    """Small crisp accents: the lit front edge of every top, and a dark line where a thing stands in front of another
    far behind it."""
    t, ny, oid, floor_id = maps
    below_same = (np.roll(oid, -1, axis=0) == oid) & (np.roll(ny, -1, axis=0) < 0.5) & (ny > 0.9)
    below_same[-1] = False
    edge = below_same & (oid != floor_id)
    out = pic.copy()
    out[edge] = np.clip(out[edge] * 1.22 + 0.03, 0, 1)
    for ax, sh_ in ((0, 1), (0, -1), (1, 1), (1, -1)):
        tn = np.roll(t, sh_, axis=ax)
        behind = (t - tn > 14.0) & (t - tn > 0.02 * t)
        if ax == 0:
            behind[0 if sh_ == 1 else -1] = False
        else:
            behind[:, 0 if sh_ == 1 else -1] = False
        out[behind] = out[behind] * 0.78
    return out


# ---------------------------------------------------------------- the words, laid through the camera
def words():
    """Every word in the room that must be read, as (mask, quad in the room, ink, how strong, group)."""
    out = []
    # DISPLAY ONLY, on the card on the window's sill
    q = T.card_quad(lift=0.4)
    d = T.DISPLAY_CARD
    m = pen_mask(["DISPLAY", "ONLY"], d["w"], d["h"], 10.6, res=14, pen=0.19, track=0.20, lead=1.30, seed=31, wobble=0.03)
    out.append((m, q, "#b8302a", 1.0, "back"))
    # Jolene's card to Jed on the board
    m, q = P.board_words()
    out.append((m, q, "#2a2a5a", 1.0, "back"))
    # HAROLD, on a strip of tape across the cooler's red header
    tape_q = P.harold_tape()
    w_ = tape_q[1][0] - tape_q[0][0]
    h_ = tape_q[0][1] - tape_q[3][1]
    m = pen_mask(["HAROLD"], w_, h_, 11.0, res=14, pen=0.21, track=0.14, seed=32, squeeze=0.9)
    out.append((m, tape_q, "#2a2a3a", 1.0, "cooler"))
    # ROCKS $1 on the card hung under the bins' front lip
    q = P.rock_card()
    m = pen_mask(["ROCKS $1"], P.ROCK_CARD[0], P.ROCK_CARD[1], 11.0, res=12, pen=0.21, track=0.14, seed=33, squeeze=0.85)
    out.append((m, q, "#b8302a", 1.0, "rockbins"))
    return out


_ROCKS = {}


def rock_words(edges, lip):
    out = []
    for i, (name, quad) in enumerate(P.rock_labels(edges, lip)):
        wide = quad[1][0] - quad[0][0]
        high = quad[0][1] - quad[3][1]
        if name == "SHY":
            m2 = pen_mask(["SHY"], wide, high, 8.2, res=18, pen=0.21, track=0.16, seed=40 + i, top=0.5, squeeze=0.9)
            sm = pen_mask(["(DO NOT LOOK", "AT DIRECTLY)"], wide, high, 2.6, res=26, pen=0.17, track=0.12, lead=1.3, seed=50, top=10.4, squeeze=0.85)
            out.append((m2, quad, "#2a2a3a", 1.0, "rockbins"))
            out.append((sm, quad, "#3a3a50", 0.85, "rockbins"))
        elif name == "THE SENATOR":
            m = pen_mask(["THE", "SENATOR"], wide, high, 7.4, res=18, pen=0.21, track=0.13, lead=1.16, seed=40 + i, squeeze=0.8)
            out.append((m, quad, "#2a2a3a", 1.0, "rockbins"))
        else:
            m = pen_mask([name], wide, high, 8.2, res=18, pen=0.21, track=0.14, seed=40 + i, squeeze=0.82)
            out.append((m, quad, "#2a2a3a", 1.0, "rockbins"))
    return out


def letters(pic, st, groups=None, rect=None):
    """Lay every word (and the tapes they are on) through the camera, crisp, over the painted picture; only those of
    the given groups (None: all). The light on them is the light where they are."""
    allw = words() + rock_words(*_ROCKS["bins"])
    covered = np.zeros(pic.shape[:2], F32)
    for mask, quad, ink, amount, grp in allw:
        if groups is not None and grp not in groups:
            continue
        # the ink takes the light of its paper: sample the painted paper under the quad's middle (it is pale paper or tape)
        cx = sum(q[0] for q in quad) / 4
        cy = sum(q[1] for q in quad) / 4
        cz = sum(q[2] for q in quad) / 4
        px, py = V.pt(cx, cy, cz)
        if rect:
            px, py = px - rect[0], py - rect[1]
        iy, ix = int(min(max(py, 0), pic.shape[0] - 1)), int(min(max(px, 0), pic.shape[1] - 1))
        here = pic[max(iy - 2, 0):iy + 3, max(ix - 2, 0):ix + 3].reshape(-1, 3)
        k = np.clip(np.percentile(here.max(axis=1), 80) / 0.88, 0.3, 1.1)
        tone = col(ink) * k
        cov = lay_on(pic, V, quad, mask, tone, amount=amount, sub=4, crisp=0.6, rect=rect)
        covered = np.maximum(covered, cov)
    return covered


def to_image(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def tones(a, label=""):
    lum = (np.clip(a, 0, 1) * 255) @ LUM
    print(label, "mean", (a.mean(axis=(0, 1)) * 255).round(0), "lum 5/25/50/75/95:", np.percentile(lum, [5, 25, 50, 75, 95]).round(0))


def palette_for(px, colors, seed=3, rounds=14):
    """A palette for the picture: half the sample drawn toward the coloured and the light pixels (the small bright
    things matter most: the window, letters, hubcap glints, the hats), the first choices spread far apart."""
    rng = np.random.default_rng(seed)
    px = px.reshape(-1, 3).astype(F32)
    mx, mn = px.max(axis=1), px.min(axis=1)
    w = 0.2 + (mx - mn) * 2.2 + mx * 0.6
    n = len(px)
    take = min(n, 26000)
    cum = np.cumsum(w.astype(np.float64))
    drawn = np.minimum(np.searchsorted(cum, rng.random(take) * cum[-1]), n - 1)
    pick = np.concatenate([rng.choice(n, size=take, replace=False), drawn])
    sm = px[pick]
    colors = min(colors, len(np.unique((sm * 255).astype(np.uint8), axis=0)))
    centers = np.empty((colors, 3), dtype=F32)
    centers[0] = sm[rng.integers(len(sm))]
    d = ((sm - centers[0]) ** 2).sum(axis=1)
    for k in range(1, colors):
        i = int(d.argmax())
        centers[k] = sm[i]
        d = np.minimum(d, ((sm - centers[k]) ** 2).sum(axis=1))
    for _ in range(rounds):
        dist = ((sm[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        near = dist.argmin(axis=1)
        for k in range(colors):
            mine = sm[near == k]
            if len(mine):
                centers[k] = centers[k] * 0.25 + mine.mean(axis=0) * 0.75
    return centers


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.007, amount=0.011, pal=None):
    g = grain(picture, seed, amount)
    if pal is None:
        sample_of = g if alpha is None else g[alpha > 0.5]
        pal = palette_for(sample_of, colors)
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def cover(st, grp=None, name=None):
    if grp is not None:
        gs = [grp] if isinstance(grp, str) else list(grp)
        m = np.isin(st.grp, [st.groups[g] for g in gs if g in st.groups])
    else:
        m = st.mask_of(*([name] if isinstance(name, str) else name))
    return st.down(m.astype(F32))


def bbox(mask, pad=0):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max()) + 1 + pad, int(ys.max()) + 1 + pad]


def clamp_rect(r, pad=6):
    return (max(0, r[0] - pad), max(0, r[1] - pad), min(W, r[2] + pad), min(H, r[3] + pad))


def look(src, out, *boxes):
    """Crop and enlarge parts of a picture to look at the detail: boxes (x0, y0, x1, y1, zoom)."""
    im = Image.open(src).convert("RGB") if isinstance(src, str) else src
    tiles = []
    for b in boxes:
        z = b[4] if len(b) > 4 else 2
        c = im.crop(tuple(b[:4]))
        tiles.append(c.resize((c.width * z, c.height * z), Image.NEAREST))
    w_ = sum(t.width for t in tiles) + 6 * (len(tiles) - 1)
    h_ = max(t.height for t in tiles)
    sheet = Image.new("RGB", (w_, h_), (40, 40, 40))
    x = 0
    for t in tiles:
        sheet.paste(t, (x, 0))
        x += t.width + 6
    sheet.save(out)
    return out


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "fast":
        pic, st = render(ss=1, fast=True)
        to_image(grade(pic)).save(f"{WORK}/fast.png")
        print("fast", round(time.time() - t0, 1), "s;", len(st.occ), "shadow boxes;", len(st.names), "things")
        sys.exit()
    if mode == "paint":
        pic, st = render(ss=1, fast=True)
        _ROCKS["bins"] = P.rockbins(Stage(V, ss=1, rect=(0, 0, 2, 2)), "x")
        out = details(paint(grade(wob(pic))), maps_of(st))
        letters(out, st)
        to_image(out).save(f"{WORK}/paint.png")
        tones(out, "tones:")
        print("paint", round(time.time() - t0, 1), "s")
        sys.exit()
    import nevada_store_cuts
    nevada_store_cuts.main(t0)

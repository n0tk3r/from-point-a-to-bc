"""Big Sister's attic room, "The Retreat". Night, 9:40 p.m.

    python3 home_bigsis_room.py          everything: backdrop, cut-outs, layout.json, the comp, the people test
    python3 home_bigsis_room.py fast     the under-painting only, one ray per pixel: for composing (about 15 s)
    python3 home_bigsis_room.py paint    the same with the brush pass and the details over it: for judging the look

ONE CAMERA. The room is measured in centimetres (home_bigsis_room_model.py) and every pixel of the picture is a
ray from the game's own camera for this scene (room.View: horizon 120, full 440, cam (380, 1150), yaw 0, focal
800). What the ray meets, and how the room's small lights fall on that place, is worked out in the room
(home_bigsis_room_kit.py). So the floorboards run to the one vanishing point (400, 120), the boards of the great
slope lie level across it, its rafters fan up it toward us (they meet at (400, 797), below the picture), and every
thing stands on the floor in the same perspective and throws a soft shadow away from a light that has a place.

THE VIEW. The ridge runs across the picture above the top of the frame. The far wall is a low wall, 140 cm; from
its ledge the roof comes up and over toward us as one slanted ceiling that fills the upper half of the picture,
with two skylights in it. The end walls close the room at the far left and right. We look down on the floor from
high under the ridge; the hatch we came up by is at our feet, bottom left.

LIGHT (keep to it): SOFT, WARM AND LOW, FROM MANY SMALL SOURCES. No bright lamp anywhere.
  - three paper lanterns under the slope (peach): the gentle light on the middle of the floor, where people stand;
  - two strings of tiny warm lights looped from rafter to rafter: they make the whole slope glow rose and cream;
  - flameless candles in glass along the low wall's ledge, on the bookcase, over the bed, one on the floor by the
    towels, and two candle lanterns on the floor at the bed's foot; a few of the tiny lights wound down the gauze;
  - the salt lamp on its stump, far left: deep amber on the end wall, the plants and the floor round it;
  - the desk lamp turned low; a glow from under the bed's platform; the landing's light coming up the hatch; the
    notice's own little picture-light. (The near half of the roof is cut away so that we can see in: what its
    lights would give the things that face us is put back as a low, shadowless warm light from our side.)
  - the MOON through the two skylights: pale blue, falling as two soft slanted patches across the middle of the
    floor (it stands high and to the right, beyond the far wall, so the patches slant toward us and to the left).
  What no light reaches is blue-violet, never black. The far end is a little cooler and closer in value; the near
  corners and the top corners of the roof are the deepest tones in the picture.

THREE TONES. Dark: the top corners of the slope, the night in the skylights, the near corners and the foreground.
Middle: the slope, the walls, the floor. Light: the lanterns and the glow round them, the gauze over the bed and
its linen, the candles along the ledge, the two patches of moonlight.

WHERE THINGS ARE. Far wall, left to right: the small palm in the corner, the long low bookcase with its books in a
rainbow and her timeline on the wall above it, the sound table (sound machine and little fountain), the writing
desk and stool with her novel planned on cards above it. Left end: the round window, the salt lamp on its stump,
the diffuser, the stand of ferns and ivy, her robe on its hook, the basket of rolled towels, a candle, and her
slippers set side by side where she steps into them from the hatch.
Right end: the low platform bed under its gauze. On the floor: the exercise mat and the round rug. Under the
slope: the skylights, the lanterns, the strings of lights, a hanging plant. Foreground (front plane): the hatch
with its rail and the top of the ladder, her notice on its easel, a floor cushion with her tea tray, the pouf and
a folded blanket.

HOW THE PICTURE IS MADE (the four passes of STYLE.md):
  1. under:   render() - the room as the camera sees it, lit (kit and things)
  2. strokes: paint()  - brush.strokes over it, small interior sizes
  3. details: paint() says every built edge and small thing again crisply; details() adds the lit front edges of
              tops, a dark line where a near thing stands before a far one, and the lettering of the notice
  4. finish:  finish() - grain, a limited palette chosen for a soft night picture, speckle, PNG-8
The cut-outs are the same pixels as a picture of the whole room (so they fit exactly); the backdrop is the room
painted again WITHOUT the desk and the foreground, their shadows still lying where they fall."""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, blur, lerp, noise, sample, strokes, grain, to_palette, save
from room import View
import home_bigsis_room_model as M
import home_bigsis_room_things as T
from home_bigsis_room_kit import Stage, Lamp, Moon, shade, col, floor_contact, LUM

W, H = 800, 600
V = View(**M.VIEW)
OUT = "out/home-bigsis-room"
SEED = 31
COOL_BELOW = 0.60            # light weaker than this begins to turn blue-violet
EXPOSE = 0.92                # how much light the picture is given (a dim room, but the people in it must be seen)


# ---------------------------------------------------------------- the light
def lamps():
    L = []
    for i, (x, z, y, r) in enumerate(M.LANTERNS):                # the paper lanterns: big, soft, never bright
        L.append(Lamp((x, y, z), "#ffc48c", 0.98 if i == 1 else 0.84, reach=165, size=r * 0.9, wrap=0.5, core=0.9, samples=7, name="lantern",
                      aim=(0, -1, 0), spread=-0.25, soft=0.9, back=0.18))
    sx, sz = M.SALTLAMP[0], M.SALTLAMP[1]
    L.append(Lamp((sx + 2, 63, sz + 2), "#ff7a30", 1.5, reach=62, size=7, wrap=0.45, core=0.6, samples=6, name="salt"))
    hx0, hx1, hz0, hz1 = M.HATCH                                  # the landing's lamp, coming up the hatch
    L.append(Lamp(((hx0 + hx1) / 2, -90, hz0 + 40), "#ffb878", 2.3, reach=130, size=10, wrap=0.5, shadows=False,
                  gate=("Y", 0.0, hx0, hx1, hz0, hz1), name="hatch"))
    for s_, pts in enumerate(T.STRINGS):                          # the strings of tiny lights: each bulb lights its own bit of roof
        for p in pts:
            L.append(Lamp(p, "#ffb088", 0.10, reach=32, local=68, wrap=0.6, name="bulb"))
        for k in range(0, len(pts), max(len(pts) // 7, 1)):      # and together they are a soft light for the room below
            L.append(Lamp(pts[k], "#ffbc9c", 0.013, reach=240, shadows=False, wrap=0.8, core=1.2, name="string"))
    for x in M.CANDLES:                                           # candles in glass along the ledge
        L.append(Lamp((x, 141, 7.5), "#ffa24c", 0.66, reach=30, local=88, wrap=0.7, name="candle"))
    bx0, bx1, _, by1, bz0, bz1 = M.BOOKCASE                       # two more on the bookcase
    L.append(Lamp((bx0 + 20, by1 + 9, 13), "#ffa24c", 0.40, reach=30, local=80, wrap=0.7, name="candle"))
    L.append(Lamp((bx0 + 142, by1 + 7, 16), "#ffa24c", 0.30, reach=28, local=70, wrap=0.7, name="candle"))
    dx0, dx1, _, dy1, dz0, dz1 = M.DESK                           # the desk lamp, turned low
    L.append(Lamp((dx1 - 26, dy1 + 13, dz0 + 23), "#ffae60", 0.62, reach=36, local=120, wrap=0.5, name="desk"))
    ex0, ex1, _, ey1, ez0, ez1 = M.BED                            # a glow from under the bed's platform, along its side and foot
    for z in np.arange(ez0 + 14, ez1 - 6, 26.0):
        L.append(Lamp((ex0 + 5, 5, z), "#ffa860", 0.34, reach=22, local=86, wrap=0.8, name="underbed"))
    for x in np.arange(ex0 + 14, ex1 - 4, 26.0):
        L.append(Lamp((x, 5, ez1 - 5), "#ffa860", 0.34, reach=22, local=86, wrap=0.8, name="underbed"))
    sx0, _, _, sy1, sz0, _ = M.BEDSHELF                           # the candles on the little shelf over the pillows
    L.append(Lamp((sx0 - 2, sy1 + 9, sz0 + 14), "#ffa24c", 0.46, reach=34, local=110, wrap=0.7, name="candle"))
    L.append(Lamp((sx0 - 2, sy1 + 7, sz0 + 30), "#ffa24c", 0.36, reach=30, local=100, wrap=0.7, name="candle"))
    for i, (lx, lz) in enumerate(M.FOOTLAMPS):                    # the two candle lanterns at the bed's foot
        L.append(Lamp((lx, 12 - 2 * i, lz), "#ffa850", 0.56 - 0.1 * i, reach=34, local=150, wrap=0.6, name="footlamp"))
    L.append(Lamp((M.FLOORCANDLE[0], 13, M.FLOORCANDLE[1]), "#ffa850", 0.80, reach=36, local=150, wrap=0.6, name="floorcandle"))
    for p in T.canopy_bulbs():                                    # the tiny lights wound down the parted gauze
        L.append(Lamp(p, "#ffb088", 0.07, reach=26, local=52, wrap=0.7, name="bulb"))
    x0, x1, y0, y1, z = M.SIGN                                    # the notice has its own little picture-light
    L.append(Lamp(((x0 + x1) / 2, y1 + 6, z + 14), "#ffd0a0", 0.52, reach=50, local=130, wrap=0.5, name="notice"))
    # the near half of the roof is cut away with its own strings of lights: what they give the things that face us
    for x in (120, 400, 680):
        L.append(Lamp((x, 170, 860), "#ffb898", 0.24, reach=400, shadows=False, wrap=0.1, core=1.0, ceil=120.0, name="near"))
    return L


MOON = Moon(toward=(0.22, 1.0, -0.30), color=(0.25, 0.48, 1.0), power=1.25, knee=M.KNEE, rise=M.RISE, openings=M.SKYLIGHTS,
            soft=(4.0, 0.030), bars=T.skylight_bars)


def ambient(X, Y, Z, N):
    """The light that is simply in the room: the night's blue from the skylights, and the warmth the many small
    lights give back off the pale roof and walls (more of it high in the room, where the strings are)."""
    up = 0.5 + 0.5 * N[..., 1]
    a = col("#5a5ccc")[None, None, :] * (0.25 * (0.80 + 0.20 * up))[..., None]
    high = np.clip(Y / 300.0, 0, 1)
    a = a + col("#c08868")[None, None, :] * (0.012 + 0.010 * high)[..., None]
    front = np.clip(N[..., 2], 0, 1)                                         # what turns toward us is seen
    a = a + col("#b07a60")[None, None, :] * (front * 0.04)[..., None]
    return a


# ---------------------------------------------------------------- putting the room together
def build(st):
    T.shell(st)
    T.everything(st)


def render(ss=1, fast=True, skip=(), occ=None):
    """-> (picture, stage). The picture is at picture size (rays averaged)."""
    st = Stage(V, ss=ss)
    st.skip = set(skip)
    build(st)
    sh_step = 2 if fast else 1
    L = lamps()
    pic, light = shade(st, L, ambient, MOON, fast=fast, occ=occ, expose=EXPOSE, sh_step=sh_step)
    X, Y, Z = st.places()
    # shadows are cool: where little light falls the color leans to blue-violet (a painter's shadows, not a camera's)
    lum = light @ LUM
    deep = np.clip(1 - lum / COOL_BELOW, 0, 1) ** 1.2
    pic = pic * (1 + deep[..., None] * np.array([-0.24, -0.08, 0.34], dtype=F32)[None, None, :])
    floor = st.mask_of("floor")
    # the boards give the moon back as a pale sheen (we are looking toward it); the rug does not
    rx, rz, rr = M.RUG
    bare = floor & (np.hypot(X - rx, Z - rz) > rr)
    pic = pic + (getattr(st, "moonlit", 0) * bare * 0.08)[..., None] * col((0.45, 0.66, 1.0))[None, None, :]
    # things sit on the floor: a dark line round every foot
    dark = floor_contact(X, Z, list(st.feet.values()), reach=8.0, amount=0.5) * floor
    # where wall meets floor the corners gather a little dark
    dark += floor * (np.exp(-np.clip(Z, 0, 1e4) / 12.0) * 0.26 + np.exp(-np.clip(X, 0, 1e4) / 11.0) * 0.24 + np.exp(-np.clip(M.W - X, 0, 1e4) / 11.0) * 0.24)
    wallish = st.mask_of("far", "endL", "endR")
    dark += wallish * np.exp(-np.clip(Y, 0, 1e4) / 8.0) * 0.16
    pic = pic * (1 - np.clip(dark, 0, 0.75))[..., None]
    # the far corners of the room fall away: less light finds its way into them, and what does is cool
    Zc = np.clip(Z, 0, 1e4)
    corner = (np.exp(-np.clip(X, 0, 1e4) / 70.0) + np.exp(-np.clip(M.W - X, 0, 1e4) / 70.0)) * np.exp(-Zc / 150.0)
    corner = np.clip(corner + 0.3 * np.exp(-np.clip(X, 0, 1e4) / 40.0) * np.clip((Zc - 250) / 200, 0, 1) + 0.3 * np.exp(-np.clip(M.W - X, 0, 1e4) / 40.0) * np.clip((Zc - 250) / 200, 0, 1), 0, 1)
    lit_ = np.clip(lum / 0.9, 0, 1)                                           # (but not where a lamp stands in the corner)
    k_ = (corner * 0.34 * (1 - 0.6 * lit_))[..., None]
    pic = pic * (1 - k_) + pic * col("#6a6aa8")[None, None, :] * 1.1 * k_
    # the veil (the gauze over the bed): the room shows through it
    if st.gauze is not None:
        vl = st.gauze
        vpic, vlight = shade(vl, [l for l in L if not l.shadows or l.local or l.name in ("lantern",)], ambient, None, fast=True, occ=[], expose=EXPOSE, sh_step=2)
        a = np.where(vl.t < st.t, vl.alpha, 0.0)[..., None]
        pic = pic * (1 - a) + vpic * a
    # depth by tone: the far end a little paler and bluer, as through the room's air
    t = np.minimum(st.t, 3000.0)
    air = np.clip((t - 760) / 700.0, 0, 1) * 0.07
    pic = pic * (1 - air[..., None]) + col("#6a6c9c")[None, None, :] * air[..., None]
    # the foreground is darker and warmer than the middle of the room (people pass behind it)
    fr = (st.grp == st.groups.get("front", -1)) & ~st.mask_of("rules")                 # (not the notice: it has to be read)
    pic[fr] = pic[fr] * col("#d2aea0")
    return st.down(pic), st


_Y, _X = np.mgrid[0:H, 0:W].astype(F32)
_DX = (noise((H, W), 30, SEED + 3, 3) - 0.5) * 2 * 0.8
_DY = (noise((H, W), 30, SEED + 4, 3) - 0.5) * 2 * 0.8


def wob(a):
    """Nothing a hand rules is perfectly straight: every picture and mask is pushed about by the same slow field,
    under a pixel, so all the cut-outs still fit one another exactly."""
    return sample(a, _X + _DX, _Y + _DY)


def wob_near(a):
    yy = np.clip(np.round(_Y + _DY), 0, H - 1).astype(np.intp)
    xx = np.clip(np.round(_X + _DX), 0, W - 1).astype(np.intp)
    return a[yy, xx]


def grade(pic):
    """The whole picture's last adjustments: the near corners and the top corners deeper, to hold the eye in the
    room; a little more color than a camera would give."""
    y, x = _Y, _X
    cx = ((x - 400) / 400) ** 2
    low = np.clip((y - 470) / 130, 0, 1) ** 1.4
    top = np.clip((150 - y) / 150, 0, 1) ** 1.3
    v = np.clip(cx * 0.22 * (0.3 + 0.7 * low) + low * 0.20 + top * cx * 0.34 + top * 0.06, 0, 0.6)
    warm = col("#5a3440")
    out = pic * (1 - v[..., None]) + pic * warm[None, None, :] * 1.5 * v[..., None]
    grey = (out @ LUM)[..., None]
    out = grey + (out - grey) * 1.10
    return np.clip(out, 0, 1)


def to_image(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def tones(a, label=""):
    """The picture's tones in numbers (the eye is easily fooled about how dark a night picture is)."""
    lum = (np.clip(a, 0, 1) * 255) @ LUM
    print(label, "mean", (a.mean(axis=(0, 1)) * 255).round(0), "lum 5/25/50/75/95:", np.percentile(lum, [5, 25, 50, 75, 95]).round(0))


def halo(st):
    """What glows gives the paint round it a breath of its own color (a painter's halo, a few pixels: the game
    draws any real beams and glows itself)."""
    e = np.minimum(st.down(st.emi), 1.4)
    warm = e * np.array([1.0, 0.9, 0.7], dtype=F32)
    return blur(warm, 2.0) * 0.09 + blur(warm, 7.0) * 0.10


def paint(crisp, seed=2, keep=None):
    """The brush pass, and then the built things said again crisply over it: where the under-painting has an edge or
    a small thing, most of it comes back; where it is only a broad tone, the brushwork stays."""
    b = strokes(crisp, sizes=(8, 4, 2), seed=seed, density=1.5, jitter=0.036, keep=0.24)
    hf = np.abs(crisp - blur(crisp, 1.4)).sum(axis=2)
    w = np.clip(hf * 7.5 - 0.05, 0, 1)
    w = np.maximum(w, blur(w, 0.7))
    if keep is not None:
        w = np.maximum(w, keep)
    out = lerp(b, crisp, (0.12 + 0.86 * w)[..., None])
    return np.clip(out + 0.45 * (out - blur(out, 0.9)), 0, 1)             # and the whole a little sharper, as a small brush leaves it


def maps_of(st):
    """What the details pass needs to know about each pixel: how far away it is, how much it faces up, what it is."""
    return wob(st.pick(np.minimum(st.t, 5000.0))), wob(st.pick(st.N[..., 1])), wob_near(st.pick(st.oid)), st


def details(pic, maps):
    """Small crisp accents that a painter adds last, found from what each pixel shows: the lit front edge of every
    top (a table top, a lid, a shelf), and a soft dark line where one thing stands in front of another far behind."""
    t, ny, oid, st = maps
    skip_ids = [st.names[n] for n in ("floor", "slope", "far", "endL", "endR", "strings", "skylight", "window") if n in st.names]
    below_same = (np.roll(oid, -1, axis=0) == oid) & (np.roll(ny, -1, axis=0) < 0.5) & (ny > 0.9)
    below_same[-1] = False
    edge = below_same & ~np.isin(oid, skip_ids)
    out = pic.copy()
    out[edge] = np.clip(out[edge] * 1.22 + 0.02, 0, 1)
    for ax, sh_ in ((0, 1), (0, -1), (1, 1), (1, -1)):
        tn = np.roll(t, sh_, axis=ax)
        behind = (t - tn > 14.0) & (t - tn > 0.02 * t)
        if ax == 0:
            behind[0 if sh_ == 1 else -1] = False
        else:
            behind[:, 0 if sh_ == 1 else -1] = False
        behind &= ~np.isin(np.roll(oid, sh_, axis=ax), [st.names.get(n, -1) for n in ("strings", "pampas", "canopy")])   # (not round wires and feathery things)
        out[behind] = out[behind] * 0.80
    return out


def glints(pic, maps):
    """The last touches of all: a point of light where something wet or glazed or polished turns to a lamp.
    Each is put where the thing really is (through the room's camera), and only if that thing is seen there."""
    t, ny, oid, st = maps
    fx, fz, _ = M.FOUNTAIN
    ty = M.SOUNDTABLE[3]
    tx, tz = (M.TEA[0] + M.TEA[1]) / 2, (M.TEA[2] + M.TEA[3]) / 2 - 4
    dx0, dy1, dz0 = M.DESK[0], M.DESK[3], M.DESK[4]
    spots = [("fountain", (fx - 4, ty + 10.4, fz + 7), "#dff0ff", 1.0, 0.85), ("fountain", (fx + 5, ty + 10.4, fz + 9), "#cfe4f4", 0.8, 0.7),
             ("tea", (tx - 10, 26.5, tz + 2), "#f4f8f0", 1.3, 0.8), ("tea", (tx + 12, 18.6, tz + 9), "#fff4e0", 0.8, 0.7),
             ("desk", (dx0 + 28, dy1 + 8, dz0 + 25.5), "#f4fbff", 0.8, 0.75),
             ("diffuser", (M.STUMP2[0] - 3, M.STUMP2[3] + 16, M.STUMP2[1] + 6), "#fff6ea", 1.2, 0.55),
             ("machine", (M.MACHINE[0] + 35.5, M.MACHINE[2] + 17, M.MACHINE[5] + 0.3), "#fff0d8", 0.8, 0.8)]
    for (lx, lz) in M.FOOTLAMPS:
        spots.append(("footlamps", (lx - 5, 14, lz + 6), "#fff0d0", 0.7, 0.6))
    out = pic
    for name, p, color, r, a in spots:
        x, y = V.pt(*p)
        xi, yi = int(round(x)), int(round(y))
        if not (1 <= xi < W - 1 and 1 <= yi < H - 1) or name not in st.names:
            continue
        if not (oid[yi - 1:yi + 2, xi - 1:xi + 2] == st.names[name]).any():
            continue
        d2 = (_X - x) ** 2 + (_Y - y) ** 2
        m = np.clip(1.2 - d2 / (r * r), 0, 1) * a
        out = out * (1 - m[..., None]) + col(color)[None, None, :] * m[..., None]
    return out


def keep_mask(st):
    """Where the lettering is: it is laid back wholly crisp after the brush (it has to be read)."""
    m = st.down(st.mask_of("rules").astype(F32))
    return wob(m)


def _settle(sm, centers, rounds):
    for _ in range(rounds):
        near = np.empty(len(sm), dtype=np.intp)
        for i in range(0, len(sm), 20000):
            near[i:i + 20000] = ((sm[i:i + 20000, None, :] - centers[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        for k in range(len(centers)):
            mine = sm[near == k]
            if len(mine):
                centers[k] = mine.mean(axis=0)
    return centers


def palette_for(px, colors, seed=3, rounds=12):
    """A palette for a soft night picture. Most of this room is quiet: rose plaster, cream boards in amber light,
    violet shadow, and the picture lives on the small differences between them; so three quarters of the palette
    is chosen from the picture as it is (every pixel counting the same). What matters most in it besides is small
    and colored (book spines, the red mark, candle flames, stars, the lettering): the last quarter is chosen from
    the colored and the light pixels alone, so those are not averaged away into the browns."""
    rng = np.random.default_rng(seed)
    px = px.reshape(-1, 3).astype(F32)
    n = len(px)
    colors = min(colors, len(np.unique((px[rng.choice(n, size=min(n, 20000), replace=False)] * 255).astype(np.uint8), axis=0)))
    if colors < 8:
        return px[rng.choice(n, size=colors, replace=False)].copy()
    plain = px[rng.choice(n, size=min(n, 40000), replace=False)]
    mx, mn = px.max(axis=1), px.min(axis=1)
    w = 0.02 + (mx - mn) ** 1.5 * 3.0 + np.clip(mx - 0.6, 0, 1) * 1.2
    cum = np.cumsum(w.astype(np.float64))
    vivid = px[np.minimum(np.searchsorted(cum, rng.random(min(n, 14000)) * cum[-1]), n - 1)]
    k2 = max(colors // 4, 2)
    k1 = colors - k2
    c1 = _settle(plain, plain[rng.choice(len(plain), size=k1, replace=False)].copy(), rounds)
    c2 = vivid[rng.choice(len(vivid), size=k2, replace=False)].copy()
    d = ((vivid - c2[0]) ** 2).sum(axis=1)                                  # the vivid ones start as far apart as they can be
    for k in range(1, k2):
        i = int(d.argmax())
        c2[k] = vivid[i]
        d = np.minimum(d, ((vivid - c2[k]) ** 2).sum(axis=1))
    c2 = _settle(vivid, c2, 8)
    return np.concatenate([c1, c2]).astype(F32)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.006, amount=0.009):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_for(sample_of, colors)
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def cover(st, grp=None, name=None):
    """How much of each picture pixel a group (or a named thing) fills."""
    if grp is not None:
        m = st.grp == st.groups.get(grp, -1)
    else:
        m = st.mask_of(*([name] if isinstance(name, str) else name))
    return st.down(m.astype(F32))


def whole(pic, st):
    """Under-painting -> the painted picture (passes 2 and 3)."""
    crisp = grade(wob(np.clip(pic + halo(st), 0, 1)))
    maps = maps_of(st)
    return glints(details(paint(crisp, 2, keep_mask(st)), maps), maps)


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "fast":
        pic, st = render(ss=1, fast=True)
        out = grade(np.clip(pic + halo(st), 0, 1))
        to_image(out).save("out/home-bigsis-room-2-all.png")
        tones(out, "tones:")
        print("fast", round(time.time() - t0, 1), "s;", len(st.occ), "shadow boxes;", len(st.names), "things")
        sys.exit()
    if mode == "paint":                                        # a quick look at the brushwork: one ray per pixel
        pic, st = render(ss=1, fast=True)
        out = whole(pic, st)
        to_image(out).save("out/home-bigsis-room-2-all.png")
        tones(out, "tones:")
        print("paint", round(time.time() - t0, 1), "s")
        sys.exit()

    SS = 2
    # ---- everything in the room (the cut-outs are taken from this one)
    A, stA = render(ss=SS, fast=False)
    to_image(A).save("out/home-bigsis-room-1-under.png")
    print("all", round(time.time() - t0, 1))
    # ---- the room with the desk and the foreground taken away (their shadows stay)
    B, stB = render(ss=SS, fast=False, skip=("desk", "front"), occ=stA.occ)
    print("back", round(time.time() - t0, 1))
    pA = whole(A, stA)
    pB = whole(B, stB)
    print("painted", round(time.time() - t0, 1))
    a_desk = wob(cover(stA, grp="desk"))
    a_front = wob(np.clip(cover(stA, grp="front") + cover(stA, name="well"), 0, 1))   # (the cut-out is whole over the hatch's opening)
    to_image(pA).save("out/home-bigsis-room-2-all.png")
    tones(pA, "tones:")
    sizes = {}
    sizes["back"] = finish(pB, f"{OUT}/back.png", 160)
    sizes["desk"] = finish(pA, f"{OUT}/desk.png", 64, a_desk)
    sizes["front"] = finish(pA, f"{OUT}/front.png", 96, a_front)
    print("cut-outs", round(time.time() - t0, 1), sizes)

    import home_bigsis_room_layout
    home_bigsis_room_layout.write(stA, stB, a_desk, a_front, wob)
    import subprocess
    subprocess.run([sys.executable, "comp.py", OUT, "back", "desk", "front"])
    subprocess.run([sys.executable, "home_bigsis_room_people.py"])     # the game's own figures in the room (needs the game's server)
    print("done", round(time.time() - t0, 1))

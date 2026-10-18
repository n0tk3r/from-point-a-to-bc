"""The break room of the Office Of Peculiar Sectors' field headquarters (scene `office-breakroom`): a small room the
staff have made their own and the regulations have not quite noticed, under fluorescent tubes. OFFICE-17D.

    python3 office_breakroom.py            everything: backdrop, cut-outs and their states, the clock's frames,
                                           layout.json, the comps and the check
    python3 office_breakroom.py fast       the under-painting only, one ray per pixel, hard shadows: for composing
    python3 office_breakroom.py paint      the same with the brush pass and the details over it: for judging the look

ONE CAMERA. The room is measured in centimetres (office_breakroom_model.py) and every pixel of the picture is a ray from
the game's own camera for this scene (room.View: horizon 200, full 383; the lens 2.0 m up, a step inside the room,
turned a little to the left). What the ray meets, and how the light reaches that place, is worked out in the room
(office_breakroom_kit.py, office_breakroom_things.py, office_breakroom_props.py), so the tiles of the floor and the
ceiling, the block courses and every piece of furniture run to the same vanishing point, and every shadow falls away
from the tubes.

THE VIEW. We look at the back wall almost square on: the tall fridge in the left corner (the return grille over it in
the ceiling, the box of forks and the dusty plant on top), the counter along the wall with the microwave, the dish rack
and the sink, Wendell's pie and its card, the coffee maker and the cups; the corkboard over the counter, the clock over
the board; the snack machine and the door to the hall at the right. The couch runs along the left wall toward us, the
afghan over its back; Jed's orange chair stands at the counter's right end, turned to look along it at the pie; a round
table and its chair stand in the near right, and a low table with an abandoned game of solitaire on it in the near left,
cut off by the bottom edge (the foreground: no bare floor along the bottom); the bin is in the gap by the fridge.

LIGHT (keep to it): two fluorescent fittings in the ceiling, over the counter and over the middle of the room: a cool,
faintly green white that falls straight down, so the counter's top, the floor and the tops of things are the lit
planes, the walls fall off upward to a dimmer band under the ceiling, the ceiling itself is lit only by what the
floor gives back (the fittings' own lenses the brightest things in the picture), and every shadow lies under its
thing: soft, violet, deepest under the counter's lip, the couch and the machine. The snack machine glows warm from
inside; the hall's tubes light the door's little window.

THREE TONES. Light: the fittings, the counter's top, the floor under the near fitting, the fridge's face, the sheets on
the board. Middle: the walls, the floor further off, the couch, the machine's window. Dark: under the counter, under the
couch and the table, the machine's body, the corners of the ceiling.

HOW THE PICTURE IS MADE (the four passes of the README):
  1. under:   render() - the room as the camera sees it, lit
  2. strokes: paint()  - brush.strokes over it, interior sizes
  3. details: paint() puts back every edge and small thing crisply; details() adds the lit front edges of tops and the
              dark line behind each near thing; letters() lays every word through the camera, crisp
  4. finish:  finish() - grain, a palette, speckle, PNG-8
The cut-outs are the same pixels as a picture of the whole room (so they fit exactly); the backdrop is the room painted
again WITHOUT them, their shadows still lying where they fall."""

import os
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, blur, lerp, noise, sample, strokes, grain, to_palette, save
from room import View
import office_breakroom_model as M
import office_breakroom_things as T
import office_breakroom_props as P
from office_breakroom_kit import Stage, Lamp, shade, col, floor_contact, LUM, lay_on, pen_mask

W, H = 800, 600
V = View(**M.VIEW)
OUT = "out/office-breakroom"
WORK = "out/office-breakroom-work"
SEED = 17
EXPOSE = 1.25
COOL_BELOW = 0.50                                    # light weaker than this begins to turn blue-violet

# the groups that are cut-outs (each painted on its own, and left out of the backdrop)
CUTS = ("pie", "schedule", "vent", "vending", "door", "chair", "front")


# ---------------------------------------------------------------- the light
def lamps():
    out = []
    for i, (x0, x1, z0, z1) in enumerate(M.TROFFERS):
        cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
        power = 1.15 if i == 0 else 1.15 * (1 - len(M.TUBES_OUT) / 3.0) + 0.08          # the near one has tubes out
        out.append(Lamp((cx, M.H - 4.0, cz), "#f0f6e6", power, reach=235.0, aim=(0, -1, 0), spread=0.18, soft=0.62, back=0.0, size=34.0,
                        wrap=0.35, samples=8, name=f"tubes-{i}", core=0.9, fill=0.05))
    gx0, gx1, gy0, gy1 = M.VEND_GLASS
    out.append(Lamp(((gx0 + gx1) / 2, (gy0 + gy1) / 2, M.VENDING[5] + 4), "#ffe2b0", 0.45, reach=70.0, aim=(0, -0.2, 1), spread=-0.2,
                    soft=0.8, back=0.1, local=150.0, name="vending", core=0.8, wrap=0.4))
    dx0, dx1, dy0, dy1 = M.DOOR
    out.append(Lamp(((dx0 + dx1) / 2 + 20, 150, -6), "#e6eedc", 0.20, reach=60.0, local=90.0, name="doorglass", core=0.8, wrap=0.5))
    return out


def ambient(X, Y, Z, N, st):
    """The light that is simply in a room of pale walls under tubes: even and cool, a little warmer low down where the
    floor gives it back, falling off into the corners and toward the ceiling."""
    up = N[..., 1]
    a = col("#a0a8b8")[None, None, :] * 0.17
    a = a + col("#c8c4a8")[None, None, :] * (np.clip(-up, 0, 1) * 0.20)[..., None]          # what the floor gives back to undersides and the ceiling
    a = a + col("#b8c4b0")[None, None, :] * (np.clip(up, 0, 1) * 0.05)[..., None]
    corner = np.exp(-np.clip(np.minimum(np.minimum(X, M.W - X), Z), 0, 1e4) / 60.0) * 0.35
    a = a * (1 - corner)[..., None]
    high = np.clip((Y - 150) / 140.0, 0, 1)
    a = a * (1 - 0.25 * high)[..., None]
    return a


# ---------------------------------------------------------------- putting the room together
def build(st, pie="whole", vent_eyes=False, door_open=False, vending="full", hand=None, only=None):
    """Everything in the room, in a state of the story. `only`: a list of the builders to run (for a quick patch)."""
    parts = [
        ("shell", lambda: T.shell(st)),
        ("troffers", lambda: T.troffers(st)),
        ("speaker", lambda: T.speaker(st)),
        ("vent", lambda: T.vent(st, eyes=vent_eyes)),
        ("door", lambda: T.door(st, open_=door_open)),
        ("hall", lambda: T.hall(st)),
        ("calendar", lambda: T.calendar(st)),
        ("fridge", lambda: P.fridge(st)),
        ("counter", lambda: P.counter(st, pie_state=pie)),
        ("cabinets", lambda: P.cabinets(st)),
        ("board", lambda: P.board(st)),
        ("schedule", lambda: P.schedule(st)),
        ("clock", lambda: P.clock(st, hand=hand)),
        ("vending", lambda: P.vending(st, state=vending)),
        ("couch", lambda: P.couch(st)),
        ("chair", lambda: P.chair(st)),
        ("table", lambda: P.table(st)),
        ("lowtable", lambda: P.lowtable(st)),                  # OFFICE-17D (resumed): the near left's foreground
        ("trash", lambda: P.trash(st)),
    ]
    for name, f in parts:
        if only is None or name in only:
            f()


def render(ss=1, fast=True, skip=(), rect=None, occ=None, **state):
    """-> (picture, stage). The picture is at picture size (rays averaged)."""
    st = Stage(V, ss=ss, rect=rect)
    st.skip = set(skip)
    st.pools = []                                         # soft pools of shadow on the floor under things that stand over it
    build(st, **state)
    pic, light = shade(st, lamps(), ambient, None, fast=fast, occ=occ, expose=EXPOSE, sh_step=1 if not fast else 2)
    X, Y, Z = st.places()
    outside = (st.flag & 4) > 0
    lum = light @ LUM
    deep = np.clip(1 - lum / COOL_BELOW, 0, 1) ** 1.3 * (~outside)
    pic = pic * (1 + deep[..., None] * np.array([-0.10, -0.04, 0.20], dtype=F32)[None, None, :])
    floor = st.mask_of("floor")
    # things sit on the floor: a dark line round every foot, and a shadow along the foot of every wall
    feet = list(st.feet.values())
    dark = floor_contact(X, Z, feet, reach=6.0, amount=0.55) * floor
    dark += floor * (np.exp(-np.clip(Z, 0, 1e4) / 10.0) * 0.30 + np.exp(-np.clip(X, 0, 1e4) / 10.0) * 0.30 + np.exp(-np.clip(M.W - X, 0, 1e4) / 10.0) * 0.28)
    for (px, pz, rx, rz, amt) in st.pools:
        dark += floor * amt * np.exp(-((X - px) / rx) ** 2 - ((Z - pz) / rz) ** 2)
    walls = st.mask_of("back", "left", "right")
    dark += walls * np.exp(-np.clip(Y, 0, 1e4) / 6.0) * 0.20
    dark += walls * np.clip((Y - 170) / 115.0, 0, 1) ** 1.5 * 0.22                   # the walls fall off up toward the ceiling
    ceil = st.mask_of("ceiling")
    dark += ceil * (np.exp(-np.clip(Z, 0, 1e4) / 25.0) + np.exp(-np.clip(X, 0, 1e4) / 25.0) + np.exp(-np.clip(M.W - X, 0, 1e4) / 25.0)) * 0.22
    pic = pic * (1 - np.clip(dark, 0, 0.8))[..., None]
    # the waxed floor: a soft sheen of the near fitting
    tx0, tx1, tz0, tz1 = M.TROFFERS[1]
    sheen = np.exp(-((X - (tx0 + tx1) / 2) / 90.0) ** 2 - ((Z - (tz0 + tz1) / 2 + 60) / 120.0) ** 2) * floor * 0.10
    pic = pic + sheen[..., None] * col("#f0f6e6")[None, None, :]
    # depth by tone: the far wall a little paler and cooler, as through the room's air
    t = np.minimum(st.t, 3000.0)
    air = np.clip((t - 560) / 500.0, 0, 1) * 0.08 * (~outside)
    pic = pic * (1 - air[..., None]) + col("#9aa0b4")[None, None, :] * air[..., None]
    # the near things are darker and warmer than the middle of the room
    fr = (st.grp == st.groups.get("front", -1))
    pic[fr] = pic[fr] * col("#d8c4b0")
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
    """The whole picture's last adjustments: the near corners deeper and warmer, the ceiling's band a little cooler and
    darker, to hold the eye on the counter and the board."""
    x0, y0, x1, y1 = rect or (0, 0, W, H)
    y, x = np.mgrid[y0:y1, x0:x1].astype(F32)
    cx = ((x - 400) / 400) ** 2
    low = np.clip((y - 450) / 150, 0, 1) ** 1.3
    top = np.clip((120 - y) / 120, 0, 1) ** 1.2
    v = np.clip(cx * 0.20 * (0.4 + 0.6 * low) + low * 0.20 + top * 0.14 + top * cx * 0.18, 0, 0.55)
    warm = col("#4a3040")
    out = pic * (1 - v[..., None]) + pic * warm[None, None, :] * 1.5 * v[..., None]
    out = out * (1 - top[..., None] * 0.06) + col("#3a4060") * (top * 0.05)[..., None]
    grey = (out @ LUM)[..., None]
    out = grey + (out - grey) * 1.12
    return np.clip(out, 0, 1)


def paint(crisp, seed=2):
    """The brush pass, and then the built things said again crisply over it."""
    b = strokes(crisp, sizes=(9, 5, 2), seed=seed, density=1.5, jitter=0.04, keep=0.32)
    hf = np.abs(crisp - blur(crisp, 1.4)).sum(axis=2)
    w = np.clip(hf * 7.0 - 0.05, 0, 1)
    w = np.maximum(w, blur(w, 0.7))
    out = lerp(b, crisp, (0.16 + 0.82 * w)[..., None])
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
    out[edge] = np.clip(out[edge] * 1.20 + 0.03, 0, 1)
    for ax, sh_ in ((0, 1), (0, -1), (1, 1), (1, -1)):
        tn = np.roll(t, sh_, axis=ax)
        behind = (t - tn > 14.0) & (t - tn > 0.02 * t)
        if ax == 0:
            behind[0 if sh_ == 1 else -1] = False
        else:
            behind[:, 0 if sh_ == 1 else -1] = False
        out[behind] = out[behind] * 0.80
    return out


# ---------------------------------------------------------------- the words, laid through the camera
def words(pie="whole", door_open=False):
    """Every word in the room, as (mask, quad in the room, ink, how strong, group). The Office's notices are printed
    (the pen with no wobble); the birthday card is in felt pen."""
    out = []
    # LABEL YOUR LUNCH. · MGMT., on the freezer door
    q = P.fridge_sign_quad()
    sw = M.SIGN[2] - M.SIGN[0]
    shh = M.SIGN[3] - M.SIGN[1]
    m = pen_mask(["LABEL", "YOUR", "LUNCH."], sw, shh, 8.6, res=10, pen=0.20, track=0.18, lead=1.30, top=3.2, seed=301, wobble=0.0, squeeze=0.86)
    out.append((m, q, "#1e1e2a", 1.0, "back"))
    m2 = pen_mask(["· MGMT."], sw, shh, 3.6, res=14, pen=0.18, track=0.20, top=shh - 6.4, seed=302, wobble=0.0, align="right")
    out.append((m2, q, "#3a3a48", 0.95, "back"))
    # the board: FORM 7 IS NOT OPTIONAL
    pu, pv, pw, ph = M.SHEETS["form7"]
    q = P.sheet_quad("form7")
    m = pen_mask(["FORM 7"], pw, ph, 10.0, res=10, pen=0.24, track=0.16, top=3.0, seed=303, wobble=0.0, squeeze=0.9)
    out.append((m, q, "#1a1a26", 1.0, "back"))
    m = pen_mask(["IS NOT", "OPTIONAL"], pw, ph, 4.4, res=14, pen=0.22, track=0.14, lead=1.35, top=17.4, seed=304, wobble=0.0)
    out.append((m, q, "#c8302a", 1.0, "back"))
    # the index card: FOUND: ONE ROMAN SANDAL (1951) · SEE OPAL, in an old hand (too small to read: the look says it)
    pu, pv, pw, ph = M.SHEETS["found"]
    q = P.sheet_quad("found", 0.5)
    m = pen_mask(["FOUND:", "ONE ROMAN SANDAL", "(1951)", "SEE OPAL"], pw, ph, 2.6, res=18, pen=0.17, track=0.12, lead=1.5, top=3.6, seed=305, wobble=0.05, lean=0.12)
    out.append((m, q, "#2a2a6a", 0.9, "back"))
    # the bowling sheet's heading
    pu, pv, pw, ph = M.SHEETS["bowling"]
    q = P.sheet_quad("bowling")
    m = pen_mask(["LEAGUE"], pw, ph, 3.4, res=16, pen=0.22, track=0.14, top=1.6, seed=306, wobble=0.0, align="right")
    out.append((m, q, "#1a1a26", 0.95, "back"))
    # the schedule (its own cut-out): LAMPLIGHTER · TEST SCHEDULE, and its typed lines
    pu, pv, pw, ph = M.SHEETS["schedule"]
    q = P.schedule_quad()
    m = pen_mask(["LAMPLIGHTER"], pw, ph, 3.0, res=18, pen=0.24, track=0.12, top=3.0, seed=307, wobble=0.0, squeeze=0.9)
    out.append((m, q, "#16161e", 1.0, "schedule"))
    m = pen_mask(["TEST SCHEDULE"], pw, ph, 1.9, res=20, pen=0.22, track=0.12, top=7.6, seed=308, wobble=0.0)
    out.append((m, q, "#16161e", 0.95, "schedule"))
    typed = ["30 OCT 1747 SECTOR 1921", "ONE CIVILIAN VEHICLE", "UNCONFIRMED SEE FORM 7", "", "31 OCT 1700 SECTOR 44", "B-7",
             "", "PLEASE DO NOT LOOK", "DIRECTLY AT THE SECTOR"]
    m = pen_mask(typed, pw, ph, 1.15, res=24, pen=0.20, track=0.10, lead=1.75, top=12.4, seed=309, wobble=0.0, align="left")
    out.append((m, q, "#2a2a36", 0.85, "schedule"))
    # the birthday card: HAPPY BIRTHDAY WENDELL in blue, DO NOT EAT in red, (REGULATIONS) small
    flat = pie == "gone"
    q = P.card_quad(flat)
    cw, chh = M.CARD["w"], M.CARD["h"]
    m = pen_mask(["HAPPY", "BIRTHDAY", "WENDELL"], cw, chh, 1.9, res=24, pen=0.18, track=0.14, lead=1.32, top=0.9, seed=310, wobble=0.06, lean=0.08)
    out.append((m, q, "#2a4aa8", 1.0, "pie"))
    m = pen_mask(["DO NOT EAT"], cw, chh, 1.9, res=24, pen=0.24, track=0.12, top=7.4, seed=311, wobble=0.05)
    out.append((m, q, "#c8242a", 1.0, "pie"))
    m = pen_mask(["(REGULATIONS)"], cw, chh, 1.0, res=30, pen=0.18, track=0.10, top=9.8, seed=312, wobble=0.04)
    out.append((m, q, "#c8242a", 0.9, "pie"))
    if door_open:
        q = T.door_plate_quad()
        m = pen_mask(["BREAK ROOM"], 24.0, 10.0, 4.2, res=14, pen=0.2, track=0.14, seed=313, wobble=0.0)
        out.append((m, q, "#2a2a36", 1.0, "door-open"))
    return out


def letters(pic, groups=None, rect=None, **state):
    """Lay every word through the camera, crisp, over the painted picture; only those of the given groups (None: all).
    The ink takes the light of the paper it is on."""
    covered = np.zeros(pic.shape[:2], F32)
    for mask, quad, ink, amount, grp in words(state.get("pie", "whole"), state.get("door_open", False)):
        if groups is not None and grp not in groups:
            continue
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
    things matter most: the fittings, letters, the snacks, the pie), the first choices spread far apart."""
    rng = np.random.default_rng(seed)
    px = px.reshape(-1, 3).astype(F32)
    mx, mn = px.max(axis=1), px.min(axis=1)
    w = 0.2 + (mx - mn) * 2.2 + mx * 0.6
    n = len(px)
    take = min(n, 26000)
    cum = np.cumsum(w.astype(np.float64))
    drawn = np.minimum(np.searchsorted(cum, rng.random(take) * cum[-1]), n - 1)
    pick = np.concatenate([rng.choice(n, size=take, replace=n < take), drawn])
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
        tones(grade(pic), "tones:")
        print("fast", round(time.time() - t0, 1), "s;", len(st.occ), "shadow boxes;", len(st.names), "things")
        sys.exit()
    if mode == "paint":
        pic, st = render(ss=1, fast=True)
        out = details(paint(grade(wob(pic))), maps_of(st))
        letters(out)
        to_image(out).save(f"{WORK}/paint.png")
        tones(out, "tones:")
        print("paint", round(time.time() - t0, 1), "s")
        sys.exit()
    import office_breakroom_cuts
    office_breakroom_cuts.main(t0)

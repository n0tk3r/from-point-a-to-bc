"""Dad's study under the roof, "Trip Headquarters". Night, 9:40 p.m.

    python3 home_study.py          everything: backdrop, cut-outs, layout.json, the comp, the people test (about two minutes)
    python3 home_study.py fast     the under-painting only, one ray per pixel, hard shadows: for composing (10 s)
    python3 home_study.py paint    the same with the brush pass over it: for judging the look (15 s)

ONE CAMERA. The room is measured in centimetres (home_study_model.py) and every pixel of the picture is a ray
from the game's own camera for this scene (room.View: horizon 120, full 440). What the ray meets, and how the
lamps light that place, is worked out in the room (home_study_kit.py). So floorboards, the roof's boards, the
ridge and the plates all run to the one vanishing point, the rafters step back toward it, every piece of
furniture stands on the floor in the same perspective, and every shadow falls away from a real lamp.

THE VIEW. We are high under the ridge, looking along it at the far gable wall. The roof comes down on both
sides to low walls. The door to the landing is at the front left, in a partition under the slope; its leaf
stands open into the room and shows us its landing side, with Dad's notice on it.

LIGHT (keep to it):
  - the desk lamp, far left: a small warm pool on the desk, the wall and the corkboard above it;
  - the shaded lamp on the shelves, right: the bigger warm light; it throws the shadows of the globe, the
    vault, the heap toward the left and toward us, and makes a hot patch on the roof just above it;
  - the moon, through the gable window: pale blue, falling as the window's own shape (bars and all) across
    the middle of the floor and the rug, slanting to the left;
  - the landing's lamp through the open door, front left: warm on the leaf and on the floor at its foot.
  What no lamp reaches is blue-violet. The far end is cooler and closer in value; the near corners are the
  deepest, warmest darks.

THREE TONES. Dark: the roof overhead, the near corners, the foreground heap and the door's wall.
Middle: the floor and the gable. Light: the desk's pool, the shelf lamp and its patch of roof, the moon's
window on the floor, the paper banner.

WHERE THINGS ARE. Far wall, left to right: corkboard, calendar, the desk with the mainframe (note on the
monitor), the window over the radiator, the wall map over an old chest, the globe. Left: the filing cabinet
with the answering machine. Right: the shelves, the lamp, the family vault at their near end. Overhead: the
banner TRIP HEADQUARTERS on a string between two rafters, the model aeroplane over the map, a string of flags,
a lantern and a pair of skis under the left-hand rafters. Foreground: the door (left edge), the heap that did
not fit in the car (bottom), a suitcase and a rolled mat (bottom right).

HOW THE PICTURE IS MADE (the four passes of STYLE.md):
  1. under:   render() - the room as the camera sees it, lit (home_study_kit.py, home_study_things.py)
  2. strokes: paint()  - brush.strokes over it, interior sizes
  3. details: paint() puts back every edge and small thing of the under-painting crisply; details() adds the lit
              front edges of tops and the dark line behind each near thing
  4. finish:  finish() - grain, a 160-color palette chosen for a night picture, speckle, PNG-8
The cut-outs are the same pixels as a picture of the whole room (so they fit exactly); the backdrop is the room
painted again WITHOUT the desk and the foreground, their shadows still lying where they fall."""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, blur, lerp, noise, sample, strokes, grain, palette_of, to_palette, save, rgb
from room import View
import home_study_model as M
import home_study_things as T
from home_study_kit import Stage, Lamp, shade, col, floor_contact

W, H = 800, 600
V = View(**M.VIEW)
OUT = "out/home-study"
SEED = 21
COOL_BELOW = 0.62            # light weaker than this begins to turn blue-violet
EXPOSE = 2.15                # how much light the picture is given (a night room, but the people in it must be seen)


# ---------------------------------------------------------------- the light
def lamps():
    x0, z0 = M.DESK[0], M.DESK[4]
    lx, lz = M.SHELF_LAMP
    ty = M.SHELVES[3]
    desk = Lamp((x0 + 49, 76 + 45, z0 + 39.5), "#ffc47c", 0.80, reach=110, aim=(0.55, -0.80, 0.20), spread=0.10, soft=0.9, back=0.0, size=3.5)
    desk_bounce = Lamp((x0 + 74, 86, z0 + 52), "#ffb870", 0.34, reach=110, shadows=False, wrap=1.0, fill=0.22)      # what the lit desk top gives back to the wall
    shelf = Lamp((lx, ty + 27, lz), "#ffb466", 1.45, reach=150, aim=(0, -1, 0), spread=0.5, soft=0.6, back=0.6, double=True, size=6.5, fill=0.11)
    roof_bounce = Lamp((lx - 30, ty + 70, lz + 20), "#ffbe7a", 0.66, reach=330, size=18.0, samples=8, wrap=0.6)   # the lit roof above it lights the room
    hall = Lamp((46, 150, 690), "#ffb86a", 1.1, reach=100, size=5.0)
    wx = (M.WINDOW[0] + M.WINDOW[1]) / 2
    sky = Lamp((wx, (M.WINDOW[2] + M.WINDOW[3]) / 2 - 10, 14), (0.42, 0.6, 1.0), 0.5, reach=120, shadows=False, wrap=0.35)   # the night sky's own cool light, near the window
    return [desk, desk_bounce, shelf, roof_bounce, hall, sky]


MOON = dict(dir=(0.24, 0.62, -0.76), color=(0.22, 0.52, 1.3), power=1.45, window=(M.WINDOW[0], M.WINDOW[1], M.WINDOW[2], M.WINDOW[3], -7.0), bars=T.window_bars)


def ambient(X, Y, Z, N):
    """The light that is simply in the room at night: blue from the window at the far end, deeper and warmer toward
    us; and a little warm light from behind us (the landing, and what the lamps give back off the near wall), which
    is what lets us see the faces of things that are turned our way."""
    far = np.exp(-np.clip(Z, 0, 2000) / 560.0)
    up = 0.5 + 0.5 * N[..., 1]
    a = col("#4a66d0")[None, None, :] * ((0.17 + 0.11 * far) * (0.86 + 0.14 * up))[..., None]
    a = a + col("#8a5a48")[None, None, :] * ((1 - far) * 0.07)[..., None]
    front = np.clip(N[..., 2], 0, 1)
    a = a + col("#a8704c")[None, None, :] * (front * (0.03 + 0.17 * (1 - far)))[..., None]
    return a


# ---------------------------------------------------------------- putting the room together
def build(st, vault_open=False, note=False, tape=False, screen=None):
    T.shell(st)
    T.window(st)
    T.wall_things(st)
    T.far_floor(st)
    T.cabinet(st)
    T.shelves(st)
    T.vault(st, vault_open)
    T.globe(st)
    T.overhead(st)
    T.desk_group(st)
    if note:
        T.note(st)
    if screen:
        T.screen(st, screen)
    if tape:
        T.tape(st)
    T.door(st)
    T.heap(st)
    T.pile(st)


def render(ss=1, fast=True, skip=(), rect=None, occ=None, **state):
    """-> (picture, stage). The picture is at picture size (rays averaged)."""
    st = Stage(V, ss=ss, rect=rect)
    st.skip = set(skip)
    build(st, **state)
    pic, light = shade(st, lamps(), ambient, MOON, T.ATTIC, fast=fast, occ=occ, expose=EXPOSE)
    X, Y, Z = st.places()
    # shadows are cool: where little light falls, the color leans to blue-violet (a painter's shadows, not a camera's)
    lum = light @ np.array([0.3, 0.55, 0.15], dtype=F32)
    deep = np.clip(1 - lum / COOL_BELOW, 0, 1) ** 1.2
    pic = pic * (1 + deep[..., None] * np.array([-0.14, -0.03, 0.26], dtype=F32)[None, None, :])
    floor = st.mask_of("floor")
    # the varnished boards give the moon back as a pale blue sheen (we are looking toward it); the rug does not
    rx0, rx1, rz0, rz1 = M.RUG
    bare = floor & ~((X > rx0 - 8) & (X < rx1 + 8) & (Z > rz0) & (Z < rz1))
    pic = pic + (getattr(st, "moonlit", 0) * bare * 0.2)[..., None] * col((0.5, 0.7, 1.0))[None, None, :]
    # things sit on the floor: a dark line round every foot
    feet = [f for name, f in st.feet.items()]
    dark = floor_contact(st, X, Z, feet, reach=9.0, amount=0.6) * floor
    # and where wall meets floor, and under the roof at the plates, the corners gather dark
    dark += floor * (np.exp(-np.clip(Z, 0, 1e4) / 14.0) * 0.30 + np.exp(-np.clip(X, 0, 1e4) / 12.0) * 0.28 + np.exp(-np.clip(M.W - X, 0, 1e4) / 12.0) * 0.28)
    wallish = st.mask_of("gable", "kneeL", "kneeR")
    dark += wallish * np.exp(-np.clip(Y, 0, 1e4) / 9.0) * 0.22
    pic = pic * (1 - np.clip(dark, 0, 0.8))[..., None]
    # depth by tone: the far end a little paler and bluer, as through the room's air
    t = np.minimum(st.t, 3000.0)
    air = np.clip((t - 650) / 900.0, 0, 1) * 0.10
    pic = pic * (1 - air[..., None]) + col("#5a6c9c")[None, None, :] * air[..., None]
    # the foreground is darker and warmer than the middle of the room (people pass behind it)
    fr = (st.grp == st.groups.get("front", -1)) & ~st.mask_of("landing")
    pic[fr] = pic[fr] * col("#d2b4a2")
    return st.down(pic), st


_Y, _X = np.mgrid[0:H, 0:W].astype(F32)
_DX = (noise((H, W), 30, SEED + 3, 3) - 0.5) * 2 * 0.8
_DY = (noise((H, W), 30, SEED + 4, 3) - 0.5) * 2 * 0.8


def wob(a):
    """Nothing a hand rules is perfectly straight: every picture and mask is pushed about by the same slow field,
    under a pixel, so all the cut-outs still fit one another exactly."""
    return sample(a, _X + _DX, _Y + _DY)


def wob_near(a):
    """The same, for maps of whole numbers (which thing is where)."""
    yy = np.clip(np.round(_Y + _DY), 0, H - 1).astype(np.intp)
    xx = np.clip(np.round(_X + _DX), 0, W - 1).astype(np.intp)
    return a[yy, xx]


def grade(pic, rect=None):
    """The whole picture's last adjustments: the near corners deeper and warmer, to hold the eye in the room."""
    x0, y0, x1, y1 = rect or (0, 0, W, H)
    y, x = np.mgrid[y0:y1, x0:x1].astype(F32)
    cx = ((x - 400) / 400) ** 2
    low = np.clip((y - 440) / 160, 0, 1) ** 1.4
    top = np.clip((170 - y) / 170, 0, 1) ** 1.2
    right_top = np.clip((x - 470) / 330, 0, 1) * np.clip((230 - y) / 230, 0, 1)
    v = np.clip(cx * 0.30 * (0.35 + 0.65 * low) + low * 0.30 + top * cx * 0.30 + top * 0.10 + right_top * 0.42, 0, 0.72)
    warm = col("#5a2c20")
    out = pic * (1 - v[..., None]) + pic * warm[None, None, :] * 1.5 * v[..., None]
    grey = (out @ np.array([0.3, 0.55, 0.15], dtype=F32))[..., None]
    out = grey + (out - grey) * 1.12                                      # a little more color than a camera would give
    return np.clip(out, 0, 1)


def paint(crisp, seed=2):
    """The brush pass, and then the built things said again crisply over it: where the under-painting has an edge or
    a small thing, most of it comes back; where it is only a broad tone, the brushwork stays."""
    b = strokes(crisp, sizes=(9, 5, 2), seed=seed, density=1.5, jitter=0.042, keep=0.26)
    hf = np.abs(crisp - blur(crisp, 1.4)).sum(axis=2)
    w = np.clip(hf * 7.5 - 0.05, 0, 1)
    w = np.maximum(w, blur(w, 0.7))
    out = lerp(b, crisp, (0.12 + 0.86 * w)[..., None])
    return np.clip(out + 0.5 * (out - blur(out, 0.9)), 0, 1)             # and the whole a little sharper, as a small brush leaves it


def maps_of(st):
    """What the details pass needs to know about each pixel: how far away it is, how much it faces up, what it is."""
    return wob(st.pick(np.minimum(st.t, 5000.0))), wob(st.pick(st.N[..., 1])), wob_near(st.pick(st.oid)), st.names.get("floor", -1)


def details(pic, maps):
    """Small crisp accents that a painter adds last, found from what each pixel shows: the lit front edge of every
    top (a table top, a lid, a shelf), and a dark line where one thing stands in front of another far behind it."""
    t, ny, oid, floor_id = maps
    below_same = (np.roll(oid, -1, axis=0) == oid) & (np.roll(ny, -1, axis=0) < 0.5) & (ny > 0.9)
    below_same[-1] = False
    edge = below_same & (oid != floor_id)
    out = pic.copy()
    out[edge] = np.clip(out[edge] * 1.28 + 0.03, 0, 1)
    for ax, sh_ in ((0, 1), (0, -1), (1, 1), (1, -1)):
        tn = np.roll(t, sh_, axis=ax)
        behind = (t - tn > 14.0) & (t - tn > 0.02 * t)
        if ax == 0:
            behind[0 if sh_ == 1 else -1] = False
        else:
            behind[:, 0 if sh_ == 1 else -1] = False
        out[behind] = out[behind] * 0.74
    return out


def to_image(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def tones(a, label=""):
    """The picture's tones in numbers (the eye is easily fooled about how dark a night picture is)."""
    lum = (np.clip(a, 0, 1) * 255) @ np.array([0.3, 0.55, 0.15], dtype=F32)
    print(label, "mean", (a.mean(axis=(0, 1)) * 255).round(0), "lum 5/25/50/75/95:", np.percentile(lum, [5, 25, 50, 75, 95]).round(0))


def palette_for(px, colors, seed=3, rounds=14):
    """A palette for a night picture. Most of this room is quiet browns and blues, and what matters most in it is
    small and bright (letters, a note, a moon, book spines); a palette chosen by counting pixels would spend itself
    on the browns. So half the sample is drawn toward the colored and the light pixels, and the first choice of
    palette entries is spread as far apart as it can be (each new one the color farthest from all chosen so far),
    before the usual settling."""
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


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.007, amount=0.011):
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


def bbox(mask, pad=0):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max()) + 1 + pad, int(ys.max()) + 1 + pad]


def whole(patch, alpha, rect):
    """A patch and its coverage -> a full-size picture and mask."""
    pic = np.zeros((H, W, 3), dtype=F32)
    a = np.zeros((H, W), dtype=F32)
    x0, y0, x1, y1 = rect
    pic[y0:y1, x0:x1] = patch
    a[y0:y1, x0:x1] = alpha
    return pic, a


def clamp_rect(r, pad=6):
    return (max(0, r[0] - pad), max(0, r[1] - pad), min(W, r[2] + pad), min(H, r[3] + pad))


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "fast":
        pic, st = render(ss=1, fast=True)
        to_image(grade(pic)).save("out/home-study-2-all.png")
        print("fast", round(time.time() - t0, 1), "s;", len(st.occ), "shadow boxes;", len(st.names), "things")
        sys.exit()
    if mode == "paint":                                        # a quick look at the brushwork: one ray per pixel
        pic, st = render(ss=1, fast=True)
        out = details(paint(grade(wob(pic))), maps_of(st))
        to_image(out).save("out/home-study-2-all.png")
        tones(out, "tones:")
        print("paint", round(time.time() - t0, 1), "s")
        sys.exit()

    SS = 2
    # ---- everything in the room (the cut-outs are taken from this one)
    A, stA = render(ss=SS, fast=False)
    to_image(A).save("out/home-study-1-under.png")
    print("all", round(time.time() - t0, 1))
    # ---- the room with the desk and the foreground taken away (their shadows stay)
    B, stB = render(ss=SS, fast=False, skip=("desk", "front"), occ=stA.occ)
    print("back", round(time.time() - t0, 1))
    pA = details(paint(grade(wob(A)), 2), maps_of(stA))
    pB = details(paint(grade(wob(B)), 2), maps_of(stB))
    print("painted", round(time.time() - t0, 1))
    a_desk = wob(cover(stA, grp="desk"))
    a_front = wob(cover(stA, grp="front"))
    to_image(pA).save("out/home-study-2-all.png")
    tones(pA, "tones:")

    sizes = {}
    sizes["back"] = finish(pB, f"{OUT}/back.png", 160)
    sizes["desk"] = finish(pA, f"{OUT}/desk.png", 72, a_desk)
    sizes["front"] = finish(pA, f"{OUT}/front.png", 96, a_front)

    # ---- the small things that come and go, each painted on its own patch of the picture
    boxes = {}
    # the sticky note
    r = clamp_rect(bbox(cover(stA, name="screen") > 0.1), 22)
    P, sp = render(ss=SS, fast=False, rect=r, occ=stA.occ, note=True)
    pic, a = (wob(q) for q in whole(grade(P, r), cover(sp, grp="note"), r))
    sizes["note"] = finish(pic, f"{OUT}/note.png", 16, a, amount=0.008)
    boxes["note"] = bbox(a > 0.5)
    # what the screen shows
    for kind in ("offline", "login", "map"):
        P, sp = render(ss=SS, fast=False, rect=r, occ=stA.occ, screen=kind)
        pic, a = (wob(q) for q in whole(grade(P, r), cover(sp, grp="screen"), r))
        sizes["screen-" + kind] = finish(pic, f"{OUT}/screen-{kind}.png", 24, a, amount=0.008)
        boxes["screen"] = bbox(a > 0.5)
    # the loop of tape
    r = clamp_rect(bbox(cover(stA, name=["machine", "cabinet"]) > 0.1), 8)
    P, sp = render(ss=SS, fast=False, rect=r, occ=stA.occ, skip=("desk", "front"), tape=True)
    pic, a = (wob(q) for q in whole(grade(P, r), np.clip(cover(sp, grp="tape") * 1.7, 0, 1), r))
    sizes["tape-out"] = finish(pic, f"{OUT}/tape-out.png", 12, a, amount=0.008)
    boxes["tape"] = bbox(a > 0.5)
    # the vault with its lid up: it must cover the shut one wholly
    shut = cover(stA, name="vault") > 0.02
    r = clamp_rect(bbox(shut), 60)
    P, sp = render(ss=SS, fast=False, rect=r, occ=stA.occ, skip=("desk", "front"), vault_open=True)
    x0, y0, x1, y1 = r
    a = np.maximum(cover(sp, name="vault") > 0.5, shut[y0:y1, x0:x1]).astype(F32)
    pic, a = (wob(q) for q in whole(grade(P, r), a, r))
    sizes["vault-open"] = finish(pic, f"{OUT}/vault-open.png", 40, a, amount=0.008)
    boxes["vault-open"] = bbox(a > 0.5)
    print("cut-outs", round(time.time() - t0, 1), sizes)

    import home_study_layout
    home_study_layout.write(stA, stB, boxes, a_desk, a_front, wob)
    import subprocess
    subprocess.run([sys.executable, "comp.py", OUT, "back", "desk", "screen-offline", "note", "tape-out", "front"])
    other = Image.open(f"{OUT}/back.png").convert("RGBA")              # and the other state of everything that changes, to see that it fits
    for n in ("desk", "screen-map", "vault-open", "front"):
        other.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
    other.convert("RGB").save("out/home-study-comp-later.png")
    subprocess.run([sys.executable, "home_study_people.py"])           # the game's own figures in the room (needs the game's server)
    print("done", round(time.time() - t0, 1))

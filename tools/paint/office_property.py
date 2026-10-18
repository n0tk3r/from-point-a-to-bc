"""Property & Effects (scene `office-property`), at the Office Of Peculiar Sectors' desert field headquarters, early
afternoon (no window but Opal's, onto the hall). OFFICE-17C.

    python3 office_property.py            everything: backdrop, cut-outs and their states, layout.json, the comps
    python3 office_property.py fast       the under-painting only, one ray per pixel, hard shadows: for composing
    python3 office_property.py paint      the same with the brush pass and the details over it: for judging the look

ONE CAMERA. The room is measured in centimetres (office_property_model.py) and every pixel is a ray from the game's own
camera for this scene (room.View: horizon 290, full 436; the lens 160 cm up, turned 12 degrees to the left). What the ray
meets and how the light reaches it is worked out in the room (office_room_kit.py, office_property_things.py).

THE VIEW. The back of the room behind Opal's window: we stand among the shelves and look down the aisle to her window at
the far end. Gray steel shelving floor to ceiling on both sides, every thing on it tagged: on the left, near us, the tall
bay with the banjo standing in it (No. 3117), and over it the cowboy hat bleached white; farther along, the Roman sandal,
the clay lamp and the tin cup; near us, the gnome, the cassette, the horseshoe and the goose feather in its jar, the
lantern and the bowling ball; the archive boxes, FORM 7 by the decade. On the right, the boxes seen along their ends,
and a traffic cone. At the end of the aisle, Opal's counter and her sliding window onto the hall (lit beyond the glass,
the bell on the hall's ledge), her stool, her knitting basket with the long gray scarf trailing away over the carpet,
the small sign THIS WINDOW CLOSES AT 1700; the door to the hall at the right; a filing cabinet in the far corner. The
grille in the ceiling over the left run, near us. Near us, a cart and two boxes.

LIGHT (keep to it): fluorescent, from three light panels down the aisle: pale, a little green, flat and even; the
shelves' insides darker under each shelf, the bays deep and cool; the hall beyond the window brighter than the room, a
little of its light on the counter. Nothing else is lit.

THREE TONES. Light: the light panels, the hall through the glass, the paper, the cowboy hat. Middle: the walls, the
steel, the carpet, the boxes. Dark: inside the bays, the foreground, the duct behind the grille."""

import os
import sys
import time

import numpy as np

from brush import F32, blur, lerp
from room import View
import office_property_model as M
import office_property_things as T
from office_room_kit import (Stage, Lamp, shade, col, fbm, LUM, floor_contact, troffer_lamps, Passes, to_image, tones, letters, wall_quad,
                             pen_mask, LIGHT)

W, H = 800, 600
V = View(**M.VIEW)
OUT = "out/office-property"
WORK = "out/office-property-work"
SEED = 21
EXPOSE = 1.10
COOL_BELOW = 0.50


# ---------------------------------------------------------------- the light
def lamps():
    out = []
    power = {0: 1.15, 1: 1.05, 2: 1.0}
    for i, t in enumerate(M.TROFFERS):
        out += troffer_lamps(t, M.H, power=power[i] * 4.4, color=LIGHT, n=2, name=f"t{i}-", samples=6, reach=125.0)
    for l in out:
        l.inside_only = True
    out.append(Lamp((210, 20, 300), "#c8ccbe", 0.30, reach=300, size=120.0, wrap=0.9, shadows=False, inside_only=True, name="bounce", core=1.4))
    out.append(Lamp((260, 150, 760), "#d2ccbc", 0.45, reach=420, size=160.0, wrap=0.6, shadows=False, inside_only=True, name="nearwall", core=1.6))
    # the hall's light through the window: a soft lamp just beyond the glass, aimed into the room
    out.append(Lamp((180, 150, -30), "#e4ecd8", 0.55, reach=170, aim=(0, -0.25, 1), spread=0.25, soft=0.5, size=60.0, wrap=0.5, shadows=False,
                    inside_only=True, name="hallglow", core=1.2))
    return out


def ambient(X, Y, Z, N, st):
    """Even pale light, a little green; less inside the bays (the shelves above them) and in the corners."""
    up = N[..., 1]
    a = col("#aebcb2")[None, None, :] * 0.13
    a = a * (0.85 + 0.15 * np.clip(Y / 120.0, 0, 1))[..., None]
    a = a * (1 - 0.40 * np.clip(-up, 0, 1) * (Y > M.H - 2))[..., None]
    inbay = ((X < M.LEFT_X[1] - 1.0) & (Z > M.LEFT_Z[0][0])) | ((X > M.RIGHT_X[0] + 1.0) & (Z > M.RIGHT_Z[0][0]))
    depth_in = np.where(X < M.W / 2, np.clip((M.LEFT_X[1] - X) / 40.0, 0, 1), np.clip((X - M.RIGHT_X[0]) / 40.0, 0, 1))
    a = a * (1 - 0.35 * (inbay * depth_in))[..., None]
    corner = np.exp(-np.clip(np.minimum(np.minimum(X, M.W - X), np.maximum(Z, 0)), 0, 1e4) / 60.0) * 0.25
    a = a * (1 - corner)[..., None]
    a = a + col("#a89a80")[None, None, :] * (np.clip(-up, 0, 1) * 0.05)[..., None]
    return a


# ---------------------------------------------------------------- putting the room together
def build(st, state=None):
    s = dict(eyes=False, door_open=False, banjo=True, receipt=False)
    s.update(state or {})
    T.shell(st)
    T.hall(st)
    T.window(st, G="wall")
    T.counter(st, G="wall")
    if s["receipt"]:
        T.receipt(st, G="receipt")
    T.door_casing(st, G="wall")
    T.door_leaf(st, open_=s["door_open"], G="door")
    T.stool(st)
    T.knitting(st)
    T.cabinet(st)
    T.shelving(st)
    if s["banjo"]:
        T.banjo(st, G="banjo")
    T.ceiling_things(st, eyes=s["eyes"], G_vent="vent")
    T.front(st, G="front")


def render(ss=1, fast=True, skip=(), rect=None, occ=None, state=None):
    """-> (picture, stage). The picture is at picture size (rays averaged)."""
    st = Stage(V, ss=ss, rect=rect)
    st.skip = set(skip)
    build(st, state=state)
    pic, light = shade(st, lamps(), ambient, None, fast=fast, occ=occ, expose=EXPOSE, sh_step=1 if not fast else 2)
    X, Y, Z = st.places()
    outside = (st.flag & 4) > 0
    lum = light @ LUM
    deep = np.clip(1 - lum / COOL_BELOW, 0, 1) ** 1.3 * (~outside)
    pic = pic * (1 + deep[..., None] * np.array([-0.10, -0.02, 0.16], dtype=F32)[None, None, :])
    floor = st.mask_of("floor")
    feet = list(st.feet.values())
    dark = floor_contact(X, Z, feet, reach=6.0, amount=0.40) * floor
    dark += floor * (np.exp(-np.clip(Z, 0, 1e4) / 10.0) * 0.30 + np.exp(-np.clip(X - M.LEFT_X[1], 0, 1e4) / 10.0) * 0.30 * (Z > M.LEFT_Z[0][0])
                     + np.exp(-np.clip(M.RIGHT_X[0] - X, 0, 1e4) / 10.0) * 0.30 * (Z > M.RIGHT_Z[0][0]))
    walls = st.mask_of("back", "left", "right")
    dark += walls * np.exp(-np.clip(Y, 0, 1e4) / 6.0) * 0.20
    ceil = st.mask_of("ceiling")
    dark += ceil * (np.exp(-np.clip(X, 0, 1e4) / 14.0) * 0.25 + np.exp(-np.clip(M.W - X, 0, 1e4) / 14.0) * 0.25 + np.exp(-np.clip(Z, 0, 1e4) / 14.0) * 0.25)
    pic = pic * (1 - np.clip(dark, 0, 0.8))[..., None]
    t = np.minimum(st.t, 3000.0)
    air = np.clip((t - 550) / 500.0, 0, 1) * 0.08 * (~outside)
    pic = pic * (1 - air[..., None]) + col("#9aa0b0")[None, None, :] * air[..., None]
    fr = (st.grp == st.groups.get("front", -1))
    pic[fr] = pic[fr] * col("#d8ccbc")
    pic = st.down(pic)
    pic = glass_sheen(pic, st, rect)
    return pic, st


def glass_sheen(pic, st, rect=None):
    """Opal's window's glass: what is seen through it (the hall) a shade paler, with two soft slanting streaks of
    reflected tube light, as glass has."""
    x0, y0 = (rect[0], rect[1]) if rect else (0, 0)
    outside = st.down(((st.flag & 4) > 0).astype(F32))
    wx0, wx1, wy0, wy1 = M.WINDOW
    pts = [V.pt(X, Y, -1.0) for X in (wx0, wx1) for Y in (wy0, wy1)]
    h, w = pic.shape[:2]
    yy, xx = np.mgrid[y0:y0 + h, x0:x0 + w].astype(F32)
    ax0, ax1 = min(p[0] for p in pts), max(p[0] for p in pts)
    ay0, ay1 = min(p[1] for p in pts), max(p[1] for p in pts)
    inwin = ((xx > ax0) & (xx < ax1) & (yy > ay0) & (yy < ay1)).astype(F32) * outside
    streak = np.clip(np.sin((xx * 0.9 + yy * 0.6) * 0.055) * 1.6 - 0.9, 0, 1) * 0.10
    k = inwin * (0.06 + streak)
    return pic * (1 - k[..., None]) + col("#eef4ea")[None, None, :] * k[..., None]


def grade(pic, rect=None):
    """The near corners deeper and warmer (the foreground, the near ceiling, the near shelves), to hold the eye down
    the aisle on the window."""
    x0, y0, x1, y1 = rect or (0, 0, W, H)
    y, x = np.mgrid[y0:y1, x0:x1].astype(F32)
    cx = ((x - 440) / 440) ** 2
    low = np.clip((y - 470) / 130, 0, 1) ** 1.1
    top = np.clip((150 - y) / 150, 0, 1) ** 1.1
    v = np.clip(cx * 0.20 * (0.4 + 0.6 * low) + low * 0.26 + top * 0.18 + top * cx * 0.12, 0, 0.55)
    warm = col("#5a3828")
    out = pic * (1 - v[..., None]) + pic * warm[None, None, :] * 1.4 * v[..., None]
    grey = (out @ LUM)[..., None]
    out = grey + (out - grey) * 1.08
    return np.clip(out, 0, 1)


P = Passes(seed=SEED, grade_fn=grade)


# ---------------------------------------------------------------- the words, laid through the camera
def box_labels():
    """Where the near archive boxes' labels are (a quad on each box's end), and what each says: FORM 7, and its years."""
    return []


def words(state=None):
    out = []
    # the sign over the window: THIS WINDOW / CLOSES AT 1700
    x0, x1, y0, y1 = M.SIGN
    q = wall_quad("back", x0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, at=0.0, lift=0.7)
    m = pen_mask(["THIS WINDOW", "CLOSES AT 1700"], x1 - x0 - 3.0, y1 - y0 - 3.0, 4.6, res=16, pen=0.22, track=0.10, lead=1.30, seed=401, wobble=0.0)
    out.append((m, q, "#2a3446", 1.0, "wall"))
    # the hall's sign beyond the door: INTERVIEW ROOMS (on the hall's far wall)
    zf = -M.HALL_D + 0.3
    q = [(298.0, 170.0, zf), (394.0, 170.0, zf), (394.0, 152.0, zf), (298.0, 152.0, zf)]
    m = pen_mask(["< INTERVIEW ROOMS"], 96.0, 18.0, 8.0, res=10, pen=0.22, track=0.10, seed=402, wobble=0.0, squeeze=0.8)
    out.append((m, q, "#e8e4d8", 1.0, "hall"))
    return out


def hall_clip(st):
    return P.wob(st.down(st.mask_of("hall").astype(F32)))


def paint_full(pic, st, state=None, groups=None):
    out = P.details(P.paint(P.grade(P.wob(pic)), 2), P.maps_of(st))
    letters(out, V, words(state), groups=groups, clips={"hall": hall_clip(st)})
    return out


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode in ("fast", "paint"):
        state = {}
        for a in sys.argv[2:]:
            k, _, v = a.partition("=")
            state[k] = (v == "1")
        pic, st = render(ss=1, fast=True, state=state)
        if mode == "fast":
            to_image(grade(pic)).save(f"{WORK}/fast.png")
        else:
            out = paint_full(pic, st)
            to_image(out).save(f"{WORK}/paint.png")
            tones(out, "tones:")
        print(mode, round(time.time() - t0, 1), "s;", len(st.occ), "shadow boxes;", len(st.names), "things")
        sys.exit()
    import office_property_cuts
    office_property_cuts.main(t0)

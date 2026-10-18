"""Interview Room C, the Comfortable Room (scene `office-room`), at the Office Of Peculiar Sectors' desert field
headquarters, early afternoon (no window: it could be any time). OFFICE-17C.

    python3 office_room.py            everything: backdrop, cut-outs and their states, frames, layout.json, the comps
    python3 office_room.py fast       the under-painting only, one ray per pixel, hard shadows: for composing
    python3 office_room.py paint      the same with the brush pass and the details over it: for judging the look

ONE CAMERA. The room is measured in centimetres (office_room_model.py) and every pixel is a ray from the game's own
camera for this scene (room.View: horizon 295, full 446; the lens 165 cm up, turned 25 degrees to the right). What the
ray meets and how the light reaches it is worked out in the room (office_room_kit.py, office_room_things.py).

THE VIEW. A small room, all of it in the picture: the back wall from its near left corner (the corner chair under the
ceiling grille; the door with the clock over it; the sign, the thermostat and the intercom by the door; the poster;
the long one-way mirror) away to the far right corner, the right wall coming back toward us (the floor lamp, the water
cooler, the plastic plant); the table in the middle with Grandpa Joe's chair on its left side and Dale's and Merle's on
its right; the ceiling over all of it, with its tubes.

LIGHT (keep to it): fluorescent, from four light panels in the ceiling (two tubes each, behind prismatic lenses):
pale, a little green, flat and even, the brightest pool on the table; soft shadows straight down under the table and
the chairs; the corners and the near foreground a little darker and warmer, the far corner a little cooler; the hall
seen through the doorway a little brighter than the room. Nothing else is lit: the lamp in the corner is unplugged.

THREE TONES. Light: the light panels, the table's top, the paper, the walls near the tubes. Middle: the walls, the
carpet, the steel. Dark: the mirror (the darkest big thing), the duct behind the grille, the foreground, under the table.

HOW THE PICTURE IS MADE (the four passes of the README): render (under), Passes.paint (strokes, then every edge said
again crisply), details and words, finish (grain, a palette, speckle, PNG-8). The cut-outs are the same pixels as a
picture of the whole room; the backdrop is the room painted again without them, their shadows still lying where they
fall. The one-way mirror's reflection is the room rendered again through the mirror (a camera in the mirror's place,
the picture turned about), dimmed and cooled: faint, the tubes brightest in it."""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, blur, lerp, sample
from room import View
import office_room_model as M
import office_room_things as T
from office_room_kit import (Stage, Lamp, shade, col, fbm, LUM, floor_contact, troffer_lamps, Passes, finish, to_image, tones,
                             cover, bbox, clamp_rect, letters, wall_quad, pen_mask, LIGHT)

W, H = 800, 600
V = View(**M.VIEW)
OUT = "out/office-room"
WORK = "out/office-room-work"
SEED = 17
EXPOSE = 1.08
COOL_BELOW = 0.50                    # light weaker than this begins to turn blue-violet


# ---------------------------------------------------------------- the light
def lamps():
    out = []
    power = {0: 1.35, 1: 1.05, 2: 0.95, 3: 0.90}
    for i, t in enumerate(M.TROFFERS):
        out += troffer_lamps(t, M.H, power=power[i] * 4.4, color=LIGHT, n=3, name=f"t{i}-", samples=6, reach=125.0)
    for l in out:
        l.inside_only = True
    # what the pale room gives back: a broad soft light from the carpet up, and from the lit walls
    out.append(Lamp((280, 20, 180), "#c8ccbe", 0.36, reach=300, size=120.0, wrap=0.9, shadows=False, inside_only=True, name="bounce", core=1.4))
    # and what the lit walls round us give back: a broad soft light from our side of the room, onto faces turned to us
    out.append(Lamp((250, 150, 660), "#d2ccbc", 0.55, reach=420, size=160.0, wrap=0.6, shadows=False, inside_only=True, name="nearwall", core=1.6))
    return out


def ambient(X, Y, Z, N, st):
    """The light that is simply in a pale room under tubes: even, a little green, less in the corners and under
    things, a little less up at the ceiling."""
    up = N[..., 1]
    a = col("#aebcb2")[None, None, :] * 0.135
    a = a * (0.85 + 0.15 * np.clip(Y / 120.0, 0, 1))[..., None]
    a = a * (1 - 0.40 * np.clip(-up, 0, 1) * (Y > M.H - 2))[..., None]                   # the ceiling: lit only by what the room gives back
    corner = np.exp(-np.minimum(np.minimum(X, M.W - X), np.maximum(Z, 0)) / 60.0) * 0.30
    a = a * (1 - corner)[..., None]
    a = a + col("#a89a80")[None, None, :] * (np.clip(-up, 0, 1) * 0.06)[..., None]      # the carpet gives back to undersides
    return a


# ---------------------------------------------------------------- putting the room together
def build(st, state=None, reflection=None, mirror_view=False):
    s = dict(thermo=72, eyes=False, door_open=False, lit=False, droop=False, hand=None, questionnaire=True, bubble=None)
    s.update(state or {})
    T.shell(st)
    if not mirror_view:                     # (the camera in the mirror stands behind the back wall: nothing behind it is seen)
        T.hall(st)
        T.door_casing(st, G="doorframe")
        T.door_leaf(st, open_=s["door_open"], G="door")
    T.clock(st, hand_angle=s["hand"])
    T.sign(st)
    T.thermostat(st, G="thermostat")
    T.intercom(st, lit=s["lit"], G="intercom")
    T.poster(st)
    if not mirror_view:
        T.mirror(st, reflection=reflection)
    T.ceiling_things(st, eyes=s["eyes"], G_vent="vent")
    T.table(st, G="table")
    if s["questionnaire"]:
        T.questionnaire(st, G="questionnaire")
    T.chairs(st, G_corner="chair-corner")
    T.cooler(st, bubble=s["bubble"])
    T.lamp(st)
    T.plant(st, droop=s["droop"], G="plant")
    T.basket(st, G="front")
    T.filebox(st, G="front")


def render(ss=1, fast=True, skip=(), rect=None, occ=None, state=None, reflection=None, view=None, mirror_view=False):
    """-> (picture, stage). The picture is at picture size (rays averaged)."""
    v = view or V
    st = Stage(v, ss=ss, rect=rect)
    st.skip = set(skip)
    build(st, state=state, reflection=reflection, mirror_view=mirror_view)
    pic, light = shade(st, lamps(), ambient, None, fast=fast, occ=occ, expose=EXPOSE, sh_step=1 if not fast else 2)
    X, Y, Z = st.places()
    outside = (st.flag & 4) > 0
    lum = light @ LUM
    deep = np.clip(1 - lum / COOL_BELOW, 0, 1) ** 1.3 * (~outside)
    pic = pic * (1 + deep[..., None] * np.array([-0.10, -0.02, 0.16], dtype=F32)[None, None, :])
    floor = st.mask_of("floor")
    feet = list(st.feet.values())
    dark = floor_contact(X, Z, feet, reach=6.0, amount=0.45) * floor
    dark += floor * (np.exp(-np.clip(Z, 0, 1e4) / 10.0) * 0.30 + np.exp(-np.clip(X, 0, 1e4) / 10.0) * 0.30 + np.exp(-np.clip(M.W - X, 0, 1e4) / 10.0) * 0.28)
    walls = st.mask_of("back", "left", "right")
    dark += walls * np.exp(-np.clip(Y, 0, 1e4) / 6.0) * 0.20
    ceil = st.mask_of("ceiling")
    dark += ceil * (np.exp(-np.clip(X, 0, 1e4) / 14.0) * 0.25 + np.exp(-np.clip(Z, 0, 1e4) / 14.0) * 0.25)       # the ceiling's edges, along the walls
    pic = pic * (1 - np.clip(dark, 0, 0.8))[..., None]
    # depth by tone: the far end a little paler and cooler
    t = np.minimum(st.t, 3000.0)
    air = np.clip((t - 600) / 500.0, 0, 1) * 0.08 * (~outside)
    pic = pic * (1 - air[..., None]) + col("#9aa0b0")[None, None, :] * air[..., None]
    fr = (st.grp == st.groups.get("front", -1))
    pic[fr] = pic[fr] * col("#e0d4c4")
    return st.down(pic), st


def grade(pic, rect=None):
    """The whole picture's last adjustments: the near corners (the foreground, the near ceiling) deeper and warmer, to
    hold the eye in the room and on the table."""
    x0, y0, x1, y1 = rect or (0, 0, W, H)
    y, x = np.mgrid[y0:y1, x0:x1].astype(F32)
    cx = ((x - 430) / 430) ** 2
    low = np.clip((y - 460) / 140, 0, 1) ** 1.1
    top = np.clip((170 - y) / 170, 0, 1) ** 1.1
    v = np.clip(cx * 0.18 * (0.4 + 0.6 * low) + low * 0.30 + top * 0.20 + top * cx * 0.14, 0, 0.55)
    warm = col("#5a3828")
    out = pic * (1 - v[..., None]) + pic * warm[None, None, :] * 1.4 * v[..., None]
    grey = (out @ LUM)[..., None]
    out = grey + (out - grey) * 1.08
    return np.clip(out, 0, 1)


P = Passes(seed=SEED, grade_fn=grade)


# ---------------------------------------------------------------- the one-way mirror's reflection
def mirror_view():
    """The camera in the mirror: the lens reflected through the back wall's plane (Z = 0), turned to look back into the
    room. Its picture, turned about (left for right), is what the mirror shows."""
    vw = dict(M.VIEW)
    vw["cam"] = (M.VIEW["cam"][0], -M.VIEW["cam"][1])
    vw["yaw"] = 180.0 - M.VIEW["yaw"]
    return View(**vw)


def reflection_image(ss=1, fast=True):
    """The room as the mirror shows it, at picture size, over the mirror's own patch of the picture (else black)."""
    x0, x1, y0, y1 = M.MIRROR
    pts = [V.pt(X, Y, 0.0) for X in (x0, x1) for Y in (y0, y1)]
    bx0, bx1 = int(min(p[0] for p in pts)) - 3, int(max(p[0] for p in pts)) + 4
    by0, by1 = int(min(p[1] for p in pts)) - 3, int(max(p[1] for p in pts)) + 4
    bx0, bx1, by0, by1 = max(bx0, 0), min(bx1, W), max(by0, 0), min(by1, H)
    r = (W - bx1, by0, W - bx0, by1)                          # the same patch in the turned-about picture
    pic, st = render(ss=ss, fast=fast, rect=r, view=mirror_view(), mirror_view=True)
    full = np.zeros((H, W, 3), F32)
    full[by0:by1, bx0:bx1] = pic[:, ::-1]
    return full


def reflection_fn(img, amount=0.38):
    """(X, Y, Z) on the glass -> the reflection seen there: the room through the mirror, dimmed and cooled, the tubes
    brightest."""
    tint = col("#a8b4cc")

    def f(X, Y, Z):
        xs, ys = [], []
        a, u, d = V.cam_space(X, Y, Z)
        px = V.cx + a * V.F / d
        py = V.hz - u * V.F / d
        rgb = sample(img, np.asarray(px, F32) - 0.5, np.asarray(py, F32) - 0.5)
        lum = rgb @ LUM
        k = amount * (0.55 + 0.45 * np.clip((lum - 0.55) * 2.5, 0, 1))
        return rgb * tint * k[..., None]
    return f


# ---------------------------------------------------------------- the words, laid through the camera
def words(state=None):
    """Every word in the room that must be read, as (mask, quad in the room, ink, how strong, group)."""
    s = dict(thermo=72)
    s.update(state or {})
    out = []
    # the sign by the door: INTERVIEW / ROOM C on the brown band (cream letters), then the rest in brown on beige
    x0, x1, y0, y1 = M.SIGN
    w_, h_ = x1 - x0, y1 - y0
    q = wall_quad("back", x0 + 1.5, x1 - 1.5, y1 - 23.0, y1 - 1.0, at=1.0, lift=0.1)
    m = pen_mask(["INTERVIEW", "ROOM C"], w_ - 3.0, 22.0, 8.4, res=12, pen=0.21, track=0.12, lead=1.25, seed=101, wobble=0.0)
    out.append((m, q, "#f2e8cc", 1.0, "back"))
    # (three lines, so that the letters can be big enough to read: 7 px and more)
    q = wall_quad("back", x0 + 2.0, x1 - 2.0, y0 + 11.0, y1 - 26.0, at=1.0, lift=0.1)
    m = pen_mask(["THE", "COMFORTABLE", "ROOM"], w_ - 4.0, h_ - 37.0, 7.8, res=12, pen=0.20, track=0.10, lead=1.30, seed=102, wobble=0.0)
    out.append((m, q, "#5a3c2a", 1.0, "back"))
    q = wall_quad("back", x0 + 2.0, x1 - 2.0, y0 + 1.5, y0 + 10.0, at=1.0, lift=0.1)
    m = pen_mask(["THIS ROOM HAS BEEN", "RATED COMFORTABLE"], w_ - 4.0, 8.5, 3.0, res=24, pen=0.18, track=0.12, lead=1.35, seed=103, wobble=0.0)
    out.append((m, q, "#6a4c38", 1.0, "back"))
    # the thermostat's number, in its window (one state for each)
    tx0, tx1, ty0, ty1 = M.THERMO
    wx0, wx1, wy0, wy1 = tx0 + 12.0, tx1 - 2.5, ty0 + 4.0, ty1 - 3.0
    q = wall_quad("back", wx0, wx1, wy0, wy1, at=4.0, lift=0.1)
    m = pen_mask([str(s["thermo"])], wx1 - wx0, wy1 - wy0, 10.5, res=14, pen=0.22, track=0.12, seed=104, wobble=0.0, squeeze=0.80)
    out.append((m, q, "#1c1a18" if s["thermo"] < 80 else "#a8241c", 1.0, "thermostat"))
    # the intercom's label: DISPATCH / PRESS TO TALK (small: the look says it)
    ix0, ix1, iy0, iy1 = M.INTERCOM
    q = wall_quad("back", ix0 + 2.0, ix1 - 2.0, iy0 + 3.0, iy0 + 8.0, at=2.0, lift=0.1)
    m = pen_mask(["DISPATCH", "PRESS TO TALK"], ix1 - ix0 - 4.0, 5.0, 1.9, res=40, pen=0.20, track=0.12, lead=1.3, seed=105, wobble=0.0)
    out.append((m, q, "#2a2a30", 1.0, "intercom"))
    # the poster: PECULIAR? over the picture, REPORT IT. under it
    px0, px1, py0, py1 = M.POSTER
    q = wall_quad("back", px0 + 2.0, px1 - 2.0, py1 - 21.0, py1 - 2.0, at=0.3, lift=0.1)
    m = pen_mask(["PECULIAR?"], px1 - px0 - 4.0, 19.0, 11.0, res=12, pen=0.24, track=0.08, seed=106, wobble=0.0, squeeze=0.88)
    out.append((m, q, "#b8302a", 1.0, "back"))
    q = wall_quad("back", px0 + 3.0, px1 - 3.0, py0 + 2.0, py0 + 15.0, at=0.3, lift=0.1)
    m = pen_mask(["REPORT IT."], px1 - px0 - 6.0, 13.0, 8.0, res=12, pen=0.24, track=0.10, seed=107, wobble=0.0, squeeze=0.9)
    out.append((m, q, "#24304c", 1.0, "back"))
    # the box of spare questionnaires near us: its stencilled label
    q = T.filebox_label()
    lw = M.FILEBOX[1] - M.FILEBOX[0] - 6.0
    m = pen_mask(["QUESTIONNAIRE", "FORM 7-C  47 PP."], lw, 18.0, 5.6, res=14, pen=0.22, track=0.12, lead=1.45, seed=109, wobble=0.0)
    out.append((m, q, "#3a2a1e", 1.0, "front"))
    # the hall's sign, through the doorway: an arrow and PROPERTY & EFFECTS (on the hall's far wall)
    q = [(62.0, 158.0, -T.HALL_D + 0.3), (148.0, 158.0, -T.HALL_D + 0.3), (148.0, 134.0, -T.HALL_D + 0.3), (62.0, 134.0, -T.HALL_D + 0.3)]
    m = pen_mask(["PROPERTY & EFFECTS >"], 86.0, 24.0, 7.0, res=10, pen=0.22, track=0.10, seed=108, wobble=0.0, squeeze=0.8)
    out.append((m, q, "#e8e4d8", 1.0, "hall"))
    return out


# ---------------------------------------------------------------- the modes
def hall_clip(st):
    """Where the hall's far wall is seen (through the doorway, the door open): its sign is laid there and nowhere else."""
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
        refl = reflection_image(ss=1, fast=True)
        pic, st = render(ss=1, fast=True, reflection=reflection_fn(refl))
        if mode == "fast":
            to_image(grade(pic)).save(f"{WORK}/fast.png")
        else:
            out = paint_full(pic, st)
            to_image(out).save(f"{WORK}/paint.png")
            tones(out, "tones:")
        print(mode, round(time.time() - t0, 1), "s;", len(st.occ), "shadow boxes;", len(st.names), "things")
        sys.exit()
    import office_room_cuts
    office_room_cuts.main(t0)

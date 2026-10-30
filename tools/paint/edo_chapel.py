"""The room under the charcoal-burner's storehouse (edo-chapel), by oil lamp. Night, spring rain above; and the
morning after, with the sun down the open trapdoor. PAINT-20F (round twenty).

    python3 edo_chapel.py          everything: backdrop, cut-outs, layout.json, the comps (a few minutes)
    python3 edo_chapel.py fast     the under-painting only, one ray per pixel, hard shadows (10 s); `fast open day out`
    python3 edo_chapel.py paint    the same with the brush pass and the keyblock over it (20 s)

ONE CAMERA, inside the room's height (edo_chapel_model.py: horizon 243, full 362, the lens 130 cm up under a ceiling
of 182), so the earth ceiling, its beams and the trapdoor press down over the people. The ray-caster is the study's
(home_study_kit); the shell, the things and the sun are this room's (edo_chapel_things.py).

THE LOOK is the act's (S/work-20-paintA/style.md): flats, not modelled forms. The ray-caster works out where the
lamps' light falls; the light is then cut into FOUR FLATS (lit, half, shade, deep) with hard edges between them, and
each flat is a colour: the lit flat the thing's own paint warmed with naples yellow, the half flat the paint, the shade
flat the paint pulled toward ultramarine, the deep toward prussian blue. No gradient crosses a plane. The one fine
prussian contour (the keyblock) is drawn after the brush pass along every silhouette (where the depth jumps, and where
a face turns), 1 px near, thinner and fainter far. Chrome yellow only at the flames' oil.

LIGHT (keep to it):
  - three small clay oil lamps: one on a ledge in the left wall by the ladder's foot, one on a lamp stand on the floor
    before the altar's left side (it lights the altar's front and the Kannon when the doors are open), one in a niche
    in the back wall right of the mirror. Naples-yellow pools; the shade goes blue (ultramarine toward prussian).
    The flames themselves are the engine's (fx `flame`): the painting has the lamps alight but no tongue.
  - at morning (the state `trapdoor-day`): a cool shaft of daylight down the open trapdoor (cerulean and lead white),
    landing on the mats at SUNPATCH, the ladder's upper rungs in it.
THREE TONES. Dark: the ceiling and beams, the near corners, the foreground. Middle: the earth walls and the floor.
Light: the lamps' pools, the Kannon when the doors are open (the brightest small thing), the mirror's face, and, at
morning, the sun on the mats.
The four passes are the study's: render, brush, details, finish."""

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
import edo_chapel_model as M
import edo_chapel_things as T
from home_study_kit import Stage, Lamp, shade, seg_hits, col, floor_contact
from home_study import finish, to_image, tones, bbox, whole, clamp_rect
from postimp_paints import PAINTS

W, H = 800, 600
V = View(**M.VIEW)
OUT = "out/edo-chapel"
SEED = 2031
EXPOSE = 1.7
SUN_COLOR = (0.80, 0.90, 1.0)
SUN_POWER = 2.6
PRUSSIAN = col(PAINTS["prussian-blue"]["hex"])
ULTRA = col(PAINTS["ultramarine"]["hex"])
COBALT = col(PAINTS["cobalt-blue"]["hex"])
NAPLES = col(PAINTS["naples-yellow"]["hex"])
PAPER = col(PAINTS["lead-white"]["hex"])
# the four flats: the light's luminance below which a place is in each, and what each does to the paint
FLATS = [(0.20, 0.12, 0.80), (0.50, 0.28, 0.55), (1.05, 0.58, 0.22), (9.0, 1.1, -0.2)]   # (up to, level, pull: toward blue if > 0, toward naples if < 0)


# ---------------------------------------------------------------- the light
def lamps(lit=True):
    out = []
    for name, pos in T.lamp_places().items():
        p = (pos[0], pos[1] + 2.0, pos[2])
        power = 0.85 if name == "lamp-stand" else 1.15                      # the stand's lamp is low: a smaller pool on the mats
        out.append(Lamp(p, "#f6e0a8", power if lit else 0.2, reach=110, size=3.2, fill=0.05, samples=5))
    # the lit mats give a little warm light back to the undersides of things, and to the foreground
    out.append(Lamp((250, 30, 170), "#f0d8a8", 0.62 if lit else 0.1, reach=250, shadows=False, wrap=0.6, fill=0.0, size=30.0))
    return out


def ambient(X, Y, Z, N):
    """The dark that is simply in the room: blue, a shade warmer low down where the mats give light back."""
    up = 0.5 + 0.5 * N[..., 1]
    a = col("#3c4a9a")[None, None, :] * (0.075 * (0.85 + 0.15 * up))[..., None]
    a = a + col("#a08050")[None, None, :] * (0.04 * (1 - up))[..., None]
    return a.astype(F32)


def sunlight(st, occ, fast):
    """The morning sun down the open hatch: for every ray's place, is the hatch's opening on its line to the sun?"""
    d = np.asarray(M.SUN_DIR, dtype=np.float64)
    d /= np.linalg.norm(d)
    X, Y, Z = st.places()
    N = st.N
    ss, o = st.ss, st.ss // 2
    Xs, Ys, Zs, Ns = X[o::ss, o::ss], Y[o::ss, o::ss], Z[o::ss, o::ss], N[o::ss, o::ss]
    Ps = (Xs + Ns[..., 0] * 0.7, Ys + Ns[..., 1] * 0.7, Zs + Ns[..., 2] * 0.7)
    hx0, hx1, hz0, hz1 = M.HATCH
    tt = (M.H - Ps[1]) / (-d[1])
    Qx, Qz = Ps[0] - tt * d[0], Ps[2] - tt * d[2]
    hit = (st.t < 9e8)[o::ss, o::ss]
    ndl_s = np.clip(-(Ns[..., 0] * d[0] + Ns[..., 1] * d[1] + Ns[..., 2] * d[2]), 0, 1)
    through = (tt > 0) & (Qx > hx0) & (Qx < hx1) & (Qz > hz0) & (Qz < hz1) & (ndl_s > 0) & hit
    vis = np.zeros(through.shape, dtype=F32)
    if through.any():
        Pa = tuple(p[through] for p in Ps)
        Qa = (Qx[through], np.full(Pa[0].shape, M.H + 0.5, dtype=F32), Qz[through])
        blocked = seg_hits(Pa, Qa, occ, 0.0)
        vis[through] = np.where(blocked, 0.0, 1.0)
    vis = blur(vis, 0.6 if fast else 0.9)
    vis = np.repeat(np.repeat(vis, ss, axis=0), ss, axis=1) if ss > 1 else vis
    ndl = np.clip(-(N[..., 0] * d[0] + N[..., 1] * d[1] + N[..., 2] * d[2]), 0, 1)
    return (vis * ndl * SUN_POWER)[..., None] * col(SUN_COLOR)[None, None, :], vis * ndl


def flats(light, sun):
    """The light cut into the four flats: -> (the light's level, flat; which flat each ray is in; the sun's own flat)."""
    lum = light @ np.array([0.3, 0.55, 0.15], dtype=F32)
    level = np.zeros(lum.shape, dtype=F32)
    pull = np.zeros(lum.shape, dtype=F32)
    done = np.zeros(lum.shape, dtype=bool)
    which = np.zeros(lum.shape, dtype=np.int8)
    for k, (upto, lv, pl) in enumerate(FLATS):
        m = ~done & (lum < upto)
        level[m], pull[m], which[m] = lv, pl, k
        done |= m
    sunlit = sun > 0.35
    which[sunlit] = 4
    return level, pull, which, sunlit


# ---------------------------------------------------------------- putting the room together
def render(ss=1, fast=True, skip=(), rect=None, occ=None, **state):
    """-> (picture, stage). The picture is at picture size (rays averaged)."""
    st = Stage(V, ss=ss, rect=rect)
    st.skip = set(skip)
    T.build(st, **state)
    lit = state.get("lit", True)
    _, light = shade(st, lamps(lit), ambient, None, None, fast=fast, occ=occ, expose=EXPOSE)
    occ_ = st.occ if occ is None else occ
    st.sunlit = np.zeros(light.shape[:2], dtype=F32)
    sun_k = np.zeros(light.shape[:2], dtype=F32)
    if state.get("trap") == "day":
        sun, sun_k = sunlight(st, occ_, fast)
        st.sunlit = sun_k
    hit = st.t < 9e8
    X, Y, Z = st.places()
    # ---- the four flats
    level, pull, which, sunlit = flats(light * EXPOSE, sun_k)
    lamp_hue = light / (light @ np.array([0.3, 0.55, 0.15], dtype=F32) + 1e-4)[..., None]           # the light's colour, at level 1
    lamp_hue = np.clip(lamp_hue, 0.6, 1.4)
    pic = st.alb * (level[..., None] * lamp_hue)
    warm = np.clip(-pull, 0, 1)[..., None]
    pic = lerp(pic, pic * (NAPLES / NAPLES.max())[None, None, :], warm)                        # the lit flat: naples' warmth
    cool = np.clip(pull, 0, 1)
    toblue = np.where((which == 0)[..., None], PRUSSIAN[None, None, :], lerp(ULTRA, COBALT, 0.25)[None, None, :])
    pic = lerp(pic, pic * 0.45 + toblue * level[..., None] * 1.6, cool[..., None])                     # the shade flats: the paint pulled to blue
    # the sun's flat: lead white and cerulean, flat
    sunc = lerp(PAPER, col(PAINTS["cerulean"]["hex"]), 0.22)
    pic = np.where(sunlit[..., None], lerp(st.alb * 1.25, sunc[None, None, :], 0.55), pic)
    pic = pic + st.emi
    pic = 1 - np.exp(-pic * 1.25)
    pic = np.where(hit[..., None], pic, 0).astype(F32)
    floor = st.mask_of("floor")
    feet = [f for name, f in st.feet.items()]
    # things sit on the floor: a flat of shadow round every foot (a hard edge, no gradient)
    dark = (floor_contact(st, X, Z, feet, reach=9.0, amount=1.0) > 0.33).astype(F32) * floor * 0.5
    # the corners gather the deep blue: where the walls meet the floor and the ceiling
    dark += floor * ((np.exp(-np.clip(Z, 0, 1e4) / 14.0) > 0.4) * 0.3 + (np.exp(-np.clip(X, 0, 1e4) / 12.0) > 0.4) * 0.28 + (np.exp(-np.clip(M.W - X, 0, 1e4) / 12.0) > 0.4) * 0.28)
    wallish = st.mask_of("back", "left", "right")
    dark += wallish * ((np.exp(-np.clip(Y, 0, 1e4) / 9.0) > 0.4) * 0.22 + (np.exp(-np.clip(M.H - Y, 0, 1e4) / 10.0) > 0.4) * 0.26)
    dark = np.clip(dark, 0, 0.6)[..., None]
    pic = lerp(pic, pic * 0.5 + PRUSSIAN[None, None, :] * 0.12, dark)
    # the foreground is darker and bluer than the middle of the room (people pass behind it)
    fr = (st.grp == st.groups.get("front", -1))
    pic[fr] = lerp(pic[fr], pic[fr] * 0.6 + PRUSSIAN * 0.1, 0.5)
    st.which = which
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


def grade(pic, rect=None):
    """The whole picture's last adjustments: the near corners and the top (the near ceiling) deeper and BLUER, to hold
    the eye in the room and send it to the altar; a little more colour than a camera would give."""
    x0, y0, x1, y1 = rect or (0, 0, W, H)
    y, x = np.mgrid[y0:y1, x0:x1].astype(F32)
    cx = ((x - 400) / 400) ** 2
    low = np.clip((y - 430) / 170, 0, 1) ** 1.4
    top = np.clip((150 - y) / 150, 0, 1) ** 1.1
    v = np.clip(cx * 0.30 * (0.35 + 0.65 * low) + low * 0.28 + top * cx * 0.25 + top * 0.20, 0, 0.7)
    out = pic * (1 - v[..., None]) + (pic * 0.55 + PRUSSIAN[None, None, :] * 0.14) * v[..., None]
    grey = (out @ np.array([0.3, 0.55, 0.15], dtype=F32))[..., None]
    out = grey + (out - grey) * 1.08
    return np.clip(out, 0, 1)


def maps_of(st):
    return (wob(st.pick(np.minimum(st.t, 5000.0))), wob(st.pick(st.N)), wob_near(st.pick(st.oid)), st.names.get("floor", -1),
            wob_near(st.pick(st.which)))


def paint(crisp, seed=2):
    """The brush pass at the indoor sizes, and the flats said again over it (keep 0.26): where the under-painting has an
    edge, most of it comes back; where it is only a flat, the brushwork stays."""
    b = strokes(crisp, sizes=(9, 5, 2), seed=seed, density=1.5, jitter=0.03, keep=0.26)
    hf = np.abs(crisp - blur(crisp, 1.4)).sum(axis=2)
    w = np.clip(hf * 7.5 - 0.05, 0, 1)
    w = np.maximum(w, blur(w, 0.7))
    out = lerp(b, crisp, (0.12 + 0.86 * w)[..., None])
    return np.clip(out + 0.4 * (out - blur(out, 0.9)), 0, 1)


def keyblock(pic, maps):
    """The one fine contour, in prussian blue, as the keyblock prints it: along every silhouette (where the depth jumps:
    a thing in front of what is behind it) and where a face turns (a beam's edge, the altar's corner); 1 px and alpha
    0.85 near, 0.7 px and 0.6 far. Not inside a flat, not between the flats of the light, not on the floor's or a wall's
    own plane. And the lit edge of every top, as before."""
    t, N, oid, floor_id, which = maps
    out = pic.copy()
    edge = np.zeros(t.shape, dtype=F32)
    for ax, sh_ in ((0, 1), (0, -1), (1, 1), (1, -1)):
        tn = np.roll(t, sh_, axis=ax)
        Nn = np.roll(N, sh_, axis=ax)
        on = np.roll(oid, sh_, axis=ax)
        jump = (t - tn > 8.0) & (t - tn > 0.025 * t)                        # this pixel is farther: the near thing's edge lies here
        turn = ((N - Nn) ** 2).sum(axis=2) > 0.6                            # a face turns
        m = jump | (turn & (np.abs(t - tn) < 40))
        if ax == 0:
            m[0 if sh_ == 1 else -1] = False
        else:
            m[:, 0 if sh_ == 1 else -1] = False
        edge = np.maximum(edge, m.astype(F32))
    near = np.clip((900 - t) / 500.0, 0, 1)                                 # 1 near, 0 far
    alpha = edge * (0.55 + 0.3 * near)
    out = lerp(out, PRUSSIAN[None, None, :], alpha[..., None])
    return out


def painted(P, st, seed=2):
    return keyblock(paint(grade(wob(P)), seed), maps_of(st))


def cover(st, grp=None, name=None):
    if grp is not None:
        m = st.grp == st.groups.get(grp, -1)
    else:
        m = st.mask_of(*([name] if isinstance(name, str) else name))
    return st.down(m.astype(F32))


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode in ("fast", "paint"):
        state = {}
        for a in sys.argv[2:]:                                     # e.g. python3 edo_chapel.py fast open day
            state.update({"open": {"doors_open": True}, "day": {"trap": "day"}, "lamp": {"trap": "lamp"}, "out": {"lit": False}}.get(a, {}))
        pic, st = render(ss=1, fast=True, **state)
        out = grade(pic) if mode == "fast" else painted(pic, st)
        to_image(out).save("out/edo-chapel-2-all.png")
        tones(out, "tones:")
        print(mode, round(time.time() - t0, 1), "s;", len(st.occ), "shadow boxes;", len(st.names), "things")
        sys.exit()

    SS = 2
    CUTS = ("altar", "mirror", "ladder", "props", "front", "lamps")
    # ---- everything in the room, as it is first seen (the cut-outs are taken from this one)
    A, stA = render(ss=SS, fast=False)
    to_image(A).save("out/edo-chapel-1-under.png")
    print("all", round(time.time() - t0, 1))
    # ---- the room with every cut-out taken away (their shadows stay); the hatch open on the dark storehouse under the trapdoor's states
    B, stB = render(ss=SS, fast=False, skip=CUTS, occ=stA.occ, trap="lamp")
    print("back", round(time.time() - t0, 1))
    # ---- the morning: the sun down the open hatch
    D, stD = render(ss=SS, fast=False, trap="day")
    print("day", round(time.time() - t0, 1))
    pA, pB, pD = painted(A, stA), painted(B, stB), painted(D, stD)
    print("painted", round(time.time() - t0, 1))
    to_image(pA).save("out/edo-chapel-2-all.png")
    tones(pA, "tones:")

    # ---- the room by night with the hatch open: the ladder's top shows through the hole (the night ladder is taken from this one)
    AL, stAL = render(ss=SS, fast=False, trap="lamp")
    pAL = painted(AL, stAL)
    print("night, open", round(time.time() - t0, 1))

    sizes, boxes = {}, {}
    sizes["back"] = finish(pB, f"{OUT}/back.png", 160, amount=0.02)
    for grp, name, colors in (("altar", "altar-shut", 64), ("mirror", "mirror", 24), ("props", "props", 40),
                              ("front", "front", 72), ("lamps", "lamps", 32)):
        a = wob(cover(stA, grp=grp))
        sizes[name] = finish(pA, f"{OUT}/{name}.png", colors, a, amount=0.02)
        boxes[name] = bbox(a > 0.5)
    # the hatch's three states share one alpha (the union of what each shows), so that each covers the others exactly
    a_hatch = np.maximum.reduce([wob(cover(stA, grp="hatch")), wob(cover(stB, grp="hatch")), wob(cover(stD, grp="hatch"))])
    sizes["trapdoor-shut"] = finish(pA, f"{OUT}/trapdoor-shut.png", 48, a_hatch, amount=0.02)
    sizes["trapdoor-lamp"] = finish(pB, f"{OUT}/trapdoor-lamp.png", 40, a_hatch, amount=0.02)
    boxes["trapdoor-shut"] = boxes["trapdoor-lamp"] = bbox(a_hatch > 0.5)
    # the ladder, by night (its top through the open hole) and in the morning sun: one alpha for both
    a_ladder = np.maximum(wob(cover(stAL, grp="ladder")), wob(cover(stD, grp="ladder")))
    sizes["ladder"] = finish(pAL, f"{OUT}/ladder.png", 48, a_ladder, amount=0.02)
    boxes["ladder"] = bbox(a_ladder > 0.5)
    # the day: the open hatch bright, and the sun's flat on the mats and the floor (the back plane), cropped to the light's
    # own box; the ladder in the sun is its own state
    back_px = wob(cover(stD, grp="back")) > 0.5
    sunlit = wob(stD.down((stD.which == 4).astype(F32))) > 0.3
    sb = bbox(sunlit & back_px, pad=4) or [0, 0, 0, 0]
    inbox = np.zeros((H, W), dtype=bool)
    inbox[max(0, sb[1]):sb[3], max(0, sb[0]):sb[2]] = True
    diff = np.abs(pD - pA).sum(axis=2) > 0.08
    a_day = np.maximum(a_hatch, ((sunlit | (diff & inbox)) & back_px).astype(F32))
    a_day = np.maximum(a_day, (blur(a_day, 1.0) > 0.3).astype(F32))
    sizes["trapdoor-day"] = finish(pD, f"{OUT}/trapdoor-day.png", 64, a_day, amount=0.02)
    boxes["trapdoor-day"] = bbox(a_day > 0.5)
    sizes["ladder-day"] = finish(pD, f"{OUT}/ladder-day.png", 48, a_ladder, amount=0.02)
    boxes["ladder-day"] = bbox(a_ladder > 0.5)
    # ---- the altar with its doors open: it must cover the shut one wholly
    shut = cover(stA, grp="altar") > 0.02
    r = clamp_rect(bbox(shut), 70)
    P, sp = render(ss=SS, fast=False, rect=r, occ=stA.occ, doors_open=True)
    x0, y0, x1, y1 = r
    a = np.maximum(cover(sp, grp="altar") > 0.5, shut[y0:y1, x0:x1]).astype(F32)
    pic, a = (wob(q) for q in whole(grade(P, r), a, r))
    pic = keyblock(paint(pic), maps_of(stA))
    sizes["altar-open"] = finish(pic, f"{OUT}/altar-open.png", 72, a, amount=0.02)
    boxes["altar-open"] = bbox(a > 0.5)
    for nm in ("kannon", "calendar", "bowl"):
        m = np.zeros((H, W), dtype=F32)
        m[y0:y1, x0:x1] = cover(sp, name=nm)
        boxes[nm] = bbox(wob(m) > 0.5)
    # ---- the lamps cold
    r = clamp_rect(bbox(cover(stA, grp="lamps") > 0.02), 12)
    P, sp = render(ss=SS, fast=False, rect=r, occ=stA.occ, lit=False)
    pic, a = (wob(q) for q in whole(grade(P, r), cover(sp, grp="lamps"), r))
    sizes["lamps-out"] = finish(pic, f"{OUT}/lamps-out.png", 24, a, amount=0.012)
    boxes["lamps-out"] = bbox(a > 0.5)
    print("cut-outs", round(time.time() - t0, 1), sizes)

    import edo_chapel_layout
    edo_chapel_layout.write(stA, stB, stD, boxes, wob)
    subprocess.run([sys.executable, "comp.py", OUT, "back", "props", "trapdoor-shut", "altar-shut", "mirror", "lamps", "ladder", "front"])
    for label, names in (("open", ("back", "props", "trapdoor-lamp", "altar-open", "mirror", "lamps", "ladder", "front")),
                         ("day", ("back", "props", "trapdoor-day", "altar-open", "lamps", "ladder-day", "front")),
                         ("out", ("back", "props", "trapdoor-shut", "altar-shut", "mirror", "lamps-out", "ladder", "front"))):
        im = Image.open(f"{OUT}/{names[0]}.png").convert("RGBA")
        for n in names[1:]:
            im.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
        im.convert("RGB").save(f"out/edo-chapel-comp-{label}.png")
    print("done", round(time.time() - t0, 1))

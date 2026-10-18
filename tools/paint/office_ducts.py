"""The air ducts over the Office's ground floor (office-ducts, OFFICE-17B; painted again in OFFICE-17B2): Ranger's world,
as a cut-away.

    python3 office_ducts.py          everything: the backdrop, the fan's frames, layout.json, the comps (two minutes)
    python3 office_ducts.py fast     the under-painting only, one ray per pixel, hard shadows: for composing (20 s)
    python3 office_ducts.py paint    the same with the brush pass over it: for judging the look
    python3 office_ducts.py layout   layout.json alone, measured again from the geometry (no light, no paint: a few
                                     seconds); the same numbers as the full run's, for a change to office_ducts_layout.py only
    python3 office_ducts_check.py [folder]    the checks, and the pictures to look at (Ranger at every mark, the grille's
                                     view over three rooms): out/office-ducts-check/

A CUT-AWAY, LIKE AN ARCHITECT'S SECTION: a sheet-metal tube, cut open along its near side, with a raccoon in it, over
the rooms. The building's ceiling space is cut through by one plane; the near side of the long duct is taken away with
everything nearer us, so that we see into the duct and Ranger walks left and right along its floor. Where the plane
cuts a wall of the duct (and of the intake run and the B-7 shaft, which are cut the same way) it shows a band: the cut
sheet bright on the tube's inside, a thin hatched core, the outer sheet dark; so the cut is one clean outline round the
tubes, painted as drawn. ONE CAMERA (room.View: horizon 333, full 470, focal 600; the measurements in
office_ducts_model.py): every pixel is a ray, and what it meets is lit from where the light really is
(office_ducts_kit.py). Ranger walks the middle of the duct's floor on the row 470, at exactly his painted size; the
duct's inside is 3.5 times his height.

LIGHT (keep to it; OFFICE-17B2):
  - the duct is the brightest, clearest thing: the rooms' fluorescent light, warm white with a little green, up through
    each of its four grilles, in bars up its back wall to its top, and round the metal inside it; each boot glows;
  - daylight down the intake run at the left, from the rooftop unit's open grille at its top, past the intake fan,
    still; dimmer down the run;
  - the light fittings glowing up between the tiles: the two the plane cuts show their tubes alight, and their light
    falls in soft fans into the rooms under the tiles' cut line (the rooms are not drawn: seen only through the grilles);
    the ones behind the duct fan up the far wall;
  - in the B-7 shaft a little light from its cap on the roof, a caged bulb over the duct's mouth, and more light from far
    below (the way down);
  - the ceiling space round the duct dim but readable; what no light reaches is blue-violet, never black.

THREE TONES. Light: the duct's inside, its grilles and bars, the intake's daylight, the fittings' tubes and the fans of
their light, the shaft below the fan. Middle: the run, the shaft, the pink insulation, the tiles' backs, the pipes.
Dark: the ceiling space's far wall and the joists up under the deck, the rooms' dark under the tiles' line; and the
cut's hatched bands, which outline everything.

CUT-OUTS. Nothing is in front of the duct: the cut is the front. The B-7 fan's blades and hub are the one cut-out, in
small cropped frames (fan-0 .. fan-3 turning, a quarter of a quarter turn apart; fan-stopped, still, from the first
time Ranger is in the duct), each with the same box and foot; the backdrop has the fan's ring plate empty, the shaft
going on down round it and through it."""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, blur, lerp, noise, sample, strokes, grain, to_palette, save, palette_of
from room import View
import office_ducts_model as M
import office_ducts_things as T
from office_ducts_kit import Stage, Lamp, shade, col, LUM

W, H = 800, 600
V = View(**M.VIEW)
OUT = "out/office-ducts"
WORK = "out/office-ducts-work"
SEED = 17
COOL_BELOW = 0.42            # light weaker than this begins to turn blue-violet
EXPOSE = 1.18                # (OFFICE-17B2: 1.12 before)

FLUO = T.FLUO
DAY = T.DAYLIGHT


# ---------------------------------------------------------------- the light
def lamps(fast=False):
    """OFFICE-17B2: the duct is the brightest, clearest thing; round it the ceiling space is dim but readable."""
    n = 1 if fast else 4
    out = []
    for gid, _, gx in M.GRILLES:
        # the room's light under the grille: it comes up through the diffuser and the boot, through the slats, and
        # strikes the back wall above in bars (the slats are what throw them), fading as they rise
        out.append(Lamp((gx, M.TILE_Y - 14.0, 292.0), FLUO, 6.4, reach=118.0, aim=(0.0, 1.0, -0.62), spread=0.25, soft=0.35,
                        size=1.6, samples=n, wrap=0.05))                    # (a small source: the slats' bars stay crisp)
        # and the same light, gone soft off the duct's top inside, round the grille (no bars in it)
        out.append(Lamp((gx, M.DUCT_H - 14.0, 268.0), FLUO, 0.95, reach=100.0, size=30.0, samples=n, wrap=0.35, shadows=False))
    # daylight down the intake run, from the rooftop unit's open grille at its top
    out.append(Lamp((44.0, 560.0, 272.0), DAY, 5.0, reach=130.0, aim=(0.0, -1.0, -0.30), spread=0.35, soft=0.5, size=30.0,
                    samples=n, wrap=0.2))
    out.append(Lamp((44.0, 600.0, 230.0), DAY, 0.35, reach=200.0, aim=(0.0, -1.0, 0.1), spread=0.6, soft=0.4, size=40.0,
                    samples=n, wrap=0.2))
    out.append(Lamp((44.0, 330.0, 292.0), DAY, 0.14, reach=150.0, size=30.0, samples=n, wrap=0.35, shadows=False))   # its bounce
    # the light fittings, up through the tiles: under each, its light (the tiles do not stop it: they glow round it)
    for (x0, x1, z0, z1) in M.FITTINGS:
        cx, cz = (x0 + x1) / 2, (z0 + min(z1, M.CUT)) / 2
        out.append(Lamp((cx, M.TILE_Y - 30.0, cz), FLUO, 1.45, reach=150.0, aim=(0.0, 1.0, 0.0), spread=0.25, soft=0.6,
                        size=45.0, samples=n, wrap=0.15))
    # the fittings behind the duct: their light comes up between the tiles and fans up the far wall (OFFICE-17B2)
    for gx, gz in M.GLOWS:
        out.append(Lamp((gx, M.TILE_Y + 14.0, gz), FLUO, 3.6, reach=185.0, aim=(0.0, 1.0, -0.12), spread=0.93, soft=0.06,
                        size=14.0, samples=n, wrap=0.65))
    # and where they leak at their edges into the gap: low, along the tiles
    for (x0, x1, z0, z1) in M.CUT_FITTINGS:
        for ex in (x0 - 2.0, x1 + 2.0):
            out.append(Lamp((ex, M.TILE_Y + 1.5, M.CUT - 26.0), FLUO, 0.26, reach=60.0, size=6.0, samples=n, wrap=0.5))
    # the room's light up through the crack under the lifted tile, on the pencil and the wrapper beside it
    lt = M.LIFTED
    out.append(Lamp(((lt["X"][0] + lt["X"][1]) / 2, M.TILE_Y + 1.2, lt["Z"][1] + 1.5), FLUO, 0.34, reach=36.0, size=20.0,
                    samples=n, wrap=0.5, shadows=False))
    # the B-7 shaft: clean cool light from far below (the way down), the bulb over the duct's mouth, a little daylight
    # from its cap on the roof
    out.append(Lamp((745.0, -380.0, 232.0), "#d4dcf0", 3.0, reach=260.0, aim=(0.0, 1.0, 0.0), spread=0.45, soft=0.35,
                    size=40.0, samples=n, wrap=0.25))
    bx, by, bz = M.BULB["at"]
    out.append(Lamp((bx, by - 3.0, bz + 9.0), "#fff2d8", 0.95, reach=95.0, size=6.0, samples=n, wrap=0.2))
    out.append(Lamp((745.0, 640.0, 250.0), "#eef0f0", 0.30, reach=300.0, aim=(0.0, -1.0, -0.2), spread=0.5, soft=0.4,
                    size=40.0, samples=n, wrap=0.2))
    return out


def ambient(X, Y, Z, N):
    """The dim cool light that is simply in a ceiling space: a little more from below (the rooms' light round every
    edge of every tile), less high up under the deck. OFFICE-17B2: more of it than before (dim, but readable); inside the
    duct the grilles' light goes round the metal; inside the shaft its clean light; up the run the day."""
    up = 0.5 - 0.5 * N[..., 1]                                         # what faces down gets a little more (from below)
    high = np.clip((Y - 150.0) / 300.0, 0, 1)
    wall = (Z < M.FAR + 2.0).astype(F32)
    a = col("#58607e")[None, None, :] * ((0.17 + 0.07 * up * (1.0 - high)) * (1.0 - 0.66 * high) * (1.0 - 0.35 * wall))[..., None]
    # the fittings' light washing up the far wall from below, strongest just over the duct (it silhouettes the duct's top)
    a = a + col(FLUO)[None, None, :] * (wall * 0.12 * np.exp(-np.clip(Y - 120.0, 0, None) / 110.0))[..., None]
    toward = np.clip(N[..., 2], 0, 1)
    a = a + col("#6a6a80")[None, None, :] * (toward * 0.06)[..., None]
    inside = ((Z > M.DUCT_Z[0] - 1.0) & (Y > -2.0) & (Y < M.DUCT_H + 2.0) & (X > M.DUCT_X[0] - 2.0) & (X < M.SHAFT_X[0] + 2.0)).astype(F32)
    a = a + col(FLUO)[None, None, :] * (inside * (0.30 + 0.12 * np.clip(1 - Y / 130.0, 0, 1)))[..., None]
    shaft_ = ((X > M.SHAFT_X[0] - 1.0) & (X < M.SHAFT_X[1] + 1.0) & (Z > M.SHAFT_Z[0] - 1.0)).astype(F32)
    a = a + col("#cfd6e6")[None, None, :] * (shaft_ * (0.02 + 0.40 * np.clip((-Y - 40.0) / 220.0, 0, 1)
                                                        + 0.05 * np.clip(1 - np.abs(Y - 60.0) / 120.0, 0, 1)))[..., None]
    run_ = ((X > M.RUN_X[0] - 1.0) & (X < M.RUN_X[1] + 1.0) & (Z > M.DUCT_Z[0] - 1.0) & (Y > M.DUCT_H)).astype(F32)
    return a + col(DAY)[None, None, :] * (run_ * (0.01 + 0.10 * np.clip((Y - 130.0) / 400.0, 0, 1) ** 1.5))[..., None]


# ---------------------------------------------------------------- putting it together
def stage(ss=1, skip=(), rect=None, fan_angle=None, fan_only=False):
    """Every thing put on the stage: what each ray meets (no light yet)."""
    st = Stage(V, ss=ss, rect=rect)
    st.skip = set(skip) | {"ghost"}                                     # (the cut-away walls: shadows only)
    T.build(st, fan_angle=fan_angle, fan_only=fan_only)
    return st


def fan_patch():
    """The patch of the picture round the B-7 fan that its frames are painted on: (hub x, hub y, rect)."""
    fx, fy = V.pt(M.FAN["at"][0], M.FAN["at"][1], M.FAN["at"][2])
    rx0, ry0 = int(math.floor(fx - M.FAN["r"] * 1.15 - 12)), int(math.floor(fy - 34))
    rect = (max(rx0, 0), max(ry0, 0), min(int(math.ceil(fx + M.FAN["r"] * 1.15 + 12)), W), min(int(math.ceil(fy + 34)), H))
    return fx, fy, rect


def fan_frames_box(masks, fx, fy, rect):
    """One box round the fan at every angle (the union of their masks), and the foot (the hub) in it."""
    ys, xs = np.nonzero(np.any(masks, axis=0))
    bx0, by0, bx1, by1 = int(xs.min()) - 1, int(ys.min()) - 1, int(xs.max()) + 2, int(ys.max()) + 2
    crop = (rect[0] + bx0, rect[1] + by0, rect[0] + bx1, rect[1] + by1)               # on the stage
    foot = [int(round(fx)) - crop[0], int(round(fy)) - crop[1]]
    return (bx0, by0, bx1, by1), crop, foot


FAN_FRAMES = [(f"fan-{i}", a) for i, a in enumerate(M.FAN_TURN)] + [("fan-stopped", M.FAN["rest"])]


def render(ss=1, fast=True, skip=(), rect=None, occ=None, fan_angle=None, fan_only=False):
    st = stage(ss, skip, rect, fan_angle, fan_only)                     # OFFICE-17B (resumed): the build alone is stage()
    pic, light = shade(st, lamps(fast), ambient, fast=fast, occ=occ, expose=EXPOSE)
    glass = (st.flag & 4) > 0
    lum = light @ LUM
    deep = np.clip(1 - lum / COOL_BELOW, 0, 1) ** 1.1
    pic = np.where(glass[..., None], pic, pic * (1 + deep[..., None] * np.array([-0.14, -0.06, 0.24], dtype=F32)[None, None, :]))
    # depth by tone: the far wall and what is near it a little cooler and closer in value
    X, Y, Z = st.places()
    far = np.clip((140.0 - Z) / 140.0, 0, 1) * (~glass) * (st.t < 9e8)
    pic = pic * (1 - 0.18 * far[..., None]) + col("#2a2c48")[None, None, :] * (0.18 * far)[..., None]
    # OFFICE-17B2: the air of the ceiling space between us and its far wall: the wall and what is on it quieter, a little
    # hazed toward one dim violet (it reads as far, and the duct in front of it as near)
    haze = np.clip((M.FAR + 12.0 - Z) / 12.0, 0, 1) * (~glass) * (st.t < 9e8)
    pic = pic * (1 - 0.22 * haze[..., None]) + col("#3c3a56")[None, None, :] * (0.22 * haze)[..., None]
    return st.down(pic), st


_Y, _X = np.mgrid[0:H, 0:W].astype(F32)
_DX = (noise((H, W), 30, SEED + 3, 3) - 0.5) * 2 * 0.6
_DY = (noise((H, W), 30, SEED + 4, 3) - 0.5) * 2 * 0.6


def wob(a, rect=None):
    """Nothing a hand rules is perfectly straight: every picture and mask is pushed about by the same slow field, under
    a pixel, so the cut-outs still fit the backdrop exactly."""
    if rect is None:
        return sample(a, _X + _DX, _Y + _DY)
    x0, y0, x1, y1 = rect
    return sample(a, _X[y0:y1, x0:x1] - x0 + _DX[y0:y1, x0:x1], _Y[y0:y1, x0:x1] - y0 + _DY[y0:y1, x0:x1])


def grade(pic, rect=None):
    """The whole picture's last adjustments: the top (the joists and the deck) a little deeper, the corners a little
    deeper and warmer, to hold the eye on the duct. (OFFICE-17B2: far less than before: the ceiling space is to read.)"""
    x0, y0, x1, y1 = rect or (0, 0, W, H)
    y, x = np.mgrid[y0:y1, x0:x1].astype(F32)
    cx = ((x - 400) / 400) ** 2
    top = np.clip((150 - y) / 150, 0, 1) ** 1.3
    low = np.clip((y - 560) / 40, 0, 1)
    v = np.clip(top * 0.28 + cx * 0.06 + low * 0.06, 0, 0.4)
    warm = col("#3a2a3a")
    out = pic * (1 - v[..., None]) + pic * warm[None, None, :] * 1.4 * v[..., None]
    grey = (out @ LUM)[..., None]
    out = grey + (out - grey) * 1.08
    return np.clip(out, 0, 1)


def paint(crisp, seed=2):
    """The brush pass, and then the built things said again crisply over it."""
    b = strokes(crisp, sizes=(9, 5, 2), seed=seed, density=1.5, jitter=0.04, keep=0.32)
    hf = np.abs(crisp - blur(crisp, 1.4)).sum(axis=2)
    w = np.clip(hf * 7.5 - 0.05, 0, 1)
    w = np.maximum(w, blur(w, 0.7))
    out = lerp(b, crisp, (0.16 + 0.82 * w)[..., None])
    return np.clip(out + 0.40 * (out - blur(out, 0.9)), 0, 1)


def maps_of(st, rect=None):
    """What each pixel shows, for the details: its depth, its surface's upward lean, which thing it is."""
    return wob(st.pick(np.minimum(st.t, 5000.0)), rect), wob(st.pick(st.N[..., 1]), rect), st.pick(st.oid), st.pick(st.N[..., 2])


def details(pic, maps):
    """Small crisp accents found from what each pixel shows: the lit front edge of every top (the duct's floor where it
    is cut, the tiles' cut, the plate's lip), and a dark line where one thing stands in front of another far behind."""
    t, ny, oid, nz = maps
    below_same = (np.roll(oid, -1, axis=0) == oid) & (np.roll(ny, -1, axis=0) < 0.5) & (ny > 0.9)
    below_same[-1] = False
    out = pic.copy()
    out[below_same] = np.clip(out[below_same] * 1.25 + 0.04, 0, 1)
    for ax, sh_ in ((0, 1), (0, -1), (1, 1), (1, -1)):
        tn = np.roll(t, sh_, axis=ax)
        behind = (t - tn > 14.0) & (t - tn > 0.03 * t)
        if ax == 0:
            behind[0 if sh_ == 1 else -1] = False
        else:
            behind[:, 0 if sh_ == 1 else -1] = False
        out[behind] = out[behind] * 0.74
    return out


def to_image(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def tones(a, label=""):
    lum = (np.clip(a, 0, 1) * 255) @ LUM
    print(label, "mean", (a.mean(axis=(0, 1)) * 255).round(0), "lum 5/25/50/75/95:", np.percentile(lum, [5, 25, 50, 75, 95]).round(0))


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "fast":
        ang = float(sys.argv[2]) if len(sys.argv) > 2 else M.FAN["rest"]
        pic, st = render(ss=1, fast=True, fan_angle=ang)
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
    if mode == "layout":
        # layout.json again from the geometry alone (no light, no paint: a few seconds): the same rays as the full run's,
        # so the same numbers; for a change to office_ducts_layout.py that leaves the pictures as they are
        from office_ducts_layout import write as write_layout
        stA = stage(ss=2)
        fx, fy, rect = fan_patch()
        masks = [wob(stR.down((stR.grp == stR.groups.get("fan", -99)).astype(F32)), rect) > 0.5
                 for stR in (stage(ss=2, rect=rect, fan_angle=ang) for _, ang in FAN_FRAMES)]
        (bx0, by0, bx1, by1), crop, foot = fan_frames_box(masks, fx, fy, rect)
        for nm, _ in FAN_FRAMES:
            p = f"{OUT}/{nm}.png"
            if os.path.exists(p) and Image.open(p).size != (bx1 - bx0, by1 - by0):
                sys.exit(f"{p} is not the fan's box measured now ({bx1 - bx0} x {by1 - by0}): paint everything again (no argument)")
        write_layout(stA, crop, foot)
        print("layout.json written: fan", crop, "foot", foot, round(time.time() - t0, 1), "s")
        sys.exit()

    # ================================================================ the full run
    from office_ducts_layout import write as write_layout
    SS = 2
    # ---- the backdrop: everything, the B-7 fan's plate with its hole empty (the blades are the cut-out)
    A, stA = render(ss=SS, fast=False)
    to_image(A).save(f"{WORK}/1-under.png")
    print("rendered", round(time.time() - t0, 1))
    pA = details(paint(grade(wob(A)), 2), maps_of(stA))
    to_image(pA).save(f"{WORK}/2-painted.png")
    tones(pA, "tones:")
    print("painted", round(time.time() - t0, 1))

    def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.007, amount=0.011):
        g = grain(picture, seed, amount)
        sample_of = g if alpha is None else g[alpha > 0.5]
        pal = palette_of([sample_of.reshape(-1, 3)], colors=min(colors, max(8, len(np.unique((sample_of.reshape(-1, 3) * 255).astype(np.uint8), axis=0)))))
        idx = to_palette(g, pal, speckle=speckle)
        save(name, idx, pal, alpha)
        return os.path.getsize(name)

    sizes = {"back": finish(pA, f"{OUT}/back.png", 160)}
    # ---- the B-7 fan: its blades and hub at each angle, painted on a patch of the picture round it, cut out by what the
    #      rays met of it; every frame cropped to one box (the union of them all), with one foot point (the hub's middle)
    fx, fy, rect = fan_patch()
    frames = {}
    for nm, ang in FAN_FRAMES:
        R, stR = render(ss=SS, fast=False, rect=rect, fan_angle=ang)
        pR = details(paint(grade(wob(R, rect), rect), 2), maps_of(stR, rect))
        m = wob(stR.down((stR.grp == stR.groups.get("fan", -99)).astype(F32)), rect) > 0.5
        frames[nm] = (pR, m)
    (bx0, by0, bx1, by1), crop, foot = fan_frames_box([m for _, m in frames.values()], fx, fy, rect)
    for nm, (pR, m) in frames.items():
        sizes[nm] = finish(pR[by0:by1, bx0:bx1], f"{OUT}/{nm}.png", 48, m[by0:by1, bx0:bx1].astype(F32))
    print("fan frames", crop, "foot", foot, round(time.time() - t0, 1))
    write_layout(stA, crop, foot)
    # ---- the comps: the backdrop with the fan stopped, and with it turning
    for which in ("fan-stopped", "fan-0"):
        im = Image.open(f"{OUT}/back.png").convert("RGBA")
        im.alpha_composite(Image.open(f"{OUT}/{which}.png").convert("RGBA"), (crop[0], crop[1]))
        im.convert("RGB").save(f"out/office-ducts-comp{'' if which == 'fan-stopped' else '-turning'}.png")
    print("sizes", sizes)
    print("done", round(time.time() - t0, 1))

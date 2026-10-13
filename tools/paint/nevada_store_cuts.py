"""The full run of nevada_store.py: the whole room painted twice (with everything, and without the cut-outs), the
cut-outs taken from the first, the frames of the things that move by nature, the hens, layout.json, the comps and
the people standing in it.

The cut-outs (each 800x600, clear but for the thing, hard-edged):
    hat-1 .. hat-5     Jolene's five hats on their pegs (the scene hides the one she is wearing today)
    doorframe          the back wall round the back door, its casing, the screen door, her chair and the phone: what
                       is outside (the hens, Little Sister on the step) is seen through it
    cooler             Harold, with the TV's corner behind him
    counter            the counter and all on it, the grill with the roller (frame 0), the map rack, Ranger's basket
    spinner            the sunglasses rack
    rockbins           the rock bins, their tapes and the ROCKS $1 card
    front              the water flats, the crate of bottles, the tyres
    window-shade       (alt) the sun shade in the window, until it is given
    mirror-shades      (alt) the last pair of mirror shades on the spinner, until it is bought
Frames (cropped, with a foot point): roller-0, roller-1 (2 fps), tv-0, tv-1, tv-2 (6 fps), hen-<n>-<state>, egg-dust."""

import json
import os
import subprocess
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, grain, to_palette, save
import nevada_store as S
import nevada_store_model as M
import nevada_store_props as P
from nevada_store_kit import Stage

OUT = S.OUT
WORK = S.WORK
W, H = 800, 600
CUT_FILES = [  # file name, group, palette size
    ("hat-1", "hat-1", 24), ("hat-2", "hat-2", 24), ("hat-3", "hat-3", 16), ("hat-4", "hat-4", 16), ("hat-5", "hat-5", 20),
    ("cooler", "cooler", 72), ("counter", "counter", 96), ("spinner", "spinner", 40), ("rockbins", "rockbins", 72),
    ("front", "front", 72), ("window-shade", "shade", 40), ("mirror-shades", "mirror", 16),
]
DOOR_RECT = (566, 224, 708, 396)                       # the picture round the back door that the door frame's cut-out may hold


def door_mask(stA, others):
    """The back door's frame: everything that is not outside, inside DOOR_RECT, and not another cut-out; and all of
    Jolene's chair and her knitting (the chair reaches past the rectangle's right side)."""
    outside = stA.down(((stA.flag & 4) > 0).astype(F32))
    m = np.zeros((H, W), F32)
    x0, y0, x1, y1 = DOOR_RECT
    m[y0:y1, x0:x1] = 1.0
    m = np.maximum(m, S.cover(stA, name=("chair", "knitting")))
    m = m * (1 - outside)
    for o in others:
        m = m * (1 - np.clip(o * 2, 0, 1))
    return m


def frame_patch(rect, state, grp, ss=2):
    """Render a small patch of the picture in another state and take one group's pixels: -> (picture, alpha) of the
    patch. Graded like the picture, not brushed: a frame is keyed colour by colour and laid over the painting."""
    P_, sp = S.render(ss=ss, fast=False, rect=rect, **state)
    pic = S.grade(P_, rect)
    a = S.cover(sp, grp=grp)
    return pic, a


def save_frame(pic, a, name, colors=32, seed=7):
    g = grain(pic, seed, 0.008)
    pal = S.palette_for(g[a > 0.5] if (a > 0.5).any() else g, colors)
    idx = to_palette(g, pal, speckle=0.004)
    save(name, idx, pal, a)


def main(t0):
    SS = 2
    S._ROCKS["bins"] = P.rockbins(Stage(S.V, ss=1, rect=(0, 0, 2, 2)), "x")
    # ---- everything in the room (the cut-outs are taken from this one)
    A, stA = S.render(ss=SS, fast=False)
    S.to_image(A).save(f"{WORK}/1-under.png")
    print("all", round(time.time() - t0, 1))
    # ---- the room with the cut-outs taken away (their shadows stay where they fall)
    B, stB = S.render(ss=SS, fast=False, skip=S.CUTS, occ=stA.occ)
    print("back", round(time.time() - t0, 1))
    pA = S.details(S.paint(S.grade(S.wob(A)), 2), S.maps_of(stA))
    S.letters(pA, stA)
    pB = S.details(S.paint(S.grade(S.wob(B)), 2), S.maps_of(stB))
    S.letters(pB, stB, groups=("back",))
    S.to_image(pA).save(f"{WORK}/2-all.png")
    S.to_image(pB).save(f"{WORK}/2-back.png")
    S.tones(pA, "tones:")
    print("painted", round(time.time() - t0, 1))

    sizes = {}
    sizes["back"] = S.finish(pB, f"{OUT}/back.png", 160)
    covers = {}
    for name, grp, colors in CUT_FILES:
        a = S.wob(S.cover(stA, grp=grp))
        covers[name] = a
        sizes[name] = S.finish(pA, f"{OUT}/{name}.png", colors, a)
    others = [covers[n] for n in ("cooler", "counter", "spinner", "rockbins", "front", "hat-1", "hat-2", "hat-3", "hat-4", "hat-5")]
    covers["doorframe"] = door_mask(stA, others)
    sizes["doorframe"] = S.finish(pA, f"{OUT}/doorframe.png", 64, covers["doorframe"])
    print("cut-outs", round(time.time() - t0, 1), sizes)

    # ---- the frames of the things that move by nature: the roller turning, the snow on the TV
    frames = {}
    rr = S.clamp_rect(S.bbox(S.cover(stA, name="rollers") > 0.05), 4)
    for k, ph in enumerate((0.0, np.pi / 3)):
        pic, a = frame_patch(rr, dict(roller_phase=ph), "roller")
        save_frame(pic, a, f"{OUT}/roller-{k}.png", 24)
    frames["roller"] = crop_frames([f"roller-{k}.png" for k in range(2)], rr[:2])
    tr = S.clamp_rect(S.bbox(S.cover(stA, name="tvscreen") > 0.05), 3)
    for k in range(3):
        pic, a = frame_patch(tr, dict(tv_frame=(0, 2, 3)[k]), "tvscreen")
        save_frame(pic, a, f"{OUT}/tv-{k}.png", 24, seed=11 + k)
    frames["tv"] = crop_frames([f"tv-{k}.png" for k in range(3)], tr[:2])
    print("frames", round(time.time() - t0, 1), frames)

    # ---- the hens, and the egg
    import nevada_store_hens
    hens = nevada_store_hens.paint(OUT)
    print("hens", round(time.time() - t0, 1))

    import nevada_store_layout
    L = nevada_store_layout.write(stA, stB, covers, frames, hens, wob=S.wob)
    comp_all()
    nevada_store_layout.check()
    print("layout and comps", round(time.time() - t0, 1))
    subprocess.run([sys.executable, "nevada_store_people.py"])
    print("done", round(time.time() - t0, 1))


def crop_frames(files, origin=(0, 0)):
    """The frames of one moving thing are painted full size: crop them all to the box that holds every one of them,
    and say where that box is and where its foot is (the middle of its bottom edge). -> {files, at, foot, rect}"""
    ims = [Image.open(f"{OUT}/{f}") for f in files]
    boxes = [im.convert("RGBA").getchannel("A").getbbox() for im in ims]
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[2] for b in boxes)
    y1 = max(b[3] for b in boxes)
    for im, f in zip(ims, files):
        c = im.crop((x0, y0, x1, y1))
        if "transparency" in im.info:
            c.info["transparency"] = im.info["transparency"]
            c.save(f"{OUT}/{f}", optimize=True, transparency=im.info["transparency"])
        else:
            c.save(f"{OUT}/{f}", optimize=True)
    foot = [(x1 - x0) // 2, y1 - y0]
    ox, oy = origin
    return {"files": files, "rect": [ox + x0, oy + y0, x1 - x0, y1 - y0], "foot": foot, "at": [ox + x0 + foot[0], oy + y0 + foot[1]]}


def comp_all():
    """The scene's pictures laid together: as it first is (the shade and the mirror shades still there), and later
    (both gone, another hat on the peg), with the roller and the TV's frames and the hens laid where the scene lays
    them."""
    L = json.load(open(f"{OUT}/layout.json"))

    def lay(im, f, at=None, foot=None):
        top = Image.open(f"{OUT}/{f}").convert("RGBA")
        if at is None:
            im.alpha_composite(top)
        else:
            im.alpha_composite(top, (int(at[0] - foot[0]), int(at[1] - foot[1])))
    for state, hide in (("comp", ()), ("comp-later", ("window-shade", "mirror-shades", "hat-2"))):
        im = Image.open(f"{OUT}/back.png").convert("RGBA")
        for fx in L["fx"]:
            if fx["id"] in ("tv",):
                lay(im, fx["frames"][0], fx["at"], fx["foot"])
        hj = L["hens"]
        for h in hj["hens"]:
            lay(im, f"hen-{h['n']}-guard-a.png" if state == "comp" else (f"hen-{h['n']}-sit.png" if h["n"] == 1 else f"hen-{h['n']}-guard-b.png"), h["at"], hj["foot"])
        if state != "comp":
            lay(im, hj["egg"]["file"], hj["egg"]["at"], hj["egg"]["foot"])
        for p in L["planes"]:
            if p.get("file") and p["id"] not in hide and p.get("plane") != "front":
                lay(im, p["file"])
            if p["id"] == "counter":
                for fx in L["fx"]:
                    if fx["id"] == "roller":
                        lay(im, fx["frames"][0], fx["at"], fx["foot"])
        for p in L["planes"]:
            if p.get("plane") == "front":
                lay(im, p["file"])
        im.convert("RGB").save(f"out/nevada-store-{state}.png")

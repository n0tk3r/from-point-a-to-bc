"""The full run of office_breakroom.py: the whole room painted twice (with everything, and without the cut-outs), the
cut-outs taken from the first, each other state of a cut-out painted as a patch of the picture in that state, the
clock's second hand in its sixty frames, layout.json, the comps and the check. OFFICE-17D.

The cut-outs (each 800x600, clear but for the thing, hard-edged):
    pie               Wendell's pie in its tin, the card stood against it (first state)
    pie-eaten         (alt) the empty tin, sticky, a bottle cap set in its middle, the card still standing
    pie-gone          (alt) the tin taken: the card fallen flat, the bottle cap left on it, a sticky ring
    schedule          the test schedule on the corkboard (gone: the scene hides it; a pin and a torn corner are under it)
    vent              the return grille over the fridge, plain (hidden: the duct's dark mouth is under it)
    vent-eyes         (alt) the grille with Ranger's eyes shining in it, his mask, his nose
    vending           the snack machine (first state: full)
    vending-peanuts   (alt) a packet of peanuts come down into the tray, its coil empty
    vending-taken     (state of vending-peanuts) the tray empty again, the coil still empty
    door              the door to the hall, shut, the jacket on its hook (plane: back)
    door-open         (alt) the door standing open into the room, its hall side to us (the hall is in the backdrop)
    chair             Jed's chair
    front             the round table in the near right and its chair, and the low table in the near left (the foreground)
Frames: clock-0 .. clock-59 (the second hand, one a second)."""

import json
import os
import subprocess
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, grain, to_palette, save, blur
import office_breakroom as S
import office_breakroom_model as M

OUT = S.OUT
WORK = S.WORK
W, H = 800, 600
CUT_FILES = [  # file name, group, palette size (the paints re-index every file of the scene into one palette at install)
    ("pie", "pie", 48), ("schedule", "schedule", 24), ("vent", "vent", 24), ("vending", "vending", 96), ("door", "door", 64),
    ("chair", "chair", 40), ("front", "front", 96),
]
# the other states, each painted as a patch round its thing: name, the state, the group it takes, the first-state cut-out
# it replaces (the union of the two shapes is taken, so that nothing of the old state is left showing round the new)
STATES = [
    ("pie-eaten", dict(pie="eaten"), "pie", "pie"),
    ("pie-gone", dict(pie="gone"), "pie", "pie"),
    ("vent-eyes", dict(vent_eyes=True), "vent", "vent"),
    ("vending-peanuts", dict(vending="peanuts"), "vending", "vending"),
    ("vending-taken", dict(vending="taken"), "vending", "vending"),
    ("door-open", dict(door_open=True), "door-open", None),
]


def dilate(a, px=1):
    m = a > 0.5
    out = m.copy()
    for dy in range(-px, px + 1):
        for dx in range(-px, px + 1):
            out |= np.roll(np.roll(m, dy, axis=0), dx, axis=1)
    return out.astype(F32)


def patch_paint(rect, state, groups_for_words):
    """Paint a patch of the picture in another state through all the passes, as the whole picture is painted. ->
    (picture, stage), both the patch's size."""
    P_, sp = S.render(ss=2, fast=False, rect=rect, **state)
    x0, y0, x1, y1 = rect
    maps = (S.wob(sp.pick(np.minimum(sp.t, 5000.0)), rect), S.wob(sp.pick(sp.N[..., 1]), rect), _wob_near_rect(sp.pick(sp.oid), rect),
            sp.names.get("floor", -1))
    pic = S.details(S.paint(S.grade(S.wob(P_, rect), rect), 2), maps)
    S.letters(pic, groups=groups_for_words, rect=rect, **state)
    return pic, sp


def _wob_near_rect(a, rect):
    x0, y0, x1, y1 = rect
    yy = np.clip(np.round(S._Y[y0:y1, x0:x1] + S._DY[y0:y1, x0:x1]) - y0, 0, y1 - y0 - 1).astype(np.intp)
    xx = np.clip(np.round(S._X[y0:y1, x0:x1] + S._DX[y0:y1, x0:x1]) - x0, 0, x1 - x0 - 1).astype(np.intp)
    return a[yy, xx]


def cover_rect(sp, grp, rect):
    """A group's coverage in a patch, wobbled as the whole picture's masks are, put into a full-size mask."""
    gs = [grp] if isinstance(grp, str) else list(grp)
    m = np.isin(sp.grp, [sp.groups[g] for g in gs if g in sp.groups])
    m = sp.down(m.astype(F32))
    full = np.zeros((H, W), F32)
    x0, y0, x1, y1 = rect
    full[y0:y1, x0:x1] = S.wob(m, rect)
    return full


def save_frame(pic, a, name, colors=16, seed=7):
    g = grain(pic, seed, 0.006)
    pal = S.palette_for(g[a > 0.5] if (a > 0.5).any() else g, colors)
    idx = to_palette(g, pal, speckle=0.003)
    save(name, idx, pal, a)


def main(t0):
    SS = 2
    # ---- everything in the room, in the first state (the cut-outs are taken from this one)
    A, stA = S.render(ss=SS, fast=False)
    S.to_image(A).save(f"{WORK}/1-under.png")
    print("all", round(time.time() - t0, 1))
    # ---- the room with the cut-outs taken away (their shadows stay where they fall)
    B, stB = S.render(ss=SS, fast=False, skip=S.CUTS, occ=stA.occ)
    print("back", round(time.time() - t0, 1))
    pA = S.details(S.paint(S.grade(S.wob(A)), 2), S.maps_of(stA))
    S.letters(pA)
    pB = S.details(S.paint(S.grade(S.wob(B)), 2), S.maps_of(stB))
    S.letters(pB, groups=("back",))
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
    print("cut-outs", round(time.time() - t0, 1), sizes)

    # ---- the other states, painted as patches round their things
    full_pics = {}
    for name, state, grp, replaces in STATES:
        base = covers.get(replaces) if replaces else None
        probe = S.render(ss=1, fast=True, **state)[1]                       # where the thing is in that state (a quick look)
        mask = S.cover(probe, grp=grp)
        if base is not None:
            mask = np.maximum(mask, base)
        if name == "pie-gone":                                              # the tin's place and its shadow, cleaned
            tin = S.wob(S.cover(stA, name=("pietin", "piecrust", "card")))
            mask = np.maximum(mask, dilate(tin, 3))
        r = S.clamp_rect(S.bbox(mask > 0.05), 10)
        pic, sp = patch_paint(r, state, groups_for_words=(grp, "pie") if grp == "pie" else (grp,))
        a = cover_rect(sp, grp, r)
        if base is not None:
            a = np.maximum(a, base)
        if name == "pie-gone":
            a = np.maximum(a, dilate(tin, 3))
        canvas = pA.copy()
        x0, y0, x1, y1 = r
        canvas[y0:y1, x0:x1] = pic
        full_pics[name] = canvas
        covers[name] = a
        sizes[name] = S.finish(canvas, f"{OUT}/{name}.png", 64 if "pie" in name or "vent" in name else 96, a)
        print("state", name, r, round(time.time() - t0, 1))

    # ---- the clock's second hand, one frame a second (graded like the picture, not brushed: frames are keyed colour by
    # colour and laid over the painting)
    cx, cy, cr = M.CLOCK
    pts = [S.V.pt(cx + dx, cy + dy, 4.7) for dx in (-cr, cr) for dy in (-cr, cr)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    cr_ = S.clamp_rect((int(min(xs)), int(min(ys)), int(max(xs)) + 1, int(max(ys)) + 1), 3)
    files = []
    for k in range(60):
        P_, sp = S.render(ss=2, fast=False, rect=cr_, hand=k)
        pic = S.grade(P_, cr_)
        a = cover_rect(sp, "secondhand", cr_)[cr_[1]:cr_[3], cr_[0]:cr_[2]]
        full_pic = np.zeros((H, W, 3), F32)
        full_pic[cr_[1]:cr_[3], cr_[0]:cr_[2]] = pic
        full_a = np.zeros((H, W), F32)
        full_a[cr_[1]:cr_[3], cr_[0]:cr_[2]] = a
        save_frame(full_pic, full_a, f"{OUT}/clock-{k}.png", 8, seed=40 + k)
        files.append(f"clock-{k}.png")
    frames = {"clock": crop_frames(files, keep_box=cr_)}
    print("frames", round(time.time() - t0, 1), frames["clock"]["rect"])

    import office_breakroom_layout
    L = office_breakroom_layout.write(stA, stB, covers, frames, wob=S.wob)
    comp_all()
    office_breakroom_layout.check()
    print("layout and comps", round(time.time() - t0, 1))


def crop_frames(files, keep_box=None):
    """The frames of one moving thing are painted full size: crop them all to one box (the box given, or the one that
    holds every frame's pixels), and say where that box is and where its foot is (the middle of its bottom edge)."""
    ims = [Image.open(f"{OUT}/{f}") for f in files]
    if keep_box is not None:
        x0, y0, x1, y1 = keep_box
    else:
        boxes = [im.convert("RGBA").getchannel("A").getbbox() for im in ims]
        x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
        x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    for im, f in zip(ims, files):
        c = im.crop((x0, y0, x1, y1))
        if "transparency" in im.info:
            c.info["transparency"] = im.info["transparency"]
            c.save(f"{OUT}/{f}", optimize=True, transparency=im.info["transparency"])
        else:
            c.save(f"{OUT}/{f}", optimize=True)
    foot = [(x1 - x0) // 2, y1 - y0]
    return {"files": files, "rect": [x0, y0, x1 - x0, y1 - y0], "foot": foot, "at": [x0 + foot[0], y0 + foot[1]]}


def comp(states=(), hide=(), second=0, out=None):
    """The scene's pictures laid together as the game lays them: the backdrop, the cut-outs in their first state (or
    the alts named in `states` in place of the cut-out each replaces; any in `hide` left off), the clock's hand."""
    L = json.load(open(f"{OUT}/layout.json"))
    im = Image.open(f"{OUT}/back.png").convert("RGBA")
    alts = {a: p for p in L["planes"] for a in [p.get("id")] if p.get("alt")}
    replaced = set()
    for s_ in states:
        replaced |= set(alts.get(s_, {}).get("replaces", []))
    for p in L["planes"]:
        pid = p["id"]
        if p.get("alt") and pid not in states:
            continue
        if pid in replaced or pid in hide or p.get("plane") == "front":
            continue
        im.alpha_composite(Image.open(f"{OUT}/{p['file']}").convert("RGBA"))
    clock = Image.open(f"{OUT}/{L['frames']['clock']['files'][second]}").convert("RGBA")
    at, foot = L["frames"]["clock"]["at"], L["frames"]["clock"]["foot"]
    im.alpha_composite(clock, (at[0] - foot[0], at[1] - foot[1]))
    for p in L["planes"]:
        if p.get("plane") == "front" and p["id"] not in hide:
            im.alpha_composite(Image.open(f"{OUT}/{p['file']}").convert("RGBA"))
    im = im.convert("RGB")
    if out:
        im.save(out)
    return im


def comp_all():
    comp(out="out/office-breakroom-comp.png")
    comp(states=("pie-eaten", "vent-eyes", "vending-peanuts", "door-open"), out="out/office-breakroom-comp-later.png", second=20)
    comp(states=("pie-gone", "vending-taken"), hide=("schedule",), out="out/office-breakroom-comp-end.png", second=40)

"""The full run of office_room.py: the whole room painted (with everything, and without the cut-outs), the cut-outs and
their other states taken from it, the frames of the clock's second hand and the cooler's bubble, layout.json, and the
comps. OFFICE-17C.

The cut-outs (each 800x600, clear but for the thing, hard-edged):
    vent             the grille over the corner, plain (the backdrop has it too)
    vent-eyes        (alt) the same grille, two eyes in a black mask shining between its slats: Ranger is up there
    thermostat-72    the thermostat, 72 in its window (the backdrop has it too)
    thermostat-77    (alt) 77
    thermostat-81    (alt) 81, the number red
    intercom         the intercom, its button dark (the backdrop has it too)
    intercom-lit     (alt) the button lit, while it is pressed
    door             the leaf, shut (the backdrop shows the doorway open on the hall)
    door-open        (alt) the leaf swung out into the hall, seen past the jamb
    doorframe        the back wall round the doorway and the steel casing: whoever is in the hall is behind it
    chair-corner     the fourth chair, in the corner under the grille (Grandpa Joe stands on its seat)
    table            the table (whoever sits at it, or stands behind it, is behind it), painted whole under the questionnaire
    questionnaire    the questionnaire on the table, while the suits are there
    plant            the plastic plant, upright
    plant-droop      (alt) the plastic plant, drooping (it cannot; it does)
    front            the wastebasket near us at the left
Frames (cropped, with a foot point): second-00 .. second-59 (the clock's red second hand, 1 fps), bubble-0 .. bubble-5
(a bubble rising in the cooler's jug, now and then)."""

import json
import math
import os
import subprocess
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, grain, to_palette, save
import office_room as R
import office_room_model as M
from office_room_kit import (Stage, finish, to_image, tones, cover, bbox, clamp_rect, letters, palette_for, poly_of_mask, rect_of_mask,
                             inside, LUM)

OUT = R.OUT
WORK = R.WORK
W, H = 800, 600
V = R.V
P = R.P
DRAFT = os.environ.get("OFFICE_DRAFT") == "1"        # a quick run of the whole pipeline: one ray a pixel, hard shadows
SS = 1 if DRAFT else 2
FAST = DRAFT

# file name, group, palette size
CUT_FILES = [("vent", "vent", 40), ("thermostat-72", "thermostat", 32), ("intercom", "intercom", 32), ("door", "door", 48),
             ("chair-corner", "chair-corner", 48), ("table", "table", 64), ("questionnaire", "questionnaire", 24), ("plant", "plant", 56),
             ("front", "front", 48)]
CUT_GROUPS = ("vent", "thermostat", "intercom", "door", "doorframe", "chair-corner", "table", "questionnaire", "plant", "front", "clockhand")
# the alts: file, group, the state that paints it
ALTS = [("vent-eyes", "vent", dict(eyes=True)), ("thermostat-77", "thermostat", dict(thermo=77)), ("thermostat-81", "thermostat", dict(thermo=81)),
        ("intercom-lit", "intercom", dict(lit=True)), ("door-open", "door", dict(door_open=True)), ("plant-droop", "plant", dict(droop=True))]


def door_rect():
    """The patch of picture round the doorway that the door frame's cut-out may hold: the back wall from a little left of
    the casing to a little right of it, from over the casing down to the floor."""
    dx0, dx1, dy0, dy1 = M.DOOR
    pts = [V.pt(X, Y, 0.0) for X in (dx0 - 42, dx1 + 42) for Y in (0.0, dy1 + 26)]
    return (int(min(p[0] for p in pts)), int(min(p[1] for p in pts)), int(max(p[0] for p in pts)) + 1, int(max(p[1] for p in pts)) + 2)


def doorframe_mask(stA, others):
    """The back wall round the doorway and the casing: everything in door_rect() that is the back wall or on it (not the
    hall seen through the opening, not the room's floor, not another cut-out)."""
    X, Y, Z = stA.places()
    wall = stA.down(((Z < 6.5) & ((stA.flag & 4) == 0)).astype(F32))
    m = np.zeros((H, W), F32)
    x0, y0, x1, y1 = door_rect()
    m[y0:y1, x0:x1] = 1.0
    m = m * np.clip(wall * 2 - 0.5, 0, 1)
    m = np.maximum(m, cover(stA, grp="doorframe"))
    for o in others:
        m = m * (1 - np.clip(o * 2, 0, 1))
    return m


def patch_state(base_raw, state, rect, ss=SS):
    """The room in another state over a patch of the picture: rendered there, set into a copy of the whole under-
    painting, and painted whole (so its strokes are the picture's own everywhere else). -> (painted picture, stage of
    the patch, the rect)."""
    pic, st = R.render(ss=ss, fast=FAST, rect=rect, state=state, reflection=R.reflection_fn(_REFL["img"]))
    full = base_raw.copy()
    x0, y0, x1, y1 = rect
    full[y0:y1, x0:x1] = pic
    return full, st


def group_mask_in(st, grp, rect):
    m = np.zeros((H, W), F32)
    x0, y0, x1, y1 = rect
    m[y0:y1, x0:x1] = cover(st, grp=grp)
    return m


_REFL = {}


def main(t0):
    os.makedirs(OUT, exist_ok=True)
    # ---- the mirror's reflection, then everything in the room (the cut-outs are taken from this one)
    _REFL["img"] = R.reflection_image(ss=SS, fast=FAST)                 # (patch_state renders with it too)
    refl = R.reflection_fn(_REFL["img"])
    print("reflection", round(time.time() - t0, 1))
    A, stA = R.render(ss=SS, fast=FAST, reflection=refl)
    R.to_image(R.grade(A)).save(f"{WORK}/1-under.png")
    print("all", round(time.time() - t0, 1))
    # ---- the room with the cut-outs taken away (their shadows stay where they fall); the plain grille, the thermostat
    # at 72 and the dark intercom stay in the backdrop as well
    B, stB = R.render(ss=SS, fast=FAST, skip=("door", "doorframe", "chair-corner", "table", "questionnaire", "plant", "front", "clockhand"),
                      occ=stA.occ, reflection=refl)
    print("back", round(time.time() - t0, 1))
    pA = R.paint_full(A, stA)
    pB = R.paint_full(B, stB, groups=("back", "thermostat", "intercom", "hall"))
    to_image(pA).save(f"{WORK}/2-all.png")
    to_image(pB).save(f"{WORK}/2-back.png")
    tones(pA, "tones:")
    print("painted", round(time.time() - t0, 1))

    sizes = {}
    sizes["back"] = finish(pB, f"{OUT}/back.png", 160)
    covers = {}
    for name, grp, colors in CUT_FILES:
        a = P.wob(cover(stA, grp=grp))
        covers[name] = a
        sizes[name] = finish(pA, f"{OUT}/{name}.png", colors, a)
    # the table: painted from the room without the questionnaire, so that its top is whole under it (the suits take the
    # questionnaire away in #17: the table must not have a hole where it lay)
    rect = clamp_rect(bbox(cover(stA, grp="table") > 0.02), 8)
    full, stP = patch_state(A, dict(questionnaire=False), rect)
    painted = P.details(P.paint(P.grade(P.wob(full)), 2), _maps_with_patch(stA, stP, rect))
    covers["table"] = P.wob(group_mask_in(stP, "table", rect))
    sizes["table"] = finish(painted, f"{OUT}/table.png", 64, covers["table"])
    others = [covers[n] for n in ("vent", "thermostat-72", "intercom", "door", "chair-corner", "table", "questionnaire", "plant", "front")]
    covers["doorframe"] = P.wob(doorframe_mask(stA, others))
    sizes["doorframe"] = finish(pA, f"{OUT}/doorframe.png", 64, covers["doorframe"])
    print("cut-outs", round(time.time() - t0, 1), sizes)

    # ---- the alts: each painted from the room in its state, over the patch it changes
    A_raw = A
    for name, grp, state in ALTS:
        r0 = bbox(np.maximum(cover(stA, grp=grp), 0) > 0.02)
        if name == "plant-droop":
            r0 = [r0[0] - 30, r0[1] - 10, r0[2] + 10, r0[3] + 10]
        if name == "door-open":
            x0, y0, x1, y1 = door_rect()
            r0 = [x0, y0, x1, y1]
        rect = clamp_rect(r0, 8)
        full, stP = patch_state(A_raw, state, rect)
        painted = P.details(P.paint(P.grade(P.wob(full)), 2), _maps_with_patch(stA, stP, rect))
        hall = R.hall_clip(stA).copy()
        hall[rect[1]:rect[3], rect[0]:rect[2]] = P.wob(np.pad(stP.down(stP.mask_of("hall").astype(F32)),
                                                              ((rect[1], H - rect[3]), (rect[0], W - rect[2]))))[rect[1]:rect[3], rect[0]:rect[2]]
        letters(painted, V, R.words(state), clips={"hall": hall})
        a = P.wob(group_mask_in(stP, grp, rect))
        covers[name] = a
        sizes[name] = finish(painted, f"{OUT}/{name}.png", 48, a)
        to_image(painted).save(f"{WORK}/alt-{name}.png")
        print("alt", name, round(time.time() - t0, 1))

    # ---- the frames of the things that move by nature: the clock's second hand, the bubble in the cooler
    frames = {}
    cx, cy, r = M.CLOCK
    pts = [V.pt(cx + dx, cy + dy, 4.6) for dx in (-r, r) for dy in (-r, r)]
    crect = clamp_rect((int(min(p[0] for p in pts)), int(min(p[1] for p in pts)), int(max(p[0] for p in pts)) + 1, int(max(p[1] for p in pts)) + 1), 3)
    files = []
    for k in range(60):
        pic, stc = R.render(ss=SS, fast=True, rect=crect, state=dict(hand=6.0 * k))
        pic = R.grade(pic, crect)
        a = cover(stc, grp="clockhand")
        save_frame(pic, a, f"{OUT}/second-{k:02d}.png", 8, seed=200 + k)
        files.append(f"second-{k:02d}.png")
    frames["second"] = crop_frames(files, crect[:2])
    print("second hand", round(time.time() - t0, 1), frames["second"]["rect"])
    files = []
    brect = bubble_rect()
    for k in range(7):
        pic, stb = R.render(ss=SS, fast=True, rect=brect, state=dict(bubble=k))
        pic = R.grade(pic, brect)
        a = cover(stb, grp="bubble")
        name = f"bubble-{k}" if k < 6 else "bubble-none"
        save_frame(pic, a, f"{OUT}/{name}.png", 8, seed=300 + k)
        files.append(f"{name}.png")
    frames["bubble"] = crop_frames(files, brect[:2])
    print("bubble", round(time.time() - t0, 1), frames["bubble"]["rect"])

    import office_room_layout
    office_room_layout.write(stA, stB, covers, frames)
    comp_all()
    office_room_layout.check()
    print("layout and comps", round(time.time() - t0, 1))


def bubble_rect():
    x0, x1, y0, y1, z0, z1 = M.COOLER
    cxj, czj = (x0 + x1) / 2, (z0 + z1) / 2
    pts = [V.pt(cxj + dx, Y, czj + dz) for dx in (-14, 14) for dz in (-14, 14) for Y in (100, 150)]
    return clamp_rect((int(min(p[0] for p in pts)), int(min(p[1] for p in pts)), int(max(p[0] for p in pts)) + 1, int(max(p[1] for p in pts)) + 1), 2)


def _maps_with_patch(stA, stP, rect):
    """The detail maps of the whole picture with the patch's own put in its place (the patch's things renamed to the
    whole picture's numbers, so that an edge is an edge in both)."""
    t, ny, oid, skip = P.maps_of(stA)
    t, ny, oid = t.copy(), ny.copy(), oid.copy()
    x0, y0, x1, y1 = rect
    remap = np.zeros(max(stP.names.values()) + 1, dtype=np.int32)
    nxt = max(stA.names.values()) + 1
    for nm, i in stP.names.items():
        if nm in stA.names:
            remap[i] = stA.names[nm]
        else:
            remap[i] = nxt
            nxt += 1
    pt_ = stP.pick(np.minimum(stP.t, 5000.0))
    pn = stP.pick(stP.N[..., 1])
    po = remap[stP.pick(stP.oid).astype(np.int32)]
    t[y0:y1, x0:x1] = pt_
    ny[y0:y1, x0:x1] = pn
    oid[y0:y1, x0:x1] = po
    return t, ny, oid, skip


def save_frame(pic, a, name, colors=16, seed=7):
    g = grain(pic, seed, 0.006)
    sel = g[a > 0.5] if (a > 0.5).any() else g.reshape(-1, 3)
    pal = palette_for(sel, colors)
    idx = to_palette(g, pal, speckle=0.003)
    save(name, idx, pal, a)


def crop_frames(files, origin=(0, 0)):
    """The frames of one moving thing are painted over their patch: crop them all to the box that holds every one of
    them, and say where that box is and where its foot is (the middle of its bottom edge). -> {files, at, foot, rect}"""
    ims = [Image.open(f"{OUT}/{f}") for f in files]
    boxes = [im.convert("RGBA").getchannel("A").getbbox() for im in ims]
    boxes = [b for b in boxes if b]
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


def lay(im, f, at=None, foot=None, folder=None):
    top = Image.open(f"{folder or OUT}/{f}").convert("RGBA")
    if at is None:
        im.alpha_composite(top)
    else:
        im.alpha_composite(top, (int(at[0] - foot[0]), int(at[1] - foot[1])))


def comp_all(folder=None, tag=""):
    """The scene's pictures laid together as the game lays them: at the start (the suits there, 72, the door shut), and
    later (hot: 81, the plant drooping, Ranger at the grille, the intercom pressed, the door open, the questionnaire gone)."""
    folder = folder or OUT
    L = json.load(open(f"{folder}/layout.json"))
    states = {
        "start": dict(show=("vent", "thermostat-72", "intercom", "door", "doorframe", "chair-corner", "table", "questionnaire", "plant", "front")),
        "later": dict(show=("vent-eyes", "thermostat-81", "intercom-lit", "door-open", "doorframe", "chair-corner", "table", "plant-droop", "front")),
    }
    for name, s in states.items():
        im = Image.open(f"{folder}/back.png").convert("RGBA")
        for fx in L["fx"]:
            lay(im, fx["frames"][0], fx["at"], fx["foot"], folder)
        for p in L["planes"]:
            if p["file"].replace(".png", "") in s["show"] and p.get("plane") != "front":
                lay(im, p["file"], folder=folder)
        for p in L["planes"]:
            if p.get("plane") == "front" and p["file"].replace(".png", "") in s["show"]:
                lay(im, p["file"], folder=folder)
        im.convert("RGB").save(f"out/office-room{tag}-comp-{name}.png")

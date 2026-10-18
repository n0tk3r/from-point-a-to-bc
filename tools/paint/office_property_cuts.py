"""The full run of office_property.py: the whole room painted (with everything, and without the cut-outs), the cut-outs
and their other states taken from it, layout.json, and the comps. OFFICE-17C.

The cut-outs (each 800x600, clear but for the thing, hard-edged):
    vent         the grille over the left run, plain (the backdrop has it too)
    vent-eyes    (alt) the same grille, two eyes in a black mask shining between its slats: Ranger is up there
    wall         the far wall round Opal's window and the door: the window's frame, her counter and everything on it, the
                 door's casing, the sign (whoever is in the hall is behind it, seen through the glass and the doorway)
    door         the door's leaf, shut (the backdrop shows the doorway open on the hall)
    door-open    (alt) the leaf swung out into the hall, seen past the jamb
    receipt      (alt) the receipt, lying on the counter where it lands (absent: not shown)
    banjo        the banjo in its bay, with its tag (gone: not shown; the backdrop has the bay empty)
    front        near us: the cart, the kick stool, the boxes on the floor"""

import json
import os
import time

import numpy as np
from PIL import Image

import office_property as R
import office_property_model as M
from office_room_kit import finish, to_image, tones, cover, bbox, clamp_rect, letters

OUT = R.OUT
WORK = R.WORK
W, H = 800, 600
V = R.V
P = R.P
DRAFT = os.environ.get("OFFICE_DRAFT") == "1"
SS = 1 if DRAFT else 2
FAST = DRAFT

# file name, group, palette size
CUT_FILES = [("vent", "vent", 40), ("banjo", "banjo", 64), ("door", "door", 48), ("front", "front", 64)]
# the alts: file, group, the state that paints it
ALTS = [("vent-eyes", "vent", dict(eyes=True)), ("door-open", "door", dict(door_open=True)), ("receipt", "receipt", dict(receipt=True))]


def wall_rect():
    """The patch of picture the far wall's cut-out may hold: the wall from a little left of the counter to the door's
    right, from the floor to over the sign and the door."""
    pts = [V.pt(X, Y, 0.0) for X in (M.COUNTER[0] - 6.0, M.DOOR[1] + 20.0) for Y in (0.0, 236.0)]
    pts += [V.pt(X, 0.0, M.COUNTER[5] + 2.0) for X in (M.COUNTER[0] - 6.0, M.COUNTER[1] + 2.0)]
    return (int(min(p[0] for p in pts)), int(min(p[1] for p in pts)), int(max(p[0] for p in pts)) + 1, int(max(p[1] for p in pts)) + 2)


def wall_mask(stA, others):
    """The far wall round the window and the door, and the group `wall` (the counter and what is on it, the window's
    frame, the casing, the sign): not the hall seen through the openings, not the room's floor, not another cut-out."""
    X, Y, Z = stA.places()
    wall = stA.down(((Z < 1.5) & (Z > -6.0) & ((stA.flag & 4) == 0)).astype(np.float32))
    m = np.zeros((H, W), np.float32)
    x0, y0, x1, y1 = wall_rect()
    m[y0:y1, x0:x1] = 1.0
    m = m * np.clip(wall * 2 - 0.5, 0, 1)
    m = np.maximum(m, cover(stA, grp="wall"))
    for o in others:
        m = m * (1 - np.clip(o * 2, 0, 1))
    return m


def patch_state(base_raw, state, rect, ss=SS):
    pic, st = R.render(ss=ss, fast=FAST, rect=rect, state=state)
    full = base_raw.copy()
    x0, y0, x1, y1 = rect
    full[y0:y1, x0:x1] = pic
    return full, st


def group_mask_in(st, grp, rect):
    m = np.zeros((H, W), np.float32)
    x0, y0, x1, y1 = rect
    m[y0:y1, x0:x1] = cover(st, grp=grp)
    return m


def _maps_with_patch(stA, stP, rect):
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
    t[y0:y1, x0:x1] = stP.pick(np.minimum(stP.t, 5000.0))
    ny[y0:y1, x0:x1] = stP.pick(stP.N[..., 1])
    oid[y0:y1, x0:x1] = remap[stP.pick(stP.oid).astype(np.int32)]
    return t, ny, oid, skip


def main(t0):
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    A, stA = R.render(ss=SS, fast=FAST)
    to_image(R.grade(A)).save(f"{WORK}/1-under.png")
    print("all", round(time.time() - t0, 1))
    # the room with the cut-outs taken away (their shadows stay where they fall); the plain grille stays in the backdrop
    B, stB = R.render(ss=SS, fast=FAST, skip=("banjo", "door", "wall", "front"), occ=stA.occ)
    print("back", round(time.time() - t0, 1))
    pA = R.paint_full(A, stA)
    pB = R.paint_full(B, stB, groups=("back", "hall"))
    to_image(pA).save(f"{WORK}/2-all.png")
    to_image(pB).save(f"{WORK}/2-back.png")
    tones(pA, "tones:")
    print("painted", round(time.time() - t0, 1))

    sizes = {"back": finish(pB, f"{OUT}/back.png", 160)}
    covers = {}
    for name, grp, colors in CUT_FILES:
        a = P.wob(cover(stA, grp=grp))
        covers[name] = a
        sizes[name] = finish(pA, f"{OUT}/{name}.png", colors, a)
    covers["wall"] = P.wob(wall_mask(stA, [covers[n] for n in ("vent", "banjo", "door", "front")]))
    sizes["wall"] = finish(pA, f"{OUT}/wall.png", 72, covers["wall"])
    print("cut-outs", round(time.time() - t0, 1), sizes)

    for name, grp, state in ALTS:
        if name == "door-open":
            dx0, dx1, dy0, dy1 = M.DOOR
            pts = [V.pt(X, Y, 0.0) for X in (dx0 - 10, dx1 + 10) for Y in (0.0, dy1 + 10)]
            r0 = [int(min(p[0] for p in pts)), int(min(p[1] for p in pts)), int(max(p[0] for p in pts)) + 1, int(max(p[1] for p in pts)) + 2]
        elif name == "receipt":
            rx, rz, _ = M.RECEIPT
            pts = [V.pt(rx + dx, M.COUNTER[3] + dy, rz + dz) for dx in (-12, 12) for dy in (-8, 4) for dz in (-12, 12)]
            r0 = [int(min(p[0] for p in pts)), int(min(p[1] for p in pts)), int(max(p[0] for p in pts)) + 1, int(max(p[1] for p in pts)) + 1]
        else:
            r0 = bbox(np.maximum(cover(stA, grp=grp), 0) > 0.02)
        rect = clamp_rect(r0, 8)
        full, stP = patch_state(A, state, rect)
        painted = P.details(P.paint(P.grade(P.wob(full)), 2), _maps_with_patch(stA, stP, rect))
        hall = R.hall_clip(stA).copy()
        hall[rect[1]:rect[3], rect[0]:rect[2]] = P.wob(np.pad(stP.down(stP.mask_of("hall").astype(np.float32)),
                                                              ((rect[1], H - rect[3]), (rect[0], W - rect[2]))))[rect[1]:rect[3], rect[0]:rect[2]]
        letters(painted, V, R.words(state), clips={"hall": hall})
        a = P.wob(group_mask_in(stP, grp, rect))
        covers[name] = a
        sizes[name] = finish(painted, f"{OUT}/{name}.png", 48, a)
        to_image(painted).save(f"{WORK}/alt-{name}.png")
        print("alt", name, round(time.time() - t0, 1))

    import office_property_layout
    office_property_layout.write(stA, stB, covers)
    comp_all()
    office_property_layout.check()
    print("layout and comps", round(time.time() - t0, 1))


def lay(im, f, folder=None):
    im.alpha_composite(Image.open(f"{folder or OUT}/{f}").convert("RGBA"))


def comp_all(folder=None, tag=""):
    """The scene's pictures laid together as the game lays them: at the start (the banjo on its shelf, the door shut, no
    receipt), and later (the receipt on the counter, Ranger at the grille, the banjo gone, the door open)."""
    folder = folder or OUT
    L = json.load(open(f"{folder}/layout.json"))
    states = {
        "start": ("vent", "wall", "door", "banjo", "front"),
        "later": ("vent-eyes", "wall", "receipt", "door-open", "front"),
    }
    for name, show in states.items():
        im = Image.open(f"{folder}/back.png").convert("RGBA")
        for p in L["planes"]:
            if p["file"].replace(".png", "") in show and p.get("plane") != "front":
                lay(im, p["file"], folder)
        for p in L["planes"]:
            if p.get("plane") == "front" and p["file"].replace(".png", "") in show:
                lay(im, p["file"], folder)
        im.convert("RGB").save(f"out/office-property{tag}-comp-{name}.png")

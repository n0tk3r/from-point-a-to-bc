"""The gray limousine, parked in the Office's lot (OFFICE-17A): the same car as the roadside's (PAINT-12A's drawing,
nevada_roadside_limo.py: every measurement, panel, window, chrome strip and the plate are its own), drawn here through
the lot's camera where it stands, in the lot's light, as a cut-out in place; and the same with its rear door open.

Why not the roadside's own pictures (limo-side-0/1.png): they are the car in the morning, the sun low on the right, a
long shadow out to the left and its nose catching the light. At this hour the sun is high and behind us on the left:
the near side is in the sun, the tail turns toward it, the nose away, and its shadow is short and falls back behind it,
almost all hidden under it. So it is painted again, the same car at the same size the game would scale the roadside's
to here (it is exactly what that camera sees), and the roadside's files are left as they were.

    car     near side on z 640 (its foot line on row 393), the tail at x 205, nose to the right (the front bumper just
            past the picture's right edge); limo.png
    open    the back pair's rear door (164 to 233 cm from the tail) swung open 50 degrees on its front hinges: we see
            its outside, turned toward the tail, and in the opening the back seat; limo-door-open.png"""

import math

import numpy as np

from brush import F32, blur, grid, lerp, noise, over, rgb
import nevada_roadside_limo as RL
from nevada_roadside_kit import Paper, Solid, brushed
import office_lot_kit as K

AT = (K.LIMO["tail"], K.LIMO["z"])                       # the car's rear near corner, on the ground
L, WID = RL.L, RL.WID
HINGE = 233.0                                            # the rear door's front edge, where it is hung
FREE = 164.0                                             # its back edge
SWING = K.LIMO["swing"]

# the lot's light on the same gray car: the near side in the sun (lighter than in the roadside's half light)
PAINT = dict(RL.PAINT, side="#9a9ea8", sky="#c8d2e0", sky2="#b4bccb", land="#7c7e8c", floor="#b7aa9a", under="#5e5d68", sill="#40404a",
             roof="#aeb2bc", roof_sun="#e4ddd4", roof_sky="#c2cad8", hood="#b4b6bd", trunk="#aaacb3", pillar="#7a7e8a", shoulder="#a8acb6",
             far="#8a8e9c")


def side_bands(shape, d, side_pts):
    """What the near side holds, as polished paint does: the sky along its shoulder, the far land as a dark line, the
    lit gravel below, its underside turning away; the tail end turning toward the sun (warm), the nose end away (cool)."""
    zs = 0.0
    sm = RL.mask_poly(shape, d.pts([(x, y, zs) for x, y in side_pts]))
    s = Paper(shape)
    x0, x1 = -10.0, L + 10.0
    for (y0, y1, c, al) in ((95.0, 100.5, PAINT["sky"], 0.9), (86.0, 95.0, PAINT["sky2"], 0.75), (79.0, 86.0, PAINT["land"], 0.65),
                            (56.0, 79.0, PAINT["floor"], 0.40), (38.0, 56.0, PAINT["under"], 0.45), (RL.SILL - 2.0, RL.SILL + 11.0, PAINT["sill"], 0.85)):
        s.poly(d.pts([(x0, y0, zs), (x1, y0, zs), (x1, y1, zs), (x0, y1, zs)]), c, al)
    # the tail turns toward the sun: its corner warm; the nose turns away from it: cool and darker
    s.poly(d.pts([(-1, 26, zs), (16, 28, zs), (22, 92, zs), (8, 96, zs), (-1, 90, zs)]), "#e6d6c4", 0.55)
    s.poly(d.pts([(596, 30, zs), (629.5, 36, zs), (629.5, 86, zs), (620, 94, zs), (600, 96, zs)]), "#5c6070", 0.45)
    c, a = s.done()
    return c, a * sm


def body_layers(shape, open_door=False, seed=4, fast=False):
    """-> [(name, color, hard alpha)] back to front: the dark under it, the wheels, the body (with its door open or
    not), the open door's leaf."""
    out = []
    # ---- under the car: the gravel in its shadow, darkest where the tires stand (its shadow falls behind it, hidden)
    u, t = Paper(shape), Paper(shape)
    du, dt = Solid(u, AT, 0.0, cam=K.CAM), Solid(t, AT, 0.0, cam=K.CAM)
    for z0, al in ((-2.0, 0.40), (8.0, 0.70), (26.0, 1.0)):
        du.poly([(10, 0, z0), (620, 0, z0), (620, 0, 150), (10, 0, 150)], "#000000", al)
    for ax in (RL.R_AX, RL.F_AX):
        dt.poly([(ax - 26, 0, -1.0), (ax + 26, 0, -1.0), (ax + 30, 0, 26), (ax - 30, 0, 26)], "#000000")
    deep, touch = u.done()[1], t.done()[1]
    shade = np.empty(shape + (3,), F32)
    shade[...] = rgb("#8a8494")
    over(shade, "#4a4452", np.clip(deep, 0, 1) * 0.8)
    over(shade, "#2c2632", np.clip(touch, 0, 1) * 0.9)
    out.append(("under", shade, (np.maximum(deep, touch) > 0.5).astype(F32)))
    # ---- the wheels (still: it is parked)
    base, lines = Paper(shape), Paper(shape)
    RL.draw_wheels(Solid(base, AT, 0.0, cam=K.CAM), Solid(lines, AT, 0.0, cam=K.CAM), 0.0)
    c, a = base.done()
    lc, la = lines.done()
    pc, pa = brushed(c, a, lc, la, "#2a2830", seed=seed + 1, sizes=(4, 2), keep=0.55, fast=fast)
    out.append(("wheels", pc, (pa > 0.5).astype(F32)))
    # ---- the body: the tops, the near side with its reflections, everything it carries; the plate
    base, lines = Paper(shape), Paper(shape)
    notes = []
    d, dl = Solid(base, AT, 0.0, cam=K.CAM), Solid(lines, AT, 0.0, cam=K.CAM)
    RL.draw_tops(d, dl, paint=PAINT)
    side = RL.profile(d)
    d.poly(side, PAINT["side"])
    c, a = base.done()
    bc, ba = side_bands(shape, d, side)
    over(c, bc, ba)
    RL.draw_side_things(d, dl, notes, paint=PAINT)
    lc, la = lines.done()
    import nevada_roadside_props as RP
    RP.letter_on(lc, la, notes)
    if open_door:
        # the opening where the door was: the back seat in the dark of the car, the far side's smoked glass
        hole, hl = Paper(shape), Paper(shape)
        dh, dhl = Solid(hole, AT, 0.0, cam=K.CAM), Solid(hl, AT, 0.0, cam=K.CAM)
        opening = [(FREE, RL.SILL + 1.0), (HINGE, RL.SILL + 1.0), (HINGE, 133.5), (FREE + 2.0, 133.5)]
        dh.poly([(x, y, 0.0) for x, y in opening], "#1c1a22")
        dh.poly([(FREE + 2, 104.0, WID - 20), (HINGE - 2, 104.0, WID - 20), (HINGE - 2, 130.0, WID - 20), (FREE + 2, 130.0, WID - 20)], "#3a4252")   # the far window
        dh.poly([(FREE, 42.0, 60.0), (HINGE, 42.0, 60.0), (HINGE, 42.0, 150.0), (FREE, 42.0, 150.0)], "#4a3a44")      # the seat's cushion
        dh.poly([(FREE, 42.0, 150.0), (HINGE, 42.0, 150.0), (HINGE, 96.0, 168.0), (FREE, 96.0, 168.0)], "#3c2e38")    # its back
        dhl.line([(FREE, 42.0, 60.0), (HINGE, 42.0, 60.0)], "#6a5660", 1.2, 0.9)
        dh.poly([(FREE, RL.SILL + 1.0, 0.0), (HINGE, RL.SILL + 1.0, 0.0), (HINGE, RL.SILL + 1.0, 30.0), (FREE, RL.SILL + 1.0, 30.0)], "#2a2a30")  # the sill
        dhl.line([(FREE, RL.SILL + 1.2, 0.0), (HINGE, RL.SILL + 1.2, 0.0)], "#c9d4e4", 1.0, 0.9)
        hc, ha = hole.done()
        hlc, hla = hl.done()
        om = RL.mask_poly(shape, d.pts([(x, y, 0.0) for x, y in opening]))
        over(c, hc, ha * om)
        over(lc, hlc, hla * om)
        la[...] = la * (1 - om) + hla * om
    pc, pa = brushed(c, a, lc, la, "#7c7e88", seed=seed, sizes=(6, 3, 2), keep=0.42, fast=fast)
    out.append(("body", pc, (pa > 0.5).astype(F32)))
    if open_door:
        out.append(("leaf",) + leaf(shape, seed=seed + 3, fast=fast))
    return out


def leaf(shape, seed=7, fast=False):
    """The open door itself: hung on its front edge (x 233), its back edge swung out toward us by SWING degrees. We see
    its outside: the gray panel, the smoked window in its frame, the chrome, the handle; its back edge lit."""
    a_ = math.radians(SWING)
    ca, sa = math.cos(a_), math.sin(a_)

    def sw(x, y, z=0.0):
        dx = x - HINGE                                                          # (turned about the hinge: the back edge comes toward us)
        return (HINGE + dx * ca - z * sa, y, dx * sa + z * ca)
    base, lines = Paper(shape), Paper(shape)
    d, dl = Solid(base, AT, 0.0, cam=K.CAM), Solid(lines, AT, 0.0, cam=K.CAM)
    f = K.lambert((sa, 0.0, -ca))                                               # its outer face's normal, turned with it (to our right)
    panel = K.lit(PAINT["side"], f)
    win = [(FREE + 4, 104), (FREE + 4, 133.5), (HINGE - 4, 133.5), (HINGE - 4, 104)]
    d.poly([sw(FREE, RL.SILL + 2), sw(HINGE, RL.SILL + 2), sw(HINGE, 133.5), sw(FREE + 1, 133.5)], panel)
    d.poly([sw(x, y, -0.4) for x, y in win], RL.GLASS["dark"])
    dl.poly([sw(FREE + 7, 132.0, -0.5), sw(FREE + 15, 132.0, -0.5), sw(FREE + 7, 106.0, -0.5), sw(FREE + 1, 106.0, -0.5)], RL.GLASS["sheen"], 0.5)
    dl.line([sw(x, y, -0.6) for x, y in win] + [sw(win[0][0], win[0][1], -0.6)], RL.CHROME["mid"], 1.4, 0.95)
    dl.line([sw(FREE, RL.BELT, -0.8), sw(HINGE, RL.BELT, -0.8)], RL.CHROME["light"], 1.1, 0.95)
    dl.line([sw(FREE + 2, 88, -1.2), sw(FREE + 11, 88, -1.2)], RL.CHROME["dark"], 2.4)
    dl.line([sw(FREE + 2, 88.8, -1.4), sw(FREE + 10, 88.8, -1.4)], RL.CHROME["light"], 1.0)
    dl.line([sw(FREE, RL.SILL + 2), sw(FREE, 133.5)], "#f2ece2", 1.2, 0.9)       # its back edge, catching the sun
    dl.line([sw(FREE, RL.SILL + 2), sw(HINGE, RL.SILL + 2)], "#2c2c34", 1.0, 0.8)
    c, a = base.done()
    lc, la = lines.done()
    pc, pa = brushed(c, a, lc, la, "#7c7e88", seed=seed, sizes=(4, 2), keep=0.5, fast=fast)
    return pc, (pa > 0.5).astype(F32)


def car(shape, open_door=False, fast=False):
    """The whole car as one cut-out: -> (color, alpha)."""
    pic = np.zeros(shape + (3,), F32)
    alpha = np.zeros(shape, F32)
    for name, c, a in body_layers(shape, open_door, fast=fast):
        over(pic, c, a)
        alpha = np.maximum(alpha, a)
    return pic, alpha


def measure():
    """Where it stands, in picture pixels: its foot line's row, its x range, its foot point (as the roadside's frames
    give theirs: the middle of the ground line under the near side, half way between the wheels), and the open door's
    place."""
    foot = K.P(AT[0] + RL.MID, 0.0, AT[1])
    a = math.radians(SWING)
    free = (AT[0] + HINGE + (FREE - HINGE) * math.cos(a), AT[1] + (FREE - HINGE) * math.sin(a))
    return {"foot": [round(foot[0], 1), round(foot[1], 1)], "row": round(foot[1], 1), "scale": round(K.scale_at(AT[1]), 4),
            "tail_x": round(K.P(AT[0], 0, AT[1])[0], 1), "nose_x": round(K.P(AT[0] + L, 0, AT[1])[0], 1),
            "door": {"hinge": [round(v, 1) for v in K.P(AT[0] + HINGE, 0, AT[1])], "free": [round(v, 1) for v in K.P(free[0], 0, free[1])],
                     "opening": [round(K.P(AT[0] + FREE, 0, AT[1])[0], 1), round(K.P(AT[0] + HINGE, 0, AT[1])[0], 1)]}}

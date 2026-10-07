"""The stone of the pyramid for egypt_site.py: its two faces seen close, course by course and block by
block, and the notch of the doorway cut into the shaded one. Worked out once and kept, because the
block-in and the crisp pass both need it."""

import math

import numpy as np

from egypt_site_kit import *
from egypt_site_plan import *

_kept = {}


def _tile(seed, cell):
    return noise((512, 512), cell, seed, 3)


def shaded_face(seed=21):
    """The face we mostly see, in cool shade. -> dict(color, mask, joints, light, rough, s, v, zc)."""
    if "shade" in _kept:
        return _kept["shade"]
    shape = (H, W)
    rng = np.random.default_rng(seed)
    s, v, zc, on = SHADE.coords(shape)
    s = s + (noise(shape, 26, seed + 30, 2) - 0.5) * 3.0                      # nothing is ruled: joints wander a finger's width
    v = v + (noise(shape, 26, seed + 31, 2) - 0.5) * 3.0
    k, tone, dv, ds, fv, fs, wide, levels = masonry(s, v, on, seed + 1)
    tall = (levels[k + 1] - levels[k]).astype(F32)
    m = mask_poly(shape, [SHADE.pt(0, 0), SHADE.pt(1500 / TAN, 1500), (W + 80, -80), (W + 80, SHADE.pt(2700, 0)[1]), SHADE.pt(2700, 0)], wobble=0.5, seed=seed)

    # ---- its color: lilac, deeper and bluer up toward the sky, warmer below where the sand throws light back up
    th = np.clip(v / 1150.0, 0, 1)
    col = ramp(th, [(0.0, "#c0abb0"), (0.16, "#b1a1b6"), (0.5, "#a19cc2"), (1.0, "#8c8ec0")])
    col *= (1 - 0.17 * np.clip((s - 500) / 1500, 0, 1) * (0.25 + 0.75 * th))[..., None]   # and deeper toward the top right corner
    rows = rng.normal(0, 1, len(levels)).astype(F32)
    streak = sample(_tile(seed + 3, (5, 70)), mirror(s * 0.30, 508), mirror(v * 0.30, 508)) - 0.5
    patch = noise(shape, (150, 90), seed + 4, 3) - 0.5
    col *= (1 + rows[k] * 0.028 + (tone - 0.5) * 0.10 + streak * 0.07 + patch * 0.07)[..., None]
    col *= (1 + (fv - 0.5) * 0.055 + (0.5 - fs) * 0.02)[..., None]              # each block a touch lighter toward its top and its left: the face is not dead flat
    stain = ((tone * 5.31) % 1.0 > 0.86)                                       # a block here and there has kept the quarry's tan
    col = np.where(stain[..., None], col * np.array([1.02, 0.97, 0.90], dtype=F32), col)
    over(col, "#dcc6b6", (np.exp(-np.clip(v, 0, None) / 46.0) * 0.34).astype(F32))    # dust and thrown-up light along the foot
    col *= (1 - 0.05 * np.exp(-np.clip(s - v / TAN, 0, None) / 160.0))[..., None]   # a shade darker against the bright edge

    # ---- blocks not yet dressed: they stand a hand proud of the face, rough, with the bosses they were levered by
    sc = s - (fs - 0.5) * wide                                                 # each block's own middle
    vc = (levels[k] + levels[k + 1]) / 2
    pick = (tone * 7.13) % 1.0
    work = ((sc > 1490) & (sc < 2120) & (vc > 200) & (vc < 1030))              # where the scaffold stands the masons are not done
    chance = np.where(work, 0.86, 0.045)
    chance = np.where((k == 0) & (sc < 560), 0.42, chance)
    chance = np.where((sc > NOTCH_S - 420) & (sc < NOTCH_S + 420) & (vc > SILL - 80) & (vc < SILL + NOTCH_H + 120), 0.0, chance)   # round the door it is finished
    rough = on & (pick < chance)
    grit = noise(shape, 3.2, seed + 5, 2) - 0.5
    a, b = fs * wide, (1 - fs) * wide                                          # cm from the block's left and right ends
    c, e = fv * tall, (1 - fv) * tall                                          # cm from its bottom and top
    bulge = (0.5 - fs) * 0.05 + (fv - 0.5) * 0.07
    rc = col * np.array([1.0, 0.965, 0.90], dtype=F32) * (0.955 + grit * 0.10 + bulge)[..., None]
    over(rc, "#ffe6b8", np.clip(1 - a / 7.0, 0, 1) * 0.62)                     # their left ends catch the sun that slides along the face
    over(rc, "#dcd6ee", np.clip(1 - e / 6.0, 0, 1) * 0.45)                     # top edge: sky
    over(rc, "#5e5886", np.clip(1 - b / 9.0, 0, 1) * 0.55)                     # right end and underside: dark
    over(rc, "#5a5482", np.clip(1 - c / 10.0, 0, 1) * 0.62)
    for at in (0.30, 0.70):                                                    # the bosses
        has = (((tone * 13.7 + at) % 1.0) < 0.62) & (wide > 150)
        du, dw = (fs - at) * wide, (fv - 0.40) * tall
        r = np.hypot(du / 15.0, dw / 11.0)
        knob = np.clip((1.0 - r) * 3.0, 0, 1) * has
        lit_side = np.clip(0.5 + (-du * 0.7 + dw) / 14.0, 0, 1)
        over(rc, ramp(lit_side, [(0.0, "#595482"), (0.5, "#a89cb8"), (1.0, "#ffe9c4")]), knob.astype(F32))
        fall = np.clip((1.0 - np.hypot((du - 11) / 15.0, (dw + 9) / 9.0)) * 2.0, 0, 1) * has * (1 - knob)
        over(rc, "#5a5482", (fall * 0.5).astype(F32))
    col = np.where(rough[..., None], rc, col)

    chip = ((tone * 9.77) % 1.0 > 0.72) & ~rough                                # a corner knocked off, here and there
    corner = np.clip(1 - (np.minimum(a, b) + e * 1.3) / 15.0, 0, 1) * chip
    over(col, "#6a6492", (corner * 0.7).astype(F32))
    under_door = np.clip(1 - np.abs(s - (NOTCH_S - 40)) / (NOTCH_W * 0.55), 0, 1) * np.clip((SILL - v) / 150.0, 0, 1) * (v < SILL)
    grime = under_door * (0.5 + 0.9 * sample(_tile(seed + 7, (4, 90)), mirror(s * 0.5, 508), mirror(v * 0.2, 508)))
    over(col, "#8e7c8c", np.clip(grime * 0.30, 0, 1).astype(F32))             # dust trodden off the landing has run down the stone

    # ---- joints: hairlines between dressed blocks, deeper round rough ones
    broken = 0.55 + 0.45 * step(0.25, 0.6, noise(shape, (40, 12), seed + 6, 3))
    level = joint(dv, zc, 1.0) * broken
    upright = joint(ds, zc, 0.9) * broken
    joints = np.maximum(level, upright) * on
    lightline = np.clip(1 - np.abs(e - 4.5) / 2.2, 0, 1) * on * (1 - rough) * broken     # the arris of the block below catches a little sky
    out = dict(color=np.clip(col, 0, 1).astype(F32), mask=m, joints=joints.astype(F32), light=lightline.astype(F32), rough=(rough * m).astype(F32),
               s=s, v=v, zc=zc, on=on, k=k)
    _kept["shade"] = out
    return out


def lit_face(seed=21):
    """The narrow face in the sun: a glowing, warm white wedge, seen almost edge-on."""
    if "lit" in _kept:
        return _kept["lit"]
    shape = (H, W)
    rng = np.random.default_rng(seed + 50)
    s, v, zc, on = LIT.coords(shape)
    v = v + (noise(shape, 30, seed + 32, 2) - 0.5) * 3.0 * np.clip(zc / 3000.0, 1, 3)          # the beds wander a finger's width
    k, tone, dv, ds, fv, fs, wide, levels = masonry(s, v, on, seed + 11, top=7000.0)
    m = mask_poly(shape, [LIT.pt(0, 0), LIT.pt(BASE, 0), LIT.pt(BASE - 6000 / TAN, 6000), LIT.pt(6000 / TAN, 6000)], wobble=0.4, seed=seed + 1)
    th = np.clip(v / 2600.0, 0, 1)
    col = ramp(th, [(0.0, "#f3c984"), (0.25, "#f9dca4"), (1.0, "#fff0c4")])
    far = np.clip((zc - CORNER_ZC) / 9000.0, 0, 1)
    rows = rng.normal(0, 1, len(levels)).astype(F32)
    streak = sample(_tile(seed + 13, (5, 70)), mirror(s * 0.12, 508), mirror(v * 0.30, 508)) - 0.5
    col *= (1 + (rows[k] * 0.045 + (tone - 0.5) * 0.085 + streak * 0.06) * (1 - far * 0.6)[...] + (noise(shape, (90, 60), seed + 14, 3) - 0.5) * 0.06)[..., None]
    near = np.exp(-np.clip(s - v / TAN, 0, None) / 500.0)                      # hottest just beside the near edge
    over(col, "#fff8dc", (near * 0.45).astype(F32))
    over(col, "#f6e2bc", (far ** 0.8 * 0.38).astype(F32))                       # air: the far end pales
    size = 105.0 * FOC / np.maximum(zc, 1.0)                                    # how many pixels a course is, there
    show = np.clip((size - 4.0) / 16.0, 0.0, 1.0)
    level = joint(dv, zc, 1.0) * show
    upright = joint(ds, zc, 0.9, squash=0.45) * show * np.clip((size - 9) / 12.0, 0, 1)   # seen so much on edge the upright joints nearly vanish
    out = dict(color=np.clip(col, 0, 1).astype(F32), mask=m, joints=(np.maximum(level, upright) * on).astype(F32), s=s, v=v, zc=zc, on=on, far=far.astype(F32))
    _kept["lit"] = out
    return out


def lay_faces(picture, amount=1.0, joints=0.4, seed=21):
    """Paint both faces onto the picture. `amount` under 1 lets what is already there show through
    (for saying them again over brushwork); `joints` is how dark the joints are drawn."""
    sf, lf = shaded_face(seed), lit_face(seed)
    lit = lf["color"].copy()
    over(lit, "#c28c5a", np.clip(lf["joints"] * joints * 1.15, 0, 1))
    over(picture, lit, lf["mask"] * amount)
    sh = sf["color"].copy()
    over(sh, "#dcd8f0", sf["light"] * joints * 0.5)
    over(sh, "#5f5a88", sf["joints"] * joints * (0.75 + 0.6 * sf["rough"]))
    over(picture, sh, sf["mask"] * amount)
    return picture


def entrance(shape, crisp=False):
    """The notch in the shaded face, its upright back wall with the doorway, and the two great slabs
    leaning together over it. -> (color, mask). Flat planes first; with `crisp`, joints and edges too."""
    s0, s1 = NOTCH_S - NOTCH_W / 2, NOTCH_S + NOTCH_W / 2
    top = SILL + NOTCH_H
    hw = NOTCH_W / 2
    u0, u1 = DOOR_OFF - DOOR_W / 2, DOOR_OFF + DOOR_W / 2
    opening = [SHADE.pt(s0, SILL), SHADE.pt(s1, SILL), SHADE.pt(s1, top), SHADE.pt(s0, top)]
    sheet = Paper(shape)
    sheet.poly([backp(-hw - 200, -20), backp(hw + 200, -20), backp(hw + 200, NOTCH_H + 20), backp(-hw - 200, NOTCH_H + 20)], "#7b78a6")       # the back wall
    sheet.poly([backp(hw, 0), SHADE.pt(s1, SILL), backp(hw, NOTCH_H)], "#a898ae")                 # the right cheek takes light thrown up from the sand
    sheet.poly([backp(-hw - 200, 0), backp(hw, 0), SHADE.pt(s1, SILL), SHADE.pt(s0 - 200, SILL)], "#c6b4b6")   # the floor of the notch
    # the wall is darker up under the overhang of the slope, and in its left corner
    sheet.poly([backp(-hw - 200, NOTCH_H + 20), backp(hw, NOTCH_H + 20), backp(hw, NOTCH_H - 60), backp(-hw - 200, NOTCH_H - 110)], "#5c5a8a", 0.55)
    sheet.poly([backp(-hw - 200, 0), backp(-hw + 150, 0), backp(-hw + 60, NOTCH_H), backp(-hw - 200, NOTCH_H)], "#5c5a8a", 0.40)
    # the two great slabs, leaning together like a gable, and the lintel they stand on
    spring, peak, thick = DOOR_H + LINTEL, NOTCH_H - 26.0, 84.0
    reach = DOOR_W / 2 + 104
    inner = reach - thick * 1.2

    def slab(sgn):
        return [backp(DOOR_OFF + sgn * reach, spring), backp(DOOR_OFF, peak), backp(DOOR_OFF, peak - thick), backp(DOOR_OFF + sgn * inner, spring)]
    sheet.poly([backp(DOOR_OFF - inner, spring), backp(DOOR_OFF, peak - thick), backp(DOOR_OFF + inner, spring)], "#5d5a88")      # the wall under them, in their shade
    sheet.poly(slab(-1), "#b3acd0")
    sheet.poly(slab(1), "#9f99c2")
    sheet.poly([backp(u0 - 58, DOOR_H), backp(u1 + 58, DOOR_H), backp(u1 + 58, spring), backp(u0 - 58, spring)], "#b8b1d2")       # lintel
    # the doorway: dark, and a little warm far inside where a lamp is burning
    sheet.poly([backp(u0, 0), backp(u1, 0), backp(u1, DOOR_H), backp(u0, DOOR_H)], "#1f1828")
    sheet.poly([backp(u1 - 46, 0), backp(u1, 0), backp(u1, DOOR_H), backp(u1 - 46, DOOR_H - 34)], "#382834", 0.95)                # its right reveal
    sheet.poly([backp(u1 - 46, 0), backp(u1 - 22, 0), backp(u1 - 32, DOOR_H * 0.5), backp(u1 - 46, DOOR_H * 0.58)], "#7a4c34", 0.55)
    sheet.poly([backp(u0, 0), backp(u1 - 46, 0), backp(u1 - 46, 26), backp(u0, 14)], "#4a3a44", 0.6)                                # the passage floor going in
    if crisp:
        edge, dark, light = "#514d7a", "#3a3660", "#d6d1ea"
        for vv in (104.0, 210.0, 302.0, 396.0):                                             # beds of the back wall's big blocks
            for ua, ub in ((-hw - 200, u0 - (58 if vv > DOOR_H else 0)), (u1 + (58 if vv > DOOR_H else 0), hw)):
                if vv > spring:
                    half = reach * (peak - vv) / (peak - spring) + 4
                    ua, ub = (ua, DOOR_OFF - half) if ub < DOOR_OFF else (DOOR_OFF + half, ub)
                if ub > ua:
                    sheet.line([backp(ua, vv), backp(ub, vv)], edge, 0.9, 0.55)
        for uu, va, vb in ((-hw + 110, 0, 104), (u1 + 62, 0, 104), (-hw + 168, 104, 210), (u1 + 26, 104, 210), (hw - 46, 210, 302), (-hw + 120, 210, 302), (-hw + 150, 302, 396), (hw - 30, 302, 396)):
            if not (u0 - 4 < uu < u1 + 4):
                sheet.line([backp(uu, va), backp(uu, vb)], edge, 0.9, 0.5)
        for sgn in (-1, 1):                                                                 # the slabs: light along their backs, dark beneath
            q = slab(sgn)
            sheet.line([q[0], q[1]], light, 1.1, 0.85)
            sheet.line([q[3], q[2]], dark, 1.2, 0.9)
            sheet.line([q[0], q[3]], edge, 1.0, 0.7)
            sheet.line([backp(DOOR_OFF + sgn * (reach - 30), spring + 6), backp(DOOR_OFF + sgn * 26, peak - thick * 0.45)], edge, 0.7, 0.3)   # a bed in the stone
        sheet.line([backp(DOOR_OFF, peak), backp(DOOR_OFF, peak - thick)], dark, 1.1, 0.9)  # where the two meet
        sheet.line([backp(u0 - 58, spring), backp(u1 + 58, spring)], light, 1.0, 0.8)
        sheet.line([backp(u0 - 58, DOOR_H), backp(u0, DOOR_H)], dark, 1.0, 0.75)
        sheet.line([backp(u1, DOOR_H), backp(u1 + 58, DOOR_H)], dark, 1.0, 0.75)
        sheet.line([backp(u0 - 58, DOOR_H), backp(u0 - 58, spring)], edge, 0.9, 0.7)
        sheet.line([backp(u1 + 58, DOOR_H), backp(u1 + 58, spring)], edge, 0.9, 0.7)
        sheet.line([backp(u0, 0), backp(u0, DOOR_H), backp(u1, DOOR_H)], "#120e18", 1.2, 0.95)      # the doorway's own edges
        sheet.line([backp(u1 + 1, 0), backp(u1 + 1, DOOR_H)], "#9790b8", 1.0, 0.8)
        sheet.line([backp(u0 - 2, 0), backp(u0 - 2, DOOR_H)], "#aaa4c8", 0.9, 0.6)
        sheet.line([backp(hw, 0), backp(hw, NOTCH_H)], edge, 1.0, 0.75)                             # the corner of wall and cheek
    color, alpha = sheet.done()
    alpha = alpha * mask_poly(shape, opening, wobble=0.4, seed=3)
    if crisp:                                                                               # the cut edges of the casing round the notch
        rim = Paper(shape)
        rim.line([SHADE.pt(s0, SILL), SHADE.pt(s0, top), SHADE.pt(s1, top)], "#3a3660", 1.3, 0.85)
        rim.line([SHADE.pt(s0 - 3, SILL), SHADE.pt(s0 - 3, top)], "#d6d1ea", 0.9, 0.5)
        rim.line([SHADE.pt(s1, SILL), SHADE.pt(s1, top)], "#d6d1ea", 1.0, 0.6)
        rim.line([SHADE.pt(s0, SILL), SHADE.pt(s1, SILL)], "#e6dadc", 1.0, 0.7)             # the sill's front edge
        rc, ra = rim.done()
        color = color * (1 - ra[..., None]) + rc * ra[..., None]
        alpha = np.maximum(alpha, ra)
    return color, alpha


def masons_marks(sheet, seed=23):
    """Red ochre on the shaded face: levelling lines snapped with a string, a setting mark or two. (Invented signs.)"""
    rng = np.random.default_rng(seed)
    red = "#a8463a"
    for (s, v, long) in ((250, 118, 150), (640, 228, 120), (1420, 118, 170), (860, 760, 130)):
        pts = [SHADE.pt(s + t * long, v + rng.normal(0, 1.2)) for t in np.linspace(0, 1, 5)]
        sheet.line(pts, red, 0.9, 0.45)
        a = SHADE.pt(s + long * 0.5, v)
        b = SHADE.pt(s + long * 0.5, v + 26)
        sheet.line([a, b], red, 0.9, 0.5)                                       # a tick up from it
        if rng.random() < 0.7:
            c = SHADE.pt(s + long + 22, v + 16)
            sheet.line([(c[0] - 2.5, c[1] + 2.5), (c[0], c[1] - 3), (c[0] + 2.5, c[1] + 2.5)], red, 0.9, 0.55)
            sheet.ellipse(c[0] + 6, c[1], 1.0, 1.0, red, 0.6)
    return sheet

"""Things people built: pyramids, ramps, huts, boats, squared blocks. Each is a few flat faces, a
warm lit one and a cool shaded one, with the joints of the stone drawn over them."""

import math

import numpy as np

from brush import F32, Sheet, blur, grid, lerp, mask_ellipse, mask_poly, noise, over, ramp, rgb, tint, vary


def _p(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _on(base0, base1, apex, s, f):
    """A place on a pyramid's face: `s` along the base (0 to 1), `f` up toward the apex (0 to 1)."""
    return _p(_p(base0, base1, s), apex, f)


def face(picture, apex, base0, base1, top, tones, seed, courses=44, band=0.045, streak=0.05, wobble=0.6):
    """One face of a pyramid, from its base (base0 to base1) up to where the building has got (`top`, 0 to 1).
    `tones` are (color near the top, color at the base). The stone lies in level courses, each a touch
    lighter or darker than the next, and each made of blocks that differ a little again."""
    shape = picture.shape[:2]
    x, y = grid(shape)
    A, L, C = apex, base0, base1
    den = (A[0] - L[0]) * (C[1] - L[1]) - (A[1] - L[1]) * (C[0] - L[0])
    f = ((x - L[0]) * (C[1] - L[1]) - (y - L[1]) * (C[0] - L[0])) / den               # 0 on the base line, 1 at the apex
    bx, by = C[0] - L[0], C[1] - L[1]
    s = ((x - L[0]) * bx + (y - L[1]) * by) / (bx * bx + by * by)
    quad = [_p(L, A, top), _p(C, A, top), C, L]
    m = mask_poly(shape, quad, wobble=wobble, seed=seed)
    rng = np.random.default_rng(seed)
    color = ramp(np.clip(f / max(top, 1e-3), 0, 1), [(0.0, tones[1]), (1.0, tones[0])])
    k = np.clip((f * courses).astype(int), 0, courses)
    rows = rng.normal(0, 1, courses + 2).astype(F32)
    blocks = rng.normal(0, 1, (courses + 2, 64)).astype(F32)
    j = np.clip((s * 46 + k * 0.37).astype(int) % 64, 0, 63)
    tone = rows[k] * band + blocks[k, j] * band * 0.7
    tone += (noise(shape, (6, 60), seed + 3, 3) - 0.5) * 2 * streak                    # dust and rain run down the face
    tone += (noise(shape, (90, 40), seed + 4, 3) - 0.5) * 2 * band                     # and big patches, as paint is uneven
    color = color * (1 + tone[..., None])
    over(picture, np.clip(color, 0, 1), m)
    return m


def pyramid(picture, apex, left, corner, right, seed, lit=("#fff2cf", "#f3d397"), shade=("#a9a8c8", "#b4a3b0"), built=1.0,
            courses=44, haze=None, haze_amount=0.3, edge="#fffbe6", top_color="#c9a878"):
    """A pyramid seen corner-on: `left` and `right` are the far ends of its base, `corner` the near one.
    The left face is in the sun and the right face in shade. `built` under 1 leaves the top unfinished."""
    shape = picture.shape[:2]
    face(picture, apex, left, corner, built, lit, seed, courses)
    face(picture, apex, corner, right, built, shade, seed + 10, courses, band=0.035, streak=0.035)
    tl, tc, tr = _p(left, apex, built), _p(corner, apex, built), _p(right, apex, built)
    line = Sheet(shape)
    line.line([tc, corner], edge, 1.1, 0.75)                                            # the near edge catches the light
    line.line([_p(left, apex, 0.0), tl], "#fff6da", 0.9, 0.35)
    if built < 0.999:
        line.poly([tl, tc, tr, (tc[0], tc[1] - 1.4)], top_color, 0.95)                  # the flat top where the work is
    line.onto(picture)
    if haze is not None:                                                                # air: the base is paler than the top
        x, y = grid(shape)
        whole = mask_poly(shape, [tl, tc, tr, right, corner, left])
        bottom, upper = max(left[1], corner[1], right[1]), min(tl[1], tr[1])
        t = np.clip((y - upper) / max(bottom - upper, 1), 0, 1)
        over(picture, haze, (whole * t ** 1.6 * haze_amount).astype(F32))
    return picture


def works(sheet, apex, left, corner, right, built, seed, wood="#5a4030", block="#fff0c8", folk="#6b3f2a"):
    """The work going on at the top of an unfinished pyramid: blocks waiting, a hoist, and a few people."""
    rng = np.random.default_rng(seed)
    tl, tc, tr = _p(left, apex, built), _p(corner, apex, built), _p(right, apex, built)
    for k in range(6):
        t = 0.1 + 0.8 * rng.random()
        bx, by = lerp(tl[0], tr[0], t), lerp(tl[1], tr[1], t) + abs(t - 0.45) * 0 - 1.0
        by = min(by, tc[1] - 0.5)
        wd = 2.2 + rng.random() * 1.6
        sheet.poly([(bx - wd, by), (bx + wd, by), (bx + wd, by - 3), (bx - wd, by - 3)], block if k % 3 else "#c8b08c")
        sheet.line([(bx + wd, by), (bx + wd, by - 3)], "#9a94b4", 0.8, 0.9)
    hx, hy = tc[0] - 5, tc[1] - 1
    sheet.line([(hx - 6, hy), (hx, hy - 15)], wood, 1.0)                                # two poles lashed at the top, and a rope
    sheet.line([(hx + 7, hy), (hx, hy - 15)], wood, 1.0)
    sheet.line([(hx, hy - 15), (hx + 1, hy - 5)], "#3a2a20", 0.7, 0.9)
    for k in range(4):                                                                  # people are two dabs: brown, and a white kilt
        px = lerp(tl[0], tr[0], 0.15 + 0.7 * rng.random())
        py = lerp(tl[1], tr[1], 0.5) - 1.5
        sheet.line([(px, py - 4.5), (px, py - 2)], folk, 1.2)
        sheet.line([(px, py - 2), (px, py)], "#fff8ea", 1.3)
    return sheet


def wrap_ramp(sheet, apex, left, corner, right, seed, turns=((0.04, 0.40), (0.40, 0.74)), top="#e6c88e", side="#8f6f58", folk="#6b3f2a"):
    """A builders' ramp of mud brick and rubble that climbs round the pyramid: up the sunlit face, then on
    up the shaded one. People and a sledge are on it."""
    rng = np.random.default_rng(seed)
    faces = ((left, corner), (corner, right))
    for (b0, b1), (f0, f1), dark in zip(faces, turns, (False, True)):
        pts = [_on(b0, b1, apex, s, lerp(f0, f1, s)) for s in np.linspace(0.02, 0.98, 14)]
        sheet.line([(px, py + 2.6) for px, py in pts], "#5d4a52" if dark else side, 3.4, 0.92)       # its side, in shadow
        sheet.line(pts, "#a8929c" if dark else top, 2.0, 0.96)                                        # its top, trodden pale
        for k in range(5 if not dark else 2):
            i = rng.integers(1, len(pts) - 1)
            px, py = pts[i]
            sheet.line([(px, py - 4.2), (px, py - 2.0)], folk, 1.1)
            sheet.line([(px, py - 2.0), (px, py - 0.4)], "#fff8ea" if not dark else "#c8c4dc", 1.2)
    px, py = _on(left, corner, apex, 0.55, lerp(turns[0][0], turns[0][1], 0.55))
    sheet.poly([(px - 4, py - 1), (px + 3, py - 1), (px + 3, py - 4.5), (px - 4, py - 4.5)], "#fff4d4")   # a block on its sledge
    sheet.line([(px + 3, py - 1), (px + 3, py - 4.5)], "#a09ab8", 0.8)
    sheet.line([(px + 3, py - 2.5), (px + 12, py - 5.5)], "#4a3626", 0.6, 0.9)                             # the rope, and the team on it
    return sheet


def block(sheet, x, y, w, h, d, light="#fff0c6", front="#e2c592", side="#a99aa6", joint="#7d6258", lean=0.0):
    """A squared block of stone standing on the ground at (x, y) (its near left corner). The top is in the
    sun, the front half-lit, the right side in shade."""
    dx, dy = d * 0.8, -d * 0.42                                                          # the way the depth runs off, up and to the right
    a, b = (x, y), (x + w, y + w * lean)
    c, e = (x + w, y + w * lean - h), (x, y - h)
    sheet.poly([a, b, c, e], front)
    sheet.poly([b, (b[0] + dx, b[1] + dy), (c[0] + dx, c[1] + dy), c], side)
    sheet.poly([e, c, (c[0] + dx, c[1] + dy), (e[0] + dx, e[1] + dy)], light)
    sheet.line([e, c], "#fffbe8", 0.9, 0.8)
    sheet.line([c, b], joint, 0.8, 0.5)
    sheet.line([a, b], joint, 1.0, 0.55)
    return sheet


def hut(sheet, x, y, w, h, d, seed, wall="#d9b78a", shade="#9a8088", roof="#ecd3a2", door="#4a3838"):
    """A small flat-roofed house of mud brick, with its foot at (x, y)."""
    rng = np.random.default_rng(seed)
    dx, dy = d * 0.8, -d * 0.4
    sheet.poly([(x, y), (x + w, y), (x + w, y - h), (x, y - h)], wall)
    sheet.poly([(x + w, y), (x + w + dx, y + dy), (x + w + dx, y - h + dy), (x + w, y - h)], shade)
    sheet.poly([(x, y - h), (x + w, y - h), (x + w + dx, y - h + dy), (x + dx, y - h + dy)], roof)
    if w > 7:
        px = x + w * (0.3 + 0.4 * rng.random())
        sheet.poly([(px, y), (px + w * 0.16, y), (px + w * 0.16, y - h * 0.6), (px, y - h * 0.6)], door)
    return sheet


def boat(sheet, x, y, length, seed, hull=("#3a2a22", "#7a5636", "#b98d58"), cargo="#fff2cc", sail=None, folk="#6b3f2a", flip=1):
    """A river boat of the Old Kingdom, seen from the side with its waterline at y: a long hull that curls up
    at both ends, a two-legged mast, rowers, and a block of white stone amidships."""
    rng = np.random.default_rng(seed)
    L = length
    k = flip

    def at(u, v):
        return (x + k * u * L, y - v * L)
    keel = [at(-0.50, 0.11), at(-0.42, 0.03), at(-0.25, -0.012), at(0.0, -0.02), at(0.25, -0.012), at(0.42, 0.03), at(0.50, 0.13)]
    deck = [at(0.50, 0.13), at(0.40, 0.06), at(0.2, 0.045), at(0.0, 0.04), at(-0.2, 0.045), at(-0.40, 0.055), at(-0.50, 0.11)]
    sheet.poly(keel + deck, hull[0])
    sheet.line(deck, hull[2], max(0.9, L * 0.012), 0.95)
    sheet.line([at(-0.40, 0.02), at(0.0, 0.0), at(0.40, 0.02)], hull[1], max(0.9, L * 0.014), 0.9)
    sheet.poly([at(-0.10, 0.045), at(0.08, 0.045), at(0.08, 0.125), at(-0.10, 0.125)], cargo)                 # the block
    sheet.poly([at(0.08, 0.045), at(0.11, 0.055), at(0.11, 0.135), at(0.08, 0.125)], "#b0a4b4")
    mast_foot, mast_top = at(0.17, 0.045), at(0.20, 0.42)
    sheet.line([mast_foot, mast_top], hull[1], max(0.9, L * 0.012))
    sheet.line([at(0.24, 0.045), mast_top], hull[1], max(0.9, L * 0.010))
    if sail:
        sheet.poly([at(0.10, 0.40), at(0.31, 0.41), at(0.30, 0.16), at(0.11, 0.15)], sail)
        sheet.line([at(0.10, 0.40), at(0.31, 0.41)], hull[0], 0.8)
        sheet.line([at(0.11, 0.15), at(0.30, 0.16)], hull[0], 0.8)
    else:
        sheet.line([at(0.06, 0.36), at(0.33, 0.39)], "#f2e6c8", max(1.4, L * 0.02))                              # the sail furled on its yard
    sheet.line([mast_top, at(0.48, 0.13)], hull[0], 0.6, 0.8)
    sheet.line([mast_top, at(-0.47, 0.11)], hull[0], 0.6, 0.8)
    for i in range(6):                                                                                             # rowers, and the steersman aft
        u = -0.36 + i * 0.045
        px, py = at(u, 0.05)
        sheet.line([(px, py), (px, py - L * 0.045)], folk, max(1.1, L * 0.014))
        sheet.line([(px, py - L * 0.015), (px - k * L * 0.03, py + L * 0.055)], hull[2], 0.7, 0.9)                 # an oar
    px, py = at(0.42, 0.075)
    sheet.line([(px, py), (px, py - L * 0.06)], folk, max(1.1, L * 0.014))
    sheet.line([(px, py - L * 0.02), at(0.52, -0.03)], hull[2], 0.8, 0.9)                                          # the steering oar
    return sheet

"""The Forum's ground in depth (rome_forum.py; round twenty-three: tools/paint/DEPTH.md, "Middle"): the shade that
falls into the picture from where we stand, the paving's tone from far to near, and the small things that lie on it at
a true size for their distance.

Everything is on the ground as rome_forum_model measures it (x across, D from the lens, cm), so it lies in the
picture through the scene's own camera and runs to its vanishing points.

  the porch's shade   The door's porch we stand in (rome_forum_near.py) is behind and above us: a gabled front from its
                      left end (PORCH x0) to our right. The sun is behind our left shoulder, 27 degrees up (model.SUN),
                      so its shadow lies on the paving below the landing, to the right: its left edge runs from under
                      the landing's end toward the shadows' vanishing point (686, 235), as the statues' and Castor's
                      do; its far edge is the gable's slant, from row 457 at its corner up to the right. The Gaul's
                      places, the boy's arriving place and Phyllis's are all in the sun beyond it.
  the laurel's shade  The laurel by the door's left post (the bough in the picture's top left corner, and more of it out
                      of the picture) reaches out past the porch: its shade hangs on the left edge of the porch's in
                      clumps of leaves, each leaf's own small shadow laid through the camera, solid in the middle of a
                      clump and single leaves at its edge; flecks of sun let through, in the clumps and a little way
                      into the porch's shade.
  the paving's tone   paler and nearer the horizon's light far up the square, deeper and more golden toward us.
  what lies on it     by the spring a wet patch that gives back the sky, and a pierced drain stone; stone chips and
                      sawdust along the foot of the hoarding and out of its gateway, a few board offcuts at its foot;
                      straw by the moneychanger's table; a few laurel leaves blown down under the door: laid by
                      depth.scatter at a true number to the square metre (many and small far off, few and large near)."""

import math

import numpy as np

from rome_forum_kit import *
import depth

PORCH = dict(x0=-140.0, D=420.0, eaves=535.0, pitch=0.30, half=560.0)     # what throws the porch's shade: its left end (with the eaves' overhang), its front, the
                                                         # eaves' height at that corner, the gable's pitch, half its breadth (the gable's top is over our right)
CASTX, CASTD = CAST                                      # where a shadow falls on the ground, for each cm of height: across, away (model.CAST)


def porch_edge_x(D):
    """The x of the left edge of the porch's shade on the paving, at a distance D: the shadow of its upright corner,
    which runs to the shadows' vanishing point."""
    p = PORCH
    return p["x0"] + (D - p["D"]) * (CASTX / CASTD)


def porch_far():
    """How far from the lens the eaves' corner throws its shadow on the paving."""
    p = PORCH
    return p["D"] + p["eaves"] * CASTD


def eaves_far(u):
    """The far edge of the porch's shade across it (D): its gable's raking edge, from the eaves' corner up to the
    gable's top (which is over our right, out of the picture) and down again. A slant, not a level line: it shows that
    a gabled porch stands behind us."""
    p = PORCH
    c0 = p["x0"] + p["eaves"] * CASTX                                     # where the eaves' corner's shadow is, across
    run = 1.0 + CASTX * p["pitch"]                                        # across, for each cm along the gable
    top = c0 + p["half"] * run
    return porch_far() + (CASTD * p["pitch"] / run) * np.clip(p["half"] * run - np.abs(u - top), 0, None)


def in_porch_shade(u, v):
    """The porch's own shade on a level place (u across, v away, cm): 0 to 1, its edges a little soft."""
    return step(-6.0, 6.0, u - porch_edge_x(v)) * step(8.0, -8.0, v - eaves_far(u))


def porch_shade(x, h, D):
    """How much of the sun the porch takes from a place in the world at a height h (numbers or pictures): for the
    things that stand in its shade (the statue base at the front, the foot of the hoarding's near boards)."""
    x, h, D = [np.asarray(q, dtype=F32) for q in (x, h, D)]
    return in_porch_shade(x + CASTX * h, D + CASTD * h).astype(F32)


# The laurel by the door's left post: the bough in the picture's top left corner (rome_forum_near.SHOOTS_LEFT: some
# 1.5 m to our left, 3.6 m out, 4.4 to 4.9 m up, so its shade falls at x 110 to 205, D 1170 to 1260) and the rest of it,
# out of the picture. Clumps of its shade lie along the left edge of the porch's (the middle of each on the ground, how
# far it reaches across and away, in cm), built of the leaves' own small shadows.
CLUMPS = [(70.0, 1160.0, 100.0, 95.0), (136.0, 1286.0, 82.0, 70.0), (26.0, 1066.0, 70.0, 50.0), (-42.0, 1130.0, 40.0, 34.0), (196.0, 1372.0, 46.0, 30.0)]
# Sun let through the leaves, inside the shade: roundish flecks (each a small picture of the sun): where, and how big.
FLECKS = [(150.0, 1175.0, 12.0), (184.0, 1230.0, 9.0), (118.0, 1118.0, 8.0), (216.0, 1264.0, 13.0), (238.0, 1316.0, 9.0), (92.0, 1088.0, 7.0), (264.0, 1198.0, 7.0),
          (160.0, 1302.0, 8.0), (64.0, 1152.0, 9.5), (300.0, 1350.0, 10.0), (38.0, 1100.0, 7.0), (198.0, 1122.0, 6.0), (20.0, 1186.0, 8.0), (102.0, 1240.0, 7.0)]


def laurel_cast(seed=361):
    """The laurel's shade on the paving, as a mask of the picture (0 to 1): every leaf's shadow laid on the ground
    through the camera."""
    rng = np.random.default_rng(seed)
    s = Sheet2(SHAPE)
    for (cx, cD, rx, rD) in CLUMPS:
        n = int(math.pi * rx * rD / 30.0 * 2.3)
        for _ in range(n):
            a_, r_ = rng.uniform(0, 2 * math.pi), math.sqrt(rng.random()) * 1.12
            if rng.random() > min(1.0, 1.9 * (1.0 - min(r_, 1.0) ** 2) ** 0.75 + (0.10 if r_ < 1.12 else 0.0)):
                continue
            X, Z = cx + math.cos(a_) * rx * r_, cD + math.sin(a_) * rD * r_
            th = rng.uniform(0, math.pi)
            la, lb = rng.uniform(4.8, 6.6), rng.uniform(1.7, 2.4)                    # half a leaf's length and breadth, cm
            pts = []
            for ph in np.linspace(0, 2 * math.pi, 7)[:-1]:
                dx, dz = la * math.cos(ph), lb * math.sin(ph)
                pts.append(pt(X + dx * math.cos(th) - dz * math.sin(th), 0.0, Z + dx * math.sin(th) + dz * math.cos(th)))
            s.poly(pts, "#000000")
    return np.clip(blur(s.done()[1], 0.45), 0, 1).astype(F32)


def near_shade(u, v, seed=361):
    """The shade that falls into the picture from where we stand, on the paving (0 to 1): the porch's, with its clean
    edges (the left one runs to the shadows' vanishing point; the far one is its gable's slant); the laurel's, hung
    on its left edge; flecks of sun in both."""
    shade = np.maximum(in_porch_shade(u, v), laurel_cast(seed))
    hole = np.zeros(u.shape, dtype=F32)
    wob = (tex(u, v, 9.0, seed + 5, 2) - 0.5) * 0.35
    for (cx, cD, r) in FLECKS:
        d = np.hypot((u - cx) / r, (v - cD) / r) + wob
        hole = np.maximum(hole, step(1.05, 0.78, d))
    return np.clip(shade * (1 - 0.94 * hole), 0, 1).astype(F32)


def deepen(own, row, u, v):
    """The paving's own colour by distance: paler and nearer the horizon's light far up the square, deeper and more
    golden toward us (the nearest slabs are the Sacred Way's, older and browner)."""
    near = np.clip((row - HZ) / (H - HZ), 0, 1)
    far_ = (1 - near) ** 2.2
    c = lerp(own, col("#f6eedc")[None, None, :], (0.34 * far_)[..., None])
    c = c * (1 - (near ** 1.5)[..., None] * (1 - np.array([0.86, 0.79, 0.64], dtype=F32)))
    return np.clip(c, 0, 1).astype(F32)


# ---------------------------------------------------------------- what lies on the paving
def ground_pt(X, Z):
    return pt(X, 0.0, Z)


def ground_k(X, Z):
    return k(Z)


def wet(pic, info, seed=371):
    """By Juturna's spring: water slopped over the basin's rim lies on the paving in front of it. Wet stone is darker
    and richer; where the water stands it gives back the sky, with a thin bright edge; damp follows the joints away."""
    u, v = info["u"], info["v"]
    spots = [(-492.0, 1090.0, 60.0, 27.0, 1.0), (-408.0, 1064.0, 26.0, 13.0, 1.0)]
    damp = np.zeros(SHAPE, F32)
    pool = np.zeros(SHAPE, F32)
    wob = (tex(u, v, 40.0, seed, 3) - 0.5) * 0.9
    for (cx, cD, rx, rD, a) in spots:
        d = np.sqrt(((u - cx) / rx) ** 2 + ((v - cD) / rD) ** 2) + wob
        damp = np.maximum(damp, step(1.9, 1.0, d) * a)
        pool = np.maximum(pool, step(0.86, 0.66, d) * a)
    seep = info["joints"] * step(280.0, 60.0, np.hypot(u + 470.0, (v - 1070.0) * 1.6)) * 0.9          # it follows the joints away
    damp = np.clip(np.maximum(damp, seep), 0, 1) * info["ground"]
    pool = pool * info["ground"]
    tint(pic, "#a8845e", (damp * 0.62).astype(F32))                                                  # wet travertine: deeper, more golden
    sky_ = lerp(col("#5f8fc8")[None, None, :], col("#a8c8e4")[None, None, :], np.clip((v - 1010.0) / 120.0, 0, 1)[..., None])
    over(pic, sky_, (pool * 0.78).astype(F32))
    rim = np.clip(blur(pool, 0.8) * (1 - pool) * 3.2, 0, 1)
    glow(pic, "#fffbe8", (rim * 0.42).astype(F32))
    glint = step(0.80, 0.90, tex(u, v * 2.4, 13.0, seed + 3, 2)) * pool                               # the sun on it, here and there
    glow(pic, "#ffffff", (glint * 0.7).astype(F32))
    return pool


def drain(sheet, seed=373):
    """A drain in the paving near the basin's corner: a round stone, worn, pierced with a ring of holes: the square's
    rain and the spring's overflow go down it to the great sewer under the Forum."""
    cx, cD, r = -338.0, 1090.0, 23.0
    ring = [ground_pt(cx + r * math.cos(a), cD + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 20, endpoint=False)]
    sheet.poly(ring, "#c9b99c", 0.8)
    sheet.line(ring[10:] + ring[:1], "#8a7462", 1.0, 0.7)                                             # the near edge of its seat, in shade
    sheet.line(ring[:11], "#fff2d2", 0.9, 0.55)
    kk = k(cD)
    for a in np.linspace(0, 2 * math.pi, 6, endpoint=False):
        q = ground_pt(cx + r * 0.52 * math.cos(a), cD + r * 0.52 * math.sin(a))
        sheet.ellipse(q[0], q[1], max(1.1, 3.6 * kk), max(0.7, 1.6 * kk), "#3e3440", 0.92)
    q = ground_pt(cx, cD)
    sheet.ellipse(q[0], q[1], max(1.1, 3.6 * kk), max(0.7, 1.6 * kk), "#3e3440", 0.92)


def chips(sheet, pic, info, seed=375):
    """Stone chips, sawdust and a few offcuts along the foot of the hoarding and out of its gateway: the site's own
    litter, thick at the boards and thinning onto the square. (Between the boards and the walk's edge, and beyond.)"""
    rng = np.random.default_rng(seed)
    (ax, aD), (bx, bD) = HOARD["a"], HOARD["b"]
    L = math.hypot(ax - bx, aD - bD)
    tx, tD = (ax - bx) / L, (aD - bD) / L                                 # along the hoarding, from its far end to its near
    nx, nD = -tD, tx                                                      # out of the site, into the square? (checked below)
    if nx > 0:
        nx, nD = -nx, -nD                                                 # (the square is to the left of the boards)
    g0, g1 = HOARD["gate"]

    def keep(X, Z):
        s_ = (X - bx) * tx + (Z - bD) * tD                                # along
        d_ = (X - bx) * nx + (Z - bD) * nD                                # out from the boards
        if d_ < 2.0 or s_ < -40.0 or s_ > L + 200.0:
            return False
        gate = abs(s_ / L - (1 - (g0 + g1) / 2)) < 0.11                   # opposite the gateway the litter is tracked farther out
        reach = 240.0 if gate else 85.0
        return rng.random() < math.exp(-d_ / reach) * (1.0 if gate else 0.8)
    # a dusting of sawdust first: a pale stain along the foot
    u, v = info["u"], info["v"]
    s_ = (u - bx) * tx + (v - bD) * tD
    d_ = (u - bx) * nx + (v - bD) * nD
    gate = np.exp(-(((s_ / L) - (1 - (g0 + g1) / 2)) / 0.09) ** 2)
    dust = np.exp(-np.clip(d_, 0, None) / (60.0 + 150.0 * gate)) * (d_ > 0) * (s_ > -40) * (s_ < L + 200) * (0.45 + 0.75 * tex(u, v, 90.0, seed, 3))
    over(pic, "#f1e2bc", np.clip(dust * 0.34 * info["ground"] * (1 - 0.6 * info["cut"]), 0, 1).astype(F32))
    places = depth.scatter(ground_pt, ground_k, (300.0, 1200.0, 1200.0, 3200.0), 9.0, seed, size=(7.0, 4.0), keep=keep, most=900)
    for (x, y, kk, r) in places:
        w = max(0.7, (3.0 + 6.0 * r) * kk)
        tone = ["#fbf3e0", "#e6d8ba", "#c9b592", "#a08a70", "#d9b780"][int(r * 4.999)]
        sheet.ellipse(x + w * 0.7, y + 0.35, w * 1.1, max(0.5, w * 0.32), "#8f7e9a", 0.45)     # its shadow, away and to the right
        sheet.poly([(x - w, y), (x - w * 0.2, y - w * (0.35 + 0.5 * r)), (x + w, y - w * 0.15), (x + w * 0.5, y + w * 0.2)], tone)
    # three offcuts of board lying along the foot of the boards (between them and the walk's edge)
    for (X, Z, ln, ang) in ((598.0, 2300.0, 64.0, 1.36), (584.0, 2392.0, 48.0, 1.22), (672.0, 1800.0, 56.0, 1.30)):
        a = ground_pt(X - math.cos(ang) * ln / 2, Z - math.sin(ang) * ln / 2)
        b = ground_pt(X + math.cos(ang) * ln / 2, Z + math.sin(ang) * ln / 2)
        sheet.line([(a[0] + 1.0, a[1] + 0.8), (b[0] + 1.0, b[1] + 0.8)], "#8f7e9a", max(1.2, 9 * k(Z)), 0.5)
        sheet.line([a, b], "#b98e5e", max(1.2, 9 * k(Z)))
        sheet.line([(a[0], a[1] - 0.5), (b[0], b[1] - 0.5)], "#e2bc86", max(0.7, 3 * k(Z)), 0.8)


def straw(sheet, seed=377):
    """Straw the coin sacks came packed in, round the far side of the moneychanger's table, and a little blown along
    the paving."""
    rng = np.random.default_rng(seed)
    t = TABLE
    places = depth.scatter(ground_pt, ground_k, (t["x"] - 190.0, t["x"] + 230.0, t["D"] - 40.0, t["D"] + 260.0), 26.0, seed, size=(14.0, 2.0),
                           keep=lambda X, Z: rng.random() < math.exp(-(((X - t["x"] - 30.0) / 150.0) ** 2 + ((Z - t["D"] - 120.0) / 110.0) ** 2)), most=260)
    for (x, y, kk, r) in places:
        ang = rng.uniform(-0.5, 0.5) + (0.0 if r < 0.7 else 1.2)
        ln = (9.0 + 12.0 * r) * kk
        sheet.line([(x - math.cos(ang) * ln / 2, y - math.sin(ang) * ln * 0.18), (x + math.cos(ang) * ln / 2, y + math.sin(ang) * ln * 0.18)],
                   ["#f0d68a", "#d9b860", "#b8964a"][int(r * 2.999)], max(1.0, 1.6 * kk), 0.95)


def fallen(sheet, seed=379):
    """A few laurel leaves blown down off the door's bough, on the paving below the landing."""
    rng = np.random.default_rng(seed)
    places = depth.scatter(ground_pt, ground_k, (-60.0, 520.0, 1010.0, 1330.0), 0.55, seed, size=(10.0, 3.0), most=40)
    for (x, y, kk, r) in places:
        ang = rng.uniform(0, math.pi)
        ln = 10.0 * kk * (0.8 + 0.4 * r)
        ca_, sa_ = math.cos(ang), math.sin(ang) * 0.32
        tone = ["#2c4630", "#3f6238", "#5d7e3e", "#8fa652"][int(r * 3.999)]
        pts = [(x + ca_ * ln * (t - 0.5), y + sa_ * ln * (t - 0.5) - w * ln * 0.10) for t, w in ((0, 0), (0.25, 0.8), (0.5, 1.0), (0.78, 0.62), (1, 0), (0.78, -0.62), (0.5, -1.0), (0.25, -0.8))]
        sheet.ellipse(x + 1.2, y + 0.6, ln * 0.5, ln * 0.12, "#8f7e9a", 0.4)
        sheet.poly(pts, tone)

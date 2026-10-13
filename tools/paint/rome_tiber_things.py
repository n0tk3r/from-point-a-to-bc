"""What stands about across the Tiber (rome_tiber.py paints the place): every made thing drawn through the scene's own
camera in its own measurements (rome_tiber_model.py), face by face, each face lit by the morning sun as it faces it.

  cut-outs (each -> (color, coverage) at picture size):
    barge_plane()          the barge moored off the quay, bow upstream toward us, piled with bales, jars and linen,
                           its towing mast, its steering oar trailing from the stern; the plank to it from the landing
    curb_plane()           the edge stones along the landing's far side and its river side, a bollard: they stand in
                           front of the barge, so that the barge can ride the water behind them
    landing_front_plane()  the landing's near edge stones, a bollard and its rope (the cut-out landing-edge)
    fence_plane()          the hen yard's wattle fence, as two cut-outs: the near run of its front (fence), and the
                           rest of the front with the corner post and the side (fence-corner)
    well_plane()           the well's stone curb, its bucket
    washing_plane()        the washing on the line between Eleazar's two upper windows
  into the backdrop:
    bench(), coop(), dish(), fig_tree(), landing_stack(), landing_steps(), yard_ground(), lane_things()

No statue, picture or carving of any living thing on any of them; no lettering."""

import math

import numpy as np

from brush import F32, blur, curve, grid, lerp, mask_poly, noise, over, rgb, step, tint
from rome_steps_kit import Frame, col, hash2, lathe, mix
from rome_street_kit import Sheet2, wn
import rome_tiber_model as M
from rome_tiber_kit import (LIGHT, SHAPE, FACE_FRONT, FACE_UP, Q, facing, fpoly, fpt, frame_of, from_frame, sun_in, W, H)

WF = Frame.at(M.CAM, 0.0, 0.0, M.Z0)                         # a frame lined up with the world: u = x, v = z, h = y
FE = frame_of(M.FRONT0, M.D)                                 # the near houses' frame: u = s along their front, v back into them


def shade(local, normal, cut=0.0, deep=0.0, bounce=0.5):
    """A flat face's color: its own color, lit as it faces the sun (normal in the world: x, y, z)."""
    n = np.asarray(normal, dtype=float)
    n = n / (np.linalg.norm(n) + 1e-9)
    return LIGHT.on(col(local) if isinstance(local, str) else np.asarray(local, dtype=F32), facing(*n), cut, up=float(n[1]), deep=deep, bounce=bounce)


def fe_normal(nu, nv, nh):
    """A direction in the near houses' frame (along, back, up) -> the world."""
    x = nu * FE["d"][0] - nv * FE["out"][0]
    z = nu * FE["d"][1] - nv * FE["out"][1]
    return (x, nh, z)


class Pen:
    """A clear sheet drawn on in the world's own measurements (cm), with faces lit by the sun."""

    def __init__(self):
        self.s = Sheet2(SHAPE)

    def poly(self, pts3, color, a=1.0):
        self.s.poly(Q(pts3), color, a)
        return self

    def face(self, pts3, local, normal, cut=0.0, deep=0.0, bounce=0.35, a=1.0):
        self.s.poly(Q(pts3), shade(local, normal, cut, deep, bounce), a)
        return self

    def line(self, pts3, color, w=1.0, a=1.0):
        self.s.line(Q(pts3), color, w, a)
        return self

    def fpoly(self, pts, color, a=1.0):
        """A shape given in the near houses' frame (u, v, h)."""
        self.s.poly(fpoly(FE, pts), color, a)
        return self

    def fline(self, pts, color, w=1.0, a=1.0):
        self.s.line(fpoly(FE, pts), color, w, a)
        return self

    def done(self):
        return self.s.done()


def k_at(z):
    return M.F / (M.Z0 + z)


# ================================================================ the barge
B = M.BARGE
XC = (B["xs"] + B["xp"]) / 2.0                               # its keel line
HALF = (B["xs"] - B["xp"]) / 2.0


def hull_at(t):
    """Along the barge from its bow (t = 0, toward us) to its stern (t = 1): -> (half beam, gunwale height)."""
    bow = max(0.0, 0.16 - t) / 0.16
    stern = max(0.0, t - 0.86) / 0.14
    half = HALF * (1 - 0.62 * bow ** 1.6 - 0.40 * stern ** 2)
    gun = B["gunwale"] + 40.0 * bow ** 2 + 24.0 * stern ** 2
    return half, gun


def z_of(t):
    return B["z0"] + t * (B["z1"] - B["z0"])


def barge_plane(seed=101):
    """The barge as the camera sees it: its starboard side and bow toward us (both turned from the sun, dark), the
    planking and a pale rub-rail, the far gunwale, the deck, the cargo (tall jars in straw forward, bales of papyrus
    rolled in mats amidships, bolts of linen aft under a hide), the towing mast, the steering oar. -> (color, coverage)"""
    rng = np.random.default_rng(seed)
    p = Pen()
    ts = np.linspace(0.0, 1.0, 41)
    stations = [(z_of(t),) + hull_at(t) for t in ts]
    W_ = M.WATER
    # ---- the far gunwale's inner side and the hold's floor, seen over the near side
    deck = []
    for z, half, gun in stations:
        deck.append((XC - half + 6, B["deck"], z))
    for z, half, gun in reversed(stations):
        deck.append((XC + half - 6, B["deck"], z))
    p.face(deck, "#7a5a40", (0, 1, 0), deep=0.25)
    for i in range(len(stations) - 1):                        # the far side's inside: the planks of the port side, lit on the inside
        (za, ha, ga), (zb, hb, gb) = stations[i], stations[i + 1]
        p.face([(XC - ha, ga, za), (XC - hb, gb, zb), (XC - hb + 6, B["deck"], zb), (XC - ha + 6, B["deck"], za)], "#8a6444", (1, 0.2, 0), deep=0.1)
    for z, half, gun in stations[::2]:                       # the ribs inside
        p.line([(XC - half + 4, gun - 2, z), (XC - half + 7, B["deck"] + 2, z)], "#4e3828", 0.8, 0.8)
    # ---- the cargo
    # tall jars standing in straw, forward
    straw = [(XC - HALF * 0.55, B["deck"] + 22, z_of(0.12)), (XC + HALF * 0.55, B["deck"] + 22, z_of(0.12)), (XC + HALF * 0.75, B["deck"] + 22, z_of(0.24)), (XC - HALF * 0.75, B["deck"] + 22, z_of(0.24))]
    p.face(straw, "#c8a65c", (0, 1, 0), bounce=0.2)
    jars = Pen()
    # bales amidships: rolls of papyrus wrapped in mats and corded, lying across the barge, two tiers
    bales = []
    for tier in (0, 1):
        for j in range(9):
            t = 0.27 + j * 0.052 + tier * 0.026
            if tier == 1 and j > 7:
                continue
            for side in (-1, 1):
                bales.append((t, side, tier))
    bales.sort(key=lambda b: (-z_of(b[0]), b[2]))            # far ones first, then the lower tier under the upper
    for t, side, tier in bales:
        z = z_of(t)
        r = 30.0
        y0 = B["deck"] + r + tier * (2 * r - 6)
        x0 = XC + side * HALF * 0.42 - 55
        x1 = x0 + 110
        tone = mix("#c4a060", "#a8844c", rng.random())
        # the body of the roll (its top in the sun, its front face toward us darker) and the end toward the quay (shade)
        p.face([(x0, y0 + r, z - r * 0.15), (x1, y0 + r, z - r * 0.15), (x1, y0 + r * 0.3, z - r * 0.95), (x0, y0 + r * 0.3, z - r * 0.95)], tone, (0, 0.85, -0.5))
        p.face([(x0, y0 + r * 0.3, z - r * 0.95), (x1, y0 + r * 0.3, z - r * 0.95), (x1, y0 - r * 0.7, z - r * 0.8), (x0, y0 - r * 0.7, z - r * 0.8)], tone, (0, -0.2, -1.0), deep=0.15)
        end = [(x1, y0 + r * math.cos(a), z + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 14, endpoint=False)]
        p.face(end, mix(tone, "#7a5a34", 0.3), (1, 0, 0), deep=0.1)
        p.line([(x1, y0, z), (x1, y0 + r * 0.6, z - r * 0.5)], "#5a4028", 0.7, 0.7)          # the rolled end
        for c in (0.3, 0.7):                                                               # its cords
            xc = lerp(x0, x1, c)
            p.line([(xc, y0 + r, z - r * 0.15), (xc, y0 + r * 0.3, z - r * 0.95), (xc, y0 - r * 0.7, z - r * 0.8)], "#4a3420", 1.0, 0.85)
    # bolts of linen aft, stacked and half under a hide thrown over them
    for j in range(6):
        t = 0.72 + j * 0.032
        z = z_of(t)
        for tier in (0, 1):
            if tier == 1 and j % 2:
                continue
            y0 = B["deck"] + tier * 34
            x0, x1 = XC - HALF * 0.7, XC + HALF * 0.66
            tone = mix("#efe6d0", "#e2d6bc", rng.random())
            p.face([(x0, y0 + 34, z), (x1, y0 + 34, z), (x1, y0 + 34, z + 42), (x0, y0 + 34, z + 42)], tone, (0, 1, 0))
            p.face([(x0, y0, z), (x1, y0, z), (x1, y0 + 34, z), (x0, y0 + 34, z)], tone, (0, 0, -1), deep=0.1)
            p.face([(x1, y0, z), (x1, y0, z + 42), (x1, y0 + 34, z + 42), (x1, y0 + 34, z)], tone, (1, 0, 0), deep=0.1)
            p.line([(x0, y0 + 17, z), (x1, y0 + 17, z)], "#b8aa90", 0.6, 0.6)
    # an ox hide thrown over the stack, hanging down its front and its side toward the quay in folds
    ha, hb, zf_, zb_ = XC - HALF * 0.74, XC + HALF * 0.69, z_of(0.72) - 3, z_of(0.88) + 44
    top = B["deck"] + 71
    p.face([(ha, top, zf_), (hb, top, zf_), (hb + 4, top + 1, zb_), (ha - 4, top + 1, zb_)], "#8e6c4c", (0, 1, 0), bounce=0.3)
    hem = lambda f: B["deck"] + 40 + 7 * math.sin(f * 9.0 + 0.6) + 4 * math.sin(f * 23.0)
    fs = np.linspace(0.0, 1.0, 17)
    p.face([(lerp(ha, hb, f), top, zf_) for f in fs] + [(lerp(ha, hb, f), hem(f), zf_ - 1) for f in fs[::-1]], "#8e6c4c", (0, 0, -1), deep=0.05, bounce=0.6)
    for f in fs[1:-1:2]:                                      # its folds
        p.line([(lerp(ha, hb, f), top - 2, zf_ - 1.5), (lerp(ha, hb, f) + 3, hem(f) + 3, zf_ - 1.5)], "#4e3a2c", 0.8, 0.55)
    gs = np.linspace(0.0, 1.0, 9)
    p.face([(hb + 1, top, lerp(zf_, zb_, g)) for g in gs] + [(hb + 2, B["deck"] + 30 + 8 * math.sin(g * 7.0), lerp(zf_, zb_, g)) for g in gs[::-1]],
           "#8e6c4c", (1, 0, 0), deep=0.1, bounce=0.6)
    p.line([(ha, top, zf_), (hb, top, zf_)], "#c49a70", 1.0, 0.8)        # the light along its top edge
    # ---- the jars: tall amphorae standing in two rows in the straw, forward of the bales
    for row, t in ((0, 0.215), (1, 0.165)):
        for j in range(3):
            x = XC + (-0.5 + 0.45 * j + 0.22 * row) * HALF
            z = z_of(t)
            hj = 96.0 + rng.uniform(-6, 6)
            jars_one(p, x, z, B["deck"] + 22 - 0.24 * hj, hj, lean=rng.uniform(-0.04, 0.04), sunk=0.24)
    # ---- the towing mast, a little forward of amidships, and the rope from its head
    mz, mt = z_of(0.33), 310.0                                 # a short mast: the towing rope runs from its head
    p.face([(XC - 8, B["deck"], mz - 8), (XC + 8, B["deck"], mz - 8), (XC + 6, mt, mz - 6), (XC - 6, mt, mz - 6)], "#6a4e38", (0, 0, -1), deep=0.1)
    p.face([(XC + 8, B["deck"], mz - 8), (XC + 8, B["deck"], mz + 8), (XC + 6, mt, mz + 6), (XC + 6, mt, mz - 6)], "#6a4e38", (1, 0, 0), deep=0.1)
    p.line([(XC - 7, B["deck"], mz - 8), (XC - 5, mt, mz - 6)], "#d8b080", 0.8, 0.7)         # the sun along its far edge
    p.line([(XC, mt - 5, mz), (XC + 20, mt * 0.62, mz - 300), (XC + 90, 60, z_of(0.02))], "#4a3a2c", 0.9, 0.85)   # its rope, down to the bow
    p.poly([(XC - 10, mt - 16, mz - 10), (XC + 10, mt - 16, mz - 10), (XC + 10, mt + 4, mz - 10), (XC - 10, mt + 4, mz - 10)], "#4a3626")
    # ---- the near side: dark tarred planks in strakes, a pale rub-rail along the gunwale, the bow toward us
    for i in range(len(stations) - 1):
        (za, ha, ga), (zb, hb, gb) = stations[i], stations[i + 1]
        dz, dx = zb - za, hb - ha
        n = (dz, 0.0, -dx)                                                                  # the side's normal (toward +x, and toward us where it tapers)
        p.face([(XC + ha, W_ - 2, za), (XC + hb, W_ - 2, zb), (XC + hb, gb, zb), (XC + ha, ga, za)], "#4a3a32", n, deep=0.05, bounce=0.55)
    for frac, tone, w in ((0.30, "#2e2428", 0.8), (0.55, "#2e2428", 0.8), (0.78, "#3a2c2c", 0.7)):      # the strakes' seams
        p.line([(XC + h_, W_ + (g_ - W_) * frac, z) for z, h_, g_ in stations], tone, w, 0.8)
    p.line([(XC + h_, g_ - 6, z) for z, h_, g_ in stations], "#a07850", 2.0, 0.95)                 # the rub-rail
    p.line([(XC + h_, g_ - 7.5, z) for z, h_, g_ in stations], "#d8b07a", 0.8, 0.7)
    p.line([(XC + h_, g_, z) for z, h_, g_ in stations], "#c49a6a", 1.0, 0.9)                       # the gunwale's top edge, lit
    z0, h0, g0 = stations[0]                                                                         # the bow's face, toward us
    p.face([(XC - h0, W_ - 2, z0), (XC + h0, W_ - 2, z0), (XC + h0, g0, z0), (XC - h0, g0, z0)], "#3e3230", (0, 0, -1), deep=0.1, bounce=0.6)
    p.face([(XC - 9, g0, z0 - 4), (XC + 9, g0, z0 - 4), (XC + 7, g0 + 46, z0 - 22), (XC - 7, g0 + 46, z0 - 22)], "#5a4434", (0, 0.3, -1), deep=0.05)   # the stem post
    p.line([(XC - 8, g0 + 2, z0 - 4), (XC - 6, g0 + 44, z0 - 22)], "#c49a6a", 0.8, 0.8)
    for z, half, gun in stations[2:-2:5]:                                                            # fenders of old rope hung over the side
        p.face([(XC + half + 3, gun - 10, z - 14), (XC + half + 3, gun - 10, z + 14), (XC + half + 5, gun - 36, z + 12), (XC + half + 5, gun - 36, z - 12)], "#8a7458", (1, 0, -0.2), bounce=0.5)
    # ---- the steering oar on the stern quarter, trailing into the water
    zs = z_of(0.97)
    loom, pivot, blade = (XC + HALF * 0.55, 150.0, z_of(0.84)), (XC + HALF * 0.62, 30.0, zs), (XC + HALF * 0.7, W_ + 2, zs + 260.0)
    p.line([loom, pivot, blade], "#5a4434", 2.2, 1.0)
    p.line([(loom[0], loom[1] + 2, loom[2]), (pivot[0], pivot[1] + 2, pivot[2])], "#c8a070", 0.7, 0.7)
    # ---- the plank from the landing to the bow
    L = M.LANDING
    pk0, pk1 = (-560.0, 2.0, L["z1"] - 6.0), (XC + h0 * 0.55, g0 + 4, z0 + 36.0)
    p.face([(pk0[0] - 16, pk0[1], pk0[2]), (pk0[0] + 16, pk0[1], pk0[2]), (pk1[0] + 16, pk1[1], pk1[2]), (pk1[0] - 16, pk1[1], pk1[2])], "#a8845c", (0, 1, 0))
    p.face([(pk0[0] + 16, pk0[1], pk0[2]), (pk1[0] + 16, pk1[1], pk1[2]), (pk1[0] + 16, pk1[1] - 5, pk1[2]), (pk0[0] + 16, pk0[1] - 5, pk0[2])], "#6a5038", (1, 0, -0.3), deep=0.1)
    c, a = p.done()
    jc, ja = jars.done()
    return c, a


def jars_one(p, x, z, y0, hgt, lean=0.0, sunk=0.0):
    """A tall amphora standing (in the straw): a long body swelling to its shoulder, a neck, two handles; lit from the
    left, its right side and its front in shade. `sunk`: how much of it, from its toe up, the straw hides."""
    k = k_at(z)
    bx, by = M.P(x, y0, z)
    tx, ty = M.P(x + lean * hgt, y0 + hgt, z)
    hp = hgt * k
    w = 17.0 * k
    lx = lambda f: lerp(bx, tx, f)
    prof = [(0.0, 0.18), (0.12, 0.55), (0.40, 0.92), (0.62, 1.0), (0.74, 0.86), (0.80, 0.40), (0.86, 0.26), (0.97, 0.24), (1.0, 0.30)]
    if sunk > 0:
        r_at = float(np.interp(sunk, [f for f, _ in prof], [r_ for _, r_ in prof]))
        prof = [(sunk, r_at)] + [(f, r_) for f, r_ in prof if f > sunk]
    left = [(lx(f) - w * r, by - hp * f) for f, r in prof]
    right = [(lx(f) + w * r, by - hp * f) for f, r in reversed(prof)]
    p.s.poly(left + right, shade("#a8644a", (0.2, 0, -1), deep=0.05, bounce=0.6))
    body = [(f, r) for f, r in prof if 0.0 < f <= 0.80]
    lit = [(lx(f) - w * r, by - hp * f) for f, r in body] + [(lx(f) - w * r * 0.35, by - hp * f) for f, r in reversed(body)]
    p.s.poly(lit, shade("#c47a54", (-1, 0.2, -0.2)))
    p.s.line([(lx(0.42) - w * 0.62, by - hp * 0.42), (lx(0.64) - w * 0.7, by - hp * 0.64)], "#e8a87a", max(0.7, 2.0 * k), 0.7)
    for sd in (-1, 1):                                        # the handles, from the neck to the shoulder
        p.s.line([(lx(0.92) + sd * w * 0.24, by - hp * 0.92), (lx(0.90) + sd * w * 0.58, by - hp * 0.90), (lx(0.76) + sd * w * 0.62, by - hp * 0.76)],
                 "#7a4434", max(0.8, 2.6 * k), 0.95)
    p.s.ellipse(tx, ty, w * 0.30, max(0.6, w * 0.10), "#4a2c24")
    if sunk > 0:                                              # the straw tucked round it where it goes in
        f0, r0 = prof[0]
        sx_, sy_ = lx(f0), by - hp * f0
        p.s.ellipse(sx_, sy_ + 0.5, w * r0 * 1.25, max(0.8, w * 0.22), shade("#c8a65c", (0, 1, 0)), 0.95)
        for j in range(5):
            a_ = -0.9 + 0.45 * j
            p.s.line([(sx_ + w * r0 * 1.1 * math.sin(a_), sy_ + 0.5), (sx_ + w * r0 * 1.5 * math.sin(a_), sy_ - w * 0.35 * math.cos(a_))], "#e0c47c", max(0.6, 0.9 * k), 0.8)


# ================================================================ the landing
def curb_plane(seed=111):
    """The edge stones along the landing's far side (toward the barge) and along its river side: travertine blocks
    standing CURB proud of the paving, worn round on top, an iron ring in one; a squat bollard at the far corner.
    -> (color, coverage)"""
    rng = np.random.default_rng(seed)
    p = Pen()
    L = M.LANDING
    hgt = M.CURB
    zf = L["z1"]
    # along the river side first (it is farther left), then the far side
    x = L["x0"]
    zz = L["z0"]
    while zz < zf - 1:
        zb = min(zf, zz + rng.uniform(70, 110))
        tone = mix("#d8ccb2", "#c8b898", rng.random())
        p.face([(x, hgt, zz), (x + 34, hgt, zz), (x + 34, hgt, zb), (x, hgt, zb)], tone, (0, 1, 0))
        p.face([(x + 34, 0, zz), (x + 34, 0, zb), (x + 34, hgt, zb), (x + 34, hgt, zz)], tone, (1, 0, 0), deep=0.05)
        p.line([(x + 34, hgt, zz), (x + 34, 0, zz)], "#7a6c60", 0.6, 0.7)
        zz = zb
    xx = L["x0"]
    while xx < L["x1"] - 1:
        xb = min(L["x1"] + 10, xx + rng.uniform(80, 120))
        tone = mix("#d8ccb2", "#c8b898", rng.random())
        p.face([(xx, hgt, zf - 34), (xb, hgt, zf - 34), (xb, hgt, zf), (xx, hgt, zf)], tone, (0, 1, 0))
        p.face([(xx, 0, zf - 34), (xb, 0, zf - 34), (xb, hgt, zf - 34), (xx, hgt, zf - 34)], tone, (0, 0, -1), deep=0.05, bounce=0.9)
        p.line([(xb, hgt, zf - 34), (xb, 0, zf - 34)], "#7a6c60", 0.6, 0.7)
        xx = xb
    # an iron ring set in the curb, by the plank
    rx, rz = -520.0, zf - 34
    pts = [(rx + 9 * math.cos(a), hgt * 0.5 + 9 * math.sin(a) * 0.9, rz - 1) for a in np.linspace(0, 2 * math.pi, 16)]
    p.line(pts, "#3a3030", 1.0, 0.95)
    # a squat bollard at the far corner by the river, its rope to the barge's bow
    bx, bz = L["x0"] + 30, zf - 30
    bollard(p, bx, bz, 52.0, 19.0)
    p.line([(bx, 40, bz), (bx - 60, 20, bz + 120), (XC + 20, B["gunwale"] + 20, B["z0"] + 6)], "#5a4a3a", 1.1, 0.95)
    return p.done()


def bollard(p, x, z, hgt, r, tone="#cfc2a6"):
    """A squat stone mooring post: a round shaft, a rounded head, worn bright where the ropes run."""
    k = k_at(z)
    bx, by = M.P(x, 0, z)
    tx, ty = M.P(x, hgt, z)
    w = r * k
    p.s.poly([(bx - w, by), (tx - w * 0.9, ty + w * 0.2), (tx + w * 0.9, ty + w * 0.2), (bx + w, by)], shade(tone, (0.3, 0, -1), deep=0.05, bounce=0.5))
    p.s.poly([(bx - w, by), (tx - w * 0.9, ty + w * 0.2), (tx - w * 0.2, ty + w * 0.2), (bx - w * 0.3, by)], shade(tone, (-1, 0.1, -0.3)))
    p.s.ellipse(tx, ty + w * 0.15, w * 1.0, w * 0.55, shade(tone, (-0.3, 1, -0.3)))
    p.s.ellipse(tx - w * 0.3, ty + w * 0.05, w * 0.45, w * 0.22, shade(mix(tone, "#ffffff", 0.2), (-0.5, 1, -0.3)))
    p.s.line([(bx - w * 0.95, (by + ty) / 2 + w * 0.5), (bx + w * 0.95, (by + ty) / 2 + w * 0.8)], "#8a7a64", max(0.7, w * 0.25), 0.6)


def landing_front_plane(seed=121):
    """The landing's near edge, in front of everybody: its edge stones each side of the steps down into the water and a
    bollard with a coil of rope. -> (color, coverage)"""
    rng = np.random.default_rng(seed)
    p = Pen()
    L, S = M.LANDING, M.STEPS
    hgt = M.CURB
    z0 = L["z0"]
    for (xa, xb) in ((L["x0"], S["x0"]), (S["x1"], L["x1"] + 6)):
        xx = xa
        while xx < xb - 1:
            x2 = min(xb, xx + rng.uniform(70, 105))
            tone = mix("#d4c8ae", "#c4b494", rng.random())
            p.face([(xx, hgt, z0), (x2, hgt, z0), (x2, hgt, z0 + 32), (xx, hgt, z0 + 32)], tone, (0, 1, 0))
            p.face([(xx, -2, z0), (x2, -2, z0), (x2, hgt, z0), (xx, hgt, z0)], tone, (0, 0, -1), deep=0.05, bounce=1.0)
            p.line([(x2, hgt, z0), (x2, -2, z0)], "#6e6056", 0.7, 0.7)
            xx = x2
    bx, bz = S["x1"] + 34, z0 + 18
    bollard(p, bx, bz, 58.0, 21.0, "#d2c4a8")
    k = k_at(bz)
    cx, cy = M.P(bx + 46, 0, bz + 10)
    for i in range(4):                                        # a coil of rope on the edge stone
        p.s.ellipse(cx, cy - 2 * k - i * 2.2 * k, (24 - i * 3) * k, (9 - i) * k, mix("#8a7050", "#6a5440", i / 4), 0.95)
        p.s.ellipse(cx - 3 * k, cy - 3 * k - i * 2.2 * k, (16 - i * 3) * k, (5 - i * 0.6) * k, "#5a4634", 0.9)
    return p.done()


def landing_steps(pic, hide=None, seed=131):
    """Into the backdrop: the steps that go down from the landing's near edge into the river, toward us: travertine
    worn round at the nosings, the lower ones wet and dark, weed on their risers, the lowest awash with the sky in the
    film of water on it; the stair's side toward the quay in shade. `hide`: where the quay's own paving is seen, which
    stands in front of them (the quay's edge cuts across the stair's near end)."""
    rng = np.random.default_rng(seed)
    p = Pen()
    L, S = M.LANDING, M.STEPS
    z0 = L["z0"]
    W_ = M.WATER
    p.face([(L["x0"], W_ - 4, z0), (L["x1"], W_ - 4, z0), (L["x1"], 0, z0), (L["x0"], 0, z0)], "#a89478", (0, 0, -1), deep=0.05, bounce=1.0)
    prof = [(S["x1"], 0.0, z0)]
    for n in range(S["n"]):                                   # each step: the riser over it (toward us, in shade), its tread (lit)
        y = -(n + 1) * S["rise"]
        zt = z0 - (n + 1) * S["tread"]
        if y < W_ - 4:
            break
        wet = float(np.clip((n - 0.5) / 2.5, 0, 1))           # dry at the top, wet down at the water
        tone = mix(mix("#d6c6a2", "#c4b28c", n / S["n"]), "#7a7458", wet * 0.7)
        riser = mix(mix(tone, "#9c8668", 0.25), "#56603e", wet * 0.55)
        zr = zt + S["tread"]
        p.face([(S["x0"], y, zr), (S["x1"], y, zr), (S["x1"], y + S["rise"], zr), (S["x0"], y + S["rise"], zr)], riser, (0, 0, -1), deep=0.0, bounce=1.0)
        p.face([(S["x0"], y, zt), (S["x1"], y, zt), (S["x1"], y, zr), (S["x0"], y, zr)], tone, (0, 1, 0))
        # the shadow of the step above on it: the low sun comes from ahead and the left, so the riser above shades the
        # back of the tread, all but a corner toward the river where the light slips past (the landing itself, over the top one)
        reach = min(S["tread"], S["rise"] * M.SUN[2] / M.SUN[1])
        slide = 0.0 if n == 0 else -M.SUN[0] / M.SUN[2]
        p.face([(S["x0"], y, zr), (S["x1"], y, zr), (S["x1"], y, zr - reach), (min(S["x1"], S["x0"] + slide * reach), y, zr - reach)], tone, (0, 1, 0), cut=1.0)
        for j in ((0.31, 0.69) if n % 2 else (0.14, 0.5, 0.86)):                     # the joints between its blocks, staggered
            xj = S["x0"] + (S["x1"] - S["x0"]) * (j + rng.normal(0, 0.03))
            p.line([(xj, y, zt + 1), (xj, y, zr - 1)], "#5a5044", 0.7, 0.5)
            p.line([(xj, y + 1, zr), (xj, y + S["rise"] - 1, zr)], "#3e3832", 0.7, 0.45)
        p.line([(S["x0"], y + S["rise"] - 0.5, zr), (S["x1"], y + S["rise"] - 0.5, zr)], "#4a4238", 0.7, 0.35)    # the shadow under the nosing above
        p.line([(S["x0"], y, zt), (S["x1"], y, zt)], mix("#f2e6ca", "#d4dcd8", wet), 0.8, 0.65)                    # its nosing, worn round, catching the light
        if wet > 0.95:                                        # awash: the sky in the film of water over it
            p.line([(S["x0"] + 12, y + 0.3, zt + 9), (S["x1"] - 26, y + 0.3, zt + 13)], "#c4d2dc", 1.3, 0.55)
            p.line([(S["x0"] + 30, y + 0.3, zt + 20), (S["x1"] - 50, y + 0.3, zt + 22)], "#a8bccc", 0.9, 0.45)
        prof += [(S["x1"], y + S["rise"], zr), (S["x1"], y, zr), (S["x1"], y, zt)]
    prof += [(S["x1"], W_ - 4, prof[-1][2]), (S["x1"], W_ - 4, z0)]
    p.face(prof, "#a89878", (1, 0, 0), deep=0.1, bounce=0.8)  # the stair's side toward the quay (seen only where the quay leaves it)
    c, a = p.done()
    if hide is not None:
        a = (a * (1 - hide)).astype(F32)
    over(pic, c, a)
    return a


def landing_stack(pic, seed=141):
    """Into the backdrop: what is waiting on the landing to go aboard, against its river side (nobody walks behind it):
    bales of papyrus in their mats, two bolts of linen, two tall jars in a rack."""
    rng = np.random.default_rng(seed)
    p = Pen()
    L = M.LANDING
    x0 = L["x0"] + 6
    for j, (z, tier) in enumerate(((470.0, 0), (535.0, 0), (502.0, 1))):
        r = 30.0
        y0 = r + tier * (2 * r - 8)
        xa, xb = x0, x0 + 96
        tone = mix("#c8a464", "#a8844c", rng.random())
        p.face([(xa, y0 + r, z - r * 0.15), (xb, y0 + r, z - r * 0.15), (xb, y0 + r * 0.3, z - r * 0.95), (xa, y0 + r * 0.3, z - r * 0.95)], tone, (0, 0.85, -0.5))
        p.face([(xa, y0 + r * 0.3, z - r * 0.95), (xb, y0 + r * 0.3, z - r * 0.95), (xb, y0 - r * 0.8, z - r * 0.75), (xa, y0 - r * 0.8, z - r * 0.75)], tone, (0, -0.2, -1), deep=0.15, bounce=0.5)
        end = [(xb, y0 + r * math.cos(a), z + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 14, endpoint=False)]
        p.face(end, mix(tone, "#7a5a34", 0.3), (1, 0, 0), deep=0.1, bounce=0.5)
        p.line([(xb, y0, z), (xb, y0 + r * 0.6, z - r * 0.5)], "#5a4028", 0.8, 0.7)
        for c in (0.28, 0.72):
            xc = lerp(xa, xb, c)
            p.line([(xc, y0 + r, z - r * 0.15), (xc, y0 + r * 0.3, z - r * 0.95), (xc, y0 - r * 0.8, z - r * 0.75)], "#4a3420", 1.0, 0.85)
    for j, z in enumerate((410.0,)):                          # a bolt of linen
        y0 = 0.0
        xa, xb = x0 + 6, x0 + 96
        tone = mix("#f0e8d4", "#e4d8c0", rng.random())
        p.face([(xa, y0 + 30, z), (xb, y0 + 30, z), (xb, y0 + 30, z + 40), (xa, y0 + 30, z + 40)], tone, (0, 1, 0))
        p.face([(xa, y0, z), (xb, y0, z), (xb, y0 + 30, z), (xa, y0 + 30, z)], tone, (0, 0, -1), deep=0.1, bounce=0.5)
        p.face([(xb, y0, z), (xb, y0, z + 40), (xb, y0 + 30, z + 40), (xb, y0 + 30, z)], tone, (1, 0, 0), deep=0.1, bounce=0.5)
        p.line([(xa, 15, z), (xb, 15, z)], "#b4a68c", 0.7, 0.6)
    for j, z in enumerate((598.0,)):
        for i in range(2):
            jars_one(p, x0 + 26 + i * 40, z - i * 6, 0.0, 92.0, lean=0.03 * (i - 0.5))
    c, a = p.done()
    over(pic, c, a)
    return pic


# ================================================================ the hen yard, the bench, the well
YD = M.YARD


def fence_plane(seed=151):
    """The hen yard's wattle fence: stakes driven in every half metre, withies woven between them, grey with weather;
    along the yard's front (toward the square, lit at a slant like the house front) and its side by the door (we see
    its inner face, in shade). Two cut-outs, so that each can lie at one depth (a row: see rome_tiber_layout.py): the
    near run of its front, from the picture's edge to the stake at YARD["split"]; and the corner, the rest of the front
    with the corner post and the side. -> {"fence": (color, coverage), "fence-corner": (color, coverage)}"""
    rng = np.random.default_rng(seed)
    p, pn = Pen(), Pen()                                      # p: the corner (and the side); pn: the near run
    hgt = YD["fence"]
    # the side, by the door (farther), first: its inner face toward us, in shade, woven the same way as the front
    us, vside = YD["s1"], -YD["out"]
    srng = np.random.default_rng(seed + 1)
    at = lambda t, o, h: (us - o, vside + t, h)              # t cm along the side from the front corner, o cm toward us
    sn = fe_normal(-1, 0, 0)
    p.fpoly([at(0, -2, 0), at(-vside, -2, 0), at(-vside, -2, hgt), at(0, -2, hgt)], shade("#3e3630", sn, deep=0.3, bounce=0.5))
    stk = list(np.arange(0.0, -vside + 1, 47.0))
    stones = ("#a08e74", "#86745e", "#6e5e4a", "#ae9c82")
    srows = np.arange(3.0, hgt - 1.0, 4.6)
    for j, hh in enumerate(srows):
        for i in range(len(stk) - 1):
            a, b = stk[i], stk[i + 1]
            fr = (i + j) % 2 == 0
            tone = stones[(i + j) % 4] if srng.random() < 0.8 else stones[srng.integers(4)]
            pts = [(a, 1.0 if fr else -0.5, hh), ((a + b) / 2, 2.5 if fr else -1.5, hh - 0.9), (b, -0.5 if fr else 1.0, hh + srng.normal(0, 0.4))]
            p.fline([at(*q) for q in pts], shade(tone, fe_normal(-1, 0, 0.25), bounce=0.5), 1.9, 0.97)
            p.fline([at(t, o + 0.4, h + 1.0) for t, o, h in pts], shade(mix(tone, "#fff2d6", 0.25), fe_normal(-0.3, 0, 1), bounce=0.5), 0.6, 0.5)
    for i, t in enumerate(stk[1:], 1):                        # its stakes (the corner post is the front's)
        p.fline([at(t, 2, -2), at(t, 2, hgt + srng.uniform(5, 12))], shade("#5e4e40", sn, bounce=0.6), 3.0, 1.0)
        for j, hh in enumerate(srows):
            if (i + j) % 2 == 1 and i < len(stk) - 1:
                p.fline([at(t - 6, 2.6, hh), at(t + 6, 2.6, hh)], shade(stones[(i + j) % 4], fe_normal(-1, 0, 0.25), bounce=0.5), 1.9, 0.97)
    # the front, toward the square: stakes every 45 cm, withies woven between them, in front of one stake and behind the
    # next, row by row the other way about, each sagging a little between the stakes
    vf = -YD["out"]
    u0, u1, us_ = YD["s0"], YD["s1"], YD["split"]
    pen = lambda u: pn if u <= us_ + 0.5 else p               # which cut-out a thing at u along the front belongs to
    dark = shade("#4e4236", fe_normal(0, -1, 0), deep=0.3)    # the dark between the withies
    pn.fpoly([(u0, vf + 2, 0), (us_, vf + 2, 0), (us_, vf + 2, hgt), (u0, vf + 2, hgt)], dark)
    p.fpoly([(us_, vf + 2, 0), (u1, vf + 2, 0), (u1, vf + 2, hgt), (us_, vf + 2, hgt)], dark)
    stakes = list(np.arange(u1, u0 - 1, -45.0))
    assert any(abs(u - us_) < 0.5 for u in stakes)
    tones = ("#b8a07c", "#9a8262", "#7e684e", "#c4ae88")
    rows = np.arange(3.0, hgt - 1.0, 4.6)

    def withy(a, b, hh, j, i, front):
        mid = (a + b) / 2
        bulge = -2.5 if front else 1.5
        tone = tones[(i + j) % 4] if rng.random() < 0.8 else tones[rng.integers(4)]
        pts = [(a, vf - 1.0 + (0 if front else 1.5), hh), (mid, vf + bulge, hh - 0.9), (b, vf - 1.0 + (1.5 if front else 0), hh + rng.normal(0, 0.4))]
        q = pen(mid)
        q.fline(pts, shade(tone, fe_normal(0, -1, 0.25)), 1.9, 0.97)
        q.fline([(x, v - 0.4, h + 1.0) for x, v, h in pts], shade(mix(tone, "#fff2d6", 0.35), fe_normal(-0.2, -0.6, 1)), 0.6, 0.6)
    for j, hh in enumerate(rows):
        for i in range(len(stakes) - 1):
            withy(stakes[i], stakes[i + 1], hh + rng.normal(0, 0.5), j, i, (i + j) % 2 == 0)
    for i, u in enumerate(stakes):                            # the stakes, a little above the weave, cut rough
        t = rng.uniform(5, 12)
        q = pen(u)
        q.fline([(u, vf - 2, -2), (u, vf - 2, hgt + t)], shade("#6a5644", fe_normal(0, -1, 0), bounce=0.6), 3.0, 1.0)
        q.fline([(u + 1.4, vf - 3, 0), (u + 1.4, vf - 3, hgt + t)], shade("#b09474", fe_normal(-0.6, -1, 0)), 0.8, 0.7)
        for j, hh in enumerate(rows):                         # the withies that pass in front of this stake
            if (i + j) % 2 == 1 and 0 < i < len(stakes) - 1:
                q.fline([(u - 6, vf - 2.6, hh), (u + 6, vf - 2.6, hh)], shade(tones[(i + j) % 4], fe_normal(0, -1, 0.25)), 1.9, 0.97)
    p.fline([(u1, vf - 2, -2), (u1, vf - 2, hgt + 10)], shade("#6a5644", fe_normal(0, -1, 0), bounce=0.6), 3.4, 1.0)     # the corner post
    return {"fence": pn.done(), "fence-corner": p.done()}


def bench(pic, seed=161):
    """Into the backdrop: the stone bench before the house of prayer, a slab on two blocks, its back to the wall."""
    p = Pen()
    b = M.BENCH
    v0, v1 = -b["out"] - b["deep"] / 2, -b["out"] + b["deep"] / 2
    for (a, c) in ((b["s0"] + 12, b["s0"] + 48), (b["s1"] - 48, b["s1"] - 12)):
        p.fpoly([(a, v0 + 4, 0), (c, v0 + 4, 0), (c, v0 + 4, b["h"] - 7), (a, v0 + 4, b["h"] - 7)], shade("#cbbd9e", fe_normal(0, -1, 0), bounce=0.4))
        p.fpoly([(a, v0 + 4, 0), (a, v1, 0), (a, v1, b["h"] - 7), (a, v0 + 4, b["h"] - 7)], shade("#cbbd9e", fe_normal(-1, 0, 0), deep=0.1, bounce=0.5))
    p.fpoly([(b["s0"], v0, b["h"] - 7), (b["s1"], v0, b["h"] - 7), (b["s1"], v0, b["h"]), (b["s0"], v0, b["h"])], shade("#ddd1b6", fe_normal(0, -1, 0)))
    p.fpoly([(b["s0"], v0, b["h"]), (b["s1"], v0, b["h"]), (b["s1"], v1, b["h"]), (b["s0"], v1, b["h"])], shade("#e6dcc4", (0, 1, 0)))
    p.fpoly([(b["s0"], v0, b["h"] - 7), (b["s0"], v1, b["h"] - 7), (b["s0"], v1, b["h"]), (b["s0"], v0, b["h"])], shade("#d0c4a8", fe_normal(-1, 0, 0), deep=0.1, bounce=0.5))
    p.fline([(b["s0"] + 2, v0, b["h"]), (b["s1"] - 2, v0, b["h"])], "#f8f0dc", 0.8, 0.6)
    c, a = p.done()
    over(pic, c, a)
    return pic


def coop(pic, seed=171):
    """Into the backdrop: the hens' coop against the house front in the near corner of the yard: a low box of weathered
    boards on two stones, a lid sloping down to the front, a small door with a board for a ramp."""
    p = Pen()
    u0, u1, v0, v1, hb, hf = -10.0, 140.0, -74.0, 0.0, 74.0, 58.0
    boards = "#8e8070"
    p.fpoly([(u0, v0, 8), (u1, v0, 8), (u1, v0, hf), (u0, v0, hf)], shade(boards, fe_normal(0, -1, 0)))
    for hh in np.arange(20.0, hf, 12.5):
        p.fline([(u0, v0 - 0.5, hh), (u1, v0 - 0.5, hh)], "#5a5048", 0.7, 0.75)
    for uu in (u0 + 8, u1 - 8):                               # the two stones it stands on
        p.fpoly([(uu - 10, v0 + 2, 0), (uu + 10, v0 + 2, 0), (uu + 10, v0 + 2, 8), (uu - 10, v0 + 2, 8)], shade("#b4a690", fe_normal(0, -1, 0)))
    p.fpoly([(u1, v0, 8), (u1, v1, 8), (u1, v1, hb), (u1, v0, hf)], shade(boards, fe_normal(1, 0, 0), deep=0.1))
    p.fpoly([(u0 - 5, v0 - 7, hf), (u1 + 5, v0 - 7, hf), (u1 + 5, v1, hb + 3), (u0 - 5, v1, hb + 3)], shade("#7c7064", fe_normal(0, -0.7, 1)))
    p.fline([(u0 - 5, v0 - 7, hf), (u1 + 5, v0 - 7, hf)], "#c4b49a", 0.9, 0.8)
    du0, du1 = u0 + 52, u0 + 76
    p.fpoly([(du0, v0 - 0.6, 12), (du1, v0 - 0.6, 12), (du1, v0 - 0.6, 40), (du0, v0 - 0.6, 40)], "#2e2428")
    p.fpoly([(du0 + 2, v0 - 1, 10), (du1 - 2, v0 - 1, 10), (du1 - 2, v0 - 38, 0), (du0 + 2, v0 - 38, 0)], shade("#9a8466", (0, 0.8, -0.5)))
    c, a = p.done()
    over(pic, c, a)
    return pic


def dish(pic, seed=181):
    """Into the backdrop: a shallow clay dish of water on the ground in the yard; it holds the sky."""
    x, z = M.out(M.along(330.0), 160.0)
    k = k_at(z)
    cx, cy = M.P(x, 6, z)
    p = Pen()
    p.s.ellipse(cx, cy + 3 * k, 24 * k, 9 * k, shade("#a85c3c", (0, 0, -1), bounce=0.5))
    p.s.ellipse(cx, cy, 24 * k, 8.5 * k, shade("#c87450", (0, 1, 0)))
    p.s.ellipse(cx + 1 * k, cy + 0.6 * k, 19 * k, 6.4 * k, "#8aa6c8")
    p.s.ellipse(cx - 4 * k, cy - 0.4 * k, 9 * k, 2.4 * k, "#c8dcec", 0.8)
    c, a = p.done()
    over(pic, c, a)
    return pic


def well_plane(seed=191):
    """The well in the square: a round curb of travertine, worn smooth, its rim thicker, a wooden bucket standing on it
    with its rope. -> (color, coverage)"""
    wl = M.WELL
    x, z, r, hgt = wl["x"], wl["z"], wl["r"], wl["h"]

    def paint(h, around):
        c = np.empty(h.shape + (3,), dtype=F32)
        c[...] = col("#d8ccb4")
        c *= (0.92 + 0.12 * hash2(np.floor(around * 9), np.floor(h / 30), seed)[..., None])
        rim = step(hgt - 12, hgt - 9, h)
        c = lerp(c, col("#e6dcc6"), rim[..., None] * 0.8)
        c = c * (1 - 0.18 * np.clip(1 - h / 20.0, 0, 1)[..., None])
        return c
    prof = [(0.0, r + 2), (6.0, r), (hgt - 12, r - 1), (hgt - 11, r + 3), (hgt, r + 3)]
    color, cov = lathe(WF, LIGHT, x, z, prof, paint, deep=0.0, bounce=0.6, wrap=0.25)
    p = Pen()
    k = k_at(z)
    tx, ty = M.P(x, hgt, z)
    p.s.ellipse(tx, ty, (r + 3) * k, (r + 3) * k * 0.20, shade("#efe6d2", (0, 1, 0)))
    p.s.ellipse(tx, ty + 0.6, (r - 6) * k, (r - 6) * k * 0.19, "#3a3036")          # the dark of the shaft
    p.s.ellipse(tx + 4 * k, ty + 1.2, (r - 14) * k, (r - 14) * k * 0.12, "#2a2228")
    bx, by = M.P(x + r * 0.55, hgt, z - r * 0.35)                                   # a bucket on the rim, its rope over the edge
    bw, bh = 14 * k, 24 * k
    p.s.poly([(bx - bw, by), (bx - bw * 0.82, by - bh), (bx + bw * 0.82, by - bh), (bx + bw, by)], shade("#8a6844", (0, 0, -1), bounce=0.5))
    p.s.poly([(bx - bw, by), (bx - bw * 0.82, by - bh), (bx - bw * 0.2, by - bh), (bx - bw * 0.3, by)], shade("#a07c50", (-1, 0, -0.3)))
    p.s.ellipse(bx, by - bh, bw * 0.82, bw * 0.25, "#4a3a30")
    for f in (0.3, 0.75):
        p.s.line([(bx - bw * (1 - f * 0.18), by - bh * f), (bx + bw * (1 - f * 0.18), by - bh * f)], "#4a3a2a", max(0.7, 2 * k), 0.8)
    p.s.line([(bx - bw * 0.8, by - bh), (bx, by - bh - 10 * k), (bx + bw * 0.8, by - bh)], "#5a4a3a", 0.7, 0.9)
    p.s.line([(bx, by - bh - 10 * k), (bx - 18 * k, ty - 2), (tx - 6 * k, ty + 2)], "#6a5844", 0.8, 0.9)
    c2, a2 = p.done()
    c = color * cov[..., None]
    out_c = c * (1 - a2[..., None]) + c2 * a2[..., None]
    out_a = np.clip(cov + a2 - cov * a2, 0, 1)
    return np.where(out_a[..., None] > 1e-3, out_c / np.maximum(out_a[..., None], 1e-3), 0).astype(F32), out_a.astype(F32)


def washing_plane(seed=201):
    """The washing on the line between Eleazar's two upper windows: a small tunic of undyed wool and a faded blue cloth,
    hung on the line pegged out from the wall. -> (color, coverage). (The line itself is in the backdrop.)"""
    p = Pen()
    out_ = M.WASH["out"]
    items = [(M.WASH["s0"] + 10, M.WASH["s0"] + 52, 58.0, "#efe4cc", True), (M.WASH["s0"] + 62, M.WASH["s1"] - 8, 46.0, "#7c98bc", False)]
    for (a, b, drop, tone, tunic) in items:
        ya, yb = line_h(a), line_h(b)
        pts = [(a, -out_, ya), (b, -out_, yb), (b, -out_ + 3, yb - drop * (0.9 if tunic else 1.0)), ((a + b) / 2, -out_ + 4, (ya + yb) / 2 - drop * 1.03), (a, -out_ + 3, ya - drop)]
        if tunic:                                             # a small tunic: its sleeves out at the top
            pts = [(a - 6, -out_, ya - 2), (a, -out_, ya), (b, -out_, yb), (b + 6, -out_, yb - 2), (b + 5, -out_ + 1, yb - 14), (b - 1, -out_ + 2, yb - 13),
                   (b, -out_ + 3, yb - drop), ((a + b) / 2, -out_ + 4, (ya + yb) / 2 - drop * 1.04), (a, -out_ + 3, ya - drop), (a + 1, -out_ + 2, ya - 13), (a - 5, -out_ + 1, ya - 14)]
        p.fpoly(pts, shade(tone, fe_normal(0, -1, 0), bounce=0.4))
        for f in (0.33, 0.66):                                # folds: a darker crease, a lit edge
            u = lerp(a, b, f)
            p.fline([(u, -out_ + 1, line_h(u) - 4), (u + 2, -out_ + 3, line_h(u) - drop * 0.9)], mix(tone, "#6a5a6a", 0.35), 1.2, 0.7)
            p.fline([(u - 2, -out_ + 1, line_h(u) - 4), (u, -out_ + 3, line_h(u) - drop * 0.9)], mix(tone, "#ffffff", 0.25), 0.7, 0.6)
        p.fline([(a, -out_ - 0.5, ya - drop), ((a + b) / 2, -out_ + 4, (ya + yb) / 2 - drop * 1.03), (b, -out_ + 3, yb - drop)], mix(tone, "#ffffff", 0.3), 0.8, 0.7)
        for u in (a + 3, b - 3):                              # two pegs
            p.fline([(u, -out_ - 1, line_h(u) + 3), (u, -out_ - 1, line_h(u) - 6)], "#6a5040", 1.4, 1.0)
    return p.done()


def line_h(u):
    """The height of the washing line at u along the front: pegged at both windows, sagging between."""
    w = M.WASH
    t = (u - w["s0"]) / (w["s1"] - w["s0"])
    return w["h"] - 14.0 * 4 * t * (1 - t)


# ================================================================ the fig tree
def fig_limbs():
    """The fig in the yard: a short trunk forking into three smooth grey limbs, the twigs at their ends in first leaf.
    -> [(points (x, y, z) from the foot up, thickness in cm at its start and end)]"""
    fx, fz = M.out(M.along(M.FIG["s"]), M.FIG["out"])
    rng = np.random.default_rng(211)
    at = lambda dx, dy, dz: (fx + dx, dy, fz + dz)
    limbs = [([at(0, 0, 0), at(-2, 55, 3), at(-5, 105, 6)], 19.0, 13.0)]
    main = [([at(-5, 105, 6), at(-36, 168, 18), at(-82, 226, 34), at(-118, 282, 44), at(-136, 318, 50)], 9.0, 3.0),
            ([at(-5, 105, 6), at(8, 176, -6), at(24, 250, -14), at(32, 318, -10), at(30, 352, -6)], 8.5, 2.6),
            ([at(-5, 105, 6), at(38, 150, 24), at(92, 196, 38), at(140, 226, 56)], 8.0, 3.0)]
    limbs += main
    for pts, w0, w1 in main:                                  # twigs off each limb, mostly upward, a few drooping
        for j in range(1, len(pts)):
            for n in range(3):
                bx, by, bz = pts[j]
                a = rng.uniform(-2.4, -0.4) if rng.random() < 0.8 else rng.uniform(0.3, 1.2)
                L_ = rng.uniform(26, 58)
                tip = (bx + math.cos(a) * L_ * rng.uniform(0.4, 1.0) * (1 if rng.random() < 0.5 else -1), by - math.sin(a) * L_, bz + rng.uniform(-18, 18))
                mid = ((bx + tip[0]) / 2 + rng.normal(0, 4), (by + tip[1]) / 2 + rng.normal(0, 4), (bz + tip[2]) / 2)
                limbs.append(([pts[j], mid, tip], max(1.6, lerp(w0, w1, j / len(pts)) * 0.45), 1.0))
    return limbs


def fig_tree(pic, seed=221):
    """Into the backdrop: the fig tree in the yard, in first leaf: smooth grey limbs lit on the side toward the sun,
    small pale new leaves in tufts at the twigs' ends, a few small green figs."""
    rng = np.random.default_rng(seed)
    p = Pen()
    limbs = fig_limbs()
    for pts, w0, w1 in limbs:
        pp = Q(pts)
        z = pts[0][2]
        k = k_at(z)
        sm = curve(pp, 5) if len(pp) > 2 else pp
        p.s.taper(sm, shade("#8a7a66", (0.2, 0.3, -1), deep=0.0, bounce=1.1), max(1.0, w0 * k * 1.2), max(0.8, w1 * k * 1.1))
        p.s.taper([(x_ - w0 * k * 0.30, y_) for x_, y_ in sm], shade("#d2c8b4", (-1, 0.3, 0)), max(0.7, w0 * k * 0.45), max(0.5, w1 * k * 0.35), 0.95)
    tips = [pts[-1] for pts, w0, w1 in limbs[4:]] + [pts[-1] for pts, w0, w1 in limbs[1:4]]
    for (x, y, z) in tips:                                    # tufts of new leaves, small and pale, at the ends of the twigs
        k = k_at(z)
        cx, cy = M.P(x, y, z)
        for n in range(rng.integers(4, 9)):                  # each a small leaf, three-lobed, turned every way
            a = rng.uniform(0, 2 * math.pi)
            r = rng.uniform(2, 11) * k
            lx, ly = cx + math.cos(a) * r, cy + math.sin(a) * r * 0.8 - 2 * k
            sz = rng.uniform(3.0, 5.5) * k
            tone = mix("#a8bc5c", "#d8e094", rng.random()) if rng.random() < 0.65 else mix("#6e8a44", "#8aa452", rng.random())
            ang = rng.uniform(0, math.pi)
            for lobe in (-0.7, 0.0, 0.7):
                p.s.ellipse(lx + math.cos(ang + lobe) * sz * 0.6, ly + math.sin(ang + lobe) * sz * 0.6, sz * 0.55, sz * 0.42, tone, 0.95)
        if rng.random() < 0.5:                                # a small green fig
            p.s.ellipse(cx + 2 * k, cy + 4 * k, 2.2 * k, 2.6 * k, "#6e8640")
    c, a = p.done()
    over(pic, c, a)
    return a


def thing_solids():
    """What stands on the lane and throws a shadow on it, as solids: in the world's plan (x, z, up)."""
    wl = M.WELL
    L, S = M.LANDING, M.STEPS
    fx, fz = M.out(M.along(M.FIG["s"]), M.FIG["out"])
    return [("cyl", wl["x"], wl["z"], wl["r"] + 3, 0, wl["h"]),
            ("cyl", L["x0"] + 30, L["z1"] - 30, 19, 0, 52), ("cyl", S["x1"] + 34, L["z0"] + 18, 21, 0, 58),
            ("box", L["x0"], L["x1"], L["z1"] - 34, L["z1"], 0, M.CURB), ("box", L["x0"], L["x0"] + 34, L["z0"], L["z1"], 0, M.CURB),
            ("box", L["x0"] + 6, L["x0"] + 102, 440, 568, 0, 108), ("box", L["x0"] + 10, L["x0"] + 92, 568, 606, 0, 92),
            ("cyl", fx, fz, 9, 0, 105)]


def front_thing_solids():
    """...and in the near houses' frame (u, v, h): the fence, the coop, the bench."""
    b = M.BENCH
    return [("box", YD["s0"], YD["s1"], -YD["out"] - 3, -YD["out"] + 3, 0, YD["fence"]),
            ("box", YD["s1"] - 3, YD["s1"] + 3, -YD["out"], 0, 0, YD["fence"]),
            ("box", -10, 140, -74, 0, 0, 74),
            ("box", b["s0"], b["s1"], -b["out"] - b["deep"] / 2, -b["out"] + b["deep"] / 2, 0, b["h"])]

"""The near things of the Forum (rome_forum.py): the cut-outs (the temple of Castor's corner, Juturna's basin, the
Puteal, the moneychanger's table and its awning, the hoarding of the senate house's site, the three statues on their
columns, the statue base at the front) and the things painted into the backdrop round Phyllis's place (her baskets and
the pole of garlands).

Each cut-out is painted on a Canvas of its own, crisply; rome_forum.py brushes it against the backdrop and finishes it.
`solids()` gives everything that throws a shadow on the paving, for the ground's light."""

import math

import numpy as np

from rome_forum_kit import *

# ---------------------------------------------------------------- the temple of Castor's corner
C_RADIUS = 56.0


def castor_column_profile(hp, hc):
    """(height, radius) up one of Castor's columns: an Attic base, the shaft with its swelling, the foot of the capital."""
    p = [(0, 74), (14, 74), (16, 70), (24, 70), (28, 66), (36, 64), (40, 60), (46, 58)]
    for i in range(1, 15):
        t = i / 14.0
        p.append((46 + (hc - 140) * t, C_RADIUS * (1 - 0.13 * (0.25 * t + 0.75 * t * t))))
    p += [(hc - 120, 50), (hc - 100, 54), (hc, 62)]
    return [(hp + a, b) for a, b in p]


def castor_column_paint(seed, hp):
    def paint(h, around):
        b = h - hp
        a = around * 2 * math.pi * C_RADIUS
        c = np.empty(h.shape + (3,), dtype=F32)
        c[...] = col("#f3ead6")
        c *= (1 + (tex(a, b, 160, seed)[..., None] - 0.5) * 0.10 + (tex(a, b, 30, seed + 1)[..., None] - 0.5) * 0.05)
        streak = step(0.62, 0.9, tex(a * 5.0, b * 0.3, 90, seed + 2)) * np.clip((b - 120) / 300.0, 0, 1)
        c = c * (1 - 0.08 * streak[..., None])                                     # rain has run down them
        base = b <= 46
        c = np.where(base[..., None], col(TRAV) * (0.92 + 0.12 * tex(a, b, 20, seed + 3)[..., None]), c)
        lime = step(0.80, 0.9, tex(a * 9.0, b * 0.25, 110, seed + 4)) * (b > 46) * (b < 120)
        c = c * (1 - 0.15 * lime[..., None] * np.array([0.6, 0.8, 1.0], dtype=F32))     # scuffs where people lean
        return np.clip(c, 0, 1).astype(F32)
    return paint


def castor(seed=81):
    """The corner of the temple of Castor, near us on the left: its broad flight of steps coming down toward us, the
    low cheek wall that ends it on the right, the two nearest columns of its front rising out of the top of the picture,
    and the deep porch behind them with the great door. Its front faces us (turned a little to our right) and is in the
    sun. -> Canvas"""
    kf = castor_frame()
    c = CASTOR
    cv = Canvas(SHAPE)
    W_, hp, rise, tread, porch = c["width"], c["podium"], c["rise"], c["tread"], c["porch"]
    n = c["steps"]
    vf = castor_steps_foot()
    su, sv, sh = kf.to_frame(SUN)
    RISER = -sv                                   # how squarely a riser faces the sun
    SIDE = su                                     # the cheek wall's outer face (u = W_)
    cheek = 46.0
    u0, u1 = -400.0, W_ - cheek                   # the flight runs between these (its left end is far off the picture)

    def vk(i):                                    # the riser of step i (1 at the bottom) stands at v = vk(i)
        return vf + (i - 1) * tread

    # ---- the porch behind the columns: the cella's front wall with its great door, in deep shade; the ceiling far above
    wall_v = 640.0
    for Wf, m in kf.face([(u0, wall_v, hp), (W_ - 40, wall_v, hp), (W_ - 40, wall_v, hp + 1500), (u0, wall_v, hp + 1500)]):
        u, h, ppc = Wf.on_front(wall_v)
        own = plain(u, h, "#ead6b2", seed + 1, amount=0.07)
        own = np.where(((h - hp) < 140)[..., None], col(DADO) * 1.15, own)
        door = (np.abs(u - (W_ - 1020)) < 260) & (h - hp < 1150)
        frame_ = (np.abs(u - (W_ - 1020)) < 320) & (h - hp < 1210) & ~door
        own = np.where(frame_[..., None], col(MARBLE), own)
        own = np.where(door[..., None], ramp(np.clip((h - hp) / 1150.0, 0, 1), [(0.0, "#3a2a2e"), (1.0, "#1c1620")]), own)
        glowv = np.clip(1 - (h - hp) / 500.0, 0, 1)
        cv.put(LIT.on(own, 0.0, deep=0.40, bounce=1.3 * glowv + 0.5), m, Wf)
    # ---- its right flank, seen at a slant as a narrow strip beside the corner, in shade: the podium, and over it the
    # columns down the side with the cella's wall behind them
    back_v = CASTOR_BACK
    for Wf, m in kf.face([(W_, -porch, 0), (W_, back_v, 0), (W_, back_v, hp), (W_, -porch, hp)]):
        v, h, ppc = Wf.on_side(W_)
        own, _ = tufa(v, h, ppc, seed + 6, base="#d6c29c", long=118, high=58)
        own = own * (1 - 0.3 * (np.clip(1.5 - np.abs(h - 40) * ppc / 1.2, 0, 1) + np.clip(1.5 - np.abs(h - (hp - 30)) * ppc / 1.2, 0, 1))[..., None])
        cv.put(LIT.on(own, 0.0, 0.0, deep=0.12, bounce=0.5 + 0.8 * np.clip(1 - h / 200.0, 0, 1)), m, Wf)
    for Wf, m in kf.face([(W_ - 60, 0, hp), (W_ - 60, back_v, hp), (W_ - 60, back_v, hp + 1500), (W_ - 60, 0, hp + 1500)]):
        v, h, ppc = Wf.on_side(W_ - 60)
        q = (v - 0.0) / c["gap"]
        f = q - np.floor(q)
        colm = (f < 0.36) | (f > 0.96)
        own = np.where(colm[..., None], col("#efe4cc") * (0.92 + 0.12 * (f < 0.12)[..., None]), col("#a89a8c")) * np.ones(v.shape + (1,), dtype=F32)
        cv.put(LIT.on(own, 0.0, 0.0, deep=np.where(colm, 0.15, 0.55), bounce=0.6), m, Wf)
    # the porch floor's front edge as seen from below: only the crown moulding of the podium shows
    # ---- the steps: risers lit, treads seen from above while they are below our eye. (The risers face the sun almost
    # squarely; they are given the light the steps of Saturn have in the act's first picture, STEP_SUN, so that the same
    # travertine looks the same in both and does not glare yellow; the treads, which the low sun only grazes, a little
    # less. Long blocks, each its own tone; their joints fine and faint: stone, not boards.)
    STEP_SUN, TREAD_SUN = 0.44, 0.36

    def weather(u, h):
        """Stains that run across the steps regardless of their joints, as on old stone: broad soft mottling, rain-dark
        patches, and the bottom steps greyed by the dust of the square. -> a multiplier (h, w, 3)"""
        mott = (tex(u, h * 1.6, 260, seed + 70) - 0.5) * 0.12 + (tex(u, h * 2.5, 70, seed + 71) - 0.5) * 0.05
        dark = step(0.58, 0.80, tex(u * 0.8, h * 1.2, 180, seed + 72)) * 0.07
        low = np.clip(1 - h / 140.0, 0, 1) * 0.08
        m = 1 + mott - dark - low
        return np.stack([m, m * 0.995 + low * 0.10, m * 1.01 + low * 0.25], axis=-1).astype(F32)

    for i in range(n, 0, -1):
        hi = i * rise
        for Wf, m in kf.face([(u0, vk(i), hi - rise), (u1, vk(i), hi - rise), (u1, vk(i), hi), (u0, vk(i), hi)], pad=1):
            u, h, ppc = Wf.on_front(vk(i))
            tone, jm, _ = courses(u, h + i * 37.0, long=460.0, high=rise, seed=seed + 10 + i, joint=1.0, ppc=ppc, vary_len=0.5)
            own = col(TRAV)[None, None, :] * (1 + (tone[..., None] - 0.5) * 0.06) * (1 + (tex(u, h + i * 40, 140, seed + 9)[..., None] - 0.5) * 0.06)
            own = own * weather(u, h)
            own = own * (1 - 0.10 * jm[..., None])
            worn = np.exp(-((u - (W_ - 600)) / 420.0) ** 2) * 0.06                     # the middle of the flight is worn paler
            own = own * (1 + worn[..., None])
            hb = h - (hi - rise)
            own = own * (1 - 0.22 * np.clip(1 - hb / 3.0, 0, 1)[..., None])           # dirt where it meets the tread below
            chip = step(0.66, 0.74, tex(u, h * 3 + i * 50, 22, seed + 18, 3)) * np.clip((hb - rise + 2.5) / 2.5, 0, 1)
            own = own * (1 - 0.12 * chip[..., None])
            cv.put(LIT.on(own * 0.98, STEP_SUN, 0.0, bounce=0.9), m, Wf)
        if i < n and hi < EYE - 2:
            for Wf, m in kf.face([(u0, vk(i), hi), (u1, vk(i), hi), (u1, vk(i + 1), hi), (u0, vk(i + 1), hi)], pad=1):
                u, v, ppc = Wf.on_floor(hi)
                tone, jm, _ = courses(u, v, long=460.0, high=tread, seed=seed + 50 + i, joint=1.2, ppc=ppc)
                own = col(TRAV)[None, None, :] * (1 + (tone[..., None] - 0.5) * 0.06) * (1 + (tex(u, v + i * 60, 110, seed + 11)[..., None] - 0.5) * 0.06)
                own = own * weather(u, np.full_like(u, hi))
                own = own * (1 - 0.14 * jm[..., None])
                tv = (v - vk(i)) / tread
                trodden = np.exp(-((u - (W_ - 700)) / 500.0) ** 2) * 0.6
                own = own * (1 + 0.08 * trodden[..., None])
                own = own * (1 - 0.18 * step(0.70, 1.0, tv + 0.12 * (tex(u, v, 30, seed + 13) - 0.5))[..., None])
                cv.put(LIT.on(own * 1.02, TREAD_SUN, 0.0, up=1, bounce=0.5), m, Wf)
    # ---- the cheek wall that ends the flight on our side: its outer face (in shade), its sloping coping, its end
    slope = lambda v: np.clip(rise * 2.0 + (v - vf) / (-porch - vf) * (hp - rise * 2.0), rise * 2.0, hp)
    prof = [(W_, vf, 0.0), (W_, -porch, 0.0), (W_, -porch, hp + 40), (W_, vf + 60, rise * 2.0 + 40)]
    for Wf, m in kf.face(prof):
        v, h, ppc = Wf.on_side(W_)
        own, _ = travertine(v, h, ppc, seed + 3, base="#e9dfca", long=110, high=52)
        top = slope(v) + 40
        own = own * (1 - 0.0 * (h > top)[..., None])
        bounce = 0.6 + 0.9 * np.clip(1 - h / 200.0, 0, 1)
        cv.put(LIT.on(own, max(0.0, SIDE), 0.0, deep=0.10, bounce=bounce), m, Wf)
    for Wf, m in kf.face([(W_ - cheek, vf + 60, rise * 2.0 + 40), (W_, vf + 60, rise * 2.0 + 40), (W_, -porch, hp + 40), (W_ - cheek, -porch, hp + 40)]):
        u, v, ppc = Wf.on_floor(hp)
        cv.put(LIT.on(col(MARBLE) * (0.95 + 0.08 * tex(u, v, 40, seed + 4)[..., None]), 0.75, 0.0, up=0.7), m, Wf)
    for Wf, m in kf.face([(W_ - cheek, vf, 0), (W_, vf, 0), (W_, vf + 60, rise * 2.0 + 40), (W_ - cheek, vf + 60, rise * 2.0 + 40)]):
        u, h, ppc = Wf.on_front(vf)
        own, _ = travertine(u, h, ppc, seed + 5, base="#ece2cc")
        cv.put(LIT.on(own, STEP_SUN + 0.04, 0.0, bounce=0.7), m, Wf)
    # the moulded base and coping lines of the cheek wall, crisp; and every step's edge: a bright worn arris in broken
    # runs, chipped here and there, and a faint dark line, also broken, where each riser stands on the tread below
    s = Sheet(SHAPE)
    rng = np.random.default_rng(seed + 60)
    for i in range(1, n + 1):
        hi = i * rise
        u = u0
        while u < u1:
            u2 = min(u1, u + rng.uniform(60, 260))
            if rng.random() < 0.85:
                s.line([kf.pt(u, vk(i), hi - rise + 0.5), kf.pt(u2, vk(i), hi - rise + 0.5)], "#8c7a74", 1.0, rng.uniform(0.18, 0.38))
            if rng.random() < 0.82:
                if hi < EYE + 30:
                    s.line([kf.pt(u, vk(i), hi), kf.pt(u2, vk(i), hi)], "#fff8e6", 1.0, rng.uniform(0.40, 0.80))
                else:
                    s.line([(q[0], q[1] + 0.8) for q in (kf.pt(u, vk(i), hi), kf.pt(u2, vk(i), hi))], "#b8aab4", 0.9, rng.uniform(0.25, 0.5))
            u = u2 + rng.uniform(3, 40)
        for j in range(int(rng.integers(0, 3))):
            a = kf.pt(rng.uniform(W_ - 1500, u1 - 20), vk(i), hi)
            if 0 <= a[0] < 200:
                w = rng.uniform(1.0, 2.6)
                s.poly([(a[0] - w, a[1] - 0.3), (a[0] + w, a[1] - 0.3), (a[0] + rng.uniform(-1.0, 1.0), a[1] + rng.uniform(1.0, 2.2))], "#a8947c", rng.uniform(0.35, 0.6))   # a chip out of the edge
    a0, a1 = kf.pt(W_, vf, 30), kf.pt(W_, -porch, 30)
    s.line([a0, a1], "#9a92a8", 1.1, 0.7)
    b0, b1 = kf.pt(W_, vf + 60, rise * 2.0 + 40), kf.pt(W_, -porch, hp + 40)
    s.line([b0, b1], "#fff4dc", 1.3, 0.85)
    s.line([(b0[0], b0[1] + 2.4), (b1[0], b1[1] + 2.4)], "#8a82a0", 1.0, 0.7)
    # ---- the columns of the front, the two nearest (a third just at the left edge)
    for j in range(3):
        cu = W_ - 120 - j * c["gap"]
        prof_ = castor_column_profile(hp, c["cols"])
        k_ = kf.k(cu, 0)
        xc = kf.pt(cu, 0, hp)[0]
        top_y = kf.pt(cu, 0, hp + c["cols"])[1]
        Wc = kf.window([(xc - 80 * k_, max(-5.0, top_y)), (xc + 80 * k_, kf.pt(cu, -60, hp - 10)[1])])
        if Wc is None:
            continue
        shade_fn = lambda h, s_, around: np.zeros_like(h)
        cc, ca = lathe(Wc, LIT, cu, 0.0, prof_, castor_column_paint(seed + 20 + j * 7, hp), flutes=24, flute_from=hp + 46 + 30, flute_to=hp + c["cols"] - 140, deep=0.0, bounce=0.5)
        # the column's square plinth on the porch floor (its front shows above the top step)
        for Wp, mp in kf.face([(cu - 78, -78, hp - 2), (cu + 78, -78, hp - 2), (cu + 78, -78, hp + 16), (cu - 78, -78, hp + 16)]):
            uu, hh, pp = Wp.on_front(-78.0)
            cv.put(LIT.on(col(TRAV) * (0.93 + 0.1 * tex(uu, hh, 20, seed + 30)[..., None]), STEP_SUN + 0.04, 0.0, bounce=0.5), mp, Wp)
        cv.put(cc, ca, Wc)
    # the crown moulding of the podium under the porch's edge, seen from below between the columns
    s.line([kf.pt(u0, -porch, hp), kf.pt(W_, -porch, hp)], "#fbf0d8", 1.2, 0.9)
    s.line([kf.pt(u0, -porch - 6, hp - 8), kf.pt(W_, -porch - 6, hp - 8)], "#9088a6", 1.0, 0.7)
    sc, sa = s.done()
    cv.put(sc, sa)
    return cv


def castor_base_line():
    """Castor's cut-out's base: the foot of the cheek wall, from the front of the steps to the podium's corner."""
    kf = castor_frame()
    c = CASTOR
    a = kf.pt(c["width"], castor_steps_foot(), 0)
    b = kf.pt(c["width"], -c["porch"], 0)
    return [[round(a[0], 1), round(a[1], 1)], [round(b[0], 1), round(b[1], 1)]]


# ---------------------------------------------------------------- Juturna's spring
def basin(seed=85):
    """Juturna's spring: a square basin of stone, its rim worn smooth, full of clear still water that shows its stone
    floor and a little of the sky; at its back, against the lowest step, the spout where the spring comes in. (The water's
    movement is the engine's: the stream from the spout, rings where it falls, light on the water.) -> Canvas"""
    b = BASIN
    cv = Canvas(SHAPE)
    x0, x1, D0, D1, hh, w = b["x0"], b["x1"], b["D0"], b["D1"], b["h"], b["wall"]
    # the water: a level surface a little under the rim; the floor seen through it
    for Wf, m in WORLD.face([(x0 + w, D0 + w, hh - 8), (x1 - w, D0 + w, hh - 8), (x1 - w, D1 - w, hh - 8), (x0 + w, D1 - w, hh - 8)]):
        u, v, ppc = Wf.on_floor(hh - 8)
        floor_, jm = travertine(u, v, ppc, seed + 1, base="#c9d2c4", long=70, high=50, holes_=False)
        depth = np.clip((v - D0) / (D1 - D0), 0, 1)
        water = lerp(floor_ * np.array([0.62, 0.80, 0.84], dtype=F32), col("#5f8fae"), (0.30 + 0.35 * depth)[..., None])
        sky_ = col("#a9cde6")
        water = lerp(water, sky_, (0.22 * (1 - depth))[..., None])              # the near water gives back the bright sky
        shade_ = np.clip((v - (D1 - 80)) / 60.0, 0, 1) * 0.5                   # the back wall's shadow on the water
        cv.put(LIT.on(water, 0.6, shade_, up=1, bounce=0.2), m, Wf)
    # the rim: the near wall's top, the two side walls' tops
    for (a, bb, c_, d_) in (((x0, D0), (x1, D0), (x1, D0 + w), (x0, D0 + w)), ((x1 - w, D0), (x1, D0), (x1, D1), (x1 - w, D1)), ((x0, D1 - w), (x1, D1 - w), (x1, D1), (x0, D1))):
        for Wf, m in WORLD.face([(a[0], a[1], hh), (bb[0], bb[1], hh), (c_[0], c_[1], hh), (d_[0], d_[1], hh)]):
            u, v, ppc = Wf.on_floor(hh)
            own = col("#f2eadb") * (0.92 + 0.12 * tex(u, v, 25, seed + 2)[..., None])
            cv.put(LIT.on(own, 0.62, 0.0, up=1), m, Wf)
    # the near wall's face (toward us: in the sun) and the right wall's face (toward the square: in shade)
    for Wf, m in WORLD.face([(x0, D0, 0), (x1, D0, 0), (x1, D0, hh), (x0, D0, hh)]):
        u, h, ppc = Wf.on_front(D0)
        own, _ = travertine(u, h, ppc, seed + 3, base="#ebe1cc", long=95, high=hh + 2)
        own = own * (1 - 0.2 * np.clip(1 - h / 14.0, 0, 1)[..., None] * np.array([0.6, 0.5, 0.3], dtype=F32))   # green damp at the foot
        cv.put(LIT.on(own, FACE_US, 0.0, bounce=0.5), m, Wf)
    for Wf, m in WORLD.face([(x1, D0, 0), (x1, D1, 0), (x1, D1, hh), (x1, D0, hh)]):
        v, h, ppc = Wf.on_side(x1)
        own, _ = travertine(v, h, ppc, seed + 4, base="#e6dcc6", long=95, high=hh + 2)
        cv.put(LIT.on(own, 0.0, 0.0, deep=0.05, bounce=0.9), m, Wf)
    s = Sheet(SHAPE)
    for p0, p1, tone, wd, al in (((x0, D0, hh), (x1, D0, hh), "#fff8e8", 1.2, 0.9), ((x1, D0, hh), (x1, D0, 0), "#b8b0c4", 1.0, 0.6), ((x1, D0, hh), (x1, D1, hh), "#fff4e0", 1.0, 0.7)):
        s.line([pt(p0[0], p0[2], p0[1]), pt(p1[0], p1[2], p1[1])], tone, wd, al)
    # the spout: a small stone head in the back wall, the water's way in
    sx_, sy_ = pt(SPOUT[0], hh + 14, SPOUT[1])
    kk = k(SPOUT[1])
    s.ellipse(sx_, sy_ - 4 * kk, 5 * kk, 4.4 * kk, "#cfc2aa")
    s.ellipse(sx_ - 1 * kk, sy_ - 5 * kk, 2.6 * kk, 2.2 * kk, "#efe4d0")
    s.ellipse(sx_, sy_ - 1.5 * kk, 1.6 * kk, 1.1 * kk, "#2e3a44")
    sc, sa = s.done()
    cv.put(sc, sa)
    return cv


SPOUT = (BASIN["x0"] + 0.62 * (BASIN["x1"] - BASIN["x0"]), BASIN["D1"] - 4.0)       # where the spring comes in, at the back


# ---------------------------------------------------------------- the Puteal
def puteal(seed=87):
    """The Puteal: a round kerb of white stone round a spot once struck by lightning, carved with garlands and lyres,
    worn by the moneylenders who meet here. -> Canvas"""
    p = PUTEAL
    cv = Canvas(SHAPE)
    Wf = WORLD.window([pt(p["x"] - p["r"] - 10, p["h"] + 20, p["D"]), pt(p["x"] + p["r"] + 10, -5, p["D"] + p["r"])])
    prof = [(0, p["r"] + 6), (8, p["r"] + 6), (10, p["r"]), (p["h"] - 12, p["r"]), (p["h"] - 10, p["r"] + 5), (p["h"], p["r"] + 5)]

    def paint(h, around):
        a = around * 2 * math.pi * p["r"]
        c = np.empty(h.shape + (3,), dtype=F32)
        c[...] = col("#f3ecdc")
        c *= (1 + (tex(a, h, 60, seed)[..., None] - 0.5) * 0.10)
        band = (h > 18) & (h < p["h"] - 16)
        # a garland swinging between ox-skulls, and a lyre in every other bay: low relief, read by its shadows
        q = (a % 70.0) / 70.0
        swag = np.abs((h - 18) - (34 - 22 * np.sin(math.pi * q))) < 4.0
        lyre = (np.abs(q - 0.5) < 0.08) & (np.abs(h - 44) < 14) & ((np.floor(a / 70.0) % 2) == 0)
        c = np.where((band & swag)[..., None], col("#c8bca8"), c)
        c = np.where((band & lyre)[..., None], col("#bdb0a0"), c)
        c = np.where((np.abs(h - 18) < 1.6)[..., None] | (np.abs(h - (p["h"] - 16)) < 1.6)[..., None], col("#b0a698"), c)
        return np.clip(c, 0, 1).astype(F32)
    cc, ca = lathe(Wf, LIT, p["x"], p["D"], prof, paint, deep=0.0, bounce=0.6)
    # the top of the kerb, a ring, and the hollow inside it
    for Wt, mt in WORLD.face([(p["x"] - p["r"] - 5, p["D"] - p["r"] - 5, p["h"]), (p["x"] + p["r"] + 5, p["D"] - p["r"] - 5, p["h"]), (p["x"] + p["r"] + 5, p["D"] + p["r"] + 5, p["h"]), (p["x"] - p["r"] - 5, p["D"] + p["r"] + 5, p["h"])]):
        u, v, ppc = Wt.on_floor(p["h"])
        r_ = np.hypot(u - p["x"], v - p["D"])
        ring = (r_ < p["r"] + 5) & (r_ > p["r"] - 14)
        hole = r_ <= p["r"] - 14
        own = np.where(hole[..., None], col("#6a5a50") * (0.7 + 0.4 * tex(u, v, 15, seed + 2)[..., None]), col("#fbf4e6"))
        a_ = (ring | hole).astype(F32) * mt
        cv.put(LIT.on(own, 0.62, np.where(hole, 0.6, 0.0), up=1, deep=np.where(hole, 0.4, 0.0)), a_, Wt)
    cv.put(cc, ca, Wf)
    return cv


# ---------------------------------------------------------------- the moneychanger's table, and its awning
def table(seed=89):
    """The moneychanger's table by the Puteal, set out and waiting for him: a heavy table with a striped cloth over his
    scales and his stacks of coin, a stool behind it, and the two poles that hold the little awning. -> Canvas"""
    t = TABLE
    cv = Canvas(SHAPE)
    x, D_, w, d, h = t["x"], t["D"], t["w"], t["d"], t["h"]
    x0, x1, D0, D1 = x - w / 2, x + w / 2, D_ - d / 2, D_ + d / 2
    s = Sheet2(SHAPE)
    # the stool behind it
    for (lx, lD) in ((x - 30, D1 + 40), (x + 30, D1 + 40), (x - 26, D1 + 76), (x + 26, D1 + 76)):
        s.line([pt(lx, 0, lD), pt(lx, 44, lD)], "#6a4a34", max(1.0, 5 * k(lD)))
    s.poly([pt(x - 36, 46, D1 + 36), pt(x + 36, 46, D1 + 36), pt(x + 32, 46, D1 + 80), pt(x - 32, 46, D1 + 80)], "#a87a50")
    # the poles of the awning, at the back corners, and their stays
    for px_ in (x0 + 6, x1 - 6):
        a, b = pt(px_, 0, D1 + 8), pt(px_, t["awning"] + 6, D1 + 8)
        s.line([a, b], "#5e3e28", max(1.2, 6 * k(D1)))
        s.line([(a[0] - 0.6, a[1]), (b[0] - 0.6, b[1])], "#c99a62", max(0.7, 2.2 * k(D1)), 0.9)
    sc, sa = s.done()
    cv.put(sc, sa)
    # the table: legs, the apron, the top under its cloth
    for (lx, lD) in ((x0 + 8, D0 + 8), (x1 - 8, D0 + 8)):
        for Wf, m in WORLD.face([(lx - 5, lD, 0), (lx + 5, lD, 0), (lx + 5, lD, h - 12), (lx - 5, lD, h - 12)]):
            cv.put(LIT.on(col(WOOD), FACE_US, 0.0, bounce=0.6), m, Wf)
    cloth = "#e9dcc0"
    for Wf, m in WORLD.face([(x0 - 6, D0 - 6, h - 24), (x1 + 6, D0 - 6, h - 24), (x1 + 6, D0 - 6, h + 2), (x0 - 6, D0 - 6, h + 2)]):
        u, hh, ppc = Wf.on_front(D0 - 6)
        stripe = (np.abs(((u - x0) % 34.0) - 17) < 4.0)
        own = np.where(stripe[..., None], col("#b9473a"), col(cloth)) * (0.94 + 0.10 * tex(u, hh, 20, seed)[..., None])
        fold = np.abs(np.sin((u - x0) / 9.0)) * 0.08 * np.clip((h - hh) / 20.0, 0, 1)
        own = own * (1 - fold[..., None])
        cv.put(LIT.on(own, FACE_US, 0.0, bounce=0.6), m, Wf)
    for Wf, m in WORLD.face([(x0 - 6, D0 - 6, h + 2), (x1 + 6, D0 - 6, h + 2), (x1 + 6, D1 + 6, h + 2), (x0 - 6, D1 + 6, h + 2)]):
        u, v, ppc = Wf.on_floor(h + 2)
        own = col(cloth) * (0.95 + 0.08 * tex(u, v, 18, seed + 1)[..., None])
        # what lies under the cloth: the long beam of the scales and its pans, two stacks of coin
        lump = np.exp(-(((u - (x + 30)) / 32.0) ** 2 + ((v - D_) / 14.0) ** 2)) + 0.8 * np.exp(-(((u - (x - 40)) / 10.0) ** 2 + ((v - (D_ - 6)) / 8.0) ** 2)) \
            + 0.8 * np.exp(-(((u - (x - 18)) / 9.0) ** 2 + ((v - (D_ + 10)) / 8.0) ** 2))
        cv.put(LIT.on(own * (1 + 0.10 * lump[..., None]), 0.62 + 0.2 * lump, 0.0, up=1), m, Wf)
    s = Sheet2(SHAPE)
    a = pt(x + 30, h + 14, D_)
    s.line([pt(x - 4, h + 6, D_), pt(x + 64, h + 6, D_)], "#d8ccb0", 1.0, 0.9)              # the cloth draped over the scale's beam
    s.line([pt(x0 - 6, h + 2, D0 - 6), pt(x1 + 6, h + 2, D0 - 6)], "#fff8e8", 1.0, 0.85)
    for px_ in (x0 - 6 + 12, x1 + 6 - 12):
        s.line([pt(px_, h + 2, D0 - 6), pt(px_ + 3, h - 26, D0 - 6)], "#a8988a", 0.8, 0.6)     # the cloth's corners hang
    sc, sa = s.done()
    cv.put(sc, sa)
    return cv


def awning(seed=91):
    """The little awning over the table: a square of striped linen tied to the tops of the two poles behind and held
    out over the table on two light rods, its front edge a hem with a fringe. A cut-out of its own: it stirs. -> Canvas"""
    t = TABLE
    cv = Canvas(SHAPE)
    x, D_, w, d = t["x"], t["D"], t["w"], t["d"]
    x0, x1, D0, D1 = x - w / 2, x + w / 2, D_ - d / 2, D_ + d / 2
    hb, hf = t["awning"] + 4, t["awning"] - 26                    # its back edge on the poles, its front edge lower
    Dbk, Dfr = D1 + 8, D0 - 40
    for Wf, m in WORLD.face([(x0 - 8, Dfr, hf), (x1 + 8, Dfr, hf), (x1 + 8, Dbk, hb), (x0 - 8, Dbk, hb)]):
        u, v, ppc = Wf.on_floor(hf)
        stripe = ((np.floor((u - x0) / 22.0) % 2) == 0)
        own = np.where(stripe[..., None], col("#c95a3e"), col("#f2e4c4")) * (0.94 + 0.1 * tex(u, v, 30, seed)[..., None])
        sag = np.sin(np.clip((v - Dfr) / (Dbk - Dfr), 0, 1) * math.pi)
        cv.put(LIT.on(own * (1 - 0.06 * sag[..., None]), 0.35, 0.0, up=-0.6, deep=0.2, bounce=0.9), m, Wf)
    # its front hem, hanging: lit, with a fringe
    for Wf, m in WORLD.face([(x0 - 8, Dfr, hf - 16), (x1 + 8, Dfr, hf - 16), (x1 + 8, Dfr, hf), (x0 - 8, Dfr, hf)]):
        u, h, ppc = Wf.on_front(Dfr)
        stripe = ((np.floor((u - x0) / 22.0) % 2) == 0)
        own = np.where(stripe[..., None], col("#c95a3e"), col("#f2e4c4"))
        fringe = (h < hf - 10) & ((np.floor(u / 4.0) % 2) == 0)
        own = np.where(fringe[..., None], col("#e8c070"), own)
        cv.put(LIT.on(own, FACE_US, 0.0, bounce=0.5), m * np.where((h < hf - 10) & ((np.floor(u / 4.0) % 2) == 1), 0.0, 1.0), Wf)
    s = Sheet2(SHAPE)
    for px_ in (x0 - 4, x1 + 4):                                   # the two light rods that hold its front out
        s.line([pt(px_, hb - 4, Dbk), pt(px_, hf, Dfr)], "#6a4a30", 1.0, 0.9)
    sc, sa = s.done()
    cv.put(sc, sa)
    return cv


# ---------------------------------------------------------------- the hoarding of the senate house's site
def hoard_frame():
    """The hoarding as a frame: u along its face from its far end (b, u = 0) to its near end (a); v into the site."""
    (ax, aD), (bx, bD) = HOARD["a"], HOARD["b"]
    ang = math.degrees(math.atan2(aD - bD, ax - bx))
    return frame(ang, bx, bD), math.hypot(ax - bx, aD - bD)


def hoard_gate():
    """The gateway's two sides, as u along the hoarding's frame."""
    fr, L = hoard_frame()
    g0, g1 = HOARD["gate"]                                         # fractions from the near end
    return L * (1 - g1), L * (1 - g0)


def hoarding(seed=93):
    """The hoarding round the building site: a fence of upright boards a little over two metres high, weathered, its posts
    showing, its face toward the square taking the low sun at a slant; an open gateway in it, its two gateposts and the
    gate itself swung back inside. Its foot is the cut-out's base. -> Canvas"""
    fr, L = hoard_frame()
    g0, g1 = hoard_gate()
    hh = HOARD["h"]
    cv = Canvas(SHAPE)
    su, sv, sh = fr.to_frame(SUN)
    FACE = -sv
    for (ua, ub) in ((-60.0, g0), (g1, L + 400.0)):
        for Wf, m in fr.face([(ua, 0, 0), (ub, 0, 0), (ub, 0, hh), (ua, 0, hh)]):
            u, h, ppc = Wf.on_front(0.0)
            ragged = hh - 6 + 10 * hash2(np.floor(u / 24.0), 2, seed)                  # the boards' tops are not cut level
            own = boards(u, h, seed, width=24.0, base="#b98e5e", ppc=ppc)
            post = (np.abs(((u + 40) % 300.0) - 150.0) > 141)                         # a post every three metres, its face darker
            own = np.where(post[..., None], own * np.array([0.82, 0.76, 0.72], dtype=F32), own)
            rail = (np.abs(h - 40) < 6) | (np.abs(h - (hh - 40)) < 6)
            own = np.where(rail[..., None] & ~post[..., None], own * 0.92, own)
            mud = np.clip(1 - h / 30.0, 0, 1) * (0.5 + tex(u, h, 40, seed + 3))
            own = own * (1 - 0.25 * np.clip(mud, 0, 1)[..., None] * np.array([0.6, 0.7, 0.8], dtype=F32))
            mm = m * (h < ragged)
            cv.put(LIT.on(own, FACE, 0.0, bounce=0.6 * np.clip(1 - h / 150.0, 0, 1) + 0.15), mm, Wf)
    s = Sheet2(SHAPE)
    # the gateposts, heavy, a little taller than the boards; the gate swung back into the site
    for gu in (g0, g1):
        a, b = fr.pt(gu, 0, 0), fr.pt(gu, 0, hh + 30)
        kk = fr.k(gu, 0)
        s.line([a, b], "#6e4a30", max(1.5, 18 * kk))
        s.line([(a[0] - 1.2, a[1]), (b[0] - 1.2, b[1])], "#d8a870", max(0.8, 6 * kk), 0.9)
    gate = [fr.pt(g1, 6, 20), fr.pt(g1 - 30, 150, 20), fr.pt(g1 - 30, 150, hh - 30), fr.pt(g1, 6, hh - 20)]
    s.poly(gate, "#8a6440")
    for q in np.linspace(0.15, 0.85, 4):
        s.line([fr.pt(g1 - 30 * q, 6 + 144 * q, 22), fr.pt(g1 - 30 * q, 6 + 144 * q, hh - 24)], "#5a3e28", 0.8, 0.7)
    # the top edge catches the light; a few nail heads; weathered streaks
    rng = np.random.default_rng(seed)
    for (ua, ub) in ((-60.0, g0), (g1, L)):
        for u_ in np.arange(ua + 12, ub, 24.0):
            for hh_ in (40, hh - 40):
                p_ = fr.pt(u_, -1, hh_)
                if rng.random() < 0.7:
                    s.ellipse(p_[0], p_[1], 0.7, 0.7, "#3e2c22", 0.8)
    sc, sa = s.done()
    cv.put(sc, sa)
    return cv


def hoarding_base_line():
    fr, L = hoard_frame()
    a, b = fr.pt(0, 0, 0), fr.pt(L, 0, 0)
    return [[round(a[0], 1), round(a[1], 1)], [round(b[0], 1), round(b[1], 1)]]


# The hoarding is laid as two cut-outs, cut at the middle of its gateway: `hoarding` (the far part, to the far gatepost)
# and `hoarding-near` (from the near gatepost on, with the gate swung back inside). Each has its own base line, which the
# engine holds at its own ends. One cut-out with one long slanted base would make the engine's depth comparison go round
# in a circle (cast.js compares a person with a cut-out at the person's x, and two people by their feet only): someone
# standing in front of its far end, higher in the picture than someone standing in the gateway or behind it, would be
# drawn in front of the one and behind the other, and the sort could then put either on the wrong side of the boards.
def hoarding_split_x():
    """Where the hoarding's picture is cut in two: the middle of the gateway (a picture column)."""
    fr, L = hoard_frame()
    g0, g1 = hoard_gate()
    return 0.5 * (fr.pt(g0, 0, 0)[0] + fr.pt(g1, 0, 0)[0])


def hoarding_base_lines():
    """-> (the far part's base: its far end to the far gatepost's foot, the near part's: the near gatepost's foot to its
    near end, beyond the picture's edge)."""
    fr, L = hoard_frame()
    g0, g1 = hoard_gate()
    r = lambda p: [round(float(p[0]), 1), round(float(p[1]), 1)]
    return [r(fr.pt(0, 0, 0)), r(fr.pt(g0, 0, 0))], [r(fr.pt(g1, 0, 0)), r(fr.pt(L, 0, 0))]


# ---------------------------------------------------------------- honorary statues on their columns
def statue(i, seed=95):
    """An honorary statue on a tall column: a moulded base, a plain shaft of white stone, a capital, and a man in a toga
    cast in bronze, gone dark and green, one arm raised as if speaking. Nobody in particular. -> Canvas"""
    x, D_, hc = STATUES[i]
    cv = Canvas(SHAPE)
    hb = 150.0
    # the base: a block, its front toward us in the sun, its left side too, mouldings top and bottom
    for Wf, m in WORLD.face([(x - 62, D_ - 62, 0), (x + 62, D_ - 62, 0), (x + 62, D_ - 62, hb), (x - 62, D_ - 62, hb)]):
        u, h, ppc = Wf.on_front(D_ - 62)
        own = col("#f1e8d6") * (0.92 + 0.10 * tex(u, h, 40, seed + i)[..., None])
        own = own * (1 - 0.3 * (np.clip(1.5 - np.abs(h - 18) * ppc / 1.2, 0, 1) + np.clip(1.5 - np.abs(h - (hb - 18)) * ppc / 1.2, 0, 1))[..., None])
        panel = (np.abs(u - x) < 40) & (h > 40) & (h < hb - 40)
        own = np.where(panel[..., None], own * 0.95, own)
        cv.put(LIT.on(own, FACE_US, 0.0, bounce=0.6), m, Wf)
    if x < 0:
        pass
    for Wf, m in WORLD.face([(x - 62, D_ - 62, 0), (x - 62, D_ + 62, 0), (x - 62, D_ + 62, hb), (x - 62, D_ - 62, hb)]) if x > 0 else []:
        v, h, ppc = Wf.on_side(x - 62)
        cv.put(LIT.on(col("#ece2cc"), FACE_LEFT, 0.0, bounce=0.5), m, Wf)
    for Wf, m in WORLD.face([(x + 62, D_ - 62, 0), (x + 62, D_ + 62, 0), (x + 62, D_ + 62, hb), (x + 62, D_ - 62, hb)]) if x < 0 else []:
        v, h, ppc = Wf.on_side(x + 62)
        cv.put(LIT.on(col("#ece2cc"), 0.0, 0.0, deep=0.05, bounce=0.7), m, Wf)
    # the shaft
    prof = [(hb, 36), (hb + 10, 36), (hb + 14, 32)] + [(hb + 14 + (hc - 30) * q, 32 - 4 * q) for q in np.linspace(0.1, 1, 8)] + [(hb + hc - 12, 30), (hb + hc - 4, 40), (hb + hc + 8, 44)]
    k_ = k(D_)
    xc = pt(x, 0, D_)[0]
    Wc = WORLD.window([(xc - 50 * k_, pt(x, hb + hc + 12, D_)[1]), (xc + 50 * k_, pt(x, hb - 2, D_ - 40)[1])])

    def paint(h, around):
        c_ = np.empty(h.shape + (3,), dtype=F32)
        c_[...] = col("#f4ecdc")
        return (c_ * (0.95 + 0.07 * tex(around * 200, h, 60, seed + 10 + i)[..., None])).astype(F32)
    cc, ca = lathe(Wc, LIT, x, D_, prof, paint, bounce=0.5)
    cv.put(cc, ca, Wc)
    # the abacus, and the bronze figure on it
    top = hb + hc + 8
    s = Sheet2(SHAPE)
    a0, a1 = pt(x - 48, top, D_ - 48), pt(x + 48, top + 12, D_ - 48)
    s.poly([(a0[0], a0[1]), (a1[0], a0[1]), (a1[0], a1[1]), (a0[0], a1[1])], "#f6eee0")
    fx_, fy_ = pt(x, top + 12, D_)
    kk = k(D_)
    body, lite, dark = "#46604f", "#8fb08a", "#2a3a34"
    s.poly([(fx_ - 20 * kk, fy_), (fx_ + 22 * kk, fy_), (fx_ + 18 * kk, fy_ - 150 * kk), (fx_ - 16 * kk, fy_ - 150 * kk)], body)       # the toga'd body
    s.poly([(fx_ - 20 * kk, fy_), (fx_ - 6 * kk, fy_), (fx_ - 4 * kk, fy_ - 146 * kk), (fx_ - 16 * kk, fy_ - 150 * kk)], lite, 0.8)  # lit on the left
    s.line([(fx_ - 14 * kk, fy_ - 110 * kk), (fx_ + 16 * kk, fy_ - 60 * kk)], dark, max(0.8, 6 * kk), 0.8)                         # the toga's fold across
    s.ellipse(fx_ + 1 * kk, fy_ - 164 * kk, 12 * kk, 13 * kk, body)
    s.ellipse(fx_ - 3 * kk, fy_ - 167 * kk, 6 * kk, 7 * kk, lite, 0.8)
    s.line([(fx_ - 14 * kk, fy_ - 128 * kk), (fx_ - 44 * kk, fy_ - 168 * kk)], body, max(1.0, 11 * kk))                              # an arm raised
    s.line([(fx_ - 15 * kk, fy_ - 130 * kk), (fx_ - 44 * kk, fy_ - 170 * kk)], lite, max(0.6, 4 * kk), 0.8)
    sc, sa = s.done()
    cv.put(sc, sa)
    return cv


def statue_base_row(i):
    x, D_, hc = STATUES[i]
    return round(pt(x, 0, D_ - 62)[1], 1)


# ---------------------------------------------------------------- the statue base at the front
def front_base(seed=97):
    """A statue's base near us at the bottom right: a tall block of white stone on a moulded footing, with a crowning
    moulding; its statue not yet set up on it, only the lead-filled holes waiting. People pass behind it. -> Canvas"""
    f = FRONT_BASE
    x, D_, w, d, hh = f["x"], f["D"], f["w"], f["d"], f["h"]
    x0, x1, D0, D1 = x - w / 2, x + w / 2, D_ - d / 2, D_ + d / 2
    cv = Canvas(SHAPE)
    for (e, h0, h1, tone) in ((8, 0, 16, "#e6dcc8"), (0, 16, hh - 16, "#f2eadb"), (8, hh - 16, hh, "#f7f0e2")):
        for Wf, m in WORLD.face([(x0 - e, D0 - e, h0), (x1 + e, D0 - e, h0), (x1 + e, D0 - e, h1), (x0 - e, D0 - e, h1)]):
            u, h, ppc = Wf.on_front(D0 - e)
            own = col(tone) * (0.92 + 0.10 * tex(u, h, 40, seed + int(h0))[..., None])
            lichen = step(0.6, 0.75, tex(u, h, 26, seed + 11)) * step(0.5, 0.8, tex(u, h, 120, seed + 12))
            own = own * (1 - 0.25 * lichen[..., None] * np.array([0.5, 0.4, 0.9], dtype=F32))
            cv.put(LIT.on(own, FACE_US, 0.0, bounce=0.5), m, Wf)
        for Wf, m in WORLD.face([(x0 - e, D0 - e, h0), (x0 - e, D1 + e, h0), (x0 - e, D1 + e, h1), (x0 - e, D0 - e, h1)]):
            v, h, ppc = Wf.on_side(x0 - e)
            cv.put(LIT.on(col(tone) * 0.97, FACE_LEFT, 0.0, bounce=0.5), m, Wf)
    for Wf, m in WORLD.face([(x0 - 8, D0 - 8, hh), (x1 + 8, D0 - 8, hh), (x1 + 8, D1 + 8, hh), (x0 - 8, D1 + 8, hh)]):
        u, v, ppc = Wf.on_floor(hh)
        own = col("#f6efe2") * (0.93 + 0.1 * tex(u, v, 30, seed + 3)[..., None])
        holes_ = (np.hypot(u - (x - 30), v - D_) < 6) | (np.hypot(u - (x + 34), v - (D_ + 8)) < 6)
        own = np.where(holes_[..., None], col("#6a6470"), own)
        cv.put(LIT.on(own, 0.62, 0.0, up=1), m, Wf)
    s = Sheet2(SHAPE)
    for (p0, p1, tone, wd, al) in (((x0 - 8, hh, D0 - 8), (x1 + 8, hh, D0 - 8), "#fffaf0", 1.3, 0.9), ((x0, 16, D0), (x1, 16, D0), "#a8a0b4", 1.1, 0.7),
                                   ((x0, hh - 16, D0), (x1, hh - 16, D0), "#a8a0b4", 1.1, 0.7)):
        s.line([pt(*p0), pt(*p1)], tone, wd, al)
    sc, sa = s.done()
    cv.put(sc, sa)
    return cv


# ---------------------------------------------------------------- Phyllis's place (in the backdrop)
def garlands(sheet, seed=99):
    """Her baskets round her place (violets, laurel, myrtle), the finished garlands hung on a pole beside it, a few
    stems dropped on the paving. Her own place is left clear: the game draws her on her low stool."""
    rng = np.random.default_rng(seed)
    px_, pD = PHYLLIS
    s = sheet

    def basket(x, D_, w, h0, kind):
        kk = k(D_)
        b0, b1 = pt(x - w / 2, h0, D_), pt(x + w / 2, h0, D_)
        top = pt(x, h0 + 22, D_)[1]
        bw = (b1[0] - b0[0])
        s.ellipse((b0[0] + b1[0]) / 2 + bw * 0.12, b0[1] + 0.5, bw * 0.62, bw * 0.12, "#8f86a4", 0.55)       # its shadow, away and right
        s.poly([(b0[0], b0[1]), (b1[0], b1[1]), (b1[0] + bw * 0.08, top), (b0[0] - bw * 0.08, top)], "#b0864e")
        s.poly([(b0[0], b0[1]), (b0[0] + bw * 0.25, b0[1]), (b0[0] + bw * 0.2, top), (b0[0] - bw * 0.08, top)], "#d6a868", 0.8)
        for j in range(4):
            yy = lerp(b0[1], top, (j + 0.5) / 4)
            s.line([(b0[0] - bw * 0.04 * j / 3, yy), (b1[0] + bw * 0.04 * j / 3, yy)], "#7a5a34", 0.7, 0.7)
        s.ellipse((b0[0] + b1[0]) / 2, top, bw * 0.55, bw * 0.16, "#6a4a2c")
        for j in range(int(40 * bw / 30) + 10):                              # what fills it, heaped a little over the rim
            ex = (b0[0] + b1[0]) / 2 + rng.uniform(-0.5, 0.5) * bw * 0.95
            ey = top - abs(rng.normal(0, bw * 0.06)) * (1 - abs(ex - (b0[0] + b1[0]) / 2) / bw) - 0.5
            if kind == "violets":
                s.ellipse(ex, ey, 1.6 * kk * 3, 1.3 * kk * 3, ["#5a2c8a", "#7a46b0", "#9a6ad0", "#3e6a2c"][int(rng.integers(4))])
            elif kind == "laurel":
                leaf(s, ex, ey, rng.uniform(0, 2 * math.pi), rng.uniform(4, 7) * kk * 2.4, ["#2c4a24", "#3f6a2c", "#5c8a34"][int(rng.integers(3))])
            else:
                leaf(s, ex, ey, rng.uniform(0, 2 * math.pi), rng.uniform(3, 5) * kk * 2.4, ["#3a6a34", "#5a8a3c", "#7aa44c"][int(rng.integers(3))], wide=0.3)
                if rng.random() < 0.3:
                    s.ellipse(ex, ey, 0.9, 0.9, "#f4f0e0")
    for (bx_, bD_, bh_, bw_, kind) in BASKETS:
        basket(bx_, bD_, bw_, bh_, kind)
    # the pole of finished garlands: a stout pole in a weighted foot, a crossbar, wreaths hanging from pegs
    x, D_ = POLE
    a, b = pt(x, 0, D_), pt(x, 196, D_)
    kk = k(D_)
    s.ellipse(a[0] + 6, a[1] + 0.5, 12 * kk * 4, 2.4 * kk * 4, "#8f86a4", 0.5)
    s.line([a, b], "#6a4a30", max(1.6, 8 * kk))
    s.line([(a[0] - 1.0, a[1]), (b[0] - 1.0, b[1])], "#c99a62", max(0.8, 2.6 * kk), 0.9)
    s.poly([(a[0] - 9 * kk * 3, a[1]), (a[0] + 9 * kk * 3, a[1]), (a[0] + 6 * kk * 3, a[1] - 7 * kk * 3), (a[0] - 6 * kk * 3, a[1] - 7 * kk * 3)], "#9a8a76")
    c0, c1 = pt(x - 46, 182, D_), pt(x + 46, 182, D_)
    s.line([c0, c1], "#6a4a30", max(1.2, 5 * kk))
    for (wx, wh, r) in ((-38, 140, 10), (-12, 116, 11), (16, 150, 9.5), (40, 126, 10.5), (2, 166, 8)):
        cx, cy = pt(x + wx, wh, D_)
        R = r * kk
        s.line([(cx, cy - R), (cx, pt(x + wx, 182, D_)[1])], "#d84a3a", 0.8)                   # its ribbon to the bar
        for j in range(16):
            q = j / 16 * 2 * math.pi
            lx, ly = cx + math.cos(q) * R, cy + math.sin(q) * R * 0.9
            tone = ["#2e5226", "#46782e", "#6a9a3c"][int(rng.integers(3))]
            leaf(s, lx, ly, q + math.pi / 2 + rng.normal(0, 0.4), rng.uniform(2.6, 3.8) * kk * 2.2, tone)
            if j % 3 == 0:
                s.ellipse(lx + rng.normal(0, 0.8), ly + rng.normal(0, 0.8), 1.3 * kk * 3, 1.1 * kk * 3, ["#6a3a9a", "#8a5ac0", "#f4ecd8"][int(rng.integers(3))])
        s.line([(cx - R * 0.2, cy + R * 0.9), (cx - R * 0.5, cy + R * 2.0)], "#d84a3a", 0.8, 0.9)
    for j in range(7):                                                       # stems and petals dropped about her place
        ex, ey = pt(px_ + rng.normal(0, 60), 0, pD + rng.normal(-20, 30))
        s.line([(ex, ey), (ex + rng.uniform(-3, 3), ey + rng.uniform(-1, 1))], "#4a6a2c", 0.8, 0.8)
        s.ellipse(ex + 1, ey, 0.9, 0.7, "#8a5ac0", 0.9)


# ---------------------------------------------------------------- what throws a shadow on the paving
def solids_world():
    """Shadow-casters in the world's own measurements (u = x, v = D, h): -> list for rome_steps_kit.sunless."""
    S = []
    j = JULIA
    S.append(("box", j["x"] - 2500, j["x"], j["D0"], j["D1"] + 2000, 0, j["roof"]))
    t = TUSCAN
    S.append(("box", t["x"] - 2600, t["x"], t["D1"] - 200, t["D1"], 0, 1100))
    p = PUTEAL
    S.append(("cyl", p["x"], p["D"], p["r"] + 5, 0, p["h"]))
    tb = TABLE
    S.append(("box", tb["x"] - tb["w"] / 2 - 6, tb["x"] + tb["w"] / 2 + 6, tb["D"] - tb["d"] / 2 - 6, tb["D"] + tb["d"] / 2 + 6, tb["h"] - 24, tb["h"] + 6))
    for lx in (tb["x"] - tb["w"] / 2 + 8, tb["x"] + tb["w"] / 2 - 8):
        S.append(("box", lx - 5, lx + 5, tb["D"] - tb["d"] / 2 + 3, tb["D"] - tb["d"] / 2 + 13, 0, tb["h"]))
    for px_ in (tb["x"] - tb["w"] / 2 + 6, tb["x"] + tb["w"] / 2 - 6):
        S.append(("cyl", px_, tb["D"] + tb["d"] / 2 + 8, 4, 0, tb["awning"] + 6))
    S.append(("box", tb["x"] - tb["w"] / 2 - 8, tb["x"] + tb["w"] / 2 + 8, tb["D"] - tb["d"] / 2 - 40, tb["D"] + tb["d"] / 2 + 8, tb["awning"] - 26, tb["awning"] + 4))
    for (x, D_, hc) in STATUES:
        S.append(("box", x - 62, x + 62, D_ - 62, D_ + 62, 0, 150))
        S.append(("cyl", x, D_, 34, 150, 150 + hc))
        S.append(("cyl", x, D_, 20, 150 + hc, 150 + hc + 175))
    f = FRONT_BASE
    S.append(("box", f["x"] - f["w"] / 2 - 8, f["x"] + f["w"] / 2 + 8, f["D"] - f["d"] / 2 - 8, f["D"] + f["d"] / 2 + 8, 0, f["h"]))
    b = BASIN
    S.append(("box", b["x0"], b["x1"], b["D0"], b["D1"], 0, b["h"]))
    S.append(("cyl", POLE[0], POLE[1], 5, 0, 196))
    S.append(("box", POLE[0] - 46, POLE[0] + 46, POLE[1] - 12, POLE[1] + 12, 105, 182))
    r = ROSTRA
    S.append(("box", r["x0"], r["x1"], r["D"] - r["bulge"], r["D"] + 600, 0, r["h"]))
    cr = CRANE
    S.append(("box", cr["x"] - 300, cr["x"] - 200, cr["D"] + 200, cr["D"] + 300, 600, 1260))
    return S


def solids_castor():
    """Castor, in its own frame: the podium and its steps (coarsely), the columns, the porch's roof far above."""
    c = CASTOR
    W_, hp = c["width"], c["podium"]
    vf = castor_steps_foot()
    S = [("box", -3000, W_, -c["porch"], CASTOR_BACK, 0, hp)]
    span = -c["porch"] - vf
    for q in range(6):                                       # the flight, as six blocks
        S.append(("box", -3000, W_, vf + span * q / 6, -c["porch"], 0, hp * (q + 1) / 6))
    for j in range(8):
        cu = W_ - 120 - j * c["gap"]
        S.append(("cyl", cu, 0.0, C_RADIUS, hp, hp + c["cols"]))
    S.append(("box", -3000, W_ + 40, -120, CASTOR_BACK, hp + c["cols"], hp + c["cols"] + 700))
    S.append(("box", -3000, W_ - 40, 600, CASTOR_BACK, hp, hp + c["cols"]))
    return S


CASTOR_BACK = 1300.0                                         # how far back the temple goes (its far end is never seen)


def castor_shade(x, h, D):
    """How much of the sun the temple of Castor takes from a place in the world (x, h, D: numbers or pictures)."""
    kf = castor_frame()
    rx, rz = np.asarray(x, dtype=F32) - kf.cx, np.asarray(D, dtype=F32) - kf.cz
    u = rx * kf.eu[0] + rz * kf.eu[1]
    v = rx * kf.ev[0] + rz * kf.ev[1]
    return sunless(solids_castor(), u, v, h, kf.to_frame(SUN))


def solids_hoard():
    fr, L = hoard_frame()
    g0, g1 = hoard_gate()
    return fr, [("box", -60, g0, 0, 8, 0, HOARD["h"]), ("box", g1, L + 400, 0, 8, 0, HOARD["h"])]


def solids_saturn():
    from rome_forum_far import saturn_frame, S_UW, S_HP, S_E3, S_BACK, S_VK, S_SU0, S_SU1, S_EDGE
    sf = saturn_frame()
    return sf, [("box", 0, S_UW, S_EDGE, S_BACK, 0, S_HP), ("box", 45, S_UW - 45, -40, S_BACK, S_HP, S_E3 + 100), ("box", S_SU0, S_SU1, S_VK(1), S_EDGE, 0, S_HP * 0.5)]

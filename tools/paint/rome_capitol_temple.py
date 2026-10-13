"""The temple of Jupiter Best and Greatest on the Capitol, painted face by face through the game's camera
(rome_capitol.py lays it into the picture).

It faces south, toward us, its front turned a little to our right, on a podium 4.5 m high with a broad flight of
25 steps across its whole front between two cheek blocks. Six plain Doric columns across the front (the coins of
43 B.C. show them Doric), three rows of them deep, and more down each flank; three doors in the back wall of the
porch, the middle one (Jupiter's) open, and far inside the dim gleam of the great seated god in gold and ivory. Over
the columns the beam, the band with one name on it in bronze letters, Q LVTATIVS CATVLVS (the man who rebuilt the
temple: the inscription's own words are not known, so nothing more is painted), the cornice, and the low broad
pediment crowded with figures. The roof is plated with gilt bronze: from down here we see it only at its edges, along
the raking cornices, the antefixes on the eaves, the corners, and the bronze chariot of four horses on the peak.

The sun is low on our right (east-south-east): the front takes it at a slant, the right-hand side of every column is
lit, the porch behind them is deep in shade, the left flank in cool shade."""

import math

import numpy as np

from brush import F32, Sheet, blur, lerp, mask_poly, noise, ramp, step
from rome_capitol_kit import *
from rome_steps_kit import Canvas, col, courses, hash2, holes, lathe, mix, stone, sunless, tex

SU, SV, SH = T.to_frame(SUN)                                 # the sun along the front, into it, and up
FR = -SV                                                     # how squarely a front faces the sun
VE = COLV - COL_R - 10.0                                     # the face of the beam over the front columns
UE0, UE1 = COLS[0] - COL_R - 10.0, COLS[-1] + COL_R + 10.0   # ...and over the flank columns
VC = VE - EAVE                                               # the face of the cornice and the pediment's raking edge
PED_V = VE + 22.0                                            # the pediment's field, a little back from the beam
MID = (UE0 + UE1) / 2                                        # the middle of the front (the peak is over it)
RK0, RK1 = UE0 - EAVE - 20.0, UE1 + EAVE + 20.0              # the ends of the raking cornices
HALF_R = MID - RK0


def rake(u):
    """The height of the underside of the raking cornice over a place along the front."""
    return E3 + (HALF_R - np.abs(u - MID)) * PITCH


PEAK = E3 + HALF_R * PITCH + 58.0                            # the top of the raking cornice at the peak, where the chariot stands

PODIUM, TRAV, STUC, STUC_SHADE = "#cdbb9a", "#efe5cf", "#f1e5c6", "#e6d7b8"
GILT, GILT_D, GILT_L = "#e2ac40", "#7d5420", "#fff0a8"
BRONZE, BRONZE_D = "#8f6a34", "#3e2e1c"
FIELD = "#4e7792"                                            # the pediment's painted field
DOORS = [(1000.0, 330.0, 700.0), (1600.0, 420.0, 820.0), (2200.0, 330.0, 700.0)]     # u of the middle, width, height


def VK(k):
    """How far back the riser of step k stands (k = 1 at the paving, 25 at the porch)."""
    return -RUN + (k - 1) * TREAD


def solids():
    """The temple as blocks, for its shadows on itself."""
    S = [("box", 0, UW, 0, BACK, 0, HP), ("box", 0, CHEEK, -RUN, 0, 0, HP), ("box", UW - CHEEK, UW, -RUN, 0, 0, HP)]
    S += [("box", CHEEK, UW - CHEEK, VK(k), 0, 0, k * RISE) for k in range(1, NSTEP + 1)]
    S += [("box", CELLA[0], CELLA[1], DEEP, BACK - 120, HP, E0)]
    S += [("cyl", cu, cv, COL_R * 0.92, HP, E0) for cu in COLS for cv in ROWS_V]
    S += [("cyl", cu, cv, COL_R * 0.92, HP, E0) for cu in (COLS[0], COLS[-1]) for cv in FLANK_V if cv > ROWS_V[-1]]
    S += [("box", UE0, UE1, VE, BACK - 60, E0, E2), ("box", UE0 - EAVE, UE1 + EAVE, VC, BACK, E2, E3),
          ("gable", UE0 - EAVE, UE1 + EAVE, VC, BACK, E3, PITCH)]
    return S


def column_profile():
    """(height, radius) up a plain Doric column from the porch floor: a low round base, the shaft with its swelling,
    the necking, the round cushion of the capital (the square slab on top is drawn as a block)."""
    r = COL_R
    p = [(0, r * 1.22), (14, r * 1.22), (17, r * 1.16), (26, r * 1.10), (32, r * 1.03), (36, r)]
    for i in range(1, 15):
        t = i / 14.0
        p.append((36 + (HC - 150) * t, r * (1 - 0.18 * (0.25 * t + 0.75 * t * t))))
    top = HC - 114
    p += [(top + 4, r * 0.80), (top + 10, r * 0.84), (top + 14, r * 0.80), (top + 30, r * 0.80), (top + 40, r * 0.94), (top + 58, r * 1.08),
          (top + 72, r * 1.12), (top + 80, r * 1.10)]
    return [(HP + a, b) for a, b in p]


def column_paint(seed, inner=False):
    """White stucco over the stone: weathered, darker where hands and rain have been, a few patches gone to the stone."""
    def paint(h, around):
        b = h - HP
        a = around * 2 * math.pi * COL_R
        c = np.empty(h.shape + (3,), dtype=F32)
        c[...] = col(STUC)
        c *= (1 + (tex(a, b, 220, seed)[..., None] - 0.5) * 0.10 + (tex(a, b, 40, seed + 1)[..., None] - 0.5) * 0.05)
        streak = step(0.6, 0.9, tex(a * 5.0, b * 0.3, 140, seed + 4)) * np.clip((b - 300) / 500.0, 0, 1)
        c = c * (1 - 0.08 * streak[..., None])
        bare = holes(a, b, seed + 5, cell=160.0, amount=0.07 + 0.08 * ((seed * 0.37) % 1), sharp=0.03) * (b > 40) * (b < HC - 130)
        c = c * (1 - 0.18 * bare[..., None] * np.array([0.6, 0.9, 1.3], dtype=F32))
        foot = np.clip(1 - b / 90.0, 0, 1)
        c = c * (1 - 0.10 * foot[..., None])
        ring = np.clip(1.5 - np.abs(b - (HC - 114 + 4)) / 2.5, 0, 1)            # the groove at the necking
        c = c * (1 - 0.35 * ring[..., None])
        return np.clip(c, 0, 1).astype(F32)
    return paint


def column(Tf, canvas, u0, v0, seed, deep=0.0, shaded=False):
    """One column: base, shaft, capital (lathe), and the square slab on top. `shaded`: it stands in the porch's
    shade (the inner rows and the flank: the porch is the picture's dark mass behind the lit front)."""
    k = Tf.k(u0, v0)
    xc = Tf.pt(u0, v0, HP)[0]
    Wf = Tf.window([(xc - COL_R * 1.4 * k, Tf.pt(u0, v0, E0 + 4)[1]), (xc + COL_R * 1.4 * k, Tf.pt(u0, v0, HP)[1])])
    if Wf is None:
        return

    def shade(h, s, around):
        if shaded:
            return np.ones(np.shape(h), F32)
        ang = around * 2 * math.pi
        du, dv = COL_R * np.cos(ang) * T.eu[0] + COL_R * np.sin(ang) * T.eu[1], COL_R * np.cos(ang) * T.ev[0] + COL_R * np.sin(ang) * T.ev[1]
        return sunless(SOL, u0 + du * 1.02, v0 + dv * 1.02, h, (SU, SV, SH), spread=0.01, eps=8.0)
    c, a = lathe(Wf, LIT, u0, v0, column_profile(), column_paint(seed), shadow=shade, deep=deep, bounce=0.7)
    canvas.put(c, a, Wf)
    ab = COL_R * 1.18                                        # the abacus: its left side, its front
    h0, h1 = E0 - 34, E0
    for Wa, m in Tf.face([(u0 - ab, v0 - ab, h0), (u0 - ab, v0 + ab, h0), (u0 - ab, v0 + ab, h1), (u0 - ab, v0 - ab, h1)]):
        canvas.put(LIT.on(col(STUC) * 0.96, 0.0, deep=deep + 0.1, bounce=0.4), m, Wa)
    for Wa, m in Tf.face([(u0 - ab, v0 - ab, h0), (u0 + ab, v0 - ab, h0), (u0 + ab, v0 - ab, h1), (u0 - ab, v0 - ab, h1)]):
        u, h, _ = Wa.on_front(v0 - ab)
        cut = sunless(SOL, u, v0 - ab - 1, h, (SU, SV, SH), spread=0.01, eps=6.0)
        canvas.put(LIT.on(col(STUC), FR, 1.0 if shaded else cut, deep=deep, bounce=0.4), m, Wa)


def mouldings(own, h, top):
    """A plinth course at the foot of the podium and a heavy crown under its top."""
    line = np.clip(1.5 - np.abs(h - 40) / 2.0, 0, 1) + np.clip(1.5 - np.abs(h - (top - 34)) / 2.5, 0, 1) + np.clip(1.5 - np.abs(h - (top - 12)) / 2.0, 0, 1)
    return own * (1 - 0.40 * np.clip(line, 0, 1)[..., None]) * np.where(((h < 38) | (h > top - 32))[..., None], 1.07, 1.0)


def letters(Wf, u, h, seed):
    """The bronze letters of the one name, standing proud of the band over the beam: -> (letter, its lit rim, the
    little shadow it throws), each 0 to 1."""
    import letter
    from brush import sample
    cap = FRIEZE * 0.70
    scale = 2.0                                              # cm -> sheet pixels
    wide, _ = letter.roman_size(NAME, cap * scale, spacing=0.95)
    w, hh = int(wide) + 60, int(cap * scale) + 40
    words = letter.roman_mask((hh, w), NAME, (w / 2, hh / 2), cap * scale, anchor="mm", thick=0.16, thin=0.08, tilt=12, spacing=0.95, rough=0.0, hook=False)
    top = E1 + (FRIEZE - cap) / 2 + cap
    uu = (u - MID) * scale + w / 2
    vv = (top - h) * scale + 20
    look = lambda du, dv: sample(words, uu + du, vv + dv) * ((uu + du > 0) & (uu + du < w - 1) & (vv + dv > 0) & (vv + dv < hh - 1))
    m = look(0, 0)
    toward = look(2.2, -2.2)                                 # (toward the sun: right and up)
    return np.clip(m, 0, 1).astype(F32), np.clip(m - toward, 0, 1).astype(F32), np.clip(toward - m, 0, 1).astype(F32)


def temple(fine=2, seed=5):
    """The whole temple on a clear sheet at picture size -> Canvas."""
    global SOL
    SOL = solids()
    Tf = T.finer(fine)
    c = Canvas(Tf.shape)
    sun = (SU, SV, SH)

    # ---- the podium's left flank, in shade: big squared blocks, a plinth and a crown
    for Wf, m in Tf.face([(0, -RUN, 0), (0, BACK, 0), (0, BACK, HP), (0, -RUN, HP)]):
        v, h, ppc = Wf.on_side(0.0)
        own, _ = stone(v, h, ppc, PODIUM, seed + 1, long=150, high=62, spread=0.10, joint=2.2)
        own = mouldings(own, h, HP)
        moss = np.clip(1 - h / 80.0, 0, 1) * step(0.35, 0.75, tex(v, h, 120, seed + 31))
        own = own * (1 - moss[..., None] * np.array([0.26, 0.14, 0.30], dtype=F32))
        c.put(LIT.on(own, 0.0, 1.0, deep=0.04, bounce=0.65 * np.clip(1 - h / 400.0, 0, 1)), m, Wf)
    # ---- the cheek blocks either side of the steps: their fronts take the sun at a slant
    for (a0, a1) in ((0.0, CHEEK), (UW - CHEEK, UW)):
        for Wf, m in Tf.face([(a0, -RUN, 0), (a1, -RUN, 0), (a1, -RUN, HP), (a0, -RUN, HP)]):
            u, h, ppc = Wf.on_front(-RUN)
            own, _ = stone(u, h, ppc, PODIUM, seed + 2, long=130, high=62, spread=0.09, joint=2.0)
            own = mouldings(own, h, HP)
            cut = sunless(SOL, u, -RUN - 1, h, sun, spread=0.01)
            c.put(LIT.on(own, FR, cut, bounce=0.6 * np.clip(1 - h / 300.0, 0, 1)), m, Wf)
    # ---- the steps: a riser for each, and the treads we can look down on (those below our eye)
    for k in range(NSTEP, 0, -1):
        vk = VK(k)
        for Wf, m in Tf.face([(CHEEK, vk, (k - 1) * RISE), (UW - CHEEK, vk, (k - 1) * RISE), (UW - CHEEK, vk, k * RISE), (CHEEK, vk, k * RISE)], pad=1):
            u, h, ppc = Wf.on_front(vk)
            q = u / 160.0 + (k * 0.618) % 1 * 4
            joint = np.clip(1.5 - np.abs((q - np.floor(q)) - 0.5 - 0.47) * 160.0 / 2.0, 0, 1) * np.clip(ppc * 2.0 / 0.5, 0, 1)
            own = col(TRAV)[None, None, :] * (1 + (hash2(np.floor(q), k, 3)[..., None] - 0.5) * 0.10) * (1 + (tex(u, h + k * 40, 160, seed + 9)[..., None] - 0.5) * 0.12)
            own = own * (1 - 0.14 * joint[..., None])
            hb = h - (k - 1) * RISE
            own = own * (1 - 0.42 * np.clip(1 - hb / 5.0, 0, 1)[..., None])          # dark where it meets the tread below
            own = own * (1 + 0.10 * np.clip((hb - RISE + 3.0) / 3.0, 0, 1)[..., None])   # the worn nosing catches the light
            cut = sunless(SOL, u, vk - 0.5, h, sun, spread=0.02)
            c.put(LIT.on(own * 0.98, 0.42, cut, bounce=0.8), m, Wf)
        hk = k * RISE
        if k < NSTEP and hk < EYE - 4:
            for Wf, m in Tf.face([(CHEEK, vk, hk), (UW - CHEEK, vk, hk), (UW - CHEEK, VK(k + 1), hk), (CHEEK, VK(k + 1), hk)], pad=1):
                u, v, ppc = Wf.on_floor(hk)
                own = col(TRAV)[None, None, :] * (1 + (tex(u, v + k * 60, 140, seed + 11)[..., None] - 0.5) * 0.14)
                trodden = np.exp(-((u - UW / 2) / 700.0) ** 2)
                own = own * (1 + 0.08 * trodden[..., None])
                cut = sunless(SOL, u, v, hk, sun, spread=0.02)
                c.put(LIT.on(own, SH, cut, up=1, bounce=0.5), m, Wf)

    # ---- the porch: its ceiling (we look up into it), the cella's side wall down the left wing, the wall with the doors
    for Wf, m in Tf.face([(UE0, VE, E0), (UE1, VE, E0), (UE1, BACK - 60, E0), (UE0, BACK - 60, E0)]):
        u, v, ppc = Wf.on_floor(E0)
        beam = (np.abs(((u - COLS[0] + GAP / 2) % GAP) - GAP / 2) < 34) | (np.abs(((v - COLV + 300) % 600.0) - 300) < 34)
        cof = ((u - COLS[0]) % (GAP / 2)) - GAP / 4
        cv_ = ((v - COLV) % 300.0) - 150.0
        own = np.where(beam[..., None], col("#8a6a48"), col("#3f6170"))
        own = np.where(((np.abs(cof) > GAP / 4 - 22) | (np.abs(cv_) > 128))[..., None] & ~beam[..., None], col("#a84a34") * 0.9, own)
        own = np.where((np.hypot(cof, cv_) < 26)[..., None] & ~beam[..., None], col("#d8a040"), own)
        deep_ = 0.55 + 0.35 * np.clip((v - VE) / (DEEP - VE), 0, 1)
        c.put(LIT.on(own, 0.0, 1.0, deep=deep_, up=-1, bounce=0.8 * np.clip(1.2 - (v - VE) / 900.0, 0.15, 1.0)), m, Wf)
    for Wf, m in Tf.face([(CELLA[0], DEEP, HP), (CELLA[0], BACK - 120, HP), (CELLA[0], BACK - 120, E0), (CELLA[0], DEEP, E0)]):
        v, h, ppc = Wf.on_side(CELLA[0])
        own, _ = stone(v, h, ppc, "#d9c9a8", seed + 3, long=120, high=55, spread=0.06, joint=1.6)
        c.put(LIT.on(own, 0.0, 1.0, deep=0.72, bounce=0.25), m, Wf)
    for Wf, m in Tf.face([(CELLA[0], DEEP, HP), (CELLA[1], DEEP, HP), (CELLA[1], DEEP, E0), (CELLA[0], DEEP, E0)]):
        u, h, ppc = Wf.on_front(DEEP)
        own, _ = stone(u, h, ppc, "#dccbaa", seed + 4, long=120, high=55, spread=0.06, joint=1.6)
        dado = (h - HP) < 160
        own = np.where(dado[..., None], own * col("#a8604a") / col("#dccbaa") * 1.05, own)
        for (du, dw, dh) in DOORS:                           # the door cases
            case = (np.abs(u - du) < dw / 2 + 40) & (h < HP + dh + 40)
            own = np.where(case[..., None], col(TRAV) * (0.95 + 0.1 * tex(u, h, 50, seed + 33)[..., None]), own)
        c.put(LIT.on(own, 0.0, 1.0, deep=0.78, bounce=0.40 * np.clip(1.4 - (h - HP) / 500.0, 0.2, 1.0)), m, Wf)
    # the doors: the two side doors shut (bronze over wood, in panels); the middle one open on the dark room and the god
    for i, (du, dw, dh) in enumerate(DOORS):
        hole = [(du - dw / 2, DEEP, HP), (du + dw / 2, DEEP, HP), (du + dw / 2, DEEP, HP + dh), (du - dw / 2, DEEP, HP + dh)]
        for Wf, m in Tf.face(hole):
            u, h, ppc = Wf.on_front(DEEP)
            if i == 1:
                inside = ramp(np.clip((h - HP) / dh, 0, 1), [(0.0, "#2e2026"), (0.3, "#1e1520"), (1.0, "#120d16")])
                c.put(inside, m, Wf)
            else:
                a_ = np.abs(u - du)
                panel = (np.abs(((h - HP) % 140.0) - 70.0) < 52) & (a_ > 14) & (a_ < dw / 2 - 18)
                own = np.where(panel[..., None], col(BRONZE) * 0.9, col("#b08a48"))
                stud = (np.hypot(((u - du) % 40.0) - 20.0, ((h - HP) % 140.0) - 8.0) < 4.5)
                own = np.where(stud[..., None], col(GILT), own)
                own = np.where((a_ < 3)[..., None], col("#2a2018"), own)
                c.put(LIT.on(own, 0.0, 1.0, deep=0.7, bounce=0.5), m, Wf)
    god(Tf, c)

    # ---- the columns: the far rows and the flank first, in the porch's shade, then the front row
    for cv in reversed(FLANK_V):
        if cv > ROWS_V[-1]:
            column(Tf, c, COLS[0], cv, seed + 40 + int(cv) % 97, deep=0.45, shaded=True)
    for j, cv in enumerate(reversed(ROWS_V[1:])):
        for i, cu in enumerate(COLS):
            column(Tf, c, cu, cv, seed + 70 + i * 7 + j * 3, deep=0.62 - 0.10 * j, shaded=True)
    for i, cu in enumerate(COLS):
        column(Tf, c, cu, COLV, seed + 100 + i * 7, deep=0.0)

    # ---- the beam, the band with the name and the cornice: along the left flank (in shade), then across the front
    for Wf, m in Tf.face([(UE0, VE, E0), (UE0, BACK, E0), (UE0, BACK, E2), (UE0, VE, E2)]):
        v, h, ppc = Wf.on_side(UE0)
        own = col(STUC_SHADE)[None, None, :] * (0.94 + 0.10 * tex(v, h, 120, seed + 12)[..., None])
        fas = np.clip(1.5 - np.abs(h - E0 - 60) / 1.8, 0, 1) + np.clip(1.5 - np.abs(h - E1) / 2.2, 0, 1)
        own = own * (1 - 0.30 * np.clip(fas, 0, 1)[..., None])
        c.put(LIT.on(own, 0.0, 1.0, deep=0.08, bounce=0.3), m, Wf)
    for Wf, m in Tf.face([(UE0, VE, E0), (UE1, VE, E0), (UE1, VE, E2), (UE0, VE, E2)]):
        u, h, ppc = Wf.on_front(VE)
        own = col(STUC)[None, None, :] * (0.95 + 0.10 * tex(u, h, 160, seed + 13)[..., None])
        fas = np.clip(1.5 - np.abs(h - E0 - 60) / 1.8, 0, 1) + np.clip(1.5 - np.abs(h - E1) / 2.2, 0, 1) + np.clip(1.5 - np.abs(h - E1 - 6) / 1.4, 0, 1) * 0.5
        own = own * (1 - 0.32 * np.clip(fas, 0, 1)[..., None])
        rain = step(0.55, 0.85, tex(u * 6.0, h * 0.4, 160, seed + 14))
        own = own * (1 - 0.10 * rain[..., None])
        lm, ll, ls = letters(Wf, u, h, seed)
        own = own * (1 - 0.35 * ls[..., None])
        own = own * (1 - lm[..., None]) + col(BRONZE) * lm[..., None]
        cast_ = sunless(SOL, u, VE - 1, h, sun, spread=0.01, eps=6.0)
        lit = LIT.on(own, FR, cast_, bounce=0.5)
        glint = ll * (1 - cast_)
        lit = lit * (1 - 0.85 * glint[..., None]) + col(GILT_L) * 0.85 * glint[..., None]
        c.put(lit, m, Wf)
    for Wf, m in Tf.face([(UE0 - EAVE, VC, E2), (UE0 - EAVE, BACK, E2), (UE0 - EAVE, BACK, E3), (UE0 - EAVE, VC, E3)]):
        v, h, ppc = Wf.on_side(UE0 - EAVE)
        own = col(STUC_SHADE)[None, None, :] * (0.95 + 0.08 * tex(v, h, 90, seed + 15)[..., None])
        own = own * (1 - 0.35 * np.clip(1.5 - np.abs(h - E2 - 14) / 2.0, 0, 1)[..., None])
        c.put(LIT.on(own, 0.0, 1.0, deep=0.05, bounce=0.25), m, Wf)
    for Wf, m in Tf.face([(UE0 - EAVE, VC, E2), (UE1 + EAVE, VC, E2), (UE1 + EAVE, VC, E3), (UE0 - EAVE, VC, E3)]):
        u, h, ppc = Wf.on_front(VC)
        own = col(STUC)[None, None, :] * (0.97 + 0.08 * tex(u, h, 90, seed + 16)[..., None])
        dent = (np.abs((u % 26.0) - 13.0) < 6.5) & (h < E2 + 18)
        own = np.where(dent[..., None], own * 0.78, own)
        own = own * (1 - 0.35 * np.clip(1.5 - np.abs(h - E2 - 20) / 2.0, 0, 1)[..., None])
        c.put(LIT.on(own, FR, 0.0, bounce=0.3), m, Wf)

    # ---- the pediment: its field painted blue, crowded with figures; the raking cornices; the gilt edges of the roof
    for Wf, m in Tf.face([(UE0, PED_V, E3), (MID, PED_V, rake(MID)), (UE1, PED_V, E3)]):
        u, h, ppc = Wf.on_front(PED_V)
        own = col(FIELD)[None, None, :] * (0.92 + 0.16 * tex(u, h, 140, seed + 17)[..., None])
        fm, fc = pediment_figures(u, h, seed)
        own = np.where(fm[..., None] > 0.5, fc, own)
        under_rake = step(-64, -40, h - rake(u))
        c.put(LIT.on(own, FR, under_rake * 0.85, deep=0.15 * under_rake, bounce=0.35), m, Wf)
    for (a0, a1) in ((RK0, MID), (MID, RK1)):               # the raking cornices, gilt tiles along their tops
        for Wf, m in Tf.face([(a0, VC, rake(a0) - 6), (a1, VC, rake(a1) - 6), (a1, VC, rake(a1) + 58), (a0, VC, rake(a0) + 58)]):
            u, h, ppc = Wf.on_front(VC)
            hh = h - rake(u)
            own = np.where((hh > 30)[..., None], col(GILT), col(STUC))
            own = np.where(((hh > 26) & (hh < 31))[..., None], col(GILT_D), own)
            tiles = (np.abs((np.abs(u - MID) % 42.0) - 21.0) < 5.0) & (hh > 31)
            own = np.where(tiles[..., None], col(GILT_L), own)
            own = own * (1 - 0.3 * np.clip(1.5 - np.abs(hh - 12) / 2.0, 0, 1)[..., None])
            c.put(LIT.on(own, FR + 0.25, 0.0, bounce=0.2), m, Wf)
    roof_edges(Tf, c, seed)
    return c.reduced(fine)


def pediment_figures(u, h, seed):
    """Figures crowded in the pediment, in painted terracotta and stone: the god enthroned in the middle, gods and
    heroes either side, smaller and lying down toward the corners. -> (mask, colour)."""
    rng = np.random.default_rng(seed + 3)
    m = np.zeros(u.shape, F32)
    colour = np.zeros(u.shape + (3,), F32)
    half = MID - UE0
    figs = [(MID, 0.0, 1.0)]
    for side in (-1, 1):
        for j in range(1, 9):
            figs.append((MID + side * j * half / 9.0, side, 1.0 - j / 9.0))
    for (fu, side, t) in figs:
        room = float(rake(np.array(fu))) - E3 - 34
        if room < 30:
            continue
        hgt = room * (0.90 if t > 0.3 else 0.8)
        if t < 0.3:                                          # in the corners they lie along the floor of the field
            body = (np.abs(u - fu) < hgt * 1.3) & (h > E3 + 6) & (h < E3 + 6 + hgt * 0.5 - np.abs(u - fu) * 0.18)
            head = np.hypot(u - (fu - side * hgt * 1.2), h - (E3 + 6 + hgt * 0.5)) < hgt * 0.24
            shape_ = body | head
        else:
            w = hgt * 0.22
            lean = side * hgt * 0.08
            rel = (h - E3) / hgt
            body = (np.abs(u - fu - lean * rel) < w * (1.0 - 0.35 * rel)) & (h > E3 + 6) & (h < E3 + hgt * 0.84)
            head = np.hypot(u - fu - lean, h - (E3 + hgt * 0.91)) < hgt * 0.095
            arm = (np.abs((h - E3 - hgt * 0.62) + side * (u - fu) * 0.6) < hgt * 0.05) & (np.abs(u - fu - side * hgt * 0.22) < hgt * 0.24)
            shape_ = body | head | arm
            if t == 1.0:                                     # the god in the middle, enthroned
                shape_ = shape_ | ((np.abs(u - fu) < hgt * 0.34) & (h > E3 + 6) & (h < E3 + hgt * 0.40))
        tone = col(["#d9a070", "#ecdcbc", "#c46a48", "#f2e6c8", "#b8784c", "#e2b878"][int(rng.integers(6))])
        m = np.where(shape_, 1.0, m)
        colour = np.where(shape_[..., None], tone * (0.92 + 0.12 * tex(u, h, 30, seed + int(fu))[..., None]), colour)
    return m, colour


def roof_edges(Tf, c, seed):
    """The gilt bronze of the roof where it shows from below: antefixes standing along the left eaves, the corner
    ornaments, and a crest on the peak for the chariot to stand on."""
    s = Sheet(Tf.shape, ss=2)
    f = Tf.fine
    P2 = lambda u, v, h: tuple(q * f for q in T.pt(u, v, h))
    for v in np.arange(VC + 40, BACK, 62.0):               # antefixes on the left eaves: a row of little gilt palmettes
        a, b = P2(UE0 - EAVE, v, E3), P2(UE0 - EAVE, v, E3 + 44)
        w = max(1.0, (a[1] - b[1]) * 0.42)
        s.poly([(a[0] - w * 0.5, a[1]), (a[0] + w * 0.5, a[1]), (b[0] + w * 0.6, b[1] + w * 0.4), (b[0], b[1]), (b[0] - w * 0.6, b[1] + w * 0.4)], GILT_D)
        s.poly([(a[0] - w * 0.25, a[1]), (a[0] + w * 0.35, a[1]), (b[0] + w * 0.3, b[1] + w * 0.5), (b[0], b[1] + w * 0.1)], "#b88a38")
    for (u, h) in ((RK0, rake(RK0) + 50), (RK1, rake(RK1) + 50)):     # corner ornaments: a gilt palmette on a scroll
        a = P2(u, VC, h)
        k = Tf.k(u, VC) * f
        s.poly([(a[0] - 38 * k, a[1]), (a[0] + 38 * k, a[1]), (a[0] + 46 * k, a[1] - 70 * k), (a[0], a[1] - 128 * k), (a[0] - 46 * k, a[1] - 70 * k)], GILT_D)
        s.poly([(a[0] - 26 * k, a[1] - 4 * k), (a[0] + 30 * k, a[1] - 4 * k), (a[0] + 34 * k, a[1] - 66 * k), (a[0] + 2 * k, a[1] - 116 * k), (a[0] - 30 * k, a[1] - 66 * k)], GILT)
        s.line([(a[0] + 4 * k, a[1] - 10 * k), (a[0] + 28 * k, a[1] - 62 * k)], GILT_L, max(1.0, 6 * k))
    a = P2(MID, VC, PEAK)                                    # the peak: a gilt crest, and the chariot of four horses on it
    k = Tf.k(MID, VC) * f
    s.poly([(a[0] - 120 * k, a[1] + 6 * k), (a[0] + 120 * k, a[1] + 6 * k), (a[0] + 100 * k, a[1] - 26 * k), (a[0] - 100 * k, a[1] - 26 * k)], GILT_D)
    s.line([(a[0] - 100 * k, a[1] - 24 * k), (a[0] + 100 * k, a[1] - 24 * k)], GILT_L, max(1.0, 5 * k))
    quadriga(s, a[0], a[1] - 26 * k, k)
    cc, ca = s.done()
    c.put(cc, ca)


def god(Tf, c):
    """Far inside the open middle door, the great seated god in gold and ivory, small and dim in the dark room."""
    f = Tf.fine
    du, dw, dh = DOORS[1]
    vg = DEEP + 2400.0
    s = Sheet(Tf.shape, ss=2)
    P2 = lambda u, h: tuple(q * f for q in T.pt(u, vg, h))
    k = Tf.k(du, vg) * f
    b0 = P2(du, HP)
    base_top = P2(du, HP + 190)[1]
    s.poly([(b0[0] - 230 * k, b0[1]), (b0[0] + 230 * k, b0[1]), (b0[0] + 230 * k, base_top), (b0[0] - 230 * k, base_top)], "#3a2c26")
    seat = P2(du, HP + 190 + 230)[1]
    s.poly([(b0[0] - 170 * k, base_top), (b0[0] + 170 * k, base_top), (b0[0] + 170 * k, seat - 260 * k), (b0[0] - 170 * k, seat - 260 * k)], "#4a3624")    # the throne
    s.poly([(b0[0] - 120 * k, base_top), (b0[0] + 120 * k, base_top), (b0[0] + 95 * k, seat), (b0[0] - 95 * k, seat)], "#7a5a2a")                            # the lap and legs, in gold
    s.poly([(b0[0] - 70 * k, seat), (b0[0] + 75 * k, seat), (b0[0] + 62 * k, seat - 230 * k), (b0[0] - 58 * k, seat - 230 * k)], "#8a7a62")                  # the body, ivory
    s.ellipse(b0[0] + 4 * k, seat - 262 * k, 38 * k, 44 * k, "#9a8a70")                                                                                      # the head
    s.ellipse(b0[0] + 4 * k, seat - 296 * k, 44 * k, 16 * k, "#8a6a2a")                                                                                      # a wreath
    s.line([(b0[0] + 120 * k, base_top), (b0[0] + 128 * k, seat - 380 * k)], "#a07a30", max(1.0, 14 * k))                                                     # the sceptre
    s.line([(b0[0] + 60 * k, seat - 160 * k), (b0[0] + 122 * k, seat - 200 * k)], "#7a6a52", max(1.0, 24 * k))                                               # the arm that holds it
    s.ellipse(b0[0] - 60 * k, seat - 40 * k, 30 * k, 14 * k, "#c09a48", 0.8)                                                                                 # a gleam on the gold
    s.line([(b0[0] + 18 * k, seat - 220 * k), (b0[0] + 40 * k, seat - 60 * k)], "#b8a882", max(1.0, 8 * k), 0.7)                                             # and on the ivory
    cc, ca = s.done()
    door = Tf.mask(T.pts([(du - dw / 2, DEEP, HP), (du + dw / 2, DEEP, HP), (du + dw / 2, DEEP, HP + dh), (du - dw / 2, DEEP, HP + dh)]))
    c.put(cc * 0.62 + np.array([0.04, 0.03, 0.04], F32), ca * door * 0.92)


def quadriga(sheet, x, y, k, tones=(GILT_D, "#b8842e", GILT, GILT_L)):
    """The bronze chariot of four horses on the peak, seen from the front: four horses abreast, each with a foreleg
    pawing the air and the outer two turning their heads outward, the car behind them, and the god standing in it.
    (x, y) is the middle of its foot on the peak; k is pixels per cm. Lit from our right."""
    dark, mid_, lit, shine = tones
    q = lambda dx, h: (x + dx * k, y - h * k)
    # the car behind the horses, and the god standing in it
    sheet.poly([q(-75, 70), q(75, 70), q(70, 150), q(-70, 150)], dark)
    sheet.poly([q(10, 70), q(75, 70), q(70, 150), q(14, 150)], mid_)
    sheet.poly([q(-24, 140), q(26, 140), q(20, 268), q(-18, 268)], mid_)                       # his body, in a cloak
    sheet.poly([q(4, 140), q(26, 140), q(20, 268), q(6, 268)], lit)
    sheet.ellipse(*q(1, 285), 17 * k, 19 * k, mid_)                                             # his head
    sheet.ellipse(*q(6, 287), 9 * k, 13 * k, lit)
    sheet.line([q(18, 240), q(48, 286)], mid_, max(1.0, 9 * k))                                # his raised arm,
    sheet.line([q(50, 200), q(46, 330)], shine, max(1.0, 6 * k))                               # and the sceptre in it
    sheet.line([q(-16, 236), q(-40, 196)], dark, max(1.0, 9 * k))                              # the other hand on the reins
    for i, off in enumerate((-132, -46, 46, 132)):
        turn = (-1 if off < -100 else 1 if off > 100 else 0)                                   # the outer two turn their heads out
        tone, side = (dark, mid_) if off < 0 else (mid_, lit)
        hx = lambda dx: off + dx
        sheet.line([q(hx(12), 0), q(hx(12), 90)], tone, max(1.0, 10 * k))                      # a foreleg planted
        sheet.line([q(hx(-12), 92), q(hx(-22), 58), q(hx(-8), 40)], tone, max(1.0, 10 * k))     # and one pawing the air
        sheet.ellipse(*q(hx(0), 122), 30 * k, 38 * k, tone)                                    # the chest
        sheet.ellipse(*q(hx(9), 126), 15 * k, 30 * k, side)                                    # its lit side
        neck = [q(hx(-16), 140), q(hx(16), 140), q(hx(14 + turn * 12), 200), q(hx(-12 + turn * 12), 204)]
        sheet.poly(neck, tone)
        sheet.line([q(hx(8 + turn * 6), 146), q(hx(10 + turn * 12), 198)], side, max(1.0, 7 * k))
        sheet.line([q(hx(-14 + turn * 10), 150), q(hx(-10 + turn * 14), 212)], dark, max(1.0, 6 * k))   # the mane
        hd = [q(hx(-12 + turn * 16), 212), q(hx(14 + turn * 16), 214), q(hx(10 + turn * 26), 168), q(hx(-6 + turn * 26), 166)]
        sheet.poly(hd, tone)                                                                   # the head, nose down and toward us
        sheet.line([q(hx(6 + turn * 18), 208), q(hx(8 + turn * 26), 172)], side, max(1.0, 5 * k))
        sheet.poly([q(hx(-10 + turn * 14), 210), q(hx(-14 + turn * 14), 232), q(hx(-3 + turn * 14), 212)], tone)    # ears
        sheet.poly([q(hx(6 + turn * 16), 212), q(hx(8 + turn * 16), 234), q(hx(14 + turn * 16), 212)], tone)
    sheet.line([q(-170, 2), q(170, 2)], shine, max(1.0, 4 * k))

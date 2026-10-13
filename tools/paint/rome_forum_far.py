"""The far half of the Forum picture (rome_forum.py): the Capitol and its three buildings, the far end of the square
(the temple of Saturn, the new speakers' platform, the older temple behind it), the two basilicas down the sides, the
mouth of the Tuscan street, and what is seen of the senate house's site over its hoarding.

Each function paints on a clear Canvas, crisply, and returns it: rome_forum.py lays them in softly under the brushwork
and states them again, crisply, over it (as rome_steps.py does with its Forum)."""

import math

import numpy as np

from rome_forum_kit import *

# ---------------------------------------------------------------- the temple of Saturn, as rome_steps.py measures it
S_HP, S_RISE, S_TREAD, S_NSTEP, S_EDGE, S_GAP = 252.0, 18.0, 38.0, 14, -60.0, 255.0
S_COLS = [70.0 + S_GAP * i for i in range(6)]
S_UW = S_COLS[-1] + 70.0
S_SU0, S_SU1 = 90.0, S_UW - 90.0
S_HC, S_DEEP, S_BACK = 610.0, 520.0, 1900.0
S_DOOR = (S_UW / 2 - 95.0, S_UW / 2 + 95.0, S_HP + 8.0, S_HP + 478.0)
S_ARCH, S_FRIEZE, S_CORN, S_EAVE = 66.0, 56.0, 28.0, 30.0
S_PITCH = math.tan(math.radians(17))
S_E0 = S_HP + S_HC
S_E1, S_E2 = S_E0 + S_ARCH, S_E0 + S_ARCH + S_FRIEZE
S_E3 = S_E2 + S_CORN


def S_VK(k):
    return S_EDGE - (S_NSTEP - k) * S_TREAD


def saturn_frame(fine=1):
    return frame(SATURN["angle"], SATURN["x"], SATURN["D"], fine)


def saturn_foot():
    """The middle of the foot of the temple of Saturn's steps, on the picture, and where on the ground it is."""
    sf = saturn_frame()
    a = sf.pt(S_SU0 + 120, S_VK(1) - 40, 0)
    return a


# ---------------------------------------------------------------- the Capitol
CREST = [(-12, 132), (30, 122), (70, 114), (112, 110), (200, 108), (300, 109), (338, 113), (370, 119), (420, 123), (480, 123), (520, 120),
         (546, 113), (590, 108), (660, 108), (705, 114), (742, 126), (780, 138), (812, 146)]


def crest_at(x):
    xs = [p[0] for p in CREST]
    ys = [p[1] for p in CREST]
    return float(np.interp(x, xs, ys))


def capitol(seed=31):
    """The hill above everything: its face of tufa, green slopes and gardens, terrace walls and houses, the road that
    climbs it, and on top the temple of Jupiter (left), Juno's temple where the money is made (right), and the record
    office's arcades on the slope between. All in the morning sun, which comes from behind us, pale with the air. -> Canvas."""
    rng = np.random.default_rng(seed)
    D = HILL_D
    c = Canvas(SHAPE)
    s = Sheet2(SHAPE)
    lit_c, half, shade, dark = "#fbe9c2", "#e8d2a8", "#a9a6c8", "#7c7aa0"
    hill_top = curve(CREST, 6)
    x, y = grid(SHAPE)
    # the face of the hill: a wash of sunlit green-gold, cooler in its folds, warmer where the tufa shows
    face = far("#a9a774", D, 0.5)
    s.poly(hill_top + [(812, 300), (-12, 300)], face)
    for (x0, x1, a) in ((-12, 100, 0.30), (350, 430, 0.30), (520, 560, 0.25), (700, 812, 0.35)):
        s.poly([(x0, crest_at(x0) + 5), (x1, crest_at(x1) + 6), (x1 + 30, 300), (x0 - 10, 300)], far("#8f96a8", D, 0.55), a)
    # tufa cliffs under the summits: pale ochre, crisp edges catching the sun, cracks running down
    for (x0, x1, top, depth) in ((104, 344, 2, 26), (544, 712, 2, 24), (30, 104, 4, 18)):
        pts = [(x0, crest_at(x0) + top)]
        for xx in np.linspace(x0, x1, 14)[1:]:
            pts.append((xx, crest_at(xx) + top + rng.uniform(-0.6, 1.2)))
        bottom = [(xx, crest_at(xx) + top + depth * rng.uniform(0.6, 1.1)) for xx in np.linspace(x1, x0, 12)]
        s.poly(pts + bottom, far("#dcc596", D, 0.45))
        s.poly(pts + [(xx, yy + 5) for xx, yy in reversed(pts)], far("#f2deae", D, 0.42), 0.8)
        for xx in np.linspace(x0 + 6, x1 - 6, int((x1 - x0) / 8)):
            y0 = crest_at(xx) + top + 3
            s.line([(xx, y0), (xx + rng.uniform(-1.5, 1.5), y0 + depth * rng.uniform(0.4, 0.9))], far("#a08e86", D, 0.5), 0.8, 0.55)
        s.line(pts, far("#fff4d8", D, 0.4), 1.0, 0.85)
    # gardens and trees on the slopes: umbrella pines, cypresses, laurels, figs just in leaf
    def pine(px, py, hgt):
        s.line([(px, py), (px + hgt * 0.05, py - hgt * 0.55), (px - hgt * 0.02, py - hgt)], far("#6a5648", D, 0.45), max(0.9, hgt * 0.05))
        for (dx, dy, rx, ry, tone) in ((-0.22, -1.02, 0.34, 0.15, "#3f5c3e"), (0.20, -1.06, 0.36, 0.16, "#4c6c46"), (0.0, -1.12, 0.30, 0.13, "#62824e"), (-0.1, -1.17, 0.2, 0.08, "#8aa45e")):
            s.ellipse(px + dx * hgt, py + dy * hgt, rx * hgt, ry * hgt, far(tone, D, 0.42))

    def cypress(px, py, hgt):
        s.poly([(px - hgt * 0.10, py), (px - hgt * 0.13, py - hgt * 0.45), (px, py - hgt), (px + hgt * 0.13, py - hgt * 0.45), (px + hgt * 0.10, py)], far("#34503a", D, 0.42))
        s.poly([(px - hgt * 0.10, py), (px - hgt * 0.13, py - hgt * 0.45), (px, py - hgt), (px - hgt * 0.02, py - hgt * 0.5), (px + hgt * 0.02, py)], far("#5f8450", D, 0.4))

    for i in range(110):                                     # bushes and small trees all over the face, thicker low down
        px = rng.uniform(-10, 810)
        py = crest_at(px) + 10 + (rng.random() ** 0.7) * (250 - crest_at(px))
        r = rng.uniform(2.0, 5.5) * (0.7 + 0.5 * (py - 110) / 140)
        tone = far(mix("#4f6c3e", "#7f9450", rng.random()), D, 0.45)
        s.ellipse(px, py, r * 1.3, r * 0.8, tone, 0.95)
        s.ellipse(px - r * 0.35, py - r * 0.25, r * 0.8, r * 0.45, far("#a8b86a", D, 0.42), 0.75)
        s.ellipse(px + r * 0.3, py + r * 0.35, r * 0.9, r * 0.4, far("#3c5444", D, 0.45), 0.65)
    for i in range(30):                                      # houses on the slopes: pale walls, red roofs, the shade side violet
        px = rng.uniform(0, 790)
        if 105 < px < 335 or 540 < px < 650:
            continue
        py = rng.uniform(crest_at(px) + 22, 240)
        w, hgt = rng.uniform(7, 15), rng.uniform(5, 9)
        s.poly([(px, py), (px + w, py), (px + w, py - hgt), (px, py - hgt)], far(mix(lit_c, half, rng.random()), D, 0.55))
        s.poly([(px + w * 0.72, py), (px + w, py), (px + w, py - hgt), (px + w * 0.72, py - hgt)], far(shade, D, 0.55), 0.8)
        s.poly([(px - 1, py - hgt), (px + w + 1, py - hgt), (px + w * 0.45, py - hgt - 2.8)], far("#d47a50", D, 0.5))
        for j in range(int(w // 5)):
            s.line([(px + 2 + j * 5, py - hgt * 0.62), (px + 2 + j * 5, py - hgt * 0.32)], far("#5a4a66", D, 0.55), 0.9, 0.8)
    for (x0, x1, y0, n) in ((14, 96, 152, 6), (640, 742, 152, 8), (120, 220, 190, 8), (440, 530, 200, 7)):      # terrace walls with blind arches
        s.poly([(x0, y0), (x1, y0 + 1), (x1, y0 + 12), (x0, y0 + 11)], far(half, D, 0.55))
        s.line([(x0, y0), (x1, y0 + 1)], far("#fff4d8", D, 0.45), 1.0)
        for j in range(n):
            ax = lerp(x0 + 4, x1 - 4, j / max(1, n - 1))
            s.poly([(ax - 2.0, y0 + 11), (ax - 2.0, y0 + 5), (ax, y0 + 3.5), (ax + 2.0, y0 + 5), (ax + 2.0, y0 + 11)], far(shade, D, 0.5), 0.9)
    # the road up the hill: it leaves the far end by the temple of Saturn and climbs in zigzags to the precinct's gate
    road = [(300, 226), (250, 212), (296, 196), (256, 180), (300, 164), (262, 150), (294, 136), (282, 126)]
    s.line(road, far("#d8bd90", D, 0.5), 3.2)
    s.line([(xx, yy + 2.2) for xx, yy in road], far("#8f86a8", D, 0.5), 1.3, 0.8)
    s.line([(xx, yy - 1.6) for xx, yy in road], far("#fff0d0", D, 0.45), 0.9, 0.8)
    for (px, py, hgt) in ((40, 136, 22), (64, 124, 18), (352, 126, 19), (380, 132, 16), (516, 128, 18), (712, 126, 21), (748, 136, 17), (92, 118, 14), (430, 128, 15)):
        pine(px, py, hgt)
    for (px, py, hgt) in ((96, 146, 17), (104, 148, 13), (340, 138, 15), (532, 134, 16), (540, 138, 12), (694, 136, 16), (24, 154, 15), (458, 136, 13), (470, 138, 11)):
        cypress(px, py, hgt)
    sc, sa = s.done()
    c.put(sc, sa)
    tabularium(c, rng)
    jupiter(c)
    moneta(c)
    return c


def tabularium(c, rng):
    """The record office: a long front of round arches between half-columns, on the slope between the summits, over a
    tall plain wall of squared stone with small windows; a gallery above. Warm grey-ochre stone in the sun; the arches
    deep in shade. (Nothing is written on it.)"""
    t = TABULARIUM
    s = Sheet2(SHAPE)
    D = t["D"]
    P = lambda x, h: pt(x, h, D)
    stone_c = far("#dcc49a", D, 0.42)
    shade_c, deep_c = far("#9c94bc", D, 0.42), far("#4e4a74", D, 0.40)
    s.poly([P(t["x0"], 200), P(t["x1"], 200), P(t["x1"], t["h0"]), P(t["x0"], t["h0"])], far("#cfb78c", D, 0.45))      # the plain wall below
    for hh in np.arange(260, t["h0"], 64):
        s.line([P(t["x0"], hh), P(t["x1"], hh)], far("#a8967c", D, 0.45), 0.7, 0.45)
    for j in range(16):                                      # its small windows
        xa = lerp(t["x0"] + 200, t["x1"] - 200, j / 15)
        a0, a1 = P(xa - 40, t["h0"] - 330), P(xa + 40, t["h0"] - 230)
        s.poly([a0, (a1[0], a0[1]), a1, (a0[0], a1[1])], deep_c, 0.8)
    s.poly([P(t["x0"], t["h0"]), P(t["x1"], t["h0"]), P(t["x1"], t["h1"]), P(t["x0"], t["h1"])], stone_c)           # the arcade
    n = 9
    bay = (t["x1"] - t["x0"]) / n
    for j in range(n):
        xa = t["x0"] + bay * j
        a0, a1 = P(xa + bay * 0.20, t["h0"] + 60), P(xa + bay * 0.80, t["h0"] + 60)
        top = P(xa + bay * 0.5, t["h1"] - 160)
        r = (a1[0] - a0[0]) / 2
        arch = [a0, (a0[0], top[1] + r)] + [(top[0] + r * math.cos(q), top[1] + r - r * math.sin(q)) for q in np.linspace(math.pi, 0, 11)] + [(a1[0], top[1] + r), a1]
        s.poly(arch, deep_c)
        s.poly([(a1[0] - r * 0.45, a1[1]), (a1[0], a1[1]), (a1[0], top[1] + r), (a1[0] - r * 0.45, top[1] + r * 1.2)], far("#7c76a0", D, 0.4), 0.7)   # light inside, on the far pier
        hc0, hc1 = P(xa, t["h0"]), P(xa, t["h1"] - 80)                                                                # a half-column, lit on its left
        s.line([hc0, hc1], far("#fff2d2", D, 0.4), 2.0, 0.95)
        s.line([(hc0[0] + 1.3, hc0[1]), (hc1[0] + 1.3, hc1[1])], shade_c, 0.9, 0.8)
    s.line([P(t["x0"], t["h1"] - 80), P(t["x1"], t["h1"] - 80)], far("#fff2d2", D, 0.4), 1.2)
    s.line([P(t["x0"], t["h1"] - 60), P(t["x1"], t["h1"] - 60)], shade_c, 0.9, 0.8)
    s.poly([P(t["x0"], t["h1"]), P(t["x1"], t["h1"]), P(t["x1"], t["h2"]), P(t["x0"], t["h2"])], far("#e6d0a2", D, 0.42))    # the gallery above
    for j in range(24):
        xa = lerp(t["x0"] + 80, t["x1"] - 80, j / 23)
        s.line([P(xa, t["h1"] + 40), P(xa, t["h2"] - 50)], deep_c, 1.4, 0.8)
    s.poly([P(t["x0"] - 60, t["h2"]), P(t["x1"] + 60, t["h2"]), P(t["x1"] + 30, t["h2"] + 100), P(t["x0"] - 30, t["h2"] + 100)], far("#d07e58", D, 0.42))
    sc, sa = s.done()
    c.put(sc, sa)


def jupiter(c):
    """The temple of Jupiter Best and Greatest on the left summit, seen from far below and to the east: its front (which
    faces south) at its left end, turned a little toward us, with its deep porch of three rows of columns and its gable;
    its long side toward us; a very high base, plain Doric columns, white, the shade between them deep; the roof of gilt
    bronze, of which we see from down here only its edge and the bright sliver of its near slope, blazing in the sun; a
    bronze chariot of four horses on the peak over the front."""
    J = JUPITER
    jf = frame(J["angle"], J["x"], J["D"])
    D = J["D"]
    s, g = Sheet2(SHAPE), Sheet2(SHAPE)
    h0 = J["base"]
    hp = h0 + J["podium"]
    hc = hp + J["cols"]
    he = hc + 320
    W_, L_ = J["width"], J["length"]
    P = jf.pt
    most = 0.42
    lit_c, front_c = far("#fbf1da", D, most), far("#efe0c2", D, most)
    shade_c, deep_c = far("#a49cc4", D, most), far("#5e5a8a", D, most)
    stone_lit, stone_front = far("#ead6aa", D, most), far("#dcc69c", D, most)
    # the podium: the long side (u = W_, facing us) and the front end (v = 0, facing left and a little toward us)
    s.poly([P(0, 0, h0), P(W_, 0, h0), P(W_, 0, hp), P(0, 0, hp)], stone_front)
    s.poly([P(W_, 0, h0), P(W_, L_, h0), P(W_, L_, hp), P(W_, 0, hp)], stone_lit)
    for hh, tone, wd in ((hp - 40, "#fff4dc", 1.0), (hp - 60, "#9a8fb4", 0.8), (h0 + 70, "#9a8fb4", 0.8)):
        s.line([P(W_, 0, hh), P(W_, L_, hh)], far(tone, D, most), wd, 0.8)
        s.line([P(0, 0, hh), P(W_, 0, hh)], far(tone, D, most), wd, 0.7)
    # the steps up the front: a broad flight between the podium's wings, pale in the light
    s.poly([P(900, -900, h0), P(W_ - 900, -900, h0), P(W_ - 900, 0, hp), P(900, 0, hp)], far("#fff6e2", D, most))
    for q in np.linspace(0.1, 0.9, 7):
        s.line([P(900, -900 * (1 - q), h0 + J["podium"] * q), P(W_ - 900, -900 * (1 - q), h0 + J["podium"] * q)], far("#cfc0b0", D, most), 0.6, 0.6)
    # behind the columns: the porch and the cella's long wall, in deep shade
    s.poly([P(0, 160, hp), P(W_ - 170, 160, hp), P(W_ - 170, 160, he), P(0, 160, he)], deep_c)
    s.poly([P(W_ - 170, 160, hp), P(W_ - 170, L_ - 120, hp), P(W_ - 170, L_ - 120, he), P(W_ - 170, 160, he)], far("#7a73a2", D, most))
    # the columns: along the long side, and three rows across the front (the farther rows dimmer)
    kk = k(D)
    for row in (2, 1):
        for j in range(6):
            u = lerp(300, W_ - 300, j / 5)
            a0, a1 = P(u, 140 + row * 560, hp), P(u, 140 + row * 560, hc)
            g.line([a0, a1], far("#cfc4dc", D, most), max(1.0, 150 * kk), 0.75)
    n_side = 10
    for j in range(n_side):
        v = lerp(140, L_ - 240, j / (n_side - 1))
        a0, a1 = P(W_ - 120, v, hp), P(W_ - 120, v, hc)
        g.line([a0, a1], lit_c, max(1.3, 170 * kk))
        g.line([(a0[0] + 1.1, a0[1]), (a1[0] + 1.1, a1[1])], shade_c, 0.8, 0.85)
        g.line([(a1[0] - 1.6, a1[1]), (a1[0] + 1.6, a1[1])], lit_c, 1.0)                    # the plain Doric capital
    for j in range(6):
        u = lerp(300, W_ - 300, j / 5)
        a0, a1 = P(u, 120, hp), P(u, 120, hc)
        g.line([a0, a1], front_c, max(1.1, 160 * kk))
        g.line([(a0[0] + 0.9, a0[1]), (a1[0] + 0.9, a1[1])], shade_c, 0.7, 0.8)
    # the entablature: the beam, a painted band, the cornice
    g.poly([P(0, 0, hc), P(W_, 0, hc), P(W_, 0, he), P(0, 0, he)], front_c)
    g.poly([P(W_, 0, hc), P(W_, L_, hc), P(W_, L_, he), P(W_, 0, he)], lit_c)
    for hh, tone, wd in ((hc + 130, "#c0563e", 1.0), (hc + 200, "#3f6a96", 0.8), (he - 30, "#fff4d8", 1.0)):
        g.line([P(W_, 0, hh), P(W_, L_, hh)], far(tone, D, most * 0.8), wd, 0.85)
        g.line([P(0, 0, hh), P(W_, 0, hh)], far(tone, D, most * 0.8), wd, 0.75)
    # the roof of gilt bronze: from down here its near slope is a bright sliver over the eaves, the ridge above it
    pitch = 0.30
    ridge = he + W_ / 2 * pitch
    g.poly([P(W_ + 60, -60, he), P(W_ + 60, L_ + 60, he), P(W_ / 2, L_ + 60, ridge), P(W_ / 2, -60, ridge)], "#f2b840")
    for q in np.linspace(0.04, 0.96, 18):                                    # the joints of the plates, catching the light by turns
        g.line([P(W_ + 60, L_ * q, he), P(W_ / 2, L_ * q, ridge)], "#ffe9a0" if int(q * 18) % 3 == 0 else "#c8862a", 0.7, 0.7)
    g.line([P(W_ + 60, -60, he), P(W_ + 60, L_ + 60, he)], "#fff6d0", 1.4)    # the eaves, blazing
    g.line([P(W_ / 2, -60, ridge), P(W_ / 2, L_ + 60, ridge)], "#ffe28a", 1.2)
    # the front's gable, seen aslant at the left end: the pediment, its raking cornices of gilt bronze
    g.poly([P(-60, -60, he), P(W_ / 2, -60, ridge), P(W_ + 60, -60, he)], far("#e8d4b2", D, most))
    g.line([P(-60, -60, he), P(W_ / 2, -60, ridge), P(W_ + 60, -60, he)], "#f6c450", 1.2)
    # the chariot on the peak over the front: four horses and a driver, bronze, gilded, catching the light
    qx, qy = P(W_ / 2, -60, ridge)
    q4 = max(1.0, 26 * kk)
    for i in range(4):
        hx = qx - 2.2 * q4 + i * 1.5 * q4
        g.line([(hx, qy), (hx + 0.2 * q4, qy - 3.4 * q4)], "#6a4a22", max(0.8, 0.7 * q4))
    g.poly([(qx - 3.2 * q4, qy - 2.8 * q4), (qx + 4.0 * q4, qy - 3.4 * q4), (qx + 5.0 * q4, qy - 5.6 * q4), (qx + 3.2 * q4, qy - 6.8 * q4), (qx - 2.4 * q4, qy - 5.4 * q4)], "#8a6630")
    g.line([(qx + 4.2 * q4, qy - 6.0 * q4), (qx + 6.0 * q4, qy - 8.4 * q4)], "#8a6630", max(1.0, 1.1 * q4))
    g.line([(qx - 2.0 * q4, qy - 4.8 * q4), (qx - 2.4 * q4, qy - 9.4 * q4)], "#6a4a22", max(0.9, 1.0 * q4))
    g.ellipse(qx - 2.4 * q4, qy - 10.0 * q4, 0.9 * q4, 0.9 * q4, "#6a4a22")
    g.line([(qx - 3.0 * q4, qy - 3.8 * q4), (qx + 4.6 * q4, qy - 6.4 * q4)], "#ffe08a", max(0.7, 0.6 * q4), 0.95)
    # the altar before the temple, where the Ides offering has been made (its smoke is the engine's)
    ax, ay = P(W_ * 0.5, -1300, h0)
    s.poly([(ax - 3.0, ay), (ax + 3.0, ay), (ax + 3.0, ay - 3.4), (ax - 3.0, ay - 3.4)], far("#fff2d8", D, most))
    s.line([(ax - 3.0, ay - 3.4), (ax + 3.0, ay - 3.4)], far("#ffffff", D, most), 0.8)
    for sh in (s, g):
        sc, sa = sh.done()
        c.put(sc, sa)


def moneta(c):
    """Juno's temple on the other summit, where the money is struck: smaller and plainer, its front toward us."""
    m = MONETA
    mf = frame(m["angle"], m["x"], m["D"])
    D = m["D"]
    s = Sheet2(SHAPE)
    h0 = m["base"]
    hp = h0 + m["podium"]
    hc = hp + m["cols"]
    W_ = m["width"]
    P = mf.pt
    lit_c, shade_c, deep_c = far("#f7e8c8", D, 0.5), far("#aaa4c8", D, 0.5), far("#77729c", D, 0.5)
    s.poly([P(0, 0, h0), P(0, 1800, h0), P(0, 1800, hp), P(0, 0, hp)], shade_c)                    # the left side
    s.poly([P(0, 0, h0), P(W_, 0, h0), P(W_, 0, hp), P(0, 0, hp)], lit_c)
    s.poly([P(300, -300, h0), P(W_ - 300, -300, h0), P(W_ - 300, 0, hp), P(300, 0, hp)], far("#fff4dc", D, 0.5))
    s.poly([P(60, 120, hp), P(W_ - 60, 120, hp), P(W_ - 60, 120, hc), P(60, 120, hc)], deep_c)
    s.poly([P(0, 0, hp), P(0, 1800, hp), P(0, 1800, hc), P(0, 0, hc)], shade_c)
    for j in range(6):
        u = lerp(110, W_ - 110, j / 5)
        a0, a1 = P(u, 0, hp), P(u, 0, hc)
        s.line([a0, a1], lit_c, max(1.1, 110 * k(D)))
        s.line([(a0[0] + 0.9, a0[1]), (a1[0] + 0.9, a1[1])], shade_c, 0.7, 0.7)
    s.poly([P(-20, 0, hc), P(W_ + 20, 0, hc), P(W_ + 20, 0, hc + 160), P(-20, 0, hc + 160)], lit_c)
    apex = hc + 160 + W_ / 2 * 0.32
    s.poly([P(-30, 0, hc + 160), P(W_ / 2, 0, apex), P(W_ + 30, 0, hc + 160)], far("#ead7b6", D, 0.5))
    s.line([P(-30, 0, hc + 160), P(W_ / 2, 0, apex), P(W_ + 30, 0, hc + 160)], far("#d47c56", D, 0.45), 1.0)
    s.poly([P(-30, 0, hc + 160), P(W_ / 2, 0, apex), P(W_ / 2, 1800, apex), P(-30, 1800, hc + 160)], far("#cf7c56", D, 0.5), 0.95)
    ax, ay = P(W_ / 2, 0, apex)
    s.ellipse(ax, ay - 1.4, 1.3, 1.6, far("#9a7a40", D, 0.4))              # a small figure on the peak
    sc, sa = s.done()
    c.put(sc, sa)


# ---------------------------------------------------------------- the far end of the square
def concord(c, seed=41):
    """An older temple at the foot of the hill, behind the platform: grey stone and stucco, a terracotta roof."""
    m = CONCORD
    mf = frame(m["angle"], m["x"], m["D"])
    D = m["D"]
    s = Sheet2(SHAPE)
    hp, hc = m["podium"], m["podium"] + m["cols"]
    W_ = m["width"]
    P = mf.pt
    lit_c, shade_c, deep_c = far("#efdcb8", D, 0.5), far("#a8a0c2", D, 0.5), far("#6e6890", D, 0.5)
    s.poly([P(0, 0, 0), P(W_, 0, 0), P(W_, 0, hp), P(0, 0, hp)], far("#d6c39c", D, 0.5))
    s.poly([P(0, 0, 0), P(0, 2000, 0), P(0, 2000, hp), P(0, 0, hp)], far("#c4b294", D, 0.5))
    s.poly([P(200, -420, 0), P(W_ - 200, -420, 0), P(W_ - 200, 0, hp), P(200, 0, hp)], far("#f6ead2", D, 0.5))
    for i in range(1, 9):
        hh = hp * i / 9
        s.line([P(200, -420 * (1 - i / 9), hh), P(W_ - 200, -420 * (1 - i / 9), hh)], far("#c8b8a4", D, 0.5), 0.6, 0.6)
    s.poly([P(50, 140, hp), P(W_ - 50, 140, hp), P(W_ - 50, 140, hc), P(50, 140, hc)], deep_c)
    s.poly([P(0, 0, hp), P(0, 2000, hp), P(0, 2000, hc), P(0, 0, hc)], far("#d9c6a6", D, 0.5))
    for j in range(6):
        u = lerp(100, W_ - 100, j / 5)
        a0, a1 = P(u, 0, hp), P(u, 0, hc)
        s.line([a0, a1], lit_c, max(1.2, 90 * k(D)))
        s.line([(a0[0] + 1.0, a0[1]), (a1[0] + 1.0, a1[1])], shade_c, 0.8, 0.7)
    s.poly([P(-20, 0, hc), P(W_ + 20, 0, hc), P(W_ + 20, 0, hc + 140), P(-20, 0, hc + 140)], lit_c)
    apex = hc + 140 + W_ / 2 * 0.30
    s.poly([P(-30, 0, hc + 140), P(W_ / 2, 0, apex), P(W_ + 30, 0, hc + 140)], far("#e6d0ae", D, 0.5))
    s.line([P(-30, 0, hc + 140), P(W_ / 2, 0, apex), P(W_ + 30, 0, hc + 140)], far("#c8603e", D, 0.45), 1.1)
    s.poly([P(-30, 0, hc + 140), P(W_ / 2, 0, apex), P(W_ / 2, 2000, apex), P(-30, 2000, hc + 140)], far("#c86e4a", D, 0.5), 0.95)
    sc, sa = s.done()
    c.put(sc, sa)


def saturn(c, seed=5):
    """The temple of Saturn, the act's own, from across the square: six columns on a high base, the lower third of each
    red, the painted beam and band above them, the blue-green pediment, the bronze doors standing open; its steps
    coming down toward us. (The same temple and colours as rome_steps.py, small and far off.)"""
    sf = saturn_frame(fine=2)
    D = SATURN["D"]
    cv = Canvas(sf.shape)
    FR = -sf.to_frame(SUN)[1]                                # how squarely its front faces the sun
    LF = -sf.to_frame(SUN)[0]                                # ...and its left flank
    stucco, red, trav, tufa_ = far(STUCCO, D, 0.45), far(RED, D, 0.4), far(TRAV, D, 0.45), far(TUFA, D, 0.45)
    pf = lambda own: own
    # the left flank of the podium and of the cella, a sliver, in the sun at a slant
    for Wf, m in sf.face([(0, S_EDGE, 0), (0, S_BACK, 0), (0, S_BACK, S_HP), (0, S_EDGE, S_HP)]):
        v, h, ppc = Wf.on_side(0.0)
        own, _ = tufa(v, h, ppc, seed + 2, base=TUFA)
        cv.put(LIT.on(far(own, D, 0.45), LF, 0.0, bounce=0.5), m, Wf)
    for Wf, m in sf.face([(45, S_DEEP, S_HP), (45, S_BACK, S_HP), (45, S_BACK, S_E0), (45, S_DEEP, S_E0)]):
        v, h, ppc = Wf.on_side(45.0)
        own = np.where(((h - S_HP) < 150)[..., None], col(DADO), col(STUCCO))[...] * np.ones(v.shape + (1,), dtype=F32)
        cv.put(LIT.on(far(own, D, 0.45), LF, 0.0, deep=0.1, bounce=0.3), m, Wf)
    # the porch: its wall with the doorway, the dark room inside, the bronze leaves; the ceiling dark
    d0, d1, dh0, dh1 = S_DOOR
    for Wf, m in sf.face([(45, S_DEEP, S_HP), (S_UW - 45, S_DEEP, S_HP), (S_UW - 45, S_DEEP, S_E0), (45, S_DEEP, S_E0)]):
        u, h, ppc = Wf.on_front(S_DEEP)
        own = np.where(((h - S_HP) < 150)[..., None], col(DADO), col(STUCCO)) * np.ones(u.shape + (1,), dtype=F32)
        door = (u > d0) & (u < d1) & (h > dh0) & (h < dh1)
        own = np.where(door[..., None], col("#1c141a"), own)
        leaf_l = (u > d0) & (u < d0 + 50) & (h > dh0) & (h < dh1)
        leaf_r = (u > d1 - 26) & (u < d1) & (h > dh0) & (h < dh1)
        own = np.where((leaf_l | leaf_r)[..., None], col("#c89a4a"), own)
        case = ((np.abs(u - d0) < 22) | (np.abs(u - d1) < 22) | (np.abs(h - dh1 - 12) < 14)) & (u > d0 - 30) & (u < d1 + 30) & (h < dh1 + 28)
        own = np.where(case[..., None] & ~door[..., None], col(TRAV), own)
        cv.put(LIT.on(far(own, D, 0.42), 0.0, deep=0.55, bounce=0.9 * (1 - np.clip((h - S_HP) / S_HC, 0, 1))), m, Wf)
    for Wf, m in sf.face([(45, -36, S_E0), (S_UW - 45, -36, S_E0), (S_UW - 45, S_DEEP, S_E0), (45, S_DEEP, S_E0)]):
        cv.put(LIT.on(far("#7a5a3e", D, 0.4), 0.0, deep=0.7, up=-1, bounce=0.8), m, Wf)
    # the porch floor, and the podium's front beside the steps
    for Wf, m in sf.face([(0, S_EDGE, S_HP), (S_UW, S_EDGE, S_HP), (S_UW, S_DEEP, S_HP), (0, S_DEEP, S_HP)]):
        cv.put(LIT.on(trav, WSH, 0.0, up=1, deep=0.3), m, Wf)
    for (a0, a1) in ((0, S_SU0), (S_SU1, S_UW)):
        for Wf, m in sf.face([(a0, S_EDGE, 0), (a1, S_EDGE, 0), (a1, S_EDGE, S_HP), (a0, S_EDGE, S_HP)]):
            u, h, ppc = Wf.on_front(S_EDGE)
            own, _ = tufa(u, h, ppc, seed + 7, base=TUFA)
            cv.put(LIT.on(far(own, D, 0.45), FR, 0.0, bounce=0.6), m, Wf)
    # the steps, fourteen of them: risers facing us, treads lit from above
    for kk in range(S_NSTEP, 0, -1):
        vk = S_VK(kk)
        for Wf, m in sf.face([(S_SU0, vk, (kk - 1) * S_RISE), (S_SU1, vk, (kk - 1) * S_RISE), (S_SU1, vk, kk * S_RISE), (S_SU0, vk, kk * S_RISE)], pad=1):
            cv.put(LIT.on(trav * 0.97, max(FR, 0.42), 0.0, bounce=0.9), m, Wf)
        if kk < S_NSTEP:
            for Wf, m in sf.face([(S_SU0, vk, kk * S_RISE), (S_SU1, vk, kk * S_RISE), (S_SU1, S_VK(kk + 1), kk * S_RISE), (S_SU0, S_VK(kk + 1), kk * S_RISE)], pad=1):
                cv.put(LIT.on(trav * 1.02, 0.62, 0.0, up=1, bounce=0.5), m, Wf)
    for Wf, m in sf.face([(S_SU0, S_VK(1), 0), (S_SU0, S_EDGE, 0), (S_SU0, S_EDGE, S_HP), (S_SU0, S_VK(S_NSTEP), S_HP - S_RISE)]):
        v, h, ppc = Wf.on_side(S_SU0)
        cv.put(LIT.on(trav * 0.95, LF * 0.8, 0.0, bounce=0.6), m, Wf)
    # the six columns of the front: cream stucco, the lower third red, a dark ring where the red stops
    k_ = sf.k(S_UW / 2, 0)
    for i, cu in enumerate(S_COLS):
        for Wf, m in sf.face([(cu - 38, -38, S_HP), (cu + 38, -38, S_HP), (cu + 32, -38, S_E0), (cu - 32, -38, S_E0)], pad=1):
            u, h, ppc = Wf.on_front(-38.0)
            across = np.clip((u - (cu - 36)) / 72.0, 0, 1)
            own = np.where(((h - S_HP) < 220)[..., None] & ((h - S_HP) > 33)[..., None], col(RED), col(STUCCO)) * np.ones(u.shape + (1,), dtype=F32)
            own = np.where((np.abs(h - S_HP - 222) < 6)[..., None], col(P_BLACK), own)
            facing = np.clip(0.95 - across * 0.85, 0, 1)                   # lit on the left, turning away on the right
            cv.put(LIT.on(far(own, D, 0.42), facing, 0.0, bounce=0.5), m, Wf)
    # the beam, the painted band and the gutter across the front; the pediment, blue-green, with its raking gutters
    for (h0, h1, paint) in ((S_E0, S_E1, "revet"), (S_E1, S_E2, "frieze"), (S_E2, S_E3, "gutter")):
        for Wf, m in sf.face([(34, -36, h0), (S_UW - 34, -36, h0), (S_UW - 34, -36, h1), (34, -36, h1)], pad=1):
            u, h, ppc = Wf.on_front(-36.0)
            b = h - h0
            if paint == "revet":
                own = np.where((b < 10)[..., None], col(P_BLACK), np.where(((u % 16) < 8)[..., None] & (b > 24)[..., None], col(P_CREAM), col(P_RED)))
            elif paint == "frieze":
                x_ = ((u - 70 + 42.5) % 85.0) - 42.5
                own = np.where((np.abs(x_) < 15)[..., None], col(P_CREAM), np.where(((np.floor((u - 27.5) / 85.0) % 2) == 0)[..., None], col(P_RED), col(P_BLACK)))
            else:
                own = np.where(((u % 13) < 6.5)[..., None], col(P_RED), col(P_BLUE)) * 0.9 + col(P_CREAM) * 0.1
            own = own * np.ones(u.shape + (1,), dtype=F32)
            cv.put(LIT.on(far(own, D, 0.42), FR, 0.0, bounce=0.4), m, Wf)
    half = S_UW / 2 - 34 + S_EAVE
    apex = S_E3 + half * S_PITCH
    for Wf, m in sf.face([(34 - S_EAVE, -28, S_E3), (S_UW / 2, -28, apex), (S_UW - 34 + S_EAVE, -28, S_E3)]):
        u, h, ppc = Wf.on_front(-28.0)
        own = col("#6e97a6")[None, None, :] * (1 + (tex(u, h, 200, seed + 15)[..., None] - 0.5) * 0.3)
        cv.put(LIT.on(far(own, D, 0.4), FR, 0.0, bounce=0.3), m, Wf)
    for Wf, m in sf.face([(34 - S_EAVE - 14, -40, S_E3 - 2), (S_UW / 2, -40, apex + 14), (S_UW - 34 + S_EAVE + 14, -40, S_E3 - 2),
                          (S_UW - 34 + S_EAVE, -40, S_E3 - 2), (S_UW / 2, -40, apex - 18), (34 - S_EAVE, -40, S_E3 - 2)]):
        cv.put(LIT.on(far(col(P_RED) * 0.6 + col(P_CREAM) * 0.4, D, 0.42), FR, 0.0, bounce=0.3), m, Wf)
    # the roof's long slope over the flank, tiles in the sun
    for Wf, m in sf.face([(34 - S_EAVE, -40, S_E3), (34 - S_EAVE, S_BACK + 30, S_E3), (S_UW / 2, S_BACK + 30, apex), (S_UW / 2, -40, apex)]):
        cv.put(LIT.on(far(TILE, D, 0.45), 0.55, 0.0, up=0.6), m, Wf)
    out = cv.reduced(2)
    c.lay(out)


def rostra(c, seed=43):
    """The new speakers' platform, long and low and gently curved, faced with pale stone, the bronze beaks of old ships
    set along its front, statues on it; unfinished: its right end still rough, facing stones stacked beside it."""
    r = ROSTRA
    s, g = Sheet2(SHAPE), Sheet2(SHAPE)
    rng = np.random.default_rng(seed)
    n = 24
    xs = np.linspace(r["x0"], r["x1"], n)
    Ds = [r["D"] - r["bulge"] * math.sin(math.pi * (x - r["x0"]) / (r["x1"] - r["x0"])) for x in xs]
    foot = [pt(x, 0, D_) for x, D_ in zip(xs, Ds)]
    top = [pt(x, r["h"], D_) for x, D_ in zip(xs, Ds)]
    Dm = r["D"]
    face_c = far("#f1e6cc", Dm, 0.4)
    s.poly(foot + top[::-1], face_c)
    for i in range(n - 1):                                    # the facing slabs, a little different each
        tone = mix("#efe2c6", "#e2d2b0", rng.random())
        s.poly([foot[i], foot[i + 1], top[i + 1], top[i]], far(tone, Dm, 0.4), 0.6)
        if i % 2 == 0:
            s.line([foot[i], top[i]], far("#b9a88e", Dm, 0.4), 0.6, 0.6)
    for hh in (60, 260):                                     # the base course and the crown, mouldings in shade
        s.line([pt(x, hh, D_) for x, D_ in zip(xs, Ds)], far("#a59cb6", Dm, 0.4), 1.0, 0.8)
    s.line(top, far("#fff6de", Dm, 0.4), 1.2)
    # the top: a pale floor seen just from above, a low rail of posts
    back = [pt(x, r["h"], D_ + 600) for x, D_ in zip(xs, Ds)]
    s.poly(top + back[::-1], far("#f7ecd2", Dm, 0.4))
    for x, D_ in list(zip(xs, Ds))[1:-1:2]:
        s.line([pt(x, r["h"], D_ + 30), pt(x, r["h"] + 90, D_ + 30)], far("#d8c6a2", Dm, 0.4), 0.9)
    s.line([pt(x, r["h"] + 90, D_ + 30) for x, D_ in zip(xs, Ds)], far("#f6e8c8", Dm, 0.4), 0.9)
    # the beaks of old warships, bronze gone green, set along the front (not yet along its unfinished right-hand part)
    for j in (0, 1, 2, 3, 6):
        t_ = (j + 0.5) / 7
        x = lerp(r["x0"] + 80, r["x1"] - 200, t_)
        D_ = r["D"] - r["bulge"] * math.sin(math.pi * (x - r["x0"]) / (r["x1"] - r["x0"]))
        a = pt(x, 170, D_ - 10)
        kk = k(D_)
        w = 28 * kk
        g.poly([(a[0] - w, a[1] - w * 0.7), (a[0] + w * 0.4, a[1] - w * 0.8), (a[0] + w * 1.2, a[1] - w * 0.1), (a[0] + w * 0.6, a[1] + w * 0.6), (a[0] - w, a[1] + w * 0.4)], far("#3c5a50", D_, 0.30))
        g.line([(a[0] - w * 0.8, a[1] - w * 0.5), (a[0] + w * 0.5, a[1] - w * 0.6)], far("#c8b070", D_, 0.3), 0.7, 0.8)
        g.line([(a[0] - w * 1.2, a[1] + w * 1.4), (a[0] - w * 2.6, a[1] + w * 1.6)], far("#a49cbc", D_, 0.4), 1.2, 0.5)      # its shadow on the stone
    # statues on the platform: one on horseback, two standing, bronze, one gilded
    for (fx_, kind) in ((0.30, "rider"), (0.52, "stand"), (0.68, "stand")):
        x = lerp(r["x0"], r["x1"], fx_)
        D_ = r["D"] - r["bulge"] * math.sin(math.pi * fx_) + 260
        bx, by = pt(x, r["h"], D_)
        kk = k(D_)
        s.poly([(bx - 50 * kk, by), (bx + 50 * kk, by), (bx + 46 * kk, by - 120 * kk), (bx - 46 * kk, by - 120 * kk)], far("#e8dcc0", D_, 0.4))
        top_ = by - 120 * kk
        body = far("#5a6a52" if kind == "stand" else "#b08a3c", D_, 0.35)
        if kind == "rider":
            g.poly([(bx - 36 * kk, top_ - 60 * kk), (bx + 40 * kk, top_ - 64 * kk), (bx + 44 * kk, top_ - 100 * kk), (bx - 30 * kk, top_ - 96 * kk)], body)
            for lx in (-30, -14, 20, 34):
                g.line([(bx + lx * kk, top_ - 62 * kk), (bx + lx * kk, top_)], body, max(0.8, 9 * kk))
            g.line([(bx + 40 * kk, top_ - 96 * kk), (bx + 58 * kk, top_ - 124 * kk)], body, max(0.9, 14 * kk))
            g.poly([(bx - 6 * kk, top_ - 96 * kk), (bx + 12 * kk, top_ - 96 * kk), (bx + 8 * kk, top_ - 160 * kk), (bx - 4 * kk, top_ - 160 * kk)], body)
            g.ellipse(bx + 2 * kk, top_ - 172 * kk, 10 * kk, 11 * kk, body)
            g.line([(bx - 20 * kk, top_ - 92 * kk), (bx + 30 * kk, top_ - 100 * kk)], far("#ffe9a0", D_, 0.3), 0.8, 0.9)
        else:
            g.poly([(bx - 20 * kk, top_), (bx + 22 * kk, top_), (bx + 16 * kk, top_ - 150 * kk), (bx - 14 * kk, top_ - 150 * kk)], body)
            g.ellipse(bx + 1 * kk, top_ - 164 * kk, 11 * kk, 12 * kk, body)
            g.line([(bx + 14 * kk, top_ - 120 * kk), (bx + 38 * kk, top_ - 150 * kk)], body, max(0.9, 9 * kk))
            g.line([(bx - 12 * kk, top_ - 20 * kk), (bx - 10 * kk, top_ - 140 * kk)], far("#9ab89a", D_, 0.3), 0.7, 0.8)
    # unfinished: a stretch of its front right of the statues not yet faced, the rough tufa core showing in courses, the
    # crown not on; the facing slabs for it leaning against it, waiting (where the column of a statue does not hide them)
    bD = lambda x: r["D"] - r["bulge"] * math.sin(math.pi * (x - r["x0"]) / (r["x1"] - r["x0"]))
    core = [(x, bD(x)) for x in np.linspace(560.0, 800.0, 7)]
    s.poly([pt(x, 0, D_) for x, D_ in core] + [pt(x, r["h"] - 26, D_) for x, D_ in core[::-1]], far("#bba78c", Dm, 0.4))
    for hh in (75, 150, 225):
        s.line([pt(x, hh, D_ + 2) for x, D_ in core], far("#8e7c66", Dm, 0.4), 0.6, 0.55)
    for x, D_ in core[1:-1:2]:
        s.line([pt(x, 0, D_), pt(x, r["h"] - 26, D_)], far("#8e7c66", Dm, 0.4), 0.5, 0.4)
    for j, xs in enumerate((590.0, 668.0, 742.0)):
        D_ = bD(xs + 35) - 38
        top = 128 + 12 * j
        q = [pt(xs, 0, D_), pt(xs + 70, 0, D_), pt(xs + 70, top, D_ + 24), pt(xs, top, D_ + 24)]
        s.poly(q, far(mix("#f6efe0", "#e6d9c2", rng.random()), D_, 0.4))
        s.line([q[3], q[2]], far("#fffaea", D_, 0.4), 0.7)
        s.line([q[1], q[2]], far("#a89cb4", D_, 0.4), 0.6, 0.7)
        s.line([(q[0][0] + 0.6, q[0][1] + 0.4), (q[1][0] + 2.2, q[1][1] + 0.6)], far("#a49cbc", D_, 0.4), 0.9, 0.5)     # its shadow at its foot
    for sh in (s, g):
        sc, sa = sh.done()
        c.put(sc, sa)


def far_people(c, seed=45):
    """A few tiny figures far off at the end of the square: dabs of toga and tunic, a dark head, a short shadow away."""
    s = Sheet2(SHAPE)
    rng = np.random.default_rng(seed)
    cloth = ["#fbf2dc", "#c8553a", "#7d94b8", "#f6ead0", "#d9a441", "#8a6a4e", "#fbf2dc"]
    spots = [(-560, 6500), (-470, 6650), (60, 7600), (140, 7700), (980, 6700), (-120, 6900), (1120, 7000)]
    for i, (x, D_) in enumerate(spots):
        up = 300.0 if D_ > 7500 else 0.0                   # two stand on the platform
        if up:
            D_ = ROSTRA["D"] + 300
        p = pt(x, up, D_)
        hgt = (150 + 30 * rng.random()) * k(D_)
        s.line([(p[0] + 0.5, p[1]), (p[0] + 2.5, p[1] - 1.5)], far("#8f88a8", D_, 0.4), max(0.8, hgt * 0.12), 0.45)
        s.line([p, (p[0], p[1] - hgt * 0.84)], far(cloth[i % len(cloth)], D_, 0.35), max(1.1, hgt * 0.30))
        s.ellipse(p[0], p[1] - hgt * 0.92, max(0.7, hgt * 0.10), max(0.7, hgt * 0.10), far("#7a5a48", D_, 0.35))
    sc, sa = s.done()
    c.put(sc, sa)


# ---------------------------------------------------------------- the sides of the square
def julia(c, seed=51):
    """Caesar's basilica down the left side, beyond the Tuscan street: two storeys of arches between piers with half-
    columns, white and new; its long front faces across the square and is in shade, glowing low down with the light
    thrown up from the paving; its near end faces us across the street's mouth, in the temple of Castor's long shadow.
    At its far end it is not finished: timber scaffolding against it, a small crane."""
    from rome_forum_things import castor_shade
    j = JULIA
    x = j["x"]
    s = Canvas(SHAPE)
    bay = j["bay"]

    def storeys(a, h, ppc, f, pier):
        own = np.empty(a.shape + (3,), dtype=F32)
        own[...] = col(MARBLE)
        own = own * (0.95 + 0.07 * tex(a, h, 160, seed)[..., None])
        for (h0, h1) in ((24, j["h1"] - 50), (j["h1"] + 34, j["h2"] - 40)):
            spring = h1 - (bay * 0.62) / 2
            cx = 0.59
            r = 0.31
            inside = (~pier) & (h > h0) & ((h < spring) | ((((f - cx) * bay) ** 2 + (h - spring) ** 2) < (r * bay) ** 2))
            depth = np.clip((h - h0) / (h1 - h0), 0, 1)
            room = ramp(depth, [(0.0, "#7a6468"), (0.5, "#56485e"), (1.0, "#40364e")])
            own = np.where(inside[..., None], room, own)
        for hh in (j["h1"] - 34, j["h1"], j["h2"] - 24, j["h2"]):
            own = own * (1 - 0.32 * np.clip(1.5 - np.abs(h - hh) * ppc / 1.2, 0, 1)[..., None])
        return own

    # the long front, facing across the square (to our right): in shade
    for Wf, m in WORLD.face([(x, j["D0"], 0), (x, j["D1"], 0), (x, j["D1"], j["roof"]), (x, j["D0"], j["roof"])]):
        Dv, h, ppc = Wf.on_side(x)
        q = (Dv - j["D0"]) / bay
        f = q - np.floor(q)
        pier = (f < 0.26) | (f > 0.92)
        own = storeys(Dv, h, ppc, f, pier)
        half_col = (np.abs(f - 0.10) < 0.04) & (h < j["h2"])
        own = np.where(half_col[..., None], own * 1.06, own)
        far_part = np.clip((Dv - (j["D1"] - 700)) / 400.0, 0, 1)                    # its far end: not yet faced, rougher
        own = lerp(own, own * np.array([0.88, 0.82, 0.76], dtype=F32), (far_part * 0.8)[..., None])
        bounce = 0.45 + 1.0 * np.clip(1 - h / 360.0, 0, 1)
        lit_ = LIT.on(own, FACE_RIGHT, 0.0, deep=0.10, bounce=bounce)
        s.put(far(lit_, Dv, 0.6), m, Wf)
    # its near end, facing us across the street's mouth: in the long shadow of the temple of Castor
    for Wf, m in WORLD.face([(x - 900, j["D0"], 0), (x, j["D0"], 0), (x, j["D0"], j["roof"]), (x - 900, j["D0"], j["roof"])]):
        u, h, ppc = Wf.on_front(j["D0"])
        q = (x - u) / bay
        f = q - np.floor(q)
        pier = (f < 0.26) | (f > 0.92)
        own = storeys(u, h, ppc, f, pier)
        cut = castor_shade(u, h, j["D0"])
        s.put(far(LIT.on(own, FACE_US, cut, deep=0.05 * cut, bounce=0.5), j["D0"], 0.6), m, Wf)
    # the roof: a low pitch of tiles over the finished part; at the far end bare rafters
    for Wf, m in WORLD.face([(x - 900, j["D0"], j["roof"]), (x, j["D0"], j["roof"]), (x, j["D1"] - 700, j["roof"]), (x - 900, j["D1"] - 700, j["roof"])]):
        s.put(far(LIT.on(col(TILE), 0.7, 0.0, up=1), j["D0"] + 600, 0.6), m, Wf)
    sh = Sheet2(SHAPE)
    for i in range(10):                                                          # rafters standing bare over the far bays
        Dp = j["D1"] - 700 + i * 70
        sh.line([pt(x, j["roof"], Dp), pt(x - 300, j["roof"] + 90, Dp)], far(WOOD, Dp, 0.45), 0.8, 0.9)
    # the scaffolding at the far end: poles, ledgers, braces; a small crane at the corner
    for i in range(6):
        Dp = j["D1"] - 760 + i * 150
        a, b = pt(x + 50, 0, Dp), pt(x + 50, j["roof"] + 140, Dp)
        sh.line([a, b], far(WOOD_L, Dp, 0.45), max(0.8, 14 * k(Dp)))
    for hh in (150, j["h1"], j["h1"] + 170, j["h2"], j["roof"] + 80):
        sh.line([pt(x + 50, hh, j["D1"] - 760), pt(x + 50, hh, j["D1"])], far(WOOD, j["D1"], 0.45), 0.9)
        sh.line([pt(x + 44, hh + 6, j["D1"] - 760), pt(x + 44, hh + 6, j["D1"])], far("#e8c890", j["D1"], 0.45), 0.7, 0.8)
    for i in range(3):
        Dp = j["D1"] - 760 + i * 250
        sh.line([pt(x + 50, 0, Dp), pt(x + 50, j["h2"], Dp + 250)], far(WOOD_D, Dp, 0.45), 0.8, 0.8)
    cx_, cD = x + 160, j["D1"] - 200
    head = pt(cx_ + 60, j["roof"] + 380, cD - 160)
    sh.line([pt(cx_, 0, cD), head], far(WOOD_D, cD, 0.45), 1.1)
    sh.line([pt(cx_ + 180, 0, cD + 80), head], far(WOOD, cD, 0.45), 0.9)
    sh.line([head, (head[0], head[1] + 16)], far("#5a4a40", cD, 0.4), 0.6)
    sh.poly([(head[0] - 2.4, head[1] + 16), (head[0] + 2.4, head[1] + 16), (head[0] + 2.4, head[1] + 19.5), (head[0] - 2.4, head[1] + 19.5)], far("#f2ece0", cD, 0.4))
    sc, sa = sh.done()
    s.put(sc, sa)
    c.lay(s)


def paullus(c, seed=55):
    """The basilica of Paullus down the right side: a long two-storey colonnade, its front facing across the square (to
    our left) and taking the low sun at a slant; under the lower colonnade the shop fronts, dim and warm, goods out on
    their counters, an awning or two; the upper colonnade open, its back wall in shade."""
    p = PAULLUS
    x = p["x"]
    s = Canvas(SHAPE)
    bay = p["bay"]
    for Wf, m in WORLD.face([(x, p["D0"], 0), (x, p["D1"], 0), (x, p["D1"], p["roof"]), (x, p["D0"], p["roof"])]):
        Dv, h, ppc = Wf.on_side(x)
        q = (Dv - p["D0"]) / bay
        i = np.floor(q)
        f = q - i
        col_ = (f < 0.15)                                            # a column, and the opening beside it
        own = np.empty(Dv.shape + (3,), dtype=F32)
        own[...] = col("#f2e6cc")
        own = own * (0.95 + 0.07 * tex(Dv, h, 150, seed)[..., None])
        lower = (h > 16) & (h < p["h1"] - 56)
        upper = (h > p["h1"] + 50) & (h < p["h2"] - 40)
        # behind the lower columns: the shop fronts, warm and dim; a doorway dark in each; goods on the counter
        shop = col("#9a7a6a") * (0.80 + 0.35 * hash2(i, 7, seed)[..., None]) * np.ones(Dv.shape + (1,), dtype=F32)
        door = (f > 0.42) & (f < 0.72) & (h < p["h1"] - 120)
        shop = np.where(door[..., None], col("#3a2a34"), shop)
        goods = (h < 110) & (f > 0.20) & (f < 0.92) & ~door & (hash2(i, 9, seed) > 0.2)
        gtone = np.where((hash2(i, 11, seed) > 0.5)[..., None], col("#d4924c"), col("#b4bc80"))
        shop = np.where(goods[..., None], gtone * (0.75 + 0.45 * tex(Dv * 4.0, h * 4.0, 30, seed + 4)[..., None]), shop)
        awn = (h > p["h1"] - 150) & (h < p["h1"] - 110) & (f > 0.17) & (hash2(i, 13, seed) > 0.45)
        shop = np.where(awn[..., None], np.where(((np.floor(Dv / 18.0) % 2) == 0)[..., None], col("#c8503c"), col("#f2e4c6")), shop)
        open_low = lower & ~col_
        open_up = upper & ~col_
        own = np.where(open_low[..., None], shop, own)
        gallery = col("#8a7a8e") * (0.9 + 0.2 * np.clip((h - p["h1"]) / 300.0, 0, 1))[..., None] * np.ones(Dv.shape + (1,), dtype=F32)
        own = np.where(open_up[..., None], gallery, own)
        for hh in (p["h1"] - 56, p["h1"], p["h2"] - 40, p["h2"]):
            own = own * (1 - 0.30 * np.clip(1.5 - np.abs(h - hh) * ppc / 1.2, 0, 1)[..., None])
        # the sun comes in between the columns at a slant: the column's shadow falls on what is behind it, to its right
        lit_part = (f > 0.15 + 0.22) & (f < 0.98)
        shadowed = (open_low | open_up) & ~lit_part
        cut = np.where(open_low | open_up, np.where(shadowed, 0.9, 0.35), 0.0)
        lit_ = LIT.on(own, FACE_LEFT, cut, deep=np.where(open_low | open_up, 0.25, 0.0), bounce=0.5)
        s.put(far(lit_, Dv, 0.6), m, Wf)
    for Wf, m in WORLD.face([(x, p["D0"], p["roof"]), (x, p["D1"], p["roof"]), (x + 700, p["D1"], p["roof"] + 200), (x + 700, p["D0"], p["roof"] + 200)]):
        s.put(far(LIT.on(col(TILE), 0.6, 0.0, up=0.7), p["D0"] + 800, 0.6), m, Wf)
    sh = Sheet2(SHAPE)
    sh.line([pt(x - 10, p["roof"], p["D0"]), pt(x - 10, p["roof"], p["D1"])], far("#fff0d0", p["D0"] + 1500, 0.5), 1.2)        # the eaves catch the sun
    sc, sa = sh.done()
    s.put(sc, sa)
    c.lay(s)


def tuscan(c, seed=61):
    """What is seen behind the temple of Castor's corner and in the mouth of the Tuscan street: the street's paving in
    the long shadow of the temple, a house front deep in it, a shrine at the corner, the slope of the Palatine beyond with
    its houses and trees. (Most of it is hidden by the temple, which is a cut-out: this is the backdrop under it.)"""
    t = TUSCAN
    s = Canvas(SHAPE)
    sh = Sheet2(SHAPE)
    # the Palatine beyond, left of the Capitol: houses up its slope, gardens, all pale with the air
    pal = [(-12, 150), (40, 138), (100, 134), (140, 140), (160, 152), (166, 236), (-12, 236)]
    sh.poly(pal, far("#cbb994", 15000, 0.6))
    rng = np.random.default_rng(seed)
    for i in range(30):
        px = rng.uniform(-5, 150)
        py = rng.uniform(142, 232)
        w, hgt = rng.uniform(8, 18), rng.uniform(6, 12)
        sh.poly([(px, py), (px + w, py), (px + w, py - hgt), (px, py - hgt)], far(mix("#f6e2b8", "#e6cca0", rng.random()), 14000, 0.6))
        sh.poly([(px - 1, py - hgt), (px + w + 1, py - hgt), (px + w / 2, py - hgt - 3)], far(TILE, 14000, 0.55))
    for i in range(18):
        px = rng.uniform(-5, 150)
        py = rng.uniform(140, 230)
        sh.ellipse(px, py, rng.uniform(4, 9), rng.uniform(3, 6), far("#5f7a4a", 14000, 0.5), 0.9)
    sc, sa = sh.done()
    s.put(sc, sa)
    # the house front at the street's bend, facing us, in the shade of the temple
    for Wf, m in WORLD.face([(t["x"] - 2600, t["D1"] - 200, 0), (t["x"], t["D1"] - 200, 0), (t["x"], t["D1"] - 200, 700), (t["x"] - 2600, t["D1"] - 200, 700)]):
        u, h, ppc = Wf.on_front(t["D1"] - 200)
        own = plain(u, h, "#e2b878", seed + 2)
        own = np.where((h < 120)[..., None], col("#8a3e32"), own)
        win = ((u % 260) > 90) & ((u % 260) < 170) & (h > 380) & (h < 520)
        door = ((u % 520) > 140) & ((u % 520) < 300) & (h < 260)
        own = np.where((win | door)[..., None], col("#3a2a36"), own)
        s.put(LIT.on(own, 0.0, 0.0, deep=0.25, bounce=0.6), m, Wf)
    c.lay(s)


def site_inside(c, seed=65):
    """The ground of the site of the new senate house, behind its hoarding: trodden earth and stone chips round the
    pit. (The hoarding is a cut-out: this is all behind it, and none of it shows over the hoarding; what does show, the
    new wall going up and the blocks and the scaffold, is site_works, laid after the basilica of Paullus.)"""
    s = Canvas(SHAPE)
    sh = Sheet2(SHAPE)
    hd = HOARD
    (ax, aD), (bx, bD) = hd["a"], hd["b"]
    inside = [pt(ax, 0, aD), pt(bx, 0, bD), pt(PAULLUS["x"] - 40, 0, PAULLUS["D0"]), pt(PAULLUS["x"] + 400, 0, 1000)]
    sh.poly(inside, "#c8ae86")
    sc, sa = sh.done()
    s.put(sc, sa)
    c.lay(s)


def site_works(c, seed=67):
    """What of the site shows over its hoarding: the new senate house's front wall risen out of the pit, squared tufa
    full in the morning sun, its near end stepped down where the courses stop; blocks of white stone set out along its
    top for the next course; a stack of tufa blocks waiting at its foot; a little timber scaffold under the crane's load.
    (Laid after the basilica of Paullus, which stands behind it; the crane is laid over all of it, in `details`.)"""
    w = SITE_WALL
    s = Canvas(SHAPE)
    rng = np.random.default_rng(seed)
    Df, Dt, hh = w["D"], w["D"] + w["thick"], w["h"]
    x0, x1 = w["x0"], w["x1"]
    pieces = [(x0, x0 + 55.0, hh - 120.0), (x0 + 55.0, x0 + 110.0, hh - 60.0), (x0 + 110.0, x1, hh)]
    FRONT = 0.62                                              # (a little less than full sun, as the other faces toward us here)

    def block(xa, xb, Da, Db, ha, hb, paint, sd):
        """A squared block or a length of wall: its left end (toward the square, at a slant), its top, its front."""
        for Wf, m in WORLD.face([(xa, Da, ha), (xa, Db, ha), (xa, Db, hb), (xa, Da, hb)]):
            v, h, ppc = Wf.on_side(xa)
            own, _ = paint(v, h, ppc, sd)
            s.put(far(LIT.on(own, FACE_LEFT, 0.0, bounce=0.4), Da, 0.6), m, Wf)
        if hb < EYE - 2:
            for Wf, m in WORLD.face([(xa, Da, hb), (xb, Da, hb), (xb, Db, hb), (xa, Db, hb)]):
                u, v, ppc = Wf.on_floor(hb)
                own, _ = paint(u, v, ppc, sd + 1)
                s.put(far(LIT.on(own, FACE_UP, 0.0, up=1), Da, 0.6), m, Wf)
        for Wf, m in WORLD.face([(xa, Da, ha), (xb, Da, ha), (xb, Da, hb), (xa, Da, hb)]):
            u, h, ppc = Wf.on_front(Da)
            own, _ = paint(u, h, ppc, sd + 2)
            s.put(far(LIT.on(own, FRONT, 0.0, bounce=0.4), Da, 0.6), m, Wf)

    fresh = lambda a, b, ppc, sd: tufa(a, b, ppc, seed + sd, long=120.0, high=60.0)
    white = lambda a, b, ppc, sd: travertine(a, b, ppc, seed + 30 + sd, base="#f4ede0", long=400.0, high=400.0)
    for i, (xa, xb, top) in enumerate(pieces):
        block(xa, xb, Df, Dt, 0.0, top, fresh, 3 * i)
    # white blocks set out along the top, waiting for the next course
    for (xa, xb) in ((905.0, 1012.0), (1040.0, 1150.0), (1188.0, 1290.0)):
        block(xa, xb, Df + 25.0, Df + 85.0, hh, hh + 58.0, white, int(xa))
    # a stack of tufa blocks at the wall's foot, three high, each course a little askew of the one under it
    st = SITE_STACK
    for j in range(st["courses"]):
        off = (-14.0, 10.0, -4.0)[j % 3]
        block(st["x0"] + off, st["x1"] + off, st["D"] + off * 0.5, st["D"] + st["d"] + off * 0.5, j * st["high"], (j + 1) * st["high"], fresh, 40 + j)
    # the scaffold under the crane's load: two poles, two ledgers, a brace, a plank, the lashings
    sc_ = SITE_SCAFFOLD
    sh = Sheet2(SHAPE)
    Dp = sc_["D"]
    kk = k(Dp)
    xa, xb = sc_["xs"]
    for xp in (xa, xb):
        a, b = pt(xp, 0.0, Dp), pt(xp, sc_["h"], Dp)
        sh.line([a, b], "#8a5e38", max(1.4, 10 * kk))
        sh.line([(a[0] - 0.8, a[1]), (b[0] - 0.8, b[1])], "#e0b070", 0.8, 0.85)
    for hl in sc_["ledgers"]:
        sh.line([pt(xa - 45, hl, Dp), pt(xb + 45, hl, Dp)], "#6e4a2e", max(1.2, 8 * kk))
        sh.line([pt(xa - 45, hl + 4, Dp), pt(xb + 45, hl + 4, Dp)], "#d9a868", 0.7, 0.8)
    sh.line([pt(xa, 20.0, Dp), pt(xb, sc_["ledgers"][1], Dp)], "#6e4a2e", max(1.0, 7 * kk), 0.95)
    sh.line([pt(xa - 30, sc_["ledgers"][0] + 9, Dp - 20), pt(xb + 40, sc_["ledgers"][0] + 9, Dp - 20)], "#c99a62", max(1.0, 6 * kk))   # a plank laid across
    for xp in (xa, xb):
        for hl in sc_["ledgers"]:
            q = pt(xp, hl + 2, Dp)
            sh.ellipse(q[0], q[1], 1.3, 1.1, "#4a3828", 0.9)                                                   # the rope lashings
    sh.line([pt(xb, sc_["ledgers"][1], Dp), (pt(xb, sc_["ledgers"][1], Dp)[0] + 2.0, pt(xb, sc_["ledgers"][0] - 30, Dp)[1])], "#7a6a58", 0.7, 0.8)   # a rope hanging down
    sc2, sa2 = sh.done()
    s.put(sc2, sa2)
    c.lay(s)


def crane_parts(t=0.0):
    """The treadwheel crane, in the site: the two legs of its A-frame leaning out over the work, the head with its
    pulleys, the rope down to a block of white stone in a sling, the back-stays; and the great wheel at its foot that men
    walk in to wind the rope (`t` turns the wheel: 0 to 1 is one spoke's turn). -> (frame, wheel, (wheel's middle, its
    height in pixels))"""
    cr = CRANE
    x0, D0 = cr["x"], cr["D"]
    fr, wh = Sheet2(SHAPE), Sheet2(SHAPE)
    head = (x0 - 330.0, 1080.0, D0 + 300.0)
    legs = [(x0 - 150.0, 0.0, D0 - 60.0), (x0 + 120.0, 0.0, D0 + 220.0)]
    hx, hy = pt(head[0], head[1], head[2])
    for i, (lx, lh, lD) in enumerate(legs):
        a = pt(lx, lh, lD)
        kk = k(lD)
        fr.line([a, (hx, hy)], "#6e4a2e" if i else "#8a5e38", max(1.6, 24 * kk))
        fr.line([(a[0] - 1.0, a[1]), (hx - 0.8, hy)], "#e0b070", max(0.8, 7 * kk), 0.9)       # the side of the timber toward the sun
    for q in (0.35, 0.62):                                    # cross-ties between the legs
        p0 = pt(lerp(legs[0][0], head[0], q), lerp(0, head[1], q), lerp(legs[0][2], head[2], q))
        p1 = pt(lerp(legs[1][0], head[0], q), lerp(0, head[1], q), lerp(legs[1][2], head[2], q))
        fr.line([p0, p1], "#6e4a2e", 1.6)
    kk = k(head[2])
    fr.ellipse(hx, hy + 4, 14 * kk * 3, 14 * kk * 3, "#5a3e28")
    fr.ellipse(hx - 1, hy + 3, 7 * kk * 3, 7 * kk * 3, "#c99a62", 0.9)
    for (sx, sD) in ((x0 + 520.0, D0 - 200.0), (x0 + 600.0, D0 + 500.0)):
        fr.line([(hx, hy), pt(sx, 0.0, sD)], "#7a6a58", 0.8, 0.85)
    # the load: a block of white stone in a rope sling, hanging under the head
    bh = 560.0
    bx, by = pt(head[0], bh, head[2])
    bw, bd = 160 * kk, 62 * kk
    fr.line([(hx, hy + 6), (bx - bw * 0.25, by - bd * 1.5)], "#4a3c30", 1.0)
    fr.line([(hx, hy + 6), (bx + bw * 0.25, by - bd * 1.5)], "#4a3c30", 1.0)
    fr.poly([(bx - bw / 2, by - bd), (bx + bw / 2, by - bd), (bx + bw / 2, by + bd * 0.4), (bx - bw / 2, by + bd * 0.4)], "#f6efe2")
    fr.poly([(bx - bw / 2, by - bd), (bx + bw / 2, by - bd), (bx + bw / 2 - bw * 0.12, by - bd * 1.45), (bx - bw / 2 + bw * 0.10, by - bd * 1.45)], "#fffbf2")
    fr.poly([(bx + bw / 2 - 2.0, by - bd), (bx + bw / 2, by - bd), (bx + bw / 2, by + bd * 0.4), (bx + bw / 2 - 2.0, by + bd * 0.4)], "#c4bcd2")
    for q in (-0.25, 0.25):
        fr.line([(bx + bw * q, by - bd * 1.5), (bx + bw * q, by + bd * 0.4)], "#6a5a48", 0.9)
    # the great wheel at the foot, on the near side: men walk inside it to wind the rope round its axle
    wc = pt(x0 - 340.0, 250.0, D0 - 120.0)
    kw = k(D0 - 120.0)
    R = 230 * kw
    wh.ellipse(wc[0], wc[1], R * 0.42, R, "#6a4630")            # seen nearly edge-on: an upright ellipse
    wh.ellipse(wc[0], wc[1], R * 0.42 - 3.0, R - 4.0, "#3e2c22")
    for jj in range(8):
        q = (jj + t) / 8.0 * math.pi
        dy = math.cos(q) * (R - 4)
        dx = math.sin(q) * (R * 0.42 - 3)
        wh.line([(wc[0] - dx, wc[1] - dy), (wc[0] + dx, wc[1] + dy)], "#9a6a44", max(1.0, 9 * kw))
    for jj in range(16):                                      # the treads inside the rim, catching the light
        q = (jj + t * 2) / 16.0 * 2 * math.pi
        if math.sin(q) < 0.3:
            wh.line([(wc[0] - (R * 0.42 - 2) * math.sin(q) * 0.9, wc[1] - (R - 3) * math.cos(q)), (wc[0] - (R * 0.42 - 2) * math.sin(q) * 0.9 + 1.6, wc[1] - (R - 3) * math.cos(q))], "#e0b070", 1.0, 0.9)
    wh.ellipse(wc[0], wc[1], 10 * kw, 10 * kw, "#4a3222")
    wh.line([(wc[0], wc[1]), pt(x0 - 150.0, 160.0, D0 - 60.0)], "#5a4a3c", 0.9)       # the rope from its axle to the foot of the frame
    for (px_, pD) in ((x0 - 420.0, D0 - 160.0), (x0 - 260.0, D0 - 80.0)):            # the posts that carry its axle
        wh.line([pt(px_, 0, pD), pt(px_, 270, pD)], "#5e3e28", max(1.2, 10 * kw))
    return fr, wh, (wc, R)


def jupiter_altar():
    """Where the altar before the temple of Jupiter is, on the picture (for the smoke of the Ides offering)."""
    J = JUPITER
    jf = frame(J["angle"], J["x"], J["D"])
    return jf.pt(J["width"] * 0.5, -1300, J["base"] + 40)

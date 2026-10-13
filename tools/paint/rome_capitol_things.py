"""What stands in the precinct of the Capitol, each painted crisply on a clear sheet in the world's own measurements
(rome_capitol_kit), lit by the low sun on our right: the row of kings with the broad base in the middle of it (the
keeper's boy sits on that one: the game draws him), the dictator's statue on the bronze ball of the world, his bronze
chariot facing the temple, the great altar, Romulus's hut, the geese's pen, the parapet over the drop, and the row of
bronze tablets on their posts at the front. rome_capitol.py lays them in: the kings into the backdrop, the rest as
cut-outs that people pass behind."""

import math

import numpy as np

from brush import F32, Sheet, blur, grid, lerp, mask_poly, noise, step
from rome_capitol_kit import *
from rome_steps_kit import Canvas, Frame, col, courses, hash2, holes, mix, stone, tex

SUNW = (SUN[0], SUN[2], SUN[1])                              # toward the sun in the world as (along X, along Z, up)
G = Frame.at(CAM, 0.0, 0.0, 1000.0)                          # the precinct square to us: u = X, v = Z - 1000


def gpt(X, h, Z):
    return P(X, h, Z)


def block(canvas, box, base, seed, grain=0.16, cell=40.0, paint=None, deep=0.0, shadow=0.0, bounce=0.6, fine=1):
    """A squared block standing on the paving, square to us: (X0, X1, Z0, Z1, h0, h1). Its front, the side we can
    see, and its top if it is below our eye. `paint(face, a, b, own)` may change its colour (face "front": a = X,
    b = h; "side": a = Z; "top": a = X, b = Z). `shadow` may be a number or a function (face, a, b) -> 0..1."""
    X0, X1, Z0, Z1, h0, h1 = box
    F = G.finer(fine)
    off = 1000.0
    sh_ = (lambda face, a, b: shadow(face, a, b)) if callable(shadow) else (lambda face, a, b: shadow)
    if X0 > 0 or X1 < 0:                                     # the side toward the middle of the picture
        Xs = X0 if X0 > 0 else X1
        for Wf, m in F.face([(Xs, Z0 - off, h0), (Xs, Z1 - off, h0), (Xs, Z1 - off, h1), (Xs, Z0 - off, h1)]):
            v, h, ppc = Wf.on_side(Xs)
            own = col(base)[None, None, :] * (1 - grain / 2 + grain * tex(v, h, cell, seed)[..., None])
            own = own if paint is None else paint("side", v + off, h, own)
            facing = max(0.0, SUNW[0]) if Xs == X1 else 0.0
            canvas.put(LIT.on(own, facing, 1.0 if Xs == X0 else sh_("side", v + off, h), deep=deep, bounce=bounce * np.clip(1 - (h - h0) / 160.0, 0.2, 1)), m, Wf)
    for Wf, m in F.face([(X0, Z0 - off, h0), (X1, Z0 - off, h0), (X1, Z0 - off, h1), (X0, Z0 - off, h1)]):
        u, h, ppc = Wf.on_front(Z0 - off)
        own = col(base)[None, None, :] * (1 - grain / 2 + grain * tex(u, h, cell, seed + 1)[..., None])
        own = own if paint is None else paint("front", u, h, own)
        canvas.put(LIT.on(own, -SUNW[1], sh_("front", u, h), deep=deep, bounce=bounce * np.clip(1 - (h - h0) / 160.0, 0.2, 1)), m, Wf)
    if h1 < EYE:
        for Wf, m in F.face([(X0, Z0 - off, h1), (X1, Z0 - off, h1), (X1, Z1 - off, h1), (X0, Z1 - off, h1)]):
            u, v, ppc = Wf.on_floor(h1)
            own = col(base)[None, None, :] * (1 - grain / 2 + grain * tex(u, v, cell, seed + 2)[..., None])
            own = own if paint is None else paint("top", u, v + off, own)
            canvas.put(LIT.on(own, SUNW[2], sh_("top", u, v + off), up=1, deep=deep), m, Wf)


def moulded(canvas, X, Z, w, d, h, tone, seed, plinth=14.0, crown=16.0, paint=None, bounce=0.6):
    """A statue's base: a plinth, the die, a moulded crown, as three blocks."""
    block(canvas, (X - w / 2 - 6, X + w / 2 + 6, Z - 6, Z + d + 6, 0, plinth), mix(tone, "#000000", 0.06), seed, bounce=bounce)
    block(canvas, (X - w / 2, X + w / 2, Z, Z + d, plinth, h - crown), tone, seed + 3, paint=paint, bounce=bounce)
    block(canvas, (X - w / 2 - 7, X + w / 2 + 7, Z - 7, Z + d + 7, h - crown, h), mix(tone, "#ffffff", 0.08), seed + 6, bounce=bounce)


# ---------------------------------------------------------------- bronze people
OLD_BRONZE = ("#22201a", "#4a4636", "#9c8a5c", "#e6d28e")      # darkest, shade, lit, glint: old bronze, dark, gone green where rain runs
NEW_BRONZE = ("#4a2c10", "#8a5a24", "#d8a448", "#fff0b0")      # the dictator's new statue, still bright


def figure(s, x, y, k, kind, tones=OLD_BRONZE, seed=0):
    """A bronze statue standing at (x, y) (the middle of its feet), k pixels per cm, lit from our right. `kind` says
    who: "old" (a bearded king in a long robe with a sceptre), "brutus" (the old consul who drove the kings out, his
    sword drawn and held up), "seat" (a king in a long cloak, a staff in his hand), "old2" (a king in a cuirass with
    a spear), "new" (the new statue in a toga, one arm raised as a speaker raises it)."""
    dk, sh, lt, gl = tones
    q = lambda dx, h: (x + dx * k, y - h * k)
    rng = np.random.default_rng(seed)
    H = 1.0
    if kind in ("old", "seat"):                                  # long robe to the feet
        robe = [q(-24, 0), q(26, 0), q(22, 60), q(24, 120), q(20, 150), q(-18, 150), q(-22, 110), q(-26, 50)]
        s.poly(robe, sh)
        s.poly([q(4, 0), q(26, 0), q(22, 60), q(24, 120), q(20, 150), q(6, 150), q(8, 80)], lt)
        for fx in (-14, -4, 12):                                 # folds
            s.line([q(fx, 4), q(fx + 3, 70), q(fx + 1, 140)], dk, max(1.0, 2.2 * k), 0.8)
        torso = [q(-21, 148), q(21, 148), q(24, 192), q(-23, 192)]
        s.poly(torso, sh)
        s.poly([q(3, 148), q(21, 148), q(24, 192), q(5, 192)], lt)
        s.poly([q(-25, 190), q(25, 190), q(16, 204), q(-17, 204)], sh)                    # the cloak over the shoulders
        hx, hy = 1, 214
    elif kind in ("old2", "general"):                            # cuirass, a short kilt of straps, bare legs
        for lx in (-9, 9):
            s.line([q(lx, 2), q(lx * 0.9, 92)], sh if lx < 0 else lt, max(1.0, 9 * k))
        s.poly([q(-21, 90), q(21, 90), q(23, 118), q(-23, 118)], dk)                      # the straps
        for fx in range(-18, 20, 6):
            s.line([q(fx, 92), q(fx, 116)], lt if fx > 0 else sh, max(1.0, 1.6 * k), 0.8)
        s.poly([q(-20, 118), q(20, 118), q(22, 196), q(-20, 196)], sh)                    # cuirass
        s.poly([q(2, 118), q(20, 118), q(22, 196), q(4, 196)], lt)
        s.line([q(-14, 170), q(18, 170)], dk, max(1.0, 1.5 * k), 0.7)
        s.poly([q(-26, 196), q(26, 196), q(20, 208), q(-20, 208)], sh)                    # a cloak on the shoulders
        s.poly([q(-26, 196), q(-34, 110), q(-24, 80), q(-20, 196)], dk)                   # hanging behind
        hx, hy = 0, 220
    elif kind == "brutus":                                       # tunic to the knee, a cloak, the sword up
        for lx in (-9, 9):
            s.line([q(lx, 2), q(lx * 0.8, 70)], sh if lx < 0 else lt, max(1.0, 9 * k))
        s.poly([q(-22, 66), q(24, 66), q(20, 192), q(-18, 192)], sh)
        s.poly([q(4, 66), q(24, 66), q(20, 192), q(6, 192)], lt)
        s.line([q(-16, 70), q(-12, 186)], dk, max(1.0, 2 * k), 0.7)
        s.poly([q(-24, 192), q(22, 192), q(14, 204), q(-18, 204)], sh)
        s.poly([q(-22, 190), q(-34, 120), q(-26, 76), q(-14, 170)], dk)                  # his cloak, thrown back
        hx, hy = 2, 216
    else:                                                        # "new": a toga, one arm raised
        robe = [q(-23, 0), q(25, 0), q(22, 70), q(24, 150), q(25, 192), q(16, 202), q(-16, 202), q(-24, 192), q(-24, 120), q(-25, 50)]
        s.poly(robe, sh)
        s.poly([q(4, 0), q(25, 0), q(22, 70), q(24, 150), q(18, 196), q(6, 196), q(8, 90)], lt)
        s.line([q(-20, 120), q(10, 186)], dk, max(1.0, 3 * k), 0.8)                      # the toga's fold across the chest
        s.line([q(-6, 6), q(-2, 110)], dk, max(1.0, 2 * k), 0.7)
        s.line([q(14, 6), q(16, 80)], gl, max(1.0, 1.6 * k), 0.8)
        hx, hy = 1, 212
    # the head: a beard for the old kings and Brutus
    s.line([q(hx, hy - 14), q(hx, hy - 6)], sh, max(1.0, 9 * k))                         # the neck
    s.ellipse(*q(hx, hy), 11 * k, 13.5 * k, sh)
    s.ellipse(*q(hx + 3, hy + 1), 7 * k, 11 * k, lt)
    if kind in ("old", "seat", "brutus", "old2"):                # (the general on the world is clean-shaven, as Romans are now)
        s.poly([q(hx - 8, hy - 4), q(hx + 9, hy - 4), q(hx + 6, hy - 18), q(hx - 4, hy - 20)], sh)    # beard
        s.poly([q(hx + 1, hy - 4), q(hx + 9, hy - 4), q(hx + 6, hy - 17), q(hx + 2, hy - 18)], lt)
    if kind in ("old", "seat"):
        s.poly([q(hx - 10, hy + 9), q(hx + 10, hy + 9), q(hx + 8, hy + 16), q(hx, hy + 13), q(hx - 8, hy + 16)], dk)   # a crown
        s.line([q(hx - 9, hy + 10), q(hx + 9, hy + 10)], gl, max(1.0, 1.4 * k), 0.8)
    # the arms and what they hold
    if kind == "old":
        s.line([q(18, 190), q(30, 160), q(28, 128)], lt, max(1.0, 8 * k))                # right arm down to the sceptre
        s.line([q(30, 2), q(30, 250)], dk, max(1.0, 4 * k))                               # the sceptre
        s.line([q(31, 30), q(31, 246)], gl, max(1.0, 1.4 * k), 0.8)
        s.ellipse(*q(30, 254), 4.5 * k, 4.5 * k, lt)
        s.line([q(-18, 190), q(-26, 150), q(-18, 120)], sh, max(1.0, 8 * k))
    elif kind == "seat":
        s.line([q(18, 190), q(32, 158), q(34, 140)], lt, max(1.0, 8 * k))
        s.line([q(36, 2), q(36, 232)], dk, max(1.0, 4.5 * k))                             # a tall staff
        s.line([q(37, 20), q(37, 228)], gl, max(1.0, 1.4 * k), 0.8)
        s.line([q(-18, 190), q(-22, 150), q(-10, 128)], sh, max(1.0, 8 * k))
    elif kind == "general":
        s.line([q(20, 192), q(36, 214), q(44, 250)], lt, max(1.0, 8 * k))                # the right arm raised
        s.ellipse(*q(45, 256), 4.5 * k, 5 * k, lt)
        s.line([q(-20, 192), q(-30, 160), q(-22, 136)], sh, max(1.0, 8 * k))
    elif kind == "old2":
        s.line([q(20, 192), q(34, 150), q(30, 132)], lt, max(1.0, 8 * k))
        s.line([q(31, 0), q(36, 262)], dk, max(1.0, 3.5 * k))                             # the spear
        s.poly([q(33, 262), q(39, 262), q(36, 284)], gl)
        s.line([q(-20, 192), q(-30, 156), q(-24, 128)], sh, max(1.0, 8 * k))
    elif kind == "brutus":
        s.line([q(18, 188), q(36, 206), q(46, 224)], lt, max(1.0, 8 * k))               # the sword arm, raised
        s.line([q(44, 220), q(58, 292)], gl, max(1.0, 3.2 * k))                           # the drawn sword, catching the sun
        s.line([q(42, 218), q(56, 290)], sh, max(1.0, 1.4 * k), 0.8)
        s.line([q(38, 222), q(52, 216)], dk, max(1.0, 3 * k))                             # its guard
        s.line([q(-18, 188), q(-28, 150), q(-22, 124)], sh, max(1.0, 8 * k))
    else:
        s.line([q(18, 186), q(36, 206), q(46, 240)], lt, max(1.0, 8 * k))               # the raised arm of a man speaking
        s.ellipse(*q(47, 246), 4 * k, 5 * k, lt)
        s.line([q(-18, 186), q(-22, 150), q(-12, 120)], sh, max(1.0, 9 * k))
        s.line([q(19, 182), q(38, 206)], gl, max(1.0, 1.6 * k), 0.8)
    # a rim of sun down the right side, and the feet on their bronze plinth
    s.poly([q(-26, -2), q(28, -2), q(28, 6), q(-26, 6)], dk)


def bronze(alpha, tones, seed, patina=0.0, top=None):
    """Colour a statue's silhouette as rounded bronze lit from our right: across each run of it, row by row, dark at
    its left edge, through the shade and the middle to the light and a glint near its right edge (so every limb and
    fold reads round), then streaks of green where the rain has run down old bronze. -> colour picture."""
    dk, sh, lt, gl = [col(t) for t in tones]
    md = (sh + lt) / 2
    m = alpha > 0.35
    t = np.zeros(alpha.shape, F32)
    ys = np.where(m.any(axis=1))[0]
    for yy in ys:
        row = m[yy]
        d = np.diff(np.concatenate([[0], row.astype(np.int8), [0]]))
        starts, ends = np.where(d == 1)[0], np.where(d == -1)[0]
        for a, b in zip(starts, ends):
            n = b - a
            t[yy, a:b] = (np.arange(n) + 0.5) / n
    tt = t[..., None]
    c = np.where(tt < 0.30, dk + (sh - dk) * (tt / 0.30), np.where(tt < 0.62, sh + (md - sh) * ((tt - 0.30) / 0.32),
                 np.where(tt < 0.82, md + (lt - md) * ((tt - 0.62) / 0.20), np.where(tt < 0.92, lt + (gl - lt) * ((tt - 0.82) / 0.10) * 0.8, lt))))
    if patina:
        x, y = grid(alpha.shape)
        streak = step(0.55, 0.80, noise(alpha.shape, (3, 22), seed, 3)) * np.clip(tt[..., 0] * 1.6, 0, 1) * (1 - tt[..., 0]) * 2.2
        c = c * (1 - patina * streak[..., None]) + col("#4f7a5e") * patina * streak[..., None]
    if top is not None:                                      # a little more light on what faces up (heads, shoulders)
        c = np.clip(c * (1 + 0.10 * top[..., None]), 0, 1)
    return np.clip(c, 0, 1).astype(F32)


def statue(canvas, x, y, k, kind, tones, seed, patina=0.35):
    """A bronze statue standing at (x, y): its silhouette from figure(), shaded round by bronze(), the lines of its
    folds, beard and crown over it, a darker edge round it."""
    from brush import grid as _grid
    sm = Sheet(SHAPE, ss=4)
    figure(sm, x, y, k, kind, ("#ffffff",) * 4, seed)
    _, a = sm.done()
    c = bronze(a, tones, seed, patina)
    edge = np.clip(a - blur(a, 0.7) * 0.0, 0, 1)
    rim = np.clip(a - np.minimum(np.minimum(np.roll(a, 1, 1), np.roll(a, -1, 1)), np.minimum(np.roll(a, 1, 0), np.roll(a, -1, 0))), 0, 1)
    c = c * (1 - 0.45 * rim[..., None] * (np.roll(a, -1, 1) < 0.5)[..., None])        # the edge away from the sun is darker still
    canvas.put(c, a)
    sd = Sheet(SHAPE, ss=4)
    figure_lines(sd, x, y, k, kind, tones)
    dc, da = sd.done()
    canvas.put(dc, da * (a > 0.4))


def figure_lines(s, x, y, k, kind, tones):
    """The lines over a statue's bronze: folds of the robe, the edge of the beard, the band of a crown, the belt, the
    straps; and the bright things: a sceptre's knob, the sword's blade, a spear's head."""
    dk, sh, lt, gl = tones
    q = lambda dx, h: (x + dx * k, y - h * k)
    w = max(0.6, 1.4 * k)
    if kind in ("old", "seat"):
        for fx in (-14, -5, 10):
            s.line([q(fx, 4), q(fx + 3, 70), q(fx + 1, 140)], dk, w, 0.55)
        s.line([q(-19, 150), q(19, 150)], dk, w, 0.6)                                   # the belt
        s.line([q(-9, 214), q(9, 214)], gl, w, 0.7)                                     # the crown's band
    elif kind == "new":
        s.line([q(-20, 120), q(10, 186)], dk, w * 1.4, 0.6)
        s.line([q(-6, 6), q(-2, 110)], dk, w, 0.5)
        s.line([q(14, 8), q(16, 90)], gl, w, 0.6)
    elif kind in ("old2", "general"):
        s.line([q(-20, 118), q(20, 118)], dk, w, 0.7)
        for fx in range(-18, 20, 6):
            s.line([q(fx, 92), q(fx, 116)], dk, w * 0.7, 0.6)
        s.line([q(-14, 170), q(18, 170)], dk, w, 0.5)
        if kind == "old2":
            s.poly([q(33, 262), q(39, 262), q(36, 284)], gl)
    elif kind == "brutus":
        s.line([q(44, 220), q(58, 292)], gl, max(0.8, 2.6 * k))                        # the drawn sword, catching the sun
        s.line([q(38, 222), q(52, 216)], dk, max(0.8, 2.4 * k))
        s.line([q(-16, 70), q(-12, 186)], dk, w, 0.5)
    if kind in ("old", "seat", "brutus", "old2"):
        s.line([q(-6, 200), q(0, 194), q(7, 200)], dk, w, 0.5)                          # the beard's edge


def kings_layer(seed=41):
    """The row of kings: each statue on its stone base, the broad low base in the middle (the boy's seat: a king in
    a cloak stands at the back of it, so the front of its top is clear). Old Brutus has a few scratched letters on
    his base, too small to read. -> Canvas (in the backdrop: nobody walks behind the row)."""
    c = Canvas(SHAPE)
    rng = np.random.default_rng(seed)
    tones_b = {"old": "#ddd2bc", "brutus": "#cfc2a8", "seat": "#e4d8c0", "new": "#f2ead8", "old2": "#d6caae"}
    order = sorted(range(len(KINGS)), key=lambda i: -base_box(KINGS[i])[2])
    for i in order:
        kg = KINGS[i]
        X0, X1, Z0, Z1, h = base_box(kg)
        Xm = (X0 + X1) / 2
        tone = tones_b[kg["kind"]]

        def paint(face, a, b, own, kg=kg, Xm=Xm, i=i):
            old = kg["kind"] != "new"
            if face in ("front", "side"):
                own = own * (1 - 0.13 * step(0.55, 0.9, tex(a * 5.0, b * 0.35, 80, seed + i))[..., None])          # rain marks
                damp = np.clip(1 - (b - 14) / 40.0, 0, 1) * (0.6 + 0.4 * tex(a, b, 30, seed + 20 + i))
                own = own * (1 - 0.16 * damp[..., None] * np.array([1.0, 0.95, 0.85], dtype=F32))
                if old:
                    lich = step(0.62, 0.72, tex(a, b, 14, seed + 30 + i, 3)) * step(0.45, 0.75, tex(a, b, 60, seed + 40 + i))
                    own = own * (1 - 0.35 * lich[..., None]) + col("#b8b48a") * 0.35 * lich[..., None]
            if face == "front":
                pw = kg["w"] / 2 - 9
                panel = (np.abs(a - Xm) < pw) & (b > 30) & (b < kg["h"] - 28)
                edge = panel & ((np.abs(np.abs(a - Xm) - pw) < 1.6) | (np.abs(b - 30) < 1.6) | (np.abs(b - (kg["h"] - 28)) < 1.6))
                own = np.where(edge[..., None], own * 0.80, own)
                if kg["kind"] not in ("seat",):              # a few lines cut in it, too small to read
                    top_ = kg["h"] - 40
                    lines_ = (np.abs(((top_ - b) % 9.0) - 4.5) < 1.1) & (b > top_ - 30) & (b < top_) & (np.abs(a - Xm) < pw - 6) & (tex(a * 2.5, b, 8, seed + 50 + i) > 0.4)
                    own = np.where(lines_[..., None], own * 0.72, own)
                if kg["kind"] == "brutus":                   # and scratched over them: words somebody wrote, too small to read
                    scr = (np.abs(((b - 58) % 6.0) - 3.0) < 0.8) & (b > 50) & (b < 74) & (np.abs(a - Xm + 4) < 20) & (tex(a * 3, b, 6, seed + 9) > 0.42)
                    own = np.where(scr[..., None], own * 0.62, own)
                if kg["kind"] == "seat":                     # scuffed where boys climb and sit
                    own = own * (1 - 0.12 * step(0.5, 0.8, tex(a, b, 30, seed + 12))[..., None] * np.clip((b - 50) / 60.0, 0, 1)[..., None])
            return own
        moulded(c, Xm, Z0, kg["w"], kg["d"], kg["h"], tone, seed + 10 * i, paint=paint)
        # the statue: on the middle base it stands at the back, leaving the front of the top clear
        Zs = Z1 - 30 if kg["kind"] == "seat" else (Z0 + Z1) / 2
        fx, fy = P(Xm, kg["h"], Zs)
        k = k_at(Zs) * kg["statue"] / 225.0
        new = kg["kind"] == "new"
        statue(c, fx, fy, k, kg["kind"], NEW_BRONZE if new else OLD_BRONZE, seed + i, patina=0.0 if new else 0.16)
    return c


def world_layer(seed=51):
    """The dictator's statue on the great bronze ball of the world, on a tall base. -> Canvas (a cut-out: people pass
    behind it on their way to the altar)."""
    c = Canvas(SHAPE)
    w = WORLD
    bw, bd, bh = w["base"]
    moulded(c, w["X"], w["Z"], bw, bd, bh, "#ece2cc", seed, plinth=20, crown=20)
    Zc = w["Z"] + bd / 2
    k = k_at(Zc)
    gx, gy = P(w["X"], bh + w["r"] * 0.96, Zc)
    r = w["r"] * k
    s = Sheet(SHAPE, ss=4)
    s.ellipse(gx, gy, r, r, "#4a3a22")                       # the ball: shade, then its lit side, the bands of the world
    s.ellipse(gx + r * 0.22, gy - r * 0.10, r * 0.78, r * 0.86, "#8a6a34")
    s.ellipse(gx + r * 0.38, gy - r * 0.22, r * 0.46, r * 0.52, "#c09048")
    s.line([(gx - r * 0.98, gy + r * 0.05), (gx + r * 0.98, gy - r * 0.05)], "#2e2416", max(1.0, 0.07 * r))     # the band of the middle
    s.line([(gx - r * 0.35, gy - r * 0.94), (gx - r * 0.20, gy), (gx - r * 0.34, gy + r * 0.94)], "#3a2e1c", max(1.0, 0.05 * r), 0.8)
    s.ellipse(gx + r * 0.50, gy - r * 0.40, r * 0.14, r * 0.12, "#fff0b8")                                       # the sun on it
    sc, sa = s.done()
    c.put(sc, sa)
    fx, fy = P(w["X"], bh + w["r"] * 1.9, Zc)
    statue(c, fx, fy, k * w["man"] / 225.0, "general", ("#3a2a14", "#7a5a28", "#c09040", "#ffe8a0"), seed + 2, patina=0.0)
    return c


def chariot_layer(seed=61):
    """The dictator's bronze chariot on its stone base, facing the temple's doors: we see it from behind, the open
    back of the car with its wheels and, beyond it, the four horses with their rumps and tails toward us and their
    heads high. Bigger than life, as such a gift is. -> Canvas."""
    c = Canvas(SHAPE)
    ch = CHARIOT
    bw, bd, bh = ch["base"]
    X, Z = ch["X"], ch["Z"]

    def paint(face, a, b, own):
        if face != "top":
            own = own * (1 - 0.12 * step(0.55, 0.9, tex(a * 5.0, b * 0.35, 80, seed + 3))[..., None])
            if face == "front":
                pw = bw / 2 - 16
                panel = (np.abs(a - X) < pw) & (b > 34) & (b < bh - 30)
                edge = panel & ((np.abs(np.abs(a - X) - pw) < 2.0) | (np.abs(b - 34) < 2.0) | (np.abs(b - (bh - 30)) < 2.0))
                own = np.where(edge[..., None], own * 0.80, own)
        return own
    moulded(c, X, Z, bw, bd, bh, "#ebe2cc", seed, plinth=20, crown=18, paint=paint)
    S = 1.25                                                 # bigger than life
    tones = ("#2e2414", "#5e4826", "#b08a44", "#f6dc90")
    # the four horses, side by side, seen from behind: drawn as one silhouette and shaded round, far ones first
    sm = Sheet(SHAPE, ss=4)
    Zh = Z + 270
    k = k_at(Zh) * S
    for off in (-102, -34, 34, 102):
        x0, y0 = P(X + off * S, bh, Zh)
        q = lambda dx, h: (x0 + dx * k, y0 - h * k)
        sm.poly([q(-15, 150), q(15, 150), q(12, 188), q(-11, 188)], "#ffffff")                            # the neck, going away from us, short
        sm.ellipse(*q(0, 192), 12 * k, 11 * k, "#ffffff")                                                # the back of the head, held high
        sm.poly([q(-10, 196), q(-8, 212), q(-3, 199)], "#ffffff")                                        # ears
        sm.poly([q(3, 199), q(8, 212), q(10, 196)], "#ffffff")
        for lx in (-14, 14):                                                                              # hind legs: hoof, cannon, hock, gaskin
            sgn = 1 if lx > 0 else -1
            sm.poly([q(lx - 6, 0), q(lx + 7, 0), q(lx + 5, 14), q(lx + 5, 40), q(lx + sgn * 3 + 7, 52), q(lx + sgn * 6 + 12, 100),
                     q(lx + sgn * 6 - 12, 100), q(lx + sgn * 3 - 7, 52), q(lx - 5, 40), q(lx - 5, 14)], "#ffffff")
        sm.ellipse(*q(-17, 124), 24 * k, 33 * k, "#ffffff")                                              # the two haunches of the rump
        sm.ellipse(*q(17, 124), 24 * k, 33 * k, "#ffffff")
        sm.ellipse(*q(0, 150), 32 * k, 15 * k, "#ffffff")                                                # the croup
    _, ha = sm.done()
    c.put(bronze(ha, tones, seed, 0.2), ha)
    sd = Sheet(SHAPE, ss=4)
    for off in (-102, -34, 34, 102):
        x0, y0 = P(X + off * S, bh, Zh)
        q = lambda dx, h: (x0 + dx * k, y0 - h * k)
        sd.line([q(0, 158), q(-1, 128), q(2, 96), q(-2, 66)], tones[0], max(1.0, 8 * k))                  # the tail, hanging
        sd.line([q(0, 100), q(0, 146)], tones[0], max(0.8, 1.6 * k), 0.8)                                 # the cleft between the haunches
        sd.line([q(26, 150), q(34, 118)], tones[3], max(0.8, 1.6 * k), 0.7)                               # the sun on the right haunch
    dc, da = sd.done()
    c.put(dc, da * (ha > 0.4))
    # the car: its open back toward us, its two wheels edge on, the gilt rail round it
    sm = Sheet(SHAPE, ss=4)
    Zc = Z + 110
    k = k_at(Zc) * S
    x0, y0 = P(X, bh, Zc)
    q = lambda dx, h: (x0 + dx * k, y0 - h * k)
    for wx in (-64, 64):
        sm.poly([q(wx - 6, 0), q(wx + 6, 0), q(wx + 7, 46), q(wx + 6, 92), q(wx - 6, 92), q(wx - 7, 46)], "#ffffff")
    sm.poly([q(-66, 42), q(66, 42), q(66, 50), q(-66, 50)], "#ffffff")                                    # the axle
    sm.poly([q(-52, 38), q(52, 38), q(56, 104), q(40, 118), q(-40, 118), q(-56, 104)], "#ffffff")         # the body of the car
    _, ca = sm.done()
    c.put(bronze(ca, tones, seed + 1, 0.15), ca)
    sd = Sheet(SHAPE, ss=4)
    sd.poly([q(-42, 42), q(42, 42), q(44, 100), q(-44, 100)], "#1e160e")                                 # the open back: the dark floor and inside
    sd.line([q(-56, 104), q(-40, 118), q(40, 118), q(56, 104)], tones[3], max(1.0, 3 * k))                # the gilt rail
    sd.line([q(-44, 44), q(44, 44)], tones[2], max(0.8, 2 * k), 0.8)                                     # the step at the back
    for wx in (-64, 64):
        sd.line([q(wx + 4, 6), q(wx + 4, 88)], tones[3] if wx > 0 else tones[2], max(0.8, 1.6 * k), 0.8)
    dc, da = sd.done()
    c.put(dc, da * (ca > 0.4))
    return c


def altar_layer(seed=71):
    """The great altar of Jupiter: long, of grey stone, on a step, moulded top and bottom, with a roll at each end;
    its fire has burned low (the embers and the smoke are the game's): a pan of ash and coals on top. -> Canvas."""
    c = Canvas(SHAPE)
    X0, X1 = ALTAR["X"]
    Z0, Z1 = ALTAR["Z"]
    hh = ALTAR["h"]
    grey = "#d4cab8"
    block(c, (X0 - 30, X1 + 30, Z0 - 30, Z1 + 30, 0, 18), mix(grey, "#000000", 0.05), seed)

    def die(face, a, b, own):
        if face == "front":                                  # panels with garlands carved in low relief
            span = (X1 - X0)
            t = (a - X0) / span * 4.0
            cell = t - np.floor(t)
            sag = 42 + 22 * np.sin(cell * math.pi)
            garl = (np.abs(b - (hh - sag)) < 6) & (cell > 0.06) & (cell < 0.94)
            own = np.where(garl[..., None], own * 0.80, own)
            bucr = (np.hypot((cell - 0.0) * span / 4.0, b - (hh - 36)) < 10) | (np.hypot((cell - 1.0) * span / 4.0, b - (hh - 36)) < 10)
            own = np.where(bucr[..., None], own * 0.84, own)
            own = own * (1 - 0.12 * step(0.5, 0.85, tex(a * 5.0, b * 0.5, 60, seed + 9))[..., None])
        return own
    block(c, (X0 - 12, X1 + 12, Z0 - 12, Z1 + 12, 18, 34), mix(grey, "#ffffff", 0.06), seed + 3, cell=20)
    block(c, (X0, X1, Z0, Z1, 34, hh - 20), grey, seed + 6, paint=die)
    block(c, (X0 - 10, X1 + 10, Z0 - 10, Z1 + 10, hh - 20, hh), mix(grey, "#ffffff", 0.10), seed + 9, cell=20)
    s = Sheet(SHAPE, ss=3)
    for Xe, tone_top, tone_end in ((X0 + 12, "#b9aeb4", "#958aa0"), (X1 - 12, "#f4e8d0", "#dacbb2")):      # the rolls at either end
        a0, a1 = P(Xe, hh + 12, Z0 - 6), P(Xe, hh + 12, Z1 + 6)
        k = k_at(Z0)
        s.line([a0, a1], tone_top, 24 * k)
        s.ellipse(a0[0], a0[1], 12.5 * k, 12.5 * k, tone_end)
        s.ellipse(a0[0], a0[1], 7 * k, 7 * k, "#7c7288", 0.8)
    f0, f1 = P(X0 + 120, hh + 2, (Z0 + Z1) / 2), P(X1 - 120, hh + 2, (Z0 + Z1) / 2)
    k = k_at((Z0 + Z1) / 2)
    s.ellipse((f0[0] + f1[0]) / 2, f0[1] - 1, (f1[0] - f0[0]) / 2, 9 * k, "#5a4a3c")        # the long pan of ash and coals
    s.ellipse((f0[0] + f1[0]) / 2, f0[1] - 1.5, (f1[0] - f0[0]) / 2 - 2, 6 * k, "#3a3030")
    rng = np.random.default_rng(seed)
    for i in range(16):
        ex = lerp(f0[0] + 6, f1[0] - 6, rng.random())
        s.ellipse(ex, f0[1] - 2 + rng.normal(0, 0.8), 1.4, 0.9, ["#a89c94", "#cfc6bc", "#7a6e68"][int(rng.integers(3))])      # grey ash
    for i in range(6):
        ex = lerp(f0[0] + 10, f1[0] - 10, rng.random())
        s.ellipse(ex, f0[1] - 2 + rng.normal(0, 0.6), 1.3, 0.8, mix("#ff8a30", "#ffd060", rng.random()))
    s.line([(f0[0] + 10, f0[1] - 3), (f1[0] - 30, f0[1] - 5)], "#3a2c26", 1.4)                                         # charred wood
    # a garland of laurel tied along its front for the Ides
    ga, gb = P(X0 + 14, hh - 26, Z0 - 13), P(X1 - 14, hh - 26, Z0 - 13)
    rope = [(lerp(ga[0], gb[0], t), lerp(ga[1], gb[1], t) + 10 * k * math.sin(math.pi * (t * 3 % 1)) ** 0.9) for t in np.linspace(0, 1, 40)]
    s.line(rope, "#2f4a26", max(1.0, 7 * k))
    for (px, py) in rope[::2]:
        for j in range(2):
            ang = rng.uniform(0, 2 * math.pi)
            ln = rng.uniform(1.6, 2.6)
            s.line([(px, py), (px + math.cos(ang) * ln, py + math.sin(ang) * ln)], ["#2c4a24", "#4f7a30", "#86a648"][int(rng.integers(3))], 1.0)
    for (px, py) in (ga, gb, rope[13], rope[26]):
        s.line([(px, py), (px + rng.normal(0, 0.6), py + 5)], "#c8483a", 1.0)
    sc, sa = s.done()
    c.put(sc, sa)
    return c


def hut_layer(seed=81):
    """Romulus's hut, kept as it was: small and round, walls of woven wattle daubed with clay, a steep thatch of
    reeds gone grey with age, a low doorway toward us with a timber porch post. -> Canvas."""
    c = Canvas(SHAPE)
    X, Z, r, hw, top = HUT["X"], HUT["Z"], HUT["r"], HUT["wall"], HUT["top"]
    k = k_at(Z)
    s = Sheet(SHAPE, ss=3)
    # the wall: a drum, darker toward the left; wattle courses and daub
    n = 48
    rng = np.random.default_rng(seed)
    ring = lambda h, rr: [P(X + rr * math.cos(a), h, Z - rr * math.sin(a)) for a in np.linspace(0, math.pi, n)]
    lo, hi = ring(0, r), ring(hw, r)
    for j in range(n - 1):
        a = math.pi * (j + 0.5) / (n - 1)
        lit = max(0.0, math.cos(a) * 0.9 + 0.25)                 # the right side toward the sun
        tone = mix("#6e5640", "#c49a64", lit)
        s.poly([lo[j], lo[j + 1], hi[j + 1], hi[j]], tone)
    for hh in np.arange(10, hw, 11.0):                          # the woven rods showing through the daub
        pts = ring(hh, r * 1.005)
        s.line(pts, "#5a4430", max(0.8, 1.2 * k), 0.55)
    for i in range(14):                                          # patches of daub, paler
        a = rng.uniform(0.1, 2.9)
        hh = rng.uniform(15, hw - 15)
        p = P(X + r * math.cos(a), hh, Z - r * math.sin(a))
        s.ellipse(p[0], p[1], rng.uniform(5, 12) * k, rng.uniform(3, 7) * k, mix("#b8946a", "#d8b484", max(0.0, math.cos(a))), 0.85)
    d0, d1 = P(X + 14, 0, Z - r), P(X + 70, 92, Z - r)             # the low doorway, a dark gap, and its post
    s.poly([(d0[0], d0[1]), (d1[0], d0[1]), (d1[0], d1[1]), (d0[0], d1[1])], "#2a2024")
    s.line([P(X + 8, 0, Z - r - 6), P(X + 8, 112, Z - r - 6)], "#4a3a2c", max(1.0, 7 * k))
    s.line([P(X + 76, 0, Z - r - 6), P(X + 76, 112, Z - r - 6)], "#8a6a48", max(1.0, 7 * k))
    # the thatch: a steep cone overhanging the wall, its eaves ragged
    eave = hw - 10
    er = r + 34
    cone_base = [P(X + er * math.cos(a), eave + rng.normal(0, 3), Z - er * math.sin(a) * 0.98) for a in np.linspace(-0.25, math.pi + 0.25, 40)]
    apex = P(X - 6, top, Z)
    s.poly(cone_base + [apex], "#8a7a5c")
    s.poly([p for p in cone_base[:22]] + [apex], "#b8a477")      # the half toward the sun
    for i in range(70):                                          # the reeds, in long strokes from the top
        t = rng.random()
        a = -0.2 + t * (math.pi + 0.4)
        b = P(X + er * math.cos(a), eave - rng.uniform(0, 8), Z - er * math.sin(a) * 0.98)
        lit = max(0.0, math.cos(a) * 0.8 + 0.3)
        s.line([(lerp(apex[0], b[0], 0.15), lerp(apex[1], b[1], 0.15)), b], mix("#5a4c3a", "#d8c69a", lit * rng.uniform(0.6, 1.0)), max(0.8, 1.6 * k), 0.75)
    for hh in (top - 30, top - 60):                              # two bands of rope round the top
        rr = (top - hh) / (top - eave) * er
        pts = [P(X - 6 + rr * math.cos(a), hh, Z - rr * math.sin(a)) for a in np.linspace(0, math.pi, 16)]
        s.line(pts, "#4a3c2c", max(0.8, 2 * k), 0.8)
    s.ellipse(apex[0], apex[1] + 2 * k, 6 * k, 5 * k, "#4a3c2c")
    sc, sa = s.done()
    c.put(sc, sa)
    return c


def pen_layers(seed=91):
    """The geese's pen: a low fence of woven wattle on stakes round a stone trough, its gate on the side toward the
    base standing open. -> (the back of it, for the backdrop: the far fence, the trough, the straw; the front: the
    near fence and the gate side, a cut-out the geese inside stand behind)."""
    X0, X1 = PEN["X"]
    Z0, Z1 = PEN["Z"]
    hh = PEN["h"]
    gx, g0, g1 = PEN["gate"]
    back, front = Canvas(SHAPE), Canvas(SHAPE)
    sb, sf = Sheet(SHAPE, ss=3), Sheet(SHAPE, ss=3)
    rng = np.random.default_rng(seed)
    floor = [P(X0, 0, Z0), P(X1, 0, Z0), P(X1, 0, Z1), P(X0, 0, Z1)]
    sb.poly(floor, "#c8aa6c")                                    # straw and trodden earth inside
    for i in range(300):
        a, b = rng.random(), rng.random()
        Xp, Zp = lerp(X0 + 10, X1 - 10, a), lerp(Z0 + 10, Z1 - 10, b)
        p = P(Xp, 0, Zp)
        ang = rng.uniform(0, math.pi)
        ln = rng.uniform(2, 5) * k_at(Zp)
        sb.line([p, (p[0] + math.cos(ang) * ln, p[1] + math.sin(ang) * ln * 0.3)], ["#d8c48a", "#a8905c", "#e8d8a0", "#8a7448"][int(rng.integers(4))], 1.0, 0.85)
    t0, t1 = X0 + 40, X0 + 170                                   # the trough, at the back
    tz0, tz1 = Z1 - 70, Z1 - 30
    th = 34
    sb.poly([P(t0, 0, tz0), P(t1, 0, tz0), P(t1, th, tz0), P(t0, th, tz0)], "#a8a090")
    sb.poly([P(t0, th, tz0), P(t1, th, tz0), P(t1, th, tz1), P(t0, th, tz1)], "#d4ccbc")
    sb.poly([P(t0 + 6, th, tz0 + 6), P(t1 - 6, th, tz0 + 6), P(t1 - 6, th, tz1 - 6), P(t0 + 6, th, tz1 - 6)], "#6a8a98")      # water in it
    sb.line([P(t0, 0, tz0), P(t1, 0, tz0)], "#5a5048", 1.0, 0.6)

    def fence(sheet, A, B, gaps=(), lit_side=False):
        """A run of wattle from A to B (world X, Z): a dense weave of rods between stakes every 45 cm."""
        (XA, ZA), (XB, ZB) = A, B
        L = math.hypot(XB - XA, ZB - ZA)
        n = max(2, int(L / 6))
        along = lambda t: (lerp(XA, XB, t), lerp(ZA, ZB, t))
        in_gap = lambda X, Z: any(g[0] <= (Z if XA == XB else X) <= g[1] for g in gaps)
        base_c, rod_l, rod_d = ("#9a7448", "#d0a868", "#5e4630") if lit_side else ("#6e5238", "#a0805a", "#45331f")
        # the panel, run by run so that a gap stays open
        runs, cur = [], []
        for j in range(n + 1):
            X, Z = along(j / n)
            if in_gap(X, Z):
                if len(cur) > 1:
                    runs.append(cur)
                cur = []
            else:
                cur.append((X, Z))
        if len(cur) > 1:
            runs.append(cur)
        for rn in runs:
            (X0_, Z0_), (X1_, Z1_) = rn[0], rn[-1]
            sheet.poly([P(X0_, 2, Z0_), P(X1_, 2, Z1_), P(X1_, hh, Z1_), P(X0_, hh, Z0_)], base_c)
            for hrow in np.arange(5, hh - 1, 5.0):                      # the rods, woven: light where they bow out, dark between
                pts = [P(X, hrow + 1.4 * math.sin((X + Z) / 22.0 + hrow), Z) for X, Z in rn]
                sheet.line(pts, rod_l if int(hrow / 5) % 2 else mix(rod_l, rod_d, 0.4), max(0.8, 2.6 * k_at(Z0_)), 0.9)
                sheet.line([(p[0], p[1] + max(0.6, 1.4 * k_at(Z0_))) for p in pts], rod_d, max(0.5, 0.9 * k_at(Z0_)), 0.7)
            sheet.line([P(X0_, hh, Z0_), P(X1_, hh, Z1_)], rod_l, max(0.8, 2.0 * k_at(Z0_)), 0.9)     # the top rod, catching the light
        for j in range(int(L / 45) + 1):                                 # the stakes
            X, Z = along(min(1.0, j * 45 / L))
            if in_gap(X, Z):
                continue
            sheet.line([P(X, 0, Z), P(X, hh + 9, Z)], "#3e2c1c", max(1.0, 4.5 * k_at(Z)))
            sheet.line([P(X + 2, 4, Z), P(X + 2, hh + 8, Z)], "#7a5a3a", max(0.6, 1.2 * k_at(Z)), 0.8)
    fence(sb, (X0, Z1), (X1, Z1), lit_side=True)                 # the far side (we see its inner face, toward the sun)
    fence(sb, (X0, Z0), (X0, Z1))                                # the left side (its inner face)
    fence(sf, (X0, Z0), (X1, Z0), lit_side=True)                 # the near side
    fence(sf, (X1, Z0), (X1, Z1), gaps=((g0, g1),), lit_side=True)   # the right side, the gate's gap in it
    # the gate, a hurdle of the same wattle, swung right back and standing open against the outside of the fence
    fence(sf, (X1 + 9, g1 + 4), (X1 + 15, g1 + 4 + (g1 - g0)), lit_side=True)
    for (cv, sh) in ((back, sb), (front, sf)):
        sc, sa = sh.done()
        cv.put(sc, sa)
    return back, front


def wall_layer(seed=95):
    """The parapet across the left, where the hill drops away: big squared blocks of grey tufa, a coping of
    travertine on top, worn and stained, a weed or two in its joints. -> Canvas."""
    c = Canvas(SHAPE)
    Zw, hw, t = WALL["Z"], WALL["h"], WALL["t"]
    Xe = wall_end_X()

    def paint(face, a, b, own):
        if face == "front":
            tone, jm, _ = courses(a, b, long=110, high=48, seed=seed, joint=1.8, ppc=k_at(Zw))
            own = own * (1 + (tone[..., None] - 0.5) * 0.14) * (1 - 0.35 * jm[..., None])
            own = own * (1 - 0.16 * np.clip(1 - b / 30.0, 0, 1)[..., None] * step(0.3, 0.7, tex(a, b, 60, seed + 3))[..., None])
        return own
    block(c, (-2400.0, Xe, Zw, Zw + t, 0, hw - 14), "#c8b898", seed, paint=paint, cell=60)
    block(c, (-2410.0, Xe + 8, Zw - 8, Zw + t + 8, hw - 14, hw), "#ece2cc", seed + 4, cell=30)
    s = Sheet(SHAPE)
    rng = np.random.default_rng(seed)
    for i in range(7):
        Xp = rng.uniform(-1800, Xe - 40)
        p = P(Xp, 0, Zw - 1)
        for j in range(7):
            a = math.pi * rng.uniform(0.15, 0.85)
            l = rng.uniform(4, 9)
            s.line([(p[0] + rng.normal(0, 1.2), p[1]), (p[0] + math.cos(a) * l * 0.8, p[1] - math.sin(a) * l)], ["#55662e", "#7f9440", "#b4bf60"][int(rng.random() ** 1.4 * 3)], 1.0)
    sc, sa = s.done()
    c.put(sc, sa)
    return c


def wall_end_X():
    """Where the parapet across the left ends, at the first king's base."""
    X0, X1, Z0, Z1, h = base_box(KINGS[0])
    return X0 - 30.0


def tablet_posts():
    """The posts of the tablets: (X of the middle, Z of the front) each, nearest first."""
    return [(TABLETS["X"], lerp(TABLETS["Z"][0], TABLETS["Z"][1], i / (TABLETS["n"] - 1))) for i in range(TABLETS["n"])]


POST = (40.0, 40.0, 84.0)                                    # a post: width, depth, height (the sloping head on it is wider)
DESK = (70.0, 52.0, 30.0)                                    # the sloping head: width, depth, how much higher its back is


def tablets_layer(seed=97):
    """At the front, bottom right: a row of short stone posts running away from us, each with a sloping head like a
    reading desk, and fixed on the slope a bronze tablet, the laws and treaties and decrees of the Roman People, in
    lines of letters far too small to read. The slopes face the gate, so whoever comes in can read them; the low sun
    is on them. -> Canvas (people pass behind it)."""
    c = Canvas(SHAPE)
    w, d, h = POST
    dw, dd, rise = DESK
    rng = np.random.default_rng(seed)
    for i, (Xp, Zp) in reversed(list(enumerate(tablet_posts()))):
        def paint(face, a, b, own, i=i):
            if face != "top":
                own = own * (1 - 0.14 * step(0.5, 0.85, tex(a * 4.0, b * 0.5, 50, seed + i))[..., None])
                own = own * (1 - 0.20 * np.clip(1 - b / 16.0, 0, 1)[..., None])
                lich = step(0.62, 0.72, tex(a, b, 10, seed + 30 + i, 3)) * step(0.45, 0.75, tex(a, b, 40, seed + 40 + i))
                own = own * (1 - 0.3 * lich[..., None]) + col("#b8b48a") * 0.3 * lich[..., None]
            return own
        Zm = Zp + d / 2
        block(c, (Xp - w / 2 - 5, Xp + w / 2 + 5, Zm - d / 2 - 5, Zm + d / 2 + 5, 0, 10), "#cfc2a8", seed + i, cell=20)
        block(c, (Xp - w / 2, Xp + w / 2, Zm - d / 2, Zm + d / 2, 10, h), "#d9cdb4", seed + i + 3, cell=30, paint=paint)
        # the sloping head: its two sides and its front edge in stone, the slope itself covered by the bronze tablet
        f0, f1 = Zm - dd / 2, Zm + dd / 2
        s = Sheet(SHAPE, ss=4)
        k = k_at(Zm)
        side_l = [P(Xp - dw / 2, h, f0), P(Xp - dw / 2, h, f1), P(Xp - dw / 2, h + 8 + rise, f1), P(Xp - dw / 2, h + 8, f0)]
        s.poly(side_l, "#a89a8c")
        s.poly([P(Xp - dw / 2, h, f0), P(Xp + dw / 2, h, f0), P(Xp + dw / 2, h + 8, f0), P(Xp - dw / 2, h + 8, f0)], "#e2d6bc")     # its front edge
        slope = [P(Xp - dw / 2, h + 8, f0), P(Xp + dw / 2, h + 8, f0), P(Xp + dw / 2, h + 8 + rise, f1), P(Xp - dw / 2, h + 8 + rise, f1)]
        s.poly(slope, "#d8ccb2")
        m_ = 4.0
        tab = [P(Xp - dw / 2 + m_, h + 9, f0 + m_ * 0.7), P(Xp + dw / 2 - m_, h + 9, f0 + m_ * 0.7), P(Xp + dw / 2 - m_, h + 7 + rise, f1 - m_ * 0.7), P(Xp - dw / 2 + m_, h + 7 + rise, f1 - m_ * 0.7)]
        s.poly(tab, "#7a6234")                                                    # the bronze, warm in the sun, a little green with age
        inner = [P(Xp - dw / 2 + m_ + 3, h + 10, f0 + 4), P(Xp + dw / 2 - m_ - 3, h + 10, f0 + 4), P(Xp + dw / 2 - m_ - 3, h + 6 + rise, f1 - 5), P(Xp - dw / 2 + m_ + 3, h + 6 + rise, f1 - 5)]
        s.poly(inner, "#9a7e46")
        s.poly([inner[0], (lerp(inner[0][0], inner[3][0], 0.5), lerp(inner[0][1], inner[3][1], 0.5)), (lerp(inner[0][0], inner[3][0], 0.5) + 2, lerp(inner[0][1], inner[3][1], 0.5)), inner[0]], "#6a8a70", 0.5)
        s.line([tab[0], tab[1]], "#f4dc90", max(0.8, 1.4 * k))                     # its lower rim in the sun
        s.line([tab[1], tab[2]], "#e8c878", max(0.8, 1.2 * k))
        s.line([tab[3], tab[0]], "#4a3a20", max(0.8, 1.2 * k))
        for r_ in range(1, 8):                                                     # lines of letters, too small to read
            t = r_ / 8.0
            za = lerp(f0 + 6, f1 - 6, t)
            ha = lerp(h + 10, h + 6 + rise, t)
            xx = Xp - dw / 2 + m_ + 6
            while xx < Xp + dw / 2 - m_ - 6:
                run = rng.uniform(3, 9)
                s.line([P(xx, ha, za), P(min(Xp + dw / 2 - m_ - 6, xx + run), ha, za)], "#4e3c1e", max(0.6, 0.9 * k), 0.8)
                xx += run + rng.uniform(1.5, 3)
        for (xx, hh_, zz) in ((Xp - dw / 2 + m_ + 2, h + 10, f0 + 3), (Xp + dw / 2 - m_ - 2, h + 10, f0 + 3), (Xp - dw / 2 + m_ + 2, h + 6 + rise, f1 - 4), (Xp + dw / 2 - m_ - 2, h + 6 + rise, f1 - 4)):
            p = P(xx, hh_, zz)
            s.ellipse(p[0], p[1], max(0.8, 1.4 * k), max(0.6, 1.0 * k), "#f0d080")                # the nails that hold it
        sc, sa = s.done()
        c.put(sc, sa)
    return c


# ---------------------------------------------------------------- what throws shadows on the paving (world cm)
def ground_solids():
    S = []
    for kg in KINGS:
        X0, X1, Z0, Z1, h = base_box(kg)
        S.append(("box", X0 - 7, X1 + 7, Z0 - 7, Z1 + 7, 0, h))
        Zs = Z1 - 30 if kg["kind"] == "seat" else (Z0 + Z1) / 2
        S.append(("cyl", (X0 + X1) / 2, Zs, 26.0, h, h + kg["statue"] * 0.85))
    w = WORLD
    bw, bd, bh = w["base"]
    S += [("box", w["X"] - bw / 2 - 6, w["X"] + bw / 2 + 6, w["Z"] - 6, w["Z"] + bd + 6, 0, bh), ("cyl", w["X"], w["Z"] + bd / 2, w["r"], bh, bh + 2 * w["r"]),
          ("cyl", w["X"], w["Z"] + bd / 2, 22.0, bh + 2 * w["r"], bh + 2 * w["r"] + w["man"] * 0.9)]
    ch = CHARIOT
    bw, bd, bh = ch["base"]
    S += [("box", ch["X"] - bw / 2 - 6, ch["X"] + bw / 2 + 6, ch["Z"] - 6, ch["Z"] + bd + 6, 0, bh), ("box", ch["X"] - 120, ch["X"] + 120, ch["Z"] + 60, ch["Z"] + 380, bh, bh + 200)]
    X0, X1 = ALTAR["X"]
    Z0, Z1 = ALTAR["Z"]
    S += [("box", X0 - 30, X1 + 30, Z0 - 30, Z1 + 30, 0, 18), ("box", X0 - 10, X1 + 10, Z0 - 10, Z1 + 10, 18, ALTAR["h"] + 10)]
    S += [("cyl", HUT["X"], HUT["Z"], HUT["r"], 0, HUT["wall"]), ("cyl", HUT["X"], HUT["Z"], HUT["r"] * 0.7, HUT["wall"], (HUT["wall"] + HUT["top"]) / 2),
          ("cyl", HUT["X"], HUT["Z"], HUT["r"] * 0.3, HUT["wall"], HUT["top"] - 20)]
    X0, X1 = PEN["X"]
    Z0, Z1 = PEN["Z"]
    hh = PEN["h"]
    S += [("box", X0, X1, Z0 - 3, Z0 + 3, 0, hh), ("box", X0, X1, Z1 - 3, Z1 + 3, 0, hh), ("box", X0 - 3, X0 + 3, Z0, Z1, 0, hh),
          ("box", X1 - 3, X1 + 3, Z0, PEN["gate"][1], 0, hh), ("box", X1 - 3, X1 + 3, PEN["gate"][2], Z1, 0, hh)]
    S += [("box", -2410.0, wall_end_X() + 8, WALL["Z"] - 8, WALL["Z"] + WALL["t"] + 8, 0, WALL["h"])]
    S += [("box", 380.0, 520.0, 690.0, 830.0, 0, 620.0), ("box", -490.0, -350.0, 690.0, 830.0, 0, 620.0)]   # the gate's piers, behind us
    w, d, h = POST
    for Xp, Zp in tablet_posts():
        S.append(("box", Xp - w / 2 - 5, Xp + w / 2 + 5, Zp - 5, Zp + d + 5, 0, h))
        S.append(("box", Xp - DESK[0] / 2, Xp + DESK[0] / 2, Zp + d / 2 - DESK[1] / 2, Zp + d / 2 + DESK[1] / 2, h, h + 8 + DESK[2] * 0.6))
    return S

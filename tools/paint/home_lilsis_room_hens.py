"""Chickens for Little Sister's room (home_lilsis_room.py): the stuffed ones, the drawn ones, and the lettering.

    hen(p, L, P, h, kind, face)          a stuffed chicken sitting at P in the room, seen in profile, lit by the room's lamps
    flat_hen(card, x, y, s, ...)         a chicken drawn flat on a Card: for her crayon drawings, the chart, the quilt, felt
    stroke_word(card, ...)               crayon capitals (signs seen large)
    tiny_word(p, L, ...)                 capitals 7 pixels high, set pixel by pixel (signs seen small)

Every design here is our own: plain farmyard hens, nothing from any toy line, book or film."""

import math

import numpy as np

from home_lilsis_room_kit import col, mix

RED = (0.88, 0.14, 0.12)
BEAK = (0.98, 0.66, 0.14)
INK = (0.07, 0.05, 0.08)

KINDS = {
    "white": dict(body=(0.97, 0.96, 0.91), wing=(0.86, 0.85, 0.83), tail=(0.90, 0.89, 0.87)),
    "buff": dict(body=(0.93, 0.66, 0.32), wing=(0.80, 0.50, 0.20), tail=(0.68, 0.40, 0.15)),
    "brown": dict(body=(0.60, 0.34, 0.18), wing=(0.47, 0.25, 0.13), tail=(0.35, 0.19, 0.11)),
    "black": dict(body=(0.19, 0.18, 0.25), wing=(0.30, 0.29, 0.40), tail=(0.13, 0.22, 0.22)),
    "grey": dict(body=(0.68, 0.70, 0.80), wing=(0.55, 0.57, 0.70), tail=(0.46, 0.48, 0.62)),
    "speckled": dict(body=(0.95, 0.94, 0.90), wing=(0.84, 0.83, 0.82), tail=(0.20, 0.19, 0.25), specks=(0.13, 0.12, 0.17)),
    "dotty": dict(body=(0.24, 0.23, 0.31), wing=(0.33, 0.32, 0.42), tail=(0.16, 0.15, 0.21), specks=(0.96, 0.96, 0.93)),
    "calico": dict(body=(0.98, 0.60, 0.70), wing=(0.99, 0.84, 0.40), tail=(0.50, 0.78, 0.90), specks=(0.99, 0.96, 0.90)),
    "chick": dict(body=(1.00, 0.86, 0.26), wing=(0.98, 0.72, 0.16), tail=None),
    "rooster": dict(body=(0.76, 0.27, 0.13), wing=(0.98, 0.66, 0.16), tail=None, hackle=(0.99, 0.80, 0.30)),
    "snowrooster": dict(body=(0.96, 0.95, 0.90), wing=(0.84, 0.84, 0.86), tail=None, hackle=(0.99, 0.86, 0.50)),
}
PLUMES = [(0.08, 0.44, 0.44), (0.16, 0.30, 0.66), (0.20, 0.56, 0.28), (0.52, 0.24, 0.62), (0.88, 0.24, 0.16)]


def _specks(color, seed=0.0, dens=0.55, size=8.0):
    c = col(color)
    def f(u, v, a):
        m = (np.sin(u * size + 1.3 + seed) * np.sin(v * (size + 2.0) + 0.7 + seed * 1.7) + 0.35 * np.sin((u + v) * size * 1.9 + seed)) > dens
        return np.where(m[..., None], c, a)
    return f


def hen(p, L, P, h, kind="white", face=1, keep=0.82, fine=False, gain=1.0, lean=0.0, outline=0.85, seed=0.0, feet=True):
    """A stuffed chicken, sitting, in profile. P = the place its seat rests; h = its height to the top of the comb (cm);
    face = +1 looking to the right of the picture, -1 to the left."""
    K = KINDS[kind]
    R, B, f = p.R, p.B, float(face)
    k = p.k(P)
    px = h * k                                                # how tall it is in the picture
    def at(dx, dy, dz=0.0):
        s_ = dx * f + lean * dy
        return (P[0] + (R[0] * s_ + B[0] * dz) * h, P[1] + dy * h, P[2] + (R[2] * s_ + B[2] * dz) * h)
    chick = kind == "chick"
    cock = "rooster" in kind
    body, wing, tail = K["body"], K["wing"], K.get("tail")
    sp = _specks(K["specks"], seed, 0.50 if kind != "calico" else 0.62, 8.0 if px > 30 else 6.0) if "specks" in K else None
    # every part: (place, radius, color, sx, sy, rot, flat, spots)
    parts = []
    if chick:
        parts += [((-0.02, 0.30), 0.30, body, 1.05, 1.0, 0, 0.05, None), ((0.10, 0.67), 0.235, body, 1.0, 1.0, 0, 0.05, None)]
    else:
        if tail is not None:
            for (dx, dy, rr, ang) in ((-0.38, 0.40, 0.125, -1.02), (-0.40, 0.52, 0.145, -0.62), (-0.34, 0.62, 0.13, -0.26)):
                parts.append(((dx, dy), rr, tail, 0.46, 1.0, ang * f, 0.55, None))
        parts += [((-0.05, 0.29), 0.29, body, 1.20, 0.98, 0, 0.05, sp), ((0.13, 0.36), 0.215, body, 1.0, 1.0, 0, 0.05, sp),
                  ((0.20, 0.53), 0.135, body, 1.0, 1.1, 0, 0.1, None), ((0.25, 0.70), 0.148, body, 1.0, 1.0, 0, 0.05, None)]
    o = outline / max(k, 1e-3)                                # the dark edge, in centimetres
    dark = (0.045, 0.035, 0.055)
    kw = dict(keep=keep, fine=fine)
    plume_pts = []
    if cock:                                                  # the magnificent tail: five felt plumes, arching up and over
        for i in range(5):
            p0, p1, p2 = (-0.26, 0.40 + 0.035 * i), (-0.40 - 0.07 * i, 1.04 - 0.08 * i), (-0.74 - 0.03 * i, 0.80 - 0.15 * i)
            pts = []
            for j in range(9):
                t = j / 8.0
                pts.append(at((1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * p1[1] + t * t * p2[1], -0.02))
            plume_pts.append(pts)
    comb = [((0.19, 0.855), 0.052), ((0.265, 0.885), 0.06), ((0.335, 0.85), 0.046)] if not cock else [((0.15, 0.86), 0.06), ((0.225, 0.91), 0.072), ((0.305, 0.905), 0.068), ((0.37, 0.855), 0.05)]
    wattle = [((0.355, 0.575), 0.046)] if not cock else [((0.35, 0.56), 0.055), ((0.30, 0.52), 0.05)]
    # ---- the dark edge first, under everything
    if outline:
        for pts in plume_pts:
            p.path(L, pts, dark, 0.085 * h + 2 * o, 1.0, fine=fine, keep=keep)
        for (c, r, cc, sx, sy, rot, flat, spots) in parts:
            p.ball(L, at(*c), r * h + o, dark, sx=(r * h * sx + o) / (r * h + o), sy=(r * h * sy + o) / (r * h + o), rot=rot, **kw)
        if not chick:
            for (c, r) in comb + wattle:
                p.ball(L, at(*c), r * h + o * 0.8, dark, **kw)
    # ---- the plumes, far ones first
    for i, pts in enumerate(plume_pts):
        cc = PLUMES[(i + int(seed)) % len(PLUMES)]
        for j in range(len(pts) - 1):
            p.seg(L, pts[j], pts[j + 1], cc, 0.085 * h * (1 - 0.45 * j / 8.0), 1.0, fine=fine, lit=B, keep=keep, gain=gain * 1.25)
    # ---- comb and wattle (felt), behind the head
    if not chick:
        for (c, r) in comb:
            p.ball(L, at(*c), r * h, RED, flat=0.5, gain=gain * 1.15, **kw)
    # ---- body
    for (c, r, cc, sx, sy, rot, flat, spots) in parts:
        p.ball(L, at(*c), r * h, cc, sx=sx, sy=sy, rot=rot, flat=flat, spots=spots, gain=gain, **kw)
    if cock:                                                  # the hackle: a golden collar
        p.ball(L, at(0.17, 0.50, 0.03), 0.165 * h, K["hackle"], sx=0.95, sy=1.12, flat=0.25, gain=gain, **kw)
        p.ball(L, at(0.25, 0.70), 0.148 * h, body, gain=gain, **kw)
    if not chick:
        for (c, r) in wattle:
            p.ball(L, at(c[0], c[1], 0.05), r * h, RED, sy=1.25, flat=0.4, gain=gain * 1.15, **kw)
    # ---- wing
    wr = -0.36 * f
    if chick:
        p.ball(L, at(-0.07, 0.31, 0.1), 0.14 * h, wing, sx=1.2, sy=0.72, rot=wr, flat=0.35, gain=gain, **kw)
    else:
        if outline and px > 16:
            p.ball(L, at(-0.09, 0.30, 0.08), 0.178 * h + o * 0.5, mix(wing, dark, 0.55), sx=1.28, sy=0.80, rot=wr, flat=0.5, gain=gain, **kw)
        p.ball(L, at(-0.085, 0.305, 0.09), 0.17 * h, wing, sx=1.28, sy=0.78, rot=wr, flat=0.35, spots=sp, gain=gain, **kw)
    # ---- beak, eye
    big = max(1.0, 24.0 / max(px, 1.0))                       # small ones get a beak one can still see
    hx, hy = (0.25, 0.70) if not chick else (0.10, 0.67)
    hr = 0.148 if not chick else 0.235
    b0, b1, tip = at(hx + hr * 0.82, hy + 0.045 * big, 0.02), at(hx + hr * 0.82, hy - 0.05 * big, 0.02), at(hx + hr * 0.82 + 0.13 * big, hy - 0.012, 0.02)
    if outline and px > 20:
        ol = 0.03
        p.poly3(L, [at(hx + hr * 0.7, hy + 0.045 * big + ol, 0.02), at(hx + hr * 0.7, hy - 0.05 * big - ol, 0.02), at(hx + hr * 0.82 + 0.13 * big + ol * 1.6, hy - 0.012, 0.02)], dark, fine=fine, keep=keep)
    p.poly3(L, [b0, b1, tip], BEAK, fine=fine, keep=keep, lit=B, gain=gain * 1.3)
    ex, ey = (hx + hr * 0.36, hy + hr * 0.2)
    p.dot(L, at(ex, ey, 0.05), 0.024 * h * (1.2 if chick else 1.0), INK, fine=fine, keep=keep, min_px=0.75)
    if px > 34:                                               # big enough for a glint in the eye
        p.dot(L, at(ex + 0.008, ey + 0.01, 0.06), 0.008 * h, (0.9, 0.9, 0.9), fine=fine, keep=keep, min_px=0.4)
    # ---- felt feet stick out in front
    if feet:
        for (dx, dz) in ((0.10, 0.10), (0.24, 0.07)):
            p.ball(L, at(dx, 0.035, dz), 0.062 * h, BEAK, sx=1.55, sy=0.55, flat=0.5, gain=gain * 1.1, **kw)
    return at


# ---------------------------------------------------------------- chickens drawn flat (crayon, felt, cloth)
def flat_hen(c, x, y, s, body=(0.97, 0.96, 0.92), face=1, kind="hen", wing=None, tail=None, legs=True, edge=None, edge_w=None,
             crest=False, boots=False, specks=None, seed=0, comb=RED, beak=BEAK, eye=INK):
    """A chicken on a Card. (x, y) = where it stands (the middle of its feet); s = its height (card cm).
    kind: "hen", "rooster", "chick", "sitting" (a hen on her eggs: no legs)."""
    f = face
    r = np.random.default_rng(seed)
    wing = mix(body, (0, 0, 0), 0.16) if wing is None else wing
    tail = mix(body, (0, 0, 0), 0.22) if tail is None else tail
    leg_h = 0.20 * s if (legs and kind != "sitting") else 0.0
    by = y - leg_h                                             # the underside of the body
    def P_(dx, dy):
        return (x + f * dx * s, by - dy * s)
    shapes = []                                                # (what, args) in painting order, so that an edge can go under them all
    if kind == "chick":
        shapes += [("disc", P_(-0.02, 0.26), 0.27 * s, 0.25 * s, body), ("disc", P_(0.10, 0.60), 0.20 * s, 0.20 * s, body)]
    else:
        if kind == "rooster":
            cols = PLUMES
            for i in range(4):
                p0, p1, p2 = (-0.20, 0.36 + 0.03 * i), (-0.34 - 0.07 * i, 0.98 - 0.07 * i), (-0.66 - 0.02 * i, 0.74 - 0.15 * i)
                pts = [P_((1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * p1[1] + t * t * p2[1]) for t in np.linspace(0, 1, 9)]
                shapes.append(("line", pts, 0.085 * s, cols[(i + seed) % len(cols)]))
        else:
            shapes.append(("poly", [P_(-0.20, 0.42), P_(-0.50, 0.72), P_(-0.52, 0.52), P_(-0.56, 0.36), P_(-0.24, 0.22)], tail))
        shapes += [("disc", P_(-0.04, 0.27), 0.31 * s, 0.25 * s, body), ("disc", P_(0.14, 0.34), 0.20 * s, 0.20 * s, body),
                   ("poly", [P_(0.06, 0.40), P_(0.16, 0.66), P_(0.34, 0.62), P_(0.30, 0.36)], body), ("disc", P_(0.24, 0.66), 0.135 * s, 0.135 * s, body)]
    if edge is not None:                                       # a crayon line round the whole bird
        ew = edge_w or 0.06 * s
        for sh in shapes:
            if sh[0] == "disc":
                c.disc(sh[1][0], sh[1][1], sh[2] + ew, edge, sh[3] + ew)
            elif sh[0] == "poly":
                c.poly(sh[1], edge); c.line(sh[1] + [sh[1][0]], edge, ew * 2)
            else:
                c.line(sh[1], edge, sh[2] + ew * 2)
    if kind != "chick":                                        # comb and wattle first: the head overlaps their roots
        hx, hy = P_(0.24, 0.66)
        n = 4 if kind == "rooster" else 3
        k_ = 1.3 if kind == "rooster" else 1.0
        for i in range(n):
            u = (i - (n - 1) / 2.0)
            c.disc(hx + f * u * 0.075 * s * k_, hy - (0.145 + 0.035 * k_ - abs(u) * 0.02) * s, 0.055 * s * k_, comb)
        c.disc(hx + f * 0.10 * s, hy + 0.13 * s * k_, 0.045 * s * k_, comb, 0.06 * s * k_)
    for sh in shapes:
        if sh[0] == "disc":
            c.disc(sh[1][0], sh[1][1], sh[2], sh[4], sh[3])
        elif sh[0] == "poly":
            c.poly(sh[1], sh[2])
        else:
            c.line(sh[1], sh[3], sh[2])
    if specks is not None and kind != "chick":
        for _ in range(int(16)):
            a, rr = r.random() * 6.28, r.random() ** 0.5
            c.disc(x + f * (-0.04) * s + math.cos(a) * rr * 0.27 * s, by - 0.27 * s + math.sin(a) * rr * 0.21 * s, 0.028 * s, specks)
    if crest and kind != "chick":
        hx, hy = P_(0.24, 0.66)
        c.disc(hx - f * 0.02 * s, hy - 0.16 * s, 0.10 * s, mix(body, (1, 1, 1), 0.3))
    # wing
    if kind == "chick":
        c.disc(*P_(-0.06, 0.26), 0.12 * s, wing, 0.09 * s)
        hx, hy = P_(0.10, 0.60)
        c.poly([(hx + f * 0.17 * s, hy - 0.035 * s), (hx + f * 0.17 * s, hy + 0.05 * s), (hx + f * 0.30 * s, hy + 0.01 * s)], beak)
        c.disc(hx + f * 0.07 * s, hy - 0.04 * s, 0.030 * s, eye)
    else:
        w0 = P_(-0.08, 0.28)
        c.poly([P_(0.06, 0.36), P_(-0.10, 0.40), P_(-0.28, 0.26), P_(-0.14, 0.15), P_(0.02, 0.20)], wing)
        hx, hy = P_(0.24, 0.66)
        c.poly([(hx + f * 0.115 * s, hy - 0.05 * s), (hx + f * 0.115 * s, hy + 0.045 * s), (hx + f * 0.27 * s, hy + 0.0 * s)], beak)
        c.disc(hx + f * 0.045 * s, hy - 0.03 * s, 0.026 * s, eye)
    if leg_h:
        for dx in (-0.02, 0.12):
            lx = x + f * dx * s
            if boots:
                c.rect(lx - 0.035 * s, by - 0.01 * s, lx + 0.035 * s, y, boots); c.rect(lx - 0.035 * s, y - 0.045 * s, lx + f * 0.09 * s if f > 0 else lx + 0.035 * s, y, boots) if f > 0 else c.rect(lx - 0.09 * s, y - 0.045 * s, lx + 0.035 * s, y, boots)
            else:
                c.line([(lx, by - 0.02 * s), (lx, y)], beak, max(0.03 * s, 0.25))
                c.line([(lx - f * 0.05 * s, y), (lx + f * 0.09 * s, y)], beak, max(0.03 * s, 0.25))


def egg(c, x, y, rx, color, stripe=None, dots=None):
    """An egg standing on its round end, on a Card: (x, y) its middle."""
    ry = rx * 1.3
    pts = []
    for a in np.linspace(0, 6.2832, 28, endpoint=False):
        k = 1.0 - 0.16 * math.sin(a)                           # narrower at the top
        pts.append((x + math.cos(a) * rx * k, y + math.sin(a) * ry))
    c.poly(pts, color)
    if stripe is not None:
        c.line([(x - rx * 0.86, y + ry * 0.1), (x - rx * 0.4, y - ry * 0.12), (x, y + ry * 0.1), (x + rx * 0.4, y - ry * 0.12), (x + rx * 0.86, y + ry * 0.1)], stripe, rx * 0.22)
    if dots is not None:
        for (dx, dy) in ((-0.4, 0.5), (0.3, 0.55), (0.0, -0.5), (-0.35, -0.3), (0.4, -0.25)):
            c.disc(x + dx * rx, y + dy * ry, rx * 0.13, dots)


# ---------------------------------------------------------------- lettering
STROKES = {
    "B": [[(0, 6), (0, 0), (2.5, 0), (3.6, 0.8), (3.6, 2.2), (2.6, 3), (0, 3)], [(2.6, 3), (3.9, 3.8), (3.9, 5.2), (2.8, 6), (0, 6)]],
    "C": [[(3.8, 1.1), (2.7, 0), (1.3, 0), (0, 1.4), (0, 4.6), (1.3, 6), (2.7, 6), (3.8, 4.9)]],
    "D": [[(0, 0), (0, 6), (2.3, 6), (3.8, 4.6), (3.8, 1.4), (2.3, 0), (0, 0)]],
    "E": [[(3.6, 0), (0, 0), (0, 6), (3.7, 6)], [(0, 3), (2.8, 3)]],
    "G": [[(3.8, 1.1), (2.7, 0), (1.3, 0), (0, 1.4), (0, 4.6), (1.3, 6), (2.8, 6), (3.9, 5), (3.9, 3.3), (2.1, 3.3)]],
    "H": [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3), (4, 3)]],
    "I": [[(2, 0), (2, 6)], [(0.7, 0), (3.3, 0)], [(0.7, 6), (3.3, 6)]],
    "K": [[(0, 0), (0, 6)], [(3.8, 0), (0, 3.5)], [(1.4, 2.3), (4, 6)]],
    "N": [[(0, 6), (0, 0), (4, 6), (4, 0)]],
    "O": [[(2, 0), (0.7, 0.7), (0, 3), (0.7, 5.3), (2, 6), (3.3, 5.3), (4, 3), (3.3, 0.7), (2, 0)]],
    "R": [[(0, 6), (0, 0), (2.6, 0), (3.7, 0.8), (3.7, 2.3), (2.6, 3.1), (0, 3.1)], [(1.8, 3.1), (3.9, 6)]],
    "S": [[(3.7, 1.0), (2.7, 0), (1.3, 0), (0.2, 0.9), (0.2, 2.0), (1.2, 2.8), (2.8, 3.2), (3.8, 4.0), (3.8, 5.1), (2.8, 6), (1.2, 6), (0.1, 5.0)]],
    "T": [[(0, 0), (4, 0)], [(2, 0), (2, 6)]],
    "U": [[(0, 0), (0, 4.6), (1.3, 6), (2.7, 6), (4, 4.6), (4, 0)]],
    "V": [[(0, 0), (2, 6), (4, 0)]],
}


def stroke_word(c, text, x0, y0, lh, lw, gap, inks, k0=0, w_cm=1.75, seed=4, wobble=1.0):
    """Crayon capitals on a Card, by somebody who is seven: each letter its own size, lean and crayon. -> the x where it ended."""
    r = np.random.default_rng(seed)
    x = x0
    for i, ch in enumerate(text):
        if ch == " ":
            x += lw * 0.75
            continue
        sc = 1 + r.normal(0, 0.035) * wobble
        dy = r.normal(0, 0.036 * lh) * wobble
        lean = r.normal(0, 0.05) * wobble
        for st in STROKES[ch]:
            pts = [(x + (px / 4.0) * lw * sc + (6 - py) / 6.0 * lean * lh, y0 + dy + (py / 6.0) * lh * sc) for px, py in st]
            c.line(pts, inks[(k0 + i) % len(inks)], w_cm)
        x += lw * sc + gap
    return x


BITS = {  # capitals 7 pixels high, for signs that are small in the picture and must still be read
    "R": ["XXX.", "X..X", "X..X", "XXX.", "X.X.", "X..X", "X..X"],
    "E": ["XXXX", "X...", "X...", "XXX.", "X...", "X...", "XXXX"],
    "S": [".XXX", "X...", "X...", ".XX.", "...X", "...X", "XXX."],
    "V": ["X...X", "X...X", "X...X", ".X.X.", ".X.X.", "..X..", "..X.."],
    "D": ["XXX.", "X..X", "X..X", "X..X", "X..X", "X..X", "XXX."],
    "C": [".XXX", "X...", "X...", "X...", "X...", "X...", ".XXX"],
    "H": ["X..X", "X..X", "X..X", "XXXX", "X..X", "X..X", "X..X"],
    "I": ["XXX", ".X.", ".X.", ".X.", ".X.", ".X.", "XXX"],
    "K": ["X..X", "X.X.", "XX..", "X...", "XX..", "X.X.", "X..X"],
    "N": ["X...X", "XX..X", "XX..X", "X.X.X", "X..XX", "X..XX", "X...X"],
    "O": [".XX.", "X..X", "X..X", "X..X", "X..X", "X..X", ".XX."],
    "U": ["X..X", "X..X", "X..X", "X..X", "X..X", "X..X", ".XX."],
    "T": ["XXXXX", "..X..", "..X..", "..X..", "..X..", "..X..", "..X.."],
    "G": [".XXX", "X...", "X...", "X.XX", "X..X", "X..X", ".XXX"],
    "B": ["XXX.", "X..X", "X..X", "XXX.", "X..X", "X..X", "XXX."],
    "M": ["X...X", "XX.XX", "X.X.X", "X.X.X", "X...X", "X...X", "X...X"],
    "Y": ["X...X", "X...X", ".X.X.", "..X..", "..X..", "..X..", "..X.."],
}


def tiny_width(text, gap=1, space=3):
    return sum((len(BITS[ch][0]) + gap) if ch != " " else space for ch in text) - gap


def tiny_word(layer, text, x, y, inks, gap=1, space=3, scale=1, fine=True, alpha=1.0):
    """Set capitals pixel by pixel on a layer's fine sheet (so the brush never touches them). (x, y) = the top left pixel.
    `inks`: one color, or a list to go through letter by letter. -> the x after the last letter."""
    inks = [inks] if not isinstance(inks, list) else inks
    c, a = (layer.fc, layer.fa) if fine else (layer.c, layer.a)
    h, w = a.shape
    n = 0
    x = int(round(x)); y = int(round(y))
    for ch in text:
        if ch == " ":
            x += space * scale
            continue
        ink = col(inks[n % len(inks)])
        n += 1
        rows = BITS[ch]
        for j, row in enumerate(rows):
            for i, bit in enumerate(row):
                if bit == "X":
                    y0, x0 = y + j * scale, x + i * scale
                    if 0 <= y0 < h - scale and 0 <= x0 < w - scale:
                        c[y0:y0 + scale, x0:x0 + scale] = c[y0:y0 + scale, x0:x0 + scale] * (1 - alpha) + ink * alpha
                        a[y0:y0 + scale, x0:x0 + scale] = a[y0:y0 + scale, x0:x0 + scale] * (1 - alpha) + alpha
        x += (len(rows[0]) + gap) * scale
    return x

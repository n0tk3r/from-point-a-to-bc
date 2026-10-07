"""The crisp small things of the backdrop, painted over the brushwork: mouldings and panel lines, the door's
furniture, the window's bars and what stands on its sill, the clock, the cork board, the photographs,
the rug's fringe. (The bookcase's books and the staircase's balusters are with those things, in _room.)"""

from home_living_room_plan import *
from home_living_room_room import (wp, wrect, panes, curtain_shape, FRAMES, CORK, CLOCK, bookcase, stairs, small_things, stair_x, crooked, rug_pt, TILT, SEED)

DARK = "#160e14"
FAMILY = [("#2aa27a", 15.0, "#7a3a22"), ("#666cd6", 13.0, "#4a3020"), ("#f0607f", 9.0, "#e8c070"), ("#4fc0e2", 11.0, "#c84a3a")]   # Mom, Big Sister, Little Sister, the Son: shirt, height, hair or cap


def wl(albedo, X, Y, dim=1.0, n=(0, 0, -1)):
    """Paint for something flat on the back wall at (X, Y)."""
    return lit(albedo, (X, Y, ZW - 1), n, dim)


def wline(s, pts, color, width=1.0, alpha=1.0):
    s.line([wp(x, y) for x, y in pts], color, width, alpha)


def sunk(s, x0, x1, y0, y1, a=0.5):
    """A sunk panel: shadow under its top and right edges, light on its bottom and left ones."""
    wline(s, [(x0, y1), (x1, y1), (x1, y0)], DARK, 0.9, a)
    wline(s, [(x0, y1), (x0, y0), (x1, y0)], "#ffe6b8", 0.8, a * 0.55)


def in_frame(s, x0, x1, y0, y1, what, rng):
    """What is in a photograph frame: blobs of color, never a face."""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w, h = x1 - x0, y1 - y0
    c = lambda a, d=1.0: wl(a, cx, cy, d)

    def r(u0, u1, v0, v1, color):                                       # u across 0..1, v UP 0..1
        wrect(s, x0 + u0 * w, x0 + u1 * w, y0 + v0 * h, y0 + v1 * h, color)

    def blob(u, v, ru, rv, color):
        p = wp(x0 + u * w, y0 + v * h)
        s.ellipse(p[0], p[1], ru * w * KW, rv * h * KW, color)
    if what == "lake":                                                  # the five of us at the lake; Dad set the timer and ran: he is the blur
        r(0, 1, 0.58, 1, c("#bcd8ea"))
        r(0, 1, 0.50, 0.60, c("#5f8058"))
        r(0, 1, 0.26, 0.52, c("#6a9cc8"))
        r(0, 1, 0, 0.27, c("#d8c494"))
        for k in range(4):
            wline(s, [(x0 + (0.1 + 0.2 * k) * w, y0 + (0.34 + 0.04 * (k % 2)) * h), (x0 + (0.24 + 0.2 * k) * w, y0 + (0.34 + 0.04 * (k % 2)) * h)], c("#a8c8e4"), 0.7, 0.8)
        for (shirt, tall, hair), u in zip(FAMILY, (0.14, 0.31, 0.46, 0.60)):
            x = x0 + u * w
            wrect(s, x - 3.0, x + 3.0, y0 + 0.10 * h, y0 + 0.10 * h + tall * 0.62, c(shirt))
            wrect(s, x - 2.2, x + 2.2, y0 + 0.10 * h - 0.0, y0 + 0.10 * h + tall * 0.22, c("#4a5a78"))
            p = wp(x, y0 + 0.10 * h + tall * 0.62 + 2.6)
            s.ellipse(p[0], p[1], 1.9, 2.0, c("#e8b083"))
            s.ellipse(p[0], p[1] - 1.2, 2.0, 1.1, c(hair))
        for k in range(5):                                              # the blur
            x = x0 + (0.72 + 0.05 * k) * w
            wrect(s, x - 3.5, x + 3.5, y0 + 0.11 * h, y0 + 0.11 * h + 11, c("#f4c043"), 0.34)
            p = wp(x + 1.5, y0 + 0.11 * h + 13.6)
            s.ellipse(p[0], p[1], 2.4, 2.0, c("#e8b083"), 0.34)
    elif what == "wedding":
        r(0, 1, 0, 1, c("#c9c0b0"))
        s.poly([wp(x0 + 0.20 * w, y0), wp(x0 + 0.62 * w, y0), wp(x0 + 0.46 * w, y0 + 0.62 * h), wp(x0 + 0.36 * w, y0 + 0.62 * h)], c("#fbf8f0"))
        r(0.56, 0.86, 0, 0.66, c("#2a2a34"))
        blob(0.41, 0.72, 0.09, 0.07, c("#e8b083"))
        blob(0.71, 0.76, 0.09, 0.07, c("#e8b083"))
        blob(0.41, 0.77, 0.12, 0.05, c("#fbf8f0"), )
    elif what in ("baby", "baby2"):
        r(0, 1, 0, 1, c("#b8d0e0" if what == "baby" else "#e8d0d8"))
        blob(0.5, 0.42, 0.32, 0.28, c("#fbf4e0"))
        blob(0.5, 0.60, 0.16, 0.14, c("#f0c0a0"))
    elif what in ("portrait", "portrait2"):
        r(0, 1, 0, 1, c("#56708c" if what == "portrait" else "#8a6a5a"))
        blob(0.5, 0.20, 0.36, 0.26, c("#c8483c" if what == "portrait" else "#e8e0c8"))
        blob(0.5, 0.60, 0.17, 0.17, c("#e8b083"))
        blob(0.5, 0.72, 0.19, 0.10, c("#5a3a22" if what == "portrait" else "#d8c890"))
    elif what == "hills":
        r(0, 1, 0.5, 1, c("#c8dcea"))
        s.poly([wp(x0, y0 + 0.5 * h), wp(x0 + 0.3 * w, y0 + 0.8 * h), wp(x0 + 0.55 * w, y0 + 0.55 * h), wp(x0 + 0.8 * w, y0 + 0.86 * h), wp(x1, y0 + 0.5 * h)], c("#8a9ab8"))
        r(0, 1, 0, 0.5, c("#7fa060"))
        r(0.30, 0.70, 0.12, 0.30, c("#c8483c"))                       # the wagon, on some other holiday
        r(0.30, 0.70, 0.12, 0.19, c("#a87444"))
    elif what == "drawing":                                             # by the youngest: a house, a sun, five people
        r(0, 1, 0, 1, c("#fbf8ee"))
        wline(s, [(x0 + 0.15 * w, y0 + 0.2 * h), (x0 + 0.15 * w, y0 + 0.55 * h), (x0 + 0.3 * w, y0 + 0.78 * h), (x0 + 0.45 * w, y0 + 0.55 * h), (x0 + 0.45 * w, y0 + 0.2 * h), (x0 + 0.15 * w, y0 + 0.2 * h)], c("#c8483c"), 0.9)
        blob(0.8, 0.8, 0.09, 0.10, c("#f0c030"))
        for k, cc in enumerate(("#f4c043", "#2aa27a", "#666cd6", "#4fc0e2", "#f0607f")):
            wline(s, [(x0 + (0.52 + 0.09 * k) * w, y0 + 0.2 * h), (x0 + (0.52 + 0.09 * k) * w, y0 + (0.52 - 0.05 * k) * h)], c(cc), 1.0)
        wline(s, [(x0 + 0.05 * w, y0 + 0.18 * h), (x0 + 0.95 * w, y0 + 0.18 * h)], c("#5a9a4a"), 1.0)
    elif what == "old":                                                 # grandparents, in brown
        r(0, 1, 0, 1, c("#b89a78"))
        for u in (0.34, 0.66):
            blob(u, 0.22, 0.2, 0.26, c("#5a4636"))
            blob(u, 0.60, 0.11, 0.13, c("#e0c0a0"))
            blob(u, 0.70, 0.12, 0.07, c("#e8e4dc"))
    elif what == "school":
        r(0, 1, 0, 1, c("#7a9a70"))
        for row in range(2):
            for k in range(4):
                u = 0.16 + 0.22 * k + 0.05 * row
                blob(u, 0.26 + 0.3 * row, 0.08, 0.12, c(("#c8483c", "#3f6f8f", "#e8e0c8", "#d9a441")[(k + row) % 4]))
                blob(u, 0.42 + 0.3 * row, 0.05, 0.06, c("#e8b083"))
    elif what == "sampler":                                             # stitched by somebody's grandmother: a house, trees, rows of stitches (no words)
        r(0, 1, 0, 1, c("#e8dcc0"))
        s.poly([wp(x0 + 0.36 * w, y0 + 0.30 * h), wp(x0 + 0.64 * w, y0 + 0.30 * h), wp(x0 + 0.64 * w, y0 + 0.56 * h), wp(x0 + 0.36 * w, y0 + 0.56 * h)], c("#b0483c"))
        s.poly([wp(x0 + 0.32 * w, y0 + 0.56 * h), wp(x0 + 0.68 * w, y0 + 0.56 * h), wp(x0 + 0.5 * w, y0 + 0.80 * h)], c("#5a4636"))
        for u in (0.18, 0.82):
            s.poly([wp(x0 + (u - 0.07) * w, y0 + 0.32 * h), wp(x0 + (u + 0.07) * w, y0 + 0.32 * h), wp(x0 + u * w, y0 + 0.70 * h)], c("#5a8a4a"))
        for v, cc in ((0.16, "#3f6f8f"), (0.90, "#b0483c")):
            for k in range(9):
                blob(0.1 + k * 0.1, v, 0.022, 0.035, c(cc))
    else:                                                               # the sea
        r(0, 1, 0.55, 1, c("#d0e4f0"))
        r(0, 1, 0.2, 0.56, c("#4a86b8"))
        r(0, 1, 0, 0.22, c("#e2d0a0"))
        s.poly([wp(x0 + 0.6 * w, y0 + 0.5 * h), wp(x0 + 0.7 * w, y0 + 0.8 * h), wp(x0 + 0.8 * w, y0 + 0.5 * h)], c("#fbf8f0"))


def wall(L, info):
    rng = np.random.default_rng(SEED + 200)
    # ---- mouldings and the panelling's lines, only where the wall is bare
    t = Sheet(SHAPE)
    x = -616.0
    while x < 620:
        k = np.floor((x + 10.0) / 46.0)
        xa, xb = -10 + 46 * k + 10.5, -10 + 46 * (k + 1) - 1.5
        sunk(t, xa, xb, 27.5, DADO - 11.5, 0.5)
        x += 46.0
    for (y, c, wd, a) in ((DADO + 4.6, "#ffe6b8", 0.9, 0.55), (DADO - 0.6, DARK, 1.1, 0.55), (12.8, "#ffe6b8", 0.8, 0.4), (0.6, DARK, 1.4, 0.6),
                          (PICRAIL + 4.2, "#ffe6b8", 0.8, 0.5), (PICRAIL - 0.6, DARK, 1.1, 0.5), (WALL_H - 13.5, DARK, 1.0, 0.45),
                          (WALL_H - 9.0, "#fff0d0", 0.9, 0.4), (WALL_H - 4.5, DARK, 0.9, 0.35), (WALL_H - 0.6, DARK, 1.3, 0.5)):
        wline(t, [(-640, y), (640, y)], c, wd, a)
    tc, ta = t.done()
    over(L.rgb, tc, ta * info["bare"])

    s = Sheet(SHAPE)
    # ---- the front door
    d = DOOR
    lx0, lx1, ltop = d["lx0"], d["lx1"], d["ltop"]
    lm = (lx0 + lx1) / 2
    wline(s, [(d["x0"], 0), (d["x0"], d["top"]), (d["x1"], d["top"]), (d["x1"], 0)], DARK, 1.0, 0.5)
    wline(s, [(d["x0"] + 3.5, 0), (d["x0"] + 3.5, d["top"] - 3.5), (d["x1"] - 3.5, d["top"] - 3.5), (d["x1"] - 3.5, 0)], DARK, 0.7, 0.25)
    wline(s, [(lx0, 0), (lx0, ltop), (lx1, ltop), (lx1, 0)], DARK, 1.0, 0.6)
    for (xa, xb) in ((lx0 + 9, lm - 4), (lm + 4, lx1 - 9)):
        for (ya, yb) in ((12, 86), (112, 131)):
            wrect(s, xa, xb, ya, yb, DARK, 0.07)
            sunk(s, xa, xb, ya, yb, 0.5)
        sunk(s, xa, xb, 138, 192, 0.6)                                   # the frosted lights
        wline(s, [((xa + xb) / 2, 138), ((xa + xb) / 2, 192)], wl("#e4dcc6", lm, 165), 1.1, 0.9)
        wline(s, [(xa, 165), (xb, 165)], wl("#e4dcc6", lm, 165), 1.1, 0.9)
    brass = lambda Y, dm=1.0: wl("#e0b550", lx1, Y, dm, (0.3, 0.3, -0.9))
    wrect(s, lm - 14, lm + 14, 94.5, 103, brass(99))                     # the letter flap
    wline(s, [(lm - 11, 98.5), (lm + 11, 98.5)], DARK, 0.9, 0.7)
    p = wp(lx1 - 10, 101)
    wrect(s, lx1 - 14.5, lx1 - 5.5, 90, 112, brass(100, 0.8))
    s.ellipse(p[0], p[1], 3.0, 3.0, brass(101, 1.15))
    s.ellipse(p[0] - 0.8, p[1] - 0.8, 1.1, 1.1, "#fff4c0", 0.8)
    p = wp(lx1 - 10, 122)
    s.ellipse(p[0], p[1], 2.0, 2.0, brass(122))
    a, b = wp(d["x1"] - 3, 134), wp(lx1 - 26, 134)                       # the chain, on
    wrect(s, lx1 - 30, lx1 - 12, 132.5, 135.5, brass(134, 0.85))
    s.line([a, ((a[0] + b[0]) / 2 + 2, a[1] + 5), (b[0] + 4, b[1] + 1)], brass(134), 0.8, 0.9)
    for hy in (26, 104, 180):                                           # hinges
        wrect(s, lx0 - 0.5, lx0 + 2.5, hy, hy + 9, brass(hy, 0.8))
    wrect(s, d["x0"] - 2, d["x1"] + 2, 0, 2.6, wl("#8c5a30", lm, 2))
    # ---- the light switch, on the bit of wall between the window and the clock
    wrect(s, -155, -147, 124, 137, wl("#e8e2d0", -151, 130))
    wline(s, [(-155, 124), (-155, 137), (-147, 137)], DARK, 0.6, 0.4)
    wline(s, [(-151, 128), (-151, 133)], wl("#8a8478", -151, 130), 1.0)
    # ---- the children's heights, pencilled up the door frame year by year
    for k, (yy, ln) in enumerate(((96, 4.0), (104, 3.0), (119, 4.0), (128, 3.0), (131, 2.4), (146, 4.0), (150, 3.0))):
        wline(s, [(d["x0"] + 2.0, yy), (d["x0"] + 2.0 + ln, yy)], "#4a4650", 0.7, 0.8)
    L.sheet(s)

    # ---- the window: its bars said again, the pole and rings, the ties, what stands on the sill
    s = Sheet(SHAPE)
    w = WIN
    white = lambda X, Y, dm=1.0: wl("#f0ead8", X, Y, dm)
    wline(s, [(w["x0"], w["y0"]), (w["x0"], w["y1"]), (w["x1"], w["y1"]), (w["x1"], w["y0"])], DARK, 1.0, 0.5)
    for (xa, xb, ya, yb) in panes():
        wline(s, [(xa, ya), (xa, yb), (xb, yb), (xb, ya), (xa, ya)], "#0a1028", 1.0, 0.75)
        wline(s, [(xa - 1.2, ya - 1.2), (xb + 1.2, ya - 1.2)], white((xa + xb) / 2, ya, 1.15), 0.8, 0.8)
    for xs in (w["m1"], w["m2"]):
        wline(s, [(xs - 3, w["y0"] + 7), (xs - 3, w["y1"] - 7)], white(xs, 160, 1.15), 0.7, 0.7)
    for xs in ((w["x0"] + w["m1"]) / 2, (w["x1"] + w["m2"]) / 2):        # the catches of the side sashes
        wrect(s, xs - 2.5, xs + 2.5, w["rail"] - 2, w["rail"] + 2.5, wl("#c9a050", xs, w["rail"]))
    wrect(s, w["x0"] - 9, w["x1"] + 9, w["y0"] - 6.5, w["y0"], wl("#c9905a", (w["x0"] + w["x1"]) / 2, w["y0"]))
    wline(s, [(w["x0"] - 9, w["y0"]), (w["x1"] + 9, w["y0"])], wl("#f0c890", -310, w["y0"], 1.1, (0, 1, 0)), 1.0, 0.9)
    wline(s, [(w["x0"] - 9, w["y0"] - 7), (w["x1"] + 9, w["y0"] - 7)], DARK, 1.3, 0.5)
    # pole, finials, rings
    wline(s, [(w["x0"] - 46, POLE), (w["x1"] + 46, POLE)], wl("#7a4c2a", -310, POLE), 2.2)
    wline(s, [(w["x0"] - 46, POLE + 1.2), (w["x1"] + 46, POLE + 1.2)], wl("#c08a50", -310, POLE, 1.0, (0, 1, 0)), 0.8, 0.8)
    for xs in (w["x0"] - 48, w["x1"] + 48):
        p = wp(xs, POLE)
        s.ellipse(p[0], p[1], 2.6, 2.6, wl("#8a5630", xs, POLE))
    for side in (-1, 1):
        xo, xi = curtain_shape(np.float32(POLE - 1), side)
        for k in range(6):
            xr = lerp(float(xo), float(xi), (k + 0.5) / 6)
            p = wp(xr, POLE - 1.5)
            s.ellipse(p[0], p[1], 1.5, 2.0, wl("#e0b550", xr, POLE))
        # the folds, drawn down the cloth; they gather at the tie
        for f in (0.16, 0.38, 0.62, 0.84):
            pts = []
            for Y in np.linspace(POLE - 2, 61, 26):
                a_, b_ = curtain_shape(np.float32(Y), side)
                pts.append((lerp(float(a_), float(b_), f + 0.03 * np.sin(Y * 0.11 + f * 9)), Y))
            wline(s, pts, "#101830", 0.9, 0.42)
            wline(s, [(x + side * 1.6, y) for x, y in pts], "#a8c8e8", 0.7, 0.22)
        pts = []
        for Y in np.linspace(POLE - 2, 60, 26):                          # the inner edge
            a_, b_ = curtain_shape(np.float32(Y), side)
            pts.append((float(b_), Y))
        wline(s, pts, "#101830", 0.9, 0.5)
        a_, b_ = curtain_shape(np.float32(118.0), side)
        wline(s, [(float(a_) - side * 1, 121), (float(b_) + side * 1.5, 116)], wl("#e0b550", float(a_), 118), 2.0)
        p = wp(float(b_) + side * 1.0, 115)
        s.line([p, (p[0] + side * 0.5, p[1] + 6)], wl("#e0b550", float(a_), 112), 1.4)
    # a geranium in a clay pot, and the rabbit who is keeping watch
    gx = w["x1"] - 30
    s.poly([wp(gx - 7, w["y0"]), wp(gx + 7, w["y0"]), wp(gx + 9, w["y0"] + 12), (wp(gx - 9, w["y0"] + 12))], wl("#b8623a", gx, w["y0"] + 6))
    wline(s, [(gx - 9, w["y0"] + 12), (gx + 9, w["y0"] + 12)], wl("#d88a5a", gx, w["y0"] + 12), 1.2)
    for k in range(16):
        lx, ly = gx + rng.normal(0, 8), w["y0"] + 16 + rng.random() * 16
        p = wp(lx, ly)
        s.ellipse(p[0], p[1], 2.6, 2.0, wl(("#3f6a34", "#5a8a44", "#2f5228")[k % 3], lx, ly, 1.1))
    for k in range(5):
        lx, ly = gx + rng.normal(0, 7), w["y0"] + 28 + rng.random() * 8
        p = wp(lx, ly)
        s.ellipse(p[0], p[1], 2.0, 1.8, wl("#d8483c", lx, ly, 1.2))
    rx = w["x0"] + 26
    fur = lambda Y, dm=1.0: wl("#d8c8c0", rx, Y, dm)
    p = wp(rx, w["y0"] + 7)
    s.ellipse(p[0], p[1], 4.6, 5.0, fur(w["y0"] + 7, 0.9))
    p2 = wp(rx - 0.5, w["y0"] + 17)
    s.ellipse(p2[0], p2[1], 3.3, 3.2, fur(w["y0"] + 17))
    s.line([(p2[0] - 1.6, p2[1] - 2), (p2[0] - 2.6, p2[1] - 10)], fur(w["y0"] + 24), 1.9)
    s.line([(p2[0] + 1.2, p2[1] - 2), (p2[0] + 2.4, p2[1] - 9.5)], fur(w["y0"] + 24, 0.85), 1.9)
    s.line([(p2[0] - 2.4, p2[1] - 4), (p2[0] - 2.8, p2[1] - 9)], wl("#e8a0a0", rx, w["y0"] + 24), 0.7, 0.8)
    L.sheet(s)

    # ---- the clock (twenty to ten), the cork board, the photographs: each with its shadow on the paper
    s = Sheet(SHAPE)
    cx, cy = CLOCK
    wood_c, wood_l = wl("#7a4c2a", cx, cy), wl("#b07a44", cx, cy)
    wrect(s, cx - 8 + 2, cx + 8 + 2, cy - 42, cy - 8, DARK, 0.30)
    p = wp(cx + 2, cy - 2)
    s.ellipse(p[0], p[1], 15.5 * KW, 15.5 * KW, DARK, 0.30)
    wrect(s, cx - 8, cx + 8, cy - 40, cy - 8, wood_c)
    wrect(s, cx - 5.5, cx + 5.5, cy - 37, cy - 14, wl("#2a1c18", cx, cy - 26))
    wline(s, [(cx, cy - 12), (cx + 1.6, cy - 31)], wl("#e0b550", cx, cy - 22), 0.8)
    p = wp(cx + 1.8, cy - 32)
    s.ellipse(p[0], p[1], 2.2, 2.2, wl("#f0cc6a", cx, cy - 32))
    p = wp(cx, cy)
    r = 14.5 * KW
    octa = [(p[0] + math.cos(math.radians(22.5 + 45 * k)) * r * 1.08, p[1] + math.sin(math.radians(22.5 + 45 * k)) * r * 1.08) for k in range(8)]
    s.poly(octa, wood_c)
    s.line(octa[4:7], wood_l, 0.9, 0.8)
    s.ellipse(p[0], p[1], r * 0.80, r * 0.80, wl("#f4ecd6", cx, cy))
    for k in range(12):
        a = math.radians(30 * k)
        s.line([(p[0] + math.sin(a) * r * 0.62, p[1] - math.cos(a) * r * 0.62), (p[0] + math.sin(a) * r * 0.74, p[1] - math.cos(a) * r * 0.74)], "#2a2024", 0.7 if k % 3 else 1.1, 0.9)
    ah, am = math.radians(290.0), math.radians(240.0)                   # 9:40
    s.line([p, (p[0] + math.sin(ah) * r * 0.42, p[1] - math.cos(ah) * r * 0.42)], "#1a1418", 1.4)
    s.line([p, (p[0] + math.sin(am) * r * 0.66, p[1] - math.cos(am) * r * 0.66)], "#1a1418", 1.0)
    s.ellipse(p[0], p[1], 0.9, 0.9, "#b8923e")
    # the cork board
    x0, x1, y0, y1 = CORK
    wrect(s, x0 + 2.5, x1 + 2.5, y0 - 3, y1 - 3, DARK, 0.28)
    wrect(s, x0, x1, y0, y1, wl("#8a5a34", (x0 + x1) / 2, (y0 + y1) / 2))
    wrect(s, x0 + 4, x1 - 4, y0 + 4, y1 - 4, wl("#c49a66", (x0 + x1) / 2, (y0 + y1) / 2))
    sunk(s, x0 + 4, x1 - 4, y0 + 4, y1 - 4, 0.45)
    cork = lambda a_, X, Y, dm=1.0: wl(a_, X, Y, dm)
    # a calendar: this month, days crossed off
    ca0, ca1, cb0, cb1 = x0 + 8, x0 + 34, y0 + 16, y1 - 8
    wrect(s, ca0, ca1, cb0, cb1, cork("#f6f2e6", ca0, cb0))
    wrect(s, ca0, ca1, cb1 - 12, cb1, cork("#c8483c", ca0, cb1))
    for r_ in range(4):
        for c_ in range(6):
            q = wp(ca0 + 3.2 + c_ * 4.0, cb0 + 4 + r_ * 6.2)
            s.ellipse(q[0], q[1], 0.7, 0.7, "#5a5660" if (r_ * 6 + (5 - c_)) % 5 else "#c8483c", 0.85)
    # a child's drawing in crayon, a postcard, a yellow note, a ticket
    da0, da1, db0, db1 = x0 + 38, x0 + 62, y0 + 26, y1 - 7
    s.poly([wp(da0, db0 + 1), wp(da1, db0 - 1), wp(da1 + 1, db1), wp(da0 + 1, db1 + 1)], cork("#fbf8ee", da0, db0))
    wline(s, [(da0 + 4, db0 + 5), (da0 + 4, db0 + 14), (da0 + 9, db0 + 20), (da0 + 14, db0 + 14), (da0 + 14, db0 + 5), (da0 + 4, db0 + 5)], cork("#c8483c", da0, db0), 0.8)
    q = wp(da1 - 5, db1 - 6)
    s.ellipse(q[0], q[1], 2.2, 2.2, cork("#f0c030", da0, db1))
    wline(s, [(da0 + 2, db0 + 4), (da1 - 2, db0 + 3)], cork("#5a9a4a", da0, db0), 1.0)
    wrect(s, x0 + 40, x0 + 58, y0 + 8, y0 + 22, cork("#6aa6d0", x0 + 50, y0 + 14))
    wrect(s, x0 + 40, x0 + 58, y0 + 8, y0 + 13, cork("#e8d49a", x0 + 50, y0 + 10))
    s.poly([wp(x0 + 64, y0 + 30), wp(x0 + 77, y0 + 31), wp(x0 + 76.5, y0 + 44), wp(x0 + 63.5, y0 + 43)], cork("#ffe36b", x0 + 70, y0 + 36))
    for k in range(3):
        wline(s, [(x0 + 66, y0 + 34 + k * 3), (x0 + 74, y0 + 34.5 + k * 3)], "#6b5a1c", 0.6, 0.7)
    wrect(s, x0 + 64, x0 + 77, y0 + 10, y0 + 24, cork("#f6f2e6", x0 + 70, y0 + 16))
    for k in range(4):
        wline(s, [(x0 + 66, y0 + 13 + k * 2.8), (x0 + 75 - (k % 2) * 3, y0 + 13 + k * 2.8)], "#5a5660", 0.6, 0.6)
    wrect(s, x0 + 64, x0 + 77, y0 + 48, y1 - 8, cork("#e8a0b0", x0 + 70, y1 - 12))
    for (px_, py_, cc) in ((ca0 + 13, cb1 - 3, "#3f6f8f"), (da0 + 12, db1 - 2, "#c8483c"), (x0 + 49, y0 + 21, "#e8c84a"), (x0 + 70, y0 + 43, "#c8483c"), (x0 + 70, y0 + 23, "#3f8c7c"), (x0 + 70, y1 - 9, "#3f6f8f")):
        q = wp(px_, py_)
        s.ellipse(q[0], q[1], 1.1, 1.1, cork(cc, px_, py_, 1.2))
    # the photographs; the big ones hang from the picture rail on cords, the old way
    for (fx0, fx1, fy0, fy1, frame, mat, what) in FRAMES:
        if what in ("lake", "wedding", "portrait", "school"):
            hx = (fx0 + fx1) / 2
            for xe in (fx0 + 4, fx1 - 4):
                wline(s, [(xe, fy1), (hx, PICRAIL - 1)], "#3a2c28", 0.6, 0.55)
            p = wp(hx, PICRAIL - 1)
            s.ellipse(p[0], p[1], 1.2, 1.2, wl("#c9a050", hx, PICRAIL))
    lamp_w = wp(PIANOLAMP[0], PIANOLAMP[1])
    for (fx0, fx1, fy0, fy1, frame, mat, what) in FRAMES:
        TILT[0] = None
        c_ = wp((fx0 + fx1) / 2, (fy0 + fy1) / 2)
        crooked(what, fx0, fx1, fy0, fy1)
        dx, dy = c_[0] - lamp_w[0], c_[1] - lamp_w[1]
        k = math.hypot(dx, dy) + 1e-6
        ox, oy = dx / k * 2.2 / KW, -dy / k * 2.2 / KW                   # its shadow falls away from the piano lamp
        wrect(s, fx0 + ox, fx1 + ox, fy0 + oy, fy1 + oy, DARK, 0.32)
        X, Y = (fx0 + fx1) / 2, (fy0 + fy1) / 2
        wrect(s, fx0, fx1, fy0, fy1, wl(frame, X, Y))
        wline(s, [(fx0, fy0), (fx0, fy1), (fx1, fy1)], wl(lerp(col(frame), col("#ffe6b0"), 0.45), X, Y), 0.8, 0.8)
        wline(s, [(fx0, fy0), (fx1, fy0), (fx1, fy1)], DARK, 0.8, 0.5)
        m = 2.6
        wrect(s, fx0 + m, fx1 - m, fy0 + m, fy1 - m, wl(mat, X, Y))
        m2 = 5.5 if (fx1 - fx0) > 40 else 4.6
        in_frame(s, fx0 + m2, fx1 - m2, fy0 + m2, fy1 - m2, what, rng)
        wline(s, [(fx0 + m2, fy0 + m2), (fx0 + m2, fy1 - m2), (fx1 - m2, fy1 - m2)], DARK, 0.6, 0.35)
        s.poly([wp(fx0 + m, fy1 - m), wp(fx0 + m + (fx1 - fx0) * 0.3, fy1 - m), wp(fx0 + m, fy1 - m - (fy1 - fy0) * 0.45)], "#ffffff", 0.10)     # glass
        TILT[0] = None
    # somebody small has been at the panelling with crayons, and somebody else has nearly scrubbed it off
    for pts_, cc in (([(-236, 34), (-231, 44), (-226, 36), (-221, 47), (-216, 38), (-212, 46)], "#c8483c"),
                     ([(-232, 54), (-228, 60), (-222, 58), (-222, 52), (-229, 51), (-232, 54)], "#3f6f9f"),
                     ([(-213, 52), (-213, 62)], "#e8a030"), ([(-217, 58), (-209, 58)], "#e8a030")):
        wline(s, pts_, wl(cc, -224, 46), 0.9, 0.5)
    # a wall socket by the desk, and the computer's cable to it
    wrect(s, -169, -160, 30, 43, wl("#e8e2d0", -165, 36))
    for yy in (33.5, 39.5):
        wline(s, [(-166.2, yy - 1), (-166.2, yy + 1)], "#3a3438", 0.6)
        wline(s, [(-163.0, yy - 1), (-163.0, yy + 1)], "#3a3438", 0.6)
    L.sheet(s)


def plate_rail(L, info):
    """The picture rail is also a narrow shelf, and the family's treasures stand along it, up in the dim
    above the lamps: best plates on edge, a jug, a model ship, cups somebody won, a toy engine."""
    rng = np.random.default_rng(SEED + 240)
    s = Sheet(SHAPE)
    Y0 = PICRAIL + 4.6
    z = ZW - 5.0
    c = lambda a, X, Y, d=1.0, n=(0, 0.25, -1): lit(a, (X, Y, z), n, d * 0.95)

    def q(X, Y):
        return P(X, Y, z)

    def shadow(X, w):
        s.ellipse(q(X, Y0)[0] + 1.5, q(X, Y0)[1] - 0.5, w * KW * 0.6, 1.4, DARK, 0.35)

    def plate(X, d, rim, mid, dot=None):
        shadow(X, d)
        p = q(X, Y0 + d / 2)
        r = d / 2 * KW * 1.02
        s.ellipse(p[0] + 1.2, p[1] + 0.6, r, r, DARK, 0.30)
        s.ellipse(p[0], p[1], r, r, c(rim, X, Y0 + d / 2))
        s.ellipse(p[0], p[1], r * 0.72, r * 0.72, c("#efe8d6", X, Y0 + d / 2))
        s.ellipse(p[0], p[1], r * 0.60, r * 0.60, c(mid, X, Y0 + d / 2))
        if dot:
            s.ellipse(p[0], p[1], r * 0.26, r * 0.26, c(dot, X, Y0 + d / 2))
        s.line([(p[0] - r * 0.7, p[1] - r * 0.55), (p[0] - r * 0.2, p[1] - r * 0.9)], "#ffffff", 0.7, 0.35)

    def jug(X, h, body, band=None):
        shadow(X, h * 0.6)
        a, b, m = q(X, Y0), q(X, Y0 + h), q(X, Y0 + h * 0.45)
        w = h * 0.30 * KW
        s.poly([(a[0] - w * 0.7, a[1]), (a[0] + w * 0.7, a[1]), (m[0] + w, m[1]), (b[0] + w * 0.55, b[1]), (b[0] - w * 0.55, b[1]), (m[0] - w, m[1])], c(body, X, Y0 + h / 2))
        s.poly([(a[0] - w * 0.7, a[1]), (a[0] - w * 0.1, a[1]), (m[0] - w * 0.2, m[1]), (b[0] - w * 0.2, b[1]), (b[0] - w * 0.55, b[1]), (m[0] - w, m[1])], c(body, X, Y0 + h / 2, 0.7))
        if band:
            s.line([(m[0] - w, m[1]), (m[0] + w, m[1])], c(band, X, Y0 + h / 2), 1.3)
        s.line([(b[0] + w * 0.55, b[1] + 1.5), (b[0] + w * 1.5, b[1] + 3), (m[0] + w, m[1] - 1)], c(body, X, Y0 + h / 2), 1.1)

    def cup(X, h, metal="#e0b550"):
        shadow(X, h * 0.4)
        a, b = q(X, Y0), q(X, Y0 + h)
        w = h * 0.2 * KW
        s.poly([(a[0] - w, a[1]), (a[0] + w, a[1]), (a[0] + w * 0.7, a[1] - h * 0.18 * KW), (a[0] - w * 0.7, a[1] - h * 0.18 * KW)], c("#3a2a20", X, Y0))
        s.line([(a[0], a[1] - h * 0.18 * KW), (a[0], a[1] - h * 0.5 * KW)], c(metal, X, Y0 + h * 0.3), 1.2)
        s.poly([(b[0] - w * 1.25, b[1]), (b[0] + w * 1.25, b[1]), (a[0] + w * 0.4, a[1] - h * 0.5 * KW), (a[0] - w * 0.4, a[1] - h * 0.5 * KW)], c(metal, X, Y0 + h * 0.8))
        s.line([(b[0] - w * 0.9, b[1] + 1), (a[0] - w * 0.2, a[1] - h * 0.5 * KW)], "#fff4c0", 0.7, 0.5)

    def ship(X):
        shadow(X, 34)
        h = 30.0
        a = q(X, Y0)
        k = KW
        s.poly([(a[0] - 16 * k, a[1] - 3 * k), (a[0] + 17 * k, a[1] - 3 * k), (a[0] + 13 * k, a[1]), (a[0] - 12 * k, a[1])], c("#6a3e24", X, Y0 + 2))
        s.line([(a[0] - 16 * k, a[1] - 3.2 * k), (a[0] + 17 * k, a[1] - 3.2 * k)], c("#e8d8b0", X, Y0 + 4), 0.8)
        for mx_, mh in ((-6, 30), (6, 26)):
            s.line([(a[0] + mx_ * k, a[1] - 3 * k), (a[0] + mx_ * k, a[1] - mh * k)], c("#3a2a20", X, Y0 + 15), 0.8)
            s.poly([(a[0] + (mx_ + 1) * k, a[1] - 6 * k), (a[0] + (mx_ + 10) * k, a[1] - 7 * k), (a[0] + (mx_ + 1) * k, a[1] - (mh - 2) * k)], c("#efe6d0", X, Y0 + 18))
        s.poly([(a[0] - 7 * k, a[1] - 6 * k), (a[0] - 15 * k, a[1] - 5 * k), (a[0] - 7 * k, a[1] - 24 * k)], c("#e2d8c0", X, Y0 + 14, 0.85))

    def engine(X):
        shadow(X, 26)
        a = q(X, Y0)
        k = KW
        s.poly([(a[0] - 12 * k, a[1] - 3 * k), (a[0] + 8 * k, a[1] - 3 * k), (a[0] + 8 * k, a[1] - 10 * k), (a[0] - 12 * k, a[1] - 10 * k)], c("#3f8a5a", X, Y0 + 6))
        s.poly([(a[0] + 8 * k, a[1] - 3 * k), (a[0] + 15 * k, a[1] - 3 * k), (a[0] + 15 * k, a[1] - 15 * k), (a[0] + 8 * k, a[1] - 15 * k)], c("#c8483c", X, Y0 + 9))
        s.poly([(a[0] - 9 * k, a[1] - 10 * k), (a[0] - 6 * k, a[1] - 10 * k), (a[0] - 5.5 * k, a[1] - 15 * k), (a[0] - 9.5 * k, a[1] - 15 * k)], c("#2a2a30", X, Y0 + 12))
        for wx in (-8, 0, 10):
            s.ellipse(a[0] + wx * k, a[1] - 2.4 * k, 2.6 * k, 2.6 * k, c("#e0b550", X, Y0 + 2))

    def books(X, n):
        shadow(X, n * 4)
        for i in range(n):
            hh = 16 + rng.random() * 7
            a, b = q(X + i * 4.2, Y0), q(X + i * 4.2 + 3.6, Y0 + hh)
            s.poly([(a[0], a[1]), (b[0], a[1]), (b[0], b[1]), (a[0], b[1])], c(("#6a3e34", "#3a5a4a", "#4a4a6a", "#8a6a3a")[i % 4], X, Y0 + 9))

    def bottle(X, h, glass):
        a, b = q(X, Y0), q(X, Y0 + h)
        w = 3.2 * KW
        s.poly([(a[0] - w, a[1]), (a[0] + w, a[1]), (a[0] + w, a[1] - h * 0.6 * KW), (a[0] + w * 0.35, a[1] - h * 0.76 * KW), (b[0] + w * 0.35, b[1]), (b[0] - w * 0.35, b[1]), (a[0] - w * 0.35, a[1] - h * 0.76 * KW), (a[0] - w, a[1] - h * 0.6 * KW)], c(glass, X, Y0 + h / 2), 0.85)
        s.line([(a[0] - w * 0.5, a[1] - 1), (a[0] - w * 0.5, a[1] - h * 0.55 * KW)], "#ffffff", 0.6, 0.4)
    # the shelf's own edge
    s.line([q(-640, Y0), q(640, Y0)], lit("#c08a50", (0, Y0, z), (0, 1, 0), 1.2), 0.9, 0.55)
    def tray(X, w, h, body, edge):
        shadow(X, w)
        p = q(X, Y0 + h / 2)
        s.ellipse(p[0] + 1.2, p[1] + 0.6, w / 2 * KW, h / 2 * KW, DARK, 0.30)
        s.ellipse(p[0], p[1], w / 2 * KW, h / 2 * KW, c(edge, X, Y0 + h / 2))
        s.ellipse(p[0], p[1], w / 2 * KW * 0.84, h / 2 * KW * 0.80, c(body, X, Y0 + h / 2))
        s.line([(p[0] - w * 0.2 * KW, p[1] - h * 0.2 * KW), (p[0] + w * 0.1 * KW, p[1] - h * 0.32 * KW)], "#ffffff", 0.7, 0.3)

    def candle(X, h):
        a, b = q(X, Y0), q(X, Y0 + h)
        s.poly([(a[0] - 2.6, a[1]), (a[0] + 2.6, a[1]), (a[0] + 1.0, a[1] - 2.5), (a[0] - 1.0, a[1] - 2.5)], c("#e0b550", X, Y0 + 2))
        s.line([(a[0], a[1] - 2.5), (b[0], b[1] + 5)], c("#e0b550", X, Y0 + h / 2), 1.0)
        s.line([(b[0], b[1] + 5), (b[0], b[1])], c("#efe6d0", X, Y0 + h), 1.3)

    plate(-560, 26, "#3f68a8", "#dfe6f0", "#3f68a8")
    jug(-524, 24, "#e8e0cc", "#3f68a8")
    books(-474, 4)
    tray(-404, 40, 28, "#b88a4a", "#e0b550")
    cup(-352, 22)
    bottle(-322, 30, "#4a8a6a")
    candle(-286, 22)
    candle(-272, 22)
    ship(-206)
    jug(-128, 20, "#b8623a")
    plate(-70, 28, "#3f68a8", "#e6ecf4")
    books(-40, 2)
    engine(34)
    cup(84, 26)
    cup(104, 18, "#c8ccd4")
    bottle(142, 26, "#6a5a9a")
    plate(204, 30, "#3f8a8a", "#f0ead8", "#3f8a8a")
    jug(250, 26, "#d8cfb8", "#b0483c")
    books(290, 3)
    tray(356, 36, 26, "#c8ccd4", "#e8ecf0")
    ship(424)
    plate(486, 26, "#b0483c", "#f2e6d0")
    cup(530, 20)
    c_, a_ = s.done()
    over(L.rgb, c_, a_ * (1 - np.clip(info["solid"] * 2, 0, 1)))


def floor(L, info):
    s = Sheet(SHAPE)
    r = RUG
    rng = np.random.default_rng(SEED + 210)
    # the rug's fringe at its two ends, and the shadow of its thickness along the near edge
    hw, hd = (r["x1"] - r["x0"]) / 2, (r["z1"] - r["z0"]) / 2
    for sgn in (-1, 1):
        lz = -hd + 1.0
        while lz < hd - 0.5:
            ln = 5.5 + rng.random() * 3
            a_ = rug_pt(sgn * hw, lz, 0.3)
            b_ = rug_pt(sgn * (hw + ln), lz + rng.normal(0, 0.8), 0.3)
            s.line(pts2([a_, b_]), lit("#e2d2a6", a_), 0.7, 0.85)
            lz += 2.2
    s.line(pts2([rug_pt(-hw, -hd - 0.8, 0.2), rug_pt(hw, -hd - 0.8, 0.2)]), DARK, 1.3, 0.45)
    s.line(pts2([rug_pt(hw + 0.6, -hd, 0.2), rug_pt(hw + 0.6, hd, 0.2)]), DARK, 1.0, 0.3)
    s.line(pts2([rug_pt(-hw, -hd + 0.5, 0.4), rug_pt(hw, -hd + 0.5, 0.4)]), lit("#6a3a4a", rug_pt(0, -hd)), 0.9, 0.7)
    # one corner of it has turned up, as it always does
    c0 = rug_pt(-hw, -hd)
    s.poly(pts2([c0, rug_pt(-hw + 14, -hd, 0.5), rug_pt(-hw + 9, -hd + 7, 3.5), rug_pt(-hw, -hd + 12, 0.5)]), lit("#6a5a48", c0))
    s.line(pts2([rug_pt(-hw + 14, -hd, 0.5), rug_pt(-hw + 9, -hd + 7, 3.5), rug_pt(-hw, -hd + 12, 0.5)]), lit("#e2d2a6", c0), 0.8, 0.8)
    # the mat's bristles
    m = MAT
    for k in range(9):
        zz = lerp(m["z0"] + 8, m["z1"] - 8, k / 8)
        s.line(pts2([(m["x0"] + 9, 0.3, zz), (m["x1"] - 9, 0.3, zz)]), DARK, 0.7, 0.22)
    s.line(pts2([(m["x0"], 0.3, m["z0"] - 0.6), (m["x1"], 0.3, m["z0"] - 0.6)]), DARK, 1.1, 0.4)
    # knots and nail heads in the boards, a few scratches where chairs are dragged
    for k in range(70):
        X = rng.uniform(-460, 460)
        Z = rng.uniform(-10, ZW - 6)
        if r["x0"] - 12 < X < r["x1"] + 12 and r["z0"] - 12 < Z < r["z1"] + 12:
            continue
        p = P(X, 0, Z)
        if k % 3 == 0:
            s.ellipse(p[0], p[1], 1.1 * cam.scale(Z) + 0.3, 1.5 * cam.scale(Z), "#3a2416", 0.45)
        else:
            s.ellipse(p[0], p[1], 0.7, 0.5, "#2a1a12", 0.5)
    for k in range(9):
        X, Z = rng.uniform(-330, -120), rng.uniform(140, 215)
        a = rng.uniform(-0.5, 0.5)
        s.line(pts2([(X, 0, Z), (X + math.cos(a) * 16, 0, Z + math.sin(a) * 12 + 6)]), "#f6e2c0", 0.6, 0.22)
    L.sheet(s)


def ceiling(L, info):
    from home_living_room_room import BEAMS
    s = Sheet(SHAPE)
    x, y, z = PENDANT
    for zb in BEAMS:                                           # the beams' edges: light along the lower one, the grain, a crack or two
        y_near, y_far = ceil_pt(0, zb - 9)[1], ceil_pt(0, zb + 9)[1]
        drop = 15.0 * cam.scale(zb) * 0.72
        s.line([(0, y_near + drop), (W, y_near + drop)], "#ffd9a0", 0.9, 0.22)
        s.line([(0, y_far + drop + 0.5), (W, y_far + drop + 0.5)], "#0c0810", 1.2, 0.5)
        s.line([(0, y_near), (W, y_near)], "#0c0810", 1.0, 0.4)
    c = ceil_pt(x, z)                                          # the plaster rose the lamp hangs from
    rose = LIGHTS.tone(col("#e8dcc4") * LIGHTS.light(x, WALL_H, z, (0, -1, 0)))
    s.ellipse(c[0] + 1, c[1] + 1.5, 15, 5.4, "#0c0810", 0.35)
    s.ellipse(c[0], c[1], 14, 4.8, rose * 1.5)
    s.ellipse(c[0], c[1] + 0.4, 9.5, 3.0, rose * 1.15)
    s.ellipse(c[0], c[1] + 0.6, 3.2, 1.3, "#6a5020")
    # a hair crack in the plaster, wandering from the corner over the stairs
    rng = np.random.default_rng(SEED + 220)
    pts = [(700.0, CEIL_Y - 2.0)]
    for k in range(8):
        pts.append((pts[-1][0] - 6 - rng.random() * 9, pts[-1][1] - 1 - rng.random() * 2.5))
    s.line(pts, "#0c0810", 0.7, 0.32)
    L.sheet(s)


def clutter(L, info):
    """The small things of what was left lying about (see _room.clutter), and a few more that are only small."""
    st = STAIR
    z0, R = st["z0"], st["rise"]
    rng = np.random.default_rng(SEED + 230)
    s = Sheet(SHAPE)
    # the washing: folds, a stripe on the towel
    xa = stair_x(2) + 3
    for k in range(4):
        y = 2 * R + k * 4.5
        s.line(pts2([(xa, y, z0 + 26), (xa + 19, y, z0 + 26)]), DARK, 0.7, 0.35)
        s.line(pts2([(xa, y + 4.4, z0 + 26), (xa, y + 4.4, z0 + 58)]), "#ffffff", 0.6, 0.25)
    s.line(pts2([(xa + 4, 2 * R + 18.2, z0 + 26), (xa + 4, 2 * R + 18.2, z0 + 58)]), lit("#c8483c", (xa, 2 * R + 18, z0 + 40)), 1.0, 0.8)
    # the books: page edges
    xb = stair_x(4) + 4
    s.line(pts2([(xb, 4 * R + 1.6, z0 + 5.8), (xb + 15, 4 * R + 1.6, z0 + 5.8)]), lit("#efe8d4", (xb, 4 * R, z0)), 0.9, 0.85)
    s.line(pts2([(xb + 1.5, 4 * R + 5, z0 + 6.8), (xb + 14, 4 * R + 5, z0 + 6.8)]), lit("#efe8d4", (xb, 4 * R, z0)), 0.9, 0.85)
    # the bear, sitting on the carpet of the fifth step: honey-colored, with a blue ribbon
    Rb = st["rise"] * 5
    bx, bz = stair_x(5) + 12, z0 + 40
    fur = lambda y, d=1.0, c="#d8a85c": lit(c, (bx, y, bz), (-0.4, 0.4, -0.8), d)
    c = P(bx, Rb + 8, bz)
    k = cam.scale(bz) * 1.2
    s.ellipse(c[0] + 1.5, c[1] + 6.5 * k, 8.5 * k, 2.6 * k, DARK, 0.35)
    for sx in (-1, 1):
        s.ellipse(c[0] + sx * 6.8 * k, c[1] + 5.6 * k, 3.6 * k, 2.8 * k, fur(Rb + 2, 0.85))        # feet
        s.ellipse(c[0] + sx * 7.4 * k, c[1] - 1.0 * k, 2.6 * k, 4.2 * k, fur(Rb + 9, 0.85))        # arms
    s.ellipse(c[0], c[1], 7.2 * k, 8.2 * k, fur(Rb + 8, 0.92))
    s.ellipse(c[0] - 0.6, c[1] + 1, 4.0 * k, 5.0 * k, fur(Rb + 8, 1.0, "#f0d49a"))
    h = P(bx - 0.3, Rb + 20.5, bz)
    for sx in (-1, 1):
        s.ellipse(h[0] + sx * 4.6 * k, h[1] - 4.2 * k, 2.4 * k, 2.4 * k, fur(Rb + 24, 0.9))
        s.ellipse(h[0] + sx * 4.6 * k, h[1] - 4.0 * k, 1.2 * k, 1.2 * k, fur(Rb + 24, 1.0, "#f0d49a"))
    s.ellipse(h[0], h[1], 5.8 * k, 5.4 * k, fur(Rb + 20))
    s.ellipse(h[0] - 0.4, h[1] + 1.6 * k, 2.6 * k, 2.0 * k, fur(Rb + 19, 1.0, "#f6e2b4"))
    s.ellipse(h[0] - 0.4, h[1] + 0.9 * k, 0.9, 0.8, "#1c1418")
    for sx in (-1, 1):
        s.ellipse(h[0] + sx * 2.2 * k - 0.3, h[1] - 1.0 * k, 0.7, 0.7, "#1c1418")
    s.poly([(h[0] - 4.2 * k, h[1] + 4.6 * k), (h[0] + 4.2 * k, h[1] + 4.6 * k), (h[0] + 3.0 * k, h[1] + 6.6 * k), (h[0] - 3.0 * k, h[1] + 6.6 * k)], lit("#3f6f9f", (bx, Rb + 15, bz), (-0.4, 0.4, -0.8)))
    L.sheet(s)

    s = Sheet(SHAPE)
    # the waste-paper basket: its weave, and what was thrown at it
    za = ZW - 26.2
    for k in range(1, 6):
        s.line(pts2([(-186 + k * 3.7, 0, za), (-186 + k * 3.7, 30, za)]), DARK, 0.7, 0.30)
    for yy in (7, 15, 23):
        s.line(pts2([(-186, yy, za), (-164, yy, za)]), "#ffe2a8", 0.7, 0.22)
    s.line(pts2([(-186, 30, za), (-164, 30, za)]), lit("#e0b870", (-175, 30, za)), 1.0, 0.8)
    for (dx, dy, dz, r) in ((-4, 31, 8, 3.4), (3, 32, 12, 3.0), (-1, 34, 14, 2.6)):
        c = P(-175 + dx, dy, ZW - 22 + dz)
        s.ellipse(c[0], c[1], r, r * 0.85, lit("#f2eee0", (-175, 32, ZW - 15)))
        s.line([(c[0] - r * 0.6, c[1]), (c[0] + r * 0.2, c[1] - r * 0.4)], DARK, 0.6, 0.3)
    c = P(-150, 2.5, ZW - 34)                                             # one that missed
    s.ellipse(c[0] + 1.5, c[1] + 1, 3.4, 1.6, DARK, 0.35)
    s.ellipse(c[0], c[1], 2.8, 2.4, lit("#f2eee0", (-150, 3, ZW - 34)))
    # a ball that rolled to the wall and stayed there
    c = P(-206, 7, ZW - 14)
    s.ellipse(c[0] + 2, c[1] + 4, 5.5, 2.2, DARK, 0.4)
    s.ellipse(c[0], c[1], 5.0, 5.0, lit("#c8483c", (-206, 7, ZW - 14), (0.3, 0.4, -0.8)))
    s.ellipse(c[0] + 1.2, c[1] - 1.2, 3.2, 3.0, lit("#e8786a", (-206, 9, ZW - 14), (0.5, 0.6, -0.6)))
    s.line([(c[0] - 4.6, c[1] + 0.6), (c[0] + 4.8, c[1] - 1.0)], lit("#f2eee0", (-206, 7, ZW - 14)), 1.0, 0.85)
    # shoes left by the door: his, hers, small ones
    for k, (X, cc, sz) in enumerate(((-455, "#6a4a34", 1.0), (-446, "#6a4a34", 1.0), (-434, "#e8e2d8", 0.8), (-427, "#e8e2d8", 0.8))):
        zz = ZW - 12 - (k % 2) * 2
        c = P(X, 3, zz)
        s.ellipse(c[0] + 1, c[1] + 2, 3.4 * sz, 2.4 * sz, DARK, 0.4)
        s.ellipse(c[0], c[1], 3.0 * sz, 3.8 * sz, lit(cc, (X, 4, zz), (0, 0.6, -0.7)))
        s.ellipse(c[0], c[1] - 1.6 * sz, 2.0 * sz, 1.6 * sz, lit("#2a2024", (X, 6, zz)))
        if k >= 2:
            s.line([(c[0] - 2.6 * sz, c[1] + 2.2 * sz), (c[0] + 2.6 * sz, c[1] + 2.2 * sz)], lit("#c8483c", (X, 2, zz)), 1.0)
    L.sheet(s)

    # ---- on the wall: the skateboard propped by the door, the children's heights pencilled on the door frame
    s = Sheet(SHAPE)
    X0 = -448.0
    deck = [(X0 - 9.5, 12), (X0 - 8, 5), (X0, 3), (X0 + 8, 5), (X0 + 9.5, 12), (X0 + 9.5, 70), (X0 + 8, 77), (X0, 79), (X0 - 8, 77), (X0 - 9.5, 70)]
    s.poly([wp(x + 2.2, y - 1) for x, y in deck], DARK, 0.4)
    s.poly([wp(x, y) for x, y in deck], wl("#2a2630", X0, 40))
    s.poly([wp(X0 - 6, 28), wp(X0 + 6, 24), wp(X0 + 7, 44), wp(X0, 56), wp(X0 - 7, 42)], wl("#e8a030", X0, 40))            # a flame painted under it
    s.poly([wp(X0 - 3, 30), wp(X0 + 3.5, 28), wp(X0 + 4, 40), wp(X0, 48), wp(X0 - 4, 39)], wl("#d8483c", X0, 40))
    for yy in (16, 66):
        wline(s, [(X0 - 11, yy), (X0 + 11, yy)], wl("#b8bcc4", X0, yy), 1.6)
        for xx in (X0 - 12, X0 + 12):
            c = wp(xx, yy)
            s.ellipse(c[0], c[1], 2.3, 3.0, wl("#f0e8c8", xx, yy))
            s.ellipse(c[0], c[1], 0.8, 1.0, wl("#6a6a70", xx, yy))
    # the computer's cable, from under the desk to the socket
    wline(s, [(-164.5, 32), (-163, 20), (-158, 8), (-152, 3)], "#2a2428", 0.9, 0.8)
    L.sheet(s)



def scarf(L, info):
    """A long striped scarf left hanging over the newel post at the foot of the stairs."""
    st = STAIR
    z0 = st["z0"]
    s = Sheet(SHAPE)
    nx, zz = stair_x(1) - 9, z0 - 11.6
    wool = lambda y, c="#2f8a8a", d=1.0: lit(c, (nx, y, zz), (0, 0.2, -1), d)
    front = [(nx - 9.5, 119, zz), (nx - 1.0, 122, zz), (nx - 2.0, 62, zz), (nx - 11.5, 64, zz)]         # the long end, down the front of the post
    side = [(nx + 1.5, 122, zz), (nx + 9.5, 119, zz), (nx + 12, 90, zz), (nx + 5, 88, zz)]              # the short end
    over_top = [(nx - 9.5, 118, zz), (nx + 9.5, 118, zz), (nx + 7, 125, zz - 3), (nx - 7, 125, zz - 3)]
    s.poly(pts2([(x + 1.8, y - 1.5, z) for x, y, z in front]), DARK, 0.35)
    s.poly(pts2(front), wool(95))
    s.poly(pts2(side), wool(105, d=0.85))
    s.poly(pts2(over_top), wool(121, d=1.1))
    for k in range(9):
        y = 114 - k * 6.2
        t = (119 - y) / 57.0
        s.line(pts2([(lerp(nx - 9.5, nx - 11.5, t), y, zz - 0.1), (lerp(nx - 1.0, nx - 2.0, t), y + 1.4, zz - 0.1)]), wool(y, "#f2e6c8"), 1.5, 0.95)
        if k < 4:
            s.line(pts2([(lerp(nx + 1.5, nx + 5, k / 4), y + 1.4, zz - 0.1), (lerp(nx + 9.5, nx + 12, k / 4), y, zz - 0.1)]), wool(y, "#f2e6c8", 0.85), 1.5, 0.95)
    for k in range(5):
        s.line(pts2([(nx - 11 + k * 2.1, 63.5, zz), (nx - 11.4 + k * 2.1, 57, zz)]), wool(60, "#f2e6c8"), 0.8, 0.9)
        s.line(pts2([(nx + 5.6 + k * 1.5, 88.5, zz), (nx + 5.9 + k * 1.5, 83, zz)]), wool(85, "#f2e6c8"), 0.8, 0.9)
    s.line(pts2([front[0], front[3]]), DARK, 0.7, 0.35)
    L.sheet(s)


def details(L, info):
    wall(L, info)
    plate_rail(L, info)
    bookcase(L, True)
    clutter(L, info)
    stairs(L, True)
    scarf(L, info)
    small_things(L, True)
    floor(L, info)
    ceiling(L, info)

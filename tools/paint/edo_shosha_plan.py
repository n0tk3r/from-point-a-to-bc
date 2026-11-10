"""PAINT-23: the foot of Mount Shosha's SKELETON, drawn through its camera before any painting (DEPTH.md, "Perspective"):
the hall as boxes under its pyramid roof, the hut, the bench, the path's steps, the stone, the terrace's edge and the
plain's band, the near pine and the lantern (the front plane, tinted red), the walk outline, and stand-in people at
every mark and standing place at the size the game will draw them. If this is not a deep place with people the right
size in it, no painting will mend it: change edo_shosha_kit.py and look again.

    python3 edo_shosha_plan.py [out.png]        -> out/edo-shosha-skeleton.png

The magenta line is the game's `horizon` (eye level: the terrace is level); the grid lies on the terrace, a line every
metre away and every two metres across."""

import math
import sys

import numpy as np
from PIL import Image, ImageDraw

from edo_shosha_kit import *

WHO = {"mom": (168.0, (40, 170, 110)), "bigsis": (160.0, (70, 80, 190)), "lilsis": (122.0, (235, 120, 160)), "ume": (136.0, (150, 120, 160)),
       "monk": (150.0, (90, 90, 100)), "woman": (146.0, (120, 150, 200)), "old": (138.0, (60, 70, 140)), "girl": (138.0, (190, 140, 200))}


def person(d, S, place, who, label, seated=False):
    cm, colr = WHO[who]
    fx, fy = foot(*place)
    hp = grownup_px(fy) * cm / 175.0 * (0.74 if seated else 1.0)
    w = hp * (0.34 if seated else 0.27)
    d.ellipse(S([(fx - w * 0.8, fy - 3), (fx + w * 0.8, fy + 3)]), fill=(0, 0, 0, 90))
    d.rectangle(S([(fx - w / 2, fy - hp * 0.86), (fx + w / 2, fy)]), fill=colr + (255,), outline=(20, 20, 30))
    d.ellipse(S([(fx - hp * 0.08, fy - hp), (fx + hp * 0.08, fy - hp * 0.84)]), fill=(240, 200, 170), outline=(20, 20, 30))
    if label:
        d.text(((fx + w / 2 + 2) * 2, (fy - hp * 0.55) * 2), f"{label} {grownup_px(fy):.0f}", fill=(255, 255, 170))


def quad(d, S, pts, fill, outline=(30, 30, 40)):
    d.polygon(S(pts), fill=fill, outline=outline)


def hall(d, S):
    bo, bh = BASE_OUT, BASE_H
    # the base: its front and west faces, its top
    quad(d, S, [HP(-bo, -bo, 0), HP(SIDE + bo, -bo, 0), HP(SIDE + bo, -bo, bh), HP(-bo, -bo, bh)], (160, 160, 168))
    quad(d, S, [HP(-bo, SIDE + bo, 0), HP(-bo, -bo, 0), HP(-bo, -bo, bh), HP(-bo, SIDE + bo, bh)], (206, 200, 186))
    # the step before the doors
    st = STEP
    quad(d, S, [HP(st["a0"], -bo - st["out"], 0), HP(st["a1"], -bo - st["out"], 0), HP(st["a1"], -bo - st["out"], st["h"]), HP(st["a0"], -bo - st["out"], st["h"])], (150, 150, 160))
    quad(d, S, [HP(st["a0"], -bo - st["out"], st["h"]), HP(st["a1"], -bo - st["out"], st["h"]), HP(st["a1"], -bo, st["h"]), HP(st["a0"], -bo, st["h"])], (196, 196, 204))
    # the walls: the west side lit, the front at a slant
    quad(d, S, [HP(0, SIDE, bh), HP(0, 0, bh), HP(0, 0, EAVE_Y), HP(0, SIDE, EAVE_Y)], (226, 170, 96))
    quad(d, S, [HP(0, 0, bh), HP(SIDE, 0, bh), HP(SIDE, 0, EAVE_Y), HP(0, 0, EAVE_Y)], (160, 112, 72))
    da, db = DOOR_A
    dy0, dy1 = DOOR_Y
    quad(d, S, [HP(da, 0, dy0), HP(db, 0, dy0), HP(db, 0, dy1), HP(da, 0, dy1)], (70, 50, 46))
    la, lb = LATTICE_B
    ly0, ly1 = LATTICE_Y
    quad(d, S, [HP(0, la, ly0), HP(0, lb, ly0), HP(0, lb, ly1), HP(0, la, ly1)], (80, 56, 40))
    a, y = LOCK_AT
    quad(d, S, [HP(a - LOCK_W / 2, -4, y - LOCK_H / 2), HP(a + LOCK_W / 2, -4, y - LOCK_H / 2), HP(a + LOCK_W / 2, -4, y + LOCK_H / 2), HP(a - LOCK_W / 2, -4, y + LOCK_H / 2)], (30, 20, 20))
    # the eaves' underside and the roof's two faces we see
    e = EAVE_OUT
    ye = EAVE_Y - EAVE_DROP
    quad(d, S, [HP(0, 0, EAVE_Y), HP(SIDE, 0, EAVE_Y), HP(SIDE + e, -e, ye), HP(-e, -e, ye)], (80, 64, 70))
    quad(d, S, [HP(0, SIDE, EAVE_Y), HP(0, 0, EAVE_Y), HP(-e, -e, ye), HP(-e, SIDE + e, ye)], (96, 80, 84))
    apex = HP(SIDE / 2, SIDE / 2, APEX_Y)
    quad(d, S, [HP(-e, SIDE + e, ye), HP(-e, -e, ye), apex], (150, 156, 176))
    quad(d, S, [HP(-e, -e, ye), HP(SIDE + e, -e, ye), apex], (110, 116, 140))
    d.line(S([apex, (apex[0], apex[1] - 22)]), fill=(60, 50, 50), width=6)


def hut(d, S):
    hw, hd, wall = HUT["w"], HUT["d"], HUT["wall"]
    P_ = lambda a, b, y: P(*hut_at(a, b)[:1], y, hut_at(a, b)[1])
    quad(d, S, [P_(0, hd, 0), P_(0, 0, 0), P_(0, 0, wall), P_(0, hd, wall)], (210, 190, 150))
    quad(d, S, [P_(0, 0, 0), P_(hw, 0, 0), P_(hw, 0, wall), P_(0, 0, wall)], (170, 150, 120))
    e = HUT["eave"]
    quad(d, S, [P_(-e, -e, wall - 10), P_(hw + e, -e, wall - 10), P_(hw - 30, hd / 2, HUT["ridge"]), P_(30, hd / 2, HUT["ridge"])], (150, 120, 70))
    quad(d, S, [P_(-e, hd + e, wall - 10), P_(-e, -e, wall - 10), P_(30, hd / 2, HUT["ridge"])], (190, 160, 96))
    a, b, y = HUT_LANTERN_AB
    lp = P_(a, b, y)
    d.rectangle(S([(lp[0] - 5, lp[1]), (lp[0] + 5, lp[1] + 16)]), fill=(250, 240, 210), outline=(30, 30, 40))


def path(d, S):
    rise, tread = PATH_RISE, PATH_TREAD
    steps = []
    for i in range(PATH_N):
        s0, s1 = i * tread, (i + 1) * tread
        y0 = i * rise
        steps.append((s0, s1, y0, y0 + rise))
    for (s0, s1, y0, y1) in steps[::-1]:
        hw = PATH_W / 2
        a, b = path_at(s0, -hw), path_at(s0, hw)
        c, e = path_at(s1, hw), path_at(s1, -hw)
        quad(d, S, [P(a[0], y0, a[1]), P(b[0], y0, b[1]), P(b[0], y1, b[1]), P(a[0], y1, a[1])], (90, 92, 104), None)
        quad(d, S, [P(a[0], y1, a[1]), P(b[0], y1, b[1]), P(c[0], y1, c[1]), P(e[0], y1, e[1])], (170, 168, 160), None)


def box_up(d, S, X, D, w, h, t, fill):
    quad(d, S, [P(X - w / 2, 0, D), P(X + w / 2, 0, D), P(X + w / 2, h, D), P(X - w / 2, h, D)], fill)


def trunk(d, S, X, D, r, top, fill, outline=(24, 22, 34)):
    a, b = P(X - r, 0, D), P(X + r, 0, D)
    c, e = P(X + r * 0.8, top, D), P(X - r * 0.8, top, D)
    d.polygon(S([a, b, c, e]), fill=fill, outline=outline)


def skeleton(out="out/edo-shosha-skeleton.png", which="arrive"):
    ss = 2
    im = Image.new("RGB", (W * ss, H * ss), (196, 210, 226))
    d = ImageDraw.Draw(im, "RGBA")
    S = lambda pts: [(x * ss, y * ss) for x, y in pts]
    # the far: the plain below the horizon at the right, its far hills, the castle; the mountain's layers at the left
    d.rectangle([0, HZ * ss, W * ss, H * ss], fill=(170, 186, 150))
    d.polygon(S([(430, 300), (560, 312), (660, 318), (800, 322), (800, 336), (430, 336)]), fill=(150, 170, 200))       # the far hills
    cx_, cy_ = 742, 326
    d.rectangle(S([(cx_ - 8, cy_ - 16), (cx_ + 8, cy_)]), fill=(250, 250, 244), outline=(60, 60, 80))
    # the mountain: three layers, each paler
    for (pts, fill) in (([(-10, -10), (330, -10), (520, 120), (640, 236), (720, 300), (520, 330), (-10, 330)], (150, 176, 170)),
                        ([(-10, 20), (190, 30), (380, 140), (520, 250), (600, 330), (-10, 360)], (110, 140, 120)),
                        ([(-10, 140), (110, 150), (250, 220), (380, 300), (460, 400), (-10, 420)], (70, 100, 80))):
        d.polygon(S(pts), fill=fill)
    # the terrace (below the mountain's foot), and its edge at the right with the plain beyond it
    X, D, below = ground_grid()
    ground = np.zeros(SHAPE, dtype=bool)
    edge_pts = [foot(x, dd) for (x, dd) in EDGE]
    foot_pts = [foot(-1600, 2600), foot(-600, 2500), foot(-100, 2300), foot(300, 2100)]
    terr = foot_pts + edge_pts[1:] + [(820, edge_pts[-1][1]), (820, 610), (-10, 610), (-10, foot_pts[0][1])]
    d.polygon(S(terr), fill=(196, 176, 130))
    # the grid on the terrace: every metre away, every two across
    for dd in range(600, 4001, 100):
        d.line(S([foot(-3000, dd), foot(3000, dd)]), fill=(150, 130, 96, 200 if dd % 500 == 0 else 90), width=1)
    for xx in range(-3000, 3001, 200):
        d.line(S([foot(xx, 600), foot(xx, 6000)]), fill=(150, 130, 96, 90), width=1)
    d.line(S([(0, HZ), (W, HZ)]), fill=(255, 80, 255), width=2)
    # the road up at the bottom right
    rl = [foot(x - ROAD_W / 2, dd) for (x, dd) in ROAD]
    rr = [foot(x + ROAD_W / 2, dd) for (x, dd) in ROAD]
    d.polygon(S(rl + rr[::-1]), fill=(214, 196, 150, 200))
    # the trees at the mountain's foot (behind the hut and the path), the cherry
    for (X_, D_, r, top) in ((-1100, 2400, 30, 1400), (-560, 2600, 26, 1200), (-60, 2700, 24, 1300), (-900, 1900, 28, 1300), (300, 2900, 24, 1200)):
        trunk(d, S, X_, D_, r, top, (90, 70, 60))
    cx2, cy2 = foot(*CHERRY)
    d.ellipse(S([(cx2 - 40, cy2 - 130), (cx2 + 46, cy2 - 76)]), fill=(240, 196, 210), outline=(30, 30, 40))
    path(d, S)
    hut(d, S)
    # the stone
    sx, sd = STONE
    w_, h_, t_ = STONE_SIZE
    box_up(d, S, sx, sd, w_, h_, t_, (186, 186, 196))
    # the bench, the combs' cloth
    fl, fr, br, bl = bench_pts()
    bh = BENCH["h"]
    quad(d, S, [P(fl[0], bh, fl[1]), P(fr[0], bh, fr[1]), P(br[0], bh, br[1]), P(bl[0], bh, bl[1])], (170, 120, 80))
    quad(d, S, [P(fl[0], 0, fl[1]), P(fr[0], 0, fr[1]), P(fr[0], bh, fr[1]), P(fl[0], bh, fl[1])], (120, 84, 60))
    cx3, cd3 = COMBS
    quad(d, S, [foot(cx3 - 45, cd3 - 30), foot(cx3 + 45, cd3 - 30), foot(cx3 + 45, cd3 + 30), foot(cx3 - 45, cd3 + 30)], (110, 130, 190))
    hall(d, S)
    # the walk outline
    wk = walk_outline()
    d.line(S(wk + [wk[0]]), fill=(0, 255, 255), width=3)
    # stand-in people: the arrival (as the game stages it), or every mark and standing place
    M = MARKS_W
    person(d, S, M["ume"], "ume", "ume")
    person(d, S, M["ryokai"], "monk", "ryokai", seated=True)
    person(d, S, M["tome"], "old", "tome", seated=True)
    person(d, S, M["wife"], "woman", "wife", seated=True)
    person(d, S, M["girl"], "girl", "girl", seated=True)
    if which == "arrive":
        person(d, S, M["road"], "mom", "road")
        person(d, S, ARRIVE_W["road"][0], "bigsis", "")
        person(d, S, ARRIVE_W["road"][1], "lilsis", "")
    else:
        for name, who_ in (("hall", "mom"), ("stone", "bigsis"), ("hut", "lilsis"), ("view", "bigsis"), ("combs", "lilsis"), ("path", "mom"),
                           ("bench", "mom"), ("step", "lilsis"), ("lock", "bigsis")):
            person(d, S, M[name], who_, name)
        person(d, S, LATTICE_W, "monk", "lattice")
    # the front plane (tinted red): the old pine up the left edge, a great bough of it sweeping across the top into the
    # hall's peak, its roots and ferns along the bottom left; grass and ferns on the bank's lip in the bottom right corner
    n = NEAR_PINE
    a, b = P(n["X"] - n["r"], 0, n["D"]), P(n["X"] + n["r"], 0, n["D"])
    c, e = P(n["X"] + n["r"] * 0.8 + 70, 1000, n["D"]), P(n["X"] - n["r"] * 0.8 + 70, 1000, n["D"])
    d.polygon(S([a, b, c, e]), fill=(120, 40, 50, 225), outline=(20, 18, 26))
    d.polygon(S([(-10, -10), (560, -10), (548, 40), (520, 96), (486, 150), (450, 128), (380, 92), (300, 98), (220, 70), (150, 110), (60, 140), (-10, 150)]), fill=(120, 44, 54, 200))
    d.polygon(S([(-10, 610), (-10, 520), (50, 528), (110, 556), (170, 580), (240, 596), (250, 610)]), fill=(120, 44, 54, 200))
    d.polygon(S([(810, 610), (810, 548), (770, 560), (730, 584), (700, 610)]), fill=(120, 44, 54, 200))
    im = im.resize((W, H), Image.LANCZOS)
    im.save(out)
    return out


if __name__ == "__main__":
    print(skeleton("out/edo-shosha-skeleton.png", "arrive"))
    print(skeleton("out/edo-shosha-skeleton-marks.png", "marks"))

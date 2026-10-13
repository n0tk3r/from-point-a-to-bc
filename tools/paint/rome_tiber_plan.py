"""The skeleton of across the Tiber, before any painting: the model (rome_tiber_model.py) drawn through the scene's
camera as flat-shaded planes, with stand-in people at the size the game will draw them, the rows horizon and full,
and the marks. If this does not look like a quiet river bank with people of the right size in it, no painting will
mend it.

    python3 rome_tiber_plan.py [out.png]          (default out/rome-tiber-plan.png)"""

import math
import os
import sys

from PIL import Image, ImageDraw

import rome_tiber_model as M
from rome_tiber_model import P, along, out, D, N

KIND_H = {"son": 0.74, "mariam": 0.69, "felix": 1.0, "eleazar": 0.96, "egyptian": 1.0}


def poly(d, pts3, fill, outline=None):
    d.polygon([P(*p) for p in pts3], fill=fill, outline=outline)


def front_face(d, s0, s1, y0, y1, fill, inset=0.0):
    a, b = along(s0), along(s1)
    a, b = out(a, inset), out(b, inset)
    poly(d, [(a[0], y0, a[1]), (b[0], y0, b[1]), (b[0], y1, b[1]), (a[0], y1, a[1])], fill)


def person(d, who, x, y, scale=None, seated=False, color=(40, 40, 60)):
    s = scale if scale is not None else max(0.26, (y - M.HZ) / (M.FULL - M.HZ))
    h = KIND_H.get(who, 1.0) * 160 * s * (0.72 if seated else 1.0)
    w = h * 0.26
    d.rectangle([x - w / 2, y - h, x + w / 2, y], outline=color, width=2)
    d.ellipse([x - w * 0.35, y - h, x + w * 0.35, y - h + w * 0.7], outline=color, width=2)
    d.text((x - 10, y + 2), who, fill=color)


def draw(path):
    im = Image.new("RGB", (M.W, M.H), (150, 190, 230))
    d = ImageDraw.Draw(im)
    for r in range(0, M.HZ):                                       # sky
        t = r / M.HZ
        d.line([(0, r), (799, r)], fill=(int(70 + 150 * t), int(120 + 110 * t), int(200 + 40 * t)))
    # the far bank: the Aventine, the warehouses, the shore
    d.polygon([(0, 268), (0, 170), (60, 160), (140, 178), (220, 205), (300, 232), (360, 246), (M.VX, 250), (M.VX, 268)], fill=(150, 140, 175))
    d.polygon([(0, 272), (0, 252), (120, 255), (250, 258), (M.VX, 252), (M.VX, 262)], fill=(175, 160, 180))
    # the river
    far = P(M.FAR_BANK, M.WATER, 30000.0)
    d.polygon([(0, 266), (M.VX, 251), P(M.Q, M.WATER, 4000), P(M.Q, M.WATER, -60), (0, 600)], fill=(150, 170, 160))
    # the ground: the lane and the square
    poly(d, [(M.Q, 0, -60), (M.Q, 0, 60000), (3000, 0, 60000), (3000, 0, -60)], (205, 185, 150))
    L = M.LANDING
    poly(d, [(L["x0"], 0, L["z0"]), (L["x1"], 0, L["z0"]), (L["x1"], 0, L["z1"]), (L["x0"], 0, L["z1"])], (196, 180, 156))
    poly(d, [(L["x0"], M.WATER, L["z0"]), (L["x1"], M.WATER, L["z0"]), (L["x1"], 0, L["z0"]), (L["x0"], 0, L["z0"])], (120, 110, 110))   # its near face
    # the barge
    B = M.BARGE
    poly(d, [(B["xp"], B["gunwale"], B["z0"]), (B["xs"], B["gunwale"], B["z0"]), (B["xs"], B["gunwale"], B["z1"]), (B["xp"], B["gunwale"], B["z1"])], (110, 80, 60))
    poly(d, [(B["xs"], M.WATER, B["z0"]), (B["xs"], M.WATER, B["z1"]), (B["xs"], B["gunwale"], B["z1"]), (B["xs"], B["gunwale"], B["z0"])], (70, 50, 45))
    poly(d, [(B["xp"], M.WATER, B["z0"]), (B["xs"], M.WATER, B["z0"]), (B["xs"], B["gunwale"], B["z0"]), (B["xp"], B["gunwale"], B["z0"])], (90, 60, 50))
    poly(d, [(B["xp"] + 40, 70, B["z0"] + 250), (B["xs"] - 30, 70, B["z0"] + 250), (B["xs"] - 30, 70, B["z1"] - 300), (B["xp"] + 40, 70, B["z1"] - 300)], (200, 180, 130))
    poly(d, [(B["xp"] + 40, B["deck"], B["z0"] + 250), (B["xs"] - 30, B["deck"], B["z0"] + 250), (B["xs"] - 30, 70, B["z0"] + 250), (B["xp"] + 40, 70, B["z0"] + 250)], (170, 150, 100))
    mx, mz = (B["xp"] + B["xs"]) / 2, B["z1"] - 450
    d.line([P(mx, B["deck"], mz), P(mx, 390, mz)], fill=(60, 40, 30), width=2)
    # the road houses (fronts at ROAD_X, facing the river), then the garden wall and pines far off
    pend = along(M.PR["s1"])
    for z0, z1, h in ((pend[1], pend[1] + 900, 900), (pend[1] + 900, pend[1] + 1700, 700), (pend[1] + 1700, pend[1] + 2700, 760), (pend[1] + 2700, pend[1] + 4200, 650)):
        poly(d, [(M.ROAD_X, 0, z0), (M.ROAD_X, 0, z1), (M.ROAD_X, h, z1), (M.ROAD_X, h, z0)], (235, 200, 150))
        poly(d, [(M.ROAD_X, h, z0), (M.ROAD_X, h, z1), (M.ROAD_X + 300, h + 150, z1), (M.ROAD_X + 300, h + 150, z0)], (200, 110, 80))
    poly(d, [(M.ROAD_X, 0, pend[1] + 4200), (M.ROAD_X, 0, 30000), (M.ROAD_X, 300, 30000), (M.ROAD_X, 300, pend[1] + 4200)], (220, 210, 190))
    for zz in (9000, 12000, 16000, 21000):
        x, y = P(M.ROAD_X + 600, 1300, zz)
        r = 900 * M.k_at(zz)
        d.ellipse([x - r, y - r * 0.45, x + r, y + r * 0.45], fill=(70, 100, 70))
    # the house of prayer: front, roof
    front_face(d, M.PR["s0"], M.PR["s1"], 0, M.PR["eave"], (210, 190, 170))
    a, b = along(M.PR["s0"]), along(M.PR["s1"])
    ra, rb = (a[0] - N[0] * 500, a[1] - N[1] * 500), (b[0] - N[0] * 500, b[1] - N[1] * 500)
    poly(d, [(a[0], M.PR["eave"], a[1]), (b[0], M.PR["eave"], b[1]), (rb[0], M.PR["eave"] + 180, rb[1]), (ra[0], M.PR["eave"] + 180, ra[1])], (180, 100, 70))
    dp = M.DOOR_P
    front_face(d, dp["s0"], dp["s1"], 0, dp["h"], (60, 45, 50), 0.5)
    # Eleazar's house: front, roof, window, door
    front_face(d, M.EL["s0"], M.EL["s1"], 0, M.EL["eave"], (240, 200, 140))
    a, b = along(M.EL["s0"]), along(M.EL["s1"])
    ra, rb = (a[0] - N[0] * 450, a[1] - N[1] * 450), (b[0] - N[0] * 450, b[1] - N[1] * 450)
    poly(d, [(a[0], M.EL["eave"], a[1]), (b[0], M.EL["eave"], b[1]), (rb[0], M.EL["eave"] + 170, rb[1]), (ra[0], M.EL["eave"] + 170, ra[1])], (190, 95, 60))
    for w in (M.WINDOW, M.WINDOW2):
        front_face(d, w["s0"], w["s1"], w["sill"], w["top"], (50, 40, 50), 0.5)
    de = M.DOOR_E
    front_face(d, de["s0"], de["s1"], 0, de["h"], (50, 40, 50), 0.5)
    # the bench
    bn = M.BENCH
    a, b = out(along(bn["s0"]), bn["out"] - bn["deep"] / 2), out(along(bn["s1"]), bn["out"] - bn["deep"] / 2)
    c, e = out(along(bn["s0"]), bn["out"] + bn["deep"] / 2), out(along(bn["s1"]), bn["out"] + bn["deep"] / 2)
    poly(d, [(c[0], bn["h"], c[1]), (e[0], bn["h"], e[1]), (b[0], bn["h"], b[1]), (a[0], bn["h"], a[1])], (220, 215, 200))
    poly(d, [(c[0], 0, c[1]), (e[0], 0, e[1]), (e[0], bn["h"], e[1]), (c[0], bn["h"], c[1])], (160, 150, 150))
    # the hen yard: its fence
    y = M.YARD
    f0, f1 = out(along(y["s0"]), y["out"]), out(along(y["s1"]), y["out"])
    w0, w1 = along(y["s1"]), along(y["s0"])
    poly(d, [(f0[0], 0, f0[1]), (f1[0], 0, f1[1]), (w0[0], 0, w0[1]), (w1[0], 0, w1[1])], (185, 160, 120))
    poly(d, [(f0[0], 0, f0[1]), (f1[0], 0, f1[1]), (f1[0], y["fence"], f1[1]), (f0[0], y["fence"], f0[1])], (140, 110, 70))
    poly(d, [(f1[0], 0, f1[1]), (w0[0], 0, w0[1]), (w0[0], y["fence"], w0[1]), (f1[0], y["fence"], f1[1])], (120, 95, 60))
    # the well and the fig tree
    for (x, z, r, h, c) in ((M.WELL["x"], M.WELL["z"], M.WELL["r"], M.WELL["h"], (200, 195, 185)),):
        a, b = P(x - r, 0, z), P(x + r, 0, z)
        top = P(x, h, z)
        d.rectangle([a[0], top[1], b[0], a[1]], fill=c)
    fx, fz = out(along(M.FIG["s"]), M.FIG["out"])
    t0, t1 = P(fx, 0, fz), P(fx, 260, fz)
    d.line([t0, t1], fill=(90, 80, 70), width=4)
    cx, cy = P(fx + 20, 360, fz)
    r = 230 * M.k_at(fz)
    d.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], outline=(90, 130, 60), width=3)
    h0, h1 = out(along(M.HENS_ROW["s0"]), M.HENS_ROW["o0"]), out(along(M.HENS_ROW["s1"]), M.HENS_ROW["o1"])
    d.line([P(h0[0], 0, h0[1]), P(h1[0], 0, h1[1])], fill=(255, 255, 255), width=2)
    # rows
    d.line([(0, M.HZ), (799, M.HZ)], fill=(255, 0, 0))
    d.line([(0, M.FULL), (799, M.FULL)], fill=(255, 0, 255))
    d.line([(0, 545), (399, 545)], fill=(255, 255, 0))
    # stand-in people (at the layout's own marks: rome_tiber_layout.py)
    import rome_tiber_layout as LAY
    wm, _ = LAY.window_place()
    sx, sy = wm["at"]
    person(d, "eleazar", sx, sy, scale=wm["scale"], color=(200, 30, 30))
    bx, by = LAY.bench_seat()["at"]
    person(d, "eleazar", bx, by, seated=True, color=(200, 30, 30))
    person(d, "mariam", *LAY.marks()["mariam"]["at"])
    person(d, "felix", *P(-560, 0, 560))
    person(d, "felix", *P(-470, 0, 420))
    person(d, "son", *P(150, 0, 60))
    person(d, "son", *P(30, 0, 640))
    im.save(path)
    print(path, "eleazar at the window:", (round(sx), round(sy)), "scale", wm["scale"], " on the bench:", (round(bx), round(by)))


if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    draw(sys.argv[1] if len(sys.argv) > 1 else "out/rome-tiber-plan.png")

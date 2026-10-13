"""A quick skeleton of the Forum (rome-forum): every mass as a flat-lit polygon through the game's camera, with
stand-in people at the size the game draws them, to judge the layout before anything is painted.

    python3 rome_forum_mock.py        -> out/rome-forum-mock.png"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw

from rome_forum_model import *

SUNV = SUN


def shade(rgb, normal):
    """Flat light on a face with this outward normal (x, y, z)."""
    n = np.asarray(normal, float)
    n = n / np.linalg.norm(n)
    f = max(0.0, float(n @ np.asarray(SUNV)))
    f = min(1.0, f / 0.72) ** 0.6
    c = np.asarray(rgb, float) / 255.0
    lit = c * np.array([1.08, 1.0, 0.84]) * f + c * np.array([0.52, 0.56, 0.86]) * (1 - f) ** 1.4
    return tuple(int(v) for v in np.clip(lit * 255, 0, 255))


def main():
    im = Image.new("RGB", (W, H), (120, 170, 225))
    d = ImageDraw.Draw(im)
    for y in range(HZ + 1):                                  # sky
        t = y / HZ
        d.line([(0, y), (W, y)], fill=(int(60 + 170 * t), int(120 + 110 * t), int(205 + 30 * t)))
    # the hill
    hill = [(-10, 190), (40, 168), (100, 140), (160, 122), (250, 116), (340, 121), (400, 140), (450, 158), (500, 160), (540, 140), (590, 126), (660, 122), (720, 134), (770, 156), (810, 172), (810, 300), (-10, 300)]
    d.polygon(hill, fill=(170, 175, 140))
    # ground
    d.rectangle([0, HZ, W, H], fill=(214, 196, 160))

    def face(pts3, fr, color, normal):
        d.polygon([fr.pt(*p) for p in pts3], fill=shade(color, normal))

    def box(fr, u0, u1, v0, v1, h0, h1, color, top=True):
        eu, ev = fr.eu, fr.ev
        # outward normals in world (x, y, z): front (-v), right (+u), left (-u), top
        nf = (-ev[0], 0, -ev[1]); nr = (eu[0], 0, eu[1]); nl = (-eu[0], 0, -eu[1])
        cam_u, cam_v = fr.find(VX, 1e7)
        if cam_u > u1:
            face([(u1, v0, h0), (u1, v1, h0), (u1, v1, h1), (u1, v0, h1)], fr, color, nr)
        if cam_u < u0:
            face([(u0, v0, h0), (u0, v1, h0), (u0, v1, h1), (u0, v0, h1)], fr, color, nl)
        face([(u0, v0, h0), (u1, v0, h0), (u1, v0, h1), (u0, v0, h1)], fr, color, nf)
        if top and h1 < EYE:
            face([(u0, v0, h1), (u1, v0, h1), (u1, v1, h1), (u0, v1, h1)], fr, color, (0, 1, 0))

    # ---- the Capitol's buildings (far)
    J = JUPITER
    jf = frame(J["angle"], J["x"], J["D"])
    box(jf, 0, J["width"], 0, J["length"], 3900, 3900 + J["podium"] + J["cols"], (236, 226, 200))
    m = MONETA
    mf = frame(m["angle"], m["x"], m["D"])
    box(mf, 0, m["width"], 0, 2400, 3800, 3800 + m["podium"] + m["cols"], (236, 220, 190))
    t = TABULARIUM
    d.polygon([pt(t["x0"], t["h0"], t["D"]), pt(t["x1"], t["h0"], t["D"]), pt(t["x1"], t["h2"], t["D"]), pt(t["x0"], t["h2"], t["D"])], fill=shade((222, 200, 160), (0, 0, -1)))
    # ---- Concord
    c = CONCORD
    cf = frame(c["angle"], c["x"], c["D"])
    box(cf, 0, c["width"], 0, 2600, 0, c["podium"] + c["cols"] + 300, (230, 214, 186))
    # ---- Saturn (the steps' temple: 14.15 m across, podium 2.52 m, columns 6.1 m, roof to 12.3 m)
    s = SATURN
    sf = frame(s["angle"], s["x"], s["D"])
    box(sf, 0, 1415, -60, 1900, 0, 252, (201, 181, 146))
    box(sf, 90, 1325, -554, -60, 0, 120, (242, 234, 216))
    box(sf, 45, 1370, 0, 1900, 252, 252 + 610 + 150, (235, 220, 190))
    face([(15, -6, 1012), (707, -6, 1227), (1400, -6, 1012)], sf, (110, 150, 166), (-sf.ev[0], 0, -sf.ev[1]))
    # ---- the speakers' platform
    r = ROSTRA
    pts = []
    for i in range(13):
        tt = i / 12
        x = r["x0"] + (r["x1"] - r["x0"]) * tt
        D = r["D"] - r["bulge"] * math.sin(math.pi * tt)
        pts.append((x, D))
    d.polygon([pt(x, 0, D) for x, D in pts] + [pt(x, r["h"], D) for x, D in reversed(pts)], fill=shade((228, 210, 180), (0, 0, -1)))
    # ---- Julia (left, beyond the street)
    j = JULIA
    d.polygon([pt(j["x"], 0, j["D0"]), pt(j["x"], 0, j["D1"]), pt(j["x"], j["h2"], j["D1"]), pt(j["x"], j["h2"], j["D0"])], fill=shade((240, 236, 226), (1, 0, 0)))
    d.polygon([pt(j["x"] - 2000, 0, j["D0"]), pt(j["x"], 0, j["D0"]), pt(j["x"], j["h2"], j["D0"]), pt(j["x"] - 2000, j["h2"], j["D0"])], fill=shade((240, 236, 226), (0, 0, -1)))
    # the far side of the Tuscan street (a house front facing us, deep in the street)
    d.polygon([pt(j["x"] - 3000, 0, TUSCAN["D0"]), pt(j["x"], 0, TUSCAN["D0"]), pt(j["x"], 800, TUSCAN["D0"]), pt(j["x"] - 3000, 800, TUSCAN["D0"])], fill=(120, 110, 140))
    # ---- Paullus (right)
    p = PAULLUS
    d.polygon([pt(p["x"], 0, p["D0"]), pt(p["x"], 0, p["D1"]), pt(p["x"], p["h2"], p["D1"]), pt(p["x"], p["h2"], p["D0"])], fill=shade((236, 222, 196), (-1, 0, 0)))
    # ---- the site: the crane (A-frame), the hoarding
    cr = CRANE
    foot = pt(cr["x"], 0, cr["D"])
    top = pt(cr["x"] - 250, 1350, cr["D"] - 300)
    d.line([foot, top], fill=(120, 90, 60), width=5)
    d.line([pt(cr["x"] + 200, 0, cr["D"] + 150), top], fill=(120, 90, 60), width=5)
    d.ellipse([foot[0] - 50, foot[1] - 110, foot[0] + 50, foot[1] - 10], outline=(110, 80, 50), width=4)
    blk = pt(cr["x"] - 250, 700, cr["D"] - 300)
    d.line([top, blk], fill=(60, 50, 40), width=1)
    d.rectangle([blk[0] - 14, blk[1], blk[0] + 14, blk[1] + 20], fill=(230, 225, 215))
    hd = HOARD
    (ax, aD), (bx, bD) = hd["a"], hd["b"]
    g0, g1 = hd["gate"]
    for (t0, t1) in ((0.0, g0), (g1, 1.0)):
        x0, D0 = ax + (bx - ax) * t0, aD + (bD - aD) * t0
        x1, D1 = ax + (bx - ax) * t1, aD + (bD - aD) * t1
        d.polygon([pt(x0, 0, D0), pt(x1, 0, D1), pt(x1, hd["h"], D1), pt(x0, hd["h"], D0)], fill=shade((170, 130, 90), (-0.99, 0, -0.12)))
    # ---- Castor (near left)
    cc = CASTOR
    kf = castor_frame()
    vf = castor_steps_foot()
    box(kf, 0, cc["width"], -cc["porch"], 2600, 0, cc["podium"], (210, 196, 170))
    for i in range(cc["steps"]):
        vv = vf + i * cc["tread"]
        box(kf, 100, cc["width"] - 40, vv, -cc["porch"], i * cc["rise"], (i + 1) * cc["rise"], (236, 226, 206))
    for i in range(8):
        u = cc["width"] - 70 - i * cc["gap"]
        b0 = kf.pt(u - 55, -10, cc["podium"])
        b1 = kf.pt(u + 55, -10, cc["podium"] + cc["cols"])
        d.rectangle([b0[0], b1[1], b1[0], b0[1]], fill=shade((240, 232, 212), (0, 0, -1)))
    # ---- the basin
    b = BASIN
    d.polygon([pt(b["x0"], b["h"], b["D0"]), pt(b["x1"], b["h"], b["D0"]), pt(b["x1"], b["h"], b["D1"]), pt(b["x0"], b["h"], b["D1"])], fill=(120, 160, 170))
    d.polygon([pt(b["x0"], 0, b["D0"]), pt(b["x1"], 0, b["D0"]), pt(b["x1"], b["h"], b["D0"]), pt(b["x0"], b["h"], b["D0"])], fill=shade((210, 200, 180), (0, 0, -1)))
    # ---- the Puteal, the table, the statues
    pu = PUTEAL
    c0, c1 = pt(pu["x"] - pu["r"], 0, pu["D"]), pt(pu["x"] + pu["r"], pu["h"], pu["D"])
    d.rectangle([c0[0], c1[1], c1[0], c0[1]], fill=shade((220, 210, 190), (0, 0, -1)))
    tb = TABLE
    c0, c1 = pt(tb["x"] - tb["w"] / 2, 0, tb["D"]), pt(tb["x"] + tb["w"] / 2, tb["h"], tb["D"])
    d.rectangle([c0[0], c1[1], c1[0], c0[1]], fill=shade((160, 110, 70), (0, 0, -1)))
    a0, a1 = pt(tb["x"] - 110, tb["awning"], tb["D"] - 20), pt(tb["x"] + 110, tb["awning"] + 15, tb["D"] - 20)
    d.rectangle([a0[0], a1[1], a1[0], a0[1]], fill=(200, 80, 60))
    for (x, D, hc) in STATUES:
        b0, b1 = pt(x - 45, 0, D), pt(x + 45, 150, D)
        d.rectangle([b0[0], b1[1], b1[0], b0[1]], fill=shade((225, 214, 190), (0, 0, -1)))
        c0, c1 = pt(x - 22, 150, D), pt(x + 22, 150 + hc, D)
        d.rectangle([c0[0], c1[1], c1[0], c0[1]], fill=shade((235, 225, 205), (0, 0, -1)))
        s0, s1 = pt(x - 18, 150 + hc, D), pt(x + 18, 150 + hc + 180, D)
        d.rectangle([s0[0], s1[1], s1[0], s0[1]], fill=(70, 95, 80))
    fb = FRONT_BASE
    c0, c1 = pt(fb["x"] - fb["w"] / 2, 0, fb["D"]), pt(fb["x"] + fb["w"] / 2, fb["h"], fb["D"])
    d.rectangle([c0[0], c1[1], c1[0], c0[1]], fill=shade((225, 214, 190), (0, 0, -1)))
    # ---- stand-in people: a boy (0.74) and a grown man, at the size the game draws them
    def person(x, D, height=1.0, color=(30, 40, 120)):
        foot = pt(x, 0, D)
        hpx = 160 * height * scale_at(foot[1])
        d.rectangle([foot[0] - hpx * 0.13, foot[1] - hpx, foot[0] + hpx * 0.13, foot[1]], fill=color)
        return foot, hpx
    sat_foot = sf.pt(700, -600, 0)
    print("Saturn's steps' foot", [round(v) for v in sat_foot], "boy there", round(160 * 0.74 * scale_at(sat_foot[1]), 1))
    for (x, D, hh, colr) in ((sat_foot[0], None, 0.74, (40, 40, 160)),):
        xx, DD = x_of(sat_foot[0], sat_foot[1])
        print(person(xx, DD, hh, colr))
    print("gaul", person(330, 1900, 1.08, (200, 40, 40)))
    print("phyllis (standing)", person(*PHYLLIS, 0.94, (200, 40, 160)))
    print("boy mid", person(-60, 2600, 0.74))
    print("boy near", person(80, 1100, 0.74))
    d.line([(0, HZ), (W, HZ)], fill=(255, 0, 0))
    im.save("out/rome-forum-mock.png")
    print("out/rome-forum-mock.png")


if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    main()

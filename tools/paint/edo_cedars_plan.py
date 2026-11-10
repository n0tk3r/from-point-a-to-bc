"""PAINT-23: the cedar path's SKELETON, drawn through its camera before any painting (DEPTH.md, "Perspective"): a box for
the storehouse under its thatch, a dome for the kiln, cylinders for the trunks, the steps, the walk outline, and stand-in
people at every mark and standing place at the size the game will draw them. If this is not a deep place with people the
right size in it, no painting will mend it: change edo_cedars_kit.py and look again.

    python3 edo_cedars_plan.py [out.png]        -> out/edo-cedars-skeleton.png

What to read in it: the magenta line is the game's `horizon` (the row the climbing hillside runs back to), the yellow line
eye level (lower: we look up at the storehouse); the grid lies on the hillside, a square every metre away and every two
metres across; the far trunks are three stand-in ranks; the front plane's things are tinted red."""

import math
import sys

import numpy as np
from PIL import Image, ImageDraw

from edo_cedars_kit import *

WHO = {"mom": (168.0, (40, 170, 110)), "bigsis": (160.0, (70, 80, 190)), "lilsis": (122.0, (235, 120, 160)), "man": (156.0, (170, 140, 90))}


def person(d, S, place, who, label):
    cm, colr = WHO[who]
    fx, fy = on(*place)
    hp = grownup_px(fy) * cm / 175.0                 # as the game draws them: by the row of the feet
    w = hp * 0.27
    d.ellipse(S([(fx - w * 0.8, fy - 3), (fx + w * 0.8, fy + 3)]), fill=(0, 0, 0, 90))
    d.rectangle(S([(fx - w / 2, fy - hp * 0.86), (fx + w / 2, fy)]), fill=colr + (255,), outline=(20, 20, 30))
    d.ellipse(S([(fx - hp * 0.08, fy - hp), (fx + hp * 0.08, fy - hp * 0.84)]), fill=(240, 200, 170), outline=(20, 20, 30))
    if label:
        d.text(((fx + w / 2 + 2) * 2, (fy - hp * 0.55) * 2), f"{label} {grownup_px(fy):.0f}", fill=(255, 255, 170))


def trunk(d, S, spec, fill, outline=(24, 22, 34)):
    px, py, r, lean = spec
    L, R = trunk_edges((px, py), r, lean)
    x, dd = G(px, py)
    fa, fb = on(x - r * 2.0, dd), on(x + r * 2.0, dd)
    a, b = on(x - r, dd, r * 2.2), on(x + r, dd, r * 2.2)
    d.polygon(S([fa, fb, b, a]), fill=fill)                                   # the roots' spread
    d.polygon(S(L + R[::-1]), fill=fill, outline=outline)


def skeleton(out="out/edo-cedars-skeleton.png"):
    ss = 2
    im = Image.new("RGB", (W * ss, H * ss), (198, 207, 214))
    d = ImageDraw.Draw(im, "RGBA")
    S = lambda pts: [(x * ss, y * ss) for x, y in pts]
    # the hillside below its vanishing line, and a grid on it: every metre away, every 2 m across
    d.rectangle([0, HZ * ss, W * ss, H * ss], fill=(122, 130, 112))
    for dd in list(range(300, 2001, 100)) + list(range(2200, 8001, 400)):
        d.line(S([on(-4000, dd), on(4000, dd)]), fill=(84, 96, 86, 230 if dd % 500 == 0 else 110), width=1)
    for xx in range(-3000, 3001, 200):
        d.line(S([on(xx, 300), on(xx, 12000)]), fill=(84, 96, 86, 110), width=1)
    d.line(S([(0, HZ), (W, HZ)]), fill=(255, 80, 255), width=2)               # the game's horizon: where the hillside runs to
    d.line(S([(0, TRUE_HZ), (W, TRUE_HZ)]), fill=(255, 200, 0), width=2)      # eye level
    # the far trunks (stand-ins: three ranks, each paler)
    rng = np.random.default_rng(4)
    for (d0, d1, n, tone) in ((5200, 9000, 26, 180), (3200, 5000, 20, 162), (2300, 3100, 12, 144)):
        for _ in range(n):
            dd = rng.uniform(d0, d1)
            x = rng.uniform(-0.75, 0.75) * dd
            L, R = trunk_edges(None, 36.0, 0.0, x=x, d=dd)
            d.polygon(S(L + R[::-1]), fill=(tone, tone + 8, tone + 16))
    # the backdrop's trunks that stand behind the storehouse
    hd = HOUSE.corner[1]
    for spec in sorted(TRUNKS_MID, key=lambda t: t[1]):
        if G(spec[0], spec[1])[1] > hd + 200:
            trunk(d, S, spec, (128, 120, 128))
    # the cut bank behind the storehouse's far end, with the pipe
    d.polygon(S(BANK_FOOT + BANK_TOP[::-1]), fill=(100, 94, 86))
    d.line(S(list(pipe_ends())), fill=(214, 196, 130), width=6)
    # the kiln: a dome, its mouth toward the yard
    kx, kd = KILN["at"]
    r, h = KILN["r"], KILN["h"]
    dome = [on(kx + r * math.cos(a), kd, h * math.sin(a) ** 0.85) for a in np.linspace(0, math.pi, 22)]
    front = [on(kx - r * math.cos(b), kd - r * 0.92 * math.sin(b)) for b in np.linspace(0, math.pi, 16)]
    d.polygon(S(dome + front[1:-1]), fill=(118, 98, 78), outline=(30, 26, 30))
    ma = math.radians(-52.0)
    mx, md = kx + r * 0.98 * math.cos(ma), kd + r * 0.98 * math.sin(ma)
    tx, td_ = -math.sin(ma), math.cos(ma)
    d.polygon(S([on(mx + tx * w, md + td_ * w, hh) for (w, hh) in ((-30, 0), (-30, 34), (-22, 52), (-8, 62), (8, 62), (22, 52), (30, 34), (30, 0))]), fill=(22, 20, 28))
    # the steps: each tread level, each riser its own height
    ft, fy = foot_tread()
    d.polygon(S([level(x, dd, fy) for (x, dd) in ft]), fill=(150, 152, 162))
    for st in steps():
        d.polygon(S([level(x, dd, st["Y"]) for (x, dd) in st["tread"]]), fill=(156, 158, 168))
    for st in steps():
        d.polygon(S([level(*st["l"], st["Y0"]), level(*st["r"], st["Y0"]), level(*st["r"], st["Y"]), level(*st["l"], st["Y"])]), fill=(74, 76, 96))
    # the storehouse: under the floor, the two walls, the door and the window, the thatch's cut edge, its two slopes, the ridge
    Hs = HOUSE
    LW, LD, e = Hs.LW, Hs.LD, Hs.eave
    yu, yt = Hs.eave_under, Hs.eave_top
    d.polygon(S([Hs.foot(0, 0), Hs.foot(LW, 0), Hs.pt(LW, 0, 0), Hs.pt(0, 0, 0)]), fill=(26, 26, 40))
    d.polygon(S([Hs.foot(0, 0), Hs.foot(0, LD), Hs.pt(0, LD, 0), Hs.pt(0, 0, 0)]), fill=(34, 32, 46))
    for u in Hs.posts_w:
        d.line(S([Hs.foot(u, 0), Hs.pt(u, 0, 0)]), fill=(90, 70, 60), width=4)
    for w in Hs.posts_d:
        d.line(S([Hs.foot(0, w), Hs.pt(0, w, 0)]), fill=(110, 86, 70), width=4)
    d.polygon(S([Hs.pt(0, 0, 0), Hs.pt(LW, 0, 0), Hs.pt(LW, 0, yu + 20), Hs.pt(0, 0, yu + 20)]), fill=(104, 78, 62), outline=(30, 30, 40))   # the window's wall (the shade side)
    d.polygon(S([Hs.pt(0, 0, 0), Hs.pt(0, LD, 0), Hs.pt(0, LD, yu + 20), Hs.pt(0, 0, yu + 20)]), fill=(134, 102, 78), outline=(30, 30, 40))  # the door wall (toward the gap)
    d0, d1, dh = Hs.door
    d.polygon(S([Hs.pt(0, d0, 0), Hs.pt(0, d1, 0), Hs.pt(0, d1, dh), Hs.pt(0, d0, dh)]), fill=(58, 44, 42), outline=(20, 20, 30))
    w0, w1, ws, wh = Hs.window
    d.polygon(S([Hs.pt(w0, 0, ws), Hs.pt(w1, 0, ws), Hs.pt(w1, 0, wh), Hs.pt(w0, 0, wh)]), fill=(244, 216, 130), outline=(20, 20, 30))
    (r0u, r0w), (r1u, r1w) = Hs.ridge_at
    A0u, B0u, D0u = Hs.pt(-e, -e, yu), Hs.pt(LW + e, -e, yu), Hs.pt(-e, LD + e, yu)
    A0t, B0t, D0t = Hs.pt(-e, -e, yt), Hs.pt(LW + e, -e, yt), Hs.pt(-e, LD + e, yt)
    R0, R1 = Hs.pt(r0u, r0w, Hs.ridge), Hs.pt(r1u, r1w, Hs.ridge)
    d.polygon(S([A0t, B0t, R1, R0]), fill=(128, 114, 92), outline=(30, 30, 40))        # the long slope, over the window's wall
    d.polygon(S([A0t, D0t, R0]), fill=(154, 136, 106), outline=(30, 30, 40))           # the hip, over the door
    d.polygon(S([A0u, B0u, B0t, A0t]), fill=(78, 68, 62), outline=(30, 30, 40))        # the thatch's cut edge
    d.polygon(S([A0u, D0u, D0t, A0t]), fill=(96, 84, 70), outline=(30, 30, 40))
    d.line(S([R0, R1]), fill=(226, 216, 186), width=5)
    d.polygon(S([Hs.foot(-12, 50), Hs.foot(-12, 164), Hs.foot(-84, 158), Hs.foot(-80, 56)]), fill=(150, 150, 160))   # the stone before the door
    # the stone figure
    jx, jd = JIZO["at"]
    a, b, t = on(jx - 13, jd), on(jx + 13, jd), on(jx, jd, JIZO["h"])
    d.rectangle(S([(a[0], t[1]), (b[0], a[1])]), fill=(172, 176, 182), outline=(40, 40, 50))
    d.rectangle(S([(a[0], t[1] + (a[1] - t[1]) * 0.36), (b[0], t[1] + (a[1] - t[1]) * 0.56)]), fill=(214, 63, 42))
    # the trunks nearer than the storehouse's back, far to near; the two that people walk behind in a warmer brown
    near_mid = [(s, (128, 120, 128)) for s in TRUNKS_MID if G(s[0], s[1])[1] <= hd + 200]
    cuts = [(s, (104, 66, 60)) for s in CEDAR_L + CEDAR_R]
    for spec, colr in sorted(near_mid + cuts, key=lambda t: t[0][1]):
        trunk(d, S, spec, colr + (255,))
    # the walk outline and the blocked patch
    d.line(S(WALK + [WALK[0]]), fill=(0, 255, 255), width=3)
    for bl in BLOCKED:
        d.line(S(list(bl) + [bl[0]]), fill=(255, 120, 0), width=2)
    # people at every mark and standing place, as the game sizes them
    person(d, S, MARKS["enter"], "mom", "enter")
    person(d, S, ARRIVE["enter"][0], "bigsis", "")
    person(d, S, ARRIVE["enter"][1], "lilsis", "")
    person(d, S, MARKS["door"], "mom", "door")
    person(d, S, MARKS["window"], "lilsis", "window")
    person(d, S, LIFT_AT, "mom", "lift")
    person(d, S, MARKS["pipe"], "bigsis", "pipe")
    person(d, S, MARKS["figure"], "lilsis", "figure")
    person(d, S, KILN_STAND, "bigsis", "kiln")
    person(d, S, ISUKE_WAY[3], "man", "isuke")
    # the front plane (tinted red): the great cedar on its bank, a bough across the top right corner, ferns in the bottom corners
    n = NEAR
    L, R = trunk_edges(None, n["r"], 0.6, x=n["x"], d=n["d"], base=n["bank"], top=2600.0)
    d.polygon(S(L + R[::-1]), fill=(120, 40, 50, 225), outline=(20, 18, 26))
    d.polygon(S([(0, 520), (60, 512), (104, 540), (150, 588), (168, 606), (0, 606)]), fill=(120, 44, 54, 215))      # its roots, and the ferns at its foot
    d.polygon(S([(820, -10), (590, -10), (604, 60), (640, 130), (700, 150), (740, 190), (820, 200)]), fill=(120, 44, 54, 215))
    d.polygon(S([(820, 610), (640, 610), (676, 568), (740, 530), (820, 520)]), fill=(120, 44, 54, 215))
    im = im.resize((W, H), Image.LANCZOS)
    im.save(out)
    return out


if __name__ == "__main__":
    print(f"eye {EYE:.0f} cm above the hillside; eye level at row {TRUE_HZ:.0f}; the game's horizon {HZ}, full {FULL}")
    for r, true, game in sizes():
        print(f"  row {r}: a grown-up {true:6.1f} px (the engine draws {game:6.1f})")
    print(skeleton(sys.argv[1] if len(sys.argv) > 1 else "out/edo-cedars-skeleton.png"))

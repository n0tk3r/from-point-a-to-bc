"""PAINT-23: Nishikurasawa's SKELETON, drawn through its new camera before any painting (DEPTH.md, "Perspective"): the
ground with a grid on it (a line every metre away, every two metres across), the road, the teahouse as boxes under its
hip roof, the mound and the hackberry, the palanquin, the trunks, the grill, the bench and the sign, the bank, Mount
Satta and Fuji as flat shapes, the near plane tinted red, the walk outline, and stand-in people at every mark and
standing place at the size the game will draw them.

    python3 edo_kurasawa_plan.py [out.png]        -> out/edo-kurasawa-skeleton.png

The magenta line is the scene's `horizon` (eye level: the ground here is level)."""

import math
import sys

import numpy as np
from PIL import Image, ImageDraw

import edo_kurasawa_view as V
from edo_kurasawa_view import *

WHO = {"mom": (168.0, (40, 170, 110)), "bigsis": (160.0, (70, 80, 190)), "lilsis": (122.0, (235, 120, 160)), "man": (156.0, (170, 140, 90)),
       "woman": (146.0, (190, 110, 90))}


def box(d, S, corners, height, fills, base=0.0):
    """A box on the ground: `corners` four ground places (X, Z) counter-clockwise seen from above; the faces we see,
    far ones first, then the top."""
    pts = [P(X, Z, base) for X, Z in corners]
    top = [P(X, Z, base + height) for X, Z in corners]
    faces = []
    for i in range(4):
        a, b = corners[i], corners[(i + 1) % 4]
        nx, nz = b[1] - a[1], -(b[0] - a[0])                       # the outward normal (corners go counter-clockwise from above)
        mx, mz = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        if nx * (0 - mx) + nz * (0 - mz) > 0:                       # it faces the lens
            dist = math.hypot(mx, mz)
            faces.append((dist, [pts[i], pts[(i + 1) % 4], top[(i + 1) % 4], top[i]], fills[i % len(fills)]))
    for _, f, c in sorted(faces, key=lambda t: -t[0]):
        d.polygon(S(f), fill=c, outline=(30, 30, 40))
    if base + height < EYE:
        d.polygon(S(top), fill=fills[-1], outline=(30, 30, 40))


def person(d, S, x, y, who, label=""):
    cm, colr = WHO[who]
    hp = grownup_px(y) * cm / 175.0
    w = hp * 0.27
    d.ellipse(S([(x - w * 0.8, y - 3), (x + w * 0.8, y + 3)]), fill=(0, 0, 0, 90))
    d.rectangle(S([(x - w / 2, y - hp * 0.86), (x + w / 2, y)]), fill=colr + (255,), outline=(20, 20, 30))
    d.ellipse(S([(x - hp * 0.08, y - hp), (x + hp * 0.08, y - hp * 0.84)]), fill=(240, 200, 170), outline=(20, 20, 30))
    if label:
        d.text(((x + w / 2 + 2) * 2, (y - hp * 0.6) * 2), f"{label} {grownup_px(y):.0f}", fill=(255, 255, 170), stroke_width=2, stroke_fill=(0, 0, 0))


def skeleton(out="out/edo-kurasawa-skeleton.png"):
    ss = 2
    im = Image.new("RGB", (W * ss, H * ss), (196, 214, 232))
    d = ImageDraw.Draw(im, "RGBA")
    S = lambda pts: [(x * ss, y * ss) for x, y in pts]
    # ---- the far plane: Fuji, the bay, the far shore, the capes, Satta and the cliff road
    d.polygon(S(V.FUJI_OUTLINE), fill=(150, 170, 205))
    d.polygon(S(V.FUJI_SNOW), fill=(246, 246, 250))
    d.polygon(S(V.CAP), fill=(250, 250, 255), outline=(120, 140, 170))
    d.polygon(S([(-10, HZ), (810, HZ), (810, 520), (-10, 520)]), fill=(70, 120, 180))
    d.polygon(S(V.FAR_SHORE), fill=(120, 150, 150))
    for cape in V.CAPES:
        d.polygon(S(cape), fill=(96, 130, 130))
    d.polygon(S(V.SATTA), fill=(40, 84, 66))
    d.line(S(V.CLIFF_ROAD), fill=(214, 196, 150), width=6)
    # ---- the ground: the ledge out to the wall over the shore, the bank, and the road on it
    d.polygon(S(V.ground_outline()), fill=(150, 140, 100))
    for Z in list(range(700, 2400, 100)) + list(range(2400, 4001, 200)):
        d.line(S([P(-3000, Z), P(3000, Z)]), fill=(110, 100, 80, 230 if Z % 500 == 0 else 110), width=1)
    for X in range(-2400, 2401, 200):
        d.line(S([P(X, 650), P(X, 4000)]), fill=(110, 100, 80, 110), width=1)
    d.polygon(S(V.road_outline()), fill=(200, 180, 134, 220))
    d.polygon(S(V.climb_outline()), fill=(206, 186, 140))
    d.polygon(S(V.wall_outline()), fill=(160, 160, 170), outline=(60, 60, 70))
    d.line(S([(0, HZ), (W, HZ)]), fill=(255, 80, 255), width=2)
    # ---- what stands, far to near
    things = []
    m = V.MOUND
    def mound(d, S):
        rim = [P(m["X"] + m["r"] * math.cos(a), m["Z"] + m["r"] * 0.9 * math.sin(a)) for a in np.linspace(math.pi, 2 * math.pi, 16)]
        top = [P(m["X"] + m["r"] * math.cos(a), m["Z"], m["h"] * math.sin(a) ** 0.6) for a in np.linspace(0, math.pi, 18)]
        d.polygon(S(top + rim[1:-1]), fill=(96, 140, 80), outline=(30, 50, 30))
        hx, hz = m["X"], m["Z"]
        tr = V.HACK["r"]
        d.polygon(S([P(hx - tr, hz, m["h"] - 30), P(hx + tr, hz, m["h"] - 30), P(hx + tr * 0.7, hz, m["h"] + 420), P(hx - tr * 0.7, hz, m["h"] + 420)]), fill=(90, 70, 60))
        crown = V.hack_crown()
        d.polygon(S(crown), fill=(110, 160, 90, 235), outline=(40, 70, 40))
    things.append((math.hypot(m["X"], m["Z"]), mound))
    kg = V.KAGO
    def kago(d, S):
        L, Wd, Hh = kg["length"], kg["width"], kg["height"]
        c = (kg["X"], kg["Z"])
        corners = [add(add(c, U, -L / 2), NL, -Wd / 2), add(add(c, U, L / 2), NL, -Wd / 2), add(add(c, U, L / 2), NL, Wd / 2), add(add(c, U, -L / 2), NL, Wd / 2)]
        box(d, S, corners, 30, [(150, 120, 70), (120, 96, 60), (150, 120, 70), (120, 96, 60), (170, 140, 90)])
        a, b = add(c, U, -kg["pole"] / 2), add(c, U, kg["pole"] / 2)
        d.line(S([P(*a, Hh + 10), P(*b, Hh - 16)]), fill=(80, 50, 30), width=6)
    things.append((math.hypot(kg["X"], kg["Z"]), kago))
    tk = V.TRUNKS
    def trunks(d, S):
        c = (tk["X"], tk["Z"])
        w2, d2 = tk["w"] / 2, tk["d"] / 2
        corners = [add(add(c, U, -w2), NL, -d2), add(add(c, U, w2), NL, -d2), add(add(c, U, w2), NL, d2), add(add(c, U, -w2), NL, d2)]
        box(d, S, corners, tk["tier"] * tk["n"] + 4, [(200, 180, 120), (150, 130, 90), (200, 180, 120), (150, 130, 90), (120, 100, 70)])
    things.append((math.hypot(tk["X"], tk["Z"]), trunks))
    for _, draw in sorted(things, key=lambda t: -t[0]):
        draw(d, S)
    # ---- the teahouse
    teahouse(d, S)
    # ---- the walk outline and the blocked patches
    walk = V.WALK
    d.line(S(list(walk) + [walk[0]]), fill=(0, 255, 255), width=3)
    for bl in V.BLOCKED:
        d.line(S(list(bl) + [bl[0]]), fill=(255, 120, 0), width=2)
    # ---- people at every mark, as the game sizes them (by the row of the feet)
    for name, (x, y, who) in V.marks_for_plan().items():
        person(d, S, x, y, who, name)
    # ---- the near plane (tinted red)
    for poly in V.near_outlines():
        d.polygon(S(poly), fill=(150, 40, 50, 200), outline=(20, 18, 26))
    im = im.resize((W, H), Image.LANCZOS)
    im.save(out)
    return out


def teahouse(d, S):
    T = V.TEA
    r = T.roof_pts()
    e, top = r["e"], r["top"]
    # the inside, seen through the open front: the floor, the back wall (open on the bay), the dark under the roof
    d.polygon(S([T.pt(0, 0, T.floor), T.pt(T.door[0], 0, T.floor), T.pt(T.door[0], T.D, T.floor), T.pt(0, T.D, T.floor)]), fill=(170, 170, 110))
    d.polygon(S([T.pt(0, T.D, T.floor), T.pt(T.door[0], T.D, T.floor), T.pt(T.door[0], T.D, 200), T.pt(0, T.D, 200)]), fill=(80, 130, 190))
    d.polygon(S([T.pt(0, T.D, 200), T.pt(T.door[0], T.D, 200), T.pt(T.door[0], 0, T.eave), T.pt(0, 0, T.eave)]), fill=(46, 40, 50))
    d.polygon(S([T.pt(T.door[0], 0, 0), T.pt(T.L, 0, 0), T.pt(T.L, 0, T.eave), T.pt(T.door[0], 0, T.eave)]), fill=(50, 42, 46))
    d.polygon(S([T.pt(T.door[0], 0, 0), T.pt(T.door[1], 0, 0), T.pt(T.door[1], 0, 186), T.pt(T.door[0], 0, 186)]), fill=(30, 26, 40))
    for u in T.posts:
        d.line(S([T.pt(u, 0, 0), T.pt(u, 0, T.eave)]), fill=(90, 70, 50), width=5)
    for u in (0.0, 200.0, 400.0, T.L):
        d.line(S([T.pt(u, -T.over + 6, 0), T.pt(u, -T.over + 6, T.eave)]), fill=(110, 84, 60), width=5)
    # the bench, the grill, the sign
    B = V.BENCH
    box(d, S, [T.xz(B["u0"], B["w0"]), T.xz(B["u1"], B["w0"]), T.xz(B["u1"], B["w1"]), T.xz(B["u0"], B["w1"])], B["h"],
        [(160, 120, 80), (130, 96, 64), (160, 120, 80), (130, 96, 64), (190, 150, 100)])
    Gd = V.GRILL
    box(d, S, [T.xz(Gd["u"] - Gd["len"] / 2, Gd["w"] - Gd["wid"] / 2), T.xz(Gd["u"] + Gd["len"] / 2, Gd["w"] - Gd["wid"] / 2),
               T.xz(Gd["u"] + Gd["len"] / 2, Gd["w"] + Gd["wid"] / 2), T.xz(Gd["u"] - Gd["len"] / 2, Gd["w"] + Gd["wid"] / 2)], Gd["h"],
        [(190, 140, 90), (150, 100, 70), (190, 140, 90), (150, 100, 70), (60, 40, 40)])
    Sg = V.SIGN
    a, b = T.pt(Sg["u"], Sg["w"]), T.pt(Sg["u"], Sg["w"], Sg["h"])
    d.line(S([a, b]), fill=(70, 50, 40), width=4)
    d.polygon(S([T.pt(Sg["u"] - Sg["wid"] / 2, Sg["w"], 40), T.pt(Sg["u"] + Sg["wid"] / 2, Sg["w"], 40), T.pt(Sg["u"] + Sg["wid"] / 2, Sg["w"], Sg["h"] - 6),
                 T.pt(Sg["u"] - Sg["wid"] / 2, Sg["w"], Sg["h"] - 6)]), fill=(230, 210, 160), outline=(40, 30, 30))
    # the near end wall (it faces us and the left: in the sun)
    d.polygon(S([T.pt(0, 0, 0), T.pt(0, T.D, 0), T.pt(0, T.D, T.eave), T.pt(0, 0, T.eave)]), fill=(214, 200, 170), outline=(30, 30, 40))
    # the roof: the front slope and the near hip; its thick cut edge
    A, B_, C, D_, R0, R1 = (r[k] for k in ("A", "B", "C", "D", "R0", "R1"))
    q = lambda uw, y: T.pt(uw[0], uw[1], y)
    d.polygon(S([q(A, e), q(B_, e), q(B_, e + T.thick), q(A, e + T.thick)]), fill=(120, 96, 60), outline=(30, 30, 40))
    d.polygon(S([q(A, e), q(D_, e), q(D_, e + T.thick), q(A, e + T.thick)]), fill=(150, 120, 76), outline=(30, 30, 40))
    d.polygon(S([q(A, e + T.thick), q(B_, e + T.thick), q(R1, top), q(R0, top)]), fill=(200, 170, 110), outline=(30, 30, 40))
    d.polygon(S([q(A, e + T.thick), q(D_, e + T.thick), q(R0, top)]), fill=(222, 192, 128), outline=(30, 30, 40))


def check_picture(picture="out/edo-kurasawa-2-all.png", out="out/edo-kurasawa-plancheck.png"):
    """The painting (as composed) with layout.json over it: the walk outline, the blocked patches, the areas, the base
    lines, and stand-ins at every mark and standing place at the game's size."""
    import json
    lay = json.load(open("out/edo-kurasawa/layout.json"))
    im = Image.open(picture).convert("RGB").resize((W * 2, H * 2), Image.LANCZOS)
    d = ImageDraw.Draw(im, "RGBA")
    S = lambda pts: [(x * 2, y * 2) for x, y in pts]
    for t in lay["things"]:
        sh = t["shape"]
        if "rect" in sh and sh["rect"]:
            x, y, w, h = sh["rect"]
            d.rectangle(S([(x, y), (x + w, y + h)]), outline=(255, 235, 60, 200))
        elif "poly" in sh:
            d.line(S(sh["poly"] + [sh["poly"][0]]), fill=(255, 235, 60, 200), width=1)
    d.line(S(lay["walk"] + [lay["walk"][0]]), fill=(0, 255, 255), width=2)
    for bl in lay["blocked"]:
        d.polygon(S(bl), outline=(255, 90, 0), fill=(255, 90, 0, 60))
    for pl in lay["planes"]:
        b = pl.get("base")
        if isinstance(b, list):
            d.line(S(b), fill=(255, 140, 0), width=3)
    who = {"kuni": "woman", "bearers": "man", "tora": "man", "peddler": "man", "komuso": "man", "arrive_lilsis": "lilsis", "arrive_bigsis": "bigsis"}
    for name, (x, y) in lay["marks"].items():
        person(d, S, x, y, who.get(name, "mom"), name)
    for i, (x, y) in enumerate(lay["fromTop"]):
        person(d, S, x, y, "bigsis" if i == 0 else "lilsis", "top" + str(i))
    for k_, (x, y) in lay["atGrill"].items():
        person(d, S, x, y, k_, "g." + k_)
    x, y = lay["kagoSeat"]
    d.ellipse(S([(x - 3, y - 3), (x + 3, y + 3)]), fill=(255, 0, 255))
    for f in lay["fx"]:
        if f["type"] == "passer":
            d.line(S(f["path"]), fill=(255, 0, 255, 200), width=2)
    im = im.resize((W, H), Image.LANCZOS)
    im.save(out)
    return out


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        print(check_picture(*sys.argv[2:]))
    else:
        print(f"eye {EYE:.0f} cm; Z0 {Z0:.0f}; the road runs to x {VP_ROAD:.0f}, the ends to x {VP_END:.0f}")
        print(skeleton(sys.argv[1] if len(sys.argv) > 1 else "out/edo-kurasawa-skeleton.png"))

"""Jolene's five hens, out in the yard behind the store, seen through the open back door: painted as small cropped
frames at the size they show at the yard's depth through the store's camera (a hen about 40 cm tall is about 20 px
there), crisp, hard-edged, every frame of every hen on one canvas with her feet at one point.

    hen-<n>-guard-a.png   standing with her back to us, facing the fence (and the place beyond it where the tracks stop)
    hen-<n>-guard-b.png   the same, her head turned a little: the small twitch the scene shows now and then
    hen-<n>-turn.png      turned round to look at us
    hen-<n>-sit.png       settled down on the dirt (stood down: Little Sister told her she could)
    hen-<n>-peck.png      pecking the ground
    egg-dust.png          one warm egg in the dust where Darlene sat
    hens.json             the foot point and the canvas (the same for every frame), where each hen stands, and the egg

    python3 nevada_store_hens.py       paints them into out/nevada-store/ and a sheet to look at (out/nevada-store-work/hens.png)

The hens: Darlene (red-brown, a big single comb, the eldest), Charlene (golden buff), Marlene (black with a green
sheen, a small pea comb), Arlene (white, her comb flopped over), Doreen (the small one, silver-grey and speckled, a
little fluffed: she feels the cold). Plain farmyard hens of our own drawing. They stand in the morning sun beyond the
shack's shadow: the sun is behind us, so their backs and tails are lit and their fronts (when they turn) are not."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image

from brush import F32, Sheet, grain, to_palette, save
from room import View
import nevada_store_model as M

V = View(**M.VIEW)
CANVAS = (32, 30)                                       # every frame: width, height
FOOT = (16, 27)                                         # the ground point in every frame
STATES = ["guard-a", "guard-b", "turn", "sit", "peck"]

HENS = [  # n, name, height (cm), body, shade, tail, light, comb kind, X, Z (where she stands in the yard: a row a little staggered, facing the fence)
    dict(n=1, name="Darlene", h=42, body="#a8552e", shade="#6e321e", tail="#3a2418", light="#d8844a", comb="single", X=712.0, Z=-300),
    dict(n=2, name="Charlene", h=40, body="#d89a48", shade="#9a6430", tail="#8a5426", light="#f0c070", comb="rose", X=670.0, Z=-322),
    dict(n=3, name="Marlene", h=39, body="#26242c", shade="#141218", tail="#1a2c2a", light="#4a5a52", comb="pea", X=694.0, Z=-350),
    dict(n=4, name="Arlene", h=41, body="#ece6d8", shade="#b4aaa4", tail="#d8d0c4", light="#fffaf0", comb="flop", X=738.0, Z=-340),
    dict(n=5, name="Doreen", h=31, body="#a8a8b0", shade="#6e6e7c", tail="#4a4a58", light="#d0d0d8", comb="small", X=752.0, Z=-318, specks="#3e3e4a"),
]
EGG_OFFSET = (-6.0, 7.0)                                # cm from Darlene's place, toward us and a little left: where the egg lies


def scale_at(X, Z):
    """Pixels per centimetre for something standing on the yard (Y = the step down) at X, Z."""
    return V.scale_at(X, Z)


def at_of(X, Z):
    x, y = V.pt(X, M.STEP, Z)
    return [int(round(x)), int(round(y))]


def ell(sh, cx, cy, rx, ry, color, ang=0.0, n=24):
    ca, sa = math.cos(ang), math.sin(ang)
    pts = [(cx + rx * math.cos(t) * ca - ry * math.sin(t) * sa, cy + rx * math.cos(t) * sa + ry * math.sin(t) * ca)
           for t in np.linspace(0, 2 * math.pi, n, endpoint=False)]
    sh.poly(pts, color)


def comb(sh, cx, cy, k, kind, face=0.0, red="#d42a20"):
    """The comb on her crown, seen from behind (face 0), turned (face +-1), or from in front (face 2)."""
    if kind == "single":
        for i, (dx, dy, r) in enumerate(((-1.6, -0.9, 1.15), (0.0, -1.5, 1.3), (1.6, -0.9, 1.1))):
            ell(sh, cx + dx * k * (0.7 if face == 0 else 1.0) + face * 0.6 * k, cy + dy * k, r * k, r * k, red)
    elif kind == "rose":
        ell(sh, cx + face * 0.5 * k, cy - 0.8 * k, 1.7 * k, 0.9 * k, red)
    elif kind == "pea":
        ell(sh, cx + face * 0.4 * k, cy - 0.7 * k, 1.0 * k, 0.75 * k, red)
    elif kind == "flop":
        ell(sh, cx + 1.4 * k + face * 0.4 * k, cy - 0.6 * k, 1.8 * k, 0.9 * k, red, ang=0.5)
    else:
        ell(sh, cx + face * 0.3 * k, cy - 0.6 * k, 0.8 * k, 0.6 * k, red)


def hen(sh, hn, state, k):
    """One hen on a Sheet, her feet at FOOT. Drawn in centimetres (k: pixels per cm at her place), seen from behind
    and a little above (the camera is high and far): her head and comb clear above a short tail fan, her back lit."""
    fx, fy = FOOT
    s = hn["h"] / 40.0
    body, shade, tail, light = hn["body"], hn["shade"], hn["tail"], hn["light"]
    legc = "#e2b23a"

    def P(x, y):                                          # cm from her foot point (x right, y up) -> sheet pixels
        return (fx + x * s * k, fy - y * s * k)

    def E(x, y, rx, ry, color, ang=0.0):
        cx, cy = P(x, y)
        ell(sh, cx, cy, rx * s * k, ry * s * k, color, ang)

    def legs():
        for dx in (-2.6, 2.6):
            sh.line([P(dx, 9), P(dx, 0.6)], legc, max(1.0, 1.5 * s * k))
            sh.line([P(dx - 2.4, 0.4), P(dx + 2.4, 0.4)], legc, 1.0)
    # the contact shadow on the dirt
    cx, cy = P(0, 0)
    ell(sh, cx, cy - 0.3, 9.5 * s * k, 1.2, "#7a5a44")
    if state in ("guard-a", "guard-b"):
        turn = 0.0 if state == "guard-a" else 1.0
        legs()
        sh.line([P(0, 21), P(0.4 + turn * 1.6, 33)], body, 6.6 * s * k)                        # her neck, beyond the back
        hx, hy = 0.4 + turn * 2.0, 34.0
        comb(sh, *P(hx, hy + 2.4), s * k, hn["comb"], face=turn)
        E(hx, hy, 3.5, 3.6, shade)
        E(hx - 0.4, hy + 0.6, 2.7, 2.6, body)
        if turn:                                                                            # her beak shows past her cheek
            sh.poly([P(hx + 3.0, hy + 0.6), P(hx + 6.4, hy - 0.4), P(hx + 3.0, hy - 1.6)], "#e8a830")
        E(0, 16, 11.0, 8.4, shade)                                                          # the body
        E(0, 17.4, 10.2, 7.0, body)
        E(0.4, 20.6, 7.6, 3.4, light)                                                       # the sun on her back
        if hn.get("specks"):
            rng = np.random.default_rng(hn["n"] * 7 + len(state))
            for _ in range(10):
                a, r = rng.random() * 6.28, rng.random() ** 0.5
                q = P(math.cos(a) * r * 8.5, 16 + math.sin(a) * r * 6)
                sh.ellipse(q[0], q[1], 0.55 * k, 0.55 * k, hn["specks"])
        fan = [P(-3.2, 16.5), P(-7.2, 23.5), P(-5.6, 27.2), P(-2.2, 25.4), P(0.2, 27.8), P(2.4, 25.4), P(5.8, 27.0), P(7.2, 23.2), P(3.4, 16.5)]
        sh.poly(fan, tail)                                                                  # the tail fan, nearest us, spread
        sh.line([P(-4.6, 25.4), P(-1.2, 18.4)], light, max(0.9, 0.8 * s * k))
        E(0, 9.4, 7.0, 2.6, shade)                                                         # the fluff under her
    elif state == "peck":                                                                   # head down in front, out of sight; rump and tail up
        legs()
        E(0, 18, 10.4, 8.0, shade)
        E(0, 19.4, 9.6, 6.6, body)
        E(0.4, 22.6, 7.2, 3.0, light)
        sh.poly([P(-3.2, 19.5), P(-7.2, 27.5), P(-5.6, 31.2), P(-2.2, 29.4), P(0.2, 32.0), P(2.4, 29.4), P(5.8, 31.0), P(7.2, 27.2), P(3.4, 19.5)], tail)
        sh.line([P(-4.6, 29.4), P(-1.2, 22.4)], light, max(0.9, 0.8 * s * k))
        E(0, 11.4, 6.6, 2.4, shade)
    elif state == "sit":                                                                    # settled on the dirt, fluffed round her feet
        sh.line([P(0, 12), P(0.4, 24)], body, 6.6 * s * k)
        comb(sh, *P(0.4, 27.4), s * k, hn["comb"], face=0.0)
        E(0.4, 25.0, 3.5, 3.6, shade)
        E(0.0, 25.6, 2.7, 2.6, body)
        E(0, 7.4, 12.6, 7.2, shade)
        E(0, 8.6, 11.8, 6.0, body)
        E(0.4, 11.4, 8.4, 2.8, light)
        sh.poly([P(-3.2, 8.5), P(-7.0, 14.6), P(-5.4, 18.0), P(-2.0, 16.4), P(0.2, 18.6), P(2.4, 16.4), P(5.6, 17.8), P(7.0, 14.4), P(3.4, 8.5)], tail)
        if hn.get("specks"):
            rng = np.random.default_rng(hn["n"] * 5)
            for _ in range(8):
                a, r = rng.random() * 6.28, rng.random() ** 0.5
                q = P(math.cos(a) * r * 9.5, 8 + math.sin(a) * r * 4.5)
                sh.ellipse(q[0], q[1], 0.55 * k, 0.55 * k, hn["specks"])
    elif state == "turn":                                                                   # turned round, looking at us
        legs()
        sh.poly([P(-4.0, 19), P(-4.8, 27), P(-1.6, 31.5), P(1.6, 31.5), P(4.8, 27), P(4.0, 19)], tail)     # the tail, behind her now
        E(0, 16, 9.8, 8.8, shade)                                                          # her breast, on the shaded side (the sun is behind her)
        E(0, 20.6, 7.8, 3.2, body)                                                         # the light along her shoulders
        for d in (-1, 1):
            E(d * 8.6, 16.6, 2.6, 5.6, body)                                               # her wings, rimmed with sun
        if hn.get("specks"):
            rng = np.random.default_rng(hn["n"] * 11)
            for _ in range(7):
                a, r = rng.random() * 6.28, rng.random() ** 0.5
                q = P(math.cos(a) * r * 6.5, 15 + math.sin(a) * r * 5.5)
                sh.ellipse(q[0], q[1], 0.55 * k, 0.55 * k, hn["specks"])
        sh.line([P(0, 20), P(0, 30)], shade, 6.0 * s * k)
        hx, hy = 0.0, 32.0
        comb(sh, *P(hx, hy + 2.8), s * k, hn["comb"], face=0.0)
        E(hx, hy, 3.7, 3.8, shade)
        E(hx, hy + 1.0, 3.0, 2.4, body)
        sh.poly([P(hx - 1.4, hy - 0.4), P(hx + 1.4, hy - 0.4), P(hx, hy - 3.6)], "#e8a830")              # the beak, at us
        E(hx, hy - 4.4, 1.2, 1.6, "#c82a22")                                               # the wattles
        for d in (-1, 1):
            q = P(hx + d * 1.8, hy + 0.6)
            sh.ellipse(q[0], q[1], 0.6 * k, 0.6 * k, "#1a1210")                            # both eyes


def frame(hn, state, k):
    """-> (RGB picture, hard alpha), CANVAS-sized."""
    W_, H_ = CANVAS
    sh = Sheet((H_, W_), ss=8)
    hen(sh, hn, state, k)
    c, a = sh.done()
    hard = (a >= 0.5).astype(F32)
    return c, hard


def egg_frame(k):
    """One brown egg lying in the dust, its warm side toward us, a speck of light on it (a little bigger than life, so
    that it reads at all: life size it would be three pixels)."""
    W_, H_ = 9, 6
    sh = Sheet((H_, W_), ss=8)
    ell(sh, 4.5, 3.6, 3.2, 2.2, "#a87050")
    ell(sh, 4.3, 3.1, 2.5, 1.6, "#d8a070")
    sh.ellipse(3.6, 2.6, 0.7, 0.55, "#fff2dc")
    c, a = sh.done()
    return c, (a >= 0.5).astype(F32), (4, 5)


def paint(out="out/nevada-store", sheet="out/nevada-store-work/hens.png"):
    os.makedirs(out, exist_ok=True)
    pics = {}
    allc = []
    for hn in HENS:
        k = scale_at(hn["X"], hn["Z"])
        for state in STATES:
            c, a = frame(hn, state, k)
            pics[(hn["n"], state)] = (c, a)
            allc.append(c[a > 0.5])
    ec, ea, efoot = egg_frame(scale_at(HENS[0]["X"], HENS[0]["Z"]))
    allc.append(ec[ea > 0.5])
    pal = None
    from nevada_store import palette_for
    pal = palette_for(np.concatenate(allc)[None, :, :], 40)
    for (n, state), (c, a) in pics.items():
        g = grain(c, n * 13 + len(state), 0.012)
        save(f"{out}/hen-{n}-{state}.png", to_palette(g, pal, speckle=0.004), pal, a)
    save(f"{out}/egg-dust.png", to_palette(grain(ec, 3, 0.01), pal, speckle=0.003), pal, ea)
    d = HENS[0]
    ex, ez = d["X"] + EGG_OFFSET[0], d["Z"] + EGG_OFFSET[1]
    data = {
        "foot": list(FOOT), "size": list(CANVAS),
        "states": {s: f"hen-<n>-{s}.png" for s in STATES},
        "hens": [{"n": h["n"], "name": h["name"], "at": at_of(h["X"], h["Z"]), "tall_px": round(h["h"] * scale_at(h["X"], h["Z"]), 1)} for h in HENS],
        "egg": {"file": "egg-dust.png", "at": at_of(ex, ez), "foot": list(efoot), "size": [9, 6]},
        "note": ("Each hen is a cut-out laid with her foot point (`foot`) at her place (`at`), behind the door's frame (doorframe.png) "
                 "and behind anyone on the step: sort her by her `at` row like a person. Painted at the size they show there (a hen "
                 "about 40 cm tall is about 20 px; Doreen is the small one); never scaled. The egg is a little bigger than life, so "
                 "that it reads."),
    }
    json.dump(data, open(f"{out}/hens.json", "w"), indent=1)
    if sheet:
        make_sheet(out, sheet)
    return data


def make_sheet(out, path, zoom=6):
    """Every frame enlarged, on the yard's dirt colour, a row for each hen."""
    W_, H_ = CANVAS
    im = Image.new("RGBA", ((W_ + 2) * len(STATES) + 12, (H_ + 2) * len(HENS)), (200, 160, 112, 255))
    for r, hn in enumerate(HENS):
        for c_, st in enumerate(STATES):
            f = Image.open(f"{out}/hen-{hn['n']}-{st}.png").convert("RGBA")
            im.alpha_composite(f, (c_ * (W_ + 2), r * (H_ + 2)))
    egg = Image.open(f"{out}/egg-dust.png").convert("RGBA")
    im.alpha_composite(egg, ((W_ + 2) * len(STATES) + 1, 4))
    im = im.resize((im.width * zoom, im.height * zoom), Image.NEAREST)
    im.convert("RGB").save(path)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(json.dumps(paint(), indent=1)[:600])

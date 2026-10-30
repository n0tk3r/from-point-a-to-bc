"""Inside Kihei's fish shop at Yui (scene `edo-fishshop`), the morning of about 8 April 1830: the earth floor open to
the street, the bay and Fuji in the opening, the raised tatami room at the right. PAINT-20B (round twenty).

    python3 edo_fishshop.py            everything: the backdrop, the cut-outs and their states, layout.json, the look
    python3 edo_fishshop.py fast       no brush pass (for composing)
    python3 edo_fishshop.py layout     layout.json alone, from the model (no painting)

ONE CAMERA (edo_fishshop_model.py: room.View, horizon 200, full 401, the lens 2.20 m up at the back of the earth floor,
turned 6 degrees to the right). Every surface is laid through it (floor_xz, plane_uv), every thing is a box or a
polygon in centimetres, so people the game draws stand in it at the right size.

THE LOOK (S/briefs/out/edo-design.md, section 4; PAINT-20A's style.md when it is there): the game's own painting,
composed and coloured as the woodblock landscape prints are: big flat masses, a graded sky, a fine even contour in
Prussian blue (the key block's line) laid AFTER the brush pass, few colours, the new deep blue leading. Nothing is
copied: the print of Fuji on the post is our own small design.

THREE TONES. Light: the opening (sky, water, Fuji, sand). Middle: the earth floor, the plaster, the tatami, the wood.
Dark: the roof space, the gap under the floor, the foreground.

Painted in the README's four passes: under (flat fills) - strokes - details (the ink sheet, crisp) - finish (grain,
one palette of 255 for every file, speckle, PNG-8 with a clear colour)."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image

from brush import F32, rgb, lerp, noise, grid, blur, strokes, grain, palette_of, to_palette, save, Sheet, over
from room import View
import edo_fishshop_model as M

W, H = 800, 600
V = View(**M.VIEW)
OUT = "out/edo-fishshop"
SEED = 1830
FAST = "fast" in sys.argv

INK = "#1d3a5c"            # the contour: Prussian blue
INK_W = 1.1
C = {
    "sky_top": "#2a5a8c", "sky_low": "#dfe8ee", "sea": "#2d5b88", "sea_far": "#6f93b6", "wave": "#eaf0f4", "shore": "#aebccb",
    "fuji": "#eef2f5", "fuji_shade": "#b9c9d9", "fuji_foot": "#7f9ab6", "sand": "#e4d4ab", "street": "#c6b088",
    "earth": "#8c7c64", "earth_dk": "#6f6250", "plaster": "#d2c6aa", "plaster_dk": "#b8ab8e", "wain": "#6b5137",
    "wood": "#8a6238", "wood_lt": "#b58a56", "wood_dk": "#5a3d24", "post": "#4e361f", "roof": "#3a2c22", "roof_dk": "#2a2019",
    "tatami": "#b7b67c", "tatami_dk": "#9c9a62", "heri": "#2e3440", "void": "#241f1b", "kamachi": "#452e1a",
    "indigo": "#243a6b", "indigo_lt": "#3a5490", "white": "#f2efe6", "paper": "#ece4cf", "straw": "#c9ad6a", "straw_dk": "#9a7f44",
    "iron": "#3b3b40", "fish": "#9fb1bd", "fish_dk": "#5e7384", "clay": "#9c7b5e", "clay_dk": "#73553c", "coal": "#2b2420",
    "copper": "#8a5a36", "rice": "#f4efe2", "mackerel": "#7c93a6", "bamboo": "#8fa06a", "red": "#b83a2a",
}
CUTS = ["noren", "driedfish", "tub-1", "tub-2", "tub-3", "stand", "sushibox-empty", "sushibox-filled", "sushibox-cut",
        "hearth", "basket", "front"]


# ---------------------------------------------------------------- the sheets
class Lay:
    """One layer of the picture: its flat fills (brushed later) and its ink (laid crisp after the brush)."""
    def __init__(self):
        self.fill, self.ink = Sheet((H, W), ss=3), Sheet((H, W), ss=3)

    def face(self, pts, color, ink=True, alpha=1.0, w=INK_W):
        if len(pts) < 3:
            return
        self.fill.poly(pts, color, alpha)
        if ink:
            self.ink.line(list(pts) + [pts[0]], INK, w, 0.85)

    def line(self, pts, color=INK, w=INK_W, alpha=0.85):
        self.ink.line(pts, color, w, alpha)


LAYERS = {}


def lay(name):
    if name not in LAYERS:
        LAYERS[name] = Lay()
    return LAYERS[name]


def rp(X, Y, Z):
    return V.pt(X, Y, Z)


def box(layer, b, tones, ink=True):
    """A box in the room on a layer: tones = (top, lit side, shaded side)."""
    X0, X1, Y0, Y1, Z0, Z1 = b
    for name, pp, n in V.box(X0, X1, Y0, Y1, Z0, Z1):
        col = tones[0] if name == "top" else (tones[1] if name in ("front", "left") else tones[2])
        if name == "bottom":
            col = tones[2]
        layer.face(pp, col, ink)


def ring(X, Y, Z, r, n=28):
    return [(X + math.cos(2 * math.pi * i / n) * r, Y, Z + math.sin(2 * math.pi * i / n) * r) for i in range(n)]


def cylinder(layer, X, Z, r, Y0, Y1, side, top, ink=True, hoops=()):
    """A tub or a pot: its side as the near half of the ring, its top as an ellipse."""
    pts = [V.pt(X + math.cos(a) * r, Y0, Z + math.sin(a) * r) for a in np.linspace(0, math.pi, 18)]   # the near side (Z + r is toward us)
    pts2 = [V.pt(X + math.cos(a) * r, Y1, Z + math.sin(a) * r) for a in np.linspace(math.pi, 0, 18)]
    layer.face(pts + pts2, side, ink)
    layer.face(V.poly(ring(X, Y1, Z, r)), top, ink)
    for hy in hoops:
        layer.line([V.pt(X + math.cos(a) * r, hy, Z + math.sin(a) * r) for a in np.linspace(0.05, math.pi - 0.05, 14)], C["iron"], 1.6, 0.9)


# ---------------------------------------------------------------- the under-painting of the far view and the shell (numpy)
def far_and_shell():
    """The sky, the bay, Fuji, the beach, the street, then the room's surfaces: all flat, in perspective."""
    pic = np.zeros((H, W, 3), dtype=F32)
    y, x = np.mgrid[0:H, 0:W].astype(F32)
    hz = V.hz
    # the sky: graded, Prussian blue above melting to pale at the horizon (the prints' bokashi), a little grain
    t = np.clip((hz - y) / hz, 0, 1) ** 0.8
    pic[...] = lerp(rgb(C["sky_low"]), rgb(C["sky_top"]), t[..., None])
    # the water, Y 0, Z < BEACH[1], up to the horizon: deeper near us, paler far off
    X, Z, ok = V.floor_xz((H, W), 0.0)
    water = (ok > 0) & (Z < M.BEACH[1])
    far = np.clip((y - hz) / 60.0, 0, 1)
    pic[water] = lerp(rgb(C["sea_far"]), rgb(C["sea"]), far[..., None])[water]
    # the far shore under Fuji: a low pale band at the horizon
    shore = (y >= hz - 3) & (y < hz + 3) & (x > 430) & (x < 760)
    pic[shore] = rgb(C["shore"])
    # the beach and the street
    beach = (ok > 0) & (Z >= M.BEACH[1]) & (Z < M.BEACH[0])
    street = (ok > 0) & (Z >= M.STREET[1]) & (Z < 0)
    pic[beach] = rgb(C["sand"])
    pic[street] = rgb(C["street"])
    # the earth floor, inside: X 0..STEP_X, Z 0..D
    earth = (ok > 0) & (Z >= 0) & (X >= 0) & ((X <= M.STEP_X) | (Z < M.BACKWALL_Z)) & (X <= M.W)
    pic[earth] = rgb(C["earth"])
    # the tatami floor at Y 45, X STEP_X..W, Z BACKWALL_Z..D, with the mats' borders (90 x 180, the borders dark)
    X2, Z2, ok2 = V.floor_xz((H, W), M.STEP_Y)
    tat = (ok2 > 0) & (X2 >= M.STEP_X) & (X2 <= M.W) & (Z2 >= M.BACKWALL_Z)
    pic[tat] = rgb(C["tatami"])
    heri = tat & ((np.mod(X2 - M.STEP_X, 90) < 2.5) | (np.mod(Z2 - M.BACKWALL_Z, 180) < 2.5))
    pic[heri] = rgb(C["heri"])
    # the kamachi (edge board) and the void under the raised floor, the plane X STEP_X
    u, v, okp = V.plane_uv((H, W), "X", M.STEP_X)
    kam = (okp > 0) & (u >= M.BACKWALL_Z) & (v >= M.STEP_Y - 9) & (v <= M.STEP_Y)
    void = (okp > 0) & (u >= M.BACKWALL_Z) & (v >= 0) & (v < M.STEP_Y - 9)
    pic[void] = rgb(C["void"])
    pic[kam] = rgb(C["kamachi"])
    # the left wall (X 0): dark planks below 90, plaster above, the roof space above 300
    u, v, okp = V.plane_uv((H, W), "X", 0.0)
    wall = (okp > 0) & (u >= 0) & (u <= M.D)
    pic[wall & (v >= 90) & (v < M.EAVE)] = rgb(C["plaster"])
    pic[wall & (v >= 0) & (v < 90)] = rgb(C["wain"])
    pic[wall & (v >= M.EAVE)] = rgb(C["roof"])
    # the right wall (X W): plaster above the tatami, from the back wall toward us
    u, v, okp = V.plane_uv((H, W), "X", float(M.W))
    wall = (okp > 0) & (u >= M.BACKWALL_Z) & (u <= M.D)
    pic[wall & (v >= M.STEP_Y) & (v < M.EAVE)] = rgb(C["plaster_dk"])
    pic[wall & (v >= M.EAVE)] = rgb(C["roof"])
    # the raised floor's front end (Z BACKWALL_Z, X STEP_X..W): the kamachi's end and the void under it
    u, v, okp = V.plane_uv((H, W), "Z", float(M.BACKWALL_Z))
    endf = (okp > 0) & (u >= M.STEP_X) & (u <= M.W)
    pic[endf & (v >= 0) & (v < M.STEP_Y - 9)] = rgb(C["void"])
    pic[endf & (v >= M.STEP_Y - 9) & (v <= M.STEP_Y)] = rgb(C["kamachi"])
    # the front wall over the lintel (Z 0): the gable boards, dark; and the roof space over everything above the walls
    u, v, okp = V.plane_uv((H, W), "Z", 0.0)
    gable = (okp > 0) & (u >= 0) & (u <= M.W) & (v >= M.LINTEL)
    pic[gable] = rgb(C["roof_dk"])
    # whatever is left above the walls' heads (the roof's underside, between the rafters) is the dark roof
    roofmask = (y < hz) & ~(water | shore | beach | street | gable)
    inside_open = (okp > 0) & (u >= 0) & (u <= M.W) & (v < M.LINTEL) & (v > 0)
    roofmask &= ~inside_open
    wallL = V.plane_uv((H, W), "X", 0.0)
    wallR = V.plane_uv((H, W), "X", float(M.W))
    left_seen = (wallL[2] > 0) & (wallL[0] >= 0) & (wallL[0] <= M.D) & (wallL[1] < M.EAVE)
    right_seen = (wallR[2] > 0) & (wallR[0] >= M.BACKWALL_Z) & (wallR[0] <= M.D) & (wallR[1] < M.EAVE) & (wallR[1] >= M.STEP_Y)
    roofmask &= ~(left_seen | right_seen)
    pic[roofmask] = rgb(C["roof"])
    # a little air: the far view is paler and cooler toward the horizon (the prints' fading), the floor darker near us
    near = np.clip((y - V.full) / 200.0, 0, 1)
    pic = lerp(pic, rgb(C["earth_dk"]), (near * 0.35 * earth)[..., None])
    pic = pic * (1 - 0.06 * noise((H, W), 60, SEED, octaves=3)[..., None])
    return np.clip(pic, 0, 1).astype(F32)


def far_things(L):
    """Fuji, the waves, a boat on the beach, the posts and beams: on the backdrop's layer, in the ink/fill sheets."""
    hz = V.hz
    # Fuji in the right bay: a cone, white, its lower slopes blue-grey, three ridge lines; small, across the water
    px, pw, ph = 575.0, 170.0, 37.0
    cone = [(px - pw / 2, hz), (px - 8, hz - ph + 1), (px + 7, hz - ph), (px + pw / 2 + 6, hz)]
    L.face(cone, C["fuji_foot"], ink=False)
    snow = [(px - pw * 0.30, hz - ph * 0.42), (px - 8, hz - ph + 1), (px + 7, hz - ph), (px + pw * 0.31, hz - ph * 0.40), (px + 10, hz - ph * 0.52), (px - 4, hz - ph * 0.46)]
    L.face(snow, C["fuji"], ink=False)
    L.line(cone[:3], INK, 0.9, 0.7)
    L.line(cone[1:], INK, 0.9, 0.7)
    for k in (-0.5, -0.15, 0.3):
        L.ink.line([(px + k * 10, hz - ph + 4), (px + k * pw * 0.55, hz - 2)], C["fuji_shade"], 1.2, 0.8)
    # the waves: rows of pale curls on the water, wider apart toward us (pattern, as the prints draw water)
    yy = hz + 4.0
    k = 0
    while yy < 236:
        n = int(14 - k * 0.6)
        for i in range(max(n, 5)):
            x0 = 170 + (i + (k % 2) * 0.5) * (470 / max(n, 5)) + 6 * math.sin(k * 1.7 + i)
            wlen = 7 + k * 1.3
            L.ink.line([(x0, yy), (x0 + wlen * 0.4, yy - 1.2 - k * 0.12), (x0 + wlen, yy)], C["wave"], 1.0 + k * 0.08, 0.9)
        yy += 2.4 + k * 0.9
        k += 1
    # a boat drawn up on the sand (a flat hull, its bow up), in the left bay
    hull = [V.pt(60, 0, -420), V.pt(170, 0, -400), V.pt(185, 36, -398), V.pt(150, 44, -405), V.pt(60, 30, -430)]
    L.face(hull, C["wood_lt"])
    L.face([V.pt(150, 44, -405), V.pt(185, 36, -398), V.pt(176, 50, -396), V.pt(150, 52, -404)], C["wood_dk"])
    # the posts of the open front, the lintel beam, the tie beams
    for p in M.POSTS:
        t = M.POST_T / 2
        box(L, (p - t, p + t, 0, M.LINTEL + 20, -t, t), (C["post"], C["wood_dk"], C["post"]))
    box(L, (-8, M.W + 8, M.LINTEL, M.LINTEL + 22, -10, 10), (C["wood_dk"], C["wood"], C["wood_dk"]))
    for zb in (400, 700):
        box(L, (0, M.W, M.EAVE - 6, M.EAVE + 20, zb - 12, zb + 12), (C["post"], C["wood_dk"], C["post"]))
    # rafters: lines from the eaves up into the dark, every 60 cm along Z, over each wall's head
    for z in range(40, 1000, 60):
        a, b = V.pt(0, M.EAVE, z), V.pt(-60, M.RIDGE, z)
        L.ink.line([a, b], C["roof_dk"], 2.2, 0.9)
        a, b = V.pt(M.W, M.EAVE, z), V.pt(M.W + 60, M.RIDGE, z)
        L.ink.line([a, b], C["roof_dk"], 2.2, 0.9)
    # the plank lines of the left wall's wainscot, the plaster's lower edge
    for z in range(0, 1000, 28):
        a, b = V.pt(0, 0, z), V.pt(0, 90, z)
        L.ink.line([a, b], C["wood_dk"], 0.9, 0.6)
    L.line([V.pt(0, 90, 0), V.pt(0, 90, 1000)], INK, 0.9, 0.6)
    L.line([V.pt(0, M.EAVE, 0), V.pt(0, M.EAVE, 1000)], INK, 0.9, 0.5)
    L.line([V.pt(M.W, M.EAVE, M.BACKWALL_Z), V.pt(M.W, M.EAVE, 1000)], INK, 0.9, 0.5)
    L.line([V.pt(M.STEP_X, M.STEP_Y, M.BACKWALL_Z), V.pt(M.STEP_X, M.STEP_Y, 1000)], INK, 1.0, 0.8)   # the kamachi's edge
    L.line([V.pt(M.STEP_X, M.STEP_Y, M.BACKWALL_Z), V.pt(M.W, M.STEP_Y, M.BACKWALL_Z)], INK, 1.0, 0.8)   # and its front end
    L.line([V.pt(M.STEP_X, 0, M.BACKWALL_Z), V.pt(M.W, 0, M.BACKWALL_Z)], INK, 0.9, 0.6)
    L.line([V.pt(M.STEP_X, M.STEP_Y - 9, M.BACKWALL_Z), V.pt(M.STEP_X, M.STEP_Y - 9, 1000)], INK, 0.9, 0.7)
    # the posts under the raised floor, in the void (every 90 cm)
    for z in range(M.BACKWALL_Z + 20, 1000, 90):
        box(L, (M.STEP_X - 2, M.STEP_X + 10, 0, M.STEP_Y - 9, z - 6, z + 6), (C["void"], C["kamachi"], C["void"]), ink=False)


# ---------------------------------------------------------------- the things on the backdrop (nobody passes behind them)
def backdrop_things(L):
    # the cutting board on two trestles, along the left wall (Kihei's place in front of it)
    X0, X1, Y0, Y1, Z0, Z1 = M.BOARD
    for z in M.TRESTLE_Z:
        box(L, (X0 + 6, X1 - 6, 0, Y0, z - 5, z + 5), (C["wood_dk"], C["wood"], C["wood_dk"]))
    box(L, M.BOARD, (C["wood_lt"], C["wood"], C["wood_dk"]))
    # a knife and two mackerel on it
    L.face([V.pt(30, Y1, 250), V.pt(58, Y1, 262), V.pt(60, Y1 + 1, 265), V.pt(32, Y1 + 1, 254)], C["iron"], ink=False)
    for (zx, zz) in ((44, 200), (52, 226)):
        L.face(V.poly([(zx - 16, Y1 + 1, zz - 4), (zx + 16, Y1 + 1, zz - 2), (zx + 16, Y1 + 1, zz + 3), (zx - 16, Y1 + 1, zz + 5)]), C["mackerel"])
    # the money box on the tatami at the back, strings of square-holed copper coins on and beside it
    box(L, M.MONEYBOX, (C["wood_lt"], C["wood"], C["wood_dk"]))
    bx0, bx1, by0, by1, bz0, bz1 = M.MONEYBOX
    for i in range(3):
        pts = [V.pt(bx0 - 2 - j * 4, by1 + 1 - (j % 2) * 0.5, bz0 + 6 + i * 12) for j in range(9)]
        L.ink.line(pts, C["copper"], 2.4, 0.95)
    L.ink.line([V.pt(bx0 - 6, M.STEP_Y + 1, bz1 + 6), V.pt(bx0 - 40, M.STEP_Y + 1, bz1 + 10)], C["copper"], 2.6, 0.95)
    # O-Tami's clothes chest against the right wall, with its drawer pulls
    box(L, M.CHEST, (C["wood"], C["wood_lt"], C["wood_dk"]))
    cx0, cx1, cy0, cy1, cz0, cz1 = M.CHEST
    for k in range(3):
        yk = cy0 + 14 + k * 26
        L.line([V.pt(cx0, yk, cz0), V.pt(cx0, yk, cz1)], INK, 0.9, 0.7)
        L.ink.ellipse(*V.pt(cx0 - 0.5, yk + 12, (cz0 + cz1) / 2), 2.2, 1.6, C["iron"], 0.95)
    # the god-shelf, high on the right wall: a small plain shelf, a tiny shrine shape on it (scenery, never used)
    gX, gY0, gY1, gZ0, gZ1 = M.GODSHELF
    box(L, (gX - 26, gX, gY0, gY0 + 4, gZ0, gZ1), (C["paper"], C["wood_lt"], C["wood_dk"]))
    box(L, (gX - 20, gX - 4, gY0 + 4, gY1 - 10, gZ0 + 16, gZ1 - 16), (C["paper"], C["paper"], C["plaster_dk"]))
    L.face([V.pt(gX - 24, gY1 - 10, gZ0 + 10), V.pt(gX - 24, gY1 - 10, gZ1 - 10), V.pt(gX - 12, gY1 + 2, (gZ0 + gZ1) / 2)], C["wood_dk"])
    # the print of Fuji in the new blue, on a board hung on the post at X 430 (facing left, into the shop): our own small
    # design: a band of deep blue sky, the cone in Prussian blue, its snow the paper, the sea a dark band at the foot
    pX, pY0, pY1, pZ = M.PRINT
    fX = pX - M.POST_T / 2 - 1.5
    def pf(dy0, dy1, dz0, dz1, off=0.0):
        return [V.pt(fX - off, pY0 + dy0, dz0), V.pt(fX - off, pY0 + dy0, dz1), V.pt(fX - off, pY0 + dy1, dz1), V.pt(fX - off, pY0 + dy1, dz0)]
    L.face(pf(-3, 59, -19, 27), C["wood_dk"])                                     # the board
    L.face(pf(0, 56, -16, 24, 0.5), C["paper"])                                   # the sheet
    L.face(pf(30, 52, -13, 21, 1.0), C["indigo_lt"], ink=False)                   # the sky band
    L.face(pf(6, 12, -13, 21, 1.0), C["indigo"], ink=False)                       # the sea at the foot
    L.face([V.pt(fX - 1.5, pY0 + 12, -13), V.pt(fX - 1.5, pY0 + 12, 21), V.pt(fX - 1.5, pY0 + 44, 4)], C["indigo"], ink=False)   # the cone
    L.face([V.pt(fX - 2, pY0 + 33, -3), V.pt(fX - 2, pY0 + 33, 11), V.pt(fX - 2, pY0 + 44, 4)], C["white"], ink=False)           # its snow
    L.face(pf(50, 52, -13, 21, 1.5), C["indigo"], ink=False)
    # sedge hats hung on the left wall by the front: two shallow cones, side on
    for (hx, hz_, hy0, hy1) in M.HATS:
        L.face([V.pt(1, hy0 + 6, hz_ - 30), V.pt(1, hy0 + 6, hz_ + 30), V.pt(1, hy1, hz_ + 2)], C["straw"])
        L.ink.line([V.pt(1, hy0 + 7, hz_ - 26), V.pt(1, hy0 + 7, hz_ + 26)], C["straw_dk"], 1.2, 0.9)
    # straw sandals hanging for sale from the lintel beside the left bay, on a cord
    sx0, sx1, sy0, sy1, sz = M.SANDALS
    L.ink.line([V.pt(sx0, sy1 + 4, sz + 4), V.pt(sx1, sy1 + 4, sz + 4)], C["straw_dk"], 1.4, 0.9)
    for i in range(4):
        x = sx0 + 10 + i * 26
        L.ink.line([V.pt(x, sy1 + 4, sz + 4), V.pt(x, sy0 + 36, sz + 4)], C["straw_dk"], 1.0, 0.9)
        for dx in (-5, 5):
            L.face([V.pt(x + dx - 4, sy0 + 36, sz + 4), V.pt(x + dx + 4, sy0 + 36, sz + 4), V.pt(x + dx + 4, sy0, sz + 4), V.pt(x + dx - 4, sy0, sz + 4)], C["straw"])


# ---------------------------------------------------------------- the cut-outs
def cut_things():
    for i, (tx, tz, r, h) in enumerate(M.TUBS, 1):
        L = lay(f"tub-{i}")
        cylinder(L, tx, tz, r, 0, h, C["wood"], C["sea"], hoops=(h * 0.3, h * 0.8))
        for j in range(3):          # fish in the water: a few pale backs
            a = 0.7 + j * 1.9 + i
            L.face(V.poly([(tx + math.cos(a) * r * 0.5 - 9, h - 1, tz + math.sin(a) * r * 0.5), (tx + math.cos(a) * r * 0.5 + 9, h - 1, tz + math.sin(a) * r * 0.5 + 3),
                           (tx + math.cos(a) * r * 0.5 + 7, h - 1, tz + math.sin(a) * r * 0.5 + 7)]), C["fish"], ink=False)
    # the stand the sushi box is pressed on, and the box's three states on it
    L = lay("stand")
    box(L, M.STAND, (C["wood_lt"], C["wood"], C["wood_dk"]))
    bx0, bx1, by0, by1, bz0, bz1 = M.SUSHIBOX
    Lb = lay("sushibox-empty")                      # the box, its lid leaning against it
    box(Lb, (bx0, bx1, by0, by1, bz0, bz1), (C["rice"], C["wood_lt"], C["wood"]))
    box(Lb, (bx0 + 2, bx1 - 2, by0 + 3, by0 + 4, bz0 + 2, bz1 - 2), (C["wood_lt"], C["wood"], C["wood"]), ink=False)
    Lb.face(V.poly([(bx1 + 2, by0, bz0), (bx1 + 14, by0, bz1), (bx1 + 4, by1 + 8, bz1), (bx1 - 2, by1 + 8, bz0)]), C["wood_lt"])
    Lf = lay("sushibox-filled")                     # filled and pressed: the lid down inside, a weight stone on it
    box(Lf, (bx0, bx1, by0, by1, bz0, bz1), (C["wood_lt"], C["wood_lt"], C["wood"]))
    box(Lf, (bx0 + 3, bx1 - 3, by1 - 3, by1 + 1, bz0 + 3, bz1 - 3), (C["wood"], C["wood"], C["wood_dk"]))
    Lf.face(V.poly(ring((bx0 + bx1) / 2, by1 + 9, (bz0 + bz1) / 2, 9)), C["iron"])
    Lf.face(V.poly(ring((bx0 + bx1) / 2, by1 + 1, (bz0 + bz1) / 2, 11)), C["iron"], ink=False)
    Lc = lay("sushibox-cut")                        # turned out and cut on a board: a slab of rice and mackerel in slices
    box(Lc, (bx0 - 4, bx1 + 8, by0, by0 + 2, bz0 - 2, bz1 + 2), (C["wood_lt"], C["wood"], C["wood_dk"]))
    box(Lc, (bx0, bx1 + 2, by0 + 2, by0 + 8, bz0 + 4, bz1 - 4), (C["mackerel"], C["rice"], C["rice"]))
    for k in range(1, 6):
        xk = bx0 + k * (bx1 + 2 - bx0) / 6
        Lc.line([V.pt(xk, by0 + 8.5, bz0 + 4), V.pt(xk, by0 + 8.5, bz1 - 4)], INK, 0.9, 0.8)
        Lc.line([V.pt(xk, by0 + 2, bz1 - 4), V.pt(xk, by0 + 8, bz1 - 4)], INK, 0.9, 0.8)
    # the cooking hearth against the left wall in the foreground, its pot on it (the fire's mouth dark; steam is the engine's)
    L = lay("hearth")
    hx0, hx1, hy0, hy1, hz0, hz1 = M.HEARTH
    box(L, M.HEARTH, (C["clay"], C["clay"], C["clay_dk"]))
    L.face(V.poly([(hx1 - 0.5, 8, hz0 + 20), (hx1 - 0.5, 8, hz1 - 20), (hx1 - 0.5, 30, hz1 - 24), (hx1 - 0.5, 30, hz0 + 24)]), C["coal"])
    pX, pZ, pr, ph = M.POT
    cylinder(L, pX, pZ, pr, hy1 - 4, hy1 + ph, C["iron"], C["iron"], hoops=())
    L.face(V.poly([(pX - pr + 2, hy1 + ph + 1, pZ - pr + 4), (pX + pr - 2, hy1 + ph + 1, pZ - pr + 4), (pX + pr - 2, hy1 + ph + 1, pZ + pr - 4), (pX - pr + 2, hy1 + ph + 1, pZ + pr - 4)]), C["wood_lt"])
    box(L, (pX - 4, pX + 4, hy1 + ph + 1, hy1 + ph + 7, pZ - 3, pZ + 3), (C["wood_dk"], C["wood"], C["wood_dk"]), ink=False)
    # the baby's basket on the tatami near us: a shallow oval basket, a quilt in it
    L = lay("basket")
    kx0, kx1, ky0, ky1, kz0, kz1 = M.BASKET
    cx, cz = (kx0 + kx1) / 2, (kz0 + kz1) / 2
    oval = [(cx + math.cos(2 * math.pi * i / 28) * (kx1 - kx0) / 2, ky0, cz + math.sin(2 * math.pi * i / 28) * (kz1 - kz0) / 2) for i in range(28)]
    side = [V.pt(X, ky0, Z) for X, _, Z in oval[:15]] + [V.pt(X, ky1, Z) for X, _, Z in oval[14::-1]]
    L.face(side, C["straw"])
    L.face(V.poly([(X, ky1, Z) for X, _, Z in oval]), C["straw_dk"])
    L.face(V.poly([(cx + math.cos(2 * math.pi * i / 20) * (kx1 - kx0) / 2.6, ky1 + 1, cz + math.sin(2 * math.pi * i / 20) * (kz1 - kz0) / 2.6) for i in range(20)]), C["indigo"])
    L.face(V.poly([(cx + math.cos(2 * math.pi * i / 16) * 9, ky1 + 2, cz - 12 + math.sin(2 * math.pi * i / 16) * 9) for i in range(16)]), C["paper"])
    for yy in (ky0 + 8, ky0 + 18, ky0 + 27):
        L.ink.line([V.pt(X, yy, Z) for X, _, Z in oval[:15]], C["straw_dk"], 0.9, 0.8)
    # the dried fish on a line along the left wall: split fish hung by the tail (a sway, anchored at the top)
    L = lay("driedfish")
    fx, fz0, fz1, fy = M.DRIEDFISH
    L.ink.line([V.pt(fx + 12, fy, fz0), V.pt(fx + 12, fy, fz1)], C["straw_dk"], 1.2, 0.9)
    for i in range(7):
        z = fz0 + 20 + i * 42
        L.face([V.pt(fx + 12, fy, z), V.pt(fx + 12, fy - 10, z - 7), V.pt(fx + 12, fy - 34, z - 9), V.pt(fx + 12, fy - 44, z), V.pt(fx + 12, fy - 34, z + 9), V.pt(fx + 12, fy - 10, z + 7)], C["fish"])
        L.line([V.pt(fx + 12, fy - 8, z), V.pt(fx + 12, fy - 38, z)], C["fish_dk"], 0.9, 0.8)
    # the noren across the middle bay: two indigo panels, a white mark of our own (a fish's curve) on each
    L = lay("noren")
    nx0, nx1, ny0, ny1 = M.NOREN
    mid = (nx0 + nx1) / 2
    for (a, b) in ((nx0 + 4, mid - 3), (mid + 3, nx1 - 4)):
        L.face([V.pt(a, ny1, 2), V.pt(b, ny1, 2), V.pt(b + 2, ny0, 6), V.pt(a - 2, ny0, 6)], C["indigo"])
        cxp, cyp = V.pt((a + b) / 2, (ny0 + ny1) / 2, 4)
        L.ink.line([(cxp - 9, cyp + 5), (cxp - 3, cyp - 6), (cxp + 5, cyp - 4), (cxp + 9, cyp + 6), (cxp + 3, cyp + 2)], C["white"], 1.8, 0.95)
    L.line([V.pt(nx0, ny1 + 2, 2), V.pt(nx1, ny1 + 2, 2)], C["wood_dk"], 1.6, 0.9)
    # the front plane: the near end of the kamachi with its corner post, and a stack of firewood at the bottom left
    L = lay("front")
    box(L, (M.STEP_X - 6, M.STEP_X + 8, 0, M.EAVE, 760, 774), (C["post"], C["kamachi"], C["post"]))
    for k in range(6):
        y0 = k * 11
        for j in range(5 - (k % 2)):
            x = 130 + j * 28 + (k % 2) * 14
            box(L, (x, x + 24, y0, y0 + 11, 700, 820), (C["wood_lt"], C["wood"], C["wood_dk"]))
    cylinder(L, 330, 790, 26, 0, 34, C["wood"], C["sea"], hoops=(10, 28))      # a water bucket, bottom middle


# ---------------------------------------------------------------- putting it together
def composite():
    under = far_and_shell()
    back = lay("back")
    far_things(back)
    backdrop_things(back)
    cut_things()
    fc, fa = back.fill.done()
    under = over(under, fc, fa)
    pic = under if FAST else strokes(under, sizes=(9, 5, 2), seed=SEED, density=1.5, jitter=0.03, keep=0.42)
    ic, ia = back.ink.done()
    pic = over(pic, ic, ia)
    pic = grain(np.clip(pic, 0, 1), SEED, 0.02)
    files = {"back": (pic, None)}
    for name in CUTS:
        L = LAYERS[name]
        c, a = L.fill.done()
        ic, ia = L.ink.done()
        alpha = np.maximum(a, ia)
        col = over(np.where(a[..., None] > 0.02, c, pic), ic, ia)
        col = grain(np.clip(col, 0, 1), SEED + 7, 0.02)
        files[name] = (col, alpha)
    return files


def finish(files):
    os.makedirs(OUT, exist_ok=True)
    layered = files["back"][0].copy()
    for name in CUTS:
        c, a = files[name]
        layered = over(layered, c, a)
    pal = palette_of([layered, files["back"][0]], colors=255, seed=3)
    for name, (c, a) in files.items():
        idx = to_palette(c, pal, seed=5, speckle=0.014)
        save(f"{OUT}/{name}.png", idx, pal, alpha=None if a is None else (a > 0.5).astype(F32))
    Image.fromarray((np.clip(layered, 0, 1) * 255 + 0.5).astype(np.uint8)).save(f"{OUT}-look.png")


# ---------------------------------------------------------------- layout.json
def px(p):
    return [round(float(p[0]), 1), round(float(p[1]), 1)]


def foot(X, Z, cm=175):
    x, y, h = V.person(X, Z, cm)
    return px((x, y)), round(float(h), 1)


def footprint(b):
    X0, X1, Y0, Y1, Z0, Z1 = b
    return [px(p) for p in V.poly([(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)])]


def shape_of(b, pad=0):
    """The picture box of a thing (its visible faces), as a polygon."""
    X0, X1, Y0, Y1, Z0, Z1 = b
    pts = [V.pt(X, Y, Z) for X in (X0, X1) for Y in (Y0, Y1) for Z in (Z0, Z1)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    x0, x1 = max(0.0, min(xs) - pad), min(800.0, max(xs) + pad)
    y0, y1 = max(0.0, min(ys) - pad), min(600.0, max(ys) + pad)
    return [[round(x0, 1), round(y0, 1)], [round(x1, 1), round(y0, 1)], [round(x1, 1), round(y1, 1)], [round(x0, 1), round(y1, 1)]]


def layout():
    marks, stands = {}, {}
    for k, (X, Z) in M.MARKS.items():
        at, h = foot(X, Z)
        marks[k] = {"at": at, "face": M.FACE[k], "grownup_px": h, "cm": [X, Z]}
    seat_note = ("the three of them seated on the kamachi (the raised room's edge, 45 cm up), facing W into the shop, feet on the earth floor: "
                 "a seated person's `at` is the ground under the hips (X 402, 18 cm in front of the edge at X 420); the rig sits them with the "
                 "hips `seat` of 175 cm above it: 0.257 is 45 cm (the rig's SEATS.chair, 0.262, is 46 cm: `sit: { seat: \"chair\" }` does as well; "
                 "NOT the rig's \"step\", which is a kerb of 18 cm). seat_row is the kamachi's top at the mark. Guests' knees come out over the "
                 "earth floor; nothing covers them")
    seats = {}
    for k in ("stepmom", "stepbig", "steplil"):
        X, Z = M.MARKS[k]
        seats[k] = {"at": marks[k]["at"], "face": "W", "seat": 0.257, "seat_cm": M.STEP_Y, "seat_row": round(V.pt(X, M.STEP_Y, Z)[1], 1),
                    "grownup_px": marks[k]["grownup_px"], "note": seat_note}
    walk = [px(V.pt(X, 0, Z)) for X, Z in M.WALK]
    blocked = {
        "tubs": [footprint((tx - r, tx + r, 0, h, tz - r, tz + r)) for tx, tz, r, h in M.TUBS],
        "board": footprint((M.BOARD[0], M.BOARD[1] + 10, 0, 1, M.BOARD[4], M.BOARD[5])),
        "stand": footprint(M.STAND), "hearth": footprint(M.HEARTH),
    }
    things = {
        "street": {"shape": [[183, 182], [618, 182], [618, 352], [183, 352]], "what": "the open front: the street, the beach, the bay and Fuji"},
        "fuji": {"shape": [[487, 162], [667, 162], [667, 202], [487, 202]], "what": "Fuji across the water, in the right bay"},
        "noren": {"shape": [px(V.pt(M.NOREN[0], M.NOREN[3], 0)), px(V.pt(M.NOREN[1], M.NOREN[3], 0)), px(V.pt(M.NOREN[1], M.NOREN[2], 0)), px(V.pt(M.NOREN[0], M.NOREN[2], 0))]},
        "tubs": {"shape": shape_of((M.TUBS[2][0] - 40, M.TUBS[1][0] + 30, 0, 46, 20, 190), 2)},
        "cuttingboard": {"shape": shape_of(M.BOARD, 3)}, "kihei": {"at": marks["kihei"]["at"]},
        "sushibox": {"shape": shape_of((M.STAND[0], M.STAND[1] + 16, 0, 62, M.STAND[4], M.STAND[5]), 2), "states": ["sushibox-empty", "sushibox-filled", "sushibox-cut"]},
        "hearth": {"shape": shape_of((M.HEARTH[0], M.HEARTH[1], 0, 96, M.HEARTH[4], M.HEARTH[5]), 2), "pot": px(V.pt(M.POT[0], M.HEARTH[3] + M.POT[3], M.POT[1]))},
        "driedfish": {"shape": shape_of((0, 14, M.DRIEDFISH[3] - 46, M.DRIEDFISH[3] + 2, M.DRIEDFISH[1], M.DRIEDFISH[2]), 2)},
        "print": {"shape": shape_of((M.PRINT[0] - 10, M.PRINT[0] - 7, M.PRINT[1] - 3, M.PRINT[2] + 3, -19, 27), 2)},
        "money": {"shape": shape_of((M.MONEYBOX[0] - 40, M.MONEYBOX[1] + 4, M.MONEYBOX[2], M.MONEYBOX[3] + 4, M.MONEYBOX[4] - 4, M.MONEYBOX[5] + 12), 2)},
        "godshelf": {"shape": shape_of((M.W - 28, M.W, M.GODSHELF[1], M.GODSHELF[2] + 4, M.GODSHELF[3], M.GODSHELF[4]), 2)},
        "step": {"shape": [px(V.pt(M.STEP_X, M.STEP_Y, M.BACKWALL_Z)), px(V.pt(M.W, M.STEP_Y, M.BACKWALL_Z)), px(V.pt(M.W, M.STEP_Y, 700)), px(V.pt(M.STEP_X, M.STEP_Y, 700)), px(V.pt(M.STEP_X, 0, 700)), px(V.pt(M.STEP_X, 0, M.BACKWALL_Z))], "what": "the raised room (the tatami) and its edge, the step guests sit on"},
        "sandals": {"shape": shape_of((M.SANDALS[0] - 6, M.SANDALS[1] + 6, M.SANDALS[2], M.SANDALS[3] + 6, 0, 8), 2)},
        "hats": {"shape": shape_of((0, 4, 178, 228, 20, 150), 3)},
        "chest": {"shape": shape_of(M.CHEST, 3)}, "baby": {"shape": shape_of(M.BASKET, 3)},
        "tami": {"at": marks["tami"]["at"]}, "cat": {"at": marks["cat"]["at"]},
        "under": {"shape": [px(V.pt(M.STEP_X, 0, M.UNDER[3])), px(V.pt(M.STEP_X, M.UNDER[2], M.UNDER[3])), px(V.pt(M.STEP_X, M.UNDER[2], M.UNDER[4])), px(V.pt(M.STEP_X, 0, M.UNDER[4]))]},
    }
    for t in things.values():                       # every shape inside the picture
        if "shape" in t:
            t["shape"] = [[round(min(800.0, max(0.0, x)), 1), round(min(600.0, max(0.0, y)), 1)] for x, y in t["shape"]]
    planes = [
        {"id": "noren", "picture": "noren.png", "base": "back", "note": "the noren in the middle bay: a sway (anchor top)"},
        {"id": "driedfish", "picture": "driedfish.png", "base": "back", "note": "fish drying on the line along the left wall: a sway"},
        {"id": "tub-1", "picture": "tub-1.png", "base": round(V.pt(M.TUBS[0][0], 0, M.TUBS[0][1] + M.TUBS[0][2])[1], 1), "solid": blocked["tubs"][0]},
        {"id": "tub-2", "picture": "tub-2.png", "base": round(V.pt(M.TUBS[1][0], 0, M.TUBS[1][1] + M.TUBS[1][2])[1], 1), "solid": blocked["tubs"][1]},
        {"id": "tub-3", "picture": "tub-3.png", "base": round(V.pt(M.TUBS[2][0], 0, M.TUBS[2][1] + M.TUBS[2][2])[1], 1), "solid": blocked["tubs"][2]},
        {"id": "stand", "picture": "stand.png", "base": round(V.pt(M.STAND[1], 0, M.STAND[5])[1], 1), "solid": blocked["stand"]},
        {"id": "sushibox", "picture": "sushibox-empty.png", "base": round(V.pt(M.STAND[1], 0, M.STAND[5])[1], 1),
         "states": {"empty": "sushibox-empty.png", "filled": "sushibox-filled.png", "cut": "sushibox-cut.png"}},
        {"id": "hearth", "picture": "hearth.png", "base": round(V.pt(M.HEARTH[1], 0, M.HEARTH[5])[1], 1), "solid": blocked["hearth"]},
        {"id": "basket", "picture": "basket.png", "base": round(V.pt(M.BASKET[0], 0, M.BASKET[5])[1], 1), "note": "on the tatami: its base is the earth floor's row under its near edge"},
        {"id": "front", "picture": "front.png", "base": "front"},
    ]
    fx = [
        {"id": "steam", "type": "smoke", "at": things["hearth"]["pot"], "base": planes[7]["base"], "height": 120, "width": [4, 26], "lean": [-12, -120],
         "rate": 2.5, "color": "#f0ece4", "opacity": 0.4, "what": "steam from the pot on the hearth"},
        {"id": "noren-sway", "type": "sway", "plane": "noren", "anchor": "top", "amount": 3, "period": 3.2, "what": "the noren lifting in the sea wind"},
        {"id": "fish-sway", "type": "sway", "plane": "driedfish", "anchor": "top", "amount": 1.5, "period": 4.1},
        {"id": "hearth-fire", "type": "flame", "at": px(V.pt(M.HEARTH[1] - 1, 18, (M.HEARTH[4] + M.HEARTH[5]) / 2)), "base": planes[7]["base"] + 1, "size": 7, "lull": 0.4,
         "glow": 20, "glowColor": "#ff9a40", "glowOpacity": 0.18, "what": "the fire in the hearth's mouth"},
        {"id": "tub-flip", "type": "ripples", "at": px(V.pt(M.TUBS[1][0], M.TUBS[1][3], M.TUBS[1][1])), "radius": [1, 8], "flat": 0.3, "every": [6, 14], "base": planes[3]["base"],
         "what": "a fish in the second tub flipping now and then: rings on its water (a painted flip is ENGINE-20's if wanted)"},
    ]
    cat_sizeAt = M.VIEW["full"]
    out = {
        "scene": M.ID, "size": [W, H], "horizon": M.VIEW["horizon"], "full": M.VIEW["full"], "view": M.VIEW, "key": "edo-morning",
        "camera_note": "the lens 2.20 m up (below the lintel at 2.80 m, so that the sea's horizon and Fuji show through the open front): people "
                       "at the street line are 119 px, at full (Z 373) 160; the walk's front edge keeps them under 195",
        "walk": walk, "blocked": blocked, "marks": marks, "seats": seats, "things": things, "planes": planes, "fx": fx,
        "cat": {"sidecar": "cat.json", "sizeAt": cat_sizeAt, "at": marks["cat"]["at"], "under": things["under"]["shape"],
                "note": "the cat's frames (edo_fishshop_cat.py) are painted at the size of the row `full`; the engine scales them by depth as it does Ranger's"},
        "edges": {"street": {"shape": things["street"]["shape"], "to": "edo-village", "mark": "shop", "note": "out through the open front (mark `door` inside it)"}},
        "notes": ["People walk only on the earth floor (walk) and sit on the step (seats). The tatami is nobody's floor.",
                  "The gap under the raised floor (things.under) is the cat's way and Little Sister's: she goes in at `under` and comes back with the fish.",
                  "The kamachi board's row at a given Z is V.pt(420, 45, Z): someone seated there is drawn in front of it; the raised room's things (chest, money box, god-shelf, back wall) are the backdrop's."],
    }
    with open(f"{OUT}/layout.json", "w") as f:
        json.dump(out, f, indent=1)
    return out


if __name__ == "__main__":
    t0 = __import__("time").time()
    if "layout" in sys.argv:
        os.makedirs(OUT, exist_ok=True)
        lo = layout()
        print(f"{OUT}/layout.json: {len(lo['marks'])} marks, {len(lo['things'])} things, {len(lo['planes'])} planes, {len(lo['fx'])} fx")
        sys.exit(0)
    files = composite()
    finish(files)
    lo = layout()
    print(f"{OUT}: {len(files)} pictures, {len(lo['marks'])} marks, {len(lo['planes'])} planes, {len(lo['fx'])} fx, {__import__('time').time() - t0:.0f} s")
    for k, m in lo["marks"].items():
        print(f"  {k:9s} at {m['at']} face {m['face']} grownup {m['grownup_px']}")

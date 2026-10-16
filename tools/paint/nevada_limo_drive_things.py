"""The upright things beside the road (nevada_limo_drive.py, DRIVE-16P): drive-things.png, a sheet of pictures, and
drive-things.json, where each one is on it.

Each thing is painted as the camera sees it, at 24 pixels a metre, on clear ground with hard edges, its foot on the
ground at the middle of its bottom row; the engine stands it at its place along the road and draws it at the size it
is there. (A billboard facing the camera is exactly right for anything that lies across the road: a sign facing the
traffic, a pole's crossarm. Round things look the same from anywhere.) Heights are true: the telephone pole 8.7 m to
its top insulator, the fence post 1.3 m, the reflector post 1.1 m, the mile marker 1.5 m, sagebrush 0.6 to 1 m,
the Joshua trees 5 and 4 m.

TWO LIGHTS. One sun, low on the car's right and a little behind it, lights everything from the screen's right through
both sides' windows, but not alike: through the LEFT windows we have the sun at our back and see the things' sunlit
faces, a sliver of shade on their left (`-l`); through the RIGHT windows we look toward the sun's side of the sky and
see their shaded faces, with a rim of sun down their right-hand edge (`-r`). So every thing is here twice.

NO SHADOWS ON THE SHEET (DRIVE-16F). A shadow lies on the ground, and the engine stands each picture upright: a shadow
painted along a picture's bottom rows stood up with it, a brown bar in the air beside the post. So each thing is
painted alone, its box only as wide as the thing itself (the foot still the middle of its bottom edge), and the engine
lays each thing's shadow on the ground in perspective, from its foot along the sun (the drive's `sun`: 0.36 m forward
and 1.95 m to the car's left a metre of height, this kit's SHADOW_FWD and SHADOW_LEFT), as wide as the thing is at each
height of it: away from the road on the left, toward it on the right.

Every thing also has its plain name (pole, post, sage-1, joshua, reflector, marker, sign-range...): the picture for the
side it mostly stands on (the reflector posts, the mile marker and the signs' backs the left's; everything else the
right's, as the master brief's example has it). Signs are seen from the right as faces (OPEN RANGE with a cow; NEXT SERVICES 112 MI),
and from the left as backs (the oncoming traffic's signs face away from us). All original and plain: no real sign's
design is copied; the lettering is Pillow's plain face."""

import json
import math

import numpy as np
from PIL import Image

from brush import F32, lerp, rgb
from letter import mask as letter_mask
from nevada_limo_drive_kit import SUN_EL, THINGS_PPM, smoke                # (DRIVE-16F: the shadows are the engine's now)
from nevada_roadside_kit import Paper
from solid import mix

PPM = THINGS_PPM
SUN_PHI = {"l": 44.0, "r": 115.0}                                         # the sun round the thing from the side facing us, + to the right


def sun_vec(light):
    """Toward the sun, in the picture's frame: x right, y up, z toward the camera."""
    p, e = math.radians(SUN_PHI[light]), math.radians(SUN_EL)
    return np.array([math.sin(p) * math.cos(e), math.sin(e), math.cos(p) * math.cos(e)], F32)


def shade_of(n, light, ambient=0.24):
    """How lit a surface turned to the normal n (picture frame) is: 0 to about 1."""
    s = sun_vec(light)
    return float(np.clip(ambient + 0.82 * max(0.0, float(np.dot(n, s))), 0, 1.15))


def tone(tones, t):
    """A colour from four tones (deep shade, shade, lit, highlight) by how lit, 0 to 1+."""
    t = float(np.clip(t, 0, 1.15))
    if t < 0.35:
        return mix(tones[0], tones[1], t / 0.35)
    if t < 0.75:
        return mix(tones[1], tones[2], (t - 0.35) / 0.40)
    return mix(tones[2], tones[3], min(1.0, (t - 0.75) / 0.35))


class Thing:
    """A thing being drawn on its own canvas: metres up and across from its foot, to canvas pixels."""

    def __init__(self, half_w_m, height_m, top_pad=4):
        hw = int(math.ceil(half_w_m * PPM)) + 3                             # (DRIVE-16F: no room for a shadow: it is the engine's)
        self.w = 2 * hw + 1
        self.h = int(math.ceil(height_m * PPM)) + top_pad + 2
        self.fx, self.fy = hw + 0.5, float(self.h)                          # the foot: the middle of the bottom edge
        self.sheet = Paper((self.h, self.w), ss=4)

    def p(self, x_m, y_m):
        return (self.fx + x_m * PPM, self.fy - y_m * PPM)

    def poly(self, pts, color, alpha=1.0):
        self.sheet.poly([self.p(*q) for q in pts], color, alpha)

    def line(self, pts, color, width_m, alpha=1.0):
        self.sheet.line([self.p(*q) for q in pts], color, max(0.5, width_m * PPM), alpha)

    def dot(self, x_m, y_m, rx_m, ry_m, color, alpha=1.0):
        cx, cy = self.p(x_m, y_m)
        self.sheet.ellipse(cx, cy, max(0.35, rx_m * PPM), max(0.35, ry_m * PPM), color, alpha)

    # (DRIVE-16F: `shadow`, the band painted along the bottom rows, is gone: the engine lays the shadow on the ground)

    def done(self):
        c, a = self.sheet.done()
        return c, a


# ---------------------------------------------------------------- round upright things: poles, posts
def tube(t, x_m, y0, y1, r0, r1, tones, light, n=9, grain=None):
    """An upright round thing from y0 to y1 m, r0 to r1 m thick: strips across it lit as a cylinder is."""
    for i in range(n):
        u0, u1 = -1 + 2 * i / n, -1 + 2 * (i + 1) / n
        um = (u0 + u1) / 2
        nrm = np.array([um, 0.0, math.sqrt(max(0.0, 1 - um * um))], F32)
        c = tone(tones, shade_of(nrm, light))
        t.poly([(x_m + u0 * r0, y0), (x_m + u1 * r0, y0), (x_m + u1 * r1, y1), (x_m + u0 * r1, y1)], c)


def pole(light, seed=11):
    """A telephone pole: a weathered wooden pole, its crossarm across the road with two braces and four glass
    insulators on pins, one more on its top. The wires (the engine's) meet it at 8.6 m (the top) and 8.1 m."""
    rng = np.random.default_rng(seed)
    t = Thing(1.3, 8.75)                                                   # (DRIVE-16F: no shadow painted: the engine's)
    wood = ("#3a3240", "#6a5a54", "#a89080", "#d8c0a4")
    tube(t, 0.0, 0.0, 8.5, 0.15, 0.11, wood, light, n=11)
    for k in range(9):                                                     # checks and cracks in the old wood, and its grain
        y = rng.uniform(0.3, 8.0)
        t.line([(rng.uniform(-0.05, 0.05), y), (rng.uniform(-0.05, 0.05), y + rng.uniform(0.4, 1.4))], "#3e3440", 0.025, 0.7)
    t.dot(0.0, 8.5, 0.11, 0.035, tone(wood, 0.9))                          # its top, cut and weathered
    # the crossarm (seen end on to the road: it lies across, so we see its whole length), braces, insulators
    arm = tone(wood, shade_of(np.array([0, 0, 1.0], F32), light))
    t.poly([(-1.2, 8.02), (1.2, 8.02), (1.2, 8.13), (-1.2, 8.13)], arm)
    t.poly([(-1.2, 8.11), (1.2, 8.11), (1.2, 8.14), (-1.2, 8.14)], tone(wood, 0.95))     # its top in the sky's light
    t.line([(-0.12, 7.55), (-0.75, 8.03)], tone(wood, 0.3), 0.035)
    t.line([(0.12, 7.55), (0.75, 8.03)], tone(wood, 0.5), 0.035)
    glass = ("#2e5a5a", "#4e8a86", "#86c4b8", "#dcfff4")
    for xi in (-1.05, -0.4, 0.4, 1.05):
        t.line([(xi, 8.14), (xi, 8.2)], "#5a5048", 0.03)
        t.poly([(xi - 0.05, 8.2), (xi + 0.05, 8.2), (xi + 0.035, 8.32), (xi - 0.035, 8.32)], tone(glass, 0.55 if light == "l" else 0.3))
        t.dot(xi + 0.025, 8.27, 0.012, 0.03, glass[3], 0.9)
    t.line([(0.0, 8.5), (0.0, 8.58)], "#5a5048", 0.03)
    t.poly([(-0.05, 8.58), (0.05, 8.58), (0.035, 8.72), (-0.035, 8.72)], tone(glass, 0.55 if light == "l" else 0.3))
    t.dot(0.025, 8.66, 0.012, 0.03, glass[3], 0.9)
    t.dot(0.0, 0.02, 0.2, 0.03, "#4e4044", 0.8)                             # where it goes into the ground
    return t.done()


def post(light, seed=12):
    """A wooden fence post, 1.3 m: grey, split and leaning a hair, its top cut aslant, the staples of three wires."""
    rng = np.random.default_rng(seed)
    t = Thing(0.2, 1.36)                                                   # (DRIVE-16F: no shadow painted)
    wood = ("#3e3846", "#6e6464", "#aea290", "#e2d6c0")
    lean = rng.normal(0, 0.01)
    tube(t, 0.0, 0.0, 1.3, 0.07, 0.06, wood, light, n=7)
    t.poly([(-0.06 + lean, 1.28), (0.06 + lean, 1.33), (0.06 + lean, 1.3), (-0.06 + lean, 1.26)], tone(wood, 0.95))
    for k in range(3):
        y = rng.uniform(0.1, 1.0)
        t.line([(rng.uniform(-0.03, 0.03), y), (rng.uniform(-0.03, 0.03), y + rng.uniform(0.15, 0.35))], "#463e48", 0.012, 0.8)
    for hy in (1.25, 0.95, 0.65):
        t.dot(-0.04, hy, 0.016, 0.012, "#2e2a34")
    return t.done()


def tpost(light, seed=13):
    """A steel fence post, 1.25 m: painted green, its top white, the clips of three wires."""
    t = Thing(0.15, 1.28)                                                  # (DRIVE-16F: no shadow painted)
    steel = ("#1e2a26", "#3a5440", "#6a8a62", "#b4cca4")
    tube(t, 0.0, 0.0, 1.12, 0.035, 0.03, steel, light, n=5)
    tube(t, 0.0, 1.12, 1.25, 0.03, 0.028, ("#8a8a9a", "#c4c4cc", "#eeeeea", "#ffffff"), light, n=5)
    for hy in (1.2, 0.92, 0.64):
        t.dot(0.02, hy, 0.014, 0.01, "#c8c8cc")
    return t.done()


def reflector(light, seed=14):
    """A white reflector post at the shoulder's edge, 1.1 m: a flat white post, an amber reflector near its top."""
    t = Thing(0.2, 1.12)                                                   # (DRIVE-16F: no shadow painted)
    white = ("#8c8ca4", "#c4c4d0", "#f2f0ea", "#ffffff")
    face = shade_of(np.array([0.0, 0.0, 1.0], F32), light)
    t.poly([(-0.05, 0.0), (0.05, 0.0), (0.05, 1.1), (-0.05, 1.1)], tone(white, face))
    t.poly([(0.03, 0.0), (0.05, 0.0), (0.05, 1.1), (0.03, 1.1)], tone(white, shade_of(np.array([0.9, 0, 0.44], F32), light)))
    t.poly([(-0.05, 0.0), (-0.03, 0.0), (-0.03, 1.1), (-0.05, 1.1)], tone(white, shade_of(np.array([-0.9, 0, 0.44], F32), light)))
    t.poly([(-0.035, 0.86), (0.035, 0.86), (0.035, 1.02), (-0.035, 1.02)], "#e88a28")
    t.poly([(-0.035, 0.98), (0.035, 0.98), (0.035, 1.02), (-0.035, 1.02)], "#ffc46a")
    t.poly([(-0.05, 0.0), (0.05, 0.0), (0.05, 0.08), (-0.05, 0.08)], "#a8a29a")                # dust splashed on its foot
    return t.done()


def marker(light, seed=15):
    """A mile marker, 1.5 m: a small green plate, a white border, MILE and the number stacked, on a steel post."""
    t = Thing(0.25, 1.52)                                                  # (DRIVE-16F: no shadow painted)
    steel = ("#4a4a5a", "#7a7a88", "#b4b4be", "#e4e4ea")
    tube(t, 0.0, 0.0, 0.8, 0.025, 0.025, steel, light, n=4)
    face = shade_of(np.array([0.0, 0.25, 0.97], F32), light)
    green = tone(("#123826", "#1e4a34", "#2e6a4a", "#5a9a74"), face + 0.15)
    white = tone(("#8a8aa0", "#c4c4cc", "#f0f0e8", "#ffffff"), face + 0.35)
    t.poly([(-0.17, 0.78), (0.17, 0.78), (0.17, 1.5), (-0.17, 1.5)], white)
    t.poly([(-0.145, 0.805), (0.145, 0.805), (0.145, 1.475), (-0.145, 1.475)], green)
    _words(t, [("MILE", 1.38, 0.07), ("4", 1.2, 0.13), ("1", 0.99, 0.13)], white)
    return t.done()


def _words(t, lines, color, bold=False):
    """Lettering on a plate: [(words, middle height m, letter height m)], Pillow's plain face, laid as paint."""
    for words, ym, size_m in lines:
        cx, cy = t.p(0.0, ym)
        m = letter_mask((t.h, t.w), words, (cx, cy), size_m * PPM * 1.3, anchor="mm", rough=0.0)
        if bold:
            from brush import blur
            m = np.clip(m * 1.6, 0, 1)
        ys, xs = np.nonzero(m > 0.02)
        for yy, xx in zip(ys.tolist(), xs.tolist()):
            t.sheet.poly([(xx, yy), (xx + 1, yy), (xx + 1, yy + 1), (xx, yy + 1)], color, float(min(1.0, m[yy, xx] * 1.15)))


def sign_range(light, seed=16):
    """OPEN RANGE, with a cow: a plain yellow board, a black cow standing on its left, the words on its right, on two
    steel posts."""
    t = Thing(1.05, 2.75)                                                  # (DRIVE-16F: no shadow painted)
    steel = ("#4a4a5a", "#7a7a88", "#b4b4be", "#e4e4ea")
    for px in (-0.6, 0.6):
        tube(t, px, 0.0, 1.6, 0.035, 0.035, steel, light, n=5)
    face = shade_of(np.array([0.0, 0.15, 0.99], F32), light) + 0.2
    board = tone(("#6a5420", "#a8862c", "#e6be3c", "#ffe27a"), face)
    ink = "#1e1c22"
    t.poly([(-0.98, 1.55), (0.98, 1.55), (0.98, 2.72), (-0.98, 2.72)], ink)
    t.poly([(-0.94, 1.59), (0.94, 1.59), (0.94, 2.68), (-0.94, 2.68)], board)
    # the cow, standing, facing right: a plain shape of my own, 0.8 m long on the board
    cx, cy = -0.52, 1.99
    q = lambda pts: [(cx + x * 1.05, cy + y * 1.05) for x, y in pts]
    t.poly(q([(-0.30, 0.0), (0.22, 0.0), (0.26, 0.05), (0.26, 0.24), (0.20, 0.28), (-0.26, 0.28), (-0.31, 0.22), (-0.31, 0.04)]), ink)
    t.poly(q([(0.20, 0.20), (0.29, 0.30), (0.39, 0.29), (0.45, 0.20), (0.44, 0.13), (0.37, 0.12), (0.30, 0.15), (0.22, 0.10)]), ink)
    t.line(q([(0.31, 0.29), (0.34, 0.37)]), ink, 0.03)                    # a horn
    t.line(q([(0.37, 0.28), (0.43, 0.33)]), ink, 0.03)                    # an ear
    for lx in (-0.27, -0.18, 0.12, 0.2):                                   # the legs
        t.poly(q([(lx - 0.025, 0.02), (lx + 0.025, 0.02), (lx + 0.025, -0.2), (lx - 0.025, -0.2)]), ink)
    t.line(q([(-0.31, 0.24), (-0.36, 0.06)]), ink, 0.025)                 # the tail
    t.dot(*q([(-0.36, 0.05)])[0], 0.03, 0.04, ink)
    for words, ym in (("OPEN", 2.33), ("RANGE", 1.92)):
        cx2, cy2 = t.p(0.48, ym)
        m = letter_mask((t.h, t.w), words, (cx2, cy2), 0.22 * PPM * 1.3, anchor="mm", rough=0.0)
        ys, xs = np.nonzero(m > 0.02)
        for yy, xx in zip(ys.tolist(), xs.tolist()):
            t.sheet.poly([(xx, yy), (xx + 1, yy), (xx + 1, yy + 1), (xx, yy + 1)], ink, float(min(1.0, m[yy, xx] * 1.25)))
    return t.done()


def _shift_words(t, words_lines, color, dx):
    for words, ym, size_m in words_lines:
        cx, cy = t.p(dx, ym)
        m = letter_mask((t.h, t.w), words, (cx, cy), size_m * PPM * 1.3, anchor="mm", rough=0.0)
        ys, xs = np.nonzero(m > 0.02)
        for yy, xx in zip(ys.tolist(), xs.tolist()):
            t.sheet.poly([(xx, yy), (xx + 1, yy), (xx + 1, yy + 1), (xx, yy + 1)], color, float(min(1.0, m[yy, xx] * 1.15)))


def sign_services(light, seed=17):
    """NEXT SERVICES 112 MI: a plain green board, a white border and white letters, on two steel posts."""
    t = Thing(1.4, 2.9)                                                    # (DRIVE-16F: no shadow painted)
    steel = ("#4a4a5a", "#7a7a88", "#b4b4be", "#e4e4ea")
    for px in (-0.9, 0.9):
        tube(t, px, 0.0, 1.75, 0.04, 0.04, steel, light, n=5)
    face = shade_of(np.array([0.0, 0.15, 0.99], F32), light) + 0.15
    green = tone(("#103224", "#1a4632", "#286648", "#4e9070"), face)
    white = tone(("#8a8aa0", "#c4c4cc", "#f0f0e8", "#ffffff"), face + 0.3)
    t.poly([(-1.32, 1.7), (1.32, 1.7), (1.32, 2.86), (-1.32, 2.86)], white)
    t.poly([(-1.27, 1.75), (1.27, 1.75), (1.27, 2.81), (-1.27, 2.81)], green)
    _words(t, [("NEXT SERVICES", 2.5, 0.2), ("112 MI", 2.08, 0.2)], white)
    return t.done()


def sign_back(light, seed=18, big=False):
    """The back of a sign facing the oncoming traffic: bare grey metal, two rails bolted across it, its posts."""
    wide, top, bottom = (1.32, 2.86, 1.7) if big else (0.74, 2.55, 1.65)
    t = Thing(wide + 0.1, top + 0.05)                                      # (DRIVE-16F: no shadow painted)
    steel = ("#4a4a5a", "#7a7a88", "#b4b4be", "#e4e4ea")
    for px in ((-0.9, 0.9) if big else (0.0,)):
        tube(t, px, 0.0, top - 0.1, 0.035, 0.035, steel, light, n=5)
    face = shade_of(np.array([0.0, 0.15, 0.99], F32), light) + 0.1
    t.poly([(-wide, bottom), (wide, bottom), (wide, top), (-wide, top)], tone(("#585a68", "#868896", "#b8bac2", "#e2e4ea"), face))
    for ry in (bottom + (top - bottom) * 0.28, bottom + (top - bottom) * 0.72):
        t.poly([(-wide, ry - 0.035), (wide, ry - 0.035), (wide, ry + 0.035), (-wide, ry + 0.035)], tone(("#3e404c", "#5e606e", "#8e909c", "#c4c6ce"), face))
        t.poly([(-wide, ry + 0.025), (wide, ry + 0.025), (wide, ry + 0.035), (-wide, ry + 0.035)], tone(("#3e404c", "#5e606e", "#8e909c", "#c4c6ce"), face + 0.4))
    return t.done()


# ---------------------------------------------------------------- what grows
def dome_sprays(t, cx, base, rx, ry, count, tones, light, seed, leaf=0.05, lift=0.08):
    """A rounded bush's sprays: short leafy strokes over a dome rx wide and ry high, each lit by where it is on the
    dome. The deep ones first, the lit ones last."""
    rng = np.random.default_rng(seed)
    ph1, ph2 = rng.uniform(0, 6.3), rng.uniform(0, 6.3)
    lump = lambda a: 1 + 0.10 * math.sin(3 * a + ph1) + 0.06 * math.sin(5 * a + ph2)
    for k in range(int(count * 0.12)):                                    # the dark inside, seen through gaps
        a = math.radians(rng.uniform(20, 160))
        d = rng.random() ** 0.8 * 0.7
        t.dot(cx + math.cos(a) * d * rx, base + lift + math.sin(a) * d * ry, leaf * 1.3, leaf * 1.1, tones[0])
    sprays = []
    for k in range(count):
        a = math.radians(rng.uniform(4, 176))
        d = rng.random() ** 0.55 * lump(a)
        nx, ny = math.cos(a) * d, math.sin(a) * d
        nz = math.sqrt(max(0.0, 1 - nx * nx - ny * ny))
        lit = shade_of(np.array([nx, ny, nz], F32), light) + rng.normal(0, 0.08)
        rim = max(0.0, nx) * (1 - nz) * (0.55 if light == "r" else 0.15)  # backlit, the silver hairs on the edge glow
        if rng.random() < 0.18:                                           # sprays deep in the bush, in its own shade
            lit -= 0.35
        sprays.append((lit + rim, cx + nx * rx, base + lift + ny * ry, a))
    for lit, x, y, a in sorted(sprays):
        c = tone(tones, lit)
        for j in range(3):
            b = a + rng.normal(0, 0.55)
            l = leaf * rng.uniform(0.7, 1.4)
            t.line([(x, y), (x + math.cos(b) * l, y + math.sin(b) * l * 0.9 + l * 0.3)], c, 0.03, 0.95)


def sage(light, height, width, seed):
    """Sagebrush: crooked grey wood at the foot, a dome of grey-green sprays, silver where the light catches them."""
    rng = np.random.default_rng(seed)
    t = Thing(width / 2 + 0.1, height + 0.1)                               # (DRIVE-16F: no shadow painted)
    for k in range(6):                                                     # the woody stems
        a = math.radians(rng.uniform(55, 125))
        l = height * rng.uniform(0.3, 0.55)
        x0 = rng.normal(0, width * 0.08)
        t.line([(x0, 0.0), (x0 + math.cos(a) * l * 0.5, math.sin(a) * l * 0.5), (x0 + math.cos(a) * l, math.sin(a) * l)], "#4a3a32", 0.035)
    dome_sprays(t, 0.0, 0.0, width / 2, height * 0.88, int(70 + width * 90), ("#283028", "#4a5644", "#7a886a", "#b8c09c"), light, seed + 1, leaf=0.06)
    return t.done()


def creosote(light, seed=31, height=1.5, width=1.8):
    """Creosote: many thin dark stems fanning up from the foot like a vase, small dark-green leaves in knots on them,
    open, the ground seen through it."""
    rng = np.random.default_rng(seed)
    t = Thing(width / 2 + 0.15, height + 0.12)                             # (DRIVE-16F: no shadow painted)
    tones = ("#222a1e", "#3e4a26", "#6a7a36", "#b0ba6a")
    stems = []
    for k in range(22):
        a = math.radians(rng.uniform(58, 122))
        l = height * rng.uniform(0.6, 1.0)
        x0 = rng.normal(0, 0.05)
        bend = rng.normal(0, 0.12)
        pts = [(x0 + math.cos(a) * l * s + bend * s * s, math.sin(a) * l * s) for s in np.linspace(0, 1, 5)]
        stems.append(pts)
        t.line(pts, "#3a3028", 0.018)
    for pts in stems:
        for s in (0.45, 0.65, 0.82, 1.0):
            x, y = pts[min(4, int(s * 4))]
            for j in range(3):
                dx, dy = rng.normal(0, 0.06), rng.normal(0, 0.05)
                nx = np.clip((x + dx) / (width / 2), -1, 1)
                lit = shade_of(np.array([nx, 0.4, math.sqrt(max(0.0, 1 - nx * nx - 0.16))], F32), light) + rng.normal(0, 0.08)
                t.dot(x + dx, y + dy, 0.035, 0.03, tone(tones, lit))
    return t.done()


def rabbitbrush(light, seed=41, height=0.9, width=1.0):
    """Rabbitbrush in October: a rounded mass of fine upright grey-green stems, flat heads of yellow flowers on top."""
    rng = np.random.default_rng(seed)
    t = Thing(width / 2 + 0.1, height + 0.1)                               # (DRIVE-16F: no shadow painted)
    for k in range(40):                                                    # the stems, upright
        x0 = rng.normal(0, width * 0.12)
        a = math.radians(rng.uniform(70, 110))
        l = height * rng.uniform(0.5, 0.85)
        nx = np.clip(x0 / (width / 2), -1, 1)
        t.line([(x0, 0.0), (x0 + math.cos(a) * l, math.sin(a) * l)], tone(("#3a4234", "#5e6a52", "#94a080", "#c8d0b0"), shade_of(np.array([nx, 0.2, 0.8], F32), light)), 0.02)
    dome_sprays(t, 0.0, height * 0.25, width / 2, height * 0.55, 90, ("#323e2c", "#56644a", "#8a9872", "#bcc49c"), light, seed + 1, leaf=0.05, lift=0.0)
    for k in range(70):                                                    # the flower heads
        a = math.radians(rng.uniform(20, 160))
        d = rng.random() ** 0.4
        x, y = math.cos(a) * d * width * 0.48, height * 0.62 + math.sin(a) * d * height * 0.36
        nx = x / (width / 2)
        lit = shade_of(np.array([nx, 0.7, math.sqrt(max(0.0, 1 - nx * nx * 0.5 - 0.49))], F32), light)
        t.dot(x, y, 0.045, 0.03, tone(("#8a6a1c", "#c09a28", "#ecc63c", "#fff08a"), lit + 0.1))
    return t.done()


def joshua(light, seed=51, height=5.0, arms=3):
    """A Joshua tree: a stout trunk in a shaggy skirt of dead grey leaves, two or three arms forking out and up and
    forking again, every limb shaggy, each tip a ball of stiff dark-green spikes, the crown as wide as it is tall."""
    rng = np.random.default_rng(seed)
    segs, tips = [], []

    def grow(x, y, ang, length, thick, depth):
        """A limb from (x, y) at `ang` degrees from upright (+ to the right): a bend at its middle, then a fork or a tip."""
        bend = ang * rng.uniform(0.35, 0.7)                                # limbs turn upward as they grow
        mx, my = x + math.sin(math.radians(ang)) * length * 0.5, y + math.cos(math.radians(ang)) * length * 0.5
        ex, ey = mx + math.sin(math.radians(bend)) * length * 0.5, my + math.cos(math.radians(bend)) * length * 0.5
        segs.append(((x, y), (mx, my), thick))
        segs.append(((mx, my), (ex, ey), thick * 0.92))
        if depth > 0 and rng.random() < 0.85:
            n = 2 if rng.random() < 0.75 else 1
            for k in range(n):
                a = bend + (rng.uniform(18, 42) * (-1 if k == 0 else 1) if n == 2 else rng.uniform(-25, 25))
                grow(ex, ey, a, length * rng.uniform(0.62, 0.85), thick * 0.82, depth - 1)
        else:
            tips.append((ex, ey))

    trunk_top = 1.0
    segs.append(((0.0, 0.0), (0.02, trunk_top), 0.36))
    for k in range(arms):
        a = (k - (arms - 1) / 2) * rng.uniform(38, 55) + rng.normal(0, 8)
        grow(0.02, trunk_top - 0.05, a, rng.uniform(1.0, 1.35), 0.24, 2)
    # scale it to its height (the leaf balls' tops), keeping its foot
    top = max(ty for tx, ty in tips) + 0.32
    k_ = height / top
    segs = [((a[0] * k_, a[1] * k_), (b[0] * k_, b[1] * k_), t * min(1.0, k_ * 0.9 + 0.1)) for a, b, t in segs]
    tips = [(tx * k_, ty * k_) for tx, ty in tips]
    span = max(abs(tx) for tx, ty in tips) + 0.45
    t = Thing(span, height + 0.25)                                         # (DRIVE-16F: no shadow painted)
    bark = ("#2e2a30", "#55493f", "#8a7a64", "#c4b08c")
    shag = ("#3a3236", "#6a5c4e", "#a08c6c", "#d4c098")
    for (a, b, th) in segs:                                                 # the limbs, each a shaded round thing
        dxs, dys = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dxs, dys) + 1e-6
        nx, ny = dys / L, -dxs / L                                          # across the limb, to its right
        for i, u in enumerate(np.linspace(-1, 1, 5)):
            nrm = np.array([nx * u, ny * u, math.sqrt(max(0.0, 1 - u * u))], F32)
            c = tone(bark, shade_of(nrm, light))
            off = u * th * 0.4
            t.line([(a[0] + nx * off, a[1] + ny * off), (b[0] + nx * off, b[1] + ny * off)], c, th * 0.32)
    for (a, b, th) in segs:                                                 # the shag: dead leaves hanging down every limb
        for j in range(int(6 + 26 * math.hypot(b[0] - a[0], b[1] - a[1]))):
            f = rng.random()
            x, y = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
            side = rng.choice([-1.0, 1.0])
            x += side * th * rng.uniform(0.3, 0.6)
            nrm = np.array([side * 0.8, -0.2, 0.55], F32)
            c = tone(shag, shade_of(nrm / np.linalg.norm(nrm), light) + rng.normal(0, 0.07))
            t.line([(x, y), (x + side * rng.uniform(0.02, 0.07), y - rng.uniform(0.1, 0.24))], c, 0.028)
    green = ("#1e2a1c", "#34472c", "#5c7040", "#a4b46c")
    for (tx, ty) in tips:                                                   # the leaf balls: stiff spikes all ways, up most
        spikes = []
        for j in range(60):
            a = rng.uniform(-0.25 * math.pi, 1.25 * math.pi) if rng.random() < 0.8 else rng.uniform(0, 2 * math.pi)
            l = rng.uniform(0.2, 0.36)
            nx, ny = math.cos(a), math.sin(a)
            lit = shade_of(np.array([nx * 0.9, ny * 0.9, 0.42], F32), light) + rng.normal(0, 0.07)
            spikes.append((lit, a, l))
        t.dot(tx, ty + 0.04, 0.13, 0.12, tone(green, 0.15))
        for lit, a, l in sorted(spikes):
            t.line([(tx, ty + 0.04), (tx + math.cos(a) * l, ty + 0.04 + math.sin(a) * l)], tone(green, lit), 0.034)
    return t.done()


def rock(light, seed=61, height=0.6, width=1.1):
    """A boulder, rounded and cracked, its sunward planes warm."""
    rng = np.random.default_rng(seed)
    t = Thing(width / 2 + 0.1, height + 0.08)                              # (DRIVE-16F: no shadow painted)
    tones = ("#4a3c48", "#7a6060", "#c09a7c", "#f2d4ae")
    pts = []
    for i in range(12):
        a = math.pi * i / 11
        r = 1.0 + rng.normal(0, 0.06)
        pts.append((math.cos(a) * width / 2 * r, math.sin(a) * height * r))
    t.poly(pts + [(-width / 2, 0.0), (width / 2, 0.0)], tones[0])
    for k in range(9):                                                     # facets, lit by their facing
        a = rng.uniform(0.15, math.pi - 0.15)
        d = rng.uniform(0.25, 0.8)
        cx, cy = math.cos(a) * width / 2 * d, math.sin(a) * height * d
        n = np.array([math.cos(a), math.sin(a), 0.7], F32)
        c = tone(tones, shade_of(n / np.linalg.norm(n), light) + rng.normal(0, 0.05))
        s = rng.uniform(0.12, 0.24)
        t.poly([(cx - s, cy - s * 0.5), (cx + s * 0.6, cy - s * 0.6), (cx + s, cy + s * 0.4), (cx - s * 0.3, cy + s * 0.6)], c)
    t.line([(-0.1, height * 0.2), (0.05, height * 0.55), (0.0, height * 0.8)], tones[0], 0.02)
    return t.done()


# ---------------------------------------------------------------- the sheet
SPRITES = [  # base name, painter
    ("pole", pole), ("post", post), ("tpost", tpost), ("reflector", reflector), ("marker", marker),
    ("sage-1", lambda L: sage(L, 0.6, 1.0, 71)), ("sage-2", lambda L: sage(L, 0.8, 1.3, 72)), ("sage-3", lambda L: sage(L, 1.0, 1.6, 73)),
    ("creosote", creosote), ("rabbitbrush", rabbitbrush),
    ("joshua", lambda L: joshua(L, 51, 5.0, 3)), ("joshua-2", lambda L: joshua(L, 54, 4.0, 2)),
    ("sign-range", sign_range), ("sign-services", sign_services),
    ("sign-back", lambda L: sign_back(L, 18, False)), ("sign-back-2", lambda L: sign_back(L, 19, True)),
    ("rock", rock),
]
# Every thing also under its plain name: the picture for the side it mostly stands on. The fence, the poles and the
# signs' faces are the right's (the brief's example puts pole, post, sage-1, sage-2 and joshua there, so the plants are
# the right's too); the reflector posts, the mile marker and the signs' backs are the left's. On the other side, use
# the names with -l or -r: a plant on the left is best drawn with its -l picture.
ALIASES = {name: name + ("-l" if name in ("reflector", "marker", "sign-back", "sign-back-2") else "-r") for name, fn in SPRITES}


def crop(c, a):
    """Cut a thing's canvas to what is painted, keeping its foot at the middle of the bottom edge."""
    hard = a >= 0.5
    ys, xs = np.nonzero(hard)
    h, w = a.shape
    mid = (w - 1) // 2                                                     # the middle column (the canvas is odd wide)
    half = int(max(mid - xs.min(), xs.max() - mid)) if len(xs) else 0
    top = int(ys.min()) if len(ys) else h - 1
    x0, x1 = mid - half, mid + half + 1
    return c[top:, x0:x1], a[top:, x0:x1]


def paint_things():
    """Every thing in both lights, cropped. -> [(name, rgb, alpha)] (smoked)."""
    out = []
    for name, fn in SPRITES:
        for L in ("l", "r"):
            c, a = fn(L)
            # hard edges, cut a little past half: a filled shape on the sheet spreads by a part of a pixel, and a thin
            # post would otherwise come out a pixel wider where it is widest (a step in it)
            a = (a >= 0.56).astype(F32)
            c, a = crop(c, a)
            out.append((f"{name}-{L}", smoke(c), a))
    return out


def pack(items, width=1024, gap=2):
    """Lay the pictures on a sheet in shelves, tallest first. -> (sheet rgb, alpha, {name: (x, y, w, h)})."""
    order = sorted(items, key=lambda it: (-it[2].shape[0], -it[2].shape[1]))
    boxes, x, y, shelf = {}, gap, gap, 0
    for name, c, a in order:
        h, w = a.shape
        if x + w + gap > width:
            x, y, shelf = gap, y + shelf + gap, 0
        boxes[name] = (x, y, w, h)
        x += w + gap
        shelf = max(shelf, h)
    H = y + shelf + gap
    rgb_ = np.zeros((H, width, 3), F32)
    alpha = np.zeros((H, width), F32)
    for name, c, a in items:
        x, y, w, h = boxes[name]
        rgb_[y:y + h, x:x + w] = c
        alpha[y:y + h, x:x + w] = a
    return rgb_, alpha, boxes


def sheet_json(boxes, heights):
    sprites = {}
    for name in sorted(boxes):
        x, y, w, h = boxes[name]
        sprites[name] = {"box": [x, y, w, h], "foot": [w / 2, h], "height": round(heights[name], 2)}
    for alias, name in ALIASES.items():
        sprites[alias] = dict(sprites[name])
    # exactly the contract's shape: { "ppm": 24, "sprites": { name: { "box", "foot", "height" } } }; each foot is in its
    # box's own pixels, from the box's top left (the middle of its bottom edge: [w / 2, h])
    return {"ppm": int(PPM), "sprites": dict(sorted(sprites.items()))}

"""Everything inside the limousine, built in the car's own centimetres (nevada_limo.py).

Each function puts one group of things on the Stage (nevada_limo_kit.Stage): boxes, rods, round things and flat
sheets, each with a material that paints it in ITS OWN measurements. All measurements come from the model
(nevada_limo_model.py), so the skeleton, the picture and layout.json agree.

Groups (grp): "back" is the backdrop. A cut-out is its own group: "glass" (the divider, up or down), "ropes", "bag",
"juice", "clipboard", and "front" (the seat we sit on and its armrests). The ropes have four states (strands left) and
the divider two (up, down). Glass (the window panes, the divider) is flat colour that no light in the car changes
(the kit's flag 4)."""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, lerp, sample, blur
import nevada_limo_model as M
from nevada_limo_kit import col, mixc, fbm, hashf, grad_of, lines_aa, band, rect, disc, lay, sstep, curve3

# ---------------------------------------------------------------- the colours of things (before any light falls on them)
LEATHER = "#a8a2a2"          # gray leather, the seats (a warm light gray: it takes the windows' light)
LEATHER_D = "#4c4a52"        # its grooves and seams
LEATHER_BACK = "#7e787a"     # the backrests, a shade darker
CARPET = "#4e3846"           # a deep plum-gray pile: the gray raccoon reads on it
CARPET_FLECK = "#664a58"
WALL = "#74727a"             # the padded panels round the windows
HEADLINER = "#d8d0c8"        # the ceiling's cloth, a warm light gray
TRIM = "#1c1c22"             # the black rubber round the glass
CHROME = "#e2e6ec"
CHROME_D = "#6a7080"
BAR_WOOD = "#5a3424"
BAR_WOOD_L = "#8e5a3a"
PANE = "#c4ccd6"             # the plain pale desert-sky grey of the window glass when no strip is drawn behind it
GLASS = "#20242e"            # the divider's smoked glass
PAPER = "#b88c5c"            # the bag
CREAM = "#e2dac4"            # the car phone
ROPE = "#f2eee2"
ROPE_RED = "#c8392e"
BELT = "#34343c"


def P3(X, Y, Z):
    return (float(X), float(Y), float(Z))


def plain(color, amt=0.10, s=18.0, seed=0):
    """One paint, a little patchy as a brush leaves it."""
    k = col(color)

    def f(c):
        n = fbm((c.X + 0.37 * c.Y) / s, (c.Z + 0.61 * c.Y) / s, seed, 3)
        return k * (1 + amt * 2 * (n[..., None] - 0.5))
    return f


# ---------------------------------------------------------------- the shell: carpet, walls, windows, headliner, the partition
def m_carpet(c):
    X, Z = c.X, c.Z
    nap = fbm(X / 3.0, Z / 3.0, 21, 3)
    base = col(CARPET) * (0.86 + 0.28 * nap[..., None])
    fleck = sstep(0.74, 0.86, fbm(X / 1.6, Z / 1.6, 23, 2))
    base = lay(base, CARPET_FLECK, fleck * 0.5)
    track = np.exp(-((X - M.W / 2) / 70.0) ** 2) * 0.08               # the pile pressed flat down the middle
    base = base * (1 - track[..., None])
    gX, gZ = c.gX * c.ss, c.gZ * c.ss
    # a chrome sill strip along the foot of each seat, where the carpet meets the leather
    for xe in (M.SEAT_D, M.W - M.SEAT_D):
        base = lay(base, CHROME_D, band(np.abs(X - xe), 0.0, 1.6, gX) * 0.7)
    return base


def m_wall(side):
    """A side wall's padded panels: the black rubber seal and a chrome strip round each pane, a darker pillar between
    the panes with a little vent grille, a padded roll along the sill, a seam above the windows."""
    def f(c):
        Y, Z = c.Y, c.Z
        gY, gZ = c.gY * c.ss, c.gZ * c.ss
        n = fbm(Z / 24.0, Y / 24.0, 5 if side == "L" else 6, 3)
        base = col(WALL) * (0.90 + 0.2 * n[..., None])
        y0, y1 = M.WINDOW_Y
        base = base * (1 - 0.25 * band(Y, y1 + 7.0, y1 + 8.2, gY)[..., None])           # a seam above the glass
        roll = band(Y, M.BACK_H, y0 - 0.5, gY)                                          # the padded sill roll
        base = lay(base, mixc(WALL, "#ffffff", 0.18), roll * 0.7)
        dist = np.full(Y.shape, 1e9, dtype=F32)
        for (z0, z1) in M.PANES[side]:
            dz = np.maximum(np.maximum(z0 - Z, Z - z1), 0)
            dy = np.maximum(np.maximum(y0 - Y, Y - y1), 0)
            dist = np.minimum(dist, np.sqrt(dz * dz + dy * dy))
        g = np.maximum(gY, gZ)
        base = lay(base, TRIM, band(dist, 0.0, 3.2, g))
        base = lay(base, CHROME, band(dist, 3.2, 4.4, g) * 0.9)
        base = lay(base, CHROME_D, band(dist, 4.4, 5.2, g) * 0.6)
        pz0, pz1 = M.PILLAR
        pil = band(Z, pz0 + 5.5, pz1 - 5.5, gZ) * band(Y, y0 + 10, y1 - 10, gY)
        base = lay(base, "#5e5e68", pil * 0.7)
        base = base * (1 - 0.4 * (pil * lines_aa(Y, 2.6, 0.9, gY))[..., None])
        return base
    return f


def m_pane(c):
    """The window glass as painted: the plain pale grey behind which the game scrolls the desert."""
    k = col(PANE)
    return k * (0.985 + 0.03 * fbm(c.Y / 30.0, c.Z / 30.0, 7, 2)[..., None])


def m_headliner(c):
    """The headliner: padded cloth, diamond-tufted (a button at each crossing, the padding puffed between), with a
    console of darker cloth down the middle and the row of small lights set in it."""
    X, Z = c.X, c.Z
    gX, gZ = c.gX * c.ss, c.gZ * c.ss
    g = np.maximum(gX, gZ)
    n = fbm(X / 30.0, Z / 30.0, 9, 3)
    base = col(HEADLINER) * (0.90 + 0.18 * n[..., None])
    # the tufting: a diamond lattice (two sets of diagonal seams), puffed between, a button at every crossing
    TU = 24.0                                                            # the tufting's diamond, cm
    sa, sb = (X + Z * 0.75) / TU, (X - Z * 0.75) / TU
    fa, fb = sa - np.floor(sa), sb - np.floor(sb)
    da, db = np.abs(fa - 0.5), np.abs(fb - 0.5)                            # 0.5 at a seam, 0 in the middle of a diamond
    puff = (1 - np.maximum(da, db) * 2)                                    # 1 in the middle of each diamond, 0 at its seams
    ta = (fa - 0.5) * 2, (fb - 0.5) * 2
    c.nrm = np.stack([-(ta[0] + ta[1]) * 0.12, -np.ones_like(X), -(ta[0] - ta[1]) * 0.09], axis=1).astype(F32)
    c.nrm = c.nrm / np.linalg.norm(c.nrm, axis=1, keepdims=True)
    base = base * (0.88 + 0.12 * np.sqrt(np.clip(puff, 0, 1)))[..., None]
    gs = g * 2.0 / TU
    seam = np.clip(1 - (0.5 - np.maximum(da, db)) / np.maximum(gs, 1e-4), 0, 1)
    base = lay(base, mixc(HEADLINER, "#3a3036", 0.45), seam * 0.30 * np.clip((TU / np.maximum(g, 1e-3) - 3) / 4, 0, 1))
    btn = np.clip((1.4 - np.hypot((np.round(sa) - sa) * TU, (np.round(sb) - sb) * TU)) / np.maximum(g, 1e-3) + 0.5, 0, 1)
    base = lay(base, "#7a6e72", btn * 0.55)
    # the console down the middle, a chrome edge to it
    cw = 26.0
    con = band(np.abs(X - M.W / 2), 0.0, cw / 2, gX)
    base = lay(base, mixc(HEADLINER, "#34303a", 0.55), con)
    base = lay(base, CHROME, band(np.abs(X - M.W / 2), cw / 2 - 1.0, cw / 2, gX) * 0.85)
    c.nrm = np.where(con[:, None] > 0.5, np.array([[0.0, -1.0, 0.0]], dtype=F32), c.nrm)
    emi = np.zeros(base.shape, dtype=F32)
    for (lx, lz) in M.LIGHTS:
        d = np.hypot(X - lx, Z - lz)
        ring = band(d, M.LIGHT_R - 1.6, M.LIGHT_R + 0.6, g)
        bulb = np.clip((M.LIGHT_R - 1.6 - d) / g + 0.5, 0, 1)
        base = lay(base, CHROME_D, ring)
        base = lay(base, CHROME, ring * band(d, M.LIGHT_R - 0.6, M.LIGHT_R + 0.6, g) * 0.8)
        base = lay(base, "#fff4d8", bulb)
        glow = np.clip((M.LIGHT_R + 12.0 - d) / 12.0, 0, 1) ** 2
        emi = emi + (bulb * 0.95 + glow * 0.20)[..., None] * col("#ffd590")[None, :]
    return base, emi


def m_partition(c):
    """The partition at the far end: the front seats' backs below the sill (gray leather, two humps with a seam
    between), the headliner's cloth above the opening, the frame round it (its own boxes)."""
    X, Y = c.X, c.Y
    gX, gY = c.gX * c.ss, c.gY * c.ss
    sill = M.DIVIDER["sill"]
    n = fbm(X / 20.0, Y / 20.0, 12, 3)
    seat = col(LEATHER_BACK) * (0.84 + 0.26 * n[..., None])
    for cx in (M.W * 0.28, M.W * 0.72):                                  # each front seat's back bulges a little: lit along its top
        hump = np.clip(1 - ((X - cx) / (M.W * 0.21)) ** 2, 0, 1)
        seat = seat * (0.9 + 0.14 * hump[..., None] * np.clip((Y - 20) / 60, 0, 1)[..., None])
    seat = seat * (1 - 0.45 * lines_aa(X, 1e6, 1.6, gX, phase=M.W / 2)[..., None])
    seat = seat * (1 - 0.22 * (lines_aa(Y, 10.0, 0.9, gY) * band(Y, 0, sill - 4, gY))[..., None])
    cloth = col(HEADLINER) * (0.82 + 0.2 * n[..., None])
    above = band(Y, sill, 1e5, gY)
    return lerp(seat, cloth, above[..., None])


def m_frame(c):
    """The frame round the divider's opening: black rubber with a chrome lip toward us."""
    base = col(TRIM) * (0.9 + 0.2 * fbm(c.X / 6, c.Y / 6, 14, 2)[..., None])
    if c.face == "front":
        g = np.maximum(c.gX, c.gY) * c.ss
        x0, x1, y0, y1, z0, z1 = c.box
        inner = np.minimum(np.minimum(c.X - x0, x1 - c.X), np.minimum(c.Y - y0, y1 - c.Y))
        base = lay(base, CHROME, band(inner, 0.4, 1.4, g) * 0.75)
    return base


def shell(st):
    """The carpet, the side walls with their window panes, the headliner, the partition at the far end."""
    W, H, L = M.W, M.H, M.L
    st.box(-60, W + 60, -10, 0, -60, L + 80, m_carpet, name="carpet", shadow=False)
    st.box(-60, W + 60, H, H + 10, -60, L + 80, m_headliner, name="headliner", shadow=False)
    y0, y1 = M.WINDOW_Y
    for side, (xa, xb) in (("L", (-10.0, 0.0)), ("R", (W, W + 10.0))):
        mat, nm = m_wall(side), "wall-" + side.lower()
        # the wall in pieces round the panes (each throws a shadow), so the daylight comes in through the glass only
        st.box(xa, xb, -10, y0, -10, L + 80, mat, name=nm)
        st.box(xa, xb, y1, H + 10, -10, L + 80, mat, name=nm)
        zs = [-10.0] + [z for pane in M.PANES[side] for z in pane] + [L + 80]
        for z0, z1 in zip(zs[0::2], zs[1::2]):
            st.box(xa, xb, y0, y1, z0, z1, mat, name=nm)
        for i, (z0, z1) in enumerate(M.PANES[side]):
            gx = (xa + xb) / 2
            st.box(gx - 0.5, gx + 0.5, y0, y1, z0, z1, m_pane, name=f"pane-{side.lower()}{i}", shadow=False, flag=4)
    # the partition, in pieces round the opening; the frame proud of it toward us
    x0, x1 = M.DIVIDER["x"]
    sill, top, fr = M.DIVIDER["sill"], M.DIVIDER["top"], M.DIVIDER["frame"]
    for b in ((-10, W + 10, -10, sill), (-10, W + 10, top, H + 10), (-10, x0, sill, top), (x1, W + 10, sill, top)):
        st.box(b[0], b[1], b[2], b[3], -10, 0, m_partition, name="partition")
    for b in ((x0 - fr, x1 + fr, sill - fr, sill), (x0 - fr, x1 + fr, top, top + fr), (x0 - fr, x0, sill, top), (x1, x1 + fr, sill, top)):
        st.box(b[0], b[1], b[2], b[3], -2.0, 1.5, m_frame, name="frame")


# ---------------------------------------------------------------- the divider's two states: a flat picture each, in cm
def _front_view(w_cm, h_cm, k=4):
    """What is seen through the open divider: the front compartment. The backs of two heads, an earpiece's curl at
    each, the rear-view mirror with two pairs of black sunglasses in it, the windshield, the road running ahead. One of
    the two is eating a doughnut. -> an RGB array, k px to a cm, V up. Comic, never menacing: round heads, neat hair."""
    Wp, Hp = int(w_cm * k), int(h_cm * k)
    im = Image.new("RGB", (Wp, Hp), (120, 150, 190))
    d = ImageDraw.Draw(im)
    cm = lambda x, y: (x * k, (h_cm - y) * k)                              # (x right, y up) in cm -> pixel
    hy = 50.0                                                            # the horizon through the windshield, cm up the opening
    for i in range(24):                                                  # the sky: deeper blue up high, pale at the horizon
        t = i / 23
        y0, y1 = h_cm - (h_cm - hy) * (i / 24), h_cm - (h_cm - hy) * ((i + 1) / 24)
        d.rectangle([cm(0, y0), cm(w_cm, y1)], fill=(int(70 + 150 * t), int(118 + 104 * t), int(196 + 34 * t)))
    for (mx, mw, mh, c) in ((w_cm * 0.08, 40, 8, (150, 128, 172)), (w_cm * 0.33, 26, 5, (164, 140, 178)), (w_cm * 0.66, 46, 9, (146, 122, 168)), (w_cm * 0.93, 30, 6, (160, 136, 176))):
        d.polygon([cm(mx - mw / 2, hy), cm(mx - mw / 2 + 6, hy + mh), cm(mx + mw / 2 - 6, hy + mh), cm(mx + mw / 2, hy)], fill=c)
    d.rectangle([cm(0, hy), cm(w_cm, 0)], fill=(222, 186, 138))          # the desert floor
    for i in range(10):                                                  # paler bands toward the horizon
        t = i / 9
        y = hy * (0.55 + 0.45 * t)
        d.rectangle([cm(0, y), cm(w_cm, y - 2)], fill=(int(226 + 14 * t), int(192 + 22 * t), int(146 + 28 * t)))
    d.polygon([cm(w_cm / 2 - 70, 0), cm(w_cm / 2 + 70, 0), cm(w_cm / 2 + 3, hy), cm(w_cm / 2 - 3, hy)], fill=(102, 98, 118))
    for i in range(5):                                                   # the dashes down its middle, smaller toward the horizon
        a, b = i / 5, (i + 0.45) / 5
        ya, yb = hy * (1 - (1 - a) ** 2), hy * (1 - (1 - b) ** 2)
        wa, wb = 2.2 * (1 - ya / hy) + 0.3, 2.2 * (1 - yb / hy) + 0.3
        d.polygon([cm(w_cm / 2 - wa, ya), cm(w_cm / 2 + wa, ya), cm(w_cm / 2 + wb, yb), cm(w_cm / 2 - wb, yb)], fill=(240, 210, 96))
    d.rectangle([cm(0, h_cm), cm(w_cm, h_cm - 4)], fill=(36, 36, 44))    # the roof's edge at the top of the windshield
    d.rectangle([cm(0, 26), cm(w_cm, 0)], fill=(40, 38, 46))             # the dashboard
    d.rectangle([cm(0, 28), cm(w_cm, 26)], fill=(74, 72, 84))
    # the rear-view mirror, hung from the roof: two pairs of black sunglasses looking back at us
    mx, my, mw, mh = w_cm * 0.5, h_cm - 17, 52, 13
    d.line([cm(mx, my + mh / 2), cm(mx, h_cm)], fill=(30, 30, 36), width=int(1.8 * k))
    d.rounded_rectangle([cm(mx - mw / 2 - 1.5, my + mh / 2 + 1.5), cm(mx + mw / 2 + 1.5, my - mh / 2 - 1.5)], radius=int(3 * k), fill=(30, 30, 36))
    d.rounded_rectangle([cm(mx - mw / 2, my + mh / 2), cm(mx + mw / 2, my - mh / 2)], radius=int(2.5 * k), fill=(196, 206, 216))
    for fx in (mx - 13, mx + 13):                                        # a face each in the glass, and its glasses: big and black
        d.ellipse([cm(fx - 8, my + 6.0), cm(fx + 8, my - 7.5)], fill=(226, 194, 168))
        d.chord([cm(fx - 8, my + 7.5), cm(fx + 8, my - 4)], 180, 360, fill=(70, 52, 42))
        for gx in (fx - 3.4, fx + 3.4):
            d.ellipse([cm(gx - 3.1, my + 2.4), cm(gx + 3.1, my - 1.8)], fill=(14, 14, 18))
        d.line([cm(fx - 6.5, my + 1.4), cm(fx + 6.5, my + 1.4)], fill=(14, 14, 18), width=max(1, int(0.7 * k)))
        d.line([cm(fx - 2.0, my - 4.6), cm(fx + 2.0, my - 4.6)], fill=(150, 90, 80), width=max(1, int(0.6 * k)))    # a straight, earnest mouth
    # the two heads from behind, over the tops of the front seats: neat dark hair, gray collars, an earpiece's curl
    for hx, big, hair in ((w_cm * 0.27, 1.0, (60, 44, 36)), (w_cm * 0.73, 1.07, (84, 62, 44))):
        r = 15 * big
        d.rounded_rectangle([cm(hx - 30, 40), cm(hx + 30, 22)], radius=int(5 * k), fill=(150, 152, 162))    # the seat's headrest... below, his shoulders
        d.rectangle([cm(hx - 27, 34), cm(hx + 27, 20)], fill=(122, 122, 134))                              # gray shoulders
        d.rectangle([cm(hx - 7, 36), cm(hx + 7, 31)], fill=(236, 236, 240))                                 # a white collar
        d.rectangle([cm(hx - 6, 44), cm(hx + 6, 35)], fill=(226, 194, 168))                                 # the neck
        d.ellipse([cm(hx - r, 42 + 2 * r), cm(hx + r, 40)], fill=(226, 194, 168))                           # the head
        d.ellipse([cm(hx - r, 42 + 2 * r), cm(hx + r, 40 + r * 0.7)], fill=hair)                            # the back of the head is hair
        for ex in (hx - r, hx + r):                                                                        # ears
            d.ellipse([cm(ex - 2.6, 40 + r * 1.25), cm(ex + 2.6, 40 + r * 0.55)], fill=(214, 176, 150))
        ex = hx + r * (1 if hx > w_cm / 2 else -1)                                                          # the earpiece: a clear curl and its wire
        d.arc([cm(ex - 3.6, 40 + r * 1.5), cm(ex + 3.6, 40 + r * 0.7)], 0, 360, fill=(236, 240, 246), width=max(1, int(0.8 * k)))
        d.line([cm(ex, 40 + r * 0.7), cm(ex + (2 if hx > w_cm / 2 else -2), 31)], fill=(236, 240, 246), width=max(1, int(0.6 * k)))
        d.line([cm(hx - r * 0.7, 40 + r * 1.62), cm(hx - r * 0.1, 40 + r * 1.8)], fill=tuple(min(255, v + 30) for v in hair), width=max(1, int(0.8 * k)))   # a combed line
    # the one on the right is eating: a doughnut held up beside his head, a bite out of it
    hx = w_cm * 0.73
    d.ellipse([cm(hx + 20, 58), cm(hx + 34, 44)], fill=(214, 150, 92))
    d.ellipse([cm(hx + 25, 54), cm(hx + 29, 49)], fill=(196, 206, 216))
    d.arc([cm(hx + 20, 58), cm(hx + 34, 44)], 200, 340, fill=(240, 130, 160), width=int(1.6 * k))
    d.ellipse([cm(hx + 30, 59), cm(hx + 37, 53)], fill=(196, 206, 216))                                   # the bite
    d.ellipse([cm(hx + 17, 50), cm(hx + 25, 42)], fill=(226, 194, 168))                                   # his hand
    d.rectangle([cm(hx + 15, 43), cm(hx + 25, 28)], fill=(122, 122, 134))                                 # his sleeve
    return np.asarray(im, F32) / 255.0


def _glass_view(w_cm, h_cm, k=4):
    """The smoked glass up: dark, the front seats' headrests dimly through it, and one broad sheen across it where the
    light from our windows is reflected, as a dark glass shows it."""
    Wp, Hp = int(w_cm * k), int(h_cm * k)
    im = Image.new("RGB", (Wp, Hp), tuple(int(v * 255) for v in col(GLASS)))
    d = ImageDraw.Draw(im)
    cm = lambda x, y: (x * k, (h_cm - y) * k)
    for hx in (w_cm * 0.27, w_cm * 0.73):                                 # the headrests and shoulders, dim
        d.rounded_rectangle([cm(hx - 16, 44), cm(hx + 16, 16)], radius=int(7 * k), fill=(40, 44, 54))
        d.rounded_rectangle([cm(hx - 30, 14), cm(hx + 30, -4)], radius=int(5 * k), fill=(38, 42, 52))
    a = np.asarray(im, F32) / 255.0
    a = blur(a, 2.2 * k)
    yy = np.linspace(1, 0, Hp, dtype=F32)[:, None, None]
    xx = np.linspace(0, 1, Wp, dtype=F32)[None, :, None]
    a = a * (0.80 + 0.30 * yy)                                           # a little lighter up high: the headliner in it
    for c0, wd, amt in ((0.16, 0.10, 0.16), (0.30, 0.04, 0.10), (0.78, 0.07, 0.06)):     # sheen: two streaks on the left, one faint on the right
        u = (xx - c0) + (yy - 0.5) * 0.35
        a = a + np.clip(1 - np.abs(u) / wd, 0, 1) ** 1.6 * amt
    return np.clip(a, 0, 1)


_VIEWS = {}


def divider_picture(which, k=4):
    key = (which, k)
    if key not in _VIEWS:
        x0, x1 = M.DIVIDER["x"]
        w, h = x1 - x0, M.DIVIDER["top"] - M.DIVIDER["sill"]
        _VIEWS[key] = (_front_view if which == "down" else _glass_view)(w, h, k)
    return _VIEWS[key]


def m_divider_picture(which, k=4):
    pic = divider_picture(which, k)
    h = pic.shape[0]

    def f(c):
        px, py = c.U * k, h - 1 - c.V * k                                # U: cm along the sill, V: cm up
        return sample(pic, np.clip(px, 0, pic.shape[1] - 1.001), np.clip(py, 0, h - 1.001))
    return f


def divider(st, down=False):
    """The smoked glass in its frame (up), or the opening with the front compartment seen through it and the glass's
    top edge peeking out of the seat back at the sill (down). Both are flat colour (glass)."""
    x0, x1 = M.DIVIDER["x"]
    sill, top = M.DIVIDER["sill"], M.DIVIDER["top"]
    if down:
        pts = [P3(x0, sill, -8.0), P3(x1, sill, -8.0), P3(x1, top, -8.0), P3(x0, top, -8.0)]
        st.poly(pts, m_divider_picture("down"), name="divider-down", grp="glass", flag=4)
        st.box(x0, x1, sill, sill + 2.2, -4.0, -2.0, "#9aa6b4", name="glass-edge", grp="glass", shadow=False, flag=4)
    else:
        pts = [P3(x0, sill, -3.0), P3(x1, sill, -3.0), P3(x1, top, -3.0), P3(x0, top, -3.0)]
        st.poly(pts, m_divider_picture("up"), name="divider-up", grp="glass", flag=4)


# ---------------------------------------------------------------- the seats
def rolls(c, al, pl, axis, depth=0.85):
    """Padded rolls every `pl` cm along the measurement `al` (pleats): sets the surface's own normal on each roll, so the
    light models it, and -> (cavity shade, groove coverage). `axis` is the room direction `al` runs in."""
    f = al / pl - np.floor(al / pl)
    sv = 2 * f - 1
    th = np.arcsin(np.clip(sv, -0.97, 0.97)) * depth
    n0 = np.asarray(c.n, dtype=F32)[None, :]
    ax = np.asarray(axis, dtype=F32)[None, :]
    nrm = n0 * np.cos(th)[:, None] + ax * np.sin(th)[:, None]
    c.nrm = (nrm / np.linalg.norm(nrm, axis=1, keepdims=True)).astype(F32)
    cavity = 0.70 + 0.30 * np.sqrt(np.clip(1 - sv * sv, 0, 1))
    return cavity.astype(F32), f


def m_cushion(along, seed=3, color=LEATHER):
    """A leather cushion: padded rolls every 13 cm along `along` ("z" for a seat along the car, "x" across it), a
    deep crease where it meets its backrest, a piping roll along its front edge, a dark kick strip at its foot."""
    def f(c):
        X, Y, Z = c.X, c.Y, c.Z
        al = Z if along == "z" else X
        g_al = (c.gZ if along == "z" else c.gX) * c.ss
        axis = (0.0, 0.0, 1.0) if along == "z" else (1.0, 0.0, 0.0)
        n = fbm(X / 14.0, Z / 14.0, seed, 3) * 0.5 + fbm(X / 3.0, Z / 3.0, seed + 1, 2) * 0.5
        base = col(color) * (0.92 + 0.14 * n[..., None])
        x0, x1, y0, y1, z0, z1 = c.box
        if c.face == "top":
            cav, fr = rolls(c, al, 13.0, axis)
            base = base * cav[..., None]
            base = lay(base, LEATHER_D, lines_aa(al, 13.0, 1.0, g_al) * 0.42)
            base = lay(base, mixc(color, "#ffffff", 0.45), (np.clip(1 - np.abs(fr - 0.60) / 0.14, 0, 1) * 0.45))     # the sheen on each roll's crest
            if along == "z":
                left = x0 < M.W / 2
                crease = np.abs(X - (M.BACK_T if left else M.W - M.BACK_T))
                edge = np.abs(X - (x1 if left else x0))
                ge = (c.gX) * c.ss
            else:
                crease = np.full(X.shape, 1e5, dtype=F32)
                edge = np.abs(Z - z0)
                ge = c.gZ * c.ss
            base = lay(base, "#24222a", band(crease, 0.0, 2.2, ge) * 0.85)
            base = lay(base, mixc(color, "#ffffff", 0.32), band(edge, 0.6, 2.8, ge) * 0.85)
            base = lay(base, LEATHER_D, band(edge, 2.8, 3.8, ge) * 0.6)
        else:
            if c.face in ("left", "right", "front", "back"):
                cav, fr = rolls(c, al, 13.0, axis, depth=0.5) if (along == "z" and c.face in ("left", "right")) or (along == "x" and c.face in ("front", "back")) else (np.ones(X.shape, F32), None)
                base = base * cav[..., None]
            up = np.clip((Y - y0) / max(y1 - y0, 1), 0, 1)
            base = base * (0.80 + 0.16 * up[..., None])
            gY = c.gY * c.ss
            base = lay(base, mixc(color, "#ffffff", 0.24), band(Y, y1 - 3.2, y1 - 0.3, gY) * 0.85)     # the piping, seen from the side
            base = lay(base, LEATHER_D, band(Y, y1 - 4.4, y1 - 3.2, gY) * 0.7)
            base = lay(base, "#24222a", band(Y, y0, y0 + 3.4, gY) * 0.75)                              # the kick strip at its foot
            if c.face in ("left", "right") and along == "z":
                base = lay(base, LEATHER_D, (lines_aa(Z, 13.0, 1.0, c.gZ * c.ss) * band(Y, y0 + 3.4, y1 - 4.4, gY)) * 0.5)
        return base
    return f


def m_backrest(seed=4, color=LEATHER_BACK):
    """A backrest: upright padded rolls every 13 cm along the car, a fat roll along its top."""
    def f(c):
        X, Y, Z = c.X, c.Y, c.Z
        gZ, gY = c.gZ * c.ss, c.gY * c.ss
        n = fbm(Z / 14.0, Y / 14.0, seed, 3) * 0.5 + fbm(Z / 3.0, Y / 3.0, seed + 1, 2) * 0.5
        base = col(color) * (0.92 + 0.14 * n[..., None])
        x0, x1, y0, y1, z0, z1 = c.box
        if c.face in ("left", "right"):
            top_roll = band(Y, y1 - 7.0, y1 + 1.0, gY)
            cav, fr = rolls(c, Z, 13.0, (0.0, 0.0, 1.0))
            base = base * (cav * (1 - top_roll) + top_roll)[..., None]
            base = lay(base, LEATHER_D, lines_aa(Z, 13.0, 1.0, gZ) * 0.40 * band(Y, y0, y1 - 7.0, gY))
            base = lay(base, LEATHER_D, band(Y, y1 - 7.6, y1 - 6.2, gY) * 0.75)
            base = lay(base, mixc(color, "#ffffff", 0.28), band(Y, y1 - 5.6, y1 - 1.0, gY) * 0.75)
            base = lay(base, mixc(color, "#ffffff", 0.40), (np.clip(1 - np.abs(fr - 0.6) / 0.14, 0, 1) * 0.40 * band(Y, y0 + 4, y1 - 8, gY)))
            # the top roll bends its light: it faces up as much as out
            nrm = np.asarray(c.nrm, dtype=F32)
            k = top_roll[:, None]
            up = np.array([[0.0, 1.0, 0.0]], dtype=F32)
            c.nrm = nrm * (1 - k * 0.55) + up * (k * 0.55)
        elif c.face == "top":
            base = base * 1.06
        else:
            base = base * 0.86
        return base
    return f


def seats(st):
    x0, x1, y0, y1, z0, z1 = M.LONG_SEAT
    st.box(x0, x1, y0, y1, z0, z1, m_cushion("z", 3), name="seat", foot=True)
    st.box(0.0, M.BACK_T, y1, M.BACK_H, z0, z1, m_backrest(4), name="seat-back")
    x0, x1, y0, y1, z0, z1 = M.FACING_SEAT
    st.box(x0, x1, y0, y1, z0, z1, m_cushion("z", 5), name="facingseat", foot=True)
    st.box(M.W - M.BACK_T, M.W, y1, M.BACK_H, z0, z1, m_backrest(6), name="facing-back")


def m_ourseat(c):
    """The seat we sit on, seen from just above and behind its front: a fat padded bolster along its front edge (its
    crest catching the light, sewn in segments), and on our side of it the cushion, its pleats running toward us,
    falling away into our own shadow."""
    X, Y, Z = c.X, c.Y, c.Z
    x0, x1, y0, y1, z0, z1 = c.box
    n = fbm(X / 14.0, Z / 14.0, 7, 3) * 0.5 + fbm(X / 3.0, Z / 3.0, 8, 2) * 0.5
    base = col(LEATHER) * (0.92 + 0.12 * n[..., None])
    if c.face == "top":
        gZ, gX = c.gZ * c.ss, c.gX * c.ss
        bol = 18.0                                                       # the bolster: the first 18 cm from the front edge
        u = np.clip((Z - z0) / bol, 0, 1)
        th = (u - 0.45) * 2.0                                            # its roll: facing forward and up at the front, toward us and up behind
        bolster = (Z - z0) < bol
        cav, fr = rolls(c, X, 15.0, (1.0, 0.0, 0.0), depth=0.6)         # the cushion's pleats, toward us
        nrm_c = np.asarray(c.nrm, dtype=F32)
        nrm_b = np.stack([np.zeros_like(th), np.cos(th), np.sin(th)], axis=1).astype(F32)
        seg = (X / 24.0) - np.floor(X / 24.0)                            # the bolster's segments: each puffs a little across
        nrm_b[:, 0] = (seg - 0.5) * 0.5
        c.nrm = np.where(bolster[:, None], nrm_b, nrm_c)
        c.nrm = c.nrm / np.linalg.norm(c.nrm, axis=1, keepdims=True)
        behind = np.clip((Z - z0 - bol) / 46.0, 0, 1)
        base = base * np.where(bolster, 1.0, cav * (1.0 - 0.50 * behind))[..., None]
        base = lay(base, LEATHER_D, (lines_aa(X, 24.0, 1.0, gX) * bolster) * 0.45)                    # the bolster's seams
        base = lay(base, LEATHER_D, band(Z, z0 + bol - 1.2, z0 + bol + 0.8, gZ) * 0.85)               # the seam behind the bolster
        base = lay(base, LEATHER_D, (lines_aa(X, 15.0, 1.0, gX) * np.clip((Z - z0 - bol) / 4.0, 0, 1)) * 0.30)
        base = lay(base, mixc(LEATHER, "#ffffff", 0.35), (np.clip(1 - np.abs(u - 0.40) / 0.16, 0, 1) * bolster) * 0.5)   # the crest's sheen
    return base


def m_rolled_arm(seed):
    """A rolled arm, as on a good sofa: the roll's leather sewn in pleats along it, catching the light along its
    crown; its round end toward us with a seam round it and a button in the middle."""
    def f(c):
        n = fbm(c.X / 8.0, c.Z / 8.0, seed, 3)
        base = col(LEATHER_BACK) * (0.9 + 0.14 * n[..., None])
        if c.face == "round":
            wall = c.kind <= 2
            pl = np.mod(c.ang / 0.42, 1.0)
            base = base * np.where(wall, 0.80 + 0.20 * np.sqrt(np.clip(1 - (2 * pl - 1) ** 2, 0, 1)), 0.86)[..., None]
            seam = np.clip(1 - np.abs(pl - 0.5) * 2 / 0.12, 0, 1) * wall * 0
            seam = (np.abs(pl - 0.0) < 0.06) | (np.abs(pl - 1.0) < 0.06)
            base = lay(base, LEATHER_D, (seam & wall) * 0.5)
            cap = c.kind >= 3
            ring = (np.abs(c.rad - 9.5) < 0.9) & cap
            base = lay(base, LEATHER_D, ring * 0.7)
            base = lay(base, "#3c383e", ((c.rad < 1.6) & cap) * 0.9)
        return base
    return f


def front(st):
    """The seat we sit on (its bolster and cushion) and the rolled arms where it meets the side seats: the
    foreground, on the front plane."""
    x0, x1, y0, y1, z0, z1 = M.BACK_SEAT
    st.box(x0, x1, y0, y1, z0, z1, m_ourseat, name="backseat", grp="front", shadow=False)
    for name, (ax0, ax1, ay0, ay1, az0, az1) in (("armrest-l", M.ARMREST_L), ("armrest-r", M.ARMREST_R)):
        cx = (ax0 + ax1) / 2
        r = (ax1 - ax0) / 2 - 2.0
        st.box(cx - r + 1.0, cx + r - 1.0, ay0, ay1 - r * 0.6, az0, az1, m_armrest(8 if name.endswith("l") else 9), name=name, grp="front", shadow=False)
        st.cyl((cx, ay1 - r * 0.6), r, az0, az1, m_rolled_arm(8 if name.endswith("l") else 9), axis="z", name=name, grp="front", shadow=False)


def m_armrest(seed):
    """A padded armrest: its top rounded across and sewn in pleats along it, a seam round it, a chrome cap at its far end."""
    def f(c):
        X, Y, Z = c.X, c.Y, c.Z
        x0, x1, y0, y1, z0, z1 = c.box
        n = fbm(X / 10.0, Z / 10.0, seed, 3)
        base = col(LEATHER_BACK) * (0.9 + 0.14 * n[..., None])
        if c.face == "top":
            u = np.clip((X - x0) / max(x1 - x0, 1), 0, 1)
            th = (u - 0.5) * 1.8
            pl = (Z / 9.0) - np.floor(Z / 9.0)
            c.nrm = np.stack([np.sin(th), np.cos(th), (pl - 0.5) * 0.6], axis=1).astype(F32)
            c.nrm = c.nrm / np.linalg.norm(c.nrm, axis=1, keepdims=True)
            gX, gZ = c.gX * c.ss, c.gZ * c.ss
            base = base * (0.78 + 0.22 * np.sqrt(np.clip(1 - (2 * pl - 1) ** 2, 0, 1)))[..., None]
            base = lay(base, LEATHER_D, (band(X, x0, x0 + 2.0, gX) + band(X, x1 - 2.0, x1, gX)).clip(0, 1) * 0.6)
            base = lay(base, mixc(LEATHER_BACK, "#ffffff", 0.35), (np.clip(1 - np.abs(u - 0.38) / 0.12, 0, 1)) * 0.35)
        else:
            gY = c.gY * c.ss
            base = base * 0.82
            base = lay(base, mixc(LEATHER_BACK, "#ffffff", 0.22), band(Y, y1 - 3.0, y1 - 0.5, gY) * 0.75)
            if c.face == "back":
                base = lay(base, CHROME, band(Y, y0 + 5, y1 - 6, gY) * 0.55)
        return base
    return f


# ---------------------------------------------------------------- the bar at the far end, the phone, the ashtray
def m_bar(c):
    X, Y, Z = c.X, c.Y, c.Z
    x0, x1, y0, y1, z0, z1 = c.box
    if c.face == "top":
        gr = fbm(X / 40.0, Z / 2.5, 31, 3)
        base = lerp(col(BAR_WOOD), col(BAR_WOOD_L), (0.3 + 0.5 * gr)[..., None])
        base = base * (0.9 + 0.2 * fbm(X / 6.0, Z / 6.0, 32, 2)[..., None])
        gX, gZ = c.gX * c.ss, c.gZ * c.ss
        edge = 1 - band(X, x0 + 2.2, x1 - 2.2, gX) * band(Z, z0 + 2.2, z1 - 2.2, gZ)
        return lay(base, CHROME, edge * 0.85)
    gY, gX = c.gY * c.ss, c.gX * c.ss
    n = fbm(X / 10.0, Y / 10.0, 33, 2)
    base = col("#24202a") * (0.9 + 0.2 * n[..., None])
    base = lay(base, CHROME, band(Y, y1 - 2.4, y1 - 1.0, gY) * 0.8)                    # the chrome lip
    base = lay(base, "#18161c", band(Y, y0 + 7.0, y0 + 8.2, gY) * 0.6)                 # a kick line
    base = lay(base, "#18161c", lines_aa(X, 1e6, 1.0, gX, phase=(x0 + x1) / 2) * 0.7)  # two cupboard doors
    for hx in ((x0 + x1) / 2 - 6, (x0 + x1) / 2 + 6):                                  # and their chrome pulls
        base = lay(base, CHROME, rect(X, Y, hx - 0.6, hx + 0.6, y1 - 22, y1 - 12, np.maximum(gX, gY)) * 0.8)
    return base


def phone(st):
    """A car phone of the old kind: a black cradle on the bar with a row of pale keys on its front, a cream handset
    lying across it (its two round ends plain to see), a coiled black cord down the bar's front into a little box."""
    px, py, pz = M.PHONE["at"]
    w, h, d = M.PHONE["cradle"]
    cream = plain(CREAM, 0.08, 6.0, 41)
    st.box(px - w / 2, px + w / 2, py, py + h, pz - d / 2, pz + d / 2, plain("#2a2830", 0.08, 6.0, 42), name="phone")
    st.poly([P3(px - 10, py + 1.4, pz + d / 2 + 0.05), P3(px + 10, py + 1.4, pz + d / 2 + 0.05), P3(px + 10, py + 5.6, pz + d / 2 + 0.05), P3(px - 10, py + 5.6, pz + d / 2 + 0.05)],
            lambda c: lay(col("#2a2830"), "#e8e2d0", rect(np.mod(c.U, 3.3), np.mod(c.V, 2.1), 0.5, 2.7, 0.4, 1.7, c.gU * c.ss) * 0.95), name="phone", bias=0.3)
    hy = py + h + 2.8                                                   # the handset: a grip with a round cup at each end
    st.cyl((hy, pz), 2.0, px - w / 2 + 2.0, px + w / 2 - 2.0, cream, axis="x", name="phone")
    for ex in (px - w / 2 + 0.5, px + w / 2 - 0.5):
        st.ball((ex, hy + 0.6, pz), 4.2, cream, name="phone")
    bx0, bx1, by0, by1, bz0, bz1 = M.BAR
    pts, n = [], 28                                                     # the coiled cord, down the front of the bar
    for i in range(n + 1):
        t = i / n
        pts.append(P3(px + w / 2 + 3 + 2.6 * math.sin(t * math.pi * 9), hy - 2 - (hy - 2 - 20) * t, bz1 + 2.0 + 2.2 * math.cos(t * math.pi * 9)))
    st.rope(pts, 0.9, "#26242a", name="phone")
    st.box(px + w / 2 - 1, px + w / 2 + 7, 15, 21, bz1 - 0.5, bz1 + 1.5, "#26242a", name="phone", shadow=False)


def m_glass_tray(c):
    """Cut glass: pale, cool, with bright facets."""
    n = fbm(c.X / 2.0, (c.Y + c.Z) / 2.0, 44, 2)
    base = col("#bcc8d0") * (0.75 + 0.5 * n[..., None])
    if c.face == "round":
        facet = sstep(0.5, 0.62, fbm(c.ang * 3.0, c.along / 2.0, 45, 1))
        base = lay(base, "#f6fafc", facet * 0.85)
    return base, col("#bcc8d0") * 0.10


def ashtray(st):
    ax, ay, az = M.ASHTRAY["at"]
    r, h = M.ASHTRAY["r"], M.ASHTRAY["h"]
    st.cyl((ax, az), r, ay, ay + h, m_glass_tray, name="ashtray", hollow=True)
    st.cyl((ax, az), r - 1.6, ay, ay + 1.2, "#a8b4bc", name="ashtray", shadow=False)
    rng = np.random.default_rng(7)
    beans = ["#e0362c", "#f4a41e", "#5ab84a", "#f8e43a", "#8048b8", "#f46eaa", "#faf6e4", "#2f90dc"]
    for i in range(46):                                                  # heaped high in the middle: it is FULL
        a = rng.uniform(0, 2 * math.pi)
        rr = (r - 2.4) * math.sqrt(rng.uniform(0, 1))
        bx, bz = ax + math.cos(a) * rr, az + math.sin(a) * rr
        by = ay + 2.6 + rng.uniform(0, 1.4) + 5.0 * (1 - (rr / r) ** 2)
        st.ball((bx, by, bz), 2.0, lambda c, k=beans[i % len(beans)]: col(k), name="ashtray", shadow=False, flag=2)


def bar(st):
    x0, x1, y0, y1, z0, z1 = M.BAR
    st.box(x0, x1, y0, y1, z0, z1, m_bar, name="bar", foot=True)
    phone(st)
    ashtray(st)


# ---------------------------------------------------------------- the fridge in the facing seat's base, at its near end
def m_fridge(c):
    X, Y, Z = c.X, c.Y, c.Z
    n = fbm(Y / 12.0, Z / 12.0, 51, 2)
    base = col("#c2c5cc") * (0.9 + 0.16 * n[..., None])
    x0, x1, y0, y1, z0, z1 = c.box
    if c.face == "left":                                                 # the door, toward the carpet
        gY, gZ = c.gY * c.ss, c.gZ * c.ss
        g = np.maximum(gY, gZ)
        inner = band(Y, y0 + 2.5, y1 - 2.5, gY) * band(Z, z0 + 2.5, z1 - 2.5, gZ)
        base = lay(base, "#5a5c64", (1 - inner) * 0.75)                  # the gap round the door
        base = base * (1 + 0.06 * inner[..., None])
        base = lay(base, "#eae6dc", rect(Z, Y, z1 - 30, z1 - 12, y1 - 11, y1 - 7.5, g) * 0.9)     # a small plate, nothing on it to read
        base = lay(base, "#54565e", (rect(Z, Y, z0 + 9, z1 - 9, y0 + 4, y0 + 8.5, g) * lines_aa(Y, 1.3, 0.55, gY)) * 0.9)   # the vent
        base = lay(base, "#8ad0ff", disc(Z, Y, z0 + 8, y1 - 9, 1.0, g) * 0.9)                    # its little light: on
    else:
        base = base * 0.86
    return base


def fridge(st):
    x0, x1, y0, y1, z0, z1 = M.FRIDGE
    st.box(x0, x1, y0, y1, z0, z1, m_fridge, name="fridge", foot=True)
    hz = z1 - 5.0                                                        # the handle, upright near its near edge
    st.stick(P3(x0 - 1.6, y0 + 9, hz), P3(x0 - 1.6, y1 - 8, hz), 0.9, CHROME, name="fridge")
    for yy in (y0 + 9, y1 - 8):
        st.stick(P3(x0 - 1.6, yy, hz), P3(x0 + 0.2, yy, hz), 0.6, CHROME_D, name="fridge")


# ---------------------------------------------------------------- what lies on the facing seat
def m_paper(c):
    """Brown kraft paper: crinkled (darker creases running mostly up and down, as a bag that has been carried), a grease
    spot low on the side toward us, nothing written on it."""
    X, Y, Z = c.X, c.Y, c.Z
    x0, x1, y0, y1, z0, z1 = getattr(c, "box", (0, 0, 0, 0, 0, 0))     # (the rolled top is round: it has no box)
    u = X + Z                                                            # across whichever face it is
    n = fbm(u / 2.2, Y / 3.0, 61, 3)
    crinkle = np.abs(fbm(u / 1.6, Y / 9.0, 62, 2) - 0.5)
    base = col(PAPER) * (0.88 + 0.24 * n[..., None])
    base = base * (1 - 0.30 * (1 - sstep(0.0, 0.05, crinkle))[..., None])       # creases
    base = base * (1 + 0.12 * (sstep(0.05, 0.10, crinkle) * (1 - sstep(0.10, 0.16, crinkle)))[..., None])   # their lit edges
    if c.face == "front":                                                # the grease spot, low on the side toward us
        d = np.hypot((X - (x0 + 6.5)) / 5.0, (Y - (y0 + 8)) / 4.2) + 0.25 * fbm(X / 3, Y / 3, 63, 2)
        spot = np.clip(1.3 - d, 0, 1)
        base = lerp(base, base * col("#7c5a34") * 1.05, (spot * 0.8)[..., None])
    if c.face in ("left", "right"):                                      # the side gusset, folded in down its middle
        gZ = c.gZ * c.ss
        mid = (z0 + z1) / 2
        base = lay(base, "#6a482a", band(np.abs(Z - mid), 0.0, 0.7, gZ) * 0.75)
        base = base * (1 - 0.10 * np.clip((Z - mid) / max(z1 - mid, 1), 0, 1))[..., None]
    if c.face == "top":
        base = base * 1.06
    return base


def bag(st):
    bx, by, bz = M.BAG["at"]
    w, d, h = M.BAG["w"], M.BAG["d"], M.BAG["h"]
    g = dict(name="bag", grp="bag")
    st.box(bx - w / 2, bx + w / 2, by, by + h, bz - d / 2, bz + d / 2, m_paper, **g)
    # the top rolled over toward us, twice: a fat roll across the top, a little wider than the bag, and its lip
    st.cyl((by + h + 1.6, bz + d / 2 - 1.0), 2.4, bx - w / 2 - 0.4, bx + w / 2 + 0.4, m_paper, axis="x", **g)
    st.cyl((by + h - 0.6, bz + d / 2 + 1.0), 1.8, bx - w / 2 - 0.2, bx + w / 2 + 0.2, m_paper, axis="x", shadow=False, **g)


def m_juice(c):
    X, Y, Z = c.X, c.Y, c.Z
    base = col("#ecebb0") * (0.92 + 0.12 * fbm(X / 2, Y / 2, 71, 2)[..., None])
    x0, x1, y0, y1, z0, z1 = c.box
    g = np.maximum(c.gX, c.gY) * c.ss
    if c.face == "front":                                                # toward us: a plain apple and its leaf, no name
        cx, cy = (x0 + x1) / 2, y0 + 6.0
        base = lay(base, "#d63a2a", disc(X, Y, cx, cy, 3.0, g))
        base = lay(base, "#f87458", disc(X, Y, cx - 1.0, cy + 1.0, 1.0, g) * 0.85)
        base = lay(base, "#5a3a22", rect(X, Y, cx - 0.35, cx + 0.35, cy + 2.6, cy + 4.0, g))
        base = lay(base, "#3f9a3a", np.clip(1.2 - np.hypot((X - cx - 1.3) / 1.5, (Y - cy - 3.6) / 0.75), 0, 1) * 1.6)
        base = lay(base, "#3f9a3a", rect(X, Y, x0 + 0.4, x1 - 0.4, y0 + 0.8, y0 + 1.9, g) * 0.9)   # a green band at its foot
    elif c.face == "left":
        base = lay(base * 0.9, "#3f9a3a", rect(Z, Y, z0 + 0.4, z1 - 0.4, y0 + 0.8, y0 + 1.9, np.maximum(c.gZ, c.gY) * c.ss) * 0.9)
    elif c.face == "top":
        base = col("#dcd99e")
    return base


def juice(st):
    jx, jy, jz = M.JUICE["at"]
    w, d, h = M.JUICE["w"], M.JUICE["d"], M.JUICE["h"]
    g = dict(name="juice", grp="juice")
    st.box(jx - w / 2, jx + w / 2, jy, jy + h, jz - d / 2, jz + d / 2, m_juice, **g)
    st.stick(P3(jx + 2.0, jy + h - 0.5, jz - 0.8), P3(jx + 2.3, jy + h + 4.6, jz - 0.8), 0.42, "#f6f6f2", **g)      # the straw, bent at the top
    st.stick(P3(jx + 2.3, jy + h + 4.6, jz - 0.8), P3(jx + 4.2, jy + h + 7.0, jz - 1.4), 0.42, "#f6f6f2", **g)


DIGITS = {                                                               # pen numerals in a box 10 wide, 14 tall (y down)
    "1": [[(2, 4), (6, 0), (6, 14)]],
    "2": [[(1, 3), (4, 0), (8, 1), (9, 4), (7, 8), (1, 14), (9.5, 14)]],
    "4": [[(7, 14), (7, 0), (0, 10), (10, 10)]],
    "9": [[(9, 5), (6, 0.5), (2.5, 0.5), (0.5, 4), (2.5, 8), (6.5, 8), (9, 5), (8, 14)]],
}


def sheet_picture(k=10):
    """The sheet on the clipboard: the office's map of the desert in pen, three sectors circled, two of them numbered
    44 and 1921 (big pen numerals, readable at a glance), the third under a thumb-sized smudge; a column of empty boxes
    down the right; a note in the margin that is only a squiggle. -> RGB array, k px to a cm, V up."""
    w, h = M.CLIPBOARD["w"] - 2.4, M.CLIPBOARD["h"] - 4.0
    Wp, Hp = int(w * k), int(h * k)
    im = Image.new("RGB", (Wp, Hp), (244, 240, 228))
    d = ImageDraw.Draw(im)
    cm = lambda x, y: (x * k, (h - y) * k)
    ink = (30, 36, 72)
    pen = max(1, int(0.16 * k))
    for i in range(3):                                                   # a printed header nobody can read, and a rule
        d.line([cm(1.6 + i * 6.0, h - 1.6), cm(1.6 + i * 6.0 + 4.6, h - 1.6)], fill=(130, 130, 140), width=max(1, int(0.12 * k)))
    d.line([cm(1.2, h - 2.6), cm(w - 1.2, h - 2.6)], fill=(96, 96, 108), width=max(1, int(0.1 * k)))
    road = curve3([(1.5, h - 4.0), (5.0, h - 8.0), (7.6, h - 13.0), (6.6, h - 19.0), (10.0, h - 25.0), (12.0, h - 28.5)], 6)
    d.line([cm(x, y) for x, y, *_ in road], fill=ink, width=pen * 2)
    for (mx, my, mw) in ((4.2, h - 12.0, 2.0), (12.6, h - 5.6, 2.6)):    # two mesas: a flat line and hatching
        d.line([cm(mx - mw, my), cm(mx + mw, my)], fill=ink, width=pen)
        for j in range(5):
            x = mx - mw + j * (2 * mw / 4)
            d.line([cm(x, my), cm(x + 0.4, my - 1.0)], fill=ink, width=pen)
    d.line([cm(1.0, h - 17.0), cm(13.0, h - 15.6)], fill=ink, width=pen)                                 # the fence
    for j in range(7):
        x = 1.0 + j * 2.0
        d.line([cm(x, h - 17.0 + j * 0.23), cm(x, h - 16.0 + j * 0.23)], fill=ink, width=pen)
    # the three sectors, each circled in pen, two numbered beside their circles in big numerals
    circles = [(3.6, h - 21.0, 1.9, "44", (5.9, h - 18.8)), (10.4, h - 10.8, 2.1, "1921", (2.6, h - 6.4)), (8.6, h - 26.2, 1.8, None, None)]
    for (cx, cy, r, label, at) in circles:
        d.ellipse([cm(cx - r, cy + r), cm(cx + r, cy - r)], outline=ink, width=pen * 2)
        if label:
            dh, dw, gap = 3.6, 2.0, 0.55
            x, y = at
            for ch in label:
                for stroke_ in DIGITS[ch]:
                    pts = [cm(x + px * dw / 10.0, y - py * dh / 14.0) for px, py in stroke_]
                    d.line(pts, fill=ink, width=int(pen * 2.4), joint="curve")
                x += dw + gap
    sx, sy = 11.6, h - 26.6                                              # the thumb-sized smudge over the third sector's number
    for i in range(6):
        rr = 2.3 - i * 0.28
        d.ellipse([cm(sx - rr * 1.25, sy + rr), cm(sx + rr * 1.25, sy - rr)], fill=(156 + i * 9, 146 + i * 9, 128 + i * 9))
    bx = w - 4.0                                                         # the column of empty boxes, under a heading too small to read
    d.line([cm(bx - 0.4, h - 4.2), cm(bx + 3.2, h - 4.2)], fill=ink, width=pen)
    for i in range(8):
        y0 = h - 5.4 - i * 2.5
        d.rectangle([cm(bx, y0), cm(bx + 2.0, y0 - 1.8)], outline=ink, width=pen)
    mx, my = 1.2, 2.6                                                    # the margin note: a squiggle, and a hook that might be a question mark
    for row_, n in ((0.0, 7), (-1.4, 5)):
        sq = curve3([(mx + i * 1.4, my + row_ + (0.5 if i % 2 else -0.2)) for i in range(n)], 4)
        d.line([cm(x, y) for x, y, *_ in sq], fill=ink, width=pen)
    d.arc([cm(mx + 9.6, my + 1.0), cm(mx + 11.0, my - 0.4)], 200, 90, fill=ink, width=pen)
    return np.asarray(im, F32) / 255.0


_SHEET = {}


def m_sheet(k=10):
    if k not in _SHEET:
        _SHEET[k] = sheet_picture(k)
    pic = _SHEET[k]
    hp = pic.shape[0]

    def f(c):
        px, py = c.U * k, hp - 1 - c.V * k
        a = sample(pic, np.clip(px, 0, pic.shape[1] - 1.001), np.clip(py, 0, hp - 1.001))
        return a * (0.97 + 0.06 * fbm(c.U / 1.5, c.V / 1.5, 81, 2)[..., None])
    return f


def clipboard_frame():
    """The board's place: its bottom edge's middle on the cushion, turned to face us across the car (half way between
    facing the carpet and facing the back of the car), leaning back against the backrest. -> (origin, across, up, out)."""
    bx, by, bz = M.CLIPBOARD["at"]
    t = math.radians(M.CLIPBOARD["tilt"])
    nh = np.array([-math.sqrt(0.5), 0.0, math.sqrt(0.5)])                # its face, level: toward the carpet and toward us
    across = np.array([math.sqrt(0.5), 0.0, math.sqrt(0.5)])             # along its bottom edge, left to right as we see it
    up = np.array([-nh[0] * math.sin(t), math.cos(t), -nh[2] * math.sin(t)])
    out = np.cross(across, up)
    if np.dot(out, nh) < 0:
        out = -out
    return np.array([bx, by, bz]), across, up, out


def clipboard(st):
    o, a, u, n = clipboard_frame()
    w, h = M.CLIPBOARD["w"], M.CLIPBOARD["h"]
    g = dict(name="clipboard", grp="clipboard")

    def C(x, y, z=0.0):                                                  # x across, y up the board, z out of its face
        p = o + a * (x - w / 2) + u * y + n * z
        return P3(*p)
    th = 0.9
    st.poly([C(0, 0), C(w, 0), C(w, h), C(0, h)], plain("#7a5434", 0.14, 4.0, 91), **g)          # (no shadow box: a tilted board's box would shade its own face)
    st.poly([C(0, 0, -th), C(w, 0, -th), C(w, 0), C(0, 0)], "#4a3020", **g)                 # its bottom edge
    st.poly([C(w, 0, -th), C(w, h, -th), C(w, h), C(w, 0)], "#4a3020", **g)                 # its right edge
    st.poly([C(1.2, 1.2, 0.25), C(w - 1.2, 1.2, 0.25), C(w - 1.2, h - 2.8, 0.25), C(1.2, h - 2.8, 0.25)], m_sheet(), bias=0.3, **g)
    clip = [C(3.0, h - 5.0, 0.9), C(w - 3.0, h - 5.0, 0.9), C(w - 3.0, h - 0.6, 0.9), C(3.0, h - 0.6, 0.9)]
    st.poly(clip, lambda c: lay(col(CHROME), CHROME_D, band(c.V, 1.5, 2.5, c.gV * c.ss) * 0.8), bias=1.0, **g)
    st.poly([C(w / 2 - 4.5, h - 1.0, 1.1), C(w / 2 + 4.5, h - 1.0, 1.1), C(w / 2 + 4.5, h + 1.4, 2.4), C(w / 2 - 4.5, h + 1.4, 2.4)], CHROME_D, bias=1.2, **g)


# ---------------------------------------------------------------- Grandpa Joe's side: the ropes, the seatbelt
def m_rope(c):
    """White regulation rope with a red thread spiralling round it."""
    s = (c.X * 0.7 + c.Z * 0.7 + c.Y * 0.5) / 3.6 + c.side * 0.35
    thread = (np.mod(s, 1.0) < 0.2).astype(F32)
    base = col(ROPE) * (0.9 + 0.14 * fbm(c.X * 1.5 + c.Z * 1.5, c.Y, 101, 2)[..., None])
    return lay(base, ROPE_RED, thread * 0.95)


def rope_paths(strands=4):
    """The ropes as a list of (points, radius) lengths on the cushion: the knot, the bow's loops (slacker as strands
    go), `strands` lengths running from the knot to Joe, and the loose end toward us, longer each time."""
    rx, ry, rz = M.ROPES["at"]
    r = 2.3
    y = ry + r * 0.8
    gone = 4 - strands
    out = []
    out.append(([P3(rx - 2.8, y + 0.6, rz - 2.4), P3(rx + 2.8, y + 1.0, rz + 2.0)], r * 1.45))          # the knot
    loops = 1.0 - gone * 0.22                                            # the bow's loops: two, then one, as it comes undone
    for sgn in ((-1, 1) if strands >= 2 else (1,)):
        pts, n = [], 18
        for i in range(n + 1):
            a = math.pi * i / n
            pts.append(P3(rx + sgn * (2.6 + 12.5 * loops * math.sin(a)), y + 0.8 * math.sin(a) ** 2,
                          rz - sgn * (0.8 - 5.6 * loops * math.cos(a))))
        out.append((pts, r))
    jz = M.JOE[1] + 20.0                                                 # the strands run back to where he sits (the game draws the rest on him)
    for i in range(strands):
        off = (i - (strands - 1) / 2) * 5.6
        pts = curve3([(rx - 2.0 + off * 0.5, y, rz - 2.5), (rx + off + 1.0 * math.sin(i * 1.7), y, (rz + jz) / 2), (rx + off * 0.7 - 2.0, y, jz)], 6)
        out.append(([P3(*p) for p in pts], r * 0.92))
    length = 16.0 + gone * 15.0
    wig = [(rx + 2.4, rz + 2.0), (rx + 6.0, rz + length * 0.3), (rx - 1.5 + 2.5 * gone, rz + length * 0.62), (rx + 3.5 - 1.5 * gone, rz + length)]
    pts = curve3([(x, y, z) for x, z in wig], 8)
    out.append(([P3(*p) for p in pts], r))
    ex, ey, ez = pts[-1]
    for i in range(4):                                                   # its frayed tip
        out.append(([P3(ex, ey, ez), P3(ex + 2.0 * math.cos(i * 1.9), ey + 0.3 * (i % 2), ez + 2.6 + 0.7 * i)], 0.4))
    return out


def ropes(st, strands=4):
    for pts, r in rope_paths(strands):
        st.rope(pts, r, m_rope, name="ropes", grp="ropes")


def belt(st):
    """The buckle end of a spare seatbelt lying on the long seat's cushion: a short black strap out of the crease between
    the cushion and the backrest, the buckle at its end near the cushion's edge, its chrome tongue toward us and its red
    button (the belt round Joe is drawn on him)."""
    bx, by, bz = M.BELT["at"]
    strap = plain("#202026", 0.08, 3.0, 111)
    wd = 6.0
    st.poly([P3(M.BACK_T + 0.5, by + 0.5, bz - 9 - wd / 2), P3(M.BACK_T + 0.5, by + 0.5, bz - 9 + wd / 2), P3(bx - 4, by + 0.7, bz + wd / 2), P3(bx - 4, by + 0.7, bz - wd / 2)],
            strap, name="belt", bias=0.6)
    st.box(bx - 5.0, bx + 5.0, by, by + 2.6, bz - 4.4, bz + 4.4, "#1c1c22", name="belt")                   # the buckle's black head
    st.box(bx - 2.6, bx + 1.8, by + 2.6, by + 3.3, bz - 2.2, bz + 2.2, "#d8382c", name="belt", shadow=False)       # its red button
    st.box(bx + 5.0, bx + 11.0, by + 0.6, by + 1.6, bz - 2.4, bz + 2.4, "#f0f2f6", name="belt", shadow=False)      # the chrome tongue, out of it toward the aisle


# ---------------------------------------------------------------- all of it
def build(st, strands=4, divider_down=False, things=True):
    shell(st)
    divider(st, down=divider_down)
    seats(st)
    bar(st)
    fridge(st)
    belt(st)
    if strands > 0:
        ropes(st, strands)
    if things:
        bag(st)
        juice(st)
        clipboard(st)
    front(st)

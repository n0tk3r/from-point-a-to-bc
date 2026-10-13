"""Everything inside the wagon, built in the car's own centimetres (egypt_car.py).

Each function puts one group of things on the Stage (egypt_car_kit.Stage): boxes, rods, round things and flat sheets,
each with a material that paints it in ITS OWN measurements (the cushion's pleats along its own length, the wood's grain
along the dash). All measurements come from the model (egypt_car_model.py), so the skeleton, the picture and layout.json
agree. The smallest marks (the numbers on the dials, the key's ring, the drawing behind the visor) are not here: they are
egypt_car_details.py's, said crisply over the brushwork as the painter's details pass does.

Groups (grp): "back" is the backdrop; each cut-out is its own group: "glovebox" (the door, shut, or dropped open with the
map in the compartment: "map" is the map alone), "visor" (the driver's sun visor, up or down) and "freshener" (the little
cardboard wagon on its string). Rays that leave the car (the windshield, the passenger's window, the open window at Dad's
left) meet nothing: egypt_car.py lays the world outside there (egypt_car_world.py). The hood, the cowl and the wipers are
the car's own, outside the glass, and are built here.

No maker's name or badge anywhere: not on the wheel's horn pad, the radio, the dials, the slushie's cup or the
wrappers. "NEW CAR" on the air freshener is the only word, and it is too small to read."""

import math

import numpy as np

from brush import F32, lerp
import egypt_car_model as M
import egypt_car_props as PR
from egypt_car_kit import col, mixc, fbm, hashf, lines_aa, band, rect, disc, lay, sstep

_TEX = {}


def tex(name):
    """The props' flat pictures (egypt_car_props.py), drawn once."""
    if name not in _TEX:
        if name.startswith("dial-"):
            i = int(name[-1])
            X, Y, r = M.DIALS[i]
            _TEX[name] = PR.Tex(PR.dial("speed" if i == 0 else "fuel", r), origin=(X - r, Y + r), flip=True)
        elif name == "prndl":
            x0, x1 = M.PRNDL["x"]
            y0, y1 = M.PRNDL["y"]
            _TEX[name] = PR.Tex(PR.prndl(x1 - x0, y1 - y0), origin=(x0, y1), flip=True)
        elif name == "drawing":
            _TEX[name] = PR.Tex(PR.drawing(), origin=VISOR_SHEETS["drawing"])
        elif name == "registration":
            _TEX[name] = PR.Tex(PR.registration(), origin=VISOR_SHEETS["registration"])
    return _TEX[name]


VISOR_SHEETS = {"drawing": (4.5, 4.2), "registration": (24.5, 4.0)}      # where on the visor's back (U across from its inner end, V down from its hinge)
STRAP = (6.0, 7.6)                                                        # the strap across the visor's back (V)

# ---------------------------------------------------------------- the colours of things (before any light falls on them)
TAN = "#cda677"            # the dash and the doors' upper panels: tan vinyl
TAN_L = "#d8b686"          # the glovebox's door, a shade lighter, so that it reads at a glance
TAN_D = "#a27e54"          # darker tan vinyl: the doors' lower panels, the seats' sides
CLOTH = "#d0aa7a"          # the seats' tan cloth
HEADLINER = "#e2caa2"      # the headliner's cloth, warm and pale
WOOD = "#9a5e32"           # the wood-grain strip across the dash (the outside's wood, echoed)
WOOD_D = "#5e341a"
WOOD_L = "#be7e48"
CHROME = "#eef0f2"
CHROME_D = "#62666e"
RUBBER = "#2c2629"         # the wheel's rim, the column: dark, a little warm
DIAL = "#211e24"           # the dials' faces
CARPET = "#4a3022"         # the floor: a deep warm brown
RED = "#b84a38"            # the hood, outside: the wagon's red, a little dusty
PACKET = "#c8322a"         # the ketchup packets


def P3(X, Y, Z):
    return (float(X), float(Y), float(Z))


def plain(color, amt=0.08, s=14.0, seed=0):
    """One paint, a little patchy as a brush leaves it."""
    k = col(color)

    def f(c):
        n = fbm((c.X + 0.37 * c.Y) / s, (c.Z + 0.61 * c.Y) / s, seed, 3)
        return k * (1 + amt * 2 * (n[..., None] - 0.5))
    return f


def vinyl(color, seed=0, amt=0.07, grain=0.05):
    """Tan vinyl: a little patchy, with a fine pebbled grain that fades to a tone where it is too small to see."""
    k = col(color)

    def f(c):
        n = fbm((c.X + 0.37 * c.Y) / 16.0, (c.Z + 0.61 * c.Y) / 16.0, seed, 3)
        out = k * (1 + amt * 2 * (n[..., None] - 0.5))
        if grain and hasattr(c, "gX"):                                                        # (rods and round things have no steps: no grain)
            fine = fbm((c.X + 0.5 * c.Z) / 0.5, (c.Y + 0.3 * c.Z) / 0.5, seed + 3, 2)
            g = np.clip(0.9 / np.maximum(np.maximum(c.gX, c.gY), np.maximum(c.gZ, 1e-3)) * 0.5 - 0.5, 0, 1)     # only where a 5 mm pebble is a pixel or more
            out = out + k * grain * g[..., None] * (fine[..., None] - 0.5)
        return out
    return f


def occlude(st, x0, x1, y0, y1, z0, z1, grp="back"):
    """A box that throws a shadow and is not drawn (for slanted things the boxes of the kit cannot draw)."""
    st.occ.append((min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), min(z0, z1), max(z0, z1)))
    st.occ_grp.append(grp)


def rounded(x0, x1, y0, y1, r, n=5):
    """A rounded rectangle's corners (convex), counter-clockwise from the bottom left, in (x, y)."""
    pts = []
    for (cx, cy, a0) in ((x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def inside_rounded(u, v, x0, x1, y0, y1, r):
    """How far inside a rounded rectangle (cm; negative outside)."""
    qx = np.maximum(np.abs(u - (x0 + x1) / 2) - ((x1 - x0) / 2 - r), 0)
    qy = np.maximum(np.abs(v - (y0 + y1) / 2) - ((y1 - y0) / 2 - r), 0)
    inner = np.minimum(np.maximum(np.abs(u - (x0 + x1) / 2) - ((x1 - x0) / 2 - r), np.abs(v - (y0 + y1) / 2) - ((y1 - y0) / 2 - r)), 0)
    return -(np.hypot(qx, qy) + inner - r)


# ---------------------------------------------------------------- the shell: floor, doors, roof, pillars
def m_headliner(c):
    """The headliner: a pale warm cloth, its bows showing as soft seams across the car."""
    X, Z = c.X, c.Z
    n = fbm(X / 30.0, Z / 30.0, 9, 3)
    base = col(HEADLINER) * (0.93 + 0.1 * n[..., None])
    seam = lines_aa(Z, 27.0, 0.8, c.gZ * c.ss, phase=M.GLASS["z1"] + 14.0)
    base = base * (1 - 0.13 * seam[..., None])
    weave = fbm(X / 0.35, Z / 0.35, 10, 1)
    vis = np.clip(0.35 / np.maximum(np.maximum(c.gX, c.gZ), 1e-3) - 0.6, 0, 1)
    return base * (1 + 0.04 * vis[..., None] * (weave[..., None] - 0.5))


def m_trim(color, seed):
    """The cloth-covered trim of the pillars and the roof rails: the headliner's cloth, a seam along it."""
    k = col(color)

    def f(c):
        n = fbm((c.X + c.Z) / 12.0, c.Y / 12.0, seed, 3)
        base = k * (0.92 + 0.12 * n[..., None])
        if hasattr(c, "V"):
            seam = band(c.V, 1.4, 1.9, np.maximum(c.gV, 1e-3) * c.ss)
            base = base * (1 - 0.18 * seam[..., None])
        return base
    return f


def m_door(side):
    """A door's inner panel below the belt line: the window's channel at the top (felt, and in it, on Dad's side, the
    top edge of the glass wound down, a bright sliver); a padded band of tan vinyl; a chrome strip; the lower panel in
    darker vinyl with upright pleats; the seal along its front edge."""
    def f(c):
        Y, Z = c.Y, c.Z
        gY, gZ = c.gY * c.ss, c.gZ * c.ss
        n = fbm(Z / 18.0, Y / 18.0, 31 if side == "L" else 32, 3)
        top = col(TAN) * (0.92 + 0.12 * n[..., None])
        low = col(TAN_D) * (0.90 + 0.14 * n[..., None])
        pleat = lines_aa(Z, 4.2, 0.7, gZ)
        low = low * (1 - 0.16 * pleat[..., None])
        base = lerp(low, top, band(Y, 61.0, 200.0, gY)[..., None])
        base = lay(base, CHROME, band(Y, 60.4, 61.3, gY) * 0.85)
        base = lay(base, "#3a2a22", band(Y, M.BELT - 1.6, M.BELT + 2.0, gY))                     # the window's channel
        if side == "L":
            base = lay(base, "#eef4f4", band(Y, M.BELT - 1.25, M.BELT - 0.55, gY) * 0.95)       # the glass's top edge, wound down
        base = lay(base, "#2c2420", band(Z, -50.0, 1.4, gZ))                                      # the seal along its front edge
        return base
    return f


def m_carpet(c):
    nap = fbm(c.X / 2.5, c.Z / 2.5, 21, 3)
    return col(CARPET) * (0.85 + 0.3 * nap[..., None])


def shell(st):
    """The floor and the hump, the two doors below the belt line, the roof and its headliner, the windshield's pillars
    and header, the roof rails over the side windows. The windshield, the passenger's window and the driver's (rolled
    down) are openings: rays go through them to the world."""
    W, B, R, T = M.W, M.BELT, M.ROOF, M.TUMBLE
    st.box(-60, W + 60, -10, 0, -80, 260, m_carpet, name="floor", shadow=False)
    st.box(64, 100, 0, 17, -60, 260, m_carpet, name="hump")
    st.box(-12, 0, 0, B, -40, 260, m_door("L"), name="door-l")
    st.box(W, W + 12, 0, B, -40, 260, m_door("R"), name="door-r")
    st.box(-20, W + 20, R, R + 8, M.GLASS["z1"], 260, m_headliner, name="headliner")
    for side in (-1, 1):                                                                  # the roof rails over the side windows
        x_out = 0.0 if side < 0 else W
        x_in = x_out - side * T
        st.poly([P3(x_out, M.SIDE_TOP, M.GLASS["z1"] + 4), P3(x_out, M.SIDE_TOP, 260), P3(x_in, R, 260), P3(x_in, R, M.GLASS["z1"] + 4)],
                m_trim(HEADLINER, 41 + side), name="rail-l" if side < 0 else "rail-r")
        occlude(st, min(x_out, x_in) - 6, max(x_out, x_in) + 6, M.SIDE_TOP, R + 8, M.GLASS["z1"], 260)
    for side in (-1, 1):                                                                  # the windshield's pillars
        foot = P3(0.0 if side < 0 else W, B, M.GLASS["z0"])
        top = P3(T if side < 0 else W - T, R, M.GLASS["z1"])
        wid = 10.5
        inward = 6.0 if side < 0 else 3.2                                                 # (Dad's own pillar turns its face a little more to him)
        a = P3(foot[0] - side * inward, foot[1], foot[2] + wid)
        b = P3(top[0] - side * inward * 0.8, top[1], top[2] + wid * 0.85)
        st.poly([foot, top, b, a], m_trim("#d6bc94", 43 + side), name="pillar-l" if side < 0 else "pillar-r")
        for k in range(6):
            t0, t1 = k / 6, (k + 1) / 6
            p0 = [lerp(foot[i], top[i], t0) for i in range(3)]
            p1 = [lerp(foot[i], top[i], t1) for i in range(3)]
            occlude(st, min(p0[0], p1[0]) - 3.5, max(p0[0], p1[0]) + 3.5, p0[1], p1[1], min(p0[2], p1[2]) - 1, max(p0[2], p1[2]) + wid)
    st.poly([P3(T, R - 2.2, M.GLASS["z1"] + 0.6), P3(W - T, R - 2.2, M.GLASS["z1"] + 0.6), P3(W - T, R, M.GLASS["z1"] + 4.2), P3(T, R, M.GLASS["z1"] + 4.2)],
            m_trim("#d8be96", 45), name="header")
    occlude(st, -20, W + 20, R - 2.5, R + 8, M.GLASS["z1"] - 1, M.GLASS["z1"] + 5)


# ---------------------------------------------------------------- the dashboard
def m_dash_top(c):
    """The padded top: tan vinyl in hard sun; along the glass, the defroster's two long grilles."""
    base = vinyl(TAN, 51, 0.06, 0.05)(c)
    X, Z = c.X, c.Z
    gX, gZ = c.gX * c.ss, c.gZ * c.ss
    for (x0, x1) in ((8.0, 70.0), (94.0, 156.0)):
        g = band(X, x0, x1, gX) * band(Z, 0.8, 3.4, gZ)
        rib = lines_aa(X, 1.3, 0.55, gX)
        base = lay(base, "#2e2622", g * (0.85 - 0.5 * rib))
    return base


def m_face(glove_open):
    """The dash's face toward Dad: tan vinyl, a stitched seam under the lip, the wood-grain band along its foot with a
    chrome line at each edge; holes where the gauges, the vents and (open) the glovebox's compartment are set in."""
    hx0, hx1, hy0, hy1 = M.HOOD_CLUSTER["opening"]
    g = M.GLOVEBOX

    def f(c):
        X, Y = c.X, c.Y
        gX, gY = c.gX * c.ss, c.gY * c.ss
        base = vinyl(TAN, 52, 0.06, 0.04)(c)
        base = base * (1 - 0.22 * band(Y, M.DASH["top"] - M.DASH["lip"] - 1.4, M.DASH["top"] - M.DASH["lip"] - 0.9, gY)[..., None])
        w0, w1 = M.WOOD
        grain = fbm(X / 9.0, Y / 0.55, 53, 3)
        streak = 0.5 + 0.5 * np.sin(X * 0.21 + grain * 9.0 + Y * 1.7)
        wood = lerp(col(WOOD), col(WOOD_L), (streak ** 3 * 0.55)[..., None])
        wood = lerp(wood, col(WOOD_D), (np.clip(grain - 0.62, 0, 1) * 1.6)[..., None])
        base = lay(base, wood, band(Y, w0, w1, gY))
        base = lay(base, CHROME, (band(Y, w0 - 0.45, w0, gY) + band(Y, w1, w1 + 0.45, gY)) * 0.85)
        keep = inside_rounded(X, Y, hx0, hx1, hy0, hy1, 2.6) < 0
        for (x0, x1, y0, y1) in M.VENTS:
            keep &= inside_rounded(X, Y, x0, x1, y0, y1, 0.8) < 0
        if glove_open:
            keep &= inside_rounded(X, Y, g["x"][0] + 0.8, g["x"][1] - 0.8, g["y"][0] + 0.5, g["y"][1] - 0.6, g["r"]) < 0
        return base, None, keep
    return f


def m_cluster_back(c):
    """Behind the dials: dark, with a chrome ring round each dial's well, and the gear strip between them (P R N D L,
    the pointer at P)."""
    base = col("#262328") * (0.9 + 0.15 * fbm(c.X / 3, c.Y / 3, 54, 2)[..., None])
    g = np.maximum(c.gX, c.gY) * c.ss
    for (X, Y, r) in M.DIALS:
        d = np.hypot(c.X - X, c.Y - Y)
        base = lay(base, CHROME_D, band(d, r, r + 0.9, g) * 0.9)
        base = lay(base, CHROME, band(d, r + 0.15, r + 0.55, g) * 0.8)
    rgb, a = tex("prndl").sample(c.X, c.Y)
    return base * (1 - a[..., None]) + rgb * a[..., None]


def m_dial(c):
    """A dial's face: dark, its figures and ticks white, its needles orange; the warning lamp lit (it glows)."""
    out = np.broadcast_to(col(DIAL), c.X.shape + (3,)).copy()
    emi = np.zeros_like(out)
    for i in range(len(M.DIALS)):
        rgb, a = tex(f"dial-{i}").sample(c.X, c.Y)
        out = out * (1 - a[..., None]) + rgb * a[..., None]
        red = (rgb[..., 0] > 0.9) & (rgb[..., 1] < 0.5) & (a > 0.5)
        emi = emi + (red * 0.55)[..., None] * col("#ff5a3c")[None, :]
    return out, emi


def m_vent(c):
    """A square air vent: a chrome bezel, and behind it dark louvers, level, each slat's top edge catching the light."""
    out = col("#1e1a1c")
    slat = lines_aa(c.Y, 1.15, 0.55, c.gY * c.ss)
    return lay(out, "#6a6064", slat * 0.85)


def m_radio(c):
    """The radio's face: a charcoal plate, a chrome rim, the cassette slot along its top half, the tuning window below."""
    X, Y = c.X, c.Y
    gX, gY = c.gX * c.ss, c.gY * c.ss
    x0, x1 = M.RADIO["x"]
    y0, y1 = M.RADIO["y"]
    base = col("#36302f") * (0.92 + 0.12 * fbm(X / 2, Y / 2, 55, 2)[..., None])
    rimd = np.minimum(np.minimum(X - x0, x1 - X), np.minimum(Y - y0, y1 - Y))
    base = lay(base, CHROME, band(rimd, 0.0, 0.55, np.maximum(gX, gY)) * 0.9)
    base = lay(base, "#100e10", rect(X, Y, x0 + 4.5, x1 - 4.5, y1 - 2.9, y1 - 1.7, np.maximum(gX, gY)))        # the cassette's slot
    win = rect(X, Y, x0 + 5.0, x1 - 5.0, y0 + 1.2, y0 + 3.4, np.maximum(gX, gY))
    scale = lerp(col("#e8dcb8"), col("#c8b890"), fbm(X / 3, Y, 56, 2)[..., None])
    scale = lay(scale, "#5a5040", lines_aa(X, 0.85, 0.35, gX) * 0.6)
    base = lay(base, scale, win)
    return base


def tape_mat(c):
    """A cassette half out of the deck: dark grey, and along its spine a plain white label (Mom's musical: no title on it)."""
    base = col("#4a4648") * (0.92 + 0.1 * fbm(c.X, c.Z, 68, 2)[..., None])
    if c.face == "front":
        g = np.maximum(c.gX, c.gY) * c.ss
        base = lay(base, "#ece6d6", band(c.X, M.RADIO["x"][0] + 6.0, M.RADIO["x"][0] + 14.0, g) * 0.9)
    if c.face == "top":
        g = np.maximum(c.gX, c.gZ) * c.ss
        base = lay(base, "#ece6d6", band(c.X, M.RADIO["x"][0] + 6.0, M.RADIO["x"][0] + 14.0, g) * band(c.Z, M.DASH["z_face"] + 1.6, M.DASH["z_face"] + 4.2, g) * 0.85)
    return base


def m_sliders(c):
    X, Y = c.X, c.Y
    gX, gY = c.gX * c.ss, c.gY * c.ss
    base = col("#3a3233")
    for k in range(3):
        yy = M.SLIDERS["y"][0] + 0.9 + k * 1.15
        base = lay(base, "#0e0c0e", band(Y, yy - 0.18, yy + 0.18, gY) * band(X, M.SLIDERS["x"][0] + 2.0, M.SLIDERS["x"][1] - 2.0, gX))
    rimd = np.minimum(np.minimum(X - M.SLIDERS["x"][0], M.SLIDERS["x"][1] - X), np.minimum(Y - M.SLIDERS["y"][0], M.SLIDERS["y"][1] - Y))
    return lay(base, CHROME_D, band(rimd, 0, 0.4, np.maximum(gX, gY)) * 0.8)


def m_ashtray(c):
    X, Y = c.X, c.Y
    g = np.maximum(c.gX, c.gY) * c.ss
    grain = fbm(X / 9.0, Y / 0.55, 57, 3)
    wood = lerp(col(WOOD), col(WOOD_L), (0.5 + 0.5 * np.sin(X * 0.3 + grain * 8.0))[..., None] ** 3 * 0.5)
    rimd = np.minimum(np.minimum(X - M.ASHTRAY["x"][0], M.ASHTRAY["x"][1] - X), np.minimum(Y - M.ASHTRAY["y"][0], M.ASHTRAY["y"][1] - Y))
    wood = lay(wood, CHROME, band(rimd, 0, 0.4, g) * 0.85)
    mid = (M.ASHTRAY["x"][0] + M.ASHTRAY["x"][1]) / 2
    return lay(wood, CHROME, rect(X, Y, mid - 3.0, mid + 3.0, M.ASHTRAY["y"][1] - 1.3, M.ASHTRAY["y"][1] - 0.6, g))        # its pull


def m_glovedoor(c):
    """The glovebox's door, shut: tan vinyl a shade lighter than the dash, a raised border round it, the push-button
    latch at its top middle (chrome) with the keyhole in it."""
    g = M.GLOVEBOX
    X, Y = c.X, c.Y
    gg = np.maximum(c.gX, c.gY) * c.ss
    base = vinyl(TAN_L, 58, 0.05, 0.04)(c)
    d = inside_rounded(X, Y, g["x"][0], g["x"][1], g["y"][0], g["y"][1], g["r"])
    base = base * (1 - 0.30 * band(d, 1.25, 1.55, gg)[..., None])                      # the border's groove
    base = lay(base, "#f0d8b0", band(d, 1.55, 1.85, gg) * 0.55)                        # and its lit edge
    base = lay(base, "#a07a52", band(d, 0.0, 0.35, gg) * 0.6)                          # the door's own edge
    mid = (g["x"][0] + g["x"][1]) / 2
    btn = inside_rounded(X, Y, mid - 2.4, mid + 2.4, g["y"][1] - 3.0, g["y"][1] - 1.0, 0.7)
    base = lay(base, CHROME_D, band(btn, 0.0, 0.35, gg))
    base = lay(base, CHROME, np.clip(btn / 0.35 - 1, 0, 1))
    key = np.hypot((X - mid) / 0.55, (Y - (g["y"][1] - 2.0)) / 0.55)
    base = lay(base, "#24201e", np.clip((1 - key) * 3, 0, 1))
    return base


def m_glovedoor_in(c):
    """The glovebox's door, dropped open: its inside face, moulded plastic in tan, two round cup recesses and a ridge."""
    U, V = c.U, c.V
    gU, gV = np.maximum(c.gU, 1e-3) * c.ss, np.maximum(c.gV, 1e-3) * c.ss
    base = col("#c09a6c") * (0.93 + 0.1 * fbm(U / 4, V / 4, 59, 2)[..., None])
    L = M.GLOVEBOX["x"][1] - M.GLOVEBOX["x"][0]
    for cu in (L * 0.3, L * 0.7):
        d = np.hypot(U - cu, V - 7.0)
        base = base * (1 - 0.22 * np.clip(1 - d / 3.6, 0, 1)[..., None])
        base = lay(base, "#f0d6ac", band(d, 3.4, 3.8, np.maximum(gU, gV)) * 0.5)
    base = base * (1 - 0.18 * band(V, 12.6, 13.2, gV)[..., None])
    return base


def m_compartment(c):
    """Inside the glovebox: dark brown, in its own shade."""
    return col("#4a3626") * (0.85 + 0.25 * fbm(c.X / 4, (c.Y + c.Z) / 4, 60, 2)[..., None])


def dash(st, glove_open=False):
    """The padded top (in the sun), its rounded lip, the face toward Dad with the wood strip along its foot, the hood
    over the gauges and the dials set in under it, the middle (vents, radio, sliders, ashtray), and the glovebox's
    compartment (its door is glovebox(), a cut-out). The lower dash slopes in under the face to the footwells."""
    W, D = M.W, M.DASH
    zf = D["z_face"]
    st.box(-2, W + 2, D["top"] - 6.0, D["top"], -6.0, zf - D["lip"], m_dash_top, name="dash-top")
    st.cyl((D["top"] - D["lip"], zf - D["lip"]), D["lip"], -2, W + 2, vinyl(TAN, 61, 0.05, 0.03), axis="x", name="dash-lip")
    st.poly([P3(-2, D["low"], zf), P3(W + 2, D["low"], zf), P3(W + 2, D["top"] - D["lip"], zf), P3(-2, D["top"] - D["lip"], zf)],
            m_face(glove_open), name="dash-face")
    occlude(st, -2, W + 2, D["low"], D["top"], -8, zf)
    st.poly([P3(-2, D["low"], zf), P3(W + 2, D["low"], zf), P3(W + 2, 30.0, 4.0), P3(-2, 30.0, 4.0)], vinyl(TAN_D, 62, 0.08, 0.03), name="dash-low")
    st.poly([P3(-2, 30.0, 4.0), P3(W + 2, 30.0, 4.0), P3(W + 2, 0.0, -20.0), P3(-2, 0.0, -20.0)], m_carpet, name="toeboard")
    # the hood over the gauges, and the well it shades: the dials' faces set back, a chrome ring round each
    h = M.HOOD_CLUSTER
    hx0, hx1, hy0, hy1 = h["opening"]
    st.box(h["x"][0], h["x"][1], hy1, h["top"], 6.0, h["z"], vinyl(TAN, 63, 0.05, 0.03), name="cluster-hood")
    st.poly([P3(hx0, hy0, M.DIAL_Z - 0.4), P3(hx1, hy0, M.DIAL_Z - 0.4), P3(hx1, hy1, M.DIAL_Z - 0.4), P3(hx0, hy1, M.DIAL_Z - 0.4)], m_cluster_back, name="cluster")
    for x in (hx0, hx1):
        st.poly([P3(x, hy0, M.DIAL_Z - 0.4), P3(x, hy0, zf), P3(x, hy1, zf), P3(x, hy1, M.DIAL_Z - 0.4)], plain("#2a2628", 0.05, 4, 64), name="cluster")
    st.poly([P3(hx0, hy0, M.DIAL_Z - 0.4), P3(hx1, hy0, M.DIAL_Z - 0.4), P3(hx1, hy0, zf), P3(hx0, hy0, zf)], plain("#3a3436", 0.05, 4, 65), name="cluster")
    for (X, Y, r) in M.DIALS:
        st.poly([P3(X + r * math.cos(a), Y + r * math.sin(a), M.DIAL_Z) for a in np.linspace(0, 2 * math.pi, 48, endpoint=False)], m_dial, name="dial")
    # the middle: two square vents (set back behind the face), the radio, the heater's sliders, the ashtray
    for (x0, x1, y0, y1) in M.VENTS:
        st.poly([P3(x0, y0, zf - 1.2), P3(x1, y0, zf - 1.2), P3(x1, y1, zf - 1.2), P3(x0, y1, zf - 1.2)], m_vent, name="vent")
        st.poly([P3(x0, y0, zf - 1.2), P3(x1, y0, zf - 1.2), P3(x1, y0, zf), P3(x0, y0, zf)], plain("#4a4044", 0.05, 4, 66), name="vent")
        for x in (x0, x1):                                                                # the well's sides (a ray slanting in by its edge meets one)
            st.poly([P3(x, y0, zf - 1.2), P3(x, y0, zf), P3(x, y1, zf), P3(x, y1, zf - 1.2)], plain("#2c2628", 0.05, 4, 69), name="vent")
    r = M.RADIO
    st.box(r["x"][0], r["x"][1], r["y"][0], r["y"][1], zf, zf + 0.9, m_radio, name="radio")
    yt = r["y"][1] - 2.3                                                                  # the tape, half out of the deck: its top, its spine toward Dad
    st.box(r["x"][0] + 5.0, r["x"][0] + 15.0, yt - 0.55, yt + 0.55, zf + 0.9, zf + 4.2, tape_mat, name="radio")
    for kx in (r["x"][0] + 2.3, r["x"][1] - 2.3):                                         # its two knobs
        st.cyl((kx, (r["y"][0] + r["y"][1]) / 2 - 0.6), 1.15, zf + 0.9, zf + 2.6, plain("#2a2628", 0.04, 4, 67), axis="z", name="radio", cap="#d8dce0")
    s = M.SLIDERS
    st.poly([P3(s["x"][0], s["y"][0], zf + 0.3), P3(s["x"][1], s["y"][0], zf + 0.3), P3(s["x"][1], s["y"][1], zf + 0.3), P3(s["x"][0], s["y"][1], zf + 0.3)], m_sliders, name="sliders")
    a = M.ASHTRAY
    st.poly([P3(a["x"][0], a["y"][0], zf + 0.35), P3(a["x"][1], a["y"][0], zf + 0.35), P3(a["x"][1], a["y"][1], zf + 0.35), P3(a["x"][0], a["y"][1], zf + 0.35)], m_ashtray, name="ashtray")
    # the glovebox's compartment, behind the face (seen when its door is down)
    g = M.GLOVEBOX
    x0, x1, y0, y1, dz = g["x"][0] + 0.8, g["x"][1] - 0.8, g["y"][0] + 0.5, g["y"][1] - 0.6, g["depth"]
    st.poly([P3(x0, y0, zf - dz), P3(x1, y0, zf - dz), P3(x1, y0, zf), P3(x0, y0, zf)], m_compartment, name="glove-inside")       # its floor
    st.poly([P3(x0, y0, zf - dz), P3(x1, y0, zf - dz), P3(x1, y1, zf - dz), P3(x0, y1, zf - dz)], m_compartment, name="glove-inside")   # its back
    for x in (x0, x1):
        st.poly([P3(x, y0, zf - dz), P3(x, y0, zf), P3(x, y1, zf), P3(x, y1, zf - dz)], m_compartment, name="glove-inside")
    st.poly([P3(x0, y1, zf - dz), P3(x1, y1, zf - dz), P3(x1, y1, zf), P3(x0, y1, zf)], m_compartment, name="glove-inside")


# ---------------------------------------------------------------- the glovebox: its door (a cut-out), the packets, the map
def packets(st, seed=3, grp="back"):
    """A drift of ketchup packets on the compartment's floor, heaped toward its back and sliding to its lip: plain red,
    a pale band across one end where it tears; no writing on them."""
    g = M.GLOVEBOX
    zf, dz = M.DASH["z_face"], g["depth"]
    rng = np.random.default_rng(seed)
    floor = g["y"][0] + 0.5
    n = 0
    for layer in range(3):
        for k in range(16 - layer * 5):
            cx = g["x"][0] + 3.0 + rng.random() * (g["x"][1] - g["x"][0] - 6.0)
            cz = zf - dz + 2.0 + (1 - rng.random() ** (1.6 + layer * 0.4)) * (dz - 3.0 - layer * 2.0)
            cz = min(cz, zf - 3.3)                                                        # none pokes out over the lip (the shut door would not hide it)
            heap = 1.6 * math.exp(-((cx - (g["x"][0] + g["x"][1]) / 2) / 14.0) ** 2) * (1 - (cz - (zf - dz)) / dz)
            cy = floor + 0.25 + layer * 0.55 + heap * layer * 0.6
            a = rng.random() * math.pi
            w, h = 2.6, 1.7
            tilt = rng.normal(0, 0.18)
            ca, sa = math.cos(a), math.sin(a)
            pts = [P3(cx + ca * u - sa * v, cy + tilt * u, cz + sa * u + ca * v) for u, v in ((-w, -h), (w, -h), (w, h), (-w, h))]
            tone = ["#dc3a2e", "#c8322a", "#e44634", "#b82c26"][int(rng.integers(0, 4))]
            end = 1 if rng.random() < 0.5 else -1
            def mat(c, tone=tone, end=end, w=w):
                base = col(tone) * (0.9 + 0.2 * fbm(c.U * 1.5, c.V * 1.5, 70, 2)[..., None])
                strip = band(c.U * end if end > 0 else (2 * w - c.U), 2 * w - 0.9, 2 * w + 1.0, np.maximum(c.gU, 1e-3) * c.ss)
                return lay(base, "#efe4d2", strip * 0.9)
            st.poly(pts, mat, name="packets", grp=grp, bias=0.02 * (layer + 1))
            n += 1
    return n


def m_map(c):
    """The folded road map, its cover up: white card, a broad blue band across its top, and under it a bright little map
    (yellow land, green valleys, a blue river, two red roads) as such covers have; no names that can be read, no maker's
    mark. Its folds show as faint creases."""
    U, V = c.U, c.V
    gg = np.maximum(np.maximum(c.gU, c.gV), 1e-3) * c.ss
    L, D = MAP["w"], MAP["d"]
    base = np.broadcast_to(col("#f6f1e2"), U.shape + (3,)).copy()
    inner = rect(U, V, 1.2, L - 1.2, 4.2, D - 1.0, gg)
    land = fbm(U / 2.6, V / 2.6, 71, 3)
    pic = lerp(col("#f2dc78"), col("#8cc06a"), sstep(0.42, 0.62, land)[..., None])
    river = np.abs(V - (D * 0.62 + 1.6 * np.sin(U * 0.45) + 0.8 * fbm(U / 3, V / 3, 72, 2)))
    pic = lay(pic, "#3c7cc8", np.clip((0.55 - river) / 0.35, 0, 1))
    for k, (a, b) in enumerate(((0.5, 0.0), (-0.35, 1.0))):
        road = np.abs((V - D * 0.3) - a * (U - L * 0.5) - b * 2.0)
        pic = lay(pic, "#d83a2c", np.clip((0.32 - road) / 0.18, 0, 1))
    base = lerp(base, pic, inner[..., None])
    base = lay(base, "#2c58a8", rect(U, V, 0.0, L, 0.6, 3.6, gg) * 0.95)                  # the cover's band
    base = lay(base, "#f6f1e2", rect(U, V, 2.0, L * 0.55, 1.6, 2.6, gg) * 0.8)             # (a pale bar in it: a title nobody can read)
    base = base * (1 - 0.10 * lines_aa(U, L / 3.0, 0.5, gg, phase=0.0)[..., None])        # its folds
    return base


MAP = dict(w=24.0, d=13.5)


def the_map(st, grp="glovebox"):
    """The folded road map, lying on top of the packets, its near corner over the lip of the compartment."""
    g = M.GLOVEBOX
    zf, dz = M.DASH["z_face"], g["depth"]
    y = g["y"][0] + 3.0
    x0 = g["x"][0] + 6.0
    a = math.radians(-7.0)                                                                # it lies a little askew, its near edge over the lip
    z1 = zf + 1.4
    u = (math.cos(a), math.sin(a))
    v = (-math.sin(a), math.cos(a))
    P = lambda s, t, h: P3(x0 + s * u[0] - t * v[0], y + h, z1 - s * u[1] - t * v[1])
    st.poly([P(0, 0, 0.9), P(MAP["w"], 0, 1.4), P(MAP["w"], MAP["d"], 2.2), P(0, MAP["d"], 1.6)], m_map, name="map", grp=grp)


def glovebox(st, state="shut"):
    """The glovebox's door: a big rounded door proud of the dash's face. Shut; or dropped open on its bottom hinge,
    hanging a little past level so that its inside face shows (and, `state` "map", the road map in the compartment)."""
    g, zf = M.GLOVEBOX, M.DASH["z_face"]
    x0, x1, y0, y1 = g["x"][0], g["x"][1], g["y"][0], g["y"][1]
    if state == "shut":
        st.poly([P3(x, y, zf + 1.2) for x, y in rounded(x0, x1, y0, y1, g["r"])], m_glovedoor, name="glove-door", grp="glovebox")
        st.poly([P3(x0 + 2, y1, zf), P3(x1 - 2, y1, zf), P3(x1 - 2, y1, zf + 1.2), P3(x0 + 2, y1, zf + 1.2)], vinyl("#e2c494", 74, 0.03, 0.0), name="glove-door", grp="glovebox")
        return
    a = math.radians(M.GLOVE_OPEN)
    h = y1 - y0
    hinge_z = zf + 0.6
    free = lambda X: P3(X, y0 + h * math.cos(a), hinge_z + h * math.sin(a))
    st.poly([P3(x0 + 0.4, y0, hinge_z), P3(x1 - 0.4, y0, hinge_z), free(x1 - 0.4), free(x0 + 0.4)], m_glovedoor_in, name="glove-door", grp="glovebox")
    th = 1.2                                                                              # its edge, toward Dad
    e = lambda X, k: P3(X, y0 + h * math.cos(a) - k * th * math.sin(a), hinge_z + h * math.sin(a) + k * th * math.cos(a))
    st.poly([e(x0 + 0.4, 0), e(x1 - 0.4, 0), e(x1 - 0.4, 1), e(x0 + 0.4, 1)], vinyl("#d8b886", 75, 0.03, 0.0), name="glove-door", grp="glovebox")
    if state == "map":
        the_map(st)


# ---------------------------------------------------------------- the wheel, the column, the key, the gear lever
def wheel(st):
    """A big thin rim with three spokes and a plain horn pad (no emblem); the column down into the dash; the gear lever
    from its right side; the ignition below the right spoke (the key itself, its ring and fob, are details)."""
    u, v, n = M.wheel_frame()
    c, r, tube = M.WHEEL["c"], M.WHEEL["r"], M.WHEEL["tube"]
    rim = [M.wheel_pt(a) for a in np.linspace(0, 360, 97)]
    st.rope(rim, tube, plain(RUBBER, 0.04, 4, 81), name="rim", min_px=0.6)
    for a in (0, 180, 270):
        st.stick(M.wheel_pt(a, 4.8, 0.9), M.wheel_pt(a, r - 0.5), 0.95, plain("#3a3438", 0.04, 4, 82), name="spoke")
    hw, hh = M.WHEEL["hub"]
    pad = [tuple(c[i] + x * u[i] + y * v[i] + 2.8 * n[i] for i in range(3)) for x, y in rounded(-hw / 2, hw / 2, -hh / 2, hh / 2, 2.6)]
    st.poly(pad, plain("#3c3438", 0.05, 6, 83), name="horn")
    rim2 = [tuple(c[i] + x * u[i] + y * v[i] + 1.2 * n[i] for i in range(3)) for x, y in rounded(-hw / 2 - 0.6, hw / 2 + 0.6, -hh / 2 - 0.6, hh / 2 + 0.6, 3.0)]
    st.poly(rim2, plain("#2a2427", 0.04, 6, 84), name="horn")
    t = (c[2] - M.COLUMN["to_z"]) / n[2]
    end = tuple(c[i] - t * n[i] for i in range(3))
    st.stick(tuple(c[i] - 1.2 * n[i] for i in range(3)), end, M.COLUMN["r"], plain("#2e282b", 0.04, 4, 85), name="column")
    st.stick(M.GEARS["root"], M.GEARS["knob"], 0.6, plain("#d8dce0", 0.03, 4, 86), name="gears")
    st.ball(M.GEARS["knob"], 1.55, plain("#1e1b1f", 0.04, 4, 87), name="gears-knob", squash=1.0)
    k = M.KEY["at"]
    st.ball(k, 1.05, plain("#c8ccd2", 0.03, 4, 88), name="ignition")
    key(st)


def key(st):
    """The car's key alone, in the ignition: its plain head sticking out of the lock, a small plain ring through it, and
    a plain leather fob hanging from the ring (Dad's house keys are on his own ring, in his pocket)."""
    kx, ky, kz = M.KEY["at"]
    head = [P3(kx + 0.9, ky - 1.3, kz + 1.0), P3(kx + 3.0, ky - 1.0, kz + 1.4), P3(kx + 3.0, ky + 1.0, kz + 1.4), P3(kx + 0.9, ky + 1.3, kz + 1.0)]
    st.poly(head, plain("#b8bcc2", 0.04, 4, 89), name="key")
    ring = [P3(kx + 3.4 + 1.25 * math.sin(a) * 0.35, ky - 1.6 - 1.25 + 1.25 * math.cos(a), kz + 1.6 + 1.25 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 25)]
    st.rope(ring, 0.16, plain("#d8dce0", 0.03, 4, 90), name="key", min_px=0.55)
    fx, fy, fz = kx + 3.6, ky - 4.0, kz + 2.9
    fob = [P3(fx - 1.0, fy, fz), P3(fx + 1.0, fy, fz + 0.2), P3(fx + 1.05, fy - 4.4, fz + 0.5), P3(fx - 0.95, fy - 4.4, fz + 0.3)]
    st.poly(fob, fob_mat, name="key")


def fob_mat(c):
    """A plain leather fob, brown, stitched round its edge: no name on it."""
    base = col("#7a4a2a") * (0.9 + 0.15 * fbm(c.U * 2, c.V * 2, 95, 2)[..., None])
    g = np.maximum(np.maximum(c.gU, c.gV), 1e-3) * c.ss
    d = np.minimum(np.minimum(c.U, 2.0 - c.U), np.minimum(c.V, 4.4 - c.V))
    return lay(base, "#c89a68", band(d, 0.3, 0.45, g) * 0.6)


# ---------------------------------------------------------------- the Son's half of the bench, the doors' fittings
def m_cushion(c):
    """The Son's cushion: tan cloth in pleats running back along the seat, a welt of darker vinyl along its front."""
    X, Z = c.X, c.Z
    gX, gZ = c.gX * c.ss, c.gZ * c.ss
    n = fbm(X / 14.0, Z / 14.0, 91, 3)
    base = col(CLOTH) * (0.92 + 0.14 * n[..., None])
    pleat = (X - M.SEAT["x"][0]) / 8.6
    f = pleat - np.floor(pleat)
    base = base * (0.94 + 0.10 * np.sin(f * math.pi)[..., None])                          # each pleat a little rounded
    base = base * (1 - 0.22 * lines_aa(X, 8.6, 0.7, gX, phase=M.SEAT["x"][0])[..., None])
    cx, cz, r = SEAT_CORNER
    edge = np.where((X < cx) & (Z < cz), r - np.hypot(X - cx, Z - cz), Z - M.SEAT["front"])
    base = base * (1 - 0.25 * band(edge, 0.0, 3.2, np.maximum(gX, gZ))[..., None])        # the welt's shadow along the edge
    weave = fbm(X / 0.4, Z / 0.4, 92, 1)
    return base * (1 + 0.05 * (weave[..., None] - 0.5))


SEAT_CORNER = (100.0, 70.0, 25.0)                                       # the cushion's front corner toward the bench's middle, rounded (X, Z of its middle, radius)


def seat_outline(n=12):
    """The Son's cushion's top, seen from above: its front edge, then its rounded corner, then its inner side, back."""
    s = M.SEAT
    cx, cz, r = SEAT_CORNER
    pts = [(s["x"][1], s["front"]), (cx, s["front"])]
    pts += [(cx + r * math.cos(a), cz + r * math.sin(a)) for a in np.linspace(math.radians(265), math.radians(185), n)]
    pts += [(cx - r, s["back"]), (s["x"][1], s["back"])]
    return pts


def bench(st):
    """The Son's half of the bench: its cushion's top (tan cloth), rounded at the corner toward the bench's middle, a welt
    of darker vinyl round its edge; the corner and its sides go down out of the picture."""
    s = M.SEAT
    st.poly([P3(x, s["top"], z) for x, z in seat_outline()], m_cushion, name="seat")
    occlude(st, SEAT_CORNER[0] - SEAT_CORNER[2], s["x"][1], 30.0, s["top"], s["front"], s["back"])
    st.cyl((s["top"] - 2.2, s["front"] + 2.2), 2.2, SEAT_CORNER[0], s["x"][1], vinyl(TAN_D, 93, 0.06, 0.03), axis="x", name="seat")
    cx, cz, r = SEAT_CORNER
    arc = [P3(cx + (r - 1.6) * math.cos(a), s["top"] - 1.4, cz + (r - 1.6) * math.sin(a)) for a in np.linspace(math.radians(272), math.radians(178), 40)]
    st.rope(arc, 1.6, vinyl(TAN_D, 94, 0.06, 0.0), name="seat", min_px=0.6)
    junk(st)


WRAPPERS = [((95.5, 52.0), 25, "#e0402c", "#f6d040"), ((97.5, 56.0), -40, "#f2c22e", "#e0402c"), ((107.0, 48.0), 70, "#3a9e4a", "#f4f0e0"),
            ((116.0, 54.5), 10, "#8a4aa8", "#f2c22e"), ((123.0, 47.5), -15, "#f08a2a", "#3a7ad0"), ((84.0, 57.5), 55, "#3a7ad0", "#f4f0e0")]


def junk(st, seed=5):
    """What the Son left on his seat: his seat belt lying unbuckled across it, its tongue near the middle; six candy
    wrappers, each a different loud colour, twisted at the ends (no names on them); and one sock, white, striped at the
    top, crumpled."""
    s = M.SEAT
    y = s["top"] + 0.15
    # the belt: comes off the cushion's far side at the right and lies across it to its tongue
    path = [(132.0, 58.0), (118.0, 55.5), (104.0, 52.0), (92.0, 51.5)]
    w = 2.4
    for (x0, z0), (x1, z1) in zip(path[:-1], path[1:]):
        L = math.hypot(x1 - x0, z1 - z0)
        nx, nz = -(z1 - z0) / L * w, (x1 - x0) / L * w
        st.poly([P3(x0 - nx, y, z0 - nz), P3(x1 - nx, y, z1 - nz), P3(x1 + nx, y, z1 + nz), P3(x0 + nx, y, z0 + nz)], belt_mat, name="belt", bias=0.05)
    tx, tz = path[-1]
    st.poly([P3(tx - 0.3, y + 0.25, tz - 1.6), P3(tx - 5.6, y + 0.25, tz - 1.2), P3(tx - 5.6, y + 0.25, tz + 1.2), P3(tx - 0.3, y + 0.25, tz + 1.6)],
            plain("#dfe3e8", 0.04, 4, 160), name="belt", bias=0.1)                                   # the tongue
    # the wrappers
    for k, ((cx, cz), ang, c1, c2) in enumerate(WRAPPERS):
        a = math.radians(ang)
        ca, sa = math.cos(a), math.sin(a)
        P = lambda u, v, h=0.0: P3(cx + ca * u - sa * v, y + 0.3 + h, cz + sa * u + ca * v)
        st.poly([P(-2.2, -1.3, 0.2), P(2.2, -1.3, 0.1), P(2.2, 1.3, 0.25), P(-2.2, 1.3, 0.15)], wrapper_mat(c1, c2, k), name="wrapper", bias=0.12)
        for e in (-1, 1):                                                                             # its twisted ends, a little fan each
            st.poly([P(e * 2.15, -0.6, 0.1), P(e * 3.0, -1.05, 0.05), P(e * 3.0, 1.05, 0.05), P(e * 2.15, 0.6, 0.12)], wrapper_mat(c1, c2, k + 7, end=True), name="wrapper", bias=0.12)
    # the sock
    sx, sz = 101.0, 59.5
    st.poly([P3(sx - 6.5, y + 0.6, sz - 1.8), P3(sx + 1.0, y + 0.9, sz - 2.4), P3(sx + 1.6, y + 0.8, sz + 1.6), P3(sx - 6.2, y + 0.5, sz + 2.0)], sock_mat(0), name="sock", bias=0.15)
    st.poly([P3(sx + 0.8, y + 0.9, sz - 2.4), P3(sx + 5.4, y + 0.7, sz - 4.6), P3(sx + 7.2, y + 0.6, sz - 1.2), P3(sx + 1.6, y + 0.8, sz + 1.6)], sock_mat(1), name="sock", bias=0.15)


def belt_mat(c):
    """The seat belt's webbing: grey-beige, its weave running along it."""
    return col("#8e826e") * (0.9 + 0.12 * fbm(c.U / 1.5, c.V / 0.4, 161, 2)[..., None])


def wrapper_mat(c1, c2, seed, end=False):
    """A candy wrapper: shiny paper in a loud colour, a band of another across it, crumpled (light and dark facets)."""
    def f(c):
        crumple = fbm(c.U * 1.3, c.V * 1.3, 170 + seed, 2)
        base = col(c1) * (0.8 + 0.45 * crumple[..., None])
        if not end:
            base = lay(base, c2, band(np.abs(c.U - 2.2), 0.0, 0.7, np.maximum(c.gU, 1e-3) * c.ss) * 0.9)
        shine = sstep(0.72, 0.9, crumple)
        return lay(base, "#ffffff", shine * 0.45)
    return f


def sock_mat(part):
    """The sock: white cotton gone a little grey, two stripes round its top (red and blue)."""
    def f(c):
        base = col("#ece6da") * (0.88 + 0.16 * fbm(c.U / 1.2, c.V / 1.2, 180 + part, 2)[..., None])
        if part == 0:
            g = np.maximum(c.gU, 1e-3) * c.ss
            base = lay(base, "#d63a32", band(c.U, 0.8, 1.6, g))
            base = lay(base, "#2f62b4", band(c.U, 2.2, 3.0, g))
        return base
    return f


def doors(st):
    """The driver's door's front part, where the camera sees it: the end of the armrest, the window crank, the lock knob
    on the sill, the pocket at the bottom with the owner's manual standing in it."""
    a0, a1 = M.DOOR_L["armrest"]
    st.box(0.0, 6.5, a0, a1, 6.0, 90.0, vinyl(TAN_D, 101, 0.06, 0.03), name="armrest")
    st.box(0.0, 6.0, a1 - 0.6, a1 + 1.4, 6.0, 90.0, vinyl("#d0aa7c", 102, 0.05, 0.03), name="armrest")
    p0, p1 = M.DOOR_L["pocket"]
    st.box(0.0, 3.2, p0, p0 + 1.2, 1.5, 70.0, vinyl(TAN_D, 103, 0.06, 0.03), name="pocket")          # the pocket's lip
    st.box(0.0, 3.6, p1 - 1.4, p1, 1.5, 70.0, vinyl(TAN_D, 104, 0.06, 0.03), name="pocket")
    st.box(0.6, 3.0, p0 + 1.2, p1 - 2.0, 7.0, 21.0, manual_mat, name="manual")                       # the owner's manual, standing in it
    # the window crank: its hub on the panel, the arm, the knob
    hub = P3(0.6, 64.5, 15.0)
    st.ball(hub, 1.4, plain(CHROME, 0.03, 4, 105), name="crank")
    knob = P3(2.6, 58.0, 12.0)
    st.stick(hub, P3(1.2, 58.6, 12.4), 0.55, plain(CHROME, 0.03, 4, 106), name="crank")
    st.stick(P3(1.2, 58.6, 12.4), knob, 0.85, plain("#2a2426", 0.03, 4, 107), name="crank")
    # the lock knob on the sill, at the door's front
    st.cyl((1.6, 9.0), 0.75, M.BELT - 0.5, M.BELT + 2.6, plain(CHROME, 0.03, 4, 108), axis="y", name="lock")


def manual_mat(c):
    """The owner's manual, standing in the pocket: a plain dark cover with a pale label on it (nothing to read), its
    spine up, worn pale at the middle (he reads his manuals to the middle)."""
    base = col("#3c3a4a") * (0.9 + 0.15 * fbm(c.Y / 2, c.Z / 2, 109, 2)[..., None])
    if c.face == "top":
        worn = np.exp(-((c.Z - 14.0) / 2.2) ** 2)
        base = lay(base, "#b8b2a8", worn * 0.8)
    if c.face == "right":
        g = np.maximum(c.gY, c.gZ) * c.ss
        base = lay(base, "#d8d0bc", rect(c.Z, c.Y, 10.0, 18.0, 40.0, 43.0, g) * 0.85)
    return base


# ---------------------------------------------------------------- overhead: the visors, the mirror, the freshener
def m_visor_under(c):
    """A sun visor's face: padded vinyl, pale, a stitched seam round it."""
    base = vinyl("#dcc29a", 111, 0.05, 0.03)(c)
    x0, x1, z0, z1 = c.box[0], c.box[1], c.box[4], c.box[5]
    d = np.minimum(np.minimum(c.X - x0, x1 - c.X), np.minimum(c.Z - z0, z1 - c.Z))
    g = np.maximum(c.gX, c.gZ) * c.ss
    base = base * (1 - 0.2 * band(d, 1.2, 1.45, g)[..., None])
    return base


def m_visor_back(c):
    """The driver's visor's back, seen once it is down: padded vinyl, an elastic strap across it, and under the strap the
    drawing Little Sister made for Dad's car and the car's registration card beside it."""
    U, V = c.U, c.V
    g = np.maximum(np.maximum(c.gU, c.gV), 1e-3) * c.ss
    base = vinyl("#dcc29c", 113, 0.05, 0.03)(c)
    w, h = M.VISOR_D["x"][1] - M.VISOR_D["x"][0], M.VISOR_D["depth"]
    d = np.minimum(np.minimum(U, w - U), np.minimum(V, h - V))
    base = base * (1 - 0.2 * band(d, 1.1, 1.35, g)[..., None])
    for name in ("registration", "drawing"):
        rgb, a = tex(name).sample(U, V)
        shade = 1 - 0.18 * band(V - VISOR_SHEETS[name][1], -0.6, 0.0, g)                      # a soft shadow along each sheet's top
        base = base * (1 - a[..., None]) + rgb * a[..., None]
        base = base * shade[..., None]
    s0, s1 = STRAP
    strap = band(V, s0, s1, g) * band(U, 1.0, w - 1.0, g)
    base = lay(base, "#8c6a46", strap * 0.92)
    base = base * (1 - 0.25 * band(V, s1, s1 + 0.4, g)[..., None])                               # its shadow on the sheets
    return base


def visors(st, driver="up"):
    """The two sun visors: the passenger's flat against the headliner, plain (no mirror on either). The driver's, a
    cut-out: up, flat against the headliner; or pulled down, hanging over the windshield's top left, showing its back
    (its strap, the drawing and the registration card under it are details)."""
    for which, v in (("driver", M.VISOR_D), ("passenger", M.VISOR_P)):
        x0, x1 = v["x"]
        hz, dpt, th = v["hinge_z"], v["depth"], v["thick"]
        grp = "visor" if which == "driver" else "back"
        rod = P3(x1 + 1.5, M.ROOF - th / 2 - 0.4, hz + 0.4)
        if which == "driver" and not driver:
            st.stick(P3(x1 + 1.5, M.ROOF, hz + 0.4), P3(x1 + 1.5, M.ROOF - 1.0, hz + 0.4), 0.5, plain(CHROME_D, 0.03, 4, 112), name="visor-hinge")
            continue
        if which == "driver" and driver == "down":
            a = math.radians(M.VISOR_DOWN)
            y_h = M.ROOF - th / 2 - 0.4
            back = lambda X, k: P3(X, y_h - dpt * k * math.sin(a), hz + dpt * k * math.cos(a))
            st.poly([back(x0, 0), back(x1, 0), back(x1, 1), back(x0, 1)], m_visor_back, name="visor", grp=grp)
            st.stick(back(x0 - 0.5, 0), back(x1 + 1.5, 0), 0.55, plain(CHROME_D, 0.03, 4, 114), name="visor", grp=grp)
            continue
        nm = "visor" if which == "driver" else "visor-p"
        st.box(x0, x1, M.ROOF - th - 0.2, M.ROOF - 0.2, hz, hz + dpt - th / 2, m_visor_under, name=nm, grp=grp)
        st.cyl((M.ROOF - th / 2 - 0.2, hz + dpt - th / 2), th / 2, x0, x1, vinyl("#dcc29a", 116, 0.04, 0.0), axis="x", name=nm, grp=grp)       # its padded edge
        st.stick(P3(x0 - 0.5, M.ROOF - th / 2 - 0.4, hz + 0.3), rod, 0.5, plain(CHROME_D, 0.03, 4, 115), name="visor" if which == "driver" else "visor-p", grp=grp)


def m_mirror_glass(c):
    """What the rearview mirror shows: the back of the car (the cargo floor's dark, the tailgate's top) and, filling
    most of it, the sky through the rear window, the car's tail being up."""
    U, V = c.U, c.V
    w, h = M.MIRROR["w"] - 1.6, M.MIRROR["h"] - 1.6
    gg = np.maximum(np.maximum(c.gU, c.gV), 1e-3) * c.ss
    skyc = lerp(col("#5a8cc8"), col("#8ab0dc"), np.clip(V / h, 0, 1)[..., None])
    win = rect(U, V, 2.0, w - 2.0, 1.4, h - 0.6, gg)
    base = lerp(col("#5c4636"), skyc, win[..., None])
    base = lay(base, "#d8e4ee", band(np.abs(U - V * 2.2 - w * 0.3), 0, 0.9, gg) * 0.35)        # a streak of light across the glass
    return base, base * 0.25


def mirror(st):
    m = M.MIRROR
    x0, x1 = m["x"] - m["w"] / 2, m["x"] + m["w"] / 2
    y0, y1 = m["y"] - m["h"] / 2, m["y"] + m["h"] / 2
    st.poly([P3(x, y, m["z"] - 0.4) for x, y in rounded(x0, x1, y0, y1, 1.8)], plain("#2c2729", 0.04, 6, 121), name="mirror")
    st.poly([P3(x, y, m["z"] - 2.4) for x, y in rounded(x0 + 0.4, x1 - 0.4, y0 + 0.4, y1 - 0.4, 1.6)], plain("#1e1b1d", 0.04, 6, 122), name="mirror")
    st.poly([P3(x0 + 0.8, y0 + 0.8, m["z"] - 0.2), P3(x1 - 0.8, y0 + 0.8, m["z"] - 0.2), P3(x1 - 0.8, y1 - 0.8, m["z"] - 0.2), P3(x0 + 0.8, y1 - 0.8, m["z"] - 0.2)],
            m_mirror_glass, name="mirror", flag=4)
    st.stick(P3(m["x"], y1 - 0.5, m["z"] - 1.6), P3(m["x"], M.ROOF, m["z"] - 2.4), 0.75, plain("#2c2729", 0.04, 4, 123), name="mirror")
    st.ball(P3(m["x"], M.ROOF - 0.6, m["z"] - 2.4), 1.6, plain("#2c2729", 0.04, 4, 124), name="mirror")


def m_freshener(c):
    """The air freshener: a little cardboard station wagon, red, wood down its side, two pale windows, two black wheels,
    'NEW CAR' on it in letters too small to read. Cut out round its own outline."""
    U, V = c.U, c.V
    w, h = M.FRESHENER["card"]
    gg = np.maximum(np.maximum(c.gU, c.gV), 1e-3) * c.ss
    u, v = U / w, V / h                                                                    # 0..1 across and up the card
    body = (v > 0.18) & (v < 0.62) & (u > 0.02) & (u < 0.98)
    cabin = (v >= 0.6) & (v < 0.97) & (u > 0.22) & (u < 0.9) & (v < 0.97 - np.clip(0.3 - u, 0, 1) * 3.0)
    wheels = (np.hypot((u - 0.24) * w, (v - 0.2) * h) < 0.6) | (np.hypot((u - 0.78) * w, (v - 0.2) * h) < 0.6)
    keep = body | cabin | wheels
    base = np.broadcast_to(col("#d93a2c"), U.shape + (3,)).copy()
    base = lay(base, "#a8693a", band(V, h * 0.25, h * 0.4, gg) * band(U, w * 0.05, w * 0.95, gg))        # the wood
    base = lay(base, "#d8ecf4", (band(U, w * 0.3, w * 0.52, gg) + band(U, w * 0.58, w * 0.84, gg)) * band(V, h * 0.66, h * 0.88, gg))
    base = lay(base, "#f8f0e0", band(V, h * 0.45, h * 0.52, gg) * band(U, w * 0.12, w * 0.7, gg) * 0.8)  # NEW CAR (too small to read)
    base = np.where(wheels[..., None], col("#1a1618"), base)
    return base, None, keep


def freshener(st):
    f = M.FRESHENER
    kx, ky, kz = f["knot"]
    w, h = f["card"]
    top = ky - f["drop"]
    st.stick(P3(kx, ky, kz), P3(kx, top - 0.2, kz), 0.1, plain("#4a3a30", 0.02, 4, 131), name="freshener", grp="freshener", min_px=0.7)   # a dark string, 1.4 px: it reads against the sky
    turn = math.radians(20.0)
    p = lambda du, dv: P3(kx + du * math.cos(turn), top - h + dv, kz + du * math.sin(turn))
    st.poly([p(-w / 2, 0), p(w / 2, 0), p(w / 2, h), p(-w / 2, h)], m_freshener, name="freshener", grp="freshener")


# ---------------------------------------------------------------- the slushie
def m_cup(c):
    """The Son's slushie: a tall paper cup, blue, a band of pale waves round it (no name on it)."""
    base = col("#2f62b4") * (0.92 + 0.12 * fbm(c.ang * 3, c.along / 2, 141, 2)[..., None])
    wave = np.sin(c.ang * 6.0 + c.along * 0.4)
    band_ = sstep(0.0, 0.4, c.along - 7.0 - wave * 0.8) * sstep(0.0, 0.4, 10.5 + wave * 0.8 - c.along)
    return lay(base, "#e6eef6", band_ * 0.9)


def slushie(st):
    """In its clip-on holder on the right-hand vent: the tall blue cup, its clear dome lid (the slush halfway down it
    seen through the lid's lower part), and a striped straw."""
    cu = M.CUP
    X, Y, Z = cu["at"]
    r0, r1 = cu["r"]
    y0, y1 = cu["y"]
    st.cyl((X, Z), r0, y0, y1, m_cup, axis="y", r1=r1, name="slushie")
    st.cyl((X, Z), r1 + 0.2, y1, y1 + 0.5, plain("#e8ecf0", 0.03, 4, 142), axis="y", name="slushie")                     # the lid's rim
    st.ball(P3(X, y1 + 0.4, Z), r1 * 0.92, plain("#c8d8e4", 0.04, 4, 143), name="slushie", squash=1.0)                     # the dome
    st.stick(P3(X + 0.6, y1 + 2.0, Z), P3(X + 1.8, y1 + 9.0, Z + 1.2), 0.32, straw_mat, name="slushie")
    # the holder: a ring round the cup and an arm up to the vent's louvers
    st.cyl((X, Z), r0 + 0.9, 70.5, 72.5, plain("#2a2628", 0.04, 4, 144), axis="y", name="holder")
    st.stick(P3(X - 2.0, 72.0, Z - 3.5), P3(X - 3.8, 79.0, M.DASH["z_face"] - 0.4), 0.5, plain("#2a2628", 0.04, 4, 145), name="holder")


def straw_mat(c):
    s = np.sin(c.along * 40.0 + c.side)
    return lerp(col("#f4f0ea"), col("#e03a32"), (s > 0)[..., None].astype(F32))


# ---------------------------------------------------------------- outside the glass: the hood, the cowl, the wipers
def m_hood(c):
    """The wagon's red hood, its top in the sun: the paint a little patchy with dust, a crease down its middle."""
    X, Z = c.X, c.Z
    base = col(RED) * (0.92 + 0.12 * fbm(X / 30, Z / 30, 151, 3)[..., None])
    dust = sstep(0.55, 0.85, fbm(X / 18, Z / 18, 152, 3))
    base = lay(base, "#e0a878", dust * 0.35)
    crease = band(np.abs(X - M.W / 2), 0.0, 0.6, c.gX * c.ss)
    return base * (1 + 0.12 * crease[..., None])


def outside(st):
    hd = M.HOOD
    st.box(hd["x"][0], hd["x"][1], hd["y"] - 12.0, hd["y"], hd["z_far"], -3.0, m_hood, name="hood")
    st.box(-4, M.W + 4, hd["y"] - 2, M.BELT - 0.5, -4.0, 0.2, plain("#2e2a2c", 0.05, 8, 153), name="cowl")
    for px in (44.0, 112.0):                                                              # the wipers, lying at the hood's foot
        st.stick(P3(px, hd["y"] + 1.2, -3.5), P3(px - 40.0, hd["y"] + 1.5, -2.6), 0.55, plain("#1e1c20", 0.04, 4, 154), name="wiper")
        st.stick(P3(px - 2.0, hd["y"] + 1.8, -2.4), P3(px - 44.0, hd["y"] + 2.0, -1.5), 0.35, plain("#141214", 0.04, 4, 155), name="wiper")
    occlude(st, -40, M.W + 40, 70.0, 125.0, -345.0, -300.0)                                # the mound ahead: its shadow on the hood's front


def build(st, glovebox_state="shut", visor_state="up", freshener_on=True, packets_on=True):
    """The whole car, in a given state of its cut-outs. glovebox_state: "shut", "map", "empty" (its door and the map)
    or None (no door: the backdrop, the compartment open with only the packets in it). visor_state: "up", "down" or None
    (no driver's visor: the backdrop)."""
    shell(st)
    dash(st, glove_open=glovebox_state != "shut")
    if glovebox_state is not None:
        glovebox(st, glovebox_state)
    if packets_on and glovebox_state != "shut":
        packets(st)
    wheel(st)
    bench(st)
    doors(st)
    visors(st, visor_state)
    mirror(st)
    if freshener_on:
        freshener(st)
    slushie(st)
    outside(st)

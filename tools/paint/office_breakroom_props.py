"""Everything that stands, hangs or lies in the break room, built in the room's own centimetres (office_breakroom.py):
the fridge and what is on it and on top of it, the counter and what is on it (the microwave, the dish rack, the sink,
Wendell's pie and its card, the coffee maker and its pot, the paper cups, the sugar), the wall cabinets and the paper
towels, the corkboard and its sheets, the clock, the snack machine, the couch and its afghan, Jed's chair, the table
in the near right and its two chairs, and the bin. OFFICE-17D.

Each function puts one group of things on the Stage, each with a paint that colours it in ITS OWN measurements.
Groups (`grp`) are the cut-outs: "pie", "schedule", "vending", "chair", "front" (and the states' own: see
office_breakroom_cuts.py); everything else is the backdrop ("back"). All measurements come from
office_breakroom_model.py. Every label is a plain word or a drawing of a thing: no brand, no logo, nobody's typeface."""

import math

import numpy as np

from brush import F32, lerp
import office_breakroom_model as M
from office_breakroom_kit import normals, col, mixc, vnoise, fbm, hashf, grad_of, lines_aa, band, rect, disc, lay, sstep, curve3, pen_mask
from office_breakroom_things import plain, wood, metal, chrome, rm, rect_uv, disc_uv, OUTSIDE, PAPER

VENEER = "#9a6c46"               # the cabinets' wood-grain veneer
LAMINATE = "#c9cab4"             # the counter's top: a pale grey-green, speckled
ALMOND = "#e8dec4"               # the fridge's enamel
COUCH = "#7a4e30"                # the couch: a nubby brown tweed
ORANGE = "#d8752e"               # Jed's plastic chair
AVOCADO = "#7f8c3e"              # the near table's other chair


def obox(st, c, size, ang, mat, name=None, grp="back", flag=0, shadow=True, faces=("left", "right", "top", "front", "back", "bottom")):
    """A box turned about the upright through its middle by `ang` degrees (positive turns its front toward +X).
    c: the middle of its foot (X, Y0, Z). size: (width along its own x, height, depth along its own z)."""
    w, h, dpt = size
    a = math.radians(ang)
    ux, uz = math.cos(a), -math.sin(a)
    vx, vz = math.sin(a), math.cos(a)
    X0, Y0, Z0 = c

    def P(sx, sy, sz):
        return (X0 + ux * sx + vx * sz, Y0 + sy, Z0 + uz * sx + vz * sz)
    hw, hd = w / 2, dpt / 2
    F = {
        "front": [P(-hw, 0, hd), P(hw, 0, hd), P(hw, h, hd), P(-hw, h, hd)],
        "back": [P(hw, 0, -hd), P(-hw, 0, -hd), P(-hw, h, -hd), P(hw, h, -hd)],
        "left": [P(-hw, 0, -hd), P(-hw, 0, hd), P(-hw, h, hd), P(-hw, h, -hd)],
        "right": [P(hw, 0, hd), P(hw, 0, -hd), P(hw, h, -hd), P(hw, h, hd)],
        "top": [P(-hw, h, hd), P(hw, h, hd), P(hw, h, -hd), P(-hw, h, -hd)],
        "bottom": [P(-hw, 0, -hd), P(hw, 0, -hd), P(hw, 0, hd), P(-hw, 0, hd)],
    }
    if shadow:
        pts = [p for f in F.values() for p in f]
        xs, ys, zs = zip(*pts)
        st.occ.append((min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))
    for k in faces:
        m = mat[k] if isinstance(mat, dict) else mat
        if m is None:
            continue
        st.poly(F[k], m, name, grp=grp, flag=flag)
    return P


# ---------------------------------------------------------------- the fridge
def fridge(st, G="back"):
    """A tall old fridge in almond enamel, the freezer door over the fridge door, long chrome handles at their right
    edges (it opens from the counter's side), a kick grille, magnets in every colour holding a takeout menu, and the
    sign: LABEL YOUR LUNCH. · MGMT. (its words are laid afterwards, crisp). On top, a box of plastic forks and a dusty
    plant whose runners hang down over the front corner."""
    x0, x1, y0, y1, z0, z1 = M.FRIDGE
    enamel = metal(ALMOND, 101, 0.06)
    st.box(x0, x1, y0 + 9, y1, z0, z1, enamel, "fridge", grp=G, foot=True)
    st.box(x0 + 3, x1 - 3, 0, 9, z0 + 2, z1 - 5, plain("#3a3632", 0.08, 3, 102), "fridge", grp=G)              # the kick grille's recess
    def m_kick(c):
        slot = (np.abs(((c.X - x0) % 2.4) - 1.2) < 0.55) & (c.Y > 2) & (c.Y < 7.5)
        return np.where(slot[..., None], col("#1e1c1a"), col("#5a5650"))
    st.poly([(x0 + 4, 1.5, z1 - 4.9), (x1 - 4, 1.5, z1 - 4.9), (x1 - 4, 8.5, z1 - 4.9), (x0 + 4, 8.5, z1 - 4.9)], m_kick, "fridge", grp=G, bias=0.1)
    # the two doors, a little proud of the body, with a dark gap between them
    fy = M.FREEZER_Y
    st.box(x0 + 0.6, x1 - 0.6, 10, fy - 0.8, z1, z1 + 3.2, enamel, "fridge", grp=G, shadow=False)
    st.box(x0 + 0.6, x1 - 0.6, fy + 0.8, y1 - 1.0, z1, z1 + 3.2, enamel, "fridge", grp=G, shadow=False)
    # the handles: long chrome bars on stand-offs at the right edge of each door
    hx = x1 - 6.0
    for (ha, hb) in ((60.0, 118.0), (136.0, 176.0)):
        st.stick((hx, ha, z1 + 6.4), (hx, hb, z1 + 6.4), 1.2, chrome("#c8ccce", 0.7, 103), "fridge", grp=G)
        for hy in (ha + 2, hb - 2):
            st.stick((hx, hy, z1 + 3.2), (hx, hy, z1 + 6.4), 0.8, chrome("#b8bcbe", 0.5, 104), "fridge", grp=G)
    # magnets: little discs and fruit in every colour; the takeout menu under two of them
    mx0, my0, mx1, my1 = M.MENU_ON_FRIDGE
    def m_menu(c):
        u, v = c.U, c.V
        k = col("#f6f2e6") * (0.95 + 0.05 * fbm(u / 3, v / 3, 105, 2))[..., None]
        head = (v > (my1 - my0) - 8) & (v < (my1 - my0) - 2)
        k = np.where(head[..., None], col("#c8302a"), k)
        burger = np.hypot((u - 14) / 7.0, (v - 22) / 4.0) < 1
        k = np.where(burger[..., None], col("#b8783a"), k)
        lines_ = (np.abs(((v - 3) % 2.6) - 1.3) < 0.45) & (v < 14) & (u > 3) & (u < 25)
        return np.where(lines_[..., None], col("#5a5a66"), k)
    st.poly([(mx0, my0, z1 + 3.4), (mx1, my0, z1 + 3.4), (mx1, my1, z1 + 3.4), (mx0, my1, z1 + 3.4)], m_menu, "fridgemenu", grp=G, bias=0.2)
    sx0, sy0, sx1, sy1 = M.SIGN
    st.poly([(sx0, sy0, z1 + 3.4), (sx1, sy0, z1 + 3.4), (sx1, sy1, z1 + 3.4), (sx0, sy1, z1 + 3.4)], plain(PAPER, 0.04, 6, 106), "fridgesign", grp=G, bias=0.2)
    for (u, v), cc in zip(((mx0 + 4, my1 - 3), (mx1 - 4, my1 - 3), (sx0 + 3, sy1 - 3), (sx1 - 3, sy1 - 3), (64, 40), (96, 52), (78, 30),
                           (60, 98), (104, 30), (90, 194 - 70), (110, 70)),
                          ("#d8302a", "#2f63b8", "#2fa673", "#f2b42e", "#e9772b", "#8e5ea8", "#d8302a", "#f2b42e", "#2fa673", "#c9375e", "#2f63b8")):
        st.disc3((u, v, z1 + 3.6), 1.7, (0, 0, 1), col(cc), sides=12, name="magnet", grp=G, bias=0.3)
    # the box of plastic forks on top, open, the forks' handles standing up white
    fx0, fx1, fy0, fy1, fz0, fz1 = M.FORKS
    st.box(fx0, fx1, fy0, fy1, fz0, fz1, wood("#c8a874", 107, "x", 0.12, 3.0, 20.0), "forks", grp=G)
    st.box(fx0 + 1, fx1 - 1, fy0 + 3, fy1, fz0 + 1, fz1 - 1, plain("#e8e4d8", 0.06, 4, 108), "forks", grp=G, inside=True)
    rng = np.random.default_rng(109)
    for i in range(16):
        px, pz = fx0 + 4 + rng.random() * (fx1 - fx0 - 8), fz0 + 4 + rng.random() * (fz1 - fz0 - 8)
        st.stick((px, fy1 - 4, pz), (px + rng.normal(0, 1.2), fy1 + 3.5 + rng.random() * 2, pz + rng.normal(0, 1.0)), 0.5, col("#f4f2ea"), "forks", grp=G)
    def m_label(c):
        k = col("#f4efe2")
        stripe = np.abs(c.V - 7.5) < 1.2
        return np.where(stripe[..., None], col("#2f63b8"), k)
    st.poly([(fx0 + 6, fy0 + 3, fz1 + 0.15), (fx1 - 6, fy0 + 3, fz1 + 0.15), (fx1 - 6, fy0 + 13, fz1 + 0.15), (fx0 + 6, fy0 + 13, fz1 + 0.15)],
            m_label, "forks", grp=G, bias=0.1)
    # the dusty plant: a plain pot, and leaves gone grey-green under the dust, runners hanging down the front corner
    px, ptop, pz, pr = M.PLANT
    st.cyl((px, pz), pr * 0.8, y1, ptop, plain("#c07a52", 0.1, 5, 110), r1=pr, name="plant", grp=G, cap=col("#4a3a2c"))
    leaf = col("#7d9466")
    def m_leaf(c):
        dust = np.clip((fbm(c.X / 1.5, c.Z / 1.5 + c.Y / 1.5, 111, 2) - 0.4) * 2, 0, 1)
        return lerp(leaf * (0.8 + 0.3 * fbm(c.X / 2, c.Y / 2, 112, 2))[..., None], col("#b8b8a4"), (dust * 0.45)[..., None])
    rng = np.random.default_rng(113)
    for i in range(9):
        a = rng.random() * 6.28
        st.ball((px + math.cos(a) * 4.5, ptop + 3 + rng.random() * 5, pz + math.sin(a) * 4.5), 3.0, m_leaf, "plant", grp=G, squash=(1.3, 0.55, 0.9))
    for run, (ex, ez) in enumerate(((x1 + 2, z1 + 1), (x1 - 4, z1 + 4))):
        pts = curve3([(px + 2, ptop + 2, pz + 3), ((px + ex) / 2 + 3, y1 + 4, (pz + ez) / 2 + 5), (ex, y1 - 6, ez), (ex - 1, y1 - 30 - run * 14, ez + 0.5)], 5)
        st.rope(pts, 0.35, col("#6a7a52"), name="plant", grp=G)
        for j in range(3, len(pts), 3):
            q = pts[j]
            st.ball((q[0] + 1.2, q[1], q[2] + 1.0), 1.9, m_leaf, "plant", grp=G, shadow=False, squash=(1.2, 0.9, 0.5))


def fridge_sign_quad():
    sx0, sy0, sx1, sy1 = M.SIGN
    z = M.FRIDGE[5] + 3.7
    return [(sx0, sy1, z), (sx1, sy1, z), (sx1, sy0, z), (sx0, sy0, z)]


# ---------------------------------------------------------------- the counter, and what is on it
def counter(st, G="back", pie_state="whole"):
    """Base cabinets in a wood-grain veneer with chrome pulls, a pale speckled laminate top with a steel edge, a
    backsplash of the same; the microwave at the left end by the fridge, the dish rack, the sink and its tap, Wendell's
    pie (a cut-out, in its states), the coffee maker with its pot, the paper cups and the sugar at the right end."""
    x0, x1, y0, y1, z0, z1 = M.COUNTER
    tt = M.TOP_T
    sx0, sx1, sz0, sz1, sdep = M.SINK

    def m_front(c):
        if c.face != "front":
            return col(VENEER) * 0.8 * (0.9 + 0.2 * fbm(c.Y / 20, c.Z / 20, 120, 2))[..., None]
        X, Y = c.X, c.Y
        g = c.fp
        k = col(VENEER) * (0.88 + 0.24 * fbm(X / 40, Y / 3.2, 121, 3))[..., None] * (0.94 + 0.12 * fbm(X / 3, Y / 60, 122, 2))[..., None]
        # the doors and drawers: a row of drawers under the top, doors under them, a gap between every one
        units = (x0, 186, 238, 290, 342, 394, 446, x1)
        for u in units[1:-1]:
            k = k * (1 - 0.55 * rm(X, u - 0.6, u + 0.6, g))[..., None]
        drawer = rm(Y, 70.0, 70.0 + 1.2, g)
        k = k * (1 - 0.5 * drawer)[..., None]
        # chrome pulls: a short bar on each drawer and near the top of each door
        for a, b in zip(units[:-1], units[1:]):
            mid = (a + b) / 2
            k = lay(k, "#d4d8da", rect_uv(X, Y, mid - 5, mid + 5, 76.5, 78.0, g))
            k = lay(k, "#d4d8da", rect_uv(X, Y, b - 7.5, b - 6.2, 52, 62, g) * (b < x1 - 1))
        kick = rm(Y, -1, 9.5, g)
        return lerp(k, col("#2a2420"), kick[..., None])
    st.box(x0, x1, 9.5, y1 - tt, z0, z1 - 1.0, m_front, "counter", grp=G, foot=True)
    st.box(x0, x1, 0, 9.5, z0, z1 - 7.0, plain("#2a2420", 0.08, 3, 123), "counter", grp=G)                  # the toe kick, set back

    def m_top(c):
        X, Z = c.X, c.Z
        k = col(LAMINATE) * (0.95 + 0.07 * fbm(X / 9, Z / 9, 124, 2))[..., None]
        fleck = fbm(X / 0.7, Z / 0.7, 125, 2)
        k = lay(k, "#8a8c78", np.clip((fleck - 0.7) * 5, 0, 1) * 0.5)
        k = lay(k, "#f0f0e0", np.clip((0.28 - fleck) * 5, 0, 1) * 0.5)
        ring = np.abs(np.hypot(X - 410, Z - 40) - 4.2) < 0.45                                  # a coffee ring, long dry
        return lay(k, "#9a8a6a", ring * 0.4)
    # the top in four pieces round the sink's hole
    for (a0, a1, b0, b1) in ((x0 - 1, sx0, z0, z1 + 2), (sx1, x1 + 1, z0, z1 + 2), (sx0, sx1, z0, sz0), (sx0, sx1, sz1, z1 + 2)):
        st.box(a0, a1, y1 - tt, y1, b0, b1, m_top, "countertop", grp=G)
    st.box(x0 - 1.2, x1 + 1.2, y1 - tt - 0.3, y1 - 0.2, z1 + 2, z1 + 2.8, chrome("#b8bcc0", 0.5, 126), "countertop", grp=G, shadow=False)
    st.box(x0, x1, y1, y1 + M.SPLASH, z0, z0 + 1.4, m_top, "splash", grp=G, shadow=False)                    # the backsplash
    # the sink: a steel basin let into the top, a drain, the tap
    def m_basin(c):
        k = col("#a8acae") * (0.85 + 0.25 * fbm(c.X / 2, c.Z / 2 + c.Y / 2, 127, 2))[..., None]
        drain = np.hypot(c.X - (sx0 + sx1) / 2, c.Z - (sz0 + sz1) / 2) < 2.4
        k = np.where((drain & (c.Y < y1 - sdep + 0.6))[..., None], col("#3a3c3e"), k)
        wet = np.clip((fbm(c.X / 4, c.Z / 4, 128, 2) - 0.55) * 3, 0, 1) * (c.Y < y1 - sdep + 0.6)
        return k, col("#ffffff")[None, :] * (wet * 0.18)[..., None]
    st.box(sx0, sx1, y1 - sdep, y1, sz0, sz1, m_basin, "sink", grp=G, inside=True)
    st.box(sx0 - 1.5, sx1 + 1.5, y1 - 0.2, y1 + 0.5, sz0 - 1.5, sz0, chrome("#c0c4c6", 0.6, 129), "sink", grp=G, shadow=False)
    st.box(sx0 - 1.5, sx1 + 1.5, y1 - 0.2, y1 + 0.5, sz1, sz1 + 1.5, chrome("#c0c4c6", 0.6, 130), "sink", grp=G, shadow=False)
    fxx, fzz = M.FAUCET
    tap = chrome("#ccd0d2", 0.8, 131)
    st.cyl((fxx, fzz + 1.5), 2.2, y1, y1 + 4, tap, name="faucet", grp=G, shadow=False)
    st.rope(curve3([(fxx, y1 + 3, fzz + 1.5), (fxx, y1 + 24, fzz + 2.5), (fxx, y1 + 29, fzz + 9), (fxx, y1 + 22, fzz + 15)], 6), 1.0, tap, name="faucet", grp=G)
    for dx in (-8.0, 8.0):
        st.cyl((fxx + dx, fzz + 1.8), 1.4, y1, y1 + 3.5, tap, name="faucet", grp=G, shadow=False)
        st.stick((fxx + dx, y1 + 3.5, fzz + 1.8), (fxx + dx * 1.3, y1 + 4.5, fzz + 4.5), 0.6, tap, "faucet", grp=G)
    microwave(st, G)
    rack(st, G)
    coffee(st, G)
    cups(st, G)
    pie(st, pie_state)


def microwave(st, G="back"):
    """An almond microwave with a smoked window and a panel of buttons: Ranger's step down from the fridge."""
    x0, x1, y0, y1, z0, z1 = M.MICRO
    st.box(x0, x1, y0 + 1.2, y1, z0, z1, metal("#ddd2b8", 140, 0.06), "micro", grp=G, foot=True)
    for fx in (x0 + 3, x1 - 3):
        for fz in (z0 + 4, z1 - 4):
            st.cyl((fx, fz), 1.4, y0, y0 + 1.3, col("#2a2826"), name="micro", grp=G, shadow=False)
    def m_face(c):
        u, v = c.U, c.V
        win = (u > 2.5) & (u < 37) & (v > 4) & (v < 27)
        k = col("#ddd2b8") * (0.95 + 0.05 * fbm(u / 4, v / 4, 141, 2))[..., None]
        glass = col("#2e2c2a") * (0.9 + 0.2 * np.clip(1 - (v - 4) / 23, 0, 1))[..., None]
        k = np.where(win[..., None], glass, k)
        panel = (u > 40) & (u < 56) & (v > 3) & (v < 28)
        k = np.where(panel[..., None], col("#c8bea6"), k)
        disp = (u > 42) & (u < 54) & (v > 22) & (v < 26)
        k = np.where(disp[..., None], col("#1e2a22"), k)
        keys = panel & (v > 6) & (v < 20) & (np.abs(((u - 42) % 3.0) - 1.5) < 0.9) & (np.abs(((v - 6) % 3.2) - 1.6) < 1.0)
        k = np.where(keys[..., None], col("#eee6d0"), k)
        handle = (u > 37.2) & (u < 39.2) & (v > 6) & (v < 25)
        k = np.where(handle[..., None], col("#8a8070"), k)
        shine = win & (np.abs((u + v * 0.6) - 18) < 1.6)
        e = np.where(shine[..., None], col("#ffffff") * 0.18, 0.0)
        dig = (u > 43) & (u < 53) & (v > 22.8) & (v < 25.2) & (np.abs(((u - 43) % 2.6) - 1.3) < 0.7)
        e = e + np.where(dig[..., None], col("#7ee0a0") * 0.55, 0.0)
        return k, e
    st.poly([(x0, y0 + 2, z1 + 0.2), (x1, y0 + 2, z1 + 0.2), (x1, y1 - 1, z1 + 0.2), (x0, y1 - 1, z1 + 0.2)], m_face, "micro", grp=G, bias=0.1)


def rack(st, G="back"):
    """A dish rack of white-coated wire: a plate standing in it, two mugs upside down on its pegs (a red one, a blue
    one), a spoon."""
    x0, x1, y0, y1, z0, z1 = M.RACK
    wire = col("#ecece4")
    st.box(x0, x1, y0, y0 + 1.6, z0, z1, plain("#d8dcd0", 0.05, 4, 142), "rack", grp=G, shadow=False)          # the drip tray
    for x in np.linspace(x0 + 1, x1 - 1, 7):
        st.stick((x, y0 + 2, z0 + 1), (x, y0 + 12, z0 + 1), 0.28, wire, "rack", grp=G)
        st.stick((x, y0 + 2, z1 - 1), (x, y0 + 9, z1 - 1), 0.28, wire, "rack", grp=G)
    for y in (y0 + 2.5, y0 + 8.5):
        st.stick((x0 + 1, y, z1 - 1), (x1 - 1, y, z1 - 1), 0.28, wire, "rack", grp=G)
        st.stick((x0 + 1, y + 3, z0 + 1), (x1 - 1, y + 3, z0 + 1), 0.28, wire, "rack", grp=G)
    st.disc3((x0 + 9, y0 + 11.5, (z0 + z1) / 2 - 4), 10.0, (1, 0.05, 0.1), plain("#f2f0e8", 0.04, 4, 143), sides=24, name="rack", grp=G)
    for (mx, mz, mc) in ((x0 + 22, z0 + 12, "#c8402e"), (x0 + 30, z1 - 12, "#3a6ab8")):
        st.cyl((mx, mz), 3.9, y0 + 2, y0 + 11.5, plain(mc, 0.1, 3, 144), name="rack", grp=G, cap=col(mc) * 0.7)
        st.rope(curve3([(mx + 3.8, y0 + 4, mz), (mx + 6.2, y0 + 6.5, mz), (mx + 3.8, y0 + 9.5, mz)], 4), 0.7, col(mc), name="rack", grp=G)


def coffee(st, G="back"):
    """A drip coffee maker in black plastic: the tower at the back with the hood over the pot, the warmer plate, the
    glass pot full of coffee (its steam is the engine's: layout.json `fx`), and a small lamp lit at its foot."""
    x0, x1, y0, y1, z0, z1 = M.COFFEE
    black = plain("#2c2a28", 0.08, 4, 150)
    st.box(x0, x1, y0, y0 + 3.0, z0, z1, black, "coffee", grp=G, foot=True)                                 # the base
    st.box(x0, x1, y0 + 3.0, y1, z0, z0 + 11, black, "coffee", grp=G)                                       # the tower
    st.box(x0, x1, y1 - 7, y1, z0 + 11, z1 - 2, black, "coffee", grp=G)                                     # the hood
    st.ball((x1 - 3.5, y0 + 1.6, z1 + 0.2), 0.7, col("#ff8a3a"), "coffee", grp=G, shadow=False, emi=col("#ff9a4a") * 1.2)
    px, pz, pr, pf, ptop = M.POT
    def m_pot(c):
        # glass, the coffee in it nearly to the top: dark, warm at its edges where the light comes through
        level = c.Y < ptop - 3.0
        n = normals(c)
        edge = np.clip(1 - np.abs(n[:, 2]) * 1.1, 0, 1)
        coffee_ = lerp(col("#2a1408"), col("#7a3e14"), (edge * 0.7)[:, None])
        k = np.where(level[:, None], coffee_, col("#c8d0cc") * 0.55)
        streak = np.clip(1 - np.abs(np.arctan2(n[:, 0], n[:, 2]) + 0.5) * 3.5, 0, 1)
        return k, col("#ffffff")[None, :] * (streak * 0.45)[:, None]
    st.cyl((px, pz), pr * 0.92, pf, ptop - 4, m_pot, r1=pr, name="pot", grp=G)
    st.cyl((px, pz), pr * 0.86, ptop - 4, ptop, m_pot, name="pot", grp=G, hollow=False, cap=col("#2a1408"))
    st.cyl((px, pz), pr * 0.9, ptop - 0.6, ptop + 0.6, plain("#1e1c1a", 0.05), name="pot", grp=G, shadow=False)
    st.rope(curve3([(px + pr * 0.9, ptop - 2, pz), (px + pr + 4.5, ptop - 4, pz), (px + pr + 4.5, pf + 6, pz), (px + pr * 0.9, pf + 4, pz)], 4), 1.1,
            col("#1e1c1a"), name="pot", grp=G)


def cups(st, G="back"):
    """A stack of paper cups, white with a pale blue band, upside down; and the sugar, in a glass shaker with a steel
    top."""
    x, z, r, y0, y1 = M.CUPS
    def m_cups(c):
        Y = c.Y
        lip = ((Y - y0) % 2.0) < 0.4
        k = np.where(lip[..., None] if lip.ndim == 1 else lip, col("#d8d8d0"), col("#f4f2ea"))
        bandd = (Y > y1 - 9) & (Y < y1 - 6)
        k = np.where(bandd[..., None], col("#8ab0d0"), k)
        return k
    st.cyl((x, z), r, y0, y1, m_cups, r1=r * 0.82, name="cups", grp=G, cap=col("#ecece4"))
    sx, sz, sr, sy0, sy1 = M.SUGAR
    def m_glass(c):
        lvl = c.Y < sy1 - 6
        k = np.where(lvl[:, None], col("#f2f0e8"), col("#b8c0bc") * 0.6)
        n = normals(c)
        streak = np.clip(1 - np.abs(np.arctan2(n[:, 0], n[:, 2]) + 0.4) * 4, 0, 1)
        return k, col("#ffffff")[None, :] * (streak * 0.4)[:, None]
    st.cyl((sx, sz), sr, sy0, sy1 - 4, m_glass, name="sugar", grp=G)
    st.cyl((sx, sz), sr * 0.95, sy1 - 4, sy1, chrome("#c8ccce", 0.6, 151), r1=sr * 0.55, name="sugar", grp=G, cap=col("#d8dcde"))


# ---------------------------------------------------------------- Wendell's pie, in its three states
def pie(st, state="whole", G="pie"):
    """A whole cherry pie with a lattice top in a tin with a crimped rim, and the card stood against the tin
    (state "whole"); the empty tin, sticky, crumbs in it and a bottle cap set in its middle, the card still standing
    ("eaten"); the card fallen flat where it stood, the bottle cap left on it, a sticky ring where the tin was ("gone").
    The card's words are laid afterwards (office_breakroom.words)."""
    X, Z, R = M.PIE
    y = M.COUNTER[3]
    tin_h = M.PIE_TIN_H

    def m_tin(c):
        n = normals(c)
        up = np.clip(n[:, 1] * 0.6 + n[:, 2] * 0.5, 0, 1)
        k = col("#c4c8cc")[None, :] * (0.62 + 0.5 * up)[:, None]
        flute = 0.5 + 0.5 * np.cos(c.ang * 64)
        k = k * (0.88 + 0.14 * flute)[:, None]
        if state == "eaten":                                                     # OFFICE-17D (resumed): the inside of the far wall
            inner = (np.asarray(c.kind) == 2)                                    # (the part of the inside that shows) sticky with filling
            smear = np.clip((fbm(c.X / 1.3, c.Y / 0.8 + c.Z / 1.3, 169, 3) - 0.42) * 3.0, 0, 1) * inner
            k = lerp(k, col("#6e1822"), (smear * 0.85)[:, None])
        return k, col("#f4f8ec")[None, :] * (np.clip(up - 0.72, 0, 1) * 0.8)[:, None]
    if state in ("whole", "eaten"):
        st.cyl((X, Z), R - 1.6, y, y + tin_h, m_tin, r1=R, name="pietin", grp=G, foot=True, hollow=(state == "eaten"), cap=col("#b8bcc0"))
        # the crimped rim: a ring of little ridges round the top
        def m_crimp(c):
            r_ = 0.5 + 0.5 * np.cos(c.ang * 72)
            k = col("#d4d8dc") * (0.75 + 0.35 * r_)[..., None]
            return k, col("#f4f8ec")[None, :] * (r_ * 0.12)[..., None]
        st.cyl((X, Z), R + 1.3, y + tin_h - 0.4, y + tin_h + 0.25, m_crimp, name="pietin", grp=G, shadow=False,
               hollow=(state == "eaten"))                                       # OFFICE-17D (resumed): a ring, not a lid, once the pie is gone
    if state == "whole":
        # the crust's fluted edge, then the lattice dome with the cherries showing between its strips
        def m_edge(c):
            f = 0.5 + 0.5 * np.cos(c.ang * 22)
            k = lerp(col("#c88a46"), col("#e8b866"), f[..., None])
            return k * (0.9 + 0.15 * fbm(c.X / 1.2, c.Z / 1.2, 160, 2))[..., None]
        st.cyl((X, Z), R - 0.6, y + tin_h, y + tin_h + 1.6, m_edge, r1=R - 1.6, name="piecrust", grp=G, shadow=False, cap=col("#d8a056"))

        def m_dome(c):
            u, v = c.X - X, c.Z - Z
            a = math.radians(18)
            s, t = u * math.cos(a) + v * math.sin(a), -u * math.sin(a) + v * math.cos(a)
            sa = np.abs(((s + 1.0) % 4.4) - 2.2) < 1.15
            sb = np.abs(((t + 0.4) % 4.4) - 2.2) < 1.15
            crust = sa | sb
            cherry = col("#a8222c") * (0.75 + 0.45 * fbm(u / 1.1, v / 1.1, 161, 2))[..., None]
            gloss = np.clip((fbm(u / 0.8, v / 0.8, 162, 2) - 0.62) * 4, 0, 1)
            cherry = lerp(cherry, col("#e05a5a"), (gloss * 0.6)[..., None])
            gold = lerp(col("#d89a4e"), col("#f0c878"), np.clip(fbm(u / 1.5, v / 1.5, 163, 2) * 1.3 - 0.2, 0, 1)[..., None])
            cross = sa & sb
            gold = np.where(cross[..., None], gold * 0.86, gold)
            k = np.where(crust[..., None], gold, cherry)
            return k
        st.ball((X, y + tin_h + 0.6, Z), R - 1.8, m_dome, "piecrust", grp=G, shadow=False, squash=(1.0, M.PIE_DOME / (R - 1.8), 1.0))
        # a drip of the filling over the edge, toward us
        st.ball((X + 3, y + tin_h + 0.4, Z + R - 1.4), 1.3, col("#9a1e28"), "piecrust", grp=G, shadow=False, squash=(1.0, 0.6, 0.7))
    if state == "eaten":
        def m_inside(c):
            k = col("#b8bcc0") * (0.8 + 0.3 * fbm(c.X / 2, c.Z / 2, 164, 2))[..., None]
            smear = np.clip((fbm(c.X / 1.6, c.Z / 1.6, 165, 3) - 0.55) * 3.5, 0, 1)
            k = lerp(k, col("#7a1a22"), (smear * 0.75)[..., None])
            crumbs = (fbm(c.X / 0.5, c.Z / 0.5, 166, 2) > 0.8)
            return np.where(crumbs[..., None], col("#d8a056"), k)
        st.cyl((X, Z), R - 1.7, y + 0.3, y + 0.5, m_inside, name="pietin", grp=G, shadow=False)
        # the cap set in the middle on the last sticky lump of filling, a little back of the tin's centre: from this eye
        # the tin's near side hides its floor for about 19 cm, so set any lower or nearer, the cap would not show at all.
        # OFFICE-17D (resumed): stood up in the lump on its edge, its crown to the room, leaning back: lying flat, it was a
        # sliver under one pixel and did not show at all; stood so, it is a red disc about four pixels across.
        st.ball((X + 0.5, y + 0.5, Z - 6.0), 3.0, col("#7a1a22"), "pietin", grp=G, shadow=False, squash=(1.0, 0.3, 0.8))
        bottlecap(st, (X + 0.5, y + 0.1 + CAP_R * math.cos(math.radians(35.0)), Z - 6.0), G, lean=35.0)
    if state in ("whole", "eaten"):
        card(st, G)
    else:
        card(st, G, flat=True)
        # the cap left on the card where the pie was, propped on its bent skirt, its crown leaning back toward the wall
        bottlecap(st, (CARD_FLAT["x"] + 9.0, y + 0.25 + CAP_R * math.cos(math.radians(55.0)), CARD_FLAT["z"] + 3.0), G, lean=55.0)


CARD_FLAT = dict(x=352.0, z=24.0)                         # where the card lies once the tin is gone (its corner nearest the wall)


def card(st, G="pie", flat=False):
    """The birthday card: folded, standing behind the tin a little to the right, leaning back toward the wall; or
    fallen flat on the counter once the tin is taken."""
    c = M.CARD
    y = M.COUNTER[3]
    w, h = c["w"], c["h"]
    def m_card(cc):
        k = col("#f6f0de") * (0.95 + 0.05 * fbm(cc.U / 3, cc.V / 3, 167, 2))[..., None]
        edge = (cc.U < 0.8) | (cc.U > w - 0.8)
        return np.where(edge[..., None], col("#e8dcc4"), k)
    if not flat:
        a = math.radians(c["lean"])
        x0 = c["x"] + 6.0
        zf = c["z"] + 1.0
        st.poly([(x0, y, zf), (x0 + w, y, zf - 4.0), (x0 + w, y + h * math.cos(a), zf - 4.0 - h * math.sin(a)), (x0, y + h * math.cos(a), zf - h * math.sin(a))],
                m_card, "card", grp=G, shadow=True)
    else:
        fx, fz = CARD_FLAT["x"], CARD_FLAT["z"]
        def m_white(cc):
            return col("#fffcf2") * (0.97 + 0.03 * fbm(cc.U / 3, cc.V / 3, 168, 2))[..., None]
        st.poly([(fx - 0.6, y + 0.06, fz - 0.4), (fx + w + 0.6, y + 0.06, fz - 3.4), (fx + w + 2.8, y + 0.06, fz - 2.4 + h * 0.98),
                 (fx + 1.6, y + 0.06, fz + 0.6 + h * 0.98)], col("#5a5a50"), "card", grp=G, bias=0.03)          # its shadow round its edge
        st.poly([(fx, y + 0.14, fz), (fx + w, y + 0.14, fz - 3.0), (fx + w + 2.2, y + 0.14, fz - 3.0 + h * 0.98), (fx + 2.2, y + 0.14, fz + h * 0.98)],
                m_white, "card", grp=G, bias=0.06)


def card_quad(flat=False):
    """The card's face as a quad for its words: top left, top right, bottom right, bottom left (cm in the room)."""
    c = M.CARD
    y = M.COUNTER[3]
    w, h = c["w"], c["h"]
    if not flat:
        a = math.radians(c["lean"])
        x0, zf = c["x"] + 6.0, c["z"] + 1.0
        lift = 0.25
        return [(x0, y + h * math.cos(a), zf - h * math.sin(a) + lift), (x0 + w, y + h * math.cos(a), zf - 4.0 - h * math.sin(a) + lift),
                (x0 + w, y, zf - 4.0 + lift), (x0, y, zf + lift)]
    fx, fz = CARD_FLAT["x"], CARD_FLAT["z"]
    return [(fx, y + 0.3, fz), (fx + w, y + 0.3, fz - 3.0), (fx + w + 2.2, y + 0.3, fz - 3.0 + h * 0.98), (fx + 2.2, y + 0.3, fz + h * 0.98)]


CAP_R = 2.4                                               # the cap's radius (larger than life, as the pie is: so that it reads)


def bottlecap(st, at, G="pie", lean=35.0, turn=4.0):
    """Ranger's best bottle cap: red, a pale ring pressed round its crown, its crimped skirt darker; a glint on it.
    OFFICE-17D (resumed): it is stood on its edge with its crown to the room, leaning back `lean` degrees from upright and
    turned `turn` degrees to the right, `at` the middle of its crown: from this eye (2 m up, 6 m off) a cap lying flat
    is under a pixel high, and stood so it is a red disc about four pixels across."""
    x, y, z = at
    a, b = math.radians(lean), math.radians(turn)
    n = (math.sin(b) * math.cos(a), math.sin(a), math.cos(b) * math.cos(a))      # its crown's normal: toward us, tipped up

    def m_crown(c):
        r = np.sqrt(c.U ** 2 + c.V ** 2)
        k = np.broadcast_to(col("#d8342c"), r.shape + (3,)).copy()
        ring = np.clip(1 - np.abs(r - 1.70) / 0.30, 0, 1)                            # the ring pressed round the crown
        k = lerp(k, col("#f0b4a0"), (ring * 0.65)[:, None])
        crimp = 0.5 + 0.5 * np.cos(np.arctan2(c.V, c.U) * 21)
        skirt = (r > 2.05)[:, None]
        k = np.where(skirt, col("#9a201c")[None, :] * (0.8 + 0.3 * crimp)[:, None], k)
        glint = np.exp(-((c.U + 0.85) ** 2 + (c.V - 0.85) ** 2) / 0.30)           # its glint, up on the left
        return k, col("#fff4ec")[None, :] * (glint * 0.9)[:, None]
    back = (x - n[0] * 0.45, y - n[1] * 0.45, z - n[2] * 0.45)
    st.disc3(back, CAP_R + 0.15, n, col("#6a1414"), sides=20, name="bottlecap", grp=G)        # the skirt's depth, behind the crown
    st.disc3((x, y, z), CAP_R, n, m_crown, sides=20, name="bottlecap", grp=G)


# ---------------------------------------------------------------- the wall cabinets and the paper towels
def cabinets(st, G="back"):
    x0, x1, y0, y1, z0, z1 = M.CABINETS
    def m_cab(c):
        if c.face != "front":
            return col(VENEER) * 0.85 * (0.9 + 0.2 * fbm(c.X / 20, c.Y / 20 + c.Z / 20, 170, 2))[..., None]
        X, Y = c.X, c.Y
        g = c.fp
        k = col(VENEER) * (0.88 + 0.24 * fbm(X / 40, Y / 3.2, 171, 3))[..., None] * (0.94 + 0.12 * fbm(X / 3, Y / 60, 172, 2))[..., None]
        for u in (x0 + (x1 - x0) * f for f in (0.25, 0.5, 0.75)):
            k = k * (1 - 0.55 * rm(X, u - 0.6, u + 0.6, g))[..., None]
        for i, u in enumerate((x0 + (x1 - x0) * f for f in (0.25, 0.5, 0.75, 1.0))):
            pull = u - (x1 - x0) * 0.25 + 4 if i % 2 else u - 6
            k = lay(k, "#d4d8da", rect_uv(X, Y, pull, pull + 1.4, y0 + 4, y0 + 13, g))
        return k
    st.box(x0, x1, y0, y1, z0, z1, m_cab, "cabinets", grp=G)
    tx0, tx1, ty, tz, tr = M.TOWELS
    st.stick((tx0 - 2, ty, tz), (tx1 + 2, ty, tz), 0.6, chrome("#b8bcbe", 0.5, 173), "towels", grp=G)
    for tx in (tx0 - 2, tx1 + 2):
        st.stick((tx, y0, tz), (tx, ty, tz), 0.5, chrome("#b8bcbe", 0.5, 174), "towels", grp=G)
    def m_roll(c):
        return col("#f2f0e6") * (0.92 + 0.1 * (0.5 + 0.5 * np.cos(c.ang * 3)))[..., None]
    st.cyl((ty, tz), tr, tx0 + 1, tx1 - 1, m_roll, axis="x", name="towels", grp=G, cap=col("#d8d4c4"))
    st.poly([(tx0 + 14, ty - tr + 0.3, tz + tr - 0.5), (tx1 - 16, ty - tr + 0.3, tz + tr - 0.5), (tx1 - 17, ty - tr - 9, tz + tr + 0.6), (tx0 + 15, ty - tr - 9, tz + tr + 0.6)],
            plain("#f4f2e8", 0.04, 4, 175), "towels", grp=G)                                    # the sheet hanging down


# ---------------------------------------------------------------- the corkboard
def board(st, G="back"):
    """The corkboard over the counter, at a raccoon's eye from the counter's top: FORM 7 IS NOT OPTIONAL (a printed
    notice), FOUND: ONE ROMAN SANDAL (1951) · SEE OPAL (an index card gone yellow, pinned with too many pins), the
    bowling league's sheet, a menu from somewhere that delivers; and where the test schedule hangs (a cut-out of its
    own: `schedule`), one pin with a torn corner of paper under it, for when it has gone."""
    x0, x1, y0, y1 = M.BOARD
    w, h = x1 - x0, y1 - y0
    S = M.SHEETS

    def m_board(c):
        u, v = c.X - x0, c.Y - y0
        if c.face != "front":
            return col("#6a4a30")
        g = c.fp
        out = col("#b88a52") * (0.82 + 0.34 * fbm(u / 0.9, v / 0.9, 180, 2))[..., None]
        out = lay(out, "#8a5e34", np.clip((fbm(u / 0.5, v / 0.5, 181, 2) - 0.7) * 4, 0, 1) * 0.5)
        for i, name in enumerate(("form7", "found", "bowling", "menu")):
            pu, pv, pw, ph = S[name]
            lean = {"form7": 0.012, "found": -0.035, "bowling": 0.02, "menu": -0.05}[name]
            uu = u - pu - (v - pv) * lean
            vv = v - pv + (u - pu) * lean
            m = rect_uv(uu, vv, 0, pw, 0, ph, g)
            base = {"form7": "#f6f4ec", "found": "#e8d8a0", "bowling": "#f2eee0", "menu": "#f8f0e0"}[name]
            sheet = np.zeros(u.shape + (3,), dtype=F32) + col(base)
            if name == "found":                                                        # an index card: its red top rule and blue lines
                sheet = np.where((np.abs(vv - (ph - 4.5)) < 0.35)[..., None], col("#c86060"), sheet)
                ln = (np.abs(((vv - 2) % 2.6) - 1.3) < 0.18) & (vv < ph - 6)
                sheet = np.where(ln[..., None], col("#9ab0c8"), sheet)
                sheet = lerp(sheet, col("#c8a860"), (np.clip((fbm(uu / 4, vv / 4, 182, 2) - 0.5) * 2, 0, 1) * 0.35)[..., None])
            if name == "bowling":                                                      # a ball and three pins drawn at the top; a grid of scores
                ball = np.hypot(uu - 7, vv - (ph - 7)) < 3.2
                sheet = np.where(ball[..., None], col("#2a2a3a"), sheet)
                for k_ in range(3):
                    pin = (np.abs(uu - (16 + k_ * 3.4)) < 1.0) & (np.abs(vv - (ph - 7)) < 3.4)
                    sheet = np.where(pin[..., None], col("#f8f6f0") * 0.85, sheet)
                    sheet = np.where((pin & (np.abs(vv - (ph - 6)) < 0.5))[..., None], col("#c8302a"), sheet)
                gr = ((np.abs(((uu - 2) % 5.6) - 2.8) > 2.55) | (np.abs(((vv - 2) % 3.0) - 1.5) > 1.32)) & (vv < ph - 13) & (vv > 2) & (uu > 2) & (uu < pw - 2)
                sheet = np.where(gr[..., None], col("#6a6a7a"), sheet)
            if name == "menu":                                                         # a drawing of a cheeseburger, and prices
                bun = np.hypot((uu - pw / 2) / 4.2, (vv - (ph - 7)) / 2.4) < 1
                sheet = np.where(bun[..., None], col("#c8843a"), sheet)
                cheese = (np.abs(vv - (ph - 7.4)) < 0.5) & (np.abs(uu - pw / 2) < 4.6)
                sheet = np.where(cheese[..., None], col("#f2c02e"), sheet)
                ln = (np.abs(((vv - 2) % 2.4) - 1.2) < 0.4) & (vv < ph - 12) & (uu > 1.5) & (uu < pw - 1.5)
                sheet = np.where(ln[..., None], col("#5a5a66"), sheet)
            sheet = sheet * (0.95 + 0.06 * fbm(uu / 5, vv / 5, 183 + i, 2))[..., None]
            shd = rect_uv(uu - 0.6, vv + 0.6, 0, pw, 0, ph, g)
            out = out * (1 - 0.3 * np.clip(shd - m, 0, 1)[..., None])
            out = out * (1 - m[..., None]) + sheet * m[..., None]
            pins = {"form7": ((pw / 2, ph - 1.6),), "found": ((2, ph - 2), (pw - 2, ph - 2), (2, 2), (pw - 2, 2), (pw / 2, ph - 1.5), (pw / 2, 1.8)),
                    "bowling": ((pw / 2, ph - 1.6),), "menu": ((pw / 2, ph - 1.5),)}[name]
            for j, (qu, qv) in enumerate(pins):
                out = lay(out, ("#d83a2c", "#2c64c8", "#e8c030", "#2fa673")[(i + j) % 4], disc_uv(uu, vv, qu, qv, 0.95, g))
        # where the schedule hangs: a pin, and under it a torn corner of paper (seen once the sheet has gone)
        pu, pv, pw, ph = S["schedule"]
        out = lay(out, "#f6f4ec", np.clip((1.6 - np.abs(u - (pu + pw / 2)) * 0.5 - (pv + ph - v)) / 1.0, 0, 1) * (v < pv + ph) * (v > pv + ph - 2.2))
        out = lay(out, "#e8c030", disc_uv(u, v, pu + pw / 2, pv + ph - 1.6, 0.95, g))
        fr = 1 - rect_uv(u, v, 2.4, w - 2.4, 2.4, h - 2.4, g)
        frame = col("#7a5232") * (0.85 + 0.3 * fbm(u / 2.0 + v / 30, v / 2.0 + u / 30, 184, 2))[..., None]
        return out * (1 - fr[..., None]) + frame * fr[..., None]
    st.box(x0, x1, y0, y1, 0, M.BOARD_T, m_board, "board", grp=G)


def schedule(st, G="schedule"):
    """The test schedule: a typed sheet, a little crooked, its one pin at the top; its heading LAMPLIGHTER · TEST
    SCHEDULE and the lines under it are laid afterwards (too small to read in the picture: the thing's own picture
    and the lines say what it says)."""
    x0, x1, y0, y1 = M.BOARD
    pu, pv, pw, ph = M.SHEETS["schedule"]
    z = M.BOARD_T + 0.25
    a = math.radians(-2.0)

    def at(u, v):
        uu, vv = u - pw / 2, v - ph
        return (x0 + pu + pw / 2 + uu * math.cos(a) - vv * math.sin(a), y0 + pv + ph + uu * math.sin(a) + vv * math.cos(a), z)
    def m_sheet(c):
        return col("#f8f6ee") * (0.96 + 0.04 * fbm(c.U / 4, c.V / 4, 190, 2))[..., None]
    st.poly([at(0, 0), at(pw, 0), at(pw, ph), at(0, ph)], m_sheet, "schedule", grp=G, bias=0.15)
    st.ball(at(pw / 2, ph - 1.6)[:2] + (z + 0.6,), 0.95, col("#e8c030"), "schedule", grp=G, shadow=False)


def schedule_quad():
    """The schedule's face: top left, top right, bottom right, bottom left (for its typing)."""
    x0, x1, y0, y1 = M.BOARD
    pu, pv, pw, ph = M.SHEETS["schedule"]
    z = M.BOARD_T + 0.5
    a = math.radians(-2.0)

    def at(u, v):
        uu, vv = u - pw / 2, v - ph
        return (x0 + pu + pw / 2 + uu * math.cos(a) - vv * math.sin(a), y0 + pv + ph + uu * math.sin(a) + vv * math.cos(a), z)
    return [at(0, ph), at(pw, ph), at(pw, 0), at(0, 0)]


def sheet_quad(name, lift=0.4):
    x0, x1, y0, y1 = M.BOARD
    pu, pv, pw, ph = M.SHEETS[name]
    lean = {"form7": 0.012, "found": -0.035, "bowling": 0.02, "menu": -0.05}.get(name, 0.0)
    z = M.BOARD_T + lift

    def at(u, v):                                                                              # the inverse of the board's lean
        return (x0 + pu + u + v * lean / (1 + lean * lean), y0 + pv + v - u * lean / (1 + lean * lean), z)
    return [at(0, ph), at(pw, ph), at(pw, 0), at(0, 0)]


# ---------------------------------------------------------------- the clock
def clock(st, G="back", hand=None):
    """A plain round wall clock, a black rim and a white face, twelve marks, the hour and minute hands at ten to two;
    its red second hand is drawn by itself in its frames (`hand`: the second, 0 to 59; None: no second hand)."""
    X, Y, R = M.CLOCK
    st.cyl((X, Y), R, 0, 3.6, plain("#22201e", 0.06, 3, 200), axis="z", name="clock", grp=G, cap=col("#2a2826"))
    def m_face(c):
        U, V = c.U, c.V
        k = col("#f4f2e8") * (0.96 + 0.04 * fbm(U / 3, V / 3, 201, 2))[..., None]
        r = np.hypot(U, V)
        ang = np.degrees(np.arctan2(U, V)) % 360
        tick = (r > R * 0.72) & (r < R * 0.86) & ((np.abs(((ang + 15) % 30) - 15) < 2.2))
        k = np.where(tick[..., None], col("#22201e"), k)
        mins = (r > R * 0.80) & (r < R * 0.86) & ((np.abs(((ang + 3) % 6) - 3) < 0.7))
        return np.where(mins[..., None], col("#6a6866"), k)
    st.disc3((X, Y, 3.7), R * 0.9, (0, 0, 1), m_face, sides=40, name="clock", grp=G, bias=0.1)
    hh, mm = M.CLOCK_TIME
    ma = math.radians(mm * 6)
    ha = math.radians((hh % 12) * 30 + mm * 0.5)
    for a_, L, wdt in ((ha, R * 0.48, 0.75), (ma, R * 0.74, 0.55)):
        st.stick((X - math.sin(a_) * 1.5, Y - math.cos(a_) * 1.5, 4.0), (X + math.sin(a_) * L, Y + math.cos(a_) * L, 4.0), wdt, col("#1a1816"), "clockhands", grp=G, shade=False)
    st.cyl((X, Y), 0.9, 3.8, 4.6, col("#1a1816"), axis="z", name="clockhands", grp=G, shadow=False)
    if hand is not None:
        sa = math.radians(hand * 6)
        st.stick((X - math.sin(sa) * 2.4, Y - math.cos(sa) * 2.4, 4.7), (X + math.sin(sa) * R * 0.82, Y + math.cos(sa) * R * 0.82, 4.7), 0.32,
                 col("#d02a24"), "secondhand", grp="secondhand", shade=False, min_px=0.5)


# ---------------------------------------------------------------- the snack machine
SNACKS = ["#d8302a", "#f2b42e", "#2f63b8", "#2fa673", "#e9772b", "#8e5ea8", "#f4f0e0", "#c9375e"]


def vending(st, G="vending", state="full"):
    """A snack machine with no name on it: a dark blue steel cabinet, a big window onto five rows of coils with packets
    in plain colours (a drawing on each: a pretzel, a peanut, a cracker; no brand), lit inside; a column of buttons and a
    coin slot at the right; the tray at the bottom behind its flap. `state`: "full"; "peanuts" (the packet of peanuts
    has come down: its coil is empty and the packet lies in the tray); "taken" (its coil empty, the tray empty again)."""
    x0, x1, y0, y1, z0, z1 = M.VENDING
    gx0, gx1, gy0, gy1 = M.VEND_GLASS
    body = metal("#2c4678", 210, 0.07)
    tx0, tx1, ty0, ty1 = M.VEND_TRAY
    zw = z1 - 34                                                 # the back of the window's well
    st.box(x0, x1, y0 + 4, y1, z0, zw, body, "vending", grp=G, foot=True)
    # its front, in pieces round the window and the tray (so that both are open)
    for (a0, a1, b0, b1) in ((x0, gx0, y0 + 4, y1), (gx1, x1, y0 + 4, y1), (gx0, gx1, gy1, y1),
                             (gx0, tx0, y0 + 4, gy0), (tx1, gx1, y0 + 4, gy0), (tx0, tx1, y0 + 4, ty0), (tx0, tx1, ty1, gy0)):
        st.box(a0, a1, b0, b1, zw, z1, body, "vending", grp=G, shadow=False)
    st.occ.append((x0, x1, y0, y1, z0, z1))
    for fx in (x0 + 4, x1 - 4):
        st.box(fx - 3, fx + 3, 0, 4, z1 - 8, z1 - 2, plain("#1a1a1e", 0.05), "vending", grp=G, shadow=False)
    # the window's well: lit inside, its shelves and coils and packets
    well = (gx0, gx1, gy0, gy1, z1 - 34, z1 - 2)
    def m_well(c):
        k = col("#e8e4d4")
        return k * 0.3, k * 0.55
    st.box(*well, m_well, "vending", grp=G, inside=True)
    rows, cols = M.VEND_ROWS, M.VEND_COLS
    rh = (gy1 - gy0 - 4) / rows
    cw = (gx1 - gx0 - 4) / cols
    rng = np.random.default_rng(211)
    for r in range(rows):
        sy = gy1 - 2 - (r + 1) * rh
        st.box(gx0 + 1, gx1 - 1, sy - 0.8, sy, z1 - 33, z1 - 4, plain("#9aa0a4", 0.05), "vending", grp=G, shadow=False, emi=col("#e8e4d4") * 0.2)
        for k in range(cols):
            cx = gx0 + 2 + (k + 0.5) * cw
            empty = (r, k) == M.PEANUT_SLOT and state in ("peanuts", "taken")
            st.rope([(cx - cw * 0.36 + (i / 12.0) * cw * 0.72, sy + 3.0 + 2.6 * math.sin(i * 1.3), z1 - 10 - 2.6 * math.cos(i * 1.3)) for i in range(13)],
                    0.35, col("#c8ccd0"), name="vending", grp=G)
            if empty:
                continue
            peanut = (r, k) == M.PEANUT_SLOT
            cc = "#f2c02e" if peanut else SNACKS[int(rng.integers(len(SNACKS)))]
            draw = "peanut" if peanut else ("pretzel", "cracker", "chip", "stripe")[int(rng.integers(4))]
            packet(st, (cx, sy, z1 - 9), cw * 0.62, rh * 0.74, cc, draw, G)
    # the glass: a frame round it, a long streak of light across it
    def m_glass(c):
        u, v = c.U, c.V
        streak = (np.abs((u + v * 0.45) - 20) < 2.6) | (np.abs((u + v * 0.45) - 27) < 0.9)
        k = col("#f0f4f0")
        return k * 0.1, np.where(streak[..., None], col("#ffffff") * 0.28, 0.0), streak
    st.poly([(gx0, gy0, z1 + 0.3), (gx1, gy0, z1 + 0.3), (gx1, gy1, z1 + 0.3), (gx0, gy1, z1 + 0.3)], m_glass, "vending", grp=G, flag=1)
    trim = plain("#1c1e26", 0.05, 3, 212)
    for (a0, a1, b0, b1) in ((gx0 - 2.5, gx1 + 2.5, gy1, gy1 + 2.5), (gx0 - 2.5, gx1 + 2.5, gy0 - 2.5, gy0), (gx0 - 2.5, gx0, gy0, gy1), (gx1, gx1 + 2.5, gy0, gy1)):
        st.box(a0, a1, b0, b1, z1, z1 + 0.8, trim, "vending", grp=G, shadow=False)
    # the buttons and the coin slot, at the right
    px0, px1, py0, py1 = M.VEND_PANEL
    def m_panel(c):
        u, v = c.U, c.V
        k = col("#d8d4c4") * (0.95 + 0.05 * fbm(u / 3, v / 3, 213, 2))[..., None]
        btn = (np.abs(((u - 1.5) % 7.0) - 3.5) < 2.3) & (np.abs(((v - 2.0) % 5.2) - 2.6) < 1.7) & (v < 32) & (v > 1)
        k = np.where(btn[..., None], col("#3a3a40"), k)
        slot = (np.abs(u - 8.5) < 0.7) & (v > 40) & (v < 47)
        k = np.where(slot[..., None], col("#141416"), k)
        ret = (np.abs(u - 8.5) < 2.8) & (v > 35.5) & (v < 37.5)
        k = np.where(ret[..., None], col("#7a7a80"), k)
        return k
    st.poly([(px0, py0, z1 + 0.4), (px1, py0, z1 + 0.4), (px1, py1, z1 + 0.4), (px0, py1, z1 + 0.4)], m_panel, "vending", grp=G, bias=0.1)
    # the tray: a dark well behind a flap that is pushed in at the top; with the peanuts lying in it
    st.box(tx0, tx1, ty0, ty1, z1 - 16, z1 + 0.1, plain("#141418", 0.06, 3, 214), "vending", grp=G, inside=True)
    def m_flap(c):
        return col("#262830") * (0.9 + 0.1 * fbm(c.U / 3, c.V / 3, 215, 2))[..., None]
    st.poly([(tx0 + 0.5, ty1 - 0.5, z1 - 3.5), (tx1 - 0.5, ty1 - 0.5, z1 - 3.5), (tx1 - 0.5, ty0 + 9, z1 - 9.0), (tx0 + 0.5, ty0 + 9, z1 - 9.0)],
            m_flap, "vending", grp=G)
    st.box(tx0 - 2, tx1 + 2, ty0 - 2, ty0, z1, z1 + 1.5, trim, "vending", grp=G, shadow=False)
    st.box(tx0 - 2, tx1 + 2, ty1, ty1 + 2, z1, z1 + 1.5, trim, "vending", grp=G, shadow=False)
    if state == "peanuts":
        packet(st, ((tx0 + tx1) / 2 + 4, ty0 + 1.2, z1 - 5.0), 15.0, 10.5, "#f2c02e", "peanut", G, lying=True)
    # a bowling trophy on top (the league's), a little crooked
    tx, tz = x0 + 26, z0 + 50
    st.box(tx - 6, tx + 6, y1, y1 + 4, tz - 5, tz + 5, wood("#5a3a24", 216, "x", 0.15), "trophy", grp=G)
    gold = chrome("#d8b45a", 0.6, 217)
    st.cyl((tx, tz), 1.2, y1 + 4, y1 + 13, gold, name="trophy", grp=G)
    st.ball((tx, y1 + 16, tz), 3.6, gold, "trophy", grp=G)                                    # a gold bowling ball (who else would)
    st.box(tx - 3.5, tx + 3.5, y1 + 4, y1 + 5.5, tz - 3, tz + 3, gold, "trophy", grp=G, shadow=False)


def packet(st, at, w, h, color, draw, G, lying=False):
    """One packet of a snack: a pillow of plain colour, crimped at its ends, with a drawing of what is in it."""
    x, y, z = at
    k = col(color)

    def m_pack(c, draw=draw):
        u, v = c.U, c.V
        out = k * (0.9 + 0.12 * fbm(u / 2, v / 2, 220, 2))[..., None]
        crimp = (v < 1.0) | (v > (w if lying else h) * 0 + (h if not lying else w) - 1.0)
        mid_u, mid_v = (w / 2, h / 2) if not lying else (w / 2, h / 2)
        if draw == "peanut":
            nut = (np.hypot((u - mid_u + 1.6) / 2.0, (v - mid_v) / 1.6) < 1) | (np.hypot((u - mid_u - 1.4) / 1.9, (v - mid_v) / 1.5) < 1)
            out = np.where(nut[..., None], col("#b07a3c"), out)
        elif draw == "pretzel":
            ring = np.abs(np.hypot((u - mid_u) / 2.6, (v - mid_v) / 2.0) - 1) < 0.28
            out = np.where(ring[..., None], col("#8a4a1e"), out)
        elif draw == "cracker":
            sq = (np.abs(u - mid_u) < 2.2) & (np.abs(v - mid_v) < 2.2)
            out = np.where(sq[..., None], col("#e8c070"), out)
        elif draw == "chip":
            chip = np.hypot((u - mid_u) / 2.8, (v - mid_v) / 1.8) < 1
            out = np.where(chip[..., None], col("#f0d070"), out)
        else:
            out = np.where((np.abs(v - mid_v) < 1.1)[..., None], col("#f4f0e0"), out)
        return out
    if not lying:
        # standing in its coil, its face toward us, a little tipped forward
        st.poly([(x - w / 2, y + 0.5, z + 1.6), (x + w / 2, y + 0.5, z + 1.6), (x + w / 2, y + h, z - 0.8), (x - w / 2, y + h, z - 0.8)], m_pack, "vending", grp=G)
    else:
        st.poly([(x - w / 2, y + 0.4, z + h * 0.15), (x + w / 2, y + 0.4, z + h * 0.15), (x + w / 2 - 1.0, y + 3.2, z - h * 0.75),
                 (x - w / 2 + 0.6, y + 3.0, z - h * 0.75)], m_pack, "peanuts", grp=G)


# ---------------------------------------------------------------- the couch, and its afghan
def couch(st, G="back"):
    """A brown tweed couch along the left wall, facing into the room: a plain base on short legs, three seat cushions
    with their seams, three back cushions, square arms with a rolled top; over its back a crocheted afghan of granny
    squares (orange, gold, avocado, brown, cream), hanging down over the back cushions in points. Floyd sleeps on it
    (the game draws him: he is not painted)."""
    x0, x1, y0, y1, z0, z1 = M.COUCH
    sh_ = M.SEAT_H
    bx = M.BACK_X
    aw, ah = M.ARM_W, M.ARM_H

    def m_tweed(c):
        k = col(COUCH) * (0.86 + 0.22 * fbm(c.X / 0.8, c.Y / 0.8 + c.Z / 0.8, 230, 2))[..., None]
        k = k * (0.92 + 0.1 * fbm(c.X / 12, c.Z / 12 + c.Y / 12, 231, 2))[..., None]
        nub = fbm(c.X / 0.35 + c.Y / 0.5, c.Z / 0.35, 232, 1) > 0.78
        return np.where(nub[..., None], k * 1.16, k)

    def m_skirt(c):                                                              # the base's front: a band of the tweed with a welt along its top
        k = m_tweed(c)
        welt = np.abs(c.Y - 27.0) < 0.9
        return np.where(welt[..., None], k * 0.62, k)
    for lz in (z0 + 6, z1 - 6):
        for lx in (x0 + 6, x1 - 6):
            st.cyl((lx, lz), 2.0, 0, 9, wood("#3a2618", 233, "y", 0.2), r1=1.4, name="couch", grp=G, shadow=False, foot=True)
    st.box(x0, x1 - 2, 9, 28, z0 + aw, z1 - aw, m_skirt, "couch", grp=G)
    st.occ.append((x0, x1, 0, 28, z0, z1))
    # the frame of the back, against the wall
    st.box(x0, 12, 28, y1, z0 + aw, z1 - aw, m_tweed, "couch", grp=G)
    # three seat cushions, a seam between each, each a little domed and sagging at its middle
    n = 3
    span = (z1 - z0 - 2 * aw) / n
    for i in range(n):
        a, b = z0 + aw + i * span + 0.8, z0 + aw + (i + 1) * span - 0.8
        st.box(bx - 2, x1 - 1, 28, sh_ - 2.6, a, b, m_tweed, "cushion", grp=G)
        st.ball((bx + (x1 - bx) / 2 - 1, sh_ - 2.8, (a + b) / 2), 1.0, m_tweed, "cushion", grp=G, squash=((x1 - bx) / 2.0, 2.9, (b - a) / 2.0))
        # its back cushion, leaning on the frame
        st.box(12, bx + 2, sh_ - 3, y1 - 6, a + 0.6, b - 0.6, m_tweed, "backcushion", grp=G)
        st.ball((bx - 4, y1 - 7, (a + b) / 2), 1.0, m_tweed, "backcushion", grp=G, squash=(10.5, 4.0, (b - a) / 2.0 - 0.8))
    # the arms: square, with a rolled top
    for (a, b) in ((z0, z0 + aw), (z1 - aw, z1)):
        st.box(x0, x1, 9, ah - 6, a, b, m_tweed, "couch", grp=G)
        st.cyl((ah - 6.5, (a + b) / 2), (b - a) / 2 + 0.6, x0, x1 + 0.6, m_tweed, axis="x", name="couch", grp=G)
    # a cushion in mustard at the near end, leaning in the corner of the arm
    def m_pillow(c):
        return col("#c8962e") * (0.88 + 0.2 * fbm(c.X / 1.2, c.Y / 1.2 + c.Z / 1.2, 234, 2))[..., None]
    st.ball((bx + 12, sh_ + 15, z1 - aw - 15), 1.0, m_pillow, "pillow", grp=G, squash=(7.0, 15.0, 14.0))
    # the afghan: over the top of the back and hanging down over the back cushions, in points; granny squares 9 cm a side
    def m_afghan(c):
        along = c.Z
        up = c.Y + np.maximum(c.X - 10.0, 0) * 1.4
        sq = 9.0
        i, j = np.floor(along / sq), np.floor(up / sq)
        cu, cv = along - i * sq - sq / 2, up - j * sq - sq / 2
        r = np.maximum(np.abs(cu), np.abs(cv))
        pal = np.stack([col("#e9772b"), col("#f2b42e"), col("#7f8c3e"), col("#8c3b20"), col("#c9375e")])
        h = (hashf(i * 31 + j * 7, 235) * 5).astype(np.int64) % 5
        ring1, ring2 = pal[h], pal[(h + 2) % 5]
        k = np.where((r < 1.6)[..., None], ring2, np.where((r < 3.2)[..., None], ring1, col("#efe6cc")))
        k = np.where((r > 4.0)[..., None], col("#3a2a20"), k)                     # the dark rounds that join the squares
        stitch = 0.85 + 0.25 * fbm(along / 0.45, up / 0.45, 236, 1)
        return k * stitch[..., None]
    zz0, zz1 = z0 + aw + 6, z1 - aw - 40
    ctop = y1 - 3.0                                                              # the back cushions' tops, where it lies over them
    st.box(x0 - 0.5, bx + 3.0, ctop, ctop + 3.0, zz0, zz1, m_afghan, "afghan", grp=G)
    drop = 24.0
    fx = bx + 3.4
    st.poly([(fx, ctop + 3.0, zz0), (fx, ctop + 3.0, zz1), (fx + 1.6, ctop - drop, zz1), (fx + 1.6, ctop - drop, zz0)], m_afghan, "afghan", grp=G)
    for k in range(int((zz1 - zz0) / 9.0)):
        za = zz0 + k * 9.0
        st.poly([(fx + 1.6, ctop - drop, za), (fx + 1.6, ctop - drop, za + 9.0), (fx + 2.4, ctop - drop - 6.5, za + 4.5)], m_afghan, "afghan", grp=G)
        st.stick((fx + 2.4, ctop - drop - 6.5, za + 4.5), (fx + 2.8, ctop - drop - 11.0, za + 4.8), 0.35, col("#e9772b"), "afghan", grp=G)
    # where it is dark under the seat and in front of it: a pool on the floor (office_breakroom.render lays it)
    st.pools.append(((x0 + x1) / 2 + 8, (z0 + z1) / 2, (x1 - x0) / 2 + 16, (z1 - z0) / 2 + 10, 0.30))


# ---------------------------------------------------------------- Jed's chair
def molded_chair(st, x, z, face_deg, color, name, G):
    """A molded plastic chair on four chrome legs. face_deg: which way its sitter would look (0 toward us, 90 to +X,
    180 away from us, 270 to -X)."""
    a = math.radians(face_deg)
    fx, fz = math.sin(a), math.cos(a)                            # forward
    rx, rz = math.cos(a), -math.sin(a)                           # its right
    seat_y, back_y = M.CHAIR_SEAT, M.CHAIR_BACK

    def P(s, y, f):
        return (x + rx * s + fx * f, y, z + rz * s + fz * f)
    shell = plain(color, 0.07, 6, 240)
    leg = chrome("#c0c4c8", 0.6, 241)
    for s in (-19, 19):
        for f in (-17, 17):
            st.stick(P(s * 0.92, 0, f * 0.92), P(s * 0.8, seat_y - 3, f * 0.78), 0.9, leg, name, grp=G)
            fx_, _, fz_ = P(s * 0.92, 0, f * 0.92)
            st.feet[f"{name}-{len(st.feet)}"] = (fx_ - 1.0, fx_ + 1.0, fz_ - 1.0, fz_ + 1.0)            # each leg's own foot
    st.stick(P(-19 * 0.86, 12, -17 * 0.9), P(19 * 0.86, 12, -17 * 0.9), 0.6, leg, name, grp=G)
    seat = [P(-21, seat_y, 19), P(21, seat_y, 19), P(21, seat_y - 1, -19), P(-21, seat_y - 1, -19)]
    st.poly(seat, shell, name, grp=G)
    st.poly([P(-21, seat_y - 2.6, 19.5), P(21, seat_y - 2.6, 19.5), P(21, seat_y, 19.5), P(-21, seat_y, 19.5)], shell, name, grp=G)       # its front lip
    back = [P(-20, seat_y + 4, -21), P(20, seat_y + 4, -21), P(19, back_y, -25), P(-19, back_y, -25)]
    st.poly(back, shell, name, grp=G)
    st.poly([P(-20, seat_y - 1, -19), P(20, seat_y - 1, -19), P(20, seat_y + 4.5, -21.5), P(-20, seat_y + 4.5, -21.5)], shell, name, grp=G)
    xs = [p[0] for p in seat + back]
    zs = [p[2] for p in seat + back]
    st.occ.append((min(xs), max(xs), seat_y - 4, back_y, min(zs), max(zs)))                       # its shell throws the shadow; light goes between its legs
    st.pools.append((x, z, 26.0, 26.0, 0.30))                                                      # and under it, a pool of shadow


def chair(st, G="chair"):
    x0, x1, z0, z1 = M.CHAIR
    molded_chair(st, (x0 + x1) / 2, (z0 + z1) / 2, 270.0, ORANGE, "chair", G)


# ---------------------------------------------------------------- the near table and its chairs (the front plane)
def table(st, G="front"):
    """A round table in the near right, white laminate edged in steel on a black pedestal, a folded newspaper on it
    (no name), a mug, a napkin holder; two plastic chairs at it, one avocado (turned to the table), one orange with its
    back to us."""
    X, Z, R, Ht = M.TABLE
    def m_top(c):
        k = col("#ece8da") * (0.95 + 0.06 * fbm(c.X / 9, c.Z / 9, 250, 2))[..., None]
        return k
    st.cyl((X, Z), R, Ht - 2.8, Ht, m_top, name="table", grp=G, cap=col("#ece8da"))
    st.cyl((X, Z), R + 0.4, Ht - 3.0, Ht - 0.2, chrome("#b8bcc0", 0.5, 251), name="table", grp=G, shadow=False)
    st.cyl((X, Z), 3.2, 4, Ht - 3, plain("#22201e", 0.05), name="table", grp=G)
    st.cyl((X, Z), 22.0, 0, 4, plain("#22201e", 0.05), r1=14.0, name="table", grp=G, foot=True)
    st.pools.append((X - 6, Z - 6, R + 6, R + 6, 0.42))
    def m_paper(c):
        u, v = c.U, c.V
        k = col("#e4e0d0") * (0.95 + 0.05 * fbm(u / 4, v / 4, 252, 2))[..., None]
        cols_ = (np.abs(((u - 2) % 7.0) - 3.5) < 2.9) & (np.abs(((v - 2) % 1.4) - 0.7) < 0.3) & (v < 22)
        k = np.where(cols_[..., None], col("#8a8a90"), k)
        head = (v > 24) & (v < 27.5) & (u > 3) & (u < 27)
        return np.where(head[..., None], col("#3a3a40"), k)
    a = math.radians(-24)
    cx, cz = X - 14, Z - 4

    def P(u, v):
        return (cx + u * math.cos(a) - v * math.sin(a), Ht + 0.3, cz + u * math.sin(a) + v * math.cos(a))
    st.poly([P(-15, -14), P(15, -14), P(15, 14), P(-15, 14)], m_paper, "newspaper", grp=G, bias=0.05)
    st.cyl((X + 16, Z + 10), 4.2, Ht, Ht + 9.5, plain("#2fa673", 0.08, 3, 253), name="mug", grp=G, cap=col("#2a1810"), hollow=False)
    st.rope(curve3([(X + 20, Ht + 3, Z + 10), (X + 23.5, Ht + 5.5, Z + 10), (X + 20, Ht + 8, Z + 10)], 4), 0.75, col("#2fa673"), name="mug", grp=G)
    st.box(X + 2, X + 12, Ht, Ht + 9, Z - 22, Z - 17, chrome("#c0c4c8", 0.5, 254), "napkins", grp=G)
    st.box(X + 2.6, X + 11.4, Ht + 1, Ht + 10.5, Z - 21, Z - 18, plain("#f6f4ec", 0.03), "napkins", grp=G)
    for (cx_, cz_, face) in M.TABLE_CHAIRS:
        molded_chair(st, cx_, cz_, face, AVOCADO if face == 90.0 else ORANGE, "tablechair", G)


# ---------------------------------------------------------------- the low table in front of the couch (the front plane)
def lowtable(st, G="front"):
    """OFFICE-17D (resumed). A low table in front of the couch's near end, in the near left, its near legs cut off by the
    picture's bottom edge: a wood-grain laminate top with a dark edge band, on four tapered legs. On it, a game of
    solitaire laid out and left halfway (Floyd's, before Regulation 22 took him), the pack face down beside it; two
    magazines fanned (a fish on one cover, a bowling pin on the other: no names); a white mug with a blue band."""
    x0, x1, z0, z1, ht = M.LOWTABLE
    tt = 3.0                                                                     # the top's thickness

    def m_top(c):
        if c.face != "top":
            return col("#5a3a24") * (0.9 + 0.15 * fbm(c.X / 6, c.Z / 6 + c.Y / 3, 270, 2))[..., None]        # the edge band
        g = fbm(c.X / 30.0, c.Z / 2.2, 271, 3)                                   # the grain runs along X
        k = lerp(col("#8a5c38"), col("#b07c4c"), np.clip(g * 1.4 - 0.2, 0, 1)[..., None])
        return k * (0.92 + 0.1 * fbm(c.X / 4, c.Z / 4, 272, 2))[..., None]
    st.box(x0, x1, ht - tt, ht, z0, z1, m_top, "lowtable", grp=G)
    st.box(x0 + 4, x1 - 4, ht - tt - 7, ht - tt, z0 + 4, z1 - 4, col("#4e3220"), "lowtable", grp=G)      # its rails, under the top
    for lx in (x0 + 7, x1 - 7):
        for lz in (z0 + 7, z1 - 7):
            st.cyl((lx, lz), 1.5, 0, ht - tt, wood("#4a3020", 273, "y", 0.2), r1=2.5, name="lowtable", grp=G, foot=True)
    st.pools.append(((x0 + x1) / 2, (z0 + z1) / 2, (x1 - x0) / 2 + 8, (z1 - z0) / 2 + 8, 0.34))
    y = ht + 0.05
    cw, ch = 6.3, 8.8                                                            # a playing card

    def back(c):                                                                 # a card's back: blue, a white border, a fine lattice
        u, v = np.asarray(c.U), np.asarray(c.V)
        k = np.broadcast_to(col("#2c4c9c"), u.shape + (3,)).copy()
        lat = (np.abs(((u + v) % 1.2) - 0.6) < 0.12) | (np.abs(((u - v) % 1.2) - 0.6) < 0.12)
        k = np.where(lat[..., None], col("#5a78c0"), k)
        border = (u < 0.5) | (v < 0.5) | (u > cw - 0.5) | (v > ch - 0.5)
        return np.where(border[..., None], col("#f4f2ea"), k)

    def face(red):
        def f(c):
            u, v = np.asarray(c.U), np.asarray(c.V)
            k = np.broadcast_to(col("#f6f4ec"), u.shape + (3,)).copy()
            ink = col("#c8242a") if red else col("#1e1e26")
            pip = ((u - cw / 2) ** 2 / 1.3 ** 2 + (v - ch / 2) ** 2 / 1.5 ** 2) < 1.0
            corner = (u < 1.6) & (v > ch - 2.4)
            return np.where((pip | corner)[..., None], ink, k)
        return f

    def card(cx, cz, mat, lift, turn=0.0):
        a = math.radians(turn)
        ca, sa = math.cos(a), math.sin(a)

        def P(u, v):                                                             # u across (to +X), v away from us (to -Z)
            return (cx + u * ca + v * sa, y + lift, cz - v * ca + u * sa)
        st.poly([P(0, 0), P(cw, 0), P(cw, ch), P(0, ch)], mat, "cards", grp=G, bias=0.04 + lift)
    # the tableau: seven columns, each with as many cards face down as its number, the last face up
    reds = [True, False, False, True, False, True, True]
    for i in range(7):
        cx = x0 + 34 + i * 8.6
        far = z0 + 9.0
        for j in range(i):
            card(cx, far + ch + j * 1.3, back, 0.02 * j)
        card(cx, far + ch + i * 1.3 + (2.6 if i in (2, 5) else 0.0), face(reds[i]), 0.02 * i + 0.02)
        if i in (2, 5):                                                          # a short run on two of them
            card(cx, far + ch + i * 1.3, face(not reds[i]), 0.02 * i + 0.01)
    # the stock, face down, a little squared stack; and the card turned up from it
    st.box(x0 + 9, x0 + 9 + cw, ht, ht + 1.1, z0 + 10, z0 + 10 + ch, col("#e8e4d8"), "cards", grp=G, shadow=False)
    card(x0 + 9, z0 + 10 + ch, back, 1.15)
    card(x0 + 18.5, z0 + 10.5 + ch, face(True), 0.05, turn=-6.0)

    # two magazines, fanned, at the near right corner
    def cover(kind):
        def f(c):
            u, v = np.asarray(c.U), np.asarray(c.V)
            if kind == "fish":
                k = lerp(col("#2a7a8a"), col("#7ac0c8"), np.clip(v / 28.0, 0, 1)[..., None])
                fish = (((u - 10.5) / 6.5) ** 2 + ((v - 12.0) / 2.6) ** 2) < 1.0
                tail = (u > 15.5) & (u < 19.0) & (np.abs(v - 12.0) < (u - 15.5) * 0.9)
                k = np.where((fish | tail)[..., None], col("#d8a040"), k)
            else:
                k = np.broadcast_to(col("#e8d8b8"), u.shape + (3,)).copy()
                pin = ((((u - 10.5) / 2.6) ** 2 + ((v - 9.5) / 4.2) ** 2) < 1.0) | ((((u - 10.5) / 1.5) ** 2 + ((v - 16.5) / 2.4) ** 2) < 1.0)
                k = np.where(pin[..., None], col("#fbfaf4"), k)
                k = np.where((pin & (np.abs(v - 14.0) < 0.5))[..., None], col("#c8242a"), k)
            band = v > 23.0                                                     # the masthead: a band of colour, no name
            k = np.where(band[..., None], col("#a8282c") if kind == "fish" else col("#2a3a6a"), k)
            lines = (v < 5.0) & (np.abs((v % 1.4) - 0.7) < 0.25) & (u > 2.0) & (u < 13.0)
            return np.where(lines[..., None], col("#f4f0e4"), k)
        return f
    for (mx, mz, turn, kind, lift) in ((x1 - 47.0, z1 - 4.0, 8.0, "pin", 0.10), (x1 - 40.0, z1 - 2.0, -14.0, "fish", 0.40)):
        a = math.radians(turn)
        ca, sa = math.cos(a), math.sin(a)

        def P(u, v, mx=mx, mz=mz, ca=ca, sa=sa, lift=lift):
            return (mx + u * ca + v * sa, ht + lift, mz - v * ca + u * sa)
        st.poly([P(0, 0), P(21, 0), P(21, 28), P(0, 28)], cover(kind), "magazine", grp=G, bias=0.05 + lift)
    # the mug, at the far right corner, half full and gone cold
    mx, mz = x1 - 14.0, z0 + 13.0
    def m_mug(c):
        band_ = np.abs(np.asarray(c.Y) - (ht + 6.2)) < 0.9
        return np.where(band_[..., None], col("#3a5ab0"), col("#f2f0e8"))
    st.cyl((mx, mz), 4.2, ht, ht + 9.5, m_mug, name="lowmug", grp=G, cap=col("#3a2416"))
    st.rope(curve3([(mx + 4.0, ht + 3, mz), (mx + 7.4, ht + 5.5, mz), (mx + 4.0, ht + 8, mz)], 4), 0.75, col("#f2f0e8"), name="lowmug", grp=G)


# ---------------------------------------------------------------- the bin
def trash(st, G="back"):
    """A tan plastic kitchen bin with a swing lid, in the gap between the fridge and the left wall."""
    x0, x1, y0, y1, z0, z1 = M.TRASH
    k = plain("#c8b48a", 0.08, 4, 260)
    st.box(x0, x1, y0, y1 - 8, z0, z1, k, "trash", grp=G, foot=True)
    st.box(x0 - 0.6, x1 + 0.6, y1 - 8, y1 - 6, z0 - 0.6, z1 + 0.6, k, "trash", grp=G)
    st.poly([(x0, y1 - 6, z1), (x1, y1 - 6, z1), (x1, y1, (z0 + z1) / 2 + 2), (x0, y1, (z0 + z1) / 2 + 2)], k, "trash", grp=G)
    st.poly([(x0, y1, (z0 + z1) / 2 + 2), (x1, y1, (z0 + z1) / 2 + 2), (x1, y1 - 6, z0), (x0, y1 - 6, z0)], k, "trash", grp=G)

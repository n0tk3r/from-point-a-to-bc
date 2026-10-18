"""Everything in Interview Room C, the Comfortable Room (office_room.py), built in the room's own centimetres: the shell
(carpet, painted block, the suspended ceiling), the hall seen through the doorway, the door, what is on the walls, the
ceiling's fittings, and the furniture. OFFICE-17C.

Each function puts one group of things on the Stage with a paint that colours it in ITS OWN measurements. Groups (`grp`)
are the cut-outs: "table", "questionnaire", "chair-corner", "vent", "thermostat", "intercom", "door", "doorframe",
"plant", "front"; everything else is the backdrop ("back"). All measurements come from office_room_model.py. Every word
is the Office's own; no brand, no logo, nobody's typeface."""

import math

import numpy as np

from brush import F32, lerp
import office_room_model as M
from office_room_kit import (col, fbm, hashf, grad_of, px_of, lines_aa, band, lay, normals, rm, rect_uv, disc_uv, plain, painted_steel,
                             chrome, molded, laminate, obox, m_carpet, block_wall, ceiling_paint, m_troffer, vent, sprinkler,
                             smoke_detector, ceiling_speaker, stacking_chair, curve3, face_at_grille, OUTSIDE, PAPER, STEEL, STEEL_D)
from room import View

H = M.H


# ---------------------------------------------------------------- the shell
CARPET = m_carpet(seed=5, stains=((236.0, 214.0, 13.0), (430.0, 150.0, 9.0)),
                  paths=(((109.0, 60.0), (260.0, 160.0), 34.0), ((260.0, 160.0), (250.0, 230.0), 30.0), ((420.0, 60.0), (440.0, 200.0), 26.0)))


def m_back(c):
    X, Y = c.X, c.Y
    return block_wall(c, X, Y, grad_of(X) * c.ss, grad_of(Y) * c.ss, seed=1)


def m_left(c):
    Z, Y = c.Z, c.Y
    return block_wall(c, Z, Y, grad_of(Z) * c.ss, grad_of(Y) * c.ss, seed=2)


def m_right(c):
    Z, Y = c.Z, c.Y
    return block_wall(c, Z, Y, grad_of(Z) * c.ss, grad_of(Y) * c.ss, seed=3)


CEILING = ceiling_paint(grid=M.GRID, origin=(M.GRID_X0, M.GRID_Z0), seed=4, stains=((372.0, 400.0, 26.0),))


def holes():
    dx0, dx1, dy0, dy1 = M.DOOR
    vx0, vx1, vz0, vz1 = M.VENT
    return {
        "back": lambda X, Y, Z: (X > dx0) & (X < dx1) & (Y < dy1),
        "ceiling": lambda X, Y, Z: (X > vx0 + 3.5) & (X < vx1 - 3.5) & (Z > vz0 + 3.5) & (Z < vz1 - 3.5),
    }


def shell(st):
    st.shell(M.W, H, dict(floor=CARPET, back=m_back, left=m_left, right=m_right, ceiling=CEILING), holes=holes())
    # the room's near wall (behind the lens: only the mirror sees it)
    def m_front(c):
        X, Y = c.X, c.Y
        g = px_of(c, 1.5)
        return block_wall(c, X, Y, g, g, seed=6)
    st.poly([(0, 0, M.D), (M.W, 0, M.D), (M.W, H, M.D), (0, H, M.D)], m_front, "frontwall")


# ---------------------------------------------------------------- the hall, through the doorway (lit by its own tubes)
HALL_D = 170.0                   # how wide the hall is (its far wall at Z = -HALL_D)
HALL_GLOW = 1.08                 # the hall a little brighter than the room


def hall(st, G="back"):
    """What the doorway shows: the hall's vinyl floor, its far wall of the same block, a sign pointing the way to
    PROPERTY & EFFECTS, and its ceiling. Self-lit (the room's lamps leave it alone)."""
    dx0, dx1 = M.DOOR[0], M.DOOR[1]
    zf = -HALL_D
    x0, x1 = dx0 - 260, dx1 + 260

    def lit(base, k=1.0):
        def f(c):
            out = base(c)
            # the hall's tubes run along it, overhead: brightest near the doorway's line of sight, falling off
            g = HALL_GLOW * k * (0.86 + 0.14 * np.clip(1 - np.abs(c.Z + HALL_D * 0.5) / HALL_D, 0, 1))
            return out * 0.10, out * np.asarray(g)[..., None]
        return f

    def m_vinyl(c):
        T = 30.0
        ix, iz = np.floor(c.X / T), np.floor(c.Z / T)
        chk = ((ix + iz) % 2) == 0
        base = np.where(chk[..., None], col("#d6d0bc"), col("#c4bea8"))
        base = base * (0.95 + 0.08 * fbm(c.X / 9, c.Z / 9, 61, 2))[..., None]
        g = px_of(c, 3.0)
        seam = np.maximum(lines_aa(c.X, T, 0.6, g), lines_aa(c.Z, T, 0.6, g))
        return base * (1 - 0.12 * seam[..., None])

    def m_far(c):
        X, Y = c.X, c.Y
        g = px_of(c, 1.2)
        out = block_wall(c, X, Y, g, g, seed=7)
        # a sign on the far wall: an arrow and PROPERTY & EFFECTS (laid as words, later): its plate
        plate = rect_uv(X, Y, 60.0, 150.0, 132.0, 160.0, g)
        out = lay(out, "#3c4a5e", plate * 0.95)
        # a fire extinguisher's red, at the right of what the doorway shows
        ext = rect_uv(X, Y, 180.0, 194.0, 40.0, 92.0, g)
        out = lay(out, "#b8382c", ext)
        return out

    def m_hceil(c):
        X, Z = c.X, c.Z
        out = col("#d8d4c4") * (0.95 + 0.06 * fbm(X / 30, Z / 30, 63, 2))[..., None]
        tube = np.exp(-((Z + HALL_D * 0.5) / 9.0) ** 2)
        return out * (1 + 1.4 * tube[..., None])

    st.poly([(x0, 0, zf), (x1, 0, zf), (x1, 0, -M.WALL_T), (x0, 0, -M.WALL_T)], lit(m_vinyl), "hall", grp=G, flag=OUTSIDE)
    st.poly([(x0, 0, zf), (x1, 0, zf), (x1, H, zf), (x0, H, zf)], lit(m_far), "hall", grp=G, flag=OUTSIDE)
    st.poly([(x0, H, zf), (x1, H, zf), (x1, H, -M.WALL_T), (x0, H, -M.WALL_T)], lit(m_hceil, 0.9), "hall", grp=G, flag=OUTSIDE)
    # the doorway's reveal: the wall's thickness, painted, round the opening
    rev = lit(plain(M_BLOCK_REVEAL, 0.06, seed=8), 0.62)
    st.poly([(dx0, 0, 0), (dx0, 0, -M.WALL_T), (dx0, M.DOOR[3], -M.WALL_T), (dx0, M.DOOR[3], 0)], rev, "doorway", grp=G, flag=OUTSIDE)
    st.poly([(dx1, 0, 0), (dx1, 0, -M.WALL_T), (dx1, M.DOOR[3], -M.WALL_T), (dx1, M.DOOR[3], 0)], rev, "doorway", grp=G, flag=OUTSIDE)
    st.poly([(dx0, M.DOOR[3], 0), (dx1, M.DOOR[3], 0), (dx1, M.DOOR[3], -M.WALL_T), (dx0, M.DOOR[3], -M.WALL_T)], rev, "doorway", grp=G, flag=OUTSIDE)


M_BLOCK_REVEAL = "#c8b994"


# ---------------------------------------------------------------- the door: its casing, the leaf shut, the leaf open
DOOR_GRAY = "#7f8891"


def door_casing(st, G="doorframe"):
    """The steel door frame round the opening: a hollow-metal frame, painted the regulation gray."""
    dx0, dx1, dy0, dy1 = M.DOOR
    fw, fd = M.DOOR_FRAME, 1.6
    m = painted_steel(DOOR_GRAY, seed=21, chips=0.4)
    st.box(dx0 - fw, dx0, 0, dy1 + fw, 0, fd, m, "doorcasing", grp=G)
    st.box(dx1, dx1 + fw, 0, dy1 + fw, 0, fd, m, "doorcasing", grp=G)
    st.box(dx0 - fw, dx1 + fw, dy1, dy1 + fw, 0, fd, m, "doorcasing", grp=G)


def door_leaf(st, open_=False, G="door"):
    """The leaf: gray steel, flush, a narrow wired-glass slit (the hall's light through it), a lever handle on the
    right, three hinges on the left. It opens OUT into the hall: open, it stands swung away into the hall, seen past
    the jamb through the doorway."""
    dx0, dx1, dy0, dy1 = M.DOOR
    sx0, sx1, sy0, sy1 = M.DOOR_SLIT
    t = 4.4                                                     # the leaf's thickness
    wleaf = dx1 - dx0 - 0.6

    def m_leaf(c, along):
        u, v = along(c), c.Y
        g = px_of(c, 1.2)
        base = col(DOOR_GRAY) * (0.94 + 0.08 * fbm(u / 20, v / 20, 31, 3))[..., None]
        scuff = np.clip((fbm(u / 4, v / 2, 32, 3) - 0.62) * 4, 0, 1) * np.clip((40 - v) / 30, 0, 1)
        base = lay(base, "#6c7178", scuff * 0.6)
        # the slit: wired glass, the hall's light through it; a steel bead round it
        su0, su1 = sx0 - dx0, sx1 - dx0
        slit = rect_uv(u, v, su0, su1, sy0, sy1, g)
        bead = rect_uv(u, v, su0 - 1.6, su1 + 1.6, sy0 - 1.6, sy1 + 1.6, g) - slit
        wires = np.maximum(lines_aa(u - su0, 2.6, 0.5, g, fade=False), lines_aa(v, 2.6, 0.5, g, fade=False))
        glass = col("#e6efe0") * (0.85 + 0.15 * fbm(u / 6, v / 6, 33, 2))[..., None]
        glass = glass * (1 - 0.14 * wires[..., None])
        out = lay(base, "#6a7078", np.clip(bead, 0, 1) * 0.9)
        out = out * (1 - slit[..., None]) + glass * slit[..., None] * 0.15
        e = glass * (slit * 1.25)[..., None]
        return out, e

    if not open_:
        z = 0.8
        def m_face(c):
            return m_leaf(c, lambda c_: c_.X - dx0)
        st.poly([(dx0 + 0.3, 0.5, z), (dx1 - 0.3, 0.5, z), (dx1 - 0.3, dy1 - 0.3, z), (dx0 + 0.3, dy1 - 0.3, z)], m_face, "door", grp=G)
        # the lever handle and its rose, the hinges
        hx, hy = dx1 - 9.0, 102.0
        st.cyl((hx, hy), 2.8, z, z + 1.2, chrome(), axis="z", name="door", grp=G, shadow=False)
        st.stick((hx, hy, z + 3.5), (hx - 11.0, hy - 0.8, z + 3.8), 0.9, col("#c8ccd2"), "door", grp=G)
        st.stick((hx, hy, z + 0.8), (hx, hy, z + 3.6), 0.8, col("#c8ccd2"), "door", grp=G)
        for hy2 in (24.0, 102.0, 182.0):
            st.box(dx0 + 0.2, dx0 + 2.4, hy2, hy2 + 10, z, z + 1.0, painted_steel("#7a8088", 22), "door", grp=G, shadow=False)
    else:
        # swung out into the hall on its left hinges, about 70 degrees: across the left of the doorway, its face to us
        ang = math.radians(70.0)
        ax, az = dx0 + 0.5, -M.WALL_T
        ex, ez = ax + wleaf * math.cos(ang), az - wleaf * math.sin(ang)
        def m_open(c):
            return m_leaf(c, lambda c_: np.hypot(c_.X - ax, c_.Z - az))
        st.poly([(ax, 0.5, az), (ex, 0.5, ez), (ex, dy1 - 0.5, ez), (ax, dy1 - 0.5, az)], m_open, "door", grp=G, flag=OUTSIDE)
        nx, nz = -math.sin(ang) * t * 0.0, 0.0
        st.poly([(ax + 1.2, 0.5, az + 0.6), (ex + 1.2, 0.5, ez + 0.6), (ex + 1.2, dy1 - 0.5, ez + 0.6), (ax + 1.2, dy1 - 0.5, az + 0.6)],
                lambda c: (col("#6a7078") * 0.3 * np.ones(c.X.shape + (3,), F32), col("#6a7078") * 0.55 * np.ones(c.X.shape + (3,), F32)),
                "door", grp=G, flag=OUTSIDE)


# ---------------------------------------------------------------- on the walls
def clock(st, hand_angle=None, G="back", hands=True):
    """The wall clock over the door: a white face, a black rim, short black ticks, the hands at twenty to two; the red
    second hand is its own frames (`hand_angle` in degrees from twelve, clockwise; None: none)."""
    cx, cy, r = M.CLOCK
    z = 4.0

    def m_face(c):
        u, v = c.X - cx, c.Y - cy
        rr = np.hypot(u, v)
        g = px_of(c, 1.2)
        out = col("#f2f0e6") * np.ones(rr.shape + (3,), F32)
        ang = np.arctan2(u, v)
        tick = (np.abs(((ang / (2 * np.pi)) * 12 + 0.5) % 1 - 0.5) < 0.055) & (rr > r * 0.74) & (rr < r * 0.90)
        out = lay(out, "#202024", tick.astype(F32))
        if hands:
            for (deg, ln, w_) in ((-305.0 + 360 * 0, 0.50, 0.11), (240.0, 0.72, 0.07)):      # the hour hand near 2, the minute at 8
                a = math.radians(deg)
                dx, dy = math.sin(a), math.cos(a)
                along = u * dx + v * dy
                side = np.abs(-u * dy + v * dx)
                on = (along > -r * 0.08) & (along < r * ln) & (side < r * w_ * 0.5 + g * 0.3)
                out = lay(out, "#18181c", on.astype(F32))
            hub = np.clip((r * 0.07 - rr) / g + 0.5, 0, 1)
            out = lay(out, "#18181c", hub)
        rim = np.clip((rr - r * 0.92) / g + 0.5, 0, 1)
        return lay(out, "#1e1e22", rim)
    st.cyl((cx, cy), r, 0, z, m_face, axis="z", name="clock", grp=G, cap=m_face)
    if hand_angle is not None:
        a = math.radians(hand_angle)
        st.stick((cx - math.sin(a) * r * 0.16, cy - math.cos(a) * r * 0.16, z + 0.6),
                 (cx + math.sin(a) * r * 0.80, cy + math.cos(a) * r * 0.80, z + 0.6), 0.32, col("#c42e24"), "clockhand", grp="clockhand", shade=False)


def sign(st, G="back"):
    """The sign by the door: a beige plastic plate, a brown band at the top, its words laid later (`words`)."""
    x0, x1, y0, y1 = M.SIGN

    def m(c):
        g = px_of(c, 1.2)
        out = col("#e8dcc0") * (0.96 + 0.06 * fbm(c.X / 9, c.Y / 9, 41, 2))[..., None]
        top = rect_uv(c.X, c.Y, x0, x1, y1 - 24.0, y1, g)
        out = lay(out, "#6a4a36", top)
        edge = 1 - rect_uv(c.X, c.Y, x0 + 1.0, x1 - 1.0, y0 + 1.0, y1 - 1.0, g)
        return lay(out, "#9a8a70", edge * 0.7)
    st.box(x0, x1, y0, y1, 0, 1.0, m, "sign", grp=G, shadow=False)


THERMO_DIGITS = {72: "72", 77: "77", 81: "81"}


def thermostat(st, G="back"):
    """The thermostat by the door: a beige box with rounded edges, a small dial on its left, a window on its right with
    the number in it (the number is laid as words: one state for each of 72, 77 and 81)."""
    x0, x1, y0, y1 = M.THERMO
    dz = 4.0

    def m(c):
        g = px_of(c, 1.2)
        out = col("#ddd2b6") * (0.96 + 0.05 * fbm(c.X / 4, c.Y / 4, 43, 2))[..., None]
        # the window: a cream panel set in a dark bezel
        wx0, wx1, wy0, wy1 = x0 + 12.0, x1 - 2.5, y0 + 4.0, y1 - 3.0
        bez = rect_uv(c.X, c.Y, wx0 - 1.2, wx1 + 1.2, wy0 - 1.2, wy1 + 1.2, g)
        win = rect_uv(c.X, c.Y, wx0, wx1, wy0, wy1, g)
        out = lay(out, "#4a4640", bez)
        out = lay(out, "#f4f0dc", win)
        # the dial: a round knob with a pointer
        dcx, dcy = x0 + 6.2, (y0 + y1) / 2
        rr = np.hypot(c.X - dcx, c.Y - dcy)
        knob = np.clip((4.2 - rr) / g + 0.5, 0, 1)
        out = lay(out, "#b8ac90", knob)
        ptr = (np.abs(c.X - dcx - (c.Y - dcy) * 0.3) < 0.5) & (c.Y > dcy) & (rr < 3.8)
        out = lay(out, "#3a3630", ptr.astype(F32))
        return out
    st.box(x0, x1, y0, y1, 0, dz, m, "thermostat", grp=G, shadow=True)


def intercom(st, lit=False, G="back"):
    """The intercom panel by the door: a gray steel plate, a round speaker grille of little holes, the red button under
    it (dark; lit, while pressed), and a strip of label (DISPATCH: PRESS TO TALK, laid as words)."""
    x0, x1, y0, y1 = M.INTERCOM
    dz = 2.0

    def m(c):
        g = px_of(c, 1.2)
        out = col("#9aa0a6") * (0.95 + 0.07 * fbm(c.X / 5, c.Y / 5, 45, 2))[..., None]
        scx, scy, sr = (x0 + x1) / 2, y1 - 11.5, 7.5
        rr = np.hypot(c.X - scx, c.Y - scy)
        grill = np.clip((sr - rr) / g + 0.5, 0, 1)
        holes = lines_aa(c.X, 1.4, 0.55, g) * lines_aa(c.Y, 1.4, 0.55, g)
        out = lay(out, "#6c7278", grill * 0.5)
        out = out * (1 - (0.45 * holes * grill)[..., None])
        lab = rect_uv(c.X, c.Y, x0 + 2.0, x1 - 2.0, y0 + 3.0, y0 + 8.0, g)
        out = lay(out, "#e8e4d8", lab)
        screws = sum(np.clip((0.7 - np.hypot(c.X - sx, c.Y - sy)) / g + 0.5, 0, 1) for sx in (x0 + 1.8, x1 - 1.8) for sy in (y0 + 1.8, y1 - 1.8))
        return lay(out, "#5a5e64", np.clip(screws, 0, 1))
    st.box(x0, x1, y0, y1, 0, dz, m, "intercom", grp=G, shadow=True)
    bx, by = (x0 + x1) / 2, y0 + 13.0

    def m_btn(c):
        n = normals(c)
        k = col("#ff6a40") if lit else col("#8c241c")
        out = k * (0.85 + 0.25 * np.clip(n[..., 1], 0, 1))[..., None]
        e = (col("#ff7a48") * 0.95 * np.ones_like(out)) if lit else None
        return (out, e) if lit else out
    st.cyl((bx, by), 2.6, dz, dz + 1.6, m_btn, axis="z", name="intercombutton", grp=G, shadow=False)


def poster(st, G="back"):
    """The poster: PECULIAR? REPORT IT. in big letters (laid as words), and between them a cartoon in two inks: a chain
    -link fence across a desert, and in the sky behind it a round hole with a ring round it (a drawing, not a light)."""
    x0, x1, y0, y1 = M.POSTER

    def m(c):
        X, Y = c.X, c.Y
        g = px_of(c, 1.2)
        out = col("#efe6cc") * (0.96 + 0.05 * fbm(X / 7, Y / 7, 47, 2))[..., None]
        # the picture panel: the sky a pale blue, the desert ochre, the fence across, the hole in the sky
        px0, px1, py0, py1 = x0 + 4.0, x1 - 4.0, y0 + 16.0, y1 - 22.0
        pan = rect_uv(X, Y, px0, px1, py0, py1, g)
        sky = col("#a8c8dc")
        desert = col("#d8b070")
        hor = py0 + (py1 - py0) * 0.36
        pic = np.where((Y > hor)[..., None], sky, desert)
        hcx, hcy, hr = px0 + (px1 - px0) * 0.62, py0 + (py1 - py0) * 0.70, (py1 - py0) * 0.17
        rr = np.hypot(X - hcx, (Y - hcy) * 1.05)
        pic = lay(pic, "#2a3048", np.clip((hr - rr) / g + 0.5, 0, 1))
        for k_ in (1.35, 1.75):                              # rings round the hole, as a cartoonist draws a whirl
            ring = np.clip(1 - np.abs(rr - hr * k_) / (g * 0.9 + 0.5), 0, 1)
            pic = lay(pic, "#2a3048", ring * (0.9 if k_ < 1.5 else 0.6))
        spin = np.sin(np.arctan2(Y - hcy, X - hcx) * 3 + rr * 0.9)
        pic = lay(pic, "#5a6488", ((spin > 0.6) & (rr < hr * 0.9)).astype(F32) * 0.6)
        # the fence: posts and a diamond mesh, from the horizon down a little
        fy0, fy1 = hor - 9.0, hor + 3.0
        infence = (Y > fy0) & (Y < fy1)
        mesh = np.maximum(lines_aa(X + Y, 2.2, 0.45, g, fade=False), lines_aa(X - Y, 2.2, 0.45, g, fade=False)) * infence
        posts = lines_aa(X - px0, 11.0, 0.9, g, fade=False) * infence
        rail = band(Y, fy1 - 0.6, fy1 + 0.3, g) * band(X, px0, px1, g)
        pic = lay(pic, "#3a3a44", np.clip(mesh * 0.6 + posts + rail, 0, 1))
        out = out * (1 - pan[..., None]) + pic * pan[..., None]
        frame = 1 - rect_uv(X, Y, x0 + 0.8, x1 - 0.8, y0 + 0.8, y1 - 0.8, g)
        out = lay(out, "#b8ac90", frame * 0.6)
        tape = sum(rect_uv(X, Y, tx - 2.2, tx + 2.2, ty - 1.2, ty + 1.2, g) for tx, ty in ((x0 + 1, y1 - 1), (x1 - 1, y1 - 1)))
        return lay(out, "#e4e0c8", np.clip(tape, 0, 1) * 0.8)
    st.box(x0, x1, y0, y1, 0, 0.3, m, "poster", grp=G, shadow=False)


def mirror(st, reflection=None, G="back"):
    """The one-way mirror: glass in a steel frame, a little ledge under it. From this side it is a mirror, dark: a faint
    reflection of the room (the tubes brightest in it), over the glass's own deep blue-gray. `reflection`: a function
    (X, Y, Z) on the glass -> the room's colour seen in it (office_room.py renders it through the mirror)."""
    x0, x1, y0, y1 = M.MIRROR
    fw = M.MIRROR_FRAME
    m_fr = painted_steel("#50565e", seed=51, chips=0.15)
    st.box(x0 - fw, x1 + fw, y0 - fw, y0, 0, 3.0, m_fr, "mirrorframe", grp=G)
    st.box(x0 - fw, x1 + fw, y1, y1 + fw, 0, 3.0, m_fr, "mirrorframe", grp=G)
    st.box(x0 - fw, x0, y0, y1, 0, 3.0, m_fr, "mirrorframe", grp=G)
    st.box(x1, x1 + fw, y0, y1, 0, 3.0, m_fr, "mirrorframe", grp=G)
    st.box(x0 - fw, x1 + fw, y0 - fw - 2.0, y0 - fw, 0, 7.0, m_fr, "mirrorframe", grp=G)        # the ledge

    def m_glass(c):
        base = col("#151a26") * (0.9 + 0.15 * fbm(c.X / 50, c.Y / 30, 53, 2))[..., None]
        if reflection is None:
            return base
        r = reflection(c.X, c.Y, c.Z)
        foot = np.clip((c.Y - y0) / 40.0, 0.35, 1.0)                 # darker toward its foot (where the chairs are reflected)
        streak = 0.85 + 0.15 * np.clip(np.sin((c.X + c.Y * 0.6) * 0.045), 0, 1)
        return base * 0.6, r * (foot * streak)[..., None]
    st.poly([(x0, y0, 0.8), (x1, y0, 0.8), (x1, y1, 0.8), (x0, y1, 0.8)], m_glass, "mirror", grp=G)


# ---------------------------------------------------------------- the ceiling's fittings
def ceiling_things(st, eyes=False, G_vent="vent", flicker=None):
    for i, t in enumerate(M.TROFFERS):
        st.poly([(t[0], H - 0.4, t[2]), (t[1], H - 0.4, t[2]), (t[1], H - 0.4, t[3]), (t[0], H - 0.4, t[3])],
                m_troffer(t, H, seed=i, flicker_tube=(flicker if i == 1 else None)), f"troffer{i}")
    vx0, vx1, vz0, vz1 = M.VENT
    vent(st, vx0, vx1, vz0, vz1, H, name="vent", grp=G_vent, eyes=None, slats=6, along="z")
    if eyes:                                                  # Ranger's face just above the slats, square to the lens
        face_at_grille(st, ((vx0 + vx1) / 2 + 2.0, H + 1.2, (vz0 + vz1) / 2 + 3.0), View(**M.VIEW), grp=G_vent, eye_r=4.8, glow=1.9)
    sx, sz, sr = M.SPEAKER
    ceiling_speaker(st, sx, sz, sr, H, name="speaker")
    mx, mz, mr = M.SMOKE
    smoke_detector(st, mx, mz, mr, H, name="smoke")
    for (px, pz) in M.SPRINKLERS:
        sprinkler(st, px, pz, H, name="sprinkler")


# ---------------------------------------------------------------- the furniture
def table(st, G="table"):
    """The table: a wood-grain laminate top with a black vinyl edge, on a gray steel frame: an apron and four legs with
    levelling feet."""
    x0, x1, y0, y1, z0, z1 = M.TABLE
    tt = M.TOP_T
    top = laminate(seed=61, grain_dir="z")
    st.box(x0, x1, y1 - tt, y1, z0, z1, {"top": top} and top, "table", grp=G)
    st.box(x0 - 0.4, x1 + 0.4, y1 - tt - 0.2, y1 - 0.4, z0 - 0.4, z1 + 0.4, col("#2a2828"), "tableedge", grp=G, shadow=False)
    st.box(x0, x1, y1 - tt + 0.01, y1 + 0.01, z0, z1, top, "table", grp=G, shadow=False)
    m_fr = painted_steel(STEEL_D, seed=62, chips=0.3)
    ap = 9.0
    st.box(x0 + 4, x1 - 4, y1 - tt - ap, y1 - tt, z0 + 4, z0 + 6, m_fr, "table", grp=G)
    st.box(x0 + 4, x1 - 4, y1 - tt - ap, y1 - tt, z1 - 6, z1 - 4, m_fr, "table", grp=G)
    st.box(x0 + 4, x0 + 6, y1 - tt - ap, y1 - tt, z0 + 4, z1 - 4, m_fr, "table", grp=G)
    st.box(x1 - 6, x1 - 4, y1 - tt - ap, y1 - tt, z0 + 4, z1 - 4, m_fr, "table", grp=G)
    for lx in (x0 + 5, x1 - 5):
        for lz in (z0 + 5, z1 - 5):
            st.box(lx - 1.8, lx + 1.8, 2.0, y1 - tt, lz - 1.8, lz + 1.8, m_fr, "table", grp=G)
            st.cyl((lx, lz), 2.2, 0, 2.0, col("#2a2a2c"), name="table", grp=G, shadow=False)
    st.feet["table"] = (x0, x1, z0, z1)


def questionnaire(st, G="questionnaire"):
    """The questionnaire on the table before Dale: a thick stack of pages (forty-seven, and the green one), a black
    binder clip, the top sheet's ruled boxes (too small to read: the look says what it says)."""
    x0, x1, z0, z1 = M.QUESTIONNAIRE
    y = M.TABLE[3]

    def m(c):
        X, Z = c.X, c.Z
        g = px_of(c, 2.0)
        out = col(PAPER) * (0.96 + 0.04 * fbm(X / 3, Z / 3, 71, 2))[..., None]
        lines = lines_aa(Z - z0, 2.4, 0.4, g) * rect_uv(X, Z, x0 + 3, x1 - 3, z0 + 6, z1 - 3, g)
        out = out * (1 - 0.18 * lines[..., None])
        head = rect_uv(X, Z, x0 + 3, x1 - 3, z0 + 2, z0 + 5, g)
        return lay(out, "#3c3c48", head * 0.6)

    def m_side(c):
        stripes = 0.5 + 0.5 * np.sin(c.Y * 22.0)
        out = col("#e8e4d8") * (0.88 + 0.12 * stripes)[..., None]
        green = band(c.Y, y + 2.2, y + 2.6, px_of(c, 1.0))
        return lay(out, "#6aa868", green * 0.9)
    st.box(x0, x1, y, y + 4.6, z0, z1, m_side, "questionnaire", grp=G)
    st.poly([(x0, y + 4.62, z0), (x1, y + 4.62, z0), (x1, y + 4.62, z1), (x0, y + 4.62, z1)], m, "questionnaire", grp=G)
    st.box((x0 + x1) / 2 - 2.5, (x0 + x1) / 2 + 2.5, y + 3.0, y + 6.2, z0 - 0.6, z0 + 2.4, col("#1c1c20"), "questionnaire", grp=G, shadow=False)


def chairs(st, G_corner="chair-corner"):
    for k, (X, Z, f) in M.CHAIRS.items():
        stacking_chair(st, X, Z, "+x" if f > 0 else "-x", "chair-" + k, grp="back", seat=M.SEAT, back_top=M.CHAIR_BACK, seed=80 + len(k))
    cx, cz = M.CORNER_CHAIR
    stacking_chair(st, cx, cz, "+z", "chair-corner", grp=G_corner, seat=M.SEAT, back_top=M.CHAIR_BACK, seed=88, ang=8.0)


def cooler(st, G="back", bubble=None):
    """The water cooler against the right wall: a cream cabinet, a big blue-tinted jug upside down on top, two taps
    (a red, a blue), a drip tray; the paper cones in their tube on its side, and a few used ones in a little bin."""
    x0, x1, y0, y1, z0, z1 = M.COOLER
    m_cab = painted_steel("#e2ddd0", seed=91, amt=0.05)
    st.box(x0, x1, 0, 98, z0, z1, m_cab, "cooler", grp=G)
    st.box(x0 - 1.0, x1, 96, 100, z0 - 1.0, z1 + 1.0, painted_steel("#d0cabc", seed=92), "cooler", grp=G)
    cxj, czj = (x0 + x1) / 2, (z0 + z1) / 2

    def m_jug(c):
        n = normals(c)
        k = col("#a8cce4")
        water = (c.Y < 100 + 34)
        out = np.where(water[..., None], k * 0.85, k * 1.05)
        rim = np.clip(np.abs(n[..., 0]) - 0.6, 0, 1)
        e = col("#d8ecf8") * (np.clip(n[..., 1], 0, 1) ** 6 * 0.25 + rim * 0.15)[..., None]
        return out * (0.9 + 0.2 * np.clip(n[..., 2], 0, 1))[..., None], e
    st.cyl((cxj, czj), 13.5, 104, 136, m_jug, name="cooler", grp=G)
    st.ball((cxj, 136, czj), 13.5, m_jug, name="cooler", grp=G, squash=(1.0, 0.45, 1.0))
    st.cyl((cxj, czj), 5.0, 100, 104, col("#7aa8c8"), name="cooler", grp=G)
    if bubble is not None and bubble < 6:
        # a bubble going up in the jug, on its side toward us (frames bubble-0 .. bubble-5; bubble-none is the jug at rest)
        dx, dz = 91.0 - cxj, 617.0 - czj
        dl = math.hypot(dx, dz)
        k = 13.8 + 0.2 * bubble
        st.ball((cxj + dx / dl * k, 106.0 + 4.6 * bubble, czj + dz / dl * k), 1.1 + 0.12 * bubble, lambda c: (col("#e8f4fc") * np.ones(np.shape(c.X) + (3,), F32),
                col("#f4fbff") * 0.55 * np.ones(np.shape(c.X) + (3,), F32)), name="bubble", grp="bubble", shadow=False)
    # the taps, on the front (the side facing -X, into the room)
    for i, (tc) in enumerate(("#c03028", "#3060b8")):
        tz = czj + (-6 if i == 0 else 6)
        st.box(x0 - 3.0, x0, 80, 85, tz - 1.6, tz + 1.6, col(tc), "cooler", grp=G, shadow=False)
    st.box(x0 - 7.0, x0, 60, 62, czj - 10, czj + 10, col("#7a7e84"), "cooler", grp=G, shadow=False)          # the drip tray
    # the paper cones: a white tube on the cooler's near side, cones nesting in it, one sticking out of its mouth
    tx, tz = x0 + 8.0, z1 + 3.5
    st.cyl((tx, tz), 3.4, 70, 118, painted_steel("#f0eee6", seed=93), name="cones", grp=G)
    st.cyl((tx, tz), 3.6, 64.0, 70.0, col("#f6f4ee"), name="cones", grp=G, r1=1.0)
    st.feet["cooler"] = (x0, x1, z0, z1)


def lamp(st, G="back"):
    """The floor lamp in the far corner, unlit (no unauthorized lighting): a brass pole on a round foot, a pleated
    rose-colored shade with a fringe, its cord coiled on the carpet with the plug, unplugged."""
    lx, lz, r = M.LAMP
    brass = col("#b89850")
    st.cyl((lx, lz), 13.0, 0, 2.5, brass, name="lamp", grp=G)
    st.stick((lx, 2.5, lz), (lx, 150.0, lz), 1.1, brass, "lamp", grp=G)

    def m_shade(c):
        ang = np.arctan2(c.X - lx, c.Z - lz)
        pleat = 0.5 + 0.5 * np.sin(ang * 26)
        out = col("#d89a84") * (0.82 + 0.18 * pleat)[..., None]
        return out
    st.cyl((lx, lz), r, 140, 162, m_shade, r1=r * 0.62, name="lamp", grp=G, hollow=False)
    for i in range(36):                                    # the fringe
        a = 2 * math.pi * i / 36
        fx, fz = lx + math.sin(a) * r * 1.0, lz + math.cos(a) * r * 1.0
        st.stick((fx, 140.0, fz), (fx, 135.5, fz), 0.35, col("#e8c0a0"), "lamp", grp=G, shade=False)
    st.feet["lamp"] = (lx - 13, lx + 13, lz - 13, lz + 13)
    pts = curve3([(lx - 4, 0.4, lz + 8), (lx - 18, 0.4, lz + 22), (lx - 30, 0.4, lz + 16), (lx - 34, 0.4, lz + 30)], 5)
    st.rope(pts, 0.4, col("#3a3a3c"), name="lamp", grp=G)
    st.box(lx - 37, lx - 32, 0, 2.0, lz + 30, lz + 34, col("#e6e2d8"), "lamp", grp=G, shadow=False)


def plant(st, droop=False, G="plant"):
    """The plastic plant against the right wall near us: a ficus in a plastic pot of no particular colour, a trunk and a
    round crown of stiff glossy leaves. Drooping (the room is hot): the same plant, the crown sagged and every leaf
    hanging. A plastic plant cannot droop. It does."""
    px, pz, pr = M.PLANT
    pot_h = 34.0

    def m_pot(c):
        n = normals(c)
        out = col("#a86a44") * (0.85 + 0.2 * np.clip(n[..., 1] * 0.5 + n[..., 2] * 0.5 + 0.3, 0, 1))[..., None]
        rib = 0.5 + 0.5 * np.sin(c.Y * 1.5)
        return out * (0.95 + 0.05 * rib)[..., None]
    st.cyl((px, pz), pr * 0.78, 0, pot_h, m_pot, r1=pr, name="plant", grp=G)
    st.cyl((px, pz), pr * 1.04, pot_h - 3.0, pot_h, m_pot, name="plant", grp=G)
    st.cyl((px, pz), pr * 0.95, pot_h - 1.5, pot_h - 0.5, col("#3a2c22"), name="plant", grp=G, shadow=False)     # its "soil": foam pebbles
    st.feet["plant"] = (px - pr, px + pr, pz - pr, pz + pr)
    rng = np.random.default_rng(7)
    leaf_c = [col("#3f8a44"), col("#4e9c4a"), col("#2f7238"), col("#5aa852"), col("#468f40")]
    # the crown: a round mass whose middle is up the trunk; drooping, it sags lower and leans out from the wall
    if not droop:
        ccx, ccy, ccz, rx, ry, rz = px - 4.0, pot_h + 98.0, pz, 30.0, 26.0, 26.0
    else:
        ccx, ccy, ccz, rx, ry, rz = px - 14.0, pot_h + 66.0, pz + 4.0, 32.0, 22.0, 27.0
    trunk = [(px, pot_h - 1, pz), (px - 1.0, pot_h + 30, pz), ((px + ccx) / 2, (pot_h + 30 + ccy) / 2, (pz + ccz) / 2), (ccx, ccy - 6, ccz)]
    st.rope(curve3(trunk, 4), 1.5, col("#6a5040"), name="plant", grp=G)
    for i in range(70):
        # a place on the crown's shell (more on its top and its near side), and a leaf there, turned to its own way
        u, v = rng.uniform(-1, 1), rng.uniform(0, 2 * math.pi)
        sy = u if not droop else (u * 0.8 - 0.25)
        rr = math.sqrt(max(0.0, 1 - u * u))
        lx, ly, lz = ccx + rx * rr * math.cos(v) * rng.uniform(0.75, 1.0), ccy + ry * sy * rng.uniform(0.8, 1.0), ccz + rz * rr * math.sin(v) * rng.uniform(0.75, 1.0)
        if lx > M.W - 3:
            continue
        if not droop:
            sq = (1.0, 0.40, 0.62)
            ly2 = ly
        else:
            sq = (0.48, 1.15, 0.48)
            ly2 = ly - 3.5 - 4.0 * (1 - u) * 0.5
        st.ball((lx, ly2, lz), 4.4 + rng.uniform(-0.6, 0.8), leaf_c[i % 5] * (0.92 + 0.16 * rng.random()), name="plant", grp=G, squash=sq, shadow=False)
    # a few twigs out to the leaves at the crown's edge
    for i in range(6):
        v = 2 * math.pi * i / 6 + 0.3
        tip = (ccx + math.cos(v) * rx * 0.8, ccy + (6 if not droop else -10), ccz + math.sin(v) * rz * 0.8)
        st.stick((ccx, ccy - 4, ccz), tip, 0.45, col("#5a5a40"), "plant", grp=G)


def basket(st, G="front"):
    """The wastebasket near us at the left: gray steel mesh, crumpled pages of questionnaire in it."""
    bx, bz, r, h = M.BASKET
    def m_mesh(c):
        ang = np.arctan2(c.X - bx, c.Z - bz)
        g = px_of(c, 1.0)
        mesh = np.maximum(lines_aa(ang * r + c.Y, 2.0, 0.5, g, fade=False), lines_aa(ang * r - c.Y, 2.0, 0.5, g, fade=False))
        out = col("#5e636a") * (0.9 + 0.2 * mesh)[..., None]
        return out
    st.cyl((bx, bz), r * 0.86, 0, h, m_mesh, r1=r, name="basket", grp=G)
    st.cyl((bx, bz), r * 1.02, h - 1.5, h, col("#4a4e54"), name="basket", grp=G)
    rng = np.random.default_rng(11)
    for i in range(4):
        a = rng.uniform(0, 2 * math.pi)
        cxp, cyp, czp = bx + math.cos(a) * r * 0.42, h + 0.5 + rng.uniform(0, 3), bz + math.sin(a) * r * 0.42
        for j in range(7):                                   # a crumpled sheet: lumps and creases
            off = rng.normal(0, 2.2, 3)
            st.ball((cxp + off[0], cyp + abs(off[1]) * 0.8, czp + off[2]), 2.4 + rng.uniform(0, 1.4), col("#ece8dc") * (0.85 + 0.15 * rng.random()),
                    name="basket", grp=G, squash=(1.0, 0.7 + 0.3 * rng.random(), 0.8), shadow=False)


def filebox(st, G="front"):
    """A box of spare questionnaires on the floor near us: a brown file box, its lid on, a stencilled label on its end
    toward us (laid as words), and a stack of loose copies on its lid with a rubber band round them."""
    x0, x1, y0, y1, z0, z1 = M.FILEBOX
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    w, d = x1 - x0, z1 - z0

    def m_card(c):
        n = normals(c)
        out = col("#b89466") * (0.92 + 0.10 * fbm(c.X / 6, (c.Y + c.Z) / 6, 121, 2))[..., None]
        out = out * (0.9 + 0.1 * np.clip(n[..., 1], 0, 1))[..., None]
        # a white label pasted on the end toward us (its words are laid later)
        q = filebox_label()
        lab = _in_quad(c, q)
        return lay(out, "#ece6d4", lab)
    obox(st, (cx, 0.0, cz), (w, y1 - 2.0, d), M.FILEBOX_ANG, m_card, "filebox", grp=G)
    obox(st, (cx, y1 - 3.0, cz), (w + 1.4, 3.0, d + 1.4), M.FILEBOX_ANG, painted_like("#a07e52"), "filebox", grp=G)

    def m_paper(c):
        out = col(PAPER) * (0.94 + 0.06 * fbm(c.X / 2, c.Z / 2, 122, 2))[..., None]
        edges = 0.5 + 0.5 * np.sin(c.Y * 30.0)
        return out * (0.92 + 0.08 * edges)[..., None]
    obox(st, (cx - 2.0, y1, cz + 1.0), (30.0, 6.0, 22.0), M.FILEBOX_ANG + 9.0, m_paper, "filebox", grp=G)
    obox(st, (cx - 2.0, y1 + 2.6, cz + 1.0), (30.6, 0.9, 1.2), M.FILEBOX_ANG + 9.0, col("#c03a2a"), "filebox", grp=G, shadow=False)


def painted_like(hexc):
    k = col(hexc)

    def f(c):
        return k * (0.94 + 0.08 * fbm(c.X / 6, c.Z / 6, 123, 2))[..., None]
    return f


def filebox_label():
    """The box's label, on its end toward us: four corners in the room (top left, top right, bottom right, bottom left)."""
    x0, x1, y0, y1, z0, z1 = M.FILEBOX
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    w, d = x1 - x0, z1 - z0
    a = math.radians(M.FILEBOX_ANG)
    ux, uz = math.cos(a), -math.sin(a)
    vx, vz = math.sin(a), math.cos(a)

    def P(sx, sy, sz):
        return (cx + ux * sx + vx * sz, sy, cz + uz * sx + vz * sz)
    hz = d / 2 + 0.25
    return [P(-w / 2 + 3, y1 - 6, hz), P(w / 2 - 3, y1 - 6, hz), P(w / 2 - 3, 6, hz), P(-w / 2 + 3, 6, hz)]


def _in_quad(c, q):
    """1 where a place of the end toward us lies inside the label's quad (its corners, as filebox_label gives them)."""
    (ax, ay, az), (bx, by, bz), (cx_, cy_, cz_), _ = q
    ux, uz = bx - ax, bz - az
    L = math.hypot(ux, uz)
    s_ = ((c.X - ax) * ux + (c.Z - az) * uz) / (L * L)
    t_ = (ay - c.Y) / (ay - cy_)
    return ((s_ >= -0.02) & (s_ <= 1.02) & (t_ >= -0.04) & (t_ <= 1.04)).astype(F32)

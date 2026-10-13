"""Everything that stands, hangs or lies in the store, built in the room's own centimetres (nevada_store.py): the
counter and what is on it, Harold the cooler, the grill and the roller, the spinner rack, the shelves, the rock
bins, Jolene's chair and the pay phone, the bulletin board, the hats, the hundred and twelve hubcaps, the fan that
has not turned since 1979, and the things in the foreground.

Each function puts one group of things on the Stage, each with a paint that colours it in ITS OWN measurements.
Groups (`grp`) are the cut-outs: "counter", "cooler", "spinner", "mirror", "rockbins", "hat-1" .. "hat-5", "front";
everything else is the backdrop ("back"). All measurements come from nevada_store_model.py. Every label is a plain
word or a made-up thing: no brand, no logo, nobody's typeface."""

import math

import numpy as np

from brush import F32, lerp
import nevada_store_model as M
from nevada_store_kit import normals, col, mixc, vnoise, fbm, hashf, grad_of, lines_aa, band, rect, disc, lay, sstep, curve3, pen_mask
from nevada_store_things import plain, wood, metal, rm, rect_uv, disc_uv, OUTSIDE

PAPER = "#f1ead6"


def chrome(tint="#c8ccd2", glint=0.5, seed=0, warm=0.0):
    """Chrome or polished steel: what it shows is the room, so it is mostly a mid grey that takes the light, with a
    bright streak where it faces the window (to the left of us) and a dark one where it faces the floor."""
    k = col(tint)

    def f(c):
        n = normals(c)
        face_win = np.clip(-n[:, 0] * 0.7 + n[:, 1] * 0.5 + n[:, 2] * 0.3, 0, 1)
        dark = np.clip(-n[:, 1] * 0.8 + n[:, 0] * 0.3, 0, 1)
        out = k[None, :] * (0.55 + 0.6 * face_win - 0.35 * dark)[:, None]
        out = out * (0.92 + 0.16 * fbm(c.X / 3 + seed, (c.Y + c.Z) / 3, 7 + seed, 2))[:, None]
        e = col("#fff4e0")[None, :] * (np.clip(face_win - 0.62, 0, 1) * glint * 2.2)[:, None]
        if warm:
            out = lerp(out, out * col("#e8b878"), warm)
        return out, e
    return f


def obox(st, c, size, ang, mat, name=None, grp="back", flag=0, shadow=True, faces=("left", "right", "top", "front", "back", "bottom")):
    """A box turned about the upright through its middle by `ang` degrees (positive turns its front toward +X).
    c: the middle of its foot (X, Y0, Z). size: (width along its own x, height, depth along its own z)."""
    w, h, dpt = size
    a = math.radians(ang)
    ux, uz = math.cos(a), -math.sin(a)                   # its own x axis on the floor plan
    vx, vz = math.sin(a), math.cos(a)                    # its own z axis (toward its front)
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


# ---------------------------------------------------------------- the counter, and what is on it
def counter(st, G="counter", roller_phase=None):
    x0, x1, y0, y1, z0, z1 = M.COUNTER
    # the body: painted boards, barn red, a cream rail along the top of the front, a dark kick plate, boots' scuffs
    def m_front(c):
        if c.face != "front":
            return col("#8a3828") * (0.9 + 0.2 * fbm(c.X / 20, c.Y / 20, 3, 2))[..., None]
        X, Y = c.X, c.Y
        g = c.fp
        ib = np.floor((X - x0) / 14.0)
        base = col("#a8432f") * (0.86 + 0.24 * hashf(ib, 4))[..., None] * (0.92 + 0.16 * fbm(X / 3, Y / 40, 5, 2))[..., None]
        groove = np.clip(1.2 - np.abs(((X - x0) / 14.0) - np.round((X - x0) / 14.0)) * 14.0 / np.maximum(g, 0.3), 0, 1)
        base = base * (1 - 0.35 * groove[..., None])
        scuff = np.clip((fbm(X / 8, Y / 4, 6, 3) - 0.5) * 3, 0, 1) * np.clip((26 - Y) / 18, 0, 1)
        base = lerp(base, col("#d8b89a"), (scuff * 0.45)[..., None])
        worn = np.clip((fbm(X / 25, Y / 25, 7, 3) - 0.6) * 3, 0, 1)
        base = lerp(base, col("#b89070"), (worn * 0.35)[..., None])
        rail = rm(Y, y1 - 12, y1 - 3, g)
        base = lerp(base, col("#e2d0a4") * (0.9 + 0.2 * fbm(X / 30, Y, 8, 2))[..., None], rail[..., None])
        kick = rm(Y, -1, 10, g)
        base = lerp(base, col("#3a2a24"), kick[..., None])
        return base
    st.box(x0, x1, 0, y1 - 3, z0 + 2, z1, m_front, "counter", grp=G, foot=True)
    # the top: a pale laminate with little boomerangs on it, worn through to brown where the money changes hands
    def m_top(c):
        X, Z = c.X, c.Z
        base = col("#e8dcb8") * (0.94 + 0.1 * fbm(X / 6, Z / 6, 9, 2))[..., None]
        bx, bz = (X % 23.0) - 11.5, (Z % 17.0) - 8.5
        boom = (np.abs(np.hypot(bx * 0.9, bz * 1.3) - 4.5) < 0.55) & (bx > -1) & (np.abs(bz) < 3.5)
        base = np.where(boom[..., None], col("#7aa8b8"), base)
        wear = np.exp(-(((X - 360) / 60) ** 2) - (((Z - 150) / 14) ** 2)) * 0.6 + np.exp(-(((X - 250) / 50) ** 2) - (((Z - 150) / 12) ** 2)) * 0.4
        return lerp(base, col("#a88a64"), (wear * 0.7)[..., None])
    st.box(x0 - 2, x1 + 2, y1 - 3, y1, z0, z1 + 3, m_top, "counter", grp=G)
    st.box(x0 - 2.5, x1 + 2.5, y1 - 3.5, y1 - 0.5, z1 + 2.5, z1 + 3.6, chrome("#c0c4c8", 0.6, 1), "counter", grp=G, shadow=False)   # the chrome edge
    # the end panels (seen at the left end)
    st.box(x0 - 1, x0 + 1, 0, y1 - 3, z0, z1, wood("#7a4a30", 3, "y", 0.2), "counter", grp=G, shadow=False)
    # the shelf under the counter on Jolene's side (seen past the left end): paper bags, a cigar box
    st.box(x0 + 4, x0 + 60, 20, 22, z0 - 30, z0, wood("#8a6040", 4), "counter", grp=G, shadow=False)
    st.box(x0 + 8, x0 + 30, 22, 34, z0 - 24, z0 - 4, plain("#c8a878", 0.15, 4, 3), "counter", grp=G, shadow=False)

    register(st, G)
    eggs(st, G)
    pennydish(st, G)
    postcards(st, G)
    maprack(st, G)
    basket(st, G)
    grill(st, G, roller_phase)


def register(st, G):
    """An old brass cash register on the counter, turned a little toward the room: the tall back with the window
    where the amount shows, a sloping bank of round keys on Jolene's side, a crank, the drawer."""
    x0, x1, y0, y1, z0, z1 = M.REGISTER
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    ang = -24.0                                          # its front (the keys) faces Jolene and a little toward the window
    brass = chrome("#c9a254", 0.55, 3, 0.0)
    dark = plain("#3a2c20", 0.1, 4, 4)
    # the drawer and the body
    P = obox(st, (cx, y0, cz), (54, 14, 44), ang + 180, brass, "register", grp=G)
    P2 = obox(st, (cx, y0 + 14, cz + 2), (50, 22, 36), ang + 180, brass, "register", grp=G)
    # the sloping keyboard (on the far side) as a wedge of keys: we see their tops over the body
    for row in range(3):
        for k in range(7):
            sx = -18 + k * 6
            sz = -14 + row * 6
            q = P2(sx, 22 + 2 + row * 3.0, sz)
            st.cyl((q[0], q[2]), 2.0, q[1], q[1] + 2.2, plain(["#f2ead6", "#e8d8b8", "#d8382c"][(row + k) % 3 if row == 0 else 0], 0.05, 2, 5),
                   name="register", grp=G, shadow=False)
            st.stick((q[0], q[1] - 3, q[2]), (q[0], q[1] + 0.2, q[2]), 0.6, col("#8a7040"), "register", grp=G)
    # the tall back with the amount window, facing the customer (toward us)
    P3 = obox(st, (cx, y0 + 36, cz + 12), (42, 22, 10), ang, {"front": None, "back": brass, "left": brass, "right": brass, "top": brass, "bottom": None}, "register", grp=G)
    def m_window(c):
        k = col("#1e1a18")
        # the little flags: $ 0 . 0 0, white on black
        u = c.U
        v = c.V
        flags = (np.abs(((u + 1.0) % 5.0) - 2.5) < 1.4) & (v > 2.0) & (v < 7.0)
        return np.where(flags[..., None], col("#f4ecd6"), k)
    q0, q1, q2, q3 = P3(-15, 6, 5.2), P3(15, 6, 5.2), P3(15, 16, 5.2), P3(-15, 16, 5.2)
    st.poly([q0, q1, q2, q3], m_window, "register", grp=G)
    for (sx0, sx1, sy0, sy1) in ((-21, 21, 0, 6), (-21, 21, 16, 22), (-21, -15, 6, 16), (15, 21, 6, 16)):
        st.poly([P3(sx0, sy0, 5.0), P3(sx1, sy0, 5.0), P3(sx1, sy1, 5.0), P3(sx0, sy1, 5.0)], brass, "register", grp=G)
    # an ornamented crest on top, and the crank on its side
    top = P3(0, 22, 0)
    st.ball((top[0], top[1] + 1, top[2]), 5.0, brass, "register", grp=G, squash=(1.8, 0.6, 0.4), shadow=False)
    crank = P2(27, 12, 0)
    st.stick(crank, (crank[0] + 6, crank[1] - 4, crank[2] + 4), 0.9, col("#a88a4a"), "register", grp=G)
    st.ball((crank[0] + 6.5, crank[1] - 4.5, crank[2] + 4.5), 1.6, plain("#2a2020", 0.1), "register", grp=G, shadow=False)


def eggs(st, G):
    """The jar of pickled eggs: a big glass jar, the eggs pale in a yellowish brine, a tin lid, older than the eggs."""
    X, Y0, Y1, Z, R = M.EGGS
    def m_jar(c):
        if c.face == "round" and (c.kind <= 2).any():
            pass
        ang = c.ang
        Yn = (c.Y - Y0) / (Y1 - Y0)
        brine = lerp(col("#d8c878"), col("#b8a458"), np.clip(Yn, 0, 1)[..., None])
        # the eggs inside, seen through the glass: pale ovals in rows
        ex = (ang * 3.0) % 1.0
        ey = ((c.Y - Y0) / 9.0) % 1.0
        egg = (np.hypot((ex - 0.5) * 1.6, (ey - 0.5) * 1.15) < 0.42) & (c.Y < Y1 - 10)
        k = np.where(egg[..., None], col("#f4ecd0"), brine)
        k = k * (0.9 + 0.15 * fbm(c.X / 2, c.Y / 2, 11, 2))[..., None]
        top = c.Y > Y1 - 9
        k = np.where(top[..., None], col("#e8e0c0") * 0.8, k)
        # the glass's own shine: a bright streak on the side toward the window
        n = normals(c)
        streak = np.clip(1 - np.abs(np.arctan2(n[:, 2], n[:, 0]) - 2.2) * 4, 0, 1)
        return k, col("#ffffff")[None, :] * (streak * 0.6)[:, None]
    st.cyl((X, Z), R, Y0, Y1, m_jar, name="eggs", grp=G, cap=col("#d8cc90"))
    st.cyl((X, Z), R * 0.9, Y1, Y1 + 4, chrome("#b8b0a0", 0.4, 4), name="eggs", grp=G, shadow=False)
    st.cyl((X, Z), R * 0.92, Y1 + 4, Y1 + 5, plain("#8a7a60", 0.1), name="eggs", grp=G, shadow=False)


def pennydish(st, G):
    """The take-a-penny dish: a chipped saucer with a few pennies in it, and a little card propped behind."""
    x0, x1, y0, y1, z0, z1 = M.PENNYDISH
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    st.cyl((cx, cz), 11.0, y0, y0 + 1.6, plain("#ece4d0", 0.08, 3, 6), r1=12.5, name="pennydish", grp=G, shadow=False)
    st.cyl((cx, cz), 7.0, y0 + 1.6, y0 + 1.9, plain("#e2d8c2", 0.05, 3, 7), name="pennydish", grp=G, shadow=False)
    rng = np.random.default_rng(14)
    for i in range(7):
        a, r = rng.random() * 6.28, rng.random() ** 0.5 * 6.0
        st.cyl((cx + math.cos(a) * r, cz + math.sin(a) * r), 0.95, y0 + 1.9 + i * 0.08, y0 + 2.1 + i * 0.08, plain("#c87a3a", 0.1, 1, 9),
               name="pennydish", grp=G, shadow=False, cap=col("#d88a48"))
    # the card: TAKE A PENNY / LEAVE A PENNY, too small to read from here, but it is there
    m = pen_mask(["TAKE A PENNY", "LEAVE A PENNY"], 16, 9, 2.4, res=20, seed=4)
    def m_card(c):
        tx = np.clip(c.U * 20, 0, m.shape[1] - 1.001).astype(np.intp)
        ty = np.clip((9 - c.V) * 20, 0, m.shape[0] - 1.001).astype(np.intp)
        ink = m[ty, tx]
        return lerp(col(PAPER), col("#3a3060"), ink[..., None] * 0.9)
    st.poly([(cx - 8, y0, cz - 9), (cx + 8, y0, cz - 9), (cx + 8, y0 + 9, cz - 11.5), (cx - 8, y0 + 9, cz - 11.5)], m_card, "pennydish", grp=G)


def postcards(st, G):
    """A wire postcard spinner on the counter's left end: three tiers of cards, desert views, a little faded."""
    X, Y0, Y1, Z, R = M.POSTCARDS
    st.cyl((X, Z), 6.0, Y0, Y0 + 2, plain("#4a4a4a", 0.1), name="postcards", grp=G)
    st.stick((X, Y0, Z), (X, Y1, Z), 0.6, col("#8a8a8a"), "postcards", grp=G)
    views = [("#e8904a", "#5a9cc8", "#a8482c"), ("#f0c060", "#7ab0d8", "#c06038"), ("#d86a5a", "#e8b860", "#5a3a5a"),
             ("#88b8d8", "#e8d8a8", "#8a6a4a"), ("#f0a070", "#4a80b8", "#3a6a3a"), ("#c8d8e0", "#e8c890", "#b86a48")]
    for tier, ty in enumerate((Y0 + 6, Y0 + 26, Y0 + 46)):
        for k in range(6):
            a = math.radians(k * 60 + tier * 20 + 15)
            nx, nz = math.cos(a), math.sin(a)
            tx, tz = -nz, nx
            cxp, czp = X + nx * (R - 3), Z + nz * (R - 3)
            v = views[(k + tier * 2) % len(views)]
            def m_card(c, v=v, k=k, tier=tier):
                f = np.clip(c.V / 14.0, 0, 1)
                sky = lerp(col(v[1]), col(v[0]), (1 - f)[..., None] * 0.6)
                land = (c.V < 5 + 2.5 * np.sin(c.U * 0.9 + k))
                out = np.where(land[..., None], col(v[2]), sky)
                border = (c.U < 0.8) | (c.U > 9.2) | (c.V < 0.8) | (c.V > 13.2)
                out = np.where(border[..., None], col("#f4ecdc"), out)
                return out * 0.92
            pts = [(cxp - tx * 5, ty, czp - tz * 5), (cxp + tx * 5, ty, czp + tz * 5), (cxp + tx * 5, ty + 14, czp + tz * 5), (cxp - tx * 5, ty + 14, czp - tz * 5)]
            st.poly(pts, m_card, "postcards", grp=G, flag=1)
    st.ball((X, Y1 + 1, Z), 1.4, col("#a8a8a8"), "postcards", grp=G, shadow=False)


def maprack(st, G):
    """A wire rack hung on the counter's front: road maps in its pockets, folded, their covers bright."""
    x0, x1, y0, y1, z0, z1 = M.MAPRACK
    wire = col("#9a9a96")
    for xx in (x0, x1):
        st.stick((xx, y0, z1), (xx, y1, z1), 0.5, wire, "maprack", grp=G)
    covers = ["#2f63b8", "#d63f2a", "#e8b030", "#2fa673", "#e9772b", "#3f7fb8", "#c9375e", "#f0d070"]
    for row, yy in enumerate((y0 + 2, y0 + 22, y0 + 42)):
        st.stick((x0, yy, z1 + 1), (x1, yy, z1 + 1), 0.45, wire, "maprack", grp=G)
        n = 3
        for k in range(n):
            u0 = x0 + 2 + k * (x1 - x0 - 4) / n
            u1 = u0 + (x1 - x0 - 4) / n - 2
            cvr = covers[(row * 3 + k) % len(covers)]
            def m_map(c, cvr=cvr, row=row, k=k):
                v = c.V / 20.0
                band_ = (v > 0.66) & (v < 0.86)
                out = np.where(band_[..., None], col("#f4ecd8"), col(cvr))
                road = np.abs(c.U - 6 - 3 * np.sin(c.V * 0.4 + k)) < 0.6
                out = np.where((road & (v < 0.6))[..., None], col("#f4ecd8"), out)
                title = (v > 0.7) & (v < 0.82) & (np.abs(((c.U * 1.3) % 2.2) - 1.1) < 0.55)
                return np.where(title[..., None], col("#3a3060"), out)
            st.poly([(u0, yy + 1, z1 + 1.5), (u1, yy + 1, z1 + 1.5), (u1, yy + 19, z1 + 0.5), (u0, yy + 19, z1 + 0.5)], m_map, "maprack", grp=G)


def basket(st, G):
    """Ranger's basket at the counter's foot, on our side: a round wicker basket, its lid tipped half off and resting
    on the rim, and inside, in the dark, a glint (the stash: a coin among the bottle caps)."""
    x0, x1, y0, y1, z0, z1 = M.BASKET
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    r = (x1 - x0) / 2
    def m_wicker(c):
        a = np.asarray(c.ang) if hasattr(c, "ang") else c.X * 0.1
        weave = np.sin(a * 22 + np.floor(c.Y / 2.4) * 1.7) * 0.5 + 0.5
        rows = np.abs(((c.Y / 2.4) % 1) - 0.5) < 0.12
        k = lerp(col("#a8783e"), col("#dcae66"), weave[..., None])
        k = np.where(rows[..., None], k * 0.7, k)
        return k * (0.9 + 0.2 * fbm(c.X / 3, c.Y / 3, 12, 2))[..., None]
    st.cyl((cx, cz), r, y0, y1, m_wicker, r1=r * 1.08, name="basket", grp=G, foot=True, hollow=True)
    st.cyl((cx, cz), r * 0.96, y0, y0 + 1.5, plain("#1e140c", 0.1), name="basket", grp=G, shadow=False)          # the dark inside
    st.ball((cx + 1, y1 - 7, cz - 2), r * 0.8, plain("#2a1c10", 0.1), "basket", grp=G, shadow=False, squash=(1.0, 0.35, 1.0))   # the heap of the stash, dim
    st.cyl((cx - 3, cz - 5), 3.2, y1 - 3.2, y1 - 2.4, chrome("#e8ecf0", 1.4, 5), name="basket", grp=G, shadow=False, emi=col("#fff8e8") * 2.2)   # the glint
    st.cyl((cx + 6, cz - 2), 1.8, y1 - 3.6, y1 - 3.0, plain("#c8a050", 0.1), name="basket", grp=G, shadow=False)      # a bottle cap
    # the lid, tipped: half off to the right, resting on the rim and the floor
    def m_lid(c):
        U = c.U if hasattr(c, "U") else c.X + c.Z
        V_ = c.V if hasattr(c, "V") else c.Y
        rr = np.hypot(U, V_)
        weave = np.sin(rr * 2.2) * 0.5 + 0.5
        k = lerp(col("#9a6c36"), col("#d0a058"), weave[..., None])
        rim = rr > r * 0.86
        return np.where(rim[..., None], col("#6a4420"), k)
    st.disc3((x1 + 8, y1 * 0.55, cz + 4), r * 1.05, (0.75, 0.55, 0.36), m_lid, sides=22, name="basket", grp=G)
    st.ball((x1 + 6, y1 * 0.55 + 12, cz + 6), 2.0, plain("#7a5228", 0.1), "basket", grp=G, shadow=False, squash=(1.0, 0.6, 1.0))   # its knob


def grill(st, G, roller_phase=None):
    """The grill unit at the counter's right end: a stainless cabinet, the griddle (cold since 1979), a scraper,
    and the hot dog roller on it, turning, empty (its two frames are painted by nevada_store.py)."""
    x0, x1, y0, y1, z0, z1 = M.GRILL
    steel = chrome("#b4b8bc", 0.35, 6)
    def m_cab(c):
        if c.face != "front":
            return col("#9ca0a4") * (0.9 + 0.1 * fbm(c.Z / 10, c.Y / 10, 13, 2))[..., None]
        X, Y = c.X, c.Y
        k = col("#a8acb0") * (0.85 + 0.25 * fbm(X / 2, Y / 30, 14, 2))[..., None]           # brushed
        door = rm(X, x0 + 6, x1 - 6, c.fp) * rm(Y, 12, 80, c.fp) - rm(X, x0 + 7, x1 - 7, c.fp) * rm(Y, 13, 79, c.fp)
        k = lay(k, "#5a5e62", np.clip(door, 0, 1) * 0.8)
        handle = rm(X, x0 + 12, x1 - 12, c.fp) * rm(Y, 70, 73, c.fp)
        k = lay(k, "#e0e4e8", handle * 0.9)
        kick = rm(Y, -1, 9, c.fp)
        return lay(k, "#2a2a2c", kick)
    st.box(x0, x1, y0, y1, z0, z1, m_cab, "grill", grp=G, foot=True)
    gx0, gx1, gy0, gy1, gz0, gz1 = M.GRIDDLE
    st.box(gx0, gx1, gy0, gy1, gz0, gz1, plain("#2c2a2a", 0.15, 4, 15), "grill", grp=G)
    st.box(gx0 - 1, gx1 + 1, gy1, gy1 + 7, gz0 - 1, gz0 + 1, steel, "grill", grp=G, shadow=False)      # the splash guard
    st.box(gx0 - 1, gx0 + 1, gy1, gy1 + 5, gz0, gz1, steel, "grill", grp=G, shadow=False)
    st.stick((gx0 + 10, gy1 + 0.5, gz1 - 10), (gx0 + 24, gy1 + 1.5, gz1 - 4), 0.5, col("#d0d4d8"), "grill", grp=G)  # a scraper
    st.box(gx0 + 22, gx0 + 28, gy1 + 0.4, gy1 + 1.4, gz1 - 7, gz1 - 2, plain("#3a2a20", 0.1), "grill", grp=G, shadow=False)
    roller_body(st, G, roller_phase)
    # a card on the grill: CLOSED (it has been since 1979), hand-lettered, propped on the guard
    m = pen_mask(["GRILL", "CLOSED"], 22, 12, 3.6, res=20, seed=6)
    def m_card(c):
        tx = np.clip(c.U * 20, 0, m.shape[1] - 1.001).astype(np.intp)
        ty = np.clip((12 - c.V) * 20, 0, m.shape[0] - 1.001).astype(np.intp)
        return lerp(col("#f4e8c8"), col("#8a2a24"), m[ty, tx][..., None] * 0.95)
    st.poly([(gx0 + 3, gy1, gz0 + 6), (gx0 + 25, gy1, gz0 + 6), (gx0 + 25, gy1 + 12, gz0 + 2), (gx0 + 3, gy1 + 12, gz0 + 2)], m_card, "grill", grp=G)


ROLL_N = 7


def roller_body(st, G, phase=None):
    """The roller: a steel tray with seven chrome rollers turning side by side. phase None: the tray and the rollers
    as the painting has them (frame 0, part of the counter's cut-out); a number: the rollers turned that far, as a
    group of their own ("roller": a frame of roller-0/1)."""
    x0, x1, y0, y1, z0, z1 = M.ROLLER
    st.box(x0, x1, y0, y0 + 6, z0, z1, chrome("#a8acb0", 0.3, 16), "roller", grp=G)
    st.box(x0, x0 + 2, y0 + 6, y0 + 12, z0, z1, chrome("#a8acb0", 0.3, 17), "roller", grp=G, shadow=False)
    st.box(x1 - 2, x1, y0 + 6, y0 + 12, z0, z1, chrome("#a8acb0", 0.3, 18), "roller", grp=G, shadow=False)
    st.box(x0 + 2, x0 + 8, y0 + 1, y0 + 4, z1, z1 + 1, plain("#d83a2c", 0.1), "roller", grp=G, shadow=False)   # the pilot light (off)
    ph = 0.0 if phase is None else phase
    gr = G if phase is None else "roller"
    for i in range(ROLL_N):
        zc = z0 + 5 + i * (z1 - z0 - 10) / (ROLL_N - 1)
        def m_roll(c, i=i):
            a = c.ang + ph + i * 0.7
            stripe = (np.cos(a * 3.0) > 0.45)
            k = np.where(stripe[..., None], col("#f4f6f8"), col("#7a8088"))
            return k * (0.8 + 0.25 * np.clip(normals(c)[:, 1], 0, 1))[:, None], col("#ffffff")[None, :] * (stripe * 0.3)[:, None]
        st.cyl((y0 + 8.5, zc), 1.8, x0 + 2, x1 - 2, m_roll, axis="x", name="rollers", grp=gr, shadow=False, cap=col("#b8bcc0"))


# ---------------------------------------------------------------- Harold, the drinks cooler
def cooler(st, G="cooler"):
    """A tall old drinks cooler, white enamel gone cream, its glass door toward us, lit inside by a tube: jugs of
    lemonade on the shelves, bottles of pop in plain colours (no labels anyone would know), and HAROLD on a strip of
    tape across the top, because Jolene names everything."""
    x0, x1, y0, y1, z0, z1 = M.COOLER
    enamel = metal("#e6ddc6", 21, 0.12)
    # the shell, seen from outside: two sides, a top, a bottom and a back; the front is a frame round the glass
    fx0, fx1, fy0, fy1 = x0 + 7, x1 - 7, 22, 166
    zf = z1 - 6
    st.box(x0, fx0, y0, y1, z0, zf, enamel, "cooler", grp=G, foot=True)
    st.box(fx1, x1, y0, y1, z0, zf, enamel, "cooler", grp=G, foot=True)
    st.box(fx0, fx1, fy1, y1, z0, zf, enamel, "cooler", grp=G)
    st.box(fx0, fx1, y0, fy0, z0, zf, enamel, "cooler", grp=G)
    st.box(fx0, fx1, fy0, fy1, z0, z0 + 4, enamel, "cooler", grp=G)
    # the frame round the door
    for (a0, a1, b0, b1) in ((x0, fx0, 0, y1), (fx1, x1, 0, y1), (fx0, fx1, 0, fy0), (fx0, fx1, fy1, y1)):
        st.box(a0, a1, b0, b1, zf, z1, enamel, "cooler", grp=G, shadow=False)
    # the grille at the bottom, the header with its tape
    def m_header(c):
        k = col("#c83a2c") * (0.92 + 0.1 * fbm(c.X / 6, c.Y / 6, 22, 2))[..., None]
        return k
    st.box(fx0, fx1, fy1 + 4, y1 - 4, z1, z1 + 0.6, m_header, "cooler", grp=G, shadow=False)
    st.box(fx0 + 2, fx1 - 2, 4, 16, z1, z1 + 0.6, plain("#3a3a3c", 0.1, 3, 23), "cooler", grp=G, shadow=False)
    # the inside: lit, cool white; three wire shelves; lemonade jugs and bottles
    inner = (fx0 + 1, fx1 - 1, fy0 + 1, fy1 - 1, z0 + 4, zf)
    def m_lining(c):
        glow = np.clip(1.15 - (fy1 - c.Y) / 260, 0.55, 1)
        k = col("#dfe8ea")
        return k * 0.25, k * (0.62 * glow)[..., None]
    st.box(*inner, m_lining, "cooler", grp=G, inside=True)
    shelf_y = (fy0 + 4, fy0 + 52, fy0 + 98)
    for sy in shelf_y:
        st.box(inner[0], inner[1], sy - 1, sy, inner[4], inner[5] - 2, plain("#b8c0c4", 0.05), "cooler", grp=G, shadow=False,
               emi=col("#d8e4e8") * 0.35)
    rng = np.random.default_rng(31)
    pops = ["#d8382c", "#f0a028", "#2c8a4a", "#8a3a8a", "#e8d040", "#3a6ab8"]
    for si, sy in enumerate(shelf_y):
        if si == 2:                                          # the top shelf: the lemonade, in big glass jugs
            for k in range(3):
                jx = inner[0] + 12 + k * 25
                def m_jug(c, k=k):
                    lv = c.Y < sy + 26
                    a = lerp(col("#f6e070"), col("#f8f0a8"), np.clip((c.Y - sy) / 26, 0, 1)[..., None])
                    a = np.where(lv[..., None], a, col("#e8f0f0") * 0.8)
                    return a * 0.3, a * 0.75
                st.cyl((jx, inner[4] + 22), 9.5, sy, sy + 30, m_jug, name="cooler", grp=G, shadow=False)
                st.cyl((jx, inner[4] + 22), 3.5, sy + 30, sy + 36, plain("#e8e8e0", 0.1), name="cooler", grp=G, shadow=False)
                st.cyl((jx, inner[4] + 22), 3.8, sy + 36, sy + 38, plain("#d8382c", 0.1), name="cooler", grp=G, shadow=False, emi=col("#d8382c") * 0.4)
        else:
            for k in range(7):
                bx = inner[0] + 6 + k * 11.5
                c_ = pops[int(rng.integers(len(pops)))]
                def m_bottle(c, c_=c_):
                    a = col(c_)
                    return a * 0.3, a * 0.6
                st.cyl((bx, inner[4] + 30 + rng.normal(0, 4)), 3.4, sy, sy + 22, m_bottle, name="cooler", grp=G, shadow=False)
                st.cyl((bx, inner[4] + 30), 1.4, sy + 22, sy + 29, m_bottle, name="cooler", grp=G, shadow=False)
    # the glass: its frame of chrome, a handle, and the shine across it (the glass itself is clear)
    def m_glass(c):
        u, v = c.U, c.V
        streak = np.abs((u + v * 0.55) - 30) < 3.0
        streak |= np.abs((u + v * 0.55) - 42) < 1.2
        streak |= np.abs((u + v * 0.55) - 95) < 4.0
        fog = (fbm(u / 6, v / 6, 33, 2) > 0.72) & (v < 30)
        keep = streak | fog
        k = np.where(streak[..., None], col("#ffffff"), col("#e8f0f4"))
        return k * 0.4, k * np.where(streak, 0.55, 0.25)[..., None], keep
    st.poly([(fx0, fy0, z1 + 0.3), (fx1, fy0, z1 + 0.3), (fx1, fy1, z1 + 0.3), (fx0, fy1, z1 + 0.3)], m_glass, "cooler", grp=G, flag=1)
    st.box(fx1 - 8, fx1 - 5, fy0 + 50, fy0 + 92, z1 + 0.5, z1 + 4.5, chrome("#d8dce0", 0.8, 24), "cooler", grp=G, shadow=False)
    # the tape across the header: HAROLD, in Jolene's marker (the word goes on afterwards, crisp)
    def m_tape(c):
        return col("#ece2c4") * (0.92 + 0.1 * fbm(c.U / 2, c.V / 2, 25, 2))[..., None]
    q = harold_tape()
    st.poly([q[3], q[2], q[1], q[0]], m_tape, "cooler", grp=G, bias=0.2)
    return (fx0, fx1, fy1, y1, z1)


def harold_tape():
    x0, x1, y0, y1, z0, z1 = M.COOLER
    fx0, fx1, fy1 = x0 + 7, x1 - 7, 166
    return [(fx0 + 8, y1 - 8, z1 + 0.9), (fx1 - 8, y1 - 8, z1 + 0.9), (fx1 - 8, fy1 + 8, z1 + 0.9), (fx0 + 8, fy1 + 8, z1 + 0.9)]


# ---------------------------------------------------------------- the survival shelf, and the TV on top
def survival(st, G="back", tv_frame=None):
    """A tall shelf of things for the desert: flats of water, bottles of water with plain blue labels, jerky in
    packets, folded space blankets in silver packets, a few cans. The TV stands on top."""
    x0, x1, y0, y1, z0, z1 = M.SURVIVAL
    w = wood("#8a6a48", 41, "x", 0.2)
    st.box(x0, x0 + 2, 0, y1, z0, z1, w, "survival", grp=G)
    st.box(x1 - 2, x1, 0, y1, z0, z1, w, "survival", grp=G)
    st.box(x0, x1, 0, y1, z0, z0 + 1, plain("#6a5038", 0.1), "survival", grp=G, shadow=False)
    shelves = (6, 46, 86, 126, y1 - 2)
    for sy in shelves:
        st.box(x0, x1, sy - 2, sy, z0, z1, w, "survival", grp=G, shadow=False)
    # bottom: a flat of water, shrink-wrapped
    def m_wrap(c):
        k = col("#bcd4e8") * (0.85 + 0.25 * fbm(c.X / 4, c.Y / 4, 42, 2))[..., None]
        return k
    st.box(x0 + 3, x1 - 3, 6, 30, z0 + 4, z1 - 2, m_wrap, "survival", grp=G, shadow=False)
    # next two: bottles of water standing in rows, blue labels
    for sy in (46, 86):
        for k in range(7):
            bx = x0 + 6 + k * 7.6
            def m_b(c):
                lab = (c.Y > sy + 7) & (c.Y < sy + 15)
                a = np.where(lab[..., None], col("#3a6ab8"), col("#cfe2f0"))
                return a
            st.cyl((bx, z1 - 6), 3.2, sy, sy + 22, m_b, name="survival", grp=G, shadow=False)
            st.cyl((bx, z1 - 6), 1.4, sy + 22, sy + 26, plain("#4a7ac8", 0.1), name="survival", grp=G, shadow=False)
    # then jerky: packets hanging and lying, brown and red
    for k in range(5):
        px = x0 + 5 + k * 10.5
        def m_j(c, k=k):
            a = col(["#8a3a24", "#a84a28", "#7a2a1c", "#a84a28", "#8a3a24"][k])
            win = (np.abs(c.U - 4.5) < 2.5) & (c.V > 3) & (c.V < 10)
            return np.where(win[..., None], col("#6a3a20") * 0.8, a)
        st.poly([(px, 128, z1 - 3), (px + 9, 128, z1 - 3), (px + 9, 156, z1 - 5), (px, 156, z1 - 5)], m_j, "survival", grp=G)
    # top shelf (under the TV): folded space blankets in silver packets
    for k in range(4):
        px = x0 + 4 + k * 13
        st.box(px, px + 11, 126 + 30, 126 + 33 + k % 2, z0 + 8, z1 - 4, chrome("#d8dce4", 0.7, 43 + k), "survival", grp=G, shadow=False)
    tv(st, G, tv_frame)


def tv(st, G="back", snow_seed=None):
    """A small portable TV with a wood-grain case and rabbit ears, on top of the survival shelf. Its screen is snow:
    snow_seed None is the painting's own screen (frame 0); a number paints the screen alone, as a group of its own
    ("tvscreen": the frames tv-0, tv-1, tv-2)."""
    x0, x1, y0, y1, z0, z1 = M.TV
    st.box(x0, x1, y0, y1, z0, z1, wood("#8a5a34", 44, "x", 0.25, 1.5, 30.0), "tv", grp=G)
    st.box(x0 + 2, x1 - 2, y0 + 2, y1 - 2, z1, z1 + 1.2, plain("#2a2624", 0.1), "tv", grp=G, shadow=False)          # the bezel
    st.cyl((x1 - 5, y0 + 10), 1.8, z1, z1 + 2.2, plain("#c8c0b0", 0.1), axis="z", name="tv", grp=G, shadow=False)   # the knobs
    st.cyl((x1 - 5, y0 + 20), 1.8, z1, z1 + 2.2, plain("#c8c0b0", 0.1), axis="z", name="tv", grp=G, shadow=False)
    top = (x0 + x1) / 2
    mz = (z0 + z1) / 2
    st.ball((top, y1 + 1.5, mz), 3.0, plain("#3a3a3a", 0.1), "tv", grp=G, shadow=False, squash=(1.4, 0.6, 1.0))
    st.stick((top - 1, y1 + 2, mz), (top - 20, y1 + 40, mz - 6), 0.45, col("#c8ccd0"), "tv", grp=G)                 # the rabbit ears
    st.stick((top + 1, y1 + 2, mz), (top + 15, y1 + 44, mz + 4), 0.45, col("#c8ccd0"), "tv", grp=G)
    st.ball((top - 20, y1 + 40, mz - 6), 0.9, col("#d8dce0"), "tv", grp=G, shadow=False)
    st.ball((top + 15, y1 + 44, mz + 4), 0.9, col("#d8dce0"), "tv", grp=G, shadow=False)
    st.box(top + 6, top + 9, y1 + 36, y1 + 41, mz + 2, mz + 3, plain("#c8c8c8", 0.1), "tv", grp=G, shadow=False)     # a bit of foil on one ear
    seed = 0 if snow_seed is None else snow_seed
    gr = G if snow_seed is None else "tvscreen"
    sx0, sx1, sy0, sy1 = x0 + 4, x1 - 12, y0 + 4, y1 - 4
    def m_screen(c, seed=seed):
        cu, cv = np.floor(c.U / 0.9), np.floor(c.V / 0.9)
        n = hashf(cu * 913 + cv * 37 + seed * 7919, 61 + seed)
        n2 = hashf(cu * 211 + cv * 91 + seed * 3301, 67 + seed)
        k = 0.35 + 0.65 * (n * 0.6 + n2 * 0.4)
        band_ = np.clip(1 - np.abs(((c.V + seed * 5.3) % 14.0) - 7) / 2.0, 0, 1) * 0.15
        k = np.clip(k + band_, 0, 1)
        g = (col("#c8d4dc")[None, :] * k[:, None])
        edge = np.clip(1 - np.minimum(np.minimum(c.U, (sx1 - sx0) - c.U), np.minimum(c.V, (sy1 - sy0) - c.V)) / 3.0, 0, 1)
        g = g * (1 - 0.45 * edge)[:, None]
        return g * 0.15, g * 0.95
    st.poly([(sx0, sy0, z1 + 1.4), (sx1, sy0, z1 + 1.4), (sx1, sy1, z1 + 1.4), (sx0, sy1, z1 + 1.4)], m_screen, "tvscreen", grp=gr)
    return (sx0, sx1, sy0, sy1, z1 + 1.4)


# ---------------------------------------------------------------- the auto shelf under the window
def autoshelf(st, G="back"):
    """A low shelf under the window: quarts of oil in plain cans, two jugs of blue wiper fluid, a can of chrome
    polish from 1987 (its label faded to nothing, dust on its lid), a squeegee leaning on the end, a funnel."""
    x0, x1, y0, y1, z0, z1 = M.AUTOSHELF
    w = wood("#7a5a3a", 51, "z", 0.22)
    st.box(x0, x1, 0, 4, z0, z1, w, "autoshelf", grp=G)
    st.box(x0, x1, 34, 37, z0, z1, w, "autoshelf", grp=G, shadow=False)
    st.box(x0, x1, y1 - 3, y1, z0, z1, w, "autoshelf", grp=G, shadow=False)
    for zz in (z0, z1 - 3):
        st.box(x0, x1, 0, y1, zz, zz + 3, w, "autoshelf", grp=G)
    rng = np.random.default_rng(52)
    oils = ["#2a6a4a", "#b83a2a", "#2a4a8a", "#d8a830", "#2a6a4a", "#b83a2a"]
    z = z0 + 8
    k = 0
    while z < z1 - 12:
        c_ = oils[k % len(oils)]
        def m_can(c, c_=c_):
            band_ = (c.Y % 34 > 6) & (c.Y % 34 < 12)
            a = np.where(band_[..., None], col("#f0e8d0"), col(c_))
            return a * (0.9 + 0.2 * fbm(c.Y / 3, c.Z / 3, 53, 2))[..., None]
        st.cyl((x1 - 9, z), 5.0, 4, 20, m_can, name="autoshelf", grp=G, shadow=False, cap=col("#c8c8c0"))
        z += 11.5
        k += 1
    # the top shelf: two jugs of wiper fluid, the polish, a funnel
    for jz in (z0 + 16, z0 + 36):
        def m_jug(c):
            a = col("#5aa8e8")
            lab = (c.Y > 44) & (c.Y < 54)
            return np.where(lab[..., None], col("#f4f0e4"), a) * 0.95
        st.box(x1 - 20, x1 - 4, 37, 62, jz - 7, jz + 7, m_jug, "autoshelf", grp=G, shadow=False)
        st.cyl((x1 - 12, jz), 2.2, 62, 66, plain("#e8e8e0", 0.1), name="autoshelf", grp=G, shadow=False)
    def m_polish(c):
        band_ = (c.Y > 43) & (c.Y < 48)
        a = np.where(band_[..., None], col("#c84a3a") * 0.75, col("#b8b8b0"))
        return a * (0.85 + 0.25 * fbm(c.Y / 2, c.Z / 2, 54, 2))[..., None]
    st.cyl((x1 - 11, z0 + 62), 5.5, 37, 52, m_polish, name="autoshelf", grp=G, shadow=False, cap=col("#a8a49c"))
    st.cyl((x1 - 11, z0 + 86), 7.0, 37, 40, plain("#3a6a3a", 0.1), r1=2.0, name="autoshelf", grp=G, shadow=False)         # the funnel, upside down
    st.cyl((x1 - 11, z0 + 86), 1.6, 40, 50, plain("#3a6a3a", 0.1), name="autoshelf", grp=G, shadow=False)
    # cans on the top further along, and a box of fuses
    for i, zz in enumerate(range(int(z0 + 110), int(z1 - 20), 13)):
        st.cyl((x1 - 10, zz), 5.0, 37, 51, plain(oils[(i + 2) % len(oils)], 0.12, 3, 55 + i), name="autoshelf", grp=G, shadow=False, cap=col("#c0c0b8"))
    # the squeegee, leaning on the near end of the shelf
    sz = z1 + 6
    st.stick((x1 - 4, 0, sz + 10), (x1 - 8, 58, sz), 0.9, col("#3a3a3a"), "autoshelf", grp=G)
    st.box(x1 - 12, x1 - 4, 56, 59, sz - 14, sz + 12, plain("#2a2a2c", 0.1), "autoshelf", grp=G, shadow=False)
    st.box(x1 - 11, x1 - 5, 59, 66, sz - 13, sz + 11, plain("#e8a830", 0.1), "autoshelf", grp=G, shadow=False)     # its sponge


# ---------------------------------------------------------------- the spinner rack of sunglasses
def spinner(st, G="spinner", mirror=True, G_mirror="mirror"):
    """A wire rack that turns: a pole on a round foot, five tiers of hooks, a few pairs of cheap sunglasses left on
    it (dusty), a little card on top ($3.99), and the last pair of mirror shades, toward us (G_mirror)."""
    X, Z, Hh = M.SPINNER
    R = M.SPINNER_R
    wire = col("#a8acb0")
    st.cyl((X, Z), 18.0, 0, 3, plain("#3a3a3c", 0.1, 3, 61), r1=16.0, name="spinner", grp=G, foot=True)
    st.stick((X, 3, Z), (X, Hh, Z), 1.1, col("#b0b4b8"), "spinner", grp=G)
    rng = np.random.default_rng(62)
    frames = ["#e85aa0", "#f4f0e8", "#5a3a2a", "#3a6ab8", "#e8c040", "#2a2a2a", "#3aa878"]
    tiers = (40, 70, 100, 130, 158)
    for ti, ty in enumerate(tiers):
        for k in range(6):
            a = math.radians(k * 60 + ti * 30 + 10)
            nx, nz = math.cos(a), math.sin(a)
            end = (X + nx * R, ty, Z + nz * R)
            st.stick((X, ty + 2, Z), end, 0.32, wire, "spinner", grp=G)
            # a pair of glasses on this hook? (most hooks are empty now)
            if (ti, k) == MIRROR_HOOK or (ti * 6 + k) % 4 == 0:
                continue
            if rng.random() < 0.45:
                fc = frames[int(rng.integers(len(frames)))]
                glasses(st, end, nx, nz, fc, "#2a3038", "spinner", G)
    # the card on top
    m = pen_mask(["$3.99"], 14, 7, 4.2, res=20, seed=8)
    def m_card(c):
        tx = np.clip(c.U * 20, 0, m.shape[1] - 1.001).astype(np.intp)
        ty = np.clip((7 - c.V) * 20, 0, m.shape[0] - 1.001).astype(np.intp)
        return lerp(col("#f4ecd4"), col("#b8302a"), m[ty, tx][..., None])
    a = math.radians(-40)
    tx_, tz_ = math.cos(a), -math.sin(a)
    st.poly([(X - tx_ * 7, Hh + 1, Z - tz_ * 7), (X + tx_ * 7, Hh + 1, Z + tz_ * 7), (X + tx_ * 7, Hh + 8, Z + tz_ * 7), (X - tx_ * 7, Hh + 8, Z - tz_ * 7)],
            m_card, "spinner", grp=G, flag=1)
    if mirror:
        mirror_shades(st, G_mirror)


MIRROR_HOOK = (2, 0)                                     # the tier and the hook the mirror shades hang on (toward us)


def mirror_hook():
    X, Z, Hh = M.SPINNER
    ti, k = MIRROR_HOOK
    ty = (40, 70, 100, 130, 158)[ti]
    a = math.radians(k * 60 + ti * 30 + 10)
    return (X + math.cos(a) * M.SPINNER_R, ty, Z + math.sin(a) * M.SPINNER_R), math.cos(a), math.sin(a)


def mirror_shades(st, G="mirror"):
    """The last pair of mirror shades, on the hook toward us: a thin wire frame, two lenses that are little
    mirrors with the desert sky in them."""
    end, nx, nz = mirror_hook()
    glasses(st, end, nx, nz, "#d8dce0", "mirror", "mirrorshades", G, size=1.15)


def glasses(st, end, nx, nz, frame, lens, name, G, size=1.0):
    """A pair of sunglasses hanging by their bridge from a hook's end, facing out along (nx, nz)."""
    tx, tz = -nz, nx                                     # across the glasses
    cx, cy, cz = end[0] + nx * 1.0, end[1] - 3.2 * size, end[2] + nz * 1.0
    for s in (-1, 1):
        lx, lz = cx + tx * s * 3.4 * size, cz + tz * s * 3.4 * size
        if lens == "mirror":
            def m_lens(c, s=s):
                f = np.clip((c.Y - (cy - 3)) / 5.0, 0, 1)
                sky = lerp(col("#e8c890"), col("#6aa8e8"), f[..., None])
                streak = np.abs((c.Y - cy) + (c.X - lx) * 0.6 * s) < 0.5
                sky = np.where(streak[..., None], col("#ffffff"), sky)
                return sky * 0.5, sky * 0.75
            m = m_lens
        else:
            m = plain(lens, 0.1, 2, 63)
        pts = []
        for q in np.linspace(0, 2 * math.pi, 14, endpoint=False):
            ox, oy = math.cos(q) * 3.0 * size, math.sin(q) * 2.3 * size
            pts.append((lx + tx * ox + nx * 0.2, cy + oy, lz + tz * ox + nz * 0.2))
        st.poly(pts, m, name, grp=G, flag=1)
        st.rope([(lx + tx * math.cos(q) * 3.2 * size, cy + math.sin(q) * 2.5 * size, lz + tz * math.cos(q) * 3.2 * size)
                 for q in np.linspace(0, 2 * math.pi, 13)], 0.28 * size, col(frame), name=name, grp=G)
    st.stick((cx - tx * 1.0, cy + 1.6 * size, cz - tz * 1.0), (cx + tx * 1.0, cy + 1.6 * size, cz + tz * 1.0), 0.3 * size, col(frame), name, grp=G)


# ---------------------------------------------------------------- the rock bins
ROCK_BINS = [  # name on the tape, the bin's share of the width, the rock: colour, size (cm), how lumpy
    ("PEBBLE", 0.205, "#d8d0c4", 3.0, 0.1),
    ("STONY", 0.18, "#8a8a8c", 9.0, 0.25),
    ("ROCKY", 0.18, "#b4583a", 11.0, 0.45),
    ("THE SENATOR", 0.255, "#4a4248", 14.0, 0.12),
    ("SHY", 0.18, "#e8dccc", 8.0, 0.3),
]


def rock(st, c, r, color, lumpy, seed, name, G, squash=(1.0, 0.7, 1.0), lit=None):
    """A rock: a squashed ball with its colour broken into grains and veins."""
    def m_rock(cx_):
        n = fbm(cx_.X / (r * 0.4), (cx_.Y + cx_.Z) / (r * 0.4), seed, 3)
        k = col(color) * (0.8 + 0.4 * n)[:, None] if n.ndim == 1 else col(color) * (0.8 + 0.4 * n)[..., None]
        vein = np.abs(fbm(cx_.X / (r * 0.8), cx_.Y / (r * 0.3), seed + 5, 2) - 0.5) < 0.03
        return np.where(vein[..., None], col("#f0e8dc"), k)
    st.ball(c, r, m_rock, name, grp=G, squash=squash)
    if lumpy:
        rng = np.random.default_rng(seed)
        for i in range(3):
            o = rng.normal(0, r * 0.45, 3)
            st.ball((c[0] + o[0], c[1] + abs(o[1]) * 0.4, c[2] + o[2]), r * (0.45 + lumpy), m_rock, name, grp=G, squash=squash, shadow=False)


def rockbins(st, G="rockbins"):
    """Grandpa Joe's rocks: a wooden stand with a sloping tray of five bins, a heap of rocks in each and in front of
    each the bin's own rock, named on a strip of tape on the bin's front lip; ROCKS $1 on a card hung under the lip."""
    x0, x1, y0, y1, z0, z1 = M.ROCKBINS
    w = wood("#a07040", 71, "x", 0.22)
    wd = wood("#7a5030", 72, "y", 0.22)
    # legs and the frame
    for lx in (x0 + 3, x1 - 3):
        for lz in (z0 + 3, z1 - 3):
            st.box(lx - 2.5, lx + 2.5, 0, 44 + (z1 - lz) * 0 + (6 if lz < z1 - 10 else 0), lz - 2.5, lz + 2.5, wd, "rockbins", grp=G, foot=True)
    # the tray: its floor slopes down toward us (back at 62, front at 46), with a lip along the front
    def m_tray(c):
        return col("#8a6038") * (0.85 + 0.25 * fbm(c.X / 3, c.Z / 30, 73, 2))[..., None]
    st.poly([(x0, 46, z1), (x1, 46, z1), (x1, 62, z0), (x0, 62, z0)], m_tray, "rockbins", grp=G, shadow=True)
    st.box(x0, x1, 62, y1, z0, z0 + 3, w, "rockbins", grp=G)                                     # the back board
    st.box(x0, x0 + 2.5, 40, 66, z0, z1, w, "rockbins", grp=G, shadow=False)                       # the ends
    st.box(x1 - 2.5, x1, 40, 66, z0, z1, w, "rockbins", grp=G, shadow=False)
    lip = (38, 56)                                                                                   # the front lip (the tapes go on it)
    st.box(x0, x1, lip[0], lip[1], z1 - 2.5, z1, w, "rockbins", grp=G)
    # the dividers and the rocks
    rng = np.random.default_rng(74)
    edges = [x0 + 2.5]
    for name_, share, *_ in ROCK_BINS:
        edges.append(edges[-1] + share * (x1 - x0 - 5))
    for i in range(1, len(edges) - 1):
        st.box(edges[i] - 0.8, edges[i] + 0.8, 46, 64, z0 + 3, z1 - 2.5, w, "rockbins", grp=G, shadow=False)
    heaps = ["#c8a080", "#a8a098", "#d8c0a0", "#8a7a70", "#e0d4c4", "#b06a48", "#6a6a70"]
    for i, (name_, share, color, size, lumpy) in enumerate(ROCK_BINS):
        bx0, bx1 = edges[i] + 2, edges[i + 1] - 2
        for k in range(int(10 * share * 5)):                                                         # the heap of the others
            rx = rng.uniform(bx0 + 3, bx1 - 3)
            rz = rng.uniform(z0 + 8, z1 - 22)
            ry = 46 + (z1 - rz) / (z1 - z0) * 16 + 2
            rock(st, (rx, ry, rz), rng.uniform(2.6, 4.6), heaps[int(rng.integers(len(heaps)))], 0.0, int(80 + i * 20 + k), "rockbins", G)
            if rng.random() < 0.5:                                                                     # each has its name: a fleck of tape
                st.box(rx - 1.2, rx + 1.2, ry + 2.2, ry + 3.0, rz - 0.5, rz + 0.5, plain("#f0e4c0", 0.05), "rockbins", grp=G, shadow=False)
        # the bin's own rock, front and middle (set back far enough that its name shows under it)
        rx, rz = (bx0 + bx1) / 2, z1 - 22
        ry = 46 + (z1 - rz) / (z1 - z0) * 16 + size * 0.55
        if name_ == "SHY":                                                                             # SHY is tucked half behind a little paper screen
            rock(st, (rx + 2, ry, rz - 2), size * 0.75, color, lumpy, 200 + i, "rockbins", G)
            def m_screen(c):
                return col("#f4ecd8") * (0.92 + 0.1 * fbm(c.U, c.V, 75, 2))[..., None]
            st.poly([(rx - 7, 48, rz + 5), (rx + 1, 48, rz + 7), (rx + 1, 62, rz + 6), (rx - 7, 62, rz + 4)], m_screen, "rockbins", grp=G, flag=1)
            st.poly([(rx + 1, 48, rz + 7), (rx + 8, 48, rz + 4), (rx + 8, 62, rz + 3), (rx + 1, 62, rz + 6)], m_screen, "rockbins", grp=G, flag=1)
        elif name_ == "PEBBLE":                                                                      # a very small pebble, alone, in a bin of its own
            rock(st, (rx, 49.0, rz + 4), size, color, lumpy, 200 + i, "rockbins", G, squash=(1.0, 0.75, 0.9))
        else:
            rock(st, (rx, ry, rz), size, color, lumpy, 200 + i, "rockbins", G)
    # the tapes on the lip, one under each bin (the names go on them afterwards, crisp)
    for name_, quad in rock_labels(edges, lip):
        def m_tape(c):
            return col("#ece0bc") * (0.92 + 0.1 * fbm(c.U / 2, c.V / 2, 78, 2))[..., None]
        st.poly([quad[3], quad[2], quad[1], quad[0]], m_tape, "rockbins", grp=G, bias=0.1)
    # the card, hung on two strings under the front lip at the right end: low, so that nothing behind the bins is
    # hidden by it (the back door's step and the hens, Jolene's chair and her knitting)
    w_, h_, top = ROCK_CARD
    sx, sz = x1 - ROCK_CARD_IN, z1 - 1.0
    for dx in (-w_ / 2 + 6, w_ / 2 - 6):
        st.stick((sx + dx, lip[0], sz), (sx + dx, top + 0.5, sz), 0.25, col("#d8ccb0"), "rockbins", grp=G, min_px=0.6)
    st.poly([(sx - w_ / 2 - 1, top + 1, sz), (sx + w_ / 2 + 1, top + 1, sz), (sx + w_ / 2 + 1, top - h_ - 1, sz), (sx - w_ / 2 - 1, top - h_ - 1, sz)],
            plain("#efe6cc", 0.06, 6, 77), "rockbins", grp=G, flag=2)
    return edges, lip


def rock_labels(edges, lip):
    """Where the tapes go: [(name, quad in the room: TL, TR, BR, BL)]."""
    x0, x1, y0, y1, z0, z1 = M.ROCKBINS
    out = []
    for i, (name_, *_r) in enumerate(ROCK_BINS):
        bx0, bx1 = edges[i] + 1.2, edges[i + 1] - 1.2
        zf = z1 + 0.15
        out.append((name_, [(bx0, lip[1] - 1.0, zf), (bx1, lip[1] - 1.0, zf), (bx1, lip[0] + 1.0, zf), (bx0, lip[0] + 1.0, zf)]))
    return out


ROCK_CARD = (62.0, 22.0, 33.0)                              # the ROCKS $1 card hung under the front lip: wide, high, the height of its top
ROCK_CARD_IN = 50.0                                          # its middle, this far in from the bins' right end (under THE SENATOR and SHY)


def rock_card():
    x0, x1, y0, y1, z0, z1 = M.ROCKBINS
    sx, sz = x1 - ROCK_CARD_IN, z1 - 1.0
    w, h, top = ROCK_CARD
    return [(sx - w / 2, top, sz + 0.4), (sx + w / 2, top, sz + 0.4), (sx + w / 2, top - h, sz + 0.4), (sx - w / 2, top - h, sz + 0.4)]


# ---------------------------------------------------------------- Jolene's chair, the pay phone
def chair(st, G="back"):
    """A chrome kitchen chair with a red vinyl seat, right of the back door, turned to face it: from it she can see
    her hens and reach the phone. Her knitting on the seat: a very small sweater, striped, the needles through it,
    and the ball of yarn fallen on the floor in front."""
    x0, x1, y0, y1, z0, z1 = M.CHAIR
    for lx in (x0 + 3, x1 - 3):
        for lz in (z0 + 3, z1 - 3):
            st.stick((lx, 0, lz), (lx, 44, lz), 1.0, col("#c0c4c8"), "chair", grp=G)
    st.feet["chair"] = (x0, x1, z0, z1)
    def m_vinyl(c):
        return col("#c8402e") * (0.9 + 0.15 * fbm(c.X / 4, c.Z / 4, 82, 2))[..., None]
    st.box(x0, x1, 44, 50, z0, z1, m_vinyl, "chair", grp=G)
    st.stick((x1 - 2, 50, z0 + 3), (x1 - 1, 92, z0 + 3), 1.0, col("#c0c4c8"), "chair", grp=G)              # the back is on her far side
    st.stick((x1 - 2, 50, z1 - 3), (x1 - 1, 92, z1 - 3), 1.0, col("#c0c4c8"), "chair", grp=G)
    st.box(x1 - 4, x1 + 1, 66, 90, z0 + 1, z1 - 1, m_vinyl, "chair", grp=G)
    def m_sweater(c):
        stripe = (np.floor((c.Z - z0) / 2.6) % 2) == 0
        k = np.where(stripe[..., None], col("#e88ab0"), col("#b8a2d8"))
        return k * (0.9 + np.abs(np.sin(c.X * 3.0))[..., None] * 0.15)
    sx, sz = (x0 + x1) / 2 - 3, (z0 + z1) / 2
    st.box(sx - 8, sx + 8, 50, 53, sz - 8, sz + 8, m_sweater, "knitting", grp=G, shadow=False)
    st.box(sx - 4, sx + 4, 50, 52.5, sz - 13, sz - 8, m_sweater, "knitting", grp=G, shadow=False)        # its sleeves
    st.box(sx - 4, sx + 4, 50, 52.5, sz + 8, sz + 13, m_sweater, "knitting", grp=G, shadow=False)
    st.stick((sx - 12, 53.5, sz - 3), (sx + 10, 55, sz + 6), 0.4, col("#e8e0c8"), "knitting", grp=G)
    st.stick((sx - 11, 53.5, sz + 5), (sx + 11, 55.5, sz - 3), 0.4, col("#e8e0c8"), "knitting", grp=G)
    st.ball((x0 - 9, 5, z1 - 4), 5.0, m_sweater, "knitting", grp=G)                                 # the ball of yarn, on the floor
    st.rope(curve3([(x0 - 5, 8, z1 - 4), (x0 - 1, 30, z1 - 2), (sx - 6, 50, sz + 2)], 5), 0.3, col("#e88ab0"), name="knitting", grp=G)


def payphone(st, G="back"):
    """A pay phone on the wall, dead since the eighties: a steel box, a dial, the coin slot, the handset on its hook
    with its armoured cord."""
    x0, x1, y0, y1 = M.PAYPHONE
    steel = chrome("#a8aeb4", 0.4, 91)
    st.box(x0, x1, y0, y1, 0, 15, steel, "payphone", grp=G)
    st.box(x0 + 3, x1 - 3, y0 + 30, y0 + 50, 15, 16, plain("#2a2a2c", 0.1), "payphone", grp=G, shadow=False)           # the dial's plate
    st.cyl((x1 - 12, y0 + 40), 6.0, 15.5, 17, plain("#e8e8e0", 0.1), axis="z", name="payphone", grp=G, shadow=False)
    st.cyl((x1 - 12, y0 + 40), 2.0, 17, 17.6, plain("#2a2a2c", 0.1), axis="z", name="payphone", grp=G, shadow=False)
    st.box(x1 - 9, x1 - 4, y1 - 9, y1 - 7, 15, 16.5, plain("#1a1a1a", 0.1), "payphone", grp=G, shadow=False)          # the coin slot
    st.box(x0 + 4, x1 - 4, y0 + 4, y0 + 10, 15, 16, plain("#c8c8c0", 0.1), "payphone", grp=G, shadow=False)             # the return
    # the handset on its hook, on the left side
    st.box(x0 - 7, x0 - 1, y0 + 10, y1 - 8, 6, 13, plain("#1e1e20", 0.12, 3, 92), "payphone", grp=G)
    st.box(x0 - 9, x0 - 1, y1 - 14, y1 - 5, 5, 14, plain("#1e1e20", 0.12, 3, 93), "payphone", grp=G, shadow=False)
    st.box(x0 - 9, x0 - 1, y0 + 8, y0 + 17, 5, 14, plain("#1e1e20", 0.12, 3, 94), "payphone", grp=G, shadow=False)
    st.rope(curve3([(x0 - 4, y0 + 9, 9), (x0 - 6, y0 - 8, 10), (x0 - 1, y0 - 10, 8), (x0 + 3, y0 + 2, 5)], 5), 0.9, col("#9aa0a6"),
            name="payphone", grp=G)


# ---------------------------------------------------------------- the bulletin board
BOARD_NOTES = [  # (u0, v0, wide, high, kind, colour): on the board, cm from its lower left corner
    (6, 58, 30, 40, "dog", PAPER), (38, 64, 26, 32, "dog", "#f4e8b0"), (6, 8, 28, 40, "dog", "#e8f0f4"),
    (38, 10, 14, 20, "card", "#f0d8a8"), (38, 36, 24, 22, "list", PAPER),
]
JED_CARD = (68, 6, 64, 98)                                   # Jolene's card to Jed: u0, v0, wide, high (cm, on the board)


def bulletin(st, G="back"):
    """The cork board: lost-dog notices with tear-off tabs and drawings of dogs, a business card, a list, and
    Jolene's card to Jed in big marker (its words are laid crisply afterwards: see board_words)."""
    x0, x1, y0, y1 = M.BULLETIN
    w, h = x1 - x0, y1 - y0
    def m_board(c):
        u, v = c.X - x0, c.Y - y0
        if c.face != "front":
            return col("#6a4a30")
        out = col("#b88a5a") * (0.82 + 0.36 * fbm(u / 1.1, v / 1.1, 101, 2))[..., None]
        for i, (pu, pv, pw, ph, kind, pc) in enumerate(BOARD_NOTES):
            lean = (hashf(i, 3) - 0.5) * 0.06
            uu = u - pu - (v - pv) * lean
            vv = v - pv + (u - pu) * lean
            m = rect(uu, vv, 0, pw, 0, ph, c.fp)
            sheet = np.zeros(u.shape + (3,), dtype=F32) + col(pc)
            if kind == "dog":
                head = (vv > ph - 9) & (vv < ph - 3) & (uu > 3) & (uu < pw - 3)                       # LOST DOG, in big red letters
                sheet = np.where(head[..., None], col("#c8302a"), sheet)
                dog = (np.hypot((uu - pw * 0.5) / 7.0, (vv - ph * 0.52) / 5.0) < 1) | (np.hypot((uu - pw * 0.5 - 6) / 3.4, (vv - ph * 0.62) / 3.2) < 1)
                sheet = np.where(dog[..., None], col("#6a4a3a"), sheet)
                ln = (((vv - 9) % 3.2) < 1.0) & (vv > 8) & (vv < ph * 0.36) & (uu > 3) & (uu < pw - 3)
                sheet = np.where(ln[..., None], col("#3a3a50"), sheet)
                tabs = (vv < 7) & (np.abs(((uu - 1) % 4.0) - 2.0) < 1.6) & (uu > 1) & (uu < pw - 1)
                sheet = np.where((tabs & ((uu % 4.0) > 0.3))[..., None], sheet * 0.97, sheet)
                cut = (vv < 7) & (((uu - 1) % 4.0) < 0.35)
                sheet = np.where(cut[..., None], col("#b88a5a"), sheet)
            elif kind == "list":
                ln = (((vv - 3) % 3.0) < 0.9) & (vv > 2) & (vv < ph - 3) & (uu > 2.5) & (uu < pw - 5)
                sheet = np.where(ln[..., None], col("#3c4660"), sheet)
            elif kind == "card":
                ln = (np.abs(vv - ph * 0.6) < 1.0) & (uu > 2) & (uu < pw - 2)
                sheet = np.where(ln[..., None], col("#2a6a4a"), sheet)
            sheet = sheet * (0.94 + 0.08 * fbm(uu / 5, vv / 5, 110 + i, 2))[..., None]
            shd = rect(uu - 0.8, vv + 0.8, 0, pw, 0, ph, c.fp)
            out = out * (1 - 0.3 * np.clip(shd - m, 0, 1)[..., None])
            out = out * (1 - m[..., None]) + sheet * m[..., None]
            out = lay(out, "#d83a2c" if i % 2 else "#2c64c8", disc(uu, vv, pw * 0.5, ph - 1.8, 1.2, c.fp))
        # Jolene's card: a piece of a cardboard box, its words laid afterwards
        ju, jv, jw, jh = JED_CARD
        m = rect(u - ju, v - jv, 0, jw, 0, jh, c.fp)
        card = col("#d9b98a") * (0.94 + 0.1 * fbm(u / 4, v / 4, 120, 2))[..., None]
        flute = lines_aa(v, 0.8, 0.3, np.full_like(v, 0.4), fade=False) * 0.04
        card = card * (1 - flute[..., None])
        shd = rect(u - ju - 1.0, v - jv + 1.0, 0, jw, 0, jh, c.fp)
        out = out * (1 - 0.35 * np.clip(shd - m, 0, 1)[..., None])
        out = out * (1 - m[..., None]) + card * m[..., None]
        for (pu, pv) in ((ju + 4, jv + jh - 3), (ju + jw - 4, jv + jh - 3)):
            out = lay(out, "#e8c030", disc(u, v, pu, pv, 1.4, c.fp))
        fr = 1 - rect(u, v, 3.0, w - 3.0, 3.0, h - 3.0, c.fp)
        frame = col("#8a5c30") * (0.85 + 0.3 * fbm(u / 2.0 + v / 30, v / 2.0 + u / 30, 102, 2))[..., None]
        return out * (1 - fr[..., None]) + frame * fr[..., None]
    st.box(x0, x1, y0, y1, 0, 2.5, m_board, "bulletin", grp=G)


def board_words():
    """The card's words, and where they go: (mask, quad in the room)."""
    x0, x1, y0, y1 = M.BULLETIN
    ju, jv, jw, jh = JED_CARD
    lines = ["JED: NO", "CHEESE-", "BURGERS.", "WE TOLD", "YOU."]
    cap = 11.6
    m = pen_mask(lines, jw, jh, cap, res=14, pen=0.21, track=0.13, lead=1.36, seed=21, wobble=0.03, squeeze=0.80)
    z = 2.6
    quad = [(x0 + ju, y0 + jv + jh, z), (x0 + ju + jw, y0 + jv + jh, z), (x0 + ju + jw, y0 + jv, z), (x0 + ju, y0 + jv, z)]
    return m, quad


# ---------------------------------------------------------------- the hats on their pegs
HAT_NAMES = {1: "the straw cowboy hat", 2: "the sun hat with fruit on it", 3: "the tiara", 4: "the yellow hard hat", 5: "the hat shaped like a hen"}


def hatrack(st, G="back"):
    """The board with its five pegs, high on the wall over the counter (the hats are cut-outs of their own)."""
    x0, x1, y0, y1 = M.HATRACK
    st.box(x0, x1, y0, y1, 0, 2.5, wood("#8a5a34", 131, "x", 0.22), "hatrack", grp=G)
    for i, px in enumerate(M.HAT_PEGS):
        st.cyl((px, (y0 + y1) / 2), 1.3, 2.5, 11, wood("#a07040", 132 + i, "z", 0.2), axis="z", name="hatrack", grp=G)
        st.ball((px, (y0 + y1) / 2 + 0.4, 11.5), 1.9, wood("#a07040", 133, "x", 0.2), "hatrack", grp=G, shadow=False)
    # a little card under each peg: the hour it is worn? No: her name for it (too small to read: it says it is hers)
    for i, px in enumerate(M.HAT_PEGS):
        st.box(px - 4, px + 4, y0 - 6, y0 - 2, 0, 0.8, plain("#f0e6cc", 0.05, 2, 134 + i), "hatrack", grp=G, shadow=False)


def hat(st, n, G=None):
    """Hat n (1 to 5) on its peg."""
    G = G or f"hat-{n}"
    px = M.HAT_PEGS[n - 1]
    py = (M.HATRACK[2] + M.HATRACK[3]) / 2
    pz = 9.0
    name = f"hat{n}"
    if n == 1:                                           # a straw cowboy hat: crown pinched, brim curled up at the sides
        def m_straw(c):
            weave = np.sin(c.X * 2.4) * np.sin(c.Y * 2.4 + c.Z * 2.4) * 0.5 + 0.5
            return lerp(col("#d8b868"), col("#f0d890"), weave[..., None] * 0.6) * (0.9 + 0.15 * fbm(c.X / 3, c.Y / 3, 141, 2))[..., None]
        st.ball((px, py - 1, pz + 5), 19.0, m_straw, name, grp=G, squash=(1.0, 0.16, 0.8))
        for s in (-1, 1):
            st.ball((px + s * 14, py + 1.5, pz + 5), 7.0, m_straw, name, grp=G, squash=(0.6, 0.45, 1.6), shadow=False)
        st.ball((px, py + 7, pz + 5), 9.5, m_straw, name, grp=G, squash=(1.0, 0.85, 0.85))
        st.box(px - 9, px + 9, py + 1.8, py + 4.6, pz - 1, pz + 13, plain("#7a3a2a", 0.1), name, grp=G, shadow=False)    # the band
        st.ball((px, py + 14.5, pz + 9), 3.0, m_straw, name, grp=G, squash=(2.4, 0.5, 0.8), shadow=False)
    elif n == 2:                                         # a wide sun hat, its brim drooping, fruit on the band
        def m_sun(c):
            return col("#f2e2b8") * (0.9 + 0.15 * fbm(c.X / 2, c.Z / 2, 142, 2))[..., None]
        st.ball((px, py - 2, pz + 6), 22.0, m_sun, name, grp=G, squash=(1.0, 0.13, 0.8))
        st.ball((px, py + 4, pz + 6), 9.0, m_sun, name, grp=G, squash=(1.0, 0.8, 0.85))
        st.box(px - 9, px + 9, py + 1.5, py + 4, pz - 1, pz + 14, plain("#e86a8a", 0.1), name, grp=G, shadow=False)
        for (dx, dz, r, cc) in ((-7, 13, 2.6, "#d63f2a"), (-2, 15, 2.8, "#f2b42e"), (3.5, 14, 2.4, "#9ac77f"), (7.5, 12, 2.2, "#8e5ea8")):
            st.ball((px + dx, py + 4.5, pz + dz), r, plain(cc, 0.1, 2, 143), name, grp=G, shadow=False)
        st.ball((px + 1, py + 7.5, pz + 15.5), 2.6, plain("#2fa673", 0.1), name, grp=G, squash=(1.6, 0.4, 0.8), shadow=False)    # a leaf
    elif n == 3:                                         # a tiara, hung by its band on the peg: it glints
        gold = chrome("#e8c870", 1.4, 144)
        for i in range(11):
            a = math.radians(-75 + i * 15)
            x, y = px + math.sin(a) * 13, py - 6 + math.cos(a) * 6
            st.ball((x, y, pz + 3), 1.3, gold, name, grp=G, shadow=False)
        st.rope([(px - 12, py - 4, pz + 3), (px - 8, py + 2, pz + 3.5), (px - 4, py + 5, pz + 4), (px, py + 11, pz + 4.5), (px + 4, py + 5, pz + 4),
                 (px + 8, py + 2, pz + 3.5), (px + 12, py - 4, pz + 3)], 0.9, col("#f0d890"), name=name, grp=G)
        for (dx, dy, r, cc) in ((0, 9.5, 2.0, "#c9375e"), (-6.5, 4.0, 1.4, "#7fb8de"), (6.5, 4.0, 1.4, "#7fb8de")):
            st.ball((px + dx, py + dy, pz + 4.8), r, plain(cc, 0.05), name, grp=G, shadow=False, emi=col("#ffffff") * 0.4)
    elif n == 4:                                         # a yellow hard hat
        def m_hard(c):
            k = col("#f2c020")
            n_ = normals(c)
            sh = np.clip(-n_[:, 0] * 0.6 + n_[:, 1] * 0.5 + n_[:, 2] * 0.4, 0, 1)
            return k * (0.8 + 0.25 * sh)[:, None], col("#fff8d0")[None, :] * (np.clip(sh - 0.75, 0, 1) * 1.2)[:, None]
        st.ball((px, py + 2, pz + 6), 12.0, m_hard, name, grp=G, squash=(1.0, 0.82, 1.05))
        st.ball((px, py - 2, pz + 8), 14.0, m_hard, name, grp=G, squash=(1.0, 0.12, 1.15), shadow=False)
        st.box(px - 1.2, px + 1.2, py + 2, py + 12, pz + 5, pz + 19, m_hard, name, grp=G, shadow=False)                      # the ridge
    elif n == 5:                                         # a hat shaped like a hen: a plump hen sitting, comb and tail and all
        def m_hen(c):
            return col("#f6f0e2") * (0.88 + 0.15 * fbm(c.X / 2, c.Y / 2, 145, 2))[..., None]
        st.ball((px, py + 3, pz + 6), 12.0, m_hen, name, grp=G, squash=(1.1, 0.8, 0.9))                                       # the body
        st.ball((px - 9, py + 9, pz + 6), 5.0, m_hen, name, grp=G, squash=(0.8, 1.4, 0.8), shadow=False)                      # the tail
        st.ball((px + 9, py + 12, pz + 9), 5.2, m_hen, name, grp=G, shadow=False)                                              # the head
        for (dx, dy) in ((-1.6, 5.0), (0.6, 5.8), (2.6, 5.0)):
            st.ball((px + 9 + dx, py + 12 + dy, pz + 9), 1.7, plain("#d83a2c", 0.05), name, grp=G, shadow=False)
        st.ball((px + 14, py + 11.5, pz + 9), 1.4, plain("#f2a020", 0.05), name, grp=G, squash=(1.5, 0.7, 0.7), shadow=False)  # beak
        st.ball((px + 12.5, py + 9, pz + 10), 1.2, plain("#d83a2c", 0.05), name, grp=G, squash=(0.7, 1.4, 0.7), shadow=False)  # wattle
        st.ball((px + 11, py + 13, pz + 13.6), 0.8, plain("#1a1418", 0.05), name, grp=G, shadow=False)                       # eye
        st.ball((px, py + 2, pz + 14), 7.0, plain("#e8e0d0", 0.1), name, grp=G, squash=(1.3, 0.6, 0.3), shadow=False)          # the wing


# ---------------------------------------------------------------- the hubcaps
def hubcap_places():
    """Where the hundred and twelve hang: rows on the back wall wherever it is free (round the cooler, the board, the
    hats, the phone, the doors and the shelf), on along the left wall over the window, and round the corner onto the
    right-hand wall. -> [(wall, u, v, r, style, seed)]: u along the wall (X on the back wall, Z on the side walls)."""
    rng = np.random.default_rng(1974)
    taken = {  # rectangles on each wall (u0, u1, v0, v1) that are something else
        "back": [(M.COOLER[0] - 2, M.COOLER[1] + 2, 0, M.COOLER[3] + 3), (M.BULLETIN[0] - 3, M.BULLETIN[1] + 3, 0, M.BULLETIN[3] + 3),
                 (M.HATRACK[0] - 8, M.HATRACK[1] + 12, 0, M.HATRACK[3] + 20), (M.PAYPHONE[0] - 14, M.PAYPHONE[1] + 4, 0, M.PAYPHONE[3] + 4),
                 (M.BACKDOOR[0] - 104, M.BACKDOOR[1] + 12, 0, M.BACKDOOR[3] + 12), (M.SURVIVAL[0] - 2, M.SURVIVAL[1] + 2, 0, M.TV[3] + 50),
                 (0, M.W, 0, 104)],
        "left": [(M.WINDOW[0] - 12, M.WINDOW[1] + 12, 0, M.WINDOW[3] + 14), (0, 400, 0, 120), (M.COOLER[4], M.COOLER[5] + 4, 0, M.COOLER[3] + 3)],
        "right": [(0, M.SURVIVAL[5] + 2, 0, M.TV[3] + 50)],
    }
    out = []
    tractor = ("back", 386, 318, 32.0, "tractor", 0)       # the tractor's wheel: one, big, in pride of place over the counter
    out.append(tractor)

    def free(wall, cu, cv, r):
        for (a0, a1, b0, b1) in taken[wall]:
            if cu + r > a0 and cu - r < a1 and cv - r < b1 and cv + r > b0:
                return False
        for (w2, ux, uy, ur, _s, _q) in out:
            if w2 == wall and math.hypot(cu - ux, cv - uy) < ur + r + 1.2:
                return False
        return cv + r < M.H - 3
    plan = [("back", (0, M.W), [(363, 15.5), (330, 17.0), (294, 17.5), (257, 17.0), (220, 16.0), (184, 16.0), (148, 15.5), (116, 13.0)]),
            ("left", (4, 400), [(364, 15.5), (330, 16.5), (294, 16.5), (258, 16.0), (222, 15.5)]),
            ("right", (4, 330), [(362, 15.5), (328, 16.5), (292, 16.5), (256, 16.0), (220, 15.5), (184, 15.5)])]
    for wall, (ua, ub), rows in plan:
        for (vy, rr) in rows:
            x = ua + rng.uniform(0, 10)
            while x < ub - 6:
                r = rr * rng.uniform(0.80, 1.06)
                cu, cv = x + r, vy + rng.normal(0, 1.8)
                if cu + r < ub and free(wall, cu, cv, r):
                    out.append((wall, cu, cv, r, int(rng.integers(0, 9)), int(rng.integers(0, 10000))))
                    x += 2 * r + rng.uniform(1.6, 5.0)
                else:
                    x += 4.0
    # a hundred and twelve, no more: the ones over the counter first, then the left wall, then round the corner
    back = [h for h in out if h[0] == "back"]
    left = [h for h in out if h[0] == "left"]
    right = [h for h in out if h[0] == "right"]
    keep = back[:M.HUBCAPS]
    keep += left[:max(0, M.HUBCAPS - len(keep))]
    keep += right[:max(0, M.HUBCAPS - len(keep))]
    return keep


HUB_TINTS = ["#c8ccd4", "#bfc4cc", "#d0d0d2", "#c6c8cc", "#d4c8a8", "#b8bcc4", "#c8ccd4", "#a8acb4", "#ccd0d6"]


def m_hubcap(style, seed, r):
    """A hubcap's face, by its style: plain domed chrome, slotted, wire-spoked, a pressed star, a baby moon, a white
    ring, gold, rusty, dented; and the tractor's wheel, a red rim with a yellow hub and its lug holes. Chrome shows
    the room, not its own colour: the dark tin ceiling in its upper half, the warm floor in its lower, and the window
    as a bright streak on the side toward it. U, V are cm on the disc from its middle."""
    rng = np.random.default_rng(seed)
    turn = rng.uniform(0, 6.28)
    tint = col(HUB_TINTS[style]) if isinstance(style, int) else col("#c8ccd4")
    dull = rng.uniform(0.72, 1.18)

    def f(c):
        u, v = c.U, c.V
        rr = np.hypot(u, v) / r
        a = np.arctan2(v, u) + turn
        hx, hy = u / r, v / r
        # what the shallow dish reflects: a little darker toward its top (the tin ceiling), lighter low (the floor),
        # pressed rings round it, and the window as a streak on the side toward it
        env = 0.58 + 0.14 * np.clip(-hy, 0, 1) - 0.10 * np.clip(hy, 0, 1) - 0.06 * np.clip(hx, 0, 1)
        rings = (np.abs(rr - 0.32) < 0.035) | (np.abs(rr - 0.64) < 0.035)
        env = np.where(rings, env * 0.55, env)
        bright = (np.abs(rr - 0.38) < 0.03) | (np.abs(rr - 0.70) < 0.025)
        env = np.where(bright, env * 1.3, env)
        win = np.exp(-((hx + 0.40) / 0.16) ** 2 - ((hy - 0.10) / 0.42) ** 2)            # the window, as a streak
        env = env + 0.75 * win
        # where the wall is: the back wall's left part and the left wall see more of the window
        place = np.clip(1.1 - np.asarray(c.X) / 1100.0 - np.clip(np.asarray(c.Y) - 300, 0, 100) / 300.0, 0.55, 1.1)
        if style == "tractor":
            k = col("#a8302a") * (0.55 + 0.55 * np.clip(0.6 - hx * 0.5 + hy * 0.3, 0, 1))[..., None]
            ring = (rr > 0.62) & (rr < 0.70)
            k = np.where(ring[..., None], col("#6a1a18"), k)
            holes = np.zeros_like(rr, dtype=bool)
            for q in range(10):
                ang = q * math.pi / 5 + turn
                holes |= np.hypot(u - math.cos(ang) * r * 0.48, v - math.sin(ang) * r * 0.48) < r * 0.085
            k = np.where(holes[..., None], col("#1a0e0c"), k)
            hub = rr < 0.30
            k = np.where(hub[..., None], col("#e2b830") * (0.6 + 0.6 * np.clip(0.6 - hx * 0.5 + hy * 0.4, 0, 1))[..., None], k)
            lugs = np.zeros_like(rr, dtype=bool)
            for q in range(6):
                ang = q * math.pi / 3
                lugs |= np.hypot(u - math.cos(ang) * r * 0.2, v - math.sin(ang) * r * 0.2) < r * 0.04
            k = np.where(lugs[..., None], col("#3a2a14"), k)
            rim = rr > 0.92
            k = np.where(rim[..., None], col("#7a1c18") * (0.6 + 0.6 * np.clip(-hx * 0.6 + hy * 0.5, 0, 1))[..., None], k)
            rust = np.clip((fbm(u / 4, v / 4, seed + 7, 3) - 0.6) * 4, 0, 1)
            k = lerp(k, col("#6a3a20"), (rust * 0.5)[..., None])
            return k, col("#fff0d0") * (win * 0.35 * (rr < 0.9))[..., None]
        val = env * dull
        if style == 1:                                   # slots round the middle
            slot = (np.abs(((a * 8 / (2 * math.pi)) % 1) - 0.5) < 0.17) & (rr > 0.42) & (rr < 0.76)
            val = np.where(slot, 0.06, val)
        elif style == 2:                                 # wire spokes, dark between
            sp = (np.abs(((a * 22 / (2 * math.pi)) % 1) - 0.5) < 0.14) & (rr > 0.24) & (rr < 0.84)
            val = np.where(((rr > 0.24) & (rr < 0.84)) & ~sp, 0.08, val)
        elif style == 3:                                 # a star pressed into it
            star = np.cos(a * 5) * 0.16 + 0.5 > rr
            val = np.where(star, val * 1.25, val * 0.75)
        elif style == 4:                                 # a baby moon: a plain bright dome
            val = val * 1.2
        elif style == 5:                                 # a white ring
            ring = (rr > 0.6) & (rr < 0.8)
            val = np.where(ring, 0.75 + 0.2 * np.clip(-hx + hy, 0, 1), val)
        elif style == 8:                                 # a dent
            dent = np.hypot(u - r * 0.3, v + r * 0.25) < r * 0.28
            val = np.where(dent, val * 0.45 + 0.2 * np.clip(hx, 0, 1), val)
        k = tint * val[..., None]
        if style == 5:
            k = np.where(((rr > 0.6) & (rr < 0.8))[..., None], col("#f2eee4") * val[..., None], k)
        if style == 7:                                   # rusty
            rust = np.clip((fbm(u / 3, v / 3, seed, 3) - 0.42) * 3, 0, 1)
            k = lerp(k, col("#7a3e22") * (0.5 + 0.5 * env)[..., None], (rust * 0.85)[..., None])
        # the rim: a raised ring, lit on its upper left, dark on its lower right; the dark gap inside it
        rim = (rr > 0.88)
        rl = np.clip(0.5 - hx * 0.6 + hy * 0.6, 0, 1)
        k = np.where(rim[..., None], tint * (0.18 + 0.85 * rl)[..., None], k)
        gap = np.abs(rr - 0.875) < 0.03
        k = np.where(gap[..., None], col("#1a1816"), k)
        hub = rr < 0.18
        hv = 0.3 + 0.8 * np.exp(-((hx + 0.08) / 0.07) ** 2 - ((hy - 0.05) / 0.07) ** 2)
        k = np.where(hub[..., None], tint * hv[..., None], k)
        e = k * (0.34 * place)[..., None] + col("#fff6e4") * (np.clip(win - 0.5, 0, 1) * 1.4 * place * (rr < 0.88))[..., None]
        return k * 0.35, e
    return f


def hubcaps(st, G="back"):
    places = hubcap_places()
    for i, (wall, u, v, r, style, seed) in enumerate(places):
        lift = 1.5 + (i % 3) * 0.6
        if wall == "back":
            c, n = (u, v, lift), (0, 0, 1)
        elif wall == "left":
            c, n = (lift, v, u), (1, 0, 0)
        else:
            c, n = (M.W - lift, v, u), (-1, 0, 0)
        st.disc3(c, r, n, m_hubcap(style, seed, r), sides=28, name="hubcaps", grp=G)
    return places


# ---------------------------------------------------------------- the fan that has not turned since 1979
def fan(st, G="back"):
    X, Y, Z = M.FAN
    wd = wood("#7a4a2a", 151, "x", 0.25, 1.2, 30.0)
    st.stick((X, M.H, Z), (X, Y + 10, Z), 1.4, col("#7a6a50"), "fan", grp=G)
    st.cyl((X, Z), 9.0, Y + 2, Y + 12, chrome("#8a7a5a", 0.3, 152), name="fan", grp=G, cap=col("#6a5a40"))
    st.cyl((X, Z), 5.0, Y - 4, Y + 2, chrome("#8a7a5a", 0.3, 153), name="fan", grp=G, cap=col("#5a4a30"))
    for k in range(4):
        a = math.radians(k * 90 + 28)
        dx, dz = math.cos(a), math.sin(a)
        tx, tz = -dz, dx
        r0, r1, hw = 10.0, 62.0, 7.0
        pts = [(X + dx * r0 - tx * hw * 0.7, Y, Z + dz * r0 - tz * hw * 0.7), (X + dx * r1 - tx * hw, Y - 2.0, Z + dz * r1 - tz * hw),
               (X + dx * r1 + tx * hw, Y - 0.5, Z + dz * r1 + tz * hw), (X + dx * r0 + tx * hw * 0.7, Y + 1.0, Z + dz * r0 + tz * hw * 0.7)]
        def m_blade(c):
            k_ = col("#8a5a34") * (0.85 + 0.25 * fbm(c.U / 6, c.V / 1.5, 154, 2))[..., None]
            dust = np.clip((fbm(c.U / 2, c.V / 2, 155, 2) - 0.4) * 2, 0, 1) * 0.35
            return lerp(k_, col("#b8b0a0"), dust[..., None])
        st.poly(pts, m_blade, "fan", grp=G, flag=1)
        st.box(X + dx * 8 - 2, X + dx * 8 + 2, Y - 1, Y + 1, Z + dz * 8 - 2, Z + dz * 8 + 2, chrome("#8a7a5a", 0.3, 156), "fan", grp=G, shadow=False)
    # the pull chain, and a cobweb from one blade to the downrod
    st.stick((X + 4, Y - 4, Z + 2), (X + 4, Y - 34, Z + 2), 0.18, col("#c8b880"), "fan", grp=G)
    st.ball((X + 4, Y - 35, Z + 2), 0.9, col("#c8b880"), "fan", grp=G, shadow=False)


# ---------------------------------------------------------------- the foreground
def foreground(st, G="front"):
    """What stands near us and is cut off by the picture's edges (front plane): a stack of water flats at the bottom
    left, a crate of empty pop bottles in the middle, old tyres stacked at the bottom right with a hubcap leaning on
    them (one that did not make the wall)."""
    x0, x1, y0, y1, z0, z1 = M.WATERFLATS
    def m_flat(c):
        if c.face == "top":
            u = (c.X - x0) % 6.5
            v = (c.Z - z0) % 6.5
            cap = np.hypot(u - 3.25, v - 3.25) < 1.6
            k = np.where(cap[..., None], col("#3a6ab8"), col("#a8c4dc"))
            shine = (fbm(c.X / 6, c.Z / 6, 161, 2) > 0.66)
            return k, col("#ffffff")[None, :] * (shine * 0.25)[:, None]
        u = c.X if c.face in ("front", "back") else c.Z
        bottle = np.abs((u % 6.5) - 3.25) < 2.8
        lab = (np.abs(((c.Y % 20) - 9)) < 3.5)
        return np.where(bottle[..., None], np.where(lab[..., None], col("#3a6ab8"), col("#b8d0e4")), col("#5a7088"))
    st.box(x0, x1, 0, 20, z0, z1, m_flat, "waterflats", grp=G, foot=True)
    st.box(x0 + 6, x1 + 4, 20, 40, z0 + 8, z1 - 6, m_flat, "waterflats", grp=G)
    # the crate of empty bottles
    cx0, cx1, cy0, cy1, cz0, cz1 = M.CRATE
    w = wood("#9a6a3a", 165, "x", 0.25)
    st.box(cx0, cx1, 0, cy1, cz0, cz0 + 2.5, w, "crate", grp=G, foot=True)
    st.box(cx0, cx1, 0, cy1, cz1 - 2.5, cz1, w, "crate", grp=G)
    st.box(cx0, cx0 + 2.5, 0, cy1, cz0, cz1, w, "crate", grp=G)
    st.box(cx1 - 2.5, cx1, 0, cy1, cz0, cz1, w, "crate", grp=G)
    st.box(cx0, cx1, 0, 3, cz0, cz1, w, "crate", grp=G, shadow=False)
    glass = ["#4a8a5a", "#8a5a2a", "#c8d8d0", "#4a8a5a", "#3a5a8a"]
    k = 0
    for i in range(6):
        for j in range(3):
            bx = cx0 + 12 + i * (cx1 - cx0 - 24) / 5
            bz = cz0 + 14 + j * (cz1 - cz0 - 28) / 2
            if (i + 2 * j) % 7 == 3:
                continue                                                                          # an empty slot or two
            g = glass[k % len(glass)]
            k += 1
            def m_btl(c, g=g):
                a = col(g)
                n = normals(c)
                sh = np.clip(-n[:, 0] * 0.6 + n[:, 2] * 0.5, 0, 1)
                return a * 0.6, a * 0.25 + col("#ffffff")[None, :] * (np.clip(sh - 0.6, 0, 1) * 1.2)[:, None]
            st.cyl((bx, bz), 3.4, 3, 30, m_btl, name="crate", grp=G, shadow=False)
            st.cyl((bx, bz), 1.4, 30, 42, m_btl, name="crate", grp=G, shadow=False)
    # the tyres, and the hubcap leaning on them
    tx, tz, tr, tn = M.TIRES
    def m_tyre(c):
        n = normals(c)
        k = col("#2a2628") * (0.8 + 0.3 * fbm(c.X / 3, c.Y / 3 + c.Z / 3, 166, 2))[..., None]
        tread = np.abs(np.sin(c.ang * 40)) > 0.6 if hasattr(c, "ang") else False
        k = np.where(np.asarray(tread)[..., None], k * 0.8, k)
        return k
    for i in range(tn):
        y = i * 19.0
        st.cyl((tx + (i % 2) * 3, tz - (i % 2) * 2), tr, y, y + 18, m_tyre, name="tires", grp=G, foot=(i == 0), cap=col("#1e1a1c"))
    st.cyl((tx + 3, tz - 2), tr * 0.55, tn * 19.0 - 0.5, tn * 19.0 + 0.2, plain("#0e0c0c", 0.05), name="tires", grp=G, shadow=False)
    st.disc3((tx - tr - 2, 22, tz + 14), 17.0, (-0.25, 0.25, 0.94), m_hubcap(1, 77, 17.0), sides=28, name="tires", grp=G)

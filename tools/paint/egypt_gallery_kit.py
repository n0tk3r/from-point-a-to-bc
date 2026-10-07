"""The Grand Gallery, measured: where every stone is, and which stone each pixel of the picture sees.

One true perspective for the whole picture. The world is in centimetres: X to the right of the middle,
Y up from the level floor at the foot, Z away from us. The gallery's own floor is a ramp that starts
at Z1 and climbs; `h` is height above that ramp (measured straight up), so everything that runs
with the gallery (benches, the laps of the walls, the roof) is at a constant h.

The game's two depth numbers are built in: anything standing on the ramp is drawn at the scale the
game uses for a person there (horizon 50, full 580)."""

import math

import numpy as np

from brush import F32, grid, noise

W, H = 800, 600
F = 500.0                                   # the lens, in pixels
VX, VY = 400.0, 50.0                        # where the ramp runs to: the game's horizon
YH = 260.0                                  # where level things run to (the level floor at the foot)
Y1 = 500.0                                  # the picture row where the ramp leaves the level floor
EYE = (Y1 - YH) * 580.0 / (Y1 - VY)         # the lens above the level floor (about 3.1 m)
T = (YH - VY) / F                           # the slope of the ramp (rise over run)
Z1 = F * 580.0 / (Y1 - VY)                  # where the ramp starts

HALF = 220.0                                # wall to wall is twice this at the floor
RAMP = 120.0                                # half the width of the ramp between the benches
TR = 42.0                                   # half the width of the cut that leads to the low passage
BENCH = 55.0                                # how high the benches stand above the ramp
LIP0, COURSE, STEPIN, NCOR = 300.0, 60.0, 20.0, 7        # the first lap, each lap's height, how far each steps in, how many
TOP = LIP0 + COURSE * NCOR                  # the roof, above the ramp
Z_END = F / 0.3                             # the top of the ramp (people are a third of full size there)
STEP_H = 100.0                              # the tall step
Z_WALL = Z_END + 150.0                      # the end wall, behind the step
MOUTH_H = 80.0                              # the low passage: how high its opening is
LEDGE_X = 160.0                             # the level bench along the right wall at the foot starts here
ZA, ZB, GATE_H = 466.0, 616.0, 150.0        # the way in from outside: an opening in the left wall
DOOR_W, DOOR_H = 62.0, 165.0                # the upper doorway (half width, height)


def R(Z):
    """How high the ramp's plane is above the level floor at depth Z."""
    return (Z - Z1) * T


Y_STEP = R(Z_END) + STEP_H
ZM = Z1 + 100.0 / T                         # where the cut ends, at the mouth of the low passage


def P(X, Y, Z):
    """World -> picture."""
    return (VX + F * X / Z, YH + F * (EYE - Y) / Z)


def Pr(X, h, Z):
    """The same, for a place given by its height above the ramp."""
    return P(X, R(Z) + h, Z)


def floor_at(row):
    """Depth of the level floor at a picture row."""
    return EYE * F / max(row - YH, 1e-3)


def ramp_at(row):
    """Depth of the ramp at a picture row."""
    return 580.0 * F / max(row - VY, 1e-3)


def half_at(h):
    """Half the width between the walls at a height above the ramp (a number or an array)."""
    n = np.where(h < LIP0, 0, np.floor((h - LIP0) / COURSE) + 1)
    return HALF - STEPIN * np.clip(n, 0, NCOR)


# ---- what a pixel can be looking at
LANDING, RAMP_S, TRENCH, TRENCH_L, TRENCH_R, MOUTH, LOW_IN = 1, 2, 3, 4, 5, 6, 7
BTOP_L, BTOP_R, BIN_L, BIN_R, BFRONT_L, BFRONT_R = 8, 9, 10, 11, 12, 13
LEDGE_TOP, LEDGE_IN, STEP_F, STEP_T, END, DOOR_IN, PASS_FAR, PASS_FLOOR, ROOF = 14, 15, 16, 17, 18, 19, 20, 21, 22
WALL_L, WALL_R, SOFF_L, SOFF_R = 30, 40, 50, 60            # plus the number of the course, 0 to 7

NORMALS = {LANDING: (0, 1, 0), TRENCH: (0, 1, 0), PASS_FLOOR: (0, 1, 0), LEDGE_TOP: (0, 1, 0), STEP_T: (0, 1, 0),
           TRENCH_L: (1, 0, 0), TRENCH_R: (-1, 0, 0), BIN_L: (1, 0, 0), BIN_R: (-1, 0, 0), LEDGE_IN: (-1, 0, 0),
           MOUTH: (0, 0, -1), BFRONT_L: (0, 0, -1), BFRONT_R: (0, 0, -1), STEP_F: (0, 0, -1), END: (0, 0, -1),
           PASS_FAR: (0, 0, -1), LOW_IN: (0, 0, -1), DOOR_IN: (0, 0, -1)}
_up = np.array([0, 1, -T]) / math.hypot(1, T)
for _k in (RAMP_S, BTOP_L, BTOP_R):
    NORMALS[_k] = tuple(_up)
NORMALS[ROOF] = tuple(-_up)
for _n in range(NCOR + 1):
    NORMALS[WALL_L + _n] = (1, 0, 0)
    NORMALS[WALL_R + _n] = (-1, 0, 0)
    NORMALS[SOFF_L + _n] = tuple(-_up)
    NORMALS[SOFF_R + _n] = tuple(-_up)


def cast(wobble=0.6, seed=3, ss=1):
    """For every pixel: which surface it sees and where on it. -> dict of arrays: sid, X, Y, Z, h.
    `wobble` lets every edge wander by that many pixels, as a hand-drawn line does. `ss` works at that
    many times the picture's size (to be reduced afterwards, so edges come out smooth)."""
    from brush import resize
    shape = (H * ss, W * ss)
    px, py = grid(shape)
    px, py = (px + 0.5) / ss - 0.5, (py + 0.5) / ss - 0.5
    wx = wy = 0.0
    if wobble:
        wx = (noise((H, W), 52, seed, 3) - 0.5) * 2 * wobble + (noise((H, W), 15, seed + 5, 2) - 0.5) * 0.7 * wobble
        wy = (noise((H, W), 52, seed + 1, 3) - 0.5) * 2 * wobble + (noise((H, W), 15, seed + 6, 2) - 0.5) * 0.7 * wobble
        if ss > 1:
            wx, wy = resize(wx, shape), resize(wy, shape)
        px, py = px + wx, py + wy
    dx = ((px - VX) / F).astype(np.float64)                 # X for each unit of Z
    dy = ((py - YH) / F).astype(np.float64)                 # (EYE - Y) for each unit of Z
    dv = ((py - VY) / F).astype(np.float64)                 # (580 - h) for each unit of Z
    zbuf = np.full(shape, 1e9)
    sid = np.zeros(shape, dtype=np.int16)

    def put(Z, ok, k):
        ok = ok & np.isfinite(Z) & (Z > 1.0) & (Z < zbuf)
        zbuf[ok] = Z[ok]
        sid[ok] = k

    def at(Z):
        Y = EYE - dy * Z
        return dx * Z, Y, Y - R(Z)

    with np.errstate(divide="ignore", invalid="ignore"):
        # ---- level planes
        Z = EYE / dy
        X, Y, h = at(Z)
        put(Z, (np.abs(X) <= HALF) & (Z <= Z1), LANDING)
        put(Z, (np.abs(X) <= TR) & (Z > Z1) & (Z <= ZM), TRENCH)
        put(Z, (X < -HALF) & (Z >= ZA) & (Z <= ZB), PASS_FLOOR)
        Z = (EYE - BENCH) / dy
        X, Y, h = at(Z)
        put(Z, (X >= LEDGE_X) & (X <= HALF) & (Z <= Z1), LEDGE_TOP)
        Z = (EYE - Y_STEP) / dy
        X, Y, h = at(Z)
        put(Z, (np.abs(X) <= HALF) & (Z >= Z_END) & (Z <= Z_WALL), STEP_T)
        # ---- planes that run with the ramp
        Z = 580.0 / dv
        X, Y, h = at(Z)
        put(Z, (np.abs(X) <= RAMP) & (Z >= Z1) & (Z <= Z_END) & ~((np.abs(X) < TR) & (Z < ZM)), RAMP_S)
        Z = (580.0 - BENCH) / dv
        X, Y, h = at(Z)
        ok = (np.abs(X) >= RAMP) & (np.abs(X) <= HALF) & (Z >= Z1) & (Z <= Z_END)
        put(Z, ok & (X < 0), BTOP_L)
        put(Z, ok & (X > 0), BTOP_R)
        for n in range(1, NCOR + 1):
            Z = (580.0 - (LIP0 + COURSE * (n - 1))) / dv
            X, Y, h = at(Z)
            ok = (np.abs(X) >= HALF - STEPIN * n) & (np.abs(X) <= HALF - STEPIN * (n - 1)) & (Z <= Z_WALL)
            put(Z, ok & (X < 0), SOFF_L + n)
            put(Z, ok & (X > 0), SOFF_R + n)
        Z = (580.0 - TOP) / dv
        X, Y, h = at(Z)
        put(Z, (np.abs(X) <= HALF - STEPIN * NCOR) & (Z <= Z_WALL), ROOF)
        # ---- planes that face the middle
        for side, wall, bin_, trench in ((-1, WALL_L, BIN_L, TRENCH_L), (1, WALL_R, BIN_R, TRENCH_R)):
            for n in range(NCOR + 1):
                c = side * (HALF - STEPIN * n)
                Z = c / dx
                X, Y, h = at(Z)
                lo = LIP0 + COURSE * (n - 1) if n else -1e9
                ok = (h >= lo) & (h <= LIP0 + COURSE * n) & (Z <= Z_WALL)
                if n == 0:
                    foot = np.where(Z < Z1, Y >= 0, np.where(Z <= Z_END, h >= BENCH, Y >= Y_STEP))
                    ok = ok & foot
                    if side < 0:
                        ok = ok & ~((Z >= ZA) & (Z <= ZB) & (Y <= GATE_H))
                put(Z, ok, wall + n)
            Z = side * RAMP / dx
            X, Y, h = at(Z)
            put(Z, (h >= 0) & (h <= BENCH) & (Z >= Z1) & (Z <= Z_END), bin_)
            Z = side * TR / dx
            X, Y, h = at(Z)
            put(Z, (Y >= 0) & (h <= 0) & (Z >= Z1) & (Z <= ZM), trench)
        Z = LEDGE_X / dx
        X, Y, h = at(Z)
        put(Z, (Y >= 0) & (Y <= BENCH) & (Z <= Z1), LEDGE_IN)
        # ---- planes that face us
        def facing(c):
            Z = np.full(shape, float(c))
            X, Y, h = at(Z)
            return Z, X, Y, h
        Z, X, Y, h = facing(Z1)
        ok = (np.abs(X) >= RAMP) & (np.abs(X) <= HALF) & (Y >= 0) & (Y <= BENCH)
        put(Z, ok & (X < 0), BFRONT_L)
        put(Z, ok & (X > 0), BFRONT_R)
        Z, X, Y, h = facing(ZM)
        put(Z, (np.abs(X) <= TR) & (Y >= MOUTH_H) & (Y <= 100.0), MOUTH)
        put(Z, (np.abs(X) <= TR) & (Y >= 0) & (Y < MOUTH_H), LOW_IN)
        Z, X, Y, h = facing(Z_END)
        put(Z, (np.abs(X) <= HALF) & (Y <= Y_STEP) & (h >= np.where(np.abs(X) <= RAMP, 0.0, BENCH)), STEP_F)
        Z, X, Y, h = facing(Z_WALL)
        inside = (np.abs(X) <= half_at(h)) & (Y >= Y_STEP) & (h <= TOP)
        door = (np.abs(X) <= DOOR_W) & (Y <= Y_STEP + DOOR_H)
        put(Z, inside & ~door, END)
        put(Z, inside & door, DOOR_IN)
        Z, X, Y, h = facing(ZB)
        put(Z, (X < -HALF) & (Y >= 0) & (Y <= GATE_H), PASS_FAR)

    Z = np.where(sid > 0, zbuf, Z_WALL)
    Y = EYE - dy * Z
    out = dict(sid=sid, X=(dx * Z).astype(F32), Y=Y.astype(F32), Z=Z.astype(F32), h=(Y - R(Z)).astype(F32),
               px=px, py=py, wx=wx, wy=wy, ss=ss, shape=shape)
    return out


def edges(sid, Z=None, jump=40.0):
    """Where one surface ends and another begins (a mask one pixel wide)."""
    e = np.zeros(sid.shape, dtype=bool)
    e[:, 1:] |= sid[:, 1:] != sid[:, :-1]
    e[1:, :] |= sid[1:, :] != sid[:-1, :]
    if Z is not None:
        e[:, 1:] |= np.abs(Z[:, 1:] - Z[:, :-1]) > jump
        e[1:, :] |= np.abs(Z[1:, :] - Z[:-1, :]) > jump
    return e.astype(F32)


def per_px(a, sid):
    """How many units of `a` one picture pixel covers (the size of its gradient), ignoring the jumps
    where one surface gives way to another."""
    big = 1e9
    fx = np.full(a.shape, big, dtype=F32)
    bx = np.full(a.shape, big, dtype=F32)
    fy = np.full(a.shape, big, dtype=F32)
    by = np.full(a.shape, big, dtype=F32)
    same = sid[:, 1:] == sid[:, :-1]
    d = np.where(same, np.abs(a[:, 1:] - a[:, :-1]), big)
    fx[:, :-1], bx[:, 1:] = d, d
    same = sid[1:, :] == sid[:-1, :]
    d = np.where(same, np.abs(a[1:, :] - a[:-1, :]), big)
    fy[:-1, :], by[1:, :] = d, d
    gx, gy = np.minimum(fx, bx), np.minimum(fy, by)
    gx = np.where(gx >= big, 0, gx)
    gy = np.where(gy >= big, 0, gy)
    return np.maximum(np.hypot(gx, gy), 1e-4).astype(F32)


def blocks(a, b, rows, seed, length=(120.0, 230.0), start=0.0, stop=2600.0):
    """Squared stones laid in rows. `a` runs along the wall and `b` across the rows (both in cm, as
    arrays); `rows` are the heights where one row ends and the next begins. Every row gets its own
    upright joints, so they break bond. -> (a number 0..1 for each stone, cm to the nearest upright
    joint, cm to the nearest bed)."""
    rows = np.asarray(rows, dtype=np.float64)
    r = np.clip(np.searchsorted(rows, b) - 1, 0, len(rows) - 2)
    tone = np.zeros(a.shape, dtype=F32)
    da = np.full(a.shape, 1e6, dtype=F32)
    rng = np.random.default_rng(seed)
    for i in range(len(rows) - 1):
        joints = [start - rng.random() * length[0]]
        while joints[-1] < stop:
            joints.append(joints[-1] + length[0] + rng.random() * (length[1] - length[0]))
        joints = np.array(joints)
        tones = rng.random(len(joints) + 1).astype(F32)
        m = r == i
        if not m.any():
            continue
        j = np.clip(np.searchsorted(joints, a[m]), 1, len(joints) - 1)
        tone[m] = tones[j]
        da[m] = np.minimum(a[m] - joints[j - 1], joints[j] - a[m])
    db = np.minimum(b - rows[r], rows[r + 1] - b).astype(F32)
    return tone, np.abs(da), np.abs(db)

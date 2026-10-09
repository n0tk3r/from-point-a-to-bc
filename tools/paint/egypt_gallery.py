"""Egypt, about 2560 B.C.: inside the pyramid. The great rising gallery, seen from its foot.

THE PLAN
  Light      Small oil lamps (a wick in a dish) stand in the slots of the two benches all the way up, and
             two more at the foot. Each makes a warm pool on the stone beside it and nothing else: between
             them the stone falls away into cool blue-brown dark. From the opening in the left wall at the
             foot comes cool daylight, lying a little way across the level floor. The far doorway at the
             top is faintly lit from the room beyond. LIGHT COMES FROM BELOW: every lap of the wall is
             brightest along its lower edge and goes dark toward its top.
  Depth      horizon 50 (where the ramp runs to), full 580. The level floor at the foot runs to row 260.
  Three      DARK: the upper laps of both walls, the roof, the top of the gallery, the bottom corners.
  tones      MIDDLE: the ramp and the lower walls where lamplight thins out.
             LIGHT: the pools at each lamp, the daylight at the foot on the left, the far doorway.
             The lamps make two strings of light that close on the doorway: that is where the eye goes.
  Places     the way in from outside: left wall at the foot, about (164..222, 389..593), daylight inside it
             the low passage: the dark mouth at the end of the level cut in the ramp's foot, about (400, 412);
               people walk up the ramp on either side of the cut
             slot-foot: the first, big slot of the right-hand bench, about (545, 433)
             the tall step and the upper doorway: (400, 194) and (400, 174)
             builders' marks: right wall above the level bench, in the lamp's pool, about (599, 381)
             oil jars, spare lamp dishes, a lit lamp: on the floor in front of the left bench, about (270, 476)
             the lamp boy: sits on the edge of the level bench along the right wall, feet at (582, 586)
  Cut-outs   front.png (a ladder and a jar in the near left corner; a water jar, a cup and a lit lamp on the
             bench at the near right), mirror-foot.png (the car's door mirror in slot-foot), mirror-top.png
             (the copper hand mirror on the lip of the step)
  Liberties  The gallery is about 4.4 m wide at the floor, not 2: at the size the game draws people a 2 m
             passage would be under 200 pixels wide at the bottom of the picture, with no room at its foot for
             the way in, the jars, the bench and the boy. It keeps its shape: seven laps close it to 1.6 m.

Everything is measured in egypt_gallery_kit.py, which also works out which stone every pixel sees."""

import json, math, os, sys, time
import numpy as np
from PIL import Image
from brush import *
import egypt_gallery_kit as K
import egypt_gallery_things as T
from egypt_gallery_kit import P, Pr, R, HALF, RAMP, TR, BENCH, Z1, ZM, Z_END, Z_WALL, ZA, ZB

W, H = 800, 600
OUT = "out/egypt-gallery"
SHAPE = (H, W)

# ---- the slots in the benches (side, near end, far end, inner edge, outer edge), and the lamps
SLOT_Z = [700.0, 822.0, 944.0, 1066.0, 1188.0, 1310.0, 1432.0, 1554.0]
SLOTS = [(-1, z - 23, z + 23, 188.0, 211.0) for z in SLOT_Z] + [(1, z - 23, z + 23, 188.0, 211.0) for z in SLOT_Z[1:]]
SLOT_FOOT = (1, 655.0, 715.0, 183.0, 212.0)                 # the big one, where the car mirror will go
FLOOR_LAMP = (-116.0, 7.0, 604.0)                           # on the floor by the oil jars
LEDGE_LAMP = (186.0, BENCH + 7.0, 598.0)                    # on the level bench, by the boy


def lamp_list():
    """(X, Y, Z, strength, kind) of every flame. Up the gallery the lamps stand in slots 1, 3, 5 and 7, on the
    left and the right bench by turns, so the pools of light step from side to side with dark between,
    and two burn at the top, one each side of the step."""
    out = [FLOOR_LAMP + (0.8, "floor"), LEDGE_LAMP + (1.0, "ledge"), (198.0, BENCH + 7.0, 424.0, 0.8, "hidden")]
    for i, side, power in ((1, -1, 1.0), (3, 1, 0.95), (5, -1, 0.86), (7, 1, 0.78), (7, -1, 0.70)):
        z = SLOT_Z[i]
        out.append((side * 199.5, R(z) + BENCH + 6.0, z, power, "slot"))
    return out


LAMPS = lamp_list()
WARM = np.array([1.0, 0.57, 0.26], dtype=F32)                # lamplight: thin, it is deep orange; thick, it burns out to gold
COOL = np.array([0.40, 0.62, 1.0], dtype=F32)                # daylight that has come a long way down a stone passage


def nz(g, cell, seed, octaves=3):
    """Noise the size of the working picture, with blobs `cell` picture-pixels across."""
    ss = g["ss"]
    cell = cell * ss if np.isscalar(cell) else (cell[0] * ss, cell[1] * ss)
    return noise(g["shape"], cell, seed, octaves)


def normals(sid):
    table = np.zeros((80, 3), dtype=F32)
    for k, n in K.NORMALS.items():
        table[k] = n
    return table[sid]


def lamplight(g, n, reach=74.0, floor_reach=78.0):
    """How much lamplight reaches every pixel; a soft wide glow for the light that bounces about; and the
    shine of the lamps in the polished ramp. The lamps are taken to stand a little out from the wall and a
    little above the bench, or their own bench would hide them from the floor."""
    X, Y, Z, sid = g["X"], g["Y"], g["Z"], g["sid"]
    floorish = np.isin(sid, (K.RAMP_S, K.TRENCH, K.LANDING, K.PASS_FLOOR))
    direct = np.zeros(g["shape"], dtype=F32)
    soft = np.zeros(g["shape"], dtype=F32)
    shine = np.zeros(g["shape"], dtype=F32)
    climb = np.zeros(g["shape"], dtype=F32)
    ex, ey, ez = -X, K.EYE - Y, -Z                                        # toward the eye
    el = np.sqrt(ex * ex + ey * ey + ez * ez) + 1e-3
    for (lx, ly, lz, power, kind) in LAMPS:
        if kind == "slot":
            lx = lx * 0.86
        for lift, share, where, rr_ in ((14.0, 1.0, ~floorish, reach), (36.0, {"hidden": 0.0, "floor": 0.95}.get(kind, 0.66), floorish, floor_reach)):
            if share == 0:
                continue
            vx, vy, vz = lx - X, ly + lift - Y, lz - Z
            d = np.sqrt(vx * vx + vy * vy + vz * vz) + 1e-3
            facing = (n[..., 0] * vx + n[..., 1] * vy + n[..., 2] * vz) / d
            lam = np.clip((facing + 0.16) / 1.16, 0, 1)
            direct += where * (power * share * lam / (1 + (d / rr_) ** 2) ** 1.4).astype(F32)
            if share < 1:
                hx, hy, hz = vx / d + ex / el, vy / d + ey / el, vz / d + ez / el
                hl = np.sqrt(hx * hx + hy * hy + hz * hz) + 1e-6
                spec = np.clip((n[..., 0] * hx + n[..., 1] * hy + n[..., 2] * hz) / hl, 0, 1) ** 60
                shine += (sid == K.RAMP_S) * (power * spec / (1 + (d / 260.0) ** 2)).astype(F32)
        d2 = (lx - X) ** 2 + (ly - Y) ** 2 + (lz - Z) ** 2
        soft += (power / (1 + d2 / 170.0 ** 2)).astype(F32)
        if kind != "floor":                                               # lamplight climbs the wall behind it, a long way, failing as it goes
            rise = np.clip(Y - ly, 0, None)
            mine = (X * lx > 0) & (np.abs(X) > 60) & ~floorish
            climb += mine * (power * np.exp(-np.abs(Z - lz) / (70.0 + rise * 0.35)) * np.exp(-rise / 210.0)).astype(F32)
    direct = np.clip(direct - 0.012, 0, None)                             # far from any lamp there is no lamplight at all
    return direct, soft, shine, climb


def daylight(g, n):
    """The cool light from outside: it comes down the low passage in the left wall and lies a little way
    across the level floor, in the shape of the opening, soft at its edges and soon gone."""
    X, Y, Z, sid = g["X"], g["Y"], g["Z"], g["sid"]
    out = np.zeros(g["shape"], dtype=F32)
    across = np.clip(X + HALF, 0, None)                                   # how far in from the left wall
    soft = 5 + 0.16 * across
    skew = across * 0.22                                                  # it comes in a little aslant, leaning up the gallery
    band = step(ZA + 8 - soft + skew, ZA + 8 + soft * 0.6 + skew, Z) * (1 - step(ZB - 4 - soft * 0.4 + skew, ZB - 4 + soft + skew, Z))
    fade = np.exp(-across / 78.0) * (0.75 + 0.5 * nz(g, 34, 77, 3))
    out += (sid == K.LANDING) * band * fade * 1.55
    out += (sid == K.LEDGE_IN) * band * fade * 1.4
    inside = np.clip((-X - HALF) / 75.0, 0, 1)
    out += (sid == K.PASS_FAR) * (0.24 + 0.66 * inside ** 1.3) * (1.25 - 0.7 * np.clip(Y / K.GATE_H, 0, 1))
    out += (sid == K.PASS_FLOOR) * (0.72 + 0.8 * inside)
    # and what the lit floor throws back onto the stone round about
    d2 = (X + HALF - 40) ** 2 + (Y - 30) ** 2 + (Z - (ZA + ZB) / 2) ** 2
    out += (sid != K.PASS_FAR) * (sid != K.PASS_FLOOR) * 0.055 / (1 + d2 / 120.0 ** 2)
    return out.astype(F32)


def stone(g, seed=5):
    """The color of the stone itself before any light falls on it: pale limestone, every block a little
    different, the ramp polished, the roof and the laps plainer. -> (color, joints, block tone)
    `joints` is how many (working) pixels each pixel is from the nearest joint between two stones."""
    X, Y, Z, h, sid, shape = g["X"], g["Y"], g["Z"], g["h"], g["sid"], g["shape"]
    tone = np.full(shape, 0.5, dtype=F32)
    da = np.full(shape, 1e6, dtype=F32)                                   # cm to an upright joint
    db = np.full(shape, 1e6, dtype=F32)                                   # cm to a bed
    ua = np.ones(shape, dtype=F32)                                        # cm per pixel, along and across
    ub = np.ones(shape, dtype=F32)
    rows = [-500.0, BENCH, 172.0, K.LIP0] + [K.LIP0 + K.COURSE * i for i in range(1, K.NCOR + 1)]

    def lay(mask, a, b, rws, sd, length, stop=2600.0, start=0.0):
        t, xa, xb = K.blocks(a, b, rws, sd, length, start, stop)
        tone[mask], da[mask], db[mask] = t[mask], xa[mask], xb[mask]
        ua[mask], ub[mask] = K.per_px(a, sid)[mask], K.per_px(b, sid)[mask]

    left = (sid >= K.WALL_L) & (sid <= K.WALL_L + K.NCOR)
    right = (sid >= K.WALL_R) & (sid <= K.WALL_R + K.NCOR)
    lay(left, Z, h, rows, seed + 1, (130.0, 250.0), start=300.0)
    lay(right, Z, h, rows, seed + 2, (130.0, 250.0), start=300.0)
    lay(sid == K.RAMP_S, Z, X, [-RAMP - 1, RAMP + 1], seed + 3, (230.0, 380.0), start=Z1 + 120)
    lay((sid == K.BTOP_L) | (sid == K.BIN_L), Z, X, [-HALF - 1, -RAMP + 0.01, 0], seed + 4, (118.0, 126.0), start=Z1 + 60)
    lay((sid == K.BTOP_R) | (sid == K.BIN_R), Z, X, [0, RAMP - 0.01, HALF + 1], seed + 5, (118.0, 126.0), start=Z1 + 60)
    lay((sid == K.LANDING) | (sid == K.TRENCH), X, Z, [300.0, 452.0, 548.0, Z1 + 0.5, ZM + 1], seed + 6, (95.0, 150.0), start=-HALF, stop=HALF + 200)
    lay((sid == K.END), X, h, [-500.0] + rows[3:], seed + 7, (80.0, 150.0), start=-HALF, stop=HALF + 200)
    lay((sid == K.STEP_F), X, Y, [0.0, 2000.0], seed + 8, (150.0, 190.0), start=-HALF + 20, stop=HALF + 200)
    lay((sid == K.BFRONT_L) | (sid == K.BFRONT_R), X, Y, [-10.0, 200.0], seed + 9, (300.0, 400.0), start=-HALF, stop=HALF + 300)
    lay((sid == K.LEDGE_TOP) | (sid == K.LEDGE_IN), Z, X, [0, 500.0], seed + 10, (105.0, 150.0), start=300.0)
    lay(sid == K.PASS_FAR, X, Y, [-10.0, 78.0, 300.0], seed + 11, (60.0, 110.0), start=-HALF - 300, stop=-HALF + 50)

    # the lintel over the way in is one long level stone, let into the sloping courses
    lint = (sid == K.WALL_L) & (Z > ZA - 34) & (Z < ZB + 34) & (Y > K.GATE_H) & (Y < K.GATE_H + 46)
    tone[lint] = 0.82
    dz = np.minimum(Z - (ZA - 34), (ZB + 34) - Z)
    dyy = np.minimum(Y - K.GATE_H, (K.GATE_H + 46) - Y)
    da[lint], db[lint] = dz[lint], dyy[lint]
    ua[lint], ub[lint] = K.per_px(Z, sid)[lint], K.per_px(Y, sid)[lint]

    base = ramp(tone, [(0.0, "#bfa880"), (0.3, "#d6c39a"), (0.65, "#e8d8b2"), (1.0, "#f6ead0")])
    hue = (np.sin(tone * 91.7) * 0.5 + 0.5)[..., None]                    # some stones pinker, some greyer
    base = base * lerp(np.array([1.05, 0.98, 0.92], dtype=F32), np.array([0.95, 1.0, 1.07], dtype=F32), hue)
    base = np.where((sid == K.RAMP_S)[..., None], lerp(base, rgb("#f2e4c2")[None, None, :], 0.6), base)   # the ramp is all of a piece, and polished
    prof = np.convolve(np.random.default_rng(seed + 60).normal(0, 1, 300), np.ones(9) / 9, "same")
    streak = np.interp(X + 7 * np.sin(Z / 95.0), np.linspace(-RAMP - 12, RAMP + 12, 300), prof)
    base = np.where((sid == K.RAMP_S)[..., None], base * (1 + 0.16 * streak)[..., None], base)        # streaked along its length by sledges and feet
    plain = (sid >= K.SOFF_L) | (sid == K.ROOF) | np.isin(sid, (K.TRENCH_L, K.TRENCH_R, K.MOUTH))
    base = np.where(plain[..., None], rgb("#dccca8")[None, None, :], base)
    blot = nz(g, 70, seed + 20, 4) - 0.5                                  # uneven, as stone and paint both are
    fine = nz(g, 14, seed + 21, 3) - 0.5
    run = nz(g, (7, 70), seed + 23, 3) - 0.5                              # and streaked where water and oil and hands have been
    wallish = left | right | (sid == K.END)
    base = base * (1 + blot[..., None] * 0.18 + fine[..., None] * 0.09 + (run * wallish)[..., None] * 0.14)
    high = (wallish & (h >= K.LIP0)).astype(F32)
    base = base * (1 + high * ((tone - 0.5) * 0.34 + run * 0.34 + blot * 0.2))[..., None]              # high up, each stone its own tone, and streaked
    k = (nz(g, 120, seed + 22, 3) - 0.5) * 0.08
    base[..., 0] += k
    base[..., 2] -= k
    # grime low on the walls where people lean and lamps are filled, and dust in the corners of the floor
    low = wallish * (sid % 10 == 0) * (1 - step(0.0, 70.0, np.where(Z < Z1, Y, h - BENCH))) * (0.5 + nz(g, 40, seed + 24, 3))
    base = base * (1 - 0.22 * low)[..., None]
    for (lx, ly, lz, power, kind) in LAMPS:                              # soot on the wall above each lamp
        if kind in ("slot", "ledge"):
            rise = (h - (ly - R(lz))) if kind == "slot" else (Y - ly)
            mine = (left if lx < 0 else right) & (sid % 10 == 0)
            plume = np.exp(-((Z - lz) / (15.0 + np.clip(rise, 0, 400) * 0.10)) ** 2) * step(-6, 14, rise) * (1 - step(60, 230, rise))
            base = base * (1 - (mine * plume * 0.34)[..., None] * np.array([0.9, 1.0, 1.1], dtype=F32))
    joints = np.minimum(da / ua, db / ub)
    return np.clip(base, 0, 1).astype(F32), joints.astype(F32), tone


def shade(g, albedo, seed=5):
    """Stone, lamplight, daylight and the dark between -> the picture, broad and soft."""
    X, Y, Z, h, sid, shape = g["X"], g["Y"], g["Z"], g["h"], g["sid"], g["shape"]
    n = normals(sid)
    direct, soft, shine, climb = lamplight(g, n)
    day = daylight(g, n)
    wall = ((sid >= K.WALL_L) & (sid <= K.WALL_R + K.NCOR)) | (sid == K.END)
    # light from below: each lap is brightest along its lower edge
    lapn = np.clip((h - K.LIP0) / K.COURSE, -1, K.NCOR)
    inlap = np.where(h >= K.LIP0, lapn - np.floor(lapn), 0.0)
    direct = direct * np.where(wall, 1.15 - 0.6 * inlap, 1.0)
    direct = direct * np.where(sid == K.TRENCH, 0.30, 1.0)
    direct = direct * (0.74 + 0.52 * nz(g, 90, seed + 30, 3))             # no pool of light is perfectly even
    direct = 0.70 * np.tanh(direct / 0.70)                                # and the stone by a lamp is gold, never burnt out to white
    # the dark: cool above, a little warmer low down where lit stone throws light back
    up = np.clip((Y - R(np.clip(Z, Z1, None))) / 420.0, 0, 1)
    amb = lerp(rgb("#3c2e46"), rgb("#18285a"), up[..., None]) * 0.66
    amb = amb + (soft * (1 - 0.7 * up))[..., None] * rgb("#7a3a20") * 0.07
    amb = amb * (0.78 + 0.44 * nz(g, 150, seed + 31, 3))[..., None]
    amb = amb * np.where(wall, 1.22 - 0.5 * inlap, 1.0)[..., None]        # even the dark is lighter along the foot of each lap
    amb = amb * np.where(sid == K.RAMP_S, 1.5, 1.0)[..., None]            # the polished ramp gives back more of what little there is
    amb = amb * np.where(sid == K.TRENCH, 0.7, 1.0)[..., None]
    light = amb + (climb * (0.7 + 0.6 * nz(g, 60, seed + 33, 3)))[..., None] * rgb("#b0522a") * 0.16 + direct[..., None] * WARM * 4.2 + shine[..., None] * rgb("#ffb870") * 1.0 + day[..., None] * COOL * 2.2
    pic = albedo * light
    pic = 1 - np.exp(-pic * 1.45)                                         # bright places roll off softly
    # the holes: the low passage is black, the upper doorway is dimly warm
    zin = K.EYE * K.F / np.maximum(g["py"] - K.YH, 1.0)                    # how far in along the passage floor we are looking
    inside = np.exp(-np.clip(zin - ZM, 0, None) / 55.0) * np.clip(1.25 - np.abs(X) / TR, 0, 1)
    hole = lerp(rgb("#0b0a12")[None, None, :], rgb("#4a3640")[None, None, :], (inside * 0.8)[..., None])
    pic = np.where((sid == K.LOW_IN)[..., None], hole, pic)
    dy = np.clip((P(0, K.Y_STEP, Z_WALL)[1] - g["py"]) / 40.0, 0, 1)      # 0 at the sill, 1 at the lintel
    door = ramp(dy, [(0.0, "#e9a650"), (0.3, "#c47a3a"), (0.65, "#7a422a"), (1.0, "#40242a")])
    pic = np.where((sid == K.DOOR_IN)[..., None], door, pic)
    # air: far up the gallery the dark is bluer and a little lifted, and the lights are dimmer
    far = np.clip((Z - 760.0) / 1100.0, 0, 1) ** 1.1
    pic = lerp(pic, rgb("#1c2036")[None, None, :], (far * 0.42)[..., None] * (sid != K.DOOR_IN)[..., None])
    # the corners of the picture go deeper, to hold the eye in the middle
    gx, gy = g["px"], g["py"]
    corner = np.clip(((gx - 400) / 400) ** 2 * 0.55 + ((gy - 330) / 300) ** 2 * 0.5, 0, 1) ** 1.5
    pic = pic * (1 - 0.42 * corner)[..., None]
    return np.clip(pic, 0, 1).astype(F32), dict(direct=direct, soft=soft, day=day, shine=shine)


def small(a, ss):
    """Reduce a working-size array to picture size."""
    if ss == 1:
        return a
    hh, ww = a.shape[0] // ss, a.shape[1] // ss
    return a.reshape((hh, ss, ww, ss) + a.shape[2:]).mean(axis=(1, 3)).astype(F32)


def under(seed=5, ss=1):
    """Everything broad: the stone and the light on it. Worked at `ss` times the size and reduced, so
    that every edge is smooth. -> (picture, things the later passes need, all at picture size)"""
    g = K.cast(wobble=1.0, seed=seed, ss=ss)
    albedo, joints, tone = stone(g, seed)
    pic, info = shade(g, albedo, seed)
    sid = g["sid"]
    line = np.clip(1.25 - joints / ss, 0, 1)
    edge = K.edges(sid, g["Z"])
    lip = np.zeros(g["shape"], dtype=F32)                                 # the first rows of each course that lies under a lap
    for wall in (K.WALL_L, K.WALL_R):
        for n in range(1, K.NCOR + 1):
            upper, lower = sid == wall + n, sid == wall + n - 1
            for r in range(1, 2 * ss + 1):
                lip = np.maximum(lip, (lower & np.roll(upper, r, axis=0)) * (1 - (r - 1) / (2.0 * ss)))
    info = {k: small(v, ss) for k, v in info.items()}
    info.update(line=small(line, ss), edge=small(edge, ss), lip=small(lip, ss), albedo=small(albedo, ss))
    g1 = g if ss == 1 else K.cast(wobble=1.0, seed=seed, ss=1)
    g1["wob"] = (g1["wx"], g1["wy"])
    info["g"] = g1
    return small(pic, ss), info


def PW(g, X, Y, Z):
    """World -> picture, moved the way the wobble moved the stone the place lies on."""
    qx, qy = P(X, Y, max(Z, 1.0))
    ix, iy = int(np.clip(qx, 0, W - 1)), int(np.clip(qy, 0, H - 1))
    return (qx - float(g["wob"][0][iy, ix]), qy - float(g["wob"][1][iy, ix]))


def rr(X, h, Z):
    """A place given by its height above the ramp -> world."""
    return (X, R(Z) + h, Z)


def line3(sheet, g, a, b, color, width=1.0, alpha=1.0, pieces=1, rng=None, gap=0.0):
    """A straight edge in the world, drawn as a hand draws it: in pieces, each a little stronger or
    weaker than the last, with a break here and there."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    for i in range(pieces):
        if rng is not None and rng.random() < gap:
            continue
        p0, p1 = PW(g, *(a + (b - a) * i / pieces)), PW(g, *(a + (b - a) * (i + 1) / pieces))
        k = 1.0 if rng is None else 0.55 + 0.45 * rng.random()
        sheet.line([p0, p1], color, width, alpha * k)


def lamp(sheet, g, X, Y, Z, rng, lit=True, tongue=False):
    """An oil lamp: a shallow dish of red clay with oil in it and a wick at the lip. (X, Y, Z) is where it stands.
    Round four: a lit lamp's flame is drawn by the game, moving; `tongue=True` paints it in still, as approved."""
    k = F_ / Z
    cx, cy = PW(g, X, Y, Z)
    rx, ry = max(2.6, 10.5 * k), max(1.4, 4.4 * k)
    sheet.ellipse(cx, cy - ry * 0.2, rx, ry * 1.25, "#3a1c16")                       # the dish, its foot in shadow
    sheet.ellipse(cx, cy - ry * 0.75, rx, ry, "#b8683a" if lit else "#6a4a44")       # the lip
    sheet.ellipse(cx, cy - ry * 0.75, rx * 0.78, ry * 0.7, "#5a3018" if lit else "#3a2a2c")   # the oil
    if lit:
        fx, fy = cx + rx * 0.62, cy - ry * 0.9
        fh = max(5.0, 16.0 * k)
        if tongue:
            sheet.poly([(fx - fh * 0.26, fy), (fx + fh * 0.26, fy), (fx + fh * 0.1, fy - fh * 0.62), (fx - fh * 0.05, fy - fh)], "#ffb23c")
            sheet.poly([(fx - fh * 0.15, fy), (fx + fh * 0.15, fy), (fx, fy - fh * 0.66)], "#fff6c4")
        sheet.ellipse(cx + rx * 0.2, cy - ry * 0.8, rx * 0.4, ry * 0.3, "#f0b060", 0.8)   # the flame in the oil
    return cx, cy


def stonework(pic, info, seed=5, tongues=False):
    """Over the brushwork: the joints between the stones, a dark line at every hard edge and a light one
    on every edge that faces a lamp, the laps of the walls, the slots in the benches, and the lamps.
    (`tongues=True`: with the lamps' flames painted in still, as approved; round four leaves them to the game.)"""
    g = info["g"]
    sid, X, Y, Z, h = g["sid"], g["X"], g["Y"], g["Z"], g["h"]
    rng = np.random.default_rng(seed + 100)
    lit = np.clip(info["direct"] * 2.6 + info["day"] * 1.1, 0, 1)                    # where there is light for an edge to catch
    far = np.clip((Z - 900.0) / 900.0, 0, 1)

    # ---- joints: tight as a hair in most places, a little open in others
    line = info["line"]
    strength = (0.16 + 0.62 * noise(SHAPE, 60, seed + 40, 3) ** 1.3) * (1 - 0.5 * far) * (0.7 + 0.3 * lit)
    tint(pic, "#6a5148", (line * strength).astype(F32))
    above = np.roll(line, -1, axis=0)                                                # the lower edge of the stone above each bed catches the lamp
    over(pic, "#ffdc9c", (np.clip(above - line, 0, 1) * lit * 0.30).astype(F32))

    # ---- a dark line wherever one surface meets another
    e = info["edge"] * (0.45 + 0.55 * noise(SHAPE, 40, seed + 41, 3)) * (1 - 0.35 * far)
    tint(pic, "#4a3840", np.clip(e * 0.9, 0, 1).astype(F32))

    # ---- and a light one along every edge that stands out toward the lamps
    hi = Sheet(SHAPE)
    cool = Sheet(SHAPE)
    for sgn in (-1, 1):
        line3(hi, g, rr(sgn * RAMP, BENCH, Z1), rr(sgn * RAMP, BENCH, Z_END), "#fff0c0", 1.1, 0.9, 26, rng, 0.06)
        line3(hi, g, (sgn * RAMP, BENCH, Z1), (sgn * HALF, BENCH, Z1), "#fff0c0", 1.2, 0.9, 5, rng)
        line3(hi, g, rr(sgn * TR, 0, Z1), rr(sgn * TR, 0, ZM), "#ffeab8", 1.0, 0.8, 8, rng, 0.08)
        line3(hi, g, (sgn * TR, 0, Z1), (sgn * RAMP, 0, Z1), "#ffeab8", 1.0, 0.45, 4, rng, 0.1)
        for n in range(1, K.NCOR + 1):
            xn = sgn * (HALF - K.STEPIN * n)
            line3(hi, g, rr(xn, K.LIP0 + K.COURSE * (n - 1), 230.0), rr(xn, K.LIP0 + K.COURSE * (n - 1), Z_WALL), "#ffe6b0", 1.2, 0.95, 60, rng, 0.05)
    line3(hi, g, rr(-TR, 0, ZM), rr(TR, 0, ZM), "#ffeab8", 1.1, 0.85, 3, rng)
    line3(hi, g, (-HALF, K.Y_STEP, Z_END), (HALF, K.Y_STEP, Z_END), "#ffe6b0", 1.1, 0.95, 7, rng, 0.12)
    line3(hi, g, (-RAMP, K.Y_STEP - 2, Z_END), (RAMP, K.Y_STEP - 2, Z_END), "#fff2cc", 1.0, 0.6, 5, rng, 0.2)
    line3(hi, g, (K.LEDGE_X, BENCH, 330.0), (K.LEDGE_X, BENCH, Z1), "#fff0c0", 1.3, 0.9, 12, rng, 0.06)
    line3(cool, g, (-HALF, 0, ZB), (-HALF, K.GATE_H, ZB), "#e4f2ff", 1.3, 0.9, 5, rng)   # the far jamb of the way in, in daylight
    line3(cool, g, (-HALF, 0, ZA), (-HALF, 0, ZB), "#d6eaff", 1.2, 0.8, 5, rng)
    for yy in (52.0, 104.0):
        line3(cool, g, (-HALF - 2, yy, ZB), (-HALF - 78, yy, ZB), "#6e80b0", 1.0, 0.55, 3, rng)
    for (xx, y0, y1) in ((-HALF - 30.0, 0.0, 52.0), (-HALF - 58.0, 52.0, 104.0), (-HALF - 22.0, 104.0, K.GATE_H)):
        line3(cool, g, (xx, y0, ZB), (xx, y1, ZB), "#6e80b0", 1.0, 0.5, 2, rng)
    hc, ha = hi.done()
    catch = np.clip(blur(lit, 1.5) * 1.5, 0.0, 1)
    over(pic, hc, (ha * catch).astype(F32))
    over(pic, "#5a6c9c", (ha * (1 - catch) * 0.42 * (1 - 0.4 * far)).astype(F32))                 # in the dark the same edges are a cold thread
    cool.onto(pic)
    shade_top = (sid == K.PASS_FAR) * step(K.GATE_H - 62.0, K.GATE_H, Y)                             # under its lintel the passage is in shade
    tint(pic, "#6a78a8", np.clip(shade_top * 0.55, 0, 1).astype(F32))

    # ---- under each lap, the stone below is set back: a line of shade, strongest where the light is
    tint(pic, "#584048", np.clip(info["lip"] * (0.35 + 0.5 * lit), 0, 1).astype(F32))

    # ---- over every slot a small stone is let into the wall, with a groove cut slantwise across it; and a mason's patch or two
    w = Sheet(SHAPE)
    for (side, z0, z1, x0, x1) in SLOTS + [SLOT_FOOT]:
        q = [PW(g, *rr(side * HALF, BENCH + 20.0, z0 - 4)), PW(g, *rr(side * HALF, BENCH + 20.0, z1 + 4)), PW(g, *rr(side * HALF, BENCH + 50.0, z1 + 4)), PW(g, *rr(side * HALF, BENCH + 50.0, z0 - 4))]
        w.poly(q, "#3c2c30", 0.16)
        w.line(q + [q[0]], "#3c2c30", 1.0, 0.6)
        w.line([q[0], q[2]], "#3c2c30", 1.2, 0.45)
        w.line([(q[3][0], q[3][1] + 1.2), (q[2][0], q[2][1] + 1.2)], "#ffe2a8", 0.8, 0.4)
    for (side, z, y, wd, ht) in ((1, 548.0, 96.0, 30.0, 20.0), (-1, 792.0, 168.0, 26.0, 18.0), (1, 760.0, 250.0, 34.0, 20.0), (-1, 668.0, 236.0, 28.0, 22.0), (1, 452.0, 196.0, 30.0, 24.0)):
        q = [PW(g, side * HALF, y, z), PW(g, side * HALF, y, z + wd), PW(g, side * HALF, y + ht, z + wd), PW(g, side * HALF, y + ht, z)]
        w.poly(q, "#fff0d0", 0.10)
        w.line(q + [q[0]], "#40302e", 0.9, 0.6)
    wc, wa = w.done()
    over(pic, wc, (wa * (0.35 + 0.65 * np.clip(lit * 1.4, 0, 1))).astype(F32))

    # ---- the upper doorway, said properly: we look up into a low passage, and the lit room is at the end of it
    d = Sheet(SHAPE)
    zf = Z_WALL + 290.0
    yt = K.Y_STEP + K.DOOR_H
    sill = PW(g, 0, K.Y_STEP, Z_END)[1] - 0.5
    nl, nr, fl_, fr = PW(g, -K.DOOR_W, yt, Z_WALL), PW(g, K.DOOR_W, yt, Z_WALL), PW(g, -K.DOOR_W, yt, zf), PW(g, K.DOOR_W, yt, zf)
    d.poly([nl, nr, (nr[0], sill), (nl[0], sill)], "#3a2024")
    d.poly([nl, nr, fr, fl_], "#6a3a26")                                                # the roof of the passage
    d.poly([(lerp(nl[0], fl_[0], 0.5), lerp(nl[1], fl_[1], 0.5)), (lerp(nr[0], fr[0], 0.5), lerp(nr[1], fr[1], 0.5)), fr, fl_], "#96522c")
    d.poly([fl_, fr, (fr[0], sill), (fl_[0], sill)], "#f2ae54")                            # the room beyond, in lamplight
    d.poly([fl_, fr, (fr[0], fl_[1] + 5.5), (fl_[0], fl_[1] + 5.5)], "#c06a34")           # its far wall is red granite
    d.poly([(fl_[0] + 3, sill - 7), (fr[0] - 6, sill - 7), (fr[0] - 6, sill), (fl_[0] + 3, sill)], "#ffd27c")
    d.line([(fl_[0] + 9, sill - 9), (fl_[0] + 12, sill - 3)], "#fff4c4", 1.4)               # and something in it is gold
    d.line([nl, (nl[0], sill)], "#1a141c", 1.2)
    d.line([nr, (nr[0], sill)], "#1a141c", 1.2)
    d.line([(nl[0] - 1, nl[1]), (nr[0] + 1, nr[1])], "#1a141c", 1.3)
    d.line([(nl[0] + 1.3, nl[1] + 2), (nl[0] + 1.3, sill)], "#d88a48", 0.9, 0.8)             # the jambs catch it
    d.line([(nr[0] - 1.3, nr[1] + 2), (nr[0] - 1.3, sill)], "#d88a48", 0.9, 0.6)
    ll, lr = PW(g, -K.DOOR_W - 30, yt, Z_WALL), PW(g, K.DOOR_W + 30, yt + 52, Z_WALL)        # the lintel: one great stone
    d.poly([ll, (lr[0], ll[1]), lr, (ll[0], lr[1])], "#8a94c0", 0.10)
    d.line([ll, (ll[0], lr[1]), lr, (lr[0], ll[1])], "#10101c", 1.0, 0.7)
    d.line([(ll[0] + 1, lr[1] + 1.2), (lr[0] - 1, lr[1] + 1.2)], "#6474a8", 0.9, 0.55)
    d.onto(pic)

    # ---- the slots cut in the benches; we look down into them
    s = Sheet(SHAPE)
    flames = []
    with_lamp = {(round(lz), 1 if lx > 0 else -1) for (lx, ly, lz, pw, kind) in LAMPS if kind == "slot"}
    for (side, z0, z1, x0, x1) in SLOTS + [SLOT_FOOT]:
        deep = 13.0
        top = [PW(g, *rr(side * x0, BENCH, z0)), PW(g, *rr(side * x1, BENCH, z0)), PW(g, *rr(side * x1, BENCH, z1)), PW(g, *rr(side * x0, BENCH, z1))]
        backwall = [top[3], top[2], PW(g, *rr(side * x1, BENCH - deep, z1)), PW(g, *rr(side * x0, BENCH - deep, z1))]
        has = (round((z0 + z1) / 2), side) in with_lamp
        s.poly(top, "#17121c", 0.94)
        s.poly(backwall, "#d09a58" if has else "#4a3a3c", 0.9 if has else 0.75)
        s.line([top[0], top[1]], "#f6dca6" if has else "#8a7460", 1.0, 0.7)             # the near rim
        if has:
            zc = (z0 + z1) / 2
            flames.append(lamp(s, g, side * (x0 + x1) / 2, R(zc) + BENCH - deep + 2.5, zc - 4, rng, tongue=tongues) + (F_ / zc,))
    for (lx, ly, lz, pw, kind) in LAMPS:
        if kind in ("floor", "ledge"):
            flames.append(lamp(s, g, lx, ly - 7.0, lz, rng, tongue=tongues) + (F_ / lz,))
    px0, py0 = PW(g, -HALF - 52.0, 108.0, ZB)                                        # a peg in the passage wall, and rope hung on it
    kk = F_ / ZB
    s.line([(px0 - 3, py0), (px0 + 3.5, py0 - 1)], "#3a3040", 2.0)
    for rr_ in (7.5, 5.6):
        s.line([(px0 + math.cos(a) * rr_ * kk, py0 + (9 + math.sin(a) * 12) * kk) for a in np.linspace(0, 6.3, 16)], "#4a4458", 2.0)
    bx0, by0 = PW(g, -HALF - 38.0, 0.0, ZB - 10.0)                                     # a basket standing inside
    s.poly([(bx0 - 9, by0), (bx0 + 9, by0), (bx0 + 11, by0 - 13), (bx0 - 11, by0 - 13)], "#4a4254")
    s.ellipse(bx0, by0 - 13, 11, 3.6, "#6c6a84")
    s.ellipse(bx0, by0 - 12.6, 8.5, 2.4, "#2c2838")
    for i in range(3):
        s.line([(bx0 - 10 + i * 0.4, by0 - 3.5 - i * 3.2), (bx0 + 10 - i * 0.4, by0 - 3.5 - i * 3.2)], "#2e2a3a", 0.9, 0.8)
    s.onto(pic)
    for (cx, cy, k) in flames:                                                           # the least bit of glow, right at the flame
        r = max(4.0, 17.0 * k)
        glow(pic, "#ffc070", mask_ellipse(SHAPE, cx + 6 * k, cy - 9 * k, r, r, soft=r * 0.55) * 0.7)
        if tongues:                                                                      # (and its white heart: part of the flame, so the game draws it now)
            glow(pic, "#fff2c0", mask_ellipse(SHAPE, cx + 6.5 * k, cy - 10 * k, r * 0.3, r * 0.36, soft=1.0) * 0.9)
    info["flames"] = flames
    return pic


JARS = [(-197.0, 636.0, 80.0, 36.0, "linen", 0.6), (-165.0, 638.0, 66.0, 31.0, "open", None), (-184.0, 613.0, 50.0, 26.0, "linen", None)]   # X, Z, height, width, top, sling
COIL = (136.0, 613.0)
RUNNER = ((131.0, 735.0), (131.0, 978.0))                    # along the right-hand bench


def things(pic, info, seed=5):
    """What people have left lying about: all of it off the floor where they walk."""
    g = info["g"]
    sid = g["sid"]
    rng = np.random.default_rng(seed + 200)
    pw = lambda X, Y, Z: PW(g, X, Y, Z)
    landing = (sid == K.LANDING).astype(F32)

    # ---- red marks on the right-hand wall, above the level bench
    T.marks(pic, pw, rng, z0=486.0, z1=640.0, level=150.0, amount=0.95)
    T.marks(pic, pw, np.random.default_rng(seed + 9), z0=700.0, z1=790.0, level=R(745.0) + 200.0, wall=-HALF, amount=0.45)   # and an older line on the other wall

    # ---- shadows first, on the floor: thrown away from the lamp that stands by the jars
    for (X, Z, hgt, wid, cap, band) in JARS:
        x, y, k = T.on_floor(pw, X, Z)
        T.shadow_on(pic, landing, x - wid * k * 0.55, y + 1, wid * k * 0.95, wid * k * 0.26, 0.62)
    x, y, k = T.on_floor(pw, *COIL)
    T.shadow_on(pic, landing, x - 6 * k, y + 2 * k, 30 * k, 9 * k, 0.6)

    s = Sheet(SHAPE)
    # ---- chips and dust swept to the foot of the walls and benches
    T.chips(s, pw, rng, [(-175.0, 640.0, 26.0, 2.5, 16), (150.0, 560.0, 3.0, 50.0, 18), (140.0, 640.0, 12.0, 2.5, 8), (-214.0, 440.0, 3.0, 14.0, 6),
                         (-150.0, 596.0, 30.0, 8.0, 7), (60.0, 641.0, 12.0, 2.0, 5), (-70.0, 641.0, 12.0, 2.0, 5)])
    # ---- the oil jars, the spare dishes, a little jug for filling
    for (X, Z, hgt, wid, cap, band) in sorted(JARS, key=lambda j: -j[1]):
        x, y, k = T.on_floor(pw, X, Z)
        T.profile_jar(s, x, y, hgt * k, wid * k, T.CLAY, cap=cap, band=band, light=1)
    x, y, k = T.on_floor(pw, -136.0, 634.0)
    T.dishes(s, x, y, k, n=5, light=1)
    x, y, k = T.on_floor(pw, -152.0, 617.0)
    T.profile_jar(s, x, y, 21 * k, 17 * k, T.CLAY, cap="open", light=1,
                  shape=[(0.0, 0.5), (0.1, 0.8), (0.4, 1.0), (0.66, 0.78), (0.8, 0.42), (0.9, 0.4), (1.0, 0.56)])
    # ---- a coil of rope by the level bench, its end trailing
    x, y, k = T.on_floor(pw, *COIL)
    T.coil(s, x, y, k, light=1, tail=[(x + 4 * k, y + 10 * k), (x - 20 * k, y + 17 * k), (x - 44 * k, y + 13 * k)], seed=seed)
    # ---- an old sledge runner laid along the right-hand bench, out of the way
    (ax, az), (bx, bz) = RUNNER
    T.timber(s, pw, (ax, R(az) + BENCH, az), (bx, R(bz) + BENCH, bz), 13.0, 11.0, nose=20.0)
    # ---- on the left bench: a mallet and a copper chisel, put down and forgotten
    mx, my = pw(-156.0, R(676.0) + BENCH, 676.0)
    k = F_ / 676.0
    club = [(-17, 1.4), (-2, 1.6), (4, 5.2), (15, 6.0), (18, 3.0), (18, -3.0), (15, -6.0), (4, -5.2), (-2, -1.6), (-17, -1.4)]      # a mason's mallet: one piece of wood, handle and bell
    turn = lambda pts, a: [(mx + (x * math.cos(a) - y * math.sin(a)) * k, my + (x * math.sin(a) + y * math.cos(a)) * k * 0.62) for x, y in pts]
    s.poly(turn(club, -0.35), "#6a4830")
    s.poly(turn([(-16, 0.2), (-2, 0.2), (4, 2.0), (15, 2.6), (15, -4.6), (4, -4.0), (-2, -1.0), (-16, -1.0)], -0.35), "#b98a56")
    s.line(turn([(5, -3.2), (14, -3.6)], -0.35), "#efc88c", 1.0, 0.9)
    s.line([(mx - 16 * k, my + 9 * k), (mx + 6 * k, my + 5.5 * k)], "#a85a2a", 1.7 * k)                                              # and a copper chisel
    s.line([(mx + 1 * k, my + 5.8 * k), (mx + 6 * k, my + 5.0 * k)], "#ffc880", 1.3 * k)
    # ---- on the level bench by the lamp: the boy's filling jug and a hank of wicks
    x, y, k = T.on_floor(pw, 168.0, 622.0, BENCH)
    T.profile_jar(s, x, y, 22 * k, 16 * k, T.CLAY, cap="open", light=-1,
                  shape=[(0.0, 0.5), (0.1, 0.8), (0.4, 1.0), (0.66, 0.78), (0.8, 0.42), (0.9, 0.4), (1.0, 0.56)])
    x, y, k = T.on_floor(pw, 204.0, 560.0, BENCH)
    for i in range(5):
        s.line([(x - 7 * k + i * 1.2, y - i * 0.9), (x + 7 * k + i * 1.2, y - 2 * k - i * 0.9)], T.LINEN["lit"] if i % 2 else T.LINEN["mid"], 1.3 * k)
    s.line([(x - 1 * k, y + 1.5 * k), (x + 1.5 * k, y - 4.5 * k)], "#4a3428", 1.2 * k)
    # ---- somebody's dinner, left on the left-hand bench beyond the lamp: beer jars, and bread in a basket
    for (X_, Z_, hgt, wid) in ((-186.0, 902.0, 34.0, 20.0), (-170.0, 884.0, 30.0, 19.0)):
        x, y = pw(*rr(X_, BENCH, Z_))
        k = F_ / Z_
        T.profile_jar(s, x, y, hgt * k, wid * k, T.CLAY, cap="open", light=-1)
    x, y = pw(*rr(-150.0, BENCH, 872.0))
    T.basket(s, x, y, F_ / 872.0, light=-1)
    # ---- higher up on the right: a chest for the king's house of eternity and two jars of fine white stone,
    #      set down by porters who would go no further
    zc = 1150.0
    T.chest(s, pw, 134.0, 182.0, zc, zc + 84.0, R(zc) + BENCH, 44.0)
    for (X_, Z_, hgt, wid) in ((150.0, 1262.0, 46.0, 21.0), (172.0, 1276.0, 40.0, 19.0)):
        x, y = pw(*rr(X_, BENCH, Z_))
        k = F_ / Z_
        T.profile_jar(s, x, y, hgt * k, wid * k, T.ALABASTER, cap="linen", light=1,
                      shape=[(0.0, 0.42), (0.1, 0.6), (0.5, 0.8), (0.8, 1.0), (0.9, 0.7), (1.0, 0.62)])
    # ---- a reed mat on the level bench, where the lamp boy sits
    T.mat(s, pw, 163.0, 216.0, 414.0, 508.0, BENCH + 0.6)
    # ---- chips along the foot of the benches, where the ramp has been swept
    for sgn in (-1, 1):
        for _ in range(26):
            z = Z1 + 20 + rng.random() ** 1.5 * 900
            x, y = pw(*rr(sgn * (RAMP - 2 - rng.random() * 7), 0.0, z))
            r = (0.6 + rng.random() * 1.4) * min(1.0, 700.0 / z)
            s.ellipse(x, y, r * 1.3, r * 0.7, "#f2dcae" if rng.random() < 0.5 else "#bfa074", 0.85)
    # ---- a hauling rope left along the left-hand bench
    pts = [pw(*rr(-128.0 - 7 * math.sin(i * 0.9) - (i > 13) * (i - 13) * 6.0, BENCH, 760.0 + i * 24.0)) for i in range(18)]
    s.line(pts, T.ROPE["shade"], 2.4)
    s.line([(x, y - 0.7) for x, y in pts], T.ROPE["mid"], 1.3, 0.95)
    sc, sa = s.done()
    sc = sc * (1 + (noise(SHAPE, 4, seed + 60, 2) - 0.5)[..., None] * 0.22)                 # unevenness, as paint has
    glowmap = np.clip(blur(info["direct"], 3) * 2.2 + blur(info["day"], 3) * 0.8 + 0.42, 0, 1.15)[..., None]
    over(pic, np.clip(sc * glowmap, 0, 1), sa)                                              # things are only as bright as the light where they stand

    # ---- dust in the air: a few bright motes where the lamps are, and in the daylight
    m = Sheet(SHAPE)
    for (cx, cy, k) in info.get("flames", []):
        for _ in range(int(4 + 14 * k)):
            a, d = rng.random() * 6.28, (8 + rng.random() ** 0.7 * 60) * k
            m.ellipse(cx + math.cos(a) * d, cy - 10 * k + math.sin(a) * d * 0.8, 0.55, 0.55, "#ffe2a0", 0.25 + 0.4 * rng.random())
    for _ in range(26):
        X, Y, Z = -HALF + rng.random() * 120, rng.random() * 120, ZA + rng.random() * (ZB - ZA)
        px_, py_ = pw(X, Y, Z)
        m.ellipse(px_, py_, 0.55, 0.55, "#dcecff", 0.2 + 0.35 * rng.random())
    m.onto(pic)
    gx_, gy_ = PW(g, -HALF + 30.0, 70.0, (ZA + ZB) / 2)
    glow(pic, "#9cc0ee", mask_ellipse(SHAPE, gx_, gy_, 62, 78, soft=26) * 0.07)                        # the least haze of daylight in the air there
    return pic


def wear(pic, info, seed=5):
    """What four-and-a-half thousand years have not yet done, but twenty years of building have: nicks along the
    joints, a crack or two, oil and soot, and a floor worn pale where people walk."""
    g = info["g"]
    sid, X, Y, Z, h = g["sid"], g["X"], g["Y"], g["Z"], g["h"]
    rng = np.random.default_rng(seed + 300)
    lit = np.clip(info["direct"] * 2.6 + info["day"] * 1.1, 0, 1)
    near = 1 - np.clip((Z - 900.0) / 700.0, 0, 1)
    line = info["line"]
    # nicks: where a joint is chipped it is wider and darker, and the chip's lower lip catches light
    nick = step(0.80, 0.90, noise(SHAPE, 5, seed + 50, 2)) * np.clip(blur(line, 0.8) * 2.2, 0, 1) * near
    tint(pic, "#4a3a3c", np.clip(nick * 0.85, 0, 1).astype(F32))
    over(pic, "#ffe6b4", (np.roll(nick, 1, axis=0) * (1 - nick) * lit * 0.5).astype(F32))
    # pitting and tool marks on the dressed faces, only where there is light to show them
    wallish = ((sid >= K.WALL_L) & (sid <= K.WALL_R + K.NCOR)) | np.isin(sid, (K.BFRONT_L, K.BFRONT_R, K.LEDGE_IN, K.STEP_F))
    pit = step(0.90, 0.97, noise(SHAPE, 2.4, seed + 51, 2)) * step(0.4, 0.7, noise(SHAPE, 50, seed + 55, 3)) * wallish * near * (0.25 + 0.75 * lit)
    tint(pic, "#7a625a", np.clip(pit * 0.45, 0, 1).astype(F32))
    # the floor: worn pale along the way people go, from the way in to the foot of the ramp
    floor = (sid == K.LANDING).astype(F32)
    way = mask_line(SHAPE, [PW(g, -205, 0, 545), PW(g, -110, 0, 560), PW(g, 20, 0, 590), PW(g, 86, 0, 644)], [44, 40, 34, 22], soft=9)
    way = np.maximum(way, mask_line(SHAPE, [PW(g, 20, 0, 590), PW(g, -84, 0, 644)], [30, 20], soft=8))
    way = way * (0.5 + 0.7 * noise(SHAPE, 26, seed + 52, 3)) * floor
    glow(pic, "#d8c8b0", np.clip(way * 0.10 * (0.4 + lit), 0, 1).astype(F32))
    dust = step(0.55, 0.9, noise(SHAPE, (60, 16), seed + 53, 3)) * floor * (1 - np.clip(way * 2, 0, 1))
    tint(pic, "#8a6e5c", np.clip(dust * 0.28, 0, 1).astype(F32))
    # spilled oil by the jars: a dark stain with a glint in it
    ox, oy = PW(g, -128.0, 0, 588.0)
    spill = mask_ellipse(SHAPE, ox, oy, 15, 4.6, soft=1.2, wobble=2.5, seed=seed + 54) * floor
    tint(pic, "#5a4032", np.clip(spill * 0.7, 0, 1).astype(F32))
    over(pic, "#ffd9a0", (mask_ellipse(SHAPE, ox + 3, oy - 0.6, 5, 1.0, soft=0.7) * spill * 0.55).astype(F32))
    # cracks: a few, in the big stones low on the walls
    s = Sheet(SHAPE)
    for (side, z, y0, run) in ((-1, 742.0, 150.0, 70.0), (1, 700.0, 160.0, 90.0), (1, 880.0, 235.0, 60.0), (-1, 560.0, 268.0, 55.0), (1, 452.0, 132.0, 60.0), (-1, 1010.0, 400.0, 70.0)):
        pts, zz, yy = [], z, y0
        for i in range(7):
            pts.append(PW(g, side * HALF, yy, zz))
            zz += rng.normal(6, 5)
            yy += run / 7 * (0.6 + 0.8 * rng.random())
        s.line(pts, "#3a2c30", 1.0, 0.7)
        s.line([(x + 1.0, y + 0.4) for x, y in pts[2:6]], "#f6dcae", 0.8, 0.35)
    s.onto(pic)
    return pic


def restate(pic, crisp, info):
    """After the brush: say the hard things again. Edges of stone come back sharp, and so does everything far
    up the gallery, where a brush mark is as big as a block."""
    g = info["g"]
    Z, sid = g["Z"], g["sid"]
    m = np.clip(blur(info["edge"], 1.0) * 2.4, 0, 1) * 0.8
    m = np.maximum(m, np.clip((Z - 950.0) / 500.0, 0, 1) * 0.72)
    m = np.maximum(m, np.isin(sid, (K.PASS_FAR, K.PASS_FLOOR, K.DOOR_IN, K.LOW_IN, K.MOUTH, K.STEP_F)) * 0.85)
    m = np.maximum(m, np.isin(sid, (K.BIN_L, K.BIN_R, K.TRENCH_L, K.TRENCH_R, K.BFRONT_L, K.BFRONT_R)) * 0.6)
    return lerp(pic, crisp, m[..., None].astype(F32))


def flames(pic, info):
    """Last of all, the flames themselves, small and sharp: white at the wick, yellow, an orange tip. (As approved:
    round four no longer paints them. A flame that never moves breaks the illusion; the game draws each one
    flickering, at the wick, from layout.json "fx".)"""
    s = Sheet(SHAPE)
    for (cx, cy, k) in info.get("flames", []):
        rx, ry = max(2.6, 10.5 * k), max(1.4, 4.4 * k)
        fx, fy = cx + rx * 0.62, cy - ry * 0.9
        fh = max(5.5, 17.0 * k)
        s.poly([(fx - fh * 0.30, fy + 0.6), (fx + fh * 0.30, fy + 0.6), (fx + fh * 0.16, fy - fh * 0.55), (fx - fh * 0.04, fy - fh)], "#f08a1c")
        s.poly([(fx - fh * 0.20, fy + 0.3), (fx + fh * 0.20, fy + 0.3), (fx + fh * 0.06, fy - fh * 0.74)], "#ffd45a")
        s.poly([(fx - fh * 0.11, fy), (fx + fh * 0.11, fy), (fx + 0.2, fy - fh * 0.46)], "#fff0a8")
    s.onto(pic)
    return pic


def grade(pic):
    """The last look over the whole picture: a little more depth in the darks and more color in the lights."""
    lum = (pic @ np.array([0.3, 0.55, 0.15], dtype=F32))[..., None]
    pic = lum + (pic - lum) * 1.22                                       # color
    pic = np.clip(pic, 0, 1)
    pic = pic + 0.10 * (pic - 0.42) * (1 - np.abs(2 * pic - 1))          # a gentle S: lights up, darks down
    return np.clip(pic, 0, 1).astype(F32)


MIRROR_FOOT = (197.0, 687.0)                                 # X, Z of the middle of the big slot
MIRROR_TOP = (9.0, K.Y_STEP, Z_END)                          # on the lip of the tall step, a little right of the middle


def cutouts(info, seed=5, tongues=False):
    """-> {name: (color, alpha)}: the two mirrors, each where the story will put it, and the front plane.
    (`tongues=True`: the front plane's lamp with its flame painted in, as approved.)"""
    g = info["g"]
    out = {}
    s = Sheet(SHAPE)
    fx, fy = PW(g, *rr(MIRROR_FOOT[0], BENCH - 4.0, MIRROR_FOOT[1]))
    T.car_mirror(s, (fx, fy), 1.0)
    out["mirror-foot"] = s.done()
    s = Sheet(SHAPE)
    T.hand_mirror(s, PW(g, *MIRROR_TOP), 1.0)
    out["mirror-top"] = s.done()
    s = Sheet(SHAPE)
    T.front_left(s, P)
    flame = T.front_right(s, P, lambda X, Y, Z: lamp(s, {"wob": (np.zeros(SHAPE, F32), np.zeros(SHAPE, F32))}, X, Y, Z, None, tongue=tongues))
    c, a = s.done()
    c = c * (1 + (noise(SHAPE, 4, seed + 70, 2) - 0.5)[..., None] * 0.2)
    out["front"] = (np.clip(c, 0, 1), a)
    out["front-flame"] = tuple(flame) + (F_ / 424.0,)                 # (where the front lamp is, as the slots' lamps are listed: x, y, size)
    return out


def fx_marks(info, cuts):
    """Round four: each lamp's flame, for the game to draw flickering (layout.json "fx"), in the engine's own terms
    (js/engine/effects.js). The painting keeps the lamplight on the stone, the warm glow round each flame and the
    flame's light in the oil; only the tongues (and their white hearts) are gone."""
    out = []
    lamps = [(f, False) for f in info.get("flames", [])] + [(cuts["front-flame"], True)]
    for i, ((cx, cy, k), front) in enumerate(lamps):
        rx, ry = max(2.6, 10.5 * k), max(1.4, 4.4 * k)
        fx, fy = cx + rx * 0.62, cy - ry * 0.9                       # the wick, at the lip of the dish
        fh = max(5.5, 17.0 * k)                                       # how tall the painted flame stood
        out.append({"type": "flame", "id": f"lamp-{i + 1}", "at": [round(fx, 1), round(fy, 1)], "base": "front" if front else int(round(cy)),
                    "size": round(fh, 1), "width": round(fh * 0.6, 1), "edge": "#f08a1c", "color": "#ffd45a", "glowOpacity": 0.12, "lean": round(-0.04 * fh, 1),
                    "svg": [int(round(cx + 6.5 * k)), int(round(cy - 10 * k))], "pxPerCm": round(float(k), 2),
                    "what": "an oil lamp's flame: a small tongue standing up from the wick at the dish's lip (orange outside, yellow, white at the wick). "
                            "'at' is the wick; 'svg' the point the scene's SVG flicker uses today. The painting keeps a warm glow round it already, "
                            "so the engine's own glow can be faint" + ("; this lamp is on the front plane (front.png): its flame is drawn over the cast" if front else "")})
    return out


def grained(picture, seed=7, amount=0.02):
    lum = (picture @ np.array([0.3, 0.55, 0.15], dtype=F32))[..., None]
    g = picture + (grain(picture, seed, amount) - picture) * np.clip(0.30 + 1.5 * lum, 0, 1)
    return np.clip(g, 0, 1)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02, keep=None, keep_alpha=None):
    """Grain, then the limited palette. (As in the example, but the grain is scaled to the light: in a picture
    this dark, full-strength grain would turn the shadows to snow.) `keep` (round four) is the picture as approved,
    with `keep_alpha` its mask if it is a cut-out: the palette is worked out from it exactly as before, every pixel
    where `picture` is the same keeps its old index, and only the changed places are reduced again."""
    g = grained(picture if keep is None else keep, seed, amount)
    a = alpha if keep is None else (alpha if keep_alpha is None else keep_alpha)
    sample_of = g if a is None else g[a > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    if keep is not None:
        changed = np.abs(picture - keep).max(axis=2) > 0.5 / 255
        idx = np.where(changed, to_palette(grained(picture, seed, amount), pal, speckle=speckle), idx)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def layout(info, cuts):
    """The numbers the game needs, taken from the picture as painted."""
    g = info["g"]
    pt = lambda X, Y, Z: [int(round(v)) for v in PW(g, X, Y, Z)]
    fl = lambda X, Z: pt(X, 0.0, Z)                                    # a place on the level floor
    rp = lambda X, Z: pt(*rr(X, 0.0, Z))                               # a place on the ramp
    top = Z_END - 14.0                                                 # as far up as feet can go: just short of the step

    def box(alpha, pad=2):
        ys, xs = np.nonzero(alpha > 0.5)
        return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 2 * pad, int(ys.max() - ys.min()) + 2 * pad]

    def rect(points, pad=3):
        xs, ys = [p[0] for p in points], [p[1] for p in points]
        return [min(xs) - pad, min(ys) - pad, max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad]

    gate = [pt(-HALF, 0, ZA), pt(-HALF, 0, ZB), pt(-HALF, K.GATE_H, ZB), pt(-HALF, K.GATE_H, ZA)]
    mouth = [pt(-TR, 0, ZM), pt(TR, 0, ZM), pt(TR, 100.0, ZM), pt(-TR, 100.0, ZM)]
    door = [pt(-K.DOOR_W, K.Y_STEP, Z_END), pt(K.DOOR_W, K.Y_STEP, Z_END), pt(K.DOOR_W, K.Y_STEP + K.DOOR_H, Z_WALL), pt(-K.DOOR_W, K.Y_STEP + K.DOOR_H, Z_WALL)]
    side, z0, z1, x0, x1 = SLOT_FOOT
    slot = [pt(*rr(x0, BENCH, z0)), pt(*rr(x1, BENCH, z0)), pt(*rr(x1, BENCH, z1)), pt(*rr(x0, BENCH, z1))]
    step = [pt(-RAMP, K.Y_STEP, Z_END), pt(RAMP, K.Y_STEP, Z_END), pt(RAMP, K.Y_STEP - 28.0, Z_END), pt(-RAMP, K.Y_STEP - 28.0, Z_END)]
    jars = [pt(-218, 0, 600), pt(-100, 0, 600), pt(-218, 86, 640), pt(-100, 86, 640)]
    red = [pt(HALF, 138, 486), pt(HALF, 225, 486), pt(HALF, 138, 640), pt(HALF, 225, 640)]
    mf, mt = box(cuts["mirror-foot"][1], 0), box(cuts["mirror-top"][1], 0)
    out = {
        "id": "egypt-gallery", "horizon": 50, "full": 580, "size": [W, H],
        "light": "oil lamps low on both sides (warm, from below); cool daylight from the opening in the left wall at the foot; the upper doorway faintly warm",
        "note": "People on the ramp are exactly the size the picture is drawn for. On the level floor at the foot (rows 500 to 600) the picture's own perspective is a little steeper, so a figure at the very bottom edge is about a tenth small for the stone round it: not noticeable.",
        "walk": [fl(-204, 462), fl(-204, 590), fl(-102, 590), rp(-106, Z1), rp(-110, top), rp(110, top), rp(108, Z1), fl(108, 592), fl(150, 592), fl(150, 462)],
        "blocked": [[rp(-TR - 5, Z1), rp(TR + 5, Z1), rp(TR + 5, ZM + 12), rp(-TR - 5, ZM + 12)]],
        "planes": [
            {"id": "front", "file": "front.png", "plane": "front"},
            {"id": "mirror-foot", "file": "mirror-foot.png", "base": rp(MIRROR_FOOT[0], MIRROR_FOOT[1])[1], "when": "egypt.footSet", "rect": mf},
            {"id": "mirror-top", "file": "mirror-top.png", "base": pt(*MIRROR_TOP)[1], "when": "egypt.topSet", "rect": mt}],
        "things": [
            {"id": "low-passage", "what": "the low dark mouth at the end of the cut in the ramp's foot: a level passage to another chamber", "shape": {"rect": rect(mouth)}, "stand": fl(0, 618), "face": "N"},
            {"id": "slot-foot", "what": "the first, big slot in the right-hand bench (mirror place 1)", "shape": {"rect": rect(slot, 5)}, "stand": rp(84, 690), "face": "E"},
            {"id": "step-top", "what": "the top of the tall step under the upper doorway (mirror place 2)", "shape": {"rect": rect(step, 2)}, "stand": rp(-16, top - 44), "face": "N"},
            {"id": "marks", "what": "builders' marks in red ochre on the right-hand wall: a levelling line, its triangle, tallies, a gang's sign", "shape": {"rect": rect(red)}, "stand": fl(112, 556), "face": "E"},
            {"id": "oil-jars", "what": "oil jars, spare lamp dishes and a lit lamp, on the floor against the left-hand bench", "shape": {"rect": rect(jars)}, "stand": fl(-96, 574), "face": "W"},
            {"id": "ladder", "what": "a ladder leaning in the near left corner (front plane)", "shape": {"rect": [92, 250, 66, 350]}, "stand": fl(-190, 500), "face": "W"},
            {"id": "sledge-runner", "what": "an old sledge runner laid along the right-hand bench", "shape": {"rect": rect([pt(*rr(128, BENCH, 735)), pt(*rr(150, BENCH + 30, 978))], 4)}, "stand": rp(96, 800), "face": "E"},
            {"id": "chest", "what": "a gold-banded chest on carrying poles and two jars of white stone, set down on the right-hand bench halfway up", "shape": {"rect": rect([pt(*rr(130, BENCH, 1100)), pt(*rr(190, BENCH + 60, 1290))], 3)}, "stand": rp(70, 1130), "face": "E"},
            {"id": "dinner", "what": "beer jars and a basket of bread left on the left-hand bench", "shape": {"rect": rect([pt(*rr(-196, BENCH, 860)), pt(*rr(-134, BENCH + 40, 910))], 3)}, "stand": rp(-80, 880), "face": "W"},
            {"id": "rope", "what": "a coil of rope on the floor by the level bench", "shape": {"rect": rect([fl(112, 600), fl(160, 628)], 6)}, "stand": fl(86, 578), "face": "E"}],
        "exits": [
            {"to": "egypt-site", "what": "the low passage that comes in from outside: the lit opening in the left wall", "shape": {"poly": gate}, "stand": fl(-176, 548), "face": "W"},
            {"to": "egypt-chamber", "id": "top-door", "what": "the small doorway above the tall step at the top of the ramp", "shape": {"rect": rect(door, 4)}, "stand": rp(0, top - 44), "face": "N"}],
        "marks": {"lampboy": [pt(K.LEDGE_X + 2, BENCH, 445)[0], pt(K.LEDGE_X + 2, BENCH, 445)[1] + 40], "dad-from-site": fl(-150, 548), "dad-from-chamber": rp(0, top - 60)},
        "marks-note": "lampboy: the foot point of a SITTING figure on the front edge of the level stone bench along the right wall (his seat is 40 px above it, on the reed mat; his legs hang down the face of the bench). Facing SW (toward the middle of the floor) looks right.",
        "beam": {"gate": [int((gate[0][0] + gate[1][0]) / 2), int((gate[1][1] + gate[2][1]) / 2)], "mirror-foot": [mf[0] + mf[2] // 3, mf[1] + mf[3] // 3],
                 "mirror-top": [mt[0] + mt[2] // 2 - 2, mt[1] + mt[3] // 3], "door": [400, int((door[0][1] + door[2][1]) / 2)]},
        "lamps": [[int(round(cx + 6.5 * k)), int(round(cy - 10 * k)), round(float(k), 2)] for (cx, cy, k) in info.get("flames", [])] + [[int(round(v)) for v in P(198.0 + 6, BENCH + 12, 424.0)] + [1.18]],
        "lamps-note": "x, y of each flame and its size (pixels per cm there), for the game's flicker; the last is on the front plane.",
        "fx": fx_marks(info, cuts),
        "notes": ["round four: no flame is painted still any more. The tongues of all eight lamps, and the white heart of each, are gone (back.png and front.png); "
                  "the lamplight on the stone, the warm glow round each flame and the flame's light in the oil are as they were. 'fx' gives each flame's wick ('at'), its height ('size'), and its depth; "
                  "'svg' is the point the scene's SVG flicker uses today (the same as 'lamps')"],
    }
    return out


def tidy(d):
    """JSON with one short entry to a line, so the numbers can be read."""
    lines = []
    for k, v in d.items():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            inner = ",\n".join("    " + json.dumps(e) for e in v)
            lines.append(f"  {json.dumps(k)}: [\n{inner}\n  ]")
        else:
            lines.append(f"  {json.dumps(k)}: {json.dumps(v)}")
    return "{\n" + ",\n".join(lines) + "\n}\n"


F_ = K.F


def show(pic, name):
    Image.fromarray((np.clip(pic, 0, 1) * 255).astype(np.uint8)).save(name)


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = "fast" in sys.argv
    ss = 1 if fast else 2
    if "ss2" in sys.argv:
        ss = 2
    base, info = under(ss=ss)
    show(base, OUT + "-1-under.png")
    print("under", round(time.time() - t0, 1))
    gx, gy = grid(SHAPE)
    along = np.arctan2(gy - K.VY, gx - K.VX).astype(F32)                 # brush marks run with the courses, toward the place the gallery runs to
    pic = base.copy() if fast else strokes(base, sizes=(9, 5, 2), seed=2, density=1.6, jitter=0.042, keep=0.32, flow=along)
    pic = restate(pic, base, info)
    approved = pic.copy()                                                # as approved: the flames painted in still (for the palettes)
    stonework(approved, info, tongues=True)
    wear(approved, info)
    things(approved, info)
    approved = grade(approved)
    flames(approved, info)
    stonework(pic, info)                                                 # round four: no flame is painted; the game draws them moving
    wear(pic, info)
    things(pic, info)
    pic = grade(pic)
    cuts = cutouts(info)
    cuts0 = cutouts(info, tongues=True)
    whole = pic.copy()
    for name in ("mirror-foot", "mirror-top", "front"):
        over(whole, cuts[name][0], (cuts[name][1] > 0.5).astype(F32))
    show(pic, OUT + "-2-back.png")
    show(whole, OUT + "-2-all.png")
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    print("back", finish(pic, OUT + "/back.png", 160, speckle=0.008, keep=approved))
    print("front", finish(cuts["front"][0], OUT + "/front.png", 64, cuts["front"][1], keep=cuts0["front"][0], keep_alpha=cuts0["front"][1]))
    print("mirror-foot", finish(cuts["mirror-foot"][0], OUT + "/mirror-foot.png", 40, cuts["mirror-foot"][1], speckle=0.006, amount=0.008))
    print("mirror-top", finish(cuts["mirror-top"][0], OUT + "/mirror-top.png", 32, cuts["mirror-top"][1], speckle=0.006, amount=0.008))
    with open(OUT + "/layout.json", "w") as f:
        f.write(tidy(layout(info, cuts)))
    print("done", round(time.time() - t0, 1))

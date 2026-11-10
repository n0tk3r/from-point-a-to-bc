"""PAINT-23: the MIDDLE plane of the foot of Mount Shosha (edo-shosha), in either light (edo_shosha_kit.LIGHT): the
woods at the mountain's foot rising behind the terrace (pines, maples in new leaf, the late cherry in their shade), the
east path's worn steps climbing into them, the terrace's ground and the road (through the camera), O-Ume's hut, the
women's hall, every shadow, and the cut-outs that stand in the play (the doors, the lock, the rice ball, the stone, the
bench).

Everything is measured in centimetres and drawn through the scene's one camera (edo_shosha_kit.P), each face a graded
wash (Wet), lit by how squarely it takes the light's sun (kit.faced), shadows laid as cool glazes. The research is round
twenty-one's (edo_shosha_kit's header): nothing here reads as a cross (the jewel on the roof sits in a lotus cup, with
nothing standing out sideways; the stone's marks are short strokes, dots and hooks, none crossing another)."""

import math

import numpy as np

from brush import F32, Sheet, blur, curve, grid, lerp, mask_line, mask_poly, mask_ellipse, noise, over, sample, step, tint, warp, glow
import depth as DEPTH
import edo_shosha_kit as K
from edo_shosha_kit import *

X_, Y_ = grid(SHAPE)
LUM = np.array([0.30, 0.55, 0.15], F32)

# ---------------------------------------------------------------- local colours (as the paint is mixed: the light is laid by kit.faced)
WOOD = thin(mixp(mixp(OCHRE, SIENNA, 0.38), PRUSSIAN, 0.16), 0.26)     # the hall's old boards, unpainted, weathered: warm grey-brown
TIMBER = mixp(mixp(SIENNA, PRUSSIAN, 0.40), OCHRE, 0.12)  # posts, beams: darker, oiled by hands
TILE = thin(mixp(PRUSSIAN, COBALT, 0.22), 0.42)           # grey roof tiles
STONE_C = thin(mixp(PRUSSIAN, OCHRE, 0.22), 0.55)         # dressed granite, weathered
PLASTER = thin(mixp(OCHRE, NAPLES, 0.35), 0.62)           # mud plaster
THATCH = thin(mixp(OCHRE, SIENNA, 0.30), 0.30)
EARTH = thin(mixp(OCHRE, SIENNA, 0.22), 0.42)             # the terrace: packed earth and fine gravel
EARTH_NEAR = thin(mixp(OCHRE, SIENNA, 0.34), 0.22)
GRASS = thin(mixp(VERONESE, OCHRE, 0.25), 0.28)
MOSS = thin(mixp(VIRIDIAN, OCHRE, 0.30), 0.22)
PINE = mixp(VIRIDIAN, PRUSSIAN, 0.40)
PINE_LIT = thin(mixp(VIRIDIAN, OCHRE, 0.40), 0.10)
MAPLE = thin(mixp(VERONESE, NAPLES, 0.28), 0.12)          # new leaf: yellow-green, thin, luminous
MAPLE_DEEP = mixp(mixp(VERONESE, VIRIDIAN, 0.55), PRUSSIAN, 0.10)
BARK = mixp(SIENNA, PRUSSIAN, 0.38)                       # red pine bark
BARK_LIT = thin(mixp(SIENNA, ORANGE, 0.35), 0.18)
CHERRY_C = thin(LAKE, 0.70)
PAPER_SLIP = WPAPER
PAPER_OLD = thin(mixp(OCHRE, NAPLES, 0.5), 0.62)
INK = PRUSSIAN


def smoothstep_(a, b, x):
    q = np.clip((x - a) / (b - a), 0, 1)
    return (q * q * (3 - 2 * q)).astype(F32)


def light_k():
    """1 in the gold light, 0 at sunset (for what changes with the hour)."""
    return 1.0 if K.LIGHT == "gold" else 0.0


# ================================================================ the woods at the mountain's foot
# The bank behind the terrace rises steeply; its trees stand on it. Their crowns' skyline against the shoulder beyond
# (picture points, left to right), and the trees themselves: (X, D, kind, height cm, crown radius cm).
SKYLINE = [(0.0, 64.0), (90.0, 56.0), (170.0, 78.0), (250.0, 66.0), (320.0, 84.0), (380.0, 100.0), (430.0, 118.0), (480.0, 140.0),
           (516.0, 168.0), (546.0, 206.0), (572.0, 250.0), (592.0, 292.0), (606.0, 334.0)]
BANK_FOOT = [(-2200.0, 2050.0), (-1100.0, 2010.0), (-800.0, 1960.0), (-600.0, 1930.0), (-500.0, 1800.0), (-455.0, 1500.0), (-420.0, 1340.0),
             (-250.0, 1420.0), (-60.0, 1900.0), (300.0, 2560.0), (620.0, 2500.0), (900.0, 2300.0)]
BANK_SLOPE = 0.75                                          # the bank climbs 75 cm in every metre
BANK_TOP = 560.0                                           # to a shelf 5.6 m up, the woods on it; the main slope rises far beyond
TREES = [
    # pines (red pine: tall, straight, its crown high up in flat pads)
    (-1350.0, 2700.0, "pine", 1900.0, 300.0), (-820.0, 2560.0, "pine", 2100.0, 330.0), (-400.0, 2380.0, "pine", 1800.0, 280.0),
    (-120.0, 2950.0, "pine", 2200.0, 320.0), (260.0, 3200.0, "pine", 2000.0, 300.0), (520.0, 3050.0, "pine", 1700.0, 260.0),
    (-1700.0, 3300.0, "pine", 2000.0, 280.0), (60.0, 3700.0, "pine", 2100.0, 300.0),
    # maples in new leaf, lower, broad
    (-1050.0, 2300.0, "maple", 820.0, 300.0), (-620.0, 2200.0, "maple", 760.0, 280.0), (-260.0, 2420.0, "maple", 900.0, 330.0),
    (60.0, 2700.0, "maple", 880.0, 320.0), (380.0, 2850.0, "maple", 820.0, 300.0), (-1500.0, 2450.0, "maple", 700.0, 260.0),
    (620.0, 2650.0, "maple", 640.0, 240.0),
]


def woods_edge():
    """The right-hand edge of the mountain's side (its woods and its bank): the spur's line, then down behind the hall's
    south-east corner (the plain opens from the hall's wall)."""
    import edo_shosha_far as FAR
    return [p for p in FAR.SPUR if p[1] < 300] + [(624.0, 300.0), (612.0, 330.0), (608.0, 610.0)]


def bank_back(X):
    xs = [p[0] for p in BANK_FOOT]
    ds = [p[1] for p in BANK_FOOT]
    return float(np.interp(X, xs, ds))


def ground_y(X, D):
    """The ground's height at a place: the terrace is level; the bank behind it climbs to the shelf."""
    return min(BANK_TOP, BANK_SLOPE * max(0.0, D - bank_back(X)))


def bank_mask():
    """Where the picture shows the bank (the ground behind the terrace, rising), below the woods' skyline: for each pixel
    whose ray meets the bank before the terrace. -> (mask, the bank's depth there)."""
    out = np.zeros(SHAPE, F32)
    dep = np.zeros(SHAPE, F32)
    for xi in range(W):
        x = xi + 0.5
        # march each row's ray: find the first D where the ray is under the ground
        for yi in range(0, 420):
            y = yi + 0.5
            k = (HZ - y) / F                               # the ray rises k cm per cm of depth (falls if negative)
            # solve EYE + k D = slope (D - back(X(D))): try depths
            hit = None
            for Dd in (900.0, 1200.0, 1500.0, 1800.0, 2100.0, 2400.0, 2700.0, 3000.0, 3400.0, 3800.0, 4300.0, 4900.0, 5600.0, 6400.0, 7300.0, 8400.0):
                Xd = (x - CX) * Dd / F
                if EYE + k * Dd <= ground_y(Xd, Dd):
                    hit = Dd
                    break
            if hit is not None and EYE + k * hit > 0.5:
                out[yi, xi] = 1.0
                dep[yi, xi] = hit
    return out, dep


def bank_mask_fast():
    """Where the picture shows the bank (the ground rising behind the terrace to the shelf), on the mountain's side only
    (left of the spur: at the right the land falls away to the plain). -> (mask, the bank's depth there)."""
    import edo_shosha_far as FAR
    Ds = np.geomspace(800.0, 9000.0, 170).astype(F32)
    xs = (np.arange(W, dtype=F32) + 0.5)
    ys = (np.arange(H, dtype=F32) + 0.5)
    out = np.zeros(SHAPE, F32)
    dep = np.full(SHAPE, 1e6, F32)
    backs = np.array([[bank_back((x - CX) * Dd / F) for x in xs] for Dd in Ds], F32)
    for i, Dd in enumerate(Ds):
        gy = np.minimum(BANK_TOP, BANK_SLOPE * np.maximum(0.0, Dd - backs[i]))
        ray = EYE + (HZ - ys[:, None]) / F * Dd
        under = (ray <= gy[None, :]) & (gy[None, :] > 0.5) & (ray > 0.5) & (dep > 1e5)
        dep[under] = Dd
        out[under] = 1.0
    side, _ = FAR.left_of(woods_edge(), soft=1.0)
    out = out * side
    return out.astype(F32), dep


def woods(pic, info):
    """The bank and its woods, far to near. The bank: the forest floor rising from the terrace's back to the shelf, in the
    trees' shade (dead leaves, ferns, young growth), a fleck of sun here and there. On it and on the shelf behind it, the
    trees: tall red pines (their trunks lit on the sun's side, their crowns high up in flat pads against the far slope),
    maples in new leaf (luminous yellow-green masses, broken, with gaps), the late cherry in their shade. Behind them
    the far slope (edo_shosha_far): seen in the gaps. -> masks."""
    rng = np.random.default_rng(71)
    bank, bdep = info["bank"], info["bank_d"]
    gold = light_k()
    # the shelf's woods behind the bank: a canopy of small crowns up to its ragged skyline against the far slope (it falls
    # away at the right toward the spur's foot), lit on top, deeper below, a breath of the air in its upper parts
    sky_m, sky_y = left_skyline()
    import edo_shosha_far as FAR_
    side, _ = FAR_.left_of(woods_edge(), soft=1.0)
    can = sky_m * side * (Y_ < 420)
    dark_c = shaded(mixp(PINE, MAPLE_DEEP, 0.35), 0.75 if gold else 1.0)
    lit_c = faced(mixp(MAPLE_DEEP, MAPLE, 0.45), 0.85 if gold else 0.1)
    body = FAR_.crowns(can, 81, 12.0, dark_c, lit_c, 0.55)
    body2 = FAR_.crowns(can, 82, 6.0, dark_c, lit_c, 0.45)
    body = lerp(body, body2, 0.4)
    depth_up = np.clip((sky_y[None, :] + 140 - Y_) / 140.0, 0, 1)
    body = lerp(body, K.horizon_c()[None, None, :], (depth_up * 0.22)[..., None])
    body = lerp(body, shaded(PINE, 1.0)[None, None, :], (np.clip((Y_ - 160) / 160.0, 0, 1) * 0.45)[..., None])     # deeper toward the bank
    over(pic, body.astype(F32), can.astype(F32))
    info["canopy"] = can.astype(F32)
    # the bank: the woods' floor in their shade, as deep as the canopy's foot at its top (they are one darkness), lighter
    # and warmer toward its foot where the terrace's light reaches in: ferns, young azaleas, dead leaves
    yb = np.where(bank > 0.5, Y_, 0).max(axis=0).astype(F32)                      # the bank's foot row in each column
    yt = np.where(bank > 0.5, Y_, 9999).min(axis=0).astype(F32)
    u = np.clip((Y_ - yt[None, :]) / np.maximum(yb - yt, 1)[None, :], 0, 1)     # 0 at its top, 1 at its foot
    floor_top = shaded(mixp(PINE, MAPLE_DEEP, 0.35), 1.0)
    floor_foot = shaded(mixp(mixp(SIENNA, OCHRE, 0.35), VIRIDIAN, 0.40), 0.70 if gold else 0.95)
    fl = lerp(floor_top[None, None, :], floor_foot[None, None, :], (u ** 1.6)[..., None])
    n = blur(noise(SHAPE, (22, 10), 74, 3), 1.0)
    fl = fl * (1 + (n - 0.5)[..., None] * 0.20)
    under_ = smoothstep_(0.48, 0.74, blur(noise(SHAPE, (14, 8), 78, 3), 1.0)) * (u > 0.25)
    fl = lerp(fl, faced(mixp(VERONESE, VIRIDIAN, 0.55), 0.35 if gold else 0.0), (under_ * u * 0.55)[..., None])
    over(pic, np.clip(fl, 0, 1), bank)
    if gold:
        fleck = smoothstep_(0.72, 0.80, blur(noise(SHAPE, (14, 5), 75, 3), 1.0)) * bank * (u > 0.5)
        over(pic, sunlit(mixp(MOSS, NAPLES, 0.4), 0.7), (fleck * 0.40).astype(F32))
    # ferns at the bank's foot, where the light comes in
    S = Wet(SHAPE)
    rng_s = np.random.default_rng(79)
    for x in np.arange(0.0, 640.0, 9.0):
        y = float(yb[int(x)])
        if y < 300 or bank[int(y), int(x)] < 0.5:
            continue
        for q in range(2):
            x0 = x + rng_s.uniform(-4, 4)
            ln = rng_s.uniform(7, 15)
            ang = -math.pi / 2 + rng_s.uniform(-0.9, 0.9)
            c = faced(mixp(VERONESE, VIRIDIAN, 0.45), 0.6 if gold else 0.0)
            S.line(curve([(x0, y + 1), (x0 + math.cos(ang) * ln * 0.5, y + math.sin(ang) * ln * 0.6), (x0 + math.cos(ang) * ln, y + math.sin(ang) * ln * 0.8 + 2)], 4), c, 1.2, 0.8)
    c_, a_ = S.done()
    over(pic, c_, a_)
    info["woods"] = bank
    # the trees, far to near
    L = Wet(SHAPE)
    for (Xt, Dt, kind, ht, cr) in sorted(TREES, key=lambda t_: -t_[1]):
        base = ground_y(Xt, Dt)
        rng_t = np.random.default_rng(int(abs(Xt * 7 + Dt)))                    # each tree its own chance: one mended moves no other
        if kind == "pine":
            pine_tree(L, Xt, Dt, base, ht, cr, rng_t)
        else:
            maple_tree(L, Xt, Dt, base, ht, cr, rng_t)
        if (Xt, Dt) == (-620.0, 2200.0):
            cherry_tree(L, rng)
    c, a = L.done()
    side, _ = __import__("edo_shosha_far").left_of(woods_edge(), soft=1.0)
    a = a * np.maximum(side, np.clip((236.0 - Y_) / 14.0, 0, 1))             # (high up their crowns may stand against the sky)
    over(pic, c, a)
    info["trees"] = a
    info["woods"] = np.clip(bank + a, 0, 1)
    return info


def left_skyline():
    """The woods' skyline against the shoulder: a mask of everything below it (left of x 640), ragged with crowns."""
    xs = [p[0] for p in SKYLINE]
    ys = [p[1] for p in SKYLINE]
    line = np.interp(np.arange(W), xs, ys).astype(F32)
    line += (noise((1, W * 4), (26, 1), 76, 3)[0, :W] - 0.5) * 18
    line += (noise((1, W * 4), (7, 1), 77, 2)[0, :W] - 0.5) * 7
    m = np.clip(Y_ - line[None, :] + 0.5, 0, 1) * (X_ < 640)
    return m.astype(F32), line


def pine_tree(L, X, D, base, ht, cr, rng):
    """A red pine on the bank: a tall trunk, never quite straight, its bark warm and red up high and lit on the sun's
    side; its crown high up in flat pads of needles on crooked limbs, each pad's top lit, its fringe all needle ends."""
    k = F / D
    A = lambda c: aired(c, D, start=2500.0, scale=26000.0)
    lean = rng.uniform(-0.07, 0.07)
    pts = []
    for i in range(14):
        h = ht * i / 13
        pts.append(P(X + lean * h + 22 * math.sin(h / 300.0 + X), base + h, D))
    w0 = 44.0 * k
    L.taper(pts, A(shaded(BARK, 0.45)), w0, w0 * 0.5)
    L.taper([(p[0] - w0 * (0.30 - 0.14 * i / 13), p[1]) for i, p in enumerate(pts)], A(faced(BARK_LIT, 0.85 if light_k() else 0.95)), w0 * 0.30, w0 * 0.16, alpha=0.85)
    for j in range(9):
        h = ht * (0.50 + 0.47 * (j / 8) ** 0.8) + rng.uniform(-40, 40)
        side = -1 if j % 2 else 1
        reach = cr * rng.uniform(0.45, 1.0) * (1.1 - 0.4 * j / 8)
        root = P(X + lean * h, base + h - 30, D)
        tip = P(X + lean * h + side * reach, base + h + rng.uniform(-30, 50), D)
        m1 = (root[0] + (tip[0] - root[0]) * 0.35 + rng.normal(0, 2.0), root[1] + (tip[1] - root[1]) * 0.35 - rng.uniform(2.0, 6.0))
        m2 = (root[0] + (tip[0] - root[0]) * 0.70 + rng.normal(0, 2.0), root[1] + (tip[1] - root[1]) * 0.70 + rng.uniform(-4.0, 2.0))
        L.taper(curve([root, m1, m2, tip], 4), A(shaded(BARK, 0.65)), max(1.2, 10 * k), max(0.7, 3 * k))      # crooked, as a pine's limb is
        rx, ry = reach * k * 0.85 + 4, reach * k * 0.24 + 2
        cx_, cy_ = tip[0] - side * rx * 0.25, tip[1] - ry * 0.3
        # the pad: not one saucer but a few clumps of needles along the limb's end, each its own small flat cloud, its
        # top lit in dabs, its fringe beneath all needle ends; the tips droop a little
        n_cl = max(2, int(round(rx / 8.0)))
        for c_i in range(n_cl):
            u = ((c_i + 0.5) / n_cl) * 2 - 1
            ccx = cx_ + u * rx * 0.72 + rng.normal(0, rx * 0.05)
            ccy = cy_ + ry * (0.22 * abs(u) + rng.normal(0, 0.12))
            crx = rx / n_cl * 1.35 * rng.uniform(0.85, 1.2)
            cry = ry * rng.uniform(0.70, 0.95) * (1 - 0.22 * abs(u))
            pad_ = []
            ph = rng.uniform(0, 6.3)
            for q in range(16):
                a_ = 2 * math.pi * q / 16
                rr = 1.0 + 0.16 * math.sin(3 * a_ + ph) + rng.uniform(-0.14, 0.14)
                pad_.append((ccx + math.cos(a_) * crx * rr, ccy + math.sin(a_) * cry * rr))
            L.poly(pad_, A(shaded(PINE, 0.55 if light_k() else 0.9)), A(shaded(PINE, 0.95)), g=((ccx, ccy - cry), (ccx, ccy + cry)))
            for q in range(int(crx * 1.3)):                                      # the fringe of needle ends, down and out
                v = rng.uniform(-1, 1)
                ex, ey = ccx + v * crx * 0.95, ccy + cry * (0.6 + 0.25 * rng.random()) * math.sqrt(max(0.0, 1 - v * v))
                L.line([(ex, ey - 1), (ex + rng.uniform(-1.5, 1.5), ey + rng.uniform(1.2, 3.0))], A(shaded(PINE, 0.8)), 0.8, 0.85)
            for q in range(int(2 + crx / 6)):                                    # the light on its top in dabs
                v = rng.uniform(-0.85, 0.45)
                L.ellipse(ccx + v * crx, ccy - cry * (0.25 + 0.3 * rng.random()) * math.sqrt(max(0.0, 1 - v * v)), crx * rng.uniform(0.22, 0.36),
                          cry * rng.uniform(0.28, 0.42), A(faced(PINE_LIT, 0.75 if light_k() else 0.15)), alpha=0.8)
            for q in range(int(crx * 0.7)):                                      # needle tufts along its lit top
                v = rng.uniform(-0.85, 0.5)
                ex, ey = ccx + v * crx, ccy - cry * 0.8 * math.sqrt(max(0.0, 1 - v * v))
                L.line([(ex, ey + 1), (ex + rng.uniform(-2, 1), ey - rng.uniform(1.2, 2.6))], A(faced(PINE_LIT, 0.9 if light_k() else 0.1)), 0.8, 0.7)


def spray(L, rng, cx, cy, r, lit_c, mid_c, dark_c, A, dab=1.6):
    """One spray of leaves, as a brush dabs it: a pale wash for its shape (loose, toothed), then small dabs of leaf in
    three tones, the lit ones on its upper side, the dark ones underneath where the next spray's shade lies; gaps left
    between the dabs at its edge."""
    pts = []
    n = 16
    ph = rng.uniform(0, 6.3)
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * (1.0 + 0.22 * math.sin(3 * a + ph) + rng.uniform(-0.18, 0.18))
        pts.append((cx + math.cos(a) * rr * 1.25, cy + math.sin(a) * rr * 0.55))
    L.poly(pts, A(lerp(lit_c, mid_c, 0.35)), A(mid_c), g=((cx, cy - r * 0.55), (cx, cy + r * 0.55)), alpha=0.75)
    nd = int(10 + r * r * 0.35)
    for q in range(nd):
        a = rng.uniform(0, 2 * math.pi)
        rr = math.sqrt(rng.random())
        dx, dy = math.cos(a) * rr * r * 1.2, math.sin(a) * rr * r * 0.55
        up = -dy / max(r * 0.55, 1)                                          # 1 at its top, -1 under it
        c = lit_c if up > 0.15 and rng.random() < 0.75 else (dark_c if up < -0.35 and rng.random() < 0.6 else mid_c)
        s_ = dab * rng.uniform(0.7, 1.3)
        L.ellipse(cx + dx, cy + dy, s_ * 1.2, s_ * 0.8, A(c), alpha=0.9)


def maple_tree(L, X, D, base, ht, cr, rng):
    """A maple in new leaf: a short crooked grey trunk and its limbs, and a broad crown in tiers of leafy sprays, thin
    and luminous, gaps between the sprays where the woods show through."""
    k = F / D
    A = lambda c: aired(c, D, start=2500.0, scale=26000.0)
    trunk_c = A(shaded(mixp(PRUSSIAN, OCHRE, 0.30), 0.45))
    trunk = [P(X, base, D), P(X + 18, base + ht * 0.28, D), P(X - 14, base + ht * 0.50, D), P(X + 6, base + ht * 0.62, D)]
    L.taper(curve(trunk, 5), trunk_c, 24 * k, 10 * k)
    tips = []
    for (dx, dh) in ((-cr * 0.8, ht * 0.66), (cr * 0.85, ht * 0.62), (-cr * 0.3, ht * 0.86), (cr * 0.4, ht * 0.84), (cr * 0.05, ht * 0.96)):
        tip = P(X + dx, base + dh, D)
        L.line(curve([P(X, base + ht * 0.48, D), P(X + dx * 0.5, base + dh * 0.86, D), tip], 4), trunk_c, max(0.7, 5 * k), 0.9)
        tips.append((X + dx, base + dh))
    gold = light_k()
    lit_c = faced(MAPLE, 0.95 if gold else 0.08)
    mid_c = faced(mixp(MAPLE, MAPLE_DEEP, 0.40), 0.55 if gold else 0.0)
    dark_c = shaded(MAPLE_DEEP, 0.50 if gold else 0.95)
    for j in range(14):                                                      # the sprays, in tiers, lower first
        tx, th_ = tips[j % len(tips)]
        cx_, cy_ = P(tx + rng.normal(0, cr * 0.28), th_ + rng.normal(0, 60) - 30, D)
        r = cr * k * rng.uniform(0.20, 0.30)
        spray(L, rng, cx_, cy_, r, lit_c, mid_c, dark_c, A, dab=max(1.0, 1.9 * k * 100 / 3.0 * 0.06 + 0.9))


CHERRY_CLOUDS = ((-130, 360, 110), (10, 420, 140), (170, 400, 105), (-40, 330, 90), (90, 470, 95), (-90, 440, 80))   # (across, up, size) cm


def cherry_box():
    """The late cherry's blossom in the picture: (left, top, right, bottom), for its area and the petals."""
    X, D = CHERRY
    base = ground_y(X, D)
    k = F / D
    xs, ys = [], []
    for (dx, dy, r_) in CHERRY_CLOUDS:
        cx_, cy_ = P(X + dx, base + dy, D)
        xs += [cx_ - r_ * k * 1.05, cx_ + r_ * k * 1.05]
        ys += [cy_ - r_ * k * 0.55, cy_ + r_ * k * 0.55]
    return min(xs), min(ys), max(xs), max(ys)


def cherry_tree(L, rng):
    """The late cherry in the shade of the woods, by the path: a dark leaning trunk and a few soft clouds of pale pink
    (geranium lake thinned nearly to the paper), cooler where the shade lies on it, the blossom thin and broken."""
    X, D = CHERRY
    base = ground_y(X, D)
    k = F / D
    trunk_c = shaded(mixp(PRUSSIAN, SIENNA, 0.45), 0.5)
    tr = [P(X, base, D), P(X + 30, base + 140, D), P(X + 4, base + 300, D), P(X + 50, base + 400, D)]
    L.taper(curve(tr, 5), trunk_c, 24 * k, 11 * k)
    L.line(curve([P(X + 14, base + 250, D), P(X - 80, base + 330, D), P(X - 150, base + 350, D)], 4), trunk_c, 7 * k, 0.9)
    L.line(curve([P(X + 30, base + 330, D), P(X + 130, base + 390, D), P(X + 200, base + 380, D)], 4), trunk_c, 6 * k, 0.9)
    gold = light_k()
    pink = shaded(CHERRY_C, 0.22 if gold else 0.55)
    pink_lit = faced(thin(CHERRY_C, 0.40), 0.45 if gold else 0.0)
    pink_d = shaded(thin(mixp(LAKE, COBALT, 0.25), 0.45), 0.30 if gold else 0.7)
    for (dx, dy, r) in CHERRY_CLOUDS:
        for q in range(3):
            cx_, cy_ = P(X + dx + rng.normal(0, r * 0.35), base + dy + rng.normal(0, r * 0.22), D)
            rr = r * k * rng.uniform(0.45, 0.65)
            spray(L, rng, cx_, cy_, rr, pink_lit, pink, pink_d, lambda c: c, dab=1.4)


# ================================================================ the path
def path_steps():
    """The east path's steps, bottom first: each tread (four places), its level, and its riser's level below it. The
    steps are worn, set by hand: each a little askew, its edges rounded."""
    rng = np.random.default_rng(81)
    out = []
    s = 0.0
    y = 0.0
    for i in range(PATH_N):
        tr = PATH_TREAD * rng.uniform(0.85, 1.15)
        rise = PATH_RISE * rng.uniform(0.85, 1.12)
        skew = rng.uniform(-6, 6)
        w = PATH_W * rng.uniform(0.94, 1.04)
        a = path_at(s + skew, -w / 2)
        b = path_at(s - skew, w / 2)
        c_ = path_at(s + tr - skew * 0.5, w / 2)
        d_ = path_at(s + tr + skew * 0.5, -w / 2)
        out.append(dict(front=(a, b), tread=[a, b, c_, d_], y0=y, y1=y + rise, s=s))
        s += tr
        y += rise
    return out


def path(pic, info):
    """The east path: worn stone steps climbing from the terrace into the woods, each slab uneven and rounded at its
    edges, moss in its joints and at its ends, its riser in shade; the woods' shade closing over it as it climbs; ferns
    and young azaleas crowding its sides; past the stone and up behind the hall's roof, out of sight."""
    L = Wet(SHAPE)
    rng = np.random.default_rng(82)
    steps = path_steps()
    t_tread = face_t((0, 1, 0))
    t_riser = face_t((-PATH_DIR[0], 0, -PATH_DIR[1]))
    stone_ = mixp(STONE_C, mixp(OCHRE, PRUSSIAN, 0.5), 0.35)
    for i, st in enumerate(steps[::-1]):
        (a, b), y0, y1 = st["front"], st["y0"], st["y1"]
        dim = float(np.clip((st["s"] - 90.0) / 240.0, 0, 1)) * 0.85 + 0.08
        D = st["tread"][0][1]
        kk = F / D
        q_ = st["tread"]
        # the slab's outline, its corners worn round
        def rp(p, yy, j):
            return P(p[0] + rng.normal(0, 3), yy + rng.normal(0, 0.8), p[1] + rng.normal(0, 3))
        tread = [rp(q_[0], y1, 0), P(*(lambda p: (p[0], y1 + 0.8, p[1]))((q_[0][0] * 0.5 + q_[1][0] * 0.5, 0, q_[0][1] * 0.5 + q_[1][1] * 0.5))[::2][:1], y1 + 0.8,
                                     (q_[0][1] * 0.5 + q_[1][1] * 0.5)) if False else rp(((q_[0][0] + q_[1][0]) / 2, (q_[0][1] + q_[1][1]) / 2), y1 + 0.6, 1),
                 rp(q_[1], y1, 2), rp(q_[2], y1, 3), rp(q_[3], y1, 4)]
        riser = [P(a[0], y0, a[1]), P(b[0], y0, b[1]), tread[2], tread[0]]
        rc = lerp(shaded(stone_, 0.75), shaded(mixp(stone_, PRUSSIAN, 0.35), 1.0), dim)
        tc = lerp(faced(mixp(stone_, MOSS, 0.20), t_tread * 0.8), shaded(mixp(stone_, MOSS, 0.55), 0.95), dim)
        L.poly(riser, rc, shaded(rc, 0.4), g=(riser[3], riser[0]))
        L.poly(tread, tc, lerp(tc, faced(MOSS, t_tread * (1 - dim)), 0.30), g=(tread[0], tread[3]))
        # worn bare in the middle, moss at the ends and in the joint behind
        mid_ = path_at(st["s"] + 14, 0)
        mx, my = P(mid_[0], y1 + 0.4, mid_[1])
        L.ellipse(mx, my, 34 * kk, 5 * kk + 0.5, lerp(tc, faced(mixp(stone_, WPAPER, 0.3), t_tread), 0.4 * (1 - dim)), alpha=0.55)
        for side in (-1, 1):
            m0 = path_at(st["s"] + rng.uniform(4, 20), side * (PATH_W / 2 - rng.uniform(6, 20)))
            mx, my = P(m0[0], y1 + 0.5, m0[1])
            L.ellipse(mx, my, rng.uniform(10, 22) * kk, rng.uniform(2.5, 4.5) * kk + 0.5, faced(MOSS, t_tread * 0.6 * (1 - dim)) if dim < 0.5 else shaded(MOSS, 0.85), alpha=0.75)
        if dim < 0.6:
            keyline(L, [riser[3], riser[2]], row=riser[2][1], seed=200 + i, weight=0.7, alpha=0.30)
    # ferns and young azaleas crowding its sides, more as it climbs, its top lost in them
    for st in steps[2:]:
        for side in (-1, 1):
            if rng.random() < 0.35:
                continue
            m0 = path_at(st["s"] + rng.uniform(0, 30), side * (PATH_W / 2 + rng.uniform(0, 30)))
            D = m0[1]
            kk = F / D
            yb = st["y1"] + rng.uniform(-6, 10)
            cx_, cy_ = P(m0[0], yb, D)
            dim = float(np.clip((st["s"] - 90.0) / 240.0, 0, 1))
            for q in range(5):
                ln = rng.uniform(18, 40) * kk
                ang = -math.pi / 2 + rng.uniform(-1.2, 1.2)
                c = faced(mixp(VERONESE, VIRIDIAN, 0.5), 0.6 * (1 - dim)) if rng.random() < 0.5 else shaded(mixp(VIRIDIAN, PRUSSIAN, 0.2), 0.8)
                L.line(curve([(cx_, cy_), (cx_ + math.cos(ang) * ln * 0.5, cy_ + math.sin(ang) * ln * 0.6), (cx_ + math.cos(ang) * ln, cy_ + math.sin(ang) * ln * 0.7 + ln * 0.2)], 4), c, max(0.8, 2.4 * kk), 0.85)
    c, a = L.done()
    over(pic, c, a)
    info["path"] = a
    return info


# ================================================================ the terrace
def vista_mask():
    """Where the plain far below is seen: right of the woods, below the horizon, above the terrace's edge."""
    edge = [foot(*p) for p in EDGE]
    ex = [p[0] for p in edge]
    ey = [p[1] for p in edge]
    line = np.interp(np.arange(W), ex, ey, left=ey[0], right=ey[-1]).astype(F32)
    m = (Y_ > HZ - 2) & (Y_ < line[None, :] + 2) & (X_ > 560)
    return m.astype(F32), line


def ground(pic, info):
    """The terrace before the hall: packed earth and fine gravel, worn pale where feet go (to the doors, to the bench, up
    the road), grass along its edges and moss under the woods; deeper and warmer toward us, paler toward the back; the
    road coming up from the town at the bottom right, its two worn tracks. Measured on the ground (world_noise), so all
    of it shrinks with distance."""
    Xg, Dg, below = ground_grid()
    _, edge_line = vista_mask()
    terrace = below * (Y_ >= edge_line[None, :] - 1) * (1 - info["bank"])
    t = np.clip((Y_ - HZ) / float(H - HZ), 0, 1) ** 0.9
    gold = light_k()
    e_far = lerp(EARTH, K.horizon_c(), 0.25)
    base = lerp(e_far[None, None, :], EARTH[None, None, :], np.clip(t * 2.2, 0, 1)[..., None])
    base = lerp(base, EARTH_NEAR[None, None, :], (np.clip((t - 0.5) * 2.0, 0, 1) * 0.8)[..., None])
    blot = world_noise(Xg, Dg, 160, 91, 3)
    fine = world_noise(Xg, Dg, 34, 92, 3)
    base = base * (1 + ((blot - 0.5) * 0.16 + (fine - 0.5) * 0.10)[..., None])
    warmcool = (world_noise(Xg, Dg, 420, 93, 2) - 0.5) * 0.05
    base[..., 0] += warmcool
    base[..., 2] -= warmcool
    # worn ways: pale and smooth where everyone walks
    wear = np.zeros(SHAPE, F32)
    for pts_w, wd in (([(560.0, 620.0), (470.0, 900.0), (330.0, 1000.0), (230.0, 1060.0)], 140.0),          # up the road to the doors
                      ([(230.0, 1060.0), (60.0, 1020.0), (-100.0, 1020.0), (-260.0, 1100.0), (-380.0, 1200.0)], 90.0),   # along to the bench and the path
                      ([(-380.0, 1200.0), (-600.0, 1500.0), (-760.0, 1580.0)], 70.0)):                     # to the hut
        m = mask_line(SHAPE, [foot(x, d) for x, d in pts_w], [max(1.0, wd * F / d) for x, d in pts_w], soft=4.0)
        np.maximum(wear, m, out=wear)
    wear = wear * (0.5 + 0.5 * world_noise(Xg, Dg, 90, 94, 2))
    base = lerp(base, lerp(EARTH, WPAPER, 0.35)[None, None, :], (wear * 0.42)[..., None])
    # the road at the bottom right: its two tracks worn pale, its verge rough
    ro = road_mask()
    rx_ = road_across(Xg, Dg)
    track = sum(np.exp(-((rx_ - c) / 0.16) ** 2) for c in (-0.42, 0.40))
    road_c = lerp(base, lerp(EARTH, WPAPER, 0.42)[None, None, :], (np.clip(track, 0, 1) * 0.55)[..., None])
    road_c = road_c * (1 - (step(0.78, 1.0, np.abs(rx_)) * 0.12)[..., None])
    base = lerp(base, road_c, ro[..., None])
    # grass and moss: along the terrace's edge on the right, at the foot of the bank and the hut, in the hall's lee
    gr = world_noise(Xg, Dg, 110, 95, 3)
    edge_near = np.clip(1 - (Y_ - edge_line[None, :]) / 22.0, 0, 1) * (X_ > 600)
    bank_foot = np.clip(1 - np.abs(Dg - np.interp(Xg, [p[0] for p in BANK_FOOT], [p[1] for p in BANK_FOOT])) / 260.0, 0, 1)
    grass_m = np.clip((edge_near + bank_foot * 0.8) * step(0.35, 0.65, gr), 0, 1)
    base = lerp(base, GRASS[None, None, :], (grass_m * 0.50)[..., None])
    base = lerp(base, MOSS[None, None, :], (bank_foot * step(0.55, 0.75, 1 - gr) * 0.30)[..., None])
    # fine gravel: paler and darker grains, by place (large near us, a speckle far off); needles under the old pine
    grit = world_noise(Xg, Dg, 6, 99, 2)
    grit2 = world_noise(Xg, Dg, 2.5, 100, 1)
    base = base * (1 + ((grit - 0.5) * 0.14 + (grit2 - 0.5) * 0.12)[..., None])
    needles = step(0.62, 0.70, world_noise(Xg, Dg, (3, 26), 101, 2)) * np.clip(1 - (Dg - 700.0) / 500.0, 0, 1) * np.clip(1 - Xg / 400.0, 0, 1)
    base = lerp(base, mixp(SIENNA, OCHRE, 0.45)[None, None, :], (needles * 0.35)[..., None])
    # the light on it (shadows are laid after, as glazes)
    lit_c = np.clip(1 - (1 - base * K._LIT_MUL[K.LIGHT]) * (1 - K._LIT_ADD[K.LIGHT] * 0.8), 0, 1)
    if not gold:
        lit_c = base * np.array([0.86, 0.76, 0.80], F32)                     # at sunset the ground away from the streaks is dim
    over(pic, lit_c.astype(F32), terrace.astype(F32))
    info["terrace"] = terrace.astype(F32)
    info["wear"] = wear
    # pebbles and tufts at a true density, few and large near us, many and small far off
    s = Wet(SHAPE)
    zone = terrace * (1 - info.get("hallfoot", 0))
    for (x, y, kk, r) in DEPTH.scatter(lambda X, Z: foot(X, Z), lambda X, Z: F / Z, (-1600, 1600, 700, 2600), 3.0, 96, size=(3.0, 2.0), zone=zone):
        rr = (1.0 + 2.6 * r) * kk
        if rr < 0.45:
            continue
        sc = lerp(faced(STONE_C, 0.7), faced(mixp(STONE_C, OCHRE, 0.3), 0.6), r)
        s.ellipse(x + rr * 0.3, y + rr * 0.25, rr * 1.2, rr * 0.45, shaded(EARTH, 0.7), alpha=0.6)
        s.ellipse(x, y, rr, rr * 0.55, sc, shaded(sc, 0.5), g=((x - rr, y - rr), (x + rr, y + rr)))
    for (x, y, kk, r) in DEPTH.scatter(lambda X, Z: foot(X, Z), lambda X, Z: F / Z, (-1600, 1600, 700, 2600), 3.0, 97, size=(6.0, 9.0), zone=zone):
        hgt = (5.0 + 9.0 * r) * kk
        if hgt < 0.8:
            continue
        for q in range(4):
            a_ = -math.pi / 2 + (q - 1.5) * 0.35 + (r - 0.5) * 0.4
            s.line([(x + (q - 1.5) * kk * 1.5, y), (x + (q - 1.5) * kk * 1.5 + math.cos(a_) * hgt, y + math.sin(a_) * hgt)],
                   faced(GRASS, 0.7) if q % 2 else shaded(GRASS, 0.4), max(0.6, kk * 1.4), 0.85)
    c, a = s.done()
    over(pic, c, a * terrace)
    return info


ROAD_N = 9


def road_across(Xg, Dg):
    """-1..1 across the road at each place (beyond: outside it)."""
    xs = [p[0] for p in ROAD]
    ds = [p[1] for p in ROAD]
    mid = np.interp(Dg, ds, xs)
    return ((Xg - mid) / (ROAD_W / 2)).astype(F32)


def road_mask():
    Xg, Dg, below = ground_grid()
    ra = road_across(Xg, Dg)
    m = np.clip(1.15 - np.abs(ra), 0, 1) * (Dg < ROAD[-1][1] + 60) * below
    m = m * np.clip((ROAD[-1][1] + 60 - Dg) / 120.0, 0, 1)
    return np.clip(m * 4.0, 0, 1).astype(F32)


def terrace_edge(pic, info):
    """The terrace's edge over the plain, at the right. Beyond it the slope falls away, and the crowns of its trees rise
    into view just past the edge: a band of treetops, dark, lit on their tops, overlapping the near plain (the vista's
    first layer). On the edge itself, short rough grass and two low shrubs."""
    L = Wet(SHAPE)
    rng = np.random.default_rng(98)
    _, line = vista_mask()
    gold = light_k()
    # the treetops of the slope below: only the tops of the tallest crowns rise past the lip, a ragged band
    T_ = Wet(SHAPE)
    for i in range(34):
        x = rng.uniform(596, 812)
        y0 = float(line[min(int(x), W - 1)]) + 1
        hgt = rng.uniform(6, 30)
        wid = rng.uniform(16, 44)
        pine_ = rng.random() < 0.35
        c_dark = shaded(mixp(VIRIDIAN, PRUSSIAN, 0.35 if pine_ else 0.15), 0.80 if gold else 1.0)
        c_lit = faced(mixp(VIRIDIAN, VERONESE, 0.25 if pine_ else 0.55), 0.85 if gold else 0.05)
        if pine_:
            for j in range(3):
                cy_ = y0 - hgt + j * hgt * 0.38
                T_.ellipse(x + rng.normal(0, 3), cy_, wid * (0.30 + 0.12 * j), hgt * 0.16 + 1.5, c_dark)
                T_.ellipse(x - 2, cy_ - 1.2, wid * (0.18 + 0.08 * j), hgt * 0.07 + 0.8, c_lit, alpha=0.8)
        else:
            n_ = 12
            pts = [(x - wid / 2, y0 + 4)]
            for q in range(n_ + 1):
                u = q / n_
                bump = math.sin(math.pi * u) ** 0.7 * hgt * rng.uniform(0.75, 1.1)
                pts.append((x - wid / 2 + wid * u, y0 - bump))
            pts.append((x + wid / 2, y0 + 4))
            T_.poly(pts, c_lit, c_dark, g=((x, y0 - hgt), (x, y0 + 2)))
    tc, ta = T_.done()
    ta = ta * (Y_ < line[None, :] + 3)
    over(pic, tc, ta)
    # short rough grass along the lip, and two low shrubs on it
    for (x, w, h) in ((652.0, 24.0, 16.0), (742.0, 30.0, 20.0)):
        y = float(line[int(x)]) + 5
        for q in range(22):
            cx_ = x + rng.uniform(-w, w) * 0.85
            up = rng.random()
            cy_ = y - h * (0.15 + 0.75 * up)
            r = rng.uniform(3.5, 6.0)
            c = faced(mixp(VIRIDIAN, VERONESE, 0.35), 0.85 if gold else 0.05) if (up > 0.45 and rng.random() < 0.7) else shaded(mixp(VIRIDIAN, PRUSSIAN, 0.35), 0.75)
            pts = [(cx_ + math.cos(a) * r * rng.uniform(0.75, 1.2), cy_ + math.sin(a) * r * 0.62 * rng.uniform(0.75, 1.2)) for a in np.linspace(0, 2 * math.pi, 9)[:-1]]
            L.poly(pts, c)
    for x in np.arange(600.0, 806.0, 2.2):
        y = float(line[min(int(x), W - 1)]) + 4
        ln = rng.uniform(3, 8)
        lean = rng.uniform(-0.7, 0.7)
        c = faced(mixp(GRASS, VIRIDIAN, 0.35), 0.75 if gold else 0.0) if rng.random() < 0.55 else shaded(mixp(GRASS, VIRIDIAN, 0.5), 0.7)
        L.line([(x, y + 1), (x + lean * ln, y - ln)], c, 1.0, 0.85)
    c, a = L.done()
    over(pic, c, a)
    info["edge"] = a
    return info


# ================================================================ O-Ume's hut
def hut(L):
    """O-Ume's hut, farther off at the foot of the woods: a little hut of boards and mud plaster under a thick thatch,
    hipped, its front to the south (toward us and right), its west end lit; a door with a straw curtain rolled half up,
    a small barred window, the paper lantern on its hook by the door (unlit), firewood stacked against its east end."""
    w, d, wall, e = HUT["w"], HUT["d"], HUT["wall"], HUT["eave"]
    Q = lambda a, b, y: P(*hut_at(a, b)[:1], y, hut_at(a, b)[1])
    t_front, t_west = face_t(N_FRONT), face_t(N_WEST)
    D0 = hut_at(0, 0)[1]
    A = lambda c: aired(c, D0, scale=30000)
    # the west end (lit) and the front
    west = [Q(0, d, 0), Q(0, 0, 0), Q(0, 0, wall), Q(0, d, wall)]
    front = [Q(0, 0, 0), Q(w, 0, 0), Q(w, 0, wall), Q(0, 0, wall)]
    L.poly(west, A(faced(PLASTER, t_west)), A(faced(PLASTER, t_west * 0.8)), g=(west[3], west[0]))
    L.poly(front, A(faced(PLASTER, t_front)), A(faced(mixp(PLASTER, OCHRE, 0.2), t_front * 0.7)), g=(front[3], front[0]))
    for (poly_, t_) in (([Q(0, d, 0), Q(0, 0, 0), Q(0, 0, 70), Q(0, d, 70)], t_west), ([Q(0, 0, 0), Q(w, 0, 0), Q(w, 0, 70), Q(0, 0, 70)], t_front)):
        L.poly(poly_, A(faced(WOOD, t_)), A(faced(mixp(WOOD, TIMBER, 0.4), t_)), g=(poly_[3], poly_[0]))
    for a_ in (0.0, w * 0.48, w):                                            # posts
        L.poly([Q(a_ - 6, -1, 0), Q(a_ + 6, -1, 0), Q(a_ + 6, -1, wall), Q(a_ - 6, -1, wall)], A(faced(TIMBER, t_front)))
    L.poly([Q(-2, -1, wall - 12), Q(w + 2, -1, wall - 12), Q(w + 2, -1, wall), Q(-2, -1, wall)], A(faced(TIMBER, t_front)))
    # the door: dark inside, the straw curtain rolled half up
    door = [Q(26, -2, 0), Q(108, -2, 0), Q(108, -2, 168), Q(26, -2, 168)]
    L.poly(door, A(shaded(mixp(PRUSSIAN, SIENNA, 0.4), 0.5)))
    L.poly([Q(26, -3, 112), Q(108, -3, 112), Q(108, -3, 168), Q(26, -3, 168)], A(faced(THATCH, t_front)), A(faced(mixp(THATCH, SIENNA, 0.3), t_front)), g=(Q(60, -3, 168), Q(60, -3, 112)))
    L.line([Q(26, -4, 112), Q(108, -4, 112)], A(shaded(THATCH, 0.8)), 2.0, 0.9)
    # the window
    win = [Q(w - 96, -2, 92), Q(w - 34, -2, 92), Q(w - 34, -2, 138), Q(w - 96, -2, 138)]
    L.poly(win, A(shaded(mixp(PRUSSIAN, SIENNA, 0.35), 0.6)))
    for i in range(1, 5):
        aa = w - 96 + 62 * i / 5
        L.line([Q(aa, -3, 92), Q(aa, -3, 138)], A(faced(WOOD, t_front)), 1.2, 0.9)
    # firewood against the east end
    for j in range(5):
        yy = 6 + j * 15
        L.poly([Q(w + 4, -10, yy), Q(w + 4, 60, yy), Q(w + 4, 60, yy + 13), Q(w + 4, -10, yy + 13)], A(faced(mixp(WOOD, OCHRE, 0.3), t_front * 0.6)))
        for q in range(4):
            L.ellipse(*Q(w + 3, -4 + q * 16, yy + 6.5), 2.2, 2.0, A(faced(mixp(OCHRE, NAPLES, 0.4), 0.6)), alpha=0.9)
    # the thatch: hipped, thick at its eave, its west hip lit
    ye = wall - 6
    ridge_w = (55.0, w - 55.0)
    eF0, eF1 = Q(-e, -e, ye), Q(w + e, -e, ye)
    eB0 = Q(-e, d + e, ye)
    r0, r1 = Q(ridge_w[0], d / 2, HUT["ridge"]), Q(ridge_w[1], d / 2, HUT["ridge"])
    hip = [eB0, eF0, r0]
    slope = [eF0, eF1, r1, r0]
    n_hip = (-0.8, 0.6, -0.2)
    n_slope = (math.sin(PHI) * 0.6, 0.75, -math.cos(PHI) * 0.6)
    L.poly(hip, A(faced(THATCH, face_t(n_hip))), A(faced(mixp(THATCH, SIENNA, 0.3), face_t(n_hip) * 0.7)), g=(r0, eF0))
    L.poly(slope, A(faced(THATCH, face_t(n_slope))), A(faced(mixp(THATCH, SIENNA, 0.35), face_t(n_slope) * 0.6)), g=(r0, eF0))
    th = 34.0
    L.poly([Q(-e, -e, ye), Q(w + e, -e, ye), Q(w + e, -e, ye - th), Q(-e, -e, ye - th)], A(shaded(mixp(THATCH, SIENNA, 0.25), 0.5)))
    L.poly([Q(-e, d + e, ye), Q(-e, -e, ye), Q(-e, -e, ye - th), Q(-e, d + e, ye - th)], A(faced(mixp(THATCH, SIENNA, 0.2), face_t(N_WEST) * 0.8)))
    L.line([r0, r1], A(shaded(mixp(THATCH, PRUSSIAN, 0.3), 0.6)), 3.0, 0.9)
    rng = np.random.default_rng(99)
    for i in range(40):                                                      # the straw, in dry strokes down the slopes
        u = rng.random()
        p0 = (eF0[0] + (eF1[0] - eF0[0]) * u, eF0[1] + (eF1[1] - eF0[1]) * u)
        p1 = (r0[0] + (r1[0] - r0[0]) * u, r0[1] + (r1[1] - r0[1]) * u)
        v0 = rng.uniform(0.0, 0.6)
        a_ = (p0[0] + (p1[0] - p0[0]) * v0, p0[1] + (p1[1] - p0[1]) * v0)
        b_ = (p0[0] + (p1[0] - p0[0]) * (v0 + 0.3), p0[1] + (p1[1] - p0[1]) * (v0 + 0.3))
        L.line([a_, b_], A(shaded(THATCH, 0.6)), 0.6, 0.35)
    keyline(L, [eF0, eF1], seed=301, weight=0.9)
    keyline(L, [front[0], front[1]], seed=302)
    keyline(L, [front[1], front[2]], seed=303)
    # the lantern on its hook (unlit): a folding paper lantern, its frame dark
    la, lb, ly = HUT_LANTERN_AB
    hx, hy = Q(la, lb, ly)
    kk = F / hut_at(la, lb)[1]
    L.line([(hx, hy - 16 * kk), (hx, hy)], A(TIMBER), 1.0, 0.9)
    lw, lh = 15 * kk, 28 * kk
    lan = [(hx - lw, hy + 2), (hx + lw, hy + 2), (hx + lw * 1.12, hy + lh * 0.5), (hx + lw, hy + lh), (hx - lw, hy + lh), (hx - lw * 1.12, hy + lh * 0.5)]
    L.poly(lan, A(faced(WPAPER, t_front * 0.6 + 0.3)), A(faced(mixp(WPAPER, OCHRE, 0.25), t_front * 0.5)), g=((hx - lw, hy), (hx + lw, hy)))
    for j in range(1, 5):
        yy = hy + 2 + (lh - 2) * j / 5
        L.line([(hx - lw * 1.05, yy), (hx + lw * 1.05, yy)], A(shaded(mixp(WPAPER, OCHRE, 0.4), 0.4)), 0.5, 0.6)
    L.poly([(hx - lw * 0.7, hy), (hx + lw * 0.7, hy), (hx + lw * 0.7, hy + 2.6), (hx - lw * 0.7, hy + 2.6)], A(TIMBER))
    L.poly([(hx - lw * 0.7, hy + lh), (hx + lw * 0.7, hy + lh), (hx + lw * 0.7, hy + lh + 2.6), (hx - lw * 0.7, hy + lh + 2.6)], A(TIMBER))
    return dict(lantern=(hx, hy, lw, lh))


# ================================================================ the women's hall
SLIPS = []


def build_slips():
    rng = np.random.default_rng(57)
    out = []
    da, db = DOOR_A
    for (a0, a1) in ((14, da - 14), (db + 14, SIDE - 14)):                   # on the panels either side, many, old and new
        for i in range(30):
            out.append((rng.uniform(a0, a1 - 7), rng.uniform(70, 262), rng.uniform(6.5, 8.5), rng.uniform(18, 27), rng.random()))
    for a in (da - 12, db + 2, 2, SIDE - 12):                                # up the posts
        for i in range(8):
            out.append((a, 64 + i * 26 + rng.uniform(-3, 3), 9, rng.uniform(16, 22), rng.random()))
    for i in range(12):                                                      # on the lintel
        out.append((da - 4 + i * 15 + rng.uniform(-2, 2), 258 + rng.uniform(-2, 2), 8, 12, rng.random()))
    return out


def hall(L, inside=True):
    """The hall: the stone base; the west side (boards between posts, a tie beam, the lattice window: in full sun); the
    front (posts, board panels either side of the doorway, the lintel, the sill: at a slant); the slips pasted round
    the doors and up the posts; the step; the deep eaves (their rafters seen from below, in shade); the pyramid roof of
    tiles, its two faces we see, the hips; the jewel. The doorway is left empty: the doors and the inside are their own."""
    t_f, t_w = face_t(N_FRONT), face_t(N_WEST)
    bo, bh = BASE_OUT, BASE_H
    rng = np.random.default_rng(58)
    # ---- the base: dressed granite blocks, its top lit
    bf = [HP(-bo, -bo, 0), HP(SIDE + bo, -bo, 0), HP(SIDE + bo, -bo, bh), HP(-bo, -bo, bh)]
    bw = [HP(-bo, SIDE + bo, 0), HP(-bo, -bo, 0), HP(-bo, -bo, bh), HP(-bo, SIDE + bo, bh)]
    L.poly(bw, faced(STONE_C, t_w), faced(mixp(STONE_C, OCHRE, 0.15), t_w * 0.8), g=(bw[3], bw[0]))
    L.poly(bf, faced(STONE_C, t_f), shaded(STONE_C, 0.4) if t_f < 0.3 else faced(STONE_C, t_f * 0.7), g=(bf[3], bf[0]))
    top = [HP(-bo, -bo, bh), HP(SIDE + bo, -bo, bh), HP(SIDE + bo, SIDE + bo, bh), HP(-bo, SIDE + bo, bh)]
    L.poly(top, faced(mixp(STONE_C, WPAPER, 0.25), face_t((0, 1, 0))))
    for k_ in range(1, 7):                                                   # joints
        a = -bo + (SIDE + 2 * bo) * k_ / 7 + rng.uniform(-6, 6)
        L.line([HP(a, -bo - 0.5, 1), HP(a, -bo - 0.5, bh - 1)], shaded(STONE_C, 0.9), 0.7, 0.55)
        L.line([HP(-bo - 0.5, a, 1), HP(-bo - 0.5, a, bh - 1)], shaded(STONE_C, 0.7), 0.7, 0.5)
    L.line([HP(-bo, -bo - 0.5, bh * 0.5), HP(SIDE + bo, -bo - 0.5, bh * 0.5)], shaded(STONE_C, 0.8), 0.6, 0.35)
    keyline(L, [bf[0], bf[1]], seed=401)
    keyline(L, [bw[0], bw[1]], seed=402, lit=True)
    # ---- the west side: in full sun. Boards, two posts and the corner posts, a tie beam, the lattice window
    y0, y1 = bh, EAVE_Y
    west = [HP(0, SIDE, y0), HP(0, 0, y0), HP(0, 0, y1), HP(0, SIDE, y1)]
    L.poly(west, faced(WOOD, t_w), faced(mixp(WOOD, OCHRE, 0.2), t_w * 0.85), g=(west[3], west[1]))
    boards(L, rng, lambda b_, y_: HP(-0.5, b_, y_), 0.0, SIDE, y0, y1, t_w)
    for b_ in (0.0, SIDE / 2, SIDE - 12.0):
        L.poly([HP(-1.5, b_, y0), HP(-1.5, b_ + 12, y0), HP(-1.5, b_ + 12, y1), HP(-1.5, b_, y1)], faced(TIMBER, t_w), faced(mixp(TIMBER, SIENNA, 0.2), t_w))
    L.poly([HP(-2, 0, 96), HP(-2, SIDE, 96), HP(-2, SIDE, 106), HP(-2, 0, 106)], faced(TIMBER, t_w))                  # the tie beam
    la, lb = LATTICE_B
    ly0, ly1 = LATTICE_Y
    frame = [HP(-2.5, la - 7, ly0 - 7), HP(-2.5, lb + 7, ly0 - 7), HP(-2.5, lb + 7, ly1 + 7), HP(-2.5, la - 7, ly1 + 7)]
    L.poly(frame, faced(TIMBER, t_w))
    win = [HP(-3, la, ly0), HP(-3, lb, ly0), HP(-3, lb, ly1), HP(-3, la, ly1)]
    L.poly(win, shaded(mixp(PRUSSIAN, SIENNA, 0.35), 0.7), shaded(mixp(PRUSSIAN, SIENNA, 0.25), 0.4), g=(win[3], win[0]))
    for k_ in range(1, 14):                                                  # its bars: square, lit on the sun's side
        b_ = la + (lb - la) * k_ / 14
        L.line([HP(-3.5, b_, ly0), HP(-3.5, b_, ly1)], faced(mixp(TIMBER, WOOD, 0.5), t_w), 1.5, 0.95)
    keyline(L, [frame[0], frame[1]], seed=403, weight=0.8)
    # the eave's shadow down the sunlit wall: a band of cool glaze under the deep eave
    drop = 70.0 if K.LIGHT == "gold" else 22.0
    L.glaze([HP(-2.5, SIDE + 4, y1), HP(-2.5, -4, y1), HP(-2.5, -4, y1 - drop * 0.85), HP(-2.5, SIDE + 4, y1 - drop * 1.15)], K._SHADE[K.LIGHT], 0.95)
    keyline(L, [west[1], west[2]], seed=404, lit=True)
    # ---- the front: at a slant (gold), in shade (sunset)
    front = [HP(0, 0, y0), HP(SIDE, 0, y0), HP(SIDE, 0, y1), HP(0, 0, y1)]
    L.poly(front, faced(WOOD, t_f), shaded(WOOD, 0.35) if t_f < 0.2 else faced(WOOD, t_f * 0.7), g=(front[3], front[0]))
    da, db = DOOR_A
    dy0, dy1 = DOOR_Y
    boards(L, rng, lambda a_, y_: HP(a_, -0.5, y_), 0.0, da - 12, y0, y1, t_f)
    boards(L, rng, lambda a_, y_: HP(a_, -0.5, y_), db + 12, SIDE, y0, y1, t_f)
    # the doorway: cleared (the inside and the doors are drawn on their own)
    L.clear([HP(da, 0, dy0), HP(db, 0, dy0), HP(db, 0, dy1), HP(da, 0, dy1)])
    for a in (0.0, da - 13, db, SIDE - 13):                                  # posts: corners, the doorway's sides
        p = [HP(a, -2, y0), HP(a + 13, -2, y0), HP(a + 13, -2, y1), HP(a, -2, y1)]
        L.poly(p, faced(TIMBER, t_f), faced(mixp(TIMBER, SIENNA, 0.2), t_f))
    L.poly([HP(da - 13, -2.5, dy1), HP(db + 13, -2.5, dy1), HP(db + 13, -2.5, dy1 + 16), HP(da - 13, -2.5, dy1 + 16)], faced(TIMBER, t_f))      # the lintel
    L.poly([HP(da - 13, -2.5, dy0 - 9), HP(db + 13, -2.5, dy0 - 9), HP(db + 13, -2.5, dy0), HP(da - 13, -2.5, dy0)], faced(mixp(TIMBER, WOOD, 0.3), t_f))   # the sill
    L.poly([HP(-2, -2.5, 96), HP(da - 13, -2.5, 96), HP(da - 13, -2.5, 106), HP(-2, -2.5, 106)], faced(TIMBER, t_f))                       # tie beams
    L.poly([HP(db + 13, -2.5, 96), HP(SIDE + 2, -2.5, 96), HP(SIDE + 2, -2.5, 106), HP(db + 13, -2.5, 106)], faced(TIMBER, t_f))
    slips(L, t_f)
    L.glaze([HP(-2, -3, y1), HP(SIDE + 2, -3, y1), HP(SIDE + 2, -3, y1 - 70), HP(-2, -3, y1 - 50)], K._SHADE[K.LIGHT], 0.55 if K.LIGHT == "gold" else 0.25)
    keyline(L, [front[0], front[1]], seed=405)
    keyline(L, [front[1], front[2]], seed=406)
    # ---- the step before the doors: one broad dressed stone, worn in the middle
    st = STEP
    sa0, sa1, so, sh = st["a0"], st["a1"], st["out"], st["h"]
    riser = [HP(sa0, -bo - so, 0), HP(sa1, -bo - so, 0), HP(sa1, -bo - so, sh), HP(sa0, -bo - so, sh)]
    end_w = [HP(sa0, -bo, 0), HP(sa0, -bo - so, 0), HP(sa0, -bo - so, sh), HP(sa0, -bo, sh)]
    tread = [HP(sa0, -bo - so, sh), HP(sa1, -bo - so, sh), HP(sa1, -bo, sh), HP(sa0, -bo, sh)]
    L.poly(end_w, faced(STONE_C, t_w))
    L.poly(riser, faced(STONE_C, t_f), shaded(STONE_C, 0.5) if t_f < 0.3 else faced(STONE_C, t_f * 0.8), g=(riser[3], riser[0]))
    L.poly(tread, faced(mixp(STONE_C, WPAPER, 0.2), face_t((0, 1, 0))), faced(mixp(STONE_C, WPAPER, 0.35), face_t((0, 1, 0))), g=(tread[0], tread[2]))
    wm = [HP(150, -bo - so + 10, sh + 0.3), HP(220, -bo - so + 10, sh + 0.3), HP(214, -bo - 10, sh + 0.3), HP(156, -bo - 10, sh + 0.3)]
    L.poly(wm, faced(mixp(STONE_C, WPAPER, 0.5), face_t((0, 1, 0))), alpha=0.5)
    keyline(L, [riser[0], riser[1]], seed=407)
    # ---- the eaves: their undersides in shade, the rafters' ends seen from below, a bracket on each post
    e = EAVE_OUT
    ye = EAVE_Y - EAVE_DROP
    w_fl, w_fr, w_bl = HP(0, 0, y1), HP(SIDE, 0, y1), HP(0, SIDE, y1)
    e_fl, e_fr, e_bl = HP(-e, -e, ye), HP(SIDE + e, -e, ye), HP(-e, SIDE + e, ye)
    under_c = shaded(mixp(TIMBER, WOOD, 0.4), 0.75)
    bounce = faced(mixp(WOOD, OCHRE, 0.3), 0.35) if K.LIGHT == "gold" else shaded(mixp(WOOD, LAKE, 0.2), 0.5)
    L.poly([w_fl, w_fr, e_fr, e_fl], under_c, bounce, g=(e_fl, w_fl))
    L.poly([w_bl, w_fl, e_fl, e_bl], under_c, bounce, g=(e_bl, w_bl))
    for k_ in range(0, 23):                                                  # the rafters
        a = -e + (SIDE + 2 * e) * k_ / 22
        ia = min(max(a, 0), SIDE)
        L.line([HP(ia, 0, y1), HP(a, -e, ye)], lerp(under_c, bounce, 0.5), 1.2, 0.7)
        L.line([HP(0, ia, y1), HP(-e, a, ye)], lerp(under_c, bounce, 0.5), 1.2, 0.7)
    # ---- the roof: its two faces, tiles in rows running down, the hips, the eave's edge with its round tile ends
    apex = HP(SIDE / 2, SIDE / 2, APEX_Y)
    n_front_roof = (math.sin(PHI) * 0.7, 0.72, -math.cos(PHI) * 0.7)
    n_west_roof = (-math.cos(PHI) * 0.7, 0.72, -math.sin(PHI) * 0.7)
    t_fr, t_wr = face_t(n_front_roof), face_t(n_west_roof)
    lip = 10.0
    e_fl2, e_fr2, e_bl2 = HP(-e, -e, ye + lip), HP(SIDE + e, -e, ye + lip), HP(-e, SIDE + e, ye + lip)
    sag = lambda a0, a1, b0, b1, n=9: [HP(a0 + (a1 - a0) * i / n, b0 + (b1 - b0) * i / n, ye + lip - 5 * math.sin(math.pi * i / n)) for i in range(n + 1)]
    fr_edge = sag(-e, SIDE + e, -e, -e)
    wr_edge = sag(-e, -e, SIDE + e, -e)
    front_roof = fr_edge + [apex]
    west_roof = wr_edge + [apex]
    L.poly(west_roof, faced(TILE, t_wr), faced(mixp(TILE, WPAPER, 0.2), t_wr * 0.9), g=(apex, e_fl2))
    L.poly(front_roof, faced(TILE, t_fr), faced(TILE, t_fr * 0.6) if t_fr > 0 else shaded(TILE, 0.8), g=(apex, HP(SIDE / 2, -e, ye)))
    yr = lambda bb: ye + lip + (APEX_Y - ye - lip) * (bb + e) / (SIDE / 2 + e)       # the roof's height, so far in from its eave
    crest_f = faced(mixp(TILE, WPAPER, 0.30), max(t_fr, 0) * 0.9 + 0.1)
    trough_f = shaded(mixp(TILE, PRUSSIAN, 0.15), 0.75 if t_fr > 0.25 else 1.0)
    crest_w = faced(mixp(TILE, WPAPER, 0.35), t_wr)
    trough_w = faced(mixp(TILE, PRUSSIAN, 0.18), t_wr * 0.45)
    n_rows = 34
    for k_ in range(1, n_rows):                                              # the rows of round tiles, up each face to its hips
        u = -e + (SIDE + 2 * e) * k_ / n_rows
        b_end = min(u, SIDE - u)
        sg = -5 * math.sin(math.pi * k_ / n_rows)
        L.line([HP(u - 3.5, -e + 1, ye + lip + sg), HP(u - 3.5, b_end, yr(b_end))], trough_f, 0.9, 0.55)
        L.line([HP(u + 2.5, -e + 1, ye + lip + sg), HP(u + 2.5, b_end, yr(b_end))], crest_f, 0.8, 0.50)
        L.line([HP(-e + 1, u - 3.5, ye + lip + sg), HP(b_end, u - 3.5, yr(b_end))], trough_w, 0.9, 0.45)
        L.line([HP(-e + 1, u + 2.5, ye + lip + sg), HP(b_end, u + 2.5, yr(b_end))], crest_w, 0.8, 0.50)
    for q in range(1, 9):                                                    # the courses, faint, across each face
        bb = -e + (SIDE / 2 + e) * q / 9
        L.line([HP(bb, bb, yr(bb)), HP(SIDE - bb, bb, yr(bb))], trough_f, 0.5, 0.25)
        L.line([HP(bb, bb, yr(bb)), HP(bb, SIDE - bb, yr(bb))], trough_w, 0.5, 0.22)
    rng_l = np.random.default_rng(59)
    for q in range(26):                                                      # lichen and the weather's stains
        uu, vv = rng_l.uniform(-e + 20, SIDE + e - 20), rng_l.uniform(-e + 10, 120)
        if vv > min(uu, SIDE - uu) - 10:
            continue
        px_, py_ = HP(uu, vv, yr(vv))
        kk = F / H_(uu, vv)[1]
        L.ellipse(px_, py_, rng_l.uniform(4, 10) * kk, rng_l.uniform(2, 4) * kk, faced(mixp(TILE, mixp(OCHRE, VERONESE, 0.4), 0.5), max(t_fr, 0.2)) if q % 3 else shaded(TILE, 0.7), alpha=0.18)
    # the eave's edge: a thickness, the tile ends a row of small round dots
    L.poly(fr_edge + [HP(SIDE + e, -e, ye - 4), HP(-e, -e, ye - 4)], shaded(mixp(TILE, PRUSSIAN, 0.2), 0.7))
    L.poly(wr_edge + [HP(-e, -e, ye - 4), HP(-e, SIDE + e, ye - 4)], faced(mixp(TILE, PRUSSIAN, 0.15), t_w * 0.8))
    for k_ in range(0, 41):
        u = k_ / 40
        a_ = -e + (SIDE + 2 * e) * u
        px, py = HP(a_, -e - 1, ye + 2 - 5 * math.sin(math.pi * u))
        kk = F / H_(a_, -e)[1]
        L.ellipse(px, py, 5.2 * kk, 5.0 * kk, faced(mixp(TILE, WPAPER, 0.15), t_f * 0.8 + 0.1), alpha=0.9)
        px, py = HP(-e - 1, a_, ye + 2 - 5 * math.sin(math.pi * u))
        kk = F / H_(-e, a_)[1]
        L.ellipse(px, py, 5.2 * kk, 5.0 * kk, faced(mixp(TILE, WPAPER, 0.2), t_w), alpha=0.9)
    for c_ in (e_fl2, e_fr2, e_bl2):                                         # the hips: rounded ridge tiles, lit
        L.line([c_, apex], faced(mixp(TILE, WPAPER, 0.3), max(t_fr, t_wr)), 3.4, 0.95)
        L.line([(c_[0] - 1, c_[1] - 1.5), (apex[0] - 0.5, apex[1] - 1)], sunlit(mixp(TILE, WPAPER, 0.5), 0.6), 1.0, 0.6 * light_k() + 0.2)
    keyline(L, fr_edge, seed=408, weight=0.9)
    finial(L, apex)
    return dict(apex=apex)


def boards(L, rng, at, u0, u1, y0, y1, t_):
    """Vertical boards on a wall (at(u, y) -> a picture point): their joints, the grain along each, the wall darker at its
    foot where rain splashes and greyer up under the eave."""
    n = max(2, int((u1 - u0) / 24.0))
    for i in range(1, n):
        u = u0 + (u1 - u0) * i / n + rng.uniform(-2, 2)
        L.line([at(u, y0 + 2), at(u, y1 - 2)], faced(mixp(WOOD, PRUSSIAN, 0.35), t_ * 0.5), 0.7, 0.55)
    for i in range(int((u1 - u0) / 5.0)):
        u = rng.uniform(u0 + 2, u1 - 2)
        ya = rng.uniform(y0, y1 - 40)
        yb = min(y1 - 2, ya + rng.uniform(30, 120))
        c = faced(mixp(WOOD, WPAPER, 0.25), t_) if rng.random() < 0.5 else faced(mixp(WOOD, SIENNA, 0.35), t_ * 0.7)
        L.line([at(u, ya), at(u + rng.normal(0, 0.6), yb)], c, 0.5, 0.30)
    L.glaze([at(u0, y0), at(u1, y0), at(u1, y0 + 34), at(u0, y0 + 40)], mixp(WPAPER, mixp(SIENNA, PRUSSIAN, 0.5), 0.25), 0.55)


def slips(L, t_f):
    """The name slips pasted round the doors and up the posts: paper and thin wood, old and new (the new white, the old
    yellowed), each with a few ink marks of our own (no real text), overlapping."""
    global SLIPS
    if not SLIPS:
        SLIPS = build_slips()
    for (a, y, w, h, t) in SLIPS:
        c = PAPER_SLIP if t < 0.5 else (PAPER_OLD if t < 0.86 else thin(mixp(WOOD, NAPLES, 0.4), 0.3))
        p = [HP(a, -3.2, y), HP(a + w, -3.2, y), HP(a + w, -3.2, y + h), HP(a, -3.2, y + h)]
        L.poly(p, faced(c, max(t_f, 0.0) * 0.8 + 0.2 * light_k()), faced(c, max(t_f, 0.0) * 0.5))
        top_ = HP(a + w / 2, -3.6, y + h * 0.8)
        bot_ = HP(a + w / 2, -3.6, y + h * 0.3)
        L.line([top_, bot_], INK, 0.55, 0.45)


def finial(L, apex):
    """The roof's jewel, as a Buddhist hall carries it: a hoju, round below and drawn up to a point, of dark bronze,
    sitting directly in a small lotus cup on the peak. No stem, no plate, nothing across (round twenty-one's fix, at the
    lead's word: nothing on a Buddhist hall may read as a cross)."""
    ax, ay = apex
    k = F / H_(SIDE / 2, SIDE / 2)[1]
    W_, Hj = 30.0 * k, 38.0 * k
    cw, ch = 24.0 * k, 10.0 * k
    bronze = shaded(mixp(TIMBER, PRUSSIAN, 0.3), 0.3)
    lit_ = sunlit(mixp(TIMBER, OCHRE, 0.4), 0.9)
    foot_ = ay - ch * 0.55
    prof = [(0.00, 0.00), (0.26, 0.03), (0.40, 0.12), (0.47, 0.26), (0.48, 0.38), (0.43, 0.52), (0.33, 0.66), (0.20, 0.80), (0.09, 0.91), (0.00, 1.00)]
    right = [(ax + u * W_, foot_ - v * Hj) for (u, v) in prof]
    left = [(ax - u * W_, foot_ - v * Hj) for (u, v) in prof[::-1]]
    jewel = right + left[1:-1]
    L.poly(jewel, bronze)
    L.poly([(ax - u * W_ * 0.94, foot_ - v * Hj) for (u, v) in prof[1:9]] + [(ax - 0.12 * W_, foot_ - 0.62 * Hj), (ax - 0.16 * W_, foot_ - 0.30 * Hj)], lit_, alpha=0.8)
    rim = ay - ch
    top = []
    for i in range(3):
        x0 = ax - cw / 2 + cw * i / 3
        x1 = ax - cw / 2 + cw * (i + 1) / 3
        top += [(x0, rim), ((x0 + x1) / 2, rim - ch * 0.38)]
    top.append((ax + cw / 2, rim))
    bowl = [(ax + cw / 2 * math.cos(t_), rim + ch * math.sin(t_)) for t_ in np.linspace(0.0, math.pi, 12)]
    L.poly(top + bowl[1:-1], lerp(bronze, lit_, 0.25))
    keyline(L, jewel, row=HZ + 60, seed=409, weight=0.8, alpha=0.4)


def interior(L, light):
    """What the open doors show, in the backdrop behind them: the dim hall, its boards, at the back the small shut
    cabinet on its stand, and the bars of light from the west lattice lying across the floor and up the east wall (gold
    by day, red at sunset). Kept to the doorway."""
    da, db = DOOR_A
    dy0, dy1 = DOOR_Y
    dark = shaded(mixp(PRUSSIAN, SIENNA, 0.38), 0.6)
    far_ = shaded(mixp(PRUSSIAN, ULTRA, 0.35), 0.5)
    L.poly([HP(da, 0, dy0), HP(db, 0, dy0), HP(db, 0, dy1), HP(da, 0, dy1)], dark)
    L.poly([HP(da - 20, SIDE, dy0), HP(db + 20, SIDE, dy0), HP(db + 20, SIDE, dy1 + 40), HP(da - 20, SIDE, dy1 + 40)], far_)
    L.poly([HP(da - 20, 30, dy0), HP(db + 20, 30, dy0), HP(db + 20, SIDE, dy0), HP(da - 20, SIDE, dy0)], lerp(dark, far_, 0.3))
    L.poly([HP(150, SIDE - 4, dy0), HP(214, SIDE - 4, dy0), HP(214, SIDE - 4, dy0 + 42), HP(150, SIDE - 4, dy0 + 42)], lerp(dark, faced(WOOD, 0.3), 0.3))
    L.poly([HP(160, SIDE - 6, dy0 + 42), HP(204, SIDE - 6, dy0 + 42), HP(204, SIDE - 6, dy0 + 124), HP(160, SIDE - 6, dy0 + 124)], lerp(dark, TIMBER, 0.3))
    L.poly([HP(SIDE - 2, 40, dy0), HP(SIDE - 2, SIDE, dy0), HP(SIDE - 2, SIDE, dy1 + 40), HP(SIDE - 2, 40, dy1 + 40)], lerp(dark, far_, 0.5))
    bar = thin(NAPLES, 0.35) if light == "gold" else thin(mixp(ORANGE, LAKE, 0.35), 0.15)
    for j in range(4):
        b0 = 150 + j * 32
        L.poly([HP(60, b0, dy0 + 1), HP(SIDE - 2, b0 - 150, dy0 + 1), HP(SIDE - 2, b0 - 136, dy0 + 1), HP(60, b0 + 14, dy0 + 1)], bar, alpha=0.45)
        L.poly([HP(SIDE - 3, b0 - 150, dy0 + 1), HP(SIDE - 3, b0 - 136, dy0 + 1), HP(SIDE - 3, b0 - 118, dy0 + 120), HP(SIDE - 3, b0 - 132, dy0 + 120)], bar, alpha=0.6)


# ================================================================ the cut-outs of the play
def doors(L, state="shut"):
    """The double doors (they part in the middle and swing out toward us): each leaf a frame round a fine lattice (the
    dim hall behind it), a board panel low down; the meeting stiles broad, the hasp's iron across them where the lock
    hangs. shut / half (each leaf 45 degrees out) / open (turned back, nearly against the front)."""
    da, db = DOOR_A
    dy0, dy1 = DOOR_Y
    leaf = (db - da) / 2
    ang = {"shut": 0.0, "half": 45.0, "open": 84.0}[state]
    th = math.radians(ang)
    t_f = face_t(N_FRONT)
    order = (1, -1)                                                          # (the right leaf first: the left one is nearer us when open)
    for side in order:
        hinge = da if side < 0 else db
        sgn = 1 if side < 0 else -1

        def at(u, y, out=0.0):
            a = hinge + sgn * leaf * u * math.cos(th)
            b = -leaf * u * math.sin(th) - 2.0 - out
            return HP(a, b, y)
        # the leaf's facing: its outer face turns with it
        nx = N_FRONT[0] * math.cos(th) - sgn * UX * math.sin(th) * 0 + (-VX if False else 0)
        rot = -sgn * th
        nfx = math.sin(PHI + rot) if True else 0
        n_leaf = (math.sin(PHI - sgn * th), 0.0, -math.cos(PHI - sgn * th))
        t_l = face_t(n_leaf)
        frame_c = faced(TIMBER, t_l) if t_l > 0 else shaded(TIMBER, 0.6)
        stile_c = faced(mixp(WOOD, TIMBER, 0.35), t_l) if t_l > 0 else shaded(mixp(WOOD, TIMBER, 0.35), 0.55)
        corners = [at(0, dy0), at(1, dy0), at(1, dy1), at(0, dy1)]
        L.poly(corners, frame_c)
        # the low board panel
        panel = [at(0.08, dy0 + 6), at(0.92, dy0 + 6), at(0.92, dy0 + 52), at(0.08, dy0 + 52)]
        L.poly(panel, stile_c, lerp(stile_c, frame_c, 0.4), g=(panel[3], panel[0]))
        # the lattice: the dim inside crossed by fine square bars
        inner = [at(0.10, dy0 + 60), at(0.84, dy0 + 60), at(0.84, dy1 - 12), at(0.10, dy1 - 12)]
        L.poly(inner, shaded(mixp(PRUSSIAN, SIENNA, 0.38), 0.6), shaded(mixp(PRUSSIAN, SIENNA, 0.3), 0.4), g=(inner[3], inner[0]))
        for k_ in range(1, 8):
            u = 0.10 + 0.74 * k_ / 8
            L.line([at(u, dy0 + 60), at(u, dy1 - 12)], stile_c, 1.3, 0.95)
        for k_ in range(1, 13):
            y = dy0 + 60 + (dy1 - dy0 - 72) * k_ / 13
            L.line([at(0.10, y), at(0.84, y)], stile_c, 1.1, 0.9)
        # the meeting stile, broad (it carries the hasp)
        L.poly([at(0.84, dy0), at(1.0, dy0), at(1.0, dy1), at(0.84, dy1)], stile_c, lerp(stile_c, frame_c, 0.3), g=(at(0.9, dy1), at(0.9, dy0)))
        keyline(L, [corners[0], corners[1]], seed=500 + side)
        keyline(L, [corners[1], corners[2]], seed=502 + side, weight=0.8)
        if ang == 0:                                                         # the hasp: an iron strap to the meeting
            a_, y_ = LOCK_AT
            iron = shaded(mixp(PRUSSIAN, SIENNA, 0.2), 0.3)
            L.poly([at(0.70, y_ - 4.5), at(1.0, y_ - 4.5), at(1.0, y_ + 4.5), at(0.70, y_ + 4.5)], iron)
            L.line([at(0.70, y_ - 4.5), at(1.0, y_ - 4.5)], faced(mixp(WPAPER, COBALT, 0.3), max(t_l, 0.25)), 0.8, 0.8)
            for u in (0.74, 0.92):
                L.ellipse(*at(u, y_), 1.0, 1.0, faced(mixp(SIENNA, OCHRE, 0.5), 0.5), alpha=0.8)


def lock(L, state="shut"):
    """The shipwright's lock on the hasp, made plain to see (the close-up, edo-lock, opens from it): a block of dark wood
    carved as a rabbit running over waves, bound with iron at its ends, its bolt through the staple. Its carved face
    takes the light: the rabbit's back and ears a lighter wood, the waves' crests pale, the iron bands bright. Open: the
    bolt drawn, the lock hanging from the staple on one side."""
    a, y = LOCK_AT
    w, h = LOCK_W, LOCK_H
    t_f = face_t(N_FRONT)
    dark = shaded(mixp(TIMBER, PRUSSIAN, 0.35), 0.15)
    carve = lerp(faced(mixp(WOOD, OCHRE, 0.25), max(t_f, 0.2) + 0.25), sunlit(NAPLES, 0.6), 0.25)
    iron = faced(lerp(mixp(PRUSSIAN, SIENNA, 0.3), WPAPER, 0.30), max(t_f, 0.15) + 0.1)
    glint = faced(mixp(WPAPER, COBALT, 0.25), max(t_f, 0.15) + 0.2)
    if state == "shut":
        y0, y1 = y - h / 2, y + h / 2
        body = [HP(a - w / 2, -6.5, y0 + 2), HP(a - w / 2 + 2, -6.5, y0), HP(a + w / 2 - 2, -6.5, y0), HP(a + w / 2, -6.5, y0 + 2),
                HP(a + w / 2, -6.5, y1 - 2), HP(a + w / 2 - 2, -6.5, y1), HP(a - w / 2 + 2, -6.5, y1), HP(a - w / 2, -6.5, y1 - 2)]
        # its shadow on the doors, a sliver below it and to the side away from the sun: it stands off them
        sx_ = 1.6 if K.LIGHT == "gold" else 1.2
        L.poly([(px_ + sx_, py_ + 1.6) for px_, py_ in body], shaded(mixp(TIMBER, PRUSSIAN, 0.5), 0.6))
        L.poly(body, dark)
        # the waves: three crests across its lower half, pale
        for k_ in range(3):
            c0 = a - w / 2 + 3 + k_ * (w - 6) / 3
            pts = [HP(c0 + (w - 6) / 3 * u, -6.8, y0 + 3.0 + 2.6 * math.sin(math.pi * u) ** 0.8) for u in np.linspace(0, 1, 6)]
            L.line(pts, lerp(carve, WPAPER, 0.25), 1.0, 0.9)
        # the rabbit running over them: its back, its long ears laid back, lit
        back = [HP(a - 8.5, -6.8, y + 0.5), HP(a - 4, -6.8, y + 4.5), HP(a + 2.5, -6.8, y + 4.8), HP(a + 7, -6.8, y + 2.0), HP(a + 5, -6.8, y - 0.5), HP(a - 6, -6.8, y - 1.0)]
        L.poly(back, carve)
        L.line([HP(a + 6, -7.0, y + 3.5), HP(a + 10.5, -7.0, y + 6.8)], carve, 1.1, 0.95)
        L.line([HP(a + 5, -7.0, y + 4.0), HP(a + 9, -7.0, y + 7.6)], carve, 0.9, 0.9)
        # the iron bands at its ends, the staple and the bolt through it
        for sx in (-1, 1):
            L.poly([HP(a + sx * (w / 2 - 3.5), -7.0, y0), HP(a + sx * (w / 2 - 0.5), -7.0, y0), HP(a + sx * (w / 2 - 0.5), -7.0, y1), HP(a + sx * (w / 2 - 3.5), -7.0, y1)], iron)
            L.line([HP(a + sx * (w / 2 - 3.5), -7.2, y1 - 0.5), HP(a + sx * (w / 2 - 0.5), -7.2, y1 - 0.5)], glint, 0.7, 0.8)     # its lit top
        L.line([HP(a - 1.5, -6.0, y1), HP(a - 1.5, -6.0, y1 + 3.5), HP(a + 1.5, -6.0, y1 + 3.5), HP(a + 1.5, -6.0, y1)], iron, 0.9, 0.95)
        keyline(L, body + [body[0]], row=HZ + 160, seed=510, weight=0.9, alpha=0.6)
    else:
        y0, y1 = y - h / 2 - 9, y + h / 2 - 9
        body = [HP(a + 3, -6.5, y0), HP(a + 3 + w * 0.9, -6.5, y0 - 3), HP(a + 3 + w * 0.9, -6.5, y1 - 3), HP(a + 3, -6.5, y1)]
        L.poly(body, dark)
        L.line([HP(a, -6.0, y + 4), HP(a + 4, -6.0, y1 + 1)], iron, 1.0, 0.95)
        back = [HP(a + 7, -6.8, y1 - 5), HP(a + 12, -6.8, y1 - 2), HP(a + 20, -6.8, y1 - 3), HP(a + 24, -6.8, y1 - 6)]
        L.line(back, carve, 1.4, 0.95)
        keyline(L, body + [body[0]], row=HZ + 160, seed=511, weight=0.9, alpha=0.6)


def stepball(L):
    """O-Ume's rice ball for the voice, on a leaf on the step: a white rice ball on a broad green leaf (drawn half again
    its true size, as round twenty-one did: it is clicked)."""
    a = (DOOR_A[0] + DOOR_A[1]) / 2 + 34
    b = -BASE_OUT - STEP["out"] * 0.45
    y = STEP["h"] + 0.4
    leaf = [HP(a - 18, b - 10, y), HP(a + 2, b - 15, y), HP(a + 20, b - 4, y), HP(a + 4, b + 12, y), HP(a - 15, b + 6, y)]
    L.poly(leaf, faced(mixp(VIRIDIAN, VERONESE, 0.4), face_t((0, 1, 0)) * 0.8), faced(mixp(VIRIDIAN, PRUSSIAN, 0.2), 0.4), g=(leaf[0], leaf[2]))
    L.line([HP(a - 18, b - 10, y + 0.2), HP(a + 20, b - 4, y + 0.2)], faced(mixp(VERONESE, NAPLES, 0.4), 0.8), 0.7, 0.8)
    cx, cy = HP(a, b - 1, y + 6)
    kk = F / H_(a, b)[1]
    rx, ry = 8.0 * kk * 1.5, 5.6 * kk * 1.5
    L.ellipse(cx + rx * 0.25, cy + ry * 0.9, rx * 1.1, ry * 0.4, shaded(mixp(STONE_C, WPAPER, 0.3), 0.8), alpha=0.6)
    L.ellipse(cx, cy, rx, ry, faced(WPAPER, 0.6 + 0.3 * light_k()), shaded(WPAPER, 0.35), g=((cx - rx, cy - ry), (cx + rx, cy + ry)))
    L.ellipse(cx - rx * 0.3, cy - ry * 0.3, rx * 0.45, ry * 0.4, sunlit(WPAPER, 1.0), alpha=0.8)
    L.poly([(cx - rx * 0.5, cy + ry * 0.1), (cx + rx * 0.5, cy + ry * 0.1), (cx + rx * 0.45, cy + ry * 0.75), (cx - rx * 0.45, cy + ry * 0.75)], shaded(mixp(PRUSSIAN, VIRIDIAN, 0.4), 0.3), alpha=0.85)     # its band of laver


def stone(L):
    """The small stone at the foot of the east path: a rough upright slab, its face dressed and cut with a few lines of
    marks of our own (short strokes, dots, ticks and hooks: no cut crosses another), moss at its foot."""
    X, D = STONE
    w, h, t = STONE_SIZE
    face = [P(X - w / 2, 0, D), P(X + w / 2, 0, D), P(X + w / 2 - 2, h, D), P(X + 2, h + 9, D), P(X - w / 2 + 1, h - 3, D)]
    side = [P(X - w / 2, 0, D), P(X - w / 2, 0, D + t), P(X - w / 2 + 1, h - 3, D + t), P(X - w / 2 + 1, h - 3, D)]
    t_face, t_side = face_t((0.25, 0, -1)), face_t((-1, 0, 0.1))
    L.poly(side, faced(STONE_C, t_side), faced(mixp(STONE_C, OCHRE, 0.2), t_side * 0.8), g=(side[2], side[0]))
    L.poly(face, faced(STONE_C, t_face), faced(mixp(STONE_C, MOSS, 0.3), t_face * 0.6), g=(face[3], face[0]))
    rng = np.random.default_rng(64)
    ink = shaded(mixp(STONE_C, PRUSSIAN, 0.5), 0.6)
    for col_ in (-7.0, 6.0):
        yy = h - 12.0
        while True:
            kind = ("vert", "vert", "dot", "tick", "hook")[int(rng.integers(5))]
            ln = {"vert": rng.uniform(8.0, 11.0), "dot": 3.0, "tick": 6.0, "hook": rng.uniform(8.0, 10.0)}[kind]
            if yy - ln < 22.0:
                break
            if kind == "vert":
                L.line([P(X + col_, yy, D - 0.5), P(X + col_, yy - ln, D - 0.5)], ink, 1.0, 0.85)
            elif kind == "dot":
                L.ellipse(*P(X + col_, yy - ln / 2, D - 0.5), 1.0, 0.9, ink, alpha=0.85)
            elif kind == "tick":
                L.line([P(X + col_ - 2.0, yy, D - 0.5), P(X + col_ + 2.0, yy - ln, D - 0.5)], ink, 0.9, 0.8)
            else:
                L.line([P(X + col_, yy, D - 0.5), P(X + col_, yy - ln * 0.78, D - 0.5), P(X + col_ - 2.5, yy - ln, D - 0.5)], ink, 0.9, 0.85)
            yy -= ln + rng.uniform(4.5, 6.0)
    L.ellipse(*P(X, 3, D - 3), 15, 3.5, faced(MOSS, 0.4), alpha=0.9)
    keyline(L, face[1:4], seed=520)
    keyline(L, [face[0], face[1]], seed=521)


def bench(L):
    """The bench where the women wait: a long plain plank on four legs, worn pale where they sit."""
    fl, fr, br, bl = bench_pts()
    hgt = BENCH["h"]
    t_top, t_edge, t_end = face_t((0, 1, 0)), face_t(N_FRONT), face_t(N_WEST)
    legs = []
    for t_ in (0.06, 0.92):
        for o in (4.0, BENCH["deep"] - 8.0):
            px_ = fl[0] + (fr[0] - fl[0]) * t_ + o * VX
            pd_ = fl[1] + (fr[1] - fl[1]) * t_ + o * VD
            legs.append((px_, pd_))
    for (px_, pd_) in sorted(legs, key=lambda q: -q[1]):
        L.poly([P(px_, 0, pd_), P(px_ + 6, 0, pd_), P(px_ + 6, hgt - 5, pd_), P(px_, hgt - 5, pd_)], faced(TIMBER, t_edge))
    top = [P(fl[0], hgt, fl[1]), P(fr[0], hgt, fr[1]), P(br[0], hgt, br[1]), P(bl[0], hgt, bl[1])]
    edge = [P(fl[0], hgt - 6, fl[1]), P(fr[0], hgt - 6, fr[1]), P(fr[0], hgt, fr[1]), P(fl[0], hgt, fl[1])]
    endw = [P(bl[0], hgt - 6, bl[1]), P(fl[0], hgt - 6, fl[1]), P(fl[0], hgt, fl[1]), P(bl[0], hgt, bl[1])]
    L.poly(top, faced(mixp(WOOD, WPAPER, 0.15), t_top), faced(WOOD, t_top * 0.8), g=(top[0], top[1]))
    L.poly(edge, faced(TIMBER, t_edge))
    L.poly(endw, faced(TIMBER, t_end))
    keyline(L, [edge[0], edge[1]], seed=530)


def combs(L):
    """The heap of combs and hairpins on a faded indigo cloth on the ground before the bench: half-moon combs of boxwood
    (honey), of tortoiseshell (mottled brown), of black lacquer; pins with a bead or a flower at the end."""
    rng = np.random.default_rng(58)
    X, D = COMBS
    cl = [foot(X - 46, D - 28), foot(X + 44, D - 34), foot(X + 50, D + 28), foot(X - 40, D + 32)]
    cloth = thin(mixp(ULTRA, COBALT, 0.4), 0.42)
    L.poly(cl, faced(cloth, face_t((0, 1, 0))), faced(cloth, 0.3), g=(cl[3], cl[1]))
    k = F / D
    for i in range(30):
        x = X + rng.uniform(-30, 30)
        d = D + rng.uniform(-18, 20)
        cx, cy = P(x, 1.5 + rng.uniform(0, 5), d)
        r = rng.uniform(4.0, 5.5) * k * 1.4
        tone = [faced(mixp(OCHRE, NAPLES, 0.35), 0.7), faced(mixp(SIENNA, OCHRE, 0.25), 0.6), shaded(mixp(PRUSSIAN, SIENNA, 0.3), 0.2)][int(rng.integers(3))]
        if rng.random() < 0.6:
            pts = [(cx + r * math.cos(t_), cy - r * 0.6 * math.sin(t_)) for t_ in np.linspace(0, math.pi, 8)]
            L.poly(pts + [(cx - r, cy + 1.0), (cx + r, cy + 1.0)], tone)
            L.line([(cx - r * 0.8, cy + 0.5), (cx + r * 0.8, cy + 0.5)], shaded(tone, 0.6), 0.6, 0.8)
        else:
            a = rng.uniform(-0.6, 0.6)
            ln = rng.uniform(10, 14) * k * 1.4
            L.line([(cx, cy), (cx + ln * math.cos(a), cy + ln * math.sin(a) * 0.4)], faced(mixp(WPAPER, OCHRE, 0.4), 0.5), 0.9, 0.95)
            L.ellipse(cx, cy, 1.4, 1.4, [faced(VERMILION, 0.6), faced(WPAPER, 0.6), faced(LAKE, 0.6)][int(rng.integers(3))])


# ================================================================ shadows
def hull(points):
    pts = sorted(set((round(float(x), 2), round(float(y), 2)) for x, y in points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def solid_shadow(pts3):
    """The shadow on the ground of a solid given by some of its points (X, Y, D): the hull of their feet and shadows."""
    cx, cd = cast_of(K.LIGHT)
    g = []
    for (X, Y, D) in pts3:
        g.append((X, D))
        g.append((X + cx * Y, D + cd * Y))
    return [foot(x, d) for x, d in hull(g)]


def shadows(pic, info):
    """Every standing thing's shadow, one way, as a cool glaze over the terrace (the hall's, the hut's, the bench's, the
    stone's, the combs' cloth's lip); and the shade of the pines that stand out of the picture at our left, lying across
    the near ground, dappled, its edge leading in. SUNSET: the woods at the left throw the whole terrace into shade but
    for streaks of red light through the gaps between their trunks."""
    terrace = info["terrace"]
    sh = np.zeros(SHAPE, F32)

    def add(pts, amount=0.9, soft=0.8, wobble=0.8, seed=0):
        if len(pts) >= 3:
            np.maximum(sh, mask_poly(SHAPE, pts, soft=soft, wobble=wobble, seed=seed) * amount, out=sh)
    hp = []
    for (a, b) in ((-BASE_OUT, -BASE_OUT), (SIDE + BASE_OUT, -BASE_OUT), (-BASE_OUT, SIDE + BASE_OUT), (SIDE + BASE_OUT, SIDE + BASE_OUT)):
        X, D = H_(a, b)
        hp.append((X, 0, D))
    for (a, b) in ((-EAVE_OUT, -EAVE_OUT), (SIDE + EAVE_OUT, -EAVE_OUT), (-EAVE_OUT, SIDE + EAVE_OUT), (SIDE + EAVE_OUT, SIDE + EAVE_OUT)):
        X, D = H_(a, b)
        hp.append((X, EAVE_Y - EAVE_DROP, D))
    X, D = H_(SIDE / 2, SIDE / 2)
    hp.append((X, APEX_Y, D))
    add(solid_shadow(hp), 0.95, seed=1)
    hw, hd, wall = HUT["w"], HUT["d"], HUT["wall"]
    hut_pts = [(*hut_at(a, b)[:1], y, hut_at(a, b)[1]) for (a, b, y) in ((0, 0, 0), (hw, 0, 0), (0, hd, 0), (hw, hd, 0), (-70, -70, wall), (hw + 70, -70, wall), (55, hd / 2, HUT["ridge"]), (hw - 55, hd / 2, HUT["ridge"]))]
    add(solid_shadow(hut_pts), 0.9, seed=2)
    X, D = STONE
    add(solid_shadow([(X - 17, 0, D), (X + 17, 0, D), (X, 112, D), (X - 17, 0, D + 20), (X + 17, 0, D + 20)]), 0.85, soft=0.6, seed=3)
    fl, fr, br, bl = bench_pts()
    for q in (fl, fr, br, bl):
        pass
    add(solid_shadow([(fl[0], BENCH["h"], fl[1]), (fr[0], BENCH["h"], fr[1]), (br[0], BENCH["h"], br[1]), (bl[0], BENCH["h"], bl[1]),
                      (fl[0], BENCH["h"] - 6, fl[1]), (fr[0], BENCH["h"] - 6, fr[1])]), 0.7, soft=0.7, seed=4)
    # the old pine's trunk (in the picture, at the left edge): its long shadow comes in across the near ground
    cx, cd = cast_of(K.LIGHT)
    n = NEAR_PINE
    tr = [foot(n["X"] + cx * h_ + 40 * math.sin(h_ / 300.0), n["D"] + cd * h_) for h_ in np.linspace(0, 900, 16)]
    wd = [max(2.0, 2 * n["r"] * F / (n["D"] + cd * h_)) * 0.9 for h_ in np.linspace(0, 900, 16)]
    np.maximum(sh, mask_line(SHAPE, tr, wd, soft=1.2) * 0.62, out=sh)
    # the shade of things out of the picture, through the light: the old pine's great bough and its crown over us (its
    # shadow lies on the terrace at the right, before the hall's corner), and the low crowns of the trees behind us at
    # the left (theirs across the bottom of the picture). Each pad or crown an ellipsoid; a few flecks of sun come through.
    Xg, Dg, below = ground_grid()
    ln = math.hypot(cx, cd)
    ux, ud = cx / ln, cd / ln
    m = np.zeros(SHAPE, F32)
    casters = []
    for i in range(16):                                                     # the pads along the bough (4.6 to 5.6 m up)
        u = i / 15
        casters.append((-240.0 + 500.0 * u, 470.0 + 260.0 * u, 470.0 + 90.0 * math.sin(u * 3.0), 70.0, 40.0))
    for (X0, D0, Y0, rr) in ((-760.0, 120.0, 470.0, 260.0), (-520.0, -80.0, 520.0, 300.0), (-980.0, 360.0, 430.0, 240.0), (-300.0, -260.0, 600.0, 280.0),
                             (-1200.0, 560.0, 520.0, 260.0)):
        rng_c = np.random.default_rng(int(abs(X0 * 7 + D0)))
        for q in range(9):
            casters.append((X0 + rng_c.normal(0, rr * 0.5), D0 + rng_c.normal(0, rr * 0.4), Y0 + rng_c.uniform(-60, 120), rr * rng_c.uniform(0.35, 0.6), rr * 0.25))
    for (X0, D0, Y0, a_, b_) in casters:
        sx, sd = X0 + cx * Y0, D0 + cd * Y0
        pts = [(sx + ux * a_ * 1.6 * math.cos(t_) - ud * a_ * math.sin(t_), sd + ud * a_ * 1.6 * math.cos(t_) + ux * a_ * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 18)[:-1]]
        pp = [foot(x_, d_) for x_, d_ in pts if d_ > 300]
        if len(pp) >= 3:
            np.maximum(m, mask_poly(SHAPE, pp, soft=1.2, wobble=1.5, seed=int(abs(X0 + Y0))) * 0.92, out=m)
    fleck = smoothstep_(0.74, 0.79, world_noise(Xg, Dg, (34, 22), 302, 2))
    pines_sh = np.clip(m * (1 - fleck * 0.80), 0, 1) * below
    info["pines_shade"] = pines_sh
    if K.LIGHT == "gold":
        sh = np.maximum(sh, pines_sh)
        sh = blur(sh, 0.5) * terrace
        glaze(pic, sh, K._SHADE["gold"], 0.92)
    else:
        # sunset: the woods at the left put the whole terrace in shade; streaks of red light come through the gaps,
        # lying long across it to the right, along the light
        rng2 = np.random.default_rng(303)
        streak = np.zeros(SHAPE, F32)
        for (d0, w_) in ((1180.0, 40.0), (1420.0, 26.0), (1660.0, 34.0), (1960.0, 22.0), (2350.0, 30.0), (1040.0, 18.0)):
            x0 = -0.62 * d0
            pts_l = []
            for s_ in np.linspace(0, 520, 40):
                xx, dd = x0 + cx * s_, d0 + cd * s_
                if dd < 645 or (xx - CX) > 0.62 * dd + 200:
                    break
                pts_l.append((xx, dd))
            line_ = [foot(x_, d_) for x_, d_ in pts_l]
            if len(line_) >= 2:
                wid = [max(1.0, w_ * (1 + 0.5 * math.sin(i_ * 0.7 + d0)) * F / d_) for i_, (x_, d_) in enumerate(pts_l)]
                np.maximum(streak, mask_line(SHAPE, line_, wid, soft=2.5), out=streak)
        streak = streak * (1 - sh) * (1 - pines_sh * 0.5)
        info["streak"] = streak
        shade_all = np.clip(1 - streak, 0, 1) * terrace
        glaze(pic, shade_all, K._SHADE["sunset"], 0.74)
        # in the shade the earth takes the evening sky's light, not the sun's: cooler than a plain glaze leaves it, and a
        # breath lighter, so the streaks of sun across it glow
        lum = pic @ np.array([0.3, 0.55, 0.15], F32)
        cool = np.clip(lum[..., None] * np.array([0.94, 0.88, 1.24], F32) + np.array([0.03, 0.025, 0.05], F32), 0, 1)
        pic[...] = lerp(pic, cool, (shade_all * 0.55)[..., None])
        glow(pic, thin(mixp(ORANGE, VERMILION, 0.30), 0.10), (streak * terrace * 0.62).astype(F32))
        sh = np.maximum(sh, shade_all)
    info["shadow"] = sh
    return info

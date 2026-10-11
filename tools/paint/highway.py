"""A two-lane highway in Nevada at dusk: the title screen and the opening movie.

The road runs from the bottom of the picture straight away to a low horizon, and the sun is going
down exactly at the end of it. The family wagon (a cut-out the game moves) drives up the right-hand
lane toward it. Nobody walks here: the picture is a stage for the movie.

LIGHT: the sun is dead ahead, half sunk on the horizon at (400, 330). Everything is seen against it:
  - the sides of things that face us are in shadow (cool violet, lit only by the sky behind us);
  - their tops and edges carry a thin warm rim of gold, thickest on the side toward the sun;
  - every shadow on the ground runs TOWARD us, along the line from the sun's place through the thing's
    foot (so they fan out from the vanishing point, as the road does);
  - clouds are lit from underneath: gold and rose bellies, violet tops, the last blue on their backs;
  - the asphalt far off is a mirror for the sky, and a long shine runs down the middle of it to us.

HORIZON 330.  CAMERA: persp.Camera(330, 577): the lens is 270 cm above the road (a little above a
grown-up's head), so each row below the horizon is worth 1/270 px per cm more. The road is 6.2 m of
asphalt: 620 px wide at the bottom edge (x 90 to 710), nothing at all at (400, 330).

THE THREE TONES
  dark    the sagebrush and the near pole; the high sky and the backs of the clouds
  middle  the plain (plum and dusty rose), the near road (violet grey), the mesas
  light   the gold of the horizon, the bellies of the clouds, the shine running down the road: all of
          it gathered round the place where the road ends, which is where the story happens

WHERE THINGS ARE
  the sun's place          (400, 330), r 25: NOT painted (its glow is); delivered as the cut-out sun.png
  the road                 asphalt between x = 400 -/+ 310 cm; broken yellow line down the middle
  the wagon's lane         the right-hand one: its middle is 150 cm right of the yellow line
                           (x 550 at the bottom edge, 521 at row 548 where the comp shows the wagon)
  telephone poles          left of the road, 7.5 m from its middle: the nearest stands at (67, 450) and
                           reaches to y 72; five more march to the sun; three birds on the top wire
  the road sign            right of the road: board x 599-752, y 286-378, on two posts down to y 455
  mesas                    violet, far left (x 0-300, a windpump in front of them) and far right (x 480-800)
  sagebrush, grass, stones everywhere off the road, biggest in the two bottom corners; fences far out
  left lying about         a strip of tire and a green bottle (left shoulder), a hubcap (right shoulder),
                           a tumbleweed against the sign's post, a jackrabbit watching from (235, 444)

Cut-outs: sun.png (soft-edged, RGBA), sign-bc.png (800x600: the board again, saying POINT B.C., laid over
the board; round twelve: the sign no longer gets a red slash and dripping letters, it is bent by the hole in time
and comes out changed, so the two edits are one plain cut-out), and the wagon seen from behind (highway_wagon.py): wagon-rear-0.png, wagon-rear-1.png, cropped to
their own box; layout.json says where its foot is and how big to draw it at each row.
"""

import json, math, os, sys, time

import numpy as np
from PIL import Image

from brush import *
import sky, land, persp, letter
from highway_kit import Paper, mix, grade

W, H = 800, 600
HZ = 330                                                    # the horizon
VX = 400                                                    # the road ends here
SUN = (400, 330, 25)
CAM = persp.Camera(HZ, 577, vanish_x=VX)                    # lens 270 cm up
ROAD = 310.0                                                # half the width of the asphalt, cm
LANE = 150.0                                                # the middle of the wagon's lane, cm right of the yellow line
SEED = 21


def px(cm_across, row):
    """Picture x of a place on the ground `cm_across` from the middle of the road, at picture row `row`."""
    return VX + cm_across * (row - HZ) / CAM.eye


def row_of(z_cm):
    """Picture row of the ground `z_cm` from the lens."""
    return HZ + CAM.eye * CAM.F / z_cm


# ---------------------------------------------------------------------------------------------- sky
def sunward(shape):
    """For every pixel: how far it is from the sun's place (flattened, so the glow is a wide low arch),
    and the unit direction from it to the sun."""
    x, y = grid(shape)
    dx, dy = VX - x, HZ - y
    far = np.hypot(dx / 1.75, dy)
    n = np.hypot(dx, dy) + 1e-6
    return far, dx / n, dy / n


def open_sky(shape, seed):
    """The sky with no clouds in it: indigo overhead, through violet and rose to gold where the sun went."""
    x, y = grid(shape)
    far, _, _ = sunward(shape)
    stops = [(0.0, "#14164a"), (0.18, "#1e1f60"), (0.36, "#32297c"), (0.52, "#57358c"), (0.66, "#8f4692"),
             (0.78, "#c95a80"), (0.88, "#ee7c5c"), (0.95, "#fba452"), (1.0, "#ffc868")]
    pic = sky.field(shape, HZ, stops, seed, patch=0.05)
    # the light is not in level bands: it is an arch over the place where the sun is
    arch = np.exp(-(far / 170.0) ** 1.6)
    warm = ramp(np.clip(1 - far / 250.0, 0, 1), [(0.0, "#c2567e"), (0.30, "#ee6e5a"), (0.58, "#ff964a"), (0.82, "#ffb252"), (1.0, "#ffc264")])
    drift = 0.75 + 0.5 * noise(shape, (300, 90), seed + 3, 4)
    over(pic, warm, np.clip(arch * drift * 0.9, 0, 1) * (y < HZ + 2))
    core = np.exp(-(far / 64.0) ** 2)                                 # (the disc itself is a cut-out: round it the sky is gold, not white, so that it shows)
    glow(pic, "#ffd68c", (core * 0.30).astype(F32))
    # and the far corners overhead are deeper still
    corner = np.clip(((x - VX) / 400.0) ** 2 * 0.6 + np.clip((150 - y) / 150.0, 0, 1) * 0.5, 0, 1)
    tint(pic, "#6060aa", (corner * 0.45).astype(F32))
    return np.clip(pic, 0, 1).astype(F32)


HOT = ["#43296a", "#7a3272", "#c44a64", "#f67648", "#ffb650", "#fff0a4"]     # a cloud near the sun: plum body, fire underneath
COOL = ["#22225e", "#372b76", "#673b86", "#ae5088", "#ea8478", "#ffcc9c"]    # one far from it: indigo body, rose underneath
STOPS = [0.0, 0.26, 0.46, 0.64, 0.82, 1.0]


def cloud_color(bright, heat):
    """The color of cloud that is `bright` (0 shade .. 1 full in the light) and `heat` (0 far from the sun .. 1 beside it)."""
    hot = ramp(bright, list(zip(STOPS, HOT)))
    cool = ramp(bright, list(zip(STOPS, COOL)))
    return lerp(cool, hot, heat[..., None])


def bank(shape, spine, count, size, seed, flat=0.6, pile=0.9, ragged=1.0, taper=0.6):
    """A bank of cloud lying along `spine` (a few points, left to right): round puffs heaped upward from a
    flattish base. -> thickness, 0 to 1."""
    rng = np.random.default_rng(seed)
    h, w = shape
    pts = curve(spine, 14)
    n = len(pts)
    T = np.zeros(shape, dtype=F32)
    for i in range(count):
        t = rng.random()
        j = min(int(t * (n - 1)), n - 2)
        f = t * (n - 1) - j
        cx, cy = lerp(pts[j][0], pts[j + 1][0], f), lerp(pts[j][1], pts[j + 1][1], f)
        mid = math.sin(math.pi * t) ** taper                        # biggest in the middle of the bank
        r = size * (0.30 + 0.70 * rng.random()) * (0.40 + 0.60 * mid)
        cy -= rng.random() ** 1.4 * size * pile * mid                # they pile upward
        cx += rng.normal(0, r * 0.35)
        rx, ry = r * 1.45, r * flat * 1.45
        x0, x1, y0, y1 = int(max(cx - rx - 1, 0)), int(min(cx + rx + 2, w)), int(max(cy - ry - 1, 0)), int(min(cy + ry + 2, h))
        if x1 <= x0 or y1 <= y0:
            continue
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(F32)
        d2 = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
        cap = np.sqrt(np.clip(1 - d2, 0, 1)) * (0.55 + 0.45 * r / size)
        T[y0:y1, x0:x1] = np.maximum(T[y0:y1, x0:x1], cap)
    # the base is nearly flat: cut the puffs off along a line a little under the spine
    x, y = grid(shape)
    line = np.interp(np.arange(w), [p[0] for p in pts], [p[1] for p in pts]).astype(F32)
    line = line + size * flat * 0.30 + (noise((1, w * 2), (70, 1), seed + 3, 3)[0, :w] - 0.5) * size * 0.30
    T = T * np.clip((line[None, :] - y) / (size * 0.10) + 0.5, 0, 1)
    # ragged: push it about, coarse then fine (never further than the noise can carry without tearing)
    a = size * 0.22 * ragged
    T = sample(T, x + (noise(shape, max(40.0, size * 1.6), seed + 11, 3) - 0.5) * 2 * a, y + (noise(shape, max(40.0, size * 1.6), seed + 12, 3) - 0.5) * 2 * a * 0.7)
    b = size * 0.07 * ragged
    T = sample(T, x + (noise(shape, max(10.0, size * 0.35), seed + 13, 3) - 0.5) * 2 * b, y + (noise(shape, max(10.0, size * 0.35), seed + 14, 3) - 0.5) * 2 * b)
    return np.clip(T, 0, 1).astype(F32)


def billow(shape, cell, seed, octaves=3):
    """Cauliflower: round domes with sharp creases between them. 0 in a crease, 1 on a dome."""
    total, weight, norm = np.zeros(shape, dtype=F32), 1.0, 0.0
    for o in range(octaves):
        n = noise(shape, max(4.0, cell / 2 ** o), seed + o * 7, 2)
        total += weight * np.abs(2 * n - 1)
        norm += weight
        weight *= 0.5
    out = total / norm
    lo, hi = np.percentile(out, (2, 98))
    return np.clip((out - lo) / (hi - lo + 1e-6), 0, 1).astype(F32)


def underlit(pic, T, size, seed, amount=1.0, depth=0.9, lift=0.0, sun=(VX, HZ + 50), crisp=1.0, puff=0.5):
    """Paint a cloud of thickness T lit from where the sun is. Light that has to pass through more cloud to
    reach a place arrives weaker, so the side toward the sun burns and the far side sinks into violet.
    `depth` is how far into the cloud the light gets, in cloud sizes: a cloud high overhead shows us its
    whole lit underside (deep), one near the horizon only a bright lower edge (shallow).
    -> (how bright each place is, the cloud's mask)"""
    shape = pic.shape[:2]
    x, y = grid(shape)
    dx, dy = sun[0] - x, sun[1] - y
    n = np.hypot(dx, dy) + 1e-6
    lx, ly = dx / n, dy / n
    relief = billow(shape, size * puff, seed + 17)                    # the cloud is made of round puffs
    lumpy = np.clip(T * (0.50 + 0.72 * relief), 0, 1)
    smooth_t = blur(T, max(1.0, size * 0.05))
    soft = blur(lumpy, max(0.8, size * 0.02))

    def passed(field, reach, steps):
        """How much cloud (in pixels of it) lies between each place and the sun, looking `reach` pixels that way."""
        total = np.zeros(shape, dtype=F32)
        for k in range(steps):
            d = reach * (k + 0.5) / steps
            total += sample(field, x + lx * d, y + ly * d)
        return total * reach / steps

    deep = np.exp(-passed(smooth_t, size * 3.2, 12) / (size * depth))     # the whole bank: lit below, dark above
    near = np.exp(-passed(soft, size * 0.45, 5) / (size * 0.16))          # and each puff in it: lit on its own sunward side
    gy, gx = np.gradient(blur(lumpy, max(1.0, size * 0.025)))
    inside = T > 0.05
    norm = (np.percentile(np.hypot(gx, gy)[inside], 88) + 1e-6) if inside.any() else 1.0
    slope = np.clip(-(gx * lx + gy * ly) / norm, -1, 1)
    top = np.clip(gy / norm, 0, 1)                                    # faces that look up at the high sky
    reach = 0.25 + 0.75 * deep
    bright = 0.05 + 0.56 * deep ** 0.75 + 0.20 * near * reach + 0.30 * slope * reach + lift
    bright -= (1 - relief) ** 2 * 0.16 * reach                        # the creases between puffs stay dim
    bright += (noise(shape, max(14.0, size * 0.5), seed + 21, 4) - 0.5) * 0.10
    bright = np.clip(bright, 0, 1)
    far, _, _ = sunward(shape)
    heat = np.clip(1.12 - far / 320.0, 0, 1)
    color = cloud_color(bright, heat)
    cool = (top * (1 - deep) * 0.38)[..., None]                       # the last blue of the day on the shaded tops
    color = color * (1 - cool) + rgb("#6c70c4") * cool
    fray = 0.62 + 0.76 * noise(shape, max(12.0, size * 0.4), seed + 31, 4)
    body = smooth(np.clip((blur(T, 1.0) + (relief - 0.6) * 0.16 * (T > 0.01)) * 3.2 * fray, 0, 1))      # a scalloped outline
    edge = lerp(blur(body, max(2.0, size * 0.07)) * 0.92, body, np.clip(bright * 1.6 * crisp, 0, 1)) * amount
    edge = np.clip(edge, 0, 1).astype(F32)
    over(pic, color, edge)
    return bright, edge, (top * (1 - deep) * edge).astype(F32)


def deck(pic, seed, cover=0.52, amount=1.0, top=0.0, bottom=1.0, scale=1.0, lift=0.0):
    """A ceiling of broken cloud seen from underneath, in perspective: broad rafts overhead that thin to
    level bars toward the horizon. Each raft is lit on the edge that is toward the sun."""
    shape = pic.shape[:2]
    x, y = grid(shape)
    far, sx, sy = sunward(shape)
    up = np.clip((HZ - y) / HZ, 0.0, 1.3)
    away = 1.0 / (up + 0.13)
    size = 1024
    tile = noise((size, size), 56 * scale, seed, 5, gain=0.55)
    u = np.clip((x - VX) * away * 0.15 + size / 2, 1, size - 3)
    v = np.clip(away * 112.0 + 20, 1, size - 3)
    n = sample(tile, u, v)
    n = n + (noise(shape, (90, 30), seed + 5, 3) - 0.5) * 0.10
    thick = step(cover, cover + 0.20, n)
    gy, gx = np.gradient(blur(n, 2.0))
    slope = -(gx * sx + gy * sy)
    slope = np.clip(slope / (np.percentile(np.abs(slope), 97) + 1e-6), -1, 1)
    inner = step(cover + 0.02, cover + 0.34, n)                       # the thick middle of a raft is in its own shade
    bright = np.clip(0.50 + 0.50 * slope - 0.30 * inner + (1 - inner) * 0.16 + lift, 0, 1)
    heat = np.clip(1.15 - far / 330.0, 0, 1)
    color = cloud_color(bright, heat)
    band = step(top, top + 0.12, y / HZ) * (1 - step(bottom - 0.05, bottom, y / HZ))
    over(pic, color, np.clip(blur(thick, 0.8) * band * amount, 0, 1).astype(F32))
    return pic


BANKS = [   # spine, puffs, size, flat, pile, lift, depth
    ([(-60, 150), (90, 168), (260, 196), (452, 222)], 110, 60, 0.62, 1.2, 0.0, 1.05),     # the great bank from the upper left, its base running down toward the sun
    ([(552, 138), (680, 118), (850, 92)], 60, 44, 0.60, 1.0, 0.0, 1.0),                   # its answer on the right
    ([(604, 214), (690, 208), (790, 196)], 26, 21, 0.55, 0.8, 0.04, 0.8),                 # a small one lower right
    ([(292, 78), (372, 70), (452, 76)], 16, 17, 0.55, 0.7, 0.0, 1.0),                     # high, small, almost in the dark already
    ([(470, 172), (520, 166), (566, 170)], 12, 13, 0.55, 0.7, 0.03, 0.9),                 # a scrap between the two big ones
    ([(150, 44), (200, 40), (246, 46)], 9, 11, 0.5, 0.6, 0.0, 1.0),                       # and a higher scrap
    ([(-20, 258), (110, 262), (250, 270)], 26, 15, 0.42, 0.7, 0.06, 0.6),                 # level bars low down
    ([(486, 274), (610, 268), (742, 262), (830, 262)], 30, 13, 0.40, 0.7, 0.08, 0.6),
    ([(300, 300), (400, 297), (520, 301)], 16, 7, 0.36, 0.6, 0.10, 0.5),
]


def cirrus(pic, seed):
    """Mares' tails very high up, still in the sun when everything under them has lost it: thin, combed,
    slanting up and away from the place where the sun went."""
    shape = pic.shape[:2]
    x, y = grid(shape)
    for k, (cx, cy, length, slope, tone, amount) in enumerate([(560, 58, 300, -0.16, "#b65a96", 0.50), (120, 34, 220, 0.10, "#8a4c9c", 0.40), (690, 172, 200, -0.10, "#e2708a", 0.40), (330, 122, 180, 0.05, "#c46092", 0.30)]):
        u = (x - cx) / length
        v = (y - cy - (x - cx) * slope) / 9.0
        comb = noise(shape, (120, 3.2), seed + k * 5, 3)
        v = v + (noise(shape, (160, 40), seed + k * 5 + 1, 2) - 0.5) * 3.0
        m = np.clip(1 - u * u, 0, 1) ** 1.5 * np.exp(-v * v) * step(0.42, 0.72, comb)
        over(pic, tone, np.clip(blur(m.astype(F32), 0.8) * amount, 0, 1))
    return pic


def the_sky(shape, seed):
    """-> (the sky, a mask of the burning edges of its clouds, to be said again crisply after the brushwork)"""
    pic = open_sky(shape, seed)
    cirrus(pic, seed + 30)
    deck(pic, seed + 40, cover=0.62, amount=0.8, top=0.62, bottom=0.99, scale=0.8)      # far-off streaks first
    hot = np.zeros(shape, dtype=F32)
    cover = np.zeros(shape, dtype=F32)
    for k, (spine, count, size, flat, pile, lift, depth) in enumerate(BANKS):
        T = bank(shape, spine, count, size, seed + 60 + k * 9, flat=flat, pile=pile)
        bright, edge, tops = underlit(pic, T, size, seed + 60 + k * 9, lift=lift, depth=depth)
        hot = np.maximum(hot * (1 - edge), np.maximum(step(0.62, 0.86, bright), tops * 0.8) * edge)
        cover = np.maximum(cover, edge)
    return np.clip(pic, 0, 1).astype(F32), hot, cover


# ---------------------------------------------------------------------------------------------- land
def P(across, up, z):
    """World (cm across from the yellow line, cm up, cm from the lens) -> picture."""
    return CAM.pt(across, up, z - CAM.Z0)


MESAS_FAR = ([(0, 316), (60, 312), (120, 318), (190, 314), (250, 322), (300, 325), (338, 329), (360, 331)],
             [(446, 331), (470, 328), (520, 322), (580, 318), (650, 321), (720, 314), (800, 316)])
MESAS = ([(0, 281), (30, 279), (98, 278), (110, 281), (116, 293), (132, 303), (150, 310), (170, 312), (177, 301), (182, 298), (204, 298), (209, 302), (216, 313), (240, 321), (272, 326), (300, 331)],
         [(480, 331), (504, 325), (518, 312), (524, 304), (530, 302), (574, 301), (580, 304), (590, 316), (640, 320), (700, 317), (722, 300), (730, 292), (800, 290)])
POLES = [(-750.0, 1800.0 + 4000.0 * i) for i in range(6)]            # across, from the lens (cm): the nearest first
POLE_H = 850.0
SIGN = dict(z=1730.0, x0=430.0, x1=760.0, lo=170.0, hi=362.0, posts=(486.0, 706.0), slant=0.022)     # the board, in cm: across, and above the ground


def bushes(seed):
    """Where the sagebrush stands: (across cm, from the lens cm, width cm, height cm, seed), far ones first.
    It grows in drifts, with bare ground between."""
    rng = np.random.default_rng(seed)
    drift = noise((256, 256), 26, seed + 1, 3)                      # one cell of this is about 12 m of desert
    out = []
    tries = 0
    while len(out) < 430 and tries < 20000:
        tries += 1
        z = 900.0 + rng.random() ** 1.35 * 15000.0
        half = 400.0 * z / CAM.F                                     # how far to the side the picture reaches at that distance
        side = -1 if rng.random() < 0.5 else 1
        across = side * (455.0 + rng.random() * max(half + 150.0 - 455.0, 0.0))
        if abs(across) > half + 120:
            continue
        d = drift[int(z / 46.0) % 256, int(across / 46.0 + 128) % 256]
        if rng.random() > step(0.36, 0.60, d) * 0.95 + 0.05:
            continue
        wide = 60.0 + rng.random() ** 1.5 * 110.0
        tall = wide * (0.55 + 0.3 * rng.random())
        # keep clear of the poles' feet, the sign's posts, and the two front corners (big ones are placed by hand there)
        if any(abs(across - px_) < 110 and abs(z - pz) < 160 for px_, pz in POLES):
            continue
        if SIGN["x0"] - 120 < across < SIGN["x1"] + 120 and abs(z - SIGN["z"]) < 420:
            continue
        if z < 1500:
            continue
        out.append((across, z, wide, tall, int(rng.integers(1 << 30))))
    out += [(-428.0, 880.0, 150.0, 104.0, 5), (-545.0, 1160.0, 118.0, 82.0, 6), (436.0, 858.0, 140.0, 98.0, 7), (556.0, 1105.0, 110.0, 78.0, 8),
            (-700.0, 1420.0, 150.0, 100.0, 9), (640.0, 1340.0, 130.0, 92.0, 10), (-600.0, 1700.0, 100.0, 70.0, 11), (505.0, 1420.0, 84.0, 56.0, 12)]
    return sorted(out, key=lambda b: -b[1])


def shadows(shape, seed, reach=5.5):
    """Every shadow on the plain, as a mask: each runs TOWARD us from the thing's foot, along the line from
    the sun's place through it. `reach` is how many times its own height a bush's shadow runs."""
    shade = Paper(shape)
    for (ax, z, wide, tall, k) in bushes(seed + 200):
        s = CAM.F / z
        fy = HZ + CAM.eye * s
        z1 = max(z - tall * reach, 420.0)
        s1 = CAM.F / z1
        y1 = HZ + CAM.eye * s1
        hw = wide * 0.42
        zm = (z + z1) / 2
        sm = CAM.F / zm
        ym = HZ + CAM.eye * sm
        shade.poly([(VX + (ax - hw) * s, fy - 1), (VX + (ax + hw) * s, fy - 1), (VX + (ax + hw * 0.8) * sm, ym), (VX + (ax - hw * 0.8) * sm, ym)], "#000000")
        shade.poly([(VX + (ax - hw * 0.8) * sm, ym), (VX + (ax + hw * 0.8) * sm, ym), (VX + (ax + hw * 0.5) * s1, y1), (VX + (ax - hw * 0.5) * s1, y1)], "#000000", 0.5)
    for (ax, z) in POLES:                                           # the poles
        s = CAM.F / z
        z1 = max(z - 2600.0, 380.0)
        s1 = CAM.F / z1
        shade.poly([(VX + (ax - 16) * s, HZ + CAM.eye * s), (VX + (ax + 16) * s, HZ + CAM.eye * s), (VX + (ax + 16) * s1, HZ + CAM.eye * s1), (VX + (ax - 16) * s1, HZ + CAM.eye * s1)], "#000000", 0.85)
    for ax in SIGN["posts"]:                                        # the sign's posts
        z = SIGN["z"]
        s, s1 = CAM.F / z, CAM.F / 500.0
        shade.poly([(VX + (ax - 8) * s, HZ + CAM.eye * s), (VX + (ax + 8) * s, HZ + CAM.eye * s), (VX + (ax + 8) * s1, HZ + CAM.eye * s1), (VX + (ax - 8) * s1, HZ + CAM.eye * s1)], "#000000", 0.85)
    return shade.done()[1]


def under(seed=SEED):
    """Everything broad and soft: the sky and its clouds, the far mesas, the plain, the road as a ribbon of
    reflected sky, and the long shadows. No small things."""
    shape = (H, W)
    x, y = grid(shape)
    info = {}
    pic, hot, cover = the_sky(shape, seed)
    info.update(sky=pic.copy(), hot=hot, cloud=cover)
    far, _, _ = sunward(shape)
    heat = np.clip(1.1 - np.abs(x - VX) / 420.0, 0, 1)                # how near the sun's side of the picture

    # ---- the far ranges: pale and rosy where the dust is lit, then the mesas proper in violet
    for k, pts in enumerate(MESAS_FAR):
        m, line = land.ridge(shape, pts, HZ + 2, seed + 100 + k, rough=1.2)
        up = np.clip((HZ - y) / 18.0, 0, 1)
        col = lerp(ramp(up, [(0.0, "#e79a78"), (1.0, "#b0688e")]), ramp(up, [(0.0, "#ffc47c"), (1.0, "#d8787c")]), (heat ** 2)[..., None])
        over(pic, col, m)
    lines = []
    for k, pts in enumerate(MESAS):
        m, line = land.ridge(shape, pts, HZ + 2, seed + 110 + k, rough=1.0)
        lines.append(line)
        up = np.clip((HZ - y) / 44.0, 0, 1)
        col = lerp(ramp(up, [(0.0, "#a8607e"), (0.45, "#74468a"), (1.0, "#553a86")]), ramp(up, [(0.0, "#f0a070"), (0.5, "#b05a7c"), (1.0, "#7a4484")]), (heat ** 2.5)[..., None])
        col = col * (1 + (noise(shape, (7, 40), seed + 120 + k, 3) - 0.5)[..., None] * 0.14)     # gullies down the cliffs
        over(pic, np.clip(col, 0, 1), m)
        foot = np.clip(1 - (HZ - y) / 13.0, 0, 1) ** 1.5 * m * (y <= HZ)
        over(pic, lerp(rgb("#d8907c"), rgb("#ffc27e"), (heat ** 2)[..., None]), (foot * 0.85).astype(F32))
    info.update(mesa_lines=lines)

    # ---- the plain: glowing dust at the horizon, dusty rose in the middle distance, plum at our feet
    ground = np.clip(y - HZ + 0.5, 0, 1).astype(F32)
    near = np.clip((y - HZ) / (H - HZ), 0, 1)
    flat = ramp(near ** 0.5, [(0.0, "#f4b27c"), (0.10, "#d48c74"), (0.24, "#a2626a"), (0.50, "#774862"), (1.0, "#523252")])
    blot = land.texture(shape, HZ, seed + 40, 150.0, 4) - 0.5
    fine = land.texture(shape, HZ, seed + 41, 30.0, 3) - 0.5
    flat = flat * (1 + blot[..., None] * 0.22 + fine[..., None] * 0.12)
    k = (noise(shape, (340, 90), seed + 42, 3) - 0.5) * 0.07       # warmer and cooler drifts, as when a wash is not quite mixed
    flat[..., 0] += k
    flat[..., 2] -= k * 0.8
    bare = land.texture(shape, HZ, seed + 43, 260.0, 3, stretch=0.5)                              # paler flats where nothing grows
    pale = ramp(near ** 0.5, [(0.0, "#ffc890"), (0.2, "#cf9080"), (0.5, "#a06e78"), (1.0, "#7c5468")])
    flat = lerp(flat, pale, (step(0.50, 0.85, bare) * 0.6)[..., None])
    flat = np.clip(flat, 0, 1).astype(F32)
    over(pic, flat, ground)
    glow(pic, "#ffc880", (np.exp(-((y - HZ) / 16.0) ** 2) * (0.22 + 0.42 * heat) * ground).astype(F32))   # the dust in the air is on fire
    glow(pic, "#ffd08a", (np.exp(-(far / 70.0) ** 2) * 0.40 * ground).astype(F32))

    # ---- the shoulders, and the road between them
    wob = (land.texture(shape, HZ, seed + 46, 60.0, 3) - 0.5)
    across = (x - VX) * CAM.eye / np.maximum(y - HZ, 0.5)                                         # cm from the yellow line, for every pixel of ground
    side = np.abs(across)
    sh_in, sh_out = ROAD - 6 + wob * 26, ROAD + 120 + wob * 150 + (noise(shape, (90, 26), seed + 47, 3) - 0.5) * 120
    soft = np.maximum(CAM.eye / np.maximum(y - HZ, 0.5) * 0.9, 1.0)                               # one pixel, in cm, at this row
    shoulder = np.clip((side - sh_in) / soft, 0, 1) * np.clip((sh_out - side) / (soft * 6), 0, 1) * ground
    sand = ramp(near ** 0.6, [(0.0, "#ffd49a"), (0.15, "#e2a488"), (0.5, "#b4847c"), (1.0, "#8c6670")])
    sand = sand * (1 + (land.texture(shape, HZ, seed + 48, 22.0, 3) - 0.5)[..., None] * 0.20)
    over(pic, np.clip(sand, 0, 1), (shoulder * 0.92).astype(F32))
    road = (np.clip((ROAD + wob * 9 - side) / soft + 0.5, 0, 1) * ground).astype(F32)
    tar = ramp(near ** 0.55, [(0.0, "#ffca8a"), (0.10, "#eaa884"), (0.24, "#b98c94"), (0.5, "#877394"), (1.0, "#625a7e")])
    blot = land.texture(shape, HZ, seed + 50, 120.0, 4) - 0.5
    fine = land.texture(shape, HZ, seed + 51, 16.0, 3) - 0.5
    tar = tar * (1 + blot[..., None] * 0.16 + fine[..., None] * 0.10)
    # the wheels have polished two tracks in each lane, and oil has dripped between them
    for lane in (-155.0, 155.0):
        for off in (-78.0, 78.0):
            trk = np.exp(-((across - lane - off) / 30.0) ** 2)
            tar = tar * (1 + (trk * 0.10)[..., None])
        tar = tar * (1 - (np.exp(-((across - lane) / 26.0) ** 2) * 0.10 * (0.5 + noise(shape, (30, 80), seed + 52, 3)))[..., None])
    over(pic, np.clip(tar, 0, 1), road)
    blown = step(0.56, 0.84, land.texture(shape, HZ, seed + 55, 80.0, 3)) * np.exp(-((side - ROAD) / 46.0) ** 2) * road      # sand has blown in over the edge here and there
    over(pic, np.clip(sand, 0, 1), np.clip(blown * 0.62, 0, 1).astype(F32))
    info.update(road=road, shoulder=shoulder, across=across, ground=ground)

    # ---- the sun lies along the road: a long shine straight down the middle, broken by the surface
    streak = land.texture(shape, HZ, seed + 53, 40.0, 3, stretch=0.25)
    width = 22.0 + 120.0 * near
    shine = np.exp(-(across / width) ** 2) * (1 - near) ** 1.05 * (0.50 + 1.0 * streak) * road
    glow(pic, "#ffdc9a", np.clip(shine * 1.15, 0, 1).astype(F32))
    for lane in (-155.0, 155.0):
        for off in (-78.0, 78.0):
            trk = np.exp(-((across - lane - off) / 22.0) ** 2) * (1 - near) ** 0.8 * road * (0.4 + 0.9 * streak)
            glow(pic, "#ffc890", np.clip(trk * 0.40, 0, 1).astype(F32))
    info.update(shine=np.clip(shine, 0, 1).astype(F32))

    # ---- long shadows, every one of them running toward us from the sun's place
    sm = shadows(shape, seed, 5.5)
    sm = lerp(sm, blur(sm, 3.0), np.clip(near * 1.2, 0, 1))
    tint(pic, "#5c4a86", (np.clip(sm, 0, 1) * 0.50 * ground).astype(F32))

    # ---- the corners go deeper, to hold the eye on the road and the light at the end of it
    corner = np.clip((np.abs(x - VX) / 400.0) ** 2.2 * 0.55 + ((y - 430) / 170.0).clip(0, 2) ** 2 * 0.40, 0, 1)
    tint(pic, "#6a4a78", (corner * 0.55 * ground).astype(F32))
    return np.clip(pic, 0, 1), info


# ---------------------------------------------------------------------------------------------- small things
def fat(m, by=1.0):
    """Thicken a lettering mask by about `by` pixels, as paint spreads."""
    return np.clip((blur(m, by) - 0.22) * 3.6, 0, 1).astype(F32)


def airy(color, row, amount=1.0):
    """A thing's color as the dusty air between changes it: far off (near the horizon) it goes pale and warm."""
    t = np.clip(1 - (row - HZ) / 110.0, 0, 1) ** 1.7 * 0.72 * amount
    return mix(color, "#f2a878", t)


def sage(sheet, fx, fy, w, h, seed, side):
    """A sagebrush with the middle of its foot at (fx, fy), seen against the light: a dark, cool mass of
    rounded clumps, silvery where the sky lights their crowns, with the sun coming over the top of each
    as a thin broken line of gold and a few lit twig-ends. `side` is -1 when the sun is to its left,
    +1 to its right. One in six is rabbitbrush instead: rounder, with a dusting of yellow bloom."""
    rng = np.random.default_rng(seed)
    bloom = rng.random() < 0.16
    dry = (not bloom) and rng.random() < 0.10
    dark = airy("#3a2a34" if dry else "#241f3a", fy)
    mid = airy("#5a4648" if dry else ("#3d4a4e" if bloom else "#3b4558"), fy)
    lite = airy("#8a6a5c" if dry else ("#6c7c62" if bloom else "#66787e"), fy)
    rim, fire = airy("#e2924e", fy, 0.5), airy("#ffd98c", fy, 0.3)
    if w < 7:                                                      # far off it is a dab and a spark
        sheet.ellipse(fx, fy - h * 0.5, w * 0.5, h * 0.5, dark, 0.9)
        sheet.line([(fx - w * 0.3, fy - h * 0.95), (fx + w * 0.3, fy - h * 0.95)], rim, max(0.7, h * 0.14), 0.75)
        return
    lobes = []
    for i in range(4 + int(w / 13)):
        u = rng.uniform(-0.5, 0.5)
        top = h * (0.60 + 0.42 * rng.random()) * (1 - 0.55 * (2 * u) ** 2)
        r = w * (0.15 + 0.11 * rng.random())
        lobes.append((fx + u * w * 0.86, fy - top + r * 0.5, r, rng.random()))

    def buried(px_, py_, me):                                      # is this place inside some other clump?
        return any(k != me and ((px_ - lx) / (r * 1.12)) ** 2 + ((py_ - ly) / (r * 0.94)) ** 2 < 1 for k, (lx, ly, r, d) in enumerate(lobes))

    # the woody stems, splaying from the root
    for i in range(3 + int(w / 30)):
        tx = fx + rng.uniform(-0.36, 0.36) * w
        sheet.taper(curve([(fx + rng.normal(0, w * 0.04), fy), ((fx + tx) / 2 + rng.normal(0, w * 0.04), fy - h * 0.22), (tx, fy - h * 0.5)], 4), dark, max(1.0, w * 0.035), max(0.7, w * 0.012))
    sheet.poly([(fx - w * 0.30, fy), (fx - w * 0.44, fy - h * 0.34), (fx + w * 0.44, fy - h * 0.34), (fx + w * 0.30, fy)], dark)
    order = sorted(range(len(lobes)), key=lambda k: lobes[k][3])
    thin = max(0.8, w * 0.014)
    glowing = mix(dark, rim, 0.40)
    for k in order:                                                # the clumps, far ones first
        lx, ly, r, d = lobes[k]
        sheet.ellipse(lx, ly, r * 1.12, r * 0.92, dark)
        for i in range(int(7 + r * 1.3)):                          # a ragged edge: dark leaves standing out of it all round the top
            t = math.radians(rng.uniform(-10, 190))
            ex, ey = lx + math.cos(t) * r * 1.06, ly - math.sin(t) * r * 0.86
            ln = r * rng.uniform(0.14, 0.34)
            sheet.line([(ex, ey), (ex + math.cos(t) * ln * 0.7 + rng.normal(0, ln * 0.3), ey - math.sin(t) * ln * 0.7 - ln * 0.35)], dark, thin * 1.5)
        for i in range(int(9 + r * 2.4)):                          # leaves: short dabs, palest on the crown where the sky is on them
            px_, py_ = lx + rng.normal(0, r * 0.46), ly + rng.normal(0, r * 0.36) - r * 0.14
            if ((px_ - lx) / (r * 1.05)) ** 2 + ((py_ - ly) / (r * 0.86)) ** 2 > 1:
                continue
            high = float(np.clip((ly + r * 0.4 - py_) / (r * 1.2), 0, 1))
            tone = mix(dark, mid, 0.25 + 0.75 * rng.random()) if rng.random() < 0.45 else mix(mid, lite, high * rng.random() ** 0.7)
            a = math.radians(rng.uniform(20, 160))
            ln = r * rng.uniform(0.12, 0.28)
            sheet.line([(px_, py_), (px_ + math.cos(a) * ln, py_ - math.sin(a) * ln)], tone, thin * 1.25)
        if w > 50:                                                 # near enough to see the silver of the small leaves on each crown
            for i in range(int(r * 3.2)):
                px_, py_ = lx + rng.normal(0, r * 0.40) - side * r * 0.08, ly - abs(rng.normal(0, r * 0.34)) - r * 0.02
                if ((px_ - lx) / (r * 1.0)) ** 2 + ((py_ - ly) / (r * 0.82)) ** 2 > 1:
                    continue
                a = math.radians(rng.uniform(30, 150))
                ln = r * rng.uniform(0.07, 0.15)
                sheet.line([(px_, py_), (px_ + math.cos(a) * ln, py_ - math.sin(a) * ln)], mix(mid, lite, 0.5 + 0.5 * rng.random()), max(0.8, thin * 0.8))
    expo = 0.30 + 0.70 * rng.random() ** 0.7                       # some stand in the shade of others, and get little of it
    for k in order:                                                # the sun comes over the top: lit leaves all along the upper edge, thickest toward the sun
        lx, ly, r, d = lobes[k]
        for i in range(int(12 + r * 2.8)):
            t = math.radians(rng.uniform(12, 168))
            toward = math.cos(t) * side                            # +1 on the side toward the sun
            if rng.random() > (0.52 + 0.42 * toward) * expo:
                continue
            rr = rng.uniform(0.94, 1.14)
            ex, ey = lx + math.cos(t) * r * 1.10 * rr, ly - math.sin(t) * r * 0.90 * rr
            if buried(ex, ey - 1.0, k):
                continue
            ln = r * rng.uniform(0.07, 0.22)
            ang = t + rng.normal(0, 0.6)
            inner = rr < 1.0
            hot = (not inner) and rng.random() < 0.30 + 0.25 * toward
            tone = glowing if inner else (fire if hot else rim)
            sheet.line([(ex, ey), (ex + math.cos(ang) * ln * 0.8, ey - abs(math.sin(ang)) * ln)], tone, thin * (1.5 if hot else 1.25), 0.96)
        if bloom:                                                  # rabbitbrush: its crown is dusted with yellow
            for i in range(int(3 + r * 0.7)):
                t = math.radians(rng.uniform(25, 155))
                rr = rng.uniform(0.5, 1.0)
                bx_, by_ = lx + math.cos(t) * r * 1.05 * rr, ly - math.sin(t) * r * 0.86 * rr
                sheet.ellipse(bx_, by_, max(0.6, thin * 0.9), max(0.6, thin * 0.8), airy("#d9a246" if rng.random() < 0.65 else "#ffd870", fy, 0.4), 0.95)
    for i in range(int(1 + w / 26)):                               # last year's flower stalks stand up out of it, lit
        k = int(rng.integers(len(lobes)))
        lx, ly, r, d = lobes[k]
        sx_ = lx + rng.normal(0, r * 0.5)
        if buried(sx_, ly - r * 1.0, k):
            continue
        sheet.line([(sx_, ly - r * 0.7), (sx_ + rng.normal(0, r * 0.15), ly - r * (1.25 + 0.5 * rng.random()))], rim, max(0.7, w * 0.009), 0.8)


def tuft(sheet, fx, fy, r, seed, side):
    """Dry grass with the low sun behind it: it glows like a lamp wick."""
    rng = np.random.default_rng(seed)
    cols = (airy("#4a3040", fy), airy("#a06c4c", fy, 0.6), airy("#f6c078", fy, 0.3))
    for k in range(int(7 + r * 0.9)):
        a = math.radians(rng.uniform(35, 145))
        ln = r * (0.5 + 0.7 * rng.random())
        bx_ = fx + rng.normal(0, r * 0.22)
        t = rng.random()
        tone = cols[0] if t < 0.4 else (cols[1] if t < 0.8 else cols[2])
        sheet.line(curve([(bx_, fy), (bx_ + math.cos(a) * ln * 0.5, fy - math.sin(a) * ln * 0.6), (bx_ + math.cos(a) * ln + side * ln * 0.12, fy - math.sin(a) * ln * 0.95)], 3), tone, max(0.7, r * 0.07), 0.95)


def stone(sheet, fx, fy, rx, ry, seed, side):
    """A stone on the ground: dark toward us, a paler plane turned to the sky, and a bright edge along
    the top where the sun reaches over it."""
    rng = np.random.default_rng(seed)
    n = 8
    pts = []
    for i in range(n):
        a = math.pi * 2 * i / n + rng.normal(0, 0.16)
        r = 0.78 + 0.3 * rng.random()
        pts.append((fx + math.cos(a) * rx * r, min(fy - ry + math.sin(a) * ry * r, fy + ry * 0.05)))
    cx, cy = fx, fy - ry
    sheet.poly(pts, airy("#3e2f52", fy))
    sheet.poly([(cx + (p[0] - cx) * 0.74 - side * rx * 0.08, cy + (p[1] - cy) * 0.5 - ry * 0.30) for p in pts], airy("#66506e", fy))
    top = sorted(sorted(pts, key=lambda p: p[1])[:3], key=lambda p: p[0])
    if rx > 1.6:
        sheet.line([(p[0], p[1] + 0.5) for p in top], airy("#f6b878", fy, 0.4), max(0.7, ry * 0.16), 0.9)


def bird(sheet, bx, by, size, facing=1):
    """A small bird on a wire, against the sky: a dab for the body, a dot for the head, a tail."""
    dark = "#221a30"
    sheet.ellipse(bx, by - size * 0.50, size * 0.36, size * 0.48, dark)
    sheet.ellipse(bx + facing * size * 0.16, by - size * 1.02, size * 0.25, size * 0.24, dark)
    sheet.line([(bx - facing * size * 0.10, by - size * 0.2), (bx - facing * size * 0.42, by + size * 0.42)], dark, max(0.9, size * 0.20))
    sheet.line([(bx + facing * size * 0.36, by - size * 1.0), (bx + facing * size * 0.58, by - size * 0.94)], dark, 0.8)
    sheet.line([(bx + size * 0.30, by - size * 0.80), (bx + size * 0.36, by - size * 0.30)], "#f09a58", 0.8, 0.9)        # the sun on its breast


def windpump(sheet, across, z, seed):
    """A ranch windpump far out on the flat, and the stock tank beside it: tiny, against the last light."""
    s = CAM.F / z
    foot = P(across, 0, z)
    tone, lit = airy("#33264c", foot[1], 0.55), "#ffd08a"
    for sgn in (-1, 1):
        sheet.line([P(across + sgn * 120, 0, z), P(across + sgn * 16, 930, z)], tone, 0.9)
    for (h0, h1) in ((120, 360), (360, 600), (600, 820)):
        w0, w1 = 120 - 104 * h0 / 930, 120 - 104 * h1 / 930
        sheet.line([P(across - w0, h0, z), P(across + w1, h1, z)], tone, 0.6, 0.85)
        sheet.line([P(across + w0, h0, z), P(across - w1, h1, z)], tone, 0.6, 0.85)
    hub = P(across, 985, z)
    r = 150 * s
    for i in range(12):
        a = math.pi * 2 * i / 12 + 0.2
        sheet.line([hub, (hub[0] + math.cos(a) * r, hub[1] + math.sin(a) * r)], tone, 0.8)
    sheet.line([(hub[0] + math.cos(a_) * r, hub[1] + math.sin(a_) * r) for a_ in np.linspace(0, math.pi * 2, 17)], tone, 0.8)
    sheet.line([(hub[0] + math.cos(a_) * r, hub[1] + math.sin(a_) * r) for a_ in np.linspace(-0.9, 0.5, 5)], lit, 0.8, 0.9)
    sheet.poly([hub, (hub[0] - r * 2.0, hub[1] - r * 0.5), (hub[0] - r * 2.3, hub[1] + r * 0.1), (hub[0] - r * 1.9, hub[1] + r * 0.55)], tone)
    t0, t1 = P(across + 300, 0, z), P(across + 640, 230, z)
    sheet.poly([(t0[0], t0[1]), (t1[0], t0[1]), (t1[0], t1[1]), (t0[0], t1[1])], tone)
    sheet.line([(t0[0], t1[1]), (t1[0], t1[1])], lit, 0.8, 0.9)


def tumbleweed(sheet, fx, fy, r, seed, side):
    """A tumbleweed that has fetched up against something: a ball of fine twigs with the light in it."""
    rng = np.random.default_rng(seed)
    cy = fy - r * 0.92
    sheet.ellipse(fx, cy, r * 0.90, r * 0.84, "#2c2238", 0.55)
    twigs = []
    for i in range(80):
        a0 = rng.uniform(0, math.pi * 2)
        rr = r * rng.uniform(0.25, 1.0)
        c0 = (fx + rng.normal(0, r * 0.2), cy + rng.normal(0, r * 0.2))
        pts = [(c0[0] + math.cos(a0 + t) * rr * 0.8, c0[1] + math.sin(a0 + t) * rr * 0.74) for t in np.linspace(0, rng.uniform(0.7, 1.9), 5)]
        pts = [p_ for p_ in pts if (p_[0] - fx) ** 2 + ((p_[1] - cy) * 1.08) ** 2 < (r * 1.04) ** 2]
        if len(pts) < 2:
            continue
        m = pts[len(pts) // 2]
        lit = (cy - m[1]) / r * 0.8 + (m[0] - fx) * side / r * 0.5 + rng.normal(0, 0.25)
        twigs.append((lit, pts))
    for lit, pts in sorted(twigs, key=lambda t_: t_[0]):
        tone = "#ffd690" if lit > 0.62 else ("#e09a56" if lit > 0.3 else ("#7a5448" if lit > -0.1 else "#3a2a38"))
        sheet.line(pts, tone, 0.8 if lit < 0.62 else 0.95, 0.95)


def jackrabbit(sheet, fx, fy, size, side):
    """A jackrabbit sitting up at the edge of the road, watching the car go by. The sun is in its ears."""
    k = size / 22.0
    dark, mid, lit = "#33283e", "#52405a", "#f6a868"
    f = side                                                        # it faces the road
    sheet.ellipse(fx - f * 2.2 * k, fy - 4.6 * k, 6.0 * k, 4.8 * k, dark)                     # the haunch
    sheet.ellipse(fx + f * 1.6 * k, fy - 7.6 * k, 4.4 * k, 5.6 * k, dark)                     # chest and back
    sheet.line([(fx + f * 3.6 * k, fy - 5.0 * k), (fx + f * 3.9 * k, fy - 0.2 * k)], dark, 2.0 * k)      # a foreleg
    sheet.line([(fx - f * 5.0 * k, fy - 0.8 * k), (fx + f * 0.6 * k, fy - 0.6 * k)], dark, 2.0 * k)      # the long hind foot
    sheet.ellipse(fx + f * 3.9 * k, fy - 13.6 * k, 3.5 * k, 2.9 * k, dark)                    # the head
    sheet.ellipse(fx + f * 6.4 * k, fy - 13.0 * k, 1.5 * k, 1.3 * k, dark)                    # the nose
    for (lean, ln) in ((-0.18, 10.5), (0.12, 9.6)):                                           # the ears
        base = (fx + f * (3.0 + lean * 4) * k, fy - 15.4 * k)
        tip = (base[0] - f * (0.8 - lean * 6) * k, base[1] - ln * k)
        sheet.taper([base, ((base[0] + tip[0]) / 2 - f * 0.5 * k, (base[1] + tip[1]) / 2), tip], dark, 2.3 * k, 1.1 * k)
        sheet.taper([(base[0] + f * 0.25 * k, base[1] - 1.5 * k), ((base[0] + tip[0]) / 2 - f * 0.25 * k, (base[1] + tip[1]) / 2), (tip[0] + f * 0.1 * k, tip[1] + 1.6 * k)], "#e8846a", 1.15 * k, 0.6 * k, 0.9)
    sheet.ellipse(fx - f * 7.6 * k, fy - 4.2 * k, 1.5 * k, 1.5 * k, "#8a7088")                # the scut
    sheet.ellipse(fx - f * 1.5 * k, fy - 5.4 * k, 3.0 * k, 2.4 * k, mid, 0.8)
    # the sun along its chest, its face and the front of its ears
    sheet.line([(fx + f * 5.3 * k, fy - 9.6 * k), (fx + f * 5.6 * k, fy - 6.2 * k), (fx + f * 4.9 * k, fy - 3.6 * k)], lit, 0.9, 0.9)
    sheet.line([(fx + f * 6.2 * k, fy - 15.2 * k), (fx + f * 7.6 * k, fy - 13.4 * k)], lit, 0.9, 0.95)
    sheet.ellipse(fx + f * 4.9 * k, fy - 14.3 * k, 0.6 * k, 0.6 * k, "#120c18")                # an eye


def pole(sheet, across, z, seed, arms=True, fade=1.0):
    """A telephone pole standing at (across, z): weathered wood against the sky, two crossarms, glass insulators."""
    rng = np.random.default_rng(seed)
    s = CAM.F / z
    lean = rng.normal(0, 0.012)
    foot = P(across, 0, z)
    topx = across + lean * POLE_H
    wood, edge, cool = mix("#2b1d30", "#f2a878", (1 - fade) * 0.8), mix("#f6a85a", "#ffe0a0", 1 - fade), "#57477c"
    w0, w1 = 15.0, 10.0                                              # half widths, cm
    a, b = P(across - w0, 0, z), P(across + w0, 0, z)
    c, d = P(topx + w1, POLE_H, z), P(topx - w1, POLE_H, z)
    sheet.poly([a, b, c, d], wood, fade)
    if s > 0.3:                                                       # the near one: we can see how the weather has opened the wood
        for i in range(9):
            u0 = rng.uniform(-0.75, 0.75)
            h0 = rng.uniform(30, POLE_H - 160)
            h1 = h0 + rng.uniform(60, 260)
            w_at = lambda hh: lerp(w0, w1, hh / POLE_H)
            sheet.line([P(across + lean * h0 + u0 * w_at(h0), h0, z), P(across + lean * h1 + (u0 + rng.normal(0, 0.06)) * w_at(h1), h1, z)],
                       "#1a1020" if rng.random() < 0.6 else "#4a3850", 0.8, 0.75)
        t0 = P(across - 7, 205, z)
        sheet.poly([t0, (t0[0] + s * 14, t0[1]), (t0[0] + s * 14, t0[1] + s * 20), (t0[0], t0[1] + s * 20)], "#7c7890")           # its number, on a tin tag
        sheet.line([(t0[0] + s * 3, t0[1] + s * 7), (t0[0] + s * 11, t0[1] + s * 7)], "#2a2236", 0.7, 0.8)
        sheet.line([(t0[0] + s * 3, t0[1] + s * 13), (t0[0] + s * 9, t0[1] + s * 13)], "#2a2236", 0.7, 0.8)
    if s > 0.05:
        sheet.line([b, c], edge, max(0.8, s * 5.5), 0.9 * fade)       # the sun finds the edge of it
        sheet.line([(a[0] + s * 3, a[1]), (d[0] + s * 3, d[1])], cool, max(0.7, s * 4.0), 0.45 * fade)
    out = []
    if arms:
        for (hgt, half, pegs) in ((790.0, 122.0, (-104.0, -58.0, 58.0, 104.0)), (712.0, 96.0, (-80.0, 80.0))):
            cx_ = across + lean * hgt
            l, r = P(cx_ - half, hgt, z), P(cx_ + half, hgt, z)
            thick = max(1.0, s * 12.0)
            sheet.line([l, r], wood, thick, fade)
            if s > 0.05:
                sheet.line([(l[0], l[1] - thick * 0.42), (r[0], r[1] - thick * 0.42)], edge, max(0.7, s * 3.0), 0.8 * fade)
                for sgn in (-1, 1):                                  # the braces
                    sheet.line([P(cx_ + sgn * half * 0.62, hgt - 4, z), P(cx_ + sgn * 4, hgt - 62, z)], wood, max(0.8, s * 4.0), fade)
            for pg in pegs:
                base, tip = P(cx_ + pg, hgt + 6, z), P(cx_ + pg, hgt + 30, z)
                sheet.line([base, tip], wood, max(0.8, s * 4.0), fade)
                if s > 0.05:
                    sheet.ellipse(tip[0], tip[1], max(0.9, s * 5.0), max(1.0, s * 6.4), "#4fb6a8", fade)             # old green glass, lit from behind
                    sheet.ellipse(tip[0], tip[1] + s * 2.4, max(0.8, s * 5.6), max(0.6, s * 2.2), "#2a6e70", fade)
                    sheet.ellipse(tip[0] + s * 1.2, tip[1] - s * 1.6, max(0.6, s * 2.0), max(0.6, s * 2.4), "#e6fff0", fade)
                out.append((cx_ + pg, hgt + 34.0))
    return out


def wires(sheet, seed):
    """The wires from pole to pole, sagging, and from the nearest pole out over our heads."""
    rng = np.random.default_rng(seed)
    pegs = [(-104.0, 824.0), (-58.0, 824.0), (58.0, 824.0), (104.0, 824.0), (-80.0, 746.0), (80.0, 746.0)]
    spans = [(POLES[i], POLES[i + 1]) for i in range(len(POLES) - 1)]
    spans = [((POLES[0][0], POLES[0][1] - 4000.0), POLES[0])] + spans
    runs = []
    for (a, b) in spans:
        for k, (dx, hgt) in enumerate(pegs):
            sag = 105.0 + 30.0 * math.sin(k * 1.7 + a[1] * 0.001)
            pts = []
            for i in range(25):
                u = i / 24
                z = lerp(a[1], b[1], u)
                if z < 430:
                    continue
                pts.append(P(lerp(a[0], b[0], u) + dx, hgt - 4 * sag * u * (1 - u), z))
            if len(pts) < 2:
                continue
            s = CAM.F / max(a[1], 600.0)
            fade = np.clip(1 - (pts[-1][0] - 330) / 50.0, 0.25, 1.0)             # lost in the glare toward the sun
            sheet.line(pts, "#2a1c36", max(0.75, min(1.5, s * 3.2)), 0.9 * fade)
            if k % 2 == 0 and s > 0.1:
                sheet.line(pts[len(pts) // 2:], "#f2a060", 0.7, 0.5)             # a thread of light along it
            runs.append(pts)
    return runs


def the_sign(pic, seed, letters=True, text="POINT B", size=31):
    """The road sign: a green board on two posts. -> its rectangle in the picture (x, y, w, h), and a function
    that turns a place on the board (0..1 across, 0..1 down) into a place in the picture. `text` is the first line
    of it (POINT B; after the hole in time has had its way with it, POINT B.C., in smaller letters to fit)."""
    shape = pic.shape[:2]
    S = SIGN
    s = CAM.F / S["z"]
    x0, y0 = P(S["x0"], S["hi"], S["z"])
    x1, y1 = P(S["x1"], S["lo"], S["z"])
    bw, bh = x1 - x0, y1 - y0

    def at(u, v):                                                   # the board hangs a little out of true
        return (x0 + u * bw, y0 + v * bh - (u - 0.5) * bw * S["slant"])

    sh = Paper(shape)
    for ax in S["posts"]:                                           # the posts: grey steel channel, lit along the edge toward the sun
        f, t = P(ax, -6, S["z"]), P(ax, S["hi"] - 10, S["z"])
        sh.line([f, t], "#3e3550", max(2.0, s * 11.0))
        sh.line([(f[0] + s * 2.5, f[1]), (t[0] + s * 2.5, t[1])], "#5d5674", max(1.0, s * 4.0))
        sh.line([(f[0] - s * 5.0, f[1]), (t[0] - s * 5.0, t[1])], "#f6b062", 1.0, 0.95)
    sh.onto(pic)
    # the board: laid on as paint, uneven, darker toward the top where the weather comes from
    r = 5.0
    outline = []
    for (cu, cv, a0) in ((0, 0, 180), (1, 0, 270), (1, 1, 0), (0, 1, 90)):
        cx_, cy_ = at(cu, cv)
        ox, oy = (r if cu == 0 else -r), (r if cv == 0 else -r)
        for i in range(5):
            a = math.radians(a0 + 90 * i / 4)
            outline.append((cx_ + ox + math.cos(a) * r, cy_ + oy + math.sin(a) * r))
    board = mask_poly(shape, outline, wobble=0.5, seed=seed)
    x, y = grid(shape)
    v = np.clip((y - y0) / bh, 0, 1)
    u = np.clip((x - x0) / bw, 0, 1)
    green = ramp(v, [(0.0, "#155440"), (0.45, "#1c6a4c"), (1.0, "#237a54")])
    green = green * (1 + (noise(shape, (7, 26), seed + 1, 3) - 0.5)[..., None] * 0.14 + (noise(shape, 30, seed + 2, 3) - 0.5)[..., None] * 0.12)
    green = green * (1 + ((1 - u) * 0.10)[..., None])              # the side toward the sun is a touch lighter
    over(pic, np.clip(green, 0, 1), board)
    info = dict(rect=[round(x0, 1), round(min(at(1, 0)[1], y0), 1), round(bw, 1), round(bh + abs(bw * S["slant"]), 1)], at=at, board=board, bw=bw, bh=bh)
    sh = Paper(shape)
    white = "#f1f0e2"
    inset = 4.2
    ring = []
    rr = 3.6
    for (cu, cv, a0) in ((0, 0, 180), (1, 0, 270), (1, 1, 0), (0, 1, 90)):
        cx_, cy_ = at(cu, cv)
        ox, oy = (inset + rr if cu == 0 else -inset - rr), (inset + rr if cv == 0 else -inset - rr)
        for i in range(5):
            a = math.radians(a0 + 90 * i / 4)
            ring.append((cx_ + ox + math.cos(a) * rr, cy_ + oy + math.sin(a) * rr))
    sh.line(ring + [ring[0]], white, 1.7, 0.92)
    for ax in S["posts"]:                                           # the bolts that hold it to its posts
        for hgt in (S["hi"] - 34, S["lo"] + 34):
            bx_, by_ = P(ax, hgt, S["z"])
            by_ -= ((bx_ - x0) / bw - 0.5) * bw * S["slant"]
            sh.ellipse(bx_, by_, 1.5, 1.5, "#c9d2c4")
            sh.ellipse(bx_ + 0.5, by_ + 0.6, 1.0, 1.0, "#0e3a2c", 0.7)
    sh.line([at(0.004, 0.02), at(0.996, 0.02)], "#ffc070", 1.3, 0.95)        # the sun catches its top edge, and the edge toward it
    sh.line([at(0.0, 0.03), at(0.0, 0.97)], "#ffb866", 1.2, 0.9)
    sh.line([at(1.0, 0.05), at(1.0, 0.97)], "#0c3628", 1.2, 0.8)
    sh.line([at(0.01, 0.995), at(0.99, 0.995)], "#0c3628", 1.2, 0.8)
    sh.onto(pic)
    if letters:
        cu, cv = at(0.5, 0.0)
        m1 = fat(letter.mask(shape, text, at(0.085, 0.31), size, anchor="lm", rough=0.35, spacing=1.6, slant=S["slant"], seed=seed + 3), 0.9)
        m2 = fat(letter.mask(shape, "40", at(0.915, 0.70), 37, anchor="rm", rough=0.35, spacing=2.0, slant=S["slant"], seed=seed + 4), 1.0)
        m = np.maximum(m1, m2) * (0.90 + 0.10 * noise(shape, 5, seed + 5, 2))
        over(pic, "#0f4332", np.clip(np.roll(np.roll(m, 1, axis=0), 1, axis=1) - m, 0, 1) * 0.5)
        over(pic, white, m * 0.96)
        ys_, xs_ = np.where(m1 > 0.5)
        info.update(point_b=m1, point_b_rect=[xs_.min(), ys_.min(), xs_.max() - xs_.min() + 1, ys_.max() - ys_.min() + 1])
    # weather: rust weeping from a bolt, and two holes somebody shot in it
    sh = Paper(shape)
    for (u_, v_) in ((0.80, 0.24), (0.62, 0.86)):
        hx, hy = at(u_, v_)
        sh.ellipse(hx, hy, 2.0, 2.0, "#0a241c")
        sh.ellipse(hx - 0.5, hy - 0.5, 2.6, 2.6, "#d8dccc", 0.0)
        sh.line([(hx - 2.4, hy - 1.2), (hx - 1.0, hy - 2.4)], "#dfe6d6", 0.8, 0.8)
        sh.line([(hx + 0.3, hy + 2.0), (hx + 0.6, hy + 7.0)], "#7a4a30", 0.9, 0.5)
    sh.onto(pic)
    return info


def stroke_mask(shape, pts, width, seed, dry=0.5):
    """One pass of a loaded brush through `pts`: fat where it lands, starved and streaky where it leaves."""
    x, y = grid(shape)
    n = len(pts)
    ws = [width * (1.0 - 0.45 * (i / (n - 1)) ** 2) * (0.9 + 0.2 * math.sin(i * 1.3 + seed)) for i in range(n)]
    m = mask_line(shape, pts, ws, soft=0.0)
    m = warp(m, 1.2, 7.0, seed)
    along = np.clip((x - pts[0][0]) / max(pts[-1][0] - pts[0][0], 1), 0, 1)
    hair = noise(shape, (46, 2.0), seed + 1, 2)                     # the bristles leave lanes
    m = m * (1 - step(0.50, 0.72, hair) * np.clip(along * 1.5 - 0.35, 0, 1) * dry)
    return np.clip(m, 0, 1).astype(F32)


def red_paint(shape, m, seed):
    """Thick red paint through a mask: -> (color, alpha), with a wet highlight and a dark edge."""
    body = np.empty(shape + (3,), dtype=F32)
    body[...] = rgb("#e2382a")
    body *= (1 + (noise(shape, (30, 3), seed, 3) - 0.5)[..., None] * 0.22)
    inner = blur(m, 1.6)
    over(body, "#9c1f1c", np.clip(1.0 - inner * 1.25, 0, 1) * 0.75)             # the edge of the paint is darker
    lit = np.clip(np.roll(inner, 1, axis=0) - inner, 0, 1) * 5                  # and its upper edge is wet
    over(body, "#ff8a6a", np.clip(lit, 0, 1) * 0.7)
    return np.clip(body, 0, 1), (m > 0.5).astype(F32)


def sign_after(pic, info, seed):
    """The sign once the hole in time has bent it (round twelve): the board painted again on a copy of the picture,
    saying POINT B.C. where it said POINT B, cut out along the board's own edge. -> (color, alpha). The game shows it
    over the backdrop, and the `portal` effect bends the one into the other."""
    after = pic.copy()
    the_sign(after, seed, text="POINT B.C.", size=24)
    board = info["board"]
    inner = board.copy()
    for dy in (-1, 0, 1):                                              # a pixel inside the edge, so the cut-out's rim is the board's own paint
        for dx in (-1, 0, 1):
            inner = np.minimum(inner, np.roll(np.roll(board, dy, axis=0), dx, axis=1))
    return after, (inner > 0.5).astype(F32)


def sign_edits(info, seed):
    """(Rounds one to eleven: the two cut-outs that changed the sign's mind, a red stroke through POINT B and B.C.
    painted in red underneath. No longer painted: see sign_after.)"""
    shape = (H, W)
    at = info["at"]
    # the stroke: one angry pass, a little uphill, and a short second touch where it began
    pts = curve([at(0.045, 0.37), at(0.30, 0.325), at(0.62, 0.29), at(0.955, 0.235)], 8)
    m = stroke_mask(shape, pts, 7.4, seed + 1)
    m = np.maximum(m, stroke_mask(shape, curve([at(0.03, 0.33), at(0.13, 0.345), at(0.24, 0.31)], 5), 5.0, seed + 2, dry=0.2))
    strike = red_paint(shape, m, seed + 3)
    # B.C.: big, by hand, running a little uphill, and it has dripped
    S = SIGN
    b = fat(letter.mask(shape, "B.C.", at(0.065, 0.735), 52, hand=True, anchor="lm", rough=0.8, slant=S["slant"] + 0.07, spacing=1.0, seed=seed + 5), 1.25)
    x, y = grid(shape)
    drips = Paper(shape)
    rng = np.random.default_rng(seed + 6)
    cols = np.where(b.sum(axis=0) > 3)[0]
    for u_ in (0.12, 0.36, 0.71, 0.93):
        cx_ = int(cols[0] + u_ * (cols[-1] - cols[0]))
        rows = np.where(b[:, cx_] > 0.5)[0]
        if not len(rows):
            continue
        top = rows[-1] - 1
        ln = 7 + rng.random() * 15
        drips.taper([(cx_, top), (cx_ + rng.normal(0, 0.3), top + ln * 0.6), (cx_ + rng.normal(0, 0.4), top + ln)], "#ffffff", 2.4, 1.5)
        drips.ellipse(cx_, top + ln, 1.7, 2.2, "#ffffff")
    _, dm = drips.done()
    bc = red_paint(shape, np.maximum(b, dm), seed + 7)
    return strike, bc


def details(pic, info, seed=SEED):
    """Over the brushwork: say the hard things again, crisply, then all the small crisp things."""
    shape = (H, W)
    x, y = grid(shape)
    rng = np.random.default_rng(seed + 77)
    ground, road, across, crisp = info["ground"], info["road"], info["across"], info["under"]
    near = np.clip((y - HZ) / (H - HZ), 0, 1)

    # ---- the sky: the burning edges of the clouds again, and the first stars
    pic[...] = lerp(pic, crisp, (info["cloud"] * 0.24)[..., None])                # the round forms of the clouds, lightly
    pic[...] = lerp(pic, crisp, (info["hot"] * 0.66)[..., None])                  # and their burning edges, firmly
    lum = crisp @ np.array([0.3, 0.55, 0.15], dtype=F32)
    stars = Paper(shape)
    made = 0
    while made < 20:
        sx_, sy_ = rng.random() * W, rng.random() ** 1.5 * 150
        if lum[int(sy_), int(sx_)] > 0.21 or info["hot"][int(sy_), int(sx_)] > 0.05:
            continue
        big = rng.random()
        r = 0.55 if big < 0.7 else (0.8 if big < 0.93 else 1.1)
        tone = "#fff6e4" if rng.random() < 0.7 else "#dfe6ff"
        stars.ellipse(sx_, sy_, r, r, tone, 0.55 + 0.45 * rng.random())
        if big > 0.93:
            stars.line([(sx_ - 2.6, sy_), (sx_ + 2.6, sy_)], tone, 0.5, 0.55)
            stars.line([(sx_, sy_ - 2.6), (sx_, sy_ + 2.6)], tone, 0.5, 0.55)
        made += 1
    ex, ey = 668, 176                                               # the evening star, low in the violet
    stars.ellipse(ex, ey, 1.3, 1.3, "#fffaf0")
    stars.line([(ex - 4, ey), (ex + 4, ey)], "#fff2dc", 0.6, 0.7)
    stars.line([(ex, ey - 5), (ex, ey + 5)], "#fff2dc", 0.6, 0.7)
    stars.onto(pic)

    # ---- the mesas: their shape against the sky, the beds in their cliffs, the last light along their rims
    mesa = np.zeros(shape, dtype=F32)
    edge = Paper(shape)
    for k, line in enumerate(info["mesa_lines"]):
        m = np.clip(y - line[None, :] + 0.5, 0, 1) * np.clip(HZ + 1 - y, 0, 1)
        mesa = np.maximum(mesa, m)
        xs = range(0, 304, 4) if k == 0 else range(486, 800, 4)
        land.strata(edge, line, xs[0], xs[-1], seed + 130 + k, offsets=(4, 9, 15, 22), color="#3f2f6c", light="#e88e78", alpha=0.5)
        sky_line = [(float(px_), float(line[px_]) - 0.3) for px_ in xs]
        edge.line(sky_line, "#ffb07a" if k == 0 else "#ffa878", 1.0, 0.55)
    pic[...] = lerp(pic, crisp, (mesa * 0.75)[..., None])
    edge.onto(pic)
    pic[...] = lerp(pic, crisp, (np.clip(1 - np.abs(y - HZ) / 2.0, 0, 1) * 0.6)[..., None])       # the horizon itself, level and sharp

    # ---- the road: its broken edges, the worn white lines, the yellow dashes, the cracks and their tar
    e = blur(road, 0.9)
    lip = np.clip(1 - np.abs(e - 0.5) * 3.2, 0, 1) * ground * (0.45 + 0.75 * noise(shape, (14, 5), seed + 60, 3))
    tint(pic, "#6a5478", np.clip(lip * 0.75 * np.clip(near * 4, 0.25, 1), 0, 1).astype(F32))
    outer = np.clip(1 - np.abs(e - 0.14) * 7, 0, 1) * ground * noise(shape, (20, 4), seed + 61, 3)
    over(pic, "#f6cca0", np.clip(outer * 0.5, 0, 1).astype(F32))
    rd = Paper(shape)
    zs = [520.0 * 1.045 ** i for i in range(120)]
    for sgn in (-1, 1):                                             # the white edge lines, mostly worn away
        for i in range(len(zs) - 1):
            wear = rng.random()
            if wear < 0.14:
                continue
            z0, z1 = zs[i], zs[i + 1]
            row = row_of(z0)
            tone = mix("#cfc4d2", "#ffe6b4", np.clip(1 - (row - HZ) / 120.0, 0, 1) ** 1.5)
            a0, a1 = sgn * (287 + rng.normal(0, 1.2)), sgn * (298 + rng.normal(0, 1.2))
            rd.poly([P(a0, 0, z0), P(a1, 0, z0), P(a1, 0, z1), P(a0, 0, z1)], tone, 0.30 + 0.5 * wear)
    k0 = 0
    for i in range(-1, 60):                                         # the broken yellow line
        z0 = 836.0 + 914.0 * i
        z1 = z0 + 305.0
        if z1 < 500:
            continue
        z0 = max(z0, 430.0)
        n = 9 if i < 2 else (4 if i < 6 else 1)
        for j in range(n):
            za, zb = lerp(z0, z1, j / n), lerp(z0, z1, (j + 1) / n)
            row = row_of(za)
            tone = mix(mix("#c99a44", "#e6b850", rng.random()), "#fff0b0", np.clip(1 - (row - HZ) / 90.0, 0, 1) ** 1.3)
            hw = 7.5 + rng.normal(0, 0.5)
            off = rng.normal(0, 0.5)
            rd.poly([P(off - hw, 0, za), P(off + hw, 0, za), P(off + hw, 0, zb), P(off - hw, 0, zb)], tone, 0.80 + 0.2 * rng.random())
    rd.onto(pic)
    # paint that has flaked off the lines lets the road show through
    flake = step(0.60, 0.74, land.texture(shape, HZ, seed + 62, 9.0, 2)) * (np.abs(across) < 12) * road * np.clip(near * 3, 0, 1)
    pic[...] = lerp(pic, crisp, (flake * 0.55)[..., None])
    ck = Paper(shape)
    for i in range(13):                                             # cracks right across, where the cold has opened it
        z = 700.0 + rng.random() ** 1.5 * 7000.0
        s = CAM.F / z
        a0, a1 = (-ROAD, ROAD) if rng.random() < 0.45 else sorted((rng.uniform(-ROAD, ROAD), rng.uniform(-ROAD, ROAD)))
        if a1 - a0 < 150:
            continue
        m = max(4, int((a1 - a0) / 30))
        zz, pts = z, []
        for j in range(m + 1):
            zz += rng.normal(0, 9)
            pts.append(P(lerp(a0, a1, j / m), 0, zz + 20 * math.sin(j * 0.5 + i)))
        tone = mix("#3e3456", "#93748a", np.clip(1 - s * 1.6, 0, 1))
        for j in range(m):
            if rng.random() < 0.12:
                continue
            ck.line([pts[j], pts[j + 1]], tone, max(0.7, s * (2.2 + 2.0 * rng.random())), np.clip(s * 2.0, 0.2, 0.75))
    for (a_mid, z_from, z_to) in ((2.0, 520.0, 5200.0), (176.0, 760.0, 2600.0), (-212.0, 1200.0, 4200.0)):      # and along it, where two strips of paving meet
        pts, a = [], a_mid
        for z in np.geomspace(z_from, z_to, 30):
            a += rng.normal(0, 2.4)
            pts.append(P(a, 0, z))
        for j in range(len(pts) - 1):
            if rng.random() < 0.3:
                continue
            s = (pts[j][1] - HZ) / CAM.eye
            ck.line([pts[j], pts[j + 1]], mix("#3e3456", "#93748a", np.clip(1 - s * 1.6, 0, 1)), max(0.7, s * 2.8), np.clip(s * 1.8, 0.2, 0.7))
    for (a0, a1, z0, z1, k_) in ((-270.0, -128.0, 2320.0, 2840.0, 3), (64.0, 218.0, 3300.0, 4000.0, 5)):      # where it has been mended: a darker piece let in, with tar round it
        r3 = np.random.default_rng(seed + 800 + k_)
        ring = []
        for (ua, za) in ((0, 0), (0.5, -0.04), (1, 0), (1.04, 0.5), (1, 1), (0.5, 1.05), (0, 1), (-0.03, 0.5)):
            ring.append(P(lerp(a0, a1, ua) + r3.normal(0, 5), 0, lerp(z0, z1, za) + r3.normal(0, 14)))
        ck.poly(ring, "#463c62", 0.30)
        for j in range(len(ring)):
            if r3.random() < 0.85:
                ck.line([ring[j], ring[(j + 1) % len(ring)]], "#3a3052", max(0.7, (ring[j][1] - HZ) / CAM.eye * 3.0), 0.55)
    for a_ in (-236.0, -84.0):                                      # the marks where somebody braked hard, long ago
        pts = [P(a_ + 0.00002 * (z - 900) ** 2 * (1 if a_ < -100 else 1.1), 0, z) for z in np.geomspace(900.0, 2100.0, 12)]
        ck.taper(pts, "#3c3454", 6.5, 1.5, 0.30)
    ck.onto(pic)
    grit = (rng.random(shape) < info["shine"] ** 2 * 0.035 * np.clip(near * 6, 0.2, 1)) * road       # the low sun picks out the grit in it
    over(pic, "#ffe8b4", (grit * 0.7).astype(F32))

    # ---- the shadows again, shorter and with a harder edge, close in under each thing
    sm = shadows(shape, seed, 2.6)
    tint(pic, "#5a467e", (np.clip(sm, 0, 1) * 0.40 * ground * (1 - road * 0.5)).astype(F32))
    thin = Paper(shape)                                             # and the thin ones: the sign's posts, the reflector posts
    for ax, z, half, length in [(a_, SIGN["z"], 7.0, 1150.0) for a_ in SIGN["posts"]] + [(352.0, z_, 4.0, 330.0) for z_ in (1240.0, 3040.0, 4840.0)] + [(-352.0, z_ + 900, 4.0, 330.0) for z_ in (1240.0, 3040.0, 4840.0)]:
        s0, s1 = CAM.F / z, CAM.F / max(z - length, 430.0)
        thin.poly([(VX + (ax - half) * s0, HZ + CAM.eye * s0), (VX + (ax + half) * s0, HZ + CAM.eye * s0), (VX + (ax + half) * s1, HZ + CAM.eye * s1), (VX + (ax - half) * s1, HZ + CAM.eye * s1)], "#000000")
    tint(pic, "#55427a", (thin.done()[1] * 0.46 * ground).astype(F32))

    # ---- everything that stands on the plain, far things first
    things = [("bush", b[1], b) for b in bushes(seed + 200)]
    things += [("pole", z, (ax, z, i)) for i, (ax, z) in enumerate(POLES)]
    r2 = np.random.default_rng(seed + 300)
    for i in range(150):                                            # dry grass: along the edge of the paving, and here and there out on the flat
        z = 700.0 + r2.random() ** 1.5 * 9000.0
        half = 400.0 * z / CAM.F
        sgn = -1 if r2.random() < 0.5 else 1
        ax = sgn * ((ROAD + 6 + r2.random() ** 2 * 40) if i < 60 else (ROAD + 110 + r2.random() ** 1.3 * (half + 60 - ROAD - 110)))
        things.append(("tuft", z, (ax, z, 12.0 + r2.random() * 22.0, int(r2.integers(1 << 30)))))
    for i in range(170):                                            # stones
        z = 700.0 + r2.random() ** 1.4 * 6000.0
        half = 400.0 * z / CAM.F
        sgn = -1 if r2.random() < 0.5 else 1
        ax = sgn * (ROAD + 14 + r2.random() ** 1.5 * (half + 40 - ROAD))
        things.append(("stone", z, (ax, z, 5.0 + r2.random() ** 2 * 22.0, int(r2.integers(1 << 30)))))
    for sgn in (-1, 1):                                             # the fences that keep the range cattle off the road
        for i in range(60):
            z = 2300.0 + 520.0 * i + r2.normal(0, 30)
            things.append(("post", z, (sgn * (1460.0 + r2.normal(0, 14)), z, 118.0 + r2.normal(0, 10), r2.normal(0, 0.05))))
    for i, z in enumerate((1240.0, 3040.0, 4840.0, 6640.0, 8440.0, 10240.0)):                     # reflector posts along our side
        things.append(("marker", z, (352.0, z)))
        things.append(("marker", z + 900, (-352.0, z + 900)))
    things += [("pump", 17000.0, (-4300.0, 17000.0)), ("weed", 1705.0, (452.0, 1705.0, 36.0)), ("weed", 3900.0, (-1440.0, 3900.0, 30.0)),
               ("hubcap", 1190.0, (374.0, 1190.0)), ("bottle", 1015.0, (-350.0, 1015.0)), ("tread", 1330.0, (-382.0, 1330.0)), ("rabbit", 1900.0, (-392.0, 1900.0))]
    things.sort(key=lambda t: -t[1])
    sheet = Paper(shape)
    runs = wires(sheet, seed + 9)
    # three birds on the top wire, between the first pole and the second
    top = min((r_ for r_ in runs if 60 < r_[0][0] < 140 and r_[-1][0] > 250), key=lambda r_: r_[0][1], default=None)
    if top is not None:
        for bx in (150.0, 161.0, 196.0):
            j = max(i for i, p_ in enumerate(top) if p_[0] <= bx)
            j = min(j, len(top) - 2)
            f_ = (bx - top[j][0]) / max(top[j + 1][0] - top[j][0], 1e-3)
            bird(sheet, bx, lerp(top[j][1], top[j + 1][1], f_) + 0.3, 6.4 if bx != 161.0 else 5.6, 1 if bx != 196.0 else -1)
    sign_done = False
    fence = {-1: [], 1: []}
    for kind, z, what in things:
        if z < SIGN["z"] and not sign_done:                         # the sign takes its place in the queue
            sheet.onto(pic)
            info["sign"] = the_sign(pic, seed + 400)
            sheet = Paper(shape)
            sign_done = True
        s = CAM.F / z
        if kind == "bush":
            ax, _, wide, tall, k = what
            sage(sheet, VX + ax * s, HZ + CAM.eye * s, wide * s, tall * s, k, 1 if ax < 0 else -1)
        elif kind == "tuft":
            ax, _, size, k = what
            tuft(sheet, VX + ax * s, HZ + CAM.eye * s, max(1.6, size * s), k, 1 if ax < 0 else -1)
        elif kind == "stone":
            ax, _, size, k = what
            if size * s > 0.9:
                stone(sheet, VX + ax * s, HZ + CAM.eye * s, size * s, size * s * 0.62, k, 1 if ax < 0 else -1)
        elif kind == "pole":
            ax, _, i = what
            fade = float(np.clip(1.15 - i * 0.14, 0.3, 1.0))
            pole(sheet, ax, z, seed + 500 + i, fade=fade)
        elif kind == "post":
            ax, _, tall, lean = what
            f, t = P(ax, 0, z), P(ax + lean * tall, tall, z)
            tone = airy("#3a2a40", f[1])
            sheet.line([f, t], tone, max(0.8, s * 9.0))
            if s > 0.1:
                sheet.line([(f[0] - (1 if ax > 0 else -1) * s * 4, f[1]), (t[0] - (1 if ax > 0 else -1) * s * 4, t[1])], airy("#f0a868", f[1], 0.4), 0.7, 0.8)
            sgn = 1 if ax > 0 else -1
            if fence[sgn]:
                pf, pt_ = fence[sgn][-1]
                for frac in (0.92, 0.55):
                    a_ = (lerp(pf[0], pt_[0], frac), lerp(pf[1], pt_[1], frac))
                    b_ = (lerp(f[0], t[0], frac), lerp(f[1], t[1], frac))
                    mid_ = ((a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2 + s * 5)
                    sheet.line([a_, mid_, b_], airy("#3a2a40", f[1]), 0.6, 0.55)
            fence[sgn].append((f, t))
        elif kind == "pump":
            windpump(sheet, what[0], z, seed + 700)
        elif kind == "weed":
            ax, _, size = what
            tumbleweed(sheet, VX + ax * s, HZ + CAM.eye * s, size * s, seed + 710 + int(z), 1 if ax < 0 else -1)
        elif kind == "hubcap":                                      # somebody's hubcap, where it rolled to
            cx_, cy_ = VX + what[0] * s, HZ + CAM.eye * s
            rx_, ry_ = 20 * s, 20 * s * 0.34
            sheet.ellipse(cx_ + 2, cy_ + 1.5, rx_ * 1.1, ry_ * 1.0, "#33284a", 0.6)
            sheet.ellipse(cx_, cy_ - 1, rx_, ry_, "#8884a2")
            sheet.ellipse(cx_, cy_ - 1.6, rx_ * 0.62, ry_ * 0.58, "#56506e")
            sheet.ellipse(cx_, cy_ - 1.9, rx_ * 0.2, ry_ * 0.26, "#a6a2bc")
            sheet.line([(cx_ + math.cos(a_) * rx_, cy_ - 1 + math.sin(a_) * ry_) for a_ in np.linspace(math.pi * 1.05, math.pi * 1.95, 7)], "#ffdca4", 0.9)
        elif kind == "bottle":                                      # and a green bottle, the sun shining through it
            cx_, cy_ = VX + what[0] * s, HZ + CAM.eye * s
            ln, wd = 23 * s, 6.2 * s
            sheet.line([(cx_ - ln * 0.5 + 2, cy_ + 1.2), (cx_ + ln * 0.5 + 2, cy_ + 0.2)], "#33284a", wd * 0.9, 0.55)
            sheet.line([(cx_ - ln * 0.5, cy_ - wd * 0.5), (cx_ + ln * 0.22, cy_ - wd * 0.72)], "#2e6650", wd)
            sheet.line([(cx_ + ln * 0.22, cy_ - wd * 0.72), (cx_ + ln * 0.5, cy_ - wd * 0.82)], "#2e6650", wd * 0.45)
            sheet.line([(cx_ - ln * 0.38, cy_ - wd * 0.86), (cx_ + ln * 0.12, cy_ - wd * 1.04)], "#b6f0b0", 0.9)
            sheet.line([(cx_ - ln * 0.1, cy_ - wd * 0.3), (cx_ + ln * 0.14, cy_ - wd * 0.42)], "#5cc08a", 1.0, 0.9)
        elif kind == "tread":                                       # a strip of somebody's tire
            cx_, cy_ = VX + what[0] * s, HZ + CAM.eye * s
            ln = 74 * s
            pts = curve([(cx_ - ln * 0.5, cy_ - 1), (cx_ - ln * 0.2, cy_ - 6 * s), (cx_ + ln * 0.15, cy_ - 2 * s), (cx_ + ln * 0.5, cy_ - 9 * s)], 5)
            sheet.line([(p_[0] + 2, p_[1] + 2.2) for p_ in pts], "#33284a", 13 * s, 0.5)
            sheet.line(pts, "#221a2a", 13 * s)
            for j in range(1, len(pts) - 1, 2):
                sheet.line([(pts[j][0] - 1, pts[j][1] - 5.5 * s), (pts[j][0] + 1, pts[j][1] + 5.5 * s)], "#3e3448", 0.9)
            sheet.line([(p_[0], p_[1] - 6.0 * s) for p_ in pts[2:]], "#e89c5c", 0.8, 0.85)
        elif kind == "rabbit":
            jackrabbit(sheet, VX + what[0] * s, HZ + CAM.eye * s, 58 * s, 1 if what[0] < 0 else -1)
        elif kind == "marker":
            ax, _ = what
            f, t = P(ax, 0, z), P(ax, 105, z)
            sheet.line([f, t], airy("#8a8098", f[1]), max(0.8, s * 6.0))
            sheet.line([P(ax, 82, z), t], airy("#e8e2e6", f[1], 0.5), max(0.8, s * 7.0))
            if s > 0.2:
                sheet.ellipse(t[0], t[1] + s * 12, s * 4.2, s * 4.2, "#ffd27a")
    if not sign_done:
        sheet.onto(pic)
        info["sign"] = the_sign(pic, seed + 400)
        sheet = Paper(shape)
    sheet.onto(pic)
    return pic


def the_sun(info):
    """The sun's disc, half sunk at the end of the road: -> (color, alpha), soft-edged. It is a little
    flattened, as the setting sun is, whiter at the top and redder where it meets the ground, and the
    thin bar of cloud that lies across it shows through."""
    shape = (H, W)
    x, y = grid(shape)
    cx, cy, r = SUN
    d = np.hypot((x - cx) / 1.04, (y - cy) / 0.96)
    disc = np.clip((r - d) / 3.0 + 0.5, 0, 1)                         # soft over three pixels
    halo = np.clip(1 - (d - r) / 9.0, 0, 1) ** 2 * 0.34 * (d >= r - 1.5)
    alpha = np.maximum(disc, halo)
    alpha = alpha * np.clip((HZ + 0.5 - y) / 1.2, 0, 1)                 # the ground hides its lower half
    alpha = alpha * (1 - np.clip(info["cloud"] * 1.1, 0, 0.9))          # and the cloud in front of it stays in front
    up = np.clip((cy - y) / r, 0, 1)
    color = ramp(up, [(0.0, "#ffbc58"), (0.18, "#ffdc80"), (0.45, "#fff6c0"), (1.0, "#fffef0")])
    color = lerp(color, ramp(up, [(0.0, "#ff9038"), (1.0, "#ffc45c")]), np.clip((d - r * 0.80) / (r * 0.30), 0, 1)[..., None])    # its limb is deeper
    color = np.clip(color * (1 + (noise(shape, 9, 77, 2) - 0.5)[..., None] * 0.05), 0, 1)
    # the same grain and the same few colors as the painting it lies on, so that it is not smoother than the sky round it
    g = grain(color.astype(F32), 7, 0.02)
    box = (slice(int(cy - r - 12), int(cy + 3)), slice(int(cx - r - 14), int(cx + r + 14)))
    pal = palette_of([g[box].reshape(-1, 1, 3)], colors=14)
    g[box] = pal[to_palette(g[box], pal, speckle=0.014)]
    return np.clip(g, 0, 1).astype(F32), np.clip(alpha, 0, 1).astype(F32)


def lay_sprite(picture, color, alpha, foot, at, scale):
    """Lay a cropped sprite on a picture with its foot at `at`, at `scale` (smoothly): only for looking."""
    h, w = alpha.shape
    nw, nh = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
    rgba = np.dstack([color * alpha[..., None], alpha])
    small = np.dstack([np.asarray(Image.fromarray(rgba[..., i].astype(F32), "F").resize((nw, nh), Image.LANCZOS), dtype=F32) for i in range(4)])
    x0, y0 = int(round(at[0] - foot[0] * scale)), int(round(at[1] - foot[1] * scale))
    X0, Y0, X1, Y1 = max(x0, 0), max(y0, 0), min(x0 + nw, picture.shape[1]), min(y0 + nh, picture.shape[0])
    if X1 <= X0 or Y1 <= Y0:
        return picture
    part = small[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
    a = np.clip(part[..., 3:4], 0, 1)
    picture[Y0:Y1, X0:X1] = picture[Y0:Y1, X0:X1] * (1 - a) + np.clip(part[..., :3], 0, 1)
    return picture


def wagon_scale(row):
    """How big the wagon cut-out must be drawn when the middle of its back axle is on picture row `row`,
    for it to fit the lane it is in (the car is 200 cm wide and 384 px wide at full size)."""
    return (row - HZ) / CAM.eye / (384.0 / 200.0)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def show(pic, name):
    Image.fromarray((np.clip(pic, 0, 1) * 255).astype(np.uint8)).save(name)


def save_soft(color, alpha, name):
    """A cut-out with a soft edge: full color and real transparency."""
    a8 = (np.clip(alpha, 0, 1) * 255 + 0.5).astype(np.uint8)
    c8 = (np.clip(color, 0, 1) * 255 + 0.5).astype(np.uint8)
    seen = c8[a8 > 0]
    c8[a8 == 0] = seen.mean(axis=0).astype(np.uint8) if len(seen) else 0       # where nothing shows, one plain color: small file, no dark fringe
    Image.fromarray(np.dstack([c8, a8]), "RGBA").save(name, optimize=True)
    return os.path.getsize(name)


def comp(folder, out, wagon_at):
    """Everything laid together from the finished files, the wagon at a place on its lane: to look at."""
    im = Image.open(f"{folder}/back.png").convert("RGBA")
    for n in ("sun", "sign-bc"):
        im.alpha_composite(Image.open(f"{folder}/{n}.png").convert("RGBA"))
    pic = np.asarray(im.convert("RGB"), dtype=F32) / 255
    w = np.asarray(Image.open(f"{folder}/wagon-rear-0.png").convert("RGBA"), dtype=F32) / 255
    row, foot = wagon_at
    lay_sprite(pic, w[..., :3], w[..., 3], foot, (px(LANE, row), row), wagon_scale(row))
    show(pic, out)


def box_of(alpha):
    ys, xs = np.where(alpha > 0.5)
    return [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


def layout(info, foot, size, title_row, bc_box):
    s = info["sign"]
    rect = [int(round(v)) for v in s["rect"]]
    rows = [600, 570, 540, 510, 480, 450, 420, 400, 380, 360, 345, 336, 330]
    data = {
        "id": "highway", "horizon": HZ, "full": 577,
        "light": "the sun is dead ahead, half sunk at the end of the road (400, 330): everything is seen against it, shadows run toward us, clouds are lit from underneath",
        "walk": [], "blocked": [],
        "planes": [
            {"id": "sun", "file": "sun.png", "plane": "back", "soft": True},
            {"id": "sign-bc", "file": "sign-bc.png", "plane": "back", "rect": bc_box,
             "note": "the board saying POINT B.C. (round twelve): the game bends the sign with its `portal` effect and this comes out of it; it replaces the red slash (sign-strike.png) and the dripping B.C. of rounds one to eleven"},
            {"id": "wagon", "frames": ["wagon-rear-0.png", "wagon-rear-1.png"], "fps": 4, "foot": [int(round(foot[0])), int(round(foot[1]))],
             "at": [int(round(px(LANE, title_row))), int(title_row)], "scale": round(wagon_scale(title_row), 3)},
        ],
        "things": [{"id": "sign", "what": "the road sign: POINT B, 40", "shape": {"rect": rect}},
                   {"id": "sun", "what": "the sun, going down at the end of the road", "shape": {"rect": [SUN[0] - SUN[2], SUN[1] - SUN[2], SUN[2] * 2, SUN[2]]}}],
        "exits": [], "marks": {},
        "road": [[int(round(px(LANE, r))), r] for r in rows],
        "sun": [SUN[0], SUN[1], SUN[2]],
        "sign": {"rect": rect, "board": rect, "posts_foot_y": int(round(P(SIGN["posts"][0], 0, SIGN["z"])[1])),
                 "point_b": [int(round(v)) for v in s["point_b_rect"]]},
        "wagon": {
            "files": ["wagon-rear-0.png", "wagon-rear-1.png"], "size": [int(size[0]), int(size[1])],
            "foot": [int(round(foot[0])), int(round(foot[1]))],
            "foot_is": "the middle of the rear axle, on the road (the shadow lies below it, toward us)",
            "full_size_body_px": 384,
            "scale_rule": "to sit in its lane the cut-out is drawn at scale = (foot_y - 330) / 518.4, with foot_x on the 'road' line",
            "scale_at": {str(r): round(wagon_scale(r), 3) for r in (600, 548, 500, 434, 380, 345)},
            "lane_half_width_px_at_600": 150,
        },
        "vanish": [VX, HZ],
        "road_edges_at_600": [int(round(px(-ROAD, 600))), int(round(px(ROAD, 600)))],
    }
    return data


if __name__ == "__main__":
    import highway_wagon
    t0 = time.time()
    os.makedirs("out/highway", exist_ok=True)
    fast = len(sys.argv) > 1
    base, info = under()
    info["under"] = base
    show(base, "out/highway-1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.22)
    print("brushed", round(time.time() - t0, 1))
    details(pic, info)
    bc, ba = sign_after(pic, info["sign"], SEED + 400)                # (the sign's own seed: the same board, other letters)
    pic, bc = grade(pic), grade(bc)
    show(pic, "out/highway-2-back.png")
    sunc, suna = the_sun(info)
    parts = highway_wagon.layers()
    frames, foot = highway_wagon.frames(parts=parts)
    whole = pic.copy()
    over(whole, sunc, suna)
    over(whole, bc, ba)
    row = 548.0
    lay_sprite(whole, frames[0][0], frames[0][1], foot, (px(LANE, row), row), wagon_scale(row))
    show(whole, "out/highway-2-all.png")
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    print("back", finish(pic, "out/highway/back.png", 152))
    print("bc", finish(bc, "out/highway/sign-bc.png", 48, ba, amount=0.012))
    if os.path.exists("out/highway/sign-strike.png"):
        os.remove("out/highway/sign-strike.png")                     # (the red slash of rounds one to eleven)
    print("sun", save_soft(sunc, suna, "out/highway/sun.png"))
    foot, (w_, h_), sizes = highway_wagon.write(["out/highway/wagon-rear-0.png", "out/highway/wagon-rear-1.png"], 96, parts=parts)
    print("wagon", sizes, "foot", foot, "size", (w_, h_))
    with open("out/highway/layout.json", "w") as f:
        data = layout(info, foot, (w_, h_), row, box_of(ba))
        f.write("{\n" + ",\n".join(f"  {json.dumps(k)}: {json.dumps(v)}" for k, v in data.items()) + "\n}\n")
    comp("out/highway", "out/highway-comp.png", (row, foot))
    print("done", round(time.time() - t0, 1))

"""Nevada, the present day: the last stop before nothing. Early morning.

The picture's idea: emptiness, with one human thing in it. A vast clean sky, a flat floor of desert
running to far mesas, long cool shadows, and a shabby stand that somebody has loved for forty years.

LIGHT   The sun is low on the RIGHT, a little behind our right shoulder (it is out of the picture). Every
        thing throws a long cool shadow to the LEFT and a little away from us (nevada_roadside_kit.SUN);
        right-hand ends are in full warm sun, fronts take it aslant, left-hand ends are in blue-violet shade.
DEPTH   horizon 290, full 590 (the game's numbers; nevada_roadside_kit.CAM is that camera, and every
        standing thing is drawn through it, so each is the right size for the people beside it).
TONES   light: the far plain and the pale packed lot in the sun, the clouds, the glow along the horizon.
        middle: the deep blue sky, the mesas, the nearer ground, which deepens and warms toward us.
        dark: the long shadows, the car at the bottom left, the sagebrush and drum at the bottom right,
        the deepened bottom corners. They frame the pale middle, where the old man's stand is.
PLACE   (left to right, in the old scene's order)
        car      bottom left, nose to the right, its tail off the edge of the picture         cut-out
        road     far left: two lanes running away to the horizon at x 150, telephone poles beside it;
                 at its edge the old gas sign on a tall pipe (GAS painted out) and a leaning mail box
        shack    left of middle, set back: boards, tin roof, porch, LAST STOP on a board on the roof
        pump     on its concrete island, right of the shack                                    cut-out
        old man  (drawn by the game) in his lawn chair, left of the table: clear floor at (388, 498)
        stand    middle: a board on trestles, jug, glasses, rocks, price board, beach umbrella   cut-out
        fence    right: chain link and barbed wire; a corner post at x 612, one side running to the right
                 edge, the other straight away to the horizon. The notice is on it, x 630 to 695.
        tracks   come straight toward us out of the desert (far off they swing in from the road as a
                 thread), in under the fence right below the notice, and stop at the glass, front
                 right, (646, 535). The glass lies in the sun.
        front    bottom right corner: sagebrush and a rusty oil drum                  cut-out, front plane

Three things in the shared library are worked round here, not changed (see nevada_roadside_kit):
land.texture leaves straight seams across a big floor (ground_tex, desert); brush.Sheet punches half-clear
holes when thin paint goes over solid paint (Paper); land.cast and land.rock_shadow only throw shadows to
the right (Shade lays a thing's own drawing down along the sun's rays; the stones are painted in a mirror).
"""

import json, math, os, sys, time
import numpy as np
from PIL import Image
from brush import *
import sky, land, letter
from nevada_roadside_kit import *
import nevada_roadside_props as P

SEED = 21
OUT = "out/nevada-roadside"
SHADE = "#6664ac"                                           # what a morning shadow does to the ground

# ---- where things are, in the world (cm). x right of the middle, z away.
ROAD_T = (150 - 400) / 800.0                                # the road runs away toward a vanishing point at x 150
GLASS = (330.0, 196.0, 107.0, 84.0)                         # the patch of fused sand: middle x, z; half width, half depth
TRACK_DIR = (0.3355, 0.9420)                                # the way the tracks came, read backward: away from us, a little right
TRACK_END = (353.5, 262.0)                                  # where they stop, at the far lip of the glass
TRACK = [TRACK_END, (594.5, 939.5), (1328.0, 3000.0), (2397.0, 6000.0), (3465.0, 9000.0), (3760.0, 10600.0), (3200.0, 12200.0), (1600.0, 13300.0), (-1500.0, 13200.0), (-4258.0, 12000.0)]
OLDTIMER = (388, 498)                                       # the old man's chair goes here (the game draws him)
POLES = [9400.0 + 3000.0 * i for i in range(9)]             # telephone poles along the far side of the road


def road_x(z, across=0.0):
    """World x of the road at depth z: across = 0 is its right edge (ours), 1 its far edge."""
    return -507.8 + ROAD_T * z - across * 765.0


def rut(side, n=40):
    """One wheel's track, as world points from the glass back to the fence and on."""
    px, pz = TRACK_DIR[1], -TRACK_DIR[0]                    # square to the way the tracks run
    pts = []
    for t in np.linspace(0, 1, n):
        z = lerp(TRACK[0][1], 9000.0, t ** 2.2)
        x = TRACK[0][0] + (z - TRACK[0][1]) * TRACK_DIR[0] / TRACK_DIR[1]
        pts.append((x + side * 75.0 * px, z + side * 75.0 * pz))
    return pts


# ---------------------------------------------------------------- the sky
def paint_sky(shape, seed):
    x, y = grid(shape)
    pic = sky.field(shape, HZ, [(0.0, "#2654a8"), (0.30, "#3676c6"), (0.58, "#60a2dc"), (0.78, "#a4cde6"), (0.92, "#e6dccc"), (1.0, "#f8dcb2")],
                    seed, haze="#f8e0bc", patch=0.03)
    # the sun is just out of the picture on the right: the air glows that way
    near_sun = np.exp(-((x - 930) / 430.0) ** 2 - ((y - 262) / 120.0) ** 2)
    glow(pic, "#ffd49a", (near_sun * 0.62).astype(F32))
    tint(pic, "#7f8fd0", (np.clip(1 - x / 520.0, 0, 1) * np.clip(1 - y / 260.0, 0, 1) * 0.30).astype(F32))    # and is deepest up on the left
    return pic


def long_clouds(shape, clouds, seed, ragged=1.0, vanish=(-1500.0, float(HZ))):
    """Morning clouds: long, level, flat underneath and gently heaped on top, in rows that draw together
    toward a far point on the horizon. Each is (middle x, base y, half length, thickness, how many heaps).
    -> (thickness 0-1, height map), as sky.billows gives."""
    rng = np.random.default_rng(seed)
    x, y = grid(shape)
    height = np.zeros(shape, dtype=F32)
    comb = noise(shape, (170, 5.5), seed + 15, 3)                   # the wind combs them into level streaks
    comb2 = noise(shape, (260, 9), seed + 16, 3)
    for (cx, base, half, thick, heaps) in clouds:
        tilt = (vanish[1] - base) / (vanish[0] - cx)
        yy = y - (x - cx) * tilt                                    # the cloud straightened out
        u = (x - cx) / half
        v = (base - yy) / thick
        # the body: a long lens, flat below, with its thick part toward the sunward end
        prof = np.sqrt(np.clip(1 - u * u, 0, 1)) * np.clip(1 + 0.30 * u, 0.4, 1.3)
        lens = prof * np.clip(1 - np.abs(v - 0.30 * prof) / (0.36 * prof + 1e-3), 0, 1)
        one = lens * thick * 0.46
        for _ in range(heaps):                                      # heaps along the top: wide and low
            p = max(-0.95, min(0.95, rng.normal(0.12, 0.42)))
            dome = math.sqrt(max(0.0, 1 - p * p))
            ry = thick * (0.18 + 0.36 * rng.random()) * (0.45 + 0.65 * dome) * (1 + 0.25 * p)
            rx = ry * (2.4 + 2.6 * rng.random())
            lx, ly = cx + p * half * 0.9, base - ry * 0.55 - rng.random() ** 1.4 * thick * 0.42 * dome
            d2 = ((x - lx) / rx) ** 2 + (np.where(yy > ly, (yy - ly) / (ry * 0.55), (yy - ly) / ry)) ** 2
            one = np.maximum(one, np.sqrt(np.clip(1 - d2, 0, 1)) * ry)
        # trails of thin cloud drawn out past both ends and a little below the base
        far_u = (x - cx) / (half * 1.45)
        veil = np.sqrt(np.clip(1 - far_u * far_u, 0, 1)) * np.clip(1 - np.abs(v - 0.12) / 0.5, 0, 1) * step(0.50, 0.78, comb2) * thick * 0.16
        one = np.maximum(one * np.clip(1.22 - 0.85 * step(0.42, 0.9, comb), 0, 1), veil)
        height = np.maximum(height, one)
    dx = (noise(shape, (140, 40), seed + 11, 4) - 0.5) * 2          # edges: long slow waves, then a fine fret
    dy = (noise(shape, (160, 28), seed + 12, 4) - 0.5) * 2
    height = sample(height, x + dx * 16 * ragged, y + dy * 5.5 * ragged)
    fx = (noise(shape, (22, 10), seed + 13, 3) - 0.5) * 2
    fy = (noise(shape, (26, 8), seed + 14, 3) - 0.5) * 2
    height = sample(height, x + fx * 4.5 * ragged, y + fy * 2.2 * ragged)
    thick_ = smooth(height / (height.max() * 0.11 + 1e-6))
    return thick_.astype(F32), height.astype(F32)


def morning_clouds(pic, seed):
    """Long clouds lying across the sky: cool lavender in their shade, rose where they turn to the light,
    and a burning gold edge on the side that faces the sun."""
    shape = pic.shape[:2]
    x, y = grid(shape)
    light = (0.93, -0.36)                                    # the light comes from the right, a little from above
    sets = [
        ([(610, 118, 330, 50, 22), (190, 72, 180, 26, 10)], seed + 5, 40.0, ("#6a80c0", "#9a9ccc", "#eea6a6", "#ffd8a2"), 1.0),
        ([(410, 188, 200, 26, 12), (790, 208, 150, 22, 8)], seed + 6, 26.0, ("#7888c4", "#a6a4d0", "#f0aca6", "#ffdca8"), 0.8),
        ([(500, 240, 200, 11, 8), (716, 262, 170, 8, 7), (250, 256, 130, 7, 5)], seed + 7, 12.0, ("#8a98cc", "#b2aed6", "#f4b8aa", "#ffe2b0"), 0.5),
    ]
    for clouds, sd, reach, tones, ragged in sets:
        thick, height = long_clouds(shape, clouds, sd, ragged)
        bright = sky.lit(thick, height, light, sd, reach=reach, rise=0.5)
        bright = np.clip(bright + (noise(shape, (90, 7), sd + 41, 3) - 0.5) * 0.16, 0, 1)             # streaks of thicker and thinner cloud
        color = ramp(bright, [(0.0, tones[0]), (0.50, tones[1]), (0.72, tones[2]), (0.90, tones[3]), (1.0, "#fff0cc")])
        fray = 0.55 + 0.9 * noise(shape, (60, 18), sd + 31, 4)
        body = smooth(blur(thick, 1.3) * fray)
        edge = lerp(blur(body, 4.0) * 0.9, body, np.clip(bright * 1.4, 0, 1))
        over(pic, color, np.clip(edge, 0, 1))
        # the edge that faces the sun burns: a thin line of gold where cloud ends and sky begins
        rim = np.clip(body - sample(body, x + light[0] * 3.5, y + light[1] * 3.5), 0, 1) * np.clip(body * 3, 0, 1)
        rim = np.clip(rim * 2.4, 0, 1) * (0.5 + 0.7 * noise(shape, 40, sd + 9, 3))
        over(pic, "#fff2c8", np.clip(rim * 0.8, 0, 1).astype(F32))


def all_clouds(pic, seed):
    sky.wisps(pic, HZ, seed + 3, "#ffe4c8", top=0.60, amount=0.45, cell=(420, 14))
    sky.wisps(pic, HZ, seed + 4, "#cfe2f4", top=0.0, amount=0.22, cell=(300, 34))
    morning_clouds(pic, seed)


# ---------------------------------------------------------------- the far country
def hills(pic, pts, base, seed, shade, lit, rough=2.0, ribs=0.5, haze=None, haze_amount=0.3, cap=None, sun=1.0, cliff=0.45):
    """A far mesa or range: a violet mass; under its rim a band of cliff broken into buttresses, each with
    its right-hand face in the sun; below that the talus, smooth and half lit."""
    shape = pic.shape[:2]
    x, y = grid(shape)
    m, line = land.ridge(shape, pts, base, seed, rough=rough)
    tall = np.maximum(base - line[None, :], 1.0)
    up = np.clip((base - y) / tall, 0, 1)                                              # 0 at its foot, 1 at the skyline
    body = ramp(up, [(0.0, tone(shade, 1.16, 0.02)), (0.45, tone(shade, 1.05)), (1.0, tone(shade, 0.93))])
    over(pic, body, m)
    # buttresses: uneven upright ribs, pushed about so no two are alike; each rib's right side is lit
    n = warp(noise(shape, (15, 70), seed + 3, 3), 7.0, (40, 18), seed + 5)
    right_side = np.clip((np.roll(n, 2, axis=1) - n) * 9.0, 0, 1)                       # where the rib falls away to the right
    band = np.clip((up - (1 - cliff)) / 0.12, 0, 1)                                     # the cliff under the rim
    slope = np.gradient(blur(np.tile(line[None, :], (9, 1)), 4.0)[4])                    # > 0 where the skyline falls to the right: a sunward end
    end = np.clip(slope * 1.6, 0, 1)[None, :] * np.ones(shape, dtype=F32)
    talus = (1 - band) * (0.22 + 0.25 * step(0.4, 0.7, noise(shape, (46, 10), seed + 4, 3)))
    warm = np.clip(right_side * band * ribs + end * 0.9 + talus * 0.5, 0, 1) * sun
    over(pic, lit, (warm * m).astype(F32))
    foot_of_cliff = np.clip(1 - np.abs(up - (1 - cliff)) / 0.07, 0, 1) * (0.4 + 0.6 * noise(shape, (30, 6), seed + 6, 2))
    tint(pic, tone(shade, 0.86), (foot_of_cliff * m * 0.45).astype(F32))                # the cliff's own shadow on the talus
    if cap is not None:                                                                  # the rim catches the light
        rim = np.clip(1 - np.abs(y - (line[None, :] + 1.0)) / 1.2, 0, 1) * m
        over(pic, cap, (rim * 0.6 * (0.5 + 0.5 * noise(shape, (50, 4), seed + 7, 2))).astype(F32))
    if haze is not None:
        over(pic, haze, (m * (1 - up) ** 1.2 * haze_amount).astype(F32))
    return m, line


def far_country(pic, seed):
    """A pale range right along the horizon, and mesas standing in front of it. -> the mask of all of it."""
    far_range = [(0, 272), (40, 266), (84, 270), (130, 278), (176, 280), (230, 273), (268, 262), (300, 268), (350, 276), (410, 281), (452, 277), (486, 268),
                 (520, 273), (566, 280), (620, 276), (668, 266), (700, 260), (742, 268), (800, 262)]
    m, _ = hills(pic, far_range, HZ + 2, seed + 11, "#aab0dc", "#ecc8c0", rough=3.0, ribs=0.0, haze="#f2dccc", haze_amount=0.6, cliff=0.3)
    for pts, sd, shade, lit_, cap, hz in (
            ([(-10, 258), (26, 256), (60, 258), (84, 259), (92, 266), (104, 277), (124, 285), (150, 290)], 12, "#9690c6", "#eeb49a", "#ffdcb8", 0.5),
            ([(160, 290), (184, 283), (200, 273), (206, 262), (236, 259), (262, 260), (268, 252), (300, 250), (346, 251), (356, 258), (366, 272), (384, 282), (412, 290)], 13, "#8e86c0", "#eeac8e", "#ffd8b0", 0.46),
            ([(498, 290), (512, 284), (520, 272), (524, 258), (536, 256), (541, 266), (548, 280), (566, 290)], 14, "#928ac2", "#f0b090", "#ffd8b0", 0.44),
            ([(574, 290), (596, 282), (610, 270), (616, 254), (640, 250), (652, 242), (700, 239), (748, 241), (780, 244), (810, 247)], 15, "#867cba", "#eea684", "#ffd4a8", 0.42)):
        mm, _ = hills(pic, pts, HZ + 2, seed + sd, shade, lit_, rough=1.3, ribs=0.9, haze="#eed8cc", haze_amount=hz, cap=cap)
        m = np.maximum(m, mm)
    return m


# ---------------------------------------------------------------- pass 1
def road_mask(shape, a0=0.0, a1=1.0, soft=0.0, z0=-700.0):
    zs = [z0, -300, 0, 400, 1000, 2000, 4000, 8000, 16000, 40000, 120000]
    pts = [gp(road_x(z, a0), z) for z in zs] + [gp(road_x(z, a1), z) for z in reversed(zs)]
    return mask_poly(shape, pts, soft=soft)


def shadows(shape):
    """Every standing thing's shadow, laid the same way by the same sun. -> one mask."""
    sh = np.zeros(shape, dtype=F32)
    on_island = np.zeros(shape, dtype=F32)
    for draw, at, yaw, lift, soft in ((P.draw_shack, P.SHACK_AT, P.SHACK_YAW, 0.0, 1.2), (P.draw_shack_side, P.SHACK_AT, P.SHACK_YAW, 0.0, 1.0), (P.draw_signpole, P.SIGN_AT, 0.0, 0.0, 1.0),
                                      (P.draw_mailbox, P.MAIL_AT, 0.0, 0.0, 0.8), (P.draw_island, P.PUMP_AT, 0.0, 0.0, 0.8), (P.draw_pump, P.PUMP_AT, 0.0, P.ISLAND[4], 1.0),
                                      (P.draw_stand, P.STAND_AT, 0.0, 0.0, 1.2), (P.draw_car, P.CAR_AT, 0.0, 0.0, 1.6), (P.draw_drum, P.DRUM_AT, 0.0, 0.0, 1.5)):
        one = P.shade_of(shape, draw, at, yaw, lift=lift, soft=soft)
        sh = np.maximum(sh, one)
        if draw in (P.draw_pump, P.draw_stand):
            on_island = np.maximum(on_island, one)
    hard, veil = P.fence_shadow(shape)
    sh = np.maximum(sh, np.maximum(hard * 0.9, veil * 0.26))
    for z in POLES:                                           # the poles along the road
        x0 = road_x(z, 1.0) - 150
        k = kz(z)
        sh = np.maximum(sh, mask_line(shape, [gp(x0, z), gp(x0 + SUN[0] * 850, z + SUN[1] * 850)], max(0.6, 30 * k * 0.5), soft=0.5) * 0.8)
    return np.clip(sh, 0, 1), on_island


def under(seed=SEED):
    """Everything broad and soft: the sky, the far country, the desert floor, the road, the big shadows."""
    shape = (H, W)
    x, y = grid(shape)
    info = {}
    pic = paint_sky(shape, seed)
    all_clouds(pic, seed)
    far_country(pic, seed)

    # ---- the desert floor
    ground = np.clip(y - HZ + 0.5, 0, 1).astype(F32)
    sand = desert(shape, seed + 20, far="#f4dcc6", mid="#e6b888", near="#c47e46", patch=0.08)
    over(pic, sand, ground)
    X, Z, below = floor(shape)
    # pale alkali flats far off, and darker ground where the scrub grows thick: both seen almost edge-on
    lie = noise(shape, (340, 7), seed + 21, 4)
    flats = step(0.50, 0.70, lie) * np.clip((372 - y) / 50.0, 0, 1) * ground
    over(pic, "#fbf0e0", (flats * 0.55).astype(F32))
    brushy = step(0.52, 0.76, noise(shape, (260, 9), seed + 22, 4)) * np.clip((y - 298) / 20.0, 0, 1) * np.clip((430 - y) / 90.0, 0, 1) * ground
    tint(pic, "#b4a694", (brushy * 0.42).astype(F32))
    # the shadows of two of the clouds lie across the far plain
    for (cy, cx, wd, ht, sd) in ((316, 300, 330, 5.0, 71), (332, 700, 240, 6.5, 72), (350, 60, 230, 9.0, 73)):
        cs = mask_ellipse(shape, cx, cy, wd, ht, soft=2.0, wobble=3.0, seed=seed + sd) * ground
        tint(pic, "#9a96cc", (cs * 0.58).astype(F32))
    # the lot in front of the shack: forty years of tires have packed it pale and hard
    lot = mask_poly(shape, [(30, 486), (110, 436), (330, 424), (520, 430), (606, 442), (700, 470), (742, 530), (690, 600), (0, 600)], soft=16, wobble=12, seed=seed + 23) * ground
    lot_light = lot * np.clip(1.25 - (y - 430) / 150.0, 0.25, 1.0)                    # palest in front of the shack, deepening toward us
    over(pic, vary("#eed2ae", shape, seed + 24, 0.05, 60), (lot_light * 0.46 * (0.7 + 0.5 * ground_tex(shape, 260.0, seed + 25))).astype(F32))
    # where cars have swung in off the road and round the pump, year after year: pale curving wheel ways
    for pts in ([(-640, 40), (-420, 300), (-250, 520), (-60, 600), (160, 610), (420, 520), (620, 300), (760, 60)],
                [(-700, 420), (-430, 560), (-200, 650), (40, 690), (260, 640), (420, 560)],
                [(-560, 760), (-360, 700), (-120, 560), (60, 380), (140, 160), (160, -60)]):
        for off in (-75.0, 75.0):
            way = [(px_ + off * 0.7, pz_ + off * 0.7) for px_, pz_ in pts]
            over(pic, "#f0d8b4", (strip(shape, way, 46.0, soft=2.2) * ground * 0.22 * (0.4 + 0.9 * noise(shape, (90, 20), seed + 28, 3))).astype(F32))
    # the trodden way from his door to his table
    over(pic, "#f2dec0", (strip(shape, [(-300, 930), (-230, 760), (-120, 600), (-40, 500)], 70.0, soft=3.0) * ground * 0.30).astype(F32))
    # old oil, by the pump
    for (ox, oz, rx_, rz_, sd) in ((-40, 730, 46, 30, 1), (-190, 716, 34, 20, 2), (30, 770, 22, 14, 3), (-110, 690, 18, 12, 4)):
        blot = ground_poly(shape, [(ox + math.cos(a) * rx_, oz + math.sin(a) * rz_) for a in np.linspace(0, 2 * math.pi, 16, endpoint=False)], soft=1.6, wobble=2.5, seed=seed + 80 + sd)
        tint(pic, "#7c6a64", (blot * 0.42).astype(F32))
    # sand the wind has laid against the foot of the fence
    for leg, s0, s1 in (("A", 0.0, 700.0), ("B", 0.0, 2400.0)):
        drift_ = [P.fworld(leg, s_, 34.0) for s_ in np.linspace(s0, s1, 8)]
        over(pic, "#f6e6cc", (strip(shape, drift_, 70.0, soft=2.0, steps=0) * ground * 0.34).astype(F32))

    # ---- the road, with its sandy shoulders
    shoulder = np.maximum(road_mask(shape, -0.22, 0.0, soft=2.5), road_mask(shape, 1.0, 1.22, soft=2.5)) * ground
    over(pic, "#f0dcc0", (shoulder * 0.30 * (0.5 + noise(shape, (60, 30), seed + 26, 3))).astype(F32))
    road = road_mask(shape, soft=0.8) * ground
    t = np.clip((y - HZ) / 200.0, 0, 1)
    asphalt = ramp(t, [(0.0, "#b9b2c4"), (0.25, "#9d98b0"), (1.0, "#807a94")])
    asphalt = asphalt * (1 + (ground_tex(shape, 300.0, seed + 27) - 0.5)[..., None] * 0.16)
    over(pic, asphalt, road)
    worn = np.maximum(road_mask(shape, 0.12, 0.34, soft=1.5), road_mask(shape, 0.64, 0.86, soft=1.5)) * road       # where the wheels run it is paler
    over(pic, "#b8b2c0", (worn * 0.30).astype(F32))
    land.haze(pic, HZ, "#f6dcc8", 0.50, 0.10, ground)

    # ---- the tracks, as broad soft marks, and the scorched ground round the glass
    for side in (-1, 1):
        r = rut(side)
        tint(pic, "#c09880", (strip(shape, r, 40.0, soft=2.0, steps=0) * ground * 0.32).astype(F32))
    gx, gz, grx, grz = GLASS
    ring = [gp(gx + math.cos(a) * (grx + 26), gz + math.sin(a) * (grz + 22)) for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)]
    tint(pic, "#9a6a58", (mask_poly(shape, ring, soft=5.0, wobble=5.0, seed=seed + 30) * 0.62).astype(F32))
    pool = [gp(gx + math.cos(a) * grx, gz + math.sin(a) * grz) for a in np.linspace(0, 2 * math.pi, 40, endpoint=False)]
    gm = mask_poly(shape, pool, soft=1.2, wobble=3.0, seed=seed + 31)
    glass = ramp(np.clip((y - 514) / 44.0, 0, 1), [(0.0, "#d4ecec"), (0.5, "#9cd0d8"), (1.0, "#6cb0c8")])
    over(pic, glass, gm)
    info["glass"] = gm

    # ---- the long shadows
    sh, info["on_island"] = shadows(shape)
    sh = np.maximum(sh, mask_poly(shape, [(520, 601), (600, 590), (700, 586), (760, 588), (800, 584), (800, 601)], soft=3.0, wobble=3.0, seed=seed + 33) * 0.85)
    tint(pic, SHADE, (sh * ground * (1 - gm * 0.5) * 0.62).astype(F32))
    over(pic, "#5c5c9c", (sh * ground * (1 - gm) * 0.15).astype(F32))                  # morning shade is cool: a little of the sky lies in it
    info["shadow"] = sh

    # ---- the bottom corners go deeper and warmer, to hold the eye in the picture
    corner = np.clip(((x - 400) / 400) ** 2 * 0.55 + ((y - 400) / 200).clip(0, 2) ** 2 * 0.6, 0, 1)
    tint(pic, "#b87c58", (corner * 0.40 * ground * (1 - gm)).astype(F32))
    tint(pic, "#c88a5c", (np.clip((y - 520) / 80.0, 0, 1) * 0.16 * ground * (1 - gm)).astype(F32))             # the nearest ground is the deepest
    glow(pic, "#fff0d0", (np.clip((x - 260) / 540.0, 0, 1) * np.clip((y - 330) / 120.0, 0, 1) * 0.09 * ground).astype(F32))    # and the light comes from the right
    glow(pic, "#ffe8c8", (np.clip(1 - np.abs(y - (HZ + 10)) / 34, 0, 1) * 0.10 * ground).astype(F32))       # dust in the air over the plain
    info.update(ground=ground, X=X, Z=Z, lot=lot, road=road)
    return np.clip(pic, 0, 1), info


# ---------------------------------------------------------------- pass 3
def lay(pic, draw, at, yaw=0.0, lift=0.0, fast=False, seed=4, sizes=(5, 3, 2), keep=0.45):
    """Paint one of the standing things into the backdrop: brushed, then its crisp lines."""
    shape = pic.shape[:2]
    c, a, lc, la = P.render(shape, draw, at, yaw, lift=lift)
    ys, xs = np.where(a > 0.5)
    under_color = np.median(pic[ys, xs], axis=0) if len(ys) else "#d8b890"
    pc, pa = brushed(c, a, lc, la, under_color, seed=seed, sizes=sizes, keep=keep, fast=fast)
    over(pic, pc, pa)
    return pa


BIRDS = [(486, 150, 5.0), (702, 60, 3.6)]                    # two birds high over the desert (round four: the game flies them)


def details(pic, info, seed=SEED, fast=False, as_approved=False):
    """The crisp things, over the brushwork. Round four: the two birds in the sky are no longer painted still (the game
    flies them); `as_approved=True` paints them in as the picture was approved, to work out its palette."""
    shape = (H, W)
    x, y = grid(shape)
    rng = np.random.default_rng(seed + 77)
    ground = info["ground"]

    # ---- first say the far country again, crisply: its edges were softened by the brush
    crisp = pic.copy()
    fm = far_country(crisp, seed)
    pic[...] = lerp(pic, crisp, (0.62 * fm * (y < HZ + 1))[..., None])
    line = Paper(shape)
    line.line([(0, HZ + 1.2), (W, HZ + 1.2)], "#c8a898", 1.0, 0.5)                    # where the plain ends

    # ---- the road: its edges, the broken yellow line, cracks, patches
    def lane(across, z0, z1, color, wd_cm, alpha):
        k = kz((z0 + z1) / 2)
        line.line([gp(road_x(z0, across), z0), gp(road_x(z1, across), z1)], color, max(0.5, wd_cm * k * 0.75), alpha)
    z = 300.0
    while z < 60000:
        lane(0.5, z, z + 300, "#f6cc4e", 15.0, 0.95 if z < 9000 else 0.6)
        z += 1200
    for across in (0.03, 0.97):
        for z0, z1 in ((300, 700), (760, 1500), (1640, 3200), (3500, 7000), (7600, 16000), (17000, 60000)):
            lane(across, z0, z1, "#f4ecdc", 10.0, 0.55)
    for z0, z1 in ((-200, 2400), (2500, 9000), (9000, 60000)):                        # the edge of the asphalt, bitten by the sand
        line.line([gp(road_x(zz, 0.0), zz) for zz in np.linspace(z0, z1, 6)], "#6a6278", 1.0, 0.6)
    for (zc, a0, a1, dz) in ((560, 0.02, 0.30, 90), (900, 0.55, 0.92, 120), (1500, 0.1, 0.45, 160), (2600, 0.5, 0.95, 260)):       # patches of newer tar
        q = [gp(road_x(zc, a0), zc), gp(road_x(zc, a1), zc), gp(road_x(zc + dz, a1 - 0.03), zc + dz), gp(road_x(zc + dz, a0 + 0.04), zc + dz)]
        line.poly(q, "#5e5a74", 0.55)
    for k_ in range(44):                                                              # cracks across it, tarred over more than once
        zc = 380 + rng.random() ** 2 * 9000
        a0, a1 = rng.uniform(0, 0.5), rng.uniform(0.5, 1.0)
        pts = [gp(road_x(zc + rng.normal(0, 26), a), zc + rng.normal(0, 22)) for a in np.linspace(a0, a1, 5)]
        line.line(pts, "#4a4662", max(0.55, 6.0 * kz(zc)), 0.72)
    for across, z0, z1 in ((0.22, 350, 1500), (0.30, 900, 2600), (0.74, 500, 2000), (0.66, 2200, 5200), (0.12, 1800, 4200)):       # and along it, where the wheels have broken it
        pts = [gp(road_x(zz, across + 0.012 * math.sin(zz * 0.011 + across * 9)), zz) for zz in np.linspace(z0, z1, 9)]
        line.line(pts, "#4a4662", 0.7, 0.6)
    for (zc, across, wd) in ((700, 0.06, 60), (1250, 0.10, 46), (2100, 0.04, 70)):                                                 # sand has crept in over the edge
        q = [gp(road_x(zc - wd, -0.02), zc - wd), gp(road_x(zc, across), zc), gp(road_x(zc + wd * 1.4, -0.02), zc + wd * 1.4)]
        line.poly(q, "#ecd4b4", 0.7)
    line.onto(pic)

    # ---- telephone poles, going away along the far side of the road
    poles = Paper(shape)
    tops = []
    for zp in POLES:
        x0 = road_x(zp, 1.0) - 150
        k = kz(zp)
        a, b = gp(x0, zp), gp(x0, zp, 850)
        poles.line([a, b], "#5a4a50", max(0.7, 26 * k))
        poles.line([(a[0] + max(0.4, 6 * k), a[1]), (b[0] + max(0.4, 6 * k), b[1])], "#e8c8a8", max(0.4, 7 * k), 0.8)
        l, r = gp(x0 - 130, zp, 800), gp(x0 + 130, zp, 800)
        poles.line([l, r], "#5a4a50", max(0.6, 14 * k))
        tops.append((l, r, k))
    for (l0, r0, k0), (l1, r1, k1) in zip(tops[:-1], tops[1:]):                       # the wires sag between them
        for p0, p1 in ((l0, l1), (r0, r1)):
            mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + 60 * (k0 + k1) / 2)
            poles.line(curve([p0, mid, p1], 6), "#4a4458", 0.45, 0.7)
    l0, r0, k0 = tops[0]
    for p0, drop in ((l0, 90), (r0, 60)):                                             # and run off the edge toward us
        poles.line(curve([p0, ((p0[0] - 10) / 2, p0[1] - 8 + drop * k0), (-12, p0[1] - 50)], 6), "#4a4458", 0.45, 0.7)
    for (bx, by, bw) in (BIRDS if as_approved else ()):
        poles.line([(bx - bw, by - bw * 0.35), (bx - bw * 0.3, by - bw * 0.05), (bx, by + bw * 0.25), (bx + bw * 0.4, by - bw * 0.15), (bx + bw * 1.1, by - bw * 0.5)], "#2e3a5c", 0.9, 0.85)
    poles.onto(pic)

    # ---- the scrub, far to near: far off only flecks, nearer small grey bushes, each with its shadow to
    # the left; in drifts, never evenly, and none where the wheels and the feet have been
    scrub = Paper(shape)
    keep_out = np.maximum(info["lot"], blur(info["road"], 3) * 2).clip(0, 1)
    lane = np.zeros(shape, dtype=F32)                                                 # keep the way the tracks came clear too
    for side in (-1, 1):
        lane = np.maximum(lane, strip(shape, rut(side), 150.0, soft=2.0, steps=0))
    drift = noise(shape, (130, 12), seed + 40, 3)
    n = 0
    for _ in range(9000):
        if n >= 700:
            break
        py = HZ + 4 + (176 - 4) * rng.random() ** 1.9
        px = rng.random() * W
        iy, ix = int(min(py, H - 1)), int(px)
        if keep_out[iy, ix] > 0.2 or lane[iy, ix] > 0.2 or drift[iy, ix] < 0.40 + 0.3 * rng.random():
            continue
        k = (py - HZ) / 328.0
        r = max(0.7, k * rng.uniform(11, 27))                                         # a bush is 25 to 55 cm across
        kind = rng.random()                                                           # sage mostly; some dead and brown; some rabbitbrush, yellow at the tips
        col = mix("#8a8e78", "#b4b49a", rng.random()) if kind < 0.6 else (mix("#9a8870", "#c8b490", rng.random()) if kind < 0.82 else mix("#96a064", "#c6c47c", rng.random()))
        dark = "#5c6454" if kind < 0.6 else ("#6a5a50" if kind < 0.82 else "#5e6a40")
        if r < 1.6:                                                                   # far off: a fleck and its shadow
            scrub.line([(px - r * 2.2, py + 0.3), (px, py + 0.3)], "#8f84ac", max(0.5, r * 0.5), 0.45)
            scrub.line([(px - r, py - 0.4), (px + r, py - 0.4)], mix(col, "#6a7060", 0.4), max(0.6, r * 0.9), 0.85)
        else:
            flat = rng.uniform(0.46, 0.72)
            scrub.ellipse(px - r * 1.8, py + r * 0.05, r * 2.0, max(0.5, r * 0.24), "#8f84ac", 0.34)
            for j in range(3):                                                        # a low mound of two or three dabs, lit from the right
                ox, oy, rr = rng.normal(0, r * 0.38), -abs(rng.normal(0, r * 0.18)), r * rng.uniform(0.5, 0.9)
                scrub.ellipse(px + ox, py - rr * 0.55 + oy, rr, rr * flat, mix(col, dark, 0.48 - 0.16 * j))
            scrub.ellipse(px + r * 0.35, py - r * 0.72, r * 0.55, r * 0.30, tone(col, 1.16, 0.02), 0.9)
            if r > 2.6:                                                               # near enough to see its twigs
                for j in range(int(4 + r)):
                    a = math.radians(rng.uniform(20, 160))
                    l = r * rng.uniform(0.5, 1.15)
                    bx_, by_ = px + rng.normal(0, r * 0.4), py - r * rng.uniform(0.2, 0.6)
                    scrub.line([(bx_, by_), (bx_ + math.cos(a) * l * 0.6, by_ - math.sin(a) * l * 0.6)], tone(col, 1.22, 0.02) if math.cos(a) > -0.2 else mix(col, dark, 0.6), 0.6, 0.85)
        n += 1
    scrub.onto(pic)
    near_scrub = Paper(shape)
    for (bx, by, br, sd) in ((122, 453, 11, 1), (88, 463, 8, 2), (758, 434, 8, 4), (790, 427, 6, 5), (16, 508, 12, 9)):
        tint(pic, SHADE, (mask_ellipse(shape, bx - br * 1.9, by - br * 0.10, br * 2.0, br * 0.26, soft=0.8) * 0.42).astype(F32))
        sagebrush(near_scrub, bx, by, br, seed + 60 + sd)
    for (tx, ty, tr_, sd) in ((60, 478, 9, 1), (140, 458, 7, 2), (150, 437, 6, 3), (204, 443, 6, 4), (418, 458, 5, 5), (286, 461, 6, 6), (402, 462, 5, 7), (604, 440, 6, 8), (640, 441, 5, 9),
                              (706, 446, 6, 10), (770, 449, 7, 11), (32, 462, 7, 12), (106, 448, 6, 13), (346, 430, 5, 14), (590, 420, 5, 15), (598, 405, 4, 16)):
        tuft(near_scrub, tx, ty, tr_, seed + 300 + sd)
    near_scrub.onto(pic)

    # ---- dried mud: the lot has cracked into plates
    d_, below = crackle(shape, 46.0, seed + 41)
    kpx = np.clip((y - HZ) / 328.0, 0, 1)
    wide = 1.3 / np.maximum(kpx, 0.05)                                                # a crack about a pixel wide wherever it is
    crack = np.clip(1 - d_ / wide, 0, 1) * np.clip((kpx - 0.38) * 5, 0, 1)
    patch = step(0.46, 0.66, ground_tex(shape, 330.0, seed + 42)) * (1 - info["glass"]) * (1 - info["road"])
    tint(pic, "#8e6850", (crack * patch * 0.5 * ground).astype(F32))

    # ---- stones (the sun is on the right, so they are painted in a mirror and turned round)
    stones = Sheet(shape)
    flip = pic[:, ::-1]
    zone = ((ground > 0.5) & (y > 330) & (info["glass"] < 0.1) & (info["road"] < 0.5))[:, ::-1]
    land.stones(stones, flip, HZ, seed + 90, 110, zone=zone, ground=np.ascontiguousarray(ground[:, ::-1]), size=(0.7, 3.0),
                tones=("#fff0d4", "#e2c8a4", "#a48c84", "#6a5868"))
    sc, sa = stones.done()
    over(pic, sc[:, ::-1], sa[:, ::-1])
    big = Sheet(shape)
    for (rx_, ry_, rr) in ((300, 597, 9), (428, 600, 8), (612, 597, 7), (62, 507, 6), (186, 473, 4), (20, 596, 8), (522, 446, 3), (704, 452, 3.5)):
        land.rock_shadow(flip, W - 1 - rx_, ry_, rr * 1.25, rr * 0.85, color=SHADE, amount=0.5, reach=1.9)
        land.rock(big, rx_, ry_, rr * 1.25, rr * 0.85, seed + rx_, tones=("#fff0d4", "#e6c8a0", "#a88c80", "#685664"), light=1)
    big.onto(pic)

    # ---- the tracks: two ruts pressed in the sand, each with a shaded wall and a lit lip, and the print
    # of the tread where they are near enough to see. They are a day old: the edges have begun to crumble.
    tr = Paper(shape)
    px_, pz_ = TRACK_DIR[1], -TRACK_DIR[0]
    for side in (-1, 1):
        r = rut(side, 90)
        for i, ((ax, az), (bx, bz)) in enumerate(zip(r[:-1], r[1:])):
            k = kz((az + bz) / 2)
            if k < 0.045:
                break
            fade = min(1.0, k / 0.34) * (0.75 + 0.5 * rng.random())
            w0, w1 = rng.normal(0, 1.6), rng.normal(0, 1.6)
            tr.line([gp(ax, az), gp(bx, bz)], "#b08468", max(0.6, 22.0 * k * 0.62), 0.30 * fade, round_ends=False)                          # the pressed floor of the rut
            if rng.random() > 0.12:
                tr.line([gp(ax + px_ * (11 + w0), az + pz_ * (11 + w0)), gp(bx + px_ * (11 + w1), bz + pz_ * (11 + w1))], "#86604e", max(0.4, 3.4 * k), 0.62 * fade)   # the wall the sun does not reach
            if rng.random() > 0.2:
                tr.line([gp(ax - px_ * (13 + w0), az - pz_ * (13 + w0)), gp(bx - px_ * (13 + w1), bz - pz_ * (13 + w1))], "#fff2d6", max(0.4, 3.0 * k), 0.55 * fade)   # the lip that it does
        zz, j = TRACK[0][1] + 6, 0
        while zz < 1080:                                                              # the tread: short bars, slanting one way then the other
            cxw = TRACK[0][0] + (zz - TRACK[0][1]) * TRACK_DIR[0] / TRACK_DIR[1] + side * 75.0 * px_
            czw = zz + side * 75.0 * pz_
            k = kz(czw)
            s_ = 1 if j % 2 else -1
            if rng.random() > 0.25:
                tr.line([gp(cxw - 7, czw - 3.5 * s_), gp(cxw + 7, czw + 3.5 * s_)], "#94705c", max(0.4, 2.6 * k), 0.34 * min(1.0, k / 0.5))
            zz += 11.0
            j += 1
    far_trail = curve([gp(*q) for q in TRACK[4:]], 10)                                # far off, where they swung in from the road: only a thread
    for i in range(0, len(far_trail) - 1):
        if rng.random() > 0.18:
            tr.line([far_trail[i], far_trail[i + 1]], "#b08a7c", 0.8, 0.5)
            tr.line([(far_trail[i][0], far_trail[i][1] - 0.8), (far_trail[i + 1][0], far_trail[i + 1][1] - 0.8)], "#fff4e0", 0.5, 0.35)
    tr.onto(pic)

    # ---- the glass: where the sand was fused. It holds the sky, and the fence upside down.
    gl = Paper(shape)
    gx, gz, grx, grz = GLASS

    def lip(a, f=1.0, g=1.0):
        w = 1 + 0.07 * math.sin(a * 3 + 1.0) + 0.05 * math.sin(a * 7 + 2.0)
        return gp(gx + math.cos(a) * grx * f * w, gz + math.sin(a) * grz * g * w)
    angs = np.linspace(0, 2 * math.pi, 48, endpoint=False)
    gl.poly([lip(a, 1.15, 1.20) for a in angs], "#7a5448", 0.6)                        # scorched crust, burnt dark at the lip
    gl.poly([lip(a, 1.05, 1.07) for a in angs], "#3a2c34", 0.85)
    gl.poly([lip(a) for a in angs], "#86c6cc")
    gl.onto(pic)
    # the sky in it: deep blue from overhead and the rose of a cloud, drawn out in level streaks
    sky_in = sample(info["sky"], x + (noise(shape, (30, 4), seed + 50, 3) - 0.5) * 18, 236 - (y - 514) * 4.4)
    inner = mask_poly(shape, [lip(a, 0.95, 0.93) for a in angs], soft=1.0)
    over(pic, lerp(sky_in, rgb("#c4ecdc"), 0.30), (inner * 0.92).astype(F32))
    gl = Paper(shape)
    c0 = gp(gx, gz)
    over(pic, "#4a8c78", (inner * np.clip((y - c0[1] + 2) / 17.0, 0, 1) * 0.30).astype(F32))    # toward us we see down into it: bottle green
    far_lip = lip(math.pi / 2, 0.9, 0.9)
    for sp in (0.0, 300.0):                                                            # two posts and the notice stand in it, upside down
        fx_, fy_ = P.fpt("A", sp)
        tx = c0[0] + (fx_ - 662.0) * 0.62
        gl.line([(tx, far_lip[1] + 1), (tx + 1.5, far_lip[1] + 9), (tx - 0.5, far_lip[1] + 17)], "#c8d0dc", 1.5, 0.55)
    gl.poly([(c0[0] - 17, far_lip[1] + 3), (c0[0] - 2, far_lip[1] + 3.4), (c0[0] - 3, far_lip[1] + 10.5), (c0[0] - 16, far_lip[1] + 11)], "#f4f0e6", 0.42)
    gl.poly([(c0[0] + 2, far_lip[1] + 3.8), (c0[0] + 17, far_lip[1] + 3.5), (c0[0] + 18, far_lip[1] + 10), (c0[0] + 3, far_lip[1] + 10.8)], "#f4f0e6", 0.36)
    gl.line([(c0[0] - 16, far_lip[1] + 11), (c0[0] + 18, far_lip[1] + 10.4)], "#d05a48", 1.6, 0.45)
    for a in (0.45, 1.25, 2.3, 3.2, 4.15, 5.3):                                        # it cracked as it cooled
        p1 = lip(a, 0.97, 0.97)
        mid = ((c0[0] * 0.45 + p1[0] * 0.55) + rng.normal(0, 3), (c0[1] * 0.45 + p1[1] * 0.55) + rng.normal(0, 1))
        st = (c0[0] + (p1[0] - c0[0]) * 0.10, c0[1] + (p1[1] - c0[1]) * 0.10)
        gl.line([st, mid, p1], "#24506a", 0.6, 0.75)
        gl.line([(st[0] + 0.8, st[1] + 0.7), (mid[0] + 0.8, mid[1] + 0.7), (p1[0] + 0.8, p1[1] + 0.7)], "#f4ffff", 0.5, 0.7)
    gl.line([lip(a, 0.55, 0.5) for a in np.linspace(3.6, 5.4, 8)], "#24506a", 0.5, 0.5)
    gl.line([lip(a, 0.74, 0.70) for a in np.linspace(2.5, 3.9, 8)], "#24506a", 0.5, 0.55)
    gl.line([lip(a, 0.36, 0.34) for a in np.linspace(5.6, 7.2, 7)], "#24506a", 0.5, 0.5)
    gl.line([lip(a, 0.36, 0.34) for a in np.linspace(5.7, 7.1, 7)][::1], "#f4ffff", 0.4, 0.4)
    gl.line([lip(a, 0.99, 0.99) for a in np.linspace(0.35, 2.8, 14)], "#f8ffff", 1.0, 0.9)      # the far lip shines
    gl.line([lip(a, 1.0, 1.0) for a in np.linspace(3.4, 6.0, 16)], "#22404e", 1.7, 0.85)        # the near edge shows how thick it is
    gl.line([lip(a, 0.96, 0.88) for a in np.linspace(3.6, 5.8, 14)], "#d8fff4", 0.8, 0.65)
    for (ux, uz, l) in ((-0.5, -0.25, 9), (0.3, 0.2, 12), (0.56, -0.4, 7)):                      # and it glitters
        p = gp(gx + ux * grx, gz + uz * grz)
        gl.line([(p[0] - l, p[1]), (p[0] + l, p[1])], "#ffffff", 0.8, 0.9)
        gl.line([(p[0], p[1] - l * 0.45), (p[0], p[1] + l * 0.45)], "#ffffff", 0.8, 0.9)
        gl.ellipse(p[0], p[1], 1.4, 1.2, "#ffffff")
    for a in np.linspace(0, 2 * math.pi, 22, endpoint=False):                           # beads of glass thrown out round it
        p = lip(a + rng.normal(0, 0.1), 1.2 + rng.random() * 0.25, 1.25 + rng.random() * 0.3)
        gl.ellipse(p[0], p[1], 1.6, 0.9, "#3e3038", 0.8)
        gl.ellipse(p[0] + 0.5, p[1] - 0.4, 0.8, 0.5, "#c8f0f0", 0.9)
    gl.onto(pic)

    # ---- the things that are built, each brushed and then drawn crisp
    isl = lay(pic, P.draw_island, P.PUMP_AT, fast=fast, seed=3)
    tint(pic, SHADE, (info["on_island"] * (isl > 0.5) * 0.6).astype(F32))                # the umbrella's shadow lies across the island too
    info["shack"] = lay(pic, P.draw_shack, P.SHACK_AT, P.SHACK_YAW, fast=fast, seed=5)
    lay(pic, P.draw_shack_side, P.SHACK_AT, P.SHACK_YAW, fast=fast, seed=6)
    lay(pic, P.draw_mailbox, P.MAIL_AT, fast=fast, seed=7, sizes=(3, 2), keep=0.5)
    lay(pic, P.draw_signpole, P.SIGN_AT, fast=fast, seed=8, sizes=(4, 2), keep=0.5)

    clutter(pic, info, seed)

    # ---- the fence, wire by wire
    fence = Paper(shape)
    notes = []
    P.draw_fence(fence, notes)
    fc, fa = fence.done()
    P.letter_on(fc, fa, notes)
    over(pic, fc, fa)
    return pic


def clutter(pic, info, seed=SEED):
    """What people left lying about: by the corner of the fence, what was over when the men in grey went
    home (cement, a roll of wire, two posts, a cone); a tire half sunk in the lot; a tumbleweed the fence
    caught in the night."""
    shape = pic.shape[:2]
    rng = np.random.default_rng(seed + 123)
    for (cx, cy, rx, ry) in ((566, 428.5, 18, 2.6), (584, 432.5, 14, 2.4), (586, 436.5, 8, 2.0), (228, 451.5, 16, 3.0), (716, 441.5, 14, 2.6)):      # their shadows
        tint(pic, SHADE, (mask_ellipse(shape, cx, cy, rx, ry, soft=0.8) * 0.5).astype(F32))
    sh = Paper(shape)
    for a, b in (((372, 1062), (500, 1150)), ((388, 1048), (512, 1128))):              # two posts they did not need
        sh.line([gp(*a), gp(*b)], STEEL_DARK, 2.0)
        sh.line([gp(a[0], a[1], 4), gp(b[0], b[1], 4)], "#e8e8e4", 1.0, 0.9)
    d = Solid(sh, (420, 1040), yaw=18)                                                # sacks of cement, one split
    d.box(-30, 30, 0, 13, -20, 20, "#a8a096", "#dcd4c4", "#c4bcae", back="#8a8490")
    d2 = Solid(sh, (424, 1036), yaw=-12, lift=13)
    d2.box(-29, 29, 0, 12, -19, 19, "#b0a89c", "#e8e0d0", "#ccc4b6", back="#908a96")
    d2.line([(-8, 12, -19), (-8, 0, -19)], "#7a6a8c", 2.0, 0.8)
    d.poly([(30, 0, -30), (62, 0, -22), (48, 0, 6), (28, 0, 2)], "#c8c4c0", 0.8)        # and what ran out of it
    d = Solid(sh, (462, 1000), yaw=-8)                                                 # a roll of chain link, on its side
    d.poly([(-56, 0, -20), (56, 0, -20), (56, 42, -20), (-56, 42, -20)], "#8c90a4")
    d.poly([(-56, 30, -20), (56, 30, -20), (56, 42, -20), (-56, 42, -20)], "#d4d8e0")
    d.poly([(-56, 0, -20), (56, 0, -20), (56, 12, -20), (-56, 12, -20)], "#62667c")
    d.poly([(-56, 21 + math.sin(a) * 21, math.cos(a) * 21) for a in np.linspace(0, 2 * math.pi, 16)], "#787c92")
    d.poly([(-56.5, 21 + math.sin(a) * 9, math.cos(a) * 9) for a in np.linspace(0, 2 * math.pi, 12)], "#3c3c4c")
    for xx in np.arange(-48, 56, 9):
        d.line([(xx, 1, -20.4), (xx + 8, 41, -20.4)], "#4e5268", 1.2, 0.6)
        d.line([(xx + 8, 1, -20.4), (xx, 41, -20.4)], "#f0f0f0", 1.0, 0.45)
    d = Solid(sh, (452, 930))                                                          # a cone
    d.poly([(-13, 0, 0), (13, 0, 0), (13, 3, 0), (-13, 3, 0)], "#c85a28")
    d.poly([(-9, 3, 0), (9, 3, 0), (2.4, 52, 0), (-2.4, 52, 0)], "#f08030")
    d.poly([(1, 3, 0), (9, 3, 0), (2.4, 52, 0), (0.6, 52, 0)], "#ffa858")
    d.poly([(-6.2, 22, 0), (6.2, 22, 0), (4.6, 34, 0), (-4.6, 34, 0)], "#fff4e4")
    d = Solid(sh, (-336, 764))                                                         # the tire
    d.hdisc(0, 9, 0, 33, "#2a2630")
    d.poly(d.hring(0, 9, 0, 33, n=20, a0=180, a1=360) + d.hring(0, 0, 0, 33, n=20, a0=360, a1=180), "#1a1820")
    d.poly(d.hring(8, 9.4, 0, 33, n=14, a0=-70, a1=70) + d.hring(8, 9.4, 0, 26, n=14, a0=70, a1=-70), "#6c6474", 0.8)
    d.hdisc(0, 9.5, 0, 19, "#d8b890")
    d.hdisc(-3, 9.6, 2, 13, "#b8947a", 0.6)
    sh.onto(pic)
    tw = Paper(shape)                                                                  # the tumbleweed: a ball of dry twigs you can see through
    cx, cy, r = 730.0, 433.5, 8.0
    for i in range(46):
        a0, a1 = rng.uniform(0, 2 * math.pi), rng.uniform(0, 2 * math.pi)
        r0, r1 = r * rng.uniform(0.5, 1.0), r * rng.uniform(0.5, 1.0)
        p0, p1 = (cx + math.cos(a0) * r0, cy + math.sin(a0) * r0 * 0.9), (cx + math.cos(a1) * r1, cy + math.sin(a1) * r1 * 0.9)
        mid = ((p0[0] + p1[0]) / 2 + rng.normal(0, 2), (p0[1] + p1[1]) / 2 + rng.normal(0, 2))
        lit_ = (p0[0] + p1[0]) / 2 > cx - 1
        tw.line(curve([p0, mid, p1], 4), mix("#7a6248", "#f0d8a0", rng.random() * (1.0 if lit_ else 0.4)), 0.55, 0.85)
    tw.onto(pic)
    return pic


STEEL_DARK = "#8c90a4"


# ---------------------------------------------------------------- the cut-outs
def cut(back, draw, at, yaw=0.0, lift=0.0, fast=False, seed=4, sizes=(6, 3, 2), keep=0.42):
    """A thing people can walk behind: painted on a clear sheet the size of the picture. -> (color, alpha)."""
    shape = back.shape[:2]
    c, a, lc, la = P.render(shape, draw, at, yaw, lift=lift)
    ys, xs = np.where(a > 0.5)
    under_color = np.median(back[ys, xs], axis=0)
    return brushed(c, a, lc, la, under_color, seed=seed, sizes=sizes, keep=keep, fast=fast)


def front_plane(back, fast=False, seed=SEED):
    """Right at the front, bottom right: sagebrush, and the drum standing in it."""
    shape = back.shape[:2]
    s = Paper(shape)
    back_tones = ("#2c342e", "#4c5848", "#7c8a70", "#b4bc9c")
    sagebrush(s, 716, 612, 50, seed + 1, tones=back_tones)
    sagebrush(s, 800, 598, 44, seed + 2, tones=back_tones)
    c0, a0 = s.done()
    dc, da = cut(back, P.draw_drum, P.DRUM_AT, fast=fast, seed=9, sizes=(6, 3, 2), keep=0.4)
    over(c0, dc, da)
    a0 = np.maximum(a0, da)
    s = Paper(shape)
    sagebrush(s, 668, 626, 44, seed + 3, tones=("#232a26", "#3e4a3e", "#6c7a64", "#aab494"))
    sagebrush(s, 792, 640, 56, seed + 4, tones=("#232a26", "#3e4a3e", "#6c7a64", "#aab494"))
    tuft(s, 742, 604, 22, seed + 5)
    tuft(s, 634, 603, 16, seed + 6)
    c1, a1 = s.done()
    over(c0, c1, a1)
    return c0, np.maximum(a0, a1)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02, keep=None):
    """Grain, then the limited palette. `keep` (round four) is the picture as approved: the palette is worked out from
    it exactly as before, every pixel where `picture` is the same keeps its old index, and only the changed places are
    reduced again (with that palette)."""
    g = grain(picture if keep is None else keep, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    if keep is not None:
        changed = np.abs(picture - keep).max(axis=2) > 0.5 / 255
        idx = np.where(changed, to_palette(grain(picture, seed, amount), pal, speckle=speckle), idx)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def box_of(alpha, pad=0):
    ys, xs = np.where(alpha > 0.5)
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 1 + 2 * pad, int(ys.max() - ys.min()) + 1 + 2 * pad]


def fx_marks():
    """Round four: what moves by nature here, for the game to draw moving (layout.json "fx"), in the engine's own terms
    (js/engine/effects.js)."""
    shack = Solid(None, P.SHACK_AT, P.SHACK_YAW)
    pipe = shack.pt(316, 356, 190)                                    # under the stovepipe's cap
    foot = shack.pt(0, 0, 0)                                          # the shack's front left corner, on the ground
    return [
        {"type": "birds", "kind": "flyers", "id": "birds", "lanes": [[[-20, 168], [820, 128]], [[820, 54], [-20, 92]], [[-20, 112], [820, 70]]],
         "every": [25, 55], "group": [1, 2], "speed": 34, "color": "#2e3a5c", "size": [7, 10],
         "frames": {"glide": "bird-0.png", "flap": ["bird-1.png", "bird-0.png", "bird-2.png", "bird-0.png"], "bank": "bird-3.png", "middle": [7.0, 5.5]},
         "what": "two big dark birds (ravens, or a hawk) high over the desert, crossing slowly now and then: a long glide, a few slow beats. The painting "
                 "had them still at [486, 150] and [702, 60], 7 and 10 px across. No base: they are behind everything"},
        {"type": "smoke", "id": "stovepipe", "at": [round(pipe[0], 1), round(pipe[1], 1)], "base": int(round(foot[1])),
         "color": "#e6e2ea", "opacity": 0.30, "height": 46, "width": [1.5, 7], "lean": [4, -46], "rate": 2, "new": True,
         "what": "NEW (nothing was painted here): the old-timer has his coffee on, so a thin thread of woodsmoke from the stovepipe on the shack's roof. "
                 "There is no wind this morning (the painting's own note: the wind sock hangs slack), so it rises nearly straight and spreads at the top"},
    ]


def layout(planes, info):
    """The numbers the game needs, taken from the picture as painted."""
    r = lambda p: [int(round(p[0])), int(round(p[1]))]
    shack = Solid(None, P.SHACK_AT, P.SHACK_YAW)
    n0, n1, nb, nt = P.NOTICE
    notice = [r(P.fpt("A", n0, nb)), r(P.fpt("A", n1, nb)), r(P.fpt("A", n1, nt)), r(P.fpt("A", n0, nt))]
    gx, gz, grx, grz = GLASS
    gc = gp(gx, gz)
    glass = [int(round(gc[0])), int(round(gc[1])), int(round(grx * kz(gz))), int(round((gp(gx, gz - grz)[1] - gp(gx, gz + grz)[1]) / 2))]
    fence_a = [r(P.fpt("A", 0)), r((800, P.fpt("A", 400)[1])), r((800, P.fpt("A", 400, 250)[1])), r(P.fpt("A", 0, 250))]
    car_base = [[0, 592], r(gp(P.CAR_AT[0] + 394, P.CAR_AT[1] + P.CAR_W))]
    nose_far, nose_near = gp(P.CAR_AT[0] + 398, P.CAR_AT[1] + P.CAR_W + 6), gp(P.CAR_AT[0] + 398, P.CAR_AT[1] - 8)
    car_block = [[0, int(nose_far[1]) - 2], [int(nose_far[0]) + 3, int(nose_far[1]) - 2], [int(nose_near[0]) + 6, 596], [0, 596]]
    agent, agent2 = [661, 458], [752, 468]
    out = {
        "id": "nevada-roadside", "horizon": HZ, "full": FULL,
        "light": "early morning sun, low from the right and a little behind us: shadows fall to the left",
        "walk": [[0, 470], [40, 464], [104, 458], [150, 450], [262, 444], [270, 461], [410, 461], [414, 448], [540, 444], [600, 441], [640, 446], [760, 452], [800, 455],
                 [800, 498], [738, 506], [722, 560], [652, 588], [600, 596], [0, 596]],
        "blocked": [car_block,
                    [[410, 474], [546, 474], [548, 497], [408, 497]]],
        "planes": [
            {"id": "pump", "file": "pump.png", "base": 452},
            {"id": "stand", "file": "stand.png", "base": 493},
            {"id": "car", "file": "car.png", "base": car_base},
            {"id": "front", "file": "front.png", "plane": "front"},
        ],
        "things": [
            {"id": "car", "what": "Mom's car", "shape": {"rect": box_of(planes["car"][1])}, "stand": [int(nose_near[0]) + 36, 588], "face": "W"},
            {"id": "shack", "what": "the shack: LAST STOP", "shape": {"rect": box_of(info["shack"])}, "stand": [254, 449], "face": "N"},
            {"id": "pump", "what": "the gas pump", "shape": {"rect": box_of(planes["pump"][1], 2)}, "stand": [346, 466], "face": "N"},
            {"id": "oldtimer", "what": "the old-timer in his lawn chair (drawn by the game)", "shape": {"rect": [OLDTIMER[0] - 26, OLDTIMER[1] - 86, 52, 90]}, "stand": [432, 528], "face": "NW"},
            {"id": "stand", "what": "the lemonade stand", "shape": {"rect": box_of(planes["stand"][1])}, "stand": [486, 522], "face": "N"},
            {"id": "fence", "what": "the fence: its far side, its corner, and the top of its near side with the barbed wire (the notice and the men are kept out of this shape)",
             "shape": {"poly": [r(P.fpt("B", 2400)), r(P.fpt("B", 2400, 250)), r(P.fpt("A", 0, 280)), [800, int(P.fpt("A", 400, 280)[1])], [800, 354], [int(P.fpt("A", n0 - 6)[0]), 354],
                                r(P.fpt("A", n0 - 6)), r(P.fpt("A", 0))]},
             "stand": [590, 456], "face": "N"},
            {"id": "notice", "what": "the notice on the fence: AREA CLOSED", "shape": {"poly": notice}, "stand": [646, 472], "face": "N"},
            {"id": "agent", "what": "the man in gray, in front of the notice (drawn by the game)", "shape": {"rect": [agent[0] - 16, agent[1] - 92, 32, 96]}, "stand": [626, 476], "face": "NE"},
            {"id": "agent2", "what": "the man in gray, after he has backed off along the fence (drawn by the game)", "shape": {"rect": [agent2[0] - 16, agent2[1] - 98, 32, 102]}, "stand": [708, 482], "face": "E"},
            {"id": "tracks", "what": "where the tracks stop: the ruts from the fence to the glass, and the glass", "shape": {"poly": [[604, 466], [712, 466], [732, 520], [730, 548], [650, 560], [566, 546], [564, 522]]},
             "stand": [548, 548], "face": "E"},
        ],
        "exits": [],
        "marks": {"oldtimer": list(OLDTIMER), "agent": agent, "agent2": agent2, "mom": [268, 572], "bigsis": [318, 588], "lilsis": [232, 554],
                  "at_the_glass": {"mom": [548, 548], "bigsis": [574, 572], "lilsis": [524, 574]}},
        "glass": glass,
        "over_the_glass": [glass[0], glass[1] - 52],
        "over_the_glass_is": "a place in the air above the glass, for whatever the game opens there",
        "glass_is": "[middle x, middle y, half width, half height] of the patch of fused sand; it lies in the sun",
        "fence_side": {"poly": fence_a, "what": "the whole of the fence's near side, to the right edge"},
        "tracks_run": [r(gp(*TRACK[0])), r(gp(*TRACK[1])), r(gp(*TRACK[2])), r(gp(*TRACK[3]))],
        "old_grid": "the old 320x200 scene put its things, left to right: car, shack, pump, oldtimer, stand, fence, tracks, notice, agent, agent2. The same order holds here.",
        "fx": fx_marks(),
        "fx_note": "round four: the two birds that were painted still in the sky are gone from back.png (every other pixel is as it was); 'fx' flies them, and adds "
                   "a thread of smoke from the stovepipe (new). Left still on purpose: the wind sock, the umbrella, the hanging GAS sign and the tumbleweed in the "
                   "fence: there is no wind this morning, and the wind sock hangs slack to say so.",
    }
    return out


def check(whole, lay_):
    """The comp with the layout drawn on it and grey people of the right size standing on the marks."""
    from PIL import ImageDraw
    im = Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.polygon([tuple(p) for p in lay_["walk"]], outline=(40, 220, 255, 255))
    for b in lay_["blocked"]:
        d.polygon([tuple(p) for p in b], outline=(255, 60, 60, 255), fill=(255, 60, 60, 40))
    for t in lay_["things"]:
        sh = t["shape"]
        if "rect" in sh:
            x, y, w, h = sh["rect"]
            d.rectangle([x, y, x + w, y + h], outline=(255, 255, 0, 255))
        else:
            d.polygon([tuple(p) for p in sh["poly"]], outline=(255, 255, 0, 255))
        sx, sy = t["stand"]
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 0, 255, 255))
        d.text((sx + 5, sy - 5), t["id"], fill=(0, 0, 0, 255))

    def person(at, tall=1.0, col=(90, 90, 110, 200), seated=False):
        x, y = at
        hgt = 160.0 * (y - HZ) / (FULL - HZ) * tall * (0.74 if seated else 1.0)
        wd = hgt * 0.26
        d.rectangle([x - wd / 2, y - hgt * 0.86, x + wd / 2, y], fill=col)
        d.ellipse([x - hgt * 0.07, y - hgt, x + hgt * 0.07, y - hgt * 0.86], fill=col)
    m = lay_["marks"]
    person(m["oldtimer"], seated=True)
    person(m["agent"], col=(110, 110, 120, 210))
    person(m["agent2"], col=(110, 110, 120, 120))
    person(m["mom"], 0.95, (60, 150, 110, 210))
    person(m["bigsis"], 0.88, (110, 110, 200, 210))
    person(m["lilsis"], 0.64, (230, 110, 140, 210))
    for who, tall, col in (("mom", 0.95, (60, 150, 110, 120)), ("bigsis", 0.88, (110, 110, 200, 120)), ("lilsis", 0.64, (230, 110, 140, 120))):
        person(m["at_the_glass"][who], tall, col)
    for pl in lay_["planes"]:
        b = pl.get("base")
        if isinstance(b, (int, float)):
            d.line([0, b, 800, b], fill=(255, 140, 0, 110))
        elif b:
            d.line([tuple(b[0]), tuple(b[1])], fill=(255, 140, 0, 255), width=2)
    im.alpha_composite(ov)
    im.convert("RGB").save(OUT + "-check.png")


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    fast = "fast" in sys.argv
    base, info = under()
    info["sky"] = base.copy()
    Image.fromarray((base * 255).astype(np.uint8)).save(OUT + "-1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.22)
    print("brushed", round(time.time() - t0, 1))
    approved = pic.copy()
    details(approved, info, fast=fast, as_approved=True)              # as approved, with the birds painted in: for the palette
    details(pic, info, fast=fast)
    print("details", round(time.time() - t0, 1))
    planes = {}
    planes["pump"] = cut(pic, P.draw_pump, P.PUMP_AT, lift=P.ISLAND[4], fast=fast, seed=11, sizes=(5, 3, 2))
    planes["stand"] = cut(pic, P.draw_stand, P.STAND_AT, fast=fast, seed=12, sizes=(5, 3, 2), keep=0.45)
    planes["car"] = cut(pic, P.draw_car, P.CAR_AT, fast=fast, seed=13, sizes=(7, 4, 2))
    planes["front"] = front_plane(pic, fast=fast)
    whole = pic.copy()
    for name in ("pump", "stand", "car", "front"):
        c, a = planes[name]
        over(whole, c, (a > 0.5).astype(F32))
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-all.png")
    lay_ = layout(planes, info)
    check(whole, lay_)
    with open(OUT + "/layout.json", "w") as f:
        json.dump(lay_, f, indent=1)
    print("painted", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    print("back", finish(pic, OUT + "/back.png", 152, keep=approved))
    print("pump", finish(planes["pump"][0], OUT + "/pump.png", 48, planes["pump"][1]))
    print("stand", finish(planes["stand"][0], OUT + "/stand.png", 80, planes["stand"][1]))
    print("car", finish(planes["car"][0], OUT + "/car.png", 64, planes["car"][1]))
    print("front", finish(planes["front"][0], OUT + "/front.png", 40, planes["front"][1]))
    comp = Image.open(OUT + "/back.png").convert("RGBA")                               # (what comp.py does)
    for name in ("pump", "stand", "car", "front"):
        comp.alpha_composite(Image.open(f"{OUT}/{name}.png").convert("RGBA"))
    comp.convert("RGB").save(OUT + "-comp.png")
    print("done", round(time.time() - t0, 1))

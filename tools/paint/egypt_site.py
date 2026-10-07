"""Egypt, about 2560 B.C.: the building site at the foot of the Great Pyramid, on a working afternoon.
This is where the track from the riverbank (egypt1) comes up to, so the light, sand, sky and white
casing stone are the same paint.

LIGHT   Low afternoon sun from the left, and a little from beyond the pyramid. Tops and left sides are
        warm; sides turned to the right, and to us, are cool. Shadows lie to the right and 30 degrees
        toward us, about as long as the thing is tall (egypt_site_kit.SUN_LONG, SUN_TURN). The pyramid's
        own shadow lies over the bank at its foot, the podium and the top of the steps (egypt_site_plan).
DEPTH   horizon 250, full 590 (persp.Camera, through egypt_site_kit): a grown-up is 160 px at the bottom
        edge, 71 px at the foot of the steps, about 53 px on the landing (minScale 0.33).
TONES   Light: the narrow sunlit face, the cloud behind it, the trodden floor in the middle, the awning,
        the block on its sledge.
        Middle: the great lilac face that fills the upper right (deeper toward its top right), the sky.
        Dark: the doorway and its notch, the podium under it in the pyramid's shadow, the scaffold, the
        shade under the scribe's awning, the water jars bottom left, the waiting blocks in a cloud's
        shadow bottom right. Corners deeper and warmer.
WHERE   The pyramid's near edge comes down from the top (x 424) to its foot at (268, 334). Left of it the
        sunlit face, a leaning wedge; left of that, sky, the queens' three pyramids (the middle one
        unfinished), the builders' town, the river, the foot of the great ramp, and nearer, the stone yard.
        Right of it the shaded face. The doorway is at about (541, 233), 43 x 66 px, in a notch cut back
        into the casing, under two slabs leaning together. A mud-brick podium stands before it; its steps
        come down toward us to the sand at (716, 400). Scaffold on the face right of the steps, where the
        last blocks are still rough. Scribe's awning left (62..245, 335..474). Sledge and block in the
        middle (384..565, 385..480), its rope lying up-left to where the gang stands by their standard.
        Sunny spot (330, 520), with a clear line to the doorway. Waiting blocks and tools bottom right,
        water jars bottom left (front plane). The road from the river comes in bottom left.

The picture is a backdrop and four cut-outs: awning, sledge, front (the waiting blocks and the water
jars), and shade (the windshield sun-shade as it is held up at the sunny spot).

The work is in several files: egypt_site_kit (measuring, the camera, a sheet that glazes), egypt_site_plan
(where everything stands), egypt_site_stone (the pyramid's faces and doorway), egypt_site_works (podium,
steps, scaffold), egypt_site_things (the cut-outs and the scribe's station), egypt_site_ground (small
things on the sand, the distance), egypt_site_props (pots, rope, timber, tools)."""

import json
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import *
import sky, land, flora, build
from egypt_site_kit import *
from egypt_site_plan import *
import egypt_site_stone as stone
import egypt_site_works as works
import egypt_site_things as things
import egypt_site_props as props
import egypt_site_ground as ground

LIGHT = (-0.78, -0.62)
SKY = [(0.0, "#2a72c6"), (0.38, "#4a9ae0"), (0.68, "#86c6ec"), (0.86, "#cfe6e0"), (1.0, "#f8e6be")]      # the riverbank's sky
CLOUDS = [(96, 226, 320, 150, 34), (30, 246, 150, 24, 7), (262, 104, 150, 40, 9)]
QUEENS = [(36, 278, 29, 51), (88, 275, 24, 42), (130, 273, 19, 33)]                                    # middle x, base y, half width, height
OUT = "out/egypt-site"


def small(q):
    cx, by, hw, hgt = q
    return (cx, by - hgt), (cx - hw, by - 1), (cx + hw * 0.3, by + 2), (cx + hw, by - 1)


def queens(pic, seed):
    for i, q in enumerate(QUEENS):
        build.pyramid(pic, *small(q), seed + 23 + i, courses=16, lit=("#fdeec6", "#f2d298"), shade=("#a8a6c8", "#b4a6b6"), haze="#f6e2bc", haze_amount=0.34,
                      built=0.70 if i == 1 else 1.0)


def line_y(points, shape=(H, W)):
    """The height of a line through picture points, for every column."""
    pts = sorted(points)
    return np.interp(np.arange(shape[1]), [p[0] for p in pts], [p[1] for p in pts]).astype(F32)


def lit_ground(s, q, y=0.0):
    """A place on the sunlit side: `s` along that face's foot from the near corner, `q` out from it (negative: away from the stone)."""
    return P(CX + s * NX[0] + q * DX[0], y, CORNER_ZC + s * NX[1] + q * DX[1])


def banks(shape, seed):
    """The bank of chips and sand the pyramid stands in: masks for its shaded side and its sunlit side,
    and how far up each (0 at the sand, 1 against the stone)."""
    x, y = grid(shape)
    top = [SHADE.pt(s, 0) for s in (0, 500, 1000, 1500, 2700)]
    foot = [GP(s, -BANK, 0) for s in (2700, 1500, 1000, 500, 0, -BANK)]
    ms = mask_poly(shape, top + foot, soft=0.8, wobble=1.6, seed=seed)
    ty, fy = line_y(top), line_y([f for f in foot if f[0] >= foot[-1][0]])
    ups = np.clip((fy[None, :] - y) / np.maximum(fy - ty, 1)[None, :], 0, 1)
    topl = [LIT.pt(s, 0) for s in (0, 1500, 4000, BASE)]
    footl = [lit_ground(s, -BANK) for s in (BASE, 4000, 1500, 400, -BANK)]
    ml = mask_poly(shape, topl + footl, soft=0.8, wobble=1.2, seed=seed + 1)
    return ms, ups.astype(F32), ml


def track(shape, points, wide_cm, soft=3.0, steps=12):
    """A worn way over the sand through picture points, `wide_cm` wide on the ground. -> (mask, path, widths)"""
    path = curve(points, steps)
    widths = [max(1.5, wide_cm * size_at(py)) for _, py in path]
    return mask_line(shape, path, widths, soft=soft), path, widths


HAUL = [(860, 520), (700, 494), (590, 476), (498, 463), (420, 447), (350, 424), (290, 402), (243, 389), (214, 366), (196, 334), (183, 306), (174, 284), (168, 272)]      # the hauling road
RIVER = [(20, 720), (104, 618), (176, 578), (270, 558), (384, 553), (500, 563), (610, 588), (720, 640)]   # the road the blocks come up from the river by, to the yard
PATH = [(150, 566), (230, 536), (300, 512), (360, 490), (410, 470)]                                    # feet have worn a way from it up to the site
WET = [(430, 452), (398, 441), (366, 430)]                                                           # sand wetted ahead of the runners


def cloud_shadow(shape, seed=21):
    """Where a cloud's shadow lies over the near right corner. -> mask"""
    x, y = grid(shape)
    r = np.hypot((x - 770) / 310.0, (y - 650) / 205.0) + (noise(shape, (200, 70), seed + 51, 3) - 0.5) * 0.16
    return step(0.0, 1.0, (1.0 - r) / 0.13).astype(F32)


def under(seed=21):
    """Everything broad and soft: sky, distance, sand, the two faces of the pyramid, the big shadows."""
    shape = (H, W)
    x, y = grid(shape)
    info = {}

    # ---- sky: the riverbank's sky, with one great heap of cloud standing behind the sunlit face
    pic = sky.field(shape, HZ, SKY, seed, haze="#fbeacc", patch=0.03)
    sky.wisps(pic, HZ, seed + 3, "#fdf0d8", top=0.55, amount=0.55)
    sky.paint_clouds(pic, CLOUDS, seed + 5, tones=("#86a6da", "#bcd0ea", "#fbf2de", "#fffcf0"), light=LIGHT, ragged=13)

    # ---- far left: the hills across the river
    hills, hl = land.ridge(shape, [(0, 241), (50, 237), (110, 242), (190, 245), (300, 247)], HZ + 3, seed + 6, rough=1.8)
    over(pic, ramp(np.clip((y - hl[None, :]) / 16, 0, 1), [(0.0, "#e2c6b8"), (1.0, "#e9d8c8")]), hills)
    tint(pic, "#a79cc0", (hills * step(0.55, 0.8, noise(shape, (16, 30), seed + 61, 3)) * 0.5).astype(F32))
    land.haze(pic, HZ - 4, "#e8ead6", 0.38, 0.05, hills)

    # ---- the sand, far to near (the riverbank's sand)
    below = np.clip(y - HZ + 0.5, 0, 1).astype(F32)
    sand = land.sand(shape, HZ, seed + 40, far="#f3d6a0", mid="#e8b468", near="#c9823c", patch=0.08, ripple=0.0)
    over(pic, sand, below)

    # ---- beyond the plateau's lip the desert falls away: the valley, green by the river, pale with distance
    lip = line_y([(0, 284), (60, 278), (120, 273), (180, 269), (260, 266), (800, 262)])
    lip += (noise((1, W * 4), (60, 1), seed + 7, 3)[0, :W] - 0.5) * 3
    beyond = (np.clip(lip[None, :] - y + 0.5, 0, 1) * below).astype(F32)
    t = np.clip((y - HZ) / np.maximum(lip[None, :] - HZ, 1), 0, 1)
    valley = ramp(t, [(0.0, "#c4dcd2"), (0.09, "#e2f2ec"), (0.2, "#8fa878"), (0.42, "#a9b27e"), (0.7, "#d8c896"), (1.0, "#ead4a4")])
    valley *= (1 + (noise(shape, (110, 3), seed + 8, 2) - 0.5) * 0.14)[..., None]
    over(pic, valley, beyond)
    land.haze(pic, HZ, "#f2e6c4", 0.30, 0.06, beyond)
    over(pic, "#fff0c4", (np.clip(1 - np.abs(y - (lip[None, :] + 1.5)) / 2.5, 0, 1) * below * 0.5).astype(F32))    # the lip itself, in the sun
    queens(pic, seed)
    info.update(lip=lip, below=below)

    # ---- the floor of the site is paler than open desert: years of limestone dust and chips trodden in
    floor = below * (1 - beyond)
    dusty = np.clip(1.25 - np.abs(y - 420) / 150.0, 0, 1) * (0.6 + 0.6 * noise(shape, (220, 60), seed + 41, 3))
    over(pic, vary("#f6dfae", shape, seed + 42, 0.05, 30), (np.clip(dusty, 0, 1) * 0.50 * floor).astype(F32))

    # ---- the pyramid: the narrow face in the sun, the great face in shade
    stone.lay_faces(pic, 1.0, joints=0.32, seed=seed)
    sf, lf = stone.shaded_face(seed), stone.lit_face(seed)

    # ---- the bank of chips it stands in: bright on the sunny side, half-lit under the shaded face
    ms, ups, ml = banks(shape, seed + 20)
    over(pic, vary("#f8e2b4", shape, seed + 21, 0.05, 18), ml * 0.92)
    chips = vary("#e6c8a0", shape, seed + 22, 0.07, 14)
    chips *= (1 - 0.20 * ups)[..., None]
    over(pic, chips, ms * 0.95)
    over(pic, "#9a8cae", (ms * ups ** 1.5 * 0.42).astype(F32))                   # cooler and darker up against the stone
    info.update(bank=np.maximum(ms, ml))

    # ---- the way in: the notch and its doorway
    over(pic, *stone.entrance(shape))
    sand_only = (floor * (1 - np.maximum(ms, ml)) * (1 - np.maximum(sf["mask"], lf["mask"]))).astype(F32)     # flat ground we can see, for roads and shadows to lie on

    # ---- the hauling road: sledges have come this way for twenty years. Pale, hard, grooved by runners
    haul_path = ground_path(HAUL, 8)
    road = ground_line(shape, haul_path, 300, soft=45) * sand_only
    worn = road * (0.55 + 0.6 * ground_tex(shape, seed + 45, 150, (2.5, 1.0)))
    over(pic, vary("#f9e6b8", shape, seed + 44, 0.05, 26), (np.clip(worn, 0, 1) * 0.50).astype(F32))
    edge = (ground_line(shape, haul_path, 420, soft=60) * sand_only - road).clip(0, 1)
    tint(pic, "#b48c70", (edge * 0.30).astype(F32))                               # darker, churned margins
    for off, deep in ((-58, 0.55), (58, 0.6), (-88, 0.3), (30, 0.3)):             # the grooves
        groove = ground_line(shape, offset_path(haul_path, off), 11, soft=4) * sand_only
        tint(pic, "#a67a5c", (groove * (0.4 + 0.6 * ground_tex(shape, seed + 46, 90, (3.0, 1.0))) * deep).astype(F32))
    river_path = ground_path(RIVER, 8)
    old_road = ground_line(shape, river_path, 250, soft=45) * sand_only
    over(pic, vary("#f6dca6", shape, seed + 52, 0.05, 26), (old_road * (0.5 + 0.6 * ground_tex(shape, seed + 53, 150, (2.5, 1.0))) * 0.40).astype(F32))
    tint(pic, "#b48c70", ((ground_line(shape, river_path, 360, soft=60) * sand_only - old_road).clip(0, 1) * 0.26).astype(F32))
    for off, deep in ((-52, 0.5), (52, 0.55), (-20, 0.25), (84, 0.25)):
        groove = ground_line(shape, offset_path(river_path, off), 10, soft=4) * sand_only
        tint(pic, "#a67a5c", (groove * (0.4 + 0.6 * ground_tex(shape, seed + 54, 90, (3.0, 1.0))) * deep).astype(F32))
    foot_path = ground_path(PATH, 8)
    trod = ground_line(shape, foot_path, 130, soft=40) * sand_only
    over(pic, vary("#f6dca6", shape, seed + 48, 0.05, 26), (trod * (0.5 + 0.6 * ground_tex(shape, seed + 49, 110)) * 0.36).astype(F32))
    tint(pic, "#b48c70", ((ground_line(shape, foot_path, 230, soft=50) * sand_only - trod).clip(0, 1) * 0.22).astype(F32))
    wet = ground_line(shape, ground_path(WET, 6), 150, soft=30) * sand_only * step(0.25, 0.6, ground_tex(shape, seed + 50, 70) + 0.25)
    tint(pic, "#86604e", (wet * 0.78).astype(F32))
    over(pic, "#6a5458", (wet * 0.20).astype(F32))
    road = np.maximum(road, old_road)
    spot = mask_ellipse(shape, SUNSPOT[0], SUNSPOT[1] - 2, 50, 15, soft=7, wobble=4, seed=seed + 57) * sand_only    # the sunny spot: hard, pale, swept clear
    over(pic, "#fbe8b8", (spot * 0.38).astype(F32))
    drip = mask_ellipse(shape, 62, 600, 88, 16, soft=5, wobble=5, seed=seed + 56) * sand_only        # damp sand under the water jars
    tint(pic, "#8f6a58", (drip * 0.5).astype(F32))
    info.update(road=road, trod=trod, wet=wet, sand=sand_only, haul_path=haul_path, foot_path=foot_path)

    # ---- the scribe's reed mat, then the shadows lying to the right: the steps and podium, the awning, the sledge
    sheet = Paper(shape)
    things.station_under(sheet)
    sheet.onto(pic)
    lying = (floor * (1 - ml) * (1 - np.maximum(sf["mask"], lf["mask"]))).astype(F32)       # where a shadow can lie
    pyr = np.maximum(floor_shade(shape) * sand_only, ms)                          # the pyramid's own shadow: over the bank and a strip of the floor
    shadow(pic, pyr, 0.50)
    shadow(pic, works.works_shadow(shape) * lying * (1 - pyr * 0.7), 0.52)
    shadow(pic, things.awning_shadow(shape) * lying, 0.50)
    shadow(pic, things.sledge_shadow(shape) * lying, 0.52)

    # ---- the podium and the steps (their big planes; the brickwork comes later)
    sheet = Paper(shape)
    works.podium(sheet)
    works.steps(sheet)
    sheet.onto(pic)
    in_shade = works.works_shade(shape)
    shadow(pic, in_shade, 0.50)

    # ---- a cloud's shadow lies over the nearest corner, bottom right; the sunny spot stays in full sun
    cloud = cloud_shadow(shape, seed)
    tint(pic, "#b98a74", (cloud * 0.40 * floor).astype(F32))
    # ---- the corners go deeper and warmer, to hold the eye in the picture
    corner = np.clip(((x - 400) / 400) ** 2 * 0.5 + ((y - 380) / 220).clip(0, 2) ** 2 * 0.5, 0, 1)
    tint(pic, "#c08a5c", (corner * 0.24 * floor).astype(F32))
    glow(pic, "#fff0c8", (np.clip(1 - np.abs(y - (HZ + 8)) / 30, 0, 1) * 0.08 * floor * (x < 270)).astype(F32))       # dust in the air over the plateau
    land.ripples(pic, HZ, seed + 47, sand_only * (1 - np.clip(road * 2 + trod * 2, 0, 1)) * (y > 470), amount=0.05)
    info.update(floor=floor, cloud=cloud, ms=ms, ml=ml, pyr=pyr, in_shade=in_shade)
    return np.clip(pic, 0, 1), info


def details(pic, info, seed=21):
    """The crisp things, over the brushwork: every edge of the stone again, joints, the works on the
    face, and all the small things lying about."""
    shape = (H, W)
    x, y = grid(shape)
    rng = np.random.default_rng(seed + 77)

    # ---- first, say the pyramid again, crisply
    crisp = pic.copy()
    stone.lay_faces(crisp, 1.0, joints=0.72, seed=seed)
    sf, lf = stone.shaded_face(seed), stone.lit_face(seed)
    pic[...] = lerp(pic, crisp, (np.maximum(sf["mask"], lf["mask"]) * 0.74)[..., None])
    edge = Paper(shape)
    top_v = 1500.0
    edge.line([SHADE.pt(0, 0), SHADE.pt(top_v / TAN, top_v)], "#fffbe6", 1.3, 0.9)             # the near edge catches the light
    edge.line([(px + 1.4, py) for px, py in (SHADE.pt(0, 0), SHADE.pt(top_v / TAN, top_v))], "#8582b0", 1.0, 0.45)
    edge.line([LIT.pt(BASE, 0), LIT.pt(BASE - 6000 / TAN, 6000)], "#fff6da", 1.0, 0.5)         # the far edge against the sky
    edge.line([SHADE.pt(0, 0), SHADE.pt(2700, 0)], "#6c6690", 1.2, 0.55)                       # the foot of the casing, in the bank
    edge.line([LIT.pt(0, 0), LIT.pt(BASE, 0)], "#d2a26c", 1.0, 0.55)
    for (bx, by, r) in ((196, 58, 4.2), (214, 70, 3.2), (150, 96, 2.6)):                           # kites turning in the warm air
        edge.line([(bx - r, by - r * 0.35), (bx - r * 0.3, by - r * 0.1), (bx, by + r * 0.25), (bx + r * 0.35, by - r * 0.15), (bx + r, by - r * 0.5)], "#3a3a4e", 1.0, 0.8)
    edge.onto(pic)

    # ---- the works on the sunlit face, and far things on the left
    ground.far(pic, info, seed)
    crisp = pic.copy()
    queens(crisp, seed)
    pic[...] = lerp(pic, crisp, 0.8)
    far = Paper(shape)
    for i, q in enumerate(QUEENS):
        a, l, c, r = small(q)
        far.line([a if i != 1 else (lerp(c[0], a[0], 0.7), lerp(c[1], a[1], 0.7)), c], "#fffbe6", 0.9, 0.6)
    a, l, c, r = small(QUEENS[1])                                             # the middle one is still building: a ramp up its side, men on top
    far.line([(l[0] - 9, l[1] + 1), (lerp(l[0], a[0], 0.7), lerp(l[1], a[1], 0.7))], "#d9b78a", 1.6, 0.95)
    far.line([(l[0] - 9, l[1] + 1.6), (lerp(l[0], a[0], 0.7), lerp(l[1], a[1], 0.7) + 1.6)], "#a08068", 0.9, 0.7)
    for dx in (-3, 0.5, 4):
        props.dab(far, lerp(c[0], a[0], 0.7) + dx, lerp(c[1], a[1], 0.7) - 0.5, 3.2)
    far.onto(pic)
    ground.middle(pic, info, seed)

    # ---- the doorway, the podium, the steps, the scaffold
    over(pic, *stone.entrance(shape, crisp=True))
    sheet = Paper(shape)
    works.cradles(sheet)
    stone.masons_marks(sheet)
    sheet.onto(pic)
    sheet = Paper(shape)
    works.scaffold(sheet)
    sc, sa = sheet.done()
    over(pic, sc, sa)
    shadow(pic, sa, 0.36, cool=0.12)                                            # the scaffold stands wholly in the pyramid's shadow
    sheet = Paper(shape)
    works.podium(sheet, crisp=True)
    works.steps(sheet, crisp=True)
    sc, sa = sheet.done()
    over(pic, sc, sa)
    shadow(pic, np.minimum(sa, info["in_shade"]), 0.50)                         # and so do the podium and the top of the steps

    # ---- the scribe's station (what is not on the cut-out). Things under the awning stand in its shade
    shade_all = np.clip(things.awning_shadow(shape) + things.sledge_shadow(shape), 0, 1)
    sheet = Paper(shape)
    things.station(sheet)
    sc, sa = sheet.done()
    over(pic, sc, sa)
    shadow(pic, sa * shade_all, 0.40, cool=0.08)

    # ---- and everything small on the ground
    ground.near(pic, info, seed)
    return pic


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def layout():
    """The numbers the game needs, worked out from the same measurements the picture is painted from."""
    def r(p):
        return [int(round(p[0])), int(round(p[1]))]

    def bbox(points, grow=0):
        xs, ys = [p[0] for p in points], [p[1] for p in points]
        return [int(min(xs) - grow), int(min(ys) - grow), int(max(xs) - min(xs) + 2 * grow), int(max(ys) - min(ys) + 2 * grow)]
    m, sl, st = things.mat_frame(), things.sledge_frame(), things.stack_frame()
    MW, MD, MT = things.MW, things.MD, things.MT
    u0, u1 = DOOR_OFF - DOOR_W / 2, DOOR_OFF + DOOR_W / 2
    door = [backp(u0, 0), backp(u1, 0), backp(u1, DOOR_H), backp(u0, DOOR_H)]
    s0, s1, top = NOTCH_S - NOTCH_W / 2, NOTCH_S + NOTCH_W / 2, SILL + NOTCH_H
    notch = [SHADE.pt(s0, SILL), SHADE.pt(s1, SILL), SHADE.pt(s1, top), SHADE.pt(s0, top)]
    at_door = GP(NOTCH_S + DOOR_OFF + 8, Q_BACK - 70, LAND_Y)                  # feet on the floor of the notch, before the doorway
    stair = [stair_walk(t) for t in (0.0, 0.25, 0.5, 0.75, 1.0)]              # feet, from the sand to the top step
    landing = [GP(STAIR_TOP_S, -POD_OUT + 50, LAND_Y), GP(NOTCH_S + DOOR_OFF + 30, Q_FACE + 10, LAND_Y), at_door]
    # the floor: all the sand a person may stand on, clockwise from the bottom left, with the steps and landing as a tongue
    side = 0.6
    up = [stairp(a, -side, LAND_Y * (1 - a / RUN)) for a in np.linspace(RUN - TREAD * 0.4, 0, 6)]
    down = [stairp(a, side, LAND_Y * (1 - a / RUN)) for a in np.linspace(0, RUN - TREAD * 0.4, 6)]
    ledge = [(up[-1][0], up[-1][1] + 5), (backp(u0 - 30, 0)[0], backp(0, 0)[1] + 7), (backp(u0 - 30, 0)[0], backp(0, 0)[1] - 5), (down[0][0], down[0][1] - 7)]
    walk = [(0, 578), (0, 398), (120, 392), (212, 381), (248, 378)] + [GP(s, -BANK - 34, 0) for s in (120, 380, 640)] + [GP(POD_S0 - 30, -POD_OUT - 30, 0)]
    walk += [stairp(a, -1.45, 0) for a in (150, 330, RUN - TREAD * 0.5)] + [up[0]] + up[1:] + ledge + down[:-1] + [down[-1]]
    walk += [(752, 409), (800, 411), (800, 506), (722, 504), (612, 516), (552, 572), (544, 596), (122, 596), (112, 587)]
    station = [m.pt(-10, 0, -8), m.pt(MW + 12, 0, -8), m.pt(MW + 12, 0, MD + 6), m.pt(-10, 0, MD + 6)]
    sledge = [sl.pt(-38, 0, -8), sl.pt(242, 0, -8), sl.pt(242, 0, 124), sl.pt(-38, 0, 124)]
    bricks = [(524, 398), (604, 392), (606, 380), (526, 384)]
    jar = [(360, 472), (384, 472), (384, 462), (360, 462)]
    cloth = [m.pt(-8, MT, -8), m.pt(MW + 8, MT, -8), m.pt(MW + 8, MT, MD + 6), m.pt(-8, MT, MD + 6)]
    block = sl.pts([(things.BLOCK_U[0], things.BLOCK_V[0], 0), (things.BLOCK_U[1], things.BLOCK_V[0], 0), (things.BLOCK_U[1], things.BLOCK_V[1], things.BLOCK_D[1]), (things.BLOCK_U[0], things.BLOCK_V[1], things.BLOCK_D[1])])
    k = size_at(SUNSPOT[1])
    shade_mid = (SUNSPOT[0] + 20 * k + 0.925 * 65 * k + 0.30 * 15 * k, SUNSPOT[1] - 118 * k - 0.38 * 65 * k - 0.954 * 15 * k)
    return {
        "id": "egypt-site", "horizon": HZ, "full": FULL, "minScale": 0.33, "light": "low afternoon sun from the left; shadows lie to the right and a little toward us",
        "note": "minScale 0.33 keeps a grown-up about 53 px tall on the steps and landing, which fits the doorway (%d x %d px). 'stair' and 'landing' are feet positions for walking up, foot of the steps first; the game may walk them as a path." % (bbox(door)[2], bbox(door)[3]),
        "walk": [r(p) for p in walk],
        "blocked": [[r(p) for p in station], [r(p) for p in sledge], [r(p) for p in bricks], [r(p) for p in jar]],
        "planes": [{"id": "awning", "file": "awning.png", "base": int(round(m.pt(0, 0, 0)[1]))},
                   {"id": "sledge", "file": "sledge.png", "base": [r(sl.pt(0, 0, 0)), r(sl.pt(236, 0, 0))]},
                   {"id": "front", "file": "front.png", "plane": "front"},
                   {"id": "shade", "file": "shade.png", "base": int(SUNSPOT[1]) + 1, "note": "show only while the shade is being held up at the sunny spot"}],
        "things": [
            {"id": "entrance", "what": "the doorway into the pyramid, under two great slabs", "shape": {"rect": bbox(door, 4)}, "stand": r(at_door), "face": "N"},
            {"id": "stair", "what": "the mud-brick steps up to the doorway", "shape": {"poly": [r(p) for p in [stairp(RUN, -1, 0), stairp(RUN, 1, 0), stairp(0, 1, LAND_Y), stairp(0, -1, LAND_Y)]]}, "stand": r(stair[0]), "face": "N"},
            {"id": "scribe-desk", "what": "the scribe's station under its awning", "shape": {"rect": bbox(cloth + station, 2)}, "stand": r(m.pt(MW + 34, 0, 60)), "face": "W"},
            {"id": "sledge", "what": "the sledge with its block, and the wet sand before it", "shape": {"rect": bbox(sledge + block, 2)}, "stand": r(sl.pt(110, 0, -70)), "face": "N"},
            {"id": "rope", "what": "the hauling rope lying up to the gang", "shape": {"poly": [[392, 444], [400, 460], [300, 414], [226, 388], [222, 374], [300, 396]]}, "stand": [330, 440], "face": "N"},
            {"id": "blocks", "what": "casing blocks waiting, with the masons' tools on them", "shape": {"poly": [[561, 486], [636, 447], [800, 440], [800, 600], [556, 600]]}, "stand": [538, 566], "face": "E"},
            {"id": "sunspot", "what": "a clear patch of sand in full sun, in sight of the doorway", "shape": {"rect": [296, 504, 70, 30]}, "stand": r(SUNSPOT), "face": "E"},
            {"id": "scaffold", "what": "the masons' scaffold on the shaded face", "shape": {"rect": [640, 60, 160, 300]}, "stand": [744, 414], "face": "N"},
            {"id": "pyramid", "what": "the Great Pyramid, close to", "shape": {"poly": [[268, 334], [341, 0], [800, 0], [800, 316]]}, "stand": [430, 420], "face": "N"},
            {"id": "queens", "what": "the queens' three small pyramids, the builders' town and the river", "shape": {"rect": [0, 228, 176, 56]}, "stand": [60, 410], "face": "N"},
            {"id": "yard", "what": "the stone yard: blocks waiting beside the hauling road", "shape": {"rect": [24, 280, 140, 48]}, "stand": [110, 404], "face": "N"},
            {"id": "water", "what": "the site's water jars, by the road from the river", "shape": {"rect": [0, 496, 104, 104]}, "stand": [130, 590], "face": "W"},
            {"id": "bricks", "what": "mud bricks stacked to dry, and their mould", "shape": {"rect": [520, 376, 96, 24]}, "stand": [560, 410], "face": "N"},
        ],
        "exits": [{"to": "egypt-gallery", "shape": {"poly": [r(p) for p in door]}, "stand": r(at_door)},
                  {"to": "egypt-crash", "shape": {"poly": [[0, 520], [150, 540], [176, 600], [0, 600]]}, "stand": [130, 590]}],
        "marks": {"dad": [170, 574], "scribe": list(MARKS["scribe"]), "overseer": list(MARKS["overseer"]), "hauler1": list(MARKS["hauler1"]), "hauler2": list(MARKS["hauler2"]),
                  "hauler3": list(MARKS["hauler3"]), "guard": list(MARKS["guard"]), "shadeHolder": r(SUNSPOT), "atDoor": r(at_door), "stairFoot": r(stair[0]), "stairTop": r(stair[-1])},
        "stair": [r(p) for p in stair], "landing": [r(p) for p in landing],
        "door": {"rect": bbox(door), "middle": r(backp(DOOR_OFF, DOOR_H * 0.5))},
        "beam": [r(shade_mid), r(backp(DOOR_OFF, DOOR_H * 0.55))],
        "shade": {"heldAt": r(SUNSPOT), "middle": r(shade_mid)},
    }


if __name__ == "__main__":
    # python3 egypt_site.py         everything, with the brush pass, and the finished files
    # python3 egypt_site.py fast    no brush pass, no files: just out/egypt-site-2-all.png to look at
    # python3 egypt_site.py planes  only the cut-outs again, over the backdrop painted last time
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    fast = mode != "full"
    if mode == "planes":
        pic = np.asarray(Image.open(OUT + "-2-back.png").convert("RGB"), dtype=F32) / 255
    else:
        base, info = under()
        Image.fromarray((base * 255).astype(np.uint8)).save(OUT + "-1-under.png")
        print("under", round(time.time() - t0, 1), flush=True)
        pic = base.copy() if fast else strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.22)
        print("brushed", round(time.time() - t0, 1), flush=True)
        details(pic, info)
        Image.fromarray((np.clip(pic, 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-back.png")
    planes = {"awning": things.awning_plane((H, W), fast), "sledge": things.sledge_plane((H, W), fast),
              "shade": things.shade_plane((H, W), fast), "front": things.front_plane((H, W), fast, cloud_shadow((H, W)))}
    whole = pic.copy()
    for name in ("awning", "sledge", "shade", "front"):
        c, a = planes[name]
        over(whole, c, (a > 0.5).astype(F32))
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save(OUT + "-2-all.png")
    print("painted", round(time.time() - t0, 1), flush=True)
    if fast:
        sys.exit()
    print("back", finish(pic, OUT + "/back.png", 152))
    for name, colors in (("awning", 56), ("sledge", 56), ("front", 72), ("shade", 32)):
        c, a = planes[name]
        print(name, finish(c, OUT + "/" + name + ".png", colors, a))
    with open(OUT + "/layout.json", "w") as f:
        json.dump(layout(), f, indent=1)
    for comp, names in ((OUT + "-comp.png", ("awning", "sledge", "shade", "front")), (OUT + "-comp-noshade.png", ("awning", "sledge", "front"))):
        im = Image.open(OUT + "/back.png").convert("RGBA")                       # everything laid together, as comp.py does
        for name in names:
            im.alpha_composite(Image.open(OUT + "/" + name + ".png").convert("RGBA"))
        im.convert("RGB").save(comp)
    print("done", round(time.time() - t0, 1))

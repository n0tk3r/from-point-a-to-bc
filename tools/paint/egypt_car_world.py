"""The world outside the wagon's glass (egypt_car.py): what Dad sees through the windshield, his open window and the
Son's, one afternoon, the car nose-down in the sand on the bank of the Nile.

It is painted in the picture's own pixels, through the scene's camera: every pixel is a direction from Dad's eye
(egypt_car_model.VIEW), turned through the car's pitch (the nose is 7 degrees down, so the world is tilted up by as much:
its horizon is the level row 119.6). Far things (the sky, the far bank, the river) depend on the direction alone; the
mound of sand the nose ploughed up is near, and is shaped in the picture over the hood.

THE LIGHT. The sun is low, ahead of the car and a little to its right (azimuth 40 degrees right of the car's line, 26
up): above the windshield's top right corner, behind the passenger's visor and the roof's edge. Through the glass the
world is seen against the light: the sky deepest blue away from the sun (top left), paling and warming toward it, the
sun's glare in the glass's top right corner; the far hills and the far bank's fields and palms a dark line against the
bright sky; the river carrying the sun's glitter toward Dad under the glare (only right of x 600: the words box over
the middle of the sky stays deep blue); the mound piled in front of the nose showing Dad the side the sun is not on
(warm sand in its own shade, lit by the light the sunlit sand throws about, its crest rim-lit). Through Dad's own
window, on the car's shade side: the warm glow of sand in the car's shadow and a clump of papyrus, not sun. Through the
Son's window: sunlit sand under a sky white with the sun, the brightest pane."""

import math

import numpy as np

from brush import F32, Sheet, blur, grid, lerp, noise, over, ramp, rgb, sample, smooth, step, tint, glow, mask_poly, curve
import egypt_car_model as M
import flora
import sky

W, H = 800, 600
HZ = M.VIEW["horizon"] - M.VIEW["focal"] * math.tan(math.radians(M.PITCH))      # the world's horizon, a level row
SUN = dict(az=40.0, el=26.0)                                                       # the sun: degrees right of the car's line, degrees up (in the world)


def directions(shape=(H, W)):
    """For every pixel: (azimuth, world elevation) in degrees, through the camera and the car's pitch."""
    x, y = grid(shape)
    F, cx, hz = M.VIEW["focal"], M.VIEW["centre_x"], M.VIEW["horizon"]
    dx, dy, df = (x + 0.5 - cx) / F, (hz - (y + 0.5)) / F, np.ones(shape, F32)
    p = math.radians(M.PITCH)
    up = dy * math.cos(p) - df * math.sin(p)
    fwd = df * math.cos(p) + dy * math.sin(p)
    az = np.degrees(np.arctan2(dx, fwd))
    el = np.degrees(np.arctan2(up, np.hypot(dx, fwd)))
    return az.astype(F32), el.astype(F32)


def to_picture(az, el):
    """A direction (degrees right, degrees up in the world) -> the pixel that shows it."""
    p = math.radians(M.PITCH)
    a, e = math.radians(az), math.radians(el)
    dx, up, fwd = math.sin(a) * math.cos(e), math.sin(e), math.cos(a) * math.cos(e)
    dy = up * math.cos(p) + fwd * math.sin(p)                     # back into the car's frame
    df = fwd * math.cos(p) - up * math.sin(p)
    F, cx, hz = M.VIEW["focal"], M.VIEW["centre_x"], M.VIEW["horizon"]
    return cx + F * dx / df, hz - F * dy / df


def sun_angle(az, el):
    """Degrees between every pixel's direction and the sun's."""
    a0, e0 = math.radians(SUN["az"]), math.radians(SUN["el"])
    a, e = np.radians(az), np.radians(el)
    c = np.sin(e) * math.sin(e0) + np.cos(e) * math.cos(e0) * np.cos(a - a0)
    return np.degrees(np.arccos(np.clip(c, -1, 1))).astype(F32)


# ---------------------------------------------------------------- the mound the nose ploughed up, and the sand on the hood
CREST = [(-10, 196), (40, 186), (110, 172), (190, 162), (262, 158), (330, 163), (400, 171), (452, 168), (520, 160), (590, 164),
         (660, 174), (720, 186), (780, 198), (812, 204)]                           # its ridge across the glass, left to right


def crest_line(seed=7):
    """The mound's ridge: one row for every column, uneven as wind-blown sand is."""
    xs = np.arange(W)
    line = np.interp(xs, [p[0] for p in CREST], [p[1] for p in CREST]).astype(F32)
    line += (noise((1, W * 4), (70, 1), seed, 4)[0, :W] - 0.5) * 2 * 2.6
    line += (noise((1, W * 4), (12, 1), seed + 1, 2)[0, :W] - 0.5) * 1.4
    return line


def world(seed=21):
    """-> (the outside, as Dad sees it through the glass, the whole picture's size; info: the masks and rows it was
    painted by: 'mound', 'crest', 'river', 'sky', and the glare and glitter as masks, for the checks)."""
    shape = (H, W)
    x, y = grid(shape)
    az, el = directions(shape)
    ang = sun_angle(az, el)
    rng = np.random.default_rng(seed)
    # ---- the sky: deep blue away from the sun, paling and warming toward it; never a plain gradient
    pic = sky.field(shape, HZ, [(0.0, "#22569c"), (0.5, "#2c6ab2"), (0.8, "#3e7ec2"), (0.92, "#76a6d2"), (1.0, "#c8d8d2")], seed, haze="#dce0d0", patch=0.04)
    near_sun = np.exp(-ang / 15.0)
    over(pic, "#dcecf0", (near_sun * 0.6).astype(F32))
    over(pic, "#fff6dc", (np.exp(-ang / 11.0) * 0.85).astype(F32))
    glare = np.exp(-ang / 5.5)
    glow(pic, "#ffffff", np.clip(glare * 1.2, 0, 1).astype(F32))
    # a low heap of cloud over the far hills at the left, lit from beyond; and one near the sun, all rim and glare
    sky.paint_clouds(pic, [(105, int(HZ) - 7, 190, 26, 9)], seed + 3, tones=("#5c86bc", "#7698c4", "#aabcd4", "#e8eef0"), light=(0.9, -0.2), ragged=8, amount=0.85)
    sky.paint_clouds(pic, [(712, int(HZ) - 8, 130, 30, 7)], seed + 4, tones=("#9eb2c8", "#c2cedc", "#f2f2ea", "#ffffff"), light=(-0.4, -0.9), ragged=8, amount=0.9)
    sky.wisps(pic, HZ, seed + 5, "#e8ecf0", top=0.55, amount=0.35)
    # ---- the far hills, low and pale with haze, their faces toward us in shade (the sun is beyond them)
    hills = np.zeros(shape, F32)
    xs = np.arange(W)
    hl = np.interp(xs, [-10, 90, 200, 300, 420, 520, 640, 760, 810], [HZ - 7, HZ - 11, HZ - 8, HZ - 13, HZ - 10, HZ - 6, HZ - 9, HZ - 5, HZ - 4]).astype(F32)
    hl += (noise((1, W * 4), (60, 1), seed + 6, 4)[0, :W] - 0.5) * 3.0
    hills = np.clip(y - hl[None, :] + 0.5, 0, 1) * (y < HZ + 2)
    hill_col = lerp(rgb("#a99ab8"), rgb("#c8bcc4"), np.clip((x / W)[..., None], 0, 1))
    over(pic, hill_col * (1 + (noise(shape, (40, 6), seed + 7, 3) - 0.5)[..., None] * 0.12), hills.astype(F32))
    over(pic, "#e4dccc", (hills * np.exp(-ang / 18.0) * 0.6).astype(F32))
    # ---- the far bank: fields, then palms and their crowns, dark against the light
    trees = noise((1, W * 4), (26, 1), seed + 8, 4)[0, :W]                                     # the fields and the trees along them: a dark line
    bank_top = HZ - 1.5 - np.clip(trees - 0.45, 0, 1) * 7.0 + (noise((1, W * 4), (7, 1), seed + 16, 2)[0, :W] - 0.5) * 1.6
    bank = np.clip(y - bank_top[None, :] + 0.5, 0, 1) * (y < HZ + 2.4)
    over(pic, lerp(rgb("#2f3c32"), rgb("#4a5848"), np.clip((x / W)[..., None] * 0.6, 0, 1)), bank.astype(F32))
    palms = Sheet(shape)
    for k in range(70):                                            # date palms standing up out of it, dark against the light
        px = rng.random() * (W + 40) - 20
        if 210 < px < 590 and rng.random() < 0.3:
            continue
        hgt = 6 + rng.random() * 9
        lean = rng.normal(0, 0.7)
        top = (px + lean, HZ - 1 - hgt)
        palms.line([(px, HZ - 1), top], "#2a342c", 0.8, 0.95)
        for a in np.linspace(0.15, 3.0, 8):
            palms.line([top, (top[0] + math.cos(a) * 3.8, top[1] - math.sin(a) * 2.0 + 2.0)], "#27302a", 0.9, 0.95)
    palms.onto(pic)
    rim = np.clip(np.exp(-ang / 16.0) * 1.4, 0, 1)                 # near the sun the bank's top edge glows
    edge = np.clip(1 - np.abs(y - (bank_top[None, :] - 0.6)) / 1.2, 0, 1)
    over(pic, "#f2e2b8", (edge * rim * 0.6).astype(F32))
    # ---- the river: the sky lying in it, the far bank's dark below the far shore, level streaks, the sun's glitter
    river = (y >= HZ + 1.6).astype(F32)
    t = np.clip((y - HZ) / 60.0, 0, 1)
    wat = ramp(t, [(0.0, "#7f9cbc"), (0.25, "#4f78a8"), (1.0, "#2f5a8c")])
    wat = lerp(wat, ramp(np.clip(x / W, 0, 1), [(0.0, "#3a6aa0"), (0.6, "#5a86b4"), (1.0, "#a8c0d4")]), 0.45)
    streak = noise(shape, (220, 2.4), seed + 9, 4) - 0.5
    wat = wat * (1 + streak[..., None] * 0.16)
    shore = np.clip(1 - (y - (HZ + 1.8)) / 3.5, 0, 1) * river
    wat = lerp(wat, rgb("#33443e"), (shore * 0.7)[..., None])
    over(pic, wat, river)
    # the glitter: short level dashes of light under the sun, thickest in its path, kept right of x 600
    path_x = to_picture(SUN["az"], -SUN["el"])[0]
    spark = noise(shape, (16, 1.6), seed + 10, 2)
    lane = np.exp(-((x - path_x) / 46.0) ** 2) * step(598, 612, x)
    glit = step(0.74, 0.9, spark) * lane * river * np.clip((y - HZ - 2) / 4.0, 0, 1)
    over(pic, "#fffaf0", np.clip(glit * 1.25, 0, 1).astype(F32))
    glow(pic, "#fff4dc", (lane * river * 0.25).astype(F32))
    # ---- the ground beyond the river's near edge, and beside the car: sand (the near bank lies behind the mound)
    line = crest_line(seed + 11)
    # left of the glass (Dad's window): the sand in the car's own shadow, a warm glow; right (the Son's): in the sun
    ground_row = HZ + 34 + (x < 120) * np.clip((120 - x) * 0.9, 0, 200)
    ground = step(0.0, 1.0, y - ground_row) * (x < 60)
    sand_shade = ramp(np.clip((y - HZ) / 300.0, 0, 1), [(0.0, "#d8b48a"), (1.0, "#b8865a")])
    over(pic, sand_shade * (1 + (noise(shape, (60, 14), seed + 12, 3) - 0.5)[..., None] * 0.1), ground.astype(F32))
    # right of the glass (the Son's window): the desert beside the car, in full sun under a sky white with it, and the
    # river's end there (its bank turns away to the right): the brightest pane
    beyond = step(735.0, 760.0, x) * step(0.0, 2.0, y - (HZ + 1.5))
    dunes = HZ + 4.0 + (x - 740) * 0.05 + (noise((1, W * 4), (40, 1), seed + 18, 3)[0, :W][None, :] - 0.5) * 6.0
    lit_sand = ramp(np.clip((y - HZ) / 200.0, 0, 1), [(0.0, "#fae6c0"), (0.3, "#f4d6a2"), (1.0, "#eec48a")])
    lit_sand = lit_sand * (1 + (noise(shape, (70, 18), seed + 19, 3) - 0.5)[..., None] * 0.08)
    over(pic, lit_sand, (beyond * step(0.0, 1.5, y - dunes)).astype(F32))
    over(pic, "#ffffff", (np.exp(-ang / 30.0) * step(735.0, 760.0, x) * (y < HZ) * 0.5).astype(F32))
    # ---- the mound: everything under its ridge
    mound = np.clip(y - line[None, :] + 0.5, 0, 1).astype(F32)
    depth = np.clip((y - line[None, :]) / 110.0, 0, 1)
    face = ramp(depth, [(0.0, "#c8945e"), (0.08, "#a8764c"), (0.45, "#9a6a46"), (1.0, "#a6744c")])
    lump = noise(shape, (140, 60), seed + 13, 4) - 0.5
    face = face * (1 + lump[..., None] * 0.10)
    tint(face, "#9a7a98", np.clip((noise(shape, (160, 70), seed + 14, 3) - 0.3) * 0.8, 0.12, 0.42).astype(F32))    # the cool of shade on warm sand
    rip = np.sin((y - line[None, :]) * 0.62 + noise(shape, (60, 18), seed + 15, 3) * 7.0)
    broken = step(0.55, 0.8, noise(shape, (40, 10), seed + 17, 3))
    face = face * (1 - (step(0.86, 0.99, rip) * broken * 0.06)[..., None])                                          # a few wind ripples, faint and broken
    over(pic, face, mound)
    rimlit = np.clip(1 - (y - line[None, :]) / 3.2, 0, 1) * mound
    over(pic, "#fff0c4", (rimlit * 0.85).astype(F32))
    info = dict(mound=mound, crest=line, river=river * (1 - mound), sky=(y < HZ).astype(F32), glare=glare, glitter=glit, horizon=HZ,
                path_x=path_x, sun_xy=to_picture(SUN["az"], SUN["el"]))
    return np.clip(pic, 0, 1).astype(F32), info


def papyrus(pic, seed=31):
    """A clump of papyrus outside Dad's open window, at the left: dark stems, heads catching a little light."""
    s = Sheet((H, W))
    flora.papyrus_stand(s, 8, 300, 50, 140, seed, count=6, greens=("#1a2418", "#2a3e22", "#46602e", "#8e9454"))
    s.onto(pic)
    return pic

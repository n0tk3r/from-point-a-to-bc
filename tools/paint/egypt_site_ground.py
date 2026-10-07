"""The small things on the ground and in the distance for egypt_site.py: chips of limestone, stones, the
hauling rope, footprints, what the workmen left lying about, and the far left of the picture (the
plateau, another gang at work, the builders' town down by the river)."""

import math

import numpy as np

from brush import *
import land, build
from egypt_site_kit import *
from egypt_site_kit import SHADOW
from egypt_site_plan import *
import egypt_site_props as props
import egypt_site_things as things

ROPE_WAY = [(396, 453), (378, 449), (356, 441), (338, 428), (318, 414), (300, 405), (283, 398), (266, 392), (250, 387), (236, 384), (224, 377), (214, 366)]
SON = [(120, 598), (160, 574), (206, 550), (262, 528), (318, 512), (372, 505), (430, 506), (486, 503), (540, 490), (590, 468), (636, 444), (672, 424), (696, 410)]


def chips(sheet, picture, rng, chance, count, size=(0.5, 1.9), tones=("#fffbe8", "#f6e4bc", "#dcc49c")):
    """Flakes of white limestone lying where `chance` (a mask) is high: each a tiny bright shape with its shadow."""
    h, w = chance.shape
    done = 0
    for _ in range(count * 12):
        if done >= count:
            break
        px, py = rng.random() * w, HZ + 4 + rng.random() * (h - HZ - 5)
        if rng.random() > chance[int(py), int(px)]:
            continue
        r = lerp(size[0], size[1], (py - HZ) / (h - HZ)) * (0.6 + rng.random())
        sheet.ellipse(px + r * 0.9, py + r * 0.35, r * 1.2, max(0.5, r * 0.45), "#6a5884", 0.38)
        a = rng.random() * 3.1
        sheet.poly([(px + math.cos(a + i * 2.1) * r * (0.8 + 0.5 * rng.random()), py + math.sin(a + i * 2.1) * r * 0.6) for i in range(3)] + [(px, py - r * 0.5)],
                   tones[int(rng.integers(len(tones)))], 0.95)
        done += 1
    return sheet


def offcut(sheet, picture, x, y, w, h, d, rng, ground=None, lean=0.0):
    """A squared offcut of white stone lying on the sand, with its shadow (as the dropped block at the riverbank)."""
    land.shadow(picture, mask_poly(picture.shape[:2], [(x + w, y), (x + w + d * 0.8 + h * 0.9, y - d * 0.2 + h * 0.2), (x + w + h * 1.1, y + h * 0.35), (x + w * 0.4, y + 2)], soft=1.2)
                * (1.0 if ground is None else ground), "#665082", 0.5, 0)
    build.block(sheet, x, y, w, h, d, lean=lean)
    return sheet


def bricks(sheet, f, rows=3, seed=0):
    """Mud bricks stacked to dry, a few loose, and the wooden mould they are struck in."""
    rng = np.random.default_rng(seed)
    lit, front, top, joint = "#e2bc88", "#b88e66", "#f0d8a8", "#86644c"
    f.box(sheet, 0, 150, 0, 13 * rows, 0, 62, front=front, top=top, left=lit, right="#8f7468")
    for r in range(1, rows):
        f.line(sheet, [(0, 13 * r, 0), (150, 13 * r, 0)], joint, 0.7, 0.7)
    for r in range(rows):
        for u in np.arange(15 + (r % 2) * 15, 150, 30):
            f.line(sheet, [(u, 13 * r, 0), (u, 13 * r + 13, 0)], joint, 0.7, 0.6)
    for u in np.arange(30, 150, 30):
        f.line(sheet, [(u, 13 * rows, 0), (u, 13 * rows, 62)], joint, 0.7, 0.45)
    f.line(sheet, [(0, 13 * rows, 0), (150, 13 * rows, 0)], "#fff0c8", 0.9, 0.8)
    for (u, d, t) in ((176, 20, 0.2), (196, 52, -0.5), (-34, 30, 0.6)):       # loose ones
        g = Frame(world=(f.w(u, 0, d)[0], f.w(u, 0, d)[2]), turn=math.degrees(t) * 0.4)
        g.box(sheet, 0, 30, 0, 12, 0, 15, front=front, top=top, left=lit, right="#8f7468")
    g = Frame(world=(f.w(230, 0, -6)[0], f.w(230, 0, -6)[2]), turn=-14)      # the mould: an open wooden frame with a handle
    for (u0, u1, d0, d1) in ((0, 34, 0, 3), (0, 34, 17, 20), (0, 3, 0, 20), (31, 34, 0, 20)):
        g.box(sheet, u0, u1, 0, 10, d0, d1, front="#8a623c", top="#d0aa72", left="#b08450", right="#644630")
    g.line(sheet, [(34, 9, 10), (56, 9, 10)], "#8a623c", 1.6)
    return sheet


def log_pile(sheet, x, y, r, n=3, length=60, seed=0):
    """Timber stacked for the scaffold: we see the sawn ends, and the poles running back."""
    rng = np.random.default_rng(seed)
    row = 0
    while n > 0:
        for i in range(n):
            cx, cy = x + (i - (n - 1) / 2) * r * 2.02 + rng.normal(0, 0.3), y - r - row * r * 1.74
            sheet.poly([(cx - r, cy), (cx - r + length * 0.8, cy - length * 0.36), (cx + r + length * 0.8, cy - length * 0.36), (cx + r, cy)], "#7a5a3a")
            sheet.line([(cx - r * 0.2, cy - r * 0.9), (cx - r * 0.2 + length * 0.8, cy - r * 0.9 - length * 0.36)], "#c49a62", max(0.8, r * 0.4), 0.9)
            sheet.ellipse(cx, cy, r, r, "#4a3020")
            sheet.ellipse(cx - r * 0.1, cy - r * 0.1, r * 0.72, r * 0.72, "#b08a58")
            sheet.ellipse(cx - r * 0.1, cy - r * 0.1, r * 0.3, r * 0.3, "#7a5a3a")
        n -= 1
        row += 1
    return sheet


def near(picture, info, seed=21):
    """Everything small on the floor of the site. Painted straight onto the backdrop."""
    shape = picture.shape[:2]
    x, y = grid(shape)
    rng = np.random.default_rng(seed + 300)
    sand, floor, ms, ml = info["sand"], info["floor"], info["ms"], info["ml"]
    road, trod = info["road"], info["trod"]
    s = Paper(shape)

    # ---- the bank against the stone: chips by the thousand, lumps of rock, a few offcuts. Under the shaded
    #      face they lie in the pyramid's shadow, so they are painted on their own sheet and shaded with it
    sb = Paper(shape)
    for (bx, by, r) in [(322, 372, 7), (352, 366, 5), (388, 374, 9), (432, 368, 6), (474, 372, 8), (506, 364, 5), (760, 356, 7)]:
        land.rock_shadow(picture, bx, by, r * 1.3, r * 0.85, ground=floor, amount=0.25)
        land.rock(sb, bx, by, r * 1.3, r * 0.85, seed + bx)
    offcut(sb, picture, 404, 366, 15, 9, 9, rng, floor)
    offcut(sb, picture, 454, 360, 10, 7, 8, rng, floor, lean=-0.08)
    offcut(sb, picture, 336, 362, 12, 8, 8, rng, floor, lean=0.06)
    chips(sb, picture, rng, np.clip(ms * 0.9, 0, 1), 190, size=(0.6, 1.1))
    bc, ba = sb.done()
    over(picture, bc, ba)
    shadow(picture, ba * info["pyr"], 0.46, cool=0.14)
    for (bx, by, r) in [(232, 360, 6), (214, 338, 4), (198, 312, 3)]:           # and on the sunny side
        land.rock_shadow(picture, bx, by, r * 1.3, r * 0.85, ground=floor)
        land.rock(s, bx, by, r * 1.3, r * 0.85, seed + bx)
    chips(s, picture, rng, np.clip(ml * 0.8, 0, 1), 70, size=(0.6, 1.1))
    edge = np.clip(blur(np.maximum(ms, ml), 9) * 2.2 - np.maximum(ms, ml), 0, 1) * sand            # and spilling out over the sand at its foot
    chips(s, picture, rng, edge * 0.8, 130, size=(0.6, 1.2))

    # ---- stones and chips over the floor, thick along the hauling road's margins and round the stacks
    zone = (sand > 0.5) & (y > 372)
    for (mx, my) in list(MARKS.values()) + [SUNSPOT]:
        zone &= np.hypot((x - mx) / 26, (y - my) / 9) > 1                      # but not where people are to stand
    land.stones(s, picture, HZ, seed + 90, 85, zone=zone & (road < 0.3), ground=floor)
    margin = np.clip(blur(road, 6) * 1.6 - road * 1.2, 0, 1) * zone
    chips(s, picture, rng, margin * 0.7 + zone * 0.03, 150, size=(0.5, 1.9))
    heap = np.exp(-(((x - 610) / 70) ** 2 + ((y - 520) / 34) ** 2)) + np.exp(-(((x - 500) / 46) ** 2 + ((y - 496) / 12) ** 2))
    chips(s, picture, rng, np.clip(heap, 0, 1) * zone, 80, size=(0.7, 2.2))
    for (rx, ry, r) in [(196, 588, 9), (218, 595, 5), (566, 548, 10), (590, 556, 6), (30, 492, 8), (470, 590, 9), (446, 596, 5), (744, 434, 5)]:
        land.rock_shadow(picture, rx, ry, r * 1.25, r * 0.85, ground=floor)
        land.rock(s, rx, ry, r * 1.25, r * 0.85, seed + rx)

    # ---- the hauling rope, lying slack from the sledge up to where the gang stands
    sl = things.sledge_frame()
    start = sl.pt(-62, 1, things.RUNNERS[2] * 0.56)
    way = curve([start] + ROPE_WAY, 6)
    for i in range(0, len(way) - 6, 6):
        props.rope(s, way[i:i + 7], lerp(2.4, 1.3, i / len(way)), twist=3.0)
    for (hx, hy) in ((300, 405), (266, 392), (236, 384)):                        # the bars the men haul by, knotted into it
        k = size_at(hy)
        props.log(s, (hx - 22 * k, hy + 2 * k), (hx + 23 * k, hy - 4 * k), max(1.2, 3.6 * k))
        props.lash(s, hx, hy - 1, 1.8, seed=int(hx))

    # ---- the gang's standard, planted where they rest: a painted board on a pole, two streamers. (An invented emblem.)
    px, py = 199.0, 398.0
    k = size_at(py)
    top = py - 262 * k
    land.shadow(picture, mask_line(shape, [(px, py), (px + 262 * k * SHADOW[0], py + 14)], 2.0, soft=0.8) * floor, "#665082", 0.45, 0)
    props.log(s, (px, py), (px + 1, top), max(1.8, 5.5 * k))
    props.log(s, (px - 6, top + 12.5), (px + 8, top + 11.5), 1.3)
    s.poly([(px - 5, top - 1), (px + 6.5, top - 1.5), (px + 6.5, top + 10), (px - 5, top + 10.5)], "#2c6c7e")
    s.poly([(px - 5, top - 1), (px + 6.5, top - 1.5), (px + 6.5, top + 1), (px - 5, top + 1.5)], "#4a94a2")
    s.ellipse(px + 0.8, top + 5, 3.2, 3.2, "#f2c444")
    s.ellipse(px + 0.2, top + 4.4, 1.6, 1.6, "#fbe08a")
    s.line([(px - 5, top - 1), (px + 6.5, top - 1.5), (px + 6.5, top + 10), (px - 5, top + 10.5), (px - 5, top - 1)], "#f6ecd2", 0.8, 0.9)
    s.poly([(px + 1.5, top + 12.5), (px + 15, top + 15), (px + 23, top + 25), (px + 13, top + 22.5), (px + 2, top + 18)], "#b8402c")
    s.line([(px + 3, top + 14.5), (px + 15, top + 17.5), (px + 21, top + 24)], "#de6a4c", 0.9, 0.8)
    s.poly([(px + 1, top + 18.5), (px + 12, top + 24), (px + 16, top + 35), (px + 8, top + 30.5), (px + 1, top + 24.5)], "#f4ead0")
    s.line([(px + 2, top + 21), (px + 10, top + 26), (px + 14, top + 33.5)], "#c8bca0", 0.8, 0.7)

    # ---- where the sand was wetted ahead of the runners: a dark rim, a little shine, the jar and the dipper
    wet = info["wet"]
    shine = step(0.62, 0.8, noise(shape, (26, 3), seed + 55, 2)) * wet
    over(picture, "#e8d2b4", (shine * 0.4).astype(F32))
    jx, jy = 372, 467
    props.jar(s, jx, jy, 23, "water", props.POT)
    s.ellipse(jx + 15, jy + 3, 6, 2.2, "#5e4a7c", 0.4)
    s.ellipse(jx + 14, jy + 1, 5, 2.4, props.POT[2])
    s.ellipse(jx + 14, jy + 0.4, 3.6, 1.4, props.POT[0])
    s.line([(jx + 18, jy), (jx + 27, jy - 5)], props.WOOD[1], 1.2)

    # ---- small sneaker prints: his son came up from the river and went straight for the steps
    walkway = curve(SON, 3)
    for i, (px, py) in enumerate(walkway):
        if sand[int(min(py, shape[0] - 1)), int(min(max(px, 0), shape[1] - 1))] < 0.5:
            continue
        k = size_at(py) * 1.15
        nx, ny = walkway[min(i + 1, len(walkway) - 1)][0] - walkway[max(i - 1, 0)][0], walkway[min(i + 1, len(walkway) - 1)][1] - walkway[max(i - 1, 0)][1]
        n = math.hypot(nx, ny) + 1e-6
        side = 7.5 * k * (1 if i % 2 else -1)
        cx, cy = px - ny / n * side, py + nx / n * side * 0.45
        s.ellipse(cx, cy, 5.0 * k, 2.4 * k, "#a87850", 0.6)
        s.ellipse(cx - nx / n * 3.4 * k, cy - ny / n * 1.3 * k + 0.5 * k, 3.3 * k, 1.5 * k, "#7c5840", 0.45)

    # ---- left lying about: levers behind the sledge, mud bricks and their mould before the podium, timber, a basket
    for (a, b, wd) in (((512, 498), (592, 489), 3.2), ((528, 504), (600, 499), 2.8)):
        s.line([(a[0] + 2, a[1] + 2.5), (b[0] + 2, b[1] + 2.5)], "#5e4a7c", wd, 0.4)
        props.log(s, a, b, wd, knots=2, seed=int(a[0]))
    bricks(s, Frame((530, 394), turn=-6), rows=3, seed=4)
    props.basket(s, 516, 384, 15, 9, seed=7)
    props.jar(s, 665, 405, 20, "beer", stopper="#a39078")
    props.jar(s, 656, 409, 13, "water", props.MARL)
    log_pile(s, 772, 393, 4.2, n=3, length=30, seed=3)
    props.coil(s, 596, 421, 10, 3.6, turns=3, width=1.5)
    # on the landing by the doorway: lamps and oil for going in
    for i, (du, hh) in enumerate(((-NOTCH_W / 2 + 52, 34), (-NOTCH_W / 2 + 84, 26), (NOTCH_W / 2 - 40, 30))):
        c = P(*G(NOTCH_S + du, Q_FACE + 70, LAND_Y))
        props.jar(s, c[0], c[1], hh * FOC / G(NOTCH_S, Q_FACE + 70, 0)[2], "beer" if i != 1 else "water", props.MARL if i == 1 else props.POT, shadow=False, stopper=None)
    s.onto(picture)
    return picture


def far(picture, info, seed=21):
    """The far left, before the queens' pyramids are said again: beyond the plateau's lip, the builders'
    town and the river, pale with distance."""
    shape = picture.shape[:2]
    rng = np.random.default_rng(seed + 400)
    lip = info["lip"]
    s = Paper(shape)
    s.line([(0, HZ + 1.7), (60, HZ + 1.4), (178, HZ + 1.2)], "#f8fffa", 1.6, 0.95)  # the river: a thin bright line
    s.line([(0, HZ + 3.2), (178, HZ + 2.8)], "#8faa80", 1.0, 0.55)
    s.poly([(58, HZ + 1.5), (61.2, HZ - 4.0), (61.8, HZ + 1.5)], "#fff6dc")     # a sail on it
    s.line([(55.5, HZ + 2), (65, HZ + 2)], "#6a5646", 1.0, 0.9)
    for k in range(26):                                                        # palms down there are only dabs
        px = rng.random() * 176
        py = HZ + 4.5 + rng.random() * 5
        hgt = 2.5 + rng.random() * 2.2
        s.line([(px, py), (px + rng.normal(0, 0.5), py - hgt)], "#8a9c7a", 0.8, 0.7)
        s.ellipse(px, py - hgt, 1.7, 1.1, "#7c9a70", 0.8)
    for k, hx in enumerate([4, 15, 24, 37, 49, 58, 71, 86, 97, 109, 121, 136, 148, 160]):      # the town: flat roofs on the edge of the fields
        hy = float(lip[int(hx)]) - 4.2 - (k % 3) * 1.5
        build.hut(s, hx, hy, 5 + (k * 5) % 4, 2.6 + (k % 2) * 0.8, 2.5, seed + 30 + k, wall="#e6cca4", shade="#b8a4a8", roof="#f2e0b8", door="#8a7470")
    s.onto(picture, 0.85)
    for sx in (20, 88, 140):                                                    # bread ovens smoking
        sy = float(lip[sx]) - 8
        smoke = mask_line(shape, curve([(sx, sy), (sx + 3, sy - 7), (sx + 9, sy - 13), (sx + 20, sy - 17)], 6), [1.0, 1.6, 2.4, 3.2, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5][:19], soft=1.6)
        over(picture, "#f4ecdc", smoke * 0.32)
    return picture


def middle(picture, info, seed=21):
    """The plateau on the left between the far things and the scribe's awning: the stone yard, where
    blocks wait in rows beside the hauling road, a store hut, heaps of chips, and the foot of the great ramp."""
    shape = picture.shape[:2]
    rng = np.random.default_rng(seed + 500)
    floor = info["floor"]
    s = Paper(shape)
    # the foot of the builders' great ramp, beyond the pyramid's far corner: mud brick, rising to the right, men on it
    fc = LIT.pt(BASE, 0)
    s.poly([(fc[0] - 78, fc[1] + 3), (fc[0] - 30, fc[1] - 6), (fc[0] + 5, fc[1] - 16), (fc[0] + 5, fc[1] + 2)], "#dcb686")
    s.poly([(fc[0] - 78, fc[1] + 3), (fc[0] - 30, fc[1] - 6), (fc[0] + 5, fc[1] - 16), (fc[0] + 5, fc[1] - 13.6), (fc[0] - 30, fc[1] - 3.8)], "#f8e6ba")
    s.line([(fc[0] - 78, fc[1] + 3.5), (fc[0] + 5, fc[1] + 2.5)], "#a07c62", 0.9, 0.6)
    for i in range(5):
        t = 0.22 + i * 0.15
        props.dab(s, fc[0] - 78 + 82 * t, fc[1] + 3 - 19.5 * t - 1.2, 4.6, lean=0.2)
    s.poly([(fc[0] - 28, fc[1] - 8.6), (fc[0] - 21, fc[1] - 10.6), (fc[0] - 21, fc[1] - 15), (fc[0] - 28, fc[1] - 13)], "#fffbe6")
    s.poly([(fc[0] - 21, fc[1] - 10.6), (fc[0] - 19, fc[1] - 11.8), (fc[0] - 19, fc[1] - 16), (fc[0] - 21, fc[1] - 15)], "#b0a4bc")
    # blocks waiting in rows beside the road
    yard = [(78, 297, 1.0), (102, 294, 0.95), (125, 291, 0.9), (30, 318, 1.0), (64, 314, 1.1), (99, 310, 1.0), (133, 305, 0.9)]
    for (bx, by, m) in yard:
        k = size_at(by)
        w, h, d = 150 * k * m, 100 * k * m, 110 * k
        land.shadow(picture, mask_poly(shape, [(bx + w, by), (bx + w + h * 1.0 + d * 0.6, by - d * 0.25 + h * 0.2), (bx + w + h * 1.0, by + h * 0.4), (bx + w * 0.4, by + 1.5)], soft=1.0) * floor, "#665082", 0.5, 0)
        if m > 1.02:                                                             # one or two still on the sledges they came on
            s.line([(bx - w * 0.22, by - 2.5), (bx - w * 0.08, by + 1), (bx + w * 1.05, by + 1.2)], "#5a4030", max(1.2, w * 0.07))
        tones = (("#fff0c6", "#e2c592"), ("#fbe8bc", "#dcbc88"), ("#fff4d2", "#e8cc9a"))[int(rng.integers(3))]
        build.block(s, bx, by, w, h, d, light=tones[0], front=tones[1], lean=rng.normal(0, 0.02))
        s.line([(bx + w * 0.08, by - h * 0.92), (bx + w * 0.92, by - h * 0.92)], "#fff6dc", 0.7, 0.5)       # the drafted margin along its top
        if rng.random() < 0.5:                                                   # a gang's red mark on some
            s.line([(bx + w * 0.25, by - h * 0.6), (bx + w * 0.4, by - h * 0.35), (bx + w * 0.55, by - h * 0.6)], "#b4452c", 0.8, 0.7)
    props.log(s, (28, 326), (70, 321), 1.5)                                     # levers left among them
    s.onto(picture)
    return picture

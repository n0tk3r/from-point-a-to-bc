"""The castle approach at Himeji (edo-castle), round twenty-three (DEPTH.md): the FAR plane, laid in watercolour behind the
walked ground, layer behind layer, each paler, plainer and nearer the sky's colour at the horizon than the one in front
of it, and none of them with a key line (the act's watercolour: DEPTH.md, "Japan in watercolour").

From the farthest to the nearest:

    the sky         a graded wash, deep at the top, the paper warmed by the low sun at the horizon on the right; clouds
                    lifted out of it, large and high, small and flat toward the horizon, lit on the side toward the sun
    the hills       the hills of Harima in three ranges, the farthest the palest
    the town        roofs of the castle town in rows under the hills (far: grey-blue, small, no line)
    the keep        edo_castle_model's keep through the scene's camera: its stone base of fitted stones, five roofs,
                    their gables, plastered eaves, white walls and windows; the long face lit, the short face in shade; the
                    corridor turret on from its right side (behind the gate tower). A breath of the evening air on it.
    the hill        the castle hill's pines round the keep's foot and an inner wall's tiled coping

paint_far(seed) -> (picture, info): info holds the masks the finish and the layout need (sky, clouds, hills, town,
keep, base, wing, hill).
"""

import math

import numpy as np

from brush import *
import land
import sky as skylib
from edo_village_kit import (COBALT, CERULEAN, LAKE, NAPLES, OCHRE, PRUSSIAN, SIENNA, ULTRA, VERONESE, VIRIDIAN, WHITE, WPAPER,
                             Wet, mixp, thin, tintw)
from edo_village_kit import P as PAINT
from edo_castle_kit import EYE, FOC, H, HZ, SHAPE, W
import edo_castle_model as MD

LILAC = PAINT("lilac")
HORIZON_C = lerp(WPAPER, lerp(CERULEAN, NAPLES, 0.40), 0.20)          # the sky low down: paper, a breath of blue, warmed
AIR = lerp(WPAPER, CERULEAN, 0.30)                                     # the evening air between us and far things

# the keep's paints (thinned toward the paper, as washes are)
WALL_LIT = lerp(WPAPER, NAPLES, 0.16)
WALL_SUN = lerp(WPAPER, mixp(NAPLES, "chrome-orange", 0.30), 0.32)     # the last light where it falls fullest
WALL_SHADE = thin(mixp(COBALT, LILAC, 0.55), 0.60)
WALL_BOUNCE = thin(mixp(LILAC, NAPLES, 0.45), 0.58)                    # the shade's foot, warmed by light thrown up
SOFFIT = thin(mixp(LILAC, COBALT, 0.35), 0.70)
ROOF_LIT = thin(mixp(PRUSSIAN, COBALT, 0.30), 0.52)
ROOF_LIT_WARM = lerp(ROOF_LIT, NAPLES, 0.16)
ROOF_SHADE = thin(mixp(PRUSSIAN, ULTRA, 0.25), 0.34)
ROOF_DEEP = thin(PRUSSIAN, 0.16)
STONE_LIT = thin(mixp(OCHRE, SIENNA, 0.22), 0.48)
STONE_TOP = thin(mixp(OCHRE, NAPLES, 0.35), 0.56)
STONE_SHADE = thin(mixp(COBALT, SIENNA, 0.32), 0.46)
JOINT = thin(mixp(SIENNA, PRUSSIAN, 0.55), 0.30)
WINDOW = thin(mixp(PRUSSIAN, SIENNA, 0.18), 0.12)
PINE = thin(mixp(VIRIDIAN, PRUSSIAN, 0.50), 0.16)
PINE_LIT = thin(mixp(VERONESE, OCHRE, 0.32), 0.24)


# ================================================================ the sky
def paint_sky(seed):
    x, y = grid(SHAPE)
    drift = (noise(SHAPE, (520, 230), seed, 3) - 0.5) * 0.12
    t = np.clip(y / float(HZ) + drift, 0, 1)
    pic = ramp(t, [(0.0, thin(mixp(COBALT, ULTRA, 0.30), 0.05)), (0.18, thin(mixp(COBALT, ULTRA, 0.12), 0.12)), (0.40, thin(COBALT, 0.28)),
                   (0.62, thin(mixp(COBALT, CERULEAN, 0.6), 0.46)), (0.82, thin(CERULEAN, 0.70)), (0.95, HORIZON_C), (1.0, HORIZON_C)])
    pic *= (1 + (noise(SHAPE, (420, 34), seed + 1, 3) - 0.5)[..., None] * 0.07)           # the wide brush, drawn across
    # the sun is low on the right, behind us: the paper warms low on that side
    glow(pic, thin(NAPLES, 0.35), (np.clip((x - 300) / 500.0, 0, 1) * np.clip(1 - np.abs(y - 250) / 110.0, 0, 1) * 0.16).astype(F32))
    return np.clip(pic, 0, 1).astype(F32)


def paint_clouds(pic, seed):
    """Clouds lifted out of the wet wash, lit on the side toward the low sun (right), a thin grey-violet under them;
    large high up, small and flat toward the horizon. -> their mask."""
    x, y = grid(SHAPE)
    shade = thin(mixp(COBALT, LILAC, 0.45), 0.62)
    tones = (shade, thin(mixp(COBALT, SIENNA, 0.12), 0.80), lerp(WPAPER, NAPLES, 0.10), lerp(WPAPER, NAPLES, 0.30))
    masses = [(612, 74, 250, 52, 26), (120, 52, 190, 34, 16), (452, 128, 150, 26, 12), (744, 150, 150, 24, 12),
              (560, 192, 110, 13, 8), (700, 214, 96, 9, 7), (420, 222, 70, 7, 5)]
    thick = skylib.paint_clouds(pic, masses, seed + 5, tones, light=(0.85, -0.5), ragged=11.0, amount=0.92, reach=30.0)
    n = noise(SHAPE, (300, 15), seed + 6, 4)
    slant = sample(n, x - (140 - y) * 1.2, y)
    high = step(0.64, 0.90, slant) * np.clip(1 - y / 90.0, 0, 1) * 0.26
    low = step(0.62, 0.9, noise(SHAPE, (240, 7), seed + 7, 3)) * np.clip(1 - np.abs(y - 238) / 26.0, 0, 1) * 0.42
    wisp = blur((high + low).astype(F32), 1.0)
    over(pic, lerp(WPAPER, NAPLES, 0.12), wisp)
    return np.clip(thick + wisp, 0, 1).astype(F32)


# ================================================================ the hills and the town
def far_layer(pic, crest, color, seed, rough=1.6, base=HZ + 60, foot=0.55, foot_rows=14.0, lit=None, lit_amount=0.0):
    """One far layer of land under a skyline: a wash of `color`, paler toward its foot (the air lies in the hollows
    between layers), lighter where it turns to the sun. No line. -> its mask."""
    x, y = grid(SHAPE)
    m, line = land.ridge(SHAPE, crest, base, seed, rough=rough)
    body = np.empty(SHAPE + (3,), dtype=F32)
    body[...] = color
    body *= (1 + (noise(SHAPE, (60, 22), seed + 2, 3) - 0.5)[..., None] * 0.08)
    if lit is not None and lit_amount:
        n = noise(SHAPE, (34, 16), seed + 3, 3)
        facing = np.clip((np.roll(n, 3, axis=1) - n) * 9.0, 0, 1)            # slopes turned to the right take the sun
        body = lerp(body, np.asarray(lit, dtype=F32), (facing * lit_amount)[..., None])
    down = np.clip((y - (line[None, :] + 1)) / foot_rows, 0, 1)
    body = lerp(body, HORIZON_C, (down ** 1.3 * foot)[..., None])
    over(pic, body, m.astype(F32))
    return m.astype(F32)


def paint_hills(pic, seed):
    a = [(-10, 252), (70, 244), (150, 250), (240, 238), (330, 246), (430, 230), (500, 216), (548, 222), (600, 232), (690, 220), (760, 228), (812, 222)]
    m = far_layer(pic, a, thin(mixp(COBALT, CERULEAN, 0.45), 0.70), seed + 40, rough=1.8, foot=0.75, foot_rows=22.0,
                  lit=lerp(HORIZON_C, NAPLES, 0.15), lit_amount=0.45)
    b = [(-10, 268), (80, 260), (170, 266), (290, 256), (400, 262), (490, 240), (530, 236), (570, 246), (650, 244), (740, 256), (812, 250)]
    m = np.maximum(m, far_layer(pic, b, thin(mixp(COBALT, VIRIDIAN, 0.28), 0.56), seed + 44, rough=1.6, foot=0.65, foot_rows=16.0,
                                lit=thin(mixp(CERULEAN, VERONESE, 0.4), 0.62), lit_amount=0.45))
    c = [(-10, 281), (60, 277), (140, 280), (230, 274), (330, 279), (450, 272), (540, 276), (620, 270), (720, 276), (812, 272)]
    m = np.maximum(m, far_layer(pic, c, thin(mixp(VIRIDIAN, COBALT, 0.40), 0.44), seed + 48, rough=2.2, foot=0.55, foot_rows=10.0,
                                lit=thin(mixp(VERONESE, OCHRE, 0.2), 0.50), lit_amount=0.5))
    return m


def paint_town(pic, seed):
    """The castle town's roofs in rows under the hills: small grey-blue roofs, white walls under their eaves, each row
    paler and smaller the farther it is. Far: no line. -> its mask."""
    rng = np.random.default_rng(seed)
    L = Wet(SHAPE)
    rows = [(262, 3.2, 0.66, 1.0), (271, 4.0, 0.60, 1.0), (283, 4.8, 0.54, 1.0), (293, 6.0, 0.48, 1.0), (302, 7.5, 0.42, 1.0)]
    for (yy, size, thin_t, _) in rows:
        x = -8.0
        roof_c = thin(mixp(PRUSSIAN, COBALT, 0.35), thin_t)
        wall_c = lerp(WPAPER, CERULEAN, 0.10 + 0.25 * (thin_t - 0.4))
        while x < 810:
            w = size * rng.uniform(2.2, 4.6)
            h = size * rng.uniform(0.6, 1.0)
            y0 = yy + rng.normal(0, 1.1)
            ridge = (x + w * rng.uniform(0.3, 0.7), y0 - h)
            if rng.random() < 0.85:
                L.poly([(x, y0 + size * 0.75), (x + w, y0 + size * 0.75), (x + w, y0), (x, y0)], wall_c)                 # the wall under the eave
                L.poly([(x - size * 0.25, y0 + 0.5), (x + w + size * 0.25, y0 + 0.5), (ridge[0] + w * 0.25, ridge[1]), (ridge[0] - w * 0.25, ridge[1])],
                       lerp(roof_c, WPAPER, rng.uniform(0.0, 0.18)), roof_c, g=((x, y0 - h), (x + w, y0)))
            x += w * rng.uniform(0.75, 1.15)
    c, a = L.done()
    c = lerp(c, HORIZON_C, 0.25)
    over(pic, c, a)
    return a


# ================================================================ the keep
def poly_mask(pts):
    from PIL import Image, ImageDraw
    im = Image.new("L", (W * 3, H * 3), 0)
    ImageDraw.Draw(im).polygon([(px * 3, py * 3) for px, py in pts], fill=255)
    return np.asarray(im.resize((W, H), Image.BOX), dtype=F32) / 255


def wall_face(L, fr, d, side, sun=True):
    """A storey's wall: the long face lit (warm, fullest toward its right), the short face in shade (cool, warmed at
    its foot by light thrown up)."""
    A, B, y0, y1 = d["A"], d["B"], d["y0"], d["y1"]
    if side == "front":
        pts = [fr.p(-A, y0, -B), fr.p(A, y0, -B), fr.p(A, y1, -B), fr.p(-A, y1, -B)]
        L.poly(pts, WALL_LIT, WALL_SUN, g=(pts[0], pts[1]))
    else:
        pts = [fr.p(-A, y0, B), fr.p(-A, y0, -B), fr.p(-A, y1, -B), fr.p(-A, y1, B)]
        L.poly(pts, WALL_SHADE, WALL_BOUNCE, g=((pts[2][0], pts[2][1]), (pts[1][0], pts[1][1])))
    return pts


def eave_shadow(L, fr, d):
    """The eave's shadow on the lit face: a band under it about as deep as the eave reaches times the sun's height."""
    A, B, y1 = d["A"], d["B"], d["y1"]
    drop = d["e"] * 0.37 + 18
    pts = [fr.p(-A, y1, -B), fr.p(A, y1, -B), fr.p(A, y1 - drop * 1.05, -B), fr.p(-A, y1 - drop * 0.92, -B)]
    L.glaze(pts, lerp(np.ones(3, F32), mixp(COBALT, LILAC, 0.5), 0.36))


def windows(L, fr, d, side, n, rng):
    A, B, y0, y1 = d["A"], d["B"], d["y0"], d["y1"]
    h = y1 - y0
    wy0, wy1 = y0 + h * 0.20, y0 + h * 0.20 + min(118.0, h * 0.42)
    span = (2 * A) if side == "front" else (2 * B)
    ww = min(96.0, span / (n * 2.4))
    for j in range(n):
        c = -span / 2 + span * (j + 0.5) / n
        if side == "front":
            q = lambda a_, y_: fr.p(a_, y_, -B - 4)
        else:
            q = lambda a_, y_: fr.p(-A - 4, y_, -a_)
        pts = [q(c - ww / 2, wy0), q(c + ww / 2, wy0), q(c + ww / 2, wy1), q(c - ww / 2, wy1)]
        L.poly(pts, WINDOW, lerp(WINDOW, WALL_SHADE, 0.35), g=(pts[3], pts[0]))
        for k in range(1, 4):                                                   # the bars: plastered posts, lighter
            t = k / 4
            a_ = c - ww / 2 + ww * t
            L.line([q(a_, wy0 + 3), q(a_, wy1 - 3)], lerp(WALL_SHADE, WPAPER, 0.4) if side == "front" else WALL_SHADE, 0.55, 0.85)
        L.line([q(c - ww / 2 - 6, wy0 - 4), q(c + ww / 2 + 6, wy0 - 4)], WALL_LIT if side == "front" else WALL_BOUNCE, 0.6, 0.7)   # the sill


def soffit(L, fr, d):
    """The plastered underside of the eave, seen from below: between the eave's edge and the top of the wall."""
    A, B, y1, ye, e, lift = d["A"], d["B"], d["y1"], d["ye"], d["e"], d["lift"]
    Ae, Be = A + e, B + e
    L.poly([fr.p(-Ae, ye + lift, Be), fr.p(-Ae, ye + lift * 0.6, 0), fr.p(-Ae, ye + lift, -Be), fr.p(-A, y1, -B), fr.p(-A, y1, B)], SOFFIT)
    L.poly([fr.p(-Ae, ye + lift, -Be), fr.p(0, ye + lift * 0.0, -Be), fr.p(Ae, ye + lift, -Be), fr.p(A, y1, -B), fr.p(-A, y1, -B)], lerp(SOFFIT, WALL_BOUNCE, 0.35))


def roof_skirt(L, fr, d, rng):
    """A skirt roof: its left slope (half lit: it faces away from the sun) and its long front slope (lit), the tiles'
    rows running down them, the white-plastered hip at the near corner, the eave's dark edge of tile ends."""
    ef = MD.eave_pts(fr, d, "front")
    el = MD.eave_pts(fr, d, "left")
    A2, B2, y2 = d["A2"], d["B2"], d["y2"]
    top_f = [fr.p(A2, y2, -B2), fr.p(-A2, y2, -B2)]
    top_l = [fr.p(-A2, y2, -B2), fr.p(-A2, y2, B2)]
    L.poly(el + top_l, ROOF_SHADE, lerp(ROOF_SHADE, ROOF_LIT, 0.35), g=(el[0], el[-1]))
    L.poly(ef + top_f, ROOF_LIT, ROOF_LIT_WARM, g=(ef[0], ef[-1]))
    # the rows of round tiles, down each slope
    for (ev, top, tone, alpha) in ((ef, [fr.p(-A2, y2, -B2), fr.p(A2, y2, -B2)], ROOF_SHADE, 0.30), (el, [fr.p(-A2, y2, B2), fr.p(-A2, y2, -B2)], ROOF_DEEP, 0.30)):
        n = len(ev) - 1
        for j in range(1, 3 * n):
            t = j / (3 * n)
            i0 = min(int(t * n), n - 1)
            f = t * n - i0
            p0 = (ev[i0][0] + (ev[i0 + 1][0] - ev[i0][0]) * f, ev[i0][1] + (ev[i0 + 1][1] - ev[i0][1]) * f)
            tt = min(max((t - 0.12) / 0.76, 0.0), 1.0)                              # the hips cut the rows off at the ends
            p1 = (top[0][0] + (top[1][0] - top[0][0]) * tt, top[0][1] + (top[1][1] - top[0][1]) * tt)
            if t < 0.12 or t > 0.88:
                k = (0.12 - t) / 0.12 if t < 0.12 else (t - 0.88) / 0.12
                p1 = (p1[0] + (p0[0] - p1[0]) * k, p1[1] + (p0[1] - p1[1]) * k)
            L.line([p0, p1], tone, 0.45, alpha * rng.uniform(0.6, 1.0))
    # the white hips (the near corner's, and the far ends'), the plastered ridge where the roof meets the wall above
    near_e = ef[0]
    L.line([near_e, fr.p(-A2, y2, -B2)], lerp(WPAPER, WALL_SHADE, 0.25), 1.5)
    L.line([ef[-1], fr.p(A2, y2, -B2)], lerp(WPAPER, NAPLES, 0.1), 1.2)
    L.line([el[0], fr.p(-A2, y2, B2)], lerp(WPAPER, WALL_SHADE, 0.45), 1.1)
    L.line(top_f[::-1], lerp(ROOF_DEEP, ROOF_SHADE, 0.5), 0.8, 0.8)
    L.line(top_l, lerp(ROOF_DEEP, ROOF_SHADE, 0.5), 0.8, 0.8)
    # the eave's edge: the tile ends, dark, with the white plaster line of the first course under them
    L.line(el, ROOF_DEEP, 1.6)
    L.line(ef, ROOF_DEEP, 1.6)
    L.line([(px, py + 1.1) for px, py in el], lerp(WPAPER, WALL_SHADE, 0.5), 0.6, 0.8)
    L.line([(px, py + 1.1) for px, py in ef], WPAPER, 0.6, 0.8)


def roof_top(L, fr, d, rng):
    """The top roof: hip and gable, its long ridge with a fish (shachi) rising at each end; the gable at its left end in
    shade with the gable's ornament."""
    A, B, ye, e, lift = d["A"], d["B"], d["ye"], d["e"], d["lift"]
    Ae, Be = A + e, B + e
    ra, yr = d["ridge_a"], d["yr"]
    ef = MD.eave_pts(fr, d, "front")
    el = MD.eave_pts(fr, d, "left")
    hip_y = ye + (yr - ye) * 0.42
    ag = -ra - (Ae - ra) * 0.30
    g0, g1 = fr.p(ag, hip_y, Be * 0.66), fr.p(ag, hip_y, -Be * 0.66)
    apex = fr.p(-ra - 20, yr - 10, 0)
    L.poly(el + [g1, g0], ROOF_SHADE, lerp(ROOF_SHADE, ROOF_LIT, 0.3), g=(el[0], el[-1]))          # the left hip's slope under the gable
    L.poly(ef + [fr.p(ra, yr, 0), fr.p(-ra, yr, 0)], ROOF_LIT, ROOF_LIT_WARM, g=(ef[0], ef[-1]))    # the long slope
    L.poly([g0, g1, apex], WALL_SHADE, WALL_BOUNCE, g=(apex, g1))                                   # the gable, white in shade
    L.line([g0, apex, g1], ROOF_DEEP, 1.4)
    L.line([(g0[0] - 1, g0[1] + 1.2), (apex[0], apex[1] + 1.4), (g1[0] - 0.5, g1[1] + 1.2)], lerp(WPAPER, WALL_SHADE, 0.3), 0.6)
    L.ellipse(apex[0] + 0.2, apex[1] + 4.0, 1.2, 1.6, ROOF_DEEP)                                     # the gable's ornament
    n = len(ef) - 1
    for j in range(1, 3 * n):                                                                      # the tiles' rows on the long slope
        t = j / (3 * n)
        i0 = min(int(t * n), n - 1)
        f = t * n - i0
        p0 = (ef[i0][0] + (ef[i0 + 1][0] - ef[i0][0]) * f, ef[i0][1] + (ef[i0 + 1][1] - ef[i0][1]) * f)
        tt = min(max((t - 0.18) / 0.64, 0.0), 1.0)
        p1 = fr.p(-ra + 2 * ra * tt, yr, 0)
        if t < 0.18 or t > 0.82:
            k = (0.18 - t) / 0.18 if t < 0.18 else (t - 0.82) / 0.18
            p1 = (p1[0] + (p0[0] - p1[0]) * k, p1[1] + (p0[1] - p1[1]) * k)
        L.line([p0, p1], ROOF_SHADE, 0.45, 0.32 * rng.uniform(0.6, 1.0))
    L.line([ef[0], fr.p(-ra, yr, 0)], lerp(WPAPER, WALL_SHADE, 0.25), 1.4)                         # the hips, white
    L.line([ef[-1], fr.p(ra, yr, 0)], lerp(WPAPER, NAPLES, 0.1), 1.2)
    L.line(el, ROOF_DEEP, 1.6)
    L.line(ef, ROOF_DEEP, 1.6)
    L.line([(px, py + 1.1) for px, py in ef], WPAPER, 0.6, 0.8)
    # the ridge: plastered white on its sunlit side, its top dark; the two fish, tails up
    r0, r1 = fr.p(-ra, yr, 0), fr.p(ra, yr, 0)
    L.line([r0, r1], ROOF_DEEP, 2.6)
    L.line([(r0[0], r0[1] + 1.0), (r1[0], r1[1] + 1.0)], lerp(WPAPER, NAPLES, 0.12), 1.1)
    for end, sgn in ((-ra, -1), (ra, 1)):
        bx, by = fr.p(end, yr, 0)
        k = fr.k(end, 0)
        hgt = 175 * k                                                               # the fish: about 1.8 m tall
        body = [(bx - 1.4, by), (bx + 1.4, by), (bx + 1.9 + sgn * 0.6, by - hgt * 0.45), (bx + sgn * 2.6, by - hgt * 0.85), (bx + sgn * 4.0, by - hgt),
                (bx + sgn * 1.2, by - hgt * 0.80), (bx - 1.9 + sgn * 0.4, by - hgt * 0.45)]
        L.poly(body, ROOF_DEEP)
        L.line([(bx + 1.0, by - 1), (bx + 1.6 + sgn * 0.4, by - hgt * 0.5)], lerp(ROOF_LIT, NAPLES, 0.5), 0.5, 0.8)   # a glint of the sun on it
    return r0, r1


def gable(L, fr, d, face, place, w, h, kind, up, rng):
    """A gable on a skirt roof's slope: chidori (a triangle standing on the slope, white, its edges dark tiles),
    irimoya (a great triangle on the eave), kara (the eave lifted in a bell's curve over a white face)."""
    lit = face == "front"
    white = WALL_LIT if lit else WALL_SHADE
    white2 = WALL_SUN if lit else WALL_BOUNCE
    if face == "front":
        a_c = place * (d["A2"] if kind == "chidori" else d["A"])
        if kind == "kara":
            bq = -(d["B"] + d["e"])
            yq = d["ye"]
        else:
            bq, yq = MD.slope_at(d, "front", up)
        q = lambda a_, y_: fr.p(a_, y_, bq)
    else:
        a_c = place * (d["B2"] if kind == "chidori" else d["B"])
        if kind == "kara":
            aq = -(d["A"] + d["e"])
            yq = d["ye"]
        else:
            aq, yq = MD.slope_at(d, "left", up)
        q = lambda a_, y_: fr.p(aq, y_, -a_)
    if kind in ("chidori", "irimoya"):
        b0, b1, ap = q(a_c - w / 2, yq), q(a_c + w / 2, yq), q(a_c, yq + h)
        # its own little roof seen from below: the two eaves of the gable reach out past its foot
        e0, e1 = q(a_c - w / 2 - 40, yq - 18), q(a_c + w / 2 + 40, yq - 18)
        L.poly([b0, b1, ap], white, white2, g=(ap, b1))
        if lit:                                                                     # the right bargeboard's shadow inside the face
            sh = [ap, q(a_c - w * 0.08, yq + h * 0.82), b0, q(a_c - w / 2 + w * 0.10, yq)]
            L.glaze([ap, b0, q(a_c - w * 0.38, yq), q(a_c - w * 0.03, yq + h * 0.86)], lerp(np.ones(3, F32), mixp(COBALT, LILAC, 0.5), 0.30))
        L.line([e0, ap, e1], ROOF_DEEP, 1.7 if kind == "chidori" else 2.2)
        L.line([(e0[0] + 0.6, e0[1] + 1.4), (ap[0], ap[1] + 1.6), (e1[0] - 0.6, e1[1] + 1.4)], lerp(WPAPER, SOFFIT, 0.4 if lit else 0.8), 0.6)
        L.ellipse(ap[0], ap[1] + 3.2, 1.1, 1.5, ROOF_DEEP)                       # the ornament under its apex
        if kind == "irimoya":                                                       # the great gable's own lattice of boards, faint
            for k in range(1, 4):
                t = k / 4
                pa, pb = q(a_c - w / 2 * (1 - t), yq + h * t), q(a_c + w / 2 * (1 - t), yq + h * t)
                L.line([pa, pb], lerp(white, WALL_SHADE, 0.5), 0.5, 0.6)
    else:
        n = 14
        top, bot = [], []
        for j in range(n + 1):
            t = j / n
            u = (t - 0.5) * 2
            bell = math.exp(-(u * 1.55) ** 2) - 0.10 * (abs(u) > 0.75) * (abs(u) - 0.75) * 4
            top.append(q(a_c - w / 2 + w * t, yq + h * max(bell, -0.05)))
            bot.append(q(a_c - w / 2 + w * t, yq - 10))
        L.poly(top + bot[::-1], white, white2, g=(top[n // 2], bot[n // 2]))
        L.line(top, ROOF_DEEP, 2.0)
        L.line([(px, py + 1.3) for px, py in top], lerp(WPAPER, SOFFIT, 0.3 if lit else 0.8), 0.6)


def base_stones(L, fr, yb, rng, face):
    """The stone base's face: fitted stones in rough courses (every stone a different shape, no gaps), the corner's
    long and short stones interlocking, the batter curving out toward the foot."""
    At, Bt = 1230.0, 1010.0
    depth = MD.BASE_HEIGHT
    flare = MD.BASE_FLARE
    yf = yb - depth

    def half(y):
        t = max((yb - y) / depth, 0.0)
        return At + flare * t ** 1.8, Bt + flare * t ** 1.8

    def q(s, y):                                     # s: along the face (-1 near corner .. 1 far end), y: height
        Ah, Bh = half(y)
        if face == "front":
            return fr.p(-Ah + (s + 1) * Ah, y, -Bh)
        return fr.p(-Ah, y, -Bh + (s + 1) * Bh)
    ys = np.linspace(yb, yf, 18)
    for y_a, y_b in zip(ys[:-1], ys[1:]):
        pts = [q(-1, y_a), q(1, y_a), q(1, y_b), q(-1, y_b)]
        if face == "front":
            L.poly(pts, STONE_TOP if y_a == ys[0] else STONE_LIT, STONE_LIT, g=(pts[0], pts[3]))
        else:
            L.poly(pts, STONE_SHADE, lerp(STONE_SHADE, STONE_LIT, 0.22), g=(pts[0], pts[3]))
    y = yb - 6
    row = 0
    while y > yf + 60:
        hgt = rng.uniform(95, 150)
        y1 = y - hgt
        s = -1.0
        ln_unit = 2.0 / ((2 * (1230 if face == "front" else 1010)) / 170.0)
        first = True
        while s < 1.0:
            ln = ln_unit * rng.uniform(0.55, 1.45) * (1.7 if first and row % 2 == 0 else (0.75 if first else 1.0))
            s1 = min(1.0, s + ln)
            tone = rng.uniform(-0.06, 0.06)
            base_c = STONE_LIT if face == "front" else STONE_SHADE
            c = np.clip(base_c * (1 + tone), 0, 1)
            sk = rng.uniform(-0.05, 0.05) * ln
            pts = [q(s, y), q(s1, y + rng.uniform(-8, 8)), q(s1 + sk, y1), q(s + sk, y1 + rng.uniform(-8, 8))]
            L.poly(pts, c, alpha=0.55)
            L.line([pts[1], pts[2]], JOINT, 0.55, 0.55)
            if face == "front":                                                    # the top edge of a stone catches the light
                L.line([pts[0], pts[1]], lerp(STONE_TOP, WPAPER, 0.3), 0.5, 0.5)
            s, first = s1, False
        L.line([q(-1, y1), q(1, y1)], JOINT, 0.6, 0.65)
        y, row = y1, row + 1


def paint_wing(L, fr, yb, rng):
    """The corridor turret on from the keep's right side: a white wall with a row of windows under a hip roof, its
    long face lit, running on behind the gate tower."""
    w = MD.wing_rows(yb)
    A0, A1, B0, B1, y0, y1, e, ye, yr, lift = w["A0"], w["A1"], w["B0"], w["B1"], w["y0"], w["y1"], w["e"], w["ye"], w["yr"], w["lift"]
    # its stone platform under it (a band of stone)
    L.poly([fr.p(A0, y0, B0 - 30), fr.p(A1, y0, B0 - 30), fr.p(A1, y0 - 600, B0 - 160), fr.p(A0, y0 - 600, B0 - 160)], STONE_LIT, lerp(STONE_LIT, STONE_SHADE, 0.3))
    pts = [fr.p(A0, y0, B0), fr.p(A1, y0, B0), fr.p(A1, y1, B0), fr.p(A0, y1, B0)]
    L.poly(pts, WALL_LIT, WALL_SUN, g=(pts[0], pts[1]))
    L.glaze([fr.p(A0, y1, B0), fr.p(A1, y1, B0), fr.p(A1, y1 - e * 0.45, B0), fr.p(A0, y1 - e * 0.45, B0)], lerp(np.ones(3, F32), mixp(COBALT, LILAC, 0.5), 0.34))
    n = int((A1 - A0) / 330)
    for j in range(n):                                                          # its windows
        c = A0 + (A1 - A0) * (j + 0.5) / n
        wq = [fr.p(c - 45, y0 + 120, B0 - 4), fr.p(c + 45, y0 + 120, B0 - 4), fr.p(c + 45, y0 + 230, B0 - 4), fr.p(c - 45, y0 + 230, B0 - 4)]
        L.poly(wq, WINDOW)
        for k in (1, 2):
            L.line([fr.p(c - 45 + 30 * k, y0 + 124, B0 - 6), fr.p(c - 45 + 30 * k, y0 + 226, B0 - 6)], lerp(WALL_SHADE, WPAPER, 0.4), 0.5, 0.8)
    L.poly([fr.p(A0, ye + lift * 0.2, B0 - e), fr.p(A1, ye + lift * 0.2, B0 - e), fr.p(A1, y1, B0), fr.p(A0, y1, B0)], lerp(SOFFIT, WALL_BOUNCE, 0.3))
    eave = [fr.p(A0 + (A1 - A0) * t, ye + lift * (abs(2 * t - 1) ** 3.2) * 0.4, B0 - e) for t in np.linspace(0, 1, 16)]
    ridge = [fr.p(A1 - (B1 - B0) * 0.4, yr, (B0 + B1) / 2), fr.p(A0, yr, (B0 + B1) / 2)]
    L.poly(eave + ridge, ROOF_LIT, ROOF_LIT_WARM, g=(eave[0], eave[-1]))
    for t in np.linspace(0.02, 0.98, 60):
        p0 = fr.p(A0 + (A1 - A0) * t, ye + lift * (abs(2 * t - 1) ** 3.2) * 0.4, B0 - e)
        p1 = fr.p(A0 + (A1 - (B1 - B0) * 0.4 - A0) * t, yr, (B0 + B1) / 2)
        L.line([p0, p1], ROOF_SHADE, 0.45, 0.28)
    L.line(ridge, ROOF_DEEP, 1.6)
    L.line([(px, py + 0.8) for px, py in ridge], lerp(WPAPER, NAPLES, 0.1), 0.8)
    L.line(eave, ROOF_DEEP, 1.4)
    L.line([(px, py + 1.0) for px, py in eave], WPAPER, 0.55, 0.8)


def paint_keep(pic, seed):
    """The keep and its corridor turret, through the camera. -> (keep mask, stone base mask, wing mask)."""
    rng = np.random.default_rng(seed)
    fr, yb = MD.keep_frame()
    rows = MD.storey_rows(yb)
    # the corridor turret first: it is behind the keep's right side
    LW = Wet(SHAPE)
    paint_wing(LW, fr, yb, rng)
    cw, aw = LW.done()
    cw = lerp(cw, AIR, 0.22)
    over(pic, cw, aw)
    L = Wet(SHAPE)
    LB = Wet(SHAPE)
    base_stones(LB, fr, yb, rng, "front")
    base_stones(LB, fr, yb, rng, "left")
    near = fr.p(-1230, yb, -1010)                                                  # the base's corner: long and short stones
    cb, ab = LB.done()
    L.add(cb, ab)
    gables = {}
    for g_ in MD.GABLES:
        gables.setdefault(g_[0], []).append(g_)
    for i, d in enumerate(rows):
        wall_face(L, fr, d, "left")
        wall_face(L, fr, d, "front")
        wf, wl = MD.WINDOWS[i]
        windows(L, fr, d, "front", wf, rng)
        windows(L, fr, d, "left", wl, rng)
        eave_shadow(L, fr, d)
        if i > 0:                                                                   # the gables of the roof under this storey stand in front of its foot
            for (k, face, place, w_, h_, kind, up) in gables.get(i - 1, []):
                if kind != "kara":
                    gable(L, fr, rows[i - 1], face, place, w_, h_, kind, up, rng)
        soffit(L, fr, d)
        if d["top"]:
            roof_top(L, fr, d, rng)
        else:
            roof_skirt(L, fr, d, rng)
            for (k, face, place, w_, h_, kind, up) in gables.get(i, []):           # the curved gables sit on this eave itself
                if kind == "kara":
                    gable(L, fr, d, face, place, w_, h_, kind, up, rng)
    c, a = L.done()
    c = lerp(c, AIR, 0.18)                                                          # the evening air: 100 m of it
    over(pic, c, a)
    base_m = ab * (1 - np.clip(a - ab, 0, 1))
    return np.clip(a, 0, 1), np.clip(ab, 0, 1), np.clip(aw, 0, 1)


# ================================================================ the castle hill in front of the keep's foot
def crown(L, rng, cx, top, w, h, tone, lit, dark, tiers=2):
    """A pine's crown on the castle hill, 40 to 80 m off (only its top shows over the wall): flat irregular tiers, dark,
    each lit only along its top toward the low sun on the right; a glimpse of the crooked trunk between them."""
    L.line([(cx, top + h + 4), (cx + rng.normal(0, 3), top + h * 0.72)], lerp(dark, SIENNA, 0.35), max(0.8, w * 0.05), 0.9)
    for j in range(tiers):
        tw = w * (1.15 - 0.30 * j) * rng.uniform(0.85, 1.15)
        ty = top + h * (0.62 - 0.55 * j / max(tiers - 1, 1)) + rng.normal(0, 1.2)
        th = max(3.0, h * rng.uniform(0.20, 0.30))
        ox = cx + rng.normal(0, w * 0.10)
        pts = []
        for k in range(24):
            t = 2 * math.pi * k / 24
            r = 1 + 0.18 * math.sin(4 * t + j * 1.7) + rng.uniform(-0.14, 0.14)
            py_ = math.sin(t)
            pts.append((ox + math.cos(t) * tw / 2 * r, ty + (py_ * th * 0.55 * r if py_ < 0 else py_ * th * 0.30 * r)))
        L.poly(pts, tone, dark, g=((ox, ty - th * 0.5), (ox, ty + th * 0.3)))
        rim = [p_ for p_ in pts if p_[1] < ty - th * 0.15 and p_[0] > ox - tw * 0.15]
        if len(rim) > 2:
            rim.sort(key=lambda q: q[0])
            L.line([(q[0], q[1] + 0.8) for q in rim], lit, max(1.0, th * 0.30), 0.85)


def paint_hill(pic, seed):
    """Below the keep, behind the outer wall: the inner walls on the hill's shoulders, and the castle hill's trees (black
    pines, a few in fresh leaf), low in front of the keep's stone base so that the stones show, higher at the flanks.
    -> its mask."""
    rng = np.random.default_rng(seed)
    L = Wet(SHAPE)
    for (x0, x1, y0, y1) in ((-10, 230, 316, 312), (470, 600, 318, 322), (770, 810, 314, 314)):
        L.poly([(x0, y0 + 14), (x1, y1 + 14), (x1, y1), (x0, y0)], lerp(WALL_LIT, AIR, 0.25), lerp(WALL_SHADE, AIR, 0.25), g=((x0, y0), (x0, y0 + 14)))
        L.poly([(x0, y0 + 1), (x1, y1 + 1), (x1, y1 - 4), (x0, y0 - 4)], lerp(ROOF_SHADE, AIR, 0.20))
        L.line([(x0, y0 - 4), (x1, y1 - 4)], lerp(WPAPER, AIR, 0.3), 0.7, 0.8)
    far_t = (lerp(PINE, AIR, 0.42), lerp(PINE_LIT, AIR, 0.40), lerp(PINE, AIR, 0.30))
    near_t = (PINE, PINE_LIT, lerp(PINE, PRUSSIAN, 0.25))
    spring = (thin(mixp(VERONESE, VIRIDIAN, 0.35), 0.40), lerp(thin(VERONESE, 0.45), NAPLES, 0.25), thin(mixp(VIRIDIAN, VERONESE, 0.4), 0.28))
    # the far row: higher up the hill, paler
    x = -14.0
    while x < 812:
        w = rng.uniform(32, 56)
        in_front_of_base = 240 < x < 474
        top = rng.uniform(330, 338) if in_front_of_base else rng.uniform(296, 314)
        if not (600 < x < 772):
            crown(L, rng, x, top, w, 346 - top, *(spring if rng.random() < 0.10 else far_t), tiers=2 if 346 - top < 30 else 3)
        x += w * rng.uniform(0.55, 0.9)
    # the near row, just behind the outer wall: darker
    x = -10.0
    while x < 812:
        w = rng.uniform(38, 66)
        in_front_of_base = 244 < x < 470
        top = rng.uniform(334, 341) if in_front_of_base else rng.uniform(312, 326)
        if not (600 < x < 772) and rng.random() < (0.45 if in_front_of_base else 0.85):
            crown(L, rng, x, top, w, 352 - top, *(spring if rng.random() < 0.08 else near_t), tiers=2 if w < 40 else 3)
        x += w * rng.uniform(0.6, 1.0)
    L.poly([(-10, 352), (810, 352), (810, 340), (-10, 340)], near_t[2])
    c, a = L.done()
    over(pic, c, a)
    return a


def paint_far(seed=1830):
    info = {}
    pic = paint_sky(seed)
    info["clouds"] = paint_clouds(pic, seed)
    info["sky"] = pic.copy()
    info["hills"] = paint_hills(pic, seed)
    info["town"] = paint_town(pic, seed + 9)
    info["keep"], info["base"], info["wing"] = paint_keep(pic, seed + 11)
    info["hill"] = paint_hill(pic, seed + 13)
    return np.clip(pic, 0, 1).astype(F32), info


if __name__ == "__main__":
    import os
    import time
    from PIL import Image
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    t0 = time.time()
    pic, info = paint_far()
    Image.fromarray((pic * 255).astype(np.uint8)).save("out/edo-castle-far.png")
    print("far", round(time.time() - t0, 1))

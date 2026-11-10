"""PAINT-23 (round twenty-three, DEPTH.md): the FAR plane of Himeji town (edo-town), laid in washes, layer behind layer.

Beyond the walked ground the town is staged again, and the castle brought nearer. From the farthest to the nearest, each
layer paler, plainer and nearer the colour of the sky at the horizon (HORIZON_C: the paper, a breath of blue, the spring
haze warming it a little) than the one in front of it, and none of them with a key line:

    the sky         a graded wash, deep at the top (the eave hides most of it), the haze at the horizon; clouds lifted out
                    of it, larger and rounder high up, small and flat toward the hills (a sky has perspective too)
    the hills       north of the castle, two ridges, the farther the palest, laid wet
    Himeyama        the castle's hill in its spring green, its stone walls and the white walls on them in tiers, two corner
                    turrets, and on its top THE KEEP: PAINT-20D's keep (edo_castle.py: the same five roofs, the same gables, the
                    same tall stone base), larger than before and turned in the world, so that two faces show: the one with
                    its gables toward us and the left (in the sun), its end toward the right (in a soft shade)
    the roofs       the town's roofs, row behind row, climbing toward the hill: tiles, ridges, a storehouse's white gable, a
                    temple's great roof in its grove, the ward's fire tower, the fresh green of spring trees

Nothing here is copied from any print: the castle's shape is PAINT-20D's own; the rest is the scene's.
"""

import math

import numpy as np

from brush import F32, rgb, lerp, blur, grid, noise, curve, step, warp, over, tint, glow, mask_poly, ramp, sample
import sky as skylib
from edo_village_kit import Wet
from edo_town_kit import PAINT, mix, col, SHAPE, W, H, HZ
from edo_town_wc import thin, deepen, WPAPER

C_ = lambda name: col(PAINT[name])
HORIZON_C = lerp(lerp(WPAPER, C_("cerulean"), 0.16), C_("naples"), 0.05).astype(F32)


def air(c, t):
    """A colour seen through `t` of the spring air: toward the sky's colour at the horizon."""
    return lerp(col(c), HORIZON_C, t).astype(F32)


# ---------------------------------------------------------------- the sky
def paint_sky(seed):
    """The graded wash: cobalt toward ultramarine at the top, the haze at the horizon; never even."""
    x, y = grid(SHAPE)
    drift = (noise(SHAPE, (520, 220), seed, 3) - 0.5) * 0.10
    t = np.clip(y / 250.0 + drift, 0, 1)
    pic = ramp(t, [(0.0, thin(mix(PAINT["cobalt"], PAINT["ultra"], 0.30), 0.06)), (0.18, thin(mix(PAINT["cobalt"], PAINT["ultra"], 0.12), 0.12)),
                   (0.40, thin(PAINT["cobalt"], 0.28)), (0.60, thin(mix(PAINT["cobalt"], PAINT["cerulean"], 0.6), 0.46)),
                   (0.78, thin(PAINT["cerulean"], 0.70)), (0.92, HORIZON_C), (1.0, HORIZON_C)])
    pic *= (1 + (noise(SHAPE, (420, 34), seed + 1, 3) - 0.5)[..., None] * 0.06)
    # the sun is high behind us: the paper warms a breath low on the left
    glow(pic, thin(PAINT["naples"], 0.4), (np.clip(1 - x / 520.0, 0, 1) * np.clip(1 - np.abs(y - 190) / 90.0, 0, 1) * 0.10).astype(F32))
    return np.clip(pic, 0, 1).astype(F32)


def paint_clouds(pic, seed):
    """Spring clouds lifted out of the wet wash: bare paper where the sun is on them, a thin lilac-grey under them. Rounder
    and larger high up, small and flat toward the hills. -> their mask (laid wet)."""
    x, y = grid(SHAPE)
    shade = thin(mix(PAINT["cobalt"], PAINT["sienna"], 0.16), 0.62)
    tones = (shade, thin(mix(PAINT["cobalt"], PAINT["sienna"], 0.10), 0.80), WPAPER, WPAPER)
    #         middle x, base row, width, height, billows (clear of the keep's upper storeys: blue sky behind its white)
    masses = [(456, 96, 96, 30, 10), (664, 74, 64, 24, 8), (330, 128, 120, 16, 9),
              (690, 158, 90, 10, 7), (420, 168, 70, 7, 6), (560, 186, 110, 7, 7)]
    thick = skylib.paint_clouds(pic, masses, seed + 5, tones, light=(-0.4, -0.9), ragged=9.0, amount=0.9, reach=24.0)
    n = noise(SHAPE, (300, 9), seed + 7, 3)
    low = step(0.60, 0.88, n) * np.clip(1 - np.abs(y - 176) / 26.0, 0, 1) * 0.42                 # level threads of haze low down
    wisp = blur(low.astype(F32), 1.0)
    over(pic, WPAPER, wisp)
    return np.clip(thick + wisp, 0, 1).astype(F32)


# ---------------------------------------------------------------- the hills behind the castle
def ridge(points, base_row, seed, rough=3.0, cell=40):
    """A ridge as a mask: its crest through `points`, filled down to base_row, the crest a little ragged (trees)."""
    xs = np.arange(-20, 821)
    cx = [p[0] for p in points]
    cy = [p[1] for p in points]
    crest = np.interp(xs, cx, cy)
    n = noise((1, 900), (cell, 1), seed, 3)[0, :len(xs)] - 0.5
    crest = crest + n * rough * 2 + (noise((1, 900), (7, 1), seed + 1, 2)[0, :len(xs)] - 0.5) * rough
    x, y = grid(SHAPE)
    cr = crest[np.clip(x.astype(int) + 20, 0, len(xs) - 1)]
    m = (y >= cr) & (y <= base_row)
    return m.astype(F32), cr


def paint_hills(pic, seed):
    """Two ridges north of the castle, laid wet: the farther all but the sky's colour, the nearer a pale blue-green, each
    darker along its crest and fading into the haze at its foot. -> (mask of both, the nearer's mask)"""
    x, y = grid(SHAPE)
    far_m, far_c = ridge([(-20, 190), (180, 176), (330, 160), (470, 151), (610, 160), (720, 150), (820, 158)], 240, seed + 11, 2.5, 60)
    col_far = air(mix(PAINT["ultra"], PAINT["cerulean"], 0.55), 0.70)
    t = np.clip((y - far_c) / 40.0, 0, 1)
    body = lerp(col_far, air(col_far, 0.55), t[..., None])
    over(pic, body, blur(far_m, 1.2))
    near_m, near_c = ridge([(-20, 205), (200, 192), (300, 178), (400, 172), (520, 184), (650, 170), (760, 176), (820, 186)], 240, seed + 12, 3.0, 34)
    col_near = air(mix(PAINT["viridian"], PAINT["ultra"], 0.42), 0.52)
    t = np.clip((y - near_c) / 34.0, 0, 1)
    body = lerp(col_near, air(col_near, 0.50), t[..., None])
    # its woods: blotches a little darker along the crest
    wood = (noise(SHAPE, (14, 8), seed + 13, 3) - 0.5) * 0.10
    body = body * (1 + wood[..., None] * (1 - t[..., None]))
    over(pic, np.clip(body, 0, 1), blur(near_m, 0.9))
    return np.clip(far_m + near_m, 0, 1).astype(F32), near_m


# ---------------------------------------------------------------- the keep, turned (PAINT-20D's keep: edo_castle.KEEP)
# Each storey of PAINT-20D's drawing (castle picture px): its wall's width and height, its roof's eave width and how far
# the roof climbs to the next wall. Here every storey is a box and every roof a hipped frustum, seen from the south-west:
# the gabled face (the castle scene's front) to the left, in the sun; the end to the right, in a soft shade.
STOREYS = [  # wall w, wall h, roof eave w, roof rise, gable on the front slope, gable on the end slope
    (160, 44, 204, 19, "chidori", None),
    (132, 29, 168, 18, None, "chidori"),
    (108, 26, 140, 16, "chidori", None),
    (84, 24, 112, 14, "kara", None),
    (64, 20, 88, 18, "ridge", "irimoya"),
]
BASE = (168, 228, 66)        # the stone base: its top's width, its foot's width, its height
DEPTH_K = 0.82               # each storey's end is this fraction of its front
KEEP_FOOT = (585.0, 166.0)   # the picture place of the base's near corner, at its foot
KEEP_K = 0.49                # picture px per castle-picture px (round twenty-one's town keep was 0.36)
FRONT = (-0.86, 0.035)       # one unit along the front (to the left), on the picture: across, down
END = (0.50, 0.060)          # one unit along the end (to the right)


def kp(u, v, h):
    """A point of the keep (castle-picture px: u along the front from the near corner, v along the end, h up from the
    base's foot) -> the picture."""
    x0, y0 = KEEP_FOOT
    k = KEEP_K
    return (x0 + k * (u * FRONT[0] + v * END[0]), y0 + k * (u * FRONT[1] + v * END[1] - h))


def sweep_eave(L, u0, u1, v, h, axis, lift, n=16):
    """Points along an eave edge with its corners lifted: along u (axis 'u', at end-coordinate v) or along v."""
    pts = []
    for i in range(n + 1):
        t = i / n
        a = u0 + (u1 - u0) * t
        rise = lift * (abs(2 * t - 1)) ** 3.0
        pts.append(kp(a, v, h + rise) if axis == "u" else kp(v, a, h + rise))
    return pts


def paint_keep(seed):
    """The keep on Layer `Wet`: -> (colour, cover) of the whole keep, and of its lit front face's walls (the lightest)."""
    L = Wet(SHAPE)
    rng = np.random.default_rng(seed)
    a_ = 0.40                                                  # the air between us and the castle
    WHITE_LIT = air(lerp(WPAPER, C_("naples"), 0.05), 0.24)
    WHITE_SH = air(thin(mix(PAINT["lilac"], PAINT["cobalt"], 0.35), 0.52), a_)
    WHITE_UNDER = air(thin(mix(PAINT["lilac"], PAINT["cobalt"], 0.45), 0.40), a_)
    ROOF = air(mix(PAINT["prussian"], "#7a84a0", 0.50), a_ + 0.02)
    ROOF_LIT = air(mix(PAINT["prussian"], "#8a94ae", 0.78), a_)
    ROOF_END = air(mix(PAINT["prussian"], "#6f7890", 0.38), a_ + 0.06)
    STONE_LIT = air(lerp(mix(WPAPER, PAINT["prussian"], 0.24), C_("ochre"), 0.16), a_ + 0.02)
    STONE_SH = air(mix(PAINT["lilac"], PAINT["prussian"], 0.38), a_ + 0.08)
    SLOT = air(mix(PAINT["prussian"], PAINT["sienna"], 0.25), a_ + 0.08)
    # ---- the stone base: its faces flaring out toward the foot (the curve of its slope)
    tw, fw, bh = BASE
    td, fd = tw * DEPTH_K, fw * DEPTH_K
    off_u, off_v = (fw - tw) / 2, (fd - td) / 2
    def base_pt(t, along, on):     # t 0 foot .. 1 top; on 'u' (front) at `along` 0..1, or 'v'
        flare = (1 - t) ** 1.9                                 # the slope steepens toward the top
        pu = -off_u * flare if on == "v" else -off_u * flare + (tw + 2 * off_u * flare) * along
        pv = -off_v * flare if on == "u" else -off_v * flare + (td + 2 * off_v * flare) * along
        return kp(pu, pv, bh * t)
    front_face = [base_pt(t, 0.0, "u") for t in np.linspace(0, 1, 10)] + [base_pt(t, 1.0, "u") for t in np.linspace(1, 0, 10)]
    end_face = [base_pt(t, 0.0, "v") for t in np.linspace(0, 1, 10)] + [base_pt(t, 1.0, "v") for t in np.linspace(1, 0, 10)]
    L.poly(front_face, STONE_LIT, air(STONE_LIT, 0.25), g=(kp(0, 0, bh), kp(0, 0, 0)))
    L.poly(end_face, STONE_SH, air(STONE_SH, 0.22), g=(kp(0, 0, bh), kp(0, 0, 0)))
    for t in np.linspace(0.10, 0.94, 9):                       # the courses, and the joints between the stones
        L.line([base_pt(t, a, "u") for a in np.linspace(0, 1, 8)], air(STONE_SH, 0.15), 0.6, 0.5)
        L.line([base_pt(t, a, "v") for a in np.linspace(0, 1, 6)], air(STONE_SH, -0.1), 0.6, 0.45)
    for j in range(70):
        t = rng.uniform(0.05, 0.95)
        dt = 1.0 / 9
        on = "u" if j % 3 else "v"
        al = rng.random()
        L.line([base_pt(t, al, on), base_pt(min(1, t + dt * 0.9), al, on)], air(STONE_SH, 0.1), 0.5, 0.35)
    # ---- the storeys, from the bottom up: walls, then the roof over them
    h = float(bh)
    lit_mask = Wet(SHAPE)
    for i, (ww, wh, rw, rise, gf, ge) in enumerate(STOREYS):
        wd = ww * DEPTH_K
        u0 = (tw - ww) / 2 if i == 0 else (STOREYS[0][0] - ww) / 2
        u0 = (tw - ww) / 2
        v0 = (td - wd) / 2
        u1, v1 = u0 + ww, v0 + wd
        # the walls: the front (lit, the paper itself) and the end (a soft cool shade)
        fw_ = [kp(u0, v0, h), kp(u1, v0, h), kp(u1, v0, h + wh), kp(u0, v0, h + wh)]
        ew_ = [kp(u0, v0, h), kp(u0, v1, h), kp(u0, v1, h + wh), kp(u0, v0, h + wh)]
        L.poly(fw_, WHITE_LIT, air(WHITE_LIT, 0.10), g=(kp(u0, v0, h + wh), kp(u0, v0, h)))
        lit_mask.poly(fw_, (1.0, 1.0, 1.0))
        L.poly(ew_, WHITE_SH, air(WHITE_SH, 0.10), g=(kp(u0, v0, h + wh), kp(u0, v1, h)))
        # the eaves' shadow across the top of each wall (the sun is high: a deep band)
        sh = 0.42 * wh
        L.glaze([kp(u0, v0, h + wh), kp(u1, v0, h + wh), kp(u1, v0, h + wh - sh * 0.9), kp(u0, v0, h + wh - sh)], air(thin(PAINT["lilac"], 0.25), 0.15), 0.55)
        L.glaze([kp(u0, v0, h + wh), kp(u0, v1, h + wh), kp(u0, v1, h + wh - sh), kp(u0, v0, h + wh - sh)], air(thin(PAINT["cobalt"], 0.30), 0.10), 0.40)
        # window slots: on the front, and on the end
        nwin = 4 - i // 2
        for j in range(nwin):
            uu = u0 + ww * (j + 1) / (nwin + 1)
            wh_ = min(9.0, wh * 0.36)
            L.poly([kp(uu - 4, v0, h + 6), kp(uu + 4, v0, h + 6), kp(uu + 4, v0, h + 6 + wh_), kp(uu - 4, v0, h + 6 + wh_)], SLOT)
        for j in range(max(1, nwin - 1)):
            vv = v0 + wd * (j + 1) / max(2, nwin)
            wh_ = min(9.0, wh * 0.36)
            L.poly([kp(u0, vv - 4, h + 6), kp(u0, vv + 4, h + 6), kp(u0, vv + 4, h + 6 + wh_), kp(u0, vv - 4, h + 6 + wh_)], air(SLOT, 0.12))
        h += wh
        # the roof: a hipped frustum from the eave rectangle (overhang o) up to the next wall's foot (or the ridge)
        o = (rw - ww) / 2
        eu0, eu1, ev0, ev1 = u0 - o, u1 + o, v0 - o * 0.95, v1 + o * 0.95
        top_h = h + rise
        if gf == "ridge":                                      # the top roof: hipped and gabled, its ridge along the front
            nu0, nu1 = u0 + ww * 0.18, u1 - ww * 0.18
            nv0 = nv1 = (v0 + v1) / 2
        else:
            nww = STOREYS[i + 1][0]
            nwd = nww * DEPTH_K
            nu0, nu1 = (tw - nww) / 2 - 1, (tw - nww) / 2 + nww + 1
            nv0, nv1 = (td - nwd) / 2 - 1, (td - nwd) / 2 + nwd + 1
        lift = 3.6 + 0.5 * i
        front_eave = sweep_eave(L, eu0, eu1, ev0, h, "u", lift)
        end_eave = sweep_eave(L, ev0, ev1, eu0, h, "v", lift)
        # the plastered underside of the eaves, seen from below: a pale band under each eave line
        under_f = [(p[0], p[1] + 2.4 * KEEP_K / 0.49) for p in front_eave]
        under_e = [(p[0], p[1] + 2.4 * KEEP_K / 0.49) for p in end_eave]
        L.poly(front_eave + under_f[::-1], WHITE_UNDER)
        L.poly(end_eave + under_e[::-1], air(WHITE_UNDER, 0.05))
        fs = [front_eave[0], front_eave[-1], kp(nu1, nv0, top_h), kp(nu0, nv0, top_h)]
        es = [end_eave[0], end_eave[-1], kp(nu0, nv1, top_h), kp(nu0, nv0, top_h)]
        L.poly(front_eave + [kp(nu1, nv0, top_h), kp(nu0, nv0, top_h)], ROOF_LIT, ROOF, g=(kp(nu0, nv0, top_h), front_eave[len(front_eave) // 2]))
        L.poly(end_eave + [kp(nu0, nv1, top_h), kp(nu0, nv0, top_h)], ROOF_END, air(ROOF_END, 0.12), g=(kp(nu0, nv0, top_h), end_eave[len(end_eave) // 2]))
        # the hip at the near corner, and the eave lines: light where the sun catches the tiles' edges
        L.line([front_eave[0], kp(nu0, nv0, top_h)], air(mix("#8a94ae", WPAPER, 0.4), 0.15), 1.0, 0.8)
        L.line(front_eave, air(mix("#8a94ae", WPAPER, 0.5), 0.2), 0.8, 0.5)
        L.line(end_eave, air(ROOF_LIT, 0.25), 0.7, 0.4)
        if gf == "ridge":
            L.line([kp(nu0, nv0, top_h), kp(nu1, nv0, top_h)], air(WPAPER, 0.2), 1.4, 0.8)
            for uu in (nu0 - 1.5, nu1 + 1.5):                  # the top ridge's two fish, as dabs
                bx, by = kp(uu, nv0, top_h)
                L.poly([(bx - 1.2, by + 0.5), (bx + 1.2, by + 0.5), (bx + 0.9, by - 4.5), (bx - 0.9, by - 4.5)], air(SLOT, 0.05))
                L.ellipse(bx, by - 5.0, 1.4, 1.1, air(SLOT, 0.05))
        # gables: a dormer gable (chidori) on a slope, the curved one (kara) on the front, the hip-and-gable's end at the top
        def chidori(on, centre, wdt, ht):
            if on == "front":
                b0, b1 = kp(centre - wdt, (ev0 + nv0) / 2, h + rise * 0.45), kp(centre + wdt, (ev0 + nv0) / 2, h + rise * 0.45)
                apex = kp(centre, (ev0 + nv0) / 2, h + rise * 0.45 + ht)
                fill, edge = WHITE_LIT, ROOF
            else:
                b0, b1 = kp((eu0 + nu0) / 2, centre - wdt, h + rise * 0.45), kp((eu0 + nu0) / 2, centre + wdt, h + rise * 0.45)
                apex = kp((eu0 + nu0) / 2, centre, h + rise * 0.45 + ht)
                fill, edge = WHITE_SH, ROOF_END
            L.poly([b0, b1, apex], fill)
            L.line([b0, apex, b1], edge, 1.3, 0.9)
            cx_, cy_ = (b0[0] + b1[0] + apex[0]) / 3, (b0[1] + b1[1] + apex[1]) / 3 + 0.5
            L.poly([(cx_ - 1.2, cy_ - 1.2), (cx_ + 1.2, cy_ - 1.2), (cx_ + 1.2, cy_ + 1.4), (cx_ - 1.2, cy_ + 1.4)], SLOT)
        if gf == "chidori":
            chidori("front", u0 + ww * (0.62 if i == 0 else 0.40), 26 if i == 0 else 18, 16 if i == 0 else 11)
        elif gf == "kara":
            cxk = u0 + ww * 0.5
            pts = [kp(cxk + 20 * math.cos(t), ev0 * 0.5 + nv0 * 0.5, h + 2 + 9 * math.sin(t) ** 1.4) for t in np.linspace(0, math.pi, 14)]
            L.poly(pts, WHITE_LIT)
            L.line(pts, ROOF, 1.3, 0.9)
        if ge == "chidori":
            chidori("end", v0 + wd * 0.5, 16, 10)
        elif ge == "irimoya":
            b0, b1 = kp(nu0, nv0 - wd * 0.30, top_h - 7), kp(nu0, nv0 + wd * 0.30, top_h - 7)
            apex = kp(nu0, nv0, top_h + 1)
            L.poly([b0, b1, apex], WHITE_SH)
            L.line([b0, apex, b1], ROOF_END, 1.2, 0.9)
        h = top_h
    c, a = L.done()
    lc, la = lit_mask.done()
    return c, a, la


# ---------------------------------------------------------------- Himeyama and the castle's works on it
def paint_castle_hill(pic, seed):
    """The castle's hill in spring green under the keep, its stone walls in tiers with white walls on them, two corner
    turrets, all in the air. -> (the hill's mask, the walls' mask)"""
    x, y = grid(SHAPE)
    rng = np.random.default_rng(seed)
    kx, ky = KEEP_FOOT
    hill_m, crest = ridge([(330, 230), (420, 206), (480, 186), (530, 174), (600, 170), (660, 176), (720, 190), (790, 206), (840, 222)], 260, seed + 21, 2.4, 22)
    t = np.clip((y - crest) / 50.0, 0, 1)
    green = air(mix(PAINT["veronese"], PAINT["viridian"], 0.45), 0.38)
    green_lo = air(mix(PAINT["viridian"], PAINT["ultra"], 0.25), 0.40)
    body = lerp(green, green_lo, t[..., None])
    trees = noise(SHAPE, (9, 6), seed + 22, 3)
    body = body * (1 + ((trees - 0.5) * 0.22)[..., None])
    lit = step(0.55, 0.75, noise(SHAPE, (7, 5), seed + 23, 2)) * 0.18           # the tops of the crowns in the sun
    body = lerp(body, air(mix(PAINT["veronese"], PAINT["naples"], 0.35), 0.30), lit[..., None])
    over(pic, np.clip(body, 0, 1), blur(hill_m, 0.7))
    # the walls: stone walls (warm pale, their faces sloping) with a white wall on top and its dark coping; in tiers
    L = Wet(SHAPE)
    STONE = air(mix(WPAPER, PAINT["ochre"], 0.20), 0.30)
    STONE_SH = air(mix(PAINT["lilac"], PAINT["prussian"], 0.20), 0.42)
    WHITE = air(WPAPER, 0.10)
    COPE = air(mix(PAINT["prussian"], "#6f7890", 0.45), 0.42)
    # each tier of walls runs in straight lengths that turn at corners (a face toward us lit, a face turned away in shade),
    # with gaps where the hill's trees stand in front of it
    tiers = [  # the corners of the wall's top along the tier (x, row), the stone wall's height, the white wall's height
        ([(470.0, 171.0), (505.0, 168.0), (515.0, 172.0), (612.0, 167.0), (622.0, 171.0), (700.0, 170.0)], 9.0, 3.0),
        ([(416.0, 190.0), (452.0, 186.0), (462.0, 191.0), (560.0, 187.0), (650.0, 189.0), (662.0, 185.0), (762.0, 190.0)], 10.0, 3.5),
        ([(370.0, 208.0), (430.0, 205.0), (444.0, 210.0), (590.0, 206.0), (604.0, 202.0), (700.0, 205.0), (712.0, 209.0), (805.0, 206.0)], 9.0, 3.0),
    ]
    for (corners, sh, wh) in tiers:
        for (xa, ya), (xb, yb) in zip(corners[:-1], corners[1:]):
            turned = (yb - ya) / max(xb - xa, 1.0)
            away = abs(turned) > 0.12                               # a short length turned away from us: in shade
            top = [(xa, ya), (xb, yb)]
            bot = [(xb + 2.0, yb + sh), (xa - 2.0, ya + sh)]
            L.poly(top + bot, STONE_SH if away else STONE, air(STONE_SH if away else STONE, 0.12))
            if not away:
                for k_ in range(int((xb - xa) / 9)):                # the stone wall's courses, faint
                    yy = 0.3 + 0.6 * k_ / max(1, int((xb - xa) / 9))
                L.line([(xa, ya + sh * 0.5), (xb, yb + sh * 0.5)], air(STONE_SH, 0.2), 0.5, 0.3)
            L.poly([(xa, ya - wh), (xb, yb - wh), (xb, yb), (xa, ya)], air(thin(PAINT["lilac"], 0.45), 0.25) if away else WHITE)
            L.line([(xa - 0.5, ya - wh - 0.5), (xb + 0.5, yb - wh - 0.5)], COPE, 1.2, 0.85)
    # two corner turrets on the walls: white two-storey blocks, their roofs grey, the end in a soft shade
    for (tx, ty, s_) in ((440.0, 186.0, 1.0), (726.0, 186.0, 0.9)):
        w_, h1, h2 = 22 * s_, 11 * s_, 8 * s_
        L.poly([(tx - w_ / 2, ty), (tx + w_ / 2, ty), (tx + w_ / 2, ty - h1), (tx - w_ / 2, ty - h1)], WHITE)
        L.poly([(tx + w_ / 2, ty), (tx + w_ / 2 + 6 * s_, ty - 1), (tx + w_ / 2 + 6 * s_, ty - h1 - 1), (tx + w_ / 2, ty - h1)], air(thin(PAINT["lilac"], 0.4), 0.3))
        L.poly([(tx - w_ / 2 - 4, ty - h1), (tx + w_ / 2 + 9 * s_, ty - h1 - 1), (tx + w_ / 2 + 2, ty - h1 - 6 * s_), (tx - w_ / 2 + 4, ty - h1 - 6 * s_)], air(mix(PAINT["prussian"], "#7a84a0", 0.55), 0.38))
        L.poly([(tx - w_ / 3, ty - h1 - 6 * s_), (tx + w_ / 3, ty - h1 - 6 * s_), (tx + w_ / 3, ty - h1 - 6 * s_ - h2), (tx - w_ / 3, ty - h1 - 6 * s_ - h2)], WHITE)
        L.poly([(tx - w_ / 3 - 4, ty - h1 - 6 * s_ - h2), (tx + w_ / 3 + 6, ty - h1 - 6 * s_ - h2), (tx + w_ / 6, ty - h1 - 12 * s_ - h2), (tx - w_ / 6, ty - h1 - 12 * s_ - h2)], air(mix(PAINT["prussian"], "#7a84a0", 0.55), 0.38))
        for j in range(3):
            L.poly([(tx - w_ / 2 + 4 + j * 6, ty - 4), (tx - w_ / 2 + 6 + j * 6, ty - 4), (tx - w_ / 2 + 6 + j * 6, ty - 7), (tx - w_ / 2 + 4 + j * 6, ty - 7)], air(mix(PAINT["prussian"], PAINT["sienna"], 0.3), 0.30))
    # pines on the slopes between the walls: dark dabs, paled by the air
    for i in range(46):
        px_ = rng.uniform(380, 780)
        py_ = float(np.interp(px_, [380, 480, 600, 700, 780], [222, 196, 182, 196, 214])) + rng.uniform(-6, 18)
        r_ = rng.uniform(3.0, 6.0)
        L.ellipse(px_, py_, r_ * 1.4, r_ * 0.7, air(mix(PAINT["viridian"], PAINT["prussian"], 0.40), 0.36), alpha=0.85)
        L.ellipse(px_ - r_ * 0.3, py_ - r_ * 0.3, r_ * 0.9, r_ * 0.35, air(mix(PAINT["veronese"], PAINT["viridian"], 0.4), 0.32), alpha=0.7)
    c, a = L.done()
    over(pic, c, a)
    return hill_m, a


# ---------------------------------------------------------------- the town's roofs, row behind row
def roof_row(L, y_base, h_range, w_range, tone, lit, wall, seed, x0=230.0, x1=820.0, gables=0.25, kura=0.12, trees=0.18, air_t=0.0):
    """One row of the town's roofs: tiled roofs of different heights and widths, side by side and overlapping, now and
    then a gable end turned to us or a storehouse's white gable; spring trees between."""
    rng = np.random.default_rng(seed)
    x = x0 + rng.uniform(-30, 0)
    while x < x1:
        w = rng.uniform(*w_range)
        hgt = rng.uniform(*h_range)
        yb = y_base + rng.uniform(-3, 3)
        r = rng.random()
        if r < trees:                                         # a tree: rounded crowns, fresh green, its shade side bluer
            cx, cy, rr = x + w * 0.5, yb - hgt * 0.7, w * 0.42
            for k_ in range(5):
                ox, oy = rng.normal(0, rr * 0.35), rng.normal(0, rr * 0.25)
                L.ellipse(cx + ox, cy + oy, rr * rng.uniform(0.5, 0.8), rr * rng.uniform(0.4, 0.6), air(mix(PAINT["viridian"], PAINT["veronese"], 0.5), air_t + 0.06),
                          air(mix(PAINT["viridian"], PAINT["ultra"], 0.25), air_t + 0.08))
            L.ellipse(cx - rr * 0.25, cy - rr * 0.25, rr * 0.45, rr * 0.3, air(mix(PAINT["veronese"], PAINT["naples"], 0.4), air_t), alpha=0.6)
        elif r < trees + kura:                                # a storehouse: its white gable end toward us, a dark tiled roof
            L.poly([(x, yb), (x + w, yb), (x + w, yb - hgt * 0.75), (x + w / 2, yb - hgt * 1.25), (x, yb - hgt * 0.75)], wall)
            L.line([(x - 3, yb - hgt * 0.72), (x + w / 2, yb - hgt * 1.28), (x + w + 3, yb - hgt * 0.72)], tone, 2.2, 0.9)
            L.poly([(x + w * 0.42, yb - hgt * 0.55), (x + w * 0.58, yb - hgt * 0.55), (x + w * 0.58, yb - hgt * 0.4), (x + w * 0.42, yb - hgt * 0.4)], air(mix(PAINT["prussian"], PAINT["sienna"], 0.3), air_t + 0.1))
        elif r < trees + kura + gables:                       # a gable end turned toward us
            L.poly([(x, yb), (x + w, yb), (x + w / 2, yb - hgt)], tone, air(tone, 0.10))
            L.poly([(x + w * 0.2, yb), (x + w * 0.8, yb), (x + w / 2, yb - hgt * 0.62)], wall, alpha=0.85)
            L.line([(x, yb), (x + w / 2, yb - hgt), (x + w, yb)], lit, 1.0, 0.7)
        else:                                                 # a roof's long slope toward us, its ridge lit
            sl = rng.uniform(0.15, 0.3) * w
            L.poly([(x, yb), (x + w, yb), (x + w - sl, yb - hgt), (x + sl, yb - hgt)], lit, tone, g=((x, yb - hgt), (x, yb)))
            L.line([(x + sl, yb - hgt), (x + w - sl, yb - hgt)], air(WPAPER, air_t * 0.5 + 0.1), 1.0, 0.75)
            L.line([(x - 2, yb), (x + w + 2, yb)], air(mix(PAINT["prussian"], PAINT["sienna"], 0.2), air_t + 0.1), 1.0, 0.5)
        x += w * rng.uniform(0.55, 1.0)


def paint_roofs(pic, seed):
    """The town between the near row and the castle hill: three rows of roofs climbing toward it, each paler; among them a
    temple's great roof in its grove and the ward's fire tower. -> their mask."""
    L = Wet(SHAPE)
    tile = mix(PAINT["prussian"], "#7a84a0", 0.55)
    tile_lit = mix("#7a84a0", WPAPER, 0.30)
    wall = WPAPER
    for (y_base, hr, wr, a_t, sd) in ((214.0, (10, 16), (26, 52), 0.48, 41), (224.0, (12, 19), (32, 62), 0.36, 42), (238.0, (14, 22), (38, 74), 0.24, 43)):
        roof_row(L, y_base, hr, wr, air(tile, a_t), air(tile_lit, a_t), air(wall, a_t * 0.5), sd, air_t=a_t)
    # the temple's great roof, in its grove, between the castle hill's foot and the near row (at the left of the gap)
    tx, ty = 322.0, 212.0
    for i in range(9):                                        # its grove
        L.ellipse(tx + (i - 4) * 11 + (i % 2) * 4, ty - 14 - (i % 3) * 4, 12, 9, air(mix(PAINT["viridian"], PAINT["prussian"], 0.25), 0.30), air(mix(PAINT["viridian"], PAINT["ultra"], 0.3), 0.34))
    rf = curve([(tx - 46, ty - 16), (tx - 30, ty - 21), (tx - 22, ty - 37), (tx + 22, ty - 37), (tx + 30, ty - 21), (tx + 46, ty - 16)], 10)
    L.poly(rf + [(tx + 42, ty - 10), (tx - 42, ty - 10)], air(mix(PAINT["prussian"], "#8a94ae", 0.62), 0.34), air(tile, 0.36), g=((tx, ty - 37), (tx, ty - 10)))
    L.poly([(tx - 9, ty - 37), (tx + 9, ty - 37), (tx, ty - 46)], air(WPAPER, 0.25))       # the gable of its hip-and-gable roof
    L.line([(tx - 10.5, ty - 36.5), (tx, ty - 46.5), (tx + 10.5, ty - 36.5)], air(tile, 0.30), 1.2, 0.9)
    L.line([(tx - 22, ty - 37), (tx + 22, ty - 37)], air(WPAPER, 0.3), 1.0, 0.8)
    L.line(rf, air(mix("#8a94ae", WPAPER, 0.5), 0.3), 0.8, 0.6)
    # the ward's fire tower: its timbers leaning in, rungs up it, a roofed platform and its bell (no crossed braces)
    fx, fy, fh = 392.0, 205.0, 34.0
    wood = air(mix(PAINT["sienna"], PAINT["prussian"], 0.40), 0.32)
    for (xa, xb) in ((fx - 4.5, fx - 2.4), (fx + 4.5, fx + 2.4)):
        L.line([(xa, fy), (xb, fy - fh)], wood, 1.1, 0.95)
    for k_ in range(1, 7):
        yy = fy - fh * k_ / 7
        L.line([(fx - 4.4 + 2.0 * k_ / 7, yy), (fx + 4.4 - 2.0 * k_ / 7, yy)], wood, 0.5, 0.75)
    L.poly([(fx - 5.5, fy - fh), (fx + 5.5, fy - fh), (fx + 4.5, fy - fh - 2), (fx - 4.5, fy - fh - 2)], wood)
    L.line([(fx - 3.4, fy - fh - 2), (fx - 3.4, fy - fh - 7)], wood, 0.6, 0.9)
    L.line([(fx + 3.4, fy - fh - 2), (fx + 3.4, fy - fh - 7)], wood, 0.6, 0.9)
    L.poly([(fx - 6.5, fy - fh - 7), (fx + 6.5, fy - fh - 7), (fx, fy - fh - 11.5)], air(tile, 0.30))
    L.ellipse(fx, fy - fh - 4.4, 1.2, 1.5, air(mix(PAINT["ochre"], PAINT["sienna"], 0.5), 0.25))
    c, a = L.done()
    over(pic, c, a)
    return a


def paint_haze(pic, seed, near_hills):
    """The spring haze lying across the middle distance, as it does over a town at noon in late April: a soft band over
    the castle hill's foot and the tops of the far roofs (so the hill and its keep rise out of it, the nearer roofs below
    stand clear of it), and a thinner one along the foot of the hills behind. Laid wet. -> its mask."""
    x, y = grid(SHAPE)
    wob = (noise(SHAPE, (180, 30), seed + 51, 3) - 0.5) * 9.0
    band = np.clip(1.0 - np.abs(y + wob - 196.0) / 14.0, 0, 1) ** 1.2
    band *= 0.62 + 0.38 * noise(SHAPE, (140, 20), seed + 52, 3)
    high = np.clip(1.0 - np.abs(y + wob * 0.6 - 186.0) / 7.0, 0, 1) * near_hills * 0.6
    m = np.clip(band * 0.74 + high * 0.5, 0, 1).astype(F32)
    over(pic, lerp(HORIZON_C, WPAPER, 0.4), blur(m, 1.5))
    return m


def paint_far(pic, seed=1830):
    """Everything beyond the near row, far to near, onto the picture. -> dict of masks: sky, clouds, hills, hill (the
    castle's), keep (and keep_lit), roofs."""
    info = {}
    info["clouds"] = paint_clouds(pic, seed)
    info["hills"], info["hills_near"] = paint_hills(pic, seed)
    info["hill"], info["works"] = paint_castle_hill(pic, seed)
    kc, ka, kl = paint_keep(seed)
    over(pic, kc, ka)
    info["keep"], info["keep_lit"] = ka, kl
    info["roofs"] = paint_roofs(pic, seed)
    info["haze"] = paint_haze(pic, seed, info["hills"])
    return info


if __name__ == "__main__":                       # a quick look: python3 edo_town_far.py
    from PIL import Image
    pic = paint_sky(1830)
    info = paint_far(pic)
    Image.fromarray((np.clip(pic, 0, 1) * 255).astype(np.uint8)).save("out/edo-town-work/far-look.png")
    ys, xs = np.where(info["keep"] > 0.5)
    print("keep box", xs.min(), ys.min(), xs.max(), ys.max())

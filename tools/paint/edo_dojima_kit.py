"""PAINT-21C: the kit for Osaka (round twenty-one): the Dojima shore (edo-dojima) and the merchant street (edo-street).

Both are painted in the act's woodblock manner (S/work-20-paintA/style.md: flat masses, a graded sky, one fine prussian
contour, few paints, the blue leading) and keyed in `edo-city` (postimp_paints.py). This file holds what the two share:
the paints by name, a turned camera for the outdoors (room.View, whose numbers are the scene's horizon and full, so the
game's people stand in it at the right size), the two flats of a lit thing and its shade, the contour's weight by depth,
cast shadows along the sun, and the builders of the town: a tiled roof, a townhouse front, a warehouse, a painted
figure far off, writing that is only the shape of writing, and the brushed cut-out.

World measurements are centimetres. Each scene says which way its axes run and where its sun is (`City(sun=...)`).
"""

import math

import numpy as np

from brush import F32, Sheet, blur, curve, grid, lerp, mask_line, mask_poly, noise, over, rgb, strokes, grain, palette_of, to_palette, save
from postimp_paints import PAINTS
from room import View
from edo_village_kit import Paper, bands, flat           # round twenty's sheet that takes thin paint, its graded bands and its flats

W, H = 800, 600
SHAPE = (H, W)


# ---------------------------------------------------------------- the paints, by name (style.md section 2)
def P(name):
    return rgb(PAINTS[name]["hex"])


WHITE, NAPLES, CERULEAN, COBALT, ULTRA, PRUSSIAN = P("lead-white"), P("naples-yellow"), P("cerulean"), P("cobalt-blue"), P("ultramarine"), P("prussian-blue")
OCHRE, SIENNA, VERONESE, VIRIDIAN, LAKE, VERMILION = P("yellow-ochre"), P("burnt-sienna"), P("veronese-green"), P("viridian"), P("geranium-lake"), P("vermilion")
FLESH, FLESH_SH = P("flesh-light"), P("flesh-shadow")


def mixp(a, b, t):
    a = P(a) if isinstance(a, str) else np.asarray(a, dtype=F32)
    b = P(b) if isinstance(b, str) else np.asarray(b, dtype=F32)
    return lerp(a, b, t)


def tintw(c, t):
    """A paint lightened with lead white (a tint)."""
    return lerp(np.asarray(c, dtype=F32), WHITE, t)


def shade(c, t):
    """A paint darkened with prussian blue (never black)."""
    return lerp(np.asarray(c, dtype=F32), PRUSSIAN, t)


def shaded(c, t=0.35):
    """The shade flat of a lit flat: pulled toward the key's shade (cobalt, then ultramarine), not darkened grey."""
    c = np.asarray(c, dtype=F32)
    return lerp(lerp(c, COBALT, t), ULTRA, t * 0.25)


# Osaka in the afternoon, in the act's paints: the paper a little warmer than Suruga's
PAPER = lerp(WHITE, NAPLES, 0.16)                        # the sky at the horizon in the haze
HAZE = lerp(lerp(WHITE, NAPLES, 0.22), CERULEAN, 0.10)   # the warm haze over the water and the roofs
PLASTER_LIT = lerp(WHITE, NAPLES, 0.22)                  # white plaster in the sun
PLASTER_SH = lerp(tintw(COBALT, 0.66), NAPLES, 0.06)     # white plaster in shade: a pale blue, not grey
TILE_LIT = lerp(tintw(PRUSSIAN, 0.50), COBALT, 0.10)     # roof tiles, grey-blue, the slope that takes the light
TILE_SH = lerp(tintw(PRUSSIAN, 0.26), COBALT, 0.14)      # the slope turned from it
TILE_DEEP = shade(TILE_SH, 0.35)
WOOD_LIT = lerp(tintw(OCHRE, 0.12), SIENNA, 0.35)        # timber in the sun: ochre going to burnt sienna
WOOD = lerp(SIENNA, OCHRE, 0.18)
WOOD_SH = lerp(SIENNA, PRUSSIAN, 0.38)
WOOD_DARK = lerp(SIENNA, PRUSSIAN, 0.62)
INDIGO = lerp(ULTRA, PRUSSIAN, 0.38)                     # dyed cloth: the noren, clothes
INDIGO_LIT = lerp(ULTRA, COBALT, 0.45)
STRAW_LIT, STRAW_SH = lerp(tintw(OCHRE, 0.38), NAPLES, 0.2), lerp(OCHRE, SIENNA, 0.45)
EARTH = lerp(lerp(tintw(OCHRE, 0.52), PRUSSIAN, 0.12), NAPLES, 0.10)    # packed earth of the street, warm
STONE_LIT = lerp(tintw(PRUSSIAN, 0.62), OCHRE, 0.16)
STONE_SH = lerp(tintw(PRUSSIAN, 0.40), COBALT, 0.18)


# ---------------------------------------------------------------- the camera and the light
class City:
    """One camera for a whole outdoor scene: room.View (horizon, full, where it stands, how far it is turned), so that
    every row's people are the game's size; and the scene's sun. `sun` is the way toward the sun in the scene's world
    (X, Y up, Z), any length."""

    def __init__(self, horizon, full, cam, yaw, sun, focal=800.0):
        self.v = View(horizon, full, cam, yaw=yaw, focal=focal)
        self.hz, self.full, self.focal = float(horizon), float(full), float(focal)
        s = np.asarray(sun, dtype=F32)
        self.sun = s / np.linalg.norm(s)

    # world -> picture
    def pt(self, X, Y, Z):
        return self.v.pt(X, Y, Z)

    def g(self, X, Z, Y=0.0):
        return self.v.pt(X, Y, Z)

    def poly(self, pts3):
        return self.v.poly(pts3)

    def depth(self, X, Z):
        return self.v.depth(X, Z)

    def k(self, X, Z):
        """Picture pixels per cm at a place on the ground."""
        return self.v.scale_at(X, Z)

    def row(self, X, Z):
        return self.v.pt(X, 0, Z)[1]

    def grownup(self, y):
        """The game's size for a grown-up (175 cm) with feet on row y."""
        return 160.0 * (y - self.hz) / (self.full - self.hz)

    def floor_at(self, x, y):
        return self.v.floor_at(x, y)

    def floor(self, Y=0.0):
        return self.v.floor_xz(SHAPE, Y)

    def depth_map(self, Y=0.0):
        return self.v.depth_map(SHAPE, Y)

    # light
    def lit(self, normal):
        n = np.asarray(normal, dtype=F32)
        n = n / (np.linalg.norm(n) + 1e-6)
        return float(np.dot(n, self.sun))

    def flat_for(self, lit_c, shade_c, normal):
        """Two flats and a hard edge between them (style.md section 5)."""
        return lit_c if self.lit(normal) > 0.25 else shade_c

    def cast(self, X, Y, Z, floor=0.0):
        """Where a point's shadow falls on a level floor (at height `floor`): along the sun."""
        h = max(Y - floor, 0.0)
        return (X - self.sun[0] / self.sun[1] * h, Z - self.sun[2] / self.sun[1] * h)

    def shadow_poly(self, pts3, floor=0.0):
        """World points laid along the sun onto the floor -> picture points."""
        out = []
        for X, Y, Z in pts3:
            cx, cz = self.cast(X, Y, Z, floor)
            out.append(self.pt(cx, floor, cz))
        return out

    # the contour (style.md section 4): 1.0 px near, 0.7 in the middle, 0.5 far; never on the far distance
    def weight(self, d):
        t = np.clip((math.log(30000.0) - math.log(max(d, 300.0))) / (math.log(30000.0) - math.log(900.0)), 0, 1)
        return 0.5 + 0.5 * t, 0.42 + 0.43 * t

    def line(self, sheet, pts, d, warm=False, alpha=None, width=None, color=None):
        w, a = self.weight(d)
        sheet.line(pts, color if color is not None else (SIENNA if warm else PRUSSIAN), width if width else w, alpha if alpha is not None else a)
        return sheet

    def line3(self, sheet, pts3, warm=False, alpha=None, width=None, color=None, close=False):
        """A contour along world points (clipped where it passes behind the lens)."""
        p = list(pts3) + ([pts3[0]] if close else [])
        pp = [self.pt(*q) for q in p]                      # (nothing in these scenes is behind the lens)
        d = min(self.depth(q[0], q[2]) for q in p)
        return self.line(sheet, pp, d, warm, alpha, width, color)

    # boxes: their faces as two flats, then the contour round the silhouette and the corners
    def box(self, sheet, X0, X1, Y0, Y1, Z0, Z1, lit_c, shade_c, top=None, lines=None, warm=False, faces=None):
        """A box standing in the world, each face we can see one flat (lit or shade by the sun). `faces` picks the
        faces to draw (names as room.View: top, bottom, left (-X), right (+X), back (-Z), front (+Z))."""
        out = {}
        for name, pp, n in self.v.box(X0, X1, Y0, Y1, Z0, Z1):
            if faces and name not in faces:
                continue
            c = top if (name == "top" and top is not None) else self.flat_for(lit_c, shade_c, n)
            sheet.poly(pp, c)
            out[name] = pp
        if lines is not None:
            d = self.depth((X0 + X1) / 2, (Z0 + Z1) / 2)
            for name, pp in out.items():
                lines.line(list(pp) + [pp[0]], PRUSSIAN, self.weight(d)[0] * 0.9, self.weight(d)[1] * 0.75)
        return out


# ---------------------------------------------------------------- the town's builders
def tile_rows(sheet, cam, A, B, C, Dp, color, n=None, alpha=0.32, width=0.7):
    """The rows of tiles on a roof slope (quad A-B along the eave, C-Dp along the top): lines running up the slope, as
    the round tiles' ribs, a few pixels apart; drawn texture, never shading (style.md section 5)."""
    pa, pb, pc, pd = [cam.pt(*q) for q in (A, B, C, Dp)]
    length = math.hypot(pb[0] - pa[0], pb[1] - pa[1])
    n = n or max(3, int(length / 5.5))
    for i in range(1, n):
        u = i / n
        p0 = (pa[0] + (pb[0] - pa[0]) * u, pa[1] + (pb[1] - pa[1]) * u)
        p1 = (pd[0] + (pc[0] - pd[0]) * u, pd[1] + (pc[1] - pd[1]) * u)
        sheet.line([p0, p1], color, width, alpha)


def roof_slope(sheet, cam, lines, eave_a, eave_b, ridge_a, ridge_b, lit_c=TILE_LIT, shade_c=TILE_SH, ribs=True, edge=True):
    """One slope of a tiled roof between its eave (two world points) and its ridge (two world points)."""
    n = np.cross(np.subtract(eave_b, eave_a), np.subtract(ridge_a, eave_a))
    if n[1] < 0:
        n = -n
    c = cam.flat_for(lit_c, shade_c, n)
    pts = [eave_a, eave_b, ridge_b, ridge_a]
    pp = cam.poly(pts)
    if len(pp) < 3:
        return None
    sheet.poly(pp, c)
    if ribs:
        tile_rows(sheet, cam, eave_a, eave_b, ridge_b, ridge_a, shade(c, 0.35), alpha=0.35)
    if edge:
        d = cam.depth((eave_a[0] + eave_b[0]) / 2, (eave_a[2] + eave_b[2]) / 2)
        lines.line([cam.pt(*eave_a), cam.pt(*eave_b)], PRUSSIAN, cam.weight(d)[0], cam.weight(d)[1])
        lines.line([cam.pt(*ridge_a), cam.pt(*ridge_b)], PRUSSIAN, cam.weight(d)[0], cam.weight(d)[1])
    return pp


def lattice(sheet, cam, X0, X1, Y0, Y1, Z, color, gap=7.0, bar=3.5, along="X", alpha=1.0):
    """A wooden lattice of upright slats on a face (Z fixed, running along X; or along Z with X fixed)."""
    n = int(abs(X1 - X0) / (gap + bar))
    for i in range(n + 1):
        u = X0 + (X1 - X0) * i / max(n, 1)
        if along == "X":
            pa, pb = cam.pt(u, Y0, Z), cam.pt(u, Y1, Z)
        else:
            pa, pb = cam.pt(Z, Y0, u), cam.pt(Z, Y1, u)
        k = cam.k(u, Z) if along == "X" else cam.k(Z, u)
        sheet.line([pa, pb], color, max(0.6, bar * k), alpha)


def writing(sheet, top, bottom, rng, color, width=0.7, alpha=0.85, cols=1, colw=0.0):
    """The shape of writing down a board: a column of short brush marks and hooks, never a character anyone could read
    (style: the village's board). `top` and `bottom` are the column's ends (picture points)."""
    tx, ty = top
    bx, by = bottom
    for c in range(cols):
        ox = (c - (cols - 1) / 2) * colw
        t = 0.04
        while t < 0.94:
            ln = rng.uniform(0.05, 0.11)
            a = (tx + (bx - tx) * t + ox, ty + (by - ty) * t)
            b_ = (tx + (bx - tx) * min(0.96, t + ln) + ox, ty + (by - ty) * min(0.96, t + ln))
            kind = rng.integers(0, 4)
            h = abs(b_[1] - a[1])
            if kind == 0:                                  # a stroke down
                sheet.line([a, b_], color, width, alpha)
            elif kind == 1:                                # a stroke across and one down
                sheet.line([(a[0] - h * 0.45, a[1] + h * 0.2), (a[0] + h * 0.45, a[1] + h * 0.1)], color, width, alpha)
                sheet.line([(a[0], a[1]), (b_[0], b_[1])], color, width, alpha)
            elif kind == 2:                                # a hook
                sheet.line([(a[0] - h * 0.3, a[1]), (a[0] + h * 0.35, a[1] + h * 0.15), (a[0] - h * 0.1, b_[1])], color, width, alpha)
            else:                                          # two dots and a sweep
                sheet.line([(a[0] - h * 0.35, a[1] + h * 0.1), (a[0] - h * 0.2, a[1] + h * 0.3)], color, width, alpha)
                sheet.line([(a[0] + h * 0.2, a[1]), (a[0] - h * 0.25, b_[1])], color, width, alpha)
            t += ln + rng.uniform(0.03, 0.06)


def figure(sheet, x, y, h, rng, robe=None, sleeves="down", face="S", head_cloth=False, hat=None, load=None, alpha=1.0, line=True,
           jacket=None, tucked=False, woman=False, turn=0.0):
    """A painted figure in a crowd or far off, in the flat manner of the prints (the game draws the people who matter):
    a kimono as one flat with its shade side (the sun is on the right), wide sleeves, a jacket over it if `jacket`, a
    head with the shaved crown and the topknot (or a cloth or a hat; a woman's hair up), feet in sandals. (x, y) is
    the point between the feet, h the height in pixels. `sleeves`: down, up (both hands raised: a dealer calling a
    price), one (one hand raised), bucket (a water man's bucket on his arm), pole (poling a boat). `tucked`: the robe
    tucked up to the thigh, bare legs (a labourer). `turn` -1..1 leans the head and the hands a little that way."""
    robe = robe if robe is not None else [INDIGO, lerp(SIENNA, OCHRE, 0.3), lerp(tintw(PRUSSIAN, 0.45), OCHRE, 0.2), lerp(COBALT, PRUSSIAN, 0.2)][rng.integers(0, 4)]
    sh = shaded(robe, 0.32)
    sw = h * 0.150                                         # half the shoulders' width
    hw = h * 0.118                                         # half the hem's width
    neck_y = y - h * 0.845
    sho_y = neck_y + h * 0.045
    hem_y = y - h * (0.30 if tucked else 0.035)
    lw = 0.5 if not line else max(0.5, min(1.0, h / 110.0))
    # legs (bare when tucked) and sandals
    for dx in (-0.45, 0.45):
        fx = x + dx * hw
        if tucked:
            sheet.line([(fx, hem_y - h * 0.02), (fx + dx * h * 0.01, y - h * 0.02)], FLESH_SH, max(0.8, h * 0.05), alpha)
        sheet.line([(fx - h * 0.025, y), (fx + h * 0.03, y)], lerp(STRAW_SH, PRUSSIAN, 0.3), max(0.7, h * 0.025), alpha)
    # the robe: shoulders to hem, a little wider at the shoulders; its right third turned to the sun... the left in shade
    body = [(x - hw, hem_y), (x + hw, hem_y), (x + sw * 0.95, sho_y + h * 0.04), (x + sw * 0.55, neck_y + h * 0.01), (x - sw * 0.55, neck_y + h * 0.01), (x - sw * 0.95, sho_y + h * 0.04)]
    sheet.poly(body, robe, alpha)
    sheet.poly([(x - hw, hem_y), (x - hw * 0.15, hem_y), (x - sw * 0.10, neck_y + h * 0.02), (x - sw * 0.55, neck_y + h * 0.01), (x - sw * 0.95, sho_y + h * 0.04)], sh, alpha)
    # the collar's V, light
    sheet.line([(x - sw * 0.35, neck_y + h * 0.01), (x + sw * 0.05, sho_y + h * 0.13), (x + sw * 0.40, neck_y + h * 0.01)], lerp(robe, WHITE, 0.55), max(0.6, h * 0.018), alpha)
    if jacket is not None:                                 # a jacket (haori) over the kimono, to the hips
        jy = y - h * 0.44
        jk = [(x - sw * 1.0, jy), (x + sw * 1.0, jy), (x + sw * 0.98, sho_y + h * 0.04), (x + sw * 0.55, neck_y + h * 0.01), (x - sw * 0.55, neck_y + h * 0.01), (x - sw * 0.98, sho_y + h * 0.04)]
        sheet.poly(jk, jacket, alpha)
        sheet.poly([(x - sw * 1.0, jy), (x - sw * 0.2, jy), (x - sw * 0.2, neck_y + h * 0.03), (x - sw * 0.55, neck_y + h * 0.01), (x - sw * 0.98, sho_y + h * 0.04)], shaded(jacket, 0.3), alpha)
        sheet.line([(x, neck_y + h * 0.05), (x, jy)], lerp(jacket, WHITE, 0.35), max(0.5, h * 0.012), alpha)
    else:
        sheet.line([(x - hw * 1.05, y - h * 0.47), (x + hw * 1.05, y - h * 0.47)], shade(robe, 0.55), max(0.7, h * 0.03), alpha)   # the sash
    # the arms: wide sleeves; raised hands show the forearms
    arm_c, arm_sh = (jacket if jacket is not None else robe), shaded(jacket if jacket is not None else robe, 0.3)
    lsx, rsx = x - sw * 0.92, x + sw * 0.92
    def sleeve(sx, side, down=True):
        c = arm_sh if side < 0 else arm_c
        if down:
            sheet.poly([(sx, sho_y + h * 0.02), (sx + side * h * 0.07, sho_y + h * 0.06), (sx + side * h * 0.075, sho_y + h * 0.30), (sx - side * h * 0.02, sho_y + h * 0.30)], c, alpha)
        else:
            sheet.poly([(sx, sho_y + h * 0.01), (sx + side * h * 0.08, sho_y - h * 0.02), (sx + side * h * 0.07, sho_y + h * 0.12), (sx - side * h * 0.01, sho_y + h * 0.10)], c, alpha)
    def raised(sx, side, lean=0.0):
        el = (sx + side * h * 0.08, sho_y - h * 0.03)
        hand = (sx + side * h * (0.04 + lean) + turn * h * 0.04, sho_y - h * (0.24 + 0.03 * rng.random()))
        sheet.line([el, hand], FLESH_SH if side < 0 else FLESH, max(0.9, h * 0.04), alpha)
        sheet.ellipse(hand[0], hand[1], h * 0.024, h * 0.03, FLESH, alpha)
        sleeve(sx, side, down=False)
    if sleeves == "up":
        raised(lsx, -1)
        raised(rsx, 1)
    elif sleeves == "one":
        raised(rsx, 1, 0.02)
        sleeve(lsx, -1)
    elif sleeves == "bucket":
        sleeve(lsx, -1)
        hand = (rsx + h * 0.05, sho_y + h * 0.33)
        sheet.line([(rsx, sho_y + h * 0.03), hand], FLESH, max(0.9, h * 0.045), alpha)
        bw = h * 0.16
        sheet.poly([(hand[0] - bw * 0.5, hand[1]), (hand[0] + bw * 0.5, hand[1]), (hand[0] + bw * 0.42, hand[1] + bw * 0.85), (hand[0] - bw * 0.42, hand[1] + bw * 0.85)], WOOD_LIT, alpha)
        sheet.line([(hand[0] - bw * 0.48, hand[1] + bw * 0.28), (hand[0] + bw * 0.47, hand[1] + bw * 0.28)], WOOD_DARK, max(0.5, bw * 0.1), alpha)
        sheet.ellipse(hand[0], hand[1], bw * 0.5, bw * 0.15, lerp(lerp(VIRIDIAN, OCHRE, 0.4), CERULEAN, 0.3), alpha)
    elif sleeves == "pole":
        top = (x + sw * 3.0, y - h * 1.12)
        bot = (x - sw * 2.0, y + h * 0.35)
        sheet.line([top, bot], WOOD_SH, max(0.7, h * 0.03), alpha)
        sheet.line([(rsx, sho_y + h * 0.02), (x + sw * 1.3, sho_y - h * 0.04)], arm_c, max(0.8, h * 0.06), alpha)
        sheet.line([(lsx, sho_y + h * 0.04), (x + sw * 0.2, sho_y + h * 0.14)], arm_sh, max(0.8, h * 0.06), alpha)
    else:
        sleeve(lsx, -1)
        sleeve(rsx, 1)
    # the head
    hr = h * 0.068
    hx, hy = x + turn * h * 0.01, neck_y - hr * 0.95
    sheet.ellipse(hx, hy, hr * 0.86, hr, FLESH if face == "S" else FLESH_SH, alpha)
    sheet.ellipse(hx - hr * 0.38, hy + hr * 0.1, hr * 0.42, hr * 0.8, FLESH_SH, alpha * 0.8)       # the side away from the sun
    if hat == "sedge":
        sheet.poly([(hx - hr * 2.4, hy - hr * 0.15), (hx + hr * 2.4, hy - hr * 0.15), (hx, hy - hr * 1.8)], STRAW_LIT, alpha)
    elif hat == "deep":                                    # a deep woven hat (costume only)
        sheet.poly([(hx - hr * 1.5, hy + hr * 0.6), (hx + hr * 1.5, hy + hr * 0.6), (hx + hr * 1.2, hy - hr * 1.6), (hx - hr * 1.2, hy - hr * 1.6)], STRAW_SH, alpha)
    elif head_cloth:
        sheet.poly([(hx - hr * 1.0, hy - hr * 0.05), (hx + hr * 1.0, hy - hr * 0.05), (hx + hr * 0.88, hy - hr * 0.95), (hx - hr * 0.88, hy - hr * 0.95)], tintw(CERULEAN, 0.72), alpha)
        sheet.line([(hx + hr * 0.8, hy - hr * 0.4), (hx + hr * 1.4, hy - hr * 0.2)], tintw(CERULEAN, 0.72), max(0.5, hr * 0.25), alpha)
    elif woman:
        sheet.ellipse(hx, hy - hr * 0.55, hr * 1.05, hr * 0.62, PRUSSIAN, alpha)
        sheet.ellipse(hx - hr * 0.1, hy - hr * 1.15, hr * 0.7, hr * 0.42, PRUSSIAN, alpha)
    else:                                                  # the shaved crown, the hair at the sides and back, the topknot
        sheet.poly([(hx - hr * 0.95, hy + hr * 0.15), (hx - hr * 0.85, hy - hr * 0.55), (hx - hr * 0.35, hy - hr * 0.30), (hx - hr * 0.55, hy + hr * 0.25)], PRUSSIAN, alpha)
        sheet.poly([(hx + hr * 0.95, hy + hr * 0.15), (hx + hr * 0.85, hy - hr * 0.55), (hx + hr * 0.45, hy - hr * 0.30), (hx + hr * 0.6, hy + hr * 0.25)], PRUSSIAN, alpha)
        sheet.line([(hx - hr * 0.05, hy - hr * 0.95), (hx + hr * 0.25, hy - hr * 1.05), (hx + hr * 0.15, hy - hr * 0.55)], PRUSSIAN, max(0.7, hr * 0.38), alpha)
    if load == "bale":
        sheet.ellipse(x, neck_y - hr * 2.4, sw * 1.4, hr * 1.2, STRAW_LIT, alpha)
    if line:
        sheet.line(body + [body[0]], PRUSSIAN, lw, 0.45 * alpha)


def brushed(color, alpha, lc, la, under, seed=4, sizes=(6, 3, 2), keep=0.45, fast=False):
    """A cut-out, painted: its flats brushed over the colour it stands in front of, its lines put back on top
    (round twenty's way: edo_village.brushed)."""
    whole = np.maximum(alpha, la)
    ys, xs = np.where(whole > 0.02)
    if len(ys) == 0:
        return color, whole
    y0, y1, x0, x1 = max(ys.min() - 12, 0), min(ys.max() + 13, H), max(xs.min() - 12, 0), min(xs.max() + 13, W)
    flat_ = np.empty((y1 - y0, x1 - x0, 3), dtype=F32)
    flat_[...] = np.asarray(under, dtype=F32)
    over(flat_, color[y0:y1, x0:x1], alpha[y0:y1, x0:x1])
    painted = flat_ if fast else strokes(flat_, sizes=sizes, seed=seed, density=1.8, jitter=0.025, keep=keep)
    over(painted, lc[y0:y1, x0:x1], la[y0:y1, x0:x1])
    out = np.zeros(SHAPE + (3,), dtype=F32)
    out[y0:y1, x0:x1] = painted
    return out, np.clip(whole, 0, 1)


def under_colour(back, alpha, fallback):
    ys, xs = np.where(alpha > 0.5)
    return np.median(back[ys, xs], axis=0) if len(ys) else fallback


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02):
    """Grain, then a limited palette with a fine speckle (the kit's fourth pass); a cut-out keeps its hard edge."""
    import os
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    n = min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0))))
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=n)
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def crop_save(picture, alpha, name, colors=48, pad=2):
    """A small cropped picture of a thing that moves (a frame): -> (its box in the stage, the size)."""
    from PIL import Image
    ys, xs = np.where(alpha > 0.5)
    y0, y1, x0, x1 = max(ys.min() - pad, 0), min(ys.max() + pad + 1, H), max(xs.min() - pad, 0), min(xs.max() + pad + 1, W)
    finish(picture[y0:y1, x0:x1].copy(), name, colors, alpha[y0:y1, x0:x1].copy())
    return [int(x0), int(y0), int(x1 - x0), int(y1 - y0)]


# ---------------------------------------------------------------- layout helpers
def rp(p):
    return [int(round(p[0])), int(round(p[1]))]


def box_of(alpha, pad=0):
    ys, xs = np.where(alpha > 0.5)
    if len(ys) == 0:
        return [0, 0, 0, 0]
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 1 + 2 * pad, int(ys.max() - ys.min()) + 1 + 2 * pad]


def stand(cam, p, face="N"):
    x, y = p
    return {"at": [int(round(x)), int(round(y))], "grownup_px": int(round(cam.grownup(y))), "face": face}


def person_rect(cam, p, cm):
    px_ = cam.grownup(p[1]) * cm / 175.0
    return [int(round(p[0] - px_ * 0.17)), int(round(p[1] - px_)), int(round(px_ * 0.34)), int(round(px_))]

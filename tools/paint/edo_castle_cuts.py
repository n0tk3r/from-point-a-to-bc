"""The castle approach's cut-outs, round twenty-three (DEPTH.md): each painted again in the act's watercolour INSIDE ITS
OLD OUTLINE, so that the scene file's shapes, bases and solid ground hold (DEPTH.md, "What the pilot taught" 6).

The outlines are round twenty's own (edo_castle.cut_layers, unchanged: the town's script imports edo_castle and its keep).
The drawing of the ladder, the scaffold, the tub, the buckets and the cherry is round twenty's too, laid again through
Recolor: the same strokes in the same places, its paints thinned toward the paper as washes are, its key line quieter
(thinner, a little broken, lighter), the cherry's two flat pinks turned into graded washes lit from the low sun.

The gate is painted afresh on round twenty's measurements, with its eaves true: the plastered underside of the tower's
eave seen from below, the eave's shadow across the tower's white walls, the pent roof's shadow on the walls under it,
the posts' sunward edges, the ladder's shadow on the gate's wall. Its outline is the old one with its holes filled:
round twenty's sheet let a half-transparent stroke replace an opaque one, and half the tower's roof, its gable and the
pent roof's right half were see-through. The cross on the gable's round end tile is drawn exactly as before.
"""

import math

import numpy as np

from brush import *
from rome_steps_kit import Canvas
from edo_village_kit import (COBALT, CERULEAN, LAKE, NAPLES, OCHRE, PRUSSIAN, SIENNA, ULTRA, VERONESE, VIRIDIAN, WPAPER, Wet,
                             grade_cut, keyline, mixp, thin)
from edo_village_kit import P as PAINT
import edo_castle as EC
from edo_castle_kit import C, SHAPE, W, H
import depth as D

LILAC = PAINT("lilac")


def key(c):
    c = rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)
    return tuple(int(round(v * 255)) for v in c[:3])


class Recolor:
    """A stand-in for brush.Sheet: round twenty's strokes laid on a watercolour layer (Wet), each paint mapped to a
    thinner one, the keyblock's prussian line made quieter."""

    def __init__(self, L, cmap, line=0.55, line_alpha=0.55, default_thin=0.18):
        self.L, self.cmap, self.line_w, self.line_a, self.dt = L, {key(k): np.asarray(v, F32) for k, v in cmap.items()}, line, line_alpha, default_thin
        self.prussian = key(C["line"])

    def col(self, c):
        k = key(c)
        if k in self.cmap:
            return self.cmap[k]
        c = rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)
        return lerp(c, WPAPER, self.dt).astype(F32)

    def line(self, points, color, width=1.0, alpha=1.0, round_ends=True):
        if key(color) == self.prussian:
            self.L.line(list(points), thin(PRUSSIAN, 0.30), width * self.line_w, alpha * self.line_a)
        else:
            self.L.line(list(points), self.col(color), width, alpha)
        return self

    def taper(self, points, color, w0, w1, alpha=1.0):
        self.L.taper(list(points), self.col(color), w0, w1, alpha=alpha)
        return self

    def poly(self, points, color, alpha=1.0):
        self.L.poly(list(points), self.col(color), alpha=alpha)
        return self

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0):
        self.L.ellipse(cx, cy, rx, ry, self.col(color), alpha=alpha)
        return self

    def clear(self, points):
        self.L.clear(list(points))
        return self


class Solid(Sheet):
    """A sheet that keeps every stroke's cover whole: a half-transparent stroke never thins what is under it (for an
    outline: everything the drawing meant to cover)."""

    @staticmethod
    def _fill(color, alpha=1.0):
        return (255, 255, 255, 255)


def handed(c, a, amount):
    """Round twenty's hand (edo_castle.hand), the same push, on colour and cover together, so that a thing drawn again
    lies exactly where its old outline is."""
    if not amount:
        return c, a
    both = EC.hand(np.dstack([c * a[..., None], a]), amount)
    a2 = np.clip(both[..., 3], 0, 1)
    return (both[..., :3] / np.maximum(a2, 1e-4)[..., None]).astype(F32), a2.astype(F32)


# ---------------------------------------------------------------- the paints
WOOD_LIT = thin(mixp(SIENNA, OCHRE, 0.45), 0.42)
WOOD = thin(mixp(SIENNA, PRUSSIAN, 0.30), 0.22)
WOOD_DARK = thin(mixp(SIENNA, PRUSSIAN, 0.55), 0.10)
BAMBOO = thin(mixp(OCHRE, NAPLES, 0.30), 0.42)
BAMBOO_LIT = lerp(WPAPER, NAPLES, 0.45)
BAMBOO_DARK = thin(mixp(OCHRE, SIENNA, 0.50), 0.24)
ROPE = thin(mixp(SIENNA, OCHRE, 0.35), 0.30)
LIME = lerp(WPAPER, CERULEAN, 0.04)
LIME_SHADE = thin(mixp(COBALT, LILAC, 0.4), 0.70)
TILE = thin(mixp(PRUSSIAN, COBALT, 0.28), 0.42)
TILE_LIT = lerp(TILE, NAPLES, 0.18)
TILE_DEEP = thin(PRUSSIAN, 0.18)
WHITE_LIT = lerp(WPAPER, NAPLES, 0.12)
WHITE_SUN = lerp(WPAPER, mixp(NAPLES, "chrome-orange", 0.25), 0.30)
WHITE_SHADE = thin(mixp(COBALT, LILAC, 0.55), 0.62)
SOFFIT = thin(mixp(LILAC, COBALT, 0.30), 0.70)
COOL = lerp(np.ones(3, F32), mixp(COBALT, LILAC, 0.5), 0.40)               # a shadow's glaze (multiplied)
TRUNK = thin(mixp(SIENNA, PRUSSIAN, 0.52), 0.10)
TRUNK_LIT = thin(mixp(SIENNA, OCHRE, 0.40), 0.30)
BLOOM_SHADE = thin(mixp(LAKE, LILAC, 0.42), 0.36)
BLOOM = lerp(thin(LAKE, 0.52), LILAC, 0.10)
BLOOM_LIT = lerp(WPAPER, LAKE, 0.20)
BLOOM_SUN = lerp(WPAPER, mixp(LAKE, NAPLES, 0.4), 0.14)

SIMPLE_MAP = {
    C["wood"]: WOOD, C["wood_lit"]: WOOD_LIT, C["wood_dark"]: WOOD_DARK, C["bamboo"]: BAMBOO, C["bamboo_lit"]: BAMBOO_LIT,
    C["bamboo_dark"]: BAMBOO_DARK, C["rope"]: ROPE, C["lime"]: LIME, C["lime_shade"]: LIME_SHADE, "#2a2a30": thin(PRUSSIAN, 0.12),
}


def simple_cut(draw, amount, seed):
    """A round-twenty drawing laid again in watercolour: -> (colour, cover) aligned with its old outline."""
    L = Wet(SHAPE)
    draw(Recolor(L, SIMPLE_MAP))
    c, a = L.done()
    c, a = handed(c, a, amount)
    c = grade_cut(c, a, 0.90, lightfrom=(1.0, -0.4), seed=seed, uneven=0.05)      # deeper away from the sun (it is on the right)
    return c


def fill_to(c, a_new, a_old, fallback):
    """Every pixel of the old outline gets a colour (where the new drawing left it thin, the drawing's own colour round
    it, or `fallback`)."""
    have = a_new > 0.15
    if (a_old & ~have).any():
        from scipy import ndimage
        idx = ndimage.distance_transform_edt(~have, return_distances=False, return_indices=True)
        near = c[idx[0], idx[1]]
        c = np.where((a_old & ~have)[..., None], near, c)
    return c


# ---------------------------------------------------------------- the gate
def gate_outline():
    """The gate's old outline with its holes filled: everything round twenty's drawing meant to cover, pushed by the
    same hand, the opening wiped as before."""
    s = Solid(SHAPE, 3)
    EC.gate(s)
    EC.gate_clear(s)
    c, a = s.done()
    _, a = handed(c, a, 0.4)
    o0, o1 = EC.GATE["open"]
    m = mask_poly(SHAPE, [(o0 + 1, EC.GATE["sill"] + 6), (o1 - 1, EC.GATE["sill"] + 6), (o1 - 1, EC.GATE["lintel"] + 1), (o0 + 1, EC.GATE["lintel"] + 1)])
    return (a * (1 - m)) > 0.5


def eave(x0, x1, y, lift=4.0, n=16):
    return EC.eave(x0, x1, y, lift, n)


def gate_paint(seed):
    """The Ni-no-mon, on round twenty's measurements, in watercolour, its eaves true."""
    G = EC.GATE
    x0, x1, sill = G["x0"], G["x1"], G["sill"]
    o0, o1 = G["open"]
    lintel = G["lintel"]
    p0, p1 = G["pent"]
    ux0, ux1, ut, uf = G["upper"]
    rx0, rx1, ey, ry, nx0, nx1 = G["roof"]
    rng = np.random.default_rng(seed)
    L = Wet(SHAPE)
    # the lower storey's white walls either side of the opening: the low sun from the right, fullest at the right
    for (xa, xb) in ((x0 - 4, o0 - 8), (o1 + 8, x1 + 4)):
        L.poly([(xa, sill + 2), (xb, sill + 2), (xb, p1 - 2), (xa, p1 - 2)], WHITE_LIT, WHITE_SUN, g=((x0, 360), (x1, 360)))
    L.poly([(x0 - 4, sill + 2), (x0 + 14, sill + 2), (x0 + 13, p1), (x0 - 4, p1)], WHITE_SHADE, lerp(WHITE_SHADE, WHITE_LIT, 0.5), g=((x0, 360), (x0 + 14, 360)), alpha=0.5)
    for (xa, xb) in ((x0 - 4, o0 - 8), (o1 + 8, x1 + 4)):                    # the plinth of dark boards at the foot
        L.poly([(xa, sill + 2), (xb, sill + 2), (xb, sill - 14), (xa, sill - 14)], WOOD, lerp(WOOD, WOOD_LIT, 0.4), g=((xa, sill), (xb, sill)))
        for k in range(int((xb - xa) / 9)):
            L.line([(xa + 4 + k * 9, sill - 13), (xa + 4 + k * 9, sill)], WOOD_DARK, 0.5, 0.5)
        L.line([(xa, sill - 14), (xb, sill - 14)], WOOD_LIT, 0.9, 0.8)
    # the posts and the lintel round the opening: dark timber, their sunward (right) edges lit
    for (xa, xb) in ((o0 - 8, o0), (o1, o1 + 8)):
        L.poly([(xa, sill + 1), (xb, sill + 1), (xb, lintel - 10), (xa, lintel - 10)], WOOD, WOOD_DARK, g=((xb, 360), (xa, 360)))
        L.line([(xb - 1.2, sill), (xb - 1.2, lintel - 10)], WOOD_LIT, 1.1, 0.75)
    L.poly([(o0 - 14, lintel), (o1 + 14, lintel), (o1 + 14, lintel - 14), (o0 - 14, lintel - 14)], WOOD, lerp(WOOD, WOOD_LIT, 0.5), g=((o0, 0), (o1, 0)))
    L.line([(o0 - 14, lintel - 14), (o1 + 14, lintel - 14)], WOOD_LIT, 1.0, 0.8)
    L.glaze([(o0 - 14, lintel), (o1 + 14, lintel), (o1 + 14, lintel - 4), (o0 - 14, lintel - 4)], COOL)
    for k in range(6):
        sx_ = o0 + 6 + k * (o1 - o0 - 12) / 5
        L.ellipse(sx_, lintel - 7, 1.5, 1.5, thin(PRUSSIAN, 0.1))
        L.ellipse(sx_ + 0.5, lintel - 7.5, 0.6, 0.6, WOOD_LIT)
    # the pent roof across the front: its tiles seen from a little above, the eave's dark tile ends; its shadow on the walls
    ev = eave(x0 - 10, x1 + 10, p1, lift=2.5)
    L.poly([(x0 - 2, p0), (x1 + 2, p0)] + ev[::-1], TILE, TILE_LIT, g=((x0, 290), (x1, 290)))
    for px_ in np.arange(x0 - 6, x1 + 8, 3.0):
        L.line([(px_ + (px_ - 675) * 0.02, p0 + 1), (px_, p1 - 1)], TILE_DEEP, 0.45, 0.35)
    L.line(ev, TILE_DEEP, 1.5)
    L.line([(x0 - 2, p0), (x1 + 2, p0)], lerp(TILE, WPAPER, 0.5), 1.1, 0.9)
    L.glaze([(x0 - 4, p1 + 1), (x1 + 4, p1 + 1), (x1 + 4, p1 + 9), (x0 + 30, p1 + 9), (x0 - 4, p1 + 14)], COOL)       # the pent roof's shadow
    # the tower: white walls set back, its two barred windows; the left end turning from the light
    L.poly([(ux0, uf + 1), (ux1, uf + 1), (ux1, ut), (ux0, ut)], WHITE_LIT, WHITE_SUN, g=((ux0, 250), (ux1, 250)))
    L.poly([(ux0, uf + 1), (ux0 + 20, uf + 1), (ux0 + 19, ut), (ux0, ut)], WHITE_SHADE, lerp(WHITE_SHADE, WHITE_LIT, 0.6), g=((ux0, 250), (ux0 + 20, 250)), alpha=0.55)
    L.line([(ux0, uf), (ux1, uf)], WOOD_DARK, 1.2, 0.7)
    for wx in (628, 722):
        L.poly([(wx - 13, uf - 14), (wx + 13, uf - 14), (wx + 13, uf - 42), (wx - 13, uf - 42)], thin(mixp(PRUSSIAN, SIENNA, 0.2), 0.12), thin(mixp(PRUSSIAN, LILAC, 0.3), 0.22), g=((wx, uf - 42), (wx, uf - 14)))
        for k in range(4):
            bx = wx - 10 + k * 6.5
            L.line([(bx, uf - 14), (bx, uf - 42)], WHITE_SHADE, 1.3, 0.85)
            L.line([(bx + 0.6, uf - 14), (bx + 0.6, uf - 42)], WHITE_LIT, 0.5, 0.8)
        L.line([(wx - 13, uf - 28), (wx + 13, uf - 28)], WHITE_SHADE, 1.0, 0.7)
        L.line([(wx - 14, uf - 13), (wx + 14, uf - 13)], WHITE_SUN, 0.9, 0.9)         # the sill, in the sun
    # the tower's roof: its plastered underside seen from below (the eave is over our eye), the slope, the ridge, the fish
    ev = eave(rx0, rx1, ey, lift=3.5)
    soff = [(p[0], p[1]) for p in ev] + [(ux1, ut + 1), (ux0, ut + 1)]
    L.poly(soff, SOFFIT, lerp(SOFFIT, WHITE_LIT, 0.3), g=((rx0, ey), (rx1, ey)))
    for k in range(18):                                                          # the plastered rafters' rhythm
        t = (k + 0.5) / 18
        pa = (rx0 + (rx1 - rx0) * t, ey + 0.5)
        pb = (ux0 + (ux1 - ux0) * t, ut + 0.5)
        L.line([pa, pb], lerp(SOFFIT, WHITE_SHADE, 0.6), 0.45, 0.5)
    L.glaze([(ux0, ut), (ux1, ut), (ux1, ut + 10), (ux0 + 60, ut + 10), (ux0, ut + 15)], COOL)                 # the eave's shadow on the walls
    L.glaze([(ux0, ut), (ux1, ut), (ux1, ut + 4), (ux0, ut + 5)], COOL)
    roof_poly = [(nx0, ry), (nx1, ry)] + ev[::-1]
    L.poly(roof_poly, TILE, TILE_LIT, g=((rx0, 210), (rx1, 210)))
    L.poly([(nx0 + (nx1 - nx0) * 0.5, ry), (nx1, ry), (rx1, ev[-1][1]), (rx0 + (rx1 - rx0) * 0.55, ey)], lerp(TILE_LIT, WPAPER, 0.25), alpha=0.6)    # the right half in the low sun
    L.glaze([(nx0, ry), (nx0 + (nx1 - nx0) * 0.5, ry), (rx0 + (rx1 - rx0) * 0.55, ey), (rx0, ey)], COOL, 0.5)                                         # the left half turned from it
    for k in range(40):
        t = (k + 0.5) / 40
        pa = (rx0 + (rx1 - rx0) * t, ey - 1)
        pb = (nx0 + (nx1 - nx0) * t, ry + 1)
        L.line([pa, pb], TILE_DEEP, 0.45, 0.32)
    L.line([(nx0, ry), ev[0]], lerp(WPAPER, WHITE_SHADE, 0.3), 1.2)                # the hips, plastered
    L.line([(nx1, ry), ev[-1]], WHITE_SUN, 1.1)
    L.line(ev, TILE_DEEP, 1.7)
    L.line([(p[0], p[1] + 1.4) for p in ev], WHITE_LIT, 0.6, 0.9)
    L.line([(nx0, ry), (nx1, ry)], TILE_DEEP, 2.2)
    L.line([(nx0, ry + 0.9), (nx1, ry + 0.9)], WHITE_SUN, 0.8)
    for ex in (nx0 - 1, nx1 + 1):                                                # the ridge's fish
        L.poly([(ex - 2.2, ry + 1), (ex + 2.2, ry + 1), (ex + 1.6, ry - 8), (ex - 1.6, ry - 8)], TILE_DEEP)
        L.ellipse(ex, ry - 9, 2.4, 1.8, TILE_DEEP)
        L.line([(ex + 1.2, ry), (ex + 1.0, ry - 8)], TILE_LIT, 0.5, 0.8)
    # the gable toward us: white in the sun, its bargeboards, and at its apex the round end tile with the cross (as before)
    ax, ay = EC.GABLE["apex"]
    (b0x, b0y), (b1x, b1y) = EC.GABLE["base"]
    L.poly([(b0x, b0y), (b1x, b1y), (ax, ay)], WHITE_LIT, WHITE_SUN, g=((b0x, b0y), (b1x, b1y)))
    L.glaze([(ax, ay + 2), (ax - 3, ay + 6), (b0x + 6, b0y), (b0x, b0y)], COOL)
    L.line([(b0x - 2, b0y + 1), (ax, ay - 1), (b1x + 2, b1y + 1)], TILE, 2.4)
    L.line([(b0x - 1, b0y + 2.2), (ax, ay + 0.6), (b1x + 1, b1y + 2.2)], WHITE_LIT, 0.6, 0.8)
    # the ladder's shadow on the gate's wall: from where its top rests, spreading to the left as it comes away from the wall
    (lf0, lf1), (lt0, lt1) = EC.LADDER["foot"], EC.LADDER["top"]
    for (ta, fa) in ((lt0, lf0), (lt1, lf1)):
        L.glaze([(ta[0] - 1, ta[1] + 2), (ta[0] + 1, ta[1] + 2), (fa[0] - 22, sill - 1), (fa[0] - 26, sill - 1)], COOL, 0.8)
    # the act's key line, quieter: thin, broken, only on the edges turned from the sun (the left) and along the eaves
    keyline(L, [(x0, sill), (x0, p1 + 2)], row=sill, seed=51)
    keyline(L, [(o0 - 8, sill), (o0 - 8, lintel - 10)], row=sill, seed=52)
    keyline(L, [(o1 + 8, lintel - 10), (o1 + 8, sill)], row=sill, seed=53, weight=0.7)
    keyline(L, [(ux0, ut + 2), (ux0, uf)], row=sill, seed=54)
    keyline(L, eave(x0 - 10, x1 + 10, p1 + 1.5, lift=2.5), row=sill, seed=55, weight=0.8)
    keyline(L, [(p[0], p[1] + 2.4) for p in eave(rx0, rx1, ey, lift=3.5)], row=sill, seed=56, weight=0.8)
    keyline(L, [(nx0, ry), (rx0, ey)], row=sill, seed=57, weight=0.7)
    c, a = L.done()
    # the cross tile, exactly as round twenty drew it (the puzzle's clue: it must read the same)
    s = Sheet(SHAPE)
    tx, ty = EC.GABLE["tile"]
    r = EC.GABLE["r"]
    s.ellipse(tx, ty, r + 1.0, r + 1.0, C["roof_deep"])
    s.ellipse(tx, ty, r, r, "#6f7890")
    s.line([(tx, ty - r * 0.72), (tx, ty + r * 0.72)], "#dfe4ec", 1.0)
    s.line([(tx - r * 0.55, ty - r * 0.15), (tx + r * 0.55, ty - r * 0.15)], "#dfe4ec", 1.0)
    tc, ta = s.done()
    over(c, tc, ta)
    a = np.maximum(a, ta)
    c, a = handed(c, a, 0.4)
    tile_keep = mask_ellipse(SHAPE, tx, ty, r + 3, r + 3, soft=1.0)
    return c, a, tile_keep


# ---------------------------------------------------------------- the cherry
def cherry_paint(seed):
    """Round twenty's double cherry laid again in watercolour: the same limbs, masses, gaps and dabs, the blossom's two
    flats now graded washes (deep rose in the shade under and to the left of each mass, warm white-pink where the low sun
    from the right falls), the trunk warm and dark with its sunward edge lit."""
    shade_, lit_ = EC.mix(EC.PAPER, "#c9375e", 0.46), EC.mix(EC.PAPER, "#c9375e", 0.24)
    deep = EC.mix(shade_, "#c9375e", 0.25)
    cmap = {C["trunk"]: TRUNK, C["trunk_lit"]: TRUNK_LIT, "#2a1e22": thin(mixp(PRUSSIAN, SIENNA, 0.4), 0.06), "#3a3034": thin(mixp(PRUSSIAN, SIENNA, 0.4), 0.10),
            "#8c3b20": thin(SIENNA, 0.25), tuple(shade_): BLOOM, tuple(lit_): BLOOM_LIT, tuple(deep): BLOOM_SHADE}
    L = Wet(SHAPE)

    def draw(s):
        EC.cherry(s)
        EC.cherry_contour(s)
    R = Recolor(L, {})
    R.cmap = {key(k): np.asarray(v, F32) for k, v in cmap.items()}
    draw(R)
    c, a = L.done()
    c, a = handed(c, a, 0.6)
    # light the masses: each one's lower left in its own shade, its upper right in the sun
    x, y = grid(SHAPE)
    lightm = np.zeros(SHAPE, F32)
    shadem = np.zeros(SHAPE, F32)
    for (cx, cy, rx, ry) in EC.MASSES:
        d = ((x - cx) / (rx + 2)) ** 2 + ((y - cy) / (ry + 2)) ** 2
        inside = np.clip((1.15 - d) * 3, 0, 1)
        u = ((x - cx) * 0.8 / rx - (y - cy) * 0.6 / ry)                         # toward the sun: right and a little up
        np.maximum(lightm, inside * np.clip(u * 1.1 + 0.15, 0, 1), out=lightm)
        np.maximum(shadem, inside * np.clip(-u * 0.9 - 0.05, 0, 1) * np.clip(d * 1.2, 0, 1), out=shadem)
    pink = np.clip((c[..., 0] - c[..., 2]) * 4, 0, 1) * (c[..., 0] > 0.55)
    c = lerp(c, BLOOM_SUN[None, None, :] * np.ones_like(c), (lightm * pink * 0.72)[..., None])
    c = lerp(c, c * thin(mixp(LAKE, ULTRA, 0.45), 0.42), (shadem * pink * 0.80)[..., None])
    # the trunk: cherry bark, dark and warm, ringed with pale bands; its left side deeper, its sunward edge lit
    T = Wet(SHAPE)
    trunk = [(74, 548), (104, 546), (106, 500), (108, 460), (100, 440), (84, 440), (78, 480), (72, 520)]
    T.poly(trunk, thin(mixp(SIENNA, PRUSSIAN, 0.45), 0.16), thin(mixp(SIENNA, PRUSSIAN, 0.62), 0.06), g=((104, 500), (76, 500)))
    rng = np.random.default_rng(seed + 3)
    for yy in np.arange(446, 544, 5.0):                                           # the lenticels: short pale dashes across the bark
        w0 = np.interp(yy, [440, 460, 500, 546], [84, 78, 74, 74])
        w1 = np.interp(yy, [440, 460, 500, 546], [100, 108, 106, 104])
        for k in range(int(rng.integers(1, 3))):
            xa_ = rng.uniform(w0 + 2, w1 - 8)
            ln = rng.uniform(3, 9)
            T.line([(xa_, yy + rng.uniform(-1, 1)), (xa_ + ln, yy + rng.uniform(-1, 1) - 0.4)], thin(mixp(LILAC, SIENNA, 0.3), 0.45), rng.uniform(0.7, 1.2), 0.55)
    T.poly([(97, 546), (104, 546), (106, 500), (108, 460), (101, 442), (99, 470), (100, 510)], thin(mixp(SIENNA, OCHRE, 0.5), 0.38), alpha=0.85)   # the lit side
    T.line([(103.5, 546), (105.5, 500), (107.4, 462)], lerp(WPAPER, mixp(NAPLES, "chrome-orange", 0.3), 0.35), 1.0, 0.9)
    T.poly([(60, 551), (74, 544), (88, 546), (110, 545), (122, 551)], thin(mixp(SIENNA, PRUSSIAN, 0.45), 0.2), alpha=0.9)       # its foot's flare
    tc, ta = T.done()
    tc, ta = handed(tc, ta, 0.6)
    m = np.clip(ta, 0, 1) * (a > 0.5)
    c = lerp(c, tc, m[..., None])
    return c


# ---------------------------------------------------------------- all of them
def cut_layers(pic, info, fast=False):
    """-> {name: (colour, cover)} for every round-twenty cut-out, in its old outline."""
    old = EC.cut_layers()
    out = {}
    for name, draw, amount in (("ladder", EC.ladder, 0.3), ("scaffold", EC.scaffold, 0.3), ("tub", EC.tub, 0.2)):
        a_old = old[name].a > 0.5
        c = simple_cut(draw, amount, seed=len(name))
        L_ = Wet(SHAPE)
        draw(Recolor(L_, SIMPLE_MAP))
        _, a_new = handed(*L_.done(), amount)
        c = fill_to(c, a_new, a_old, WOOD)
        out[name] = (c.astype(F32), a_old.astype(F32))
    for i, b in enumerate(EC.BUCKETS):
        name = f"bucket-{i + 1}"
        a_old = old[name].a > 0.5
        dr = lambda s, b=b: EC.bucket(s, b)
        c = simple_cut(dr, 0.2, seed=20 + i)
        L_ = Wet(SHAPE)
        dr(Recolor(L_, SIMPLE_MAP))
        _, a_new = handed(*L_.done(), 0.2)
        c = fill_to(c, a_new, a_old, WOOD)
        out[name] = (c.astype(F32), a_old.astype(F32))
    gc, ga, tile_keep = gate_paint(31)
    g_out = gate_outline()
    gc = fill_to(gc, ga, g_out, WHITE_LIT)
    out["gate"] = (gc.astype(F32), g_out.astype(F32))
    info["tile_keep"] = tile_keep
    a_old = old["cherry"].a > 0.5
    cc = cherry_paint(41)
    Lc = Wet(SHAPE)

    def drawc(s):
        EC.cherry(s)
        EC.cherry_contour(s)
    drawc(Recolor(Lc, {}))
    _, ac = handed(*Lc.done(), 0.6)
    cc = fill_to(cc, ac, a_old, BLOOM)
    out["cherry"] = (cc.astype(F32), a_old.astype(F32))
    return out

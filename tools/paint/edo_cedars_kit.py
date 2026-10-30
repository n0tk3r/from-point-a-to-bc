"""PAINT-20C: the cedar path's measurements and small tools (shared by edo_cedars.py, its layout and its check).

The hills north of Osaka, about 24 April 1830, dusk, in fine steady spring rain. The picture is composed in its own
pixels (as the Tiber's far bank is), with the land camera's rule for sizes: a grown-up is 160 px tall with feet on
row FULL and nothing at row HZ; the path climbs the slope away from us, so people get smaller as they go up.

LIGHT. Dusk under rain: little light, all of it cool and soft, from the sky above (no sun, no shadows but a soft
darkening under things). The one warm thing is the storehouse's lamp: a thin line of it under the floor (a cut-out
with states; the game shows it or not), and nothing else.

THE PLACE. Stone steps climb from the foot of the picture, narrowing, to a charcoal-burner's storehouse at the top
of the slope (dark boards, a thatched roof, a lean-to on its left, its front door facing down the path, a small high
square window in its right end wall, the back of the house); beside it on the right an earth charcoal kiln, cold;
a bamboo pipe out of the hillside behind it. A small stone figure by the path on the left, worn, with a scrap of red
cloth. Cedar trunks on both sides in a rhythm of verticals, their crowns lost above the frame, mist between them."""

import math

import numpy as np

from brush import F32, Sheet, rgb, lerp, mask_poly, mask_ellipse, mask_line, noise, blur, over, tint, glow, step, grid, curve
from PIL import Image, ImageDraw

W, H = 800, 600
SHAPE = (H, W)
HZ, FULL = 250, 600
ID = "edo-cedars"
PX, PY = grid(SHAPE)


def k_at(y):
    """The game's size at a row: 1 on FULL, 0 on HZ (a grown-up is 160 * k px tall)."""
    return (np.asarray(y, F32) - HZ) / float(FULL - HZ)


def cm(y):
    """Picture pixels per centimetre for a thing standing on row y."""
    return 160.0 / 175.0 * k_at(y)


def grownup_px(y):
    return float(160.0 * k_at(y))


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, F32)


def mix(a, b, t):
    return lerp(col(a), col(b), t)


class Paper(Sheet):
    """A Sheet whose half-transparent strokes glaze over earlier ones instead of replacing them (as highway_kit.Paper)."""

    def _glaze(self, box, draw):
        w, h = self.im.size
        x0, y0 = max(int(box[0]) - 2, 0), max(int(box[1]) - 2, 0)
        x1, y1 = min(int(box[2]) + 3, w), min(int(box[3]) + 3, h)
        if x1 <= x0 or y1 <= y0:
            return self
        tmp = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        draw(ImageDraw.Draw(tmp), x0, y0)
        self.im.alpha_composite(tmp, (x0, y0))
        return self

    def poly(self, points, color, alpha=1.0):
        if alpha >= 0.999:
            return super().poly(points, color, alpha)
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        fill = self._fill(color, alpha)
        box = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
        return self._glaze(box, lambda d, ox, oy: d.polygon([(px - ox, py - oy) for px, py in pts], fill=fill))

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0):
        if alpha >= 0.999:
            return super().ellipse(cx, cy, rx, ry, color, alpha)
        s = self.ss
        fill = self._fill(color, alpha)
        box = ((cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s)
        return self._glaze(box, lambda d, ox, oy: d.ellipse([box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy], fill=fill))

    def line(self, points, color, width=1.0, alpha=1.0, round_ends=True):
        if alpha >= 0.999:
            return super().line(points, color, width, alpha, round_ends)
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        wd = max(1, int(round(width * s)))
        fill = self._fill(color, alpha)
        box = (min(p[0] for p in pts) - wd, min(p[1] for p in pts) - wd, max(p[0] for p in pts) + wd, max(p[1] for p in pts) + wd)

        def draw(d, ox, oy):
            q = [(px - ox, py - oy) for px, py in pts]
            d.line(q, fill=fill, width=wd, joint="curve")
            if round_ends and wd > 2:
                r = wd / 2
                for px, py in (q[0], q[-1]):
                    d.ellipse([px - r, py - r, px + r, py + r], fill=fill)
        return self._glaze(box, draw)


# ---------------------------------------------------------------- the path and the house, in picture pixels
# The steps' centre line, from the foot of the picture up to the storehouse's door: (x, y) pairs, bottom first.
PATH = [(400, 606), (412, 560), (424, 520), (432, 488), (436, 462), (434, 444), (428, 432)]
# Half the path's width at a row (it narrows as it climbs, in proportion to the size there)
def half_width(y):
    return 92.0 * k_at(y) + 18.0


def path_x(y):
    xs = [p[0] for p in PATH][::-1]
    ys = [p[1] for p in PATH][::-1]
    return float(np.interp(y, ys, xs))


# The storehouse: a box seen three-quarters on, its front wall facing down the path (toward us and a little left), its
# right end wall receding. Picture points of its footprint: front-left, front-right, back-right (the back-left is hidden).
HOUSE = {
    "fl": (318, 436), "fr": (486, 430), "br": (552, 406),
    "wall_h": 108,          # the eaves' height above the front sill at the front-left corner, px (about 2.4 m at this depth)
    "ridge_h": 174,         # the ridge above the front sill
    "floor_gap": 9,         # the floor stands this high over the ground on its posts: the line of light shows here
    "door": (384, 428),     # door: x0, x1 along the front wall (base on the sill's line)
    "window": (514, 532, 344, 362),   # the small high square window in the right end wall: x0, x1, y0, y1
}
LEANTO = {"x0": 250, "x1": 318, "post_y": 450, "roof_y": 380, "wall_y": 370}
KILN = {"cx": 606, "cy": 420, "rx": 48, "ry": 30}                    # the earth kiln: a dome right of the house
PIPE = {"from": (640, 372), "to": (664, 360), "mouth": (666, 359)}      # the bamboo pipe out of the hillside
FIGURE = {"x": 286, "base": 526, "h": 42}                              # the stone figure by the path, 42 px (about 60 cm there)
MARKS = {"enter": (400, 580), "figure": (340, 540), "pipe": (612, 452), "door": (404, 444), "window": (536, 444),
         "isukeFrom": (340, 596)}
# the constable's way up the path (points, bottom first), ending at the door
ISUKE_WAY = [(340, 596), (360, 566), (388, 528), (410, 492), (420, 464), (410, 448), (404, 444)]

# The near cedars: (x of the trunk's middle at its base, base row, half width at the base) left and right of the path,
# back to front. The two nearest stand at the picture's edges and are the front plane.
TRUNKS_L = [(284, 452, 9), (250, 468, 11), (208, 492, 14), (160, 524, 18), (104, 566, 24)]
TRUNKS_R = [(578, 452, 9), (612, 470, 11), (650, 494, 14), (696, 526, 19), (742, 564, 24)]
FRONT_L = (36, 640, 44)
FRONT_R = (776, 648, 46)
# far trunks in the mist behind the house and up the slope: (x, base row, half width)
TRUNKS_FAR = [(300, 404, 5), (338, 396, 5), (372, 392, 4), (570, 388, 5), (604, 392, 5), (640, 400, 6), (690, 410, 6),
              (262, 416, 6), (236, 426, 7), (720, 428, 7), (760, 446, 8), (460, 384, 4), (500, 386, 4), (430, 380, 3)]
# The crowns that close the top of the picture: (middle x, middle y, radius) of each lobed mass, by plane. The near
# trunks' own crowns are above the frame; what hangs in at the top are the undersides of the middle and far crowns and,
# at the two top corners, the near plane's lowest boughs.
CROWNS_NEAR = [(36, -14, 130), (776, -10, 132), (120, -40, 96), (700, -36, 96)]
CROWNS_MID = [(104, -30, 104), (160, 0, 88), (208, 30, 76), (250, 60, 66), (284, 90, 56), (742, -28, 104), (696, 4, 88), (650, 34, 76), (612, 64, 66), (578, 94, 56)]
CROWNS_FAR = [(300, 120, 56), (338, 140, 48), (372, 158, 44), (430, 170, 40), (460, 164, 38), (500, 156, 40), (570, 140, 50), (604, 150, 46), (640, 128, 54), (690, 116, 56),
              (236, 150, 50), (262, 176, 42), (720, 146, 52), (760, 172, 44), (400, 96, 44), (520, 100, 44)]

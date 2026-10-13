"""The sun shade from the store's window, held up (NEVADA-12A, round twelve): shade-held.png, an alt of the roadside.

The folding windshield shade that stood DISPLAY ONLY in the store's window for forty summers, held up by Grandpa Joe
standing at the coin-holder's place (572, 560) and facing east: the panel is in his hands in front of him, turned
toward the sun (low on the right, behind our right shoulder) and toward the place that hums (646, 483). What we see
is its BACK, the side that faced out of the window: the silver gone to a pale chalky grey, matte and patchy, with the
pattern of its folds still in it. The low sun rakes across it from the right, so the leaves of the accordion that
turn that way are a warm pale grey and the others a cool one. Along its top edge a sliver of the bright side shows,
where the top of the panel leans toward us as it tilts, and the sun flashes on it.

He holds it by its near edge, the end by his body: his right hand (his right side is toward us) at its lower corner,
HANDS["R"], and his left at its upper corner, HANDS["L"], higher. PEOPLE-12 puts his hands there. The panel's edge
passes two or three pixels beyond each hand point, so his fingers show round it.

The panel is a windshield shade, 140 by 70 cm: 115 by 58 px face-on at his row. It is tilted back a little and turned
toward the east, so it is drawn in perspective: the near edge 46 px tall, the far end smaller (41) and higher, and the
leaves closing up toward it. It clears the notice on the fence (x 630 to 695, bottom edge y 402 to 405) by five pixels
and the place that hums by eight.

    python3 nevada_roadside_held.py     paints out/nevada-roadside-held-try.png (the shade over the finished picture) to look at
"""

import math

import numpy as np

from brush import *
from nevada_roadside_kit import Paper, brushed

HANDS = {"R": (598, 482), "L": (602, 437)}                  # his hands, in picture pixels: near lower corner, near upper corner
BL, TL = (600.5, 482.5), (604.5, 436.5)                     # the panel's near edge (by his hands): bottom, top
BR, TR = (710.0, 452.0), (712.5, 411.0)                     # its far end: bottom, top
FOLDS = 12                                                  # the accordion: twelve leaves
DIP = 2.0                                                   # a ridge toward us sits this much lower in the picture than a valley
LIP = 3.2                                                   # the sliver of the bright side along the top


def _t(s):
    """Where a point s of the way along the panel (0 at his hands, 1 at the far end) is drawn: closer together toward the
    far end, as a thing turned away from us is (the ends' heights give the depth ratio)."""
    hn, hf = BL[1] - TL[1], BR[1] - TR[1]
    return s * hf / ((1 - s) * hn + s * hf)


def panel_at(s, b, i=None):
    """A point on the panel: s along it (0 at his hands, 1 at the far end), b up it (0 the bottom edge, 1 the top);
    `i` the crease it is on, for the zigzag of the edges."""
    t = _t(s)
    bot = (BL[0] + (BR[0] - BL[0]) * t, BL[1] + (BR[1] - BL[1]) * t)
    top = (TL[0] + (TR[0] - TL[0]) * t, TL[1] + (TR[1] - TL[1]) * t)
    x, y = bot[0] + (top[0] - bot[0]) * b, bot[1] + (top[1] - bot[1]) * b
    if i is not None:
        y += DIP * (1 if i % 2 else -1) * (0.75 + 0.25 * (1 - abs(2 * b - 1))) * (1 - 0.15 * t)
    return (x, y)


def shade_held_sheets(shape, seed=62):
    """-> (base, lines): the panel's flat paint; its crisp edges, creases, flashes, a price sticker, the elastic loop."""
    rng = np.random.default_rng(seed)
    base, lines = Paper(shape), Paper(shape)
    n = FOLDS
    under = [panel_at(i / n, 0, i) for i in range(n + 1)]
    top = [panel_at(i / n, 1, i) for i in range(n + 1)]
    lip = [(x - 0.8, y - LIP) for x, y in top]
    base.poly([(px, py + 2.6) for px, py in under] + under[::-1], "#5a5c68")             # the pleats' thickness along the bottom
    for i in range(n):
        quad = [panel_at(i / n, 0, i), panel_at((i + 1) / n, 0, i + 1), panel_at((i + 1) / n, 1, i + 1), panel_at(i / n, 1, i)]
        sunward = i % 2 == 1                                                 # this leaf turns toward the low sun on the right
        base.poly(quad, ("#d8d4cb", "#d4d1ca", "#dbd6cc")[i % 3] if sunward else ("#aeb0b9", "#a9acb6", "#b3b4bb")[i % 3])
        for k in range(3):                                                   # chalky: matte, in level streaks where the window's sun lay
            b0 = rng.uniform(0.04, 0.84)
            b1 = min(0.98, b0 + rng.uniform(0.07, 0.2))
            streak = [panel_at(i / n + 0.012, b0, i), panel_at((i + 1) / n - 0.012, b0, i + 1), panel_at((i + 1) / n - 0.012, b1, i + 1), panel_at(i / n + 0.012, b1, i)]
            base.poly(streak, ("#e6e1d6" if sunward else "#bfc0c6") if rng.random() < 0.55 else ("#c8c4bc" if sunward else "#9ea1ac"), rng.uniform(0.25, 0.45))
        base.poly([quad[0], quad[1], panel_at((i + 1) / n, 0.38, i + 1), panel_at(i / n, 0.38, i)], "#cdb9a2", 0.28)    # the lot's warmth, thrown up into its lower part
        base.poly([quad[3], quad[2], lip[i + 1], lip[i]], "#f6f9fd" if sunward else "#d2dbe6")                         # the sliver of the bright side
    for i in range(1, n):                                                    # the creases, faint: a valley a shade darker, a ridge a shade lighter
        a, b = panel_at(i / n, 0, i), panel_at(i / n, 1, i)
        lines.line([a, b], "#8e919c" if i % 2 else "#eeebe4", 0.8, 0.55 if i % 2 else 0.45)
    lines.line(lip, "#ffffff", 0.9, 0.95)                                    # the bright edge, and where the sun flashes on it
    for i in (3, 7, 10):
        c = lip[i]
        lines.line([(c[0] - 3.4, c[1]), (c[0] + 3.4, c[1])], "#ffffff", 0.9)
        lines.line([(c[0], c[1] - 3.0), (c[0], c[1] + 3.0)], "#ffffff", 0.9)
        lines.ellipse(c[0], c[1], 1.2, 1.2, "#ffffff")
    lines.line(top, "#8a8e9a", 0.8, 0.7)                                     # where the bright side turns over into the back
    lines.line([(px, py + 2.6) for px, py in under], "#343744", 1.0, 0.9)    # the binding along the bottom
    lines.line(under, "#80838e", 0.7, 0.5)
    lines.line([under[0], lip[0]], "#3c4050", 1.4, 0.95)                     # the bound ends
    lines.line([under[-1], lip[-1]], "#3c4050", 1.3, 0.95)
    s0 = panel_at(0.78, 0.18)                                                # the store's price sticker, never taken off
    lines.poly([(s0[0], s0[1]), (s0[0] + 8.0, s0[1] - 1.6), (s0[0] + 8.4, s0[1] - 6.6), (s0[0] + 0.4, s0[1] - 5.0)], "#ece4c2", 0.95)
    lines.line([(s0[0] + 1.8, s0[1] - 2.8), (s0[0] + 6.4, s0[1] - 3.8)], "#a2483a", 1.0, 0.85)
    e, u = lip[-1], under[-1]                                                # the elastic loop that holds it shut, hanging off the far end
    lines.line([(e[0] + 0.5, e[1] + 1.5), (e[0] + 5.0, e[1] + 9.0), (e[0] + 2.5, e[1] + 17.0), (u[0] + 0.5, u[1] - 4.0)], "#1e2230", 1.1, 0.95)
    return base, lines


def shade_held(back, fast=False):
    """The alt, painted over the finished backdrop: -> (color, alpha), the size of the picture, hard-edged."""
    base, lines = shade_held_sheets(back.shape[:2])
    c, a = base.done()
    lc, la = lines.done()
    return brushed(c, a, lc, la, "#b4b2b2", seed=17, sizes=(4, 2), keep=0.55, fast=fast)


def box_of(alpha, pad=0):
    ys, xs = np.where(alpha > 0.5)
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 1 + 2 * pad, int(ys.max() - ys.min()) + 1 + 2 * pad]


def clearances(alpha):
    """How far the panel keeps from the notice's bottom edge and from the place that hums (pixels): both must be > 0."""
    ys = np.where(alpha[:, 630:696] > 0.5)
    notice = min(int(ys[0][ys[1] == j].min()) - (402 + 3 * j / 65.0) for j in range(66) if (ys[1] == j).any())
    col = np.where(alpha[:, 646] > 0.5)[0]
    return round(float(notice), 1), int(483 - col.max())


if __name__ == "__main__":
    from PIL import Image
    back = np.asarray(Image.open("out/nevada-roadside-comp.png").convert("RGB"), dtype=F32) / 255
    c, a = shade_held(back)
    whole = back.copy()
    over(whole, c, (a > 0.5).astype(F32))
    Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save("out/nevada-roadside-held-try.png")
    print("shade-held box", box_of(a), "hands", HANDS, "clear of the notice, of the hum", clearances(a))

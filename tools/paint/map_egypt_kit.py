"""The map of Egypt (MAP-15E): its measurements, its paints, the papyrus, and the reed pen.

A scribe's working sketch on a sheet of papyrus, drawn for a stranger: the Nile along the bottom, the edge of the
desert, the Horizon (the pyramid) seen from the river with its inside left blank, and the four places of the act.
Black (carbon) for the drawing, red (ochre) for the ways and the marks, a little thin colour where a brush would
put it. Every number here is a place on the 800 x 600 frame of the map screen.

The papyrus is made the way papyrus is: strips laid across (the side we see) over strips laid along (showing
through), pressed into one sheet; two sheets joined with a narrow overlap; the edges a little frayed and browned;
an old fold, a stain or two. The reed pen is a rush with a chewed end: its line swells and thins with the hand,
starts dark from the ink pot and runs paler, and catches on the fibres where it runs dry."""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, blur, curve, grid, lerp, noise, rgb, smooth, warp
import postimp_paints as PP

W, H = 800, 600
SHAPE = (H, W)
OUT = "out/map-egypt"
CHECK = "out/map-egypt-check"

# ---------------------------------------------------------------- the paints (mixed from the box by name)


def paint(name):
    return rgb(PP.PAINTS[name]["hex"])


def mix(*parts):
    """mix(("naples-yellow", 3), ("lead-white", 1)): the paints in those proportions."""
    tot = float(sum(k for _, k in parts))
    out = np.zeros(3, dtype=F32)
    for name, k in parts:
        out += (paint(name) if isinstance(name, str) else np.asarray(name, F32)) * (k / tot)
    return out


def darker(c, k):
    """A paint brought down by adding a dark: the same colour at k of its strength of light."""
    return np.clip(np.asarray(c, F32) * k, 0, 1).astype(F32)


SHEET_PALE = mix(("lead-white", 5), ("naples-yellow", 4))                         # the middle of the sheet
SHEET = mix(("naples-yellow", 7), ("lead-white", 2), ("yellow-ochre", 1.2))       # straw
SHEET_WARM = mix(("naples-yellow", 5), ("yellow-ochre", 4), ("lead-white", 1))    # toward the edges
SHEET_EDGE = mix(("yellow-ochre", 6), ("burnt-sienna", 3), ("naples-yellow", 1))  # the browned edge
SHEET_DARK = mix(("yellow-ochre", 4), ("burnt-sienna", 4), ("deep-violet", 0.6))  # stains, the frayed rim
INK = darker(mix(("prussian-blue", 5), ("burnt-sienna", 3.4), ("yellow-ochre", 1.2)), 0.62)   # carbon black, a little warm
RED = mix(("burnt-sienna", 6), ("vermilion", 3), ("yellow-ochre", 1))                         # red ochre
WATER = mix(("cerulean", 6), ("veronese-green", 3), ("lead-white", 1))           # a thin wash in the river
GREEN = mix(("veronese-green", 6), ("emerald-green", 1.5), ("yellow-ochre", 2.5))  # palm crowns and reeds
WAGON = mix(("vermilion", 6), ("chrome-orange", 2), ("burnt-sienna", 2))          # "a red box"
GOLD = mix(("chrome-yellow", 5), ("yellow-ochre", 4), ("naples-yellow", 1))       # the king's furniture
LOTUS = mix(("cerulean", 5), ("lilac", 3), ("lead-white", 2))
HALO = mix(("lead-white", 6), ("naples-yellow", 5), ("yellow-ochre", 0.6))        # the names' soft edge


def hexof(c):
    c = np.clip(np.asarray(c, F32) * 255 + 0.5, 0, 255).astype(int)
    return "#%02x%02x%02x" % tuple(c)


# ---------------------------------------------------------------- the sheet and the lie of the land
EDGE = (47, 143, 753, 557)           # where the papyrus's edge runs on average (it wanders by a few pixels)
JOINS = (298.0, 574.0)               # where one sheet of papyrus overlaps the next (the joins run down the sheet)
CREASE_X = 404.0                     # an old fold down the middle
CREASE_Y = 338.0                     # and a shorter one across the left half

RIVER_TOP = [(50, 507), (160, 509), (290, 506), (420, 509), (560, 506), (690, 508), (751, 507)]
RIVER_BOTTOM = [(50, 548), (170, 550), (300, 547), (440, 550), (580, 548), (700, 550), (751, 548)]
# the edge of the desert: the valley floor by the river (below and left of it) and the plateau (above and right)
DESERT_EDGE = [(49, 382), (100, 380), (152, 386), (204, 398), (244, 418), (270, 440), (300, 455), (352, 461),
               (420, 459), (500, 464), (590, 461), (670, 465), (752, 462)]

# the Horizon: the great pyramid seen from the river
APEX = (566.0, 154.0)
BASE_Y = 394.0
HALF = 178.0
LEFT = (APEX[0] - HALF, BASE_Y)
RIGHT = (APEX[0] + HALF, BASE_Y)
SLOPE = (BASE_Y - APEX[1]) / HALF    # rise per pixel across


def left_x(y):
    """Where the pyramid's left face is at row y."""
    return APEX[0] - (y - APEX[1]) / SLOPE


def right_x(y):
    return APEX[0] + (y - APEX[1]) / SLOPE


SMALL_PYRAMIDS = [(98.0, 262.0, 34.0), (146.0, 262.0, 26.0), (186.0, 262.0, 19.0)]   # (middle, foot row, height): far off

# ---------------------------------------------------------------- the places and ways (the places' own drawings are in map_egypt_things)
# where the ways meet at each place: the portraits stand there (the layout script measures them back from the paint)
JOIN = {
    "river": (263.0, 455.0),      # beside the wagon's tail, where the boy's prints start up the track
    "site": (365.0, 420.0),       # in front of the works, below the foot of the stair
    "gallery": (452.0, 368.0),    # the level floor at the foot of the gallery, where the way in arrives
    "chamber": (548.0, 285.0),    # just inside the chamber's doorway, at the top of the ramp
}
STAIR_FOOT = 377.0                   # where the stair up the face starts, on the ground in front of it
ENTRANCE = (left_x(360.0), 360.0)    # the doorway in the face, up the stair (its sill)
DOOR_H = 9.5                         # the doorway's height, up the face
PASSAGE_FALL = 0.40                  # the low passage in: it runs down into the stone this much a pixel
GALLERY_FOOT = (461.0, 373.0)        # the bottom of the ramp, inside
GALLERY_TOP = (527.0, 307.5)         # the top step, under the chamber's doorway (its top is the chamber's floor)
CHAMBER = (538.0, 266.0, 641.0, 303.0)   # the room: x0, y0, x1, y1 (its floor at y1)

# the track up from the river, from the river's pin to the site's (the other two ways follow the stair and the ramp:
# map_egypt_things works them out from the places' own measurements)
TRACK = [JOIN["river"], (287.0, 446.5), (312.0, 438.0), (338.0, 428.5), JOIN["site"]]

# ---------------------------------------------------------------- the papyrus


def _strip_edges(lo, hi, rng, narrow, wide):
    edges, at = [], lo - rng.uniform(0, wide)
    while at < hi + wide:
        edges.append(at)
        at += rng.uniform(narrow, wide)
    return np.array(edges, dtype=F32)


def papyrus(seed=11, ss=2):
    """The sheet, before any brush or ink: (picture, alpha, info). `info` holds the maps the later passes need:
    'fibre' (the grain of the top strips, 0..1, at frame size), 'edge' (distance in from the sheet's edge)."""
    rng = np.random.default_rng(seed)
    h, w = H * ss, W * ss
    gx, gy = grid((h, w))
    x, y = (gx + 0.5) / ss - 0.5, (gy + 0.5) / ss - 0.5
    x0, y0, x1, y1 = EDGE

    # the edge: a rectangle whose sides wander, with a few chips out of it
    wl = (noise((h, 1), (1, 70 * ss), seed + 1, 3)[:, 0] - 0.5) * 6.0
    wr = (noise((h, 1), (1, 70 * ss), seed + 2, 3)[:, 0] - 0.5) * 6.0
    wt = (noise((1, w), (70 * ss, 1), seed + 3, 3)[0] - 0.5) * 5.0
    wb = (noise((1, w), (70 * ss, 1), seed + 4, 3)[0] - 0.5) * 5.0
    fine = (noise((h, w), 3.0 * ss, seed + 5, 2) - 0.5) * 1.6
    d = np.minimum.reduce([x - (x0 + wl[:, None]), (x1 + wr[:, None]) - x, y - (y0 + wt[None, :]), (y1 + wb[None, :]) - y]) + fine
    ragged = noise((h, w), 4.0 * ss, seed + 36, 2) - 0.5
    for cx, cy, r in ((47, 300, 3.2), (210, 143, 2.6), (753, 236, 3.8), (520, 557, 2.8), (753, 521, 2.4), (96, 557, 2.2)):
        d = np.minimum(d, np.hypot((x - cx) / 1.5, y - cy) * (1 + 0.7 * ragged) - r)   # small chips broken out of the edge
    alpha = np.clip(d + 0.5, 0, 1).astype(F32)

    # the colour of the sheet: pale straw in the middle, warmer toward the edges, mottled
    mott = noise((h, w), 150 * ss, seed + 6, 4)
    warmth = 0.12 + 0.62 * (1 - smooth(np.clip(d, 0, None) / 120.0)) + 0.30 * (mott - 0.5)
    pic = lerp(SHEET_PALE[None, None, :], SHEET_WARM[None, None, :], np.clip(warmth, 0, 1)[..., None])
    pic = lerp(pic, SHEET[None, None, :], 0.30)

    # the top strips: laid across, each a little lighter or darker, their edges a fine ridge and shadow
    edges = _strip_edges(y0 - 4, y1 + 4, rng, 15.0, 33.0)
    sway = (noise((1, w), (240 * ss, 1), seed + 7, 3)[0] - 0.5) * 3.0
    ys = y + sway[None, :]
    k = np.clip(np.searchsorted(edges, ys) - 1, 0, len(edges) - 2)
    tone = rng.normal(0, 0.020, len(edges)).astype(F32)[k]
    lo, hi = edges[k], edges[k + 1]
    dist = np.minimum(ys - lo, hi - ys)
    ridge = np.exp(-((ys - lo - 0.9) ** 2) / 0.5) * 0.045 - np.exp(-((ys - lo + 0.2) ** 2) / 0.35) * 0.060
    ridge *= 0.4 + 0.9 * noise((h, w), (70 * ss, 1), seed + 10, 2)
    streak = (noise((h, w), (130 * ss, 0.9 * ss), seed + 8, 3) - 0.5)
    streak2 = (noise((h, w), (46 * ss, 1.5 * ss), seed + 9, 3) - 0.5)

    # the strands of the pith: thin darker fibres of every length, a few lighter ones, none quite straight
    dark_im, light_im = Image.new("L", (w, h), 0), Image.new("L", (w, h), 0)
    dd, dl = ImageDraw.Draw(dark_im), ImageDraw.Draw(light_im)
    area = (x1 - x0) * (y1 - y0)
    for kind, count, draw_ in (("dark", int(area / 190), dd), ("light", int(area / 520), dl)):
        for _ in range(count):
            sy = rng.uniform(y0 - 2, y1 + 2)
            sx = rng.uniform(x0 - 30, x1)
            ln = rng.choice([rng.uniform(8, 40), rng.uniform(30, 120), rng.uniform(100, 320)], p=[0.45, 0.4, 0.15])
            slope = rng.normal(0, 0.010)
            amp, per, ph = rng.uniform(0.1, 0.7), rng.uniform(40, 160), rng.uniform(0, 6.3)
            n = max(2, int(ln / 6))
            pts = [((sx + ln * i / n) * ss, (sy + slope * ln * i / n + amp * math.sin(ph + ln * i / n / per * 6.28)) * ss) for i in range(n + 1)]
            val = int(255 * (rng.uniform(0.25, 1.0) if kind == "dark" else rng.uniform(0.3, 1.0)))
            draw_.line(pts, fill=val, width=max(1, int(round(ss * rng.uniform(0.45, 1.25)))))
    strands = blur(np.asarray(dark_im, dtype=F32) / 255, 0.35 * ss)
    pith = blur(np.asarray(light_im, dtype=F32) / 255, 0.45 * ss)
    fibre = np.clip(0.5 + streak * 0.8 + streak2 * 0.45 - strands * 0.55 + pith * 0.35, 0, 1)
    lum = 1 + tone + streak * 0.050 + streak2 * 0.030 - strands * 0.085 + pith * 0.040 + ridge
    lum -= np.exp(-dist / 2.5) * 0.008

    # the strips laid along, behind, showing through faintly; and the weave where the two cross
    vedges = _strip_edges(x0 - 4, x1 + 4, rng, 17.0, 31.0)
    vsway = (noise((h, 1), (1, 260 * ss), seed + 11, 3)[:, 0] - 0.5) * 3.0
    xs = x + vsway[:, None]
    kv = np.clip(np.searchsorted(vedges, xs) - 1, 0, len(vedges) - 2)
    vdist = np.minimum(xs - vedges[kv], vedges[kv + 1] - xs)
    vtone = rng.normal(0, 0.012, len(vedges)).astype(F32)[kv]
    vstreak = noise((h, w), (1.2 * ss, 90 * ss), seed + 12, 3) - 0.5
    lum += vtone + vstreak * 0.022 - np.exp(-vdist / 1.6) * 0.016 * (0.5 + noise((h, w), (1, 80 * ss), seed + 37, 2))

    # where two sheets were joined: a narrow band of double thickness, a little darker, with a crisp edge
    for jx, wd, sd in ((JOINS[0], 15.0, 13), (JOINS[1], 13.0, 14)):
        wob = (noise((h, 1), (1, 120 * ss), seed + sd, 3)[:, 0] - 0.5) * 3.0
        u = x - (jx + wob[:, None])
        band = smooth((u + 0.5) / 1.2) * (1 - smooth((u - wd) / 2.5))
        lum -= band * 0.035
        lum -= np.exp(-((u - 0.3) ** 2) / 0.6) * 0.06
        lum += np.exp(-((u - 1.6) ** 2) / 0.8) * 0.025
    pic = pic * lum[..., None]

    # the edges: browned and darker, unevenly, as handling leaves them
    rim = (1 - smooth(np.clip(d, 0, None) / (10.0 + 10.0 * noise((h, w), 40 * ss, seed + 15, 3))))
    pic = lerp(pic, (pic * SHEET_EDGE / SHEET)[...], (rim * 0.55)[..., None])
    pic = lerp(pic, SHEET_DARK[None, None, :] * (0.85 + 0.3 * fibre[..., None]), (np.exp(-np.clip(d, 0, None) / 1.4) * 0.55)[..., None])

    # an old fold down the middle, and a shorter one across: a lit ridge, a shadow, and little cracks along it
    for axis, at, span, sd in (("x", CREASE_X, (y0, y1), 21), ("y", CREASE_Y, (x0, 470.0), 22)):
        if axis == "x":
            wob = (noise((h, 1), (1, 160 * ss), seed + sd, 3)[:, 0] - 0.5) * 5.0
            u = x - (at + wob[:, None])
            along = y
        else:
            wob = (noise((1, w), (160 * ss, 1), seed + sd, 3)[0] - 0.5) * 5.0
            u = y - (at + wob[None, :])
            along = x
        reach = smooth((along - span[0]) / 30.0) * (1 - smooth((along - span[1]) / 60.0))
        crack = (noise((h, w), (6 * ss, 6 * ss), seed + sd + 1, 2) > 0.72).astype(F32)
        pic = pic * (1 + (np.exp(-((u + 1.0) ** 2) / 1.0) * 0.050 - np.exp(-((u - 0.8) ** 2) / 0.9) * 0.065
                          - np.exp(-(u ** 2) / 0.4) * crack * 0.10) * reach)[..., None]

    # stains: a drop of something long ago, with its tide line; a smaller darker spot; a few flecks
    for cx, cy, r, depth, sd in ((206.0, 204.0, 26.0, 0.028, 31), (684.0, 486.0, 13.0, 0.040, 32), (118.0, 172.0, 8.0, 0.025, 33)):
        rr = np.hypot(x - cx, (y - cy) * 1.15) / r + (noise((h, w), 22 * ss, seed + sd, 3) - 0.5) * 0.5
        inside = (1 - smooth((rr - 0.88) / 0.12)) * (0.35 + 0.65 * smooth((rr - 0.25) / 0.65))   # darker toward its rim
        tide = np.exp(-((rr - 0.93) ** 2) / 0.0010) * (0.4 + 0.8 * noise((h, w), 9 * ss, seed + sd + 3, 2))
        pic = pic * (1 - (inside * depth + tide * depth * 0.9))[..., None]
        pic = lerp(pic, pic * SHEET_EDGE / SHEET, (inside * 0.25)[..., None])
    flecks = (noise((h, w), 2.0 * ss, seed + 34, 1) > 0.992).astype(F32) * (noise((h, w), 50 * ss, seed + 35, 2) > 0.6)
    pic = pic * (1 - flecks[..., None] * 0.16)

    # threads at the edge: fibres of the top strips stand out at the two ends, of the back strips at top and bottom
    hair = Image.new("L", (w, h), 0)
    dr = ImageDraw.Draw(hair)
    for side in (-1, 1):
        for _ in range(70):
            yy = rng.uniform(y0 + 6, y1 - 6)
            xx = (x0 + wl[int(min(h - 1, yy * ss))] if side < 0 else x1 + wr[int(min(h - 1, yy * ss))])
            ln = rng.uniform(2.0, 9.0)
            dr.line([(xx - side * 1.5) * ss, yy * ss, (xx + side * ln) * ss, (yy + rng.normal(0, 0.8)) * ss], fill=255, width=max(1, int(ss * rng.uniform(0.7, 1.2))))
    for side in (-1, 1):
        for _ in range(55):
            xx = rng.uniform(x0 + 8, x1 - 8)
            yy = (y0 + wt[int(min(w - 1, xx * ss))] if side < 0 else y1 + wb[int(min(w - 1, xx * ss))])
            ln = rng.uniform(1.5, 5.0)
            dr.line([xx * ss, (yy - side * 1.5) * ss, (xx + rng.normal(0, 0.6)) * ss, (yy + side * ln) * ss], fill=255, width=max(1, int(ss * rng.uniform(0.7, 1.1))))
    hairs = np.asarray(hair, dtype=F32) / 255 * (d < 1.0)
    pic = lerp(pic, SHEET_EDGE[None, None, :] * (0.8 + 0.25 * fibre[..., None]), hairs[..., None] * 0.9)
    alpha = np.maximum(alpha, hairs)

    def down(a):
        if ss == 1:
            return a.astype(F32)
        sh = (H, W) + a.shape[2:]
        return a.reshape(H, ss, W, ss, *a.shape[2:]).mean(axis=(1, 3)).astype(F32).reshape(sh)

    info = {"fibre": down(fibre), "edge": down(d), "strip_lum": down(lum)}
    return np.clip(down(pic), 0, 1), np.clip(down(alpha), 0, 1), info


# ---------------------------------------------------------------- the reed pen


def path(points, step=2.0, smooth_it=False):
    """A path through the points, at about `step` pixels a point: straight between them, or a smooth curve."""
    pts = curve(points, 12) if smooth_it and len(points) > 2 else [tuple(map(float, p)) for p in points]
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        for i in range(1, n + 1):
            t = i / n
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return out


class Pen:
    """A reed pen's marks on one layer of the map (the sheet itself, one place, or one way).

    Three kinds of mark: 'black' (carbon ink), 'red' (ochre), and washes (thin colour laid with a brush, under
    the lines). Each is kept as coverage (0 to 1) at frame size; map_egypt lays them on the papyrus. A stroke
    swells and thins along its length as a hand presses and lifts, starts dark and runs paler, and wanders a
    little off the line it was meant to follow."""

    def __init__(self, seed=0, ss=3):
        self.ss = ss
        self.rng = np.random.default_rng(seed)
        self.cov = {"black": np.zeros(SHAPE, F32), "red": np.zeros(SHAPE, F32)}
        self.washes = []              # (colour, coverage, rim): laid first, in order

    # -- the stroke itself
    def stroke(self, points, width=1.6, ink="black", dark=1.0, fade=0.22, wobble=0.35, taper=(0.35, 0.55), swell=0.22,
               smooth_it=False, step=1.6, cap=True):
        rng = self.rng
        pts = path(points, step, smooth_it)
        if len(pts) < 2:
            return self
        P = np.array(pts, dtype=np.float64)
        seg = np.hypot(*(P[1:] - P[:-1]).T)
        L = np.concatenate([[0.0], np.cumsum(seg)])
        total = max(L[-1], 1e-6)
        t = L / total
        # the wander: a smooth drift off the line, across it
        tang = np.gradient(P, axis=0)
        tang /= np.maximum(np.hypot(tang[:, 0], tang[:, 1]), 1e-9)[:, None]
        nrm = np.stack([-tang[:, 1], tang[:, 0]], axis=1)
        k = max(2, int(total / 18) + 2)
        drift = np.interp(L, np.linspace(0, total, k), rng.normal(0, wobble, k))
        P = P + nrm * drift[:, None]
        # the width: pressed in the middle, lighter where the pen lands and lifts, with a little life in it
        kw = max(2, int(total / 10) + 2)
        life = np.interp(L, np.linspace(0, total, kw), rng.normal(0, swell * 0.6, kw))
        start = np.minimum(1.0, (L + 0.6) / max(0.6, width * 2.2)) if taper[0] else 1.0
        end = np.minimum(1.0, (total - L + 0.6) / max(0.6, width * 3.0)) if taper[1] else 1.0
        wd = width * (1 + swell * np.sin(np.pi * t) ** 0.7 + life) * (1 - taper[0] + taper[0] * start) * (1 - taper[1] + taper[1] * end)
        wd = np.maximum(wd, 0.45)
        # the ink: dark from the pot, paler as it runs out
        dens = dark * (1 - fade * t ** 1.2) * (1 + rng.normal(0, 0.03))
        self._lay(P, wd, dens, ink, cap)
        return self

    def _lay(self, P, wd, dens, ink, cap):
        ss = self.ss
        pad = float(wd.max()) + 3
        bx0, by0 = int(max(0, math.floor(P[:, 0].min() - pad))), int(max(0, math.floor(P[:, 1].min() - pad)))
        bx1, by1 = int(min(W, math.ceil(P[:, 0].max() + pad))), int(min(H, math.ceil(P[:, 1].max() + pad)))
        if bx1 <= bx0 or by1 <= by0:
            return
        acc = np.zeros(((by1 - by0) * ss, (bx1 - bx0) * ss), dtype=F32)
        n = len(P)
        chunk = 6                                        # about ten pixels of line share one loading of ink
        Qall = (P - [bx0, by0]) * ss
        wall = wd * ss
        for s in range(0, n - 1, chunk):
            e = min(n, s + chunk + 1)
            cx0, cy0 = int(max(0, Qall[s:e, 0].min() - wall[s:e].max() - 2)), int(max(0, Qall[s:e, 1].min() - wall[s:e].max() - 2))
            cx1, cy1 = int(min(acc.shape[1], Qall[s:e, 0].max() + wall[s:e].max() + 3)), int(min(acc.shape[0], Qall[s:e, 1].max() + wall[s:e].max() + 3))
            if cx1 <= cx0 or cy1 <= cy0:
                continue
            im = Image.new("L", (cx1 - cx0, cy1 - cy0), 0)
            dr = ImageDraw.Draw(im)
            Q = Qall[s:e] - [cx0, cy0]
            wq = wall[s:e]
            for i in range(len(Q)):                      # a disc at every point, and a quad to the next: corners stay solid
                qx, qy = Q[i]
                r = wq[i] / 2
                if cap or 0 < s + i < n - 1:
                    dr.ellipse([qx - r, qy - r, qx + r, qy + r], fill=255)
                if i + 1 < len(Q):
                    dx, dy = Q[i + 1] - Q[i]
                    ln = math.hypot(dx, dy) or 1.0
                    nx, ny = -dy / ln, dx / ln
                    r2 = wq[i + 1] / 2
                    dr.polygon([(qx + nx * r, qy + ny * r), (Q[i + 1][0] + nx * r2, Q[i + 1][1] + ny * r2),
                                (Q[i + 1][0] - nx * r2, Q[i + 1][1] - ny * r2), (qx - nx * r, qy - ny * r)], fill=255)
            a = np.asarray(im, dtype=F32) / 255 * float(np.mean(dens[s:e]))
            sub = acc[cy0:cy1, cx0:cx1]
            np.maximum(sub, a, out=sub)
        cov = acc.reshape(by1 - by0, ss, bx1 - bx0, ss).mean(axis=(1, 3))
        layer = self.cov[ink]
        sub = layer[by0:by1, bx0:bx1]
        sub[...] = 1 - (1 - sub) * (1 - np.clip(cov, 0, 1))

    def dot(self, x, y, r=1.2, ink="black", dark=1.0):
        """A dab of the pen: a dot that is not quite round."""
        a = self.rng.uniform(0, math.pi)
        pts = [(x + math.cos(a + i * math.pi / 3) * r * self.rng.uniform(0.8, 1.15), y + math.sin(a + i * math.pi / 3) * r * self.rng.uniform(0.75, 1.1)) for i in range(6)]
        P = np.array(path(pts + [pts[0]], 0.8), dtype=np.float64)
        self._fill(P, ink, dark)
        return self

    def fill(self, points, ink="black", dark=1.0):
        """A small solid patch of ink (a doorway's dark, a dot of red): pen strokes laid side by side, in effect."""
        self._fill(np.array(points, dtype=np.float64), ink, dark)
        return self

    def _fill(self, P, ink, dark):
        ss = self.ss
        bx0, by0 = int(max(0, math.floor(P[:, 0].min() - 2))), int(max(0, math.floor(P[:, 1].min() - 2)))
        bx1, by1 = int(min(W, math.ceil(P[:, 0].max() + 2))), int(min(H, math.ceil(P[:, 1].max() + 2)))
        if bx1 <= bx0 or by1 <= by0:
            return
        im = Image.new("L", ((bx1 - bx0) * ss, (by1 - by0) * ss), 0)
        ImageDraw.Draw(im).polygon([((px - bx0) * ss, (py - by0) * ss) for px, py in P], fill=255)
        cov = (np.asarray(im, dtype=F32) / 255).reshape(by1 - by0, ss, bx1 - bx0, ss).mean(axis=(1, 3)) * dark
        sub = self.cov[ink][by0:by1, bx0:bx1]
        sub[...] = 1 - (1 - sub) * (1 - np.clip(cov, 0, 1))

    # -- washes: thin colour laid with a soft brush, a darker rim where the water dried
    def wash(self, points, colour, amount=0.35, rim=0.35, seed=0, brush=6.0, soft=0.9, dabs=True, body=0.0):
        """Thin colour inside a polygon, laid as a brush lays it: in overlapping dabs along the shape, a little
        uneven, with the pigment gathered at the rim where the wash dried. `body` (0 to 1) makes it less of a
        glaze over the sheet and more the paint's own colour."""
        rng = np.random.default_rng(seed)
        P = np.array(points, dtype=np.float64)
        bx0, by0 = int(max(0, math.floor(P[:, 0].min() - 6))), int(max(0, math.floor(P[:, 1].min() - 6)))
        bx1, by1 = int(min(W, math.ceil(P[:, 0].max() + 6))), int(min(H, math.ceil(P[:, 1].max() + 6)))
        ss = 3
        im = Image.new("L", ((bx1 - bx0) * ss, (by1 - by0) * ss), 0)
        ImageDraw.Draw(im).polygon([((px - bx0) * ss, (py - by0) * ss) for px, py in P], fill=255)
        m = (np.asarray(im, dtype=F32) / 255).reshape(by1 - by0, ss, bx1 - bx0, ss).mean(axis=(1, 3))
        hh, ww = m.shape
        m = warp(m, 0.8, 6.0, seed)
        if soft:
            m = blur(m, soft)
        bm = np.clip(m * 1.15 - 0.08, 0, 1)
        if dabs:                                          # the brush's own marks: patches a little more and less loaded
            lumps = noise((hh, ww), brush * 1.6, seed + 1, 3)
            bm = bm * (0.72 + 0.5 * lumps)
        edge = np.clip(bm - blur(bm, 1.6), 0, 1) * 2.4    # pigment gathers where the wash dried
        cov = np.clip(bm * amount + edge * rim * amount, 0, 1).astype(F32)
        full = np.zeros(SHAPE, F32)
        full[by0:by1, bx0:bx1] = cov
        self.washes.append((np.asarray(colour, F32), full, body))
        return self

    # -- what the layer covers
    def coverage(self):
        c = np.maximum(self.cov["black"], self.cov["red"])
        for _, a, _ in self.washes:
            c = np.maximum(c, a)
        return c


def lay(picture, pen, info, black=INK, red=RED):
    """Lay a pen's marks on a picture of the papyrus: the washes, then the red, then the black. The sheet's grain
    shows through all of them, more where the pen ran dry."""
    pic = picture.copy()
    fib = info["fibre"]
    tex = (fib - 0.5)
    for colour, a, body in pen.washes:
        glaze = np.clip(colour / np.maximum(SHEET, 1e-3), 0, 1.05)            # a wash darkens toward its colour
        aa = np.clip(a * (1 + 0.6 * tex), 0, 1)[..., None]
        glazed = pic * lerp(np.ones(3, F32)[None, None, :], glaze[None, None, :], aa)
        own = lerp(pic, colour[None, None, :] * (0.92 + 0.16 * fib[..., None]), aa)
        pic = lerp(glazed, own, body) if body else glazed
    r = pen.cov["red"]
    if r.any():
        ra = np.clip(r * (0.93 + 0.22 * tex) - np.clip(0.55 - r, 0, 1) * np.clip(tex, 0, 1) * 0.6, 0, 1)
        target = np.clip(pic * (red / SHEET)[None, None, :] * 1.02, 0, 1)
        pic = lerp(pic, target, (ra * 0.92)[..., None])
    b = pen.cov["black"]
    if b.any():
        ba = np.clip(b * (0.95 + 0.14 * tex) - np.clip(0.6 - b, 0, 1) * np.clip(tex, 0, 1) * 0.7, 0, 1)
        lum = (picture @ np.array([0.3, 0.55, 0.15], F32))[..., None]
        target = black[None, None, :] * (0.88 + 0.30 * lum)
        pic = lerp(pic, target, (ba * 0.96)[..., None])
    return np.clip(pic, 0, 1).astype(F32)

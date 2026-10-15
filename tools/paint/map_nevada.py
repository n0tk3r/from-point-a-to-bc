"""The map of Nevada (MAP-15N): Grandpa Joe's own road map, from the rack on his counter, opened out flat.

    python3 map_nevada.py fast     a quick look: no brush pass
    python3 map_nevada.py          the full passes: writes out/map-nevada/ (the pictures and layout.json), then checks it

What is painted (see map_nevada_kit.py for the sheet, its inks and its folds):

  back.png                the sheet: the paper, its folds and wear; the land in cream and tan, the ranges hatched in
                          brown, the dry lakes, the faint grid of sections, the highway in red from the west edge
                          through LAST GAS to the east edge (TO NOTHING), two dirt roads; the cover panel ("Compliments
                          of GRANDPA JOE'S LAST STOP", the sign's GAS crossed out, ROCKS, LEMONADE), the legend with
                          the scale of miles and the north arrow, and the detail panel, empty but for its frame and
                          title. Never a place, never a way.
  place-roadside.png      in the detail: the lot in plan (the road, the shack's walls and porch, the pump, the lemonade
                          stand and its umbrella, the sign, the fence and its notice, the tire tracks stopping, the
                          glass, Mom's car); on the main map: the No Gas sign on the highway where the Last Stop is,
                          with a short leader up to the detail.
  place-store.png         in the detail, inside the shack's walls: the store in plan, from its model (the checkered
                          floor, the hubcaps round the walls and the red tractor wheel among them, the counter and the
                          register, the grill, Harold the cooler, the shelves, the spinner, the rock bins, Jolene's
                          chair, the hat board with four hats and today's peg empty, the still fan, the water by the
                          door, the screen door open) and out back the hen yard: five hens in a row.
  place-road.png          on the main map: the stretch of the highway beyond the Last Stop picked out (a heavier line)
                          and a small printed limousine on it.
  path-roadside-store.png the shop's door: a short printed arrow from the lot in at the door.

The light: a flat sheet under a light from the upper left (the folds' shadows and lights). Ink lies on the paper: every
place's picture is the finished sheet with that place's ink printed on it, cut out where the ink is (wherever it covers
more than KEEP of a pixel, so that a thin line keeps its soft edge).

The four passes: under() the paper (its age, its stains, its fold dirt) and the broad tints printed on it (the land, the
high ground, the lakes, the cover's band); light_folds() the panels' tilt; strokes() the brush over all that (the paper
and the tints: a brush where a brush belongs); then the details, crisp: the lines and the lettering printed over the
brushwork, the creases and their worn crossings, the paper's edge; and finish(): one grain, one palette for the whole map
(the sheet with every place and way on it), each file reduced to it and written with a hard-edged clear ground.
"""

import math
import os
import sys

import numpy as np
from PIL import Image

from brush import F32, blur, grid, lerp, noise, palette_of, save, strokes, to_palette, grain
import map_nevada_kit as K
from map_nevada_kit import (W, H, SHEET, NEAT, COVER, LEGEND, INSET, INSET_TITLE, FOLDS_X, FOLDS_Y, Press, mixp, paint,
                            smooth_path, cut, at_x, along, path_length)
import nevada_store_model as SM

FAST = "fast" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "map-nevada")
SEED = 1504

ROAD = smooth_path(K.HIGHWAY, 12)                        # the highway, as a dense polyline, west to east


# ================================================================ the inset's measurements (the plan of the Last Stop)
# The detail is drawn "not to scale": the shack large, so that the store's inside can be read; the rest of the lot laid
# round it as the roadside shows it (the road on the left, the shack's front to us, the pump and the stand in front of
# it to the right, the fence on the right with its notice, the tracks running out from under it and stopping, the
# glass where they stop, Mom's car at the front by the road).
SHACK = (498.0, 203.0)                                   # the shack's back left corner (the store model's Z = 0, X = 760)
K_CM = 150.0 / SM.D                                      # pixels per centimetre in the detail (the shack is 10.4 m long)


def plan(X, Z):
    """The store model's floor (X out from the front wall, Z along it from the hen-yard end) -> a point of the detail.
    The shack's front (X = 0) is toward us (down), the hen-yard end (Z = 0) on the left: as it stands on the lot."""
    return (SHACK[0] + Z * K_CM, SHACK[1] + (SM.W - X) * K_CM)


def plan_box(X0, X1, Z0, Z1):
    (ax, ay), (bx, by) = plan(X0, Z0), plan(X1, Z1)
    return (min(ax, bx), min(ay, by), max(ax, bx), max(ay, by))


SHACK_BOX = plan_box(0, SM.W, 0, SM.D)                   # its walls' middle lines: x 498..648, y 203..312.6
FRONT_DOOR = plan_box(0, 0, SM.FRONTDOOR[0], SM.FRONTDOOR[1])
BACK_DOOR = plan_box(SM.BACKDOOR[0], SM.BACKDOOR[1], 0, 0)
DOOR_X = (FRONT_DOOR[0] + FRONT_DOOR[2]) / 2             # the middle of the shop's door, across
ARROW = (SHACK_BOX[3] + 32.0, SHACK_BOX[3] - 25.0)        # the way's arrow: its tail (on the lot) and its tip (inside), y
ROAD_BAND = (444.0, 460.0)                               # the road in the detail: its two edges (x)
INNER_TOP = 168.0                                        # the top of the detail's drawing room (under its title)
INNER_BOTTOM = 446.0


# ================================================================ the sheet's own printing
def print_land(broad, crisp):
    """The main map: the land, the grid, the ranges, the lakes, the roads, Last Gas, the mileage, TO NOTHING."""
    x0, y0, x1, y1 = NEAT
    broad.rect("cream", x0, y0, x1, y1)
    # the high ground: a tan tint wherever the land rises (from the ranges' height field), its edge as printed
    h = K.relief(K.RANGES, SEED + 71)
    tan = (blur(h, 2.6) > 0.025).astype(np.uint8) * 255
    tan_im = Image.fromarray(tan, "L").resize((W * broad.ss, H * broad.ss), Image.BILINEAR).point(lambda v: 255 if v > 127 else 0)
    broad.plate("tan").paste(255, mask=tan_im)
    # the dry lakes: a pale tint, a dashed shore, a few stipples, a name
    for lk in K.LAKES:
        pts = lake_outline(lk)
        broad.poly("blue_tint", pts)
        crisp.dashed("blue", pts + [pts[0]], 0.8, 2.6, 1.8)
        rng = np.random.default_rng(lk["seed"])
        for _ in range(int(lk["r"][0] * lk["r"][1] * 0.10)):
            a, rr = rng.random() * 2 * math.pi, math.sqrt(rng.random()) * 0.72
            crisp.ellipse("blue", lk["c"][0] + math.cos(a) * rr * lk["r"][0], lk["c"][1] + math.sin(a) * rr * lk["r"][1], 0.45, 0.45)
        if lk["name"]:
            crisp.text("blue", "DRY LAKE", lk["name"], 12, anchor="ms", spacing=1.0, slant=0.18)
    # the grid of sections: faint, every 36 pixels, the north-south lines jogging once at a correction line
    jog_y, jog = 278.0, 9.0
    for gx in np.arange(x0 + 18, x1, 36.0):
        crisp.line("grid", [(gx, y0), (gx, jog_y)], 0.7, round_ends=False)
        crisp.line("grid", [(gx + jog, jog_y), (gx + jog, y1)], 0.7, round_ends=False)
    for gy in np.arange(y0 + 26, y1, 36.0):
        crisp.line("grid", [(x0, gy), (x1, gy)], 0.7, round_ends=False)
    crisp.line("grid", [(x0, jog_y), (x1, jog_y)], 0.9, round_ends=False)
    # the ranges, in hachures down their slopes
    K.hachures(crisp, h, "brown", step=0.16, spacing=2.1, seed=SEED + 73)
    # the dirt roads (dashed), then the highway over them
    for pts in (K.LAST_GAS_ROAD, K.SOUTH_ROAD):
        crisp.dashed("key", smooth_path(pts, 8), 1.0, 3.6, 2.6)
    crisp.line("red", ROAD, 3.0)
    # Last Gas: a town's open circle, its name, a gas pump; mileage ticks; the 37 between Last Gas and the Last Stop
    (gx_, gy_), _ = at_x(ROAD, K.LAST_GAS_T)
    for (px, py), (dx, dy) in (at_x(ROAD, K.LAST_GAS_T), at_x(ROAD, K.LAST_STOP_T)):
        crisp.line("key", [(px + dy * 5.5, py - dx * 5.5), (px - dy * 5.5, py + dx * 5.5)], 1.0, round_ends=False)
    for ink in ("red", "grid", "tan", "brown"):
        crisp.ellipse(ink, gx_, gy_, 3.6, 3.6, 0)
    crisp.ring("key", gx_, gy_, 3.6, 3.6, 1.3)
    crisp.text("key", "LAST GAS", (gx_ - 4, gy_ - 10), 12, anchor="rs", spacing=0.8, bold=0.25)
    pump(crisp, gx_ + 9, gy_ - 14, 1.0)
    mid = (K.LAST_GAS_T + K.LAST_STOP_T) / 2
    (mx, my), (mdx, mdy) = at_x(ROAD, mid)
    crisp.text("red", "37 MI.", (mx + mdy * 9 + 4, my - mdx * 9 + 4), 12, anchor="ms", spacing=0.5, bold=0.3)
    # the east end: the highway runs off the sheet, toward nothing
    (ex, ey), (edx, edy) = at_x(ROAD, x1 - 1)
    tip = (x1 - 2.0, ey)
    crisp.poly("red", [tip, (tip[0] - 9, tip[1] - 4.8), (tip[0] - 9, tip[1] + 4.8)])
    crisp.text("red", "TO NOTHING", (x1 - 6, ey - 9), 12, anchor="rs", spacing=1.0, bold=0.3)


def lake_outline(lk, n=36):
    rng = np.random.default_rng(lk["seed"])
    ph = rng.random(4) * 2 * math.pi
    out = []
    for i in range(n):
        a = i / n * 2 * math.pi
        k = 1 + 0.12 * math.sin(2 * a + ph[0]) + 0.08 * math.sin(3 * a + ph[1]) + 0.05 * math.sin(5 * a + ph[2])
        out.append((lk["c"][0] + math.cos(a) * lk["r"][0] * k, lk["c"][1] + math.sin(a) * lk["r"][1] * k))
    return out


def pump(press, cx, cy, s=1.0, ink="key"):
    """A gas pump, as a map's symbol: a body, a lamp on top, a hose. (cx, cy) the middle of its body."""
    press.rect(ink, cx - 2.6 * s, cy - 3.6 * s, cx + 2.6 * s, cy + 4.4 * s)
    press.rect(ink, cx - 1.5 * s, cy - 2.4 * s, cx + 1.5 * s, cy - 0.4 * s, 0)       # its little window
    press.ellipse(ink, cx, cy - 5.2 * s, 1.7 * s, 1.5 * s)
    press.line(ink, [(cx + 2.6 * s, cy - 1.8 * s), (cx + 4.4 * s, cy - 0.6 * s), (cx + 4.6 * s, cy + 3.2 * s), (cx + 3.6 * s, cy + 4.6 * s)], 0.8 * s)


def no_gas(press, cx, cy, s=1.0):
    """The Last Stop's sign as a map's symbol: a gas pump in a red ring with a red bar across it."""
    pump(press, cx - 0.4 * s, cy + 0.6 * s, 0.72 * s)
    r = 7.0 * s
    press.poly("key", slash(cx, cy, r, 1.9 * s), 0)                         # the bar is clean of the pump under it
    press.ring("red", cx, cy, r, r, 1.6 * s)
    press.poly("red", slash(cx, cy, r, 1.5 * s))


def slash(cx, cy, r, w):
    a = math.radians(-45)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    return [(cx - ux * r + nx * w / 2, cy - uy * r + ny * w / 2), (cx + ux * r + nx * w / 2, cy + uy * r + ny * w / 2),
            (cx + ux * r - nx * w / 2, cy + uy * r - ny * w / 2), (cx - ux * r - nx * w / 2, cy - uy * r - ny * w / 2)]


ALL_LAND = ("cream", "tan", "grid", "blue", "blue_tint", "brown", "red", "key", "red_tint", "key_tint", "brown_tint", "tan_tint")


def print_panels(broad, crisp):
    """The cover, the legend and the detail panel: each knocks the map out of the plates under it."""
    for (bx0, by0, bx1, by1) in (COVER, LEGEND, INSET):
        box = [(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)]
        broad.knock(ALL_LAND, box)
        crisp.knock(ALL_LAND, box)
    print_cover(broad, crisp)
    print_legend(broad, crisp)
    print_inset_frame(broad, crisp)
    # the neat line round the whole map
    crisp.frame("key", NEAT[0], NEAT[1], NEAT[2], NEAT[3], 1.1)


def print_cover(broad, crisp):
    x0, y0, x1, y1 = COVER
    cx = (x0 + x1) / 2
    crisp.frame("key", x0, y0, x1, y1, 1.3)
    crisp.frame("key", x0 + 2.5, y0 + 2.5, x1 - 2.5, y1 - 2.5, 0.6)
    # the red band, NEVADA knocked out of it in the paper's colour
    band = (x0 + 4.5, y0 + 4.5, x1 - 4.5, y0 + 36)
    broad.rect("red", *band)
    for p in (broad, crisp):
        p.text("red", "NEVADA", (cx, band[3] - 9.0), 21, anchor="ms", spacing=1.6, bold=0.55, value=0)
    crisp.text("key", "ROAD  MAP", (cx, y0 + 52), 12, anchor="ms", spacing=1.6, bold=0.2)
    # the little picture: the road to the horizon, mesas, the sun
    vig = (x0 + 7, y0 + 58, x1 - 7, y0 + 104)
    vx0, vy0, vx1, vy1 = vig
    hz = vy0 + 24
    broad.rect("blue_tint", vx0, vy0, vx1, hz)
    broad.rect("tan", vx0, hz, vx1, vy1)
    broad.ellipse("red", vx0 + 62, vy0 + 11, 6.5, 6.5)
    mesas = [[(vx0, hz), (vx0, hz - 6), (vx0 + 8, hz - 7), (vx0 + 12, hz - 12), (vx0 + 30, hz - 12), (vx0 + 34, hz - 6), (vx0 + 40, hz)],
             [(vx0 + 52, hz), (vx0 + 57, hz - 5), (vx0 + 70, hz - 5), (vx0 + 73, hz - 9), (vx0 + 82, hz - 9), (vx1, hz - 4), (vx1, hz)]]
    for m in mesas:
        broad.poly("tan", m)
        broad.poly("brown_tint", m)
        crisp.line("brown", m[1:-1], 0.8)
    vp = ((vx0 + vx1) / 2 - 3, hz)
    crisp.poly("key_tint", [(vp[0] - 0.8, hz), (vp[0] + 0.8, hz), (vx1 - 14, vy1), (vx0 + 18, vy1)])
    crisp.line("key", [vp, (vx0 + 18, vy1)], 0.8)
    crisp.line("key", [vp, (vx1 - 14, vy1)], 0.8)
    for t0, t1 in ((0.15, 0.28), (0.42, 0.6), (0.75, 1.0)):
        a = (lerp(vp[0], (vx0 + vx1) / 2 + 2, t0), lerp(hz, vy1, t0))
        b = (lerp(vp[0], (vx0 + vx1) / 2 + 2, t1), lerp(hz, vy1, t1))
        crisp.line("red_tint", [a, b], 0.6 + 1.1 * t1, round_ends=False)
    crisp.frame("key", vx0, vy0, vx1, vy1, 0.8)
    # compliments of the store
    crisp.text("key", "Compliments of", (cx, y0 + 120), 12, anchor="ms", slant=0.2)
    crisp.text("key", "GRANDPA JOE'S", (cx, y0 + 135), 12, anchor="ms", spacing=0.6, bold=0.3)
    crisp.text("red", "LAST STOP", (cx, y0 + 154), 16.5, anchor="ms", spacing=0.8, bold=0.55)
    # the sign's own words: GAS (crossed out, as on the sign), ROCKS, LEMONADE
    gx, gy, gr = x0 + 18.5, y0 + 175, 12.5
    crisp.ring("key", gx, gy, gr, gr, 1.0)
    crisp.text("key", "GAS", (gx, gy + 4.5), 12, anchor="ms", bold=0.25)
    crisp.ring("red", gx, gy, gr - 1.6, gr - 1.6, 1.8)
    crisp.poly("red", slash(gx, gy, gr - 1.6, 1.8))
    crisp.text("key", "ROCKS", (x0 + 35, gy - 2.5), 12, anchor="ls", spacing=0.5, bold=0.25)
    crisp.text("key", "LEMONADE", (x0 + 35, gy + 11.5), 12, anchor="ls", spacing=0.0, bold=0.25)


def print_legend(broad, crisp):
    x0, y0, x1, y1 = LEGEND
    crisp.frame("key", x0, y0, x1, y1, 1.1)
    crisp.text("key", "LEGEND", (x0 + 8, y0 + 15), 12, anchor="ls", spacing=1.6, bold=0.3)
    rows = y0 + 30
    step = 14.0
    sx0, sx1 = x0 + 8, x0 + 26
    tx = x0 + 31
    entries = ["Highway", "Dirt road", "Dry lake", "Mountains", "Gas", "No gas"]
    for i, words in enumerate(entries):
        by = rows + i * step
        cy = by - 4.0
        if words == "Highway":
            crisp.line("red", [(sx0, cy), (sx1, cy)], 3.0)
        elif words == "Dirt road":
            crisp.dashed("key", [(sx0, cy), (sx1, cy)], 1.0, 3.6, 2.6)
        elif words == "Dry lake":
            pts = [(sx0 + 1, cy - 3.5), (sx1 - 2, cy - 4.2), (sx1, cy + 2.5), (sx0 + 4, cy + 4)]
            broad.poly("blue_tint", pts)
            crisp.dashed("blue", pts + [pts[0]], 0.8, 2.6, 1.8)
        elif words == "Mountains":
            mini = K.relief([dict(crest=[(sx0 + 1, cy + 1.0), (sx0 + 9, cy - 1.0), (sx1 - 1, cy + 0.5)], reach=[3, 5.5, 3], spurs=0, seed=77)], SEED + 78)
            broad.paste_mask("tan", blur(mini, 1.0) > 0.05)
            K.hachures(crisp, mini, "brown", step=0.22, spacing=2.4, seed=SEED + 79)
        elif words == "Gas":
            pump(crisp, (sx0 + sx1) / 2, cy + 0.5, 0.9)
        elif words == "No gas":
            no_gas(crisp, (sx0 + sx1) / 2, cy, 0.78)
        crisp.text("key", words, (tx, by), 12, anchor="ls")
    # the north arrow and the scale of miles, in the right-hand column
    nx_, ny_ = x1 - 32, y0 + 32
    crisp.poly("key", [(nx_, ny_ - 9), (nx_ + 4.2, ny_ + 6), (nx_, ny_ + 3.2)])
    crisp.poly("key", [(nx_, ny_ - 9), (nx_ - 4.2, ny_ + 6), (nx_, ny_ + 3.2)])
    crisp.poly("key", [(nx_, ny_ - 6.5), (nx_ - 2.6, ny_ + 3.0), (nx_, ny_ + 1.4)], 0)     # one half open, as compasses are
    crisp.line("key", [(nx_, ny_ - 9), (nx_ - 4.2, ny_ + 6), (nx_, ny_ + 3.2), (nx_, ny_ - 9)], 0.7)
    crisp.text("key", "N", (nx_, ny_ - 12), 12, anchor="ms", bold=0.3)
    per_mile = MILE_PX
    bar = 10 * per_mile
    bx0 = x1 - 8 - bar
    by = y1 - 22
    crisp.text("key", "MILES", (bx0 + bar / 2, by - 6), 12, anchor="ms", spacing=1.2)
    crisp.rect("key", bx0, by, bx0 + bar, by + 3.2)
    crisp.rect("key", bx0 + 0.6, by + 0.6, bx0 + 5 * per_mile, by + 2.6, 0)
    for k, lab in ((0, "0"), (5, "5"), (10, "10")):
        crisp.line("key", [(bx0 + k * per_mile, by - 1.5), (bx0 + k * per_mile, by + 4.6)], 0.8)
        crisp.text("key", lab, (bx0 + k * per_mile, by + 15), 12, anchor="ms")


def print_inset_frame(broad, crisp):
    x0, y0, x1, y1 = INSET
    crisp.frame("key", x0, y0, x1, y1, 1.6)
    crisp.frame("key", x0 + 3.2, y0 + 3.2, x1 - 3.2, y1 - 3.2, 0.6)
    crisp.text("key", INSET_TITLE, ((x0 + x1) / 2, y0 + 14.5), 12, anchor="ms", spacing=0.9, bold=0.25)
    crisp.line("key", [(x0 + 6, y0 + 18.5), (x1 - 6, y0 + 18.5)], 0.6, round_ends=False)
    crisp.text("key", "NOT TO SCALE", (x1 - 8, y1 - 7), 12, anchor="rs", spacing=0.8)


# ================================================================ the places
INNER_RIGHT = INSET[2] - 4.5                             # the right edge of the detail's drawing room
FENCE_X = INSET[2] - 32.0                                # the closed area's fence: its west side (x); fence_y() its corner


def lot_tint(p):
    """The lot and the desert round it, in a pale tan, everywhere in the detail but the road, the shack's inside and its
    hen yard (the store's), the strip of paper above them where the store's name is printed, the closed area beyond
    the fence, and a clean path from the lot in at the shop's door."""
    bx0, by0, bx1, by1 = SHACK_BOX
    p.rect("tan_tint", ROAD_BAND[1] + 0.6, by0 - 1.4, INNER_RIGHT, INNER_BOTTOM)       # (above it, the store's name)
    p.rect("tan_tint", bx0 + 1.0, by0 + 1.0, bx1 - 1.0, by1 - 1.0, 0)                 # the inside
    p.rect("tan_tint", HEN_YARD[0] - 1.0, HEN_YARD[1] - 1.0, bx0, HEN_YARD[3] + 1.0, 0)  # the hen yard
    p.rect("tan_tint", FENCE_X + 0.5, INNER_TOP + 2, INNER_RIGHT + 1, fence_y() - 0.5, 0)
    p.rect("tan_tint", DOOR_X - 6.5, by1 - 1.2, DOOR_X + 6.5, ARROW[0] + 4.0, 0)


def fence_y():
    return SHACK_BOX[3] + 18.0


def print_roadside(p):
    """The Last Stop: the lot in plan in the detail, and the No Gas sign on the highway of the main map."""
    lot_tint(p)
    # -- the road along the left of the lot: a red tint between two edges, its middle line knocked out in dashes
    rx0, rx1 = ROAD_BAND
    ry0, ry1 = INNER_TOP + 2, INNER_BOTTOM
    p.rect("red_tint", rx0, ry0, rx1, ry1)
    p.line("key", [(rx0, ry0), (rx0, ry1)], 0.9, round_ends=False)
    p.line("key", [(rx1, ry0), (rx1, ry1)], 0.9, round_ends=False)
    for a, b in K.dashes([((rx0 + rx1) / 2, ry0 + 2), ((rx0 + rx1) / 2, ry1)], 6, 5, 2):
        p.line("red_tint", [a, b], 1.4, 0, round_ends=False)
    # -- the shack: its walls (thick), the doors as gaps, the window as a thin double line; the porch along its front
    bx0, by0, bx1, by1 = SHACK_BOX
    t = 2.4
    fd0, fd1 = FRONT_DOOR[0], FRONT_DOOR[2]
    bd0, bd1 = BACK_DOOR[1], BACK_DOOR[3]
    wz0, wz1 = plan(0, SM.WINDOW[0])[0], plan(0, SM.WINDOW[1])[0]
    p.line("key", [(bx0, by0), (bx1, by0), (bx1, by1)], t)                    # the rear wall and the far end
    p.line("key", [(bx1, by1), (fd1, by1)], t)                               # the front, right of the door
    p.line("key", [(fd0, by1), (wz1, by1)], t)                               # the front between the window and the door
    p.line("key", [(wz0, by1), (bx0, by1), (bx0, bd1)], t)                   # the front left of the window, the yard end
    p.line("key", [(bx0, bd0), (bx0, by0)], t)                               # the yard end above the back door
    p.line("key", [(wz0, by1 - 0.9), (wz1, by1 - 0.9)], 0.6, round_ends=False)     # the window: two thin lines
    p.line("key", [(wz0, by1 + 0.9), (wz1, by1 + 0.9)], 0.6, round_ends=False)
    py = by1 + 7.0                                                           # the porch: boards, its edge, its posts
    for (a, b) in ((bx0 + 1.5, fd0 - 4.0), (fd1 + 4.0, bx1 - 1.5)):
        p.rect("tan_tint", a, by1 + 1.3, b, py, 0)
        p.rect("tan", a, by1 + 1.3, b, py - 0.3)
        for x in np.arange(a + 3.0, b - 1.0, 3.2):
            p.line("brown_tint", [(x, by1 + 1.5), (x, py - 0.5)], 0.4, round_ends=False)
        p.line("key", [(a, py), (b, py)], 0.7, round_ends=False)
    for x in (bx0 + 2.5, fd0 - 4.5, fd1 + 4.5, bx1 - 2.5):
        p.ellipse("key", x, py, 1.4, 1.4)
    # -- the sign at the road's edge, on its pole: GAS, crossed out
    sx, sy = rx1 + 10, by1 + 14
    p.ring("key", sx, sy - 2, 4.8, 4.8, 0.7)
    p.ring("red", sx, sy - 2, 3.9, 3.9, 1.1)
    p.poly("red", slash(sx, sy - 2, 3.9, 1.1))
    p.line("key", [(sx, sy + 2.8), (sx, sy + 10)], 1.0)
    # -- the gas pump, at the porch's right end: red, in a key outline, its lamp and its hose
    gx, gy = bx1 + 11, by1 + 10
    p.rect("red", gx - 3.2, gy - 4.2, gx + 3.2, gy + 4.2)
    p.frame("key", gx - 3.4, gy - 4.4, gx + 3.4, gy + 4.4, 0.8)
    p.ellipse("key", gx, gy - 6.3, 1.9, 1.7)
    p.ellipse("cream", gx, gy - 6.3, 0.9, 0.8)
    p.line("key", [(gx + 3.4, gy - 1.5), (gx + 6.2, gy + 0.5), (gx + 6.0, gy + 5.5), (gx + 3.8, gy + 7.2)], 0.8)
    # -- the lemonade stand and its umbrella (red and white, from above)
    ux, uy, ur = bx1 + 41, by1 + 27, 11.0
    p.rect("tan", ux - 14.2, uy + 5.8, ux + 14.2, uy + 12.2)
    p.frame("key", ux - 14.5, uy + 5.5, ux + 14.5, uy + 12.5, 0.7)
    for k in range(8):
        a0, a1 = k * math.pi / 4 - math.pi / 8, (k + 1) * math.pi / 4 - math.pi / 8
        wedge = [(ux, uy)] + [(ux + math.cos(a0 + (a1 - a0) * j / 6) * ur, uy + math.sin(a0 + (a1 - a0) * j / 6) * ur) for j in range(7)]
        if k % 2 == 0:
            p.poly("red", wedge)
        else:
            p.poly("key", wedge, 0)
            p.poly("red", wedge, 0)
            p.poly("tan_tint", wedge, 0)                                     # the white of the umbrella
    p.ring("key", ux, uy, ur, ur, 0.8)
    for k in range(8):
        a = k * math.pi / 4 - math.pi / 8
        p.line("key", [(ux, uy), (ux + math.cos(a) * ur, uy + math.sin(a) * ur)], 0.4)
    p.ellipse("key", ux, uy, 1.3, 1.3)
    # -- the fence: the closed area's west side and its corner, barbed wire as x's; its notice
    fx, fy = FENCE_X, fence_y()
    fence = [(fx, INNER_TOP + 3), (fx, fy), (INNER_RIGHT, fy)]
    p.line("key", fence, 1.0, round_ends=False)
    for (qx, qy) in along(fence, 5.6, 2.8):
        p.line("key", [(qx - 1.6, qy - 1.6), (qx + 1.6, qy + 1.6)], 0.6, round_ends=False)
        p.line("key", [(qx - 1.6, qy + 1.6), (qx + 1.6, qy - 1.6)], 0.6, round_ends=False)
    nx0 = fx + 9
    p.rect("tan_tint", nx0 - 0.5, fy - 5.5, nx0 + 12.5, fy + 4.5, 0)
    p.rect("key", nx0, fy - 5.0, nx0 + 12, fy + 4.0)
    p.rect("key", nx0 + 0.8, fy - 4.2, nx0 + 11.2, fy + 3.2, 0)
    p.rect("red", nx0 + 0.8, fy - 4.2, nx0 + 11.2, fy - 1.6)
    p.line("key", [(nx0 + 2.5, fy + 0.5), (nx0 + 9.5, fy + 0.5)], 0.5, round_ends=False)
    # -- the tire tracks: out from under the fence, and stopping in the middle of nothing; the glass where they stop
    tx = fx + 15
    stop_y = fy + 58
    for off in (-2.8, 2.8):
        p.dashed("key", [(tx + off, fy + 3.5), (tx + off - 2.2, stop_y)], 1.0, 3.2, 2.0)
    gl = [(tx - 9, stop_y + 4.5), (tx - 3, stop_y + 1.5), (tx + 6, stop_y + 2.5), (tx + 9.5, stop_y + 6.5), (tx + 4, stop_y + 10.5), (tx - 6, stop_y + 9.5)]
    p.poly("blue_tint", gl)
    p.line("blue", gl + [gl[0]], 0.8)
    # -- Mom's car, at the front by the road, from above
    car_plan(p, rx1 + 21, by1 + 74)
    # -- on the main map: the No Gas sign on the highway, where the Last Stop is, and a short dashed leader from it up
    #    to the detail's frame (this is the place the detail shows)
    (sx_, sy_), (sdx, sdy) = at_x(ROAD, K.LAST_STOP_T)
    no_gas(p, sx_ + 1, sy_ - 13, 1.0)
    p.dashed("key", [(sx_ + 3.0, sy_ - 21.5), (sx_ + 8.0, INSET[3] + 2.5)], 1.0, 2.4, 1.6)


def car_plan(p, cx, cy, L=30.0, Wd=13.5):
    """A small car seen from above, nose toward the road's way out (left): body, windscreen, back window, roof."""
    body = rounded(cx, cy, L / 2, Wd / 2, 3.4)
    p.poly("blue_tint", body)
    p.line("key", body + [body[0]], 0.8)
    p.poly("blue", rounded(cx - 5.0, cy, 2.1, Wd / 2 - 1.9, 0.8))             # the windscreen
    p.poly("blue", rounded(cx + 7.6, cy, 1.5, Wd / 2 - 2.3, 0.6))             # the back window
    p.poly("cream", rounded(cx + 1.4, cy, 3.6, Wd / 2 - 2.4, 1.0))            # the roof
    for sy in (-1, 1):
        p.line("key", [(cx - 9.6, cy + sy * (Wd / 2 - 0.4)), (cx - 11.4, cy + sy * (Wd / 2 + 1.6))], 0.8)   # its mirrors


def rounded(cx, cy, hw, hh, r, n=5):
    pts = []
    for (sx, sy, a0) in ((1, -1, -90), (1, 1, 0), (-1, 1, 90), (-1, -1, 180)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + sx * (hw - r) + math.cos(a) * r, cy + sy * (hh - r) + math.sin(a) * r))
    return pts


def print_store(p):
    """Grandpa Joe's store: its inside in plan, inside the shack's walls (from the store's model): the checkered floor,
    the hubcaps round the walls, the counter, the register, the grill, Harold the cooler, the shelves, the spinner, the
    rock bins, Jolene's chair, the hat pegs, the ceiling fan, the props by the door, the screen door open on the hen
    yard; and out back, the hen yard with five hens in a row."""
    bx0, by0, bx1, by1 = SHACK_BOX
    inner = (bx0 + 1.3, by0 + 1.3, bx1 - 1.3, by1 - 1.3)
    # -- the floor: cream and tan squares, as it is laid
    sq = 60.0 * K_CM
    for i, x in enumerate(np.arange(inner[0], inner[2], sq)):
        for j, y in enumerate(np.arange(inner[1], inner[3], sq)):
            if (i + j) % 2 == 0:
                p.rect("tan_tint", x, y, min(x + sq, inner[2]), min(y + sq, inner[3]))
    p.rect("tan_tint", DOOR_X - 6.5, ARROW[1] - 4.0, DOOR_X + 6.5, inner[3] + 0.5, 0)    # the mat inside the door

    def box(X0, X1, Z0, Z1, fill=None, outline=0.6):
        a = plan_box(X0, X1, Z0, Z1)
        p.rect("tan_tint", a[0] - 0.6, a[1] - 0.6, a[2] + 0.6, a[3] + 0.6, 0)
        if fill:
            p.rect(fill, a[0], a[1], a[2], a[3])
        if outline:
            p.frame("key", a[0], a[1], a[2], a[3], outline)
        return a
    # -- the hubcaps, high round the walls (on the plan, a row of small rings along the rear wall and the yard end;
    #    the red one is a tractor's wheel)
    caps = [(x, by0 + 3.6) for x in np.arange(bx0 + 6.0, bx1 - 4.0, 4.9)]
    tractor = len(caps) // 2 - 4
    for k, (x, y) in enumerate(caps):
        if k == tractor:
            p.ellipse("red", x, y + 0.6, 2.3, 2.3)
            p.ellipse("red", x, y + 0.6, 0.8, 0.8, 0)
            continue
        p.ring("key", x, y, 1.55, 1.55, 0.5)
        p.ellipse("key", x, y, 0.45, 0.45)
    # -- the counter (barn red), the grill at its end (cold) and the roller's rollers
    c = box(*SM.COUNTER[0:2], *SM.COUNTER[4:6], "red", 0.7)
    g = box(*SM.GRILL[0:2], *SM.GRILL[4:6], "key_tint", 0.7)
    for k in range(3):
        y = g[1] + 2.4 + k * 2.0
        p.line("key", [(g[0] + 1.8, y), (g[2] - 1.8, y)], 0.5, round_ends=False)
    r = plan_box(*SM.REGISTER[0:2], *SM.REGISTER[4:6])                          # the brass register
    p.rect("key", r[0] - 0.6, r[1] - 0.4, r[2] + 0.6, r[3] + 0.4)
    p.rect("key", r[0] + 0.6, r[1] + 0.8, r[2] - 0.6, r[3] - 0.8, 0)
    p.rect("tan", r[0] + 0.6, r[1] + 0.8, r[2] - 0.6, r[3] - 0.8)
    for (X, Z, rr) in ((SM.EGGS[0], SM.EGGS[3], SM.EGGS[4]), (SM.POSTCARDS[0], SM.POSTCARDS[3], SM.POSTCARDS[4]),
                       ((SM.PENNYDISH[0] + SM.PENNYDISH[1]) / 2, (SM.PENNYDISH[4] + SM.PENNYDISH[5]) / 2, 12.0)):
        q = plan(X, Z)
        p.ellipse("cream", q[0], q[1], max(1.3, rr * K_CM), max(1.3, rr * K_CM))
        p.ring("key", q[0], q[1], max(1.3, rr * K_CM), max(1.3, rr * K_CM), 0.45)
    m = plan_box(*SM.MAPRACK[0:2], *SM.MAPRACK[4:6])                            # the map rack (this map's)
    p.rect("tan_tint", m[0] - 0.4, m[1], m[2] + 1.4, m[3], 0)
    p.rect("key", m[0], m[1], m[2] + 1.0, m[3])
    b = plan((SM.BASKET[0] + SM.BASKET[1]) / 2, (SM.BASKET[4] + SM.BASKET[5]) / 2)      # Ranger's basket
    p.ellipse("tan_tint", b[0], b[1], 3.6, 3.6, 0)
    p.ellipse("tan", b[0], b[1], 2.9, 2.9)
    p.ring("key", b[0], b[1], 2.9, 2.9, 0.6)
    p.ring("brown", b[0], b[1], 1.6, 1.6, 0.45)
    # -- Harold the cooler (lemonade), the survival shelf with the TV on it, the auto shelf under the window
    h = box(*SM.COOLER[0:2], *SM.COOLER[4:6], "blue_tint", 0.7)
    p.line("key", [(h[2] - 1.5, h[1] + 1.2), (h[2] - 1.5, h[3] - 1.2)], 0.5, round_ends=False)
    box(*SM.SURVIVAL[0:2], *SM.SURVIVAL[4:6], "tan", 0.6)
    tv = plan_box(*SM.TV[0:2], *SM.TV[4:6])
    p.rect("key", tv[0] + 0.5, tv[1] + 0.5, tv[2] - 0.5, tv[3] - 0.5)
    box(*SM.AUTOSHELF[0:2], *SM.AUTOSHELF[4:6], "tan", 0.6)
    # -- the spinner rack of sunglasses
    sp = plan(SM.SPINNER[0], SM.SPINNER[1])
    rr = SM.SPINNER_R * K_CM + 0.8
    p.ellipse("tan_tint", sp[0], sp[1], rr + 0.8, rr + 0.8, 0)
    p.ellipse("blue_tint", sp[0], sp[1], rr, rr)
    p.ring("key", sp[0], sp[1], rr, rr, 0.8)
    for k in range(4):
        a = k * math.pi / 4
        p.line("key", [(sp[0] - math.cos(a) * rr, sp[1] - math.sin(a) * rr), (sp[0] + math.cos(a) * rr, sp[1] + math.sin(a) * rr)], 0.55)
    p.ellipse("key", sp[0], sp[1], 0.9, 0.9)
    # -- the rock bins: five bins, a few rocks in each
    rb = box(*SM.ROCKBINS[0:2], *SM.ROCKBINS[4:6], "tan", 0.7)
    rng = np.random.default_rng(SEED + 31)
    for k in range(5):
        y0_ = lerp(rb[1], rb[3], k / 5)
        y1_ = lerp(rb[1], rb[3], (k + 1) / 5)
        if k:
            p.line("key", [(rb[0], y0_), (rb[2], y0_)], 0.5, round_ends=False)
        for j in range(3):
            p.ellipse("brown", lerp(rb[0] + 2.0, rb[2] - 2.0, rng.random()), lerp(y0_ + 1.6, y1_ - 1.6, rng.random()), 1.0, 0.85)
    # -- Jolene's chair by the back door, the pay phone over it; the hat pegs and the bulletin board on the yard end
    box(*SM.CHAIR[0:2], *SM.CHAIR[4:6], "red_tint", 0.6)
    hb = plan_box(SM.HATRACK[0], SM.HATRACK[1], 0, 0)
    p.rect("tan_tint", hb[0] + 1.4, hb[1] - 2.6, hb[0] + 6.4, hb[3] + 2.6, 0)
    p.rect("tan", hb[0] + 1.6, hb[1] - 1.0, hb[0] + 3.4, hb[3] + 1.0)
    p.frame("key", hb[0] + 1.6, hb[1] - 1.0, hb[0] + 3.4, hb[3] + 1.0, 0.45)
    for k, X in enumerate(SM.HAT_PEGS):
        q = plan(X, 0)
        if k == 2:
            p.ellipse("key", q[0] + 3.0, q[1], 0.7, 0.7)                     # today's peg, empty
            continue
        p.ellipse("key", q[0] + 3.6, q[1], 2.2, 2.2)                         # a hat from above: brim and crown
        p.ellipse("key", q[0] + 3.6, q[1], 1.5, 1.5, 0)
        p.ellipse("red_tint" if k % 2 else "tan", q[0] + 3.6, q[1], 1.5, 1.5)
        p.ellipse("key", q[0] + 3.6, q[1], 0.6, 0.6)
    bb_ = plan_box(SM.BULLETIN[0], SM.BULLETIN[1], 0, 0)
    p.rect("tan_tint", bb_[0] + 5.0, bb_[1] - 0.6, bb_[0] + 8.2, bb_[3] + 0.6, 0)
    p.rect("tan", bb_[0] + 5.4, bb_[1], bb_[0] + 7.8, bb_[3])
    p.frame("key", bb_[0] + 5.4, bb_[1], bb_[0] + 7.8, bb_[3], 0.45)
    ph = plan_box(*SM.PAYPHONE[0:2], 0, 0)
    p.rect("key", ph[0] + 5.6, ph[1], ph[0] + 7.8, ph[3])
    # -- the ceiling fan, still since 1979 (overhead things are drawn dashed on a plan)
    fq = plan(SM.FAN[0], SM.FAN[2])
    p.ellipse("tan_tint", fq[0], fq[1], 6.6, 6.6, 0)
    for k in range(4):
        a = k * math.pi / 2 + 0.4
        p.line("key", [(fq[0] + math.cos(a) * 1.6, fq[1] + math.sin(a) * 1.6), (fq[0] + math.cos(a) * 5.6, fq[1] + math.sin(a) * 5.6)], 1.3)
        p.line("key", [(fq[0] + math.cos(a) * 2.4, fq[1] + math.sin(a) * 2.4), (fq[0] + math.cos(a) * 5.0, fq[1] + math.sin(a) * 5.0)], 0.5, 0)
    p.ellipse("key", fq[0], fq[1], 1.3, 1.3)
    # -- by the door: the water flats
    wf = box(SM.WATERFLATS[0], SM.WATERFLATS[1], SM.WATERFLATS[4], SM.WATERFLATS[5], "blue_tint", 0.6)
    for i in range(1, 3):
        p.line("key", [(lerp(wf[0], wf[2], i / 3), wf[1]), (lerp(wf[0], wf[2], i / 3), wf[3])], 0.4, round_ends=False)
    # -- the back door: the screen door hooked back inside, its swing, the step down to the yard
    bdx = bx0
    span = BACK_DOOR[3] - BACK_DOOR[1]
    hinge = (bdx + 1.2, BACK_DOOR[3])
    p.line("key", [hinge, (bdx + 1.2 + span * 0.92, BACK_DOOR[3] - 0.4)], 0.9)
    arc = [(bdx + 1.2 + math.cos(a) * span * 0.92, BACK_DOOR[3] - math.sin(a) * span * 0.92) for a in np.linspace(0.08, math.pi / 2, 12)]
    p.dashed("key", arc, 0.5, 1.6, 1.2)
    p.rect("tan", bdx - 6.0, BACK_DOOR[1] + 0.5, bdx - 1.6, BACK_DOOR[3] - 0.5)
    p.frame("key", bdx - 6.0, BACK_DOOR[1] + 0.5, bdx - 1.6, BACK_DOOR[3] - 0.5, 0.45)
    # -- the hen yard: its ground, chicken wire round it, five hens in a row facing its far side (as they face the fence)
    yx0, yy0, yx1, yy1 = HEN_YARD
    p.rect("tan_tint", yx0, yy0, yx1, yy1)
    p.rect("tan_tint", bdx - 6.5, BACK_DOOR[1], yx1 + 0.5, BACK_DOOR[3], 0)
    wire = [(yx1, yy0), (yx0, yy0), (yx0, yy1), (yx1, yy1)]
    p.dotted("key", wire, 0.6, 2.3)
    hx = yx0 + 8.0
    for k in range(5):
        hy = lerp(yy0 + 5.0, yy1 - 5.0, k / 4)
        p.ellipse("key", hx, hy, 2.3, 2.0)
        p.ellipse("cream", hx + 0.5, hy - 0.4, 1.0, 0.8)
        p.poly("red", [(hx - 1.8, hy - 0.8), (hx - 4.0, hy), (hx - 1.8, hy + 0.8)])      # a beak, toward the wire


HEN_YARD = (ROAD_BAND[1] + 9.0, SHACK_BOX[1] - 0.5, SHACK_BOX[0] - 1.5, BACK_DOOR[3] + 13.0)


def print_road(p):
    """On the road: the stretch of the highway beyond the Last Stop, picked out (a heavier line, edged), and a small
    printed limousine on it (gray, long, its windows down the side)."""
    s = cut(ROAD, *K.STRETCH)
    p.line("key", s, 7.2)
    p.line("key", s, 4.4, 0)
    p.line("red", s, 4.8)
    (cx, cy), (dx, dy) = at_x(ROAD, K.STRETCH[1] - 28)
    limo(p, cx, cy - 1.0, math.degrees(math.atan2(dy, dx)))


def limo(p, cx, cy, deg, L=42.0, Hh=9.0):
    """A long gray car, side on, nose to the right: cut out of the road under it, then printed."""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)

    def R(pts):
        return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]
    body = [(-L / 2, 2.0), (-L / 2, -1.8), (-L / 2 + 3.6, -2.8), (-L / 2 + 6.6, -Hh + 1.4), (L / 2 - 8.4, -Hh + 1.4),
            (L / 2 - 5.6, -3.2), (L / 2 - 0.6, -2.4), (L / 2, 2.0)]
    out = [(x * 1.08 + (0.6 if x > 0 else -0.6), y * 1.18 + 0.4) for x, y in body] + []
    p.poly("paper", R(out))
    for ink in ("red", "key"):
        p.poly(ink, R(out), 0)
    p.poly("key_tint", R(body))
    p.line("key", R(body + [body[0]]), 0.8)
    for wx0, wx1 in ((-L / 2 + 7.2, -L / 2 + 11.8), (-L / 2 + 13.0, -L / 2 + 17.6), (-L / 2 + 18.8, -L / 2 + 23.4),
                     (-L / 2 + 24.6, L / 2 - 9.0)):
        p.poly("key_tint", R([(wx0, -Hh + 2.6), (wx1, -Hh + 2.6), (wx1, -3.6), (wx0, -3.6)]), 0)
        p.poly("blue_tint", R([(wx0, -Hh + 2.6), (wx1, -Hh + 2.6), (wx1, -3.6), (wx0, -3.6)]))
    for wx in (-L / 2 + 5.4, L / 2 - 5.4):
        q = R([(wx, 2.0)])[0]
        p.ellipse("key", q[0], q[1], 2.5, 2.5)
        p.ellipse("key", q[0], q[1], 0.9, 0.9, 0)


def print_way(p):
    """The shop's door: a short printed arrow, from the lot in at the door."""
    x = DOOR_X
    y_tail, y_tip = ARROW
    p.line("red", [(x, y_tail), (x, y_tip + 6.5)], 1.9, round_ends=True)
    p.poly("red", [(x, y_tip), (x - 4.6, y_tip + 8.0), (x, y_tip + 6.2), (x + 4.6, y_tip + 8.0)])
    p.ellipse("red", x, y_tail, 2.4, 2.4)


# ================================================================ the scale of miles: measured on the printed road
def mile_px():
    seg = cut(ROAD, K.LAST_GAS_T, K.LAST_STOP_T)
    return path_length(seg) / K.MILES


MILE_PX = mile_px()


# ================================================================ painting
def under(alpha):
    """The paper: new in the middle of each panel, yellower toward the edges and on the cover; its grain; the light on
    its folds. Then the broad inks printed on it (the land's tints, the lakes, the cover's band)."""
    xx, yy = grid((H, W))
    pic = np.empty((H, W, 3), F32)
    pic[...] = K.PAPER
    big = noise((H, W), 150, SEED, 4) - 0.5
    fibre = noise((H, W), (70, 9), SEED + 1, 3) - 0.5
    pic *= (1 + 0.030 * big + 0.012 * fibre)[..., None]
    de = K.edge_distance(alpha)
    age = np.exp(-de / 16.0) * 0.55 + np.exp(-de / 60.0) * 0.18
    on_cover = blur(((xx < FOLDS_X[0]) & (yy < FOLDS_Y[0])).astype(F32), 3.0)
    age = age + on_cover * 0.22 * (0.6 + 0.8 * noise((H, W), 40, SEED + 2, 3))
    # the panels age unevenly: a little yellower where a panel was the outside of the folded map
    rng = np.random.default_rng(SEED + 3)
    edges = [SHEET[0]] + list(FOLDS_X) + [SHEET[2]]
    for i in range(len(edges) - 1):
        for j, (ya, yb) in enumerate(((SHEET[1], FOLDS_Y[0]), (FOLDS_Y[0], SHEET[3]))):
            inside = ((xx >= edges[i]) & (xx < edges[i + 1]) & (yy >= ya) & (yy < yb)).astype(F32)
            age += blur(inside, 2.0) * rng.random() * 0.07
    # the outside folds of the folded map (the mountain creases, and the middle one) carried the dirt of the pocket
    dirt = noise((H, W), (6, 6), SEED + 8, 3)
    for x, valley in zip(FOLDS_X, K.VALLEY_X):
        if not valley:
            age += np.exp(-((xx - x) / 5.0) ** 2) * (0.10 + 0.22 * dirt)
    for y in FOLDS_Y:
        age += np.exp(-((yy - y) / 5.0) ** 2) * (0.06 + 0.16 * dirt)
    pic = lerp(pic, K.PAPER_OLD[None, None, :], np.clip(age, 0, 1)[..., None])
    # a few broad soft patches where the paper has browned more than elsewhere (it was left in the sun, or in a glove box)
    for (px_, py_, rx_, ry_, k) in ((612, 520, 60, 26, 0.16), (120, 420, 46, 60, 0.12), (430, 190, 70, 40, 0.08)):
        d = np.hypot((xx - px_) / rx_, (yy - py_) / ry_) * (1 + (noise((H, W), 30, SEED + px_, 3) - 0.5) * 0.6)
        pic = lerp(pic, K.PAPER_OLD[None, None, :], (np.clip(1 - d, 0, 1) ** 1.5 * k)[..., None])
    # foxing: a few small brown spots
    for _ in range(14):
        fx, fy = rng.uniform(SHEET[0] + 10, SHEET[2] - 10), rng.uniform(SHEET[1] + 10, SHEET[3] - 10)
        r = rng.uniform(0.8, 2.2)
        d = np.hypot(xx - fx, yy - fy)
        pic = lerp(pic, mixp("yellow-ochre", "burnt-sienna", 0.4)[None, None, :], (np.exp(-(d / r) ** 2) * rng.uniform(0.15, 0.35))[..., None])
    return pic


def light_folds(pic):
    """The light on the folded sheet: each panel a little toward the light or away, each crease a fine line."""
    h = K.folds_height(SEED + 7)
    sh = K.shading(h)
    pic *= np.clip(1 + (sh - 1) * 0.85, 0.8, 1.15)[..., None]
    return pic


def creases(pic, alpha):
    """The creases themselves, crisp: a valley a fine shadow, a mountain a fine light with its shadow beside it; and
    where two cross, the paper rubbed pale and soft."""
    xx, yy = grid((H, W))
    shade = K.SHADE
    for m, valley, axis, at in K.crease_lines():
        if valley:
            pic[...] = lerp(pic, pic * shade[None, None, :] * 1.05, (m * 0.42)[..., None])
            side = np.roll(m, 1, axis=1 if axis == "x" else 0)
            pic[...] = lerp(pic, np.minimum(pic * 1.05, 1), (side * 0.35)[..., None])
        else:
            pic[...] = lerp(pic, np.minimum(pic * 1.10 + 0.02, 1), (m * 0.55)[..., None])
            side = np.roll(m, 1, axis=1 if axis == "x" else 0)
            pic[...] = lerp(pic, pic * shade[None, None, :] * 1.08, (side * 0.30)[..., None])
    n = noise((H, W), 4, SEED + 11, 3)
    for x in FOLDS_X:
        for y in FOLDS_Y:
            r = np.hypot(xx - x, yy - y)
            soft = np.exp(-(r / 5.5) ** 2) * (0.55 + 0.45 * n)
            pic[...] = lerp(pic, (K.WHITE * 0.98)[None, None, :], (soft * 0.55)[..., None])
    return pic


def sheet_edge(pic, alpha):
    """The paper's edge: a thin darker, browner rim, as old paper has."""
    rim = np.clip((1 - blur(alpha, 1.3)) * 2.4, 0, 1) * alpha
    pic[...] = lerp(pic, mixp(K.PAPER_OLD, "burnt-sienna", 0.25)[None, None, :], (rim * 0.5)[..., None])
    return pic


def paint_all():
    alpha = K.sheet_mask(SEED)
    wear = K.wear_mask(SEED + 41)
    lie = K.Lie(SEED + 61)

    # the sheet's own printing, broad (brushed) and crisp (restated after the brush)
    broad, crisp = Press(), Press()
    print_land(broad, crisp)
    print_panels(broad, crisp)

    pic = under(alpha)
    plain = creases(light_folds(pic.copy()), alpha)             # the paper with nothing printed on it (for knockouts)
    plain = sheet_edge(plain, alpha)
    K.print_layer(pic, broad, wear, lie)
    pic = light_folds(pic)
    if not FAST:
        flow = (noise((H, W), 90, SEED + 21, 3) - 0.5) * 0.5
        pic = strokes(np.clip(pic, 0, 1), sizes=(7, 4, 2), seed=SEED + 22, density=1.5, jitter=0.026, flow=flow, keep=0.50)
    K.print_layer(pic, crisp, wear, lie)
    pic = creases(pic, alpha)
    pic = sheet_edge(pic, alpha)
    back = np.clip(pic, 0, 1)

    # the places and the way: each printed on the finished sheet, alone
    layers = {}
    for name, fn in (("place-roadside", print_roadside), ("place-store", print_store), ("place-road", print_road),
                     ("path-roadside-store", print_way)):
        p = Press()
        fn(p)
        pic_l = back.copy()
        K.print_layer(pic_l, p, wear, lie, plain=plain)
        foot = presence(p, lie) * alpha
        layers[name] = (np.clip(pic_l, 0, 1), foot)
    return back, alpha, layers


def presence(press, lie):
    """Where a layer's ink is (before any wear): what its picture's cut-out keeps."""
    out = np.zeros((H, W), F32)
    for ink in press.inks():
        out = np.maximum(out, K.register(lie(press.cover(ink)), ink))
    if "paper" in press.plates:
        out = np.maximum(out, lie(press.cover("paper")))
    return out


KEEP = 0.12          # a pixel belongs to a place's picture where its ink covers more than this (its colour is the sheet's
                     # with that much ink on it, so a thin line keeps its soft edge instead of breaking up)


def finish(back, alpha, layers):
    """Grain, one palette for the whole map (the sheet with every place and way on it), each file reduced to it."""
    os.makedirs(OUT, exist_ok=True)
    g = grain(np.zeros((H, W, 3), F32) + 0.5, SEED + 90, 0.010) - 0.5      # one grain for every file, pixel for pixel
    full = back.copy()
    for name, (pic_l, foot) in layers.items():
        m = (foot > KEEP)[..., None]
        full = np.where(m, pic_l, full)
    full_g = np.clip(full + g, 0, 1)
    # the sample: the whole sheet, and the printed things again (lines and lettering are few pixels, and must keep
    # their own colours), so that small inks are not lost among the paper's many tones
    sheet_px = full_g[alpha > 0.5]
    ink_mask = (np.abs(full - blur(full, 3.0)).sum(axis=2) > 0.06) & (alpha > 0.5)
    places_px = np.concatenate([full_g[(foot > KEEP)] for _, foot in layers.values()])
    pal = palette_of([sheet_px, full_g[ink_mask], places_px, places_px], colors=200, seed=SEED + 91)
    sizes = {}
    idx_back = to_palette(np.clip(back + g, 0, 1), pal, seed=SEED + 92, speckle=0.010)
    path = os.path.join(OUT, "back.png")
    save(path, idx_back, pal, alpha)
    sizes["back.png"] = os.path.getsize(path)
    for name, (pic_l, foot) in layers.items():
        idx = to_palette(np.clip(pic_l + g, 0, 1), pal, seed=SEED + 92, speckle=0.010)
        path = os.path.join(OUT, name + ".png")
        save(path, idx, pal, (foot > KEEP).astype(F32))
        sizes[name + ".png"] = os.path.getsize(path)
    return pal, sizes


def main():
    back, alpha, layers = paint_all()
    pal, sizes = finish(back, alpha, layers)
    total = sum(sizes.values())
    for k, v in sizes.items():
        print(f"  {k}: {v / 1024:.0f} KB")
    print(f"map-nevada: {len(pal)} colours, {total / 1024:.0f} KB in all{' (fast: no brush pass)' if FAST else ''}")
    if "nolayout" in sys.argv:
        return
    import map_nevada_layout
    map_nevada_layout.write(OUT)
    if "nocheck" not in sys.argv:
        import map_nevada_check
        map_nevada_check.run(OUT)


if __name__ == "__main__":
    main()

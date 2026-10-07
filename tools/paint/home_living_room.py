"""The family's living room, 9:40 at night, the present day.

THE PICTURE'S IDEA: home at night. Three warm pools of lamplight, a cold blue window, and two places
at the table that nobody is sitting at.

LIGHT (kept to everywhere): night, so nothing comes from the sky. The room is lit by its own three
shaded lamps, each a warm pool of light that falls DOWNWARD and outward from it: the pendant over
the dining table (left front), the reading lamp behind Dad's armchair (right front; it also throws a
disc up onto the ceiling), the small lamp on the piano (back wall, right of the middle: it lights the
family photographs). Whatever no lamp reaches is cool blue-violet, darkest in the ceiling and the far
corners. Two cold notes: the window on the street, and the monitor. Every thing that stands on the
floor throws its shadow away from the lamp nearest it (chairs outward from under the pendant, and so on).

HOW IT IS LAID OUT (800 x 600; horizon -150, full 585; the back wall meets the floor at row 385):
  ceiling    rows 0 to 130: plain plaster in shadow, the lamp's chain coming down from its rose.
  back wall  rows 130 to 385. Up in the dim, a shelf of the family's treasures along the picture rail.
             Then left to right: the front door (cream, two frosted lights) | the wide window on the
             night street, blue curtains | the wall clock at twenty to ten and a cork board, over the
             desk with the family computer | the bookcase | the family photographs, over the piano |
             the stairs going up to the right, the closet door under them standing a little open.
  floor      rows 385 to 600: boards, the red rug in the middle where the three of them stand;
             LEFT FRONT the dining table under its pendant lamp, set for five, two places untouched;
             RIGHT FRONT Dad's armchair, his reading lamp and his slippers. An aspidistra at the
             bottom left corner is the front plane.

THE THREE TONES: dark = ceiling, the upper wall and the corners of the floor (cool blue-violet);
middle = the lit wall and floor; light = the tablecloth under its lamp, the lampshades, the wall
over the piano.

HOW IT IS MADE: as STYLE.md says, in four passes (under-painting, brush, crisp details, grain and a
limited palette). Because this is a room, the under-painting is not blocked in by hand: every surface
has a local color and is lit by the three lamps where it stands (see _kit and _plan), which is what
keeps the pools of light, the shadows and the furniture in agreement.
Scripts: _kit (camera, lamps, lit faces, shadows), _plan (where everything is; the lamps), _room (the
backdrop's under-painting), _fine (the backdrop's crisp small things), _things (the cut-outs), this file
(putting it together, the screen and the note, finishing, the layout), _check (pictures for checking)."""

import json, os, sys, time
import numpy as np
from PIL import Image
from brush import *
from home_living_room_plan import *
import home_living_room_room as room
import home_living_room_things as things
import home_living_room_fine as fine

OUT = "out/home-living-room"
NAMES = {"desk": things.desk, "piano": things.piano, "table": things.table, "armchair": things.armchair}


def brushed(pic, fast, box=None, seed=2, keep=0.30, sizes=(9, 5, 2), fine=0.75):
    """The brush pass over a crisp under-painting, and then what the brush took away put back: the hard
    edges nearly whole, and the fine lines (board joints, stripes, patterns) at `fine` of their strength,
    so it is brushwork between crisp drawing and not a blur. `box` limits it to part of the picture."""
    if fast:
        return pic.copy()

    def one(part):
        b = strokes(part, sizes=sizes, seed=seed, density=1.5, jitter=0.048, keep=keep)
        b = lerp(b, part, edge_weight(part)[..., None])
        return np.clip(b + (part - blur(part, 1.3)) * fine, 0, 1)
    if box is None:
        return one(pic)
    x0, y0, x1, y1 = box
    out = pic.copy()
    out[y0:y1, x0:x1] = one(pic[y0:y1, x0:x1])
    return out


def paint(fast=False, t0=None):
    t0 = t0 or time.time()
    L, info = room.backdrop(things.PIECES)
    save_rgb(L.rgb, OUT + "-1-under.png")
    print("under", round(time.time() - t0, 1), flush=True)
    back = Layer(brushed(L.rgb, fast, keep=0.30))
    print("brushed", round(time.time() - t0, 1), flush=True)
    fine.details(back, info)
    cuts = {}
    for name, piece in NAMES.items():
        C = Layer()
        piece(C, False)
        comp = back.rgb.copy()
        over(comp, C.true(), C.w)
        ys, xs = np.nonzero(C.w > 0.02)
        box = (max(0, xs.min() - 12), max(0, ys.min() - 12), min(W, xs.max() + 13), min(H, ys.max() + 13))
        D = Layer(brushed(comp, fast, box=box, seed=7, keep=0.40, sizes=(7, 4, 2)))
        D.a = C.w.copy()
        piece(D, True)
        cuts[name] = D
        print(name, round(time.time() - t0, 1), flush=True)
    return back, cuts, info


def save_rgb(a, path):
    Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).save(path)


def whole(back, cuts, order=("desk", "piano", "armchair", "table")):
    pic = back.rgb.copy()
    for n in order:
        over(pic, cuts[n].rgb, (cuts[n].a > 0.5).astype(F32))
    return pic


# ---------------------------------------------------------------- the monitor's screen, and Dad's note
def screen_box():
    a = P(SCR["x0"], SCR["y1"], MON["z"] - 0.3)
    b = P(SCR["x1"], SCR["y0"], MON["z"] - 0.3)
    return a[0], a[1], b[0], b[1]


def screen(kind):
    """What the monitor shows, as a cut-out the size of the picture: only the lit glass.
    offline: grey, a broken link.  login: blue, a white box for four figures.  map: a pale map and a red dot."""
    x0, y0, x1, y1 = screen_box()
    w, h = x1 - x0, y1 - y0
    s = Sheet(SHAPE)

    def r(u0, v0, u1, v1, c, a=1.0):
        s.poly([(x0 + u0 * w, y0 + v0 * h), (x0 + u1 * w, y0 + v0 * h), (x0 + u1 * w, y0 + v1 * h), (x0 + u0 * w, y0 + v1 * h)], c, a)

    def at(u, v):
        return (x0 + u * w, y0 + v * h)
    if kind == "offline":
        r(0, 0, 1, 1, "#39455a")
        r(0, 0, 1, 0.13, "#1c2636")
        r(0.03, 0.03, 0.09, 0.10, "#ff6b5a")
        r(0.33, 0.27, 0.45, 0.50, "#8796ac")                             # two halves of a plug that do not meet
        r(0.55, 0.27, 0.67, 0.50, "#8796ac")
        s.line([at(0.45, 0.33), at(0.49, 0.33)], "#8796ac", 0.8)
        s.line([at(0.45, 0.44), at(0.49, 0.44)], "#8796ac", 0.8)
        s.line([at(0.46, 0.20), at(0.54, 0.57)], "#ff6b5a", 1.3)
        r(0.24, 0.66, 0.76, 0.74, "#d5dde8")
        r(0.32, 0.82, 0.68, 0.87, "#8796ac")
    elif kind == "login":
        r(0, 0, 1, 1, "#2a5a8c")
        r(0, 0, 1, 0.13, "#16283d")
        r(0.03, 0.03, 0.09, 0.10, "#ff6b5a")
        r(0.30, 0.22, 0.70, 0.29, "#cfe3ff")
        r(0.20, 0.40, 0.80, 0.68, "#ffffff")                             # four figures wanted
        for k in range(4):
            r(0.27 + k * 0.125, 0.58, 0.35 + k * 0.125, 0.62, "#6a86a8")
        r(0.36, 0.80, 0.64, 0.85, "#ffe9a8")
    else:
        r(0, 0, 1, 1, "#ece4c8")
        for k in range(1, 6):
            s.line([at(k / 6, 0.13), at(k / 6, 1)], "#d3c9a8", 0.6, 0.8)
        for k in range(1, 4):
            s.line([at(0, 0.13 + k * 0.22), at(1, 0.13 + k * 0.22)], "#d3c9a8", 0.6, 0.8)
        s.line(curve([at(0.0, 0.92), at(0.22, 0.80), at(0.42, 0.62), at(0.62, 0.52)], 8), "#b9aa8a", 1.4)
        s.ellipse(*at(0.80, 0.34), w * 0.10, h * 0.06, "#cfe2e4")        # a dry lake
        for (u, v) in ((0.16, 0.36), (0.36, 0.30)):                      # hills
            s.line([at(u, v + 0.06), at(u + 0.04, v - 0.04), at(u + 0.08, v + 0.06)], "#b9aa8a", 0.8)
        r(0, 0, 1, 0.13, "#16283d")
        r(0.03, 0.03, 0.09, 0.10, "#ff6b5a")
        r(0.50, 0.66, 0.96, 0.94, "#ffffff")
        s.line([at(0.50, 0.66), at(0.96, 0.66), at(0.96, 0.94), at(0.50, 0.94), at(0.50, 0.66)], "#c8402f", 0.6)
        r(0.54, 0.72, 0.80, 0.77, "#c8402f")
        r(0.54, 0.82, 0.92, 0.86, "#7a6f55")
        s.ellipse(*at(0.63, 0.50), 4.2, 4.2, "#ff6b5a", 0.4)
        s.ellipse(*at(0.63, 0.50), 2.3, 2.3, "#c8402f")
        s.ellipse(*at(0.63, 0.50), 0.8, 0.8, "#ffffff")
    c, a = s.done()
    box = mask_poly(SHAPE, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
    px, py = grid(SHAPE)
    c = c * (1 - 0.22 * np.clip(((px - (x0 + x1) / 2) / (w / 2)) ** 2 * 0.5 + ((py - (y0 + y1) / 2) / (h / 2)) ** 2 * 0.5, 0, 1))[..., None]   # dimmer at the corners, as these screens are
    return c.astype(F32), box


def note():
    """The yellow sticky note on the corner of the monitor."""
    z = MON["z"] - 0.5
    xa, xb, ya, yb = MON["x1"] - 15.5, MON["x1"] - 1.0, MON["y1"] - 15.0, MON["y1"] - 1.0
    q = [(xa + 0.8, ya - 0.6, z), (xb + 0.6, ya + 0.6, z), (xb, yb + 0.4, z), (xa, yb, z)]             # stuck on a little crooked
    s = Sheet(SHAPE)
    s.poly(pts2([(x + 1.6, y - 1.6, zz) for x, y, zz in q]), "#06080c", 0.45)
    body = lit("#ffe36b", (xa, ya, z), (0, 0, -1), 2.1)
    s.poly(pts2(q), body)
    s.poly(pts2([q[3], q[2], (q[2][0], q[2][1] - 3.4, z), (q[3][0], q[3][1] - 3.4, z)]), body * col("#f6d258"))
    s.poly(pts2([q[0], (q[0][0] + 4, q[0][1], z), (q[0][0], q[0][1] + 4, z)]), body * col("#d9b83c"))    # a corner curling up
    for k in range(3):
        yy = yb - 5.6 - k * 2.9
        s.line(pts2([(xa + 2.2, yy, z), (xb - 2.0 - (k == 2) * 4, yy + 0.3, z)]), "#6b5a1c", 0.6, 0.85)
    return s.done()


# ---------------------------------------------------------------- finishing: grain, a limited palette, the files
def grade(c, sat=1.13, con=1.05):
    """The last look over the whole picture: color a little richer, darks a little deeper. The same for
    every layer, so the cut-outs still match the backdrop."""
    lum = (c @ np.array([0.3, 0.55, 0.15], dtype=F32))[..., None]
    c = lum + (c - lum) * sat
    return np.clip((c - 0.45) * con + 0.45, 0, 1).astype(F32)


def soft_grain(picture, seed, amount):
    """Pigment grain like brush.grain, but lighter in the dark: by lamplight most of the picture is dim, and
    even grain there reads as dirt."""
    h, w, _ = picture.shape
    rng = np.random.default_rng(seed)
    fine = rng.normal(0, 1, (h, w)).astype(F32)
    coarse = blur(rng.normal(0, 1, (h, w)).astype(F32), 0.8) * 1.6
    lum = picture @ np.array([0.3, 0.55, 0.15], dtype=F32)
    k = amount * (0.40 + 1.0 * lum)
    return np.clip(picture + ((fine * 0.7 + coarse * 0.6) * k)[..., None], 0, 1)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.007, amount=0.017, care=()):
    """Grain, then a limited palette with a little speckle, then the file. `care` lists rectangles
    (x0, y0, x1, y1, times) whose colors must not be lost though they are small (photographs, books, the
    table): they are counted several times over when the palette is chosen."""
    g = soft_grain(grade(picture), seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    chosen = [sample_of.reshape(-1, 1, 3)]
    for (x0, y0, x1, y1, times) in care:
        chosen += [g[y0:y1, x0:x1].reshape(-1, 1, 3)] * times
    pal = palette_of(chosen, colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def rect_of(points, pad=0):
    """The picture rectangle [x, y, w, h] round some places in the room."""
    pp = [P(*p) for p in points]
    x0, x1 = min(p[0] for p in pp) - pad, max(p[0] for p in pp) + pad
    y0, y1 = min(p[1] for p in pp) - pad, max(p[1] for p in pp) + pad
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    return [int(round(x0)), int(round(y0)), int(round(x1 - x0)), int(round(y1 - y0))]


def floor_poly(points, grow_by=0.0):
    """A patch of floor (corners given in cm) as a picture outline."""
    pp = hull([P(x, 0.0, z) for x, z in points])
    if grow_by:
        pp = grow(pp, grow_by)
    return [[int(round(min(max(x, 0), W))), int(round(min(max(y, 0), H)))] for x, y in pp]


def feet(x, z):
    p = P(x, 0.0, z)
    return [int(round(p[0])), int(round(p[1]))]


def layout(bases):
    d, w, t, st, c = DOOR, WIN, TABLE, STAIR, CLOSET
    a = things.Turned(ARM["cx"], ARM["cz"], ARM["ang"])
    wall = lambda x0, x1, y0, y1, pad=0: rect_of([(x0, y0, ZW), (x1, y1, ZW)], pad)
    stair_top = lambda n: (room.stair_x(n), st["rise"] * n, st["z0"])
    N = st["steps"]
    sx0, sx1 = (PIANO["x0"] + PIANO["x1"]) / 2 - 36, (PIANO["x0"] + PIANO["x1"]) / 2 + 34
    chair = things.Turned(-58.0, DESK["z0"] - 52.0, 26.0)
    arm_foot = [(a.p(lx, 0, lz)[0], a.p(lx, 0, lz)[2]) for lx, lz in ((-47, -44), (47, -44), (47, 44), (-47, 44))]
    side_table = a.p(72, 0, -8)
    blocked = [
        floor_poly([(DESK["x0"], DESK["z0"]), (DESK["x1"], DESK["z0"]), (DESK["x1"], ZW), (DESK["x0"], ZW)], 3),
        floor_poly([(chair.p(lx, 0, lz)[0], chair.p(lx, 0, lz)[2]) for lx, lz in ((-28, -34), (28, -34), (28, 30), (-28, 30))], 2),
        floor_poly([(BOOKS["x0"], BOOKS["z0"]), (BOOKS["x1"], BOOKS["z0"]), (BOOKS["x1"], ZW), (BOOKS["x0"], ZW)], 3),
        floor_poly([(PIANO["x0"], PIANO["keys"]), (PIANO["x1"], PIANO["keys"]), (PIANO["x1"], ZW), (PIANO["x0"], ZW)], 3),
        floor_poly([(sx0, PIANO["z0"] - 92), (sx1, PIANO["z0"] - 92), (sx1, PIANO["z0"] - 58), (sx0, PIANO["z0"] - 58)], 2),
        floor_poly([(st["x0"] - 16, st["z0"] - 10), (640, st["z0"] - 10), (640, ZW), (st["x0"] - 16, ZW)], 3),
        floor_poly([(t["x0"] - 26, t["z0"] - 60), (t["x1"] + 8, t["z0"] - 60), (t["x1"] + 22, t["z1"] + 62), (t["x0"] - 8, t["z1"] + 66)], 3),
        floor_poly(arm_foot + [(FLOORLAMP[0] - 14, FLOORLAMP[2] - 12), (FLOORLAMP[0] + 14, FLOORLAMP[2] + 12), (side_table[0] - 20, side_table[2] - 18), (side_table[0] + 20, side_table[2] - 18), (side_table[0] + 20, side_table[2] + 18)], 3),
        floor_poly([(-420, ZW - 32), (-384, ZW - 32), (-384, ZW), (-420, ZW)], 2),
        floor_poly([(-606, ZW - 28), (-580, ZW - 28), (-580, ZW), (-606, ZW)], 2),
        floor_poly([(-188, ZW - 28), (-162, ZW - 28), (-162, ZW), (-188, ZW)], 2),
        floor_poly([(-440, -20), (-388, -20), (-388, 18), (-440, 18)], 2),
    ]
    sb = screen_box()
    nq = [P(MON["x1"] - 15.5, MON["y1"] - 15, MON["z"]), P(MON["x1"], MON["y1"], MON["z"])]
    data = {
        "id": "home-living-room", "size": [W, H], "horizon": HZ, "full": FULL,
        "light": "night: three lamps (pendant over the table left front, reading lamp right front, small lamp on the piano); cool from the window and the monitor",
        "wallMeetsFloor": WALL_Y,
        "walk": [[8, 393], [792, 393], [792, 598], [8, 598]],
        "blocked": blocked,
        "planes": [
            {"id": "desk", "file": "desk.png", "base": bases["desk"], "what": "desk, chair and computer, the screen dark",
             "baseNote": "the base is the front of the desk; the chair stands out in front of it (down to row 458) and has its own outline in blocked"},
            {"id": "screen", "base": bases["desk"] + 1, "states": {"offline": "screen-offline.png", "login": "screen-login.png", "map": "screen-map.png"},
             "what": "the lit screen, laid over the dark one: grey with a broken link / blue with a box for four figures / a pale map with a red dot"},
            {"id": "note", "file": "note.png", "base": bases["desk"] + 2, "what": "the yellow sticky note on the monitor's corner: shown until it is taken"},
            {"id": "piano", "file": "piano.png", "base": bases["piano"], "what": "piano, its lamp and its stool",
             "baseNote": "the base is the piano's front legs; the stool stands out in front of it (down to row 462) and has its own outline in blocked"},
            {"id": "armchair", "file": "armchair.png", "base": bases["armchair"], "what": "Dad's armchair, the reading lamp behind it, the little table, his slippers"},
            {"id": "table", "file": "table.png", "base": bases["table"], "what": "the dining table, all five chairs, and the pendant lamp on its chain"},
            {"id": "front", "file": "front.png", "plane": "front", "what": "the aspidistra at the bottom left corner"},
        ],
        "things": [
            {"id": "door", "what": "the front door", "shape": {"rect": wall(d["x0"], d["x1"], 0, d["top"])}, "stand": feet(-518, ZW - 34), "face": "N"},
            {"id": "window", "what": "the window on the street", "shape": {"rect": wall(w["x0"] - 34, w["x1"] + 34, w["y0"] - 8, POLE + 4)}, "stand": feet(-368, ZW - 44), "face": "N"},
            {"id": "computer", "what": "the family computer on the desk", "shape": {"rect": rect_of([(DESK["x0"], 0, DESK["z0"]), (DESK["x1"], MON["y1"], ZW), (DESK["x1"], DESK["top"], DESK["z0"]), (DESK["x0"], MON["y1"], MON["z"])])}, "stand": feet(-118, DESK["z0"] - 22), "face": "N"},
            {"id": "note", "what": "the sticky note on the monitor", "shape": {"rect": [int(nq[0][0]) - 3, int(nq[1][1]) - 3, int(nq[1][0] - nq[0][0]) + 7, int(nq[0][1] - nq[1][1]) + 7]}, "stand": feet(-118, DESK["z0"] - 22), "face": "NE"},
            {"id": "books", "what": "the bookcase", "shape": {"rect": rect_of([(BOOKS["x0"], 0, BOOKS["z0"]), (BOOKS["x1"], BOOKS["top"], ZW), (BOOKS["x1"], 0, BOOKS["z0"])])}, "stand": feet(71, BOOKS["z0"] - 26), "face": "N"},
            {"id": "piano", "what": "the piano", "shape": {"rect": rect_of([(PIANO["x0"], 0, PIANO["keys"]), (PIANO["x1"], PIANO["top"], ZW), (PIANO["x1"], 0, PIANO["keys"])])}, "stand": feet((PIANO["x0"] + PIANO["x1"]) / 2 + 2, PIANO["z0"] - 100), "face": "N"},
            {"id": "photo", "what": "the family photograph over the piano", "shape": {"rect": wall(PHOTO["x0"], PHOTO["x1"], PHOTO["y0"], PHOTO["y1"], 2)}, "stand": feet(PIANO["x0"] + 20, PIANO["z0"] - 100), "face": "N"},
            {"id": "stairs", "what": "the stairs", "shape": {"poly": [[min(W, int(round(P(*q)[0]))), int(round(P(*q)[1]))] for q in ((st["x0"] - 16, 0, st["z0"] - 9), (st["x0"] - 16, 126, st["z0"] - 9), (room.stair_x(4), 72 + 92, st["z0"]), (555, 18 * 10 + 96, st["z0"]), (555, 18 * 8.4, st["z0"]), (st["x0"] + 112, 0, st["z0"]))]}, "stand": feet(st["x0"] - 26, st["z0"] - 30), "face": "NE"},
            {"id": "closet", "what": "the closet under the stairs", "shape": {"rect": rect_of([(c["x0"] - 4, 0, st["z0"] - c["ajar"]), (c["x1"] + 4, c["top"] + 4, st["z0"])])}, "stand": feet(c["x0"] - 6, st["z0"] - 26), "face": "NE"},
            {"id": "table", "what": "the dinner table", "shape": {"rect": rect_of([(t["x0"], 50, t["z0"]), (t["x1"], t["top"] + 26, t["z1"]), (t["x1"], t["top"], t["z0"]), (t["x0"], t["top"], t["z1"])])}, "stand": feet(t["x1"] + 52, (t["z0"] + t["z1"]) / 2 - 8), "face": "W"},
            {"id": "armchair", "what": "Dad's armchair", "shape": {"rect": rect_of([a.p(lx, y, lz) for lx in (-47, 47) for lz in (-44, 44) for y in (0, 104)])}, "stand": feet(*[(a.p(-78, 0, -34)[0], a.p(-78, 0, -34)[2])][0]), "face": "E"},
        ],
        "exits": [{"to": "nevada-roadside", "shape": {"poly": [[int(round(v)) for v in wp_] for wp_ in (P(d["x0"], 0, ZW), P(d["x1"], 0, ZW), P(d["x1"], d["top"], ZW), P(d["x0"], d["top"], ZW))]}, "stand": feet(-518, ZW - 34)}],
        "marks": {"mom": feet(24, 112), "bigsis": feet(140, 140), "lilsis": feet(-66, 126)},
        "extras": {
            "scripted": {"closetIn": feet(c["x0"] + 8, st["z0"] - 6), "pianoStool": feet((PIANO["x0"] + PIANO["x1"]) / 2 - 1, PIANO["z0"] - 75),
                         "what": "places a script may send someone that are not on the walkable floor: the foot of the closet's gap (the youngest goes in here), the middle of the piano stool"},
            "screen": {"rect": [int(round(sb[0])), int(round(sb[1])), int(round(sb[2] - sb[0])), int(round(sb[3] - sb[1]))]},
            "routerLed": [int(round(v)) for v in P(c["x0"] + 3.5, 30, st["z0"] + 6)],
            "closetGap": {"rect": rect_of([(c["x0"], 0, st["z0"]), (c["x0"] + 9, c["top"], st["z0"] - c["ajar"])])},
            "lamps": {"pendant": [int(round(v)) for v in P(*PENDANT)], "reading": [int(round(v)) for v in P(*FLOORLAMP)], "piano": [int(round(v)) for v in P(*PIANOLAMP)]},
            "clock": "the wall clock shows 9:40",
        },
    }
    return data


def bases():
    """The picture row where each cut-out meets the floor (people whose feet are above it go behind)."""
    a = things.Turned(ARM["cx"], ARM["cz"], ARM["ang"])
    tb = a.p(72, 0, -8)
    return {
        "desk": int(round(P(0, 0, DESK["z0"])[1])) + 1,                                   # the front of the desk (its chair stands out past this: see blocked)
        "piano": int(round(P(0, 0, PIANO["keys"] + 2)[1])) + 1,                           # the legs under the keyboard (the stool stands out past this)
        "armchair": int(round(max(P(0, 0, tb[2] - 15)[1], P(0, 0, a.p(47, 0, -44)[2])[1]))) + 1,
        "table": int(round(P(0, 0, TABLE["z0"] - 36 - 21)[1])) + 1,                       # the feet of the two near chairs
    }


def write_files(L):
    """Finish every layer and write the files. Every layer gets the same slight wander of the hand, so
    they still fit one another to the pixel."""
    care = [(100, 215, 300, 335, 3), (300, 235, 400, 300, 3), (400, 235, 500, 400, 2), (500, 190, 760, 300, 4)]       # window, clock and board, books, photographs
    print("back", finish(hand(L["back"]), OUT + "/back.png", 160, care=care), flush=True)
    for name, colors in (("desk", 72), ("piano", 64), ("table", 88), ("armchair", 80)):
        rgb_, a_ = hand(L[name]), hand(L[name + "_a"])
        if name == "table":
            things.chain(rgb_, a_)
        print(name, finish(rgb_, f"{OUT}/{name}.png", colors, a_, seed=11), flush=True)
    for k in ("offline", "login", "map"):
        print(k, finish(hand(L["screen_" + k]), f"{OUT}/screen-{k}.png", 24, hand(L["screen_" + k + "_a"]), seed=13, speckle=0.005, amount=0.010), flush=True)
    print("note", finish(hand(L["note"]), OUT + "/note.png", 12, hand(L["note_a"]), seed=13, speckle=0.004, amount=0.008), flush=True)
    print("front", finish(hand(L["front"]), OUT + "/front.png", 40, hand(L["front_a"]), seed=17), flush=True)
    import subprocess
    subprocess.run([sys.executable, "comp.py", OUT, "back", "desk", "screen-offline", "note", "piano", "armchair", "table", "front"], check=True)


if __name__ == "__main__":
    # python3 home_living_room.py          everything (about three minutes)
    # python3 home_living_room.py fast     no brush pass and no files: only out/home-living-room-2-all.png, to look at
    # python3 home_living_room.py finish   finish again from the layers kept by the last full run
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    if "finish" in sys.argv:
        write_files({k: v.astype(F32) for k, v in np.load(OUT + "-layers.npz").items()})
        print("done", round(time.time() - t0, 1))
        sys.exit()
    fast = "fast" in sys.argv
    back, cuts, info = paint(fast, t0)
    scr = {k: screen(k) for k in ("offline", "login", "map")}
    nt = note()
    fr = things.front_plane()
    things.chain(cuts["table"].rgb, cuts["table"].a)
    pic = back.rgb.copy()
    over(pic, cuts["desk"].rgb, (cuts["desk"].a > 0.5).astype(F32))
    over(pic, scr["offline"][0], scr["offline"][1])
    over(pic, nt[0], nt[1])
    for n in ("piano", "armchair", "table"):
        over(pic, cuts[n].rgb, (cuts[n].a > 0.5).astype(F32))
    under_front = pic.copy()                                   # the plant in front is brushed where it stands, like the rest
    over(under_front, fr[0], fr[1])
    ys, xs = np.nonzero(fr[1] > 0.02)
    fr = (brushed(under_front, fast, box=(max(0, xs.min() - 12), max(0, ys.min() - 12), min(W, xs.max() + 13), H), seed=9, keep=0.45, sizes=(7, 4, 2)), fr[1])
    over(pic, fr[0], fr[1])
    save_rgb(pic, OUT + "-2-all.png")
    print("painted", round(time.time() - t0, 1), flush=True)
    with open(OUT + "/layout.json", "w") as f:
        json.dump(layout(bases()), f, indent=1)
    if fast:
        sys.exit()
    L = {"back": back.rgb, "note": nt[0], "note_a": nt[1], "front": fr[0], "front_a": fr[1]}
    for name, c in cuts.items():
        L[name], L[name + "_a"] = c.rgb, c.a
    for k, (c, a) in scr.items():
        L["screen_" + k], L["screen_" + k + "_a"] = c, a
    np.savez_compressed(OUT + "-layers.npz", **{k: v.astype(np.float16) for k, v in L.items()})
    write_files({k: v.astype(F32) for k, v in L.items()})
    print("done", round(time.time() - t0, 1))

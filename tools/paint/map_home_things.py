"""The map of the house: what is drawn on the sheet, in pencil (MAP-15H). The back (every floor's walls, its doors as
gaps, its windows, the stairs, the attic hatch, the porch's posts, the rooms that are not places, the three titles),
each place's drawing (its furniture in plan, from its model: map_home_house.py), and each way's.

THE SHEET. Three plans side by side at one scale, SCALE pixels a centimetre (one square of the paper is two feet), the
house turned half round as a plan is usually drawn, the street at the bottom: the ground floor on the left; upstairs
on the right, its landing level with the ground floor's stairs, so that Dad's arrow runs straight across from the one
to the other; the attic above it, its hatch right over the landing's, so that the ladder's dotted line goes straight up.
The attic is drawn as one comes up into it (as its picture faces): it is a plan of its own.

Every drawing function takes a Lead (map_home_kit.py) and draws into it; centimetres go through the floor's Plan."""

import math

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

import brush
import map_home_house as H
from map_home_kit import SS, Plan

SCALE = 0.189                                  # pixels a centimetre: one square of the paper (two feet) is 11.5 pixels
SQUARE = 60.96 * SCALE
SHEET_BOX = (46.0, 142.0, 754.0, 559.0)        # the paper's rectangle (its edge wanders a pixel or so about it)
TURNED = ((754.0, 142.0), 40.0)                # the corner turned over, and how far along the top
CREASES = [("v", 401.0, 1.0), ("h", 331.0, -0.7)]   # folded in half, and in half again, to go in a pocket

BACK = -(694.0 + H.SON_D)                    # the back of the house (Little Sister's far wall), in Z
GF = Plan((-214.0, 1307.0), (BACK, 1150.0), SCALE, 104.0, 151.0, 180)      # (X0..X1 takes in the porch, under the study)
# upstairs, cut at the landing's railing, placed so that the landing is level with the top of the ground floor's stairs
UP = Plan((-214.0, 1307.0), (BACK, 175.0), SCALE, 420.0, 0.0, 180)
UP.oy = GF(54.0, H.STAIRS["z_top"])[1] + 8.0 - (175.0 - 88.0) * SCALE
AT = Plan((0.0, float(H.BS.W)), (0.0, H.A_FRONT), SCALE, 0.0, 0.0, 0)      # the Retreat, as one comes up into it
AT.ox = UP(552.0, 83.0)[0] - (H.A_HATCH[0] + H.A_HATCH[1]) / 2 * SCALE     # its hatch right over the landing's
AT.oy = UP.oy - 56.0 - H.A_FRONT * SCALE - H.WALL_OUT * SCALE              # room under it for the landing's people
TITLE_SIZE = 17
# each title at its plan's top left: beside the ground floor's living room and the attic, over the upstairs' study
TITLES = {"ground": ("Ground floor", (GF(780.0 + H.WALL_OUT, 1150.0)[0] - 10.0, GF.oy + 14.0), "rs"),
          "upstairs": ("Upstairs", (UP(780.0 + H.WALL_OUT, 175.0)[0] - 12.0, UP.oy - 2.0), "rs"),
          "attic": ("The attic", (AT.ox - 12.0, AT.oy + 14.0), "rs")}


def plan_of(floor):
    return {"ground": GF, "upstairs": UP, "attic": AT}[floor]


# ================================================================ walls
def wall_masks(shape, floor, extra_open=()):
    """(walls, rooms) as masks at SS times the size: walls are everything within WALL_OUT of a room that is not a room
    and not an opening; rooms are the floors' interiors."""
    rooms, opens, _ = H.floors()[floor]
    P = plan_of(floor)
    h, w = shape
    wall = Image.new("L", (w * SS, h * SS), 0)
    dw = ImageDraw.Draw(wall)
    t = H.WALL_OUT

    def poly_ss(poly):
        return [(x * SS, y * SS) for x, y in P.pts(poly)]

    for name, poly in rooms.items():             # each room's box grown by the outside wall (the study's L: its box)
        xs = [p[0] for p in poly]
        zs = [p[1] for p in poly]
        dw.polygon(poly_ss(H.rect(min(xs) - t, max(xs) + t, min(zs) - t, max(zs) + t)), fill=255)
    room = Image.new("L", (w * SS, h * SS), 0)
    dr = ImageDraw.Draw(room)
    for name, poly in rooms.items():
        dr.polygon(poly_ss(poly), fill=255)
        dw.polygon(poly_ss(poly), fill=0)
    for name, kind, (a, b, c, d) in list(opens) + list(extra_open):
        if kind in ("door", "doorway", "open"):
            dw.polygon(poly_ss(H.rect(a, b, c, d)), fill=0)
    return wall, room


def wall_edges(mask_im):
    """The edges of a wall mask: its outline, about a pixel wide (at SS)."""
    eroded = mask_im.filter(ImageFilter.MinFilter(5))
    return ImageChops.subtract(mask_im, eroded)


def draw_walls(lead, floor, extra_open=()):
    """The walls of a floor: a mid-grey band between ruled dark edges (outside walls), or one dark ruled line (the
    walls between rooms, which are thinner); doors and doorways left as gaps."""
    wall, _ = wall_masks(lead.shape, floor, extra_open)
    edges = wall_edges(wall)
    lead.can["faint"].paste(ImageChops.lighter(lead.can["faint"], wall))
    lead.can["hard"].paste(ImageChops.lighter(lead.can["hard"], edges))


def draw_windows(lead, floor):
    rooms, opens, _ = H.floors()[floor]
    P = plan_of(floor)
    for name, kind, (a, b, c, d) in opens:
        if kind != "window":
            continue
        q = P.rect(a, b, c, d)
        xs, ys = [p[0] for p in q], [p[1] for p in q]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        lead.clear([(x0 + 0.5, y0 + 0.5), (x1 - 0.5, y0 + 0.5), (x1 - 0.5, y1 - 0.5), (x0 + 0.5, y1 - 0.5)])
        if x1 - x0 > y1 - y0:                    # along X: two thin lines (the sill and the glass), the ends ruled
            for yy in (y0 + (y1 - y0) * 0.30, y0 + (y1 - y0) * 0.70):
                lead.rule((x0, yy), (x1, yy), 0.7, "soft", over=0.0, wob=0.05)
            lead.rule((x0, y0), (x0, y1), 1.0, "hard", over=0.0)
            lead.rule((x1, y0), (x1, y1), 1.0, "hard", over=0.0)
        else:
            for xx in (x0 + (x1 - x0) * 0.30, x0 + (x1 - x0) * 0.70):
                lead.rule((xx, y0), (xx, y1), 0.7, "soft", over=0.0, wob=0.05)
            lead.rule((x0, y0), (x1, y0), 1.0, "hard", over=0.0)
            lead.rule((x0, y1), (x1, y1), 1.0, "hard", over=0.0)


def door(lead, P, hinge, open_end, shut_end, weight="firm", arc_weight="soft"):
    """A door in plan: its leaf, standing open, and the arc it swings through from shut (centimetres)."""
    h = P(*hinge)
    o = P(*open_end)
    s_ = P(*shut_end)
    lead.free([h, o], 1.1, weight, wob=0.1)
    r = math.hypot(o[0] - h[0], o[1] - h[1])
    a0 = math.degrees(math.atan2(o[1] - h[1], o[0] - h[0]))
    a1 = math.degrees(math.atan2(s_[1] - h[1], s_[0] - h[0]))
    while a1 - a0 > 180:
        a1 -= 360
    while a0 - a1 > 180:
        a1 += 360
    lead.arc(h, r, a0, a1, 0.7, arc_weight, wob=0.12)


# ================================================================ the back
def draw_back(lead):
    """Every floor's walls, doors (as gaps; the swings of the rooms that are not places), windows; the stairs; the
    hatch in the landing's ceiling and the opening in the attic's floor; the porch's posts; the titles."""
    # ---- the ground floor
    draw_walls(lead, "ground")
    draw_windows(lead, "ground")
    for name, hinge, o, s_ in H.G_LEAVES:
        door(lead, GF, hinge, o, s_, weight="firm")
    st = H.STAIRS                                                 # the stairs: sixteen treads up the left wall
    x0, x1 = st["X"]
    for k in range(st["steps"] + 1):
        z = st["z_foot"] + (st["z_top"] - st["z_foot"]) * k / st["steps"]
        lead.rule(GF(x0, z), GF(x1, z), 0.8, "firm", over=0.0, wob=0.08)
    lead.rule(GF(x1, st["z_foot"]), GF(x1, st["z_top"]), 1.0, "firm", over=0.6)
    # the porch, outside the front door, under the study: the study's outline over it, dashed, on its posts
    px0, px1, pz0, pz1 = H.PORCH
    lead.dashed(GF.pts([(px0, pz0), (px1, pz0), (px1, pz1), (780.0 + H.WALL_OUT, pz1)]), 0.8, "faint", on=3.5, off=2.6)
    for (X, Z) in H.PORCH_POSTS:
        c = GF(X, Z)
        lead.fill([(c[0] - 1.6, c[1] - 1.6), (c[0] + 1.6, c[1] - 1.6), (c[0] + 1.6, c[1] + 1.6), (c[0] - 1.6, c[1] + 1.6)], "hard")
    # ---- upstairs (cut at the landing's railing: the open side is left open)
    cut = [("cut", "open", (0.0, 780.0, 175.0, 175.0 + H.WALL_OUT + 6))]
    draw_walls(lead, "upstairs", cut)
    draw_windows(lead, "upstairs")
    for name, hinge, o, s_ in H.U_LEAVES:
        if name in ("lilsis-door", "study-door"):
            continue                                              # (the landing's drawing: its doors)
        door(lead, UP, hinge, o, s_, weight="firm")
    a, b, c, d = H.HATCH                                          # the hatch, overhead: dashed
    lead.dashed(UP.pts(H.rect(a, b, c, d)), 0.8, "faint", on=2.6, off=2.0, closed=True)
    # ---- the attic
    draw_walls(lead, "attic")
    draw_windows(lead, "attic")
    a, b, c, d = H.A_HATCH                                        # the opening in the floor: the top of the ladder
    lead.poly(AT.rect(a, b, c, d), 1.1, "firm", ruled=True, over=0.6)
    # ---- the titles, each underlined (a tidy man, and a little proud of it)
    for key, (words, at, anchor) in TITLES.items():
        m = lead.text(words, at, TITLE_SIZE, "firm", anchor=anchor, rough=0.22)
        ys, xs = np.nonzero(m > 0.3)
        lead.rule((xs.min() - 2, at[1] + 4.0), (xs.max() + 3, at[1] + 4.5), 0.9, "soft", over=0.0, wob=0.25)


# ================================================================ the places
def _rot(c, pts, deg):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (z - c[1]) * sa, c[1] + (x - c[0]) * sa + (z - c[1]) * ca) for x, z in pts]


def box(lead, P, x0, x1, z0, z1, width=1.0, weight="firm", ruled=False, wob=0.25):
    lead.poly(P.rect(x0, x1, z0, z1), width, weight, ruled=ruled, wob=wob)


def chair(lead, P, x0, x1, z0, z1, back):
    """A dining chair from above: its seat, and its back drawn heavier on the side away from the table."""
    box(lead, P, x0 + 4, x1 - 4, z0 + 4, z1 - 4, 0.9, "firm", wob=0.12)
    e = {"N": [(x0 + 4, z0 + 4), (x1 - 4, z0 + 4)], "S": [(x0 + 4, z1 - 4), (x1 - 4, z1 - 4)],
         "W": [(x0 + 4, z0 + 4), (x0 + 4, z1 - 4)], "E": [(x1 - 4, z0 + 4), (x1 - 4, z1 - 4)]}[back]
    lead.free(P.pts(e), 1.7, "firm", wob=0.1)


def draw_living(lead):
    P = GF
    T = {k: v for k, v in H.living_things() if k not in ("chair",)}
    chairs = [v for k, v in H.living_things() if k == "chair"]
    # the landing above, across the back of the room: dashed, as overhead
    lead.dashed(P.pts([(108.0, 175.0), (780.0, 175.0)]), 0.8, "faint", on=3.0, off=2.4)
    # Mom's bookcase, and the little telephone table
    x0, x1, z0, z1 = T["books"]
    box(lead, P, x0, x1, z0, z1, 1.0, "firm", ruled=True)
    lead.hatch(P.rect(x0 + 2, x1 - 2, z0 + 2, z1 - 9), angle=60.0, spacing=2.2, width=0.7, weight="faint")
    for k in range(1, 9):
        x = x0 + (x1 - x0) * k / 9
        lead.free(P.pts([(x, z0 + 3), (x, z1 - 9)]), 0.6, "soft", wob=0.05)
    x0, x1, z0, z1 = T["phone-table"]
    box(lead, P, x0, x1, z0, z1, 0.9, "firm", wob=0.1)
    # the piano against the back wall, its keyboard toward the room, its bench
    x0, x1, z0, z1 = T["piano"]
    box(lead, P, x0, x1, z0, z1, 1.2, "firm", ruled=True)
    lead.hatch(P.rect(x0 + 3, x1 - 3, z0 + 3, z1 - 16), angle=50.0, spacing=1.5, width=0.75, weight="soft")
    lead.rule(P(x0 + 6, z1 - 14), P(x1 - 6, z1 - 14), 0.8, "firm", over=0.0)
    for k in range(1, 14):
        x = x0 + 6 + (x1 - x0 - 12) * k / 14
        if k % 7 not in (3, 0):
            lead.free(P.pts([(x, z1 - 14), (x, z1 - 5)]), 0.6, "soft", wob=0.02)
    x0, x1, z0, z1 = T["stool"]
    box(lead, P, x0, x1, z0, z1, 0.9, "firm", wob=0.15)
    # the rug: its border and its diamond
    x0, x1, z0, z1 = T["rug"]
    box(lead, P, x0, x1, z0, z1, 0.9, "soft", wob=0.3)
    box(lead, P, x0 + 22, x1 - 22, z0 + 22, z1 - 22, 0.6, "soft", wob=0.3)
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    for r in (70.0, 38.0):
        lead.free(P.pts([(cx - r * 1.35, cz), (cx, cz - r), (cx + r * 1.35, cz), (cx, cz + r)]), 0.7, "soft", wob=0.15, closed=True)
    # the dinner table, running away from us, set for five, the family Bible at its head
    x0, x1, z0, z1 = T["table"]
    box(lead, P, x0, x1, z0, z1, 1.2, "firm", ruled=True)
    for (px_, pz_) in [((x0 + x1) / 2, z0 + 20), (x0 + 22, 628.0), (x0 + 22, 722.0), (x1 - 22, 627.0), (x1 - 22, 732.0)]:
        lead.circle(P(px_, pz_), 15.0 * SCALE, 0.75, "firm", wob=0.05)
    lead.poly(P.rect((x0 + x1) / 2 + 16, (x0 + x1) / 2 + 40, z0 + 8, z0 + 26), 0.8, "firm", wob=0.05)
    backs = {"chair-head": "N", "chair-left-far": "W", "chair-left-near": "W", "chair-right-far": "E", "chair-right-near": "E"}
    for (a, b, c, d, k) in chairs:
        chair(lead, P, a, b, c, d, backs[k])
    # Dad's armchair, its back to the room's front, turned toward the room; his reading lamp; the newspapers
    cx, cz, turn = T["armchair"]
    seat = _rot((cx, cz), H.rect(cx - 40, cx + 40, cz - 38, cz + 34), turn)
    back = _rot((cx, cz), H.rect(cx - 48, cx + 48, cz + 30, cz + 48), turn)
    armL = _rot((cx, cz), H.rect(cx - 50, cx - 34, cz - 40, cz + 34), turn)
    armR = _rot((cx, cz), H.rect(cx + 34, cx + 50, cz - 40, cz + 34), turn)
    for part, wgt in ((back, "firm"), (armL, "firm"), (armR, "firm"), (seat, "firm")):
        lead.free(P.pts(part), 1.0, wgt, wob=0.15, closed=True)
    lead.hatch(P.pts(back), angle=30.0, spacing=1.6, width=0.55, weight="soft")
    x0, x1, z0, z1 = T["lamp"]
    c = P((x0 + x1) / 2, (z0 + z1) / 2)
    lead.circle(c, 15.0 * SCALE, 0.8, "firm", wob=0.05)
    lead.free([(c[0] - 2.2, c[1]), (c[0] + 2.2, c[1])], 0.5, "soft", wob=0.0)
    lead.free([(c[0], c[1] - 2.2), (c[0], c[1] + 2.2)], 0.5, "soft", wob=0.0)
    x0, x1, z0, z1 = T["basket"]
    lead.circle(P((x0 + x1) / 2, (z0 + z1) / 2), (x1 - x0) / 2 * SCALE, 0.8, "firm", wob=0.1, ry=(z1 - z0) / 2 * SCALE)
    # the rubber plant by the right-hand wall
    x0, x1, z0, z1 = T["plant"]
    c = P((x0 + x1) / 2, (z0 + z1) / 2)
    lead.circle(c, 2.2, 0.7, "firm", wob=0.05)
    for k in range(7):
        a = 2 * math.pi * k / 7 + 0.3
        lead.free([(c[0] + 2.0 * math.cos(a), c[1] + 2.0 * math.sin(a)), (c[0] + 5.0 * math.cos(a), c[1] + 5.0 * math.sin(a))], 0.6, "soft", wob=0.1)
    # the cupboard under the stairs: its low door in the panelling, opening into the room
    z0, z1 = T["closet"]
    door(lead, P, (108.0, z1), (172.0, z1), (108.0, z0), weight="firm")
    # the front door, marked: its leaf and swing, and the doormat outside on the porch
    door(lead, P, (664.0, 0.0), (664.0, 96.0), (760.0, 0.0), weight="firm")
    mat = H.rect(660.0, 768.0, -96.0, -40.0)
    lead.poly(P.pts(mat), 0.9, "firm", wob=0.1)
    lead.hatch(P.pts(H.rect(666.0, 762.0, -90.0, -46.0)), angle=0.0, spacing=1.5, width=0.5, weight="soft")


def draw_landing(lead):
    P = UP
    T = dict(H.landing_things())
    # the railing along the gallery, its newel posts, a gap where the ladder's dotted line goes up past it
    hx = (H.HATCH[0] + H.HATCH[1]) / 2
    lead.rule(P(108.0, 175.0), P(hx - 22, 175.0), 1.2, "firm", over=0.0)
    lead.rule(P(hx + 22, 175.0), P(780.0, 175.0), 1.2, "firm", over=0.0)
    for (a, b, c, d, e, f) in T["posts"]:
        q = P.rect(a - 2, b + 2, e - 2, f + 2)
        lead.fill(q, "hard")
    lead.rule(P(108.0, 175.0), P(108.0, 210.0), 1.2, "firm", over=0.0)       # down the stairwell, to the cut
    lead.rule(P(0.0, 175.0), P(108.0, 175.0), 0.6, "soft", over=0.0)          # the top step
    # the quilt hung over the rail to air
    a, b, _, _, c, d = T["quilt"]
    q = P.rect(a, b, c - 4, d + 4)
    lead.poly(q, 0.8, "firm", wob=0.05)
    for k in range(1, 6):
        x = a + (b - a) * k / 6
        lead.free(P.pts([(x, c - 4), (x, d + 4)]), 0.5, "soft", wob=0.0)
    # the hall table and its lamp, the hamper with the washing on its lid, the Son's school bag on its peg
    a, b, _, _, c, d = T["halltable"]
    box(lead, P, a, b, c, d, 1.0, "firm", ruled=True)
    lead.hatch(P.rect(a + 2, b - 2, c + 2, d - 2), angle=60.0, spacing=2.2, width=0.7, weight="faint")
    a, b, _, _, c, d = T["lamp"]
    lead.circle(P((a + b) / 2, (c + d) / 2), (b - a) / 2 * SCALE, 0.7, "firm", wob=0.05)
    a, b, _, _, c, d = T["hamper"]
    box(lead, P, a, b, c, d, 1.0, "firm", wob=0.2)
    lead.free(P.pts([(a + 6, (c + d) / 2), (b - 6, (c + d) / 2)]), 0.6, "soft", wob=0.2)
    a, b, _, _, c, d = T["bag"]
    box(lead, P, a, b, c + 2, d + 14, 0.9, "firm", wob=0.1)
    # the attic ladder, let down from its hatch: its two rails and its rungs, its feet on the landing
    a, b, _, _, c, d = T["ladder"]
    for z in (c + 4, d - 4):
        lead.rule(P(a, z), P(b, z), 1.0, "firm", over=0.3)
    n = 6
    for k in range(n + 1):
        x = a + 6 + (b - a - 12) * k / n
        lead.rule(P(x, c + 4), P(x, d - 4), 0.7, "firm", over=0.0)
    # the three doors off it: the Son's shut (all act), Little Sister's and the study's ajar
    lead.rule(P(190.0, -6.0), P(275.0, -6.0), 1.4, "firm", over=0.0)
    for name, hinge, end, _ in H.U_LEAVES:
        if name in ("lilsis-door", "study-door"):                              # open, back against the passage's wall
            lead.free([P(*hinge), P(*end)], 1.2, "firm", wob=0.05)
    # Dad's notice on the study door, as a small square
    q = P.rect(630.0, 674.0, 4.0, 46.0)
    lead.poly(q, 0.9, "firm", wob=0.05)
    for k in (1, 2, 3):
        z = 4 + 42 * k / 4
        lead.free(P.pts([(636.0, z), (668.0, z)]), 0.45, "soft", wob=0.1)


def draw_study(lead):
    P = UP
    T = dict(H.study_things())
    s = H.st
    # under the slope of the roof: the ridge, dash and dot, and where the ceiling comes down low on each side
    for X in (58.0, 642.0):
        lead.dashed([P(*s(X, 0.0)), P(*s(X, 748.0))], 0.6, "faint", on=2.2, off=2.2)
    lead.dashed([P(*s(350.0, 0.0)), P(*s(350.0, 748.0))], 0.7, "faint", on=6.0, off=2.4)
    for key in ("desk", "cabinet", "shelves", "heap", "pile", "rug", "chair"):
        v = T[key]
        X0, X1, Z0, Z1 = (v[0], v[1], v[4], v[5]) if len(v) == 6 else (v[0], v[1], v[2], v[3])
        lead.clear(P.pts([s(X0 - 8, Z0 - 8), s(X1 + 8, Z0 - 8), s(X1 + 8, Z1 + 8), s(X0 - 8, Z1 + 8)]))
    g = T["globe"]
    lead.clear(P.pts([s(g[0] - 30, g[1] - 30), s(g[0] + 30, g[1] - 30), s(g[0] + 30, g[1] + 30), s(g[0] - 30, g[1] + 30)]))

    def bx(v, width=1.0, weight="firm", ruled=False, inset=0.0):
        X0, X1, _, _, Z0, Z1 = v
        lead.poly(P.pts([s(X0 + inset, Z0 + inset), s(X1 - inset, Z0 + inset), s(X1 - inset, Z1 - inset), s(X0 + inset, Z1 - inset)]),
                  width, weight, ruled=ruled, wob=0.15)

    # the desk, two pedestals of drawers; the computer on it, its screen toward the chair; the chair
    bx(T["desk"], 1.2, "firm", ruled=True)
    X0, X1, _, _, Z0, Z1 = T["desk"]
    lead.hatch(P.pts([s(X0 + 3, Z0 + 3), s(X1 - 3, Z0 + 3), s(X1 - 3, Z1 - 3), s(X0 + 3, Z1 - 3)]), angle=60.0, spacing=2.4, width=0.7, weight="faint")
    for xa, xb in ((X0 + 6, X0 + 52), (X1 - 52, X1 - 6)):
        lead.poly(P.pts([s(xa, Z0 + 6), s(xb, Z0 + 6), s(xb, Z1 - 6), s(xa, Z1 - 6)]), 0.6, "soft", wob=0.05)
    bx(T["computer"], 0.9, "firm")
    X0, X1, _, _, Z0, Z1 = T["monitor"]
    lead.free(P.pts([s(X0, Z1), s(X1, Z1)]), 1.8, "firm", wob=0.05)
    lead.free(P.pts([s(X0 + 8, Z0), s(X1 - 8, Z0), s(X1, Z1), s(X0, Z1)]), 0.8, "firm", wob=0.05, closed=True)
    X0, X1, _, _, Z0, Z1 = T["chair"]
    c = P(*s((X0 + X1) / 2, (Z0 + Z1) / 2))
    lead.circle(c, (X1 - X0) / 2 * SCALE, 0.9, "firm", wob=0.08)
    back = P.angle(90.0)                                       # its back is on the side away from the desk (toward +Z)
    lead.arc(c, (X1 - X0) / 2 * SCALE + 1.2, back - 60.0, back + 60.0, 1.4, "firm", wob=0.05)
    # the filing cabinet, the answering machine on it: its little window for the tape, its buttons
    bx(T["cabinet"], 1.0, "firm", ruled=True)
    X0c, X1c, _, _, Z0c, Z1c = T["cabinet"]
    lead.hatch(P.pts([s(X0c + 2, Z0c + 2), s(X1c - 2, Z0c + 2), s(X1c - 2, Z1c - 2), s(X0c + 2, Z1c - 2)]), angle=60.0, spacing=2.4, width=0.7, weight="faint")
    bx(T["machine"], 0.9, "firm")
    X0, X1, _, _, Z0, Z1 = T["machine"]
    lead.poly(P.pts([s(X0 + 10, Z0 + 8), s(X1 - 18, Z0 + 8), s(X1 - 18, Z0 + 22), s(X0 + 10, Z0 + 22)]), 0.6, "soft", wob=0.0)
    for k in range(3):
        lead.dot(P(*s(X0 + 12 + 11 * k, Z1 - 9)), 0.55, "firm")
    # the shelves along the right-hand wall, the family vault at their near end, its dial
    bx(T["shelves"], 1.0, "firm", ruled=True)
    X0, X1, _, _, Z0, Z1 = T["shelves"]
    lead.hatch(P.pts([s(X0 + 3, Z0 + 3), s(X1 - 3, Z0 + 3), s(X1 - 3, H.ST_M.VAULT[4] - 6), s(X0 + 3, H.ST_M.VAULT[4] - 6)]), angle=60.0, spacing=2.4, width=0.7, weight="faint")
    for k in range(1, 6):
        z = Z0 + (H.ST_M.VAULT[4] - 8 - Z0) * k / 6
        lead.free(P.pts([s(X0 + 4, z), s(X1 - 4, z)]), 0.5, "soft", wob=0.05)
    bx(T["vault"], 1.1, "firm", ruled=True)
    X0v, X1v, _, _, Z0v, Z1v = T["vault"]
    lead.hatch(P.pts([s(X0v + 2, Z0v + 2), s(X1v - 2, Z0v + 2), s(X1v - 2, Z1v - 2), s(X0v + 2, Z1v - 2)]), angle=45.0, spacing=1.6, width=0.7, weight="soft")
    X0, X1, _, _, Z0, Z1 = T["vault"]
    lead.circle(P(*s((X0 + X1) / 2, (Z0 + Z1) / 2)), 9.0 * SCALE, 0.7, "firm", wob=0.03)
    # the globe on its stand, in the far right corner
    gx, gz, gy, gr = T["globe"]
    c = P(*s(gx, gz))
    lead.circle(c, gr * SCALE, 0.9, "firm", wob=0.04)
    lead.free([(c[0] - gr * SCALE * 0.95, c[1]), (c[0] + gr * SCALE * 0.95, c[1])], 0.45, "soft", wob=0.0)
    lead.arc(c, gr * SCALE * 0.55, -90.0, 90.0, 0.45, "soft", wob=0.0)
    # the rug and its three diamonds
    X0, X1, Z0, Z1 = T["rug"]
    lead.poly(P.pts([s(X0, Z0), s(X1, Z0), s(X1, Z1), s(X0, Z1)]), 0.9, "soft", wob=0.3)
    zc = (Z0 + Z1) / 2
    for k in range(3):
        xc = X0 + (X1 - X0) * (k + 0.5) / 3
        lead.free(P.pts([s(xc - 34, zc), s(xc, zc - 52), s(xc + 34, zc), s(xc, zc + 52)]), 0.7, "soft", wob=0.1, closed=True)
    # the things that did not fit in the car: boxes taped shut, a rolled sleeping bag, a cooler
    X0, X1, _, _, Z0, Z1 = T["heap"]
    parts = [(X0, X0 + 70, Z0 + 8, Z0 + 66, "box"), (X0 + 78, X0 + 150, Z0 + 4, Z0 + 52, "box"),
             (X0 + 160, X0 + 236, Z0 + 12, Z1 - 30, "bag"), (X0 + 8, X0 + 92, Z0 + 74, Z1 - 4, "cooler"),
             (X0 + 104, X0 + 170, Z0 + 60, Z1 - 8, "box"), (X0 + 244, X1, Z0 + 20, Z1 - 20, "box")]
    for (a, b, c_, d, kind) in parts:
        q = P.pts([s(a, c_), s(b, c_), s(b, d), s(a, d)])
        lead.poly(q, 0.9, "firm", wob=0.15)
        if kind == "box":
            lead.free([q[0], q[2]], 0.5, "soft", wob=0.05)
            lead.free([q[1], q[3]], 0.5, "soft", wob=0.05)
        elif kind == "bag":
            for t in (0.3, 0.55, 0.8):
                lead.free(P.pts([s(a + (b - a) * t, c_ + 4), s(a + (b - a) * t, d - 4)]), 0.5, "soft", wob=0.1)
        else:
            lead.free(P.pts([s(a + 6, (c_ + d) / 2), s(b - 6, (c_ + d) / 2)]), 0.5, "soft", wob=0.05)
    X0, X1, _, _, Z0, Z1 = T["pile"]
    for (a, b, c_, d) in ((X0 + 4, X1 - 4, Z0 + 4, Z0 + 40), (X0 + 10, X1 - 2, Z0 + 46, Z1 - 4)):
        q = P.pts([s(a, c_), s(b, c_), s(b, d), s(a, d)])
        lead.poly(q, 0.9, "firm", wob=0.15)
        lead.free([q[0], q[2]], 0.5, "soft", wob=0.05)
    # the study's own door, in the partition at the lobby, standing open into the room
    (PX, PZ), (D0, D1, _), (deg, width) = T["door"]
    hinge = s(PX, D0)
    a = math.radians(deg)
    end = s(PX + width * math.cos(a), D0 + width * math.sin(a))
    door(lead, P, hinge, end, s(PX, D1), weight="firm")


def draw_lilsis(lead):
    P = UP
    T = dict(H.lilsis_things())
    s = H.ls

    def q(X0, X1, Z0, Z1):
        return P.pts([s(X0, Z0), s(X1, Z0), s(X1, Z1), s(X0, Z1)])

    # the flock: a mountain of stuffed animals where the old bed was, chickens on top
    X0, X1, _, _, Z0, Z1 = T["flock"]
    rng = np.random.default_rng(31)
    pts = []
    n = 26
    for k in range(n):
        t = 2 * math.pi * k / n
        rx, rz = (X1 - X0) / 2, (Z1 - Z0) / 2
        bump = 1.0 + 0.10 * math.sin(5 * t + 0.4) + 0.06 * rng.normal()
        pts.append(P(*s((X0 + X1) / 2 + rx * bump * math.cos(t), (Z0 + Z1) / 2 + rz * bump * math.sin(t))))
    lead.free(pts, 1.0, "firm", wob=0.2, closed=True)
    for (hx, hz) in ((110.0, 50.0), (170.0, 36.0), (226.0, 64.0), (140.0, 88.0)):
        c = P(*s(hx, hz))
        lead.circle(c, 2.0, 0.6, "soft", wob=0.05)
        lead.free([(c[0] - 1.0, c[1] - 2.0), (c[0] - 0.3, c[1] - 3.1), (c[0] + 0.4, c[1] - 2.0), (c[0] + 1.1, c[1] - 3.0), (c[0] + 1.6, c[1] - 1.9)], 0.5, "firm", wob=0.0)
    # the blanket fort: its ridge along the middle, its way in on the side toward the room
    X0, X1, _, _, Z0, Z1 = T["fort"]
    lead.poly(q(X0, X1, Z0, Z1), 1.0, "firm", wob=0.3)
    lead.hatch(q(X0 + 3, 92.0, Z0 + 3, Z1 - 3), angle=80.0, spacing=2.4, width=0.7, weight="faint")
    lead.free(P.pts([s(96.0, Z0), s(96.0, Z1)]), 0.9, "firm", wob=0.15)
    for (a, b) in ((s(X0, Z0), s(96.0, (Z0 + Z1) / 2)), (s(X1, Z0), s(96.0, (Z0 + Z1) / 2)), (s(X0, Z1), s(96.0, (Z0 + Z1) / 2)), (s(X1, Z1), s(96.0, (Z0 + Z1) / 2))):
        lead.free([P(*a), P(*b)], 0.45, "soft", wob=0.1)
    lead.clear(q(X1 - 4, X1 + 4, Z0 + 32, Z1 - 30))                           # its way in
    lead.free(P.pts([s(X1 - 2, Z0 + 32), s(X1 + 12, Z0 + 24)]), 0.8, "firm", wob=0.1)
    # her bed along the right-hand wall, the pillow at its head (one place kept free), the blanket turned down
    X0, X1, _, _, Z0, Z1 = T["bed"]
    lead.poly(q(X0, X1, Z0, Z1), 1.2, "firm", ruled=True)
    lead.hatch(q(X0 + 3, X1 - 3, T["pillow"][5] + 40, Z1 - 3), angle=35.0, spacing=2.4, width=0.7, weight="faint")
    X0p, X1p, _, _, Z0p, Z1p = T["pillow"]
    lead.free(q(X0p + 2, X1p - 2, Z0p + 2, Z1p), 0.8, "firm", wob=0.2, closed=True)
    lead.free(P.pts([s(X0 + 4, Z1p + 38), s(X1 - 4, Z1p + 30)]), 0.7, "soft", wob=0.2)
    lead.free(P.pts([s(X0 + 4, Z1p + 52), s(X1 - 4, Z1p + 46)]), 0.5, "soft", wob=0.2)
    # the bedside table and the rooster lamp on it
    X0, X1, _, _, Z0, Z1 = T["lamptable"]
    lead.poly(q(X0, X1, Z0, Z1), 0.9, "firm", wob=0.1)
    lead.circle(P(*s((X0 + X1) / 2, (Z0 + Z1) / 2)), 1.6, 0.6, "firm", wob=0.0)
    # the tea party: the little round table, every guest a chicken
    tx, tz, tr, th = T["teatable"]
    c = P(*s(tx, tz))
    lead.circle(c, tr * SCALE, 1.0, "firm", wob=0.1)
    for k, a in enumerate((20.0, 95.0, 160.0, 230.0, 300.0)):
        g = P(*s(tx + (tr + 24) * math.cos(math.radians(a)), tz + (tr + 24) * math.sin(math.radians(a))))
        lead.circle(g, 1.9, 0.7, "firm", wob=0.05)
        lead.dot((g[0] + 1.2 * math.cos(math.radians(a + 90)), g[1] + 1.2 * math.sin(math.radians(a + 90))), 0.5, "firm")
    lead.circle(c, 1.3, 0.5, "soft", wob=0.0)
    # the rug like a fried egg
    ex, ez, ew, ed = T["eggrug"]
    pts = []
    for k in range(22):
        t = 2 * math.pi * k / 22
        wob = 1.0 + 0.13 * math.sin(3 * t + 1.0) + 0.07 * math.sin(7 * t)
        pts.append(P(*s(ex + ew * wob * math.cos(t), ez + ed * wob * math.sin(t))))
    lead.free(pts, 0.8, "soft", wob=0.2, closed=True)
    lead.circle(P(*s(ex - 12, ez + 4)), 24 * SCALE, 0.8, "soft", wob=0.06)
    # the hen house (her doll's house, for chickens): its roof's ridge, its ramp down
    X0, X1, _, _, Z0, Z1 = T["coop"]
    lead.poly(q(X0, X1, Z0, Z1), 1.0, "firm", ruled=True)
    lead.hatch(q(X0 + 2, X1 - 2, Z0 + 2, (Z0 + Z1) / 2 - 2), angle=70.0, spacing=2.0, width=0.7, weight="faint")
    lead.free(P.pts([s(X0, (Z0 + Z1) / 2), s(X1, (Z0 + Z1) / 2)]), 0.6, "soft", wob=0.05)
    lead.poly(q((X0 + X1) / 2 - 12, (X0 + X1) / 2 + 12, Z0 - 26, Z0), 0.7, "firm", wob=0.05)
    # the nest: a cardboard box, a hen in it, her eggs
    X0, X1, _, _, Z0, Z1 = T["nest"]
    lead.poly(q(X0, X1, Z0, Z1), 0.9, "firm", wob=0.15)
    c = P(*s((X0 + X1) / 2 - 6, (Z0 + Z1) / 2))
    lead.circle(c, 2.4, 0.7, "firm", wob=0.05)
    lead.free([(c[0] - 1.0, c[1] - 2.3), (c[0] - 0.3, c[1] - 3.4), (c[0] + 0.4, c[1] - 2.3), (c[0] + 1.1, c[1] - 3.3)], 0.5, "firm", wob=0.0)
    for (ox, oz) in ((24.0, -10.0), (26.0, 10.0)):
        lead.circle(P(*s((X0 + X1) / 2 + ox, (Z0 + Z1) / 2 + oz)), 1.0, 0.5, "soft", wob=0.0, ry=1.3)
    # her toy box and her crate of picture books
    X0, X1, _, _, Z0, Z1 = T["toybox"]
    lead.poly(q(X0, X1, Z0, Z1), 0.9, "firm", wob=0.15)
    lead.free(P.pts([s(X0 + 4, Z0 + 10), s(X1 - 4, Z0 + 10)]), 0.5, "soft", wob=0.05)
    X0, X1, _, _, Z0, Z1 = T["crate"]
    lead.poly(q(X0, X1, Z0, Z1), 0.9, "firm", wob=0.15)
    for k in (1, 2):
        z = Z0 + (Z1 - Z0) * k / 3
        lead.free(P.pts([s(X0 + 3, z), s(X1 - 3, z)]), 0.5, "soft", wob=0.05)
    # her window in the far wall, its curtains drawn back to each side (gingham, in her picture)
    wx0, wx1, _, _ = H.LS_M.WINDOW
    for (xa, xb) in ((wx0 - 22, wx0 + 4), (wx1 - 4, wx1 + 22)):
        pts = [P(*s(xa + (xb - xa) * k / 6, 6.0 + (3.0 if k % 2 else 0.0))) for k in range(7)]
        lead.free(pts, 0.8, "firm", wob=0.05)
        lead.free(P.pts([s(xa, 3.0), s(xa, 12.0)]), 0.6, "soft", wob=0.0)
    # her door, standing open into the room at the passage's end
    dx, (dz0, dz1) = T["door"]
    door(lead, P, s(dx, dz1), s(dx, dz0), s(dx + 88.0, dz1), weight="firm")


def draw_retreat(lead):
    P = AT
    T = dict(H.retreat_things())
    # overhead: the two skylights in the slope, and the ridge (dash and dot), rubbed out where things stand under them
    for (a, b, c, d) in T["skylights"]:
        lead.dashed(P.rect(a, b, c, d), 0.6, "faint", on=2.2, off=2.0, closed=True)
    lead.dashed([P(0.0, T["ridge"]), P(float(H.BS.W), T["ridge"])], 0.7, "faint", on=6.0, off=2.4)
    for key in ("mat", "bed"):
        v = T[key]
        a, b, c, d = (v[0], v[1], v[2], v[3]) if key == "mat" else (v[0], v[1], v[4], v[5])
        lead.clear(P.rect(a - 8, b + 8, c - 8, d + 8))
    rx, rz, rr = T["rug"]
    lead.clear(P.rect(rx - rr - 8, rx + rr + 8, rz - rr - 8, rz + rr + 8))
    for (fx, fz) in T["footlamps"]:
        lead.clear(P.rect(fx - 14, fx + 14, fz - 14, fz + 14))
    # her bookcase (books by colour) along the low far wall; her timeline on the wall over it, a long line of dashes
    a, b, _, _, c, d = T["bookcase"]
    lead.poly(P.rect(a, b, c, d), 1.0, "firm", ruled=True)
    lead.hatch(P.rect(a + 2, b - 2, c + 2, d - 2), angle=60.0, spacing=2.2, width=0.6, weight="faint")
    rng = np.random.default_rng(7)
    x = a + 4
    while x < b - 4:
        lead.free([P(x, c + 3), P(x, d - 3)], 0.45, "soft", wob=0.0)
        x += 5 + rng.random() * 6
    t0, t1, _, _ = T["timeline"]
    lead.dashed([P(t0, -12.0), P(t1, -12.0)], 0.9, "firm", on=2.0, off=1.4, wob=0.05)
    red = t0 + (t1 - t0) * H.BS.TIMELINE_RED
    lead.free([P(red, -20.0), P(red, -4.0)], 1.0, "firm", wob=0.0)
    # the sound table, the sound machine on it (its dial), the little fountain
    a, b, _, _, c, d = T["soundtable"]
    lead.poly(P.rect(a, b, c, d), 1.0, "firm", ruled=True)
    a, b, _, _, c, d = T["machine"]
    lead.poly(P.rect(a, b, c, d), 0.8, "firm", wob=0.05)
    lead.dot(P(b - 9, (c + d) / 2), 0.7, "firm")
    fx, fz, fr = T["fountain"]
    lead.circle(P(fx, fz), fr * SCALE, 0.7, "firm", wob=0.03)
    # the writing desk and its stool
    a, b, _, _, c, d = T["desk"]
    lead.poly(P.rect(a, b, c, d), 1.0, "firm", ruled=True)
    sx, sz, sr, _ = T["stool"]
    lead.circle(P(sx, sz), sr * SCALE, 0.8, "firm", wob=0.03)
    # the low bed, its round pillows at the head, the canopy's hoop overhead (dashed)
    a, b, _, _, c, d = T["bed"]
    lead.poly(P.rect(a, b, c, d), 1.2, "firm", ruled=True)
    lead.hatch(P.rect(a + 3, b - 3, 246.0, d - 3), angle=35.0, spacing=2.4, width=0.7, weight="faint")
    for (px_, pz_) in ((640.0, 166.0), (690.0, 162.0), (730.0, 172.0)):
        lead.circle(P(px_, pz_), 16 * SCALE, 0.7, "firm", wob=0.05)
    lead.free([P(a + 6, 236.0), P(b - 6, 230.0)], 0.6, "soft", wob=0.15)
    cx, cy, cz, cr = T["canopy"]
    lead.dashed([P(cx + cr * math.cos(2 * math.pi * k / 24), cz + cr * math.sin(2 * math.pi * k / 24)) for k in range(25)], 0.7, "soft", on=1.8, off=1.6)
    for (fx, fz) in T["footlamps"]:
        lead.circle(P(fx, fz), 1.2, 0.6, "firm", wob=0.0)
    # the round rug, and its star
    lead.circle(P(rx, rz), rr * SCALE, 0.9, "soft", wob=0.1)
    lead.circle(P(rx, rz), rr * SCALE * 0.62, 0.6, "soft", wob=0.08)
    for k in range(8):
        a = 2 * math.pi * k / 8
        r1 = rr * (0.55 if k % 2 else 0.22)
        lead.free([P(rx + rr * 0.08 * math.cos(a), rz + rr * 0.08 * math.sin(a)), P(rx + r1 * math.cos(a), rz + r1 * math.sin(a))], 0.5, "soft", wob=0.0)
    # the exercise mat, rolled out
    a, b, c, d = T["mat"]
    lead.free(P.rect(a, b, c, d), 0.9, "soft", wob=0.2, closed=True)
    lead.hatch(P.rect(a + 3, b - 3, c + 3, d - 3), angle=90.0, spacing=2.6, width=0.6, weight="faint")
    lead.free([P(a + 4, d - 16), P(b - 4, d - 16)], 0.5, "soft", wob=0.05)
    # the left-hand wall: the salt lamp and the diffuser on their stumps, the palm, the ferns, the rolled towels, the
    # slippers set ready by the hatch, a candle on the floor; the pampas grass in the far right corner
    for key in ("stump", "stump2"):
        x_, z_, r_, _ = T[key]
        lead.circle(P(x_, z_), r_ * SCALE, 0.8, "firm", wob=0.03)
    for key, r_ in (("palm", 16.0), ("pampas", 12.0)):
        x_, z_ = T[key]
        c = P(x_, z_)
        lead.circle(c, 1.2, 0.5, "firm", wob=0.0)
        for k in range(8):
            a = 2 * math.pi * k / 8 + 0.2
            lead.free([(c[0] + 1.2 * math.cos(a), c[1] + 1.2 * math.sin(a)), (c[0] + (r_ * SCALE + 2.4) * math.cos(a), c[1] + (r_ * SCALE + 2.4) * math.sin(a))], 0.5, "soft", wob=0.1)
    a, b, _, _, c, d = T["plantstand"]
    lead.poly(P.rect(a, b, c, d), 0.8, "firm", wob=0.1)
    for k in range(4):
        cc = P(a + 14 + (k % 2) * 28, c + 14 + (k // 2) * 30)
        lead.circle(cc, 1.4, 0.5, "soft", wob=0.1)
    bx_, bz_, br_, _ = T["basket"]
    lead.circle(P(bx_, bz_), br_ * SCALE, 0.8, "firm", wob=0.05)
    lead.circle(P(bx_ - 8, bz_ - 6), 1.1, 0.5, "soft", wob=0.0)
    lead.circle(P(bx_ + 8, bz_ + 6), 1.1, 0.5, "soft", wob=0.0)
    a, b, c, d = T["slippers"]
    lead.circle(P(a + 6, (c + d) / 2), 1.0, 0.5, "firm", wob=0.0, ry=2.0)
    lead.circle(P(b - 6, (c + d) / 2), 1.0, 0.5, "firm", wob=0.0, ry=2.0)
    fx, fz = T["floorcandle"]
    lead.circle(P(fx, fz), 1.0, 0.6, "firm", wob=0.0)
    # her rules on their easel, facing whoever comes up the ladder; the tea cushion and its tray; the pouf
    a, b, _, _, z = T["sign"]
    lead.free([P(a, z), P(b, z)], 1.1, "firm", wob=0.05)
    lead.free([P((a + b) / 2, z), P((a + b) / 2, z - 30.0)], 0.6, "soft", wob=0.05)
    a, b, c, d = T["tea"]
    lead.free(P.rect(a, b, c, d), 0.9, "firm", wob=0.2, closed=True)
    lead.circle(P((a + b) / 2, (c + d) / 2), 2.4, 0.6, "firm", wob=0.05)
    lead.circle(P((a + b) / 2 + 4, (c + d) / 2 - 2), 0.9, 0.5, "soft", wob=0.0)
    px_, pz_, pr_, _ = T["pouf"]
    lead.circle(P(px_, pz_), pr_ * SCALE, 0.9, "firm", wob=0.05)
    lead.circle(P(px_, pz_), pr_ * SCALE * 0.4, 0.5, "soft", wob=0.05)
    # the rail round the hatch, and the top of the ladder in it
    a, b, c, d = T["hatch"]
    lead.rule(P(a - 6, c), P(a - 6, d + 6), 1.1, "firm", over=0.0)
    lead.rule(P(b + 6, c), P(b + 6, d + 6), 1.1, "firm", over=0.0)
    lead.rule(P(a - 6, d + 6), P(b + 6, d + 6), 1.1, "firm", over=0.0)
    for z in (d - 22, d - 46):
        lead.rule(P(a + 30, z), P(b - 30, z), 0.6, "soft", over=0.0)
    lead.rule(P(a + 30, d - 4), P(a + 30, d - 56), 0.6, "soft", over=0.0)
    lead.rule(P(b - 30, d - 4), P(b - 30, d - 56), 0.6, "soft", over=0.0)


PLACES = {"living": draw_living, "landing": draw_landing, "study": draw_study, "lilsis": draw_lilsis, "bigsis": draw_retreat}


# ================================================================ the ways
WAY_LINES = {}                                     # the line each way is drawn along, in picture pixels (for layout.json)


def way_living_landing(lead):
    """Dad's arrow 'up': along the stairs from their foot to the top, out past the stair wall, across to the landing."""
    st = H.STAIRS
    xm = (st["X"][0] + st["X"][1]) / 2
    a = GF(xm, st["z_foot"] - 22)
    b = GF(xm, st["z_top"] + 30)
    land = UP(780.0 + H.WALL_OUT + 6, 88.0)                     # just short of the landing's end wall
    corner = (GF(-H.WALL_OUT - 30, 0.0)[0], b[1] + 8)
    pts = [a, b, (b[0] + 4, b[1] + 6), corner]
    mid = ((corner[0] + land[0]) / 2, (corner[1] + land[1]) / 2 - 6)
    run = brush.curve([corner, mid, (land[0] - 2, land[1])], steps=10)
    line = pts + run[1:]
    lead.free(line, 1.4, "firm", wob=0.25)
    lead.arrowhead(line[-1], line[-2], 5.5, 1.4, "firm")
    lead.text("up", (corner[0] + 13, corner[1] - 5), 13, "firm", anchor="ms", rough=0.2)      # beside the stairs, as it leaves them
    WAY_LINES[("living", "landing")] = line


def way_landing_study(lead):
    """Through the study door into its lobby, and in through the study's own door: dots and an arrowhead."""
    a = UP(652.0, -8.0)
    b = UP(652.0, -72.0)
    c = UP(762.0, -72.0)
    line = [a, (a[0], (a[1] + b[1]) / 2), b, ((b[0] + c[0]) / 2 + 1, (b[1] + c[1]) / 2), c]
    lead.dots(line, 0.75, 3.2, "firm")
    lead.arrowhead(c, ((b[0] + c[0]) / 2, (b[1] + c[1]) / 2), 3.6, 0.9, "firm")
    WAY_LINES[("landing", "study")] = line


def way_landing_lilsis(lead):
    """Through Little Sister's door off the landing, along the passage, to her own door: dots and an arrowhead."""
    a = UP(420.0, -8.0)
    b = UP(426.0, -H.SON_D + 14.0)
    line = [a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), b]
    lead.dots(line, 0.75, 3.2, "firm")
    lead.arrowhead(b, line[1], 3.6, 0.9, "firm")
    WAY_LINES[("landing", "lilsis")] = line


def way_landing_bigsis(lead):
    """The attic ladder: a dotted line from the hatch, up past the railing, to the opening in the attic's floor."""
    hx = (H.HATCH[0] + H.HATCH[1]) / 2
    a = UP(hx, H.HATCH[3] + 6.0)
    b = AT((H.A_HATCH[0] + H.A_HATCH[1]) / 2, H.A_HATCH[3] + 14.0)
    line = [a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), b]
    lead.dots(line, 0.8, 3.4, "firm")
    lead.arrowhead(b, line[1], 3.8, 0.9, "firm")
    WAY_LINES[("landing", "bigsis")] = line


WAYS = {("living", "landing"): way_living_landing, ("landing", "study"): way_landing_study,
        ("landing", "lilsis"): way_landing_lilsis, ("landing", "bigsis"): way_landing_bigsis}

"""The numbers the game needs across the Tiber, measured from the model (rome_tiber_model.py) and the finished pictures:
layout.json's walk outline, blocked ground, the cut-outs and their bases, every thing to click (a shape hugging it, a
place to stand, a facing), the marks the master brief names, the way out, the things that move by nature (fx) and the
hens' frames. rome_tiber.py calls layout(); rome_tiber_check.py draws it over the picture and walks it on the engine's
own walk map."""

import math

import numpy as np

import rome_tiber_model as M
import rome_tiber_hens as HENS

r = lambda p: [int(round(float(p[0]))), int(round(float(p[1])))]
r1 = lambda p: [round(float(p[0]), 1), round(float(p[1]), 1)]


def G(x, z):
    """A place on the lane (y = 0) -> picture point, rounded."""
    return r(M.P(x, 0.0, z))


def F(s, o, h=0.0):
    """A place s along the near houses' front, o cm out from it (toward the square), h up -> picture point."""
    x, z = M.out(M.along(s), o)
    return r(M.P(x, h, z))


def Fz(s, o):
    return M.out(M.along(s), o)[1]


def row_scale(y):
    return max(0.0, (y - M.HZ) / (M.FULL - M.HZ))


def hull(points):
    """The convex hull of picture points (monotone chain), as whole pixels."""
    pts = sorted(set((int(round(x)), int(round(y))) for x, y in points))
    if len(pts) < 3:
        return [list(p) for p in pts]
    cross = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return [list(p) for p in lower[:-1] + upper[:-1]]


def hull_of_mask(mask, pad=2):
    """A shape hugging a painted thing: the hull of its pixels' corners, grown by `pad`."""
    ys, xs = np.where(mask > 0.5)
    if len(xs) == 0:
        return []
    pts = []
    for (dx, dy) in ((-pad, -pad), (pad + 1, -pad), (-pad, pad + 1), (pad + 1, pad + 1)):
        pts += list(zip((xs + dx).tolist(), (ys + dy).tolist()))
    h = hull(pts)
    return [[min(max(x, 0), M.W - 1), min(max(y, 0), M.H - 1)] for x, y in h]


def ring(x, z, rad, n=12):
    return [G(x + rad * math.cos(a), z + rad * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]


def walk_outline():
    """The lane, the little square and the landing: everything people may stand on. Not the water, the barge, the hen
    yard, the steps down into the river. A little in from the quay's edge and from the landing's edge stones."""
    Q = M.Q
    L = M.LANDING
    pts = [G(Q + 25, -20), G(Q + 25, L["z0"] + 40), G(-572, L["z0"] + 40), [1, G(-572, L["z0"] + 40)[1]], [1, 462],
           G(L["x0"] + 40, L["z1"] - 40), G(Q + 20, L["z1"] - 40), G(Q + 20, 2400.0), G(M.ROAD_X - 20, 2400.0),
           G(M.ROAD_X - 20, M.along(M.PR["s1"])[1] + 20)]
    for s in (M.PR["s1"], M.PR["s0"] + 1):                     # along the house of prayer, 25 cm off its front (it stands 20 proud)
        pts.append(F(s, 45.0))
    for s in (M.PR["s0"] - 1, M.YARD["s1"] + 20):                # along Eleazar's house, past his door, to the yard's side fence
        pts.append(F(s, 25.0))
    pts.append(F(M.YARD["s1"] + 20, M.YARD["out"] + 20))
    s = M.YARD["s1"]                                             # along the yard's fence, 20 cm off it, to the right edge
    while s > -400:
        p = F(s, M.YARD["out"] + 20)
        if p[0] >= 799:
            break
        pts.append(p)
        s -= 60.0
    # where that line leaves the picture
    lo, hi = s, s + 60.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if F(mid, M.YARD["out"] + 20)[0] >= 799 else (lo, mid)
    edge = F(hi, M.YARD["out"] + 20)
    pts += [[798, edge[1]], [798, 598]]
    out = []
    for p in pts:
        p = [min(max(p[0], 0), 799), min(max(p[1], 0), 599)]
        if not out or p != out[-1]:
            out.append(p)
    return out


def blocked():
    b = M.BENCH
    st = M.STACK
    bench_ = [F(b["s0"] - 6, 18.0), F(b["s1"] + 6, 18.0), F(b["s1"] + 6, b["out"] + b["deep"] / 2 + 4), F(b["s0"] - 6, b["out"] + b["deep"] / 2 + 4)]
    stack = [G(st["x0"], st["z0"]), G(st["x1"], st["z0"]), G(st["x1"], st["z1"]), G(st["x0"], st["z1"])]
    stack = [[min(max(x, 0), 799), y] for x, y in stack]
    return [bench_, stack]


WINDOW_BACK = 40.0                                           # how far back in the room from the wall's face he stands (cm)


def window_place():
    """Where the game stands Eleazar at his window: the floor of the upper room under his feet, a step back from the
    wall's face (the sill at his waist), and the size of a grown man there. We look at the window at a slant, so a man
    straight behind its middle would stand half behind its near jamb: he stands a little along the room, where we see him
    in the middle of the opening (he is facing the river, so he shows from the waist up). -> (window mark, his depth)"""
    w = M.WINDOW
    def xs(s, back):                                                       # the picture's x of a place s along the front, `back` cm out
        x, z = M.out(M.along(s), back)
        return M.P(x, 0.0, z)[0]
    mid_x = (xs(w["s0"], 0.0) + xs(w["s1"], 0.0)) / 2                     # the middle of the opening, on the wall's face
    lo, hi = w["s0"], w["s1"] + 100.0
    for _ in range(60):                                                    # (further along the front is further left)
        sm = (lo + hi) / 2
        lo, hi = (sm, hi) if xs(sm, -WINDOW_BACK) > mid_x else (lo, sm)
    x, z = M.out(M.along(sm), -WINDOW_BACK)
    at = M.P(x, M.EL["floor2"], z)
    return {"at": r1(at), "scale": round(M.man_scale(z), 3), "face": "W"}, z


def window_opening():
    w = M.WINDOW
    return [F(w["s0"], 0, w["sill"]), F(w["s1"], 0, w["sill"]), F(w["s1"], 0, w["top"]), F(w["s0"], 0, w["top"])]


def bench_seat():
    b = M.BENCH
    sm = (b["s0"] + b["s1"]) / 2
    x, z = M.out(M.along(sm), b["out"] + 4.0)                   # under the hips of a man sitting on its middle, facing the lane
    k = M.k_at(z)
    return {"at": r(M.P(x, 0, z)), "cm": b["h"], "px": round(b["h"] * k, 1)}


def hens_row():
    hr = M.HENS_ROW
    return [F(hr["s0"], hr["o0"]), F(hr["s1"], hr["o1"])]


def marks():
    win, wz = window_place()
    m = {
        "fromBridge": [520, 562], "toBridge": [520, 596], "default": [470, 528],
        "mariam": {"at": F(170, 150), "face": "W"},
        "mariam_spots": [F(80, 120) + ["W"], F(250, 90) + ["SW"]],
        "mariam_talk": F(240, 300),
        "felix": {"at": G(-520, 520), "face": "W"},
        "felix_spots": [G(-560, 592) + ["NW"], G(-540, 450) + ["E"]],
        "petosiris": G(-420, 598),
        "door": F(500, 40),
        "wait": [520, 427],                                    # beside the bench's near end, just in front of it
        "window": win,
        "window_opening": window_opening(),
        "bench_seat": bench_seat(),
        "pray_eleazar": F(830, 130) + ["W"],
        "pray_son": F(660, 150) + ["W"],
        "bless": F(850, 165) + ["E"],
        "hens": hens_row(),
    }
    return m


FX_NOTE = ("Nothing that moves by nature is in the paint; these move it. The river: river-shimmer, glints that come and drift "
           "downstream (up the picture and to the right, toward the bend) over the painting's own still sparkle, the barge a hole "
           "in it; barge-ripples (two) where the water laps along the barge between it and the quay; steps-ripples at the foot of "
           "the landing's steps, in the very corner (clipped to the stair and the water seen past the quay's edge; under the "
           "inventory bar while the game waits for a click). The barge rides at its moorings: barge-bob (ENGINE-13R's bob, as the "
           "brief gives it), the water painted whole under it, and the curb cut-out in front of the foot of its bow, so that a "
           "pixel up or down shows only water and stone. The five hens: one flock of one each (so that each keeps her own "
           "colouring and her place in the row, which runs from in front of the coop back toward the house), depth true (sized by "
           "their row from frames sizeAt 590), shy 0, never flying, turning or pecking: they stand, look up and shuffle, facing "
           "west over the river at the city. The washing sways on its line (washing-sway, its cut-out hung from the top). A thin "
           "cooking smoke rises behind the houses beyond the house of prayer (plane back). Swallows over the river and the far "
           "bank: the temple steps' swallow frames (rome_steps_birds.py), from that scene's folder.")


def hen_perches():
    """The hens' row, one short perch each (a flock of one: the engine places a flock's birds anywhere along its perch, so
    each hen keeps her own place in the row, and her own colouring): -> [(set, end, end)]."""
    return [(name, F(s - 9, o), F(s + 9, o)) for name, s, o in M.HENS]


def yard_people():
    """Where anyone in the hen yard can be: Mariam at her place and her spots, every hen from end to end of her perch."""
    m = marks()
    return [m["mariam"]["at"]] + [q[:2] for q in m["mariam_spots"]] + [p for _, a, b in hen_perches() for p in (a, b)]


def fence_rows():
    """The two fence cut-outs each lie at one depth, a row, so that the engine's order is the same whoever stands where
    (with a slanted base line, a boy in front of the fence's corner and Mariam behind its near run, lower on the screen
    than he is, make a ring that its sort cannot lay right: rome_tiber_order.py). The near run's row is below everyone
    in the yard. Nobody in the yard stands where the corner piece is on the screen (Mariam and the hens keep to the
    right of the side fence's far end), so the corner's row only has to be below its own foot, and above everyone beyond
    the side fence, by the door. Where the lane in front of the fence is above those rows, a solid keeps people off it.
    -> {id: (row, solid)}"""
    yd = M.YARD
    corner, split, wall = F(yd["s1"], yd["out"]), F(yd["split"], yd["out"]), F(yd["s1"], 0)
    yp = yard_people()
    near_row = max(y for x, y in yp) + 4
    corner_row = corner[1] + 4                                   # (nobody in the yard comes in front of the corner on the screen:)
    assert min(x for x, y in yp) > wall[0] + 18, "someone in the yard would stand behind the side fence on the screen"
    assert corner[1] < corner_row < split[1] < near_row
    foot_x = corner[0] + (corner_row - corner[1]) * (split[0] - corner[0]) / (split[1] - corner[1])
    corner_solid = [[corner[0] - 5, corner[1] - 2], [corner[0] + 2, corner[1] - 2], [int(math.ceil(foot_x)), corner_row], [corner[0] - 5, corner_row]]
    near_solid = [[split[0] - 3, split[1] - 4], [split[0] + 25, split[1] - 4], [split[0] + 25, near_row], [split[0] - 3, near_row]]
    return {"fence-corner": (corner_row, corner_solid), "fence": (near_row, near_solid)}


def landing_shape():
    """The landing's near end, where nobody stands: its edge stones, the bollard at its corner with the rope, and the steps
    down into the river below them (the walkable landing above is left to walk on)."""
    L, S = M.LANDING, M.STEPS
    bx, bz = S["x1"] + 34, L["z0"] + 18
    top = r(M.P(bx, 66.0, bz))
    foot = G(bx + 30, bz - 6)
    near = G(L["x1"], L["z0"])
    wedge = steps_wedge()
    return [[0, near[1] - 8], [top[0] - 16, near[1] - 8], [top[0] - 14, top[1]], [top[0] + 16, top[1]], [top[0] + 18, foot[1] + 2]] + wedge[1:]


def steps_wedge():
    """What is seen past the quay's edge at the bottom-left corner below the landing: the stair and the water at its foot
    (the quay's edge is a straight line in the picture, from the landing's near corner down out of the bottom edge)."""
    (x1, y1), (x2, y2) = M.P(M.Q, 0.0, M.LANDING["z0"]), M.P(M.Q, 0.0, 0.0)
    xb = x2 + (x2 - x1) * (600 - y2) / (y2 - y1)
    return [[0, int(round(y1))], [int(math.floor(x1)), int(round(y1))], [int(math.floor(xb)), 600], [0, 600]]


def fx(info, cut):
    """The things that move by nature, in the engine's own fields (DESIGN.md section 2), with notes the engine passes over."""
    wl = lambda x: float(M.HZ + (M.EYE - M.WATER) * M.F * (M.VX - x) / (-M.FAR_BANK * M.F))
    river = [[0, round(wl(0) + 1)], [120, round(wl(120) + 1)], [240, round(wl(240) + 1)], [300, round(wl(300) + 1)], r(M.P(M.Q, M.WATER, 30000.0)),
             r(M.P(M.Q, 0, 4000.0)), r(M.P(M.Q, 0, M.LANDING["z1"])), G(M.LANDING["x0"], M.LANDING["z1"]), [0, G(M.LANDING["x0"], M.LANDING["z1"])[1] + 2]]
    hull_barge = hull_of_mask(cut["barge"][1], pad=1)
    B = M.BARGE
    side = lambda t: r(M.P(B["xs"] + 2, M.WATER, B["z0"] + t * (B["z1"] - B["z0"])))
    hens = []
    for i, (name, a, b) in enumerate(hen_perches()):
        hens.append({"id": f"hen-{i + 1}", "type": "birds", "kind": "flock", "what": f"one of Mariam's hens ({name}), standing in the row with the others, looking over the river",
                     "perch": [a, b], "count": 1, "frames": HENS.frames_block(name), "depth": True, "shy": 0, "fly": False, "turn": False,
                     "walk": 4, "moves": {"stand": 3, "look": 2, "walk": 0.5, "peck": 0, "turn": 0}, "seed": i + 1})
    marks_ = [
        {"id": "river-shimmer", "type": "shimmer", "what": "the sun on the river: glints that come and drift downstream and go",
         "poly": river, "holes": [hull_barge], "count": 46, "size": 7, "flow": [3.5, -1.8], "life": 1.6, "color": "#fff4d8", "opacity": 0.55,
         "note": "The painting's own glints and its broad shine toward the sun (left) stay; this adds the moving ones. The barge is a hole."},
        {"id": "barge-ripples", "type": "ripples", "what": "the water lapping along the barge's side, between it and the quay",
         "at": side(0.42), "radius": [3, 14], "flat": 0.22, "every": [1.2, 3.0], "rings": 1, "speed": 10, "color": "#e8e4d8", "trough": "#3e4a4a", "opacity": 0.45},
        {"id": "barge-ripples-2", "type": "ripples", "at": side(0.68), "radius": [2, 10], "flat": 0.22, "every": [1.6, 3.5], "rings": 1, "speed": 8,
         "color": "#e8e4d8", "trough": "#3e4a4a", "opacity": 0.4, "seed": 2},
        {"id": "steps-ripples", "type": "ripples", "what": "where the river laps the lowest step down from the landing (bottom left)",
         "at": r(M.P(-490.0, M.WATER, M.LANDING["z0"] - 4 * M.STEPS["tread"])), "radius": [2, 9], "flat": 0.22, "every": [1.4, 3.2], "rings": 2,
         "speed": 8, "color": "#f0ead8", "trough": "#4a4a40", "opacity": 0.5, "clip": [steps_wedge()],
         "note": "In the very corner, below the quay's edge (the clip is the stair and the water seen past the quay): under the inventory bar "
                 "while the game waits for a click, seen in the cut-scenes."},
        {"id": "barge-bob", "type": "bob", "plane": "barge", "amount": 1, "period": 5,
         "what": "the barge riding the water at its moorings",
         "note": "The water is painted complete under it, and the landing's edge stones (the cut-out curb, in front of it) cover the foot of its "
                 "bow where it lies behind the landing, so a pixel up or down shows nothing but water and stone."},
    ] + hens + [
        {"id": "washing-sway", "type": "sway", "plane": "washing", "anchor": "top", "amount": 1, "period": 3.6, "wave": 40, "lean": 0.3,
         "what": "the washing on the line between Eleazar's two upper windows, stirring"},
        {"id": "cooking-smoke", "type": "smoke", "plane": "back", "what": "a thin smoke from a cooking fire, rising behind the houses beyond the house of prayer",
         "at": [492, 128], "height": 70, "width": [2, 14], "lean": [-22, -70], "rise": 10, "rate": 2.5, "gust": 0.3, "color": "#f2ede6", "opacity": 0.32},
        {"id": "birds-river", "type": "birds", "kind": "flyers", "plane": "back", "what": "swallows over the river, back for the spring",
         "lanes": [[[-12, 132], [90, 112], [200, 128], [300, 96], [412, -12]], [[-12, 60], [80, 86], [170, 70], [260, 40], [330, -12]]],
         "frames": {"flap": ["swallow-1.png", "swallow-2.png", "swallow-3.png", "swallow-2.png"], "glide": "swallow-4.png", "middle": [8, 5]},
         "dir": "art/scenes/rome-steps/", "scale": 1, "every": [7, 16], "group": [1, 2], "speed": 110,
         "note": "The temple steps' swallow frames (rome_steps_birds.py), from that scene's folder. The lanes keep over the river and the far bank, "
                 "clear of the houses' roofs (which are in back.png)."},
        {"id": "birds-far", "type": "birds", "kind": "flyers", "plane": "back", "what": "more of them far off over the far bank",
         "lanes": [[[-12, 168], [100, 150], [210, 176], [330, 140], [360, -12]]],
         "frames": {"flap": ["swallow-1.png", "swallow-2.png", "swallow-3.png", "swallow-2.png"], "glide": "swallow-4.png", "middle": [8, 5]},
         "dir": "art/scenes/rome-steps/", "scale": 0.55, "every": [8, 18], "group": [1, 3], "speed": 70, "seed": 3},
    ]
    return marks_


def things(info, cut):
    """Every thing to click: id, what, a shape hugging it, a place to stand (on the floor, reachable), a facing. Small
    things before the big ones they lie on (where two shapes overlap, the earlier one is meant)."""
    w = M.WINDOW
    sh = [F(w["s0"] - 101, -4, w["sill"]), F(w["s0"] - 101, -4, w["top"]), F(w["s1"] + 12, -2, w["top"] + 14), F(w["s1"] + 12, -5, w["sill"] - 7),
          F(w["s0"] - 101, -4, w["sill"] - 7)]
    mz = M.MEZUZAH
    mzc = F((mz["s0"] + mz["s1"]) / 2, 0, (mz["h0"] + mz["h1"]) / 2)
    D_ = M.DOOR_E
    DP = M.DOOR_P
    b = M.BENCH
    st = M.STACK
    L, S = M.LANDING, M.STEPS
    # the yard as the picture shows it, where the hens are: its floor from a line across it (at s 320, short of the side
    # fence) to the picture's edge, between the fence's foot and the house's foot, with the fence and the hens' heads over
    # the house's foot; the lane in front of the fence, and the side fence with the door beyond it, left out
    fe = lambda s, o: M.out(M.along(s), o)
    cut_s, head = 320.0, 24                                      # (a hen's head over the house's foot, px)
    edge_fence, edge_house = r(M.P(*_edge(fe, M.YARD["out"]))), r(M.P(*_edge(fe, 0.0)))
    a_fence, a_house = F(cut_s, M.YARD["out"]), F(cut_s, 0)
    assert max(x for x, y in yard_people()) < 799 and min(x for x, y in yard_people()) > a_house[0] - 12
    hens_shape = [a_fence, [799, edge_fence[1]], [799, edge_house[1] - head], [a_house[0], a_house[1] - head], a_house]
    river_poly = fx(info, cut)[0]["poly"]
    wl0 = river_poly[0]
    farbank = [[0, 148], [40, 146], [90, 154], [140, 168], [190, 186], [240, 212], [290, 234], [330, 244], [370, 250], [372, 256], [240, 260], [120, 266], [0, 272]]
    road = [G(M.Q + 20, 1500.0), G(M.ROAD_X, 1500.0), G(M.ROAD_X, 9000.0), G(M.Q, 9000.0)]
    gardens = [[300, 214], [442, 206], [442, 262], [300, 262]]
    t = [
        {"id": "doorpost", "what": "the little case fixed upright on the right-hand post of Eleazar's door (words of the Law: not seen)",
         "shape": {"rect": [mzc[0] - 6, mzc[1] - 10, 12, 20]}, "stand": F(450, 70), "face": "E"},
        {"id": "window", "what": "Eleazar's upper window, open, its shutter folded back (in the first scene he stands in it, praying)",
         "shape": {"poly": hull(window_opening() + sh)}, "stand": F(250, 330), "face": "E"},
        {"id": "washing", "what": "the washing on the line between his two upper windows: a small tunic, a blue cloth",
         "shape": {"poly": hull_of_mask(cut["washing"][1], 3)}, "stand": F(410, 300), "face": "E"},
        {"id": "figtree", "what": "a fig tree in first leaf, in the hen yard", "shape": {"poly": hull_of_mask(info["fig_a"], 2)},
         "stand": F(-40, 300), "face": "E"},
        {"id": "bench", "what": "the stone bench before the house of prayer", "shape": {"poly": hull(blocked()[0] + [F(b["s0"], b["out"] - 19, b["h"] + 3), F(b["s1"], b["out"] - 19, b["h"] + 3)])},
         "stand": [520, 427], "face": "N"},
        {"id": "well", "what": "the well: a round stone curb, a bucket on its rim", "shape": {"poly": hull_of_mask(cut["well"][1], 2)},
         "stand": G(M.WELL["x"] + 30, M.WELL["z"] - 110), "face": "N"},
        {"id": "bales", "what": "bales of papyrus rolled in mats, a bolt of linen and two tall jars, waiting on the landing to go aboard",
         "shape": {"poly": hull([[max(0, x), y] for x, y in [G(st["x0"], st["z0"]), G(st["x1"], st["z0"]), G(st["x1"], st["z1"]), G(st["x0"], st["z1"]),
                                                              r(M.P(st["x1"], 115, st["z0"])), r(M.P(st["x1"], 100, st["z1"])), r(M.P(st["x0"], 115, st["z0"]))]])},
         "stand": G(-540, 380), "face": "NW"},
        {"id": "landing", "what": "the stone landing: its steps down into the river, a bollard and a coil of rope",
         "shape": {"poly": landing_shape()},
         "stand": G(-470, 400), "face": "S"},
        {"id": "barge", "what": "the barge moored off the quay: a towing mast, a steering oar, piled with bales and jars and linen",
         "shape": {"poly": hull_of_mask(cut["barge"][1], 1)}, "stand": G(-430, 560), "face": "W"},
        {"id": "doorway", "what": "Eleazar's door, standing open", "shape": {"poly": [F(D_["s0"], 0, 0), F(D_["s1"], 0, 0), F(D_["s1"], 0, D_["h"] + 18), F(D_["s0"], 0, D_["h"] + 18)]},
         "stand": F(500, 70), "face": "E"},
        {"id": "house", "what": "Eleazar's house: plastered, two storeys, its door and window to the river", "shape": {"poly": [F(-40, 0), F(M.EL["s1"], 0),
                                                                                                                                F(M.EL["s1"], 0, 640), F(-40, 0, 640)]},
         "stand": F(480, 110), "face": "E"},
        {"id": "prayerhouse", "what": "the house of prayer: plain, a broad door, two small windows high up; no statue, picture or carving",
         "shape": {"poly": [F(M.PR["s0"], 20), F(M.PR["s1"], 20), F(M.PR["s1"], 20, 590), F(M.PR["s0"], 20, 590)]},
         "stand": F((DP["s0"] + DP["s1"]) / 2, 110), "face": "E"},
        {"id": "hens", "what": "the hen yard: a wattle fence, a coop, a dish of water, and the hens standing in a row looking over the river",
         "shape": {"poly": hens_shape}, "stand": F(200, 300), "face": "E"},
        {"id": "gardens", "what": "Caesar's gardens, far down the road where the river bends: a long wall, a gateway, pines and cypresses over it",
         "shape": {"poly": gardens}, "stand": G(-20, 1700), "face": "N"},
        {"id": "road", "what": "the road on south along the river, toward Caesar's gardens", "shape": {"poly": road}, "stand": G(-20, 1700), "face": "N"},
        {"id": "farbank", "what": "the far bank: the Aventine, its houses and temples, the quays and long warehouses along the shore",
         "shape": {"poly": farbank}, "stand": G(M.Q + 30, 900), "face": "W"},
        {"id": "river", "what": "the river, brown and quick, shining toward the sun", "shape": {"poly": river_poly}, "stand": G(M.Q + 30, 1200), "face": "W"},
    ]
    return t


def layout(info, cut):
    win, wz = window_place()
    seat = bench_seat()
    fe = lambda s, o: M.out(M.along(s), o)
    rows = fence_rows()
    things_ = things(info, cut)
    barge_row = G(M.Q, M.BARGE["z0"])[1]                         # the quay's edge level with the barge's bow
    curb_row = barge_row + 4                                      # just in front of it: the curb hides the foot of its bow
    edge_row = G(M.STEPS["x1"] + 34, M.LANDING["z0"] + 18)[1]     # the landing's near corner: the bollard's foot
    landing_rows = (G(-500, M.LANDING["z1"] - 40)[1], G(-500, M.LANDING["z0"] + 40)[1])       # where people stand on the landing (walk_outline)
    assert barge_row < curb_row < landing_rows[0] and landing_rows[1] < edge_row
    assert curb_row < rows["fence-corner"][0] < rows["fence"][0] < edge_row
    out = {
        "id": "rome-tiber", "horizon": M.HZ, "full": M.FULL,
        "light": "the sun low, ahead and to the left over the far bank: the river shines, the far bank stands against the light, faces "
                 "toward us are in shade, the two near house fronts take the sun at a slant; shadows fall toward us and to the right",
        "walk": walk_outline(),
        "blocked": blocked(),
        "planes": [                                            # back to front, as the engine lays them (rome_tiber_order.py)
            {"id": "well", "file": "well.png", "base": G(M.WELL["x"], M.WELL["z"] - M.WELL["r"])[1], "solid": ring(M.WELL["x"], M.WELL["z"], M.WELL["r"] + 8),
             "what": "the well's curb and its bucket"},
            {"id": "window-wall", "file": "window-wall.png", "base": [F(0, 0), F(M.EL["s1"], 0)], "solid": None,
             "what": "the front of Eleazar's house round his upper window, everything of it within a man's height of the opening, the opening clear: "
                     "cut from back.png itself. A man standing in the room behind it shows only through the opening."},
            {"id": "washing", "file": "washing.png", "base": [F(0, 0), F(M.EL["s1"], 0)], "solid": None,
             "what": "the washing on its line (it sways: fx washing-sway); its base is the house front's, and it comes after window-wall"},
            {"id": "barge", "file": "barge.png", "base": barge_row, "solid": None,
             "what": "the barge (it rides the water: fx barge-bob). Its base is a row: the quay's edge level with its bow. Everyone on the "
                     "landing (row 452 and lower) is in front of it, and nobody on the quay beyond comes near it on the screen (the "
                     "strip of water between it and the quay's edge lies between). A row, not the quay's slanted edge, so that the engine's "
                     "back-to-front order is the same whoever stands where (rome_tiber_order.py)."},
            {"id": "curb", "file": "curb.png", "base": curb_row, "solid": None,
             "what": "the landing's edge stones along its far side and its river side, and the bollard at its far corner: in front of the "
                     "barge (they hide the foot of its bow, so that it can ride the water behind them), behind everyone on the landing"},
            {"id": "fence-corner", "file": "fence-corner.png", "base": rows["fence-corner"][0], "solid": rows["fence-corner"][1],
             "what": "the hen yard's fence by the door: its side, its corner post, and its front as far as the stake where the near run "
                     "begins. Its base is a row (see fence): the hens and Mariam are behind it; its solid keeps the lane clear just in "
                     "front of the corner, above that row"},
            {"id": "fence", "file": "fence.png", "base": rows["fence"][0], "solid": rows["fence"][1],
             "what": "the near run of the hen yard's wattle fence, from the picture's right edge to the stake where fence-corner begins. "
                     "Its base is a row below everyone in the yard (Mariam, her spots, every hen's perch) and above everyone on the lane "
                     "who comes in front of it on the screen; its solid keeps the lane clear where it meets fence-corner"},
            {"id": "landing-edge", "file": "landing-edge.png", "base": edge_row, "solid": ring(M.STEPS["x1"] + 34, M.LANDING["z0"] + 18, 26.0, 10),
             "what": "the landing's near edge stones each side of the steps, the bollard at its near corner and a coil of rope (bottom left): "
                     "in front of everyone on the landing; people on the quay nearer us pass in front of it (so not the front plane). Its "
                     "base is the bollard's foot; its solid, the bollard"},
        ],
        "things": things_,
        "marks": marks(),
        "exits": [{"to": "rome-forum", "edge": "S", "name": "back over the stone bridge", "walkTo": [520, 596], "spawn": "fromBridge", "arrive": [520, 562],
                   "band": "rows 548 to 600; from x %d to %d no thing to click covers it, and the floor there is open" % band_free(things_)}],
        "fx": fx(info, cut),
        "fx_note": FX_NOTE,
        "frames": {name: dict(HENS.frames_block(name), files=f"hen-{name}-<n>.png, n 1 to 6", acts=HENS.ACTS,
                              note="1-3 stand (the head as it is, turned a little toward us, a little lower), 4 look (the head up, still), "
                                   "5-6 walk (a shuffle). Facing west, as painted. No peck: they will not eat.") for name in HENS.SETS},
        "sizes": {
            "grown_man_px_at_fromBridge": round(160 * row_scale(562), 1),
            "grown_man_px_at_bench": round(160 * row_scale(seat["at"][1]), 1),
            "grown_man_px_at_felix": round(160 * row_scale(G(-520, 520)[1]), 1),
            "grown_man_px_at_window": round(160 * win["scale"], 1),
            "hen_px_in_yard": round(HENS.SIZE * row_scale(hens_row()[0][1]), 1) if True else None,
            "hen_px_in_yard_far_end": round(HENS.SIZE * row_scale(hens_row()[1][1]), 1),
        },
    }
    return out


def band_free(things_, rows=(548, 600)):
    """The columns of the bottom band that no thing's shape covers: -> (first, last), checked to run unbroken."""
    from PIL import Image, ImageDraw
    im = Image.new("L", (M.W, M.H), 0)
    d = ImageDraw.Draw(im)
    for t in things_:
        sh = t["shape"]
        if "rect" in sh:
            x, y, w, h = sh["rect"]
            d.rectangle([x, y, x + w, y + h], fill=255)
        else:
            d.polygon([tuple(p) for p in sh["poly"]], fill=255)
    cov = np.asarray(im)[rows[0]:rows[1]] > 0
    free = [x for x in range(M.W) if not cov[:, x].any()]
    assert free and free[-1] - free[0] + 1 == len(free)
    return free[0], free[-1]


def _edge(fe, o):
    """Where the line o cm out from the front leaves the picture at its right edge: -> world (x, y, z)."""
    lo, hi = -400.0, M.YARD["s1"]
    for _ in range(50):
        mid = (lo + hi) / 2
        x, z = fe(mid, o)
        lo, hi = (mid, hi) if M.P(x, 0, z)[0] >= 799.5 else (lo, mid)
    x, z = fe(hi, o)
    return (x, 0.0, z)

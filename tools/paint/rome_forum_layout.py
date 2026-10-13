"""The Forum's layout.json (rome_forum.py writes it): every number the scene file needs, measured from the finished
picture and its cut-outs: the walk outline, the blocked ground, the cut-outs and their bases, the things to click
(shapes traced round the painted things), the marks, the ways out, the things that move by nature (fx), and how big a
grown man is at the main places. Also the check picture that draws all of it over the painting.

(The shapes are traced with OpenCV, which the paints need anyway: tools/paint/README.md, "The paints".)"""

import json
import math

import numpy as np
from PIL import Image, ImageDraw

from rome_forum_kit import *
import rome_forum_things as T
import rome_forum_far as Fm

r1 = lambda p: [round(float(p[0]), 1), round(float(p[1]), 1)]
ri = lambda p: [int(round(float(p[0]))), int(round(float(p[1])))]
MIN_SCALE = 0.15


def outline(mask, pad=2, eps=1.2, keep_big=True):
    """A polygon hugging a mask a few pixels outside its edge (its biggest blob)."""
    import cv2
    m = (np.asarray(mask) > 0.5).astype(np.uint8)
    if pad:
        m = cv2.dilate(m, np.ones((2 * pad + 1, 2 * pad + 1), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not cs:
        return None
    c = max(cs, key=cv2.contourArea)
    c = cv2.approxPolyDP(c, eps, True)
    return [[int(p[0][0]), int(p[0][1])] for p in c]


def ground_poly(points_xD):
    return [ri(pt(x, 0, D)) for x, D in points_xD]


def box_foot(x0, x1, D0, D1):
    return ground_poly([(x0, D0), (x1, D0), (x1, D1), (x0, D1)])


def circle_foot(x, D, r, n=10):
    return ground_poly([(x + r * math.cos(a), D + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)])


def adult_px(row):
    return round(160 * max(MIN_SCALE, scale_at(row)), 1)


# ---------------------------------------------------------------- the floor
def walk_outline():
    """The outline of the floor people walk on (see rome_forum.py's PLAN): the square from the bottom edge to the foot of
    the temple of Saturn's steps, between Castor's steps and the hoarding and the colonnade of Paullus, and into the mouth
    of the Tuscan street, round behind Castor's corner."""
    fr, L = T.hoard_frame()
    kf = castor_frame()
    c = CASTOR
    # where the hoarding's foot meets the right edge, and its far end
    u_edge = next(u for u in np.arange(0, L, 2.0) if fr.pt(u, 0, 0)[0] >= 799.0)
    off = lambda p, dx, dy: [p[0] + dx, p[1] + dy]
    right_edge = fr.pt(u_edge, -60, 0)                                     # a little in front of the hoarding
    hoard_far = fr.pt(0, -60, 0)
    yard_a = pt(HOARD["b"][0] - 50, 0, HOARD["b"][1] + 30)                  # round the hoarding's far end
    # and from there straight to the front of the colonnade, no nearer its near end than the picture's column 590: the
    # floor between the site and the colonnade's near end is hidden by the hoarding, and anyone walking there would show
    # his head over the boards in front of the new wall, which stands nearer us than he does (and is in the backdrop)
    yard_b = pt(PAULLUS["x"] - 60, 0, 800.0 * (PAULLUS["x"] - 60) / (590.0 - VX))
    paullus_far = pt(PAULLUS["x"] - 60, 0, 6200.0)
    rostra = ROSTRA
    front = []
    for t in np.linspace(1, 0, 7):                                        # along the front of the speakers' platform, a step out
        x = rostra["x0"] + (rostra["x1"] - rostra["x0"]) * t
        D_ = rostra["D"] - rostra["bulge"] * math.sin(math.pi * t) - 90
        front.append(pt(x, 0, D_))
    left_end = pt(rostra["x0"] - 40, 0, rostra["D"] - 90)
    sf = Fm.saturn_frame()
    vfoot = Fm.S_VK(1) - 30
    u_r = next(u for u in np.arange(Fm.S_SU1, Fm.S_SU0, -5.0) if sf.pt(u, vfoot, 0)[0] <= left_end[0] - 2)
    sat_a = sf.pt(u_r, vfoot, 0)                                            # the foot of Saturn's steps, left of the platform
    sat_b = sf.pt(Fm.S_SU0 + 30, vfoot, 0)
    j = JULIA
    julia_far = pt(j["x"] + 60, 0, j["D1"] - 120)
    julia_near = pt(j["x"] + 50, 0, j["D0"] - 40)
    street_in = (124.0, 297.0)                                              # in the street's mouth, behind Castor's corner, out of sight
    street_low = (122.0, 320.0)
    castor_back = kf.pt(c["width"] + 40, T.CASTOR_BACK, 0)
    castor_front = kf.pt(c["width"] + 40, -c["porch"], 0)
    steps_end = kf.pt(c["width"] + 30, castor_steps_foot() - 30, 0)
    steps_left = next(kf.pt(u, castor_steps_foot() - 30, 0) for u in np.arange(c["width"], -3000, -5.0) if kf.pt(u, castor_steps_foot() - 30, 0)[0] <= 0.5)
    pts = [[0, 597], [797, 597], right_edge, hoard_far, yard_a, yard_b, paullus_far] + front + [left_end, sat_a, sat_b, julia_far, julia_near,
           street_in, street_low, castor_back, castor_front, steps_end, steps_left]
    out = [ri(p) for p in pts]
    out = [[min(max(p[0], 0), 799), min(max(p[1], 0), 599)] for p in out]
    return out


def blocked():
    """Ground that painted things stand on, inside the walk outline (the cut-outs' own patches are their `solid`s)."""
    out = []
    for (bx, bD, bh, bw, kind) in BASKETS:                                  # Phyllis's baskets
        if bh < 1:
            out.append(box_foot(bx - bw / 2 - 4, bx + bw / 2 + 4, bD - bw * 0.4, bD + bw * 0.4))
    out.append(box_foot(POLE[0] - 16, POLE[0] + 16, POLE[1] - 12, POLE[1] + 12))     # her pole of garlands
    return out


def solids():
    """Each cut-out's patch of ground (`solid`)."""
    b, p, tb, f = BASIN, PUTEAL, TABLE, FRONT_BASE
    out = {
        "basin": box_foot(b["x0"], b["x1"], b["D0"], b["D1"]),
        "puteal": circle_foot(p["x"], p["D"], p["r"] + 8),
        "table": box_foot(tb["x"] - tb["w"] / 2 - 8, tb["x"] + tb["w"] / 2 + 8, tb["D"] - tb["d"] / 2 - 8, tb["D"] + tb["d"] / 2 + 90),
        "front-base": box_foot(f["x"] - f["w"] / 2 - 8, f["x"] + f["w"] / 2 + 8, f["D"] - f["d"] / 2 - 8, f["D"] + f["d"] / 2 + 8),
    }
    for i, (x, D_, hc) in enumerate(STATUES):
        out[f"statue-{i + 1}"] = box_foot(x - 66, x + 66, D_ - 66, D_ + 66)
    return out


def bases():
    b, p, tb, f = BASIN, PUTEAL, TABLE, FRONT_BASE
    out = {
        "castor": T.castor_base_line(),
        "basin": round(pt(0, 0, b["D0"])[1], 1),
        "puteal": round(pt(p["x"], 0, p["D"] - p["r"] - 6)[1], 1),
        "table": round(pt(tb["x"], 0, tb["D"] - tb["d"] / 2 - 6)[1], 1),
        "awning": round(pt(tb["x"], 0, tb["D"] - tb["d"] / 2 - 6)[1], 1),
        "hoarding": T.hoarding_base_lines()[0],
        "hoarding-near": T.hoarding_base_lines()[1],
        "front-base": round(pt(f["x"], 0, f["D"] - f["d"] / 2 - 8)[1], 1),
    }
    for i in range(3):
        out[f"statue-{i + 1}"] = T.statue_base_row(i)
    return out


# ---------------------------------------------------------------- the marks
def marks():
    """Every mark the scene needs, [x, y] or [x, y, face]. (Checked against the engine's walk map: forum-walkcheck.mjs.)"""
    fr, L = T.hoard_frame()
    g0, g1 = T.hoard_gate()
    sf = Fm.saturn_frame()
    foot = sf.pt(Fm.S_SU0 + 140, Fm.S_VK(1) - 40, 0)
    out = {
        "toSteps": ri(sf.pt(Fm.S_SU0 + 150, Fm.S_VK(1) - 60, 0)),                 # at the foot of the temple of Saturn's steps
        "fromSteps": ri(sf.pt(Fm.S_SU0 + 150, Fm.S_VK(1) - 560, 0)) + ["S"],      # a step out, toward us
        "toTiber": [136, 306],                                                    # in the mouth of the Tuscan street, behind Castor's corner
        "fromTiber": [214, 318, "E"],                                             # a step out of it, on the square
        "toHouse": [600, 596],                                                    # the bottom edge, for the later stage
        "fromHouse": [600, 556, "N"],
        "default": [420, 470, "S"],
        # the Gaul: in front of the hoarding, facing it; along it; out in the square; the gateway; behind it
        "gaul": ri(fr.pt(1030, -95, 0)) + ["E"],
        "gaul_spots": [ri(fr.pt(560, -90, 0)) + ["NE"], ri(fr.pt(1200, -100, 0)) + ["E"], [528, 452, "W"]],     # (the second clear of the statue base at the front)
        "gate": ri(fr.pt((g0 + g1) / 2, 10, 0)),
        "behind": ri(fr.pt(910, 70, 0)),            # just inside, by the near gatepost: wholly hidden by hoarding-near (see ready.md: why this row)
        # Phyllis: the ground under her hips on her low stool, facing the square; where she stands to hang a garland
        "phyllis": ri(pt(PHYLLIS[0], 0, PHYLLIS[1])) + ["SE"],
        "phyllis_stand": ri(pt(POLE[0] - 42, 0, POLE[1] - 50)) + ["E"],
        # for the later stage, left clear now
        "paetus": ri(pt(TABLE["x"], 0, TABLE["D"] + TABLE["d"] / 2 + 52)) + ["S"],
        "vibius": ri(fr.pt((g0 + g1) / 2, 0, 0)) + ["W"],                      # on the gateway's threshold, where the boards do not hide him
        "demetrius": ri(pt(STATUES[0][0] + 150, 0, STATUES[0][1] - 40)) + ["W"],
    }
    return out


def things(cut, layers):
    """Every thing to click: its shape traced round the painted thing, where to stand to use it, which way to face.
    Small things before the big ones they lie in (where two shapes overlap, the earlier is meant)."""
    a = lambda name: cut[name][1] > 0.5
    L = layers
    fr, Lh = T.hoard_frame()
    t = []

    def add(id_, what, shape, stand, face, **more):
        if shape:
            t.append(dict(id=id_, what=what, shape={"poly": shape}, stand=ri(stand) if len(stand) == 2 else stand, face=face, **more))
    tb = TABLE
    add("table", "the moneychanger's table by the Puteal, set out and waiting for him: his scales and stacks of coin under a striped cloth, his stool, the little awning",
        outline(a("table") | a("awning")), pt(tb["x"] + tb["w"] / 2 + 70, 0, tb["D"] - 60), "W")
    p = PUTEAL
    add("puteal", "the Puteal: a round kerb of white stone, carved with garlands and lyres, round a spot struck by lightning", outline(a("puteal")),
        pt(p["x"] - p["r"] - 75, 0, p["D"] - 60), "E")
    add("spring", "Juturna's spring: a square stone basin of clear water, fed at its back by the spring", outline(a("basin")),
        [64, 524], "N")
    gm = layers["garlands"].a > 0.5
    add("garlands", "Phyllis's baskets of violets, laurel and myrtle, and the pole hung with her finished garlands", outline(gm, pad=2, eps=1.5),
        [232, 492], "W")
    for i in range(3):
        x, D_, hc = STATUES[i]
        add("statues" if i == 0 else f"statues-{i + 1}", "an honorary statue on a tall column: a man in a toga, bronze gone green, one arm raised (nobody in particular)",
            outline(a(f"statue-{i + 1}")), pt(x + 230, 0, D_ - 160) if i != 1 else [500, 312], "W" if i != 1 else "E")     # (the second's clear of the awning)
    crane_m = layers["crane"].a > 0.5
    add("crane", "the big treadwheel crane in the site: its leaning frame, the great wheel at its foot, a block of white stone hanging from it", outline(crane_m, pad=2, eps=1.5),
        [610, 420], "E")                                                       # (clear of the statue base at the front, and of the Gaul's places)
    site_m = (a("hoarding") | a("hoarding-near") | (layers["site"].a > 0.5) | (layers["works"].a > 0.5)) & ~crane_m
    add("site", "the site of the new senate house: its hoarding with the gateway, and over it the new wall rising out of the pit, blocks of tufa and white stone, a timber scaffold",
        outline(site_m, pad=1, eps=1.5), fr.pt(720, -100, 0), "E")
    tus = layers["tuscan_mouth"]
    add("tuscan", "the mouth of the Tuscan street, in the long shadow of the temple of Castor: the way to the river", tus, [214, 318], "W")
    add("castor", "the temple of Castor: its high podium, its broad flight of steps, the columns of its front", outline(a("castor"), pad=1, eps=1.5), [196, 420], "N")
    jm = layers["julia"].a > 0.5
    scaf = np.zeros(SHAPE, bool)
    scaf[:, 262:300] = True
    add("scaffold", "timber scaffolding and a small crane at the far end of Caesar's basilica: it is not finished", outline(jm & scaf, pad=1), [290, 292], "W")
    add("julia", "Caesar's basilica: two storeys of arches, white and new, its near end in Castor's shadow", outline(jm & ~scaf, pad=1), [232, 312], "N")    # (in the street's mouth, looking up at its near end: clear of the statue's column)
    add("rostra", "the new speakers' platform, long and low and curved, faced with pale stone, the bronze beaks of old ships along its front, statues on it; unfinished",
        outline(layers["rostra"].a > 0.5, pad=1), [452, 290], "N")
    sm = layers["saturn"].a > 0.5
    add("saturn", "the temple of Saturn, the act's own, from across the square: six columns on a high base, the bronze doors open (the way back to the steps)",
        outline(sm, pad=1), "toSteps", "N")
    add("paullus", "the basilica of Paullus: a long two-storey colonnade, shops under it", outline(layers["paullus"].a > 0.5, pad=1), [505, 352], "E")
    for nm, what in (("records", "the record office on the slope of the Capitol: a long front of arches"),
                     ("moneta", "Juno's temple on the other summit, where the money is struck"),
                     ("jupiter", "the temple of Jupiter Best and Greatest on the Capitol, its roof of gilt bronze blazing in the sun, a bronze chariot on its peak")):
        add(nm, what, outline(layers[nm].a > 0.5, pad=2, eps=1.5), [400, 440], "N")         # (looked up at from the middle of the square, as the steps' own "forum" is from its pavement: not a walk to the far end)
    add("pigeons", "where the pigeons potter about the square", PIGEON_AREA, [470, 520], "N")
    first = ["table", "puteal", "spring", "garlands", "statues", "statues-2", "statues-3", "crane", "site", "tuscan", "castor", "scaffold", "julia", "rostra",
             "saturn", "paullus", "records", "moneta", "jupiter", "pigeons"]
    t.sort(key=lambda d: first.index(d["id"]))
    for d in t:
        if d["stand"] == "toSteps":
            d["stand"] = marks()["toSteps"]
    return t


PIGEON_AREA = [[300, 440], [520, 420], [690, 468], [712, 540], [420, 544], [250, 536]]     # (above the bottom band and the inventory bar, clear of the front base)


def tuscan_mouth():
    """The shape of the Tuscan street's mouth: the gap between Castor's corner and the basilica's near end, from the
    floor up to the basilica's roof."""
    j = JULIA
    kf = castor_frame()
    c = CASTOR
    back = kf.pt(c["width"], T.CASTOR_BACK, 0)
    top_left = kf.pt(c["width"], T.CASTOR_BACK, 900)
    return [ri(top_left), ri(pt(j["x"], j["roof"], j["D0"])), ri(pt(j["x"], 0, j["D0"])), ri(pt(j["x"] + 30, 0, j["D0"] - 300)),
            ri(pt(j["x"] + 30, 0, 3600.0)), ri(back)]


# ---------------------------------------------------------------- what moves by nature
def fx_marks(crane_wheel=None):
    """In the engine's own fields (docs/DESIGN.md, "Things that move by nature"), ready to copy into the scene; `what` and
    `note` are words the engine passes over."""
    alt = Fm.jupiter_altar()
    b = BASIN
    sx_, sy_ = pt(T.SPOUT[0], b["h"] + 10, T.SPOUT[1])
    land_ = pt(T.SPOUT[0] - 4, b["h"] - 8, T.SPOUT[1] - 38)
    water = [ri(pt(b["x0"] + b["wall"], b["h"] - 8, b["D0"] + b["wall"])), ri(pt(b["x1"] - b["wall"], b["h"] - 8, b["D0"] + b["wall"])),
             ri(pt(b["x1"] - b["wall"], b["h"] - 8, b["D1"] - b["wall"])), ri(pt(b["x0"] + b["wall"], b["h"] - 8, b["D1"] - b["wall"]))]
    water = [[min(max(p[0], 0), 799), p[1]] for p in water]
    tb = TABLE
    cr = CRANE
    block_land = pt(cr["x"] - 330, SITE_WALL["h"], cr["D"] + 300)                 # the top of the new wall, under the crane's head
    base_basin = round(pt(0, 0, b["D0"])[1] + 0.5, 1)          # a hair in front of the basin's own base: laid over its water whatever order things go on the stage
    pig = lambda set_, **more: dict({"dir": "art/scenes/rome-steps/", "set": set_, "foot": [23, 40], "face": "E", "sizeAt": 590, "stand": [1, 3], "look": [2],
                                     "peck": [4, 5], "walk": [6, 7, 8, 9], "turn": [10], "takeoff": [11, 12], "fly": [13, 14, 15], "glide": [17], "land": [18]}, **more)
    swallow = {"dir": "art/scenes/rome-steps/", "flap": ["swallow-1.png", "swallow-2.png", "swallow-3.png", "swallow-2.png"], "glide": "swallow-4.png", "middle": [8, 5]}
    marks_ = [
        {"id": "hill-smoke", "type": "smoke", "plane": "back", "what": "the thread of smoke from the Ides offering at the altar before the temple of Jupiter, far up on the Capitol",
         "at": ri(alt), "height": 46, "width": [1, 6], "lean": [14, -46], "rise": 6, "rate": 2, "gust": 0.2, "color": "#f4ecde", "opacity": 0.35,
         "note": "Tiny and slow, far behind everything: the same smoke the steps' picture marks as hill-smoke. It leans a little right, away from "
                 "Castor's corner, which hides the altar's left side."},
        {"id": "spring-stream", "type": "stream", "what": "the spring coming into Juturna's basin from the spout in its back wall",
         "path": [r1((sx_, sy_)), r1(((sx_ + land_[0]) / 2 - 1, sy_ + 4)), r1(land_)], "width": [2.0, 3.0], "speed": 40, "splash": 3, "opacity": 0.55,
         "base": base_basin, "note": "Short: the water falls a hand's breadth from the spout's mouth to the surface. Its base is half a row in "
                                     "front of the basin's, so it lies over the basin's water and behind anyone standing in front of the basin."},
        {"id": "spring-ripples", "type": "ripples", "what": "rings where the spring falls into the basin", "at": ri(land_), "radius": [1, 12], "flat": 0.30,
         "every": [0.9, 1.6], "rings": 2, "speed": 10, "opacity": 0.5, "base": base_basin, "clip": water},
        {"id": "spring-shimmer", "type": "shimmer", "what": "light coming and going on the basin's still water", "poly": water, "clip": water,
         "count": 5, "size": 5, "flow": [3, 0], "life": 2.0, "opacity": 0.40, "base": base_basin},
        {"id": "pigeons", "type": "birds", "kind": "flock", "what": "pigeons pottering on the square, in the sun, off the walkers' line up the middle",
         "area": PIGEON_AREA, "count": 5, "frames": pig("pigeon", shadow=None),
         "note": "The steps' own painted pigeons (rome-steps/pigeon-*), at their size at row 590 and smaller farther off. Their painted shadow (pigeon-shadow-1) "
                 "lies to the left, for the steps' sun; here the sun is behind-left of us and shadows fall away and to the right, so they go without it."},
        {"id": "pigeons-dark", "type": "birds", "kind": "flock", "area": PIGEON_AREA, "count": 2, "frames": pig("pigeon-dark", shadow=None), "seed": 2},
        {"id": "pigeons-far", "type": "birds", "kind": "flock", "what": "a few more far up the square, small", "area": [[300, 330], [500, 320], [560, 360], [300, 372]],
         "count": 3, "frames": pig("pigeon", shadow=None), "seed": 3},
        {"id": "swallows", "type": "birds", "kind": "flyers", "plane": "back", "what": "swallows over the Capitol, back for the spring, now and then",
         "lanes": [[[380, -12], [420, 30], [470, 60], [560, 64], [660, 40], [812, 30]], [[812, 90], [700, 72], [600, 86], [500, 70], [420, 30], [400, -12]]],
         "frames": swallow, "scale": 0.7, "every": [7, 16], "group": [1, 3], "speed": 90,
         "note": "Only in the open sky right of the temple of Jupiter, over the hill and the record office; the crane's frame crosses the right-hand lane (it is "
                 "in back.png, so a bird simply passes it: they are far behind it)."},
        {"id": "awning-sway", "type": "sway", "plane": "awning", "anchor": "top", "amount": 1.0, "period": 3.6, "lean": 0.2,
         "what": "the moneychanger's little awning stirring over his table"},
        {"id": "crane-dust", "type": "smoke", "what": "a little pale dust where the crane sets a block down on the new wall, now and then",
         "at": ri(block_land), "base": round(pt(HOARD["b"][0], 0, HOARD["b"][1])[1] - 4.0, 1), "height": 26, "width": [6, 26], "lean": [10, -20],
         "rise": 8, "rate": 3, "gust": 0.4, "color": "#e8d4a8", "opacity": 0.30,
         "note": "Meant to come and go: the scene can put it on the stage for six or eight seconds every thirty to fifty (a `when` on a timer, or "
                 "g.effects.add / remove), best just after the wheel has turned, as if the block had been set down. Its base is just above the crane wheel's (which is just above the hoarding's far end): it lies behind the "
                 "hoarding and the wheel, and behind anyone on the square."},
    ]
    if crane_wheel:
        marks_.append(crane_wheel)
    return marks_


def layout(cut, layers, crane_wheel=None, crane_plane=None):
    b = bases()
    sol = solids()
    planes = []
    for name in ["statue-3", "statue-2", "statue-1", "castor", "puteal", "table", "awning", "hoarding", "hoarding-near", "basin", "front-base"]:
        p = {"id": name, "file": name + ".png", "base": b[name]}
        if name in ("puteal", "table", "awning"):
            # a level line as wide as the thing, not a bare row: the same for anyone standing by it, but it gives the engine
            # the thing's own x when it compares two cut-outs (cast.js: at the middle of their bases), and so keeps its
            # order a true order (with a bare row, Castor's corner, the table and someone between their rows went round
            # in a circle)
            xs = np.where((cut[name][1] > 0.5).any(axis=0))[0]
            p["base"] = [[int(xs.min()), b[name]], [int(xs.max()), b[name]]]
        if name in sol:
            p["solid"] = sol[name]
        planes.append(p)
    if crane_plane:
        planes.insert(3, crane_plane)
    mk = marks()
    out = {
        "id": "rome-forum", "horizon": HZ, "full": FULL, "minScale": MIN_SCALE,
        "light": "the sun low in the east-south-east, behind our left shoulder: faces toward us lit and warm, the fronts down the left of the square in "
                 "cool shade, the colonnade on the right lit at a slant; long shadows run away from us and to the right (Castor's columns stripe the square)",
        "camera": {"horizon": HZ, "full": FULL, "eye_cm": round(EYE, 1), "focal": F, "vanish_x": VX,
                   "note": "persp.Camera(235, 590): the lens 3.9 m up on the rise of the Sacred Way. The square is told shorter than it is (some 60 m to the "
                           "foot of Saturn's steps), the Capitol at its true distance, far beyond."},
        "walk": walk_outline(),
        "blocked": blocked(),
        "planes": planes,
        "things": things(cut, layers),
        "marks": mk,
        "exits": [
            {"side": "N", "to": "rome-steps", "walkTo": mk["toSteps"], "arrive": "fromSteps", "name": "back to the steps of Saturn's temple",
             "note": "the top band (rows 0 to 60) is open sky right of the temple of Jupiter; the far temple (saturn) is also the way"},
            {"side": "W", "to": "rome-tiber", "walkTo": mk["toTiber"], "arrive": "fromTiber", "name": "down the Tuscan street, over the river",
             "note": "the left band (columns 0 to 44) is floor below row 508, in front of Juturna's basin; toTiber is behind Castor's corner, out of sight; "
                     "the street's mouth (tuscan) is also the way"},
            {"side": "S", "to": None, "walkTo": mk["toHouse"], "arrive": "fromHouse", "name": "(later: along the Sacred Way to the chief priest's house)",
             "note": "not a way in this stage: plain floor; the paving runs off the bottom edge clear of things from x 0 to 800"},
        ],
        "sizes": {"adult_px_at_fromSteps": adult_px(mk["fromSteps"][1]), "adult_px_at_toSteps": adult_px(mk["toSteps"][1]),
                  "adult_px_at_gaul": adult_px(mk["gaul"][1]), "gaul_px_at_gaul": round(1.08 * 160 * scale_at(mk["gaul"][1]), 1),
                  "adult_px_at_phyllis": adult_px(mk["phyllis"][1]), "adult_px_at_bottom": adult_px(596),
                  "boy_px_at_toSteps": round(0.74 * 160 * max(MIN_SCALE, scale_at(mk["toSteps"][1])), 1),
                  "hoarding_cm": HOARD["h"], "hoarding_px_at_gaul": round(HOARD["h"] * k(D_of(mk["gaul"][1])), 1)},
        "fx": fx_marks(crane_wheel),
    }
    return out


def check_layout(whole, lay, name):
    """A picture of the layout laid over the scene, to look at: the walk (green), blocked ground (red), the cut-outs'
    patches (orange) and bases (magenta), every shape (yellow) and place to stand (dot), the marks with a figure's box at
    the size the game draws it (blue)."""
    im = Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.polygon([tuple(p) for p in lay["walk"]], fill=(60, 255, 120, 40), outline=(60, 255, 120, 255))
    for bl in lay["blocked"]:
        d.polygon([tuple(p) for p in bl], fill=(255, 60, 60, 90), outline=(255, 60, 60, 255))
    for pl in lay["planes"]:
        if "solid" in pl:
            d.polygon([tuple(p) for p in pl["solid"]], fill=(255, 150, 40, 70), outline=(255, 150, 40, 255))
        bs = pl.get("base")
        if isinstance(bs, (int, float)):
            d.line([0, bs, 799, bs], fill=(255, 0, 255, 70))
        elif isinstance(bs, list):
            d.line([tuple(bs[0]), tuple(bs[1])], fill=(255, 0, 255, 255), width=2)
    for t in lay["things"]:
        d.polygon([tuple(p) for p in t["shape"]["poly"]], outline=(255, 255, 0, 200))
        sx, sy = t["stand"][:2]
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 255, 0, 255))
        d.text((sx + 4, sy - 5), t["id"], fill=(255, 255, 255, 255))
    for k_, v in lay["marks"].items():
        for m_ in (v if k_ == "gaul_spots" else [v]):
            mx, my = m_[0], m_[1]
            hgt = 160 * max(MIN_SCALE, scale_at(my)) * (1.08 if k_.startswith("gaul") else 0.74 if k_ in ("fromSteps", "toSteps", "fromTiber", "toTiber", "default", "fromHouse", "toHouse") else 1.0)
            d.rectangle([mx - hgt * 0.14, my - hgt, mx + hgt * 0.14, my], outline=(80, 200, 255, 255))
            d.text((mx - 10, my + 2), k_, fill=(80, 200, 255, 255))
    Image.alpha_composite(im, ov).convert("RGB").save(name)

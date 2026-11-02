"""PAINT-21D: layout.json for edo-theatre, measured through the scene's camera from the numbers the picture was painted
with (edo_theatre_model.py) and from the finished cut-outs' pixels; and the daylight's light pictures (the shafts in the
air), for the live layer."""

import math

import numpy as np

from brush import F32, blur, mask_poly, noise, lerp
from edo_keep_kit import _hull, W, H, SHAPE, P, PAPER, NAPLES, OCHRE, ipt
import edo_theatre_model as M

HZ, FULL = M.VIEW["horizon"], M.VIEW["full"]
BOTTOM = 594                                   # the lowest row a person's feet may be on (full + 34)


def r2(p):
    return [int(round(p[0])), int(round(p[1]))]


def box_of(a, pad=0):
    ys, xs = np.where(a > 0.5)
    if len(ys) == 0:
        return [0, 0, 0, 0]
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 1 + 2 * pad, int(ys.max() - ys.min()) + 1 + 2 * pad]


def grownup(y):
    return int(round(160.0 * (y - HZ) / (FULL - HZ)))


def clip_below(poly, ymax):
    """Sutherland-Hodgman: the polygon cut to y <= ymax."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        pin, qin = p[1] <= ymax, q[1] <= ymax
        if pin:
            out.append(p)
        if pin != qin:
            t = (ymax - p[1]) / (q[1] - p[1])
            out.append((p[0] + (q[0] - p[0]) * t, ymax))
    return out


def clip_x(poly, xmin, xmax):
    def side(pts, keep, at):
        out = []
        n = len(pts)
        for i in range(n):
            p, q = pts[i], pts[(i + 1) % n]
            pin, qin = keep(p), keep(q)
            if pin:
                out.append(p)
            if pin != qin:
                t = (at - p[0]) / (q[0] - p[0])
                out.append((at, p[1] + (q[1] - p[1]) * t))
        return out
    return side(side(poly, lambda p: p[0] >= xmin, xmin), lambda p: p[0] <= xmax, xmax)


def floor_poly(V, pts_cm, n=6):
    """A floor outline in cm -> picture points (each edge subdivided, so a long edge stays straight in the picture as
    it is; cut to the stage and to the lowest row)."""
    out = []
    for i in range(len(pts_cm)):
        a, b = pts_cm[i], pts_cm[(i + 1) % len(pts_cm)]
        for k in range(n):
            t = k / n
            out.append(V.pt(a[0] + (b[0] - a[0]) * t, 0.0, a[1] + (b[1] - a[1]) * t))
    out = clip_x(clip_below(out, BOTTOM), 2, W - 2)
    # thin the points: drop any within 3 px of the last kept
    kept = []
    for p in out:
        if not kept or math.hypot(p[0] - kept[-1][0], p[1] - kept[-1][1]) > 3:
            kept.append(p)
    return [r2(p) for p in kept]


def square(V, x, z, r):
    return [r2(V.pt(x - r, 0, z - r)), r2(V.pt(x + r, 0, z - r)), r2(V.pt(x + r, 0, z + r)), r2(V.pt(x - r, 0, z + r))]


def proj_rect(V, pts3, pad=2):
    pp = [V.pt(*p) for p in pts3]
    xs = [p[0] for p in pp]
    ys = [p[1] for p in pp]
    return [int(min(xs)) - pad, int(min(ys)) - pad, int(max(xs) - min(xs)) + 2 * pad + 1, int(max(ys) - min(ys)) + 2 * pad + 1]


def proj_hull(V, pts3):
    return [r2(p) for p in _hull([V.pt(*p) for p in pts3])]


# ================================================================ the daylight's light pictures
def shafts(V, info_before, info_show):
    """The daylight in the air: from each of the right wall's high windows down to its patch on the mats, and in the
    show from the roof hatch down to the stage (the hatch itself is above the backstage ceiling's edge: the shaft is
    seen below it). RGBA, a soft alpha; for the live layer (screen), under everybody, as the keep's beams are."""
    y, x = np.mgrid[0:H, 0:W].astype(F32)
    out = {}
    sun = M.SUN_WIN
    # what the air is seen against: the hall beyond the backstage's frame (below the ceiling's edge, right of the wing wall)
    edge = [V.pt(X, M.ROOF_BACK - 34, M.WING[3]) for X in np.linspace(-100, M.HALL_X1, 12)]
    ex = np.array([p[0] for p in edge])
    ey = np.array([p[1] for p in edge])
    ceil_row = np.interp(x[0], ex, ey)
    wall_x = V.pt(-100.0, 0.0, 770.0)[0]
    air = ((y > ceil_row[None, :] + 2) & (x > wall_x + 4)).astype(F32)

    def shaft(top3, land3, k):
        hull = _hull([V.pt(*p) for p in top3] + [V.pt(*p) for p in land3])
        vol = mask_poly(SHAPE, hull, soft=3.0)
        ytop = min(V.pt(*p)[1] for p in top3)
        ybot = max(V.pt(*p)[1] for p in land3)
        g = np.clip((y - ytop) / max(1.0, ybot - ytop), 0, 1)
        n = noise(SHAPE, (5, 60), 41 + len(out), 3)
        return vol * air * (0.10 + 0.10 * g) * (0.75 + 0.5 * n) * k, hull
    # the light: the paper with naples, warming toward the foot of each shaft (where it meets the dust over the mats)
    warm = np.clip((y - 200.0) / 260.0, 0, 1)[..., None]
    rgb = lerp(lerp(NAPLES, PAPER, 0.62)[None, None, :], lerp(NAPLES, OCHRE, 0.25)[None, None, :], warm * 0.6).astype(F32)
    a_house = np.zeros(SHAPE, F32)
    hulls = []
    for (z0, z1) in M.WINDOWS_RIGHT:
        top = [(M.HALL_X1, M.WIN_Y[0], z0), (M.HALL_X1, M.WIN_Y[0], z1), (M.HALL_X1, M.WIN_Y[1], z1), (M.HALL_X1, M.WIN_Y[1], z0)]
        land = []
        for X, Y, Z in top:
            t = Y / -sun[1]
            land.append((X + sun[0] * t, 0.0, Z + sun[2] * t))
        a, hull = shaft(top, land, 1.0)
        a_house = np.maximum(a_house, a)
        hulls.append([r2(p) for p in hull])
    out["shaft-house"] = (rgb, np.clip(a_house, 0, 0.6), hulls)
    x0, x1, z0, z1 = M.SKYLIGHT
    sk = M.SUN_SKY
    top = [(x0, M.ROOF, z0), (x1, M.ROOF, z0), (x1, M.ROOF, z1), (x0, M.ROOF, z1)]
    land = []
    for X, Y, Z in top:
        t = Y / -sk[1]
        land.append((X + sk[0] * t, 0.0, Z + sk[2] * t))
    a, hull = shaft(top, land, 1.15)
    out["shaft-stage"] = (rgb, np.clip(a, 0, 0.6), [[r2(p) for p in hull]])
    return out


# ================================================================ the numbers
def layout(V, pictures, iA, iAs, rooms):
    marks = {k: r2(V.pt(xz[0], 0.0, xz[1])) for k, (xz, f) in M.MARKS.items()}
    faces = {k: f for k, (xz, f) in M.MARKS.items()}
    # the dais's people sit on it, 45 cm up: their place is on its top, and their size is the floor's under them
    top = M.DAIS[4]
    for k in ("chanter", "shamisen"):
        (X, Z), f = M.MARKS[k]
        marks[k] = r2(V.pt(X, top, Z))
    stands = {}
    for k, at in marks.items():
        (X, Z), f = M.MARKS[k]
        floor_y = V.pt(X, 0.0, Z)[1]
        st = {"at": at, "grownup_px": grownup(floor_y), "face": f}
        if k in ("chanter", "shamisen"):
            st["scale"] = round((floor_y - HZ) / (FULL - HZ), 3)
            st["note"] = "on the dais, 45 cm up: draw them at this scale (the floor's under them), seated, facing the house"
        stands[k] = st
    # ---- the floors: the main one (the wing, the stage, backstage behind the stage); the house's front aisle (Mom's)
    g = M.GATE
    hf = M.HOUSEFRONT
    walk_cm = [(-446.0, 806.0), (-280.0, 806.0), (-280.0, 874.0), (-128.0, 874.0), (-128.0, 806.0), (-52.0, 806.0), (-52.0, 924.0),
               (8.0, 924.0), (8.0, 798.0), (562.0, 798.0), (562.0, 864.0), (522.0, 872.0), (512.0, 1150.0), (600.0, 1200.0),
               (700.0, 1240.0), (700.0, 1500.0), (-446.0, 1500.0)]
    walk = floor_poly(V, walk_cm)
    aisle_cm = [(-95.0, 690.0), (246.0, 690.0), (246.0, 764.0), (-40.0, 764.0), (-40.0, 794.0), (-95.0, 794.0)]
    aisle = floor_poly(V, aisle_cm)
    blocked = [
        {"id": "lamp", "poly": square(V, M.LAMP[0], M.LAMP[1], 22.0)},
        {"id": "stand", "poly": square(V, M.STAND[0], M.STAND[1] + 4, 30.0)},
        {"id": "gate-l", "poly": square(V, g["x"][0], g["z"], 16.0)},
        {"id": "gate-r", "poly": square(V, g["x"][1], g["z"], 16.0)},
        {"id": "front", "poly": [r2(V.pt(x_, 0, z_)) for x_, z_ in ((170, 1220), (620, 1220), (620, 1400), (170, 1400))]},
    ]
    # ---- the cut-outs, back to front with nobody on stage, with their bases and states
    def base_line(a, b):
        return [r2(V.pt(a[0], 0.0, a[1])), r2(V.pt(b[0], 0.0, b[1]))]
    planes = [
        {"id": "show", "file": "show.png", "plane": "back", "alt": True, "state": "the show (alt): the stage in the roof hatch's day, the audience all turned to the stage; laid over the backdrop (the scene fades it in), under every cut-out",
         "with": {"gate": "gate-show.png", "housefront": "housefront-show.png"}},
        {"id": "robes", "file": "robes.png", "plane": "back", "what": "the two black robes and hoods on the peg; hidden once the girls wear them (the empty peg is painted under them)"},
        {"id": "stagerail", "file": "stagerail.png", "base": base_line((M.RAIL[0], 776.0), (M.RAIL[1], 776.0)),
         "what": "the rail along the stage's front: whoever is beyond it (the house, Mom in her seat) shows only from the shoulders up; the operators (in front of it) are drawn over it"},
        {"id": "lamp", "file": "lamp.png", "base": int(round(V.pt(M.LAMP[0], 0, M.LAMP[1] + 14)[1])), "what": "the lamp on its stand, backstage (its flame: fx lamp-flame)"},
        {"id": "boypuppet", "file": "boypuppet.png", "base": int(round(V.pt(M.STAND[0], 0, M.STAND[1] + 24)[1])),
         "what": "the boy puppet hanging on his stand; hidden when he is taken off it (the puppet sprite, PEOPLE-21A, works him); the stand is painted under him"},
        {"id": "curtain", "file": "curtain.png", "base": base_line((M.CURTAIN[0], M.CURTAIN[1]), (M.CURTAIN[0], M.CURTAIN[2])),
         "what": "the black masking curtain at the stage's left end: whoever is on the stage beyond it is behind it"},
        {"id": "gate", "file": "gate.png", "states": {"before": "gate.png", "show": "gate-show.png"}, "base": base_line((g["x"][0] - 20, g["z"]), (g["x"][1] + 20, g["z"])),
         "what": "the village gate (the set), near the rail at stage left; lit in the show"},
        {"id": "housefront", "file": "housefront.png", "states": {"before": "housefront.png", "show": "housefront-show.png"}, "base": base_line(hf["p0"], hf["p1"]),
         "what": "the house front (the set) at stage right, raked toward the wing and the house; its door at the puppets' height; lit in the show"},
        {"id": "front", "file": "front.png", "plane": "front", "what": "the troupe's wicker boxes stacked behind the stage, cut by the picture's edge (bottom right)"},
    ]
    cutouts = {}
    for n, (pic, a) in pictures.items():
        if a is not None:
            cutouts[n] = box_of(a)
    # ---- things (ROUND-21's list for edo-theatre, each with a shape; and more)
    def person_rect(p, cm, seated=False, scale=None):
        k = (p[1] - HZ) / (FULL - HZ) if scale is None else scale
        px = 160 * k * cm / 175.0 * (0.55 if seated else 1.0)
        return [int(round(p[0] - px * 0.2)), int(round(p[1] - px)), int(round(px * 0.4)), int(round(px))]
    sh0, sh1, sy = M.SHELF
    lec = M.LECTERN
    things = [
        {"id": "puppets", "what": "the troupe's puppets hanging on their rail by their heads, quiet as coats", "shape": {"rect": proj_rect(V, [(M.PUPPET_RAIL[0] - 30, M.PUPPET_RAIL[2] + 6, 790), (M.PUPPET_RAIL[1] + 30, M.PUPPET_RAIL[2] - 112, 790)])},
         "stand": marks["peg"], "face": "N"},
        {"id": "heads", "what": "carved heads on a shelf (one under a cloth)", "shape": {"rect": proj_rect(V, [(sh0, sy + 30, 784), (sh1, sy - 2, 784)])}, "stand": marks["boxes"], "face": "N"},
        {"id": "boxes", "what": "the troupe's wicker boxes under the shelf (and stacked behind the stage)", "shape": {"rect": proj_rect(V, [(M.BOXES[0][0], M.BOXES[1][3], M.BOXES[0][5]), (M.BOXES[0][1], 0, M.BOXES[0][5])])},
         "stand": marks["boxes"], "face": "N"},
        {"id": "lamp", "what": "a lamp on its stand (a dish of oil on a post), alight", "shape": {"rect": cutouts.get("lamp", [0, 0, 0, 0])}, "stand": marks["lamp"], "face": "N"},
        {"id": "robes", "what": "two black robes and hoods on a peg (the robes / gone: the girls wear them)", "shape": {"rect": cutouts.get("robes", [0, 0, 0, 0])}, "stand": marks["peg"], "face": "N"},
        {"id": "boypuppet", "what": "the boy puppet on his stand, 0.9 m, a carved boy's head", "shape": {"rect": cutouts.get("boypuppet", [0, 0, 0, 0])}, "stand": marks["stand"], "face": "N"},
        {"id": "set", "what": "the set: a village gate and a house front, low painted scenery (empty / the show: lit)",
         "shape": {"rect": [min(cutouts["gate"][0], cutouts["housefront"][0]), min(cutouts["gate"][1], cutouts["housefront"][1]),
                            max(cutouts["gate"][0] + cutouts["gate"][2], cutouts["housefront"][0] + cutouts["housefront"][2]) - min(cutouts["gate"][0], cutouts["housefront"][0]),
                            max(cutouts["gate"][1] + cutouts["gate"][3], cutouts["housefront"][1] + cutouts["housefront"][3]) - min(cutouts["gate"][1], cutouts["housefront"][1])]},
         "stand": marks["wing"], "face": "E", "parts": ["gate", "housefront"]},
        {"id": "gate", "what": "the set's village gate", "shape": {"rect": cutouts["gate"]}, "stand": marks["wing"], "face": "E"},
        {"id": "housefront", "what": "the set's house front, its door at the puppets' height, an indigo noren", "shape": {"rect": cutouts["housefront"]}, "stand": marks["rail"], "face": "E"},
        {"id": "stagerail", "what": "the stage rail: a low partition of black lacquer the operators stand behind", "shape": {"poly": proj_hull(V, [(M.RAIL[0], 0, M.RAIL[2]), (M.RAIL[1], 0, M.RAIL[2]), (M.RAIL[1], M.RAIL[4], M.RAIL[3]), (M.RAIL[0], M.RAIL[4], M.RAIL[3]), (M.RAIL[0], 0, M.RAIL[3]), (M.RAIL[1], M.RAIL[4], M.RAIL[2])])},
         "stand": marks["rail"], "face": "N"},
        {"id": "dais", "what": "the chanter's dais at stage right, out in the house", "shape": {"poly": proj_hull(V, [(M.DAIS[0], 0, M.DAIS[2]), (M.DAIS[1], 0, M.DAIS[2]), (M.DAIS[1], 0, M.DAIS[3]), (M.DAIS[0], 0, M.DAIS[3]),
                                                                                                                   (M.DAIS[0], M.DAIS[4], M.DAIS[2]), (M.DAIS[1], M.DAIS[4], M.DAIS[2]), (M.DAIS[1], M.DAIS[4], M.DAIS[3]), (M.DAIS[0], M.DAIS[4], M.DAIS[3])])},
         "stand": marks["rail"], "face": "E"},
        {"id": "book", "what": "the chanter's book on its lectern (nobody touches a chanter's book)", "shape": {"rect": proj_rect(V, [(lec[0], lec[5] + 2, lec[2]), (lec[1], lec[4] + 30, lec[3])], pad=3)},
         "stand": marks["rail"], "face": "E"},
        {"id": "audience", "what": "the audience on their mats, row behind row, facing the stage", "shape": {"poly": proj_hull(V, [(-90, 110, 80), (575, 110, 80), (575, 30, 712), (-90, 30, 712)])},
         "stand": marks["rail"], "face": "N"},
        {"id": "windows", "what": "the high lattice windows: daylight", "shape": {"poly": proj_hull(V, [(M.WINDOWS_FAR[0][0], M.WIN_Y[1], 0), (M.HALL_X1, M.WIN_Y[1], 0), (M.HALL_X1, M.WIN_Y[1], M.WINDOWS_RIGHT[1][1]),
                                                                                                         (M.HALL_X1, M.WIN_Y[0], M.WINDOWS_RIGHT[1][1]), (M.WINDOWS_FAR[0][0], M.WIN_Y[0], 0)])},
         "stand": marks["wing"], "face": "N"},
        {"id": "rafters", "what": "the rafters of the hall, dark, and the backstage ceiling's edge", "shape": {"poly": [[0, 0], [799, 0], [799, 150], [0, 150]]}, "stand": marks["wing"], "face": "N"},
        {"id": "backdoor", "what": "the back door, open a hand's breadth on the alley (the way out to the street)", "shape": {"rect": proj_rect(V, [(M.BACKDOOR[0] - 8, M.BACKDOOR[3] + 8, 771), (M.BACKDOOR[1] + 8, 0, 771)])},
         "stand": marks["back"], "face": "N"},
        {"id": "curtain", "what": "the black masking curtain at the stage's left end", "shape": {"rect": cutouts["curtain"]}, "stand": marks["wing"], "face": "E"},
        {"id": "stage", "what": "the stage's polished boards", "shape": {"poly": [r2(V.pt(x_, 0, z_)) for x_, z_ in ((0, 790), (570, 790), (570, 1180), (0, 1180))]}, "stand": marks["rail"], "face": "N"},
        {"id": "stand", "what": "the boy puppet's stand", "shape": {"rect": proj_rect(V, [(M.STAND[0] - 26, M.STAND_H + 8, M.STAND[1]), (M.STAND[0] + 26, 0, M.STAND[1] + 24)])}, "stand": marks["stand"], "face": "N"},
    ]
    # the people (drawn by the game): each a rect at their place
    things += [
        {"id": "jubei", "what": "Jubei, the chief puppeteer, by the boy puppet (drawn by the game)", "shape": {"rect": person_rect(marks["jubei"], 156)}, "stand": marks["stand"], "face": "E"},
        {"id": "chanter", "what": "the chanter on his dais, at his lectern (drawn by the game, seated)", "shape": {"rect": person_rect(marks["chanter"], 156, True, stands["chanter"]["scale"])}, "stand": marks["rail"], "face": "E"},
        {"id": "shamisen", "what": "the shamisen player on the dais (drawn by the game, seated)", "shape": {"rect": person_rect(marks["shamisen"], 156, True, stands["shamisen"]["scale"])}, "stand": marks["rail"], "face": "E"},
        {"id": "tatsu", "what": "Tatsu, the thief-taker, in the front row (drawn by the game, seated)", "shape": {"rect": person_rect(marks["tatsuseat"], 156, True)}, "stand": marks["rail"], "face": "S"},
    ]
    # ---- the puppet at the rail: where the doll and its three operators stand (PEOPLE-21A places them together)
    pa = M.PUPPET_AT
    doll_feet = V.pt(pa[0], M.PUPPET_FEET_Y, pa[1])
    doll_floor = V.pt(pa[0], 0.0, pa[1])
    rail_top = V.pt(pa[0], M.RAIL[4], 776.0)
    puppet = {
        "at": r2(doll_floor), "feet": r2(doll_feet), "scale": round((doll_floor[1] - HZ) / (FULL - HZ), 3),
        "rail_top_row": int(round(rail_top[1])), "rail_height_cm": M.RAIL[4], "doll_cm": M.PUPPET_H,
        "doll_px": int(round(160 * (doll_floor[1] - HZ) / (FULL - HZ) * M.PUPPET_H / 175.0)),
        "jubei": marks["rail"], "left_hand": marks["railLeft"], "feet_operator": marks["railFeet"],
        "note": "The doll (0.9 m) walks on the rail's top, 86 cm up: draw it at `scale` with its feet at `feet` (it floats over the "
                "floor point `at`, which is between the operators and the rail). Jubei stands behind it at `rail` (his face shows), "
                "Big Sister at its left hand (`left_hand`, the wing side, nearer us), Little Sister at its feet (`feet_operator`, "
                "crouched low). We see the group from behind and to the left, about 35 degrees off its back: the doll shows to the "
                "right of Big Sister and in front of Jubei; its left hand (raised to the ear) is on our side.",
    }
    fx = [
        {"id": "lamp-flame", "type": "flame", "what": "the lamp's flame backstage", "at": iA["flame"], "size": 7, "glow": 22, "glowColor": "#f4d88e", "glowOpacity": 0.22,
         "flicker": 0.5, "base": int(round(V.pt(M.LAMP[0], 0, M.LAMP[1] + 14)[1]))},
        {"id": "shaft-house", "type": "light", "src": "shaft-house.png", "layer": "live", "blend": "screen", "air": None,
         "note": "PROPOSED: the right wall's high windows' daylight in the air, slanting down onto the mats (the patches it makes are painted): a light picture (RGBA, soft) for the live layer, as the keep's beams; dust may drift in it"},
        {"id": "shaft-stage", "type": "light", "src": "shaft-stage.png", "layer": "live", "blend": "screen", "when": "the show",
         "note": "PROPOSED: in the show only, the roof hatch's daylight falling onto the stage (the lit boards are in show.png): fade it in with the show"},
        {"id": "dust", "type": "birds", "kind": "flyers", "what": "motes turning in the house's shafts of day (a few pale specks: the flyer kind, very small, slow)",
         "lanes": [[[560, 250], [430, 330]], [[600, 240], [470, 340]]], "every": [6, 14], "group": [1, 2], "size": 2, "speed": 8, "color": "#f6eed8",
         "note": "PROPOSED, optional"},
    ]
    out = {
        "id": M.ID, "scene": M.ID, "size": [W, H], "horizon": HZ, "full": FULL, "view": M.VIEW,
        "room_cm": "edo_theatre_model.py: X across (the stage X 0..570), Y up, Z from the house's far wall toward us; one floor level",
        "light": "day: the house's high lattice windows (far wall and right wall) laying flat lit patches on the mats; backstage dim, the lamp's warm pool and a blade of the alley's day from the back door; the stage in half light before the show, in the roof hatch's day in the show",
        "walk": walk,
        "walk_floors": [
            {"name": "stage", "area": walk, "note": "the wing (backstage), the stage behind the rail, backstage behind the stage: one floor"},
            {"name": "house", "area": aisle, "note": "the house's front aisle and Mom's place in the front row: reached by a script (Mom goes round the front, through the gap at the wing wall's end, `gap` -> `aisle` -> `momseat`); nobody walks there by a click",
             "away": "(the scene's line: the house is for the audience)"},
        ],
        "blocked": blocked,
        "planes": planes, "cutouts": cutouts,
        "things": things,
        "marks": marks, "stands": stands,
        "puppet": puppet,
        "fx": fx,
        "states": {"stage": "empty (before: back.png + gate.png + housefront.png) / the show (show.png + gate-show.png + housefront-show.png; the scene fades the three together)",
                   "robes": "on the peg (robes.png) / gone (hidden)", "boypuppet": "on his stand (boypuppet.png) / gone (hidden: the puppet sprite)"},
        "exits": {"backdoor": {"to": "edo-street", "at": marks["back"], "rect": proj_rect(V, [(M.BACKDOOR[0] - 8, M.BACKDOOR[3] + 8, 771), (M.BACKDOOR[1] + 8, 0, 771)])}},
        "heights": {"mom_cm": 168, "bigsis_cm": 160, "lilsis_cm": 122, "man_1830_cm": 156, "woman_1830_cm": 146, "boypuppet_cm": 90, "grownup_at_full_px": 160},
        "notes": "PAINT-21D. The theatre's inside is the game's own (not in the sources): a hut theatre of one floor level, the stage open behind to the wing; the low set, the dais, the hatch are invented in the spirit of the art.",
    }
    return out

"""layout.json for the Office's lot (OFFICE-17A): every number the scene file needs, measured from the finished
pictures and the scene's own measurements (office_lot_kit). The scene file in js/content/scenes/ is the authority once
it is written; these are the painter's numbers.

Two floors to walk (ENGINE-17's `walk: [ground, roof]`): the gravel, and the strip of the roof in front of the unit.
The roof is a floor 3 m up, so whoever stands on it is sized by that floor, not by the gravel's rows: its own `full`
(the row on which a grown-up standing on it would be 160 px tall), with the same horizon. Ranger alone walks it."""

import json
import math

import numpy as np

import office_lot_kit as K
import office_lot_limo as LM
from office_lot_kit import (AWNING, BLD, CAN, DOOR, FENCE, FLAG, GATE, GRILLE, KEYPAD, MAT, NUTS, PIPE, SCUPPER, SIGN, SWITCH, UNIT,
                            WINDOW)

OUT = "out/office-lot"
ROOF_Y = BLD["deck"]
ROOF_FULL = K.plane_full(ROOF_Y)
RANGER_PX = 1.0 / (K.CAM.s0)                              # one of Ranger's full-size pixels, in cm (1.094)


def r1(v):
    return round(float(v), 1)


def pt(x, y, z):
    p = K.P(x, y, z)
    return [r1(p[0]), r1(p[1])]


def grown(z, y=0.0):
    """A grown-up's height in px standing at depth z on a floor y cm up."""
    return int(round(175.0 * K.k_at(z)))


def scale_of(z):
    return round(K.scale_at(z), 4)


def poly_of(points):
    return [[r1(x), r1(y)] for x, y in points]


def hull_of(alpha, step=1, maxpts=24):
    """The convex hull of a cut-out's painted pixels, simplified to at most maxpts points."""
    ys, xs = np.where(alpha > 0.5)
    pts = np.stack([xs, ys], axis=1)
    corners = np.concatenate([pts, pts + [1, 0], pts + [0, 1], pts + [1, 1]])
    import office_lot as L
    h = L._hull([tuple(p) for p in corners.tolist()])
    while len(h) > maxpts:                                   # drop the point whose loss shrinks the hull least
        best, bi = None, None
        for i in range(len(h)):
            a, b, c = h[i - 1], h[i], h[(i + 1) % len(h)]
            area = abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]))
            if best is None or area < best:
                best, bi = area, i
        h.pop(bi)
    return [[int(round(x)), int(round(y))] for x, y in h]


def box_of(alpha):
    ys, xs = np.where(alpha > 0.5)
    return [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


def ground_poly(pts_xz):
    return [pt(x, 0.0, z) for x, z in pts_xz]


def roof_poly(pts_xz):
    return [pt(x, ROOF_Y, z) for x, z in pts_xz]


def clip_x(poly):
    return [[min(max(x, 0.0), 800.0), y] for x, y in poly]


# ---------------------------------------------------------------- the walk areas
def walk_ground():
    """The gravel: from the bottom edge back to the building's front (18 cm out from its wall); on the left, past the
    building's end, back as far as the limousine's line, but only out to 20 px short of the column of the building's
    front left corner (whoever stood further right there, behind the front's line, would be drawn over the wall: we see
    the front, not the left end); and on the right back to the limousine's near side, keeping 90 cm off the building's
    right wall (so nobody walking there is drawn over the wall's corner)."""
    zf, zl = 452.0, K.LIMO["z"] - 14.0
    left_x = (0.0 - K.VX) / K.k_at(640.0)
    col = K.P(BLD["x"][0], 0.0, BLD["z"][0])[0] - 20.0                        # OFFICE-17A: the column 20 px left of the corner
    at_col = lambda z: (col - K.VX) / K.k_at(z)
    pts = [(left_x, 640.0), (at_col(640.0), 640.0), (at_col(zf), zf), (170.0, zf), (170.0, zl), (1400.0, zl)]
    poly = [pt(x, 0.0, z) for x, z in pts]
    poly = clip_x(poly)
    poly += [[800.0, 597.0], [0.0, 597.0]]
    return poly


def walk_roof():
    """The strip of roof in front of the unit: from just behind the front edge's coping to 18 cm short of the unit's
    face, and 12 cm in from the roof's ends."""
    x0, x1 = BLD["x"][0] + 12.0, BLD["x"][1] - 12.0
    z0, z1 = 512.0, UNIT["z"][0] - 18.0
    return roof_poly([(x0, z0), (x1, z0), (x1, z1), (x0, z1)])


# ---------------------------------------------------------------- the marks
def marks():
    m = {}
    # Ranger: out from under the limousine's open door (to the left of the open leaf), on the gravel
    m["fromLimo"] = pt(375.0 + 0.0, 0.0, 612.0)
    # Wendell's place: on the door, at its left side (the keypad is on its right), facing the gate (W)
    m["door"] = pt(-282.0, 0.0, 436.0)
    # the can as it stands: Ranger beside it, on its left, facing it (E), to tip it over to the right
    m["trash"] = pt(-100.0, 0.0, 434.0)
    # the foot of the drainpipe, where the can is rolled to: Ranger under the elbow, facing E (with the can there, he
    # climbs from climbFrom, on its left)
    m["pipe"] = pt(60.0, 0.0, 436.0)
    m["climbFrom"] = pt(-17.0, 0.0, 436.0)
    # on the roof, just up from the drainpipe; in front of the grille; at the switch (sitting up facing E, his hands on
    # the lever: office_lot_kit.SWITCH, nevada_ranger.LEVER)
    m["roof"] = pt(10.0, ROOF_Y, 545.0)
    m["intake"] = pt(-116.0, ROOF_Y, 742.0)
    m["switch"] = pt(-45.1, ROOF_Y, 745.0)
    # the arrival
    m["limoDoor"] = pt(400.0, 0.0, 562.0)                     # Grandpa Joe, just out of the back, between two of them
    m["dale"] = pt(318.0, 0.0, 556.0)                         # on his left (toward the car's tail)
    m["merle"] = pt(486.0, 0.0, 548.0)                        # on his right, past the open door
    xs = [K.LIMO["tail"] + c for c in (198.5, 269.0, 381.5, 450.5)]
    m["outOfCar"] = [pt(x, 0.0, 596.0) for x in xs]           # the four doors on this side, a step out from each (back to front)
    m["jedFrom"] = pt(1180.0, 0.0, 600.0)                     # Jed, round the car's nose (just past the right edge)
    m["walkIn"] = [pt(330.0, 0.0, 545.0), pt(180.0, 0.0, 470.0), pt(20.0, 0.0, 425.0), pt(-140.0, 0.0, 420.0), pt(-200.0, 0.0, 445.0)]
    m["inDoor"] = pt(-200.0, 0.0, 520.0)                      # through the door and in (behind the door's line: whoever is here is inside)
    m["queue"] = {"jed": pt(-200.0, 0.0, 440.0), "dale": pt(-262.0, 0.0, 418.0), "joe": pt(-200.0, 0.0, 410.0), "merle": pt(-140.0, 0.0, 416.0),
                  "floyd": pt(-60.0, 0.0, 400.0)}
    return m


# Which way whoever is at each mark faces (the engine's E, W, N, S): Ranger out from under the car toward the building;
# at the can, facing it, to tip it over to the right; under the pipe and climbing, facing it; on the roof, along it toward
# the unit; at the intake, facing the grille; at the switch, sitting up facing E with his hands on the lever (his pull
# frames); Wendell by regulation facing the gate (at the back left: W, or NW if the engine has it); the two who get Grandpa
# Joe out facing him; everybody in the queue facing the door.
FACES = {"fromLimo": "W", "trash": "E", "pipe": "E", "climbFrom": "E", "roof": "W", "intake": "N", "switch": "E", "door": "W",
         "limoDoor": "S", "dale": "E", "merle": "W", "outOfCar": "S", "walkIn": "W", "inDoor": "N", "queue": "N"}
FAN_X = K.FAN["x"]                                         # the middle of the intake (the fan's hub)


def stands(m):
    """Every mark and stand with the size of a grown-up there (on the roof, by the roof's own floor)."""
    out = {}
    for name, p in m.items():
        if isinstance(p, dict) or (isinstance(p, list) and isinstance(p[0], list)):
            continue
        on_roof = name in ("roof", "intake", "switch")
        full = ROOF_FULL if on_roof else K.FULL
        out[name] = {"at": p, "grownup_px": int(round(160.0 * (p[1] - K.HZ) / (full - K.HZ))), "floor": "roof" if on_roof else "ground"}
    return out


def climb_path(m):
    """Ranger's way up: from the foot of the drainpipe onto the can's lid, onto the pipe, up it (its straps are his
    rungs) and over the coping onto the roof. Each point with the size he is there (by its depth, not its row)."""
    zp = PIPE["z"]
    x_on = PIPE["x"] - PIPE["r"] - 11.0 * RANGER_PX          # his foot point when his belly is to the pipe (the frames' pipe at +11 px)
    pts = [("climbFrom", m["climbFrom"], scale_of(436.0), "on the gravel by the can (under the pipe), facing it", "walk"),
           ("lid", pt(CAN["pipe"][0] - 14.0, CAN["top"], CAN["pipe"][1]), scale_of(CAN["pipe"][1]), "up onto the can's lid", "reach"),
           ("pipeFoot", pt(x_on, PIPE["elbow"] - 4.0, zp), scale_of(zp), "his paws on the elbow, onto the pipe", "climb"),
           ("pipeTop", pt(x_on, BLD["cope"] - 44.0, zp), scale_of(zp), "up the pipe to just under the coping", "climb"),
           ("roof", m["roof"], scale_of(545.0), "over the coping onto the roof", "walk")]
    return [{"name": n, "at": p, "scale": s, "what": w, "frames": f} for n, p, s, w, f in pts]


# ---------------------------------------------------------------- the things
def rect_poly(x0, x1, y0, y1, z):
    return poly_of([K.P(x0, y0, z), K.P(x1, y0, z), K.P(x1, y1, z), K.P(x0, y1, z)])


def things(info, cuts, m):
    zw = BLD["z"][0]
    t = []

    def add(id_, what, shape, stand, face, who=None, **kw):
        e = {"id": id_, "what": what, "shape": shape, "stand": stand, "face": face}
        if who:
            e["who"] = who
        e.update(kw)
        t.append(e)
    add("door", "the front door: steel, beige, shut (locked: Wendell has the code)", {"poly": rect_poly(DOOR["x"][0], DOOR["x"][1], 0, DOOR["h"], zw)},
        pt(-200.0, 0.0, 425.0), "N")
    add("keypad", "the keypad beside the door: twelve buttons and a little red light", {"poly": rect_poly(KEYPAD["x"][0] - 4, KEYPAD["x"][1] + 4, KEYPAD["y"][0] - 4, KEYPAD["y"][1] + 4, zw)},
        pt(-128.0, 0.0, 430.0), "N")
    sb = info["sign_box"]
    add("sign", "the sign over the door: OFFICE OF PECULIAR SECTORS / DESERT FIELD HEADQUARTERS / AUTHORIZED PERSONNEL ONLY · PLEASE WIPE YOUR FEET",
        {"poly": rect_poly(SIGN["x"][0], SIGN["x"][1], SIGN["y"][0], SIGN["y"][1], zw - SIGN["proud"])}, pt(-200.0, 0.0, 420.0), "N")
    add("mat", "the mat by the door: WIPE", {"poly": ground_poly([(MAT["x"][0], MAT["z"][0]), (MAT["x"][1], MAT["z"][0]), (MAT["x"][1], MAT["z"][1]), (MAT["x"][0], MAT["z"][1])])},
        pt(-200.0, 0.0, 395.0), "N")
    add("window", "the one window on this side: small, high, frosted", {"poly": rect_poly(WINDOW["x"][0] - 4, WINDOW["x"][1] + 4, WINDOW["y"][0] - 6, WINDOW["y"][1] + 4, zw)},
        pt(-388.0, 0.0, 430.0), "N")
    add("awning", "the little flat awning over the door", {"poly": hull_of(cuts["awning"][1])}, pt(-200.0, 0.0, 425.0), "N")
    for state, file_, place in (("standing", "trash", CAN["standing"]), ("tipped", "trash-tipped", CAN["tipped"]), ("pipe", "trash-pipe", CAN["pipe"])):
        add("trash" if state == "standing" else f"trash-{state}", f"the trash can ({state}): steel, the lid chained to it, REGULATION stencilled on it",
            {"poly": hull_of(can_only(cuts, file_))}, m["trash"] if state == "standing" else (pt(place[0] - 58.0, 0.0, place[1] - 4.0) if state == "tipped" else m["pipe"]),
            "E", state=state, file=file_ + ".png")
    my, mz = PIPE["mouth"]
    pipe_poly = poly_of([K.P(SCUPPER["x"][0] - 2, SCUPPER["y"][1] + 2, SCUPPER["z"][0]), K.P(SCUPPER["x"][1] + 2, SCUPPER["y"][1] + 2, SCUPPER["z"][0]),
                         K.P(PIPE["x"] + PIPE["r"] + 4, PIPE["elbow"], PIPE["z"]), K.P(PIPE["x"] + PIPE["r"] + 4, my - 8, mz),
                         K.P(PIPE["x"] - PIPE["r"] - 4, my - 8, mz), K.P(PIPE["x"] - PIPE["r"] - 4, PIPE["elbow"], PIPE["z"])])
    add("drainpipe", "the drainpipe down the corner: it stops in an elbow three feet above the gravel (a raccoon's stretch and a half); its straps would do for rungs",
        {"poly": pipe_poly}, m["pipe"], "E")
    lm = LM.measure()
    add("limo", "the gray limousine, parked", {"poly": hull_of(cuts["limo"][1])}, pt(380.0, 0.0, 600.0), "N")
    add("limoDoor", "the limousine's rear door (open after the arrival)", {"poly": hull_of(cuts["limo-door-open"][1] * door_region(cuts))},
        m["fromLimo"], "N")
    add("unit", "the rooftop unit: an air conditioner the size of a minivan, much too big for the building, humming, ducts going down into the roof",
        {"poly": rect_poly(UNIT["x"][0], UNIT["x"][1], UNIT["curb"], UNIT["top"] + 30, UNIT["z"][0])}, m["intake"], "N", floor="roof")
    add("grille", "the intake grille on the unit's side: a big louvred panel held on by four wing nuts; the fan turning behind it",
        {"poly": rect_poly(GRILLE["x"][0] - 4, GRILLE["x"][1] + 4, GRILLE["y"][0] - 4, GRILLE["y"][1] + 4, UNIT["z"][0])}, m["intake"], "N", floor="roof")
    for i, (nx, ny) in enumerate(NUTS):
        add(f"nut-{i + 1}", f"wing nut {i + 1} ({'low' if i < 2 else 'high'}, {'left' if i % 2 == 0 else 'right'})",
            {"poly": rect_poly(nx - 16, nx + 16, ny - 7, ny + 16, UNIT["z"][0])},
            pt(nx - 20.0, ROOF_Y, 745.0), "E", floor="roof", reach="sitting up" if i < 2 else "climbing the grille (the climb frames)")
    add("switch", "the maintenance switch: a lever in a gray box, a sticker with a fan crossed out: TURN OFF BEFORE SERVICING. THIS MEANS YOU, WENDELL.",
        {"poly": rect_poly(SWITCH["box"][0] - 12, SWITCH["box"][1] + 3, SWITCH["box"][2] - 6, SWITCH["box"][3] + 4, UNIT["z"][0] - SWITCH["proud"])},
        m["switch"], "E", floor="roof")
    add("flagpole", "the flagpole, and its small pennant: O.O.P.S. in white on gray", {"poly": hull_of(cuts["flagpole"][1])}, pt(-520.0, 0.0, 380.0), "N")
    gs = info["gate_sign"]
    add("fenceSign", "the small sign on the open gate: PLEASE DO NOT LOOK DIRECTLY AT THE BUILDING", {"poly": poly_of([K.P(*p) for p in gs])},
        pt(-700.0, 0.0, 640.0), "NW")
    import office_lot_things as T
    q, _ = T.gate_leaf_points()
    leaf = [K.P(*p) for p in q]
    opening = [K.P(GATE["x"][0], 0, FENCE["z"]), K.P(GATE["x"][1], 0, FENCE["z"]), K.P(GATE["x"][1], FENCE["h"], FENCE["z"]), K.P(GATE["x"][0], FENCE["h"], FENCE["z"])]
    import office_lot as L
    add("gate", "the gate in the fence, standing open (its left post is past the picture's edge)",
        {"poly": [[max(0, int(round(x))), int(round(y))] for x, y in L._hull(leaf + opening)]}, pt(-700.0, 0.0, 640.0), "NW")
    fr = r1(K.row_of(FENCE["z"]))
    add("desert", "the desert past the fence, and the range on the horizon (list it first: everything else is over it)",
        {"poly": [[0, 112], [800, 112], [800, fr], [496, fr], [452, 220], [418, 118], [186, 118], [178, 196], [108, 249], [108, fr], [0, fr]]},
        pt(-300.0, 0.0, 600.0), "N")
    return t


def can_only(cuts, name):
    """The can's own pixels (its cut-out holds its shadow too)."""
    import office_lot as L
    s = L.can_shadow({"trash": "standing", "trash-tipped": "tipped", "trash-pipe": "pipe"}[name])
    a = cuts[name][1]
    return a * (s <= 0.45)


def door_region(cuts):
    """Where the limousine's rear door is (open or shut): the picture between its opening's columns and in front."""
    lm = LM.measure()
    x0 = int(lm["door"]["free"][0]) - 4
    x1 = int(lm["door"]["opening"][1]) + 4
    m = np.zeros(cuts["limo"][1].shape, np.float32)
    m[:, max(0, int(lm["door"]["opening"][0]) - 2):x1] = 1.0
    m[:, max(0, x0):x1] = 1.0
    return m


# ---------------------------------------------------------------- the cut-outs
def planes(cuts, m):
    """In the painter's order (back to front, as the scene should list them), with their bases and solids."""
    p = []
    roof_note = "on the unit's face, on the roof: behind everybody (whoever is on the roof stands in front of the unit)"
    p.append({"id": "grille", "file": "grille.png", "plane": "back", "note": "the intake grille, on (its louvres' slits are clear: the fan's frames turning behind it show through them). " + roof_note,
              "state": "on (grille-off when it is off)"})
    for i in range(4):
        p.append({"id": f"nut-{i + 1}", "file": f"nut-{i + 1}.png", "plane": "back", "note": f"wing nut {i + 1} on its stud ({'low' if i < 2 else 'high'}, {'left' if i % 2 == 0 else 'right'}): hide it as Ranger turns it off; all four gone, the grille comes off"})
    p.append({"id": "switch", "file": "switch.png", "plane": "back", "note": "the maintenance switch's lever, up (on); its box and sticker are the backdrop's"})
    p.append({"id": "door", "file": "door.png", "plane": "back", "note": "the front door, shut (behind everybody: whoever walks in through it, when it is open, is in front of the hall)"})
    p.append({"id": "awning", "file": "awning.png", "base": r1(K.row_of(BLD["z"][0] - AWNING["out"])), "note": "the awning over the door (base: its front edge on the gravel); it is higher than anyone's head"})
    p.append({"id": "trash", "file": "trash.png", "base": r1(K.row_of(CAN["standing"][1] - CAN["r"])), "solid": can_solid(CAN["standing"]),
              "note": "the trash can standing by the wall, with its own shadow (on the gravel and up the wall)"})
    p.append({"id": "flagpole", "file": "flagpole.png", "base": r1(K.row_of(FLAG["z"])), "solid": ellipse_solid(FLAG["x"], FLAG["z"], 30.0, 26.0),
              "note": "the flagpole on its concrete foot (its pennant: fx `pennant`, on this base)"})
    lm = LM.measure()
    p.append({"id": "limo", "file": "limo.png", "base": lm["row"], "solid": limo_solid(),
              "note": "the gray limousine, parked (its near side's foot line is the base: Jed comes round from behind it)"})
    p.append({"id": "front", "file": "front.png", "plane": "front", "note": "sagebrush in the bottom corners"})
    # the other states
    p.append({"id": "grille-off", "file": "grille-off.png", "plane": "back", "alt": True, "replaces": ["grille", "nut-1", "nut-2", "nut-3", "nut-4"],
              "solid": roof_poly([(GRILLE["x"][0] - 14 - 122, UNIT["z"][0] - 34), (GRILLE["x"][0] - 10, UNIT["z"][0] - 34), (GRILLE["x"][0] - 10, UNIT["z"][0]), (GRILLE["x"][0] - 14 - 122, UNIT["z"][0])]),
              "note": "the grille off, leaning against the unit to the left of its opening, its foot on the roof; the four wing nuts in a neat row on the roof in front of its foot (solid: its foot, on the roof)"})
    p.append({"id": "switch-off", "file": "switch-off.png", "plane": "back", "alt": True, "replaces": ["switch"], "note": "the lever pulled down (off)"})
    p.append({"id": "door-open", "file": "door-open.png", "plane": "back", "alt": True, "replaces": ["door"], "note": "the door swung in (hinged on the left), the hall inside lit by tubes"})
    p.append({"id": "trash-tipped", "file": "trash-tipped.png", "base": r1(K.row_of(CAN["tipped"][1] - 30.0)), "alt": True, "replaces": ["trash"],
              "solid": tipped_solid(), "note": "the can on its side on the gravel where it fell, its mouth toward us and to the right (Ranger in it is in front of it), the lid off beside it on its chain"})
    p.append({"id": "trash-pipe", "file": "trash-pipe.png", "base": r1(K.row_of(CAN["pipe"][1] - CAN["r"])), "alt": True, "replaces": ["trash"], "solid": can_solid(CAN["pipe"]),
              "note": "the can standing under the drainpipe's elbow (the elbow is painted over it: it is in front of it). While Ranger is on its lid or on the pipe, he is drawn in front of it (his feet are above its base)"})
    p.append({"id": "limo-door-open", "file": "limo-door-open.png", "base": lm["row"], "alt": True, "replaces": ["limo"], "solid": limo_solid(open_=True),
              "note": "the limousine with its rear door open 50 degrees (we see the door's outside, turned toward the tail, and the back seat in the opening)"})
    return p


def ellipse_solid(x, z, rx, rz, n=12):
    return ground_poly([(x + rx * math.cos(t), z + rz * math.sin(t)) for t in np.linspace(0, 2 * math.pi, n, endpoint=False)])


def can_solid(at):
    return ellipse_solid(at[0], at[1], CAN["r"] + 4.0, CAN["r"] + 4.0, n=10)


def tipped_solid():
    import office_lot_things as T
    cx, cz = CAN["tipped"]
    a = math.radians(34.0)
    ca, sa = math.cos(a), math.sin(a)
    corners = [(-40.0, -30.0), (66.0, -30.0), (66.0, 30.0), (-40.0, 30.0)]          # the can lying, and its lid past its mouth
    return ground_poly([(cx + x * ca + z * sa, cz - x * sa + z * ca) for x, z in corners])


def limo_solid(open_=False):
    x0, z0 = K.LIMO["tail"], K.LIMO["z"]
    pts = [(x0 + 2, z0 - 4), (x0 + 627, z0 - 4), (x0 + 627, z0 + 200), (x0 + 2, z0 + 200)]
    if open_:
        a = math.radians(K.LIMO["swing"])
        fx, fz = x0 + LM.HINGE + (LM.FREE - LM.HINGE) * math.cos(a), z0 + (LM.FREE - LM.HINGE) * math.sin(a)
        pts = [(x0 + 2, z0 - 4), (fx - 6, z0 - 4), (fx - 6, fz - 6), (x0 + LM.HINGE + 4, fz - 6), (x0 + LM.HINGE + 4, z0 - 4),
               (x0 + 627, z0 - 4), (x0 + 627, z0 + 200), (x0 + 2, z0 + 200)]
    return clip_x(ground_poly(pts))


# ---------------------------------------------------------------- write it
def write(info, cuts, frames):
    m = marks()
    lm = LM.measure()
    fan, pen = frames["fan"], frames["pennant"]
    lay = {
        "id": "office-lot",
        "horizon": K.HZ, "full": K.FULL,
        "view": K.VIEW,
        "view_note": "the room camera (room.View) these numbers make: X across, Z toward us; Z = -z of the painter's measurements (office_lot_kit), "
                     "the lens 490 cm up at Z 831.25, square on to the building's front (yaw 0)",
        "eye_cm": round(K.EYE, 1),
        "vanishing": [K.VX, K.HZ],
        "light": "early afternoon, 31 October: the sun high (49 degrees) and a little behind us to the left; fronts lit, tops brightest, "
                 "right-hand ends in shade; short shadows falling back and to the right. Key: nevada-morning (the same day's light)",
        "walk": [walk_ground(), walk_roof()],
        "walk_areas": {
            "ground": {"poly": walk_ground(), "horizon": K.HZ, "full": K.FULL, "who": "everybody",
                       "note": "the gravel: from the bottom edge back to 18 cm in front of the building's wall, round its left end, and on the right "
                               "back to the limousine's near side, keeping 90 cm off the building's right wall"},
            "roof": {"poly": walk_roof(), "horizon": K.HZ, "full": r1(ROOF_FULL), "y_cm": ROOF_Y, "who": "ranger",
                     "note": "the strip of the roof in front of the unit, a floor 3 m up: whoever stands on it is sized by its own full "
                             "((feet - 140) / (full - 140)), not by the gravel's rows. Reached only by the climb (climb, below)"},
        },
        "walk_note": "two floors with no way between them but Ranger's climb. On the roof he is about 0.53 (at the unit) to 0.61 (at the front edge) of full size.",
        "blocked": [ellipse_solid(FLAG["x"], FLAG["z"], 30.0, 26.0)],
        "planes": planes(cuts, m),
        "things": things(info, cuts, m),
        "marks": m,
        "faces": FACES,
        "stands": stands(m),
        "climb": climb_path(m),
        "climb_note": "for g.climbTo: on the lid and the pipe he is in front of the can (draw him at the plane of the pipe, z 463: scale 0.648, "
                      "not by his row). His climb frames put the pipe's near face 11 px (full size) east of his foot point.",
        "cans": {"standing": {"at": pt(CAN["standing"][0], 0, CAN["standing"][1] - CAN["r"]), "file": "trash.png"},
                 "tipped": {"at": pt(CAN["tipped"][0], 0, CAN["tipped"][1]), "file": "trash-tipped.png", "mouth": pt(CAN["tipped"][0] + 30.0, 26.0, CAN["tipped"][1] - 20.0)},
                 "pipe": {"at": pt(CAN["pipe"][0], 0, CAN["pipe"][1] - CAN["r"]), "file": "trash-pipe.png", "lid": pt(CAN["pipe"][0], CAN["top"], CAN["pipe"][1])}},
        "switch": {"box": rect_poly(SWITCH["box"][0], SWITCH["box"][1], SWITCH["box"][2], SWITCH["box"][3], UNIT["z"][0] - SWITCH["proud"]),
                   "handle_on": pt(SWITCH["up"][0], SWITCH["up"][1], UNIT["z"][0] - SWITCH["proud"] - 1.0),
                   "handle_off": pt(SWITCH["down"][0], SWITCH["down"][1], UNIT["z"][0] - SWITCH["proud"] - 1.0),
                   "note": "Ranger at marks.switch facing E: his pull frames' hands (x +18, y 49 and x +16, y 22 at full size) are on the handle"},
        "nuts": [{"id": f"nut-{i + 1}", "at": pt(nx, ny, UNIT["z"][0] - GRILLE["proud"] - 1.0)} for i, (nx, ny) in enumerate(NUTS)],
        "intake": {"opening": rect_poly(GRILLE["x"][0] + 3, GRILLE["x"][1] - 3, GRILLE["y"][0] + 3, GRILLE["y"][1] - 3, UNIT["z"][0]),
                   "sill": pt(FAN_X, GRILLE["y"][0] + 3, UNIT["z"][0]), "scale": scale_of(UNIT["z"][0]),
                   "note": "the unit's intake behind the grille: its opening, and the middle of its bottom edge, 33 cm above the roof, "
                           "where Ranger hops up and goes in (into office-ducts at its mark intake); scale: his size there"},
        "limo": {"files": ["limo.png", "limo-door-open.png"], "foot": lm["foot"], "row": lm["row"], "scale": lm["scale"],
                 "x": [lm["tail_x"], lm["nose_x"]], "door": lm["door"],
                 "sill": {"at": pt(K.LIMO["tail"] + (LM.FREE + LM.HINGE) / 2, 22.0, K.LIMO["z"] + 10.0), "scale": scale_of(K.LIMO["z"] + 10.0),
                          "note": "the floor of the open rear door's opening, 22 cm up: where Ranger stands in the doorway, out from under "
                                  "the seat, before he drops to the gravel (his drop frames) at marks.fromLimo"},
                 "note": "painted in place (a cut-out, not the roadside's frames, which have the morning's long shadow to the left): the "
                         "same car at the size the roadside's frames would be drawn here (limo-side-0.png laid with its foot [438, 155] on "
                         "`foot` at `scale`), its tail at x 506, its nose past the right edge; door: where the rear door's hinge and free "
                         "edge stand when open, and its opening's columns"},
        "fx": [
            {"id": "fan", "what": "the fan behind the intake grille, turning (three blades, a third of a turn in four frames)", "frames": fan["files"], "fps": 12,
             "at": fan["at"], "foot": fan["foot"], "rect": fan["rect"], "plane": "back",
             "note": "listed before the grille (it lies under it: the grille's slits show it turning); while the fans are on (until office.acOff). "
                     "Stopped, it is the backdrop's own still fan (no frame needed)"},
            {"id": "pennant", "what": "the pennant at the top of the flagpole, stirring: O.O.P.S. in white on gray", "frames": pen["files"], "fps": 3,
             "at": pen["at"], "foot": pen["foot"], "rect": pen["rect"], "base": r1(K.row_of(FLAG["z"])), "note": "on the flagpole's base, laid just after it"},
        ],
        "fx_note": "Moving: the fan (until the switch is pulled) and the pennant. The unit's hum is a sound. Nothing else moves by nature here: "
                   "no wind down here (the high cloud is combed by wind far up), and the desert's sagebrush is still.",
        "cutouts": {name: box_of(a) for name, (c, a) in cuts.items()},
        "exits": [],
        "exits_note": "no way out across the picture's edges: Ranger goes into the building by the unit's intake (a script, into office-ducts at "
                      "its mark `intake`), and the lot is left by the Office's map",
    }
    with open(f"{OUT}/layout.json", "w") as f:
        json.dump(lay, f, indent=1)
    return lay


if __name__ == "__main__":
    print(json.dumps(marks(), indent=1))
    print("roof full", ROOF_FULL)

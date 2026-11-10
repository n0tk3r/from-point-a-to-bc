"""PAINT-23: the foot of Mount Shosha's layout.json, measured from the camera, the kit's places and the painted cut-outs
(edo_shosha.py calls write() at the end of a full run). Every number of js/content/scenes/edo-shosha.js comes from here:
`python3 edo_shosha_layout.py numbers` prints them as the scene file writes them (out/edo-shosha-work/scene-numbers.txt),
and write() also writes out/edo-shosha-remap.json (where every old mark, arriving place and standing place of round
twenty-one's picture is now: js/content/checkpoints.js is the lead's to change, not ours)."""

import json
import math
import os
import sys

import numpy as np

from edo_shosha_kit import *
import edo_shosha_far as FAR

# Round twenty-one's places (PAINT-21E's picture, horizon 280, full 590), for the remap: name -> (x, y)
OLD = {
    "road": (735, 548), "stone": (248, 484), "path": (214, 468), "ryokai": (236, 456), "hall": (493, 477), "lock": (485, 473), "step": (514, 470),
    "ume": (572, 456), "hut": (62, 466), "bench": (642, 508), "tome": (604, 489), "wife": (647, 489), "girl": (690, 489), "view": (690, 455), "combs": (686, 518),
    "LATTICE": (330, 463), "DOORWAY": (458, 470), "talk.ryokai": (266, 470), "talk.ume": (548, 470), "talk.tome": (612, 512), "talk.wife": (652, 514),
    "talk.girl": (700, 514), "talk.hall": (493, 480), "arrive.road.0": (700, 560), "arrive.road.1": (764, 566), "arrive.lock.0": (456, 482),
    "arrive.lock.1": (512, 482), "arrive.hall.0": (456, 486), "arrive.hall.1": (532, 486), "edge.E": (788, 560), "talk.lattice": (356, 480),
    "homeward.0": (600, 520), "homeward.1": (760, 580), "night.ume": (470, 474),
}

r = lambda q: [int(round(q[0])), int(round(q[1]))]


def inside(poly, p):
    x, y = p
    n = len(poly)
    ins = False
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if (y0 > y) != (y1 > y):
            if x0 + (y - y0) * (x1 - x0) / (y1 - y0) > x:
                ins = not ins
    return ins


def hull(alpha, pad=2, step_=8):
    """The outline of a cut-out's painted pixels (a convex hull, padded), as picture points."""
    ys, xs = np.where(alpha > 0.5)
    if not len(ys):
        return []
    pts = []
    for yy in range(int(ys.min()), int(ys.max()) + 1, step_):
        row = xs[(ys >= yy) & (ys < yy + step_)]
        if len(row):
            pts += [(int(row.min()) - pad, yy), (int(row.max()) + pad, yy)]
    pts += [(int(xs[ys == ys.max()].min()) - pad, int(ys.max()) + pad), (int(xs[ys == ys.max()].max()) + pad, int(ys.max()) + pad),
            (int(xs[ys == ys.min()].min()) - pad, int(ys.min()) - pad), (int(xs[ys == ys.min()].max()) + pad, int(ys.min()) - pad)]
    pts = sorted(set(pts))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return [list(p) for p in lo[:-1] + up[:-1]]


def box_of(alpha):
    ys, xs = np.where(alpha > 0.5)
    if not len(ys):
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


def places():
    """Every place of the scene file, as picture points."""
    M = {k: r(foot(*v)) for k, v in MARKS_W.items()}
    out = dict(M=M)
    out["LATTICE"] = r(foot(*LATTICE_W))
    out["DOORWAY"] = r(foot(*DOORWAY_W))
    out["HOMEWARD"] = [r(foot(*HOMEWARD_W[0])), r(foot(*HOMEWARD_W[1])), [830, 612]]
    out["TALK_AT"] = {k: r(foot(*v)) for k, v in TALK_W.items()}
    out["arrive"] = {k: [r(foot(*q)) for q in v] for k, v in ARRIVE_W.items()}
    out["edgeE"] = [790, 566]
    out["latticeTalk"] = r(foot(*LATTICE_TALK_W))
    out["nightUme"] = r(foot(*NIGHT_UME_W))
    out["walk"] = [r(p) for p in walk_outline()]
    # the solid ground: the stone, the heap of combs on its cloth (the bench's is its cut-out's solid)
    X, D = STONE
    w, h, t = STONE_SIZE
    out["stone_solid"] = [r(foot(X - w / 2 - 8, D - 8)), r(foot(X + w / 2 + 8, D - 8)), r(foot(X + w / 2 + 8, D + t + 10)), r(foot(X - w / 2 - 8, D + t + 10))]
    cx, cd = COMBS
    out["combs_solid"] = [r(foot(cx - 50, cd - 34)), r(foot(cx + 50, cd - 38)), r(foot(cx + 56, cd + 32)), r(foot(cx - 44, cd + 36))]
    fl, fr, br, bl = bench_pts()
    out["bench_solid"] = [r(foot(*fl)), r(foot(*fr)), r(foot(*br)), r(foot(*bl))]
    out["bench_base"] = [r(foot(*fl)), r(foot(*fr))]
    out["stone_base"] = int(round(foot(X, D)[1]))
    return out


def things(pl, cuts):
    """Every clickable area, as the scene file gives it (back to front)."""
    A = {k: (v[1] > 0.5) for k, v in cuts.items()}
    M, T = pl["M"], pl["TALK_AT"]
    th = {}
    # the sky over the valley: right of the spur, above the far hills (the bough's pads lie over its top left)
    sx = [int(round(np.interp(y, [p[1] for p in FAR.SPUR], [p[0] for p in FAR.SPUR]))) for y in (0, 80, 160, 240, 300)]
    th["sky"] = [[sx[0] + 40, 0], [800, 0], [800, 300], [720, 306], [660, 312], [sx[4] + 6, 300], [sx[3] + 4, 240], [sx[2] + 4, 160], [sx[1] + 20, 80]]
    # the mountain: the woods and the slope above the terrace's back, left of the spur (the trees, the cherry, the hut,
    # the path and the hall lie over it)
    th["mountain"] = [[100, 0], [sx[0] + 30, 0], [sx[1] + 10, 80], [sx[2], 160], [sx[3], 240], [sx[4], 300], [616, 334], [470, 300], [300, 250], [100, 240]]
    th["plain"] = [[618, 330], [800, 322], [800, 446], [740, 446], [680, 440], [618, 436]]
    cxp, cyp = FAR.CASTLE_AT
    th["castle"] = [[int(cxp - 30), int(cyp - 34)], [int(cxp + 30), int(cyp - 34)], [int(cxp + 30), int(cyp + 6)], [int(cxp - 30), int(cyp + 6)]]
    th["trees"] = [[96, 190], [470, 190], [470, 300], [360, 300], [260, 330], [96, 330]]
    import edo_shosha_things as TH_
    x0_, y0_, x1_, y1_ = (int(round(v)) for v in TH_.cherry_box())
    th["cherry"] = [[x0_, y0_], [x1_, y0_], [x1_, y1_], [x0_, y1_]]               # its blossom
    hw, hd, wall = HUT["w"], HUT["d"], HUT["wall"]
    Q = lambda a, b, y: r(P(*hut_at(a, b)[:1], y, hut_at(a, b)[1]))
    e = HUT["eave"]
    th["hut"] = [Q(0, 0, 0), Q(hw, 0, 0), Q(hw + e, -e, wall - 6), Q(hw - 55, hd / 2, HUT["ridge"]), Q(55, hd / 2, HUT["ridge"]), Q(-e, -e, wall - 6), Q(-e, hd + e, wall - 6), Q(0, hd, 0)]
    la, lb, ly = HUT_LANTERN_AB
    lx, lyy = P(*hut_at(la, lb)[:1], ly, hut_at(la, lb)[1])
    th["lantern"] = [[int(lx) - 10, int(lyy) - 8], [int(lx) + 10, int(lyy) - 8], [int(lx) + 10, int(lyy) + 24], [int(lx) - 10, int(lyy) + 24]]
    # the east path: its steps from the foot up to where the woods take it
    import edo_shosha_things as TH
    st = TH.path_steps()
    top = st[11]
    a0, b0 = st[0]["front"]
    a1, b1 = top["front"]
    th["pathup"] = [r(P(a0[0] - 10, 0, a0[1])), r(P(b0[0] + 10, 0, b0[1])), r(P(b1[0] + 6, top["y1"], b1[1])), r(P(a1[0] - 6, top["y1"], a1[1]))]
    th["stone"] = hull(A["stone"], 3, 8)
    bo = BASE_OUT
    ev = EAVE_OUT
    ye = EAVE_Y - EAVE_DROP
    th["hall"] = [r(HP(-ev, -ev, ye)), r(HP(SIDE / 2, SIDE / 2, APEX_Y + 40)), r(HP(SIDE + ev, -ev, ye)), r(HP(SIDE + bo, -bo, 0)), r(HP(-bo, -bo, 0)), r(HP(-bo, SIDE + bo, 0)),
                  r(HP(-ev, SIDE + ev, ye))]
    lb0, lb1 = LATTICE_B
    ly0, ly1 = LATTICE_Y
    th["lattice"] = [r(HP(0, lb0 - 8, ly0 - 8)), r(HP(0, lb1 + 8, ly0 - 8)), r(HP(0, lb1 + 8, ly1 + 8)), r(HP(0, lb0 - 8, ly1 + 8))]
    da, db = DOOR_A
    th["slips"] = [r(HP(2, -3, 64)), r(HP(da - 2, -3, 64)), r(HP(da - 2, -3, 272)), r(HP(2, -3, 272))]
    th["slips2"] = [r(HP(db + 2, -3, 64)), r(HP(SIDE - 2, -3, 64)), r(HP(SIDE - 2, -3, 272)), r(HP(db + 2, -3, 272))]
    th["doors"] = hull(A["doors"], 2, 10)
    th["doors_open"] = hull(np.maximum(A["doors-open"], A["doors"]), 2, 10)
    s_ = STEP
    th["step"] = [r(HP(s_["a0"], -bo - s_["out"], 0)), r(HP(s_["a1"], -bo - s_["out"], 0)), r(HP(s_["a1"], -bo, s_["h"])), r(HP(s_["a0"], -bo, s_["h"]))]
    th["stepball"] = hull(A["stepball"], 4, 6)
    lk = LOCK_AT
    p0, p1 = HP(lk[0] - 24, -6, lk[1] - 16), HP(lk[0] + 24, -6, lk[1] + 16)
    th["lock"] = [[int(min(p0[0], p1[0])), int(min(p0[1], p1[1]))], [int(max(p0[0], p1[0])), int(min(p0[1], p1[1]))], [int(max(p0[0], p1[0])), int(max(p0[1], p1[1]))], [int(min(p0[0], p1[0])), int(max(p0[1], p1[1]))]]
    th["bench"] = hull(A["bench"], 3, 8)
    th["combs"] = pl["combs_solid"]
    return th


def person_box(mark_xy, cm, seated=False):
    """A person's clickable box (x, y, w, h) at a place, as the game sizes them."""
    x, y = mark_xy
    hp = 160.0 * scale_at(y) * cm / 175.0 * (0.74 if seated else 1.0)
    w = max(20, hp * 0.38)
    return [int(round(x - w / 2)), int(round(y - hp - 2)), int(round(w)), int(round(hp + 4))]


def write(path, cuts, info):
    pl = places()
    th = things(pl, cuts)
    M = pl["M"]
    bad = []
    pts = dict(M)
    for k in ("LATTICE", "latticeTalk", "nightUme"):                         # (DOORWAY is up on the step at the doors: the women
        pts[k] = pl[k]                                                      # step up to it by moveTo, which walks straight, as before)
    for k, v in pl["TALK_AT"].items():
        pts["talk." + k] = v
    for k, v in pl["arrive"].items():
        for i, q in enumerate(v):
            pts[f"arrive.{k}.{i}"] = q
    for name, p in pts.items():
        if not inside(pl["walk"], p):
            bad.append(f"{name} {p} is outside the walk outline")
        for b in (pl["stone_solid"], pl["combs_solid"], pl["bench_solid"]):
            if inside(b, p):
                bad.append(f"{name} {p} is on solid ground")
    for b in bad:
        print("LAYOUT:", b)
    boxes = {"ume": person_box(M["ume"], 136), "ryokai": person_box(M["ryokai"], 150, True), "ryokaiUp": person_box(M["ryokai"], 150),
             "lattice": person_box(pl["LATTICE"], 150), "tome": person_box(M["tome"], 138, True), "wife": person_box(M["wife"], 146, True),
             "girl": person_box(M["girl"], 138, True)}
    cherry_from = th["cherry"]
    lay = {
        "id": ID, "horizon": HZ, "full": FULL, "minScale": 0.3,
        "camera": {"what": "level, the eye 2.52 m above the terrace, lens 700 px, its axis's vanishing point at x 400; the hall square to the compass and so turned 26 degrees in our view (vanishing points x 59 and x 1835)",
                   "eye_cm": round(EYE, 1), "focal": F, "vanish_x": CX, "hall_turn_deg": 26},
        "light": "two states, the same geometry. GOLD (back.png and the plain cut-outs): the late afternoon sun 38 degrees behind the left, 30 up: the hall's west side in full sun, its front at a slant, shadows to the right and away, the old pine's bough and the trees behind us shading the terrace at the left and right. SUNSET (sunset.png and every cut-out's -sunset twin): the sun at the left, 6 up, behind the woods: the west side red, the front in blue shade, the terrace in the woods' long shadow with streaks of red light across it; the eastern sky over the plain in rose and cobalt, its clouds lit from below. Key: edo-sunset.",
        "walk": pl["walk"], "blocked": [pl["stone_solid"], pl["combs_solid"]],
        "blocked_note": "the stone at the path's foot, the heap of combs on its cloth; the bench is its cut-out's solid",
        "planes": [
            {"id": "sunset", "file": "sunset.png", "plane": "back", "what": "the whole stage at sunset (faded in over back.png, under everybody)"},
            {"id": "doors", "plane": "back", "states": {"shut": "doors.png", "half": "doors-half.png", "open": "doors-open.png", "shut-sunset": "doors-sunset.png",
                                                       "half-sunset": "doors-half-sunset.png", "open-sunset": "doors-open-sunset.png"}},
            {"id": "lock", "plane": "back", "states": {"shut": "lock.png", "open": "lock-open.png", "shut-sunset": "lock-sunset.png", "open-sunset": "lock-open-sunset.png"}},
            {"id": "stepball", "plane": "back", "states": {"there": "stepball.png", "there-sunset": "stepball-sunset.png"}},
            {"id": "stone", "base": pl["stone_base"], "states": {"gold": "stone.png", "sunset": "stone-sunset.png"}, "solid": pl["stone_solid"]},
            {"id": "bench", "base": pl["bench_base"], "states": {"gold": "bench.png", "sunset": "bench-sunset.png"}, "solid": pl["bench_solid"]},
            {"id": "pine", "plane": "front", "states": {"gold": "pine.png", "sunset": "pine-sunset.png"}, "what": "the old pine's trunk up the left edge and its great bough across the top (it stirs: fx pine)"},
            {"id": "near", "plane": "front", "states": {"gold": "near.png", "sunset": "near-sunset.png"}, "what": "its roots, moss and ferns along the bottom left; grass and ferns on the bank's lip in the bottom right corner (still)"},
        ],
        "cutouts": {k: box_of(v[1]) for k, v in cuts.items()},
        "marks": M, "faces": FACES, "LATTICE": pl["LATTICE"], "DOORWAY": pl["DOORWAY"], "HOMEWARD": pl["HOMEWARD"], "TALK_AT": pl["TALK_AT"],
        "arrive": pl["arrive"], "edgeE": pl["edgeE"], "latticeTalk": pl["latticeTalk"], "nightUme": pl["nightUme"], "boxes": boxes,
        "things": [{"id": k, "shape": {"poly": v}} for k, v in th.items()] +
                  [{"id": k, "shape": {"poly": [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]}, "person": True} for k, (x, y, w, h) in
                   (("ume", boxes["ume"]), ("ryokai", boxes["ryokai"]), ("tome", boxes["tome"]), ("wife", boxes["wife"]), ("girl", boxes["girl"]))],
        "stands": {k: {"at": v, "grownup_px": int(round(160 * scale_at(v[1]))), "floor": "ground"} for k, v in M.items()},
        "fx": [
            {"id": "pine", "type": "sway", "plane": "pine", "anchor": "bottom", "amount": 1.0, "period": 4.6},
            {"id": "petals", "type": "petals", "from": cherry_from, "floor": 380, "count": 4, "wind": 10, "fall": 18, "size": [2, 3], "color": "#f2c9d4", "color2": "#e2a8bc", "plane": "back"},
            {"id": "crows", "type": "birds", "lanes": [[[830, 196], [520, 70]], [[830, 250], [600, 128]]], "every": [9, 18], "group": [1, 2], "speed": 50, "size": 8, "plane": "back"},
        ],
        "problems": bad,
    }
    remap = []
    new_of = dict(pts)
    for k in ("road", "stone", "path", "ryokai", "hall", "lock", "step", "ume", "hut", "bench", "tome", "wife", "girl", "view", "combs"):
        new_of[k] = M[k]
    new_of["edge.E"] = pl["edgeE"]
    new_of["talk.lattice"] = pl["latticeTalk"]
    new_of["homeward.0"], new_of["homeward.1"] = pl["HOMEWARD"][0], pl["HOMEWARD"][1]
    new_of["night.ume"] = pl["nightUme"]
    new_of["DOORWAY"] = pl["DOORWAY"]
    for name, old in OLD.items():
        if name in new_of:
            remap.append([old[0], old[1], new_of[name][0], new_of[name][1]])
        else:
            print("REMAP: no new place for", name)
    lay["remap"] = {"points": remap, "note": "round twenty-one's marks, arriving places, standing places and the night's place for O-Ume, and where each is in this picture: [old x, old y, new x, new y]"}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(lay, f, indent=1)
    with open("out/edo-shosha-remap.json", "w") as f:
        json.dump({"points": remap}, f)
    os.makedirs("out/edo-shosha-work", exist_ok=True)
    with open("out/edo-shosha-work/scene-numbers.txt", "w") as f:
        f.write(scene_numbers(lay) + "\n")
    return lay


def scene_numbers(lay):
    j = lambda v: json.dumps(v).replace(", ", ", ")
    M = lay["marks"]
    th = {t["id"]: t["shape"]["poly"] for t in lay["things"]}
    out = [f"const HORIZON = {lay['horizon']}, FULL = {lay['full']};", f"const FLOOR = {j(lay['walk'])};",
           "const M = { " + ", ".join(f"{k}: {j(v)}" for k, v in M.items()) + " };",
           f"const LATTICE = {j(lay['LATTICE'])};", f"const DOORWAY = {j(lay['DOORWAY'])};", f"const HOMEWARD = {j(lay['HOMEWARD'])};",
           "const TALK_AT = { " + ", ".join(f"{k}: {j(v)}" for k, v in lay["TALK_AT"].items()) + " };",
           f"blocked: {j(lay['blocked'])},", "arrive: { " + ", ".join(f"{k}: {j(v)}" for k, v in lay["arrive"].items()) + " },",
           f"edges E walkTo: {j(lay['edgeE'])}", f"stone base: {lay['planes'][4]['base']}, solid: {j(lay['planes'][4]['solid'])}",
           f"bench base: {j(lay['planes'][5]['base'])}, solid: {j(lay['planes'][5]['solid'])}",
           "const BOX = { " + ", ".join(f"{k}: {j(v)}" for k, v in lay["boxes"].items()) + " };",
           f"lattice talk walkTo: {j(lay['latticeTalk'])}", f"night ume: {j(lay['nightUme'])}"]
    for k, v in th.items():
        out.append(f"{k}: {j(v)}")
    for f in lay["fx"]:
        out.append(json.dumps(f))
    return "\n".join(out)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pl = places()
    for k, v in pl["M"].items():
        print(f"  {k:8s} {v}  {160 * scale_at(v[1]):5.1f} px")
    print("  LATTICE", pl["LATTICE"], "DOORWAY", pl["DOORWAY"], "TALK", pl["TALK_AT"], "arrive", pl["arrive"])

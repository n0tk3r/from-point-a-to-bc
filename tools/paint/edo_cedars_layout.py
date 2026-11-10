"""PAINT-23: the cedar path's layout.json, measured from the camera, the kit's places and the finished pictures
(edo_cedars.py calls layout(info, cuts) at the end of a run). Every number of js/content/scenes/edo-cedars.js comes from
here: `python3 edo_cedars.py` prints them as the scene file writes them (scene_numbers), and writes
out/edo-cedars-remap.json (where every old mark and standing place of round twenty's picture is now)."""

import json
import math

import numpy as np

from edo_cedars_kit import *

# Round twenty's places (PAINT-20C's picture, horizon 250, full 600), for the remap: name -> (x, y)
OLD = {
    "enter": (400, 580), "figure": (340, 540), "pipe": (612, 452), "door": (404, 444), "window": (536, 444), "isukeFrom": (340, 596),
    "lift": (514, 447), "arrive.enter.0": (452, 586), "arrive.enter.1": (352, 588), "arrive.door.0": (372, 448), "arrive.door.1": (446, 452),
    "walkTo.cedars": (404, 520), "walkTo.mist": (380, 500), "walkTo.rain": (404, 540), "walkTo.steps": (410, 560), "walkTo.storehouse": (430, 448),
    "walkTo.kiln": (566, 452),
    "isukeWay.1": (360, 566), "isukeWay.2": (388, 528), "isukeWay.3": (410, 492), "isukeWay.4": (420, 464), "isukeWay.5": (410, 448),
}


def r2(p):
    return [int(round(p[0])), int(round(p[1]))]


def r1(p):
    return [round(float(p[0]), 1), round(float(p[1]), 1)]


def box_of(alpha):
    ys, xs = np.where(alpha > 0.5)
    if not len(ys):
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


def clip_x(poly, x0, x1):
    """A polygon cut to the upright band x0..x1 (so that a trunk standing before the storehouse keeps its own clicks)."""
    def cut(pts, x, keep_right):
        out = []
        n = len(pts)
        for i in range(n):
            a, b = pts[i], pts[(i + 1) % n]
            ain = (a[0] >= x) if keep_right else (a[0] <= x)
            bin_ = (b[0] >= x) if keep_right else (b[0] <= x)
            if ain:
                out.append(a)
            if ain != bin_:
                q = (x - a[0]) / (b[0] - a[0])
                out.append((x, a[1] + (b[1] - a[1]) * q))
        return out
    return cut(cut(list(poly), x0, True), x1, False)


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


def trunk_band(spec, pad=3):
    """The picture columns a walk-behind trunk fills where it crosses the storehouse and the kiln: (x from, x to)."""
    px_, py_, r, lean = spec
    L, R = trunk_edges((px_, py_), r, lean)
    rows = [q for q in zip(L, R) if 330 <= q[0][1] <= py_]
    return (min(q[0][0] for q in rows) - pad, max(q[1][0] for q in rows) + pad)


def places():
    """Every place of the scene file, as picture points: marks, standing places, the shapes of things, the effects."""
    Hs = HOUSE
    LW, LD, e = Hs.LW, Hs.LD, Hs.eave
    yu, yt = Hs.eave_under, Hs.eave_top
    (r0u, r0w), (r1u, r1w) = Hs.ridge_at
    cl, cr = trunk_band(CEDAR_L[0]), trunk_band(CEDAR_R[0])
    x_lo, x_hi = cl[1], cr[0]                                 # the storehouse's own clicks lie between the two trunks
    M = {k: r2(P(v)) for k, v in MARKS.items()}
    lift = r2(P(LIFT_AT))
    w0, w1, ws, wh = Hs.window
    sill = r2(Hs.pt((w0 + w1) / 2, 0, ws + 1.0))
    d0, d1, dh = Hs.door
    door = [r2(Hs.pt(0, d1, 0)), r2(Hs.pt(0, d0, 0)), r2(Hs.pt(0, d0, dh)), r2(Hs.pt(0, d1, dh))]
    win_pts = [Hs.pt(u, 0, y) for u in (w0 - 8, w1 + 8) for y in (ws - 10, wh + 8)]
    wx0, wx1 = min(p[0] for p in win_pts), max(p[0] for p in win_pts)
    wy0, wy1 = min(p[1] for p in win_pts), max(p[1] for p in win_pts)
    window = [int(math.floor(wx0)), int(math.floor(wy0)), int(math.ceil(wx1 - wx0)) + 1, int(math.ceil(wy1 - wy0)) + 1]
    # the storehouse's outline: the ground line under both walls, the thatch, the ridge
    sil = [Hs.foot(0, LD), Hs.foot(0, 0), Hs.foot(LW, 0), Hs.pt(LW, 0, yu), Hs.pt(LW + e, -e, yu), Hs.pt(LW + e, -e, yt),
           Hs.pt(r1u, r1w, Hs.ridge + 8), Hs.pt(r0u, r0w, Hs.ridge + 8), Hs.pt(-e, LD + e, yt), Hs.pt(-e, LD + e, yu), Hs.pt(0, LD, yu)]
    storehouse = [r2(p) for p in clip_x(sil, x_lo, x_hi)]
    eaves = [r2(p) for p in clip_x([Hs.pt(-e, LD + e, yu), Hs.pt(-e, -e, yu), Hs.pt(LW + e, -e, yu), Hs.pt(LW + e, -e, yt), Hs.pt(-e, -e, yt), Hs.pt(-e, LD + e, yt)], x_lo, x_hi)]
    light = [r2(p) for p in clip_x([Hs.foot(0, LD), Hs.foot(0, 0), Hs.foot(LW, 0), Hs.pt(LW, 0, -8), Hs.pt(0, 0, -8), Hs.pt(0, LD, -8)], x_lo, x_hi)]
    kx, kd = KILN["at"]
    r, h = KILN["r"], KILN["h"]
    dome = [on(kx + r * math.cos(a), kd, h * math.sin(a) ** 0.85) for a in np.linspace(0, math.pi, 9)]
    front = [on(kx - r * math.cos(b), kd - r * 0.92 * math.sin(b)) for b in np.linspace(0, math.pi, 6)]
    kiln = [r2(p) for p in clip_x(dome + front[1:-1], 0, cl[0])]
    jx, jd = JIZO["at"]
    kf = CAM.px_cm(jx, jd)
    fx_, fy_ = on(jx, jd)
    figure = [int(round(fx_ - 15 * kf)), int(round(fy_ - (JIZO["h"] + 12) * kf)), int(round(30 * kf)), int(round((JIZO["h"] + 20) * kf))]
    pa, pb = pipe_ends()
    pipe = [int(round(min(pa[0], pb[0]) - 9)), int(round(min(pa[1], pb[1]) - 10)), int(round(abs(pa[0] - pb[0]) + 18)), int(round(abs(pa[1] - pb[1]) + 20))]
    st = steps()
    steps_poly = [r2(level(*st[0]["l"], st[0]["Y"])), r2(level(*st[0]["r"], st[0]["Y"])), r2(level(*st[1]["r"], st[1]["Y0"])), r2(level(*st[1]["l"], st[1]["Y0"]))]
    steps_poly = [[steps_poly[0][0], 600], [steps_poly[1][0], 600], steps_poly[2], steps_poly[3]]
    stand = {"cedars": r2(P(G(300, 548))), "mist": r2(P(G(296, 550))), "rain": r2(P(G(304, 546))), "steps": r2(P(G(262, 574))),
             "storehouse": r2(P(G(470, 521))), "eaves": r2(P(G(470, 521))), "light": r2(P(G(470, 521))), "kiln": r2(P(KILN_STAND))}
    # ---- the effects
    behind = [[r1(Hs.pt(-e, -e, yu)), r1(Hs.pt(LW + e, -e, yu)), r1(Hs.foot(LW + e, -e)), r1(Hs.foot(-e, -e))],
              [r1(Hs.pt(-e, LD + e, yu)), r1(Hs.pt(-e, -e, yu)), r1(Hs.foot(-e, -e)), r1(Hs.foot(-e, LD + e))]]
    floor = []
    for s_ in st[:6]:
        a, b = level(*s_["l"], s_["Y"]), level(*s_["r"], s_["Y"])
        floor.append([[int(round(a[0] + 6)), int(round(a[1] - 4))], [int(round(b[0] - 6)), int(round(b[1] - 4))]])
    drips = []
    for (u, w) in ((-e, 250.0), (70.0, -e), (340.0, -e)):               # by the bales on the door wall; by the near corner; right of the window
        top, bot = Hs.pt(u, w, yu), Hs.foot(u, w)
        drips.append(dict(path=[r1(top), r1(bot)], base=int(round(bot[1])) + 1))
    walk = [list(p) for p in WALK]
    blocked = [[r2(p) for p in b] for b in BLOCKED]
    arrive = {k: [r2(P(q)) for q in v] for k, v in ARRIVE.items()}
    way = [r2(P(q)) for q in ISUKE_WAY]
    # the two walk-behind trunks' base lines: across the foot of each, where its front meets the ground
    bases = {}
    for name, spec in (("cedar-l", CEDAR_L[0]), ("cedar-r", CEDAR_R[0])):
        px0, py0, rr, lean = spec
        x, d = G(px0, py0)
        a, b = on(x - rr * 2.0, d - rr * 0.5), on(x + rr * 2.0, d - rr * 0.5)
        bases[name] = [r2(a), r2(b)]
    sil_all = [r2(p) for p in sil]
    # the cedars' own area: everything above and beside the storehouse, down the two trunks that stand before it (its
    # outline follows the roof, so that Show draws no line across the storehouse), and the great cedar down the left edge
    roof = [p for p in storehouse if p[1] < 360 or p[0] >= x_hi - 1]
    right_cut = sorted([p for p in storehouse if abs(p[0] - round(x_hi)) <= 1], key=lambda p: -p[1])
    left_top = min([p for p in storehouse if abs(p[0] - round(x_lo)) <= 1], key=lambda p: p[1])
    ridge = [p for p in storehouse if p[1] < 300 and abs(p[0] - round(x_hi)) > 1]
    cedars = [[0, 0], [800, 0], [800, 362], [int(round(cr[1])), 398], [int(round(cr[1])), 470]] + right_cut + ridge + [left_top, [left_top[0], 470], [110, 470], [100, 600], [0, 600]]
    return dict(M=M, lift=lift, sill=sill, door=door, window=window, cedars=cedars, storehouse=storehouse, eaves=eaves, light=light, kiln=kiln, figure=figure, pipe=pipe,
                steps=steps_poly, stand=stand, behind=behind, floor=floor, drips=drips, walk=walk, blocked=blocked, arrive=arrive, way=way, bases=bases,
                house_outline=sil_all, kiln_outline=[r2(p) for p in dome + front[1:-1]], bands=dict(cedar_l=[round(v) for v in cl], cedar_r=[round(v) for v in cr]))


def check(pl):
    """Every mark, standing place and arriving place inside the walk outline and off the blocked patches."""
    bad = []
    walk = pl["walk"]
    pts = dict(pl["M"])
    pts["lift"] = pl["lift"]
    for k, v in pl["stand"].items():
        pts["walkTo." + k] = v
    for k, v in pl["arrive"].items():
        for i, q in enumerate(v):
            pts[f"arrive.{k}.{i}"] = q
    for i, q in enumerate(pl["way"]):
        pts[f"isukeWay.{i}"] = q
    for name, p in pts.items():
        if not inside(walk, p) and not (name in ("isukeFrom", "isukeWay.0") and p[1] >= 596):
            bad.append(f"{name} {p} is outside the walk outline")
        if any(inside(b, p) for b in pl["blocked"]):
            bad.append(f"{name} {p} is on a blocked patch")
    return bad, pts


def layout(info, cut, puddles=()):
    pl = places()
    bad, pts = check(pl)
    for b in bad:
        print("LAYOUT:", b)
    Hs = HOUSE
    M = pl["M"]
    things = [
        {"id": "cedars", "what": "the cedars: the great one we stand under (the front plane), the two beside the path that people walk behind, the backdrop's own round the yard, and rank behind rank going up the hill into the mist",
         "shape": {"poly": pl["cedars"]},
         "stand": pl["stand"]["cedars"], "face": "N"},
        {"id": "mist", "what": "mist in the gap up the hill on the left, between the trunks", "shape": {"poly": [[98, 250], [316, 250], [316, 400], [200, 440], [98, 440]]}, "stand": pl["stand"]["mist"], "face": "NW"},
        {"id": "rain", "what": "the rain: fine straight slanting lines, steady (the engine's moving thing: fx 'rain')", "shape": {"poly": [[0, 0], [800, 0], [800, 150], [0, 150]]}, "stand": pl["stand"]["rain"], "face": "N"},
        {"id": "steps", "what": "the worn stone steps, wet, low and broad, a puddle on four of the treads (only the two bottom treads are the thing to click: a click anywhere else on them walks there)",
         "shape": {"poly": pl["steps"]}, "stand": pl["stand"]["steps"], "face": "N"},
        {"id": "storehouse", "what": "the charcoal-burner's storehouse, three-quarters on and seen from below: dark boards, a steep thatch heavy with rain coming down low over the walls, the floor on posts",
         "shape": {"poly": pl["storehouse"]}, "stand": pl["stand"]["storehouse"], "face": "N"},
        {"id": "eaves", "what": "the thatch's thick cut edge along both walls, dripping", "shape": {"poly": pl["eaves"]}, "stand": pl["stand"]["eaves"], "face": "N"},
        {"id": "light", "what": "the dark under the raised floor along both walls, and the thin line of lamplight in it (the cut-out light-on; it goes out and comes back)",
         "shape": {"poly": pl["light"]}, "stand": pl["stand"]["light"], "face": "N"},
        {"id": "door", "what": "the storehouse's plank door, up two steps (a flat stone, a wooden step), in the wall that faces down the hill to the left; barred on the inside",
         "shape": {"poly": pl["door"]}, "stand": M["door"], "face": "NE"},
        {"id": "window", "what": "the small high square window in the storehouse's other wall (inside, the wall with the sacks under it): a seven-year-old fits, lifted; lit from inside while the lantern is (window-lit)",
         "shape": {"rect": pl["window"]}, "stand": M["window"], "face": "NW", "lift": pl["lift"], "sill": pl["sill"]},
        {"id": "kiln", "what": "the earth charcoal kiln up to the left of the yard: a dome with a low mouth half walled up, cold; cut wood stacked before it", "shape": {"poly": pl["kiln"]},
         "stand": pl["stand"]["kiln"], "face": "NW"},
        {"id": "figure", "what": "a small stone figure beside the lower steps: a roadside Jizo, worn smooth, in a red bib, on a flat stone with three pebbles and a coin (scenery)",
         "shape": {"rect": pl["figure"]}, "stand": M["figure"], "face": "E"},
        {"id": "pipe", "what": "a bamboo pipe out of the cut bank behind the storehouse's far end, at the height of an ear (air for the room underneath; a murmur comes out of it)",
         "shape": {"rect": pl["pipe"]}, "stand": M["pipe"], "face": "N"},
        {"id": "isuke", "what": "Isuke, the constable's man, when he comes up the path (#27): seen only in the storehouse's looks out at the path; his way is isukeWay, ending at marks.door",
         "shape": {"rect": [M["door"][0] - 16, M["door"][1] - 96, 32, 98]}, "stand": pl["stand"]["storehouse"], "face": "W", "when": "edo.isukeOnPath"},
    ]
    planes = [
        {"id": "light-on", "file": "light-on.png", "plane": "back", "alt": True, "box": box_of(cut["light-on"][1]),
         "note": "the line of lamplight under the floor, and what it lights there: show it while the lamp below is lit (it goes out when they call, and comes back); the backdrop has the dark alone"},
        {"id": "window-lit", "file": "window-lit.png", "plane": "back", "alt": True, "box": box_of(cut["window-lit"][1]),
         "note": "the small high window lit from inside: show it while the lantern in the storehouse is lit; the backdrop has the window dark"},
        {"id": "cedar-l", "file": "cedar-l.png", "base": pl["bases"]["cedar-l"], "box": box_of(cut["cedar-l"][1]), "what": "the cedar between the kiln's corner of the yard and the door: people going to the kiln pass behind it"},
        {"id": "cedar-r", "file": "cedar-r.png", "base": pl["bases"]["cedar-r"], "box": box_of(cut["cedar-r"][1]), "what": "the cedar below the far end of the window's wall: people going along to the pipe pass behind it"},
        {"id": "front", "file": "front.png", "plane": "front", "box": box_of(cut["front"][1]),
         "what": "the front plane: the great cedar up the left edge with its roots and ferns, a bough across the top right corner, fern fronds in the bottom right corner"},
    ]
    drip_what = ["off the thatch over the bales, on the door wall", "off the thatch by the near corner", "off the thatch right of the window"]
    fx = [
        {"id": "rain", "type": "rain", "what": "fine steady spring rain over the whole stage, in front of everything; not drawn where the thatch shelters the walls and the dry strip of ground under it; splashes along six treads",
         "area": [[0, 0], [800, 0], [800, 600], [0, 600]], "slant": 8, "count": 480, "length": [10, 22], "speed": 520, "color": "#dfe6ec", "opacity": 0.42,
         "behind": pl["behind"], "floor": pl["floor"], "splash": 2, "plane": "front"},
    ]
    for i, d_ in enumerate(pl["drips"]):
        fx.append({"id": f"drip-{i + 1}", "type": "stream", "what": "a drip " + drip_what[i], "path": d_["path"], "width": 1, "color": "#cfd8e0", "light": "#eef2f4",
                   "opacity": 0.5, "speed": 90, "splash": 2, "base": d_["base"]})
    for i, (cx, cy, rx, ry) in enumerate(list(puddles)[:3]):
        fx.append({"id": f"puddle-{i + 1}", "type": "ripples", "what": "rain ringing a puddle on a tread", "at": [int(round(cx)), int(round(cy))], "radius": [1, max(4, int(round(rx * 0.8)))],
                   "flat": round(max(0.18, min(0.5, ry / max(rx, 1))), 2), "every": [0.4, 1.4] if i < 2 else [0.5, 1.6], "rings": 1, "speed": [16, 14, 12][i], "color": "#c8d4dc",
                   "opacity": 0.5 if i < 2 else 0.45,
                   "clip": [[int(round(cx - rx)), int(round(cy - ry))], [int(round(cx + rx)), int(round(cy - ry))], [int(round(cx + rx)), int(round(cy + ry))], [int(round(cx - rx)), int(round(cy + ry))]]})
    fx.append({"id": "mist-l", "type": "smoke", "what": "mist drifting through the gap up the hill on the left, slow and wide, toward the storehouse (it passes behind the kiln and the storehouse)",
               "at": [150, 432], "height": 64, "width": [120, 230], "lean": [170, -22], "rise": 2, "rate": 0.5, "gust": 0.2, "color": "#c3cbd3", "opacity": 0.14, "plane": "back",
               "behind": [pl["house_outline"], pl["kiln_outline"]]})
    fx.append({"id": "mist-r", "type": "smoke", "what": "mist drifting down from behind the bank on the right (it passes behind the storehouse)",
               "at": [770, 398], "height": 60, "width": [110, 210], "lean": [-150, -26], "rise": 2, "rate": 0.5, "gust": 0.2, "color": "#c3cbd3", "opacity": 0.14, "plane": "back",
               "behind": [pl["house_outline"]]})
    stands = {name: {"at": p, "grownup_px": round(grownup_px(p[1]), 1)} for name, p in pts.items()}
    remap = []
    new_of = dict(pts)
    for name, old in OLD.items():
        if name in new_of:
            remap.append([old[0], old[1], new_of[name][0], new_of[name][1]])
    return {
        "id": ID, "horizon": HZ, "full": FULL,
        "camera": {"what": "HillCam (edo_cedars_kit.py): the walked ground is one plane climbing away from us; `horizon` is that plane's vanishing line and `full` its 160 px row, so the engine's sizes are true on it",
                   "focal": FOCAL, "slope": SLOPE, "pitch_deg": PITCH, "eye_cm": round(EYE, 1), "eye_level_row": round(TRUE_HZ, 1), "lens_row": round(CAM.P, 1),
                   "uprights_meet": [round(v, 1) for v in CAM.up]},
        "light": "dusk in fine spring rain under cedars: little light, all of it cool and soft, most from the pale gap up the hill on the left; no sun, only soft shade under things and the great cedar's shade across the foreground; the lamp under the floor and in the window the only warm things",
        "walk": pl["walk"],
        "walk_note": "the steps from the foot of the picture (bottom left) up to the yard, the yard before the storehouse's two walls, along to the pipe at the right, and a corner toward the kiln at the left (behind cedar-l); one plane, so sizes follow the scene's horizon and full exactly (stands give grownup_px)",
        "blocked": pl["blocked"], "blocked_note": "the flat stone before the door",
        "planes": planes, "things": things, "marks": M, "lift": pl["lift"], "sill": pl["sill"], "arrive": pl["arrive"], "stands": stands,
        "isukeWay": pl["way"], "isukeWay_note": "the constable's way up the path in #27, bottom first, ending at marks.door (edo-hills.js ISUKE_WAY)",
        "exits": [{"to": "edo-storehouse", "via": "door", "name": "the storehouse's door (once it is unbarred from inside)", "walkTo": M["door"], "spawn": "door"}],
        "cutouts": {name: box_of(a) for name, (c, a) in cut.items()},
        "fx": fx,
        "fx_note": "Nothing that moves by nature is painted: the rain, three drips off the thatch (each from the thatch's lower edge to the pebbles of the drip line), three puddles that ring (each clipped to its puddle), the mist drifting (two wide, slow, faint smokes on the back plane, passing behind the storehouse).",
        "puddles": [[round(v, 1) for v in p_] for p_ in puddles],
        "sizes": {name: round(grownup_px(p[1]), 1) for name, p in M.items()},
        "remap": {"points": remap, "note": "round twenty's marks, arriving places, standing places and the constable's way, and where each is in this picture: [old x, old y, new x, new y]"},
        "problems": bad,
    }


def scene_numbers(lay):
    """The scene file's numbers, as it writes them (to paste into js/content/scenes/edo-cedars.js)."""
    j = lambda v: json.dumps(v).replace(".0,", ",").replace(".0]", "]")
    M = lay["marks"]
    th = {t["id"]: t for t in lay["things"]}
    fx = {f["id"]: f for f in lay["fx"]}
    pl = {p["id"]: p for p in lay["planes"]}
    out = [f"horizon: {lay['horizon']}, full: {lay['full']}",
           f"const WALK = {j(lay['walk'])};",
           f"const BLOCKED = {j(lay['blocked'])};",
           "const M = { " + ", ".join(f"{k}: {j(v)}" for k, v in M.items()) + " };",
           f"const LIFT = {j(lay['lift'])};   const SILL = {j(lay['sill'])};   lil.base = {lay['lift'][1] - 1}",
           f"arrive: {{ enter: {j(lay['arrive']['enter'])}, door: {j(lay['arrive']['door'])} }}",
           f"cedar-l base: {j(pl['cedar-l']['base'])}   cedar-r base: {j(pl['cedar-r']['base'])}",
           f"rain behind: {j(fx['rain']['behind'])}", f"rain floor: {j(fx['rain']['floor'])}"]
    for i in (1, 2, 3):
        out.append(f"drip-{i}: path: {j(fx[f'drip-{i}']['path'])}, base: {fx[f'drip-{i}']['base']}")
    for i in (1, 2, 3):
        f = fx.get(f"puddle-{i}")
        if f:
            out.append(f"puddle-{i}: at: {j(f['at'])}, radius: {j(f['radius'])}, flat: {f['flat']}, clip: {j(f['clip'])}")
    for m in ("mist-l", "mist-r"):
        out.append(f"{m}: at: {j(fx[m]['at'])}, lean: {j(fx[m]['lean'])}, behind: {j(fx[m]['behind'])}")
    for t in lay["things"]:
        shape = t["shape"]
        out.append(f"{t['id']}: " + ("poly: " + j(shape["poly"]) if "poly" in shape else "rect: " + j(shape["rect"])) + f", walkTo: {j(t['stand'])}, face: \"{t['face']}\"")
    out.append(f"ISUKE_WAY = {j(lay['isukeWay'])}")
    return "\n".join(out)

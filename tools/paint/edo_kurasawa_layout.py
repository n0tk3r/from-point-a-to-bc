"""PAINT-23 (round twenty-three, RECOMPOSE): layout.json for edo-kurasawa, measured through the scene's new camera
(edo_kurasawa_view) from the places the picture was painted with, and from the finished cut-outs' pixels. Every number
of js/content/scenes/edo-kurasawa.js comes from here: `python3 edo_kurasawa_layout.py` prints them as the scene file
writes them (scene_numbers), checks every mark, arriving place and standing place against the walk outline and the
blocked patches, and writes out/edo-kurasawa-remap.json (where every old mark, arriving place and standing place of round
twenty-one's picture is now). edo_kurasawa.py calls layout(planes, info) at the end of a run."""

import json
import math
import os
import sys

import numpy as np

import edo_kurasawa_view as V
from edo_kurasawa_view import (HZ, FULL, P, k, G, U, NL, NR, TEA, GRILL, KUNI_AT, SIGN, BENCH, MOUND, HACK, KAGO, TRUNKS, ROAD_W,
                               road_mid, road_edge, road_lift, S_CLIMB, S_BEND, add, grownup_px, rnd, FUJI_AT)

HERE = os.path.dirname(os.path.abspath(__file__))

# Round twenty-one's places (the scene file before this round), for the remap: name -> (x, y)
OLD = {
    "yui": (16, 532), "teahouse": (96, 494), "kuni": (224, 471), "mound": (598, 434), "bearers": (446, 462), "peddler": (376, 486), "komuso": (668, 506),
    "courierFrom": (6, 516), "courierTo": (794, 508), "climb": (784, 466), "view": (300, 476), "tora": (470, 470),
    "arrive_mom": (40, 524), "arrive_bigsis": (26, 546), "arrive_lilsis": (58, 540),
    "fromTop.0": (760, 486), "fromTop.1": (742, 500), "atGrill.mom": (190, 500), "atGrill.bigsis": (252, 504), "atGrill.lilsis": (222, 494),
    "kagoSeat": (482, 440), "printWalk": (340, 500),
    "walkTo.smoke": (212, 500), "walkTo.signboard": (282, 492), "walkTo.road": (400, 540), "walkTo.kuni": (184, 485), "walkTo.grill": (212, 500),
    "walkTo.shells": (212, 500), "walkTo.sakuji": (406, 476), "walkTo.tora": (430, 484), "walkTo.soshichi": (336, 500), "walkTo.komuso": (628, 520),
    "walkTo.courier": (400, 540),
}


def r2(p):
    return [int(round(p[0])), int(round(p[1]))]


def box_of(alpha, pad=0):
    ys, xs = np.where(alpha > 0.5)
    if not len(ys):
        return None
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min() + 1) + 2 * pad, int(ys.max() - ys.min() + 1) + 2 * pad]


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


def face_to(frm, to):
    """The way someone standing at `frm` faces to look at `to` (picture points): E, W, N or S."""
    dx, dy = to[0] - frm[0], (to[1] - frm[1]) * 2.2                         # (a step up the picture is a long way back)
    if abs(dx) >= abs(dy):
        return "E" if dx > 0 else "W"
    return "N" if dy < 0 else "S"


def person_rect(at, cm=156.0, wide=0.36):
    x, y = at
    h = grownup_px(y) * cm / 175.0
    return [int(round(x - h * wide / 2)), int(round(y - h)), int(round(h * wide)), int(round(h))]


# ================================================================ the places (cm), and where they are in the picture
T = TEA


def tea(u, w):
    return r2(P(*T.xz(u, w)))


def places():
    """Every mark and standing place of the scene file, as picture points."""
    M = {}
    M["yui"] = [12, 592]                                                    # the left edge, on the road back to Yui (the way out)
    M["arrive_mom"] = r2(P(*add(road_mid(250), NR, 10)))                    # the three come in from Yui on the road at the bottom left
    M["arrive_bigsis"] = r2(P(*add(road_mid(185), NL, 110)))
    M["arrive_lilsis"] = r2(P(*add(road_mid(300), NR, 140)))
    M["teahouse"] = tea(190, -255)                                          # before O-Kuni's bench, a step out from the eave
    M["kuni"] = tea(KUNI_AT["u"], KUNI_AT["w"])                             # O-Kuni's place: behind her grill, before her door
    kc = (KAGO["X"], KAGO["Z"])
    M["bearers"] = r2(P(*add(add(kc, U, -150), NL, -60)))                   # Sakuji squatting by the palanquin's near end
    M["tora"] = r2(P(*add(add(kc, U, -40), NL, -112)))                      # Tora beside him, at the pole's middle
    M["mound"] = [728, 471]                                                 # before the distance mound, under the hackberry: at its foot right of the
                                                                            # trunks (in the picture: nothing stands in front of it there)
    tc = (TRUNKS["X"], TRUNKS["Z"])
    M["peddler"] = r2(P(*add(add(tc, U, 100), NR, 70)))                     # Soshichi beside his trunks, at their far side (clear of the palanquin)
    M["komuso"] = tea(T.L + 110, -230)                                      # the komuso, at the rest place past the teahouse, playing
    M["view"] = r2(P(*add(road_mid(S_BEND + 40), NL, 90)))                  # (mine) on the road, looking out at Fuji and the bay
    s_c = min(np.arange(S_CLIMB - 200, S_CLIMB + 400, 4.0), key=lambda s_: abs(P(*road_mid(s_))[0] - 772))
    M["climb"] = r2(P(*road_mid(s_c)))                                      # the right edge: the road starting up the hill to the pass
    M["courierFrom"] = r2(P(*road_mid(150)))                                # the courier's run, edge to edge along the road
    M["courierTo"] = r2(P(*road_mid(S_CLIMB + 300)))
    M["courierFrom"] = [4, M["courierFrom"][1]]
    M["courierTo"] = [796, M["courierTo"][1]]
    extra = {}
    extra["fromTop"] = [[706, 478], [668, 476]]                            # down from the top: beside the one played, on the road's far side
                                                                            # (clear of Soshichi, above the trunks' top, apart from each other)
    g = GRILL
    extra["atGrill"] = {"mom": [218, 506], "bigsis": tea(g["u"] + 86, g["w"] - 92), "lilsis": [298, 501]}   # (Mom at its near end, not
    #       in front of O-Kuni; Little Sister before its front, out of the margin the game keeps round it)
    extra["printWalk"] = [M["peddler"][0] - 36, M["peddler"][1] + 22]       # Little Sister comes to Soshichi for the print (before him, at his left)
    extra["kagoSeat"] = r2(P(*add(kc, NL, 6)))                              # the ground under her hips in the palanquin (behind its front)
    return M, extra


def walk_outline():
    """The walkable ground, one floor: the road and the trodden ground either side of it, short of the bench under the
    eave, the wall over the shore, the mound and the bank along the bottom; the climb's foot out to the right edge."""
    pts = [(0, 600), (0, P(*T.xz(118, -96))[1])]
    pts += [P(*T.xz(u, -96)) for u in (180.0, 300.0, 420.0, 500.0, 600.0, 690.0)]
    pts += [P(*T.xz(T.L + 60, -60)), P(-60, 1640), P(150, 1640)]
    m = MOUND
    for a in np.linspace(math.pi * 1.10, math.pi * 1.58, 6):                # round the mound's front, a little off its foot
        pts.append(P(m["X"] + (m["r"] + 50) * math.cos(a), m["Z"] + (m["r"] + 50) * 0.9 * math.sin(a)))
    pts += [(800, P(*road_edge(S_CLIMB + 300, -1, -40))[1])]
    pts += [(800, 556), (700, 566), (600, 574), (500, 582), (420, 588), (330, 594), (260, 600)]
    return [r2(p) for p in pts]


def blocked():
    """The grill (and the ground round it O-Kuni keeps), the signboard's foot, the trunks on their cloth, the palanquin."""
    out = []
    g = GRILL
    out.append([tea(g["u"] - g["len"] / 2 - 10, g["w"] - g["wid"] / 2 - 12), tea(g["u"] + g["len"] / 2 + 10, g["w"] - g["wid"] / 2 - 12),
                tea(g["u"] + g["len"] / 2 + 10, g["w"] + g["wid"] / 2 + 4), tea(g["u"] - g["len"] / 2 - 10, g["w"] + g["wid"] / 2 + 4)])
    out.append([tea(SIGN["u"] - 20, SIGN["w"] - 18), tea(SIGN["u"] + 20, SIGN["w"] - 18), tea(SIGN["u"] + 20, SIGN["w"] + 16), tea(SIGN["u"] - 20, SIGN["w"] + 16)])
    tc = (TRUNKS["X"], TRUNKS["Z"])
    w2, d2 = TRUNKS["w"] / 2, TRUNKS["d"] / 2
    out.append([r2(P(*add(add(tc, U, a), NL, b))) for a, b in ((-w2 - 18, -d2 - 8), (w2 + 20, -d2 - 8), (w2 + 16, d2 + 10), (-w2 - 14, d2 + 8))])   # (the mat under them)
    kc = (KAGO["X"], KAGO["Z"])
    L2, W2 = KAGO["pole"] / 2, KAGO["width"] / 2
    out.append([r2(P(*add(add(kc, U, a), NL, b))) for a, b in ((-L2 + 40, -W2 - 10), (L2 - 30, -W2 - 10), (L2 - 30, -14), (-L2 + 40, -14))])   # (its near half: the seat behind it stays free)
    return out


# ================================================================ the scene's things, areas, effects
def things(planes, info, M, extra):
    th = []
    add_t = lambda id_, shape, stand, face, what: th.append({"id": id_, "shape": shape, "stand": stand, "face": face, "what": what})
    view = M["view"]
    # far things
    sx, sy = FUJI_AT
    add_t("fuji", {"rect": [int(sx - 130), int(sy - 10), 340, int(HZ - sy + 8)]}, view, "N", "Mount Fuji across the bay, white well down its flanks (as at Yui)")
    co = info.get("cloud_outline")
    add_t("cloud", {"poly": [r2(p) for p in co[::3]][:16]} if co else {"rect": [240, 100, 180, 50]}, view, "N", "the cap of cloud on Fuji's top (a cut-out: on / off)")
    add_t("bay", {"poly": BAY}, view, "N", "Suruga Bay, morning, beyond the wall over the shore")
    add_t("yuishore", {"poly": [[292, 328], [440, 330], [452, 345], [292, 345]]}, view, "N", "the far shore curving back toward Yui, a thread of sand, Yui's roofs on it")
    add_t("boats", {"rect": [330, 330, 180, 62]}, view, "N", "fishing boats on the bay, far out and nearer")
    add_t("hackberry", {"poly": HACK_POLY}, M["mound"], "N", "the hackberry on the mound, planted for the travellers' shade, in new leaf; its bough comes out over the road")
    add_t("cliffroad", {"poly": CLIFF_POLY}, M["climb"], "E", "the road to the pass: up the hill from the bend, and cut across Mount Satta's face")
    add_t("teahouse", {"poly": TEA_POLY}, M["teahouse"], "N", "O-Kuni's teahouse: thatched, its front open under a deep eave, the matted room open behind on the bay")
    g = GRILL
    gm_ = tea(g["u"], g["w"])
    add_t("smoke", {"rect": [gm_[0] - 28, gm_[1] - 92, 56, 64]}, extra["atGrill"]["lilsis"], "N", "smoke from the grill (the engine's: fx grill-smoke)")
    sb = info.get("sign_box")
    srect = [int(round(min(p[0] for p in sb))) - 3, int(round(min(p[1] for p in sb))) - 3, int(round(abs(sb[1][0] - sb[0][0]))) + 6, int(round(abs(sb[1][1] - sb[0][1]))) + 6] if sb else [340, 380, 24, 92]
    add_t("signboard", {"rect": srect}, tea(SIGN["u"] - 40, SIGN["w"] - 90), "N", "the signboard at the teahouse's far corner: a turban shell painted on it, a column of brush marks (our own: no shop's name)")
    m = MOUND
    mb = [P(m["X"] - m["r"], m["Z"]), P(m["X"] + m["r"], m["Z"]), P(m["X"], m["Z"], m["h"] + 10), P(m["X"], m["Z"] - m["r"])]
    add_t("mound", {"rect": [int(min(p[0] for p in mb)), int(min(p[1] for p in mb)), int(min(800, max(p[0] for p in mb)) - min(p[0] for p in mb)), int(max(p[1] for p in mb) - min(p[1] for p in mb)) + 2]},
          M["mound"], "N", "the 40th distance mound from Edo: a grassed mound by the road")
    add_t("palanquin", {"rect": box_of(planes["kago"][1], 2)}, [560, 501], "N", "the bearers' palanquin, set down: an open bamboo kago on one long pole (a cut-out)")
    tc = (TRUNKS["X"], TRUNKS["Z"])
    t_at = r2(P(*add(add(tc, U, -110), NR, 15)))                            # before the trunks' near corner (Soshichi stands at their road side)
    add_t("trunks", {"rect": box_of(planes["trunks"][1], 2)}, t_at, face_to(t_at, r2(P(*tc, 50))), "Soshichi's willow trunks, five tiers, the top one open with the ledger on it (a cut-out)")
    bp = info.get("bench_pts")
    brect = [max(0, int(min(p[0] for p in bp)) - 3), int(min(p[1] for p in bp)) - 6, int(max(p[0] for p in bp) - max(0, min(p[0] for p in bp))) + 6, int(max(p[1] for p in bp) - min(p[1] for p in bp)) + 10]
    add_t("bench", {"rect": brect}, M["teahouse"], "N", "the bench under the eaves, a tea tray on it")
    add_t("road", {"poly": ROAD_POLY}, r2(P(*road_mid(560))), "E", "the Tokaido: packed earth, from Yui (left) round the bend to the climb (right)")
    # the people (the game draws them; their areas go with them)
    side = lambda at, dx, dy: [at[0] + dx, at[1] + dy]                      # a standing place beside someone, in the picture
    people = [("kuni", M["kuni"], 146.0, side(M["kuni"], -48, 18), "O-Kuni at her grill"), ("grill", None, 0, extra["atGrill"]["lilsis"], "the grill"),
              ("sakuji", M["bearers"], 150.0, side(M["bearers"], -54, 12), "Sakuji, squatting by the palanquin"),
              ("tora", M["tora"], 172.0, side(M["tora"], -30, 22), "Tora, beside him"),      # (talked to from between the two: behind him stand the trunks)
              ("soshichi", M["peddler"], 156.0, side(M["peddler"], -64, 24), "Soshichi by his trunks"),
              ("komuso", M["komuso"], 160.0, side(M["komuso"], -56, 10), "the komuso under his basket hat, playing"),
              ("courier", [400, 520], 156.0, r2(P(*road_mid(560))), "the relay courier (fx courier)")]
    return th, people


# outlines drawn round what the picture shows (set by layout() from the finished pictures)
BAY = TEA_POLY = HACK_POLY = CLIFF_POLY = ROAD_POLY = None


def compute_polys(planes, info):
    global BAY, TEA_POLY, HACK_POLY, CLIFF_POLY, ROAD_POLY
    # the bay as seen: from the teahouse's far eave to Satta's seaward foot, down to the wall
    wall = [P(X, Z, 52) for X, Z in V.WALL]
    wy = lambda x: float(np.interp(x, [p[0] for p in wall], [p[1] for p in wall]))
    BAY = [[300, HZ + 1], [440, HZ + 1], [522, HZ + 2], [536, 372], [552, 404], [554, int(wy(554))], [500, int(wy(500))], [440, int(wy(440))], [380, int(wy(380))],
           [330, int(wy(330))], [300, int(wy(300))]]
    BAY = [[int(round(a)), int(round(b))] for a, b in BAY]
    # the teahouse: its roof and front, to the left edge (the picture's own: info)
    roof = info["tea_roof"]
    front = info["tea_front"]
    TEA_POLY = [[0, int(round(min(p[1] for p in roof[:2]) - 30))]] + [r2(p) for p in roof[1:4]] + [r2(roof[4]), r2(front[1]), [int(round(front[1][0])) - 30, int(round(front[1][1])) + 22], [0, int(round(P(*T.xz(118, -96))[1]))]]
    # the hackberry: its trunk on the mound and its crown under the top of the frame
    near_a = planes["near"][1]
    crown = (near_a > 0.5)
    crown[:, :400] = False
    crown[440:, :] = False
    ys, xs = np.where(crown)
    x0 = int(xs.min())
    fork = info["fork"]
    tr = info["trunk_shape"]
    tx0, tx1 = int(min(p[0] for p in tr)), int(max(p[0] for p in tr))
    ty1 = int(max(p[1] for p in tr))
    low = lambda xa, xb: int(max(ys[(xs >= xa) & (xs < xb)])) if np.any((xs >= xa) & (xs < xb)) else 0
    HACK_POLY = [[x0, 0], [800, 0], [800, low(760, 800)], [tx1 + 14, low(tx1, tx1 + 40)], [tx1, ty1 - 4], [tx0, ty1 - 4], [tx0 - 14, low(tx0 - 40, tx0)],
                 [x0 + 60, low(x0 + 40, x0 + 80)], [x0, low(x0, x0 + 20)]]
    # the cliff road: the climb at the right edge and its line across Satta's face
    CLIFF_POLY = [[584, 314], [700, 276], [800, 246], [800, 262], [700, 292], [596, 326]]
    clb = [r2(road_pt) for road_pt in (P(*road_edge(S_CLIMB + 40, -1)), P(*road_edge(S_CLIMB + 340, -1)), P(*road_edge(S_CLIMB + 340, 1)), P(*road_edge(S_CLIMB + 40, 1)))]
    CLIFF_POLY = CLIFF_POLY
    info["climb_poly"] = clb
    # the road: short of the edges' bands (left: back to Yui; right: up to the pass) and of the bottom's
    left = [r2(P(*road_edge(s, -1))) for s in np.linspace(200, S_CLIMB + 260, 12)]
    right = [r2(P(*road_edge(s, 1))) for s in np.linspace(S_CLIMB + 260, 340, 12)]
    ROAD_POLY = [[46, left[0][1] + 18]] + [p for p in left if 46 <= p[0] <= 754] + [[754, left[-1][1]], [754, 540]] + [p for p in right if 46 <= p[0] <= 754 and p[1] <= 560] + [[46, 560]]


def fx_list(info, M, extra):
    g = GRILL
    top = r2(P(*T.xz(g["u"], g["w"]), g["h"] + 4))
    base = int(round(P(*T.xz(g["u"], g["w"] - g["wid"] / 2))[1]))
    kz = k(T.xz(g["u"], g["w"])[1])
    path = [[-40, M["courierFrom"][1] + 14], M["courierFrom"]] + [r2(P(*road_mid(s))) for s in (230, 330, 450, 560, 680, 800, 920, 1040, 1160)] + [M["courierTo"], [840, M["courierTo"][1]]]
    path = [p for i, p in enumerate(path) if i == 0 or i == len(path) - 1 or 0 <= p[0] <= 800]
    roof = [r2(p) for p in info["tea_roof"]]
    gull_behind = [TEA_POLY, HACK_POLY]
    return [
        {"id": "grill-smoke", "type": "smoke", "at": top, "base": base, "height": 76, "width": [4, 24], "lean": [34, -76], "rise": 12, "rate": 3, "gust": 0.35,
         "color": "#e4e6ea", "opacity": 0.34, "what": "smoke off the turban shells on O-Kuni's grill, leaning inland with the wind off the bay, toward the mountain"},
        {"id": "grill-embers", "type": "embers", "at": top, "size": [int(round(g["len"] * kz * 0.75)), 5], "base": base, "glowOpacity": 0.10, "sparks": 0.08,
         "what": "the charcoal under the shells, glowing a little in the daylight"},
        {"id": "bay-waves", "type": "waves", "area": BAY, "rows": 8, "per": 8, "size": 4, "speed": 3, "toward": "S", "color": "#f4f8fb", "opacity": 0.36, "plane": "back"},
        {"id": "bay-shimmer", "type": "shimmer", "poly": BAY, "count": 20, "size": 4, "flow": [3, 0], "life": 1.8, "color": "#f6eed8", "opacity": 0.45, "plane": "back"},
        {"id": "noren-sway", "type": "sway", "plane": "noren", "anchor": "top", "amount": 2.0, "period": 3.4, "wave": 22, "lean": 0.35},
        {"id": "cloud-drift", "type": "bob", "plane": "cloud", "amount": 1, "period": 11},
        {"id": "gulls", "type": "birds", "plane": "back", "lanes": [[[-12, 150], [180, 190], [330, 250], [440, 236], [470, -12]], [[480, -12], [440, 230], [340, 270], [200, 200], [-12, 170]]],
         "every": [8, 16], "group": [1, 2], "speed": 50, "size": 7, "scale": [0.6, 1.0], "color": "#f6eed8", "behind": gull_behind,
         "note": "over the bay between the teahouse and the hackberry; behind the teahouse's roof and the hackberry's crown"},
        {"id": "courier", "type": "passer", "kind": "courier", "path": path, "every": [18, 34], "both": True, "area": "courier",
         "note": "along the road's middle, from the bottom left corner (from Yui) round the bend to the climb at the right edge, both ways; sorted by his feet with the cut-outs: in front of the grill, the palanquin and the sign, behind Soshichi's trunks on the verge, behind the near plane"},
    ]


def layout(planes, info):
    compute_polys(planes, info)
    M, extra = places()
    walk = walk_outline()
    bl = blocked()
    th, people = things(planes, info, M, extra)
    for pid, at, cm, stand, what in people:
        if at is None:
            gx = info["grill_box"] if "grill_box" in info else box_of(planes["grill"][1], 2)
            th.append({"id": pid, "shape": {"rect": gx}, "stand": stand, "face": "N", "what": what})
            continue
        th.append({"id": pid, "shape": {"rect": person_rect(at, cm)}, "stand": stand, "face": face_to(stand, at) if pid != "courier" else "S", "what": what + " (drawn by the game)"})
    shells = info.get("shells", [])
    th.append({"id": "shells", "shape": {"rect": [int(min(p[0] for p in shells)) - 6, int(min(p[1] for p in shells)) - 12, int(max(p[0] for p in shells) - min(p[0] for p in shells)) + 12, 16]} if shells else {"rect": [250, 470, 50, 14]},
               "stand": extra["atGrill"]["lilsis"], "face": "N", "what": "turban shells grilling in their own shells on the coals, mouth up"})
    base_of = lambda key: [r2(p) for p in info[key]]
    planes_out = [
        {"id": "cloud", "file": "cloud.png", "plane": "back", "what": "the cap of cloud on Fuji's top (on until it lifts at the top of the pass: edo.fujiClear); the backdrop under it is the clear summit"},
        {"id": "kago", "file": "kago.png", "base": base_of("kago_base"), "what": "the bearers' palanquin set down at the mound's foot (empty); Little Sister sits in it behind its front"},
        {"id": "noren", "file": "noren.png", "base": base_of("noren_base"), "what": "the noren in the teahouse's door (it stirs: fx noren-sway)"},
        {"id": "trunks", "file": "trunks.png", "base": base_of("trunks_base"), "what": "Soshichi's willow trunks on the inland verge; the courier passes behind them"},
        {"id": "grill", "file": "grill.png", "base": base_of("grill_base"), "what": "O-Kuni's grill with the turban shells; she stands behind it"},
        {"id": "front", "file": "front.png", "plane": "front", "what": "the roadside's bank along the bottom: the inland verge's lip, sasa, pampas blades, a stone"},
        {"id": "near", "file": "near.png", "plane": "front", "what": "the hackberry's crown and its bough over the top right corner; the near end of O-Kuni's eave and its reed blind at the top left"},
    ]
    stands = {}
    pts = dict(M)
    for i, q in enumerate(extra["fromTop"]):
        pts[f"fromTop.{i}"] = q
    for k_, q in extra["atGrill"].items():
        pts[f"atGrill.{k_}"] = q
    pts["printWalk"] = extra["printWalk"]
    for t in th:
        pts["walkTo." + t["id"]] = t["stand"]
    bad = []
    # the engine keeps a figure's feet 12 px sideways and 5 px up or down off every blocked outline and off the patch each
    # of the scene's people stands on (walk.js WalkMap, game.js ground): a place in that margin cannot be stood on
    def spans(poly, row):
        xs = []
        for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
            if (y0 <= row < y1) or (y1 <= row < y0):
                xs.append(x0 + (row - y0) * (x1 - x0) / (y1 - y0))
        xs.sort()
        return list(zip(xs[0::2], xs[1::2]))

    def kept_off(p_, polys):
        for poly in polys:
            for row in range(int(p_[1]) - 5, int(p_[1]) + 6):
                if any(a - 12 <= p_[0] <= b + 12 for a, b in spans(poly, row + 0.5)):
                    return True
        return False
    people_at = [M[n] for n in ("kuni", "bearers", "tora", "peddler", "komuso")]
    patches = [[[x_ - 32 * sc, y_ - 12], [x_ + 32 * sc, y_ - 12], [x_ + 32 * sc, y_ + 8], [x_ - 32 * sc, y_ + 8]]
               for x_, y_ in people_at for sc in [min(1.12, max(0.26, (y_ - HZ) / (FULL - HZ)))]]
    for name, p in pts.items():
        if name in ("yui", "courierFrom", "courierTo"):
            continue
        if not inside(walk, p):
            bad.append(f"{name} {p} is outside the walk outline")
        if any(inside(b, p) for b in bl):
            bad.append(f"{name} {p} is on a blocked patch")
        elif name not in ("kuni", "bearers", "tora", "peddler", "komuso") and kept_off(p, bl + patches):
            bad.append(f"{name} {p} is in the margin the game keeps round a blocked patch or one of the people")
    for name, p in pts.items():
        stands[name] = {"at": p, "grownup_px": round(grownup_px(p[1]), 1)}
    remap = []
    for name, old in OLD.items():
        if name in pts:
            remap.append([old[0], old[1], pts[name][0], pts[name][1]])
    remap.append([OLD["kagoSeat"][0], OLD["kagoSeat"][1], extra["kagoSeat"][0], extra["kagoSeat"][1]])
    cut_boxes = {pl["id"]: box_of(planes[pl["id"]][1]) for pl in planes_out}
    return {
        "id": "edo-kurasawa", "horizon": HZ, "full": FULL,
        "view": {"horizon": HZ, "full": FULL, "camera": f"persp.Camera({HZ}, {FULL}, focal {V.FOCAL:.0f}): the eye {V.EYE:.0f} cm above the road; the road and the teahouse turned {math.degrees(V.THETA):.0f} degrees (edo_kurasawa_view.py)",
                 "compass": "the act's (as Yui's): looking west along the Tokaido toward the pass; the bay on the left with Fuji across it; the left edge (bottom) the road back to Yui, the right edge the climb to the pass"},
        "light": "morning: the act's sun in the east, low along the road from Yui behind us and to the left, about 40 degrees up; the teahouse's front in shade, its near end lit; shadows to the right and away; a shore pine behind us on the left lays its shadow across the road at the bottom left",
        "walk": walk, "walk_note": "one floor: the road from the bottom left round the bend to the climb's foot at the right edge, the trodden ground before the teahouse (short of the bench under the eave, O-Kuni's place behind the grill kept), the rest place past it short of the wall, the ground before the mound, the inland verge above the bank",
        "blocked": bl, "planes": planes_out, "cutouts": cut_boxes, "things": th, "marks": M,
        "fromTop": extra["fromTop"], "atGrill": extra["atGrill"], "kagoSeat": extra["kagoSeat"], "printWalk": extra["printWalk"],
        "stands": stands, "fx": fx_list(info, M, extra),
        "exits": [{"to": "edo-village", "edge": "left", "at": M["yui"], "what": "the road back east to Yui"},
                  {"to": "edo-satta", "edge": "right", "at": M["climb"], "what": "up the road to the top of the pass"}],
        "sizes": {name: round(grownup_px(p[1]), 1) for name, p in M.items()},
        "remap": {"points": remap, "note": "round twenty-one's marks, arriving places and standing places, and where each is in this picture: [old x, old y, new x, new y]"},
        "polys": {"teahouse": TEA_POLY, "bay": BAY, "hackberry": HACK_POLY, "cliffroad": CLIFF_POLY, "road": ROAD_POLY},
        "problems": bad,
    }


def scene_numbers(lay):
    """The scene file's numbers, as it writes them (to paste into js/content/scenes/edo-kurasawa.js)."""
    j = lambda v_: json.dumps(v_).replace(", ", ", ")
    M = lay["marks"]
    th = {t["id"]: t for t in lay["things"]}
    fx = {f["id"]: f for f in lay["fx"]}
    pl = {p["id"]: p for p in lay["planes"]}
    out = [f"horizon: {lay['horizon']}, full: {lay['full']}",
           "const M = {\n  " + ", ".join(f"{k_}: {j(v_)}" for k_, v_ in M.items()) + ",\n};",
           f"const FROM_TOP = {j(lay['fromTop'])};",
           f"const AT_GRILL = {{ mom: {j(lay['atGrill']['mom'])}, bigsis: {j(lay['atGrill']['bigsis'])}, lilsis: {j(lay['atGrill']['lilsis'])} }};",
           f"const KAGO_SEAT = {j(lay['kagoSeat'])};",
           f"print walk: {j(lay['printWalk'])}",
           f"walk: {{ area: {j(lay['walk'])} }}",
           f"blocked: {j(lay['blocked'])}"]
    for pid in ("kago", "noren", "trunks", "grill"):
        out.append(f"plane {pid} base: {j(pl[pid]['base'])}")
    out.append(f"TEAHOUSE = {j(lay['polys']['teahouse'])}")
    out.append(f"BAY = {j(lay['polys']['bay'])}")
    out.append(f"HACKBERRY = {j(lay['polys']['hackberry'])}")
    for f_ in lay["fx"]:
        out.append(f"fx {f_['id']}: " + j({k_: v_ for k_, v_ in f_.items() if k_ not in ('what', 'note', 'id', 'type')}))
    for t in lay["things"]:
        shape = t["shape"]
        out.append(f"{t['id']}: " + ("poly: " + j(shape["poly"]) if "poly" in shape else "rect: " + j(shape["rect"])) + f", walkTo: {j(t['stand'])}, face: \"{t['face']}\"")
    return "\n".join(out)


if __name__ == "__main__":
    lay = json.load(open(os.path.join(HERE, "out", "edo-kurasawa", "layout.json")))
    for b in lay.get("problems", []):
        print("LAYOUT:", b)
    print(scene_numbers(lay))
    with open(os.path.join(HERE, "out", "edo-kurasawa-remap.json"), "w") as f:
        json.dump({"points": lay["remap"]["points"]}, f, indent=1)
    print("sizes:", lay["sizes"])

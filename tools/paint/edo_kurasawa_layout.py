"""PAINT-21A: layout.json for edo-kurasawa, measured through the scene's camera from the same numbers the picture was
painted with (edo_kurasawa.py's placings), and from the finished cut-outs' pixels."""

import math

import numpy as np

import edo_kurasawa as K
from edo_kurasawa import HZ, FULL, V, gp, kz, ROAD, TEA, BENCH, MOUND, KAGO, TRUNKS, GRILL, SIGN, FUJI, COAST, ledge_z


def r(p):
    return [int(round(p[0])), int(round(p[1]))]


def box_of(alpha, pad=0):
    ys, xs = np.where(alpha > 0.5)
    if len(ys) == 0:
        return [0, 0, 0, 0]
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 1 + 2 * pad, int(ys.max() - ys.min()) + 1 + 2 * pad]


def px(y, cm=175.0):
    """The size in pixels of someone `cm` tall with their feet on row y (the scene's straight-line rule)."""
    return 160.0 * (y - HZ) / (FULL - HZ) * cm / 175.0


def stand(p, face="N"):
    x, y = p
    return {"at": [int(round(x)), int(round(y))], "grownup_px": int(round(px(y))), "face": face}


def person_rect(p, cm):
    h = px(p[1], cm)
    return [int(round(p[0] - h * 0.17)), int(round(p[1] - h)), int(round(h * 0.34)), int(round(h))]


def rect_pts(pts, pad=2):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return [int(min(xs)) - pad, int(min(ys)) - pad, int(max(xs) - min(xs)) + 2 * pad, int(max(ys) - min(ys)) + 2 * pad]


def layout(planes, info):
    # ---- marks (ROUND-21's names, and mine), picture points on the ground
    M = {
        "yui": [16, 532],                                                    # the left edge: from Yui and back (the road east)
        "teahouse": [96, 494],                                               # before O-Kuni's bench, a step back from the eaves
        "kuni": r(gp(-325, 606)),                                            # O-Kuni's place: behind her grill, before her door
        "mound": [598, 434],                                                 # by the distance mound, under the hackberry
        "bearers": [446, 462],                                               # Sakuji and Tora, by their palanquin's near end
        "peddler": [376, 486],                                               # Soshichi by his trunks
        "komuso": [668, 506],                                                # the komuso, on the road at the climb's foot, playing
        "courierFrom": [6, 516], "courierTo": [794, 508],                    # the courier's run, edge to edge along the road
        "climb": [784, 466],                                                 # the right edge: on the ramp, the road up the cliff to the pass
        "view": [300, 476],                                                  # (mine) at the road's far edge, looking out at Fuji and the bay
        "tora": [470, 470],                                                  # (mine) the second bearer, beside Sakuji
        "arrive_mom": [40, 524], "arrive_bigsis": [26, 546], "arrive_lilsis": [58, 540],   # (mine) the three, come in from Yui
    }
    faces = {"yui": "E", "teahouse": "N", "kuni": "S", "mound": "N", "bearers": "S", "peddler": "S", "komuso": "W", "courierFrom": "E",
             "courierTo": "W", "climb": "W", "view": "N", "tora": "S", "arrive_mom": "E", "arrive_bigsis": "E", "arrive_lilsis": "E"}
    stands = {k: stand(v, faces[k]) for k, v in M.items()}
    stands["climb"]["note"] = "the road turns up the mountain's foot at the right edge: the way west to the pass (edo-satta)"
    stands["yui"]["note"] = "the left edge: the road back east to Yui (edo-village, its west end)"
    # ---- the walk: the road and the ground before the teahouse, the ledge's strip before the wall, the rest place
    # before the mound, the climb's foot; one area (the climb is the way out, not walked up here)
    walk = [[0, 476], [178, 476], [184, 470], [212, 468], [262, 468], [276, 474], [300, 466], [336, 462], [392, 452], [430, 444], [470, 436],
            [520, 428], [560, 426], [580, 428], [632, 436], [652, 458], [672, 478], [700, 482], [740, 472], [780, 458], [800, 452], [800, 596], [0, 596]]
    blocked = []
    # the grill (and O-Kuni's bucket), the signboard's foot, the trunks on their cloth, the palanquin, the mound
    g = GRILL
    blocked.append([r(gp(g["x"] - g["w"] / 2 - 26, g["z"] - g["d"] / 2 - 6)), r(gp(g["x"] + g["w"] / 2 + 6, g["z"] - g["d"] / 2 - 6)),
                    r(gp(g["x"] + g["w"] / 2 + 6, g["z"] + g["d"] / 2 + 2)), r(gp(g["x"] - g["w"] / 2 - 26, g["z"] + g["d"] / 2 + 2))])
    blocked.append([r(gp(SIGN["x"] - 18, SIGN["z"] - 14)), r(gp(SIGN["x"] + 18, SIGN["z"] - 14)), r(gp(SIGN["x"] + 18, SIGN["z"] + 10)), r(gp(SIGN["x"] - 18, SIGN["z"] + 10))])
    t = TRUNKS
    blocked.append([r(gp(t["x"] - t["w"] / 2 - 22, t["z"] - t["d"] / 2 - 14)), r(gp(t["x"] + t["w"] / 2 + 26, t["z"] - t["d"] / 2 - 10)),
                    r(gp(t["x"] + t["w"] / 2 + 20, t["z"] + t["d"] / 2 + 14)), r(gp(t["x"] - t["w"] / 2 - 18, t["z"] + t["d"] / 2 + 10))])
    k_ = KAGO
    blocked.append([r(gp(k_["x"] - k_["length"] / 2 - 8, k_["z"] - k_["width"] / 2 - 8)), r(gp(k_["x"] + k_["length"] / 2 + 8, k_["z"] - k_["width"] / 2 - 8)),
                    r(gp(k_["x"] + k_["length"] / 2 + 8, k_["z"] + k_["width"] / 2 + 8)), r(gp(k_["x"] - k_["length"] / 2 - 8, k_["z"] + k_["width"] / 2 + 8))])
    mx, mz, mr = MOUND["x"], MOUND["z"], MOUND["r"]
    blocked.append([r(gp(mx + (mr + 20) * math.cos(a), mz + (mr + 20) * math.sin(a))) for a in np.linspace(0, 2 * math.pi, 14)[:-1]])
    # ---- the cut-outs, back to front, with their bases and states
    planes_out = [
        {"id": "cloud", "file": "cloud.png", "plane": "back", "state": "on (Fuji's cap of cloud) / off: hidden once edo.noRoad's cloud has lifted at the top of the pass (the same cloud: a player who has seen it lift sees it gone here too)",
         "what": "the cap of cloud on Fuji's top; the backdrop under it is the clear summit"},
        {"id": "kago", "file": "kago.png", "base": r(gp(KAGO["x"], KAGO["z"] - KAGO["width"] / 2))[1], "what": "the bearers' palanquin set down by the mound (empty); whoever stands by the mound is behind it"},
        {"id": "noren", "file": "noren.png", "base": r(gp(TEA["door"][0], TEA["z0"]))[1], "what": "the noren over the teahouse's door (it stirs: fx noren-sway); whoever goes in at the door passes behind it"},
        {"id": "trunks", "file": "trunks.png", "base": r(gp(TRUNKS["x"], TRUNKS["z"] - TRUNKS["d"] / 2))[1], "what": "Soshichi's willow trunks set down at the road's edge (show them while he stands at `peddler`; his sprite carries them on the road)"},
        {"id": "grill", "file": "grill.png", "base": r(gp(GRILL["x"], GRILL["z"] - GRILL["d"] / 2))[1], "what": "O-Kuni's grill with the turban shells; she stands behind it (at `kuni`)"},
        {"id": "front", "file": "front.png", "plane": "front", "what": "the near verge at the bottom edge: grass, two stones and a worn-out straw sandal"},
    ]
    cutouts = {p["id"]: box_of(planes[p["id"]][1]) for p in planes_out}
    # ---- things (ROUND-21's list, each with a shape), and the stand a look or a use walks the lead to
    tea_roof = info["tea_roof"]
    bench_pts = [gp(BENCH["x0"], BENCH["z0"], 0), gp(BENCH["x1"], BENCH["z0"], 0), gp(BENCH["x1"], BENCH["z1"], BENCH["h"]), gp(BENCH["x0"], BENCH["z1"], BENCH["h"])]
    sign_pts = [gp(SIGN["x"] - SIGN["w"] / 2, SIGN["z"], 0), gp(SIGN["x"] + SIGN["w"] / 2, SIGN["z"], SIGN["h"] + 6)]
    shells = info.get("shells", [])
    cloud_outline = info.get("cloud_outline", [])
    bay_poly = [[300, 302], [520, 304], [510, 372], [546, 410], [552, 428]] + [r(gp(x_, ledge_z(x_))) for x_ in np.linspace(300, -260, 8)] + [[300, 360]]
    things = [
        {"id": "fuji", "what": "Mount Fuji across the head of the bay, white well down its flanks (its cap of cloud: `cloud`)", "shape": {"rect": [150, 64, 300, 238]}, "stand": M["view"], "face": "N"},
        {"id": "cloud", "what": "the cap of cloud on Fuji's top (a cut-out: on / off)", "shape": {"poly": [r(p) for p in cloud_outline[::3]]} if cloud_outline else {"rect": [180, 60, 190, 50]}, "stand": M["view"], "face": "N"},
        {"id": "bay", "what": "Suruga Bay, morning", "shape": {"poly": bay_poly}, "stand": M["view"], "face": "N"},
        {"id": "yuishore", "what": "the shore curving back east toward Yui (the way they came): a thread of sand, low hills, Yui's roofs", "shape": {"poly": [[270, 286], [460, 297], [460, 310], [360, 316], [300, 324], [270, 336]]}, "stand": M["view"], "face": "N"},
        {"id": "boats", "what": "fishing boats far out on the bay", "shape": {"rect": [338, 306, 160, 50]}, "stand": M["view"], "face": "N"},
        {"id": "teahouse", "what": "O-Kuni's teahouse: a thatched roof, its front open to the road, the matted room behind with the bay through its back", "shape": {"poly": [r(p) for p in tea_roof[:4]] + [[0, 470]]}, "stand": M["teahouse"], "face": "N"},
        {"id": "bench", "what": "the bench under the eaves, a tea tray on it", "shape": {"rect": rect_pts(bench_pts, 3)}, "stand": M["teahouse"], "face": "N"},
        {"id": "grill", "what": "the grill: a clay firebox of charcoal before the door (a cut-out)", "shape": {"rect": box_of(planes["grill"][1], 2)}, "stand": [212, 500], "face": "N"},
        {"id": "shells", "what": "turban shells grilling in their own shells on the coals, mouth up", "shape": {"rect": rect_pts(shells, 5) if shells else [190, 444, 60, 16]}, "stand": [212, 500], "face": "N"},
        {"id": "signboard", "what": "the signboard at the teahouse's corner: a turban shell painted on it, a column of brush marks under it (our own: no shop's name)", "shape": {"rect": rect_pts(sign_pts, 3)}, "stand": [282, 492], "face": "N"},
        {"id": "mound", "what": "the 40th distance mound from Edo: a grassed mound by the road", "shape": {"rect": info["tree"]["mound"]}, "stand": M["mound"], "face": "N"},
        {"id": "hackberry", "what": "the hackberry on the mound, planted for the travellers' shade, in new leaf", "shape": {"rect": info["tree"]["crown"]}, "stand": M["mound"], "face": "N"},
        {"id": "palanquin", "what": "the bearers' palanquin, set down: an open-sided bamboo kago on one long pole (a cut-out)", "shape": {"rect": box_of(planes["kago"][1], 2)}, "stand": M["bearers"], "face": "N"},
        {"id": "trunks", "what": "Soshichi's willow trunks, five tiers, set down and opened (a cut-out)", "shape": {"rect": box_of(planes["trunks"][1], 2)}, "stand": M["peddler"], "face": "N"},
        {"id": "road", "what": "the Tokaido: packed earth, from Yui (left) to the climb (right)", "shape": {"poly": [r(gp(-900, ROAD["z0"])), r(gp(900, ROAD["z0"])), [800, 478], [0, 478]]}, "stand": [400, 540], "face": "S"},
        {"id": "cliffroad", "what": "the road west cut across Mount Satta's face, climbing round to the right (the way to the pass)", "shape": {"poly": [[640, 262], [700, 252], [800, 226], [800, 412], [700, 410], [690, 380]]}, "stand": M["climb"], "face": "E"},
        {"id": "smoke", "what": "smoke from the grill (the engine's: fx grill-smoke)", "shape": {"rect": [196, 380, 50, 64]}, "stand": [212, 500], "face": "N"},
    ]
    people = [("kuni", M["kuni"], 146, "O-Kuni at her grill"), ("sakuji", M["bearers"], 156, "Sakuji, squatting on the palanquin's pole end"),
              ("tora", M["tora"], 156, "Tora, huge and gentle, beside him"), ("soshichi", M["peddler"], 156, "Soshichi the medicine peddler by his trunks"),
              ("komuso", M["komuso"], 156, "the komuso under his basket hat, playing"), ("courier", [400, 512], 156, "the relay courier running through (fx courier)")]
    for pid, at, cm, what in people:
        things.append({"id": pid, "what": what + " (drawn by the game)", "shape": {"rect": person_rect(at, cm)}, "stand": [at[0] - 40, at[1] + 14] if pid != "courier" else [400, 540], "face": "E"})
    # ---- fx: what moves (the engine draws it)
    gx, gz = GRILL["x"], GRILL["z"]
    grill_mid = r(gp(gx, gz, GRILL["h"] + 4))
    fx = [
        {"id": "grill-smoke", "type": "smoke", "what": "smoke off the turban shells on O-Kuni's grill, leaning away up the road with the wind off the bay",
         "at": grill_mid, "base": r(gp(gx, gz - GRILL["d"] / 2))[1], "height": 70, "width": [4, 22], "lean": [26, -70], "rise": 12, "rate": 3,
         "gust": 0.35, "color": "#e4e6ea", "opacity": 0.34},
        {"id": "grill-embers", "type": "embers", "what": "the charcoal under the shells, glowing a little in the daylight", "at": grill_mid, "size": [26, 4],
         "base": r(gp(gx, gz - GRILL["d"] / 2))[1], "glowOpacity": 0.10, "sparks": 0.08},
        {"id": "bay-waves", "type": "waves", "what": "the bay's rows of small waves, far (ENGINE-20's kind), toward the shore below us", "area": bay_poly,
         "rows": 9, "per": 8, "size": 4, "speed": 3, "toward": "S", "color": "#f4f8fb", "opacity": 0.38, "plane": "back"},
        {"id": "bay-shimmer", "type": "shimmer", "what": "the morning glitter on the bay", "poly": bay_poly, "count": 22, "size": 4, "flow": [3, 0], "life": 1.8,
         "color": "#f6eed8", "opacity": 0.45, "plane": "back"},
        {"id": "noren-sway", "type": "sway", "plane": "noren", "anchor": "top", "amount": 2.2, "period": 3.4, "wave": 26, "lean": 0.35, "what": "the noren stirring in the wind off the bay"},
        {"id": "cloud-drift", "type": "bob", "plane": "cloud", "amount": 1, "period": 11, "what": "Fuji's cap of cloud breathing on its top (very slow); the scene hides it when it has lifted"},
        {"id": "gulls", "type": "birds", "kind": "flyers", "plane": "back", "what": "gulls over the bay (the engine's own silhouettes, pale)",
         "lanes": [[[-12, 150], [200, 168], [360, 236], [452, 214], [470, -12]], [[520, -12], [430, 232], [330, 262], [180, 160], [-12, 140]]],
         "every": [8, 16], "group": [1, 2], "speed": 55, "size": 7, "scale": [0.6, 1.0], "color": "#f6eed8",
         "behind": [[r(p) for p in tea_roof[:4]] + [[0, 470]], [[452, 60], [800, 60], [800, 300], [452, 300]]],
         "note": "they cross the bay between the teahouse and the hackberry; behind the teahouse's roof and the hackberry's crown"},
        {"id": "courier", "type": "birds", "kind": "flyers", "what": "the relay courier: he runs along the road now and then, left to right and back, the letter box on his shoulder",
         "lanes": [[[-30, 512], [830, 512]], [[830, 520], [-30, 520]]], "every": [18, 34], "group": [1, 1], "speed": 150, "frames_note": "PEOPLE-21A's courier, running, both ways (until its frames are given, the engine would draw a bird's silhouette: SCENES-21A gives the frames, or walks him as a person on these lines)",
         "sizeAt": 512, "base": 512, "behind": [], "note": "His lane is the road's middle (rows 512 going right, 520 coming back): there a grown-up is 117 px and a man of 1.56 m 104 px; he passes IN FRONT of everything on the far side of the road (the grill, the trunks, the palanquin, the teahouse) and BEHIND only the front plane; nobody stands in his lane at `teahouse` or `peddler` (those are above it), so he never runs through the family unless they stand in the road's middle. If the engine walks him as a person instead, the same two lines are his path (courierFrom -> courierTo)."},
    ]
    out = {
        "id": "edo-kurasawa", "horizon": HZ, "full": FULL,
        "view": {"horizon": HZ, "full": FULL, "camera": "persp.Camera(300, 590): eye 317 cm, Z0 875, focal 800, vanishing x 400 (as Yui's)",
                 "road": "the Tokaido across the picture, z 40 to 560 cm (rows 576 to 477); the ledge beyond it, its wall's top at z 900 (left) to 1100 (middle); the rest place before the mound to z 1700 (row 399)",
                 "compass": "the act's (as Yui's): the bay in front, Fuji across it, the way west to the right; the left edge is the road back to Yui"},
        "light": "morning: the act's sun in the east, behind us and to the left, about 30 degrees up (an hour after Yui, a little more behind us: shadows fall right and away, 1.15 : 0.85); the hill behind us throws its shadow across the near verge and the near edge of the road from the left",
        "walk": walk, "walk_note": "one area: the road (rows 476 to 596), the strip before the teahouse's door (O-Kuni's place behind the grill), the ledge's strip before the wall, and the rest place before the mound (up to row 426 under the hackberry); the climb is the way out at the right edge, not walked up here",
        "blocked": blocked,
        "planes": planes_out, "cutouts": cutouts,
        "things": things,
        "marks": M, "stands": stands,
        "exits": [{"to": "edo-village", "edge": "left", "at": M["yui"], "what": "the road back east to Yui (its west end)"},
                  {"to": "edo-satta", "edge": "right", "at": M["climb"], "what": "up the cliff road to the top of the pass (once the family is dressed: #22)"}],
        "fx": fx,
        "fx_note": "the grill's smoke and embers; the bay's far waves and its glitter; the noren sways; Fuji's cloud bobs a pixel (very slow) and is hidden once it has lifted (the state is the scene's, from the pass); gulls (engine-drawn); the courier's run is a flyer along the road (PEOPLE-21A's frames) or a walk along the same line",
        "heights": {"mom_cm": 168, "bigsis_cm": 160, "lilsis_cm": 122, "man_1830_cm": 156, "woman_1830_cm": 146, "grownup_at_full_px": 160},
        "sizes": {m: {"grownup": stands[m]["grownup_px"], "mom": round(px(v[1], 168)), "lilsis": round(px(v[1], 122)), "man": round(px(v[1], 156)), "woman": round(px(v[1], 146))} for m, v in M.items()},
    }
    return out

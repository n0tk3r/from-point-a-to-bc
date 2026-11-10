"""PAINT-21A: layout.json for edo-satta, measured through the scene's camera from the same numbers the picture was painted
with (edo_satta.py's placings), and from the finished cut-outs' pixels. PAINT-23 (round twenty-three): the near plane
(near.png, and the front plane drawn again), the patch of road under the near rock (`blocked`), the near pine's sway."""

import math

import numpy as np

import edo_satta as S
from edo_satta import HZ, FULL, V, gp, kz, ROAD, BANK, JIZO, SEAT, PINE, FUJI, COAST, CLIFF_FOOT, CLIFF_TOP, RIDGE, BLOCK, bank_top, road_far


def r(p):
    return [int(round(p[0])), int(round(p[1]))]


def box_of(alpha, pad=0):
    ys, xs = np.where(alpha > 0.5)
    if len(ys) == 0:
        return [0, 0, 0, 0]
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 1 + 2 * pad, int(ys.max() - ys.min()) + 1 + 2 * pad]


def px(y, cm=175.0):
    return 160.0 * (y - HZ) / (FULL - HZ) * cm / 175.0


def stand(p, face="N"):
    x, y = p
    return {"at": [int(round(x)), int(round(y))], "grownup_px": int(round(px(y))), "face": face}


def person_rect(p, cm, seated=False):
    h = px(p[1], cm) * (0.72 if seated else 1.0)
    return [int(round(p[0] - h * 0.2)), int(round(p[1] - h)), int(round(h * 0.4)), int(round(h))]


def layout(planes, info):
    jx, jy = gp(JIZO["x"], JIZO["z"])
    sx, sy = gp(SEAT["x"], SEAT["z"] - SEAT["d"] / 2)
    pfoot = gp(PINE["x"], PINE["z"])
    M = {
        "below": [24, 578],                                                  # the left edge: up from Nishikurasawa (and back down)
        "jizo": r(gp(*S.JIZO_MARK)),                                         # before the Jizo, a little to its left: Little Sister its height here
        "pine": [654, 502],                                                  # by the bent pine at the edge
        "view": [262, 498],                                                  # at the low place in the bank: where one stands to look at Fuji
        "stone": [196, 516],                                                 # before O-Shige's stone
        "shige": [int(round(sx)), int(round(sy)) + 4],                       # O-Shige, sitting on her stone (her feet just before it)
        "kyuzo": [212, 504],                                                 # Kyuzo, standing by her with her box on its pole
        "mosukeFrom": [22, 572], "mosukeTo": [788, 522],                     # the woodcutter's way: the whole road, and back
        "okitsu": [786, 514],                                                # the right edge: west, which refuses
        "arrive_mom": [70, 556], "arrive_bigsis": [44, 572], "arrive_lilsis": [96, 566],   # (mine) the three, come up from below
        "shige_arrive": [30, 560],                                           # (mine) where O-Shige and Kyuzo come up behind them
    }
    faces = {"below": "E", "jizo": "N", "pine": "N", "view": "N", "stone": "W", "shige": "S", "kyuzo": "S", "mosukeFrom": "E", "mosukeTo": "W",
             "okitsu": "W", "arrive_mom": "E", "arrive_bigsis": "E", "arrive_lilsis": "E", "shige_arrive": "E"}
    stands = {k: stand(v, faces[k]) for k, v in M.items()}
    stands["jizo"]["note"] = "Little Sister here is exactly the Jizo's height (78 px): she can reach its hat"
    stands["shige"]["note"] = "she SITS on the stone: her feet at this point, her seat on the stone's top (44 cm up)"
    # ---- the walk: the road, edge to edge, dropping at the left to the climb and starting down at the right
    top = [[int(x_), int(round(road_far(x_) + 3))] for x_ in (0, 30, 60, 90, 120, 150, 690, 720, 750, 780, 800)]
    walk = top + [[800, 596], [0, 596]]
    sb = [r(gp(SEAT["x"] - SEAT["w"] / 2 - 10, SEAT["z"] - SEAT["d"] / 2 - 4)), r(gp(SEAT["x"] + SEAT["w"] / 2 + 10, SEAT["z"] - SEAT["d"] / 2 - 4)),
          r(gp(SEAT["x"] + SEAT["w"] / 2 + 10, SEAT["z"] + SEAT["d"] / 2)), r(gp(SEAT["x"] - SEAT["w"] / 2 - 10, SEAT["z"] + SEAT["d"] / 2))]
    blocked = [sb, BLOCK]                                                    # (round twenty-three: the road under the near rock, bottom right)
    # ---- the cut-outs, back to front, with their bases and states
    planes_out = [
        {"id": "cloud", "file": "cloud.png", "plane": "back", "state": "on: Fuji's cap of cloud / lifted: the scene fades it out (#24 step 5, Little Sister: \"It CAME OUT.\"); the backdrop under it is the clear summit",
         "what": "the cap of cloud on Fuji's top (the same cloud as at Nishikurasawa)"},
        {"id": "pine", "file": "pine.png", "base": int(round(pfoot[1])), "what": "the bent pine on the bank's edge, leaning toward Fuji (it sways: fx pine-sway); everyone on the road is in front of it"},
        {"id": "front", "file": "front.png", "plane": "front", "what": "the lip of the cutting we stand on, along the bottom edge: rock breaking through the turf, grass flattened to the left by the wind; a shoulder of rock and last year's pampas grass in the bottom right corner (round twenty-three)"},
        {"id": "near", "file": "near.png", "plane": "front", "what": "the near plane (round twenty-three): a wind-bent black pine on the slope at our right, its trunk in from the right edge above Okitsu, its limbs and pads streaming left across the top (it stirs: fx near-sway)"},
        {"id": "pass", "file": "pass.png", "alt": True, "base": int(round(jy)), "state": "on: O-Shige's pass, folded in oiled paper, caught on the Jizo's hat (from the gust as she reaches the top) / gone: lifted off (edo.passFound)",
         "what": "the folded paper on the Jizo's little hat (an alt: not shown at first)"},
    ]
    cutouts = {p["id"]: box_of(planes[p["id"]][1]) for p in planes_out}
    # ---- things (ROUND-21's list, each with a shape), and the stand a look or a use walks the lead to
    cloud_outline = info.get("cloud_outline", [])
    pass_quad = info.get("pass_quad", [])
    bay_poly = [[214, 300], [440, 296], [700, 290], [668, 300], [690, 304], [740, 312], [800, 318], [800, 470], [700, 470], [330, 474], [316, 474],
                [294, 460], [236, 440], [150, 430], [60, 437], [0, 452], [0, 372], [110, 357], [214, 346]]
    things = [
        {"id": "fuji", "what": "Mount Fuji, enormous, across the head of the bay (the cloud on it, or clear)", "shape": {"rect": [150, 30, 400, 258]}, "stand": M["view"], "face": "N"},
        {"id": "cloud", "what": "the cap of cloud on Fuji's top (a cut-out: on / lifted)", "shape": {"poly": [r(p) for p in cloud_outline[::3]]} if cloud_outline else {"rect": [240, 10, 220, 70]}, "stand": M["view"], "face": "N"},
        {"id": "bay", "what": "Suruga Bay, far below", "shape": {"poly": bay_poly}, "stand": M["view"], "face": "N"},
        {"id": "izu", "what": "Izu, long and low across the bay to the east", "shape": {"poly": [[430, 290], [452, 278], [516, 269], [584, 267], [646, 275], [700, 290]]}, "stand": M["view"], "face": "N"},
        {"id": "oldshore", "what": "the old shore under the cliffs: white water and rock (the road ran there until 1655: 'forget your parent, forget your child')",
         "shape": {"poly": [r(p) for p in CLIFF_TOP] + [r((p[0], p[1] + 6)) for p in reversed(CLIFF_FOOT)]}, "stand": M["view"], "face": "N"},
        {"id": "pine", "what": "the bent pine at the edge, leaning toward Fuji (a cut-out: it sways)", "shape": {"rect": box_of(planes["pine"][1], 2)}, "stand": M["pine"], "face": "N"},
        {"id": "jizo", "what": "the Jizo by the road: a small stone figure in a red bib and a little straw hat, child height", "shape": {"rect": info["jizo_box"]}, "stand": M["jizo"], "face": "N"},
        {"id": "jizohat", "what": "the Jizo's little straw hat (where the folded pass is caught)", "shape": {"rect": info["hat_box"]}, "stand": M["jizo"], "face": "N"},
        {"id": "pass", "what": "the folded paper in oiled paper caught on the Jizo's hat: a woman's travel pass (an alt cut-out: on / gone)", "shape": {"rect": box_of(planes["pass"][1], 3)}, "stand": M["jizo"], "face": "N"},
        {"id": "edge", "what": "the cliff edge: a low bank of earth and grass at the road's far side (never a drop at the road)",
         "shape": {"poly": [[int(x_), int(round(bank_top(x_) - 4))] for x_ in range(0, 801, 50)] + [[int(x_), int(round(road_far(x_)))] for x_ in range(800, -1, -50)]},
         "stand": M["view"], "face": "N"},
        {"id": "road", "what": "the road over the pass, narrow, cut into the mountainside: east down to Nishikurasawa, west on to Okitsu",
         "shape": {"poly": [[int(x_), int(round(road_far(x_)))] for x_ in range(0, 801, 50)] + [[800, 568], [0, 568]]}, "stand": [400, 540], "face": "S"},
        {"id": "okitsu", "what": "Okitsu's roofs far to the west, along its shore in the haze", "shape": {"rect": [700, 270, 100, 46]}, "stand": M["okitsu"], "face": "N"},
        {"id": "temple", "what": "a temple's roof among trees on a rise at Okitsu, in the haze (Big Sister: where a boy hostage once lived far from his mother)", "shape": {"rect": [726, 280, 40, 18]}, "stand": M["okitsu"], "face": "N"},
        {"id": "gulls", "what": "gulls hanging in the wind over the bay (the engine's)", "shape": {"rect": [240, 300, 420, 140]}, "stand": M["view"], "face": "N"},
    ]
    people = [("mosuke", [420, 540], 156, False, "Mosuke the woodcutter, a load of brushwood on his back, on his way along the road (fx/his walk: mosukeFrom <-> mosukeTo)"),
              ("shige", M["shige"], 146, True, "O-Shige, resting on her stone"), ("kyuzo", M["kyuzo"], 156, False, "Kyuzo, her old manservant, her box on a pole")]
    for pid, at, cm, seated, what in people:
        things.append({"id": pid, "what": what + " (drawn by the game)", "shape": {"rect": person_rect(at, cm, seated)}, "stand": [at[0] + 50, min(at[1] + 18, 560)], "face": "W"})
    # ---- fx: what moves (the engine draws it)
    cliff_water = [[p[0], p[1] - 2] for p in CLIFF_FOOT] + [[p[0] + 10, p[1] + 16] for p in reversed(CLIFF_FOOT)]
    near_water = [[p[0], p[1] - 14] for p in COAST] + [[p[0], p[1] - 1] for p in reversed(COAST)]
    fx = [
        {"id": "pine-sway", "type": "sway", "plane": "pine", "anchor": "bottom", "at": int(round(pfoot[1])), "amount": 2.2, "period": 3.8, "wave": 40, "lean": -0.4,
         "what": "the bent pine working in the wind off the sea (rooted at its foot; it leans left, toward Fuji, and the wind pushes it that way)"},
        {"id": "cloud-drift", "type": "bob", "plane": "cloud", "amount": 1, "period": 11, "what": "Fuji's cap of cloud breathing on its top; the scene fades the cut-out when it lifts"},
        {"id": "near-sway", "type": "sway", "plane": "near", "anchor": "right", "amount": 1.6, "period": 4.6, "wave": 260, "lean": 0.2,
         "what": "the near pine's limbs lifting and falling in the wind (the trunk at the right edge holds; the tips, at the left, move most)"},
        {"id": "oldshore-waves", "type": "waves", "what": "the white water breaking along the foot of the cliffs: the old shore (ENGINE-20's kind, small rows, toward the cliffs)",
         "area": cliff_water, "rows": 3, "per": 10, "size": 3, "speed": 4, "toward": "N", "color": "#f4f8fb", "opacity": 0.7, "plane": "back"},
        {"id": "flank-waves", "type": "waves", "what": "the wash round the near flank's foot, below us", "area": near_water, "rows": 3, "per": 12, "size": 4, "speed": 4,
         "toward": "S", "color": "#f4f8fb", "opacity": 0.55, "plane": "back"},
        {"id": "bay-shimmer", "type": "shimmer", "what": "the morning glitter on the bay far below", "poly": bay_poly, "count": 30, "size": 4, "flow": [-3, 0], "life": 1.8,
         "color": "#f6eed8", "opacity": 0.45, "plane": "back", "holes": [[[620, 300], [800, 300], [800, 476], [620, 476]]]},
        {"id": "bay-waves", "type": "waves", "what": "the bay's rows of waves in the middle distance (the far rows are painted still)", "area": [[230, 340], [800, 330], [800, 470], [330, 474], [300, 440], [230, 380]],
         "holes": [[[630, 300], [720, 300], [720, 476], [630, 476]]], "rows": 8, "per": 9, "size": 5, "speed": 4, "toward": "S", "color": "#f4f8fb", "opacity": 0.35, "plane": "back"},
        {"id": "gulls", "type": "birds", "kind": "flyers", "plane": "back", "what": "gulls hanging in the wind over the bay below and before us (the engine's own silhouettes, pale): slow, gliding",
         "lanes": [[[810, 360], [600, 340], [420, 372], [260, 344], [-12, 380]], [[-12, 420], [180, 400], [380, 418], [560, 396], [810, 420]],
                   [[810, 250], [640, 236], [470, 262], [300, 230], [-12, 258]]],
         "every": [7, 14], "group": [1, 2], "speed": 34, "size": 8, "scale": [0.7, 1.15], "color": "#f6eed8",
         "behind": [[[618, 160], [800, 160], [800, 480], [618, 480]]], "note": "slow (34 px a second): they hang in the wind; behind the pine (the box round it)"},
    ]
    out = {
        "id": "edo-satta", "horizon": HZ, "full": FULL,
        "view": {"horizon": HZ, "full": FULL, "camera": "persp.Camera(288, 590): eye 330 cm, Z0 875, focal 800, vanishing x 400",
                 "road": "the road across the picture, z 70 to 430 cm (rows 567 to 491), level here; its bank z 430 to 520, 34 cm high (its top about row 470); at the left edge road and bank drop away toward the climb (rows 549 at x 20), at the right edge they start down to Okitsu",
                 "height": "the pass is about 90 m over the bay: the bay lies 90 m below the road (the sea seen just over the bank is about 420 m off)",
                 "compass": "the act's: the bay in front, Fuji across it, Izu across it to the east, Okitsu far to the west at the right edge"},
        "light": "morning, wind: the act's sun in the east, behind us and to the left, about 30 degrees up (as at Yui: shadows fall right and away, 1.6 : 0.5); the wind off the sea from the right (the pine leans left, the grass too; the gulls hang facing it)",
        "walk": walk, "walk_note": "one area: the road from edge to edge (the bank is not walked: the edge is the bank's foot); it drops at the left toward the climb (from Nishikurasawa) and starts down at the right (west, to Okitsu: it refuses)",
        "blocked": blocked,
        "planes": planes_out, "cutouts": cutouts,
        "things": things,
        "marks": M, "stands": stands,
        "exits": [{"to": "edo-kurasawa", "edge": "left", "at": M["below"], "what": "back down the cliff road to Nishikurasawa"},
                  {"to": None, "edge": "right", "at": M["okitsu"], "what": "west to Okitsu: refuses (Mom: \"Not till I know what's at Arai.\" / after: \"Not by road. We said.\")"}],
        "fx": fx,
        "fx_note": "the pine sways, and the near pine's limbs; Fuji's cloud bobs a pixel and the scene fades it out when it lifts (the backdrop is the clear mountain); white water moves along the old shore and round the near flank's foot; the bay glitters and its middle rows move; gulls hang in the wind (engine-drawn); Mosuke's walk is the scene's (mosukeFrom <-> mosukeTo, the whole road)",
        "heights": {"mom_cm": 168, "bigsis_cm": 160, "lilsis_cm": 122, "man_1830_cm": 156, "woman_1830_cm": 146, "jizo_cm": JIZO["h"], "grownup_at_full_px": 160},
        "jizo": {"base": r((jx, jy)), "height_px": round(JIZO["h"] * kz(JIZO["z"]), 1), "lilsis_at_jizo_px": round(px(M["jizo"][1], 122), 1),
                 "note": "the Jizo stands 129 cm with its stone, 446 cm back; at its mark Little Sister (1.22 m) is drawn exactly its height"},
        "sizes": {m: {"grownup": stands[m]["grownup_px"], "mom": round(px(v[1], 168)), "lilsis": round(px(v[1], 122)), "man": round(px(v[1], 156)), "woman": round(px(v[1], 146))} for m, v in M.items()},
    }
    return out

"""The castle approach's layout.json: every number the scene file needs, measured from the picture as painted
(edo_castle_kit's measurements, and the painted layers themselves for the shapes that hug things). PAINT-20D.

Round twenty-three (DEPTH.md, DEEPEN): edo_castle_depth.py paints the scene and calls write() with its cut-outs' covers
and what the far plane measured: the keep and its stone base were staged again through the same camera, so their two
shapes are measured again from the painting (`keep_shape`, `stonebase_shape`); the near plane (near.png, plane front) is
listed last; every other number is round twenty's, as the scene file has them.

  python3 edo_castle_layout.py      writes out/edo-castle/layout.json from round twenty's layers (the scene's painter calls
                                    write() itself, with the round-twenty-three layers)"""

import json
import os

import numpy as np

from edo_castle_kit import *
import edo_castle as EC
import edo_castle_herons as HE

r = lambda q: [int(round(q[0])), int(round(q[1]))]


def hull(mask, pad=2.0, most=18):
    from scipy.spatial import ConvexHull
    ys, xs = np.where(mask)
    pts = np.stack([xs, ys], axis=1).astype(float)
    pts = np.concatenate([pts, pts + [1, 0], pts + [0, 1], pts + [1, 1]])
    hv = pts[ConvexHull(pts).vertices]
    c = hv.mean(axis=0)
    hv = c + (hv - c) * (1 + pad / np.maximum(np.linalg.norm(hv - c, axis=1, keepdims=True), 1))
    while len(hv) > most:
        n = len(hv)
        areas = [abs((hv[(i + 1) % n] - hv[i])[0] * (hv[i - 1] - hv[i])[1] - (hv[(i + 1) % n] - hv[i])[1] * (hv[i - 1] - hv[i])[0]) for i in range(n)]   # (numpy 2.5 has no 2-d cross)
        hv = np.delete(hv, int(np.argmin(areas)), axis=0)
    return [[int(round(x)), int(round(y))] for x, y in hv]


# ---------------------------------------------------------------- the places (ROUND-20.md's names)
MARKS = {
    "enter": [150, 580],            # from the road, after the walk: at the left, under the cherry's boughs' reach
    "cherry": [176, 526],           # under the double cherry, on the bank (behind the trunk's base row: under the low boughs)
    "ladder": [586, 468],           # the foot of Tomezo's ladder, at the gate's outer wall, left of the opening
    "tomezo": [604, 392],           # him, up the ladder (a stand with its own scale, below)
    "crew": [494, 466],             # where the crew gathers: on the terrace between the scaffold and the ladder
    "gate": [679, 444],             # the way in, past the guards: in the opening, on the threshold
    "guard1": [642, 448],           # the two guards, either side of the opening, a step out from the posts
    "guard2": [716, 448],
    "tile": [560, 520],             # where one stands on the ramp to look up at the gable's cross tile
    "moat": [300, 506],             # on the bank by the herons
    "road": [420, 584],             # the pilgrims' road below, at the ramp's foot
    "pilgrimsFrom": [812, 574],     # the pilgrims come in at the right edge and go off at the left (east: toward the Ise road)
    "pilgrimsTo": [-14, 590],
    "pilgrimsVia": [[700, 578], [560, 586], [400, 590], [240, 586], [100, 590]],
    "scaffold1": [486, 404],        # a plasterer on the lower lift of the scaffold (a stand with its own scale)
    "scaffold2": [536, 372],        # and one on the upper lift
    "underBoughs": [228, 512],      # where Little Sister lies under the boughs and lets the petals land on her face
    "toKeep": [679, 426],           # the walkTo of the way in (inside the opening, behind the gate's base: hidden)
}
FACES = {"enter": "E", "cherry": "N", "ladder": "N", "tomezo": "N", "crew": "E", "gate": "N", "guard1": "E", "guard2": "W",
         "tile": "N", "moat": "N", "road": "W", "pilgrimsFrom": "W", "pilgrimsTo": "W", "scaffold1": "N", "scaffold2": "N",
         "underBoughs": "S", "toKeep": "N"}


def walk_outline():
    """The ground people stand on: the road across the bottom; the bank under the cherry up to the water's edge; the
    ramp; the terrace before the gate, into the opening. Never the water, never behind the wall, never the parapets."""
    f0, f1, fy = EC.RAMP["foot"]
    t0, t1, ty = EC.RAMP["top"]
    o0, o1 = EC.GATE["open"]
    return [[6, 596], [794, 596], [794, EC.ROAD_TOP + 4], [f1 + 2, EC.ROAD_TOP + 2], [t1 - 2, ty + 2], [EC.TERRACE["x1"] - 6, EC.TERRACE["front"] - 4],
            [EC.TERRACE["x1"] - 6, EC.TERRACE["top"] + 6], [o1 - 4, EC.TERRACE["top"] + 6], [o1 - 4, EC.GATE["sill"] - 14], [o0 + 4, EC.GATE["sill"] - 14],
            [o0 + 4, EC.TERRACE["top"] + 6], [EC.TERRACE["x0"] + 8, EC.TERRACE["top"] + 6], [EC.TERRACE["x0"] + 8, EC.TERRACE["front"] - 6],
            [t0 + 2, ty + 2], [f0 - 2, EC.ROAD_TOP + 2], [f0 - 14, EC.ROAD_TOP - 6], [430, EC.MOAT["near"] + 10], [300, EC.MOAT["near"] + 12],
            [120, EC.MOAT["near"] + 10], [6, EC.MOAT["near"] + 8]]


def outline_of(mask, most=12, pad=2.0, rows=None):
    """A clicked area's shape round a painted mask: its hull, at most `most` points (rows: only the mask's part between
    two picture rows)."""
    m = mask > 0.5
    if rows is not None:
        m = m.copy()
        m[:rows[0]] = False
        m[rows[1]:] = False
    return hull(m, pad, most)


def trace(mask, most=16, pad=2, eps=2.0):
    """A clicked area's outline that follows a painted silhouette (not its hull: the keep's sky stays sky): the largest
    outline of the mask, grown by `pad` pixels, simplified to at most `most` points."""
    import cv2
    m = (np.asarray(mask) > 0.5).astype(np.uint8)
    if pad:
        m = cv2.dilate(m, np.ones((2 * pad + 1, 2 * pad + 1), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)
    e = eps
    while True:
        a = cv2.approxPolyDP(c, e, True)
        if len(a) <= most:
            break
        e *= 1.25
    return [[int(x), int(y)] for x, y in a[:, 0, :]]


def keep_shape(keep, base, wing):
    """The keep's area: the keep, its stone base and the corridor turret as far as the gate tower, down to where the
    outer wall's coping hides them (row 346); the stone base's own area lies over it (later in the scene's list)."""
    m = np.maximum(np.maximum(keep, base), wing).copy()
    m[346:] = 0
    m[:, 593:] = 0
    return trace(m, most=16, pad=2, eps=2.0)


def stonebase_shape(base, keep):
    """The stone base's area: the stones that show, from the keep's first wall down to the outer wall's coping."""
    m = (base > 0.5) & ~(keep - base > 0.5)
    return outline_of(m.astype(np.float32), most=6, pad=1.0, rows=(0, 346))


def write(path, planes=None, info=None):
    if planes is None:
        cuts = EC.cut_layers()
        alpha = {k: v.a > 0.5 for k, v in cuts.items()}
    else:
        alpha = {k: np.asarray(v) > 0.5 for k, v in planes.items()}
    out = {"id": "edo-castle", "horizon": HZ, "full": FULL, "minScale": 0.3,
           "light": "late afternoon, 29 April 1830: the sun low in the west, to our right and a little behind us (about 17 degrees up): "
                    "faces turned to us and to the right are warm (the last light on white plaster), left faces lilac; shadows run "
                    "far to the left and a little away, about three times a thing's height. Key: edo-castle.",
           "note": "The land camera (persp.Camera 290/588): the lens 3.26 m above the road, level. The road is the near ground (a grown-up 160 px "
                   "at the bottom edge's full row); the ramp climbs to the terrace before the gate (rows 470 to 436: 0.60 to 0.49 of full, a "
                   "1.56 m guard 70 px at the threshold); the keep is far and high (not on the ground plane: its stone base's foot, row 332, "
                   "is on the hill behind the wall). East is to the left of the picture: the pilgrims go off that way."}
    out["walk"] = walk_outline()
    out["walk_note"] = ("one floor: the road, the bank under the cherry, the ramp and the terrace, into the gate's opening (rows 422 to 436 inside the "
                        "posts: whoever walks in there is behind gate.png's base and vanishes into the passage). The water, the parapets and the "
                        "ground behind the wall are outside it.")
    f0, f1, fy = EC.RAMP["foot"]
    t0, t1, ty = EC.RAMP["top"]
    out["blocked"] = [
        [[EC.TUB["at"][0] - 24, EC.TUB["at"][1] + 1], [EC.TUB["at"][0] + 24, EC.TUB["at"][1] + 1], [EC.TUB["at"][0] + 22, EC.TUB["at"][1] - 10], [EC.TUB["at"][0] - 22, EC.TUB["at"][1] - 10]],
    ]
    out["blocked_note"] = "the tub's ground (its cut-out is also solid); the scaffold's poles and the buckets give solid ground of their own (planes)"
    # ---- the cut-outs, back to front, as the scene lists them
    sc = EC.SCAF
    planes = [
        {"id": "ladder", "file": "ladder.png", "plane": "back", "what": "Tomezo's ladder against the gate's outer wall, left of the opening: behind everybody "
                                                                        "(he climbs its front; nobody passes behind a ladder on a wall). The scene may hide it when the crew goes in."},
        {"id": "gate", "file": "gate.png", "base": EC.GATE["sill"], "what": "the Ni-no-mon gate: its opening is clear (the backdrop's passage shows through). Whoever "
                                                                          "walks past the threshold (feet above row 436) is drawn behind it: into the gate. The guards stand "
                                                                          "in front (row 448).",
         "solid": [[EC.GATE["x0"], EC.GATE["sill"] + 2], [EC.GATE["open"][0] - 2, EC.GATE["sill"] + 2], [EC.GATE["open"][0] - 2, EC.GATE["sill"] - 30], [EC.GATE["x0"], EC.GATE["sill"] - 30]]},
        {"id": "scaffold", "file": "scaffold.png", "base": sc["foot"], "what": "the plasterers' bamboo scaffold against the wall by the gate: people pass in front of it "
                                                                              "(on the terrace, rows 451 to 470) and behind it (between its poles and the wall, rows 437 to 449)",
         "solid": [[[px - 3, sc["foot"] + 2], [px + 3, sc["foot"] + 2], [px + 3, sc["foot"] - 3], [px - 3, sc["foot"] - 3]] for px in sc["x"]]},
        {"id": "tub", "file": "tub.png", "base": EC.TUB["at"][1], "what": "the mixing tub of lime on the terrace",
         "solid": [[EC.TUB["at"][0] - 23, EC.TUB["at"][1] + 1], [EC.TUB["at"][0] + 23, EC.TUB["at"][1] + 1], [EC.TUB["at"][0] + 21, EC.TUB["at"][1] - 9], [EC.TUB["at"][0] - 21, EC.TUB["at"][1] - 9]]},
    ]
    for i, b in enumerate(EC.BUCKETS):
        x, y = b["at"]
        planes.append({"id": f"bucket-{i + 1}", "file": f"bucket-{i + 1}.png", "base": y, "what": f"bucket {i + 1} of lime, full, by the ramp's top: the crew carries it away (the scene hides it; the backdrop is complete under it)",
                       "solid": [[x - 10, y + 1], [x + 10, y + 1], [x + 9, y - 6], [x - 9, y - 6]], "state": "full (hidden once carried)"})
    planes.append({"id": "cherry", "file": "cherry.png", "base": 548, "what": "the double cherry: its trunk and all its boughs. People on the bank (feet above row 548) "
                                                                            "are behind it, under the boughs; people on the road pass in front of its foot.",
                   "solid": [[70, 550], [108, 550], [108, 538], [70, 538]]})
    if "near" in alpha:                                                            # round twenty-three: the near plane, in front of everybody
        planes.append({"id": "near", "file": "near.png", "plane": "front", "what": "the near plane (DEPTH.md): the old cherry's great limb up the left edge "
                                                                                  "and its boughs of blossom across the top-left, the tips of a pine's bough at "
                                                                                  "the top right, the moat's stone edge and its reeds along the bottom. People "
                                                                                  "always pass behind it; nothing clicked or stood on is behind it."})
    out["planes"] = planes
    out["cutouts"] = {k: [int(v) for v in box_of(alpha[k])] for k in EC.CUTS + (["near"] if "near" in alpha else [])}
    # ---- the things to click (every one of ROUND-20.md's list)
    things = []

    def thing(id_, what, shape, stand, face="N", **more):
        d = {"id": id_, "what": what, "shape": {"poly": shape}, "stand": stand, "face": face}
        d.update(more)
        things.append(d)
    o0, o1 = EC.GATE["open"]
    thing("cherry", "the one old double cherry in full late bloom, its heavy pink clusters; petals coming down", hull(alpha["cherry"], 2, 20), MARKS["cherry"])
    thing("petals", "the petals drifting down from the cherry (the engine's: fx petals)", [[0, 300], [300, 300], [300, 470], [0, 470]], MARKS["underBoughs"], "S")
    if info is not None:                                                           # round twenty-three: staged again, measured again
        thing("keep", "the keep, 100 m off and turned forty degrees: white, five roofs with their gables, its long face in the low sun, its "
                      "short face in shade, on its stone base; a corridor turret runs on from it behind the gate tower. Its top ridge's "
                      "middle is where it was (x 360, row 34): the herons face it", keep_shape(info["keep"], info["base"], info["wing"]), MARKS["tile"])
        thing("stonebase", "the keep's stone base of fitted stones, every one a different shape, its sides curving out toward the foot",
              stonebase_shape(info["base"], info["keep"]), MARKS["tile"])
    else:
        thing("keep", "the keep: white, five roofs, on its tall sloping stone base, high on its hill", [[244, 334], [478, 334], [466, 266], [440, 222], [404, 56], [380, 34], [340, 34], [316, 56], [280, 222], [254, 266]], MARKS["tile"])
        thing("stonebase", "the keep's stone base, its sides curving out to the foot", [[244, 334], [478, 334], [446, 264], [274, 264]], MARKS["tile"])
    thing("gate", "the Ni-no-mon: a gate in a white wall under a small tiled tower, standing open; two guards in it", hull(alpha["gate"], 2, 16), MARKS["gate"])
    thing("gable", "the gable on the gate's tower, toward us: at its peak the round end tile, and on the tile, small, a cross",
          [[EC.GABLE["base"][0][0] - 4, EC.GABLE["base"][0][1] + 4], [EC.GABLE["base"][1][0] + 4, EC.GABLE["base"][1][1] + 4], [EC.GABLE["apex"][0], EC.GABLE["apex"][1] - 6]], MARKS["tile"],
          tile={"at": list(EC.GABLE["tile"]), "r": EC.GABLE["r"]}, note="a look from the mark tile; the tile is 9 px across at 800 x 600: it reads when told it is there")
    thing("guards", "the two gate guards, two swords each, counting everybody in and out (PEOPLE-20 draws them at guard1 and guard2)", [[o0 - 8, EC.GATE["sill"] + 16], [o1 + 8, EC.GATE["sill"] + 16], [o1 + 8, EC.GATE["sill"] - 74], [o0 - 8, EC.GATE["sill"] - 74]], MARKS["gate"])
    thing("ladder", "a ladder against the gate's outer wall, lime dripped down it", hull(alpha["ladder"], 3, 10), MARKS["ladder"])
    thing("tomezo", "Tomezo the plaster foreman, up the ladder, white from head to foot, shouting at nobody", [[586, 400], [626, 400], [626, 322], [586, 322]], MARKS["ladder"], note="his figure at marks.tomezo (PEOPLE-20): the area is his")
    thing("scaffold", "a bamboo scaffold lashed with rope against the wall, two lifts of planks, a bucket hung on it", hull(alpha["scaffold"], 2, 14), MARKS["crew"])
    thing("buckets", "three wooden buckets of lime by the ramp's top, full", hull(alpha["bucket-1"] | alpha["bucket-2"] | alpha["bucket-3"], 3, 10), [526, 520],
          each=[{"id": f"bucket-{i + 1}", "shape": hull(alpha[f"bucket-{i + 1}"], 3, 8), "stand": [b["at"][0], b["at"][1] + 18]} for i, b in enumerate(EC.BUCKETS)])
    thing("tub", "the mixing tub, lime in it, a paddle", hull(alpha["tub"], 3, 10), [520, 484])
    thing("wall", "the white wall on its stone footing, loopholes along it; grey with the winter at the far end, new white where the plasterers have been", [[0, 344], [574, 348], [574, 400], [0, 404]], MARKS["moat"])
    thing("moat", "the inner moat under the wall, still, the wall and the cherry in it", [[0, 438], [444, 438], [450, 484], [0, 486]], MARKS["moat"])
    thing("herons", "herons standing in the moat, every one facing the top of the keep (the engine's flocks: fx herons and egrets)", [[40, 440], [420, 440], [420, 484], [40, 484]], MARKS["moat"])
    thing("pilgrims", "Himeji people going by on the road now and then, east, ladles in hand (PEOPLE-20's pilgrim1 to pilgrim3, along marks.pilgrimsVia)", [[0, 560], [800, 556], [800, 598], [0, 598]], MARKS["road"], "S")
    thing("road", "the road below the castle, dusty, trodden", [[0, 540], [432, 540], [582, 540], [800, 542], [800, 598], [0, 598]], MARKS["road"])
    thing("ramp", "the stone ramp up to the gate, a low parapet each side", [[f0 - 10, fy], [f1 + 10, fy], [t1 + 6, ty], [t0 - 6, ty]], MARKS["tile"])
    thing("terrace", "the paved ground before the gate, spattered white", [[EC.TERRACE["x0"], 436], [800, 436], [800, 476], [t1, ty], [t0, ty], [EC.TERRACE["x0"], 468]], MARKS["crew"])
    thing("hills", "the hills of Harima, pale in the evening air", [[430, 240], [800, 236], [800, 300], [430, 300]], MARKS["tile"])
    thing("sky", "the sky over the castle, cerulean to cobalt, one long flat cloud", [[0, 0], [800, 0], [800, 230], [470, 230], [470, 36], [250, 36], [250, 0]], MARKS["tile"])
    out["things"] = things
    # ---- the marks and the stands
    out["marks"] = dict(MARKS)
    out["faces"] = FACES
    stands = {}
    for k, v in MARKS.items():
        if isinstance(v[0], list):
            continue
        stands[k] = {"at": v, "grownup_px": int(round(160 * scale_at(v[1]))), "floor": "ground"}
    lad_k = k_at(EC.LADDER["foot"][0][1])                      # the ladder's foot row: its depth
    stands["tomezo"] = {"at": MARKS["tomezo"], "grownup_px": int(round(175 * lad_k)), "scale": round(lad_k / (160 / 175.0), 3), "floor": "ladder", "base": 465,
                        "note": "on the ladder, 1.6 m up its rungs: his size is the ladder's depth (its foot row 464), not his own row; a 1.56 m man is "
                                f"{int(round(156 * lad_k))} px. face N (he faces the wall), turning to shout. Hands on the rails at x 600 and 616. "
                                "He must sort at base 465 (in front of gate.png, whose base is 436, and of the ladder): by his feet he would be behind the "
                                "gate's wall and hidden. SCENES-20: a person with a base of his own (as g.climbTo's base), not sorted by his row. "
                                "The ladder's rungs: `ladder` below (LADDER_RUNG 25 cm, 13.3 px; his feet on rung 6)."}
    for name, row in (("scaffold1", EC.SCAF["lifts"][0]), ("scaffold2", EC.SCAF["lifts"][1])):
        kk = k_at(EC.SCAF["foot"] - 4)
        stands[name] = {"at": MARKS[name], "grownup_px": int(round(175 * kk)), "scale": round(kk / (160 / 175.0), 3), "floor": "scaffold", "base": 451,
                        "note": f"a plasterer on the lift at row {row} (the plank's top row is {row - 6}): the scaffold's depth (its front poles' feet, row 450); "
                                f"a 1.56 m man is {int(round(156 * kk))} px; drawn in front of scaffold.png (the engine sorts him by his feet, above its base: give him base 451 or draw him as a scene person with his own base)"}
    out["stands"] = stands
    # the ladder, for PEOPLE-20's tomezo-ladder (LADDER_RUNG): its rails, its rungs' rows, the rung's height in cm
    (lf0, lf1), (lt0, lt1) = EC.LADDER["foot"], EC.LADDER["top"]
    L = ((lt0[0] - lf0[0]) ** 2 + (lt0[1] - lf0[1]) ** 2) ** 0.5
    n = EC.LADDER["rungs"]
    out["ladder"] = {"foot": [list(lf0), list(lf1)], "top": [list(lt0), list(lt1)], "rungs": n, "length_px": round(L, 1), "length_cm": round(L / lad_k),
                     "rung_px": round(L / n, 2), "rung_cm": round(L / n / lad_k), "scale": round(lad_k / (160 / 175.0), 3),
                     "rung_rows": [round(lf0[1] - (i + 0.5) * (lt0[1] - lf0[1]) / -n, 1) for i in range(n)],
                     "rails_x_at_tomezo": [round(lf0[0] + (lt0[0] - lf0[0]) * (lf0[1] - 392) / (lf0[1] - lt0[1]), 1), round(lf1[0] + (lt1[0] - lf1[0]) * (lf1[1] - 392) / (lf1[1] - lt1[1]), 1)],
                     "note": "LADDER_RUNG 25 cm: eleven rungs 13.3 px apart at the ladder's depth (0.534 px/cm, the foot row 464; the ladder is 2.74 m "
                             "long and leans 4 degrees to the right, its top on the gate's wall at row 318). Rung n is on row 464 - (n - 0.5) x 13.3: "
                             "rung 6 is row 391, where marks.tomezo puts his feet (1.37 m up). The rails are 18 px apart at the foot, 16 at the top."}
    out["sizes"] = {"man_px_at_enter": round(160 * scale_at(580), 1), "man_px_at_gate": round(160 * scale_at(444), 1), "guard_156cm_px_at_guard1": round(156 / 175 * 160 * scale_at(448), 1),
                    "man_px_at_crew": round(160 * scale_at(466), 1), "man_px_at_tile": round(160 * scale_at(520), 1), "man_px_at_cherry": round(160 * scale_at(526), 1),
                    "mom_168cm_px_at_enter": round(168 / 175 * 160 * scale_at(580), 1), "lilsis_122cm_px_at_underBoughs": round(122 / 175 * 160 * scale_at(512), 1),
                    "heron_95cm_px_in_moat": round(95 / 175 * 160 * scale_at(462), 1), "gate_opening_px": [o1 - o0, EC.GATE["sill"] - EC.GATE["lintel"]]}
    out["exits"] = [{"to": "edo-keep", "id": "in", "name": "into the gate", "walkTo": MARKS["gate"], "via": MARKS["toKeep"], "spawn": "enter",
                     "band": [[o0, EC.GATE["sill"] - 14], [o1, EC.GATE["sill"] - 14], [o1, EC.GATE["sill"] + 12], [o0, EC.GATE["sill"] + 12]],
                     "note": "the way in is the gate's opening, past the guards (the scene opens it with #28: until then the guards turn people back). "
                             "No way out at the picture's edges: the family came by the road (the walk cut-scene), and leaves the castle by the map."}]
    # ---- the moving things
    mo = EC.MOAT
    herons_area = [[60, mo["far"] + 10], [330, mo["far"] + 8], [330, mo["near"] - 6], [60, mo["near"] - 4]]
    egrets_area = [[200, mo["far"] + 12], [424, mo["far"] + 8], [424, mo["near"] - 10], [200, mo["near"] - 8]]
    water_poly = [[0, mo["far"] + 2], [mo["x1"] + 10, mo["far"] + 2], [mo["x1"] + 18, mo["near"]], [0, mo["near"] + 2]]
    out["fx"] = [
        {"id": "petals", "type": "petals", "what": "the double cherry's petals drifting down: ENGINE-20's moving thing", "from": [[10, 70], [270, 70], [290, 300], [260, 440], [120, 440], [0, 340]],
         "to": [[0, 470], [330, 470], [330, 600], [0, 600]], "count": 22, "every": [0.4, 1.6], "drift": [10, -2], "fall": 18, "size": [2, 3], "color": "#eeaac0", "light": "#f8d5de",
         "plane": "front", "wind": "from the right, light: they drift a little to the left as they fall, turning",
         "note": "ENGINE-20 names the fields: this is what the painter asks for. About 22 on the stage at once, leaving the crown anywhere in `from` (the "
                 "clusters), falling to the bank and the road in `to` at about 18 px a second at full size, drifting left, each turning as a petal does; "
                 "pink (#eeaac0) with the lit ones paler. In front of everybody (plane front): they fall across whoever stands under the tree."},
        {"id": "herons", "type": "birds", "kind": "flock", "what": "three grey herons standing in the moat, every one facing the keep", "area": herons_area, "count": 3,
         "frames": HE.frames_block("heron"), "shy": 0, "fly": False, "turn": False, "depth": True,
         "moves": {"stand": 5, "look": 3, "peck": 1, "walk": 1, "turn": 0}, "walk": 5, "plane": "back",
         "note": "Facing E (toward the keep, up and to the right); turn false: none ever faces away from it (the design: every heron faces the top of the keep). "
                 "`look` is the neck stretched up at the keep; `peck` the strike at the water; `walk` a slow stalk. They stand their ground (shy 0, fly false). "
                 "In the water, behind everybody (plane back: nobody can be in the water)."},
        {"id": "egrets", "type": "birds", "kind": "flock", "what": "two white egrets among them, facing the keep too", "area": egrets_area, "count": 2,
         "frames": HE.frames_block("egret"), "shy": 0, "fly": False, "turn": False, "depth": True,
         "moves": {"stand": 5, "look": 3, "peck": 1, "walk": 1, "turn": 0}, "walk": 5, "plane": "back", "seed": 3,
         "note": "the same frames in white, drawn a little smaller (egret-<n>: 0.86 of the heron); a flock of its own, as a flock takes one set"},
        {"id": "moat-light", "type": "shimmer", "what": "a few glints on the still water of the moat", "poly": water_poly, "count": 5, "size": 3, "flow": [-1.5, 0], "life": 2.4,
         "color": "#f4fbff", "opacity": 0.28, "plane": "back", "note": "quiet: the moat is still; the herons stand in it (their feet are drawn over the glints)"},
    ]
    out["fx_note"] = ("Moving: the petals (ENGINE-20), the herons and the egrets (frames here), the glints; and the people's small lives (PEOPLE-20): the guards "
                      "at guard1 and guard2, the plasterers on scaffold1 and scaffold2 and at crew, Tomezo on the ladder, the pilgrims along pilgrimsVia. No flags "
                      "are painted on the gate tower (none to stir). The cherry does not sway: the air is nearly still, the petals say what wind there is.")
    out["frames"] = {"herons": dict(HE.frames_block("heron"), files="heron-<n>.png and egret-<n>.png, n 1 to 11", acts=HE.ACTS, size=[HE.BOX[0], HE.BOX[1]],
                                    note=("Grey herons, facing E (the engine turns them for W; the flocks never turn); every frame on one canvas with the feet at the foot "
                                          "point; painted at full size (sizeAt 590: a heron with its neck up is 87 px there, 46 px in the moat at row 462). "
                                          "egret-<n> is the same drawing in white at 0.86."))}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    return out


def box_of(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return (0, 0, 0, 0)
    return (xs.min(), ys.min(), xs.max() - xs.min() + 1, ys.max() - ys.min() + 1)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    o = write(f"{OUT}/layout.json")
    print(json.dumps(o["stands"], indent=None)[:900])

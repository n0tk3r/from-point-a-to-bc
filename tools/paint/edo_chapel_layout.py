"""layout.json for edo-chapel: the numbers the game needs, MEASURED from the finished picture (PAINT-20F).

Every rect is the box round the pixels that really show that thing (found from what each ray of the picture met).
Places on the floor (where to stand, the walk outline, the base lines of the cut-outs) are the model's centimetres put
through the same camera as the picture."""

import json

import numpy as np

from room import View
import edo_chapel_model as M
import edo_chapel_things as T

OUT = "out/edo-chapel"
W, H = 800, 600


def write(stA, stB, stD, boxes, wob=None):
    v = View(**M.VIEW)

    def fl(X, Z):
        x, y = v.pt(X, 0, Z)
        return [int(round(x)), int(round(y))]

    def at(X, Y, Z):
        x, y = v.pt(X, Y, Z)
        return [int(round(x)), int(round(y))]

    def rect_of(st, names, extra=None):
        ids = [st.names[n] for n in names if n in st.names]
        m = np.isin(st.pick(st.oid), ids)
        if wob is not None:
            m = wob(m.astype(np.float32)) > 0.5
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            return None
        r = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
        if extra:
            r = [min(r[0], extra[0]), min(r[1], extra[1]), max(r[2], extra[2]), max(r[3], extra[3])]
        return [r[0], r[1], r[2] - r[0], r[3] - r[1]]

    def rect_xywh(b):
        return [b[0], b[1], b[2] - b[0], b[3] - b[1]] if b else None

    def grow(r, n):
        return [r[0] - n, r[1] - n, r[2] + 2 * n, r[3] + 2 * n] if r else None

    mk = M.MARKS
    stand = {k: fl(*p) for k, p in mk.items()}
    size = {k: int(round(v.person(*p)[2])) for k, p in mk.items()}

    things = []

    def thing(id_, what, rect, at_, face, **more):
        if rect is None:
            print("layout: nothing found for", id_)
            return
        t = {"id": id_, "what": what, "shape": {"rect": rect}, "stand": stand[at_], "face": face}
        t.update(more)
        things.append(t)

    def person_rect(mark, cm):
        x, y = stand[mark]
        px = size[mark] * cm / 175.0
        w = int(round(px * 0.34))
        return [x - w // 2, int(round(y - px)), w, int(round(px))]

    A, B, D = stA, stB, stD
    thing("altar", "the closet altar: a plain cupboard of two doors on a low plinth against the back wall (cut-out altar-shut.png; open: altar-open.png)",
          rect_xywh(boxes["altar-shut"]), "altar", "N", open=rect_xywh(boxes["altar-open"]))
    thing("kannon", "inside the open altar: the small white Kannon holding a child, on a red cloth (Kannon-sama to anyone who asks; Maria to them)",
          grow(rect_xywh(boxes.get("kannon")), 3), "altar", "N", when="altar open")
    thing("calendar", "the folded sheet of the calendar, leaning inside the altar at the left: columns of marks, brown at the folds",
          grow(rect_xywh(boxes.get("calendar")), 3), "altar", "N", when="altar open")
    thing("bowl", "the plain wooden bowl of water on the altar's shelf, at the right (Jinsuke keeps the water)",
          grow(rect_xywh(boxes.get("bowl")), 3), "altar", "N", when="altar open")
    thing("mirror", "the grandmother's bronze mirror, round, on its small wooden stand, its face toward the room (cut-out mirror.png)",
          grow(rect_xywh(boxes["mirror"]), 3), "atmirror", "N")
    thing("stand", "the mirror's stand: a small post of plain wood with a ledge and a back-rest", rect_of(B, ["stand"]), "atmirror", "N")
    lamp_rects = {}
    for name in M.LAMPS:
        lamp_rects[name] = grow(rect_of(A, [name, ]), 4)
    lr = [r for r in lamp_rects.values() if r]
    union = [min(r[0] for r in lr), min(r[1] for r in lr), 0, 0]
    union[2] = max(r[0] + r[2] for r in lr) - union[0]
    union[3] = max(r[1] + r[3] for r in lr) - union[1]
    thing("lamps", "the three small clay oil lamps: on the left wall's ledge, on the stand before the altar, in the niche right of the mirror (cut-outs lamps.png alight, lamps-out.png cold); the flames are the engine's",
          union, "altar", "N", each={k: v_ for k, v_ in lamp_rects.items()})
    thing("lamp-left", "the clay lamp on its ledge in the left wall, by the ladder's foot", lamp_rects["lamp-left"], "atlamp", "W")
    thing("lamp-stand", "the clay lamp on its wooden stand on the floor before the altar's left side: it lights the altar and the Kannon", lamp_rects["lamp-stand"], "altar", "N")
    thing("lampstand", "the lamp stand: a post of plain wood with a top board, before the altar's left side", rect_of(B, ["lampstand"]), "altar", "N")
    thing("lamp-altar-r", "the clay lamp in its niche in the back wall, right of the mirror", lamp_rects["lamp-altar-r"], "sei", "N")
    wx, wy = M.WALL_PATCH
    wall_rect = [at(wx - 42, wy + 44, 0)[0], at(wx - 42, wy + 44, 0)[1], 0, 0]
    br = at(wx + 42, wy - 44, 0)
    wall_rect[2], wall_rect[3] = br[0] - wall_rect[0], br[1] - wall_rect[1]
    thing("wall", "the bare earth wall left of the altar, between the ladder and the lamp's niche: where the grandmother turns the mirror's light (#27)",
          wall_rect, "atwall", "N", patch=at(wx, wy, 0), patch_px=29)
    thing("ladder", "the ladder up to the trapdoor, leaning down from the hatch toward us to the mats' near edge (cut-out ladder.png; in the morning sun ladder-day.png)",
          rect_xywh(boxes["ladder"]), "ladder", "W")
    x0, x1, z0, z1 = M.MATS
    things.append({"id": "mats", "what": "the straw mats on the floor, old gold, laid in strips, bound with dark cloth; the family sits here",
                   "shape": {"poly": [fl(x0, z0), fl(x1, z0), fl(x1, min(z1, 300)), fl(x0, min(z1, 300))]}, "stand": stand["sit"], "face": "N"})
    thing("props", "the rough timber props holding the beams: the two at the walls before the mats (cut-out props.png) and the near ones", rect_xywh(boxes["props"]), "atlamp", "W")
    thing("beams", "the cross beams under the earth ceiling, and the boards laid between them", rect_of(B, ["beam"]), "sit", "N")
    thing("trapdoor", "the trapdoor overhead, in the hatch at the top of the ladder (states: shut; open by lamplight; open by morning light)",
          grow(rect_xywh(boxes["trapdoor-shut"]), 2), "ladder", "W", open=rect_xywh(boxes["trapdoor-lamp"]), day=rect_xywh(boxes["trapdoor-day"]))
    thing("basket", "a charcoal basket of woven bamboo, heaped, near us at the left", rect_of(B, ["basket", "charcoal"]), "atlamp", "W")
    thing("jar", "a water jar, near us at the right", rect_of(B, ["jar"]), "front", "E")
    thing("sack", "a charcoal sack by the centre prop", rect_of(B, ["sack"]), "front", "S")
    thing("sei", "Grandmother Sei (1.40 m), by her mirror", person_rect("sei", 140), "sei", "S")
    thing("jinsuke", "Jinsuke (1.56 m), his arms out in front of his daughter", person_rect("jinsuke", 156), "jinsuke", "S")
    thing("orin", "O-Rin (1.18 m), behind her father, near the right wall", person_rect("orin", 118), "orin", "S")

    hx0, hx1, hz0, hz1 = M.HATCH
    hatch_poly = [at(hx0, M.H, hz0), at(hx1, M.H, hz0), at(hx1, M.H, hz1), at(hx0, M.H, hz1)]
    # the sun patch on the floor: measured from the day picture (where the sun fell on the shell)
    sun = D.down(D.sunlit) * D.down(D.mask_of("floor").astype(np.float32))
    if wob is not None:
        sun = wob(sun)
    ys, xs = np.nonzero(sun > 0.25)
    sun_rect = [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)] if len(xs) else None
    flames = {name: at(*pos) for name, pos in T.lamp_places().items()}
    mx, my, mz, mr = M.MIRROR
    lights = {
        "flames": flames,
        "hatch": hatch_poly,
        "sunpatch": {"rect": sun_rect, "centre": fl(*M.SUNPATCH), "stand": stand["sunpatch"],
                     "note": "the morning sun through the open hatch lands here (painted in trapdoor-day.png); the beam in the air is the engine's, from `hatch` to this"},
        "mirror": {"centre": at(mx, my, mz), "radius_px": int(round(mr * v.scale_at(mx, mz))),
                   "held": {"at": at(M.SUNPATCH[0], 118, M.SUNPATCH[1]), "note": "where the grandmother holds it up in the sun, at her breast, facing the back wall"}},
        "wall": {"patch": at(wx, wy, 0), "patch_px": 29, "rect": wall_rect,
                 "rule": "the mirror is 16 cm across and a little convex: its patch is about 16 x (1 + distance / 120 cm) across; from SUNPATCH to the wall is 155 cm, so 37 cm, 29 px on the back wall; the cross is the engine's, inside the patch"},
    }
    fx = [{"id": name, "type": "flame", "at": flames[name], "size": 9, "width": 4, "glow": 26, "glowColor": "#ffb060", "glowOpacity": 0.26,
           "flicker": 0.5, "base": "back", "when": "lamps lit", "what": f"the flame of {name}"} for name in M.LAMPS]

    def foot(X0, X1, Z0, Z1):
        return [fl(X0, Z0), fl(X1, Z0), fl(X1, Z1), fl(X0, Z1)]
    ax0, ax1, _, _, az0, az1 = M.ALTAR
    sx0, sx1, _, _, sz0, sz1 = M.STAND
    L = M.LADDER
    lsx, _, lsz, _ = M.LAMPS["lamp-stand"]
    feet = {"altar": foot(ax0 - 3, ax1 + 3, az0, az1 + 2), "stand": foot(sx0, sx1, sz0 - 2, sz1 + 2),
            "lampstand": foot(lsx - M.LAMP_STAND[1] / 2, lsx + M.LAMP_STAND[1] / 2, lsz - M.LAMP_STAND[1] / 2, lsz + M.LAMP_STAND[1] / 2),
            "ladder": foot(L["x"][0] - 4, L["x"][1] + 4, L["foot_z"] - 6, L["foot_z"] + 6),
            "posts": [foot(x - M.POST_R, x + M.POST_R, z - M.POST_R, z + M.POST_R) for (x, z) in M.POSTS],
            "frontpost": foot(M.FRONT_POST[0] - 9, M.FRONT_POST[0] + 9, M.FRONT_POST[1] - 9, M.FRONT_POST[1] + 9)}
    lay = {
        "id": M.ID, "horizon": M.VIEW["horizon"], "full": M.VIEW["full"], "view": M.VIEW, "eye_cm": int(round(v.eye)),
        "ceiling_cm": M.H, "beams_cm": M.BEAM_Y,
        "vanishing": [int(round(v.vanishing()[0][0])), int(round(v.vanishing()[0][1]))],
        "light": "night, by oil lamp: three small clay lamps, one on a ledge in the left wall by the ladder's foot, one on a lamp stand on the floor "
                 "before the altar's left side (it lights the altar's front and the Kannon), one in a niche in the back wall right of the mirror "
                 "(naples-yellow pools cut into flats; the shade ultramarine toward prussian); at morning (trapdoor-day) a cool shaft of daylight "
                 "down the open trapdoor onto the mats at `sunpatch`. The flames are fx.",
        "walk": [fl(X, Z) for X, Z in M.WALK],
        "blocked": [feet["lampstand"]],              # the lamp stand stands just inside the walk's notch before the altar
        "feet": feet,
        "planes": [
            {"id": "trapdoor", "states": {"shut": "trapdoor-shut.png", "lamp": "trapdoor-lamp.png", "day": "trapdoor-day.png"}, "plane": "back",
             "note": "the hatch overhead: the leaf shut; open on the dark storehouse (its lantern's faint warmth); open on the morning, and with it the sun on the mats and the wall (the back plane: people walk over the patch)"},
            {"id": "props", "file": "props.png", "base": [fl(M.POSTS[2][0], M.POSTS[2][1]), fl(M.POSTS[3][0], M.POSTS[3][1])],
             "solid": feet["posts"][2] + [], "note": "the two wall props before the mats: everyone on the mats is behind them"},
            {"id": "altar", "states": {"shut": "altar-shut.png", "open": "altar-open.png"}, "base": [fl(ax0 - 3, az1 + 2), fl(ax1 + 3, az1 + 2)],
             "solid": feet["altar"], "note": "shut: an ordinary cupboard; open: the Kannon, the calendar, the bowl, the doors swung out either side"},
            {"id": "mirror", "file": "mirror.png", "base": [fl(sx0, sz1 + 2), fl(sx1, sz1 + 2)], "note": "on its stand until the grandmother takes it down (#27); the stand is painted into the backdrop"},
            {"id": "lamps", "states": {"lit": "lamps.png", "out": "lamps-out.png"}, "plane": "back",
             "note": "the three lamps alight (the oil's surface bright) or cold; with them out the engine lays its dark glaze over the room and hides the flames"},
            {"id": "ladder", "states": {"lamp": "ladder.png", "day": "ladder-day.png"}, "base": [fl(L["x"][0], L["foot_z"]), fl(L["x"][1], L["foot_z"])],
             "solid": feet["ladder"], "note": "everyone on the walk is behind it; its upper rungs in the sun by day"},
            {"id": "front", "file": "front.png", "plane": "front", "note": "the centre prop under the near beam, at the right, cut off by the picture's bottom edge"},
        ],
        "things": things,
        "exits": [{"to": "edo-storehouse", "id": "ladder", "shape": {"rect": rect_xywh(boxes["ladder"])}, "stand": stand["ladder"], "face": "W",
                   "note": "up the ladder through the trapdoor"}],
        "marks": {"fromLadder": {k: stand[k] for k in ("mom", "bigsis", "lilsis")},
                  **{k: stand[k] for k in ("ladder", "altar", "sei", "jinsuke", "orin", "sit", "sit1", "sit2", "sit3", "sunpatch", "atwall", "atmirror", "atlamp", "front")},
                  "wall": at(wx, wy, 0)},
        "stands": {k: {"at": stand[k], "grownup_px": size[k]} for k in mk},
        "heights_px": {"at_back_wall": int(round(v.person(260, 24)[2])), "at_front": int(round(v.person(260, 176)[2])),
                       "note": "a 175 cm grown-up; Mom 168 is 0.96 of it, Sei 140 0.80, Jinsuke 156 0.89, O-Rin 118 0.67"},
        "ceiling_rows": {"back_wall": at(260, M.H, 0)[1], "walk_front": at(260, M.H, 176)[1], "beam_under_at_back": at(260, M.BEAM_Y, 86)[1],
                         "note": "Mom's head at the back wall is 13 px under the earth and 2 px under a beam: she clears them, just; the rig has no stoop"},
        "cutouts": {k: rect_xywh(b) for k, b in boxes.items() if b},
        "lights": lights,
        "fx": fx,
        "dark": {"note": "lamps out: a glaze of prussian blue #1a2846 at 0.82 over the backdrop and every cut-out (figureLight exposure -0.6), the flames hidden; "
                         "trapdoor-lamp's faint warmth, or trapdoor-shut's line of light, is then the only light"},
    }
    json.dump(lay, open(f"{OUT}/layout.json", "w"), indent=1)
    return lay

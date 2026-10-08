"""layout.json for home-bigsis-room: the numbers the game needs, MEASURED from the finished picture.

Every rect is the box round the pixels that really show that thing (found from what each ray of the picture
met), not a copy of the brief. Places on the floor (where to stand, the walk outline, the base line of the desk)
are the model's centimetres put through the same camera as the picture."""

import json

import numpy as np

from room import View
import home_bigsis_room_model as M

OUT = "out/home-bigsis-room"
W, H = 800, 600


def write(stA, stB, a_desk, a_front, wob=None):
    v = View(**M.VIEW)

    def fl(X, Z):
        x, y = v.pt(X, 0, Z)
        return [int(round(x)), int(round(y))]

    def at(X, Y, Z):
        x, y = v.pt(X, Y, Z)
        return [int(round(x)), int(round(y))]

    def rect_of(st, names, veil=False):
        ids = [st.names[n] for n in names if n in st.names]
        m = np.isin(st.pick(st.oid), ids)
        if veil and st.gauze is not None:
            g = st.gauze
            m |= np.isin(g.pick(g.oid), ids) & (g.pick(g.alpha) > 0.2) & (g.pick(g.t) < st.pick(st.t))
        if wob is not None:
            m = wob(m.astype(np.float32)) > 0.5
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            return None
        return [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]

    def quad(pts3):
        return [at(*p) for p in pts3]

    def bounds(pts):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return [max(min(xs), 0), max(min(ys), 0), min(max(xs), W) - max(min(xs), 0), min(max(ys), H) - max(min(ys), 0)]

    mk = M.MARKS
    stand = {k: fl(*p) for k, p in mk.items()}
    size = {k: int(round(v.person(*p)[2])) for k, p in mk.items()}
    things = []

    def thing(id_, what, rect, where, face, **more):
        if rect is None:
            print("layout: nothing found for", id_)
            return
        t = {"id": id_, "what": what, "shape": {"rect": rect}, "stand": stand[where], "face": face}
        t.update(more)
        things.append(t)

    A, B = stA, stB
    rx, rz, rr = M.RUG
    rug = bounds([fl(rx - rr, rz), fl(rx + rr, rz), fl(rx, rz - rr), fl(rx, rz + rr)])
    thing("bookcase", "the long low bookcase: her books arranged by color, in a rainbow", rect_of(B, ["bookcase"]), "atbooks", "N")
    thing("timeline", "her timeline: one long strip of paper on the wall, a ruled line, small drawings; a red mark three quarters along",
          rect_of(B, ["timeline"]), "attimeline", "N", red_mark=at(M.TIMELINE[0] + (M.TIMELINE[1] - M.TIMELINE[0]) * M.TIMELINE_RED, (M.TIMELINE[2] + M.TIMELINE[3]) / 2, 0.5))
    thing("soundtable", "the low table in the middle of the far wall", rect_of(B, ["soundtable", "machine", "fountain"]), "atsound", "E")
    thing("machine", "the sound machine: a small rounded box with a speaker grille and a dial (it runs on batteries)", rect_of(B, ["machine"]), "atsound", "E")
    thing("fountain", "the little tabletop fountain: water over stones in a bowl", rect_of(B, ["fountain"]), "atsound", "E")
    thing("desk", "her writing desk: the manuscript squared up, a jar of pencils, a small lamp turned low; the stool (cut-out desk.png)",
          rect_of(A, ["desk", "stool"]), "atdesk", "N")
    thing("cards", "her novel, planned on index cards in a neat grid over the desk", rect_of(B, ["cards"]), "atdesk", "N")
    thing("bed", "the low platform bed: white and cream linen, many pillows, a glow from under it", rect_of(B, ["bed", "pillows", "book"]), "atbed", "E")
    thing("book", "the book on her pillow, her place kept with a ribbon", rect_of(B, ["book"]), "atbed", "E")
    thing("canopy", "the gauze hung over the bed from a hoop under the rafters", rect_of(B, ["canopy"], veil=True), "atbed", "E")
    thing("saltlamp", "the salt lamp, deep amber, on its stump", rect_of(B, ["saltlamp"]), "atlamp", "W")
    thing("diffuser", "the diffuser on the smaller stump, breathing a thin thread of mist", rect_of(B, ["diffuser"]), "atlamp", "W",
          mist=at(M.STUMP2[0], M.STUMP2[3] + 22, M.STUMP2[1]))
    thing("plants", "the stand of green plants: ferns, trailing ivy, and the small palm in the corner", rect_of(B, ["plants", "palm"]), "atplants", "W")
    thing("towels", "the basket of rolled towels", rect_of(B, ["towels"]), "atplants", "W")
    thing("robe", "her white robe on its hook", rect_of(B, ["robe"]), "atplants", "W")
    thing("slippers", "her slippers, set side by side", rect_of(B, ["slippers"]), "atplants", "W")
    thing("mat", "the exercise mat, rolled out", rect_of(B, ["mat"]), "atmat", "W")
    thing("rug", "the round rug", rug, "middle", "N")
    thing("cushions", "floor cushions, stacked by the sound table", rect_of(B, ["cushions"]), "atsound", "E")
    sk = [bounds(quad(M.on_slope(*s))) for s in M.SKYLIGHTS]
    thing("skylight", "the two skylights in the slope of the roof: the night, the stars, the moon",
          bounds([[sk[0][0], sk[0][1]], [sk[1][0] + sk[1][2], sk[1][1] + sk[1][3]]]), "middle", "N", panes=sk)
    thing("window", "the round window in the left end wall, seen from the side", rect_of(B, ["window"]), "atlamp", "W")
    thing("hangplant", "a hanging plant under the slope, by the round window", rect_of(B, ["hangplant"]), "atplants", "W")
    thing("lanterns", "three paper lanterns under the slope", rect_of(B, ["lantern"]), "middle", "N")
    thing("strings", "strings of tiny warm lights looped from rafter to rafter", rect_of(B, ["strings"]), "middle", "N")
    thing("hatch", "the hatch in the floor: the top of the attic ladder coming up through it, and the rail round it (front plane): the way down",
          rect_of(A, ["hatch", "well"]), "athatch", "S")
    thing("rules", "her notice on its little easel: THE RETREAT / 1. SHOES OFF / 2. VOICES DOWN / 3. NO CHICKENS (front plane)",
          rect_of(A, ["rules"]), "athatch", "S")
    thing("pouf", "the big knitted pouf and a folded blanket (front plane)", rect_of(A, ["pouf", "books"]), "front", "S")
    thing("tea", "a floor cushion with her tea tray on it (front plane)", rect_of(A, ["tea"]), "front", "S")

    hx0, hx1, hz0, hz1 = M.HATCH
    hatch_rect = rect_of(A, ["hatch", "well"])
    exit_poly = [[hatch_rect[0], hatch_rect[1]], [hatch_rect[0] + hatch_rect[2], hatch_rect[1]], [hatch_rect[0] + hatch_rect[2], H], [hatch_rect[0], H]] if hatch_rect else []

    def foot(X0, X1, Z0, Z1):
        return [fl(X0, Z0), fl(X1, Z0), fl(X1, Z1), fl(X0, Z1)]

    def rnd(x, z, r):
        return foot(x - r, x + r, z - r, z + r)
    dx0, dx1, _, _, dz0, dz1 = M.DESK
    sx, sz, sr, _ = M.STOOL
    feet = {                                                 # the floor under each thing that stands beside the walk outline (none is inside it)
        "bookcase": foot(M.BOOKCASE[0], M.BOOKCASE[1], M.BOOKCASE[4], M.BOOKCASE[5]),
        "soundtable": foot(M.SOUNDTABLE[0], M.SOUNDTABLE[1], M.SOUNDTABLE[4], M.SOUNDTABLE[5]),
        "cushions": rnd(469, 31, 26), "desk": foot(dx0, dx1, dz0, dz1), "stool": rnd(sx, sz, sr),
        "bed": foot(M.BED[0], M.BED[1], M.BED[4], M.BED[5]), "footlamps": foot(612, 658, 362, 402),
        "palm": rnd(M.PALM[0], M.PALM[1], 16), "saltlamp": rnd(M.STUMP[0], M.STUMP[1], M.STUMP[2]), "diffuser": rnd(M.STUMP2[0], M.STUMP2[1], M.STUMP2[2]),
        "plants": foot(M.PLANTSTAND[0], M.PLANTSTAND[1], M.PLANTSTAND[4], M.PLANTSTAND[5]), "towels": rnd(M.BASKET[0], M.BASKET[1], M.BASKET[2]),
        "hatch": foot(hx0 - 6, hx1 + 6, hz0 - 6, hz1 + 6), "rules": foot(M.SIGN[0], M.SIGN[1], M.SIGN[4] - 44, M.SIGN[4] + 6),
        "tea": foot(M.TEA[0], M.TEA[1], M.TEA[2], M.TEA[3]), "pouf": rnd(M.POUF[0], M.POUF[1], M.POUF[2]),
    }
    lights = {                                               # where the game may draw its live lights and motion (none of them is painted as a beam)
        "lanterns": [at(x, y, z) for (x, z, y, r) in M.LANTERNS],
        "saltlamp": at(M.SALTLAMP[0], (M.SALTLAMP[2] + M.SALTLAMP[3]) / 2, M.SALTLAMP[1]),
        "candles": [at(x, M.LEDGE[3] + 8, 6.5) for x in M.CANDLES],
        "desk-lamp": at(M.DESK[1] - 26, M.DESK[3] + 15, M.DESK[4] + 22),
        "footlamps": [at(x, 10, z) for (x, z) in M.FOOTLAMPS],
        "moon": at((M.SKYLIGHTS[1][0] * 0.38 + M.SKYLIGHTS[1][1] * 0.62), M.roof(180) + 17, 180),
        "moon-patches": [[fl(x0 - 0.22 * M.roof(z0), z0 + 0.30 * M.roof(z0)), fl(x1 - 0.22 * M.roof(z0), z0 + 0.30 * M.roof(z0)),
                          fl(x1 - 0.22 * M.roof(z1), z1 + 0.30 * M.roof(z1)), fl(x0 - 0.22 * M.roof(z1), z1 + 0.30 * M.roof(z1))] for (x0, x1, z0, z1) in M.SKYLIGHTS],
        "machine": at((M.MACHINE[0] + M.MACHINE[1]) / 2, (M.MACHINE[2] + M.MACHINE[3]) / 2, M.MACHINE[5]),
        "fountain": at(M.FOUNTAIN[0], 70, M.FOUNTAIN[1]),
        "mist": at(M.STUMP2[0], M.STUMP2[3] + 22, M.STUMP2[1]),
        "hatch": at((hx0 + hx1) / 2, 0, (hz0 + hz1) / 2),
    }
    desk_base = [fl(dx0 - 2, dz1 + 2), fl(dx1 + 2, dz1 + 2)]
    ad, af = np.nonzero(a_desk > 0.5), np.nonzero(a_front > 0.5)
    L = {
        "id": M.ID, "horizon": M.VIEW["horizon"], "full": M.VIEW["full"], "view": M.VIEW, "eye_cm": int(round(v.eye)),
        "vanishing": [int(round(v.vanishing()[0][0])), int(round(v.vanishing()[0][1]))],
        "light": "night, soft and low, from many small warm sources: three paper lanterns under the slope, two strings of tiny lights looped "
                 "along the rafters, candles in glass along the far wall's ledge and by the bed, a salt lamp (deep amber) far left, a desk lamp "
                 "turned low, a glow from under the bed, the landing's light coming up the hatch; cool moonlight through the two skylights lies "
                 "in two soft slanted patches across the middle of the floor",
        "walk": [fl(X, Z) for X, Z in M.WALK],
        "blocked": [],                                       # nothing stands inside the outline: it is drawn round the furniture
        "feet": feet,
        "planes": [
            {"id": "desk", "file": "desk.png", "base": desk_base, "solid": foot(dx0 - 2, dx1 + 2, dz0, sz + sr),
             "note": "desk and stool, the manuscript, the pencils, the lamp. Nobody can stand behind it; `solid` is the floor under desk and stool."},
            {"id": "front", "file": "front.png", "plane": "front",
             "note": "the hatch with its rail and the top of the ladder, the notice on its easel, her shoes, the tea cushion, the pouf, the books"},
        ],
        "things": things,
        "exits": [{"to": "home-landing", "id": "hatch", "shape": {"poly": exit_poly}, "stand": stand["athatch"], "face": "S"}],
        "marks": {"fromLadder": {k: stand[k] for k in ("mom", "bigsis", "lilsis")},
                  "mom": stand["mom"], "bigsis": stand["bigsis"], "lilsis": stand["lilsis"]},
        "stands": {k: {"at": stand[k], "grownup_px": size[k]} for k in mk},
        "cutouts": {"desk": [int(ad[1].min()), int(ad[0].min()), int(ad[1].max() - ad[1].min() + 1), int(ad[0].max() - ad[0].min() + 1)],
                    "front": [int(af[1].min()), int(af[0].min()), int(af[1].max() - af[1].min() + 1), int(af[0].max() - af[0].min() + 1)]},
        "lights": lights,
        "notice": ["THE RETREAT", "1. SHOES OFF", "2. VOICES DOWN", "3. NO CHICKENS"],
    }
    json.dump(L, open(f"{OUT}/layout.json", "w"), indent=1)
    return L

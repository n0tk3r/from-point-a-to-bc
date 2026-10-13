"""layout.json for nevada-store: the numbers the scene writer needs, MEASURED from the finished picture.

Every shape is round the pixels that really show that thing (found from what each ray of the picture met), not a
copy of the brief. Places on the floor (where to stand, the walk outline, the base lines and the ground of the
cut-outs) are the model's centimetres put through the same camera as the picture.

    python3 nevada_store_layout.py check     draws layout.json over the comp: out/nevada-store-check.png"""

import json
import math
import sys

import numpy as np

from room import View
import nevada_store_model as M

OUT = "out/nevada-store"
W, H = 800, 600


def hull(points):
    """Convex hull (monotone chain) of [(x, y)]."""
    pts = sorted(set(map(tuple, points)))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def simplify(poly, most=12):
    """Drop the points of a closed outline that bend it least, until `most` are left."""
    p = list(poly)
    while len(p) > most:
        best, bi = 1e18, 0
        for i in range(len(p)):
            a, b, c = p[i - 1], p[i], p[(i + 1) % len(p)]
            area = abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]))
            if area < best:
                best, bi = area, i
        p.pop(bi)
    return p


def inside(pt, poly):
    x, y = pt
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1:
            c = not c
    return c


def write(stA, stB, covers, frames, hens, wob=None):
    v = View(**M.VIEW)

    def fl(X, Z):
        x, y = v.pt(X, 0, Z)
        return [int(round(x)), int(round(y))]

    def mask_of(st, names):
        ids = [st.names[n] for n in names if n in st.names]
        m = np.isin(st.pick(st.oid), ids)
        if wob is not None:
            m = wob(m.astype(np.float32)) > 0.5
        return m

    def rect_of(st, names, pad=1):
        m = mask_of(st, names)
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            return None
        x0, y0, x1, y1 = int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max()) + 1 + pad, int(ys.max()) + 1 + pad
        x0, y0 = max(x0, 0), max(y0, 0)
        x1, y1 = min(x1, W), min(y1, H)
        return [x0, y0, x1 - x0, y1 - y0]

    def poly_of(st, names, most=12, pad=1.0):
        m = mask_of(st, names)
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            return None
        pts = np.stack([xs, ys], 1)
        # the corners of the pixels on the outline are enough
        corners = np.concatenate([pts + [0, 0], pts + [1, 0], pts + [0, 1], pts + [1, 1]])
        h = hull([tuple(p) for p in corners.tolist()])
        h = simplify(h, most)
        cx, cy = np.mean([p[0] for p in h]), np.mean([p[1] for p in h])
        out = []
        for x, y in h:                                      # a pixel of air round it, so the outline does not cut the thing
            d = math.hypot(x - cx, y - cy) + 1e-6
            out.append([int(round(min(max(x + (x - cx) / d * pad, 0), W))), int(round(min(max(y + (y - cy) / d * pad, 0), H)))])
        return out

    def band_of(st, names, step=8):
        """A poly that hugs a wide band of many things (the hubcaps): its top and bottom edges column by column."""
        m = mask_of(st, names)
        cols = []
        for x0 in range(0, W, step):
            sl = m[:, x0:x0 + step]
            ys = np.nonzero(sl.any(axis=1))[0]
            if len(ys):
                cols.append((x0, int(ys.min()) - 2, int(ys.max()) + 3))
        if not cols:
            return None
        top = [[c[0], c[1]] for c in cols] + [[cols[-1][0] + step, cols[-1][1]]]
        bot = [[cols[-1][0] + step, cols[-1][2]]] + [[c[0], c[2]] for c in reversed(cols)]
        return simplify(top + bot, 40)

    mk = M.MARKS
    stand = {k: fl(*p) for k, p in mk.items()}
    size = {k: int(round(v.person(*p)[2])) for k, p in mk.items()}
    walk = [fl(X, Z) for X, Z in M.WALK]
    for k, p in stand.items():
        if k not in ("jolene", "jolene2") and not inside(p, walk):
            print("layout: the stand place", k, p, "is outside the walk outline")

    things = []

    def thing(id_, what, shape, at, face, **more):
        if shape is None:
            print("layout: nothing found for", id_)
            return
        sh = {"poly": shape} if isinstance(shape[0], list) else {"rect": shape}
        t = {"id": id_, "what": what, "shape": sh, "stand": stand[at], "face": face}
        t.update(more)
        things.append(t)

    A, B = stA, stB
    # listed back to front: where two shapes overlap, the later one is on top (the engine's areas are SVG shapes in order)
    thing("hubcaps", "the hubcap wall: a hundred and twelve, every one off this road; one is a tractor's wheel (the red one with the yellow hub, over the counter)",
          band_of(B, ["hubcaps"]), "athubcaps", "N")
    thing("fan", "the ceiling fan: it has not turned since 1979 (painted still, on purpose)", poly_of(B, ["fan"], 10), "atfan", "N")
    thing("window", "the front window: two sashes; through the near one the porch post, the back of the rocking chair, the lot and the road; "
          "the DISPLAY ONLY card propped on the sill", poly_of(B, ["window", "displaycard"], 8), "atwindow", "W")
    thing("backdoor", "the back door, open: the screen door hooked back inside, the step down, the hen yard in the sun, the five hens "
          "facing the fence, the desert past it", poly_of(B, ["backdoor", "yard", "step"], 8), "atbackdoor", "N",
          note="the hens are cut-outs the scene lays in the doorway (`hens`); Little Sister goes out onto the step (mark `step`)")
    thing("bulletin", "the bulletin board: lost dogs with tear-off tabs, and Jolene's card to Jed in big marker: JED: NO CHEESEBURGERS. WE TOLD YOU.",
          rect_of(B, ["bulletin"]), "atbulletin", "N")
    thing("hatrack", "the hat board over the counter: five pegs, today's hat missing from its peg (she is wearing it)", rect_of(A, ["hatrack", "hat1", "hat2", "hat3", "hat4", "hat5"]),
          "athatrack", "N", hats={f"hat-{n}": rect_of(A, [f"hat{n}"]) for n in range(1, 6)})
    thing("payphone", "the pay phone, dead since the eighties (she answers it)", rect_of(B, ["payphone"], 2), "atpayphone", "NE")
    thing("cooler", "Harold, the drinks cooler: lemonade in big jugs, pop in plain bottles; he hums (cut-out cooler.png)", rect_of(A, ["cooler"]), "atcooler", "N")
    thing("survival", "the survival shelf: flats and bottles of water (plain blue labels), jerky, space blankets folded in silver packets",
          rect_of(B, ["survival"]), "atsurvival", "N")
    thing("tv", "the TV on top of the survival shelf: rabbit ears with foil on one, one channel, snow (frames tv-0..2)", rect_of(B, ["tv", "tvscreen"], 2), "attv", "N")
    thing("chair", "Jolene's chair by the back door, where she watches her hens; her knitting on the seat: a very small striped sweater (for Doreen)",
          rect_of(A, ["chair", "knitting"], 2), "atchair", "E")
    thing("counter", "the counter: barn-red boards, a laminate top worn through where the money changes hands (cut-out counter.png)",
          poly_of(A, ["counter"], 8), "counter", "N")
    thing("grill", "the grill at the counter's right end: cold since 1979 (a card says GRILL CLOSED)", rect_of(A, ["grill"]), "atgrill", "N")
    thing("roller", "the hot dog roller on the grill: turning, empty, for company (frames roller-0, roller-1)", rect_of(A, ["roller", "rollers"], 2), "atroller", "N")
    thing("register", "the brass register: it rings for Jolene and nobody else", rect_of(A, ["register"]), "atregister", "N")
    thing("eggs", "the jar of pickled eggs: the jar is older than the eggs", rect_of(A, ["eggs"]), "ateggs", "N")
    thing("pennydish", "the take-a-penny dish: a chipped saucer, a few pennies, a little card (TAKE A PENNY / LEAVE A PENNY)", rect_of(A, ["pennydish"], 3), "atpennydish", "N")
    thing("postcards", "the postcard spinner on the counter: desert views", rect_of(A, ["postcards"]), "atpostcards", "N")
    thing("maprack", "the map rack on the counter's front: road maps of Nevada (it stops here too)", rect_of(A, ["maprack"]), "atmaprack", "N")
    thing("basket", "Ranger's basket at the counter's foot: wicker, the lid half off, a glint inside (his stash)", rect_of(A, ["basket"], 2), "atbasket", "NW")
    thing("autoshelf", "the auto shelf under the window: quarts of oil, wiper fluid, a can of chrome polish from 1987, a squeegee",
          rect_of(B, ["autoshelf"]), "atautoshelf", "W")
    thing("spinner", "the spinner rack of sunglasses: a few cheap pairs, $3.99 on a card (cut-out spinner.png)", rect_of(A, ["spinner"]), "atspinner", "W")
    thing("mirrorshades", "the last pair of mirror shades, on the hook toward us (cut-out mirror-shades.png, gone when bought)",
          rect_of(A, ["mirrorshades"], 3), "atspinner", "W", note="an extra id: the spinner's shape covers it too; drop it if the scene clicks the rack")
    thing("windowshade", "the sun shade in the far sash: folded silver, its bright side to us, DISPLAY ONLY on the card in front (cut-out window-shade.png)",
          rect_of(A, ["windowshade"]), "atshade", "W")
    thing("rockbins", "Grandpa Joe's rock bins: ROCKS $1; a name on tape under each bin: PEBBLE, STONY, ROCKY, THE SENATOR, SHY (DO NOT LOOK AT DIRECTLY)",
          poly_of(A, ["rockbins"], 10), "atrockbins", "N")
    thing("door", "the front door, shut behind the family: its pane bright with the porch, a card CLOSED on our side, the bell over it", poly_of(B, ["door", "bell"], 8), "atdoor", "W")

    def foot(X0, X1, Z0, Z1):
        return [fl(X0, Z0), fl(X1, Z0), fl(X1, Z1), fl(X0, Z1)]

    def circle(X, Z, r, n=10):
        return [fl(X + r * math.cos(a), Z + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n, endpoint=False)]
    cx0, cx1, _, _, cz0, cz1 = M.COUNTER
    gx1 = M.GRILL[1]
    bx0, bx1, _, _, bz0, bz1 = M.BASKET
    counter_solid = [fl(cx0, cz0), fl(gx1, cz0), fl(gx1, cz1), fl(bx1 + 18, cz1), fl(bx1 + 18, bz1 + 6), fl(bx0 - 6, bz1 + 6), fl(bx0 - 6, cz1), fl(cx0, cz1)]
    sx, sz, _ = M.SPINNER
    rk = M.ROCKBINS
    co = M.COOLER
    planes = [
        *[{"id": f"hat-{n}", "file": f"hat-{n}.png", "plane": "back",
           "note": f"hat {n}, {P_HATS[n]}: shown on its peg on every visit but the one when Jolene wears it (`when`: the visit count picks today's hat)"}
          for n in range(1, 6)],
        {"id": "doorframe", "file": "doorframe.png", "base": [fl(560, 0), fl(M.W, 0)],
         "note": "the back wall round the back door, its casing and the screen door, Jolene's chair and the phone: whoever is outside (the hens, "
                 "Little Sister on the step) is behind it and seen through the opening"},
        {"id": "cooler", "file": "cooler.png", "base": [fl(co[0], co[5]), fl(co[1], co[5])], "solid": foot(co[0], co[1], co[4], co[5])},
        {"id": "counter", "file": "counter.png", "base": [fl(cx0, cz1), fl(gx1, cz1)], "solid": counter_solid,
         "note": "the counter, the grill and the roller's tray, the register, the jar, the dish, the postcards, the map rack, Ranger's basket at its foot. "
                 "Jolene stands behind it; the roller's frames lie over it at the same base"},
        {"id": "spinner", "file": "spinner.png", "base": [fl(sx - 24, sz + 24), fl(sx + 24, sz + 24)], "solid": circle(sx, sz, 24.0)},
        {"id": "mirror-shades", "file": "mirror-shades.png", "alt": True, "base": [fl(sx - 24, sz + 24), fl(sx + 24, sz + 24)],
         "note": "an alt: the last pair, on the rack until it is bought (`when: !g.flag(\"nevada.shadesBought\")`); lay it just after the spinner"},
        {"id": "rockbins", "file": "rockbins.png", "base": [fl(rk[0], rk[5]), fl(rk[1], rk[5])], "solid": foot(rk[0], rk[1], rk[4], rk[5])},
        {"id": "window-shade", "file": "window-shade.png", "alt": True, "plane": "back",
         "note": "an alt: the sun shade in the window until Jolene gives it (`when: !g.flag(\"nevada.shadeGiven\")`); the window, the DISPLAY ONLY "
                 "card and the lot are painted complete under it"},
        {"id": "front", "file": "front.png", "plane": "front", "note": "the water flats (bottom left), the crate of empty bottles (bottom middle), the tyres (bottom right)"},
    ]
    blocked = [circle(sx, sz, 30.0)]                           # the spinner's foot, inside the walk (also its own `solid`)
    rf, tf = frames["roller"], frames["tv"]
    fx = [
        {"id": "roller", "what": "the hot dog roller turning, empty", "at": rf["at"], "foot": rf["foot"], "frames": rf["files"], "fps": 2,
         "base": [fl(cx0, cz1), fl(gx1, cz1)], "rect": rf["rect"], "note": "lies over counter.png at the counter's base"},
        {"id": "tv", "what": "snow on the TV's screen", "at": tf["at"], "foot": tf["foot"], "frames": tf["files"], "fps": 6, "plane": "back", "rect": tf["rect"]},
    ]
    door_poly = poly_of(B, ["door", "bell"], 8)
    L = {
        "id": M.ID, "horizon": M.VIEW["horizon"], "full": M.VIEW["full"], "view": M.VIEW, "eye_cm": int(round(v.eye)),
        "vanishing": [int(round(v.vanishing()[0][0])), int(round(v.vanishing()[0][1]))],
        "light": "morning: the sun low behind us and to the left comes in at the window's near sash and lies across the floor to the counter (warm); "
                 "the window is the brightest thing in the picture; cool sky light through the open back door; Harold glows a little; the corners "
                 "and the tin ceiling fall away into warm dark near us and cool dark far off",
        "fx_note": "The ceiling fan is painted still, on purpose: it has not turned since 1979. The hot dog roller turns (frames roller-0/1, 2 fps) "
                   "and the TV shows snow (tv-0/1/2, 6 fps). The cooler's hum is a sound, not paint.",
        "walk": walk,
        "walk_note": "one outline: the floor in front of the counter and round the room, through the back doorway onto the step (the step is at "
                     "floor height; the yard is a step down and not walked on), and to the front door's threshold at the left edge. Its front edge "
                     "keeps people under about 190 px; it keeps 14 px off the walls except at the two doorways",
        "blocked": blocked,
        "planes": planes,
        "things": things,
        "marks": {"fromLot": {k: stand[k] for k in ("mom", "bigsis", "lilsis")},
                  "jolene": {"at": stand["jolene"], "spots": [stand["jolene"], stand["jolene2"]], "face": "S",
                             "note": "behind the counter, standing (1.78 m): the counter's cut-out covers her below the waist; her second spot is by the register"},
                  "step": stand["step"], "step_face": "N", "counter": stand["counter"], "counter_face": "N"},
        "stands": {k: {"at": stand[k], "grownup_px": size[k]} for k in mk},
        "fx": fx,
        "hens": hens,
        "exits": [{"to": "nevada-roadside", "id": "door", "shape": {"poly": door_poly}, "stand": stand["atdoor"], "face": "W",
                   "how": "a thing `door` low at the picture's left edge (not the S edge): the shut front door with its bell. Using it takes the party "
                          "out to the lot; at the roadside they come out of the store's door (its stand place there is [296, 447])."}],
        "cutouts": {k: bbox(a) for k, a in covers.items()},
        "lights": {"window": [int(round(c)) for c in v.pt(-8, 140, 264)], "sun_on_floor": fl(300, 215), "backdoor": [int(round(c)) for c in v.pt(648, 120, 0)],
                   "harold": [int(round(c)) for c in v.pt((co[0] + co[1]) / 2, 100, co[5])]},
    }
    json.dump(L, open(f"{OUT}/layout.json", "w"), indent=1)
    return L


P_HATS = {1: "the straw cowboy hat", 2: "the sun hat with fruit on it", 3: "the tiara", 4: "the yellow hard hat", 5: "the hat shaped like a hen"}


def bbox(a):
    ys, xs = np.nonzero(a > 0.5)
    if len(xs) == 0:
        return None
    return [int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)]


def check(src="out/nevada-store-comp.png", out="out/nevada-store-check.png"):
    """Draw layout.json over the comp, to see that the numbers are where the things are."""
    from PIL import Image, ImageDraw
    L = json.load(open(f"{OUT}/layout.json"))
    im = Image.open(src).convert("RGB")
    d = ImageDraw.Draw(im)
    w = [tuple(p) for p in L["walk"]]
    d.line(w + [w[0]], fill=(120, 255, 160), width=1)
    for b in L["blocked"]:
        q = [tuple(p) for p in b]
        d.line(q + [q[0]], fill=(255, 120, 120), width=1)
    for t in L["things"]:
        sh = t["shape"]
        if "rect" in sh:
            x, y, ww, hh = sh["rect"]
            d.rectangle([x, y, x + ww, y + hh], outline=(255, 230, 90))
            lx, ly = x, y
        else:
            q = [tuple(p) for p in sh["poly"]]
            d.line(q + [q[0]], fill=(255, 230, 90), width=1)
            lx, ly = min(p[0] for p in q), min(p[1] for p in q)
        d.text((lx + 2, ly + 1), t["id"], fill=(255, 255, 255))
        sx, sy = t["stand"]
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], outline=(90, 220, 255))
    for p in L["planes"]:
        if isinstance(p.get("base"), list):
            d.line([tuple(p["base"][0]), tuple(p["base"][1])], fill=(255, 140, 40), width=2)
    for k, (x, y) in L["marks"]["fromLot"].items():
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 255, 255))
        d.text((x + 6, y - 5), k, fill=(255, 255, 255))
    for name, (x, y) in (("step", L["marks"]["step"]), ("counter", L["marks"]["counter"]), ("jolene", L["marks"]["jolene"]["spots"][0]),
                         ("jolene2", L["marks"]["jolene"]["spots"][1])):
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 120, 255))
        d.text((x + 6, y - 5), name, fill=(255, 200, 255))
    for h in L["hens"]["hens"]:
        x, y = h["at"]
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 60, 60))
    for f in L["fx"]:
        x, y = f["at"]
        d.ellipse([x - 3, y - 3, x + 3, y + 3], outline=(255, 60, 255))
    d.line([(0, L["horizon"]), (800, L["horizon"])], fill=(255, 80, 80))
    d.line([(0, L["full"]), (800, L["full"])], fill=(255, 220, 80))
    im.save(out)
    return out


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        print(check())

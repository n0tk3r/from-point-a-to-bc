"""PAINT-20A: layout.json for edo-village, measured through the scene's camera from the same numbers the picture was
painted with (edo_village.py's placings), and from the finished cut-outs' pixels."""

import numpy as np

from edo_village_kit import *
import edo_village_kit as K


def r(p):
    return [int(round(p[0])), int(round(p[1]))]


def box_of(alpha, pad=0):
    ys, xs = np.where(alpha > 0.5)
    if len(ys) == 0:
        return [0, 0, 0, 0]
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 1 + 2 * pad, int(ys.max() - ys.min()) + 1 + 2 * pad]


def stand(p, face="N"):
    """A standing place with the size of a grown-up there (the scene's straight-line rule from horizon and full)."""
    x, y = p
    return {"at": [int(round(x)), int(round(y))], "grownup_px": int(round(160 * (y - HZ) / (FULL - HZ))), "face": face}


def inland(x, z, d):
    return x + 0.857 * d, z - 0.514 * d


def layout(planes, info, SHOP, YARD, BOARD, WELL, RACKS, BIGBOAT, TENDER, SHIP_AT):
    # ---- the walk: the beach and the street, one area (the street 30 cm up: a sand slope, no second floor)
    far = 2600.0
    walk = []
    walk += [r(gp(shore_x(z) + 70, z)) for z in np.linspace(far, 1250, 6)]                 # along the water's edge (a step back from the wet sand)
    walk += [[0, int(round(gp(shore_x(1250) + 70, 1250)[1]))], [0, 596]]                   # the left edge down to the bottom
    walk += [[520, 596]]                                                                    # the bottom edge to the hen yard's corner
    yx0, yz0, yz1 = YARD["x0"] - 45, YARD["z0"], YARD["z1"] + 45                           # round the yard's fence
    walk += [r(gp(yx0, 20)), r(gp(yx0, yz1)), r(gp(min(YARD["x1"], 400 / kz(yz1) + 390), yz1))]
    walk += [[790, int(round(gp(yx0, yz1)[1]))]]
    walk += [r(gp(*inland(front_x(SHOP["z0"]) - 40, SHOP["z0"] - 30, 420)))]              # the forecourt in front of the shop's gable
    walk += [r(gp(front_x(SHOP["z0"]) - 50, SHOP["z0"] - 20))]
    walk += [r(gp(front_x(z) - 60, z)) for z in np.linspace(SHOP["z0"], far, 6)]           # along the house fronts
    # ---- blocked: the big boat, the tender, the racks, the board's platform, the well
    blocked = []
    for b in (BIGBOAT, TENDER):
        sx_, sz_ = b["stern"]
        pts = []
        for u in np.linspace(0, 1, 7):
            cx_, cz_ = inland(sx_, sz_, b["length"] * u)
            hw = b["beam"] * (0.3 + 0.7 * np.sin(np.pi * u) ** 0.6) + 25
            pts.append((cx_ - 0.514 * hw, cz_ - 0.857 * hw))
        for u in np.linspace(1, 0, 7):
            cx_, cz_ = inland(sx_, sz_, b["length"] * u)
            hw = b["beam"] * (0.3 + 0.7 * np.sin(np.pi * u) ** 0.6) + 25
            pts.append((cx_ + 0.514 * hw, cz_ + 0.857 * hw))
        blocked.append([r(gp(x_, z_)) for x_, z_ in pts])
    for rk in RACKS:
        x0, z0 = rk["x"], rk["z"]
        x1, z1 = x0 + rk["w"] * 0.76, z0 + rk["w"] * 0.64
        blocked.append([r(gp(x0 - 20, z0 - 30)), r(gp(x1 + 20, z1 - 30)), r(gp(x1 + 20, z1 + 30)), r(gp(x0 - 20, z0 + 30))])
    bz = BOARD["z"]
    bx = street_x(bz) + BOARD["off"]
    hw = BOARD["w"] / 2 + 30
    ax, az = bx - 0.514 * hw, bz - 0.857 * hw
    cx_, cz_ = bx + 0.514 * hw, bz + 0.857 * hw
    board_foot = [r(gp(*inland(ax, az, 70))), r(gp(*inland(cx_, cz_, 70))), r(gp(*inland(cx_, cz_, -50))), r(gp(*inland(ax, az, -50)))]
    blocked.append(board_foot)
    wz = WELL["z"]
    wx = street_x(wz) + WELL["off"]
    blocked.append([r(gp(wx - 70, wz - 60)), r(gp(wx + 70, wz - 60)), r(gp(wx + 70, wz + 60)), r(gp(wx - 70, wz + 60))])

    # ---- marks (ROUND-20's names)
    shop_door = gp(*inland(front_x(SHOP["z0"]) - 90, SHOP["z0"] - 55, 110))          # before the open front, a step back from the sill
    board_mark = gp(*inland(bx, bz, 150))
    marks = {
        "arrive": [150, 520],
        "board": r(board_mark), "sankichi": r(gp(*inland(bx + 0.514 * 110, bz + 0.857 * 110, 150))),
        "hens": r(gp(YARD["x0"] - 110, 230)),
        "shop": r(shop_door),
        "boat": r(gp(*inland(BIGBOAT["stern"][0] - 0.514 * 150, BIGBOAT["stern"][1] - 0.857 * 150, 520))),
        "underboat": r(gp(*inland(BIGBOAT["stern"][0], BIGBOAT["stern"][1], 300))),
        "racks": r(gp(RACKS[0]["x"] + 130, RACKS[0]["z"] - 150)),
        "gonroku": r(gp(*inland(TENDER["stern"][0] + 0.514 * 150, TENDER["stern"][1] + 0.857 * 150, 260))),
        "cherry": r(gp(street_x(2500, -0.5), 2500)),
        "clerkFrom": r(gp(street_x(2550), 2550)), "clerkTo": r(gp(street_x(60), 60)),
        "east": r(gp(street_x(40), 40)), "west": r(gp(street_x(2580), 2580)),
        "well": r(gp(wx + 110, wz - 80)),
        "masa": r(gp(RACKS[0]["x"] + 60, RACKS[0]["z"] - 90)),
        "kihei_out": r(gp(*inland(front_x(SHOP["z0"]) - 60, SHOP["z0"] - 40, 300))),
        "tokuzo_talk": r(gp(street_x(900, 0.3), 900)),
    }
    faces = {"arrive": "S", "board": "N", "sankichi": "W", "hens": "E", "shop": "E", "boat": "W", "underboat": "W", "racks": "N", "gonroku": "N",
             "cherry": "N", "clerkFrom": "S", "clerkTo": "N", "east": "N", "west": "S", "well": "W", "masa": "S", "kihei_out": "W", "tokuzo_talk": "S"}
    stands = {k: stand(v, faces[k]) for k, v in marks.items()}
    # three places for the family at the arrival, a step apart
    stands["arrive_mom"] = stand([150, 520], "S")
    stands["arrive_bigsis"] = stand([196, 538], "S")
    stands["arrive_lilsis"] = stand([112, 548], "S")

    # ---- the cut-outs, back to front, with their bases and states
    shop_gable = info.get("shop_gable")
    planes_out = [
        {"id": "ship", "file": "ship.png", "plane": "back", "what": "Gonroku's freighter at anchor far out (it rides: fx ship-bob)"},
        {"id": "racks", "file": "racks.png", "base": int(round(gp(RACKS[0]["x"], RACKS[0]["z"] - 10)[1])), "what": "the nets drying on their bamboo racks; people on the beach beyond pass behind them"},
        {"id": "tender", "file": "tender.png", "base": int(round(gp(*inland(TENDER["stern"][0], TENDER["stern"][1], 120))[1])), "what": "Gonroku's small boat, its stern in the water"},
        {"id": "board", "file": "board.png", "base": int(round(gp(*inland(bx, bz, 60))[1])), "what": "the notice-board place: posts, roof and the row of boards; people on the beach pass behind it"},
        {"id": "noren", "file": "noren.png", "base": int(round(gp(front_x(SHOP["z0"]), SHOP["z0"])[1])) + 2, "what": "Kihei's noren in the open front (it stirs: fx noren-sway); whoever goes in passes behind it"},
        {"id": "boat", "file": "boat.png", "base": int(round(gp(*inland(BIGBOAT["stern"][0], BIGBOAT["stern"][1], 180))[1])), "what": "the big boat on its props, bottom left; the beach between it and the water is behind it"},
        {"id": "fence", "file": "fence.png", "base": int(round(gp(YARD["x0"], YARD["z1"])[1])) + 1, "what": "the hen yard's bamboo fence; the hens (fx hens-*) and anyone at the shop are behind it"},
        {"id": "front", "file": "front.png", "plane": "front", "what": "a coil of rope and three net floats at the very front, bottom left"},
        # PAINT-23A (round twenty-three): the near plane, in front of everybody
        {"id": "near", "file": "near.png", "plane": "front", "what": "the near plane (DEPTH.md): the black pine's trunk up the left side and its boughs across the top left, a bough of the next pine in the top right, the bank's lip of grasses along the bottom"},
    ]
    cutouts = {p["id"]: box_of(planes[p["id"]][1]) for p in planes_out}

    # ---- things (ROUND-20's list, each with a shape)
    fuji_box = [60, 70, 560, 232]
    things = [
        {"id": "fuji", "what": "Mount Fuji across the bay, white well down its flanks", "shape": {"rect": fuji_box}, "stand": [330, 470], "face": "N"},
        {"id": "bay", "what": "Suruga Bay", "shape": {"poly": [[0, 302], [560, 302], [700, 330], [760, 320], [700, 345], [420, 365], [260, 388], [130, 410], [0, 442]]}, "stand": [300, 460], "face": "N"},
        {"id": "ship", "what": "Gonroku's freighter at anchor, its sail furled", "shape": {"rect": box_of(planes["ship"][1], 3)}, "stand": [300, 460], "face": "N"},
        {"id": "boats", "what": "the boats pulled up on their props", "shape": {"rect": box_of(planes["boat"][1], 2)}, "stand": marks["boat"], "face": "W"},
        {"id": "underboat", "what": "the gap under the big boat, between its props", "shape": {"rect": [cutouts["boat"][0] + 30, cutouts["boat"][1] + cutouts["boat"][3] - 28, 90, 26]}, "stand": marks["underboat"], "face": "W"},
        {"id": "nets", "what": "the nets drying on bamboo racks", "shape": {"rect": box_of(planes["racks"][1], 2)}, "stand": marks["racks"], "face": "N"},
        {"id": "board", "what": "the notice-board place: a row of boards under a little roof, dense with writing", "shape": {"rect": box_of(planes["board"][1], 2)}, "stand": marks["board"], "face": "N"},
        {"id": "roofs", "what": "the village's roofs: shingles weighted with stones, a few of thatch", "shape": {"rect": [520, 318, 110, 58]}, "stand": marks["well"], "face": "N"},
        {"id": "smoke", "what": "smoke from a kitchen", "shape": {"rect": [556, 262, 40, 62]}, "stand": marks["well"], "face": "E"},
        {"id": "hens", "what": "the hens in their yard, every one facing west", "shape": {"rect": [540, 505, 250, 75]}, "stand": marks["hens"], "face": "E"},
        {"id": "fence", "what": "the hen yard's low bamboo fence", "shape": {"rect": box_of(planes["fence"][1], 2)}, "stand": marks["hens"], "face": "E"},
        {"id": "cherry", "what": "the cherry by the shrine path, past its best", "shape": {"rect": info.get("cherry_box", [642, 214, 84, 76])}, "stand": marks["cherry"], "face": "N"},
        {"id": "shrinepath", "what": "the shrine path going up the slope", "shape": {"rect": [704, 206, 92, 94]}, "stand": marks["cherry"], "face": "N"},
        {"id": "gulls", "what": "gulls over the bay", "shape": {"rect": [0, 180, 460, 110]}, "stand": [300, 460], "face": "N"},
        {"id": "shop", "what": "Kihei's fish shop: its open front and the noren (the way in)", "shape": {"poly": [r(p) for p in shop_gable]} if shop_gable else {"rect": [600, 330, 200, 140]}, "stand": marks["shop"], "face": "E"},
        {"id": "road", "what": "the Tokaido, running along behind the beach", "shape": {"poly": [r(gp(street_x(z, 1), z)) for z in (60, 800, 2600)] + [r(gp(street_x(z, -1), z)) for z in (2600, 800, 60)]}, "stand": marks["clerkTo"], "face": "N"},
        {"id": "pass", "what": "the Satta pass: the headland at the end of the shore, the road climbing it", "shape": {"poly": [[520, 300], [600, 262], [680, 214], [750, 180], [800, 166], [800, 300]]}, "stand": marks["west"], "face": "N"},
        {"id": "well", "what": "the well", "shape": {"rect": [int(round(gp(wx - 60, wz)[0])), int(round(gp(wx, wz, 262)[1])), int(round(120 * kz(wz))), int(round(gp(wx, wz)[1] - gp(wx, wz, 262)[1]))]}, "stand": marks["well"], "face": "W"},
        {"id": "sand", "what": "the beach: grey sand and pebbles", "shape": {"poly": [[0, 460], [120, 440], [300, 420], [440, 400], [500, 430], [360, 470], [300, 500], [250, 540], [230, 596], [0, 596]]}, "stand": [300, 500], "face": "S"},
    ]
    # the people (drawn by the game): each a rect at their place, by ROUND-20's list
    def person_rect(p, cm):
        px_ = 160 * (p[1] - HZ) / (FULL - HZ) * cm / 175.0
        return [int(round(p[0] - px_ * 0.16)), int(round(p[1] - px_)), int(round(px_ * 0.32)), int(round(px_))]
    things += [
        {"id": "sankichi", "what": "Sankichi, 9, beside the board (drawn by the game)", "shape": {"rect": person_rect(marks["sankichi"], 125)}, "stand": marks["board"], "face": "E"},
        {"id": "tokuzo", "what": "Tokuzo, the headman's clerk, on his rounds along the street (drawn by the game)", "shape": {"rect": person_rect(marks["tokuzo_talk"], 156)}, "stand": [marks["tokuzo_talk"][0] - 40, marks["tokuzo_talk"][1] + 12], "face": "E"},
        {"id": "gonroku", "what": "Gonroku, the captain, by his boat at the water's edge (drawn by the game)", "shape": {"rect": person_rect(marks["gonroku"], 156)}, "stand": [marks["gonroku"][0] + 44, marks["gonroku"][1] + 10], "face": "W"},
        {"id": "masa", "what": "O-Masa at the net racks (drawn by the game)", "shape": {"rect": person_rect(marks["masa"], 146)}, "stand": marks["racks"], "face": "N"},
        {"id": "kihei", "what": "Kihei, out in front of his shop (drawn by the game)", "shape": {"rect": person_rect(marks["kihei_out"], 156)}, "stand": marks["shop"], "face": "E"},
        {"id": "netmender", "what": "a villager mending a net by the racks (drawn by the game)", "shape": {"rect": person_rect([262, 452], 156)}, "stand": [226, 466], "face": "E"},
        {"id": "basketwoman", "what": "a woman with a basket on the street (drawn by the game)", "shape": {"rect": person_rect([392, 444], 146)}, "stand": [356, 458], "face": "E"},
    ]
    stands["netmender"] = stand([262, 452], "W")
    stands["basketwoman"] = stand([392, 444], "E")
    # ---- fx: what moves (the engine draws it)
    yard_poly = [r(gp(YARD["x0"] + 20, YARD["z0"] + 10)), r(gp(YARD["x1"], YARD["z0"] + 10)), r(gp(YARD["x1"], YARD["z1"] - 15)), r(gp(YARD["x0"] + 20, YARD["z1"] - 15))]
    shore_pts = [r(gp(shore_x(z) - 40, z)) for z in np.geomspace(20000, 1100, 10)]
    bay_poly = [[0, 303], [540, 303], [660, 322], [740, 318], [700, 332]] + shore_pts + [[0, shore_pts[-1][1] + 6]]
    import edo_village_hens as HENS
    hen_frames = HENS.frames_block
    fx = [
        {"id": "bay-shimmer", "type": "shimmer", "what": "the morning light on the bay: a few glints that come and go", "poly": bay_poly, "count": 36, "size": 5, "flow": [3, 0], "life": 1.8,
         "color": "#f6eed8", "opacity": 0.5, "plane": "back",
         "note": "The far rows of wave-curls are painted still (beyond about a kilometre nothing moves at this size); the near water is bands only, and this moves on it"},
        {"id": "shore-ripples", "type": "ripples", "what": "the wash at the water's edge by Gonroku's tender", "at": r(gp(shore_x(1700) - 30, 1700)), "radius": [2, 12], "flat": 0.22,
         "every": [1.6, 3.4], "rings": 1, "speed": 9, "color": "#f6eed8", "trough": "#2e3a93", "opacity": 0.4, "plane": "back"},
        {"id": "ship-bob", "type": "bob", "plane": "ship", "amount": 1, "period": 6, "what": "Gonroku's freighter riding at anchor"},
        {"id": "tender-bob", "type": "bob", "plane": "tender", "amount": 1, "period": 5, "tilt": 1.0, "what": "the tender nodding where its stern lies in the water"},
        {"id": "noren-sway", "type": "sway", "plane": "noren", "anchor": "top", "amount": 2.5, "period": 3.2, "wave": 30, "lean": 0.35, "what": "the noren lifting in the wind off the bay"},
        {"id": "kitchen-smoke", "type": "smoke", "plane": "back", "what": "smoke from a kitchen in the village, beyond the shop", "at": [574, 322], "height": 58, "width": [2, 11], "lean": [16, -58],
         "rise": 9, "rate": 2.5, "gust": 0.3, "color": "#e4e6ea", "opacity": 0.3},
        {"id": "gulls", "type": "birds", "kind": "flyers", "plane": "back", "what": "gulls over the bay (the engine's own silhouettes: no frames)", "lanes": [[[-12, 262], [160, 236], [340, 250], [520, 228], [640, -12]],
         [[-12, 206], [120, 222], [300, 200], [470, 212], [560, 300]], [[600, 240], [420, 262], [220, 248], [-12, 270]]], "every": [7, 15], "group": [1, 3], "speed": 60, "size": 8, "scale": [0.6, 1.1], "color": "#f6eed8"},
        {"id": "petals", "type": "petals", "what": "petals falling from the cherry by the shrine path (ENGINE-20's kind): few, far and small", "area": [[650, 218], [726, 218], [736, 290], [660, 290]],
         "count": 6, "size": 1.5, "color": "#e6a5b8", "plane": "back", "note": "They fall on the ground under the tree: the drift painted there is their bed"},
    ]
    # the hens: five, in a row inside the fence, each on a short perch of her own (so none stands in another), all facing
    # west (right); they stand, look, peck and shuffle, and never turn or fly. Little Sister names them (#24).
    names = ["Komachi", "Oume", "Tora", "Kiku", "Cho"]
    sets = ["brown", "speckled", "brown", "speckled", "brown"]
    spots = [(300, 95), (390, 170), (436, 110), (520, 250), (420, 290)]      # all within the picture (the yard runs off its right edge)
    for i, (nm, st, (hx, hz)) in enumerate(zip(names, sets, spots)):
        a_, b_ = gp(hx - 35, hz), gp(hx + 35, hz)
        fx.append({"id": f"hen-{i + 1}", "type": "birds", "kind": "flock", "what": f"a hen in the yard ({st}), facing west with the others (Little Sister calls her {nm})",
                   "perch": [r(a_), r(b_)], "count": 1, "frames": hen_frames(st), "depth": True, "shy": 0, "fly": False, "turn": False, "walk": 5,
                   "moves": {"stand": 3, "look": 1.5, "peck": 2.5, "walk": 0.6, "turn": 0}, "seed": i + 1,
                   "note": "frames painted facing right (east on the stage is west along this coast: the street runs south-west); peck is the beak to the ground and the head coming back up to face west again"})
    out = {
        "id": "edo-village", "horizon": HZ, "full": FULL,
        "view": {"horizon": HZ, "full": FULL, "camera": "persp.Camera(300, 590): eye 317 cm, Z0 875, focal 800, vanishing x 400", "street": "x = -400 + 0.6 z (cm), half width 175; shore x = -1700 + 0.6 z; fronts x = -50 + 0.6 z; the street 30 cm above the beach"},
        "light": "early morning, the sun in the east, behind us and to the left, 30 degrees up: faces toward us and the left are lit; shadows fall to the right and away, flat and blue",
        "walk": walk, "walk_note": "one area: the beach and the street (the street a little higher than the beach, joined by a sand slope: no second floor); the hen yard, the shop and the water are outside it",
        "blocked": blocked,
        "planes": planes_out, "cutouts": cutouts,
        "things": things,
        "marks": marks, "stands": stands,
        "door": {"at": [150, 462], "r": 62, "kind": "portal", "what": "the door in time the three come out of, on the beach at `arrive`: a walk-in door, its middle a metre over their feet (as the roadside's coin door, bigger)"},
        "fx": fx,
        "fx_note": "the waves near the shore are the shimmer on the bands (no frames: say so to ENGINE-20 if a wave kind arrives); the ship and the tender bob; the noren sways; the smoke, the gulls (engine-drawn) and the petals (ENGINE-20's kind) are marks; the hens are a flock of five, each her own, on painted frames (edo_village_hens.py)",
        "heights": {"mom_cm": 168, "bigsis_cm": 160, "lilsis_cm": 122, "man_1830_cm": 156, "woman_1830_cm": 146, "sankichi_cm": 125, "grownup_at_full_px": 160},
    }
    return out

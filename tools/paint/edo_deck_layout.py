"""PAINT-21B: layout.json for edo-deck, measured through the scene's camera from the same numbers the picture was
painted with (edo_deck_kit.py), and from the finished cut-outs' pixels."""

import math

import numpy as np

from edo_deck_kit import *

MARKS_21 = ["deck", "bow", "mast", "hearth", "kota", "windlass", "kako1", "kako2", "denzo", "seijiro", "tiller", "compass", "kanbei", "rail"]
THINGS_21 = ["sail", "yard", "mast", "rings", "maststep", "windlass", "hold", "bales", "casks", "boat", "hearth", "pot", "tiller", "rudder",
             "compassbox", "deckhouse", "bow", "sea", "cape", "cask", "gulls", "spray",
             "gonroku", "kanbei", "denzo", "seijiro", "kota", "kako1", "kako2"]


def r(p):
    return [int(round(p[0])), int(round(p[1]))]


def rc(p):
    """A picture point, rounded and kept on the stage."""
    return [int(min(798, max(2, round(p[0])))), int(min(598, max(2, round(p[1]))))]


def box_of(alpha, pad=0):
    ys, xs = np.where(alpha > 0.5)
    if len(ys) == 0:
        return [0, 0, 0, 0]
    return [int(xs.min()) - pad, int(ys.min()) - pad, int(xs.max() - xs.min()) + 1 + 2 * pad, int(ys.max() - ys.min()) + 1 + 2 * pad]


def wpoly(pts):
    """World (x, z) points on the deck -> picture points kept on the stage."""
    return [rc(gp(x_, z_)) for x_, z_ in pts]


def stand(p, face="N"):
    x, y = p
    return {"at": [int(round(x)), int(round(y))], "grownup_px": int(round(160 * (y - HZ) / (FULL - HZ))), "face": face}


def person_rect(p, cm):
    px_ = 160 * (p[1] - HZ) / (FULL - HZ) * cm / 175.0
    return [int(round(p[0] - px_ * 0.17)), int(round(p[1] - px_)), int(round(px_ * 0.34)), int(round(px_))]


def sea_poly(info, step=4):
    """The sea as it is seen in the backdrop: from the horizon down to whatever stands in front of it (the cargo, the
    boat, the bulwark, the stem, the deckhouse), column by column."""
    m = info["ship_mask"] > 0.35
    top, bottom = [], []
    for x in list(range(0, W, step)) + [W - 1]:
        y0 = HZ + 1
        y = y0
        while y < H - 1 and not m[y, x]:
            y += 1
        top.append([x, y0])
        bottom.append([x, max(y0 + 1, y - 1)])
    return top + bottom[::-1]


def layout(planes, info):
    # ---- the walk: the near walkway from the bow to the stern, the mast's gangway, the bow's deck, the stern's deck
    # behind the aft hold (round the windlass, the tiller and the compass's post: blocked); the near side is cut away
    outline = [(-470, -24), (430, -24), (512, 140), (498, 300), (498, 512), (182, 512), (182, 156), (-36, 156), (-36, 322),
               (-204, 322), (-204, 156), (-416, 156), (-418, 300), (-462, 286), (-472, 214), (-466, 120), (-455, 60)]
    walk = wpoly(outline)
    blocked = []
    s = STEP
    blocked.append(wpoly([(s["x0"] - 8, s["z0"] - 7), (s["x1"] + 8, s["z0"] - 7), (s["x1"] + 8, s["z1"] + 8), (s["x0"] - 8, s["z1"] + 8)]))
    h = HEARTH
    blocked.append(wpoly([(h["x0"] - 8, h["z0"] - 8), (h["x1"] + 8, h["z0"] - 8), (h["x1"] + 8, h["z1"] + 24), (h["x0"] - 8, h["z1"] + 24)]))
    b = BALE
    blocked.append(wpoly([(b["x0"] - 8, b["z"] - 16), (b["x1"] + 8, b["z"] - 16), (b["x1"] + 8, b["z"] + 24), (b["x0"] - 8, b["z"] + 24)]))
    w = WINDLASS
    blocked.append(wpoly([(w["x"] - w["r"] - 8, w["z0"] - 30), (w["x"] + w["r"] + 8, w["z0"] - 30), (w["x"] + w["r"] + 8, w["z1"] + 30), (w["x"] - w["r"] - 8, w["z1"] + 30)]))
    c = COMPASS
    blocked.append(wpoly([(c["x"] - 18, c["z"] - 18), (c["x"] + 18, c["z"] - 18), (c["x"] + 18, c["z"] + 18), (c["x"] - 18, c["z"] + 18)]))
    t, rd = TILLER, RUDDER
    blocked.append(wpoly([(t["x0"] - 8, t["z0"] - 10), (rd["x0"], rd["z0"] - 6), (rd["x1"] + 10, rd["z0"] - 6), (rd["x1"] + 10, rd["z1"] + 8),
                          (rd["x0"], rd["z1"] + 8), (t["x0"] - 8, t["z0"] + 12)]))
    blocked.append(wpoly([(-470, -30), (-338, -30), (-338, 22), (-470, 22)]))                  # the coil of rope at the front
    blocked.append(wpoly([(-326, -30), (-276, -30), (-276, -6), (-326, -6)]))                  # the bucket
    blocked.append(wpoly([(430, -30), (520, -30), (520, 14), (430, 14)]))                      # the water cask (at the edge)

    # ---- marks (ROUND-21's names, and a few more), in world (x, z), then the picture
    M = {
        "deck": (0, 40), "bow": (-430, 118), "mast": (-150, 170), "hearth": (-212, 62), "kota": (-374, 112),
        "windlass": (300, 262), "kako1": (198, 300), "kako2": (352, 498), "denzo": (-50, 178), "seijiro": (78, 82),
        "tiller": (452, 150), "compass": (382, 108), "kanbei": (262, 112), "rail": (430, 474),
        "deck_bigsis": (-62, 22), "deck_lilsis": (58, 16),
    }
    marks = {k: r(gp(*v)) for k, v in M.items()}
    faces = {"deck": "N", "bow": "W", "mast": "N", "hearth": "N", "kota": "E", "windlass": "N", "kako1": "E", "kako2": "W", "denzo": "W",
             "seijiro": "S", "tiller": "N", "compass": "N", "kanbei": "E", "rail": "N", "deck_bigsis": "N", "deck_lilsis": "N"}
    stands = {k: stand(v, faces[k]) for k, v in marks.items()}

    # ---- the cut-outs, back to front, with their bases and states
    def row(z_):
        return int(round(row_of(z_)))
    mast_base = row(MAST["z"] - MAST["r"])
    tiller_base = [r(gp(t["x0"], t["z0"] + 6)), r(gp(rd["x1"], rd["z0"]))]
    planes_out = [
        {"id": "swell", "file": "swell.png", "plane": "back", "what": "the far sea and the cape of Daiozaki on the horizon: it rocks a pixel or two on the long swell (fx swell)"},
        {"id": "sail", "file": "sail.png", "plane": "back", "what": "the great sail on its yard, filling (fx sail-breath)"},
        {"id": "rigging", "file": "rigging.png", "plane": "back", "what": "the sheets, the brace and a lift: ropes from the sail and the yard down to the deck"},
        {"id": "mast", "file": "mast.png", "base": mast_base, "what": "the mast, iron-ringed, from its step out of the picture's top; whoever stands behind its step passes behind it"},
        {"id": "windlass", "file": "windlass.png", "base": row(w["z0"] - 22), "what": "the windlass at the stern: its drum, cheek posts and two bars"},
        {"id": "tiller", "file": "tiller.png", "base": tiller_base, "what": "the long tiller and the rudder's head: whoever is beyond the tiller passes behind it"},
        {"id": "compass", "file": "compass-shut.png", "base": row(c["z"] - 10), "states": {"shut": "compass-shut.png", "open": "compass-open.png"},
         "what": "the compass box on its post by the helm: the lid shut; propped open (then the card's white shows: the close-up edo-compass opens from it)"},
        {"id": "pot", "file": "pot.png", "base": row(h["z0"]), "states": {"lid": "pot.png", "lifted": "pot-lifted.png", "steam": "pot-steam.png"},
         "what": "Kota's rice pot in the hearth box: the lid on; the lid lifted (the rice showing, half raw); boiling, the lid on, starch run down under it (with fx pot-steam)"},
        {"id": "front", "file": "front.png", "plane": "front", "what": "the nearest things on the walkway at the picture's bottom corners: a coil of rope and a bucket (left), a water cask (right edge)"},
    ]
    cutouts = {p["id"]: box_of(planes[p["file"][:-4]][1]) for p in planes_out}
    for st in ("compass-open", "pot-lifted", "pot-steam"):
        cutouts[st] = box_of(planes[st][1])

    # ---- things (ROUND-21's list, each with a shape)
    from edo_deck import sail_geometry, SWELL_ROWS, SKY_UNDER
    outline_s, yard, leech, foot, seam_x = sail_geometry()
    sail_poly = [rc(p) for p in outline_s]
    yard_poly = [r((p[0], p[1] - 9)) for p in yard] + [r((p[0], p[1] + 9)) for p in yard[::-1]]
    yard_poly = [[min(798, max(2, x)), min(598, max(2, y))] for x, y in yard_poly]
    mb = box_of(planes["mast"][1])
    mast_rect = [mb[0] - 3, 2, mb[2] + 6, 290]
    rings_rect = [mb[0] - 3, 292, mb[2] + 6, mb[1] + mb[3] - 292]
    step_poly = [r(gp(s["x0"], s["z0"])), r(gp(s["x1"], s["z0"])), r(gp(s["x1"], s["z1"])), r(gp(s["x1"], s["z1"], s["h"])), r(gp(s["x0"], s["z1"], s["h"])), r(gp(s["x0"], s["z0"], s["h"]))]
    hold_xs, hold_at, prof = info["holds"]["aft"]
    hold_poly = [r(P3(hold_at(x_, 6))) for x_ in hold_xs[::3]] + [r(gp(x_, WALK_Z)) for x_ in hold_xs[::-3]]
    fwd_xs, fwd_at, _ = info["holds"]["fwd"]
    xe = HOLD_F[1]
    stack = [r(P3(fwd_at(xe, i))) for i in range(len(prof))] + [r(gp(xe, far_z(xe) - 30)), r(gp(xe, WALK_Z))]
    bales_poly = stack
    cask_heads = info.get("cask_heads") or []
    if cask_heads:
        xs_ = [p[0] for p in cask_heads]
        ys_ = [p[1] for p in cask_heads]
        casks_rect = [int(min(xs_)) - 10, int(min(ys_)) - 14, int(max(xs_) - min(xs_)) + 20, int(max(ys_) - min(ys_)) + 28]
    else:
        casks_rect = [255, 470, 30, 40]
    bt = BOAT
    boat_rect = [int(round(gp(bt["x0"], bt["z"])[0])) - 4, int(round(gp(0, bt["z"], CARGO_TOP + bt["h"] + 4)[1])),
                 int(round(gp(bt["x1"], bt["z"])[0] - gp(bt["x0"], bt["z"])[0])) + 8,
                 int(round(gp(0, bt["z"] - bt["beam"] / 2, CARGO_TOP - 10)[1] - gp(0, bt["z"], CARGO_TOP + bt["h"] + 4)[1]))]
    hearth_poly = [r(gp(h["x0"], h["z0"])), r(gp(h["x1"], h["z0"])), r(gp(h["x1"], h["z1"])), r(gp(h["x1"] - 4, h["z1"] + 22, h["h"] + 58)),
                   r(gp(h["x0"] + 4, h["z1"] + 22, h["h"] + 58)), r(gp(h["x0"], h["z0"], h["h"]))]
    pb = box_of(np.maximum(planes["pot"][1], planes["pot-lifted"][1]), 3)
    tb = box_of(planes["tiller"][1])
    rud = [int(round(gp(rd["x0"], rd["z0"])[0])), int(round(gp(rd["x0"], rd["z0"], rd["h"])[1])), 0, 0]
    rud[2] = int(round(gp(rd["x1"], rd["z0"])[0])) - rud[0]
    rud[3] = int(round(gp(rd["x0"], rd["z0"])[1])) - rud[1]
    rud[2] = min(rud[2], 798 - rud[0])
    tiller_rect = [tb[0], tb[1], max(10, rud[0] - tb[0]), tb[3]]
    cb = box_of(np.maximum(planes["compass-shut"][1], planes["compass-open"][1]), 4)
    ho = HOUSE
    house_poly = [rc(gp(ho["x0"], ho["z1"])), rc(gp(ho["x0"], ho["z0"])), rc(gp(ho["x1"], ho["z0"])), rc(gp(ho["x1"], ho["z0"], ho["h"])),
                  rc(gp(ho["x1"], ho["z1"], ho["h"] + 34)), rc(gp(ho["x0"] - 26, ho["z1"], ho["h"] + 34)), rc(gp(ho["x0"] - 26, ho["z0"] - 26, ho["h"]))]
    stem_box = box_of(info["stem_mask"])
    sea = sea_poly(info)
    things = [
        {"id": "sail", "what": "the great sail: woven cotton in vertical bolts (the Takasago captain's sail), filling", "shape": {"poly": sail_poly}, "stand": marks["deck"], "face": "N"},
        {"id": "yard", "what": "the yard the sail hangs from (the masthead out of the picture above)", "shape": {"poly": yard_poly}, "stand": marks["windlass"], "face": "N"},
        {"id": "mast", "what": "the mast, built up and bound with iron rings, nine-tenths of the hull's length", "shape": {"rect": mast_rect}, "stand": marks["mast"], "face": "N"},
        {"id": "rings", "what": "the iron rings round the mast", "shape": {"rect": rings_rect}, "stand": marks["mast"], "face": "N"},
        {"id": "maststep", "what": "the mast step: a block of timber at the mast's foot, the Funadama sealed in it, the plug nailed", "shape": {"poly": step_poly}, "stand": marks["mast"], "face": "N"},
        {"id": "windlass", "what": "the windlass that hauls the yard up: a drum, two bars", "shape": {"rect": box_of(planes["windlass"][1], 2)}, "stand": marks["windlass"], "face": "N"},
        {"id": "hold", "what": "the hold: no deck over it, the cargo heaped under straw mat covers, lashed", "shape": {"poly": hold_poly}, "stand": marks["deck"], "face": "N"},
        {"id": "bales", "what": "the cargo's end at the gangway: bales of straw stacked, a cask or two among them", "shape": {"poly": bales_poly}, "stand": marks["mast"], "face": "W"},
        {"id": "casks", "what": "casks in the stack (a mixed lot)", "shape": {"rect": casks_rect}, "stand": marks["mast"], "face": "W"},
        {"id": "boat", "what": "the ship's boat, lashed upside down on the forward mats", "shape": {"rect": boat_rect}, "stand": marks["hearth"], "face": "N"},
        {"id": "hearth", "what": "Kota's hearth box: a wooden box lined with clay, its lid propped", "shape": {"poly": hearth_poly}, "stand": marks["hearth"], "face": "W"},
        {"id": "pot", "what": "the rice pot in the hearth box (its lid)", "shape": {"rect": pb}, "stand": marks["hearth"], "face": "W"},
        {"id": "tiller", "what": "the long tiller, Gonroku's", "shape": {"rect": tiller_rect}, "stand": marks["tiller"], "face": "N"},
        {"id": "rudder", "what": "the rudder's head, coming up through the stern (the huge blade under the overhang)", "shape": {"rect": rud}, "stand": marks["tiller"], "face": "E"},
        {"id": "compassbox", "what": "the compass box on its post: the ship's clock (opens the close-up edo-compass)", "shape": {"rect": cb}, "stand": marks["compass"], "face": "N"},
        {"id": "deckhouse", "what": "the stern deckhouse over the overhang", "shape": {"poly": house_poly}, "stand": marks["rail"], "face": "E"},
        {"id": "bow", "what": "the bow: the single heavy stem timber rising", "shape": {"rect": [0, stem_box[1], stem_box[0] + stem_box[2] + 6, stem_box[3]]}, "stand": marks["bow"], "face": "W"},
        {"id": "sea", "what": "the sea in rows, the Kumano-nada ahead", "shape": {"poly": sea}, "stand": marks["deck"], "face": "N"},
        {"id": "cape", "what": "Daiozaki: a far grey cape off the starboard bow", "shape": {"poly": [[2, HZ - 22], [120, HZ - 22], [240, HZ - 10], [268, HZ + 3], [2, HZ + 3]]}, "stand": marks["bow"], "face": "N"},
        {"id": "cask", "what": "the floating cask, set adrift for Konpira, bobbing past now and then (a flyer: fx cask); its band of sea", "shape": {"rect": [2, 338, 796, 24]}, "stand": marks["deck"], "face": "N"},
        {"id": "gulls", "what": "gulls over the ship (fx gulls)", "shape": {"rect": [2, 120, 330, 110]}, "stand": marks["deck"], "face": "N"},
        {"id": "spray", "what": "spray over the bow now and then (fx bow-spray)", "shape": {"rect": [2, 300, 70, 80]}, "stand": marks["bow"], "face": "W"},
    ]
    people = {"gonroku": ("tiller", 158, "Gonroku, the master, at the tiller"), "kanbei": ("kanbei", 156, "Kanbei, the omote, by the compass box"),
              "denzo": ("denzo", 160, "Denzo, the oyaji (bosun), by the mast step"), "seijiro": ("seijiro", 156, "Seijiro, the makanai (purser), on his bale with his abacus"),
              "kota": ("kota", 138, "Kota, the kashiki (the ship's boy cook), at his hearth box"),
              "kako1": ("kako1", 156, "a sailor leaning on the windlass's near bar"), "kako2": ("kako2", 156, "a sailor leaning on the windlass's far bar")}
    for pid, (mk, cm, what) in people.items():
        things.append({"id": pid, "what": what + " (drawn by the game)", "shape": {"rect": person_rect(marks[mk], cm)}, "stand": marks["deck"] if pid in ("seijiro", "denzo") else marks[mk], "face": faces[mk]})

    # ---- fx: what moves (the engine draws it; ENGINE-21 makes what is missing)
    bow_top = gp(BOW_X - 24, CL + 50, sheer(BOW_X) - 4)              # just over the bow's bulwark, beside the stem, at the stage's left edge
    fx = [
        {"id": "sea-rows", "type": "waves", "what": "the sea's rows running past the ship toward the stern (she goes left, the water goes right), fast",
         "area": sea, "toward": "E", "speed": 32, "rows": 16, "per": 20, "size": 13, "life": 2.6, "color": "#f6eed8", "opacity": 0.6, "plane": "back",
         "note": "the waves kind in one direction, faster than a bay's; drawn OVER the swell layer (so the far rows show on it) and under everything else; the area is the sea as seen in the backdrop (it stops at the cargo, the boat, the bulwark, the stem and the deckhouse)"},
        {"id": "swell", "type": "bob", "plane": "swell", "amount": 1, "period": 9, "tilt": 0.25,
         "what": "the long slow swell: the far sea and the cape rise and fall and the horizon tilts a pixel or two",
         "note": "the swell layer covers rows %d-%d (the cape above the horizon, the far sea below it); the backdrop's sky runs %d rows below the horizon under it, so the horizon can drop; its lower edge lies in a flat band of the sea, so a pixel or two of travel shows no seam" % (SWELL_ROWS[0], SWELL_ROWS[1], SKY_UNDER)},
        {"id": "sail-breath", "type": "sway", "plane": "sail", "anchor": "top", "at": 0, "amount": 1.5, "period": 4.6, "wave": 260, "lean": 0.15,
         "what": "the sail breathing in the wind: its foot and leech stir a pixel or two",
         "note": "a sway from the top edge (the yard is out of the picture at the left); ENGINE-21 may give it a breathing kind of its own (the foot's middle bellying out and back): the sky is painted complete under it"},
        {"id": "bow-spray", "type": "spray", "at": rc(bow_top), "every": [5, 11], "height": 54, "width": 40, "lean": [26, -10], "drops": 26, "base": int(round(row_of(CL))),
         "color": "#f6eed8", "opacity": 0.75, "plane": "back",
         "what": "spray flung up over the bow now and then, blown aft (to the right) and away",
         "note": "a new small kind (ENGINE-21): a burst of white drops rising from `at` and falling back, `lean` the wind's push; until then a short smoke puff in white will stand for it"},
        {"id": "cask", "type": "birds", "kind": "flyers", "what": "the floating cask (nagashi-daru) bobbing past on the sea now and then, toward the stern",
         "lanes": [[[-30, 352], [830, 352]]], "every": [55, 95], "group": [1, 1], "speed": 40, "frames": {"glide": ["cask-1.png", "cask-2.png", "cask-3.png"], "flap": ["cask-1.png", "cask-2.png", "cask-3.png"]},
         "scale": 1, "clip": sea, "plane": "back",
         "note": "a flyer that floats: its frames (40 x 26, the waterline's middle at (20, 19)) bob in turn; it stays on its lane (no rise and fall but the frames'), hidden where the cargo and the bulwark stand (clip)"},
        {"id": "gulls", "type": "birds", "kind": "flyers", "plane": "back", "what": "gulls over the ship (the engine's own silhouettes, white as Yui's)",
         "lanes": [[[-12, 176], [120, 160], [260, 184], [420, 212], [600, 222], [812, 210]], [[812, 24], [770, 64], [730, 120], [600, 236], [300, 246], [-12, 214]]],
         "every": [8, 16], "group": [1, 2], "speed": 64, "size": 9, "scale": [0.7, 1.1], "color": "#f4f1e6", "behind": [sail_poly],
         "note": "white against the cobalt and cerulean of the sky; they fly beyond the sail and the mast (hidden behind the sail: `behind`)"},
        {"id": "hearth-embers", "type": "embers", "at": r(gp(POT["x"], POT["z"] - 2, HEARTH["h"] - 1)), "size": [6, 2], "glowOpacity": 0.16, "plane": "pot",
         "what": "the charcoal under the rice pot, in the hearth box's mouth"},
        {"id": "hearth-smoke", "type": "smoke", "at": r(gp(POT["x"] - 22, POT["z"] + 10, HEARTH["h"] + 2)), "height": 46, "width": [2, 10], "lean": [26, -46], "rise": 10,
         "rate": 1.6, "color": "#e4e6ea", "opacity": 0.22, "base": int(round(row_of(HEARTH["z0"]))), "what": "a thread of smoke from the hearth box, blown away and aft"},
        {"id": "pot-steam", "type": "smoke", "at": r(gp(POT["x"], POT["z"], HEARTH["h"] + 14)), "height": 40, "width": [3, 14], "lean": [18, -40], "rise": 14,
         "rate": 3.0, "color": "#f6eed8", "opacity": 0.38, "base": int(round(row_of(HEARTH["z0"]))), "when": "the pot's state is steam",
         "what": "steam from the rice pot while it boils (with the pot's steam state)"},
    ]
    out = {
        "id": "edo-deck", "horizon": HZ, "full": FULL,
        "view": {"horizon": HZ, "full": FULL, "camera": "persp.Camera(262, 590): eye 359 cm over the deck, Z0 875, focal 800, vanishing x 400",
                 "ship": "keel across the picture, bow left (-x), stern right (+x); x 0 at the picture's middle; near side z -60 (cut away), far bulwark z 540, centreline z 240; the deck level"},
        "light": "noon, the sun high in the south (about 66 degrees), behind us and a little to the left (we face NNW across the ship, heading WSW): faces toward us, the left and up are lit; shadows short, away and a little right, flat and blue",
        "walk": walk, "walk_note": "one area: the near walkway from the bow to the stern (the near side is cut away, as a stage's fourth wall), the mast's gangway, the bow's deck forward of the hold, the stern's deck aft of it; the cargo, the far walkway and the deckhouse are outside it; the step, the hearth, the bale, the windlass, the compass's post, the tiller and the front things are blocked",
        "blocked": blocked,
        "planes": planes_out, "cutouts": cutouts,
        "things": things,
        "marks": marks, "stands": stands,
        "seats": {"seijiro": {"at": marks["seijiro"], "seat_cm": 42, "what": "Seijiro sits on the bale (its top 42 cm up), his feet at the mark"},
                  "kota": {"at": marks["kota"], "seat_cm": 0, "what": "Kota squats (or sits on his heels) at the hearth box's left, facing it"}},
        "fx": fx,
        "fx_note": "ENGINE-21 drives: the sea's rows (waves, toward the stern, fast), the swell (the swell layer on a slow bob with a tilt), the sail breathing (the sail layer), spray at the bow now and then (a new small kind), the floating cask (a flyer that floats: three frames), gulls (flyers); the hearth's embers and smoke, and the pot's steam when it boils. Nothing that moves is painted still.",
        "closeup": {"from": "compassbox", "scene": "edo-compass", "what": "the compass box's lid propped (state open) as the close-up opens; shut again when it closes"},
        "heights": {"mom_cm": 168, "bigsis_cm": 160, "lilsis_cm": 122, "man_1830_cm": 156, "kota_cm": 138, "grownup_at_full_px": 160},
    }
    return out

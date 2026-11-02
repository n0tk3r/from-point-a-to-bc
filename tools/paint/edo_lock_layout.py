"""The lock close-up's layout.json: the parts and their states, every thing's shape, the hand points. PAINT-21E.

  python3 edo_lock_layout.py      writes out/edo-lock/layout.json (edo_lock.py also calls write())"""

import json
import math
import os

import numpy as np

import edo_lock as EL
from edo_town_kit import hull, box_of

r = lambda q: [int(round(q[0])), int(round(q[1]))]


def write(path):
    cuts = EL.cut_layers()
    alpha = {k: v.a > 0.5 for k, v in cuts.items()}
    Q = EL.Q
    bw, bh = EL.BODY
    hole = Q(*EL.EARHOLE)
    post = Q(EL.POST[0], EL.POST[1])
    a, b, y = EL.SLITS
    slits = Q((a + b) / 2, y + 0.2)
    bolt = Q(0.0, EL.BOLT_Y)
    out = {"id": "edo-lock", "closeup": True, "horizon": 290, "full": 590,
           "light": "late afternoon: the low gold sun from the left, raking across the carving (every raised edge lit on its upper left, shaded on its "
                    "lower right); the lock's shadow falls down and to the right on the stile. Key: edo-sunset (PAINT-20E's).",
           "note": "A close-up: a whole-stage picture of the lock on the women's hall's doors, nobody standing in it, flat and frontal at 22 px to the "
                   "centimetre (the lock's body 21 x 10 cm is 462 x 220 px, its top-left at (204, 196)). Behind: the doors' lattice and the seam (x 176) "
                   "where the leaves meet; the hasp's plate and staple on the left leaf; slips on the stiles. The tiny walk patch at the bottom middle is "
                   "the Egypt car's way, until ENGINE-21's close-up mode makes it unneeded.",
           "scale_px_per_cm": EL.S}
    out["walk"] = [[410, 580], [450, 580], [450, 598], [410, 598]]
    out["walk_note"] = "nobody walks: a tiny patch for the lead to stand on, undrawn (egypt-car's way); not needed once the engine's close-up mode is in"
    out["blocked"] = []
    out["marks"] = {"default": [430, 590]}
    out["faces"] = {"default": "N"}
    out["stands"] = {"default": {"at": [430, 590], "grownup_px": 160, "floor": "none", "note": "undrawn"}}
    planes = [
        {"id": "wave", "file": "wave.png", "plane": "back", "what": "the middle wave, in place in its groove",
         "states": {"in": "wave.png", "slid": "wave-slid.png"}, "note": "slid: aside to the right, over the third wave's foot (3.6 cm), the recess and the post showing"},
        {"id": "ear", "file": "ear.png", "plane": "back", "what": "the long ear laid back along the rabbit's back, its tiny hole black with dust",
         "states": {"dusty": "ear.png", "clean": "ear-clean.png"}},
        {"id": "bolt", "file": "bolt.png", "plane": "back", "what": "the bolt through the staple", "states": {"in": "bolt.png", "out": "bolt-out.png"}},
    ]
    parts = [
        {"id": "post", "plane": "back", "what": "the square post in the recess (in the backdrop: seen when the wave is slid); with the coin on it "
                                                             "(post-coin.png), turned a quarter (post-turned.png: the groove across its end and the coin's marks turned)",
         "states": {"bare": None, "coin": "post-coin.png", "turned": "post-turned.png"}},
        {"id": "back", "plane": "back", "what": "along the rabbit's back, a carved line (the backdrop); opened, a row of thin slits (back-open.png)",
         "states": {"shut": None, "open": "back-open.png"}},
    ]
    out["planes"] = planes
    out["parts"] = parts
    out["parts_note"] = "the post and the back line are painted in the backdrop; their other states are the alts named (no cut-out of their own)"
    out["cutouts"] = {k: list(box_of(alpha[k])) for k in EL.CUTS + EL.ALTS}
    things = []

    def thing(id_, what, shape, **more):
        d = {"id": id_, "what": what, "shape": {"poly": shape}}
        d.update(more)
        things.append(d)
    body = [r(Q(0, 0)), r(Q(bw, 0)), r(Q(bw, bh)), r(Q(0, bh))]
    thing("lock", "the lock: a block of dark wood bound with iron, carved", body)
    thing("rabbit", "a rabbit carved running over waves, stretched out, its long ears laid back", [r(Q(*p)) for p in EL.RABBIT[::2]])
    thing("ear", "its long ear laid back along its back, a tiny hole in it", hull(alpha["ear"] | alpha["ear-clean"], 4, 12))
    hx, hy = hole
    thing("earhole", "the tiny hole in the ear (black with forty years of dust / clean)", [[int(hx) - 14, int(hy) - 12], [int(hx) + 14, int(hy) - 12], [int(hx) + 14, int(hy) + 12], [int(hx) - 14, int(hy) + 12]],
          note="a generous shape round a 5 px hole: the pin goes here")
    thing("waves", "three carved waves under the rabbit, curling to the left", [r(Q(EL.WAVES[0][0], EL.WAVE_Y[0])), r(Q(EL.WAVES[2][1], EL.WAVE_Y[0])), r(Q(EL.WAVES[2][1], EL.WAVE_Y[1])), r(Q(EL.WAVES[0][0], EL.WAVE_Y[1]))])
    thing("wave", "the middle wave: a hair loose in its groove / slid aside", hull(alpha["wave"], 3, 12), slid=hull(alpha["wave-slid"], 3, 12))
    px_, py_ = post
    thing("post", "under the wave, a square post the size of a coin's hole (showing once the wave is slid; then with the coin on it, turned)",
          [[int(px_) - 30, int(py_) - 30], [int(px_) + 30, int(py_) - 30], [int(px_) + 30, int(py_) + 30], [int(px_) - 30, int(py_) + 30]])
    thing("back", "a line carved along the rabbit's back, behind the ear (shut / a row of thin slits, as close as a fine comb's teeth)",
          [r(Q(a - 0.3, y - 0.6)), r(Q(b + 0.3, y - 0.6)), r(Q(b + 0.3, y + 0.9)), r(Q(a - 0.3, y + 0.9))])
    thing("bolt", "the bolt through the hasp's staple (in / drawn back)", hull(alpha["bolt"], 3, 10), out=hull(alpha["bolt-out"], 3, 8))
    thing("hasp", "the hasp's iron plate on the other leaf, riveted, its staple", [[98, 220], [168, 216], [172, 398], [102, 402]])
    thing("lattice", "the doors' lattice: the dim hall between the bars", [[0, 0], [84, 0], [84, 600], [0, 600]], also=[[[690, 0], [800, 0], [800, 600], [690, 600]]])
    thing("slips", "name slips pasted on the doors' stiles, old and new", [[96, 16], [146, 16], [146, 176], [96, 176]],
          also=[[[606, 16], [662, 16], [662, 176], [606, 176]], [[90, 426], [144, 426], [144, 584], [90, 584]], [[634, 446], [684, 446], [684, 594], [634, 594]]])
    out["things"] = things
    # ---- the hands (PEOPLE-21B draws them; the scene places them): where each one's working point goes, and where it comes from
    out["hands"] = {
        "handEar": {"at": r(hole), "who": "lilsis", "holds": "pin", "from": [228, 40], "angle_deg": 214,
                    "note": "Little Sister's small hand with the hairpin: the pin's ear-pick tip in the ear's hole; the hand comes in from the upper left "
                            "(her wrist about (228, 40)), the pin pointing down and to the right into the hole. Her hand is about 12 cm long: ~260 px here."},
        "handPost": {"at": r(post), "who": "mom", "holds": "coin", "from": [470, 600], "angle_deg": 270,
                     "note": "Mom's hand with the one-mon coin: her fingertips on the coin's rim at the post (the coin is painted on the post in post-coin and "
                             "post-turned: draw the hand without its own coin there, or the scene hides the painted one); the hand comes up from below "
                             "(her wrist about (470, 600)). A woman's hand about 17 cm: ~370 px here."},
        "handComb": {"at": r(slits), "who": "bigsis", "holds": "comb", "from": [660, 40], "angle_deg": 300,
                     "note": "Big Sister's hand with the boxwood comb: the comb's teeth pressed down into the slits along the rabbit's back (the slits run "
                             f"{round((b - a) * EL.S)} px from {r(Q(a, y))} to {r(Q(b, y))}); the hand comes in from the upper right (her wrist about "
                             "(660, 40)). A girl's hand about 16 cm: ~350 px here; the comb about 9 cm: ~200 px."},
    }
    out["hands_note"] = ("All three at once at the last moment (the ear held, the post held, the comb pressed): the ear's hand from the upper left, the comb's "
                         "from the upper right, the post's from below, so that none covers another's working point. The scale is 22 px to the cm. The engine "
                         "draws the hands as overlay sprites at these points (ENGINE-21 close-ups).")
    out["exits"] = [{"id": "back", "to": "edo-shosha", "spawn": "lock", "name": "Step back.", "band": [[0, 560], [800, 560], [800, 600], [0, 600]],
                     "note": "leaving lets everything go (the scene's event: the ear, the post and the comb spring back)"}]
    out["fx"] = [
        {"id": "dust", "type": "shimmer", "what": "a few motes of dust in the low sun across the lock", "rect": [180, 140, 520, 320], "count": 8, "size": 2,
         "flow": [3, -1], "life": 3.0, "color": "#fff2cc", "opacity": 0.35},
    ]
    out["sequence_note"] = ("The puzzle's order (#37): the pin cleans the hole (ear -> ear-clean) and, held in, slides the middle wave aside (wave -> "
                            "wave-slid: the post shows); the coin on the post (post-coin), turned (post-turned): the back's line opens into slits "
                            "(back-open); the comb's teeth in the slits: the bolt can move (bolt -> bolt-out), and the lock chirps. Let go of the pin "
                            "and the wave slides back (hide post-coin/post-turned/back-open with it); let go of the coin and the slits close.")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    return out


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    o = write(f"{EL.OUT}/layout.json")
    print(json.dumps(o["hands"], indent=None)[:600])

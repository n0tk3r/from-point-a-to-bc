"""PAINT-21D: the game's own people stood in edo-theatre and edo-akashi at their marks, in each state (for the check
pictures; edo_d_check.py --people PORT calls it). The people of the new places are drawn this round by PEOPLE-21A/B: until
then round twenty's Edo people of the same heights stand in for them (said on each picture)."""

import os

from PIL import Image, ImageDraw

# stand-ins of round twenty's cast, by height: a man of 1830 1.56 m, a woman 1.46, a girl of nine 1.25, a child 1.18
STAND_INS = {"jubei": "kihei", "chanter": "tokuzo", "shamisen": "gonroku", "tatsu": "isuke", "fusa": "orin", "leader": "pilgrim1",
             "heita": "netmender", "sato": "masa", "satosister": "basketwoman", "awapilgrim1": "pilgrim2", "awapilgrim2": "pilgrim3"}
YAW = {"N": 180, "S": 0, "E": 90, "W": 270}


def pose_js(kind):
    """A pose expression for the sprites page: stand, or seated on the floor, or kneeling."""
    return {"stand": "L.poses.stand(spec, 0)", "sit": "L.poses.sit(spec, 0, { seat: 'ground' })", "walk": "L.poses.walk(spec, 0.3)"}[kind]


def label(im, text):
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 800, 14], fill=(0, 0, 0, 160))
    d.text((4, 2), text, fill=(255, 255, 255, 255))
    return im


def shots(scene, folder, lay, port, outdir, compose, figures_from_game):
    os.makedirs(outdir, exist_ok=True)
    M, S = lay["marks"], lay["stands"]
    made = []

    PL = lay.get("places", {})

    def who(kind, mark, face=None, pose="stand", scale=None, at=None):
        p = at or (M[mark] if mark in M else PL[mark]["at"])
        f = face or S.get(mark, {}).get("face", "S")
        return (kind, p[0], p[1], YAW.get(f, 0), pose_js(pose), scale)

    def shot(name, state, folk, text, hide=()):
        figs = figures_from_game(port, lay, folk)
        im = compose(folder, lay, state, figs, hide=hide)
        label(im, text)
        p = os.path.join(outdir, f"{scene}-{name}.png")
        im.convert("RGB").save(p)
        made.append(p)

    if scene == "edo-theatre":
        pu = lay["puppet"]
        sc = S["chanter"].get("scale")
        shot("01-arrive", {}, [who("mom-edo", "back_mom", "S"), who("bigsis-edo", "back_bigsis", "S"), who("lilsis-edo", "back_lilsis", "S"),
                               who(STAND_INS["jubei"], "jubei", "W")],
             "edo-theatre, before the show: the three just in at the back door; Jubei (stand-in: kihei 1.56 m) by the boy puppet on his stand")
        shot("02-rehearse", {}, [who("bigsis-edo", "stand", "N"), who("lilsis-edo", "stand", "N", at=[M["stand"][0] + 34, M["stand"][1] + 6]),
                                 who(STAND_INS["jubei"], "jubei", "W"), who("mom-edo", "peg", "N"), who(STAND_INS["tatsu"], "tatsuseat", "S", "sit")],
             "rehearsal at the stand; Mom at the peg (the robes); Tatsu (stand-in: isuke) already in the front row")
        # the show: the robes gone (the girls wear them), the boy off his stand (he is the sprite at the rail)
        doll_scale = pu["scale"] * 0.9 / 1.18
        folk = [who(STAND_INS["jubei"], "rail", "N"), who("bigsis-edo", "railLeft", "N"), who("lilsis-edo", "railFeet", "N"),
                ("orin", pu["feet"][0], pu["feet"][1], 90, pose_js("stand"), doll_scale),
                who("mom-edo", "momseat", "S", "sit"), who(STAND_INS["tatsu"], "tatsuseat", "S", "sit"),
                (STAND_INS["chanter"], M["chanter"][0], M["chanter"][1], 180, pose_js("sit"), sc),
                (STAND_INS["shamisen"], M["shamisen"][0], M["shamisen"][1], 180, pose_js("sit"), S["shamisen"].get("scale"))]
        shot("03-show", {"show": "show.png", "gate": "gate-show.png", "housefront": "housefront-show.png"}, folk,
             "the show: Jubei at the rail, Big Sister (left hand) and Little Sister (feet) beside him, the doll (stand-in orin at 0.9 m) on the rail's top; Mom and Tatsu in the front row; the chanter and shamisen on the dais",
             hide=("robes", "boypuppet"))
        shot("04-wing", {}, [who("mom-edo", "wing", "E"), who("bigsis-edo", "lamp", "N"), who("lilsis-edo", "boxes", "N"), who("mom-edo", "gap", "S", at=M["aisle"])],
             "the wing (Mom at the curtain), Big Sister by the lamp, Little Sister by the boxes; Mom again in the house's front aisle, beyond the gap (her floor)")
    elif scene == "edo-akashi":
        shot("01-arrive", {}, [who("mom-edo", "road_mom", "E"), who("bigsis-edo", "road_bigsis", "E"), who("lilsis-edo", "road_lilsis", "E"),
                               who(STAND_INS["sato"], "sato", "W"), who(STAND_INS["satosister"], "satosister", "W"),
                               who(STAND_INS["fusa"], "fusa", "S"), who(STAND_INS["leader"], "leader", "S"), who(STAND_INS["heita"], "heita", "E"),
                               who(STAND_INS["awapilgrim1"], "awapilgrim1", "S"), who(STAND_INS["awapilgrim2"], "awapilgrim2", "S")],
             "edo-akashi: the three arrive on the road from the east; O-Sato and her sister-in-law (masa, basketwoman) on the road; O-Fusa (orin, 1.18) at the water's edge; the leader; Heita (netmender) by his boat; two pilgrims wading (stand-ins)")
        shot("02-wade", {}, [who("lilsis-edo", "ladle", "N"), who("mom-edo", "rocks", "E"), who("bigsis-edo", "shore", "N"),
                             who(STAND_INS["fusa"], "fusa", "S"), who(STAND_INS["heita"], "heita", "E")],
             "#35: Little Sister in the shallows at the ladle (her boots in the water: PEOPLE-21B's), Mom at the rocks, Big Sister on the shore")
        shot("03-beached", {"pilgrimboat": "pilgrimboat-beached.png"}, [who("mom-edo", "pots", "W"), who("bigsis-edo", "tub", "N"), who("lilsis-edo", "shallows", "N"),
                                                                       who(STAND_INS["leader"], "leader", "S"), who(STAND_INS["fusa"], "fusa", "S")],
             "the Awa boat beached; Mom by the pots, Big Sister at the tub, Little Sister at the shallows' edge", hide=("ladle",))
    print("people:", made)
    return made

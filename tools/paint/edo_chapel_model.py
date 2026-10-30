"""The room under the charcoal-burner's storehouse (scene `edo-chapel`): the measurements, in centimetres (room.py: X
across, left to right along the back wall; Y up; Z out from the back wall toward us). PAINT-20F (round twenty).

The game's own invention, in the spirit of the hidden rooms and closet altars that were real: a low room dug into the
hillside, its earth walls and ceiling held by rough timber props and beams; straw mats on the floor; a ladder up to a
trapdoor in the ceiling; three small clay oil lamps in niches and on a ledge; at the far end a closet altar, a plain
cupboard of two doors (shut: a cupboard; open: a white Kannon with a child on a cloth, a folded calendar sheet, a bowl
of water); beside it, on a small wooden stand, the grandmother's bronze mirror, its face toward the room. Nothing a
constable could see from the ladder.

HOW IT IS SEEN. One camera, inside the room's height, as the Office's rooms were seen (their models): the lens 130 cm
up, so that the earth ceiling, the beams and the trapdoor are in the picture and press down over the people. The
ceiling is 182 cm: a man of 1830 (156) has his head 26 under the earth; Mom (168) clears the earth by a hand and the
beams' undersides (170) by two fingers: in the picture her head is just under the beams. (The rig has no stoop: a scene
that wants her to duck says so in a line.) The camera numbers (VIEW) are the scene's; everything else is as PAINTED
(edo_chapel.py and edo_chapel_things.py read these numbers), so the picture and layout.json agree."""

ID = "edo-chapel"
VIEW = dict(horizon=243, full=362, cam=(240.0, 598.0), yaw=3.0, focal=470.0, centre_x=400.0)
W, D, H = 520.0, 600.0, 182.0                                  # across; deep (the lens stands inside, at Z 598); the earth ceiling
ROOM = dict(X=(0.0, W), Z=(0.0, D), H=H)
BEAM_Y = 170.0                                                # the undersides of the cross beams
BEAM_T = 12.0                                                 # a beam: 12 deep (along Z), from BEAM_Y up to the ceiling
BEAMS_Z = [86.0, 226.0, 404.0]                                # where the beams cross (the near one is the foreground's)
POST_R = 7.5                                                  # the props: rough round timbers
POSTS = [(POST_R + 4, 86.0), (W - POST_R - 4, 86.0), (POST_R + 4, 226.0), (W - POST_R - 4, 226.0)]   # X, Z of each wall prop
FRONT_POST = (382.0, 410.0)                                   # the centre prop under the near beam: the front plane's
MATS = (40.0, 480.0, 18.0, 262.0)                             # the straw mats: X0, X1, Z0, Z1, laid in strips 90 wide along Z
MAT_W = 88.0

# ---- the closet altar, against the back wall: a plinth, the cupboard, two doors hinged at its sides
ALTAR = (250.0, 334.0, 0.0, 110.0, 0.0, 44.0)                 # X0, X1, Y0, Y1, Z0, Z1 (the doors' faces at Z 44)
PLINTH_H = 10.0                                               # the base it stands on
DOOR_T = 2.6                                                  # the doors' thickness
SHELF_Y = 46.0                                                # the shelf inside; the Kannon stands on it
KANNON = (292.0, 36.0, 7.0)                                   # X of her middle, her height, her half-width at the robe's hem
CALENDAR = (264.0, 278.0, SHELF_Y, SHELF_Y + 18.0)            # the folded sheet, leaning on the back inside (X0, X1, Y0, Y1 at Z 4)
BOWL = (318.0, 20.0, 6.5, 5.0)                                # the water bowl on the shelf: X, Z, radius, height
DOORS_OPEN = 112.0                                            # degrees each door stands open (out into the room)

# ---- the mirror on its stand, right of the altar
STAND = (358.0, 388.0, 0.0, 40.0, 12.0, 34.0)                 # the stand: a small box of plain wood (X0, X1, Y0, Y1, Z0, Z1)
MIRROR = (373.0, 54.0, 23.0, 8.0)                             # the mirror: X, Y of its middle, Z of its face, radius (16 cm across)

# ---- the lamps: small clay saucer lamps (radius 6, height 4): two on ledges cut into the earth (a niche with a board),
# and one on a lamp stand on the floor before the altar, at its left, which lights the altar's front and the Kannon when the
# doors are open (nothing a constable could see: a lamp on a stand)
LAMPS = {                                                     # name: (X, Y of the lamp's foot, Z, where)
    "lamp-left": (0.0, 104.0, 160.0, "left"),                 # the left wall, by the ladder's foot
    "lamp-stand": (236.0, 66.0, 60.0, "stand"),               # on the stand before the altar's left side
    "lamp-altar-r": (396.0, 116.0, 0.0, "back"),              # the back wall, right of the altar and the mirror
}
NICHE = (24.0, 22.0, 15.0)                                    # a niche: wide, high, deep
LAMP_STAND = (8.0, 18.0)                                      # the stand's post (square), its top board
LAMP_R, LAMP_H = 6.0, 4.0

# ---- the ladder and the trapdoor
HATCH = (108.0, 184.0, 268.0, 348.0)                          # the hole in the ceiling: X0, X1, Z0, Z1
HATCH_T = 8.0                                                 # the shaft: the storehouse's floor boards lie right on the room's ceiling boards; the leaf rests on the rim above them
LADDER = dict(x=(138.0, 164.0), foot_z=200.0, top_z=300.0, top_y=H + HATCH_T + 28.0, rail=4.0, rung=26.0)   # it leans toward us
# the morning sun down the open trapdoor (#27): the direction the light travels; it lands on the floor at SUNPATCH
SUN_DIR = (0.30, -1.0, -0.79)
SUNPATCH = (200.0, 150.0)                                      # X, Z on the floor
WALL_PATCH = (160.0, 105.0)                                    # X, Y on the back wall (Z 0) where the mirror's light is turned

# ---- the foreground on the floor (nobody walks there)
BASKET = (66.0, 292.0, 24.0, 34.0)                             # a charcoal basket: X, Z, radius, height
JAR = (446.0, 282.0, 17.0, 46.0)                               # a water jar: X, Z, radius, height
SACK = (304.0, 344.0, 0.0, 30.0, 392.0, 434.0)                 # a charcoal sack by the centre prop (X0, X1, Y0, Y1, Z0, Z1)

# ---- where people stand (X, Z)
MARKS = {
    "ladder": (196.0, 172.0),                                  # the foot of the ladder (beside it, where one climbs)
    "altar": (296.0, 96.0),                                    # before the closet altar
    "sei": (378.0, 86.0),                                      # Grandmother Sei, by her mirror
    "jinsuke": (440.0, 144.0),                                 # Jinsuke, his arms out in front of his daughter
    "orin": (474.0, 98.0),                                     # O-Rin, behind him, near the wall
    "sit": (222.0, 126.0), "sit1": (172.0, 134.0), "sit2": (222.0, 118.0), "sit3": (272.0, 138.0),   # the family on the mats
    "sunpatch": SUNPATCH,                                      # in the morning sun under the open trapdoor
    "atwall": (160.0, 70.0),                                   # before the bare wall the mirror's light falls on
    "mom": (212.0, 152.0), "bigsis": (264.0, 160.0), "lilsis": (160.0, 164.0),   # fromLadder: just down, at its foot
    "atlamp": (46.0, 150.0), "atmirror": (372.0, 70.0), "front": (330.0, 168.0),
}
# the floor people may stand on: the mats and the earth, clear of the altar, the stand, the walls and the ladder's foot
WALK = [(36.0, 24.0), (222.0, 24.0), (222.0, 76.0), (348.0, 76.0), (348.0, 46.0), (398.0, 46.0), (398.0, 24.0),
        (484.0, 24.0), (484.0, 176.0), (36.0, 176.0)]

# for the skeleton (room_plan.py)
FLATS = [("hatch", "ceiling", *HATCH)]
BOXES = [("altar", *ALTAR), ("stand", *STAND), ("sack", *SACK), ("lampstand", LAMPS["lamp-stand"][0] - 4, LAMPS["lamp-stand"][0] + 4, 0.0, LAMPS["lamp-stand"][1], LAMPS["lamp-stand"][2] - 4, LAMPS["lamp-stand"][2] + 4),
         ("basket", BASKET[0] - BASKET[2], BASKET[0] + BASKET[2], 0.0, BASKET[3], BASKET[1] - BASKET[2], BASKET[1] + BASKET[2]),
         ("jar", JAR[0] - JAR[2], JAR[0] + JAR[2], 0.0, JAR[3], JAR[1] - JAR[2], JAR[1] + JAR[2])]

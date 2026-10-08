"""Big Sister's room in the attic, "The Retreat": a long, calm room under ONE great slope of the roof.

This room is turned the other way from the study and Little Sister's room. The ridge runs ACROSS the picture, high
and near us (out of the top of the frame). The far wall is only a low wall (140 cm), and from its top the roof
comes up and over toward us as one broad slanted ceiling, with two skylights in it. The end walls are at the far
left and right. The way in is a hatch in the floor at the front (the top of the attic ladder): a front-plane cut-out.

SLOPE: the ceiling's height above the floor at depth Z is  KNEE + RISE * Z  (140 cm at the far wall, 470 at Z = 390).

The camera and the shell (walls, roof, skylights) are as they were given. The FURNITURE below is as painted
(home_bigsis_room.py reads these same numbers, so the skeleton, the picture and layout.json agree)."""
ID = "home-bigsis-room"
VIEW = dict(horizon=120, full=440, cam=(380, 1150), yaw=0, focal=800, centre_x=400)
W, KNEE, RIDGE_Y, RIDGE_Z = 760, 140, 470, 390
RISE = (RIDGE_Y - KNEE) / RIDGE_Z
ROOM = dict(X=(0, W), Z=(0, RIDGE_Z), H=KNEE)


def roof(Z):
    return KNEE + RISE * Z


def on_slope(X0, X1, Z0, Z1):
    return [(X0, roof(Z0), Z0), (X1, roof(Z0), Z0), (X1, roof(Z1), Z1), (X0, roof(Z1), Z1)]


# ---------------------------------------------------------------- the shell (fixed)
SKYLIGHTS = [(170, 290, 110, 250), (470, 590, 110, 250)]          # X0, X1, Z0, Z1 on the slope
ROUND_WINDOW = (200, 200, 50)                                     # in the left end wall: Z, Y of its middle, radius
RAFTERS = [5 + 75 * i for i in range(11)]                         # X of each rafter's middle (9 cm wide, 16 deep)

# ---------------------------------------------------------------- the furniture, as painted (cm)
LEDGE = (0, W, 130, 134, 0, 11)             # the low wall's ledge, just under the roof: her candles stand along it
CANDLES = [96, 232, 372, 468, 612, 708]     # X of each candle in glass on the ledge
BOOKCASE = (40, 300, 0, 92, 0, 28)          # low, along the far wall; books by colour
TIMELINE = (44, 500, 98, 126)               # one long strip of paper on the far wall: X0, X1, Y0, Y1
TIMELINE_RED = 0.75                         # the red mark: this far along it
SOUNDTABLE = (326, 438, 0, 52, 6, 52)       # low table in the middle of the far wall
MACHINE = (334, 378, 52, 77, 16, 38)        # the sound machine: a small rounded box, grille and dial
FOUNTAIN = (411, 30, 21)                    # the tabletop fountain: X, Z of its middle, radius of the bowl
DESK = (500, 640, 0, 74, 8, 66)             # writing desk
STOOL = (566, 100, 17, 46)                  # X, Z of its middle, radius, height
CARDS = (520, 624, 88, 124)                 # her novel, planned on index cards in a neat grid over the desk
BED = (600, 752, 0, 40, 140, 345)           # a low platform bed at the right-hand end, head to the far wall
CANOPY = (676, 262, 176, 30)                # the hoop the gauze hangs from: X, Y, Z, radius
BEDSHELF = (752, 760, 112, 115, 176, 250)   # a little shelf on the right end wall, over the pillows: two candles
FOOTLAMPS = [(622, 372), (648, 392)]        # two candle lanterns on the floor at the foot of the bed
FLOORCANDLE = (68, 328)                     # and one at the left, by the towels and her slippers
STUMP = (38, 142, 21, 46)                   # the stump the salt lamp stands on: X, Z, radius, height
SALTLAMP = (38, 142, 46, 76)                # X, Z, and from what height to what height
STUMP2 = (80, 184, 15, 27)                  # a smaller one, for the diffuser
PALM = (30, 78)                             # the small palm, in the far left corner
PAMPAS = (724, 58)                          # a floor vase of dried pampas grass, in the far right corner behind the bed
PLANTSTAND = (4, 62, 0, 104, 206, 266)      # steps of ferns and ivy
ROBE = (266, 312, 70, 178)                  # on a hook on the left end wall: Z0, Z1, Y0, Y1
SLIPPERS = (64, 90, 340, 366)               # set side by side by the hatch, ready to step into: X0, X1, Z0, Z1
BASKET = (46, 298, 24, 36)                  # rolled towels: X, Z, radius, height
MAT = (190, 258, 146, 322)                  # the exercise mat, rolled out: X0, X1, Z0, Z1
RUG = (405, 212, 90)                        # the round rug: X, Z, radius
LANTERNS = [(120, 196, 236, 15), (392, 222, 268, 21), (540, 150, 226, 17)]   # paper lanterns: X, Z, Y of the middle, radius
HANGPLANT = (118, 300, 268)                 # a hanging plant under the slope: X, Z, Y of the pot's rim
HATCH = (110, 240, 470, 560)                # the opening in the floor: X0, X1, Z0, Z1 (front plane, with its rail)
RAIL_H = 84
SIGN = (258, 334, 16, 92, 566)              # her notice on its little easel, facing us: X0, X1, Y0, Y1, Z
TEA = (392, 470, 516, 590)                  # a flat floor cushion with a tea tray on it: X0, X1, Z0, Z1 (front plane)
POUF = (590, 522, 40, 40)                   # X, Z, radius, height (front plane)

POLYS = [
    ("left-end", [(0, 0, 0), (0, KNEE, 0), (0, RIDGE_Y, RIDGE_Z), (0, 0, RIDGE_Z)], (118, 104, 98)),
    ("right-end", [(W, 0, 0), (W, KNEE, 0), (W, RIDGE_Y, RIDGE_Z), (W, 0, RIDGE_Z)], (128, 112, 104)),
    ("slope", on_slope(0, W, 0, RIDGE_Z), (104, 92, 88)),
    ("skylight-1", on_slope(*SKYLIGHTS[0]), (60, 80, 130)),
    ("skylight-2", on_slope(*SKYLIGHTS[1]), (60, 80, 130)),
]
FLATS = [
    ("timeline", "back", TIMELINE[0], TIMELINE[1], TIMELINE[2], TIMELINE[3]),
    ("round-window", "left", ROUND_WINDOW[0] - 50, ROUND_WINDOW[0] + 50, ROUND_WINDOW[1] - 50, ROUND_WINDOW[1] + 50),
    ("cards", "back", CARDS[0], CARDS[1], CARDS[2], CARDS[3]),
    ("robe", "left", ROBE[0], ROBE[1], ROBE[2], ROBE[3]),
    ("rules", ("Z", SIGN[4]), SIGN[0], SIGN[1], SIGN[2], SIGN[3]),
]


def _round(x, z, r, y0, y1):
    return (x - r, x + r, y0, y1, z - r, z + r)


BOXES = [
    ("bookcase",) + BOOKCASE,
    ("soundtable",) + SOUNDTABLE,
    ("machine",) + MACHINE,
    ("fountain",) + _round(FOUNTAIN[0], FOUNTAIN[1], FOUNTAIN[2], 52, 80),
    ("desk",) + DESK,
    ("stool",) + _round(STOOL[0], STOOL[1], STOOL[2], 0, STOOL[3]),
    ("bed",) + BED,
    ("canopy",) + _round(CANOPY[0], CANOPY[2], CANOPY[3], CANOPY[1] - 2, CANOPY[1]),
    ("saltlamp",) + _round(STUMP[0], STUMP[1], STUMP[2], 0, SALTLAMP[3]),
    ("diffuser",) + _round(STUMP2[0], STUMP2[1], STUMP2[2], 0, STUMP2[3] + 18),
    ("plants",) + PLANTSTAND,
    ("palm",) + _round(PALM[0], PALM[1], 16, 0, 140),
    ("towels",) + _round(BASKET[0], BASKET[1], BASKET[2], 0, BASKET[3] + 10),
    ("floorcandle",) + _round(FLOORCANDLE[0], FLOORCANDLE[1], 6, 0, 17),
    ("footlamps",) + _round(FOOTLAMPS[0][0], FOOTLAMPS[0][1], 9, 0, 34),
    ("footlamps",) + _round(FOOTLAMPS[1][0], FOOTLAMPS[1][1], 7, 0, 27),
    ("pampas",) + _round(PAMPAS[0], PAMPAS[1], 12, 0, 150),
    ("cushions",) + _round(469, 31, 26, 0, 31),
    ("mat", MAT[0], MAT[1], 0, 1.5, MAT[2], MAT[3]),
    ("rug",) + _round(RUG[0], RUG[1], RUG[2], 0, 1),
    ("lantern-1",) + _round(LANTERNS[0][0], LANTERNS[0][1], LANTERNS[0][3], LANTERNS[0][2] - LANTERNS[0][3], LANTERNS[0][2] + LANTERNS[0][3]),
    ("lantern-2",) + _round(LANTERNS[1][0], LANTERNS[1][1], LANTERNS[1][3], LANTERNS[1][2] - LANTERNS[1][3], LANTERNS[1][2] + LANTERNS[1][3]),
    ("lantern-3",) + _round(LANTERNS[2][0], LANTERNS[2][1], LANTERNS[2][3], LANTERNS[2][2] - LANTERNS[2][3], LANTERNS[2][2] + LANTERNS[2][3]),
    ("hatch", HATCH[0], HATCH[1], 0, RAIL_H, HATCH[2], HATCH[3]),      # the opening in the floor and its rail: front plane
    ("tea", TEA[0], TEA[1], 0, 14, TEA[2], TEA[3]),                    # front plane
    ("pouf",) + _round(POUF[0], POUF[1], POUF[2], 0, POUF[3]),         # front plane
]
# where people stand (X, Z). The three arrive by the ladder: front left of the floor, just beyond the hatch.
MARKS = {"mom": (270, 316), "bigsis": (352, 312), "lilsis": (176, 380),
         "athatch": (176, 434), "atsound": (300, 100), "atbooks": (170, 72), "attimeline": (252, 72), "atdesk": (536, 142),
         "atbed": (572, 250), "atlamp": (128, 168), "atplants": (118, 240), "atmat": (290, 236), "middle": (405, 212), "front": (470, 436)}
# the floor a person may stand on: 64 cm clear of the far wall (the roof is low there), clear of the desk and stool,
# the bed, the things along the left wall, and of the hatch and the foreground
WALK = [(112, 64), (492, 64), (492, 132), (584, 140), (584, 400), (548, 440), (112, 440)]

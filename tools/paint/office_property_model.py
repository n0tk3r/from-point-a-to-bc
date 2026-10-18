"""Property & Effects (scene `office-property`): the back of the room behind Opal's window, measured in centimetres (see
room.py: X across, left to right along the back wall; Y up; Z out from the back wall toward us). OFFICE-17C.

HOW IT IS SEEN. The camera stands among the shelves, a man's eye high (the lens 160 cm up), a little right of the aisle's
middle and turned a little to the left, and looks down the aisle to Opal's window at the far end: gray steel shelving
floor to ceiling on both sides, every thing on it tagged; the left run comes close past the lens, so its bays show their
faces; the right run is seen along its edge. Ahead, the far wall: Opal's window onto the hall (her counter, the sliding
glass, the hall lit beyond it, the bell on the hall's side), her stool at it, her knitting, the door to the hall at its
right. The grille is in the ceiling over the top of the left run, near us, so that it is seen from below at the top of
the picture; the banjo stands in a bay of the left run near us (the nearest place a grown-up can walk to), on its
lowest shelf, turned to face us.

The camera numbers (VIEW) and the shell (ROOM, the window, the door) are the scene's; everything else is the furniture
as it is PAINTED (office_property.py reads these same numbers)."""
ID = "office-property"
VIEW = dict(horizon=290, full=436, cam=(262, 706), yaw=-12, focal=500, centre_x=400)
W, D, H = 420, 800, 260
ROOM = dict(X=(0, W), Z=(0, D), H=H)
WALL_T = 14.0

# ---- the ceiling: 60 cm tiles; three light panels down the aisle; the grille over the left run near us
GRID = (60.0, 60.0)
GRID_X0, GRID_Z0 = 0.0, 20.0
VENT = (0.0, 60.0, 380.0, 440.0)                            # the return-air grille: X0, X1, Z0, Z1
TROFFERS = [(180.0, 240.0, 20.0, 140.0), (180.0, 240.0, 260.0, 380.0), (180.0, 240.0, 500.0, 620.0)]
SPRINKLERS = [(120.0, 200.0), (300.0, 320.0), (120.0, 500.0), (320.0, 560.0)]
SPEAKER = (300.0, 110.0, 12.0)                              # the building's speaker: X, Z, radius
SMOKE = (120.0, 330.0, 7.0)

# ---- the far wall (Z = 0): Opal's window and the door
WINDOW = (96.0, 262.0, 100.0, 196.0)                        # the opening: X0, X1, Y0, Y1 (two sliding panes in it)
COUNTER = (64.0, 286.0, 88.0, 94.0, 0.0, 52.0)              # Opal's counter along the window (X0, X1, Y0, Y1 the top, Z0, Z1)
DOOR = (300.0, 386.0, 0.0, 205.0)                           # the door to the hall, at the window's right
DOOR_FRAME = 6.0
DOOR_SLIT = (356.0, 374.0, 108.0, 180.0)
HALL_D = 180.0                                              # the hall: its far wall at Z = -HALL_D
LEDGE = (92.0, 266.0, 97.0, 101.0, -34.0, -WALL_T)          # the hall's ledge under the glass (X0, X1, Y0, Y1, Z0, Z1)
BELL = (236.0, -24.0, 5.0)                                  # the bell on the hall's ledge: X, Z, radius of its dome
STOOL = (176.0, 80.0, 66.0, 18.0)                           # Opal's stool: X, Z, seat height, seat radius
BASKET = (234.0, 74.0, 17.0, 26.0)                          # her knitting basket on the floor by the stool: X, Z, radius, height
STAMP = (150.0, 20.0)                                       # her date stamp and its ink pad on the counter: X, Z
SIGN = (150.0, 208.0, 202.0, 218.0)                         # THIS WINDOW CLOSES AT 1700: a small sign over the window (X0, X1, Y0, Y1)
RECEIPT = (102.0, 50.0, -6.0)                               # where the receipt lands: at the counter's front edge (X, Z), its turn (degrees)
CABINET = (6.0, 52.0, 0.0, 132.0, 4.0, 66.0)                # a filing cabinet in the corner left of the counter (Opal's: forty-one statements)

# ---- the shelving: gray steel units, 92 wide, 45 deep, 230 high; shelves at these heights (each unit may leave some out)
SHELF_YS = (8.0, 48.0, 92.0, 136.0, 180.0, 222.0)
UNIT_W, UNIT_D, UNIT_H = 92.0, 45.0, 230.0
LEFT_X = (2.0, 47.0)                                        # the left run, against the left wall (its face at X = 47)
LEFT_Z = [(80.0, 172.0), (172.0, 264.0), (264.0, 356.0), (356.0, 448.0), (448.0, 540.0), (540.0, 632.0), (632.0, 724.0)]
RIGHT_X = (W - 47.0, W - 2.0)                               # the right run (its face at X = 373)
RIGHT_Z = [(190.0, 282.0), (282.0, 374.0), (374.0, 466.0), (466.0, 558.0), (558.0, 650.0), (650.0, 742.0)]
LEFT_SHELVES = {2: (8.0, 136.0, 180.0, 222.0)}              # left-2 is the tall bay: the banjo stands in it
BANJO = (31.0, 284.0)                                       # the banjo: the middle of its pot's foot on left-2's lowest shelf (X, Z)
BANJO_LEN, BANJO_POT = 94.0, 28.0                            # its length, its pot's width
RANGER_SHELF = (24.0, 222.0, 410.0)                         # where Ranger lands from the grille: on left-3's top shelf (X, Y, Z)

# the tagged things (unit, shelf height, Z of the middle, kind): the brief's list and a few more
LEFT_THINGS = [
    ("lamp", 1, 92.0, 232.0), ("cup", 1, 92.0, 196.0),
    ("hat", 2, 136.0, 304.0),
    ("feather", 3, 180.0, 404.0), ("sandal", 3, 136.0, 378.0), ("horseshoe", 3, 136.0, 426.0), ("gnome", 3, 92.0, 382.0), ("cassette", 3, 92.0, 424.0),
    ("lantern", 4, 136.0, 474.0), ("skate", 4, 92.0, 500.0),
]

# ---- near us (front plane: people pass behind): a cart parked by the right run, two boxes on the floor by the left run
CART = (300.0, 352.0, 470.0, 566.0)                         # X0, X1, Z0, Z1 (its top at 86, a lower shelf at 24)
FLOORBOXES = [(56.0, 100.0, 452.0, 492.0, 0.0, 28.0), (60.0, 98.0, 456.0, 488.0, 28.0, 54.0)]
KICKSTOOL = (150.0, 448.0, 22.0, 38.0)                      # a round kick stool (on casters) in the aisle near us: X, Z, radius, height

FLATS = [
    ("window", "back", WINDOW[0], WINDOW[1], WINDOW[2], WINDOW[3]),
    ("door", "back", DOOR[0], DOOR[1], DOOR[2], DOOR[3]),
    ("sign", "back", *SIGN),
]
BOXES = [
    ("counter", COUNTER[0], COUNTER[1], 0.0, COUNTER[3], COUNTER[4], COUNTER[5]),
    ("stool", STOOL[0] - STOOL[3], STOOL[0] + STOOL[3], 0.0, STOOL[2], STOOL[1] - STOOL[3], STOOL[1] + STOOL[3]),
    ("basket", BASKET[0] - BASKET[2], BASKET[0] + BASKET[2], 0.0, BASKET[3], BASKET[1] - BASKET[2], BASKET[1] + BASKET[2]),
    ("cabinet", CABINET[0], CABINET[1], CABINET[2], CABINET[3], CABINET[4], CABINET[5]),
    *[(f"left-{i}", LEFT_X[0], LEFT_X[1], 0.0, UNIT_H, z0, z1) for i, (z0, z1) in enumerate(LEFT_Z)],
    *[(f"right-{i}", RIGHT_X[0], RIGHT_X[1], 0.0, UNIT_H, z0, z1) for i, (z0, z1) in enumerate(RIGHT_Z)],
    ("vent", VENT[0], VENT[1], H - 3, H, VENT[2], VENT[3]),
    *[(f"troffer{i}", t[0], t[1], H - 4, H, t[2], t[3]) for i, t in enumerate(TROFFERS)],
    ("cart", CART[0], CART[1], 0.0, 86.0, CART[2], CART[3]),
]
MARKS = {
    "opal": (STOOL[0], STOOL[1]),                            # on her stool at the window, her back to the shelves (the floor under her hips)
    "counter": (RECEIPT[0], RECEIPT[1]),                     # (on the counter: see layout.json)
    "vent": (RANGER_SHELF[0], RANGER_SHELF[2]),              # (on left-3's top shelf: see layout.json)
    "banjo": (94.0, 292.0),                                  # in the aisle in front of the banjo's bay (where Opal takes it from)
    "door": (343.0, 46.0),                                   # just inside the door
    "atwindow": (130.0, 84.0), "atstool": (214.0, 112.0), "atbasket": (262.0, 104.0), "atstamp": (128.0, 80.0),
    "atcabinet": (86.0, 90.0), "atsign": (200.0, 100.0), "atvent": (96.0, 270.0),
    "atleft0": (84.0, 130.0), "atleft1": (86.0, 214.0), "atleft3": (100.0, 286.0),
    "atright0": (322.0, 200.0), "atright1": (326.0, 240.0),
    "front": (210.0, 270.0),
}
# the aisle: from the window and the door to where a grown-up is about 200 px tall; clear of the shelves, the stool and
# the basket (those are `blocked`)
WALK = [(66, 60), (300, 58), (300, 28), (392, 28), (392, 150), (338, 186), (336, 246), (66, 298)]

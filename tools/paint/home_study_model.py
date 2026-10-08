"""Dad's study, "Trip Headquarters": a big room under the roof. We look along the ridge at the far gable wall.

The roof comes down on both sides to low walls (130 cm); the ridge is 420 cm up, along the middle. The door to
the landing is at the front left: a partition under the slope (X = 100, from Z = 590 toward us) with the doorway
in it, and the leaf standing open into the room. Frame and leaf are a front-plane cut-out at the picture's left edge.

The camera numbers (VIEW) and the shell (ROOM, POLYS) are fixed. Everything below them is the furniture as it
is PAINTED (home_study.py reads these same numbers), in centimetres: X across, Y up, Z out from the far wall."""
ID = "home-study"
VIEW = dict(horizon=120, full=440, cam=(410, 1210), yaw=-6, focal=800, centre_x=400)
W, D, KNEE, RIDGE = 700, 430, 130, 420
ROOM = dict(X=(0, W), Z=(0, 1210), H=KNEE)
POLYS = [
    ("gable", [(0, 0, 0), (W, 0, 0), (W, KNEE, 0), (W / 2, RIDGE, 0), (0, KNEE, 0)], (150, 132, 118)),
    ("roof-left", [(0, KNEE, 0), (W / 2, RIDGE, 0), (W / 2, RIDGE, 1210), (0, KNEE, 1210)], (104, 90, 84)),
    ("roof-right", [(W, KNEE, 0), (W / 2, RIDGE, 0), (W / 2, RIDGE, 1210), (W, KNEE, 1210)], (122, 106, 96)),
]

# ---- on the far wall (X0, X1, Y0, Y1)
WINDOW = (296, 404, 136, 284)
CORK = (108, 212, 126, 206)
MAP = (418, 598, 48, 186)
CALENDAR = (232, 266, 150, 204)

# ---- standing on the floor (X0, X1, Y0, Y1, Z0, Z1)
DESK = (92, 322, 0, 76, 8, 104)
PC_CASE = (192, 254, 76, 92, 34, 82)                # "the mainframe": a flat beige case with the monitor on it
MONITOR = (195, 251, 93, 141, 58, 84)               # a fat monitor (painted a little bigger than life so it reads)
SCREEN = (201, 245, 100, 135)                       # the glass, on the monitor's front (Z = 84)
NOTE = (236, 255, 122, 141)                         # the sticky note, on the monitor's frame, top right
CHAIR = (203, 253, 0, 88, 114, 164)
CABINET = (6, 62, 0, 100, 200, 268)                 # a filing cabinet, drawers toward us
MACHINE = (9, 59, 100, 124, 222, 262)              # the answering machine: a wedge, its sloping face toward us
SHELVES = (646, 698, 0, 92, 150, 400)
VAULT = (648, 696, 92, 116, 348, 388)               # the cash box, at the near end of the shelves, dial toward us
SHELF_LAMP = (670, 190)                             # X, Z of the shaded lamp on the shelves
GLOBE = (622, 66, 88, 21)                           # X, Z of its stand, height of its middle, radius
RUG = (300, 560, 160, 340)                          # X0, X1, Z0, Z1
BANNER = (254, 446, 314, 340, 635)                  # X0, X1, Y0, Y1, Z: hung on a string between two rafters
PLANE = (458, 278, 560)                             # the model aeroplane: X, Y, Z (it hangs over the wall map)
PARTITION = (100, 590)                              # the wall the door is in: at X, from this Z toward us
DOORWAY = (640, 725, 203)                           # Z0, Z1 of the opening, its height
LEAF = (25.0, 85.0)                                 # the leaf: degrees it stands out from the X axis toward us, its width
HEAP = (268, 566, 0, 62, 520, 640)                  # the things that did not fit in the car (front plane)
PILE = (636, 698, 0, 70, 436, 520)                  # more of them, by the end of the shelves (front plane)

FLATS = [
    ("window", "back", *WINDOW),
    ("wallmap", "back", *MAP),
    ("corkboard", "back", *CORK),
    ("banner", ("Z", BANNER[4]), *BANNER[:4]),
    ("door", ("X", PARTITION[0]), DOORWAY[0], DOORWAY[1], 0, DOORWAY[2]),
]
BOXES = [
    ("desk", *DESK),
    ("computer", PC_CASE[0], PC_CASE[1], PC_CASE[2], MONITOR[3], PC_CASE[4], MONITOR[5]),
    ("chair", *CHAIR),
    ("cabinet", *CABINET),                           # the answering machine sits on this
    ("machine", *MACHINE),
    ("shelves", *SHELVES),                           # the family vault is on this, at the near end
    ("vault", *VAULT),
    ("globe", GLOBE[0] - GLOBE[3], GLOBE[0] + GLOBE[3], 0, GLOBE[2] + GLOBE[3], GLOBE[1] - GLOBE[3], GLOBE[1] + GLOBE[3]),
    ("partition", PARTITION[0] - 12, PARTITION[0], 0, 213, PARTITION[1], DOORWAY[0]),
    ("heap", *HEAP),                                 # front plane: trip supplies
    ("pile", *PILE),
]
MARKS = {"mom": (212, 372), "bigsis": (150, 335), "lilsis": (282, 388),          # fromLanding: just in, front left of the floor
         "atdesk": (228, 196), "atnote": (290, 150), "atmachine": (112, 240), "atvault": (596, 362), "atshelves": (604, 250),
         "atmap": (508, 130), "atcork": (128, 152), "atdoor": (176, 420), "atglobe": (566, 128), "atwindow": (372, 134),
         "atbanner": (350, 300), "front": (330, 430), "frontright": (540, 432)}
# the floor people may stand on: in front of the desk and its chair, clear of the cabinet, the shelves and the door's swing
WALK = [(84, 134), (190, 134), (190, 186), (268, 186), (268, 126), (596, 116), (626, 150), (626, 440), (156, 440), (84, 300)]

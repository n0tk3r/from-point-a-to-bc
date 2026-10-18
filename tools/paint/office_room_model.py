"""Interview Room C, the Comfortable Room (scene `office-room`): the measurements of the room and everything in it, in
centimetres (see room.py: X across, left to right along the back wall; Y up; Z out from the back wall toward us).
OFFICE-17C.

HOW IT IS SEEN. A small windowless room under fluorescent tubes. We stand low (the lens 165 cm up, a standing man's eye)
inside the room's near end, turned 25 degrees to the right, so that the back wall runs from its near left corner (where
the corner chair stands under the ceiling vent) away to the far right corner, and the right wall comes back toward us.
The low lens is the point: the ceiling is in the picture, so the vent over the corner chair is a grille seen from below,
and so are the tubes that light the room.

    the back wall, left to right: the corner chair under the vent; the door (gray steel, a wired-glass slit, the clock
    over it); by the door the sign, the thermostat and the intercom; the poster; the long one-way mirror
    the right wall: the floor lamp in the far corner (unlit: the Office's idea of comfort), the water cooler with its
    paper cones, the plastic plant near us
    the middle: the table, Grandpa Joe's chair on its left side, Dale's and Merle's on its right side
    near us: the wastebasket at the left, a box of spare questionnaires on the floor, the plant at the right (front plane,
    cut off by the picture's edges)

WHY THE CAMERA IS TURNED. A ceiling grille is only seen from below where the ceiling is near the lens. Seen square-on,
every corner of a room is far off and its piece of ceiling a sliver; turned, the back wall's left end comes close (a
grown-up at the corner chair is 168 px) while the floor still runs deep to the right, where the table is.

The camera numbers (VIEW) and the shell (ROOM, the door) are the scene's; everything else is the furniture as it is
PAINTED (office_room.py reads these same numbers)."""
ID = "office-room"
VIEW = dict(horizon=295, full=446, cam=(91, 617), yaw=25, focal=500, centre_x=400)
W, D, H = 520, 700, 260                                     # the room: width, depth (to behind the lens), the ceiling
ROOM = dict(X=(0, W), Z=(0, D), H=H)
WALL_T = 14.0                                               # how thick the walls are (the door's reveal): painted block

# ---- the ceiling: a suspended grid of 60 cm tiles; the border tiles along the left and back walls are cut to 70, and
# the one in the corner is the grille (the Office's air is big: so are its grilles)
GRID = (60.0, 60.0)                                         # tile size along X, along Z
GRID_X0, GRID_Z0 = 70.0, 70.0                               # where the grid's lines start (one runs along X = 70, one along Z = 70)
VENT = (0.0, 70.0, 0.0, 70.0)                               # the return-air grille over the corner: X0, X1, Z0, Z1
TROFFERS = [(310.0, 370.0, 70.0, 190.0), (130.0, 190.0, 70.0, 190.0), (250.0, 310.0, 310.0, 430.0), (430.0, 490.0, 190.0, 310.0)]   # light panels (X0, X1, Z0, Z1), each two tiles
SPEAKER = (460.0, 100.0, 13.0)                              # the building's speaker in the ceiling: X, Z, radius
SMOKE = (220.0, 220.0, 7.0)                                 # a smoke detector: X, Z, radius
SPRINKLERS = [(100.0, 160.0), (400.0, 40.0), (400.0, 340.0), (160.0, 400.0)]

# ---- on the back wall (X0, X1, Y0, Y1)
DOOR = (64.0, 154.0, 0.0, 205.0)                            # the doorway (its leaf opens OUT, into the hall)
DOOR_FRAME = 6.0
DOOR_SLIT = (122.0, 140.0, 108.0, 180.0)                    # the wired-glass slit in the leaf (X0, X1, Y0, Y1)
CLOCK = (109.0, 236.0, 15.0)                                # over the door: X, Y of its middle, radius
SIGN = (164.0, 248.0, 140.0, 212.0)                         # INTERVIEW ROOM C / THE / COMFORTABLE / ROOM / THIS ROOM HAS BEEN RATED COMFORTABLE
THERMO = (170.0, 200.0, 112.0, 134.0)                       # the thermostat: a beige box, a small dial, the number's window
INTERCOM = (212.0, 238.0, 94.0, 132.0)                      # DISPATCH: PRESS TO TALK, a speaker grille and the red button
POSTER = (258.0, 316.0, 98.0, 182.0)                        # PECULIAR? REPORT IT. (a fence, and a hole in the sky behind it)
MIRROR = (330.0, 512.0, 92.0, 196.0)                        # the one-way mirror: glass in a steel frame
MIRROR_FRAME = 5.0

# ---- standing on the floor (X0, X1, Y0, Y1, Z0, Z1)
TABLE = (284.0, 364.0, 0.0, 75.0, 56.0, 186.0)              # the table: its long sides face left and right
TOP_T = 4.0                                                 # the top's thickness
SEAT = 46.0                                                 # every chair's seat (the rig's "chair": 0.262 of 175 cm)
CHAIR_W, CHAIR_D, CHAIR_BACK = 44.0, 44.0, 86.0             # a stacking chair: seat width, depth, the top of its back
TZ = (TABLE[4] + TABLE[5]) / 2                              # the table's middle, along Z
CHAIRS = {                                                  # each chair: X, Z of the seat's middle, and which way its sitter faces (+1 east, -1 west)
    "joe": (TABLE[0] - 26.0, TZ, +1),                       # Grandpa Joe's, on the left side, facing the two of them
    "dale": (TABLE[1] + 26.0, TZ - 34.0, -1),               # Dale's, on the right side, the far one (he reads the questions)
    "merle": (TABLE[1] + 26.0, TZ + 34.0, -1),              # Merle's, the near one (he writes the answers down)
}
CORNER_CHAIR = (26.0, 27.0)                                 # the fourth chair, pushed into the corner under the vent, facing out
QUESTIONNAIRE = (322.0, 352.0, 76.0, 114.0)                 # on the table before Dale while the suits are there: X0, X1, Z0, Z1 (a thick stack)
COOLER = (480.0, 514.0, 0.0, 128.0, 170.0, 204.0)           # the water cooler against the right wall (the jug on top)
LAMP = (488.0, 28.0, 17.0)                                  # the floor lamp in the far corner: X, Z of its foot, the shade's radius (unlit)
PLANT = (492.0, 300.0, 20.0)                                # the plastic plant against the right wall near us: X, Z of the pot, its radius
BASKET = (64.0, 300.0, 17.0, 38.0)                          # front plane: the wastebasket near us at the left (X, Z, radius, height): pages of questionnaire in it
FILEBOX = (196.0, 248.0, 0.0, 30.0, 316.0, 354.0)           # front plane: a box of spare questionnaires on the floor near us (X0, X1, Y0, Y1, Z0, Z1), turned a little
FILEBOX_ANG = -14.0

# for the skeleton (room_plan.py): flats on the walls and the furniture as boxes
FLATS = [
    ("door", "back", DOOR[0], DOOR[1], DOOR[2], DOOR[3]),
    ("sign", "back", *SIGN), ("thermostat", "back", *THERMO), ("intercom", "back", *INTERCOM),
    ("poster", "back", *POSTER), ("mirror", "back", *MIRROR),
    ("clock", "back", CLOCK[0] - CLOCK[2], CLOCK[0] + CLOCK[2], CLOCK[1] - CLOCK[2], CLOCK[1] + CLOCK[2]),
]


def _chair(name, X, Z, face):
    h = CHAIR_W / 2
    return (name, X - h, X + h, 0.0, CHAIR_BACK, Z - h, Z + h)


BOXES = [
    _chair("cornerchair", *CORNER_CHAIR, 0), ("vent", VENT[0], VENT[1], H - 3, H, VENT[2], VENT[3]),
    ("table", *TABLE),
    *[_chair("chair-" + k, X, Z, f) for k, (X, Z, f) in CHAIRS.items()],
    ("cooler", *COOLER), ("lamp", LAMP[0] - LAMP[2], LAMP[0] + LAMP[2], 0.0, 160.0, LAMP[1] - LAMP[2], LAMP[1] + LAMP[2]),
    ("plant", PLANT[0] - PLANT[2], PLANT[0] + PLANT[2], 0.0, 150.0, PLANT[1] - PLANT[2], PLANT[1] + PLANT[2]),
    ("basket", BASKET[0] - BASKET[2], BASKET[0] + BASKET[2], 0.0, BASKET[3], BASKET[1] - BASKET[2], BASKET[1] + BASKET[2]),
    ("filebox", *FILEBOX),
    *[(f"troffer{i}", t[0], t[1], H - 4, H, t[2], t[3]) for i, t in enumerate(TROFFERS)],
]

# where people stand (X, Z): stand places on the floor; the seated marks are the floor under the sitter's hips
MARKS = {
    "joe": (CHAIRS["joe"][0], CHAIRS["joe"][1]), "dale": (CHAIRS["dale"][0], CHAIRS["dale"][1]),
    "merle": (CHAIRS["merle"][0], CHAIRS["merle"][1]),
    "chair": CORNER_CHAIR,                                   # on the corner chair (his feet on its seat: see layout.json)
    "atchair": (46.0, 88.0),                                 # in front of the corner chair, to climb onto it
    "door": (109.0, 46.0), "opal": (128.0, 82.0),
    "intercom": (225.0, 44.0), "thermostat": (185.0, 44.0),
    "atjoe": (TABLE[0] - 26.0, TZ + 50.0),                   # beside his chair, to sit down or get up
    "atsign": (206.0, 50.0), "atposter": (287.0, 42.0), "atmirror": (415.0, 40.0), "atclock": (109.0, 66.0),
    "attable": (252.0, 186.0), "atquestionnaire": (270.0, 108.0),
    "atcooler": (458.0, 214.0), "atlamp": (452.0, 64.0), "atplant": (452.0, 266.0), "atbasket": (106.0, 126.0),
    "atdale": (412.0, 74.0), "atmerle": (416.0, 210.0),
    "front": (380.0, 240.0),
}
# the floor people may stand on: the floor round the table, clear of the corner chair, the lamp, the cooler and the
# plant; out to where a grown-up is about 195 px tall near us (the camera is turned, so that edge runs on a slant)
WALK = [(58, 16), (458, 16), (458, 56), (504, 56), (504, 158), (468, 158), (468, 216), (504, 216), (504, 268), (462, 272),
        (440, 284), (300, 220), (200, 173), (110, 131), (20, 89), (20, 62), (58, 62)]

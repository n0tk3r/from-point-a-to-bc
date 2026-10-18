"""The break room of the Office Of Peculiar Sectors' field headquarters (scene `office-breakroom`): the measurements of
the room and everything in it, in centimetres (see room.py: X across, left to right; Y up; Z out from the back wall
toward us). OFFICE-17D.

HOW IT IS SEEN. We stand just inside the room, a step from the front, and look at the back wall almost square on:
the tall old fridge in its left corner, the counter along the wall from the fridge to the middle (the microwave, the
dish rack and the sink, Wendell's pie, the coffee maker and the paper cups), the corkboard over the counter at a
raccoon's eye from its top, the clock over the board; to the right the snack machine and the door to the hall. The
couch runs along the left wall toward us, the afghan over its back; Jed's plastic chair stands out on the floor at the
counter's right end, turned to face the pie; a round table and its chair stand in the near right, and a low table in
the near left, cut off by the picture's bottom edge (OFFICE-17D, resumed: the foreground). Overhead: a ceiling
of square tiles in their grid, two fluorescent fittings, the speaker in the far right corner, and over the fridge the
return grille Ranger comes down through (a two-by-four of slats, its length running away from us, so that it shows).

THE CHEAT. The room is wide as a cartoon's is (7.6 m), so that people come out at the game's sizes against it, and the
eye is low for one of the game's rooms (2.0 m) under a ceiling of 2.85 m: so the ceiling, and the grille over the
fridge, can be seen at all, and the counter's top and the pie on it are seen from above. The fridge is a tall
institutional one (1.95 m) and the box of plastic forks on it (16 cm) is Ranger's step to the grille (74 cm above it);
the microwave beside it is his step down to the counter.

The camera numbers (VIEW) are the scene's; everything else is the furniture as it is PAINTED (office_breakroom.py and
its helpers read these same numbers), so the skeleton, the picture and layout.json agree."""

ID = "office-breakroom"
VIEW = dict(horizon=200, full=383, cam=(372.0, 640.0), yaw=-3.0, focal=470.0, centre_x=400.0)
W, D, H = 760.0, 700.0, 285.0                             # the room: across, deep (the camera stands inside at Z 640), the ceiling
ROOM = dict(X=(0.0, W), Z=(0.0, D), H=H)
TILE = 61.0                                               # the ceiling's tiles and the floor's are laid from the back left corner

# ---- standing against the back wall (X0, X1, Y0, Y1, Z0, Z1)
FRIDGE = (40.0, 122.0, 0.0, 195.0, 0.0, 74.0)             # tall, old, almond enamel: freezer door over the fridge door, hinged at the wall
FREEZER_Y = 128.0                                         # the line between its two doors
FORKS = (50.0, 88.0, 195.0, 211.0, 16.0, 46.0)            # the box of plastic forks on top (Ranger's step up to the grille)
PLANT = (106.0, 202.0, 34.0, 8.0)                         # the dusty plant on top: X, height of its pot's rim, Z, the pot's radius
COUNTER = (124.0, 500.0, 0.0, 90.0, 0.0, 64.0)            # base cabinets and a laminate top, along the back wall from the fridge
TOP_T = 3.5                                               # the top's thickness
SPLASH = 10.0                                             # the backsplash, up from the top
MICRO = (128.0, 186.0, 90.0, 122.0, 6.0, 48.0)            # the microwave at the counter's left end, by the fridge (Ranger's step)
RACK = (192.0, 230.0, 90.0, 108.0, 10.0, 48.0)            # the dish rack: two mugs and a plate
SINK = (238.0, 290.0, 12.0, 50.0, 17.0)                   # the basin cut into the top: X0, X1, Z0, Z1, its depth
FAUCET = (264.0, 6.0)                                     # X, Z of the gooseneck tap behind the basin
PIE = (332.0, 30.0, 14.0)                                 # Wendell's pie: X, Z of its middle on the counter, the tin's radius (28 cm)
PIE_TIN_H, PIE_DOME = 3.4, 4.6                            # the tin's side, and how high the lattice crust domes over it
CARD = dict(x=332.0, z=13.0, w=17.0, h=11.0, lean=24.0)   # the card stood against the tin's far side, leaning back on the wall's side
COFFEE = (444.0, 472.0, 90.0, 126.0, 8.0, 36.0)           # the coffee maker; its glass pot, full, on the warmer at the front
POT = (458.0, 28.0, 7.0, 96.0, 116.0)                     # the pot: X, Z of its middle, radius, its foot, its rim
CUPS = (482.0, 24.0, 4.2, 90.0, 116.0)                    # the stack of paper cups: X, Z, radius, foot, top
SUGAR = (493.0, 40.0, 3.6, 90.0, 104.0)                   # the sugar canister
CABINETS = (124.0, 296.0, 142.0, 214.0, 0.0, 34.0)        # the wall cabinets over the microwave, the rack and the sink
TOWELS = (180.0, 236.0, 131.0, 22.0, 5.5)                 # the paper towel roll under the cabinets: X0, X1, Y of its middle, Z, radius
VENDING = (528.0, 622.0, 0.0, 186.0, 0.0, 88.0)           # the snack machine, against the wall right of the counter
VEND_GLASS = (535.0, 596.0, 66.0, 178.0)                  # its window (X0, X1, Y0, Y1 on its front)
VEND_PANEL = (600.0, 617.0, 96.0, 150.0)                  # its buttons (X0, X1, Y0, Y1)
VEND_TRAY = (541.0, 590.0, 16.0, 40.0)                    # its tray (X0, X1, Y0, Y1): where a packet comes down to
VEND_ROWS = 5                                             # rows of coils behind the glass
VEND_COLS = 4
PEANUT_SLOT = (2, 1)                                      # the coil that held the peanuts: row from the top, column from the left
DOOR = (650.0, 742.0, 0.0, 208.0)                         # the door to the hall, in the back wall: X0, X1, Y0, Y1 of the opening
DOOR_HINGE = "right"                                      # it swings into the room on the hinges at its right jamb
DOOR_OPEN = 76.0                                          # how far it stands open, degrees
TRASH = (6.0, 34.0, 0.0, 64.0, 6.0, 36.0)                 # a kitchen bin with a swing lid, between the fridge and the left wall
MAT = (232.0, 312.0, 68.0, 112.0)                         # a rubber mat on the floor in front of the sink: X0, X1, Z0, Z1

# ---- on the walls
BOARD = (300.0, 440.0, 104.0, 180.0)                      # the corkboard over the counter: X0, X1, Y0, Y1 on the back wall
BOARD_T = 2.5
# the sheets on the board (u0, v0, wide, high, cm from its lower left corner) and what each is
SHEETS = {
    "form7": (6.0, 38.0, 50.0, 34.0),                     # FORM 7 IS NOT OPTIONAL: a printed notice, its FORM 7 big
    "found": (10.0, 6.0, 32.0, 24.0),                     # FOUND: ONE ROMAN SANDAL (1951) · SEE OPAL: an old index card gone yellow
    "bowling": (62.0, 22.0, 32.0, 48.0),                  # the bowling league sheet: a heading, a ball and pins, a grid of scores
    "menu": (46.0, 6.0, 12.0, 26.0),                      # a menu from somewhere that delivers (no name: a drawing of a cheeseburger)
    "schedule": (102.0, 8.0, 28.0, 38.0),                 # LAMPLIGHTER · TEST SCHEDULE: a typed sheet (a cut-out: Ranger takes it)
}
CLOCK = (370.0, 218.0, 15.5)                              # the clock over the board: X, Y of its middle, radius
CLOCK_TIME = (1, 50)                                      # what it says: ten to two in the afternoon (its second hand goes round: frames)
SIGN = (52.0, 138.0, 108.0, 186.0)                        # LABEL YOUR LUNCH. · MGMT. on the freezer door: X0, Y0, X1, Y1 (on the door's face)
MENU_ON_FRIDGE = (56.0, 76.0, 84.0, 116.0)                # a takeout menu held by a magnet on the fridge door
CALENDAR = (66.0, 134.0, 126.0, 194.0)                    # on the left wall, between the fridge's corner and the couch: Z0, Z1, Y0, Y1 (October, crossed off to the 30th)
JACKET_HOOK = (720.0, 168.0)                              # a gray jacket on a hook on the door (X, Y on the leaf)

# ---- on the ceiling (X0, X1, Z0, Z1)
VENT = (61.0, 122.0, 0.0, 122.0)                          # the return grille over the fridge: a two-by-four, its slats across
VENT_SLATS = 5                                            # slats across it (painted bold: from below it is seen nearly edge-on)
TROFFERS = [(305.0, 427.0, 122.0, 183.0), (305.0, 427.0, 366.0, 427.0)]   # the two fluorescent fittings: two-by-fours along X
SPEAKER_BOX = (760.0, 236.0, 280.0, 40.0)                 # the speaker, a box across the far right corner up under the ceiling: X of the corner,
                                                          # Y of its foot and its top, how far out along each wall its foot reaches
TUBES_OUT = (0, 1)                                        # the near fitting's dead tubes (of three, the far one first)

# ---- out on the floor
COUCH = (0.0, 92.0, 0.0, 86.0, 150.0, 380.0)              # along the left wall, facing E: X0, X1 (its front), Y0, Y1 (back top), Z0, Z1
SEAT_H = 45.9                                             # the cushions' top: the rig's "chair" (0.262 of a grown person: 45.9 cm)
BACK_X = 24.0                                             # the backrest's front, out from the wall
ARM_W, ARM_H = 18.0, 62.0                                 # the arms: thick, high
CHAIR = (440.0, 486.0, 126.0, 172.0)                      # Jed's plastic chair: X0, X1, Z0, Z1 of its seat; it faces W (its back at X1)
CHAIR_SEAT, CHAIR_BACK = 45.9, 84.0
TABLE = (552.0, 330.0, 40.0, 74.0)                        # the round table in the near right: X, Z of its middle, its radius, its height
TABLE_CHAIRS = [(494.0, 322.0, 90.0)]                     # a plastic chair at it: X, Z, which way it faces (degrees: 0 toward us, 90 E, 180 away)
# OFFICE-17D (resumed): the low table in front of the couch's near end, in the near left, its near legs cut off by the
# picture's bottom edge: the foreground on that side (the round table is the right's). Out past the walk's front edge, so
# that nobody's feet go behind it. X0, X1, Z0, Z1, its height
LOWTABLE = (145.0, 295.0, 362.0, 446.0, 44.0)

# ---- where people are (X, Z on the floor). Seated people: the floor under their hips (the game draws them sitting).
MARKS = {
    "floyd": (50.0, 212.0),                               # asleep on the couch, at its far end, facing E (slumped: PEOPLE-17)
    "jed": (464.0, 149.0),                                # in his chair, facing W along the counter at the pie
    "door": (694.0, 100.0),                               # just inside the door, facing S (whoever comes in from the hall)
    "hall2": (628.0, 130.0), "hall3": (560.0, 160.0),     # the second and third of three who come in together, a step apart
    "vending": (562.0, 124.0),                            # in front of the snack machine (Ranger, on the floor; or anyone)
    "atfridge": (150.0, 112.0), "atcounter": (330.0, 104.0), "atsink": (262.0, 104.0), "atboard": (400.0, 104.0),
    "atcoffee": (452.0, 102.0), "atmicro": (166.0, 104.0), "atcouch": (150.0, 196.0), "attable": (600.0, 196.0),
    "atclock": (370.0, 110.0),
}
# Ranger's places off the floor: (X, Y, Z) on the fridge's top, the microwave's top, the counter's top
UP = {
    "fridge": (80.0, 195.0, 60.0),                        # on top of the fridge, under the grille, in front of the forks: where he drops to
    "micro": (158.0, 122.0, 30.0),                        # on the microwave: his step between the fridge and the counter
    "counter": (304.0, 90.0, 46.0),                       # on the counter beside the pie (to its left), facing E
    "sink": (264.0, 90.0, 56.0),                          # at the sink's front edge, washing (facing E)
    "board": (412.0, 90.0, 44.0),                         # on the counter at the corkboard, sitting up at the schedule
    "counter-end": (478.0, 90.0, 52.0),                   # the counter's right end, where he hops down to the floor
    "counter-left": (206.0, 90.0, 54.0),                  # just right of the microwave, where he comes down onto the counter
}
# the floor people may stand on: in front of the counter and the machine, clear of the couch, Jed's chair and the table,
# out to the door; its front edge keeps people under about 1.2 of full size
WALK = [(108.0, 84.0), (520.0, 76.0), (524.0, 98.0), (712.0, 98.0), (712.0, 150.0), (650.0, 206.0), (108.0, 206.0)]
# OFFICE-17D (resumed): the outline steps out round the snack machine's left side (it ran 1 to 4 pixels into its foot)
# Ranger's counter: the strip along the top's front where he walks (at Y 90)
COUNTER_WALK = [(192.0, 40.0), (494.0, 40.0), (494.0, 60.0), (192.0, 60.0)]

FLATS = [
    ("board", "back", BOARD[0], BOARD[1], BOARD[2], BOARD[3]),
    ("door", "back", DOOR[0], DOOR[1], DOOR[2], DOOR[3]),
    ("clock", "back", CLOCK[0] - CLOCK[2], CLOCK[0] + CLOCK[2], CLOCK[1] - CLOCK[2], CLOCK[1] + CLOCK[2]),
    ("calendar", "left", CALENDAR[0], CALENDAR[1], CALENDAR[2], CALENDAR[3]),
]
BOXES = [
    ("fridge", *FRIDGE),
    ("forks", *FORKS),
    ("counter", *COUNTER),
    ("micro", *MICRO),
    ("rack", *RACK),
    ("coffee", *COFFEE),
    ("cabinets", *CABINETS),
    ("vending", *VENDING),
    ("couch", *COUCH),
    ("chair", CHAIR[0], CHAIR[1], 0.0, CHAIR_BACK, CHAIR[2], CHAIR[3]),
    ("table", TABLE[0] - TABLE[2], TABLE[0] + TABLE[2], 0.0, TABLE[3], TABLE[1] - TABLE[2], TABLE[1] + TABLE[2]),
    ("trash", *TRASH),
    ("lowtable", LOWTABLE[0], LOWTABLE[1], 0.0, LOWTABLE[4], LOWTABLE[2], LOWTABLE[3]),             # OFFICE-17D (resumed)
]

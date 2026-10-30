"""Kihei's fish shop at Yui (scene `edo-fishshop`), about 8 April 1830, morning: the measurements, in centimetres
(room.py: X across, left to right; Y up; Z out from the street line toward us). PAINT-20B.

HOW IT IS SEEN. We stand at the back of the shop's earth floor (the doma) and look out through its OPEN FRONT: the
street, the beach, Suruga Bay and Fuji, small and white, in the opening. The raised tatami room is along the RIGHT,
a step up (the kamachi board at X 420, its floor at Y 45): guests sit on its edge, feet on the earth floor, facing
left into the shop. Kihei's cutting board, the tubs of fish, the sushi-box stand and the cooking hearth are along
the LEFT wall. The lens is LOW for a room of this game (2.20 m: horizon 200, full 401), below the lintel (2.80 m),
so that the sea's horizon and Fuji show in the opening; the floor people walk on is Z 20 to 370, as in the store.

LIGHT: the morning sky's light comes in at the open front, cool and bright; the inside is in the shade of its own
roof, warm-dark above the beams, and the hearth's fire is a small warm point (its flame and steam the engine's)."""
ID = "edo-fishshop"
VIEW = dict(horizon=200, full=401, cam=(300, 1000), yaw=6, focal=680, centre_x=400)
W, D = 640, 1000                       # the shop: width, and how far back the camera stands from the street line
LINTEL, EAVE, RIDGE = 280, 300, 420    # the beam over the open front; the wall head; the roof space above it
ROOM = dict(X=(0, W), Z=(0, D), H=RIDGE)
STEP_X, STEP_Y = 420, 45               # the raised room's edge (the kamachi) and its floor height
BACKWALL_Z = 180                       # where the raised floor begins, 1.8 m in from the street: open to the front (the right bay shows Fuji over the tatami)
POSTS = (0, 215, 430, 640)             # the open front's posts, at Z 0
POST_T = 14.0

# ---- beyond the opening (Z < 0): the street, the beach, the water
STREET = (0, -260)                     # the Tōkaidō in front of the shop: earth
BEACH = (-260, -620)                   # sand, down to the water
# the water from Z -620 to the horizon; Fuji on the horizon, seen in the right bay

# ---- the things (X0, X1, Y0, Y1, Z0, Z1 unless said)
TUBS = [(70, 60, 30, 44), (140, 95, 26, 40), (56, 150, 24, 36)]            # X, Z, radius, height: wooden tubs of fish in water, by the open front
BOARD = (16, 74, 70, 78, 140, 270)                                          # the long cutting board on its two trestles (Kihei's place in front of it)
TRESTLE_Z = (160, 250)
STAND = (124, 198, 0, 34, 285, 330)                                           # the low stand the sushi box is pressed on
SUSHIBOX = (140, 182, 34, 52, 292, 324)                                       # the wooden box on it (its three states)
HEARTH = (8, 112, 0, 56, 380, 462)                                          # the clay cooking hearth (kamado) against the left wall, in the foreground
POT = (60, 421, 26, 30)                                                     # X, Z, radius, height of the iron pot on it (its mouth at Y 86)
CHEST = (560, 640, 45, 125, 240, 330)                                       # O-Tami's clothes chest on the tatami against the right wall
BASKET = (470, 540, 45, 75, 420, 480)                                       # the baby's basket on the tatami, near us
MONEYBOX = (440, 484, 45, 69, 190, 226)                                     # the money box on the tatami at its front edge by the step, where the shopkeeper sits to be paid
GODSHELF = (640, 232, 262, 300, 380)                                        # X (the right wall), Y0, Y1, Z0, Z1: a small plain shelf with a tiny shrine on it
PRINT = (430, 150, 206, 0)                                                  # the print of Fuji on a board hung on the post at X 430's inner face (facing left into the shop): Y0..Y1; 40 wide, Z -16..24
HATS = ((0, 60, 185, 225), (0, 118, 180, 220))                              # on the left wall (X 0): Z, Z, Y0, Y1 (two sedge hats hung by the front)
SANDALS = (40, 140, 200, 262, 0)                                            # hanging from the lintel beside the left bay: X0, X1, Y0, Y1 (pairs on a cord)
DRIEDFISH = (0, 100, 400, 215)                                              # along the left wall: X, Z0, Z1, Y of the line (fish split and hung)
NOREN = (215, 430, 200, 280)                                                # the noren across the middle bay: X0, X1, Y0, Y1 at Z 0 (two panels)
UNDER = (420, 0, 36, 200, 300)                                              # the gap under the raised floor: X, Y0, Y1, Z0, Z1 (the cat's way; a seven-year-old fits)

# ---- where people stand (X, Z) and face; the step's seats are the ground under the hips, seat 45 cm (STEP_Y)
MARKS = {
    "door": (300, 70), "kihei": (118, 205), "press": (246, 312), "tami": (196, 362),
    "step": (402, 260), "stepmom": (402, 200), "stepbig": (402, 260), "steplil": (402, 320),
    "baby": (380, 352), "hearth": (238, 372), "print": (396, 84), "money": (376, 208), "godshelf": (378, 336),
    "cat": (300, 262), "under": (390, 250), "tubs": (150, 150), "board": (150, 205), "chest": (378, 286), "noren": (322, 60),
}
FACE = {"door": "S", "kihei": "W", "press": "W", "tami": "W", "step": "W", "stepmom": "W", "stepbig": "W", "steplil": "W", "baby": "E",
        "hearth": "W", "print": "N", "money": "E", "godshelf": "E", "cat": "W", "under": "E", "tubs": "W", "board": "W", "chest": "E", "noren": "N"}
# the earth floor people may stand on: inside the open front, clear of the tubs, the board, the stand (a notch round it) and the
# hearth at the left, and of the raised floor at the right (15 cm short of the kamachi); its front edge keeps people under 195 px;
# the slot between the stand and the hearth (Z 336..378, X 112..240) is O-Tami's place
WALK = [(176, 20), (600, 20), (600, 166), (405, 166), (405, 372), (240, 380), (112, 378), (112, 336), (210, 336), (210, 281), (100, 281),
        (100, 130), (176, 130)]

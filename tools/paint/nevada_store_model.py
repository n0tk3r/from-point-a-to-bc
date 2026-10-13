"""The inside of Grandpa Joe's Last Stop (scene `nevada-store`): the measurements of the room and everything in
it, in centimetres (see room.py: X across, left to right; Y up; Z out from the back wall toward us).

HOW IT IS SEEN. We stand just inside the front door and look along the store at its far wall: the front wall of
the shack, with the front window (the porch, the rocking chair's back, the lot and the road outside it) and the
front door, is the LEFT wall; the far wall (the "back wall" of the picture) has the drinks cooler in its left
corner, the long counter in the middle with the hubcaps over it, and the back door at its right, open on the hen
yard. Morning: the sun is low behind us and to the left; it comes in at the window and lies across the floor
toward the counter. Through the back door the light is the sky's, cool; the yard beyond the shack's shadow is in sun.

THE CHEAT. The camera is 3.25 m up and stands at the room's near end (Z = 1040), so the floor is broad; people walk
down to about Z = 415 (50 rows below `full`); what is nearer is foreground, cut off by the picture's bottom edge.

The camera numbers (VIEW) and the shell (ROOM, the window, the two doors) are the scene's; everything else is the
furniture as it is PAINTED (nevada_store.py reads these same numbers)."""
ID = "nevada-store"
VIEW = dict(horizon=158, full=455, cam=(520, 1040), yaw=-12, focal=680, centre_x=400)
W, D, H = 760, 1040, 390                                    # the room: width, depth, the ceiling
ROOM = dict(X=(0, W), Z=(0, D), H=H)
WALL_T = 12.0                                               # how thick the walls are (the openings' reveals)

# ---- the shell's openings
WINDOW = (66, 330, 84, 204)                                 # on the left wall: Z0, Z1, Y0, Y1 of the glass (two sashes)
MULLION = 198.0                                             # the post between the sashes: the shade stands in the far one
FRONTDOOR = (382, 468, 0, 205)                              # on the left wall: Z0, Z1, Y0, Y1 of the doorway (the way out, at the picture's left edge)
BACKDOOR = (588, 708, 0, 205)                               # on the back wall: X0, X1, Y0, Y1 of the doorway, a wide delivery door (the screen door stands open, inside, to its left)
STEP = -18.0                                                # the yard is a step down
STEP_DEPTH = 34.0                                           # the concrete step outside the back door: from the wall's outer face out this far
FENCE_Z = -400.0                                            # the chain-link fence, this far beyond the back wall

# ---- the sun: the way to it from inside the room (low, behind us and to the left)
SUN = (-0.86, 0.40, 0.17)

# ---- standing on the floor (X0, X1, Y0, Y1, Z0, Z1)
COOLER = (66, 158, 0, 196, 0, 72)                           # Harold, the drinks cooler, against the far wall at the left, his glass door toward us
COUNTER = (168, 450, 0, 92, 96, 166)                        # the counter, its front toward us
GRILL = (450, 534, 0, 92, 96, 166)                          # the grill unit at the counter's right end (cold): a griddle, and the roller on it
GRIDDLE = (454, 490, 92, 97, 104, 158)
ROLLER = (494, 530, 92, 112, 110, 152)                      # the hot dog roller (its frames: roller-0, roller-1)
REGISTER = (350, 410, 92, 140, 104, 150)                    # the register on the counter
PENNYDISH = (316, 340, 92, 96, 128, 154)                    # the take-a-penny dish beside it
EGGS = (234, 92, 136, 128, 16.0)                            # the jar of pickled eggs: X, Y0, Y1, Z, radius
POSTCARDS = (196, 92, 158, 130, 14.0)                       # the postcard rack on the counter's left end: X, Y0, Y1, Z, radius
MAPRACK = (382, 440, 22, 86, 166, 176)                      # the map rack hung on the counter's front, right half
BASKET = (184, 228, 0, 28, 170, 206)                        # Ranger's basket at the counter's foot, our side, left end
CHAIR = (713, 757, 0, 92, 12, 58)                           # Jolene's chair right of the back door, side-on to us (she watches her hens from it), the knitting on its seat
SURVIVAL = (2, 62, 0, 172, 0, 42)                           # the survival shelf, in the far left corner against the back wall
TV = (8, 54, 172, 206, 4, 40)                               # the TV on top of it, rabbit ears up
AUTOSHELF = (0, 34, 0, 68, 130, 330)                        # the auto shelf, under the window
SPINNER = (112, 262, 172)                                   # the spinner rack: X, Z of its post, its height
SPINNER_R = 22.0
ROCKBINS = (548, 748, 0, 72, 240, 308)                      # the rock bins: a sloping tray of five bins on legs, out on the floor at the right
FAN = (430, 368, 640)                                       # the ceiling fan, a hugger close under the tin: X, Y of the blades, Z
MAT = (18, 150, 384, 468)                                   # the doormat inside the front door: X0, X1, Z0, Z1
WATERFLATS = (26, 160, 0, 40, 560, 660)                     # front plane: a stack of water flats at the bottom left, cut off by the picture's edge
TIRES = (668, 568, 34.0, 3)                                 # front plane: old tyres stacked at the bottom right: X, Z of the stack, the tyre's radius, how many
CRATE = (300, 452, 0, 44, 580, 660)                         # front plane: a crate of empty pop bottles, bottom middle

# ---- on the walls (X0, X1, Y0, Y1 on the back wall)
BULLETIN = (162, 300, 106, 218)                             # the bulletin board, on the back wall behind the counter's left end
HATRACK = (276, 486, 228, 238)                              # the hat board, high on the back wall over the counter: five pegs
HAT_PEGS = (296, 344, 392, 440, 476)                        # the X of each peg (hats 1 to 5)
PAYPHONE = (718, 754, 124, 184)                             # the pay phone, over Jolene's chair
HUBCAPS = 112

FLATS = [
    ("window", "left", *WINDOW),
    ("backdoor", "back", *BACKDOOR),
    ("frontdoor", "left", *FRONTDOOR),
    ("bulletin", "back", *BULLETIN),
    ("hatrack", "back", HATRACK[0], HATRACK[1], 196, 240),
    ("payphone", "back", *PAYPHONE),
]
BOXES = [
    ("cooler", *COOLER),
    ("counter", *COUNTER),
    ("grill", *GRILL),
    ("roller", *ROLLER),
    ("register", *REGISTER),
    ("eggs", EGGS[0] - EGGS[4], EGGS[0] + EGGS[4], EGGS[1], EGGS[2], EGGS[3] - EGGS[4], EGGS[3] + EGGS[4]),
    ("postcards", POSTCARDS[0] - POSTCARDS[4], POSTCARDS[0] + POSTCARDS[4], POSTCARDS[1], POSTCARDS[2], POSTCARDS[3] - POSTCARDS[4], POSTCARDS[3] + POSTCARDS[4]),
    ("maprack", *MAPRACK),
    ("basket", *BASKET),
    ("chair", *CHAIR),
    ("survival", *SURVIVAL),
    ("tv", *TV),
    ("autoshelf", *AUTOSHELF),
    ("spinner", SPINNER[0] - SPINNER_R, SPINNER[0] + SPINNER_R, 0, SPINNER[2], SPINNER[1] - SPINNER_R, SPINNER[1] + SPINNER_R),
    ("rockbins", *ROCKBINS),
    ("waterflats", *WATERFLATS),
    ("tires", TIRES[0] - TIRES[2], TIRES[0] + TIRES[2], 0, TIRES[3] * 19, TIRES[1] - TIRES[2], TIRES[1] + TIRES[2]),
    ("crate", *CRATE),
]
# where people stand (X, Z)
MARKS = {
    "mom": (190, 330), "bigsis": (290, 368), "lilsis": (96, 382),            # fromLot: just inside the front door, in that order
    "jolene": (338, 46), "jolene2": (424, 46),                               # behind the counter: her two spots
    "counter": (330, 232), "step": (616, -28),                               # a customer at the counter; Little Sister on the back step
    "atregister": (382, 232), "atpennydish": (330, 232), "ateggs": (240, 232), "atpostcards": (206, 232), "atbasket": (236, 250),
    "athatrack": (420, 232), "atbulletin": (220, 232), "atmaprack": (412, 236), "athubcaps": (300, 240),
    "atwindow": (88, 196), "atshade": (88, 150), "atspinner": (170, 270), "atcooler": (112, 116), "atsurvival": (72, 112), "attv": (72, 112),
    "atgrill": (500, 230), "atroller": (512, 230), "atchair": (690, 80), "atpayphone": (696, 74), "atbackdoor": (632, 40), "watchleft": (566, 84), "watchright": (712, 92),
    "atautoshelf": (76, 300), "atrockbins": (640, 336), "atfan": (430, 330), "atdoor": (70, 418),
    "front": (400, 394), "frontright": (556, 362),
}
# the floor people may stand on: in front of the counter and the grill, clear of the shelf and the cooler in the far
# left corner, the window's shelf, the chair and the rock bins; out to the back door's sill; back to the front door's
# threshold. Its front edge keeps people under about 190 px (the camera is turned, so that edge runs on a slant).
WALK = [(50, 92), (162, 92), (162, 190), (534, 190), (534, 70), (600, 70), (600, -40), (694, -40), (694, 70), (736, 70), (736, 226),
        (534, 226), (534, 322), (736, 322), (736, 338), (650, 356), (560, 375), (450, 399), (350, 420), (250, 442), (150, 463), (60, 482),
        (14, 486), (14, 382), (50, 382)]
STEP_WALK = [(600, 0), (694, 0), (694, -40), (600, -40)]                    # the step outside the back door (mark `step`): part of WALK

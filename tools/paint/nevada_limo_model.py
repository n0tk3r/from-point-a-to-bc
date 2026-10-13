"""The inside of the men in gray's limousine (nevada-limo): the measurements, in centimetres.

We sit on the back seat and look forward, down the length of the car, at the divider. X runs across the car from
the left wall (0) to the right wall (W); Y is up from the carpet; Z runs from the divider's glass (0) toward us.

THE CARTOON'S CHEAT. The game draws a grown-up 160 px tall on the row `full`, and the brief wants Grandpa Joe, seated
on the long seat near the divider, at about 0.8 of that (so a centimetre is about 0.72 px where he sits), Ranger on
the carpet near us at about 0.95, and the divider readable behind Joe. A real limousine is 1.7 m wide and 1.3 m high
inside: at Joe's depth it would be 120 px wide, a drinking straw, and his hat would be in the headliner. So this
limousine's inside is roomy the way a cartoon's is: 3.5 m across, 1.82 m high, the divider 5.3 m in front of our eye,
with the seats themselves at human size (a cushion 42 cm high, a backrest to 100 cm), and the camera a wide lens at a
seated eye and a little above (148 cm, from horizon 220 and full 355). The far end of the car is where everything
happens; the near end flares toward us, as a wide lens flares it, and our own seat's cushion is the foreground.

Marks: Joe's is the ground point under his hips (it lies under the long seat's cushion: the game draws a seated person
there, his hips at the seat's height above it); Ranger's is on the carpet; `ropes` is a point ON the long seat's
cushion (Y = SEAT_H) where Ranger sits to nibble. Nobody stands in a car.

The camera numbers (VIEW) are the scene's own (see the painter's README, "Painting a room"): change any of them and the
scene file must be measured again. Everything else here is the furniture as it is painted: nevada_limo_things.py and
nevada_limo.py read these same numbers, so the skeleton, the picture and layout.json agree."""

ID = "nevada-limo"

# ---- the shell
W, H, L = 350.0, 182.0, 480.0                           # across, high, long (the divider's glass is Z = 0; the back seat ends at Z = L)
VIEW = dict(horizon=220, full=355, cam=(182.0, 530.0), yaw=-4.0, focal=345.0, centre_x=400.0)
ROOM = dict(X=(0.0, W), Z=(0.0, L), H=H)

SEAT_H, SEAT_D, BACK_H, BACK_T = 42.0, 66.0, 100.0, 16.0     # a cushion's height and depth (backrest included); a backrest's top and thickness
WINDOW_Y = (103.0, 166.0)                                   # the glass, from just above the backrests' tops up toward the headliner
PANES = {                                                   # each wall's two panes, Z from .. to; the pillar between them
    "L": [(34.0, 196.0), (214.0, 412.0)],
    "R": [(34.0, 196.0), (214.0, 412.0)],
}
PILLAR = (196.0, 214.0)

# ---- the divider: the partition at Z = 0. Its lower part is the front seats' backs; the glass slides in a frame above.
DIVIDER = dict(sill=80.0, top=166.0, x=(30.0, 320.0), frame=8.0)      # the opening: from the sill to its top, between these X

# ---- the long seat (left) and the facing seat (right), along the walls, from near the divider to the seat we sit on
LONG_SEAT = (0.0, SEAT_D, 0.0, SEAT_H, 30.0, 394.0)        # X0, X1, Y0, Y1, Z0, Z1 (the cushion; its backrest stands on its wall side)
FACING_SEAT = (W - SEAT_D, W, 0.0, SEAT_H, 58.0, 394.0)
BACK_SEAT = (0.0, W, 0.0, SEAT_H, 394.0, L)                 # the one we sit on: its front edge (Z = 394) is the foreground's top
ARMREST_L = (0.0, 40.0, SEAT_H, SEAT_H + 26.0, 394.0, 426.0)     # padded ends where the side seats meet ours
ARMREST_R = (W - 40.0, W, SEAT_H, SEAT_H + 26.0, 394.0, 426.0)

# ---- the far end: a low bar under the divider between the two seats, the car phone and the ashtray on it
BAR = (SEAT_D + 4.0, W - SEAT_D - 4.0, 0.0, 66.0, 0.0, 44.0)
PHONE = dict(at=(116.0, 66.0, 24.0), cradle=(26.0, 7.0, 12.0))        # the cradle's middle on the bar top; its width, height, depth
ASHTRAY = dict(at=(232.0, 66.0, 24.0), r=11.0, h=5.5)
# ---- the fridge: in the facing seat's base at its near end, its door to the carpet
FRIDGE = (W - SEAT_D - 1.0, W, 2.0, SEAT_H - 3.0, 300.0, 384.0)

# ---- on the facing seat, far to near: the paper bag, the juice box, the clipboard (propped against the backrest, turned to us)
BAG = dict(at=(W - 36.0, SEAT_H, 176.0), w=19.0, d=13.0, h=29.0)
JUICE = dict(at=(W - 40.0, SEAT_H, 248.0), w=9.0, d=6.0, h=13.0)
CLIPBOARD = dict(at=(W - 34.0, SEAT_H, 318.0), w=24.0, h=33.0, tilt=24.0)   # tilt: degrees it leans back from upright

# ---- Grandpa Joe, the ropes beside him, the seatbelt's buckle end on the cushion
JOE = (36.0, 62.0)                                          # X, Z of the ground point under his hips (he faces E, across the car)
ROPES = dict(at=(40.0, SEAT_H, 104.0))                      # the bow lies on the cushion beside his hands; its loose end runs toward us
BELT = dict(at=(SEAT_D - 12.0, SEAT_H, 168.0))              # the buckle, lying on the cushion near its edge; its strap comes out of the seat's crease

# ---- the ceiling: a row of small lights down the middle, from the divider to us
LIGHTS = [(W / 2, 40.0), (W / 2, 125.0), (W / 2, 210.0), (W / 2, 295.0), (W / 2, 380.0)]     # X, Z (at Y = H)
LIGHT_R = 6.0

# ---- marks: where the game puts people (X, Z on the floor). Nobody stands: Joe sits, Ranger is a raccoon.
MARKS = {
    "joe": JOE,                                             # seated on the long seat, facing E
    "ranger": (180.0, 148.0),                               # on the carpet, between the seats, near us
    "ropes": (ROPES["at"][0] + 2.0, ROPES["at"][2] + 16.0),        # where Ranger sits to nibble: ON the cushion (at SEAT_H), beside the bow, toward us
}
# the master brief's fixed marks `bag`, `juice`, `clipboard` (X, Z): ON the facing seat's cushion (at SEAT_H), where each
# thing stands. Kept apart from MARKS (which the room tools stand people on, on the carpet); layout.json gives each one
# with the size a figure is drawn at there. Ranger takes each thing from the carpet, at his stands; only the bag is far
# enough from us for him to be drawn on the seat beside it (about 1.1): the juice box (1.4) and the clipboard (1.9) are
# nearer than the engine draws painted frames (never more than 1.25 of their size).
ON_FACING_SEAT = {"bag": (BAG["at"][0], BAG["at"][2]), "juice": (JUICE["at"][0], JUICE["at"][2]), "clipboard": (CLIPBOARD["at"][0], CLIPBOARD["at"][2])}
# Ranger's stand places on the carpet, for each thing (X, Z), and which way he faces there
STANDS = {
    "atropes": ((SEAT_D + 18.0, 112.0), "W"), "atjoe": ((SEAT_D + 22.0, 74.0), "W"), "atbelt": ((SEAT_D + 18.0, 170.0), "W"),
    "atphone": ((116.0, 64.0), "N"), "atashtray": ((230.0, 64.0), "N"), "atdivider": ((175.0, 60.0), "N"),
    "atbag": ((W - SEAT_D - 20.0, 170.0), "E"), "atjuice": ((W - SEAT_D - 18.0, 200.0), "E"), "atclipboard": ((W - SEAT_D - 26.0, 206.0), "E"),
    "atfridge": ((W - SEAT_D - 34.0, 208.0), "E"), "atwindow-l": ((SEAT_D + 16.0, 150.0), "W"), "atwindow-r": ((W - SEAT_D - 16.0, 140.0), "E"),
}
# the carpet a raccoon may walk on: between the seats, from the bar to where he is drawn at about 1.23 (the engine never
# draws painted frames more than 1.25 of their size: the scene's maxScale must be at least the walk's, layout.json `maxScale`)
WALK = [(SEAT_D + 6.0, 54.0), (W - SEAT_D - 6.0, 54.0), (W - SEAT_D - 6.0, 214.0), (SEAT_D + 6.0, 220.0)]

FLATS = [
    ("divider", "back", DIVIDER["x"][0], DIVIDER["x"][1], DIVIDER["sill"], DIVIDER["top"]),
    ("window-l-far", "left", PANES["L"][0][0], PANES["L"][0][1], WINDOW_Y[0], WINDOW_Y[1]),
    ("window-l-near", "left", PANES["L"][1][0], PANES["L"][1][1], WINDOW_Y[0], WINDOW_Y[1]),
    ("window-r-far", "right", PANES["R"][0][0], PANES["R"][0][1], WINDOW_Y[0], WINDOW_Y[1]),
    ("window-r-near", "right", PANES["R"][1][0], PANES["R"][1][1], WINDOW_Y[0], WINDOW_Y[1]),
]
BOXES = [
    ("seat", *LONG_SEAT),
    ("seat-back", 0.0, BACK_T, SEAT_H, BACK_H, LONG_SEAT[4], LONG_SEAT[5]),
    ("facingseat", *FACING_SEAT),
    ("facing-back", W - BACK_T, W, SEAT_H, BACK_H, FACING_SEAT[4], FACING_SEAT[5]),
    ("bar", *BAR),
    ("fridge", *FRIDGE),
    ("bag", BAG["at"][0] - BAG["w"] / 2, BAG["at"][0] + BAG["w"] / 2, SEAT_H, SEAT_H + BAG["h"], BAG["at"][2] - BAG["d"] / 2, BAG["at"][2] + BAG["d"] / 2),
    ("juice", JUICE["at"][0] - JUICE["w"] / 2, JUICE["at"][0] + JUICE["w"] / 2, SEAT_H, SEAT_H + JUICE["h"], JUICE["at"][2] - JUICE["d"] / 2, JUICE["at"][2] + JUICE["d"] / 2),
    ("clipboard", CLIPBOARD["at"][0] - 8.0, CLIPBOARD["at"][0] + 8.0, SEAT_H, SEAT_H + 30.0, CLIPBOARD["at"][2] - CLIPBOARD["w"] / 2, CLIPBOARD["at"][2] + CLIPBOARD["w"] / 2),
    ("phone", PHONE["at"][0] - 16.0, PHONE["at"][0] + 16.0, 66.0, 79.0, PHONE["at"][2] - 7.0, PHONE["at"][2] + 7.0),
    ("ashtray", ASHTRAY["at"][0] - 11.0, ASHTRAY["at"][0] + 11.0, 66.0, 71.5, ASHTRAY["at"][2] - 11.0, ASHTRAY["at"][2] + 11.0),
    ("armrest-l", *ARMREST_L),
    ("armrest-r", *ARMREST_R),
    ("backseat", *BACK_SEAT),
]

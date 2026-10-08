"""Little Sister's room (it was the girls' room): a big room under the roof. We look along the ridge at the far
gable wall and its window. She is seven; what she loves above everything is CHICKENS, and after chickens, stuffed animals.

The camera and the shell (VIEW, W, KNEE, RIDGE, ROOM, POLYS) are fixed, and so are the blanket fort, the flashlight in
its way in, and the door at the picture's right edge: the game's scene file is written against them. Everything else
below is as PAINTED (home_lilsis_room.py reads its measurements from here).

LEFT: the flock (a mountain of stuffed animals, the chickens on top) by the far wall where the old bed was; the fort.
MIDDLE: the tea party (every guest a chicken), on the open floor. RIGHT: her bed along the right wall, its pillow at the
far end with one place kept free and a sign, RESERVED; a bedside table with the rooster lamp. FAR WALL: her drawings
(left of the window), the chicken chart (right of it), a small coat on a peg and her boots.
FRONT PLANE: her toy box, a crate of picture books, the toy hen house (the dollhouse, with a ramp), the nest (a
cardboard box, straw, a hen, plastic eggs), a mobile of felt chickens, and the door to the landing."""
ID = "home-lilsis-room"
VIEW = dict(horizon=120, full=440, cam=(310, 1210), yaw=6, focal=800, centre_x=400)
W, D, KNEE, RIDGE = 720, 430, 130, 420
ROOM = dict(X=(0, W), Z=(0, 1210), H=KNEE)
POLYS = [
    ("gable", [(0, 0, 0), (W, 0, 0), (W, KNEE, 0), (W / 2, RIDGE, 0), (0, KNEE, 0)], (150, 132, 118)),
    ("roof-left", [(0, KNEE, 0), (W / 2, RIDGE, 0), (W / 2, RIDGE, 1210), (0, KNEE, 1210)], (122, 106, 96)),
    ("roof-right", [(W, KNEE, 0), (W / 2, RIDGE, 0), (W / 2, RIDGE, 1210), (W, KNEE, 1210)], (104, 90, 84)),
]
WINDOW = (300, 420, 105, 290)                            # X0, X1, Y0, Y1 on the gable wall
CHART = (434, 566, 78, 190)                              # the chicken chart, on the gable to the right of the window
DRAWINGS = (86, 292, 92, 262)                            # the cluster of her drawings on the gable, left of the window
FLATS = [
    ("window", "back", *WINDOW),
    ("chart", "back", *CHART),
    ("drawings", "back", *DRAWINGS),
]
FLOCK = (66, 268, 0, 104, 12, 114)                       # the mountain of stuffed animals (where the old bed was)
FORT = (8, 198, 0, 110, 292, 402)                        # UNCHANGED: ridge 110 high along Z at X = 96; shoulders 62
BED = (606, 706, 0, 44, 192, 392)                        # her bed along the right wall: 44 = the top of the mattress
PILLOW = (614, 698, 44, 57, 197, 248)                    # at the far end; the RESERVED sign stands at its back
LAMPTABLE = (564, 602, 0, 48, 200, 240)                  # the bedside table; the rooster lamp stands on it
TEAPARTY = (392, 524, 0, 84, 222, 352)                   # the low table and its guests (cut-out teaparty.png)
TEATABLE = (458, 286, 35, 46)                            # the table itself: middle X, middle Z, radius, height
EGGRUG = (318, 300, 84, 62)                              # a rug like a fried egg: middle X, middle Z, half-width, half-depth
COOP = (286, 410, 0, 82, 526, 596)                       # front plane: the toy hen house (the dollhouse); its front faces us
NEST = (478, 552, 0, 36, 572, 622)                       # front plane: the cardboard nesting box
TOYBOX = (84, 166, 0, 44, 548, 602)                      # front plane
CRATE = (188, 250, 0, 27, 562, 606)                      # front plane: picture books in a low crate
MOBILE = (566, 232, 430)                                 # front plane: the felt chickens hang here (X, the height of the hub, Z)
DOOR_X, DOOR_Z, DOOR_H = 614, (606, 694), 203            # UNCHANGED: the open leaf stands along X = 614; its hinge is at Z = 694
BOXES = [
    ("flock", *FLOCK),
    ("fort", *FORT),
    ("bed", *BED),
    ("pillow", *PILLOW),
    ("lamptable", *LAMPTABLE),
    ("teaparty", *TEAPARTY),
    ("coop", *COOP),                                     # front plane
    ("nest", *NEST),                                     # front plane
    ("toybox", *TOYBOX),                                 # front plane
    ("crate", *CRATE),                                   # front plane
    ("door", DOOR_X, DOOR_X + 4, 0, DOOR_H, *DOOR_Z),    # front plane
]
MARKS = {"mom": (512, 424), "bigsis": (452, 432), "lilsis": (572, 436),
         "atfort": (222, 398), "atbed": (572, 312), "atflock": (288, 152), "atnest": (512, 446), "atteaparty": (378, 292),
         "atchart": (536, 100), "atwindow": (360, 84), "atdoor": (598, 446)}
WALK = [(300, 76), (548, 76), (548, 248), (592, 252), (592, 400), (606, 404), (606, 452), (446, 452), (446, 372), (262, 372),
        (262, 404), (212, 404), (212, 282), (224, 264), (224, 150), (290, 132), (300, 112)]      # (the notch: the hen house's roof stands before that floor)
BLOCKED = [[(396, 228), (522, 228), (522, 352), (396, 352)]]      # the tea party stands in the middle of the floor

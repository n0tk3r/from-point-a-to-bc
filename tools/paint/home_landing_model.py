"""The upstairs landing: the gallery that crosses the back of the living room, seen from out over the room.

Same house, same measurements as home_living_room_model.py, except that heights are measured from the LANDING's
floor (the living room's floor is 285 below). The stairs come up at the far left end. We hang in the air at the
front right of the big room, level with the landing, and look along it.

The camera, the room, the floors, the railing's slab and the stairs are as given. The furniture is as painted
(home_landing.py reads the marks, the stand places and the walk outline from here)."""
ID = "home-landing"
VIEW = dict(horizon=135, full=322, cam=(775, 760), yaw=-40, focal=560, centre_x=400)
ROOM = dict(X=(0, 780), Z=(0, 1100), H=275, Y0=-285)
FLOORS = [(-285, 0, 780, 0, 1100), (0, 108, 780, 0, 175), (0, 0, 108, 0, 175)]
SLABS = [
    ("rail", 108, 780, 88, 95, 172, 178),
]
FLATS = [
    ("son", "back", 190, 275, 0, 205),
    ("lilsis", "back", 400, 485, 0, 205),                 # Little Sister's door, hers alone now (it was the girls' door)
    ("study", "back", 610, 695, 0, 205),
    ("sign", "back", 613.5, 691.5, 104, 168),          # Dad's notice: a big sheet of chart paper (it has to be read)
    ("window", "left", 240, 400, -55, 215),
    ("photos", "back", 293, 387, 105, 179),
    ("chart", "back", 500, 595, 124, 162),             # the long strip of paper over the hall table (the model's second frame): a countdown to the trip
    ("photos2", "back", 118, 170, 120, 176),           # two more photographs by the head of the stairs
    ("picture", "left", 76, 122, 118, 156),            # a small framed picture at the head of the stairs
]
BOXES = [
    ("halltable", 503.5, 591.5, 0, 78, 1, 33.5),
    ("lamp", 508, 546, 78, 139, 2, 34),                 # the lamp on it (lit); the key bowl is at 550..570, the day's post beside it
    ("hamper", 295.5, 346.5, 0, 71, 2, 41.5),          # with folded washing on its lid
    ("bag", 148, 178, 62, 104, 0, 12),                  # the Son's school bag on its peg, his shoes under it
    ("hatch", 514, 590, 272, 275, 44, 122),             # the attic hatch, open, in the ceiling over the hall table (it was at X 479..557, shut)
    ("ladder", 516, 627, 0, 275, 50, 108),              # the attic ladder let down from it: its top at X 516 under the ceiling, its feet at X 627
    ("post1", 103, 113, 0, 102, 170, 180),              # newel posts of the railing, where the living room has them
    ("post2", 271, 281, 0, 102, 170, 180),
    ("post3", 439, 449, 0, 102, 170, 180),
    ("post4", 607, 617, 0, 102, 170, 180),
    ("quilt", 698, 766, 22, 97, 170, 182),              # a patchwork quilt hung over the railing to air: front plane
    ("hanging-light", 300, 376, -54, 26, 402, 478),     # out in the room, on a long chain from a beam: front plane
]
STAIRS = [dict(id="stairs", X=(0, 108), z_foot=575, z_top=175, rise=285, steps=16, floor=-285)]

# where the three stand when they arrive by each way in (X, Z)
WAYS = {
    "fromStairs": {"lilsis": (118, 134), "bigsis": (170, 100), "mom": (296, 120)},
    "fromLilsis": {"bigsis": (442, 72), "lilsis": (368, 116), "mom": (522, 110)},
    "fromStudy": {"mom": (652, 74), "bigsis": (574, 112), "lilsis": (500, 92)},
    "fromLadder": {"bigsis": (650, 80), "mom": (590, 140), "lilsis": (690, 120)},      # just come down: one at its foot, the others stepped clear
}
# where a person stands to use each thing (X, Z) and which way they then look
STANDS = {
    "stairs": ((126, 146), "W"), "son": ((232, 64), "N"), "lilsis": ((442, 64), "N"), "study": ((652, 64), "N"), "sign": ((652, 64), "N"),
    "halltable": ((548, 62), "N"), "photos": ((340, 70), "N"), "hamper": ((322, 68), "N"), "ladder": ((650, 80), "W"),
    "window": ((132, 112), "W"), "rail": ((486, 150), "S"),
}
MARKS = {**WAYS["fromLilsis"], "atstudy": STANDS["study"][0], "atstairs": STANDS["stairs"][0], "atson": STANDS["son"][0],
         "attable": STANDS["halltable"][0], "atrail": STANDS["rail"][0]}
WALK = [(114, 46), (706, 46), (716, 158), (114, 158)]
# (the newel posts of the railing stand at X 108, 276, 444 and 612: in the picture they are at x 314, 395, 504 and 654, and every
#  mark and stand place above is clear of them)

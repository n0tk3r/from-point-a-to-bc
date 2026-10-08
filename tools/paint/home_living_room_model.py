"""The living room: the measurements of the room and everything in it, in centimetres (see room.py).

A two-storey room. The stairs climb the LEFT wall from the front of the room to a landing that crosses the
back wall upstairs (the "gallery"). Under the landing, at the back: bookcase, the way through to the kitchen,
the framed Preamble, the piano, the front door. We stand at the front right of the room, a little turned to
the left.

The camera numbers and the shell (walls, stairs, gallery) are as they were given. The furniture is as it is
PAINTED (home_living_room.py reads this file): the dinner table now runs away from us (its head is its far
end, where Dad's chair faces us), the armchair is turned toward the room with its lamp on its far side, the
piano and the door have moved a little to make room for a print and a sampler large enough to be read (the door
is a low old one, 191 with its frame, because the landing's edge hides the top of the wall over it; its fanlight
is set in the door's own head; the coats hang on the right-hand wall beside it)."""
ID = "home-living-room"
VIEW = dict(horizon=150, full=455, cam=(620, 1150), yaw=-18, focal=680, centre_x=400)
ROOM = dict(X=(0, 780), Z=(0, 1150), H=560)
G = 285          # the upstairs floor
SLABS = [
    ("gallery", 108, 780, G - 18, G, 0, 175),               # the landing across the back
    ("rail", 108, 780, G + 88, G + 95, 172, 178),           # its handrail (balusters under it)
]
FLATS = [
    # under the landing, on the back wall
    ("kitchen", "back", 268, 400, 0, 225),
    ("frame", "back", 410, 490, 132, 240),                  # "We the People"
    ("clock", "back", 519, 557, 197, 235),
    ("door", "back", 664, 760, 0, 191),                   # a low old door: the sampler needs the wall over it
    ("sampler", "back", 651, 773, 193.5, 251),
    # upstairs, on the back wall
    ("up-son", "back", 190, 275, G, G + 205),
    ("up-girls", "back", 400, 485, G, G + 205),
    ("up-study", "back", 610, 695, G, G + 205),
    # the stair wall
    ("window", "left", 240, 400, 230, 500),
    ("photos", "left", 415, 600, 130, 416),                 # frames climbing with the stairs, a landscape above them
    # the cupboard under the stairs: a low door in the panelling
    ("closet", ("X", 108), 320, 400, 0, 108),
    # coats on hooks beside the front door, on the right-hand wall
    ("coats", "right", 22, 150, 70, 190),
]
BOXES = [
    ("books", 118, 250, 0, 218, 0, 34),
    ("piano", 496, 646, 0, 128, 0, 62),
    ("stool", 531, 611, 0, 48, 80, 116),                    # a bench: two can sit
    ("rug", 245, 565, 0, 1, 225, 475),
    ("armchair", 242, 362, 0, 102, 688, 806),               # turned 25 degrees toward the room: the box round it
    ("lamp", 221, 247, 0, 152, 722, 748),                   # the reading lamp, on the armchair's far side
    ("table", 545, 655, 0, 76, 578, 788),                   # the head of the table is its far end
    ("chair-head", 578, 622, 0, 98, 535, 583),              # Dad's
    ("chair-left-far", 505, 553, 0, 98, 606, 650),          # the Son's
    ("chair-left-near", 468, 528, 0, 98, 692, 752),
    ("chair-right-far", 652, 704, 0, 98, 602, 652),
    ("chair-right-near", 652, 716, 0, 98, 700, 764),
    ("pendant", 576, 624, 160, 183, 662, 710),              # the lamp over the table
    ("chandelier", 392, 468, 318, 392, 362, 438),           # hangs over the rug; not lit tonight
    ("plant", 744, 776, 0, 170, 416, 448),                  # a rubber plant by the right-hand wall
    ("basket", 376, 420, 0, 34, 689, 719),                  # newspapers, by the armchair
    ("phone-table", 109, 131, 0, 74, 92, 150),              # against the panelling: telephone, pad, flowers
]
STAIRS = [dict(id="stairs", X=(0, 108), z_foot=575, z_top=175, rise=G, steps=16)]
# where the lamps are (X, Y, Z): the pools of light the landing picture sees from above
LIGHTS = {"pendant": (600, 166, 686), "reading": (234, 150, 735), "piano": (616, 162, 26), "kitchen": (330, 232, -150),
          "upstairs": (527, G + 108, 18)}
MARKS = {"mom": (400, 330), "bigsis": (490, 285), "lilsis": (325, 305),
         "atdoor": (712, 88), "atstairs": (158, 606), "atpiano": (548, 150), "atpiano2": (602, 150), "atcloset": (172, 372),
         "atbooks": (190, 92), "atkitchen": (334, 90), "atframe": (446, 90), "attable": (508, 512), "atarmchair": (336, 606),
         "landing1": (158, 606), "landing2": (205, 535), "landing3": (322, 565)}
WALK = [(130, 80), (130, 600), (190, 628), (345, 618), (440, 572), (480, 518), (690, 500), (726, 440), (726, 80)]

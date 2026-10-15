"""The house, measured: a plan of each of its three floors in centimetres, put together from the five rooms' models
(home_*_model.py), for the map of the house (map_home.py). MAP-15H.

THE FRAME. The house is measured in the living room's own frame: X across, left to right along its back wall; Z out
from that wall toward the room's front. The landing is the gallery across that back wall upstairs, so it shares the
frame (home_landing_model.py says so). Every other room is its own model moved into this frame, never turned and never
mirrored, so that each one is drawn exactly as its model has it (and as its picture shows it), only somewhere in the
house: Little Sister's room is her model moved by LS = (dX, dZ), Dad's study his model moved by ST. The attic is drawn
as a plan of its own, in the Retreat's own frame.

HOW THE ROOMS FIT. The five models were each made for one picture, and they do not all fit at once: Little Sister's room
is 720 wide with its door at its front right corner, and the study is 700 wide with its door in a short partition at its
front left, while the landing has the three doors upstairs 210 apart along one wall (the Son's, Little Sister's, the
study's). Nothing is shrunk or turned to make them fit. Instead:
  - the Son's room (no model: nobody goes in tonight) lies right behind his door, as deep as SON_D;
  - Little Sister's door off the landing opens into a short passage beside his room, at whose end her own door stands
    open into her room, which lies behind his (her model's door lines up with the landing's door exactly);
  - the study's door off the landing opens into the little lobby the study's model leaves at its front left corner
    (its door stands in the partition there, as in its picture), so the study lies to the right, over the front porch;
  - the space between Little Sister's room and the study is a bathroom and a cupboard.
Downstairs, under the same outline: the kitchen behind the living room's back wall (its open doorway is in the
picture), a pantry, a back hall, Mom and Dad's room with its closet, a bathroom; and the covered porch under the study,
onto which the front door opens (the only way out of the house). The attic is the Retreat, over the landing.

Everything is in centimetres; map_home.py turns it into the picture. Rooms are interiors (the walls are what lies
between them); each list below says what it is."""

import home_bigsis_room_model as BS
import home_landing_model as LD
import home_lilsis_room_model as LS_M
import home_living_room_model as LR
import home_study_model as ST_M

SON_D = 270                                  # the Son's room's depth (cm): the passage to Little Sister's room is as long
WALL_IN, WALL_OUT = 12.0, 24.0               # wall thicknesses: between rooms, and outside
LS = (-214.0, -(694.0 + SON_D))              # Little Sister's model -> the house: her door (X 614..702) over the landing's (400..485)
ST = (607.0, -760.0)                         # the study's model -> the house: its lobby (X 0..88) behind the landing's door (610..695)


def ls(X, Z):
    return X + LS[0], Z + LS[1]


def st(X, Z):
    return X + ST[0], Z + ST[1]


def rect(x0, x1, z0, z1):
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


# ================================================================ the ground floor
G_ROOMS = {                                  # interiors: (X0, X1, Z0, Z1); the living room is its model's ROOM
    "living": (0.0, 780.0, 0.0, 1150.0),
    "kitchen": (120.0, 595.0, -400.0, -12.0),
    "pantry": (-214.0, 108.0, -400.0, -12.0),
    "hall": (-214.0, 595.0, -532.0, -412.0),
    "parents": (-214.0, 288.0, -994.0, -544.0),
    "bath": (300.0, 595.0, -760.0, -544.0),
    "closet": (300.0, 595.0, -994.0, -772.0),
}
# openings in the walls: (X0, X1, Z0, Z1) of the wall cut away; kind "door" (a leaf and its swing are drawn), "doorway"
# (open), "window"; and for a door, its hinge (X, Z), the end of its open leaf (X, Z), and which way it swings
G_OPEN = [
    ("kitchen-door", "doorway", (268.0, 400.0, -12.0, 0.0)),                     # the open doorway in the picture
    ("front-door", "door", (664.0, 760.0, -24.0, 0.0)),                          # the front door (the living room's drawing)
    ("pantry-door", "door", (108.0, 120.0, -330.0, -250.0)),
    ("hall-door", "door", (450.0, 532.0, -412.0, -400.0)),
    ("parents-door", "door", (100.0, 184.0, -544.0, -532.0)),
    ("bath-door", "door", (400.0, 474.0, -544.0, -532.0)),
    ("closet-door", "door", (288.0, 300.0, -950.0, -880.0)),
    ("stair-window", "window", (-24.0, 0.0, 240.0, 400.0)),                      # the tall window over the stairs
    ("kitchen-window", "window", (595.0, 619.0, -300.0, -170.0)),
    ("pantry-window", "window", (-238.0, -214.0, -300.0, -210.0)),
    ("parents-window-1", "window", (-238.0, -214.0, -880.0, -720.0)),
    ("parents-window-2", "window", (-60.0, 90.0, -1018.0, -994.0)),
    ("bath-window", "window", (595.0, 619.0, -700.0, -630.0)),
]
# door leaves on the back (the rooms that are not places): (hinge, open end) — the swing is drawn from the open end back
# to where the door shuts
G_LEAVES = [
    ("pantry-door", (114.0, -250.0), (40.0, -250.0), (114.0, -330.0)),          # hinge, open end, shut end
    ("hall-door", (532.0, -406.0), (532.0, -488.0), (450.0, -406.0)),
    ("parents-door", (184.0, -538.0), (184.0, -622.0), (100.0, -538.0)),
    ("bath-door", (474.0, -538.0), (474.0, -612.0), (400.0, -538.0)),
    ("closet-door", (294.0, -880.0), (364.0, -880.0), (294.0, -950.0)),
]
# the stairs: up the left wall from the front (Z 575) to the landing (Z 175), 16 steps (the living room's model)
STAIRS = dict(X=(0.0, 108.0), z_foot=575.0, z_top=175.0, steps=16)
# the covered porch under the study, outside the front door: its posts (the study above it is drawn dashed)
PORCH = (619.0, 1307.0, -760.0, -24.0)
PORCH_POSTS = [(1300.0, -753.0), (1300.0, -30.0), (960.0, -753.0)]


# ================================================================ upstairs
U_ROOMS = {
    "landing": (0.0, 780.0, 0.0, 175.0),      # the gallery, with the head of the stairs at its left end (X 0..108)
    "son": (-214.0, 388.0, -SON_D, -12.0),
    "passage": (400.0, 488.0, -SON_D, -12.0),
    "bath": (500.0, 595.0, -SON_D, -12.0),
    "cupboard": (518.0, 595.0, -994.0, -SON_D - 12.0),
    "lilsis": (ls(0, 0)[0], ls(720, 0)[0], ls(0, 0)[1], ls(0, 694)[1]),
    "lobby": (607.0, 695.0, -170.0, -12.0),
    "study": (607.0, 1307.0, -760.0, -24.0),  # less the lobby and its two walls (see U_STUDY)
}
# the study's floor: its model's room less the lobby in its front left corner (the partition at X 88..100, from Z 590)
U_STUDY = [st(0, 0), st(700, 0), st(700, 736), (707.0, -24.0), (707.0, -182.0), st(0, 578)]
U_OPEN = [
    ("son-door", "door", (190.0, 275.0, -12.0, 0.0)),
    ("lilsis-door", "door", (400.0, 485.0, -12.0, 0.0)),
    ("study-door", "door", (610.0, 695.0, -12.0, 0.0)),
    ("lilsis-inner", "doorway", (400.0, 488.0, -SON_D - 12.0, -SON_D)),           # her own door: its leaf is her room's drawing
    ("study-inner", "doorway", (695.0, 707.0, st(0, 640)[1], st(0, 725)[1])),     # the study's own door, in the partition
    ("bath-door", "door", (488.0, 500.0, -200.0, -130.0)),
    ("cupboard-door", "door", (525.0, 580.0, -SON_D - 12.0, -SON_D)),
    ("son-window", "window", (-238.0, -214.0, -240.0, -80.0)),
    ("lilsis-window", "window", (ls(300, 0)[0], ls(420, 0)[0], ls(0, 0)[1] - 24.0, ls(0, 0)[1])),   # her window (her model)
    ("study-window", "window", (st(296, 0)[0], st(404, 0)[0], -784.0, -760.0)),                    # his window (his model)
    ("bath-window", "window", (595.0, 607.0, -230.0, -150.0)),
]
U_LEAVES = [
    ("son-door", (275.0, -6.0), (275.0, -88.0), (190.0, -6.0)),                   # into his room; shut all act
    ("lilsis-door", (485.0, -6.0), (481.0, -91.0), (400.0, -6.0)),                # into the passage, back against its wall
    ("study-door", (610.0, -6.0), (614.0, -91.0), (695.0, -6.0)),                 # into the lobby, back against its wall
    ("bath-door", (494.0, -130.0), (560.0, -130.0), (494.0, -200.0)),
    ("cupboard-door", (580.0, -306.0), (580.0, -360.0), (525.0, -306.0)),
]
HATCH = (514.0, 590.0, 44.0, 122.0)          # the attic hatch in the landing's ceiling (the landing's model)


# ================================================================ the attic: the Retreat, in its own frame
A_FRONT = 600.0                              # the near wall (out of its picture: past the hatch and the tea cushion)
A_ROOM = (0.0, float(BS.W), 0.0, A_FRONT)
A_OPEN = [
    ("round-window", "window", (-24.0, 0.0, BS.ROUND_WINDOW[0] - 50.0, BS.ROUND_WINDOW[0] + 50.0)),
]
A_HATCH = BS.HATCH                           # (X0, X1, Z0, Z1): the opening in the floor, the top of the ladder


def floors():
    """{floor: (rooms {name: polygon}, openings, leaves)} in the house's (or the attic's) centimetres."""
    g = {k: rect(*v) for k, v in G_ROOMS.items()}
    u = {k: rect(*v) for k, v in U_ROOMS.items()}
    u["study"] = U_STUDY
    a = {"retreat": rect(*A_ROOM)}
    return {"ground": (g, G_OPEN, G_LEAVES), "upstairs": (u, U_OPEN, U_LEAVES), "attic": (a, A_OPEN, [])}


def bounds(floor):
    rooms = floors()[floor][0]
    xs = [p[0] for poly in rooms.values() for p in poly]
    zs = [p[1] for poly in rooms.values() for p in poly]
    return min(xs), max(xs), min(zs), max(zs)


# ================================================================ the places' things, from the models (cm, house frame)
def living_things():
    """The living room as its model has it (LR.BOXES etc.): (kind, data) for map_home_things.py to draw."""
    B = {b[0]: b[1:] for b in LR.BOXES}
    out = []
    for k in ("books", "piano", "stool", "rug", "table", "basket", "phone-table", "plant", "lamp"):
        X0, X1, Y0, Y1, Z0, Z1 = B[k]
        out.append((k, (X0, X1, Z0, Z1)))
    X0, X1, _, _, Z0, Z1 = B["armchair"]
    out.append(("armchair", ((X0 + X1) / 2, (Z0 + Z1) / 2, 25.0)))              # its middle, and how far it is turned
    for k in ("chair-head", "chair-left-far", "chair-left-near", "chair-right-far", "chair-right-near"):
        X0, X1, _, _, Z0, Z1 = B[k]
        out.append(("chair", (X0, X1, Z0, Z1, k)))
    out.append(("closet", (LR.FLATS[[f[0] for f in LR.FLATS].index("closet")][2:4])))   # its door's Z0, Z1 on X = 108
    out.append(("front-door", (664.0, 760.0)))
    return out


def lilsis_things():
    M = LS_M
    out = [("flock", M.FLOCK), ("fort", M.FORT), ("bed", M.BED), ("pillow", M.PILLOW), ("lamptable", M.LAMPTABLE),
           ("teatable", M.TEATABLE), ("eggrug", M.EGGRUG), ("coop", M.COOP), ("nest", M.NEST), ("toybox", M.TOYBOX),
           ("crate", M.CRATE), ("door", (M.DOOR_X, M.DOOR_Z))]
    return out


def study_things():
    M = ST_M
    return [("desk", M.DESK), ("computer", M.PC_CASE), ("monitor", M.MONITOR), ("chair", M.CHAIR), ("cabinet", M.CABINET),
            ("machine", M.MACHINE), ("shelves", M.SHELVES), ("vault", M.VAULT), ("globe", M.GLOBE), ("rug", M.RUG),
            ("heap", M.HEAP), ("pile", M.PILE), ("door", (M.PARTITION, M.DOORWAY, M.LEAF))]


def landing_things():
    B = {b[0]: b[1:] for b in LD.BOXES}
    return [("halltable", B["halltable"]), ("lamp", B["lamp"]), ("hamper", B["hamper"]), ("bag", B["bag"]),
            ("quilt", B["quilt"]), ("ladder", B["ladder"]), ("posts", [B[k] for k in ("post1", "post2", "post3", "post4")])]


def retreat_things():
    M = BS
    return [("bookcase", M.BOOKCASE), ("timeline", M.TIMELINE), ("soundtable", M.SOUNDTABLE), ("machine", M.MACHINE),
            ("fountain", M.FOUNTAIN), ("desk", M.DESK), ("stool", M.STOOL), ("bed", M.BED), ("canopy", M.CANOPY),
            ("rug", M.RUG), ("mat", M.MAT), ("stump", M.STUMP), ("stump2", M.STUMP2), ("palm", M.PALM),
            ("pampas", M.PAMPAS), ("plantstand", M.PLANTSTAND), ("basket", M.BASKET), ("slippers", M.SLIPPERS),
            ("footlamps", M.FOOTLAMPS), ("floorcandle", M.FLOORCANDLE), ("sign", M.SIGN), ("tea", M.TEA),
            ("pouf", M.POUF), ("skylights", M.SKYLIGHTS), ("ridge", M.RIDGE_Z), ("hatch", M.HATCH)]


if __name__ == "__main__":
    for f in ("ground", "upstairs", "attic"):
        print(f, bounds(f))
    print("lilsis door ->", ls(614, 694), ls(702, 694), " study lobby ->", st(0, 590), st(88, 760), " study door ->", st(100, 640), st(100, 725))

"""The Inari puppet theatre in the grounds of Naniwa Shrine, Osaka, about 22 April 1830 (scene `edo-theatre`): the
measurements, in centimetres (room.py: X across, left to right; Y up; Z out from the house's far wall toward us).
PAINT-21D (round twenty-one).

What is checked (S/work-21-factsB/facts-21b.md item 3): Osaka's puppet theatre stood in 1830 in the grounds of Naniwa
Shrine at Bakuro-machi, "the Inari theatre"; three operators to a puppet since 1734; nobody says "Bunraku" (1872). What an
1830 theatre's inside looked like is NOT in the sources: this hall is the game's own, in the spirit of the art (a hut
theatre in a shrine's grounds, its floor of one level, lit by day through high windows and by a few lamps), and the notes
say so.

THE PLACE. One hall under a plank roof on rafters. At the far end from us, the house: the audience on straw mats in rows,
facing the stage, high lattice windows in its far and right walls. Across the hall, the stage: a floor of polished
boards, with the RAIL along its front (a low partition of black lacquer: the operators stand behind it and the puppets
walk on its top), a low painted set (a village gate at stage left, near the rail; a house front at stage right, raked
toward the wing and the house so that both see its face: its door is at the puppets' height, on the rail's line). At stage
right, out into the house, the chanter's DAIS (a low platform, a lectern with the book, two cushions). Stage left is
the WING: backstage, where we stand. Its far wall is the building's outer wall left of the house (the BACK DOOR in it
opens on the alley), and on it hang the troupe's things: two black robes and hoods on a peg, a shelf of heads, the
puppets on their rail. A black masking curtain hangs at the stage's left end. The stage is open behind to the wing and
the backstage room (the audience sees only dark there).

HOW IT IS SEEN. One camera (VIEW), standing in the backstage room upstage of the stage's left end, turned to the right,
looking diagonally across the stage toward the house. Everything is one floor level (Y = 0): the house, the stage and
the wing (a hut theatre; the game's invention). The rail hides the audience below the shoulders; their heads show over
it, rising row behind row. Everything is as PAINTED: edo_theatre.py reads these numbers, and so does the layout."""

import math

ID = "edo-theatre"
VIEW = dict(horizon=190, full=560, cam=(-330.0, 1700.0), yaw=25.0, focal=600.0)

# ---- the hall
HOUSE = (-100.0, 820.0, 0.0, 770.0)          # the audience's floor: X0, X1, Z0, Z1 (mats from Z 50 to 740)
MATS = (-80.0, 800.0, 50.0, 745.0)
ROOF = 600.0                                  # the rafters' undersides over the house and the stage
ROOF_BACK = 520.0                             # backstage: a lower ceiling of boards on joists
HALL_X1 = 820.0                               # the right wall (the house and the stage)
WING = (-820.0, 0.0, 770.0, 1180.0)           # the wing: X0, X1, Z0, Z1 (its far wall is Z = 770)
BACKSTAGE = (-820.0, 820.0, 1180.0, 1900.0)   # behind the stage
WALL_WING_X = (-820.0, -100.0)                # the wing's far wall (the building's outer wall): X0, X1 at Z = 770
HOUSE_LEFT_X = -100.0                         # the house's left wall (Z 0..770)

# ---- the stage
STAGE = (0.0, 570.0, 782.0, 1180.0)           # X0, X1, Z0, Z1: the polished boards
RAIL = (0.0, 570.0, 770.0, 782.0, 86.0)       # the rail: X0, X1, Z0, Z1, its height (its top: a cap of 4 cm)
CURTAIN = (-24.0, 770.0, 905.0, 18.0)         # the masking curtain: X, Z0, Z1, its foot's height above the floor
GATE = dict(x=(26.0, 128.0), z=902.0, post=10.0, h=200.0, beam=(176.0, 188.0), roof=(188.0, 216.0), over=14.0)   # puppet-sized
HOUSEFRONT = dict(p0=(540.0, 1140.0), p1=(566.0, 884.0), h=214.0, door=(0.30, 0.58), door_y=(86.0, 182.0),
                  window=(0.68, 0.90), window_y=(106.0, 160.0), eave=(182.0, 214.0))
DAIS = (588.0, 800.0, 520.0, 860.0, 45.0)     # X0, X1, Z0, Z1, top: the chanter's dais, out into the house at stage right
LECTERN = (628.0, 676.0, 676.0, 706.0, 45.0, 98.0)  # X0, X1, Z0, Z1, Y0, Y1: the chanter's lectern, with the book on it
CUSHIONS = [(700.0, 690.0), (700.0, 790.0)]   # the chanter's and the shamisen's (X, Z of each cushion's middle)

# ---- the wing's things (on its far wall, Z = 770, unless said)
BACKDOOR = (-450.0, -368.0, 0.0, 180.0)       # X0, X1, Y0, Y1: a sliding plank door, open a hand's breadth (daylight)
DOOR_OPEN = 14.0                              # how far it stands open (cm), at its right edge
PEG = (-318.0, 172.0)                         # X, Y of the peg: two black robes and two hoods hang from it
ROBES = (-350.0, -284.0, 60.0, 172.0)         # X0, X1, Y0, Y1 of the robes as they hang (on the wall, 6 cm out)
SHELF = (-252.0, -150.0, 140.0)               # X0, X1, Y of the shelf of heads (24 cm deep)
BOXES = [(-262.0, -140.0, 0.0, 44.0, 780.0, 848.0), (-252.0, -156.0, 44.0, 78.0, 784.0, 840.0)]   # wicker boxes under the shelf
PUPPET_RAIL = (-440.0, -112.0, 300.0)         # X0, X1, Y: the rail high on the wall the puppets hang from, over the door and the peg
PUPPETS = [(-420.0, "ochre"), (-370.0, "indigo"), (-318.0, "vermilion"), (-262.0, "green"), (-206.0, "indigo2"), (-152.0, "lake")]   # X of each, its kimono
LAMP = (-118.0, 880.0, 112.0)                 # X, Z of a lamp stand (a dish of oil on a post), its height
STAND = (-110.0, 975.0)                       # X, Z of the boy puppet's stand (a post on a cross foot, a bar at 112)
STAND_H = 116.0
PUPPET_H = 90.0                               # the boy puppet: 0.9 m (ROUND-21), hung from the stand's bar by the shoulders

# ---- where the high windows are (the daylight): the house's far wall and its right wall; a hatch in the roof
WINDOWS_FAR = [(20.0, 190.0), (330.0, 500.0), (620.0, 790.0)]     # X ranges on Z = 0, Y 380..470
WINDOWS_RIGHT = [(120.0, 300.0), (420.0, 600.0)]                    # Z ranges on X = 820, Y 380..470
SKYLIGHT = (-150.0, 400.0, 570.0, 800.0)     # X0, X1, Z0, Z1 of the roof hatch over the house's front, shut before the show,
                                              # propped open for it: its day falls steeply onto the stage and the set (the
                                              # hatch itself is out of the picture, over the backstage ceiling's edge)
SUN_SKY = (0.25, -0.88, 0.40)                 # the hatch's daylight: down, toward stage right and toward us (it lights faces turned to the house)
SUN_WIN = (-0.78, -0.62, 0.06)                # the right wall's windows' daylight: toward -X, down
WIN_Y = (380.0, 470.0)

# ---- the people's places (X, Z), and which way they face (the compass of the stage: N is away from us)
MARKS = {
    "back": ((-395.0, 862.0), "S"),          # inside the back door: arriving
    "jubei": ((-40.0, 1010.0), "W"),         # Jubei, by the boy puppet on its stand
    "stand": ((-150.0, 1065.0), "N"),        # before the boy puppet on its stand (where the girls rehearse)
    "peg": ((-305.0, 905.0), "N"),           # before the peg with the black robes
    "rail": ((352.0, 868.0), "N"),           # behind the stage rail: where the operators stand in the show (Jubei's feet)
    "wing": ((-60.0, 935.0), "E"),           # in the wing, by the curtain: looking onto the stage
    "momseat": ((150.0, 705.0), "S"),        # the front of the audience's mats: Mom
    "tatsuseat": ((204.0, 707.0), "S"),      # and next to her, Tatsu
    "chanter": ((700.0, 690.0), "N"),        # on the dais (raised 45 cm): the chanter, at his lectern
    "shamisen": ((700.0, 790.0), "N"),       # on the dais: the shamisen player
    # more places: for the three as they come in, and for the scene's scripts
    "back_mom": ((-392.0, 874.0), "S"), "back_bigsis": ((-326.0, 912.0), "S"), "back_lilsis": ((-388.0, 950.0), "S"),
    "railLeft": ((228.0, 808.0), "N"),       # Big Sister at the puppet's left hand (the left-hand operator), beside it
    "railFeet": ((292.0, 846.0), "N"),       # Little Sister at its feet, crouched low behind them
    "aisle": ((-60.0, 735.0), "S"),          # the house's front aisle, beyond the gap at the wing wall's end
    "gap": ((-62.0, 790.0), "S"),            # the gap between the wing wall's end and the curtain (the way round the front)
    "lamp": ((-118.0, 940.0), "N"),
    "boxes": ((-200.0, 900.0), "N"),
    "behind": ((150.0, 1200.0), "N"),        # backstage, behind the stage
}
# the puppet, at the rail: the point under it (on the floor, in front of Jubei toward the rail) and its feet's height
PUPPET_AT = (270.0, 818.0)
PUPPET_FEET_Y = RAIL[4] + 2.0                  # it walks on the rail's top

# the floor people may stand on (one floor: the wing, the stage, the backstage room), clear of the walls, the rail, the
# set, the curtain, the boxes and the lamp; and the house's front aisle (its own floor: reached by the scene's script)
WALK = [(-450.0, 800.0), (-395.0, 800.0), (-330.0, 820.0), (-160.0, 820.0), (-160.0, 860.0), (-80.0, 840.0), (-60.0, 800.0),
        (-40.0, 920.0), (20.0, 930.0), (40.0, 830.0), (180.0, 830.0), (200.0, 800.0), (620.0, 800.0), (620.0, 900.0),
        (520.0, 960.0), (420.0, 1140.0), (440.0, 1240.0), (300.0, 1330.0), (-560.0, 1330.0), (-560.0, 860.0)]
AISLE = [(-90.0, 690.0), (330.0, 690.0), (330.0, 742.0), (-30.0, 742.0), (-30.0, 790.0), (-90.0, 790.0)]

"""The air ducts over the Office's ground floor (office-ducts): the measurements, in centimetres (OFFICE-17B, OFFICE-17B2).

A CUT-AWAY, LIKE AN ARCHITECT'S SECTION. We look along the building's ceiling space from its cut face: everything in
front of the section plane (Z = CUT) is taken away, the near side of the long sheet-metal duct with it, so that we see
into the duct and Ranger walks left and right along its floor. X runs left to right along the duct; Y is up from the
duct's floor (the floor Ranger walks on is Y = 0, the scene's ground); Z runs from the far wall of the ceiling space
toward us, and the duct's inside is Z = 200 (its back wall) to Z = CUT (the cut).

OFFICE-17B2 (the second pass: the picture did not read as a duct). The duct is the same tube where it was (the same
camera, floor, inside height, grilles, marks and walk), drawn now as a section is drawn: its walls are a double skin of
galvanized sheet with a core between them (SHELL thick), so that where the plane cuts them there is a band to see, top
and bottom, the cut sheet bright on both sides of a thin hatched core. The intake run at the left and the B-7 shaft at
the right are cut the same way, so the cut is one outline: down the run's wall, along the duct's top, up and down the
shaft's wall, along the duct's floor. Round it the ceiling space is lit dimly but readably: the insulation lies on the
duct's top and on the tiles (none hangs), the pipe and the wires run over the duct, the joists are cut at the top of the
picture, and under the tiles' cut line the rooms' light falls (the rooms are seen only through the grilles).

ONE CAMERA (room.View: horizon 333, full 470, focal 600, square to the cut, its lens at 150 cm over the duct's floor:
just above the duct's top, so that the duct's floor shows as a band 21 px deep with the grilles in it, and its top is
seen edge on). The camera's numbers are the scene's own: change any of them and the scene file must be measured again.
Ranger walks the middle of the duct's floor (Z = 250), where the row is 470 = `full`: he is drawn there at exactly his
painted size (scale 1.0, his frames pixel for pixel), a third larger than outdoors at the Last Stop (about 0.74). The
duct is drawn to fit him: its inside is 130 cm high, 3.5 times his height on all fours (34 px there, 37 cm), and 100
cm deep.

The ceiling space is a cartoon's: the picture is five metres high at the duct's depth, so the space over the duct runs
up three metres to the joists (cut at the top of the picture, the roof deck over them), with the cinder-block far wall
behind and the services along it (the water pipe, a jacketed hot-water line, the bundled wires, a conduit, the
sprinkler main), pink insulation lying along the duct's top; the ceiling's tiles lie a third of a metre under the duct,
their backs seen through the gap: the coffee cup, the pencil, the wrapper, more pink insulation, the light fittings
(the two the plane cuts show their tubes alight), and under each grille its boot down to the room.

At the LEFT END the duct turns up into a vertical run (the intake) through the roof: daylight at its top, from the
rooftop unit's open grille, and under that the intake fan's back, still. At the RIGHT END the duct opens into the B-7
shaft, a big clean vertical tube that rises to the roof and drops out of the bottom of the picture, rungs down its back
wall; across it, below the duct's floor, the big fan in its ring plate on struts (a cut-out of its own: four frames
turning, one stopped), the shaft open round it, going on down."""

ID = "office-ducts"

# ---- the camera (the scene's own: horizon 333, full 470)
VIEW = dict(horizon=333, full=470, cam=(400.0, 906.25), yaw=0.0, focal=600.0, centre_x=400.0)

CUT = 300.0                                              # the section plane: everything nearer us is taken away
FAR = 118.0                                              # the far wall of the ceiling space (cinder block)  (OFFICE-17B2: nearer)

# ---- the duct (inside measurements; its walls are SHELL thick, outside them)  (OFFICE-17B2: a double skin, to be seen cut)
SKIN = 1.6                                               # each galvanized sheet of the double wall
SHELL = 12.0                                             # sheet, core, sheet: the band the cut shows
SHEET = SHELL                                            # (the old name: how far the outside is from the inside)
DUCT_Z = (200.0, CUT)                                    # back wall .. the cut
DUCT_H = 130.0                                           # inside height: 3.5 x Ranger on all fours
FLOOR_Y = 0.0
RUN_X = (-24.0, 112.0)                                   # the intake run, inside (it rises from the duct's floor at its left end)
RUN_TOP = 760.0                                          # (it goes on up out of the picture)
CHEEK = 22.0                                             # the elbow's corner: a 45-degree plate in the floor's far left corner
SHAFT_X = (658.6, 830.0)                                 # the B-7 shaft, inside (its right wall out of the picture)
SHAFT_Z = (160.0, CUT)
SHAFT_Y = (-700.0, 760.0)
DUCT_X = (RUN_X[0], SHAFT_X[0])                          # the duct's floor, from the run's far wall to the shaft (its mouth)
JOINTS = [140.0, 274.0, 405.0, 537.0]                    # the duct's transverse joints (flanged, riveted), X

# ---- the four grilles in the duct's floor, X centre; each GRILLE_L long (X) and over most of the floor's depth (Z)
GRILLE_L = 40.0
GRILLE_Z = (214.0, 286.0)
GRILLES = [
    ("room", "ROOM C", 208.5),                           # over Interview Room C (the Comfortable Room)
    ("property", "PROP & EFF", 339.8),                   # over Property & Effects
    ("break", "BREAK", 471.1),                           # over the break room
    ("hall", "HALL", 602.4),                             # over the hall
]
STENCIL_Y = (57.0, 69.0)                                 # the room's name stencilled on the back wall over its grille (12 cm letters)

# ---- under the duct: the gap down to the ceiling's tiles, and the tiles
TILE_Y = -45.0                                           # the tiles' backs (their top face)
TILE_T = 1.8                                             # a tile's thickness
TBAR = 2.4                                               # the grid's tees hang this far below the tiles' backs
TILE = 61.0                                              # the grid's pitch (two feet)
TILE_X0, TILE_Z0 = -18.0, 4.0                            # where the grid's lines fall
BOOT_Z = (GRILLE_Z[0] - 4.0, CUT)                        # each grille's boot, down to its diffuser in the tiles (cut at the front)

# the light fittings: troffers set in the tile grid, their housings in the gap, X0 X1 Z0 Z1 (one two-by-four each). Both
# run out to the cut and are cut with everything else (their tubes alight in section).
FITTINGS = [
    (93.0, 154.0, 186.0, 308.0),                         # in the gap under the duct, between the intake and ROOM C (the one to click)
    (380.0, 441.0, 186.0, 308.0),                        # under the duct between PROP & EFF and BREAK
]
# the fittings behind the duct (out of sight under it): their light comes up between the tiles and fans up the far wall,
# X and Z of each (OFFICE-17B2)
GLOWS = [(212.0, 182.0), (590.0, 182.0)]
FITTING_H = 11.0
CUT_FITTINGS = [f for f in FITTINGS if f[3] >= CUT]

# ---- the forgotten things on the tiles (in the gap, near the cut so that they are as large as they can be)
CUP = dict(at=(286.0, 268.0), r=5.0, h=10.0)             # X, Z of a mug's foot on a tile; its radius and height
PENCIL = dict(a=(500.0, 281.0), b=(518.0, 270.0), r=0.45)       # its two ends, lying on a tile
WRAPPER = dict(at=(540.0, 272.0), w=19.0, d=14.0)        # a crumpled sandwich wrapper (about 1983)
LIFTED = dict(X=(496.0, 557.0), Z=(193.0, 250.0), lift=2.4)   # a tile behind them lifted at its front edge: room light in the crack
BATTS = [                                                # pink insulation lying on the tiles: X0 X1 Z0 Z1 thickness
    (-160.0, 84.0, 150.0, CUT, 10.0),                    # (these two run out to the cut, clear of the boots and the fittings: their
    (236.0, 276.0, 222.0, CUT, 9.0),                     #  cut faces lie on the tiles' line)
    (60.0, 300.0, 140.0, 184.0, 8.0),                    # (and these lie further back, behind the boots and the fittings)
    (330.0, 372.0, 150.0, 205.0, 8.5),
    (452.0, 494.0, 160.0, 203.0, 7.5),
]
# pink insulation lying along the duct's top (OFFICE-17B2: it lies, it does not hang): X0 X1 thickness, a lumpy top
BLANKET = [(124.0, 318.0, 22.0), (322.0, 476.0, 24.0), (481.0, 648.0, 21.0)]

# ---- the ceiling space over the duct
JOIST_Y = (438.0, 468.0)                                 # the joists (running front to back, cut at the top of the picture)
JOIST_W = 9.0
JOIST_X = [-182.0 + 61.0 * i for i in range(20)]         # their middles, two feet apart
DECK_Y = (468.0, 500.0)                                  # the deck (planks), the roofing over it (its cut along the picture's top)
# the services run along the far wall on brackets, behind the run and the shaft (they pass behind both)
PIPE = dict(Y=198.0, Z=134.0, r=5.4, X=(-260.0, 1100.0))         # the water pipe (copper), on clamps off the wall
VALVE_X = 445.0                                          # a gate valve on it, its red handwheel toward us
BRACKETS = [175.0, 300.0, 425.0, 560.0]                  # the pipe's clamps and the wires' J-hooks, screwed to the wall
WIRES = dict(Y=278.0, Z=130.0, sag=4.0, r=2.6)           # the bundled wires, sagging a little between their J-hooks
CONDUIT = dict(Y=330.0, Z=122.0, r=1.8, X=(-260.0, 1100.0), box=470.0)                # a conduit strapped to the wall, a junction box
HANGERS = [274.0, 537.0]                                 # the duct's trapeze hangers (rods behind it up to the joists, a strut under it)
HOTLINE = dict(Y=226.0, Z=133.0, r=6.5)                  # a hot-water line in its white jacket, on the same brackets, higher up
SPRINKLER = dict(Y=418.0, Z=140.0, r=2.4, heads=[205.0, 395.0, 585.0])     # the sprinkler main under the joists, red, its heads
WALL_COURSE, WALL_BLOCK = 20.3, 40.6                     # the far wall's cinder blocks (with their joints)

# ---- the intake: the run's mouth at the top and the fan in it
INTAKE_OPEN = dict(X=(-14.0, 100.0), Y=(470.0, 680.0))  # the opening in the run's back wall at the rooftop unit (daylight)
INTAKE_FAN = dict(at=(44.0, 400.0, 250.0), r=46.0, hub=9.0)       # X, Y, Z of its middle; still (Ranger switched it off)

# ---- the B-7 shaft's fan, across the shaft in its ring plate, under the duct's floor (its frames' size and place are the scene's)
FAN = dict(at=(730.0, -95.0, 230.0), r=63.0, hub=12.0, plate=2.0, blades=4, rest=11.0)    # rest: the stopped angle (degrees)
SHROUD = dict(r=66.0, h=(-105.0, -95.2))               # the fan's ring (OFFICE-17B2: on struts; the shaft is open round it, going on down)
FAN_TURN = [0.0, 22.5, 45.0, 67.5]                       # the turning frames (four broad blades: a quarter turn repeats)
RUNG_X = (772.0, 812.0)                                  # the rungs down the shaft's back wall, beside the fan
BULB = dict(at=(770.0, 168.0, 162.0), r=4.2)             # a caged bulb on the shaft's back wall, over the duct's mouth
RUNG_STEP = 30.0
B7_STENCIL = dict(X=680.0, Y=118.0)                      # the shaft's stencil: its top left, on the back wall beside the mouth

# ---- marks: where Ranger is put (X, Z on the duct's floor) and which way he faces
WALK_Z = 250.0                                           # the middle of the floor: the row `full`
MARKS = {
    "intake": ((40.0, WALK_Z), "E"),                     # just in from the roof, at the foot of the run
    "over-room": ((None, WALK_Z), "E"),                  # (at each grille: filled in below)
    "over-property": ((None, WALK_Z), "E"),
    "over-break": ((None, WALK_Z), "E"),
    "over-hall": ((None, WALK_Z), "E"),
    "shaft": ((638.0, WALK_Z), "E"),                     # at the end of the floor, the fan below him
}
PEEK_HEAD = 50.0 * 175.0 / 160.0                         # a mark at a grille is the foot point of Ranger lying there with his
                                                         # head over the grille: his foot point 50 px (at full size) behind the
                                                         # grille's middle (his nose about 42 px ahead of his foot point)
for _id, _label, _x in GRILLES:
    MARKS["over-" + _id] = ((_x - PEEK_HEAD, WALK_Z), "E")

# the walk: the floor's middle half, from the foot of the run to the end of the floor over the shaft
WALK_X = (18.0, 652.0)                                   # (past the foot of the elbow's corner, to the floor's end)
WALK_ZS = (229.0, 271.0)

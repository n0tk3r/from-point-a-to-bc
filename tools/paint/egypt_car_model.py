"""Inside the wagon (egypt-car): the measurements, in centimetres.

Dad sits in the driver's seat of the family wagon, nose-down in the sand by the Nile, and the picture is what his own eyes
see: the dashboard from the wheel to the glovebox, the windshield over it, the headliner and the visors above, his door
at the left and the Son's half of the bench at the bottom right. Dad himself is not drawn.

X runs across the car from the driver's door (0, the inside of its panel at the belt line) to the passenger's (W); Y is up
from the floor pan; Z runs from the foot of the windshield (0, where the glass meets the dash) back toward Dad. The camera
is room.View's, square to the car (yaw 0, so the dashboard runs level across the picture), its vanishing point shifted
toward the wheel (centre_x 236) so that the whole dash is in the picture.

THE CAMERA. The lens (focal 500) is the brief's, from the wheel (39 cm across, 50 cm from his eyes, about 380 pixels).
The eye's row (horizon 181) is lower than the brief's starting 130 because the car is nose-down: the river picture draws
the wagon tilted 7 degrees (wagon.py), so the world outside the glass is tilted up by 7 degrees from the car's own level,
and with the eye's row at 181 the world's horizon falls at row 120, where the design has the far bank of the Nile (its
rows 108 to 132), with the sky above it and the river below, and the mound of sand piled on the hood filling the glass.
His eye is 110.5 cm above the floor (`full` 282). Nobody is drawn here, so `horizon` and `full` size nothing anyone sees.

THE CARTOON'S CHEATS (as the limousine has its own). The design's picture is a painter's: a pinhole camera that shows the
wheel 380 pixels across sees only about 40 degrees below Dad's eye level, so it can show neither the bench under him nor
the Son's half of it, which a real driver sees only by turning his head. Two things are moved into the camera's view,
and nothing else: (1) the Son's half of the bench (a split bench) stands forward of Dad's and higher, its front edge
72 cm ahead of his eye, so that its cushion shows at the bottom right below the glovebox, clear of the glovebox's door
when it drops; its back is beside Dad's shoulder, out of any forward view, and is not in the picture (the passenger's
door is at the right edge); (2) the windshield stands nearly upright, 100 to 115 cm ahead (the old wagon's tall glass),
so that the headliner, both visors and the rearview mirror are in the picture above it, as the design has them, and its
pillars lean in toward the roof. The door's fittings (the crank, the lock knob, the armrest's end, the pocket with the
manual) are on its front part, the part the camera sees.

Everything else is at a station wagon's own size. egypt_car_things.py and egypt_car.py read these numbers, so the
skeleton, the picture and layout.json agree."""

import math

ID = "egypt-car"

# ---- the camera (the scene file takes `horizon` and `full` from layout.json)
VIEW = dict(horizon=181, full=282, cam=(46.0, 115.0), yaw=0.0, focal=500.0, centre_x=236.0)
PITCH = 7.0                                                 # the car's nose is this many degrees down (wagon.py draws it so)

# ---- the shell
W = 164.0                                                   # across, door to door at the belt line
BELT = 84.0                                                 # the belt line: the sills of the side windows, the top of the dash where it meets the glass
ROOF = 135.0                                                # the headliner, at the windshield's top
TUMBLE = 13.0                                               # how far each side leans in from the belt line to the roof
GLASS = dict(z0=0.0, z1=15.0, y0=BELT, y1=ROOF)             # the windshield: its foot (Z, Y) and its top
SIDE_TOP = 128.0                                            # the top of the side windows' openings (the roof rail below the headliner)

# ---- the dashboard: a padded top in the sun, a face toward Dad with a wood-grain strip across it
DASH = dict(top=BELT + 0.5, z_face=24.0, low=55.0, lip=2.4)            # its top's height, its face's Z, the height of its lower edge, the padded lip's radius
WOOD = (57.0, 61.0)                                                    # the wood-grain strip across the face, from .. to (Y): a band along its foot, under the glovebox
HOOD_CLUSTER = dict(x=(17.0, 76.0), top=88.0, z=28.0, opening=(19.0, 74.0, 66.0, 83.0))   # the hood over the gauges: across, its top, how far it reaches toward Dad; the opening under it (X0, X1, Y0, Y1)
DIALS = [(32.0, 74.5, 6.6), (60.0, 74.5, 6.6)]                         # the two dials: X, Y of the middle, radius (the speedometer, then fuel and temperature)
DIAL_Z = 20.0                                                          # their faces, set back under the hood
PRNDL = dict(x=(37.0, 55.0), y=(66.6, 68.2))                           # the strip under the dials, between them
STACK = dict(x=(70.0, 96.0))                                           # the middle of the dash: vents, radio, sliders, ashtray
VENTS = [(72.0, 80.5, 76.5, 82.0), (86.5, 95.0, 76.5, 82.0)]           # X0, X1, Y0, Y1: two square air vents
RADIO = dict(x=(70.5, 92.5), y=(68.0, 75.5))
SLIDERS = dict(x=(74.0, 93.0), y=(62.2, 66.2))
ASHTRAY = dict(x=(77.0, 90.0), y=(57.3, 60.7))
GLOVEBOX = dict(x=(103.0, 141.0), y=(61.5, 77.0), depth=20.0, r=3.2)   # the door's box on the face; the compartment's depth; the door's corner radius
GLOVE_OPEN = 82.0                                                      # degrees the door drops from shut (90: level; a little past, hanging at a slant)
CUP = dict(at=(95.5, 72.5, 28.6), r=(3.3, 4.2), y=(66.0, 83.5))       # the slushie in its clip-on holder on the right-hand vent: its middle (X, Y of the holder ring, Z), the cup's radius at its foot and rim, its foot and rim (Y)

# ---- the steering wheel, its column, the key, the gear lever
WHEEL = dict(c=(46.0, 79.5, 65.0), r=19.5, tube=1.15, tilt=25.0, hub=(10.5, 9.0))   # middle, rim radius, rim's thickness, tilt (its top toward the glass), horn pad (w, h)
COLUMN = dict(r=3.4, to_z=DASH["z_face"])                              # the column runs from the hub down into the dash, along the wheel's axis
KEY = dict(at=(57.0, 69.0, 50.0))                                      # the ignition, on the column's right side below the wheel
GEARS = dict(root=(50.0, 77.5, 57.0), knob=(66.5, 84.0, 60.0))         # the column shifter's stalk, and its knob

# ---- the bench: Dad's half (under him, out of the picture) and the Son's half (the cartoon's cheat: see above)
SEAT = dict(x=(78.0, W), top=64.0, front=45.0, back=118.0)             # the Son's cushion: across, its top, its front edge (Z), where it meets its back (Z)

# ---- the doors
DOOR_L = dict(armrest=(70.0, 76.0), pocket=(32.0, 48.0))               # the driver's door: the armrest's height (Y), the pocket's
DOOR_R = dict(armrest=(70.0, 76.0))

# ---- overhead: the visors and the rearview mirror (on the windshield's top, the car's middle line)
VISOR_D = dict(x=(14.0, 57.0), hinge_z=18.0, depth=20.0, thick=2.2)    # the driver's: across, its hinge (Z), how far it reaches, its thickness
VISOR_P = dict(x=(107.0, 150.0), hinge_z=18.0, depth=20.0, thick=2.2)  # the passenger's (plain: no mirror on either)
VISOR_DOWN = 75.0                                                      # degrees the driver's visor hangs from the headliner when pulled down
MIRROR = dict(x=W / 2, z=19.5, w=19.0, h=6.2, y=128.5)                 # the rearview mirror's body: middle across, Z, width, height, its middle's height
FRESHENER = dict(knot=(W / 2 + 2.0, 125.0, 18.5), card=(6.4, 3.4), drop=5.0)   # the string's knot on the mirror's stem; the card (w, h); the string's length

# ---- outside: the hood (the car's own, level in the car's frame: the car is what is tilted), the mound, the world
HOOD = dict(y=80.0, z_far=-300.0, x=(4.0, W - 4.0))                    # the hood's top: its height, its far end (the nose), across

# ---- where the game puts the lead (undrawn): the brief's fixed numbers, in picture pixels
MARK = (430, 590)
WALK = [[410, 580], [450, 580], [450, 598], [410, 598]]
BAND_TOP = 548                                                         # the bottom edge's band starts here (BANDS.S is 52)


def wheel_frame():
    """The wheel's own axes in the car: (u across the wheel's face, v up its face, n toward Dad, along the column)."""
    t = math.radians(WHEEL["tilt"])
    u = (1.0, 0.0, 0.0)
    v = (0.0, math.cos(t), -math.sin(t))                    # up the face: its top leans toward the glass (-Z)
    n = (0.0, math.sin(t), math.cos(t))                     # the column's axis, pointing at Dad
    return u, v, n


def wheel_pt(a_deg, rad=None, out=0.0):
    """A point on the wheel's plane: `a_deg` round from the right (counter-clockwise as Dad sees it), at `rad` from its
    middle, `out` toward Dad."""
    u, v, n = wheel_frame()
    r = WHEEL["r"] if rad is None else rad
    c = WHEEL["c"]
    a = math.radians(a_deg)
    return tuple(c[i] + r * (math.cos(a) * u[i] + math.sin(a) * v[i]) + out * n[i] for i in range(3))

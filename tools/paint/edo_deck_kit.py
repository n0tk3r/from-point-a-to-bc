"""PAINT-21B: the kit for the ship by day (edo-deck): the camera, the ship measured, the paints by name, and the act's
style-sheet tools (the graded bands, the flats, the keyblock contour: S/work-20-paintA/style.md), borrowed from Yui's kit.

World measurements are centimetres: x across the picture (0 is the picture's middle column, 400), y up from the deck,
z away from us (z = 0 is the deck at the row FULL). The camera is the act's outdoor kind (persp.Camera), so the game's
people come out the right size anywhere on the deck.

THE SHIP. Gonroku's coaster, a Suruga benzaisen of a few hundred koku (facts-21a item 6): her keel runs across the
picture, the bow at the left (-x) and the stern at the right (+x). We stand amidships on the port side (the near side is
cut away, as a stage's fourth wall: it is behind the camera) and look across her to starboard: she heads west-south-west
(the monkey), so we face north-north-west, toward the coast of Shima, and Daiozaki is a far grey cape off the starboard
bow (the left of the horizon). Inside her bulwarks she is 6 m across: the near side at z = -60, the far bulwark's inner
face at z = 540, the centreline z = 240.

    NEAR WALKWAY   the deck planks along the port side, z -60 to 150: the family's floor, from the bow to the stern
    THE HOLD       no deck over it: mat covers lashed over the cargo (bales, casks), z 150 to the far bulwark, in two
                   parts: forward (x -415 to -195) and aft (x -15 to 215), the mast's gangway between them
    THE MAST       on the centreline at x -90, built up and bound with iron rings; its step a block of timber at its foot
    THE STERN      the windlass (its drum athwartships, x 260, z 320 to 500), the long tiller (on the centreline, from the
                   rudder's head at the stern forward to x 360), the compass box on its post (x 300, z 200), the stern
                   deckhouse over the overhang (x 480 on, z 300 to 540)
    THE BOW        the deck narrowing to the single heavy stem timber at x -525, rising at the picture's left edge

LIGHT   Noon, the fifth day out, about 13 April 1830 (latitude 34 N): the sun high in the south (about 66 degrees up),
        behind us and to the left (we face NNW): faces turned to us, to the left and up are lit; shadows are short and
        fall away from us and a little to the right (SUN), flat and blue (style.md section 8).
"""

import math

import numpy as np

from brush import F32, Sheet, grid, lerp, mask_poly, noise, over, rgb
from persp import Camera
from postimp_paints import PAINTS
from edo_village_kit import Paper, bands, flat                    # the act's tools (PAINT-20A): the glazing sheet, the bands, the flats

W, H = 800, 600
HZ, FULL = 262, 590
CAM = Camera(HZ, FULL)                                           # eye 359 cm over the deck, Z0 875, focal 800, vanishing x 400
SHAPE = (H, W)
SUN = (0.225, 0.39)                                              # a point 1 cm up throws its shadow this far along x and z (cm)
SUN3 = np.array([-0.20, 0.91, -0.35], dtype=F32)                 # toward the sun (x right, y up, z away): high, behind us, a little left
SEA_DROP = 150.0                                                 # the sea's surface lies this far below the deck (cm)

# ---------------------------------------------------------------- the paints, by name (style.md section 2)
def P(name):
    return rgb(PAINTS[name]["hex"])


WHITE, NAPLES, CERULEAN, COBALT, ULTRA, PRUSSIAN = P("lead-white"), P("naples-yellow"), P("cerulean"), P("cobalt-blue"), P("ultramarine"), P("prussian-blue")
OCHRE, SIENNA, VERONESE, VIRIDIAN, LAKE, VERMILION = P("yellow-ochre"), P("burnt-sienna"), P("veronese-green"), P("viridian"), P("geranium-lake"), P("vermilion")


def mixp(a, b, t):
    a = P(a) if isinstance(a, str) else a
    b = P(b) if isinstance(b, str) else b
    return lerp(a, b, t)


def tintw(c, t):
    """A paint lightened with lead white (a tint)."""
    return lerp(c, WHITE, t)


def shade(c, t):
    """A paint darkened with prussian blue (never black)."""
    return lerp(c, PRUSSIAN, t)


PAPER = tintw(CERULEAN, 0.86)                                    # the sky at the horizon: the paper with a breath of blue
WOOD_LIT = lerp(tintw(OCHRE, 0.34), NAPLES, 0.18)                # weathered plank in the noon sun
WOOD_MID = tintw(OCHRE, 0.12)
WOOD_SHADE = lerp(SIENNA, PRUSSIAN, 0.22)                        # wood in its own shade
WOOD_DARK = lerp(SIENNA, PRUSSIAN, 0.55)
DECK_SHADOW = lerp(tintw(OCHRE, 0.30), COBALT, 0.42)             # a cast shadow on the planks: the plank pulled toward cobalt, flat
MAT_LIT = lerp(tintw(OCHRE, 0.48), NAPLES, 0.25)                 # the straw mat covers in the sun
MAT_SHADE = lerp(tintw(OCHRE, 0.30), COBALT, 0.38)
ROPE = lerp(tintw(OCHRE, 0.15), SIENNA, 0.25)
ROPE_DARK = lerp(SIENNA, PRUSSIAN, 0.35)
IRON = lerp(PRUSSIAN, ULTRA, 0.15)
SAIL_LIT = lerp(WHITE, NAPLES, 0.06)
SAIL_SHADE = lerp(tintw(CERULEAN, 0.62), WHITE, 0.10)
SAIL_DEEP = tintw(lerp(CERULEAN, COBALT, 0.35), 0.45)


# ---------------------------------------------------------------- the camera
def gp(x, z, y=0.0):
    """World -> picture."""
    return CAM.pt(x, y, z)


def kz(z):
    """Picture pixels per centimetre at depth z."""
    return CAM.scale(z)


def row_of(z, y=0.0):
    return gp(0.0, z, y)[1]


def floor(shape=SHAPE):
    return CAM.floor_grid(shape)


def sea_row(z):
    """The row of the sea's surface at distance z (it lies SEA_DROP below the deck)."""
    return gp(0.0, z, -SEA_DROP)[1]


# ---------------------------------------------------------------- the ship's lines (cm)
CL = 240.0                                                       # the centreline
NEAR_Z, FAR_Z = -60.0, 540.0                                     # the near side (cut away) and the far bulwark's inner face, amidships
BOW_X, STERN_X = -500.0, 700.0                                   # the stem, and the stern's end (beyond the picture)
WALK_Z = 150.0                                                   # the near walkway's inner edge: the hold's coaming
HOLD_F = (-420.0, -200.0)                                        # the forward hold (x)
GANG = (-200.0, -40.0)                                           # the mast's gangway across the ship (x)
HOLD_A = (-40.0, 175.0)                                          # the aft hold (x): short, so the windlass's men stand on the deck
MAST = dict(x=-120.0, z=CL, r=23.0)                               # the mast: 46 cm through at the deck
STEP = dict(x0=-178.0, x1=-62.0, z0=195.0, z1=290.0, h=48.0)     # the mast step: a block of timber round its foot (the Funadama is sealed in it)
HEARTH = dict(x0=-338.0, x1=-242.0, z0=88.0, z1=152.0, h=42.0)   # Kota's hearth box (the game's: facts-21a item 8)
POT = dict(x=-288.0, z=121.0, r=17.0)                            # the rice pot in it
BOAT = dict(x0=-472.0, x1=-208.0, z=335.0, beam=80.0, h=56.0)    # the ship's boat, lashed upside down on the forward mats
WINDLASS = dict(x=300.0, z0=320.0, z1=480.0, r=36.0, axis=88.0, bar=140.0)  # the windlass: a drum athwartships, its axis 86 cm up; two bars forward
TILLER = dict(x0=392.0, z0=176.0, x1=538.0, z1=CL, y=96.0)      # the long tiller, swung a little toward us, at hip height
RUDDER = dict(x0=520.0, x1=556.0, z0=222.0, z1=258.0, h=178.0)  # the rudder's head coming up through the stern (the blade is under the overhang)
COMPASS = dict(x=322.0, z=150.0, w=44.0, h=88.0)                 # the compass box on its post (84 cm to the box's top)
HOUSE = dict(x0=505.0, x1=785.0, z0=300.0, z1=FAR_Z, h=222.0)     # the stern deckhouse
BALE = dict(x0=40.0, x1=116.0, z=112.0, r=21.0)                   # the bale Seijiro sits on, by the aft hold
CARGO_TOP = 205.0                                                # the mat covers' crown over the cargo (heaped above the bulwark)


def half_width(x):
    """The hull's half-width inside the bulwarks at x (cm): 300 amidships, closing to the stem at BOW_X, a little
    narrower toward the stern."""
    if x < -40.0:
        t = (x + 40.0) / (BOW_X + 40.0)
        return 300.0 * math.sqrt(max(0.0, 1.0 - t * t))
    if x > 250.0:
        return 300.0 - 40.0 * ((x - 250.0) / 440.0) ** 2
    return 300.0


def far_z(x):
    """The far bulwark's inner face at x."""
    return min(FAR_Z, CL + half_width(x))


def sheer(x):
    """The far bulwark's top above the deck at x: a metre amidships, rising to the bow and a little to the stern."""
    return 100.0 + 92.0 * max(0.0, (-x - 170.0) / 355.0) ** 2 + 46.0 * max(0.0, (x - 200.0) / 490.0) ** 2


# ---------------------------------------------------------------- the keyblock (style.md section 4)
def contour_w(row):
    """The keyblock's weight at a picture row: 1.0 px at the front, 0.5 far off."""
    t = np.clip((row - HZ) / (FULL - HZ), 0, 1)
    return 0.5 + 0.5 * float(t)


def contour(sheet, pts, row=None, alpha=None, color=None, warm=False, pale=False):
    """The contour line along `pts` (picture points): prussian blue (burnt sienna on a warm dark thing); on a pale thing in
    full sun (the sail, the card) at alpha 0.45."""
    r = row if row is not None else max(p[1] for p in pts)
    w = contour_w(r)
    a = alpha if alpha is not None else (0.45 if pale else 0.55 + 0.3 * float(np.clip((r - HZ) / (FULL - HZ), 0, 1)))
    sheet.line(pts, color if color is not None else (SIENNA if warm else PRUSSIAN), w, a)
    return sheet


def lit(normal):
    """How much a face with this world normal takes the sun: 0 to 1."""
    n = np.asarray(normal, dtype=F32)
    n = n / (np.linalg.norm(n) + 1e-6)
    return float(np.clip(np.dot(n, SUN3), 0, 1))


def shadow_pts(pts3):
    """World points (x, y, z) laid on the deck along the sun -> picture points of their shadow."""
    return [gp(x + SUN[0] * max(y, 0.0), z + SUN[1] * max(y, 0.0)) for x, y, z in pts3]


def box_faces(x0, x1, y0, y1, z0, z1):
    """The faces of a box the camera sees, as world quads with their normals: the front (z0), the top (if below the
    eye), and the side that faces the picture's middle."""
    faces = []
    if x0 > 0:
        faces.append(("left", [(x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)], (-1, 0, 0)))
    if x1 < 0:
        faces.append(("right", [(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)], (1, 0, 0)))
    if y1 < CAM.eye:
        faces.append(("top", [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], (0, 1, 0)))
    faces.append(("front", [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], (0, 0, -1)))
    return faces


def P3(q):
    """A world point (x, y, z) -> picture."""
    return gp(q[0], q[2], q[1])

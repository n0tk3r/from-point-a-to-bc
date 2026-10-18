"""What is drawn on the Office's blueprint (OFFICE-17B), in picture pixels.

The ground floor in plan, north up, the front (the lot) at the bottom: a draughtsman's plan, eleven pixels to a foot.
The back (back.png) carries the sheet's own furniture (the border, the title block, the scale bar, the north arrow, the
general notes) and the building's walls, doors, the windowless front, the room numbers and the corridor: nothing of a
place. Each place is its own drawing:

  lot        the gravel lot in front: the chain-link fence and its gate, the flagpole, the limousine drawn as a long
             rectangle where it is parked, the walk to the front door and its keypad, the trash can by the downspout
  ducts      dotted over everything, the duct run from the roof's air-conditioning unit (drawn dashed: overhead) along
             the north wall to the B-7 shaft, its four grilles as small squares (ROOM C, PROP & EFF, BREAK, HALL)
  room       Interview Room C: the table and its three chairs, the corner chair under the grille, the long mirror, the
             water cooler, the plastic plant, the intercom, the thermostat
  property   Property & Effects: shelves round three walls (the vent over the top shelf), the low shelf with the banjo,
             Opal's counter and stool at her window onto the hall, the bell
  breakroom  the break room: the fridge under its grille, the counter with the sink and the coffee maker, the vending
             machine, the couch, Jed's chair, the corkboard
  b7         the B-7 shaft and the elevator, drawn as such (the shaft crossed, the car and its counterweight), and over them
             a rubber stamp in red: B-7 · RESTRICTED

and the one way, lot to ducts: a dashed route from the lot up the downspout to the roof and in at the unit's intake.
The duct is drawn along the north rooms' back wall, so that its drawing and the rooms' never overlap: each room's
things stand clear of the strip it runs along."""

import math

from map_office_kit import Pen

SHEET_BOX = (40, 136, 760, 564)
EAR = ((760, 136), 24)
CREASES = [("v", 400.0, 1.0), ("h", 352.0, 0.8)]
BORDER = (48, 144, 752, 556)
FT = 11.0                                                 # pixels a foot

# ---- the building
OUT = (64.0, 200.0, 648.0, 440.0)                        # outside faces of its walls
WALL = 7.0                                               # cinder block, eight inches
INNER = (OUT[0] + WALL, OUT[1] + WALL, OUT[2] - WALL, OUT[3] - WALL)    # 71, 207, 641, 433
PART = 4.0                                               # the partitions
ROOMS = {                                                # interiors, x0 y0 x1 y1
    "shaft": (71.0, 207.0, 143.0, 280.0),
    "elevator": (71.0, 284.0, 139.0, 356.0),
    "closet": (71.0, 360.0, 143.0, 433.0),
    "lobby": (147.0, 207.0, 185.0, 345.0),
    "breakroom": (189.0, 207.0, 311.0, 345.0),
    "property": (315.0, 207.0, 465.0, 345.0),
    "room": (469.0, 207.0, 641.0, 345.0),
    "hall": (147.0, 349.0, 641.0, 433.0),
}
NUMBERS = {"room": "101", "property": "102", "breakroom": "103", "hall": "CORR. 100", "closet": "JAN. 105"}
DOORS = {                                                 # (x0, x1) gaps in the rooms' south wall, and which way each swings
    "breakroom": (199.0, 227.0, "in"),
    "property": (427.0, 455.0, "in"),
    "room": (486.0, 515.0, "in"),
}
WINDOW = (343.0, 413.0)                                   # Opal's window, in Property's south wall
FRONT_DOOR = (372.0, 412.0)                               # in the building's south wall
ELEV_DOOR = (298.0, 344.0)                                # the elevator's door, in its east wall (y)
CLOSET_DOOR = (98.0, 126.0)

# ---- the duct (dotted), its grilles, the unit on the roof
DUCT_Y = (211.0, 223.0)                                   # the run's two sides
DUCT_X = (147.0, 596.0)                                   # from the shaft to the unit
UNIT = (596.0, 209.0, 637.0, 243.0)                       # the rooftop unit, overhead (dashed)
GRILLES = [("room", 548.0), ("property", 393.0), ("breakroom", 255.0), ("hall", 166.0)]
GRILLE = 10.0

# ---- the lot
LOT = (52.0, 446.0, 562.0, 548.0)                         # the gravel, inside the fence
FENCE_Y = 548.0
GATE = (112.0, 176.0)
FLAG = (88.0, 474.0)
LIMO = (206.0, 478.0, 384.0, 505.0)
TRASH = (671.0, 452.0)
DOWNSPOUT = (649.0, 433.0)

# ---- the sheet's furniture
TITLE = (574.0, 470.0, 750.0, 554.0)
SCALE = (560.0, 190.0)                                    # the scale bar's left end (its baseline), beside the north arrow
NORTH = (712.0, 178.0)
NOTES = (662.0, 262.0)

WAY_LINES = {}


def _wall(pen, x0, y0, x1, y1, hatch=True):
    """A wall of cinder block in plan: its two faces and the hatch of a cut masonry wall."""
    pen.rect(x0, y0, x1, y1, 1.1, "wall")
    if hatch and min(x1 - x0, y1 - y0) >= 5:
        pen.hatch([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 45.0, 2.4, 0.55, "thin")


def _gap(pen, pts):
    pen.clear(pts)


def draw_back(pen):
    """The sheet's furniture, the walls, doors and numbers (no place's things)."""
    bx0, by0, bx1, by1 = BORDER
    pen.rect(bx0, by0, bx1, by1, 1.3, "line")
    pen.rect(bx0 + 3, by0 + 3, bx1 - 3, by1 - 3, 0.6, "thin")
    # ---- the building's outside walls, with the front door's opening
    x0, y0, x1, y1 = OUT
    ix0, iy0, ix1, iy1 = INNER
    for (a, b, c, d) in ((x0, y0, x1, iy0), (x0, iy1, x1, y1), (x0, iy0, ix0, iy1), (ix1, iy0, x1, iy1)):
        _wall(pen, a, b, c, d)
    fd0, fd1 = FRONT_DOOR
    _gap(pen, [(fd0, iy1 - 0.5), (fd1, iy1 - 0.5), (fd1, y1 + 0.8), (fd0, y1 + 0.8)])
    pen.rule((fd0, iy1), (fd0, y1), 1.0, "line", 0)
    pen.rule((fd1, iy1), (fd1, y1), 1.0, "line", 0)
    # the front door: a pair of leaves swinging out onto the lot
    hw = (fd1 - fd0) / 2
    pen.rule((fd0, y1), (fd0, y1 + hw), 0.9, "line", 0)
    pen.rule((fd1, y1), (fd1, y1 + hw), 0.9, "line", 0)
    pen.arc((fd0, y1), hw, 0, 90, 0.6, "thin")
    pen.arc((fd1, y1), hw, 90, 180, 0.6, "thin")
    # ---- the partitions
    S = PART
    sh, el, cl, lo = ROOMS["shaft"], ROOMS["elevator"], ROOMS["closet"], ROOMS["lobby"]
    pen.rect(sh[2], iy0, sh[2] + S, iy1, 0.9, "line")                          # the core's east wall
    _gap(pen, [(sh[2] - 0.5, ELEV_DOOR[0]), (sh[2] + S + 0.5, ELEV_DOOR[0]), (sh[2] + S + 0.5, ELEV_DOOR[1]), (sh[2] - 0.5, ELEV_DOOR[1])])
    pen.rule((sh[2], ELEV_DOOR[0]), (sh[2] + S, ELEV_DOOR[0]), 0.9, "line", 0)
    pen.rule((sh[2], ELEV_DOOR[1]), (sh[2] + S, ELEV_DOOR[1]), 0.9, "line", 0)
    pen.rect(ix0, sh[3], sh[2], sh[3] + S, 0.9, "line")                        # shaft | elevator
    pen.rect(ix0, el[3], sh[2], el[3] + S, 0.9, "line")                        # elevator | closet
    pen.rect(el[2], el[1], el[2] + S, el[3], 0.9, "line")                      # the elevator's own east wall, its door in it
    _gap(pen, [(el[2] - 0.5, ELEV_DOOR[0] + 2), (el[2] + S + 0.5, ELEV_DOOR[0] + 2), (el[2] + S + 0.5, ELEV_DOOR[1] - 2), (el[2] - 0.5, ELEV_DOOR[1] - 2)])
    _gap(pen, [(CLOSET_DOOR[0], el[3] - 0.5), (CLOSET_DOOR[1], el[3] - 0.5), (CLOSET_DOOR[1], el[3] + S + 0.5), (CLOSET_DOOR[0], el[3] + S + 0.5)])
    pen.rule((CLOSET_DOOR[0], el[3]), (CLOSET_DOOR[0], el[3] + S), 0.9, "line", 0)
    pen.rule((CLOSET_DOOR[1], el[3]), (CLOSET_DOOR[1], el[3] + S), 0.9, "line", 0)
    pen.rule((CLOSET_DOOR[0], el[3] + S), (CLOSET_DOOR[0], el[3] + S + (CLOSET_DOOR[1] - CLOSET_DOOR[0])), 0.8, "line", 0)
    pen.arc((CLOSET_DOOR[0], el[3] + S), CLOSET_DOOR[1] - CLOSET_DOOR[0], 0, 90, 0.5, "thin")
    for nm in ("breakroom", "property", "room"):
        r = ROOMS[nm]
        if nm != "room":
            pen.rect(r[2], iy0, r[2] + S, r[3], 0.9, "line")                   # its east wall
    pen.rect(lo[2], iy0, lo[2] + S, lo[3], 0.9, "line")                        # lobby | break room
    yb = ROOMS["room"][3]
    pen.rect(lo[2], yb, ix1, yb + S, 0.9, "line")                              # the rooms' south wall onto the hall
    for nm, (d0, d1, how) in DOORS.items():
        _gap(pen, [(d0, yb - 0.5), (d1, yb - 0.5), (d1, yb + S + 0.5), (d0, yb + S + 0.5)])
        pen.rule((d0, yb), (d0, yb + S), 0.9, "line", 0)
        pen.rule((d1, yb), (d1, yb + S), 0.9, "line", 0)
        w = d1 - d0
        pen.rule((d0, yb), (d0, yb - w), 0.8, "line", 0)                       # the leaf, swung into the room
        pen.arc((d0, yb), w, 270, 360, 0.5, "thin")
    # Opal's window onto the hall: the wall's two faces, the glass between, a sill
    w0, w1 = WINDOW
    _gap(pen, [(w0, yb + 0.6), (w1, yb + 0.6), (w1, yb + S - 0.6), (w0, yb + S - 0.6)])
    pen.rule((w0, yb), (w0, yb + S), 0.9, "line", 0)
    pen.rule((w1, yb), (w1, yb + S), 0.9, "line", 0)
    pen.rule((w0, yb + S / 2), (w1, yb + S / 2), 0.5, "thin", 0)
    # ---- the room numbers and the corridor (small, as a plan carries them)
    for nm, t in NUMBERS.items():
        r = ROOMS[nm]
        if nm == "hall":
            pen.text(t, ((r[0] + r[2]) / 2 + 60, r[3] - 8), 6.0, "thin", anchor="ms", spacing=0.4)
        elif nm == "closet":
            pen.text(t, ((r[0] + r[2]) / 2, r[3] - 9), 5.5, "thin", anchor="ms", spacing=0.35)
        else:
            pen.text(t, (r[2] - 5, r[3] - 5), 6.0, "thin", anchor="rs", spacing=0.4)
    # an overall dimension along the west side, and one across the front
    dx = OUT[0] - 10
    pen.rule((dx, OUT[1]), (dx, OUT[3]), 0.55, "thin", 0)
    for yy in (OUT[1], OUT[3]):
        pen.rule((dx - 3, yy + 3), (dx + 3, yy - 3), 0.7, "thin", 0)
        pen.rule((dx - 4, yy), (OUT[0] - 2, yy), 0.4, "thin", 0)
    pen.text("21'-10\"", (dx - 3, (OUT[1] + OUT[3]) / 2 + 26), 5.5, "thin", anchor="ms", spacing=0.3)
    # ---- the title block
    tx0, ty0, tx1, ty1 = TITLE
    pen.rect(tx0, ty0, tx1, ty1, 1.2, "line")
    rows = [ty0 + 22, ty0 + 40, ty0 + 58, ty0 + 70]
    for ry in rows:
        pen.rule((tx0, ry), (tx1, ry), 0.6, "thin", 0)
    pen.rule((tx0 + 92, rows[2]), (tx0 + 92, ty1), 0.6, "thin", 0)
    pen.text("OFFICE OF PECULIAR SECTORS", ((tx0 + tx1) / 2, ty0 + 10), 6.6, "line", anchor="ms", spacing=0.30)
    pen.text("DESERT FIELD HQ", ((tx0 + tx1) / 2, ty0 + 19), 6.0, "thin", anchor="ms", spacing=0.45)
    pen.text("GROUND FLOOR", ((tx0 + tx1) / 2, ty0 + 35), 9.0, "line", anchor="ms", spacing=0.30)
    pen.text("PLAN · AIR SUPPLY & EXHAUST", ((tx0 + tx1) / 2, ty0 + 52), 5.4, "thin", anchor="ms", spacing=0.30)
    pen.text("SCALE 1/8\" = 1'-0\"", (tx0 + 5, ty0 + 67), 4.8, "thin", anchor="ls", spacing=0.28)
    pen.text("SHEET 1 OF 8", ((tx0 + 92 + tx1) / 2, ty0 + 67), 6.2, "line", anchor="ms", spacing=0.30)
    pen.text("DATE 3-14-51", (tx0 + 5, ty1 - 4), 4.8, "thin", anchor="ls", spacing=0.28)
    pen.text("DWG. OPS-1", ((tx0 + 92 + tx1) / 2, ty1 - 4), 4.8, "thin", anchor="ms", spacing=0.28)
    # ---- the scale bar, beside the north arrow, at the plan's own scale (FT pixels to a foot): 0 to 10 feet, the first
    #      five filled and ticked foot by foot (it stood under the building, where the trash can and the way up are)
    sx, sy = SCALE
    pen.rule((sx, sy), (sx + 10 * FT, sy), 0.7, "thin", 0)
    for k in (0, 5, 10):
        x = sx + k * FT
        pen.rule((x, sy - 3), (x, sy + 3), 0.7, "thin", 0)
    for k in range(1, 5):
        x = sx + k * FT
        pen.rule((x, sy - 1.6), (x, sy + 1.6), 0.5, "thin", 0)
    pen.fill([(sx, sy - 1.6), (sx + 5 * FT, sy - 1.6), (sx + 5 * FT, sy + 1.6), (sx, sy + 1.6)], "thin")
    for k, t in ((0, "0"), (5, "5"), (10, "10 FT")):
        pen.text(t, (sx + k * FT + (7 if k == 10 else 0), sy - 6), 4.6, "thin", anchor="ms", spacing=0.25)
    # ---- the north arrow
    nx, ny = NORTH
    pen.circle((nx, ny), 15.0, 0.8, "thin")
    pen.fill([(nx, ny - 13), (nx + 5, ny + 8), (nx, ny + 4)], "line")
    pen.poly([(nx, ny - 13), (nx - 5, ny + 8), (nx, ny + 4)], 0.7, "line")
    pen.text("N", (nx, ny - 18), 7.0, "line", anchor="ms", spacing=0.2)
    # ---- the general notes
    nx0, ny0 = NOTES
    lines = ["GENERAL NOTES", "1. ALL AIR TO B-7.", "2. RM. 101 TO BE", "   KEPT AT 72 F.", "3. NO CIVILIANS", "   BELOW GRADE.",
             "4. SEE SHEETS 2-8", "   (RESTRICTED)."]
    for i, t in enumerate(lines):
        pen.text(t, (nx0, ny0 + i * 10.5), 5.0 if i else 5.6, "thin", anchor="ls", spacing=0.26)
    pen.rule((nx0, ny0 + 2.5), (nx0 + 58, ny0 + 2.5), 0.5, "thin", 0)


# ---------------------------------------------------------------- the places
def _chair(pen, cx, cy, face, s=6.5):
    """A chair in plan: its seat, and its back on the side away from the way it faces."""
    pen.rect(cx - s, cy - s, cx + s, cy + s, 0.8, "line")
    b = 1.8
    if face == "E":
        pen.fill([(cx - s, cy - s), (cx - s + b, cy - s), (cx - s + b, cy + s), (cx - s, cy + s)])
    elif face == "W":
        pen.fill([(cx + s - b, cy - s), (cx + s, cy - s), (cx + s, cy + s), (cx + s - b, cy + s)])
    elif face == "S":
        pen.fill([(cx - s, cy - s), (cx + s, cy - s), (cx + s, cy - s + b), (cx - s, cy - s + b)])
    else:
        pen.fill([(cx - s, cy + s - b), (cx + s, cy + s - b), (cx + s, cy + s), (cx - s, cy + s)])


def place_room(pen):
    """Interview Room C."""
    x0, y0, x1, y1 = ROOMS["room"]
    # the table and its chairs: Grandpa Joe's on the west side, Dale's and Merle's across it
    pen.rect(521.0, 268.0, 591.0, 302.0, 1.0, "line")
    pen.rect(523.0, 270.0, 589.0, 300.0, 0.4, "thin")
    _chair(pen, 510.0, 285.0, "E")
    _chair(pen, 602.0, 276.0, "W")
    _chair(pen, 602.0, 294.0, "W")
    # the corner chair, against the north wall under the grille
    _chair(pen, 548.0, 241.0, "S", 6.0)
    pen.text("CHAIR", (548.0, 256.0), 3.8, "thin", anchor="ms", spacing=0.2)
    # the long mirror along the west wall (one way)
    pen.rect(x0 + 1.0, 250.0, x0 + 3.6, 322.0, 0.8, "line")
    pen.text("MIRROR", (x0 + 9.5, 286.0), 3.6, "thin", anchor="ms", spacing=0.2)
    # the water cooler in the south-east corner, the plastic plant in the north-west
    pen.circle((628.0, 330.0), 6.0, 0.8, "line")
    pen.circle((628.0, 330.0), 2.2, 0.6, "thin")
    pen.circle((483.0, 240.0), 6.5, 0.8, "line")
    for a in range(0, 360, 45):
        pen.rule((483.0, 240.0), (483.0 + 5.5 * math.cos(math.radians(a)), 240.0 + 5.5 * math.sin(math.radians(a))), 0.5, "thin", 0)
    # the intercom and the thermostat on the east wall
    pen.rect(x1 - 4.0, 268.0, x1 - 0.5, 278.0, 0.7, "line")
    pen.text("INTERCOM", (x1 - 8.0, 266.0), 3.4, "thin", anchor="rs", spacing=0.15)
    pen.circle((x1 - 3.0, 312.0), 2.6, 0.7, "line")
    pen.text("T", (x1 - 8.0, 314.0), 3.6, "thin", anchor="rs", spacing=0.1)


def place_property(pen):
    """Property & Effects."""
    x0, y0, x1, y1 = ROOMS["property"]
    # shelves to the ceiling round three walls: the north one under the duct (its top shelf under the grille)
    pen.rect(x0 + 2.0, 232.0, x1 - 2.0, 245.0, 0.9, "line")
    for k in range(1, 9):
        x = x0 + 2.0 + (x1 - x0 - 4.0) * k / 9
        pen.rule((x, 232.0), (x, 245.0), 0.4, "thin", 0)
    for sx in (x0 + 2.0, x1 - 15.0):
        pen.rect(sx, 247.0, sx + 13.0, 318.0, 0.9, "line")
        for k in range(1, 6):
            y = 247.0 + 71.0 * k / 6
            pen.rule((sx, y), (sx + 13.0, y), 0.4, "thin", 0)
    # the low shelf, and the banjo on it with its tag
    pen.rect(356.0, 285.0, 420.0, 296.0, 0.8, "line")
    pen.circle((372.0, 290.5), 4.6, 0.7, "line")
    pen.rule((376.6, 290.5), (398.0, 290.5), 0.9, "line", 0)
    pen.rect(398.0, 288.6, 402.0, 292.4, 0.5, "thin")
    pen.text("3117", (409.0, 283.0), 3.6, "thin", anchor="ms", spacing=0.15)
    # Opal's counter inside her window, her stool, her bell on the hall side
    pen.rect(345.0, 328.0, 411.0, 338.0, 0.9, "line")
    pen.circle((378.0, 318.0), 4.4, 0.8, "line")
    pen.dot((378.0, 352.5), 1.8)
    pen.text("BELL", (386.0, 354.5), 3.4, "thin", anchor="ls", spacing=0.15)


def place_breakroom(pen):
    """The break room."""
    x0, y0, x1, y1 = ROOMS["breakroom"]
    # the fridge, under its grille, and the counter with the sink and the coffee maker
    pen.rect(244.0, 233.0, 266.0, 254.0, 0.9, "line")
    pen.rule((244.0, 250.5), (266.0, 250.5), 0.4, "thin", 0)
    pen.text("REF.", (255.0, 245.0), 3.8, "thin", anchor="ms", spacing=0.15)
    pen.rect(269.0, 234.0, x1 - 2.0, 246.0, 0.9, "line")
    pen.rect(276.0, 236.0, 290.0, 244.0, 0.6, "thin")
    pen.circle((283.0, 240.0), 1.6, 0.5, "thin")
    pen.rect(296.0, 236.5, 304.0, 243.5, 0.6, "thin")
    # the corkboard on the wall over the counter
    pen.rule((271.0, 230.8), (x1 - 4.0, 230.8), 1.2, "line", 0)
    # the vending machine on the east wall, the couch along the west wall, Jed's chair, a small round table
    pen.rect(x1 - 15.0, 258.0, x1 - 2.0, 290.0, 0.9, "line")
    pen.rule((x1 - 15.0, 262.0), (x1 - 2.0, 262.0), 0.4, "thin", 0)
    pen.text("VEND.", (x1 - 19.0, 276.0), 3.6, "thin", anchor="rs", spacing=0.12)
    pen.rect(x0 + 2.0, 262.0, x0 + 18.0, 330.0, 0.9, "line")
    pen.rect(x0 + 2.0, 262.0, x0 + 6.5, 330.0, 0.5, "thin")
    for y in (284.6, 307.3):
        pen.rule((x0 + 6.5, y), (x0 + 18.0, y), 0.4, "thin", 0)
    _chair(pen, 270.0, 306.0, "N", 6.2)
    pen.circle((246.0, 296.0), 8.0, 0.8, "line")


def place_lot(pen):
    """The gravel lot in front of the building."""
    x0, y0, x1, y1 = LOT
    # the gravel: a stipple, thinner toward the edges
    import numpy as np
    rng = np.random.default_rng(7)
    for _ in range(820):
        x, y = rng.uniform(x0 + 2, x1 - 2), rng.uniform(y0 + 3, y1 - 3)
        if rng.random() < 0.35 or (LIMO[0] - 3 < x < LIMO[2] + 3 and LIMO[1] - 3 < y < LIMO[3] + 3):
            continue
        if FRONT_DOOR[0] - 4 < x < FRONT_DOOR[1] + 4 and y < 470:
            continue
        if abs(x - FLAG[0]) < 12 and abs(y - FLAG[1]) < 12:
            continue
        pen.dot((x, y), 0.42, "faint")
    # the chain-link fence along the front, the gate in it, two leaves swinging in
    g0, g1 = GATE
    for a, b in ((x0, g0), (g1, x1)):
        pen.rule((a, FENCE_Y), (b, FENCE_Y), 0.8, "line", 0)
        x = a + 4
        while x < b - 2:
            pen.rule((x - 1.6, FENCE_Y - 1.6), (x + 1.6, FENCE_Y + 1.6), 0.5, "thin", 0)
            pen.rule((x - 1.6, FENCE_Y + 1.6), (x + 1.6, FENCE_Y - 1.6), 0.5, "thin", 0)
            x += 9.0
    pen.rule((x0, FENCE_Y), (x0, y0 + 4), 0.8, "line", 0)
    pen.rule((x1, FENCE_Y), (x1, y0 + 30), 0.8, "line", 0)
    gw = (g1 - g0) / 2
    pen.rule((g0, FENCE_Y), (g0 + gw * 0.7, FENCE_Y - gw * 0.7), 0.8, "line", 0)
    pen.rule((g1, FENCE_Y), (g1 - gw * 0.7, FENCE_Y - gw * 0.7), 0.8, "line", 0)
    pen.arc((g0, FENCE_Y), gw, 315, 360, 0.5, "thin")
    pen.arc((g1, FENCE_Y), gw, 180, 225, 0.5, "thin")
    pen.text("GATE", ((g0 + g1) / 2, FENCE_Y - 4), 4.2, "thin", anchor="ms", spacing=0.2)
    # the flagpole and its pennant
    pen.circle(FLAG, 3.0, 0.8, "line")
    pen.dot(FLAG, 1.0)
    pen.poly([(FLAG[0] + 3, FLAG[1] - 1.5), (FLAG[0] + 14, FLAG[1] + 2), (FLAG[0] + 3, FLAG[1] + 4.5)], 0.6, "thin")
    # the walk to the front door, and the keypad beside the door
    pen.rule((FRONT_DOOR[0] - 2, OUT[3] + 20), (FRONT_DOOR[0] - 2, OUT[3] + 34), 0.5, "thin", 0)
    pen.rule((FRONT_DOOR[1] + 2, OUT[3] + 20), (FRONT_DOOR[1] + 2, OUT[3] + 34), 0.5, "thin", 0)
    pen.rect(FRONT_DOOR[1] + 4, OUT[3] + 2, FRONT_DOOR[1] + 9, OUT[3] + 7, 0.6, "line")
    pen.text("KEYPAD", (FRONT_DOOR[1] + 12, OUT[3] + 8), 3.6, "thin", anchor="ls", spacing=0.15)
    # the limousine, parked: a long rectangle, its glass and its wheels
    lx0, ly0, lx1, ly1 = LIMO
    pen.poly([(lx0 + 5, ly0), (lx1 - 5, ly0), (lx1, ly0 + 5), (lx1, ly1 - 5), (lx1 - 5, ly1), (lx0 + 5, ly1), (lx0, ly1 - 5), (lx0, ly0 + 5)], 1.0, "line")
    pen.rect(lx0 + 24, ly0 + 3.5, lx1 - 30, ly1 - 3.5, 0.5, "thin")
    pen.rule((lx1 - 30, ly0 + 3.5), (lx1 - 20, ly0 + 6), 0.5, "thin", 0)
    pen.rule((lx1 - 30, ly1 - 3.5), (lx1 - 20, ly1 - 6), 0.5, "thin", 0)
    pen.rule((lx1 - 20, ly0 + 6), (lx1 - 20, ly1 - 6), 0.5, "thin", 0)
    for wx in (lx0 + 16, lx1 - 16):
        pen.rect(wx - 6, ly0 - 2.5, wx + 6, ly0, 0.6, "thin")
        pen.rect(wx - 6, ly1, wx + 6, ly1 + 2.5, 0.6, "thin")
    pen.text("LIMOUSINE", ((lx0 + lx1) / 2 - 4, (ly0 + ly1) / 2 + 2.5), 4.4, "thin", anchor="ms", spacing=0.3)
    # the trash can by the downspout at the corner
    pen.circle(TRASH, 6.0, 0.8, "line")
    pen.circle(TRASH, 4.2, 0.4, "thin")
    pen.text("T.C.", (TRASH[0] + 9, TRASH[1] + 2), 3.8, "thin", anchor="ls", spacing=0.15)


def place_ducts(pen):
    """The duct run, dotted (overhead), from the unit on the roof to the B-7 shaft; its four grilles."""
    x0, x1 = DUCT_X
    ya, yb = DUCT_Y
    for y in (ya, yb):
        pen.dots([(x0, y), (x1, y)], r=0.75, gap=3.4, weight="line")
    # the unit on the roof (dashed: overhead), its fan, and the intake's arrow into it
    ux0, uy0, ux1, uy1 = UNIT
    pen.dashed([(ux0, uy0), (ux1, uy0), (ux1, uy1), (ux0, uy1)], 0.9, "line", on=4.0, off=2.6, closed=True)
    pen.circle(((ux0 + ux1) / 2, (uy0 + uy1) / 2), 9.0, 0.6, "thin")
    for a in (20, 110, 200, 290):
        r = math.radians(a)
        pen.rule(((ux0 + ux1) / 2, (uy0 + uy1) / 2), ((ux0 + ux1) / 2 + 8 * math.cos(r), (uy0 + uy1) / 2 + 8 * math.sin(r)), 0.7, "thin", 0)
    pen.text("A.C. UNIT", ((ux0 + ux1) / 2, uy1 - 2.5), 3.6, "thin", anchor="ms", spacing=0.15)
    pen.text("ABOVE", ((ux0 + ux1) / 2, uy0 + 6.0), 3.6, "thin", anchor="ms", spacing=0.15)
    # the grilles: small squares across the run, each crossed (a ceiling register)
    yc = (ya + yb) / 2
    for gid, gx in GRILLES:
        h = GRILLE / 2
        pen.rect(gx - h, yc - h, gx + h, yc + h, 0.9, "line")
        pen.rule((gx - h, yc - h), (gx + h, yc + h), 0.5, "thin", 0)
        pen.rule((gx - h, yc + h), (gx + h, yc - h), 0.5, "thin", 0)
    # the arrow of the air along the run, toward the shaft
    pen.arrowhead((x0 + 6.0, yc), (x0 + 30.0, yc), 4.0, "line")


def place_b7(pen):
    """The B-7 shaft and the elevator (the stamp over them is laid with the ink: map_office.py)."""
    sx0, sy0, sx1, sy1 = ROOMS["shaft"]
    pen.rule((sx0 + 2, sy0 + 2), (sx1 - 2, sy1 - 2), 0.9, "line", 0)
    pen.rule((sx0 + 2, sy1 - 2), (sx1 - 2, sy0 + 2), 0.9, "line", 0)
    pen.rect(sx0 + 2, sy0 + 2, sx1 - 2, sy1 - 2, 0.6, "thin")
    pen.text("SHAFT", ((sx0 + sx1) / 2, sy0 + 15), 4.4, "thin", anchor="ms", spacing=0.25)
    pen.text("DN.", ((sx0 + sx1) / 2, sy1 - 7), 4.0, "thin", anchor="ms", spacing=0.25)
    ex0, ey0, ex1, ey1 = ROOMS["elevator"]
    pen.rect(ex0 + 5, ey0 + 5, ex1 - 9, ey1 - 5, 0.9, "line")                  # the car
    pen.rule((ex0 + 5, ey0 + 5), (ex1 - 9, ey1 - 5), 0.5, "thin", 0)
    pen.rule((ex0 + 5, ey1 - 5), (ex1 - 9, ey0 + 5), 0.5, "thin", 0)
    pen.rect(ex0 + 2, ey0 + 24, ex0 + 4.5, ey1 - 24, 0.6, "thin")              # its counterweight
    pen.rule((ex1 - 6, ELEV_DOOR[0] + 4), (ex1 - 6, ELEV_DOOR[1] - 4), 1.0, "line", 0)   # its doors
    pen.text("ELEV.", ((ex0 + ex1) / 2 - 2, ey1 + 0.0 - 9.0), 4.0, "thin", anchor="ms", spacing=0.25)


STAMP = dict(centre=(106.0, 296.0), lines=["B-7", "RESTRICTED"], cap=10.5, angle=7.0)


PLACES = {"lot": place_lot, "ducts": place_ducts, "room": place_room, "property": place_property,
          "breakroom": place_breakroom, "b7": place_b7}


def way_lot_ducts(pen):
    """From the lot, round to the corner, up the downspout to the roof, and along to the unit's intake: a dashed route
    with an arrow, as a plan marks a way."""
    pts = [(562.0, 462.0), (646.0, 462.0), (656.0, 452.0), (656.0, 300.0), (656.0, 232.0), (642.0, 226.0)]
    pen.dashed(pts, 0.9, "line", on=4.5, off=3.0)
    pen.arrowhead((641.0, 226.0), (656.0, 231.0), 4.2, "line")
    pen.text("UP", (662.0, 392.0), 4.6, "thin", anchor="ls", spacing=0.2)
    pen.arrowhead((656.0, 372.0), (656.0, 382.0), 3.4, "line")
    WAY_LINES[("lot", "ducts")] = pts


WAYS = {("lot", "ducts"): way_lot_ducts}

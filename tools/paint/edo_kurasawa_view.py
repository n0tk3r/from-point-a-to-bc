"""PAINT-23 (round twenty-three, RECOMPOSE: tools/paint/DEPTH.md): Nishikurasawa's new camera, and the place measured
through it. Shared by edo_kurasawa.py (the painting), edo_kurasawa_plan.py (the skeleton), edo_kurasawa_layout.py (every
number of the scene file) and edo_kurasawa_play.py. (edo_kurasawa_kit.py, round twenty-one's kit, is the top of the
pass's too: it is imported and never changed.)

Round twenty-one's picture looked straight across the road at the bay from 3.2 m up: the teahouse square-on like a box,
the ground an empty band. This one stands ON THE TOKAIDO at the rest village, a few steps short of O-Kuni's teahouse, and
looks along the road the way it goes: west, toward the pass (the act's compass, as at Yui: the bay on the left with Fuji
across it, the way west to the right).

THE CAMERA. persp.Camera(HZ, FULL), a slightly wide lens (FOCAL 680: 61 degrees across). The eye is 2.4 m above the road
(FULL - HZ = 220): a grown-up is 95 to 150 px where people stand, and the ground is 43 per cent of the picture. The road
and everything set along it are TURNED (THETA, 34 degrees from the line of sight): two vanishing points, the road's and
the teahouse's front off the right edge, the teahouse's ends far off to the left. Nothing faces us square.

    P(X, Z, Y)   the picture point of a place: X cm to the right of the line of sight, Z cm away from the lens, Y cm up
    G(px, py)    the place on the ground (X, Z) under a picture point
    k(Z)         picture pixels per centimetre at Z

THE PLACE (cm; the lens at X 0, Z 0; U along the road toward the pass, NL to its left, the bay's side, NR to its right):
  the road         the Tokaido, 4.6 m wide, in from behind us on the left and away to the right along the teahouse;
                   at the rest place it bends right and starts up the hill (the climb), out at the right edge
  the teahouse     O-Kuni's, on the bay's side of the road: its open front along the road under a deep eave on posts,
                   its near end (a reed blind hung against the morning sun) at the left edge, the door at the far end
                   with the grill out before it and the signboard at the corner
  the rest place   the trodden ground at the bend: out to the low wall over the shore on the left; on the right, behind
                   the climb, the 40th distance mound and its hackberry at the foot of Mount Satta
  the bank         the inland verge, on our right: Soshichi's trunks set down on it; along the bottom the bank's lip
  the bay          beyond the wall; Fuji across it (as at Yui), the far shore curving back toward Yui at the left, two
                   capes stepping out from under Satta
"""

import math

import numpy as np

from persp import Camera
from brush import F32, grid

W, H = 800, 600
SHAPE = (H, W)
HZ, FULL = 342, 562
FOCAL = 680.0
CAM = Camera(HZ, FULL, vanish_x=400.0, focal=FOCAL)
EYE, Z0 = CAM.eye, CAM.Z0                                  # 240.6 cm; the lens distance of the row FULL
THETA = math.radians(45.0)
U = (math.sin(THETA), math.cos(THETA))                     # along the road, toward the pass
NL = (-math.cos(THETA), math.sin(THETA))                   # the road's left: the bay's side
NR = (math.cos(THETA), -math.sin(THETA))                   # the road's right: inland
VP_ROAD = 400.0 + FOCAL * math.tan(THETA)                  # where the road and the teahouse's front run to
VP_END = 400.0 - FOCAL / math.tan(THETA)                   # where the teahouse's ends run to


def P(X, Z, Y=0.0):
    """A place (cm: X across, Z away from the lens, Y up) -> its picture point."""
    return CAM.pt(X, Y, Z - Z0)


def k(Z):
    """Picture pixels per centimetre at a lens distance Z."""
    return FOCAL / max(Z, 1.0)


def G(px, py):
    """The place on the ground (X, Z) under a picture point below the horizon."""
    Z = EYE * FOCAL / max(py - HZ, 1e-3)
    return ((px - 400.0) * Z / FOCAL, Z)


def row_of(Z):
    return HZ + EYE * FOCAL / Z


def grownup_px(row):
    """The engine's size of a grown-up whose feet are on a row."""
    return 160.0 * (row - HZ) / (FULL - HZ)


def add(p, d, s=1.0):
    return (p[0] + d[0] * s, p[1] + d[1] * s)


def ground_grid(shape=SHAPE):
    """For every pixel below the horizon: the place on the ground (X, Z), and a mask of where the ground is."""
    px, py = grid(shape)
    below = py > HZ + 0.5
    Z = EYE * FOCAL / np.maximum(py + 0.5 - HZ, 0.5)
    X = (px + 0.5 - 400.0) * Z / FOCAL
    return X.astype(F32), Z.astype(F32), below.astype(F32)


def rnd(p):
    return [int(round(p[0])), int(round(p[1]))]


# ---------------------------------------------------------------- the sun (the act's: behind us and to the left)
# A point 1 cm up throws its shadow SUN[0] cm along X and SUN[1] cm along Z: to the right and away. (The act's sun in the
# east about 40 degrees up, an hour into the morning, low along the road from Yui: behind us and to the left, as at Yui and in
# round twenty-one. The teahouse's front, along the road, takes it edge-on and lies in shade; its near end is in full sun.)
SUN = (0.85, 0.85)
SUN3 = np.array([-0.543, 0.640, -0.543], dtype=F32)        # toward the sun (X right, Y up, Z away): 40 degrees up, straight down the road from Yui


def shadow_of(X, Z, Y):
    """Where a point's shadow falls on the ground: (X, Z)."""
    return (X + SUN[0] * max(Y, 0.0), Z + SUN[1] * max(Y, 0.0))


# ---------------------------------------------------------------- the road
ROAD_W = 460.0
ROAD_A = (-470.0, 560.0)                                   # a point of the road's middle line, near us (behind the frame's bottom)
S_BEND = 470.0                                             # where along it the bend begins
BEND_R = 640.0                                             # the bend's radius (the middle line), turning right
BEND_TO = math.radians(98.0)                               # the road's heading after the bend (from the line of sight): right, and a little toward us


def road_mid(s):
    """The road's middle line s cm along it from ROAD_A: straight to S_BEND, then round the bend to the right and on."""
    if s <= S_BEND:
        return add(ROAD_A, U, s)
    b = add(ROAD_A, U, S_BEND)
    c = add(b, NR, BEND_R)                                 # the bend's middle
    turn = BEND_TO - THETA
    arc = BEND_R * turn
    if s <= S_BEND + arc:
        a = (s - S_BEND) / BEND_R                          # how far round
        h0 = THETA + a
        return (c[0] - math.cos(h0) * BEND_R, c[1] + math.sin(h0) * BEND_R)
    e = (c[0] - math.cos(BEND_TO) * BEND_R, c[1] + math.sin(BEND_TO) * BEND_R)
    return add(e, (math.sin(BEND_TO), math.cos(BEND_TO)), s - S_BEND - arc)


def road_dir(s):
    a, b = road_mid(s - 2), road_mid(s + 2)
    d = math.hypot(b[0] - a[0], b[1] - a[1])
    return ((b[0] - a[0]) / d, (b[1] - a[1]) / d)


def road_edge(s, side, extra=0.0):
    """The road's edge: side -1 its left (the bay's side), +1 its right."""
    m = road_mid(s)
    dx, dz = road_dir(s)
    n = (-dz, dx) if side < 0 else (dz, -dx)
    return add(m, n, ROAD_W / 2 + extra)


S_CLIMB = S_BEND + BEND_R * (BEND_TO - THETA)              # where the road starts to climb
CLIMB_RISE = 0.16                                          # it climbs 16 cm in every metre from there


def road_lift(s):
    return max(0.0, s - S_CLIMB) * CLIMB_RISE


def road_pt(s, side=0, Y=0.0, extra=0.0):
    """A picture point of the road: its middle (side 0) or an edge, at its own height there."""
    q = road_mid(s) if side == 0 else road_edge(s, side, extra)
    return P(q[0], q[1], road_lift(s) + Y)


# ---------------------------------------------------------------- O-Kuni's teahouse
class Tea:
    """The teahouse: its front along the road, set back from the road's left edge; its near end toward us (east, the
    morning sun on it), the far end toward the pass. A thatched hip roof, its eave deep over the front on a row of posts.
    u: along the front from its near corner; w: back from the front (negative: out toward the road)."""
    s0 = 70.0                  # along the road from ROAD_A, the front's near corner
    back = 150.0               # the front set back from the road's left edge
    L, D = 660.0, 470.0        # the front's length; the depth back to the bay's side
    floor = 46.0               # the matted room's floor (the earth floor at the door is the ground)
    eave = 288.0               # the thatch's lower edge over the front
    over = 104.0               # how far the eave stands out over the front (a row of posts carries it)
    over_end = 90.0            # and over the ends
    thick = 44.0               # the thatch's cut edge
    pitch = 47.0               # the thatch's slope, degrees
    door = (450.0, 580.0)      # the door to the earth floor, along the front from the near corner
    posts = (0.0, 150.0, 300.0, 450.0, 580.0, 660.0)

    def __init__(self):
        e = road_edge(self.s0, -1)
        self.c0 = add(e, NL, self.back)                    # the front's near corner on the ground
        t = math.tan(math.radians(self.pitch))
        self.t = t
        self.ridge_in = self.D / 2                          # the ridge runs along the middle of the depth
        self.ridge_h = self.eave + self.thick + (self.ridge_in + self.over) * t
        self.hip_in = (self.ridge_h - self.eave - self.thick) / t - self.over_end     # where the hips meet the ridge, in from each end

    def xz(self, u, w):
        """u cm along the front from its near corner, w cm back from the front (negative: out toward the road)."""
        return add(add(self.c0, U, u), NL, w)

    def pt(self, u, w, y=0.0):
        X, Z = self.xz(u, w)
        return P(X, Z, y)

    def roof_pts(self):
        """The roof's corners, (u, w): the eave's four corners and the ridge's two ends; e and top their heights."""
        o, oe = self.over, self.over_end
        return dict(A=(-oe, -o), B=(self.L + oe, -o), C=(self.L + oe, self.D + oe), D=(-oe, self.D + oe),
                    R0=(self.hip_in, self.ridge_in), R1=(self.L - self.hip_in, self.ridge_in), e=self.eave, top=self.ridge_h)


TEA = Tea()

# what stands at the teahouse (u along its front, w back from it: negative is out toward the road)
BENCH = dict(u0=60.0, u1=330.0, w0=-100.0, w1=-58.0, h=44.0)         # the bench under the eave, along the front
GRILL = dict(u=518.0, w=-162.0, len=120.0, wid=48.0, h=44.0)        # O-Kuni's grill, out before the door
KUNI_AT = dict(u=530.0, w=-104.0)                                   # O-Kuni behind it, before her door
SIGN = dict(u=694.0, w=-140.0, h=162.0, wid=36.0)                   # the signboard at the far corner, toward the road

# ---------------------------------------------------------------- the rest place, the mound, the palanquin, the trunks
MOUND = dict(X=560.0, Z=1590.0, r=270.0, h=210.0)                  # the 40th distance mound, beyond the bend at Satta's foot
HACK = dict(r=44.0)                                                 # the hackberry's trunk
KAGO = dict(X=300.0, Z=1310.0, length=96.0, width=84.0, height=104.0, pole=420.0)   # the palanquin, set down at the mound's foot
TRUNKS = dict(X=300.0, Z=815.0, w=60.0, d=44.0, tier=15.0, n=5)    # Soshichi's willow trunks, on the inland verge
WALL = [(-1400.0, 1640.0), (-700.0, 1820.0), (-200.0, 1980.0), (200.0, 2130.0), (520.0, 2300.0)]   # the low wall over the shore


# ================================================================ the far plane, as picture points
FUJI_AT = (312.0, 132.0)                                   # the summit's middle
FUJI_FOOT, FUJI_HALF = HZ + 2.0, 372.0                     # the row it stands on, its half width there


def fuji_outline(n=48):
    sx, sy = FUJI_AT
    side = []
    for i in range(n + 1):
        t = i / n
        side.append((t, sy + (FUJI_FOOT - sy) * t, 11 + (FUJI_HALF - 11) * t ** 1.7))
    return [(sx - h, y) for t, y, h in side[::-1]] + [(sx + h, y) for t, y, h in side]


FUJI_OUTLINE = fuji_outline()
FUJI_SNOW = [(FUJI_AT[0] - 11, FUJI_AT[1])] + [(FUJI_AT[0] + dx, FUJI_AT[1] + dy) for dx, dy in ((-60, 70), (-38, 62), (-20, 78), (0, 64), (22, 80), (44, 64), (70, 74))] + [(FUJI_AT[0] + 11, FUJI_AT[1])]
CAP = [(FUJI_AT[0] - 70, FUJI_AT[1] + 14), (FUJI_AT[0] - 40, FUJI_AT[1] - 6), (FUJI_AT[0] + 10, FUJI_AT[1] - 14), (FUJI_AT[0] + 60, FUJI_AT[1] - 4),
       (FUJI_AT[0] + 80, FUJI_AT[1] + 12), (FUJI_AT[0] + 10, FUJI_AT[1] + 22)]
FAR_SHORE = [(-10, HZ + 1), (-10, HZ - 7), (120, HZ - 6), (260, HZ - 8), (380, HZ - 5), (470, HZ - 4), (470, HZ + 1)]
CAPES = [[(430, HZ + 2), (452, HZ - 6), (486, HZ - 9), (520, HZ - 13), (540, HZ - 10), (540, HZ + 2)],
         [(470, HZ + 4), (492, HZ - 4), (520, HZ - 12), (548, HZ - 20), (560, HZ - 18), (560, HZ + 4)]]
SATTA = [(530, HZ + 30), (540, HZ - 4), (558, 306), (580, 272), (606, 240), (632, 210), (660, 176), (690, 136), (722, 94), (756, 48), (790, 6), (812, -10),
         (812, 520), (530, 520)]
CLIFF_ROAD = [(560, 326), (604, 306), (650, 290), (700, 276), (760, 258), (812, 244)]


def satta_foot():
    """Where Mount Satta's slope meets the level ground (the rest place, and the road's climb), left to right."""
    pts = []
    for X in np.linspace(260.0, 1500.0, 14):
        Z = 2350.0 - 0.55 * (X - 260.0)
        pts.append(P(X, Z))
    return pts


def ground_outline():
    """The level ground: from the wall over the shore (left) to Satta's foot (right), down to the bottom."""
    wall = [P(X, Z) for X, Z in WALL]
    foot = satta_foot()
    return [(-10, wall[0][1])] + wall + foot + [(812, foot[-1][1]), (812, 612), (-10, 612)]


def road_outline():
    left = [road_pt(s, -1) for s in np.linspace(-300, S_CLIMB + 1400, 46)]
    right = [road_pt(s, 1) for s in np.linspace(S_CLIMB + 1400, -300, 46)]
    return [p for p in left + right]


def climb_outline():
    return [road_pt(s, -1) for s in np.linspace(S_CLIMB, S_CLIMB + 1400, 12)] + [road_pt(s, 1) for s in np.linspace(S_CLIMB + 1400, S_CLIMB, 12)]


def wall_outline():
    top = [P(X, Z, 60) for X, Z in WALL]
    foot = [P(X, Z) for X, Z in WALL]
    return top + foot[::-1]


def hack_crown():
    m = MOUND
    pts = []
    for a in np.linspace(0, 2 * math.pi, 40)[:-1]:
        X = m["X"] + 330 + math.cos(a) * 640
        Y = m["h"] + 820 + math.sin(a) * 480
        pts.append(P(X, m["Z"], Y))
    return pts


# ================================================================ where people stand (the walk, the marks)
def walk_outline():
    """The walkable ground: the road, the trodden ground beside it before the teahouse and at the rest place, the inland
    verge, the climb's foot; short of the wall, the mound and the bank's lip."""
    pts = [(0, 600), (0, 556)]
    pts += [P(*TEA.xz(u, -40.0)) for u in np.linspace(-40.0, TEA.L + 40, 7)]
    pts += [P(X, Z - 160) for X, Z in WALL[2:]]
    pts += [road_pt(s, -1, extra=-30) for s in np.linspace(S_CLIMB + 100, S_CLIMB + 700, 4)]
    pts += [(800, road_pt(S_CLIMB + 760, -1)[1] + 4), (800, 600)]
    return [rnd(p) for p in pts]


WALK = walk_outline()
BLOCKED = []


def marks_for_plan():
    """Every mark and standing place, for the skeleton: name -> (x, y, who)."""
    out = {}
    T = TEA
    put = lambda name, q, who: out.__setitem__(name, (P(*q)[0], P(*q)[1], who))
    put("arrive_mom", add(road_mid(-140), NR, 40), "mom")
    put("arrive_bigsis", add(road_mid(-230), NR, 120), "bigsis")
    put("arrive_lilsis", add(road_mid(-110), NL, 60), "lilsis")
    put("teahouse", T.xz(200.0, -260.0), "mom")
    put("kuni", T.xz(KUNI_AT["u"], KUNI_AT["w"]), "woman")
    put("peddler", add(add((TRUNKS["X"], TRUNKS["Z"]), U, 100), NR, 70), "man")
    put("bearers", add((KAGO["X"], KAGO["Z"]), U, -150), "man")
    put("tora", add(add((KAGO["X"], KAGO["Z"]), U, -90), NL, -80), "man")
    put("mound", (350.0, 1300.0), "mom")
    put("komuso", T.xz(T.L + 60, -250), "man")
    put("view", T.xz(T.L + 150, -120), "bigsis")
    put("climb", road_mid(S_CLIMB + 300), "mom")
    return out


def near_outlines():
    """The near plane (for the skeleton): the teahouse's near corner (post, eave and blind) at the left edge; a black
    pine's bough over the top right corner; the bank's lip along the bottom right."""
    T = TEA
    r = T.roof_pts()
    eave_near = [T.pt(-T.over_end, -T.over, T.eave), T.pt(-T.over_end, 140, T.eave), T.pt(-T.over_end, 140, T.eave + T.thick),
                 T.pt(-T.over_end, -T.over, T.eave + T.thick)]
    blind = [T.pt(-20, -T.over + 10, T.eave), T.pt(-20, 200, T.eave), T.pt(-20, 200, 110), T.pt(-20, -T.over + 10, 96)]
    post = [T.pt(-6, -T.over + 4, 0), T.pt(6, -T.over + 4, 0), T.pt(6, -T.over + 4, T.eave), T.pt(-6, -T.over + 4, T.eave)]
    bough = [(812, -10), (470, -10), (500, 20), (560, 40), (620, 50), (680, 80), (730, 130), (780, 190), (812, 200)]
    bank = [(380, 612), (420, 590), (520, 584), (640, 576), (760, 566), (812, 562), (812, 612)]
    return [eave_near, blind, post, bough, bank]

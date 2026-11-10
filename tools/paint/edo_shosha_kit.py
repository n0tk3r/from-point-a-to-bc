"""PAINT-23 (round twenty-three, RECOMPOSE and the act's watercolour): the foot of Mount Shosha (edo-shosha), its camera,
its place measured and its two lights; shared by edo_shosha.py (the painter), edo_shosha_plan.py (the skeleton),
edo_shosha_layout.py (every number of the scene file) and edo_shosha_play.py (the scene played). Round twenty-one's
picture (PAINT-21E) was the flattest of the act: the hall and the hut boxes seen square-on from 3.4 m up, the mountain a
flat green wedge. This one is seen through one camera, lower and turned.

THE PLACE (the research of round twenty-one holds). The women's hall of Engyo-ji, about 29 April 1830, at the foot of the
east path, where women stopped: women might not climb Mount Shosha (such barred mountains had a stone at the path's foot
saying so; this one is the game's, its writing our own marks). The hall (today's Nyoirin-ji; what it looked like in 1830
is not recorded): small and deep-roofed, two ken square on a low stone base, a pyramid roof of tiles with a jewel on its
peak (a hoju in a lotus cup: nothing on it reads as a cross), its latticed double doors to the south with the name slips
pasted round them, a lattice window in its west side that the sunset comes through (edo-hall, inside: the west lattice
at the left, the doors behind the lens). The mountain rises behind it in pines and maples in new leaf, a late cherry in
the shade; the east path climbs into the trees in worn stone steps and is gone; at its foot the small stone. O-Ume's
thatched hut, its paper lantern on a hook by the door; the bench where the women wait, and their failed combs and pins in
a heap on a cloth. Beyond the terrace's edge, far below, the Harima plain, and on its hill, small and white, the castle:
it lies south-east of the hall, and the picture puts it at the right, beyond the hall, as round twenty-one did (a liberty
of the prints' kind); it is drawn about three times larger than the eye would see it 6 km off ("the size of a thumbnail").

THE CAMERA. We stand on the terrace south-west of the hall, by an old pine and a stone lantern, and look north-north-east
along the foot of the mountain, the eye 2.52 m above the terrace (`full` - `horizon` = 230), level, the lens 700 px (a
little wide). The hall stands near us at the right, square to the compass, so we see it three-quarters on: its west side
(the lattice) running back toward the mountain at the left, its front (the doors) running away to the right; its two
vanishing points lie on the horizon, one near the left edge and one far off at the right. Its roof rises into the boughs
of the near pine's neighbour, which reach in over the top right. To the left of it the path's foot, the stone and
Ryokai's step, the hut farther off under the trees; to its right, past its corner and the terrace's edge, the gap: the
plain far below in layers of air, the far hills, the sky.

    P(X, Y, D)      the picture point of a place: X cm across from the lens's line (right +), Y cm up, D cm away
    foot(X, D)      the same on the ground;  G(x, y) the place on the ground (X, D) under a picture point
    H_(a, b)        a place in the hall's own measure: a cm along its front from the south-west corner, b cm in

LIGHT. Two states, the same geometry. GOLD (back.png and the plain cut-outs): the late afternoon sun from the left and
behind us (38 degrees behind the left, 30 up): the hall's west side full in it, its front at a slant, shadows to the right
and away, the old pine's shade across the near ground. SUNSET (sunset.png and every cut-out's -sunset twin): the sun low
at the left, a little beyond us (15 degrees beyond the left, 6 up), going down behind the trees of the mountain's foot:
the west side red, the front in blue shade, the terrace in the trees' long shadow with streaks of red light across it
toward the right and toward us; the sky's glow red and orange low at the left through the trunks (the act's licence for
chrome orange and geranium lake), the east over the plain in the evening's blue and rose."""

import math

import numpy as np

W, H = 800, 600
SHAPE = (H, W)
ID = "edo-shosha"
OUT = "out/edo-shosha"

# ---------------------------------------------------------------- the camera
HZ, FULL = 330, 560          # the scene's `horizon` and `full`
F = 700.0                    # the lens, px
CX = 400.0                   # where lines running straight away meet
S0 = 160.0 / 175.0           # px per cm at the row `full`
EYE = (FULL - HZ) / S0       # 251.6 cm: the eye above the terrace


def P(X, Y, D):
    k = F / D
    return (CX + X * k, HZ + (EYE - Y) * k)


def foot(X, D, h=0.0):
    return P(X, h, D)


def k_at(D):
    """Picture px per cm at a depth."""
    return F / D


def D_row(y):
    """The depth of the ground at a picture row below the horizon."""
    return EYE * F / max(y - HZ, 0.25)


def G(x, y):
    """The place on the ground (X, D) under a picture point."""
    D = D_row(y)
    return ((x - CX) * D / F, D)


def scale_at(y):
    return (y - HZ) / (FULL - HZ)


def grownup_px(y):
    return 160.0 * scale_at(y)


def r2(p):
    return [int(round(p[0])), int(round(p[1]))]


def ground_grid(shape=SHAPE):
    """For every pixel below the horizon, the place on the ground it shows: (X, D, mask)."""
    y, x = np.mgrid[0:shape[0], 0:shape[1]].astype(np.float32)
    below = y > HZ + 0.5
    D = EYE * F / np.maximum(y + 0.5 - HZ, 0.5)
    X = (x + 0.5 - CX) * D / F
    return X.astype(np.float32), D.astype(np.float32), below.astype(np.float32)


# ---------------------------------------------------------------- the hall: square to the compass, so turned in our view
PHI = math.radians(26.0)
UX, UD = math.cos(PHI), math.sin(PHI)            # along the front, west to east (away to the right)
VX, VD = -math.sin(PHI), math.cos(PHI)           # into the hall, south to north (away to the left)
FL = (66.0, 1110.0)                              # the south-west corner of the walls (X, D)
SIDE = 360.0                                     # the walls: two ken square
BASE_H = 45.0                                    # the stone base
BASE_OUT = 34.0                                  # how far the base stands out from the walls
EAVE_Y = 300.0                                   # the wall plate (the walls' top), above the terrace
EAVE_OUT = 124.0                                 # the deep eaves
EAVE_DROP = 14.0                                 # the eave's edge a little below the wall plate's height, the roof's lip
APEX_Y = 585.0                                   # the roof's peak
DOOR_A = (98.0, 262.0)                           # the double doors along the front (a)
DOOR_Y = (BASE_H + 8.0, 252.0)                   # the doorway: sill and lintel above the terrace
LATTICE_B = (126.0, 234.0)                       # the west lattice along the side (b)
LATTICE_Y = (112.0, 206.0)                       # its sill and head above the terrace (Ryokai's face at it)
STEP = dict(a0=70.0, a1=290.0, out=74.0, h=22.0)  # the broad dressed stone before the doors (from the base's front)
LOCK_AT = (180.0, 150.0)                         # the lock on the hasp: at the doors' meeting (a), its height (Y)
LOCK_W, LOCK_H = 34.0, 19.0                      # the lock's carved block (cm): the rabbit on its waves (a shipwright's lock: big)


def H_(a, b):
    """A place in the hall's own measure -> (X, D)."""
    return (FL[0] + a * UX + b * VX, FL[1] + a * UD + b * VD)


def HP(a, b, y):
    X, D = H_(a, b)
    return P(X, y, D)


def hfoot(a, b):
    return HP(a, b, 0.0)


N_FRONT = (math.sin(PHI), 0.0, -math.cos(PHI))   # the doors face south: toward us and a little right
N_WEST = (-math.cos(PHI), 0.0, -math.sin(PHI))   # the lattice faces west: left and a little toward us

# ---------------------------------------------------------------- the two lights
SUN = {
    # toward the sun: (across: negative is left, up, depth: negative is toward us)
    "gold": (-0.788 * 0.866, 0.50, -0.616 * 0.866),          # 38 degrees behind the left, 30 up
    "sunset": (-0.966 * 0.995, 0.105, 0.259 * 0.995),        # 15 degrees beyond the left, 6 up
}


def unit(v):
    n = math.sqrt(sum(c * c for c in v))
    return tuple(c / n for c in v)


def cast_of(light):
    """A shadow on the ground per cm of height: (across, away)."""
    sx, sy, sd = unit(SUN[light])
    return (-sx / sy, -sd / sy)


def lit_of(light, normal):
    s = unit(SUN[light])
    n = unit(normal)
    return max(0.0, s[0] * n[0] + s[1] * n[1] + s[2] * n[2])


def shadow_pt(light, X, Y, D):
    """Where the shadow of a point falls on the ground: (X, D)."""
    cx, cd = cast_of(light)
    return (X + cx * Y, D + cd * Y)


# ---------------------------------------------------------------- the place round the hall (X, D in cm; heights Y)
# The east path: its steps climb from the terrace to the north-west, steeply, into the trees. Its centre line from the
# front edge of the bottom step, and its width.
PATH_FOOT = (-404.0, 1268.0)
PATH_DIR = (0.33, 0.944)                        # up the path, in plan: away and a little to the left
PATH_W = 150.0
PATH_RISE = 16.0                                 # each step's riser (worn, set by hand)
PATH_TREAD = 36.0
PATH_N = 26                                      # how many steps there are before the trees take it
STONE = (-276.0, 1214.0)                         # the small stone, right of the path's foot (toward the hall)
STONE_SIZE = (34.0, 108.0, 20.0)                 # its face's width, its height, its thickness
# O-Ume's hut, farther off under the trees, left of the path's foot, square to the compass as the hall is
HUT = dict(sw=(-780.0, 1590.0), w=280.0, d=240.0, wall=182.0, eave=70.0, ridge=345.0)
HUT_LANTERN_AB = (200.0, -14.0, 158.0)          # along its front from its south-west corner, out from it, the hook's height
# The bench where the women wait: by the hall's south-east corner at the terrace's edge, square to the compass (it
# faces south); the plain far below behind them
BENCH = dict(w0=(-164.0, 1066.0), long=160.0, deep=34.0, h=42.0)
COMBS = (-246.0, 986.0)                          # the heap of combs on its cloth, before the bench (X, D)
# The terrace's edge on the right, past the hall's corner: the land drops away to the plain
EDGE = [(260.0, 2700.0), (420.0, 2100.0), (560.0, 1700.0), (740.0, 1520.0), (1000.0, 1420.0), (1400.0, 1380.0)]
# The road up from the town, at the bottom right: its centre line (X, D), up from below the frame to the terrace
ROAD = [(640.0, 560.0), (560.0, 760.0), (470.0, 940.0), (390.0, 1060.0)]
ROAD_W = 240.0
# The near things (the front plane): the old pine at the left edge (its trunk's middle at the foot, its radius)
NEAR_PINE = dict(X=-296.0, D=480.0, r=33.0)
LANTERN = dict(X=-196.0, D=600.0)
# The late cherry, in the shade at the mountain's foot behind the path and the hut
CHERRY = (-560.0, 2250.0)


def bench_pts():
    """The bench's footprint corners (X, D): front-left, front-right, back-right, back-left. It runs west to east (along
    the hall's front, so square to the compass)."""
    x0, d0 = BENCH["w0"]
    L, dp = BENCH["long"], BENCH["deep"]
    fl = (x0, d0)
    fr = (x0 + L * UX, d0 + L * UD)
    br = (fr[0] + dp * VX, fr[1] + dp * VD)
    bl = (x0 + dp * VX, d0 + dp * VD)
    return fl, fr, br, bl


def bench_at(t, out=0.0):
    """A place along the bench's front: t from 0 (west end) to 1 (east end), `out` cm in front of it."""
    x0, d0 = BENCH["w0"]
    L = BENCH["long"]
    return (x0 + t * L * UX - out * VX, d0 + t * L * UD - out * VD)


def hut_at(a, b):
    sx, sd = HUT["sw"]
    return (sx + a * UX + b * VX, sd + a * UD + b * VD)


def path_at(s, across=0.0):
    """A place on the path: s cm up it (in plan) from the bottom step's front edge, `across` cm to the right of its
    middle -> (X, D)."""
    dx, dd = PATH_DIR
    rx, rd = dd, -dx                                       # to the right of the way up
    return (PATH_FOOT[0] + dx * s + rx * across, PATH_FOOT[1] + dd * s + rd * across)


# ---------------------------------------------------------------- where people stand (places on the ground)
MARKS_W = {
    "road": (322.0, 856.0),                       # from the town: up the road at the bottom right
    "stone": (-270.0, 1110.0),                    # before the stone at the path's foot
    "path": path_at(-70.0, -40.0),                     # the foot of the east path (the way up refuses)
    "ryokai": path_at(-12.0, 34.0),               # Ryokai sitting on the bottom step, by the stone
    "hall": H_(180.0, -168.0),                    # before the doors, a step back
    "lock": H_(180.0, -126.0),                    # at the lock, close before the step: the close-up opens from here
    "step": H_(250.0, -126.0),                    # by the step and the rice ball on its leaf
    "ume": H_(-56.0, -70.0),                      # O-Ume, by the hall's south-east corner, between the hall and the bench
    "hut": hut_at(196.0, -92.0),                  # before O-Ume's hut, its lantern on the hook
    "bench": bench_at(0.55, 170.0),               # before the bench where the women wait
    "tome": bench_at(0.16, 42.0),                 # Grandmother Tome, seated on the bench (her feet before it)
    "wife": bench_at(0.50, 42.0),                 # the young wife with her baby, seated
    "girl": bench_at(0.84, 42.0),                 # the girl with her grandmother's slip, seated
    "view": (640.0, 1330.0),                      # at the terrace's edge past the bench: the plain far below, the castle
    "combs": (COMBS[0] - 30.0, COMBS[1] - 84.0),  # before the heap of failed combs and pins
}
FACES = {"road": "W", "stone": "N", "path": "N", "ryokai": "E", "hall": "N", "lock": "N", "step": "N", "ume": "W", "hut": "N",
         "bench": "N", "tome": "S", "wife": "S", "girl": "S", "view": "E", "combs": "N"}
LATTICE_W = H_(-58.0, 180.0)                       # Ryokai at the west lattice, outside, once the hall is open: his face at it
DOORWAY_W = H_(150.0, -40.0)                       # the foot of the open doors (the women go in here, and come out)
HOMEWARD_W = [H_(60.0, -260.0), (420.0, 760.0), (700.0, 560.0)]    # the young wife and the girl, home down the road (off the frame)
TALK_W = {"ryokai": (-285.0, 1122.0), "ume": H_(30.0, -150.0), "tome": bench_at(0.16, 112.0), "wife": bench_at(0.50, 112.0),
          "girl": (-14.0, 989.0), "hall": H_(180.0, -150.0)}
ARRIVE_W = {"road": [(236.0, 826.0), (406.0, 826.0)], "lock": [H_(130.0, -142.0), H_(236.0, -152.0)],
            "hall": [H_(120.0, -172.0), H_(246.0, -186.0)]}
EDGE_E_W = (560.0, 760.0)                          # the way back to the town: walk to here (the bottom right)
LATTICE_TALK_W = (-126.0, 1258.0)                  # talking to Ryokai at the lattice: from beside him, clear of the bench
NIGHT_UME_W = H_(116.0, -130.0)                     # Mind The Fire: O-Ume outside the hall with her lantern (edo-night.js)


def walk_outline():
    """The ground people may stand on, as picture points: the terrace from the bottom of the picture (clear of the old
    pine's roots) up to the hall's base and its step, along the base's west side to the lattice, round to the path's
    foot (never up it), along the hut's front; at the right up to the terrace's edge over the plain."""
    bo = BASE_OUT
    st = STEP
    r_ = lambda p: (round(p[0], 1), round(p[1], 1))
    base_se = hfoot(SIDE + bo + 10, -bo - 12)
    step_r = hfoot(st["a1"] + 8, -bo - st["out"] - 12)
    step_l = hfoot(st["a0"] - 8, -bo - st["out"] - 12)
    base_sw = hfoot(-bo - 14, -bo - 12)
    west_n = hfoot(-bo - 16, 250.0)
    edge_r = foot(*EDGE[3])
    pf_r = foot(*path_at(-3.0, PATH_W / 2 + 26))
    pf_l = foot(*path_at(-3.0, -PATH_W / 2 - 20))
    hut_r = foot(*hut_at(HUT["w"], -40.0))
    hut_l = foot(*hut_at(20.0, -46.0))
    bank_r = foot(*path_at(-3.0, -PATH_W / 2 - 60))                       # (the bank's flank between the path and the hut: its foot)
    bank_m = foot(-478.0, 1560.0)
    pts = [(78.0, 598.0), (794.0, 598.0), (794.0, edge_r[1] + 6), (edge_r[0], edge_r[1] + 6), (base_se[0] + 30, base_se[1] - 2), base_se, step_r, step_l,
           base_sw, west_n, (west_n[0] - 40, west_n[1] - 1), pf_r, pf_l, bank_r, bank_m, hut_r, hut_l, (60.0, hut_l[1] + 10), (60.0, 520.0)]
    return [r_(p) for p in pts]


def mark(name):
    return r2(foot(*MARKS_W[name]))


def sizes():
    return {k: round(grownup_px(foot(*v)[1]), 1) for k, v in MARKS_W.items()}


if __name__ == "__main__":
    print(f"eye {EYE:.1f} cm; the hall's corner {FL} at row {foot(*FL)[1]:.0f}; its vanishing points x {CX + F * UX / UD:.0f} and {CX + F * VX / VD:.0f}")
    for k, v in MARKS_W.items():
        p = foot(*v)
        print(f"  {k:8s} {r2(p)}  D {v[1]:6.0f}  a grown-up {grownup_px(p[1]):5.1f} px")


# ================================================================ the paints, the two lights, the watercolour's tools
# (the act's watercolour, as Yui's: edo_village_kit's Wet, thin, glaze, hand, grade_cut, painted; the key line and the
# ground's noise are this scene's own, for its own camera)
from brush import F32, blur, grid, lerp, noise, rgb, sample, step, tint, glow as _glow
from edo_village_kit import (P as paint, mixp, tintw, WHITE, NAPLES, CERULEAN, COBALT, ULTRA, PRUSSIAN, OCHRE, SIENNA, VERONESE,
                             VIRIDIAN, LAKE, VERMILION, Wet, thin, hand, grade_cut, painted, resample, WPAPER)
ORANGE, VIOLET, LILAC, DEEPV, CHROME = paint("chrome-orange"), paint("cobalt-violet"), paint("lilac"), paint("deep-violet"), paint("chrome-yellow")

LIGHT = "gold"


def set_light(name):
    global LIGHT
    LIGHT = name


# how a local colour is seen in each light: lit (multiply, then the sun's own light added), and in shade (a glaze)
_LIT_MUL = {"gold": np.array([1.0, 0.975, 0.90], F32), "sunset": np.array([0.97, 0.80, 0.70], F32)}
_LIT_ADD = {"gold": np.array([0.15, 0.115, 0.035], F32), "sunset": np.array([0.58, 0.25, 0.07], F32)}
_SHADE = {"gold": np.array([0.58, 0.64, 0.82], F32), "sunset": np.array([0.40, 0.42, 0.70], F32)}
_HALF = {"gold": np.array([0.84, 0.85, 0.90], F32), "sunset": np.array([0.62, 0.56, 0.70], F32)}


def col(c):
    return rgb(c) if isinstance(c, str) else np.asarray(c, dtype=F32)


def sunlit(c, t=1.0):
    """A local colour in the light's sun, `t` how squarely (0..1)."""
    c = col(c)
    m = c * _LIT_MUL[LIGHT]
    return np.clip(1 - (1 - m) * (1 - _LIT_ADD[LIGHT] * float(t)), 0, 1).astype(F32)


def shaded(c, k=1.0):
    """A local colour in shade: a cool glaze over it (`k` how deep)."""
    c = col(c)
    return np.clip(c * lerp(np.ones(3, F32), _SHADE[LIGHT], k), 0, 1).astype(F32)


def faced(c, t):
    """A local colour on a face that takes the sun by `t` (-1..1: below 0 it is turned away, in shade)."""
    t = float(t)
    if t <= 0:
        return shaded(c, 1.0)
    half = col(c) * _HALF[LIGHT]
    if t < 0.3:
        return lerp(shaded(c, 1.0), half, t / 0.3).astype(F32)
    return lerp(half, sunlit(c, 1.0), min(1.0, (t - 0.3) / 0.55)).astype(F32)


def face_t(normal):
    """How squarely a face with this outward normal (X, Y, D) takes the light's sun: -1..1."""
    s = unit(SUN[LIGHT])
    n = unit(normal)
    return s[0] * n[0] + s[1] * n[1] + s[2] * n[2]


def SHADE_GLAZE():
    """The glaze a cast shadow lays over the ground in this light (multiply)."""
    return _SHADE[LIGHT]


def SUNC():
    """The colour of the sun's light itself (for rims and glows)."""
    return np.clip(_LIT_ADD[LIGHT] * 1.6 + np.array([0.3, 0.3, 0.25], F32) * (LIGHT == "gold"), 0, 1).astype(F32)


# ---------------------------------------------------------------- the air, by distance: toward the sky's colour at the horizon
def horizon_c():
    """The sky's colour at the horizon, which far things go toward (not grey)."""
    if LIGHT == "gold":
        return lerp(WPAPER, lerp(NAPLES, CERULEAN, 0.35), 0.16).astype(F32)
    return lerp(lerp(WPAPER, LAKE, 0.22), VIOLET, 0.16).astype(F32)


def air_t(D, start=1600.0, scale=40000.0, most=0.92):
    return float(np.clip(most * (1.0 - math.exp(-max(D - start, 0.0) / scale)), 0, most))


def aired(c, D, start=1600.0, scale=40000.0, most=0.92):
    """A colour seen D cm off: toward the horizon's colour, more the farther."""
    return lerp(col(c), horizon_c(), air_t(D, start, scale, most)).astype(F32)


# ---------------------------------------------------------------- the key line, quieter (DEPTH.md), for this camera
def keyline(layer, pts, row=None, lit=False, seed=0, weight=1.0, color=None, alpha=None):
    """Thinner than the print's, a little broken, lost on the lit side of a thing (`lit`) and in the distance (above the
    row HZ + 26: no line at all)."""
    if lit or len(pts) < 2:
        return layer
    r = row if row is not None else max(p[1] for p in pts)
    if r < HZ + 26:
        return layer
    t = float(np.clip((r - HZ) / (FULL - HZ), 0, 1))
    w = (0.35 + 0.45 * t) * weight
    a = alpha if alpha is not None else 0.22 + 0.34 * t
    c = PRUSSIAN if color is None else color
    rng = np.random.default_rng(int(seed * 7919 + pts[0][0] * 13 + pts[0][1] * 31) & 0x7FFFFFFF)
    q = resample(pts, 3.0)
    i = 0
    while i < len(q) - 1:
        n = int(rng.uniform(4, 13))
        layer.line(q[i:i + n + 1], c, w * rng.uniform(0.8, 1.15), a * rng.uniform(0.55, 1.0))
        i += n + (int(rng.uniform(1, 3)) if rng.random() < 0.55 else 0)
    return layer


# ---------------------------------------------------------------- noise that lies on the ground, by place (cm)
_GTILES = {}


def world_noise(X, D, cell, seed, octaves=3):
    """Noise sampled by the place on the ground (X, D in cm), blotches `cell` cm across (or (across, along)): big near
    us, small and flattened far off; it fades to 0.5 where a blotch would be smaller than a pixel."""
    size = 1024
    tile = _GTILES.get((seed, octaves))
    if tile is None:
        tile = _GTILES[(seed, octaves)] = noise((size, size), 64, seed, octaves)
    cu, cv = (cell, cell) if np.isscalar(cell) else cell

    def fold(t):
        m = np.mod(t, 2 * (size - 2))
        return np.where(m > size - 2, 2 * (size - 2) - m, m)
    n = sample(tile, fold(X / cu * 64 + 300), fold(D / cv * 64 + 300))
    k = F / np.maximum(D, 50.0)
    small = np.minimum(cu * k, cv * k * k * EYE / F)
    fade = np.clip((small - 1.0) / 2.5, 0, 1)
    return (0.5 + (n - 0.5) * fade).astype(F32)


def glaze(picture, mask, color=None, amount=1.0):
    """A shadow as a glaze: the picture multiplied toward this light's shade through a mask."""
    return tint(picture, SHADE_GLAZE() if color is None else col(color), np.clip(mask * amount, 0, 1).astype(F32))

"""PAINT-21F: edo-hall, inside the women's hall at the foot of Mount Shosha at sunset, about 29 April 1830 (S/briefs/out/
edo2-design.md, section 5 and puzzle #38), in the act's manner (S/work-20-paintA/style.md: flats, one prussian contour round
the silhouettes, the blue leading; the sunset's chrome orange and geranium lake in the SKY seen through the lattice, and in
the light, which is not painted in the backdrop).

    python3 edo_hall.py fast     the under-painting with the contours and the light laid on, no brush pass (seconds)
    python3 edo_hall.py          everything: out/edo-hall/ (back, the cut-outs, the dusk state, the three light pictures,
                                 layout.json), and out/edo-hall-work/ (the composed pictures to look at)

THE HALL (cm; X across from the west wall, Y up, Z out from the north wall toward us): 630 wide (3.5 ken) and 450 deep
(2.5 ken), a board ceiling at 300 on battens and two cross beams. The double doors are in the SOUTH wall, BEHIND THE LENS:
the camera stands just outside the open doors, and the south wall is cut away (the way out is the bottom edge of the
picture; the evening outside lies on the floor near us as a step of paler light). The WEST wall (left) has the LATTICE
window in its north bay; the NORTH wall (back) has the altar bay in its middle with the small CABINET (doors shut: the
Kannon inside is not shown and not named) on its stand, and before the cabinet the lamp, the incense burner and the
flowers in a jar (two weeks shut in: the flowers have drooped); the EAST wall (right) is plain plaster between posts: the
light lands there, and so does the HUM. Mats (twelve tatami) on the floor, boards round them, two straw cushions before
the altar, a low desk near us at the left where women write their slips. SLIPS everywhere, paper and thin wood, old and
new, pasted on the posts, the rails, the walls round the altar and the beams overhead: hundreds (never copper).

ONE CAMERA (room.View): horizon 200, full 410 (the lens 230 cm up), standing at X 330, Z 640 (outside the south wall,
which is cut away), turned 4 degrees to the right, focal 400. Both side walls are seen at about 30 degrees, so the lattice
reads at the left and the east wall at the right; the back wall and the cabinet in the middle.

THE SUN, which is the puzzle's light: low in the WNW, shining through the lattice almost straight across the hall (the
hall's west side faces the sunset: the light runs 2.5 degrees south of due east across it). THE LIGHT IS NOT IN THE
BACKDROP. It is three RGBA pictures for the live layer (screen blend), keyed as frames, and the scene moves them as the sun
goes down (a number k, 0 at the scene's start with the sun 10 degrees up, 1 with it 2 degrees up): `bars-wall.png` (the
bars on the east wall: slid straight UP as the sun sinks, clipped to the wall: they climb), `bars-floor.png` (the bars
across the floor: slid east toward the wall, clipped to the floor, gone by k 0.44), `bars-air.png` (the faint shafts in
the dusty air: no slide, a fade). The numbers are in layout.json `bars`.

PAINT-21F."""

import json
import math
import os
import sys
import time

import numpy as np

from brush import F32, lerp, noise, blur, mask_poly, mask_ellipse, mask_line, Sheet, over, vary
from room import View
from edo_keep_kit import (Room, Passes, boards, panels, box, finish_scene, save_rgba, to_image, ipt, col, stand_in,
                          shade_of, dark_of, tint_of, boundary, _hull, W, H, SHAPE, P, PAPER, NAPLES, OCHRE, SIENNA, PRUSSIAN,
                          COBALT, ULTRA, CERULEAN, SHADE)

ID = "edo-hall"
OUT = "out/edo-hall"
WORK = "out/edo-hall-work"
VIEW = dict(horizon=200, full=410, cam=(330.0, 640.0), yaw=4.0, focal=400.0)
V = View(**VIEW)
RW, RD, RH = 630.0, 450.0, 300.0                      # the hall: west to east, north to south (the south wall, cut away), the ceiling
ZFAR = 760.0                                          # how far the side walls, the ceiling and the floor run toward us (past the frame)
POST = 15.0                                           # posts are 15 cm square
NAGESHI = (185.0, 197.0)                              # the rail round the walls
HEAD = (282.0, 300.0)                                 # the head beam under the ceiling
SILL = 14.0                                           # the sill board along the foot of each wall
N_POSTS = [0.0, 207.5, 407.5, RW - POST]              # the north wall's posts (left faces, X): three bays; the altar in the middle one
SIDE_POSTS = [0.0, 270.0, 450.0 - POST]               # the side walls' posts (north faces, Z): the lattice in the west wall's north bay
LATTICE = (70.0, 240.0, 72.0, 176.0)                  # the window in the west wall: Z0, Z1, Y0 (sill), Y1 (head)
FRAME = 6.0                                           # its frame
SLATS = 6                                             # vertical slats, each SLAT_W wide and SLAT_D deep (gaps between)
SLAT_W, SLAT_D = 7.0, 5.0
STAND = (255.0, 375.0, 0.0, 62.0, 0.0, 62.0)          # the altar stand: X0, X1, Y0, Y1, Z0, Z1
CABINET = (286.0, 344.0, 62.0, 146.0, 8.0, 48.0)      # the cabinet (zushi), doors shut; its roof above
DESK = (96.0, 208.0, 0.0, 30.0, 392.0, 436.0)         # the women's writing desk, near us at the left (the front plane)
CUSHIONS = [(262.0, 118.0), (368.0, 118.0)]           # two round straw cushions before the altar (X, Z of their middles)

# THE SUN. el falls from 10 degrees (k 0, the scene's start) to 2 degrees (k 1); the light runs east, 2.5 degrees south.
EL0, EL1, AZ = 10.0, 2.0, 2.5
T0, T1 = math.tan(math.radians(EL0)), math.tan(math.radians(EL1))
RUN = RW / math.cos(math.radians(AZ))                 # the light's horizontal run from the lattice to the east wall
DRIFT = RW * math.tan(math.radians(AZ))               # how far south it drifts on the way across

# THE HUM: on the east wall, a hand's height up, in the middle of one bar of light (layout.json `hum`, `door`)
HUM_Y = 105.0
WAINSCOT = 40.0                                       # the east wall's boards at its foot

# where people stand (X, Z), facing
MARKS = {
    # (the lens sees the east wall from the south-west: anyone standing by that wall north of the line from the lens to
    # the hum hides it; so the marks by the hum are south of that line, or low: a person sitting is looked over)
    "door": ((330.0, 285.0), "N"),                    # arriving: just in from the open doors (the bottom edge)
    "ume": ((150.0, 270.0), "NE"),                    # O-Ume kneeling by the door (the front left, by the women's desk), watching the hum
    "mats": ((300.0, 205.0), "N"),                    # on the mats, in the middle
    "cabinet": ((315.0, 112.0), "N"),                 # before the cabinet
    "lattice": ((62.0, 160.0), "W"),                  # by the west lattice
    "hum": ((612.0, 302.0), "N"),                     # beside the hum, against the east wall, just south of it: it stays in sight
    "humsit": ((590.0, 222.0), "E"),                  # Mom sitting down right before it ("Mom has to sit down"): looked over, it stays in sight
    "big": ((480.0, 285.0), "NE"),                    # Big Sister, near, watching (in front of the corner, clear of the light)
    "lil": ((600.0, 302.0), "N"),                     # Little Sister with the flashlight on the hum: by the wall south of it, beside Mom sitting (Mom's standing spot, free while she sits)
    "mid": ((360.0, 250.0), "S"),
}
RYOKAI = (-42.0, 150.0)
WALK_FRONT = 290.0                                    # the walk's front edge (Z): about 50 rows below `full`                               # Ryōkai OUTSIDE the west wall at the lattice (his feet): his face shows in its gaps

# ---------------------------------------------------------------- the act's paints, by name (style.md section 2)
GERANIUM = P("geranium-lake")
ORANGE = P("chrome-orange")
VIRIDIAN = P("viridian")
VERONESE = P("veronese-green")
VERMILION = P("vermilion")
PLASTER = lerp(lerp(PAPER, NAPLES, 0.22), GERANIUM, 0.04)              # aged lime plaster, a little rose
DUSKY = lerp(SHADE, SIENNA, 0.30)                                      # the hall's own dimness: the blue shade warmed by the wood
PL_N = lerp(lerp(PLASTER, SIENNA, 0.08), DUSKY, 0.60)                  # the north wall's plaster above the rail
PL_E = lerp(lerp(PLASTER, SIENNA, 0.08), DUSKY, 0.56)                  # the east wall: the palest wall, where the light lands
PL_W = lerp(lerp(PLASTER, SIENNA, 0.08), DUSKY, 0.70)                  # the inside of the west wall, its back to the sun
WOOD = lerp(SIENNA, PRUSSIAN, 0.46)
WOOD_D = lerp(SIENNA, PRUSSIAN, 0.66)
BOARD = lerp(lerp(SIENNA, OCHRE, 0.12), PRUSSIAN, 0.55)                # the walls' boards below the rail
CEIL = lerp(SIENNA, PRUSSIAN, 0.68)
CEIL_D = lerp(SIENNA, PRUSSIAN, 0.84)
FLOOR = lerp(lerp(SIENNA, OCHRE, 0.22), PRUSSIAN, 0.55)
TATAMI = lerp(lerp(lerp(OCHRE, PAPER, 0.30), VERONESE, 0.14), DUSKY, 0.52)
HERI = lerp(PRUSSIAN, SIENNA, 0.22)
LACQUER = lerp(PRUSSIAN, SIENNA, 0.22)
GILT = lerp(NAPLES, OCHRE, 0.45)
BRONZE = lerp(lerp(OCHRE, SIENNA, 0.5), PRUSSIAN, 0.22)
JAR = lerp(lerp(CERULEAN, PAPER, 0.45), SHADE, 0.32)
LEAF = lerp(VIRIDIAN, PRUSSIAN, 0.25)
BLOSSOM = lerp(lerp(PAPER, GERANIUM, 0.10), SHADE, 0.12)
STRAW = lerp(lerp(OCHRE, SIENNA, 0.25), DUSKY, 0.42)
INK = lerp(PRUSSIAN, SIENNA, 0.15)
SLIP_TONES = [lerp(PAPER, NAPLES, 0.06), lerp(PAPER, OCHRE, 0.22), lerp(PAPER, OCHRE, 0.38), lerp(OCHRE, SIENNA, 0.22),
              lerp(OCHRE, PAPER, 0.42)]                                 # new paper, old, older, brown with age, thin wood
EVENING = lerp(lerp(PAPER, NAPLES, 0.35), GERANIUM, 0.06)               # the evening at the open doors behind us
SUN = lerp(ORANGE, GERANIUM, 0.40)                                     # the light: red-orange (keyed as a light, never a wall)
SUN_HOT = lerp(SUN, NAPLES, 0.45)


# ---------------------------------------------------------------- geometry helpers
def wquad(wall, u0, u1, v0, v1, off=0.0):
    """A rectangle on a wall as room points. wall: "N" (Z = 0, u = X), "W" (X = 0, u = Z), "E" (X = RW, u = Z); `off` cm out
    from the wall into the room."""
    if wall == "N":
        return [(u0, v0, off), (u1, v0, off), (u1, v1, off), (u0, v1, off)]
    x = off if wall == "W" else RW - off
    return [(x, v0, u0), (x, v0, u1), (x, v1, u1), (x, v1, u0)]


def gaps():
    """The lattice's gaps (Z0, Z1) between its frame and its slats, north to south."""
    z0, z1 = LATTICE[0] + FRAME, LATTICE[1] - FRAME
    g = (z1 - z0 - SLATS * SLAT_W) / (SLATS + 1)
    out, z = [], z0
    for i in range(SLATS + 1):
        out.append((z, z + g))
        z += g + SLAT_W
    return out


def t_of(k):
    """The sun's height (as its tangent) at k: linear in the tangent, so the bars climb the wall at an even pace."""
    return T0 + (T1 - T0) * k


def wall_band(k):
    """The band of light on the east wall at k: (Y bottom, Y top) in cm (the bottom may be under the floor: hidden). The
    light comes through the window's opening inside its frame."""
    t = t_of(k)
    return LATTICE[2] + FRAME - RUN * t, LATTICE[3] - FRAME - RUN * t


def floor_from(k):
    """Where the light on the floor begins at k (X of its west end); RW or more: none on the floor."""
    return (LATTICE[2] + FRAME) * math.cos(math.radians(AZ)) / t_of(k)


def k_for_wall_top(y):
    """The k at which the band's top reaches height y on the east wall."""
    t = (LATTICE[3] - FRAME - y) / RUN
    return (T0 - t) / (T0 - T1)


K_HUM = k_for_wall_top(HUM_Y + 4.0)                   # the bar's top a little past the hum: the door can open
K_FLOOR = (T0 - (LATTICE[2] + FRAME) * math.cos(math.radians(AZ)) / RW) / (T0 - T1)       # the floor's bars gone


def hum_z():
    """The hum's Z on the east wall: the middle of the second bar of light from the band's south end (people can stand
    south of it, out of the line of sight; and it is 40 cm clear of the middle post, room for a hand-sized door)."""
    mids = sorted((a + b) / 2 + DRIFT for a, b in gaps())
    return mids[-2]


HUM = (RW, HUM_Y, hum_z())


def wall_px_per_cm(Z):
    """Picture pixels per cm, up the east wall, at Z (its depth from the lens)."""
    return V.F / V.depth(RW, Z)


# ---------------------------------------------------------------- a lean room
class HallRoom(Room):
    """The kit's Room, keeping each thing's fill as booleans and its line as bytes (a few hundred things in this hall:
    float frames for each would be gigabytes). Paints exactly as the kit's."""

    def thing(self, m, alpha=0.85, color=None, line=None):
        ln = boundary(m) if line is None else line
        self.things.append((np.asarray(m) >= 0.5, _pack(ln), PRUSSIAN if color is None else col(color), alpha))

    def lines(self, m_fill, m_line, alpha=0.3, color=None):
        self.things.append((np.asarray(m_fill) >= 0.5, _pack(m_line), PRUSSIAN if color is None else col(color), alpha))

    def contours(self, pic):
        cover = np.zeros(SHAPE, bool)
        out = pic.copy()
        layers = []
        for fill, line, color, alpha in reversed(self.things):
            if line is not None:
                vis = (line.astype(F32) / 255.0) * (~cover)
                layers.append((vis, color, alpha))
            cover |= fill
        for vis, color, alpha in reversed(layers):
            over(out, color, vis * alpha)
        return out


def _pack(m):
    m = np.clip(np.asarray(m, F32), 0, 1)
    if not m.any():
        return None
    return np.round(m * 255).astype(np.uint8)


# ---------------------------------------------------------------- details laid crisply after the brush pass
class Details:
    """Small crisp things (the slips, their writing, rims of light) drawn on sheets and laid after the brush pass, each
    sheet only where its surface is still seen (covered by every thing registered after it: nearer things)."""

    def __init__(self, R):
        self.R = R
        self.layers = []                              # (index into R.things, colour, alpha)

    def sheet(self):
        return Sheet(SHAPE, ss=3)

    def add(self, sh, keep=None):
        c, a = sh.done()
        if keep is not None:
            a = a * keep
        self.layers.append((len(self.R.things), c, a))
        return a

    def lay(self, pic):
        R = self.R
        fills = [f for f, _, _, _ in R.things]
        wanted = {L[0] for L in self.layers}
        cover_after = {}
        cov = np.zeros(SHAPE, bool)
        if len(fills) in wanted:
            cover_after[len(fills)] = cov.copy()
        for i in range(len(fills) - 1, -1, -1):
            cov |= np.asarray(fills[i], bool)
            if i in wanted:
                cover_after[i] = cov.copy()
        out = pic.copy()
        for idx, c, a in self.layers:
            cv = cover_after.get(idx, np.zeros(SHAPE, bool)).astype(F32)
            over(out, c, a * (1 - cv))
        return out


def slip_poly(wall, u, v, w, h, off=0.4):
    return V.poly(wquad(wall, u, u + w, v, v + h, off))


def paste_slips(D, R, wall, spots, seed, dim=0.3, under=True, alpha=0.95):
    """Slips pasted on a wall (or a post's face): each spot (u, v, w, h) in cm. Paper or thin wood, old and new, a little
    askew; on each, a few strokes of writing that are a pattern, not letters (the pilgrimage's name down the middle, the
    province, the name and the date at the sides). Laid in the under-painting too (so the brush knows them), and crisply
    after it."""
    rs = np.random.RandomState(seed)
    sh = D.sheet()
    under_sh = Sheet(SHAPE, ss=2) if under else None
    for (u, v, w, h) in spots:
        tone = SLIP_TONES[rs.choice(len(SLIP_TONES), p=[0.22, 0.30, 0.22, 0.10, 0.16])]
        c = lerp(tone, SHADE, dim * (0.6 + 0.4 * rs.rand()))
        tilt = rs.uniform(-2.0, 2.0)
        pts = wquad(wall, u, u + w, v, v + h, 0.4)
        # a little askew: shear the top edge sideways by `tilt` cm
        if wall == "N":
            pts = [(pts[0][0], pts[0][1], pts[0][2]), (pts[1][0], pts[1][1], pts[1][2]), (pts[2][0] + tilt, pts[2][1], pts[2][2]), (pts[3][0] + tilt, pts[3][1], pts[3][2])]
        else:
            pts = [pts[0], pts[1], (pts[2][0], pts[2][1], pts[2][2] + tilt), (pts[3][0], pts[3][1], pts[3][2] + tilt)]
        pp = V.poly(pts)
        if len(pp) < 3:
            continue
        sh.poly(pp, c, alpha)
        if under_sh is not None:
            under_sh.poly(pp, c)
        # its shadow edge (below and away from the doors' light): a hair of the wall's shade
        sh.line([pp[0], pp[1]], lerp(c, PRUSSIAN, 0.45), 0.6, 0.55)
        # the writing: strokes down the slip (in its own cm, through the camera)
        ink = lerp(INK, c, 0.18 + 0.2 * rs.rand())
        top = v + h * (0.84 - 0.06 * rs.rand())
        bot = v + h * (0.16 + 0.22 * rs.rand())
        a3 = wquad(wall, u + w * 0.5, u + w * 0.5, bot, top, 0.6)
        ln = V.line(a3[0], a3[2])
        if ln:
            sh.line([ln[0], ln[1]], ink, 0.9, 0.85)                       # the pilgrimage's name down the middle
        if w > 5.5 and rs.rand() < 0.7:
            for cx in (0.2, 0.8):                                         # the province, the name, the date: small, at the sides
                b3 = wquad(wall, u + w * cx, u + w * cx, v + h * 0.12, v + h * (0.40 + 0.15 * rs.rand()), 0.6)
                ln = V.line(b3[0], b3[2])
                if ln:
                    sh.line([ln[0], ln[1]], ink, 0.5, 0.45)
    D.add(sh)
    if under_sh is not None:
        c_, a_ = under_sh.done()
        over(R.img, c_, a_ * 0.9)


def scatter(rs, u0, u1, v0, v1, n, w=(6.0, 9.0), h=(16.0, 25.0), rows=None):
    """n slip spots scattered (in rough rows, as pasted by many hands over many years) in a rectangle of a surface."""
    spots = []
    if rows:
        for r in range(rows):
            vv = v1 - (r + 1) * (v1 - v0) / rows
            x = u0 + rs.uniform(0, 4)
            while x < u1 - w[0]:
                ww, hh = rs.uniform(*w), rs.uniform(*h)
                if rs.rand() < 0.86 and x + ww <= u1:
                    spots.append((x, vv + rs.uniform(-2, 2), ww, min(hh, (v1 - v0) / rows - 1)))
                x += ww + rs.uniform(0.6, 4.0)
        return spots
    for _ in range(n):
        ww, hh = rs.uniform(*w), rs.uniform(*h)
        spots.append((rs.uniform(u0, max(u0, u1 - ww)), rs.uniform(v0, max(v0, v1 - hh)), ww, hh))
    return spots


# ---------------------------------------------------------------- the view through the lattice (the far: flats, no contour)
def band_fill(R, m, stops, y0, y1, seed=70):
    n = len(stops)
    for i, c in enumerate(stops):
        ya = y0 + (y1 - y0) * i / n if i else -10
        yb = y0 + (y1 - y0) * (i + 1) / n if i < n - 1 else 610
        band = mask_poly(SHAPE, [(-10, ya), (810, ya), (810, yb), (-10, yb)], soft=3.0 if i else 0.0, wobble=1.5 if i else 0.0, seed=seed + i)
        R.fill(m * band, c, amount=0.02, cell=90)


def view_west(R, m):
    """What the lattice shows, looking out north-west past the hall's side at sunset: the sky in bands (the act's one place
    for chrome orange and geranium lake), the near trees of the mountain's foot as dark flat silhouettes, a pine's trunk."""
    ys = np.nonzero(m.max(axis=1) > 0.5)[0]
    if len(ys) == 0:
        return
    y0, y1 = int(ys.min()), int(ys.max())
    sky = [lerp(GERANIUM, COBALT, 0.45), lerp(GERANIUM, PAPER, 0.25), lerp(lerp(ORANGE, GERANIUM, 0.5), PAPER, 0.15), ORANGE,
           lerp(ORANGE, NAPLES, 0.55), lerp(NAPLES, PAPER, 0.45)]
    band_fill(R, m, sky, y0 - 4, y0 + (y1 - y0) * 0.72, seed=71)
    # the trees at the mountain's foot: a ragged dark line across the lower part, deeper below
    rs = np.random.RandomState(9)
    xs = np.nonzero(m.max(axis=0) > 0.5)[0]
    xa, xb = int(xs.min()) - 4, int(xs.max()) + 4
    top = []
    x = xa
    while x <= xb:
        top.append((x, y0 + (y1 - y0) * (0.62 + 0.12 * rs.rand())))
        x += rs.uniform(3, 7)
    poly = top + [(xb, y1 + 10), (xa, y1 + 10)]
    trees = mask_poly(SHAPE, poly, soft=0.5)
    R.fill(m * trees, lerp(lerp(VIRIDIAN, PRUSSIAN, 0.55), GERANIUM, 0.06), amount=0.03, cell=20)
    near = mask_poly(SHAPE, [(xa, y0 + (y1 - y0) * 0.86), (xb, y0 + (y1 - y0) * 0.80), (xb, y1 + 10), (xa, y1 + 10)], soft=0.5)
    R.fill(m * near, lerp(VIRIDIAN, PRUSSIAN, 0.75), amount=0.03, cell=20)
    # a pine trunk going up through it, dark, toward the north end
    tx = xa + (xb - xa) * 0.72
    trunk = mask_poly(SHAPE, [(tx - 2, y0 - 5), (tx + 1.5, y0 - 5), (tx + 3, y1 + 5), (tx - 2.5, y1 + 5)])
    R.fill(m * trunk, lerp(SIENNA, PRUSSIAN, 0.75), amount=0.02)


# ---------------------------------------------------------------- the hall
def shell(R, D, dusk=False):
    """Floor, walls (the lattice's wall is its own group: a cut-out), ceiling: flats in depth order, far to near."""
    k_dark = 0.22 if dusk else 0.0
    dimc = lambda c: lerp(c, SHADE, k_dark) if dusk else c
    # the window's opening and the view through it (painted first; the lattice's wall and slats are laid over it)
    z0, z1, y0, y1 = LATTICE
    win = mask_poly(SHAPE, V.poly(wquad("W", z0, z1, y0, y1)))
    view_west(R, win)
    if dusk:
        R.shade(win, 0.38, toward=lerp(GERANIUM, PRUSSIAN, 0.55))
    # the north wall (the back): plaster panels between posts on a sill board, the nageshi rail and the head beam
    u, v, okw, fp = R.wall_uv("Z", 0.0)
    back_m = okw * (u >= 0) * (u <= RW) * (v >= 0) * (v <= RH)
    panels(R, back_m, "Z", 0.0, dimc(PL_N), dimc(WOOD), dimc(WOOD_D), RW, RH, post_at=N_POSTS, post_w=POST, sill_h=SILL,
           lintel_h=HEAD[1] - HEAD[0], nageshi=NAGESHI, seed=4, alpha=0.6)
    # below the rail the north wall is boarded, bay by bay (the altar bay a shade darker), the boards' joints drawn
    for i in range(3):
        bx0, bx1 = N_POSTS[i] + POST, N_POSTS[i + 1]
        c = dimc(lerp(BOARD, PRUSSIAN, 0.14) if i == 1 else BOARD)
        boardwall(R, "N", bx0, bx1, SILL, NAGESHI[0], c)
    n_slips = north_slips(R, D, dusk)
    # the side walls: the west (the lattice's wall: its own group, a cut-out), the east (plain: the light lands there)
    ul, vl, okl, fpl = R.wall_uv("X", 0.0)
    left_m = okl * (ul >= 0) * (ul <= ZFAR) * (vl >= 0) * (vl <= RH)
    ur, vr, okr, fpr = R.wall_uv("X", RW)
    right_m = okr * (ur >= 0) * (ur <= ZFAR) * (vr >= 0) * (vr <= RH)
    n0 = len(R.things)
    panels(R, left_m, "X", 0.0, dimc(PL_W), dimc(WOOD_D), dimc(lerp(WOOD_D, PRUSSIAN, 0.2)), ZFAR, RH, post_at=SIDE_POSTS, post_w=POST,
           sill_h=SILL, lintel_h=HEAD[1] - HEAD[0], nageshi=NAGESHI, seed=5, alpha=0.55, cut=win)
    boardwall(R, "W", SIDE_POSTS[0] + POST, SIDE_POSTS[1], SILL, LATTICE[2] - 5, dimc(lerp(BOARD, PRUSSIAN, 0.2)))
    boardwall(R, "W", SIDE_POSTS[1] + POST, ZFAR, SILL, NAGESHI[0], dimc(lerp(BOARD, PRUSSIAN, 0.2)))
    R.add_mask("lattice", left_m * (1 - win))
    n_slips += west_slips(R, D, dusk)
    lattice(R, D, dusk)
    panels(R, right_m, "X", RW, dimc(PL_E), dimc(WOOD), dimc(WOOD_D), ZFAR, RH, post_at=SIDE_POSTS, post_w=POST, sill_h=SILL,
           lintel_h=HEAD[1] - HEAD[0], nageshi=NAGESHI, seed=6, alpha=0.55)
    boardwall(R, "E", SIDE_POSTS[0] + POST, SIDE_POSTS[1], SILL, WAINSCOT, dimc(BOARD))
    boardwall(R, "E", SIDE_POSTS[1] + POST, ZFAR, SILL, WAINSCOT, dimc(BOARD))
    n_slips += east_slips(R, D, dusk)
    # the ceiling: boards on battens running across the hall, two great beams across it (at the north wall, and over the
    # side walls' middle posts), the head beams along the walls
    Xc, Zc, okc, fpc = R.floor_uv(RH)
    ceil_m = okc * (Xc >= -5) * (Xc <= RW + 5) * (Zc >= -5) * (Zc <= ZFAR)
    R.fill(ceil_m, dimc(CEIL), amount=0.03, cell=90)
    R.thing(ceil_m, 0.4)
    for zz in np.arange(22.0, ZFAR, 45.0):                              # battens, across
        mk = R.flat([(0, RH - 0.5, zz), (RW, RH - 0.5, zz), (RW, RH - 0.5, zz + 5), (0, RH - 0.5, zz + 5)], dimc(CEIL_D), amount=0.02)
        R.thing(mk * ceil_m, 0.3)
    for zz in (0.0, SIDE_POSTS[1]):                                     # the beams across (their underside and their face toward us)
        for nm, pp, n in V.box(0, RW, HEAD[0] - 26, HEAD[1], zz, zz + 22):
            c = dimc(WOOD) if nm == "front" else dimc(WOOD_D)
            mk = R.flat2d(pp, c, amount=0.03, cell=60)
            R.thing(mk, 0.6)
        n_slips += beam_slips(R, D, zz + 22.4, 13 + int(zz), 0.55 if not dusk else 0.66)
    # the floor: boards (running across) round the mats; the mats; the evening's paler step near us
    X, Z, okf, fpf = R.floor_uv()
    floor_m = okf * (X >= -5) * (X <= RW + 5) * (Z >= -5) * (Z <= ZFAR)
    boards(R, floor_m, dimc(FLOOR), along="X", width=24.0, offset=4.0, seed=3, line_alpha=0.32)
    mats(R, dimc)
    light = mask_poly(SHAPE, V.poly([(170, 0.3, 300), (480, 0.3, 300), (560, 0.3, ZFAR), (90, 0.3, ZFAR)]), soft=1.0)
    if not dusk:
        R.img[...] = lerp(R.img, lerp(R.img, EVENING[None, None, :], 0.16), (light * floor_m)[..., None])
    return floor_m, back_m, right_m, left_m, ceil_m, win, n_slips


def boardwall(R, wall, u0, u1, v0, v1, c, width=28.0):
    """A wall's boarded part between posts: one flat, upright boards (each its own shade by a hair), the joints drawn."""
    mk = R.flat(wquad(wall, u0, u1, v0, v1, 0.2), c, amount=0.03, cell=(12, 90) if wall == "N" else (90, 12))
    R.thing(mk, 0.5)
    sh = Sheet(SHAPE, ss=2)
    for uu in np.arange(u0 + width, u1 - 4, width):
        q = wquad(wall, uu, uu, v0, v1, 0.3)
        ln = V.line(q[0], q[2])
        if ln:
            sh.line([ln[0], ln[1]], "#ffffff", 0.6)
    R.lines(mk, sh.done()[1] * mk, 0.32)
    return mk


def mats(R, dimc):
    """Twelve tatami (182 x 91, long sides across), each a flat with its grain; the black cloth edges (heri) along the long
    sides; the joints of the short ends drawn."""
    X0, Z0 = 42.0, 75.0
    rs = np.random.RandomState(12)
    for i in range(4):
        for j in range(3):
            x0, z0 = X0 + j * 182, Z0 + i * 91
            c = dimc(lerp(TATAMI, lerp(TATAMI, PAPER, 0.25), rs.uniform(-0.15, 0.25)))
            mk = R.flat([(x0 + 1, 0.4, z0 + 1), (x0 + 181, 0.4, z0 + 1), (x0 + 181, 0.4, z0 + 90), (x0 + 1, 0.4, z0 + 90)], c, amount=0.03, cell=(40, 8))
            R.thing(mk, 0.35)
            for (za, zb) in ((z0, z0 + 3.2), (z0 + 87.8, z0 + 91)):
                R.flat([(x0, 0.6, za), (x0 + 182, 0.6, za), (x0 + 182, 0.6, zb), (x0, 0.6, zb)], dimc(HERI), amount=0.02)
            # the straw's weave: faint lines along the mat's length (one mask for the mat)
            sh = Sheet(SHAPE, ss=2)
            for zz in np.arange(z0 + 8, z0 + 86, 6.0):
                ln = V.line((x0 + 2, 0.5, zz), (x0 + 180, 0.5, zz))
                if ln:
                    sh.line([ln[0], ln[1]], "#ffffff", 0.5)
            R.lines(mk, sh.done()[1] * mk, 0.12)


def lattice(R, D, dusk):
    """The west lattice: its frame and five slats (the inner faces dark against the sunset, their south sides seen), a thin
    rim of the sun along each slat's edge. Group "lattice" (with the west wall: one cut-out)."""
    z0, z1, y0, y1 = LATTICE
    wood = lerp(WOOD_D, PRUSSIAN, 0.18)
    side = lerp(WOOD_D, SIENNA, 0.25)
    if dusk:
        wood, side = lerp(wood, SHADE, 0.2), lerp(side, SHADE, 0.2)
    # the frame: sill, head, two jambs (a little proud of the wall)
    for (a, b, c_, d_) in ((z0, z1, y0 - 5, y0 + FRAME), (z0, z1, y1 - FRAME, y1 + 5), (z0 - 5, z0 + FRAME, y0, y1), (z1 - FRAME, z1 + 5, y0, y1)):
        mk = R.flat(wquad("W", a, b, c_, d_, 1.5), wood, "lattice", amount=0.02)
        R.thing(mk, 0.7)
    # the sill's top face, catching the evening
    mk = R.flat([(1.5, y0 + FRAME, z0), (1.5, y0 + FRAME, z1), (10, y0 + FRAME, z1), (10, y0 + FRAME, z0)], lerp(side, PAPER, 0.15), "lattice", amount=0.02)
    R.thing(mk, 0.5)
    gz = gaps()
    sh = D.sheet()
    for i in range(SLATS):
        za = gz[i][1]
        zb = za + SLAT_W
        # its south side (seen: we look from the south-east), then its inner face over it
        ms = R.flat([(0.5, y0 + FRAME, zb), (SLAT_D + 0.5, y0 + FRAME, zb), (SLAT_D + 0.5, y1 - FRAME, zb), (0.5, y1 - FRAME, zb)], side, "lattice", amount=0.02)
        mf = R.flat(wquad("W", za, zb, y0 + FRAME, y1 - FRAME, SLAT_D + 0.5), wood, "lattice", amount=0.02)
        R.thing(np.maximum(ms, mf), 0.65)
        # the sun's rim on its north edge (the light comes from the west and a little north of it)
        ln = V.line((SLAT_D + 0.6, y0 + FRAME + 2, za), (SLAT_D + 0.6, y1 - FRAME - 2, za))
        if ln and not dusk:
            sh.line([ln[0], ln[1]], lerp(SUN_HOT, PAPER, 0.3), 0.8, 0.8)
    D.add(sh)


def stand_and_cabinet(R, D, dusk=False):
    """The altar stand against the north wall, the small cabinet on it (black lacquer, gilt fittings, doors shut: the Kannon
    inside is not shown), and before it the lamp (an oil lamp on a short stand), the incense burner and the flowers in a jar
    (drooping: the hall was shut two weeks); two round straw cushions on the mats before it."""
    dimc = (lambda c: lerp(c, SHADE, 0.22)) if dusk else (lambda c: c)
    X0, X1, Y0, Y1, Z0, Z1 = STAND
    m = box(R, X0, X1, Y0, Y1, Z0, Z1, dimc(lerp(LACQUER, SIENNA, 0.18)), lit=("top", "front"), shade_k=0.4)
    # its front's two mouldings and a plinth: flats
    for (ya, yb) in ((Y1 - 8, Y1 - 4), (8, 12)):
        mk = R.flat([(X0 + 2, ya, Z1 + 0.5), (X1 - 2, ya, Z1 + 0.5), (X1 - 2, yb, Z1 + 0.5), (X0 + 2, yb, Z1 + 0.5)], dimc(lerp(GILT, LACQUER, 0.55)), amount=0.02)
        R.thing(mk, 0.4)
    # the cabinet
    cx0, cx1, cy0, cy1, cz0, cz1 = CABINET
    box(R, cx0, cx1, cy0, cy1, cz0, cz1, dimc(LACQUER), lit=("front",), shade_k=0.35)
    # its plinth and its roof: a low hipped roof that overhangs, its eaves
    box(R, cx0 - 3, cx1 + 3, cy0, cy0 + 6, cz0 - 2, cz1 + 3, dimc(lerp(LACQUER, SIENNA, 0.2)), lit=("top", "front"), shade_k=0.35)
    rf = R.flat([(cx0 - 9, cy1, cz1 + 9), (cx1 + 9, cy1, cz1 + 9), (cx1 - 6, cy1 + 18, (cz0 + cz1) / 2), (cx0 + 6, cy1 + 18, (cz0 + cz1) / 2)], dimc(lerp(LACQUER, SIENNA, 0.1)), amount=0.02)
    R.thing(rf, 0.75)
    eave = R.flat([(cx0 - 9, cy1 - 3, cz1 + 9), (cx1 + 9, cy1 - 3, cz1 + 9), (cx1 + 9, cy1, cz1 + 9), (cx0 - 9, cy1, cz1 + 9)], dimc(lerp(GILT, LACQUER, 0.5)), amount=0.02)
    R.thing(eave, 0.6)
    # the doors: two leaves meeting in the middle, a frame round each, gilt hinges and a lock-plate where they meet
    mid = (cx0 + cx1) / 2
    sh = D.sheet()
    for (a, b) in ((cx0 + 4, mid - 0.6), (mid + 0.6, cx1 - 4)):
        pp = V.poly([(a, cy0 + 10, cz1 + 0.6), (b, cy0 + 10, cz1 + 0.6), (b, cy1 - 6, cz1 + 0.6), (a, cy1 - 6, cz1 + 0.6)])
        sh.poly(pp, dimc(lerp(LACQUER, PRUSSIAN, 0.2)))
        sh.line(pp + pp[:1], dimc(lerp(GILT, LACQUER, 0.35)), 0.7, 0.8)
        for yy in (cy0 + 22, cy1 - 18):
            q = V.pt(a if a < mid else b, yy, cz1 + 0.8)
            sh.ellipse(q[0], q[1], 1.1, 1.3, dimc(GILT), 0.95)
    q = V.pt(mid, (cy0 + cy1) / 2 + 2, cz1 + 1.0)
    sh.poly([(q[0] - 1.6, q[1] - 2.6), (q[0] + 1.6, q[1] - 2.6), (q[0] + 1.6, q[1] + 2.6), (q[0] - 1.6, q[1] + 2.6)], dimc(GILT), 0.95)
    q = V.pt(mid, cy1 + 19, (cz0 + cz1) / 2)                        # a gilt finial on the roof
    sh.ellipse(q[0], q[1] - 1, 1.5, 2.2, dimc(GILT), 0.9)
    D.add(sh)
    # the incense burner (bronze, three legs, a lid) in the middle, the flowers at the left, the lamp at the right
    ix, iz = (X0 + X1) / 2, Z1 - 12
    box(R, ix - 8, ix + 8, Y1 + 3, Y1 + 13, iz - 6, iz + 6, dimc(BRONZE), lit=("front", "top"), shade_k=0.4)
    box(R, ix - 5, ix + 5, Y1 + 13, Y1 + 17, iz - 4, iz + 4, dimc(lerp(BRONZE, GILT, 0.25)), lit=("top",), shade_k=0.3)
    for dx in (-6, 0, 6):
        box(R, ix + dx - 1, ix + dx + 1, Y1, Y1 + 3, iz + (3 if dx == 0 else -2), iz + (5 if dx == 0 else 0), dimc(BRONZE), lit=("front",))
    fx_, fz = X0 + 22, Z1 - 16                                       # the jar
    box(R, fx_ - 6, fx_ + 6, Y1, Y1 + 18, fz - 6, fz + 6, dimc(JAR), lit=("front", "top"), shade_k=0.35)
    box(R, fx_ - 4, fx_ + 4, Y1 + 18, Y1 + 22, fz - 4, fz + 4, dimc(lerp(JAR, PRUSSIAN, 0.15)), lit=("top",), shade_k=0.3)
    sh = D.sheet()
    rs = np.random.RandomState(31)
    top = V.pt(fx_, Y1 + 22, fz)
    for i in range(7):                                                # sprays, drooping over the jar's lip
        ang = math.radians(-150 + i * 22 + rs.uniform(-6, 6))
        L = rs.uniform(10, 17)
        p1 = (top[0] + math.cos(ang) * L * 0.6, top[1] - abs(math.sin(ang)) * L * 0.9)
        p2 = (p1[0] + math.cos(ang) * L * 0.6, p1[1] + rs.uniform(1, 6))
        sh.line([top, p1, p2], dimc(LEAF), 1.0, 0.95)
        for (px, py) in (p1, p2):
            sh.ellipse(px + rs.uniform(-1, 1), py + rs.uniform(-1, 1), 1.6, 1.2, dimc(LEAF), 0.95)
        if i % 2 == 0:
            sh.ellipse(p2[0], p2[1] + 1, 1.2, 1.0, dimc(BLOSSOM), 0.95)
    for (px, py) in ((top[0] - 8, top[1] + 30), (top[0] + 5, top[1] + 31), (top[0] + 11, top[1] + 29)):    # petals fallen on the stand
        sh.ellipse(px, py, 0.9, 0.6, dimc(BLOSSOM), 0.85)
    D.add(sh)
    lx, lz = X1 - 20, Z1 - 16                                         # the lamp: a short turned stand, a dish of oil, a wick
    box(R, lx - 5, lx + 5, Y1, Y1 + 3, lz - 5, lz + 5, dimc(BRONZE), lit=("top", "front"))
    box(R, lx - 1.2, lx + 1.2, Y1 + 3, Y1 + 30, lz - 1.2, lz + 1.2, dimc(BRONZE), lit=("front",))
    box(R, lx - 6, lx + 6, Y1 + 30, Y1 + 33, lz - 6, lz + 6, dimc(lerp(BRONZE, GILT, 0.3)), lit=("top", "front"), shade_k=0.3)
    # the cushions: round straw mats on the tatami
    for (cx, cz) in CUSHIONS:
        pts = [(cx + 22 * math.cos(a), 0.8, cz + 22 * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 24, endpoint=False)]
        mk = R.flat(pts, dimc(STRAW), amount=0.04, cell=(6, 6))
        R.thing(mk, 0.45)
        R.thing(mk, 0.55)
        sh = Sheet(SHAPE, ss=2)
        for rr in (16.0, 10.0, 4.0):                                      # the coil of straw
            ring = [(cx + rr * math.cos(a), 0.9, cz + rr * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 24, endpoint=False)]
            pp = V.poly(ring)
            sh.line(pp + pp[:1], "#ffffff", 0.6)
        R.lines(mk, sh.done()[1] * mk, 0.35)
    X0_, X1_, Y0_, Y1_, Z0_, Z1_ = STAND
    return m, int(round(V.pt(X0_, 0, Z1_)[1]))


def desk(R, D, dusk=False, grp="front"):
    """Near us at the left (the front plane): a low writing desk where women write their slips: a stack of blank slips, a
    few written, an inkstone, a water dropper, two brushes."""
    dimc = (lambda c: lerp(c, SHADE, 0.22)) if dusk else (lambda c: c)
    X0, X1, Y0, Y1, Z0, Z1 = DESK
    top_c = dimc(lerp(lerp(SIENNA, OCHRE, 0.3), PRUSSIAN, 0.3))
    m = box(R, X0, X1, Y1 - 3, Y1, Z0, Z1, top_c, grp=grp, lit=("top",), shade_k=0.35)
    for (x, z) in ((X0 + 4, Z0 + 4), (X1 - 8, Z0 + 4), (X0 + 4, Z1 - 8), (X1 - 8, Z1 - 8)):
        m = np.maximum(m, box(R, x, x + 4, 0, Y1 - 3, z, z + 4, dimc(WOOD_D), grp=grp, lit=("front",), shade_k=0.3))
    m = np.maximum(m, box(R, X0 + 6, X0 + 36, Y1, Y1 + 5, Z0 + 10, Z1 - 12, dimc(lerp(PAPER, OCHRE, 0.18)), grp=grp, lit=("top",), shade_k=0.3))     # the blank slips
    m = np.maximum(m, box(R, X0 + 48, X0 + 70, Y1, Y1 + 3, Z0 + 12, Z0 + 34, dimc(lerp(PRUSSIAN, SIENNA, 0.1)), grp=grp, lit=("top",), shade_k=0.3))  # the inkstone
    m = np.maximum(m, box(R, X0 + 78, X0 + 84, Y1, Y1 + 4, Z0 + 14, Z0 + 20, dimc(BRONZE), grp=grp, lit=("top", "front")))                         # the dropper
    sh = D.sheet()
    for (a, b) in (((X0 + 74, Y1 + 0.8, Z0 + 34), (X1 - 6, Y1 + 0.8, Z0 + 28)), ((X0 + 72, Y1 + 0.8, Z0 + 38), (X1 - 10, Y1 + 0.8, Z0 + 36))):
        ln = V.line(a, b)
        if ln:
            sh.line([ln[0], ln[1]], dimc(lerp(OCHRE, SIENNA, 0.4)), 1.4, 1.0)
            sh.line([ln[1], (ln[1][0] + 3, ln[1][1] - 0.6)], dimc(PRUSSIAN), 1.6, 1.0)
    # two written slips laid out to dry
    for i, xx in enumerate((X0 + 40, X0 + 52)):
        pp = V.poly([(xx, Y1 + 0.5, Z1 - 4), (xx + 8, Y1 + 0.5, Z1 - 4), (xx + 8, Y1 + 0.5, Z1 - 28), (xx, Y1 + 0.5, Z1 - 28)])
        sh.poly(pp, dimc(lerp(PAPER, NAPLES, 0.1)))
        ln = V.line((xx + 4, Y1 + 0.6, Z1 - 7), (xx + 4, Y1 + 0.6, Z1 - 24))
        if ln:
            sh.line([ln[0], ln[1]], dimc(INK), 0.8, 0.9)
    a = D.add(sh, keep=None)
    R.add_mask(grp, (a >= 0.5).astype(F32))
    return m


def north_slips(R, D, dusk=False):
    """The north wall's slips: thickest round the altar bay (on the two posts beside it, in rows on the plaster next to
    it), a row between the rail and the head beam, a scatter on the side bays."""
    rs = np.random.RandomState(1830)
    dim = 0.30 if not dusk else 0.45
    spots = []
    for px in (N_POSTS[1], N_POSTS[2]):
        spots += scatter(rs, px + 1, px + POST - 1, 20, NAGESHI[0] - 4, 0, w=(6.0, 8.0), h=(17.0, 22.0), rows=7)
    spots += scatter(rs, N_POSTS[1] - 60, N_POSTS[1] - 2, 70, NAGESHI[0] - 6, 0, rows=5)
    spots += scatter(rs, N_POSTS[2] + POST + 2, N_POSTS[2] + POST + 62, 70, NAGESHI[0] - 6, 0, rows=5)
    spots += scatter(rs, 30, RW - 30, NAGESHI[1] + 4, HEAD[0] - 30, 0, rows=2, h=(18.0, 24.0))
    spots += scatter(rs, 24, 150, 40, 140, 18) + scatter(rs, 480, RW - 24, 40, 140, 18)
    paste_slips(D, R, "N", spots, 11, dim=dim)
    return len(spots)


def east_slips(R, D, dusk=False):
    """The east wall's slips: on its middle post, a row under the rail, a few near the north corner and past the post. The
    plaster where the bars land is left plain."""
    rs = np.random.RandomState(1831)
    dim = 0.42 if not dusk else 0.55
    spots = scatter(rs, SIDE_POSTS[1] + 1, SIDE_POSTS[1] + POST - 1, 20, NAGESHI[0] - 4, 0, w=(6.0, 8.0), h=(17.0, 22.0), rows=7)
    spots += scatter(rs, 18, RD - 30, 166, NAGESHI[0] - 1, 0, rows=1, h=(15.0, 18.0))
    spots += scatter(rs, 18, 70, 30, 150, 10)
    spots += scatter(rs, SIDE_POSTS[1] + POST + 4, 380, 30, 160, 14)
    paste_slips(D, R, "E", spots, 12, dim=dim)
    return len(spots)


def beam_slips(R, D, zz, seed, dim):
    """Slips on a beam's face toward us (Z = zz), in a row."""
    rs = np.random.RandomState(seed)
    spots = scatter(rs, 10, RW - 10, HEAD[0] - 24, HEAD[1] - 2, 0, rows=1, h=(18.0, 22.0))
    paste_beam(D, R, spots, zz, seed, dim)
    return len(spots)


def paste_beam(D, R, spots, zz, seed, dim):
    """Slips on a beam's face toward us (a plane Z = zz): pasted by many hands, so at all heights on the beam, some
    overlapping, some gone (a pale scar where one was torn off), a few askew."""
    rs = np.random.RandomState(seed)
    sh = D.sheet()
    lo, hi = HEAD[0] - 25, HEAD[1] - 1
    for (u, v, w, h) in spots:
        if rs.rand() < 0.22:
            continue
        hh = rs.uniform(13.0, 21.0)
        vv = rs.uniform(lo, hi - hh)
        tone = SLIP_TONES[rs.choice(len(SLIP_TONES), p=[0.18, 0.30, 0.24, 0.14, 0.14])]
        c = lerp(tone, SHADE, dim * rs.uniform(0.85, 1.1))
        tilt = rs.uniform(-2.5, 2.5)
        uu = u + rs.uniform(-3, 3)
        if rs.rand() < 0.08:                                          # torn off: a scrap and the paste's mark
            pp = V.poly([(uu, vv, zz), (uu + w, vv, zz), (uu + w, vv + hh * 0.3, zz), (uu, vv + hh * 0.45, zz)])
            if len(pp) >= 3:
                sh.poly(pp, c, 0.8)
            continue
        pp = V.poly([(uu, vv, zz), (uu + w, vv, zz), (uu + w + tilt, vv + hh, zz), (uu + tilt, vv + hh, zz)])
        if len(pp) < 3:
            continue
        sh.poly(pp, c, 0.95)
        sh.line([pp[0], pp[1]], lerp(c, PRUSSIAN, 0.45), 0.5, 0.5)
        ln = V.line((uu + w / 2 + tilt * 0.5, vv + hh * 0.2, zz + 0.2), (uu + w / 2 + tilt * 0.85, vv + hh * 0.85, zz + 0.2))
        if ln:
            sh.line([ln[0], ln[1]], lerp(INK, c, 0.3), 0.7, 0.75)
    D.add(sh)


def west_slips(R, D, dusk=False):
    """Slips round the lattice: on its jambs' posts, under its sill, along the rail over it."""
    rs = np.random.RandomState(77)
    dim = 0.55 if not dusk else 0.66
    z0, z1, y0, y1 = LATTICE
    spots = scatter(rs, 18, z0 - 8, 20, NAGESHI[0] - 4, 0, rows=6, w=(6.0, 8.0), h=(16.0, 22.0))
    spots += scatter(rs, z0, z1, 22, y0 - 8, 0, rows=2, h=(17.0, 21.0))
    spots += scatter(rs, 18, 268, y1 + 8, NAGESHI[0] - 2, 0, rows=1, h=(12.0, 14.0))
    spots += scatter(rs, SIDE_POSTS[1] + 1, SIDE_POSTS[1] + POST - 1, 20, NAGESHI[0] - 4, 0, w=(6.0, 8.0), h=(17.0, 22.0), rows=7)
    paste_slips(D, R, "W", spots, 21, dim=dim)
    return len(spots)


# ---------------------------------------------------------------- the light (three RGBA pictures for the live layer)
def light_polys(k):
    """For each gap of the lattice at k: its light on the east wall (a quad, in room points; the part under the floor
    included, to be hidden by the wall's clip) and on the floor (a quad, its part past the east wall included, hidden by
    the floor's clip). -> [(wall quad, floor quad or None, gap)]"""
    t = t_of(k)
    ca, ta = math.cos(math.radians(AZ)), math.tan(math.radians(AZ))
    y0, y1 = LATTICE[2] + FRAME, LATTICE[3] - FRAME
    out = []
    for (za, zb) in gaps():
        yb, yt = y0 - RUN * t, y1 - RUN * t
        wall = [(RW, yb, za + DRIFT), (RW, yb, zb + DRIFT), (RW, yt, zb + DRIFT), (RW, yt, za + DRIFT)]
        xa = y0 * ca / t
        if xa < RW:
            xb = y1 * ca / t
            fl = [(xa, 0.2, za + xa * ta), (xb, 0.2, za + xb * ta), (xb, 0.2, zb + xb * ta), (xa, 0.2, zb + xa * ta)]
        else:
            fl = None
        out.append((wall, fl, (za, zb)))
    return out


def bars_wall(k=0.0):
    """The bars on the east wall at k: soft-edged (the sun's own penumbra), a little brighter in the middle of each."""
    a = np.zeros(SHAPE, F32)
    for wall, fl, g in light_polys(k):
        pp = V.poly(wall)
        if len(pp) >= 3:
            m = mask_poly(SHAPE, pp, soft=1.1)
            a = np.maximum(a, m)
    core = blur(a, 2.0) * a
    alpha = np.clip(a * 0.84 + core * 0.10, 0, 0.94)
    rgb_ = np.zeros((H, W, 3), F32) + SUN[None, None, :]
    rgb_ = lerp(rgb_, SUN_HOT[None, None, :], np.clip(core, 0, 1)[..., None] * 0.35)
    return rgb_, alpha


def bars_floor(k=0.0):
    """The bars across the floor at k (with their part past the east wall: the clip hides it)."""
    a = np.zeros(SHAPE, F32)
    for wall, fl, g in light_polys(k):
        if fl is None:
            continue
        pp = V.poly(fl)
        if len(pp) >= 3:
            a = np.maximum(a, mask_poly(SHAPE, pp, soft=1.0))
    alpha = np.clip(a * 0.80, 0, 0.9)
    rgb_ = np.zeros((H, W, 3), F32) + lerp(SUN, SUN_HOT, 0.2)[None, None, :]
    return rgb_, alpha


def bars_air(k):
    """The shafts in the dusty air between the lattice and where the light lands, at k: very faint, a little brighter
    near the window, broken into motes by a grain of noise."""
    a = np.zeros(SHAPE, F32)
    t = t_of(k)
    y0, y1 = LATTICE[2] + FRAME, LATTICE[3] - FRAME
    for wall, fl, (za, zb) in light_polys(k):
        win = [(SLAT_D, y0, za), (SLAT_D, y0, zb), (SLAT_D, y1, zb), (SLAT_D, y1, za)]
        land = []
        for (x, y, z) in win:
            dist = y / t
            if dist * math.cos(math.radians(AZ)) <= RW:
                land.append((dist * math.cos(math.radians(AZ)), 0.0, z + dist * math.sin(math.radians(AZ))))
            else:
                land.append((RW, y - RUN * t, z + DRIFT))
        pts = [ipt(V.pt(*p)) for p in win + land]
        hull = _hull([tuple(p) for p in pts])
        a = np.maximum(a, mask_poly(SHAPE, hull, soft=2.5))
    x_win = V.pt(0, 120, (LATTICE[0] + LATTICE[1]) / 2)[0]
    x_end = V.pt(RW, 60, (LATTICE[0] + LATTICE[1]) / 2 + DRIFT)[0]
    xx = np.mgrid[0:H, 0:W][1].astype(F32)
    grad = np.clip(1 - (xx - x_win) / max(1.0, x_end - x_win), 0, 1)
    n = noise(SHAPE, (60, 6), 57, 3)
    alpha = np.clip(a * (0.07 + 0.13 * grad) * (0.7 + 0.6 * n), 0, 0.24)
    # the window itself glows a little into the room
    win_pp = V.poly(wquad("W", LATTICE[0], LATTICE[1], LATTICE[2], LATTICE[3], 2))
    glow_m = blur(mask_poly(SHAPE, win_pp), 9.0)
    alpha = np.maximum(alpha, glow_m * 0.22)
    rgb_ = np.zeros((H, W, 3), F32) + lerp(SUN_HOT, PAPER, 0.25)[None, None, :]
    return rgb_, alpha


# ---------------------------------------------------------------- the whole picture
def render(include=("lattice", "front", "stand"), dusk=False, seed=1):
    R = HallRoom(V, seed=seed + (5 if dusk else 0), base=dark_of(SIENNA, 0.85))
    D = Details(R)
    info = {}
    floor_m, back_m, right_m, left_m, ceil_m, win, n_slips = shell(R, D, dusk)
    info["n_slips"] = n_slips
    info["stand"] = stand_and_cabinet(R, D, dusk)[1]
    if "front" in include:
        desk(R, D, dusk)
        R.masks["lattice"] = R.masks["lattice"] * (1 - (R.masks["front"] >= 0.5))
    info["masks"] = {"floor": floor_m, "back": back_m, "right": right_m, "left": left_m, "ceil": ceil_m, "win": win}
    return R, D, info


PASS = Passes(seed=21)


def paint(R, D, fast):
    pic = R.img.copy()
    if not fast:
        pic = PASS.paint(pic, keep=0.30)
    pic = R.contours(pic)
    pic = D.lay(pic)
    return np.clip(pic, 0, 1)


def screen(pic, rgb_, a, dx=0, dy=0, clip=None):
    """Lay a light picture on a painting as the game will (screen blend), moved by (dx, dy), kept inside `clip`."""
    if dx or dy:
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        import cv2
        rgb_ = cv2.warpAffine(rgb_, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0))
        a = cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=0)
    if clip is not None:
        a = a * mask_poly(SHAPE, clip)
    lit = 1 - (1 - pic) * (1 - rgb_)
    return pic * (1 - a[..., None]) + lit * a[..., None]


# ---------------------------------------------------------------- layout.json
def clip_poly(pp):
    """A polygon clipped to the stage (Sutherland-Hodgman), as whole pixels."""
    def clip(poly, inside, inter):
        out = []
        for i in range(len(poly)):
            p, q = poly[i - 1], poly[i]
            if inside(q):
                if not inside(p):
                    out.append(inter(p, q))
                out.append(q)
            elif inside(p):
                out.append(inter(p, q))
        return out
    poly = [tuple(p) for p in pp]
    for edge in ("l", "r", "t", "b"):
        if not poly:
            break
        if edge == "l":
            poly = clip(poly, lambda p: p[0] >= 0, lambda p, q: (0, p[1] + (q[1] - p[1]) * (0 - p[0]) / (q[0] - p[0])))
        elif edge == "r":
            poly = clip(poly, lambda p: p[0] <= 799, lambda p, q: (799, p[1] + (q[1] - p[1]) * (799 - p[0]) / (q[0] - p[0])))
        elif edge == "t":
            poly = clip(poly, lambda p: p[1] >= 0, lambda p, q: (p[0] + (q[0] - p[0]) * (0 - p[1]) / (q[1] - p[1]), 0))
        else:
            poly = clip(poly, lambda p: p[1] <= 599, lambda p, q: (p[0] + (q[0] - p[0]) * (599 - p[1]) / (q[1] - p[1]), 599))
    return [ipt(p) for p in poly]


def wall_clip():
    """The east wall from its foot to the rail, from its north corner post to the edge of the picture."""
    return clip_poly(V.poly(wquad("E", POST, ZFAR, 0.0, NAGESHI[0])))


def floor_clip():
    """The floor west of the east wall's foot, from the north wall (the altar stand's front) to the bottom of the picture."""
    return clip_poly(V.poly([(0, 0, 0), (RW, 0, 0), (RW, 0, ZFAR), (0, 0, ZFAR)]))


def layout(info):
    pt = lambda X, Z: [min(799, max(0, ipt(V.pt(X, 0, Z))[0])), min(599, max(0, ipt(V.pt(X, 0, Z))[1]))]
    marks = {k: {"at": pt(*xz), "face": f} for k, (xz, f) in MARKS.items()}
    marks["ryokai"] = {"at": [ipt(V.pt(RYOKAI[0], 0, RYOKAI[1]))[0], ipt(V.pt(RYOKAI[0], 0, RYOKAI[1]))[1]], "face": "E",
                       "note": "OUTSIDE the west wall at the lattice (his feet, behind the `lattice` cut-out): only his face and shoulders show, in its gaps"}
    sx0, sx1, _, _, sz0, sz1 = STAND
    walk = [pt(24, 30), pt(sx0 - 14, 30), pt(sx0 - 14, sz1 + 14), pt(sx1 + 14, sz1 + 14), pt(sx1 + 14, 30), pt(RW - 17, 30), pt(RW - 17, WALK_FRONT + 16),
            pt(500, WALK_FRONT), pt(24, WALK_FRONT)]
    blocked = [{"id": "stand", "poly": [pt(sx0 - 6, 0), pt(sx1 + 6, 0), pt(sx1 + 6, sz1 + 8), pt(sx0 - 6, sz1 + 8)]}]
    hz = HUM[2]
    hx, hy = V.pt(*HUM)
    s = wall_px_per_cm(hz)
    # the wall's foreshortening at the hum: 10 cm along the wall beside 10 cm up it
    p0, p1, p2 = V.pt(RW, HUM_Y, hz - 5), V.pt(RW, HUM_Y, hz + 5), V.pt(RW, HUM_Y + 10, hz)
    wide = abs(p1[0] - p0[0]) / max(1e-6, abs(V.pt(RW, HUM_Y - 5, hz)[1] - V.pt(RW, HUM_Y + 5, hz)[1]))
    keep = sorted([int(round(V.pt(RW, HUM_Y, SIDE_POSTS[0] + POST + 2)[0])), int(round(V.pt(RW, HUM_Y, SIDE_POSTS[1] - 2)[0]))])
    base = int(round(V.pt(RW, 0, hz)[1]))
    r_coin = 9
    r_hand = int(round(20.0 * s))                                    # a hand's breadth across: 20 cm on the wall there
    hum_poly = [ipt((hx + 16 * wide * math.cos(a), hy + 16 * math.sin(a))) for a in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
    # the light: k -> where things are
    wall_rise_cm = RUN * (T0 - T1)
    rise_px = round(wall_rise_cm * s, 1)
    mid_z = (LATTICE[0] + LATTICE[1]) / 2 + DRIFT
    f0 = floor_from(0.0)
    p_a = V.pt(f0, 0, mid_z - DRIFT + f0 * math.tan(math.radians(AZ)))
    p_b = V.pt(RW, 0, mid_z)
    floor_to = [round(p_b[0] - p_a[0], 1), round(p_b[1] - p_a[1], 1)]
    table = []
    for k in (0.0, 0.25, round(K_FLOOR, 3), round(K_HUM, 3), 0.75, 1.0):
        yb, yt = wall_band(k)
        table.append({"k": k, "sun_deg": round(math.degrees(math.atan(t_of(k))), 2), "wall_band_cm": [round(yb, 1), round(yt, 1)],
                      "floor_from_X_cm": round(min(RW, floor_from(k)), 1), "wall_dy_px": round(-k * rise_px, 1)})
    gz = gaps()
    things = {
        "lattice": {"poly": clip_poly(V.poly(wquad("W", LATTICE[0] - 6, LATTICE[1] + 6, LATTICE[2] - 6, LATTICE[3] + 6))), "stand": marks["lattice"]["at"],
                    "note": "the west lattice: five slats, the sunset in the gaps; a cut-out with the west wall (`lattice`)"},
        "bars": {"poly": [list(p) for p in _hull([tuple(q) for wl, fl, g in light_polys(K_HUM) for q in V.poly(wl)] + [tuple(V.pt(SLAT_D, LATTICE[3], LATTICE[0])), tuple(V.pt(SLAT_D, LATTICE[2], LATTICE[1]))])],
                 "stand": marks["mid"]["at"], "note": "the shafts and bars of light (the live layer: layout.json `bars`); the shape is where they are at the hum's moment"},
        "wall": {"poly": clip_poly(V.poly(wquad("E", 30.0, 380.0, 10.0, NAGESHI[0] - 2))), "stand": marks["hum"]["at"], "note": "the east wall's plain plaster, where the light lands"},
        "hum": {"at": ipt((hx, hy)), "poly": hum_poly, "size_px": [round(32 * wide), 32], "stand": marks["hum"]["at"],
                "note": "a shimmer in the plaster where a bar of light crosses it (the engine's: nothing painted); the small door opens here"},
        "cabinet": {"poly": clip_poly(_hull([tuple(p) for nm, pp, n in V.box(CABINET[0] - 9, CABINET[1] + 9, CABINET[2], CABINET[3] + 20, CABINET[4] - 2, CABINET[5] + 9) for p in pp])),
                    "stand": marks["cabinet"]["at"], "note": "the small closed cabinet on its stand (a Kannon inside, its doors shut: not shown, not named)"},
        "lamp": {"poly": clip_poly(_hull([tuple(p) for nm, pp, n in V.box(STAND[1] - 27, STAND[1] - 13, STAND[3], STAND[3] + 34, STAND[5] - 23, STAND[5] - 9) for p in pp])),
                 "stand": marks["cabinet"]["at"], "note": "an oil lamp on a short stand, right of the cabinet (unlit: the fx `lamp-flame` if the scene lights it)"},
        "incense": {"poly": clip_poly(_hull([tuple(p) for nm, pp, n in V.box((STAND[0] + STAND[1]) / 2 - 9, (STAND[0] + STAND[1]) / 2 + 9, STAND[3], STAND[3] + 18, STAND[5] - 19, STAND[5] - 5) for p in pp])),
                    "stand": marks["cabinet"]["at"], "note": "the bronze incense burner before the cabinet (cold: the fx `incense-smoke` if lit)"},
        "flowers": {"poly": clip_poly(_hull([tuple(p) for nm, pp, n in V.box(STAND[0] + 8, STAND[0] + 36, STAND[3], STAND[3] + 40, STAND[5] - 24, STAND[5] - 8) for p in pp])),
                    "stand": marks["cabinet"]["at"], "note": "flowers in a jar, left of the cabinet: two weeks shut in, they have drooped"},
        "slips": {"poly": clip_poly(V.poly(wquad("N", N_POSTS[1] - 62, N_POSTS[2] + POST + 64, 20, HEAD[0]))), "stand": marks["cabinet"]["at"],
                  "note": f"slips everywhere ({info.get('n_slips', 0)} painted): this shape is the thickest of them, round the altar bay; paper and thin wood, never copper"},
        "posts": {"poly": clip_poly(V.poly(wquad("E", SIDE_POSTS[1] - 2, SIDE_POSTS[1] + POST + 2, 0, HEAD[1]))), "stand": marks["big"]["at"],
                  "note": "the posts, each pasted with slips (this shape: the east wall's middle post, the nearest)"},
        "ceiling": {"poly": clip_poly(V.poly([(0, RH, 0), (RW, RH, 0), (RW, RH, ZFAR), (0, RH, ZFAR)])),
                    "note": "the board ceiling on its battens, the beams across with their slips"},
        "mats": {"poly": clip_poly(V.poly([(42, 0, 75), (588, 0, 75), (588, 0, 439), (42, 0, 439)])), "stand": marks["mats"]["at"], "note": "twelve tatami, black-edged; two round straw cushions before the altar"},
        "doorway": {"poly": [[0, 572], [799, 572], [799, 599], [0, 599]], "stand": marks["door"]["at"],
                    "note": "the open doors are BEHIND us (the south wall is cut away): the way out is the bottom edge; the evening lies on the floor near us"},
        "desk": {"poly": "the cut-out `front`'s silhouette", "stand": pt(170, WALK_FRONT), "note": "a low desk where women write their slips: blank slips, an inkstone, brushes"},
        "ume": {"stand": marks["ume"]["at"], "note": "O-Ume kneels here, by the way out, watching the hum"},
        "ryokai": {"stand": marks["ryokai"]["at"], "face": "where his face shows: see `ryokai_face`"},
    }
    face = V.pt(RYOKAI[0], 140.0, RYOKAI[1])
    out = {
        "scene": ID, "size": [W, H], "view": VIEW, "horizon": VIEW["horizon"], "full": VIEW["full"], "key": "edo-sunset",
        "room_cm": {"X": [0, RW], "Z": [0, RD], "H": RH, "note": "west wall X 0, east wall X 630, north wall Z 0, the south wall (the doors) at Z 450, cut away: the lens is at (330, 640), 230 cm up, outside the open doors"},
        "walk": walk, "blocked": blocked, "marks": marks,
        "stands": {k: {"at": v["at"], "grownup_px": int(round(V.person(*MARKS[k][0])[2] * 160 / 175))} for k, v in marks.items() if k in MARKS},
        "seats": {"humsit": {"at": marks["humsit"]["at"], "note": "Mom sitting on the floor before the hum (sit, floor, or kneel): her head below the light's path, so the light passes over her to the hum"},
                  "ume": {"at": marks["ume"]["at"], "seat": "kneel", "note": "O-Ume kneeling (as Grandmother Sei kneels: sit.seat \"kneel\")"}},
        "ryokai_face": {"at": ipt(face), "feet": marks["ryokai"]["at"], "head_cm": 140, "note": "his feet outside the west wall; his head shows through the lattice's gaps at this point; the cut-out `lattice` covers the rest of him (its base is the west wall's foot)"},
        "things": things,
        "planes": [
            {"id": "lattice", "src": "lattice.png", "base": [ipt(V.pt(0, 0, 0)), ipt(V.pt(0, 0, 240))],
             "dusk": "lattice-dusk.png", "note": "the whole west wall with the lattice's frame and slats, the gaps clear: everyone in the hall is in front of it; Ryōkai outside is behind it, his face in the gaps"},
            {"id": "front", "src": "front.png", "plane": "front", "dusk": "front-dusk.png", "note": "the women's writing desk near us at the left"},
        ],
        "states": {"day": "back.png and the planes: the hall at sunset (the light is the live layer's: `bars`)",
                   "dusk": "dusk.png (an alt over the whole stage) with lattice-dusk.png and front-dusk.png: after the sun has gone (the bars faded out, the lattice's sky gone to its afterglow, the room a step darker)"},
        "bars": {
            "what": "the sunset's bars of light through the lattice: across the floor and up the east wall, climbing as the sun sinks; three RGBA light pictures, keyed as frames, for the live layer (under the people), screen blend",
            "k": "0 when the family comes in (the sun 10 degrees up), 1 when it is nearly down (2 degrees); the scene tweens it, slowly (the design: the bars climb while they talk)",
            "sun": {"el0_deg": EL0, "el1_deg": EL1, "azimuth": "from the WNW, its light 2.5 degrees south of due east across the hall"},
            "wall": {"src": "bars-wall.png", "clip": wall_clip(), "move": "straight UP: dy = -k * rise_px (rows), dx 0", "rise_px": rise_px, "rise_cm": round(wall_rise_cm, 1),
                     "note": "painted at k 0, with the band's part below the floor included (the clip hides it): as it slides up, its foot rises out of the floor and its top climbs the wall, as the real band does. rise_px is measured at the hum; a pixel or two less at the band's far end, more at its near end"},
            "floor": {"src": "bars-floor.png", "clip": floor_clip(), "move": "dx, dy = (k / k_floor) * to, while k < k_floor", "to": floor_to, "k_floor": round(K_FLOOR, 3),
                      "fade": [round(K_FLOOR * 0.55, 3), round(K_FLOOR, 3)], "note": "painted at k 0 (the bars from X 408 to the wall); they slide east into the wall's foot and are gone by k_floor (opacity to 0 over `fade`)"},
            "air": {"src": "bars-air.png", "clip": None, "move": "none", "opacity": "1 to k 0.8, then down to 0 at k 1 (with the others)",
                    "note": "the shafts in the dusty air, drawn for the hum's moment; and the window's own glow"},
            "k_hum": round(K_HUM, 3), "hum_note": "from k_hum the band's top is past the hum (105 cm up): the hum is in the light, and the small door can open",
            "fade_out": "when the sun goes (#38 step 6): every bars picture's opacity to 0 over 3 to 4 s, after k reaches 1",
            "table": table,
            "gaps_cm": [[round(a, 1), round(b, 1)] for a, b in gz],
        },
        "hum": {"at": ipt((hx, hy)), "room_cm": [round(c, 1) for c in HUM], "scale_px_per_cm": round(s, 3), "wide": round(wide, 2),
                "note": "on the east wall's plaster in the middle of a bar of light, a hand's height up (105 cm); match round twenty's keep: a portal held part open is the shimmer"},
        "door": {"type": "portal", "at": ipt((hx, hy)), "r_coin": r_coin, "r_hand": r_hand, "coin_scale": round(r_coin / r_hand, 2), "wide": round(wide, 2), "keep": keep, "base": base,
                 "light": True, "pale": "#fff4d8",
                 "note": "the small door: a coin's size (open with scale coin_scale, or a portal of r_coin: strength 0.8, as the Nevada and Rome coin doors), then a hand's (r_hand: a hand and a rice ball through it) when the pink flashlight is on it. `light: true` bends the bars of light with the wall"},
        "fx": [
            {"id": "hum", "type": "portal", "at": ipt((hx, hy)), "r": 14, "wide": round(wide, 2), "keep": keep, "base": base + 0.5, "pale": "#fff4d8", "strength": 0.9, "bend": 0.8, "light": True,
             "note": "the hum's own shimmer: held part open (as the keep's, open 0.6) once the bar of light is on it (k >= k_hum)"},
            {"id": "door", "type": "portal", "at": ipt((hx, hy)), "r": r_hand, "wide": round(wide, 2), "keep": keep, "base": base + 1, "pale": "#fff4d8", "strength": 0.8, "light": True,
             "note": "the small door: open(1, { scale: coin_scale }) for the coin, open(1, { scale: 1 }) for the hand"},
            {"id": "lamp-flame", "type": "flame", "at": ipt(V.pt(STAND[1] - 20, STAND[3] + 34, STAND[5] - 16)), "size": 5, "base": info.get("stand", 0) + 0.5, "glow": 16, "lull": 0.1,
             "when": "only if the scene lights the lamp (it is cold when the doors are opened)"},
            {"id": "incense-smoke", "type": "smoke", "at": ipt(V.pt((STAND[0] + STAND[1]) / 2, STAND[3] + 18, STAND[5] - 12)), "base": info.get("stand", 0) + 0.5, "height": 70, "width": [1, 8],
             "lean": [6, -70], "color": "#e4e6ea", "opacity": 0.28, "when": "only if O-Ume lights incense"},
            {"id": "dust", "type": "shimmer", "poly": things["bars"]["poly"], "count": 26, "size": 2, "flow": [3, -0.4], "life": 3.2, "color": "#ffd8b0", "opacity": 0.32,
             "note": "motes turning in the light (while k < 1)"},
        ],
        "notes": "The hall at sunset. The light (the bars on the floor and the east wall, the shafts in the air) is NOT in back.png: it is bars-wall/-floor/-air.png on the live layer, moved by k (layout.json `bars`). The hum and the small door are the engine's portals at `hum`/`door`. The way out is the bottom edge (the open doors behind the lens). PAINT-21F.",
    }
    return out


# ---------------------------------------------------------------- all of it
AFTERGLOW = lerp(lerp(GERANIUM, PRUSSIAN, 0.55), COBALT, 0.2)


def dusk_of(pic, win):
    """After the sun has gone: the hall a step darker and bluer, the lattice's sky gone to its afterglow."""
    out = lerp(pic, lerp(SHADE, PRUSSIAN, 0.35)[None, None, :], 0.30)
    w = np.clip(win, 0, 1)[..., None]
    sky = lerp(pic, AFTERGLOW[None, None, :], 0.55)
    return out * (1 - w) + sky * w


def compose(pic, lights, k):
    """The painting with the light laid on as the game will, at k."""
    out = pic.copy()
    (wr, wa), (fr, fa), (ar, aa) = lights["wall"], lights["floor"], lights["air"]
    s = wall_px_per_cm(HUM[2])
    out = screen(out, wr, wa, 0, -k * RUN * (T0 - T1) * s, wall_clip())
    if k < K_FLOOR:
        lay = layout_cache()
        to = lay["bars"]["floor"]["to"]
        f = k / K_FLOOR
        fade = 1.0 - np.clip((k - K_FLOOR * 0.55) / (K_FLOOR * 0.45), 0, 1)
        out = screen(out, fr, fa * fade, to[0] * f, to[1] * f, floor_clip())
    op = 1.0 if k <= 0.8 else max(0.0, 1 - (k - 0.8) / 0.2)
    out = screen(out, ar, aa * op)
    return out


_LAY = {}


def layout_cache():
    if "x" not in _LAY:
        _LAY["x"] = layout({})
    return _LAY["x"]


def layout_only(n_slips):
    """Rewrite out/edo-hall/layout.json from the measurements alone (no painting): `python3 edo_hall.py layout <slips>`."""
    lay = layout({"n_slips": n_slips, "stand": int(round(V.pt(STAND[0], 0, STAND[5])[1]))})
    json.dump(lay, open(f"{OUT}/layout.json", "w"), indent=1)
    print("layout.json written")


def main():
    t0 = time.time()
    if len(sys.argv) > 1 and sys.argv[1] == "layout":
        return layout_only(int(sys.argv[2]) if len(sys.argv) > 2 else 448)
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    fast = mode == "fast"
    lights = {"wall": bars_wall(0.0), "floor": bars_floor(0.0), "air": bars_air(K_HUM)}
    Rw, Dw, info = render()
    pic_w = paint(Rw, Dw, fast)
    lay = layout(info)
    _LAY["x"] = lay
    if fast:
        to_image(pic_w).save(f"{WORK}/fast-nolight.png")
        for k in (0.0, K_HUM, 1.0):
            to_image(compose(pic_w, lights, k)).save(f"{WORK}/fast-k{k:.2f}.png")
        json.dump(lay, open(f"{WORK}/layout-fast.json", "w"), indent=1)
        print("fast", round(time.time() - t0, 1), "s; slips", info["n_slips"], "k_hum", round(K_HUM, 3), "k_floor", round(K_FLOOR, 3), "hum", lay["hum"])
        return
    hard = lambda m: (m >= 0.5).astype(F32)
    m_lat, m_front, win = hard(Rw.masks["lattice"]), hard(Rw.masks["front"]), info["masks"]["win"]
    n_slips = info["n_slips"]
    del Rw, Dw, info
    Rb, Db, _ = render(include=())
    pic_b = paint(Rb, Db, fast)
    del Rb, Db
    pic_d, pic_db = dusk_of(pic_w, win), dusk_of(pic_b, win)
    pictures = {"back": (pic_b, None), "dusk": (pic_db, None),
                "lattice": (pic_w, m_lat), "front": (pic_w, m_front),
                "lattice-dusk": (pic_d, m_lat), "front-dusk": (pic_d, m_front)}
    finish_scene(OUT, pictures, colors=160, seed=9)
    for name, (rgb_, a) in lights.items():
        save_rgba(f"{OUT}/bars-{name}.png", rgb_, a)
    json.dump(lay, open(f"{OUT}/layout.json", "w"), indent=1)
    to_image(pic_w).save(f"{WORK}/composed-nolight.png")
    for k in (0.0, K_FLOOR, K_HUM, 0.75, 1.0):
        to_image(compose(pic_w, lights, k)).save(f"{WORK}/composed-k{k:.2f}.png")
    to_image(pic_d).save(f"{WORK}/composed-dusk.png")
    print("full", round(time.time() - t0, 1), "s:", len(pictures), "pictures + 3 light pictures, layout.json; slips", n_slips)


if __name__ == "__main__":
    main()

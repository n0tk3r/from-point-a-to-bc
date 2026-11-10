"""The Forum's front plane (rome_forum.py; round twenty-three: tools/paint/DEPTH.md, "Near"): what stands within a few
metres of the lens, between us and the play. People always pass behind it (`near.png`, plane "front", last in the
scene's `planes`).

WHERE WE STAND. The lens is 3.9 m above the square (rome_forum_model: EYE), which is a grown-up's eyes above a stone
landing 2.26 m up: the top of a doorstep on the rise of the Sacred Way, at the Forum's east end (the picture's bottom
edge is the way to the chief priest's house). So, through the scene's own camera (model.pt: x across, h up, D from the
lens, in cm), at their true size:

  the landing  the stone we stand on: its front edge 4.2 m from the lens, across the bottom of the picture from its
               left end (0.8 m to our left, where one step of the stair down shows) to the right edge. It tells why we
               look from so high, and it takes the bottom of the frame from the bare paving. Squared tufa in the
               porch's shade, its joints fanning out from the vanishing point, its worn edge catching the light of
               the square, sun through the laurel in soft flecks; a few trimmed sprigs of laurel lie on it.
  the column   the end column of the door's porch, 60 cm thick, standing at the landing's edge 3.75 m from the lens:
               its base (two tori and the hollow between) and the left third of its shaft, up the right edge of the
               frame to its top. Its lower third is painted red and smooth, with a dark ring where the red stops, and
               the stucco above is fluted: as the columns of the temple of Saturn are, at the far end of this picture.
               Deep and warm in the shade, turning lighter toward the open square on its left, a thin warm rim on
               that edge, two or three flecks of sun.
  the laurel   The doors of the priests' houses were dressed with fresh laurel on the first of March, a fortnight before
               this morning (Ovid, Fasti 3.137-142: "the king's door is green with Phoebus's tree"). A bough by each
               doorpost: the one by the column comes in from the top right corner, a dark mass with gaps to see
               through; the other, smaller, from the top left, before the temple of Castor's columns. Leaves a hand
               long at 3 m, the outer ones in the sun; bay is in bud in March: a few pale clusters. (The left bough's
               shade is the leafy edge of the shadow on the paving: rome_forum_ground.py.)

Nothing here is a thing to click or to pocket, and nothing clicked or stood on is behind it (depth_check.py): the
column's shaft begins at x 750 (the Gaul's last place ends at x 700; 27% of the site's area is behind it, and 35% is
the limit), the right bough keeps clear of the crane's head and of Juno's temple (nothing left of x 640), the left one
of Jupiter's hill (nothing right of x 165), the landing lies below the pigeons' ground (row 544).

    python3 rome_forum_near.py        -> out/rome-forum-work/near-look.png (the plane over the last painting's
                                         2-play.png), near-alpha.png, and how much of the picture it covers"""

import math

import numpy as np

from rome_forum_kit import *
from rome_steps_kit import Light
import depth

FLOOR = 226.0                                            # the landing we stand on, above the square's paving (cm)
LEDGE = dict(D=420.0, x0=-79.0, step=35.0, rise=19.0)    # its front edge, its left end; the stair goes down to the left
COLUMN = dict(x=194.0, D=375.0, r=30.0)                  # the porch's end column: its axis, the shaft's radius

FLECKS = [(-20.0, 403.0, 13.0), (44.0, 408.0, 9.0), (84.0, 396.0, 12.0), (14.0, 384.0, 8.0), (-52.0, 390.0, 9.0),
          (112.0, 411.0, 7.0)]                            # sun through the laurel, on the landing: (x, D, how big), cm

SHADE = "#2b2134"                                        # the near plane's shade: deep, a little violet (the key's own dark)
RIM = "#ffe9b8"                                          # light off the sunlit square, along the edges that face it
SUNNY = "#f6dca2"                                        # a fleck of sun on stone
ONES = Light(SUN, sun=(1.0, 1.0, 1.0), shade=(1.0, 1.0, 1.0), bounce=(0.0, 0.0, 0.0))     # (the lathe's form only: the light is in `paint`)


def shaded(color, k=0.66, warm=0.05):
    """A local colour as it is on the near plane, in the porch's shade."""
    return depth.near_tone(color, SHADE, k, warm)


# ---------------------------------------------------------------- the column
RED_TOP = 118.0                                          # the column's red goes this far up from the landing (cm), as Saturn's do


def column(cv, seed=301):
    """The end column of the porch, in shade: its base (two tori and the hollow between, straight on the landing, as
    the old temples have them), its lower third painted red and smooth, a dark ring where the red stops (the temple of
    Saturn's columns, at the far end of this picture, are painted so), the stuccoed shaft fluted above."""
    c = COLUMN
    r = c["r"]
    prof = [(FLOOR, r + 12.0), (FLOOR + 4.5, r + 13.6), (FLOOR + 9.5, r + 12.2), (FLOOR + 11, r + 6.6), (FLOOR + 14.5, r + 5.0), (FLOOR + 18, r + 6.6),
            (FLOOR + 19.5, r + 9.2), (FLOOR + 23, r + 9.8), (FLOOR + 26.5, r + 8.4), (FLOOR + 28, r + 2.8), (FLOOR + 30.5, r + 1.2), (FLOOR + 38, r + 0.2),
            (FLOOR + 330, r - 2.4)]
    Wc = WORLD.window([(700, -6), (806, 606)])
    hs_, rs_ = np.array([q[0] for q in prof]), np.array([q[1] for q in prof])
    mids, dr = hs_[:-1] + np.diff(hs_) / 2, np.diff(rs_) / np.maximum(np.diff(hs_), 1e-6)
    sky_ = unit((-1.0, 0.0, 0.15))                       # the open sky over the square, on our left
    sq = unit((-0.42, 0.0, 0.91))                        # the sunlit square, ahead and to the left

    def paint(h, around):
        a = around * 2 * math.pi
        nx, nz = np.cos(a), np.sin(a)
        arc = around * 2 * math.pi * r
        b = h - FLOOR
        own = col("#eadfc8")[None, None, :] * (1 + (tex(arc, h, 150, seed)[..., None] - 0.5) * 0.12 + (tex(arc, h, 26, seed + 1)[..., None] - 0.5) * 0.06)
        streak = step(0.60, 0.9, tex(arc * 5.0, h * 0.3, 90, seed + 2)) * 0.10
        own = own * (1 - streak[..., None])                                  # rain has run down the stucco
        red = col(RED)[None, None, :] * (0.92 + 0.16 * tex(arc, h, 40, seed + 3)[..., None])
        scuff = step(0.70, 0.86, tex(arc * 2.0, h * 0.6, 34, seed + 4, 3)) * np.clip(1 - (b - 38) / 60.0, 0, 1)
        red = lerp(red, own * 0.9, (0.55 * scuff)[..., None])                # the paint is knocked off low down, where people pass
        own = np.where(((b > 38) & (b < RED_TOP))[..., None], red, own)
        own = np.where((np.abs(b - RED_TOP - 3.0) < 3.0)[..., None], col(P_BLACK) * 1.5, own)
        open_ = np.clip(nx * sky_[0] + nz * sky_[2], 0, 1) ** 1.3             # how far the surface turns to the open square
        graze = np.clip((nx * sq[0] + nz * sq[2]) / 0.5, 0, 1)               # ...and takes light thrown back off it
        base = lerp(own, (col(SHADE) * 1.0)[None, None, :], 0.80) * np.array([1.20, 0.95, 0.88], dtype=F32)      # the porch's shade, warm with the floor's light
        lift = own * np.array([0.46, 0.41, 0.54], dtype=F32)                 # the sky's light on it
        warm = own * np.array([1.04, 0.86, 0.60], dtype=F32)                 # the square's light on it
        out = lerp(base, lift, (0.50 * open_)[..., None])
        out = lerp(out, warm, (0.72 * graze)[..., None])
        foot = np.clip((90 - b) / 90.0, 0, 1) * (b > 38)                      # light off the landing, low down
        out = out * (1 + 0.20 * foot[..., None] * np.array([1.0, 0.8, 0.5], dtype=F32))
        # the base's mouldings: what faces up takes the sky, what faces down is dark, the hollow between the tori darkest
        slope = np.interp(h, mids, dr)
        upf = np.sin(np.arctan(-slope)) * (b <= 38)
        out = out * (1 + 0.34 * np.clip(upf, 0, 1)[..., None] - 0.50 * np.clip(-upf, 0, 1)[..., None]) * (1 - 0.16 * (b <= 38)[..., None])
        out = out * (1 - 0.30 * (np.abs(b - 14.5) < 3.4)[..., None])
        return np.clip(out, 0, 1).astype(F32)

    cc, ca = lathe(Wc, ONES, c["x"], c["D"], prof, paint, flutes=20, flute_from=FLOOR + RED_TOP + 8, flute_to=FLOOR + 330, groove=0.75,
                   shadow=lambda h, s, around: np.ones_like(h), deep=0.0, bounce=0.0)
    # sun through the laurel: two flecks on the shaft, long as a round thing takes them, broken by the flutes
    sun = col(SUNNY)
    for (x, y, rx, ry, al) in ((768, 300, 6.5, 17.0, 0.80), (781, 236, 5.0, 11.0, 0.65), (762, 420, 5.5, 13.0, 0.75)):
        m = mask_ellipse(SHAPE, x, y, rx, ry, soft=1.2, wobble=2.0, seed=seed + int(x))[Wc.off[1]:Wc.off[1] + Wc.shape[0], Wc.off[0]:Wc.off[0] + Wc.shape[1]] * al
        tone = cc / np.maximum(cc.max(axis=-1, keepdims=True), 1e-3)          # (the surface's own hue, lit)
        cc = cc * (1 - m[..., None]) + np.clip(tone * sun * 1.02, 0, 1) * m[..., None]
    cv.put(cc, ca, Wc)


# ---------------------------------------------------------------- the landing we stand on
def landing(cv, seed=311):
    """The stone landing across the bottom of the picture, from its left end to the right edge, and the first step of
    the stair that goes down from its end: squared tufa in the porch's shade, slabs two feet wide laid end on to us (so
    their joints fan out from the vanishing point), worn smooth where feet cross it and giving back a little of the
    square's light toward its edge; the edge itself rounded by wear, pale, chipped; sun through the laurel in soft
    flecks; the column's own shade round its foot."""
    L, c = LEDGE, COLUMN
    for i, (xa, xb, hh, edge_) in enumerate(((L["x0"], 1500.0, FLOOR, L["D"]), (L["x0"] - L["step"], L["x0"], FLOOR - L["rise"], L["D"]))):
        for Wf, m in WORLD.face([(xa, 300.0, hh), (xb, 300.0, hh), (xb, edge_ + 1.6, hh), (xa, edge_ + 1.6, hh)], pad=2):
            u, v, ppc = Wf.on_floor(hh)
            tone, jm, above = courses(v + i * 61.0, u - L["x0"], long=124.0, high=62.0, seed=seed, joint=2.6, ppc=ppc, vary_len=0.3)
            far_ = edge_ + (hash2(np.floor((u - L["x0"]) / 62.0), 3, seed + 12) - 0.5) * 2.6       # no long edge is ruled: each slab stands a finger proud or shy of the next
            m = m * step(0.5, -0.5, v - far_)
            own = col("#c2ad90")[None, None, :] * (1 + (tone[..., None] - 0.5) * 0.22) * (1 + (tex(u, v, 60, seed + 1)[..., None] - 0.5) * 0.16)
            pit = step(0.74, 0.84, tex(u * 1.3, v * 1.3, 11.0, seed + 8, 3))                          # tufa is pitted
            own = own * (1 - 0.16 * pit[..., None])
            in_ = np.clip((far_ - v) / 62.0, 0, 1)                           # toward us it goes under the porch: darker
            foot = np.clip(1 - (np.hypot(u - c["x"], (v - c["D"]) * 0.8) - (c["r"] + 12)) / 26.0, 0, 1) if i == 0 else 0.0
            trod = np.exp(-((u + 20.0) / 85.0) ** 2) if i == 0 else 1.0     # worn smooth on the way to the stair
            dark = lerp(own, col(SHADE)[None, None, :], np.clip(0.73 + 0.17 * in_ + 0.10 * foot, 0, 0.95)[..., None]) * np.array([1.24, 0.97, 0.90], dtype=F32)
            sheen = (1 - in_) ** 2.0 * (0.40 + 0.60 * trod)                  # the worn stone gives back the square's light, at a low angle
            dark = lerp(dark, col("#a08a9c")[None, None, :], (0.20 * sheen)[..., None])
            dark = dark * (1 - 0.50 * jm[..., None]) + col("#8c7a80")[None, None, :] * (0.16 * above * (1 - jm))[..., None]      # the joints: dark, a slab's edge pale beside each
            sun = np.zeros(u.shape, dtype=F32)                               # sun through the laurel: a few soft flecks, no two alike
            wob = (tex(u, v, 14.0, seed + 6, 3) - 0.5) * 0.9
            for (fx_, fD_, fr_) in FLECKS if i == 0 else ():
                sun = np.maximum(sun, step(1.25, 0.45, np.hypot((u - fx_) / fr_, (v - fD_) / (fr_ * 0.8)) + wob) * (0.55 + 0.45 * hash2(np.float32(fx_), np.float32(fD_), seed)))
            out = lerp(dark, own * col(SUNNY) * 1.06, (0.80 * sun)[..., None])
            nose = np.clip(1 - (far_ - v) / 7.5, 0, 1) ** 0.8 * (0.50 + 1.0 * tex(u, v, 30, seed + 2))  # the edge, rounded by wear, catching the square's light
            chip = step(0.64, 0.72, tex(u * 1.0, v * 0.2, 17, seed + 3, 3)) * (v > far_ - 2.6)
            out = lerp(out, col(RIM)[None, None, :] * 0.88, (0.80 * np.clip(nose, 0, 1) * (1 - chip))[..., None])
            if i == 1:
                out = out * 0.84                                              # (the step below, a little deeper)
            cv.put(np.clip(out, 0, 1), m * (1 - chip * 0.9), Wf)              # a chipped edge is a broken outline
    s = Sheet2(SHAPE)
    a, b = pt(L["x0"], FLOOR, L["D"]), pt(L["x0"], FLOOR, 352.0)
    s.line([(a[0] + 0.4, a[1] + 0.3), (b[0] + 0.4, b[1])], mix(RIM, "#b89070", 0.30), 1.5, 0.92)      # the landing's end: its arris
    s.line([(a[0] - 1.2, a[1] + 1.6), (b[0] - 1.2, b[1])], shaded("#8c7c70", 0.86), 1.7, 0.92)         # and the riser's dark under it
    # a weed that has found a joint at the edge (the silhouette is the better for it)
    rng = np.random.default_rng(seed + 20)
    for (wx, n_, hgt) in ((-34.0, 7, 11.0), (236.0, 5, 8.0)):
        q = pt(wx, FLOOR, L["D"] - 1.5)
        for j in range(n_):
            ang = math.pi * rng.uniform(0.22, 0.78)
            ln = hgt * rng.uniform(0.6, 1.1) * k(L["D"])
            s.line([(q[0] + rng.normal(0, 1.6), q[1] + 0.5), (q[0] + math.cos(ang) * ln * 0.8, q[1] - math.sin(ang) * ln)], ["#263c28", "#34532f", "#7d9a4a"][j % 3], 1.3)
    sc, sa = s.done()
    cv.put(sc, sa)


def trimmings(cv, seed=313):
    """What was trimmed off when the door was dressed: a few sprigs and leaves of laurel lying on the landing. (Short,
    leafy and scattered: nothing that reads as a staff to pick up.)"""
    rng = np.random.default_rng(seed)
    s = Sheet2(SHAPE)
    L = LEDGE
    for i in range(13):                                  # leaves lying flat, seen at a low angle: their breadth is squeezed
        x_, D_ = rng.uniform(-50, 150), rng.uniform(L["D"] - 42, L["D"] - 6)
        p = pt(x_, FLOOR + 0.5, D_)
        ang = rng.uniform(-0.6, 0.6) + (math.pi if rng.random() < 0.5 else 0.0)
        ln = rng.uniform(8.0, 10.5) * k(D_)
        tone = (LEAF_DARK + LEAF_MID + LEAF_LIT[:1])[int(rng.integers(9))]
        ca_, sa_ = math.cos(ang), math.sin(ang) * 0.30
        pts = [(p[0] + ca_ * ln * t, p[1] + sa_ * ln * t - w * ln * 0.085) for t, w in ((0, 0), (0.25, 0.8), (0.5, 1.0), (0.78, 0.62), (1, 0), (0.78, -0.62), (0.5, -1.0), (0.25, -0.8))]
        s.poly(pts, tone)
    for (sx, sD, ang0, n_) in ((96.0, L["D"] - 9.0, 3.3, 7), (128.0, L["D"] - 17.0, 2.7, 5), (38.0, L["D"] - 12.0, 0.35, 5)):       # sprigs: a short twig, its leaves all one way
        q = pt(sx, FLOOR + 3.0, sD)
        kk = k(sD)
        tip = (q[0] + math.cos(ang0) * 15 * kk, q[1] + math.sin(ang0) * 15 * kk * 0.35)
        s.line([q, tip], "#3a2a22", max(1.2, 1.3 * kk))
        for j in range(n_):
            t = (j + 0.5) / n_
            bx, by = lerp(q[0], tip[0], t), lerp(q[1], tip[1], t)
            a_ = ang0 + (0.8 if j % 2 else -0.8) * (1 - 0.4 * t) + rng.normal(0, 0.15)
            r_ = rng.random()
            tone = LEAF_LIT[int(rng.integers(3))] if r_ < 0.18 else LEAF_MID[int(rng.integers(3))] if r_ < 0.42 else LEAF_DARK[int(rng.integers(5))]
            ln = rng.uniform(8.5, 10.5) * kk
            laurel_leaf(s, bx, by - 1.0, math.atan2(math.sin(a_) * 0.5 - 0.12, math.cos(a_)), ln * (0.75 + 0.25 * abs(math.cos(a_))), tone, wide=0.34)
    sc, sa = s.done()
    cv.put(sc, sa)


# ---------------------------------------------------------------- the laurel over the door
LEAF_DARK = ["#16271f", "#1c3023", "#223a28", "#2a4530", "#1f3526"]
LEAF_MID = ["#35553a", "#3f6340", "#476c3e"]
LEAF_LIT = ["#88a653", "#a3bd5c", "#c3d06e"]


def laurel_leaf(s, x, y, angle, length, tone, wide=0.30, rib=None, curl=0.0):
    """One bay leaf from its stalk end: lance-shaped, widest below the middle, its tip sharp."""
    ca, sa = math.cos(angle), math.sin(angle)
    left, right = [], []
    for t, w in ((0.0, 0.0), (0.10, 0.34), (0.28, 0.86), (0.45, 1.0), (0.62, 0.86), (0.80, 0.52), (0.93, 0.20), (1.0, 0.0)):
        bend = curl * length * t * t
        cx, cy = x + ca * length * t - sa * bend, y + sa * length * t + ca * bend
        wv = w * length * wide * 0.5
        left.append((cx - sa * wv, cy + ca * wv))
        right.append((cx + sa * wv * 0.92, cy - ca * wv * 0.92))
    s.poly(left + right[::-1], tone)
    if rib is not None:
        mid = [(x + ca * length * t - sa * curl * length * t * t, y + sa * length * t + ca * curl * length * t * t) for t in (0.04, 0.35, 0.65, 0.94)]
        s.line(mid, rib, max(0.7, length * 0.035), 0.85)


# The bough: two limbs in from the top right corner, and the shoots that leave them. Each shoot is (picture points, how
# thick at its two ends). A bay shoot carries its leaves close, all round it, turned toward its tip: so each shoot is a
# feather of leaves, and the feathers overlap into a mass. Nothing of it left of x 640 (the crane's head, Juno's temple).
LIMBS = [([(820, 8), (782, 18), (746, 28), (710, 43), (678, 60)], 10.0, 4.0),
         ([(820, 58), (792, 74), (770, 98), (754, 134), (746, 174)], 7.0, 3.0)]
SHOOTS = [
    ([(812, -3), (772, -1), (732, 3), (696, 9), (666, 19), (646, 33)], 4.6, 1.8),                 # along the frame's top
    ([(800, 12), (764, 9), (728, 13), (698, 23), (672, 37), (654, 55)], 4.0, 1.6),
    ([(780, 22), (748, 27), (716, 39), (690, 57), (674, 80)], 3.8, 1.6),
    ([(744, 30), (722, 48), (705, 73), (695, 101), (691, 128)], 3.6, 1.5),                        # hanging before the column's edge
    ([(708, 44), (682, 53), (661, 69), (646, 91)], 3.6, 1.5),                                     # out over the square, drooping
    ([(676, 60), (661, 84), (654, 112)], 3.0, 1.4),
    ([(690, 50), (666, 47), (647, 51)], 2.8, 1.3),
    ([(812, 40), (786, 52), (765, 70), (749, 98), (739, 132), (735, 166)], 4.4, 1.6),             # the spray down the column
    ([(806, 66), (784, 90), (771, 122), (765, 158), (767, 198)], 3.8, 1.5),
    ([(812, 100), (795, 128), (787, 160), (787, 194), (791, 222)], 3.4, 1.4),
    ([(770, 26), (758, 48), (751, 74), (749, 98)], 3.0, 1.4),
    ([(800, 30), (790, 52), (777, 70)], 3.0, 1.5),
    ([(812, 150), (801, 176), (799, 206)], 3.0, 1.4),
    ([(760, 100), (743, 118), (730, 142), (724, 168), (722, 186)], 3.0, 1.3),
    ([(792, 9), (771, 15), (753, 19)], 2.8, 1.4),
    ([(726, 14), (706, 28), (694, 44)], 2.8, 1.3),
    ([(812, 16), (798, 30), (790, 44)], 3.0, 1.5),
]


# The other doorpost's bough, on our left: less of it in the picture, in from the top left corner before the temple of
# Castor's columns (nothing of it right of x 165, where Jupiter's hill begins, or below row 120). It is this one's shade
# that lies in leaves along the edge of the porch's shadow on the paving (rome_forum_ground.CLUMPS).
LIMBS_LEFT = [([(-16, 4), (26, 16), (66, 34), (100, 56)], 8.0, 3.2)]
SHOOTS_LEFT = [
    ([(-12, -3), (28, 1), (64, 9), (98, 23), (124, 42)], 4.0, 1.6),
    ([(26, 16), (50, 38), (65, 64), (71, 92)], 3.4, 1.4),
    ([(66, 34), (96, 44), (122, 60), (140, 82)], 3.4, 1.4),
    ([(-12, 28), (13, 48), (29, 75), (35, 104)], 3.6, 1.5),
    ([(100, 56), (114, 80), (118, 102)], 2.8, 1.3),
    ([(-12, 62), (7, 86), (13, 114)], 3.0, 1.4),
    ([(40, 8), (62, 1), (86, 3)], 2.8, 1.3),
    ([(-12, 12), (4, 30), (8, 52)], 3.0, 1.4),
]


def bough(cv, limbs, shoots, out_of, seed):
    """A bough of bay: `limbs` and `shoots` as above; `out_of(x)` says how far out from under the porch's eaves a place
    in the picture is (0 to 1): the leaves out there are in the sun."""
    rng = np.random.default_rng(seed)
    deep, back, front, lit = Sheet2(SHAPE), Sheet2(SHAPE), Sheet2(SHAPE), Sheet2(SHAPE)
    wood, wood_l = "#2c221f", "#6a4c38"
    leaves = []

    def stem(pts_, w0, w1, sheet):
        cur = curve(pts_, 10)
        n = len(cur)
        for i in range(n - 1):
            wd = lerp(w0, w1, i / max(n - 2, 1))
            sheet.line([cur[i], cur[i + 1]], wood, wd)
            sheet.line([(cur[i][0] - 0.3, cur[i][1] - wd * 0.30), (cur[i + 1][0] - 0.3, cur[i + 1][1] - wd * 0.30)], wood_l, max(0.7, wd * 0.26), 0.5)
        return cur

    for (pts_, w0, w1) in limbs:
        stem(pts_, w0, w1, back)
    for si, (pts_, w0, w1) in enumerate(shoots):
        cur = stem(pts_, w0, w1, back)
        n = len(cur)
        seg = [math.hypot(cur[i + 1][0] - cur[i][0], cur[i + 1][1] - cur[i][1]) for i in range(n - 1)]
        total = sum(seg)
        want, acc, i, side = 3.0, 0.0, 0, 1
        while i < n - 1:
            while acc + seg[i] >= want:
                t = (want - acc) / max(seg[i], 1e-6)
                px_, py_ = lerp(cur[i][0], cur[i + 1][0], t), lerp(cur[i][1], cur[i + 1][1], t)
                tang = math.atan2(cur[i + 1][1] - cur[i][1], cur[i + 1][0] - cur[i][0])
                along = want / total
                ang = tang + side * rng.uniform(0.28, 0.95) * (1 - 0.45 * along)                        # turned toward the tip, the last ones along it
                ang += 0.20 * math.cos(ang)                                                             # and hanging a little
                ln = rng.uniform(21.0, 29.0) * (rng.uniform(0.60, 1.0) if rng.random() < 0.6 else 1.0) * (0.9 + 0.15 * (1 - along))
                leaves.append((px_, py_, ang, ln, rng.random(), rng.uniform(-0.10, 0.10), si))
                side = -side
                want += rng.uniform(4.2, 7.0)
            acc += seg[i]
            i += 1
        tip = cur[-1]
        tang = math.atan2(cur[-1][1] - cur[-2][1], cur[-1][0] - cur[-2][0])
        for d_ in (-0.55, -0.2, 0.15, 0.5):                                                             # the tuft at the tip
            leaves.append((tip[0], tip[1], tang + d_ + rng.normal(0, 0.1), rng.uniform(22, 29), rng.random(), rng.uniform(-0.08, 0.08), si))
    # the sun is behind us, high on the left: a leaf out over the square, on the bough's outer side, takes it; those
    # back under the porch's eaves are in its shade
    for (x, y, ang, ln, r_, curl, si) in leaves:
        tx, ty = x + math.cos(ang) * ln * 0.6, y + math.sin(ang) * ln * 0.6
        out_ = float(np.clip(out_of(tx), 0, 1))
        up_ = float(np.clip(-math.sin(ang) * 0.6 + 0.55, 0, 1))
        p_lit = 0.03 + 0.46 * out_ * (0.40 + 0.60 * up_)
        wide = rng.uniform(0.30, 0.37)
        if rng.random() < 0.55:                                                                         # the leaf behind it, in the bough's own dark
            laurel_leaf(deep, x + rng.normal(0, 2.5), y + rng.normal(0, 2.5), ang + rng.normal(0, 0.45), ln * rng.uniform(0.8, 1.05), LEAF_DARK[int(rng.integers(2))], wide)
        if r_ < p_lit * 0.5:
            laurel_leaf(lit, x, y, ang, ln, LEAF_LIT[int(rng.integers(3))], wide, rib="#eef0a8", curl=curl)
        elif r_ < p_lit:
            laurel_leaf(front, x, y, ang, ln, LEAF_MID[int(rng.integers(3))], wide, rib="#6f9050", curl=curl)
        elif r_ > 0.62:
            laurel_leaf(back, x, y, ang, ln, LEAF_DARK[int(rng.integers(5))], wide, curl=curl)
        else:
            laurel_leaf(front, x, y, ang, ln, LEAF_DARK[int(rng.integers(5))], wide, rib="#2f4a34" if r_ > 0.50 else None, curl=curl)
    for (x, y, ang, ln, r_, curl, si) in leaves[::7]:                                                   # bay in bud, in March
        for j in range(int(3 + r_ * 3)):
            bx, by = x + rng.normal(0, 2.4) + math.cos(ang) * 3, y + rng.normal(0, 2.2) + math.sin(ang) * 3
            lit.ellipse(bx, by, 1.6, 1.5, "#e2dc8e" if out_of(x) > 0.05 else "#9c9c5c")
    for sh in (deep, back, front, lit):
        sc, sa = sh.done()
        cv.put(sc, sa)


def laurel(cv, seed=321):
    """The laurel over the door: the bough by the column, a dark mass in the top right corner with gaps to see through,
    its leaves hand-long and clear at its edge, the outer ones in the sun; and the other doorpost's, in the top left."""
    bough(cv, LIMBS, SHOOTS, lambda x: (738 - x) / 78.0, seed)
    bough(cv, LIMBS_LEFT, SHOOTS_LEFT, lambda x: (x - 40) / 70.0, seed + 5)


# ---------------------------------------------------------------- the whole plane
def rim_light(cv, light=(-1.0, -0.35), width=2.0, amount=0.80):
    """A thin warm light along every edge of the plane that faces the square."""
    c, a = cv.straight()
    hard = (a > 0.5).astype(F32)
    m = depth.rim(hard, light=light, width=width) * amount
    m = m * (0.55 + 0.45 * noise(SHAPE, 34, 77, 3))                           # broken, as a brush lays it
    out = c * (1 - m[..., None]) + col(RIM)[None, None, :] * m[..., None]
    cv.c = out * cv.a[..., None]


def near(seed=301):
    """The front plane, painted: -> Canvas (rome_forum.py brushes it and gives it its hard edge)."""
    cv = Canvas(SHAPE)
    landing(cv)
    column(cv, seed)
    rim_light(cv, amount=0.85)                           # (the stone takes its rim before the leaves cross it)
    tr = Canvas(SHAPE)
    trimmings(tr)
    cv.lay(tr)
    lf = Canvas(SHAPE)
    laurel(lf)
    cv.lay(lf)
    return cv


if __name__ == "__main__":
    import os
    from PIL import Image
    cv = near()
    c, a = cv.straight()
    hard = (a > 0.5).astype(F32)
    os.makedirs("out/rome-forum-work", exist_ok=True)
    base = "out/rome-forum-work/2-play.png"
    pic = np.asarray(Image.open(base).convert("RGB"), dtype=F32) / 255.0 if os.path.exists(base) else np.full(SHAPE + (3,), 0.8, F32)
    over(pic, c, hard)
    Image.fromarray((np.clip(pic, 0, 1) * 255).astype(np.uint8)).save("out/rome-forum-work/near-look.png")
    rgba = np.dstack([np.clip(c, 0, 1), hard])
    Image.fromarray((rgba * 255).astype(np.uint8), "RGBA").save("out/rome-forum-work/near-alpha.png")
    print("covers %.1f%% of the picture" % (hard.mean() * 100))

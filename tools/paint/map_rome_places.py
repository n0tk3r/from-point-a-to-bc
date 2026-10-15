"""The map of Rome (MAP-15R): what the boy scratched into the wax. The lie of the land (the Tiber's bend, the Capitol's
hill), the six places and the five ways, each drawn with the stylus (map_rome_kit.Stylus) as a hand draws: plain lines,
small marks for buildings, an arrow or two; a small elevation for a temple or a house, a small plan for a room or a
square.

Laid out as the act's ways run (briefs/ROME-13.md, "The map"): the street to the left of Saturn's steps, the treasury
inside the temple behind them (above, on the tablet), the Forum below them, the Capitol to their right, rising above
the temple of Saturn as it does in Rome, and across the Tiber beyond the Forum's left end, over the stone bridge.

Each place's drawing is only what is in its scene (art/scenes/rome-*/ and the scene files):
  street    the street coming in, its houses, the snack bar's counter with its jars, the washerwoman's basket, the
            washing on two lines across the street (small tunics), the stepping stones, the fountain.
  steps     the temple of Saturn's front: its pediment, six columns, the doors, the notice on the high podium, the
            steps up between the podium's two cheeks.
  treasury  the room inside, in plan: thick walls, the strong door standing open, the god's niche in the far wall,
            the chests along the side walls (each a little chest seen from the side), the clerk's table and his coins.
  forum     the long open square: the hoarding round the site of the new senate house and the crane's wheel, the
            moneychanger's table under its striped awning, the Puteal, Juturna's basin, statues on two columns.
  capitol   the top of the hill: Jupiter's temple with the chariot on its roof, Romulus's hut, the geese's pen with
            three geese (the act's).
  tiber     the far bank below the bridge: the landing and its steps, two barges with their bales, the road along the
            river, the old man's house with its upper window, the house of prayer and its bench, the hen yard with its
            fig tree and the hens in a row.
No people, nothing of the story still to come, no light, no letters (the engine writes the names).

STANDS and NAMES say, for each place, the open ground its portraits stand on and on which side of its drawing its
name goes; map_rome_layout.py measures both from the finished pictures. WAYS_LINE keeps each way's line for the walk."""

import math

import numpy as np

from map_rome_kit import WAX

# ---------------------------------------------------------------- the lie of the land
RIVER = [(52, 349), (110, 351), (166, 359), (214, 377), (249, 405), (270, 441), (281, 482), (286, 522), (288, 552)]
RIVER_HALF = 14.0                  # half the river's width between its banks


def offset(pts, d, steps=14):
    """A smooth curve through pts, moved sideways by d (positive: to the right of the way it runs)."""
    from brush import curve
    c = np.asarray(curve(pts, steps), dtype=float)
    g = np.gradient(c, axis=0)
    n = np.stack([-g[:, 1], g[:, 0]], axis=1)
    n /= np.hypot(n[:, 0], n[:, 1])[:, None] + 1e-9
    return [tuple(p) for p in (c + n * d)]


def bank(which):
    """The river's bank lines: "city" (the Forum's side, up and to the right) or "far" (across the Tiber)."""
    return offset(RIVER, -RIVER_HALF if which == "city" else RIVER_HALF)


# the Capitol's hill: two rings round its top and the line of its foot, drawn round the hilltop's buildings (they run
# on off the top and the right of the tablet, where the hill goes on)
HILL = [
    [(624, 112), (594, 160), (580, 200), (580, 240), (590, 258), (615, 268), (650, 276), (700, 280), (745, 268),
     (770, 200), (760, 112)],
    [(584, 112), (568, 160), (564, 210), (567, 255), (580, 285), (610, 316), (660, 331), (720, 334), (760, 322),
     (790, 250), (790, 112)],
]
HILL_FOOT = [(576, 312), (598, 336), (640, 354), (700, 364), (748, 362)]


def land(st):
    """back.png's scratches: the Tiber's bend (its two banks and a few wavy marks between) and the Capitol's hill as
    contour lines. Nothing built: no bridge, no road, no wall."""
    for which in ("city", "far"):
        st.line(bank(which), w=1.7, depth=0.78, amp=0.6)
    rng = np.random.default_rng(17)
    from brush import curve
    mid = np.asarray(curve(RIVER, 20), dtype=float)
    seg = np.hypot(*np.diff(mid, axis=0).T)
    s = np.concatenate([[0], np.cumsum(seg)])
    for i, k in enumerate(np.arange(16, s[-1] - 10, 21.0)):
        x, y = np.interp(k, s, mid[:, 0]), np.interp(k, s, mid[:, 1])
        j = min(len(mid) - 2, int(np.searchsorted(s, k)))
        dx, dy = mid[j + 1] - mid[j]
        L = math.hypot(dx, dy) + 1e-9
        ux, uy = dx / L, dy / L
        side = (-1) ** i * rng.uniform(2.0, 5.5)
        x, y = x - uy * side, y + ux * side
        wave = [(x + ux * t - uy * 1.6 * math.sin(t / 2.2), y + uy * t + ux * 1.6 * math.sin(t / 2.2)) for t in np.linspace(-6, 6, 9)]
        st.line(wave, w=1.25, depth=0.55, amp=0.0)
    for loop in HILL:
        st.line(loop + loop[:3], w=1.3, depth=0.5, amp=0.7, smooth=True)
    st.line(HILL_FOOT, w=1.3, depth=0.5, amp=0.7, smooth=True)


# ---------------------------------------------------------------- small pictures a stylus makes
def temple_front(st, cx, apex, base, half, ncol, podium, doors=True, w=1.7):
    """A temple seen from the front: pediment, entablature, columns, the doors between the middle two, the podium's top.
    `apex` and `base` are the rows of the pediment's top and of the ground; `podium` the podium's height."""
    eave = apex + half * 0.36
    st.line([(cx - half - 2, eave), (cx, apex), (cx + half + 2, eave)], w=w, twice=True)
    st.line([(cx - half - 3, eave), (cx + half + 3, eave)], w=w, run=1)
    arch = eave + 5.5
    st.line([(cx - half - 1, arch), (cx + half + 1, arch)], w=w * 0.85)
    top = base - podium
    st.line([(cx - half - 2, top), (cx + half + 2, top)], w=w, twice=True)
    xs = np.linspace(cx - half + 4, cx + half - 4, ncol)
    for x in xs:
        st.line([(x, arch + 1.5), (x + 0.2, top - 1.5)], w=w * 1.05, amp=0.2)
        st.line([(x - 2.6, arch + 1.8), (x + 2.6, arch + 1.8)], w=1.1, amp=0.1)
        st.line([(x - 2.4, top - 1.8), (x + 2.4, top - 1.8)], w=1.1, amp=0.1)
    if doors:
        mid = ncol // 2
        dl, dr = xs[mid - 1] + 4.5, xs[mid] - 4.5
        st.line([(dl, top - 2.5), (dl, arch + 6), (dr, arch + 6), (dr, top - 2.5)], w=1.2, amp=0.15)
        st.line([((dl + dr) / 2, arch + 6.5), ((dl + dr) / 2, top - 3)], w=1.0, amp=0.1)
    return xs, top


def house(st, x0, base, w, h, roof=7.0, door=True, window=False, tiles=True):
    """A small house front: walls, a pitched roof (its tiles a few strokes), a door, an upper window."""
    x1 = x0 + w
    top = base - h
    st.line([(x0, base), (x0, top)], w=1.4, run=0.6)
    st.line([(x1, base), (x1, top)], w=1.4, run=0.6)
    st.line([(x0 - 2.5, top + 0.5), ((x0 + x1) / 2, top - roof), (x1 + 2.5, top + 0.5)], w=1.5)
    st.line([(x0 - 1, base), (x1 + 1, base)], w=1.3)
    if tiles:
        for f in (0.33, 0.66):
            st.line([(x0 + w * f * 0.5 + 1, top - roof * f * 0.95 + 1.2), (x0 + w * f * 0.5 + 3, top + 0.2)], w=0.9, amp=0.05)
    if door:
        dx = (x0 + x1) / 2
        st.line([(dx - 2.5, base - 0.5), (dx - 2.5, base - 7), (dx + 2.5, base - 7), (dx + 2.5, base - 0.5)], w=1.15, amp=0.1)
    if window:
        wx, wy = window
        st.rect(wx - 2.2, wy - 2.2, wx + 2.2, wy + 2.2, w=1.05, amp=0.05, over=0.3)


# ---------------------------------------------------------------- the places
def street(st):
    """The street, coming in from the left edge of the plan to the square before the temple."""
    y0, y1 = 253.0, 283.0              # its two sides
    xl, xr = WAX[0] - 3, 241.0
    st.line([(xl, y0 + 2), (xr - 30, y0 + 1), (xr, y0 - 1)], w=1.8, twice=True, amp=0.5, smooth=True)
    st.line([(xl, y1 + 2), (xr - 30, y1 + 1), (xr, y1 - 1)], w=1.8, twice=True, amp=0.5, smooth=True)
    # the houses along it, their fronts on the street, an alley here and there, each block its own depth
    for (a, b), d in zip(((70, 118), (122, 170), (175, 212), (216, 239)), (14, 12, 15, 11)):
        st.line([(a, y0 - 1), (a, y0 - d)], w=1.3, run=0.5)
        st.line([(a - 0.5, y0 - d), (b + 0.5, y0 - d - 0.5)], w=1.3, run=0.5)
        st.line([(b, y0 - d), (b, y0 - 1)], w=1.3)
    for (a, b), d in zip(((70, 104), (108, 160), (165, 203), (207, 239)), (12, 14, 12, 13)):
        st.line([(a, y1 + 1), (a, y1 + d)], w=1.3, run=0.5)
        st.line([(a - 0.5, y1 + d), (b + 0.5, y1 + d + 0.5)], w=1.3, run=0.5)
        st.line([(b, y1 + d), (b, y1 + 1)], w=1.3)
    # the snack bar's counter, set out on the street, with its jars sunk in it
    st.line([(76, y0 + 1), (76, y0 + 8), (106, y0 + 8), (106, y0 + 1)], w=1.6)
    for jx in (83.5, 91, 98.5):
        st.ellipse(jx, y0 + 4.6, 2.1, 1.8, w=1.05, amp=0.0)
    # the washerwoman's basket by the counter, and the washing hung across the street: two lines, a small tunic on one
    st.ellipse(88, y1 - 6.5, 6.0, 3.6, w=1.3, amp=0.1)
    st.line([(84, y1 - 8.5), (92, y1 - 4.5)], w=0.9, amp=0.05)
    st.line([(84, y1 - 4.5), (92, y1 - 8.5)], w=0.9, amp=0.05)
    for lx in (117.0, 129.0):
        st.line([(lx, y0 - 0.5), (lx + 2.2, (y0 + y1) / 2), (lx, y1 + 0.5)], w=1.0, smooth=True, amp=0.05)
    for tx, ty in ((119.2, y0 + 8), (119.2, y0 + 20), (131.2, y0 + 13)):     # tunics: a T for each
        st.line([(tx - 3.2, ty - 2.2), (tx + 3.2, ty - 2.2)], w=1.15, amp=0.0)
        st.line([(tx, ty - 2.2), (tx, ty + 3.4)], w=1.6, amp=0.0)
    # the stepping stones across it
    for sy in (y0 + 7, y0 + 15, y0 + 23):
        st.rect(208, sy - 2.6, 215, sy + 2.6, w=1.25, amp=0.05, over=0.3)
    # the fountain at the kerb, its basin and its spout on the wall
    st.rect(222, y1 - 9, 236, y1 - 1, w=1.5, amp=0.1, over=0.5)
    st.dot(229, y1 + 1.5, 1.3)
    st.line([(226, y1 - 5), (232, y1 - 5)], w=0.9, amp=0.3)


def steps(st):
    """Saturn's steps: the temple's front on its high podium, and the steps up to the columns."""
    cx = 355.0
    xs, top = temple_front(st, cx, apex=246, base=322, half=50, ncol=6, podium=25)
    # the podium's two cheeks and the steps between them
    lx, rx = cx - 33, cx + 33
    st.line([(cx - 52, top), (cx - 52, 322)], w=1.7)
    st.line([(cx + 52, top), (cx + 52, 322)], w=1.7)
    st.line([(lx, top + 1), (lx, 322)], w=1.5)
    st.line([(rx, top + 1), (rx, 322)], w=1.5)
    for i, yy in enumerate(np.linspace(top + 5, 318, 5)):
        st.line([(lx + 1, yy), (rx - 1, yy + 0.3)], w=1.25, amp=0.25)
    st.line([(cx - 60, 322.5), (cx + 60, 322)], w=1.8, twice=True, run=1)
    # the notice board on the podium's left cheek
    st.rect(cx - 47, top + 6, cx - 38, top + 15, w=1.1, amp=0.05, over=0.3)
    st.line([(cx - 45.5, top + 9.5), (cx - 39.5, top + 9.5)], w=0.8, amp=0.0)
    st.line([(cx - 45.5, top + 12.0), (cx - 40.5, top + 12.0)], w=0.8, amp=0.0)


def treasury(st):
    """The treasury, inside the temple: the room in plan behind the front."""
    x0, y0, x1, y1 = 294.0, 167.0, 416.0, 225.0
    t = 4.5                            # the walls' thickness
    door = (347.0, 363.0)
    # the walls, outer and inner lines, with the door's gap in the near wall
    st.line([(door[0], y1), (x0, y1), (x0, y0), (x1, y0), (x1, y1), (door[1], y1)], w=1.8, twice=True, amp=0.35)
    st.line([(door[0], y1 - t), (x0 + t, y1 - t), (x0 + t, y0 + t), (x1 - t, y0 + t), (x1 - t, y1 - t), (door[1], y1 - t)], w=1.4, amp=0.3)
    st.line([(door[0], y1 + 0.5), (door[0], y1 - t - 0.5)], w=1.4)
    st.line([(door[1], y1 + 0.5), (door[1], y1 - t - 0.5)], w=1.4)
    # the strong door, its two leaves standing open into the room
    st.line([(door[0] + 1, y1 - t), (door[0] + 3.5, y1 - t - 8.5)], w=1.7, amp=0.05)
    st.line([(door[1] - 1, y1 - t), (door[1] - 3.5, y1 - t - 8.5)], w=1.7, amp=0.05)
    # the god's niche in the far wall, an arch
    st.line([(348.5, y0 + t + 0.5), (348.5, y0 + t + 6), (350.5, y0 + t + 10), (355, y0 + t + 12), (359.5, y0 + t + 10),
             (361.5, y0 + t + 6), (361.5, y0 + t + 0.5)], w=1.35, amp=0.05)
    st.dot(355, y0 + t + 6.5, 1.2)
    # the chests along the side walls, each a little chest seen from the side: box, curved lid, lock
    for i, cy in enumerate((184.0, 197.0, 210.0)):
        for cxl in (x0 + t + 3.0, x1 - t - 16.0):
            st.line([(cxl, cy - 1.5), (cxl, cy + 4.5), (cxl + 13, cy + 4.5), (cxl + 13, cy - 1.5), (cxl, cy - 1.5)], w=1.2, amp=0.05)
            st.line([(cxl + 0.5, cy - 1.5), (cxl + 3, cy - 4.2), (cxl + 10, cy - 4.2), (cxl + 12.5, cy - 1.5)], w=1.1, amp=0.05)
            st.dot(cxl + 6.5, cy + 1.2, 0.85)
    # the clerk's table, and his coins on it
    st.rect(x1 - t - 34, y1 - t - 13, x1 - t - 19, y1 - t - 6, w=1.2, amp=0.05, over=0.3)
    for px, py in ((x1 - t - 30, y1 - t - 9.5), (x1 - t - 26.5, y1 - t - 9.5), (x1 - t - 23, y1 - t - 9.5)):
        st.dot(px, py, 0.9)


def forum(st):
    """The Forum: the long open square spreading from the foot of Saturn's steps."""
    x0, y0, x1, y1 = 338.0, 386.0, 624.0, 466.0
    st.line([(x0 + 2, y0), (x1, y0 + 1)], w=1.8, twice=True, run=1.5)
    st.line([(x1, y0 - 1), (x1 + 1, y1)], w=1.8, twice=True, run=1.5)
    st.line([(x1 + 1, y1), (x0, y1 + 1)], w=1.8, twice=True, run=1.5)
    st.line([(x0, y1 + 1), (x0 - 0.5, y1 - 15)], w=1.8, twice=True)                 # the mouth of the Tuscan street,
    st.line([(x0 - 0.5, y1 - 31), (x0 + 2, y0)], w=1.8, twice=True, run=1.0)          # open on the left
    # the colonnades along its two long sides: a prick for each column
    for k in range(17):
        st.dot(352 + k * 9.6 + (k % 2) * 0.4, y0 + 6.5, 1.15)
    for k in range(13):
        st.dot(410 + k * 9.6, y1 - 6.5, 1.15)
    # the hoarding round the site of the new senate house: a palisade, its gateway, and the crane's wheel by it
    hx0, hy0, hx1, hy1 = 540.0, 395.0, 614.0, 418.0
    st.line([(hx0 + 20, hy1), (hx0, hy1), (hx0, hy0), (hx1, hy0), (hx1, hy1), (hx0 + 30, hy1)], w=1.4, amp=0.25)
    for a, b, n in (((hx0, hy0), (hx1, hy0), 14), ((hx0, hy0), (hx0, hy1), 4), ((hx1, hy0), (hx1, hy1), 4)):
        st.hatch(a, b, n, 4.0, w=0.9)
    st.hatch((hx0 + 30, hy1), (hx1, hy1), 9, 4.0, w=0.9)
    st.hatch((hx0, hy1), (hx0 + 20, hy1), 4, 4.0, w=0.9)
    wx, wy = 523.0, 410.0
    st.ellipse(wx, wy, 8.0, 8.0, w=1.3, amp=0.0)
    for a in range(0, 180, 45):
        r = math.radians(a)
        st.line([(wx - 7 * math.cos(r), wy - 7 * math.sin(r)), (wx + 7 * math.cos(r), wy + 7 * math.sin(r))], w=0.9, amp=0.0)
    st.line([(wx, wy), (wx + 11, wy - 12)], w=1.2, amp=0.1)
    # the moneychanger's table under its striped awning, and his coins
    tx, ty = 398.0, 420.0
    st.rect(tx, ty, tx + 20, ty + 11, w=1.35, amp=0.05, over=0.5)
    for k in range(1, 5):
        st.line([(tx + 4 * k, ty + 0.8), (tx + 4 * k, ty + 10.2)], w=0.9, amp=0.0)
    for px, py in ((tx + 24, ty + 5), (tx + 27, ty + 8), (tx + 26.5, ty + 3)):
        st.dot(px, py, 0.9)
    # the Puteal, a ring of stone like a well's kerb
    st.ellipse(384.0, 444.0, 5.0, 5.0, w=1.3, amp=0.0)
    st.ellipse(384.0, 444.0, 2.0, 2.0, w=0.9, amp=0.0)
    # Juturna's basin, at the south side by Castor's temple
    st.ellipse(357.0, 447.0, 9.0, 6.0, w=1.4, amp=0.1)
    st.line([(351, 447), (355, 445.5), (359, 447), (363, 445.5)], w=0.9, amp=0.0)
    # statues on two columns
    for cx, cy in ((570.0, 442.0), (600.0, 440.0)):
        st.ellipse(cx, cy, 4.2, 4.2, w=1.25, amp=0.0)
        st.dot(cx, cy, 1.4)


def capitol(st):
    """The Capitol's top: the temple of Jupiter, Romulus's hut, the geese's pen and the geese."""
    cx = 674.0
    temple_front(st, cx, apex=184, base=232, half=40, ncol=6, podium=11, doors=True, w=1.6)
    # the bronze chariot on the roof's peak
    st.line([(cx - 5, 180), (cx + 4, 180)], w=1.2, amp=0.0)
    st.line([(cx - 5, 180), (cx - 6, 176)], w=1.0, amp=0.0)
    st.ellipse(cx - 2.5, 181.5, 1.6, 1.6, w=0.9, amp=0.0)
    st.ellipse(cx + 2.5, 181.5, 1.6, 1.6, w=0.9, amp=0.0)
    # Romulus's hut: round, its thatch coming to a point
    hx, hb = 612.0, 214.0
    st.line([(hx - 8, hb), (hx - 8, hb - 6), (hx, hb - 15), (hx + 8, hb - 6), (hx + 8, hb)], w=1.4, amp=0.1)
    st.line([(hx - 9, hb), (hx + 9, hb)], w=1.3)
    for k in (-4, 0, 4):
        st.line([(hx + k * 0.5, hb - 13), (hx + k, hb - 7)], w=0.8, amp=0.0)
    st.line([(hx - 2, hb), (hx - 2, hb - 4.5), (hx + 2, hb - 4.5), (hx + 2, hb)], w=1.0, amp=0.0)
    # the geese's pen, wattle round it, and three of Juno's geese in it: each a body, a long neck up, a beak
    px0, py0, px1, py1 = 590.0, 224.0, 627.0, 249.0
    st.rect(px0, py0, px1, py1, w=1.3, amp=0.15, over=0.6)
    st.hatch((px0, py0), (px1, py0), 8, 3.2, angle=60, w=0.85)
    st.hatch((px0, py1), (px1, py1), 8, 3.2, angle=60, w=0.85)
    for gx, gy, face in ((598.0, 242.0, 1), (611.0, 239.5, 1), (620.5, 243.5, -1)):
        st.line([(gx - face * 3.6, gy - 0.6), (gx + face * 2.4, gy + 0.2)], w=2.3, amp=0.0)            # the body
        st.line([(gx + face * 2.0, gy - 0.4), (gx + face * 2.6, gy - 6.0)], w=1.0, amp=0.0)            # the neck
        st.line([(gx + face * 2.6, gy - 6.0), (gx + face * 4.8, gy - 5.4)], w=1.0, amp=0.0)            # the beak


def tiber(st):
    """Across the Tiber: the far bank below the stone bridge."""
    # the landing: its steps down to the water
    for k in range(4):
        y = 460.0 + k * 5.5
        st.line([(229.0 + k * 0.7, y), (241.5 + k * 1.2, y + 1.2)], w=1.15, amp=0.1)
    st.line([(228.0, 457.0), (229.5, 480.0)], w=1.4)
    # the road along the river, downstream to the gardens' wall
    st.line([(222.0, 466.0), (220.5, 486.0), (219.5, 503.0)], w=1.5, amp=0.3, smooth=True)
    st.line([(211.0, 466.0), (209.5, 486.0), (208.5, 503.0)], w=1.5, amp=0.3, smooth=True)
    st.line([(204.0, 505.0), (227.0, 506.0)], w=1.6, twice=True)
    st.hatch((204.0, 505.0), (227.0, 506.0), 5, 3.0, angle=90, w=0.85)
    # two barges at the landing, laden with bales, and a post to tie them to
    def barge(cx, cy, L, wd, ang, bales):
        ca, sa = math.cos(ang), math.sin(ang)
        P = lambda u, v: (cx + u * ca - v * sa, cy + u * sa + v * ca)
        st.line([P(-L / 2, 0), P(-L / 2 + 6, -wd / 2), P(L / 2 - 6, -wd / 2), P(L / 2, 0), P(L / 2 - 6, wd / 2), P(-L / 2 + 6, wd / 2), P(-L / 2, 0)],
                w=1.4, amp=0.1)
        for u in bales:
            q = [P(u - 2.6, -2.4), P(u + 2.6, -2.4), P(u + 2.6, 2.4), P(u - 2.6, 2.4)]
            st.poly(q, w=0.95, amp=0.0, over=0.2)
    barge(260.5, 484.0, 34, 11, math.radians(81), (-8, 0, 8))
    barge(268.0, 524.0, 26, 9, math.radians(84), (-4, 4))
    st.dot(236.0, 491.0, 1.5)
    st.line([(237.5, 491.0), (255.5, 489.0)], w=0.8, amp=0.2)
    # a row of houses along the lane: the house of prayer (a little larger, its bench before it), a neighbour's, and
    # the old man's house with its upper window
    house(st, 76.0, 442.0, 36, 22, roof=9)
    st.line([(79, 450.0), (109, 450.0)], w=1.3)
    st.line([(82, 450.0), (82, 454.0)], w=1.0, amp=0.0)
    st.line([(106, 450.0), (106, 454.0)], w=1.0, amp=0.0)
    house(st, 122.0, 446.0, 24, 17, roof=7)
    house(st, 156.0, 446.0, 28, 22, roof=8, window=(163.0, 432.0))
    # the well in the little square before them
    st.ellipse(196.0, 446.0, 4.2, 4.2, w=1.3, amp=0.0)
    # the hen yard: a wattle fence, the fig tree in its corner, the hens in a row looking over the river at the city
    fx0, fy0, fx1, fy1 = 72.0, 462.0, 114.0, 500.0
    st.line([(fx0 + 26, fy0), (fx0, fy0), (fx0, fy1), (fx1, fy1), (fx1, fy0), (fx1 - 6, fy0)], w=1.25, amp=0.3)
    st.hatch((fx0, fy1), (fx1, fy1), 9, 3.2, angle=60, w=0.8)
    st.hatch((fx0, fy0), (fx0, fy1), 7, 3.2, angle=60, w=0.8)
    st.hatch((fx1, fy0), (fx1, fy1), 7, 3.2, angle=60, w=0.8)
    st.line([(81, 494), (81, 483)], w=1.2, amp=0.05)
    st.ellipse(81.0, 479.0, 6.0, 5.0, w=1.1, amp=0.5)
    st.ellipse(80.0, 478.5, 2.8, 2.2, w=0.9, amp=0.3)
    for k in range(5):
        hx, hy = 92.0 + k * 4.4, 471.0
        st.dot(hx, hy, 1.35)
        st.line([(hx - 1.4, hy + 0.3), (hx - 3.0, hy + 2.0)], w=0.8, amp=0.0)


PLACES = {"street": street, "steps": steps, "treasury": treasury, "forum": forum, "capitol": capitol, "tiber": tiber}


# ---------------------------------------------------------------- the ways
def way_steps_street(st):
    """From the end of the street to the foot of the temple: pricks, the way walked across the open ground."""
    st.dotted([(247, 268), (266, 273), (282, 286), (292, 304), (296, 318)], gap=6.5, r=1.3, smooth=True, first=0.1)


def way_steps_treasury(st):
    """Up the steps and in at the doors: a few pricks up from the roof, and an arrow into the door."""
    st.dotted([(355, 242), (355, 234)], gap=5.5, r=1.25, first=0.0)
    st.line([(355, 236), (355, 228.5)], w=1.4, amp=0.0)
    st.arrow((355, 228.0), (355, 240), size=5.0, spread=36, w=1.3)


def way_steps_forum(st):
    """From the foot of the steps down into the Forum: pricks, a walk across open ground."""
    st.dotted([(398, 330), (404, 346), (410, 362), (414, 380)], gap=6.5, r=1.3, smooth=True, first=0.2)


CAPITOL_ROAD = [(417, 309), (452, 315), (500, 318), (543, 308), (571, 288), (585, 268), (593, 254)]
TUSCAN = [(334, 434), (312, 432), (296, 435), (283, 441)]
BRIDGE = ((283.0, 441.0), (221.0, 455.0))


def way_steps_capitol(st):
    """Up the hill to the Capitol: the road round the back of Saturn's temple, climbing in a bend, as a double line,
    with an arrow up."""
    for side in (-5.0, 5.0):
        st.line(offset(CAPITOL_ROAD, side), w=1.6, amp=0.35)
    mid = offset(CAPITOL_ROAD, 0.0)
    n = len(mid)
    tail, tip = mid[int(n * 0.70)], mid[int(n * 0.80)]
    st.line([tail, tip], w=1.2, amp=0.0)
    st.arrow(tip, tail, size=4.2, spread=40, w=1.15)


def way_forum_tiber(st):
    """Down the Tuscan street from the Forum's left end, and over the stone bridge: the road's two lines, the bridge's
    deck across the river, its arches under it."""
    for side in (-5.0, 5.0):
        st.line(offset(TUSCAN, side, 8), w=1.6, amp=0.3)
    (ax, ay), (bx, by) = BRIDGE
    ux, uy = (bx - ax), (by - ay)
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    nx, ny = -uy, ux                      # (points down and a little left: downstream of the bridge)
    for side in (-4.5, 4.5):
        st.line([(ax + nx * side, ay + ny * side), (bx + nx * side, by + ny * side)], w=1.7, amp=0.2, twice=True)
    for f in (0.28, 0.52, 0.76):
        mx, my = ax + (bx - ax) * f + nx * 5.0, ay + (by - ay) * f + ny * 5.0
        pts = [(mx + ux * 5.0 * math.cos(t) + nx * 4.0 * (1 - math.sin(t)), my + uy * 5.0 * math.cos(t) + ny * 4.0 * (1 - math.sin(t)))
               for t in np.linspace(0, math.pi, 9)]
        st.line(pts, w=1.1, amp=0.0)
    st.line([(bx - 2, by + 1), (bx - 6, by + 6)], w=1.4, amp=0.0)


WAYS = {("steps", "street"): way_steps_street, ("steps", "treasury"): way_steps_treasury,
        ("steps", "forum"): way_steps_forum, ("steps", "capitol"): way_steps_capitol,
        ("forum", "tiber"): way_forum_tiber}

# ---------------------------------------------------------------- where the portraits stand, where the names go
# STANDS: the open ground of each place, a box (x0, y0, x1, y1) in which map_rome_layout.py finds the point farthest from
# anything drawn (the pin); "below" a place stands its portraits under its drawing, at that many pixels.
STANDS = {
    "street": (128, 258, 200, 278),
    "steps": ("below", 18),
    "treasury": (352, 192, 358, 200),
    "forum": (440, 412, 520, 440),
    "capitol": (640, 240, 708, 262),
    "tiber": (150, 476, 168, 484),
}
# NAMES: the side its name is written on, the gap (pixels) between them and the name's box, what it is beside (the
# place's drawing, its pin row, or both), and how far along that side (0 the top or left end, 1 the other; the middle
# unless it says)
NAMES = {
    "street": ("below", 3, "drawing"),
    "steps": ("right", 6, "drawing", 0.28),
    "treasury": ("left", 6, "drawing"),
    "forum": ("below", 4, "drawing"),
    "capitol": ("below", 5, "pin"),
    "tiber": ("below", 6, "pin"),
}
# WAYS_LINE: each way's line, from a's side to b's (the walk follows it; map_rome_layout.py snaps it to the scratches)
WAYS_LINE = {
    ("steps", "street"): [(296, 318), (292, 304), (282, 286), (266, 273), (247, 268)],
    ("steps", "treasury"): [(355, 244), (355, 236), (355, 230)],
    ("steps", "forum"): [(398, 330), (404, 346), (410, 362), (414, 380)],
    ("steps", "capitol"): CAPITOL_ROAD,
    ("forum", "tiber"): TUSCAN + [BRIDGE[1]],
}

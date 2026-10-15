"""The map of Rome (MAP-15R): the tablet itself, before anything is scratched on it.

PLAN
  Light     From the upper left, soft (a window): the frame's flat face lit evenly, its outer edge rounded (bright on
            the top and left, falling into cobalt-violet shade on the bottom and right), its inner walls at the top
            and the left in shade with a little shadow thrown onto the wax, those at the bottom and the right catching
            the light.
  Tones     LIGHT  the wood of the frame (the worn corners palest).
            DARK   the wax: deep brown to near black, warmer where it lies thick.
            The plan's scratches (map_rome_places.py) are the lights on the dark, where the eye goes.
  The wood  One board, hollowed out: its grain runs across the whole tablet, the same way on all four sides of the
            frame; one small knot in the bottom rail; the corners worn round and pale, a little grey where it has
            weathered, a few dents; two holes in the left rail for the cord that binds it to its other leaf, with the
            cord's ends through them.
  The wax   Smoothed with the flat end of the stylus: broad swipes, their faint ridges; the faint marks of earlier
            writing rubbed out (strokes of no letters at all: nothing in it can be read); a few specks; a little
            sheen.

under() blocks it in, strokes() (brush.py) repaints it at sizes that suit a flat sheet seen close, and details()
restates every hard edge and adds the small crisp things. map_rome.py runs the passes."""

import math

import numpy as np

from brush import F32, Sheet, blur, curve, grid, lerp, noise, over, strokes
from map_rome_kit import (BS, DV, LI, LW, NY, PB, RADIUS, SHAPE, SHEET, WAX, WAX_MID, WAX_SHEEN, WAX_THICK, WAX_THIN,
                          WOOD, WOOD_DARK, WOOD_LIGHT, WOOD_SHADE, YO, Stylus, cut, darker)

HOLES = [(52.0, 306.0), (52.0, 396.0)]     # the cord's holes in the left rail
KNOT = (588.0, 553.0)                      # a small knot in the bottom rail


def sd_box(x, y, box, r):
    """Signed distance to a rounded rectangle (negative inside)."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hx, hy = (x1 - x0) / 2 - r, (y1 - y0) / 2 - r
    qx, qy = np.abs(x - cx) - hx, np.abs(y - cy) - hy
    out = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0))
    return (out + np.minimum(np.maximum(qx, qy), 0) - r).astype(F32)


def shapes(seed=5):
    """The board's and the panel's signed distances, their edges a little uneven as a knife leaves them."""
    x, y = grid(SHAPE)
    jo = (noise(SHAPE, 60, seed, 3) - 0.5) * 1.3 + (noise(SHAPE, 14, seed + 1, 2) - 0.5) * 0.25
    ji = (noise(SHAPE, 50, seed + 2, 3) - 0.5) * 1.2
    board = sd_box(x, y, SHEET, RADIUS) + jo
    panel = sd_box(x, y, WAX, 3.5) + ji
    return board, panel


def board_mask():
    board, _ = shapes()
    return np.clip(0.5 - board, 0, 1)


def wood(seed=21):
    """The board's colour: straight grain across the tablet, bending round the knot."""
    x, y = grid(SHAPE)
    kx, ky = KNOT
    dx, dy = x - kx, (y - ky) * 1.6
    r2 = dx * dx + dy * dy
    bend = 7.0 * np.exp(-r2 / (2 * 16.0 ** 2)) * np.sign(y - ky + 1e-3)        # the grain parts round the knot
    yy = y + bend + (noise(SHAPE, (220, 40), seed, 3) - 0.5) * 9
    # broad bands of lighter and darker wood, and fine lines of grain, all running across
    from brush import sample
    bands = sample(noise(SHAPE, (300, 9), seed + 1, 4), x, yy)
    fine = sample(noise(SHAPE, (520, 2.4), seed + 2, 2), x, yy)
    lines = np.clip((fine - 0.62) * 5.0, 0, 1) * (0.5 + 0.5 * noise(SHAPE, (90, 30), seed + 3, 2))
    pores = np.clip((noise(SHAPE, (14, 1.2), seed + 4, 1) - 0.8) * 4, 0, 1)
    t = 0.25 + 0.75 * bands
    col = lerp(WOOD_LIGHT, WOOD, np.clip(t, 0, 1)[..., None])
    col = lerp(col, WOOD_DARK, (0.08 + 0.55 * lines + 0.2 * pores)[..., None] * 0.8)
    # the knot: a darker eye with rings round it
    kn = np.sqrt(r2)
    eye = np.exp(-(kn / 4.5) ** 2)
    rings = (0.5 + 0.5 * np.cos(kn / 1.6)) * np.exp(-(kn / 11) ** 2)
    col = lerp(col, lerp(WOOD_DARK, BS, 0.5), np.clip(eye * 0.95 + rings * 0.35, 0, 1)[..., None])
    weather = np.clip((noise(SHAPE, (160, 60), seed + 5, 3) - 0.45) * 2.2, 0, 1)
    col = lerp(col, lerp(col, LI, 0.5), (weather * 0.16)[..., None])            # grey-violet where it has weathered
    return col.astype(F32)


def worn(seed=31):
    """How worn the wood is: the four corners most, the outer edges a little."""
    x, y = grid(SHAPE)
    x0, y0, x1, y1 = SHEET
    w = np.zeros(SHAPE, F32)
    for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        w = np.maximum(w, np.exp(-(((x - cx) ** 2 + (y - cy) ** 2) / (2 * 26.0 ** 2))))
    board, _ = shapes()
    w = np.maximum(w, 0.35 * np.exp(-np.clip(-board, 0, None) / 3.5))
    return np.clip(w * (0.75 + 0.5 * noise(SHAPE, 20, seed, 3)), 0, 1)


def wax(seed=41):
    """The wax: its thickness (warmer where thick), the swipes of the flat end, the old writing rubbed out."""
    _, panel = shapes()
    inside = np.clip(-panel, 0, None)
    thick = 0.25 + 0.55 * noise(SHAPE, 150, seed, 4) + 0.30 * np.exp(-inside / 9.0)       # it climbs the walls a little
    thick += 0.10 * noise(SHAPE, 34, seed + 1, 3)
    t = np.clip(thick, 0, 1)
    col = lerp(WAX_THIN, WAX_MID, np.clip(t * 1.6, 0, 1)[..., None])
    col = lerp(col, WAX_THICK, np.clip((t - 0.55) * 1.7, 0, 1)[..., None])
    return col.astype(F32), t


def swipes(seed=51):
    """The flat end of the stylus, drawn over the whole panel many times: each swipe a broad band whose inside is a
    shade smoother (a little sheen) and whose two edges are faint ridges of pushed wax. -> (sheen, ridge) masks."""
    rng = np.random.default_rng(seed)
    x0, y0, x1, y1 = WAX
    sheen = Sheet(SHAPE, ss=2)
    ridge = Stylus(seed=seed, ss=2)
    for i in range(150):
        cx, cy = rng.uniform(x0 - 10, x1 + 10), rng.uniform(y0 - 6, y1 + 6)
        ang = rng.normal(0.0, 0.35) + (math.pi / 2 if rng.random() < 0.18 else 0)
        L = rng.uniform(50, 170)
        wd = rng.uniform(9, 20)
        bow = rng.normal(0, 10)
        ux, uy = math.cos(ang), math.sin(ang)
        pts = [(cx - ux * L / 2 + (-uy) * 0, cy - uy * L / 2), (cx - uy * bow, cy + ux * bow), (cx + ux * L / 2, cy + uy * L / 2)]
        pts = curve(pts, 10)
        shade = rng.uniform(0.35, 1.0)
        sheen.line(pts, (shade, shade, shade), wd, alpha=0.5)
        for side in (-1, 1):                       # its two edges
            edge = [(px - uy * side * wd / 2, py + ux * side * wd / 2) for px, py in pts]
            if rng.random() < 0.3:
                a = rng.integers(0, len(edge) // 3)
                b = len(edge) - rng.integers(0, len(edge) // 3)
                ridge.line(edge[a:b], w=0.9, depth=0.0, amp=0.6)
    c, a = sheen.done()
    s = (c[..., 0] - 0.5) * a * 2                  # -1..1 where swiped
    cov, _ = ridge.masks()
    return s.astype(F32), cov


def ghost_writing(seed=61):
    """Earlier writing, rubbed out: rows of short strokes and hooks the size of a hand's letters, no letter of any
    alphabet (they are made at random and cannot be read). -> a Stylus with them."""
    rng = np.random.default_rng(seed)
    st = Stylus(seed=seed + 1)
    x0, y0, x1, y1 = WAX
    y = y0 + rng.uniform(16, 26)
    while y < y1 - 10:
        x = x0 + rng.uniform(8, 40)
        slope = rng.normal(0, 0.02)
        end = x1 - rng.uniform(20, 160)
        while x < end:
            n = rng.integers(3, 9)                 # a run of the hand without lifting the point: a loopy line
            pts = []
            for _ in range(n):
                h = rng.uniform(5, 10)
                by = y + (x - x0) * slope
                pts += [(x, by - rng.uniform(0, 2)), (x + rng.uniform(1, 3), by - h), (x + rng.uniform(2, 5), by - rng.uniform(0, 3))]
                x += rng.uniform(4, 7)
            if rng.random() < 0.75:
                st.line(pts, w=1.1, depth=0.5, amp=0.3, smooth=True)
            x += rng.uniform(10, 30)
        y += rng.uniform(19, 25)
    return st


def under(seed=11):
    """Block in the tablet. -> (picture, info)"""
    x, y = grid(SHAPE)
    board, panel = shapes()
    on_board = np.clip(0.5 - board, 0, 1)
    in_panel = np.clip(0.5 - panel, 0, 1)
    wd = wood()
    wr = worn()
    wd = lerp(wd, lerp(WOOD_LIGHT, NY, 0.3), (wr * 0.55)[..., None])               # worn pale, the grain rubbed down
    # the frame's flat face: a little darker toward the panel where hands do not reach, lit evenly
    rim_in = np.clip(panel, 0, None)                                                # distance out from the panel
    wd = lerp(wd, WOOD_DARK, (np.exp(-rim_in / 3.0) * 0.18)[..., None])
    # its rounded outer edge: lit at the top and left, shaded at the bottom and right
    edge = np.exp(-np.clip(-board, 0, None) / 2.2) * on_board
    gy, gx = np.gradient(blur(board, 1.5))
    m = np.hypot(gx, gy) + 1e-6
    face = (gx / m) * -0.7071 + (gy / m) * -0.7071                                # >0: the edge faces the light
    wd = lerp(wd, WOOD_LIGHT, (edge * np.clip(face, 0, 1) * 0.55)[..., None])
    wd = lerp(wd, WOOD_SHADE, (edge * np.clip(-face, 0, 1) * 0.8)[..., None])
    # the panel's walls (a narrow chamfer): top and left in shade, bottom and right lit
    wall = np.exp(-np.clip(panel, 0, None) / 1.6) * (1 - in_panel)
    gy2, gx2 = np.gradient(blur(panel, 1.5))
    m2 = np.hypot(gx2, gy2) + 1e-6
    face2 = (gx2 / m2) * 0.7071 + (gy2 / m2) * 0.7071                              # >0: the wall faces up-left (lit)
    wd = lerp(wd, WOOD_SHADE, (wall * np.clip(-face2, 0, 1) * 0.85)[..., None])
    wd = lerp(wd, WOOD_LIGHT, (wall * np.clip(face2, 0, 1) * 0.5)[..., None])
    # the wax
    wx, thick = wax()
    s, ridges = swipes()
    wx = lerp(wx, WAX_SHEEN, (np.clip(s, 0, 1) * 0.045)[..., None])
    wx = wx * lerp(np.ones(3, F32), PB, (np.clip(-s, 0, 1) * 0.10)[..., None])
    # a broad soft sheen where the light lies along the wax, upper left to the middle
    sh = np.exp(-(((x - 300) * 0.55 + (y - 250)) ** 2) / (2 * 120.0 ** 2)) * np.exp(-((x - 330) ** 2) / (2 * 260.0 ** 2))
    wx = lerp(wx, WAX_SHEEN, (sh * 0.05)[..., None])
    # the frame's shadow on the wax, along the top and the left
    insd = np.clip(-panel, 0, None)
    top_left = np.clip(((WAX[0] + 9) - x) / 9, 0, 1) ** 1.5 + np.clip(((WAX[1] + 9) - y) / 9, 0, 1) ** 1.5
    shadow = np.clip(top_left, 0, 1) * np.exp(-insd / 5.0) * in_panel
    wx = wx * lerp(np.ones(3, F32), darker(DV, "prussian-blue", 0.3), (shadow * 0.55)[..., None])
    # and the wax's own edge catching the light at the bottom and the right
    lip = np.exp(-insd / 1.2) * in_panel * np.clip((x - (WAX[2] - 40)) / 40, 0, 1) ** 2
    lip += np.exp(-insd / 1.2) * in_panel * np.clip((y - (WAX[3] - 40)) / 40, 0, 1) ** 2
    wx = lerp(wx, lerp(WAX_THICK, NY, 0.25), (np.clip(lip, 0, 1) * 0.45)[..., None])
    pic = lerp(wd, wx, in_panel[..., None])
    # outside the board: the board's own shaded edge colour, so the brush carries nothing strange in
    pic = lerp(WOOD_SHADE * np.ones_like(pic), pic, on_board[..., None])
    info = {"board": board, "panel": panel, "on_board": on_board, "in_panel": in_panel, "ridges": ridges, "thick": thick}
    return pic.astype(F32), info


def flow_field(info, seed=71):
    """The brush's way where the picture is flat: along the grain on the wood, along the swipes on the wax."""
    a = (noise(SHAPE, 90, seed, 3) - 0.5) * 0.9
    return (a * info["in_panel"]).astype(F32)


def brushed(pic, info, fast=False, seed=2):
    """The brush pass: small brushes (the sheet is seen close), a high keep (the wax must stay calm under names)."""
    if fast:
        return pic.copy()
    wax_ = strokes(pic, sizes=(7, 4, 2), seed=seed, density=1.4, jitter=0.028, flow=flow_field(info), keep=0.55)
    wood_ = strokes(pic, sizes=(8, 4, 2), seed=seed + 1, density=1.6, jitter=0.04, flow=np.zeros(SHAPE, F32), keep=0.30)
    m = np.clip(info["in_panel"] * 1.0, 0, 1)[..., None]
    return (wood_ * (1 - m) + wax_ * m).astype(F32)


def details(pic, info, seed=81):
    """Every hard thing again, crisply, and the small crisp things."""
    board, panel = info["board"], info["panel"]
    on_board, in_panel = info["on_board"], info["in_panel"]
    rng = np.random.default_rng(seed)
    x, y = grid(SHAPE)
    # the ridges of the swipes, faint (no groove: only the pushed-up wax)
    rid = info["ridges"] * in_panel
    E = blur(rid, 1.3)
    gy, gx = np.gradient(E)
    relief = -(gx * -0.7071 + gy * -0.7071) * 3.0
    pic = lerp(pic, lerp(pic, WAX_SHEEN, 0.5), (np.clip(relief, 0, 1) * 0.12)[..., None])
    pic = pic * lerp(np.ones(3, F32), PB, (np.clip(-relief, 0, 1) * 0.10)[..., None])
    # the old writing, rubbed out: its grooves mostly filled, a faint trace and a faint burr left, patchily
    gw = ghost_writing()
    cov, dep = gw.masks()
    rub = np.clip((noise(SHAPE, 80, seed + 3, 3) - 0.42) * 2.4, 0, 1) * np.clip((noise(SHAPE, 9, seed + 4, 2) - 0.15) * 2, 0, 1)
    old, _ = cut(pic, cov * 0.9, dep * 0.35, seed=seed + 5, burr=0.8)
    pic = lerp(pic, old, (0.16 * rub * in_panel)[..., None])
    # specks of dust in the wax, and a few pits
    for _ in range(60):
        px, py = rng.uniform(WAX[0] + 4, WAX[2] - 4), rng.uniform(WAX[1] + 4, WAX[3] - 4)
        r = rng.uniform(0.5, 1.0)
        m = np.exp(-((x - px) ** 2 + (y - py) ** 2) / (2 * r * r)) * in_panel
        if rng.random() < 0.5:
            pic = lerp(pic, lerp(WAX_THICK, NY, 0.35), (m * 0.45)[..., None])
        else:
            pic = pic * lerp(np.ones(3, F32), PB, (m * 0.5)[..., None])
    # the frame's edges, crisp: a dark line where the rounded edge turns under at the bottom and right, a light one at
    # the top and left; the panel's edge the same, the other way round
    gyb, gxb = np.gradient(blur(board, 1.0))
    mb = np.hypot(gxb, gyb) + 1e-6
    face = (gxb / mb) * -0.7071 + (gyb / mb) * -0.7071
    line_out = np.clip(1 - np.abs(board + 0.9) / 0.9, 0, 1)
    pic = lerp(pic, darker(WOOD_SHADE, "deep-violet", 0.35), (line_out * np.clip(-face + 0.2, 0, 1) * 0.8)[..., None])
    pic = lerp(pic, WOOD_LIGHT, (line_out * np.clip(face, 0, 1) * 0.45)[..., None])
    gyp, gxp = np.gradient(blur(panel, 1.0))
    mp = np.hypot(gxp, gyp) + 1e-6
    facep = (gxp / mp) * 0.7071 + (gyp / mp) * 0.7071           # >0: the wall here faces up-left, toward the light
    line_in = np.clip(1 - np.abs(panel - 0.6) / 0.9, 0, 1)
    pic = lerp(pic, darker(lerp(WOOD_DARK, DV, 0.4), "prussian-blue", 0.3), (line_in * np.clip(-facep + 0.15, 0, 1) * 0.85)[..., None])
    pic = lerp(pic, lerp(WOOD_LIGHT, LW, 0.3), (line_in * np.clip(facep, 0, 1) * 0.6)[..., None])
    # a few crisp grain lines on the frame, and dents from years of use
    frame = on_board * (1 - in_panel) * np.clip(panel - 1.5, 0, 1)
    s = Sheet(SHAPE)
    for _ in range(26):
        yy = rng.choice([rng.uniform(SHEET[1] + 4, WAX[1] - 4), rng.uniform(WAX[3] + 4, SHEET[3] - 4)])
        xx = rng.uniform(SHEET[0] + 10, SHEET[2] - 160)
        L = rng.uniform(40, 150)
        pts = [(xx + t, yy + 0.9 * math.sin(t / rng.uniform(20, 40) + rng.uniform(0, 6))) for t in np.linspace(0, L, 14)]
        s.line(pts, lerp(WOOD_DARK, BS, 0.4), rng.uniform(0.5, 0.9), alpha=rng.uniform(0.25, 0.5))
    for _ in range(18):                                            # the side rails' grain is short, running across
        xx = rng.choice([rng.uniform(SHEET[0] + 3, WAX[0] - 3), rng.uniform(WAX[2] + 3, SHEET[2] - 3)])
        yy = rng.uniform(WAX[1], WAX[3])
        L = rng.uniform(8, 20)
        s.line([(xx - L / 2, yy), (xx + L / 2, yy + rng.normal(0, 0.6))], lerp(WOOD_DARK, BS, 0.4), 0.6, alpha=0.35)
    c, a = s.done()
    pic = over(pic, c, a * frame)
    dent = Stylus(seed=seed + 9)
    for _ in range(14):
        side = rng.integers(0, 4)
        if side == 0:
            px, py = rng.uniform(SHEET[0] + 20, SHEET[2] - 20), rng.uniform(SHEET[1] + 5, WAX[1] - 6)
        elif side == 1:
            px, py = rng.uniform(SHEET[0] + 20, SHEET[2] - 20), rng.uniform(WAX[3] + 6, SHEET[3] - 5)
        elif side == 2:
            px, py = rng.uniform(SHEET[0] + 5, WAX[0] - 6), rng.uniform(SHEET[1] + 20, SHEET[3] - 20)
        else:
            px, py = rng.uniform(WAX[2] + 6, SHEET[2] - 5), rng.uniform(SHEET[1] + 20, SHEET[3] - 20)
        a0 = rng.uniform(0, math.pi)
        L = rng.uniform(2, 6)
        dent.line([(px, py), (px + math.cos(a0) * L, py + math.sin(a0) * L)], w=0.9, depth=0.0, amp=0.2)
    cov, _ = dent.masks()
    E = blur(cov, 0.7)
    gy, gx = np.gradient(E)
    rel = -(gx * -0.7071 + gy * -0.7071) * 5
    pic = pic * lerp(np.ones(3, F32), darker(WOOD_DARK, "deep-violet", 0.2), (cov * 0.35 * frame)[..., None])
    pic = lerp(pic, WOOD_LIGHT, (np.clip(-rel, 0, 1) * 0.3 * frame)[..., None])
    # the cord's holes, and the cord's ends through them, running out over the edge to the other leaf
    for hx, hy in HOLES:
        d = np.hypot(x - hx, y - hy)
        hole = np.clip(4.8 - d, 0, 1)
        rim = np.clip(1 - np.abs(d - 5.3) / 1.2, 0, 1)
        dirx, diry = (x - hx) / (d + 1e-6), (y - hy) / (d + 1e-6)
        lit = np.clip(dirx * 0.7071 + diry * 0.7071, 0, 1)      # the far wall inside the hole, lower right, is lit
        pic = lerp(pic, darker(DV, "prussian-blue", 0.5), hole[..., None])
        pic = lerp(pic, lerp(WOOD_DARK, YO, 0.3), (hole * lit * np.clip(d - 1.5, 0, 1) * 0.6)[..., None])
        pic = lerp(pic, WOOD_SHADE, (rim * np.clip(-(dirx * 0.7071 + diry * 0.7071), 0, 1) * 0.5)[..., None])
        pic = lerp(pic, WOOD_LIGHT, (rim * lit * 0.5)[..., None])
    cord = Sheet(SHAPE)
    cord_dark = Sheet(SHAPE)
    for (hx, hy), bend in zip(HOLES, (-1, 1)):
        pts = curve([(hx + 0.5, hy), (hx - 5, hy + bend * 2.2), (SHEET[0] - 2, hy + bend * 4.5)], 8)
        cord_dark.line([(px + 0.8, py + 1.1) for px, py in pts], darker(WOOD_SHADE, "deep-violet", 0.3), 4.4, alpha=0.75)
        cord.line(pts, lerp(lerp(YO, NY, 0.45), LI, 0.15), 3.4)
        for i in range(1, len(pts) - 1, 2):                    # the twist of the cord
            px, py = pts[i]
            cord.line([(px - 1.4, py - 1.5), (px + 1.1, py + 1.4)], lerp(YO, BS, 0.6), 0.8)
    c, a = cord_dark.done()
    pic = over(pic, c, a * on_board)
    c, a = cord.done()
    pic = over(pic, c, a * on_board)
    return np.clip(pic, 0, 1).astype(F32)

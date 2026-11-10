"""PAINT-23 (round twenty-three, DEPTH.md): the NEAR plane of Himeji town (edo-town): what stands within a few metres of the
lens, between us and the play. People always pass behind it (`plane: "front"`).

WHERE WE STAND   The lens is 3.3 m above the highway (the scene's camera, unchanged), so what is near us and in the frame
is high: we look out from under the eaves of a house on our own side of the Saigoku-kaido (at the height of its upper
storey), north across the highway at Watamachi's fronts and the castle. Our side's fronts follow the highway's bend: the
eave over us runs back a little toward the left. What is near us, then:

  near.png        OUR EAVE: its underside across the top left, the rafters running back over us, the beam they lie on, the
                  edge with the lips of its tiles, its corner swept up at about x 400 where the house ends (beyond it the sky
                  is open over the keep); and ITS POST down the left edge, from the beam to below the frame, a bracket arm at
                  its head. Through the camera at its true size: the eave's edge is 2.6 to 3.1 m from the lens and 4 m up;
                  a rafter 6 cm wide is a finger's breadth of the picture.
  near-noren.png  across the top right corner, the hem of the next shop's eave curtain (two panels of indigo cotton, a
                  slit, a ring dyed white with a cotton boll in it: our own mark, no real house's), hanging from a pole
                  under that house's eave, out of the frame. Cloth: it stirs (the scene's one `sway` line).

All of it in shade (the houses behind us shade it from the high sun): the richest, warmest darks of the picture, lit only
by the sunlit street throwing its light up into it: a warm glow along the eave's edge, on the undersides of the rafters
and of the beam, down the street side of the post, on the curtain's hem. Outline before inside: the eave's edge and its
swept corner against the sky, the slit of the curtain; no small holes of sky inside any dark (the game's paints key a
speck of light shut in by darks as a highlight).

Nothing here is clicked or picked up, and nothing clicked or stood on is behind it (depth_check.py): the eave stays above
the cotton office's roof and well clear of the keep and the kite's circle; the post covers a sliver of the cotton office
(the scene's one `blocked` patch is the strip of street behind it, x 6 to 30); the curtain hangs over the sky and the far
roofs at the right, above the gate.
"""

import math

import numpy as np

from brush import F32, rgb, lerp, blur, grid, noise, curve, step
import depth as D
from edo_village_kit import Wet, grade_cut
from edo_town_kit import P, HZ, FOC, VX, EYE, W, H, SHAPE, PAINT, mix, col
from edo_town_wc import thin, deepen, WPAPER

# ---------------------------------------------------------------- the near paints: deep and warm in shade; the street's light
DARK = lerp(mix(PAINT["sienna"], col(PAINT["prussian"]), 0.66), rgb("#1c1220"), 0.42).astype(F32)       # old wood in deep shade
MID = lerp(mix(PAINT["sienna"], col(PAINT["prussian"]), 0.50), rgb("#1c1220"), 0.12).astype(F32)
WARM = lerp(mix(PAINT["sienna"], col(PAINT["ochre"]), 0.35), rgb("#2a1a1a"), 0.30).astype(F32)          # wood with the street's light in it
GLOW = lerp(mix(PAINT["ochre"], col(PAINT["sienna"]), 0.30), col(PAINT["naples"]), 0.22).astype(F32)          # the brightest bounce, at the very edge
BOARD = lerp(mix(PAINT["sienna"], col(PAINT["prussian"]), 0.74), rgb("#141018"), 0.50).astype(F32)       # the soffit boards between the rafters
TILE = lerp(mix(PAINT["prussian"], "#6f7890", 0.30), rgb("#141824"), 0.40).astype(F32)              # the tiles' lips, against the sky
TILE_LIT = lerp(mix("#6f7890", col(PAINT["cerulean"]), 0.25), rgb("#202838"), 0.30).astype(F32)
INDIGO = lerp(mix(PAINT["prussian"], col(PAINT["ultra"]), 0.45), rgb("#141632"), 0.18).astype(F32)       # the curtain in shade
INDIGO_MID = lerp(mix(PAINT["ultra"], col(PAINT["prussian"]), 0.38), rgb("#262646"), 0.08).astype(F32)
INDIGO_LIT = lerp(mix(PAINT["ultra"], col(PAINT["cobalt"]), 0.35), col(PAINT["sienna"]), 0.10).astype(F32)
DYE_WHITE = lerp(thin(col(PAINT["cerulean"]), 0.55), rgb("#9aa2c0"), 0.40).astype(F32)                   # the resist-dyed white, in shade

# ---------------------------------------------------------------- the eave over us, in the world (cm)
A = np.array([-178.0, 404.0, 313.0])          # the eave's edge at the left (beyond the frame)
C = np.array([-14.0, 404.0, 258.0])           # its corner, where our house ends
U = (C - A) / np.linalg.norm(C - A)           # along the eave, left to right
WIN = np.array([U[2], 0.0, -U[0]])            # inward: under the eave, toward the wall behind us (and toward the lens)
WIN /= np.linalg.norm(WIN)
PITCH = 0.42                                  # the rafters rise this much per cm inward
LIFT = 3.0                                    # the corner swept up (cm), over the last 70 cm of the edge
SWEEP = 70.0
ROOF = 0.52                                   # the roof's pitch (its verge rises this much per cm in)
BEAM_IN = 46.0                                # the beam the rafters lie on: this far in from the edge
POST_S = 63.0                                 # the post: this far along the eave from A (cm), under the beam (its middle at x 6)


def pt(v):
    return P(float(v[0]), float(v[1]), float(v[2]))


def lift(dist):
    """How far the edge is swept up at a distance (cm) from the corner (a townhouse's sweep: slight)."""
    t = max(0.0, 1.0 - dist / SWEEP)
    return LIFT * t ** 2.2


def front_edge(s, y_off=0.0):
    """The eave's front edge at s cm along it from A (its swept height at the corner)."""
    L = float(np.linalg.norm(C - A))
    p = A + U * s
    return p + np.array([0.0, lift(L - s) + y_off, 0.0])


def verge(r, y_off=0.0, out=0.0):
    """The gable's verge at our house's end: from the eave's corner, r cm in toward us and up the roof's slope (ROOF)."""
    p = C + WIN * r + U * out
    return p + np.array([0.0, LIFT + ROOF * r + y_off, 0.0])


def underside(base, r):
    """A point r cm in (toward the wall) from an edge point, on the rafters' underside."""
    return base + WIN * r + np.array([0.0, PITCH * r, 0.0])


def near_cut(seed=231):
    """near.png: our eave and its post. -> (colour, cover)."""
    L = Wet(SHAPE)
    rng = np.random.default_rng(seed)
    total = float(np.linalg.norm(C - A))
    # ---------------- the underside as seen: the front edge to the corner, the gable's verge up out of the frame; the soffit
    # fills to the top of the frame above them
    front = [pt(front_edge(s)) for s in np.linspace(-40.0, total, 60)]
    vg = [pt(verge(r, 0.0, 1.5)) for r in np.linspace(0.0, 90.0, 30)]
    vg = [p for p in vg if p[1] > -40]
    region = [(-20.0, -20.0)] + front + vg + [(vg[-1][0], -20.0)]
    g0 = pt(front_edge(total * 0.5))
    L.poly(region, lerp(BOARD, DARK, 0.3), lerp(BOARD, WARM, 0.14), g=((g0[0], -10.0), (g0[0], g0[1] + 4)))
    # ---------------- the rafters, running in over us: each a little lighter than the boards above it, its foot (near the
    # edge, where the street's light comes in under the eave) warm; its side toward us in its own shade
    for s in np.arange(-40.0, total - 10.0, 17.5):
        b = front_edge(s)
        a0, a1 = b - U * 3.0 + np.array([0, -1.0, 0]), b + U * 3.0 + np.array([0, -1.0, 0])
        poly = [pt(underside(a0, 3)), pt(underside(a1, 3)), pt(underside(a1, 170)), pt(underside(a0, 170))]
        L.poly(poly, lerp(MID, WARM, 0.14 + 0.10 * rng.random()), lerp(MID, DARK, 0.80), g=(pt(underside(b, 3)), pt(underside(b, 34))))
        sp = [pt(underside(a1, 3)), pt(underside(a1 + U * 1.6, 3)), pt(underside(a1 + U * 1.6, 170)), pt(underside(a1, 170))]
        L.poly(sp, lerp(DARK, BOARD, 0.5), alpha=0.85)
    # ---------------- the beam the rafters lie on (in the frame only near the post, where it is farthest from us)
    beam = []
    for s in np.linspace(POST_S - 30.0, total - 70.0, 30):
        e = front_edge(s)
        beam.append(e + WIN * BEAM_IN + np.array([0.0, PITCH * BEAM_IN - 9.0, 0.0]))
    bottom = [pt(b) for b in beam]
    inner = [pt(b + WIN * 13.0) for b in beam]
    top_in = [pt(b + WIN * 13.0 + np.array([0, 18.0, 0])) for b in beam]
    L.poly(bottom + inner[::-1], lerp(MID, WARM, 0.55), MID, g=(bottom[3], inner[3]))
    L.poly(inner + top_in[::-1], DARK)
    # ---------------- the gable's end at the corner: the barge board up the verge, dark, its lower edge catching the light
    vb_out = [pt(verge(r, 2.0, 3.0)) for r in np.linspace(0.0, 90.0, 24)]
    vb_in = [pt(verge(r, -16.0, 3.0)) for r in np.linspace(0.0, 90.0, 24)]
    L.poly(vb_out + vb_in[::-1], DARK)
    L.line([pt(verge(r, -16.0, 3.0)) for r in np.linspace(0.0, 90.0, 24)], WARM, 1.6, 0.6)
    # ---------------- the edge: the fascia's underside (a strip the street's light reaches), then the tiles' lips
    n_f = 70
    fas_out = [pt(front_edge(s)) for s in np.linspace(-40.0, total, n_f)]
    fas_in = [pt(front_edge(s) + WIN * 5.0 + np.array([0, 2.0, 0])) for s in np.linspace(-40.0, total, n_f)]
    L.poly(fas_out + fas_in[::-1], lerp(WARM, GLOW, 0.25), lerp(WARM, MID, 0.4), g=((200, 100), (200, 60)))
    lip = []
    for s in np.linspace(-40.0, total + 4.0, 230):
        ph = ((s + 400.0) % 27.0) / 27.0
        lip.append(pt(front_edge(s, -(2.4 + 1.3 * math.sin(ph * math.pi) ** 0.6))))
    outer = [pt(front_edge(s, 0.5)) for s in np.linspace(-40.0, total + 4.0, 230)]
    L.poly(lip + outer[::-1], TILE)
    for s in np.arange(-40.0 + 13.5, total - 4.0, 27.0):                    # the round end tiles' bottoms, the sky's light on them
        c = pt(front_edge(s, -2.2))
        r_ = 7.0 * FOC / front_edge(s)[2]
        L.ellipse(c[0], c[1] + 0.5, r_ * 0.60, r_ * 0.22, TILE_LIT, alpha=0.30)
    # ---------------- the post, down the left edge, under the beam (a 12 cm square timber, turned with the house)
    pc = A + U * POST_S + WIN * (BEAM_IN + 6.5)
    half = 6.0
    fl, fr = pc - U * half - WIN * half, pc + U * half - WIN * half       # its face toward the street (away from us)
    nl, nr = pc - U * half + WIN * half, pc + U * half + WIN * half       # its face toward us
    ytop = beam[0][1] + 2.0
    q = lambda v, y: pt(np.array([v[0], y, v[2]]))
    near_face = [q(nl, -400), q(nr, -400), q(nr, ytop), q(nl, ytop)]
    side_face = [q(nr, -400), q(fr, -400), q(fr, ytop), q(nr, ytop)]
    L.poly(near_face, DARK, lerp(DARK, MID, 0.25), g=((near_face[0][0], 0), (near_face[1][0], 0)))
    L.poly(side_face, lerp(DARK, MID, 0.6), lerp(MID, WARM, 0.65), g=((side_face[0][0], 0), (side_face[1][0], 0)))
    for i in range(11):                                                      # the grain: long checks, the weather's marks
        face = side_face if i % 3 else near_face
        t = rng.uniform(0.15, 0.85)
        y0, y1 = rng.uniform(20, 380), rng.uniform(420, 640)
        xa = face[0][0] + (face[1][0] - face[0][0]) * t
        L.line([(xa, y0), (xa + rng.normal(0, 0.6), (y0 + y1) / 2), (xa + rng.normal(0, 1.0), y1)], lerp(DARK, rgb("#0c0810"), 0.5), rng.uniform(0.5, 1.1), rng.uniform(0.35, 0.7))
    # the post's head: a short bracket block where it takes the beam, its underside lit from the street
    hd = [q(nl, ytop - 12.0), q(fr + U * 9.0, ytop - 12.0), q(fr + U * 9.0, ytop + 1.0), q(nl, ytop + 1.0)]
    L.poly(hd, DARK, lerp(DARK, WARM, 0.5), g=(hd[2], hd[1]))
    c, a = L.done()
    # ---------------- the light: the street's warm light along the edges that face down and out; the frame's corner deepest
    a_hard = (a > 0.5).astype(F32)
    rim = D.rim(a_hard, light=(0.35, 1.0), width=2.2)
    x, y = grid(SHAPE)
    warm = np.clip(c * 1.7 + np.array([0.12, 0.07, 0.02], dtype=F32), 0, 1)
    c = lerp(c, warm, (np.clip(rim, 0, 1) * 0.40)[..., None])
    deep = np.clip(1.0 - (x / 320.0) - (y / 140.0), 0, 1) ** 1.3 * 0.30   # farthest in under the eave: the top left corner
    c = c * (1 - deep[..., None])
    c = grade_cut(c, a, 0.96, lightfrom=(0.4, 1.0), seed=seed, uneven=0.07)
    return c.astype(F32), np.clip(a, 0, 1).astype(F32)


# ---------------------------------------------------------------- the next shop's curtain, across the top right corner
NOREN_S = (84.0, 160.0)       # along our house's line beyond its corner (cm from C): the curtain's left and right
NOREN_Y = (418.0, 371.0)      # its pole (out of the frame) and its hem
PANEL = 25.5                  # one width of cotton
SLIT = 3.4


def noren_cut(seed=233):
    """near-noren.png: the hem of the next shop's eave curtain, two widths of indigo cotton and the slit between them, hanging
    in soft folds; the dyed mark on the first. In shade: the folds that turn down toward the street catch its warm light.
    -> (colour, cover)"""
    L = Wet(SHAPE)
    rng = np.random.default_rng(seed)
    s0, s1 = NOREN_S
    y_top, y_hem = NOREN_Y
    out = C + WIN * -6.0                                     # (the next front stands a little forward of ours)
    panels = [(s0, s0 + PANEL), (s0 + PANEL + SLIT, s1)]
    dark = lerp(INDIGO, rgb("#0a0a1a"), 0.25)
    for i, (a_, b_) in enumerate(panels):
        # the cloth as many narrow upright strips, each coloured by how its fold is turned (a ripple across the width)
        n = 90
        ph0 = rng.uniform(0, 6.28)
        folds = rng.uniform(4.2, 5.2)
        for j in range(n):
            u0, u1 = a_ + (b_ - a_) * j / n, a_ + (b_ - a_) * (j + 1.05) / n
            t = (j + 0.5) / n
            ph = ph0 + t * folds * 2 * math.pi + 0.6 * math.sin(t * 7.0 + i)
            turn = math.sin(ph)                               # +1: the fold faces the street and its light, -1: in its trough
            depth_ = 0.5 + 0.5 * math.cos(ph)
            pa, pb = out + U * u0 + WIN * (1.2 * depth_), out + U * u1 + WIN * (1.2 * depth_)
            sag = 1.2 * math.sin(t * math.pi) + 0.9 * math.cos(ph)
            top = (pt(np.array([pa[0], y_top, pa[2]])), pt(np.array([pb[0], y_top, pb[2]])))
            bot = (pt(np.array([pb[0], y_hem - sag, pb[2]])), pt(np.array([pa[0], y_hem - sag, pa[2]])))
            lit = max(0.0, turn)
            c_top = lerp(dark, INDIGO_MID, 0.15 + 0.55 * lit)
            c_bot = lerp(lerp(INDIGO_MID, INDIGO_LIT, 0.75 * lit), dark, 0.45 * max(0.0, -turn))
            L.poly([top[0], top[1], bot[0], bot[1]], c_top, c_bot, g=((top[0][0], top[0][1] + 40), bot[0]))
        # the hem turned up and stitched: a deeper band; its very edge caught by the street's light
        hem = [pt(np.array([(out + U * u)[0], y_hem - 1.2 * math.sin((u - a_) / (b_ - a_) * math.pi), (out + U * u)[2]])) for u in np.linspace(a_, b_, 30)]
        hem_in = [pt(np.array([(out + U * u)[0], y_hem + 5.0, (out + U * u)[2]])) for u in np.linspace(a_, b_, 30)]
        L.poly(hem + hem_in[::-1], dark, alpha=0.45)
        L.line(hem, lerp(INDIGO_LIT, col(PAINT["ochre"]), 0.35), 1.1, 0.55)
    # the dyed mark on the first width, seen through the cloth from behind: a ring, and a cotton boll in it (our own mark)
    a_, b_ = panels[0]
    cm = out + U * ((a_ + b_) / 2)
    cx, cy = pt(np.array([cm[0], 395.0, cm[2]]))
    r_ = 6.2 * FOC / cm[2]
    ring_o = [(cx + r_ * math.cos(t), cy + r_ * 1.04 * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 48)]
    ring_i = [(cx + r_ * 0.76 * math.cos(t), cy + r_ * 0.79 * math.sin(t)) for t in np.linspace(2 * math.pi, 0, 48)]
    L.poly(ring_o + ring_i, DYE_WHITE, alpha=0.46)
    for t in (math.pi * -0.5, math.pi * -0.5 + 2.1, math.pi * -0.5 - 2.1):        # the boll's three locks, and its calyx below
        bx, by = cx + r_ * 0.26 * math.cos(t), cy + r_ * 0.26 * math.sin(t)
        L.ellipse(bx, by, r_ * 0.24, r_ * 0.22, DYE_WHITE, alpha=0.42)
    L.ellipse(cx, cy + r_ * 0.04, r_ * 0.08, r_ * 0.08, INDIGO_MID)
    c, a = L.done()
    a_hard = (a > 0.5).astype(F32)
    rim = D.rim(a_hard, light=(-0.2, 1.0), width=2.0)
    warm = np.clip(c * 1.5 + np.array([0.09, 0.06, 0.02], dtype=F32), 0, 1)
    c = lerp(c, warm, (np.clip(rim, 0, 1) * 0.40)[..., None])
    c = grade_cut(c, a, 0.95, lightfrom=(0.0, 1.0), seed=seed, uneven=0.05)
    return c.astype(F32), np.clip(a, 0, 1).astype(F32)


if __name__ == "__main__":                       # a quick look over a picture: python3 edo_town_near.py [picture.png]
    import sys
    from PIL import Image
    base = sys.argv[1] if len(sys.argv) > 1 else "out/edo-town-work/before-full.png"
    pic = np.asarray(Image.open(base).convert("RGB"), dtype=F32) / 255
    for f in (near_cut, noren_cut):
        c, a = f()
        m = (a > 0.5).astype(F32)[..., None]
        pic = pic * (1 - m) + c * m
        print(f.__name__, "covers", round(float((a > 0.5).mean()) * 100, 1), "%")
    Image.fromarray((np.clip(pic, 0, 1) * 255).astype(np.uint8)).save("out/edo-town-work/near-look.png")
    print([tuple(round(v, 1) for v in pt(front_edge(0))), tuple(round(v, 1) for v in pt(C)), tuple(round(v, 1) for v in pt(A + U * POST_S + WIN * BEAM_IN))])

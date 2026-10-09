"""Round four: the birds of the temple steps, painted as frames for the game to move (the smoke and the
birds are not painted into the picture any more: see PAINT_MOVING in rome_steps.py).

  pigeon-<n>.png        a feral pigeon, blue-grey, facing right (the game mirrors it to face left)
  pigeon-dark-<n>.png   the same frames, a darker chequered bird
  pigeon-pale-<n>.png   the same frames, a pale, nearly white one
  pigeon-shadow-1.png   the shadow a pigeon throws on the pavement (soft; never mirrored: the sun is on the right)
  swallow-<n>.png       a swallow high up, seen from below as it crosses the sky (wings up, level, down, swept)
  hen-white-<n>.png     the soothsayer's two sacred hens, seen from behind: they stand facing the temple doors
  hen-brown-<n>.png     (up the steps and a little to the right), stirring their heads and shuffling. They never peck.

Every frame of a set is the same size, with its foot point at the same place (FRAMES gives both), so the game
can swap frames without the bird jumping. Painted in the picture's own way: flat colour, the light from the upper
right, pigment grain, then the backdrop's own palette with its speckle (so they sit in the picture), hard edges.

  python3 rome_steps_birds.py      paints the frames into out/rome-steps/ and a sheet of them to look at
                                   (out/rome-steps-4-work/frames.png); rome_steps.py also calls paint() itself."""

import math
import os

import numpy as np
from PIL import Image

from brush import F32, Sheet, grain, lerp, save, to_palette
from rome_steps_kit import col, mix

S = 15.5                       # a pigeon's size, in pixels, at row 590 where the game draws people full size (scale 1)
PIGEON_BOX = (46, 50, 23, 40)  # frame width, height; the foot point (x, y) in it
SWALLOW_BOX = (16, 11, 8, 5)   # (the foot point of a flyer is the middle of its body)
HEN_BOX = (18, 20, 8, 17)

# the frames of each set, by what the game uses them for (numbers are the <n> of the file names)
PIGEON_ACTS = {
    "stand": [1], "look": [2], "alert": [3], "peck": [4, 5],
    "walk": [6, 7, 8, 9],                 # one step each: head back as the foot goes forward, head forward as it lands
    "turn": [10],                         # facing us: between facing right and facing left
    "takeoff": [11, 12], "fly": [13, 14, 15, 16], "glide": [17], "land": [18, 11],
}
PIGEON_NOTE = ("Facing right; mirror for left. Painted at scale 1 (row 590): the scene's own pigeons were 15.5 x (y - 260) / 330 px, "
               "so scale them like people. Feet on the ground at the foot point in every frame; in the flying frames the body "
               "stays where it is when standing, so the foot point can simply travel along the flight path.")
SWALLOW_ACTS = {"fly": [1, 2, 3, 2], "glide": [4]}
HEN_ACTS = {"stand": [1], "look": [2, 1, 3], "up": [4], "shuffle": [5, 6], "ruffle": [7]}

PIGEONS = {   # body, wing, dark (head, tail, bars), gleam
    "pigeon": ("#8a92a8", "#aab0c0", "#3c4256", "#6fa08c"),
    "pigeon-dark": ("#6a6c80", "#8a8a98", "#2c2c3c", "#7a9a7c"),
    "pigeon-pale": ("#e8e2d8", "#f4f0e8", "#a8a4a8", "#a8c4b0"),
}


def oval(sh, cx, cy, rx, ry, ang, color, alpha=1.0, n=28):
    """An ellipse turned by `ang` (radians, + turns its right end up)."""
    ca, sa = math.cos(ang), math.sin(ang)
    pts = [(cx + rx * math.cos(t) * ca + ry * math.sin(t) * sa, cy - rx * math.cos(t) * sa + ry * math.sin(t) * ca)
           for t in np.linspace(0, 2 * math.pi, n, endpoint=False)]
    sh.poly(pts, color, alpha)


def turned(points, pivot, ang):
    """Points turned about a pivot by `ang` (+ lifts what is right of the pivot)."""
    px, py = pivot
    ca, sa = math.cos(ang), math.sin(ang)
    return [(px + (x - px) * ca + (y - py) * sa, py - (x - px) * sa + (y - py) * ca) for x, y in points]


def finish_frame(c, a, palette, seed=7):
    """Grain, the palette with its speckle, hard edges: -> (index, alpha) like every cut-out of the scene."""
    g = grain(c, seed, 0.02)
    return to_palette(g, palette, seed=5, speckle=0.014), a


# ---------------------------------------------------------------- the pigeon
POSES = {
    #      head (x, y) in s,  beak,  body tilt, body lift, legs,      wings
    1: dict(head=(0.45, -0.86), beak=1, tilt=0.10, lift=0.0, legs="stand", wings="folded"),
    2: dict(head=(0.36, -0.92), beak=-1, tilt=0.10, lift=0.0, legs="stand", wings="folded"),      # looks back over its shoulder
    3: dict(head=(0.42, -1.00), beak=1, tilt=0.18, lift=0.0, legs="stand", wings="folded"),       # head up, neck stretched
    4: dict(head=(0.62, -0.50), beak=1, tilt=-0.12, lift=0.0, legs="stand", wings="folded"),      # pecking: on the way down
    5: dict(head=(0.68, -0.17), beak=1, tilt=-0.26, lift=0.0, legs="stand", wings="folded"),      # beak to the ground
    6: dict(head=(0.38, -0.88), beak=1, tilt=0.10, lift=0.0, legs="walk-a", wings="folded"),      # walking: head back,
    7: dict(head=(0.62, -0.80), beak=1, tilt=0.06, lift=0.02, legs="walk-mid", wings="folded"),   # head forward,
    8: dict(head=(0.38, -0.88), beak=1, tilt=0.10, lift=0.0, legs="walk-b", wings="folded"),      # (the other foot)
    9: dict(head=(0.62, -0.80), beak=1, tilt=0.06, lift=0.02, legs="walk-mid2", wings="folded"),
    11: dict(head=(0.52, -1.02), beak=1, tilt=0.45, lift=-0.05, legs="crouch", wings="up"),       # taking off: wings high,
    12: dict(head=(0.60, -0.92), beak=1, tilt=0.30, lift=0.22, legs="dangle", wings="down"),      # then the first beat down
    13: dict(head=(0.58, -0.70), beak=1, tilt=0.04, lift=0.0, legs="tucked", wings="up"),         # flying
    14: dict(head=(0.58, -0.70), beak=1, tilt=0.04, lift=0.0, legs="tucked", wings="level"),
    15: dict(head=(0.58, -0.70), beak=1, tilt=0.04, lift=0.0, legs="tucked", wings="down"),
    16: dict(head=(0.58, -0.70), beak=1, tilt=0.04, lift=0.0, legs="tucked", wings="half"),
    17: dict(head=(0.58, -0.70), beak=1, tilt=0.02, lift=0.0, legs="tucked", wings="glide"),
    18: dict(head=(0.42, -1.05), beak=1, tilt=0.65, lift=0.12, legs="reach", wings="brake"),      # landing: upright, wings forward
}

WINGS = {  # a wing in s, before the body is turned: shoulder, wrist, tip, then back along the trailing edge
    "up": [(0.05, -0.62), (-0.12, -1.20), (-0.52, -1.80), (-0.46, -1.40), (-0.40, -0.92), (-0.24, -0.62)],
    "down": [(0.08, -0.52), (0.06, -0.20), (-0.18, 0.34), (-0.28, 0.06), (-0.32, -0.30), (-0.22, -0.50)],
    "level": [(0.10, -0.60), (-0.20, -0.74), (-0.78, -0.70), (-0.60, -0.58), (-0.40, -0.50), (-0.20, -0.48)],
    "half": [(0.05, -0.62), (-0.20, -1.00), (-0.70, -1.24), (-0.55, -1.00), (-0.42, -0.74), (-0.24, -0.58)],
    "glide": [(0.06, -0.62), (-0.24, -0.92), (-0.80, -1.02), (-0.62, -0.84), (-0.44, -0.66), (-0.22, -0.56)],
    "brake": [(0.04, -0.66), (0.14, -1.26), (-0.10, -1.86), (-0.20, -1.40), (-0.30, -0.94), (-0.22, -0.62)],
}


def pigeon(sh, ox, oy, s, pose, tones):
    """A pigeon with its feet at (ox, oy), facing right. Its far wing (in shade), legs, tail, body, folded or
    spread near wing, neck with its green gleam, head, eye, pale cere and beak."""
    body, wing, dark, gleam = tones[:4]
    leg_c, beak_c, eye_c = tones[4:7] if len(tones) > 4 else ("#c8605a", "#d8c8a8", "#e88838")     # (a bird in the shade has them dimmer)
    shade = mix(body, "#4a4a6a", 0.38)
    p = POSES[pose]
    tilt, lift = p["tilt"], p["lift"]
    hip = (-0.05, -0.40 - lift)                              # the body turns about the hip, after it has been lifted
    P = lambda pts: [(ox + x * s, oy + y * s) for x, y in turned([(x, y - lift) for x, y in pts], hip, tilt)]
    pt = lambda x, y: P([(x, y)])[0]
    w = p["wings"]
    if w != "folded":                                        # the far wing, behind the body, in shade
        far = [(x + 0.10, y - 0.06) for x, y in WINGS[w]]
        sh.poly(P(far), mix(wing, "#52526e", 0.45))
    # legs (pink-red), drawn first so the body sits on them
    lw = max(0.75, s * 0.065)
    kind = p["legs"]
    hipL, hipR = (-0.16, -0.30), (0.06, -0.30)
    feet = {"stand": [(-0.20, 0.0), (0.10, 0.0)], "walk-a": [(-0.28, 0.0), (0.24, 0.0)], "walk-b": [(-0.06, -0.10), (0.06, 0.0)],
            "walk-mid": [(-0.12, 0.0), (0.04, -0.08)], "walk-mid2": [(-0.10, -0.06), (0.10, 0.0)],
            "crouch": [(-0.16, 0.0), (0.12, 0.0)], "dangle": [(-0.22, 0.02), (-0.04, 0.04)], "reach": [(0.10, -0.02), (0.28, -0.06)]}
    if kind in feet:
        for (hx, hy), (fx, fy) in zip((hipL, hipR), feet[kind]):
            a = pt(hx, hy)
            if kind in ("dangle", "reach"):
                b = pt(fx, fy)
            else:
                b = (ox + fx * s, oy + fy * s)                # feet on the ground stay on the ground, whatever the body does
            knee = ((a[0] + b[0]) / 2 + (0.05 * s if kind == "crouch" else 0.0), (a[1] + b[1]) / 2)
            sh.line([a, knee, b], leg_c, lw)
            sh.line([(b[0] - 0.06 * s, b[1]), (b[0] + 0.12 * s, b[1])], leg_c, lw * 0.9)          # the toes
    # tail: dark, with a darker band at its end
    tail_up = 0.06 if kind == "tucked" else 0.0
    tail = [(-0.95, -0.30 - tail_up), (-0.30, -0.62), (-0.20, -0.22)]
    band = [(-0.92, -0.31 - tail_up), (-0.78, -0.27)]
    if kind in ("reach", "crouch"):                          # fanned, and held up off the ground as the body tips up
        tail = turned([(-0.84, -0.42), (-0.30, -0.62), (-0.20, -0.22), (-0.80, -0.16)], (-0.25, -0.42), -tilt * 0.75)
        band = turned([(-0.83, -0.38), (-0.80, -0.20)], (-0.25, -0.42), -tilt * 0.75)
    sh.poly(P(tail), dark)
    sh.line(P(band), mix(dark, "#101018", 0.5), max(0.7, s * 0.07))
    # body: shaded below, lit along the top toward the sun
    c0 = pt(-0.05, -0.47)
    oval(sh, c0[0], c0[1], 0.50 * s, 0.30 * s, tilt, body)
    c1 = pt(-0.03, -0.38)
    oval(sh, c1[0], c1[1], 0.42 * s, 0.17 * s, tilt, mix(body, shade, 0.55))
    c2 = pt(0.02, -0.60)
    oval(sh, c2[0], c2[1], 0.34 * s, 0.10 * s, tilt, mix(body, "#ffffff", 0.16))
    if w == "folded":
        cw = pt(-0.20, -0.50)
        oval(sh, cw[0], cw[1], 0.36 * s, 0.20 * s, tilt, wing)
        sh.line(P([(-0.42, -0.42), (-0.02, -0.36)]), dark, max(0.7, s * 0.07))                     # the two dark bars
        sh.line(P([(-0.50, -0.50), (-0.12, -0.45)]), dark, max(0.7, s * 0.06))
        sh.line(P([(-0.52, -0.56), (-0.26, -0.64)]), mix(wing, "#ffffff", 0.21), max(0.6, s * 0.05))   # the light on the wing's top
    # neck and head
    nb = pt(0.26, -0.55)
    hx, hy = ox + p["head"][0] * s, oy + (p["head"][1] - lift) * s
    sh.line([nb, (hx, hy)], dark, 0.32 * s)
    sh.line([pt(0.31, -0.58), (lerp(nb[0], hx, 0.62), lerp(nb[1], hy, 0.62))], gleam, 0.15 * s)
    if len(tones) <= 4:
        sh.line([pt(0.33, -0.52), (lerp(nb[0], hx, 0.4) + 0.06 * s, lerp(nb[1], hy, 0.4) + 0.04 * s)], mix(dark, "#9a6a9a", 0.6), 0.08 * s)   # and a little purple
    sh.ellipse(hx, hy, 0.17 * s, 0.15 * s, dark)
    d = p["beak"]
    down = 0.12 if pose in (4, 5) else 0.04
    sh.line([(hx + d * 0.11 * s, hy + 0.0 * s), (hx + d * 0.31 * s, hy + down * s)], beak_c, max(0.7, s * 0.075))
    if len(tones) <= 4:
        sh.ellipse(hx + d * 0.13 * s, hy - 0.02 * s, 0.05 * s, 0.04 * s, "#f4f0e4")             # the pale cere
    sh.ellipse(hx + d * 0.02 * s, hy - 0.04 * s, 0.045 * s, 0.045 * s, eye_c)                  # an orange eye
    if w != "folded":                                        # the near wing, spread
        near = WINGS[w]
        lit = mix(wing, "#ffffff", 0.12)
        sh.poly(P(near), lit)
        tip = near[1:4]                                      # the long flight feathers at the end are darker
        sh.poly(P([tip[0], tip[1], tip[2], (lerp(tip[0][0], tip[2][0], 0.5), lerp(tip[0][1], tip[2][1], 0.5))]), mix(wing, dark, 0.55))
        sh.line(P([near[0], near[1]]), mix(lit, "#ffffff", 0.24), max(0.6, s * 0.05))      # its leading edge catches the light
        if w in ("up", "half", "level", "glide", "brake"):
            mid = [(lerp(near[0][0], near[-1][0], 0.5), lerp(near[0][1], near[-1][1], 0.5)), (lerp(near[1][0], near[-2][0], 0.5), lerp(near[1][1], near[-2][1], 0.5))]
            sh.line(P(mid), mix(lit, dark, 0.6), max(0.6, s * 0.05))                             # a wing bar


def pigeon_front(sh, ox, oy, s, tones):
    """The same bird facing us, as it turns round: round breast, the wings close at its sides, head on top."""
    body, wing, dark, gleam = tones[:4]
    leg_c, beak_c, eye_c = tones[4:7] if len(tones) > 4 else ("#c8605a", "#d8c8a8", "#e88838")
    lw = max(0.75, s * 0.065)
    for fx in (-0.09, 0.09):
        sh.line([(ox + fx * s, oy - 0.28 * s), (ox + fx * s, oy)], leg_c, lw)
        sh.line([(ox + (fx - 0.06) * s, oy), (ox + (fx + 0.06) * s, oy)], leg_c, lw * 0.9)
    sh.ellipse(ox, oy - 0.50 * s, 0.33 * s, 0.32 * s, body)
    sh.ellipse(ox - 0.27 * s, oy - 0.52 * s, 0.10 * s, 0.24 * s, mix(wing, "#52526e", 0.4))     # the wing in shade
    sh.ellipse(ox + 0.27 * s, oy - 0.53 * s, 0.10 * s, 0.24 * s, wing)                          # the wing in the sun
    sh.ellipse(ox + 0.02 * s, oy - 0.38 * s, 0.22 * s, 0.14 * s, mix(body, "#4a4a6a", 0.15))
    sh.ellipse(ox + 0.04 * s, oy - 0.62 * s, 0.20 * s, 0.10 * s, mix(body, "#ffffff", 0.12))
    sh.ellipse(ox, oy - 0.78 * s, 0.17 * s, 0.10 * s, gleam)                                    # the gleaming collar
    sh.ellipse(ox, oy - 0.92 * s, 0.15 * s, 0.15 * s, dark)
    sh.poly([(ox - 0.04 * s, oy - 0.88 * s), (ox + 0.04 * s, oy - 0.88 * s), (ox, oy - 0.78 * s)], beak_c)
    for ex in (-0.09, 0.09):
        sh.ellipse(ox + ex * s, oy - 0.95 * s, 0.04 * s, 0.04 * s, eye_c)


def pigeon_shadow(box, s):
    """Soft, cool and see-through: what the pavement does under a pigeon (as land.shadow painted it). -> RGBA"""
    w, h, fx, fy = box
    ss = 4
    yy, xx = np.mgrid[0:h * ss, 0:w * ss] / ss
    cx, cy = fx - 0.75 * s, fy - 0.5
    d = ((xx - cx) / (0.9 * s)) ** 2 + ((yy - cy) / (0.22 * s + 0.6)) ** 2
    a = np.clip(1.3 - d, 0, 1) ** 1.2
    a = a.reshape(h, ss, w, ss).mean(axis=(1, 3)) * 0.42
    out = np.zeros((h, w, 4), np.uint8)
    out[..., :3] = (54, 44, 84)
    out[..., 3] = np.clip(a * 255, 0, 255).astype(np.uint8)
    return out


# ---------------------------------------------------------------- the swallow
def swallow(sh, ox, oy, sz, frame, tone="#34405c"):
    """A swallow high up, as the picture painted them: the two wings spread from a small dark body, the way a bird
    against the sky looks whichever way it is going (so the frames are never mirrored). Wings up, level, down,
    and held in a shallow M to glide."""
    wrist, tip = {1: ((0.42, -0.34), (0.98, -0.80)), 2: ((0.46, -0.12), (1.0, -0.24)),
                  3: ((0.44, 0.06), (0.90, 0.40)), 4: ((0.44, -0.18), (0.96, -0.40))}[frame]
    for d in (-1, 1):
        sh.line([(ox, oy), (ox + d * wrist[0] * sz, oy + wrist[1] * sz)], tone, max(1.25, sz * 0.28))
        sh.line([(ox + d * wrist[0] * sz, oy + wrist[1] * sz), (ox + d * tip[0] * sz, oy + tip[1] * sz)], tone, max(1.05, sz * 0.21))
    sh.ellipse(ox, oy + 0.04 * sz, 0.16 * sz, 0.17 * sz, tone)


# ---------------------------------------------------------------- the hens
HENS = {"hen-white": ("#f4ead8", "#d0c4b8", "#e6dcc8", "#d03a2c"), "hen-brown": ("#a8683a", "#7a4a2a", "#6a3c24", "#c83428")}


def hen(sh, ox, oy, k, frame, tones):
    """A hen from behind, with her feet at (ox, oy): she faces into the picture, up the steps and a little to the
    right, toward the temple doors. Her tail is toward us, her head and comb beyond her back. `k` is pixels per cm."""
    body, shade, tail_c, comb = tones
    shift = {5: -0.9, 6: 0.9}.get(frame, 0.0) * k              # a shuffle: her weight from foot to foot
    big = 1.07 if frame == 7 else 1.0                         # ruffled up
    hx, hy = {1: (5.0, -18.6), 2: (3.0, -18.8), 3: (7.0, -18.2), 4: (5.4, -21.4), 5: (4.4, -18.4), 6: (5.8, -18.4), 7: (5.0, -18.0)}[frame]
    hx, hy = ox + hx * k + shift * 0.5, oy + hy * k
    if frame in (5, 6):                                       # the foot she lifts shows for a moment
        fx = ox + (-3.2 if frame == 5 else 3.2) * k
        sh.line([(fx, oy - 2.6 * k), (fx, oy - 0.4 * k)], "#e0b040", max(0.8, 1.1 * k))
    sh.line([(ox + shift + 3.0 * k, oy - 12.0 * k), (hx, hy + 1.0 * k)], mix(body, shade, 0.25), 4.6 * k)    # her neck,
    sh.ellipse(hx, hy, 4.0 * k, 4.2 * k, mix(body, shade, 0.2))                               # head, beyond the back
    sh.ellipse(hx + (0.0 if frame in (1, 4, 5, 6, 7) else (-0.6 if frame == 2 else 0.6)) * k, hy - 3.9 * k, 2.6 * k, 1.8 * k, comb)    # comb
    if frame == 2:                                            # she turns her head to look with one eye: her beak shows
        sh.poly([(hx - 3.6 * k, hy - 0.4 * k), (hx - 6.4 * k, hy + 0.6 * k), (hx - 3.4 * k, hy + 1.4 * k)], "#e0a030")
        sh.ellipse(hx - 2.6 * k, hy + 2.2 * k, 1.1 * k, 1.5 * k, comb)                       # and her wattle
    if frame == 3:
        sh.poly([(hx + 3.6 * k, hy - 0.4 * k), (hx + 6.4 * k, hy + 0.6 * k), (hx + 3.4 * k, hy + 1.4 * k)], "#e0a030")
        sh.ellipse(hx + 2.6 * k, hy + 2.2 * k, 1.1 * k, 1.5 * k, comb)
    bx, by = ox + shift, oy - 8.4 * k
    oval(sh, bx, by, 9.6 * k * big, 7.8 * k * big, 0.10, body)                               # her body,
    oval(sh, bx - 2.2 * k, by + 2.0 * k, 7.0 * k * big, 5.2 * k * big, 0.10, mix(body, shade, 0.45))     # the side away from the sun,
    oval(sh, bx + 2.6 * k, by - 3.6 * k, 5.6 * k, 2.6 * k, 0.25, mix(body, "#ffffff", 0.14))   # her back in the sun
    tl = [(bx - 4.6 * k, by + 1.0 * k), (bx - 8.8 * k, by - 9.6 * k), (bx - 5.0 * k, by - 11.4 * k), (bx - 1.0 * k, by - 3.6 * k)]
    if frame == 7:
        tl = [(x, y - 1.0 * k) for x, y in tl]
    sh.poly(tl, tail_c)                                       # and her tail toward us, standing up
    sh.line([tl[1], tl[3]], mix(tail_c, shade, 0.4), max(0.6, 0.8 * k))


# ---------------------------------------------------------------- painting them all
def frame_of(box, draw, palette, ss=4):
    """Draw one frame on a clear sheet the frame's size, finish it -> (index, alpha)."""
    w, h, fx, fy = box
    sh = Sheet((h, w), ss=ss)
    draw(sh, fx, fy)
    c, a = sh.done()
    return finish_frame(c, a, palette)


def flock_frames(name, box=PIGEON_BOX, size_at=None):
    """A pigeon set (or a sparrow's) as the engine's flock takes it (briefs/out/fx-4-ready.md): lists of files by what
    the bird is doing, its foot point, which way it faces as painted, and the row where it is the right size."""
    f = lambda ns: [f"{name}-{n}.png" for n in ns]
    spec = {"foot": [box[2], box[3]], "face": "E", "stand": f([1, 3]), "look": f([2]), "peck": f([4, 5]), "walk": f([6, 7, 8, 9]),
            "turn": f([10]), "fly": f([13, 14, 15]), "land": f([18])}
    if size_at:
        spec["sizeAt"] = size_at
    return spec


def flyer_frames(name, box=SWALLOW_BOX):
    """The swallows as the engine's flyers take them: the wingbeat, the glide, the point that flies along the lane."""
    return {"flap": [f"{name}-{n}.png" for n in (1, 2, 3, 2)], "glide": f"{name}-4.png", "middle": [box[2], box[3]]}


def hen_frames(name):
    """A hen as the engine's flock takes it: she stands (her head now neutral, now turned, now up, now ruffled), looks
    with one eye, shuffles; never pecks, never turns round, never flies."""
    f = lambda ns: [f"{name}-{n}.png" for n in ns]
    return {"foot": [HEN_BOX[2], HEN_BOX[3]], "face": "E", "stand": f([1, 3, 1, 4, 1, 7]), "look": f([2]), "walk": f([5, 6])}


def box_for(box, f):
    """A frame box (w, h, foot x, foot y) for birds painted f times the size."""
    w, h, fx, fy = box
    return (int(math.ceil(w * f)), int(math.ceil(h * f)), int(round(fx * f)), int(round(fy * f)))


def pigeon_frames(out, name, palette, s, tones, box):
    """The 18 frames of a pigeon (or any bird drawn the same way: a sparrow), `s` its size, into `out`/name-<n>.png."""
    files = []
    for n in range(1, 19):
        if n == 10:
            draw = lambda sh, fx, fy: pigeon_front(sh, fx, fy, s, tones)
        else:
            draw = lambda sh, fx, fy, n=n: pigeon(sh, fx, fy, s, n, tones)
        idx, a = frame_of(box, draw, palette, ss=4 if s > 10 else 6)
        save(f"{out}/{name}-{n}.png", idx, palette, a)
        files.append(f"{name}-{n}.png")
    return files


def swallow_frames(out, name, palette, sz, tone, box):
    files = []
    for n in range(1, 5):
        idx, a = frame_of(box, lambda sh, fx, fy, n=n: swallow(sh, fx, fy, sz, n, tone), palette, ss=6)
        save(f"{out}/{name}-{n}.png", idx, palette, a)
        files.append(f"{name}-{n}.png")
    return files


def paint(out, palette, hen_k):
    """Every frame, into the folder `out`. `hen_k`: pixels per cm on the step where the hens' cage stands.
    -> {set: [file names]}"""
    os.makedirs(out, exist_ok=True)
    made = {}
    clear = len(palette)
    for name, tones in PIGEONS.items():
        made[name] = []
        for n in range(1, 19):
            if n == 10:
                draw = lambda sh, fx, fy: pigeon_front(sh, fx, fy, S, tones)
            else:
                draw = lambda sh, fx, fy, n=n: pigeon(sh, fx, fy, S, n, tones)
            idx, a = frame_of(PIGEON_BOX, draw, palette)
            save(f"{out}/{name}-{n}.png", idx, palette, a)
            made[name].append(f"{name}-{n}.png")
    Image.fromarray(pigeon_shadow(PIGEON_BOX, S), "RGBA").save(f"{out}/pigeon-shadow-1.png", optimize=True)
    made["pigeon-shadow"] = ["pigeon-shadow-1.png"]
    made["swallow"] = []
    for n in range(1, 5):
        idx, a = frame_of(SWALLOW_BOX, lambda sh, fx, fy, n=n: swallow(sh, fx, fy, 5.0, n), palette, ss=6)
        save(f"{out}/swallow-{n}.png", idx, palette, a)
        made["swallow"].append(f"swallow-{n}.png")
    for name, tones in HENS.items():
        made[name] = []
        for n in range(1, 8):
            idx, a = frame_of(HEN_BOX, lambda sh, fx, fy, n=n: hen(sh, fx, fy, hen_k * (1.0 if name == "hen-white" else 0.94), n, tones), palette, ss=6)
            save(f"{out}/{name}-{n}.png", idx, palette, a)
            made[name].append(f"{name}-{n}.png")
    return made


def sheet(out, made, palette, path, zoom=4):
    """All the frames side by side, enlarged, on the pavement's colour, each with its foot point marked."""
    rows = []
    for name, files in made.items():
        ims = [Image.open(f"{out}/{f}").convert("RGBA") for f in files]
        w = sum(im.width + 3 for im in ims)
        h = max(im.height for im in ims)
        row = Image.new("RGBA", (w, h), (226, 206, 160, 255))
        x = 0
        for im in ims:
            row.alpha_composite(im, (x, 0))
            x += im.width + 3
        rows.append(row)
    W_ = max(r.width for r in rows)
    H_ = sum(r.height + 4 for r in rows)
    big = Image.new("RGBA", (W_, H_), (90, 90, 110, 255))
    y = 0
    for r in rows:
        big.alpha_composite(r, (0, y))
        y += r.height + 4
    big = big.resize((W_ * zoom, H_ * zoom), Image.NEAREST)
    big.convert("RGB").save(path)


if __name__ == "__main__":
    import rome_steps as R
    from rome_steps_palette import PALETTE
    cu0, cu1, ck = R.CAGE
    made = paint(R.OUT, PALETTE, R.T.k((cu0 + cu1) / 2, R.VK(ck)))
    os.makedirs("out/rome-steps-4-work", exist_ok=True)
    sheet(R.OUT, made, PALETTE, "out/rome-steps-4-work/frames.png")
    print({k: len(v) for k, v in made.items()})

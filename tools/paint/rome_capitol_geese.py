"""The sacred geese of Juno on the Capitol, painted as frames for the game to move (rome-capitol, layout.json "frames").

White farmyard geese, a little grey on the back and wings, orange bills and feet, painted in the game's manner for
things that move (as its people are drawn): a dark line round them, flat colours with one darker tone, the light from
the upper left; hard edges. Painted at their size where a person is 160 px tall (sizeAt 590): a goose standing with
its neck up is about 65 cm, 59 px. Every frame is on one canvas, with the feet at one foot point, facing E (the engine
turns them round for W).

  goose-<n>.png        the white geese          goose-grey-<n>.png   a greyer one (a second colouring, the same frames)
    1, 2    stand      a breath, and a blink
    3, 4    look       the neck stretched out low and forward, the bill open: hissing, the wings held a little out
    5 to 8  walk       a waddle, one foot and then the other
    9 to 12 run        running with the wings half open, the neck stretched out
    13      turn       facing us
    14, 15  peck       the bill to the ground
    16, 17  flap       standing, the wings up and spread (16 high, 17 half down)

  python3 rome_capitol_geese.py      paints the frames into out/rome-capitol/ and lays them on a sheet to look at
                                     (out/rome-capitol-geese-sheet.png, 4x, the foot point marked; and the run as a strip,
                                     out/rome-capitol-geese-run.png). rome_capitol.py calls paint_all() itself."""

import math
import os

import numpy as np
from PIL import Image

from brush import F32, Sheet

BOX = (116, 104, 54, 98)                 # frame width, height; the foot point (x, y) in it
S = 160.0 / 175.0                        # pixels per cm at row 590 (sizeAt)
SETS = {
    #            body       shade      back/wing  wing dark  bill       bill dark  leg        line
    "goose":      ("#f8f4ea", "#c9c4d4", "#e2e0e4", "#a9a6b8", "#f08c28", "#b8581a", "#f0962e", "#2c2a3c"),
    "goose-grey": ("#ece8e0", "#b9b4c4", "#a8a2a0", "#77727a", "#f08c28", "#b8581a", "#f0962e", "#2a2832"),
}
ACTS = {"stand": [1, 2], "look": [3, 4], "walk": [5, 6, 7, 8], "run": [9, 10, 11, 12], "turn": [13], "peck": [14, 15], "flap": [16, 17]}


def rot(points, pivot, ang):
    """Turn points (cm, y up) about a pivot by ang radians (+ lifts what is ahead of the pivot)."""
    px, py = pivot
    ca, sa = math.cos(ang), math.sin(ang)
    return [(px + (x - px) * ca - (y - py) * sa, py + (x - px) * sa + (y - py) * ca) for x, y in points]


def oval(cx, cy, rx, ry, ang=0.0, n=36):
    pts = [(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in np.linspace(0, 2 * math.pi, n, endpoint=False)]
    return rot(pts, (cx, cy), ang) if ang else pts


def tube(path, w0, w1):
    """A neck: an outline round a path (cm), w0 wide at its start and w1 at its end."""
    left, right = [], []
    for i, (x, y) in enumerate(path):
        a = path[max(0, i - 1)]
        b = path[min(len(path) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        w = (w0 + (w1 - w0) * i / (len(path) - 1)) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1]


def bez(p0, p1, p2, n=10):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in np.linspace(0, 1, n)]


POSES = {
    #    body tilt (rad, + raises the breast), lift (cm), neck path (three points: base, bend, head), head angle, bill open,
    #    wings ("fold", "out", "half", "up", "spread"), legs: (near foot x, lift), (far foot x, lift)
    1: dict(tilt=0.06, lift=0.0, neck=((18, 38), (22, 52), (31, 62)), head=0.05, bill=0.0, wings="fold", legs=((5, 0), (-3, 0)), eye=True),
    2: dict(tilt=0.07, lift=0.6, neck=((18, 38), (22, 53), (31, 63)), head=0.05, bill=0.0, wings="fold", legs=((5, 0), (-3, 0)), eye=False),
    3: dict(tilt=-0.10, lift=-1.0, neck=((18, 34), (34, 30), (50, 26)), head=-0.10, bill=0.55, wings="out", legs=((7, 0), (-6, 0)), eye=True),
    4: dict(tilt=-0.14, lift=-1.5, neck=((18, 32), (36, 26), (54, 21)), head=-0.18, bill=0.85, wings="out", legs=((8, 0), (-7, 0)), eye=True),
    5: dict(tilt=0.03, lift=0.4, neck=((18, 38), (25, 51), (34, 61)), head=0.0, bill=0.0, wings="fold", legs=((12, 0), (-6, 3)), eye=True),
    6: dict(tilt=0.06, lift=1.2, neck=((18, 38), (23, 52), (32, 62)), head=0.05, bill=0.0, wings="fold", legs=((4, 2), (2, 0)), eye=True),
    7: dict(tilt=0.03, lift=0.4, neck=((18, 38), (25, 51), (34, 61)), head=0.0, bill=0.0, wings="fold", legs=((-5, 3), (11, 0)), eye=True),
    8: dict(tilt=0.06, lift=1.2, neck=((18, 38), (23, 52), (32, 62)), head=0.05, bill=0.0, wings="fold", legs=((2, 0), (4, 2)), eye=True),
    9: dict(tilt=-0.16, lift=4.0, neck=((18, 36), (32, 40), (46, 44)), head=-0.05, bill=0.35, wings="half", legs=((16, 2), (-12, 7)), eye=True),
    10: dict(tilt=-0.12, lift=7.0, neck=((18, 36), (33, 41), (47, 46)), head=-0.02, bill=0.35, wings="half2", legs=((4, 8), (2, 4)), eye=True),
    11: dict(tilt=-0.16, lift=4.0, neck=((18, 36), (32, 40), (46, 44)), head=-0.05, bill=0.35, wings="half", legs=((-12, 7), (16, 2)), eye=True),
    12: dict(tilt=-0.12, lift=7.0, neck=((18, 36), (33, 41), (47, 46)), head=-0.02, bill=0.35, wings="half2", legs=((2, 4), (4, 8)), eye=True),
    14: dict(tilt=-0.20, lift=-1.0, neck=((18, 32), (36, 22), (40, 6)), head=-1.15, bill=0.0, wings="fold", legs=((6, 0), (-4, 0)), eye=True),
    15: dict(tilt=-0.22, lift=-1.2, neck=((18, 31), (36, 20), (42, 3)), head=-1.30, bill=0.2, wings="fold", legs=((6, 0), (-4, 0)), eye=True),
    16: dict(tilt=0.30, lift=1.0, neck=((16, 40), (18, 56), (24, 68)), head=0.35, bill=0.7, wings="up", legs=((4, 0), (-4, 0)), eye=True),
    17: dict(tilt=0.24, lift=0.6, neck=((16, 40), (19, 55), (26, 66)), head=0.30, bill=0.5, wings="spread", legs=((4, 0), (-4, 0)), eye=True),
}

WING = {   # the near wing's outline from the shoulder, in cm, before the body is turned (the folded wing lies along the side)
    "fold": [(12, 38), (4, 41), (-14, 40), (-30, 36), (-38, 33), (-30, 29), (-12, 28), (6, 30)],
    "out": [(12, 39), (2, 46), (-16, 47), (-32, 43), (-41, 38), (-31, 33), (-12, 33), (6, 33)],
    "half": [(10, 40), (2, 54), (-10, 66), (-30, 72), (-46, 68), (-36, 58), (-26, 48), (-10, 40)],
    "half2": [(10, 40), (4, 50), (-8, 58), (-28, 62), (-46, 56), (-34, 50), (-22, 44), (-8, 38)],
    "up": [(10, 42), (14, 62), (8, 86), (-6, 100), (-14, 96), (-12, 76), (-14, 56), (-4, 44)],
    "spread": [(10, 42), (18, 56), (12, 66), (-10, 72), (-40, 74), (-52, 66), (-30, 56), (-6, 44)],
}


def goose(sh, ox, oy, pose, tones, k):
    """One goose with its feet at (ox, oy) (sheet pixels), facing right, k sheet pixels per cm."""
    body, shade, back, wingd, bill, billd, leg, line = tones
    p = POSES[pose]
    tilt, lift = p["tilt"], p["lift"]
    hip = (0.0, 26.0)
    T = lambda pts: [(ox + x * k, oy - (y + lift) * k) for x, y in rot(pts, hip, tilt)]
    Tf = lambda pts: [(ox + x * k, oy - y * k) for x, y in pts]          # (feet stay on the ground)
    # the far wing, when it is open, behind everything, darker
    w = p["wings"]
    if w in ("half", "half2", "up", "spread"):
        far = [(x - 6, y + (8 if w in ("up",) else 4)) for x, y in WING[w]]
        sh.poly(T(far), wingd)
    # legs: orange, from the body to the webbed feet
    for (fx, fl), near in ((p["legs"][1], False), (p["legs"][0], True)):
        top = T([(2 if near else -2, 22)])[0]
        foot = Tf([(fx, fl)])[0]
        knee = ((top[0] + foot[0]) / 2 + 1.5 * k, (top[1] + foot[1]) / 2)
        sh.line([top, knee, foot], leg if near else billd, 2.6 * k)
        sh.poly(Tf([(fx - 3, fl), (fx + 7, fl - 0.5), (fx + 6, fl + 1.6), (fx - 2, fl + 2.0)]), leg if near else billd)    # the webbed foot
    # the body: white, its belly and the side away from the light in the darker tone
    sh.poly(T(oval(-4, 30, 30, 15.5, 0.04)), body)
    sh.poly(T([(-24, 34), (-38, 33), (-45, 39), (-42, 43), (-28, 42)]), body)                         # the tail, cocked up
    sh.poly(T([(-30, 22), (-12, 15.5), (10, 16.5), (22, 22), (14, 20), (-10, 19.5), (-28, 25)]), shade)  # the belly in shade
    sh.poly(T([(-38, 33), (-45, 39), (-40, 36)]), shade)
    # the neck and the head
    n0, n1, n2 = p["neck"]
    path = bez(n0, n1, n2, 12)
    sh.poly(T(tube(path, 13.0, 8.5)), body)
    sh.poly(T([(path[i][0] + 2.5, path[i][1] - 2.0) for i in range(len(path))] + [(path[i][0] + 4.2, path[i][1] - 3.0) for i in reversed(range(len(path)))]), shade)
    hx, hy = n2
    ha = p["head"]
    head = oval(hx + 2, hy, 7.4, 5.2, ha)
    sh.poly(T(head), body)
    # the bill: upper and lower, open by `bill`, a dark nail at the tip
    o = p["bill"]
    tip = rot([(hx + 16.5, hy - 0.6)], (hx + 2, hy), ha)[0]
    root_u, root_l = rot([(hx + 6.0, hy + 2.8)], (hx + 2, hy), ha)[0], rot([(hx + 6.0, hy - 2.4)], (hx + 2, hy), ha)[0]
    up_tip = rot([tip], (hx + 6, hy), o * 0.30)[0]
    lo_tip = rot([tip], (hx + 6, hy), -o * 0.45)[0]
    mid_ = rot([(hx + 6.5, hy + 0.2)], (hx + 2, hy), ha)[0]
    if o > 0.05:
        sh.poly(T([mid_, up_tip, lo_tip]), "#b84a5a")                                                  # the inside of the open bill
        sh.line(T([mid_, ((up_tip[0] + lo_tip[0]) / 2, (up_tip[1] + lo_tip[1]) / 2)]), "#e88a9a", 1.6 * k)   # the tongue
    sh.poly(T([root_u, up_tip, mid_]), bill)
    sh.poly(T([mid_, lo_tip, root_l]), billd)
    sh.ellipse(*T([up_tip])[0], 1.3 * k, 1.1 * k, line)                                              # the nail
    ex, ey = rot([(hx + 2.6, hy + 1.4)], (hx + 2, hy), ha)[0]
    if p["eye"]:
        sh.ellipse(*T([(ex, ey)])[0], 1.15 * k, 1.15 * k, line)
    else:
        sh.line(T([(ex - 1.3, ey), (ex + 1.3, ey)]), line, 0.9 * k)
    # the near wing: grey-white, its long feathers darker
    wpts = WING[w]
    sh.poly(T(wpts), back)
    prim = wpts[2:6] if w in ("fold", "out") else wpts[3:7]
    sh.poly(T(prim + [((prim[0][0] + prim[-1][0]) / 2 + 2, (prim[0][1] + prim[-1][1]) / 2)]), wingd)
    if w in ("fold", "out"):
        for j in range(3):                                                                           # feather edges
            a = (wpts[1][0] - 4 - j * 9, wpts[1][1] - 2 - j * 0.5)
            b = (a[0] - 7, a[1] - 5)
            sh.line(T([a, b]), wingd, 0.9 * k)


def goose_front(sh, ox, oy, tones, k):
    """Facing us, as it turns: the round breast, the wings close at its sides, the neck up, the bill toward us."""
    body, shade, back, wingd, bill, billd, leg, line = tones
    T = lambda pts: [(ox + x * k, oy - y * k) for x, y in pts]
    for fx in (-6, 6):
        sh.line(T([(fx, 22), (fx * 1.1, 2)]), leg, 2.6 * k)
        sh.poly(T([(fx * 1.1 - 4.5, 0), (fx * 1.1 + 4.5, 0), (fx * 1.1 + 3, 2.5), (fx * 1.1 - 3, 2.5)]), leg)
    sh.poly(T(oval(0, 30, 17, 16)), body)
    sh.poly(T(oval(-13, 31, 6, 12)), back)                                                          # the wings at its sides
    sh.poly(T(oval(13, 31, 6, 12)), wingd)
    sh.poly(T([(-14, 20), (0, 15), (14, 20), (8, 18), (-8, 18)]), shade)
    sh.poly(T(tube([(0, 40), (0.6, 52), (0, 62)], 11, 8)), body)
    sh.poly(T([(2.5, 40), (3.5, 52), (2.5, 62), (4, 62), (5, 52), (4, 40)]), shade)
    sh.poly(T(oval(0, 64, 5, 5)), body)
    sh.poly(T([(-2.4, 63), (2.4, 63), (1.6, 57.5), (-1.6, 57.5)]), bill)                         # the bill, pointing at us
    sh.poly(T([(0, 63), (2.4, 63), (1.6, 57.5), (0, 57.5)]), billd)
    for ex in (-3.2, 3.2):
        sh.ellipse(*T([(ex, 65.5)])[0], 1.0 * k, 1.0 * k, line)


def frame(n, tones, ss=4):
    """One frame: drawn at ss times, cut to hard edges and flat colours, the dark line laid round it. -> RGBA uint8."""
    w, h, fx, fy = BOX
    sh = Sheet((h * ss, w * ss), ss=1)
    k = S * ss
    if n == 13:
        goose_front(sh, fx * ss, fy * ss, tones, k)
    else:
        goose(sh, fx * ss, fy * ss, n, tones, k)
    c, a = sh.done()
    # down to the frame's size: each pixel takes the colour most of it has, hard edged
    c4 = c.reshape(h, ss, w, ss, 3)
    a4 = a.reshape(h, ss, w, ss)
    alpha = a4.mean(axis=(1, 3)) > 0.5
    cols = np.array([np.array([int(t[i:i + 2], 16) for i in (1, 3, 5)]) / 255.0 for t in tones] + [[0.72, 0.29, 0.35], [0.91, 0.54, 0.60]], F32)
    sub = c4.transpose(0, 2, 1, 3, 4).reshape(h, w, ss * ss, 3)
    subw = a4.transpose(0, 2, 1, 3).reshape(h, w, ss * ss)
    d = ((sub[..., None, :] - cols[None, None, None, :, :]) ** 2).sum(-1)                  # every sub-pixel to its nearest flat colour
    near = d.argmin(-1)
    votes = np.zeros((h, w, len(cols)), F32)
    for j in range(len(cols)):
        votes[..., j] = ((near == j) * subw).sum(-1)
    idx = votes.argmax(-1)
    rgb = cols[idx]
    # the dark line round it, where it is more than a sliver thick (legs, bill and the like keep their colour)
    from scipy import ndimage
    inner = ndimage.binary_erosion(alpha, structure=np.ones((3, 3), bool), border_value=0)
    edge = alpha & ~inner
    thin = np.isin(idx, [4, 5, 6, 8, 9])                         # bill, its dark, legs, the inside of the bill, tongue
    rgb = np.where((edge & ~thin)[..., None], cols[7], rgb)
    out = np.zeros((h, w, 4), np.uint8)
    out[..., :3] = np.clip(np.round(rgb * 255), 0, 255).astype(np.uint8)
    out[..., 3] = np.where(alpha, 255, 0).astype(np.uint8)
    return out


def save_frame(path, rgba):
    """As a palette PNG with one clear colour (the game's frames are palette pictures)."""
    im = Image.fromarray(rgba, "RGBA")
    q = im.convert("RGB").quantize(colors=15, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()[:15 * 3]
    idx = np.asarray(q).copy()
    idx[rgba[..., 3] == 0] = 15
    out = Image.fromarray(idx.astype(np.uint8), "P")
    out.putpalette(pal + [0, 0, 0] * (256 - 15))
    out.save(path, optimize=True, transparency=15)


def paint_all(out, palette=None):
    """Every frame of both colourings into `out`. -> {set: [file names]}"""
    os.makedirs(out, exist_ok=True)
    made = {}
    for name, tones in SETS.items():
        made[name] = []
        for n in range(1, 18):
            f = f"{name}-{n}.png"
            save_frame(f"{out}/{f}", frame(n, tones))
            made[name].append(f)
    return made


def frames_block():
    """The frames as the engine's flock takes them (layout.json "frames", and the fx mark of the geese)."""
    f = lambda ns: [f"goose-{n}.png" for n in ns]
    return {"set": "goose", "foot": [BOX[2], BOX[3]], "face": "E", "sizeAt": 590,
            "stand": f(ACTS["stand"]), "look": f(ACTS["look"]), "walk": f(ACTS["walk"]), "run": f(ACTS["run"]), "turn": f(ACTS["turn"]),
            "peck": f(ACTS["peck"]), "flap": f(ACTS["flap"])}


def sheet(out, made, path, zoom=4):
    """Every frame side by side on the paving's colour, 4x, the foot point marked; one row a colouring."""
    rows = []
    for name, files in made.items():
        ims = [Image.open(f"{out}/{f}").convert("RGBA") for f in files]
        wsum = sum(im.width + 4 for im in ims)
        row = Image.new("RGBA", (wsum, BOX[1] + 14), (226, 210, 176, 255))
        x = 0
        for im in ims:
            row.alpha_composite(im, (x, 0))
            px = row.load()
            for d in range(-3, 4):
                for (xx, yy) in ((x + BOX[2] + d, BOX[3]), (x + BOX[2], BOX[3] + d)):
                    if 0 <= xx < row.width and 0 <= yy < row.height:
                        px[xx, yy] = (220, 30, 30, 255)
            x += im.width + 4
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


def run_strip(out, path, zoom=3):
    """The run as a strip: the four frames one after another, moving along, as the engine shows them."""
    ims = [Image.open(f"{out}/goose-{n}.png").convert("RGBA") for n in (9, 10, 11, 12, 9, 10, 11, 12)]
    strip = Image.new("RGBA", (BOX[0] + 7 * 34 + 10, BOX[1] + 6), (226, 210, 176, 255))
    for i, im in enumerate(ims):
        strip.alpha_composite(im, (5 + i * 34, 3))
    strip.resize((strip.width * zoom, strip.height * zoom), Image.NEAREST).convert("RGB").save(path)


if __name__ == "__main__":
    OUT = "out/rome-capitol"
    made = paint_all(OUT)
    sheet(OUT, made, "out/rome-capitol-geese-sheet.png")
    run_strip(OUT, "out/rome-capitol-geese-run.png")
    print({k: len(v) for k, v in made.items()})

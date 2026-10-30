"""The herons in the inner moat at Himeji, painted as frames for the game to move (edo-castle, layout.json "frames").
PAINT-20D, round twenty.

Grey herons (heron-<n>) and white egrets (egret-<n>): the same frames in two colourings, in the game's manner for things
that move (as its people are drawn, and as the Capitol's geese were): flat colours, one darker tone, a dark line round
them, hard edges. Facing E (the engine turns them for W). Painted at their size where a person is 160 px tall (sizeAt
590): a grey heron standing with its neck up is about 95 cm, 87 px; the egret is the same drawing a little smaller.
Every frame on one canvas with the feet at one foot point. The design: every heron faces the top of the keep.

    1, 2    stand     still, the neck up; a blink
    3, 4    look      the neck stretched up and the head turned up: looking at the top of the keep
    5 to 8  walk      stalking a step, slow, one foot lifted and set down, then the other
    9, 10   peck      the strike: the neck drawn back, then shot down at the water
    11      turn      facing us, the neck up

  python3 edo_castle_herons.py      paints the frames into out/edo-castle/ and a sheet to look at (out/edo-castle-herons-sheet.png)
                                    edo_castle.py calls paint_all() itself."""

import math
import os

import numpy as np
from PIL import Image

from brush import F32, Sheet

BOX = (100, 104, 48, 98)                  # frame width, height; the foot point (x, y) in it
S = 160.0 / 175.0                         # pixels per cm at row 590 (sizeAt)
SETS = {
    #           body       shade      wing       wing dark  bill       bill dark  leg        line       crest
    "heron":   ("#b9bcc4", "#8d93a4", "#7d8494", "#56607a", "#e2b25a", "#9c7a3a", "#5a5a52", "#262a3c", "#30364a"),
    "egret":   ("#f6f3ea", "#c8c6d6", "#e8e6e4", "#b4b2c4", "#e2b25a", "#9c7a3a", "#2e2e30", "#2a2a3a", "#f6f3ea"),
}
ACTS = {"stand": [1, 2], "look": [3, 4], "walk": [5, 6, 7, 8], "peck": [9, 10], "turn": [11]}
SIZE = {"heron": 1.0, "egret": 0.86}


def bez(p0, p1, p2, n=12):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in np.linspace(0, 1, n)]


def tube(path, w0, w1):
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


def oval(cx, cy, rx, ry, ang=0.0, n=32):
    pts = []
    ca, sa = math.cos(ang), math.sin(ang)
    for t in np.linspace(0, 2 * math.pi, n, endpoint=False):
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


POSES = {
    #   body: (centre x, centre y, tilt); neck: (base, bend, head) in cm; head angle (rad, + is up); legs: (near x, lift), (far x, lift)
    1: dict(body=(-4, 46, 0.10), neck=((10, 58), (14, 76), (12, 88)), head=0.0, legs=((3, 0), (-4, 0)), eye=True),
    2: dict(body=(-4, 46, 0.10), neck=((10, 58), (14, 76), (12, 88)), head=0.0, legs=((3, 0), (-4, 0)), eye=False),
    3: dict(body=(-4, 47, 0.16), neck=((10, 60), (16, 80), (16, 94)), head=0.55, legs=((3, 0), (-4, 0)), eye=True),
    4: dict(body=(-4, 48, 0.20), neck=((10, 61), (17, 82), (18, 97)), head=0.75, legs=((3, 0), (-4, 0)), eye=True),
    5: dict(body=(-2, 45, 0.04), neck=((12, 56), (22, 66), (26, 80)), head=-0.15, legs=((10, 6), (-6, 0)), eye=True),
    6: dict(body=(0, 45, 0.02), neck=((12, 56), (22, 66), (26, 80)), head=-0.15, legs=((12, 0), (-6, 0)), eye=True),
    7: dict(body=(2, 45, 0.04), neck=((12, 56), (22, 66), (26, 80)), head=-0.15, legs=((4, 0), (0, 6)), eye=True),
    8: dict(body=(4, 45, 0.02), neck=((12, 56), (22, 66), (26, 80)), head=-0.15, legs=((2, 0), (6, 0)), eye=True),
    9: dict(body=(-4, 44, -0.06), neck=((10, 54), (0, 68), (10, 74)), head=-0.6, legs=((3, 0), (-4, 0)), eye=True),
    10: dict(body=(-2, 40, -0.30), neck=((12, 48), (30, 30), (40, 8)), head=-1.25, legs=((3, 0), (-4, 0)), eye=True),
}


def heron(sh, ox, oy, pose, tones, k):
    """One heron with its feet at (ox, oy) (sheet pixels), facing right, k sheet pixels per cm."""
    body, shade, wing, wingd, bill, billd, leg, line, crest = tones
    p = POSES[pose]
    T = lambda pts: [(ox + x * k, oy - y * k) for x, y in pts]
    bx, by, tilt = p["body"]
    # the legs: long, thin, a knee bent backward; the far one darker
    for (fx, fl), near in ((p["legs"][1], False), (p["legs"][0], True)):
        hip = (bx + (3 if near else -1), by - 10)
        knee = ((hip[0] + fx) / 2 - 2, (hip[1] + fl) / 2 + 2)
        sh.line(T([hip, knee, (fx, fl)]), leg if near else billd, 1.8 * k)
        sh.line(T([(fx - 4, fl), (fx + 5, fl)]), leg if near else billd, 1.3 * k)                 # the toes
        sh.line(T([(fx, fl), (fx + 2, fl + 2.5)]), leg if near else billd, 1.1 * k)
    # the body: an oval, the back and the folded wing darker, the breast lighter
    sh.poly(T(oval(bx, by, 22, 11, -tilt)), body)
    sh.poly(T(oval(bx - 4, by + 3, 18, 7, -tilt - 0.08)), wing)
    sh.poly(T(oval(bx - 10, by + 4, 10, 4, -tilt - 0.1)), wingd, 0.8)
    sh.poly(T([(bx - 22, by + 2), (bx - 34, by - 2), (bx - 36, by + 4), (bx - 26, by + 7)]), wingd)           # the tail, short
    sh.poly(T(oval(bx + 6, by - 4, 11, 6, -tilt)), shade)                                                     # the breast's shade under the neck
    # the neck: an S, the head, the long bill
    n0, n1, n2 = p["neck"]
    path = bez(n0, n1, n2, 14)
    sh.poly(T(tube(path, 9.0, 6.0)), body)
    sh.poly(T([(q[0] - 2.2, q[1]) for q in path] + [(q[0] - 3.6, q[1]) for q in reversed(path)]), shade)   # its back edge in shade
    hx, hy = n2
    ha = p["head"]
    ca, sa = math.cos(ha), math.sin(ha)
    R = lambda x, y: (hx + x * ca - y * sa, hy + x * sa + y * ca)
    sh.poly(T([R(x, y) for x, y in oval(2, 0, 6.5, 4.6)]), body)
    sh.poly(T([R(6, 1.8), R(24, 0.4), R(6, -1.6)]), bill)                                                  # the bill: long, a dagger
    sh.poly(T([R(6, -1.6), R(24, 0.4), R(6, -2.6)]), billd)
    sh.poly(T([R(-2, 3.2), R(-9, 5.5), R(-10, 3.8), R(-3, 1.6)]), crest)                                    # the crest off the back of the head
    ex, ey = R(3.2, 1.4)
    if p["eye"]:
        sh.ellipse(*T([(ex, ey)])[0], 1.0 * k, 1.0 * k, line)
        sh.ellipse(*T([(ex, ey)])[0], 0.5 * k, 0.5 * k, bill)
    else:
        sh.line(T([(ex - 1.1, ey), (ex + 1.1, ey)]), line, 0.8 * k)
    sh.line(T([R(-1, 2.6), R(5, 1.2)]), line, 0.7 * k)                                                      # the dark stripe over the eye


def heron_front(sh, ox, oy, tones, k):
    """Facing us, as it turns: the breast, the neck up, the bill toward us."""
    body, shade, wing, wingd, bill, billd, leg, line, crest = tones
    T = lambda pts: [(ox + x * k, oy - y * k) for x, y in pts]
    for fx in (-4, 4):
        sh.line(T([(fx, 36), (fx * 1.2, 0)]), leg, 1.8 * k)
        sh.line(T([(fx * 1.2 - 4, 0), (fx * 1.2 + 4, 0)]), leg, 1.3 * k)
    sh.poly(T(oval(0, 46, 12, 12)), body)
    sh.poly(T(oval(-9, 47, 4, 10)), wing)
    sh.poly(T(oval(9, 47, 4, 10)), wingd)
    sh.poly(T(oval(0, 40, 7, 5)), shade)
    sh.poly(T(tube([(0, 56), (0.6, 72), (0, 86)], 8, 6)), body)
    sh.poly(T([(1.8, 56), (2.6, 72), (1.8, 86), (3.2, 86), (4.0, 72), (3.2, 56)]), shade)
    sh.poly(T(oval(0, 88, 4.6, 4.6)), body)
    sh.poly(T([(-1.8, 87), (1.8, 87), (0.9, 80), (-0.9, 80)]), bill)
    sh.poly(T([(0, 87), (1.8, 87), (0.9, 80), (0, 80)]), billd)
    for ex in (-2.6, 2.6):
        sh.ellipse(*T([(ex, 89.5)])[0], 0.9 * k, 0.9 * k, line)


def frame(n, tones, size=1.0, ss=4):
    """One frame: drawn at ss times, cut to hard edges and flat colours, the dark line laid round it. -> RGBA uint8"""
    w, h, fx, fy = BOX
    sh = Sheet((h * ss, w * ss), ss=1)
    k = S * ss * size
    if n == 11:
        heron_front(sh, fx * ss, fy * ss, tones, k)
    else:
        heron(sh, fx * ss, fy * ss, n, tones, k)
    c, a = sh.done()
    c4 = c.reshape(h, ss, w, ss, 3)
    a4 = a.reshape(h, ss, w, ss)
    alpha = a4.mean(axis=(1, 3)) > 0.5
    cols = np.array([np.array([int(t[i:i + 2], 16) for i in (1, 3, 5)]) / 255.0 for t in tones], F32)
    sub = c4.transpose(0, 2, 1, 3, 4).reshape(h, w, ss * ss, 3)
    subw = a4.transpose(0, 2, 1, 3).reshape(h, w, ss * ss)
    d = ((sub[..., None, :] - cols[None, None, None, :, :]) ** 2).sum(-1)
    near = d.argmin(-1)
    votes = np.zeros((h, w, len(cols)), F32)
    for j in range(len(cols)):
        votes[..., j] = ((near == j) * subw).sum(-1)
    idx = votes.argmax(-1)
    rgb = cols[idx]
    from scipy import ndimage
    inner = ndimage.binary_erosion(alpha, structure=np.ones((3, 3), bool), border_value=0)
    edge = alpha & ~inner
    thin = np.isin(idx, [4, 5, 6])                           # bill and legs keep their colour (they are a sliver wide)
    rgb = np.where((edge & ~thin)[..., None], cols[7], rgb)
    out = np.zeros((h, w, 4), np.uint8)
    out[..., :3] = np.clip(np.round(rgb * 255), 0, 255).astype(np.uint8)
    out[..., 3] = np.where(alpha, 255, 0).astype(np.uint8)
    return out


def save_frame(path, rgba):
    im = Image.fromarray(rgba, "RGBA")
    q = im.convert("RGB").quantize(colors=15, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()[:15 * 3]
    idx = np.asarray(q).copy()
    idx[rgba[..., 3] == 0] = 15
    out = Image.fromarray(idx.astype(np.uint8), "P")
    out.putpalette(pal + [0, 0, 0] * (256 - 15))
    out.save(path, optimize=True, transparency=15)


def paint_all(out):
    os.makedirs(out, exist_ok=True)
    made = {}
    for name, tones in SETS.items():
        made[name] = []
        for n in range(1, 12):
            f = f"{name}-{n}.png"
            save_frame(f"{out}/{f}", frame(n, tones, SIZE[name]))
            made[name].append(f)
    return made


def frames_block(name="heron"):
    """The frames as the engine's flock takes them (layout.json "frames", and the fx marks of the two flocks)."""
    f = lambda ns: [f"{name}-{n}.png" for n in ns]
    return {"set": name, "foot": [BOX[2], BOX[3]], "face": "E", "sizeAt": 590,
            "stand": f(ACTS["stand"]), "look": f(ACTS["look"]), "walk": f(ACTS["walk"]), "peck": f(ACTS["peck"]), "turn": f(ACTS["turn"])}


def sheet(out, made, path, zoom=3):
    rows = []
    for name, files in made.items():
        ims = [Image.open(f"{out}/{f}").convert("RGBA") for f in files]
        row = Image.new("RGBA", (sum(im.width + 4 for im in ims), BOX[1] + 14), (63, 116, 168, 255))
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
    big = Image.new("RGBA", (max(r.width for r in rows), sum(r.height + 4 for r in rows)), (90, 90, 110, 255))
    y = 0
    for r in rows:
        big.alpha_composite(r, (0, y))
        y += r.height + 4
    big.resize((big.width * zoom, big.height * zoom), Image.NEAREST).convert("RGB").save(path)


if __name__ == "__main__":
    OUT = "out/edo-castle"
    made = paint_all(OUT)
    sheet(OUT, made, "out/edo-castle-herons-sheet.png")
    print({k: len(v) for k, v in made.items()})

"""Ranger, Grandpa Joe's raccoon, as painted frames (PAINT-12C): the lead who has paws and no words.

    python3 nevada_ranger.py        writes ranger-*.png, ranger-shades-*.png and ranger.json into out/nevada-roadside/
                                    (installed with the roadside, keyed as its frames: install.py nevada-roadside), the
                                    two portraits into out/portraits/ (installed as painted, like the inventory pictures:
                                    install.py portraits); and out/nevada-ranger-sheet.png (every frame, 4x, the foot
                                    point marked) and out/nevada-ranger-walk.png (the walk laid out as a strip, as he goes)

He is drawn in the manner of the game's people (js/art/pix.js): hard edges, flat colours, the side turned from the
light one darker tone with a clean edge, one light from the upper left, a dark line round him. Every frame faces E, on
one canvas, his feet on one point (`FOOT`), at 1.25 times life where a person is 160 tall: sitting up he is 46 px from
the ground to the top of his head, on all fours 34, nose to the root of his tail 70. The engine mirrors him for W.

HOW A FRAME IS MADE. He is a small rig of parts (body, head, ears, the mask, the muzzle, four legs, two arms, the tail
in rings), each a smooth shape in his own pixels (x forward, y up from the ground, the foot point at 0, 0), posed for
the frame. The parts are laid far to near at 8 times the size, and each pixel of the frame takes the part that covers
most of it (so no pixel is half one colour and half another). Then each part's side away from the light is its shade,
a near limb that lies over his body has a dark line along its edge, a dark line goes round him, and the eye's glint,
the nose and the mouth are set as single pixels.

HIS CHARACTER (keep to it): tidy and particular. He sits up straight with his hands folded and his tail laid neatly
round his feet. He reads with his hands. He is never menacing: no teeth, ever; the nibble is busy, not fierce.

THE SETS (the master brief's format, ranger.json): stand 2 (on all fours, breathing), sit 2 (sitting up, hands folded;
a blink), walk 6, run 4 (a scamper), nibble 4 (chewing at a strand of rope held at his mouth, sitting up), wash 4
(turning a pebble over in both hands, sitting up), reach 2 (both hands out flat, holding something up), look 1
(sitting up, his head turned to us); walkN and walkS (from behind, from the front); and all of them again in the
mirror shades (a wire frame, two small mirrored lenses over the mask). Two portraits, 64 x 64, for the team bar."""

import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw

OUT = "out/nevada-roadside"         # (integration, round twelve: his frames live with the roadside's, where he lives)
FACES = "out/portraits"             # the team bar's portraits are the interface's: never keyed (install.py portraits)
CW, CH = 124, 58                    # the canvas, every frame
FOOT = (68, 56)                     # the ground point under him: the row of the dark line under his feet (his lowest row
                                    # stands on the ground's row, as the engine's critter and the game's people do); his
                                    # feet's own colour ends on the row above it
SS = 8                              # parts are laid at 8x, then each pixel takes its majority

# ---------------------------------------------------------------- his colours (flat, and one darker tone each)
C = {
    "fur": ("#9a96a0", "#6c6876"),          # his coat: a cool mid gray; its shade
    "fur_far": ("#76727e", "#57535f"),      # the far limbs and the far ear, in his own shadow
    "pale": ("#ece6da", "#bdb4aa"),         # muzzle, brows, ear rims, cheeks
    "belly": ("#b6b2b8", "#8c8892"),        # his front, paler than his back
    "mask": ("#2c2832", "#201c26"),         # the bandit's mask
    "dark": ("#3a3540", "#29252e"),         # hands, feet, lower legs, the tail's rings
    "nose": ("#18161c", "#18161c"),
    "rope": ("#f0ece0", "#c8c0b4"),
    "pebble": ("#c8c2b8", "#948e88"),
    "coin": ("#e4e8ec", "#a8b0b8"),
    "lens": ("#9ad8ee", "#4a8cb0"),         # the mirror shades: mirrored lenses (the sky in them)
    "wire": ("#d4d6dc", "#9a9ca4"),
}
LINE = "#221e28"                            # the dark line round him
GLINT = "#f6f2ea"
RED = "#c8392e"


def hexc(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.uint8)


def near4(m):
    """Pixels with a 4-neighbour in m (no wrapping round the edges)."""
    p = np.pad(m, 1)
    return p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]


# ---------------------------------------------------------------- shapes, in his own pixels (x forward, y up)
def catmull(points, steps=6, closed=False):
    p = [np.asarray(q, dtype=float) for q in points]
    if closed:
        p = p[-1:] + p + p[:2]
    else:
        p = [p[0] * 2 - p[1]] + p + [p[-1] * 2 - p[-2]]
    out = []
    for i in range(1, len(p) - 2):
        for s in range(steps):
            t = s / steps
            q = 0.5 * ((2 * p[i]) + (-p[i - 1] + p[i + 1]) * t + (2 * p[i - 1] - 5 * p[i] + 4 * p[i + 1] - p[i + 2]) * t * t
                       + (-p[i - 1] + 3 * p[i] - 3 * p[i + 1] + p[i + 2]) * t ** 3)
            out.append((float(q[0]), float(q[1])))
    if not closed:
        out.append((float(p[-2][0]), float(p[-2][1])))
    return out


def to_canvas(x, y):
    """His own (x, y) -> canvas pixels at SS (y up from the ground; the ground is the top edge of the foot row: the
    parts end there, and the dark line round him fills the foot row under his feet)."""
    return ((FOOT[0] + x) * SS, (FOOT[1] - y) * SS)


class Rig:
    """The parts of one frame, far to near."""

    def __init__(self):
        self.parts = []                     # (name, colour key, mask at SS, line?)
        self.dots = []                      # single pixels set last: (x, y, colour)

    def _mask(self, draw_fn):
        im = Image.new("L", (CW * SS, CH * SS), 0)
        draw_fn(ImageDraw.Draw(im))
        return np.asarray(im) > 127

    def blob(self, name, ck, pts, line=False, steps=6):
        """A closed smooth shape through the points."""
        q = [to_canvas(*p) for p in catmull(pts, steps, closed=True)]
        self.parts.append((name, ck, self._mask(lambda d: d.polygon(q, fill=255)), line))

    def poly(self, name, ck, pts, line=False):
        q = [to_canvas(*p) for p in pts]
        self.parts.append((name, ck, self._mask(lambda d: d.polygon(q, fill=255)), line))

    def ellipse(self, name, ck, cx, cy, rx, ry, line=False, ang=0.0):
        if ang:
            pts = [(cx + rx * math.cos(t) * math.cos(ang) - ry * math.sin(t) * math.sin(ang), cy + rx * math.cos(t) * math.sin(ang) + ry * math.sin(t) * math.cos(ang))
                   for t in np.linspace(0, 2 * math.pi, 40, endpoint=False)]
            return self.poly(name, ck, pts, line)
        (x0, y1), (x1, y0) = to_canvas(cx - rx, cy - ry), to_canvas(cx + rx, cy + ry)
        self.parts.append((name, ck, self._mask(lambda d: d.ellipse([x0, y0, x1, y1], fill=255)), line))

    def limb(self, name, ck, pts, widths, line=False):
        """A limb: a smooth line through the points, its width (px) along it (a list as long as the points, or one)."""
        path = catmull(pts, 5) if len(pts) > 2 else [tuple(map(float, p)) for p in pts]
        ws = widths if isinstance(widths, (list, tuple)) else [widths] * len(pts)
        n = len(path)
        wpath = np.interp(np.linspace(0, len(pts) - 1, n), np.arange(len(pts)), ws)

        def draw(d):
            for i in range(n):
                cx, cy = to_canvas(*path[i])
                r = wpath[i] * SS / 2
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
                if i:
                    px, py = to_canvas(*path[i - 1])
                    d.line([px, py, cx, cy], fill=255, width=max(1, int(round((wpath[i] + wpath[i - 1]) / 2 * SS))))
        self.parts.append((name, ck, self._mask(draw), line))

    def dot(self, x, y, colour):
        """A single pixel, in his own (x, y) (the pixel whose middle is nearest)."""
        cx, cy = FOOT[0] + x, FOOT[1] - y
        self.dots.append((int(math.floor(cx)), int(math.floor(cy)), colour))

    # ---- the frame
    def render(self, light=(1, 1)):
        """-> RGBA uint8 (CH, CW, 4): the parts laid far to near, each pixel the part covering most of it."""
        n = len(self.parts)
        lab = np.zeros((CH * SS, CW * SS), dtype=np.int16)
        ground = FOOT[1] * SS                                           # nothing of him is below the ground (but his line)
        for i, (_, _, m, _) in enumerate(self.parts):
            m = m.copy()
            m[ground:] = False
            lab[m] = i + 1
        blocks = lab.reshape(CH, SS, CW, SS).transpose(0, 2, 1, 3).reshape(CH, CW, SS * SS)
        counts = np.stack([(blocks == k).sum(axis=2) for k in range(n + 1)], axis=2)
        counts[..., 0] = (counts[..., 0] * 1.12).astype(counts.dtype)        # (the edge kept a little tight)
        win = counts.argmax(axis=2)
        # each part's own whole shape at 1x (for its light and shade, so a limb laid over the body casts no false shade)
        own = [m.reshape(CH, SS, CW, SS).mean(axis=(1, 3)) > 0.5 for (_, _, m, _) in self.parts]
        rgb = np.zeros((CH, CW, 3), dtype=np.uint8)
        alpha = win > 0
        for i, (name, ck, m, line) in enumerate(self.parts):
            here = win == i + 1
            if not here.any():
                continue
            fill, shade = (hexc(c) for c in C[ck])
            o = own[i] if own[i].any() else here
            # the side away from the light: where the shape ends within k pixels toward the lower right
            ys, xs = np.nonzero(o)
            span = max(2, min(ys.max() - ys.min() + 1, xs.max() - xs.min() + 1))
            k = max(1, int(round(span * 0.30)))
            sh = np.zeros_like(o)
            sy, sx = light
            moved = np.zeros_like(o)
            moved[:CH - k * sy if sy else CH, :CW - k * sx if sx else CW] = o[k * sy:, k * sx:]
            sh = o & ~moved
            rgb[here] = fill
            rgb[here & sh] = shade
            if line:                                                        # a near limb over his body: a dark line along its edge
                farther = np.zeros_like(here)
                for j in range(i):
                    farther |= win == j + 1
                edge = here & near4(farther)
                rgb[edge] = hexc(LINE)
        # the dark line round him
        out = np.zeros((CH, CW, 4), dtype=np.uint8)
        ring = ~alpha & near4(alpha)
        out[alpha, :3] = rgb[alpha]
        out[alpha, 3] = 255
        out[ring, :3] = hexc(LINE)
        out[ring, 3] = 255
        for (x, y, c) in self.dots:
            if 0 <= x < CW and 0 <= y < CH:
                out[y, x, :3] = hexc(c)
                out[y, x, 3] = 255
        return out


# ---------------------------------------------------------------- the head, in profile or turned to us
def head(r, hx, hy, tilt=0.0, mouth=0, blink=False, shades=False, chew=0.0, far_ear=True):
    """His head in profile facing E: (hx, hy) the middle of the skull; tilt in radians (+ nose up). mouth 1: open a
    pixel (chewing, never teeth). The mask across the eye, the pale brow over it and the pale muzzle under it, a dark
    stripe down the nose, round ears with pale rims, a glint in the eye."""
    ca, sa = math.cos(tilt), math.sin(tilt)
    K = 1.12                                                            # (a lead's face is drawn a little large, to read)
    P = lambda x, y: (hx + K * (x * ca - y * sa), hy + K * (x * sa + y * ca))
    Ps = lambda pts: [P(*p) for p in pts]
    if far_ear:
        r.blob("ear-far", "fur_far", Ps([(1.0, 5.0), (2.4, 9.4), (4.2, 10.2), (5.2, 7.6), (4.6, 5.0)]))
    # skull and snout, one piece: round at the back, tapering to the nose
    r.blob("head", "fur", Ps([(-6.0, 0.5), (-5.0, 4.8), (-1.5, 7.0), (3.0, 6.6), (7.0, 4.4), (10.5, 2.0), (12.8, 0.2), (12.6, -1.6),
                              (9.8, -3.0 - chew), (5.0, -4.6 - chew), (0.0, -5.6), (-4.4, -4.4)]))
    r.blob("cheek", "pale", Ps([(-5.6, -0.6), (-3.6, 1.2), (-1.0, 0.0), (0.5, -2.6), (-1.2, -5.2), (-4.0, -4.6)]))
    r.blob("muzzle", "pale", Ps([(3.5, -0.8), (7.0, 0.4), (10.5, 0.6), (12.6, -0.6), (12.2, -1.8), (9.6, -3.0 - chew), (5.0, -4.4 - chew), (2.2, -3.2)]))
    r.blob("mask", "mask", Ps([(-2.4, 2.6), (0.6, 3.6), (4.6, 3.0), (8.2, 1.6), (8.4, 0.0), (5.6, -0.8), (2.0, -0.6), (-1.4, -0.2)]))
    r.limb("brow", "pale", Ps([(-0.6, 4.6), (2.6, 5.2), (6.2, 4.0)]), [1.5, 1.6, 1.2])
    r.limb("stripe", "mask", Ps([(1.2, 6.6), (5.4, 5.0), (9.4, 2.8)]), [1.4, 1.3, 1.0])
    r.blob("ear", "fur", Ps([(-3.4, 5.0), (-3.6, 9.2), (-1.4, 10.6), (0.8, 9.0), (1.2, 5.4)]))
    r.blob("ear-rim", "pale", Ps([(-3.0, 8.6), (-1.4, 10.2), (0.6, 8.8), (-1.2, 9.3)]))
    r.ellipse("nose", "nose", *P(12.9, -0.4), 1.2, 1.1)
    if shades:
        ex, ey = P(4.4, 1.3)
        r.limb("wire", "wire", [P(-2.6, 2.6), P(2.0, 2.0)], 0.9)                     # the arm of the frame, back to his ear
        r.ellipse("lens", "lens", ex, ey, 2.6, 2.0)
        r.limb("bridge", "wire", [P(6.6, 1.6), P(8.6, 1.4)], 0.8)
        r.ellipse("lens-far", "lens", *P(9.6, 1.6), 1.0, 1.6)
        r.dot(ex - 0.8, ey + 0.6, "#ffffff")
    else:
        gx, gy = P(4.4, 1.6)
        if blink:
            r.dot(gx - 1, gy - 0.6, C["mask"][0])
        else:
            r.dot(gx, gy, GLINT)
    if mouth:
        mx, my = P(9.0, -2.4 - chew * 0.5)
        r.dot(mx, my, C["mask"][1])
        r.dot(mx - 1, my + 0.2, C["mask"][1])


def head_front(r, hx, hy, blink=False, shades=False):
    """His head turned to us: the bandit's mask across both eyes, a pale brow over each, the pale muzzle with the black
    nose at its tip, round ears with pale rims, a glint in each eye. Never teeth."""
    r.blob("ear-l", "fur", [(hx - 7.4, hy + 3.0), (hx - 8.6, hy + 7.6), (hx - 6.6, hy + 9.4), (hx - 4.0, hy + 7.8), (hx - 3.6, hy + 4.4)])
    r.blob("ear-r", "fur", [(hx + 7.4, hy + 3.0), (hx + 8.6, hy + 7.6), (hx + 6.6, hy + 9.4), (hx + 4.0, hy + 7.8), (hx + 3.6, hy + 4.4)])
    r.blob("rim-l", "pale", [(hx - 8.0, hy + 7.4), (hx - 6.6, hy + 9.0), (hx - 4.8, hy + 7.8), (hx - 6.4, hy + 8.2)])
    r.blob("rim-r", "pale", [(hx + 8.0, hy + 7.4), (hx + 6.6, hy + 9.0), (hx + 4.8, hy + 7.8), (hx + 6.4, hy + 8.2)])
    r.blob("head", "fur", [(hx - 8.0, hy), (hx - 7.0, hy + 4.8), (hx - 3.0, hy + 7.2), (hx + 3.0, hy + 7.2), (hx + 7.0, hy + 4.8), (hx + 8.0, hy),
                           (hx + 7.4, hy - 3.6), (hx + 4.4, hy - 6.4), (hx, hy - 7.4), (hx - 4.4, hy - 6.4), (hx - 7.4, hy - 3.6)])
    r.blob("cheek-l", "pale", [(hx - 8.0, hy - 0.6), (hx - 6.0, hy + 0.6), (hx - 4.4, hy - 2.6), (hx - 6.4, hy - 4.6)])
    r.blob("cheek-r", "pale", [(hx + 8.0, hy - 0.6), (hx + 6.0, hy + 0.6), (hx + 4.4, hy - 2.6), (hx + 6.4, hy - 4.6)])
    r.blob("muzzle", "pale", [(hx - 3.4, hy - 1.0), (hx, hy + 0.4), (hx + 3.4, hy - 1.0), (hx + 3.2, hy - 4.6), (hx, hy - 6.6), (hx - 3.2, hy - 4.6)])
    r.blob("mask", "mask", [(hx - 7.6, hy + 1.4), (hx - 4.6, hy + 3.0), (hx - 1.2, hy + 1.6), (hx, hy + 2.6), (hx + 1.2, hy + 1.6), (hx + 4.6, hy + 3.0),
                            (hx + 7.6, hy + 1.4), (hx + 6.0, hy - 1.2), (hx + 2.6, hy - 1.2), (hx, hy - 0.2), (hx - 2.6, hy - 1.2), (hx - 6.0, hy - 1.2)])
    r.limb("brow-l", "pale", [(hx - 6.6, hy + 3.4), (hx - 4.4, hy + 4.4), (hx - 2.0, hy + 3.6)], 1.4)
    r.limb("brow-r", "pale", [(hx + 6.6, hy + 3.4), (hx + 4.4, hy + 4.4), (hx + 2.0, hy + 3.6)], 1.4)
    r.limb("stripe", "mask", [(hx, hy + 6.6), (hx, hy + 2.4)], 1.4)
    r.ellipse("nose", "nose", hx, hy - 2.8, 1.5, 1.1)
    if shades:
        for sx in (-1, 1):
            r.ellipse("lens", "lens", hx + sx * 3.8, hy + 1.0, 2.6, 2.0)
        r.limb("bridge", "wire", [(hx - 1.4, hy + 1.6), (hx + 1.4, hy + 1.6)], 0.8)
        r.limb("arm-l", "wire", [(hx - 6.2, hy + 1.6), (hx - 7.8, hy + 2.2)], 0.8)
        r.limb("arm-r", "wire", [(hx + 6.2, hy + 1.6), (hx + 7.8, hy + 2.2)], 0.8)
        r.dot(hx - 4.6, hy + 1.6, "#ffffff")
        r.dot(hx + 3.0, hy + 1.6, "#ffffff")
    elif blink:
        r.dot(hx - 4.0, hy + 0.6, C["mask"][1])
    else:
        r.dot(hx - 3.8, hy + 1.2, GLINT)
        r.dot(hx + 3.8, hy + 1.2, GLINT)


# ---------------------------------------------------------------- the tail, in rings
def tail(r, pts, widths, rings=7, near=True):
    """The ringed tail: a smooth line through the points, its width along it; laid as `rings` bands, light and dark in
    turn from the root, the tip dark."""
    path = catmull(pts, 8)
    n = len(path)
    ws = np.interp(np.linspace(0, len(pts) - 1, n), np.arange(len(pts)), widths)
    for k in range(rings):
        a, b = int(n * k / rings), int(n * (k + 1) / rings) + 1
        seg = path[a:min(b, n)]
        if len(seg) < 2:
            continue
        ck = "dark" if (rings - 1 - k) % 2 == 0 else "fur"
        r.limb(f"tail{k}", ck if near else ("dark" if ck == "dark" else "fur_far"), seg, list(ws[a:min(b, n)]))


# ---------------------------------------------------------------- on all fours
def legs_at(phase, stride=32.0, duty=0.60, lift=3.0):
    """Where each foot is (x forward of the foot point, y up) at a phase of the walk: diagonal pairs, each foot on the
    ground `duty` of the cycle moving back at the speed he goes forward (so it does not slide), then swung forward."""
    out = {}
    reach = stride * duty / 2
    for leg, base, off in (("nf", 19.0, 0.0), ("fh", -20.0, 0.0), ("ff", 20.5, 0.5), ("nh", -18.5, 0.5)):
        p = (phase + off) % 1.0
        if p < duty:
            x = base + reach - (p / duty) * 2 * reach
            y = 0.0
        else:
            q = (p - duty) / (1 - duty)
            x = base - reach + q * 2 * reach
            y = lift * math.sin(q * math.pi)
        out[leg] = (x, y)
    return out


def all_fours(feet=None, bob=0.0, stretch=0.0, arch=0.0, head_dy=0.0, head_tilt=0.0, tail_lift=0.0, blink=False, shades=False, breath=0.0):
    """On all fours, facing E: a hunched back, high at the hips; short sturdy legs, the front paws like small black
    hands, the hind feet flat on their soles; a big round haunch. feet: {nf, ff, nh, fh}: (x, y) of each foot (y up);
    bob lifts the body; stretch lengthens it (a scamper); arch bows the back."""
    feet = feet or {"nf": (19.0, 0.0), "ff": (21.0, 0.0), "nh": (-19.0, 0.0), "fh": (-21.5, 0.0)}
    r = Rig()
    b = bob
    sh_x, hip_x = 17.0 + stretch * 0.5, -19.0 - stretch * 0.5

    def leg_front(name, ck, fx, fy, line=False):
        top = (sh_x - 0.5, 16.0 + b)
        elbow = (top[0] - 1.8 + (fx - top[0]) * 0.35, 8.6 + fy * 0.5 + b * 0.5)
        wrist = (fx + 0.2, fy + 2.6)
        r.limb(name, ck, [top, elbow, wrist], [6.0, 4.4, 3.6], line)
        r.limb(name + "-low", "dark", [((elbow[0] + wrist[0]) / 2, (elbow[1] + wrist[1]) / 2), wrist], [3.8, 3.6], line)
        r.ellipse(name + "-paw", "dark", fx + 1.2, fy + 1.2, 2.6, 1.3)

    def leg_hind(name, ck, fx, fy, line=False):
        hip = (hip_x + 1.0, 17.0 + b + arch * 0.5)
        knee = (hip[0] + 3.4 + (fx - hip_x) * 0.30, 9.0 + fy * 0.5 + b * 0.4)
        hock = (fx - 2.6, fy + 3.4)
        r.blob(name + "-haunch", ck, [(hip[0] - 7.4, hip[1] + 2.0), (hip[0] - 3.0, hip[1] + 7.4), (hip[0] + 4.6, hip[1] + 5.4), (hip[0] + 6.4, hip[1] - 1.4),
                                     (knee[0] + 1.6, knee[1] + 0.4), (knee[0] - 2.4, knee[1] - 1.2), (hip[0] - 6.0, hip[1] - 4.6)], line)
        r.limb(name, ck, [knee, hock], [4.6, 3.6], line)
        r.limb(name + "-sole", "dark", [hock, (fx + 3.4, fy + 1.0)], [3.0, 2.2], line)
    leg_front("leg-ff", "fur_far", *feet["ff"])
    leg_hind("leg-fh", "fur_far", *feet["fh"])
    # the tail behind, its root at the rump: held low and level, its tip lifted a little
    tx = hip_x - 8.0
    tail(r, [(tx + 3.0, 23.0 + b + arch * 0.4), (tx - 6.0, 19.5 + b * 0.5), (tx - 15.0, 17.0 + tail_lift * 0.4), (tx - 24.0, 17.6 + tail_lift * 0.8), (tx - 30.0, 21.0 + tail_lift)],
         [7.6, 9.0, 9.2, 8.0, 5.6], rings=7)
    # the body: the chest low in front, the back rising to a hunch over the hips, a round rump, the belly
    back = 32.6 + b + arch                                                # the hunch: highest over the hips, as a raccoon goes
    r.blob("body", "fur", [(sh_x + 4.0, 21.0 + b), (sh_x - 2.0, 24.6 + b + arch * 0.2), (sh_x - 13.0 - stretch * 0.3, 29.0 + b + arch * 0.6), (hip_x + 4.0, back),
                           (hip_x - 5.0, 30.6 + b + arch * 0.8), (hip_x - 11.0, 23.0 + b + arch * 0.4), (hip_x - 11.6, 14.0 + b), (hip_x - 5.0, 9.6 + b),
                           (0.0, 9.0 + b - arch * 0.4), (sh_x - 3.0, 9.4 + b), (sh_x + 2.4, 12.0 + b), (sh_x + 5.0, 16.4 + b)])
    r.blob("belly", "belly", [(sh_x + 1.4, 13.0 + b), (sh_x - 6.0, 10.0 + b), (hip_x + 3.0, 10.0 + b), (hip_x + 2.0, 12.6 + b), (sh_x - 8.0, 13.0 + b)])
    # the near legs, over the body, a dark line along their edges
    leg_hind("leg-nh", "fur", *feet["nh"], line=True)
    leg_front("leg-nf", "fur", *feet["nf"], line=True)
    head(r, sh_x + 9.0 + stretch * 0.3, 21.6 + b + head_dy + breath * 0.3, tilt=head_tilt - 0.06, blink=blink, shades=shades)
    return r


# ---------------------------------------------------------------- sitting up
def sitting(arms="fold", head_mode="profile", head_dy=0.0, head_tilt=0.0, mouth=0, chew=0.0, blink=False, shades=False, held=None, hands=None, breath=0.0):
    """Sitting up straight on his haunches, facing E, his tail laid neatly round his feet. arms: "fold" (hands folded
    in front: tidy), "mouth" (both hands at his mouth, holding `held` there), "wash" (both hands in front, turning a
    pebble), "out" (both hands out flat in front, holding something up). `hands`: the hands' places for this frame."""
    r = Rig()
    b = breath
    # the far arm (only its hand shows past the body), the far hind foot
    r.ellipse("foot-far", "dark", 9.6, 1.4, 3.0, 1.3)
    hand_n, hand_f = hands or {"fold": ((10.6, 16.6), (12.6, 17.4)), "mouth": ((16.0, 32.5), (17.6, 33.6)),
                               "wash": ((12.8, 20.6), (14.8, 22.0)), "out": ((21.0, 25.0), (22.6, 25.6))}[arms]
    shoulder = (5.6, 29.0 + b)
    if arms != "fold":
        r.limb("arm-far", "fur_far", [(shoulder[0] + 1.6, shoulder[1] + 0.4), ((shoulder[0] + hand_f[0]) / 2 + 1.0, (shoulder[1] + hand_f[1]) / 2 - 2.0), hand_f], [3.6, 3.0, 2.6])
        r.ellipse("hand-far", "dark", hand_f[0] + 0.6, hand_f[1], 1.9, 1.5)
    # the body: a pear, wide at the haunches, the chest up to the shoulders, straight-backed
    r.blob("body", "fur", [(6.4, 30.0 + b), (1.4, 32.6 + b), (-4.4, 31.4 + b), (-8.0, 26.0 + b), (-10.4, 18.0), (-12.4, 10.0), (-11.0, 4.0), (-5.0, 2.2),
                           (5.0, 2.4), (10.6, 6.0), (11.4, 14.0), (9.6, 23.0 + b * 0.5)])
    r.blob("belly", "belly", [(8.0, 27.6 + b), (10.0, 20.0), (10.2, 11.0), (8.0, 5.0), (4.0, 8.0), (4.0, 18.0), (5.0, 25.0 + b)])
    # the near haunch, a round thigh; the near hind foot flat in front; the tail laid round his feet, its tip turned up
    r.blob("haunch", "fur", [(-10.6, 11.0), (-6.4, 17.4), (0.6, 17.6), (5.4, 12.0), (5.0, 5.0), (-0.6, 2.4), (-8.0, 3.0)], line=True)
    r.limb("foot", "dark", [(2.6, 1.6), (9.6, 1.4)], [3.0, 2.6])
    tail(r, [(-10.4, 4.6), (-13.0, 3.8), (-9.0, 3.6), (0.0, 3.6), (9.0, 3.8), (14.6, 4.6), (17.2, 7.4)], [6.6, 7.0, 7.0, 6.8, 6.4, 5.6, 4.2], rings=7)
    # the near arm
    if arms == "fold":                                                     # the forearm across his front, his hands folded, tidy
        r.limb("arm", "fur", [(shoulder[0] - 0.6, shoulder[1]), (4.0, 21.6), (9.0, 18.4)], [4.0, 3.6, 3.2], line=True)
        r.ellipse("hand-far", "dark", 11.6, 19.0, 1.9, 1.5)
        r.ellipse("hand", "dark", 10.0, 18.0, 2.1, 1.6)
    else:
        elbow = ((shoulder[0] + hand_n[0]) / 2 - 0.4, (shoulder[1] + hand_n[1]) / 2 - 3.2)
        r.limb("arm", "fur", [(shoulder[0] - 1.0, shoulder[1]), elbow, hand_n], [3.8, 3.2, 2.8], line=True)
    if held == "rope":                                                    # a strand of rope, white with its red thread, held at his mouth
        r.limb("rope", "rope", [(hand_n[0] - 3.0, hand_n[1] - 4.0), (hand_n[0] + 1.0, hand_n[1] + 0.4), (hand_n[0] + 4.6, hand_n[1] + 2.2)], 1.6)
        r.dot(hand_n[0] - 1.6, hand_n[1] - 2.4, RED)
    elif held == "pebble":
        r.ellipse("pebble", "pebble", (hand_n[0] + hand_f[0]) / 2 + 0.8, (hand_n[1] + hand_f[1]) / 2 + 0.6, 1.8, 1.5)
    elif held == "coin":
        r.ellipse("coin", "coin", hand_n[0] + 0.8, hand_n[1] + 1.6, 1.9, 1.0)
    if arms != "fold":
        r.ellipse("hand", "dark", hand_n[0] + 0.6, hand_n[1], 2.0, 1.5)
    if head_mode == "front":
        head_front(r, 4.6, 37.0 + b + head_dy, blink=blink, shades=shades)
    else:
        head(r, 3.6, 36.8 + b + head_dy, tilt=head_tilt, mouth=mouth, chew=chew, blink=blink, shades=shades)
    return r


# ---------------------------------------------------------------- from behind and from the front (walkN, walkS)
def walk_ns(view, phase, shades=False):
    """On all fours, going away from us (N) or coming toward us (S), the legs stepping in diagonal pairs and the body
    rocking a little. Going away: his round rump, the ringed tail hanging toward us and swinging, the soles of his
    hind feet as they lift, his ears over his back. Coming toward us: his head low in front, the mask and both eyes,
    his back humped up behind it, the front paws stepping at either side of his chin."""
    r = Rig()
    s1 = math.sin(phase * 2 * math.pi)
    rock = s1 * 0.7
    up_l, up_r = max(0.0, s1) * 2.6, max(0.0, -s1) * 2.6
    if view == "N":
        r.blob("ears", "fur_far", [(-5.0 + rock, 30.0), (-4.4 + rock, 34.6), (-2.4 + rock, 32.4), (2.4 + rock, 32.4), (4.4 + rock, 34.6), (5.0 + rock, 30.0)])
        r.blob("back", "fur", [(-8.6 + rock, 20.0), (-7.4 + rock, 28.0), (0.0 + rock, 31.0), (7.4 + rock, 28.0), (8.6 + rock, 20.0), (0.0, 16.0)])
        for sx, up in ((-1, up_l), (1, up_r)):                           # the hind legs, stepping; a lifted foot shows its dark sole
            r.limb(f"leg{sx}", "fur", [(sx * 7.0, 14.0), (sx * 7.2, 6.0 + up), (sx * 7.0, 2.4 + up)], [5.4, 4.2, 3.6], line=True)
            r.ellipse(f"sole{sx}", "dark", sx * 7.0, 1.4 + up, 2.4, 1.4 + 0.3 * (up > 0))
        r.blob("rump", "fur", [(-10.4 + rock * 0.6, 12.0), (-9.6 + rock, 20.0), (-5.0 + rock, 25.0), (5.0 + rock, 25.0), (9.6 + rock, 20.0), (10.4 + rock * 0.6, 12.0),
                               (6.0, 7.0), (0.0, 6.0), (-6.0, 7.0)], line=True)
        sw = -s1 * 2.4                                                   # the tail swings against the rock of his hips
        tail(r, [(rock, 22.0), (rock + sw * 0.4, 17.0), (sw * 0.8, 11.0), (sw, 5.6), (sw * 1.1, 2.4)], [6.0, 7.6, 8.0, 7.0, 4.6], rings=6)
    else:
        r.blob("back", "fur", [(-10.0 + rock, 14.0), (-9.0 + rock, 23.0), (0.0 + rock, 28.6), (9.0 + rock, 23.0), (10.0 + rock, 14.0), (0.0, 10.0)])
        for sx, up in ((-1, up_r), (1, up_l)):                           # the short front legs at either side of his chin, stepping
            r.limb(f"arm{sx}", "fur", [(sx * 7.8, 11.0), (sx * 7.6, 5.0 + up), (sx * 7.4, 2.4 + up)], [5.0, 4.2, 3.6], line=True)
            r.ellipse(f"paw{sx}", "dark", sx * 7.4, 1.4 + up, 2.8, 1.4)
        head_front(r, rock * 0.5, 15.2, shades=shades)
    return r


# ---------------------------------------------------------------- the portraits (64 x 64, head and shoulders, to us)
def portrait(shades=False):
    """Head and shoulders, looking at us, drawn at 64 x 64 in the same manner with more room: the mask across both
    eyes, bright eyes, the pale brows and muzzle, the black nose, round ears with pale rims, his chest fur; tidy."""
    S = 4
    im = Image.new("RGBA", (64 * S, 64 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    P = lambda x, y: (x * S, y * S)

    def blob(pts, colour):
        q = [P(*p) for p in catmull(pts, 8, closed=True)]
        d.polygon(q, fill=colour)

    def ell(cx, cy, rx, ry, colour):
        d.ellipse([P(cx - rx, cy - ry), P(cx + rx, cy + ry)], fill=colour)

    fur, fur_sh = C["fur"]
    pale, pale_sh = C["pale"]
    mask, mask_sh = C["mask"]
    blob([(8, 64), (10, 54), (18, 47), (32, 45), (46, 47), (54, 54), (56, 64)], fur_sh)          # shoulders
    blob([(14, 64), (17, 55), (24, 50), (32, 49), (40, 50), (47, 55), (50, 64)], fur)
    blob([(24, 64), (26, 56), (32, 53), (38, 56), (40, 64)], C["belly"][0])                      # his chest
    for sx in (-1, 1):                                                                            # ears
        blob([(32 + sx * 13, 21), (32 + sx * 19, 10), (32 + sx * 16, 5), (32 + sx * 10, 9), (32 + sx * 8, 16)], fur_sh)
        blob([(32 + sx * 14, 18), (32 + sx * 17.5, 10.5), (32 + sx * 15.5, 7.5), (32 + sx * 11.5, 10), (32 + sx * 10.5, 15)], "#4a4552")
        blob([(32 + sx * 18.6, 10.4), (32 + sx * 16.2, 5.6), (32 + sx * 10.6, 9.0), (32 + sx * 15.4, 7.6)], pale)
    blob([(13, 30), (14, 21), (20, 14), (32, 12), (44, 14), (50, 21), (51, 30), (49, 38), (42, 45), (32, 48), (22, 45), (15, 38)], fur)   # the head
    blob([(13, 32), (16, 30), (22, 34), (24, 41), (20, 44), (15, 39)], pale)                                # cheeks
    blob([(51, 32), (48, 30), (42, 34), (40, 41), (44, 44), (49, 39)], pale)
    blob([(24, 35), (32, 33), (40, 35), (41, 42), (37, 47), (32, 48.5), (27, 47), (23, 42)], pale)          # the muzzle
    blob([(13.5, 27), (19, 23), (26, 24.5), (30, 28), (32, 27.5), (34, 28), (38, 24.5), (45, 23), (50.5, 27),
          (48, 32), (41, 33), (35, 31.5), (32, 33), (29, 31.5), (23, 33), (16, 32)], mask)              # the mask
    d.line([P(32, 13.5), P(32, 26)], fill=mask_sh, width=3 * S // 2 + 2)                                 # the stripe down the nose
    for sx in (-1, 1):                                                                                   # the brows
        d.line([P(32 + sx * 5.5, 21.5), P(32 + sx * 10, 19.6), P(32 + sx * 15, 21.2)], fill=pale, width=2 * S, joint="curve")
    if shades:
        for sx in (-1, 1):
            ell(32 + sx * 9.5, 27.6, 6.4, 4.6, C["wire"][1])
            ell(32 + sx * 9.5, 27.6, 5.6, 3.9, C["lens"][1])
            ell(32 + sx * 9.0, 26.8, 4.6, 3.0, C["lens"][0])
            d.polygon([P(32 + sx * 9.5 - 3.6, 25.4), P(32 + sx * 9.5 - 1.6, 24.6), P(32 + sx * 9.5 - 3.0, 27.4)], fill="#ffffff")
        d.line([P(28.4, 26.4), P(35.6, 26.4)], fill=C["wire"][0], width=S)
        d.line([P(16.6, 26.6), P(13.2, 25.6)], fill=C["wire"][0], width=S)
        d.line([P(47.4, 26.6), P(50.8, 25.6)], fill=C["wire"][0], width=S)
    else:
        for sx in (-1, 1):                                                                                # eyes: dark, a glint
            ell(32 + sx * 9.0, 27.8, 3.0, 2.6, "#141218")
            ell(32 + sx * 9.0 - 0.9, 27.0, 1.1, 1.0, GLINT)
    blob([(28.4, 37.6), (32, 36.2), (35.6, 37.6), (34.4, 40.2), (32, 41), (29.6, 40.2)], C["nose"][0])  # the nose
    ell(31.0, 37.6, 0.9, 0.6, "#5a5662")
    d.line([P(32, 41), P(32, 43.4)], fill=pale_sh, width=S)                                             # a small, closed, contented mouth
    d.line([P(29.6, 44.2), P(32, 43.4), P(34.4, 44.2)], fill=pale_sh, width=S, joint="curve")
    a = np.asarray(im.resize((64, 64), Image.BOX))
    out = a.copy()
    # hard edges and flat colour: every pixel opaque or clear, and snapped to the colours it was drawn in
    alpha = a[..., 3] > 110
    pal = np.array([hexc(c) for c in [fur, fur_sh, pale, pale_sh, mask, mask_sh, C["belly"][0], "#4a4552", "#141218", GLINT, C["nose"][0], "#5a5662"]
                    + ([C["wire"][0], C["wire"][1], C["lens"][0], C["lens"][1], "#ffffff"] if shades else [])], dtype=np.int32)
    rgb = a[..., :3].astype(np.int32)
    dist = ((rgb[:, :, None, :] - pal[None, None, :, :]) ** 2).sum(axis=3)
    snapped = pal[dist.argmin(axis=2)].astype(np.uint8)
    out[..., :3] = snapped
    out[..., 3] = np.where(alpha, 255, 0)
    ring = ~alpha & near4(alpha)
    out[ring, :3] = hexc(LINE)
    out[ring, 3] = 255
    return out


# ---------------------------------------------------------------- all the sets
WALK_FRAMES, RUN_FRAMES = 6, 4
STRIDE, RUN_STRIDE, PACE = 32.0, 70.0, 100.0


def frames(shades=False):
    sets = {}
    sets["stand"] = [all_fours(shades=shades).render(), all_fours(bob=0.6, breath=0.6, shades=shades).render()]
    sets["sit"] = [sitting(shades=shades).render(), sitting(blink=True, shades=shades).render()]
    walk = []
    for i in range(WALK_FRAMES):
        ph = i / WALK_FRAMES
        bob = 0.7 * (0.5 - 0.5 * math.cos(ph * 4 * math.pi))
        walk.append(all_fours(feet=legs_at(ph, STRIDE), bob=bob, head_dy=-bob * 0.4, tail_lift=0.8 * math.sin(ph * 2 * math.pi), shades=shades).render())
    sets["walk"] = walk
    run = []
    for i, (st, ar, bob, feet) in enumerate((
            (5.0, -1.0, 1.0, {"nf": (36.0, 2.0), "ff": (32.0, 3.0), "nh": (-35.0, 1.0), "fh": (-31.0, 0.0)}),       # stretched out, flying
            (2.0, 0.0, 0.4, {"nf": (22.0, 0.0), "ff": (18.0, 0.0), "nh": (-25.0, 2.6), "fh": (-21.0, 3.6)}),         # front feet down
            (-3.0, 3.0, 0.8, {"nf": (9.0, 2.4), "ff": (5.0, 1.4), "nh": (-1.0, 0.0), "fh": (3.0, 0.0)}),            # gathered: hind feet past the front
            (1.0, 1.0, 0.2, {"nf": (24.0, 3.0), "ff": (20.0, 2.0), "nh": (-16.0, 0.0), "fh": (-12.0, 0.0)}))):      # pushing off
        run.append(all_fours(feet=feet, bob=bob, stretch=st, arch=ar, tail_lift=2.0 + i % 2, head_dy=-0.5 * (i % 2), shades=shades).render())
    sets["run"] = run
    sets["nibble"] = [sitting(arms="mouth", held="rope", head_tilt=t, mouth=m, chew=ch, head_dy=dy, shades=shades,
                              hands=((16.0 + hx, 32.0 + hy), (17.6 + hx, 33.2 + hy))).render()
                      for (t, m, ch, dy, hx, hy) in ((-0.10, 0, 0.0, 0.0, 0.0, 0.0), (-0.16, 1, 0.8, -0.6, 0.0, -0.6), (-0.06, 0, 0.0, 0.2, 0.6, 0.2), (-0.16, 1, 0.8, -0.6, -0.4, -0.6))]
    sets["wash"] = [sitting(arms="wash", held="pebble", head_tilt=-0.22, head_dy=-0.6, shades=shades, hands=h).render()
                    for h in (((12.6, 20.4), (14.8, 22.2)), ((13.6, 22.2), (14.0, 20.0)), ((12.8, 21.8), (15.0, 20.6)), ((13.8, 20.2), (13.8, 22.4)))]
    sets["reach"] = [sitting(arms="out", held="coin", hands=((17.0, 23.6), (18.6, 24.2)), shades=shades).render(),
                     sitting(arms="out", held="coin", hands=((21.6, 25.2), (23.2, 25.8)), head_tilt=0.06, shades=shades).render()]
    sets["look"] = [sitting(head_mode="front", shades=shades).render()]
    sets["walkN"] = [walk_ns("N", i / WALK_FRAMES, shades).render() for i in range(WALK_FRAMES)]
    sets["walkS"] = [walk_ns("S", i / WALK_FRAMES, shades).render() for i in range(WALK_FRAMES)]
    return sets


def edges(all_sets):
    """Frames that touch the canvas's edge (something of him would be cut off)."""
    bad = []
    for name, fr in all_sets.items():
        for i, a in enumerate(fr):
            m = a[..., 3] > 0
            if m[0].any() or m[-1].any() or m[:, 0].any() or m[:, -1].any():
                bad.append(f"{name}-{i}")
    return bad


def measure(frames_):
    """Ground to the top of the head (px), the nose to the root of the tail, as painted."""
    def top(a):
        ys = np.nonzero(a[..., 3] > 0)[0]
        return FOOT[1] - ys.min()
    return top(frames_["stand"][0]) - 1, top(frames_["sit"][0]) - 1        # (less the line round him)


def sheet(all_sets, path, zoom=4):
    """Every frame on one sheet, 4x, on a mid ground, the foot point marked; a row a set (shades below)."""
    names = list(all_sets.keys())
    rows = []
    for n in names:
        fr = all_sets[n]
        row = np.zeros((CH + 4, len(fr) * (CW + 4), 4), dtype=np.uint8)
        row[...] = (150, 132, 112, 255)
        for i, f in enumerate(fr):
            x0 = i * (CW + 4)
            a = f[..., 3:4].astype(np.float32) / 255
            row[2:2 + CH, x0:x0 + CW, :3] = (f[..., :3] * a + row[2:2 + CH, x0:x0 + CW, :3] * (1 - a)).astype(np.uint8)
            row[2 + FOOT[1], x0 + FOOT[0], :3] = (255, 40, 200)
            row[2 + FOOT[1] + 1, x0 + FOOT[0] - 1:x0 + FOOT[0] + 2, :3] = (255, 40, 200)
        rows.append((n, row))
    wmax = max(r.shape[1] for _, r in rows)
    H_ = sum(r.shape[0] + 10 for _, r in rows)
    big = Image.new("RGB", (wmax * zoom + 120, H_ * zoom), (40, 38, 46))
    d = ImageDraw.Draw(big)
    y = 0
    for n, r in rows:
        big.paste(Image.fromarray(r).convert("RGB").resize((r.shape[1] * zoom, r.shape[0] * zoom), Image.NEAREST), (120, y))
        d.text((6, y + 20), n, fill=(240, 236, 220))
        y += (r.shape[0] + 10) * zoom
    big.save(path)


def walk_strip(walk, path, cycles=2, zoom=3, stride=STRIDE):
    """The walk as it is seen: each frame laid where he is at that moment, going right at his own pace (the foot point
    moving `stride` a cycle), on a ground line, so feet that slide or a body that jerks show."""
    n = len(walk)
    W_ = int(CW + stride * cycles + 20)
    im = Image.new("RGBA", (W_, CH + 8), (150, 132, 112, 255))
    d = ImageDraw.Draw(im)
    d.line([(0, FOOT[1]), (W_, FOOT[1])], fill=(110, 96, 84, 255))
    frames_ = []
    for k in range(n * cycles):
        x = int(round(k * stride / n))
        im2 = im.copy()
        im2.alpha_composite(Image.fromarray(walk[k % n]), (x, 0))
        frames_.append(im2)
    strip_ = Image.new("RGBA", (W_, (CH + 8) * len(frames_)), (0, 0, 0, 0))
    for i, f in enumerate(frames_):
        strip_.paste(f, (0, i * (CH + 8)))
    strip_.convert("RGB").resize((W_ * zoom, (CH + 8) * len(frames_) * zoom), Image.NEAREST).save(path)
    # and an animated look at it (a GIF), going along
    gif = [f.convert("RGB").resize((W_ * zoom, (CH + 8) * zoom), Image.NEAREST) for f in frames_]
    gif[0].save(path.replace(".png", ".gif"), save_all=True, append_images=gif[1:], duration=125, loop=0)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(FACES, exist_ok=True)
    made = {}
    for variant, prefix in ((False, "ranger-"), (True, "ranger-shades-")):
        sets = frames(variant)
        for name, fr in sets.items():
            files = []
            for i, a in enumerate(fr):
                fn = f"{prefix}{name}-{i}.png"
                Image.fromarray(a, "RGBA").save(f"{OUT}/{fn}", optimize=True)
                files.append(fn)
            if not variant:
                made[name] = files
        Image.fromarray(portrait(variant), "RGBA").save(f"{FACES}/{prefix}face.png", optimize=True)
        if not variant:
            plain = sets
        else:
            shaded = sets
    stand_h, sit_h = measure(plain)
    print("touching the canvas's edge:", edges(plain) + edges(shaded) or "none")
    sidecar = {
        "id": "ranger", "face": "E",
        "foot": list(FOOT),
        "tall": {"stand": int(stand_h), "sit": int(sit_h)},
        "stride": {"walk": STRIDE, "run": RUN_STRIDE},
        "pace": PACE,
        "frames": made,
        "fps": {"stand": 1.5, "sit": 1.5, "walk": 8, "run": 10, "nibble": 6, "wash": 5, "reach": 2, "look": 1, "walkN": 8, "walkS": 8},
        "fidgets": ["look", "wash"],
        "portrait": "art/portraits/ranger-face.png",
        "variants": {"shades": {"prefix": "ranger-shades-", "portrait": "art/portraits/ranger-shades-face.png"}},
    }
    with open(f"{OUT}/ranger.json", "w") as f:
        json.dump(sidecar, f, indent=2)
    sheet({**plain, **{"shades " + k: v for k, v in shaded.items()}}, "out/nevada-ranger-sheet.png")
    walk_strip(plain["walk"], "out/nevada-ranger-walk.png")
    walk_strip(plain["run"], "out/nevada-ranger-run.png", stride=RUN_STRIDE)
    print("ranger:", sum(len(v) for v in made.values()), "frames a variant;", "tall", sidecar["tall"])

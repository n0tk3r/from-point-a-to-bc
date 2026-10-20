"""The painting's world, in metres (highway_drive.py, ROAD-18P): everything highway.py paints on its plain and its road,
read out of highway.py's own code, so that the drive's pictures are the painting's and the camera can stop in it.

highway.py places its things in centimetres from the middle of the road (`across`) and from the lens (`z`), and paints
them through its camera (persp.Camera(330, 577): the horizon on row 330, the focal length 800 px, the eye 270.16 cm up).
Nothing here copies those lists: `painted()` runs highway.py's own `under()` with its light switched part by part, and
`details_until_things()` runs highway.py's own `details()` up to the moment it has sorted its things (the source is read
and cut there, and run in highway's own namespace, so every random number falls as it does in the painting). From those:

  things()      every standing thing of the painting, far first: bushes, tufts, stones, the fence posts, the reflector
                posts, the poles, the windpump, the two tumbleweeds, the jackrabbit, the hubcap, the bottle, the tread
  road_marks()  every mark details() lays on the road, in metres: the worn white edge lines, the yellow dashes, the cracks
                across and along, the two mended patches, the old brake marks (with their colours and widths)
  birds()       the three birds on the top wire between the first two poles
  SIGN_M        the sign, in metres

THE CONTRACT'S CAMERA (S/briefs/ROAD-18.md): x = 400 + 800 X / z, y = 330 + 800 (2.70 - Y) / z, X metres right of the
middle of the road, z ahead, Y up. The painting's eye is 2.7016 m (CAM.eye): 0.16 px lower at the bottom of the picture,
0.07 px at the sign; the drive's sprites are footed by the contract's 2.70, so the engine puts them where the painting has
them (see highway_drive_things.py)."""

import inspect
import math
import textwrap

import numpy as np

import highway as HW

F32 = np.float32
HZ, VX, FOCAL, EYE = 330.0, 400.0, 800.0, 2.70           # the contract's camera
EYE_PAINT = HW.CAM.eye / 100.0                             # the painting's own: 2.7016 m
W, H = 800, 600
STOP_SIGN_Z = HW.SIGN["z"] / 100.0                         # 17.3 m: where the sign is when the camera stops

SIGN_M = dict(z=STOP_SIGN_Z, x0=HW.SIGN["x0"] / 100, x1=HW.SIGN["x1"] / 100, lo=HW.SIGN["lo"] / 100, hi=HW.SIGN["hi"] / 100,
              posts=tuple(p / 100 for p in HW.SIGN["posts"]))


def stage(X, z, Y=0.0, eye=EYE):
    """The contract's projection: (x, y) on the stage of a point X right, z ahead, Y up (metres)."""
    return VX + FOCAL * X / z, HZ + FOCAL * (eye - Y) / z


def air(z):
    """How much of the painting's air lies over a thing z metres ahead: highway.airy() at the row of its foot
    (t = 0.72 (1 - (row - 330) / 110) ** 1.7, none nearer than 19.6 m), toward #f2a878."""
    row = HZ + EYE_PAINT * FOCAL / np.maximum(z, 1e-3)
    return 0.72 * np.clip(1 - (row - HZ) / 110.0, 0, 1) ** 1.7


# ---------------------------------------------------------------- highway.py's own code, run in its own namespace
def _source(fn, cuts):
    """The source of one of highway's functions, dedented, with `cuts` applied: [(text that must be there once, text
    to put in its place)]."""
    src = textwrap.dedent(inspect.getsource(fn))
    for old, new in cuts:
        if src.count(old) != 1:
            raise SystemExit(f"highway.{fn.__name__} is not what highway_drive_world.py expects (looking for {old.strip()!r})")
        src = src.replace(old, new)
    return src


def _run(fn, cuts, extra=None, transform=None):
    ns = dict(HW.__dict__)
    ns.update(extra or {})
    src = _source(fn, cuts)
    exec(transform(src) if transform else src, ns)
    return ns[fn.__name__]


# under()'s light, line by line: each can be switched off, so that the ground can be read as it is painted (its
# colours by distance) apart from the light laid over it (the shine, the glows, the long shadows, the deep corners)
_LIGHTS = {
    "glow_horizon": '    glow(pic, "#ffc880",',
    "glow_sun": '    glow(pic, "#ffd08a",',
    "shine": '    glow(pic, "#ffdc9a",',
    "tracks": '            glow(pic, "#ffc890",',
    "shadows": '    tint(pic, "#5c4a86",',
    "corners": '    tint(pic, "#6a4a78",',
}


_STREAK = "    streak = land.texture(shape, HZ, seed + 53, 40.0, 3, stretch=0.25)\n"


def under(seed=HW.SEED, off=(), even=False, smooth=False):
    """highway.under(), with the lights named in `off` left out. -> (picture, info). `even`: the shine down the road
    not broken by the surface (its streaks at their mean): a light that stays on the stage while the road goes by
    under it cannot carry the road's own breaks, which must go by with the road. `smooth`: every texture and noise of
    under()'s own at its mean (0.5): its ground as pure ramps by distance, the road's and the sand's edges straight (for
    the light pictures, which must carry none of the painting's blotches: those go by with the ground)."""
    cuts = []
    for name in off:
        line = _LIGHTS[name]
        indent = line[:len(line) - len(line.lstrip())]
        cuts.append((line, indent + "if False: " + line.lstrip()))
    if even:
        cuts.append((_STREAK, _STREAK.replace("land.texture(shape, HZ, seed + 53, 40.0, 3, stretch=0.25)", "np.full(shape, 0.5, dtype=F32)")))
    if smooth:
        flat = lambda shape, *a, **k: np.full(shape, 0.5, dtype=F32)
        fn = _run(HW.under, cuts, {"_SMOOTH": flat}, lambda s: s.replace("land.texture(", "_SMOOTH(").replace("noise(", "_SMOOTH("))
    else:
        fn = _run(HW.under, cuts) if cuts else HW.under
    return fn(seed)


_UNTIL_THINGS = [("    things.sort(key=lambda t: -t[1])\n", "    things.sort(key=lambda t: -t[1])\n    _KEEP['things'] = list(things)\n    return pic\n")]


def details_until_things(pic, info, seed=HW.SEED, extra=None):
    """highway.details() as far as the sorting of its things: the sky's crisp edges and stars, the mesas, the horizon,
    the road's lines, cracks and patches, the shadows' second pass. Nothing standing is drawn: no wire, bird, pole, sign,
    bush or post. -> (picture, the things list, the namespace it ran in)."""
    keep = {}
    ns_extra = {"_KEEP": keep}
    ns_extra.update(extra or {})
    fn = _run(HW.details, _UNTIL_THINGS, ns_extra)
    out = fn(pic, info, seed)
    return out, keep["things"]


# ---------------------------------------------------------------- the things
def things(info=None):
    """Every standing thing of the painting, far first, as highway.details() lists them:
    [{kind, X, z (metres), and what the painting draws it with}]. `info`: highway.under()'s (made here if not given)."""
    if info is None:
        base, info = HW.under()
        info["under"] = base
    pic = info["under"].copy()
    _, raw = details_until_things(pic, info)
    out = []
    for i, (kind, z, what) in enumerate(raw):
        t = {"kind": kind, "z": z / 100.0, "order": i}
        if kind == "bush":
            ax, _, wide, tall, k = what
            t.update(X=ax / 100, wide=wide / 100, tall=tall / 100, seed=int(k))
        elif kind in ("tuft", "stone"):
            ax, _, size, k = what
            t.update(X=ax / 100, size=size / 100, seed=int(k))
        elif kind == "post":
            ax, _, tall, lean = what
            t.update(X=ax / 100, tall=tall / 100, lean=float(lean))
        elif kind == "pole":
            ax, _, i_ = what
            t.update(X=ax / 100, index=int(i_), seed=HW.SEED + 500 + int(i_), fade=float(np.clip(1.15 - i_ * 0.14, 0.3, 1.0)))
        elif kind == "weed":
            ax, _, size = what
            t.update(X=ax / 100, size=size / 100, seed=HW.SEED + 710 + int(z))
        else:                                                  # marker, pump, hubcap, bottle, tread, rabbit
            t.update(X=what[0] / 100)
        out.append(t)
    return out


# ---------------------------------------------------------------- the road's marks, in metres
class _WPt(tuple):
    """A point of the picture that remembers where it is in the world (across cm, up cm, z cm from the lens)."""
    w = None


def _P_recording(across, up, z):
    p = _WPt(HW.CAM.pt(across, up, z - HW.CAM.Z0))
    p.w = (float(across), float(up), float(z))
    return p


class _Recorder:
    """Stands in for a Paper: keeps every mark laid on it, draws nothing."""
    made = []

    def __init__(self, shape, ss=3):
        self.shape, self.marks = shape, []
        _Recorder.made.append(self)

    def poly(self, points, color, alpha=1.0):
        self.marks.append(("poly", list(points), color, None, alpha)); return self

    def line(self, points, color, width=1.0, alpha=1.0, round_ends=True):
        self.marks.append(("line", list(points), color, width, alpha)); return self

    def taper(self, points, color, w0, w1, alpha=1.0):
        self.marks.append(("taper", list(points), color, (w0, w1), alpha)); return self

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0):
        self.marks.append(("ellipse", [(cx, cy)], color, (rx, ry), alpha)); return self

    def clear(self, points):
        return self

    def done(self):
        h, w = self.shape
        return np.zeros((h, w, 3), F32), np.zeros((h, w), F32)

    def onto(self, picture, amount=1.0):
        return picture


def _hexof(c):
    if isinstance(c, str):
        return c
    c = np.clip(np.asarray(c, F32), 0, 1)
    return "#%02x%02x%02x" % tuple(int(round(v * 255)) for v in c)


def road_marks(info):
    """The marks details() lays on the road, in metres: [{what, pts: [(X, z)], color, width (m, at each point, or
    None for a filled shape), alpha}], what one of: edge-line, dash, crack, seam, patch, patch-edge, brake."""
    _Recorder.made = []
    pic = info["under"].copy()
    details_until_things(pic, info, extra={"P": _P_recording, "Paper": _Recorder})
    # the Papers details() makes before its things, in order: stars, the mesas' edges, the road's lines (rd), its cracks
    # (ck), the thin shadows (shadows() makes its own, with highway's real Paper)
    papers = _Recorder.made
    rd, ck = papers[2], papers[3]
    out = []

    def world(pts):
        return [(p.w[0] / 100.0, p.w[2] / 100.0) for p in pts]

    for kind, pts, color, width, alpha in rd.marks:
        wp = world(pts)
        X = [p[0] for p in wp]
        what = "dash" if max(abs(v) for v in X) < 0.5 else "edge-line"
        out.append({"what": what, "pts": wp, "color": _hexof(color), "width": None, "alpha": float(alpha)})
    for kind, pts, color, width, alpha in ck.marks:
        if not all(isinstance(p, _WPt) for p in pts):
            continue
        wp = world(pts)
        zs = [p.w[2] for p in pts]
        if kind == "taper":                                    # the brake marks: widths in px, from the near end to the far
            n = len(pts)
            w_px = [width[0] + (width[1] - width[0]) * i / max(n - 2, 1) for i in range(n)]
            wm = [wpx / (FOCAL / z) / 100.0 for wpx, z in zip(w_px, zs)]
            out.append({"what": "brake", "pts": wp, "color": _hexof(color), "width": wm, "alpha": float(alpha)})
        elif kind == "poly":
            out.append({"what": "patch", "pts": wp, "color": _hexof(color), "width": None, "alpha": float(alpha)})
        else:
            wm = [width / (FOCAL / z) / 100.0 for z in zs]
            # a patch's ring edges are its own colour; cracks across run sideways (X changes most), seams along
            dX, dz = abs(wp[-1][0] - wp[0][0]), abs(wp[-1][1] - wp[0][1])
            what = "patch-edge" if _hexof(color) == "#3a3052" else ("crack" if dX > dz else "seam")
            out.append({"what": what, "pts": wp, "color": _hexof(color), "width": wm, "alpha": float(alpha)})
    return out


def birds():
    """The three birds on the top wire between the first two poles: [{X, z, Y (m), size (m), facing}], as details()
    places them (on the wire's run whose first point is nearest the top of the picture, at x 150, 161 and 196)."""
    sheet = _Recorder((H, W))
    runs = HW.wires(sheet, HW.SEED + 9)
    top = min((r_ for r_ in runs if 60 < r_[0][0] < 140 and r_[-1][0] > 250), key=lambda r_: r_[0][1])
    # that run again in the world: wires() goes from pole a to pole b in 25 steps, those nearer than 4.3 m left out
    pegs = [(-104.0, 824.0), (-58.0, 824.0), (58.0, 824.0), (104.0, 824.0), (-80.0, 746.0), (80.0, 746.0)]
    spans = [((HW.POLES[0][0], HW.POLES[0][1] - 4000.0), HW.POLES[0])] + [(HW.POLES[i], HW.POLES[i + 1]) for i in range(len(HW.POLES) - 1)]
    found = None
    for (a, b) in spans:
        for k, (dx, hgt) in enumerate(pegs):
            sag = 105.0 + 30.0 * math.sin(k * 1.7 + a[1] * 0.001)
            pts, wpts = [], []
            for i in range(25):
                u = i / 24
                z = a[1] + (b[1] - a[1]) * u
                if z < 430:
                    continue
                X_ = a[0] + (b[0] - a[0]) * u + dx
                Y_ = hgt - 4 * sag * u * (1 - u)
                pts.append(HW.P(X_, Y_, z))
                wpts.append((X_, Y_, z))
            if len(pts) == len(top) and np.allclose(np.array(pts), np.array(top)):
                found = wpts
    out = []
    for bx, size, facing in ((150.0, 6.4, 1), (161.0, 5.6, 1), (196.0, 6.4, -1)):
        j = max(i for i, p_ in enumerate(top) if p_[0] <= bx)
        j = min(j, len(top) - 2)
        f_ = (bx - top[j][0]) / max(top[j + 1][0] - top[j][0], 1e-3)
        a_, b_ = found[j], found[j + 1]
        Xc, Yc, zc = (a_[q] + (b_[q] - a_[q]) * f_ for q in range(3))
        by = top[j][1] + (top[j + 1][1] - top[j][1]) * f_ + 0.3              # (details: the bird's feet 0.3 px under the wire)
        s = FOCAL / zc                                                       # px a cm there
        out.append({"X": Xc / 100, "z": zc / 100, "Y": Yc / 100 - 0.3 / s / 100, "size": size / s / 100, "facing": facing,
                    "at": (bx, by), "size_px": size})
    return out


# ---------------------------------------------------------------- the painting's things, one at a time
class _Tee:
    """Stands in for highway's Paper in details(): draws on a real one, and keeps every mark of the thing being drawn, so
    that the thing can be drawn again alone."""
    current = None

    def __init__(self, shape, ss=3):
        self.inner = HW.Paper(shape, ss)
        self.shape, self.ss = shape, ss

    def _keep(self, rec):
        if _Tee.current is not None:
            _Tee.current.append(rec)

    def poly(self, points, color, alpha=1.0):
        self._keep(("poly", [(float(x), float(y)) for x, y in points], color, alpha))
        self.inner.poly(points, color, alpha)
        return self

    def line(self, points, color, width=1.0, alpha=1.0, round_ends=True):
        self._keep(("line", [(float(x), float(y)) for x, y in points], color, width, alpha, round_ends))
        self.inner.line(points, color, width, alpha, round_ends)
        return self

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0):
        self._keep(("ellipse", float(cx), float(cy), float(rx), float(ry), color, alpha))
        self.inner.ellipse(cx, cy, rx, ry, color, alpha)
        return self

    def taper(self, points, color, w0, w1, alpha=1.0):
        self._keep(("taper", [(float(x), float(y)) for x, y in points], color, w0, w1, alpha))
        self.inner.taper(points, color, w0, w1, alpha)
        return self

    def clear(self, points):
        self.inner.clear(points)
        return self

    def done(self):
        return self.inner.done()

    def onto(self, picture, amount=1.0):
        return self.inner.onto(picture, amount)


def marks_box(marks, pad=2, size=(H, W)):
    """The pixels a thing's marks can touch (within a picture of `size`; None: wherever they are): (x0, y0, x1, y1), or
    None."""
    xs, ys = [], []
    for m in marks:
        if m[0] == "poly":
            for x, y in m[1]:
                xs.append(x); ys.append(y)
        elif m[0] in ("line", "taper"):
            r = (m[3] if m[0] == "line" else max(m[3], m[4])) / 2 + 1
            for x, y in m[1]:
                xs += [x - r, x + r]; ys += [y - r, y + r]
        else:
            _, cx, cy, rx, ry = m[:5]
            xs += [cx - rx, cx + rx]; ys += [cy - ry, cy + ry]
    if not xs:
        return None
    x0, y0 = int(math.floor(min(xs))) - pad, int(math.floor(min(ys))) - pad
    x1, y1 = int(math.ceil(max(xs))) + pad + 1, int(math.ceil(max(ys))) + pad + 1
    if size is not None:
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(size[1], x1), min(size[0], y1)
    return (x0, y0, x1, y1) if x1 > x0 and y1 > y0 else None


def replay(marks, box, ss=3):
    """A thing drawn again alone, on a Paper the size of its box (moved by whole pixels, so every edge falls as it
    did): -> (colour, coverage)."""
    x0, y0, x1, y1 = box
    p = HW.Paper((y1 - y0, x1 - x0), ss)
    for m in marks:
        if m[0] == "poly":
            p.poly([(x - x0, y - y0) for x, y in m[1]], m[2], m[3])
        elif m[0] == "line":
            p.line([(x - x0, y - y0) for x, y in m[1]], m[2], m[3], m[4], m[5])
        elif m[0] == "taper":
            p.taper([(x - x0, y - y0) for x, y in m[1]], m[2], m[3], m[4], m[5])
        else:
            _, cx, cy, rx, ry, color, alpha = m
            p.ellipse(cx - x0, cy - y0, rx, ry, color, alpha)
    return p.done()


def _composite(sheet, pic, box):
    """What the painting shows in `box` if its sheet were laid on it now."""
    x0, y0, x1, y1 = box
    ss = sheet.ss
    part = sheet.inner.im.crop((x0 * ss, y0 * ss, x1 * ss, y1 * ss)).resize((x1 - x0, y1 - y0), HW.Image.BOX)
    a = np.asarray(part, F32) / 255
    c = pic[y0:y1, x0:x1].copy()
    return c * (1 - a[..., 3:4]) + a[..., :3] * a[..., 3:4]


def details_one_by_one(pic, info, seed=HW.SEED):
    """highway.details() whole, exactly as the painting runs it (its every mark is drawn on a real Paper), and on the
    way, for every standing thing in its queue (far first): the marks it laid, the box they touch, and what the painting
    shows in that box just after the thing was drawn (before anything nearer). And the same for the sign.
    -> (the finished picture, [{kind, z, what, marks, box, after}], {box, after} for the sign)."""
    records, state, sign = [], {"prev": None}, {}

    def finish_prev(sheet, pic_):
        prev = state["prev"]
        if prev is None:
            return
        prev["box"] = marks_box(prev["marks"])
        prev["after"] = _composite(sheet, pic_, prev["box"]) if prev["box"] else None
        records.append(prev)
        state["prev"] = None

    def hook(kind, z, what, sheet, pic_):
        finish_prev(sheet, pic_)
        if kind is None:
            _Tee.current = None
            return
        rec = {"kind": kind, "z": z, "what": what, "marks": []}
        state["prev"] = rec
        _Tee.current = rec["marks"]

    def sign_hook(pic_):
        sign["after"] = pic_.copy()

    cuts = [("    for kind, z, what in things:\n", "    for kind, z, what in things:\n        _HOOK(kind, z, what, sheet, pic)\n"),
            ('            info["sign"] = the_sign(pic, seed + 400)\n', '            info["sign"] = the_sign(pic, seed + 400)\n            _SIGN_HOOK(pic)\n'),
            ("    if not sign_done:\n", "    _HOOK(None, None, None, sheet, pic)\n    if not sign_done:\n")]
    _Tee.current = None
    fn = _run(HW.details, cuts, {"Paper": _Tee, "_HOOK": hook, "_SIGN_HOOK": sign_hook})
    out = fn(pic, info, seed)
    _Tee.current = None
    return out, records, sign

"""Checks on the highway's pictures for the drive (highway_drive.py, ROAD-18P), and the chase view drawn as the engine
draws it, with the contract's own formulas, before the engine is there.

    python3 highway_drive_check.py [pictures folder] [scene folder]
        pictures folder: out/highway (the paintings, default), or the scene's folder in the game as installed, keyed
                         (../../art/scenes/highway from tools/paint)
        scene folder: where back.png, sun.png and the wagon are (default: the pictures folder)

THE CONTRACT (S/briefs/ROAD-18.md): x = 400 + 800 X / z, y = 330 + 800 (2.70 - Y) / z. A moment is drawn as the engine's
drive straight ahead draws it (effects.js, ROAD-18E, as it stood when this was written): sky.png, still, with the sun's
disc on it (the live layer); over them the drive's pane: below the horizon each pixel's patch of ground read from the
strip under it (its row (X - from) * ppm, its column ((z + s) * ppm) mod width), averaged over the patch it sees (along
the road and across: no shimmer; longer along by the streak while moving), beyond the outermost strips their outer rows'
colour, the haze over it as far off as its middle (1 - 2^(-d / haze_far)): toward a colour, or (`haze: "backdrop"`) into
clear, so that sky.png's own far plain shows through; the things' shadows multiplied on it (sun [-5.5, 0]: 5.5 m toward
us for a metre of height, as wide as the thing is at each height); the lights laid on it as the canvas lays them (over a
pane that is part clear where the haze is backdrop); then the things far to near, each at 800 / z / ppm of its size
(smaller: averaged; larger: hard pixels; at its own size within a fifth of a percent: pixel for pixel), as solid as
1 - haze * its "air"; the wires; the wagon.

It writes, into out/highway-drive-check/ (or -installed/):
    cruise-a.png, cruise-b.png    the chase view cruising (the wagon at row 548), a quarter of a second apart at 25 m/s,
                                  with a haze colour (the contract's way)
    cruise-backdrop.png           the same moment as cruise-a with `haze: "backdrop"`
    stop.png, stop-backdrop.png   the camera stopped where the painting is (drive-stop.json's things placed), both hazes
    stop-vs-back.png              stop.png (top) and stop-backdrop.png (below) beside back.png with sun.png; the
                                  difference (four times over) of each in the third column
    approach.png                  four moments as the camera comes up to the stop (60, 30, 10 and 0 m before it)
    title-a.png, title-b.png      the title's cruise (no sign), a quarter of a second apart
    film.png                      the road under the wagon every 0.1 s for half a second (the motion)
and checks the numbers: every file, its size and its palette; the loops' seams; the strips meeting across; the dashes'
rhythm; the sheet's boxes, feet and heights; the sign landing on the painting's board; drive-stop.json; the lights."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

import highway_drive_kit as K

F32 = np.float32
HZ, VX, FOCAL, EYE = K.HZ, K.VX, K.FOCAL, K.EYE
W, H = K.W, K.H
SPEED, FPS, STREAK = 25.0, 30.0, 0.6
FAR = 2000.0                                       # the engine's `far`: no ground beyond (the backdrop shows)
SUN = (-5.5, 0.0)                                  # the contract's: shadows 5.5 m toward us a metre of height
SHADE, SHADE_K = "#5c4a86", 0.55                   # the things' shadows (highway.under: #5c4a86 at 0.5, then #5a467e at 0.4)
WIRE = (42, 28, 54)
STOP_AT = 1280.0                                   # the camera stops at s = 1280: a whole number of loops (64 m) and of poles (40 m)
# the hazes: a colour (the contract's way) and the backdrop (the engine's `haze: "backdrop"`); the numbers are fitted below
COLOR = dict(mode="color", haze=K.HAZE, haze_far=K.HAZE_FAR)
BACKDROP = dict(mode="backdrop", haze=None, haze_far=90.0)

# The rows of things (the preview's own placement: the merge's engine places its own from its seed). At the painting's
# density near the road (highway.bushes(): about 17 bushes in 100 m2 within 12 m of the road from 15 to 40 m ahead,
# about 6 from 12 to 30 m out; tufts all along the edge of the paving; stones) and thinning out; Joshua trees now and
# then. Phased so that the poles, the reflector posts and the fences stand where the painting has them when the camera
# stops at STOP_AT; the rest are kept off the stretch the painting's own things (drive-stop.json) hold then (GAP).
ROWS = [
    {"sprite": "pole", "every": 40.0, "at": -7.5, "phase": 18.0, "wires": "pole"},
    {"sprite": "post", "every": 18.0, "at": 3.52, "phase": 12.4},
    {"sprite": "post", "every": 18.0, "at": -3.52, "phase": 21.4},
    {"sprite": ["fence-1-l", "fence-2-l"], "every": 5.2, "at": -14.6, "phase": 23.4, "wires": [1.09, 0.65]},
    {"sprite": ["fence-1-r", "fence-2-r"], "every": 5.2, "at": 14.6, "phase": 23.4, "wires": [1.09, 0.65]},
    {"sprite": ["sage-1", "sage-2", "sage-3", "sage-4", "sage-5", "sage-6"], "every": [0.15, 0.6], "at": [4.4, 12.0], "both": True, "gap": True},
    {"sprite": ["sage-1-mid", "sage-2-mid", "sage-3-mid", "sage-4-mid"], "every": [0.3, 0.9], "at": [12.0, 30.0], "both": True, "gap": True},
    {"sprite": ["sage-1-far", "sage-2-far", "sage-3-far", "sage-4-far"], "every": [0.4, 1.2], "at": [30.0, 80.0], "both": True, "gap": True},
    {"sprite": ["tuft-1", "tuft-2"], "every": [0.5, 1.5], "at": [3.15, 4.4], "both": True, "gap": True},
    {"sprite": ["tuft-1", "tuft-2", "tuft-1"], "every": [0.5, 1.5], "at": [4.4, 30.0], "both": True, "gap": True},
    {"sprite": ["stone-1", "stone-2", "stone-3", "stone-1", "stone-1"], "every": [0.4, 1.2], "at": [3.25, 8.0], "both": True, "gap": True},
    {"sprite": ["stone-1", "stone-2", "stone-1"], "every": [0.5, 1.5], "at": [8.0, 30.0], "both": True, "gap": True},
    {"sprite": ["joshua-1", "joshua-2"], "every": [60.0, 160.0], "at": [9.0, 60.0], "both": True, "gap": True},
    {"sprite": "tumbleweed", "every": [150.0, 400.0], "at": [3.6, 14.0], "both": True, "gap": True},
]
GAP = (4.0, 170.0)                                 # metres ahead of the stopped camera that the painting's own things hold
POLE_WIRES = [(-1.04, 8.24), (-0.58, 8.24), (0.58, 8.24), (1.04, 8.24), (-0.80, 7.46), (0.80, 7.46)]
LIGHTS = [("shade", "multiply"), ("glow", "screen")]       # in this order (highway_drive_sky.py: the two, made for COLOR)


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], F32)


def load(folder, name, mode="RGBA"):
    return np.asarray(Image.open(os.path.join(folder, name)).convert(mode), F32) / 255.0


# ---------------------------------------------------------------- the ground
class Strip:
    def __init__(self, folder, name):
        self.name = name
        self.lo, self.hi, self.ppm = K.STRIPS[name]
        self.pic = load(folder, f"drive-{name}.png", "RGB")
        h, w, _ = self.pic.shape
        self.h, self.w = h, w
        self.P = np.concatenate([np.zeros((h, 1, 3), F32), np.cumsum(self.pic, axis=1, dtype=np.float64).astype(F32)], axis=1)

    def along(self, a, b):
        """Each row's average from column a to b (fractional, wrapping): -> (h, 3)."""
        def S(u):
            k = math.floor(u)
            loops, m = divmod(k, self.w)
            f = u - k
            return self.P[:, -1] * loops + self.P[:, m] + self.pic[:, m] * f
        if b - a < 1e-6:
            return self.pic[:, int(math.floor(a)) % self.w]
        return (S(b) - S(a)) / (b - a)


def ground(strips, s, travel=0.0):
    """The ground below the horizon as the engine draws it at s (metres gone), before the haze: -> (colours, how far off
    each pixel's middle is along the ground (inf where there is no ground), X of each pixel's middle)."""
    out = np.zeros((H, W, 3), F32)
    xs = np.arange(W, dtype=F32)
    dist = np.full((H, W), np.inf, F32)
    Xmap = np.zeros((H, W), F32)
    for y in range(int(HZ), H):
        v0 = y - HZ
        zc = FOCAL * EYE / (v0 + 0.5)
        if zc > FAR:
            continue
        z_lo, z_hi = FOCAL * EYE / (v0 + 1), FOCAL * EYE / max(v0, 1e-3)
        ext = (travel - (z_hi - z_lo)) / 2 if travel > z_hi - z_lo else 0.0          # (the streak)
        X0 = (xs - VX) * zc / FOCAL
        X1 = (xs + 1 - VX) * zc / FOCAL
        Xc = (X0 + X1) / 2
        col = np.zeros((W, 3), F32)
        for st in strips:
            v = st.along((z_lo + s - ext) * st.ppm, (z_hi + s + ext) * st.ppm)
            Q = np.concatenate([np.zeros((1, 3), F32), np.cumsum(v, axis=0)], 0)

            def Sq(r):
                r = np.clip(r, 0, st.h)
                k = np.minimum(np.floor(r).astype(np.intp), st.h - 1)
                return Q[k] + v[k] * (r - k)[:, None]

            sel = (Xc >= st.lo) & (Xc < st.hi)
            if st.lo <= min(o.lo for o in strips):                  # (the outermost strips carry their outer rows on)
                sel |= Xc < st.lo
            if st.hi >= max(o.hi for o in strips):
                sel |= Xc >= st.hi
            if not sel.any():
                continue
            r0 = (np.minimum(X0[sel], X1[sel]) - st.lo) * st.ppm
            r1 = (np.maximum(X0[sel], X1[sel]) - st.lo) * st.ppm
            beyond_lo, beyond_hi = r1 <= 0, r0 >= st.h
            r0c, r1c = np.clip(r0, 0, st.h), np.clip(r1, 0, st.h)
            span = np.maximum(r1c - r0c, 1e-6)
            c = (Sq(r1c) - Sq(r0c)) / span[:, None]
            thin = (r1c - r0c) < 1e-5
            if thin.any():
                c[thin] = v[np.clip(np.floor(r0c[thin]).astype(np.intp), 0, st.h - 1)]
            c[beyond_lo] = v[:8].mean(0)
            c[beyond_hi] = v[-8:].mean(0)
            col[sel] = c
        out[y] = col
        dist[y] = zc * np.sqrt(1 + ((xs + 0.5 - VX) / FOCAL) ** 2)
        Xmap[y] = Xc
    return out, dist, Xmap


# ---------------------------------------------------------------- the things
class Sheet:
    def __init__(self, folder):
        self.pic = load(folder, "drive-things.png")
        self.meta = json.load(open(os.path.join(folder, "drive-things.json")))
        self.cache, self.profiles = {}, {}

    def sprite(self, name):
        s = self.meta["sprites"][name]
        x, y, w, h = s["box"]
        return self.pic[y:y + h, x:x + w], s

    def at(self, name, k):
        """The sprite at k times its size, premultiplied: averaged smaller, hard pixels larger, itself at k = 1."""
        key = (name, round(k, 3))
        if key in self.cache:
            return self.cache[key]
        pic, s = self.sprite(name)
        h, w = pic.shape[:2]
        pm = pic.copy()
        pm[..., :3] *= pm[..., 3:4]
        if abs(k - 1) < 0.002:
            out = pm
        else:
            W_, H_ = max(1, int(round(w * k))), max(1, int(round(h * k)))
            how = Image.BOX if k < 1 else Image.NEAREST
            out = np.dstack([np.asarray(Image.fromarray(np.ascontiguousarray(pm[..., i]), "F").resize((W_, H_), how), F32) for i in range(4)])
        res = (out, s["foot"][0] * (out.shape[1] / w), s["foot"][1] * (out.shape[0] / h))
        self.cache[key] = res
        return res

    def profile(self, name):
        """How wide the thing is (metres) at each height (metres) above its foot: its solid pixels row by row."""
        if name in self.profiles:
            return self.profiles[name]
        pic, s = self.sprite(name)
        ppm = s.get("ppm", self.meta["ppm"])
        fy = s["foot"][1]
        a = pic[..., 3] >= 0.5
        out = []
        for r in range(a.shape[0]):
            n = int(a[r].sum())
            if n:
                out.append(((fy - r - 0.5) / ppm, n / ppm))
        out = sorted(out)[::max(1, len(out) // 24)]
        self.profiles[name] = out
        return out


def place_rows(sheet, s_lo, s_hi, seed=18, stop_at=None):
    """The rows' things from s_lo to s_hi metres along the road: [{sprite, X, w}]. (The preview's own placement.)"""
    out = []
    for i, r in enumerate(ROWS):
        rng = np.random.default_rng(seed * 100 + i)
        names = r["sprite"] if isinstance(r["sprite"], list) else [r["sprite"]]
        ev = r["every"]
        if "phase" in r:
            base = (stop_at if stop_at is not None else STOP_AT) + r["phase"]
            for k in range(math.floor((s_lo - base) / ev) - 1, math.ceil((s_hi - base) / ev) + 2):
                w = base + k * ev
                name = names[k % len(names)]
                X = r["at"]
                if "fence" in name:                                         # (the painting's fences wander a little)
                    j = np.random.default_rng((k * 7 + i) % (1 << 32))
                    w += float(j.normal(0, 0.3))
                    X += float(j.normal(0, 0.14))
                out.append({"sprite": name, "X": X, "w": w, "row": i})
            continue
        lo, hi = ev
        w = math.floor(s_lo / 400.0) * 400.0 - hi                         # (the same things for the same stretch)
        rng = np.random.default_rng((seed * 100 + i + int(w // 400) * 7919) % (1 << 32))
        while w < s_hi:
            w += rng.uniform(lo, hi)
            X = rng.uniform(*r["at"])
            side = -1 if (r.get("both") and rng.random() < 0.5) else 1
            name = names[int(rng.integers(len(names)))]
            if w < s_lo - 10:
                continue
            if r.get("gap") and stop_at is not None and stop_at + GAP[0] <= w <= stop_at + GAP[1]:
                continue
            Xs = side * X
            full = f"{name}-{'l' if Xs < 0 else 'r'}" if f"{name}-l" in sheet.meta["sprites"] else name
            out.append({"sprite": full, "X": Xs, "w": w, "row": i})
    return out


def shadows_mask(sheet, items, s):
    """The things' shadows on the ground, as the engine lays them (one shape, filled once): a band from each foot toward
    us, 5.5 m a metre of height, as wide as the thing at each height. -> mask (H, W)."""
    im = Image.new("L", (W * 2, H * 2), 0)
    dr = ImageDraw.Draw(im)
    for it in items:
        z = it["w"] - s
        if z < 1.5 or z > 600 or it.get("Y"):
            continue
        prof = sheet.profile(it["sprite"])
        left, right = [], []
        for Y, wd in prof:
            zz = z + SUN[0] * Y
            if zz < 1.0:
                break
            for side, lst in ((-1, left), (1, right)):
                X = it["X"] + side * max(wd / 2, 0.05)
                lst.append((2 * (VX + FOCAL * X / zz), 2 * (HZ + FOCAL * EYE / zz)))
        if len(left) >= 2:
            dr.polygon(left + right[::-1], fill=255)
    return np.asarray(im.resize((W, H), Image.BOX), F32) / 255


def haze_at(X, z, haze_far):
    return 1 - 0.5 ** (math.sqrt(X * X + z * z) / haze_far)


def draw_things(stage, sheet, items, s, haze_far):
    vis = [(it["w"] - s, it) for it in items]
    vis = [(z, it) for z, it in vis if 1.5 < z < 900]
    vis.sort(key=lambda q: -q[0])
    for z, it in vis:
        spr = sheet.meta["sprites"][it["sprite"]]
        ppm = spr.get("ppm", sheet.meta["ppm"])
        k = FOCAL / z / ppm
        if spr["box"][3] * k < 1.0:
            continue
        a = 1 - haze_at(it["X"], z, haze_far) * spr.get("air", 1)
        img, fx, fy = sheet.at(it["sprite"], k)
        sx = VX + FOCAL * it["X"] / z
        sy = HZ + FOCAL * EYE / z
        if abs(k - 1) < 0.002:
            x0, y0 = int(math.floor(sx - fx + 0.5)), int(math.floor(sy - fy + 0.5))
        else:
            x0, y0 = int(round(sx - fx)), int(round(sy - fy))
        h, w = img.shape[:2]
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
        if xa >= xb or ya >= yb:
            continue
        part = img[ya - y0:yb - y0, xa - x0:xb - x0] * a
        stage[ya:yb, xa:xb] = stage[ya:yb, xa:xb] * (1 - part[..., 3:4]) + part[..., :3]


def draw_wires(stage, items, s, haze_far):
    im = Image.new("RGBA", (W * 2, H * 2), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    poles = sorted([it for it in items if it["row"] >= 0 and ROWS[it["row"]].get("wires") == "pole"], key=lambda it: it["w"])
    spans = []
    for a, b in zip(poles[:-1], poles[1:]):
        for dx, hgt in POLE_WIRES:
            spans.append((a, b, dx, hgt, 1.2))
    first = min((p for p in poles if p["w"] - s > 1.5), key=lambda p: p["w"], default=None)
    if first:                                                               # from the nearest out over the camera
        back = dict(first, w=first["w"] - 40.0)
        for dx, hgt in POLE_WIRES:
            spans.append((back, first, dx, hgt, 1.2))
    others = {}
    for it in items:
        if it["row"] >= 0 and isinstance(ROWS[it["row"]].get("wires"), list):
            others.setdefault(it["row"], []).append(it)
    for row, its in others.items():
        its = sorted(its, key=lambda it: it["w"])
        for a, b in zip(its[:-1], its[1:]):
            for hgt in ROWS[row]["wires"]:
                spans.append((a, b, 0.0, hgt, 0.05))
    for a, b, dx, hgt, sag in spans:
        pts = []
        for i in range(25):
            u = i / 24
            z = a["w"] + (b["w"] - a["w"]) * u - s
            if z < 1.0:
                continue
            X = a["X"] + (b["X"] - a["X"]) * u + dx
            Y = hgt - 4 * sag * u * (1 - u)
            pts.append((2 * (VX + FOCAL * X / z), 2 * (HZ + FOCAL * (EYE - Y) / z)))
        if len(pts) >= 2:
            zm = max((a["w"] + b["w"]) / 2 - s, 1.0)
            al = (1 - haze_at(a["X"], zm, haze_far)) * (0.9 if hgt > 3 else 0.55)
            dr.line(pts, fill=WIRE + (int(255 * al),), width=2)
    w_ = np.asarray(im.resize((W, H), Image.BOX), F32) / 255
    stage[...] = stage * (1 - w_[..., 3:4]) + w_[..., :3] * w_[..., 3:4]


# ---------------------------------------------------------------- the canvas's blends, over a pane that may be part clear
def blend(P, A, Cs, As, how):
    """Lay a source (straight colour Cs, alpha As) on a premultiplied pane (P, A) as the canvas does. -> (P, A)."""
    As = As[..., None] if As.ndim == 2 else As
    if how == "screen":
        P2 = As * Cs + P * (1 - As * Cs)
    elif how == "multiply":
        P2 = As * Cs * (1 - A) + P * (1 - As + As * Cs)
    else:
        P2 = As * Cs + P * (1 - As)
    return P2, As + A * (1 - As)


class Lights:
    def __init__(self, folder):
        self.pics = {n: load(folder, f"light-{n}.png") for n, _ in LIGHTS}


def compose(backdrop, g, dist, shadow_m, lights, haze_cfg):
    """The drive's pane over the stage. -> picture."""
    hf = haze_cfg["haze_far"]
    below = np.isfinite(dist)
    h = np.where(below, 1 - np.power(0.5, np.where(below, dist, 0) / hf), 1.0)[..., None]
    A = below[..., None].astype(F32)
    if haze_cfg["mode"] == "color":
        P = (g * (1 - h) + hexrgb(haze_cfg["haze"]) * h) * A
    else:
        A = A * (1 - h)
        P = g * A
    P, A = blend(P, A, hexrgb(SHADE), shadow_m * SHADE_K * below, "multiply")
    for name, how in LIGHTS:
        L = lights.pics[name]
        P, A = blend(P, A, L[..., :3], L[..., 3], how)
    return P + (1 - A) * backdrop


def wagon(stage, scene, row=548.0):
    wg = load(scene, "wagon-rear-0.png")
    k = (row - HZ) / 518.4
    Wn, Hn = int(round(wg.shape[1] * k)), int(round(wg.shape[0] * k))
    pm = wg.copy()
    pm[..., :3] *= pm[..., 3:4]
    small = np.dstack([np.asarray(Image.fromarray(np.ascontiguousarray(pm[..., i]), "F").resize((Wn, Hn), Image.LANCZOS), F32) for i in range(4)])
    lane = VX + (row - HZ) * (150.0 / 270.0)
    x0, y0 = int(round(lane - 251 * k)), int(round(row - 419 * k))
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + Wn), min(H, y0 + Hn)
    part = np.clip(small[ya - y0:yb - y0, xa - x0:xb - x0], 0, 1)
    stage[ya:yb, xa:xb] = stage[ya:yb, xa:xb] * (1 - part[..., 3:4]) + part[..., :3]


class Moment:
    """One moment of the drive, its layers kept so that it can be laid with either haze."""

    def __init__(self, ctx, s, stop=None, moving=True, rows=True, pieces=True):
        self.ctx, self.s = ctx, s
        self.g, self.dist, _ = ground(ctx["strips"], s, STREAK * SPEED / FPS if moving else 0.0)
        items = place_rows(ctx["sheet"], s, s + 900.0, stop_at=stop) if rows else []
        if pieces and stop is not None:
            for p in ctx["pieces"]:
                if "row" in p:                                              # (the rows put the poles, posts and fences there)
                    continue
                items.append({"sprite": p["sprite"], "X": p["X"], "w": stop + p["z"], "row": -1})
        self.items = items
        self.shadow = shadows_mask(ctx["sheet"], items, s)

    def picture(self, haze_cfg, light=True, wagon_row=548.0):
        ctx = self.ctx
        backdrop = ctx["sky_sun"]
        if light:
            pic = compose(backdrop, self.g, self.dist, self.shadow, ctx["lights"], haze_cfg)
        else:
            dark = Lights.__new__(Lights)
            dark.pics = {n: np.zeros((H, W, 4), F32) for n, _ in LIGHTS}
            pic = compose(backdrop, self.g, self.dist, self.shadow, dark, haze_cfg)
        draw_things(pic, ctx["sheet"], self.items, self.s, haze_cfg["haze_far"])
        draw_wires(pic, self.items, self.s, haze_cfg["haze_far"])
        if wagon_row:
            wagon(pic, ctx["scene"], wagon_row)
        return np.clip(pic, 0, 1)


def save(pic, path, k=1):
    im = Image.fromarray((np.clip(pic, 0, 1) * 255 + 0.5).astype(np.uint8))
    if k != 1:
        im = im.resize((im.width * k, im.height * k), Image.NEAREST)
    im.save(path)


# ---------------------------------------------------------------- the numbers
NEW = ["sky.png", "drive-road.png", "drive-desert-l.png", "drive-desert-r.png", "drive-things.png", "drive-things.json",
       "drive-stop.json", "light-shade.png", "light-glow.png", "drive-far-l.png", "drive-far-r.png"]         # (PAINT-18B: the far strips)


def checks(folder):
    problems, notes = [], []

    def need(cond, msg):
        (notes if cond else problems).append(("ok    " if cond else "WRONG ") + msg)

    sizes = {"sky.png": (800, 600), "drive-road.png": (3072, 576), "drive-desert-l.png": (1536, 576), "drive-desert-r.png": (1536, 576),
             "light-glow.png": (800, 600), "light-shade.png": (800, 600), "drive-far-l.png": (512, 960), "drive-far-r.png": (512, 960)}
    total = 0
    for f in NEW:
        p = os.path.join(folder, f)
        if not os.path.exists(p):
            need(False, f"{f} is there")
            continue
        total += os.path.getsize(p)
        if f.endswith(".png"):
            im = Image.open(p)
            light = f.startswith("light-")
            need(im.mode == ("RGBA" if light else "P"), f"{f}: {im.mode}" + (f" ({len(im.getpalette()) // 3} colours)" if im.mode == "P" else "")
                 + f", {im.size[0]} x {im.size[1]}, {os.path.getsize(p):,} bytes")
            if f in sizes:
                need(im.size == sizes[f] and (light or "transparency" not in im.info), f"{f}: {sizes[f][0]} x {sizes[f][1]}" + ("" if light else ", opaque"))
    need(total < 3_600_000, f"the new files together: {total:,} bytes (under about 3.6 MB)")
    for f in ("drive-road.png", "drive-desert-l.png", "drive-desert-r.png", "drive-far-l.png", "drive-far-r.png"):
        a = load(folder, f, "RGB")
        sd = float(np.abs(a[:, -1] - a[:, 0]).mean())
        sa = float(np.abs(a[:, 1:] - a[:, :-1]).mean())
        # (PAINT-18B: and the neighbouring columns next to the seam, where a drift of brush may happen to lie)
        sl = float(np.concatenate([np.abs(a[:, 1:7] - a[:, :6]), np.abs(a[:, -6:] - a[:, -7:-1])], 1).mean())
        sa = max(sa, sl)
        need(sd <= sa * 1.6 + 0.004, f"{f}: loops end to end (its last column against its first {sd:.4f}, neighbouring columns anywhere {sa:.4f})")
    road, dl, dr = (load(folder, f"drive-{n}.png", "RGB") for n in ("road", "desert-l", "desert-r"))

    def band(pic, rows_, ppm):
        b = pic[rows_].mean(0)
        n = int(ppm)
        return b[: (b.shape[0] // n) * n].reshape(-1, n, 3).mean(1)
    for name, ra, da in (("left", band(road, slice(0, 4), 48), band(dl, slice(-2, None), 24)),
                         ("right", band(road, slice(-4, None), 48), band(dr, slice(0, 2), 24))):
        n = min(len(ra), len(da))
        diff = float(np.abs(ra[:n] - da[:n]).mean())
        inner = float(np.abs(band(road, slice(4, 8) if name == "left" else slice(-8, -4), 48)[:n] - ra[:n]).mean())
        need(diff <= inner * 2.5 + 0.01, f"the road and the {name} desert meet at 6 m with no seam (a metre along, across the seam {diff:.4f}; "
             f"the road's own rows a few cm apart {inner:.4f})")
    fl, fr = (load(folder, f"drive-far-{n}.png", "RGB") for n in ("l", "r"))          # PAINT-18B: the near and far deserts at 30 m
    for name, na, fa, nin, fin in (("left", band(dl, slice(0, 3), 24), band(fl, slice(-1, None), 8), band(dl, slice(3, 6), 24), band(fl, slice(-2, -1), 8)),
                                   ("right", band(dr, slice(-3, None), 24), band(fr, slice(0, 1), 8), band(dr, slice(-6, -3), 24), band(fr, slice(1, 2), 8))):
        n = min(len(na), len(fa))
        diff = float(np.abs(na[:n] - fa[:n]).mean())
        inner = max(float(np.abs(nin[:n] - na[:n]).mean()), float(np.abs(fin[:n] - fa[:n]).mean()))
        need(diff <= inner * 2.5 + 0.01, f"the {name} desert and its far strip meet at 30 m with no seam (a metre along, across the seam {diff:.4f}; "
             f"each strip's own rows next in {inner:.4f})")
    mid = road[286:290].mean(0)
    yel = (mid[:, 0] - mid[:, 2] > 0.25).astype(F32)
    yel = np.convolve(np.concatenate([yel[-20:], yel, yel[:20]]), np.ones(21), "same")[20:-20] > 0      # (flakes closed)
    starts = [i for i in range(len(yel)) if yel[i] and not yel[i - 1]]
    period = [((b - a) % 3072) / 48 for a, b in zip(starts, starts[1:] + starts[:1])]
    need(len(starts) == 7 and all(abs(p - K.DASH_EVERY) < 0.6 for p in period),
         f"the yellow dashes: {len(starts)} to the loop, from one to the next {', '.join(f'{p:.2f}' for p in period)} m (the painting's 9.14)")
    meta = json.load(open(os.path.join(folder, "drive-things.json")))
    sheet = load(folder, "drive-things.png")
    Hs, Ws = sheet.shape[:2]
    bad = []
    for name, sp in meta["sprites"].items():
        x, y, w, h = sp["box"]
        fx, fy = sp["foot"]
        inbox = -0.5 <= fx <= w + 0.5 and -0.5 <= fy <= h + 0.5
        solid = (sheet[y:y + h, x:x + w, 3] >= 0.5).any()
        if not (0 <= x and 0 <= y and x + w <= Ws and y + h <= Hs and inbox and solid):
            bad.append(name)
    need(not bad, f"the sheet: {len(meta['sprites'])} sprites, every box on the sheet, painted, its foot in it" + (f" (not: {', '.join(bad[:8])})" if bad else ""))
    for name in ("sign", "sign-bc"):
        sp = meta["sprites"][name]
        k = FOCAL / 17.3 / sp["ppm"]
        x0 = VX + FOCAL * 5.96 / 17.3 - sp["foot"][0] * k
        y0 = HZ + FOCAL * EYE / 17.3 - sp["foot"][1] * k
        need(abs(k - 1) < 0.002 and abs(x0 - round(x0)) < 0.01 and abs(y0 - round(y0)) < 0.01 and sp.get("air", 1) == 0,
             f"{name}: at 17.3 m drawn at {k:.7f} of its size, its box's corner at ({x0:.3f}, {y0:.3f}), air {sp.get('air')}: on the painting's own pixels")
    pole = meta["sprites"]["pole"]
    need(abs(pole["height"] - 8.6) < 0.5, f"pole: {pole['height']} m to its top insulator")
    stop = json.load(open(os.path.join(folder, "drive-stop.json")))
    names = set(meta["sprites"])
    missing = [t["sprite"] for t in stop if t["sprite"] not in names]
    rows = sum(1 for t in stop if "row" in t)
    need(isinstance(stop, list) and not missing and len(stop) > 100,
         f"drive-stop.json: {len(stop)} set pieces ({len(stop) - rows} the painting's own and the sign, {rows} marked as a row's), every sprite on the sheet")
    return problems, notes, total


def board_check(scene, stopped):
    """The sign where the painting has it: the drive's stopped picture against back.png over the board (x 599 to 752,
    y 286 to 378)."""
    back = load(scene, "back.png", "RGB")
    a, b = stopped[286:379, 599:753], back[286:379, 599:753]
    same = np.all(np.abs(a - b) < 0.5 / 255, axis=-1)
    return float(same.mean()), float(np.abs(a - b).mean())


def tone(a, b, rows=slice(331, 600)):
    """How far apart two pictures are in tone below the horizon (each blurred 6 px: the light and colour, not the brush):
    -> mean levels off."""
    def soft(p):
        im = Image.fromarray((np.clip(p, 0, 1) * 255 + 0.5).astype(np.uint8))
        from PIL import ImageFilter
        return np.asarray(im.filter(ImageFilter.GaussianBlur(6)), F32)
    return float(np.abs(soft(a) - soft(b))[rows].mean())


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "out/highway"
    scene = sys.argv[2] if len(sys.argv) > 2 else folder
    out = "out/highway-drive-check" + ("" if folder.startswith("out") else "-installed")
    os.makedirs(out, exist_ok=True)
    problems, notes, total = checks(folder)
    for n in notes + problems:
        print(n)
    sky = load(folder, "sky.png", "RGB")
    sp = load(scene, "sun.png")
    names = ["road", "desert-l", "desert-r"] + [n for n in ("far-l", "far-r") if os.path.exists(os.path.join(folder, f"drive-{n}.png"))]
    ctx = {"strips": [Strip(folder, n) for n in names], "sheet": Sheet(folder),
           "pieces": json.load(open(os.path.join(folder, "drive-stop.json"))), "lights": Lights(folder), "scene": scene,
           "sky_sun": sky * (1 - sp[..., 3:4]) + sp[..., :3] * sp[..., 3:4]}
    back = load(scene, "back.png", "RGB")
    back_sun = back * (1 - sp[..., 3:4]) + sp[..., :3] * sp[..., 3:4]
    # the stop, with both hazes, and the hazes' numbers fitted against the painting
    st = Moment(ctx, STOP_AT, stop=STOP_AT, moving=False)
    print("the stopped picture against the painting (back.png with sun.png):")
    pics = {}
    for cfg in (COLOR, BACKDROP):
        p = st.picture(cfg, wagon_row=None)
        pics[cfg["mode"]] = p
        share, mean = board_check(scene, p)
        print(f"  {cfg['mode']:8s} (haze_far {cfg['haze_far']:.0f}): {tone(p, back_sun):.2f} levels off in tone below the horizon (both blurred 6 px); the board "
              f"{100 * share:.1f}% back.png's own pixels (the rest {255 * mean:.2f} levels off on average); above the horizon "
              f"{255 * float(np.abs(p - back_sun)[:330].mean()):.2f} levels off")
    save(pics["color"], f"{out}/stop.png")
    save(pics["backdrop"], f"{out}/stop-backdrop.png")
    rows_ = []
    for m in ("color", "backdrop"):
        rows_.append(np.concatenate([pics[m], back_sun, np.clip(0.5 + (pics[m] - back_sun) * 4, 0, 1)], 1))
    save(np.concatenate(rows_, 0), f"{out}/stop-vs-back.png")
    save(st.picture(COLOR, light=False, wagon_row=None), f"{out}/stop-dark.png")
    # cruising, a quarter of a second apart, and with the backdrop's haze
    for tag, s in (("cruise-a", 300.0), ("cruise-b", 300.0 + SPEED * 0.25)):
        m = Moment(ctx, s)
        save(m.picture(COLOR), f"{out}/{tag}.png")
        if tag == "cruise-a":
            save(m.picture(BACKDROP), f"{out}/cruise-backdrop.png")
    # the approach
    small = []
    for d in (60.0, 30.0, 10.0, 0.0):
        m = Moment(ctx, STOP_AT - d, stop=STOP_AT, moving=d > 0)
        small.append(np.asarray(Image.fromarray((m.picture(COLOR) * 255).astype(np.uint8)).resize((400, 300), Image.BOX), F32) / 255)
    save(np.concatenate([np.concatenate(small[:2], 1), np.concatenate(small[2:], 1)], 0), f"{out}/approach.png")
    # the title (no sign: the rows only)
    for tag, s in (("title-a", 4000.0), ("title-b", 4000.0 + SPEED * 0.25)):
        save(Moment(ctx, s).picture(COLOR), f"{out}/{tag}.png")
    # the motion: the road under the wagon every 0.1 s
    film = [Moment(ctx, 300.0 + SPEED * 0.1 * i).picture(COLOR)[380:600, 200:600] for i in range(6)]
    save(np.concatenate([np.concatenate(film[:3], 1), np.concatenate(film[3:], 1)], 0), f"{out}/film.png")
    print(f"pictures in {out}/")
    print("checks: " + ("all good" if not problems else f"{len(problems)} WRONG"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

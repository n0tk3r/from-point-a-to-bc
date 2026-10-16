"""Checks on the world outside the limousine (nevada_limo_drive.py, DRIVE-16P), and the pictures seen through the
limousine's four panes with the contract's own formulas, before the engine is there.

    python3 nevada_limo_drive_check.py [pictures folder] [scene folder]
        pictures folder: out/nevada-limo (the paintings, default) or ../../art/scenes/nevada-limo (as installed, keyed)
        scene folder:    where back.png, front.png, the cut-outs and layout.json are (default: the pictures folder)

THE CONTRACT (S/briefs/DRIVE-16.md, "The camera, and the road"): a point X m out, z m ahead, Y m up is on the stage at
x = 424 -/+ 345 X / z, y = 220 + 345 (1.83 - Y) / z; the car going forward s m makes every z s smaller. Through each pane
(layout.json `windows`, a pixel is in a pane when its middle is): the sky as it is; below the horizon the ground, read at
((z + s) * 16) mod 1024 along and (X - 6) * 16 out, beyond its last row its last row, fading into the haze; each band
far to near, each column at z = 345 * distance / |x - 424|, its column ((z + s) * ppm) mod width, drawn up from its foot
y = 220 + 345 * 1.83 / z at 345 / z / ppm of its size; then the things, far to near, at their places and sizes, and the
wires from pole to pole. Smaller than its size a picture is read from averaged copies of itself; larger, its pixels are
hard (as the engine does: no shimmer). (DRIVE-16F: the things' shadows are not drawn here: the engine lays them on the
ground, from the drive's `sun`; the sheet has none.)

It writes, into out/nevada-limo-drive-check/: frame-A.png and frame-B.png (the whole stage at two moments a quarter of
a second apart at 16 m/s), frame-C.png (2.3 s later), windows-A.png, windows-B.png, windows-C.png (the four panes, twice
the size), and windows-AB.png (A over B). The numbers it checks: every file the contract names, its size, 8 bits; the
bands' bottom rows painted and their tops clear; the loops' seams; the sheet's boxes, feet and heights."""

import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

F32 = np.float32
HZ, VX, F, EYE = 220.0, 424.0, 345.0, 1.83

# The numbers this check draws with (and the ones ready.md suggests to the merge: the merge chooses).
SPEC = {
    "L": {"bands": [("drive-far-l.png", 6000.0, 0.07), ("drive-mid-l.png", 850.0, 0.5)],
          "ground": ("drive-ground-l.png", 6.0, 16.0),
          "rows": [{"sprite": "reflector-l", "every": [38, 70], "at": [9.9, 10.3]},
                   {"sprite": "marker-l", "every": [380, 420], "at": 10.4},
                   {"sprite": ["sign-back-l", "sign-back-2-l"], "every": [160, 420], "at": [10.5, 11.5]},
                   {"sprite": ["sage-1-l", "sage-2-l", "sage-3-l", "sage-1-l", "rabbitbrush-l", "creosote-l"], "every": [3, 16], "at": [10.8, 24]},
                   {"sprite": ["sage-1-l", "sage-2-l", "sage-3-l", "creosote-l"], "every": [3, 14], "at": [24, 70]},
                   {"sprite": ["joshua-l", "joshua-2-l"], "every": [50, 170], "at": [16, 90]},
                   {"sprite": "rock-l", "every": [60, 180], "at": [11, 45]}]},
    "R": {"bands": [("drive-far-r.png", 3000.0, 0.14), ("drive-mid-r.png", 850.0, 0.5)],
          "ground": ("drive-ground-r.png", 6.0, 16.0),
          "rows": [{"sprite": "pole-r", "every": 55, "at": 14.0, "wires": [8.6, 8.1]},
                   {"sprite": ["post-r", "post-r", "tpost-r"], "every": 4.6, "at": 9.5, "wires": [1.25, 0.95, 0.65]},
                   {"sprite": ["sign-range-r", "sign-services-r"], "every": [180, 420], "at": [6.0, 7.0]},
                   {"sprite": ["sage-1-r", "sage-2-r", "sage-3-r", "sage-2-r", "rabbitbrush-r", "creosote-r"], "every": [3, 16], "at": [10.4, 24]},
                   {"sprite": ["sage-1-r", "sage-2-r", "sage-3-r", "creosote-r"], "every": [3, 14], "at": [24, 70]},
                   {"sprite": ["joshua-r", "joshua-2-r"], "every": [50, 170], "at": [17, 90]},
                   {"sprite": "rock-r", "every": [60, 180], "at": [11, 45]}]},
}
HAZE, HAZE_FAR = "#d9dde6", 4000.0          # the brief's own numbers (the merge tunes them)
SPEED = 16.0


def load(folder, name, mode="RGBA"):
    return np.asarray(Image.open(os.path.join(folder, name)).convert(mode), F32) / 255.0


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], F32)


# ---------------------------------------------------------------- averaged copies (premultiplied), wrapping across
def mips(rgba, wrap=True, levels=10):
    """A picture and its halvings, each pixel the average of four (colour weighted by alpha)."""
    pm = rgba.copy()
    pm[..., :3] *= pm[..., 3:4]
    out = [pm]
    for _ in range(levels):
        p = out[-1]
        h, w = p.shape[:2]
        if h < 2 and w < 2:
            break
        if h % 2:
            p = np.concatenate([p, p[-1:]], axis=0)
        if w % 2:
            p = np.concatenate([p, p[:, :1] if wrap else p[:, -1:]], axis=1)
        out.append((p[0::2, 0::2] + p[1::2, 0::2] + p[0::2, 1::2] + p[1::2, 1::2]) / 4)
    return out


def read(mp, u, v, fp, wrap_u=True, clamp_v=True):
    """Read premultiplied mips at (u, v) (level-0 pixels) with a footprint of fp level-0 pixels a screen pixel."""
    lev = np.clip(np.floor(np.log2(np.maximum(fp, 1.0))).astype(np.intp), 0, len(mp) - 1)
    out = np.zeros(u.shape + (4,), F32)
    for L in np.unique(lev):
        sel = lev == L
        p = mp[L]
        h, w = p.shape[:2]
        uu = np.floor(u[sel] / 2 ** L).astype(np.intp)
        vv = np.floor(v[sel] / 2 ** L).astype(np.intp)
        uu = uu % w if wrap_u else np.clip(uu, 0, w - 1)
        vv = np.clip(vv, 0, h - 1)
        ok = (vv >= 0) & (vv < h) if not clamp_v else np.ones_like(vv, bool)
        o = p[vv, uu]
        o[~ok] = 0
        out[sel] = o
    return out


# ---------------------------------------------------------------- the panes
def pane_masks(windows, shape=(600, 800)):
    """Each pane's pixels: a pixel is in it when its middle is (as the engine decides)."""
    out = []
    for w in windows:
        poly = np.asarray(w["poly"], F32)
        y, x = np.mgrid[0:shape[0], 0:shape[1]].astype(F32)
        px, py = x + 0.5, y + 0.5
        inside = np.zeros(shape, bool)
        n = len(poly)
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % n]
            cond = ((y1 > py) != (y2 > py)) & (px < (x2 - x1) * (py - y1) / (y2 - y1 + 1e-12) + x1)
            inside ^= cond
        out.append((w["side"], inside))
    return out


# ---------------------------------------------------------------- the things along the road, from a seed
def place(rows, seed, length=4000.0):
    rng = np.random.default_rng(seed)
    things = []
    for i, r in enumerate(rows):
        ev, at, spr = r["every"], r["at"], r["sprite"]
        pick = lambda v: float(v) if np.isscalar(v) else float(rng.uniform(v[0], v[1]))
        p = rng.uniform(0, ev if np.isscalar(ev) else ev[1])
        while p < length:
            name = spr if isinstance(spr, str) else spr[int(rng.integers(len(spr)))]
            things.append({"row": i, "p": p, "X": pick(at), "sprite": name, "wires": r.get("wires")})
            p += pick(ev)
    return things, length


def sprite_pic(sheet, meta, name, k, cache):
    """A thing's picture at k times its size: averaged smaller, hard larger. -> (rgba, foot x, foot y) in its pixels."""
    key = (name, round(k, 3))
    if key in cache:
        return cache[key]
    s = meta["sprites"][name]
    x, y, w, h = s["box"]
    pic = sheet[y:y + h, x:x + w]
    W_, H_ = max(1, int(round(w * k))), max(1, int(round(h * k)))
    pm = pic.copy()
    pm[..., :3] *= pm[..., 3:4]
    how = Image.BOX if k < 1 else Image.NEAREST                             # (each premultiplied channel as floats: no
    out = np.dstack([np.asarray(Image.fromarray(np.ascontiguousarray(pm[..., i]), "F").resize((W_, H_), how), F32) for i in range(4)])   # double premultiplying)
    cache[key] = (out, s["foot"][0] * W_ / w, s["foot"][1] * H_ / h)
    return cache[key]


def over_pm(dst, src_pm, x0, y0):
    """Lay a premultiplied picture over dst (straight rgb) at integer (x0, y0)."""
    h, w = src_pm.shape[:2]
    H_, W_ = dst.shape[:2]
    xa, ya, xb, yb = max(0, x0), max(0, y0), min(W_, x0 + w), min(H_, y0 + h)
    if xa >= xb or ya >= yb:
        return
    s = src_pm[ya - y0:yb - y0, xa - x0:xb - x0]
    a = s[..., 3:4]
    dst[ya:yb, xa:xb] = dst[ya:yb, xa:xb] * (1 - a) + s[..., :3]


# ---------------------------------------------------------------- one frame of one side
def side_frame(folder, side, spec, s, mask, haze, haze_far, cache):
    sign = -1.0 if side == "L" else 1.0
    ys, xs = np.nonzero(mask)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    H_, W_ = y1 - y0, x1 - x0
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(F32)
    py, px = yy + 0.5, xx + 0.5
    pic = load(folder, "drive-sky.png", "RGB")[y0:y1, x0:x1].copy()
    # the ground, below the horizon
    gname, gfrom, gppm = spec["ground"]
    if gname not in cache:
        cache[gname] = mips(load(folder, gname), wrap=True)
    gm = cache[gname]
    gh, gw = gm[0].shape[:2]
    below = py > HZ + 0.02
    z = F * EYE / np.maximum(py - HZ, 0.02)
    dx = np.abs(px - VX)
    X = dx * z / F
    u = ((z + s) * gppm) % gw
    v = np.clip((X - gfrom) * gppm, 0, gh - 1)
    dzdy = z * z / (F * EYE)
    fp = np.maximum(gppm * dzdy, np.maximum(gppm * z / F, gppm * dx / F * dzdy))
    g = read(gm, u, v, fp)
    gc = g[..., :3] / np.maximum(g[..., 3:4], 1e-6)
    d = np.hypot(X, z)
    hz = (1 - np.power(0.5, d / haze_far))[..., None]
    gc = gc * (1 - hz) + haze[None, None, :] * hz
    pic = np.where(below[..., None], gc, pic)
    # the bands, far to near
    for bname, dist, ppm in spec["bands"]:
        if bname not in cache:
            cache[bname] = mips(load(folder, bname), wrap=True)
        bm = cache[bname]
        bh, bw = bm[0].shape[:2]
        zb = F * dist / np.maximum(dx, 0.5)
        k = F / (zb * ppm)
        foot = HZ + F * EYE / zb
        r = bh - (foot - py) / k
        ub = ((zb + s) * ppm) % bw
        fpb = np.maximum(ppm * F * dist / np.maximum(dx, 0.5) ** 2, 1.0 / k)
        inb = (r >= 0) & (r < bh)
        smp = read(bm, ub, np.clip(r, 0, bh - 1), fpb)
        a = (smp[..., 3:4] * inb[..., None])
        pic = pic * (1 - a) + smp[..., :3] * inb[..., None]
    # the things, far to near, and the wires
    sheet_path = os.path.join(folder, "drive-things.png")
    if "sheet" not in cache:
        cache["sheet"] = load(folder, "drive-things.png")
        cache["meta"] = json.load(open(os.path.join(folder, "drive-things.json")))
    sheet, meta = cache["sheet"], cache["meta"]
    things, length = cache.setdefault(("things", side), place(spec["rows"], 7 if side == "R" else 8))
    vis = []
    for t in things:
        zt = (t["p"] - s) % length
        if 1.5 < zt < 600:
            vis.append((zt, t))
    vis.sort(key=lambda q: -q[0])
    stage = np.zeros((600, 800, 3), F32)
    stage[y0:y1, x0:x1] = pic
    ppm_t = meta["ppm"]
    for zt, t in vis:
        k = F / zt / ppm_t
        spr = meta["sprites"][t["sprite"]]
        if spr["box"][3] * k < 1.0:
            continue
        img, fx, fy = sprite_pic(sheet, meta, t["sprite"], k, cache.setdefault("spr", {}))
        sx = VX + sign * F * t["X"] / zt
        sy = HZ + F * EYE / zt
        over_pm(stage, img, int(round(sx - fx)), int(round(sy - fy)))
    # wires between each pole and the next of its row, a little sag
    im = Image.new("RGBA", (800, 600), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    by_row = {}
    for t in sorted(things, key=lambda q: q["p"]):
        if t["wires"]:
            by_row.setdefault(t["row"], []).append(t)
    for row, ts in by_row.items():
        for a, b in zip(ts[:-1], ts[1:]):
            za, zb_ = (a["p"] - s) % length, (b["p"] - s) % length
            if not (1.5 < za < 600 and 1.5 < zb_ < 600) or zb_ < za:
                continue
            for hgt in a["wires"]:
                pts = []
                for f in np.linspace(0, 1, 9):
                    zz = za + (zb_ - za) * f
                    XX = a["X"] + (b["X"] - a["X"]) * f
                    sag = 4 * f * (1 - f) * (0.25 if hgt < 3 else 0.6)
                    pts.append((VX + sign * F * XX / zz, HZ + F * (EYE - hgt + sag) / zz))
                dr.line(pts, fill=(52, 46, 60, 230), width=1)
    w_ = np.asarray(im, F32) / 255
    stage = stage * (1 - w_[..., 3:4]) + w_[..., :3] * w_[..., 3:4]
    return stage[y0:y1, x0:x1], (y0, y1, x0, x1)


def frame(folder, scene, s, haze, haze_far, cache):
    lay = json.load(open(os.path.join(scene, "layout.json")))
    if "panes" not in cache:
        cache["panes"] = pane_masks(lay["windows"])
    stage = load(scene, "back.png", "RGB").copy()
    for side, mask in cache["panes"]:
        pic, (y0, y1, x0, x1) = side_frame(folder, side, SPEC[side], s, mask, haze, haze_far, cache)
        m = mask[y0:y1, x0:x1][..., None]
        stage[y0:y1, x0:x1] = np.where(m, pic, stage[y0:y1, x0:x1])
    # the scene's cut-outs as they are at the start (nobody drawn): the divider's glass in its slot, the bow, the bag,
    # the juice box, the clipboard, our seat in front
    def lay_cut(name, clip=None):
        p = os.path.join(scene, name)
        if not os.path.exists(p):
            return
        c = load(scene, name)
        a = (c[..., 3:4] >= 0.5).astype(F32)
        if clip:
            m = np.zeros_like(a)
            x, y, w, h = clip
            m[y:y + h, x:x + w] = 1
            a = a * m
        stage[...] = stage * (1 - a) + c[..., :3] * a
    lay_cut("divider-up.png", (327, 208, 189, 57))
    for n in ("ropes-4.png", "bag.png", "juice.png", "clipboard.png", "front.png"):
        lay_cut(n)
    return stage


# ---------------------------------------------------------------- the numbers
def checks(folder):
    problems, notes = [], []

    def need(cond, msg):
        (notes if cond else problems).append(("ok   " if cond else "WRONG ") + msg)

    files = ["drive-sky.png", "drive-far-l.png", "drive-far-r.png", "drive-mid-l.png", "drive-mid-r.png", "drive-ground-l.png", "drive-ground-r.png", "drive-things.png"]
    for f in files:
        p = os.path.join(folder, f)
        if not os.path.exists(p):
            need(False, f"{f} is there")
            continue
        im = Image.open(p)
        need(im.mode == "P", f"{f}: 8 bits (mode {im.mode}, {len(im.getpalette()) // 3} palette entries), {im.size[0]} x {im.size[1]}, {os.path.getsize(p):,} bytes")
    sky = Image.open(os.path.join(folder, "drive-sky.png"))
    need(sky.size == (800, 600) and "transparency" not in sky.info, "sky: the stage's size, opaque")
    for f, (wexp, hexp) in (("drive-far-l.png", (2400, 48)), ("drive-far-r.png", (2400, 48)), ("drive-mid-l.png", (2400, 40)), ("drive-mid-r.png", (2400, 40))):
        a = load(folder, f)
        need(a.shape[1] == wexp and a.shape[0] == hexp, f"{f}: {a.shape[1]} x {a.shape[0]}")
        need(bool((a[-1, :, 3] >= 0.5).all()), f"{f}: its bottom row is painted all along (the ground at its foot)")
        need(bool((a[:2, :, 3] < 0.5).all()), f"{f}: its top two rows are clear (clear above the land)")
        need(set(np.unique(a[..., 3]).tolist()) <= {0.0, 1.0}, f"{f}: hard edges (alpha 0 or 1 only)")
        rgb = a[..., :3] * a[..., 3:4]
        sd, sa = float(np.abs(rgb[:, -1] - rgb[:, 0]).mean()), float(np.abs(rgb[:, 1:] - rgb[:, :-1]).mean())
        need(sd <= sa * 1.6 + 0.004, f"{f}: loops end to end (seam {sd:.4f}, neighbouring columns anywhere {sa:.4f})")
    for f in ("drive-ground-l.png", "drive-ground-r.png"):
        a = load(folder, f)
        need(a.shape[:2] == (512, 1024) and bool((a[..., 3] == 1).all()), f"{f}: 1024 x 512, opaque")
        sd, sa = float(np.abs(a[:, -1, :3] - a[:, 0, :3]).mean()), float(np.abs(a[:, 1:, :3] - a[:, :-1, :3]).mean())
        need(sd <= sa * 1.6 + 0.004, f"{f}: loops end to end (seam {sd:.4f}, neighbouring columns anywhere {sa:.4f})")
        last = a[-24:, :, :3]
        blk = last.reshape(3, 8, 128, 8, 3).mean(axis=(1, 3))              # what the engine's averaged copies see there
        spread = float(blk.std(axis=1).mean())
        need(spread < 0.02, f"{f}: its last rows calm along the road (8 x 8 averages spread {spread:.4f}), for the engine carries them on")
    meta = json.load(open(os.path.join(folder, "drive-things.json")))
    sheet = load(folder, "drive-things.png")
    need(meta.get("ppm") == 24, "things: ppm 24")
    H_, W_ = sheet.shape[:2]
    for name, sp in sorted(meta["sprites"].items()):
        x, y, w, h = sp["box"]
        ok = 0 <= x and 0 <= y and x + w <= W_ and y + h <= H_ and w % 2 == 1 and sp["foot"] == [w / 2, h]
        bottom = sheet[y + h - 1, x:x + w, 3] >= 0.5
        top = sheet[y, x:x + w, 3] >= 0.5
        # DRIVE-16F: no shadow on the sheet (the engine lays it on the ground), so a thing on two posts (a sign) has bare
        # ground at the middle of its bottom row: it stands on that row somewhere; and its box is no wider than the thing
        # (painted in its first column or its last: the box is cut round the foot, as wide either side)
        foot_on = bool(bottom.any())
        snug = bool((sheet[y:y + h, x, 3] >= 0.5).any() or (sheet[y:y + h, x + w - 1, 3] >= 0.5).any())
        need(ok and foot_on and snug and bool(top.any()), f"things: {name}: box {sp['box']}, foot {sp['foot']}, standing on its bottom row, no wider than itself, {sp['height']} m")
    heights = {n: sp["height"] for n, sp in meta["sprites"].items()}
    for n, lo, hi in (("pole", 8.4, 9.2), ("post", 1.25, 1.4), ("reflector-l", 1.05, 1.15), ("sage-1", 0.6, 1.0), ("sage-2-l", 0.6, 1.0), ("sage-3-l", 0.6, 1.1), ("joshua", 4.0, 6.0), ("joshua-2-l", 3.6, 4.4)):
        need(lo <= heights.get(n, -1) <= hi, f"things: {n} is {heights.get(n)} m (true: {lo} to {hi})")
    return problems, notes


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "out/nevada-limo"
    scene = sys.argv[2] if len(sys.argv) > 2 else folder
    out = "out/nevada-limo-drive-check" + ("" if folder.startswith("out") else "-installed")
    os.makedirs(out, exist_ok=True)
    problems, notes = checks(folder)
    for n in notes + problems:
        print(n)
    haze = hexrgb(os.environ.get("DRIVE_HAZE", HAZE))
    haze_far = float(os.environ.get("DRIVE_HAZE_FAR", HAZE_FAR))
    cache = {}
    s0 = 120.0
    moments = {"A": s0, "B": s0 + SPEED * 0.25, "C": s0 + 37.0}
    shots = {}
    for tag, s in moments.items():
        st = frame(folder, scene, s, haze, haze_far, cache)
        shots[tag] = st
        Image.fromarray((np.clip(st, 0, 1) * 255 + 0.5).astype(np.uint8)).save(f"{out}/frame-{tag}.png")
        win = np.concatenate([st[168:332, 0:312], st[168:332, 536:800]], axis=1)
        Image.fromarray((np.clip(win, 0, 1) * 255 + 0.5).astype(np.uint8)).resize((win.shape[1] * 2, win.shape[0] * 2), Image.NEAREST).save(f"{out}/windows-{tag}.png")
    ab = np.concatenate([np.concatenate([shots[t][168:332, 0:312], shots[t][168:332, 536:800]], axis=1) for t in ("A", "B")], axis=0)
    Image.fromarray((np.clip(ab, 0, 1) * 255 + 0.5).astype(np.uint8)).resize((ab.shape[1] * 2, ab.shape[0] * 2), Image.NEAREST).save(f"{out}/windows-AB.png")
    print(f"pictures in {out}/: frame-A/B/C.png, windows-A/B/C.png, windows-AB.png (haze {os.environ.get('DRIVE_HAZE', HAZE)} at {haze_far:.0f} m)")
    print("checks: " + ("all good" if not problems else f"{len(problems)} WRONG"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

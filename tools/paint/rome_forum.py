"""Rome, the Ides of March, 44 B.C.: the Forum, seen from the Sacred Way at its east end, looking west up its length
to the temple of Saturn (where the act began), with the Capitol above everything. Act Two, rome-forum.

PLAN
  Light     The sun low in the east-south-east, behind our left shoulder (rome_forum_model.SUN: 27 degrees up). Every
            face toward us is lit and warm; the fronts down the left side of the square face north and are in cool
            shade; the fronts down the right take the sun at a slant; long shadows run away from us and to the right:
            the temple of Castor's columns stripe the square. The Capitol is in full sun.
  Depth     horizon 235, full 590 (persp.Camera, so the game's people fit): the lens is 3.9 m up, on the rise of the
            Sacred Way. The square is told shorter than it is (some 60 m from us to the temple of Saturn's steps) so that
            the boy arriving at their foot is still 15 pixels tall; the Capitol is far beyond, at its true distance, and
            rises over everything.
  Tones     LIGHT  the far end and the Capitol in the sun, the sunlit paving, Castor's steps.
            DARK   the mouth of the Tuscan street in Castor's shadow; the shaded front of Caesar's basilica; the porches.
            MIDDLE the sky, the hill, the colonnade of Paullus, the hoarding.
            The eye goes up the bright square to the small bright temple of Saturn and up again to the gold roof.
  Places    left: the corner of the temple of Castor (x 0 to 156), its steps' foot at row 473 to 500; Juturna's basin before
            them (x 0 to 150, rows 474 to 507); Phyllis's place at (181, 481). The Tuscan street's mouth between Castor's
            corner and Caesar's basilica (x 156 to 226). The basilica down the left to the far end (x 226 to 278).
            far end: the temple of Saturn (x 291 to 448, its steps' foot at row 279 to 281), the speakers' platform before
            it and to its right (x 375 to 545), an older temple behind (x 427 to 510).
            right: the colonnade of Paullus (x 540 to 725); before it, the site of the new senate house: the hoarding
            (its foot from (543, 342) to the right edge at row 465), the crane over it.
            the square: the Puteal (377, 386), the moneychanger's table (450, 396), statues on three columns.

The picture is a backdrop and its cut-outs: Castor's corner (people go behind it into the Tuscan street), Juturna's
basin, the Puteal, the table and its awning (which stirs), the hoarding (the Gaul changes behind it), three statues on
their columns, and a statue base near us at the bottom right. Nothing that moves by nature is painted: layout.json "fx".

  python3 rome_forum.py         paints everything into out/rome-forum/ (and out/rome-forum-comp.png)
  python3 rome_forum.py fast    skips the brush passes and the palettes: out/rome-forum-work/ only
  (rome_forum_model.py holds the measurements; rome_forum_kit.py the tools; rome_forum_far.py the far half;
   rome_forum_things.py the near things; rome_forum_check.py checks the layout against the engine's walk map.)"""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import strokes, grain, palette_of, to_palette, save
import sky
import land
from rome_forum_kit import *
import rome_forum_far as far_
import rome_forum_things as things

OUT = "out/rome-forum"
WORK = "out/rome-forum-work"
KEEP = "out/rome-forum-kept"


def show(picture, name):
    Image.fromarray((np.clip(picture, 0, 1) * 255).astype(np.uint8)).save(name)


def kept(name, make, *sources):
    """Paint a layer, or fetch it from the last run if nothing that paints it has changed (as rome_steps.py does)."""
    from rome_steps_kit import source_key
    os.makedirs(KEEP, exist_ok=True)
    key = source_key("rome_forum_model.py", "rome_forum_kit.py", *sources)
    path = f"{KEEP}/{name}-{key}.npz"
    if os.path.exists(path):
        z = np.load(path)
        return [z[k_] for k_ in sorted(z.files)]
    out = make()
    for f in os.listdir(KEEP):
        if f.startswith(name + "-"):
            os.remove(f"{KEEP}/{f}")
    np.savez_compressed(path, **{f"a{i}": o for i, o in enumerate(out)})
    return out


def canvas_of(arrays):
    c = Canvas(SHAPE)
    c.c, c.a = arrays[0].astype(F32), arrays[1].astype(F32)
    return c


def _pair(make):
    c = make()
    return [c.c, c.a]


# ---------------------------------------------------------------- the sky
def sky_layer(seed=11):
    def make():
        pic = sky.field(SHAPE, HZ, [(0.0, "#2766bc"), (0.32, "#3f88d4"), (0.60, "#78b6e6"), (0.84, "#c2dde6"), (1.0, "#f2e6c8")], seed, haze="#f8ecd0", patch=0.03)
        sky.wisps(pic, HZ, seed + 3, "#fdf2dc", top=0.45, amount=0.45)
        sky.paint_clouds(pic, [(612, 92, 300, 74, 22), (455, 112, 140, 34, 9), (765, 130, 120, 40, 8)], seed + 22,
                         tones=("#86a4d8", "#bccfe8", "#fbf3df", "#fffdf2"), light=SKY_LIGHT, ragged=11)
        return [pic]
    return kept("sky", make, repr(seed), "sky")[0].copy()


# ---------------------------------------------------------------- the paving, and the light and shadows on it
def paving(seed=17):
    """The square's paving in its own colours: big pale slabs of travertine in courses running across, some greyer,
    some yellower, a few dark old ones; worn pale along the way people walk up the middle. -> (picture, joints, u, v, ppc)"""
    u, v, ppc = WORLD.on_floor(0.0)
    tone, jm, above = courses(u, v, long=132.0, high=88.0, seed=seed, joint=1.8, ppc=ppc, vary_len=0.36)
    c = col(PAVE)[None, None, :] * (1 + (tone[..., None] - 0.5) * 0.12)
    warm = (hash2(np.floor(tone * 811), 5, seed) - 0.5) * 0.07
    c = c + np.stack([warm, warm * 0.15, -warm * 1.2], axis=-1)
    old = (hash2(np.floor(tone * 577), 9, seed) > 0.90)
    c = c * np.where(old[..., None], np.array([0.90, 0.88, 0.90], dtype=F32), 1.0)
    c = c * (1 + (tex(u, v, 420, seed + 1)[..., None] - 0.5) * 0.18 + (tex(u, v, 60, seed + 2)[..., None] - 0.5) * 0.09)
    trod = np.exp(-((u - 0.4 * (v - 1000) * 0.0) / 600.0) ** 2) * np.clip((v - 900) / 900.0, 0, 1) * np.clip((7000 - v) / 2000.0, 0, 1)
    c = c * (1 + 0.05 * trod[..., None])
    return np.clip(c, 0, 1).astype(F32), jm, u, v, ppc


def ground_shadow():
    """How much of the sun each place on the paving has lost: to the temple of Castor, the basilica, the statues, the
    table, the hoarding, and the rest (rome_forum_things.solids_*)."""
    def make():
        u, v, ppc = WORLD.on_floor(0.0)
        cut = sunless(things.solids_world(), u, v, 0.0, (WSU, WSV, WSH))
        kf = castor_frame()
        cu, cv_, _ = kf.on_floor(0.0)
        cut = np.maximum(cut, sunless(things.solids_castor(), cu, cv_, 0.0, kf.to_frame(SUN)))
        hf, hs = things.solids_hoard()
        hu, hv, _ = hf.on_floor(0.0)
        cut = np.maximum(cut, sunless(hs, hu, hv, 0.0, hf.to_frame(SUN)))
        sf, ss = things.solids_saturn()
        su_, sv_, _ = sf.on_floor(0.0)
        cut = np.maximum(cut, sunless(ss, su_, sv_, 0.0, sf.to_frame(SUN)))
        return [cut]
    return kept("shadow", make, "rome_forum_things.py", "rome_forum_far.py")[0]


def cloud_shadow(seed=11):
    """A cloud's shadow over the nearest paving, its edge soft and wandering (as on the steps): -> how much to darken."""
    x, y = grid(SHAPE)
    edge_y = 552 + (noise(SHAPE, (260, 60), seed + 15, 3) - 0.5) * 50 + (x - 400) * 0.03
    return (step(0.0, 1.0, (y - edge_y) / 40.0) * 0.32).astype(F32)


def under(seed=11):
    """Everything broad and soft: the sky, the Capitol in its air, the paving with the long shadows lying on it, the
    buildings round the square as masses of light and shade."""
    x, y = grid(SHAPE)
    info = {}
    pic = sky_layer(seed)
    layers = {}
    layers["capitol"] = canvas_of(kept("capitol", lambda: _pair(far_.capitol), "rome_forum_far.py"))
    for nm, fn in (("tuscan", lambda: _one(far_.tuscan)), ("concord", lambda: _one(far_.concord)), ("saturn", lambda: _one(far_.saturn)), ("rostra", lambda: _one(far_.rostra)),
                   ("people", lambda: _one(far_.far_people)), ("paullus", lambda: _one(far_.paullus)), ("julia", lambda: _one(far_.julia)),
                   ("site", lambda: _one(far_.site_inside)), ("works", lambda: _one(far_.site_works))):
        layers[nm] = canvas_of(kept(nm, (lambda f=fn: _pair(f)), "rome_forum_far.py"))
    info["layers"] = layers
    soft = lambda c_, s_=1.2: (blur(c_.c, s_), blur(c_.a, s_ * 0.8))
    cc, ca = soft(layers["capitol"], 1.4)
    over(pic, cc / np.maximum(ca, 1e-3)[..., None], np.clip(ca, 0, 1))
    # the paving
    own, jm, u, v, ppc = paving()
    gmask = np.clip(y - HZ - 0.5, 0, 1)
    near = np.clip((y - HZ) / (H - HZ), 0, 1) ** 1.2
    own = own * (1 - near[..., None] * (1 - np.array([1.0, 0.94, 0.80], dtype=F32)) * 0.8)       # near stone deeper and more golden
    cut = ground_shadow() * gmask
    lit = LIT.on(own, 0.62, cut, up=1, deep=0.08 * cut, bounce=0.25)
    drift = (noise(SHAPE, 150, seed + 12, 3) - 0.5) * 0.10
    lit = np.clip(lit * (1 + (cut[..., None] * np.stack([drift, drift * 0.3, -drift], axis=-1)) + (noise(SHAPE, 60, seed + 13, 3) - 0.5)[..., None] * 0.06 * cut[..., None]), 0, 1)
    over(pic, lit, gmask)
    land.haze(pic, HZ, "#f3ead2", 0.70, 0.09, gmask)
    glow(pic, "#fff0c8", (np.clip(1 - np.abs(y - (HZ + 8)) / 30, 0, 1) * 0.10 * gmask).astype(F32))
    tint(pic, "#b48c80", (cloud_shadow() * gmask).astype(F32))                                  # a cloud's shadow over the nearest paving
    corner = np.clip(((x - 400) / 400) ** 2 * 0.45 + ((y - 430) / 170).clip(0, 2) ** 2 * 0.55, 0, 1)
    tint(pic, "#cba27a", (corner * 0.16 * gmask).astype(F32))                                   # the near corners deeper and warmer
    info.update(u=u, v=v, ppc=ppc, joints=jm, ground=gmask, cut=cut)
    for nm in ("tuscan", "site", "concord", "saturn", "rostra", "people", "paullus", "julia", "works"):
        cc, ca = soft(layers[nm], 1.1)
        over(pic, cc / np.maximum(ca, 1e-3)[..., None], np.clip(ca, 0, 1))
    return np.clip(pic, 0, 1), info


def _one(fn):
    c = Canvas(SHAPE)
    fn(c)
    return c


# ---------------------------------------------------------------- the details, over the brushwork
def details(pic, info, seed=11):
    """Over the brushwork: every built thing said again crisply, then the small things."""
    x, y = grid(SHAPE)
    rng = np.random.default_rng(seed + 5)
    L = info["layers"]
    L["capitol"].onto(pic, 0.85)
    land.haze(pic, HZ, "#f3ead2", 0.10, 0.06, L["capitol"].a)
    # the joints of the paving: thin, broken, fainter far away
    jm = hand(info["joints"]) * info["ground"] * (0.62 + 0.5 * noise(SHAPE, 110, seed + 21, 3))
    tint(pic, "#8a6f5c", np.clip(jm * 0.55, 0, 1).astype(F32))
    lip = np.roll(info["joints"], 1, axis=0) * info["ground"] * (1 - info["cut"]) * (1 - np.clip(info["joints"] * 2, 0, 1))
    glow(pic, "#fff2d0", np.clip(lip * 0.14, 0, 1).astype(F32))
    for nm in ("tuscan", "site", "concord", "saturn", "rostra", "people", "paullus", "julia", "works"):
        handed(L[nm]).onto(pic, 0.9)
    # the crane in the site, its frame and its wheel (the wheel's frames are the engine's: see crane_frames)
    info["before_crane"] = pic.copy()                    # (the crane's wheel turns in frames painted into the picture as it was here)
    fr, wh, _ = far_.crane_parts(0.0)
    crane = Canvas(SHAPE)
    for sh in (wh, fr):
        sc, sa = sh.done()
        crane.put(sc, sa)
    crane.onto(pic)
    info["layers"]["crane"] = crane
    g = Sheet2(SHAPE)
    things.garlands(g)                                   # Phyllis's baskets and her pole of garlands
    gc, ga = g.done()
    over(pic, gc, ga)
    gl = Canvas(SHAPE)
    gl.put(gc, ga)
    info["layers"]["garlands"] = gl
    s = Sheet2(SHAPE)
    # weeds in the joints near the edges of the square, grit, a crack or two
    def tuft(px, py, r, tones=("#55662e", "#7f9440", "#b4bf60")):
        for j in range(int(5 + r)):
            a = math.pi * rng.uniform(0.15, 0.85)
            l_ = r * rng.uniform(0.5, 1.1)
            s.line([(px + rng.normal(0, r * 0.25), py), (px + math.cos(a) * l_ * 0.8, py - math.sin(a) * l_)], tones[int(rng.random() ** 1.4 * 3)], max(0.8, r * 0.14))
    for (gx_, gy_, r_) in ((286, 560, 4.0), (612, 588, 4.5), (520, 470, 3.0), (330, 420, 2.6), (690, 510, 3.4), (250, 520, 3.0)):
        tuft(gx_, gy_, r_)
    for i in range(30):
        gx_, gy_ = rng.uniform(200, 800), HZ + (H - HZ) * rng.uniform(0.45, 1.0)
        r_ = 0.6 + 1.0 * (gy_ - 420) / 180 * rng.random()
        if r_ > 0.5:
            s.ellipse(gx_ + r_ * 1.2, gy_ + 0.3, r_ * 1.6, r_ * 0.5, "#8f7c98", 0.5)
            s.ellipse(gx_, gy_, r_ * 1.2, r_ * 0.8, ["#f4e2bc", "#cbb089", "#a48a70"][int(rng.integers(3))])
    for (cx_, cy_, l_) in ((330, 575, 32), (560, 545, 24), (470, 452, 18), (640, 430, 16)):
        pts_ = [(cx_, cy_)]
        ang = rng.uniform(-0.5, 0.5)
        for j in range(5):
            ang += rng.normal(0, 0.5)
            pts_.append((pts_[-1][0] + math.cos(ang) * l_ / 5, pts_[-1][1] + math.sin(ang) * l_ / 9))
        s.line(pts_, "#8a6c50", 0.9, 0.6)
        s.line([(q[0], q[1] + 1) for q in pts_], "#fff0c8", 0.7, 0.35)
    s.onto(pic)
    return pic


# ---------------------------------------------------------------- the cut-outs
PLANES = ["statue-3", "statue-2", "statue-1", "castor", "puteal", "table", "awning", "hoarding", "hoarding-near", "basin", "front-base"]


def cutouts():
    """Every cut-out, painted: -> {name: Canvas}"""
    out = {}
    out["castor"] = canvas_of(kept("cut-castor", lambda: _pair(things.castor), "rome_forum_things.py"))
    out["basin"] = canvas_of(kept("cut-basin", lambda: _pair(things.basin), "rome_forum_things.py"))
    out["puteal"] = canvas_of(kept("cut-puteal", lambda: _pair(things.puteal), "rome_forum_things.py"))
    out["table"] = canvas_of(kept("cut-table", lambda: _pair(things.table), "rome_forum_things.py"))
    out["awning"] = canvas_of(kept("cut-awning", lambda: _pair(things.awning), "rome_forum_things.py"))
    whole = canvas_of(kept("cut-hoarding", lambda: _pair(things.hoarding), "rome_forum_things.py"))
    left = (PX < things.hoarding_split_x()).astype(F32)            # cut in two at the gateway (rome_forum_things: why)
    for nm, part in (("hoarding", left), ("hoarding-near", 1 - left)):
        out[nm] = Canvas(SHAPE)
        out[nm].c, out[nm].a = whole.c * part[..., None], whole.a * part
    for i in range(3):
        out[f"statue-{i + 1}"] = canvas_of(kept(f"cut-statue-{i + 1}", (lambda i=i: _pair(lambda: things.statue(i))), "rome_forum_things.py"))
    out["front-base"] = canvas_of(kept("cut-front-base", lambda: _pair(things.front_base), "rome_forum_things.py"))
    return out


def brushed(layer, ground, seed, sizes=(6, 3, 2), keep=0.40, restate=0.6):
    """A cut-out, repainted with a small brush on the ground it stands against, then said again crisply (as the steps').
    -> (colour, hard coverage)"""
    c, a = layer.straight()
    ys, xs = np.where(a > 0.02)
    if len(xs) == 0:
        return c, a
    x0, x1, y0, y1 = max(0, xs.min() - 12), min(W, xs.max() + 13), max(0, ys.min() - 12), min(H, ys.max() + 13)
    flat = ground[y0:y1, x0:x1].copy()
    over(flat, c[y0:y1, x0:x1], a[y0:y1, x0:x1])
    painted = strokes(flat, sizes=sizes, seed=seed, density=1.8, jitter=0.03, keep=keep)
    painted = lerp(painted, flat, (restate * a[y0:y1, x0:x1])[..., None])
    out = c.copy()
    out[y0:y1, x0:x1] = painted
    return out, (a > 0.5).astype(F32)


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.014, amount=0.02, palette=None):
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette if palette is not None else palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name), pal, idx


if __name__ == "__main__":
    t0 = time.time()
    fast = "fast" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    base, info = under()
    show(base, f"{WORK}/1-under.png")
    print("under", round(time.time() - t0, 1))
    pic = base.copy() if fast else strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.22)
    print("brushed", round(time.time() - t0, 1))
    ground = pic.copy()
    details(pic, info)
    print("details", round(time.time() - t0, 1))
    cut = cutouts()
    whole = pic.copy()
    finished_cuts = {}
    for i, name in enumerate(PLANES):
        layer = cut[name]
        if fast:
            c, a = layer.straight()
            a = (a > 0.5).astype(F32)
        else:
            c, a = brushed(layer, pic, seed=20 + i)
        finished_cuts[name] = (c, a)
        over(whole, c, a)
    show(pic, f"{WORK}/2-back.png")
    show(whole, f"{WORK}/2-all.png")
    print("painted", round(time.time() - t0, 1))
    import rome_forum_layout as lay_
    for nm, fn in (("records", lambda c_: far_.tabularium(c_, np.random.default_rng(31))), ("jupiter", far_.jupiter), ("moneta", far_.moneta)):
        c_ = Canvas(SHAPE)
        fn(c_)
        info["layers"][nm] = c_
    info["layers"]["tuscan_mouth"] = lay_.tuscan_mouth()
    lay = lay_.layout(finished_cuts, info["layers"])
    lay_.check_layout(whole, lay, f"{WORK}/3-layout.png")
    with open(f"{WORK}/layout.json", "w") as fh:
        json.dump(lay, fh, indent=1)
    print("layout", round(time.time() - t0, 1))
    if fast:
        sys.exit()
    # ---- the finish: grain, then each file's own palette with a fine speckle
    size, pal, back_idx = finish(pic, f"{OUT}/back.png", 160)
    print("back", size)
    COLOURS = {"castor": 96, "basin": 48, "puteal": 40, "table": 48, "awning": 32, "hoarding": 48, "hoarding-near": 64, "front-base": 32, "statue-1": 32, "statue-2": 32, "statue-3": 32}
    for name in PLANES:
        c, a = finished_cuts[name]
        print(name, finish(c, f"{OUT}/{name}.png", COLOURS[name], a)[0])
    import rome_forum_frames as frames_
    files, wheel, same = frames_.wheel_frames(info["before_crane"], pal, OUT, back_idx)
    print("crane frames", files, "frame 0 the same as the backdrop:", same)
    lay["planes"].insert(3, wheel)
    lay["frames"] = {"crane": {"files": "crane-<n>.png, n 0 to 5", "size": wheel["size"], "foot": wheel["foot"], "at": wheel["at"],
                               "note": "the crane's great wheel, a sixth of a spoke further round in each; cut from the finished picture"}}
    lay["fx_note"] = ("Nothing that moves by nature is painted: the smoke of the Ides offering before the temple of Jupiter, Juturna's spring (the "
                      "water coming in at the back of its basin, rings, light on the water), the pigeons (the steps' own frames), the swallows over "
                      "the Capitol (the steps' frames), the moneychanger's awning (its own cut-out, a sway), the dust where the crane sets a block "
                      "down (now and then), and the crane's wheel (painted frames, crane-0 to crane-5, as a plane: see `planes`). Left painted, on "
                      "purpose: the clouds, the garlands on Phyllis's pole (wreaths hanging still), the far people (dabs of a few pixels), the "
                      "stone block hanging from the crane (it is lifted slowly; it does not swing), the statues.")
    with open(f"{OUT}/layout.json", "w") as fh:
        json.dump(lay, fh, indent=1)
    os.system(f"{sys.executable} comp.py {OUT} back " + " ".join(PLANES))
    print("done", round(time.time() - t0, 1))

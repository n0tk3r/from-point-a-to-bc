"""PAINT-23 (round twenty-three, RECOMPOSE and the act's watercolour): the foot of Mount Shosha, about 29 April 1830: the
women's hall of Engyo-ji (edo-shosha), late afternoon and then sunset. Round twenty-one's picture (PAINT-21E) was the
flattest of the act; this one is painted again from a new place, through one camera, in three planes, and laid in
washes. edo_shosha_kit.py has the research, the camera, the place measured and the two lights; DEPTH.md the direction.

THE PICTURE. We stand on the terrace south-west of the hall under an old red pine, and look north-north-east along the
foot of the mountain. NEAR (pine.png, near.png: edo_shosha_near.py): the pine's trunk up the left edge, its great bough
across the top with its pads hanging into the hall's peak; its roots, moss and ferns along the bottom left; grass and
ferns on the bank's lip in the bottom right corner. MIDDLE (edo_shosha_things.py): the hall near at the right, three-
quarters on: its west wall in full sun with the lattice, its front at a slant with hundreds of slips round the latticed
doors (doors*.png), the lock on the hasp (lock*.png), the step and the rice ball (stepball*.png); the women's bench
before the west wall (bench*.png), the heap of combs on its cloth; O-Ume's hut farther off at the left, its lantern; the
stone at the path's foot (stone*.png) and the path climbing from Ryokai's bottom step into pines and maples, up behind the
hall's roof and out of sight, the late cherry in their shade; the terrace, the road up from the town, every shadow one way. FAR (edo_shosha_far.py): the woods' skyline against the mountain's shoulder and
its far spur, each paler; beyond the hall's corner the far hills, the Harima plain far below in layers of air with the
castle small and white, the sky.

TWO LIGHTS, the same geometry: back.png and the plain cut-outs (gold); sunset.png (the whole stage at sunset, which the
scene fades in over back.png, under everybody) and every cut-out's -sunset twin. Not painted: people (the game's), the
petals, the crows and the pine's stirring (fx), light (the game's).

    python3 edo_shosha.py           paints both lights into out/edo-shosha/ and layout.json; out/edo-shosha-comp-*.png
    python3 edo_shosha.py fast      no brush pass and no palette: out/edo-shosha-work/ (the composites, to judge)
    python3 edo_shosha.py fast gold the same, one light only
    python3 edo_shosha_plan.py      the skeleton (before any painting);  python3 edo_shosha_play.py  the scene played"""

import json
import os
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, blur, grain, grid, lerp, over, palette_of, save, step, strokes, to_palette
import watercolor as WC
import edo_shosha_kit as K
from edo_shosha_kit import SHAPE, HZ, W, H, Wet, painted
import edo_shosha_far as FAR
import edo_shosha_things as T
import edo_shosha_near as NEAR

OUT = "out/edo-shosha"
WORK = "out/edo-shosha-work"
SEED = 1830                                        # the paper: one sheet under the backdrop and every cut-out (both lights)
X_, Y_ = grid(SHAPE)
CUTS = ["doors", "lock", "stepball", "stone", "bench", "pine", "near"]       # back to front, as the scene lists them
ALTS = ["doors-half", "doors-open", "lock-open"]
_BANK = {}


def bank():
    if not _BANK:
        _BANK["m"], _BANK["d"] = T.bank_mask_fast()
    return _BANK["m"], _BANK["d"]


def layer(fn, *a):
    L = Wet(SHAPE)
    out = fn(L, *a)
    c, al = L.done()
    return c, al, out


def under():
    """Pass one: the washes, back to front. -> (picture, info, the crisp layers to restate after the brush)."""
    info = {}
    pic = FAR.sky()
    vista, edge_line = T.vista_mask()
    info.update(FAR.paint_far(pic, vista))
    info["bank"], info["bank_d"] = bank()
    T.woods(pic, info)
    T.ground(pic, info)
    T.path(pic, info)                                  # (after the ground: its bottom steps stand on the terrace, Ryokai's seat)
    T.terrace_edge(pic, info)
    crisp = {}
    crisp["combs"] = layer(T.combs)
    over(pic, crisp["combs"][0], crisp["combs"][1])
    crisp["hut"] = layer(T.hut)
    T.shadows(pic, info)
    over(pic, crisp["hut"][0], crisp["hut"][1])
    crisp["inside"] = layer(T.interior, K.LIGHT)
    da, db = K.DOOR_A
    dy0, dy1 = K.DOOR_Y
    from brush import mask_poly
    door_m = mask_poly(SHAPE, [K.HP(da, 0, dy0), K.HP(db, 0, dy0), K.HP(db, 0, dy1), K.HP(da, 0, dy1)])
    crisp["inside"] = (crisp["inside"][0], crisp["inside"][1] * door_m, None)
    over(pic, crisp["inside"][0], crisp["inside"][1])
    crisp["hall"] = layer(T.hall)
    over(pic, crisp["hall"][0], crisp["hall"][1])
    info["hall_a"] = crisp["hall"][1]
    info["hut_a"] = crisp["hut"][1]
    return np.clip(pic, 0, 1).astype(F32), info, crisp


def wet_mask(info):
    """What was laid wet in wet (watercolor.wash's `soft`): the sky 1.0; the far hills and the plain 0.6, the far spur
    0.6, the shoulder 0.45; the woods' upper mass a breath (0.15); the castle firmer (it is clicked); the play 0."""
    sky = (1 - np.clip(info["far"] + info["shoulder"], 0, 1)) * (Y_ < HZ + 1)
    m = sky * 1.0
    m = np.maximum(m, info["far"] * (1 - info["shoulder"]) * 0.60)
    m = np.maximum(m, info["shoulder"] * 0.45)
    m = np.maximum(m, info["plain"] * 0.55)
    m = np.maximum(m, info["hills"] * (Y_ < HZ + 1) * 0.6)
    m = m * (1 - info["woods"] * 0.85)
    m = m * (1 - np.clip(blur(info["castle"], 1.5) * 2, 0, 1) * 0.6)
    for k_ in ("hall_a", "hut_a", "edge", "trees", "path"):
        if k_ in info:
            m = m * (1 - np.clip(blur((info[k_] > 0.3).astype(F32), 1.5) * 2, 0, 1))
    return np.clip(m, 0, 1).astype(F32)


def cut_layers():
    return {
        "doors": layer(T.doors, "shut")[:2], "doors-half": layer(T.doors, "half")[:2], "doors-open": layer(T.doors, "open")[:2],
        "lock": layer(T.lock, "shut")[:2], "lock-open": layer(T.lock, "open")[:2],
        "stepball": layer(T.stepball)[:2], "stone": layer(T.stone)[:2], "bench": layer(T.bench)[:2],
        "pine": NEAR.pine_cut(), "near": NEAR.near_cut(),
    }


def paint_light(name, fast):
    """One light, all of it, washed: -> (backdrop, {cut-out: (colour, cover)}, info)."""
    K.set_light(name)
    t0 = time.time()
    base, info, crisp = under()
    print(name, "under", round(time.time() - t0, 1))
    wm = wet_mask(info)
    if fast:
        pic = base.copy()
    else:
        brushed_ = strokes(base, sizes=(12, 6, 3), seed=2, density=1.5, jitter=0.022, keep=0.0)
        keep = np.clip(0.50 + 0.38 * wm, 0, 0.92)
        pic = lerp(brushed_, base, keep[..., None]).astype(F32)
        for k_ in ("combs", "hut", "inside", "hall"):                         # what is built: restated crisp over the brush
            c, a, _ = crisp[k_]
            over(pic, c, a * 0.86)
    print(name, "brushed", round(time.time() - t0, 1))
    cuts = cut_layers()
    out = {}
    for i, (n, (c, a)) in enumerate(cuts.items()):
        a = (a > 0.5).astype(F32)
        if not fast and n not in ("pine", "near", "lock", "stepball"):
            c, _ = painted(c, a, np.median(pic[a > 0.5], axis=0) if a.any() else c[0, 0], seed=60 + i, sizes=(4, 2), keep=0.72, fast=fast)
        if n in ("doors", "doors-half", "doors-open", "stone", "bench"):
            c, a2 = K.hand(c, a, seed=70 + i, amount=0.5)
        out[n] = (c, a)
    # the watercolour: one sheet of paper under all of it (the same seed), the far things wet in wet
    back = WC.wash(pic, seed=SEED, soft=wm, wander=1.5, fleck=0.35)
    washed = {}
    for n, (c, a) in out.items():
        hard = np.clip(blur((a > 0.3).astype(F32), 1.2) * 2.0, 0, 1)
        washed[n] = (WC.wash_cut(c, a, pic, seed=SEED, soft=wm * (1 - hard), wander=1.5, fleck=0.2 if n in ("pine", "near") else 0.35), a)
    info["wet"] = wm
    print(name, "washed", round(time.time() - t0, 1))
    return back, washed, info


def show(picture, path):
    Image.fromarray((np.clip(picture, 0, 1) * 255 + 0.5).astype(np.uint8)).save(path)


def to_file(picture, name, colors=128, alpha=None, seed=7, speckle=0.010, amount=0.010):
    """Pigment grain (little: the wash has its own granulation), then a limited palette with speckle: an 8-bit PNG."""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 1, 3)], colors=min(colors, max(2, len(np.unique((sample_of * 255).astype(np.uint8).reshape(-1, 3), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def composite(back, cuts, which):
    whole = back.copy()
    for n in which:
        c, a = cuts[n]
        over(whole, c, a)
    return whole


if __name__ == "__main__":
    t0 = time.time()
    fast = "fast" in sys.argv
    lights = [l for l in ("gold", "sunset") if l in sys.argv] or ["gold", "sunset"]
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    results = {}
    for name in lights:
        back, cuts, info = paint_light(name, fast)
        results[name] = (back, cuts, info)
        show(composite(back, cuts, CUTS), f"{WORK}/{name}-all.png")
        show(back, f"{WORK}/{name}-back.png")
        show(composite(back, cuts, ["doors-open", "stepball", "stone", "bench", "pine", "near"]), f"{WORK}/{name}-open.png")
    if fast:
        print("done (fast)", round(time.time() - t0, 1))
        sys.exit()
    for name in lights:
        back, cuts, info = results[name]
        suffix = "" if name == "gold" else "-sunset"
        print("back" if name == "gold" else "sunset", to_file(back, f"{OUT}/{'back' if name == 'gold' else 'sunset'}.png", 250))
        for n, (c, a) in cuts.items():
            colors = {"pine": 96, "near": 64, "doors": 96, "doors-half": 96, "doors-open": 96, "lock": 32, "lock-open": 32, "stepball": 24, "stone": 48, "bench": 48}[n]
            print(n + suffix, to_file(c, f"{OUT}/{n}{suffix}.png", colors, a))
    if "gold" in results:
        import edo_shosha_layout as LY
        LY.write(f"{OUT}/layout.json", results["gold"][1], results["gold"][2])
    for name in lights:
        comp = Image.open(f"{OUT}/{'back' if name == 'gold' else 'sunset'}.png").convert("RGBA")
        for n in (CUTS if name == "gold" else ["doors", "lock", "stepball", "stone", "bench", "pine", "near"]):
            comp.alpha_composite(Image.open(f"{OUT}/{n}{'' if name == 'gold' else '-sunset'}.png").convert("RGBA"))
        comp.convert("RGB").save(f"out/edo-shosha-comp-{name}.png")
    print("done", round(time.time() - t0, 1))

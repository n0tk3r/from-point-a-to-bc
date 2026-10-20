"""The highway at dusk, to be driven down (ROAD-18P): the pictures the engine's `drive` draws the opening movie and the
title from, seen straight ahead down the road from behind the wagon (S/briefs/ROAD-18.md, the contract).

    python3 highway_drive.py           every picture, the full passes (about three minutes)
    python3 highway_drive.py sky ground things light    some of them (light: from the strips as written)
    python3 highway_drive.py fast      a quick look: no brush pass on the grounds (the painting's own pass is kept)
    python3 highway_drive_check.py     the checks, and the chase view drawn with the contract's formulas: cruising, the
                                       camera stopped (beside back.png), the title's loop

writes, into out/highway/ beside the scene's other paintings (install.py keys them as the scene's frames):

    sky.png               800 x 600: back.png with nothing standing in it: the sky, the glow round the sun's place,
                          the mesas; below the horizon the far plain, glowing (highway_drive_sky.py)
    light-shade.png, light-glow.png
                          800 x 600 RGBA: the painting's light, which stays on the stage while the ground goes by (the
                          engine's `light`: multiply, then screen): the dust and the sun's glow, the shine down the road,
                          the deeper corners, and the painting's colours by distance where the haze misses them. Beyond
                          the contract's table (the engine's own idea; its stand-ins have these two names). Made last,
                          from the strips as written (highway_drive_sky.lights)
    drive-road.png        3072 x 576: the road and its shoulders from straight above, 48 px a metre, 6 m left (top row)
                          to 6 m right, 64 m along, looping (highway_drive_ground.py)
    drive-desert-l.png    1536 x 576: the desert from 30 m left (top row) to 6 m left, 24 px a metre, 64 m, looping
    drive-desert-r.png    1536 x 576: from 6 m right (top row) to 30 m right
    drive-things.png      the sheet of upright things (highway_drive_things.py), and drive-things.json, where each is
    drive-stop.json       every standing thing of the painting where the camera stops: [{ "sprite", "X", "z" }], far first
                          (those a regular row puts there too marked "row": "pole", "post" or "fence")

and looks at each into out/highway-drive/. Everything is painted by highway.py's own code: this script runs the painting
once, exactly as highway.py does (it checks that it gets back.png again, index for index), and takes the sky, the
road's marks, the things and the sign from it. The numbers every part shares are in highway_drive_kit.py."""

import json
import os
import sys
import time

import numpy as np
from PIL import Image

import highway as HW
from brush import save
from highway_kit import grade
from nevada_limo_drive_kit import finish as strip_finish, look, seam
import highway_drive_kit as K
import highway_drive_world as Wd
import highway_drive_sky as S
import highway_drive_ground as G
import highway_drive_things as T

OUT = "out/highway"
WORK = "out/highway-drive"
SEED = 1800


def painting():
    """highway.py's painting, run once: its under(), its brush pass, and its details() one thing at a time.
    -> dict(info, brushed, final (before grade), records, sign, palette)."""
    base, info = HW.under()
    info["under"] = base
    brushed = HW.strokes(base, sizes=(14, 7, 3), seed=2, density=1.5, jitter=0.03, keep=0.22)
    final, records, sign = Wd.details_one_by_one(brushed.copy(), info)
    back = grade(final)
    from brush import grain, palette_of
    g = grain(back, 7, 0.02)
    colors = min(152, len(np.unique((g * 255).astype(np.uint8).reshape(-1, 3), axis=0)))
    pal = palette_of([g.reshape(-1, 1, 3)], colors=colors)
    return dict(info=info, brushed=brushed, final=final, back=back, records=records, sign=sign, palette=pal)


def report(path, idx, pal, alpha=None, loops=False):
    shown = pal[idx]
    s = seam(shown) if loops else None
    print(f"  {os.path.basename(path)}: {idx.shape[1]} x {idx.shape[0]}, {len(pal)} colours, {os.path.getsize(path):,} bytes"
          + (f", seam {s[0]:.4f} (neighbouring columns anywhere {s[1]:.4f})" if s else "")
          + (f", {100 * float((alpha >= 0.5).mean()):.1f}% painted" if alpha is not None else ""))
    return shown


def do_sky(P, fast):
    idx, _ = S.paint_sky(P, fast)
    save(f"{OUT}/sky.png", idx, P["palette"])
    shown = report(f"{OUT}/sky.png", idx, P["palette"])
    raw = f"{OUT}/back.png"
    if os.path.exists(raw):
        same = np.asarray(Image.open(raw)) == idx
        print(f"    the same as back.png at {100 * same.mean():.1f}% of its pixels ({100 * same[:330].mean():.1f}% above the horizon)")
    look(f"{WORK}/sky.png", shown)


def do_light():
    """The light that stays on the stage (beyond the contract's table: the engine's `light`), for the strips as written."""
    L, src = S.lights(OUT)
    L8 = {}
    for name in ("shade", "glow"):
        path = f"{OUT}/light-{name}.png"
        Image.fromarray(S.to8(L[name]), "RGBA").save(path, optimize=True)
        L8[name] = np.asarray(Image.open(path), np.float32) / 255
        a = L8[name][..., 3]
        print(f"  light-{name}.png: 800 x 600 RGBA, {os.path.getsize(path):,} bytes, alpha up to {a.max():.3f} "
              f"({100 * float((a > 0).mean()):.1f}% of the stage)")
    if os.path.exists(f"{OUT}/light-shine.png"):                          # (an earlier try: the shine is in light-glow now)
        os.remove(f"{OUT}/light-shine.png")
    lit = S.lay(S.lay(src["D"], L8["shade"], "multiply"), L8["glow"], "screen")
    d = np.abs(lit - src["target"])[331:] * 255
    print(f"    the drive's ground on average, with the two laid on it, against the painting's on average, lit: {d.mean():.2f} "
          f"levels off on average, {np.percentile(d, 99):.1f} at the 99th percentile")
    for c in ("road", "sand", "plain"):
        r = src["ratio"][c]
        print(f"    the painting's {c} against the haze's, from the horizon down (rows 331, 360, 420, 520, 599): "
              + ", ".join(f"{r[i].mean():.2f}" for i in (0, 29, 89, 189, 268)))
    look(f"{WORK}/lights.png", np.concatenate([np.concatenate([src["D"], lit], 1),
                                                np.concatenate([L8["glow"][..., :3] * L8["glow"][..., 3:],
                                                                1 - L8["shade"][..., 3:] * (1 - L8["shade"][..., :3])], 1)], 0))


def do_ground(P, fast):
    marks = Wd.road_marks(P["info"])
    T_ = G.world_textures(SEED)
    TF = G.far_textures(SEED + 40)                                         # PAINT-18B: the plain out to 150 m
    only = [a for a in ("road", "desert-l", "desert-r", "far-l", "far-r") if a in sys.argv[1:]]
    strips = {}
    if not only or "road" in only:
        strips["road"], _ = G.paint_road(T_, marks, seed=SEED + 1, fast=fast)
    for name, sd in (("desert-l", 10), ("desert-r", 20)):
        if not only or name in only:
            strips[name] = G.paint_desert(T_, name, SEED + sd, fast=fast, TF=TF)
    for name, sd in (("far-l", 50), ("far-r", 60)):
        if not only or name in only:
            strips[name] = G.paint_far(TF, name, SEED + sd, fast=fast)
    for name, pic in strips.items():
        t = time.time()
        X = np.abs(K.strip_X(name))[:, None]
        # grain and speckle in full where the strip is seen close by; the desert beyond 15 m out is only ever seen far
        # off, averaged by the engine, where they would only cost bytes
        where = np.broadcast_to(np.clip(1 - (X - 15.0) / 15.0, 0.1, 1.0), pic.shape[:2]) if name != "road" else None
        idx, pal = strip_finish(pic, SEED + 30 + len(name), 144 if name == "road" else 64,
                                grain=0.022 if name == "road" else 0.016, speckle=0.014 if name == "road" else 0.010, where=where)
        path = f"{OUT}/drive-{name}.png"
        save(path, idx, pal)
        shown = report(path, idx, pal, loops=True)
        look(f"{WORK}/{name}.png", shown)
        if name == "road":
            look(f"{WORK}/road-stop.png", shown[:, 384:1536], k=2)              # the stretch from 8 to 32 m when the camera stops


def do_things(P):
    fin = T.Finish(P["palette"])
    pieces = T.stop_pieces(P["records"], P["final"], fin)
    birds = T.stop_birds(P["final"], fin)
    sign, sign_bc, _ = T.sign_pieces(P["sign"]["after"], fin, f"{OUT}/sign-bc.png")
    pole = T.pole_piece(P["records"], fin)
    gen = T.generic()
    idx, alpha, pal, meta = T.sheet(pieces + birds + [sign, sign_bc, pole], gen, P["palette"], f"{OUT}/sign-bc.png")
    save(f"{OUT}/drive-things.png", idx, pal, alpha)
    report(f"{OUT}/drive-things.png", idx, pal, alpha)
    with open(f"{OUT}/drive-things.json", "w") as f:
        f.write(json_text(meta))
    print(f"  drive-things.json: {len(meta['sprites'])} sprites ({len(pieces) + len(birds)} of the painting's own things, the two signs, "
          f"the pole, {len(gen)} for the rows)")
    look(f"{WORK}/things.png", pal[idx], alpha=alpha, under="#c8a4a0")
    stop = stop_json(pieces + birds + [sign], P["records"])
    with open(f"{OUT}/drive-stop.json", "w") as f:
        f.write("[\n" + ",\n".join("  " + json.dumps(t, separators=(", ", ": ")) for t in stop) + "\n]\n")
    rows = sum(1 for t in stop if "row" in t)
    print(f"  drive-stop.json: {len(stop)} set pieces ({len(stop) - rows} the painting's own, the sign among them; {rows} where its rows' "
          f"poles, reflector posts and fence posts stand)")


def json_text(d):
    """Indented JSON with each sprite or set piece on one line."""
    def one(v):
        return json.dumps(v, separators=(", ", ": "))
    lines = ["{"]
    keys = list(d)
    for i, k in enumerate(keys):
        v = d[k]
        end = "," if i < len(keys) - 1 else ""
        if isinstance(v, dict) and k in ("sprites", "rows"):
            lines.append(f"  {json.dumps(k)}: {{")
            ks = list(v)
            for j, n in enumerate(ks):
                lines.append(f"    {json.dumps(n)}: {one(v[n])}" + ("," if j < len(ks) - 1 else ""))
            lines.append("  }" + end)
        elif isinstance(v, list) and k == "things":
            lines.append(f"  {json.dumps(k)}: [")
            for j, t in enumerate(v):
                lines.append(f"    {one(t)}" + ("," if j < len(v) - 1 else ""))
            lines.append("  ]" + end)
        else:
            lines.append(f"  {json.dumps(k)}: {one(v)}{end}")
    lines.append("}")
    return "\n".join(lines) + "\n"


STOP_FAR = 170.0                       # drive-stop.json runs out to the windpump: every standing thing of the painting nearer


def stop_json(pieces, records):
    """drive-stop.json: every standing thing of the painting where the camera stops, far first, as the contract has it:
    [{ "sprite", "X", "z" }] (z metres ahead of the stopped camera, X metres right of the middle of the road; every one
    stands on the ground, Y 0: the birds' boxes run down to the ground under them). Its own things (each its own sprite,
    cut out of the painting: bushes, tufts, stones, the two tumbleweeds, the jackrabbit, the three birds, the windpump,
    the strip of tire, the bottle and the hubcap)
    and the sign; and, marked "row", the things a regular row would put there too, where the painting has them (the
    telephone poles, the reflector posts, the fence posts): place those, or phase the rows to them and leave them out."""
    things = []
    for p in pieces:
        things.append({"sprite": p["name"], "X": round(float(p["X"]), 3), "z": round(float(p["z"]), 3)})
    for r in records:
        z = r["z"] / 100.0
        if z > STOP_FAR:
            continue
        X = r["what"][0] / 100.0
        if r["kind"] == "pole":
            things.append({"sprite": "pole", "X": round(X, 3), "z": round(z, 3), "row": "pole"})
        elif r["kind"] == "marker":
            things.append({"sprite": "post", "X": round(X, 3), "z": round(z, 3), "row": "post"})
        elif r["kind"] == "post":                                          # (the fence posts: the sprite nearest in height)
            tall = r["what"][2] / 100.0
            things.append({"sprite": f"fence-{1 if tall < 1.19 else 2}-{'l' if X < 0 else 'r'}", "X": round(X, 3), "z": round(z, 3), "row": "fence"})
    things.sort(key=lambda t: (-t["z"], t["X"]))
    return things


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    fast = "fast" in sys.argv
    want = [a for a in ("sky", "ground", "things", "light") if a in sys.argv[1:]] or ["sky", "ground", "things", "light"]
    t0 = time.time()
    P = None
    if set(want) - {"light"}:
        P = painting()
        idx = S.finish_as_back(P["back"], P["palette"])
        same = os.path.exists(f"{OUT}/back.png") and np.array_equal(np.asarray(Image.open(f"{OUT}/back.png")), idx)
        print(f"the painting, run again: {time.time() - t0:.0f} s; " + ("back.png again, index for index" if same else "NOT back.png: the hand has changed"))
    for part in want:
        t = time.time()
        print(part + (" (fast)" if fast else ""))
        {"sky": lambda: do_sky(P, fast), "ground": lambda: do_ground(P, fast), "things": lambda: do_things(P), "light": do_light}[part]()
        print(f"  {time.time() - t:.0f} s")
    print(f"done in {time.time() - t0:.0f} s")

#!/usr/bin/env python3
"""The game's paints: key a painted scene, every picture file of it, at the game's strength (50).

    python3 postimp_key.py rome-street               keys out/rome-street/ (the scene's script's painting) into
                                                     out/rome-street-keyed/, to look at
    python3 postimp_key.py rome-street --from DIR --to DIR [--strength N]
    python3 postimp_key.py --js                      writes js/art/look-data.js: the keys and the table of which scene
                                                     uses which, for the people and the moving things (run it after
                                                     adding a scene or changing a key)
    python3 postimp_key.py --check                   checks every scene's pictures in art/scenes against
                                                     postimp_keyed.json (what was installed, keyed, from what)

install.py keys every scene as it installs it (`python3 install.py rome-street`: see the README, "The paints"), so a
repainted scene, or a new one, goes in keyed. Never key a picture twice: install.py starts from the painting in out/.

How a scene is keyed (docs/DESIGN.md, "The paints"):
  - The picture as the game composes it with nobody on stage (back + its cut-outs in their first state: the plan in
    postimp_plans.py) is painted as one picture, so the cut-outs and what is round them read the same light and get the
    same strokes. back.png is that painting wherever the back shows, and the back keyed alone under the cut-outs (seen
    only when a cut-out sways or goes).
  - Each cut-out is the painting under its own edge (alpha), so it fits exactly; a cut-out of another state (the open
    lids, the open piano) is cut from the painting of the picture in that state.
  - All the files of a scene share one palette of 255 colours (k-means in OKLab), as indexed PNGs like the painter's,
    with a little speckle as a scan has; so a cut-out's edge meets the back in the same paints.
  - The small moving things' frames (birds, the cat, the radiator's steam, the kites, the wagon from behind) are keyed
    colour by colour (a palette remap: no shape changes), without strokes.

Needs numpy, Pillow and OpenCV (pip install opencv-python-headless). The pictures in the game were keyed with numpy
2.5.3, Pillow 12.3.0 and OpenCV 5.0.0; another version of OpenCV may differ in a few pixels.
"""

import glob
import hashlib
import json
import os
import shutil
import sys
import time

import cv2
import numpy as np
from PIL import Image

from postimp_look import key_points, paint, read_maps
from postimp_oklab import F32, lab_to_rgb, rgb_to_lab
from postimp_paints import (ERA_KEY, GROUND_ALPHA_GAIN, GROUND_SHADOW, KEYS, PAINTS, PEOPLE, SCENE_KEY, SCENE_PAINTS,
                            STRENGTH, key_for)
from postimp_plans import PLANS, alpha, load_rgb, path, picture

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.normpath(os.path.join(HERE, "..", ".."))
ART = os.path.join(GAME, "art", "scenes")
LEDGER = os.path.join(HERE, "postimp_keyed.json")
LOOK_DATA = os.path.join(GAME, "js", "art", "look-data.js")


# ------------------------------------------------------------------ 256 colours, as the game keeps its pictures
def palette_for(pictures, masks, colors=255, seed=5):
    """One palette for several pictures (k-means in OKLab on a sample of the pixels under their masks)."""
    rng = np.random.default_rng(seed)
    px = np.concatenate([rgb_to_lab(p[m]).reshape(-1, 3) for p, m in zip(pictures, masks)])
    take = px[rng.choice(len(px), size=min(len(px), 90000), replace=False)].astype(np.float32)
    w = np.array([1.6, 1.0, 1.0], np.float32)                               # lightness matters most to the eye here
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-5)
    cv2.setRNGSeed(seed)
    _, _, centers = cv2.kmeans(take * w, colors, None, crit, 2, cv2.KMEANS_PP_CENTERS)
    return centers / w                                                      # OKLab


def to_index(rgb, pal_lab, seed=5, speckle=0.004):
    """Each pixel to its nearest palette colour, with a little noise first (a scan's speckle, lighter)."""
    h, w, _ = rgb.shape
    rng = np.random.default_rng(seed)
    lab = rgb_to_lab(rgb).reshape(-1, 3)
    lab = lab + np.concatenate([rng.normal(0, speckle, (len(lab), 1)), rng.normal(0, speckle * 0.5, (len(lab), 2))], axis=1).astype(F32)
    wt = np.array([1.6, 1.0, 1.0], np.float32)
    P = pal_lab * wt
    out = np.empty(len(lab), np.uint8)
    for i in range(0, len(lab), 60000):
        q = lab[i:i + 60000] * wt
        d = (q * q).sum(1)[:, None] - 2 * q @ P.T + (P * P).sum(1)[None, :]
        out[i:i + 60000] = d.argmin(1)
    return out.reshape(h, w)


def save_indexed(dst, index, pal_lab, mask=None):
    pal = np.clip(np.round(lab_to_rgb(pal_lab[None, :, :])[0] * 255), 0, 255).astype(np.uint8)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if mask is None:
        im = Image.fromarray(index, "P")
        im.putpalette(pal.tobytes())
        im.save(dst, optimize=True)
        return
    clear = len(pal)
    idx = index.copy()
    idx[~mask] = clear
    im = Image.fromarray(idx, "P")
    im.putpalette(pal.tobytes() + bytes(3))
    im.save(dst, optimize=True, transparency=clear)


# ------------------------------------------------------------------ the small moving things
def key_frame(src, dst, key, strength):
    """A frame keyed colour by colour. A palette picture keeps its indexes (a palette remap); an RGBA one keeps its
    alpha. Ground shadows (dark, see-through) take the key's shadow."""
    im = Image.open(src)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if im.mode == "P":
        pal = np.asarray(im.getpalette(), np.uint8).reshape(-1, 3).astype(F32) / 255
        new = key_points(pal, key, strength)
        out = im.copy()
        out.putpalette(np.clip(np.round(new * 255), 0, 255).astype(np.uint8).ravel().tolist())
        if "transparency" in im.info:
            out.info["transparency"] = im.info["transparency"]
            out.save(dst, optimize=True, transparency=im.info["transparency"])
        else:
            out.save(dst, optimize=True)
        return
    rgba = np.asarray(im.convert("RGBA"), F32) / 255
    rgb = rgba[..., :3]
    mean_l = float((rgb.mean(-1) * rgba[..., 3]).sum() / max(1e-6, rgba[..., 3].sum()))
    laid = 1.0 if mean_l < 0.25 else None                                  # a see-through dark: a shadow on the ground
    new = key_points(rgb, key, strength, laid=None if laid is None else np.full(rgb.shape[:2], laid, F32))
    out = np.dstack([new, rgba[..., 3:]])
    Image.fromarray(np.clip(np.round(out * 255), 0, 255).astype(np.uint8), "RGBA").save(dst, optimize=True)


# ------------------------------------------------------------------ a scene
def files_of(scene, src):
    """The scene's picture files in `src`, sorted into the plan's parts. Stops at a file the plan does not know."""
    plan = PLANS[scene]
    named = {"back"} | set(plan["planes"]) | set(plan["alt"]) | set(plan["union"]) | {n for names in plan.get("states", {}).values() for n in names}
    frames = sorted({os.path.basename(f)[:-4] for pat in plan["frames"] for f in glob.glob(os.path.join(src, pat + ".png"))})
    have = sorted(f[:-4] for f in os.listdir(src) if f.endswith(".png"))
    unknown = [f for f in have if f not in named and f not in frames]
    missing = [f for f in named if f not in have]
    if unknown or missing:
        raise SystemExit(f"{scene}: the plan in postimp_plans.py does not fit {src}: "
                         + (f"not in the plan: {', '.join(unknown)}. " if unknown else "")
                         + (f"missing: {', '.join(sorted(missing))}." if missing else ""))
    return frames


def key_scene(scene, src, dst, strength=STRENGTH, quiet=False):
    """Key every picture file of a painted scene in `src` (the painting as its script left it) into `dst`.
    Returns the names of the files written."""
    if scene not in PLANS or scene not in SCENE_KEY:
        raise SystemExit(f"{scene}: no plan (postimp_plans.PLANS) or no key (postimp_paints.SCENE_KEY) for it yet: add them first.")
    t0 = time.time()
    key, plan = key_for(scene), PLANS[scene]
    frames = files_of(scene, src)
    comp = picture(src, plan)
    back = load_rgb(path(src, "back"))
    lab_c, lab_b = rgb_to_lab(comp), rgb_to_lab(back)
    maps_c, maps_b = read_maps(lab_c, key), read_maps(lab_b, key)
    planes = list(plan["planes"])
    masks = {n: alpha(src, n) for n in planes}
    covered = np.zeros(back.shape[:2], bool)
    for n in planes:
        covered |= masks[n]
    alts = {}
    for alt, replaces in plan["alt"].items():
        pic = picture(src, plan, extra=[alt], without=replaces)
        lab = rgb_to_lab(pic)
        alts[alt] = (pic, lab, read_maps(lab, key), alpha(src, alt))
    # Further states of an alt (the trunk as the story empties it): keyed from the picture in that state as the alt is,
    # but left out of the palette's sample (postimp_plans.py, "states"), so that adding one changes no other file.
    states = {}
    for base_alt, names in plan.get("states", {}).items():
        for n in names:
            pic = picture(src, plan, extra=[n], without=plan["alt"][base_alt])
            lab = rgb_to_lab(pic)
            states[n] = (pic, lab, read_maps(lab, key), alpha(src, n))
    unions = {u: np.any([masks[n] for n in parts], axis=0) for u, parts in plan["union"].items()}
    st = strength
    pc = paint(comp, key, st, maps=maps_c, lab0=lab_c)
    pb = paint(back, key, st, maps=maps_b, lab0=lab_b)
    back_out = np.where(covered[..., None], pb, pc)
    painted_alts = {a: paint(p, key, st, maps=m, lab0=l) for a, (p, l, m, _) in alts.items()}
    painted_states = {n: paint(p, key, st, maps=m, lab0=l) for n, (p, l, m, _) in states.items()}
    # A cut-out that another cut-out lies over (the pencil on the armchair, the door mirror on the wagon, the flashlight
    # in the fort's way in) is keyed from the picture with nothing over it: back and the cut-outs up to itself. Taken from
    # the whole composite, it would carry the thing over it baked into its own pixels, and show it after the game had
    # hidden that thing (a pencil still on the crossword once it is in the pocket). Elsewhere the two pictures are the same.
    pcs = {}
    for i, n in enumerate(planes):
        above = [m for m in planes[i + 1:] if (masks[n] & masks[m]).any()]
        if not above:
            pcs[n] = pc
            continue
        own = picture(src, plan, without=planes[i + 1:])
        lab_n = rgb_to_lab(own)
        pcs[n] = paint(own, key, st, maps=read_maps(lab_n, key), lab0=lab_n)
    full = np.ones(back.shape[:2], bool)
    pal = palette_for([back_out, pc] + list(painted_alts.values()), [full, covered] + [alts[a][3] for a in alts])
    written = ["back"]
    save_indexed(path(dst, "back"), to_index(back_out, pal, seed=st), pal)
    ic = to_index(pc, pal, seed=st + 1)
    for n in planes:
        if pcs[n] is pc:
            save_indexed(path(dst, n), ic, pal, masks[n])
        else:
            save_indexed(path(dst, n), to_index(pcs[n], pal, seed=st + 1), pal, masks[n])
        written.append(n)
    for u, m in unions.items():
        save_indexed(path(dst, u), ic, pal, m)
        written.append(u)
    for a, pa in painted_alts.items():
        save_indexed(path(dst, a), to_index(pa, pal, seed=st + 2), pal, alts[a][3])
        written.append(a)
    for n, pn in painted_states.items():
        save_indexed(path(dst, n), to_index(pn, pal, seed=st + 2), pal, states[n][3])
        written.append(n)
    for f in frames:
        key_frame(path(src, f), path(dst, f), key, st)
        written.append(f)
    if not quiet:
        print(f"{scene}: keyed in {SCENE_KEY[scene]} at {st}: {len(written)} pictures, {time.time() - t0:.1f}s")
    return [w + ".png" for w in written]


# ------------------------------------------------------------------ what was installed (postimp_keyed.json)
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def ledger():
    try:
        return json.load(open(LEDGER))
    except FileNotFoundError:
        return {}


def record(scene, raw_dir, keyed_dir, names, strength=STRENGTH):
    """Note in postimp_keyed.json what each installed file was keyed from and what it became."""
    led = ledger()
    led[scene] = {"key": SCENE_KEY[scene], "strength": strength,
                  "files": {n: {"raw": sha(os.path.join(raw_dir, n)), "keyed": sha(os.path.join(keyed_dir, n))} for n in sorted(names)}}
    with open(LEDGER, "w") as f:
        json.dump(dict(sorted(led.items())), f, indent=1)
        f.write("\n")


def check():
    """Every scene's pictures in art/scenes against the ledger: keyed, installed raw, or changed since."""
    led, problems = ledger(), 0
    for scene in PLANS:
        folder = os.path.join(ART, scene)
        entry = led.get(scene)
        if not entry:
            print(f"{scene}: not keyed (not in postimp_keyed.json)"); problems += 1; continue
        if entry["key"] != SCENE_KEY.get(scene) or entry["strength"] != STRENGTH:
            print(f"{scene}: keyed in {entry['key']} at {entry['strength']}, but the table says {SCENE_KEY.get(scene)} at {STRENGTH}")
            problems += 1
        names = sorted(f for f in os.listdir(folder) if f.endswith(".png"))
        for n in names:
            e = entry["files"].get(n)
            h = sha(os.path.join(folder, n))
            if not e:
                print(f"{scene}/{n}: not keyed (new since)"); problems += 1
            elif h == e["raw"]:
                print(f"{scene}/{n}: installed unkeyed"); problems += 1
            elif h != e["keyed"]:
                print(f"{scene}/{n}: changed since it was keyed (repainted? install it again with install.py)"); problems += 1
        for n in entry["files"]:
            if n not in names:
                print(f"{scene}/{n}: keyed, but no longer in art/"); problems += 1
    # every folder of pictures has a plan, and the game's copy of the table is current
    for sid in [s for s in os.listdir(ART) if os.path.isdir(os.path.join(ART, s))]:
        if sid not in PLANS:
            print(f"{sid}: has pictures, but no plan in postimp_plans.py"); problems += 1
    try:
        if open(LOOK_DATA).read() != look_data():
            print("js/art/look-data.js is out of date: run python3 postimp_key.py --js"); problems += 1
    except FileNotFoundError:
        print("js/art/look-data.js is missing: run python3 postimp_key.py --js"); problems += 1
    print("the paints: " + ("all keyed, and the game's table is current" if not problems else f"{problems} problem(s)"))
    return problems


# ------------------------------------------------------------------ the game's copy of the keys (js/art/look-data.js)
def look_data():
    def lab(v):
        v = PAINTS[v]["lab"] if isinstance(v, str) else np.asarray(v)
        return [round(float(x), 6) for x in v]

    def ramp(names):
        return sorted([lab(n) for n in names], key=lambda t: t[0])

    keys = {}
    for name, k in KEYS.items():
        keys[name] = {
            "title": k["title"],
            "pair": [lab(k["pair"][0]), lab(k["pair"][1])],
            "light": ramp(k["light"]),
            "sky": ramp(k["sky"]),
            "lightGreen": ramp(["veronese-green", "emerald-green", "viridian"]),
            "shadow": {f: ramp(v) for f, v in k["shadow"].items()},
            "weight": {p: float(k["weight"].get(p, 0.8)) for p in SCENE_PAINTS},
            "turnPaint": lab(k.get("turn_paint", "chrome-orange")),
            **{n: float(k[n]) for n in ("warm_light", "shade", "turn", "snap", "chroma", "shade_lo", "shade_hi", "lift")},
            "lit_lo": float(k.get("lit_lo", 0.55)), "lit_hi": float(k.get("lit_hi", 0.80)),
            "turn_orange": float(k.get("turn_orange", 0.18)),
            "light_chroma": float(k.get("light_chroma", 0.5)),
            "light_add": float(k.get("light_add", 0.04)),
            "people": {n: float(v) for n, v in PEOPLE.items()},
            "groundL": float(GROUND_SHADOW[name]),
        }
    data = {
        "strength": STRENGTH,
        "white": lab("lead-white"),
        "paints": {n: lab(n) for n in SCENE_PAINTS},
        "prussian": lab("prussian-blue"),
        "deepViolet": lab("deep-violet"),
        "keys": keys,
        "scenes": SCENE_KEY,
        "eras": ERA_KEY,
        "groundAlphaGain": GROUND_ALPHA_GAIN,
    }
    return ("// Written by tools/paint/postimp_key.py --js: the game's paint box and its keys, and which scene uses which\n"
            "// (tools/paint/postimp_paints.py; see docs/DESIGN.md, \"The paints\"). Do not edit by hand.\n"
            "export const LOOK_DATA = " + json.dumps(data, separators=(",", ":")) + ";\n")


def write_js():
    with open(LOOK_DATA, "w") as f:
        f.write(look_data())
    print("wrote", os.path.relpath(LOOK_DATA, GAME))


# ------------------------------------------------------------------
def main(args):
    if "--js" in args:
        return write_js()
    if "--check" in args:
        sys.exit(1 if check() else 0)
    opt = lambda name, default=None: args[args.index(name) + 1] if name in args else default
    scenes = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or not args[i - 1].startswith("--"))]
    if not scenes:
        print(__doc__)
        return
    strength = int(opt("--strength", STRENGTH))
    for scene in scenes:
        folder = PLANS.get(scene, {}).get("folder", scene)
        src = opt("--from", os.path.join(HERE, "out", folder))
        dst = opt("--to", os.path.join(HERE, "out", folder + "-keyed"))
        if os.path.normpath(src) == os.path.normpath(dst):
            raise SystemExit("--from and --to must be different folders (a picture is never keyed twice)")
        os.makedirs(dst, exist_ok=True)
        key_scene(scene, src, dst, strength)
        print(f"  into {dst}")


if __name__ == "__main__":
    main(sys.argv[1:])

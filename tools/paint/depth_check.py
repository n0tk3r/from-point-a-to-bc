#!/usr/bin/env python3
"""The three planes, measured (round twenty-three: tools/paint/DEPTH.md).

    python3 depth_check.py <scene id> [--art DIR] [--out PNG]

Reads the scene file through scene_dump.mjs (needs node) and the scene's pictures (art/scenes/<id>/, or DIR: a painter's
out/ folder), lays the backdrop, the floor cut-outs and the front plane together, and says:

  NEAR    how much of the picture the front plane covers, which edges of the frame it reaches, how dark it is beside the rest
  HIDDEN  every clickable area, standing place and mark that the front plane hides too much of
  GROUND  how much of the walkable ground is flat, empty colour; how its tone runs from far to near
  PEOPLE  how tall a grown-up is at the marks (a scene whose people are all small is seen from too far away)

and writes a picture to look at (out/<id>-depth.png, or PNG): the front plane tinted red, areas outlined, a box for a
grown-up at every mark. The numbers are a floor, not the goal: look at the picture.
"""

import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
NODE = os.environ.get("NODE", "node")
W, H = 800, 600
LUM = np.array([0.30, 0.55, 0.15], dtype=np.float32)


def dump(scene):
    for node in (NODE, "/opt/node22/bin/node"):
        try:
            out = subprocess.run([node, os.path.join(HERE, "scene_dump.mjs"), scene], capture_output=True, text=True, cwd=ROOT, timeout=60)
            if out.returncode == 0:
                return json.loads(out.stdout.strip().splitlines()[-1])
        except FileNotFoundError:
            continue
    sys.exit("scene_dump.mjs failed: " + (out.stderr or out.stdout)[-400:])


def load(path):
    """-> (rgb float, alpha float) at the stage's size, or None."""
    if not os.path.exists(path):
        return None
    im = Image.open(path).convert("RGBA")
    if im.size != (W, H):
        return None
    a = np.asarray(im, dtype=np.float32) / 255
    return a[..., :3], a[..., 3]


def poly_mask(points):
    im = Image.new("L", (W, H), 0)
    if points and len(points) >= 3:
        ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in points], fill=255)
    return np.asarray(im, dtype=np.float32) / 255


def main(argv):
    if not argv or argv[0].startswith("-"):
        sys.exit(__doc__)
    scene = argv[0]
    art = os.path.join(ROOT, "art", "scenes", scene)
    out_png = os.path.join(HERE, "out", f"{scene}-depth.png")
    if "--art" in argv:
        art = argv[argv.index("--art") + 1]
    if "--out" in argv:
        out_png = argv[argv.index("--out") + 1]
    d = dump(scene)
    hz, full = float(d["horizon"]), float(d["full"])

    back = load(os.path.join(art, "back.png"))
    if back is None:
        sys.exit(f"no 800x600 back.png in {art}")
    comp = back[0].copy()
    near = np.zeros((H, W), dtype=np.float32)
    near_rgb = np.zeros((H, W, 3), dtype=np.float32)
    missing = []
    for p in d["planes"]:
        pic = load(os.path.join(art, os.path.basename(p["src"]))) if p.get("src") else None
        if pic is None:
            if p.get("src"):
                missing.append(os.path.basename(p["src"]))
            continue
        rgb, a = pic
        if p["plane"] == "front":
            near_rgb = near_rgb * (1 - a[..., None]) + rgb * a[..., None]
            near = np.maximum(near, a)
        elif not p["conditional"]:
            comp = comp * (1 - a[..., None]) + rgb * a[..., None]
    whole = comp * (1 - near[..., None]) + near_rgb * near[..., None]
    lum = whole @ LUM
    problems, notes = [], []

    # ---------------------------------------------------------------- NEAR: the front plane
    share = float(near.mean())
    edges = {"left": float(near[:, :6].max(axis=1).mean()), "right": float(near[:, -6:].max(axis=1).mean()),
             "top": float(near[:6, :].max(axis=0).mean()), "bottom": float(near[-6:, :].max(axis=0).mean())}
    reached = [k for k, v in edges.items() if v >= 0.12]
    l_near = float((lum * near).sum() / max(near.sum(), 1))
    rest = 1 - near
    l_rest = float((lum * rest).sum() / max(rest.sum(), 1))
    print(f"NEAR    the front plane covers {share * 100:.1f}% of the picture; it reaches the frame's " + (", ".join(f"{k} ({edges[k] * 100:.0f}%)" for k in reached) or "no edge"))
    print(f"        its tone {l_near:.2f} beside {l_rest:.2f} for everything behind it (difference {abs(l_near - l_rest):.2f})")
    if share < 0.10:
        problems.append(f"NEAR: the front plane covers {share * 100:.1f}% of the picture: at least 10% (12 to 25% is usual)")
    if share > 0.34:
        problems.append(f"NEAR: the front plane covers {share * 100:.1f}%: over a third of the picture hides the play")
    if len(reached) < 2:
        problems.append("NEAR: the front plane should run off at least two edges of the frame (things near us are cut off by it)")
    if share >= 0.03 and abs(l_near - l_rest) < 0.10:
        problems.append(f"NEAR: the front plane's tone ({l_near:.2f}) is too close to the rest ({l_rest:.2f}): it should be a clear dark (or, in a dark room, a clear light) mass")

    # ---------------------------------------------------------------- HIDDEN: what the front plane covers
    def scale_at(y):
        return min(max((y - hz) / max(full - hz, 1), d["minScale"]), d["maxScale"])

    def person_box(x, y):
        h = 160 * scale_at(y)
        return [x - h * 0.16, y - h, x + h * 0.16, y]

    hidden = []
    for a in d["areas"]:
        if a["shape"]:
            m = poly_mask(a["shape"])
            if m.sum() > 20:
                cov = float((m * near).sum() / m.sum())
                if 0.35 < cov < 0.70:                      # (70% and more: it is the near thing itself, or lies on it)
                    hidden.append(f"area '{a['id']}' is {cov * 100:.0f}% behind the front plane")
        if a["walkTo"]:
            x0, y0, x1, y1 = [int(round(v)) for v in person_box(*a["walkTo"])]
            box = near[max(y0, 0):max(y1, 1), max(x0, 0):max(x1, 1)]
            if box.size and float(box.mean()) > 0.40:
                hidden.append(f"whoever stands at '{a['id']}' ({a['walkTo'][0]:.0f}, {a['walkTo'][1]:.0f}) is {float(box.mean()) * 100:.0f}% hidden")
    for name, (x, y) in d["marks"].items():
        x0, y0, x1, y1 = [int(round(v)) for v in person_box(x, y)]
        box = near[max(y0, 0):max(y1, 1), max(x0, 0):max(x1, 1)]
        if box.size and float(box.mean()) > 0.40:
            hidden.append(f"whoever stands on the mark '{name}' ({x:.0f}, {y:.0f}) is {float(box.mean()) * 100:.0f}% hidden")
    print("HIDDEN  " + ("nothing that is clicked or stood on" if not hidden else f"{len(hidden)}:"))
    for h in hidden:
        print("        " + h)
        problems.append("HIDDEN: " + h)

    # ---------------------------------------------------------------- GROUND: the walkable floor
    walk = np.zeros((H, W), dtype=np.float32)
    for f in d["floors"]:
        walk = np.maximum(walk, poly_mask(f["area"]))
    for b in d["blocked"]:
        walk = walk * (1 - poly_mask(b))
    if walk.sum() > 400:
        gl = (comp @ LUM)
        calm = gl.reshape(H // 4, 4, W // 4, 4).mean(axis=(1, 3))          # (the grain of the paint averaged away)
        cells = flat = 0
        for y in range(0, H, 24):
            for x in range(0, W, 24):
                w = walk[y:y + 24, x:x + 24]
                if w.mean() > 0.8:
                    cells += 1
                    if calm[y // 4:y // 4 + 6, x // 4:x // 4 + 6].std() < 0.013:
                        flat += 1
        ys = np.where(walk.max(axis=1) > 0)[0]
        y_far, y_near = ys.min(), ys.max()
        band = max(8, (y_near - y_far) // 5)
        far_m = walk[y_far:y_far + band]
        near_m = walk[y_near - band:y_near]
        l_far = float((gl[y_far:y_far + band] * far_m).sum() / max(far_m.sum(), 1))
        l_nr = float((gl[y_near - band:y_near] * near_m).sum() / max(near_m.sum(), 1))
        share_flat = flat / max(cells, 1)
        print(f"GROUND  {share_flat * 100:.0f}% of the walkable ground is flat colour ({flat} of {cells} squares of 24 px); its tone runs {l_far:.2f} far to {l_nr:.2f} near")
        if share_flat > 0.40:
            problems.append(f"GROUND: {share_flat * 100:.0f}% of the walkable ground is flat, empty colour: lay shadows, joints, ruts, stones, tufts across it, in perspective (under 40%)")
        if abs(l_far - l_nr) < 0.04:
            notes.append(f"GROUND: far and near ground are the same tone ({l_far:.2f}, {l_nr:.2f}): let it deepen toward us or lighten toward the horizon")
    else:
        print("GROUND  (no walkable ground to measure)")

    # ---------------------------------------------------------------- WALK: anywhere a person can stand, are they in sight?
    if walk.sum() > 400 and share > 0.01:
        spots = lost = 0
        worst = (0.0, 0, 0)
        for y in range(4, H, 8):
            for x in range(4, W, 8):
                if walk[y, x] < 0.5:
                    continue
                x0, y0, x1, y1 = [int(round(v)) for v in person_box(x, y)]
                box = near[max(y0, 0):max(y1, 1), max(x0, 0):max(min(x1, W), 1)]
                if not box.size:
                    continue
                spots += 1
                c = float(box.mean())
                if c > 0.5:
                    lost += 1
                if c > worst[0]:
                    worst = (c, x, y)
        if spots:
            print(f"WALK    at {lost * 100 / spots:.1f}% of the places a person can stand, more than half of them is behind the front plane (the worst: {worst[0] * 100:.0f}% hidden at ({worst[1]}, {worst[2]}))")
            if lost / spots > 0.08 or worst[0] > 0.85:
                problems.append(f"WALK: at {lost * 100 / spots:.1f}% of the walkable places a person is more than half hidden behind the front plane (worst at ({worst[1]}, {worst[2]})): move the near thing off the walked ground, or ask the lead for a `blocked` patch there")

    # ---------------------------------------------------------------- PEOPLE: how big they are where they stand
    heights = sorted(160 * scale_at(y) for _, (x, y) in d["marks"].items()) + sorted(160 * scale_at(a["walkTo"][1]) for a in d["areas"] if a["walkTo"])
    if heights:
        heights.sort()
        med = heights[len(heights) // 2]
        print(f"PEOPLE  a grown-up is {heights[0]:.0f} to {heights[-1]:.0f} px tall where people stand (middle {med:.0f}); the eye is {(full - hz) * 175 / 160 / 100:.1f} m above the ground")
        if med < 84:
            notes.append(f"PEOPLE: at half the standing places a grown-up is under {med:.0f} px tall: the play is far away (a recomposed scene brings it nearer)")
    if missing:
        notes.append("pictures the scene file names that are not in the folder: " + ", ".join(missing))

    # ---------------------------------------------------------------- the picture to look at
    look = (whole * 255).astype(np.uint8)
    tint = look.astype(np.float32)
    tint[..., 0] = tint[..., 0] * (1 - 0.45 * near) + 255 * 0.45 * near
    im = Image.fromarray(np.clip(tint, 0, 255).astype(np.uint8))
    dr = ImageDraw.Draw(im)
    for f in d["floors"]:
        dr.line([tuple(p) for p in f["area"]] + [tuple(f["area"][0])], fill=(40, 220, 90), width=1)
    for a in d["areas"]:
        if a["shape"]:
            dr.line([tuple(p) for p in a["shape"]] + [tuple(a["shape"][0])], fill=(255, 235, 60), width=1)
        if a["walkTo"]:
            dr.rectangle(person_box(*a["walkTo"]), outline=(80, 200, 255))
    for name, (x, y) in d["marks"].items():
        dr.rectangle(person_box(x, y), outline=(255, 255, 255))
    dr.line([(0, hz), (W, hz)], fill=(255, 80, 255), width=1)
    os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
    im.save(out_png)
    side = Image.new("RGB", (W * 2, H))
    side.paste(Image.fromarray(look), (0, 0))
    side.paste(im, (W, 0))
    side.save(out_png.replace(".png", "-pair.png"))
    for n in notes:
        print("note    " + n)
    print(("DEPTH: PASS" if not problems else f"DEPTH: {len(problems)} TO MEND") + f"   (look at {os.path.relpath(out_png)})")
    for p in problems:
        print("  - " + p)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

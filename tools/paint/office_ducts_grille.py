"""The grille's view (OFFICE-17B): what Ranger sees looking down through a grille with his nose to it.

    python3 office_ducts_grille.py          paints out/office-ducts/grille-view.png and its check pictures

800 x 600 RGBA, laid by the engine over the room it draws under it (the room scene, live). The slats of the grille seen
from above and very close, softly out of focus (the eye is on the room): four broad galvanized slats across the
picture, two of them half out of it at the top and the bottom, the two across the middle narrower (the eye is over the
middle, so it sees their tops, and the outer ones' sides as well); the room's light catching their edges toward the
middle; the duct's dark round the edges of the picture. Between the slats the picture is clear: the slats cover under a
third of it.

It goes in keyed with the Office's key (postimp_plans: a frame of office-ducts, keyed colour by colour, its alpha
untouched), as everything in the scene's folder does. Its check pictures (out/office-ducts-check/grille-*.png) lay it over
three of the game's interiors, the store and two rooms of the house, with the game's people standing in them (the
figures as people_on.py draws them, when the game is being served; without it, the rooms alone)."""

import os
import sys

import numpy as np
from PIL import Image

import brush
from brush import F32, blur, noise, grain, strokes, lerp

W, H = 800, 600
OUT = "out/office-ducts"
CHECK = "out/office-ducts-check"
SEED = 41

# the slats, top to bottom: (middle row, half its height, how soft its edges are, px)
SLATS = [(-16.0, 50.0, 10.0), (190.0, 16.0, 5.5), (410.0, 17.0, 5.5), (616.0, 53.0, 10.0)]
CORE = "#535b6d"             # a slat's top, in the duct's dim light
SIDE = "#6c7482"             # an outer slat's side, which the eye sees as well
RIM = "#eef0d6"              # the room's light catching an edge (warm white, a little green)
DARK = "#24222f"             # the duct's dark round the picture's edges


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return (t * t * (3 - 2 * t)).astype(F32)


def paint():
    y, x = np.mgrid[0:H, 0:W].astype(F32)
    rgb = np.zeros((H, W, 3), F32)
    a = np.zeros((H, W), F32)
    wav = (noise((H, W), (220, 40), SEED, 3) - 0.5) * 3.0                 # nothing is ruled: each edge wanders a little
    mott = noise((H, W), (26, 8), SEED + 1, 3)
    for i, (cy, hh, soft) in enumerate(SLATS):
        top, bot = cy - hh + wav, cy + hh + wav * 0.8
        m = smooth(top - soft, top + soft, y) * (1 - smooth(bot - soft, bot + soft, y))
        k = (y - top) / np.maximum(1e-3, bot - top)                          # 0 at its top edge, 1 at its bottom edge
        col = np.broadcast_to(brush.rgb(CORE), (H, W, 3)).copy()
        outer = i in (0, len(SLATS) - 1)
        if outer:                                                            # the outer ones: their side toward the middle shows too
            side = smooth(0.45, 0.85, k) if i == 0 else 1 - smooth(0.15, 0.55, k)
            col = lerp(col, brush.rgb(SIDE), side[..., None])
        col = col * (0.88 + 0.22 * mott[..., None])
        # the edges toward the middle of the picture catch the room's light, the others a little
        toward = (1 - smooth(0.0, 0.16, 1 - k)) if cy < H / 2 else (1 - smooth(0.0, 0.16, k))
        away = (1 - smooth(0.0, 0.10, k)) if cy < H / 2 else (1 - smooth(0.0, 0.10, 1 - k))
        col = lerp(col, brush.rgb(RIM), np.clip(toward * 0.85 + away * 0.25, 0, 1)[..., None])
        # dust on the outer ones' tops, soft (out of focus)
        if outer:
            fleck = smooth(0.78, 0.92, noise((H, W), 5, SEED + 10 + i, 2)) * 0.35
            col = lerp(col, brush.rgb("#8a8478"), fleck[..., None])
        rgb = rgb * (1 - m[..., None]) + col * m[..., None]
        a = np.maximum(a, m)
    # the duct's dark all round the picture's edges, laid over the slats (premultiplied: dark over what is there)
    e = np.minimum(np.minimum(x, W - 1 - x), np.minimum(y, H - 1 - y)) + (noise((H, W), 60, SEED + 2, 2) - 0.5) * 10
    v = (1 - smooth(0.0, 64.0, e)) ** 1.5 * 0.88
    corner = np.clip(1 - np.hypot((x - W / 2) / (W * 0.62), (y - H / 2) / (H * 0.66)), 0, 1)
    v = np.maximum(v, (1 - smooth(0.0, 0.30, corner)) * 0.70)
    out_a = 1 - (1 - a) * (1 - v)
    pre = rgb * (a * (1 - v))[..., None] + brush.rgb(DARK)[None, None, :] * v[..., None]
    rgb = np.where((out_a > 1e-4)[..., None], pre / np.maximum(out_a, 1e-4)[..., None], brush.rgb(DARK)[None, None, :])
    a = out_a
    # the brush, calm (a soft thing seen close), then the grain
    filled = rgb.copy()
    b = strokes(np.clip(filled, 0, 1), sizes=(9, 5), seed=SEED, density=1.2, jitter=0.03, keep=0.55)
    rgb = lerp(b, filled, 0.35)
    rgb = grain(np.clip(rgb, 0, 1), SEED + 3, 0.010)
    a = blur(a, 1.2)
    return np.clip(rgb, 0, 1), np.clip(a, 0, 1)


def coverage(a):
    return float((a >= 0.5).mean()), float(a.mean())


def save(rgb, a, path):
    out = np.dstack([rgb, a])
    Image.fromarray((out * 255 + 0.5).astype(np.uint8), "RGBA").save(path, optimize=True)


def rooms():
    """Three of the game's interiors as the game composes them with nobody on stage: back and first-state cut-outs."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from postimp_plans import PLANS
    art = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "art", "scenes")
    out = []
    for sid in ("nevada-store", "home-living-room", "home-study"):
        im = Image.open(os.path.join(art, sid, "back.png")).convert("RGBA")
        for n in PLANS[sid]["planes"]:
            p = os.path.join(art, sid, n + ".png")
            if os.path.exists(p):
                im.alpha_composite(Image.open(p).convert("RGBA"))
        out.append((sid, im))
    return out


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(CHECK, exist_ok=True)
    rgb, a = paint()
    save(rgb, a, f"{OUT}/grille-view.png")
    cov, mean_a = coverage(a)
    lum = float((rgb.mean(-1) * a).sum() / max(1e-6, a.sum()))
    print(f"grille-view.png: {cov * 100:.1f}% of the picture covered (alpha at least a half), mean alpha {mean_a:.2f}, "
          f"alpha-weighted mean colour {lum:.3f} (the key's frames read under 0.25 as a ground shadow)")
    view = Image.open(f"{OUT}/grille-view.png").convert("RGBA")
    people = sys.argv[1] if len(sys.argv) > 1 else None
    for sid, im in rooms():
        base = im
        if people and os.path.exists(os.path.join(people, sid + ".png")):
            base = Image.open(os.path.join(people, sid + ".png")).convert("RGBA")
        base.convert("RGB").save(f"{CHECK}/grille-room-{sid}.png")
        comp = base.copy()
        comp.alpha_composite(view)
        comp.convert("RGB").save(f"{CHECK}/grille-{sid}.png")
    print("check pictures:", ", ".join(f"{CHECK}/grille-{s}.png" for s, _ in rooms()))

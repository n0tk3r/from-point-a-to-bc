"""office-breakroom: the depth pass (round twenty-three, wave two; DEPTH.md "The three planes", "Light and air").

Works over the painting as it is: reads out/office-breakroom-orig/ (the full, seeded run of office_breakroom.py, never
changed) and writes the scene's whole set back into out/office-breakroom/, every file as it was, except:

    back.png    deepened: the floor's tile joints through the room's own camera (room.View, a foot square, 30.5 cm, from the back left
                corner), a few heel scuffs (depth.scatter: few and large near, many and small far), the tubes' light
                falling off toward the corners, the far wall (and all that stands at it) a little cooler and paler by
                its distance, the near floor deeper
    front.png   the near tables (the round one, its chair, the low table) deeper and warmer, a lit rim on their tops
    near.png    new: one of the building's columns, boxed in drywall, standing by the lens at the right edge (its lit
                side toward the tubes, its face to us in shade) and the girder's bulkhead it carries across the ceiling

Every clock frame, the door, the vent, the pie's states, the vending machine's states, the chair: copied over as they
are. Run:  python3 office_breakroom_depth.py   (light: a few seconds)
"""

import math
import os
import shutil

import numpy as np
from PIL import Image

import depth
import office_breakroom_model as M
from brush import F32, Sheet, blur, grid, lerp, mask_poly, noise, palette_of, rgb, save, to_palette
from room import View

SRC = os.environ.get("DEPTH_SRC", "out/office-breakroom-orig")      # (DEPTH_SRC/DEPTH_OUT: for a trial elsewhere)
OUT = os.environ.get("DEPTH_OUT", "out/office-breakroom")
V = View(**M.VIEW)
H, W = 600, 800
RW, RD, RH = M.W, M.D, M.H


def load(name):
    im = Image.open(f"{SRC}/{name}").convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


def finish(picture, path, colors, alpha=None, speckle=0.006):
    """Back to a palette, as the scene's own finish does (no second grain: the painting has its grain)."""
    pic = np.clip(picture, 0, 1).astype(F32)
    src = pic if alpha is None else pic[alpha > 0.5][:, None, :]
    pal = palette_of([src], colors=colors)
    idx = to_palette(pic, pal, speckle=speckle)
    save(path, idx, pal, alpha)


# ---------------------------------------------------------------- the room's surfaces, through its camera
def surfaces():
    """-> (d, label): each pixel's distance along the lens axis to the room's shell (cm) and which surface it is
    (0 floor, 1 ceiling, 2 left wall, 3 right wall, 4 back wall). What stands at a wall takes the wall's distance."""
    x, y = grid((H, W))
    a = (x - V.cx) / V.F
    u = (V.hz - y) / V.F
    big = np.full((H, W), 1e9, dtype=F32)
    cands = []
    with np.errstate(divide="ignore", invalid="ignore"):
        cands.append(np.where(u < 0, -V.eye / u, big))                                     # the floor
        cands.append(np.where(u > 0, (RH - V.eye) / u, big))                               # the ceiling
        dx = a * V.rx + V.fx
        cands.append(np.where(dx < 0, -V.cam_x / dx, big))                                 # the left wall
        cands.append(np.where(dx > 0, (RW - V.cam_x) / dx, big))                           # the right wall
        dz = a * V.rz + V.fz
        cands.append(np.where(dz < 0, -V.cam_z / dz, big))                                 # the back wall
    st = np.stack([np.where(c > 0, c, big) for c in cands])
    return st.min(axis=0).astype(F32), st.argmin(axis=0)


def floor_mask(label):
    """The floor where it shows in the backdrop: not the couch, not the two mats."""
    m = (label == 0).astype(F32)
    couch = [[0, 326], [3, 324], [66, 304], [79, 304], [89, 306], [167, 326], [169, 332], [168, 378], [160, 392], [0, 494]]
    m *= 1 - mask_poly((H, W), couch, soft=1.0)
    for x0, y0, x1, y1 in ((298, 358, 380, 380), (543, 345, 636, 368)):
        m *= 1 - mask_poly((H, W), [[x0, y0], [x1, y0], [x1, y1], [x0, y1]], soft=1.0)
    y = grid((H, W))[1]
    m *= np.clip((y - 357) / 3.0, 0, 1)                                                     # under the back wall's foot
    return m


def joints(fl):
    """The floor's tile joints, both ways, through the camera: a hair near, finer far."""
    sh = Sheet((H, W), ss=3)

    def run(points):
        prev = None
        for X, Z in points:
            d = V.depth(X, Z)
            if d < 60:
                prev = None
                continue
            p = V.pt(X, 0, Z)
            if prev is not None:
                k = V.scale_at(X, Z)
                sh.line([prev, p], "#2c2a30", width=max(0.5, 0.45 * k), alpha=float(np.clip(0.4 + 0.15 * k, 0.45, 0.7)))
            prev = p

    T = 30.5                                                                                # (office_breakroom_things.m_floor)
    for i in range(int(RW // T) + 1):
        X = i * T
        run([(X, Z) for Z in np.arange(0, RD + 1, 8.0)])
    for j in range(int(RD // T) + 1):
        Z = j * T
        run([(X, Z) for X in np.arange(0, RW + 1, 8.0)])
    _, a = sh.done()
    return a * fl


def scuffs(fl):
    """Heel marks and a chair-leg scrape or two: few and large near, many and small far."""
    sh = Sheet((H, W), ss=3)
    pts = depth.scatter(lambda X, Z: V.pt(X, 0, Z), lambda X, Z: V.scale_at(X, Z), (0, RW, 0, RD), 2.2, seed=1723,
                        size=(9.0, 2.0), zone=fl)
    for x, y, k, r in pts:
        L = (4 + 7 * r) * k
        ang = (r * 7.3 % 1.0 - 0.5) * 0.9
        dx, dy = math.cos(ang) * L / 2, math.sin(ang) * L / 2 * 0.45
        sh.line([(x - dx, y - dy), (x + dx, y + dy)], "#24222a", width=max(0.4, 0.9 * k), alpha=0.18 + 0.12 * r)
    _, a = sh.done()
    return a * fl


def deepen_back(pic, d, label):
    fl = floor_mask(label)
    jm = joints(fl)
    pic[...] = pic * (1 - jm[..., None] * 0.34) + rgb("#3a3640") * jm[..., None] * 0.34 * 0.4
    sc = scuffs(fl)
    pic[...] = pic * (1 - sc[..., None] * 0.45)

    # The far wall and all that stands at it: a little cooler and paler with its distance (the floor and side walls graded).
    far = np.clip((d - 235.0) / (650.0 - 235.0), 0, 1)
    depth.air(pic, far, "#c3cdd2", amount=0.13, power=1.6)
    # The near floor deeper (and a touch warm, so the bottom of the picture sits).
    near = (1 - far) ** 1.6 * fl
    pic[...] = pic * (1 - near[..., None] * 0.20) + pic * rgb("#6a5a5e")[None, None, :] * near[..., None] * 0.20

    # The tubes' light falling off toward the corners (the pool is the room's middle, under the fittings).
    x, y = grid((H, W))
    uu, vv = (x - 415) / 430.0, (y - 330) / 330.0
    fall = np.clip((uu * uu + vv * vv - 0.38) / 1.3, 0, 1) ** 1.25 * 0.34
    pic[...] = pic * (1 - fall[..., None]) + pic * rgb("#48465e")[None, None, :] * fall[..., None]
    return np.clip(pic, 0, 1)


# ---------------------------------------------------------------- the front plane
def deepen_front(pic, a):
    """The near tables: deeper and a little warm, lit along their tops (the tubes are overhead)."""
    shade = rgb("#2a2030")
    out = lerp(pic, shade[None, None, :], 0.48)
    out[..., 0] += 0.035
    out[..., 1] += 0.008
    r = depth.rim(a, light=(-0.2, -1.0), width=1.6)
    thick = np.clip(blur(a, 3.0) * 2.2 - 0.9, 0, 1)                  # not along the chair's and the tables' thin legs
    r = np.clip(r * 1.3, 0, 1) * thick * 0.55
    out = out * (1 - r[..., None]) + rgb("#eadcb8")[None, None, :] * r[..., None]
    return np.clip(out, 0, 1)


def near_plane(wall):
    """One of the building's round columns, by the lens at the right edge (the room's camera: 50 cm across, its
    near side about 1.6 m from the lens, so a hand's breadth of it shows), running off the top, the right and the
    bottom. In shade: the tubes are beyond it and to the left, so only its side toward them is lit, a grazing light
    that falls off as the round turns toward us; a lit rim along that edge."""
    Z0 = 470.0
    lo, hi = V.cam_x, V.cam_x + 400.0
    for _ in range(40):                                  # the column's left side (its silhouette) at x 754
        mid = (lo + hi) / 2
        if V.pt(mid, 100.0, Z0)[0] < 754.0:
            lo = mid
        else:
            hi = mid
    xl = V.pt(lo, 100.0, Z0)[0]
    R = 25.0 * V.F / V.depth(lo + 25.0, Z0 + 25.0)        # its radius in the picture
    xc = xl + R
    x, y = grid((H, W))
    sh = Sheet((H, W), ss=3)
    sh.poly([(xl, -30), (W + 30, -30), (W + 30, H + 30), (xl, H + 30)], "#000000")
    _, a = sh.done()
    s_ = np.clip((x - xc) / R, -1, 1)                    # -1 at the silhouette toward the room, 0 square to us
    th = np.arcsin(s_)                                   # the round's angle there
    lam = np.clip(-np.sin(th), 0, 1) ** 3.0                  # a grazing light from the left, falling off as it turns to us
    base = depth.near_tone(wall, shade="#231e26", k=0.80, warm=0.05)
    litc = depth.near_tone(wall, shade="#231e26", k=0.30, warm=0.04)
    k = (lam * 0.95)[..., None] * (1.0 + 0.10 * (1 - y / H))[..., None]
    col = base[None, None, :] * (1 - k) + litc[None, None, :] * k
    n = noise((H, W), 9.0, seed=2301) * 0.5 + noise((H, W), 2.5, seed=2302) * 0.5
    col *= (1 + (n - 0.5) * 0.05)[..., None]
    # a scuffed band low on it (chairs, carts), the paint a touch darker; a seam where the column's casing meets
    low = np.clip((y - 470) / 70.0, 0, 1) * (0.6 + 0.4 * noise((H, W), 3.0, seed=2303))
    col *= (1 - low[..., None] * 0.15)
    r = depth.rim(a, light=(-1.0, -0.3), width=1.8)
    r = np.clip(r * 1.4, 0, 1) * 0.65
    col = col * (1 - r[..., None]) + rgb("#e6e0c6") * r[..., None]
    print("column: edge x", round(xl, 1), "radius px", round(R, 1))
    return np.clip(col, 0, 1), a


def near_tone_of(c, k, warm):
    return depth.near_tone(c, shade="#2a1f2c", k=k, warm=warm)


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(SRC):
        p = f"{SRC}/{f}"
        if os.path.isfile(p):
            shutil.copy2(p, f"{OUT}/{f}")
    d, label = surfaces()
    back, _ = load("back.png")
    wall = back[150:200, 480:530].reshape(-1, 3).mean(axis=0)                  # the back wall's own paint (by the coffee maker, above it)
    finish(deepen_back(back, d, label), f"{OUT}/back.png", 160)
    fr, fa = load("front.png")
    finish(deepen_front(fr, fa), f"{OUT}/front.png", 96, fa)
    col, na = near_plane(wall)
    finish(col, f"{OUT}/near.png", 48, na)
    # a look: the composite, nobody there
    im = Image.open(f"{OUT}/back.png").convert("RGBA")
    for n_ in ("vent", "door", "schedule", "pie", "vending", "chair", "front", "near"):
        im.alpha_composite(Image.open(f"{OUT}/{n_}.png").convert("RGBA"))
    im.convert("RGB").save(f"{OUT}-depth-comp.png")
    print("near share", round(float((na > 0.5).mean()), 4), "wall", np.round(wall, 3))


if __name__ == "__main__":
    main()

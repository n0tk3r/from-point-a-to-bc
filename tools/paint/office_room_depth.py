"""Interview Room C, the Comfortable Room (scene `office-room`): the depth pass (round twenty-three, wave two; DEPTH.md,
LITE.md). Works over the room as painted (out/office-room-orig/, the full run of office_room.py, unkeyed) and writes the
scene's full set back into out/office-room/, every file as before plus near.png.

    python3 office_room_depth.py [SRC [DST]]

ONE CAMERA: everything new is a place in the room (office_room_model.py, cm) seen through the scene's own room.View.

NEAR (near.png, the front plane): the room's near left corner, a column cased in the same painted block as the walls
(X 0..57, Z 428..480, floor to ceiling), up the left edge of the frame; and across the top the near light fixture, a
pendant strip hung under the ceiling grid (X 0..175, Z 486..522, its underside 30 cm under the tiles), switched off
(the Office's idea of comfort, like the lamp in the corner). Both in deep warm shade, lit only along the edges that
face the room's lit panels. The wastebasket and the box of questionnaires (front.png) are kept and made to count:
darker, warmer, their tops lit.

BACK (back.png): the tubes' light falling off toward the corners and the near floor (the four panels' light, worked
out on the room's surfaces), a soft shade on the near floor from the column and the room's near end, the carpet tiles'
joints and their laid-crosswise tone in perspective (60 cm, the model's grid), the floor dark along the foot of every
wall, the far walls a little cooler and paler. Nothing clicked moves; the cut-outs and the frames are copied as they
were.
"""

import os
import shutil
import sys

import numpy as np
from PIL import Image

import depth
import office_room_model as M
from brush import F32, Sheet, blur, rgb, lerp, mask_poly
from office_room_kit import finish
from room import View

W, H = 800, 600
V = View(**M.VIEW)
SRC = sys.argv[1] if len(sys.argv) > 1 else "out/office-room-orig"
DST = sys.argv[2] if len(sys.argv) > 2 else "out/office-room"
RW, RD, RH = M.W, M.D, M.H


def load(name):
    im = Image.open(os.path.join(SRC, name)).convert("RGBA")
    a = np.asarray(im, dtype=F32) / 255
    return a[..., :3].copy(), a[..., 3].copy()


# ---------------------------------------------------------------- the room's shell, ray by ray
def shell():
    """For every pixel: what of the room's box it sees (0 floor, 1 ceiling, 2 left wall, 3 right wall, 4 back wall),
    the place (X, Y, Z) and the distance along the ray, in cm."""
    y, x = np.mgrid[0:H, 0:W].astype(F32) + 0.5
    a = (x - V.cx) / V.F
    u = (V.hz - y) / V.F
    dX = a * V.rx + V.fx
    dZ = a * V.rz + V.fz
    dY = u
    X0, Y0, Z0 = V.cam_x, V.eye, V.cam_z
    big = np.full((H, W), 1e9, F32)
    t_all = []
    with np.errstate(divide="ignore", invalid="ignore"):
        t_all.append(np.where(dY < 0, (0 - Y0) / dY, big))              # floor
        t_all.append(np.where(dY > 0, (RH - Y0) / dY, big))             # ceiling
        t_all.append(np.where(dX < 0, (0 - X0) / dX, big))              # left wall
        t_all.append(np.where(dX > 0, (RW - X0) / dX, big))             # right wall
        t_all.append(np.where(dZ < 0, (0 - Z0) / dZ, big))              # back wall
    T = np.stack(t_all)
    T[~np.isfinite(T) | (T <= 0)] = 1e9
    surf = T.argmin(axis=0)
    t = T.min(axis=0)
    PX, PY, PZ = X0 + dX * t, Y0 + dY * t, Z0 + dZ * t
    dist = t * np.sqrt(dX * dX + dY * dY + dZ * dZ)
    return surf, PX.astype(F32), PY.astype(F32), PZ.astype(F32), dist.astype(F32)


_E = {}


def panel_light(surf, PX, PY, PZ):
    if "E" not in _E:
        _E["E"] = _panel_light(surf, PX, PY, PZ)
    return _E["E"]


def _panel_light(surf, PX, PY, PZ):
    """How much of the four panels' light reaches each place of the shell (1 the brightest): the tubes falling off
    toward the corners and the near floor."""
    nrm = {0: (0, 1, 0), 1: (0, -1, 0), 2: (1, 0, 0), 3: (-1, 0, 0), 4: (0, 0, 1)}
    E = np.zeros((H, W), F32)
    for x0, x1, z0, z1 in M.TROFFERS:
        for fx in (0.25, 0.75):
            for fz in (0.25, 0.75):
                LX, LY, LZ = x0 + (x1 - x0) * fx, RH - 2.0, z0 + (z1 - z0) * fz
                vx, vy, vz = LX - PX, LY - PY, LZ - PZ
                r2 = vx * vx + vy * vy + vz * vz + 900.0
                r = np.sqrt(r2)
                cos_l = np.clip(-vy / r * -1, 0, 1)                        # the panel faces down
                cos_l = np.clip(vy / r, 0, 1)
                cos_s = np.zeros_like(E)
                for k, (nx, ny, nz) in nrm.items():
                    m = surf == k
                    cos_s[m] = np.clip((vx[m] * nx + vy[m] * ny + vz[m] * nz) / r[m], 0, 1)
                E += cos_l * cos_s / r2
    E = blur(E, 3.0)
    ref = np.percentile(E[surf == 0], 97)
    return np.clip(E / ref, 0, 1.4)


def poly_mask(pts, soft=0.8):
    return mask_poly((H, W), pts, soft=soft)


def hot_mask():
    """Where something clicked or standing is painted into the backdrop (the scene file's areas, the chairs' feet, the
    lamp's foot): no new texture is laid there."""
    m = np.zeros((H, W), F32)
    polys = [
        [[541, 351], [553, 318], [557, 315], [569, 314], [578, 318], [590, 353], [589, 445], [568, 449], [564, 449], [543, 441]],
        [[619, 316], [627, 309], [646, 303], [663, 306], [676, 313], [684, 324], [677, 447], [671, 480], [646, 482], [632, 475], [619, 470]],
        [[414, 415], [415, 401], [448, 356], [452, 356], [466, 359], [468, 362], [464, 434], [432, 439], [431, 439], [414, 430]],
        [[442, 402], [478, 363], [483, 363], [489, 364], [502, 367], [502, 375], [497, 450], [464, 456], [463, 456], [442, 440]],
        [[313, 369], [316, 369], [326, 374], [371, 411], [371, 458], [331, 464], [330, 464], [318, 452], [313, 372]],
        [[346, 370], [370, 368], [382, 368], [423, 370], [461, 381], [466, 384], [466, 388], [461, 458], [460, 459], [397, 469], [345, 440]],
        [[70, 370], [96, 368], [112, 368], [117, 372], [118, 375], [122, 412], [122, 460], [121, 461], [72, 469], [71, 469]],
        [[315, 450], [358, 445], [374, 457], [328, 464]], [[412, 429], [446, 424], [466, 434], [431, 439]],
        [[439, 443], [476, 438], [501, 450], [462, 456]],
        [[462, 260], [500, 260], [500, 418], [462, 418]],                 # the floor lamp in the far corner
        [[530, 300], [600, 300], [600, 460], [530, 460]],                 # the cooler with its feet
    ]
    for p in polys:
        m = np.maximum(m, poly_mask(p, 1.0))
    return np.clip(blur(m, 2.0) * 1.6, 0, 1)


# ---------------------------------------------------------------- the back
def deepen(back, surf, PX, PY, PZ, dist, keep, tex=True):
    pic = back.copy()
    floor = (surf == 0).astype(F32)
    walls = ((surf >= 2)).astype(F32)
    ceil = (surf == 1).astype(F32)

    # the panels' light falling off toward the corners and the near floor (laid as a glaze over the light already there)
    E = panel_light(surf, PX, PY, PZ)
    fall = np.clip(0.80 + 0.22 * E, 0.74, 1.04)
    warm = rgb("#5a4436")
    k = np.clip((1.0 - fall) * 1.0, 0, 0.3)
    pic = pic * fall[..., None] * (1 - k[..., None] * 0.25) + pic * warm * 1.6 * k[..., None] * 0.25

    # the floor dark along the foot of every wall, the ceiling along its top
    dwall = np.minimum(np.minimum(PX, RW - PX), PZ)
    ao = 1.0 - 0.16 * np.exp(-np.clip(dwall, 0, None) / 14.0) * floor
    ao *= 1.0 - 0.10 * np.exp(-np.clip(RH - PY, 0, None) / 10.0) * walls
    ao *= 1.0 - 0.10 * np.exp(-np.clip(np.minimum(np.minimum(PX, RW - PX), PZ), 0, None) / 12.0) * ceil
    pic *= blur(ao.astype(F32), 1.0)[..., None]

    # the carpet tiles: laid crosswise, one a little lighter than the next, and the joints between them, in perspective
    gx, gz = M.GRID
    ix = np.floor((PX - M.GRID_X0) / gx)
    iz = np.floor((PZ - M.GRID_Z0) / gz)
    par = ((ix + iz) % 2 == 0).astype(F32) * 2 - 1
    near_w = np.clip((900 - dist) / 600, 0.25, 1.0)
    tile_m = floor * (1 - keep)
    if tex:
        pic *= (1 + 0.022 * par * near_w * tile_m)[..., None]
    if tex:
        sh = Sheet((H, W), ss=3)
        joint = "#2c2a30"
        for k in range(-1, 12):
            X = M.GRID_X0 + gx * k
            if 0 < X < RW:
                pts = [V.pt(X, 0, Z) for Z in np.linspace(2, 600, 60) if V.depth(X, Z) > 40]
                for p, q in zip(pts, pts[1:]):
                    d = V.depth(X, 300)
                    sh.line([p, q], joint, width=1.2, alpha=0.9)
            Z = M.GRID_Z0 + gz * k
            if 0 < Z < 600:
                pts = [V.pt(X2, 0, Z) for X2 in np.linspace(2, RW - 2, 60) if V.depth(X2, Z) > 40]
                for p, q in zip(pts, pts[1:]):
                    sh.line([p, q], joint, width=1.2, alpha=0.9)
        jc, ja = sh.done()
        ja = ja * floor * (1 - keep) * (0.10 + 0.10 * near_w) * (1.0 if tex else 0.0)
        pic = pic * (1 - ja[..., None]) + pic * jc * 2.2 * ja[..., None]

    # a soft shade on the near floor: the column at the left and the room's near end between us and the panels; its
    # edge runs in from the lower left toward the table (thin where people stand)
    s = (PZ - (440.0 + 0.30 * (PX - 60.0))) / 40.0
    rng = np.random.default_rng(23)
    wob = blur(rng.normal(0, 1, (H, W)).astype(F32), 6.0) * 6.0
    sh_m = np.clip(s + wob * 0.15, 0, 1) ** 1.2 * floor
    sh_m = blur(sh_m.astype(F32), 2.5)
    walked = poly_mask([[133, 451], [456, 413], [472, 419], [500, 416], [553, 435], [528, 439], [565, 453], [590, 448], [631, 463],
                        [603, 471], [595, 479], [80, 479], [84, 470], [130, 464]], 2.0)
    amt = 0.30 * (1 - 0.55 * walked)
    shade = rgb("#463a40")
    m = sh_m * amt
    pic = pic * (1 - m[..., None]) + pic * shade * 1.5 * m[..., None]

    # air: the far walls and the far ceiling a little cooler and paler (toward the tubes' pale green-grey)
    far = np.clip((dist - 330.0) / 420.0, 0, 1)
    far = far * (walls + ceil * 0.7)
    sky = rgb("#c3cdca")
    depth.air(pic, far, sky, amount=0.16, power=1.0)
    # and the near floor deeper and warmer
    nf = np.clip((420.0 - dist) / 200.0, 0, 1) * floor
    pic = pic * (1 - 0.12 * nf[..., None]) + pic * rgb("#6a5040") * 1.4 * (0.12 * nf[..., None])

    # the frame's corners a little deeper (warm, as the room's own light says)
    depth.frame(pic, amount=0.14, bottom=0.10, color="#3a2c28")
    return np.clip(pic, 0, 1)


# ---------------------------------------------------------------- the near plane
def face(pts3):
    return [V.pt(*p) for p in pts3]


def near_plane(back):
    """-> (colour, alpha): the near column up the left edge and the pendant strip across the top."""
    wall = np.median(back[300:420, 4:30].reshape(-1, 3), axis=0)              # the left wall's painted block, as painted
    tile = np.median(back[20:60, 330:420].reshape(-1, 3), axis=0)             # the ceiling's tiles
    shade = "#2a1e1c"
    col_side = depth.near_tone(wall, shade=shade, k=0.76, warm=0.04)          # the face toward the room
    col_front = depth.near_tone(wall, shade=shade, k=0.86, warm=0.03)         # the face toward us
    col_joint = depth.near_tone(wall, shade=shade, k=0.90, warm=0.03)
    hous = depth.near_tone(tile, shade="#221d1e", k=0.86, warm=0.035)              # the fixture's enamel housing, in shade
    lens = depth.near_tone(tile, shade="#2a2830", k=0.68, warm=0.02)          # its lens, unlit
    rib = depth.near_tone(tile, shade=shade, k=0.88, warm=0.03)

    sh = Sheet((H, W), ss=3)
    # the column: X 0..CX, Z CZ0..CZ1, floor to ceiling
    CX, CZ0, CZ1 = 58.0, 423.0, 482.0
    Y0, Y1 = -40.0, RH + 40.0
    side = face([(CX, Y0, CZ0), (CX, Y1, CZ0), (CX, Y1, CZ1), (CX, Y0, CZ1)])
    front = face([(CX, Y0, CZ1), (CX, Y1, CZ1), (-200.0, Y1, CZ1), (-200.0, Y0, CZ1)])
    sh.poly(front, col_front)
    sh.poly(side, col_side)
    # its block: 20 cm courses, joints staggered every 40 cm (on the side face, and across the face toward us)
    for c in range(0, 14):
        Yc = 20.0 * c
        sh.line([V.pt(CX, Yc, CZ0), V.pt(CX, Yc, CZ1)], col_joint, width=1.1, alpha=0.8)
        Zj = CZ0 + (20.0 if c % 2 else 40.0)
        if CZ0 < Zj < CZ1:
            sh.line([V.pt(CX, Yc, Zj), V.pt(CX, Yc + 20.0, Zj)], col_joint, width=1.1, alpha=0.8)
    # the corner's arris, worn
    sh.line([V.pt(CX, Y0, CZ1), V.pt(CX, Y1, CZ1)], col_joint, width=1.4, alpha=0.6)

    # the pendant strip: X 0..FX1, Z FZ0..FZ1, its underside FY0, its top FY1; hung on two rods
    FX1, FZ0, FZ1, FY0, FY1 = 168.0, 493.0, 521.0, 232.0, 246.0
    under = face([(0.0, FY0, FZ0), (FX1, FY0, FZ0), (FX1, FY0, FZ1), (0.0, FY0, FZ1)])
    nearf = face([(0.0, FY0, FZ1), (FX1, FY0, FZ1), (FX1, FY1, FZ1), (0.0, FY1, FZ1)])
    endf = face([(FX1, FY0, FZ0), (FX1, FY1, FZ0), (FX1, FY1, FZ1), (FX1, FY0, FZ1)])
    for X in (30.0, 150.0):
        sh.line([V.pt(X, FY1, (FZ0 + FZ1) / 2), V.pt(X, RH, (FZ0 + FZ1) / 2)], hous, width=1.6)
    sh.poly(endf, hous)
    sh.poly(nearf, hous)
    sh.poly(under, hous)
    # the lens set into the underside (2 cm in from its rim) and its prisms' ribs along it
    lens_p = face([(4.0, FY0, FZ0 + 3), (FX1 - 3, FY0, FZ0 + 3), (FX1 - 3, FY0, FZ1 - 3), (4.0, FY0, FZ1 - 3)])
    sh.poly(lens_p, lens)
    for f in np.linspace(0.18, 0.82, 6):
        Z = FZ0 + 3 + (FZ1 - FZ0 - 6) * f
        sh.line([V.pt(4.0, FY0, Z), V.pt(FX1 - 3, FY0, Z)], rib, width=0.9, alpha=0.7)
    # the tube's end caps showing through, dark
    sh.line([V.pt(FX1 - 3, FY0, FZ0 + 3), V.pt(FX1 - 3, FY0, FZ1 - 3)], rib, width=1.4)
    colr, alpha = sh.done()

    # rims: the column's side toward the lit room (right), the fixture's far underside edge toward the panels (up)
    rim_col = depth.rim(alpha, light=(1.0, -0.25), width=2.2)
    rim_fix = depth.rim(alpha, light=(0.15, -1.0), width=2.0)
    xs = np.arange(W)[None, :].repeat(H, 0)
    ys = np.arange(H)[:, None].repeat(W, 1)
    in_col = (xs < 120).astype(F32)
    lit = rgb("#e8d9b8")
    r = np.clip(rim_col * in_col * 0.55 + rim_fix * (1 - in_col) * 0.45, 0, 0.6)
    colr = colr * (1 - r[..., None]) + lit * r[..., None]
    # a little bounce from the floor low on the column, and its top deeper under the ceiling
    up = np.clip((ys - 300) / 300.0, 0, 1) * in_col
    colr = colr * (1 + 0.10 * up[..., None])
    top = np.clip((120 - ys) / 120.0, 0, 1) * in_col
    colr = colr * (1 - 0.15 * top[..., None])
    # painted, not ruled: a little brush in the tone
    rng = np.random.default_rng(1830)
    n = blur(rng.normal(0, 1, (H, W)).astype(F32), 1.4) * 0.035
    colr = np.clip(colr * (1 + n[..., None]), 0, 1)
    return colr, alpha


def front_deeper(colr, alpha):
    """The wastebasket and the box near us: darker and warmer, their tops lit by the tubes."""
    c = colr.copy()
    sh = rgb("#2a1e1c")
    c = lerp(colr, sh, 0.34)
    c[..., 0] = np.clip(c[..., 0] + 0.025, 0, 1)
    rr = depth.rim(alpha, light=(0.2, -1.0), width=2.0)
    c = c * (1 - rr[..., None] * 0.35) + colr * 1.05 * rr[..., None] * 0.35
    return np.clip(c, 0, 1)


CUTS = {"vent": 40, "vent-eyes": 48, "thermostat-72": 32, "thermostat-77": 48, "thermostat-81": 48, "intercom": 32,
        "intercom-lit": 48, "door": 48, "door-open": 48, "doorframe": 64, "chair-corner": 48, "table": 64,
        "questionnaire": 24, "plant": 56, "plant-droop": 48}


def main():
    os.makedirs(DST, exist_ok=True)
    back, _ = load("back.png")
    surf, PX, PY, PZ, dist = shell()
    keep = hot_mask()
    deep = deepen(back, surf, PX, PY, PZ, dist, keep)
    finish(deep, f"{DST}/back.png", 160, amount=0.006, speckle=0.006)

    ncol, na = near_plane(back)
    finish(ncol, f"{DST}/near.png", 48, na, amount=0.008)
    print("near share", round(float((na > 0.5).mean()) * 100, 1), "%")

    # the smooth grade (everything but the carpet's texture) is affine in colour at every pixel: out = c * A + B
    B = deepen(np.zeros((H, W, 3), F32), surf, PX, PY, PZ, dist, keep, tex=False)
    A = (deepen(np.full((H, W, 3), 0.5, F32), surf, PX, PY, PZ, dist, keep, tex=False) - B) / 0.5
    fcol, fa = load("front.png")
    finish(front_deeper(fcol, fa), f"{DST}/front.png", 48, fa, amount=0.006)

    # the cut-outs that lie in the room: the same smooth grade as the backdrop round them (no carpet texture), inside
    # their own outlines; their palettes as the scene's finish gives them. The frames (the second hand, the bubble) and
    # everything else are copied as they were.
    for f in sorted(os.listdir(SRC)):
        if f in ("back.png", "front.png", "near.png"):
            continue
        s = os.path.join(SRC, f)
        if not os.path.isfile(s):
            continue
        name = f[:-4]
        if f.endswith(".png") and name in CUTS:
            c, a = load(f)
            g = np.clip(c * A + B, 0, 1)
            finish(g, os.path.join(DST, f), CUTS[name], a, amount=0.004, speckle=0.004)
        else:
            shutil.copy2(s, os.path.join(DST, f))
    # a quick look at the whole: backdrop, cut-outs in the scene's order, then the front plane
    comp = Image.open(f"{DST}/back.png").convert("RGBA")
    for n in ("vent", "thermostat-72", "intercom", "door", "doorframe", "chair-corner", "table", "questionnaire", "plant", "front", "near"):
        p = f"{DST}/{n}.png"
        if os.path.exists(p):
            comp.alpha_composite(Image.open(p).convert("RGBA"))
    comp.convert("RGB").save(os.environ.get("COMP", "out/office-room-depth-comp.png"))


if __name__ == "__main__":
    main()

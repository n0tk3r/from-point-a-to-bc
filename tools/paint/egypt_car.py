"""Inside the wagon (egypt-car), nose-down in the sand by the Nile, one afternoon: what Dad sees from the driver's seat.

    python3 egypt_car.py            everything: backdrop, cut-outs and their states, layout.json, the comps
    python3 egypt_car.py plan       the skeleton: the car's shapes through the camera, flat-lit, with the design's places
                                    and the brief's fixed numbers drawn over it (out/egypt-car-work/plan.png)
    python3 egypt_car.py fast       the under-painting only: one ray per pixel, hard shadows (out/egypt-car-work/fast.png)
    python3 egypt_car.py paint      the same with the brush pass and the details over it (out/egypt-car-work/paint.png)
    python3 egypt_car.py layout     layout.json again from the masks the last full run kept (no painting)

ONE CAMERA. The car is measured in centimetres (egypt_car_model.py) and every pixel of the picture is a ray from Dad's
eye: room.View, square to the car (the dashboard runs level), its vanishing point toward the wheel. What the ray meets,
and how the light falls there, is worked out in the car (egypt_car_kit.py, egypt_car_things.py); rays that leave the car
by its glass or its open window are the world outside (egypt_car_world.py). Dad himself is not in the picture: nobody is.

THE LIGHT: the afternoon (the river picture's sun, low on the left of it, beyond the scene: ahead of the car, a little to
its right, 26 degrees up; the car's own pitch lifts it to 33 in the car's frame). Keep to it:
  - no sun in the picture: it is above the windshield's top right corner, behind the passenger's visor and the roof's
    edge; its glare is at the glass's top right corner;
  - the dash top takes the sun through the glass: hard, bleached highlights, the brightest thing inside the car, with
    the shadow of the right-hand pillar across its end; a shaft comes in over the passenger side of the dash and lies
    across the Son's cushion; the Son's window, at the right edge, is the brightest pane;
  - Dad's open window, at the left, is on the car's shade side: sand glowing warm in the car's shadow, not sun;
  - everything that faces Dad (the dials, the radio, the glovebox's door, the wheel's spokes) is in warm half shade,
    lit by the light thrown back from the sand and the sunlit dash: warm, mid-toned, easy to read; the glovebox's door
    above all reads at a glance;
  - the headliner and the visors' undersides glow warm with the light the sunlit dash throws up; the footwells and
    under the dash are deep warm brown: the darkest things in the picture.

THREE TONES. Dark: the footwells, under the dash, the wheel's rim, the column. Middle: the dash's face, the doors, the
headliner, the seat. Light: the dash top in the sun, the world through the glass (the sky, the river's glitter), the
Son's window.

CUT-OUTS (pixel-aligned, the backdrop complete under each): glovebox-shut, glovebox-map, glovebox-empty (the door, and
the map: the backdrop shows the compartment open with only the ketchup packets in it); visor-up, visor-down (the backdrop
has no driver's visor); freshener (the little cardboard wagon on its string, on the front plane: the game sways it).
Nothing that moves by nature is painted: the steam over the hood and the dust in the sun are the game's (layout.json
"fx")."""

import json
import math
import os
import sys
import time

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, blur, lerp, noise, sample, strokes, grain, to_palette, save, rgb, palette_of
from room import View
import egypt_car_model as M
import egypt_car_things as T
import egypt_car_world as WD
from egypt_car_kit import Stage, Lamp, shade, col, LUM

W, H = 800, 600
V = View(**M.VIEW)
OUT = "out/egypt-car"
WORK = "out/egypt-car-work"
SEED = 13
EXPOSE = 0.95


# ---------------------------------------------------------------- the light
def sun_dir():
    """The way to the sun in the car's own frame (X right, Y up, Z toward Dad): the world's direction turned through
    the car's pitch."""
    a, e, p = math.radians(WD.SUN["az"]), math.radians(WD.SUN["el"]), math.radians(M.PITCH)
    right, up, fwd = math.sin(a) * math.cos(e), math.sin(e), math.cos(a) * math.cos(e)
    cu = up * math.cos(p) + fwd * math.sin(p)
    cf = fwd * math.cos(p) - up * math.sin(p)
    return (right, cu, -cf)


def lamps(fast=False):
    """The low sun (a lamp very far off: its shadows are the car's own shell, so it comes in through the glass only);
    the sky ahead and above and the sunlit sand ahead, seen through the glass (broad, soft); the glow the sunlit dash
    throws up at the headliner and the visors; the sand outside Dad's window, in the car's shadow; and the light from
    behind him (the rear windows, the cabin's own tan). The last two are fills: they throw no shadows (a broad light from
    behind the seats, shadowed by the roof, would darken everything just under it)."""
    n = 1 if fast else 3
    eye = (V.cam_x, V.eye, V.cam_z)
    s = sun_dir()
    return [
        Lamp(tuple(eye[i] + 1.0e5 * s[i] for i in range(3)), "#ffe6bc", 1.30, reach=1.0e6, size=900.0, samples=n, wrap=0.02),
        Lamp((82.0, 300.0, -300.0), "#a8c6ee", 0.30, reach=900.0, size=180.0, samples=n, wrap=0.3),
        Lamp((82.0, 40.0, -420.0), "#f0c690", 0.42, reach=1200.0, size=260.0, samples=n, wrap=0.3),
        Lamp((82.0, 89.0, 6.0), "#ffd29a", 0.62, reach=120.0, aim=(0.0, 1.0, 0.5), spread=math.cos(math.radians(84)), soft=0.4, back=0.15,
             size=40.0, shadows=False, wrap=0.6),
        Lamp((-160.0, 95.0, 70.0), "#e6c29a", 0.22, reach=360.0, size=110.0, shadows=False, wrap=0.3),
        Lamp((82.0, 108.0, 280.0), "#ecd8c0", 0.46, reach=520.0, size=60.0, shadows=False, wrap=0.45),
    ]


def ambient(X, Y, Z, N):
    """The light that is simply in a tan car standing in the sun: warm, from everywhere, less down low in the footwells
    and under the dash."""
    up = 0.5 + 0.5 * N[..., 1]
    low = np.clip((Y - 8.0) / 70.0, 0, 1)
    fwd = np.clip((Z + 10.0) / 40.0, 0, 1)                                 # deep under the dash, toward the firewall, less
    return col("#8a6842")[None, None, :] * ((0.16 + 0.07 * up) * (0.40 + 0.60 * low) * (0.6 + 0.4 * fwd))[..., None]


# ---------------------------------------------------------------- putting the car together
def render(ss=1, fast=True, skip=(), rect=None, occ=None, **state):
    """-> (picture, stage, escaped): the picture at picture size (rays averaged), and how much of each pixel's rays left
    the car (the world shows there)."""
    st = Stage(V, ss=ss, rect=rect)
    st.skip = set(skip)
    T.build(st, **state)
    pic, light = shade(st, lamps(fast), ambient, fast=fast, occ=occ, expose=EXPOSE)
    lum = light @ LUM
    deep = np.clip(1 - lum / 0.42, 0, 1) ** 1.4                         # the deepest shade goes warm brown toward violet, never grey
    pic = pic * (1 + deep[..., None] * np.array([0.04, -0.05, 0.03], dtype=F32)[None, None, :])
    out = st.t >= 9e8
    return st.down(pic), st, st.down(out.astype(F32))


_Y, _X = np.mgrid[0:H, 0:W].astype(F32)


def openings():
    """Which way each pixel's ray leaves the car, if it does: through the windshield (1), the Son's window (2, glass) or
    Dad's open window (3). Worked out from the ray: where it crosses the windshield's plane, and whether that is inside
    the glass (between the pillars, which lean in toward the roof); a ray that passes left of Dad's pillar goes out by
    his window (the old wagon's thin pillars: what is beside them is the side window's), one right of the other pillar
    by the Son's."""
    dX = (_X + 0.5 - V.cx) / V.F
    dY = (V.hz - (_Y + 0.5)) / V.F
    g = M.GLASS
    k = (g["z1"] - g["z0"]) / (g["y1"] - g["y0"])                          # the glass's plane: Z = z0 + k (Y - y0)
    t = (V.cam_z - g["z0"] - k * (V.eye - g["y0"])) / (1.0 + k * dY)       # (along the ray, Z = cam_z - t)
    xs, ys = V.cam_x + dX * t, V.eye + dY * t
    f = np.clip((ys - g["y0"]) / (g["y1"] - g["y0"]), 0, 1)
    left, right = f * M.TUMBLE, M.W - f * M.TUMBLE
    out = np.zeros((H, W), np.uint8)
    out[xs < left] = 3
    out[xs > right] = 2
    out[(xs >= left) & (xs <= right)] = 1
    return out


def compose(pic, st, escaped, world):
    """The world laid where the rays leave the car: through the windshield a little dimmed and cooled by the old glass,
    with the faint pale ghost of the sunlit dash top in its lower part; through the Son's window, the glass and the sun's
    glare on it; through Dad's open window, nothing between. Then the sand the nose ploughed up, lying over the hood's
    front, its edge in the sun."""
    way = openings()
    w = world.copy()
    glass = way == 1
    w[glass] = w[glass] * np.array([0.93, 0.95, 0.97], dtype=F32)
    ghost = np.clip((300 - _Y) / 4.0, 0, 1) * np.clip(1 - (300 - _Y) / 46.0, 0, 1) * glass
    ghost = ghost * (0.65 + 0.35 * noise((H, W), (60, 8), SEED + 1, 3))
    w = w + (col("#fff0d8") - w) * (ghost * 0.16)[..., None]
    side = way == 2
    w[side] = w[side] * 0.96 + col("#fff8ea") * 0.06
    out = pic + w * escaped[..., None]
    # the sand on the hood's front: where the hood runs under the mound, with a thin lip of it in the sun over the paint
    X, Y, Z = st.places()
    hood = st.mask_of("hood")
    Xd, Zd = st.pick(X), st.pick(Z)
    cov = st.down(hood.astype(F32))
    hood_p = cov > 0.5
    edge = -112.0 - 34.0 * noise((H, W), (90, 30), SEED + 2, 3) + 18.0 * np.clip((Xd - 70.0) / 90.0, -1, 1)
    under = hood_p & (Zd < edge)
    near = under.copy()                                                    # the hood's own edge where it runs under (pixels it only partly
    for _ in range(2):                                                     # covers): the sand there too, so no outline of it shows in the mound
        near = near | np.roll(near, 1, 0) | np.roll(near, -1, 0) | np.roll(near, 1, 1) | np.roll(near, -1, 1)
    under = under | ((cov > 0.01) & ~hood_p & near)
    lip = hood_p & (Zd >= edge) & (Zd < edge + 14.0 + 10.0 * noise((H, W), (25, 6), SEED + 3, 2))
    sand_lit = col("#ecc48a") * (0.92 + 0.12 * noise((H, W), (30, 6), SEED + 4, 3))[..., None]
    out[lip] = lerp(out[lip], sand_lit[lip], 0.82)
    out[under] = world[under]
    return np.clip(out, 0, 1), dict(way=way, under=under, lip=lip, hood=hood_p)


def grade(pic, rect=None):
    """The whole picture's last adjustments: the bottom (the footwells, the near corners) deeper and warmer, to hold the
    eye up on the dash and the glovebox; the top corners a little deeper too. (With `rect`, for a patch of it.)"""
    x0, y0, x1, y1 = rect or (0, 0, W, H)
    y, x = _Y[y0:y1, x0:x1], _X[y0:y1, x0:x1]
    low = np.clip((y - 470) / 130, 0, 1) ** 1.4
    side = np.clip(np.abs(x - 430) / 430, 0, 1) ** 2
    top = np.clip((60 - y) / 60, 0, 1) * side
    v = np.clip(low * 0.22 + side * 0.10 * low + top * 0.12, 0, 0.5)
    warm = col("#4a2c1e")
    out = pic * (1 - v[..., None]) + pic * warm[None, None, :] * 1.6 * v[..., None]
    grey = (out @ LUM)[..., None]
    return np.clip(grey + (out - grey) * 1.06, 0, 1)


def paint(crisp, seed=2):
    """The brush pass, and then the built things said again crisply over it: where the under-painting has an edge or a
    small thing, most of it comes back; where it is only a broad tone, the brushwork stays."""
    b = strokes(crisp, sizes=(9, 5, 2), seed=seed, density=1.5, jitter=0.035, keep=0.32)
    hf = np.abs(crisp - blur(crisp, 1.4)).sum(axis=2)
    w = np.clip(hf * 7.5 - 0.05, 0, 1)
    w = np.maximum(w, blur(w, 0.7))
    out = lerp(b, crisp, (0.16 + 0.82 * w)[..., None])
    return np.clip(out + 0.40 * (out - blur(out, 0.9)), 0, 1)


_DX = (noise((H, W), 30, SEED + 3, 3) - 0.5) * 2 * 0.6
_DY = (noise((H, W), 30, SEED + 4, 3) - 0.5) * 2 * 0.6


def wob(a, rect=None):
    """Nothing a hand rules is perfectly straight: every picture and mask is pushed about by the same slow field, under a
    pixel, so all the cut-outs still fit one another exactly. (With `rect`, for a patch of the picture.)"""
    if rect is None:
        return sample(a, _X + _DX, _Y + _DY)
    x0, y0, x1, y1 = rect
    return sample(a, _X[y0:y1, x0:x1] - x0 + _DX[y0:y1, x0:x1], _Y[y0:y1, x0:x1] - y0 + _DY[y0:y1, x0:x1])


def crisp_edges(pic, st, rect=None, far=None):
    """Small crisp accents found from what each pixel shows: a dark line where one thing stands in front of another
    far behind it (the wheel's rim against the dash, the dash's lip against the footwell), so the built things keep
    their edges under the brush. `far`: pixels that show the world though a ray met something there (the hood's front,
    under the sand: no edge of it is drawn in the mound)."""
    t = st.pick(np.minimum(st.t, 5000.0))
    if far is not None:
        t = np.where(far, 5000.0, t).astype(F32)
    t = wob(t, rect)
    out = pic.copy()
    for ax, sh_ in ((0, 1), (0, -1), (1, 1), (1, -1)):
        tn = np.roll(t, sh_, axis=ax)
        behind = (t - tn > 12.0) & (t - tn > 0.08 * t)
        if ax == 0:
            behind[0 if sh_ == 1 else -1] = False
        else:
            behind[:, 0 if sh_ == 1 else -1] = False
        out[behind] = out[behind] * 0.8
    return out


def to_image(a):
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))


def tones(a, label=""):
    lum = (np.clip(a, 0, 1) * 255) @ LUM
    print(label, "lum 5/25/50/75/95:", np.percentile(lum, [5, 25, 50, 75, 95]).round(0))


def whole(fast=True, ss=1, details=False, **state):
    """The picture in one state, painted (for looking)."""
    pic, st, esc = render(ss=ss, fast=fast, **state)
    world, info = WD.world()
    WD.papyrus(world)
    out, cinfo = compose(pic, st, esc, world)
    out = grade(out)
    return out, st, info, cinfo


# ---------------------------------------------------------------- the skeleton
DESIGN = {"visor up": (88, 14, 328, 58), "visor down": (88, 52, 328, 170), "visor P": (472, 14, 730, 58), "rearview": (346, 54, 454, 94),
          "freshener": (392, 96, 414, 142), "dash top": (0, 296, 800, 326), "gauges": (118, 330, 342, 402), "center": (346, 326, 470, 460),
          "radio": (354, 356, 464, 400), "cupholder": (466, 334, 512, 408), "glovebox": (546, 364, 736, 446), "horn": (188, 444, 284, 506),
          "gears": (300, 418, 420, 446), "key": (334, 500, 366, 528), "door": (0, 58, 70, 600), "manual": (8, 492, 58, 560),
          "cushion": (470, 470, 800, 600), "seat back": (690, 300, 800, 600), "bench middle": (380, 500, 470, 600), "P window": (780, 58, 800, 300)}
GLASS_DESIGN = [(86, 58), (722, 58), (774, 298), (36, 298)]


def overlay(base, name):
    im = to_image(base).convert("RGBA")
    dr = ImageDraw.Draw(im, "RGBA")
    for nm, (x0, y0, x1, y1) in DESIGN.items():
        dr.rectangle([x0, y0, x1, y1], outline=(255, 0, 255, 200))
        dr.text((x0 + 2, y0 + 1), nm, fill=(255, 0, 255, 255))
    dr.line(GLASS_DESIGN + GLASS_DESIGN[:1], fill=(255, 0, 255, 160), width=1)
    dr.rectangle([200, 70, 600, 150], outline=(255, 255, 0, 255))
    dr.text((204, 72), "words", fill=(255, 255, 0, 255))
    dr.line([(0, M.BAND_TOP), (800, M.BAND_TOP)], fill=(0, 255, 0, 255))
    dr.line([tuple(p) for p in M.WALK] + [tuple(M.WALK[0])], fill=(0, 255, 255, 255))
    dr.line([(0, WD.HZ), (800, WD.HZ)], fill=(0, 255, 255, 120))
    dr.line([(0, M.VIEW["horizon"]), (800, M.VIEW["horizon"])], fill=(255, 128, 0, 120))
    im.convert("RGB").save(f"{WORK}/{name}")


def plan():
    st = Stage(V, ss=1)
    T.build(st)
    lamps_ = [Lamp((400.0, 400.0, -400.0), "#fff4e0", 0.7, reach=2000.0, shadows=False, wrap=0.3),
              Lamp((40.0, 60.0, 220.0), "#ffe8c8", 0.35, reach=400.0, shadows=False, wrap=0.4)]
    pic, light = shade(st, lamps_, lambda X, Y, Z, N: np.full(X.shape + (3,), 0.18, dtype=F32), fast=True)
    pic[st.t >= 9e8] = col("#9ec8e8")
    overlay(pic, "plan.png")


def finish(picture, name, colors=128, alpha=None, seed=7, speckle=0.008, amount=0.012):
    """Grain, then a palette of the picture's own with a little speckle, as a scanned painting has: an 8-bit PNG."""
    g = grain(picture, seed, amount)
    sample_of = g if alpha is None else g[alpha > 0.5]
    pal = palette_of([sample_of.reshape(-1, 3)], colors=min(colors, max(8, len(np.unique((sample_of.reshape(-1, 3) * 255).astype(np.uint8), axis=0)))))
    idx = to_palette(g, pal, speckle=speckle)
    save(name, idx, pal, alpha)
    return os.path.getsize(name)


def patch(rect, back_composed, **state):
    """One cut-out's state, rendered and painted on its own patch of the picture (the world shows where its rays leave
    the car, as in the backdrop). -> (painted patch at full size, stage)."""
    x0, y0, x1, y1 = rect
    pic, st, esc = render(ss=SS, fast=False, rect=rect, occ=OCC_B, **state)
    whole_ = back_composed[y0:y1, x0:x1] * esc[..., None] + pic
    painted = crisp_edges(paint(grade(wob(whole_, rect), rect), seed=5), st, rect)
    out = np.zeros((H, W, 3), F32)
    out[y0:y1, x0:x1] = painted
    return out, st


def cover(st, grp, rect=None):
    """The pixels a group of things covers (a cut-out's shape), pushed by the hand-wobble like the paint."""
    m = st.down((st.grp == st.groups.get(grp, -99)).astype(F32))
    if rect is None:
        return wob(m) > 0.5
    x0, y0, x1, y1 = rect
    out = np.zeros((H, W), bool)
    out[y0:y1, x0:x1] = wob(m, rect) > 0.5
    return out


def named(st, *names, rect=None):
    """The pixels where the rays met things of these names."""
    m = st.down(st.mask_of(*names).astype(F32))
    if rect is None:
        return wob(m) > 0.5
    x0, y0, x1, y1 = rect
    out = np.zeros((H, W), bool)
    out[y0:y1, x0:x1] = wob(m, rect) > 0.5
    return out


SS = 2
OCC_B = None
RECT_GLOVE = (528, 340, 784, 548)
RECT_VISOR = (40, 40, 330, 190)


def full():
    global OCC_B
    from egypt_car_layout import write as write_layout, edge_poly, inside_poly, outline
    t0 = time.time()
    world, winfo = WD.world()
    WD.papyrus(world)
    # ---- the first state (the cut-outs are cut from it): the glovebox shut, the visor up, the freshener on its string
    A, stA, escA = render(ss=SS, fast=False)
    print("first state", round(time.time() - t0, 1))
    # ---- the backdrop: the glovebox's door gone (its compartment open, only the packets in it), no driver's visor, no
    #      freshener; and their shadows gone with them
    OCC_B = stA.occ_without("glovebox", "visor", "freshener")
    B, stB, escB = render(ss=SS, fast=False, occ=OCC_B, glovebox_state=None, visor_state=None, freshener_on=False)
    print("backdrop", round(time.time() - t0, 1))
    cA, iA = compose(A, stA, escA, world)
    cB, iB = compose(B, stB, escB, world)
    pA = crisp_edges(paint(grade(wob(cA))), stA, far=iA["under"])
    pB = crisp_edges(paint(grade(wob(cB))), stB, far=iB["under"])
    print("painted", round(time.time() - t0, 1))
    # ---- the other states, each painted on its own patch
    pMap, stMap = patch(RECT_GLOVE, cB, glovebox_state="map", visor_state=None, freshener_on=False)
    pEmpty, stEmpty = patch(RECT_GLOVE, cB, glovebox_state="empty", visor_state=None, freshener_on=False)
    pDown, stDown = patch(RECT_VISOR, cB, glovebox_state=None, visor_state="down", freshener_on=False)
    print("states", round(time.time() - t0, 1))
    m = {"glovebox-shut": cover(stA, "glovebox"), "visor-up": cover(stA, "visor"), "freshener": cover(stA, "freshener"),
         "glovebox-map": cover(stMap, "glovebox", RECT_GLOVE), "glovebox-empty": cover(stEmpty, "glovebox", RECT_GLOVE),
         "visor-down": cover(stDown, "visor", RECT_VISOR)}
    # the glovebox's door is the same door with the map in the compartment or not: the empty state takes the map state's
    # own painted pixels wherever the door shows in both, so that taking the map changes nothing of the door
    door_map = named(stMap, "glove-door", rect=RECT_GLOVE)
    pEmpty = np.where((door_map & m["glovebox-empty"])[..., None], pMap, pEmpty)
    pics = {"glovebox-shut": pA, "visor-up": pA, "freshener": pA, "glovebox-map": pMap, "glovebox-empty": pEmpty, "visor-down": pDown}
    np.save(f"{WORK}/back.npy", pB)
    np.save(f"{WORK}/first.npy", pA)
    to_image(pB).save(f"{WORK}/2-back.png")
    to_image(pA).save(f"{WORK}/2-first.png")
    for nm, p, (x0, y0, x1, y1) in (("map", pMap, RECT_GLOVE), ("empty", pEmpty, RECT_GLOVE), ("down", pDown, RECT_VISOR)):
        ref = pB.copy()                                                    # each later state's own painting (egypt_car_check.py lays the
        ref[y0:y1, x0:x1] = p[y0:y1, x0:x1]                                # backdrop and the cut-outs together and compares)
        to_image(ref).save(f"{WORK}/2-{nm}.png")
    sizes = {"back": finish(pB, f"{OUT}/back.png", 160)}
    for name in ("glovebox-shut", "visor-up", "visor-down", "freshener"):
        sizes[name] = finish(pics[name], f"{OUT}/{name}.png", 64, m[name].astype(F32))
    sizes.update(finish_states(pics, m, ("glovebox-map", "glovebox-empty"), 64))
    print("finished", round(time.time() - t0, 1), sizes)
    # ---- what each thing covers, for layout.json
    way = openings()
    seen_out = (iB["way"] == 1) * escB + stB.down(stB.mask_of("hood", "cowl", "wiper").astype(F32))
    glass_view = wob(np.clip(seen_out, 0, 1).astype(F32)) > 0.5           # through the windshield: the world, and the hood, the cowl, the wipers
    masks = {
        "windshield": glass_view,
        "visor": m["visor-up"], "rearview": named(stA, "mirror"), "freshener": m["freshener"],
        "door": (named(stA, "door-l", "armrest", "pocket", "crank", "lock", "manual") | (wob(((way == 3) & (escA > 0.5)).astype(F32)) > 0.5)) & (_Y > 40),
        "manual": named(stA, "manual"),
        "seat": named(stA, "seat", "belt", "wrapper", "sock"),
        "glovebox": m["glovebox-shut"],
        "cupholder": named(stA, "slushie", "holder"),
        "wheel": named(stA, "rim", "spoke"),
        "radio": named(stA, "radio"),
        "gauges": named(stA, "cluster", "dial"),
        "horn": named(stA, "horn"),
        "gears": named(stA, "gears", "gears-knob"),
        "key": named(stA, "key", "ignition"),
    }
    extra_masks = {"visor-down": m["visor-down"],
                   "glovebox-open": m["glovebox-map"] | named(stMap, "glove-inside", "packets", rect=RECT_GLOVE)}
    json.dump({"names": sorted(stA.names)}, open(f"{WORK}/names.json", "w"))
    # kept for the layout (python3 egypt_car.py layout, without painting again) and for egypt_car_check.py: what each
    # thing covers, what the rays met that is not glass (the car itself), the hood under the sand
    solid = (1 - escB) - stB.down(stB.mask_of("hood", "cowl", "wiper").astype(F32))
    np.savez_compressed(f"{WORK}/masks.npz", glass_view=glass_view, solid=wob(np.clip(solid, 0, 1).astype(F32)) > 0.5,
                        escaped_a=escA, escaped_b=escB, way=way, under=iA["under"], hood=iA["hood"],
                        **{"m-" + k: v for k, v in masks.items()}, **{"x-" + k: v for k, v in extra_masks.items()})
    doc = lay(masks, extra_masks, glass_view, iA)
    # ---- the comps: the first state, and the later one (the glovebox open with the map, the visor down)
    comp(["back", "glovebox-shut", "visor-up", "freshener"], "out/egypt-car-comp.png")
    comp(["back", "glovebox-map", "visor-down", "freshener"], "out/egypt-car-comp-later.png")
    comp(["back", "glovebox-empty", "visor-down", "freshener"], "out/egypt-car-comp-empty.png")
    print("done", round(time.time() - t0, 1))
    return doc


def lay(masks, extra_masks, glass_view, info):
    """layout.json from what each thing covers: the glass traced exactly, the moving things' marks, the notes."""
    from egypt_car_layout import write as write_layout, edge_poly
    glass = edge_poly(glass_view)
    fx = fx_marks(glass, info)
    notes = layout_notes(glass, glass_view)
    return write_layout(masks, dict(extra_masks, glass=glass, fx=fx, notes=notes))


def relay():
    """layout.json again from the masks the last full run kept (out/egypt-car-work/masks.npz)."""
    z = np.load(f"{WORK}/masks.npz")
    masks = {k[2:]: z[k] for k in z.files if k.startswith("m-")}
    extra = {k[2:]: z[k] for k in z.files if k.startswith("x-")}
    return lay(masks, extra, z["glass_view"], {"under": z["under"], "hood": z["hood"]})


def finish_states(pics, m, names, colors):
    """The states of one cut-out finished together: one palette for all of them and the same grain, so that a pixel
    painted alike in two states (the glovebox's door, with the map in the compartment or not) is the same pixel in both
    files."""
    gs = {n: grain(pics[n], 7, 0.012) for n in names}
    sample_of = np.concatenate([gs[n][m[n]].reshape(-1, 3) for n in names])
    pal = palette_of([sample_of], colors=colors)
    sizes = {}
    for n in names:
        save(f"{OUT}/{n}.png", to_palette(gs[n], pal, speckle=0.008), pal, m[n].astype(F32))
        sizes[n] = os.path.getsize(f"{OUT}/{n}.png")
    return sizes


def comp(names, out, folder=OUT):
    im = Image.open(f"{folder}/{names[0]}.png").convert("RGBA")
    for n in names[1:]:
        im.alpha_composite(Image.open(f"{folder}/{n}.png").convert("RGBA"))
    im.convert("RGB").save(out)
    return im


def fx_marks(glass, info):
    """Everything here that moves by nature, in the engine's own terms (js/engine/effects.js), in the order they are laid:
    the light on the strip of river, the steam off the hood, the air freshener's swing, the dust in the sun over the
    Son's seat. Measured from the picture: the steam leaves where the hood runs under the sand at its left, the
    freshener's knot is the row its string is tied at, the dust's patch is the sunlit part of the cushion and the air
    over it."""
    r = lambda pts: [[int(round(x)), int(round(y))] for x, y in pts]
    under, hood = info["under"], info["hood"]
    ys, xs = np.nonzero(hood & ~under)                                     # the hood as seen, and where it runs under the sand
    edge = [(x, y) for x, y in zip(xs.tolist(), ys.tolist()) if under[max(y - 1, 0), x]]
    left = [p for p in edge if p[0] < 330]
    sx, sy = min(left, key=lambda p: abs(p[0] - 300)) if left else (300, 260)
    kx, ky, kz = M.FRESHENER["knot"]
    knot = V.pt(kx, ky, kz)
    xr0 = V.pt(M.TUMBLE + 2, M.ROOF, M.GLASS["z1"])[0]
    river = r([(xr0 + 4, WD.HZ + 2.5), (744, WD.HZ + 2.5), (744, 158), (520, 156), (400, 166), (262, 154), (120, 168), (60, 180), (xr0 - 8, 186)])
    dust = r([(548, 516), (742, 512), (746, 598), (552, 598)])                    # the cushion in the sun (x 540 to 740; beyond, the Son's door shades it)
    return [
        {"type": "shimmer", "id": "river", "poly": river, "count": 14, "size": 3, "flow": [3, 0], "life": 1.6, "color": "#fff6e2", "opacity": 0.3,
         "plane": "back", "clip": glass, "optional": True,
         "what": "the strip of the Nile above the mound, through the windshield: light moving on it, very small and quiet (the painting's own glitter "
                 "under the sun stays, at the right). Behind every cut-out (the air freshener hangs in front of it), and kept in the glass ('clip')"},
        {"type": "smoke", "id": "steam", "at": [int(sx), int(sy)], "height": int(sy - 120), "width": [4, 30], "lean": [34, -int(sy - 120)], "rise": 22,
         "rate": 3, "gust": 0.4, "color": "#f6f4ee", "opacity": 0.4, "plane": "back", "clip": glass,
         "what": "steam off the radiator, rising from the hood's left side where it runs under the sand, up across the shaded mound to the "
                 "river's strip, leaning a little to the right: white against the sand. 'clip' is the windshield's glass, exactly (it is outside "
                 "the glass: it never runs over a pillar, the dash, the mirror or the wheel); 'plane' back: behind every cut-out (the visor, down, "
                 "hangs in front of it)"},
        {"type": "sway", "id": "freshener", "plane": "freshener", "anchor": "top", "at": [int(round(knot[0])), int(round(knot[1]))], "amount": 1.2,
         "period": 3.5,
         "what": "the air freshener swinging a little on its string, in the air from the open window: pinned at the string's knot under the "
                 "mirror ('at': the knot, its row the pin's), the card at the string's end moving most"},
        {"type": "shimmer", "id": "dust", "poly": dust, "count": 12, "size": 1.5, "flow": [2, -4], "life": 3, "color": "#fff2d8", "opacity": 0.5,
         "plane": "front", "optional": True,
         "what": "dust drifting up in the shaft of sun that lies across the Son's cushion: the cushion's sunlit patch, below the glovebox's dropped "
                 "door and clear of it (on the front plane, so it is kept off the glovebox altogether). If it reads as glints on water, leave it out"},
    ]


def layout_notes(glass, glass_view):
    inside = __import__("egypt_car_layout").inside_poly(glass)
    off = int((inside & ~glass_view).sum())
    missed = int((glass_view & ~inside).sum())
    return [
        "nobody is drawn here: the scene is unseen; the lead stands, undrawn, on the mark 'default' (430, 590), in the walk patch; no thing's shape "
        "covers it",
        "the camera is room.View's (view): square to the car (yaw 0: the dashboard runs level), its vanishing point toward the wheel (centre_x 236), "
        "the lens 500; the eye's row (horizon 181) is where the car's own level is: the car is nose-down 7 degrees (as the river picture draws it), "
        "so the world's horizon through the glass is row 120. 'full' 282 is the eye 110.5 cm above the floor. Nobody is drawn: they size nothing seen",
        "the cartoon's cheats (egypt_car_model.py): the Son's half of the bench is drawn forward of Dad's and higher, so that its cushion shows at the "
        "bottom right (a forward camera cannot see a real one); its back is beside Dad's shoulder and is not in the picture (the passenger's door and "
        "window are at the right edge); the windshield stands nearly upright, so that the headliner, the visors and the mirror show above it",
        "the bottom band (rows 548 to 600) is the way out: no shape reaches into it but the door's, the manual's and the key's ring; the bench's "
        "middle at the bottom (x 380 to 470) is bare (the floor between the halves of the bench)",
        "the glovebox is seen whole, shut and open, with nothing in front of it; the cut-outs are pixel-aligned with the backdrop, which is "
        "complete under them: it shows the compartment open with only the ketchup packets in it, no driver's visor, no air freshener",
        f"glass: the windshield's glass, exactly: {len(glass)} corners; {off} pixels inside it that are not glass, {missed} pixels of glass outside it",
    ]


if __name__ == "__main__":
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    if mode == "plan":
        plan()
        print("plan", round(time.time() - t0, 1), "s")
        sys.exit()
    if mode == "layout":
        relay()
        print("layout", round(time.time() - t0, 1), "s")
        sys.exit()
    if mode in ("fast", "paint"):
        out, st, info, cinfo = whole(fast=True, ss=1)
        to_image(out).save(f"{WORK}/fast.png")
        overlay(out, "fast-plan.png")
        tones(out, "tones:")
        print("fast", round(time.time() - t0, 1), "s;", len(st.occ), "shadow boxes;", len(st.names), "things")
        if mode == "paint":
            p = paint(out)
            to_image(p).save(f"{WORK}/paint.png")
            print("paint", round(time.time() - t0, 1), "s")
        sys.exit()
    doc = full()

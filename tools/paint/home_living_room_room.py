"""The living room's shell and everything that never moves: floor, walls, stairs, the landing upstairs, the
kitchen seen through its doorway, bookcase, print, clock, front door, sampler, coats, window, chandelier.

All of it is laid into one Layer through the one camera (see home_living_room_kit.py). Measurements are the
model's (home_living_room_model.py), in centimetres."""

import math

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, rgb, lerp, noise
from room import View
import home_living_room_model as M
from home_living_room_kit import (Cam, Layer, Lamps, paint_of, flat, col, sstep, hash2, vnoise, fbm, rot, tone)

V = View(**M.VIEW)
(XL, XR), (ZB, ZF), HH, G = M.ROOM["X"], M.ROOM["Z"], M.ROOM["H"], M.G
FL = {f[0]: f for f in M.FLATS}
BX = {b[0]: b[1:] for b in M.BOXES}
ST = M.STAIRS[0]
RISE, STEPS = ST["rise"], ST["steps"]
STEP_H, STEP_D = RISE / STEPS, (ST["z_foot"] - ST["z_top"]) / STEPS
SW = ST["X"][1]                                             # the stairs' open side (X = 108)
PITCH = STEP_H / STEP_D

TAG = dict(door=1, sampler=2, kitchen=3, books=4, frame=5, clock=6, piano=7, stairs=8, closet=9, window=10, photos=11, table=12,
           bible=13, armchair=14, crossword=15, pencil=16, rug=17, coats=18, chandelier=19, upson=20, upgirls=21, upstudy=22,
           lamp=23, stool=24, pendant=25, panel=26, rail=27)

# ---- the colors things are made of (before any light falls on them)
WHITE = col((0.80, 0.76, 0.63))                             # painted woodwork
PAPER = col((0.50, 0.62, 0.55))                             # the wallpaper: a grey sea-green
OAK = col((0.60, 0.45, 0.28))
DARKWOOD = col((0.30, 0.17, 0.10))
BRASS = col((0.80, 0.60, 0.24))
RED = col((0.52, 0.13, 0.11))
NAVY = col((0.13, 0.18, 0.34))
CREAM = col((0.86, 0.79, 0.62))
MOON_WAY = (-0.565, 0.740, -0.367)                          # the way to the moon from inside the room


def pxcm(X, Z):
    """Picture pixels per centimetre at a place in the room (so that thin lines never get thinner than a pixel)."""
    d = (X - V.cam_x) * V.fx + (Z - V.cam_z) * V.fz
    return V.F / np.maximum(d, 30.0)


def near(v, at, half, px, least=0.55):
    """1 on the line v = at, falling to 0 at `half` cm away; never thinner than about a pixel."""
    h = np.maximum(half, least / px)
    return np.clip(1.0 - np.abs(v - at) / h, 0, 1)


def panel(u, v, u0, u1, v0, v1, bevel=3.0):
    """A sunk panel in painted woodwork: -> how much lighter or darker (1 = the frame round it)."""
    inside = (u > u0) & (u < u1) & (v > v0) & (v < v1)
    du0, du1, dv0, dv1 = u - u0, u1 - u, v - v0, v1 - v
    k = np.where(inside, 0.90, 1.0)
    k = np.where(inside & (dv1 < bevel) & (dv1 < du0 + 0.01) & (dv1 < du1 + 0.01), 0.60, k)       # the top edge is in its own shade
    k = np.where(inside & (du0 < bevel) & (du0 <= dv1) & (du0 <= dv0), 0.70, k)
    k = np.where(inside & (dv0 < bevel) & (dv0 <= du0) & (dv0 <= du1), 1.12, k)                    # the bottom edge catches the light
    k = np.where(inside & (du1 < bevel) & (du1 <= dv1) & (du1 <= dv0), 1.06, k)
    return k.astype(F32)


class Tex:
    """A flat drawing (made with Pillow in its own measurements) to be laid on a wall, a floor or a page."""

    def __init__(self, w_cm, h_cm, ppc=3.0, ground=(128, 128, 128)):
        self.wc, self.hc, self.k = w_cm, h_cm, ppc
        self.im = Image.new("RGB", (max(2, int(w_cm * ppc)), max(2, int(h_cm * ppc))), ground)
        self.d = ImageDraw.Draw(self.im)

    def xy(self, u, v):
        return (u * self.k, (self.hc - v) * self.k)          # v runs up, as heights do

    def rect(self, u0, v0, u1, v1, fill):
        a, b = self.xy(u0, v1), self.xy(u1, v0)
        self.d.rectangle([a[0], a[1], b[0], b[1]], fill=fill)

    def poly(self, pts, fill):
        self.d.polygon([self.xy(u, v) for u, v in pts], fill=fill)

    def line(self, pts, fill, w=1.0):
        self.d.line([self.xy(u, v) for u, v in pts], fill=fill, width=max(1, int(round(w * self.k))))

    def oval(self, u, v, ru, rv, fill):
        a, b = self.xy(u - ru, v + rv), self.xy(u + ru, v - rv)
        self.d.ellipse([a[0], a[1], b[0], b[1]], fill=fill)

    def array(self):
        self.arr = np.asarray(self.im, dtype=F32) / 255.0
        return self.arr

    def at(self, u, v):
        """Colors at places (u, v) in cm (bilinear)."""
        a = getattr(self, "arr", None)
        if a is None:
            a = self.array()
        h, w = a.shape[:2]
        x = np.clip(u * self.k - 0.5, 0, w - 1.001)
        y = np.clip((self.hc - v) * self.k - 0.5, 0, h - 1.001)
        x0, y0 = np.floor(x).astype(np.intp), np.floor(y).astype(np.intp)
        fx, fy = (x - x0)[:, None], (y - y0)[:, None]
        return (a[y0, x0] * (1 - fx) + a[y0, x0 + 1] * fx) * (1 - fy) + (a[y0 + 1, x0] * (1 - fx) + a[y0 + 1, x0 + 1] * fx) * fy


def c255(c, k=1.0):
    c = col(c) * k
    return tuple(int(max(0, min(255, v * 255))) for v in c)


# =================================================================== the room
class Room:
    def __init__(self, cache=None, ss=2):
        self.cam = Cam(V, ss)
        self.ss = ss
        self.L = Lamps(self.cam)
        self.cache = cache
        self.mott = noise((600, 800), 46, 21, 4)             # patchiness, as a brush leaves
        self.mott2 = noise((600, 800), 12, 22, 3)
        self.lights()

    # ------------------------------------------------------------ light
    def lights(self):
        L, lt = self.L, M.LIGHTS
        warm = (1.0, 0.72, 0.40)
        L.lamp("pendant", lt["pendant"], (1.0, 0.76, 0.44), 3.3, reach=165, down=1.0, up=0.10, side=0.30, fill=0.12)
        L.lamp("reading", lt["reading"], warm, 3.6, reach=125, down=1.0, up=0.55, side=0.50, fill=0.12)
        L.lamp("piano", lt["piano"], (1.0, 0.78, 0.48), 3.9, reach=120, down=1.0, up=1.0, side=0.34, fill=0.12)
        k = FL["kitchen"]
        L.lamp("kitchen", lt["kitchen"], (1.0, 0.86, 0.60), 5.6, reach=210, down=1.0, up=0.6, side=0.9, fill=0.10,
               door=("Z", 0.0, k[2], k[3], k[4], k[5]))
        L.lamp("upstairs", lt["upstairs"], warm, 3.9, reach=140, down=0.9, up=1.0, side=0.36, fill=0.2)
        # the room's own glow over the rug (lamplight that has been round the walls once): soft, and it throws no shadows
        L.lamp("glow", (410, 250, 400), (1.0, 0.80, 0.52), 0.50, reach=250, down=1.0, up=0.2, side=0.5, fill=0.3, throws=False)
        w = FL["window"]
        L.set_moon(MOON_WAY, (0.50, 0.66, 1.0), 1.45, (w[2], w[3], w[4], w[5], [w[2] + 53.3, w[2] + 106.7], [w[4] + 54, w[4] + 108, w[4] + 162, w[4] + 216], 2.6))
        L.cool = col((0.066, 0.092, 0.195))
        L.warm = col((0.066, 0.044, 0.024))

    def occluders(self, things=()):
        """Everything that throws a shadow on the floor and the walls."""
        b = []
        for x0, x1, y0, y1, z0, z1 in V.stairs(ST["X"][0], ST["X"][1], ST["z_foot"], ST["z_top"], RISE, STEPS)[1::2]:
            b.append((x0, x1, y0, y1, z0 - STEP_D, z1))      # the stairs, two steps at a time
        b.append((0, SW, 0, G, 0, ST["z_top"]))               # the block under the top of the stairs
        b.append((0, XR, G - 18, G, 0, 175))                  # the landing
        b.append(BX["books"])
        b.append((XR - 36, XR - 4, 0, 29, 416, 448))            # the plant's pot
        b.append((XR - 22, XR - 4, 0, 34, 172, 204))            # the school bag
        b.append((XR - 34, XR - 14, 0, 20, 308, 328))           # the ball
        b.append((SW - 7, SW + 5, 0, 126, ST["z_foot"] + 4, ST["z_foot"] + 16))    # the newel at the foot of the stairs
        b.append((SW + 1, SW + 22, 60, 74, 90, 152))             # the telephone table
        for t in things:
            b.append(tuple(float(v) for v in t))
        self.L.boxes = b
        return b

    def bake(self):
        L = self.L
        L.bake("floor", "Y", 0.0, cache=self.cache)
        L.bake("back", "Z", 0.0, cache=self.cache, soft=1.2)
        L.bake("left", "X", 0.0, cache=self.cache, soft=1.2)
        L.bake("right", "X", float(XR), cache=self.cache, soft=1.2)
        L.bake("side", "X", float(SW), cache=self.cache, soft=1.2)
        L.bake_moon("floor", "Y", 0.0, self.banister_boxes())

    def banister_boxes(self):
        """The stairs and their rail, for the moon's shadows: every step, every baluster, the handrail in short lengths."""
        zt, zf, x1 = ST["z_top"], ST["z_foot"], SW
        b = [tuple(float(v) for v in bx) for bx in V.stairs(ST["X"][0], ST["X"][1], zf, zt, RISE, STEPS)]
        b.append((0.0, x1, 0.0, float(G), 0.0, zt))

        def rail_y(Z):
            return (zf - Z) * PITCH + STEP_H + 88.0
        for i in range(STEPS):
            y = STEP_H * (i + 1)
            for f in (0.28, 0.78):
                z = zf - STEP_D * (i + f)
                if z < zt + 9:
                    continue
                b.append((x1 - 4.4, x1 - 1.6, y, rail_y(z) - 3.0, z - 1.4, z + 1.4))
            zc = zf - STEP_D * (i + 0.5)
            b.append((x1 - 6.0, x1 + 1.0, rail_y(zc + STEP_D / 2) - 6.0, rail_y(zc - STEP_D / 2), zc - STEP_D / 2, zc + STEP_D / 2))
        b.append((x1 - 7.0, x1 + 5.0, 0.0, rail_y(zf + 10.0) + 30.0, zf + 4.0, zf + 16.0))
        b.append((x1 - 7.0, x1 + 5.0, float(G), G + 120.0, zt - 4.0, zt + 8.0))
        return b

    def P(self, albedo, **kw):
        if "mott" not in kw:
            kw["mott"] = (self.mott, 0.07)
        return paint_of(self.L, albedo, **kw)

    # ------------------------------------------------------------ what surfaces are made of
    def floor_alb(self, X, Y, Z, iy, ix):
        px = pxcm(X, Z)
        w = 12.0
        b = np.floor(X / w)
        f = X / w - b
        ln = 120.0 + 110.0 * hash2(b, 1.0, 3.0)
        zz = (Z + hash2(b, 2.0, 3.0) * ln) / ln
        seg = np.floor(zz)
        fz = zz - seg
        tn = 0.80 + 0.40 * hash2(b, seg, 7.0)
        hue = hash2(b, seg, 11.0) - 0.5
        g = fbm(X * 0.5, Z * 0.03, 5.0, 2)
        c = OAK[None, :] * (tn * (0.86 + 0.28 * g))[:, None]
        c[:, 0] *= 1 + 0.10 * hue
        c[:, 2] *= 1 - 0.25 * hue
        jw = np.maximum(0.5, 0.62 / px)
        j = np.clip(1 - np.minimum(f, 1 - f) * w / jw, 0, 1)
        bj = np.clip(1 - np.minimum(fz, 1 - fz) * ln / jw, 0, 1)
        c *= (1 - 0.50 * np.maximum(j, bj))[:, None]
        # the lane people walk (door to stairs, round the rug) is worn paler; the edges by the walls are darker
        wear = fbm(X * 0.012, Z * 0.012, 9.0, 2)
        c *= (0.93 + 0.14 * wear)[:, None]
        edge = np.minimum(np.minimum(X, XR - X), Z)
        edge = np.where(X < SW + 2, np.minimum(edge, np.abs(Z - ST["z_foot"]) + 400 * (Z < ST["z_foot"])), edge)
        c *= (1 - 0.30 * np.exp(-np.maximum(edge, 0) / 9.0))[:, None]
        return c

    def floor_sheen(self, X, Y, Z, n, iy, ix):
        """The floor is polished: the lit kitchen doorway lies in it as a long soft streak toward us."""
        k = FL["kitchen"]
        vx, vy, vz = X - V.cam_x, Y - V.eye, Z - V.cam_z
        rz = np.where(vz > -1e-3, -1e-3, vz)
        s = -Z / rz                                           # the mirrored sight line meets the back wall here
        hx, hy = X + vx * s, -vy * s
        soft = 5.0 + 0.10 * hy
        g = sstep(k[2] - soft, k[2] + soft, hx) * sstep(k[3] + soft, k[3] - soft, hx) * sstep(k[5] + soft * 2, k[5] - soft * 2, hy)
        vl = np.sqrt(vx * vx + vy * vy + vz * vz)
        graze = (1 - np.abs(vy) / vl) ** 2
        streak = 0.55 + 0.45 * fbm(X * 0.45, Z * 0.02, 19.0, 2)                                   # broken by the boards
        return (g * graze * streak * 1.05)[:, None] * np.array([1.0, 0.86, 0.60], dtype=F32)

    def wall_alb(self, wall):
        """Painted woodwork below a rail, striped paper above, a skirting, a cornice. `wall`: back, left, right."""

        def alb(X, Y, Z, iy, ix):
            px = pxcm(X, Z)
            u = X if wall == "back" else Z
            if wall == "back":
                base = np.where(Y > G - 1, float(G), 0.0)                       # upstairs the wall starts again at the landing's floor
                top = np.where(Y > G - 1, float(HH), float(G - 18))
            elif wall == "left":
                base = np.where(Z < ST["z_foot"], np.clip((ST["z_foot"] - Z) * PITCH + STEP_H, 0, RISE), 0.0)
                top = np.full_like(Y, float(HH))
            else:
                base = np.where((Z < 175) & (Y > G - 1), float(G), 0.0)
                top = np.where((Z < 175) & (Y < G), float(G - 18), float(HH))
            h = Y - base
            # paper: stripes every nine centimetres, with a pale pin line between
            s = np.floor(u / 9.0)
            fs = u / 9.0 - s
            even = (np.mod(s, 2) < 0.5)
            c = PAPER[None, :] * np.where(even, 1.0, 0.84)[:, None]
            pin = near(fs, 0.0, 0.05, px * 9.0, 0.35) + near(fs, 1.0, 0.05, px * 9.0, 0.35)
            c = c + (CREAM[None, :] * 0.8 - c) * (np.clip(pin, 0, 1) * 0.50)[:, None]
            sprig = (hash2(s, np.floor(Y / 13.0), 4.0) > 0.5) & even                 # a small sprig in the wider stripes
            dd = np.hypot((fs - 0.5) * 9.0, np.mod(Y, 13.0) - 6.5)
            c = c + (CREAM[None, :] * 0.9 - c) * (np.clip(1 - dd / np.maximum(1.6, 0.8 / px), 0, 1) * sprig * 0.55)[:, None]
            c *= (0.92 + 0.16 * fbm(u * 0.02, Y * 0.02, 13.0, 2))[:, None]
            # woodwork below the rail: narrow boards with a bead between
            dado = h < 96.0
            wb = WHITE[None, :] * (0.95 + 0.08 * hash2(np.floor(u / 9.0), 0.0, 17.0))[:, None]
            bead = near(u / 9.0 - np.floor(u / 9.0), 0.0, 0.07, px * 9.0, 0.4) + near(u / 9.0 - np.floor(u / 9.0), 1.0, 0.07, px * 9.0, 0.4)
            wb = wb * (1 - 0.30 * np.clip(bead, 0, 1))[:, None]
            c = np.where(dado[:, None], wb, c)
            rail = (h > 92.0) & (h < 100.0)
            c = np.where(rail[:, None], WHITE[None, :] * 1.06, c)
            c *= (1 - 0.42 * near(h, 91.2, 0.9, px))[:, None]                    # the shade under the rail
            c *= (1 - 0.25 * near(h, 100.4, 0.5, px))[:, None]
            skirt = h < 14.0
            c = np.where(skirt[:, None], WHITE[None, :] * 0.98, c)
            c *= (1 - 0.40 * near(h, 14.5, 0.7, px))[:, None]
            # a picture rail where the upstairs floor is, and a cornice under the ceiling (the two-storey walls only)
            if wall != "back":
                two = (top > G + 10) & (base < 1.0) if wall == "right" else (top > G + 10)
                pr = two & (Y > G - 4) & (Y < G + 5)
                c = np.where(pr[:, None], WHITE[None, :] * 1.02, c)
                c *= (1 - 0.35 * near(Y, G - 5.0, 0.8, px) * two)[:, None]
            corn = (Y > HH - 22) & (top > HH - 1)
            c = np.where(corn[:, None], WHITE[None, :] * (0.92 + 0.10 * np.sin((Y - (HH - 22)) / 22.0 * 9.0))[:, None], c)
            c *= (1 - 0.40 * near(Y, HH - 22.6, 0.8, px) * (top > HH - 1))[:, None]
            # corners and the meeting with floor and ceiling are a little darker
            dn = np.minimum(h, top - Y)
            c *= (1 - 0.30 * np.exp(-np.maximum(dn, 0) / 10.0))[:, None]
            if wall == "back":
                side = np.minimum(X - np.where(Y < G, SW, 0.0), XR - X)
            else:
                side = Z
            c *= (1 - 0.28 * np.exp(-np.maximum(side, 0) / 16.0))[:, None]
            return c
        return alb

    def wood(self, base, seed=1.0, along="Y", grain=0.22, scale=1.0):
        base = col(base)

        def alb(X, Y, Z, iy, ix):
            if along == "Y":
                g = fbm((X + Z) * 0.6 * scale, Y * 0.035 * scale, seed, 2)
            elif along == "X":
                g = fbm((Y + Z) * 0.6 * scale, X * 0.035 * scale, seed, 2)
            else:
                g = fbm((X + Y) * 0.6 * scale, Z * 0.035 * scale, seed, 2)
            return base[None, :] * (1 - grain / 2 + grain * g)[:, None]
        return alb

    def runner_alb(self, X, Y, Z, iy, ix, tread=True):
        """The stair carpet: a deep red runner with a gold and navy border, oak (or white risers) either side."""
        px = pxcm(X, Z)
        mid = 54.0
        d = np.abs(X - mid)
        wood = OAK[None, :] * 0.82 * (0.85 + 0.3 * fbm(X * 0.04, (Z + Y) * 0.5, 3.0, 2))[:, None] if tread else np.broadcast_to(WHITE * 0.97, X.shape + (3,)).copy()
        c = wood
        red = RED[None, :] * (0.9 + 0.25 * fbm(X * 0.15, (Z + Y) * 0.15, 8.0, 2))[:, None]
        c = np.where((d < 33)[:, None], red, c)
        c = np.where(((d > 25.5) & (d < 30))[:, None], BRASS[None, :] * 0.8, c)
        c = np.where(((d > 30) & (d < 33))[:, None], NAVY[None, :], c)
        dia = np.abs(np.mod(X - mid + (Z + Y) * 0.0, 12.0) - 6.0) + np.abs(np.mod(Z * 1.0 + Y * 1.4, 12.5) - 6.25)
        c = np.where(((d < 22) & (dia < 2.2))[:, None], BRASS[None, :] * 0.62, c)
        return c

    # ------------------------------------------------------------ the shell
    def shell(self, lay):
        P, L = self.P, self.L
        k = FL["kitchen"]
        w = FL["window"]
        # floor (and the ground beyond the picture's front edge)
        lay.poly([(XL, 0, ZB), (XR, 0, ZB), (XR, 0, ZF + 300), (XL, 0, ZF + 300)], P(self.floor_alb, plane="floor", mott=(self.mott, 0.10), gloss=self.floor_sheen, moon=2.2))
        # back wall, round the kitchen doorway
        back = P(self.wall_alb("back"), plane="back")
        lay.poly([(XL, 0, 0), (k[2], 0, 0), (k[2], HH, 0), (XL, HH, 0)], back)
        lay.poly([(k[3], 0, 0), (XR, 0, 0), (XR, HH, 0), (k[3], HH, 0)], back)
        lay.poly([(k[2], k[5], 0), (k[3], k[5], 0), (k[3], HH, 0), (k[2], HH, 0)], back)
        # left wall, round the tall window
        left = P(self.wall_alb("left"), plane="left")
        lay.poly([(0, 0, 0), (0, 0, w[2]), (0, HH, w[2]), (0, HH, 0)], left)
        lay.poly([(0, 0, w[3]), (0, 0, ZF), (0, HH, ZF), (0, HH, w[3])], left)
        lay.poly([(0, 0, w[2]), (0, 0, w[3]), (0, w[4], w[3]), (0, w[4], w[2])], left)
        lay.poly([(0, w[5], w[2]), (0, w[5], w[3]), (0, HH, w[3]), (0, HH, w[2])], left)
        # right wall
        lay.poly([(XR, 0, 0), (XR, 0, ZF), (XR, HH, ZF), (XR, HH, 0)], P(self.wall_alb("right"), plane="right"))
        # ceiling: plaster, with the night in it
        lay.poly([(XL, HH, 0), (XR, HH, 0), (XR, HH, ZF), (XL, HH, ZF)], P((0.50, 0.50, 0.50), skip=("upstairs",)))

    # ------------------------------------------------------------ the tall window on the stair wall
    def window(self, lay):
        P = self.P
        w = FL["window"]
        Z0, Z1, Y0, Y1 = w[2], w[3], w[4], w[5]
        T = Tex(Z1 - Z0, Y1 - Y0, 3.0, c255((0.10, 0.17, 0.36)))
        im = T.im
        a = np.zeros((im.size[1], im.size[0], 3), dtype=F32)
        hh, ww = a.shape[:2]
        yy = np.linspace(0, 1, hh)[:, None]
        sky = lerp(np.array([0.050, 0.085, 0.24]), np.array([0.19, 0.30, 0.52]), yy ** 1.6)                # deeper overhead
        a[...] = sky[:, None, :] if sky.ndim == 2 else sky
        a = a * (0.9 + 0.2 * noise((hh, ww), 60, 3, 3))[..., None]
        cl = noise((hh, ww), (160, 40), 5, 4)                                                               # a few torn night clouds
        a = a + np.clip(cl - 0.55, 0, 1)[..., None] * np.array([0.20, 0.24, 0.34]) * 1.5
        rng = np.random.default_rng(4)
        for _ in range(46):                                                                                  # stars
            sx, sy = rng.integers(2, ww - 2), rng.integers(2, int(hh * 0.8))
            a[sy, sx] += np.array([0.7, 0.75, 0.8]) * rng.random()
        T.im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
        T.d = ImageDraw.Draw(T.im)
        mu, mv = 80.0, 189.0                                                                                 # the moon, in the middle of an upper pane
        for r, g in ((30, 0.10), (22, 0.16), (15, 0.30)):
            T.oval(mu, mv, r, r, c255(lerp(np.array([0.12, 0.2, 0.42]), np.array([0.75, 0.82, 0.92]), g)))
        T.oval(mu, mv, 10.5, 10.5, c255((0.97, 0.96, 0.86)))
        T.oval(mu - 3.5, mv + 2.5, 2.6, 2.2, c255((0.84, 0.86, 0.80)))
        T.oval(mu + 3.0, mv - 3.5, 1.8, 1.6, c255((0.86, 0.87, 0.80)))
        ink = c255((0.022, 0.035, 0.085))

        def branch(u, v, ang, ln, wd, depth):                                                                # the black shape of a tree
            if depth == 0 or ln < 4:
                return
            u2, v2 = u + math.cos(ang) * ln, v + math.sin(ang) * ln
            T.line([(u, v), (u2, v2)], ink, wd)
            n = 2 if rng.random() < 0.75 else 3
            for i in range(n):
                branch(u2, v2, ang + rng.uniform(-0.75, 0.75), ln * rng.uniform(0.62, 0.82), max(0.4, wd * 0.62), depth - 1)
        branch(38.0, -6.0, 1.42, 62.0, 7.5, 8)
        branch(150.0, -4.0, 2.05, 40.0, 4.0, 6)
        T.poly([(0, 0), (0, 26), (26, 20), (60, 24), (96, 15), (130, 21), (160, 17), (160, 0)], c255((0.03, 0.05, 0.11)))   # the hedge and the roofs beyond
        T.rect(112, 20, 121, 27, c255((0.035, 0.05, 0.11)))
        T.rect(114.5, 21.5, 117.0, 24.0, c255((0.95, 0.72, 0.30)))                                           # one lit window, far off

        def night(X, Y, Z, n, iy, ix):
            return T.at(Z - Z0, Y - Y0) * 1.25
        lay.poly([(-9, Y0, Z0), (-9, Y0, Z1), (-9, Y1, Z1), (-9, Y1, Z0)], night, TAG["window"])
        frame = P(WHITE * 1.02, moon=0.0)
        rev = P(WHITE * 0.96, moon=0.0)
        # the reveal (the thickness of the wall) and the sill
        lay.poly([(-9, Y0, Z0), (0, Y0, Z0), (0, Y1, Z0), (-9, Y1, Z0)], rev, TAG["window"])
        lay.poly([(-9, Y0, Z1), (0, Y0, Z1), (0, Y1, Z1), (-9, Y1, Z1)], rev, TAG["window"])
        lay.poly([(-9, Y0, Z0), (0, Y0, Z0), (0, Y0, Z1), (-9, Y0, Z1)], rev, TAG["window"])
        lay.poly([(-9, Y1, Z0), (0, Y1, Z0), (0, Y1, Z1), (-9, Y1, Z1)], rev, TAG["window"])
        lay.box(0, 9, Y0 - 7, Y0, Z0 - 10, Z1 + 10, frame, TAG["window"])                                   # sill
        for z in (Z0 - 9, Z1):                                                                               # casing
            lay.box(0, 3, Y0, Y1 + 9, z, z + 9, frame, TAG["window"])
        lay.box(0, 4, Y1, Y1 + 11, Z0 - 11, Z1 + 11, frame, TAG["window"])
        bars = P(WHITE * 0.98, moon=0.0)
        for z in (Z0 + 53.3, Z0 + 106.7):
            lay.box(-7, -3, Y0, Y1, z - 2.2, z + 2.2, bars, TAG["window"])
        for y in (Y0 + 54, Y0 + 108, Y0 + 162, Y0 + 216):
            lay.box(-7, -3, y - 2.2, y + 2.2, Z0, Z1, bars, TAG["window"])
        # curtains drawn back to either side: long, heavy, a dull gold
        cur = P(self.cloth((0.62, 0.50, 0.24), 5.0, fold=7.0), moon=0.25)
        yt, yk, yb = Y1 + 16, Y0 + 50, Y0 - 14
        lay.poly([(4.5, yt, Z0 - 22), (4.5, yt, Z0 + 14), (4.5, yk, Z0 - 3), (4.5, yb, Z0 + 5), (4.5, yb, Z0 - 22)], cur, TAG["window"])
        lay.poly([(4.5, yt, Z1 + 22), (4.5, yt, Z1 - 14), (4.5, yk, Z1 + 3), (4.5, yb, Z1 - 5), (4.5, yb, Z1 + 22)], cur, TAG["window"])
        tie = P(BRASS * 0.8)
        lay.box(4.5, 6.0, yk - 3, yk + 3, Z0 - 22, Z0 - 2, tie, TAG["window"])
        lay.box(4.5, 6.0, yk - 3, yk + 3, Z1 + 2, Z1 + 22, tie, TAG["window"])
        lay.box(2, 7, Y1 + 14, Y1 + 19, Z0 - 28, Z1 + 28, self.P(DARKWOOD * 1.2), TAG["window"])              # the pole

    def cloth(self, base, seed=1.0, fold=6.0, deep=0.35, along="Z"):
        """Hanging cloth: soft upright folds."""
        base = col(base)

        def alb(X, Y, Z, iy, ix):
            u = Z if along == "Z" else X
            f = np.sin(u / fold * 2 * math.pi + 2.5 * vnoise(u * 0.05, Y * 0.012, seed)) * 0.5 + 0.5
            return base[None, :] * (1 - deep + deep * 1.4 * f)[:, None] * (0.9 + 0.2 * fbm(u * 0.03, Y * 0.03, seed + 2, 2))[:, None]
        return alb

    # ------------------------------------------------------------ the stairs, their panelled side and the cupboard
    def stairs(self, lay):
        P = self.P
        tread = P(lambda X, Y, Z, iy, ix: self.runner_alb(X, Y, Z, iy, ix, True), moon=1.9)      # the moon comes down the stairs
        riser = P(lambda X, Y, Z, iy, ix: self.runner_alb(X, Y, Z, iy, ix, False), moon=1.9)
        nose = P(OAK * 1.45, moon=1.9)
        rod = P(BRASS * 1.1, gloss=self.shine(0.9), moon=1.9)
        x0, x1 = ST["X"]
        for i in range(STEPS):
            za = ST["z_foot"] - STEP_D * i                    # the riser's Z
            zb = za - STEP_D
            y = STEP_H * (i + 1)
            lay.poly([(x0, y - STEP_H, za), (x1, y - STEP_H, za), (x1, y - 2.6, za), (x0, y - 2.6, za)], riser, TAG["stairs"])
            lay.poly([(x0, y, zb), (x1, y, zb), (x1, y, za + 2.4), (x0, y, za + 2.4)], tread, TAG["stairs"])
            lay.poly([(x0, y - 2.6, za + 2.4), (x1, y - 2.6, za + 2.4), (x1, y, za + 2.4), (x0, y, za + 2.4)], nose, TAG["stairs"])
            if i:                                               # a brass rod holds the runner into each step
                lay.ribbon((18.0, y - STEP_H + 1.2, za + 1.2), (90.0, y - STEP_H + 1.2, za + 1.2), 1.5, 1.5, rod, TAG["stairs"])
        # the landing the stairs arrive on (the left end of the gallery)
        # the panelled side: a string board along the slope, panels below it, and the block under the landing
        zt, zf = ST["z_top"], ST["z_foot"]

        def string_top(Z):
            return np.where(Z >= zt + STEP_D, (zf - Z) * PITCH + STEP_H + 7.0, RISE + 0.0)

        stiles = [0.0, 88.0, 175.0, 247.0, 320.0, 402.0, 486.0, zf + 16]

        def side_alb(X, Y, Z, iy, ix):
            px = pxcm(X, Z)
            top = string_top(Z)
            c = np.broadcast_to(WHITE, X.shape + (3,)).copy() * (0.96 + 0.07 * fbm(Z * 0.03, Y * 0.03, 31.0, 2))[:, None]
            k = np.ones(X.shape, dtype=F32)
            for za, zb in zip(stiles[:-1], stiles[1:]):
                tl = np.minimum(string_top(np.full_like(Z, za + 6.0)), string_top(np.full_like(Z, zb - 6.0)))    # the lower end of this bay's slope
                hi = string_top(Z) - 30.0                                                                          # under the string board
                if zb <= zt + 1:
                    hi = np.full_like(Z, G - 18 - 14.0)
                # a low panel and (where there is room) a tall one above the middle rail
                k = k * panel(Z, Y, za + 7.0, zb - 7.0, 21.0, np.minimum(hi, 104.0))
                k = k * panel(Z, Y, za + 7.0, zb - 7.0, 118.0, np.where(hi > 132.0, hi, 0.0))
            c *= k[:, None]
            sb = (top - Y < 23.0) & (Z >= zt)                                                                     # the string board
            c = np.where(sb[:, None], WHITE[None, :] * 1.03, c)
            c *= (1 - 0.35 * near(top - Y, 23.6, 0.8, px) * (Z >= zt))[:, None]
            c = np.where((Y < 14.0)[:, None], WHITE[None, :] * 0.98, c)
            c *= (1 - 0.40 * near(Y, 14.5, 0.7, px))[:, None]
            c *= (1 - 0.30 * np.exp(-np.maximum(Y, 0) / 8.0))[:, None]
            c *= (1 - 0.25 * np.exp(-np.maximum(Z, 0) / 14.0))[:, None]
            return c

        side = P(side_alb, plane="side")
        pts = [(x1, 0, zf + 2.4), (x1, 0, 0), (x1, G - 18, 0), (x1, G - 18, zt), (x1, G, zt), (x1, G, zt + STEP_D)]
        pts += [(x1, STEP_H + 7.0, zf), (x1, 7.0, zf + 2.4)]
        lay.poly(pts, side, TAG["stairs"])
        # the low cupboard door, child height, standing ajar the width of a hand
        c = FL["closet"]
        zc0, zc1, yc1 = c[2] + 2.0, c[3] - 2.0, c[5]
        lay.poly([(x1 + 0.4, 1, zc0), (x1 + 0.4, 1, zc1), (x1 + 0.4, yc1, zc1), (x1 + 0.4, yc1, zc0)], flat((0.020, 0.022, 0.040)), TAG["closet"])
        trim = P(WHITE * 1.04)
        for za, zb in ((zc0 - 5, zc0), (zc1, zc1 + 5)):                                                         # its little frame
            lay.box(x1, x1 + 1.6, 0, yc1 + 5, za, zb, trim, TAG["closet"])
        lay.box(x1, x1 + 1.6, yc1, yc1 + 5, zc0 - 5, zc1 + 5, trim, TAG["closet"])
        lay.tf = rot((x1 + 1.0, zc0), -9.0)

        def leaf_alb(X, Y, Z, iy, ix):
            # (the leaf is turned: measure along it by distance from the hinge)
            u = np.hypot(X - (x1 + 1.0), Z - zc0)
            c2 = np.broadcast_to(WHITE * 1.0, X.shape + (3,)).copy()
            c2 *= panel(u, Y, 8.0, (zc1 - zc0) - 8.0, 10.0, yc1 - 9.0)[:, None]
            return c2
        leaf = P(leaf_alb)
        lay.box(x1 + 1.0, x1 + 4.2, 1.5, yc1 - 0.5, zc0, zc1, leaf, TAG["closet"], paints={"front": P(WHITE * 0.80), "top": P(WHITE * 0.9)})
        lay.disc((x1 + 5.2, 52.0, zc1 - 7.0), 2.6, P(BRASS, gloss=self.shine(0.5)), TAG["closet"], axis="X", sides=10)
        lay.tf = None

    def shine(self, k=0.4, tint=(1.0, 0.9, 0.65)):
        """A little of the nearest lamp thrown straight back: for brass, glass, varnish."""
        t = col(tint)
        L = self.L

        def g(X, Y, Z, n, iy, ix):
            out = 0.0
            for l in L.lamps:
                if l["id"] == "kitchen":
                    continue
                Lx, Ly, Lz = l["at"][0] - X, l["at"][1] - Y, l["at"][2] - Z
                d = np.sqrt(Lx * Lx + Ly * Ly + Lz * Lz) + 1e-6
                Vx, Vy, Vz = V.cam_x - X, V.eye - Y, V.cam_z - Z
                dv = np.sqrt(Vx * Vx + Vy * Vy + Vz * Vz) + 1e-6
                hx, hy, hz = Lx / d + Vx / dv, Ly / d + Vy / dv, Lz / d + Vz / dv
                hl = np.sqrt(hx * hx + hy * hy + hz * hz) + 1e-6
                s = np.clip((n[0] * hx + n[1] * hy + n[2] * hz) / hl, 0, 1) ** 24
                out = out + s * l["power"] * 220.0 ** 2 / (220.0 ** 2 + d * d)
            return (out * k)[..., None] * t
        return g

    def banister(self, lay):
        """The stair rail: white balusters, a dark handrail, newel posts at the foot and the top."""
        P = self.P
        x1 = SW
        zt, zf = ST["z_top"], ST["z_foot"]
        post = P(WHITE * 1.03)
        rail = P(self.wood(DARKWOOD * 1.25, 4.0, "Z"), gloss=self.shine(0.35))
        bal = P(WHITE * 1.02)

        def rail_y(Z):
            return (zf - Z) * PITCH + STEP_H + 88.0

        # newel at the foot (on the floor, just in front of the first step) and at the top
        for (zc, ybase, ytop) in ((zf + 10.0, 0.0, rail_y(zf + 10.0) + 16.0), (zt + 2.0, float(G), G + 106.0)):
            lay.box(x1 - 7, x1 + 5, ybase, ytop, zc - 6, zc + 6, post, TAG["stairs"])
            lay.box(x1 - 8.5, x1 + 6.5, ytop, ytop + 3, zc - 7.5, zc + 7.5, post, TAG["stairs"])
            lay.lathe(x1 - 1, zc, [(4.0, ytop + 3), (6.5, ytop + 8), (5.0, ytop + 13), (0.0, ytop + 15.5)], post, TAG["stairs"], sides=8)
        # the Son's cap, left on the newel at the foot of the stairs
        zc, ytop = zf + 10.0, rail_y(zf + 10.0) + 16.0 + 15.5
        cap = P(self.cloth((0.72, 0.16, 0.14), 4.0, fold=9.0, deep=0.18))
        lay.lathe(x1 - 1, zc, [(8.2, ytop - 6.0), (8.0, ytop - 2.5), (6.0, ytop + 1.5), (2.5, ytop + 3.6), (0.0, ytop + 4.0)], cap, TAG["stairs"], sides=10)
        lay.poly([(x1 + 3, ytop - 6.0, zc + 6.5), (x1 + 9, ytop - 6.6, zc + 13), (x1 + 2, ytop - 7.2, zc + 18.5), (x1 - 6, ytop - 6.6, zc + 15), (x1 - 6, ytop - 6.0, zc + 7.5)],
                 P((0.60, 0.12, 0.11)), TAG["stairs"])
        lay.disc((x1 - 1, ytop + 4.1, zc), 1.3, P((0.90, 0.88, 0.80)), TAG["stairs"], sides=6)
        # balusters: two to a tread
        for i in range(STEPS):
            y = STEP_H * (i + 1)
            for f in (0.28, 0.78):
                z = zf - STEP_D * (i + f)
                if z < zt + 9:
                    continue
                top = rail_y(z) - 3.0
                lay.ribbon((x1 - 3, y, z), (x1 - 3, top, z), 2.6, 2.6, bal, TAG["stairs"])
                lay.ribbon((x1 - 3, y + 22, z), (x1 - 3, y + 46, z), 4.4, 3.2, bal, TAG["stairs"])
        # the handrail, from newel to newel
        za, zb = zf + 4.0, zt + 8.0
        ya, yb = rail_y(za), rail_y(zb)
        lay.poly([(x1 - 6, ya, za), (x1 + 1, ya, za), (x1 + 1, yb, zb), (x1 - 6, yb, zb)], rail, TAG["stairs"])
        lay.poly([(x1 + 1, ya - 6, za), (x1 + 1, ya, za), (x1 + 1, yb, zb), (x1 + 1, yb - 6, zb)], P(self.wood(DARKWOOD * 0.95, 4.0, "Z")), TAG["stairs"])

    # ------------------------------------------------------------ the landing upstairs
    def gallery(self, lay):
        P = self.P
        zt = 175.0

        def top_alb(X, Y, Z, iy, ix):
            c = self.floor_alb(X + 3.0, Y, Z + 40.0, iy, ix) * 0.95
            run = (Z > 52) & (Z < 132) & (X > 20)
            red = RED[None, :] * (0.9 + 0.25 * fbm(X * 0.15, Z * 0.15, 8.0, 2))[:, None]
            c = np.where(run[:, None], red, c)
            c = np.where((run & ((Z < 58) | (Z > 126)))[:, None], BRASS[None, :] * 0.7, c)
            return c
        lay.poly([(0, G, 0), (XR, G, 0), (XR, G, zt), (0, G, zt)], P(top_alb, boxes=[(0, XR, G + 40, G + 44, 170, 180)]), TAG["rail"])

        def fascia_alb(X, Y, Z, iy, ix):
            px = pxcm(X, Z)
            c = np.broadcast_to(WHITE * 1.0, X.shape + (3,)).copy()
            c *= (1 - 0.30 * near(Y, G - 5.0, 0.7, px))[:, None]
            c *= (1 - 0.22 * near(Y, G - 13.0, 0.6, px))[:, None]
            c *= (0.95 + 0.1 * fbm(X * 0.02, Y * 0.2, 41.0, 2))[:, None]
            return c
        lay.poly([(SW, G - 18, zt), (XR, G - 18, zt), (XR, G, zt), (SW, G, zt)], P(fascia_alb), TAG["rail"])
        lay.poly([(SW, G - 22, zt + 2.5), (XR, G - 22, zt + 2.5), (XR, G - 17, zt + 2.5), (SW, G - 17, zt + 2.5)], P(WHITE * 0.92), TAG["rail"])     # a moulding under it
        lay.poly([(SW, G - 22, zt), (XR, G - 22, zt), (XR, G - 22, zt + 2.5), (SW, G - 22, zt + 2.5)], P(WHITE * 0.6), TAG["rail"])
        x = SW + 14.0                                          # a row of small blocks under the moulding, as old joinery has
        while x < FL["sampler"][2] - 14:                       # (they stop short of the sampler, so that nothing hangs in front of its words)
            lay.box(x, x + 7.5, G - 28.5, G - 22, zt, zt + 3.5, P(WHITE * 0.98), TAG["rail"])
            x += 26.0
        # brackets under the landing where it meets the walls
        for xa, xb in ((SW, SW + 7.0), (XR - 7.0, XR)):
            lay.poly([(xa, G - 22, zt + 2.6), (xb, G - 22, zt + 2.6), (xb, G - 62, zt + 2.6), (xa, G - 62, zt + 2.6)], P(WHITE * 0.95), TAG["rail"])
        # the railing: white balusters, newels, a dark handrail
        post = P(WHITE * 1.03)
        bal = P(WHITE * 1.02)
        rail = P(self.wood(DARKWOOD * 1.25, 6.0, "X"), gloss=self.shine(0.3))
        newels = [SW + 0.0, 276.0, 444.0, 612.0, XR - 6.0]
        for xn in newels[1:]:
            lay.box(xn - 5, xn + 5, G, G + 102, zt - 5, zt + 5, post, TAG["rail"])
            lay.box(xn - 6.5, xn + 6.5, G + 102, G + 105, zt - 6.5, zt + 6.5, post, TAG["rail"])
            lay.lathe(xn, zt, [(3.5, G + 105), (5.5, G + 109), (4.2, G + 113), (0.0, G + 115.5)], post, TAG["rail"], sides=8)
        x = SW + 12.0
        while x < XR - 8:
            if min(abs(x - xn) for xn in newels) > 8.0:
                lay.ribbon((x, G + 5, zt), (x, G + 88, zt), 2.5, 2.5, bal, TAG["rail"])
                lay.ribbon((x, G + 26, zt), (x, G + 50, zt), 4.4, 3.2, bal, TAG["rail"])
            x += 12.4
        lay.box(SW, XR, G + 2, G + 6, zt - 3.0, zt + 3.0, post, TAG["rail"])                                  # the shoe the balusters stand in
        lay.box(SW, XR, G + 88, G + 95, zt - 4.0, zt + 4.0, rail, TAG["rail"])

    def door_tex(self, wdt, hgt, kind):
        """A six-panelled painted door, drawn flat. `kind` says whose it is (what is stuck on it)."""
        T = Tex(wdt, hgt, 4.0, c255(WHITE * 0.99))
        dark, lite, field = c255(WHITE * 0.56), c255(WHITE * 1.10), c255(WHITE * 0.90)
        rows = [(12, 60), (72, 128), (140, hgt - 12)]
        for (v0, v1) in rows:
            for (u0, u1) in ((9, wdt / 2 - 4), (wdt / 2 + 4, wdt - 9)):
                T.rect(u0, v0, u1, v1, field)
                T.line([(u0, v1), (u1, v1)], dark, 1.8)
                T.line([(u0, v0), (u0, v1)], dark, 1.5)
                T.line([(u0, v0), (u1, v0)], lite, 1.2)
                T.line([(u1, v0), (u1, v1)], lite, 1.0)
        T.oval(wdt - 6.5, 98, 2.6, 2.6, c255(BRASS * 1.1))
        T.oval(wdt - 6.9, 98.6, 1.0, 1.0, c255((1.0, 0.95, 0.7)))
        rng = np.random.default_rng({"son": 3, "girls": 5, "study": 8}[kind])
        if kind == "son":                                     # a boy's notices, and a home-made sign in red
            for (u, v, w, h, c) in ((20, 150, 44, 22, (0.93, 0.90, 0.80)), (26, 124, 30, 18, (0.92, 0.80, 0.30)), (14, 84, 24, 30, (0.86, 0.90, 0.94)),
                                    (46, 86, 26, 20, (0.90, 0.60, 0.50)), (30, 44, 32, 24, (0.80, 0.90, 0.78))):
                T.rect(u, v, u + w, v + h, c255(c))
            T.rect(22, 152, 62, 170, c255((0.80, 0.16, 0.12)))
            T.rect(24, 154, 60, 168, c255((0.95, 0.92, 0.82)))
            T.line([(28, 164), (56, 164)], c255((0.80, 0.16, 0.12)), 2.0)
            T.line([(30, 158.5), (54, 158.5)], c255((0.80, 0.16, 0.12)), 2.0)
            T.rect(wdt - 17, 106, wdt - 4, 124, c255((0.34, 0.36, 0.40)))        # his toy alarm box, by the handle
            T.rect(wdt - 15, 108, wdt - 6, 117, c255((0.16, 0.18, 0.20)))
        elif kind == "girls":                                 # two name-plates: one tidy, one covered in stickers
            T.rect(14, 146, 40, 158, c255((0.94, 0.94, 0.90)))
            T.line([(18, 152), (36, 152)], c255(NAVY), 1.2)
            T.rect(46, 142, 74, 160, c255((0.96, 0.70, 0.78)))
            for _ in range(9):
                u, v = rng.uniform(47, 72), rng.uniform(143, 158)
                T.oval(u, v, 2.0, 2.0, c255(rng.choice([(0.98, 0.86, 0.30), (0.40, 0.75, 0.90), (0.60, 0.85, 0.45), (0.95, 0.45, 0.40)])))
        else:                                                 # Dad's notice, taped up: lines of block capitals
            T.rect(20, 120, 65, 160, c255((0.95, 0.93, 0.84)))
            for i, ln in enumerate((38, 34, 36, 34, 22)):
                T.line([(24, 153 - i * 6.5), (24 + ln, 153 - i * 6.5)], c255((0.16, 0.16, 0.20)), 1.6 if i == 0 else 1.0)
            T.rect(18, 157, 26, 161, c255((0.86, 0.80, 0.56)))
            T.rect(59, 157, 67, 161, c255((0.86, 0.80, 0.56)))
        return T

    def upstairs(self, lay):
        """Behind the railing: three doors, small frames, the hall table with a lamp left on, a hamper."""
        P = self.P
        for name, kind, tag in (("up-son", "son", "upson"), ("up-girls", "girls", "upgirls"), ("up-study", "study", "upstudy")):
            f = FL[name]
            x0, x1, y0, y1 = f[2], f[3], f[4], f[5]
            T = self.door_tex(x1 - x0, y1 - y0, kind)
            lay.poly([(x0, y0, 1.0), (x1, y0, 1.0), (x1, y1, 1.0), (x0, y1, 1.0)], P(lambda X, Y, Z, iy, ix, T=T, x0=x0, y0=y0: T.at(X - x0, Y - y0)), TAG[tag])
            trim = P(WHITE * 1.05)
            lay.box(x0 - 8, x0, y0, y1 + 8, 0, 3.5, trim, TAG[tag])
            lay.box(x1, x1 + 8, y0, y1 + 8, 0, 3.5, trim, TAG[tag])
            lay.box(x0 - 9, x1 + 9, y1, y1 + 9, 0, 4.5, trim, TAG[tag])
        # the hall table between the girls' door and the study, with the lamp
        wood = P(self.wood(DARKWOOD * 1.5, 3.0, "X"))
        lay.box(505, 590, G + 72, G + 78, 0, 32, wood)
        lay.box(508, 587, G + 58, G + 72, 2, 30, P(self.wood(DARKWOOD * 1.3, 3.0, "X")))
        for xx in (507, 584):
            lay.box(xx, xx + 4, G, G + 72, 26, 30, wood)
        lx, ly, lz = M.LIGHTS["upstairs"]
        lay.lathe(lx, lz, [(6.5, G + 78), (7.5, G + 80), (2.4, G + 85), (5.5, G + 93), (1.8, G + 100)], P(BRASS * 0.9, gloss=self.shine(0.4)), sides=8)
        shade = self.shade_paint((1.0, 0.80, 0.48), 2.0)
        lay.lathe(lx, lz, [(15.0, G + 99), (9.0, G + 121)], shade, sides=10)
        lay.disc((lx, G + 121, lz), 9.0, flat((1.9, 1.65, 1.05)), sides=10)
        lay.lathe(558, 15, [(5.0, G + 78), (9.0, G + 81.5)], P((0.42, 0.52, 0.66)), sides=8)                  # the bowl for keys
        lay.disc((558, G + 81.4, 15), 8.2, P(BRASS * 0.6), sides=8)
        # the hamper, and frames on the strip of wall
        lay.box(295, 345, G, G + 68, 2, 40, P(self.wicker((0.62, 0.48, 0.28))))
        lay.box(293, 347, G + 68, G + 73, 0, 42, P(self.wicker((0.56, 0.42, 0.24))))
        rng = np.random.default_rng(12)
        for (xa, ya, w, h, tone_) in ((300, G + 122, 26, 34, 0), (334, G + 132, 22, 22, 1), (360, G + 118, 22, 30, 2), (118, G + 120, 34, 26, 3),
                                      (150, G + 150, 20, 26, 4), (716, G + 150, 30, 24, 5)):
            self.photo(lay, "back", xa, ya, w, h, int(rng.integers(0, 99)), tone_)
        # a long strip of paper pinned up over the table (somebody's chart)
        lay.box(500, 595, G + 124, G + 162, 0, 1.2, P((0.86, 0.82, 0.70)))
        lay.box(503, 592, G + 127, G + 159, 1.2, 1.5, P(lambda X, Y, Z, iy, ix: np.where((np.abs(Y - (G + 143)) < 1.2)[:, None] | ((np.mod(X, 9.0) < 1.6) & (np.abs(Y - (G + 143)) < 6))[:, None], NAVY[None, :] * 1.2, CREAM[None, :] * 1.05)))

    def photo(self, lay, wall, a, y0, w, h, seed, kind=0):
        """A framed photograph: a frame, a mount, and blobs of the right colors (no faces)."""
        P = self.P
        rng = np.random.default_rng(seed)
        frame = [DARKWOOD * 1.3, BRASS * 0.8, (0.12, 0.11, 0.12), DARKWOOD * 2.0, (0.75, 0.72, 0.62), BRASS * 0.6][kind % 6]
        T = Tex(w, h, 6.0, c255(frame))
        T.rect(2.2, 2.2, w - 2.2, h - 2.2, c255((0.90, 0.87, 0.76)))
        m = 4.6 if min(w, h) > 20 else 3.4
        bg = [(0.36, 0.48, 0.60), (0.55, 0.45, 0.30), (0.30, 0.42, 0.30), (0.62, 0.56, 0.44), (0.42, 0.34, 0.44), (0.50, 0.60, 0.66)][int(rng.integers(0, 6))]
        T.rect(m, m, w - m, h - m, c255(bg))
        T.rect(m, m, w - m, m + (h - 2 * m) * 0.3, c255(col(bg) * 0.7))
        n = int(rng.integers(1, 4)) if w > 20 else 1
        for i in range(n):                                    # people: a head and shoulders, no more
            u = m + (w - 2 * m) * (i + 0.5) / n + rng.uniform(-1, 1)
            hv = m + (h - 2 * m) * rng.uniform(0.52, 0.66)
            r = min(w, h) * (0.13 if n > 1 else 0.17)
            shirt = [(0.80, 0.25, 0.22), (0.25, 0.35, 0.60), (0.90, 0.85, 0.70), (0.30, 0.50, 0.35), (0.85, 0.60, 0.25)][int(rng.integers(0, 5))]
            T.oval(u, m + r * 0.9, r * 1.7, r * 1.5 + (hv - m - r * 2.2) * 0.9, c255(shirt))
            T.oval(u, hv, r, r * 1.15, c255((0.86, 0.66, 0.52)))
            T.oval(u, hv + r * 0.75, r * 1.05, r * 0.6, c255([(0.30, 0.20, 0.12), (0.60, 0.45, 0.20), (0.16, 0.12, 0.10)][int(rng.integers(0, 3))]))
        T.rect(m, m, w - m, m + 0.01, c255(bg))
        if wall == "back":
            lay.box(a, a + w, y0, y0 + h, 0, 2.2, P(col(frame)), TAG.get("x", 0))
            lay.poly([(a, y0, 2.3), (a + w, y0, 2.3), (a + w, y0 + h, 2.3), (a, y0 + h, 2.3)], P(lambda X, Y, Z, iy, ix: T.at(X - a, Y - y0), gloss=self.glass()))
        else:                                                 # on the stair wall (X = 0): `a` runs along Z
            lay.box(0, 2.2, y0, y0 + h, a, a + w, P(col(frame)), TAG["photos"])
            lay.poly([(2.3, y0, a), (2.3, y0, a + w), (2.3, y0 + h, a + w), (2.3, y0 + h, a)], P(lambda X, Y, Z, iy, ix: T.at(a + w - Z, Y - y0), gloss=self.glass()), TAG["photos"])

    def glass(self, k=0.05):
        def g(X, Y, Z, n, iy, ix):
            s = np.clip(1 - np.abs(np.mod((X + Z) * 0.55 + Y * 0.9, 34.0) - 6.0) / 4.0, 0, 1)
            return (s * k)[:, None] * np.array([0.75, 0.85, 1.0], dtype=F32)
        return g

    def wicker(self, base):
        base = col(base)

        def alb(X, Y, Z, iy, ix):
            a = np.sin((X + Z) * 1.3) * np.sin(Y * 1.6 + np.floor((X + Z) / 2.4) * math.pi)
            return base[None, :] * (0.86 + 0.22 * a)[:, None]
        return alb

    def shade_paint(self, color, power=1.6, band=None):
        """A lit lampshade: it shines by itself, brightest round its middle; `band` darkens a trim at top and bottom."""
        c = col(color)

        def paint(X, Y, Z, n, iy, ix):
            ny = n[1] if np.ndim(n[1]) else np.full_like(X, n[1])
            # the side that faces us is the brightest (the bulb is behind the middle of it)
            vx, vz = V.cam_x - X, V.cam_z - Z
            vl = np.sqrt(vx * vx + vz * vz) + 1e-6
            facing = np.clip((n[0] * vx + n[2] * vz) / vl, 0, 1)
            k = power * (0.55 + 0.6 * facing ** 1.5)
            out = k[:, None] * c[None, :]
            if band is not None:
                lo, hi = band
                t = (Y - lo) / (hi - lo)
                out *= np.where((t < 0.10) | (t > 0.90), 0.55, 1.0)[:, None]
                out *= (0.80 + 0.35 * np.sin(np.clip(t, 0, 1) * math.pi))[:, None]
            return out
        return paint

    # ------------------------------------------------------------ the kitchen beyond its doorway
    def kitchen(self, lay):
        P = self.P
        k = FL["kitchen"]
        x0, x1, yh = k[2], k[3], k[5]
        tag = TAG["kitchen"]
        kw = dict(skip=("pendant", "reading", "piano", "upstairs", "glow"), moon=0.0, warm=1.6, cool=0.8, gain=0.66)

        def tiles(X, Y, Z, iy, ix):
            px = pxcm(X, Z)
            a, b = np.floor((X + Z) / 21.2), np.floor((X - Z) / 21.2)                      # laid on the diagonal
            chk = np.mod(a + b, 2) < 0.5
            c = np.where(chk[:, None], np.array([0.88, 0.83, 0.68], dtype=F32)[None, :], np.array([0.50, 0.62, 0.54], dtype=F32)[None, :])
            fa, fb = (X + Z) / 21.2 - a, (X - Z) / 21.2 - b
            j = np.clip(1 - np.minimum(np.minimum(fa, 1 - fa), np.minimum(fb, 1 - fb)) * 21.2 / np.maximum(0.6, 0.6 / px), 0, 1)
            return c * (1 - 0.3 * j)[:, None] * (0.95 + 0.1 * hash2(a, b, 2.0))[:, None]
        lay.poly([(60, 0, -330), (520, 0, -330), (520, 0, 0), (60, 0, 0)], P(tiles, **kw), tag)
        wallc = (0.92, 0.74, 0.40)

        def kwall(X, Y, Z, iy, ix):
            px = pxcm(X, Z)
            c = np.broadcast_to(col(wallc), X.shape + (3,)).copy()
            tile = (Y > 90) & (Y < 150)                                                         # white tiles behind the counter
            ju = near(np.mod(X, 15.0), 0.0, 0.5, px, 0.4) + near(np.mod(Y - 90, 15.0), 0.0, 0.5, px, 0.4)
            c = np.where(tile[:, None], np.array([0.90, 0.90, 0.84], dtype=F32)[None, :] * (1 - 0.22 * np.clip(ju, 0, 1))[:, None], c)
            return c
        lay.poly([(60, 0, -320), (520, 0, -320), (520, 260, -320), (60, 260, -320)], P(kwall, **kw), tag)
        lay.poly([(150, 0, -320), (150, 0, 0), (150, 260, 0), (150, 260, -320)], P(wallc, **kw), tag)
        # the reveal of the doorway (the thickness of the wall), bright on the side the kitchen lights
        lay.poly([(x0, 0, -15), (x0, 0, 0), (x0, yh, 0), (x0, yh, -15)], P(WHITE * 1.05, **kw), tag)
        lay.poly([(x1, 0, -15), (x1, 0, 0), (x1, yh, 0), (x1, yh, -15)], P(WHITE * 1.05, **kw), tag)
        lay.poly([(x0, yh, -15), (x1, yh, -15), (x1, yh, 0), (x0, yh, 0)], P(WHITE * 1.0, **kw), tag)
        lay.poly([(x0, 0.5, -15), (x1, 0.5, -15), (x1, 0.5, 2), (x0, 0.5, 2)], P(self.wood(OAK * 0.8, 9.0, "X"), **kw), tag)     # the threshold
        # the fridge: its corner, with drawings held on by magnets
        fr = (176, 246, 0, 178, -320, -250)
        T = Tex(70, 178, 4.0, c255((0.90, 0.91, 0.88)))
        T.line([(0, 118), (70, 118)], c255((0.55, 0.57, 0.58)), 0.9)
        T.rect(60, 124, 63, 160, c255((0.62, 0.64, 0.66)))
        T.rect(60, 72, 63, 110, c255((0.62, 0.64, 0.66)))
        rng = np.random.default_rng(7)
        for (u, v, w, h, c) in ((22, 126, 26, 34, (0.97, 0.96, 0.90)), (30, 70, 28, 36, (0.95, 0.94, 0.86)), (20, 28, 30, 30, (0.96, 0.92, 0.80))):
            T.poly([(u, v), (u + w, v + 2), (u + w - 1, v + h + 1), (u - 1, v + h)], c255(c))
            for _ in range(7):                                # crayon
                cc = [(0.90, 0.25, 0.20), (0.20, 0.45, 0.85), (0.95, 0.78, 0.15), (0.25, 0.65, 0.30), (0.85, 0.40, 0.70)][int(rng.integers(0, 5))]
                ua, va = u + rng.uniform(3, w - 3), v + rng.uniform(3, h - 3)
                T.line([(ua, va), (ua + rng.uniform(-8, 8), va + rng.uniform(-8, 8))], c255(cc), 1.6)
            T.oval(u + w / 2, v + h - 1, 1.8, 1.8, c255([(0.9, 0.2, 0.2), (0.2, 0.4, 0.8), (0.95, 0.8, 0.2)][int(rng.integers(0, 3))]))
        T.rect(26, 78, 50, 90, c255((0.85, 0.20, 0.16)))      # one is plainly a red car
        T.oval(31, 78, 3, 3, c255((0.1, 0.1, 0.1)))
        T.oval(45, 78, 3, 3, c255((0.1, 0.1, 0.1)))
        Ts = Tex(70, 178, 3.0, c255((0.84, 0.86, 0.84)))
        for (u, v, w, h, c) in ((16, 120, 30, 30, (0.96, 0.95, 0.88)), (22, 60, 26, 34, (0.94, 0.90, 0.80))):
            Ts.rect(u, v, u + w, v + h, c255(c))
            for _ in range(6):
                cc = [(0.90, 0.25, 0.20), (0.20, 0.45, 0.85), (0.95, 0.78, 0.15), (0.25, 0.65, 0.30)][int(rng.integers(0, 4))]
                ua, va = u + rng.uniform(3, w - 3), v + rng.uniform(3, h - 3)
                Ts.line([(ua, va), (ua + rng.uniform(-8, 8), va + rng.uniform(-8, 8))], c255(cc), 1.8)
        lay.box(*fr, P((0.88, 0.89, 0.86), **kw), tag, paints={
            "front": P(lambda X, Y, Z, iy, ix: T.at(X - fr[0], Y), **kw),
            "right": P(lambda X, Y, Z, iy, ix: Ts.at(Z - fr[4], Y), **kw)})
        # the counter along the back, cupboards under it and over it, the kettle
        def cup(X, Y, Z, iy, ix):
            c = np.broadcast_to(col((0.90, 0.88, 0.78)), X.shape + (3,)).copy()
            u = np.mod(X - 246, 46.0)
            lo = Y < 90
            c *= panel(u, Y, 5.0, 41.0, np.where(lo, 12.0, 156.0), np.where(lo, 76.0, 224.0), 2.5)[:, None]
            knob = np.hypot(u - 38.0, Y - np.where(lo, 70.0, 162.0)) < 2.0
            return np.where(knob[:, None], BRASS[None, :], c)
        lay.box(246, 500, 0, 86, -320, -262, P(cup, **kw), tag)
        lay.box(244, 500, 86, 91, -320, -258, P(self.wood(OAK * 1.05, 14.0, "X"), **kw), tag)
        lay.box(246, 500, 152, 232, -320, -288, P(cup, **kw), tag)
        kx, kz = 296.0, -292.0
        kettle = P((0.80, 0.22, 0.16), gloss=self.shine(0.6), **kw)
        lay.lathe(kx, kz, [(10.5, 91), (11.5, 97), (10.0, 106), (5.0, 111), (1.5, 113), (0.0, 114)], kettle, tag, sides=10)
        lay.tube([(kx + 9, 100, kz + 2), (kx + 16, 106, kz + 4), (kx + 19, 110, kz + 5)], 3.0, kettle, tag)
        lay.tube([(kx - 6, 111, kz), (kx - 2, 120, kz), (kx + 5, 120, kz), (kx + 8, 111, kz)], 1.6, P((0.10, 0.10, 0.12), **kw), tag)
        for i, (cx, h, c) in enumerate(((336, 17, (0.90, 0.88, 0.78)), (352, 21, (0.90, 0.88, 0.78)), (370, 26, (0.90, 0.88, 0.78)))):       # canisters
            lay.lathe(cx, -296, [(6.5, 91), (6.5, 91 + h), (0.0, 91 + h + 1)], P(c, **kw), tag, sides=8)
            lay.lathe(cx, -296, [(6.8, 91 + h * 0.45), (6.8, 91 + h * 0.62)], P((0.25, 0.42, 0.62), **kw), tag, sides=8)
        lay.box(270, 276, 118, 146, -319, -317, P((0.86, 0.30, 0.22), **kw), tag)                             # a tea towel on a hook
        # a calendar on the side wall
        lay.poly([(150.6, 120, -210), (150.6, 120, -170), (150.6, 176, -170), (150.6, 176, -210)], P((0.95, 0.94, 0.88), **kw), tag)
        lay.poly([(150.8, 150, -208), (150.8, 150, -172), (150.8, 174, -172), (150.8, 174, -208)], P((0.30, 0.55, 0.75), **kw), tag)

    # ------------------------------------------------------------ on the back wall, under the landing
    def doorway_trim(self, lay):
        P = self.P
        k = FL["kitchen"]
        x0, x1, yh = k[2], k[3], k[5]
        trim = P(WHITE * 1.04, plane="back")
        lay.box(x0 - 9, x0, 0, yh + 9, 0, 3.5, trim, TAG["kitchen"])
        lay.box(x1, x1 + 9, 0, yh + 9, 0, 3.5, trim, TAG["kitchen"])
        lay.box(x0 - 11, x1 + 11, yh, yh + 11, 0, 5.0, trim, TAG["kitchen"])

    def bookcase(self, lay):
        """Mom's bookcase: tall, full: biographies, plays, a hymnal."""
        P = self.P
        x0, x1, y0, y1, z0, z1 = BX["books"]
        tag = TAG["books"]
        wood = P(self.wood(DARKWOOD * 1.55, 2.0, "Y"), plane=None)
        dark = P(DARKWOOD * 0.45)
        lay.box(x0, x0 + 3.5, 0, y1, z0, z1, wood, tag)
        lay.box(x1 - 3.5, x1, 0, y1, z0, z1, wood, tag)
        lay.box(x0 - 2, x1 + 2, y1, y1 + 4, z0, z1 + 2, wood, tag)
        lay.box(x0, x1, 0, 9, z0, z1 - 1, wood, tag)
        lay.poly([(x0, 0, z0 + 3), (x1, 0, z0 + 3), (x1, y1, z0 + 3), (x0, y1, z0 + 3)], dark, tag)
        shelves = [9.0, 50.0, 86.0, 120.0, 153.0, 185.0, y1]
        rng = np.random.default_rng(31)
        hues = [(0.50, 0.14, 0.12), (0.16, 0.26, 0.42), (0.20, 0.36, 0.24), (0.62, 0.48, 0.26), (0.72, 0.66, 0.50), (0.36, 0.20, 0.12),
                (0.56, 0.30, 0.14), (0.28, 0.30, 0.36), (0.60, 0.20, 0.26), (0.30, 0.42, 0.50), (0.80, 0.74, 0.60), (0.42, 0.14, 0.20)]
        for si, (ya, yb) in enumerate(zip(shelves[:-1], shelves[1:])):
            if si:
                lay.box(x0 + 3.5, x1 - 3.5, ya - 3, ya, z0 + 3, z1 - 1.5, wood, tag)
            gap = yb - ya - (3 if si < len(shelves) - 2 else 0)
            x = x0 + 4.5
            while x < x1 - 7:
                wd = rng.uniform(2.6, 6.0)
                if x + wd > x1 - 4.5:
                    break
                r = rng.random()
                if r < 0.06 and x + 16 < x1 - 5:              # a few lie flat in a pile
                    yy = ya
                    for _ in range(int(rng.integers(2, 5))):
                        th = rng.uniform(2.5, 5.0)
                        c = col(hues[int(rng.integers(0, len(hues)))]) * rng.uniform(0.8, 1.15)
                        lay.box(x, x + rng.uniform(13, 16), yy, yy + th, z0 + 8, z1 - 3 - rng.uniform(0, 3), P(c), tag)
                        yy += th
                    x += 17
                    continue
                if r > 0.955:                                 # a gap where one has been taken out
                    x += rng.uniform(3, 7)
                    continue
                hgt = gap * rng.uniform(0.66, 0.94) - 2
                c = col(hues[int(rng.integers(0, len(hues)))]) * rng.uniform(0.75, 1.2)
                zf = z1 - 2.5 - rng.uniform(0, 4.5)
                band = rng.random()

                def spine(X, Y, Z, iy, ix, c=c, ya=ya, hgt=hgt, band=band, x=x, wd=wd):
                    t = (Y - ya) / hgt
                    out = np.broadcast_to(c, X.shape + (3,)).copy()
                    if band < 0.55:                           # gilt bands and a title block
                        g = ((np.abs(t - 0.82) < 0.035) | (np.abs(t - 0.16) < 0.03))
                        out = np.where(g[:, None], BRASS[None, :] * 0.95, out)
                    if band > 0.35 and wd > 3.6:
                        g = (t > 0.52) & (t < 0.72) & (np.abs(X - (x + wd / 2)) < wd * 0.33)
                        out = np.where(g[:, None], (CREAM * 0.9 if band > 0.7 else c * 0.55)[None, :], out)
                    return out
                lay.box(x, x + wd, ya, ya + hgt, z0 + 6, zf, P(c * 0.9), tag, paints={"front": P(spine, mott=(self.mott2, 0.12)), "top": P(CREAM * 0.8)})
                x += wd + rng.uniform(0.0, 0.5)
        # on top: a trailing ivy in a pot, a small flag in a stand, a pile of books
        lay.lathe(x0 + 26, z0 + 17, [(7.0, y1 + 4), (9.5, y1 + 20), (8.5, y1 + 21)], P((0.62, 0.34, 0.22)), tag, sides=8)
        leaf = [(0.16, 0.34, 0.18), (0.22, 0.44, 0.22), (0.12, 0.26, 0.16)]
        for i in range(34):
            a = rng.uniform(0, 2 * math.pi)
            r = rng.uniform(2, 17)
            cx, cz = x0 + 26 + math.cos(a) * r, z0 + 17 + math.sin(a) * r * 0.6
            cy = y1 + 24 + rng.uniform(-3, 9) - max(0, r - 9) * rng.uniform(1.0, 3.6)
            lay.disc((cx, cy, min(cz, z1 + 6)), rng.uniform(2.2, 3.8), P(col(leaf[i % 3]) * rng.uniform(0.8, 1.3)), tag, axis="Z", sides=6, squash=0.8)
        yy = y1 + 4
        for (w, th, c) in ((30, 5, hues[0]), (27, 4, hues[4]), (24, 6, hues[1])):
            lay.box(x1 - 52, x1 - 52 + w, yy, yy + th, z0 + 5, z0 + 26, P(col(c)), tag)
            yy += th
        lay.lathe(x1 - 14, z0 + 16, [(5, y1 + 4), (5, y1 + 6), (0.8, y1 + 8), (0.8, y1 + 36)], P(BRASS * 0.8), tag, sides=6)   # a small flag in a brass stand
        T = Tex(20, 13, 6.0, c255((0.80, 0.80, 0.78)))
        for i in range(7):
            if i % 2 == 0:
                T.rect(0, 13 - (i + 1) * 13 / 7.0, 20, 13 - i * 13 / 7.0, c255((0.70, 0.16, 0.16)))
        T.rect(0, 6, 8.5, 13, c255((0.14, 0.20, 0.42)))
        lay.poly([(x1 - 13.2, y1 + 22, z0 + 16.5), (x1 + 6.8, y1 + 20.5, z0 + 19), (x1 + 6.8, y1 + 33.5, z0 + 19), (x1 - 13.2, y1 + 35, z0 + 16.5)],
                 P(lambda X, Y, Z, iy, ix: T.at(X - (x1 - 13.2), Y - (y1 + 21.5))), tag)

    def print_frame(self, lay):
        """The framed Preamble: a parchment sheet in a dark frame. (Its three large words are lettered at the end.)"""
        P = self.P
        f = FL["frame"]
        x0, x1, y0, y1 = f[2], f[3], f[4], f[5]
        lay.box(x0, x1, y0, y1, 0, 3.2, P(self.wood(DARKWOOD * 1.1, 8.0, "Y"), gloss=self.shine(0.2), plane="back"), TAG["frame"])
        lay.box(x0 + 3.5, x1 - 3.5, y0 + 3.5, y1 - 3.5, 3.2, 3.5, P(BRASS * 0.85, plane="back"), TAG["frame"])

        def sheet(X, Y, Z, iy, ix):
            px = pxcm(X, Z)
            c = np.broadcast_to(col((0.86, 0.76, 0.52)), X.shape + (3,)).copy() * (0.90 + 0.18 * fbm(X * 0.06, Y * 0.06, 77.0, 3))[:, None]
            # the body of the writing: close lines of a clerk's hand, below the three large words
            body = (Y < y1 - 46) & (Y > y0 + 16) & (X > x0 + 11) & (X < x1 - 11)
            ln = np.mod(y1 - 46 - Y, 5.4)
            ink = body & (ln < np.maximum(1.5, 0.7 / px)) & (vnoise(X * 0.9, np.floor((y1 - Y) / 5.4) * 7.0, 3.0) > 0.26)
            c = np.where(ink[:, None], c * np.array([0.50, 0.42, 0.34], dtype=F32), c)
            sig = (Y < y0 + 14) & (Y > y0 + 9) & (X > x0 + 30) & (X < x1 - 14) & (vnoise(X * 0.5, Y * 0.9, 9.0) > 0.5)
            c = np.where(sig[:, None], c * 0.6, c)
            return c
        lay.poly([(x0 + 5, y0 + 5, 3.6), (x1 - 5, y0 + 5, 3.6), (x1 - 5, y1 - 5, 3.6), (x0 + 5, y1 - 5, 3.6)], P(sheet, plane="back", warm=3.0, cool=1.4), TAG["frame"])

    def clock(self, lay):
        """A round wall clock at twenty to ten."""
        P = self.P
        f = FL["clock"]
        cx, cy, r = (f[2] + f[3]) / 2, (f[4] + f[5]) / 2, (f[3] - f[2]) / 2
        tag = TAG["clock"]
        lay.disc((cx, cy, 3.0), r, P(self.wood(DARKWOOD * 1.5, 5.0, "X"), gloss=self.shine(0.25), plane="back"), tag, axis="Z", sides=20)
        lay.disc((cx, cy, 3.4), r - 3.0, P(BRASS * 0.9, plane="back"), tag, axis="Z", sides=20)

        def face(X, Y, Z, iy, ix):
            dx, dy = X - cx, Y - cy
            rr = np.hypot(dx, dy)
            ang = np.mod(np.degrees(np.arctan2(dx, dy)), 360.0)
            c = np.broadcast_to(col((0.95, 0.92, 0.80)), X.shape + (3,)).copy()
            tick = (rr > (r - 3.8) * 0.74) & (rr < (r - 3.8) * 0.93) & (np.abs(np.mod(ang + 15.0, 30.0) - 15.0) < np.where(np.abs(np.mod(ang + 45.0, 90.0) - 45.0) < 4, 5.0, 2.6))
            return np.where(tick[:, None], np.array([0.10, 0.09, 0.10], dtype=F32)[None, :], c)
        lay.disc((cx, cy, 3.8), r - 3.8, P(face, plane="back"), tag, axis="Z", sides=20)
        ink = flat((0.06, 0.05, 0.06))
        for ang, ln, wd in ((290.0, (r - 3.8) * 0.52, 1.9), (240.0, (r - 3.8) * 0.80, 1.3)):                  # twenty to ten
            a = math.radians(ang)
            lay.ribbon((cx - math.sin(a) * 1.5, cy - math.cos(a) * 1.5, 4.2), (cx + math.sin(a) * ln, cy + math.cos(a) * ln, 4.2), wd, wd * 0.8, ink, tag)
        lay.disc((cx, cy, 4.4), 1.3, flat((0.35, 0.26, 0.10)), tag, axis="Z", sides=8)

    def front_door(self, lay):
        """The front door: solid, painted red, a fan of night-blue glass in its head; a mat; the sampler's frame over it."""
        P = self.P
        f = FL["door"]
        x0, x1, y1 = f[2], f[3], f[5]
        tag = TAG["door"]
        wd, hg = (x1 - 6) - (x0 + 6), y1 - 6
        T = Tex(wd, hg, 4.0, c255((0.50, 0.11, 0.10)))
        red_d, red_l, field = c255((0.33, 0.06, 0.06)), c255((0.64, 0.19, 0.15)), c255((0.46, 0.10, 0.09))
        for (v0, v1) in ((10, 62), (72, 136)):
            for (u0, u1) in ((8, wd / 2 - 4), (wd / 2 + 4, wd - 8)):
                T.rect(u0, v0, u1, v1, field)
                T.line([(u0, v1), (u1, v1)], red_d, 1.4)
                T.line([(u0, v0), (u0, v1)], red_d, 1.1)
                T.line([(u0, v0), (u1, v0)], red_l, 1.1)
                T.line([(u1, v0), (u1, v1)], red_l, 0.9)
        # the fanlight: a half round of small panes with the night in them
        fu, fv, fr = wd / 2, 146.0, 33.0
        pts = [(fu + math.cos(math.radians(a)) * (fr + 3), fv + math.sin(math.radians(a)) * (fr + 3)) for a in range(0, 181, 12)]
        T.poly(pts, c255(WHITE * 0.95))
        pts = [(fu + math.cos(math.radians(a)) * fr, fv + 2 + math.sin(math.radians(a)) * (fr - 2)) for a in range(0, 181, 12)]
        T.poly(pts, c255((0.10, 0.18, 0.40)))
        T.oval(fu + 12, fv + 16, 3.0, 3.0, c255((0.30, 0.42, 0.66)))
        for a in (36, 72, 108, 144):
            T.line([(fu, fv + 2), (fu + math.cos(math.radians(a)) * fr, fv + 2 + math.sin(math.radians(a)) * (fr - 2))], c255(WHITE * 0.95), 1.6)
        pts = [(fu + math.cos(math.radians(a)) * 11, fv + 2 + math.sin(math.radians(a)) * 11) for a in range(0, 181, 15)]
        T.line(pts, c255(WHITE * 0.95), 1.5)
        T.oval(wd - 8, 100, 3.2, 3.2, c255(BRASS * 1.1))      # the knob, its plate, the letter-slot
        T.oval(wd - 8.6, 100.8, 1.2, 1.2, c255((1.0, 0.96, 0.72)))
        T.rect(wd - 10.5, 108, wd - 5.5, 116, c255(BRASS * 0.8))
        T.rect(wd / 2 - 13, 66, wd / 2 + 13, 70.5, c255(BRASS * 0.9))
        T.rect(wd / 2 - 11, 67.4, wd / 2 + 11, 69.2, c255((0.10, 0.08, 0.06)))
        lay.poly([(x0 + 6, 0, 1.6), (x1 - 6, 0, 1.6), (x1 - 6, hg, 1.6), (x0 + 6, hg, 1.6)],
                 P(lambda X, Y, Z, iy, ix: T.at(X - (x0 + 6), Y), plane="back", gloss=self.shine(0.10)), tag)
        trim = P(WHITE * 1.04, plane="back")
        lay.box(x0, x0 + 6, 0, y1, 0, 4.0, trim, tag)
        lay.box(x1 - 6, x1, 0, y1, 0, 4.0, trim, tag)
        lay.box(x0 - 2, x1 + 2, hg, y1, 0, 5.0, trim, tag)
        # the mat
        def mat(X, Y, Z, iy, ix):
            c = np.broadcast_to(col((0.50, 0.36, 0.20)), X.shape + (3,)).copy() * (0.8 + 0.4 * vnoise(X * 0.9, Z * 0.9, 5.0))[:, None]
            edge = np.minimum(np.minimum(X - (x0 + 12), (x1 - 12) - X), np.minimum(Z - 10, 56 - Z))
            return np.where((edge < 4)[:, None], c * 0.6, c)
        lay.poly([(x0 + 12, 0.8, 10), (x1 - 12, 0.8, 10), (x1 - 12, 0.8, 56), (x0 + 12, 0.8, 56)], P(mat, plane="floor"), tag)
        # the sampler over the door: its frame and its linen (the stitched words are lettered at the end)
        s = FL["sampler"]
        lay.box(s[2], s[3], s[4], s[5], 0, 3.0, P(self.wood(DARKWOOD * 1.3, 12.0, "X"), plane="back"), TAG["sampler"])

        def linen(X, Y, Z, iy, ix):
            return np.broadcast_to(col((0.90, 0.85, 0.70)), X.shape + (3,)) * (0.94 + 0.10 * vnoise(X * 1.5, Y * 1.5, 8.0))[:, None]
        lay.poly([(s[2] + 3, s[4] + 3, 3.2), (s[3] - 3, s[4] + 3, 3.2), (s[3] - 3, s[5] - 3, 3.2), (s[2] + 3, s[5] - 3, 3.2)], P(linen, plane="back"), TAG["sampler"])

    def coats(self, lay):
        """Coats on hooks beside the front door, on the right-hand wall; boots under them; an umbrella in the corner."""
        P = self.P
        tag = TAG["coats"]
        lay.box(XR - 2.5, XR, 172, 180, 18, 156, P(self.wood(DARKWOOD * 1.4, 2.0, "Z")), tag)
        for (zc, y0, wdt, thick, c, hood) in ((48, 82, 40, 20, (0.16, 0.22, 0.40), False), (92, 74, 44, 22, (0.62, 0.52, 0.34), False),
                                              (132, 112, 30, 15, (0.92, 0.74, 0.16), True)):
            cl = P(self.cloth(c, zc * 0.1, fold=9.0, deep=0.30))
            out = [(XR, zc - wdt / 2), (XR - thick * 0.7, zc - wdt / 2 + 3), (XR - thick, zc), (XR - thick * 0.7, zc + wdt / 2 - 3), (XR, zc + wdt / 2)]
            lay.prism(out, y0, 162, cl, tag, cap=False)
            top = [(XR, zc - wdt / 2 + 6), (XR - thick * 0.5, zc - wdt / 2 + 9), (XR - thick * 0.6, zc), (XR - thick * 0.5, zc + wdt / 2 - 9), (XR, zc + wdt / 2 - 6)]
            lay.prism(top, 162, 173, cl, tag, top=P(col(c) * 0.8))
            if hood:
                lay.lathe(XR - 7, zc, [(8, 160), (9, 168), (5, 176)], P(col(c) * 0.9), tag, sides=6)
        lay.lathe(XR - 9, 92, [(11, 176), (11.5, 178), (6, 180), (6, 187), (0, 188)], P((0.34, 0.26, 0.18)), tag, sides=8)   # a hat
        for (zc, c, h) in ((44, (0.22, 0.14, 0.10), 26), (60, (0.22, 0.14, 0.10), 26), (120, (0.86, 0.72, 0.12), 20), (134, (0.86, 0.72, 0.12), 20)):
            lay.box(XR - 24, XR - 4, 0, 9, zc - 5, zc + 5, P(col(c)), tag)
            lay.box(XR - 14, XR - 4, 9, h, zc - 5, zc + 5, P(col(c) * 0.9), tag)
        lay.ribbon((XR - 6, 0, 8), (XR - 3, 92, 3), 3.4, 2.2, P((0.12, 0.30, 0.26)), tag)                     # the umbrella
        lay.ribbon((XR - 3, 92, 3), (XR - 3, 104, 3), 1.2, 1.2, P(DARKWOOD), tag)

    def stair_photos(self, lay):
        """Family photographs in frames, climbing the wall beside the stairs."""
        rng = np.random.default_rng(3)
        zf = ST["z_foot"]
        spots = [(596, 14, 22, 28), (566, 30, 20, 24), (538, 22, 26, 20), (540, 52, 20, 26), (508, 44, 24, 30), (478, 40, 22, 22),
                 (480, 70, 28, 22), (448, 62, 22, 28), (424, 60, 18, 22), (420, 90, 26, 20)]
        for i, (z, up, w, h) in enumerate(spots):
            base = max(0.0, (zf - (z + w / 2)) * PITCH + STEP_H)
            self.photo(lay, "left", z, base + 118 + up, w, h, int(rng.integers(0, 999)), i)

    def painting(self, lay):
        """A landscape in a gilt frame, high on the stair wall: hills, a lake, an evening sky."""
        P = self.P
        z0, z1, y0, y1 = 452.0, 548.0, 338.0, 408.0
        w, h = z1 - z0, y1 - y0
        T = Tex(w, h, 5.0, c255((0.82, 0.62, 0.40)))
        for i in range(12):                                   # the sky: peach low down, blue-green above
            t = i / 11.0
            T.rect(0, h * (0.42 + 0.58 * t), w, h, c255(lerp(np.array([0.90, 0.66, 0.42]), np.array([0.30, 0.46, 0.56]), t)))
        T.poly([(0, h * 0.42), (w * 0.18, h * 0.60), (w * 0.34, h * 0.50), (w * 0.52, h * 0.70), (w * 0.74, h * 0.48), (w, h * 0.58), (w, h * 0.30), (0, h * 0.30)], c255((0.30, 0.34, 0.46)))
        T.poly([(0, h * 0.36), (w * 0.3, h * 0.44), (w * 0.62, h * 0.38), (w, h * 0.46), (w, h * 0.2), (0, h * 0.2)], c255((0.18, 0.28, 0.24)))
        T.rect(0, 0, w, h * 0.26, c255((0.50, 0.56, 0.60)))                                                   # the lake
        T.rect(w * 0.2, h * 0.14, w * 0.7, h * 0.17, c255((0.86, 0.72, 0.56)))
        T.poly([(0, 0), (0, h * 0.20), (w * 0.22, h * 0.12), (w * 0.36, 0)], c255((0.12, 0.18, 0.14)))
        T.line([(w * 0.84, h * 0.10), (w * 0.84, h * 0.56)], c255((0.10, 0.12, 0.10)), 1.2)                 # one dark pine
        T.poly([(w * 0.76, h * 0.26), (w * 0.84, h * 0.62), (w * 0.92, h * 0.26)], c255((0.10, 0.16, 0.12)))
        gilt = P(BRASS * 0.95, gloss=self.shine(0.5), plane="left")
        lay.box(0, 4.0, y0 - 8, y1 + 8, z0 - 8, z1 + 8, gilt, TAG["photos"])
        lay.box(4.0, 5.2, y0 - 4, y1 + 4, z0 - 4, z1 + 4, P(BRASS * 0.55, plane="left"), TAG["photos"])
        lay.poly([(5.3, y0, z0), (5.3, y0, z1), (5.3, y1, z1), (5.3, y1, z0)], P(lambda X, Y, Z, iy, ix: T.at(z1 - Z, Y - y0), plane="left", cool=2.2), TAG["photos"])

    def rug(self, lay):
        """The big worn rug in the middle of the floor."""
        x0, x1, _, _, z0, z1 = BX["rug"]
        w, d = x1 - x0, z1 - z0
        T = Tex(w, d, 3.0, c255(RED * 0.95))
        navy, cream, gold, red2 = c255(NAVY * 1.05), c255(CREAM * 0.92), c255(BRASS * 0.85), c255(RED * 0.72)
        T.rect(0, 0, w, d, navy)                              # borders, from the outside in
        T.rect(5, 5, w - 5, d - 5, cream)
        T.rect(8, 8, w - 8, d - 8, navy)
        T.rect(26, 26, w - 26, d - 26, gold)
        T.rect(29, 29, w - 29, d - 29, c255(RED * 0.95))
        n = 15
        for i in range(n):                                    # a running pattern in the wide border
            for (u, v) in ((26 + (w - 52) * (i + 0.5) / n, 17), (26 + (w - 52) * (i + 0.5) / n, d - 17)):
                T.poly([(u - 7, v), (u, v + 6), (u + 7, v), (u, v - 6)], cream if i % 2 else gold)
                T.poly([(u - 3.5, v), (u, v + 3), (u + 3.5, v), (u, v - 3)], c255(RED))
        m = 11
        for i in range(m):
            for (u, v) in ((17, 26 + (d - 52) * (i + 0.5) / m), (w - 17, 26 + (d - 52) * (i + 0.5) / m)):
                T.poly([(u - 6, v), (u, v + 7), (u + 6, v), (u, v - 7)], cream if i % 2 else gold)
                T.poly([(u - 3, v), (u, v + 3.5), (u + 3, v), (u, v - 3.5)], c255(RED))
        for (u, v) in ((17, 17), (w - 17, 17), (17, d - 17), (w - 17, d - 17)):
            T.rect(u - 6, v - 6, u + 6, v + 6, gold)
            T.rect(u - 3, v - 3, u + 3, v + 3, navy)
        cu, cv = w / 2, d / 2                                  # the field: a great medallion and quarter ones in the corners
        for k, c in ((1.0, navy), (0.86, cream), (0.80, c255(NAVY * 1.3)), (0.56, gold), (0.50, c255(RED * 1.05)), (0.26, cream), (0.2, navy)):
            T.poly([(cu - 92 * k, cv), (cu, cv + 66 * k), (cu + 92 * k, cv), (cu, cv - 66 * k)], c)
        for (u, v) in ((29, 29), (w - 29, 29), (29, d - 29), (w - 29, d - 29)):
            su, sv = (1 if u < cu else -1), (1 if v < cv else -1)
            T.poly([(u, v), (u + su * 46, v), (u, v + sv * 34)], navy)
            T.poly([(u, v), (u + su * 36, v), (u, v + sv * 26)], gold)
            T.poly([(u, v), (u + su * 30, v), (u, v + sv * 21)], red2)
        rng = np.random.default_rng(8)
        for _ in range(70):                                   # small flowers scattered over the field
            u, v = rng.uniform(34, w - 34), rng.uniform(34, d - 34)
            if abs(u - cu) / 92 + abs(v - cv) / 66 < 1.12:
                continue
            T.oval(u, v, 2.4, 2.4, cream if rng.random() < 0.5 else gold)
            T.oval(u, v, 1.0, 1.0, navy)
        T.array()

        def alb(X, Y, Z, iy, ix):
            px = pxcm(X, Z)
            c = T.at(X - x0, Z - z0)
            wear = fbm((X - x0) * 0.016, (Z - z0) * 0.016, 23.0, 3)                                           # worn where they walk
            lane = np.exp(-((X - (x0 + w * 0.42)) / 80.0) ** 2) * 0.6 + 0.35
            k = np.clip((wear - 0.38) * 2.4, 0, 1) * lane
            tan = np.array([0.62, 0.50, 0.38], dtype=F32)[None, :]
            c = c + (tan - c) * (k * 0.60)[:, None]
            bare = (vnoise((X - x0) * 0.045, (Z - z0) * 1.3, 29.0) > 0.70) * k                              # threadbare along the weave
            c = c + (tan * 1.08 - c) * (bare * 0.45)[:, None]
            grey = c @ np.array([0.3, 0.55, 0.15], dtype=F32)                                                 # and all of it a little faded
            c = c + (grey[:, None] - c) * 0.10
            c = c * (0.90 + 0.2 * vnoise(X * 0.7, Z * 0.7, 2.0))[:, None]                                       # the pile
            return c
        lay.poly([(x0, 0.9, z0), (x1, 0.9, z0), (x1, 0.9, z1), (x0, 0.9, z1)], self.P(alb, plane="floor", mott=(self.mott, 0.10), moon=1.9), TAG["rug"])
        fr = self.P(CREAM * 0.9, plane="floor")
        for x in np.arange(x0 + 1.5, x1, 3.2):                # the fringe at both ends
            lay.ribbon((x, 0.7, z0), (x + 0.6, 0.7, z0 - 6.5), 1.3, 1.0, fr, TAG["rug"])
            lay.ribbon((x, 0.7, z1), (x - 0.6, 0.7, z1 + 6.5), 1.3, 1.0, fr, TAG["rug"])

    def chandelier(self, lay):
        """A simple brass chandelier on a chain, over the rug: not lit tonight, but it catches the lamps."""
        P = self.P
        x0, x1, y0, y1, z0, z1 = BX["chandelier"]
        cx, cz, r = (x0 + x1) / 2, (z0 + z1) / 2, (x1 - x0) / 2
        tag = TAG["chandelier"]
        brass = P(BRASS * 0.9, gloss=self.shine(1.3), warm=2.4, cool=1.6)
        lay.ribbon((cx, HH, cz), (cx, y1 + 6, cz), 2.2, 2.2, P(BRASS * 0.55, warm=2.0, cool=1.6), tag)
        lay.lathe(cx, cz, [(0.5, y0 + 2), (5.5, y0 + 8), (2.6, y0 + 16), (8.0, y0 + 30), (9.0, y0 + 38), (3.6, y0 + 48), (4.6, y1 - 10), (1.6, y1 + 6)], brass, tag, sides=10)
        lay.lathe(cx, cz, [(4.2, y0 - 5), (0.0, y0 + 2)], brass, tag, sides=8)
        glass = P((0.80, 0.84, 0.86), gloss=self.shine(1.6, (1.0, 0.92, 0.75)), warm=2.6, cool=2.2)
        for i in range(6):
            a = math.radians(i * 60 + 18)
            ex, ez = cx + math.cos(a) * r, cz + math.sin(a) * r
            mx, mz = cx + math.cos(a) * r * 0.55, cz + math.sin(a) * r * 0.55
            lay.tube([(cx + math.cos(a) * 7, y0 + 32, cz + math.sin(a) * 7), (mx, y0 + 17, mz), (ex - math.cos(a) * 4, y0 + 15, ez - math.sin(a) * 4), (ex, y0 + 24, ez)], 2.8, brass, tag)
            lay.lathe(ex, ez, [(1.4, y0 + 23), (5.4, y0 + 27), (5.4, y0 + 28.5)], brass, tag, sides=8)
            lay.lathe(ex, ez, [(3.0, y0 + 28.5), (7.0, y0 + 36), (8.0, y0 + 44), (6.8, y0 + 47)], glass, tag, sides=8)            # a frosted glass shade
        lay.disc((cx, HH - 0.5, cz), 16.0, P(WHITE * 1.1), tag, sides=12)                                                     # the rose on the ceiling

    def plant(self, lay):
        """A tall rubber plant in a pot by the right-hand wall."""
        P = self.P
        px_, pz_ = XR - 20.0, 432.0
        lay.lathe(px_, pz_, [(11.0, 0), (15.0, 26), (16.0, 29)], P((0.60, 0.30, 0.18)), sides=10)
        lay.disc((px_, 27.5, pz_), 14.5, P((0.16, 0.11, 0.08)), sides=10)
        stem = P((0.26, 0.22, 0.12))
        rng = np.random.default_rng(19)
        greens = [(0.10, 0.30, 0.15), (0.16, 0.40, 0.18), (0.08, 0.22, 0.13), (0.22, 0.46, 0.20)]
        for (dx, dz, top) in ((0.0, 0.0, 168.0), (-5.0, 6.0, 128.0), (4.0, -6.0, 146.0)):
            lay.tube([(px_ + dx * 0.3, 27, pz_ + dz * 0.3), (px_ + dx, top * 0.5, pz_ + dz), (px_ + dx * 1.6, top, pz_ + dz * 1.6)], 2.2, stem)
            n = int(top / 13)
            for i in range(n):
                t = 0.30 + 0.70 * (i + rng.random() * 0.5) / n
                bx_, by_, bz_ = px_ + dx * (0.3 + 1.3 * t), 27 + (top - 27) * t, pz_ + dz * (0.3 + 1.3 * t)
                a = rng.uniform(0, 2 * math.pi) if i % 2 else rng.uniform(1.6, 4.6)                # more of them reach into the room
                ln, wd = rng.uniform(20, 30), rng.uniform(8, 12)
                ux, uz = math.cos(a), math.sin(a)
                droop = rng.uniform(-10, 8)
                tip = (bx_ + ux * ln, by_ + droop, bz_ + uz * ln)
                mid_ = (bx_ + ux * ln * 0.5, by_ + droop * 0.3 + 3, bz_ + uz * ln * 0.5)
                sx_, sz_ = -uz * wd, ux * wd
                g = col(greens[int(rng.integers(0, 4))]) * rng.uniform(0.8, 1.25)
                lay.poly([(bx_, by_, bz_), (mid_[0] + sx_, mid_[1] - 2, mid_[2] + sz_), tip, mid_], P(g, gloss=self.shine(0.25)))
                lay.poly([(bx_, by_, bz_), mid_, tip, (mid_[0] - sx_, mid_[1] - 2, mid_[2] - sz_)], P(g * 0.78, gloss=self.shine(0.25)))

    def quilt(self, lay):
        """A patchwork quilt hung over the railing upstairs to air."""
        P = self.P
        zt = 175.0
        xa, xb = 698.0, 766.0
        rng = np.random.default_rng(6)
        cols = np.array([[0.62, 0.20, 0.18], [0.82, 0.74, 0.56], [0.20, 0.30, 0.50], [0.74, 0.56, 0.22], [0.30, 0.46, 0.36], [0.84, 0.80, 0.72]], dtype=F32)
        pick = rng.integers(0, 6, size=(12, 12))

        def patch(X, Y, Z, iy, ix):
            i = np.clip(np.floor((X - xa) / 9.0).astype(np.intp), 0, 11)
            j = np.clip(np.floor((Y - G) / 9.0).astype(np.intp) % 12, 0, 11)
            c = cols[pick[i, j]]
            fu, fv = np.mod(X - xa, 9.0), np.mod(Y - G, 9.0)
            tri = (fu + fv > 9.0) & ((i + j) % 2 == 0)                                             # half the squares are cut corner to corner
            c = np.where(tri[:, None], cols[pick[j, i]], c)
            fold = 0.86 + 0.20 * np.sin((X - xa) / 11.0 + Y * 0.05)
            return c * fold[:, None]
        q = P(patch)
        lay.poly([(xa, G + 96.5, zt - 5), (xb, G + 96.5, zt - 5), (xb, G + 96.5, zt + 5), (xa, G + 96.5, zt + 5)], q, TAG["rail"])
        lay.poly([(xa, G + 96.5, zt + 5), (xb, G + 96.5, zt + 5), (xb - 2, G + 22, zt + 6.5), (xa + 3, G + 30, zt + 6.5)], q, TAG["rail"])
        lay.poly([(xa, G + 96.5, zt - 5), (xb, G + 96.5, zt - 5), (xb - 1, G + 50, zt - 6.5), (xa + 1, G + 44, zt - 6.5)], q, TAG["rail"])

    def phone_table(self, lay):
        """A narrow table against the panelling at the back: the telephone, a pad and pencil, flowers in a jug."""
        P = self.P
        x0, x1, z0, z1, top = SW + 1.0, SW + 21.0, 92.0, 150.0, 74.0
        wood = P(self.wood(DARKWOOD * 1.7, 6.0, "Z"), gloss=self.shine(0.2))
        lay.box(x0, x1 + 1.5, top - 3, top, z0 - 1.5, z1 + 1.5, wood)
        lay.box(x0, x1, top - 14, top - 3, z0, z1, P(self.wood(DARKWOOD * 1.4, 6.0, "Z")))
        lay.disc((x1 + 0.3, top - 8.5, (z0 + z1) / 2), 1.4, P(BRASS, gloss=self.shine(0.8)), axis="X", sides=6)
        for za in (z0 + 1, z1 - 4):
            lay.box(x1 - 3, x1, 0, top - 14, za, za + 3, wood)
            lay.box(x0, x0 + 3, 0, top - 14, za, za + 3, wood)
        # the telephone: a cream base, a dark handset lying across it, its cord
        lay.box(x0 + 3, x0 + 16, top, top + 5, z0 + 6, z0 + 24, P((0.84, 0.80, 0.68)))
        lay.box(x0 + 5, x0 + 14, top + 5, top + 8.5, z0 + 4, z0 + 26, P((0.16, 0.15, 0.17), gloss=self.shine(0.4)))
        lay.tube([(x0 + 9, top + 3, z0 + 5), (x0 + 12, top + 1, z0 - 2), (x0 + 14, top - 20, z0 - 3), (x0 + 6, top - 40, z0 - 2), (x0 + 1, top - 30, z0 - 1)], 0.9, P((0.16, 0.15, 0.17)))
        # the pad, with a pencil across it
        lay.box(x0 + 4, x0 + 15, top, top + 1.2, z0 + 30, z0 + 43, P((0.95, 0.94, 0.86)))
        lay.ribbon((x0 + 5, top + 1.6, z0 + 32), (x0 + 15, top + 1.6, z0 + 41), 0.9, 0.9, flat((0.30, 0.42, 0.70)))
        # a jug of flowers
        jx, jz = x0 + 10.0, z1 - 8.0
        lay.lathe(jx, jz, [(4.5, top), (6.0, top + 7), (4.0, top + 14), (4.6, top + 17)], P((0.86, 0.88, 0.90), gloss=self.shine(0.7)), sides=8)
        lay.lathe(jx, jz, [(5.6, top + 5), (5.9, top + 8)], P((0.24, 0.40, 0.70)), sides=8, smooth=False)
        rng = np.random.default_rng(23)
        heads = [(0.96, 0.84, 0.24), (0.95, 0.94, 0.88), (0.86, 0.30, 0.32), (0.96, 0.84, 0.24), (0.90, 0.55, 0.70), (0.95, 0.94, 0.88), (0.86, 0.30, 0.32)]
        for i, hc in enumerate(heads):
            a = rng.uniform(0, 2 * math.pi)
            r = rng.uniform(3, 11)
            hx, hz, hy = jx + math.cos(a) * r * 0.8, jz + math.sin(a) * r * 1.2, top + 26 + rng.uniform(0, 22)
            lay.ribbon((jx, top + 16, jz), (hx, hy, hz), 0.9, 0.9, P((0.18, 0.40, 0.18)))
            lay.ribbon((hx, hy - 3.6, hz), (hx, hy + 3.6, hz), 7.6, 7.6, P(col(hc), warm=2.5, cool=1.6))
            lay.ribbon((hx, hy - 1.2, hz + 0.3), (hx, hy + 1.2, hz + 0.3), 2.4, 2.4, P((0.60, 0.40, 0.10), warm=2.5))
        for k in range(5):                                       # a few leaves
            a = rng.uniform(0, 2 * math.pi)
            lay.ribbon((jx, top + 17, jz), (jx + math.cos(a) * 7, top + 20 + rng.uniform(0, 8), jz + math.sin(a) * 9), 2.6, 0.8, P((0.16, 0.36, 0.18)))

    def odds(self, lay):
        """Small true things: the switch by the door, the cable Dad ran from the cupboard, a toy on the stairs."""
        P = self.P
        d = FL["door"]
        lay.box(d[2] - 13, d[2] - 6, 118, 131, 0, 1.0, P(WHITE * 1.15, plane="back"))
        lay.box(d[2] - 10.4, d[2] - 8.6, 122, 127, 1.0, 1.6, P((0.30, 0.28, 0.26)))
        cable = P((0.20, 0.22, 0.26))
        c = FL["closet"]
        pts = [(SW + 3, 2.0, c[3] - 6), (SW + 9, 0.8, c[3] - 18), (SW + 6, 0.8, 250), (SW + 4, 0.8, 120), (SW + 5, 0.8, 40), (SW + 30, 0.8, 37), (BX["books"][0] - 2, 0.8, 38)]
        lay.tube(pts, 1.3, cable)
        # things waiting on the stairs to be carried up: folded washing, a book on top
        y6 = STEP_H * 7
        z6 = ST["z_foot"] - STEP_D * 6.5
        for i, cc in enumerate(((0.86, 0.86, 0.82), (0.36, 0.48, 0.70), (0.88, 0.80, 0.62), (0.80, 0.40, 0.42))):
            lay.box(16, 44, y6 + i * 3.6, y6 + (i + 1) * 3.6, z6 - 9, z6 + 9, P(col(cc)))
        lay.box(20, 38, y6 + 14.4, y6 + 16.8, z6 - 7, z6 + 6, P((0.20, 0.34, 0.30)))
        # a small pair of shoes kicked off at the foot of the stairs
        for (sx, sz, a) in ((116.0, 632.0, 12.0), (124.0, 646.0, -18.0)):
            lay.tf = rot((sx, sz), a)
            lay.box(sx - 4, sx + 4, 0, 4, sz - 9, sz + 9, P((0.86, 0.50, 0.60)))
            lay.box(sx - 4, sx + 4, 4, 7, sz - 9, sz - 1, P((0.92, 0.62, 0.70)))
            lay.box(sx - 4.2, sx + 4.2, 0, 1.4, sz - 9.2, sz + 9.2, P((0.90, 0.90, 0.88)))
            lay.tf = None
        # a ball that has rolled to the wall, and a school bag under the coats
        lay.lathe(XR - 24, 318, [(0.0, 0), (7.5, 2.5), (11.0, 9), (11.0, 13), (7.5, 19.5), (0.0, 22)], P((0.86, 0.46, 0.14)), sides=10)
        bag = P(self.cloth((0.30, 0.44, 0.66), 3.0, fold=14.0, deep=0.2))
        lay.box(XR - 20, XR - 4, 0, 34, 172, 204, bag)
        lay.box(XR - 22, XR - 18, 6, 24, 177, 199, P((0.24, 0.36, 0.56)))
        lay.tube([(XR - 12, 34, 178), (XR - 13, 44, 188), (XR - 12, 34, 198)], 2.0, P((0.20, 0.30, 0.48)))
        # Little Sister's rabbit, left sitting on the fourth stair
        y = STEP_H * 4
        z = ST["z_foot"] - STEP_D * 3.5
        fur = P((0.82, 0.74, 0.66))
        lay.lathe(86, z, [(6.0, y), (7.0, y + 6), (5.0, y + 13), (0.0, y + 15)], fur, sides=8)
        lay.lathe(86, z + 1, [(4.6, y + 13), (5.2, y + 18), (3.6, y + 22), (0.0, y + 23.5)], fur, sides=8)
        for dx in (-2.4, 2.4):
            lay.ribbon((86 + dx, y + 22, z + 1), (86 + dx * 1.8, y + 33, z), 2.4, 1.6, fur)
            lay.ribbon((86 + dx, y + 24, z + 1.4), (86 + dx * 1.7, y + 31.5, z + 0.4), 1.0, 0.7, P((0.90, 0.60, 0.62)))

    # ------------------------------------------------------------ all of it
    def backdrop(self, lay):
        self.shell(lay)
        self.window(lay)
        self.kitchen(lay)
        self.doorway_trim(lay)
        self.stairs(lay)
        self.banister(lay)
        self.gallery(lay)
        self.upstairs(lay)
        self.bookcase(lay)
        self.print_frame(lay)
        self.clock(lay)
        self.front_door(lay)
        self.coats(lay)
        self.stair_photos(lay)
        self.painting(lay)
        self.rug(lay)
        self.chandelier(lay)
        self.plant(lay)
        self.quilt(lay)
        self.phone_table(lay)
        self.odds(lay)

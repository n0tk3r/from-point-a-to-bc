"""The living room's furniture that the game lays over the backdrop as cut-outs: the piano (with its lamp and
bench), Dad's armchair (with the reading lamp and the crossword), the pencil, and the dinner table (five places,
five chairs, the pendant lamp, the family Bible).

Each is built from boxes and turned pieces standing in the room, through the same camera as the room itself."""

import math

import numpy as np

from brush import F32
import home_living_room_model as M
from home_living_room_kit import Layer, paint_of, flat, col, sstep, hash2, vnoise, fbm, rot
from home_living_room_room import (V, BX, FL, TAG, G, HH, XR, WHITE, OAK, DARKWOOD, BRASS, RED, NAVY, CREAM, Tex, c255, pxcm, near, panel)


class Recorder:
    """Stands in for a Layer to find out which boxes throw shadows (the ones laid with sh=True)."""

    def __init__(self):
        self.tf, self.boxes = None, []

    def box(self, X0, X1, Y0, Y1, Z0, Z1, paint=None, tag=0, skip=(), paints=None, sh=False):
        if not sh:
            return
        pts = [(x, 0, z) for x in (X0, X1) for z in (Z0, Z1)]
        if self.tf is not None:
            pts = [self.tf(p) for p in pts]
        xs, zs = [p[0] for p in pts], [p[2] for p in pts]
        self.boxes.append((min(xs), max(xs), float(Y0), float(Y1), min(zs), max(zs)))

    def _nothing(self, *a, **k):
        return None
    poly = prism = lathe = disc = ribbon = tube = extrude_x = extrude_z = _nothing


class Things:
    def __init__(self, room):
        self.R = room
        self.P = room.P
        self.L = room.L

    # ================================================================ the piano
    def piano(self, lay, open_panel=False):
        R, P = self.R, self.P
        x0, x1, _, top, _, zk = BX["piano"]
        zb = 39.0                                             # the case is this deep; the keys stand out beyond it
        tag = TAG["piano"]
        mah = (0.34, 0.15, 0.085)
        wood = P(R.wood(mah, 6.0, "Y", grain=0.30), gloss=R.shine(0.22))
        woodx = P(R.wood(mah, 7.0, "X", grain=0.30), gloss=R.shine(0.30))
        dark = P(col(mah) * 0.55)
        # the case: two sides, the top, the bottom rail
        lay.box(x0, x0 + 5, 0, top, 0, zb, wood, tag, sh=False)
        lay.box(x1 - 5, x1, 0, top, 0, zb, wood, tag)
        lay.box(x0, x1, 0, top, 0, zb - 3, dark, tag, skip=("front",), sh=True)
        lay.box(x0 - 1.5, x1 + 1.5, top, top + 3.5, 0, zb + 1.5, woodx, tag)
        lay.box(x0, x1, 0, 13, 0, zb, woodx, tag)

        # the upper front: a panel behind the music desk
        def upper(X, Y, Z, iy, ix):
            c = R.wood(mah, 9.0, "X", grain=0.28)(X, Y, Z, iy, ix)
            c *= panel(X, Y, x0 + 12, x1 - 12, 87.0, top - 6.0, 2.5)[:, None]
            return c
        lay.poly([(x0 + 5, 82, zb - 1), (x1 - 5, 82, zb - 1), (x1 - 5, top, zb - 1), (x0 + 5, top, zb - 1)], P(upper, gloss=R.shine(0.18)), tag)
        # the lower front: the panel by the pedals (it comes off)
        lx0, lx1, ly0, ly1 = x0 + 9, x1 - 9, 15.0, 58.0
        if not open_panel:
            def lower(X, Y, Z, iy, ix):
                c = R.wood(mah, 11.0, "X", grain=0.28)(X, Y, Z, iy, ix)
                c *= panel(X, Y, lx0 + 5, lx1 - 5, ly0 + 5, ly1 - 5, 2.5)[:, None]
                return c
            lay.poly([(x0 + 5, 13, zb - 1.5), (x1 - 5, 13, zb - 1.5), (x1 - 5, 62, zb - 1.5), (x0 + 5, 62, zb - 1.5)], P(lower, gloss=R.shine(0.12)), TAG["panel"])
        else:
            # open: the frame round a dark hole, the strings' lower ends, the pedal rods, a glint of iron
            lay.poly([(x0 + 5, 13, zb - 1.5), (x1 - 5, 13, zb - 1.5), (x1 - 5, 62, zb - 1.5), (x0 + 5, 62, zb - 1.5)], P(R.wood(mah, 11.0, "X", grain=0.28)), TAG["panel"])

            def inside(X, Y, Z, n, iy, ix):
                c = np.broadcast_to(np.array([0.035, 0.028, 0.030], dtype=F32), X.shape + (3,)).copy()
                strings = (np.mod(X - lx0 + (Y - ly0) * 0.35, 3.1) < 0.9) & (Y > ly0 + 12)
                c = np.where(strings[:, None], np.array([0.30, 0.22, 0.12], dtype=F32)[None, :] * (0.5 + 0.5 * (Y[:, None] - ly0) / (ly1 - ly0)), c)
                board = (Y < ly0 + 12)
                c = np.where(board[:, None], np.array([0.11, 0.07, 0.045], dtype=F32)[None, :], c)
                return c
            lay.poly([(lx0, ly0, zb - 1.3), (lx1, ly0, zb - 1.3), (lx1, ly1, zb - 1.3), (lx0, ly1, zb - 1.3)], inside, TAG["panel"])
            rod = flat((0.28, 0.24, 0.18))
            mid = (x0 + x1) / 2
            for dx in (-9.0, 0.0, 9.0):
                lay.ribbon((mid + dx, ly0, zb - 1.0), (mid + dx * 2.6, ly1, zb - 1.0), 1.1, 1.1, rod, TAG["panel"])
            # the panel itself, taken off and stood on its end against the wall beside the piano
            px0, px1 = x0 - 50.0, x0 - 6.0
            ph = lx1 - lx0

            def off(X, Y, Z, iy, ix):
                c = R.wood(mah, 11.0, "Y", grain=0.28)(X, Y, Z, iy, ix)
                c *= panel(X, Y / 0.994, px0 + 5, px1 - 5, 5.0, ph - 5.0, 2.5)[:, None]
                return c
            lay.poly([(px0, 0.5, 17.0), (px1, 0.5, 17.0), (px1, ph * 0.994, 3.5), (px0, ph * 0.994, 3.5)], P(off, gloss=R.shine(0.15)), TAG["panel"])
            lay.poly([(px1, 0.5, 17.0), (px1, 0.5, 15.0), (px1, ph * 0.994, 1.5), (px1, ph * 0.994, 3.5)], dark, TAG["panel"])
            lay.poly([(px0, ph * 0.994, 3.5), (px1, ph * 0.994, 3.5), (px1, ph * 0.994, 1.5), (px0, ph * 0.994, 1.5)], P(col(mah) * 1.3), TAG["panel"])
        # the key bed, its cheeks, the fall above the keys
        lay.box(x0, x1, 60, 67, zb - 2, zk, woodx, tag, sh=True)
        lay.box(x0, x0 + 8, 67, 80, zb - 2, zk, wood, tag)
        lay.box(x1 - 8, x1, 67, 80, zb - 2, zk, wood, tag)
        lay.poly([(x0 + 8, 69.4, zb - 1), (x1 - 8, 69.4, zb - 1), (x1 - 8, 82, zb - 1), (x0 + 8, 82, zb - 1)], P(col(mah) * 0.9, gloss=R.shine(0.3)), tag)
        kx0, kx1 = x0 + 8.0, x1 - 8.0
        kw = (kx1 - kx0) / 52.0
        T = Tex(kx1 - kx0, zk - zb - 1.5, 6.0, c255((0.93, 0.90, 0.80)))
        dk = zk - zb - 1.5
        for i in range(52):                                   # the white keys' joints, and the black keys in their twos and threes
            T.line([(i * kw, 0), (i * kw, dk)], c255((0.50, 0.46, 0.40)), 0.30)
            if (i % 7) in (0, 1, 3, 4, 5) and i < 51:
                T.rect((i + 1) * kw - 0.75, 0, (i + 1) * kw + 0.75, dk * 0.62, c255((0.07, 0.06, 0.07)))
        T.rect(0, dk - 1.2, kx1 - kx0, dk, c255((0.70, 0.66, 0.56)))
        lay.poly([(kx0, 69.4, zb), (kx1, 69.4, zb), (kx1, 69.4, zk - 0.5), (kx0, 69.4, zk - 0.5)],
                 P(lambda X, Y, Z, iy, ix: T.at(X - kx0, (zk - 0.5) - Z)), tag)
        lay.poly([(kx0, 67, zk - 0.5), (kx1, 67, zk - 0.5), (kx1, 69.4, zk - 0.5), (kx0, 69.4, zk - 0.5)], P((0.80, 0.76, 0.64)), tag)
        # legs under the key bed, pedals
        for xa in (x0 + 1.5, x1 - 9.5):
            lay.box(xa, xa + 8, 0, 60, zb, zk - 5, wood, tag)
            lay.box(xa - 1, xa + 9, 0, 6, zb, zk - 3, woodx, tag)
        mid = (x0 + x1) / 2
        for dx in (-9.0, 0.0, 9.0):
            lay.box(mid + dx - 2.2, mid + dx + 2.2, 3.0, 4.6, zb, zb + 11, P(BRASS, gloss=R.shine(0.7)), tag)
        # the music desk and the hymnal standing open on it
        lay.box(x0 + 26, x1 - 26, 88.0, 90.0, zb - 1, zb + 6, woodx, tag)
        hx = mid - 2.0
        page = P(self.pages(hx - 15.5, 31.0, 91.0, 23.0, seed=4))
        lay.poly([(hx - 16.5, 90.2, zb + 4.6), (hx + 16.5, 90.2, zb + 4.6), (hx + 16.5, 114.5, zb + 0.2), (hx - 16.5, 114.5, zb + 0.2)], P((0.20, 0.10, 0.08)), tag)
        lay.poly([(hx - 15.5, 91.0, zb + 5.0), (hx + 15.5, 91.0, zb + 5.0), (hx + 15.5, 114.0, zb + 0.7), (hx - 15.5, 114.0, zb + 0.7)], page, tag)
        # on the top: the lamp, a metronome, a photograph, a pile of music
        ty = top + 3.5
        lx, _, lz = M.LIGHTS["piano"]
        brass = P(BRASS * 0.95, gloss=R.shine(0.6))
        lay.lathe(lx, lz, [(8.0, ty), (8.5, ty + 2), (3.0, ty + 4), (2.0, ty + 9), (5.0, ty + 14), (4.0, ty + 19), (1.4, ty + 22), (1.4, ty + 26)], brass, TAG["lamp"], sides=10)
        lay.lathe(lx, lz, [(15.0, ty + 22), (9.0, ty + 43)], R.shade_paint((1.0, 0.82, 0.52), 1.7, band=(ty + 22, ty + 43)), TAG["lamp"], sides=12)
        lay.disc((lx, ty + 43, lz), 9.0, flat((1.9, 1.65, 1.05)), TAG["lamp"], sides=12)
        mx, mz = x0 + 22.0, 20.0                              # the metronome
        mw = P(R.wood((0.42, 0.24, 0.12), 3.0, "Y"))
        lay.poly([(mx - 6, ty, mz + 5), (mx + 6, ty, mz + 5), (mx + 2.2, ty + 21, mz + 1.5), (mx - 2.2, ty + 21, mz + 1.5)], mw, tag)
        lay.poly([(mx + 6, ty, mz + 5), (mx + 6, ty, mz - 5), (mx + 2.2, ty + 21, mz - 1.5), (mx + 2.2, ty + 21, mz + 1.5)], P(col((0.42, 0.24, 0.12)) * 0.7), tag)
        lay.ribbon((mx, ty + 3, mz + 5.2), (mx + 2.5, ty + 19, mz + 2.2), 0.8, 0.8, flat((0.85, 0.80, 0.60)), tag)
        R.photo(lay, "back", x0 + 40, ty, 20, 25, 77, 1)       # (stands against the wall)
        yy = ty
        for (w, th, c) in ((30, 2.2, (0.86, 0.82, 0.70)), (28, 3.0, (0.20, 0.30, 0.48)), (29, 1.8, (0.88, 0.84, 0.72)), (26, 2.6, (0.50, 0.14, 0.12))):
            lay.box(x0 + 74, x0 + 74 + w, yy, yy + th, 8, 31, P(col(c)), tag)
            yy += th

    def pages(self, u0, w, v0, h, seed=1, flat_on="wall", lines=11, music=True):
        """An open book's two pages: lines of print (or staves), a dark gutter down the middle."""
        def alb(X, Y, Z, iy, ix):
            u = (X - u0) / w
            v = (Y - v0) / h
            c = np.broadcast_to(np.array([0.93, 0.90, 0.78], dtype=F32), X.shape + (3,)).copy()
            c *= (1 - 0.35 * np.exp(-np.abs(u - 0.5) / 0.035))[:, None]                      # the gutter
            inpage = (np.abs(np.abs(u - 0.5) - 0.25) < 0.19)
            ln = np.mod(v * lines, 1.0)
            if music:
                row = (np.mod(v * 4.0, 1.0) > 0.25) & (np.mod(v * 4.0, 1.0) < 0.70)
                ink = inpage & row & (np.mod(v * 4.0 * 9.0, 1.0) < 0.36)
            else:
                ink = inpage & (ln > 0.25) & (ln < 0.62) & (vnoise(u * 60.0, np.floor(v * lines) * 3.0, seed) > 0.22)
            ink = ink & (v > 0.08) & (v < 0.92)
            return np.where(ink[:, None], c * np.array([0.52, 0.50, 0.50], dtype=F32), c)
        return alb

    def bench(self, lay):
        R, P = self.R, self.P
        x0, x1, _, h, z0, z1 = BX["stool"]
        tag = TAG["stool"]
        wood = P(R.wood((0.34, 0.15, 0.085), 5.0, "X", grain=0.3), gloss=R.shine(0.2))
        lay.box(x0, x1, h - 8, h - 2, z0, z1, wood, tag, sh=True)
        lay.box(x0 + 2, x1 - 2, h - 2, h + 1.5, z0 + 2, z1 - 2, P(lambda X, Y, Z, iy, ix: col((0.50, 0.16, 0.14))[None, :] * (0.85 + 0.3 * vnoise(X * 0.5, Z * 0.5, 4.0))[:, None]), tag)
        for xa in (x0 + 2, x1 - 7):
            for za in (z0 + 2, z1 - 7):
                lay.box(xa, xa + 5, 0, h - 8, za, za + 5, wood, tag)
        lay.box(x0 + 5, x1 - 5, 12, 15, z0 + 3, z0 + 6, wood, tag)

    # ================================================================ Dad's armchair, the reading lamp, the crossword
    def armchair(self, lay, pencil=False, only_pencil=False):
        R, P = self.R, self.P
        bx = BX["armchair"]
        cx, cz = (bx[0] + bx[1]) / 2, (bx[4] + bx[5]) / 2
        tag = TAG["armchair"]
        lay.tf = rot((cx, cz), 25.0)

        def leather(base, seed):
            base = col(base)

            def alb(X, Y, Z, iy, ix):
                n = fbm(X * 0.06 + Y * 0.02, Z * 0.06 + Y * 0.05, seed, 3)
                crack = vnoise(X * 0.9 + Y * 0.3, Z * 0.9, seed + 4)
                return base[None, :] * (0.78 + 0.42 * n)[:, None] * (0.93 + 0.14 * crack)[:, None]
            return alb
        hide = (0.30, 0.115, 0.07)
        lea = P(leather(hide, 3.0), gloss=R.shine(0.30, (1.0, 0.85, 0.6)), warm=3.4, cool=1.7)
        lea2 = P(leather(col(hide) * 1.15, 5.0), gloss=R.shine(0.35, (1.0, 0.85, 0.6)), warm=3.4, cool=1.7)
        dk = P(col(hide) * 0.5)
        x0, x1 = cx - 46, cx + 46                              # across the chair (the sitter's left .. right)
        zf, zr = cz - 46, cz + 46                              # its front (it faces the back wall) .. its back
        if not only_pencil:
            for xa in (x0 + 3, x1 - 9):                        # stubby turned feet
                for za in (zf + 3, zr - 9):
                    lay.box(xa, xa + 6, 0, 12, za, za + 6, P(DARKWOOD), tag)
            lay.box(x0, x1, 11, 40, zf, zr - 2, lea, tag, sh=True, skip=("top", "bottom", "left", "right", "front", "back"))
            lay.box(x0 + 2, x1 - 2, 40, 98, zr - 22, zr, lea, tag, sh=True, skip=("top", "bottom", "left", "right", "front", "back"))
            # a barrel back: the hide goes round behind the sitter in one curve, low at the arms, high in the middle
            bz = cz + 4.0
            R0 = 46.0

            def ring(y, r_in, r_out, a0, a1, paint, n=6):
                for k in range(n):
                    pa, pb = math.radians(a0 + (a1 - a0) * k / n), math.radians(a0 + (a1 - a0) * (k + 1) / n)
                    lay.poly([(cx + math.cos(pa) * r_in, y, bz + math.sin(pa) * r_in), (cx + math.cos(pa) * r_out, y, bz + math.sin(pa) * r_out),
                              (cx + math.cos(pb) * r_out, y, bz + math.sin(pb) * r_out), (cx + math.cos(pb) * r_in, y, bz + math.sin(pb) * r_in)], paint, tag)

            def end(a_, y0_, y1_, r_in, r_out, paint):
                pa = math.radians(a_)
                lay.poly([(cx + math.cos(pa) * r_in, y0_, bz + math.sin(pa) * r_in), (cx + math.cos(pa) * r_out, y0_, bz + math.sin(pa) * r_out),
                          (cx + math.cos(pa) * r_out, y1_, bz + math.sin(pa) * r_out), (cx + math.cos(pa) * r_in, y1_, bz + math.sin(pa) * r_in)], paint, tag)
            lay.lathe(cx, bz, [(R0 - 2.0, 11), (R0 - 0.5, 30), (R0, 62)], lea, tag, sides=18, a0=-6, a1=186)
            lay.lathe(cx, bz, [(R0, 62), (R0 + 0.5, 80), (R0 - 1.0, 90)], lea, tag, sides=16, a0=14, a1=166)
            lay.lathe(cx, bz, [(R0 - 1.0, 90), (R0 - 2.0, 98), (R0 - 5.5, 103), (R0 - 10.0, 104.5)], lea2, tag, sides=12, a0=32, a1=148)
            lay.lathe(cx, bz, [(33.0, 46), (32.0, 90)], lea, tag, sides=16, a0=14, a1=166, smooth=False)       # the inside of the back
            lay.lathe(cx, bz, [(32.0, 90), (33.0, 100), (36.0, 104.5)], lea, tag, sides=12, a0=32, a1=148, smooth=False)
            ring(90.0, 32.0, R0 - 1.0, 14, 32, lea2)
            ring(90.0, 32.0, R0 - 1.0, 148, 166, lea2)
            for a_ in (14, 166):
                end(a_, 62.0, 90.0, 32.0, R0, lea2)
            for a_ in (32, 148):
                end(a_, 90.0, 104.0, 33.0, R0 - 2.0, lea2)
            seam = P(col(hide) * 0.40)
            for a_ in (40.0, 140.0):                                                           # the seams where the hides are joined
                pa = math.radians(a_)
                lay.ribbon((cx + math.cos(pa) * (R0 + 0.6), 13, bz + math.sin(pa) * (R0 + 0.6)), (cx + math.cos(pa) * (R0 + 0.2), 98, bz + math.sin(pa) * (R0 + 0.2)), 1.2, 1.2, seam, tag)
            nail = P(BRASS * 1.05, gloss=R.shine(0.8))
            for k in range(22):                                                                # brass nails round the foot of it
                pa = math.radians(2 + k * 8.4)
                lay.ribbon((cx + math.cos(pa) * (R0 - 0.9), 15.6, bz + math.sin(pa) * (R0 - 0.9)), (cx + math.cos(pa) * (R0 - 0.8), 17.8, bz + math.sin(pa) * (R0 - 0.8)), 2.0, 2.0, nail, tag)
            # the seat, its cushion, the arms rolled over at the top
            lay.box(cx - 33, cx + 33, 11, 42, zf, cz + 12, lea, tag)
            lay.box(cx - 30, cx + 30, 42, 51.5, zf - 2, cz + 14, self.puff(lea2, lay.tf((cx, 51.5, cz - 16)), 30.0, 30.0, 0.5), tag)
            lay.box(cx - 30, cx + 30, 45.5, 47.0, zf - 2.4, cz + 14, dk, tag, skip=("top", "bottom"))          # its piping
            for sgn, xe in ((1, x1), (-1, x0)):
                arm = [(xe - sgn * 17, 11), (xe - sgn * 17.5, 56), (xe - sgn * 20, 60), (xe - sgn * 19, 65), (xe - sgn * 13, 68.5), (xe - sgn * 5, 68.5),
                       (xe + sgn * 1.5, 65), (xe + sgn * 2, 60), (xe, 55), (xe, 11)]
                lay.extrude_z(arm, zf - 2, cz + 12, self.puff(lea, lay.tf((xe, 38.0, cz - 18)), 46.0, 30.0, 0.7), tag, cap_paint=lea2)
                for k in range(5):                                                             # brass nails down the front of the arm
                    lay.disc((xe - sgn * 8.5, 15 + k * 8.0, zf - 2.3), 1.1, nail, tag, axis="Z", sides=6)
            # a knitted blanket thrown over the back, on the far side from us
            def knit(X, Y, Z, iy, ix):
                s = np.floor((Y + (X + Z) * 0.25) / 9.0)
                cols = np.array([[0.62, 0.48, 0.22], [0.20, 0.32, 0.34], [0.70, 0.64, 0.50], [0.20, 0.32, 0.34], [0.46, 0.18, 0.15], [0.20, 0.32, 0.34]], dtype=F32)
                c = cols[np.mod(s, 6).astype(np.intp)]
                return c * (0.85 + 0.25 * np.sin((X + Z) * 2.1) * np.sin(Y * 2.3))[:, None]
            kn = P(knit, warm=3.0, cool=1.7)
            lay.lathe(cx, bz, [(R0 + 1.2, 50), (R0 + 1.6, 80), (R0 + 0.3, 90), (R0 - 0.8, 98), (R0 - 4.2, 103.8), (R0 - 9.0, 105.6)], kn, tag, sides=8, a0=66, a1=118)
            lay.lathe(cx, bz, [(R0 - 9.0, 105.6), (31.0, 101), (30.5, 82)], kn, tag, sides=8, a0=66, a1=118, smooth=False)
            for a_ in (66, 118):
                end(a_, 50.0, 98.0, R0 - 0.5, R0 + 1.6, kn)
            # the folded newspaper on the arm nearest us, crossword uppermost
            nx0, nz0 = x1 - 16.5, zf + 9.0
            T = Tex(16.0, 26.0, 8.0, c255((0.84, 0.82, 0.74)))
            for i in range(9):                                 # the grid: black squares among white
                for j in range(9):
                    blk = ((i * 3 + j * 5) % 7 == 0) or ((i + j * 2) % 9 == 4)
                    T.rect(1.5 + i * 1.45, 11.0 + j * 1.45, 1.5 + (i + 1) * 1.45, 11.0 + (j + 1) * 1.45, c255((0.10, 0.10, 0.12)) if blk else c255((0.97, 0.96, 0.90)))
            for i in range(10):
                T.line([(1.5 + i * 1.45, 11.0), (1.5 + i * 1.45, 24.05)], c255((0.25, 0.25, 0.28)), 0.14)
                T.line([(1.5, 11.0 + i * 1.45), (14.55, 11.0 + i * 1.45)], c255((0.25, 0.25, 0.28)), 0.14)
            for j in range(7):                                 # the clues
                T.line([(1.5, 2.0 + j * 1.25), (7.2, 2.0 + j * 1.25)], c255((0.42, 0.42, 0.44)), 0.35)
                T.line([(8.6, 2.0 + j * 1.25), (14.4, 2.0 + j * 1.25)], c255((0.42, 0.42, 0.44)), 0.35)
            lay.box(nx0, nx0 + 16, 66.0, 67.6, nz0, nz0 + 26, P((0.80, 0.78, 0.70)), TAG["crossword"])
            lay.poly([(nx0, 67.7, nz0), (nx0 + 16, 67.7, nz0), (nx0 + 16, 67.7, nz0 + 26), (nx0, 67.7, nz0 + 26)],
                     P(self.on_turned(T, lay.tf, (nx0, nz0), 26.0)), TAG["crossword"])
            # his reading glasses, folded, beside it
            gl = flat((0.10, 0.09, 0.08))
            gx, gz = nx0 + 3.0, nz0 + 31.0
            lay.tube([(gx, 66.6, gz), (gx + 5, 66.6, gz + 1), (gx + 6.5, 66.6, gz + 1.2), (gx + 11.5, 66.6, gz + 2)], 0.7, gl, tag)
            lay.disc((gx + 2.6, 66.5, gz + 0.5), 2.6, P((0.55, 0.62, 0.66), gloss=R.shine(0.6)), tag, sides=8)
            lay.disc((gx + 9.0, 66.5, gz + 1.6), 2.6, P((0.55, 0.62, 0.66), gloss=R.shine(0.6)), tag, sides=8)
        if pencil or only_pencil:
            # the pencil: yellow, six-sided, a pink rubber in a brass band, lying across the crossword
            nx0, nz0 = x1 - 16.5, zf + 9.0
            pa, pb = (nx0 + 2.0, 68.6, nz0 + 21.0), (nx0 + 14.5, 68.6, nz0 + 4.0)
            d = tuple(pb[k] - pa[k] for k in range(3))
            at = lambda t: tuple(pa[k] + d[k] * t for k in range(3))
            lay.ribbon(at(0.0), at(0.10), 1.5, 1.5, flat((0.93, 0.50, 0.52)), TAG["pencil"])
            lay.ribbon(at(0.10), at(0.17), 1.6, 1.6, flat((0.80, 0.66, 0.30)), TAG["pencil"])
            lay.ribbon(at(0.17), at(0.88), 1.5, 1.5, flat((0.98, 0.80, 0.12)), TAG["pencil"])
            lay.ribbon(at(0.88), at(0.97), 1.5, 0.5, flat((0.90, 0.74, 0.50)), TAG["pencil"])
            lay.ribbon(at(0.97), at(1.0), 0.5, 0.2, flat((0.12, 0.12, 0.14)), TAG["pencil"])
        lay.tf = None

    @staticmethod
    def puff(paint, centre, rx, ry, bend=0.7):
        """Paint for a stuffed surface: the same paint, lit as if the surface swelled outward from `centre`."""
        cx_, cy_, cz_ = centre

        def p(X, Y, Z, n, iy, ix):
            nx, ny, nz = n
            tl = math.hypot(nx, nz)
            if tl < 0.2:                                      # a top: let it swell both ways across
                mx, my, mz = nx + bend * (X - cx_) / rx, ny, nz + bend * (Z - cz_) / rx
            else:
                tx, tz = -nz / tl, nx / tl
                u = ((X - cx_) * tx + (Z - cz_) * tz) / rx
                v = (Y - cy_) / ry
                mx, my, mz = nx + bend * u * tx, ny + bend * v, nz + bend * u * tz
            l = np.sqrt(mx * mx + my * my + mz * mz) + 1e-6
            return paint(X, Y, Z, (mx / l, my / l, mz / l), iy, ix)
        return p

    def on_turned(self, T, tf, origin, depth):
        """Albedo from a flat drawing laid on a thing that has been turned: the drawing's own (u, v) are found
        by turning the place back."""
        (px, pz), c, s = self._pivot(tf)
        ox, oz = origin

        def alb(X, Y, Z, iy, ix):
            dx, dz = X - px, Z - pz
            lx, lz = px + dx * c + dz * s, pz - dx * s + dz * c
            return T.at(lx - ox, depth - (lz - oz))
        return alb

    @staticmethod
    def _pivot(tf):
        """The pivot and angle of a turn made with kit.rot (read back from what it does)."""
        a, b = tf((0.0, 0.0, 0.0)), tf((1.0, 0.0, 0.0))
        c, s = b[0] - a[0], b[2] - a[2]
        # tf(p) = pivot + R (p - pivot)  ->  pivot = (I - R)^-1 (a)   with a = tf(0)
        det = (1 - c) * (1 - c) + s * s
        px = ((1 - c) * a[0] - s * a[2]) / det
        pz = (s * a[0] + (1 - c) * a[2]) / det
        return (px, pz), c, s

    def reading_lamp(self, lay):
        R, P = self.R, self.P
        lx, ly, lz = M.LIGHTS["reading"]
        tag = TAG["lamp"]
        brass = P(BRASS * 0.9, gloss=R.shine(0.7))
        lay.lathe(lx, lz, [(14.0, 0), (14.0, 2.5), (5.0, 5.0), (1.6, 8.0)], brass, tag, sides=12)
        lay.ribbon((lx, 8, lz), (lx, ly - 16, lz), 2.6, 2.6, brass, tag)
        lay.lathe(lx, lz, [(3.2, ly - 16), (1.6, ly - 12), (1.6, ly + 6)], brass, tag, sides=6)
        y0, y1 = ly - 12.0, ly + 14.0

        def pleated(X, Y, Z, n, iy, ix):
            base = R.shade_paint((1.0, 0.80, 0.50), 1.75, band=(y0, y1))(X, Y, Z, n, iy, ix)
            ang = np.arctan2(Z - lz, X - lx)
            return base * (0.90 + 0.10 * np.sin(ang * 26.0))[:, None]
        lay.lathe(lx, lz, [(21.0, y0), (13.0, y1)], pleated, tag, sides=14)
        lay.disc((lx, y1, lz), 13.0, flat((1.9, 1.65, 1.05)), tag, sides=14)
        lay.ribbon((lx + 6, y0, lz + 9), (lx + 6, y0 - 15, lz + 9), 0.5, 0.5, flat((0.70, 0.56, 0.24)), tag)     # the pull chain
        lay.disc((lx + 6, y0 - 16, lz + 9), 1.2, flat((0.80, 0.64, 0.28)), tag, axis="Z", sides=6)

    def by_the_chair(self, lay):
        """What lies about Dad's chair at the front edge: a basket of newspapers, his slippers, a mug on a small table."""
        R, P = self.R, self.P
        tag = TAG["lamp"]                                     # (not part of the armchair's own outline in layout.json)
        # a round side table on the chair's far side, under the lamp: a mug, two books
        lx, _, lz = M.LIGHTS["reading"]
        tx, tz = lx + 30.0, lz - 34.0
        wood = P(R.wood(DARKWOOD * 1.6, 3.0, "Y"), gloss=R.shine(0.2))
        lay.lathe(tx, tz, [(15.0, 0), (15.0, 2), (3.0, 5), (2.2, 50), (5.0, 54)], wood, tag, sides=10)
        lay.lathe(tx, tz, [(21.0, 54), (21.0, 57)], wood, tag, sides=14)
        lay.disc((tx, 57, tz), 21.0, P(R.wood(DARKWOOD * 1.9, 4.0, "X"), gloss=R.shine(0.3)), tag, sides=14)
        lay.box(tx - 14, tx + 4, 57, 60.5, tz - 6, tz + 12, P((0.18, 0.28, 0.44)), tag)
        lay.box(tx - 12, tx + 5, 60.5, 63.0, tz - 5, tz + 11, P((0.60, 0.22, 0.16)), tag)
        lay.lathe(tx + 11, tz - 7, [(4.0, 57), (4.3, 66)], P((0.86, 0.84, 0.76)), tag, sides=8)
        lay.disc((tx + 11, 65.6, tz - 7), 3.6, P((0.22, 0.12, 0.07)), tag, sides=8)
        # a basket of newspapers, in front of the chair on our side
        bx_, bz = 398.0, 704.0
        lay.tf = rot((bx_, bz), -14.0)
        wk = P(R.wicker((0.58, 0.42, 0.22)))
        lay.box(bx_ - 22, bx_ + 22, 0, 26, bz - 15, bz + 15, wk, tag, sh=True)
        lay.poly([(bx_ - 20, 26.2, bz - 13), (bx_ + 20, 26.2, bz - 13), (bx_ + 20, 26.2, bz + 13), (bx_ - 20, 26.2, bz + 13)], P((0.12, 0.09, 0.07)), tag)
        for i, (dx, c, h) in enumerate(((-13, (0.84, 0.82, 0.74), 34), (-6, (0.78, 0.76, 0.70), 37), (1, (0.86, 0.84, 0.78), 32), (9, (0.70, 0.30, 0.22), 35), (15, (0.82, 0.80, 0.72), 30))):
            lay.box(bx_ + dx, bx_ + dx + 4.5, 6, h, bz - 12, bz + 12, P(col(c)), tag)
        lay.tf = None
        # the Son's toy station wagon, parked where he left it
        wx, wz = 432.0, 676.0
        lay.tf = rot((wx, wz), 28.0)
        red = P((0.74, 0.22, 0.16), gloss=R.shine(0.5))
        lay.box(wx - 6, wx + 6, 2.2, 7.5, wz - 14, wz + 14, red, tag)
        lay.box(wx - 5.6, wx + 5.6, 7.5, 12.0, wz - 6, wz + 13, P((0.20, 0.26, 0.36), gloss=R.shine(0.9)), tag)
        lay.box(wx - 6, wx + 6, 12.0, 13.0, wz - 6.5, wz + 13.5, red, tag)
        lay.box(wx - 6.2, wx + 6.2, 3.4, 6.2, wz - 9, wz + 12, P((0.62, 0.42, 0.20)), tag, skip=("top", "bottom", "front", "back"))
        for dz_ in (-9.0, 9.0):
            for dx_ in (-6.4, 6.4):
                lay.disc((wx + dx_, 2.4, wz + dz_), 2.4, P((0.08, 0.08, 0.09)), tag, axis="X", sides=8)
        lay.tf = None
        # his slippers, left where he stepped out of them
        for (sx, sz, a) in ((352.0, 668.0, 22.0), (366.0, 676.0, 38.0)):
            lay.tf = rot((sx, sz), a)
            sl = P((0.36, 0.22, 0.30))
            lay.box(sx - 5, sx + 5, 0, 3.5, sz - 13, sz + 13, sl, tag)
            lay.box(sx - 5.5, sx + 5.5, 3.5, 8, sz - 13.5, sz - 1, P((0.42, 0.26, 0.36)), tag)
            lay.tf = None

    # ================================================================ the dinner table
    def chair(self, lay, cx, cz, facing, tag, pulled=0.0, booster=False):
        """A ladder-back chair with a rush seat. `facing` in degrees: 0 faces the back wall, 90 faces right (+X),
        180 faces us, -90 faces left."""
        R, P = self.R, self.P
        lay.tf = rot((cx, cz), facing)
        wood = P(R.wood((0.46, 0.26, 0.12), cx * 0.01, "Y", grain=0.3), gloss=R.shine(0.15))
        x0, x1, zf, zr = cx - 21, cx + 21, cz - 21, cz + 21
        for xa in (x0, x1 - 4):
            lay.box(xa, xa + 4, 0, 44, zf, zf + 4, wood, tag)                                   # front legs
            lay.box(xa, xa + 4, 0, 98, zr - 4, zr, wood, tag, sh=True)                          # back posts
            lay.box(xa + 0.8, xa + 3.2, 14, 16.5, zf + 4, zr - 4, wood, tag)                    # stretchers
        lay.box(x0 + 4, x1 - 4, 20, 22.5, zf + 0.8, zf + 3.2, wood, tag)
        lay.box(x0 + 4, x1 - 4, 14, 16.5, zr - 3.2, zr - 0.8, wood, tag)

        def rush(X, Y, Z, iy, ix):
            (px, pz), c, s = self._pivot(rot((cx, cz), facing))
            dx, dz = X - px, Z - pz
            lx, lz = dx * c + dz * s, -dx * s + dz * c
            d = np.maximum(np.abs(lx), np.abs(lz))
            q = np.where(np.abs(lx) > np.abs(lz), lz, lx)
            wv = np.sin(d * 2.2) * 0.5 + 0.5
            return np.array([0.74, 0.60, 0.34], dtype=F32)[None, :] * (0.72 + 0.34 * wv)[:, None] * (0.92 + 0.12 * np.sin(q * 1.9))[:, None]
        lay.box(x0, x1, 42, 46, zf, zr - 3, P(rush), tag, sh=True)
        for y in (58, 73, 88):                                                                  # the slats of the back
            lay.box(x0 + 4, x1 - 4, y, y + 6.5, zr - 3.2, zr - 1.2, wood, tag, sh=True)
        for xa in (x0, x1 - 4):                                                                 # little turned finials
            lay.lathe(xa + 2, zr - 2, [(2.0, 98), (2.8, 100.5), (0.0, 103.5)], wood, tag, sides=6)
        if booster:                                                                             # a child's cushion on the seat
            lay.box(x0 + 5, x1 - 5, 46, 52, zf + 3, zr - 7, P((0.30, 0.42, 0.62)), tag)
        lay.tf = None

    def table(self, lay):
        R, P = self.R, self.P
        x0, x1, _, top, z0, z1 = BX["table"]
        tag = TAG["table"]
        mid = (x0 + x1) / 2
        wood = P(R.wood((0.40, 0.22, 0.11), 2.0, "Y"))
        for xa in (x0 + 5, x1 - 12):
            for za in (z0 + 6, z1 - 13):
                lay.box(xa, xa + 7, 0, top - 4, za, za + 7, wood, tag)
        lay.box(x0 + 3, x1 - 3, top - 12, top - 3, z0 + 4, z1 - 4, wood, tag)
        lay.box(x0, x1, top - 3, top, z0, z1, wood, tag, sh=True)

        # the white cloth: creased where it was folded, hanging a hand's length all round
        def cloth(X, Y, Z, iy, ix):
            px = pxcm(X, Z)
            c = np.broadcast_to(np.array([0.90, 0.88, 0.80], dtype=F32), X.shape + (3,)).copy()
            fold = np.maximum(near(X, mid, 0.5, px, 0.45), near(Z, z0 + (z1 - z0) / 3.0, 0.5, px, 0.45))
            fold = np.maximum(fold, near(Z, z0 + (z1 - z0) * 2.0 / 3.0, 0.5, px, 0.45))
            c *= (1 - 0.10 * fold)[:, None]
            c *= (0.95 + 0.08 * fbm(X * 0.05, Z * 0.05, 3.0, 2))[:, None]
            edge = np.minimum(np.minimum(X - x0, x1 - X), np.minimum(Z - z0, z1 - Z))
            hem = (edge > 2.2) & (edge < 4.2) & (np.mod(X + Z, 3.0) < 1.9)                        # a line of blue stitching round the edge
            c = np.where(hem[:, None], np.array([0.36, 0.50, 0.72], dtype=F32)[None, :], c)
            return c
        cl = P(cloth, mott=(R.mott, 0.04))
        lay.poly([(x0 - 1, top + 0.6, z0 - 1), (x1 + 1, top + 0.6, z0 - 1), (x1 + 1, top + 0.6, z1 + 1), (x0 - 1, top + 0.6, z1 + 1)], cl, tag)
        hang = P(R.cloth((0.86, 0.84, 0.77), 2.0, fold=11.0, deep=0.16, along="Z"))
        hangx = P(R.cloth((0.86, 0.84, 0.77), 2.0, fold=11.0, deep=0.16, along="X"))
        lay.poly([(x0 - 1, top + 0.6, z0 - 1), (x0 - 1, top + 0.6, z1 + 1), (x0 - 1.5, top - 24, z1 + 1), (x0 - 1.5, top - 24, z0 - 1)], hang, tag)
        lay.poly([(x1 + 1, top + 0.6, z0 - 1), (x1 + 1, top + 0.6, z1 + 1), (x1 + 1.5, top - 24, z1 + 1), (x1 + 1.5, top - 24, z0 - 1)], hang, tag)
        lay.poly([(x0 - 1, top + 0.6, z0 - 1), (x1 + 1, top + 0.6, z0 - 1), (x1 + 1, top - 24, z0 - 1.5), (x0 - 1, top - 24, z0 - 1.5)], hangx, tag)
        lay.poly([(x0 - 1, top + 0.6, z1 + 1), (x1 + 1, top + 0.6, z1 + 1), (x1 + 1, top - 24, z1 + 1.5), (x0 - 1, top - 24, z1 + 1.5)], hangx, tag)
        ty = top + 0.7

        china = (0.93, 0.92, 0.86)
        steel = P((0.66, 0.68, 0.70), gloss=R.shine(0.9, (1.0, 0.95, 0.85)))

        def shadow(cx, cz, r, k=0.55):
            lay.disc((cx, ty + 0.05, cz), r, P(col((0.86, 0.84, 0.77)) * k), tag, sides=12)

        def place(cx, cz, toward, used, kind=""):
            """One place: `toward` is (dx, dz) from the plate to the person's chair."""
            tx, tz = toward
            sx, sz = -tz, tx                                   # along the table edge (to the diner's right... or left)
            shadow(cx + 0.8, cz + 0.8, 13.6)
            lay.lathe(cx, cz, [(8.0, ty), (12.8, ty + 1.6)], P(china), tag, sides=14)
            lay.disc((cx, ty + 1.2, cz), 12.2, P(china), tag, sides=14)
            ring = P((0.26, 0.40, 0.66))
            lay.lathe(cx, cz, [(10.6, ty + 1.3), (11.6, ty + 1.45)], ring, tag, sides=14, smooth=False)
            fx, fz = cx + sx * 16.5, cz + sz * 16.5              # fork one side, knife and spoon the other
            kx, kz = cx - sx * 16.5, cz - sz * 16.5
            if used:
                # eaten: crumbs and a smear, knife and fork laid together across the plate, the napkin dropped beside it
                rng = np.random.default_rng(int(cx * 7 + cz))
                for _ in range(7):
                    a, r = rng.uniform(0, 6.28), rng.uniform(0, 7.5)
                    lay.disc((cx + math.cos(a) * r, ty + 1.3, cz + math.sin(a) * r), rng.uniform(0.8, 2.2),
                             P([(0.60, 0.40, 0.18), (0.50, 0.62, 0.26), (0.74, 0.30, 0.16), (0.80, 0.70, 0.40)][int(rng.integers(0, 4))]), tag, sides=6)
                lay.ribbon((cx - sx * 2 - tx * 7, ty + 1.9, cz - sz * 2 - tz * 7), (cx + sx * 6 + tx * 9, ty + 1.9, cz + sz * 6 + tz * 9), 1.3, 1.1, steel, tag)
                lay.ribbon((cx - sx * 5 - tx * 6, ty + 1.9, cz - sz * 5 - tz * 6), (cx + sx * 3 + tx * 10, ty + 1.9, cz + sz * 3 + tz * 10), 1.3, 1.1, steel, tag)
                nx, nz = fx + sx * 3 + tx * 2, fz + sz * 3 + tz * 2
                nap = P(lambda X, Y, Z, iy, ix: np.array([0.80, 0.84, 0.90], dtype=F32)[None, :] * (0.80 + 0.3 * vnoise(X * 0.5, Z * 0.5, cx))[:, None])
                lay.poly([(nx - 6, ty + 0.4, nz - 5), (nx + 3, ty + 0.4, nz - 7), (nx + 8, ty + 0.4, nz + 1), (nx + 2, ty + 0.4, nz + 7), (nx - 7, ty + 0.4, nz + 3)], nap, tag)
                lay.poly([(nx - 3, ty + 2.5, nz - 2), (nx + 3, ty + 0.6, nz - 5), (nx + 6, ty + 0.6, nz + 2), (nx + 1, ty + 2.2, nz + 4)], P((0.88, 0.90, 0.94)), tag)
            else:
                # nobody's tonight: fork and knife straight, the napkin still folded on the clean plate
                lay.ribbon((fx - tx * 8, ty + 0.5, fz - tz * 8), (fx + tx * 9, ty + 0.5, fz + tz * 9), 1.4, 1.0, steel, tag)
                lay.ribbon((kx - tx * 8, ty + 0.5, kz - tz * 8), (kx + tx * 9, ty + 0.5, kz + tz * 9), 1.5, 1.2, steel, tag)
                lay.ribbon((kx - sx * 3 - tx * 8, ty + 0.5, kz - sz * 3 - tz * 8), (kx - sx * 3 + tx * 7, ty + 0.5, kz - sz * 3 + tz * 7), 1.2, 1.0, steel, tag)
                nap = P((0.30, 0.44, 0.70))
                lay.poly([(cx - tx * 7 - sx * 6, ty + 1.8, cz - tz * 7 - sz * 6), (cx - tx * 7 + sx * 6, ty + 1.8, cz - tz * 7 + sz * 6),
                          (cx + tx * 7, ty + 4.5, cz + tz * 7)], nap, tag)
                lay.poly([(cx - tx * 7 - sx * 6, ty + 1.8, cz - tz * 7 - sz * 6), (cx + tx * 7, ty + 4.5, cz + tz * 7), (cx + tx * 7.5 - sx * 5, ty + 1.8, cz + tz * 7.5 - sz * 5)],
                         P((0.22, 0.34, 0.58)), tag)
            # a glass above the knife (a child's cup with a straw for the youngest)
            gx, gz = kx - tx * 14 + sx * 3, kz - tz * 14 + sz * 3
            shadow(gx + 0.8, gz + 0.8, 4.4, 0.7)
            if kind == "child":
                lay.lathe(gx, gz, [(3.4, ty), (3.9, ty + 9)], P((0.92, 0.46, 0.60)), tag, sides=8)
                lay.disc((gx, ty + 9, gz), 3.9, P((0.96, 0.60, 0.70)), tag, sides=8)
                lay.ribbon((gx, ty + 9, gz), (gx + 3, ty + 17, gz - 2), 0.8, 0.8, flat((0.95, 0.95, 0.90)), tag)
            else:
                water = 0.75 if not used else 0.25
                gp = P((0.60, 0.70, 0.74), gloss=R.shine(1.2, (1.0, 0.97, 0.9)))
                lay.lathe(gx, gz, [(2.6, ty), (3.4, ty + 11)], gp, tag, sides=8)
                lay.disc((gx, ty + 11 * water, gz), 2.6 + 0.8 * water, P((0.80, 0.88, 0.92)), tag, sides=8)

        places = [((mid, z0 + 18.0), (0, -1), False, ""),                         # the head of the table: Dad's
                  ((x0 + 21.0, z0 + 50.0), (-1, 0), False, ""),                    # the Son's, on the left
                  ((x1 - 21.0, z0 + 50.0), (1, 0), True, ""),
                  ((x0 + 21.0, z0 + 144.0), (-1, 0), True, "child"),
                  ((x1 - 21.0, z0 + 144.0), (1, 0), True, "")]
        for (c, toward, used, kind) in places:
            place(c[0], c[1], toward, used, kind)

        # the serving dishes down the middle, gone cold
        dz = z0 + 62.0
        shadow(mid + 1.5, dz + 1.5, 16.5)                                          # a covered casserole, blue enamel
        en = P((0.20, 0.36, 0.62), gloss=R.shine(0.8, (1.0, 0.95, 0.85)))
        lay.lathe(mid, dz, [(12.0, ty), (15.0, ty + 9.0), (15.6, ty + 9.6)], en, tag, sides=14)
        lay.lathe(mid, dz, [(15.6, ty + 9.6), (11.0, ty + 14.0), (3.0, ty + 15.5), (0.0, ty + 15.6)], P((0.24, 0.42, 0.70), gloss=R.shine(0.9, (1.0, 0.95, 0.85))), tag, sides=14)
        lay.lathe(mid, dz, [(2.2, ty + 15.4), (3.0, ty + 18.5), (0.0, ty + 19.2)], P((0.14, 0.14, 0.16)), tag, sides=8)
        lay.box(mid - 19.5, mid - 14.5, ty + 7.5, ty + 9.5, dz - 3, dz + 3, en, tag)
        lay.box(mid + 14.5, mid + 19.5, ty + 7.5, ty + 9.5, dz - 3, dz + 3, en, tag)
        dz = z0 + 100.0                                                           # a bowl of greens with the servers in it
        shadow(mid + 1.5, dz + 1.5, 14.5)
        lay.lathe(mid, dz, [(6.0, ty), (13.5, ty + 9.0)], P(R.wood((0.58, 0.36, 0.16), 3.0, "Y")), tag, sides=14)
        lay.disc((mid, ty + 8.0, dz), 12.6, P((0.20, 0.36, 0.14)), tag, sides=14)
        rng = np.random.default_rng(5)
        for _ in range(26):
            a, r = rng.uniform(0, 6.28), rng.uniform(0, 10.5)
            c = [(0.28, 0.50, 0.18), (0.40, 0.62, 0.22), (0.16, 0.34, 0.14), (0.78, 0.20, 0.14), (0.86, 0.80, 0.50)][int(rng.integers(0, 5) if rng.random() < 0.3 else rng.integers(0, 3))]
            lay.disc((mid + math.cos(a) * r, ty + 8.4 + rng.uniform(0, 1.6), dz + math.sin(a) * r), rng.uniform(1.6, 3.2), P(c), tag, sides=6)
        lay.ribbon((mid + 2, ty + 9, dz + 2), (mid + 15, ty + 15, dz - 9), 1.6, 1.2, P(R.wood((0.62, 0.40, 0.18), 3.0, "Y")), tag)
        dz = z0 + 136.0                                                           # the bread basket under its cloth, two rolls left
        shadow(mid - 3 + 1.5, dz + 1.5, 15.0)
        lay.lathe(mid - 3, dz, [(10.0, ty), (14.0, ty + 7.5)], P(R.wicker((0.66, 0.48, 0.24))), tag, sides=12)
        lay.disc((mid - 3, ty + 6.5, dz), 13.0, P((0.84, 0.30, 0.24)), tag, sides=12)
        lay.poly([(mid - 16, ty + 7.6, dz - 4), (mid - 2, ty + 9.5, dz - 12), (mid + 8, ty + 7.8, dz - 2), (mid - 4, ty + 9.0, dz + 9)], P((0.90, 0.36, 0.28)), tag)
        for (bx_, bz) in ((mid + 2, dz + 5), (mid - 7, dz + 3)):
            lay.lathe(bx_, bz, [(4.6, ty + 7.6), (4.0, ty + 10.4), (0.0, ty + 11.6)], P((0.80, 0.56, 0.26)), tag, sides=8)
        # a jug of water, the butter, salt and pepper, a gravy boat
        jx, jz = mid + 20.0, z0 + 84.0
        shadow(jx + 1, jz + 1, 7.5, 0.6)
        jug = P((0.62, 0.74, 0.80), gloss=R.shine(1.3, (1.0, 0.97, 0.9)))
        lay.lathe(jx, jz, [(5.5, ty), (6.8, ty + 9), (5.0, ty + 17), (5.6, ty + 21)], jug, tag, sides=10)
        lay.disc((jx, ty + 14, jz), 5.6, P((0.78, 0.88, 0.94)), tag, sides=10)
        lay.tube([(jx - 5.5, ty + 18, jz), (jx - 10, ty + 15, jz), (jx - 9.5, ty + 8, jz), (jx - 6.5, ty + 5, jz)], 1.4, jug, tag)
        bx_, bz = mid - 22.0, z0 + 88.0
        lay.box(bx_ - 7, bx_ + 7, ty, ty + 1.5, bz - 5, bz + 5, P(china), tag)
        lay.box(bx_ - 5, bx_ + 4, ty + 1.5, ty + 4.5, bz - 2.6, bz + 2.6, P((0.96, 0.86, 0.42)), tag)
        for (sx_, sz_, c) in ((mid - 14.0, z0 + 118.0, (0.92, 0.92, 0.90)), (mid - 9.0, z0 + 120.5, (0.30, 0.28, 0.28))):
            lay.lathe(sx_, sz_, [(2.2, ty), (2.0, ty + 6.5), (1.4, ty + 8.0)], P(c), tag, sides=6)
            lay.disc((sx_, ty + 8.0, sz_), 1.4, P((0.75, 0.76, 0.78)), tag, sides=6)
        gx, gz = mid + 19.0, z0 + 122.0
        lay.lathe(gx, gz, [(4.0, ty), (6.5, ty + 5.5)], P(china), tag, sides=10)
        lay.disc((gx, ty + 4.6, gz), 5.8, P((0.42, 0.26, 0.14)), tag, sides=10)
        # two candles in brass sticks that nobody lit
        for cz_ in (z0 + 40.0, z0 + 158.0):
            lay.lathe(mid + (6 if cz_ > z0 + 100 else -4), cz_, [(4.5, ty), (4.5, ty + 1.2), (1.2, ty + 2.5), (1.2, ty + 7.0), (2.4, ty + 8.0)], P(BRASS, gloss=R.shine(0.9)), tag, sides=8)
            lay.lathe(mid + (6 if cz_ > z0 + 100 else -4), cz_, [(1.1, ty + 8.0), (1.0, ty + 24.0), (0.0, ty + 25.0)], P((0.93, 0.90, 0.80)), tag, sides=6)

        # the family Bible, open beside the plate at the head of the table, its ribbon across the page
        bx0, bz0 = mid - 53.0, z0 + 5.0
        bw, bd = 37.0, 27.0
        btag = TAG["bible"]
        lay.box(bx0 - 1.2, bx0 + bw + 1.2, ty, ty + 1.0, bz0 - 1.2, bz0 + bd + 1.2, P((0.10, 0.07, 0.06)), btag)
        for (xa, xb, tilt) in ((bx0, bx0 + bw / 2, 1), (bx0 + bw / 2, bx0 + bw, -1)):
            lay.box(xa, xb, ty + 1.0, ty + 3.6, bz0, bz0 + bd, P((0.86, 0.80, 0.62)), btag)

        def page(X, Y, Z, iy, ix):
            u = (X - bx0) / bw
            v = (Z - bz0) / bd
            c = np.broadcast_to(np.array([0.96, 0.93, 0.80], dtype=F32), X.shape + (3,)).copy()
            c *= (1 - 0.40 * np.exp(-np.abs(u - 0.5) / 0.03))[:, None]
            colu = np.mod(np.abs(u - 0.5) * 2 * 2.0, 1.0)                                    # two columns to a page
            inpage = (np.abs(u - 0.5) > 0.03) & (np.abs(u - 0.5) < 0.465) & (colu > 0.10) & (colu < 0.92) & (v > 0.07) & (v < 0.93)
            ln = np.mod(v * 17.0, 1.0)
            ink = inpage & (ln > 0.2) & (ln < 0.62) & (vnoise(u * 90.0, np.floor(v * 17.0) * 3.0, 5.0) > 0.2)
            c = np.where(ink[:, None], c * np.array([0.55, 0.52, 0.50], dtype=F32), c)
            edge = (np.abs(u - 0.5) > 0.485) | (v < 0.015) | (v > 0.985)                       # the gilt of the page edges
            return np.where(edge[:, None], BRASS[None, :] * 1.0, c)
        lay.poly([(bx0, ty + 3.7, bz0), (bx0 + bw, ty + 3.7, bz0), (bx0 + bw, ty + 3.7, bz0 + bd), (bx0, ty + 3.7, bz0 + bd)], P(page), btag)
        rib = P((0.72, 0.10, 0.10))
        lay.poly([(bx0 + bw * 0.52, ty + 3.85, bz0), (bx0 + bw * 0.56, ty + 3.85, bz0), (bx0 + bw * 0.60, ty + 3.85, bz0 + bd), (bx0 + bw * 0.56, ty + 3.85, bz0 + bd)], rib, btag)
        lay.poly([(bx0 + bw * 0.56, ty + 3.85, bz0 + bd), (bx0 + bw * 0.60, ty + 3.85, bz0 + bd), (bx0 + bw * 0.63, ty + 0.4, bz0 + bd + 6.5), (bx0 + bw * 0.585, ty + 0.4, bz0 + bd + 7.5)], P((0.60, 0.08, 0.08)), btag)

    def chairs(self, lay):
        t = TAG["table"]
        b = BX
        self.chair(lay, *self._mid(b["chair-head"]), 180.0, t)
        self.chair(lay, *self._mid(b["chair-left-far"]), 90.0, t)
        self.chair(lay, *self._mid(b["chair-left-near"]), 66.0, t)
        self.chair(lay, *self._mid(b["chair-right-far"]), -84.0, t)
        self.chair(lay, *self._mid(b["chair-right-near"]), -122.0, t)

    @staticmethod
    def _mid(b):
        return (b[0] + b[1]) / 2, (b[4] + b[5]) / 2

    def pendant(self, lay):
        """The lamp over the table: a low dome of leaded glass, amber with a border of green and red, on a long chain."""
        R = self.R
        lx, ly, lz = M.LIGHTS["pendant"]
        x0, x1, y0, y1, z0, z1 = BX["pendant"]
        r = (x1 - x0) / 2
        tag = TAG["pendant"]

        def glass(X, Y, Z, n, iy, ix):
            ang = np.arctan2(Z - lz, X - lx)
            t = (Y - y0) / (y1 - y0)
            seg = np.floor((ang + math.pi) / (2 * math.pi) * 14.0)
            amber = np.array([1.0, 0.72, 0.30], dtype=F32)[None, :] * (0.86 + 0.24 * hash2(seg, np.floor(t * 3.0), 3.0))[:, None]
            c = amber
            border = t < 0.26
            bc = np.where((np.mod(seg, 2) < 0.5)[:, None], np.array([0.42, 0.72, 0.30], dtype=F32)[None, :], np.array([0.95, 0.32, 0.16], dtype=F32)[None, :])
            c = np.where(border[:, None], bc, c)
            fs = (ang + math.pi) / (2 * math.pi) * 14.0 - seg
            lead = (np.minimum(fs, 1 - fs) < 0.07) | (np.abs(t - 0.26) < 0.03) | (np.abs(t - 0.62) < 0.02) | (t < 0.035)
            vx, vz = V.cam_x - X, V.cam_z - Z
            vl = np.sqrt(vx * vx + vz * vz) + 1e-6
            facing = np.clip((n[0] * vx + n[2] * vz) / vl, 0, 1)
            c = c * (1.05 + 0.75 * facing ** 1.2)[:, None]
            return np.where(lead[:, None], np.array([0.10, 0.08, 0.06], dtype=F32)[None, :], c)
        lay.lathe(lx, lz, [(r, y0), (r * 0.94, y0 + (y1 - y0) * 0.26), (r * 0.66, y0 + (y1 - y0) * 0.70), (r * 0.26, y1)], glass, tag, sides=14)
        lay.lathe(lx, lz, [(r * 0.26, y1), (r * 0.20, y1 + 3), (2.0, y1 + 5)], self.P(BRASS * 0.7, gloss=R.shine(0.6)), tag, sides=8)
        lay.ribbon((lx, y1 + 5, lz), (lx, HH, lz), 0.8, 2.0, flat((0.47, 0.36, 0.18)), tag)       # its chain: about a pixel wide all the way up

    # ================================================================ what throws shadows
    def shadow_boxes(self):
        rec = Recorder()
        self.piano(rec)
        self.bench(rec)
        self.armchair(rec)
        self.by_the_chair(rec)
        self.table(rec)
        self.chairs(rec)
        return rec.boxes

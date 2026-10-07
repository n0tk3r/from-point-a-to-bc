"""Things that grow: palms, reeds, scrub. Drawn leaf by leaf on a clear sheet, dark first, light last."""

import math

import numpy as np

from brush import F32, Sheet, curve, lerp, rgb


def _mix(a, b, t):
    return lerp(rgb(a) if isinstance(a, str) else np.asarray(a, dtype=F32), rgb(b) if isinstance(b, str) else np.asarray(b, dtype=F32), t)


def palm(sheet, x, y, height, seed, lean=0.0, greens=("#10241a", "#23481f", "#5a882c", "#b6c662"), bark=("#33241e", "#77593c", "#b48e5a"),
         light=-1, fronds=26, spread=1.0, dead=("#6e5230", "#a8824a")):
    """A date palm with its foot at (x, y). `light` is -1 when the sun is on the left, +1 on the right.

    The crown is a ball of fronds. Each frond is a rib that arches out and then droops, with leaflets
    along both sides like the barbs of a feather. The far, low, shaded ones are painted first and dark;
    the high ones on the sunny side last and light."""
    rng = np.random.default_rng(seed)
    top = (x + lean * height, y - height)
    bend = (x + lean * height * 0.4 + rng.normal(0, height * 0.025), y - height * 0.5)
    trunk = curve([(x, y), bend, top], 16)
    w0, w1 = height * 0.052, height * 0.034
    sheet.taper(trunk, bark[0], w0, w1)
    sheet.taper([(px + light * w0 * 0.20, py) for px, py in trunk], bark[1], w0 * 0.55, w1 * 0.5)
    sheet.taper([(px + light * w0 * 0.34, py) for px, py in trunk], bark[2], w0 * 0.18, w1 * 0.16, 0.85)
    for i in range(1, len(trunk) - 1):                                    # the scars old fronds leave, as criss-cross nicks
        px, py = trunk[i]
        wd = lerp(w0, w1, i / len(trunk))
        d = 1 if i % 2 else -1
        sheet.line([(px - wd * 0.45, py + d * 1.2), (px + wd * 0.45, py - d * 1.2)], bark[0], max(0.9, height * 0.006), 0.6)
    foot = max(2.0, w0 * 0.75)                                            # it widens a little where it enters the sand
    sheet.poly([(x - foot, y + 1), (x - w0 * 0.5, y - foot * 1.6), (x + w0 * 0.5, y - foot * 1.6), (x + foot, y + 1)], bark[0])
    sheet.poly([(x + light * foot * 0.75, y + 1), (x + light * w0 * 0.42, y - foot * 1.6), (x + light * w0 * 0.1, y - foot * 1.6), (x + light * foot * 0.2, y + 1)], bark[1])

    L = height * 0.40 * spread
    for i in range(7):                                                    # last year's fronds hang dry against the trunk
        side = -1 if i % 2 else 1
        a = math.radians(rng.uniform(58, 84))
        length = L * rng.uniform(0.45, 0.8)
        tip = (top[0] + side * math.cos(a) * length, top[1] + math.sin(a) * length)
        mid = (top[0] + side * math.cos(a) * length * 0.55 + side * length * 0.10, top[1] + math.sin(a) * length * 0.45)
        rib = curve([(top[0], top[1] + height * 0.01), mid, tip], 6)
        tone = _mix(dead[0], dead[1], rng.random() * (0.9 if side * light > 0 else 0.4))
        sheet.taper(rib, tone, height * 0.014, height * 0.004)
        for j in range(1, len(rib) - 1, 1):
            px, py = rib[j]
            for sd in (-1, 1):
                sheet.line([(px, py), (px + sd * length * 0.10 + rng.normal(0, 1), py + length * 0.13)], tone, max(0.9, height * 0.007), 0.9)
    crown = []
    for i in range(fronds):
        a = math.radians(-38 + 256 * (i + rng.random()) / fronds)           # from below level on the right, over the top, to below level on the left
        up = math.sin(a)
        behind = rng.random()
        crown.append((0.55 * (up + 1) / 2 + 0.45 * behind, a, behind))
    for order, a, behind in sorted(crown):
        dx, up = math.cos(a), math.sin(a)
        length = L * (0.72 + 0.4 * rng.random()) * (0.8 + 0.2 * max(up, 0))
        # the rib: out along its angle, then gravity takes the tip
        sag = length * (0.10 + 0.30 * (1 - max(up, 0)) ** 1.5) * (0.7 + 0.6 * rng.random())
        p1 = (top[0] + dx * length * 0.40, top[1] - up * length * 0.42 - length * 0.07)
        p2 = (top[0] + dx * length * 0.75, top[1] - up * length * 0.74 + sag * 0.25)
        p3 = (top[0] + dx * length * 1.00, top[1] - up * length * 0.92 + sag)
        rib = curve([top, p1, p2, p3], 7)
        sunny = (dx * light > -0.2) * 0.5 + max(up, 0) * 0.6                # high fronds and those toward the sun
        depth = 0.35 + 0.65 * order
        dark = _mix(greens[0], greens[1], depth * 0.9)
        lit = _mix(greens[1], greens[2], min(1.0, sunny + 0.15 * rng.random()))
        hi = _mix(greens[2], greens[3], 0.35 + 0.4 * rng.random())
        sheet.taper(rib, dark, height * 0.011, height * 0.004)
        n = len(rib)
        for j in range(1, n - 1):
            px, py = rib[j]
            tx, ty = rib[j + 1][0] - rib[j - 1][0], rib[j + 1][1] - rib[j - 1][1]
            norm = math.hypot(tx, ty) + 1e-6
            tx, ty = tx / norm, ty / norm
            t = j / (n - 1)
            leaf = length * 0.20 * math.sin(math.pi * min(1.0, 0.10 + t * 0.92)) ** 0.8 + 1.2
            for side in (-1, 1):
                # a leaflet leaves the rib at about 50 degrees toward the tip, and hangs a little
                ca, sa = math.cos(math.radians(42)), math.sin(math.radians(42)) * side
                lx, ly = tx * ca - ty * sa, tx * sa + ty * ca
                ex = px + lx * leaf + rng.normal(0, 0.8)
                ey = py + ly * leaf + leaf * 0.16 + rng.normal(0, 0.8)
                under = ly > 0.15                                             # leaflets on the underside of the rib are in its shade
                tone = dark if under and rng.random() < 0.75 else lit
                if (not under) and sunny > 0.55 and rng.random() < 0.35:
                    tone = hi
                sheet.taper([(px, py), ((px + ex) / 2, (py + ey) / 2 - leaf * 0.04), (ex, ey)], tone, max(0.9, height * 0.010), 0.5)
    # the heart of the crown is dark; dates hang under it
    sheet.ellipse(top[0], top[1] + height * 0.01, height * 0.035, height * 0.03, greens[0])
    for k in range(3):
        cx = top[0] + (k - 1) * height * 0.03 + rng.normal(0, 1)
        sheet.line([(cx, top[1] + height * 0.02), (cx + rng.normal(0, 1), top[1] + height * 0.085)], "#a8742c", max(1.2, height * 0.012))
        sheet.ellipse(cx, top[1] + height * 0.09, height * 0.014, height * 0.02, "#7a3f18")
    return sheet


def reeds(sheet, x, y, width, height, seed, count=40, greens=("#27401f", "#4d7a2c", "#93b04a"), heads="#8a5a2c", light=-1):
    """A stand of reeds or papyrus with its feet along y, centred on x."""
    rng = np.random.default_rng(seed)
    stems = []
    for _ in range(count):
        sx = x + rng.normal(0, width * 0.28)
        hgt = height * (0.55 + 0.5 * rng.random()) * (1 - 0.45 * abs(sx - x) / width)
        stems.append((rng.random(), sx, hgt))
    for depth, sx, hgt in sorted(stems):
        sway = rng.normal(0, hgt * 0.10) + light * -hgt * 0.03
        top = (sx + sway, y - hgt)
        stem = curve([(sx, y + rng.random() * 3), (sx + sway * 0.3, y - hgt * 0.5), top], 6)
        tone = _mix(greens[0], greens[1], depth)
        sheet.taper(stem, tone, max(1.2, height * 0.022), max(0.8, height * 0.010))
        if depth > 0.4:
            sheet.taper([(px + light * 0.7, py) for px, py in stem], _mix(greens[1], greens[2], depth), max(0.8, height * 0.008), 0.6, 0.85)
        if rng.random() < 0.55:                                                  # a feathery head
            for k in range(7):
                a = math.pi * (0.15 + 0.7 * rng.random())
                r = hgt * (0.10 + 0.08 * rng.random())
                sheet.line([top, (top[0] + math.cos(a) * r * 0.8, top[1] - math.sin(a) * r)], _mix(heads, greens[2], rng.random() * 0.5), max(0.8, height * 0.007), 0.9)
        elif rng.random() < 0.5:                                                 # or a bent leaf
            mid = (sx + sway * 0.6, y - hgt * 0.7)
            tip = (mid[0] + rng.normal(0, hgt * 0.22), mid[1] + hgt * 0.18)
            sheet.taper(curve([mid, ((mid[0] + tip[0]) / 2, mid[1] - hgt * 0.05), tip], 5), tone, max(1.0, height * 0.014), 0.6)
    return sheet


def scrub(sheet, x, y, r, seed, colors=("#4a5a34", "#7a8a4a", "#a8ae68")):
    """A low desert bush: a tuft of short strokes."""
    rng = np.random.default_rng(seed)
    for k in range(int(14 + r)):
        a = math.pi * rng.random()
        l = r * (0.5 + 0.7 * rng.random())
        sheet.line([(x + rng.normal(0, r * 0.3), y), (x + math.cos(a) * l, y - math.sin(a) * l * 0.8)], _mix(colors[0], colors[2], rng.random() ** 1.3), max(0.9, r * 0.10))
    return sheet


def papyrus(sheet, x, y, height, seed, lean=0.0, greens=("#1c2f1c", "#3f6a2a", "#86a83e", "#d2d47c"), light=-1, rays=24, head=0.26):
    """One papyrus plant with its foot at (x, y): a long bare stalk and, at the top, a mop of fine rays
    that spread like a firework and droop at the ends."""
    rng = np.random.default_rng(seed)
    top = (x + lean * height, y - height)
    stalk = curve([(x, y), (x + lean * height * 0.35, y - height * 0.5), top], 8)
    wd = max(1.4, height * 0.022)
    sheet.taper(stalk, greens[0], wd, wd * 0.6)
    sheet.taper([(px + light * wd * 0.22, py) for px, py in stalk], greens[1], wd * 0.5, wd * 0.3)
    R = height * head
    marks = []
    for i in range(rays):
        a = math.radians(8 + 164 * (i + rng.random()) / rays)
        marks.append((rng.random(), a))
    for depth, a in sorted(marks):
        r = R * (0.7 + 0.45 * rng.random())
        dx, up = math.cos(a), math.sin(a)
        droop = r * (0.18 + 0.5 * (1 - up) ** 1.4)
        tip = (top[0] + dx * r, top[1] - up * r * 0.85 + droop)
        mid = (top[0] + dx * r * 0.55, top[1] - up * r * 0.62)
        sunny = (dx * light > -0.3) and depth > 0.35
        tone = _mix(greens[1], greens[2], depth) if sunny else _mix(greens[0], greens[1], depth * 0.8)
        ray = curve([top, mid, tip], 5)
        sheet.taper(ray, tone, max(0.9, height * 0.008), max(0.7, height * 0.004))
        if sunny and rng.random() < 0.5:
            sheet.line(ray[-3:], _mix(greens[2], greens[3], rng.random()), max(0.8, height * 0.006), 0.9)
    sheet.ellipse(top[0], top[1] + 1, max(1.5, height * 0.02), max(1.5, height * 0.018), greens[1])
    return sheet


def papyrus_stand(sheet, x, y, width, height, seed, count=12, **how):
    """A clump of papyrus: the far, short stems first, the near, tall ones last."""
    rng = np.random.default_rng(seed)
    stems = []
    for i in range(count):
        sx = x + (rng.random() - 0.5) * width
        back = rng.random()
        stems.append((back, sx, height * (0.55 + 0.45 * back) * (0.85 + 0.3 * rng.random()), rng.normal(0, 0.10)))
    for back, sx, hgt, lean in sorted(stems):
        papyrus(sheet, sx, y + back * 6, hgt, int(rng.integers(1 << 30)), lean=lean, **how)
    return sheet

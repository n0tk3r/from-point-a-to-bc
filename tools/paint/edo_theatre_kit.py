"""PAINT-21D: a faster Room for edo_theatre.py. edo_keep_kit.Room (PAINT-20E's, imported untouched) draws every flat
through a whole-picture mask and a whole-picture grain field; the theatre has some six hundred small flats (the audience),
so this subclass draws each polygon only in its own box and takes the grain from a few fields made once. The picture is
the same kind of picture: flats with the paper's +-3%, one contour round the silhouettes (Room.thing, Room.contours)."""

import zlib

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, noise, warp, blur, rgb
from edo_keep_kit import Room, SHAPE, W, H, col, LINE as _LINE, boundary as _boundary

SS = 3


def _cellkey(cell):
    return cell if np.isscalar(cell) else tuple(cell)


class FastRoom(Room):
    """Room, with flat2d and fill working in the box of the polygon or mask."""

    def __init__(self, view, seed=1, base="#1e2438"):
        super().__init__(view, seed=seed, base=base)
        self._fields = {}

    def field(self, cell, k=0):
        key = (_cellkey(cell), k % 4)
        f = self._fields.get(key)
        if f is None:
            f = (noise(SHAPE, cell, 7000 + 31 * (k % 4) + zlib.crc32(str(key[0]).encode()) % 997, 3) - 0.5).astype(F32)   # (seeded: the same picture every run)
            self._fields[key] = f
        return f

    def box_mask(self, pp, pad=2):
        xs = [p[0] for p in pp]
        ys = [p[1] for p in pp]
        x0 = max(int(np.floor(min(xs))) - pad, 0)
        x1 = min(int(np.ceil(max(xs))) + pad + 1, W)
        y0 = max(int(np.floor(min(ys))) - pad, 0)
        y1 = min(int(np.ceil(max(ys))) + pad + 1, H)
        if x1 <= x0 or y1 <= y0:
            return None
        im = Image.new("L", ((x1 - x0) * SS, (y1 - y0) * SS), 0)
        ImageDraw.Draw(im).polygon([((x - x0) * SS, (y - y0) * SS) for x, y in pp], fill=255)
        m = np.asarray(im.resize((x1 - x0, y1 - y0), Image.BOX), dtype=F32) / 255.0
        return (y0, y1, x0, x1), m

    def flat2d(self, pp, color, grp=None, amount=0.03, cell=90, warm=0.0, alpha=1.0, wobble=0.0, soft=0.0):
        full = np.zeros(SHAPE, F32)
        if len(pp) < 3:
            return full
        r = self.box_mask(pp, pad=2 + int(wobble * 2 + soft * 3))
        if r is None:
            return full
        (y0, y1, x0, x1), m = r
        if wobble or soft:
            full[y0:y1, x0:x1] = m
            if wobble:
                full = warp(full, wobble, max(8.0, wobble * 6), self._seed())
            if soft:
                full = blur(full, soft)
            full = np.clip(full, 0, 1)
            self.fill(full, color, amount=amount, cell=cell, warm=warm, alpha=alpha)
            self.add_mask(grp, full)
            return full
        full[y0:y1, x0:x1] = m
        self._lay(full, (y0, y1, x0, x1), color, amount, cell, warm, alpha)
        self.add_mask(grp, full)
        return full

    def _lay(self, m, box, color, amount, cell, warm, alpha):
        y0, y1, x0, x1 = box
        c = col(color)
        k = (y0 * 7 + x0 * 13 + (y1 - y0) * 3) % 4          # which grain: by the flat's place, not by how many came before it
        n = self.field(cell, k)[y0:y1, x0:x1]
        fld = np.clip(c[None, None, :] * (1 + 2 * amount * n[..., None]), 0, 1)
        if warm:
            wk = self.field(cell, k + 1)[y0:y1, x0:x1] * 2 * warm
            fld[..., 0] = np.clip(fld[..., 0] + wk, 0, 1)
            fld[..., 2] = np.clip(fld[..., 2] - wk, 0, 1)
        mm = (m[y0:y1, x0:x1] * alpha)[..., None]
        reg = self.img[y0:y1, x0:x1]
        self.img[y0:y1, x0:x1] = reg * (1 - mm) + fld * mm

    def fill(self, m, color, amount=0.03, cell=90, warm=0.0, alpha=1.0):
        ys, xs = np.nonzero(m > 0.001)
        if len(ys) == 0:
            return m
        box = (int(ys.min()), int(ys.max()) + 1, int(xs.min()), int(xs.max()) + 1)
        self._lay(m, box, color, amount, cell, warm, alpha)
        return m

    # ---- the contours, kept small: each thing's fill and line cropped to their box (Room keeps them whole: some two
    # hundred things in four renders would not fit in memory)
    def thing(self, m, alpha=0.85, color=None, line=None):
        ln = _boundary(m) if line is None else line
        self._store(m, ln, _LINE if color is None else col(color), alpha)

    def lines(self, m_fill, m_line, alpha=0.3, color=None):
        self._store(m_fill, m_line, _LINE if color is None else col(color), alpha)

    def _store(self, fill, line, color, alpha):
        fb = np.asarray(fill) >= 0.5
        ln = np.asarray(line, dtype=F32)
        ys, xs = np.nonzero(fb | (ln > 0.002))
        if len(ys) == 0:
            return
        y0, y1, x0, x1 = int(ys.min()), int(ys.max()) + 1, int(xs.min()), int(xs.max()) + 1
        self.things.append(((y0, y1, x0, x1), fb[y0:y1, x0:x1].copy(), ln[y0:y1, x0:x1].astype(np.float16), np.asarray(color, F32), alpha))

    def contours(self, pic):
        """Lay every thing's contour, each covered by the fills of the things painted after it (nearer)."""
        cover = np.zeros(SHAPE, bool)
        out = pic.copy()
        layers = []
        for (box, fb, ln, color, alpha) in reversed(self.things):
            y0, y1, x0, x1 = box
            vis = ln.astype(F32) * (~cover[y0:y1, x0:x1])
            layers.append((box, vis, color, alpha))
            cover[y0:y1, x0:x1] |= fb
        for (box, vis, color, alpha) in reversed(layers):
            y0, y1, x0, x1 = box
            m = (vis * alpha)[..., None]
            out[y0:y1, x0:x1] = out[y0:y1, x0:x1] * (1 - m) + color[None, None, :] * m
        return out


# ---------------------------------------------------------------- one brush for several states of one picture
import math as _math
from PIL import Image as _Image, ImageDraw as _ImageDraw
from brush import lerp as _lerp, grain as _grain, palette_of as _palette_of, to_palette as _to_palette, save as _save

_LUM = np.array([0.3, 0.55, 0.15], dtype=F32)


def strokes_shared(refs, sizes=(9, 5, 2), seed=21, density=1.4, jitter=0.025, keep=0.28):
    """brush.strokes for several pictures of one scene at once (the room with and without its cut-outs, before the show
    and in it): ONE layout of strokes (where each lies, how long, how wide, its jitter; a place still wrong in any of the
    pictures gets its smaller stroke in all), each stroke taking its colour and its slant from its own picture. Where
    the pictures are the same, so is the brushwork, pixel for pixel: a state laid over another shows no seam."""
    h, w, _ = refs[0].shape
    rng = np.random.default_rng(seed)
    ss = 2
    canvases = [_Image.fromarray((np.clip(blur(r, sizes[0] * 0.45), 0, 1) * 255).astype(np.uint8)).resize((w * ss, h * ss), _Image.BICUBIC) for r in refs]
    draws = [_ImageDraw.Draw(c) for c in canvases]
    lums = [r @ _LUM for r in refs]
    for r in sizes:
        srcs = [np.clip(blur(ref, r * 0.3), 0, 1) for ref in refs]
        grads = [np.gradient(blur(l, max(1.0, r * 0.35))) for l in lums]
        alongs = [np.arctan2(gy, gx) + _math.pi / 2 for gy, gx in grads]
        strongs = [np.hypot(gx, gy) for gy, gx in grads]
        n = int(w * h / (r * r) * density)
        xs = rng.integers(0, w, n)
        ys = rng.integers(0, h, n)
        if r != sizes[0]:
            wrong = np.zeros((h, w), F32)
            for c, src in zip(canvases, srcs):
                now = np.asarray(c.resize((w, h), _Image.BOX), dtype=F32) / 255
                wrong = np.maximum(wrong, np.abs(now - src).sum(axis=2))
            want = wrong[ys, xs] > (0.05 if r > sizes[-1] else 0.035)
            xs, ys = xs[want], ys[want]
        m = len(xs)
        lvl = rng.normal(0, 0.25, m)
        lens = rng.random(m)
        cj = rng.normal(0, jitter, m)
        cj3 = rng.normal(0, jitter * 0.4, (m, 3))
        wds = rng.random(m)
        for k in range(len(refs)):
            along, strong, src, draw = alongs[k], strongs[k], srcs[k], draws[k]
            for i in range(m):
                x, y = int(xs[i]), int(ys[i])
                a = along[y, x] if strong[y, x] > 0.004 else lvl[i]
                length = r * (1.2 + 2.2 * lens[i])
                dx, dy = _math.cos(a) * length / 2, _math.sin(a) * length / 2
                c = src[y, x] * (1 + cj[i]) + cj3[i]
                fill = tuple(int(v) for v in np.clip(c * 255, 0, 255))
                wd = max(1, int(r * ss * (0.75 + 0.5 * wds[i])))
                x0, y0, x1, y1 = (x - dx) * ss, (y - dy) * ss, (x + dx) * ss, (y + dy) * ss
                draw.line([x0, y0, x1, y1], fill=fill, width=wd)
                e = wd / 2
                draw.ellipse([x0 - e, y0 - e, x0 + e, y0 + e], fill=fill)
                draw.ellipse([x1 - e, y1 - e, x1 + e, y1 + e], fill=fill)
    outs = []
    for c, ref in zip(canvases, refs):
        out = np.asarray(c.resize((w, h), _Image.BOX), dtype=F32) / 255
        outs.append(_lerp(out, ref, keep) if keep else out)
    return outs


def finish_shared(folder, pictures, colors=160, seed=9, speckle=0.012, amount=0.02):
    """Grain (the paper's tooth: ONE grain for every picture, so a state laid over another matches it grain for grain),
    one palette for all the scene's files, and the PNGs. `pictures`: {name: (rgb, alpha or None)}."""
    import os as _os
    _os.makedirs(folder, exist_ok=True)
    grained = {n: _grain(p, seed, amount) for n, (p, a) in pictures.items()}
    sample = [grained[n] if a is None else grained[n][a >= 0.5] for n, (p, a) in pictures.items()]
    sample = [s.reshape(-1, 1, 3) for s in sample if s.size]
    pal = _palette_of(sample, colors=colors, seed=seed)
    sizes = {}
    for n, (p, a) in pictures.items():
        idx = _to_palette(grained[n], pal, seed=seed + 1, speckle=speckle)
        _save(_os.path.join(folder, n + ".png"), idx, pal, alpha=None if a is None else a)
        sizes[n] = _os.path.getsize(_os.path.join(folder, n + ".png"))
    return sizes

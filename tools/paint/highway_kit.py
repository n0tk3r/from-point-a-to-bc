"""Helpers the highway scene and its wagon share.

Paper is brush.Sheet with one difference: a thin mark (alpha under 1) is laid OVER what is already
drawn on the sheet, as a glaze is, where Sheet lets it replace what was there (and so lets whatever
the sheet is later laid on show through). Opaque marks behave exactly as on a Sheet."""

import numpy as np
from PIL import Image, ImageDraw

from brush import F32, Sheet, lerp, rgb


class Paper(Sheet):
    def _glaze(self, box, draw):
        w, h = self.im.size
        x0, y0 = max(int(box[0]) - 2, 0), max(int(box[1]) - 2, 0)
        x1, y1 = min(int(box[2]) + 3, w), min(int(box[3]) + 3, h)
        if x1 <= x0 or y1 <= y0:
            return self
        tmp = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        draw(ImageDraw.Draw(tmp), x0, y0)
        self.im.alpha_composite(tmp, (x0, y0))
        return self

    def poly(self, points, color, alpha=1.0):
        if alpha >= 0.999:
            return super().poly(points, color, alpha)
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        fill = self._fill(color, alpha)
        box = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
        return self._glaze(box, lambda d, ox, oy: d.polygon([(px - ox, py - oy) for px, py in pts], fill=fill))

    def ellipse(self, cx, cy, rx, ry, color, alpha=1.0):
        if alpha >= 0.999:
            return super().ellipse(cx, cy, rx, ry, color, alpha)
        s = self.ss
        fill = self._fill(color, alpha)
        box = ((cx - rx) * s, (cy - ry) * s, (cx + rx) * s, (cy + ry) * s)
        return self._glaze(box, lambda d, ox, oy: d.ellipse([box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy], fill=fill))

    def line(self, points, color, width=1.0, alpha=1.0, round_ends=True):
        if alpha >= 0.999:
            return super().line(points, color, width, alpha, round_ends)
        s = self.ss
        pts = [(float(x) * s, float(y) * s) for x, y in points]
        wd = max(1, int(round(width * s)))
        fill = self._fill(color, 1.0)
        box = (min(p[0] for p in pts) - wd, min(p[1] for p in pts) - wd, max(p[0] for p in pts) + wd, max(p[1] for p in pts) + wd)

        def draw(d, ox, oy):
            # drawn solid on its own scrap, then thinned as a whole, so that joints do not show double
            q = [(px - ox, py - oy) for px, py in pts]
            d.line(q, fill=fill, width=wd, joint="curve")
            if round_ends and wd > 2:
                r = wd / 2
                for px, py in (q[0], q[-1]):
                    d.ellipse([px - r, py - r, px + r, py + r], fill=fill)

        w, h = self.im.size
        x0, y0 = max(int(box[0]) - 2, 0), max(int(box[1]) - 2, 0)
        x1, y1 = min(int(box[2]) + 3, w), min(int(box[3]) + 3, h)
        if x1 <= x0 or y1 <= y0:
            return self
        tmp = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        draw(ImageDraw.Draw(tmp), x0, y0)
        a = tmp.getchannel("A").point(lambda v: int(v * alpha))
        tmp.putalpha(a)
        self.im.alpha_composite(tmp, (x0, y0))
        return self


def mix(a, b, t):
    a = rgb(a) if isinstance(a, str) else np.asarray(a, dtype=F32)
    b = rgb(b) if isinstance(b, str) else np.asarray(b, dtype=F32)
    return lerp(a, b, t)


def grade(picture, contrast=1.10, color=1.12, pivot=0.40):
    """The last glaze over a finished painting: a little more color, and the darks and lights pushed a
    little further apart (about `pivot`). Dusk wants it: the golds should burn and the violets go deep."""
    lum = (picture @ np.array([0.3, 0.55, 0.15], dtype=F32))[..., None]
    out = lum + (picture - lum) * color
    out = pivot + (out - pivot) * contrast
    return np.clip(out, 0, 1).astype(F32)

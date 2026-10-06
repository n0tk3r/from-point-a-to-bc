"""Build the Koine Road font from the pen skeletons in glyphs.py.

    python3 build.py            # writes ../../fonts/KoineRoad-Regular.ttf and .woff2
    python3 build.py some/path  # writes some/path.ttf and some/path.woff2

Needs: fonttools, shapely, numpy, brotli.
The build is deterministic: the same skeletons always give the same outlines.
"""
import os
import sys
import numpy as np
from shapely.ops import unary_union
from shapely import affinity
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString

import penlib
import glyphs as gl

FAMILY = "Koine Road"
STYLE = "Regular"
VERSION = "0.2"
UPM = 1000
WIDTH = 104         # pen width: about 1/6 of the letter height, as in Papyrus 46
PEN = dict(start=0.34, end=0.26, taper=0.10, lam=40.0, wobble=2.8, contrast=0.84, nib_angle=0.14)
ASCENT, DESCENT = 800, -260
SPACE = 250
NVAR = 3            # how many times each letter is "written"; text cycles through them

# Tuck round letters under overhanging bars and diagonals.
KERN = {
    ("T", "O"): -46, ("T", "A"): -56, ("A", "T"): -34, ("V", "O"): -30, ("Y", "O"): -42,
    ("F", "O"): -22, ("F", "A"): -44, ("P", "O"): -16, ("P", "A"): -40, ("A", "V"): -44,
    ("V", "A"): -54, ("A", "Y"): -44, ("Y", "A"): -56, ("L", "T"): -52, ("L", "Y"): -44,
    ("L", "V"): -40, ("A", "W"): -20, ("W", "A"): -30, ("T", "C"): -30, ("T", "E"): -30,
    ("K", "O"): -18, ("R", "O"): -10, ("O", "T"): -18, ("O", "Y"): -22, ("O", "V"): -16,
    ("T", "period"): -60, ("P", "period"): -70, ("F", "period"): -70, ("V", "period"): -60,
    ("Y", "period"): -60, ("T", "comma"): -60, ("P", "comma"): -70,
}
# A capital followed by lowercase: small letters slide under the capital's overhang.
for cap, groups in {
    "T": {"acdegoqs": -70, "mnpruvwxyz": -52},
    "Y": {"acdegoqs": -62, "mnprsu": -42},
    "V": {"acdegoq": -40, "ru": -22},
    "F": {"acdegoq": -36, "ru": -18},
    "P": {"acdegoq": -22},
    "W": {"acdegoq": -18},
    "A": {"vwy": -24, "t": -10},
    "L": {"vwy": -32},
    "K": {"eo": -12},
}.items():
    for letters, value in groups.items():
        for low in letters:
            KERN[(cap, low)] = value
# Lowercase pairs.
for first, groups in {
    "r": {"acdegoq": -14},
    "f": {"aeo": -8},
    "k": {"eo": -8},
    "v": {"aeo": -10}, "w": {"aeo": -8}, "y": {"aeo": -10},
}.items():
    for letters, value in groups.items():
        for low in letters:
            KERN[(first, low)] = value
for first in "rfvwy":
    KERN[(first, "period")] = -50
    KERN[(first, "comma")] = -50


def make_shape(name, spec, variant):
    """Ink one writing of one letter. Variant 0 is the careful one."""
    rng = np.random.default_rng(penlib.seed_for(name, variant, "shape"))
    jitter = 2.0 if variant == 0 else 5.5
    opts = dict(PEN)
    opts.update(spec["opts"])
    pool = opts.pop("pool", 9.0)     # how far ink fills the corners where strokes meet
    parts = []
    for stroke in spec["strokes"]:
        sopts = dict(opts)
        if stroke and isinstance(stroke[0], dict):   # per-stroke pen options
            sopts.update(stroke[0])
            stroke = stroke[1:]
        pts = []
        for p in stroke:
            jx, jy = rng.normal(0, jitter, 2)
            pts.append((p[0] + jx, p[1] + jy) + tuple(p[2:]))
        parts.append(penlib.stroke_polygon(penlib.build_path(pts), WIDTH, rng, **sopts))
    for (x, y, r) in spec["dots"]:
        parts.append(penlib.dot_polygon(x + rng.normal(0, 2), y + rng.normal(0, 2), r, rng))
    shape = penlib.ink(unary_union(parts), rng, pool=pool, rough=2.4, rough_scale=34.0, simplify=0.55)
    # each time the scribe writes a letter it sits a little differently
    rot = rng.normal(0, 0.7 if variant == 0 else 1.6)
    sc = 1.0 + rng.normal(0, 0.01 if variant == 0 else 0.028)
    dy = rng.normal(0, 3 if variant == 0 else 9)
    minx, _, maxx, _ = shape.bounds
    return penlib.transform(shape, rot, sc, 0, dy, origin=((minx + maxx) / 2, 300))


def draw(shape, lsb):
    """Turn an inked shape into a TrueType glyph; returns (glyph, ink width)."""
    minx, _, maxx, _ = shape.bounds
    shape = affinity.translate(shape, lsb - minx, 0)
    pen = TTGlyphPen(None)
    for poly in penlib.polygons(shape):
        for ring in [poly.exterior] + list(poly.interiors):
            pts = [(int(round(x)), int(round(y))) for x, y in list(ring.coords)[:-1]]
            clean = [pts[0]]
            for p in pts[1:]:            # rounding can create repeated points
                if p != clean[-1]:
                    clean.append(p)
            if len(clean) > 1 and clean[0] == clean[-1]:
                clean.pop()
            if len(clean) < 3:
                continue
            pen.moveTo(clean[0])
            for p in clean[1:]:
                pen.lineTo(p)
            pen.closePath()
    return pen.glyph(), (maxx - minx)


def notdef():
    pen = TTGlyphPen(None)
    for ring in ([(60, 0), (60, 620), (440, 620), (440, 0)], [(110, 50), (390, 50), (390, 570), (110, 570)]):
        pen.moveTo(ring[0])
        for p in ring[1:]:
            pen.lineTo(p)
        pen.closePath()
    return pen.glyph()


def variants(name):
    return [name] + [f"{name}.alt{v}" for v in range(1, NVAR)]


def main(out_prefix):
    order = [".notdef", "space"]
    glyf = {".notdef": notdef(), "space": TTGlyphPen(None).glyph()}
    metrics = {".notdef": (500, 60), "space": (SPACE, 0)}
    for name, spec in gl.G.items():
        for v, gname in enumerate(variants(name)):
            g, w = draw(make_shape(name, spec, v), spec["lsb"])
            glyf[gname] = g
            metrics[gname] = (int(round(w + spec["lsb"] + spec["rsb"])), spec["lsb"])
            order.append(gname)

    cmap = {32: "space", 0xA0: "space"}
    for ch in gl.LETTERS + gl.LOWER:
        cmap[ord(ch)] = ch
    for ch, name in gl.CMAP.items():
        cmap[ord(ch)] = name

    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyf)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=ASCENT, descent=DESCENT)
    fb.setupNameTable({
        "familyName": FAMILY, "styleName": STYLE,
        "uniqueFontIdentifier": f"{FAMILY} {STYLE} {VERSION}",
        "fullName": f"{FAMILY} {STYLE}", "psName": f"{FAMILY.replace(' ', '')}-{STYLE}",
        "version": f"Version {VERSION}",
        "description": "Display face for the game From Point A to B.C. Latin majuscules drawn in the "
                       "manner of Greek papyrus book hands of the second and third centuries.",
    })
    fb.setupOS2(sTypoAscender=ASCENT, sTypoDescender=DESCENT, sTypoLineGap=0,
                usWinAscent=ASCENT + 20, usWinDescent=-DESCENT + 20,
                sxHeight=480, sCapHeight=636, achVendID="PTAB")
    fb.setupPost()

    names = list(gl.G)
    fea = [f"@v{v} = [{' '.join(variants(n)[v] for n in names)}];" for v in range(NVAR)]
    fea.append(f"@lower = [{' '.join(gl.LOWER)}];")
    fea.append("feature calt {")
    # The small O is the manuscript form. A capital O that starts a lowercase word grows to full height.
    fea += ["    lookup capO {", "        sub O' @lower by O.cap;", "    } capO;"]
    # A scribe never writes a letter the same way twice: cycle through the writings.
    fea.append("    lookup cycle {")
    fea += [f"        sub @v{v - 1} @v0' by @v{v};" for v in range(1, NVAR)]
    fea += ["    } cycle;", "} calt;"]
    fea.append("feature kern {")
    fea += [f"    pos [{' '.join(variants(a))}] [{' '.join(variants(c))}] {val};" for (a, c), val in KERN.items()]
    fea.append("} kern;")
    addOpenTypeFeaturesFromString(fb.font, "\n".join(fea))

    os.makedirs(os.path.dirname(os.path.abspath(out_prefix)), exist_ok=True)
    fb.save(out_prefix + ".ttf")
    font = TTFont(out_prefix + ".ttf")
    font.flavor = "woff2"
    font.save(out_prefix + ".woff2")
    print(f"{FAMILY} {VERSION}: {len(order)} glyphs, {len(cmap)} characters, "
          f"ttf {os.path.getsize(out_prefix + '.ttf')} bytes, woff2 {os.path.getsize(out_prefix + '.woff2')} bytes")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "..", "fonts", "KoineRoad-Regular"))

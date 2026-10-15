"""The map of Rome, 44 B.C. (round fifteen, MAP-15R): a wax tablet with the boy's plan scratched into it.

The map screen (MAP-15.md) lays these pictures over one another: back.png (the tablet, the Tiber's bend and the
Capitol's hill, which anyone would know before setting foot anywhere), then a path-<a>-<b>.png for each way, then a
place-<id>.png for each place, each as visited, faint (0.28) or not there; the engine writes the names and stands the
portraits. Every picture is 800 x 600, the stage, with the tablet within x 40 to 760, y 136 to 564.

PLAN
  Light     From the upper left, soft, as on a table by a window (map_rome_sheet.py has the tablet's; map_rome_kit.cut
            the scratches': a groove's upper-left wall in shade, its lower-right wall lit, the burr bright on the
            upper-left side of a line and dark on the other).
  Tones     LIGHT  the scratches of the plan, where the eye goes, and the frame's worn wood round it.
            DARK   the wax: deep brown to near black, warmer where it is thick, calm enough to read names on.
  Places    the treasury above the temple's front (its door just over the roof), the temple's front in the middle,
            the street coming in from the left, the Capitol's hill at the upper right with Jupiter's temple on its
            top, the Forum's long square below, the Tiber's bend at the lower left and the far bank inside it, the stone
            bridge between. (map_rome_places.py draws them.)

  python3 map_rome.py fast    the passes without the brush and the palette: out/map-rome-fast.png, to look at
  python3 map_rome.py         everything into out/map-rome/ (the pictures, then layout.json from them), and
                              map_rome_check.py's checks and its four pictures into out/map-rome-check/

Each picture is cut from the same finished tablet, so a place laid over the sheet matches it pixel for pixel; one
palette (brush.palette_of over the tablet with every place and way laid on it) for all of them."""

import os
import sys
import time

import numpy as np
from PIL import Image

from brush import F32, grain, lerp, palette_of, save, to_palette
import map_rome_places as PL
import map_rome_sheet as SH
from map_rome_kit import OUT, Stylus, cut

COLORS = 200          # the map's palette
GRAIN = 0.018         # pigment grain
SPECKLE = 0.012


def layer(draw, base, panel, seed):
    """One place, way or the land: drawn with a stylus, cut into the tablet. -> (picture, hard mask)"""
    st = Stylus(seed=seed)
    draw(st)
    cov, dep = st.masks()
    cov = cov * panel                                  # the stylus only marks the wax
    pic, changed = cut(base, cov, dep, seed=seed)
    return pic, (changed >= 0.5).astype(F32)


def paint(fast=False):
    """-> (sheet, board mask, {file name: (picture, mask)}), all at picture size, before the finish."""
    t0 = time.time()
    pic, info = SH.under()
    pic = SH.brushed(pic, info, fast)
    pic = SH.details(pic, info)
    print("tablet", round(time.time() - t0, 1))
    panel = info["in_panel"]
    sheet, _ = layer(PL.land, pic, panel, seed=90)
    layers = {}
    for i, ((a, b), draw) in enumerate(PL.WAYS.items()):
        layers[f"path-{a}-{b}.png"] = layer(draw, sheet, panel, seed=200 + i)
    for i, (pid, draw) in enumerate(PL.PLACES.items()):
        layers[f"place-{pid}.png"] = layer(draw, sheet, panel, seed=100 + i)
    print("scratched", round(time.time() - t0, 1))
    board = (info["on_board"] >= 0.5).astype(F32)
    return sheet, board, layers


def composite(sheet, layers, names=None, amount=None):
    """The sheet with layers laid on in the engine's order (ways, then places). `amount` gives each name's opacity."""
    out = sheet.copy()
    order = [n for n in layers if n.startswith("path-")] + [n for n in layers if n.startswith("place-")]
    for n in order:
        if names is not None and n not in names:
            continue
        pic, m = layers[n]
        a = m * (1.0 if amount is None else amount.get(n, 1.0))
        out = lerp(out, pic, a[..., None])
    return out


def finish(sheet, board, layers):
    """Grain (the same on every picture, so that they agree where they overlap), one palette, and the files."""
    os.makedirs(OUT, exist_ok=True)
    g_sheet = grain(sheet, 7, GRAIN)
    grained = {n: (grain(p, 7, GRAIN), m) for n, (p, m) in layers.items()}
    whole = composite(g_sheet, grained)
    scratches = np.concatenate([p[m > 0.5] for p, m in grained.values()])
    pal = palette_of([whole[board > 0.5].reshape(-1, 1, 3), scratches.reshape(-1, 1, 3)], colors=COLORS)
    sizes = {}
    idx = to_palette(g_sheet, pal, speckle=SPECKLE)
    save(f"{OUT}/back.png", idx, pal, board)
    sizes["back.png"] = os.path.getsize(f"{OUT}/back.png")
    for n, (p, m) in grained.items():
        idx = to_palette(p, pal, speckle=SPECKLE)
        save(f"{OUT}/{n}", idx, pal, m)
        sizes[n] = os.path.getsize(f"{OUT}/{n}")
    return pal, sizes


def main():
    fast = len(sys.argv) > 1 and sys.argv[1] == "fast"
    t0 = time.time()
    sheet, board, layers = paint(fast)
    if fast:
        os.makedirs("out", exist_ok=True)
        whole = composite(sheet, layers) * board[..., None] + (1 - board[..., None]) * np.array([0.16, 0.17, 0.22], F32)
        Image.fromarray((np.clip(whole, 0, 1) * 255).astype(np.uint8)).save("out/map-rome-fast.png")
        print("fast: out/map-rome-fast.png", round(time.time() - t0, 1))
        return
    pal, sizes = finish(sheet, board, layers)
    print("palette", len(pal), "colours; files", sum(sizes.values()), "bytes")
    for n in sorted(sizes):
        print(f"  {n:28s} {sizes[n]:8d}")
    import map_rome_layout as LY
    LY.write(f"{OUT}/layout.json")
    import map_rome_check as CK
    ok = CK.main()
    print("done", round(time.time() - t0, 1), "checks", "passed" if ok else "FAILED")


if __name__ == "__main__":
    main()

"""The crane's great wheel in the Forum, turning: painted frames (crane-0.png ... crane-5.png), cropped, with the point
of the picture they stand at, as the cat on her sill in the street is (rome_street_four.py).

Each frame is the finished backdrop itself round the wheel, with the wheel painted a sixth of a spoke further round:
painted into the picture as it was before the crane was drawn, finished with the backdrop's own grain and palette, and
cut out round the wheel's rim. So everywhere but the spokes it is back.png pixel for pixel, and frame 0 is the wheel as
the backdrop has it. Played in a loop the wheel turns steadily (8 spokes: six frames make one spoke's turn)."""

import numpy as np
from PIL import Image

from brush import F32, grain, over, save, to_palette, mask_ellipse
import rome_forum_far as far_

N = 6


def wheel_frames(before, pal, out_dir, back_idx):
    """`before`: the picture as it was just before the crane was painted into it (floats); `pal` back.png's palette;
    `back_idx` back.png's own palette indexes. -> (files, plane mark for the scene, frame 0 the same as the backdrop?)"""
    files = []
    fr0, wh0, (wc, R) = far_.crane_parts(0.0)
    x0, x1 = int(wc[0] - R * 0.42 - 3), int(wc[0] + R * 0.42 + 4)
    y0, y1 = int(wc[1] - R - 3), int(wc[1] + R + 4)
    rim = mask_ellipse(before.shape[:2], wc[0], wc[1], R * 0.42 + 0.6, R + 0.6) > 0.35
    clear = len(pal)
    same = None
    for n in range(N):
        fr, wh, _ = far_.crane_parts(n / N)
        p = before.copy()
        for sh in (wh, fr):
            sc, sa = sh.done()
            over(p, sc, sa)
        idx = to_palette(grain(p, 7, 0.02), pal, speckle=0.014)
        frame = np.full(idx.shape, clear, np.uint8)
        frame[rim] = idx[rim]
        if n == 0:
            same = bool((idx[rim] == back_idx[rim]).all())
        crop = frame[y0:y1, x0:x1]
        name = f"crane-{n}.png"
        save(f"{out_dir}/{name}", crop, pal, (crop != clear).astype(F32))
        files.append(name)
    foot = [int(round(wc[0])) - x0, int(round(wc[1] + R)) - y0]
    at = [int(round(wc[0])), int(round(wc[1] + R))]
    from rome_forum_model import HOARD, pt
    # Its base is not its own foot (row 360) but a row just above the hoarding's far end: the wheel stands behind the
    # hoarding, and so it must sort behind anyone standing in front of the hoarding anywhere along it, the far end
    # included (with its own foot, the engine's comparison went round in a circle for someone there: in front of the
    # boards, behind the wheel's row, and the wheel behind the boards).
    base = round(pt(HOARD["b"][0], 0, HOARD["b"][1])[1] - 2.0, 1)
    plane = {"id": "crane-wheel", "frames": files, "fps": 3, "at": at, "foot": foot, "size": [x1 - x0, y1 - y0], "base": base,
             "what": "the crane's great wheel, turning slowly: frames crane-0 to crane-5 in a loop (frame 0 is the wheel as back.png has it)",
             "note": "Behind the hoarding (its base is a row just above the hoarding's far end, so that it sorts behind everyone in front of the boards). The block hanging from the crane is painted and does not "
                     "rise, so the wheel is best turned now and then, for a few seconds, and stopped: the dust (crane-dust) can follow it."}
    return files, plane, same

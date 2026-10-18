"""The full run of office_lot.py (OFFICE-17A): the backdrop and every cut-out, state and frame written into out/office-lot/
as palette PNGs, layout.json (office_lot_layout.py), and the pictures to look at (out/office-lot-*.png).

The files (all 800 x 600 and laid at 0, 0 unless cropped):
    back.png            the lot complete with everything that moves or changes taken away (the awning's and the
                        flagpole's shadows lie on it; the can's goes with the can)
    grille.png          the intake grille on the unit, its louvre slits cut clear (the fan shows through them)
    nut-1 .. nut-4.png  its four wing nuts, each a cut-out of its own (1 and 2 low, 3 and 4 high), so that they can
                        come off one by one
    switch.png          the maintenance switch's lever, up (on)
    door.png            the front door, shut
    awning.png          the little flat awning over it
    trash.png           the trash can, standing by the wall, with its own shadow
    flagpole.png        the flagpole on its foot (the pennant is frames)
    limo.png            the limousine, parked, in this light (office_lot_limo.py)
    front.png           sagebrush in the bottom corners (the front plane)
  states (alts):
    grille-off.png      the grille off, leaning against the unit left of its opening, the four nuts in a row by it
    switch-off.png      the lever pulled down (off)
    door-open.png       the door swung in, the hall inside
    trash-tipped.png    the can on its side on the gravel, its mouth toward us, the lid off on its chain
    trash-pipe.png      the can standing under the drainpipe's elbow (the elbow is laid over it again: it is in front)
    limo-door-open.png  the limousine with its rear door open
  frames (cropped, with a foot point):
    fan-0 .. fan-3      the fan behind the grille turning (12 a second); stopped, it is the backdrop's own
    pennant-0 .. 3      the pennant stirring at the top of the pole (3 a second)"""

import json
import os
import time

import numpy as np
from PIL import Image

from brush import F32, over
import office_lot as L
import office_lot_kit as K

OUT = L.OUT
COLORS = {"back": 160, "grille": 40, "switch": 16, "door": 40, "awning": 24, "trash": 48, "flagpole": 24, "limo": 96, "front": 40,
          "grille-off": 40, "switch-off": 16, "door-open": 48, "trash-tipped": 48, "trash-pipe": 48, "limo-door-open": 96}


def write(pic, info, cuts, t0):
    sizes = {}
    sizes["back"] = L.finish(pic, f"{OUT}/back.png", COLORS["back"])
    # the can under the pipe: the elbow is in front of it, so it is laid over the can again (the same drawing)
    c, a = cuts["trash-pipe"]
    s, sl = L.small_things()
    ec, ea = s.done()
    elc, ela = sl.done()
    elbow = elbow_mask()
    over(c, ec, ea * elbow * (a > 0.5))
    over(c, elc, ela * elbow * (a > 0.5))
    for name, (c, a) in cuts.items():
        n = COLORS.get(name, 16)
        sizes[name] = L.finish(c, f"{OUT}/{name}.png", n, (a > 0.5).astype(F32), seed=11 + len(name))
    print("pictures", round(time.time() - t0, 1), sizes)
    # the frames
    fans = L.fan_frames(pic)
    for i, (c, a) in enumerate(fans):
        L.finish(c, f"{OUT}/fan-{i}.png", 24, (a > 0.5).astype(F32), seed=60 + i, speckle=0.006, amount=0.008)
    fan = L.crop_frames([f"fan-{i}.png" for i in range(len(fans))])
    pens = L.pennant_frames(pic)
    for i, (c, a) in enumerate(pens):
        L.finish(c, f"{OUT}/pennant-{i}.png", 16, (a > 0.5).astype(F32), seed=70 + i, speckle=0.006, amount=0.008)
    pennant = L.crop_frames([f"pennant-{i}.png" for i in range(len(pens))])
    print("frames", round(time.time() - t0, 1), fan, pennant)
    import office_lot_layout
    lay = office_lot_layout.write(info, cuts, {"fan": fan, "pennant": pennant})
    comps(lay)
    print("layout and comps", round(time.time() - t0, 1))
    import subprocess, sys
    subprocess.run([sys.executable, "office_lot_check.py"])
    print("done", round(time.time() - t0, 1))


def elbow_mask():
    """The drainpipe's elbow and mouth, where they lie over the can that stands under them."""
    from brush import mask_poly
    my, mz = K.PIPE["mouth"]
    x0, x1 = K.PIPE["x"] - K.PIPE["r"] - 2, K.PIPE["x"] + K.PIPE["r"] + 2
    pts = [K.P(x0, K.PIPE["elbow"] + 14, K.PIPE["z"]), K.P(x1, K.PIPE["elbow"] + 14, K.PIPE["z"]), K.P(x1, my - K.PIPE["r"] - 2, mz - 2),
           K.P(x0, my - K.PIPE["r"] - 2, mz - 2)]
    return (mask_poly(L.SHAPE, pts) > 0.3).astype(F32)


def comps(lay):
    """The scene's pictures laid together as the game lays them: first (everything in its first state, the pennant's and
    the fan's first frames), and later (the grille off, the switch off, the can under the pipe, the doors open)."""
    def put(im, f, at=None, foot=None):
        top = Image.open(f"{OUT}/{f}").convert("RGBA")
        if at is None:
            im.alpha_composite(top)
        else:
            im.alpha_composite(top, (int(at[0] - foot[0]), int(at[1] - foot[1])))
    fx = {f["id"]: f for f in lay["fx"]}
    for state, show in (("comp", ["grille", "nut-1", "nut-2", "nut-3", "nut-4", "switch", "door", "awning", "trash", "flagpole", "limo", "front"]),
                        ("comp-later", ["grille-off", "switch-off", "door-open", "awning", "trash-pipe", "flagpole", "limo-door-open", "front"]),
                        ("comp-tipped", ["grille", "nut-1", "nut-2", "nut-3", "nut-4", "switch", "door", "awning", "trash-tipped", "flagpole", "limo-door-open", "front"])):
        im = Image.open(f"{OUT}/back.png").convert("RGBA")
        if state == "comp-later":
            pass                                                   # (the fan stopped: the backdrop's own)
        else:
            put(im, fx["fan"]["frames"][0], fx["fan"]["at"], fx["fan"]["foot"])
        for name in show:
            put(im, name + ".png")
            if name == "flagpole":
                put(im, fx["pennant"]["frames"][0], fx["pennant"]["at"], fx["pennant"]["foot"])
        im.convert("RGB").save(f"out/office-lot-{state}.png")

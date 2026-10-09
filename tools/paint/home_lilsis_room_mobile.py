"""Round four: Little Sister's mobile of felt chickens, made its own cut-out so that the game can stir it.

    python3 home_lilsis_room_mobile.py      splits out/home-lilsis-room/front.png (as home_lilsis_room.py finishes it)

The mobile hangs from a rafter in front of everything, and was painted into front.png with the toy box, the crate,
the hen house, the nest and the door. Nothing else of front.png lies near it, so it is lifted out by its own pixels:
mobile.png is every painted pixel of front.png inside MOBILE_BOX, and front.png keeps all the others. Both keep
front.png's palette, and laid together (in either order) they are the old front.png exactly. back.png was always
painted without the front plane, so the room behind the mobile is there already."""

import os
import sys

import numpy as np
from PIL import Image

OUT = "out/home-lilsis-room"
MOBILE_BOX = (515, 195, 630, 320)            # x0, y0, x1, y1: the mobile (painted x 540..600, y 215..302) and a margin; nothing else of front.png is near


def split(folder=OUT):
    """front.png -> front.png without the mobile, and mobile.png. -> (pixels moved, box of the mobile's paint)."""
    src = Image.open(f"{folder}/front.png")
    assert src.mode == "P" and "transparency" in src.info, "front.png should be a palette picture with a clear index"
    clear = src.info["transparency"]
    pal = src.getpalette()
    idx = np.asarray(src).copy()
    x0, y0, x1, y1 = MOBILE_BOX
    inside = np.zeros(idx.shape, bool)
    inside[y0:y1, x0:x1] = True
    painted = idx != clear
    edge = np.zeros(idx.shape, bool)                                    # (if anything painted touches the box's edge, the box is wrong)
    edge[y0:y1, x0:x1] = True
    edge[y0 + 1:y1 - 1, x0 + 1:x1 - 1] = False
    assert not (painted & edge).any(), "something painted crosses MOBILE_BOX's edge"
    mobile = np.where(inside, idx, clear).astype(np.uint8)
    rest = np.where(inside, clear, idx).astype(np.uint8)
    for name, part in (("mobile", mobile), ("front", rest)):
        im = Image.fromarray(part, "P")
        im.putpalette(pal)
        im.save(f"{folder}/{name}.png", optimize=True, transparency=clear)
    ys, xs = np.nonzero(painted & inside)
    return int((painted & inside).sum()), [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else OUT
    if os.path.exists(f"{folder}/mobile.png"):
        print("mobile.png is there already: front.png has been split (run home_lilsis_room.py first to paint it whole again)")
        sys.exit()
    print("moved", *split(folder))

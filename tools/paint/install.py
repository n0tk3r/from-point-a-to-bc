#!/usr/bin/env python3
"""Copy a painted scene from this folder's out/ into the game's art/ folder.

    python3 install.py rome-street        one scene
    python3 install.py items              the inventory pictures
    python3 install.py                    everything that has been painted

It copies every PNG and the layout.json, and says what changed. Run tools/stamp.py afterwards.
"""

import filecmp
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "..", "..", "art")
# out/<folder> -> art/<place>. (The first scene painted kept its working name, egypt1.)
PLACES = {"egypt1": "scenes/egypt-crash", "items": "items"}
# Everything that `python3 install.py` installs, in the order of the story.
SCENES = [
    "highway",
    "egypt1", "egypt-site", "egypt-gallery", "egypt-chamber",                                 # Act One
    "rome-street", "rome-steps", "rome-temple",                                               # Act Two
    "home-living-room", "home-landing", "home-study", "home-lilsis-room", "home-bigsis-room",  # Act Three: the house
    "nevada-roadside",                                                                        # Act Four
    "items",
]


def install(name):
    folder = {"egypt-crash": "egypt1"}.get(name, name)
    src = os.path.join(HERE, "out", folder)
    if not os.path.isdir(src):
        print(f"{name}: nothing painted yet (no out/{folder}/)")
        return 0
    dst = os.path.join(ART, PLACES.get(folder, "scenes/" + folder))
    os.makedirs(dst, exist_ok=True)
    changed = 0
    for f in sorted(os.listdir(src)):
        if not (f.endswith(".png") or f == "layout.json"):
            continue
        a, b = os.path.join(src, f), os.path.join(dst, f)
        if os.path.exists(b) and filecmp.cmp(a, b, shallow=False):
            continue
        shutil.copyfile(a, b)
        changed += 1
        print(f"  {os.path.relpath(b, os.path.join(HERE, '..', '..'))}")
    print(f"{name}: {changed} file{'s' if changed != 1 else ''} changed")
    return changed


if __name__ == "__main__":
    total = sum(install(n) for n in (sys.argv[1:] or SCENES))
    if total:
        print("Now run: python3 tools/stamp.py")

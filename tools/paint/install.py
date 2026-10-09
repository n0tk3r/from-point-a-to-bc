#!/usr/bin/env python3
"""Copy a painted scene from this folder's out/ into the game's art/ folder, in the game's paints.

    python3 install.py rome-street        one scene
    python3 install.py items              the inventory pictures
    python3 install.py                    everything that has been painted
    python3 install.py --raw rome-street  as painted, without the paints (to compare: never leave it so)

A scene's pictures are keyed on the way in (postimp_key.py: the scene's every picture file mixed from the game's paint
box in its key, at strength 50; see the README, "The paints"), then copied with its layout.json; it says what changed,
and notes in postimp_keyed.json what each file was keyed from. The inventory pictures are the interface's and go in as
painted. Run tools/stamp.py afterwards.
"""

import filecmp
import os
import shutil
import sys
import tempfile

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


def install(name, raw=False):
    folder = {"egypt-crash": "egypt1"}.get(name, name)
    src = os.path.join(HERE, "out", folder)
    if not os.path.isdir(src):
        print(f"{name}: nothing painted yet (no out/{folder}/)")
        return 0
    place = PLACES.get(folder, "scenes/" + folder)
    dst = os.path.join(ART, place)
    os.makedirs(dst, exist_ok=True)
    scene = place[len("scenes/"):] if place.startswith("scenes/") else None
    with tempfile.TemporaryDirectory() as keyed:
        pictures = src
        if scene and not raw:                          # the game's paints: key the painting on the way in
            import postimp_key
            postimp_key.key_scene(scene, src, keyed)
            pictures = keyed
        changed = 0
        for f in sorted(os.listdir(src)):
            if not (f.endswith(".png") or f == "layout.json"):
                continue
            a, b = os.path.join(pictures if f.endswith(".png") else src, f), os.path.join(dst, f)
            if os.path.exists(b) and filecmp.cmp(a, b, shallow=False):
                continue
            shutil.copyfile(a, b)
            changed += 1
            print(f"  {os.path.relpath(b, os.path.join(HERE, '..', '..'))}")
        if scene and not raw:
            import postimp_key
            postimp_key.record(scene, src, dst, [f for f in os.listdir(src) if f.endswith(".png")])
        elif scene:
            print(f"{name}: installed WITHOUT the paints (--raw): install it again without --raw before it ships")
    print(f"{name}: {changed} file{'s' if changed != 1 else ''} changed")
    return changed


if __name__ == "__main__":
    raw = "--raw" in sys.argv
    names = [a for a in sys.argv[1:] if a != "--raw"]
    total = sum(install(n, raw) for n in (names or SCENES))
    if total:
        print("Now run: python3 tools/stamp.py")

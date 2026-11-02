"""Checks on the foot of Mount Shosha as painted (out/edo-shosha/) or as installed (art/scenes/edo-shosha/), and the
pictures to look at, in both lights. PAINT-21E.

  python3 edo_shosha_check.py [out|art] [shots_dir]
      the sizes, every file of the plan, hard edges, every mark inside the walk, every thing of ROUND-21.md's list with
      a shape, the stands; then <shots_dir>/shosha-layout-<which>.png and, with the game served on port 8935,
      <shosha-people-gold|sunset-<which>.png>: the three of them before the hall and at the lock, O-Ume, Ryokai on his
      step, the women on the bench (round twenty's people at their heights), the doors shut (gold) and open (sunset)."""

import json
import os
import sys

from edo_town_check import check_files, check_layout, layout_picture, people_picture, HERE

NEEDED = ["mountain", "pathup", "stone", "trees", "cherry", "hall", "doors", "lock", "slips", "step", "stepball", "lattice", "hut", "lantern",
          "bench", "combs", "plain", "castle", "sky", "ume", "ryokai", "tome", "wife", "girl"]
MARKS = ["road", "stone", "path", "ryokai", "hall", "lock", "step", "ume", "hut", "bench", "tome", "wife", "girl", "view"]


def folk(lay):
    M = lay["marks"]
    return [
        ("mom-edo", M["hall"][0] - 6, M["hall"][1] + 2, 180, 0, 0, 0, "stand"), ("bigsis-edo", M["hall"][0] - 44, M["hall"][1] + 10, 150, 0, 0, 0, "stand"),
        ("lilsis-edo", M["lock"][0] + 18, M["lock"][1], 180, 0, 0, 0, "stand"),
        ("sei", M["ume"][0], M["ume"][1], 270, 136, 0, 0, "stand"),
        ("tokuzo", M["ryokai"][0], M["ryokai"][1], 90, 150, 0, 0, "sit"),
        ("sei", M["tome"][0], M["tome"][1], 0, 138, 0, 0, "sit"), ("tami-baby", M["wife"][0], M["wife"][1], 0, 146, 0, 0, "sit"),
        ("orin", M["girl"][0], M["girl"][1], 0, 138, 0, 0, "sit"),
        ("mom-edo", M["road"][0], M["road"][1], 270, 0, 0, 0, "stand"), ("lilsis-edo", M["path"][0], M["path"][1], 180, 0, 0, 0, "stand"),
        ("bigsis-edo", M["view"][0], M["view"][1], 90, 0, 0, 0, "stand"),
    ]


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "out"
    shots = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "out")
    folder = os.path.join(HERE, "out", "edo-shosha") if which == "out" else os.path.join(HERE, "..", "..", "art", "scenes", "edo-shosha")
    os.chdir(HERE)
    bad = check_files("edo-shosha", folder)
    lay = json.load(open(os.path.join(folder, "layout.json")))
    bad += check_layout(lay, NEEDED, MARKS)
    print("CHECK edo-shosha", which, "OK" if not bad else "")
    for b in bad:
        print("  ", b)
    os.makedirs(shots, exist_ok=True)
    layout_picture("edo-shosha", folder, lay, os.path.join(shots, f"shosha-layout-{which}.png"))
    bases = {pl["id"]: pl.get("base", -1 if pl.get("plane") == "back" else 10000) for pl in lay["planes"]}
    sunset_bases = dict(bases)
    for k in list(bases):
        sunset_bases[k + "-sunset"] = bases[k]
    sunset_bases["doors-open-sunset"] = bases["doors"]
    sunset_bases["sunset"] = -2
    try:
        people_picture("edo-shosha", folder, lay, folk(lay), os.path.join(shots, f"shosha-people-gold-{which}.png"))
        people_picture("edo-shosha", folder, lay, folk(lay), os.path.join(shots, f"shosha-people-sunset-{which}.png"),
                       extra=["sunset", "doors-open-sunset", "lock-open-sunset", "stone-sunset", "bench-sunset", "pine-sunset"],
                       without=["doors", "lock", "stepball", "stone", "bench", "pine"], planes_base=sunset_bases)
    except Exception as e:
        print("no people shot:", e)

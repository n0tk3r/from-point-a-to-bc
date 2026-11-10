"""PAINT-23: the foot of Mount Shosha's numbers, written into js/content/scenes/edo-shosha.js from its layout.json (as
edo_shosha_layout.py measured them): the camera, the walk, the marks and places, the solids and bases, the effects, every
area's shape. Ids, logic and wording stay; only the numbers move. Run after `python3 edo_shosha.py` (and install.py).

    python3 edo_shosha_wire.py          rewrites the numbers in place and says which it changed"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SCENE = os.path.join(HERE, "..", "..", "js", "content", "scenes", "edo-shosha.js")
NIGHT = os.path.join(HERE, "..", "..", "js", "content", "cutscenes", "edo-night.js")


def j(v):
    return json.dumps(v)


def main():
    lay = json.load(open(os.path.join(HERE, "..", "..", "art", "scenes", "edo-shosha", "layout.json")))
    th = {t["id"]: t["shape"]["poly"] for t in lay["things"]}
    pl = {q["id"]: q for q in lay["planes"]}
    fx = {q["id"]: q for q in lay["fx"]}
    s = open(SCENE).read()
    before = s
    subs = [
        (r"const HORIZON = \d+, FULL = \d+;", f"const HORIZON = {lay['horizon']}, FULL = {lay['full']};"),
        (r"const FLOOR = \[\[.*?\]\];", f"const FLOOR = {j(lay['walk'])};"),
        (r"const M = \{ road:.*? \};", "const M = { " + ", ".join(f"{k}: {j(v)}" for k, v in lay["marks"].items()) + " };"),
        (r"const LATTICE = \[\d+, \d+\];", f"const LATTICE = {j(lay['LATTICE'])};"),
        (r"const DOORWAY = \[\d+, \d+\];", f"const DOORWAY = {j(lay['DOORWAY'])};"),
        (r"const HOMEWARD = \[\[.*?\]\];", f"const HOMEWARD = {j(lay['HOMEWARD'])};"),
        (r"const TALK_AT = \{ ryokai:.*? \};", "const TALK_AT = { " + ", ".join(f"{k}: {j(v)}" for k, v in lay["TALK_AT"].items()) + " };"),
        (r"const BOX = \{ ume:.*? \};", "const BOX = { " + ", ".join(f"{k}: {j(v)}" for k, v in lay["boxes"].items()) + " };"),
        (r"  blocked: \[\[\[.*?\]\]\],", f"  blocked: {j(lay['blocked'])},"),
        (r"  arrive: \{ road:.*? \},", "  arrive: { " + ", ".join(f"{k}: {j(v)}" for k, v in lay["arrive"].items()) + " },"),
        (r'walkTo: \[\d+, \d+\], use: stayUse', f"walkTo: {j(lay['edgeE'])}, use: stayUse"),
        (r'\{ id: "stone", base: \d+,', f'{{ id: "stone", base: {pl["stone"]["base"]},'),
        (r'state: \(g\) => \(red\(g\) \? "sunset" : "gold"\), solid: \[\[\d+, \d+\], \[\d+, \d+\], \[\d+, \d+\], \[\d+, \d+\]\] \},\n    // \(the bench',
         f'state: (g) => (red(g) ? "sunset" : "gold"), solid: {j(pl["stone"]["solid"])} }},\n    // (the bench'),
        (r'\{ id: "bench", base: \[\[.*?\]\], states', f'{{ id: "bench", base: {j(pl["bench"]["base"])}, states'),
        (r'"bench-sunset.png" \}, state: \(g\) => \(red\(g\) \? "sunset" : "gold"\), solid: \[\[.*?\]\] \},',
         f'"bench-sunset.png" }}, state: (g) => (red(g) ? "sunset" : "gold"), solid: {j(pl["bench"]["solid"])} }},'),
        (r'type: "petals", from: \[\[.*?\]\], floor: \d+,', f'type: "petals", from: {j(fx["petals"]["from"])}, floor: {fx["petals"]["floor"]},'),
        (r'type: "birds", lanes: \[\[\[.*?\]\]\],', f'type: "birds", lanes: {j(fx["crows"]["lanes"])},'),
        (r'\{ id: "sky", name: "sky", poly: \[\[.*?\]\],', f'{{ id: "sky", name: "sky", poly: {j(th["sky"])},'),
        (r'\{ id: "slips2", name: "name slips", poly: \[\[.*?\]\],', f'{{ id: "slips2", name: "name slips", poly: {j(th["slips2"])},'),
        (r'\{ id: "doors", name: "doors", poly: \[\[.*?\]\],', f'{{ id: "doors", name: "doors", poly: {j(th["doors"])},'),
        (r'\{ id: "doors", name: "open doors", verb: "Go in", poly: \[\[.*?\]\],', f'{{ id: "doors", name: "open doors", verb: "Go in", poly: {j(th["doors_open"])},'),
        (r'\{ id: "stepball", name: "rice ball on a leaf", poly: \[\[.*?\]\],', f'{{ id: "stepball", name: "rice ball on a leaf", poly: {j(th["stepball"])},'),
        (r'\{ id: "lock", name: "lock", verb: "Look closer at", poly: \[\[.*?\]\],', f'{{ id: "lock", name: "lock", verb: "Look closer at", poly: {j(th["lock"])},'),
        (r'rect: BOX\.lattice, walkTo: \[\d+, \d+\],', f"rect: BOX.lattice, walkTo: {j(lay['latticeTalk'])},"),
    ]
    for name in ("mountain", "plain", "castle", "trees", "cherry", "hut", "lantern", "pathup", "stone", "hall", "lattice", "slips", "step", "bench", "combs"):
        subs.append((r'thing\("' + name + r'", "([^"]*)", poly\(\[\[.*?\]\]\)', 'thing("' + name + r'", "\1", poly(' + j(th[name]) + ")"))
    for pat, rep in subs:
        s2, n = re.subn(pat, rep, s, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f"not found in the scene file: {pat[:70]}")
        s = s2
    if s != before:
        open(SCENE, "w").write(s)
        print("edo-shosha.js: numbers written")
    else:
        print("edo-shosha.js: no change")
    c = open(NIGHT).read()
    nu = lay["nightUme"]
    c2 = re.sub(r'addFigure\("ume", "ume", \d+, \d+, g\.sizeAt\(\d+, \d+\)\);\n  ume\.place\(\d+, \d+, g\.sizeAt\(\d+, \d+\)\);',
                f'addFigure("ume", "ume", {nu[0]}, {nu[1]}, g.sizeAt({nu[0]}, {nu[1]}));\n  ume.place({nu[0]}, {nu[1]}, g.sizeAt({nu[0]}, {nu[1]}));', c, count=1)
    if c2 != c:
        open(NIGHT, "w").write(c2)
        print("edo-night.js: O-Ume's place written")


if __name__ == "__main__":
    main()

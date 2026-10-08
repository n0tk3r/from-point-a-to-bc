"""Stand the game's own figures in Little Sister's room, sorted with the tea party as the game will sort them.

    python3 home_lilsis_room_people.py [fast] [name]   -> out/home-lilsis-room-people.png (or -people-<name>.png)

People whose feet are above the tea party's base line are laid down first, then the tea party, then the others,
then the front plane. (people_on.py needs the game's server on port 8765.)"""
import json
import subprocess
import sys

from PIL import Image

import home_lilsis_room_layout as LAY

fast = "fast" in sys.argv[1:]
names = [a for a in sys.argv[1:] if a != "fast"]
L = LAY.layout()
m = L["marks"]
SETS = {
    "": [("mom", "atWindow", 180), ("bigsis", "atChart", 180), ("lilsis", "atFlock", 270), ("lilsis", "atTeaParty", 90), ("mom", "atBed", 90), ("lilsis", "atFort", 270), ("bigsis", "atNest", 0), ("mom", "atDoor", 90)],
    "arrive": [("mom", "mom", 0), ("bigsis", "bigsis", 0), ("lilsis", "lilsis", 0)],
    "walk": [("mom", [330, 400], 0), ("bigsis", [470, 460], 270), ("lilsis", [560, 440], 90), ("lilsis", [300, 455], 0), ("mom", [440, 375], 0)],
}
which = names[0] if names else ""
folk = []
for who, at, yaw in SETS[which]:
    x, y = m[at] if isinstance(at, str) else at
    folk.append((who, x, y, yaw))
(bx0, by0), (bx1, by1) = L["planes"][2]["base"]


def behind(x, y):
    return y < by0 + (by1 - by0) * (x - bx0) / (bx1 - bx0)


if fast:
    mid, tea, front = "out/home-lilsis-room-fast-mid.png", "out/home-lilsis-room-fast-teaparty.png", "out/home-lilsis-room-fast-front.png"
else:
    im = Image.open("out/home-lilsis-room/back.png").convert("RGBA")
    for n in ("fort", "flashlight"):
        im.alpha_composite(Image.open(f"out/home-lilsis-room/{n}.png").convert("RGBA"))
    mid = "out/home-lilsis-room-mid.png"
    im.convert("RGB").save(mid)
    tea, front = "out/home-lilsis-room/teaparty.png", "out/home-lilsis-room/front.png"
out = "out/home-lilsis-room-people" + ("-" + which if which else "") + ".png"
tmp = "out/home-lilsis-room-people-tmp.png"
spec = lambda fs: ";".join(f"{w}|{x}|{y}|{yaw}" for w, x, y, yaw in fs)
far = [f for f in folk if behind(f[1], f[2])]
near = [f for f in folk if not behind(f[1], f[2])]
subprocess.run([sys.executable, "people_on.py", mid, "120", "440", spec(far) or "mom|-200|300|0", tmp, tea], check=True)
subprocess.run([sys.executable, "people_on.py", tmp, "120", "440", spec(near) or "mom|-200|300|0", out, front], check=True)
print(out)

"""The test that matters: the game's own figures standing in the finished room, far wall to front.
python3 home_bigsis_room_people.py [out.png]  (the game's server must be up on port 8765)"""
import json, os, subprocess, sys
from PIL import Image
OUT = "out/home-bigsis-room"
L = json.load(open(f"{OUT}/layout.json"))
im = Image.open(f"{OUT}/back.png").convert("RGBA")
im.alpha_composite(Image.open(f"{OUT}/desk.png").convert("RGBA"))
im.convert("RGB").save("out/home-bigsis-room-nofront.png")
S = {k: v["at"] for k, v in L["stands"].items()}
who = [("mom", "mom", 0), ("bigsis", "bigsis", 300), ("lilsis", "lilsis", 0),           # just up the ladder
       ("bigsis", "atbooks", 180), ("mom", "atsound", 90), ("lilsis", "atdesk", 180),  # at the far wall
       ("mom", "atbed", 90), ("lilsis", "atlamp", 270), ("bigsis", "middle", 0), ("mom", "front", 0)]
if len(sys.argv) > 2:
    who = [w for i, w in enumerate(who) if str(i) in sys.argv[2]]
folk = ";".join(f"{w}|{S[a][0]}|{S[a][1]}|{yaw}" for w, a, yaw in who)
out = sys.argv[1] if len(sys.argv) > 1 else "out/home-bigsis-room-people.png"
print(subprocess.run([sys.executable, "people_on.py", "out/home-bigsis-room-nofront.png", str(L["horizon"]), str(L["full"]), folk, out, f"{OUT}/front.png"], capture_output=True, text=True).stdout)
os.remove("out/home-bigsis-room-nofront.png")

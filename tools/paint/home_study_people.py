"""The test that matters: the game's own figures standing in the finished room, far wall to front.
python3 home_study_people.py [out.png]  (the game's server must be up on port 8765)"""
import json, os, subprocess, sys
from PIL import Image
OUT = "out/home-study"
L = json.load(open(f"{OUT}/layout.json"))
im = Image.open(f"{OUT}/back.png").convert("RGBA")
for n in ("desk", "screen-login", "note", "tape-out"):
    im.alpha_composite(Image.open(f"{OUT}/{n}.png").convert("RGBA"))
im.convert("RGB").save("out/home-study-nofront.png")
S = {k: v["at"] for k, v in L["stands"].items()}
who = [("mom", "mom", 0), ("bigsis", "bigsis", 60), ("lilsis", "lilsis", 0),          # just in from the landing
       ("dad", "atnote", 270), ("dad", "atmap", 180),                                # at the far wall
       ("mom", "atmachine", 270), ("bigsis", "atvault", 90), ("lilsis", "atglobe", 90), ("son", "frontright", 0)]
folk = ";".join(f"{w}|{S[at][0]}|{S[at][1]}|{yaw}" for w, at, yaw in who)
out = sys.argv[1] if len(sys.argv) > 1 else "out/home-study-people.png"
print(subprocess.run([sys.executable, "people_on.py", "out/home-study-nofront.png", str(L["horizon"]), str(L["full"]), folk, out, f"{OUT}/front.png"], capture_output=True, text=True).stdout)
os.remove("out/home-study-nofront.png")

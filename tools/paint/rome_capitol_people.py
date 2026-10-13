"""The game's own people, and the geese's frames, standing in the finished Capitol: to look at sizes and places.

  python3 rome_capitol_people.py [out/rome-capitol]   -> out/rome-capitol-people.png and out/rome-capitol-geese-in.png
  python3 rome_capitol_people.py ../game/art/scenes/rome-capitol   (the installed, keyed pictures) -> out/rome-capitol-installed-people.png ...

Uses rome_capitol_people_on.py (people_on.py pointed at this copy of the game, http://localhost:8822/). People who
stand behind a cut-out are drawn before it is laid on (the goose-keeper behind his pen's fence); the rest after."""

import json
import subprocess
import sys

from PIL import Image

D = sys.argv[1] if len(sys.argv) > 1 else "out/rome-capitol"
TAG = "out/rome-capitol" + ("-installed" if "art/scenes" in D else "")      # (the pictures to look at go into out/, never into the game)
L = json.load(open(f"{D}/layout.json"))
M = L["marks"]
HZ, FULL = L["horizon"], L["full"]


def lay(base, names, out):
    im = Image.open(base).convert("RGBA")
    for n in names:
        im.alpha_composite(Image.open(f"{D}/{n}.png").convert("RGBA"))
    im.convert("RGB").save(out)


def people(pic, folk, out, fronts=()):
    spec = ";".join(folk)
    r = subprocess.run(["python3", "rome_capitol_people_on.py", pic, str(HZ), str(FULL), spec, out] + list(fronts), capture_output=True, text=True, timeout=180)
    print(r.stdout.strip(), r.stderr.strip()[-300:])


def geese_at(im, spots, frames, foot=(54, 98)):
    """Lay goose frames with their feet at picture points, at their size there (sizeAt 590, smaller with depth)."""
    for (x, y), n, flip in spots:
        g = Image.open(f"{D}/goose-{n}.png").convert("RGBA")
        k = (y - HZ) / (FULL - HZ)
        g = g.resize((max(1, round(g.width * k)), max(1, round(g.height * k))), Image.NEAREST)
        fx, fy = foot[0] * k, foot[1] * k
        if flip:
            g = g.transpose(Image.FLIP_LEFT_RIGHT)
            fx = g.width - fx
        im.alpha_composite(g, (int(round(x - fx)), int(round(y - fy))))


ts = M["titus_seat"]
k = (ts["at"][1] - HZ) / (FULL - HZ)
lift = (ts["cm"] - 0.247 * 175) * k * 160 / 175          # the lamp boy sits at his own seat height (43 cm): lift him to the base's top
seated = f"lampboy|{ts['at'][0]}|{ts['at'][1] - lift:.1f}|0|L.poses.sit(spec,0)"
lay(f"{D}/back.png", ["altar", "chariot", "world", "parapet", "hut", "tablets"], "/tmp/claude-0/-home-claude/0ac9c3a2-6bef-5d57-8b94-ee07580371d5/scratchpad/work-rome-paint2/look/p0.png")
P0 = "/tmp/claude-0/-home-claude/0ac9c3a2-6bef-5d57-8b94-ee07580371d5/scratchpad/work-rome-paint2/look/p0.png"
P1 = "/tmp/claude-0/-home-claude/0ac9c3a2-6bef-5d57-8b94-ee07580371d5/scratchpad/work-rome-paint2/look/p1.png"
# behind the pen's fence: the goose-keeper (the senator stands in for him, 1.0 tall), and the boy at the parapet
people(P0, [f"senator|{M['anser'][0]}|{M['anser'][1]}|90", f"son|{M['view'][0]}|{M['view'][1]}|270", seated], P1, [f"{D}/pen.png"])
im = Image.open(P1).convert("RGBA")
gs = M["geese"]
cx = sum(p[0] for p in gs) / len(gs)
cy = sum(p[1] for p in gs) / len(gs)
geese_at(im, [((cx - 40, cy - 8), 1, False), ((cx - 8, cy + 4), 3, False), ((cx + 26, cy - 10), 4, True), ((cx + 48, cy + 6), 1, True), ((cx - 30, cy + 14), 14, False), ((cx + 10, cy - 18), 2, True)], None)
im.convert("RGB").save(P1)
people(P1, [f"son|{M['fromSteps'][0]}|{M['fromSteps'][1]}|180", f"son|{M['atbase'][0]}|{M['atbase'][1]}|180", f"senator|{M['diodorus'][0]}|{M['diodorus'][1]}|0",
            f"son|{M['default'][0]}|{M['default'][1]}|0"], f"{TAG}-people.png")
# the geese in the pen, behind its near fence
im = Image.open(f"{D}/back.png").convert("RGBA")
for n in ("parapet", "hut"):
    im.alpha_composite(Image.open(f"{D}/{n}.png").convert("RGBA"))
pn = M["pen"]
px = sorted(p[0] for p in pn)
py = sorted(p[1] for p in pn)
geese_at(im, [((px[0] + 24, py[0] + 6), 1, False), ((px[0] + 60, py[0] + 10), 2, True), ((px[-1] - 30, py[0] + 4), 14, False), ((px[0] + 40, py[-1] - 4), 1, True),
              ((px[-1] - 50, py[-1] - 2), 13, False), ((px[-1] - 14, py[-1] - 8), 16, True)], None)
im.alpha_composite(Image.open(f"{D}/pen.png").convert("RGBA"))
gx, gy = M["pen_gate"]
geese_at(im, [((gx + 18, gy - 2), 10, True), ((gx + 52, gy - 10), 9, True)], None)
im.convert("RGB").save(f"{TAG}-geese-in.png")
print(f"{TAG}-people.png", f"{TAG}-geese-in.png")

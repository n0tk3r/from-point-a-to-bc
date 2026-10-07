"""Lay a scene's finished pictures over one another, to look at: comp.py out/egypt1 back palms front -> out/egypt1-comp.png"""
import sys
from PIL import Image
folder, names = sys.argv[1], sys.argv[2:]
im = Image.open(f"{folder}/{names[0]}.png").convert("RGBA")
for n in names[1:]:
    top = Image.open(f"{folder}/{n}.png").convert("RGBA")
    im.alpha_composite(top)
out = folder.rstrip("/") + "-comp.png"
im.convert("RGB").save(out)
print(out, im.size)

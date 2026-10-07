"""Crop a part of a picture and enlarge it, to look at the detail:
python3 nevada_roadside_look.py out/nevada-roadside-2-all.png name x y w h [zoom]"""
import sys
from PIL import Image
src, name, x, y, w, h = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
z = int(sys.argv[7]) if len(sys.argv) > 7 else 2
im = Image.open(src).convert("RGB").crop((x, y, x + w, y + h)).resize((w * z, h * z), Image.NEAREST)
im.save(f"out/nevada-roadside-look-{name}.png")
print(im.size)

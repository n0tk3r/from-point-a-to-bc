"""Enlarge parts of a picture to look at them: egypt_gallery_look.py picture.png name x0 y0 x1 y1 [scale]"""
import sys
from PIL import Image
src, name, x0, y0, x1, y1 = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:7])
k = int(sys.argv[7]) if len(sys.argv) > 7 else 2
im = Image.open(src).convert("RGB").crop((x0, y0, x1, y1))
im.resize((im.width * k, im.height * k), Image.NEAREST).save(f"out/egypt-gallery-crop-{name}.png")

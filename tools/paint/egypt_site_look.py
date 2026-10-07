"""Crop and enlarge part of a picture, to look at it closely: egypt_site_look.py in.png x0 y0 x1 y1 [zoom] [out.png]"""
import sys
from PIL import Image
src, x0, y0, x1, y1 = sys.argv[1], *[int(v) for v in sys.argv[2:6]]
zoom = int(sys.argv[6]) if len(sys.argv) > 6 else 2
out = sys.argv[7] if len(sys.argv) > 7 else "out/egypt-site-crop.png"
im = Image.open(src).convert("RGB").crop((x0, y0, x1, y1))
im.resize((im.width * zoom, im.height * zoom), Image.NEAREST).save(out)
print(out, im.size)

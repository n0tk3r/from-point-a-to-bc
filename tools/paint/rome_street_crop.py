"""Cut a piece out of a picture and enlarge it, to look closely: python3 rome_street_crop.py in.png x0 y0 x1 y1 [scale] [out.png]"""
import sys
from PIL import Image
src, x0, y0, x1, y1 = sys.argv[1], *map(int, sys.argv[2:6])
k = int(sys.argv[6]) if len(sys.argv) > 6 else 2
out = sys.argv[7] if len(sys.argv) > 7 else "out/rome-street-work/crop.png"
im = Image.open(src).convert("RGB").crop((x0, y0, x1, y1))
im.resize((im.width * k, im.height * k), Image.NEAREST).save(out)
print(out, im.size)

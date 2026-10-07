"""Look closely at part of a picture: rome_temple_look.py <png> x y w h [zoom] [name] -> out/rome-temple-crop-<name>.png"""
import sys
from PIL import Image

src = sys.argv[1]
x, y, w, h = (int(v) for v in sys.argv[2:6])
zoom = int(sys.argv[6]) if len(sys.argv) > 6 else 2
name = sys.argv[7] if len(sys.argv) > 7 else "a"
im = Image.open(src).convert("RGB").crop((x, y, x + w, y + h)).resize((w * zoom, h * zoom), Image.NEAREST)
out = f"out/rome-temple-crop-{name}.png"
im.save(out)
print(out, im.size)

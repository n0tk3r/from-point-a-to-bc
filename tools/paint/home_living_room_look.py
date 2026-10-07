"""Cut 2x crops out of a picture, to look at closely: python3 home_living_room_look.py <png> x0,y0,x1,y1[:name] ..."""
import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert("RGB")
for i, spec in enumerate(sys.argv[2:]):
    box, _, name = spec.partition(":")
    x0, y0, x1, y1 = (int(v) for v in box.split(","))
    out = f"out/home-living-room-crop-{name or i}.png"
    im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * 2, (y1 - y0) * 2), Image.NEAREST).save(out)
    print(out)

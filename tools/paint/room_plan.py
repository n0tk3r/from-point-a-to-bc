"""Draw a room's SKELETON before any painting: python3 room_plan.py home_living_room_model -> out/<id>-plan.png

It reads a scene's model (a small Python file of measurements in centimetres) and draws the room through its
camera as flat-shaded boxes, with grown-ups and a child standing on the marks at the size the GAME will draw
them. If the skeleton does not look like a deep, believable room with people the right size, no amount of
painting will fix it: change the model and look again.

A model file defines:
  ID      the scene id
  VIEW    dict for room.View: horizon, full, cam=(X, Z), yaw, focal, centre_x
  ROOM    dict: X=(left, right), Z=(back, front), H=height of the walls (cm)
  SLABS   [(id, X0, X1, Y0, Y1, Z0, Z1)]   floors, galleries, ceilings, big built-in blocks
  FLATS   [(id, wall, u0, u1, v0, v1)]     flat things on a wall. wall: "back" (Z = back), "left" (X = left),
                                           "right" (X = right), or ("X", at) / ("Z", at) for any other upright plane.
                                           u runs along the wall (X for back walls, Z for side walls), v is height.
  BOXES   [(id, X0, X1, Y0, Y1, Z0, Z1)]   furniture
  STAIRS  [dict(id=, X=(X0, X1), z_foot=, z_top=, rise=, steps=)]   or with Z=(Z0, Z1), x_foot=, x_top= for stairs running across
  POLYS   [(id, [(X, Y, Z), ...], (r, g, b))]   other flat parts of the shell: roof slopes, a gable (optional)
  FLOORS  [(Y, X0, X1, Z0, Z1)]            floors at other levels than the room's own (optional)
  MARKS   {name: (X, Z)}                   where people stand ("lilsis" is drawn child-sized)
  WALK    [(X, Z), ...]                    outline of the floor people may stand on (optional)
"""

import importlib
import sys

from PIL import Image, ImageDraw, ImageFont

from room import View

SHADE = {"top": 1.0, "front": 0.82, "left": 0.66, "right": 0.72, "back": 0.5, "bottom": 0.4}
CHILD = {"lilsis": 118.0, "son": 140.0, "bigsis": 158.0}


def tint(color, k):
    return tuple(int(max(0, min(255, c * k))) for c in color)


def wall_quad(view, room, wall, u0, u1, v0, v1):
    (XL, XR), (ZB, ZF) = room["X"], room["Z"]
    if wall == "back":
        return [(u0, v0, ZB), (u1, v0, ZB), (u1, v1, ZB), (u0, v1, ZB)]
    if wall == "left":
        return [(XL, v0, u0), (XL, v0, u1), (XL, v1, u1), (XL, v1, u0)]
    if wall == "right":
        return [(XR, v0, u0), (XR, v0, u1), (XR, v1, u1), (XR, v1, u0)]
    axis, at = wall
    if axis == "X":
        return [(at, v0, u0), (at, v0, u1), (at, v1, u1), (at, v1, u0)]
    return [(u0, v0, at), (u1, v0, at), (u1, v1, at), (u0, v1, at)]


def figure(d, view, name, X, Z):
    cm = CHILD.get(name, 175.0 if name != "mom" else 168.0)
    x, y, h = view.person(X, Z, cm)
    w = h * 0.26
    col = {"mom": (60, 170, 120), "bigsis": (110, 100, 200), "lilsis": (235, 130, 170), "dad": (230, 190, 60)}.get(name, (200, 200, 200))
    d.ellipse([x - w * 0.9, y - 5, x + w * 0.9, y + 5], fill=(0, 0, 0))                    # contact shadow
    d.rounded_rectangle([x - w / 2, y - h * 0.86, x + w / 2, y], radius=w * 0.3, fill=col, outline=(20, 20, 20))
    r = h * 0.075
    d.ellipse([x - r, y - h, x + r, y - h + 2 * r], fill=(235, 200, 170), outline=(20, 20, 20))
    d.text((x - 14, y + 6), f"{name} {h:.0f}", fill=(255, 255, 255))


def draw(model, out=None, people=True):
    v = View(**model.VIEW)
    room = model.ROOM
    (XL, XR), (ZB, ZF), H = room["X"], room["Z"], room["H"]
    Y0 = room.get("Y0", 0.0)                             # where the walls start (below 0 for a room we look down into)
    im = Image.new("RGB", (800, 600), (18, 16, 22))
    d = ImageDraw.Draw(im)

    def fill(pts3, color, outline=(30, 26, 30)):
        pp = v.poly(pts3)
        if len(pp) >= 3:
            d.polygon(pp, fill=color, outline=outline)

    # the shell: ceiling, back wall, side walls, floor (far things first)
    fill([(XL, H, ZB), (XR, H, ZB), (XR, H, ZF), (XL, H, ZF)], (70, 62, 66))
    fill([(XL, Y0, ZB), (XR, Y0, ZB), (XR, H, ZB), (XL, H, ZB)], (150, 132, 118))
    fill([(XL, Y0, ZB), (XL, Y0, ZF), (XL, H, ZF), (XL, H, ZB)], (118, 104, 98))
    fill([(XR, Y0, ZB), (XR, Y0, ZF), (XR, H, ZF), (XR, H, ZB)], (128, 112, 104))
    # the floor(s): the whole room at Y0, unless the model lists its own (FLOORS: [(Y, X0, X1, Z0, Z1)])
    floors = getattr(model, "FLOORS", None) or [(Y0, XL, XR, ZB, ZF + 400)]
    for fy, fx0, fx1, fz0, fz1 in sorted(floors, key=lambda f: f[0]):
        fill([(fx0, fy, fz0), (fx1, fy, fz0), (fx1, fy, fz1), (fx0, fy, fz1)], (120, 86, 56) if fy >= 0 else (60, 44, 34))
        x = fx0                                          # boards every 60 cm and joints every 100 cm, to show the floor's perspective
        while x <= fx1:
            ln = v.line((x, fy, fz0), (x, fy, fz1))
            if ln:
                d.line(ln, fill=(96, 68, 44), width=1)
            x += 60
        z = fz0
        while z <= fz1:
            ln = v.line((fx0, fy, z), (fx1, fy, z))
            if ln:
                d.line(ln, fill=(104, 74, 48), width=1)
            z += 100

    # any other flat pieces of the shell (roof slopes, a gable): POLYS = [(id, [(X, Y, Z), ...], (r, g, b))], drawn in order
    for pid, pts, color in getattr(model, "POLYS", []):
        fill(pts, color)

    # everything else, sorted far to near by its middle
    items = []
    for sid, X0, X1, Y0, Y1, Z0, Z1 in getattr(model, "SLABS", []):
        items.append((v.depth((X0 + X1) / 2, (Z0 + Z1) / 2), "box", sid, (X0, X1, Y0, Y1, Z0, Z1), (176, 150, 120)))
    for fid, wall, u0, u1, v0, v1 in getattr(model, "FLATS", []):
        q = wall_quad(v, room, wall, u0, u1, v0, v1)
        mid = [sum(p[k] for p in q) / 4 for k in range(3)]
        items.append((v.depth(mid[0], mid[2]) + 1, "flat", fid, q, (70, 110, 150)))
    for bid, X0, X1, Y0, Y1, Z0, Z1 in getattr(model, "BOXES", []):
        items.append((v.depth((X0 + X1) / 2, (Z0 + Z1) / 2), "box", bid, (X0, X1, Y0, Y1, Z0, Z1), (190, 120, 84)))
    for st in getattr(model, "STAIRS", []):
        if "z_foot" in st:
            boxes = v.stairs(st["X"][0], st["X"][1], st["z_foot"], st["z_top"], st["rise"], st["steps"], st.get("floor", 0.0))
        else:
            dz, dy = (st["x_top"] - st["x_foot"]) / st["steps"], st["rise"] / st["steps"]
            boxes = []
            for i in range(st["steps"]):
                xa, xb = st["x_foot"] + dz * i, st["x_foot"] + dz * (i + 1)
                boxes.append((min(xa, xb), max(xa, xb), st.get("floor", 0.0), st.get("floor", 0.0) + dy * (i + 1), st["Z"][0], st["Z"][1]))
        for b in boxes:
            items.append((v.depth((b[0] + b[1]) / 2, (b[4] + b[5]) / 2), "box", st["id"], b, (200, 170, 130)))
    if people:
        for name, (X, Z) in getattr(model, "MARKS", {}).items():
            items.append((v.depth(X, Z), "person", name, (X, Z), None))
    items.sort(key=lambda it: -it[0])
    labels = []
    for _, kind, name, geo, color in items:
        if kind == "box":
            faces = v.box(*geo)
            for fname, pp, n in faces:
                d.polygon(pp, fill=tint(color, SHADE[fname]), outline=(30, 24, 22))
            if faces:
                pp = faces[-1][1]
                labels.append((sum(p[0] for p in pp) / len(pp), sum(p[1] for p in pp) / len(pp), name))
        elif kind == "flat":
            pp = v.poly(geo)
            if len(pp) >= 3:
                d.polygon(pp, fill=color, outline=(20, 30, 50))
                labels.append((sum(p[0] for p in pp) / len(pp), sum(p[1] for p in pp) / len(pp), name))
        else:
            figure(d, v, name, *geo)
    seen = set()
    for x, y, name in labels:
        if name in seen:
            continue
        seen.add(name)
        d.text((x - 3 * len(name), y - 5), name, fill=(255, 255, 230))
    walk = getattr(model, "WALK", None)
    if walk:
        pp = v.poly([(X, 0, Z) for X, Z in walk])
        if len(pp) >= 3:
            d.line(pp + [pp[0]], fill=(120, 255, 160), width=1)
    d.line([(0, v.hz), (800, v.hz)], fill=(255, 80, 80), width=1)
    d.line([(0, v.full), (800, v.full)], fill=(255, 220, 80), width=1)
    d.text((6, v.hz - 12), f"horizon {v.hz:.0f}   eye {v.eye:.0f} cm   full {v.full:.0f}   yaw {v.yaw:.0f}   focal {v.F:.0f}", fill=(255, 160, 160))
    out = out or f"out/{model.ID}-plan.png"
    im.save(out)
    return out


if __name__ == "__main__":
    m = importlib.import_module(sys.argv[1].replace(".py", ""))
    print(draw(m, sys.argv[2] if len(sys.argv) > 2 else None))

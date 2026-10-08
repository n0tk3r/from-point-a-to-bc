"""From a room's model: the provisional numbers a scene file needs (python3 room_layout.py <model> [out.json]).

Everything is worked out through the room's camera, so it is where the skeleton says it is. The painter's own
layout.json, measured from the finished picture, replaces this at the end."""
import importlib, json, sys
from room import View
import room_plan


def layout(m):
    v = View(**m.VIEW)
    room = m.ROOM
    out = {"id": m.ID, "horizon": v.hz, "full": v.full, "eye_cm": round(v.eye), "view": m.VIEW, "provisional": True}
    out["marks"] = {}
    for name, (X, Z) in getattr(m, "MARKS", {}).items():
        x, y, h = v.person(X, Z)
        out["marks"][name] = {"at": [round(x), round(y)], "grownup_px": round(h)}
    walk = getattr(m, "WALK", None)
    if walk:
        out["walk"] = [[round(x), round(y)] for x, y in v.poly([(X, 0, Z) for X, Z in walk])]
    things = {}

    def add(name, polys):
        pts = [p for pp in polys for p in pp]
        if not pts:
            return
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        x0, y0, x1, y1 = max(0, min(xs)), max(0, min(ys)), min(800, max(xs)), min(600, max(ys))
        if x1 - x0 < 1 or y1 - y0 < 1:
            return
        t = things.setdefault(name, {"rect": [800, 600, 0, 0]})
        r = t["rect"]
        t["rect"] = [min(r[0], x0), min(r[1], y0), max(r[2], x1), max(r[3], y1)]

    for fid, wall, u0, u1, v0, v1 in getattr(m, "FLATS", []):
        add(fid, [v.poly(room_plan.wall_quad(v, room, wall, u0, u1, v0, v1))])
    for bid, X0, X1, Y0, Y1, Z0, Z1 in list(getattr(m, "BOXES", [])) + list(getattr(m, "SLABS", [])):
        add(bid, [pp for _, pp, _ in v.box(X0, X1, Y0, Y1, Z0, Z1)])
        if Y0 == 0 and bid in things:                 # the ground it stands on
            things[bid]["foot"] = [[round(x), round(y)] for x, y in v.poly([(X0, 0, Z0), (X1, 0, Z0), (X1, 0, Z1), (X0, 0, Z1)])]
    for st in getattr(m, "STAIRS", []):
        if "z_foot" in st:
            bs = v.stairs(st["X"][0], st["X"][1], st["z_foot"], st["z_top"], st["rise"], st["steps"], st.get("floor", 0.0))
            for b in bs:
                add(st["id"], [pp for _, pp, _ in v.box(*b)])
    for t in things.values():
        r = t["rect"]
        t["rect"] = [round(r[0]), round(r[1]), round(r[2] - r[0]), round(r[3] - r[1])]      # x, y, width, height
    out["things"] = things
    return out


if __name__ == "__main__":
    m = importlib.import_module(sys.argv[1].replace(".py", ""))
    L = layout(m)
    path = sys.argv[2] if len(sys.argv) > 2 else f"plans/{m.ID}-layout.json"
    json.dump(L, open(path, "w"), indent=1)
    print(path)

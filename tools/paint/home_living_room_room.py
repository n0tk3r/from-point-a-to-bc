"""The room itself: floor and rug, the back wall with its door and window, the bookcase, the stairs
and the closet under them, and the ceiling. Everything here belongs to the backdrop."""

from home_living_room_plan import *

SEED = 5
FLOOR_IN_DEPTH = True                                       # the floorboards run from the back wall toward us (tried both ways)


TILT = [None]                                               # (middle x, middle y, degrees): set while a crooked picture is drawn


def wp(X, Y):
    """A place on the back wall (cm across from the middle of the room, cm up) -> picture."""
    if TILT[0] is not None:
        cx, cy, ang = TILT[0]
        a = math.radians(ang)
        dx, dy = X - cx, Y - cy
        X, Y = cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)
    return P(X, Y, ZW)


def crooked(what, x0, x1, y0, y1):
    """Some of the photographs do not hang straight. Call before drawing one; set TILT[0] = None after."""
    ang = {"hills": 3.2, "portrait2": -2.8, "baby": 2.0, "drawing": -1.6}.get(what)
    TILT[0] = None if ang is None else ((x0 + x1) / 2, (y0 + y1) / 2, ang)


def wrect(s, x0, x1, y0, y1, color, alpha=1.0):
    """A rectangle flat on the back wall, in the wall's own measurements."""
    s.poly([wp(x0, y0), wp(x1, y0), wp(x1, y1), wp(x0, y1)], color, alpha)


# ---------------------------------------------------------------- local color: the floor
def rug_pt(lx, lz, y=0.0):
    """A place on the rug, measured from its middle along and across it -> a place in the room."""
    r = RUG
    x, z = turn((r["x0"] + r["x1"]) / 2, (r["z0"] + r["z1"]) / 2, (r["x0"] + r["x1"]) / 2 + lx, (r["z0"] + r["z1"]) / 2 + lz, r["ang"])
    return (x, y, z)


def rug_albedo(X, Z):
    r = RUG
    xc, zc = (r["x0"] + r["x1"]) / 2, (r["z0"] + r["z1"]) / 2
    hw, hd = (r["x1"] - r["x0"]) / 2, (r["z1"] - r["z0"]) / 2
    ca, sa = math.cos(math.radians(-r["ang"])), math.sin(math.radians(-r["ang"]))
    rx, rz = (X - xc) * ca - (Z - zc) * sa, (X - xc) * sa + (Z - zc) * ca
    ax, az = np.abs(rx), np.abs(rz)
    e = np.minimum(hw - ax, hd - az)                                   # cm in from the edge
    inside = (e > 0).astype(F32)
    field, deep, blue, gold, cream, bind = (col(c) for c in ("#a03230", "#74202a", "#2f4b78", "#c9a258", "#e2d2a6", "#3a1f2c"))
    c = np.empty(X.shape + (3,), dtype=F32)
    c[...] = field
    lat = np.abs(np.mod(rx + rz * 1.25, 26.0) - 13.0) + np.abs(np.mod(rx - rz * 1.25, 26.0) - 13.0)
    c[lat < 5.0] = deep                                                # a lattice of small dark flowers
    c[lat < 1.8] = gold
    m = ax / 74.0 + az / 46.0                                          # the middle medallion
    c[m < 1.0] = blue
    c[(m < 1.0) & (m > 0.90)] = cream
    c[m < 0.70] = gold
    c[m < 0.62] = field
    c[m < 0.30] = cream
    c[m < 0.20] = blue
    k = (hw - 30 - ax) / 52.0 + (hd - 30 - az) / 34.0                   # quarter medallions in the corners
    c[k < 1.0] = blue
    c[(k < 1.0) & (k > 0.86)] = cream
    c[k < 0.5] = gold
    # the border: binding, blue band with a running pattern, two thin lines
    band = (e < 30)
    c[band] = blue
    run = np.where(hw - ax < hd - az, rz, rx)                          # the way the border runs just here
    tooth = np.abs(np.mod(run, 14.0) - 7.0) + np.abs(e - 17.0) * 1.1
    c[band & (tooth < 4.6)] = cream
    c[band & (tooth < 2.2)] = field
    c[(e > 26.5) & (e < 30)] = cream
    c[(e > 4.0) & (e < 6.5)] = gold
    c[e < 4.0] = bind
    # threadbare where it is walked on, and faded generally
    worn = step(0.52, 0.80, wnoise(X * 0.8, Z * 1.1, 70, SEED + 31)) * np.clip(1.2 - m * 0.4, 0, 1)
    c = lerp(c, col("#b89a84"), (worn * 0.34)[..., None])
    c = c * (1 + ((wnoise(X, Z, (5, 5), SEED + 32, 2) - 0.5) * 0.18)[..., None])
    return c.astype(F32), inside


def floor_albedo(X, Z):
    alb = wood(Z, X, "#c48c52", "#523420", SEED, plank=13.0, length=170.0, tone=0.15, grain=0.10) if FLOOR_IN_DEPTH else wood(X, Z, "#c48c52", "#523420", SEED, plank=13.0, length=170.0, tone=0.15, grain=0.10)
    # the boards have gone pale and grey where the family walks, and darker along the walls
    path = step(0.40, 0.75, wnoise(X, Z * 1.4, 150, SEED + 21))
    alb = lerp(alb, alb * col("#f0e2d0") * 1.08, (path * 0.35)[..., None])
    alb = alb * (1 - (step(60.0, 0.0, ZW - Z) * 0.20)[..., None])
    c, inside = rug_albedo(X, Z)
    alb = lerp(alb, c, inside[..., None])
    m = MAT
    em = np.minimum(np.minimum(X - m["x0"], m["x1"] - X), np.minimum(Z - m["z0"], m["z1"] - Z))
    coir = col("#9a7844") * (1 + ((wnoise(X * 3, Z * 3, 4, SEED + 33, 2) - 0.5) * 0.3)[..., None])
    coir = np.where(((em < 7) & (em > 0))[..., None], col("#5a4026"), coir)
    alb = lerp(alb, coir, (em > 0).astype(F32)[..., None])
    return alb.astype(F32)


# ---------------------------------------------------------------- local color: the back wall
def curtain_shape(Y, side):
    """The curtain at one side of the window at height Y: (outer edge, inner edge) in wall cm.
    It is gathered on its pole, pulled in by a tie-back, and hangs loose below."""
    tie, top, hem = 118.0, POLE, 58.0
    w = np.where(Y >= tie, 19.0 + np.clip((Y - tie) / (top - tie), 0, 1) ** 0.8 * 37.0, 19.0 + (tie - Y) / (tie - hem) * 14.0)
    if side < 0:
        x0 = WIN["x0"] - 28.0
        return x0, x0 + w
    x0 = WIN["x1"] + 28.0
    return x0, x0 - w


def panes():
    """The five panes of glass in the window: (x0, x1, y0, y1) in wall cm."""
    w = WIN
    a, b, f = w["x0"] + 7, w["x1"] - 7, 4.0
    out = []
    for (x0, x1) in ((a, w["m1"] - f), (w["m2"] + f, b)):
        out += [(x0, x1, w["y0"] + 7, w["rail"] - f), (x0, x1, w["rail"] + f, w["y1"] - 7)]
    out.append((w["m1"] + f, w["m2"] - f, w["y0"] + 7, w["y1"] - 7))
    return out


def wall_albedo():
    """-> (local color of everything flat on the back wall, mask of the window glass, mask of the door glass)."""
    px, py = grid(SHAPE)
    Xw, Yw = (px + 0.5 - VX) / KW, (WALL_Y - py - 0.5) / KW
    # ---- the paper: broad cream and sage stripes, a pin line between, a small faded flower up the cream
    u = np.mod(Xw + 3.0, 20.0)
    A, Bc, pin = col("#eee0bc"), col("#c0cbaa"), col("#a8844e")
    alb = np.where((u < 11.0)[..., None], A, Bc).astype(F32)
    pinline = (np.abs(u - 11.0) < 0.9) | (u < 0.9) | (u > 19.1)
    alb[pinline] = lerp(alb[pinline], pin, 0.6)
    i = np.floor((Xw + 3.0) / 20.0)
    cy = np.mod(Yw + np.mod(i, 2) * 13.0, 26.0) - 13.0
    cx = u - 5.5
    flower = np.abs(cx) / 3.2 + np.abs(cy) / 4.0 < 1
    leaf = (np.abs(cx) / 1.6 + np.abs(cy - 6.4) / 2.3 < 1) | (np.abs(cx) / 1.6 + np.abs(cy + 6.4) / 2.3 < 1)
    alb[leaf] = lerp(alb[leaf], col("#7c9a66"), 0.7)
    alb[flower] = lerp(alb[flower], col("#c2604e"), 0.8)
    alb[np.abs(cx) / 1.1 + np.abs(cy) / 1.4 < 1] = col("#e8c070")
    # it has yellowed unevenly, most toward the top
    age = wnoise(Xw, Yw, 80, SEED + 40) - 0.5
    alb = alb * (1 + (age * 0.10)[..., None]) * (1 - np.clip((Yw - 150) / 400, 0, 1) * 0.10)[..., None]
    # ---- frieze above the picture rail (a border of swags and small roses), the rail, the cornice
    fr = Yw > PICRAIL + 4
    alb[fr] = col("#dccaa2") * (1 + age[fr][..., None] * 0.08)
    ph = np.mod(Xw, 40.0) / 40.0
    sag = PICRAIL + 36 - 13 * np.sin(np.pi * ph)                        # the line a garland hangs in
    fb = alb.copy()
    fb[fr & (np.abs(Yw - sag) < 1.7)] = col("#b07a66")
    fb[fr & (np.abs(Yw - sag + 4.6) < 0.9)] = col("#94a47c")
    knot = (np.abs(np.mod(Xw + 20.0, 40.0) - 20.0) / 4.6 + np.abs(Yw - (PICRAIL + 37)) / 5.6) < 1
    fb[fr & knot] = col("#b0604e")
    fb[fr & (np.abs(np.mod(Xw + 20.0, 40.0) - 20.0) / 1.9 + np.abs(Yw - (PICRAIL + 37)) / 2.3 < 1)] = col("#e2c078")
    fb[fr & (np.abs(Yw - (PICRAIL + 62)) < 1.1)] = col("#b07a66")
    fb[fr & (np.abs(Yw - (PICRAIL + 11)) < 1.0)] = col("#b07a66")
    worn = 0.45 + 0.4 * wnoise(Xw, Yw * 2.0, 70, SEED + 43)              # the border has faded in patches
    alb = lerp(alb, fb, worn[..., None])
    alb[(Yw > PICRAIL) & (Yw <= PICRAIL + 4)] = col("#9a6436")
    alb[Yw > WALL_H - 13] = col("#e6dac0")
    # ---- the panelling below, painted a dull green long ago: stiles and rails round sunk panels, a cap, a skirting board
    v = np.mod(Xw + 10.0, 46.0)
    low = Yw < DADO
    gr = (wnoise(Yw * 1.0, Xw * 5.0, (46, 5), SEED + 41) - 0.5)
    rub = step(0.55, 0.85, wnoise(Xw, Yw * 2.0, 60, SEED + 42)) * np.clip(1 - Yw / 60.0, 0, 1)      # scuffed pale low down, where shoes and chairs go
    frame = col("#93a88c")[None, None, :] * (1 + gr[..., None] * 0.10)
    panel = col("#839a80")[None, None, :] * (1 + gr[..., None] * 0.12) * (1 + (hash01(np.floor((Xw + 10.0) / 46.0), 7.0, 3.0)[..., None] - 0.5) * 0.08)
    is_panel = low & (v >= 9) & (Yw < DADO - 10) & (Yw > 26)
    green = np.where(is_panel[..., None], panel, frame)
    green = lerp(green, col("#c9c8b0")[None, None, :], (rub * 0.5)[..., None])
    alb = np.where(low[..., None], green, alb)
    alb[(Yw >= DADO) & (Yw < DADO + 4.5)] = col("#a8ba9c")
    alb[Yw < 12.5] = col("#7c9278") * (1 + gr[Yw < 12.5][..., None] * 0.1)
    alb = alb.astype(F32)

    s = Sheet(SHAPE)
    # ---- the front door: painted cream on this side, in a cream frame; two frosted lights at the top
    d = DOOR
    wrect(s, d["x0"], d["x1"], 0, d["top"], "#d9d0b8")
    wrect(s, d["lx0"], d["lx1"], 0.6, d["ltop"], "#e4dcc6")
    # ---- the window: a wide one, three lights; painted frame, wooden sill
    w = WIN
    wrect(s, w["x0"], w["x1"], w["y0"], w["y1"], "#e8e2d0")
    wrect(s, w["x0"] - 8, w["x1"] + 8, w["y0"] - 6, w["y0"], "#c9905a")
    # ---- above the desk: the wall clock, and a cork board
    wrect(s, *CORK, "#8a5a34")
    wrect(s, CORK[0] + 4, CORK[1] - 4, CORK[2] + 4, CORK[3] - 4, "#c49a66")
    s.ellipse(*wp(CLOCK[0], CLOCK[1]), 14.5 * KW, 14.5 * KW, "#6e4426")
    wrect(s, CLOCK[0] - 8, CLOCK[0] + 8, CLOCK[1] - 40, CLOCK[1] - 10, "#6e4426")
    # ---- the family photographs over the piano
    for (x0, x1, y0, y1, frame, mat, what) in FRAMES:
        crooked(what, x0, x1, y0, y1)
        wrect(s, x0, x1, y0, y1, frame)
        wrect(s, x0 + 3, x1 - 3, y0 + 3, y1 - 3, mat)
        TILT[0] = None
    s.onto(alb)
    bare = 1 - s.done()[1]

    # ---- curtains, with their folds already in them
    for side in (-1, 1):
        xo, xi = curtain_shape(Yw, side)
        f = (Xw - xo) / (xi - xo)
        inside = (f > 0) & (f < 1) & (Yw > 58 + 2.5 * np.sin(f * 9.0)) & (Yw < POLE)
        fold = 0.80 + 0.26 * np.sin(f * 2 * np.pi * 3.5 + 0.6) + 0.10 * np.sin(f * 2 * np.pi * 7.0 + 2.0)
        cloth = col("#456f9e")[None, None, :] * fold[..., None]
        dot = (np.abs(np.mod(Xw, 9.0) - 4.5) + np.abs(np.mod(Yw + np.floor(Xw / 9.0) * 4.5, 9.0) - 4.5) < 1.5)
        cloth = np.where(dot[..., None], cloth * 1.35, cloth)
        alb = np.where(inside[..., None], cloth, alb)
        bare = bare * (1 - inside.astype(F32))

    glass = Sheet(SHAPE)
    for (x0, x1, y0, y1) in panes():
        wrect(glass, x0, x1, y0, y1, "#ffffff")
    gm = glass.done()[1]
    for side in (-1, 1):                                       # the curtains hang in front of the glass
        xo, xi = curtain_shape(Yw, side)
        f = (Xw - xo) / (xi - xo)
        gm = gm * (1 - ((f > 0) & (f < 1) & (Yw > 58)).astype(F32))
    dg = Sheet(SHAPE)
    for (x0, x1) in ((d["lx0"] + 10, d["lx0"] + 42), (d["lx1"] - 42, d["lx1"] - 10)):
        wrect(dg, x0, x1, 138, 190, "#ffffff")
    return alb.astype(F32), gm, dg.done()[1], bare.astype(F32)


BEAMS = ()                                                  # (ceiling beams were tried and read as stripes: the ceiling is plain plaster)
CORK = (-96.0, -14.0, 150.0, 216.0)                         # the cork board over the desk: x0, x1, y0, y1
CLOCK = (-128.0, 218.0)                                     # the middle of the clock's face
# frames on the wall above the piano and up the stairs: (x0, x1, y0, y1, frame color, mat color, what is in it)
FRAMES = [
    (PHOTO["x0"], PHOTO["x1"], PHOTO["y0"], PHOTO["y1"], "#6a4426", "#efe6cf", "lake"),   # the five of us at the lake
    (150, 178, 196, 234, "#b8923e", "#efe6cf", "wedding"),
    (152, 178, 152, 184, "#3a2c28", "#e8dcc0", "baby"),
    (270, 298, 200, 236, "#3a2c28", "#efe6cf", "portrait"),
    (270, 300, 160, 190, "#8a5a34", "#e8dcc0", "hills"),
    (196, 226, 230, 256, "#8a5a34", "#efe6cf", "drawing"),
    (232, 262, 230, 258, "#3a2c28", "#e8dcc0", "old"),
    (336, 364, 190, 224, "#b8923e", "#efe6cf", "school"),                                 # and up the stairs
    (386, 418, 222, 250, "#3a2c28", "#e8dcc0", "sea"),
    (440, 468, 250, 284, "#6a4426", "#efe6cf", "portrait2"),
    (496, 522, 252, 282, "#b8923e", "#e8dcc0", "baby2"),
    (-544, -494, 224, 256, "#6a4426", "#efe6cf", "sampler"),                              # over the front door: a cross-stitch house
]


def night_view():
    """What the window shows: the street at night. A picture the size of the whole scene; only the part
    behind the glass is used. It gives its own light, so the lamps in the room do not touch it."""
    w = WIN
    ax, ay = wp(w["x0"] + 7, w["y1"] - 7)                      # top left of the glass
    bx, by = wp(w["x1"] - 7, w["y0"] + 7)                      # bottom right
    gw, gh = bx - ax, by - ay
    px, py = grid(SHAPE)
    u, v = (px - ax) / gw, (py - ay) / gh
    rng = np.random.default_rng(SEED + 50)
    sky = ramp(np.clip(v / 0.62, 0, 1), [(0.0, "#0e1840"), (0.55, "#1a2d66"), (1.0, "#34508c")])
    cloud = step(0.48, 0.80, noise(SHAPE, (46, 12), SEED + 51, 3)) * np.clip(1 - v * 1.4, 0, 1)
    pic = lerp(sky, col("#3a548e"), (cloud * 0.5)[..., None]).astype(F32)

    def at(uu, vv):
        return (ax + uu * gw, ay + vv * gh)
    s = Sheet(SHAPE)
    for _ in range(16):                                        # stars
        uu, vv = rng.random(), rng.random() * 0.42
        s.ellipse(*at(uu, vv), 0.55, 0.55, "#dfe8ff", 0.5 + 0.5 * rng.random())
    mx, my = at(0.615, 0.13)                                   # a thin moon
    s.ellipse(mx, my, 5.2, 5.2, "#f4f2dc")
    s.ellipse(mx + 2.4, my - 1.0, 4.6, 4.6, "#16265a")
    # the houses across the road, dark against the sky; one window still lit
    far = "#0d1634"
    s.poly([at(0.50, 0.70), at(0.50, 0.50), at(0.66, 0.36), at(0.82, 0.50), at(0.82, 0.46), at(1.02, 0.46), at(1.02, 0.70)], far)
    s.poly([at(0.86, 0.46), at(0.86, 0.36), at(0.90, 0.36), at(0.90, 0.46)], far)
    s.poly([at(-0.02, 0.70), at(-0.02, 0.52), at(0.10, 0.44), at(0.24, 0.53), at(0.24, 0.70)], "#101a3c")
    s.poly([at(0.26, 0.70), at(0.26, 0.60), at(0.48, 0.60), at(0.48, 0.70)], "#0f1838")                 # a hedge
    s.poly([at(0.61, 0.52), at(0.69, 0.52), at(0.69, 0.60), at(0.61, 0.60)], "#ffcf7c")                 # the lit window
    s.line([at(0.65, 0.52), at(0.65, 0.60)], far, 0.8)
    s.poly([at(0.90, 0.54), at(0.96, 0.54), at(0.96, 0.62), at(0.90, 0.62)], "#1b2a55")
    s.poly([at(0.06, 0.57), at(0.13, 0.57), at(0.13, 0.64), at(0.06, 0.64)], "#1b2a55")
    # a bare tree
    tx, ty = at(0.385, 0.70)
    s.taper([(tx, ty), (tx - 1, ty - 16), (tx + 1, ty - 30)], "#0a1230", 2.6, 1.2)
    for k in range(13):
        a0 = -1.57 + rng.normal(0, 0.75)
        l = 9 + rng.random() * 13
        y0 = ty - 12 - rng.random() * 18
        s.line([(tx, y0), (tx + np.cos(a0) * l * 0.6, y0 + np.sin(a0) * l * 0.6), (tx + np.cos(a0 + 0.4) * l, y0 + np.sin(a0 + 0.2) * l)], "#0a1230", 0.8, 0.9)
    s.onto(pic)
    # the road: empty. the street lamp lays a pale pool on it, exactly where a car would stand
    road = (v > 0.70).astype(F32)
    over(pic, ramp(np.clip((v - 0.70) / 0.3, 0, 1), [(0.0, "#1b294e"), (1.0, "#22345c")]), road)
    over(pic, "#2b3f68", (road * (np.abs(v - 0.735) < 0.012)).astype(F32))                               # the far kerb
    lx, ly = at(0.215, 0.30)
    pool = np.exp(-(((px - (lx + 16)) / 44.0) ** 2 + ((py - at(0, 0.86)[1]) / 9.0) ** 2))
    over(pic, "#93a8a8", (pool * 0.62 * road).astype(F32))
    over(pic, "#2a3c62", (road * (v > 0.955)).astype(F32))                                               # our own kerb, and the grass
    s = Sheet(SHAPE)
    s.line([at(0.20, 0.93), (lx - 2.2, ly + 3)], "#0a1028", 1.5)                                         # the lamp post
    s.line([(lx - 2.2, ly + 3), (lx - 1, ly - 1), (lx + 7, ly - 2.5)], "#0a1028", 1.3)
    s.ellipse(lx + 8, ly - 0.6, 3.6, 2.0, "#f6ffe2")
    mbx, mby = at(0.66, 0.955)                                                                           # our mailbox, at the kerb
    s.line([(mbx, mby), (mbx, mby - 9)], "#0a1028", 1.4)
    s.poly([(mbx - 4.5, mby - 9), (mbx + 4.5, mby - 9), (mbx + 4.5, mby - 13), (mbx + 2.5, mby - 14.6), (mbx - 2.5, mby - 14.6), (mbx - 4.5, mby - 13)], "#3c5078")
    s.line([(mbx + 4.5, mby - 12), (mbx + 4.5, mby - 16)], "#b0483c", 1.0)
    s.onto(pic)
    halo = np.exp(-(((px - (lx + 8)) / 10.0) ** 2 + ((py - ly) / 8.0) ** 2))
    glow(pic, "#b8d8c0", (halo * 0.55).astype(F32))
    cone = np.clip(1 - np.abs((px - (lx + 8)) - (py - ly) * 0.18) / (3 + (py - ly) * 0.34), 0, 1) * (py > ly) * (v < 0.9)
    glow(pic, "#8fb0b0", (cone * 0.10).astype(F32))
    # the glass itself: a little of the room's warmth on it, darker toward the top
    glow(pic, "#ffcf90", (np.clip(1 - np.abs(u - v * 0.4 - 0.35) * 5, 0, 1) * 0.045).astype(F32))
    return np.clip(pic, 0, 1)


# ---------------------------------------------------------------- the things that stand against the wall
def bookcase(L, fine=False):
    b = BOOKS
    x0, x1, z0, top = b["x0"], b["x1"], b["z0"], b["top"]
    if not fine:
        B(L, x0, x1, 0, top, z0, ZW, grainy("#7a4c2a", SEED + 60, "y"), top=grainy("#8a5a32", SEED + 61, "x"))
        Fc(L, [(x0 + 5, 9, z0 - 0.1), (x1 - 5, 9, z0 - 0.1), (x1 - 5, top - 6, z0 - 0.1), (x0 + 5, top - 6, z0 - 0.1)], "#3a2418", n=(0, 0, -1), dim=0.8)
        return
    if isinstance(L, Collector):
        return
    rng = np.random.default_rng(SEED + 62)
    s = Sheet(SHAPE)
    zf = z0 - 0.2
    shelves = [9, 50, 86, 120, 152, 182]                                  # the top of each shelf board
    palette = ["#b5483a", "#3f6f8f", "#d9a441", "#5b7d4b", "#7b4f8f", "#d6ceb8", "#2f3a5c", "#a8552c", "#3f8c7c", "#8a3a4a", "#c9b27a", "#4a5a3a"]
    for si, y in enumerate(shelves):
        room = (shelves[si + 1] - 4 if si + 1 < len(shelves) else top - 6) - y        # clear height above this shelf
        x = x0 + 6.5
        end = x1 - 6.5
        while x < end - 2:
            r = rng.random()
            if si == 0 and x < x0 + 40:                                 # the bottom shelf: big atlases and albums lying flat
                wd = 30
                for k in range(4):
                    hh = 4 + rng.random() * 3
                    cc = lit(palette[int(rng.integers(len(palette)))], ((x + wd / 2), y + k * 6 + 3, z0), (0, 0, -1), 0.95)
                    s.poly(pts2([(x + rng.random() * 3, y + k * 6, zf), (x + wd - rng.random() * 4, y + k * 6, zf), (x + wd - rng.random() * 4, y + k * 6 + hh, zf), (x + rng.random() * 3, y + k * 6 + hh, zf)]), cc)
                x += wd + 2
                continue
            if si == 1 and abs(x - (x0 + 60)) < 6:                      # the duck book, cover outward: a duck and no words
                wd, hh = 17, 22
                cov = lit("#5a9ec8", (x + wd / 2, y + hh / 2, z0), (0, 0, -1))
                s.poly(pts2([(x, y, zf), (x + wd, y, zf), (x + wd, y + hh, zf), (x, y + hh, zf)]), cov)
                duck = lit("#f6d24a", (x + wd / 2, y + hh / 2, z0), (0, 0, -1))
                c = P(x + wd * 0.48, y + hh * 0.42, zf)
                s.ellipse(c[0], c[1], 3.6, 2.6, duck)
                s.ellipse(c[0] + 2.6, c[1] - 3.2, 1.9, 1.8, duck)
                s.line([(c[0] + 4.2, c[1] - 3.0), (c[0] + 6.0, c[1] - 2.6)], lit("#e8843a", (x, y, z0), (0, 0, -1)), 1.1)
                x += wd + 1.5
                continue
            if r < 0.07 and x < end - 16:                               # a gap, with something small standing in it
                kind = rng.integers(3)
                c = P(x + 6, y, zf)
                if kind == 0:                                           # a little framed picture
                    s.poly(pts2([(x + 1, y, zf), (x + 12, y, zf), (x + 12, y + 14, zf), (x + 1, y + 14, zf)]), lit("#b8923e", (x, y + 7, z0), (0, 0, -1)))
                    s.poly(pts2([(x + 3, y + 2, zf), (x + 10, y + 2, zf), (x + 10, y + 12, zf), (x + 3, y + 12, zf)]), lit("#9fb6c8", (x, y + 7, z0), (0, 0, -1)))
                elif kind == 1:                                         # a jar of pencils
                    s.poly(pts2([(x + 3, y, zf), (x + 10, y, zf), (x + 10, y + 9, zf), (x + 3, y + 9, zf)]), lit("#c96a4a", (x, y + 5, z0), (0, 0, -1)))
                    for k in range(3):
                        s.line(pts2([(x + 4.5 + k * 2, y + 9, zf), (x + 3.5 + k * 3, y + 16, zf)]), lit(("#e8c84a", "#4a7ab8", "#d85a4a")[k], (x, y + 12, z0), (0, 0, -1)), 0.8)
                else:                                                   # a small trophy
                    s.poly(pts2([(x + 4, y, zf), (x + 10, y, zf), (x + 9, y + 3, zf), (x + 5, y + 3, zf)]), lit("#5a4030", (x, y, z0), (0, 0, -1)))
                    s.poly(pts2([(x + 4, y + 12, zf), (x + 10, y + 12, zf), (x + 8, y + 5, zf), (x + 7.6, y + 3, zf), (x + 6.4, y + 3, zf), (x + 6, y + 5, zf)]), lit("#e8c050", (x, y + 8, z0), (0, 0, -1)))
                x += 15
                continue
            wd = 2.6 + rng.random() * 3.6
            hh = min(room - 1, (20 + rng.random() * 9) * (0.86 if si >= 3 else 1.0))
            if si in (3, 4) and x > x0 + 62:                            # Dad's manuals: a row all alike
                wd, hh = 4.4, min(room - 1, 25.5)
                base = ("#6c7a8c", "#74828f")[int(rng.integers(2))]
            else:
                base = palette[int(rng.integers(len(palette)))]
            if x + wd > end:
                break
            lean = (rng.random() < 0.09) * (2.5 + rng.random() * 3)
            cc = lit(base, (x + wd / 2, y + hh / 2, z0), (0, 0, -1), 0.86 + 0.28 * rng.random())
            quad = [(x, y, zf), (x + wd, y, zf), (x + wd + lean, y + hh, zf), (x + lean, y + hh, zf)]
            s.poly(pts2(quad), cc)
            if wd > 3.4 and rng.random() < 0.7:                         # a band or a label on the spine: never words
                yb = y + hh * (0.62 + 0.2 * rng.random())
                lab = lit(("#e8d8a8", "#f0e8d0", "#d8b050", "#2a2420")[int(rng.integers(4))], (x, yb, z0), (0, 0, -1))
                s.poly(pts2([(x + 0.5 + lean * 0.7, yb, zf), (x + wd - 0.5 + lean * 0.7, yb, zf), (x + wd - 0.5 + lean * 0.8, yb + 3, zf), (x + 0.5 + lean * 0.8, yb + 3, zf)]), lab, 0.9)
            s.line(pts2([(x + wd + lean * 0.0, y, zf), (x + wd + lean, y + hh, zf)]), "#1c1018", 0.7, 0.45)
            x += wd + lean * 0.5 + (0.6 if rng.random() < 0.25 else 0.0)
    # the shelf boards and the case's front edges, said again crisply
    for y in shelves:
        yy = y - 4
        s.poly(pts2([(x0 + 4, yy, zf), (x1 - 4, yy, zf), (x1 - 4, y, zf), (x0 + 4, y, zf)]), lit("#8a5a32", ((x0 + x1) / 2, y, z0), (0, 0, -1), 0.9))
        s.line(pts2([(x0 + 5, y, zf), (x1 - 5, y, zf)]), lit("#c08a50", ((x0 + x1) / 2, y, z0), (0, 1, 0), 0.9), 0.8, 0.9)
        s.line(pts2([(x0 + 5, yy - 0.6, zf), (x1 - 5, yy - 0.6, zf)]), "#140c10", 1.0, 0.55)
    for xs in (x0, x1 - 5):
        s.poly(pts2([(xs, 0, zf), (xs + 5, 0, zf), (xs + 5, top, zf), (xs, top, zf)]), lit("#8a5a32", (xs, 110, z0), (0, 0, -1)))
    s.poly(pts2([(x0, top - 6, zf), (x1, top - 6, zf), (x1, top, zf), (x0, top, zf)]), lit("#94623a", ((x0 + x1) / 2, top, z0), (0, 0, -1)))
    s.poly(pts2([(x0, 0, zf), (x1, 0, zf), (x1, 9, zf), (x0, 9, zf)]), lit("#7a4c2a", ((x0 + x1) / 2, 5, z0), (0, 0, -1)))
    s.line(pts2([(x0, top, zf), (x1, top, zf)]), lit("#d8a468", ((x0 + x1) / 2, top, z0), (0, 1, 0)), 1.0)
    s.line(pts2([(x0 + 5, 0, zf), (x0 + 5, top - 6, zf)]), "#140c10", 0.8, 0.5)
    s.line(pts2([(x1 - 5, 0, zf), (x1 - 5, top - 6, zf)]), "#140c10", 0.8, 0.4)
    # on top of it: a globe, a stack of game boxes, ivy coming down the side
    gx, gz = x0 + 30, z0 + 16
    c = P(gx, top + 20, gz)
    r = 13 * cam.scale(gz)
    s.poly(pts2([(gx - 8, top, gz), (gx + 8, top, gz), (gx + 4, top + 4, gz), (gx - 4, top + 4, gz)]), lit("#4a3020", (gx, top, gz), (0, 0, -1)))
    s.ellipse(c[0], c[1], r, r, lit("#4f86b0", (gx, top + 20, gz), (-0.3, 0.3, -0.9)))
    s.poly([(c[0] - r * 0.7, c[1] - r * 0.2), (c[0] - r * 0.2, c[1] - r * 0.7), (c[0] + r * 0.2, c[1] - r * 0.3), (c[0] - r * 0.1, c[1] + r * 0.3), (c[0] - r * 0.5, c[1] + r * 0.5)], lit("#8fae6a", (gx, top + 20, gz), (-0.3, 0.3, -0.9)))
    s.poly([(c[0] + r * 0.35, c[1] + r * 0.1), (c[0] + r * 0.8, c[1] - r * 0.1), (c[0] + r * 0.6, c[1] + r * 0.6)], lit("#c9b070", (gx, top + 20, gz), (-0.3, 0.3, -0.9)))
    s.line([(c[0] - r * 0.9, c[1] - r * 0.9), (c[0] + r * 1.0, c[1] + r * 0.7)], lit("#c9a050", (gx, top + 30, gz)), 0.9, 0.9)
    bx = x0 + 62
    for k, (wd, hh, cc) in enumerate([(46, 7, "#b5483a"), (42, 6, "#3f6f8f"), (38, 6, "#d9a441")]):
        yy = top + sum(h for _, h, _ in [(46, 7, 0), (42, 6, 0), (38, 6, 0)][:k])
        s.poly(pts2([(bx + k * 2, yy, zf), (bx + k * 2 + wd, yy, zf), (bx + k * 2 + wd, yy + hh, zf), (bx + k * 2, yy + hh, zf)]), lit(cc, (bx + 20, yy, z0), (0, 0, -1)))
        s.poly(pts2([(bx + k * 2 + 6, yy + 1.5, zf), (bx + k * 2 + wd - 12, yy + 1.5, zf), (bx + k * 2 + wd - 12, yy + hh - 1.5, zf), (bx + k * 2 + 6, yy + hh - 1.5, zf)]), lit("#f0e6c8", (bx + 20, yy, z0), (0, 0, -1)), 0.8)
    L.sheet(s)
    ivy = Sheet(SHAPE)
    px0 = x1 - 12
    pot = lit("#b8623a", (px0, top + 6, z0 + 10), (0, 0, -1))
    ivy.poly(pts2([(px0 - 8, top, zf), (px0 + 8, top, zf), (px0 + 10, top + 12, zf), (px0 - 10, top + 12, zf)]), pot)
    for k in range(34):
        t = rng.random()
        if rng.random() < 0.45:
            lx, ly = px0 + rng.normal(0, 9), top + 12 + rng.random() * 12
        else:
            lx, ly = x1 - 2 + rng.normal(0, 3.5), top + 10 - t * 78
        g = lit(("#3f6a34", "#5a8a44", "#2f5228", "#7fa858")[int(rng.integers(4))], (lx, ly, z0), (0, 0, -1), 1.1)
        c = P(lx, ly, zf)
        a = rng.random() * 6.28
        ivy.poly([(c[0] + np.cos(a) * 3.2, c[1] + np.sin(a) * 3.2), (c[0] + np.cos(a + 2.2) * 2.4, c[1] + np.sin(a + 2.2) * 2.4), (c[0] + np.cos(a + 4.0) * 2.4, c[1] + np.sin(a + 4.0) * 2.4)], g)
    L.sheet(ivy)


def stair_x(n):
    """Where the riser of step n stands (n = 1 is the first)."""
    return STAIR["x0"] + STAIR["tread"] * (n - 1)


def stairs(L, fine=False):
    st = STAIR
    z0, T, R, N = st["z0"], st["tread"], st["rise"], st["steps"]
    ra, rb = z0 + 20, ZW - 20                                           # the carpet runner lies between these
    wood_t = grainy("#b07a44", SEED + 70, "z")
    wood_r = grainy("#96602f", SEED + 71, "z")
    carpet = "#8c2f38"
    if not fine:
        # ---- the side of the staircase toward the room: panelling under a saw-tooth of step ends
        prof = [(stair_x(1), 0)]
        for n in range(1, N + 1):
            prof += [(stair_x(n), R * n), (stair_x(n + 1), R * n)]
        prof += [(stair_x(N + 1), 0)]
        Fc(L, [(x, y, z0) for x, y in prof], grainy("#a56c3a", SEED + 72, "y", 0.12, (50, 5)), n=(0, 0, -1))
        for n in range(1, N + 1):
            xa, xb, y = stair_x(n), stair_x(n + 1), R * n
            # the riser (it faces down the stairs, toward the middle of the room), wood with carpet up its middle
            Fc(L, [(xa, y - R, z0), (xa, y - R, ZW), (xa, y, ZW), (xa, y, z0)], wood_r, n=(-1, 0, 0))
            Fc(L, [(xa - 0.2, y - R, ra), (xa - 0.2, y - R, rb), (xa - 0.2, y, rb), (xa - 0.2, y, ra)], carpet, n=(-1, 0, 0), dim=0.9)
            # the tread
            Fc(L, [(xa - 2.5, y, z0 - 2.5), (xb, y, z0 - 2.5), (xb, y, ZW), (xa - 2.5, y, ZW)], wood_t, n=(0, 1, 0))
            Fc(L, [(xa - 2.5, y + 0.2, ra), (xb, y + 0.2, ra), (xb, y + 0.2, rb), (xa - 2.5, y + 0.2, rb)], carpet, n=(0, 1, 0))
        if isinstance(L, Collector):                                    # for their shadow the stairs are so many boxes
            for n in range(1, N + 1):
                L.boxes.append(corners(stair_x(n), stair_x(N + 1), 0, R * n, z0, ZW))
        # ---- the closet door under the stairs: a small plank door, standing a little open
        c = CLOSET
        zin = z0 - 0.3
        if not isinstance(L, Collector):
            Fc(L, [(c["x0"] - 4, 0, zin), (c["x1"] + 4, 0, zin), (c["x1"] + 4, c["top"] + 4, zin), (c["x0"] - 4, c["top"] + 4, zin)], "#7a4c2a", n=(0, 0, -1))
            Fc(L, [(c["x0"], 0, zin - 0.1), (c["x1"], 0, zin - 0.1), (c["x1"], c["top"], zin - 0.1), (c["x0"], c["top"], zin - 0.1)], "#0b0910", n=(0, 0, -1), lit=False)
            leaf = [(c["x0"] + 2.0, 0.5, z0 - c["ajar"]), (c["x1"], 0.5, z0 - 0.6), (c["x1"], c["top"] - 0.5, z0 - 0.6), (c["x0"] + 2.0, c["top"] - 0.5, z0 - c["ajar"])]
            Fc(L, leaf, grainy("#b47a44", SEED + 73, "y", 0.14, (50, 5)))
        # ---- the newel post at the foot
        nx = stair_x(1) - 9
        B(L, nx - 6.5, nx + 6.5, 0, 112, z0 - 9, z0 + 4, grainy("#8a5630", SEED + 74, "y"), top="#b98450")
        return
    if isinstance(L, Collector):
        return
    s = Sheet(SHAPE)
    lt = lambda p, a=1.0: lit("#e0a868", p, (0, 1, 0), a)
    for n in range(1, N + 1):
        xa, xb, y = stair_x(n), stair_x(n + 1), R * n
        # nosing: a light edge to every tread, a shadow under it; the end of the tread turned round the corner
        s.line(pts2([(xa - 2.5, y, z0 - 2.5), (xb, y, z0 - 2.5)]), lt((xa, y, z0)), 1.0, 0.9)
        s.line(pts2([(xa - 2.5, y, z0 - 2.5), (xa - 2.5, y, ZW)]), lt((xa, y, z0 + 40)), 0.9, 0.75)
        s.line(pts2([(xa - 2.5, y - 2.2, z0 - 2.5), (xb, y - 2.2, z0 - 2.5)]), "#1a1014", 1.0, 0.5)
        s.line(pts2([(xa - 0.3, y - 2.0, z0), (xa - 0.3, y - 2.0, ZW)]), "#1a1014", 1.0, 0.45)
        s.line(pts2([(xa, y - R, z0), (xa, y - 2, z0)]), "#1a1014", 0.8, 0.35)
        # a small scrolled bracket under each tread end
        s.poly(pts2([(xa + 1, y - 2.5, z0 - 0.2), (xa + 15, y - 2.5, z0 - 0.2), (xa + 9, y - 7, z0 - 0.2), (xa + 4, y - 10, z0 - 0.2), (xa + 1, y - 10.5, z0 - 0.2)]), lit("#bb8248", (xa, y, z0), (0, 0, -1)), 0.9)
        # the runner's edges, its border stripe, and the brass rod that holds it in the angle of the step
        for zz in (ra, rb):
            s.line(pts2([(xa - 2.5, y + 0.3, zz), (xb, y + 0.3, zz)]), lit("#d8b060", (xa, y, zz)), 0.8, 0.8)
            s.line(pts2([(xa - 0.3, y - R, zz), (xa - 0.3, y, zz)]), lit("#d8b060", (xa, y, zz), (-1, 0, 0)), 0.8, 0.7)
        s.line(pts2([(xb - 0.6, y + 0.8, ra - 4), (xb - 0.6, y + 0.8, rb + 4)]), lit("#f0cc6a", (xb, y, z0 + 40)), 1.0, 0.95)
        s.line(pts2([(xb - 1.2, y + 0.4, ra), (xb - 1.2, y + 0.4, rb)]), "#1a1014", 1.2, 0.35)
    # panelling under the stairs: upright boards, a skirting, a shadow where the saw-tooth overhangs
    last = stair_x(N + 1)
    xx = stair_x(1) + 14
    while xx < last:
        top = R * int((xx - st["x0"]) / T) - 3                          # the boards stop under the step ends
        at_door = CLOSET["x0"] - 5 < xx < CLOSET["x1"] + 5
        foot = CLOSET["top"] + 5 if at_door else 11
        if top > foot + 3:
            s.line(pts2([(xx, foot, z0 - 0.2), (xx, top, z0 - 0.2)]), "#1a1014", 0.9, 0.34)
            if not at_door:
                s.line(pts2([(xx + 1.2, foot, z0 - 0.2), (xx + 1.2, top, z0 - 0.2)]), "#ffd9a0", 0.7, 0.16)
        xx += 14
    s.poly(pts2([(stair_x(1), 0, z0 - 0.3), (CLOSET["x0"] - 4, 0, z0 - 0.3), (CLOSET["x0"] - 4, 11, z0 - 0.3), (stair_x(1), 11, z0 - 0.3)]), lit("#8c5a30", (400, 6, z0), (0, 0, -1)))
    s.line(pts2([(stair_x(1), 11, z0 - 0.3), (CLOSET["x0"] - 4, 11, z0 - 0.3)]), lit("#d09a5c", (400, 11, z0)), 0.8, 0.8)
    L.sheet(s)

    # ---- the closet door: planks, two ledges, a ring latch; the dark of the closet at its open edge
    c = CLOSET
    s = Sheet(SHAPE)

    def on_leaf(u, y):                                                  # u: 0 at the open edge, 1 at the hinges
        return (lerp(c["x0"] + 2.0, c["x1"], u), y, lerp(z0 - c["ajar"], z0 - 0.6, u) - 0.3)
    for k in range(1, 5):
        s.line(pts2([on_leaf(k / 5, 1), on_leaf(k / 5, c["top"] - 1)]), "#1a1014", 0.9, 0.42)
        s.line(pts2([on_leaf(k / 5 + 0.02, 1), on_leaf(k / 5 + 0.02, c["top"] - 1)]), "#ffd9a0", 0.7, 0.18)
    for yy in (22, 80):
        s.poly(pts2([on_leaf(0.03, yy), on_leaf(0.97, yy), on_leaf(0.97, yy + 9), on_leaf(0.03, yy + 9)]), lit("#c08a50", on_leaf(0.5, yy), (0, 0, -1)), 0.92)
        s.line(pts2([on_leaf(0.03, yy), on_leaf(0.97, yy)]), "#1a1014", 0.9, 0.5)
    k = P(*on_leaf(0.13, 52))
    s.ellipse(k[0], k[1], 2.6, 2.6, lit("#3a3038", on_leaf(0.1, 52), (0, 0, -1)))
    s.ellipse(k[0], k[1] + 0.2, 1.5, 1.5, lit("#c9a050", on_leaf(0.1, 52), (0, 0, -1)))
    for hy in (16, 88):                                                 # strap hinges
        s.line(pts2([on_leaf(1.0, hy), on_leaf(0.72, hy)]), lit("#3a3038", on_leaf(0.9, hy), (0, 0, -1)), 1.6)
    s.line(pts2([on_leaf(0.0, 0.5), on_leaf(0.0, c["top"] - 0.5)]), lit("#e8b878", on_leaf(0.0, 50), (-0.5, 0, -0.8)), 1.3, 0.95)       # the door's edge, catching the lamp
    s.line(pts2([(c["x0"] - 4, 0, z0 - 0.4), (c["x0"] - 4, c["top"] + 4, z0 - 0.4), (c["x1"] + 4, c["top"] + 4, z0 - 0.4), (c["x1"] + 4, 0, z0 - 0.4)]), "#1a1014", 0.9, 0.5)
    L.sheet(s)

    # ---- newel, balusters and handrail (they stand on the room side of the stairs, in front of the treads)
    s = Sheet(SHAPE)
    zb = z0 + 3.0
    rail_h = 88.0
    nx = stair_x(1) - 9
    top_newel = (nx, 100.0, zb)
    wood_l, wood_m, wood_d = "#d09a5c", "#9a6436", "#4a2c1c"

    def rail_at(x):                                                     # the height of the handrail above the floor at x
        return (x - stair_x(1)) / T * R + R * 0.5 + rail_h
    end = stair_x(N + 1) + 40
    for n in range(1, N + 2):
        for f in (0.30, 0.80):
            bx = stair_x(n) + T * f
            if n > N:
                continue
            foot = (bx, R * n, zb)
            head = (bx, rail_at(bx) - 2, zb)
            mid = (bx, R * n + 26, zb)
            cl, cd = lit("#efe6d0", (bx, R * n + 50, zb), (-0.5, 0.2, -0.8)), lit("#bdb29a", (bx, R * n + 50, zb), (0.6, 0, -0.6), 0.7)
            s.line(pts2([foot, head]), cd, 1.9)
            s.line(pts2([(bx - 0.5, R * n, zb), (bx - 0.5, rail_at(bx) - 2, zb)]), cl, 1.0)
            c2 = P(*mid)
            s.ellipse(c2[0], c2[1], 1.9, 2.8, cl)                       # the turned swelling low on each baluster
    rail = [(nx, 100.0, zb), (stair_x(1) + 4, rail_at(stair_x(1) + 4), zb), (end, rail_at(end), zb)]
    s.line(pts2([(x, y - 2.2, z) for x, y, z in rail]), lit(wood_d, (stair_x(4), rail_at(stair_x(4)), zb), (0, -1, 0), 0.9), 2.6)
    s.line(pts2(rail), lit(wood_m, (stair_x(4), rail_at(stair_x(4)), zb), (0, 0.6, -0.8)), 3.0)
    for i in range(N):
        xa = stair_x(1) + T * i
        s.line(pts2([(xa, rail_at(xa) + 1.4, zb), (xa + T, rail_at(xa + T) + 1.4, zb)]), lit(wood_l, (xa, rail_at(xa), zb), (0, 1, 0)), 0.9, 0.85)
    # the newel post: chamfered, capped, with a ball on top
    s.line(pts2([(nx - 6.5, 0, z0 - 9), (nx - 6.5, 112, z0 - 9)]), lit(wood_l, (nx, 60, z0 - 9), (-1, 0, 0)), 0.9, 0.7)
    s.line(pts2([(nx + 6.5, 0, z0 - 9), (nx + 6.5, 112, z0 - 9)]), "#1a1014", 0.9, 0.5)
    for yy in (14, 96):
        s.line(pts2([(nx - 6.5, yy, z0 - 9.2), (nx + 6.5, yy, z0 - 9.2)]), "#1a1014", 0.9, 0.5)
        s.line(pts2([(nx - 6.5, yy + 1.5, z0 - 9.2), (nx + 6.5, yy + 1.5, z0 - 9.2)]), lit(wood_l, (nx, yy, z0 - 9), (0, 1, 0)), 0.8, 0.6)
    s.poly(pts2([(nx - 9, 112, z0 - 11), (nx + 9, 112, z0 - 11), (nx + 9, 116, z0 - 11), (nx - 9, 116, z0 - 11)]), lit("#a8703c", (nx, 114, z0 - 11), (0, 0, -1)))
    s.poly(pts2([(nx - 9, 116, z0 - 11), (nx + 9, 116, z0 - 11), (nx + 9, 116, z0 + 6), (nx - 9, 116, z0 + 6)]), lit("#c08a50", (nx, 116, z0), (0, 1, 0)))
    b = P(nx, 124, z0 - 3)
    rr = 7.0 * cam.scale(z0)
    s.ellipse(b[0], b[1], rr, rr, lit("#8a5630", (nx, 124, z0 - 3), (0.4, 0.2, -0.8)))
    s.ellipse(b[0] - rr * 0.25, b[1] - rr * 0.25, rr * 0.62, rr * 0.62, lit("#b98450", (nx, 124, z0 - 3), (-0.4, 0.6, -0.6)))
    s.ellipse(b[0] - rr * 0.4, b[1] - rr * 0.4, rr * 0.2, rr * 0.2, lit("#f0d0a0", (nx, 124, z0 - 3), (0, 1, 0)))
    L.sheet(s)


def small_things(L, fine=False):
    """The little step-stool under the window where the youngest keeps watch, and the umbrella stand by the door."""
    if not fine:
        B(L, -418, -386, 0, 24, ZW - 30, ZW - 6, grainy("#b8824a", SEED + 80, "x"), top=grainy("#c8925a", SEED + 81, "x"))
        B(L, -604, -582, 0, 52, ZW - 26, ZW - 6, "#4a5a52", top="#1c2024")
        return
    if isinstance(L, Collector):
        return
    s = Sheet(SHAPE)
    z = ZW - 30.2
    s.poly(pts2([(-413, 0, z), (-391, 0, z), (-391, 15, z), (-413, 15, z)]), "#1a1014", 0.55)            # the open space between its legs
    s.line(pts2([(-418, 24, z), (-386, 24, z)]), lit("#e8b878", (-400, 24, z)), 0.9, 0.8)
    # umbrellas: a black one and a red one
    for (x, c, lean) in ((-596, "#2a2a34", -3), (-589, "#a83a34", 4)):
        s.line(pts2([(x, 44, ZW - 16), (x + lean, 96, ZW - 16)]), lit(c, (x, 70, ZW - 16), (0, 0, -1)), 2.4)
        s.line(pts2([(x + lean, 96, ZW - 16), (x + lean + 1, 106, ZW - 16), (x + lean + 5, 106, ZW - 16)]), lit("#c08a50", (x, 100, ZW - 16), (0, 0, -1)), 1.2)
    L.sheet(s)


def clutter(L, fine=False):
    """What the family left lying about: washing on the stairs waiting to go up, two library books, the
    bear, the waste-paper basket by the desk, a ball. (Their small details are in _fine.)"""
    st = STAIR
    z0, R = st["z0"], st["rise"]
    if fine:
        return
    # a pile of folded washing on the second step, on the carpet
    xa = stair_x(2) + 3
    for k, c in enumerate(("#e8e2d4", "#6a9cc4", "#e8e2d4", "#e0a0a8")):
        B(L, xa + k * 0.6, xa + 19 - k * 0.4, 2 * R + k * 4.5, 2 * R + (k + 1) * 4.5, z0 + 26, z0 + 58, c, cast=False)
    # two books on the fourth
    xb = stair_x(4) + 4
    B(L, xb, xb + 15, 4 * R, 4 * R + 3.5, z0 + 6, z0 + 26, "#3f6f8f", top="#4f86a8", cast=False)
    B(L, xb + 1.5, xb + 14, 4 * R + 3.5, 4 * R + 6.5, z0 + 7, z0 + 24, "#b5483a", top="#d0604a", cast=False)
    # the waste-paper basket, between the window and the desk
    B(L, -186, -164, 0, 30, ZW - 26, ZW - 5, "#b8904e", top="#3a2a1c", cast=True)


# ---------------------------------------------------------------- putting the backdrop together
def backdrop(pieces, seed=SEED):
    """The under-painting of the whole empty room: big planes, their local color and their light.
    `pieces` are the furniture functions, gone over once here for the shadows they throw."""
    shape = SHAPE
    px, py = grid(shape)
    col_ = Collector()
    for f in pieces:
        f(col_)
    bookcase(col_)
    stairs(col_)
    small_things(col_)
    clutter(col_)
    sh = Shadows(LIGHTS.lamps)
    for cs in col_.boxes:
        sh.add(cs)
    # the banisters stand between the reading lamp and the stair wall: their shadows climb it, spread wide
    st = STAIR
    zb = st["z0"] + 3.0
    rail = lambda x: (x - stair_x(1)) / st["tread"] * st["rise"] + st["rise"] * 0.5 + 88.0
    for n in range(1, st["steps"] + 1):
        for f in (0.30, 0.80):
            bx = stair_x(n) + st["tread"] * f
            sh.add(corners(bx - 1.6, bx + 1.6, st["rise"] * n, rail(bx), zb - 1.5, zb + 1.5), lamps=("floorlamp", "pendant"), strength=0.75)
        xa, xb = stair_x(n), stair_x(n + 1)
        sh.add([(xa, rail(xa) - 4, zb - 2), (xb, rail(xb) - 4, zb - 2), (xb, rail(xb) - 4, zb + 2), (xa, rail(xa) - 4, zb + 2),
                (xa, rail(xa) + 2, zb - 2), (xb, rail(xb) + 2, zb - 2), (xb, rail(xb) + 2, zb + 2), (xa, rail(xa) + 2, zb + 2)], lamps=("floorlamp", "pendant"), strength=0.75)
    fsh, wsh = sh.done({"pendant": 3.2, "floorlamp": 3.6, "pianolamp": 2.6, "screen": 5.0, "window": 6.0})
    pic = np.zeros((H, W, 3), dtype=F32)

    # ---- the floor
    X, Z, below = cam.floor_grid(shape)
    floor = (py >= WALL_Y).astype(F32)
    light = LIGHTS.light(X, 0.0, Z, (0, 1, 0), fsh)
    light = light * (1 + ((wnoise(X, Z * 1.3, 110, seed + 90) - 0.5) * 0.20)[..., None])     # a wash of light is never quite even
    drift = (wnoise(X * 0.8, Z * 1.6, 170, seed + 93) - 0.5) * 0.11                           # nor of one color: warmer here, cooler there
    light = light * (1 + drift[..., None] * np.array([1.0, 0.1, -0.9], dtype=F32))
    over(pic, LIGHTS.tone(floor_albedo(X, Z) * light), floor)

    # ---- the back wall
    Xw, Yw = (px + 0.5 - VX) / KW, (WALL_Y - py - 0.5) / KW
    wall = ((py < WALL_Y) & (py >= CEIL_Y)).astype(F32)
    walb, glass, doorglass, bare = wall_albedo()
    wlight = LIGHTS.light(Xw, Yw, ZW, (0, 0, -1), wsh)
    wlight = wlight * (1 + ((wnoise(Xw, Yw, 120, seed + 91) - 0.5) * 0.20)[..., None])
    drift = (wnoise(Xw, Yw * 1.2, 190, seed + 94) - 0.5) * 0.12
    wlight = wlight * (1 + drift[..., None] * np.array([1.0, 0.1, -0.9], dtype=F32))
    over(pic, LIGHTS.tone(walb * wlight), wall)
    over(pic, night_view(), glass * wall)
    frost = ramp(np.clip((py - wp(0, 190)[1]) / 40.0, 0, 1), [(0.0, "#2a3c6a"), (1.0, "#3f5686")])
    frost = frost * (1 + ((noise(shape, 5, seed + 55, 2) - 0.5) * 0.25)[..., None])
    lx, ly = wp(DOOR["lx0"] + 20, 180)                         # the porch light has been left on for them: a warm blur in the frosted glass
    glow(frost, "#ffb45a", (np.exp(-(((px - lx) / 7.0) ** 2 + ((py - ly) / 8.0) ** 2)) * 0.85).astype(F32))
    over(pic, frost, doorglass * wall)

    # ---- the ceiling (a stage painter's ceiling: see ceil_pt in the plan): plaster between dark beams
    ceil = (py < CEIL_Y).astype(F32)
    zc = ZW * np.clip(py / CEIL_Y, 0, 1) ** 1.2
    kc = FO / (Z0 + zc)
    Xc = (px - VX) / kc
    calb = col("#dcd0b8")[None, None, :] * (1 + ((noise(shape, (120, 40), seed + 56, 3) - 0.5) * 0.10)[..., None])
    # it is a boarded ceiling, painted long ago: the boards run from the back wall toward us, each a little
    # different, and the joints between them open like a fan, which is what tells the eye it is overhead
    bw = 15.0
    bi = np.floor(Xc / bw)
    bf = Xc / bw - bi
    calb = calb * (1 + ((hash01(bi, 5.0, seed) - 0.5) * 0.16)[..., None])
    joint = step(0.90, 1.0, bf) + step(0.06, 0.0, bf) * 0.6
    calb = calb * (1 - np.clip(joint, 0, 1) * 0.55)[..., None]
    butt = (hash01(bi, np.floor((zc + hash01(bi, 9.0, seed) * 160.0) / 160.0), seed + 2.0) > 0.0) & (np.abs(np.mod(zc + hash01(bi, 9.0, seed) * 160.0, 160.0) - 80.0) > 78.2)
    calb = calb * (1 - butt.astype(F32) * 0.4)[..., None]
    clight = LIGHTS.light(Xc, WALL_H, zc, (0, -1, 0), bounce=0.8)
    clight = clight * (1 + ((noise(shape, (150, 50), seed + 92, 3) - 0.5) * 0.30)[..., None])
    clight = clight * (1 + ((noise(shape, (220, 70), seed + 95, 3) - 0.5) * 0.14)[..., None] * np.array([1.0, 0.1, -0.9], dtype=F32))
    clight = clight + (np.clip(py / CEIL_Y, 0, 1) ** 2.2 * 0.085)[..., None] * col((1.0, 0.82, 0.56))     # a little comes back up off the lit wall
    over(pic, LIGHTS.tone(calb * clight * 0.82), ceil)
    oak = col("#7a5434")[None, None, :] * (1 + ((noise(shape, (90, 4), seed + 57, 3) - 0.5) * 0.24)[..., None])
    for zb in BEAMS:                                           # each beam: the side toward us, then its underside in the lamplight
        y_near, y_far = ceil_pt(0, zb - 9)[1], ceil_pt(0, zb + 9)[1]
        drop = 15.0 * cam.scale(zb) * 0.72
        side = ((py >= y_near) & (py < y_near + drop)).astype(F32) * ceil
        under = ((py >= y_near + drop) & (py < y_far + drop)).astype(F32) * ceil
        Xb = (px - VX) / cam.scale(zb)
        tint(pic, "#2a2030", np.clip(1 - (py - (y_far + drop)) / 7.0, 0, 1) * (py >= y_far + drop) * ceil * 0.45)     # its shadow on the plaster behind
        over(pic, LIGHTS.tone(oak * LIGHTS.light(Xb, WALL_H - 8, zb - 9, (0, 0, -1), bounce=0.8) * 0.8), side)
        over(pic, LIGHTS.tone(oak * 1.25 * LIGHTS.light(Xb, WALL_H - 16, zb, (0, -1, 0), bounce=0.8)), under)

    # ---- where furniture meets the floor it is darkest
    foot = Image.new("L", (W * 2, H * 2), 0)
    for cs in col_.boxes:
        if min(c[1] for c in cs) < 3.0:
            hp = hull([P(x, 0.0, z) for x, y, z in cs])
            if len(hp) >= 3:
                ImageDraw.Draw(foot).polygon([(x * 2, y * 2) for x, y in grow(hp, 2.0)], fill=255)
    foot = np.asarray(foot.resize((W, H), Image.BOX), dtype=F32) / 255
    tint(pic, "#3a2c44", np.clip(blur(foot, 2.6) * 0.55, 0, 1) * floor)

    solid = Layer()
    bookcase(solid)
    stairs(solid)
    small_things(solid)
    clutter(solid)
    L = Layer(pic)
    solid.onto(L)
    return L, dict(fsh=fsh, wsh=wsh, glass=glass * wall, doorglass=doorglass * wall, wall=wall, floor=floor, ceil=ceil,
                   bare=bare * wall * (1 - np.clip(solid.w * 2, 0, 1)), solid=solid.w)

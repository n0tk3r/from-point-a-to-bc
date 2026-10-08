"""A room seen through ONE camera, so that floor, walls, ceiling, furniture and people agree.

Why this file exists: a room looks flat when its parts are drawn from different places (a wall seen
face-on, a floor seen from high up, furniture in a third projection). Here everything goes through a
single View, and the View is worked out from the two numbers the GAME uses to size people
(`horizon` and `full`), so the painted room and the people the game draws in it share one eye.

ROOM MEASUREMENTS are in centimetres:
    X  across the room, left to right along the back wall
    Y  up from the floor
    Z  out from the back wall toward us (the back wall is Z = 0)
The camera stands at (cam_x, eye, cam_z), looks toward the back wall, and may be turned (`yaw`,
degrees, positive = to the right). yaw 0 is a one-point view (back wall face-on, side walls running
to one vanishing point); a yaw of 20 to 35 is a corner view (two vanishing points).

    v = View(horizon=170, full=470, cam=(250, 760), yaw=24, focal=640)
    v.pt(X, Y, Z)            -> (x, y) in the picture
    v.person(X, Z)           -> (x, y of the feet, height in pixels of a 175 cm grown-up standing there)
    v.poly([(X, Y, Z), ...]) -> picture polygon, clipped where it passes behind the lens
    v.box(X0, X1, Y0, Y1, Z0, Z1) -> the faces of a box that the camera can see, far ones first
    v.floor_xz(shape)        -> for every pixel, the place on the floor it shows (X, Z, mask)
    v.plane_uv(shape, "X", 800) -> the same for a wall: (u along it, v up it, mask)

`eye` (how high the lens is) is not chosen: it follows from horizon and full. A grown-up, 175 cm, is
`adult` (160) pixels tall where their feet are on the row `full`, and nothing at the row `horizon`.
"""

import math

import numpy as np

F32 = np.float32
ADULT_CM = 175.0


class View:
    def __init__(self, horizon, full, cam, yaw=0.0, focal=640.0, centre_x=400.0, adult=160.0, size=(800, 600)):
        self.w, self.h = size
        self.hz, self.full, self.F, self.cx = float(horizon), float(full), float(focal), float(centre_x)
        self.s0 = adult / ADULT_CM                       # pixels per cm on the `full` row
        self.eye = (self.full - self.hz) / self.s0       # lens height above the floor, cm
        self.cam_x, self.cam_z = float(cam[0]), float(cam[1])
        self.yaw = float(yaw)
        t = math.radians(self.yaw)
        self.fx, self.fz = math.sin(t), -math.cos(t)     # the way the lens points, on the floor plan
        self.rx, self.rz = math.cos(t), math.sin(t)      # "to the right", on the floor plan
        self.near = 25.0

    # ---------------------------------------------------------------- room -> picture
    def cam_space(self, X, Y, Z):
        """Room place -> (across, up from the lens, depth along the lens axis), in cm."""
        dx, dz = X - self.cam_x, Z - self.cam_z
        return (dx * self.rx + dz * self.rz, Y - self.eye, dx * self.fx + dz * self.fz)

    def _proj(self, a, u, d):
        k = self.F / d
        return (self.cx + a * k, self.hz - u * k)

    def pt(self, X, Y, Z):
        a, u, d = self.cam_space(X, Y, Z)
        return self._proj(a, u, max(d, 1e-3))

    def depth(self, X, Z):
        return self.cam_space(X, 0, Z)[2]

    def scale_at(self, X, Z):
        """Picture pixels per centimetre for anything standing at this place on the floor."""
        return self.F / max(self.depth(X, Z), 1e-3)

    def person(self, X, Z, cm=ADULT_CM):
        x, y = self.pt(X, 0, Z)
        return x, y, cm * self.scale_at(X, Z)

    def poly(self, pts):
        """A polygon in the room -> picture points. Clipped against the plane just in front of the lens."""
        cs = [self.cam_space(*p) for p in pts]
        out = []
        n = len(cs)
        for i in range(n):
            p, q = cs[i], cs[(i + 1) % n]
            pin, qin = p[2] >= self.near, q[2] >= self.near
            if pin:
                out.append(p)
            if pin != qin:
                t = (self.near - p[2]) / (q[2] - p[2])
                out.append(tuple(p[k] + (q[k] - p[k]) * t for k in range(3)))
        return [self._proj(*c) for c in out]

    def line(self, p, q):
        """A straight edge in the room -> its two picture ends (None if it is wholly behind the lens)."""
        r = self.poly([p, q])
        return (r[0], r[1]) if len(r) >= 2 else None

    def box(self, X0, X1, Y0, Y1, Z0, Z1):
        """A box standing in the room -> [(name, picture polygon, normal)], only the faces the lens can
        see, the farthest first. Names: 'top', 'bottom', 'left' (faces -X), 'right' (+X), 'back' (faces
        -Z, toward the back wall), 'front' (+Z, toward us). The normal is for lighting."""
        C = (self.cam_x, self.eye, self.cam_z)
        faces = {
            "top":    ([(X0, Y1, Z0), (X1, Y1, Z0), (X1, Y1, Z1), (X0, Y1, Z1)], (0, 1, 0)),
            "bottom": ([(X0, Y0, Z0), (X1, Y0, Z0), (X1, Y0, Z1), (X0, Y0, Z1)], (0, -1, 0)),
            "left":   ([(X0, Y0, Z0), (X0, Y0, Z1), (X0, Y1, Z1), (X0, Y1, Z0)], (-1, 0, 0)),
            "right":  ([(X1, Y0, Z0), (X1, Y0, Z1), (X1, Y1, Z1), (X1, Y1, Z0)], (1, 0, 0)),
            "back":   ([(X0, Y0, Z0), (X1, Y0, Z0), (X1, Y1, Z0), (X0, Y1, Z0)], (0, 0, -1)),
            "front":  ([(X0, Y0, Z1), (X1, Y0, Z1), (X1, Y1, Z1), (X0, Y1, Z1)], (0, 0, 1)),
        }
        seen = []
        for name, (pts, n) in faces.items():
            mid = [sum(p[k] for p in pts) / 4 for k in range(3)]
            if sum(n[k] * (C[k] - mid[k]) for k in range(3)) <= 0:
                continue
            pp = self.poly(pts)
            if len(pp) >= 3:
                seen.append((self.cam_space(*mid)[2], name, pp, n))
        seen.sort(key=lambda s: -s[0])
        return [(name, pp, n) for _, name, pp, n in seen]

    def stairs(self, X0, X1, z_foot, z_top, rise, steps, floor=0.0):
        """A closed flight of stairs as a list of boxes (X0, X1, Y0, Y1, Z0, Z1), one per step, the foot first.
        It climbs from z_foot to z_top (either way round) and gains `rise` cm in `steps` steps."""
        out, dz, dy = [], (z_top - z_foot) / steps, rise / steps
        for i in range(steps):
            za, zb = z_foot + dz * i, z_foot + dz * (i + 1)
            out.append((X0, X1, floor, floor + dy * (i + 1), min(za, zb), max(za, zb)))
        return out

    # ---------------------------------------------------------------- picture -> room
    def _rays(self, shape):
        h, w = shape
        py, px = np.mgrid[0:h, 0:w].astype(F32)
        a = (px + 0.5 - self.cx) / self.F                # across, per unit depth
        u = (self.hz - (py + 0.5)) / self.F              # up, per unit depth
        return a * self.rx + self.fx, u, a * self.rz + self.fz      # the ray's (dX, dY, dZ) per unit depth

    def floor_xz(self, shape, Y=0.0):
        """For every pixel: the place on the floor (or on any level plane at height Y) it shows.
        -> (X, Z, mask). The mask is 1 where the plane is really seen."""
        dX, dY, dZ = self._rays(shape)
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (Y - self.eye) / dY
        ok = np.isfinite(t) & (t > self.near)
        t = np.where(ok, t, 0)
        return (self.cam_x + dX * t).astype(F32), (self.cam_z + dZ * t).astype(F32), ok.astype(F32)

    def plane_uv(self, shape, axis, at):
        """For every pixel: where it falls on an upright wall. axis "X": the wall X = at (u is Z along it);
        axis "Z": the wall Z = at (u is X along it). -> (u, v, mask), v = height above the floor."""
        dX, dY, dZ = self._rays(shape)
        with np.errstate(divide="ignore", invalid="ignore"):
            t = ((at - self.cam_x) / dX) if axis == "X" else ((at - self.cam_z) / dZ)
        ok = np.isfinite(t) & (t > self.near)
        t = np.where(ok, t, 0)
        u = (self.cam_z + dZ * t) if axis == "X" else (self.cam_x + dX * t)
        return u.astype(F32), (self.eye + dY * t).astype(F32), ok.astype(F32)

    def depth_map(self, shape, Y=0.0):
        """Depth along the lens axis, in cm, of the floor shown at every pixel (for haze and for fading light)."""
        dX, dY, dZ = self._rays(shape)
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (Y - self.eye) / dY
        return np.where(np.isfinite(t) & (t > 0), t, 1e6).astype(F32)

    # ---------------------------------------------------------------- for the layout file
    def vanishing(self):
        """Where lines running along Z, and along X, meet in the picture: ((x, y), (x, y)). None when they stay parallel."""
        def vp(dx, dz):
            d = dx * self.fx + dz * self.fz
            if abs(d) < 1e-6:
                return None
            return (self.cx + self.F * (dx * self.rx + dz * self.rz) / d, self.hz)
        return vp(0, -1), vp(1, 0)

    def row_of(self, X, Z):
        return self.pt(X, 0, Z)[1]

    def floor_at(self, x, y):
        """A place in the picture (below the horizon) -> the place on the floor (X, Z)."""
        a, u = (x - self.cx) / self.F, (self.hz - y) / self.F
        if u >= -1e-6:
            return None
        t = -self.eye / u
        return (self.cam_x + (a * self.rx + self.fx) * t, self.cam_z + (a * self.rz + self.fz) * t)

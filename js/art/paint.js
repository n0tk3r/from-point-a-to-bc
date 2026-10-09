// The painted renderer for people (the address switch ?people=painted).
//
// pix.js turns the rig's shapes into pixel art: hard edges and two flat tones. This file takes exactly the same shapes
// (limbs, balls, the shadow on the ground, the folds drawn on cloth, the buttons) and paints them instead, so that a
// person standing in one of the game's paintings looks painted into it:
//
//   - each form is modelled by how it turns to the light (from the upper left, as everywhere in the game): the four
//     tones of its material are blended smoothly, with a soft terminator, warm light and cooler shade, a touch of light
//     thrown back up into the shade from the ground, and the brightest tone only where a form faces the light squarely;
//   - where one part lies in front of another it throws a soft shadow on it (under the chin, under a hem, beside an arm);
//   - the outline is anti-aliased, with a soft painter's edge a little darker than the form;
//   - the paint has a surface: a fine grain and short strokes that follow the form, at the same scale as the grain of
//     the painted backgrounds (one picture pixel of the stage), fixed to the body so that it never swims as people move;
//   - hair is painted in locks, with a broken sheen where it catches the light;
//   - and every face is painted, not stamped: eyes with whites, a coloured iris, a pupil and a catchlight, an upper lid,
//     lashes for women and girls, brows that carry expression, a nose modelled by light and shade, coloured lips, warm
//     cheeks (see FACES below and faceOf()).
//
// A PaintSurface has the same drawing calls as pix.js's Surface (limb, ball, poly, rect, oval, dot, stroke, mark,
// finish, bounds, clipBelow, toCanvas), so the rig and every costume in people.js draw on it unchanged. It works at
// `k` painted pixels to one picture pixel of the stage: the cast asks for 2 or 3 when the stage is shown that big, so
// that faces keep their eyes, brows and lashes.
//
// Colour hook. Every colour this renderer uses goes through `colourKey`: colourKey.tones(material) gives a material's
// four tones (as packed numbers, pix.js's pack()), colourKey.color(packed) any other colour (an iris, lips, a blush).
// Both default to the colours as they are. A middle-ground study keys the people of a scene by setting them (see
// setColourKey), exactly as it keyed the four tones of pix.js.

// ---------------------------------------------------------------- the switch
/** Painted people are off unless the address asks for them (?people=painted). When the author's team approves the
    look, this one line becomes `true` and painted people are the game's own (?people=pixel then shows the old ones). */
export const PAINTED_BY_DEFAULT = false;
/** Are people painted in this page? (Read once, from the address.) */
export const paintedPeople = (() => {
  try {
    const q = new URLSearchParams(globalThis.location ? globalThis.location.search : "").get("people");
    if (q === "painted") return true;
    if (q === "pixel" || q === "pixels") return false;
  } catch { /* no address to read */ }
  return PAINTED_BY_DEFAULT;
})();

// ---------------------------------------------------------------- the colour hook
const same = (x) => x;
export const colourKey = { tones: null, color: null, id: "" };
/** Key every colour painted from now on: tones(material) -> four packed tones, color(packed) -> packed (null: as they
    are). `id` names the key: pictures painted in one key are kept apart from those painted in another (cast.js). With
    people painted by the worker (js/art/painter.js), load the module that sets the key there as well (cast.js keyPainter). */
export function setColourKey(tones = null, color = null, id = tones || color ? "key" + ++keys : "") { colourKey.tones = tones; colourKey.color = color; colourKey.id = id; }
let keys = 0;
/** fn(), painted with no colour key: the team portraits belong to the interface, not to a scene, and are never keyed. */
export function unkeyed(fn) {
  const was = { ...colourKey };
  colourKey.tones = null; colourKey.color = null; colourKey.id = "";
  try { return fn(); } finally { Object.assign(colourKey, was); }
}

// ---------------------------------------------------------------- colour arithmetic (sRGB, 0 to 1)
const unpack = (c) => [(c & 255) / 255, ((c >>> 8) & 255) / 255, ((c >>> 16) & 255) / 255, (c >>> 24) / 255];
const hex = (h) => { const n = parseInt(h.slice(1, 7), 16); return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255]; };
export const packRGB = (r, g, b, a) => ((Math.round(a * 255) << 24) | (Math.round(b * 255) << 16) | (Math.round(g * 255) << 8) | Math.round(r * 255)) >>> 0;
/** A colour given as "#rrggbb" or a packed number, keyed, as [r, g, b] from 0 to 1. */
const colourOf = (c) => { const p = typeof c === "number" ? c : packRGB(...hex(c), 1); const k = (colourKey.color || same)(p); return unpack(k).slice(0, 3); };
const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
const smooth = (a, b, x) => { const t = clamp01((x - a) / (b - a)); return t * t * (3 - 2 * t); };
const lerp = (a, b, t) => a + (b - a) * t;

// ---------------------------------------------------------------- noise: the grain of the paint
const NS = 128, NOISE = new Float32Array(NS * NS);
{
  let s = 20261008;
  const rnd = () => ((s = (Math.imul(s, 1103515245) + 12345) >>> 0) / 4294967296);
  for (let i = 0; i < NS * NS; i++) NOISE[i] = rnd() * 2 - 1;
}
/** Smooth value noise, about -1 to 1, one cell per unit, repeating every 128. */
export function noise(x, y) {
  const xi = Math.floor(x), yi = Math.floor(y), fx = x - xi, fy = y - yi;
  const x0 = xi & 127, y0 = yi & 127, x1 = (x0 + 1) & 127, y1 = (y0 + 1) & 127;
  const sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
  const a = NOISE[y0 * NS + x0], b = NOISE[y0 * NS + x1], c = NOISE[y1 * NS + x0], d = NOISE[y1 * NS + x1];
  return a + (b - a) * sx + (c - a) * sy + (a - b - c + d) * sx * sy;
}

// The light: from the upper left and toward us (as pix.js), and the half-way vector to the eye, for sheen.
const LX = -0.50, LY = -0.66, LZ = 0.56;
const HN = Math.hypot(LX, LY, LZ + 1), HX = LX / HN, HY = LY / HN, HZ = (LZ + 1) / HN;

// Part numbers, as the rig gives them (rig.js): the face goes on the head, hair is painted in locks.
const P_HEAD = 1, P_HAIR = 2, P_TORSO = 3, P_SKIRT = 19, P_NOSE = 21, P_EAR = 22, P_PELVIS = 4;
const SMOOTHED = new Set([P_HEAD, P_NOSE, P_TORSO, P_SKIRT, P_PELVIS, P_HAIR]);   // forms built of several shapes, shaded as one
const groupOf = (q) => (q === P_NOSE ? P_HEAD : q);                             // (the nose is shaded with the face it grows from)
const SMOOTH_GROUP = new Uint8Array(256);
for (const q of SMOOTHED) SMOOTH_GROUP[q] = groupOf(q);

// ---------------------------------------------------------------- work buffers, used again from one picture to the next
let POOL = null;
function buffers(n) {
  if (!POOL || POOL.n < n) {
    const N = Math.max(n, POOL ? Math.ceil(POOL.n * 1.25) : 0);
    POOL = {
      n: N, z: new Float32Array(N), m: new Uint8Array(N), t: new Uint8Array(N), p: new Uint8Array(N),
      nx: new Float32Array(N), ny: new Float32Array(N), nz: new Float32Array(N), su: new Float32Array(N), sv: new Float32Array(N), sh: new Uint16Array(N),
      ca: new Float32Array(N), fz: new Float32Array(N), fm: new Uint8Array(N), fp: new Uint8Array(N), fa: new Float32Array(N),
      fx: new Float32Array(N), fy: new Float32Array(N),
      a: new Float32Array(N), b: new Float32Array(N), c: new Float32Array(N), d: new Float32Array(N), e: new Float32Array(N), f: new Float32Array(N),
      g: new Float32Array(N), cr: new Float32Array(N), R: new Float32Array(N), G: new Float32Array(N), Bl: new Float32Array(N), Al: new Float32Array(N),
      g8: new Uint8Array(N),
    };
  }
  return POOL;
}

export class PaintSurface {
  /** w, h: the size in painted pixels; ox, oy: the anchor; o.k: painted pixels to a picture pixel of the stage. */
  constructor(w, h, ox, oy, o = {}) {
    this.w = w; this.h = h; this.ox = ox; this.oy = oy;
    this.k = o.k || 1;
    const n = w * h, B = buffers(n);
    const sub = (arr) => arr.subarray(0, n);
    this.z = sub(B.z).fill(-1e9); this.m = sub(B.m).fill(0); this.t = sub(B.t).fill(0); this.p = sub(B.p).fill(0);
    this.nx = sub(B.nx); this.ny = sub(B.ny); this.nz = sub(B.nz); this.su = sub(B.su); this.sv = sub(B.sv); this.sh = sub(B.sh);
    this.ca = sub(B.ca).fill(0);                                   // how much of the pixel the figure covers, whatever is in front
    this.fz = sub(B.fz).fill(-1e9); this.fm = sub(B.fm).fill(0); this.fp = sub(B.fp); this.fa = sub(B.fa);   // the fringe: a shape covering part of a pixel, in front
    this.fx = sub(B.fx); this.fy = sub(B.fy);
    this.B = B;
    this.mats = []; this.stamps = []; this.marks = []; this.lines = []; this.grounds = [];
    this.shapes = 0;
    this.out = null;
    this.bx0 = w; this.by0 = h; this.bx1 = -1; this.by1 = -1;      // the box anything has been drawn in
    this.head = null;                                             // the face: set by the rig (paintFace)
    this.hairMats = new Set();                                    // materials that are hair, wherever they are
    this.headShapes = new Set();                                  // the shapes that are the skull and the hair over it
  }

  mat(material) {
    let i = this.mats.indexOf(material);
    if (i < 0) { this.mats.push(material); i = this.mats.length - 1; }
    return i + 1;
  }

  /** As pix.js: a rounded, tapered tube from a to b. The pixels it covers only partly are kept apart, for the painted edge. */
  limb(ax, ay, az, bx, by, bz, ra, rb, material, o = {}) {
    const x0 = Math.max(0, Math.floor(Math.min(ax - ra, bx - rb) - 1)), x1 = Math.min(this.w - 1, Math.ceil(Math.max(ax + ra, bx + rb) + 1));
    const y0 = Math.max(0, Math.floor(Math.min(ay - ra, by - rb) - 1)), y1 = Math.min(this.h - 1, Math.ceil(Math.max(ay + ra, by + rb) + 1));
    if (x0 > x1 || y0 > y1) return;
    if (x0 < this.bx0) this.bx0 = x0; if (x1 > this.bx1) this.bx1 = x1; if (y0 < this.by0) this.by0 = y0; if (y1 > this.by1) this.by1 = y1;
    const abx = bx - ax, aby = by - ay, len2 = abx * abx + aby * aby, len = Math.sqrt(len2), il = len > 1e-6 ? 1 / len : 0;
    const mi = this.mat(material), part = o.part || 0, fn = o.fn, flat = o.flatten || 1, bias = o.bias || 0, deep = o.depth || 1, square = o.squareEnd, squareA = o.squareStart, over = o.over, fixed = o.tone;
    const sid = ++this.shapes & 65535, k = this.k, keep = o.keepNormal === true ? 1 : o.keepNormal || 0;     // keepNormal: lying on the body, it takes the body's own shading (as much as that)
    const W = this.w, Z = this.z, M = this.m, P = this.p, T = this.t, NX = this.nx, NY = this.ny, NZ = this.nz, SU = this.su, SV = this.sv, SH = this.sh, CA = this.ca;
    const FZ = this.fz, FM = this.fm, FP = this.fp, FA = this.fa, FX = this.fx, FY = this.fy;
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) {
        const px = x + 0.5, py = y + 0.5;
        let t = len2 > 1e-6 ? ((px - ax) * abx + (py - ay) * aby) / len2 : 0;
        let ct = 1;
        if (square && t > 1 - 0.75 * il) { ct = 0.5 - (t - 1) * len; if (ct <= 0.02) continue; }      // a flat end, its edge anti-aliased
        if (squareA && t < 0.75 * il) { const c2 = 0.5 + t * len; if (c2 <= 0.02) continue; if (c2 < ct) ct = c2; }
        const tc = t < 0 ? (squareA ? t : 0) : t > 1 ? (square ? t : 1) : t;
        const tr = tc < 0 ? 0 : tc > 1 ? 1 : tc;
        const r = ra + (rb - ra) * tr;
        const dx = px - (ax + abx * tc), dy = py - (ay + aby * tc), d2 = dx * dx + dy * dy;
        const rr = r + 0.5;
        if (d2 >= rr * rr) continue;
        const d = Math.sqrt(d2);
        let cov = r - d + 0.5; if (cov > 1) cov = 1;
        if (ct < cov) cov = ct;
        if (cov <= 0.02) continue;
        const up = d < r ? Math.sqrt(r * r - d2) : 0;
        let z = az + (bz - az) * tr + up * deep + bias;
        const i = y * W + x;
        let use = material, mm = mi;
        if (fn) {
          const alt = fn(tr, dx / r, dy / r, x, y);
          if (alt === null) continue;
          if (alt) { use = alt; mm = this.mat(alt); }
        }
        if (use.soft) continue;
        const ir = 1 / r, nx = dx * ir, ny = dy * ir, nz = up * ir * flat, inv = 1 / (Math.sqrt(nx * nx + ny * ny + nz * nz) || 1);
        if (cov >= 0.5) {
          if (z <= Z[i]) {
            const slack = over && over[P[i]];
            if (!slack || z + slack <= Z[i]) { if (cov > CA[i]) CA[i] = cov; continue; }
            z = Z[i] + 0.02;
          }
          if (cov > CA[i]) CA[i] = cov;
          const under = keep && M[i] && Z[i] > -1e8;
          Z[i] = z; M[i] = mm; P[i] = part; T[i] = fixed != null ? fixed + 1 : 0;
          if (under) { NX[i] = lerp(nx * inv, NX[i], keep); NY[i] = lerp(ny * inv, NY[i], keep); NZ[i] = lerp(nz * inv, NZ[i], keep); }
          else { NX[i] = nx * inv; NY[i] = ny * inv; NZ[i] = nz * inv; }
          SU[i] = (-dx * aby + dy * abx) * il / k; SV[i] = t * len / k; SH[i] = sid;
        } else {
          if (cov > CA[i]) CA[i] = cov;
          if (z > FZ[i] && z > Z[i]) { FZ[i] = z; FM[i] = mm; FP[i] = part; FA[i] = cov; FX[i] = nx * inv; FY[i] = ny * inv; }
        }
      }
    }
  }

  /** As pix.js: a ball or an egg; rz is how far it bulges toward the viewer. */
  ball(cx, cy, cz, rx, ry, rz, material, o = {}) {
    const x0 = Math.max(0, Math.floor(cx - rx - 1)), x1 = Math.min(this.w - 1, Math.ceil(cx + rx + 1));
    const y0 = Math.max(0, Math.floor(cy - ry - 1)), y1 = Math.min(this.h - 1, Math.ceil(cy + ry + 1));
    if (x0 > x1 || y0 > y1) return;
    if (x0 < this.bx0) this.bx0 = x0; if (x1 > this.bx1) this.bx1 = x1; if (y0 < this.by0) this.by0 = y0; if (y1 > this.by1) this.by1 = y1;
    const mi = this.mat(material), part = o.part || 0, fn = o.fn, bias = o.bias || 0, flat = o.flatten || 1, fixed = o.tone;
    const sid = ++this.shapes & 65535, k = this.k, irx = 1 / rx, iry = 1 / ry, keep = o.keepNormal === true ? 1 : o.keepNormal || 0;
    if (o.headShape) this.headShapes.add(sid);
    const W = this.w, Z = this.z, M = this.m, P = this.p, T = this.t, NX = this.nx, NY = this.ny, NZ = this.nz, SU = this.su, SV = this.sv, SH = this.sh, CA = this.ca;
    const FZ = this.fz, FM = this.fm, FP = this.fp, FA = this.fa, FX = this.fx, FY = this.fy;
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) {
        const ux = (x + 0.5 - cx) * irx, uy = (y + 0.5 - cy) * iry, q = ux * ux + uy * uy;
        if (q > 1.6) continue;
        const g = 2 * Math.sqrt(ux * ux * irx * irx + uy * uy * iry * iry);
        let cov = g > 1e-6 ? (1 - q) / g + 0.5 : 1;
        if (cov > 1) cov = 1;
        if (cov <= 0.02) continue;
        const uz = q < 1 ? Math.sqrt(1 - q) : 0;
        const z = cz + uz * rz + bias;
        const i = y * W + x;
        let use = material, mm = mi;
        if (fn) {
          const alt = fn(ux, uy, uz, x, y);
          if (alt === null) continue;
          if (alt) { use = alt; mm = this.mat(alt); }
        }
        if (use.soft) continue;
        const nx = ux * irx, ny = uy * iry, nz = (uz / rz) * flat, inv = 1 / (Math.sqrt(nx * nx + ny * ny + nz * nz) || 1);
        if (cov >= 0.5) {
          if (cov > CA[i]) CA[i] = cov;
          if (z <= Z[i]) continue;
          const under = keep && M[i] && Z[i] > -1e8;
          Z[i] = z; M[i] = mm; P[i] = part; T[i] = fixed != null ? fixed + 1 : 0;
          if (under) { NX[i] = lerp(nx * inv, NX[i], keep); NY[i] = lerp(ny * inv, NY[i], keep); NZ[i] = lerp(nz * inv, NZ[i], keep); }
          else { NX[i] = nx * inv; NY[i] = ny * inv; NZ[i] = nz * inv; }
          SU[i] = ux * rx / k; SV[i] = uy * ry / k; SH[i] = sid;
        } else {
          if (cov > CA[i]) CA[i] = cov;
          if (z > FZ[i] && z > Z[i]) { FZ[i] = z; FM[i] = mm; FP[i] = part; FA[i] = cov; FX[i] = nx * inv; FY[i] = ny * inv; }
        }
      }
    }
  }

  /** A flat panel in one tone (not used for people; here so that anything drawn for pix.js can be drawn here). */
  poly(points, z, material, tone = 1, o = {}) {
    let y0 = Infinity, y1 = -Infinity;
    for (const p of points) { if (p[1] < y0) y0 = p[1]; if (p[1] > y1) y1 = p[1]; }
    y0 = Math.max(0, Math.floor(y0)); y1 = Math.min(this.h - 1, Math.ceil(y1));
    const mi = this.mat(material), part = o.part || 0;
    for (let y = y0; y <= y1; y++) {
      const py = y + 0.5, xs = [];
      for (let i = 0, j = points.length - 1; i < points.length; j = i++) {
        const xi = points[i][0], yi = points[i][1], xj = points[j][0], yj = points[j][1];
        if ((yi > py) !== (yj > py)) xs.push(xi + ((py - yi) / (yj - yi)) * (xj - xi));
      }
      xs.sort((a, b) => a - b);
      for (let k = 0; k + 1 < xs.length; k += 2) {
        const xa = Math.max(0, Math.round(xs[k])), xb = Math.min(this.w, Math.round(xs[k + 1]));
        for (let x = xa; x < xb; x++) {
          const i = y * this.w + x;
          if (z < this.z[i] || material.soft) continue;
          this.z[i] = z; this.m[i] = mi; this.t[i] = tone + 1; this.p[i] = part; this.ca[i] = 1;
          if (x < this.bx0) this.bx0 = x; if (x > this.bx1) this.bx1 = x; if (y < this.by0) this.by0 = y; if (y > this.by1) this.by1 = y;
          this.nx[i] = 0; this.ny[i] = 0; this.nz[i] = 1; this.su[i] = x / this.k; this.sv[i] = y / this.k; this.sh[i] = 0;
        }
      }
    }
  }
  rect(x, y, w, h, z, material, tone = 1, o) { this.poly([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], z, material, tone, o); }

  /** A shadow on the ground: painted soft, under everything. */
  oval(cx, cy, rx, ry, z, material) { this.grounds.push([cx, cy, rx, ry, material]); }

  /** A spot of colour (a button, a star), about a picture pixel across, where `part` is on top. */
  dot(x, y, color, part = null) { this.stamps.push([x, y, color, part]); }

  /** A fold or a crease drawn on cloth or skin: a soft darker line, where `part` is on top. */
  stroke(ax, ay, bx, by_, by = 1, part = null) { this.lines.push([ax, ay, bx, by_, by, part]); }

  /** A small soft mark, darker (or with a negative `by`, lighter). */
  mark(x, y, by = 1, part = null) { this.marks.push([x, y, by, part]); }

  /** Remove everything below a row. */
  clipBelow(row) {
    for (let y = Math.max(0, Math.ceil(row)); y < this.h; y++) for (let x = 0; x < this.w; x++) { const i = y * this.w + x; this.m[i] = 0; this.z[i] = -1e9; this.ca[i] = 0; this.fz[i] = -1e9; }
    return this;
  }

  /** The highest and lowest rows with anything on them (as pix.js). */
  bounds() {
    const { w, h, m } = this;
    let top = h, bottom = -1, left = w, right = -1;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      if (!m[y * w + x]) continue;
      if (y < top) top = y; if (y > bottom) bottom = y; if (x < left) left = x; if (x > right) right = x;
    }
    return { top, bottom, left, right };
  }

  toCanvas() {
    if (!this.out) this.finish();
    const canvas = document.createElement("canvas");
    canvas.width = this.w; canvas.height = this.h;
    canvas.getContext("2d").putImageData(new ImageData(new Uint8ClampedArray(this.out.buffer, this.out.byteOffset, this.out.byteLength), this.w, this.h), 0, 0);
    return canvas;
  }

  /** Turn the shapes into a painting. The options are pix.js's, read the painter's way: `cast` says which parts throw a
      shadow on which (softly here), `seams` which touching parts show a line between them (a soft contact shadow here),
      `rim` and `outline` ask for the painted edge. */
  finish(opts = {}) {
    paintFinish(this, opts);
    // what callers may still read (bounds()): the rest of the work buffers are used again for the next picture
    this.m = this.m.slice(); this.p = this.p.slice();
    this.z = this.t = this.nx = this.ny = this.nz = this.su = this.sv = this.sh = this.ca = this.fz = this.fm = this.fp = this.fa = this.fx = this.fy = this.B = null;
    return this;
  }
}

// ---------------------------------------------------------------- painting
const toneCache = new WeakMap();
/** A material's four tones, keyed, as 12 numbers (r, g, b of light, base, shade, deep). */
function tonesOf(material) {
  const key = colourKey.tones;
  let hit = key ? null : toneCache.get(material);
  if (hit) return hit;
  const t = key ? key(material) : material.tones;
  hit = new Float32Array(12);
  for (let j = 0; j < 4; j++) { const c = unpack(t[j]); hit[j * 3] = c[0]; hit[j * 3 + 1] = c[1]; hit[j * 3 + 2] = c[2]; }
  if (!key) toneCache.set(material, hit);
  return hit;
}

/** Blur `src` into `dst` within the box [x0, x1] x [y0, y1], radius r: horizontally (into tmp), then vertically. */
function boxBlur(src, dst, tmp, w, x0, y0, x1, y1, r) {
  if (r < 1) { for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) dst[y * w + x] = src[y * w + x]; return; }
  const n = 2 * r + 1;
  for (let y = y0; y <= y1; y++) {
    const row = y * w;
    let s = 0;
    for (let x = x0; x <= Math.min(x1, x0 + r); x++) s += src[row + x];
    for (let x = x0; x <= x1; x++) {
      tmp[row + x] = s / n;
      const out = x - r, inn = x + r + 1;
      if (out >= x0) s -= src[row + out];
      if (inn <= x1) s += src[row + inn];
    }
  }
  for (let x = x0; x <= x1; x++) {
    let s = 0;
    for (let y = y0; y <= Math.min(y1, y0 + r); y++) s += tmp[y * w + x];
    for (let y = y0; y <= y1; y++) {
      dst[y * w + x] = s / n;
      const out = y - r, inn = y + r + 1;
      if (out >= y0) s -= tmp[out * w + x];
      if (inn <= y1) s += tmp[inn * w + x];
    }
  }
}

/** One pass of smoothing the normals of forms built of several shapes (grp: the part each pixel is smoothed with, or 0),
    along x (step 1) or y (step w), from (ax, ay, az) into (bx, by, bz). */
function smoothPass(ax, ay, az, bx, by, bz, grp, z, w, x0, y0, x1, y1, vertical, rHead, rBody, zt) {
  for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
    const i = y * w + x, g = grp[i];
    if (!g) { bx[i] = ax[i]; by[i] = ay[i]; bz[i] = az[i]; continue; }
    const r = g === P_HEAD || g === P_HAIR ? rHead : rBody, zi = z[i];
    let sx = ax[i], sy = ay[i], sz = az[i], c = 1;
    const lo = vertical ? Math.max(y0, y - r) : Math.max(x0, x - r), hi = vertical ? Math.min(y1, y + r) : Math.min(x1, x + r);
    for (let j = lo; j <= hi; j++) {
      const q = vertical ? j * w + x : y * w + j;
      if (q === i || grp[q] !== g) continue;
      const dz = z[q] - zi;
      if (dz > zt || dz < -zt) continue;
      sx += ax[q]; sy += ay[q]; sz += az[q]; c++;
    }
    bx[i] = sx / c; by[i] = sy / c; bz[i] = sz / c;
  }
}

// What the shading of one pixel comes to (set by shade(), read at once: no arrays made for every pixel).
let SR = 0, SG = 0, SB = 0, SS = 0;

function paintFinish(sf, { contact = true, gap = 1.6, seams = null, cast = null, reach = 12 } = {}) {
  const { w, h, m, p, z, t: T, nx: NX, ny: NY, nz: NZ, su: SU, sv: SV, sh: SH, ca: CA, fz: FZ, fm: FM, fp: FP, fa: FA, fx: FX, fy: FY, mats, k, B } = sf;
  const n = w * h;
  const out = new Uint32Array(n);
  sf.out = out;
  // the box everything lies in (shapes and fringes, as they were drawn; the shadows on the ground)
  let bx0 = sf.bx0, bx1 = sf.bx1, by0 = sf.by0, by1 = sf.by1;
  for (const [cx, cy, rx, ry] of sf.grounds) {
    bx0 = Math.max(0, Math.min(bx0, Math.floor(cx - rx * 1.3 - 1))); bx1 = Math.min(w - 1, Math.max(bx1, Math.ceil(cx + rx * 1.3 + 1)));
    by0 = Math.max(0, Math.min(by0, Math.floor(cy - ry * 1.6 - 1))); by1 = Math.min(h - 1, Math.max(by1, Math.ceil(cy + ry * 1.6 + 1)));
  }
  if (bx1 < bx0 || by1 < by0) return;
  const nm = mats.length;
  const tones = mats.map(tonesOf), hairMat = new Uint8Array(nm + 1);
  for (let j = 0; j < nm; j++) hairMat[j] = sf.hairMats.has(mats[j]) || mats[j].hair ? 1 : 0;
  const shine = mats.map((mt) => (mt.shine ? 1 : 0)), lift = mats.map((mt) => (mt.lift ? mt.lift * 0.17 : 0)), cuts = mats.map((mt) => mt.cut ?? 0.20);
  const S = sf.size || h / 1.25;                                   // the figure's height in painted pixels (the rig says)
  const A = B.a, Bb = B.b, Cc = B.c, D = B.d, E = B.e, F = B.f, G8 = B.g8;

  // ---- 1. forms built of several shapes are shaded as one: their normals are smoothed, within each part ----
  for (let y = by0; y <= by1; y++) for (let x = bx0; x <= bx1; x++) { const i = y * w + x; G8[i] = m[i] ? SMOOTH_GROUP[p[i]] : 0; }
  const rs = Math.max(1, Math.round(S * 0.016)), zt = 3 * k + S * 0.03;
  smoothPass(NX, NY, NZ, A, Bb, Cc, G8, z, w, bx0, by0, bx1, by1, false, rs, rs, zt);
  smoothPass(A, Bb, Cc, D, E, F, G8, z, w, bx0, by0, bx1, by1, true, rs, rs, zt);
  const SX = D, SY = E, SZ = F;                                     // the smoothed normals (not yet of unit length)

  // ---- 2. shadows one part throws on another, followed back toward the light; then softened ----
  const shadow = A;
  for (let y = by0; y <= by1; y++) shadow.fill(0, y * w + bx0, y * w + bx1 + 1);
  if (cast) {
    const steps = Math.max(1, Math.min(14, Math.ceil(reach / k))), tab = new Int16Array(64 * 64).fill(-1);
    const sx = new Int32Array(steps + 1), sy = new Int32Array(steps + 1);
    for (let j = 1; j <= steps; j++) { sx[j] = Math.round(j * k * 0.6); sy[j] = Math.round(j * k * 0.8); }
    for (let y = by0; y <= by1; y++) for (let x = bx0; x <= bx1; x++) {
      const i = y * w + x;
      if (!m[i]) continue;
      const pi = p[i], zi = z[i];
      for (let j = 1; j <= steps; j++) {
        const qx = x - sx[j], qy = y - sy[j];
        if (qx < 0 || qy < 0) break;
        const q = qy * w + qx;
        if (!m[q] || p[q] === pi || z[q] - zi < (j * 0.68 + 1.4) * k) continue;
        const key = (p[q] & 63) * 64 + (pi & 63);
        let reachQ = tab[key];
        if (reachQ < 0) { reachQ = cast(p[q], pi) || 0; tab[key] = reachQ; }
        if (j * k <= reachQ) { shadow[i] = (p[q] === P_HAIR && (pi === P_HEAD || pi === P_EAR) ? 0.40 : 1) * (1 - 0.35 * ((j * k) / Math.max(1, reachQ))); break; }
      }
    }
  }
  // ---- 3. where one part lies just in front of another, or two parts touch (a seam): a soft line on the farther one ----
  const touch = Bb;
  for (let y = by0; y <= by1; y++) touch.fill(0, y * w + bx0, y * w + bx1 + 1);
  if (contact) for (let y = Math.max(1, by0); y <= by1; y++) for (let x = Math.max(1, bx0); x <= bx1; x++) {
    const i = y * w + x;
    if (!m[i]) continue;
    const pi = p[i], L = i - 1, U = i - w;
    const lHit = m[L] && p[L] !== pi && (z[L] - z[i] > gap * k || (seams && seams(p[L], pi, false, x, y)));
    const uHit = !lHit && m[U] && p[U] !== pi && (z[U] - z[i] > gap * k || (seams && seams(p[U], pi, true, x, y)));
    if (lHit || uHit) touch[i] = (p[U] === P_HAIR || p[L] === P_HAIR) && pi === P_HEAD ? 0.35 : 1;
  }
  boxBlur(shadow, shadow, Cc, w, bx0, by0, bx1, by1, Math.max(1, Math.round(k * 0.6)));
  boxBlur(touch, touch, Cc, w, bx0, by0, bx1, by1, Math.max(1, Math.round(k * 0.5)));
  // ---- 4. the painter's edge: how near the outline each pixel is ----
  const edge = Cc;
  for (let y = by0; y <= by1; y++) for (let x = bx0; x <= bx1; x++) { const i = y * w + x; edge[i] = CA[i]; }
  boxBlur(edge, edge, B.g, w, bx0, by0, bx1, by1, Math.max(1, Math.round(k * 0.9)));
  // ---- 5. folds and creases: soft lines, on the part they belong to ----
  const crease = B.cr;
  for (let y = by0; y <= by1; y++) crease.fill(0, y * w + bx0, y * w + bx1 + 1);
  const lineW = 0.55 * k;
  for (const [ax, ay, bx, by_, by, part] of sf.lines) {
    const x0 = Math.max(bx0, Math.floor(Math.min(ax, bx) - 2 * k)), x1 = Math.min(bx1, Math.ceil(Math.max(ax, bx) + 2 * k));
    const y0 = Math.max(by0, Math.floor(Math.min(ay, by_) - 2 * k)), y1 = Math.min(by1, Math.ceil(Math.max(ay, by_) + 2 * k));
    const dx = bx - ax, dy = by_ - ay, l2 = dx * dx + dy * dy || 1;
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
      const i = y * w + x;
      if (!m[i] || (part !== null && p[i] !== part)) continue;
      const tt = clamp01(((x + 0.5 - ax) * dx + (y + 0.5 - ay) * dy) / l2), ex = x + 0.5 - (ax + dx * tt), ey = y + 0.5 - (ay + dy * tt);
      const c = clamp01(lineW + 0.5 - Math.sqrt(ex * ex + ey * ey));
      if (c > 0 && c * 0.55 * by > crease[i]) crease[i] = c * 0.55 * by;
    }
  }
  for (const [x, y, by, part] of sf.marks) {
    const r = 0.7 * k;
    for (let yy = Math.max(0, Math.floor(y + 0.5 - r - 1)); yy <= Math.min(h - 1, Math.ceil(y + 0.5 + r + 1)); yy++) for (let xx = Math.max(0, Math.floor(x + 0.5 - r - 1)); xx <= Math.min(w - 1, Math.ceil(x + 0.5 + r + 1)); xx++) {
      const i = yy * w + xx;
      if (!m[i] || (part !== null && p[i] !== part)) continue;
      const c = clamp01(r + 0.5 - Math.hypot(xx - x, yy - y));
      if (c > 0 && c * 0.5 * by > crease[i]) crease[i] = c * 0.5 * by;
    }
  }

  // ---- 6. each pixel, painted ----
  const face = sf.head ? faceRenderer(sf) : null, headShapes = sf.headShapes;
  /** The colour of a form at a pixel: its material's tones blended by how it turns to the light (into SR, SG, SB; SS how much in shade). */
  const shade = (mi, part, nx, ny, nz, fixed, extra, i, isFringe) => {
    const tn = tones[mi], hair = hairMat[mi] === 1 || part === P_HAIR;
    const d = nx * LX + ny * LY + nz * LZ + lift[mi];
    const cut = part === P_HEAD || part === P_NOSE || part === P_EAR ? -0.10 : cuts[mi];
    const s = smooth(cut + 0.24, cut - 0.22, d);                                  // 0 in the light, 1 in the shade, with a soft terminator between
    const hi = smooth(0.58, 0.98, d) * (shine[mi] ? 0.95 : hair ? 0.25 : 0.32);
    let tau = (1 - hi) + (2 + 0.30 * smooth(cut - 0.05, cut - 0.80, d) - (1 - hi)) * s;
    tau -= 0.38 * s * clamp01(ny * 1.4) * (1 - Math.abs(nz) * 0.6);             // light thrown back up from the ground into the shade
    if (fixed === 3 && tau < 1.85) tau = 1.85;
    tau += extra;
    if (tau < 0) tau = 0; else if (tau > 3) tau = 3;
    const j = tau >= 3 ? 2 : tau | 0, f = tau - j, o = j * 3;
    let r = tn[o] + (tn[o + 3] - tn[o]) * f, g = tn[o + 1] + (tn[o + 4] - tn[o + 1]) * f, b = tn[o + 2] + (tn[o + 5] - tn[o + 2]) * f;
    // warm light, cooler shade
    const warm = 1 - s;
    r *= 1 + 0.035 * warm - 0.03 * s; g *= 1 + 0.008 * warm - 0.012 * s; b *= 1 - 0.035 * warm + 0.045 * s;
    if (!isFringe) {
      // The paint's surface, as the painted backgrounds have it (measured on them): a grain of one picture pixel, each a
      // little lighter or darker and warmer or cooler than the next (about 3.5% in lightness), over a soft mottle, with
      // short strokes along the form. It is fixed to the form (each shape's own across-and-along, in picture pixels),
      // so that it moves with the body and never swims.
      const u = SU[i], v = SV[i], sh = SH[i], sid = sh * 7.31;
      let hh = (Math.floor(u) * 374761393 + Math.floor(v) * 668265263 + sh * 1274126177) | 0;
      hh = Math.imul(hh ^ (hh >>> 13), 1274126177); hh ^= hh >>> 16;
      const cell = ((hh >>> 0) & 65535) / 65535 - 0.5, tint = (((hh >>> 16) & 255) / 255 - 0.5);
      let g1 = cell * 2 + noise(u * 0.26 + sid, v * 0.26 - sid) * 1.0;
      let st = noise(u * 2.2 + sid * 0.7, v * 0.35 + sid);
      r *= 1 + tint * 0.022; b *= 1 - tint * 0.022;
      if (hair) {
        // locks: dark partings between them, strands along them, and a broken sheen where they catch the light. On the
        // head the strands run from the crown down round it; on a lock, a plait or a beard, along it.
        let lu, lv;
        if (face && headShapes.has(SH[i])) {
          const q = face.local(i % w, (i / w) | 0, i), len = Math.hypot(q[0], q[1], q[2]) || 1;
          lu = Math.atan2(q[0], q[2]) * 5.5; lv = Math.acos(clamp01((q[1] / len + 1) / 2) * 2 - 1) * 1.6;
        } else { lu = u * 0.55; lv = v * 0.07; }
        const lock = noise(lu + sid * 0.1, lv) * 0.65 + noise(lu * 3.1 - sid, lv * 2.4) * 0.35;
        const hd = nx * HX + ny * HY + nz * HZ, sheen = Math.pow(clamp01(hd), 5) * smooth(-0.25, 0.55, lock);
        const kk = 1 + 0.26 * lock;
        r = r * kk + (tn[0] - r) * sheen * 0.70; g = g * kk + (tn[1] - g) * sheen * 0.70; b = b * kk + (tn[2] - b) * sheen * 0.70;
        g1 *= 0.4; st *= 0.5;
      }
      const gr = 1 + (part === P_HEAD || part === P_NOSE ? 0.018 : 0.030) * g1 + 0.030 * st;
      r *= gr; g *= gr; b *= gr;
    }
    SR = r; SG = g; SB = b; SS = s;
  };

  const R = B.R, G = B.G, Bl = B.Bl, Al = B.Al;
  for (let y = by0; y <= by1; y++) Al.fill(0, y * w + bx0, y * w + bx1 + 1);
  for (let y = by0; y <= by1; y++) for (let x = bx0; x <= bx1; x++) {
    const i = y * w + x;
    if (!m[i]) continue;
    const mi = m[i] - 1, part = p[i];
    let nx = SX[i], ny = SY[i], nz = SZ[i];
    const inv = 1 / (Math.sqrt(nx * nx + ny * ny + nz * nz) || 1); nx *= inv; ny *= inv; nz *= inv;
    const near = 1 - edge[i];                                                    // near the outline: the painter's edge
    let ne = near * 1.6; if (ne > 1) ne = 1;
    const extra = 0.70 * shadow[i] + 0.55 * touch[i] + crease[i] + 0.55 * ne * (nx * 0.6 + ny * 0.8 > 0 ? 1 : 0.77);
    shade(mi, part, nx, ny, nz, T[i], extra, i, false);
    if (face && (part === P_HEAD || part === P_NOSE || (part === P_HAIR && face.beard))) {
      const f = face(x, y, i, part, SR, SG, SB, SS, mi);
      R[i] = f[0]; G[i] = f[1]; Bl[i] = f[2];
    } else { R[i] = SR; G[i] = SG; Bl[i] = SB; }
    Al[i] = 1;
  }
  // a hard change of material inside one part (a hairline, a print, a band of colour) is softened, as a brush would;
  // and so is the edge of the hair where it lies on the skin, which is cut by the hairline, not by its own shape
  const passes = k >= 1.75 ? [2, 0.26, 1, 0.42] : [1, 0.42];
  for (let pp = 0; pp < passes.length; pp += 2) {
    const step = passes[pp], by = passes[pp + 1];
    for (let y = by0; y + step <= by1; y++) for (let x = bx0; x + step <= bx1; x++) {
      const i = y * w + x;
      if (!m[i]) continue;
      const hi = hairMat[m[i] - 1] === 1 || p[i] === P_HAIR;
      for (let side = 0; side < 2; side++) {
        const q = side ? i + w * step : i + step;
        if (!m[q] || m[q] === m[i]) continue;
        const hq = hairMat[m[q] - 1] === 1 || p[q] === P_HAIR, hairEdge = hi !== hq;
        if (p[q] !== p[i]) { if (!hairEdge || (p[i] !== P_HEAD && p[q] !== P_HEAD)) continue; const dz = z[i] - z[q]; if (dz > 6 * k || dz < -6 * k) continue; }
        else if (step > 1 && !hairEdge) continue;
        const r = (R[i] + R[q]) / 2, g = (G[i] + G[q]) / 2, b = (Bl[i] + Bl[q]) / 2;
        R[i] += (r - R[i]) * by; G[i] += (g - G[i]) * by; Bl[i] += (b - Bl[i]) * by;
        R[q] += (r - R[q]) * by; G[q] += (g - G[q]) * by; Bl[q] += (b - Bl[q]) * by;
      }
    }
  }
  // spots of colour: buttons, a star on a bib, a patch
  for (const [x, y, color, part] of sf.stamps) {
    const col = colourOf(color), r0 = 0.62 * k;
    for (let yy = Math.max(0, Math.floor(y + 0.5 - r0 - 1)); yy <= Math.min(h - 1, Math.ceil(y + 0.5 + r0 + 1)); yy++) for (let xx = Math.max(0, Math.floor(x + 0.5 - r0 - 1)); xx <= Math.min(w - 1, Math.ceil(x + 0.5 + r0 + 1)); xx++) {
      const i = yy * w + xx;
      if (!m[i] || (part !== null && p[i] !== part)) continue;
      const c = clamp01(r0 + 0.5 - Math.hypot(xx - x, yy - y));
      if (c <= 0) continue;
      R[i] += (col[0] - R[i]) * c; G[i] += (col[1] - G[i]) * c; Bl[i] += (col[2] - Bl[i]) * c;
    }
  }
  // the edge: the part of a pixel a shape covers only partly, over whatever is behind it
  for (let y = by0; y <= by1; y++) for (let x = bx0; x <= bx1; x++) {
    const i = y * w + x;
    const solid = m[i] !== 0, fr = FM[i] !== 0 && FZ[i] > z[i];
    if (!solid && !fr) continue;
    let a = solid ? (CA[i] < 0.5 ? 0.5 : CA[i] > 0.999 ? 1 : CA[i]) : 0;
    if (fr) {
      const fa = FA[i];
      shade(FM[i] - 1, FP[i], FX[i], FY[i], 0.15, 0, 0.55, i, true);
      if (solid) { R[i] += (SR - R[i]) * fa; G[i] += (SG - G[i]) * fa; Bl[i] += (SB - Bl[i]) * fa; }
      else { R[i] = SR; G[i] = SG; Bl[i] = SB; a = Math.min(1, Math.max(fa, CA[i] * 0.9)); }
    }
    Al[i] = a;
  }
  // the shadow on the ground, soft, under the figure
  for (const [cx, cy, rx, ry, mt] of sf.grounds) {
    const strength = mt && mt.tones ? Math.min(0.42, ((mt.tones[1] >>> 24) / 255) * 1.35) : 0.32;
    const x0 = Math.max(0, Math.floor(cx - rx * 1.3)), x1 = Math.min(w - 1, Math.ceil(cx + rx * 1.3)), y0 = Math.max(0, Math.floor(cy - ry * 1.6)), y1 = Math.min(h - 1, Math.ceil(cy + ry * 1.6));
    const sc = colourOf("#2a1c14"), irx = 1 / (rx * 1.15), iry = 1 / (ry * 1.35);
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
      const ux = (x + 0.5 - cx) * irx, uy = (y + 0.5 - cy) * iry, q = ux * ux + uy * uy;
      if (q >= 1) continue;
      const i = y * w + x, a0 = Al[i];
      if (a0 >= 0.999) continue;
      const sa = strength * (1 - smooth(0.25, 1, q)), a = a0 + sa * (1 - a0);
      if (a <= 0) continue;
      R[i] = (R[i] * a0 + sc[0] * sa * (1 - a0)) / a; G[i] = (G[i] * a0 + sc[1] * sa * (1 - a0)) / a; Bl[i] = (Bl[i] * a0 + sc[2] * sa * (1 - a0)) / a;
      Al[i] = a;
    }
  }
  for (let y = by0; y <= by1; y++) for (let x = bx0; x <= bx1; x++) {
    const i = y * w + x, a = Al[i];
    if (!(a > 0.004)) continue;
    const r = R[i], g = G[i], b = Bl[i];
    out[i] = ((((a > 1 ? 1 : a) * 255 + 0.5) << 24) | (((b < 0 ? 0 : b > 1 ? 1 : b) * 255 + 0.5) << 16) | (((g < 0 ? 0 : g > 1 ? 1 : g) * 255 + 0.5) << 8) | ((r < 0 ? 0 : r > 1 ? 1 : r) * 255 + 0.5)) >>> 0;
  }
}

// =====================================================================================
// Faces
// =====================================================================================
// A face is painted onto the head where it is: each pixel of the head is taken back to the head's own frame (across,
// up, forward), and the features are worked out there, so a face turns, nods and foreshortens with the head and is
// hidden where the head turns away. Measurements are in half head widths (the skull's x radius) from the middle of the
// face; `y` is up. Everything is anti-aliased from its own shape, and nothing is drawn thinner than a painted pixel or
// so: a small face keeps eyes, brows and a mouth that read, as the pixel art's did, and a big one gets every detail.
//
// Eyes by kind (the rig's own words for them, people.js `face.eyes`):
//   w, h     half width and half height of the opening      iris   the iris's radius, as a fraction of w
//   lid      how far the upper lid comes down over the eye   lash   0 none, 1 a woman's, 2 a little girl's long lashes
//   lower    how dark the lower lash line is                  socket how deep the shadow round the eye is
//   kohl     black paint round the eye and out to the temple; crows: lines at the outer corner; bags: under the eye
const EYES = {
  plain:  { w: 0.205, h: 0.084, iris: 0.48, lid: 0.14, lash: 0, lower: 0.30, socket: 0.18 },
  lash:   { w: 0.215, h: 0.090, iris: 0.48, lid: 0.14, lash: 1, lower: 0.32, socket: 0.15 },
  big:    { w: 0.235, h: 0.115, iris: 0.52, lid: 0.06, lash: 0, lower: 0.26, socket: 0.10 },
  bright: { w: 0.235, h: 0.115, iris: 0.52, lid: 0.05, lash: 0, lower: 0.26, socket: 0.10, glint2: true },
  wide:   { w: 0.220, h: 0.110, iris: 0.42, lid: 0.00, lash: 0, lower: 0.30, socket: 0.12 },
  heavy:  { w: 0.205, h: 0.088, iris: 0.48, lid: 0.46, lash: 0, lower: 0.36, socket: 0.22, bags: 0.35 },
  girl:   { w: 0.222, h: 0.098, iris: 0.50, lid: 0.10, lash: 1, lower: 0.28, socket: 0.12 },
  kohl:   { w: 0.225, h: 0.088, iris: 0.48, lid: 0.14, lash: 0, lower: 0.30, socket: 0.15, kohl: 1 },
  squint: { w: 0.205, h: 0.046, iris: 0.48, lid: 0.25, lash: 0, lower: 0.42, socket: 0.20, crows: 1, thin: 1 },
  deep:   { w: 0.205, h: 0.082, iris: 0.48, lid: 0.26, lash: 0, lower: 0.36, socket: 0.38 },
};

/** Everything about one person's painted face: from their face settings (people.js `face`), and their `paint.face`. */
export function faceOf(spec) {
  const f = { ...(spec.face || {}), ...((spec.paint && spec.paint.shape) || {}) }, pf = (spec.paint && spec.paint.face) || {}, kind = EYES[f.eyes] || EYES.plain;
  const hr = spec.dim.headR, toFace = hr[1] / hr[0];                 // (the rig gives heights in the skull's half height)
  const eye = { ...kind, ...(pf.eye || {}) };
  const hairTone = spec.hair && spec.hair.mat ? spec.hair.mat.tones[2] : 0;
  return {
    eye,
    eyeX: pf.eyeX ?? (f.eyeX ?? 0.36) * 1.05,
    eyeY: (pf.eyeY ?? f.eyeY ?? 0.06) * toFace,
    iris: pf.iris || null,                                             // a colour; with none, a dark brown from `face.eye`
    dark: f.eye || "#2a1a12",
    white: pf.white || f.white || "#f4eee6",
    brow: {
      color: pf.browColor || (f.brows == null ? hairTone : f.brows),
      up: pf.browUp ?? 0.072 + 0.022 * ((f.browUp ?? 2) - 2),
      thick: pf.browThick ?? 0.060 + 0.012 * ((f.browW ?? 3) - 3),
      arch: pf.browArch ?? 0.028,
      tilt: pf.browTilt ?? -0.032 * (f.browTilt || 0),             // + raises the inner ends (worried); - lowers them (stern)
      len: pf.browLen ?? 1.0 + 0.08 * ((f.browW ?? 3) - 3),
      none: f.brows == null && !pf.browColor && !hairTone,
    },
    nose: { len: Array.isArray(f.nose) ? f.nose[0] : 1, tip: Array.isArray(f.nose) ? f.nose[2] : (f.nose ?? 1), w: pf.noseW ?? 1 },
    mouth: {
      y: (pf.mouthY ?? (f.mouthY ?? -0.74) * 0.88) * toFace,
      w: pf.mouthW ?? (f.mouthW ?? 0.22) * 1.20,
      lip: pf.lip || f.lip || "#8a4636",
      lipA: pf.lipA ?? 0.50,
      upper: pf.upper ?? 0.038, lower: pf.lower ?? 0.052,
      smile: pf.smile ?? (f.smile || 0) * 0.6,
      hidden: !!f.beard && !f.mouthShows,                             // a long beard hides a shut mouth
      onBeard: !!f.beard,
    },
    moustache: f.moustache && !f.beard ? f.moustache : null,         // (with no beard it is painted on; with one, the rig draws it over the beard)
    blush: pf.blush ?? 0.08, blushColor: pf.blushColor || "#e0675e",
    eyeshadow: pf.eyeshadow || null,
    freckles: !!f.freckles,
    lines: f.lines || 0,
    gaze: pf.gaze || [0, 0],
    expressive: pf.expressive ?? 1,
    cheer: pf.cheer ?? (f.smile > 0 ? 0.12 : 0),
    stubble: pf.stubble ?? 0,
    beardShadow: f.shadow || null,                                     // an unshaven jaw (people.js face.shadow): painted on
    shades: f.shades || null,
    where: spec.hair && spec.hair.mat && !spec.hair.wig ? spec.hair.where || null : null,
  };
}

/** How the brows move with what the body is doing: [raise both, raise the inner ends, raise the one on the left more]. */
function browsFor(pose) {
  if (pose.blink && pose.squeeze) return [-0.020, -0.040, 0];
  if (pose.praying) return [0.0, 0.014, 0];
  switch (pose.gesture) {
    case 1: return [0.014, 0.0, 0];
    case 2: return [0.018, 0.032, 0];
    case 4: return [0.042, 0.010, 0];
    case 5: return [0.006, 0.024, 0];
    case 6: return [0.006, 0.0, 0.028];
    case 7: return [-0.010, -0.034, 0];
    case 9: return [0.032, 0.0, 0];
    case 10: return [-0.004, -0.016, 0];
    case 11: return [0.032, 0.006, 0];
    case 12: return [-0.006, -0.024, 0];
    case 13: return [0.010, 0.0, 0.034];
    case 14: return [-0.012, -0.050, 0];
    case 15: return [0.004, -0.014, 0.020];
    case 16: return [0.012, 0.032, 0];
    case 17: return [0.012, 0.0, 0];
    case 18: return [0.032, 0.010, 0];
    case 19: return [0.006, 0.0, 0.022];
    case 21: return [0.004, 0.018, 0];
    default: return [0, 0, 0];
  }
}

/**
 * The painter of one head: paint(x, y, i, part, r, g, b, shade, material) -> [r, g, b] for a pixel of the head (or of
 * a beard, for the mouth on it), and local(x, y, i) -> the pixel in the head's own frame (for the locks of the hair).
 * sf.head (set by the rig) says where the head is: { hc, hy, cpi, spi, hr, S, th, ox, oy, tilt, spec, pose, skin, face }.
 */
function faceRenderer(sf) {
  const H = sf.head, F = H.face || faceOf(H.spec), pose = H.pose || {}, z = sf.z;
  const c = Math.cos(H.th), s = Math.sin(H.th), cy = Math.cos(H.hy), sy = Math.sin(H.hy), S = H.S, hr = H.hr, toFace = hr[1] / hr[0];
  const unit = hr[0] * S, pxu = 1 / unit;                         // painted pixels to one half head width, and back
  const skin = tonesOf(H.skin);
  const toHead = (vx, vy, vz) => { const a0 = vx * cy - vz * sy, a2 = vx * sy + vz * cy; return [a0, vy * H.cpi + a2 * H.spi, -vy * H.spi + a2 * H.cpi]; };
  // the light (from the picture's upper left) and the viewer, in the head's own frame
  const lh = toHead(-LX * c + LZ * s, -LY, LX * s + LZ * c), ll = Math.hypot(lh[0], lh[1]) || 1, LHX = lh[0] / ll, LHY = lh[1] / ll;
  const vh = toHead(s, 0, c);
  const e = F.eye, blink = !!pose.blink, squeeze = !!pose.squeeze;
  const [bUp, bIn, bLeft] = browsFor(pose).map((v) => v * F.expressive);
  const talk = pose.mouth || 0, browAlive = talk ? 0.008 * F.expressive : 0;
  // sizes, never smaller than a painted pixel or so
  const EW = Math.max(e.w, 1.7 * pxu), EH = Math.max(e.h, (e.thin ? 0.55 : 0.95) * pxu);
  const lashT = Math.max(e.line ?? 0.028 + 0.012 * e.lash, 0.85 * pxu), irisR = Math.max(e.iris * EW, 0.95 * pxu), pupilR = irisR * 0.45;
  const whiteK = smooth(6.5, 15, unit);                             // a small face: the whites give way to the skin, and the eye reads as a dark shape
  const detail = smooth(9, 18, unit);                               // a big face: lashes one by one, a lid crease, fine streaks in the iris
  const col = (x) => colourOf(x);
  const darkC = col(F.dark), irisBase = F.iris ? col(F.iris) : darkC.map((v) => v * 1.9 + 0.035);
  const irisC = irisBase.map((v, j) => lerp(darkC[j] * 1.1, v, smooth(0.75, 1.5, irisR * unit)));     // (an iris a pixel or two across reads only as dark)
  const whiteC = col(F.white), lipC = col(F.mouth.lip), blushC = col(F.blushColor), browC = F.brow.none ? null : col(F.brow.color);
  const lashC = [0.105, 0.068, 0.058], pupilC = [0.055, 0.040, 0.036], mouthIn = col("#3a1612"), teethC = [0.93, 0.90, 0.84], tongueC = [0.70, 0.34, 0.33];
  const baseSkin = [skin[3], skin[4], skin[5]], shadeSkin = [skin[6], skin[7], skin[8]], deepSkin = [skin[9], skin[10], skin[11]];
  const shadowC = F.eyeshadow ? col(F.eyeshadow) : null, shadesC = F.shades ? col(F.shades) : null;
  const must = F.moustache ? tonesOf(F.moustache) : null, stubbleT = F.beardShadow ? tonesOf(F.beardShadow) : null;
  const ex = F.eyeX, eyY = F.eyeY;
  const noseTipY = eyY - (0.04 + 0.34 * F.nose.len) * toFace;
  const my = F.mouth.y, mw = F.mouth.w;
  const flick = e.lash ? (e.flick ?? 0.12 + 0.10 * e.lash) : 0;
  const upper = (u) => { const q = 1 - u * u; return q <= 0 ? 0 : EH * Math.pow(q, 0.62) * (1 - 0.12 * u); };
  const cheer = (e.cheer ?? F.cheer ?? 0) * (pose.blink ? 0 : 1);       // smiling eyes: the lower lid comes up a little
  const lower = (u) => { const q = 1 - u * u; return q <= 0 ? 0 : -EH * 0.80 * (1 - 0.40 * cheer) * Math.pow(q, 0.9) * (1 + 0.12 * u); };
  const lidOf = (u) => upper(u) - e.lid * EH * Math.max(0, 1 - u * u) * 1.05;
  // where the eyes look: ahead, or (pose.look === "viewer", a portrait) back at the viewer
  const toViewer = pose.look === "viewer", gx = toViewer ? Math.max(-0.42, Math.min(0.42, vh[0] * 0.62)) : F.gaze[0], gy = toViewer ? Math.max(-0.3, Math.min(0.3, vh[1] * 0.5)) : F.gaze[1];
  const hairAt = F.where;
  const hairBase = H.spec.hair && H.spec.hair.mat ? tonesOf(H.spec.hair.mat) : null;

  const over = (C, c3, a) => { if (a > 0) { if (a > 1) a = 1; C[0] += (c3[0] - C[0]) * a; C[1] += (c3[1] - C[1]) * a; C[2] += (c3[2] - C[2]) * a; } };
  const mulc = (C, f, a) => { if (a > 0) { const m = 1 + (f - 1) * Math.min(1, a); C[0] *= m; C[1] *= m; C[2] *= m; } };
  const mulc3 = (C, fr, fg, fb, a) => { if (a > 0) { a = Math.min(1, a); C[0] *= 1 + (fr - 1) * a; C[1] *= 1 + (fg - 1) * a; C[2] *= 1 + (fb - 1) * a; } };
  const cv = (d, aa) => clamp01(0.5 - d / aa);                     // coverage from a signed distance (negative inside)
  const capsule = (px, py, ax, ay, bx, by, ra, rb) => {
    const dx = bx - ax, dy = by - ay, l2 = dx * dx + dy * dy || 1e-9, t = clamp01(((px - ax) * dx + (py - ay) * dy) / l2);
    return Math.hypot(px - ax - dx * t, py - ay - dy * t) - (ra + (rb - ra) * t);
  };

  function eyeAt(C, X, Y, side, aa, shade) {
    // eye-local: u runs from the inner corner (-1) to the outer one (1); mirrored for the left eye, and so is the light
    const LX2 = side * LHX, qx = side * X - ex, qy0 = Y - eyY, qy = qy0 - 0.06 * qx;
    // the shadow of the socket, under the brow and beside the nose; and paint on the lid
    const sdx = (qx + 0.03) / (EW * 1.6), sdy = (qy - EH * 0.7) / (EH * 3.4 + 0.04), sq = sdx * sdx + sdy * sdy;
    if (sq < 1) mulc(C, 0.82, e.socket * (1 - smooth(0.2, 1, sq)) * (0.7 + 0.6 * clamp01(-qx / EW)) * 1.25);
    if (shadowC && sq < 1 && qy > 0) over(C, shadowC, 0.32 * (1 - smooth(0.15, 1, sq)) * smooth(0, EH * 1.3, qy));
    if (Math.abs(qx) > EW * 2.0 || Math.abs(qy) > EH * 3.6 + 0.12) return;
    const u = qx / EW, uc = u < -1 ? -1 : u > 1 ? 1 : u;
    if (e.bags) { const lo = lower(uc), dd = Math.abs(qy - (lo - 0.045)) - 0.022; mulc(C, 0.86, e.bags * cv(dd, aa * 2) * Math.max(0, 1 - u * u)); }
    if (cheer > 0 && Math.abs(u) < 1.1) { const lo = lower(uc), dd = Math.abs(qy - (lo - 0.040 - 0.02 * u * u)) - 0.010; mulc(C, 0.90, cheer * 1.6 * detail * cv(dd, aa * 1.5) * Math.max(0, 1 - u * u)); }
    if (shadesC) {                                                   // dark glasses: one lens over each eye, wide and low, joined over the nose
      const lx2 = (qx - EW * 0.15) / (EW * 1.55), ly2 = (qy + 0.004) / 0.115;
      const d = (Math.pow(Math.pow(Math.abs(lx2), 3) + Math.pow(Math.abs(ly2 > 0 ? ly2 * 1.25 : ly2), 3), 1 / 3) - 1) * 0.11;
      const a = cv(d, aa);
      if (a > 0) {
        over(C, shadesC, a);
        const gl = capsule(lx2, ly2, -0.55 * side, 0.55, -0.05 * side, 0.10, 0.10, 0.04);      // the sky in it, toward the light
        over(C, [0.62, 0.66, 0.78], a * 0.55 * cv(gl, 0.2));
      }
      return;
    }
    if (e.crows || F.lines >= 2) for (const [ry, rl] of [[0.04, 0.16], [-0.03, 0.14], [0.11, 0.12]]) {
      mulc(C, 0.87, 0.6 * cv(capsule(qx, qy, EW * 1.05, ry * 0.4, EW * 1.05 + rl, ry * 1.6 + 0.01, 0.010, 0.004), aa));
    }
    if (blink) {
      // shut: the lid comes down; along its edge, the lashes (and a girl's, pointing down and out)
      const cl = (uu) => -EH * (squeeze ? 0.08 : 0.28) * Math.max(0, 1 - uu * uu) + EH * 0.10;
      if (Math.abs(u) <= 1.12) {
        const yl = cl(uc), up2 = upper(uc);
        if (qy < up2 && qy > yl && Math.abs(u) < 1) mulc(C, 0.93, 1);
        const th = lashT * (0.55 + 0.75 * smooth(-0.6, 1, u)) * (squeeze ? 1.25 : 1);
        over(C, lashC, cv(Math.max(Math.abs(qy - yl) - th * 0.5, (Math.abs(u) - 1.02) * EW), aa) * 0.92);
        if (e.lash) for (const [ru, ln] of [[0.45, 1], [0.75, 1.15], [0.98, 1.25]]) {
          const rx = ru * EW, ry = cl(Math.min(1, ru)), L = EH * (0.5 + 0.35 * e.lash) * ln;
          over(C, lashC, cv(capsule(qx, qy, rx, ry, rx + L * 0.55, ry - L * 0.85, Math.max(th * 0.42, 0.45 * pxu), th * 0.12), aa) * 0.85);
        }
        if (squeeze) for (const dy of [0.05, 0.10]) mulc(C, 0.84, cv(capsule(qx, qy, EW * 0.75, EH * 0.2 + dy * 0.3, EW * 1.25, EH * 0.2 + dy, 0.009, 0.004), aa));
      }
      return;
    }
    const top = lidOf(uc), bot = lower(uc);
    // the crease of the lid, a little above it
    if (Math.abs(u) < 1 && detail > 0) { const cr = upper(uc) + EH * 0.55 + 0.014; mulc(C, 0.88, 0.5 * detail * cv(Math.abs(qy - cr) - 0.010, aa) * smooth(-0.7, 0.2, u)); }
    // the opening: the white, the iris, the pupil, and the light in them
    const dIn = Math.max(qy - top, bot - qy, (Math.abs(u) - 1) * EW * 0.6);
    const open = cv(dIn, aa);
    if (open > 0) {
      const W = whiteC.map((v, j) => lerp(lerp(baseSkin[j], shadeSkin[j], 0.35), v, whiteK));
      if (u < -0.62) { const pk = smooth(-0.62, -0.95, u) * whiteK; W[0] = lerp(W[0], 0.86, pk); W[1] = lerp(W[1], 0.62, pk); W[2] = lerp(W[2], 0.60, pk); }   // the pink of the inner corner
      const lidSh = 0.58 + 0.42 * smooth(0, EH * 0.8, top - qy), sideSh = 1 - 0.18 * smooth(0.4, 1, Math.abs(u));
      let r = W[0] * lidSh * sideSh, g = W[1] * lidSh * sideSh, b = W[2] * lidSh * sideSh;
      const icx = side * gx * EW, icy = top * 0.42 + bot * 0.58 + gy * EH + EH * 0.03;
      const dx = qx - icx, dy = qy - icy, dr = Math.hypot(dx, dy), ia = cv(dr - irisR, aa);
      if (ia > 0) {
        const rr = dr / irisR, lit = clamp01(-(dx * LX2 + dy * LHY) / irisR);
        const f = (0.62 + 0.45 * lit) * (rr > 0.76 ? lerp(1, 0.52, smooth(0.76, 1, rr)) : 1);
        const st = 1 + detail * 0.08 * noise(Math.atan2(dy, dx) * 6, rr * 2);
        let ir = irisC[0] * f * st, ig = irisC[1] * f * st, ib = irisC[2] * f * st;
        const pa = cv(dr - pupilR, aa);
        ir = lerp(ir, pupilC[0], pa); ig = lerp(ig, pupilC[1], pa); ib = lerp(ib, pupilC[2], pa);
        const ls = 0.55 + 0.45 * lidSh;
        r = lerp(r, ir * ls, ia); g = lerp(g, ig * ls, ia); b = lerp(b, ib * ls, ia);
        // the catchlight: toward the light, high in the iris (and a second, smaller one, in bright young eyes)
        const gr = Math.max(irisR * 0.27, 0.42 * pxu);
        const ga = cv(Math.hypot(dx - LX2 * 0.42 * irisR, dy - (LHY * 0.42 + 0.20) * irisR) - gr, aa) * ia;
        r = lerp(r, 1, ga * 0.95); g = lerp(g, 1, ga * 0.95); b = lerp(b, 1, ga * 0.95);
        if (e.glint2) { const a2 = cv(Math.hypot(dx + LX2 * 0.40 * irisR, dy + LHY * 0.40 * irisR + 0.12 * irisR) - irisR * 0.12, aa) * ia * detail; r = lerp(r, 1, a2 * 0.7); g = lerp(g, 1, a2 * 0.7); b = lerp(b, 1, a2 * 0.7); }
      }
      const lt = 1 - 0.28 * shade;
      over(C, [r * lt, g * lt, b * lt], open);
    }
    // the lower lash line, faint, on the outer two thirds
    if (Math.abs(u) < 1.02) over(C, lashC, cv(Math.abs(qy - bot + 0.004) - Math.max(0.008, 0.3 * pxu), aa) * e.lower * smooth(-0.5, 0.4, u) * 0.85);
    // kohl: black paint all round the eye, and out toward the temple
    if (e.kohl) over(C, [0.07, 0.06, 0.08], cv(Math.min(Math.abs(dIn) - Math.max(0.016, 0.45 * pxu), capsule(qx, qy, EW * 0.95, EH * 0.1, EW * 1.8, EH * 0.38, Math.max(0.020, 0.5 * pxu), 0.006)), aa) * 0.95);
    // the upper lid's line of lashes, thicker toward the outer corner; for women and girls a flick out past it, and a
    // little girl's lashes one by one
    if (Math.abs(u) < 1.06) {
      const th = lashT * (0.50 + 0.80 * smooth(-0.7, 1, uc));
      over(C, lashC, cv(Math.max(Math.abs(qy - top - th * 0.15) - th * 0.5, (Math.abs(u) - 1.0) * EW), aa) * 0.96);
    }
    if (flick) {
      const x0 = EW * 0.78, y0 = lidOf(0.78);
      over(C, lashC, cv(capsule(qx, qy, x0, y0, EW * (1 + flick), y0 + EH * (0.30 + 0.28 * Math.min(1.5, e.lash)), lashT * 0.72, lashT * 0.18), aa) * 0.94);
      if (e.lash >= 2) for (const [ru, ang, ln] of [[0.40, 1.42, 0.85], [0.62, 1.18, 1.0], [0.82, 0.92, 1.05], [0.98, 0.62, 0.9]]) {
        const rx = ru * EW, ry = lidOf(ru), L = Math.max(EH * 0.55 * ln, 1.6 * pxu * ln);
        over(C, lashC, cv(capsule(qx, qy, rx, ry, rx + Math.cos(ang) * L, ry + Math.sin(ang) * L, Math.max(lashT * 0.32, 0.45 * pxu), Math.max(lashT * 0.10, 0.22 * pxu)), aa) * 0.9);
      }
    }
  }

  function browAt(C, X, Y, side, aa) {
    if (!browC) return;
    const B = F.brow, lx = side * X - ex, len = EW * 2.15 * B.len;
    const x0 = -EW * 1.05, t = (lx - x0) / len;
    if (t < -0.15 || t > 1.15) return;
    const tc = clamp01(t);
    const base = eyY + EH + B.up + bUp + (side > 0 ? bLeft : 0) + browAlive;
    const peak = 0.60, archF = tc < peak ? 1 - ((tc - peak) / peak) ** 2 : 1 - ((tc - peak) / (1 - peak)) ** 2;
    const yc = base + B.arch * archF + (B.tilt + bIn) * (1 - tc) * (1 - tc) - 0.028 * tc * tc;
    const thick = Math.max(B.thick, 0.8 * pxu);
    const th = thick * (tc < 0.16 ? 0.82 + 1.1 * tc : 1 - 0.60 * Math.pow((tc - 0.16) / 0.84, 1.4));
    const d = Math.max(Math.abs(Y - yc) - th * 0.5, Math.max(-t, t - 1) * len);
    const a = cv(d, aa);
    if (a <= 0) return;
    over(C, browC, a * 0.92 * (1 - 0.22 * detail * (0.5 + 0.5 * noise(lx * 55, Y * 8))));
  }

  function moustacheAt(C, X, Y, aa, line) {
    if (!must) return;
    const u = X / (mw * 1.25);
    if (Math.abs(u) > 1.05) return;
    const q = Math.max(0, 1 - u * u), bottom = line + Math.max(0.014, 0.6 * pxu) - 0.09 * u * u;
    const top = bottom + 0.060 + 0.120 * Math.pow(q, 0.7) - 0.012 * smooth(0.12, 0, Math.abs(u));
    const d = Math.max(Y - top, bottom - Y, (Math.abs(u) - 1) * mw);
    const a = cv(d, aa);
    if (a <= 0) return;
    const sh = smooth(bottom, top, Y), hairs = 0.85 + 0.15 * noise(X * 40 + Y * 12, Y * 6);
    const tone = 1.35 - 0.85 * sh;                                   // (darker over the lip, lighter at its upper edge)
    const j = Math.floor(tone), f = tone - j, o = j * 3;
    over(C, [lerp(must[o], must[o + 3], f) * hairs, lerp(must[o + 1], must[o + 4], f) * hairs, lerp(must[o + 2], must[o + 5], f) * hairs], a * 0.96);
  }

  function mouthAt(C, X, Y, aa, shade) {
    const M = F.mouth;
    if (Math.abs(X) > mw * 1.7 || Math.abs(Y - my) > 0.32) return;
    const u = X / mw, au = Math.abs(u), smile = M.smile;
    const line = my + smile * 0.055 * u * u - (smile < 0 ? 0.012 : 0);
    // the soft shadow under the lower lip
    mulc(C, 0.90, 0.55 * cv(capsule(X, Y, -mw * 0.42, line - M.lower - 0.034, mw * 0.42, line - M.lower - 0.034, 0.030, 0.030), aa * 3));
    if (M.hidden && !talk) return;
    const lipShade = 1 - 0.25 * shade;
    const L = [lipC[0] * lipShade, lipC[1] * lipShade, lipC[2] * lipShade];
    const open = talk === 1 ? Math.max(0.032, 1.1 * pxu) : talk >= 2 ? Math.max(0.066, 2.0 * pxu) : 0;
    const ow = mw * (talk >= 2 ? 0.74 : 0.64);
    if (au < 1.06) {
      const q = Math.max(0, 1 - u * u);
      const bow = 0.012 * smooth(0.18, 0, au) * smooth(0, 0.06, au) - 0.006 * smooth(0.06, 0, au);
      const up = M.upper * Math.pow(q, 0.55) + bow, lo = M.lower * Math.pow(q, 0.65);
      const oTop = line + (open ? open * 0.15 : 0), oBot = line - open;
      over(C, [L[0] * 0.80, L[1] * 0.76, L[2] * 0.78], cv(Math.max(Y - (oTop + up), oTop - Y, (au - 1) * mw), aa) * M.lipA);       // the upper lip, in its own shade
      const al = cv(Math.max(Y - oBot, oBot - lo - Y, (au - 1) * mw), aa) * M.lipA;
      if (al > 0) {                                                  // the lower lip, with the light on it
        const hl = smooth(0.65, 0.0, Math.hypot((X - LHX * mw * 0.22) / (mw * 0.5), (Y - (oBot - lo * 0.45)) / (lo * 0.55 + 1e-3)));
        const k2 = 1 + 0.28 * hl * detail;
        over(C, [L[0] * k2, L[1] * k2, L[2] * k2], al);
      }
      if (open) {
        const hh = (oTop - oBot) / 2, ox = X / ow, oy = (Y - (oTop + oBot) / 2) / (hh + 1e-4), od = (Math.sqrt(ox * ox + oy * oy) - 1) * Math.min(ow, hh);
        const oa = cv(od, aa);
        if (oa > 0) {
          let I = [...mouthIn];
          if (oy > 0.25) { const tt = smooth(0.25, 0.55, oy) * 0.9 * detail; I = [lerp(I[0], teethC[0], tt), lerp(I[1], teethC[1], tt), lerp(I[2], teethC[2], tt)]; }
          if (oy < -0.40) { const tg = smooth(-0.40, -0.85, oy) * 0.7; I = [lerp(I[0], tongueC[0], tg), lerp(I[1], tongueC[1], tg), lerp(I[2], tongueC[2], tg)]; }
          over(C, I.map((v) => v * lipShade), oa);
        }
      } else {                                                       // the line between the lips, deeper at the corners
        const dlin = Math.abs(Y - line) - Math.max(0.0085 + 0.006 * au * au, 0.38 * pxu);
        over(C, [L[0] * 0.45, L[1] * 0.32, L[2] * 0.32], cv(dlin, aa) * Math.min(1, 0.6 + M.lipA * 0.6) * (au < 1.02 ? 1 : 0));
      }
    }
    if (smile > 0.2 && !open) for (const sd of [-1, 1]) mulc(C, 0.84, cv(capsule(X, Y, sd * mw * 1.0, line + 0.010, sd * mw * 1.12, line + 0.032, 0.010, 0.006), aa) * 0.7 * Math.min(1, smile));
    moustacheAt(C, X, Y, aa, line);
  }

  function noseAt(C, X, Y, aa, part, shade) {
    const nw = 0.070 * F.nose.w * (0.8 + 0.2 * F.nose.tip), tipY = noseTipY;
    // under the nose, a soft shadow falling away from the light
    const sx = (X + LHX * 0.05) / (0.15 * F.nose.w), sy = (Y - (tipY - 0.10)) / 0.055, q = sx * sx + sy * sy;
    if (q < 1) over(C, shadeSkin, 0.42 * (1 - smooth(0.15, 1, q)));
    if (part !== P_NOSE) {
      for (const sd of [-1, 1]) {                                    // the nostrils
        const nx = (X - sd * nw) / 0.030, ny = (Y - (tipY - 0.045)) / 0.017;
        over(C, deepSkin, cv((Math.sqrt(nx * nx + ny * ny) - 1) * 0.017, aa) * 0.50);
      }
      // the side of the nose away from the light, down from between the eyes
      if (Y < eyY - 0.02 && Y > tipY - 0.03) mulc(C, 0.88, cv(Math.abs(X + LHX * 0.075) - 0.035, aa * 3) * 0.7 * smooth(eyY - 0.02, eyY - 0.14, Y));
    }
    // a little light on the bridge and the tip
    const hx = (X - LHX * 0.03) / 0.055, hy = (Y - tipY - 0.03) / 0.06, hq = hx * hx + hy * hy;
    if (hq < 1) over(C, [skin[0], skin[1], skin[2]], 0.40 * (1 - hq) * (1 - shade));
  }

  /** A pixel of the picture, back to the character and then to the head's own frame: [x, y, z] in half head widths. */
  const local = (x, y, i) => {
    const px = x + 0.5 - H.ox, py = y + 0.5, dp = z[i];
    const v0 = (-px * c + dp * s) / S, v2 = (px * s + dp * c) / S, v1 = (H.oy - py + dp * H.tilt) / S;
    const w0 = v0 - H.hc[0], w1 = v1 - H.hc[1], w2 = v2 - H.hc[2];
    const t0 = w0 * cy - w2 * sy, t2 = w0 * sy + w2 * cy;
    return [t0 / hr[0], (w1 * H.cpi + t2 * H.spi) / hr[0], (-w1 * H.spi + t2 * H.cpi) / hr[2]];
  };

  const paint = function paintFace(x, y, i, part, r, g, b, shade, mi) {
    const [X, Y, Zf] = local(x, y, i);
    const C = [r, g, b];
    if (Zf < -0.3) return C;
    // how big one painted pixel is here, in half head widths: bigger where the face turns away
    const Yh = Y / toFace, nl = Math.hypot(X, Yh, Zf) || 1;
    const facing = Math.abs((X * vh[0] + Yh * vh[1] + Zf * vh[2]) / nl);
    const aa = pxu / Math.max(0.28, facing);
    if (part === P_HAIR) { if (F.mouth.onBeard) mouthAt(C, X, Y, aa, shade); return C; }
    if (mi >= 0 && sf.hairMats.has(sf.mats[mi])) return C;            // (the scalp, where the hair grows: painted as hair)
    // fine hair at the edge of the hairline, so that it is not a helmet's edge
    if (hairAt && hairBase) {
      const dd = 0.9 * pxu, Yn = Y / toFace;
      let nH = 0;
      for (const [ox, oy] of [[dd, 0], [-dd, 0], [0, dd], [0, -dd]]) if (hairAt(X + ox, Yn + oy / toFace, Zf)) nH++;
      if (nH) { const k2 = r / (baseSkin[0] || 1); over(C, [hairBase[3] * k2, hairBase[4] * k2, hairBase[5] * k2], nH * 0.16); }
    }
    // A face is not one colour: a little yellower on the brow, redder across the cheeks and the nose, cooler round a
    // man's jaw. And it is modelled in planes: the side that turns from the light, the hollow under the cheekbone; a
    // light on the brow, the cheekbone and the chin.
    {
      const brow = smooth(eyY + 0.18, eyY + 0.60, Y), mid = Math.exp(-(((Y - (eyY - 0.30)) / 0.30) ** 2)) * (1 - 0.4 * smooth(0.55, 0.95, Math.abs(X)));
      mulc3(C, 1.015, 1.008, 0.965, brow * 0.9);
      mulc3(C, 1.025, 0.965, 0.955, mid * 0.9);
      if (F.stubble) mulc3(C, 0.95, 0.965, 1.0, F.stubble * smooth(my + 0.10, my - 0.25, Y) * smooth(0.95, 0.35, Math.abs(X)));
      const away = X * LHX < 0 ? 1 : 0.30;
      mulc3(C, 0.86, 0.85, 0.88, smooth(0.42, 0.95, Math.abs(X)) * away);
      for (const sd of [-1, 1]) {
        const cx = (X - sd * 0.56) / 0.20, cyv = (Y - (eyY - 0.46)) / 0.13, q = cx * cx + cyv * cyv;
        if (q < 1) mulc(C, 0.935, (1 - smooth(0.1, 1, q)) * (sd * LHX < 0 ? 1 : 0.55));
      }
      const lt = [skin[0], skin[1], skin[2]];
      for (const [hx, hy, rx, ry, a] of [[LHX * 0.22, eyY + 0.42, 0.32, 0.20, 0.14], [LHX * 0.56, eyY - 0.20, 0.16, 0.10, 0.12], [LHX * 0.05, my - 0.20, 0.13, 0.08, 0.08]]) {
        const ux = (X - hx) / rx, uy = (Y - hy) / ry, q = ux * ux + uy * uy;
        if (q < 1) over(C, lt, a * (1 - smooth(0, 1, q)) * (1 - shade));
      }
    }
    if (stubbleT && Zf > -0.1) {
      // an unshaven jaw: from the sideburns down round the jaw and the chin, and over the lip, a speckle of dark
      const ax = Math.abs(X), topY = lerp(my + 0.17, eyY - 0.40, smooth(0.22, 0.72, ax)), a = smooth(topY, topY - 0.10, Y) * (1 - smooth(0.92, 1.05, ax));
      if (a > 0) { const sp = 0.70 + 0.30 * noise(X * 90, Y * 90); over(C, [stubbleT[3] * sp, stubbleT[4] * sp, stubbleT[5] * sp], a * 0.48); }
    }
    // cheeks, warm
    if (F.blush > 0) for (const sd of [-1, 1]) {
      const bx = (X - sd * 0.50) / 0.28, by = (Y - (my * 0.40 + eyY * 0.25)) / 0.21, q = bx * bx + by * by;
      if (q < 1) over(C, blushC, F.blush * (1 - smooth(0, 1, q)) * (1 - 0.35 * shade));
    }
    if (F.freckles && Zf > 0.2) for (const [fx, fy, fr] of FRECKLES) {
      const d = Math.hypot(X - fx, Y - (eyY + fy)) - Math.max(fr, 0.4 * pxu);
      if (d < aa) over(C, [deepSkin[0] * 1.15, deepSkin[1] * 1.08, deepSkin[2]], cv(d, aa) * 0.34);
    }
    if (F.lines) for (const sd of [-1, 1]) {
      mulc(C, 0.88, cv(capsule(X, Y, sd * 0.27, eyY - 0.50, sd * 0.40, my + 0.06, 0.012, 0.008), aa * 1.5) * 0.7);
      if (F.lines > 1 && Zf > 0.5) mulc(C, 0.9, cv(Math.abs(Y - (eyY + 0.62 + 0.05 * Math.cos(X * 3))) - 0.008, aa) * 0.5 * smooth(0.5, 0.2, Math.abs(X)));
    }
    if (shadesC && Zf > -0.2) {                                      // the bridge of the dark glasses, and their arms back toward the ears
      const yb = eyY + 0.075, db = Math.min(Math.abs(X) < 0.20 ? Math.abs(Y - yb) - 0.022 : 9, Math.abs(X) > 0.66 ? Math.abs(Y - (yb - 0.01)) - 0.020 : 9);
      over(C, shadesC, cv(db, aa) * (Math.abs(X) > 0.66 ? smooth(1.0, 0.9, Math.abs(X)) : 1));
    }
    if (Zf > 0.05) {
      noseAt(C, X, Y, aa, part, shade);
      if (part === P_HEAD) {
        const side = X >= 0 ? 1 : -1;
        eyeAt(C, X, Y, side, aa, shade);
        browAt(C, X, Y, side, aa);
        mouthAt(C, X, Y, aa, shade);
      }
    }
    return C;
  };
  paint.local = local;
  paint.beard = F.mouth.onBeard;
  return paint;
}

// freckles across the nose and the cheeks: [x, y below the eyes, radius], in half head widths
const FRECKLES = [];
{
  let s = 777;
  const rnd = () => ((s = (Math.imul(s, 1103515245) + 12345) >>> 0) / 4294967296);
  for (let n = 0; n < 60 && FRECKLES.length < 16; n++) {
    const x = (rnd() * 2 - 1) * 0.60, y = -0.14 - rnd() * 0.26;
    if (Math.abs(x) < 0.12 && y > -0.22) continue;
    FRECKLES.push([x, y, 0.014 + rnd() * 0.010]);
  }
}

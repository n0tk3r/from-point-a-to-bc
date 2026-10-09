// A small pixel renderer for sprites.
//
// Characters and props are not stored as pictures. They are described as simple
// solid shapes (limbs, balls, flat panels), and this file turns those shapes into
// pixel art: hard edges, no smoothing, and flat tones instead of gradients. Because the pixels are worked out at whatever size is asked for, a
// character can stand anywhere in a scene's depth and still be drawn crisply.
//
// The picture is lit from the upper left, in every scene and every era.
//
//   const s = new Surface(64, 140, 32, 134);     // width, height, and where the feet go
//   s.limb(ax, ay, az, bx, by, bz, ra, rb, SKIN);  // a tapered limb between two points
//   s.ball(cx, cy, cz, rx, ry, rz, SHIRT);         // a rounded mass
//   s.poly([[x, y], ...], z, WOOD, 1);             // a flat panel in one tone
//   const picture = s.finish().toCanvas();
//
// x runs right, y runs DOWN, and z comes toward the viewer: a larger z is nearer
// and hides what is behind it.

import { tonesOf, pixelOf } from "./look.js";      // the paints: every colour in the key of the scene on stage (look.js)

/** "#rrggbb" (or "#rrggbbaa") as one number in the byte order a canvas wants. */
export function pack(hex) {
  const n = parseInt(hex.slice(1, 7), 16);
  const a = hex.length > 7 ? parseInt(hex.slice(7, 9), 16) : 255;
  return ((a << 24) | ((n & 255) << 16) | (((n >> 8) & 255) << 8) | ((n >> 16) & 255)) >>> 0;
}

/** A material: four tones from lightest to darkest. Shadows are a color, never black. */
export function ramp(light, base, shade, deep, more = {}) {
  return { tones: [pack(light), pack(base), pack(shade), pack(deep)], ...more };
}

/** The same material one step brighter or darker, for collars, cuffs and trims. */
export function shifted(material, by) {
  const t = material.tones, pick = (i) => t[Math.min(3, Math.max(0, i + by))];
  return { ...material, tones: [pick(0), pick(1), pick(2), pick(3)] };
}

// Direction to the light, in picture space (y down): up, left and toward the viewer.
const LX = -0.50, LY = -0.66, LZ = 0.56;

// Flat shading, the way a hand-drawn sprite is shaded: a form is its plain color, and the side turned
// from the light is one darker tone, with a clean edge between the two. Nothing is modelled round.
// The lightest tone is kept for materials that really shine (shine: true), and the deepest for the
// thin lines where one thing lies in front of another.
function toneOf(nx, ny, nz, material) {
  const d = nx * LX + ny * LY + nz * LZ + (material.lift || 0);
  if (material.shine && d > 0.80) return 0;
  return d > (material.cut ?? 0.20) ? 1 : 2;
}

export class Surface {
  constructor(w, h, ox, oy) {
    this.w = w; this.h = h;
    this.ox = ox; this.oy = oy;                 // the anchor: where the thing touches the ground
    const n = w * h;
    this.z = new Float32Array(n).fill(-1e9);    // depth of the nearest shape at each pixel
    this.m = new Uint8Array(n);                 // material number + 1 (0 = nothing here)
    this.t = new Uint8Array(n);                 // tone, 0 (light) to 3 (deep)
    this.p = new Uint8Array(n);                 // which body part or panel
    this.mats = [];
    this.stamps = [];
    this.marks = [];
    this.out = null;
  }

  mat(material) {
    let i = this.mats.indexOf(material);
    if (i < 0) { this.mats.push(material); i = this.mats.length - 1; }
    return i + 1;
  }

  /** A limb: a rounded, tapered tube from a to b, shaded as if it were round.
      Options: part, bias (nudge nearer), depth (how deep it is compared with its width),
      squareEnd (cut flat at b), squareStart (cut flat at a), fn(t, across, along, x, y) to change material or skip a pixel,
      over ({ part: slack }): lie on top of those parts even where they bulge out by up to `slack`,
      the way a loose shirt hangs over whatever is under it. tone: one fixed tone, no shading of its own
      (for a form built of several shapes, which is then shaded as one: see `inset` in finish). */
  limb(ax, ay, az, bx, by, bz, ra, rb, material, o = {}) {
    const x0 = Math.max(0, Math.floor(Math.min(ax - ra, bx - rb))), x1 = Math.min(this.w - 1, Math.ceil(Math.max(ax + ra, bx + rb)));
    const y0 = Math.max(0, Math.floor(Math.min(ay - ra, by - rb))), y1 = Math.min(this.h - 1, Math.ceil(Math.max(ay + ra, by + rb)));
    const abx = bx - ax, aby = by - ay, len2 = abx * abx + aby * aby;
    const mi = this.mat(material), part = o.part || 0, fn = o.fn, flat = o.flatten || 1, bias = o.bias || 0, deep = o.depth || 1, square = o.squareEnd, squareA = o.squareStart, over = o.over, fixed = o.tone;
    const W = this.w, Z = this.z, M = this.m, P = this.p, T = this.t;       // (this loop is where most of the time goes: nothing in it is looked up twice)
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) {
        const px = x + 0.5, py = y + 0.5;
        let t = len2 > 1e-6 ? ((px - ax) * abx + (py - ay) * aby) / len2 : 0;
        if ((square && t > 1) || (squareA && t < 0)) continue;  // cut straight across instead of rounding the end off
        t = t < 0 ? 0 : t > 1 ? 1 : t;
        const r = ra + (rb - ra) * t;
        const dx = px - (ax + abx * t), dy = py - (ay + aby * t), d2 = dx * dx + dy * dy;
        if (d2 > r * r) continue;
        const up = Math.sqrt(r * r - d2);
        let z = az + (bz - az) * t + up * deep + bias;
        const i = y * W + x;
        if (z <= Z[i]) {
          const slack = over && over[P[i]];
          if (!slack || z + slack <= Z[i]) continue;
          z = Z[i] + 0.02;                                       // resting on the thing it covers
        }
        let use = material, mm = mi;
        if (fn) {
          const alt = fn(t, dx / r, dy / r, x, y);
          if (alt === null) continue;
          if (alt) { use = alt; mm = this.mat(alt); }
        }
        Z[i] = z; M[i] = mm; P[i] = part;
        if (fixed != null) T[i] = fixed;
        else if (use.flat != null) T[i] = use.flat;
        else { const nx = dx / r, ny = dy / r, nz = (up / r) * flat, inv = 1 / Math.sqrt(nx * nx + ny * ny + nz * nz); T[i] = toneOf(nx * inv, ny * inv, nz * inv, use); }
      }
    }
  }

  /** A ball or egg shape. rz is how far it bulges toward the viewer. */
  ball(cx, cy, cz, rx, ry, rz, material, o = {}) {
    const x0 = Math.max(0, Math.floor(cx - rx)), x1 = Math.min(this.w - 1, Math.ceil(cx + rx));
    const y0 = Math.max(0, Math.floor(cy - ry)), y1 = Math.min(this.h - 1, Math.ceil(cy + ry));
    const mi = this.mat(material), part = o.part || 0, fn = o.fn, bias = o.bias || 0, flat = o.flatten || 1, fixed = o.tone;
    const W = this.w, Z = this.z, M = this.m, P = this.p, T = this.t;
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) {
        const ux = (x + 0.5 - cx) / rx, uy = (y + 0.5 - cy) / ry, q = ux * ux + uy * uy;
        if (q > 1) continue;
        const uz = Math.sqrt(1 - q);
        const z = cz + uz * rz + bias;
        const i = y * W + x;
        if (z <= Z[i]) continue;
        let use = material, mm = mi;
        if (fn) {
          const alt = fn(ux, uy, uz, x, y);
          if (alt === null) continue;
          if (alt) { use = alt; mm = this.mat(alt); }
        }
        Z[i] = z; M[i] = mm; P[i] = part;
        if (fixed != null) T[i] = fixed;
        else if (use.flat != null) T[i] = use.flat;
        else { const nx = ux / rx, ny = uy / ry, nz = (uz / rz) * flat, inv = 1 / Math.sqrt(nx * nx + ny * ny + nz * nz); T[i] = toneOf(nx * inv, ny * inv, nz * inv, use); }
      }
    }
  }

  /** A flat panel in a single tone. Later panels at the same depth paint over earlier ones. */
  poly(points, z, material, tone = 1, o = {}) {
    let y0 = Infinity, y1 = -Infinity;
    for (const p of points) { if (p[1] < y0) y0 = p[1]; if (p[1] > y1) y1 = p[1]; }
    y0 = Math.max(0, Math.floor(y0)); y1 = Math.min(this.h - 1, Math.ceil(y1));
    const mi = this.mat(material), part = o.part || 0, fn = o.fn;
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
          if (z < this.z[i]) continue;
          let tn = tone, mm = mi;
          if (fn) {
            const alt = fn(x, y);
            if (alt === null) continue;
            if (typeof alt === "number") tn = alt;
            else if (alt) mm = this.mat(alt);
          }
          this.z[i] = z; this.m[i] = mm; this.t[i] = tn; this.p[i] = part;
        }
      }
    }
  }

  rect(x, y, w, h, z, material, tone = 1, o) {
    this.poly([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], z, material, tone, o);
  }

  /** A flat oval, for shadows on the ground and for wheels. */
  oval(cx, cy, rx, ry, z, material, tone = 1, o = {}) {
    const x0 = Math.max(0, Math.floor(cx - rx)), x1 = Math.min(this.w - 1, Math.ceil(cx + rx));
    const y0 = Math.max(0, Math.floor(cy - ry)), y1 = Math.min(this.h - 1, Math.ceil(cy + ry));
    const mi = this.mat(material);
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) {
        const ux = (x + 0.5 - cx) / rx, uy = (y + 0.5 - cy) / ry;
        if (ux * ux + uy * uy > 1) continue;
        const i = y * this.w + x;
        if (z < this.z[i]) continue;
        this.z[i] = z; this.m[i] = mi; this.t[i] = tone; this.p[i] = o.part || 0;
      }
    }
  }

  /** One exact pixel, placed after shading: eyes, buttons, highlights.
      With `part`, it only lands where that part is the one showing. */
  dot(x, y, color, part = null) {
    this.stamps.push([Math.round(x), Math.round(y), color, part]);
  }

  /** A drawn line, one pixel wide, that makes whatever it crosses one tone darker (`by` tones): a fold in
      cloth, a crease, a wrinkle. With `part`, it shows only where that part is the one on top, so a fold
      drawn on a skirt never strays onto the hand in front of it. */
  stroke(ax, ay, bx, by_, by = 1, part = null) {
    const n = Math.max(1, Math.ceil(Math.max(Math.abs(bx - ax), Math.abs(by_ - ay))));
    let px = null, py = null;
    for (let i = 0; i <= n; i++) {
      const x = Math.round(ax + ((bx - ax) * i) / n - 0.5), y = Math.round(ay + ((by_ - ay) * i) / n - 0.5);
      if (x === px && y === py) continue;
      px = x; py = y;
      this.marks.push([x, y, by, part]);
    }
  }

  /** One pixel made darker (or, with a negative `by`, lighter) than it would have been. */
  mark(x, y, by = 1, part = null) { this.marks.push([Math.round(x), Math.round(y), by, part]); }

  /** Turn shapes into the finished picture.
      edge: darken the outline so the figure reads against any backdrop.
      contact: a thin shadow where a nearer part overlaps a farther one.
      seams(a, b, below, x, y): say which neighboring parts should always show a line between them.
      a is the part on the left and b the one on its right; when `below` is true, a is above b.
      x, y is the pixel that would be darkened (the right-hand or lower one).
      cast(a, b): how many pixels of shadow part a may throw on part b (0 for none). The shadow falls down
      and to the right, away from the light, and only as far as a is really in front of b: under a chin,
      under the hem of a shirt, beside an arm held across the body.
      reach: the longest shadow cast() will ever ask for, in pixels (12 if not given): no ray is followed farther.
      rim: the outline on the shadow side is drawn in the deepest tone. outline: the lit side gets a line too.
      inset(part): for a form made of several shapes drawn in one flat tone (a head: skull, jaw and chin),
      the width in pixels of the band of shade along its edge on the side away from the light. This is how a
      hand shades a small figure: not by how round the thing is, but by a band of even width inside its outline.
      It may also answer [width, dx, dy] to say which way the shade side lies for that form. */
  finish({ edge = true, contact = true, gap = 1.6, seams = null, cast = null, rim = false, inset = null, outline = false, reach = 12 } = {}) {
    const { w, h, m, t, z, p, mats } = this, n = w * h;
    const out = new Uint32Array(n), tones = new Uint8Array(n);
    const keyed = mats.map(tonesOf);                         // each material's four tones in the paints of the scene (look.js)
    // which pixels have something solid on them (a ground shadow is not solid), and the box they all lie in
    const sol = new Uint8Array(n), soft = mats.map((material) => (material.soft ? 1 : 0));
    let bx0 = w, bx1 = -1, by0 = h, by1 = -1;
    for (let y = 0, i = 0; y < h; y++) for (let x = 0; x < w; x++, i++) {
      if (!m[i]) continue;
      if (!soft[m[i] - 1]) sol[i] = 1;
      if (x < bx0) bx0 = x; if (x > bx1) bx1 = x; if (y < by0) by0 = y; if (y > by1) by1 = y;
    }
    if (inset) {
      const band = new Uint8Array(n), asked = new Map();
      const wantOf = (part) => { let v = asked.get(part); if (v === undefined) { v = inset(part) || 0; if (v && !Array.isArray(v)) v = [v, 0.6, 0.8]; asked.set(part, v); } return v; };      // how wide, and which way the shade side lies
      for (let y = by0; y <= by1; y++) for (let x = bx0; x <= bx1; x++) {
        const i = y * w + x;
        if (!m[i] || t[i] !== 1) continue;
        const want = wantOf(p[i]);
        if (!want) continue;
        const k = want[0], dx = want[1], dy = want[2];
        for (let j = 1; j <= k; j++) {
          const qx = x + Math.round(j * dx), qy = y + Math.round(j * dy);
          if (qx >= w || qy >= h) { band[i] = 1; break; }
          const q = qy * w + qx;
          if (!sol[q]) { band[i] = 1; break; }                             // the edge of the whole figure
          if (p[q] === p[i]) continue;
          if (z[q] - z[i] > 0.5) break;                                    // something lies in front here: the form's own edge is out of sight
          if (z[i] - z[q] > 2.5) { band[i] = 1; break; }                   // the form ends here, in front of something farther back
        }
      }
      for (let i = 0; i < n; i++) if (band[i]) t[i] = 2;
    }
    let dark = null;
    if (cast) {
      // Follow the light back from each lit pixel: if something nearer stands in its way, the pixel is in shadow.
      const DX = 0.60, DY = 0.80, RISE = 0.68;             // the light comes from the upper left and from in front
      const steps = Math.max(1, Math.min(12, Math.ceil(reach))), sx = [], sy = [], rise = [];
      for (let k = 0; k <= steps; k++) { sx.push(Math.round(k * DX)); sy.push(Math.round(k * DY)); rise.push(k * RISE + 1.4); }
      const known = new Map();                             // what cast() answered for each pair of parts
      const castOf = (a, b) => { const key = a * 256 + b; let v = known.get(key); if (v === undefined) { v = cast(a, b) || 0; known.set(key, v); } return v; };
      dark = new Uint8Array(n);
      for (let y = by0; y <= by1; y++) for (let x = bx0; x <= bx1; x++) {
        const i = y * w + x;
        if (!sol[i] || t[i] >= 2) continue;
        const pi = p[i], zi = z[i];
        for (let k = 1; k <= steps; k++) {
          const qx = x - sx[k], qy = y - sy[k];
          if (qx < 0 || qy < 0) break;
          const q = qy * w + qx;
          if (!sol[q] || p[q] === pi || z[q] - zi < rise[k]) continue;
          if (k <= castOf(p[q], pi)) { dark[i] = 1; break; }
        }
      }
      // a shadow is a clean shape: a lone pixel of it is only dirt
      const shaded = (j) => dark[j] || (m[j] && t[j] >= 2);
      for (let y = Math.max(1, by0); y <= Math.min(h - 2, by1); y++) for (let x = Math.max(1, bx0); x <= Math.min(w - 2, bx1); x++) {
        const i = y * w + x;
        if (dark[i] !== 1) continue;
        if (!shaded(i - 1) && !shaded(i + 1) && !shaded(i - w) && !shaded(i + w)) dark[i] = 2;      // marked, and skipped below
      }
    }
    for (let y = by0; y <= by1; y++) {
      for (let x = bx0; x <= bx1; x++) {
        const i = y * w + x;
        if (!m[i]) continue;
        const material = mats[m[i] - 1];
        let tone = t[i];
        if (sol[i]) {
          if (dark && dark[i] === 1 && tone < 2) tone = 2;
          const L = x > 0 && sol[i - 1] === 1, R = x < w - 1 && sol[i + 1] === 1, U = y > 0 && sol[i - w] === 1, D = y < h - 1 && sol[i + w] === 1;
          // The outline on the shadow side is the shade tone, not a black line. (A deeper line, and one down the lit
          // side as well, only if asked for, and only on forms thick enough to have an inside: a finger or a nose
          // two pixels wide would be nothing but outline.)
          if (edge && (!R || !D)) {
            const thick = (R || (x > 1 && sol[i - 1] === 1 && sol[i - 2] === 1)) && (D || (y > 1 && sol[i - w] === 1 && sol[i - 2 * w] === 1));
            tone = Math.max(tone, rim && thick ? 3 : 2);
          } else if (outline && ((!L && x < w - 2 && sol[i + 2] === 1) || (!U && y < h - 2 && sol[i + 2 * w] === 1))) tone = Math.max(tone, 2);
          if (contact && tone < 3) {
            if ((L && p[i - 1] !== p[i] && z[i - 1] - z[i] > gap) || (U && p[i - w] !== p[i] && z[i - w] - z[i] > gap)) tone++;
            else if (seams && ((L && p[i - 1] !== p[i] && seams(p[i - 1], p[i], false, x, y)) || (U && p[i - w] !== p[i] && seams(p[i - w], p[i], true, x, y)))) tone++;   // two parts that touch: a line between them
          }
        }
        tones[i] = tone;
        out[i] = keyed[m[i] - 1][tone];
      }
    }
    const before = this.marks.length ? tones.slice() : null;      // two lines that cross are not darker where they cross
    for (const [x, y, by, part] of this.marks) {
      if (x < 0 || y < 0 || x >= w || y >= h) continue;
      const i = y * w + x;
      if (!m[i] || (part !== null && p[i] !== part)) continue;
      const material = mats[m[i] - 1];
      if (material.soft) continue;
      const tone = Math.max(0, Math.min(3, before[i] + by));
      if (by > 0 ? tone > tones[i] : tone < tones[i]) { tones[i] = tone; out[i] = keyed[m[i] - 1][tone]; }
    }
    for (const [x, y, color, part] of this.stamps) {
      if (x < 0 || y < 0 || x >= w || y >= h) continue;
      const i = y * w + x;
      if (part !== null && p[i] !== part) continue;
      if (part === null && !m[i]) continue;
      out[i] = pixelOf(color);
    }
    this.out = out;
    return this;
  }

  /** Remove everything below a row: what has sunk into the ground is not seen. */
  clipBelow(row) {
    for (let y = Math.max(0, Math.ceil(row)); y < this.h; y++) for (let x = 0; x < this.w; x++) {
      const i = y * this.w + x;
      if (this.m[i] && !this.mats[this.m[i] - 1].soft) { this.m[i] = 0; this.z[i] = -1e9; }
    }
    return this;
  }

  /** The highest and lowest rows with anything on them. */
  bounds() {
    const { w, h, m } = this;
    let top = h, bottom = -1, left = w, right = -1;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const k = m[y * w + x];
      if (!k || this.mats[k - 1].soft) continue;
      if (y < top) top = y; if (y > bottom) bottom = y; if (x < left) left = x; if (x > right) right = x;
    }
    return { top, bottom, left, right };
  }

  toCanvas() {
    if (!this.out) this.finish();
    const canvas = document.createElement("canvas");
    canvas.width = this.w; canvas.height = this.h;
    canvas.getContext("2d").putImageData(new ImageData(new Uint8ClampedArray(this.out.buffer), this.w, this.h), 0, 0);
    return canvas;
  }
}

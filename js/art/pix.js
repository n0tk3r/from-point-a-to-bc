// A small pixel renderer for sprites.
//
// Characters and props are not stored as pictures. They are described as simple
// solid shapes (limbs, balls, flat panels), and this file turns those shapes into
// pixel art: hard edges, no smoothing, and four tones per material instead of
// gradients. Because the pixels are worked out at whatever size is asked for, a
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

function toneOf(nx, ny, nz, material) {
  const d = nx * LX + ny * LY + nz * LZ + (material.lift || 0);
  return d > 0.74 ? 0 : d > 0.22 ? 1 : d > -0.28 ? 2 : 3;
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
      the way a loose shirt hangs over whatever is under it. */
  limb(ax, ay, az, bx, by, bz, ra, rb, material, o = {}) {
    const x0 = Math.max(0, Math.floor(Math.min(ax - ra, bx - rb))), x1 = Math.min(this.w - 1, Math.ceil(Math.max(ax + ra, bx + rb)));
    const y0 = Math.max(0, Math.floor(Math.min(ay - ra, by - rb))), y1 = Math.min(this.h - 1, Math.ceil(Math.max(ay + ra, by + rb)));
    const abx = bx - ax, aby = by - ay, len2 = abx * abx + aby * aby;
    const mi = this.mat(material), part = o.part || 0, fn = o.fn, flat = o.flatten || 1, bias = o.bias || 0, deep = o.depth || 1, square = o.squareEnd, squareA = o.squareStart, over = o.over;
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
        const i = y * this.w + x;
        if (z <= this.z[i]) {
          const slack = over && over[this.p[i]];
          if (!slack || z + slack <= this.z[i]) continue;
          z = this.z[i] + 0.02;                                  // resting on the thing it covers
        }
        let use = material, mm = mi;
        if (fn) {
          const alt = fn(t, dx / r, dy / r, x, y);
          if (alt === null) continue;
          if (alt) { use = alt; mm = this.mat(alt); }
        }
        const nx = dx / r, ny = dy / r, nz = (up / r) * flat, inv = 1 / Math.hypot(nx, ny, nz);
        this.z[i] = z; this.m[i] = mm; this.p[i] = part;
        this.t[i] = use.flat != null ? use.flat : toneOf(nx * inv, ny * inv, nz * inv, use);
      }
    }
  }

  /** A ball or egg shape. rz is how far it bulges toward the viewer. */
  ball(cx, cy, cz, rx, ry, rz, material, o = {}) {
    const x0 = Math.max(0, Math.floor(cx - rx)), x1 = Math.min(this.w - 1, Math.ceil(cx + rx));
    const y0 = Math.max(0, Math.floor(cy - ry)), y1 = Math.min(this.h - 1, Math.ceil(cy + ry));
    const mi = this.mat(material), part = o.part || 0, fn = o.fn, bias = o.bias || 0;
    for (let y = y0; y <= y1; y++) {
      for (let x = x0; x <= x1; x++) {
        const ux = (x + 0.5 - cx) / rx, uy = (y + 0.5 - cy) / ry, q = ux * ux + uy * uy;
        if (q > 1) continue;
        const uz = Math.sqrt(1 - q);
        const z = cz + uz * rz + bias;
        const i = y * this.w + x;
        if (z <= this.z[i]) continue;
        let use = material, mm = mi;
        if (fn) {
          const alt = fn(ux, uy, uz, x, y);
          if (alt === null) continue;
          if (alt) { use = alt; mm = this.mat(alt); }
        }
        const nx = ux / rx, ny = uy / ry, nz = uz / rz, inv = 1 / Math.hypot(nx, ny, nz);
        this.z[i] = z; this.m[i] = mm; this.p[i] = part;
        this.t[i] = use.flat != null ? use.flat : toneOf(nx * inv, ny * inv, nz * inv, use);
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

  /** Turn shapes into the finished picture.
      edge: darken the outline so the figure reads against any backdrop.
      contact: a thin shadow where a nearer part overlaps a farther one.
      seams(a, b, below, x, y): say which neighboring parts should always show a line between them.
      a is the part on the left and b the one on its right; when `below` is true, a is above b.
      x, y is the pixel that would be darkened (the right-hand or lower one). */
  finish({ edge = true, contact = true, gap = 1.6, seams = null } = {}) {
    const { w, h, m, t, z, p, mats } = this, n = w * h;
    const out = new Uint32Array(n);
    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const i = y * w + x;
        if (!m[i]) continue;
        const material = mats[m[i] - 1];
        let tone = t[i];
        if (!material.soft) {
          const solid = (j) => m[j] !== 0 && !mats[m[j] - 1].soft;
          const L = x > 0 && solid(i - 1), R = x < w - 1 && solid(i + 1), U = y > 0 && solid(i - w), D = y < h - 1 && solid(i + w);
          if (edge) {
            if (!R || !D) tone = 3;                               // the shadow side gets a dark line
            else if (!L || !U) tone = Math.max(tone, 2);          // the lit side a softer one
          }
          if (contact && tone < 3) {
            if ((L && p[i - 1] !== p[i] && z[i - 1] - z[i] > gap) || (U && p[i - w] !== p[i] && z[i - w] - z[i] > gap)) tone++;
            else if (seams && ((L && p[i - 1] !== p[i] && seams(p[i - 1], p[i], false, x, y)) || (U && p[i - w] !== p[i] && seams(p[i - w], p[i], true, x, y)))) tone++;   // two parts that touch: a line between them
          }
        }
        out[i] = material.tones[tone];
      }
    }
    for (const [x, y, color, part] of this.stamps) {
      if (x < 0 || y < 0 || x >= w || y >= h) continue;
      const i = y * w + x;
      if (part !== null && p[i] !== part) continue;
      if (part === null && !m[i]) continue;
      out[i] = color;
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

// Depth and walking.
//
// The stage is flat, but a scene is not: the ground runs away from the viewer up
// to the horizon. Three things sell that depth, and they all come from one number,
// how far a point is below the horizon line:
//
//   1. SIZE.  A figure's size is proportional to how far its feet are below the
//      horizon. Near the bottom of the screen it is large; near the horizon, tiny.
//   2. ORDER. Whatever stands lower on the screen is nearer, so it is drawn in
//      front. (The cast layer does the sorting; see cast.js.)
//   3. PACE.  A step covers fewer screen pixels the farther away it is taken, and
//      moving "into" the picture covers more ground than moving across it.
//
// This file also knows where the lead may walk. A scene gives a walkable outline
// and each prop or painted cut-out gives a footprint; the lead cannot stand in a
// footprint, and when something is in the way a route is found around it.
//
// Every number here is in picture pixels (see grid.js).

import { W, H } from "./grid.js";

/** Moving one pixel up or down the screen covers this many times the ground of one pixel sideways. */
export const DEPTH = 2.2;

/** How big a figure is with its feet at height y. 1 is full size. */
export function scaleAt(scene, y) {
  const horizon = scene.horizon ?? 260, full = scene.full ?? 590;
  const k = (y - horizon) / (full - horizon);
  return Math.min(scene.maxScale ?? 1.12, Math.max(scene.minScale ?? 0.26, k));
}

// Where a figure may stand is kept for every pixel. Routes are searched on a coarser grid of
// squares STEP pixels wide (160 by 120 of them), which is fine enough and keeps a search short.
const STEP = 5, GW = W / STEP, GH = H / STEP;

/** Call fill(y, from, to) for each run of pixels inside an outline, row by row. Much quicker than asking about every pixel in turn. */
function rows(poly, fill) {
  let y0 = Infinity, y1 = -Infinity;
  for (const [, y] of poly) { y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
  for (let y = Math.max(0, Math.floor(y0)); y <= Math.min(H - 1, Math.ceil(y1)); y++) {
    const py = y + 0.5, xs = [];
    for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
      const xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
      if ((yi > py) !== (yj > py)) xs.push(xi + ((py - yi) / (yj - yi)) * (xj - xi));
    }
    xs.sort((a, b) => a - b);
    for (let k = 0; k + 1 < xs.length; k += 2) {
      const from = Math.max(0, Math.ceil(xs[k] - 0.5)), to = Math.min(W - 1, Math.ceil(xs[k + 1] - 0.5) - 1);   // a pixel counts when its middle is inside
      if (from <= to) fill(y, from, to);
    }
  }
}

export class WalkMap {
  /**
   * scene.walk is { area: [[x, y], ...] } (an outline) or { x: [min, max], y: [min, max] } (a box).
   * blocked is a list of outlines nobody can stand in: the footprints of props and cut-outs, seated people, water.
   */
  constructor(scene, blocked = []) {
    const walk = scene.walk || { x: [0, W], y: [290, 595] };          // with nothing said: the lower half of the picture
    const area = walk.area || [[walk.x[0], walk.y[0]], [walk.x[1], walk.y[0]], [walk.x[1], walk.y[1]], [walk.x[0], walk.y[1]]];
    const ok = (this.ok_ = new Uint8Array(W * H));
    rows(area, (y, from, to) => ok.fill(1, y * W + from, y * W + to + 1));
    // A figure has some width, so keep its center a little way off every obstacle.
    const mx = walk.margin ? walk.margin[0] : 12, my = walk.margin ? walk.margin[1] : 5;
    for (const poly of blocked) {
      rows(poly, (y, from, to) => {
        const a = Math.max(0, from - mx), b = Math.min(W - 1, to + mx);
        for (let yy = Math.max(0, y - my); yy <= Math.min(H - 1, y + my); yy++) ok.fill(0, yy * W + a, yy * W + b + 1);
      });
    }
  }

  /** May a figure stand here? */
  ok(x, y) {
    const xi = Math.floor(x), yi = Math.floor(y);
    return xi >= 0 && yi >= 0 && xi < W && yi < H && this.ok_[yi * W + xi] === 1;
  }

  /** The closest place a figure may stand. (Up and down the screen counts for more than sideways: see DEPTH.) */
  nearest(x, y) {
    if (this.ok(x, y)) return [x, y];
    const xi = Math.round(x), yi = Math.round(y), from = Math.min(W - 1, Math.max(0, xi));
    let best = null, bestD = Infinity;
    // Row by row, outward from the row asked for. In each row only two places can be the nearest: the first
    // one to the left and the first to the right. Stop once a row is too far up or down to hold anything nearer.
    for (let dy = 0, far = 0; far < bestD; dy++, far = dy * dy * DEPTH * DEPTH) {
      if (yi - dy < 0 && yi + dy >= H) break;                                  // off both ends of the picture
      for (const yy of dy ? [yi - dy, yi + dy] : [yi]) {
        if (yy < 0 || yy >= H) continue;
        const row = this.ok_.subarray(yy * W, (yy + 1) * W);
        for (const xx of [row.lastIndexOf(1, from), row.indexOf(1, from)]) {
          const d = (xx - xi) * (xx - xi) + far;
          if (xx >= 0 && d < bestD) { bestD = d; best = [xx + 0.5, yy + 0.5]; }
        }
      }
    }
    return best || [x, y];
  }

  /**
   * Where to walk to leave by an edge of the picture (edges.js): the floor nearest a click at (x, y), pushed as far
   * toward that edge as the floor goes. For "N", the column nearest x that has floor in it, and in that column the
   * floor nearest the top; for "S", the floor nearest the bottom. For "W" and "E", the floor nearest the click, and in
   * its row the floor nearest the left or the right. (A click at the side is often level with the far edge of the floor,
   * where the floor stops well short of the side: the nearest floor is then lower down, close to the side.)
   * Null if there is no floor at all.
   */
  toward(side, x, y) {
    if (side === "W" || side === "E") {
      const near = this.nearest(x, y);
      if (!this.ok(near[0], near[1])) return null;
      const row = Math.floor(near[1]), line = this.ok_.subarray(row * W, (row + 1) * W);
      const end = side === "W" ? line.indexOf(1) : line.lastIndexOf(1);
      return [end + 0.5, row + 0.5];
    }
    const from = Math.min(W - 1, Math.max(0, Math.round(x))), top = side === "N";
    for (let k = 0; k < W; k++) {
      for (const c of k ? [from - k, from + k] : [from]) {
        if (c < 0 || c >= W) continue;
        for (let d = top ? 0 : H - 1; d >= 0 && d < H; d += top ? 1 : -1) if (this.ok_[d * W + c]) return [c + 0.5, d + 0.5];
      }
    }
    return null;
  }

  /** Is the straight line from a to b free of obstacles? */
  clear(a, b) {
    const n = Math.max(1, Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1])));
    for (let i = 0; i <= n; i++) if (!this.ok(a[0] + ((b[0] - a[0]) * i) / n, a[1] + ((b[1] - a[1]) * i) / n)) return false;
    return true;
  }

  /** A route from one place to another, as a short list of points to walk through in turn. */
  path(from, to) {
    const a = this.nearest(from[0], from[1]), b = this.nearest(to[0], to[1]);
    if (this.clear(a, b)) return [b];
    // A* over a coarse grid. Moving up or down the screen costs more, as it covers more ground.
    const cell = (p) => [Math.min(GW - 1, Math.max(0, Math.floor(p[0] / STEP))), Math.min(GH - 1, Math.max(0, Math.floor(p[1] / STEP)))];
    const mid = STEP / 2;                              // a square is free when its middle is
    const free = (cx, cy) => cx >= 0 && cy >= 0 && cx < GW && cy < GH && this.ok(cx * STEP + mid, cy * STEP + mid);
    let [sx, sy] = cell(a), [tx, ty] = cell(b);
    const snap = (cx, cy) => { if (free(cx, cy)) return [cx, cy]; for (let r = 1; r < 6; r++) for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) if (free(cx + dx, cy + dy)) return [cx + dx, cy + dy]; return [cx, cy]; };
    [sx, sy] = snap(sx, sy); [tx, ty] = snap(tx, ty);
    const n = GW * GH, cost = new Float32Array(n).fill(Infinity), came = new Int32Array(n).fill(-1), done = new Uint8Array(n);
    const guess = (cx, cy) => Math.hypot(cx - tx, (cy - ty) * DEPTH);
    const heap = [];                                   // a small binary heap of [priority, cell]
    const push = (f, i) => { heap.push([f, i]); let k = heap.length - 1; while (k > 0) { const p = (k - 1) >> 1; if (heap[p][0] <= heap[k][0]) break; [heap[p], heap[k]] = [heap[k], heap[p]]; k = p; } };
    const pop = () => { const top = heap[0], last = heap.pop(); if (heap.length) { heap[0] = last; let k = 0; for (;;) { const l = k * 2 + 1, r = l + 1; let m = k; if (l < heap.length && heap[l][0] < heap[m][0]) m = l; if (r < heap.length && heap[r][0] < heap[m][0]) m = r; if (m === k) break; [heap[m], heap[k]] = [heap[k], heap[m]]; k = m; } } return top; };
    const start = sy * GW + sx, goal = ty * GW + tx;
    cost[start] = 0; push(guess(sx, sy), start);
    while (heap.length) {
      const [, i] = pop();
      if (done[i]) continue;
      done[i] = 1;
      if (i === goal) break;
      const cx = i % GW, cy = (i / GW) | 0;
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
        if (!dx && !dy) continue;
        const nx = cx + dx, ny = cy + dy;
        if (!free(nx, ny)) continue;
        if (dx && dy && (!free(cx + dx, cy) || !free(cx, cy + dy))) continue;          // no squeezing past corners
        const j = ny * GW + nx, c = cost[i] + Math.hypot(dx, dy * DEPTH);
        if (c < cost[j]) { cost[j] = c; came[j] = i; push(c + guess(nx, ny), j); }
      }
    }
    if (came[goal] < 0 && goal !== start) return [a];   // no way through: stay put
    const cells = [];
    for (let i = goal; i >= 0 && i !== start; i = came[i]) cells.push([(i % GW) * STEP + mid, ((i / GW) | 0) * STEP + mid]);
    cells.reverse();
    cells.push(b);
    // Pull the route tight: from each point, head straight for the farthest point that can be seen.
    const out = [];
    let at = a, k = 0;
    while (k < cells.length) {
      let far = k;
      for (let j = cells.length - 1; j > k; j--) if (this.clear(at, cells[j])) { far = j; break; }
      out.push(cells[far]);
      at = cells[far];
      k = far + 1;
    }
    return out;
  }
}

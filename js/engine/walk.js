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
// and each prop gives a footprint; the lead cannot stand in a footprint, and when
// something is in the way a route is found around it.

/** Moving one pixel up or down the screen covers this many times the ground of one pixel sideways. */
export const DEPTH = 2.2;

/** How big a figure is with its feet at height y. 1 is full size. */
export function scaleAt(scene, y) {
  const horizon = scene.horizon ?? 118, full = scene.full ?? 190;
  const k = (y - horizon) / (full - horizon);
  return Math.min(scene.maxScale ?? 1.12, Math.max(scene.minScale ?? 0.26, k));
}

const inside = (poly, x, y) => {
  let hit = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
    if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) hit = !hit;
  }
  return hit;
};

const W = 320, H = 200, STEP = 2, GW = W / STEP, GH = H / STEP;

export class WalkMap {
  /**
   * scene.walk is { area: [[x, y], ...] } (an outline) or { x: [min, max], y: [min, max] } (a box).
   * blocked is a list of outlines nobody can stand in: prop footprints, seated people, water.
   */
  constructor(scene, blocked = []) {
    const walk = scene.walk || { x: [0, 320], y: [130, 198] };
    const area = walk.area || [[walk.x[0], walk.y[0]], [walk.x[1], walk.y[0]], [walk.x[1], walk.y[1]], [walk.x[0], walk.y[1]]];
    const solid = new Uint8Array(W * H);
    for (const poly of blocked) {
      let x0 = W, x1 = 0, y0 = H, y1 = 0;
      for (const [x, y] of poly) { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); }
      for (let y = Math.max(0, Math.floor(y0)); y <= Math.min(H - 1, Math.ceil(y1)); y++)
        for (let x = Math.max(0, Math.floor(x0)); x <= Math.min(W - 1, Math.ceil(x1)); x++)
          if (inside(poly, x + 0.5, y + 0.5)) solid[y * W + x] = 1;
    }
    // A figure has some width, so keep its center a little way off every obstacle.
    const mx = walk.margin ? walk.margin[0] : 5, my = walk.margin ? walk.margin[1] : 2;
    const ok = (this.ok_ = new Uint8Array(W * H));
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (inside(area, x + 0.5, y + 0.5)) ok[y * W + x] = 1;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      if (!solid[y * W + x]) continue;
      for (let dy = -my; dy <= my; dy++) for (let dx = -mx; dx <= mx; dx++) {
        const xx = x + dx, yy = y + dy;
        if (xx >= 0 && yy >= 0 && xx < W && yy < H) ok[yy * W + xx] = 0;
      }
    }
  }

  /** May a figure stand here? */
  ok(x, y) {
    const xi = Math.floor(x), yi = Math.floor(y);
    return xi >= 0 && yi >= 0 && xi < W && yi < H && this.ok_[yi * W + xi] === 1;
  }

  /** The closest place a figure may stand. */
  nearest(x, y) {
    if (this.ok(x, y)) return [x, y];
    let best = null, bestD = Infinity;
    const xi = Math.round(x), yi = Math.round(y);
    for (let r = 1; r < 200 && (best === null || r * r < bestD + 4); r++) {
      for (let dy = -r; dy <= r; dy++) for (let dx = -r; dx <= r; dx++) {
        if (Math.max(Math.abs(dx), Math.abs(dy)) !== r) continue;
        const xx = xi + dx, yy = yi + dy;
        if (!this.ok(xx, yy)) continue;
        const d = dx * dx + dy * dy * DEPTH * DEPTH;
        if (d < bestD) { bestD = d; best = [xx + 0.5, yy + 0.5]; }
      }
    }
    return best || [x, y];
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
    const free = (cx, cy) => cx >= 0 && cy >= 0 && cx < GW && cy < GH && this.ok(cx * STEP + 1, cy * STEP + 1);
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
    for (let i = goal; i >= 0 && i !== start; i = came[i]) cells.push([(i % GW) * STEP + 1, ((i / GW) | 0) * STEP + 1]);
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

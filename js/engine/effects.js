// Things that move by nature: smoke, flames and embers, water, birds, and cloth that stirs in the air.
//
// The author: "any statically drawn thing that naturally moves can break the illusion of the reality we're trying to
// create". So nothing that moves by itself in the world is painted still. The painter leaves it out of the picture (or
// takes it out), marks where it goes, and the scene lists it under `fx`; this file draws it, moving:
//
//   smoke     soft puffs that rise from a point, drift with the air, widen and fade
//   flame     a flickering tongue of flame with a soft glow round it: a lamp, a candle, a torch, a brazier
//   embers    a bed of coals that glows and breathes, and now and then lets a spark go
//   ripples   rings that spread and fade on still water (a donkey drinking, a drip)
//   stream    water running along a path (a spout into a basin), with light running down it and a splash where it lands
//   shimmer   light moving on a water surface, inside a shape (a river, a basin): very quiet
//   birds     flyers that cross the sky now and then, or wheel in it; or a flock on the ground or along a ledge that
//             pecks and potters and goes up when somebody comes near, and comes back later
//   sway      a painted cut-out (washing on a line, a streamer, a palm's crown) stirring in the air from a fixed edge
//   portal    the door in time: a ripple in the paint. The painting itself bends in rings spreading from the door's
//             middle, as if a stone had been dropped in it; nothing is drawn over it (round ten: see `Portal` below)
//
// Every one is drawn on the cast layer among the people (cast.js), at a depth of its own, given as for a cut-out:
// `base` (a row, or a line) or `plane`. A man who walks behind an altar walks behind its smoke. And every one:
//   - runs on the game clock. Its time is the scene's own: it stops while the game is paused, and starts again with it.
//   - is cheap. Its picture changes only as often as its motion needs (a bird thirty times a second, smoke twenty, a
//     flame fifteen, a sway six, light on water five); it is cut to the box it can reach, and the cast repaints only
//     that box (Cast.update). In any one frame only a few of them may change (Effects.budget), so the cast repaints
//     patches and never the whole layer. A busy scene has a couple of hundred specks of smoke, light and water in all.
//   - is quieter for players who asked for less motion: slower and smaller, and no birds flapping up.
//   - is never clickable (the cast layer takes no clicks, and nothing here has a clickable area) and never outlined
//     by Show (its ids on the stage begin "fx:", and no clickable area names one).
//   - is seeded. What it does at a moment of the scene's time is worked out from its seed and that time alone, so a
//     scene opened twice looks the same at the same moment. (Birds that somebody has startled are the exception:
//     what they do depends on where people walked.)
//
// The format, every field and its default, with examples: docs/DESIGN.md, "Things that move by nature" (section 2).
// A script reaches them through g.effects: g.effects.get("altar-smoke").show(false), g.effects.add({ type: "flame", ... }).

import * as castKit from "./cast.js";
import { picture as fetchPicture, got } from "./assets.js";
import { scaleAt, DEPTH } from "./walk.js";
import { W, H } from "./grid.js";
import { keyHex, keyId } from "../art/look.js";

const { Figure, Cutout } = castKit;
const TICK = 1000 / 30;                      // the finest step anything here moves by: thirty times a second
const TAU = Math.PI * 2;

// ---------------------------------------------------------------- numbers that are the same every time
const mix = (h, k) => { k = Math.imul(k | 0, 0xcc9e2d51); k = (k << 15) | (k >>> 17); k = Math.imul(k, 0x1b873593); h ^= k; h = (h << 13) | (h >>> 19); return (Math.imul(h, 5) + 0xe6546b64) | 0; };
/** A number from 0 to 1 that depends only on what it is given (whole numbers): the same answer every time it is asked. */
export function rnd(seed, a = 0, b = 0, c = 0) {
  let h = mix(mix(mix(0x9e3779b9 ^ seed, a), b), c);
  h ^= h >>> 16; h = Math.imul(h, 0x85ebca6b); h ^= h >>> 13; h = Math.imul(h, 0xc2b2ae35); h ^= h >>> 16;
  return (h >>> 0) / 4294967296;
}
/** A run of numbers from 0 to 1, from a seed: the same run every time. */
function sequence(seed) {
  let s = seed >>> 0;
  return () => { s = (s + 0x6d2b79f5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
function hashOf(text) { let h = 0x811c9dc5; for (let i = 0; i < text.length; i++) { h ^= text.charCodeAt(i); h = Math.imul(h, 0x01000193); } return h >>> 0; }
/** Smooth noise from -1 to 1 along t: a value at each whole step of t, eased between. */
function wobble(seed, t, lane = 0) {
  const i = Math.floor(t), f = t - i, e = f * f * (3 - 2 * f), a = rnd(seed, i, lane) * 2 - 1, b = rnd(seed, i + 1, lane) * 2 - 1;
  return a + (b - a) * e;
}
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const ease = (a, b, v) => { const k = clamp((v - a) / (b - a)); return k * k * (3 - 2 * k); };
// A painter's mark can carry words where a number goes ("wind": "from the left"): those count as not given.
const num = (v, d) => (typeof v === "number" && Number.isFinite(v) ? v : d);
const isPair = (v) => Array.isArray(v) && v.length === 2 && typeof v[0] === "number" && typeof v[1] === "number";
/** A number or a range [low, high] read at r (0 to 1). */
const within = (v, r) => (isPair(v) ? v[0] + (v[1] - v[0]) * r : v);
const isPoint = (p) => Array.isArray(p) && p.length >= 2 && typeof p[0] === "number" && typeof p[1] === "number";
const isPoly = (p) => Array.isArray(p) && p.length >= 3 && p.every(isPoint);

/** A shape given as a poly ([[x, y], ...]), a rect ([x, y, w, h]) or a circle ([x, y, r]), as a poly. */
function polyOf(shape) {
  if (isPoly(shape)) return shape;
  if (Array.isArray(shape) && shape.length === 4 && shape.every((v) => typeof v === "number")) { const [x, y, w, h] = shape; return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]; }
  if (Array.isArray(shape) && shape.length === 3 && shape.every((v) => typeof v === "number")) { const [x, y, r] = shape; return Array.from({ length: 16 }, (_, i) => [x + Math.cos((i / 16) * TAU) * r, y + Math.sin((i / 16) * TAU) * r]); }
  return null;
}
/** One shape or a list of shapes, as a list of polys. */
const polysOf = (v) => (!Array.isArray(v) ? [] : polyOf(v) ? [polyOf(v)] : v.map(polyOf).filter(Boolean));
function inside(poly, x, y) {
  let hit = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, yi] = poly[i], [xj, yj] = poly[j];
    if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) hit = !hit;
  }
  return hit;
}
const areaOf = (poly) => Math.abs(poly.reduce((s, [x, y], i) => { const [x2, y2] = poly[(i + 1) % poly.length]; return s + x * y2 - x2 * y; }, 0)) / 2;
const boxOf = (points) => [Math.min(...points.map((p) => p[0])), Math.min(...points.map((p) => p[1])), Math.max(...points.map((p) => p[0])), Math.max(...points.map((p) => p[1]))];

/** A smooth line through the points (Catmull-Rom), as points about `every` pixels apart, each with its distance along: [x, y, s]. */
function smoothLine(points, every = 2) {
  const pts = (points || []).filter(isPoint);
  if (pts.length < 2) return pts.map(([x, y]) => [x, y, 0]);
  const P = (i) => pts[Math.max(0, Math.min(pts.length - 1, i))], out = [[pts[0][0], pts[0][1], 0]];
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = P(i - 1), p1 = P(i), p2 = P(i + 1), p3 = P(i + 2), n = Math.max(1, Math.ceil(Math.hypot(p2[0] - p1[0], p2[1] - p1[1]) / every));
    for (let s = 1; s <= n; s++) {
      const u = s / n, u2 = u * u, u3 = u2 * u, at = (k) => 0.5 * (2 * p1[k] + (p2[k] - p0[k]) * u + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * u2 + (3 * p1[k] - p0[k] - 3 * p2[k] + p3[k]) * u3);
      const x = at(0), y = at(1), last = out[out.length - 1];
      out.push([x, y, last[2] + Math.hypot(x - last[0], y - last[1])]);
    }
  }
  return out;
}
/** The point at distance s along a line made by smoothLine, and which way the line runs there: [x, y, dx, dy]. */
function along(line, s) {
  const n = line.length;
  if (n === 1) return [line[0][0], line[0][1], 1, 0];
  s = clamp(s, 0, line[n - 1][2]);
  let lo = 0, hi = n - 1;
  while (hi - lo > 1) { const m = (lo + hi) >> 1; if (line[m][2] <= s) lo = m; else hi = m; }
  const a = line[lo], b = line[hi], f = b[2] > a[2] ? (s - a[2]) / (b[2] - a[2]) : 0;
  return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, b[0] - a[0], b[1] - a[1]];
}

// ---------------------------------------------------------------- colours and canvases
let probe = null;
/** Any CSS colour as [r, g, b], 0 to 255. */
function rgbOf(color, fallback = [255, 255, 255]) {
  if (typeof color !== "string") return fallback;
  probe = probe || document.createElement("canvas").getContext("2d");
  probe.fillStyle = "#010203"; probe.fillStyle = color;
  const v = probe.fillStyle;
  if (v === "#010203" && color.replace(/\s/g, "").toLowerCase() !== "#010203") return fallback;      // not a colour
  if (v[0] === "#") return [1, 3, 5].map((i) => parseInt(v.slice(i, i + 2), 16));
  const m = v.match(/[\d.]+/g);
  return m ? m.slice(0, 3).map(Number) : fallback;
}
const rgba = ([r, g, b], a) => `rgba(${r | 0},${g | 0},${b | 0},${clamp(a).toFixed(3)})`;
const between = (a, b, k) => [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k];
function canvasOf(w, h) { const c = document.createElement("canvas"); c.width = Math.max(1, Math.ceil(w)); c.height = Math.max(1, Math.ceil(h)); return c; }

/**
 * Two canvases, drawn into in turn. The cast tells one picture from the next by its canvas (cast.js, Cast.update): a
 * new picture drawn into the canvas it already has would look like no change at all, and would not be painted.
 */
class Pair {
  constructor(w, h) { this.list = [canvasOf(w, h), canvasOf(w, h)]; this.i = 0; this.w = this.list[0].width; this.h = this.list[0].height; }
  get canvas() { return this.list[this.i]; }
  /** The other canvas, wiped, to draw the next picture on. */
  next() {
    this.i ^= 1;
    const ctx = this.list[this.i].getContext("2d");
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = "source-over"; ctx.setLineDash([]);
    ctx.clearRect(0, 0, this.w, this.h);
    return ctx;
  }
}

// Soft puffs for smoke, three to a colour, 32 pixels across: a little ragged, and grained like the paint. Made once and kept.
const puffs = new Map();
function puffsOf(color) {
  let list = puffs.get(color);
  if (list) return list;
  const [r, g, b] = rgbOf(color, [217, 213, 205]), N = 32;
  list = [0, 1, 2].map((v) => {
    const c = canvasOf(N, N), ctx = c.getContext("2d"), img = ctx.createImageData(N, N), d = img.data;
    const lumps = [[0, 0, 0.72]].concat([0, 1, 2].map((j) => { const a = rnd(91 + v, j) * TAU, o = 0.14 + rnd(91 + v, j, 1) * 0.14; return [Math.cos(a) * o, Math.sin(a) * o, 0.5 + rnd(91 + v, j, 2) * 0.18]; }));
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
      const px = ((x + 0.5) / N) * 2 - 1, py = ((y + 0.5) / N) * 2 - 1;
      let a = 0;
      for (const [lx, ly, lr] of lumps) { const q = ((px - lx) ** 2 + (py - ly) ** 2) / (lr * lr); if (q < 1) a = Math.max(a, (1 - q) * (1 - q)); }
      a *= 0.84 + 0.32 * rnd(7 + v, x, y);
      const i = (y * N + x) * 4;
      d[i] = r; d[i + 1] = g; d[i + 2] = b; d[i + 3] = Math.round(clamp(a) * 255);
    }
    ctx.putImageData(img, 0, 0);
    return c;
  });
  puffs.set(color, list);
  return list;
}

// ---------------------------------------------------------------- on the stage
// The fields the cast reads from anything on the stage. cast.js lends its own Sprite when it exports it; until then, the same here.
const Sprite = castKit.Sprite || class {
  constructor(id) { this.id = id; this.x = 0; this.y = 0; this.scale = 1; this.opacity = 1; this.plane = "floor"; this.base = null; this.hidden = false; this.flags = {}; }
  place(x, y, scale = this.scale) { this.x = x; this.y = y; this.scale = scale; return this; }
  fade(opacity) { this.opacity = opacity; return this; }
  flag(name, on) { this.flags[name] = on; return this; }
  face() { return this; }
  get h() { return 0; }
  baseAt(x) {
    const base = this.base;
    if (base == null) return this.y;
    if (typeof base === "number") return base;
    const [[x1, y1], [x2, y2]] = base, t = x2 === x1 ? 0.5 : Math.min(1, Math.max(0, (x - x1) / (x2 - x1)));
    return y1 + (y2 - y1) * t;
  }
  get mid() { return Array.isArray(this.base) ? (this.base[0][0] + this.base[1][0]) / 2 : this.x; }
  tick() {}
};

/** One moving thing on the cast layer (a column of smoke, one bird). Its effect says what it looks like. */
class Mote extends Sprite {
  constructor(id, effect) { super(id); this.fx = effect; this.want = false; this.waits = 0; this.urgent = false; }
  get h() { return 0; }                         // (not a head for spoken words to keep clear of: dialogue.js)
  picture(palette, calm) { return this.fx.picture(this, calm); }
  /** Its picture may change this frame (see Effects.frame, the budget). */
  grant() { this.want = false; this.fx.grant(this); }
}
/** A canvas's own number, to tell pictures apart in a few characters. */
const ids = new WeakMap();
let lastId = 0;
const idOf = (canvas) => ids.get(canvas) || (ids.set(canvas, ++lastId), lastId);

// ---------------------------------------------------------------- what every kind has
class Effect {
  constructor(host, spec, n) {
    this.host = host; this.spec = spec; this.type = spec.type;
    this.id = String(spec.id || `${spec.type}-${n + 1}`);
    this.seed = (num(spec.seed, null) ?? hashOf(`${host.place}/${this.id}`)) >>> 0;
    this.k = num(spec.scale, 1);
    this.time = 0;                  // ms of its own time: slower for players who asked for less motion
    this.slow = 0.5;                // how much slower, then
    this.forced = undefined;        // a script's show(true / false); undefined: as `when` says
    this.sprites = [];
    this.shown = false;
    this.plane = "floor";           // where it lies when the scene gives neither base nor plane
    this.drawn = 0;                 // how many specks its last picture had (smoke puffs, glints, drops, coals, birds)
  }
  get game() { return this.host.game; }
  /** A sprite of this effect's, at its depth: `base` (a row or a line) or `plane`; with neither, its own default. */
  mote(suffix = "") {
    const s = new Mote(`fx:${this.id}${suffix}`, this), sp = this.spec, word = typeof sp.base === "string" ? sp.base : null;
    s.plane = sp.plane === "front" || sp.plane === "back" ? sp.plane : word === "front" || word === "back" ? word : sp.base != null && !word ? "floor" : this.plane;
    s.base = sp.base != null && !word ? sp.base : null;
    s.hidden = true;
    this.sprites.push(s);
    return s;
  }
  /** For scripts: show it (true) or take it away (false), whatever its `when` says. auto() hands it back to `when`. */
  show(on = true) { this.forced = !!on; this.host.frame(0); return this; }
  auto() { this.forced = undefined; this.host.frame(0); return this; }
  wanted() { const w = this.spec.when; return this.forced !== undefined ? this.forced : typeof w !== "function" || !!w(this.game); }
  /** Each frame of the game clock, before the cast is painted. */
  advance(dt, calm, people) {
    const on = this.host.on && this.wanted();
    if (on !== this.shown) { this.shown = on; this.reveal(on); }
    if (!on) return;
    this.calm = calm;
    this.time += dt * (calm ? this.slow : 1);
    this.update(calm, people);
  }
  reveal(on) { for (const s of this.sprites) s.hidden = !on; }
  update() {}
  /** What asks for a turn to change its picture each frame (Effects.frame): its sprites. */
  slots() { return this.sprites; }
  grant() {}
  /** Jump to a moment of the scene's time (for tests and for screenshots): what it would be showing had the scene been open that long. */
  seek(ms) { this.time = ms * (this.calm ? this.slow : 1); this.restart(); this.update(!!this.calm, []); if (!this.shown) this.reveal(false); }
  restart() {}
  picture() { return null; }
}

/**
 * A kind that is a picture drawn by code: smoke, a flame, embers, ripples, a stream, shimmer. It is drawn afresh `fps`
 * times a second of its own time, into the other canvas of a pair, and the same picture is handed back in between.
 * `clip`: a shape it is kept inside. `behind`: shapes where it passes behind something painted nearer; it is not drawn
 * there (or only at `behindOpacity`).
 */
class Drawn extends Effect {
  constructor(host, spec, n) { super(host, spec, n); this.fps = 30; this.calmFps = 15; }
  /** The canvas: w by h, with the point `at` of the picture at (ox, oy) on it. */
  setup(w, h, ox, oy, at) {
    ox = Math.round(ox); oy = Math.round(oy);
    const x = Math.round(at[0]), y = Math.round(at[1]);
    this.pair = new Pair(w, h); this.ox = ox; this.oy = oy; this.origin = [x - ox, y - oy];
    this.sprite = this.mote().place(x, y);
    this.step = null;
    const path = (polys) => { if (!polys.length) return null; const p = new Path2D(); for (const poly of polys) { poly.forEach(([px, py], i) => (i ? p.lineTo(px - this.origin[0], py - this.origin[1]) : p.moveTo(px - this.origin[0], py - this.origin[1]))); p.closePath(); } return p; };
    this.clipPath = path(polysOf(this.spec.clip));
    this.behindPath = path(polysOf(this.spec.behind));
    this.behindOpacity = num(this.spec.behindOpacity, 0);
  }
  restart() { this.step = null; }
  /** Its next picture is due when its time has reached another of its steps; it is drawn when its turn comes (grant). */
  update(calm) {
    if (!this.pair || this.step === null) return;
    const fps = calm ? this.calmFps : this.fps;
    this.sprite.want = Math.floor((this.time * fps) / 1000) !== this.step || calm !== this.drawnCalm;
  }
  grant() { this.go = true; }
  picture(sprite, calm) {
    if (!this.pair) return null;
    const fps = calm ? this.calmFps : this.fps, step = Math.floor((this.time * fps) / 1000), go = this.go;
    this.go = false;
    if (this.step === null || (go && (step !== this.step || calm !== this.drawnCalm))) {      // (the first picture at once; after that, in its turn)
      this.step = step; this.drawnCalm = calm;
      const ctx = this.pair.next();
      if (this.clipPath) { ctx.save(); ctx.clip(this.clipPath); }
      this.drawn = 0;
      this.draw(ctx, step / fps, calm);
      if (this.clipPath) ctx.restore();
      if (this.behindPath) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = "destination-out"; ctx.globalAlpha = 1 - this.behindOpacity; ctx.fillStyle = "#000"; ctx.fill(this.behindPath); ctx.restore(); }
    }
    return { canvas: this.pair.canvas, ox: this.ox, oy: this.oy };
  }
}

// ---------------------------------------------------------------- smoke
class Smoke extends Drawn {
  constructor(host, spec, n) {
    super(host, spec, n);
    const s = spec, k = this.k, lean = isPair(s.lean) ? s.lean : null;
    this.rate = num(s.rate, 3);
    this.height = num(s.height, lean ? Math.abs(lean[1]) : 110);
    this.rise = num(s.rise, Math.max(6, this.height / 6));
    const wide = isPair(s.width) ? s.width : [null, num(s.width, 36)];
    this.top = wide[1]; this.foot = wide[0] ?? Math.max(2, this.top * 0.18);
    this.life = (1.6 * this.height) / this.rise;                         // seconds a puff lasts: it starts up at `rise` and stops at `height`
    const sideways = lean ? lean[0] : num(s.lean, null);
    this.wind = sideways != null ? sideways / this.life : num(s.wind, 6);
    this.gust = num(s.gust, 0.35);
    this.alpha = num(s.opacity, 0.32);
    this.tex = puffsOf(typeof s.color === "string" ? s.color : "#d9d5cd");
    this.fps = 20; this.calmFps = 10;
    const r = this.top * 0.62 + 2, drift = Math.abs(this.wind) * (1 + this.gust) * this.life * 1.2, play = 7 + this.foot / 2;
    const left = Math.ceil((r + play + (this.wind < 0 ? drift : 0)) * k) + 2, right = Math.ceil((r + play + (this.wind > 0 ? drift : 0)) * k) + 2;
    const above = Math.ceil((this.height + r + 3) * k) + 2, below = Math.ceil((this.foot + 4) * k) + 2;
    this.setup(left + right, above + below, left, above, s.at);
  }
  draw(ctx, t) {
    const k = this.k, seed = this.seed, rate = this.rate, tex = this.tex, ox = this.ox, oy = this.oy, life0 = this.life;
    const first = Math.floor((t - life0 * 1.2) * rate) - 1, last = Math.ceil(t * rate);
    for (let i = first; i <= last; i++) {
      const born = (i + (rnd(seed, i, 1) - 0.5) * 0.7) / rate, life = life0 * (0.85 + 0.3 * rnd(seed, i, 2)), age = t - born;
      if (age < 0 || age >= life) continue;
      const u = age / life, up = this.height * (1.6 * u - 0.6 * u * u);
      const wind = this.wind * (1 + this.gust * Math.sin(born * 0.5 + (seed % 97)));            // the air as it was when this puff set off: gusts bend the column
      const side = wind * age * Math.sqrt(u) + Math.sin(age * (1.1 + rnd(seed, i, 3) * 0.9) + rnd(seed, i, 4) * TAU) * (0.4 + 5 * u) * Math.min(1, this.top / 20) + (rnd(seed, i, 5) - 0.5) * this.foot * 0.6;
      const r = (this.foot / 2 + (this.top / 2 - this.foot / 2) * Math.pow(u, 0.8)) * (0.8 + 0.4 * rnd(seed, i, 6)) * k + 0.6;
      const a = this.alpha * (0.6 + 0.4 * rnd(seed, i, 7)) * ease(0, Math.min(0.3, life * 0.12), age) * (1 - ease(0.35, 1, u));      // (in at once, out slowly)
      if (a < 0.004) continue;
      ctx.globalAlpha = Math.min(1, a);
      ctx.drawImage(tex[Math.floor(rnd(seed, i, 8) * tex.length)], ox + side * k - r, oy - up * k - r, r * 2, r * 2);
      this.drawn++;
    }
    ctx.globalAlpha = 1;
  }
}

// ---------------------------------------------------------------- flames and embers
/** A tongue of flame standing on (cx, foot): w wide, h tall, its tip `tip` to the side. */
function tongue(ctx, cx, foot, w, h, tip) {
  const r = Math.max(0.5, w / 2), yb = foot - r;
  h = Math.max(h, w * 1.15);
  ctx.beginPath();
  ctx.moveTo(cx + tip, foot - h);
  ctx.bezierCurveTo(cx + tip * 0.35 + r * 0.95, foot - h * 0.55, cx + r, yb - r * 0.6, cx + r, yb);
  ctx.arc(cx, yb, r, 0, Math.PI, false);
  ctx.bezierCurveTo(cx - r, yb - r * 0.6, cx + tip * 0.35 - r * 0.95, foot - h * 0.55, cx + tip, foot - h);
  ctx.closePath();
  ctx.fill();
}

class Flame extends Drawn {
  constructor(host, spec, n) {
    super(host, spec, n);
    const s = spec, k = this.k;
    this.size = num(s.size, num(s.height, 12));
    this.wide = num(s.width, this.size * 0.42);
    this.core = typeof s.color === "string" ? s.color : "#fff0b3";
    this.edge = typeof s.edge === "string" ? s.edge : "#ff9a2e";
    this.glowR = num(s.glow, this.size * 2.2);
    this.glowRgb = rgbOf(s.glowColor, [255, 180, 77]);
    this.glowA = num(s.glowOpacity, 0.22);
    this.flicker = num(s.flicker, 0.5);
    this.lean = num(s.lean, 0);
    this.heart = typeof s.core === "string" ? s.core : "#fffbea";
    this.lull = clamp(num(s.lull, 0));                               // 0: it burns steadily; up to 1: it dies down to nothing now and then (charcoal's little tongues)
    this.fps = 15; this.calmFps = 6; this.slow = 0.4;
    const R = Math.ceil(Math.max(this.glowR, this.size * 1.4) * k) + 2, mid = Math.round(this.size * 0.45 * k);
    this.setup(R * 2, R * 2 + mid, R, R + mid, s.at);                  // a square round the middle of the flame; its foot is `mid` below that
  }
  draw(ctx, t, calm) {
    const k = this.k, seed = this.seed, f = this.flicker * (calm ? 0.35 : 1);
    const n1 = wobble(seed, t * 3.2), n2 = wobble(seed, t * 2.1, 1), n3 = wobble(seed, t * 9.5, 2);
    const cx = this.ox, foot = this.oy, cy = foot - this.size * 0.45 * k;
    const low = this.lull ? clamp((wobble(seed, t * 0.45, 3) + 1) / 2 * (1 + this.lull * 1.6) - this.lull * 1.1) : 1;      // (a slow swell that, with a lull, sometimes sinks to nothing)
    if (this.glowR > 0) {
      const R = this.glowR * k * (1 + 0.06 * f * n1), a = this.glowA * (0.35 + 0.65 * low) * (1 + 0.3 * f * (0.6 * n1 + 0.4 * n3)), grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, R);
      grad.addColorStop(0, rgba(this.glowRgb, a)); grad.addColorStop(0.35, rgba(this.glowRgb, a * 0.5)); grad.addColorStop(1, rgba(this.glowRgb, 0));
      ctx.fillStyle = grad; ctx.fillRect(cx - R, cy - R, R * 2, R * 2);
    }
    if (low < 0.08) { this.drawn = 1; return; }
    const h = this.size * k * low * (1 + f * (0.2 * n1 + 0.12 * n3)), w = this.wide * k * Math.sqrt(low) * (1 + 0.1 * f * n3), tip = (this.lean + f * this.wide * 0.55 * n2) * k;
    ctx.globalAlpha = 0.9; ctx.fillStyle = this.edge; tongue(ctx, cx, foot, w, h, tip);
    ctx.globalAlpha = 0.95; ctx.fillStyle = this.core; tongue(ctx, cx + tip * 0.08, foot - w * 0.1, w * 0.6, h * 0.68, tip * 0.75);
    if (h > 7) { ctx.globalAlpha = 0.9; ctx.fillStyle = this.heart; tongue(ctx, cx, foot - w * 0.14, w * 0.3, h * 0.32, tip * 0.4); }
    ctx.globalAlpha = 1;
    this.drawn = 3;
  }
}

class Embers extends Drawn {
  constructor(host, spec, n) {
    super(host, spec, n);
    const s = spec, k = this.k, bed = polyOf(s.bed) || polyOf(s.poly);
    // the bed: an ellipse round `at` (`size`: half its width and half its depth), or a shape (`bed`, or `poly`)
    let size = isPair(s.size) ? s.size : isPair(s.radius) ? s.radius : [num(s.size, 10), num(s.size, 10) * 0.35];
    let at = isPoint(s.at) ? s.at : null;
    if (bed) { const [x0, y0, x1, y1] = boxOf(bed); at = at || [(x0 + x1) / 2, (y0 + y1) / 2]; size = [Math.max(at[0] - x0, x1 - at[0]), Math.max(at[1] - y0, y1 - at[1])]; }
    if (!at) throw new Error("embers need `at` (or a `bed`)");
    [this.rx, this.ry] = size;
    this.count = Math.round(num(s.count, clamp(this.rx * this.ry * 0.45, 4, 40)));
    this.hot = rgbOf(s.color, [255, 179, 71]); this.cool = rgbOf(s.cool, [122, 29, 8]);
    this.glowR = num(s.glow, Math.min(this.rx * 1.6, bed ? this.ry * 2.4 : Infinity)); this.glowRgb = rgbOf(s.glowColor, [255, 138, 61]); this.glowA = num(s.glowOpacity, 0.2);
    this.breath = num(s.breath, 2.4);
    this.sparks = num(s.sparks, 0.25);
    this.fps = 10; this.calmFps = 5; this.slow = 0.4;
    // where each coal lies, and where the glow swells (several places over a big bed, each in its own time: now one part, now another)
    const spot = (i, lane) => {
      for (let tries = 0; tries < 10; tries++) {
        const a = rnd(this.seed, i, lane + tries * 2) * TAU, r = Math.sqrt(rnd(this.seed, i, lane + 1 + tries * 2));
        const x = at[0] + Math.cos(a) * r * this.rx, y = at[1] + Math.sin(a) * r * this.ry;
        if (!bed || inside(bed, x, y)) return [x - at[0], y - at[1], r];
      }
      return [0, 0, 0];
    };
    this.coals = Array.from({ length: this.count }, (_, i) => spot(i, 100));
    this.blobs = Array.from({ length: Math.max(1, Math.round(num(s.blobs, bed ? 3 : this.rx > 20 ? 2 : 1))) }, (_, i) => (i === 0 && !bed ? [0, 0, 0] : spot(i, 300)));
    const R = Math.ceil((Math.max(this.rx + 3, this.glowR) + (this.blobs.length > 1 ? this.rx : 0)) * k) + 2;
    const above = Math.ceil(Math.max(this.glowR * 0.6 + this.ry, this.sparks > 0 ? 56 : 0, this.ry + 3) * k) + 2, below = Math.ceil(Math.max(this.glowR * 0.6 + this.ry, this.ry + 3) * k) + 2;
    this.setup(R * 2, above + below, R, above, at);
  }
  draw(ctx, t, calm) {
    const k = this.k, seed = this.seed, cx = this.ox, cy = this.oy;
    if (this.glowR > 0) this.blobs.forEach(([bx, by], i) => {
      const breathe = 0.5 + 0.5 * Math.sin((t / (this.breath * (1 + i * 0.37))) * TAU + (seed % 7) + i * 2.1);
      const R = this.glowR * k * (this.blobs.length > 1 ? 0.8 : 1), a = this.glowA * (calm ? 0.85 : this.blobs.length > 1 ? 0.35 + 0.65 * breathe : 0.7 + 0.3 * breathe);
      ctx.save(); ctx.translate(cx + bx * k, cy + by * k); ctx.scale(1, 0.6);
      const grad = ctx.createRadialGradient(0, 0, 0, 0, 0, R);
      grad.addColorStop(0, rgba(this.glowRgb, a)); grad.addColorStop(1, rgba(this.glowRgb, 0));
      ctx.fillStyle = grad; ctx.fillRect(-R, -R, R * 2, R * 2); ctx.restore();
    });
    this.coals.forEach(([dx, dy, rad], i) => {
      const period = this.breath * (0.6 + 0.8 * rnd(seed, i, 3));
      let heat = 0.5 + 0.5 * Math.sin((t / period) * TAU + rnd(seed, i, 4) * TAU);
      heat = clamp(heat * (0.75 + 0.25 * wobble(seed + i, t * 1.7)) * (0.55 + 0.45 * (1 - rad)));           // the middle of the bed runs hotter
      if (calm) heat = 0.3 + heat * 0.4;
      const size = Math.max(1, Math.round((0.8 + 1.4 * rnd(seed, i, 5)) * k));
      ctx.globalAlpha = 0.3 + 0.7 * heat;
      ctx.fillStyle = rgba(between(this.cool, this.hot, heat), 1);
      ctx.fillRect(Math.round(cx + dx * k - size / 2), Math.round(cy + dy * k - size / 2), size, Math.max(1, Math.round(size * 0.8)));
      this.drawn++;
    });
    if (this.sparks > 0 && !calm) {
      const first = Math.floor((t - 1.6) * this.sparks) - 1, last = Math.ceil(t * this.sparks);
      for (let j = first; j <= last; j++) {
        const born = (j + rnd(seed, j, 11) * 0.8) / this.sparks, life = 0.7 + 0.8 * rnd(seed, j, 12), age = t - born;
        if (age < 0 || age >= life) continue;
        const u = age / life, x = cx + (rnd(seed, j, 13) - 0.5) * this.rx * 1.2 * k + Math.sin(age * 5 + j) * 2 * k * u, y = cy - (age * 24 + age * age * 6) * k;
        ctx.globalAlpha = (1 - u) * 0.9; ctx.fillStyle = "#ffd27a"; ctx.fillRect(Math.round(x), Math.round(y), 1, 1);
        this.drawn++;
      }
    }
    ctx.globalAlpha = 1;
  }
}

// ---------------------------------------------------------------- water
class Ripples extends Drawn {
  constructor(host, spec, n) {
    super(host, spec, n);
    const s = spec, k = this.k, radius = isPair(s.radius) ? s.radius : [1, num(s.radius, num(s.size, 16))];
    this.plane = "back";                                                // water on the ground lies under everyone: give a base for water that is raised up (a basin)
    this.every = isPair(s.every) ? s.every : num(s.every, null) ?? [1.5, 4];
    [this.r0, this.r1] = radius;
    this.flat = num(s.flat, num(s.squash, 0.32));
    this.speed = num(s.speed, 13);
    this.rings = Math.max(1, Math.round(num(s.rings, 2)));
    this.rgb = rgbOf(s.color, [255, 255, 255]);
    this.trough = s.trough === false || s.trough === "none" ? null : rgbOf(s.trough, [52, 92, 112]);      // the darker water just inside each ring: it is what makes a ring read on pale water
    this.alpha = num(s.opacity, 0.6);
    this.fps = 20; this.calmFps = 10;
    this.last = (this.r1 - this.r0) / this.speed + 0.3 * this.rings + 0.2;      // seconds a drop's rings take to fade
    const R = Math.ceil(this.r1 * k) + 3, Ry = Math.ceil(this.r1 * this.flat * k) + 4;
    this.setup(R * 2, Ry * 2, R, Ry, s.at);
    this.restart();
  }
  restart() { super.restart(); this.drops = []; this.until = -this.last * 1.5; }
  /** The moments drops fall, from a little before the scene began, worked out as far as t. */
  dropsTill(t) {
    while (this.until <= t) {
      const j = this.drops.length, gap = isPair(this.every) ? within(this.every, rnd(this.seed, j, 21)) : this.every;
      this.until += Math.max(0.05, gap);
      this.drops.push(this.until);
    }
  }
  draw(ctx, t) {
    this.dropsTill(t);
    const k = this.k, cx = this.ox, cy = this.oy, flat = this.flat, span = (this.r1 - this.r0) * k;
    ctx.lineWidth = Math.max(1, k);
    for (let j = this.drops.length - 1; j >= 0; j--) {
      const age = t - this.drops[j];
      if (age < 0) continue;
      if (age > this.last) break;
      for (let ring = 0; ring < this.rings; ring++) {
        const a0 = age - ring * 0.3, max = span * (1 - ring * 0.22);
        if (a0 <= 0) continue;
        const grown = a0 * this.speed * k * (1 - ring * 0.12);
        if (grown >= max) continue;
        const rad = this.r0 * k + grown, a = this.alpha * Math.pow(1 - grown / max, 1.3) * Math.min(1, a0 / 0.08) * (ring ? 0.65 : 1);
        if (rad < 0.8) continue;
        if (this.trough && rad > 2) { ctx.strokeStyle = rgba(this.trough, a * 0.55); ctx.beginPath(); ctx.ellipse(cx, cy + 0.7, rad - 1, Math.max(0.5, (rad - 1) * flat), 0, 0, TAU); ctx.stroke(); }
        ctx.strokeStyle = rgba(this.rgb, a);
        ctx.beginPath(); ctx.ellipse(cx, cy, rad, Math.max(0.5, rad * flat), 0, 0, TAU); ctx.stroke();
        this.drawn++;
      }
      if (age < 0.12 && this.r0 <= 2) { ctx.fillStyle = rgba(this.rgb, this.alpha * (1 - age / 0.12)); ctx.fillRect(cx - 1, cy - 1, 2, 1); }
    }
  }
}

class Stream extends Drawn {
  constructor(host, spec, n) {
    super(host, spec, n);
    const s = spec, k = this.k;
    this.line = smoothLine(s.path, 2);
    if (this.line.length < 2) throw new Error("a stream needs a path of two points or more");
    this.wide = isPair(s.width) ? s.width : [num(s.width, 3), num(s.width, 3)];
    this.color = typeof s.color === "string" ? s.color : "#b9d6e4";
    this.light = typeof s.light === "string" ? s.light : "#f4fbff";
    this.alpha = num(s.opacity, 0.55);
    this.speed = num(s.speed, 55);
    this.splash = num(s.splash, s.splash === false ? 0 : 5);
    this.fps = 20; this.calmFps = 10; this.slow = 0.4;
    const end = this.line[this.line.length - 1], pad = Math.ceil(Math.max(...this.wide) * k + this.splash * 2 * k + 4);
    const [x0, y0, x1, y1] = boxOf(this.line), top = Math.floor(y0) - pad - Math.ceil(this.splash * 2 * k), left = Math.floor(x0) - pad;
    this.setup(Math.ceil(x1) + pad - left, Math.ceil(y1) + pad - top, Math.round(end[0]) - left, Math.round(end[1]) - top, end);
    this.path = new Path2D();
    this.line.forEach(([x, y], i) => (i ? this.path.lineTo(x - this.origin[0], y - this.origin[1]) : this.path.moveTo(x - this.origin[0], y - this.origin[1])));
  }
  draw(ctx, t, calm) {
    const k = this.k, line = this.line, n = line.length, [w0, w1] = this.wide, [ox, oy] = this.origin, seed = this.seed;
    // The water: opaque first (so that where pieces of different widths overlap it is no thicker), then made see-through as a whole.
    ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.strokeStyle = this.color;
    for (let i = 0; i < n - 1; i += 4) {
      const j = Math.min(n - 1, i + 5);
      ctx.lineWidth = Math.max(1, (w0 + (w1 - w0) * (i / (n - 1))) * k);
      ctx.beginPath(); ctx.moveTo(line[i][0] - ox, line[i][1] - oy);
      for (let m = i + 1; m <= j; m++) ctx.lineTo(line[m][0] - ox, line[m][1] - oy);
      ctx.stroke();
    }
    ctx.globalCompositeOperation = "destination-in"; ctx.fillStyle = `rgba(0,0,0,${clamp(this.alpha)})`; ctx.fillRect(0, 0, this.pair.w, this.pair.h);
    ctx.globalCompositeOperation = "source-over";
    // light running down it
    const run = t * this.speed * k;
    ctx.strokeStyle = this.light; ctx.lineWidth = Math.max(1, ((w0 + w1) / 2) * k * 0.45);
    ctx.setLineDash([4 * k, 6 * k, 2 * k, 9 * k]); ctx.lineDashOffset = -run; ctx.globalAlpha = 0.6; ctx.stroke(this.path);
    ctx.setLineDash([2 * k, 11 * k, 5 * k, 14 * k]); ctx.lineDashOffset = -run * 1.23 + 7; ctx.globalAlpha = 0.35; ctx.stroke(this.path);
    ctx.setLineDash([]);
    this.drawn = 2;
    // where it lands: foam, rings, drops
    if (this.splash > 0) {
      const ex = this.ox, ey = this.oy, S = this.splash * k;
      ctx.fillStyle = this.light; ctx.globalAlpha = 0.28 + 0.12 * wobble(seed, t * 6);
      ctx.beginPath(); ctx.ellipse(ex, ey, S * 0.7, S * 0.28, 0, 0, TAU); ctx.fill();
      ctx.strokeStyle = this.light; ctx.lineWidth = 1;
      for (let j = Math.floor(t / 0.45) - 4; j <= Math.floor(t / 0.45); j++) {
        const age = t - j * 0.45, rad = age * 9 * k + 1;
        if (age < 0 || rad > S * 1.8) continue;
        ctx.globalAlpha = 0.5 * (1 - rad / (S * 1.8)); ctx.beginPath(); ctx.ellipse(ex, ey, rad, rad * 0.32, 0, 0, TAU); ctx.stroke();
        this.drawn++;
      }
      if (!calm) for (let j = Math.floor((t - 0.5) * 14) - 1; j <= Math.ceil(t * 14); j++) {
        const born = (j + rnd(seed, j, 31) * 0.9) / 14, age = t - born, life = 0.25 + 0.15 * rnd(seed, j, 32);
        if (age < 0 || age > life) continue;
        const vx = (rnd(seed, j, 33) - 0.5) * 34 * k, vy = -(16 + 22 * rnd(seed, j, 34)) * k;
        ctx.globalAlpha = 0.85 * (1 - age / life); ctx.fillStyle = this.light;
        ctx.fillRect(Math.round(ex + vx * age), Math.round(ey + vy * age + 75 * k * age * age), 1, 1);
        this.drawn++;
      }
    }
    ctx.globalAlpha = 1;
  }
}

class Shimmer extends Drawn {
  constructor(host, spec, n) {
    super(host, spec, n);
    const s = spec, k = this.k;
    this.plane = "back";
    this.area = polyOf(s.poly) || polyOf(s.area) || polyOf(s.rect);
    if (!this.area) throw new Error("shimmer needs a shape: poly, area or rect");
    this.holes = polysOf(s.holes);
    const [x0, y0, x1, y1] = boxOf(this.area).map((v, i) => (i < 2 ? Math.floor(v) : Math.ceil(v)));
    this.box = [x0, y0, x1, y1];
    this.count = Math.round(num(s.count, clamp(areaOf(this.area) / 1100, 5, 50)));
    this.size = num(s.size, 6); this.flow = isPair(s.flow) ? s.flow : [4, 0]; this.life = num(s.life, 1.8);
    this.rgb = rgbOf(s.color, [255, 244, 214]); this.alpha = num(s.opacity, 0.45);
    this.fps = 5; this.calmFps = 3;                                  // (it covers the water: a few pictures a second, the glints coming and going slowly)
    this.setup(x1 - x0 + 1, y1 - y0 + 1, 0, y1 - y0, [x0, y1]);      // placed by its bottom left corner: its own base is the near edge of the water
    if (!this.clipPath) {
      this.clipPath = new Path2D();
      this.area.forEach(([x, y], i) => (i ? this.clipPath.lineTo(x - x0, y - y0) : this.clipPath.moveTo(x - x0, y - y0)));
      this.clipPath.closePath();
    }
  }
  draw(ctx, t, calm) {
    const [x0, y0, x1, y1] = this.box, k = this.k, seed = this.seed, n = calm ? Math.ceil(this.count * 0.6) : this.count;
    for (let i = 0; i < n; i++) {
      const life = this.life * (0.75 + 0.5 * rnd(seed, i, 41)), cycle = life * (1.15 + 0.5 * rnd(seed, i, 42));
      const shifted = t + rnd(seed, i, 43) * cycle, j = Math.floor(shifted / cycle), age = shifted - j * cycle;
      if (age >= life) continue;
      let px = null, py = 0;                                            // a place in the water for this glint, found afresh for each
      for (let tries = 0; tries < 6 && px === null; tries++) {
        const x = x0 + rnd(seed, i, j, 44 + tries * 2) * (x1 - x0), y = y0 + rnd(seed, i, j, 45 + tries * 2) * (y1 - y0);
        if (inside(this.area, x, y) && !this.holes.some((h) => inside(h, x, y))) { px = x; py = y; }
      }
      if (px === null) continue;
      const u = age / life, depth = 0.45 + 0.55 * ((py - y0) / Math.max(1, y1 - y0));
      const x = px + this.flow[0] * age - x0, y = py + this.flow[1] * age - y0;
      if (this.holes.some((h) => inside(h, x + x0, y + y0))) continue;
      const len = Math.max(1, this.size * depth * k * (0.6 + 0.8 * rnd(seed, i, j, 57))), a = this.alpha * Math.pow(Math.sin(Math.PI * u), 1.5);
      ctx.fillStyle = rgba(this.rgb, a * 0.7);
      ctx.fillRect(Math.round(x - len / 2), Math.round(y), Math.round(len), 1);
      if (len >= 3) { ctx.fillStyle = rgba(this.rgb, a); ctx.fillRect(Math.round(x - len / 6), Math.round(y), Math.max(1, Math.round(len / 3)), 1); }
      this.drawn++;
    }
  }
}

// ---------------------------------------------------------------- cloth in the air
/**
 * Sway: a cut-out of the scene's (`plane`: its id under `planes`) stirs from a fixed edge. Its own picture is shifted a
 * little, row by row (or column by column), each time it is asked for, the canvas smoothing the shift to a fraction of a
 * pixel: rows that are shifted alike are drawn in one go, so a whole palm costs a few dozen draws. The cut-out keeps its
 * depth, its `when`, its states, and everything a script does to it. Only a cut-out shown at its own size sways (one a
 * script has scaled is shown as it is).
 *   anchor "bottom"   rooted at its foot (a palm, reeds): from the row at[1], or its lowest paint. It leans as one.
 *          "top"      hangs from its top (a sheet, a fringe): from the row at[1], or its highest paint. A ripple runs down it.
 *          "left", "right"   flies from a pole at that side (a banner, a streamer): from the column at[0], or the paint
 *                     nearest that side; it moves up and down, and a ripple runs out along it.
 *          [[x1, y1], [x2, y2]]   from a line in the picture (a rope): pixel by pixel, sideways if the line runs across,
 *                     up and down if it runs up (slower: for a small cut-out).
 */
/** The pixels of each cut-out picture a sway has read, by its canvas (the cut-out's own pictures are made once and kept: cast.js). */
const pixelsOf = new WeakMap();
class Sway extends Effect {
  constructor(host, spec, n) {
    super(host, spec, n);
    const s = spec;
    this.target = typeof s.plane === "string" ? s.plane : typeof s.of === "string" ? s.of : null;
    if (!this.target) throw new Error('sway needs the id of a cut-out: plane: "<its id>"');
    this.anchor = s.anchor || "top";
    this.amount = num(s.amount, 2.5); this.period = num(s.period, num(s.speed, 3.4)); this.lean = num(s.lean, 0.3);
    this.wave = num(s.wave, this.anchor === "bottom" ? 600 : 90);       // a plant leans as one; cloth ripples
    this.fps = 6; this.calmFps = 3;                                  // (slow: the far edge moves a few pixels a second at most; and the whole cut-out is repainted each time)
    this.made = new WeakMap();
    this.gen = 0; this.lastStep = null;
    this.slot = { want: false, waits: 0, urgent: false, grant: () => { this.slot.want = false; this.go = true; } };
  }
  slots() { return [this.slot]; }
  restart() { this.gen++; this.lastStep = null; }
  update(calm) {
    if (this.lastStep === null) return;
    const fps = calm ? this.calmFps : this.fps;
    this.slot.want = Math.floor((this.time * fps) / 1000) !== this.lastStep || calm !== this.lastCalm;
  }
  attach() {
    const cut = this.game.view.cast.get(this.target);
    if (!(cut instanceof Cutout)) { console.warn(`Sway "${this.id}": there is no cut-out called "${this.target}" in this scene's planes.`); return; }
    this.cut = cut;
    const own = cut.picture;                                         // (the cut-out's own way of making its picture)
    cut.picture = (palette, calm) => { const pic = own.call(cut, palette, calm); return this.stir(pic, calm) || pic; };
  }
  stir(pic, calm) {
    if (!pic || !pic.canvas || pic.w != null || !this.shown || !this.amount) return null;
    let m = this.made.get(pic.canvas);
    if (m === undefined) { m = this.measure(pic); this.made.set(pic.canvas, m); }
    if (!m) return null;
    const fps = calm ? this.calmFps : this.fps, step = Math.floor((this.time * fps) / 1000), go = this.go;
    this.go = false;
    if (m.gen !== this.gen || (go && (m.step !== step || m.calm !== calm))) {          // (a picture it has not bent yet at once; after that, in its turn)
      m.gen = this.gen; m.step = step; m.calm = calm; this.lastStep = step; this.lastCalm = calm;
      this.render(m, step / fps, calm); this.drawn = 1;
    }
    return { canvas: m.pair.canvas, ox: pic.ox + m.padX, oy: pic.oy + m.padY };
  }
  /** Read the cut-out's picture once: how far each row (or column) is from the fixed edge, 0 there and 1 at the farthest paint. */
  measure(pic) {
    const src = pic.canvas, w = src.width, h = src.height, a = this.anchor, s = this.spec, cut = this.cut;
    let data = pixelsOf.get(src);                                    // (read once for good: a scene entered again would read the same picture again, and the browser warns of that)
    if (!data) {
      try { data = src.getContext("2d").getImageData(0, 0, w, h).data; pixelsOf.set(src, data); } catch (err) { console.warn(`Sway "${this.id}" cannot read the picture of "${this.target}":`, err); return null; }
    }
    const solid = (x, y) => data[(y * w + x) * 4 + 3] > 12, at = isPoint(s.at) ? s.at : null;
    const left = Math.round(cut.x) - Math.round(pic.ox), top = Math.round(cut.y) - Math.round(pic.oy);        // where the canvas lies on the picture
    const rowHas = (y) => { for (let x = 0; x < w; x++) if (solid(x, y)) return true; return false; };
    const colHas = (x) => { for (let y = 0; y < h; y++) if (solid(x, y)) return true; return false; };
    const reach = Math.ceil(this.amount * (1 + Math.abs(this.lean)) + 1);
    const lines = (n, from, toward) => {                             // each line's distance from the fixed edge, 0 to 1
      const d = new Float32Array(n), most = Math.max(1, Math.abs(toward - from));
      for (let i = 0; i < n; i++) d[i] = clamp(((i - from) * Math.sign(toward - from || 1)) / most);
      return d;
    };
    if (a === "bottom" || a === "top") {
      let first = 0, last = h - 1;
      while (first < h && !rowHas(first)) first++;
      while (last > first && !rowHas(last)) last--;
      if (first >= h) return null;
      const edge = at ? at[1] - top : a === "bottom" ? last : first;
      return { mode: "rows", w, h, far: lines(h, edge, a === "bottom" ? first : last), padX: reach, padY: 0, pair: new Pair(w + reach * 2, h), src, step: null, calm: null, gen: null, top, left };
    }
    if (a === "left" || a === "right") {
      let first = 0, last = w - 1;
      while (first < w && !colHas(first)) first++;
      while (last > first && !colHas(last)) last--;
      if (first >= w) return null;
      const edge = at ? at[0] - left : a === "left" ? first : last;
      return { mode: "cols", w, h, far: lines(w, edge, a === "left" ? last : first), padX: 0, padY: reach, pair: new Pair(w, h + reach * 2), src, step: null, calm: null, gen: null, top, left };
    }
    if (!(Array.isArray(a) && a.length === 2 && a.every(isPoint))) { console.warn(`Sway "${this.id}": anchor "${a}" is not one the engine knows (top, bottom, left, right, or a line).`); return null; }
    // a line: each pixel by its own distance from it
    const [[x1, y1], [x2, y2]] = a, dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy) || 1, across = Math.abs(dx) >= Math.abs(dy), dist = new Float32Array(w * h);
    let most = 0;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const d = Math.abs(((x + left - x1) * dy - (y + top - y1) * dx) / len); dist[y * w + x] = d; if (d > most && solid(x, y)) most = d; }
    if (!most) return null;
    for (let i = 0; i < dist.length; i++) dist[i] = Math.pow(clamp(dist[i] / most), 1.3);
    const used = across ? Array.from({ length: h }, (_, y) => rowHas(y)) : Array.from({ length: w }, (_, x) => colHas(x));
    const padX = across ? reach : 0, padY = across ? 0 : reach, W2 = w + padX * 2, H2 = h + padY * 2;
    return { mode: "pixels", data, far: dist, w, h, W2, H2, padX, padY, across, used, out: new ImageData(W2, H2), pair: new Pair(W2, H2), step: null, calm: null, gen: null, left, top };
  }
  /** How far the cloth is pushed at distance `d` along it (0 to 1, the free end at 1), `p` its place in the picture, at t. */
  push(d, p, t, amp) {
    const om = TAU / this.period, kw = TAU / this.wave, ph = (this.seed % 1000) / 159;
    return amp * Math.pow(d, 1.3) * (0.62 * Math.sin(om * t - p * kw + ph) + 0.38 * Math.sin(1.63 * om * t - p * kw * 1.7 + ph * 2.3) + this.lean);
  }
  render(m, t, calm) {
    const amp = this.amount * (calm ? 0.6 : 1);
    if (m.mode === "pixels") return this.renderPixels(m, t, amp);
    const ctx = m.pair.next(), rows = m.mode === "rows", n = rows ? m.h : m.w, at = rows ? m.top : m.left;
    ctx.imageSmoothingEnabled = true;
    // the rows (or columns) in runs that are pushed alike (to a quarter of a pixel), each run drawn in one go
    let from = 0, shift = Math.round(this.push(m.far[0], at, t, amp) * 4) / 4;
    for (let i = 1; i <= n; i++) {
      const next = i < n ? Math.round(this.push(m.far[i], at + i, t, amp) * 4) / 4 : NaN;
      if (next === shift) continue;
      if (rows) ctx.drawImage(m.src, 0, from, m.w, i - from, m.padX + shift, from, m.w, i - from);
      else ctx.drawImage(m.src, from, 0, i - from, m.h, from, m.padY + shift, i - from, m.h);
      from = i; shift = next;
    }
  }
  renderPixels(m, t, amp) {
    const { data, far, w, h, W2, H2, padX, padY, across, used } = m, out = m.out.data;
    const wave = new Float32Array(across ? W2 : H2);                  // the push at each column (or row) for a pixel at the free end
    for (let i = 0; i < wave.length; i++) wave[i] = this.push(1, i + (across ? m.left - padX : m.top - padY), t, amp);
    out.fill(0);
    for (let j = 0; j < (across ? h : w); j++) {
      if (!used[j]) continue;
      for (let o = 0; o < (across ? W2 : H2); o++) {
        const k = o - (across ? padX : padY), ki = k < 0 ? 0 : k >= (across ? w : h) ? (across ? w : h) - 1 : k;
        const s2 = k - wave[o] * (across ? far[j * w + ki] : far[ki * w + j]), k0 = Math.floor(s2), f = s2 - k0;
        if (k0 < -1 || k0 >= (across ? w : h)) continue;
        let r = 0, g = 0, b = 0, al = 0;
        for (const [kk, q0] of [[k0, 1 - f], [k0 + 1, f]]) {
          if (kk < 0 || kk >= (across ? w : h)) continue;
          const i = (across ? j * w + kk : kk * w + j) * 4, q = data[i + 3] * q0;
          r += data[i] * q; g += data[i + 1] * q; b += data[i + 2] * q; al += q;
        }
        if (al < 0.5) continue;
        const p = (across ? j * W2 + o : o * W2 + j + padX) * 4;
        out[p] = r / al; out[p + 1] = g / al; out[p + 2] = b / al; out[p + 3] = al;
      }
    }
    m.pair.next().putImageData(m.out, 0, 0);
  }
}

// ---------------------------------------------------------------- birds
// Birds drawn by code, for a flock that has no painted frames (and for the engine's own scene): side on, facing right,
// standing on the point (0, 0). One unit is a sixteenth of the bird's length.
const LOOKS = {
  pigeon: { body: "#8e93a7", wing: "#a5aabb", bar: "#34363f", tail: "#5d6171", neck: "#71877e", head: "#80859a", beak: "#3a3432", cere: "#ece4da", legs: "#c76f6b", eye: "#d9772d" },
  dove: { body: "#cbb9a3", wing: "#b8a58d", bar: "#7b6855", tail: "#9b8872", neck: "#c6aba2", head: "#c9b9a8", beak: "#4a3f39", cere: "#e8dbcc", legs: "#c27a6e", eye: "#5b2b1b" },
  sparrow: { body: "#8c6b4c", wing: "#715439", bar: "#e6dbc5", tail: "#5e452f", neck: "#b49c80", head: "#7e6048", beak: "#3a2e27", cere: "#3a2e27", legs: "#9f7a61", eye: "#1a120f" },
};
const POSTURE = {
  stand: { tip: -0.12, head: [3.6, -8.1], neck: [2.6, -5.9] },
  look: { tip: -0.12, head: [3.2, -8.3], neck: [2.5, -5.9], away: true },
  peck0: { tip: 0.14, head: [5.1, -4.5], neck: [3.6, -4.9], down: 0.6 },
  peck1: { tip: 0.34, head: [5.5, -2.0], neck: [3.9, -3.7], down: 1.3 },
  walk0: { tip: -0.08, head: [4.3, -7.9], neck: [3.0, -5.8], legs: [[1.4, 0], [-1.3, 0]] },
  walk1: { tip: -0.14, head: [3.0, -8.2], neck: [2.4, -5.9], legs: [[0.3, -0.8], [-0.2, 0]] },
  fly0: { tip: 0, head: [4.5, -6.9], neck: [3.1, -5.7], wings: "up" },
  fly1: { tip: 0, head: [4.6, -6.6], neck: [3.1, -5.6], wings: "level" },
  fly2: { tip: 0, head: [4.5, -6.4], neck: [3.1, -5.5], wings: "down" },
};
const WINGS = {
  up: [[-0.4, -5.7], [-2.4, -12.6], [-4.3, -11.4], [-2.4, -5.2]],
  level: [[-0.4, -5.7], [-7.6, -7.4], [-6.6, -5.4], [-2.0, -4.7]],
  down: [[-0.4, -5.3], [-2.0, -0.6], [-3.6, -1.0], [-2.3, -4.6]],
};
function paintBird(ctx, u, c, pose) {
  const ell = (x, y, rx, ry, rot, fill) => { ctx.fillStyle = fill; ctx.beginPath(); ctx.ellipse(x * u, y * u, Math.max(0.3, rx * u), Math.max(0.3, ry * u), rot, 0, TAU); ctx.fill(); };
  const poly = (pts, fill) => { ctx.fillStyle = fill; ctx.beginPath(); pts.forEach(([x, y], i) => (i ? ctx.lineTo(x * u, y * u) : ctx.moveTo(x * u, y * u))); ctx.closePath(); ctx.fill(); };
  const line = (x1, y1, x2, y2, wd, col) => { ctx.strokeStyle = col; ctx.lineWidth = Math.max(0.7, wd * u); ctx.lineCap = "round"; ctx.beginPath(); ctx.moveTo(x1 * u, y1 * u); ctx.lineTo(x2 * u, y2 * u); ctx.stroke(); };
  if (pose === "turn") {                                             // facing us
    ell(-2.3, -4.7, 0.9, 2.2, 0.25, c.wing); ell(2.3, -4.7, 0.9, 2.2, -0.25, c.wing);
    line(-0.7, -2.3, -0.8, 0, 0.55, c.legs); line(0.7, -2.3, 0.8, 0, 0.55, c.legs);
    ell(0, -4.8, 2.6, 3.0, 0, c.body); ell(0, -6.0, 1.8, 1.9, 0, c.neck); ell(0, -8.3, 1.45, 1.4, 0, c.head);
    ell(-0.6, -8.5, 0.36, 0.36, 0, c.eye); ell(0.6, -8.5, 0.36, 0.36, 0, c.eye);
    poly([[-0.45, -8.0], [0.45, -8.0], [0, -7.0]], c.beak);
    return;
  }
  const P = POSTURE[pose] || POSTURE.stand, tip = P.tip, wing = P.wings ? WINGS[P.wings] : null, tailY = -3.9 - tip * 6;
  if (wing) poly(wing.map(([x, y]) => [x + 1.1, y - 0.5]), c.tail);  // the far wing, in shadow
  poly([[-3.0, -5.0 - tip * 1.5], [-7.6, tailY - 0.7], [-7.9, tailY + 0.6], [-2.6, -3.6 - tip * 1.2]], c.tail);
  if (!wing) for (const [lx, ly] of P.legs || [[0.6, 0], [-0.5, 0]]) line(lx * 0.4, -2.3, lx, ly, 0.55, c.legs);
  ell(-0.3, -4.6, 4.7, 2.75, tip - 0.1, c.body);
  if (wing) { poly(wing, c.wing); line(wing[1][0], wing[1][1], wing[2][0], wing[2][1], 0.7, c.bar); }
  else {
    ell(-1.3, -4.9 - tip, 3.6, 1.65, tip - 0.06, c.wing);
    if (u >= 1) { ctx.globalAlpha = 0.55; line(-2.3, -5.6 - tip, -1.9, -4.2 - tip, 0.35, c.bar); line(-1.3, -5.7 - tip, -0.9, -4.3 - tip, 0.35, c.bar); ctx.globalAlpha = 1; }   // the two bars across a folded wing, where there is room for them
  }
  ell(P.neck[0], P.neck[1], 1.9, 2.1, 0, c.neck);
  const [hx, hy] = P.head;
  ell(hx, hy, 1.45, 1.4, 0, c.head);
  if (P.away) poly([[hx + 0.9, hy - 0.2], [hx + 1.6, hy + 0.4], [hx + 0.8, hy + 0.6]], c.beak);
  else {
    const d = P.down || 0;
    poly([[hx + 1.2, hy - 0.3 + d * 0.3], [hx + 2.6, hy + 0.2 + d], [hx + 1.2, hy + 0.5 + d * 0.3]], c.beak);
    ell(hx + 1.35, hy - 0.15 + d * 0.2, 0.45, 0.35, 0, c.cere);
    ell(hx + 0.35, hy - 0.35, 0.42, 0.42, 0, c.eye);
  }
}
/** A small bird seen from below, flying: a dark M, its wings `pose` (up, mid, down, glide), `span` pixels from tip to tip. */
function paintFlyer(ctx, span, color, pose) {
  const h = span / 2, form = { up: [[-h, -span * 0.36], [-span * 0.2, -span * 0.08]], mid: [[-h, -span * 0.04], [-span * 0.24, -span * 0.13]], down: [[-h, span * 0.24], [-span * 0.2, span * 0.05]], glide: [[-h, -span * 0.02], [-span * 0.24, -span * 0.09]], bank: [[-h, -span * 0.2], [-span * 0.22, -span * 0.12]] }[pose];
  const [[tx, ty], [mx, my]] = form;
  ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = Math.max(1, span / 7); ctx.lineCap = "round"; ctx.lineJoin = "round";
  ctx.beginPath(); ctx.moveTo(tx, ty); ctx.quadraticCurveTo(mx, my, 0, 0); ctx.quadraticCurveTo(-mx, pose === "bank" ? my * 0.3 : my, -tx, pose === "bank" ? -ty * 0.4 : ty); ctx.stroke();
  ctx.beginPath(); ctx.ellipse(0, span * 0.02, span * 0.11, span * 0.07, 0, 0, TAU); ctx.fill();
}

// Every picture of a bird, drawn or taken from a painted frame (scaled, turned the other way), is made once and kept.
const birdPics = new Map();
function kept(key, make) {
  let hit = birdPics.get(key);
  if (hit) { birdPics.delete(key); birdPics.set(key, hit); return hit; }
  hit = make();
  birdPics.set(key, hit);
  if (birdPics.size > 800) birdPics.delete(birdPics.keys().next().value);       // (the one gone longest unused)
  return hit;
}
/** A drawn bird: { canvas, ox, oy } with (ox, oy) the point it stands on. (Exported for the tools and the tests.) */
export function drawnBird(look, pose, length, mirror) {
  const L = Math.max(4, Math.round(length * 2) / 2);
  return kept(`d|${look}|${pose}|${L}|${mirror ? 1 : 0}`, () => {
    const u = L / 16, w = Math.ceil(16 * u) + 4, h = Math.ceil(14 * u) + 3, fx = Math.ceil(8.3 * u) + 2, fy = Math.ceil(13 * u) + 1, c = canvasOf(w, h), ctx = c.getContext("2d");
    ctx.translate(mirror ? w - fx : fx, fy);
    if (mirror) ctx.scale(-1, 1);
    paintBird(ctx, u, LOOKS[look] || LOOKS.pigeon, pose);
    return { canvas: c, ox: mirror ? w - fx : fx, oy: fy };
  });
}
export function drawnFlyer(span, color, pose) {
  const S = Math.max(3, Math.round(span * 2) / 2);
  return kept(`f|${color}|${pose}|${S}`, () => {
    const side = Math.ceil(S) + 4, c = canvasOf(side, side), ctx = c.getContext("2d");
    ctx.translate(side / 2, side / 2);
    paintFlyer(ctx, S, color, pose);
    return { canvas: c, ox: side / 2, oy: side / 2 };
  });
}
/** A painted frame at size k (turned the other way if `mirror`), placed by its point `foot`; null until it has arrived. */
function paintedBird(path, k, mirror, foot, shadow = null) {
  const img = got(path), sh = shadow ? got(shadow) : null;
  if (!img || !img.naturalWidth) return null;
  const q = Math.max(1 / 16, Math.round(k * 16) / 16);
  return kept(`p|${path}|${q}|${mirror ? 1 : 0}|${sh && sh.naturalWidth ? shadow : ""}`, () => {
    const w = Math.max(1, Math.round(img.naturalWidth * q)), h = Math.max(1, Math.round(img.naturalHeight * q)), f = foot || [img.naturalWidth / 2, img.naturalHeight / 2];
    const fx = (mirror ? img.naturalWidth - f[0] : f[0]) * (w / img.naturalWidth), fy = f[1] * (h / img.naturalHeight);
    // a shadow on the ground, painted with the same foot point, goes under it and is never turned round (the sun does not move)
    let left = 0, top = 0, right = w, bottom = h, sx = 0, sy = 0, sw = 0, shh = 0;
    if (sh && sh.naturalWidth) {
      sw = Math.max(1, Math.round(sh.naturalWidth * q)); shh = Math.max(1, Math.round(sh.naturalHeight * q));
      sx = Math.round(fx - f[0] * (sw / sh.naturalWidth)); sy = Math.round(fy - f[1] * (shh / sh.naturalHeight));
      left = Math.min(0, sx); top = Math.min(0, sy); right = Math.max(w, sx + sw); bottom = Math.max(h, sy + shh);
    }
    const c = canvasOf(right - left, bottom - top), ctx = c.getContext("2d");
    ctx.imageSmoothingEnabled = q !== 1; ctx.imageSmoothingQuality = "high";
    if (sw) ctx.drawImage(sh, sx - left, sy - top, sw, shh);
    ctx.translate(-left, -top);
    if (mirror) { ctx.translate(w, 0); ctx.scale(-1, 1); }
    ctx.drawImage(img, 0, 0, w, h);
    return { canvas: c, ox: fx - left, oy: fy - top };
  });
}

const FRAME_NAMES = ["stand", "look", "peck", "walk", "turn", "fly", "takeoff", "land", "glide", "flap", "bank", "shadow"];
/** The folder a scene's own pictures are in: where a mark's frames are, when it does not say. */
const folderOf = (scene) => (scene && typeof scene.picture === "string" && scene.picture.includes("/") ? scene.picture.slice(0, scene.picture.lastIndexOf("/") + 1) : "");
/**
 * Painted frames as a mark gives them: { dir, foot, face, stand: [...], peck: [...], ... } (a name or a list of names
 * each), or just a list (a flyer's wingbeat). As { lists: { stand: [paths], ... }, foot, face }, or null.
 */
function framesOf(frames, scene) {
  if (!frames) return null;
  if (Array.isArray(frames) || typeof frames === "string") frames = { flap: frames };
  const dir = typeof frames.dir === "string" ? frames.dir : folderOf(scene), lists = {}, set = typeof frames.set === "string" ? frames.set : null;
  // a name is a file in the folder; a number n is the file "<set>-<n>.png" of the frames' `set`
  const file = (f) => (typeof f === "number" && set ? `${dir}${set}-${f}.png` : typeof f !== "string" ? null : f.startsWith("art/") ? f : dir + f);
  for (const name of FRAME_NAMES) {
    const v = frames[name];
    const list = (Array.isArray(v) ? v : v != null ? [v] : []).map(file).filter(Boolean);
    if (list.length) lists[name] = list;
  }
  const shadow = lists.shadow ? lists.shadow[0] : null;
  delete lists.shadow;
  if (!Object.keys(lists).length) return null;
  const foot = isPoint(frames.foot) ? frames.foot : isPoint(frames.middle) ? frames.middle : null;
  return { lists, foot, shadow, face: frames.face === "W" ? -1 : 1, mirror: frames.mirror !== false, sizeAt: num(frames.sizeAt, null) };
}
/** Every painted picture a scene's moving things can show (for fetching them ahead: scene.js, picturesIn). */
export function fxPictures(scene) {
  const list = scene && Array.isArray(scene.fx) ? scene.fx : [];
  return [...new Set(list.flatMap((spec) => { const f = spec && framesOf(spec.frames, scene); return f ? [...Object.values(f.lists).flat(), ...(f.shadow ? [f.shadow] : [])] : []; }))];
}

/** Birds in the air: across the sky now and then along `lanes`, or wheeling round a `circle`. */
class Flyers extends Effect {
  constructor(host, spec, n) {
    super(host, spec, n);
    const s = spec;
    this.plane = "back";
    this.lanes = (Array.isArray(s.lanes) ? s.lanes : []).map((lane) => {
      const pts = Array.isArray(lane) ? lane : lane && lane.path, line = smoothLine(pts, 4);
      return line.length > 1 ? { line, len: line[line.length - 1][2], size: lane && num(lane.size, null) } : null;
    }).filter(Boolean);
    const c = s.circle;
    this.circle = c && isPoint(c.at) ? { at: c.at, r: isPair(c.r) ? c.r : [num(c.r, 30), num(c.r, 30) * 0.4] } : null;
    if (!this.lanes.length && !this.circle) throw new Error("flyers need lanes or a circle");
    this.every = isPair(s.every) ? s.every : [num(s.every, 10) * 0.6, num(s.every, 10) * 1.4];
    this.group = isPair(s.group) ? s.group : [1, num(s.group, 3)];
    this.speed = num(s.speed, this.circle ? 14 : 70);
    this.span = isPair(s.size) ? s.size : [num(s.size, 7), num(s.size, 7)];
    this.color = typeof s.color === "string" ? s.color : "#2b2724";
    this.both = s.both !== false;
    this.frames = framesOf(s.frames, host.scene);
    this.ks = isPair(s.scale) ? s.scale : [this.k, this.k];           // `scale: [low, high]`: each bird its own size
    this.slow = 0.6;
    this.count = this.circle ? Math.max(1, Math.round(num(s.count, 2))) : 0;
    this.wheelers = [];
    // One picture for each group in the air (all the wheeling birds; each crossing's birds), so a group is one patch to repaint.
    for (let i = 0; i < (this.circle ? 1 : 3); i++) this.mote(":" + i).fade(clamp(num(s.opacity, 1)));
    this.restart();
  }
  restart() { this.trips = []; this.fresh = true; this.lastT = null; for (const s of this.sprites) { s.sig = null; s.pic = null; } }
  reveal(on) { for (const s of this.sprites) s.hidden = !on || !s.pic; }
  /** Crossings, from a little before the scene began, worked out as far as t (seconds): when, where, which way, how many. */
  plan(t) {
    while (!this.trips.length || this.trips[this.trips.length - 1].start <= t) {
      const c = this.trips.length, seed = this.seed, prev = c ? this.trips[c - 1].start : -6;
      const lane = this.lanes[Math.floor(rnd(seed, c, 2) * this.lanes.length)], start = prev + Math.max(0.5, within(this.every, rnd(seed, c, 1)));
      const speed = this.speed * (0.85 + 0.35 * rnd(seed, c, 5)), count = Math.max(1, Math.round(within(this.group, rnd(seed, c, 4)))), birds = [];
      for (let b = 0; b < count; b++) birds.push({ delay: b ? b * (0.2 + 0.45 * rnd(seed, c, 10 + b)) : 0, off: (rnd(seed, c, 20 + b) - 0.5) * 14, speed: speed * (0.95 + 0.1 * rnd(seed, c, 30 + b)),
        flap: 0.5 + rnd(seed, c, 40 + b), glide: 0.4 + 1.2 * rnd(seed, c, 50 + b), beat: 5 + 2.5 * rnd(seed, c, 60 + b), phase: rnd(seed, c, 70 + b) * 4, span: within(this.span, rnd(seed, c, 80 + b)), k: within(this.ks, rnd(seed, c, 90 + b)) });
      this.trips.push({ start, lane, dir: this.both && rnd(seed, c, 3) < 0.5 ? -1 : 1, birds, quiet: rnd(seed, c, 9) < 0.4, end: start + lane.len / (speed * 0.95) + 3 });
    }
  }
  /** The picture of one bird: its wings as they are at t (flapping in bursts, gliding between), heading `dx`. */
  look(t, b, dx, calm, banking = false) {
    const cyc = b.flap + b.glide, m = (t + b.phase) % cyc, flapping = !calm && m < b.flap, f = this.frames;
    if (f) {
      const L = f.lists, beats = L.flap || L.fly;
      let list = null, i = 0;
      if (banking && L.bank) list = L.bank;
      else if (flapping && beats) { list = beats; i = Math.floor((t + b.phase) * b.beat * beats.length) % beats.length; }
      else list = L.glide || (beats && [beats[0]]) || L.bank;
      const pic = list && paintedBird(list[i], b.k, f.mirror && dx * f.face < 0, f.foot);
      if (pic) return pic;
    }
    const pose = banking ? "bank" : flapping ? ["up", "mid", "down", "mid"][Math.floor((t + b.phase) * b.beat * 4) % 4] : "glide";
    return drawnFlyer(b.span * b.k, this.color, pose);
  }
  /** Where the birds in the air are at t, by group (the wheeling birds, or each crossing): [[x, y, picture], ...] each. */
  groups(t, calm) {
    if (this.circle) {
      const { at, r } = this.circle, seed = this.seed, list = [];
      for (let i = 0; i < this.count; i++) {
        const b = this.wheelers[i] || (this.wheelers[i] = { flap: 0.6 + rnd(seed, i, 1) * 0.6, glide: 3 + rnd(seed, i, 2) * 5, beat: 4 + rnd(seed, i, 3) * 2, phase: rnd(seed, i, 4) * 9, span: within(this.span, rnd(seed, i, 5)), turn: rnd(seed, i, 6) * TAU, rk: 0.75 + 0.5 * rnd(seed, i, 7), k: within(this.ks, rnd(seed, i, 8)) });
        const w = this.speed / Math.max(4, (r[0] + r[1]) / 2), a = b.turn + t * w * b.rk ** -0.5;
        const cx = at[0] + Math.sin(t * 0.05 + i * 2.1) * r[0] * 0.35, cy = at[1] + Math.cos(t * 0.04 + i * 1.3) * r[1] * 0.4;
        list.push([cx + Math.cos(a) * r[0] * b.rk, cy + Math.sin(a) * r[1] * b.rk, this.look(t, b, -Math.sin(a), calm, Math.abs(Math.cos(a)) > 0.9 && !calm)]);
      }
      return [list];
    }
    this.plan(t);
    const out = [];
    for (let c = this.trips.length - 1; c >= 0 && out.length < this.sprites.length; c--) {
      const trip = this.trips[c];
      if (trip.start > t || trip.end < t || (calm && trip.quiet)) { if (trip.start < t - 120) break; continue; }
      const { line, len } = trip.lane, list = [];
      for (const b of trip.birds) {
        const s = (t - trip.start - b.delay) * b.speed;
        if (s < 0 || s > len) continue;
        const [x, y, ddx] = along(line, trip.dir > 0 ? s : len - s);
        list.push([x, y + b.off + Math.sin((t + b.phase) * 2.1) * 1.5, this.look(t, b, ddx * trip.dir, calm)]);
      }
      if (list.length) out.push(list);
    }
    return out;
  }
  update(calm) {
    const t = (Math.floor(this.time / TICK) * TICK) / 1000;          // (on the grid of thirty steps a second: nothing changes in between)
    if (t === this.lastT && calm === this.lastCalm && !this.fresh) return;
    this.lastT = t; this.lastCalm = calm;
    const groups = this.groups(t, calm);
    let birds = 0;
    this.sprites.forEach((s, i) => {
      const list = groups[i] || [];
      birds += list.length;
      if (!list.length) { s.hidden = true; s.pic = null; s.sig = null; s.want = false; return; }
      const sig = list.map(([x, y, p]) => `${Math.round(x - p.ox)},${Math.round(y - p.oy)},${idOf(p.canvas)}`).join(";");
      s.next = list; s.nextSig = sig; s.want = sig !== s.sig;
      if (s.want && this.fresh) s.grant();
    });
    this.fresh = false;
    this.drawn = birds;
  }
  /** Its turn: the group's picture, every bird of it on one canvas just big enough. */
  grant(s) {
    const list = s.next;
    if (!list) return;
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const [x, y, p] of list) { const l = Math.round(x - p.ox), tp = Math.round(y - p.oy); x0 = Math.min(x0, l); y0 = Math.min(y0, tp); x1 = Math.max(x1, l + p.canvas.width); y1 = Math.max(y1, tp + p.canvas.height); }
    if (!s.pair || s.pair.w < x1 - x0 || s.pair.h < y1 - y0) s.pair = new Pair(x1 - x0 + 6, y1 - y0 + 6);
    const ctx = s.pair.next();
    for (const [x, y, p] of list) ctx.drawImage(p.canvas, Math.round(x - p.ox) - x0, Math.round(y - p.oy) - y0);
    s.place(x0, y0); s.pic = { canvas: s.pair.canvas, ox: 0, oy: 0 }; s.sig = s.nextSig; s.hidden = false;
  }
  picture(sprite) { return sprite.pic || null; }
}

/**
 * A flock on the ground (`area`, a shape) or along a ledge (`perch`, a line): each bird stands, looks about, pecks,
 * walks a little, turns; when somebody comes near (nearer than `shy`; walking past, or standing over them) it goes up
 * and lands again a little way off, and the ones beside it go too; with nowhere safe to land, it flies off and comes back
 * later. Each bird is its own sprite, sorted by its own feet. Players who asked for less motion get birds that walk off
 * instead of flying, and do everything at a gentler pace.
 */
class Flock extends Effect {
  constructor(host, spec, n) {
    super(host, spec, n);
    const s = spec;
    this.perch = isPoly(s.perch) || (Array.isArray(s.perch) && s.perch.length === 2 && s.perch.every(isPoint)) ? smoothLine(s.perch, 2) : null;
    this.area = this.perch ? null : polyOf(s.area) || polyOf(s.poly) || polyOf(s.rect);
    if (!this.perch && !this.area) throw new Error("a flock needs an area (or poly, rect) or a perch");
    this.box = this.area ? boxOf(this.area) : null;
    this.count = Math.max(1, Math.round(num(s.count, 5)));
    this.kind = LOOKS[s.look] ? s.look : "pigeon";
    this.length = num(s.size, 26);                                 // a pigeon is about a fifth of a man's height: 26 pixels long where he is 160 tall
    this.frames = framesOf(s.frames, host.scene);
    this.depth = s.depth ?? !!this.area;
    if (this.frames && s.scale === "depth" && this.frames.sizeAt == null) this.frames.sizeAt = num(host.scene && host.scene.full, 590);      // painted at full size, smaller farther off
    this.span = this.box ? Math.max(this.box[2] - this.box[0], this.box[3] - this.box[1]) : this.perch[this.perch.length - 1][2];
    // Birds on steps keep to the treads: `treads` (the rows) or `tread` (px from one to the next, from the foot of the area up).
    this.treads = Array.isArray(s.treads) ? s.treads.filter((v) => typeof v === "number").sort((a, b) => a - b)
      : this.area && num(s.tread, 0) > 0 ? Array.from({ length: Math.floor((this.box[3] - this.box[1]) / s.tread) + 1 }, (_, i) => this.box[3] - i * s.tread) : null;
    this.moves = { stand: 2, look: 2, peck: 4, walk: 3, turn: 1, away: 0 };
    if (s.moves && typeof s.moves === "object") for (const [k, v] of Object.entries(s.moves)) if (k in this.moves) this.moves[k] = Math.max(0, num(v, 0));
    this.shy = num(s.shy, 150);                                      // pixels at full size, where a man is 160 tall: a metre and a half
    this.turns = s.turn !== false;
    this.flies = s.fly !== false && (!this.frames || !!this.frames.lists.fly);
    this.back = isPair(s.back) ? s.back : [8, 20];
    this.walkSpeed = num(s.walk, 12); this.flySpeed = num(s.flight, 95);
    this.slow = 0.6;
    this.scene = host.scene;
    if (this.frames && !this.frames.lists.stand) this.frames.lists.stand = Object.values(this.frames.lists)[0];
    this.birds = [];
    for (let i = 0; i < this.count; i++) { const b = { i, sprite: this.mote(":" + i) }; b.sprite.bird = b; this.birds.push(b); }
    this.restart();
  }
  restart() {
    this.simT = 0;
    this.fresh = true;
    for (const b of this.birds) {
      b.rand = sequence(this.seed + b.i * 7919);
      const p = this.place(b) || this.center();
      Object.assign(b, { x: p[0], y: p[1], s: p[2], alt: 0, dir: this.turns ? (b.rand() < 0.5 ? -1 : 1) : this.frames ? this.frames.face : 1, act: null, startle: null, away: false });
      b.act = { kind: "stand", t0: 0, until: 0.3 + b.rand() * 2.5 };
    }
  }
  center() { if (this.perch) { const s = this.perch[this.perch.length - 1][2] / 2, [x, y] = along(this.perch, s); return [x, y, s]; } const [x0, y0, x1, y1] = this.box; return [(x0 + x1) / 2, (y0 + y1) / 2, 0]; }
  /** A random place to stand: in the area, or on the perch. [x, y, s]; null if none was found. */
  place(b) {
    if (this.perch) { const s = b.rand() * this.perch[this.perch.length - 1][2], [x, y] = along(this.perch, s); return [x, y, s]; }
    const [x0, y0, x1, y1] = this.box;
    for (let i = 0; i < 12; i++) {
      const x = x0 + b.rand() * (x1 - x0), y = this.tread(x, y0 + b.rand() * (y1 - y0));
      if (y != null && inside(this.area, x, y)) return [x, y, 0];
    }
    return null;
  }
  /** On steps, the tread nearest y that is in the area at x (or null); anywhere else, y itself. */
  tread(x, y) {
    if (!this.treads) return y;
    let best = null;
    for (const row of this.treads) if (inside(this.area, x, row) && (best === null || Math.abs(row - y) < Math.abs(best - y))) best = row;
    return best;
  }
  /** How big things are where the bird stands (1 at the row a person is drawn full size), when the flock follows the depth. */
  sizeAt(y) { return this.depth && this.scene ? scaleAt(this.scene, y) : 1; }
  /** How far a person is from a bird, in pixels as they would be at full size: up and down the picture counts for more (walk.js, DEPTH). */
  gap(b, x, y) { return Math.hypot(x - b.x, (y - b.y) * DEPTH) / Math.max(0.3, this.sizeAt(b.y)); }
  threat(b, people) {
    if (!(this.shy > 0)) return null;
    for (const p of people) if (this.gap(b, p.x, p.y) < this.shy * (p.walking ? 1 : 0.55)) return p;
    return null;
  }
  /** A place from `min` to `max` pixels away that is well clear of everybody, or null. */
  refuge(b, people, min, max) {
    for (let i = 0; i < 16; i++) {
      const p = this.place(b);
      if (!p) continue;
      const d = Math.hypot(p[0] - b.x, (p[1] - b.y) * DEPTH);
      if (d < min || d > max) continue;
      if (people.every((q) => Math.hypot(q.x - p[0], (q.y - p[1]) * DEPTH) / Math.max(0.3, this.sizeAt(p[1])) > this.shy * 1.4)) return p;
    }
    return null;
  }
  /** Somebody came too near: up and away (or, for less motion or a bird that cannot fly, off on foot). */
  startle(b, t, calm, people) {
    const k = this.sizeAt(b.y);
    b.startle = null;
    if (calm || !this.flies) {
      if (b.act.kind === "walk" && b.act.hurry) return;               // already on its way
      const to = this.refuge(b, people, 8 * k, 70 * k);
      if (to) { this.walkTo(b, t, to, 2.4); b.act.hurry = true; }
      else b.act = { kind: "look", t0: t, until: t + 0.6 };          // nowhere better: it eyes them, and tries again in a moment
      return;
    }
    const to = this.refuge(b, people, 26 * k, 150 * k);
    if (to) {
      const d = Math.hypot(to[0] - b.x, to[1] - b.y);
      b.act = { kind: "fly", t0: t, until: t + Math.max(0.5, d / (this.flySpeed * Math.max(0.4, k))), from: [b.x, b.y, b.s], to, high: (12 + d * 0.22) * Math.max(0.5, k) };
      if (this.turns) b.dir = Math.sign(to[0] - b.x) || b.dir;
    } else this.leave(b, t);
    // and the ones close by go up with it
    for (const o of this.birds) if (o !== b && o.startle == null && !o.away && o.act.kind !== "fly" && o.act.kind !== "leave" && this.gap(o, b.x, b.y) < 90) o.startle = t + 0.05 + 0.3 * o.rand();
  }
  /** Off over the rooftops (out of the picture), to come back after `back` seconds. */
  leave(b, t) {
    const side = b.x < W / 2 ? -1 : 1;
    b.act = { kind: "leave", t0: t, until: t + 2 + b.rand(), from: [b.x, b.y, b.s], to: [b.x + side * (260 + 200 * b.rand()), b.y - 30 - 50 * b.rand(), b.s], high: 300 };
    if (this.turns) b.dir = side;
  }
  walkTo(b, t, to, pace = 1) {
    const d = Math.hypot(to[0] - b.x, (to[1] - b.y) * 1.5), speed = this.walkSpeed * pace * Math.max(0.35, this.sizeAt(b.y));
    if (this.treads && Math.abs(to[1] - b.y) > 0.5) b.act = { kind: "hop", t0: t, until: t + 0.35, from: [b.x, b.y, b.s], to };      // up or down a step: a hop
    else b.act = { kind: "walk", t0: t, until: t + Math.max(0.2, d / speed), from: [b.x, b.y, b.s], to };
    if (this.turns) b.dir = Math.sign(to[0] - b.x) || b.dir;
  }
  /**
   * For scripts: the birds near a place go up (all of them, with no place), as if somebody had rushed at them: a "Chase".
   * They take the place for somebody walking there for a second and a half, and keep clear of it.
   */
  scare(at = null, radius = null) {
    const t = this.simT / 1000, r = radius ?? Math.max(this.shy, 150);
    if (at) this.chaser = { x: at[0], y: at[1], walking: true, until: t + 1.5 };
    for (const b of this.birds) {
      if (b.away || b.act.kind === "fly" || b.act.kind === "leave" || b.act.kind === "arrive" || b.act.kind === "away") continue;
      if (!at || this.gap(b, at[0], at[1]) < r) b.startle = t + 0.02 + b.rand() * 0.25;
    }
    return this;
  }
  /** What a bird on the ground does next. */
  next(b, t, calm, people) {
    const m = this.moves, w = calm ? { stand: m.stand * 2, look: m.look * 1.5, peck: m.peck * 0.5, walk: m.walk * 0.5, turn: m.turn * 0.5, away: 0 } : { ...m };
    if (!this.turns) w.turn = 0;
    if (!this.flies) w.away = 0;
    let r = b.rand() * Object.values(w).reduce((a, v) => a + v, 0), pick = "stand";
    for (const [name, v] of Object.entries(w)) { if (r < v) { pick = name; break; } r -= v; }
    const slow = calm ? 1.6 : 1;
    if (pick === "away") { this.leave(b, t); return; }               // now and then one flies off by itself, and comes back later
    if (pick === "walk") {
      const k = this.sizeAt(b.y), lo = Math.min(5 * k, this.span / 3), hi = 30 * k;
      for (let i = 0; i < 8; i++) {
        let p = this.place(b);
        if (!p) break;
        if (this.treads && b.rand() < 0.7) { const y = this.tread(p[0], b.y); if (y != null && inside(this.area, p[0], y)) p = [p[0], y, 0]; }     // (mostly along the same step)
        const d = Math.hypot(p[0] - b.x, p[1] - b.y);
        if (this.perch ? Math.abs(p[2] - b.s) > hi : d < lo || d > hi) continue;
        if (people.some((q) => this.gap({ x: p[0], y: p[1] }, q.x, q.y) < this.shy * 0.8)) continue;
        if (this.turns && Math.sign(p[0] - b.x) !== b.dir && Math.abs(p[0] - b.x) > 1.5) { b.act = { kind: "turn", t0: t, until: t + 0.2 * slow }; return; }
        this.walkTo(b, t, p, calm ? 0.6 : 1);
        return;
      }
      pick = m.peck > 0 ? "peck" : "stand";                          // (nowhere to go: something else, never a peck for birds that do not)
    }
    if (pick === "turn") b.act = { kind: "turn", t0: t, until: t + 0.2 * slow };
    else if (pick === "peck") b.act = { kind: "peck", t0: t, until: t + 0.7 * (1 + Math.floor(b.rand() * 4)) * slow };
    else if (pick === "look") b.act = { kind: "look", t0: t, until: t + (0.5 + b.rand() * 1.2) * slow };
    else b.act = { kind: "stand", t0: t, until: t + (0.8 + b.rand() * 2.2) * slow };
  }
  /** One step of thirty a second. */
  tick(t, calm, people) {
    if (this.chaser) { if (t < this.chaser.until) people = [...people, this.chaser]; else this.chaser = null; }
    for (const b of this.birds) {
      const a = b.act;
      if (a.kind === "away") {
        if (t < a.until) continue;
        const to = this.refuge(b, people, 0, Infinity);
        if (!to) { a.until = t + 3; continue; }
        const side = to[0] < W / 2 ? -1 : 1;
        b.away = false;
        b.act = { kind: "arrive", t0: t, until: t + 2 + b.rand(), from: [to[0] + side * (260 + 160 * b.rand()), to[1] - 40, to[2]], to, high: 300 };
        b.dir = Math.sign(to[0] - b.act.from[0]) || b.dir;
        continue;
      }
      if (a.kind === "fly" || a.kind === "leave" || a.kind === "arrive") {
        if (t < a.until) continue;
        if (a.kind === "leave") { b.away = true; b.act = { kind: "away", until: t + within(this.back, b.rand()) }; continue; }
        [b.x, b.y, b.s] = a.to; b.alt = 0;
        b.act = { kind: "stand", t0: t, until: t + 0.4 + b.rand() * 0.8 };
        continue;
      }
      if (a.kind === "walk" || a.kind === "hop") {                  // where it has got to (and, at the end, where it stands)
        const u = t >= a.until ? 1 : clamp((t - a.t0) / (a.until - a.t0));
        if (this.perch) { b.s = a.from[2] + (a.to[2] - a.from[2]) * u; [b.x, b.y] = along(this.perch, b.s); }
        else { b.x = a.from[0] + (a.to[0] - a.from[0]) * u; b.y = a.from[1] + (a.to[1] - a.from[1]) * u; }
      }
      if (b.startle != null && t >= b.startle) { this.startle(b, t, calm, people); continue; }
      if (people.length && this.threat(b, people)) { this.startle(b, t, calm, people); continue; }
      if (t >= a.until) {
        if (a.kind === "turn") b.dir = -b.dir;
        this.next(b, t, calm, people);
      }
    }
  }
  update(calm, people) {
    let moved = this.fresh;
    while (this.simT + TICK <= this.time) { this.simT += TICK; this.tick(this.simT / 1000, calm, people || []); moved = true; }
    if (!moved) return;                                              // (nothing changes between the steps of thirty a second)
    const t = this.simT / 1000;
    for (const b of this.birds) {
      this.show(b, t);
      const s = b.sprite, n = b.next;
      if (n.hidden) { s.hidden = true; s.want = false; continue; }      // (flown off: gone at once)
      s.want = s.hidden || s.pic !== n.pic || Math.round(s.x) !== Math.round(n.x) || Math.round(s.y) !== Math.round(n.y) || Math.round(s.alt || 0) !== Math.round(n.alt);
      s.urgent = n.moving;                                               // (a bird on the move goes before one that only pecks)
      if (s.want && this.fresh) s.grant();
    }
    this.fresh = false;
    this.drawn = this.birds.filter((b) => !b.away).length;
  }
  /** Its turn: the bird's sprite shows where it is now, and how. */
  grant(s) { const n = s.bird.next; if (!n || n.hidden) return; s.place(n.x, n.y); s.alt = n.alt; s.pic = n.pic; s.hidden = false; }
  reveal(on) { for (const b of this.birds) b.sprite.hidden = !on || b.away || !b.sprite.pic; }
  /** Where the bird is at t, and its picture (b.next): what it is doing (`pose`) and how far through it (`n`, a count of frames). */
  show(b, t) {
    const a = b.act;
    if (b.away || a.kind === "away") { b.next = { hidden: true }; return; }
    let x = b.x, y = b.y, alt = 0, pose = "stand", n = 0;
    const u = a.until > a.t0 ? clamp((t - a.t0) / (a.until - a.t0)) : 1, since = t - (a.t0 || 0);
    if (a.kind === "walk") {
      if (!this.frames || this.frames.lists.walk) { pose = "walk"; n = Math.floor(since * 8); }
      else alt = Math.abs(Math.sin(since * Math.PI * 4)) * 1.5;      // no frames of it walking: it hops
    } else if (a.kind === "hop") {                                     // up or down a step, wings half open
      alt = (2 + Math.abs(a.to[1] - a.from[1]) * 0.6) * Math.sin(Math.PI * u) * Math.max(0.5, this.sizeAt(y));
      pose = "takeoff";
    } else if (a.kind === "fly" || a.kind === "leave" || a.kind === "arrive") {
      const e = a.kind === "fly" ? u * u * (3 - 2 * u) : u;
      x = a.from[0] + (a.to[0] - a.from[0]) * e; y = a.from[1] + (a.to[1] - a.from[1]) * e;
      alt = a.kind === "fly" ? a.high * 4 * u * (1 - u) : a.kind === "leave" ? a.high * Math.pow(u, 1.6) : a.high * Math.pow(1 - u, 1.6);
      const L = this.frames && this.frames.lists, gliding = L && L.glide && ((a.kind === "arrive" && u > 0.45 && u < 0.85) || (a.until - a.t0 > 1 && since % 1.1 > 0.75));
      pose = a.kind !== "arrive" && since < 0.15 ? "takeoff" : a.kind !== "leave" && a.until - t < 0.15 ? "land" : gliding ? "glide" : "fly";
      n = Math.floor(since * 13);
    } else if (a.kind === "peck") {
      const m = since % 0.7;
      if (m < 0.38) { pose = "peck"; n = m < 0.12 || m >= 0.28 ? 0 : 1; }
    } else if (a.kind === "look") pose = "look";
    else if (a.kind === "turn") pose = "turn";
    else n = Math.floor((since + b.i) / 1.7);                         // standing: a painted bird with two stand frames shifts now and then
    const ground = a.kind === "leave" ? a.from[1] : a.kind === "arrive" ? a.to[1] : y;
    b.next = { hidden: false, x, y, alt, pic: this.picFor(pose, n, b.dir, ground, alt), moving: a.kind !== "stand" && a.kind !== "look" && a.kind !== "peck" && a.kind !== "turn" };
  }
  picFor(pose, n, dir, ground, alt = 0) {
    const f = this.frames;
    if (f) {
      const L = f.lists, list = { takeoff: L.takeoff || L.land || L.fly, land: L.land || L.takeoff || L.fly, glide: L.glide || L.fly, fly: L.fly, peck: L.peck, walk: L.walk, look: L.look, turn: L.turn }[pose] || L.stand;
      const i = pose === "peck" ? Math.min(n, list.length - 1) : pose === "fly" && list.length === 3 ? [0, 1, 2, 1][n % 4] : n % list.length;
      const k = (f.sizeAt != null && this.scene ? this.sizeAt(ground) / Math.max(0.05, scaleAt(this.scene, f.sizeAt)) : 1) * this.k;
      const pic = paintedBird(list[i], k, f.mirror && dir * f.face < 0, f.foot, alt < 0.5 ? f.shadow : null);       // (its shadow only while it is on the ground)
      if (pic) return pic;
    }
    const drawn = pose === "land" || pose === "takeoff" ? "fly0" : pose === "glide" ? "fly1" : pose === "fly" ? ["fly0", "fly1", "fly2", "fly1"][n % 4] : pose === "walk" ? `walk${n % 2}` : pose === "peck" ? `peck${n}` : pose;
    return drawnBird(this.kind, drawn, this.length * this.sizeAt(ground) * this.k, dir < 0);
  }
  picture(sprite) {
    const p = sprite.pic;
    if (!p) return null;
    return sprite.alt ? { canvas: p.canvas, ox: p.ox, oy: p.oy + sprite.alt } : p;
  }
  seek(ms) { this.time = ms * (this.calm ? this.slow : 1); this.restart(); this.update(!!this.calm, []); if (!this.shown) this.reveal(false); }
}

function Birds(host, spec, n) {
  const kind = spec.kind === "flock" || spec.kind === "flyers" ? spec.kind : spec.lanes || spec.circle ? "flyers" : "flock";
  return kind === "flyers" ? new Flyers(host, spec, n) : new Flock(host, spec, n);
}

// ---------------------------------------------------------------- the door in time
/**
 * portal: the door in time, as a ripple in the paint (round ten; the author chose it on 9 October from six looks in the
 * portal study, with the settings that are the defaults below). Nothing is drawn over the painting. Its own pixels, in
 * the box the door can reach, are read once when the scene is up (from the backdrop, with any cut-out that lies under
 * the door composited in) and written back displaced each picture: rings travel out from the door's middle and the
 * paint bends along each one, a crest catching the lamplight a shade lighter and a trough a shade darker (the paint is
 * wet), the rings fading with distance and the heart holding a soft light of the paint's own colour. The rings' strength
 * and phase wander round the circle and across the wall from seeded tables, so it is paint, not geometry. A coin-sized
 * door gets a brighter heart and a wet rim, so it shows on a dark floor and on bright sand alike. Outside the door's
 * reach the picture is left alone (those pixels are not drawn), so the door sits in the picture at its depth: a man who
 * walks in front of it is drawn over it, and the paint behind it is its own.
 *
 *   at           [x, y]: the middle of the door, wide open
 *   r            half its height, wide open (the coin doors are 10 or 11; the chamber's doorway 96)
 *   wide         how wide it is beside its height: 1 for a round hole; the chamber's doorway is 0.48
 *   keep         [x0, x1]: the bare wall it is in. Paint beyond those columns is left as it is (the bending fades out
 *                over eight pixels), so the furniture beside a door stays straight.
 *   rise         true: its middle rises out of `at` as it opens, by its radius (the sun on the highway)
 *   under        cut-outs that lie behind the door in its box, read into the paint it bends: their ids, or pictures
 *                laid over the backdrop, { src, x, y, alpha }. `alpha` (1 if not said) is how much of the picture
 *                shows; a script that changes it calls refresh(), and the door bends the paint as it is now (the road
 *                sign comes out of the rings saying something else: highway.js)
 *   light        true: the light the scene draws over the paint (its live layer: a beam on the wall, a spot of sun) is
 *                read into the paint too, so the door bends the lit wall and does not hide the light. A script calls
 *                refresh() when that light has changed (the beam has come on). Pictures the live layer shows by
 *                address are not read this way: name them in `under`.
 *   open         how far open it starts: 0 (shut: nothing drawn) to 1 (wide). Scripts: g.effects.get("door").open(k)
 *   strength     how hard the paint bends and shades, 0 to 1 (0.45)
 *   bend         what share of that goes into the bending (0.6): the author's "less motion" setting on the study page,
 *                kept as the look; the game's own "less motion" takes it to 0.6 of that again, and halves the clock
 *   rate         how fast the door's own time runs (1.5: the study page at speed 3 with less motion on)
 *   size         the door drawn this much bigger than `r` (1.11, the author's setting): the rings reach a little past it
 *   pale         the colour of its light: the paint's own colours are mixed toward it (never keyed: time's colour
 *                belongs to no place, as the old rings' did not)
 *   seed, base or plane (its depth), when: as every kind. It is drawn thirty times a second (fifteen when calm).
 *
 * open(k, { wide, at, scale, flicker }) for the moments the scripts play: the chamber door opens round and stretches
 * to a doorway (`wide` tweened 1 to 0.48); the flashlight opens a plate-sized round hole off to one side (`at` an offset
 * from the door's middle, `scale` 0.11 of its size); its batteries make it `flicker`; the coin's wink is `scale` over a
 * moment. The options hold until given again; open(k) alone keeps them.
 */
const REACH = 1.32;                                     // how far the rings reach, in radii
/** How the door opens: `k` 0 (shut) to 1 (wide). The radius grows fast at first (a small disturbance appears at once); the bending follows. */
const opening = (k) => (k <= 0 ? { k: 0, Rk: 0, amp: 0 } : { k, Rk: 0.07 + 0.93 * Math.pow(k, 0.8), amp: Math.pow(k, 0.55) });
// A sine table: the loop below asks for a few hundred thousand sines a second.
const SN = 4096, SIN = new Float32Array(SN), SK = SN / TAU;
for (let i = 0; i < SN; i++) SIN[i] = Math.sin((i / SN) * TAU);
const sinT = (ph) => SIN[((ph * SK) | 0) & (SN - 1)], cosT = (ph) => SIN[(((ph * SK) | 0) + 1024) & (SN - 1)];
/** A smooth function round the circle, -1 to 1: three harmonics with seeded phases, as a table of 256 over the angle. */
function roundTable(seed, lane, harmonics) {
  const t = new Float32Array(256);
  let most = 0;
  for (let i = 0; i < 256; i++) {
    const th = (i / 256) * TAU;
    let v = 0;
    harmonics.forEach((h, j) => { v += (1 / (j + 1)) * Math.sin(h * th + rnd(seed, lane, j) * TAU); });
    t[i] = v; most = Math.max(most, Math.abs(v));
  }
  for (let i = 0; i < 256; i++) t[i] /= most || 1;
  return t;
}
/** Smooth noise, -1 to 1, over a box of the picture (x0, y0, w by h), in cells about `cell` pixels across, two octaves: the paint's own unevenness. */
function noiseField(seed, lane, x0, y0, w, h, cell) {
  const f = new Float32Array(w * h), val = (cx, cy, o) => rnd(seed, lane + o * 7, cx, cy) * 2 - 1;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    let v = 0, amp = 1, c = cell;
    for (let o = 0; o < 2; o++) {
      const px = (x + x0) / c, py = (y + y0) / c, ix = Math.floor(px), iy = Math.floor(py);
      const fx = px - ix, fy = py - iy, ex = fx * fx * (3 - 2 * fx), ey = fy * fy * (3 - 2 * fy);
      const a = val(ix, iy, o), b = val(ix + 1, iy, o), cc = val(ix, iy + 1, o), d = val(ix + 1, iy + 1, o);
      v += amp * ((a + (b - a) * ex) * (1 - ey) + (cc + (d - cc) * ex) * ey);
      amp *= 0.5; c *= 0.5;
    }
    f[y * w + x] = v / 1.5;
  }
  return f;
}
class Portal extends Effect {
  constructor(host, spec, n) {
    super(host, spec, n);
    const s = spec;
    if (!isPoint(s.at)) throw new Error("a portal needs `at`: [x, y], the middle of the door");
    this.at = [s.at[0], s.at[1]];
    this.r = Math.max(2, num(s.r, 12)) * Math.max(0.1, num(s.size, 1.11));
    this.wide0 = clamp(num(s.wide, 1), 0.05, 4);
    this.keep = Array.isArray(s.keep) && s.keep.length === 2 && s.keep.every((v) => typeof v === "number") ? s.keep : null;
    this.rise = !!s.rise;
    this.under = Array.isArray(s.under) ? s.under : [];
    this.light = !!s.light;
    this.snap = null; this.snapGen = 0;                    // the live layer as pixels, when `light` asks for it, and which asking it answers
    this.strength = clamp(num(s.strength, 0.45));
    this.bend = clamp(num(s.bend, 0.6));
    this.rate = Math.max(0.05, num(s.rate, 1.5));
    this.pale = rgbOf(s.pale, [255, 243, 220]);
    this.openK = clamp(num(s.open, 0));
    this.opts = { wide: this.wide0, at: [0, 0], scale: 1, flicker: false };
    this.fps = 30; this.calmFps = 15;
    this.sprite = this.mote().place(this.at[0], this.at[1]);
    this.src = null; this.step = null; this.dirty = true; this.go = false; this.drawnCalm = null; this.touched = 0;
    this.build();
  }
  /** The box the door can reach wide open, on the picture, and the per-pixel tables over it. */
  build() {
    const R0 = this.r, wide = this.wide0, [cx, cy0] = this.at, cy = this.rise ? cy0 - R0 : cy0;
    const fx0 = Math.max(0, Math.floor(cx - R0 * REACH * wide) - 2), fx1 = Math.min(W - 1, Math.ceil(cx + R0 * REACH * wide) + 2);
    const fy0 = Math.max(0, Math.floor(cy - R0 * REACH) - 2), fy1 = Math.min(H - 1, Math.ceil(cy + R0 * REACH + (this.rise ? R0 : 0)) + 2);
    const fw = fx1 - fx0 + 1, fh = fy1 - fy0 + 1, n = fw * fh;
    Object.assign(this, { R0, fx0, fy0, fw, fh, cx: cx - fx0, cy: cy - fy0 });         // (cx, cy: the middle, wide open, in the box)
    const RR = new Float32Array(n), UX = new Float32Array(n), UY = new Float32Array(n), TH = new Uint8Array(n);
    for (let y = 0; y < fh; y++) for (let x = 0; x < fw; x++) {
      const i = y * fw + x, ex = (x - this.cx) / wide, ey = y - this.cy, rr = Math.hypot(ex, ey) || 1e-3;
      RR[i] = rr; UX[i] = ex / rr; UY[i] = ey / rr; TH[i] = ((Math.atan2(ey, ex) / TAU) * 256 + 256) & 255;
    }
    const seed = this.seed;
    this.N1 = noiseField(seed, 1, fx0, fy0, fw, fh, Math.max(6, R0 * 0.28));    // the paint's own unevenness, broad
    this.N2 = noiseField(seed, 2, fx0, fy0, fw, fh, Math.max(4, R0 * 0.13));    // and fine: the marks
    this.ANG = roundTable(seed, 5, [3, 4, 7]);                                     // rings a little stronger here, weaker there
    this.PHS = roundTable(seed, 6, [2, 5, 6]);                                     // and a little ahead or behind
    let KX = null;                                                                 // how much of the bend each column gets: 1 inside the bare wall, 0 beyond it
    if (this.keep) {
      KX = new Float32Array(fw);
      const [ka, kb] = this.keep;
      for (let x = 0; x < fw; x++) { const X = x + fx0; KX[x] = ease(ka - 6, ka + 2, X) * ease(kb + 6, kb - 2, X); }
    }
    Object.assign(this, { RR, UX, UY, TH, KX, out: null, pair: new Pair(fw, fh) });        // (`out`, the pixels of one picture, is made with the first)
  }
  /** How far open, and the moment's shape: see the top. */
  open(k, options = null) {
    this.openK = clamp(num(k, 0));
    if (options && typeof options === "object") {
      const o = this.opts;
      if (typeof options.wide === "number") o.wide = clamp(options.wide, 0.05, 4);
      if (isPoint(options.at)) o.at = [options.at[0], options.at[1]];
      if (typeof options.scale === "number") o.scale = clamp(options.scale, 0.01, 4);
      if (options.flicker !== undefined) o.flicker = !!options.flicker;
    }
    this.dirty = true;
    this.sprite.hidden = !(this.shown && this.openK > 0);
    this.host.frame(0);
    return this;
  }
  get isOpen() { return this.openK; }
  /** Read the paint again: the light over it has changed (`light`), or a cut-out under it has. */
  refresh() { this.src = null; this.snap = null; this.snapGen++; this.dirty = true; this.host.frame(0); return this; }
  reveal(on) { this.sprite.hidden = !(on && this.openK > 0); }
  restart() { this.step = null; }
  update(calm) {
    if (this.step === null) return;
    const fps = calm ? this.calmFps : this.fps;
    this.sprite.want = this.dirty || Math.floor((this.time * fps) / 1000) !== this.step || calm !== this.drawnCalm;
  }
  grant() { this.go = true; }
  /** Read the paint the door bends: the backdrop in its box, and whatever cut-outs lie under it there. Once a scene is up.
      False until the backdrop has been painted (the pictures come in their own time). */
  read() {
    const g = this.game, view = g.view, cast = view.cast, { fx0, fy0, fw, fh } = this;
    if (!view.backdrop) return false;
    if (this.light && !this.snap) {                                           // the light over the paint, as pixels: asked for once, answered in its own time
      if (!this.snapping && view.snapshotLive) {
        const gen = this.snapGen;
        this.snapping = view.snapshotLive().then((c) => { this.snapping = null; if (gen !== this.snapGen) return; this.snap = c || false; this.src = null; this.dirty = true; this.host.frame(0); });
      }
      if (this.snap !== false) return false;
    }
    const tmp = canvasOf(fw, fh), ctx = tmp.getContext("2d", { willReadFrequently: true });
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(view.backdrop, fx0, fy0, fw, fh, 0, 0, fw, fh);
    const paint = ctx.getImageData(0, 0, fw, fh).data;                            // (nothing painted yet? then not yet: the picture comes in its own time)
    let painted = false;
    for (let i = 3; i < paint.length; i += 4) if (paint[i] > 0) { painted = true; break; }
    if (!painted) return false;
    if (this.snap) ctx.drawImage(this.snap, fx0, fy0, fw, fh, 0, 0, fw, fh);
    for (const u of this.under) {
      if (typeof u === "string") {
        const cut = cast.get(u);
        if (!(cut instanceof Cutout) || cut.hidden) continue;
        const pic = cut.picture(cast.palette, cast.calm);
        if (!pic) return false;
        const x = Math.round(cut.x) - Math.round(pic.ox) - fx0, y = Math.round(cut.y) - Math.round(pic.oy) - fy0;
        if (pic.w == null) ctx.drawImage(pic.canvas, x, y); else ctx.drawImage(pic.canvas, 0, 0, pic.sw, pic.sh, x, y, pic.w, pic.h);
      } else if (u && typeof u.src === "string") {
        const img = got(u.src);
        if (!img) return false;
        const alpha = clamp(num(u.alpha, 1));
        if (alpha <= 0) continue;
        ctx.globalAlpha = alpha;
        ctx.drawImage(img, num(u.x, 0) - fx0, num(u.y, 0) - fy0);
        ctx.globalAlpha = 1;
      }
    }
    this.src = ctx.getImageData(0, 0, fw, fh).data;
    return true;
  }
  picture(sprite, calm) {
    if (this.openK <= 0) return null;
    if (!this.src && !this.read()) return null;                             // (the backdrop is not painted yet: next frame)
    const fps = calm ? this.calmFps : this.fps, step = Math.floor((this.time * fps) / 1000), go = this.go;
    this.go = false;
    if (this.step === null || (go && (this.dirty || step !== this.step || calm !== this.drawnCalm))) {    // (the first picture at once; after that, in its turn)
      this.step = step; this.drawnCalm = calm; this.dirty = false;
      this.render(step / fps, calm);
      this.pair.next().putImageData(this.out, 0, 0);
      this.drawn = 1;
    }
    return { canvas: this.pair.canvas, ox: this.at[0] - this.fx0, oy: this.at[1] - this.fy0 };
  }
  /** The door at a moment of its own time `t` (seconds), into `out`: the painting bent, where the rings reach; nothing elsewhere. */
  render(t, calm) {
    if (!this.out) this.out = new ImageData(this.fw, this.fh);
    const o = this.out.data, src = this.src, { fw, fh, RR, UX, UY, TH, N1, N2, ANG, PHS, KX, pale } = this, opts = this.opts;
    o.fill(0);
    const tau = t * this.rate, ok = opening(this.openK), s0 = this.strength;
    let flick = 1;
    if (opts.flicker && !calm) { const ph = (tau % 1.7) / 1.7; flick = ph < 0.4 ? 1 : ph < 0.55 ? 0.55 : ph < 0.7 ? 0.9 : 0.4; }
    const sAmp = s0 * this.bend * (calm ? 0.6 : 1) * ok.amp * flick;
    const R = this.R0 * ok.Rk * opts.scale;
    if (!(R > 0.5) || !(sAmp > 0)) { this.touched = 0; return; }
    const wide = opts.wide, own = wide === this.wide0 && opts.at[0] === 0 && opts.at[1] === 0;      // (the tables are for the door's own shape; another shape is worked out as it goes)
    const shift = this.rise ? Math.round(this.R0 - R) : 0;                                            // the middle rises out of the point as it opens
    const cx = this.cx + opts.at[0], cy = this.cy + shift + opts.at[1];
    const x0 = Math.max(0, Math.floor(cx - R * REACH * wide) - 1), x1 = Math.min(fw - 1, Math.ceil(cx + R * REACH * wide) + 1);
    const y0 = Math.max(own ? shift : 0, Math.floor(cy - R * REACH) - 1), y1 = Math.min(fh - 1, Math.ceil(cy + R * REACH) + 1);
    if (x1 < x0 || y1 < y0) { this.touched = 0; return; }
    const lam = Math.max(7, 0.3 * R), kl = TAU / lam, om = 2.0, breath = 1 + 0.1 * sinT(0.45 * tau);
    const small = clamp((34 - R) / 30);                                                               // a coin-sized door: a brighter heart, and a wet rim
    const A = sAmp * (0.07 * R + 1.2) * breath, Lc = sAmp * (0.14 + 0.7 * small) * (0.8 + 0.2 * sinT(0.45 * tau + 1)), dark = 0.34 * sAmp * small;
    const shadeK = 0.3 * s0, wm = fw - 1.001, hm = fh - 1.001;
    const ENV = new Float32Array(257);                                                                // the rings' strength by distance: a calm middle (the stone has sunk), fading out
    for (let k = 0; k <= 256; k++) { const u = (k / 256) * REACH; ENV[k] = (0.35 + 0.65 * ease(0, 0.3, u)) * Math.pow(1 - u / REACH, 1.5); }
    let touched = 0;
    for (let y = y0; y <= y1; y++) {
      const trow = (y - shift) * fw, orow = y * fw;
      for (let x = x0; x <= x1; x++) {
        let rr, ux, uy, th;
        if (own) { const i = trow + x; rr = RR[i]; ux = UX[i]; uy = UY[i]; th = TH[i]; }
        else { const ex = (x - cx) / wide, ey = y - cy; rr = Math.hypot(ex, ey) || 1e-3; ux = ex / rr; uy = ey / rr; th = ((Math.atan2(ey, ex) / TAU) * 256 + 256) & 255; }
        const u = rr / R;
        if (u >= REACH) continue;
        const i = orow + x, n1 = N1[i], env = ENV[((u / REACH) * 256) | 0], a = A * env * (1 + 0.3 * ANG[th]) * (1 + 0.25 * n1);
        const ph = rr * kl - om * tau + 0.8 * PHS[th] + 0.7 * n1, sn = sinT(ph), cs = cosT(ph), d = a * sn;
        // the paint, read from where the bend brings it (blended from the four pixels round the point)
        let sx = x + d * ux * wide, sy = y + d * uy;
        if (sx < 0) sx = 0; else if (sx > wm) sx = wm;
        if (sy < 0) sy = 0; else if (sy > hm) sy = hm;
        const sx0 = sx | 0, sy0 = sy | 0, fx = sx - sx0, fy = sy - sy0;
        const i00 = (sy0 * fw + sx0) << 2, i10 = i00 + 4, i01 = i00 + (fw << 2), i11 = i01 + 4;
        const w00 = (1 - fx) * (1 - fy), w10 = fx * (1 - fy), w01 = (1 - fx) * fy, w11 = fx * fy;
        let r = src[i00] * w00 + src[i10] * w10 + src[i01] * w01 + src[i11] * w11;
        let g = src[i00 + 1] * w00 + src[i10 + 1] * w10 + src[i01 + 1] * w01 + src[i11 + 1] * w11;
        let b = src[i00 + 2] * w00 + src[i10 + 2] * w10 + src[i01 + 2] * w01 + src[i11 + 2] * w11;
        let sl = shadeK * a * kl * (1 + 0.4 * N2[i]); if (sl > 0.3) sl = 0.3;
        if (cs < 0) { const sh = 1 + sl * cs; r *= sh; g *= sh; b *= sh; }                                   // the trough, in shade
        else { const l = 0.55 * sl * cs, sh = 1 + 0.45 * sl * cs; r = r * sh + l * (pale[0] - r); g = g * sh + l * (pale[1] - g); b = b * sh + l * (pale[2] - b); }   // the crest, catching the light
        if (dark > 0 && u > 0.45 && u < 1.15) { const sh = 1 - dark * ease(0.45, 0.8, u) * ease(1.15, 0.85, u); r *= sh; g *= sh; b *= sh; }
        if (u < 0.5) { const l = Lc * (1 - u / 0.5) * (1 - u / 0.5); r += l * (pale[0] - r); g += l * (pale[1] - g); b += l * (pale[2] - b); }
        const j = i << 2;
        if (KX) { const k = KX[x]; if (k < 1) { r = src[j] + (r - src[j]) * k; g = src[j + 1] + (g - src[j + 1]) * k; b = src[j + 2] + (b - src[j + 2]) * k; } }
        o[j] = r; o[j + 1] = g; o[j + 2] = b; o[j + 3] = 255;
        touched++;
      }
    }
    this.touched = touched;
  }
}

const KINDS = { smoke: Smoke, flame: Flame, embers: Embers, ripples: Ripples, stream: Stream, shimmer: Shimmer, birds: Birds, sway: Sway, portal: Portal };

// ---------------------------------------------------------------- the scene's moving things, together
/**
 * game.effects. The game makes one, and hands it each scene as the scene is built (enter). Each frame of the game clock,
 * before the cast is painted, it moves time on for every moving thing and tells it whether it is showing.
 *   get(id)         one of them, for a script: .show(false), .show(true), .auto() (back to its `when`)
 *   add(spec)       put another on the stage (it goes when the scene does)
 *   time            ms of the scene's time, as the moving things have seen it
 *   seek(ms)        jump to that moment (for tests and screenshots); hold(true) stops time, hold(false) lets it go
 *   enabled         false takes all of them away (?nofx in the page address does the same from the start)
 *   stats()         how much is moving: things, sprites, specks
 */
export class Effects {
  constructor(game) {
    this.game = game;
    this.list = [];
    this.time = 0;
    this.held = false;
    this.owner = undefined;              // the scene they belong to
    this.scene = null;
    this.place = "";
    this.on = true;
    try { this.on = !new URLSearchParams(location.search).has("nofx"); } catch { /* no address to read */ }
    // How many pictures of moving things may change in one frame. The cast repaints what has changed in patches, up to six
    // of them (more, and it paints the whole layer: cast.js, Cast.update), and the people need theirs.
    this.budget = 4;
    this.granted = 0; this.deferred = 0;                // turns given and turns put off, since the scene began
    if (game && game.clock) game.clock.every((dt) => this.frame(dt));
    if (game && game.store && game.store.on) game.store.on(() => this.frame(0));       // (a `when` is read again as soon as the story changes, as a cut-out's is)
  }
  get enabled() { return this.on; }
  set enabled(on) { this.on = !!on; this.frame(0); }

  /**
   * Put a scene's moving things (`fx`) on the stage. The game calls this as it builds the scene, after its cut-outs are
   * on the stage (a sway needs its cut-out). Resolves when every painted frame they can show has arrived.
   */
  enter(scene) {
    this.drop(scene);
    let specs = !scene || !scene.fx ? [] : scene.fx;
    if (typeof specs === "function") { try { specs = specs(this.game); } catch (err) { console.warn(`The moving things of ${this.place} could not be worked out:`, err); specs = []; } }
    for (const spec of Array.isArray(specs) ? specs : []) this.add(spec, true);
    this.frame(0);
    return Promise.all(this.list.flatMap((e) => (e.frames ? [...Object.values(e.frames.lists).flat(), ...(e.frames.shadow ? [e.frames.shadow] : [])] : [])).map(fetchPicture));
  }
  drop(scene = null) { this.list = []; this.time = 0; this.owner = scene; this.scene = scene; this.place = scene ? scene.id : ""; this.granted = this.deferred = 0; }

  /** Another moving thing, on the stage now. It goes when the scene does. */
  add(spec, quiet = false) {
    if (!quiet && this.owner !== this.game.scene) this.drop(this.game.scene);
    if (!spec || typeof spec !== "object") return null;
    spec = keyedSpec(spec);                                         // its colours in the paints of the scene (look.js)
    const Kind = KINDS[spec.type];
    if (!Kind) { console.warn(`A moving thing of a kind the engine does not know: "${spec.type}" (${this.place || "added by a script"}). The kinds are ${Object.keys(KINDS).join(", ")}.`); return null; }
    let e;
    try { e = new Kind(this, spec, this.list.length); }
    catch (err) { console.warn(`The moving thing "${spec.id || spec.type}" (${this.place || "added by a script"}) was left out: ${err.message}`); return null; }
    if (this.list.some((o) => o.id === e.id)) console.warn(`Two moving things in ${this.place || "this scene"} are called "${e.id}".`);
    for (const s of e.sprites) this.game.view.cast.add(s);
    if (e.attach) e.attach();
    this.list.push(e);
    if (!quiet) { if (e.frames) [...Object.values(e.frames.lists).flat(), ...(e.frames.shadow ? [e.frames.shadow] : [])].forEach(fetchPicture); this.frame(0); }
    return e;
  }
  get(id) { return this.list.find((e) => e.id === id) || null; }

  /** Each frame of the game clock (it stops while the game is paused). */
  frame(dt) {
    const g = this.game;
    if (this.list.length && this.owner !== g.scene && this.owner !== null) this.drop();     // the scene has gone (the title, or another scene being built)
    if (!this.list.length) return;
    const cast = g.view.cast, calm = !!cast.calm, step = this.held ? 0 : dt;
    this.time += step;
    let people = null;
    for (const e of this.list) {
      if (e instanceof Flock && !people) { people = []; for (const s of cast.items.values()) if (s instanceof Figure && !s.hidden && s.opacity > 0) people.push(s); }
      e.advance(step, calm, people);
    }
    // Whose picture changes this frame: no more than the budget, a bird on the move first, then whoever has waited longest.
    // The rest wait a frame or two, which nobody sees; the cast goes on repainting patches, not the whole layer.
    let wanting = null;
    for (const e of this.list) if (e.shown) for (const s of e.slots()) if (s.want) (wanting || (wanting = [])).push(s);
    if (!wanting) return;
    wanting.sort((a, b) => (b.urgent ? 1 : 0) - (a.urgent ? 1 : 0) || b.waits - a.waits);
    for (let i = 0; i < wanting.length; i++) {
      const s = wanting[i];
      if (i < this.budget) { s.waits = 0; s.grant(); this.granted++; } else { s.waits++; this.deferred++; }
    }
  }
  /** Jump every moving thing to this moment of the scene's time. Startled birds are put back: the flock is worked out as if nobody were about. */
  seek(ms) { this.time = ms; for (const e of this.list) e.seek(ms); this.frame(0); }
  hold(on = true) { this.held = !!on; return this; }
  stats() {
    let sprites = 0, specks = 0;
    for (const e of this.list) { if (!e.shown) continue; sprites += e.sprites.filter((s) => !s.hidden).length; specks += e.drawn; }
    return { things: this.list.length, shown: this.list.filter((e) => e.shown).length, sprites, specks, granted: this.granted, deferred: this.deferred };
  }
}

// ---------------------------------------------------------------- the paints
// A moving thing's colours go through the key of the scene, as the painted pictures and the people do (js/art/look.js;
// docs/DESIGN.md, "The paints"): those its description gives, and the engine's own (the defaults in the kinds above)
// where it gives none. Its painted frames come keyed already (tools/paint/postimp_key.py).
const DEFAULTS = {
  smoke: { color: "#d9d5cd" },
  flame: { color: "#fff0b3", edge: "#ff9a2e", core: "#fffbea", glowColor: "#ffb44d" },
  embers: { color: "#ffb347", cool: "#7a1d08", glowColor: "#ff8a3d" },
  ripples: { color: "#ffffff", trough: "#345c70" },
  stream: { color: "#b9d6e4", light: "#f4fbff" },
  shimmer: { color: "#fff4d6" },
};
/** A moving thing's description with its colours in the key of the scene; the same object when no key is in use. */
function keyedSpec(spec) {
  if (!keyId()) return spec;
  const out = { ...spec }, own = DEFAULTS[spec.type] || {};
  for (const k of ["color", "edge", "core", "cool", "light", "trough", "glowColor"]) {
    let v = spec[k];
    if (v === false || v === "none") continue;
    if (v === undefined) v = own[k];
    if (spec.type === "birds" && k === "color" && v === undefined && !spec.frames) v = "#2b2724";      // birds drawn as flyers
    if (typeof v !== "string") continue;
    out[k] = keyHex(v);
  }
  return out;
}

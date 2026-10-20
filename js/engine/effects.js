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
//   strip     a painted strip of country going by behind a window (the desert past a car's windows): NEVADA-12E, `Strip` below
//   bob       a painted cut-out (a boat, a barge) riding the water: rising and falling on the swell. ROME-13E, `Bob` below
//   drive     the world going by a car's side windows, as a pinhole camera moving forward sees it: the ground in perspective,
//             panoramas at their distances, posts and poles growing and sweeping past. DRIVE-16E, `Drive` below
//             (DRIVE-16F: and each thing's shadow laid on the ground in perspective, from the sun the scene gives)
//
// ROME-13E: a flock can also be sent somewhere by a script (`herd`: the geese into their pen) and made to strike a pose
// all at once (`pose`: the geese hissing): see Flock.herd.
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
import { picture as fetchPicture, got, hold } from "./assets.js";      // (DRIVE-16E: hold, for a drive's sheet of things)
import { scaleAt, DEPTH } from "./walk.js";
import { W, H } from "./grid.js";
import { keyHex, keyId } from "../art/look.js";

const { Figure, Cutout, PaintedFigure } = castKit;      // (NEVADA-12E: PaintedFigure, a person drawn from painted frames: birds take fright at him too)
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
  /** NEVADA-12E: the painted pictures it shows, fetched with the scene's: a flock's or flyers' frames, a strip's picture. */
  pics() { const f = this.frames; return f ? [...Object.values(f.lists).flat(), ...(f.shadow ? [f.shadow] : [])] : []; }
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

// ---------------------------------------------------------------- ROME-13E: a cut-out that rides the water
/**
 * bob: a cut-out of the scene's (`plane`: its id under `planes`; a boat, a barge) rises and falls on the swell, as it is
 * drawn (its state, its frame, where a script has put it): `amount` pixels up and down (1), over `period` seconds (5), as
 * two slow waves added together, so that it never ticks like a clock; seeded, on the game clock, and drawn on whole pixels,
 * as a cut-out at its own size always is. `tilt` (degrees; 0, none) rocks it as well, about the middle of its base line:
 * a turned copy of its picture for each step of a quarter of a degree, made once and kept (not for a cut-out a script shows
 * at another size, nor for one that also sways: those rise and fall without rocking). Its base, and so who is in front of
 * it and who behind, does not move; nor does its clickable area, nor its `solid` ground, nor anything a script does to it.
 * Cheap: its own picture is used as it is (no pixel is drawn again unless it rocks); only its place changes, a few times a
 * second at most, in its turn (Effects.budget), and the cast repaints its box. For less motion: half the amount (a bob of
 * one pixel then stays still) at half the pace. With a `sway` on the same cut-out both apply: it rises and falls as it stirs.
 */
const turnedOf = new WeakMap();                  // the turned copies of a cut-out's picture, by its canvas: Map(turn -> { canvas, pad })
class Bob extends Effect {
  constructor(host, spec, n) {
    super(host, spec, n);
    const s = spec;
    this.target = typeof s.plane === "string" ? s.plane : typeof s.of === "string" ? s.of : null;
    if (!this.target) throw new Error('bob needs the id of a cut-out: plane: "<its id>"');
    this.amount = Math.max(0, num(s.amount, 1)); this.period = Math.max(0.5, num(s.period, 5)); this.tilt = Math.abs(num(s.tilt, 0));
    this.fps = 10; this.calmFps = 5; this.slow = 0.5;          // (its swell is looked at ten times a second; its place changes far less often)
    const r = sequence(this.seed);
    this.phase = [r() * TAU, r() * TAU, r() * TAU]; this.beat = 1.53 + 0.14 * r();          // the second wave: a little quicker, never in step
    this.now = { lift: 0, turn: 0 }; this.due = this.now; this.fresh = true;                // what is drawn, and what its time asks for
    this.slot = { want: false, waits: 0, urgent: false, grant: () => { this.slot.want = false; this.now = this.due; } };
  }
  slots() { return [this.slot]; }
  restart() { this.fresh = true; }
  attach() {
    const cut = this.game.view.cast.get(this.target);
    if (!(cut instanceof Cutout)) { console.warn(`Bob "${this.id}": there is no cut-out called "${this.target}" in this scene's planes.`); return; }
    this.cut = cut;
    const own = cut.picture;                                         // (the cut-out's own way of making its picture, or a sway's)
    cut.picture = (palette, calm) => { const pic = own.call(cut, palette, calm); return this.ride(pic) || pic; };
  }
  /** Where the swell has it at t (seconds of its own time): how far it is lifted, in whole pixels, and how far it is
      turned, in quarter degrees. The two waves together reach 0.98 of the amount: half a pixel never makes a whole one. */
  at(t, calm) {
    const w = TAU / this.period, k = calm ? 0.5 : 1, [p0, p1, p2] = this.phase;
    const lift = Math.round(this.amount * k * (0.6 * Math.sin(w * t + p0) + 0.38 * Math.sin(w * this.beat * t + p1))) || 0;
    const turn = this.tilt ? Math.round(this.tilt * k * (0.7 * Math.sin(w * t + p0 + 1.3) + 0.28 * Math.sin(w * 1.27 * t + p2)) * 4) / 4 || 0 : 0;
    return { lift, turn };
  }
  update(calm) {
    const fps = calm ? this.calmFps : this.fps, due = this.at(Math.floor((this.time * fps) / 1000) / fps, calm);
    this.due = due;
    if (this.fresh) { this.fresh = false; this.now = due; this.slot.want = false; return; }       // (the first picture at once; after that, in its turn)
    this.slot.want = due.lift !== this.now.lift || due.turn !== this.now.turn;
    this.drawn = 1;
  }
  /** The cut-out's picture where the swell has it now (null: as it is). */
  ride(pic) {
    if (!pic || !pic.canvas || !this.shown) return null;
    const lift = this.now.lift;
    let turn = this.now.turn;
    if (turn && (pic.w != null || this.host.list.some((e) => e instanceof Sway && e.target === this.target))) turn = 0;     // (rocking only at its own size, and not while it sways)
    if (!turn) return lift ? { ...pic, oy: pic.oy + lift } : null;
    let kept = turnedOf.get(pic.canvas);
    if (!kept) turnedOf.set(pic.canvas, (kept = new Map()));
    let r = kept.get(turn);
    if (!r) kept.set(turn, (r = this.turned(pic, turn)));
    return { canvas: r.canvas, ox: pic.ox + r.pad, oy: pic.oy + r.pad + lift };
  }
  /** Its picture turned by `turn` degrees about the middle of its base line, hard-edged, on a canvas `pad` bigger all round. */
  turned(pic, turn) {
    const src = pic.canvas, cut = this.cut, left = Math.round(cut.x) - Math.round(pic.ox), top = Math.round(cut.y) - Math.round(pic.oy), b = cut.base;
    const [bx, by] = Array.isArray(b) ? [(b[0][0] + b[1][0]) / 2, (b[0][1] + b[1][1]) / 2] : [left + src.width / 2, typeof b === "number" ? b : top + src.height];
    const th = (turn * Math.PI) / 180, pad = Math.ceil(Math.hypot(src.width, src.height) * Math.abs(Math.sin(th))) + 2;
    const c = canvasOf(src.width + pad * 2, src.height + pad * 2), ctx = c.getContext("2d"), px = bx - left + pad, py = by - top + pad;
    ctx.imageSmoothingEnabled = false;
    ctx.translate(px, py); ctx.rotate(th); ctx.translate(-px, -py);
    ctx.drawImage(src, pad, pad);
    return { canvas: c, pad };
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

const FRAME_NAMES = ["stand", "look", "peck", "walk", "turn", "fly", "takeoff", "land", "glide", "flap", "bank", "shadow", "run"];     // (ROME-13E: run, a dash: a herded flock's)
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
/**
 * ROME-13E: a scene's `fx` as a list. It may be a function of the game, for a scene whose moving things follow the story
 * (a flock that has been herded into its pen is given the pen as its area from a fact, as the scene is entered: Effects.enter
 * asks it of the game). Asked here of a stand-in that knows nothing yet (every fact false, nothing carried), as the
 * storyboard asks its scenes, it says which pictures they can show; if that throws, nothing is fetched ahead, and the scene
 * still waits for its frames as it is entered.
 */
const NOBODY = { flag: () => false, has: () => false, holder: () => null, asked: () => 0, actor: () => null, plane: () => null, q: () => null,
  store: { data: { active: null, team: [], flags: {}, inventory: {}, where: {}, seenLines: {}, asked: {} } } };
function fxListOf(scene) {
  const fx = scene && scene.fx;
  if (typeof fx !== "function") return Array.isArray(fx) ? fx : [];
  try { const list = fx(NOBODY); return Array.isArray(list) ? list : []; } catch { return []; }
}
/** Every painted picture a scene's moving things can show (for fetching them ahead: scene.js, picturesIn); and a drive's
    sheet of things (DRIVE-16E: its JSON, gathered and held as a picture is, though it is none). */
export function fxPictures(scene) {
  const list = fxListOf(scene);           // (ROME-13E: a list, or a function of the game)
  const strip = (spec) => (spec && spec.type === "strip" && typeof spec.src === "string" ? [spec.src.startsWith("art/") ? spec.src : folderOf(scene) + spec.src] : []);      // (NEVADA-12E: a strip's picture)
  const at = (p) => (typeof p !== "string" ? [] : [p.startsWith("art/") ? p : folderOf(scene) + p]);
  const sheetOf = (t) => (t && typeof t.src === "string" ? (typeof t.sheet === "string" ? t.sheet : t.src.replace(/\.png$/i, "") + ".json") : null);
  const drive = (spec) => (spec && spec.type === "drive" ? [spec.sky, ...(Array.isArray(spec.bands) ? spec.bands : []).map((b) => b && b.src), spec.ground && spec.ground.src, spec.things && spec.things.src, sheetOf(spec.things),
    ...(Array.isArray(spec.grounds) ? spec.grounds : []).map((g) => g && g.src), ...[].concat(spec.light || [], spec.lights || []).map((l) => l && l.src)].flatMap(at) : []);      // DRIVE-16E: a drive's pictures, and its sheet (ROAD-18E: and straight ahead, its strips of ground and its pictures of light)
  return [...new Set(list.flatMap((spec) => { const f = spec && framesOf(spec.frames, scene); return [...(f ? [...Object.values(f.lists).flat(), ...(f.shadow ? [f.shadow] : [])] : []), ...strip(spec), ...drive(spec)]; }))];
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
    for (const run of [this.herding, this.posing]) if (run) run.resolve();      // ROME-13E: a herd or a pose under way is over (its promise kept): the flock starts afresh in its area as it is now
    this.herding = this.posing = null;
    this.simT = 0;
    this.fresh = true;
    for (const b of this.birds) {
      b.rand = sequence(this.seed + b.i * 7919);
      const p = this.place(b) || this.center();
      Object.assign(b, { x: p[0], y: p[1], s: p[2], alt: 0, dir: this.turns ? (b.rand() < 0.5 ? -1 : 1) : this.frames ? this.frames.face : 1, act: null, startle: null, away: false, herd: null });      // (ROME-13E: herd)
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
      if (b.herd || b.act.kind === "pose") continue;                    // ROME-13E: nothing startles a bird that is being herded, or holding a pose
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
      if (a.kind === "flap" || a.kind === "run") { this.herded(b, t, calm); continue; }     // ROME-13E: herded (nothing startles it)
      if (a.kind === "pose") { if (t >= a.until) this.unpose(b, t); continue; }             // ROME-13E: holding a pose, then on as it was
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
      this.sight(b, t);                                                  // (ROME-13E: was show(b, t), which hid every moving thing's show(on): a script's flock.show(false) threw)
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
  sight(b, t) {      // (ROME-13E: was show(b, t), which hid every moving thing's show(on) and threw when a script hid a flock)
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
    else if (a.kind === "flap") {                                       // ROME-13E: herded: a flap where it stands (its neck up at the noise until its beat comes)
      if (t < a.t0) pose = "look"; else { pose = "flap"; n = Math.floor((t - a.t0) * 10); }
    } else if (a.kind === "run") {                                      // ROME-13E: and a dash to its place (for less motion, a brisk walk)
      if (!this.frames || this.frames.lists.run || this.frames.lists.walk) { pose = a.walk ? "walk" : "run"; n = Math.floor(since * (a.walk ? 10 : 12)); }
      else alt = Math.abs(Math.sin(since * Math.PI * 6)) * 1.5;      // (painted, with frames neither to run nor to walk: it hops, as it walks)
    } else if (a.kind === "pose") { pose = a.name; n = Math.floor(since * (a.name === "flap" ? 10 : 5)); }      // ROME-13E: a pose a script asked for
    else n = Math.floor((since + b.i) / 1.7);                         // standing: a painted bird with two stand frames shifts now and then
    const ground = a.kind === "leave" ? a.from[1] : a.kind === "arrive" ? a.to[1] : y;
    b.next = { hidden: false, x, y, alt, pic: this.picFor(pose, n, b.dir, ground, alt), pose, moving: a.kind !== "stand" && a.kind !== "look" && a.kind !== "peck" && a.kind !== "turn" && a.kind !== "pose" };     // (ROME-13E: `pose`, what it shows, for tests)
  }
  picFor(pose, n, dir, ground, alt = 0) {
    const f = this.frames;
    if (f) {
      const L = f.lists, list = { takeoff: L.takeoff || L.land || L.fly, land: L.land || L.takeoff || L.fly, glide: L.glide || L.fly, fly: L.fly, peck: L.peck, walk: L.walk, look: L.look, turn: L.turn,
        run: L.run || L.walk, flap: L.flap || L.look }[pose] || L[pose] || L.stand;      // (ROME-13E: run, or its walk; flap, or its look; or any set a pose names)
      const i = pose === "peck" ? Math.min(n, list.length - 1) : pose === "fly" && list.length === 3 ? [0, 1, 2, 1][n % 4] : n % list.length;
      const k = (f.sizeAt != null && this.scene ? this.sizeAt(ground) / Math.max(0.05, scaleAt(this.scene, f.sizeAt)) : 1) * this.k;
      const pic = paintedBird(list[i], k, f.mirror && dir * f.face < 0, f.foot, alt < 0.5 ? f.shadow : null);       // (its shadow only while it is on the ground)
      if (pic) return pic;
    }
    const drawn = pose === "land" || pose === "takeoff" ? "fly0" : pose === "glide" ? "fly1" : pose === "fly" ? ["fly0", "fly1", "fly2", "fly1"][n % 4] : pose === "walk" || pose === "run" ? `walk${n % 2}` : pose === "peck" ? `peck${Math.min(n, 1)}` : pose === "flap" ? "look" : pose;      // (ROME-13E: run and flap, drawn; a peck held on its second picture, as a long pose's would run past it)
    return drawnBird(this.kind, drawn, this.length * this.sizeAt(ground) * this.k, dir < 0);
  }
  picture(sprite) {
    const p = sprite.pic;
    if (!p) return null;
    return sprite.alt ? { canvas: p.canvas, ox: p.ox, oy: p.oy + sprite.alt } : p;
  }
  seek(ms) { this.time = ms * (this.calm ? this.slow : 1); this.restart(); this.update(!!this.calm, []); if (!this.shown) this.reveal(false); }

  // ---------------------------------------------------------------- ROME-13E: a flock that a script sends somewhere, and a pose
  /**
   * For scripts: herd(area, { from, via, pace }): every bird runs into `area` (a shape on the ground: a poly, a rect or a
   * circle, as a flock's own), which is the flock's area from then on: there they stand, look, peck, walk and turn as they
   * did in the old one, keeping their `shy`, `fly`, `turn` and `moves` (the sacred geese, into their pen). Each is given a
   * place of its own in it, the places spread out (no two nearer than about a bird's length, where it has room for that).
   * The bird nearest `from` (where the boy stomped) sets off first, each of the others a beat (about a tenth of a second)
   * after the one before: it flaps where it stands, facing the way it will run (its `flap` frames, a third of a second),
   * then runs (its `run` frames) to its place, by `via` first if it is given (a point, or a list of points: the gap in the
   * pen's fence, so that nobody runs through the fence), at `pace` pixels a second at full size (110: a man is 160 tall
   * there), smaller and slower farther off, as a person walks. The first to set off goes deepest in. A running bird faces
   * the way it runs, whatever its `turn`. Nothing startles a bird that is being herded; one that is up and away (flown
   * off) is put at its place. It resolves when the last of them is there. At once, every bird at its place, while a
   * cut-scene is being skipped, and when the flock is not on the stage (?nofx, game.effects.enabled = false, its `when`
   * false). For less motion there is no flap, and they walk there briskly (their `walk` frames, at twice the flock's
   * walking pace, `walk`). Nothing of it is saved: a scene whose flock has been herded gives it its area from a fact as it
   * is entered (its `fx` a function of the game: Effects.enter). A flock on a perch cannot be herded: it says so, once.
   */
  herd(area, { from = null, via = null, pace = 110 } = {}) {
    if (this.perch) {
      if (!this.toldPerch) { this.toldPerch = true; console.warn(`The flock "${this.id}" is on a perch, and a flock on a perch cannot be herded: it stays where it is.`); }
      return Promise.resolve();
    }
    const poly = polyOf(area);
    if (!poly) { console.warn(`The flock "${this.id}" was sent to an area that is not a shape (a poly, a rect or a circle): it stays where it is.`); return Promise.resolve(); }
    this.endHerd(); this.endPose();
    this.setArea(poly);
    const t = this.simT / 1000, ways = (isPoint(via) ? [via] : Array.isArray(via) ? via.filter(isPoint) : []).map((p) => [p[0], p[1]]);
    const near = isPoint(from) ? (b) => this.gap(b, from[0], from[1]) : () => 0;
    const order = this.birds.slice().sort((a, b) => near(a) - near(b) || a.i - b.i);
    const places = this.spread(order.length, ways.length ? ways[ways.length - 1] : null);
    const run = { pace: Math.max(1, num(pace, 110)), left: 0, resolve: null };
    const done = new Promise((resolve) => { run.resolve = resolve; });
    order.forEach((b, n) => {
      const at = places[n];
      if (b.away || ["fly", "leave", "arrive", "away"].includes(b.act.kind)) { this.settleAt(b, at, t); return; }      // (one that is up and away is simply put there)
      b.startle = null;
      b.herd = { path: [...ways, at], to: at, run };
      const go = t + n * 0.1 + b.rand() * 0.02;
      b.act = { kind: "flap", t0: go, until: go + 0.33 };
      run.left++;
    });
    this.herding = run;
    this.fresh = true;                                                 // (their pictures follow at once)
    if (!run.left || this.quick()) this.endHerd();
    return done;
  }
  /**
   * For scripts: pose(name, seconds): every bird of the flock on the ground takes that pose at once ("look": the geese's
   * necks stretched out low, hissing; "flap"; "stand"; or any set of its frames), for about that long (each a little more
   * or less), then carries on as it was, from where it was. It resolves when they have all carried on; at once while a
   * cut-scene is being skipped, and when the flock is not on the stage. A bird up and away, or being herded, is left as
   * it is; nothing startles a bird that holds a pose. With no frames for it: `flap` shows `look`, anything else `stand`.
   */
  pose(name = "look", seconds = 1) {
    this.endPose();
    if (this.quick()) return Promise.resolve();
    const t = this.simT / 1000, run = { left: 0, resolve: null };
    const done = new Promise((resolve) => { run.resolve = resolve; });
    for (const b of this.birds) {
      if (b.away || b.herd || !["stand", "look", "peck", "walk", "turn", "hop"].includes(b.act.kind)) continue;
      b.act = { kind: "pose", name: String(name), t0: t, until: t + Math.max(0.1, num(seconds, 1)) * (0.85 + 0.3 * b.rand()), was: b.act };
      b.startle = null;
      run.left++;
    }
    this.posing = run;
    this.fresh = true;
    if (!run.left) this.endPose();
    return done;
  }
  /** Is it all to be done at once: the flock off the stage (no moving things, or its `when` false), or a cut-scene being skipped? */
  quick() { const g = this.game; return !(this.host.on && this.wanted()) || !!(g && g.clock && g.clock.skipping); }
  /** Off the stage, or a cut-scene skipped, while a herd or a pose is under way: it is over at once. */
  advance(dt, calm, people) {
    if ((this.herding || this.posing) && this.quick()) { this.endHerd(); this.endPose(); }
    super.advance(dt, calm, people);
  }
  /** The scene has gone (Effects.drop): whatever a script waits for is over. */
  end() { this.endHerd(); this.endPose(); }
  /** The area it keeps to from now on (and, on steps, the treads that are in it). */
  setArea(poly) {
    const s = this.spec;
    this.area = poly; this.box = boxOf(poly);
    this.span = Math.max(this.box[2] - this.box[0], this.box[3] - this.box[1]);
    if (this.treads) this.treads = num(s.tread, 0) > 0 ? Array.from({ length: Math.floor((this.box[3] - this.box[1]) / s.tread) + 1 }, (_, i) => this.box[3] - i * s.tread) : this.treads.filter((y) => y >= this.box[1] && y <= this.box[3]);
    if (this.treads && !this.treads.length) this.treads = null;
  }
  /** How long a bird is, standing at row y (for keeping them a bird's length apart). */
  lengthAt(y) {
    const f = this.frames, img = f && got(f.lists.stand[0]);
    if (img && img.naturalWidth) return img.naturalWidth * 0.75 * (f.sizeAt != null && this.scene ? this.sizeAt(y) / Math.max(0.05, scaleAt(this.scene, f.sizeAt)) : 1) * this.k;
    return this.length * this.sizeAt(y) * this.k;
  }
  /** n places in the area, spread out: each as far from the others as forty tries find (a bird's length apart, or more,
      where there is room). The farthest from `gate` (the way in) first. [x, y, 0] each. */
  spread(n, gate) {
    this.herds = (this.herds || 0) + 1;
    const rand = sequence(this.seed + this.herds * 104729), [x0, y0, x1, y1] = this.box, out = [];
    for (let k = 0; k < n; k++) {
      let best = null, far = -1;
      for (let tries = 0; tries < 40; tries++) {
        const x = x0 + rand() * (x1 - x0), y = y0 + rand() * (y1 - y0);
        if (!inside(this.area, x, y)) continue;
        const d = out.length ? Math.min(...out.map((p) => Math.hypot(p[0] - x, (p[1] - y) * 1.5) / this.lengthAt((p[1] + y) / 2))) : Infinity;
        if (d > far) { far = d; best = [x, y]; }
        if (d === Infinity) break;
      }
      out.push(best || this.center());
    }
    if (gate) out.sort((a, b) => Math.hypot(b[0] - gate[0], (b[1] - gate[1]) * DEPTH) - Math.hypot(a[0] - gate[0], (a[1] - gate[1]) * DEPTH));
    return out.map((p) => [p[0], p[1], 0]);
  }
  /** A bird at its place, standing: there, and done with any herd. */
  settleAt(b, at, t) {
    b.herd = null; b.away = false; b.alt = 0; b.startle = null;
    b.x = at[0]; b.y = at[1]; b.s = 0;
    b.act = { kind: "stand", t0: t, until: t + 0.4 + b.rand() * 0.8 };
    if (!this.turns) b.dir = this.frames ? this.frames.face : 1;      // (a flock that never turns faces its own way again)
  }
  /** One step of a herded bird: waiting for its beat, its flap, then its run along its way (via, then its own place), and there. */
  herded(b, t, calm) {
    const a = b.act, h = b.herd;
    if (!h) { b.act = { kind: "stand", t0: t, until: t + 0.5 }; return; }
    if (a.kind === "flap") {
      if (t < a.t0) return;                                          // (its beat has not come)
      b.dir = Math.sign(h.path[0][0] - b.x) || b.dir;               // facing the way it will run
      if (calm || t >= a.until) b.act = { kind: "run", t0: t, walk: !!calm };     // (for less motion: no flap, and a brisk walk)
      return;
    }
    const pace = a.walk ? Math.min(h.run.pace, this.walkSpeed * 2) : h.run.pace;
    let budget = pace * Math.max(0.35, this.sizeAt(b.y)) * (TICK / 1000);
    while (budget > 0 && h.path.length) {
      const [px, py] = h.path[0], dx = px - b.x, dy = py - b.y, dist = Math.hypot(dx, dy * DEPTH);
      if (dist < 0.01) { h.path.shift(); continue; }
      if (Math.abs(dx) > 0.5) b.dir = Math.sign(dx);
      const step = Math.min(budget, dist), k = step / dist;
      b.x += dx * k; b.y += dy * k; budget -= step;
      if (step >= dist) h.path.shift();
    }
    if (h.path.length) return;
    const run = h.run;
    this.settleAt(b, h.to, t);
    if (run === this.herding && --run.left <= 0) { this.herding = null; run.resolve(); }
  }
  /** The herd under way, done at once: every bird still on its way put at its place, and the promise kept. */
  endHerd() {
    const run = this.herding;
    if (!run) return;
    this.herding = null;
    const t = this.simT / 1000;
    for (const b of this.birds) if (b.herd && b.herd.run === run) this.settleAt(b, b.herd.to, t);
    this.fresh = true;
    run.resolve();
  }
  /** A bird's pose is over: it carries on as it was, from where it was (its time moved on by the pose's). */
  unpose(b, t, count = true) {
    const a = b.act, was = a.was, d = t - a.t0;
    if (was) { if (was.t0 != null) was.t0 += d; if (was.until != null) was.until += d; b.act = was; }
    else b.act = { kind: "stand", t0: t, until: t + 0.5 };
    const run = this.posing;
    if (count && run && --run.left <= 0) { this.posing = null; run.resolve(); }
  }
  /** The pose under way, over at once: every bird carries on, and the promise is kept. */
  endPose() {
    const run = this.posing;
    if (!run) return;
    this.posing = null;
    const t = this.simT / 1000;
    for (const b of this.birds) if (b.act && b.act.kind === "pose") this.unpose(b, t, false);
    this.fresh = true;
    run.resolve();
  }
}

function Birds(host, spec, n) {
  const kind = spec.kind === "flock" || spec.kind === "flyers" ? spec.kind : spec.lanes || spec.circle ? "flyers" : "flock";
  return kind === "flyers" ? new Flyers(host, spec, n) : new Flock(host, spec, n);
}

// ---------------------------------------------------------------- NEVADA-12E: a strip of painting that goes by a window
/**
 * strip: a painted strip of country (the desert, going by a limousine's windows) scrolling past behind the windows of
 * the scene, the world going by to the left as it does from a car driving right. It is one picture, wide and painted to
 * run on from its right edge into its left; only what lies behind a window is ever drawn: one picture for each window,
 * cut to the window's own shape, so the cast repaints those boxes and nothing else.
 *   src        the picture (a path from the top of the site, or a name in the scene's own folder)
 *   windows    the shapes it shows through (polys, rects or circles), each a picture of its own; or `clip`, the same.
 *              With neither: the width of the stage, over the strip's own rows
 *   row        the row of the stage at which the strip's bottom edge sits
 *   speed      pixels a second (of the picture, at its own size): the world goes by to the LEFT; negative, to the right;
 *              0, parked. A script changes it with set({ speed }), and the car slows as the script tweens it
 *   loop       true (the default): its right edge runs on into its left, so where the seam is in a window it is drawn
 *              twice; false: it goes by once and is gone
 *   offset     the column of the picture at the stage's left edge when its time begins (0)
 *   fps        pictures a second of its time (20). Less motion: its time runs at half speed, so it goes by at half the pace,
 *              drawn half as often, each picture the same step on from the last
 *   base, plane, when, scale, opacity, seed: as every kind. Its depth, given neither base nor plane: "back", behind everybody.
 * Where it is at a moment is worked out from its time alone (the offset, and the speed since the last set()), so a scene
 * opened twice shows the same picture at the same moment. At its own size it is drawn on whole pixels, and a window's
 * edge is hard: a pixel is in the window when its middle is, as for the ground in walk.js. A window's picture is drawn
 * again only when the strip has gone by a whole pixel since the last (so a parked one costs nothing).
 */
class Strip extends Effect {
  constructor(host, spec, n) {
    super(host, spec, n);
    const s = spec;
    if (typeof s.src !== "string") throw new Error("a strip needs a picture: src");
    this.row = num(s.row, null);
    if (this.row == null) throw new Error("a strip needs `row`: the row of the stage its bottom edge sits on");
    this.src = s.src.startsWith("art/") ? s.src : folderOf(host.scene) + s.src;
    this.plane = "back";                                             // (behind everybody, unless it is given a base or a plane)
    this.speed = num(s.speed, 0);
    this.loop = s.loop !== false;
    this.offset = num(s.offset, 0);
    this.fps = Math.max(1, num(s.fps, 20)); this.calmFps = this.fps;    // (for less motion its time runs at half speed: drawn half as often, each picture as far on as at full speed, never jumpier)
    this.alpha = clamp(num(s.opacity, 1));
    this.d0 = 0; this.t0 = 0;                                        // the distance gone (picture pixels) at t0 (ms of its own time): since the last change of speed
    const shapes = polysOf(s.windows).length ? polysOf(s.windows) : polysOf(s.clip);
    this.wins = (shapes.length ? shapes : [null]).map((poly, i) => {
      const win = { poly, box: null, mask: null, pair: null, step: null, pos: null, calm: null, go: false, tiles: 0, sprite: this.mote(":" + i) };
      win.sprite.win = win;
      if (poly) this.frame(win, boxOf(poly));
      return win;
    });
  }
  /** Where a window's picture lies on the stage ([x0, y0, x1, y1), whole pixels), and its shape on that picture: a mask with
      hard edges, made once (a pixel is in it when its middle is). */
  frame(win, [x0, y0, x1, y1]) {
    const box = [Math.max(0, Math.floor(x0)), Math.max(0, Math.floor(y0)), Math.min(W, Math.ceil(x1)), Math.min(H, Math.ceil(y1))];
    const w = Math.max(1, box[2] - box[0]), h = Math.max(1, box[3] - box[1]);
    win.box = box;
    win.pair = new Pair(w, h);
    win.mask = canvasOf(w, h);
    const img = win.mask.getContext("2d").createImageData(w, h), d = img.data;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) if (!win.poly || inside(win.poly, box[0] + x + 0.5, box[1] + y + 0.5)) d[(y * w + x) * 4 + 3] = 255;
    win.mask.getContext("2d").putImageData(img, 0, 0);
    win.sprite.place(box[0], box[1]);
  }
  pics() { return [this.src]; }
  slots() { return this.sprites; }
  restart() { this.d0 = 0; this.t0 = 0; for (const w of this.wins) w.step = null; }
  /** Picture pixels gone by at a moment of its own time (ms), from where it began. */
  gone(t) { return this.d0 + (this.speed * Math.max(0, t - this.t0)) / 1000; }
  /** For scripts: { speed } (pixels a second; 0 parks it), { opacity }. It goes on from where it is. */
  set(o = {}) {
    if (o && typeof o.speed === "number" && Number.isFinite(o.speed) && o.speed !== this.speed) { this.d0 = this.gone(this.time); this.t0 = this.time; this.speed = o.speed; }
    if (o && typeof o.opacity === "number") { this.alpha = clamp(o.opacity); for (const w of this.wins) w.step = null; }
    return this;
  }
  /** Where the strip is on the stage at a step of its time: the whole pixels it has gone by. */
  pos(step, fps) { return Math.round((this.offset + this.gone((step / fps) * 1000)) * this.k); }
  /** Each window's next picture is due when the strip has gone by a whole pixel since the last; it is drawn in its turn (grant). */
  update(calm) {
    const fps = calm ? this.calmFps : this.fps, at = this.pos(Math.floor((this.time * fps) / 1000), fps);
    for (const w of this.wins) if (w.step !== null) w.sprite.want = at !== w.pos || calm !== w.calm;
  }
  grant(sprite) { if (sprite.win) sprite.win.go = true; }
  picture(sprite, calm) {
    const w = sprite.win, img = got(this.src);
    if (!w || !img || !img.naturalWidth) return null;                // (not here yet)
    if (!w.box) this.frame(w, [0, this.row - img.naturalHeight * this.k, W, this.row]);
    const fps = calm ? this.calmFps : this.fps, step = Math.floor((this.time * fps) / 1000), at = this.pos(step, fps), go = w.go;
    w.go = false;
    if (w.step === null || (go && (at !== w.pos || calm !== w.calm))) {           // (the first picture at once; after that, in its turn)
      w.step = step; w.pos = at; w.calm = calm;
      this.paint(w.pair.next(), w, img, at);
    }
    return { canvas: w.pair.canvas, ox: 0, oy: 0 };
  }
  /** One window's picture with the strip gone by `pos` pixels: drawn twice where the seam is in the window, then cut to its mask. */
  paint(ctx, w, img, pos) {
    const k = this.k, iw = Math.max(1, Math.round(img.naturalWidth * k)), ih = Math.max(1, Math.round(img.naturalHeight * k));
    const top = Math.round(this.row - ih) - w.box[1], wide = w.box[2] - w.box[0];
    let x = -pos - w.box[0];                                         // the strip's left edge on this picture: the column `offset` at the stage's left edge, gone `pos` pixels
    if (this.loop) { const m = ((x % iw) + iw) % iw; x = m === 0 ? 0 : m - iw; }       // (the copy that covers the picture's left edge)
    ctx.globalAlpha = this.alpha;
    ctx.imageSmoothingEnabled = iw !== img.naturalWidth;            // (at its own size: hard pixels on whole pixels)
    let n = 0;
    for (let at = x; at < wide; at += iw) { if (at + iw > 0) { ctx.drawImage(img, at, top, iw, ih); n++; } if (!this.loop) break; }
    ctx.globalAlpha = 1; ctx.globalCompositeOperation = "destination-in";
    ctx.drawImage(w.mask, 0, 0);                                     // (nothing outside the window)
    ctx.globalCompositeOperation = "source-over";
    w.tiles = n;
    this.drawn = this.wins.reduce((sum, v) => sum + v.tiles, 0);
  }
}

// ---------------------------------------------------------------- DRIVE-16E: the world going by a car's side windows
/**
 * drive: the world outside a car's side windows, as a pinhole camera that is moving forward sees it (round sixteen: the
 * limousine's windows, where one flat strip going by at one speed on both sides looked like mirrors). The camera is the
 * scene's own, level: `vanish` is where the line of travel runs to (its row is the horizon), `focal` how far the picture
 * is from the eye in pixels, `eye` how high the eye is above the road in metres. A point X metres out to the side of the
 * line of travel, z metres ahead and Y metres up is on the stage at
 *     x = vanish x - focal * X / z  (side "L"; + on side "R")          y = vanish y + focal * (eye - Y) / z
 * and as the car goes forward s metres every z is s smaller: everything comes out of the far end of the windows small and
 * slow, and grows and speeds up as it comes nearer; how fast depends on how far out it is. Each pane (as the strip's
 * windows: a picture of its own, cut to its shape with hard edges, a pixel in it when its middle is) is drawn far to near:
 *   sky      a picture the stage's size, drawn as it is (still) wherever the pane shows sky
 *   ground   the ground beside the road seen from straight above, columns along the road (looping end to end), rows
 *            outward from `from` metres, `ppm` pixels a metre both ways: each pixel below the horizon shows the patch of
 *            ground it sees (z = focal * eye / (y - horizon), X = |x - vanish x| * z / focal: the picture read at
 *            ((z + s) * ppm) along and (X - from) * ppm across); beyond its last row the colour of its last rows; fading
 *            into the haze with distance
 *   bands    panoramas seen from the side, far to near, each standing `distance` metres out: the stage's column at
 *            u = |x - vanish x| looks at it z = focal * distance / u ahead and shows its column ((z + s) * ppm), looping,
 *            from its foot (y = horizon + focal * eye / z) up, at focal / z / ppm of its own size. A band hides the ground
 *            beyond it; the ground nearer than it lies below its foot
 *   things   upright things beside the road (posts, poles, bushes, a sign), from a sheet of pictures painted from the side,
 *            far to near, each at its place and its size there, with wires from each to the next (one pixel, dark, sagging)
 *            DRIVE-16F: given a `sun`, first every thing's shadow, lying on the ground: from its foot along the sun, as long
 *            as the light makes it, as wide as the thing is at each height of it (its picture's solid pixels counted, row
 *            by row: a post's a thin band, a bush's a rounded blob narrowing to its tip), its middle line worked out on the
 *            ground in metres and put on the stage with the camera, as the ground is, its width by the camera's rates of
 *            change there (and never thinner than `shade` says, below); all of them one shape, laid over the ground in
 *            `shade`, multiplied (overlapping shadows are no darker), its edges a pixel soft as a filled shape's. Then the
 *            things over them, far to near. A sheet of things is painted without shadows: they are the engine's
 * No shimmer: a picture drawn smaller than its own size shows, in each pixel, the average of the patch of it that pixel
 * sees (the picture's pixels are summed once, as it arrives, and any patch's average is then a few steps), never one pixel
 * picked from many; drawn larger, its pixels stay hard (a pixel that straddles two of them takes some of each). The rows
 * of ground going by faster than their own pixels in a picture are averaged along their motion over `streak` of a
 * picture's travel, so speed reads as speed; for less motion, not. A thing drawn smaller than its own size comes from a
 * copy of itself halved, and halved again (each pixel the average of four, made once); larger, with hard pixels.
 *   side       "L" or "R": the side of the line of travel its world is on (needed)
 *   windows    the panes it is seen through (polys, rects or circles), each a picture of its own; or `clip` (needed)
 *   vanish     [x, y]: the vanishing point of the line of travel (needed). Each pane lies wholly on its side of it
 *   focal      the camera's focal length in pixels (needed); eye: metres above the road (1.6)
 *   speed      metres a second (0: parked). set({ speed }) goes on from where it is; tweened, the car slows
 *   start      metres gone when its time begins (0)
 *   sky        the sky (a picture the stage's size; may be opaque); none: clear where it would show
 *   bands      [{ src, distance, ppm }]: `distance` metres out, `ppm` its pixels a metre at its own size; each loops end to
 *              end, its bottom row the ground at its foot, clear above
 *   ground     { src, from, ppm } (above)
 *   things     { src, rows }: `src` a sheet of pictures painted from the side, and beside it (its name with .json, or
 *              `sheet`) { ppm, sprites: { name: { box: [x, y, w, h], foot: [fx, fy], height } } }, `foot` the point on the
 *              ground, in the box (or on the sheet: whichever lies in the box). Each row: `sprite` a name, or a list to
 *              pick from; `every` metres from one to the next, or [min, max]; `at` metres out, or [min, max]; `wires`
 *              heights (metres) of wires from each to the next, sagging `sag` metres in the middle (1.5% of the span);
 *              `offset` where the first stands along the road (metres; from the seed); `loop` metres after which the row
 *              repeats (none: it never does; give the ground's length to keep posts on footings painted in the ground).
 *              Placed from the seed: the same every time. A thing nearer than 1.5 m ahead, or less than a pixel, is not drawn
 *   haze       the air's colour (#d9dde6), through the scene's key; haze_far: the distance at which it has half covered the
 *              ground (4000 m). Only the ground is hazed by the engine: the bands are painted in the haze of their distance,
 *              and the things are near
 *   streak     the share of a picture's travel the fast ground is averaged over (0.6; 0: none)
 *   slices     the most slices a pixel's patch of ground is taken in (2; 1 to 6): more, sharper far ground, and slower
 *   wire       the wires' colour (#2f2a26), through the scene's key
 *   sun        DRIVE-16F: [forward, left], the things' shadows: metres of shadow for a metre of a thing's height, ahead
 *              along the line of travel and to the car's left (the limousine's morning: [0.36, 1.95]; on the left side the
 *              car's left is outward, on the right toward the road). None: no shadows
 *   shade      DRIVE-16F: the colour the shadows multiply the ground by (#6664ac: the painter's for a morning shadow on the
 *              sand, the roadside's and the ground pictures' own), through the scene's key; shade_k how much of it (0.6: 0,
 *              none; 1, all of it). A shadow is never drawn thinner than 10 cm would be seen face on at its distance, up to a
 *              pixel and a half (a fence post's is about half a pixel, seen from 1.8 m up: it would not be seen)
 *   fps        pictures a second (30). Less motion: its time runs at half speed, no streaks
 *   phase      where its pictures fall between the steps of its time (0 on the left, 0.5 on the right: see below)
 *   base, plane, when, opacity, seed: as every kind (`scale` is not used: the camera says every size). Its depth, given
 *   neither base nor plane: "back", behind everybody.
 * Its time is the strip's: where it is (s, metres gone) is worked out from its time alone and the speeds since each set(),
 * so a scene opened twice shows the same thing at the same moment; parked, it draws nothing new. Each pane's picture is
 * drawn again only when s has changed (or less motion has come or gone). `cost` keeps what its pictures took.
 *
 * ROAD-18E: STRAIGHT AHEAD (side: "ahead"; round eighteen: the opening movie, the camera behind the wagon). The same camera
 * looking down the line of travel: both sides of it and the road between, one picture. A point X metres right of the line
 * of travel (negative: left), z ahead and Y up is on the stage at  x = vanish x + focal * X / z,  y = vanish y + focal *
 * (eye - Y) / z. With no `windows` (nor `clip`) the whole stage is its one pane. What it draws, far to near: the sky (if
 * it has one, where no ground is: usually none, the backdrop being the sky); the ground, every row below the horizon one
 * depth (z = focal * eye / (row - horizon)), so a row is one patch of road along it and each pixel the average of the
 * stretch across the road it covers; the things' shadows; the lights; the things and wires. Every rule above holds (no
 * shimmer, the streak, its time, the haze, the shadows), with these besides:
 *   grounds    [{ src, from, to, ppm }]: the ground from straight above in strips across the road, each its own picture:
 *              columns along the road (looping end to end), rows across from `from` (its top row) to `to` (its bottom
 *              row), metres right of the line of travel (the road -6 to 6, the desert -30 to -6 and 6 to 30). Strips that
 *              meet meet with no seam; past the outermost ones the ground goes on in the colour of their outer rows, going
 *              by with them, into the haze. (`ground`, a side view's one strip, is read as the only strip)
 *   far        metres: no ground farther off than this (2000): the backdrop shows beyond. things_far the same for things (1500)
 *   haze       a colour, as on a side; or "backdrop": the ground fades into clear with distance, so that the backdrop's
 *              own far land shows through it near the horizon (the highway's: its far plain painted in the painting's air)
 *   things     rows as on a side, `at` across the road: a number (negative on the left), a range, two numbers of opposite
 *              signs (each thing at both: posts either side of the road), or with `both: true` a range of distances out,
 *              each thing on one side or the other at random (seeded). A row's `gap` (its own stretches kept clear; false:
 *              never kept clear). A wire is a height, or [across, up] from the thing's foot (a pole's insulators either side
 *              of it). A sprite's own `ppm` on the sheet (the signs', so that at 17.3 m they are drawn pixel for pixel), its
 *              `air` (the share of the haze it takes: 1; the painter's poles 0.6; 0 for a thing painted in its own air as it
 *              is seen from where it is drawn at its own size, focal / ppm ahead: only the air beyond that), and a thing
 *              painted for each side of the road (`sage-1-l`, `sage-1-r`): a row or a piece naming "sage-1" gets the side's own
 *   gap        [[s0, s1], ...]: stretches of road (metres along it from where the drive began) where the rows put nothing
 *   pieces     [{ id, sprite, X, s, Y }]: set pieces from the start (see place)
 *   light      [{ id, src, x, y } or { id, poly, radial: { at, r: [rx, ry] } or linear: { from, to }, stops: [[offset, colour,
 *              alpha], ...] }, with `blend` ("screen", "multiply"...; "source-over") and `opacity` (1)]: light laid over the
 *              ground (under the things), still on the stage while the road goes by under it: the shine of the low sun on
 *              the asphalt, the dark corners, the hole's glow down the road. Never keyed (time's light belongs to no place)
 * For scripts, besides set({ speed }) and set({ opacity }):
 *   set({ s })          puts the camera s metres along the road and parks it there (a tween carrying it lands exactly where
 *                       it is sent; set({ s, speed }) and it goes on from there at that speed). No jump either way: speed
 *                       hands over to place at the place it has reached, and place to speed at the place it was put
 *   .s, .speed          where the camera is (metres along the road) and its speed, now
 *   place(id, { sprite, X, s, Y })   a set piece: a thing of the sheet at X across and s along the road (it stays where it
 *                       is as the camera comes on); placed again with only some of these, it keeps the rest (the sign:
 *                       place("sign", { sprite: "sign-bc" })). remove(id) takes it away
 *   set({ gap }), set({ light: { id: k } })   the stretches kept clear; a light's opacity
 * Doors in time over it: a portal names it in `under` ({ fx: id }) and reads its picture again each time it draws a new one
 * (Portal, below); { fx: id, piece, sprite, alpha } reads one set piece in, as another picture of the sheet if `sprite` says.
 * The proof: index.html?scene=engine-proof&lead=dad&flags=proof.road,proof.arrived (docs/DESIGN.md, section 2).
 */
const driveKept = new WeakMap();              // the tables made from each picture (by the picture held for the session): made once
const DRIVE_SLICES = 2;                       // the most slices a pixel's patch of ground is taken in, unless the spec says (planGround)
function driveTables(img, kind, make) {
  let m = driveKept.get(img);
  if (!m) driveKept.set(img, (m = {}));
  if (!m[kind]) {
    const w = img.naturalWidth, h = img.naturalHeight, ctx = canvasOf(w, h).getContext("2d", { willReadFrequently: true });
    ctx.drawImage(img, 0, 0);
    m[kind] = make({ w, h, d: ctx.getImageData(0, 0, w, h).data });
  }
  return m[kind];
}
/** The ground's sums, from which any patch's average is a few steps: P[(a * h + b) * 3 + c] is the sum of colour c of the
    picture's row b (outward) over its columns (along the road) before a, for a = 0 to w; F the same for its last rows' colour. */
function groundSums({ w, h, d }) {
  const P = new Float32Array((w + 1) * h * 3), F = new Float32Array((w + 1) * 3), K = Math.min(h, 8);
  for (let a = 0; a < w; a++) {
    const o = a * h * 3, n = o + h * 3;
    let fr = 0, fg = 0, fb = 0;
    for (let b = 0; b < h; b++) {
      const i = (b * w + a) * 4, k = b * 3;
      P[n + k] = P[o + k] + d[i]; P[n + k + 1] = P[o + k + 1] + d[i + 1]; P[n + k + 2] = P[o + k + 2] + d[i + 2];
      if (b >= h - K) { fr += d[i]; fg += d[i + 1]; fb += d[i + 2]; }
    }
    F[a * 3 + 3] = F[a * 3] + fr / K; F[a * 3 + 4] = F[a * 3 + 1] + fg / K; F[a * 3 + 5] = F[a * 3 + 2] + fb / K;
  }
  return { w, h, P, F };
}
/** A band's sums, the same way, its colours weighted by how solid they are: P[(a * h + t) * 4 + c], t its row from the top;
    and the row of each column's ridge (its first row with any paint), so that the clear sky above it is passed over. */
function bandSums({ w, h, d }) {
  const P = new Float32Array((w + 1) * h * 4), top = new Int16Array(w).fill(h);
  for (let a = 0; a < w; a++) {
    const o = a * h * 4, n = o + h * 4;
    for (let t = 0; t < h; t++) {
      const i = (t * w + a) * 4, k = t * 4, q = d[i + 3] / 255;
      P[n + k] = P[o + k] + d[i] * q; P[n + k + 1] = P[o + k + 1] + d[i + 1] * q; P[n + k + 2] = P[o + k + 2] + d[i + 2] * q; P[n + k + 3] = P[o + k + 3] + d[i + 3];
      if (d[i + 3] && t < top[a]) top[a] = t;
    }
  }
  return { w, h, P, top };
}
/** The weights that read a sum at a + its loops, for the average over [lo, hi] of a picture `w` wide that loops end to end. */
function spanOf(lo, hi, w) {
  const iH = Math.floor(hi), iL = Math.floor(lo), mH = ((iH % w) + w) % w, mL = ((iL % w) + w) % w;
  return { mH, fH: hi - iH, mL, fL: lo - iL, loops: (iH - mH) / w - (iL - mL) / w, inv: 1 / Math.max(1e-6, hi - lo) };
}
/** A thing's picture and copies of it halved, and halved again (each pixel the average of four, weighted by how solid they
    are), with its foot point on each: [{ canvas, w, h, fx, fy }]. `foot` is in its box, or on the sheet: whichever lies in the box. */
function spriteLevels({ w: sw, h: sh, d }, box, foot) {
  const bx = Math.max(0, Math.round(box[0])), by = Math.max(0, Math.round(box[1])), bw = Math.max(1, Math.min(sw - bx, Math.round(box[2]))), bh = Math.max(1, Math.min(sh - by, Math.round(box[3])));
  let fx = bw / 2, fy = bh;
  if (isPoint(foot)) {
    const inBox = (x, y) => x >= -0.5 && x <= bw + 0.5 && y >= -0.5 && y <= bh + 0.5, rel = inBox(foot[0], foot[1]), abs = inBox(foot[0] - bx, foot[1] - by);
    const off = (x, y) => Math.hypot(x - bw / 2, y - bh);
    [fx, fy] = rel && abs ? (off(foot[0], foot[1]) <= off(foot[0] - bx, foot[1] - by) ? foot : [foot[0] - bx, foot[1] - by]) : abs ? [foot[0] - bx, foot[1] - by] : foot;
  }
  let lw = bw, lh = bh, px = new Uint8ClampedArray(bw * bh * 4);
  for (let y = 0; y < bh; y++) px.set(d.subarray(((by + y) * sw + bx) * 4, ((by + y) * sw + bx + bw) * 4), y * bw * 4);
  const levels = [];
  for (let k = 1; ; k *= 2) {
    const c = canvasOf(lw, lh);
    c.getContext("2d").putImageData(new ImageData(px, lw, lh), 0, 0);
    levels.push({ canvas: c, w: lw, h: lh, fx: fx / k, fy: fy / k });
    if ((lw <= 2 && lh <= 2) || levels.length >= 9) return levels;
    const nw = Math.ceil(lw / 2), nh = Math.ceil(lh / 2), np = new Uint8ClampedArray(nw * nh * 4);
    for (let y = 0; y < nh; y++) for (let x = 0; x < nw; x++) {
      let r = 0, g = 0, b = 0, a = 0;
      for (let q = 0; q < 4; q++) {
        const sx = x * 2 + (q & 1), sy = y * 2 + (q >> 1);
        if (sx >= lw || sy >= lh) continue;
        const i = (sy * lw + sx) * 4, al = px[i + 3];
        r += px[i] * al; g += px[i + 1] * al; b += px[i + 2] * al; a += al;
      }
      const o = (y * nw + x) * 4;
      if (a > 0) { np[o] = r / a; np[o + 1] = g / a; np[o + 2] = b / a; np[o + 3] = a / 4; }
    }
    px = np; lw = nw; lh = nh;
  }
}
/** DRIVE-16F: what a thing's shadow is made from: how wide the thing is at each height above its foot (its picture's solid
    pixels counted row by row: a sign's two posts are two posts' width, an open bush less than its span), from its foot to
    its top, in pixels of its sheet, as few points as keep that outline to half a pixel (a post's straight sides are two).
    -> { pts: [[height, width], ...] from the foot (0) up, top (its height), area (the sum of its widths: its side's area) },
    or null for a picture with nothing solid above its foot. `foot` as for spriteLevels. */
function shadowShape({ w: sw, h: sh, d }, box, foot) {
  const bx = Math.max(0, Math.round(box[0])), by = Math.max(0, Math.round(box[1])), bw = Math.max(1, Math.min(sw - bx, Math.round(box[2]))), bh = Math.max(1, Math.min(sh - by, Math.round(box[3])));
  let fy = bh;
  if (isPoint(foot)) {
    const inBox = (x, y) => x >= -0.5 && x <= bw + 0.5 && y >= -0.5 && y <= bh + 0.5, rel = inBox(foot[0], foot[1]), abs = inBox(foot[0] - bx, foot[1] - by);
    const off = (x, y) => Math.hypot(x - bw / 2, y - bh);
    fy = rel && abs ? (off(foot[0], foot[1]) <= off(foot[0] - bx, foot[1] - by) ? foot[1] : foot[1] - by) : abs ? foot[1] - by : foot[1];
  }
  const rows = [];                                                   // [height of the row's middle above the foot, its solid pixels], from the foot up
  let top = -1, area = 0;
  for (let y = Math.min(bh, Math.floor(fy)) - 1; y >= 0; y--) {
    let n = 0;
    for (let x = 0, i = ((by + y) * sw + bx) * 4 + 3; x < bw; x++, i += 4) if (d[i] >= 128) n++;
    rows.push([fy - y - 0.5, n]);
    if (n) { top = rows.length - 1; area += n; }
  }
  if (top < 0) return null;
  const line = [[0, rows[0][1]], ...rows.slice(0, top + 1), [rows[top][0] + 0.5, rows[top][1]]];
  const keep = new Uint8Array(line.length); keep[0] = keep[line.length - 1] = 1;
  for (const stack = [[0, line.length - 1]]; stack.length;) {        // (the outline simplified: Ramer, Douglas and Peucker, to half a pixel)
    const [a, b] = stack.pop(), [ax, ay] = line[a], dx = line[b][0] - ax, dy = line[b][1] - ay, len = Math.hypot(dx, dy) || 1;
    let far = -1, most = 0.5;
    for (let i = a + 1; i < b; i++) { const off = Math.abs((line[i][0] - ax) * dy - (line[i][1] - ay) * dx) / len; if (off > most) { most = off; far = i; } }
    if (far > 0) { keep[far] = 1; stack.push([a, far], [far, b]); }
  }
  return { pts: line.filter((p, i) => keep[i]), top: line[line.length - 1][0], area };
}
/** ROAD-18E: a strip of ground seen straight ahead (`grounds`): the ground's sums (groundSums: P, and F the colour of its last
    rows), and F0 the colour of its first rows, so that past the outermost strips the ground carries on, either side, in the
    colour of their outer rows, going by with them. */
function stripSums(px) {
  const g = groundSums(px), { w, h, d } = px, F0 = new Float32Array((w + 1) * 3), K = Math.min(h, 8);
  for (let a = 0; a < w; a++) {
    let fr = 0, fg = 0, fb = 0;
    for (let b = 0; b < K; b++) { const i = (b * w + a) * 4; fr += d[i]; fg += d[i + 1]; fb += d[i + 2]; }
    F0[a * 3 + 3] = F0[a * 3] + fr / K; F0[a * 3 + 4] = F0[a * 3 + 1] + fg / K; F0[a * 3 + 5] = F0[a * 3 + 2] + fb / K;
  }
  return { ...g, F0 };
}
/** ROAD-18E: the lights a drive straight ahead lays over its ground (`light`: one, or a list), still on the stage while the
    ground goes by under them: a picture ({ src, x, y }), or a shape filled with a gradient ({ poly, radial: { at, r: [rx, ry] }
    or linear: { from, to }, stops: [[offset, colour, alpha], ...] }; with neither, `color`); each with an `id`, a `blend` (the
    canvas's: "screen", "lighter", "multiply"...; "source-over" if not said) and an `opacity` (1) a script changes with
    set({ light: { id: k } }). Never keyed: light (the hole's) need not be the place's. */
function lightsOf(spec, path) {
  const list = Array.isArray(spec.light) ? spec.light : Array.isArray(spec.lights) ? spec.lights : spec.light && typeof spec.light === "object" ? [spec.light] : [];
  return list.filter((l) => l && (typeof l.src === "string" || polyOf(l.poly))).map((l, i) => ({
    id: String(l.id || `light-${i + 1}`), src: typeof l.src === "string" ? path(l.src) : null, x: num(l.x, 0), y: num(l.y, 0),
    poly: typeof l.src === "string" ? null : polyOf(l.poly),
    radial: l.radial && isPoint(l.radial.at) ? { at: l.radial.at, r: isPair(l.radial.r) ? l.radial.r : [num(l.radial.r, 100), num(l.radial.r, 100)] } : null,
    linear: l.linear && isPoint(l.linear.from) && isPoint(l.linear.to) ? l.linear : null,
    stops: (Array.isArray(l.stops) ? l.stops : []).filter((v) => Array.isArray(v) && typeof v[0] === "number").map(([o, c, a]) => [clamp(o), rgbOf(c, [255, 255, 255]), clamp(num(a, 1))]),
    color: rgbOf(l.color, [255, 255, 255]), blend: typeof l.blend === "string" ? l.blend : "source-over", opacity: clamp(num(l.opacity, 1)), paints: new WeakMap() }));
}
/** ROAD-18E: stretches of road kept clear of seeded things: [[s0, s1], ...] (or one [s0, s1]), metres along the road. */
function gapsOf(v) {
  if (isPair(v)) v = [v];
  return Array.isArray(v) ? v.filter(isPair).map(([a, b]) => [Math.min(a, b), Math.max(a, b)]).sort((p, q) => p[0] - q[0]) : [];
}
const inGap = (gaps, w) => { for (const [a, b] of gaps) { if (w < a) return false; if (w <= b) return true; } return false; };
/** ROAD-18E: the things a sheet has painted for each side of the road, `name-l` for the left and `name-r` for the right (lit
    from the side the sun is on), by the name without its side where the sheet has no picture of that name itself: a row or a
    set piece that names "sage-1" is drawn with "sage-1-l" left of the line of travel and "sage-1-r" right of it (one painted
    for one side only stands for both). -> { L: { name: "name-l" }, R: { name: "name-r" } } */
function sidesOf(sprites) {
  const lr = { L: {}, R: {} };
  for (const name of Object.keys(sprites)) {
    const m = /^(.+)-([lr])$/.exec(name);
    if (m && !sprites[m[1]]) lr[m[2] === "l" ? "L" : "R"][m[1]] = name;
  }
  for (const [a, b] of [["L", "R"], ["R", "L"]]) for (const k of Object.keys(lr[a])) if (!lr[b][k]) lr[b][k] = lr[a][k];
  return lr;
}
/** ROAD-18E: how far a row's things reach, in metres at their own pixels a metre: half the widest, and the tallest (for how
    far its shadows reach). */
function reachOf(pics) {
  return { half: Math.max(0.5, ...pics.map((p) => p.levels[0].w / 2 / p.ppm)), tall: Math.max(0, ...pics.map((p) => p.levels[0].fy / p.ppm)) };
}

class Drive extends Effect {
  constructor(host, spec, n) {
    super(host, spec, n);
    const s = spec, folder = folderOf(host.scene), path = (p) => (typeof p !== "string" ? null : p.startsWith("art/") ? p : folder + p);
    this.ahead = s.side === "ahead";                                 // ROAD-18E: the view straight down the road: both sides, and the road between
    this.side = s.side === "L" ? -1 : s.side === "R" ? 1 : this.ahead ? 1 : 0;      // (ROAD-18E: ahead, x = vanish x + focal * X / z, X negative on the left)
    if (!this.side) throw new Error('a drive needs `side`: "L" or "R", the side of the line of travel its world is on (or "ahead": ROAD-18E)');
    if (!isPoint(s.vanish)) throw new Error("a drive needs `vanish`: [x, y], where the line of travel runs to (its row is the horizon)");
    this.focal = num(s.focal, 0);
    if (!(this.focal > 0)) throw new Error("a drive needs `focal`: the camera's focal length, in pixels");
    this.vx = s.vanish[0]; this.hz = s.vanish[1];
    this.eye = Math.max(0.05, num(s.eye, 1.6));
    this.plane = "back";                                             // (behind everybody, unless it is given a base or a plane)
    this.speed = num(s.speed, 0);
    this.start = num(s.start, 0); this.d0 = this.start; this.t0 = 0;     // metres gone at t0 (ms of its own time): since the last change of speed
    this.fps = Math.max(1, num(s.fps, 30)); this.calmFps = this.fps;    // (for less motion its time runs at half speed, as the strip's)
    // Its pictures are due at its steps, shifted by `phase` of a step: the right side's fall half way between the left's (0
    // and 0.5), so that a frame of the game draws one side's panes and the next frame the other's, never all four at once.
    this.phase = clamp(num(s.phase, this.side > 0 && !this.ahead ? 0.5 : 0), 0, 0.999);      // (ROAD-18E: straight ahead, one drive: 0)
    this.alpha = clamp(num(s.opacity, 1));
    this.streak = Math.max(0, num(s.streak, 0.6));
    this.slices = Math.round(clamp(num(s.slices, DRIVE_SLICES), 1, 6));     // the most slices a pixel's patch of ground is taken in (planGround)
    this.haze = rgbOf(s.haze, [217, 221, 230]); this.hazeFar = Math.max(1, num(s.haze_far, num(s.hazeFar, 4000)));
    this.wire = rgbOf(s.wire, [47, 42, 38]);
    // DRIVE-16F: the things' shadows (none without `sun`). A metre of a thing's height throws its shadow sun[0] m ahead and
    // sun[1] m to the car's left: outward on the left side, toward the road on the right. On the ground (z ahead, X out):
    // along (dz, dX) a metre of height, across it the unit (az, aX).
    this.sun = isPair(s.sun) && (s.sun[0] || s.sun[1]) ? [s.sun[0], s.sun[1]] : null;
    this.shade = rgbOf(s.shade, [102, 100, 172]); this.shadeK = clamp(num(s.shade_k, num(s.shadeK, 0.6)));
    if (this.sun) { const dz = this.sun[0], dX = -this.side * this.sun[1], L = Math.hypot(dz, dX); this.sunWay = { dz, dX, L, az: -dX / L, aX: dz / L }; }
    this.shadeMin = 1.5; this.shadeFace = 0.1;                       // (the least a shadow is drawn on the stage: 10 cm face on, up to 1.5 px: shadowOf)
    this.skySrc = path(s.sky);
    this.bands = (Array.isArray(s.bands) ? s.bands : []).filter((b) => b && typeof b.src === "string")
      .map((b) => ({ src: path(b.src), D: Math.max(1, num(b.distance, 1000)), ppm: Math.max(1e-4, num(b.ppm, 0.1)), tab: null }))
      .sort((a, b) => b.D - a.D);                                      // (far to near, in whatever order they are given)
    const g = s.ground;
    this.ground = g && typeof g.src === "string" ? { src: path(g.src), from: num(g.from, 0), ppm: Math.max(1e-3, num(g.ppm, 16)) } : null;
    const th = s.things;
    this.thingsSrc = th && typeof th.src === "string" ? path(th.src) : null;
    this.sheetPath = this.thingsSrc ? (typeof th.sheet === "string" ? path(th.sheet) : this.thingsSrc.replace(/\.png$/i, "") + ".json") : null;
    this.rows = this.thingsSrc && Array.isArray(th.rows) ? th.rows.map((r, i) => this.rowOf(r, i)).filter(Boolean) : [];
    this.sheet = null;                                               // the sheet's JSON once read (false: it would not come)
    const shapes = polysOf(s.windows).length ? polysOf(s.windows) : polysOf(s.clip);
    if (!shapes.length && this.ahead) shapes.push([[0, 0], [W, 0], [W, H], [0, H]]);         // ROAD-18E: straight ahead with no panes: the stage is the window
    if (!shapes.length) throw new Error("a drive needs `windows`: the panes it is seen through");
    this.wins = shapes.map((poly, i) => {
      const win = { poly, step: null, s: null, calm: null, go: false, sprite: this.mote(":" + i) };
      win.sprite.win = win;
      if (this.ahead) this.frameAhead(win); else this.frame(win);      // (ROAD-18E: frameAhead)
      return win;
    });
    const us = this.wins.flatMap((w) => [...w.U0, ...w.U1]);
    this.uMin = Math.min(...us); this.uMax = Math.max(...us);         // the directions the panes see, all of them
    this.world = null;                                               // the things and wires as seen from one s, for all the panes
    this.tabs = null;                                                // the pictures' tables, once they are all here
    this.cost = { pictures: 0, ms: 0, last: 0, most: 0, tables: 0 };  // what its pictures took (ms), and its pictures' tables, for the tests
    this.gen = 0;                                                    // ROAD-18E: how many pictures it has drawn (a door in time that bends it reads it again when this changes)
    if (this.ahead) this.setupAhead(s, path);                        // ROAD-18E: its strips of ground, lights, gaps and set pieces
    this.ready();
  }
  /** A row of things, as the engine places them: from the seed, a thing in each cell of `cell` metres along the road. */
  rowOf(r, i) {
    if (!r || typeof r !== "object") return null;
    const names = (Array.isArray(r.sprite) ? r.sprite : [r.sprite]).filter((v) => typeof v === "string");
    if (!names.length) return null;
    const every = isPair(r.every) ? [Math.max(0.1, Math.min(...r.every)), Math.max(0.1, ...r.every)] : Math.max(0.1, num(r.every, 10));
    const mean = isPair(every) ? (every[0] + every[1]) / 2 : every, loop = num(r.loop, 0);
    const n = loop > 0 ? Math.max(1, Math.round(loop / mean)) : 0, cell = n ? loop / n : mean;
    const seed = mix(this.seed, i + 1) >>> 0, at = isPair(r.at) ? [Math.min(...r.at), Math.max(...r.at)] : num(r.at, 10);
    return this.aheadRow(r, { names, n, cell, jit: isPair(every) ? (every[1] - every[0]) / 4 : 0, seed, offset: num(r.offset, rnd(seed, 7) * cell), at,
      Xs: isPair(at) ? at : [at, at], wires: (Array.isArray(r.wires) ? r.wires : []).map((v) => (isPair(v) ? [v[0], v[1]] : typeof v === "number" && Number.isFinite(v) ? [0, v] : null)).filter(Boolean), sag: num(r.sag, null), wireAlpha: r.wire_alpha == null ? null : clamp(num(r.wire_alpha, 1)), farAhead: Math.max(0, num(r.far, 0)) });      // ROAD-18M: wire_alpha, how solid its wires are (as the side views have them, if not said); far, metres: none of its things farther off straight ahead (things_far, if not said)      // (ROAD-18E: aheadRow; a wire is [across, up] from the thing's foot: a height alone is [0, height])
  }
  /** Thing i of a row: where it stands along the road (metres from where the road begins), how far out, which picture. In a
      row that loops, thing i + n is thing i again, a loop further on. (A range for `every`: each in its cell, moved by up to
      a quarter of the range either way, so that from one to the next is within it.) */
  thing(row, i) {
    const k = row.n ? ((i % row.n) + row.n) % row.n : i;
    return { w: row.offset + i * row.cell + (row.jit ? (rnd(row.seed, k, 1) * 2 - 1) * row.jit : 0), X: within(row.at, rnd(row.seed, k, 2)),
      name: row.names[Math.min(row.names.length - 1, Math.floor(rnd(row.seed, k, 3) * row.names.length))] };
  }
  /** A pane's picture, its place on the stage, its hard-edged shape (a pixel is in it when its middle is), and the tables
      that do not change: for each column of it, the directions its edges look in (u, from the vanishing point). */
  frame(win) {
    const [x0, y0, x1, y1] = boxOf(win.poly), box = [Math.max(0, Math.floor(x0)), Math.max(0, Math.floor(y0)), Math.min(W, Math.ceil(x1)), Math.min(H, Math.ceil(y1))];
    const w = Math.max(1, box[2] - box[0]), h = Math.max(1, box[3] - box[1]);
    Object.assign(win, { box, w, h, pair: new Pair(w, h), mask: canvasOf(w, h), inside: new Uint8Array(w * h) });
    const img = win.mask.getContext("2d").createImageData(w, h), d = img.data;
    win.rowA = new Int32Array(h).fill(-1); win.rowB = new Int32Array(h); win.colA = new Int32Array(w).fill(-1); win.colB = new Int32Array(w);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      if (!inside(win.poly, box[0] + x + 0.5, box[1] + y + 0.5)) continue;
      win.inside[y * w + x] = 1; d[(y * w + x) * 4 + 3] = 255;
      if (win.rowA[y] < 0) win.rowA[y] = x;
      win.rowB[y] = x + 1;
      if (win.colA[x] < 0) win.colA[x] = y;
      win.colB[x] = y + 1;
    }
    win.mask.getContext("2d").putImageData(img, 0, 0);
    win.U0 = new Float32Array(w); win.U1 = new Float32Array(w); win.KD = new Float32Array(w);
    for (let x = 0; x < w; x++) {
      const c = box[0] + x, u = this.side < 0 ? this.vx - c - 1 : c - this.vx;          // (its nearer edge to the vanishing point)
      win.U0[x] = Math.max(0.25, u); win.U1[x] = Math.max(0.5, u + 1);
      const uc = (win.U0[x] + win.U1[x]) / 2;
      win.KD[x] = (Math.LN2 * Math.sqrt(1 + (uc / this.focal) ** 2)) / this.hazeFar;      // the haze, a metre ahead in this column
    }
    win.hazeK = new Float32Array(w * h);                             // and how much of each pixel of ground it covers (as far off as the middle of its patch)
    for (let y = 0; y < h; y++) { const dy = box[1] + y + 0.5 - this.hz; if (dy > 0) for (let x = 0; x < w; x++) win.hazeK[y * w + x] = 1 - Math.exp(-((this.focal * this.eye) / dy) * win.KD[x]); }
    win.rowU0 = new Float32Array(h); win.rowU1 = new Float32Array(h);
    for (let y = 0; y < h; y++) {
      let lo = Infinity, hi = 0;
      for (let x = Math.max(0, win.rowA[y]); x < win.rowB[y]; x++) if (win.inside[y * w + x]) { lo = Math.min(lo, win.U0[x]); hi = Math.max(hi, win.U1[x]); }
      win.rowU0[y] = lo; win.rowU1[y] = hi;
    }
    win.out = new ImageData(w, h); win.out32 = new Uint32Array(win.out.data.buffer);
    win.sprite.place(box[0], box[1]);
  }
  pics() { return [this.skySrc, ...this.bands.map((b) => b.src), this.ground && this.ground.src, this.thingsSrc, ...(this.ahead ? [...this.strips.map((g) => g.src), ...this.lights.filter((l) => l.src).map((l) => l.src)] : [])].filter(Boolean); }      // (ROAD-18E: straight ahead, its strips of ground and its pictures of light)
  /** Its pictures here, the sheet that says where each thing is on its sheet read (held for the session, as a picture is),
      and, if it is on the stage as the scene opens, the tables made from them: so that a scene does not show (Effects.enter
      waits for this) until its first picture can be drawn without a pause (the tables of the limousine's pictures take some
      60 ms a side, once a session). One that is not on the stage yet (its `when`) makes them as it is first shown. */
  ready() {
    if (this.waiting) return this.waiting;
    const sheet = !this.sheetPath ? null : hold(this.sheetPath).then(async (address) => {
      let json = null;
      try { json = address ? await (await fetch(address)).json() : null; } catch { /* below */ }
      this.sheet = json && json.sprites && typeof json.sprites === "object" ? json : false;
      if (!this.sheet) console.warn(`The drive "${this.id}" (${this.host.place || "added by a script"}) has no sheet for its things (${this.sheetPath}): they are left out.`);
    });
    return (this.waiting = Promise.all([sheet, ...this.pics().map(fetchPicture)]).then(() => { if (this.host.on && this.wanted()) this.here(); }));
  }
  /** Every picture here and its tables made (once a picture, for good): false until then. */
  here() {
    if (this.tabs) return true;
    const got_ = (p) => { const i = got(p); return i && i.naturalWidth ? i : null; };
    if (this.pics().some((p) => !got_(p)) || (this.sheetPath && this.sheet === null)) return false;
    const t0 = performance.now();
    const sky = this.skySrc ? driveTables(got_(this.skySrc), "sky", ({ w, h, d }) => ({ w, h, u32: new Uint32Array(d.buffer, d.byteOffset, w * h) })) : null;
    for (const b of this.bands) b.tab = driveTables(got_(b.src), "band", bandSums);
    const ground = this.ground ? driveTables(got_(this.ground.src), "ground", groundSums) : null;
    let sprites = {};
    if (this.thingsSrc && this.sheet) {
      const sheet = this.sheet, img = got_(this.thingsSrc), all = driveTables(img, "sheet", (px) => ({ px, levels: new Map() }));
      this.sheetPpm = Math.max(1e-3, num(sheet.ppm, 24));
      for (const [name, sp] of Object.entries(sheet.sprites)) {
        if (!sp || !Array.isArray(sp.box) || sp.box.length !== 4) continue;
        const key = JSON.stringify([sp.box, sp.foot]);
        if (!all.levels.has(key)) all.levels.set(key, spriteLevels(all.px, sp.box, sp.foot));
        const shapes = all.shapes || (all.shapes = new Map());                    // DRIVE-16F: what its shadow is made from, made once
        if (this.sun && !shapes.has(key)) shapes.set(key, shadowShape(all.px, sp.box, sp.foot));
        sprites[name] = { levels: all.levels.get(key), height: num(sp.height, null), shape: this.sun ? shapes.get(key) : null,
          ppm: Math.max(1e-3, num(sp.ppm, this.sheetPpm)), air: clamp(num(sp.air, 1)) };      // ROAD-18E: its own pixels a metre, where it has them (the signs'); the sheet's if not. And `air`: how much of the haze it takes (1; 0 for a thing painted in its own air)
      }
      const lr = this.ahead ? sidesOf(sprites) : null;               // ROAD-18E: straight ahead, the things painted for each side of the road
      for (const r of this.rows) {
        for (const nm of r.names) if (!sprites[nm] && !(lr && lr.L[nm])) warnDrive(this, `has no picture called "${nm}" on its sheet: those are left out`);      // (ROAD-18E: nor "-l" and "-r")
        if (lr) { const pics = r.names.flatMap((nm) => [sprites[lr.L[nm] || nm], sprites[lr.R[nm] || nm]]).filter(Boolean); r.reach = pics.length ? reachOf(pics) : null; }      // (ROAD-18E: how wide and tall its things are, at their own pixels a metre)
        r.half = Math.max(0.5, ...r.names.filter((nm) => sprites[nm]).map((nm) => sprites[nm].levels[0].w / 2 / this.sheetPpm));     // (metres: the widest of its pictures, half)
        r.tall = Math.max(0, ...r.names.filter((nm) => sprites[nm]).map((nm) => sprites[nm].levels[0].fy / this.sheetPpm));          // DRIVE-16F: (metres: the tallest, for how far its shadows reach)
      }
    }
    const most = Math.max(1, ...this.bands.map((b) => b.tab.h));
    const gs = ((ground ? ground.h : 0) + 3) * 3 * 6;
    this.tabs = { sky, ground, sprites, R: new Float64Array(gs), Q: new Float64Array(gs), SL: new Float64Array(16 * 6),
      C: new Float64Array((most + 2) * 4), CQ: new Float64Array((most + 3) * 4) };
    if (this.ahead) { this.tabs.strips = this.stripsHere(got_); this.tabs.lr = sidesOf(sprites); }      // ROAD-18E: straight ahead, the strips of ground; the things for each side
    this.cost.tables = performance.now() - t0;                       // (ms: no time at all for pictures whose sums another drive has made)
    return true;
  }
  slots() { return this.sprites; }
  restart() { this.d0 = this.start; this.t0 = 0; this.world = null; for (const w of this.wins) w.step = null; }
  /** Metres gone at a moment of its own time (ms). */
  gone(t) { return this.d0 + (this.speed * Math.max(0, t - this.t0)) / 1000; }
  /** For scripts: { speed } (metres a second; 0 parks it), { opacity }. It goes on from where it is. */
  set(o = {}) {
    if (this.ahead && o) this.setAhead(o);                           // ROAD-18E: straight ahead, also { s }, { light: { id: k } }, { gap } (setAhead)
    if (o && typeof o.speed === "number" && Number.isFinite(o.speed) && o.speed !== this.speed && !(this.ahead && typeof o.s === "number")) { this.d0 = this.gone(this.time); this.t0 = this.time; this.speed = o.speed; }      // (ROAD-18E: with { s }, setAhead has it)
    if (o && typeof o.opacity === "number") { this.alpha = clamp(o.opacity); for (const w of this.wins) w.step = null; }
    return this;
  }
  /** Its step at a moment of its time (ms), and where it is (metres gone) at a step. */
  stepAt(t) { return Math.floor((t * this.fps) / 1000 + this.phase); }
  at(step) { return this.gone(((step - this.phase) / this.fps) * 1000); }
  /** Each pane's next picture is due when it has gone on since the last (or less motion has come or gone); drawn in its turn. */
  update(calm) {
    const s = this.at(this.stepAt(this.time));
    for (const w of this.wins) if (w.step !== null) w.sprite.want = s !== w.s || calm !== w.calm || (this.ahead && this.stale(w, s));      // (ROAD-18E: stale)
  }
  grant(sprite) { if (sprite.win) sprite.win.go = true; }
  picture(sprite, calm) {
    const w = sprite.win;
    if (!w || !this.here()) return null;                             // (not here yet)
    const step = this.stepAt(this.time), s = this.at(step), go = w.go;
    w.go = false;
    if (w.step === null || (go && (s !== w.s || calm !== w.calm || (this.ahead && this.stale(w, s))))) {           // (the first picture at once; after that, in its turn. ROAD-18E: stale)
      if (this.ahead) w.moved = w.step !== null && step > w.step && step - w.step <= 3 ? Math.abs(s - w.s) / (step - w.step) : 0;      // ROAD-18E: how far it went a picture, since the one before (a script carrying it)
      w.step = step; w.s = s; w.calm = calm;
      const t0 = performance.now();
      this.paint(w, s, calm);
      const ms = performance.now() - t0, c = this.cost;
      c.pictures++; c.ms += ms; c.last = ms; c.most = Math.max(c.most, ms);
      this.gen++;                                                    // ROAD-18E: a new picture (for a door in time that bends it)
    } else if (this.ahead && w.step !== null) this.prepare(w, step, calm);     // ROAD-18E: a frame that draws none: the next picture's ground, ahead of time
    return { canvas: w.pair.canvas, ox: 0, oy: 0 };
  }
  /** One pane's picture with the car gone s metres: the sky and the ground, the bands, the things; cut to the pane. */
  paint(w, s, calm) {
    if (this.ahead) return this.paintAhead(w, s, calm);              // ROAD-18E: straight ahead (paintAhead)
    const travel = calm ? 0 : (this.streak * Math.abs(this.speed)) / this.fps;     // metres the ground is averaged over along its motion
    this.base(w, s, travel);
    for (const band of this.bands) this.band(w, band, s);
    const ctx = w.pair.next();
    ctx.putImageData(w.out, 0, 0);
    w.shadows = this.sun ? this.shadows(ctx, w, s) : 0;              // DRIVE-16F: the things' shadows on the ground, then the things
    w.things = this.things(ctx, w, s);
    ctx.globalCompositeOperation = "destination-in"; ctx.globalAlpha = this.alpha;
    ctx.drawImage(w.mask, 0, 0);                                     // (nothing outside the pane)
    ctx.globalAlpha = 1; ctx.globalCompositeOperation = "source-over";
    this.drawn = this.wins.reduce((sum, v) => sum + 1 + (v.things || 0), 0);
  }
  /**
   * What a pane's ground sees that never changes (the pane and the camera are fixed): each row below the horizon (z from
   * zBot, its lower edge, to zTop, its upper edge; at the horizon, endless) sees columns [aLo, aLo + foot] of the picture
   * along the road, aLo going on with the car. A pixel's patch is the slanting strip between the lines of sight at its edges
   * (the further along the road, the further across it), so it is taken in K slices along the road (one for each four
   * pixels of the picture it is long, up to `slices`): each slice averaged along the road over its own stretch (R, for each
   * pixel of the picture across the road), then across, over the stretch its pixel sees there. Made once for each pane: for
   * each row its slices, and the pixels of the picture across the road its sums must cover (k0 and n).
   */
  planGround(w) {
    const G = this.tabs.ground, gr = this.ground, f = this.focal, e = this.eye, hz = this.hz, ppm = gr.ppm, from = gr.from, gh = G.h, rows = [];
    for (let j = 0; j < w.h; j++) {
      const x0 = w.rowA[j], x1 = w.rowB[j], r = w.box[1] + j;
      if (x0 < 0 || r + 0.5 <= hz) continue;
      const zBot = (f * e) / (r + 1 - hz), zTop = r > hz ? (f * e) / (r - hz) : Infinity, foot = zTop === Infinity ? G.w : (zTop - zBot) * ppm;
      const K = zTop === Infinity ? 1 : Math.max(1, Math.min(this.slices, Math.ceil(foot / 4)));
      const bFirst = ((w.rowU0[j] * zBot) / f - from) * ppm, bLast = zTop === Infinity ? Infinity : ((w.rowU1[j] * zTop) / f - from) * ppm;
      const k0 = Math.max(0, Math.min(gh, Math.floor(bFirst))), k1 = Math.max(k0, Math.min(gh, Math.ceil(Math.min(bLast, gh))));
      // for each slice, what its stretch across the road is for a pixel looking along u: [u0 * zl[k] - kb, u1 * zh[k] - kb]
      const zl = [], zh = [];
      for (let k = 0; k < K; k++) { zl.push(((zBot + (foot * k) / K / ppm) / f) * ppm); zh.push(((zBot + (foot * (k + 1)) / K / ppm) / f) * ppm); }
      rows.push({ j, x0, x1, zBot, zTop, foot, K, k0, n: k1 - k0, beyond: k1 >= gh, zl, zh, kb: k0 + from * ppm });
    }
    return { rows };
  }
  /** The sky (as painted, still) above the horizon, and the ground below it, into the pane's pixels. */
  base(w, s, travel) {
    const T = this.tabs, out = w.out32, ins = w.inside, pw = w.w, bx = w.box[0], by = w.box[1], hz = this.hz;
    const sky = T.sky, s32 = sky && sky.u32, sw = sky ? sky.w : 0, sh = sky ? sky.h : 0, G = T.ground;
    for (let j = 0; j < w.h; j++) {                                  // the sky
      const x0 = w.rowA[j], r = by + j, o = j * pw;
      if (x0 < 0 || (G && r + 0.5 > hz)) continue;
      for (let x = x0, x1 = w.rowB[j]; x < x1; x++) { if (!ins[o + x]) continue; const c = bx + x; out[o + x] = s32 && c < sw && r < sh ? s32[r * sw + c] : 0; }
    }
    if (!G) return;
    const plan = w.plan || (w.plan = this.planGround(w)), U0 = w.U0, U1 = w.U1;
    const gr = this.ground, ppm = gr.ppm, gw = G.w, gh = G.h, P = G.P, F = G.F, R = T.R, Q = T.Q, SL = T.SL, stride = (gh + 3) * 3, tot = gw * gh * 3, ft = gw * 3;
    const hr = this.haze[0], hg = this.haze[1], hb = this.haze[2], HZ = w.hazeK, long = travel * ppm;
    for (const row of plan.rows) {
      const { j, x0, x1, K, k0, n, foot } = row, o = j * pw, aLo = (row.zBot + s) * ppm;
      // A row going by faster than it is long (its picture's travel, times the streak, longer than its patch) is averaged
      // along the road over that much: the streak. A slower row is as it is parked.
      const ext = long > foot ? (long - foot) / 2 : 0;
      if (K > 1 && !ext) this.sums(G, R, Q, SL, aLo, foot, K, k0, n, row.beyond, stride);       // (slices that meet end to end: summed together)
      else for (let k = 0; k < K; k++) {
        const sp = spanOf(aLo + (foot * k) / K - ext, aLo + (foot * (k + 1)) / K + ext, gw), fH = sp.fH, fL = sp.fL, gH = 1 - fH, gL = 1 - fL, loops = sp.loops, inv = sp.inv;
        const h0 = sp.mH * gh * 3, h1 = h0 + gh * 3, l0 = sp.mL * gh * 3, l1 = l0 + gh * 3, sl = k * 16, off = k * stride, mH = sp.mH * 3, mL = sp.mL * 3;
        SL[sl + 4] = (F[mH] * gH + F[mH + 3] * fH + loops * F[ft] - F[mL] * gL - F[mL + 3] * fL) * inv;          // the colour beyond its last row
        SL[sl + 5] = (F[mH + 1] * gH + F[mH + 4] * fH + loops * F[ft + 1] - F[mL + 1] * gL - F[mL + 4] * fL) * inv;
        SL[sl + 6] = (F[mH + 2] * gH + F[mH + 5] * fH + loops * F[ft + 2] - F[mL + 2] * gL - F[mL + 5] * fL) * inv;
        if (row.zTop === Infinity) continue;
        // R: each pixel of the picture across the road, averaged along this slice's stretch of it; Q: R summed outward from k0
        Q[off] = Q[off + 1] = Q[off + 2] = 0;
        for (let b3 = k0 * 3, q = off, end = (k0 + n) * 3; b3 < end; b3 += 3, q += 3) {
          const vr = (P[h0 + b3] * gH + P[h1 + b3] * fH + loops * P[tot + b3] - P[l0 + b3] * gL - P[l1 + b3] * fL) * inv;
          const vg = (P[h0 + b3 + 1] * gH + P[h1 + b3 + 1] * fH + loops * P[tot + b3 + 1] - P[l0 + b3 + 1] * gL - P[l1 + b3 + 1] * fL) * inv;
          const vb = (P[h0 + b3 + 2] * gH + P[h1 + b3 + 2] * fH + loops * P[tot + b3 + 2] - P[l0 + b3 + 2] * gL - P[l1 + b3 + 2] * fL) * inv;
          R[q] = vr; R[q + 1] = vg; R[q + 2] = vb; Q[q + 3] = Q[q] + vr; Q[q + 4] = Q[q + 1] + vg; Q[q + 5] = Q[q + 2] + vb;
        }
        this.ends(SL, R, k, off, n, row.beyond);
      }
      if (row.zTop === Infinity) {                                   // the horizon: all of it beyond the picture, far off
        for (let x = x0; x < x1; x++) {
          if (!ins[o + x]) continue;
          const hk = HZ[o + x], cr = SL[4] + (hr - SL[4]) * hk, cg = SL[5] + (hg - SL[5]) * hk, cb = SL[6] + (hb - SL[6]) * hk;
          out[o + x] = 0xff000000 | ((cb < 0 ? 0 : cb > 255 ? 255 : cb + 0.5) << 16) | ((cg < 0 ? 0 : cg > 255 ? 255 : cg + 0.5) << 8) | (cr < 0 ? 0 : cr > 255 ? 255 : cr + 0.5);
        }
        continue;
      }
      const kb = row.kb, zl = row.zl, zh = row.zh;
      for (let x = x0; x < x1; x++) {
        if (!ins[o + x]) continue;
        const u0 = U0[x], u1 = U1[x];
        let cr = 0, cg = 0, cb = 0;
        for (let k = 0, sl = 0, off = 0; k < K; k++, sl += 16, off += stride) {
          // the sum of R over the stretch this pixel's slice sees ([lo, hi], from k0): before k0 the first pixel's colour, after
          // k0 + n the colour after it
          const lo = u0 * zl[k] - kb, hi = u1 * zh[k] - kb;
          let a = off, f0 = 0, c = off + n * 3, f1 = 0, ws = 0, we = 0;
          if (lo < 0) ws = -lo; else if (lo >= n) { we = n - lo; a = c; } else { const i = lo | 0; a += i * 3; f0 = lo - i; }
          if (hi >= n) we += hi - n; else if (hi < 0) { c = off; ws += hi; } else { const i = hi | 0; c = off + i * 3; f1 = hi - i; }
          const inv = 1 / (hi - lo);
          cr += (Q[c] + f1 * R[c] - Q[a] - f0 * R[a] + ws * SL[sl + 7] + we * SL[sl + 10]) * inv;
          cg += (Q[c + 1] + f1 * R[c + 1] - Q[a + 1] - f0 * R[a + 1] + ws * SL[sl + 8] + we * SL[sl + 11]) * inv;
          cb += (Q[c + 2] + f1 * R[c + 2] - Q[a + 2] - f0 * R[a + 2] + ws * SL[sl + 9] + we * SL[sl + 12]) * inv;
        }
        if (K > 1) { cr /= K; cg /= K; cb /= K; }
        const hk = HZ[o + x];                                        // the haze, as far off as the middle of the patch is
        cr += (hr - cr) * hk; cg += (hg - cg) * hk; cb += (hb - cb) * hk;
        out[o + x] = 0xff000000 | ((cb < 0 ? 0 : cb > 255 ? 255 : cb + 0.5) << 16) | ((cg < 0 ? 0 : cg > 255 ? 255 : cg + 0.5) << 8) | (cr < 0 ? 0 : cr > 255 ? 255 : cr + 0.5);
      }
    }
  }
  /** A slice's colours before the first pixel of its sums (the first's), and after the last (beyond the picture, the colour
      beyond it; else the last's): SL[k * 16 + 7..9] and [10..12], beside the colour beyond at [4..6]. */
  ends(SL, R, k, off, n, beyond) {
    const sl = k * 16;
    R[off + n * 3] = R[off + n * 3 + 1] = R[off + n * 3 + 2] = 0;
    for (let c = 0; c < 3; c++) {
      SL[sl + 7 + c] = n > 0 ? R[off + c] : SL[sl + 4 + c];
      SL[sl + 10 + c] = beyond || n === 0 ? SL[sl + 4 + c] : R[off + (n - 1) * 3 + c];
    }
  }
  /** The K slices of a row whose stretches meet end to end (no streak): the sums along the road read once at each of the
      K + 1 edges, for each pixel of the picture across the road that the row needs, and each slice's R and Q from them. */
  sums(G, R, Q, SL, aLo, foot, K, k0, n, beyond, stride) {
    const gw = G.w, gh = G.h, P = G.P, F = G.F, tot = gw * gh * 3, ft = gw * 3, E = this.edges || (this.edges = new Float64Array(8 * 6)), inv = K / foot;
    for (let k = 0; k <= K; k++) {                                   // each edge: its two columns of sums, their weights, its loops
      const a = aLo + (foot * k) / K, i = Math.floor(a), m = ((i % gw) + gw) % gw, o = k * 6;
      E[o] = m * gh * 3; E[o + 1] = E[o] + gh * 3; E[o + 2] = a - i; E[o + 3] = (i - m) / gw; E[o + 4] = m * 3;
    }
    for (let k = 0; k < K; k++) {                                   // the colour beyond the picture, along each slice's stretch
      const a = k * 6, b = a + 6;
      for (let c = 0; c < 3; c++) {
        const lo = F[E[a + 4] + c] * (1 - E[a + 2]) + F[E[a + 4] + 3 + c] * E[a + 2] + E[a + 3] * F[ft + c], hi = F[E[b + 4] + c] * (1 - E[b + 2]) + F[E[b + 4] + 3 + c] * E[b + 2] + E[b + 3] * F[ft + c];
        SL[k * 16 + 4 + c] = (hi - lo) * inv;
      }
      Q[k * stride] = Q[k * stride + 1] = Q[k * stride + 2] = 0;
    }
    const V = this.edgeSums || (this.edgeSums = new Float64Array(8 * 3));
    for (let b3 = k0 * 3, q = 0, end = (k0 + n) * 3; b3 < end; b3 += 3, q += 3) {
      for (let k = 0, o = 0, v = 0; k <= K; k++, o += 6, v += 3) {   // the sums at each edge, here
        const r0 = E[o] + b3, r1 = E[o + 1] + b3, fk = E[o + 2], gk = 1 - fk, lp = E[o + 3];
        V[v] = P[r0] * gk + P[r1] * fk + lp * P[tot + b3]; V[v + 1] = P[r0 + 1] * gk + P[r1 + 1] * fk + lp * P[tot + b3 + 1]; V[v + 2] = P[r0 + 2] * gk + P[r1 + 2] * fk + lp * P[tot + b3 + 2];
      }
      for (let k = 0, v = 0, off = q; k < K; k++, v += 3, off += stride) {
        const vr = (V[v + 3] - V[v]) * inv, vg = (V[v + 4] - V[v + 1]) * inv, vb = (V[v + 5] - V[v + 2]) * inv;
        R[off] = vr; R[off + 1] = vg; R[off + 2] = vb; Q[off + 3] = Q[off] + vr; Q[off + 4] = Q[off + 1] + vg; Q[off + 5] = Q[off + 2] + vb;
      }
    }
    for (let k = 0; k < K; k++) this.ends(SL, R, k, k * stride, n, beyond);
  }
  /** A band laid over the pane's pixels, column by column: its column for what the stage's column looks at, averaged over the
      stretch of it the column sees, from its foot up at its size there; each pixel the average of what it covers. */
  band(w, band, s) {
    const T = this.tabs, B = band.tab, bw = B.w, bh = B.h, P = B.P, C = T.C, CQ = T.CQ, out = w.out32, ins = w.inside, pw = w.w, by = w.box[1];
    const f = this.focal, e = this.eye, hz = this.hz, D = band.D, ppm = band.ppm;
    for (let x = 0; x < pw; x++) {
      if (w.colA[x] < 0) continue;
      const u0 = w.U0[x], u1 = w.U1[x], uc = (u0 + u1) / 2, foot = hz + (e * uc) / D, k = uc / (D * ppm), top = foot - bh * k;
      const rA = Math.max(by + w.colA[x], Math.floor(top)), rB = Math.min(by + w.colB[x], Math.ceil(foot));
      if (rA >= rB) continue;
      const lo = ((f * D) / u1 + s) * ppm, hi = ((f * D) / u0 + s) * ppm;
      let ridge = bh;                                                // the highest ridge in the stretch of the band this column sees
      for (let a = Math.floor(lo), last = Math.min(Math.floor(hi), a + bw - 1); a <= last; a++) { const t = B.top[((a % bw) + bw) % bw]; if (t < ridge) ridge = t; }
      const tA = Math.max(ridge, Math.floor(bh - (foot - rA) / k)), tB = Math.min(bh, Math.ceil(bh - (foot - rB) / k));
      if (tA >= tB) continue;
      const { mH, fH, mL, fL, loops, inv } = spanOf(lo, hi, bw);
      const h0 = mH * bh * 4, h1 = h0 + bh * 4, l0 = mL * bh * 4, l1 = l0 + bh * 4, tot = bw * bh * 4;
      CQ[0] = CQ[1] = CQ[2] = CQ[3] = 0;
      for (let t = tA, q = 0; t < tB; t++, q += 4) {
        const t4 = t * 4;
        for (let c = 0; c < 4; c++) {
          const v = (P[h0 + t4 + c] * (1 - fH) + P[h1 + t4 + c] * fH + loops * P[tot + t4 + c] - P[l0 + t4 + c] * (1 - fL) - P[l1 + t4 + c] * fL) * inv;
          C[q + c] = v; CQ[q + 4 + c] = CQ[q + c] + v;
        }
      }
      const n = tB - tA;
      C[n * 4] = C[n * 4 + 1] = C[n * 4 + 2] = C[n * 4 + 3] = 0;
      for (let r = rA; r < rB; r++) {
        const i = (r - by) * pw + x;
        if (!ins[i]) continue;
        const t0 = bh - (foot - r) / k, t1 = bh - (foot - r - 1) / k, c0 = Math.max(t0, tA), c1 = Math.min(t1, tB);
        if (c1 <= c0) continue;
        const p0 = c0 - tA, p1 = c1 - tA, i0 = Math.floor(p0), i1 = Math.min(n, Math.floor(p1)), g0 = (p0 - i0), g1 = p1 - i1, a4 = i0 * 4, b4 = i1 * 4, sp = (t1 - t0);
        const sa = (CQ[b4 + 3] + g1 * C[b4 + 3] - CQ[a4 + 3] - g0 * C[a4 + 3]) / sp;      // how solid, over the whole pixel
        if (sa < 0.5) continue;
        const sr = (CQ[b4] + g1 * C[b4] - CQ[a4] - g0 * C[a4]) / sp, sg = (CQ[b4 + 1] + g1 * C[b4 + 1] - CQ[a4 + 1] - g0 * C[a4 + 1]) / sp, sb = (CQ[b4 + 2] + g1 * C[b4 + 2] - CQ[a4 + 2] - g0 * C[a4 + 2]) / sp;
        const v = out[i], da = v >>> 24, keep = 1 - Math.min(255, sa) / 255;
        let rr, gg, bb, aa;
        if (da === 255) { rr = sr + (v & 255) * keep; gg = sg + ((v >>> 8) & 255) * keep; bb = sb + ((v >>> 16) & 255) * keep; aa = 255; }
        else {                                                      // (over a sky with clear pixels: as it is laid over the backdrop)
          const q = (da / 255) * keep;
          aa = Math.min(255, sa + da * keep);
          rr = aa > 0 ? ((sr + (v & 255) * q) * 255) / aa : 0; gg = aa > 0 ? ((sg + ((v >>> 8) & 255) * q) * 255) / aa : 0; bb = aa > 0 ? ((sb + ((v >>> 16) & 255) * q) * 255) / aa : 0;
        }
        out[i] = ((Math.round(aa) << 24) | (Math.max(0, Math.min(255, Math.round(bb))) << 16) | (Math.max(0, Math.min(255, Math.round(gg))) << 8) | Math.max(0, Math.min(255, Math.round(rr)))) >>> 0;
      }
    }
  }
  /** The things and the wires as seen with the car gone s metres, far to near: worked out once for each s, for every pane. */
  sights(s) {
    if (this.ahead) return this.sightsAhead(s);                      // ROAD-18E: straight ahead (sightsAhead)
    if (this.world && this.world.s === s) return this.world.items;
    const items = [], f = this.focal, e = this.eye, sprites = this.tabs.sprites, sppm = this.sheetPpm || 24, near = 1.5, sw = this.sunWay;
    for (const [ri, row] of this.rows.entries()) {
      // the things of this row any pane can see: from where the nearest touches the panes' widest look, to where the farthest
      // touches their narrowest (a thing X out and z ahead spans u from focal * (X - half) / z to focal * (X + half) / z).
      // DRIVE-16F: and those whose shadows can lie in a pane: as far out or in, and ahead or back, as the tallest one's reaches
      const half = row.half || 0.5, out = sw ? sw.dX * (row.tall || 0) : 0, fwd = sw ? sw.dz * (row.tall || 0) : 0, wide = sw ? half : 0;
      const zLo = Math.max(near, (f * (row.Xs[0] - half + Math.min(0, out))) / this.uMax - Math.max(0, fwd) - wide), zHi = (f * (row.Xs[1] + half + Math.max(0, out))) / Math.max(0.5, this.uMin) - Math.min(0, fwd) + wide;
      const iA = Math.floor((s + zLo - row.offset - row.jit) / row.cell) - 1, iB = Math.ceil((s + zHi - row.offset + row.jit) / row.cell) + 1;
      if (iB - iA > 4000) { warnDrive(this, `has a row of "${row.names[0]}" too close together to draw (every ${row.cell.toFixed(2)} m)`); continue; }
      let prev = null;
      for (let i = iA; i <= iB; i++) {
        const t = this.thing(row, i), z = t.w - s, sp = sprites[t.name];
        if (sp && z >= near) {
          const k = f / (z * sppm), L = k >= 1 ? 0 : Math.min(sp.levels.length - 1, Math.floor(Math.log2(1 / k))), lv = sp.levels[L], rel = k * 2 ** L;
          if (lv.h * rel >= 1) items.push({ z, wire: false, x: this.vx + (this.side * f * t.X) / z, y: this.hz + (f * e) / z, lv, rel, hard: k >= 1, key: `${ri}:${i}`, name: t.name,
            shadow: sw && sp.shape ? this.shadowOf(sp.shape, t.X, z) : null });          // (DRIVE-16F)
        }
        if (prev && row.wires.length) this.wires(row, prev, t, s, items);
        prev = t;
      }
    }
    items.sort((a, b) => b.z - a.z);
    this.world = { s, items };
    return items;
  }
  /** The wires from one thing of a row to the next, at each of the row's heights: a line through points along the span,
      sagging in the middle, cut where it comes nearer than 1.5 m. Each at the depth of its far end. */
  wires(row, a, b, s, items) {
    const f = this.focal, e = this.eye, near = 1.5, za = a.w - s, zb = b.w - s;
    if (zb < near) return;
    const span = Math.hypot(b.w - a.w, b.X - a.X), sag = row.sag != null ? row.sag : 0.015 * span, N = 10;
    const tA = za >= near ? 0 : (near - za) / (zb - za);
    for (const [dX, h] of row.wires) {                               // (ROAD-18E: [across, up]: a wire from insulators off to one side of the post, dX 0 for one on it)
      const pts = [];
      for (let q = 0; q <= N; q++) {
        const t = tA + ((1 - tA) * q) / N, z = za + (zb - za) * t, X = a.X + dX + (b.X - a.X) * t, Y = h - sag * 4 * t * (1 - t);
        pts.push(this.vx + (this.side * f * X) / z, this.hz + (f * (e - Y)) / z);
      }
      items.push({ z: zb, wire: true, pts, alpha: row.wireAlpha != null ? row.wireAlpha : clamp(0.25 + 6 / Math.max(1, (za + zb) / 2), 0.3, 0.9) });      // (ROAD-18M: or the row's own wire_alpha)
    }
  }
  /** DRIVE-16F: a thing's shadow, the thing standing X out and z ahead: a band on the ground from its foot along the sun, as
      long as the light makes it, its width at each point the thing's width at the height that throws it (shadowShape); its
      middle line worked out on the ground in metres and put on the stage with the camera, and its width there by the
      camera's rates of change at each point (the ground is seen aslant: a metre across the band is drawn mostly along it,
      and a little across). -> { pts: [x, y, ...], x0, y0, x1, y1 } on the stage, one side of the band up and the other
      back; or null when it would be too faint to see. */
  shadowOf(shape, X, z) {
    const f = this.focal, e = this.eye, sd = this.side, ppm = this.sheetPpm || 24, S = this.sunWay, P = shape.pts, n = P.length;
    if ((((shape.area / (ppm * ppm)) * S.L * f * f * e) / (z * z * z)) * this.shadeK < 0.04) return null;      // (its area on the stage, times its strength: under a 25th of a pixel)
    const pts = new Float32Array(n * 4);
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (let i = 0; i < n; i++) {
      const Y = P[i][0] / ppm, hw = P[i][1] / ppm / 2, bz = z + S.dz * Y, bX = X + S.dX * Y;
      if (bz < 0.25) return null;                                    // (beside the camera: never in a pane)
      const zz2 = bz * bz, Az = -(sd * f * bX) / zz2, Ay = -(f * e) / zz2, Bx = (sd * f) / bz;            // d(x, y)/dz = (Az, Ay); d(x, y)/dX = (Bx, 0)
      const mx = this.vx + (sd * f * bX) / bz, my = this.hz + (f * e) / bz;                                // the band's middle here, on the stage
      const lx = S.dz * Az + S.dX * Bx, ly = S.dz * Ay, ll = Math.hypot(lx, ly) || 1, ux = lx / ll, uy = ly / ll;   // the way it runs there
      const ax = S.az * Az + S.aX * Bx, ay = S.az * Ay, along = (ax * ux + ay * uy) * hw, across = ax * -uy + ay * ux;   // a metre across it, there
      // Never thinner on the stage than 10 cm seen face on at its distance (shadeFace), up to a pixel and a half (shadeMin): a
      // fence post's shadow seen from 1.8 m up is about half a pixel, and as a shade spread over two rows of the streaking
      // ground it would not be seen; at a pixel and a half some row is always at least three quarters in it. So near the car
      // (within some 23 m in the limousine) a shadow is a pixel and a half at least; farther off the least falls as the things
      // themselves grow smaller, not as fast as the ground's foreshortening would have it (a far telephone pole's long
      // shadow a faint line, not a dark one). Thickened across the way it runs on the stage, not along it.
      const least = Math.min(this.shadeMin, (this.shadeFace * f) / bz) / 2;
      const half = Math.max(Math.abs(across) * hw, least) * (across < 0 ? -1 : 1), ox = along * ux - half * uy, oy = along * uy + half * ux;
      for (let q = 0; q < 2; q++) {                                  // its two sides: one going out from the foot, the other back
        const k = q ? 2 * n - 1 - i : i, px = q ? mx + ox : mx - ox, py = q ? my + oy : my - oy;
        pts[k * 2] = px; pts[k * 2 + 1] = py;
        if (px < x0) x0 = px; if (px > x1) x1 = px; if (py < y0) y0 = py; if (py > y1) y1 = py;
      }
    }
    return { pts, x0, y0, x1, y1 };
  }
  /** DRIVE-16F: the shadows of the things that fall in a pane, laid on its ground before the things are drawn: one shape (far
      to near, all turning the same way, so where two overlap the ground is shaded once), the ground multiplied by `shade`
      at `shade_k`. -> how many. */
  shadows(ctx, w, s) {
    if (!this.rows.length && !(this.pieces && this.pieces.size)) return 0;      // (ROAD-18E: or set pieces)
    const items = this.sights(s), [bx, by, bx1, by1] = w.box;
    let n = 0;
    ctx.save();
    ctx.translate(-bx, -by);
    ctx.beginPath();
    for (const it of items) {
      const sh = it.shadow;
      if (!sh || sh.x0 > bx1 || sh.x1 < bx || sh.y0 > by1 || sh.y1 < by) continue;
      const p = sh.pts;
      ctx.moveTo(p[0], p[1]);
      for (let i = 2; i < p.length; i += 2) ctx.lineTo(p[i], p[i + 1]);
      ctx.closePath();
      n++;
    }
    if (n) { ctx.globalCompositeOperation = "multiply"; ctx.fillStyle = rgba(this.shade, this.shadeK); ctx.fill("nonzero"); }
    ctx.restore();
    return n;
  }
  /** The things and wires that fall in a pane, drawn over its ground and bands, far to near. */
  things(ctx, w, s) {
    if (!this.rows.length) return 0;
    const items = this.sights(s), [bx, by, bx1, by1] = w.box;
    let n = 0;
    ctx.save();
    ctx.translate(-bx, -by);
    ctx.lineWidth = 1; ctx.lineCap = "round";
    for (const it of items) {
      if (it.wire) {
        const p = it.pts;
        let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
        for (let i = 0; i < p.length; i += 2) { x0 = Math.min(x0, p[i]); x1 = Math.max(x1, p[i]); y0 = Math.min(y0, p[i + 1]); y1 = Math.max(y1, p[i + 1]); }
        if (x1 < bx || x0 > bx1 || y1 < by || y0 > by1) continue;
        ctx.strokeStyle = rgba(this.wire, it.alpha);
        ctx.beginPath(); ctx.moveTo(p[0], p[1]);
        for (let i = 2; i < p.length; i += 2) ctx.lineTo(p[i], p[i + 1]);
        ctx.stroke();
        n++;
        continue;
      }
      const lv = it.lv, dw = lv.w * it.rel, dh = lv.h * it.rel, x = it.x - lv.fx * it.rel, y = it.y - lv.fy * it.rel;
      if (x > bx1 || x + dw < bx || y > by1 || y + dh < by) continue;
      ctx.imageSmoothingEnabled = !it.hard;
      ctx.drawImage(lv.canvas, x, y, dw, dh);
      n++;
    }
    ctx.restore();
    return n;
  }

  // ---------------------------------------------------------------- ROAD-18E: the view straight ahead (side: "ahead")
  /** ROAD-18E: what a drive straight ahead reads of its description beyond what every drive does (see the top). */
  setupAhead(s, path) {
    this.strips = (Array.isArray(s.grounds) ? s.grounds : s.ground && typeof s.ground === "object" ? [s.ground] : [])
      .filter((g) => g && typeof g.src === "string")
      .map((g) => ({ src: path(g.src), ppm: Math.max(1e-3, num(g.ppm, 16)), from: num(g.from, 0), to: num(g.to, null) }));
    this.ground = null;                                              // (its strips are its ground: `ground`, one strip, is the first of them)
    if (this.bands.length) { warnDrive(this, "looks straight ahead: `bands` are a side view's, and are left out (the far land is the backdrop's)"); this.bands = []; }
    this.far = Math.max(1, num(s.far, 2000));                        // the ground is drawn no farther off than this (metres): beyond, the backdrop shows
    this.thingsFar = Math.max(10, num(s.things_far, num(s.thingsFar, 1500)));      // nor any thing
    this.hazeInto = s.haze === "backdrop";                           // the ground fades into the backdrop's own far land, not into a colour
    this.lights = lightsOf(s, path);
    this.gaps = gapsOf(s.gap);
    this.pieces = new Map();
    this.ver = 0;                                                    // how many times what it draws has been changed by a script (a piece, a light, a gap)
    for (const p of Array.isArray(s.pieces) ? s.pieces : []) if (p && typeof p.id === "string" && typeof p.sprite === "string") this.pieces.set(p.id, { sprite: p.sprite, X: num(p.X, 0), s: num(p.s, 0), Y: num(p.Y, 0) });      // (set pieces from the start)
  }
  /** ROAD-18E: a row of things seen straight ahead. `at` is across the road (negative on the left): two numbers of opposite
      signs are two places, each thing of the row standing at both (reflector posts either side of the road), any other pair a
      range as on a side; `both: true` puts each thing on one side or the other at random (seeded), `at` then how far out;
      `gap`, the row's own stretches kept clear (false: none, whatever the drive's `gap` says). */
  aheadRow(r, row) {
    if (!this.ahead) return row;
    const pair = isPair(r.at) && r.at[0] * r.at[1] < 0 ? [Math.min(...r.at), Math.max(...r.at)] : null, both = !pair && !!r.both;
    const out = (v) => (isPair(v) ? [Math.min(Math.abs(v[0]), Math.abs(v[1])), Math.max(Math.abs(v[0]), Math.abs(v[1]))] : Math.abs(v));
    return Object.assign(row, { pair, both, at: both ? out(row.at) : row.at, gap: r.gap === false ? [] : r.gap !== undefined ? gapsOf(r.gap) : null });
  }
  /** ROAD-18E: where thing i of a row stands across the road: [[thing, X, which], ...] (two for a pair). */
  placesAhead(row, i) {
    const t = this.thing(row, i);
    if (row.pair) return [[t, row.pair[0], "L"], [t, row.pair[1], "R"]];
    if (!row.both) return [[t, t.X, ""]];
    const k = row.n ? ((i % row.n) + row.n) % row.n : i;
    return [[t, rnd(row.seed, k, 4) < 0.5 ? -t.X : t.X, ""]];
  }
  /** ROAD-18E, for scripts: a set piece, a thing of the sheet put by name at a place of the road: `sprite`; `X` metres across
      (negative on the left); `s` metres along the road from where the drive began, so that it stays where it is as the camera
      comes on (it is s - (the drive's s) ahead); `Y` metres up (0: on the ground; one off the ground throws no shadow). Placed
      again with only some of these, it keeps the rest: place("sign", { sprite: "sign-bc" }) changes its picture. -> the drive */
  place(id, o = {}) {
    if (!this.pieces) return this;
    const was = this.pieces.get(id) || { sprite: null, X: 0, s: 0, Y: 0 };
    const p = { sprite: typeof o.sprite === "string" ? o.sprite : was.sprite, X: num(o.X, was.X), s: num(o.s, was.s), Y: num(o.Y, was.Y) };
    if (!p.sprite) { warnDrive(this, `was asked to place "${id}" with no sprite`); return this; }
    this.pieces.set(id, p);
    this.changed();
    return this;
  }
  /** ROAD-18E, for scripts: take a set piece away. */
  remove(id) { if (this.pieces && this.pieces.delete(id)) this.changed(); return this; }
  /** ROAD-18E: something it draws has been changed by a script: its panes are drawn again in their turn, parked or not. */
  changed() { this.ver++; this.world = null; if (this.host && this.host.frame && this.wins) this.host.frame(0); }
  /** ROAD-18E: set({ s }) puts it s metres along the road, parked (a script's tween carries it there, and it lands exactly);
      set({ s, speed }) and it goes on from there at that speed. set({ light: { id: k } }): a light's opacity. set({ gap }): the
      stretches kept clear of the rows' things. */
  setAhead(o) {
    if (typeof o.s === "number" && Number.isFinite(o.s)) { this.d0 = o.s; this.t0 = this.time; this.speed = typeof o.speed === "number" && Number.isFinite(o.speed) ? o.speed : 0; }
    if (o.light && typeof o.light === "object") {
      for (const [id, k] of Object.entries(o.light)) { const l = this.lights.find((v) => v.id === id); if (l && typeof k === "number" && clamp(k) !== l.opacity) { l.opacity = clamp(k); this.changed(); } }
    }
    if (o.gap !== undefined) { this.gaps = gapsOf(o.gap); this.changed(); }
  }
  /** ROAD-18E: metres gone now (for scripts: where the camera is along the road; set({ s }) puts it somewhere). */
  get s() { return this.gone(this.time); }
  /** ROAD-18E: is a pane's picture out of date though the camera has not moved? What it draws has been changed, or it was
      drawn streaked by a script's move that has now stopped (parked, it is drawn again, sharp). */
  stale(w, s) { return w.ver !== this.ver || (s === w.s && w.travel > 0 && !this.speed); }
  /** ROAD-18E: a pane straight ahead (the whole stage, unless `windows` or `clip` say): its picture, its place, its shape (a
      pixel is in it when its middle is; a rectangle that fills its box needs no mask), and for each column the directions its
      edges look in (u from the vanishing point, negative on the left). */
  frameAhead(win) {
    const [x0, y0, x1, y1] = boxOf(win.poly), box = [Math.max(0, Math.floor(x0)), Math.max(0, Math.floor(y0)), Math.min(W, Math.ceil(x1)), Math.min(H, Math.ceil(y1))];
    const w = Math.max(1, box[2] - box[0]), h = Math.max(1, box[3] - box[1]);
    Object.assign(win, { box, w, h, pair: new Pair(w, h), inside: new Uint8Array(w * h), rowA: new Int32Array(h).fill(-1), rowB: new Int32Array(h), colA: new Int32Array(w).fill(-1), colB: new Int32Array(w), ver: 0, travel: 0, moved: 0 });
    win.full = win.poly.length === 4 && win.poly.every(([px, py]) => (px === box[0] || px === box[2]) && (py === box[1] || py === box[3]));
    if (win.full) { win.inside.fill(1); win.rowA.fill(0); win.rowB.fill(w); win.colA.fill(0); win.colB.fill(h); }
    else {
      win.mask = canvasOf(w, h);
      const img = win.mask.getContext("2d").createImageData(w, h), d = img.data;
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        if (!inside(win.poly, box[0] + x + 0.5, box[1] + y + 0.5)) continue;
        win.inside[y * w + x] = 1; d[(y * w + x) * 4 + 3] = 255;
        if (win.rowA[y] < 0) win.rowA[y] = x;
        win.rowB[y] = x + 1;
        if (win.colA[x] < 0) win.colA[x] = y;
        win.colB[x] = y + 1;
      }
      win.mask.getContext("2d").putImageData(img, 0, 0);
    }
    win.U0 = new Float32Array(w); win.U1 = new Float32Array(w);
    for (let x = 0; x < w; x++) { win.U0[x] = box[0] + x - this.vx; win.U1[x] = win.U0[x] + 1; }
    win.out = new ImageData(w, h); win.out32 = new Uint32Array(win.out.data.buffer);
    win.sprite.place(box[0], box[1]);
  }
  /** ROAD-18E: the strips' tables (their sums along the road, made once a picture), each strip's place across the road, left
      to right, and room for a row's samples. */
  stripsHere(got_) {
    const list = this.strips.map((g) => {
      const tab = driveTables(got_(g.src), "strip", stripSums), to = g.to != null ? g.to : g.from + tab.h / g.ppm;
      const X0 = Math.min(g.from, to), X1 = Math.max(g.from, to);
      if (Math.abs((X1 - X0) * g.ppm - tab.h) > 1.5) warnDrive(this, `has a strip of ground (${g.src}) of ${tab.h} rows for ${(X1 - X0).toFixed(2)} m across at ${g.ppm} pixels a metre: its rows are spread from \`from\` to \`to\``);
      return { tab, X0, X1, ppm: g.ppm, ppmX: tab.h / Math.max(1e-6, X1 - X0), rev: g.from > to, src: g.src, cut: null };
    }).sort((a, b) => a.X0 - b.X0);
    for (let i = 1; i < list.length; i++) if (list[i].X0 < list[i - 1].X1 - 1e-6) { warnDrive(this, `has strips of ground that overlap (${list[i - 1].src} and ${list[i].src}): the second begins where the first ends`); list[i].cut = list[i - 1].X1; }
    const most = list.reduce((n, g) => n + g.tab.h, 0) + 4 * list.length + 8;
    return { list, SR: new Float64Array(most * 3), PT: list.map(() => new Float64Array(8)) };
  }
  /**
   * ROAD-18E: what a pane's ground straight ahead sees that never changes: each row of it below the horizon and nearer than
   * `far` is one depth (from zBot, its lower edge, to zTop, its upper edge); a pixel of it covers (x - vanish x) * d to
   * (x + 1 - vanish x) * d metres across the road (d = z / focal, at the row's middle depth); so the pieces across the row it
   * needs are known once: the ground past the leftmost strip, each strip's samples (its rows) from the first a pixel touches to
   * the last, any gap between two strips, the ground past the rightmost (SX: where each begins, in metres across; `runs`: for
   * each strip [strip, first piece, first sample, end]; `gaps`: [strip, piece]). And the haze over each pixel, as far off as
   * its middle (along the ground: z * sqrt(1 + (u / focal)^2)). `top`: the pane's first row of ground.
   */
  planAhead(w) {
    const f = this.focal, e = this.eye, bx = w.box[0], by = w.box[1], rows = [], HZ = w.hazeK || (w.hazeK = new Float32Array(w.w * w.h));
    const list = this.tabs.strips.list, nl = list.length;
    let top = w.h;
    for (let j = 0; j < w.h; j++) {
      const v0 = by + j - this.hz;
      if (!nl || w.rowA[j] < 0 || v0 + 0.5 <= 0) continue;
      const zc = (f * e) / (v0 + 0.5);
      if (zc > this.far) continue;
      const d = zc / f, xA = w.rowA[j], xB = w.rowB[j], mA = (bx + xA - this.vx) * d, mB = (bx + xB - this.vx) * d;
      const SX = [Math.min(mA, list[0].X0) - 1], runs = [], gaps = [];
      for (let q = 0; q < nl; q++) {
        const st = list[q];
        if (q > 0 && st.X0 > list[q - 1].X1 + 1e-6) { gaps.push([q, SX.length]); SX.push(Math.max(list[q - 1].X1, SX[SX.length - 1])); }      // (a gap between two strips)
        let kA = Math.max(0, Math.floor((mA - st.X0) * st.ppmX));
        const kB = Math.min(st.tab.h, Math.ceil((mB - st.X0) * st.ppmX));
        if (st.cut != null) kA = Math.max(kA, Math.floor((st.cut - st.X0) * st.ppmX));
        if (kA >= kB) continue;
        runs.push([q, SX.length, kA, kB]);
        for (let k = kA; k < kB; k++) SX.push(Math.max(st.X0 + k / st.ppmX, st.cut != null ? st.cut : -Infinity));
      }
      SX.push(Math.max(list[nl - 1].X1, SX[SX.length - 1]), Infinity);
      rows.push({ j, xA, xB, zBot: (f * e) / (v0 + 1), zTop: v0 > 0 ? (f * e) / v0 : Infinity, d, inv: 1 / d, mA, SX: Float64Array.from(SX), runs, gaps, right: SX.length - 2 });
      if (j < top) top = j;
      for (let x = xA; x < xB; x++) { const u = bx + x + 0.5 - this.vx; HZ[j * w.w + x] = 1 - Math.exp((-Math.LN2 * zc * Math.sqrt(1 + (u / f) ** 2)) / this.hazeFar); }
    }
    return { rows, top };
  }
  /** ROAD-18E: the colour of a strip's first rows (which 0) or last rows (1) along a row's patch (t: its weights), into SR at `at`. */
  edgeAhead(st, t, which, SR, at) {
    const tab = st.tab, F = which ? tab.F : tab.F0, ft = tab.w * 3;
    if (t[6]) { for (let c = 0; c < 3; c++) SR[at + c] = F[ft + c] / tab.w; return; }      // (the row at the horizon: the whole loop)
    const mH = t[0] * 3, fH = t[1], mL = t[2] * 3, fL = t[3], loops = t[4], il = t[5];
    for (let c = 0; c < 3; c++) SR[at + c] = (F[mH + c] * (1 - fH) + F[mH + 3 + c] * fH + loops * F[ft + c] - F[mL + c] * (1 - fL) - F[mL + 3 + c] * fL) * il;
  }
  /**
   * ROAD-18E: the ground straight ahead, into the pane's pixels. A row of the stage below the horizon is one depth, so its
   * patch of road (from zBot to zTop ahead, the camera s metres along; longer by the streak) is the same for every pixel of
   * it: each sample across the road (a row of a strip's picture) is averaged along that patch once, from the strip's sums
   * (SR), and each pixel is the average of the pieces across the stretch it covers (the plan's), left to right: a pixel inside
   * one sample shows it, hard; one that straddles two takes a share of each; one larger, their average. Past the outermost
   * strips, their outer rows' colour; between two strips that do not meet, the mean of their edges. Then the haze, as far off
   * as the pixel's middle: into its colour, or (`haze: "backdrop"`) into clear, so that the backdrop's own far land shows.
   */
  baseAhead(w, s, travel) {
    const T = this.tabs.strips, list = T.list, nl = list.length, SR = T.SR, PT = T.PT, out = w.out32, ins = w.full ? null : w.inside, HZ = w.hazeK;
    const pw = w.w, into = this.hazeInto, hr = this.haze[0], hg = this.haze[1], hb = this.haze[2];
    for (const row of w.plan.rows) {
      const { j, xA, xB, zBot, zTop, d, inv, SX } = row, o = j * pw, endless = zTop === Infinity;
      const ext = !endless && travel > zTop - zBot ? (travel - (zTop - zBot)) / 2 : 0;      // (the streak: a row that goes by faster than it is long)
      for (let q = 0; q < nl; q++) {                                 // each strip's patch along the road, in its own columns: the weights that read its sums
        const st = list[q], gw = st.tab.w, t = PT[q];
        if (endless) { t[6] = 1; continue; }
        const lo = (zBot + s - ext) * st.ppm, hi = (zTop + s + ext) * st.ppm, iH = Math.floor(hi), iL = Math.floor(lo), mH = ((iH % gw) + gw) % gw, mL = ((iL % gw) + gw) % gw;
        t[0] = mH; t[1] = hi - iH; t[2] = mL; t[3] = lo - iL; t[4] = (iH - mH) / gw - (iL - mL) / gw; t[5] = 1 / Math.max(1e-6, hi - lo); t[6] = 0;
      }
      // the colours of the row's pieces: past the leftmost strip; any gap (the mean of its two edges); each strip's samples; past the rightmost
      this.edgeAhead(list[0], PT[0], list[0].rev ? 1 : 0, SR, 0);
      for (const [q, n0] of row.gaps) {
        const a = list[q - 1], b = list[q], n3 = n0 * 3;
        this.edgeAhead(a, PT[q - 1], a.rev ? 0 : 1, SR, n3); this.edgeAhead(b, PT[q], b.rev ? 1 : 0, SR, n3 + 3);
        for (let c = 0; c < 3; c++) SR[n3 + c] = (SR[n3 + c] + SR[n3 + 3 + c]) / 2;
      }
      for (const [q, n0, kA, kB] of row.runs) {
        const st = list[q], tab = st.tab, gh = tab.h, P = tab.P, t = PT[q], tot = tab.w * gh * 3, inc = st.rev ? -3 : 3, end = (n0 + kB - kA) * 3;
        let b3 = (st.rev ? gh - 1 - kA : kA) * 3, n3 = n0 * 3;
        if (t[6]) { const iw = 1 / tab.w; for (; n3 < end; n3 += 3, b3 += inc) { SR[n3] = P[tot + b3] * iw; SR[n3 + 1] = P[tot + b3 + 1] * iw; SR[n3 + 2] = P[tot + b3 + 2] * iw; } continue; }
        const il = t[5], gH = (1 - t[1]) * il, fH = t[1] * il, gL = (1 - t[3]) * il, fL = t[3] * il, li = t[4] * il;
        const h0 = t[0] * gh * 3, h1 = h0 + gh * 3, l0 = t[2] * gh * 3, l1 = l0 + gh * 3;
        if (!li) for (; n3 < end; n3 += 3, b3 += inc) {
          SR[n3] = P[h0 + b3] * gH + P[h1 + b3] * fH - P[l0 + b3] * gL - P[l1 + b3] * fL;
          SR[n3 + 1] = P[h0 + b3 + 1] * gH + P[h1 + b3 + 1] * fH - P[l0 + b3 + 1] * gL - P[l1 + b3 + 1] * fL;
          SR[n3 + 2] = P[h0 + b3 + 2] * gH + P[h1 + b3 + 2] * fH - P[l0 + b3 + 2] * gL - P[l1 + b3 + 2] * fL;
        } else for (; n3 < end; n3 += 3, b3 += inc) {                 // (a patch longer than the loop: whole loops in it too)
          SR[n3] = P[h0 + b3] * gH + P[h1 + b3] * fH - P[l0 + b3] * gL - P[l1 + b3] * fL + li * P[tot + b3];
          SR[n3 + 1] = P[h0 + b3 + 1] * gH + P[h1 + b3 + 1] * fH - P[l0 + b3 + 1] * gL - P[l1 + b3 + 1] * fL + li * P[tot + b3 + 1];
          SR[n3 + 2] = P[h0 + b3 + 2] * gH + P[h1 + b3 + 2] * fH - P[l0 + b3 + 2] * gL - P[l1 + b3 + 2] * fL + li * P[tot + b3 + 2];
        }
      }
      this.edgeAhead(list[nl - 1], PT[nl - 1], list[nl - 1].rev ? 0 : 1, SR, row.right * 3);
      // the pixels, left to right: each the average of the pieces across its stretch [m0, m1) (an average of numbers from 0 to 255:
      // no clamping needed)
      let k = 0, m0 = row.mA;
      while (SX[k + 1] <= m0) k++;
      for (let x = xA; x < xB; x++) {
        const m1 = m0 + d;
        let r, g, b, k3 = k * 3;
        if (m1 <= SX[k + 1]) { r = SR[k3]; g = SR[k3 + 1]; b = SR[k3 + 2]; }
        else {
          let wd = SX[k + 1] - m0; r = wd * SR[k3]; g = wd * SR[k3 + 1]; b = wd * SR[k3 + 2]; k++; k3 += 3;
          while (SX[k + 1] < m1) { wd = SX[k + 1] - SX[k]; r += wd * SR[k3]; g += wd * SR[k3 + 1]; b += wd * SR[k3 + 2]; k++; k3 += 3; }
          wd = m1 - SX[k]; r = (r + wd * SR[k3]) * inv; g = (g + wd * SR[k3 + 1]) * inv; b = (b + wd * SR[k3 + 2]) * inv;
        }
        m0 = m1;
        const i = o + x;
        if (ins && !ins[i]) continue;
        const hk = HZ[i];
        if (into) out[i] = ((((1 - hk) * 255 + 0.5) << 24) | ((b + 0.5) << 16) | ((g + 0.5) << 8) | (r + 0.5)) >>> 0;
        else { r += (hr - r) * hk; g += (hg - g) * hk; b += (hb - b) * hk; out[i] = 0xff000000 | ((b + 0.5) << 16) | ((g + 0.5) << 8) | (r + 0.5); }
      }
    }
  }
  /** ROAD-18E: the haze over a thing X across and z ahead (0 to 1), as over the ground there. */
  hazeAt(X, z) { return 1 - Math.exp((-Math.LN2 * Math.sqrt(z * z + X * X)) / this.hazeFar); }
  /** ROAD-18E: one thing as the camera sees it straight ahead: X across, z ahead, its foot Y up; at its sheet's pixels a metre
      (or its own); from a halved copy when smaller, hard when larger; at its own size (within a fifth of a percent) on whole
      pixels, pixel for pixel; hazed by its distance (drawn the less solid, the farther); on its shadow. Null when under a pixel. */
  sightAhead(sp, X, z, Y, key, name) {
    const f = this.focal, k = f / (z * sp.ppm), exact = Math.abs(k - 1) < 0.002;
    const L = k >= 1 || exact ? 0 : Math.min(sp.levels.length - 1, Math.floor(Math.log2(1 / k))), lv = sp.levels[L], rel = exact ? 1 : k * 2 ** L;
    if (lv.h * rel < 1) return null;
    return { z, wire: false, x: this.vx + (f * X) / z, y: this.hz + (f * (this.eye - Y)) / z, lv, rel, hard: k >= 1 || exact, exact, key, name, X, Y,
      alpha: 1 - this.airOf(sp, X, z), shadow: this.sunWay && sp.shape && !Y ? this.shadowAhead(sp.shape, X, z, sp.ppm) : null };
  }
  /** ROAD-18E: how much of the air lies over a thing of the sheet X across and z ahead (0 to 1): its `air` share of the haze
      there (1: all of it; the painter's poles 0.6, to stay dark against the sky); with `air` 0, a thing painted in its own air
      as it is seen from where it is drawn at its own size (focal / its ppm metres ahead: a set piece cut from the painting,
      where the camera stops), only the air beyond that: none there or nearer, and as it is seen from farther off it fades as
      the rest do. */
  airOf(sp, X, z) {
    const h = this.hazeAt(X, z);
    return sp.air > 0 ? sp.air * h : Math.max(0, 1 - (1 - h) / (1 - this.hazeAt(X, Math.min(z, this.focal / sp.ppm))));
  }
  /** ROAD-18E: the sheet's name for a thing called `name` standing X across: its own, or the side's own ("-l", "-r": sidesOf). */
  sideName(name, X) { const lr = this.tabs.lr; return (lr && (X < 0 ? lr.L : lr.R)[name]) || name; }
  /** ROAD-18E: the things, wires and set pieces seen straight ahead with the camera s metres along, far to near, once for each
      s (and each change a script makes). A row's things come from the seed, as on a side, on both sides of the road; those in
      a gap are left out (and the wires between them); a thing farther than `things_far`, under a pixel, nearer than 1.5 m,
      or off the panes is not drawn. */
  sightsAhead(s) {
    if (this.world && this.world.s === s && this.world.ver === this.ver) return this.world.items;
    const items = [], f = this.focal, sprites = this.tabs.sprites, near = 1.5, far = this.thingsFar, sw = this.sunWay;
    for (const [ri, row] of this.rows.entries()) {
      if (!row.reach) continue;                                      // (none of its pictures on the sheet: here())
      const { half, tall } = row.reach;
      const reach = half + (sw ? Math.abs(sw.dX) * tall : 0), zHi = Math.min(far, row.farAhead || far, (f * tall) / 0.5), gaps = row.gap || this.gaps;      // (ROAD-18M: and the row's own far)
      const iA = Math.floor((s + near - row.offset - row.jit) / row.cell) - 1, iB = Math.ceil((s + zHi - row.offset + row.jit) / row.cell) + 1;
      if (iB - iA > 4000) { warnDrive(this, `has a row of "${row.names[0]}" too close together to draw (every ${row.cell.toFixed(2)} m)`); continue; }
      const prev = {};
      for (let i = iA; i <= iB; i++) {
        for (const [t, X, side] of this.placesAhead(row, i)) {
          if (gaps.length && inGap(gaps, t.w)) { prev[side] = null; continue; }
          const z = t.w - s, here = { w: t.w, X };
          if (z >= near && z <= far) {
            const u = (f * X) / z, hw = (f * reach) / z, name = this.sideName(t.name, X), sp = sprites[name];
            if (sp && u + hw >= this.uMin && u - hw <= this.uMax) { const it = this.sightAhead(sp, X, z, 0, `${ri}:${i}${side}`, name); if (it) items.push(it); }
          }
          if (prev[side] && row.wires.length && Math.min(prev[side].w, t.w) - s <= far) {
            const n0 = items.length;
            this.wires(row, prev[side], here, s, items);
            for (let q = n0; q < items.length; q++) items[q].alpha *= 1 - this.hazeAt(X, Math.max(near, (prev[side].w + t.w) / 2 - s));
          }
          prev[side] = here;
        }
      }
    }
    for (const [id, p] of this.pieces) {
      const name = this.sideName(p.sprite, p.X), sp = sprites[name], z = p.s - s;
      if (!sp) { warnDrive(this, `has no picture called "${p.sprite}" on its sheet (the set piece "${id}")`); continue; }
      if (z < near || z > far) continue;
      const it = this.sightAhead(sp, p.X, z, p.Y, `piece:${id}`, name);
      if (it) items.push(it);
    }
    items.sort((a, b) => b.z - a.z);
    this.world = { s, ver: this.ver, items };
    return items;
  }
  /** ROAD-18E: a thing's shadow straight ahead: as shadowOf (DRIVE-16F) has it, at the thing's own pixels a metre, cut where it
      would come nearer than a metre ahead (the sun ahead throws it back toward the camera, and a long one runs past it). */
  shadowAhead(shape, X, z, ppm) {
    const f = this.focal, e = this.eye, S = this.sunWay;
    if ((((shape.area / (ppm * ppm)) * S.L * f * f * e) / (z * z * z)) * this.shadeK < 0.04) return null;
    let P = shape.pts;
    if (S.dz < 0) {
      const top = ((z - 1) / -S.dz) * ppm;                           // (sheet pixels: the height whose shadow lies a metre ahead)
      if (top <= 0) return null;
      if (P[P.length - 1][0] > top) { const k = P.findIndex((v) => v[0] > top), a = P[k - 1], b = P[k], t = (top - a[0]) / (b[0] - a[0]); P = [...P.slice(0, k), [top, a[1] + (b[1] - a[1]) * t]]; }
    }
    const n = P.length, pts = new Float32Array(n * 4);
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (let i = 0; i < n; i++) {
      const Y = P[i][0] / ppm, hw = P[i][1] / ppm / 2, bz = z + S.dz * Y, bX = X + S.dX * Y;
      if (bz < 0.25) return null;
      const zz2 = bz * bz, Az = -(f * bX) / zz2, Ay = -(f * e) / zz2, Bx = f / bz;
      const mx = this.vx + (f * bX) / bz, my = this.hz + (f * e) / bz;
      const lx = S.dz * Az + S.dX * Bx, ly = S.dz * Ay, ll = Math.hypot(lx, ly) || 1, ux = lx / ll, uy = ly / ll;
      const ax = S.az * Az + S.aX * Bx, ay = S.az * Ay, along = (ax * ux + ay * uy) * hw, across = ax * -uy + ay * ux;
      const least = Math.min(this.shadeMin, (this.shadeFace * f) / bz) / 2;
      const half = Math.max(Math.abs(across) * hw, least) * (across < 0 ? -1 : 1), ox = along * ux - half * uy, oy = along * uy + half * ux;
      for (let q = 0; q < 2; q++) {
        const k = q ? 2 * n - 1 - i : i, px = q ? mx + ox : mx - ox, py = q ? my + oy : my - oy;
        pts[k * 2] = px; pts[k * 2 + 1] = py;
        if (px < x0) x0 = px; if (px > x1) x1 = px; if (py < y0) y0 = py; if (py > y1) y1 = py;
      }
    }
    return { pts, x0, y0, x1, y1 };
  }
  /** ROAD-18E: the lights over the ground (`light`), each at its opacity and in its blend, still on the stage. -> how many. */
  light(ctx, w) {
    let n = 0;
    for (const L of this.lights) {
      if (!(L.opacity > 0)) continue;
      ctx.save();
      ctx.translate(-w.box[0], -w.box[1]); ctx.globalAlpha = L.opacity; ctx.globalCompositeOperation = L.blend;
      if (L.src) { const img = got(L.src); if (img) ctx.drawImage(img, L.x, L.y); }
      else {
        ctx.beginPath(); L.poly.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.closePath();
        let paint = L.paints.get(ctx);
        if (!paint) {
          const stops = L.stops.length ? L.stops : [[0, L.color, 1]];
          if (L.radial) paint = ctx.createRadialGradient(0, 0, 0, 0, 0, Math.max(1e-3, L.radial.r[0]));
          else if (L.linear) paint = ctx.createLinearGradient(L.linear.from[0], L.linear.from[1], L.linear.to[0], L.linear.to[1]);
          if (paint) for (const [o, c, a] of stops) paint.addColorStop(o, rgba(c, a)); else paint = rgba(stops[0][1], stops[0][2]);
          L.paints.set(ctx, paint);
        }
        ctx.fillStyle = paint;
        if (L.radial) { const [cx, cy] = L.radial.at, [rx, ry] = L.radial.r; ctx.translate(cx, cy); ctx.scale(1, ry / Math.max(1e-3, rx)); }      // (an ellipse: the gradient's own space; the shape was laid down before)
        ctx.fill();
      }
      ctx.restore();
      n++;
    }
    return n;
  }
  /** ROAD-18E: the things and wires straight ahead, far to near. -> how many. */
  thingsAhead(ctx, w, s) {
    const items = this.sightsAhead(s), [bx, by, bx1, by1] = w.box;
    let n = 0;
    ctx.save();
    ctx.translate(-bx, -by);
    ctx.lineWidth = 1; ctx.lineCap = "round";
    for (const it of items) {
      if (it.wire) {
        const p = it.pts;
        let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
        for (let i = 0; i < p.length; i += 2) { x0 = Math.min(x0, p[i]); x1 = Math.max(x1, p[i]); y0 = Math.min(y0, p[i + 1]); y1 = Math.max(y1, p[i + 1]); }
        if (x1 < bx || x0 > bx1 || y1 < by || y0 > by1 || !(it.alpha > 0.01)) continue;
        ctx.globalAlpha = 1; ctx.strokeStyle = rgba(this.wire, it.alpha);
        ctx.beginPath(); ctx.moveTo(p[0], p[1]);
        for (let i = 2; i < p.length; i += 2) ctx.lineTo(p[i], p[i + 1]);
        ctx.stroke();
        n++;
        continue;
      }
      if (this.drawSight(ctx, it, 1, bx, by, bx1, by1)) n++;
    }
    ctx.restore();
    return n;
  }
  /** ROAD-18E: one thing (a sight) onto a canvas whose corner is (bx, by) on the stage (the caller has moved it there), at
      `alpha` of its own solidity; nothing if it lies outside [bx, by, bx1, by1). -> whether it was drawn. */
  drawSight(ctx, it, alpha, bx, by, bx1, by1) {
    const lv = it.lv;
    let x, y, dw, dh;
    if (it.exact) { dw = lv.w; dh = lv.h; x = Math.round(it.x - lv.fx); y = Math.round(it.y - lv.fy); }
    else { dw = lv.w * it.rel; dh = lv.h * it.rel; x = it.x - lv.fx * it.rel; y = it.y - lv.fy * it.rel; }
    const a = it.alpha * alpha;
    if (x > bx1 || x + dw < bx || y > by1 || y + dh < by || !(a > 0.004)) return false;
    ctx.globalAlpha = a; ctx.imageSmoothingEnabled = !it.hard;
    ctx.drawImage(lv.canvas, x, y, dw, dh);
    return true;
  }
  /** ROAD-18E: on a frame of the game that draws no picture of it (at 30 pictures a second, every other frame), the ground
      of its next picture is worked out ahead of time while it goes at its own speed (where it will be at its next step is
      known), so that the frame that draws that picture does some half the work. Used only if it is then where it was foreseen,
      as it was foreseen (a script carrying it wastes it, no more: it is worked out again then). */
  prepare(w, step, calm) {
    if (!this.speed || !this.tabs.strips.list.length) return;
    const s = this.at(step + 1), travel = calm ? 0 : this.streak * Math.min(Math.abs(this.speed) / this.fps, 4);
    const nx = w.next || (w.next = { s: null, travel: null, out: new ImageData(w.w, w.h) });
    if (nx.s === s && nx.travel === travel) return;
    if (!nx.out32 || nx.out32.buffer !== nx.out.data.buffer) nx.out32 = new Uint32Array(nx.out.data.buffer);
    const out = w.out, out32 = w.out32;
    w.out = nx.out; w.out32 = nx.out32;
    try { this.baseAhead(w, s, travel); } finally { w.out = out; w.out32 = out32; }
    nx.s = s; nx.travel = travel;
  }
  /** ROAD-18E: a pane's picture straight ahead: the sky (if it has one) over the rows the ground does not reach; the ground;
      the things' shadows on it; the lights over it; the things and wires, far to near; cut to the pane (and its opacity). */
  paintAhead(w, s, calm) {
    const per = this.speed ? Math.abs(this.speed) / this.fps : w.moved || 0;          // metres it goes a picture: at its speed, or as a script carries it
    const travel = calm ? 0 : this.streak * Math.min(per, 4);
    w.travel = travel; w.ver = this.ver;
    const strips = this.tabs.strips.list.length, plan = w.plan || (w.plan = this.planAhead(w)), top = strips ? plan.top : w.h, nx = w.next;
    if (strips && nx && nx.s === s && nx.travel === travel) {        // (its ground worked out ahead of time, on the frame before: prepare)
      const o = w.out, o32 = w.out32; w.out = nx.out; w.out32 = nx.out32; nx.out = o; nx.out32 = o32; nx.s = null;
    } else if (strips) this.baseAhead(w, s, travel);
    const ctx = w.pair.next(), sky = this.skySrc && got(this.skySrc);
    if (sky && top > 0) ctx.drawImage(sky, w.box[0], w.box[1], w.w, top, 0, 0, w.w, top);
    if (strips && top < w.h) ctx.putImageData(w.out, 0, 0, 0, top, w.w, w.h - top);
    w.shadows = this.sun ? this.shadows(ctx, w, s) : 0;
    w.lit = this.light(ctx, w);
    w.things = this.thingsAhead(ctx, w, s);
    if (!w.full || this.alpha < 1) {
      ctx.globalCompositeOperation = "destination-in"; ctx.globalAlpha = this.alpha;
      if (w.full) { ctx.fillStyle = "#000"; ctx.fillRect(0, 0, w.w, w.h); } else ctx.drawImage(w.mask, 0, 0);
      ctx.globalAlpha = 1; ctx.globalCompositeOperation = "source-over";
    }
    this.drawn = this.wins.reduce((sum, v) => sum + 1 + (v.things || 0), 0);
  }
  /** ROAD-18E: for a door in time that bends what this drive draws (its `under`: { fx: id }, or { fx: id, piece, sprite,
      alpha }): its panes' pictures as they are now, or one set piece as it stands now (as another picture of the sheet, if
      `sprite` says; at `alpha`), drawn onto the door's canvas, whose corner is (x0, y0) on the stage. False while it has no
      picture yet (the door waits); a piece it has not got draws nothing. */
  under(ctx, x0, y0, u) {
    if (u.piece != null) {
      const p = this.pieces && this.pieces.get(u.piece), w = this.wins[0], sp = p && this.tabs && this.tabs.sprites[this.sideName(typeof u.sprite === "string" ? u.sprite : p.sprite, p.X)];
      if (!p || !sp || w.s == null) return true;
      const it = this.sightAhead(sp, p.X, p.s - w.s, p.Y, "", "");
      if (!it) return true;
      ctx.save(); ctx.translate(-x0, -y0);
      this.drawSight(ctx, it, clamp(num(u.alpha, 1)), -Infinity, -Infinity, Infinity, Infinity);
      ctx.restore();
      return true;
    }
    let any = false;
    for (const w of this.wins) if (w.step !== null) { ctx.drawImage(w.pair.canvas, w.box[0] - x0, w.box[1] - y0); any = true; }
    return any;
  }
}
const warnedDrive = new Set();
function warnDrive(e, text) { const k = `${e.id}|${text}`; if (!warnedDrive.has(k)) { warnedDrive.add(k); console.warn(`The drive "${e.id}" (${e.host.place || "added by a script"}) ${text}.`); } }

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
 *                sign comes out of the rings saying something else: highway.js). ROAD-18E: or a moving thing's
 *                pictures, { fx: id } (a drive: the road going by under the hole), read again, in its box only, each
 *                time it draws a new picture (once when it is parked), so the far road bends as it goes by; or one of
 *                its set pieces, { fx: id, piece, sprite, alpha }, as it stands now, drawn as another picture of the
 *                sheet if `sprite` says (the sign's rings bring through the drive's own `sign-bc`)
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
    this.fxUnder = this.under.some((u) => u && typeof u.fx === "string");     // ROAD-18E: a moving thing under it (a drive): read again each time it draws a new picture
    this.gens = new Map();                                                     // (ROAD-18E: which of its pictures was read)
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
    const tmp = this.tmp || (this.tmp = canvasOf(fw, fh)), ctx = tmp.getContext("2d", { willReadFrequently: true });      // (ROAD-18E: kept, as a door over a drive reads its paint thirty times a second)
    ctx.globalAlpha = 1; ctx.globalCompositeOperation = "source-over"; ctx.clearRect(0, 0, fw, fh);                      // (ROAD-18E)
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(view.backdrop, fx0, fy0, fw, fh, 0, 0, fw, fh);
    if (!this.painted) {                                                            // ROAD-18F: the probe once: paint in its box stays painted (a scene's backdrop only gains paint, and a new scene drops its doors), so a door over a drive, reading thirty times a second, reads its pixels back once a read, not twice
      const paint = ctx.getImageData(0, 0, fw, fh).data;                          // (nothing painted yet? then not yet: the picture comes in its own time)
      let painted = false;
      for (let i = 3; i < paint.length; i += 4) if (paint[i] > 0) { painted = true; break; }
      if (!painted) return false;
      this.painted = true;
    }
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
      } else if (u && typeof u.fx === "string") {                            // ROAD-18E: a moving thing's pictures (a drive's), or one of its set pieces
        const e = this.host.get(u.fx);
        if (!e || typeof e.under !== "function") continue;
        if (!e.under(ctx, fx0, fy0, u)) return false;
        this.gens.set(u.fx, e.gen || 0);
      }
    }
    this.src = ctx.getImageData(0, 0, fw, fh).data;
    return true;
  }
  /** ROAD-18E: has a moving thing it bends (`under`: { fx }) drawn a new picture since the paint was read? Then the paint is
      read again, and the door drawn over it, in the same frame: the far road bends as it goes by. Parked, it is read once. */
  moved() {
    for (const u of this.under) if (u && typeof u.fx === "string") { const e = this.host.get(u.fx); if (e && (e.gen || 0) !== this.gens.get(u.fx)) return true; }
    return false;
  }
  picture(sprite, calm) {
    if (this.openK <= 0) return null;
    const moved = this.fxUnder && !!this.src && this.moved();               // ROAD-18E: what it bends has moved on
    if (moved) this.src = null;
    if (!this.src && !this.read()) return null;                             // (the backdrop is not painted yet: next frame)
    const fps = calm ? this.calmFps : this.fps, step = Math.floor((this.time * fps) / 1000), go = this.go;
    this.go = false;
    if (this.step === null || moved || (go && (this.dirty || step !== this.step || calm !== this.drawnCalm))) {    // (the first picture at once; after that, in its turn. ROAD-18E: or what it bends has moved on)
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

const KINDS = { smoke: Smoke, flame: Flame, embers: Embers, ripples: Ripples, stream: Stream, shimmer: Shimmer, birds: Birds, sway: Sway, portal: Portal, strip: Strip };      // (strip: NEVADA-12E)
KINDS.bob = Bob;                                 // ROME-13E: a cut-out that rides the water
KINDS.drive = Drive;                             // DRIVE-16E: the world going by a car's side windows

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
    return Promise.all([...this.list.flatMap((e) => e.pics()).map(fetchPicture), ...this.list.map((e) => (e.ready ? e.ready() : null))]);          // (NEVADA-12E: pics(), which a strip has too; DRIVE-16E: and ready(), a drive's sheet of things)
  }
  drop(scene = null) { for (const e of this.list) if (e.end) e.end(); this.list = []; this.time = 0; this.owner = scene; this.scene = scene; this.place = scene ? scene.id : ""; this.granted = this.deferred = 0; }      // (ROME-13E: end(): a herd or a pose a script waits for is over)

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
    if (!quiet) { e.pics().forEach(fetchPicture); this.frame(0); }          // (NEVADA-12E: pics(); a drive reads its sheet of things by itself: DRIVE-16E)
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
      if (e instanceof Flock && !people) { people = []; for (const s of cast.items.values()) if ((s instanceof Figure || (PaintedFigure && s instanceof PaintedFigure)) && !s.hidden && s.opacity > 0) people.push(s); }      // (NEVADA-12E: and painted figures)
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
  drive: { haze: "#d9dde6", wire: "#2f2a26", shade: "#6664ac" },              // DRIVE-16E (DRIVE-16F: shade, the things' shadows)
};
/** A moving thing's description with its colours in the key of the scene; the same object when no key is in use. */
function keyedSpec(spec) {
  if (!keyId()) return spec;
  const out = { ...spec }, own = DEFAULTS[spec.type] || {};
  for (const k of ["color", "edge", "core", "cool", "light", "trough", "glowColor", "haze", "wire", "shade"]) {      // (DRIVE-16E: a drive's haze and wires; DRIVE-16F: and its shadows' shade)
    let v = spec[k];
    if (v === false || v === "none") continue;
    if (v === undefined) v = own[k];
    if (spec.type === "birds" && k === "color" && v === undefined && !spec.frames) v = "#2b2724";      // birds drawn as flyers
    if (typeof v !== "string") continue;
    out[k] = keyHex(v);
  }
  return out;
}

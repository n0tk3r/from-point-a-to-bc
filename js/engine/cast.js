// The cast layer: everyone and everything that stands on the ground.
//
// It is one canvas, 640x400, the same pixel grid as the backdrop. Every frame the
// people and props are sorted by depth and painted back to front, so the lead
// walks behind the car when his feet are higher on the screen than its wheels and
// in front of it when they are lower.
//
// PLANES. Each thing sits on one of three planes:
//   "back"   always behind everything else (a rug, a painted floor mark)
//   "floor"  sorted by where it meets the ground (the default)
//   "front"  always in front, wherever the lead stands (a pillar at the edge of the screen, an overhanging branch)
//
// A thing on the floor plane can give a `base` line, [[x1, y1], [x2, y2]], when
// it meets the ground along a slant (a wall running into the distance); the lead
// is then behind or in front according to which side of the line his feet are on.

import { drawFigure, poses, strideOf, PARTS, BASE } from "../art/rig.js";
import { people } from "../art/people.js";
import { props } from "../art/props.js";
import { DEPTH } from "./walk.js";

export const UNIT = 2;                 // art pixels per grid unit
export const WALK_FRAMES = 12;         // pictures in one walk cycle (two steps). The rig can draw any number; more is smoother.
const COMPASS = { S: 0, SE: 45, E: 90, NE: 135, N: 180, NW: 225, W: 270, SW: 315 };

// Finished pictures are kept so the same frame is never drawn twice. The store is
// shared by everyone on stage and held to a fixed budget: when it is full, the
// pictures that have gone longest without being used are dropped.
const cache = new Map();
const BUDGET = 3_000_000;              // pixels, about 12 MB
let stored = 0;
function remember(key, make) {
  let hit = cache.get(key);
  if (hit) { cache.delete(key); cache.set(key, hit); return hit; }       // move to the fresh end
  const sf = make(), b = sf.bounds();
  hit = { canvas: sf.toCanvas(), ox: sf.ox, oy: sf.oy, top: sf.oy - b.top, size: sf.w * sf.h };
  cache.set(key, hit);
  stored += hit.size;
  for (const [old, pic] of cache) {
    if (stored <= BUDGET) break;
    cache.delete(old); stored -= pic.size;
  }
  return hit;
}

class Sprite {
  constructor(id) {
    this.id = id;
    this.x = 0; this.y = 0; this.scale = 1; this.opacity = 1;
    this.plane = "floor"; this.base = null; this.hidden = false;
    this.flags = {};
  }
  place(x, y, scale = this.scale) { this.x = x; this.y = y; this.scale = scale; return this; }
  fade(opacity) { this.opacity = opacity; return this; }
  flag(name, on) { this.flags[name] = on; return this; }
  face() { return this; }
  /** Where this meets the ground, measured at a given x. */
  baseAt(x) {
    if (!this.base) return this.y;
    const [[x1, y1], [x2, y2]] = this.base;
    const t = x2 === x1 ? 0.5 : Math.min(1, Math.max(0, (x - x1) / (x2 - x1)));
    return y1 + (y2 - y1) * t;
  }
  tick() {}
}

/** A person, drawn by the rig. */
export class Figure extends Sprite {
  constructor(id, kind) {
    super(id);
    this.kind = kind;
    this.spec = people[kind];
    if (!this.spec) throw new Error(`No character called "${kind}" in js/art/people.js`);
    this.yaw = 90;
    this.t = 0;                         // time in the current pose, for breathing and talking
    this.phase = 0;                     // where in the walk cycle
    this.walking = false; this.talking = false; this.gesture = 0; this.act = null;
    this.stride = strideOf(this.spec) * this.spec.height * (BASE / UNIT);      // grid units covered by one full cycle at scale 1
  }

  /** Height in grid units at scale 1, for placing words above the head. */
  get h() { return this.spec.height * (BASE / UNIT) * (this.spec.seated === "chair" ? 0.84 : this.spec.seated ? 0.60 : 1.04); }

  /** Turn to face a compass point ("N", "SE"), an angle, or the old -1 (left) and 1 (right). */
  face(dir) {
    if (typeof dir === "string") this.yaw = COMPASS[dir] ?? this.yaw;
    else if (dir === 1) this.yaw = 90;
    else if (dir === -1) this.yaw = 270;
    else if (typeof dir === "number") this.yaw = ((Math.round(dir / 45) * 45) % 360 + 360) % 360;
    return this;
  }

  /** Face along a movement on screen. A small change of heading is ignored, so the figure does not twitch. */
  head(dx, dy, firm = false) {
    const want = ((Math.atan2(dx, dy * DEPTH) * 180) / Math.PI + 360) % 360;
    const off = Math.abs(((want - this.yaw + 540) % 360) - 180);
    if (firm || off > 28) this.face(want);
  }

  /** Face a point on the stage. */
  look(x, y) { if (Math.hypot(x - this.x, y - this.y) > 2) this.head(x - this.x, y - this.y, true); return this; }

  talk(on, seed = 0) {
    if (on && !this.talking) { this.t = 0; this.gesture = poses.gesture(this.spec, seed); }       // each character has their own set of gestures
    this.talking = on;
    return this;
  }

  /** Walk through a list of points in turn. A new walk replaces the one in progress. */
  walkPath(clock, points, scaleOf) {
    if (this._stop) this._stop();
    if (!points.length) return Promise.resolve();
    const end = points[points.length - 1];
    if (clock.skipping) { this.place(end[0], end[1], scaleOf(end[1])); return Promise.resolve(); }
    return new Promise((resolve) => {
      let i = 0;
      this.walking = true;
      const finish = () => { stop(); this._stop = null; this.walking = false; this.t = 0; resolve(); };
      const stop = clock.every((dt) => {
        if (clock.skipping) { this.place(end[0], end[1], scaleOf(end[1])); return finish(); }
        // ground to cover this frame: farther away means smaller steps on screen
        let budget = (this.spec.pace || 62) * Math.max(this.scale, 0.5) * (dt / 1000);      // (far off he hurries a little, or crossing the distance would drag)
        while (budget > 0 && i < points.length) {
          const dx = points[i][0] - this.x, dy = points[i][1] - this.y, dist = Math.hypot(dx, dy * DEPTH);
          if (dist < 0.01) { i++; continue; }
          this.head(dx, dy);
          const step = Math.min(budget, dist), k = step / dist;
          this.x += dx * k; this.y += dy * k; budget -= step;
          this.phase = (this.phase + step / (this.stride * this.scale)) % 1;
          if (step >= dist) i++;
        }
        this.scale = scaleOf(this.y);
        if (i >= points.length) finish();
      });
      this._stop = finish;
    });
  }

  /** A one-off action: "reach" (out, at chest height) or "pick" (down to the ground). */
  play(clock, name) {
    if (clock.skipping || this.spec.seated) return Promise.resolve();
    const low = name === "pick", out = 230, hold = 170;
    return new Promise((resolve) => {
      let t = 0;
      this.act = { low, k: 0 };
      const stop = clock.every((dt) => {
        t += dt;
        const k = t < out ? t / out : t < out + hold ? 1 : 1 - (t - out - hold) / out;
        this.act.k = Math.max(0, Math.min(1, k));
        if (t >= out * 2 + hold || clock.skipping) { stop(); this.act = null; this.t = 0; resolve(); }
      });
    });
  }

  tick(dt) { this.t += dt; }

  /** Which picture to show right now. Each character stands, walks and talks in their own way (see people.js). */
  frame(calm = false) {
    const t = this.t, spec = this.spec;
    if (spec.seated) {
      const f = this.talking ? Math.floor(t / 170) % 6 : Math.floor(t / 420) % 8, g = this.talking ? 1 : 0;
      const mouth = this.talking ? [0, 1, 2, 1][Math.floor(t / 120) % 4] : 0;
      return { key: `sit${g}.${f}.${mouth}`, pose: () => ({ ...poses.sit(spec, f, { gesture: g }), mouth }) };
    }
    if (this.act) { const k = Math.round(this.act.k * 5) / 5; return { key: `act${this.act.low ? 1 : 0}.${k}`, pose: () => poses.reach(spec, k, this.act.low) }; }
    if (this.walking) { const f = Math.floor(this.phase * WALK_FRAMES) % WALK_FRAMES; return { key: `walk${f}`, pose: () => poses.walk(spec, f / WALK_FRAMES) }; }
    if (this.talking) {
      const f = Math.floor(t / 170) % 6, mouth = [0, 1, 2, 1, 0, 2][Math.floor(t / 115) % 6];
      return { key: `talk${this.gesture}.${f}.${mouth}`, pose: () => ({ ...poses.talk(spec, f, this.gesture), mouth }) };
    }
    const f = calm ? 0 : Math.floor(t / 430) % 8, blink = !calm && Math.floor(t / 110) % 39 === 0;      // breathing and blinking stop for players who asked for less motion
    return { key: `stand${f}.${blink ? 1 : 0}`, pose: () => ({ ...poses.stand(spec, f), blink }) };
  }

  picture(palette, calm) {
    const size = Math.max(10, Math.round((BASE * this.spec.height * this.scale) / 2) * 2);     // in steps of two pixels, so pictures can be reused
    const f = this.frame(calm);
    return remember(`${this.kind}|${f.key}|${this.yaw}|${size}`, () => drawFigure(this.spec, f.pose(), this.yaw, size));
  }
}

/** A prop: a thing drawn by js/art/props.js. `scale` is its own size; it does not shrink with distance by itself. */
export class Thing extends Sprite {
  constructor(id, kind, options = {}) {
    super(id);
    this.kind = kind;
    this.prop = props[kind];
    if (!this.prop) throw new Error(`No prop called "${kind}" in js/art/props.js`);
    this.options = options;
    this.now = 0;
  }
  get h() { return 0; }
  tick(dt) { this.now += dt; }
  picture(palette, calm) {
    const p = this.prop;
    let frame = 0;
    if (p.frames > 1 && !calm && (this.kind !== "wagon" || this.flags.bounce)) frame = Math.floor((this.now / 1000) * (p.fps || 4)) % p.frames;
    const scale = Math.max(0.04, Math.round(this.scale * 32) / 32);
    // options.state is how a prop shows that something has happened to it (a screen that has come on, a lid left open)
    return remember(`${this.kind}|${this.options.state || ""}|${frame}|${scale}|${palette ? palette.key : ""}`, () => p.draw(scale, frame, { ...this.options, palette }));
  }
}

export class Cast {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.ctx.imageSmoothingEnabled = false;
    this.items = new Map();
    this.palette = null;                 // the era's colors, for props that pick them up
    this.calm = false;                   // true: no idle motion
    this.last = "";
  }

  get(id) { return this.items.get(id); }
  add(sprite) { this.items.set(sprite.id, sprite); return sprite; }
  addFigure(id, kind, x, y, scale = 1) { return this.add(new Figure(id, kind).place(x, y, scale)); }
  addThing(id, kind, x, y, scale = 1, options) { return this.add(new Thing(id, kind, options).place(x, y, scale)); }
  remove(id) { this.items.delete(id); }
  clear() { this.items.clear(); this.last = ""; this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height); }

  /** Back to front. */
  order() {
    const back = [], floor = [], front = [];
    for (const s of this.items.values()) if (!s.hidden && s.opacity > 0) (s.plane === "back" ? back : s.plane === "front" ? front : floor).push(s);
    const depth = (a, b) => {
      // a figure against a prop: which side of the prop's base line are the feet on?
      if (a instanceof Figure && b.base) return a.y - b.baseAt(a.x);
      if (b instanceof Figure && a.base) return a.baseAt(b.x) - b.y;
      return a.baseAt(a.x) - b.baseAt(b.x);
    };
    floor.sort((a, b) => depth(a, b) || (a.id < b.id ? -1 : 1));
    return [...back, ...floor, ...front];
  }

  /** Advance animations and repaint if anything changed. */
  update(dt) {
    const list = this.order();
    let sig = "";
    const shots = [];
    for (const s of list) {
      s.tick(dt);
      const pic = s.picture(this.palette, this.calm);
      const x = Math.round(s.x * UNIT) - pic.ox, y = Math.round(s.y * UNIT) - pic.oy;
      shots.push([pic, x, y, s.opacity]);
      sig += `${s.id}:${x},${y},${pic.canvas.width},${s.opacity.toFixed(2)},${cacheId(pic)};`;
    }
    if (sig === this.last) return;
    this.last = sig;
    const ctx = this.ctx;
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    for (const [pic, x, y, opacity] of shots) {
      ctx.globalAlpha = opacity;
      ctx.drawImage(pic.canvas, x, y);
    }
    ctx.globalAlpha = 1;
  }
}

let ids = 0;
const cacheId = (pic) => pic.id || (pic.id = ++ids);

// ---------- head-and-shoulders portraits, for the buttons that switch between leads ----------
const faces = new Map();
/** A small picture of someone's head, facing the viewer. Drawn once and kept. */
export function portrait(kind) {
  if (faces.has(kind)) return faces.get(kind);
  const spec = people[kind];
  if (!spec) return null;
  const size = Math.round(21 / (spec.dim.headR[1] * 2));            // every head comes out about 21 pixels tall, whoever it belongs to
  const sf = drawFigure(spec, poses.stand(spec, 0), 0, size);
  const { w, h, m, p: part } = sf, head = new Set([PARTS.HEAD, PARTS.HAIR, PARTS.HAT]);
  let x0 = w, x1 = 0, y0 = h, y1 = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    if (!m[y * w + x] || !head.has(part[y * w + x])) continue;
    if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
  }
  const side = Math.max(x1 - x0 + 1, y1 - y0 + 5) + 2;               // a square with a little of the shoulders in it
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = side;
  canvas.getContext("2d").drawImage(sf.toCanvas(), -(Math.round((x0 + x1 + 1) / 2) - side / 2), -(y0 - 1));
  faces.set(kind, canvas);
  return canvas;
}

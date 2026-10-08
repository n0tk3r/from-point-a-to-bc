// The cast layer: everyone and everything that stands on the ground.
//
// It is one canvas, 800x600, pixel for pixel over the painted backdrop. Three kinds
// of thing are on it: people, drawn by the rig; painted cut-outs (a palm, a wagon, a
// table: picture files with a clear background); and props drawn by code. Every frame
// they are sorted by depth, back to front, so the lead walks behind the wagon when his
// feet are higher on the screen than its wheels and in front of it when they are lower.
// Only what has changed since the frame before is painted again (see Cast.update).
//
// PLANES. Each thing sits on one of three planes:
//   "back"   always behind everything else (a rug, a painted floor mark)
//   "floor"  sorted by where it meets the ground (the default)
//   "front"  always in front, wherever the lead stands (a pillar at the edge of the screen, an overhanging branch)
//
// Where a thing on the floor plane meets the ground is its `base`. For a person or a
// prop that is the point it stands on. A cut-out the size of the whole picture says so
// itself: a number is a row of the picture (people whose feet are above that row are
// behind it), and a pair of points, [[x1, y1], [x2, y2]], is a line for a thing that
// meets the ground along a slant (a wall running into the distance, a car seen from a
// corner); people are then behind or in front according to which side of the line their
// feet are on.
//
// Positions are picture pixels (grid.js).

import { drawFigure, poses, strideOf, tallOf, PARTS, BASE } from "../art/rig.js";
import { people } from "../art/people.js";
import { props } from "../art/props.js";
import { DEPTH } from "./walk.js";
import { picture as fetchPicture, got } from "./assets.js";
import { W, H } from "./grid.js";

export const WALK_FRAMES = 12;         // pictures in one walk cycle (two steps). The rig can draw any number; more is smoother.
// Someone standing is drawn at exactly the size they are. Someone walking is not: each step nearer or farther would
// need a new picture of them, and a picture of a grown man takes the rig several milliseconds, a frame's worth and
// more on a slow machine. A walker's pictures are drawn at a ladder of sizes instead, each rung this much bigger than
// the one below, and the nearest rung is stretched or squeezed (by 6% at most, pixels kept hard) to the size wanted.
// It is how the old adventure games sized their people, and it means a walk cycle is drawn once for a whole band
// of the floor and found again every time anyone crosses it.
export const RUNG = 1.12;
const COMPASS = { S: 0, SE: 45, E: 90, NE: 135, N: 180, NW: 225, W: 270, SW: 315 };

// Finished pictures are kept so the same frame is never drawn twice. The store is
// shared by everyone on stage and held to a fixed budget: when it is full, the
// pictures that have gone longest without being used are dropped.
const cache = new Map();
const BUDGET = 16_000_000;             // pixels, about 64 MB. A full-size adult, cut down to the paint, is some 13,000 and a big cut-out 200,000: a scene's cut-outs and well over a thousand pictures of people.
let stored = 0;
/** The picture kept under `key`; made by make() the first time. make() gives { canvas, size, ... }, size being its pixels. */
function keep(key, make) {
  let hit = cache.get(key);
  if (hit) { cache.delete(key); cache.set(key, hit); return hit; }       // move to the fresh end
  hit = make();
  cache.set(key, hit);
  stored += hit.size;
  for (const [old, pic] of cache) {
    if (stored <= BUDGET || old === key) break;
    cache.delete(old); stored -= pic.size;
  }
  return hit;
}
/**
 * The same, for a picture drawn by the pixel renderer (a person, a prop). It is cut down to the part with paint on
 * it. The renderer leaves room all round a figure for an arm flung out, and that clear margin is more than half of
 * the picture: kept, it would be stored, and wiped and painted again with every step.
 * (ox, oy) is the point of the kept picture that stands on the ground.
 */
const remember = (key, make) => keep(key, () => {
  const sf = make();
  if (!sf.out && sf.finish) sf.finish();                                 // (as toCanvas does: turn the shapes into colors)
  const { w, h, out } = sf;
  if (!(out instanceof Uint32Array) || out.length !== w * h) return { canvas: sf.toCanvas(), ox: sf.ox, oy: sf.oy, size: w * h };     // a renderer that keeps its pixels some other way: take the picture whole
  let x0 = w, x1 = -1, y0 = h, y1 = -1;
  for (let y = 0, i = 0; y < h; y++) for (let x = 0; x < w; x++, i++) {
    if (!(out[i] >>> 24)) continue;                                      // one number a pixel; the top byte is how solid it is
    if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
  }
  if (x1 < 0) { x0 = y0 = x1 = y1 = 0; }                                 // nothing on it: keep one clear pixel
  const canvas = document.createElement("canvas");
  canvas.width = x1 - x0 + 1; canvas.height = y1 - y0 + 1;
  canvas.getContext("2d").putImageData(new ImageData(new Uint8ClampedArray(out.buffer, out.byteOffset, out.byteLength), w, h), -x0, -y0, x0, y0, canvas.width, canvas.height);
  return { canvas, ox: sf.ox - x0, oy: sf.oy - y0, size: canvas.width * canvas.height };
});

// ---------- painted pictures ----------
// A cut-out is a picture file the size of the whole picture and mostly clear. It is trimmed,
// once, to the part with paint on it, so that repainting the cast does not mean pushing a
// screenful of clear pixels for every palm and table.
function trimmed(path) {
  const img = got(path);
  if (!img) return null;                                                 // not here yet, or it would not load
  return keep("cut|" + path, () => {
    const w = img.naturalWidth, h = img.naturalHeight;
    let x0 = 0, y0 = 0, x1 = w - 1, y1 = h - 1;
    try {
      const all = document.createElement("canvas");
      all.width = w; all.height = h;
      const ctx = all.getContext("2d", { willReadFrequently: true });
      ctx.drawImage(img, 0, 0);
      const px = new Uint32Array(ctx.getImageData(0, 0, w, h).data.buffer);       // one number a pixel; the top byte is how solid it is
      const row = (y) => { for (let x = 0; x < w; x++) if (px[y * w + x] >>> 24) return true; return false; };
      const col = (x) => { for (let y = y0; y <= y1; y++) if (px[y * w + x] >>> 24) return true; return false; };
      while (y0 <= y1 && !row(y0)) y0++;
      while (y1 > y0 && !row(y1)) y1--;
      while (x0 <= x1 && y0 <= y1 && !col(x0)) x0++;
      while (x1 > x0 && !col(x1)) x1--;
    } catch { /* a browser that will not hand the pixels back gets the picture as it is */ }
    if (y0 > y1 || x0 > x1) return { canvas: null, dx: 0, dy: 0, size: 0, full: [w, h] };   // nothing painted on it at all
    const canvas = document.createElement("canvas");
    canvas.width = x1 - x0 + 1; canvas.height = y1 - y0 + 1;
    canvas.getContext("2d").drawImage(img, -x0, -y0);
    return { canvas, dx: x0, dy: y0, size: canvas.width * canvas.height, full: [w, h] };      // full: the size of the file itself
  });
}

// A painted picture shown smaller than it was painted has to be scaled smoothly, or it shimmers.
// Half-size, quarter-size (and so on) copies are made once, with smoothing, and kept. The cast then
// draws from the nearest copy that is still at least as big as it needs, so it never has to shrink
// anything by more than half in one go, which is as far as a browser's own smoothing stays clean.
function halved(key, from) {
  return keep(key, () => {
    const canvas = document.createElement("canvas");
    canvas.width = Math.ceil(from.width / 2); canvas.height = Math.ceil(from.height / 2);
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = "high";
    ctx.drawImage(from, 0, 0, from.width / 2, from.height / 2);            // exactly half, even when the size is odd
    return { canvas, size: canvas.width * canvas.height };
  }).canvas;
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
  get h() { return 0; }
  /** Where this meets the ground, measured at a given x. */
  baseAt(x) {
    const base = this.base;
    if (base == null) return this.y;                     // the point it stands on
    if (typeof base === "number") return base;           // a row of the picture
    const [[x1, y1], [x2, y2]] = base;                   // a slanted line
    const t = x2 === x1 ? 0.5 : Math.min(1, Math.max(0, (x - x1) / (x2 - x1)));
    return y1 + (y2 - y1) * t;
  }
  /** The x at which to compare this with another thing: where it stands, or the middle of its base line. */
  get mid() { return Array.isArray(this.base) ? (this.base[0][0] + this.base[1][0]) / 2 : this.x; }
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
    this.stride = strideOf(this.spec) * this.spec.height * BASE;               // pixels covered by one full cycle (two steps) at scale 1
    this.tall = tallOf(this.spec) * this.spec.height * BASE;                   // from the ground to the top of the head, as they are found (standing, or sitting on whatever they sit on)
  }

  /** How far the top of the head is above the ground, in pixels at scale 1. For placing words just over it, seated or standing. */
  get h() { return this.tall; }

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
  look(x, y) { if (Math.hypot(x - this.x, y - this.y) > 5) this.head(x - this.x, y - this.y, true); return this; }

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
      const finish = () => { stop(); this._stop = null; this.walking = false; this.hurry = false; this.t = 0; resolve(); };
      const stop = clock.every((dt) => {
        if (clock.skipping) { this.place(end[0], end[1], scaleOf(end[1])); return finish(); }
        // ground to cover this frame: farther away means smaller steps on screen
        let budget = (this.spec.pace || 155) * Math.max(this.scale, 0.5) * (dt / 1000) * (this.hurry ? 3.5 : 1);     // pace: pixels a second at full size. (Far off he hurries a little, or crossing the distance would drag.)
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

  /** Keep an arm held out (or, with `low`, down to the ground) until told otherwise: for someone who holds a thing
      up while people talk. hold(false) lets it drop. */
  hold(on = true, low = false) { this.act = on ? { low, k: 1 } : null; return this; }

  /** Stand in prayer (head bowed, eyes shut, hands folded: each of the family has their own way, `pray` in js/art/people.js)
      until told otherwise: pray(false) lets it go. It eases in and out over about a quarter of a second. Like hold(), it
      stays through talking, so a prayer said aloud is said in this pose, and it is for someone standing still: end it
      before they walk. (It is an "act" called "pray" that counts from 2 to 3, so frame() never takes it for a reach.) */
  pray(on = true) {
    const SPAN = 280, now = () => performance.now(), start = now(), praying = !!this.act && this.act.low === "pray";
    if (!on && !praying) return this;                                        // not praying: nothing to end
    const from = praying ? this.act.at() : 0, to = on ? 1 : 0;               // (an ease already under way carries on from where it has got to)
    const act = { low: "pray", at: () => from + (to - from) * Math.min(1, (now() - start) / SPAN), get k() { return 2 + this.at(); } };
    this.act = act;
    if (!on) setTimeout(() => { if (this.act === act) { this.act = null; this.t = 0; } }, SPAN + 20);
    return this;
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
      if (this.talking) {                                  // sitting down, with the gesture this line was given (their own, as when standing)
        const f = Math.floor(t / 170) % 6, mouth = [0, 1, 2, 1][Math.floor(t / 120) % 4], g = this.gesture;
        return { key: `sitT${g}.${f}.${mouth}`, pose: () => ({ ...poses.sit(spec, f, { gesture: 1, main: g }), mouth }) };
      }
      const f = calm ? 0 : Math.floor(t / 420) % 8, blink = !calm && Math.floor(t / 110) % 43 === 0;
      return { key: `sit${f}.${blink ? 1 : 0}`, pose: () => ({ ...poses.sit(spec, f), blink }) };
    }
    if (this.act) { const k = Math.round(this.act.k * 5) / 5; return { key: `act${this.act.low ? 1 : 0}.${k}`, pose: () => poses.reach(spec, k, this.act.low) }; }
    if (this.walking) { const f = Math.floor(this.phase * WALK_FRAMES) % WALK_FRAMES; return { key: `walk${f}`, pose: () => poses.walk(spec, f / WALK_FRAMES), moving: true }; }
    if (this.talking) {
      const f = Math.floor(t / 170) % 6, mouth = [0, 1, 2, 1, 0, 2][Math.floor(t / 115) % 6];
      return { key: `talk${this.gesture}.${f}.${mouth}`, pose: () => ({ ...poses.talk(spec, f, this.gesture), mouth }) };
    }
    const f = calm ? 0 : Math.floor(t / 430) % 8, blink = !calm && Math.floor(t / 110) % 39 === 0;      // breathing and blinking stop for players who asked for less motion
    return { key: `stand${f}.${blink ? 1 : 0}`, pose: () => ({ ...poses.stand(spec, f), blink }) };
  }

  picture(palette, calm) {
    const full = BASE * this.spec.height, want = full * this.scale, f = this.frame(calm);
    const even = (size) => Math.max(10, Math.round(size / 2) * 2);                              // in steps of two pixels, so pictures can be reused
    const at = (size) => remember(`${this.kind}|${f.key}|${this.yaw}|${size}`, () => drawFigure(this.spec, f.pose(), this.yaw, size));
    if (!f.moving) return at(even(want));                                                       // standing, talking, reaching: exactly the size they are
    // Walking: the nearest rung of the ladder (see RUNG), shown at the size wanted.
    const size = even(full * RUNG ** Math.round(Math.log(Math.max(this.scale, 0.01)) / Math.log(RUNG)));
    const pic = at(size), k = want / size, w = Math.round(pic.canvas.width * k), h = Math.round(pic.canvas.height * k);
    if (w === pic.canvas.width && h === pic.canvas.height) return pic;
    return { canvas: pic.canvas, ox: pic.ox * k, oy: pic.oy * k, sw: pic.canvas.width, sh: pic.canvas.height, w, h, hard: true };
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

/** Every picture file one cut-out can show: its picture, or each of its states, or each of its frames. */
export const picturesOf = (spec) => [spec.src, ...Object.values(spec.states || {}), ...(spec.frames || [])].filter(Boolean);

/**
 * A painted cut-out: a picture file with a clear background. A scene lists its cut-outs under `planes`
 * (js/content/scenes/engine-proof.js shows the format), and a cutscene can add one with cast.addPicture.
 *
 *   src                 one picture
 *   states, state       several pictures, one shown at a time: `state` is a name, or a test of the story that gives one
 *   frames, fps         several pictures shown in turn, on the game clock (flag("still", true) holds the first)
 *   when                shown only while this test of the story passes
 *   base, plane         where it sorts among the people (see the top of this file)
 *   at, foot, scale     a small cropped picture: the point `foot` of the picture is put at `at` on the stage
 *
 * With no `at` the picture is the size of the stage and is laid over it at (0, 0).
 * `when` and `state` are read again whenever the story changes (refresh), so a scene never has to
 * dress its own picture: a script records a fact, and the picture follows.
 */
export class Cutout extends Sprite {
  constructor(id, spec = {}) {
    super(id);
    this.spec = spec;
    this.plane = spec.plane || "floor";
    this.base = spec.base ?? null;
    this.foot = spec.foot || [0, 0];
    if (spec.at) this.place(spec.at[0], spec.at[1]);
    this.scale = spec.scale ?? 1;
    this.now = 0;
    this.state = typeof spec.state === "string" ? spec.state : spec.states ? Object.keys(spec.states)[0] : null;
    this.forced = {};                                    // what a script has set by hand. It holds until the scene is built again.
  }

  /** Every picture this can show. */
  paths() { return picturesOf(this.spec); }

  /** Read `when` and `state` from the story again. */
  refresh(g) {
    const s = this.spec, f = this.forced;
    this.hidden = f.shown !== undefined ? !f.shown : !!s.when && !s.when(g);
    this.state = f.state !== undefined ? f.state : typeof s.state === "function" ? s.state(g) : this.state;
    return this;
  }
  /** For scripts: show it or hide it, whatever the story says. */
  show(on = true) { this.forced.shown = !!on; this.hidden = !on; return this; }
  /** For scripts: show one of its `states`, whatever the story says. A name it has no picture for shows nothing. */
  set(state) { this.forced.state = state; this.state = state; return this; }

  tick(dt) { this.now += dt; }

  /** Which picture file to show right now, or null for none. */
  path(calm) {
    const s = this.spec;
    if (s.frames) return s.frames[calm || this.flags.still ? 0 : Math.floor((this.now / 1000) * (s.fps || 6)) % s.frames.length];
    if (!s.states) return s.src || null;
    const path = s.states[this.state];
    if (!path && this.state && this.state !== this.warned) { this.warned = this.state; console.warn(`The cut-out "${this.id}" has no picture for the state "${this.state}".`); }
    return path || null;
  }

  picture(palette, calm) {
    const path = this.path(calm), cut = path ? trimmed(path) : null, k = this.scale;
    // A cut-out with no `at` or `foot` is laid over the whole picture, so its file has to be the size of the picture.
    if (cut && !this.spec.at && !this.spec.foot && (cut.full[0] !== W || cut.full[1] !== H) && this.told !== path) {
      this.told = path;
      console.warn(`The cut-out "${this.id}" (${path}) is ${cut.full[0]}x${cut.full[1]}. A cut-out with no "at" is laid over the whole ${W}x${H} picture and should be that size.`);
    }
    if (!cut || !cut.canvas || !(k > 0.005)) return null;
    const ox = (this.foot[0] - cut.dx) * k, oy = (this.foot[1] - cut.dy) * k;        // from the foot point to the corner of the paint
    if (k === 1) return { canvas: cut.canvas, ox, oy };
    // At another size: start from the kept copy nearest in size (`size` is how big that copy is beside the
    // original), and say which part of it to draw (sw, sh) and how big on the stage (w, h).
    const w = cut.canvas.width, h = cut.canvas.height;
    let from = cut.canvas, size = 1;
    for (let n = 2; k <= size / 2 && from.width > 2 && from.height > 2; n *= 2, size /= 2) from = halved(`cut|${path}|/${n}`, from);
    return { canvas: from, ox, oy, sw: w * size, sh: h * size, w: w * k, h: h * k };
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
    this.last = "";                      // what is on the layer now, in a few characters (see update)
    this.shots = [];                     // and in full: each picture painted, where, and the box of pixels it touches
  }

  get(id) { return this.items.get(id); }
  add(sprite) {
    if (this.items.has(sprite.id)) console.warn(`Two things on the stage are called "${sprite.id}". The second has taken the place of the first.`);
    this.items.set(sprite.id, sprite);
    return sprite;
  }
  addFigure(id, kind, x, y, scale = 1) { return this.add(new Figure(id, kind).place(x, y, scale)); }
  addThing(id, kind, x, y, scale = 1, options) { return this.add(new Thing(id, kind, options).place(x, y, scale)); }
  /** A painted cut-out from a scene's `planes`. Its pictures are asked for at once; load() says when they are here. */
  addCutout(id, spec) {
    const cutout = this.add(new Cutout(id, spec));
    for (const path of cutout.paths()) fetchPicture(path);
    return cutout;
  }
  /** A painted sprite for a cutscene to move about: addPicture("wagon", { src | frames, fps, foot: [x, y] }, x, y, scale).
      It has place, fade and flag like a prop. `foot` is the point of the picture that is put at (x, y); scale is about that point. */
  addPicture(id, spec, x = 0, y = 0, scale = 1) { return this.addCutout(id, spec).place(x, y, scale); }
  remove(id) { this.items.delete(id); }
  clear() { this.items.clear(); this.last = ""; this.shots = []; this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height); }

  /** The painted cut-outs on the stage. */
  cutouts() { return [...this.items.values()].filter((s) => s instanceof Cutout); }
  /** Resolves when every picture any cut-out here can show has arrived (or has failed: it never rejects). */
  load() { return Promise.all(this.cutouts().flatMap((s) => s.paths()).map(fetchPicture)); }
  /** The story has changed: have each cut-out read its `when` and `state` again. */
  refresh(g) { for (const s of this.cutouts()) s.refresh(g); }

  /** Back to front. */
  order() {
    const back = [], floor = [], front = [];
    for (const s of this.items.values()) if (!s.hidden && s.opacity > 0) (s.plane === "back" ? back : s.plane === "front" ? front : floor).push(s);
    const person = (s) => s instanceof Figure;
    const depth = (a, b) => {
      // Two things are compared where the one that stands on a single point is standing: a person against
      // a wall is in front or behind according to the side of the wall's base line that their feet are on.
      const x = person(a) ? a.x : person(b) ? b.x : a.base == null ? a.x : b.base == null ? b.x : (a.mid + b.mid) / 2;
      return a.baseAt(x) - b.baseAt(x) || person(a) - person(b);          // feet exactly on a base line are in front of it
    };
    // (things that tie keep the order they were put on the stage in: a scene's later cut-outs lie over its earlier ones)
    floor.sort(depth);
    return [...back, ...floor, ...front];
  }

  /**
   * Advance animations, and repaint what has changed.
   * Most frames nothing has, and nothing is painted. When something has (a step, a blink, a lid that opens), only
   * the boxes it touched are wiped and painted again, back to front, with everything that crosses them. A lead
   * walking past a wagon costs a patch the size of the lead, not a screenful of palms and awnings sixty times a second.
   */
  update(dt) {
    const list = this.order();
    let sig = "";
    const shots = [];
    for (const s of list) {
      s.tick(dt);
      const pic = s.picture(this.palette, this.calm);
      if (!pic) continue;                                 // a cut-out with nothing to show, or whose picture has not arrived
      // A picture at its own size goes down on whole pixels, hard-edged. One shown at another size says how big
      // (w, h). A painted one is then drawn smoothly, and placed to a fraction of a pixel so that it glides; a
      // drawn one (`hard`: somebody walking) keeps its hard pixels and stays on whole ones.
      const sized = pic.w != null, soft = sized && !pic.hard;
      const x = soft ? Math.round((s.x - pic.ox) * 8) / 8 : sized ? Math.round(s.x - pic.ox) : Math.round(s.x) - Math.round(pic.ox);
      const y = soft ? Math.round((s.y - pic.oy) * 8) / 8 : sized ? Math.round(s.y - pic.oy) : Math.round(s.y) - Math.round(pic.oy);
      const w = soft ? Math.round(pic.w * 8) / 8 : sized ? pic.w : pic.canvas.width, h = soft ? Math.round(pic.h * 8) / 8 : sized ? pic.h : pic.canvas.height;
      const key = `${nameOf(pic.canvas)}:${x},${y},${w},${h},${s.opacity.toFixed(2)}`;
      // box: the pixels it can touch, [left, top, right, bottom). (Smoothing can spill a pixel over the edge.)
      const box = soft ? [Math.floor(x) - 1, Math.floor(y) - 1, Math.ceil(x + w) + 1, Math.ceil(y + h) + 1] : [x, y, x + w, y + h];
      shots.push({ pic, x, y, w, h, opacity: s.opacity, key, box });
      sig += key + ";";
    }
    if (sig === this.last) return;
    const W = this.canvas.width, H = this.canvas.height, ctx = this.ctx;
    const dirty = changed(this.shots, shots, W, H);
    this.last = sig;
    this.shots = shots;
    const paint = (s) => {
      ctx.globalAlpha = s.opacity;
      if (s.pic.w == null) ctx.drawImage(s.pic.canvas, s.x, s.y);
      else { ctx.imageSmoothingEnabled = !s.pic.hard; ctx.drawImage(s.pic.canvas, 0, 0, s.pic.sw, s.pic.sh, s.x, s.y, s.w, s.h); ctx.imageSmoothingEnabled = false; }
    };
    if (!dirty) {                                         // too much has changed to be worth picking over: paint the lot
      ctx.clearRect(0, 0, W, H);
      for (const s of shots) paint(s);
    } else if (dirty.length) {
      ctx.save();
      ctx.beginPath();
      for (const [l, t, r, b] of dirty) ctx.rect(l, t, r - l, b - t);
      ctx.clip();                                         // nothing outside the changed boxes is touched
      for (const [l, t, r, b] of dirty) ctx.clearRect(l, t, r - l, b - t);
      for (const s of shots) if (dirty.some(([l, t, r, b]) => s.box[0] < r && l < s.box[2] && s.box[1] < b && t < s.box[3])) paint(s);
      ctx.restore();
    }
    ctx.globalAlpha = 1;
  }
}

/**
 * What has to be painted again to get from one frame of the cast layer to the next: a short list of boxes
 * [left, top, right, bottom), or null when it is simpler to paint everything.
 * A box is where something was that is no longer there (or no longer the same picture), or where something now is
 * that was not. Things that have not changed must still be in the same order front to back; if they are not, what
 * covers what may be different anywhere, and the answer is null.
 */
function changed(before, now, W, H) {
  const count = (list) => { const n = new Map(); for (const s of list) n.set(s.key, (n.get(s.key) || 0) + 1); return n; };
  const was = count(before), is = count(now);
  const stays = (s) => was.get(s.key) === is.get(s.key);
  const order = (list) => { let keys = ""; for (const s of list) if (stays(s)) keys += s.key + ";"; return keys; };
  if (order(before) !== order(now)) return null;
  const boxes = [];
  const add = (box) => {
    let b = [Math.max(0, box[0]), Math.max(0, box[1]), Math.min(W, box[2]), Math.min(H, box[3])];
    if (b[0] >= b[2] || b[1] >= b[3]) return;                           // off the picture altogether
    for (let i = 0; i < boxes.length; i++) {
      const o = boxes[i];
      if (b[0] > o[2] || o[0] > b[2] || b[1] > o[3] || o[1] > b[3]) continue;
      boxes.splice(i, 1);                                               // the two touch: make one box of them, and see what that touches
      b = [Math.min(b[0], o[0]), Math.min(b[1], o[1]), Math.max(b[2], o[2]), Math.max(b[3], o[3])];
      i = -1;
    }
    boxes.push(b);
  };
  for (const s of before) if (!stays(s)) add(s.box);
  for (const s of now) if (!stays(s)) add(s.box);
  let area = 0;
  for (const b of boxes) area += (b[2] - b[0]) * (b[3] - b[1]);
  return boxes.length > 6 || area > W * H * 0.6 ? null : boxes;
}

// a number for each finished picture, so that update() can tell in a few characters whether the stage has changed
const names = new WeakMap();
let named = 0;
const nameOf = (canvas) => names.get(canvas) || (names.set(canvas, ++named), named);

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

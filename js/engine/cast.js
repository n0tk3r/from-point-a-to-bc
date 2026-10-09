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

import { drawFigure, drawSeat, poses, strideOf, tallOf, upOf, riseOf, standOffset, fidgetsOf, fidgetMs, fidgetHold, fidgetStep, portraitOf, PARTS, BASE } from "../art/rig.js";
import { people } from "../art/people.js";
import { paintedPeople, colourKey, unkeyed } from "../art/paint.js";
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
let budget = BUDGET;                   // (painted people at 2 or 3 times the stage's pixels have more of them: Cast.setResolution)
let stored = 0;
/** The picture kept under `key`; made by make() the first time. make() gives { canvas, size, ... }, size being its pixels. */
function keep(key, make) {
  let hit = cache.get(key);
  if (hit) { cache.delete(key); cache.set(key, hit); return hit; }       // move to the fresh end
  hit = make();
  cache.set(key, hit);
  stored += hit.size;
  for (const [old, pic] of cache) {
    if (stored <= budget || old === key) break;
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

// ---------- painted people (?people=painted), painted away from the game's own thread ----------
// Painting one picture of a person (js/art/paint.js) takes some milliseconds: on a slow machine ten to thirty at twice
// the stage's size, too long for the middle of a frame. So the cast asks a worker (js/art/painter.js) for each picture
// it does not have yet: the one wanted now first, then those likely to be wanted next (the rest of a walk in that
// direction, the other breaths, the mouth's other shapes for that gesture, the rest of getting up). Meanwhile the
// person goes on showing the last picture they showed, and the new one is used the moment it is there (a fraction of
// a second at most). What nothing could stand in for is painted before it is wanted: everyone's first picture while a
// scene opens behind its fade (Cast.opened: the scene waits for them), and the first picture of getting up or of
// sitting down again, when the point someone stands on moves (Figure.ahead). Only what is wanted with nothing to stand
// in for it all the same (someone put on the stage in the middle of a scene) is painted here and now. With no worker
// (a browser without module workers), pictures are painted here, one a frame.
let frameNo = 0;                                                     // (Cast.update counts frames)
const evenPx = (size) => Math.max(10, Math.round(size / 2) * 2);     // (sizes in steps of two pixels, as picture() has them)
const painter = {
  worker: null, failed: false, queue: [], idle: [], pending: new Map(), inFlight: 0, here: { frame: -1, n: 0 },
  keyed: "",                                                         // the colour key the painter paints in (paint.js colourKey.id: "" is none)
  /** Can pictures be painted by the painter now? It must be running, and paint in the page's own colour key. */
  ready() { return !!this.start() && this.keyed === colourKey.id; },
  start() {
    if (this.worker || this.failed) return this.worker;
    try {
      this.worker = new Worker(new URL("../art/painter.js", import.meta.url), { type: "module" });
      this.worker.onmessage = (e) => this.done(e.data);
      this.worker.onerror = (e) => { console.warn("The painter (js/art/painter.js) has stopped; people are painted on the game's own thread from now on.", (e && e.message) || ""); this.stop(); };
    } catch { this.stop(); }
    return this.worker;
  },
  stop() {
    this.failed = true; if (this.worker) this.worker.terminate(); this.worker = null;
    for (const e of this.pending.values()) if (e.then) e.then({ id: e.key, error: "the painter has stopped" });
    this.queue = []; this.idle = []; this.pending.clear(); this.inFlight = 0;
  },
  /** Have a picture painted. job: { kind, up, seat, pose, yaw, size, k, stage } (or { kind, portrait }); urgent: true, it
      is wanted on the stage now; "soon", it comes after those but before everything asked ahead; "idle", only when the
      painter has nothing else to do (the most recent first; a guess at what may be wanted, let go when there are too many).
      then(answer): the painter's answer goes to it, and not to the store (a portrait). */
  ask(key, job, urgent = false, then = null) {
    if (cache.has(key) || !this.ready()) return;
    const had = this.pending.get(key);
    if (had) {
      if (urgent === true && !had.sent && !had.urgent) {                 // (wanted now after all: first in the queue)
        const list = had.idle ? this.idle : this.queue;
        list.splice(list.indexOf(had), 1); had.urgent = true; had.idle = false; this.queue.unshift(had); this.pump();
      }
      return;
    }
    if (!urgent && this.queue.length > 240) return;                  // (more than enough ahead already)
    const entry = { key, job: { ...job, keyId: colourKey.id }, urgent: urgent === true || urgent === "soon", idle: urgent === "idle", sent: false, then };
    this.pending.set(key, entry);
    if (entry.idle) { this.idle.push(entry); if (this.idle.length > 48) this.pending.delete(this.idle.shift().key); }
    else if (urgent === "soon") { const i = this.queue.findIndex((e) => !e.urgent); this.queue.splice(i < 0 ? this.queue.length : i, 0, entry); }
    else if (urgent) this.queue.unshift(entry); else this.queue.push(entry);
    this.pump();
  },
  pump() {
    const send = (e) => {
      const { stage, ...job } = e.job;
      e.sent = true; this.inFlight++;
      try { this.worker.postMessage({ id: e.key, ...job }); } catch (err) { console.warn("The painter could not be asked for", e.key, err); this.stop(); }
    };
    while (this.worker && this.inFlight < 2 && this.queue.length) send(this.queue.shift());
    if (this.worker && !this.inFlight && this.idle.length) send(this.idle.pop());      // (nothing else to do: one guess at a time)
  },
  done(msg) {
    if (msg.id == null) { if (msg.keyed != null) this.keyed = msg.keyed; if (msg.error) console.warn(msg.error); return; }     // (a colour key loaded there: keyPainter)
    this.inFlight = Math.max(0, this.inFlight - 1);
    const entry = this.pending.get(msg.id);
    this.pending.delete(msg.id);
    if (entry && entry.then) entry.then(msg);
    else if (msg.error) console.warn(`Could not paint ${msg.id}: ${msg.error}`);
    else if (entry && !msg.stale) keep(msg.id, () => {                // (stale: it was asked for in another colour key than the painter has now)
      let canvas = msg.bitmap;
      if (!canvas) { canvas = document.createElement("canvas"); canvas.width = msg.w; canvas.height = msg.h; canvas.getContext("2d").putImageData(new ImageData(msg.data, msg.w, msg.h), 0, 0); }
      return { canvas, ox: msg.ox, oy: msg.oy, size: msg.w * msg.h, stage: entry.job.stage, k: entry.job.k };
    });
    this.pump();
  },
  /** A new scene: whatever was still waiting to be painted for the last one is let go (what is being painted now still comes). */
  forget() {
    this.queue = this.queue.filter((e) => { if (e.then) return true; this.pending.delete(e.key); return false; });
    for (const e of this.idle) this.pending.delete(e.key);
    this.idle = [];
  },
  /** May a picture be painted here and now? Always when there is nothing to stand in for it; else only when the painter
      cannot paint it (there is none, or it is not in the page's colour key yet), and once a frame. */
  mayPaintHere(needed) {
    if (needed) return true;
    if (this.ready()) return false;
    if (this.here.frame !== frameNo) { this.here.frame = frameNo; this.here.n = 0; }
    return this.here.n++ < 1;
  },
};
/** How many pictures of people are still being painted (0: everyone on the stage is as they should be). */
export const stillPainting = () => painter.pending.size;
/**
 * Painted people in a colour key (paint.js setColourKey, as a middle-ground study keys a scene): the painter paints in
 * a thread of its own, with its own copy of paint.js, so the key has to be set there too. keyPainter(url) loads the
 * module at `url` in the painter's thread, as the page has loaded it (a module that sets the key when it loads), and
 * keyPainter(url, name, ...args) then calls its export `name` with `args` (say, the study's useScene(id)). Give the key
 * the same id on both sides. Until the painter has the page's key, people are painted on the page's own thread (one
 * new picture a frame), so they are never shown in the wrong colours.
 */
export function keyPainter(url, name = null, ...args) {
  if (paintedPeople && painter.start()) painter.worker.postMessage({ import: String(url), call: name, args });
}

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

export class Sprite {
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
    this.home = this.spec;              // the person as the scene has them: found sitting, or standing (while a sitter is up, `spec` is them standing)
    this.up = null;                     // someone found sitting who has got up: where their seat is, which way it faces (see sit)
    this.move = null;                   // getting up or sitting down, under way
    this.fid = null;                    // a small movement under way (see fidget)
  }

  /** How far the top of the head is above the ground, in pixels at scale 1. For placing words just over it, seated or standing. */
  get h() { return this.spec === this.home ? this.tall : (this.tallUp ??= tallOf(this.spec) * this.spec.height * BASE); }

  /** Someone found sitting: are they sitting now? (Getting up and sitting down count as not.) Anyone else: false. */
  get seated() { return !!this.home.seated && !this.up; }
  /** How long getting up or sitting down takes them, in ms of game time. */
  get sitMs() { return this.home.seated ? riseOf(this.home).ms : 0; }
  /** Where someone found sitting sits (the point under the seat), and where they stand once up from it, [x, y] on the
      stage: in front of the seat, the way they face (someone on the ground stands where they sat). Null for anyone else. */
  get seatAt() { return this.home.seated ? (this.up ? [...this.up.seat] : [this.x, this.y]) : null; }
  get standAt() {
    if (!this.home.seated) return null;
    const u = this.up, [sx, sy] = u ? u.seat : [this.x, this.y], [dx, dy] = standOffset(this.home, u ? u.yaw : this.yaw, u ? u.size : this.sizeNow());
    return [sx + dx, sy + dy];
  }
  /** Their height in pixels as drawn now (as picture() sizes someone standing still). */
  sizeNow() { return Math.max(10, Math.round((BASE * this.home.height * this.scale) / 2) * 2); }

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
      before they walk. (It is an "act" called "pray" that counts from 2 to 3, so frame() never takes it for a reach.)
      Someone found sitting (`seated`) prays sitting down, in their own way (Lot: hands lifted, open, head bowed), and
      their lips move if they speak meanwhile; when it is let go they are back as they sat. */
  pray(on = true) {
    const SPAN = 280, now = () => performance.now(), start = now(), praying = !!this.act && this.act.low === "pray";
    if (!on && !praying) return this;                                        // not praying: nothing to end
    const from = praying ? this.act.at() : 0, to = on ? 1 : 0;               // (an ease already under way carries on from where it has got to)
    const act = { low: "pray", at: () => from + (to - from) * Math.min(1, (now() - start) / SPAN), get k() { return 2 + this.at(); } };
    if (this.spec.seated) act.frame = (me) => {                              // (frame() would draw anyone seated just sitting: this says what to draw instead)
      const k = Math.round(me.act.k * 5) / 5, spec = me.spec;
      if (!me.talking) return { key: `sitpray${k}`, pose: () => poses.reach(spec, k, "pray") };
      const mouth = [0, 1, 2, 1][Math.floor(me.t / 120) % 4];
      return { key: `sitpray${k}.${mouth}`, pose: () => ({ ...poses.reach(spec, k, "pray"), mouth }) };
    };
    this.act = act;
    if (!on) setTimeout(() => { if (this.act === act) { this.act = null; this.t = 0; } }, SPAN + 20);
    return this;
  }

  /** Dazzled: a sudden glare in the eyes (the sun off a mirror). He flinches, turns his head a little away, screws his
      eyes shut and puts a hand flat to his brow (the free hand: `hand` in js/art/people.js), and holds it until
      shade(false). It comes up fast and goes down in about a quarter of a second; if he talks meanwhile his lips move.
      For someone standing still (someone seated is left as they are). (An "act" called "shade", counted from 4 to 5.) */
  shade(on = true) {
    const SPAN = on ? 140 : 240, now = () => performance.now(), start = now(), shading = !!this.act && this.act.low === "shade";
    if (this.spec.seated || (!on && !shading)) return this;
    const from = shading ? this.act.at() : 0, to = on ? 1 : 0;
    const act = { low: "shade", at: () => from + (to - from) * Math.min(1, (now() - start) / SPAN), get k() { return 4 + this.at(); } };
    act.frame = (me) => {                                                    // (talking: the same pose, with the mouth moving)
      if (!me.talking) return null;
      const k = Math.round(me.act.k * 5) / 5, mouth = [0, 1, 2, 1, 0, 2][Math.floor(me.t / 115) % 6];
      return { key: `shade${k}.${mouth}`, pose: () => ({ ...poses.reach(me.spec, k, "shade"), mouth }) };
    };
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

  /**
   * Stand up (`sit(false)`) or sit down again (`sit(true)`), for someone found sitting; anyone else is left as they are.
   * A movement, eased, on the game clock (riseOf in js/art/rig.js: about a second; quicker for a child, slower getting
   * up off the ground or with bad knees); the promise resolves when it is done. `now` (true, or a clock that is
   * skipping): at once. Getting up, they stand in front of their seat (standAt: someone on the ground stands where they
   * sat), and a seat drawn with them (a stool, a lawn chair) is left where it was, a thing of its own on the stage. Up,
   * they are themselves on their feet (`stood` in people.js): they walk, talk, pray and fidget standing. Sitting down:
   * from standAt they sit back as they got up; from where the seat is (seatAt) they sit down on it where they stand;
   * from anywhere else they are put at the seat first.
   */
  sit(down = true, now = false) {
    const home = this.home;
    if (!home.seated) return Promise.resolve();
    const instant = now === true || !!(now && now.skipping);
    if (this.move) this.endMove();                                         // (a movement under way: finished first)
    if (down === this.seated) return Promise.resolve();
    this.endFidget();
    if (!down) {
      const seat = [this.x, this.y], yaw = this.yaw, size = this.sizeNow(), [dx, dy] = standOffset(home, yaw, size), up = upOf(home);
      this.up = { seat, yaw, size, scale: this.scale, sprite: null, stride: this.stride };
      if (home.sit && home.sit.drawn && this.cast) { const chair = new Seat(`${this.id}.seat`, this.kind, home, yaw, size).place(seat[0], seat[1], this.scale); chair.cast = this.cast; this.up.sprite = this.cast.add(chair); }
      this.place(seat[0] + dx, seat[1] + dy);
      this.spec = up; this.stride = strideOf(up) * up.height * BASE; this.t = 0;
      if (instant) return Promise.resolve();
      return new Promise((resolve) => { this.move = { up: true, t: 0, ms: riseOf(home).ms, inPlace: false, resolve }; });
    }
    const u = this.up, [fx, fy] = this.standAt, inPlace = Math.hypot(this.x - fx, this.y - fy) > 6;
    this.place(inPlace ? u.seat[0] : fx, inPlace ? u.seat[1] : fy);
    this.yaw = u.yaw;
    if (instant) { this.seatDown(); return Promise.resolve(); }
    return new Promise((resolve) => { this.move = { up: false, t: 0, ms: riseOf(home).ms * 1.05, inPlace, resolve }; });
  }
  /** The end of getting up or sitting down: as they will be from now on. */
  endMove() {
    const m = this.move;
    this.move = null;
    if (!m) return;
    if (!m.up) this.seatDown();
    this.t = 0;
    m.resolve();
  }
  /** Back on their seat: where it is, as they always sit, and the seat part of them again. */
  seatDown() {
    const u = this.up;
    if (!u) return;
    if (u.sprite && this.cast) this.cast.remove(u.sprite.id);
    this.place(u.seat[0], u.seat[1], u.scale);
    this.yaw = u.yaw; this.spec = this.home; this.stride = u.stride; this.up = null; this.t = 0;
  }

  /** The small movements that suit them as they are now (sitting or standing): names for fidget(). None while they are
      getting up or sitting down, praying, holding, reaching or shading their eyes. */
  get fidgets() { return this.act || this.move ? [] : fidgetsOf(this.spec); }
  /** The small movement playing now, or null. */
  get fidgeting() { return this.fid ? this.fid.name : null; }
  /**
   * Play one of their small movements (see `fidgets`; js/art/rig.js draws them); the promise resolves when it is over.
   * It ends on its own in a second or two (fidgetMs), and at once if they walk or talk, or a script has them pray, hold,
   * reach or shade. `{ hold: true }`, for the ones that can be held (the guard leaning on his staff, the doorkeeper's
   * folded arms): it stays in the middle until fidget(null). Nothing happens while they get up or sit down, while they
   * are busy as above, or for a name the rig does not know.
   */
  fidget(name, { hold = false } = {}) {
    if (name == null || name === false) { if (this.fid) this.fid.release = true; return Promise.resolve(); }
    if (this.move || this.act || this.walking || this.talking || !fidgetMs(this.spec, name)) return Promise.resolve();
    this.endFidget();
    return new Promise((resolve) => { this.fid = { name, t: 0, ms: fidgetMs(this.spec, name), hold: hold ? fidgetHold(name) : null, release: false, spec: this.spec, resolve }; });
  }
  endFidget() { const f = this.fid; this.fid = null; if (f) f.resolve(); }

  tick(dt) {
    this.t += dt;
    const m = this.move;
    if (m && (m.t += dt) >= m.ms) this.endMove();
    const f = this.fid;
    if (f) {
      const stop = f.hold != null && !f.release ? f.hold * f.ms : Infinity;   // (held: it waits at its middle)
      f.t = Math.min(f.t + dt, Math.max(stop, f.t));
      if (f.t >= f.ms) this.endFidget();
    }
  }

  /** Which picture to show right now. Each character stands, walks and talks in their own way (see people.js). */
  frame(calm = false) {
    const t = this.t, spec = this.spec;
    if (this.act && this.act.frame) { const own = this.act.frame(this, calm); if (own) return own; }     // (a prayer sitting down, or talking while shading the eyes: see pray, shade)
    if (this.move) {                                                       // getting up, or sitting down
      const m = this.move, e = Math.min(1, m.t / m.ms), s = e * e * (3 - 2 * e), k = Math.round((m.up ? s : 1 - s) * 12) / 12;
      return { key: `rise${m.inPlace ? "i" : ""}${k}`, pose: () => poses.rise(this.home, k, m.inPlace) };
    }
    if (this.fid) {                                                        // a small movement: until they walk, talk or are given something else to do
      const f = this.fid;
      if (this.walking || this.talking || this.act || f.spec !== spec) this.endFidget();
      else {
        const n = Math.max(6, Math.round(f.ms / 110)), q = fidgetStep(spec, f.name, f.t / f.ms, n);
        return { key: `fid${f.name}.${q}`, pose: () => poses.fidget(spec, f.name, q / n) };
      }
    }
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
    if (paintedPeople) return this.painted(calm);
    const full = BASE * this.spec.height, want = full * this.scale, f = this.frame(calm);
    const even = (size) => Math.max(10, Math.round(size / 2) * 2);                              // in steps of two pixels, so pictures can be reused
    const who = this.spec === this.home ? this.kind : this.kind + "^up";                       // (someone found sitting, on their feet)
    const at = (size) => remember(`${who}|${f.key}|${this.yaw}|${size}`, () => drawFigure(this.spec, f.pose(), this.yaw, size));
    if (!f.moving) return at(even(want));                                                       // standing, talking, reaching: exactly the size they are
    // Walking: the nearest rung of the ladder (see RUNG), shown at the size wanted.
    const size = even(full * RUNG ** Math.round(Math.log(Math.max(this.scale, 0.01)) / Math.log(RUNG)));
    const pic = at(size), k = want / size, w = Math.round(pic.canvas.width * k), h = Math.round(pic.canvas.height * k);
    if (w === pic.canvas.width && h === pic.canvas.height) return pic;
    return { canvas: pic.canvas, ox: pic.ox * k, oy: pic.oy * k, sw: pic.canvas.width, sh: pic.canvas.height, w, h, hard: true };
  }

  /** Painted (?people=painted, js/art/paint.js): the same frames, sizes and rungs as picture(), painted at the cast's
      resolution (Cast.res painted pixels to a picture pixel), shown smoothly and placed to the painted pixel. A picture
      not painted yet is asked of the painter (above), and meanwhile the one shown last stands in for it. */
  painted(calm) {
    const k = (this.cast && this.cast.res) || 1, f = this.frame(calm), { who, tag, size, key } = this.paintKey(f, k);
    if (f.moving) this.walked = true;
    let pic = cache.has(key) ? keep(key) : null;
    if (!pic) {
      // What stands in while it is painted: the last picture of them on the same footing; else their calm picture (no
      // breath, no blink: the one painted first, Cast.opened), or them standing (or sitting) still; else, for someone
      // put on the stage in place of someone else (a scene showing a man in another pose), the other's last picture.
      let had = this.shown && this.shown.who === who ? this.shown.pic : null;
      if (!had) for (const c of [this.frame(true), { key: this.spec.seated ? "sit0.0" : "stand0.0" }]) {
        const ck = this.paintKey(c, k).key;
        if (ck !== key && cache.has(ck)) { had = keep(ck); break; }
      }
      if (!had && !this.shown && this.inherit) had = this.inherit;
      if (!had && this.cast && this.cast.opening) return null;                 // (the scene is still opening behind its fade: Cast.opened)
      if (painter.mayPaintHere(!had)) {
        pic = remember(key, () => drawFigure(this.spec, f.pose(), this.yaw, Math.round(size * k), { paint: { k } }));
        pic.stage = size; pic.k = k;
      } else {
        painter.ask(key, { kind: this.kind, up: this.spec !== this.home, pose: f.pose(), yaw: this.yaw, size: Math.round(size * k), k, stage: size }, true);
        pic = had;
      }
      this.ahead(f.key, size, k, tag, who);
    }
    this.shown = { pic, who };
    const s = (f.moving ? BASE * this.spec.height * this.scale : size) / pic.stage / pic.k;   // picture pixels to a painted one
    return { canvas: pic.canvas, ox: pic.ox * s, oy: pic.oy * s, sw: pic.canvas.width, sh: pic.canvas.height, w: pic.canvas.width * s, h: pic.canvas.height * s, snap: k };
  }

  /** The painted picture of frame `f` (frame()'s) at k painted pixels to a picture pixel: who (themselves, or on their
      feet), the colour key's tag, its size (picture()'s: walkers from the ladder of sizes) and its key in the store. */
  paintKey(f, k, yaw = this.yaw) {
    const full = BASE * this.spec.height, who = this.spec === this.home ? this.kind : this.kind + "^up", tag = colourKey.id ? "|" + colourKey.id : "";
    const size = f.moving ? evenPx(full * RUNG ** Math.round(Math.log(Math.max(this.scale, 0.01)) / Math.log(RUNG))) : evenPx(full * this.scale);
    return { who, tag, size, key: `${who}|${f.key}|${yaw}|${size}|p${k}${tag}` };
  }

  /** Have the painter paint frame `f` (frame()'s, or one like it: { key, pose }) first of all, and the ones likely after
      it: its key, or null if it is here already (or there is no painter). */
  prepaint(f) {
    const k = (this.cast && this.cast.res) || 1, { who, tag, size, key } = this.paintKey(f, k);
    if (cache.has(key) || !painter.ready()) return null;
    painter.ask(key, { kind: this.kind, up: this.spec !== this.home, pose: f.pose(), yaw: this.yaw, size: Math.round(size * k), k, stage: size }, true);
    this.ahead(f.key, size, k, tag, who);
    return key;
  }

  /** A scene opening (Cast.opened): the picture they will first show (calm: no breath, no blink), and the one of them
      standing or sitting still (what stands in for any other till that is painted), asked of the painter: their keys. */
  first() {
    const spec = this.spec, still = { key: spec.seated ? "sit0.0" : "stand0.0", pose: () => ({ ...(spec.seated ? poses.sit(spec, 0) : poses.stand(spec, 0)), blink: false }) };
    return [this.prepaint(this.frame(true)), this.prepaint(still)].filter(Boolean);
  }

  /** Ask the painter for the pictures likely to be wanted next, after the one with frame key `now`: the rest of the walk
      in this direction, the other breaths, the mouth's other shapes in this gesture, the rest of getting up or of a small
      movement. (The keys and poses are frame()'s own.) */
  ahead(now, size, k, tag, who) {
    if (!painter.ready()) return;
    const spec = this.spec, up = spec !== this.home, family = (/^[a-zA-Z]+/.exec(now) || [""])[0];
    const ask = (frameKey, pose) => painter.ask(`${who}|${frameKey}|${this.yaw}|${size}|p${k}${tag}`, { kind: this.kind, up, pose, yaw: this.yaw, size: Math.round(size * k), k, stage: size }, false);
    if (family === "walk") for (let n = 0; n < WALK_FRAMES; n++) ask(`walk${n}`, poses.walk(spec, n / WALK_FRAMES));
    else if (family === "stand") {
      for (let n = 0; n < 8; n++) ask(`stand${n}.0`, { ...poses.stand(spec, n), blink: false });
      if (this.walked) {                                                     // someone who walks about: the first step of their next walk, whichever way it goes (when the painter is idle)
        const n = Math.floor(this.phase * WALK_FRAMES) % WALK_FRAMES, step = { key: `walk${n}`, moving: true }, pose = poses.walk(spec, n / WALK_FRAMES);
        for (let yaw = 0; yaw < 360; yaw += 45) {
          const { size: rung, key } = this.paintKey(step, k, yaw);
          painter.ask(key, { kind: this.kind, up, pose, yaw, size: Math.round(rung * k), k, stage: rung }, "idle");
        }
      }
    }
    else if (family === "sit") {
      for (let n = 0; n < 8; n++) ask(`sit${n}.0`, { ...poses.sit(spec, n), blink: false });
      ask("sit0.1", { ...poses.sit(spec, 0), blink: true });                    // (their first picture on sitting down again)
      if (!up && this.home.seated) {
        // Getting up, they stand on another point and nothing can stand in for their first picture: painted now, with
        // the seat they leave behind (Figure.sit).
        const on = upOf(this.home), at = evenPx(BASE * on.height * this.scale), seat = this.sizeNow();
        painter.ask(`${this.kind}^up|rise0|${this.yaw}|${at}|p${k}${tag}`, { kind: this.kind, up: true, pose: poses.rise(this.home, 0, false), yaw: this.yaw, size: Math.round(at * k), k, stage: at }, false);
        if (this.home.sit && this.home.sit.drawn) painter.ask(`${this.kind}|seat|${this.yaw}|${seat}|p${k}${tag}`, { kind: this.kind, up: false, seat: true, yaw: this.yaw, size: Math.round(seat * k), k, stage: seat }, false);
      }
    }
    else if (family === "talk") { const g = this.gesture; for (let n = 0; n < 6; n++) for (const mouth of [0, 1, 2]) ask(`talk${g}.${n}.${mouth}`, { ...poses.talk(spec, n, g), mouth }); }
    else if (family === "sitT") { const g = this.gesture; for (let n = 0; n < 6; n++) for (const mouth of [0, 1, 2]) ask(`sitT${g}.${n}.${mouth}`, { ...poses.sit(spec, n, { gesture: 1, main: g }), mouth }); }
    else if (family === "rise" || family === "risei") {
      const inPlace = family === "risei", u = this.up;
      for (let q = 0; q <= 12; q++) ask(`rise${inPlace ? "i" : ""}${q / 12}`, poses.rise(this.home, q / 12, inPlace));
      if (u && this.move && !this.move.up) {                                   // sitting down again: their first pictures back on the seat (seatDown)
        const at = evenPx(BASE * this.home.height * u.scale);
        for (const blink of [true, false]) painter.ask(`${this.kind}|sit0.${blink ? 1 : 0}|${u.yaw}|${at}|p${k}${tag}`, { kind: this.kind, up: false, pose: { ...poses.sit(this.home, 0), blink }, yaw: u.yaw, size: Math.round(at * k), k, stage: at }, false);
      }
    }
    else if (family === "fid" && this.fid) { const name = this.fid.name, n = Math.max(6, Math.round(this.fid.ms / 110)); for (let q = 0; q <= n; q++) ask(`fid${name}.${q}`, poses.fidget(spec, name, q / n)); }
    else if ((family === "act" || family === "sitpray") && this.act) {       // a prayer, a hand shading the eyes, a reach: the rest of it, easing in and out
      const low = this.act.low, base = low === "pray" ? 2 : low === "shade" ? 4 : 0;
      for (let q = 0; q <= 5; q++) { const kk = (base * 5 + q) / 5; ask(family === "act" ? `act${low ? 1 : 0}.${kk}` : `sitpray${kk}`, poses.reach(spec, kk, low)); }
    }
  }
}

/** The seat of someone who has got up from it (the goldsmith's stool, the old-timer's lawn chair), left where it stood
    until they sit down on it again (Figure.sit): drawn by the rig (drawSeat), as big as they were sitting. In depth it
    is a hair behind the point it stands on, so that someone standing right at it is in front of it. Its id is the
    person's with ".seat" after it. */
export class Seat extends Sprite {
  constructor(id, kind, spec, yaw, size) { super(id); this.kind = kind; this.spec = spec; this.yaw = yaw; this.size = size; }
  place(x, y, scale = this.scale) { super.place(x, y, scale); this.base = y - 0.5; return this; }
  picture() {
    if (!paintedPeople) return remember(`${this.kind}|seat|${this.yaw}|${this.size}`, () => drawSeat(this.spec, this.yaw, this.size));
    const k = (this.cast && this.cast.res) || 1, tag = colourKey.id ? "|" + colourKey.id : "";
    const pic = remember(`${this.kind}|seat|${this.yaw}|${this.size}|p${k}${tag}`, () => drawSeat(this.spec, this.yaw, Math.round(this.size * k), { k }));
    return { canvas: pic.canvas, ox: pic.ox / k, oy: pic.oy / k, sw: pic.canvas.width, sh: pic.canvas.height, w: pic.canvas.width / k, h: pic.canvas.height / k, snap: k };
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
    this.res = 1;                        // painted pixels to one picture pixel (painted people only: see setResolution)
    this.opening = null;                 // painted people: a scene opening, its first pictures still being painted (see opened)
    this.gone = null;                    // painted people: the last one taken off the stage, and their last picture (see remove)
  }

  /**
   * Painted people (?people=painted) are painted at the stage's real size on the screen: 1, 2 or 3 painted pixels to one
   * picture pixel (the scene view measures the stage and says which: js/engine/scene.js). The layer itself is then that
   * many times 800 x 600, and everything else on it (the painted cut-outs, the props, the moving things) is laid on it
   * with hard pixels, k by k: exactly as the style sheet shows the painting under them, so the two still meet pixel for
   * pixel. Without painted people this does nothing, and the layer is the 800 x 600 it always was.
   */
  setResolution(k) {
    if (!paintedPeople) return;
    // Below 2 times the stage is shown smoothly: from 1.5 the layer is made twice the size and the browser brings it down
    // smoothly, so nothing is lost. From 2 times it is shown with hard pixels, and hard pixels can only repeat a pixel,
    // never blend two, so the layer is never made bigger than the stage is shown (3 only from 3 times); between, the
    // people are blown up a little with hard pixels, as the painting under them is. (A stage 1199.98 screen pixels wide
    // is 1.5 times 800, as one 1599.98 wide is twice: hence 1.48 and 2.98.)
    k = k >= 2.98 ? 3 : k >= 1.48 ? 2 : 1;
    if (k === this.res) return;
    this.res = k;
    budget = BUDGET * (k === 1 ? 1 : k === 2 ? 2.5 : 4);                // (pictures of people at k times the pixels: room for as many of them)
    this.canvas.width = W * k; this.canvas.height = H * k;
    this.ctx.imageSmoothingEnabled = false;
    this.last = ""; this.shots = [];                                    // (everything is painted again, at the new size)
  }

  get(id) { return this.items.get(id); }
  /** Painted people: how many of their pictures are still being painted (0: everyone shows as they should). */
  get painting() { return painter.pending.size; }
  add(sprite) {
    if (this.items.has(sprite.id)) console.warn(`Two things on the stage are called "${sprite.id}". The second has taken the place of the first.`);
    this.items.set(sprite.id, sprite);
    return sprite;
  }
  addFigure(id, kind, x, y, scale = 1) {
    const f = this.add(new Figure(id, kind).place(x, y, scale));
    f.cast = this;                                                        // (a figure that gets up from a seat drawn with it puts the seat on the stage: Figure.sit)
    if (this.gone && this.gone.id === id && this.gone.frame === frameNo) f.inherit = this.gone.pic;   // (painted people: someone put in place of someone else, there and then, shows the other's last picture till their own is painted)
    return f;
  }
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
  remove(id) {
    const s = this.items.get(id);
    if (s && s.up && s.up.sprite) this.items.delete(s.up.sprite.id);      // (someone up from their seat takes it with them)
    if (paintedPeople && s instanceof Figure && s.shown && s.shown.pic) this.gone = { id, pic: s.shown.pic, frame: frameNo };
    this.items.delete(id);
  }
  clear() {
    this.items.clear(); this.last = ""; this.shots = []; this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    if (paintedPeople) { painter.forget(); this.gone = null; this.opening = null; }
  }

  /** The painted cut-outs on the stage. */
  cutouts() { return [...this.items.values()].filter((s) => s instanceof Cutout); }
  /** Resolves when every picture any cut-out here can show has arrived (or has failed: it never rejects). With painted
      people, when the first picture of everyone on the stage is painted too (see opened). */
  load() {
    const pictures = Promise.all(this.cutouts().flatMap((s) => s.paths()).map(fetchPicture));
    return paintedPeople ? Promise.all([pictures, this.opened()]) : pictures;
  }
  /**
   * Painted people: the scene is opening, behind its fade. Its people are put on the stage in the same go as it is
   * shown (game.js, enterScene), so a moment from now they are all here; the painter then paints the picture each one
   * first shows (Figure.first), and this resolves when they are all painted: the scene fades in on a finished stage,
   * with nothing painted on the game's own thread. Meanwhile anyone not painted yet is not shown at all (it is dark).
   * Five seconds at most: whoever is not painted by then is painted here when next shown.
   */
  opened() {
    if (!painter.ready()) return Promise.resolve();                      // (no painter, or not in this colour key: they are painted here)
    const token = (this.opening = { since: performance.now() });
    return new Promise((resolve) => {
      const people = () => [...this.items.values()].filter((s) => s instanceof Figure && !s.hidden && s.opacity > 0);
      let keys = null, again = true;
      const check = () => {
        if (!keys) keys = people().flatMap((s) => s.first());
        if (this.opening === token && !painter.failed && performance.now() - token.since < 5000) {
          if (keys.some((key) => painter.pending.has(key))) { setTimeout(check, 20); return; }
          if (again) {                                                   // then what they show by now (a prayer under way, a step), if that is not painted yet
            again = false;
            keys = people().map((s) => s.prepaint(s.frame(this.calm))).filter(Boolean);
            if (keys.length) { setTimeout(check, 20); return; }
          }
        }
        if (this.opening === token) this.opening = null;
        resolve();
      };
      setTimeout(check, 0);
    });
  }
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
    frameNo++;
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
      const sized = pic.w != null, soft = sized && !pic.hard, snap = pic.snap || 8;               // (a painted person is placed to the painted pixel)
      const x = soft ? Math.round((s.x - pic.ox) * snap) / snap : sized ? Math.round(s.x - pic.ox) : Math.round(s.x) - Math.round(pic.ox);
      const y = soft ? Math.round((s.y - pic.oy) * snap) / snap : sized ? Math.round(s.y - pic.oy) : Math.round(s.y) - Math.round(pic.oy);
      const w = soft ? Math.round(pic.w * snap) / snap : sized ? pic.w : pic.canvas.width, h = soft ? Math.round(pic.h * snap) / snap : sized ? pic.h : pic.canvas.height;
      const key = `${nameOf(pic.canvas)}:${x},${y},${w},${h},${s.opacity.toFixed(2)}`;
      // box: the pixels it can touch, [left, top, right, bottom). (Smoothing can spill a pixel over the edge.)
      const box = soft ? [Math.floor(x) - 1, Math.floor(y) - 1, Math.ceil(x + w) + 1, Math.ceil(y + h) + 1] : [x, y, x + w, y + h];
      shots.push({ pic, x, y, w, h, opacity: s.opacity, key, box });
      sig += key + ";";
    }
    if (sig === this.last) return;
    const k = this.res, W = this.canvas.width / k, H = this.canvas.height / k, ctx = this.ctx;
    const dirty = changed(this.shots, shots, W, H);
    this.last = sig;
    this.shots = shots;
    const paint = (s) => {
      ctx.globalAlpha = s.opacity;
      if (s.pic.w == null) ctx.drawImage(s.pic.canvas, s.x, s.y);
      else { ctx.imageSmoothingEnabled = !s.pic.hard; ctx.drawImage(s.pic.canvas, 0, 0, s.pic.sw, s.pic.sh, s.x, s.y, s.w, s.h); ctx.imageSmoothingEnabled = false; }
    };
    if (k !== 1) {
      // (painted people at k painted pixels to a picture pixel: the boxes are cleared and clipped on whole pixels of the
      //  layer, and everything is laid on it k times its picture size)
      if (!dirty) {
        ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        ctx.setTransform(k, 0, 0, k, 0, 0);
        for (const s of shots) paint(s);
      } else if (dirty.length) {
        ctx.save();
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.beginPath();
        for (const [l, t, r, b] of dirty) ctx.rect(l * k, t * k, (r - l) * k, (b - t) * k);
        ctx.clip();
        for (const [l, t, r, b] of dirty) ctx.clearRect(l * k, t * k, (r - l) * k, (b - t) * k);
        ctx.setTransform(k, 0, 0, k, 0, 0);
        for (const s of shots) if (dirty.some(([l, t, r, b]) => s.box[0] < r && l < s.box[2] && s.box[1] < b && t < s.box[3])) paint(s);
        ctx.restore();
      }
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.globalAlpha = 1;
      return;
    }
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
const faces = new Map(), addresses = new Map();
/**
 * Painted people: the address of someone's portrait (an object URL, or a data URL), as a promise; "" for nobody. A
 * painted portrait is a big picture (256 pixels square, a quarter of a second's painting or more), so it is painted by
 * the painter, after the pictures a scene is waiting for, and the game's own thread never waits for it. Only when the
 * painter cannot (there is none, or it is in another colour key) is it painted here (portrait, below).
 */
export function portraitAddress(kind) {
  if (!addresses.has(kind)) addresses.set(kind, new Promise((resolve) => {
    const here = () => { const c = portrait(kind); resolve(c ? c.toDataURL() : ""); };
    if (!people[kind]) return resolve("");
    if (!paintedPeople || !painter.ready()) return here();
    setTimeout(() => {                                                   // (after whatever a scene opening now asks for: Cast.opened)
      if (!painter.ready()) return here();
      painter.ask(`portrait|${kind}`, { kind, portrait: 256 }, "soon", (msg) => {
        if (msg.error || msg.stale || !(msg.blob || msg.data)) return here();
        if (msg.blob) return resolve(URL.createObjectURL(msg.blob));
        const c = document.createElement("canvas");
        c.width = msg.w; c.height = msg.h; c.getContext("2d").putImageData(new ImageData(msg.data, msg.w, msg.h), 0, 0);
        resolve(c.toDataURL());
      });
    }, 0);
  }));
  return addresses.get(kind);
}
/** A small picture of someone's head, facing the viewer. Drawn once and kept. (Painted people: a painted head and
    shoulders, turned a little, 256 pixels square: several times the size it is shown at, and shown smoothly: ui.js.) */
export function portrait(kind) {
  if (faces.has(kind)) return faces.get(kind);
  const spec = people[kind];
  if (!spec) return null;
  if (paintedPeople) { const canvas = unkeyed(() => portraitOf(spec, 256).toCanvas()); faces.set(kind, canvas); return canvas; }      // (never in a colour key)
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

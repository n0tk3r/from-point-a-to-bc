// ENGINE-21: close looks that are scenes, the hands in them, and the cue helper (round twenty-one, Act Six made bigger).
//
//   A close-up scene (`closeup` on a scene: the ship's compass seen from above, the shipwright's lock on the women's hall) is a
//   whole-stage picture of one thing seen close, with nobody standing in it: no cast is drawn and nobody walks; the portraits stay
//   switchable, and whoever is played is the one whose hand acts on a thing (a scene's handlers per lead, as anywhere); hands are
//   drawn at the scene's hand points (`hands`) by a script (g.hand); "Step back" (the button in the corner, or Esc) goes back to
//   the scene it was opened from, everyone where they stood, and the close-up hears it as it is left (`leaving`). game.js does the
//   scene's side (enterScene, openCloseup, stepBack); this file has the hands and the cues. docs/DESIGN.md, section 8, "A close
//   look that is a scene".
//
//   The cue helper (g.cues): a show in which a line of the chanter's cues a lead to do her part (the boy puppet's left hand to his
//   ear; the feet stamping as he runs), the part done by an action the scene names, and a part done at the wrong moment answered
//   by the scene (the audience laughs at a sad play, "Not yet."), after which the cue comes round again. Nothing is timed: the cue
//   waits for the player as long as it takes.

import { Sprite } from "./cast.js";
import { url } from "./assets.js";
import { props } from "../art/props.js";
import { people } from "../art/people.js";

// ---------------------------------------------------------------- hands
/** The lead's skin, as an [r, g, b] (people.js: the first tone of their `skin` ramp); a warm tan if their page has none. */
function skinOf(kind) {
  const p = people[kind], t = p && p.skin && Array.isArray(p.skin.tones) ? p.skin.tones[0] : null;
  if (!Number.isFinite(t)) return [222, 172, 138];
  return [t & 255, (t >>> 8) & 255, (t >>> 16) & 255];
}
const shade = ([r, g, b], k) => `rgb(${Math.round(r * k)},${Math.round(g * k)},${Math.round(b * k)})`;

/**
 * The engine's own stand-in for a hand in a close-up, until PEOPLE-21B's are in: a plain hand, seen from above, coming in from
 * `from` (the side of the picture its arm is on: "S", "E", "W", "N"), its fingertips at the hand point, in the lead's skin, with
 * a sleeve; `holding` (an item's id) is drawn between the finger and the thumb as a small dark bar (the thing itself is the
 * picture's: the pin in the ear, the coin on the post). Drawn once for each size and kept.
 */
const standins = new Map();
function standinHand(kind, from = "S", scale = 1, holding = null) {
  const key = `${kind}|${from}|${scale}|${holding || ""}`;
  if (standins.has(key)) return standins.get(key);
  const s = Math.max(0.3, scale), W = Math.round(90 * s), H = Math.round(150 * s), c = document.createElement("canvas");
  c.width = W; c.height = H;
  const ctx = c.getContext("2d"), skin = skinOf(kind), cx = W / 2;
  ctx.lineJoin = "round";
  // the sleeve, from the bottom edge
  ctx.fillStyle = kind === "lilsis" ? "#3b6fb0" : kind === "bigsis" ? "#6b4a8c" : "#2f5d55";
  ctx.beginPath(); ctx.moveTo(cx - 26 * s, H); ctx.lineTo(cx - 22 * s, 92 * s); ctx.lineTo(cx + 22 * s, 92 * s); ctx.lineTo(cx + 26 * s, H); ctx.closePath(); ctx.fill();
  // the palm and the back of the hand
  ctx.fillStyle = shade(skin, 1); ctx.strokeStyle = shade(skin, 0.62); ctx.lineWidth = Math.max(1, 1.6 * s);
  ctx.beginPath(); ctx.ellipse(cx, 70 * s, 21 * s, 26 * s, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  // four fingers, the first reaching to the point
  const fingers = [[-15, 30, 34], [-5, 18, 44], [6, 20, 42], [16, 34, 30]];
  for (const [dx, top, len] of fingers) {
    ctx.beginPath(); ctx.moveTo(cx + dx * s - 4.5 * s, (top + len) * s); ctx.lineTo(cx + dx * s - 4 * s, top * s + 4 * s);
    ctx.quadraticCurveTo(cx + dx * s, top * s - 2 * s, cx + dx * s + 4 * s, top * s + 4 * s); ctx.lineTo(cx + dx * s + 4.5 * s, (top + len) * s); ctx.closePath(); ctx.fill(); ctx.stroke();
  }
  // the thumb
  ctx.beginPath(); ctx.ellipse(cx - 24 * s, 60 * s, 7 * s, 16 * s, -0.7, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  if (holding) { ctx.fillStyle = "#2a2622"; ctx.fillRect(cx - 8 * s, 6 * s, 3 * s, 22 * s); }
  // turned to come in from its side (the picture is drawn coming up from the bottom)
  let out = c, foot = [cx - 5 * s, 18 * s];
  if (from !== "S") {
    const turn = { N: Math.PI, E: -Math.PI / 2, W: Math.PI / 2 }[from] || 0, r = document.createElement("canvas"), sideways = from === "E" || from === "W";
    r.width = sideways ? H : W; r.height = sideways ? W : H;
    const x = r.getContext("2d");
    x.translate(r.width / 2, r.height / 2); x.rotate(turn); x.drawImage(c, -W / 2, -H / 2);
    const [fx, fy] = [foot[0] - W / 2, foot[1] - H / 2], cs = Math.cos(turn), sn = Math.sin(turn);
    foot = [r.width / 2 + fx * cs - fy * sn, r.height / 2 + fx * sn + fy * cs];
    out = r;
  }
  const pic = { canvas: out, ox: foot[0], oy: foot[1] };
  standins.set(key, pic);
  return pic;
}

/** A hand on the stage of a close-up drawn by code: PEOPLE-21B's drawing (`draw(scale)` giving a canvas, or { canvas, ox, oy }
    with its fingertips at (ox, oy)), a thing of js/art/props.js (`prop`), or the engine's stand-in; drawn in front of everything.
    (A painted hand, `src` / `frames` / `states`, is the cast's own cut-out: game.js hand.) */
export class Hand extends Sprite {
  constructor(id, spec, kind) {
    super(id);
    this.spec = spec; this.kind = kind;
    this.plane = spec.plane || "front"; this.base = spec.base ?? null;
    this.scale = spec.scale ?? 1;
    this.now = 0;
  }
  tick(dt) { this.now += dt; }
  picture(palette, calm) {
    const s = this.spec;
    if (typeof s.draw === "function") { const p = s.draw(this.scale, { palette, calm, now: this.now }); return p && p.canvas ? p : p ? { canvas: p, ox: 0, oy: 0 } : null; }      // (PEOPLE-21B's drawing, if it is a function)
    if (s.prop && props[s.prop]) return props[s.prop].draw(this.scale, 0, { ...(s.options || {}), palette });
    return standinHand(this.kind, s.from || "S", this.scale, s.holding || null);
  }
}

// ---------------------------------------------------------------- the cue helper
/**
 * g.cues({ id, cues, wrong, done, caption }): a show of cues, each waiting for the player.
 *   cues     [{ line, parts: [{ who, action }] (or who + action, for one part), fact, done(g), wrong(g, who, action) }]: in order.
 *            `line` is the cue (the chanter's words: said, then kept on the stage as a caption until the cue is answered); a cue
 *            is answered when every one of its parts has been done, each by its lead (the one being played) doing its action (a
 *            word of the scene's: "ear", "stamp", "kneel"); then its `done` runs (the doll's pose), its `fact` is set (saved:
 *            a game loaded mid-show starts at the first cue not done), and the next cue is said.
 *   wrong    (g, cue, who, action): what a part done at the wrong moment, or by the wrong lead, does (the audience laughs at a sad
 *            play, a hiss: "Not yet."); then the cue comes round again (its line said again). A cue's own `wrong` comes first.
 *   done     (g): after the last cue.
 *   caption  false: the cue's line is not kept up after it is said.
 * Methods: start(g) (the show begins: the first cue not done is said); answer(g, action) (a script's part: true when the show
 * took it, right or wrong; false when no show is on, and the scene does what it does at other times); stop(g); `on`; `cue` (the
 * cue waiting, or null); `index`. Nothing in it is timed: the cue waits as long as the player takes.
 */
export class Cues {
  constructor(spec = {}) {
    this.spec = spec;
    this.id = spec.id || "cues";
    this.list = (spec.cues || []).map((c) => ({ ...c, parts: c.parts || [{ who: c.who, action: c.action }] }));
    this.on = false;
    this.got = new Set();                         // the parts of the cue under way done so far ("who|action"): not saved
    this.log = [];                                // what was answered, for tests: [{ cue, who, action, right }]
  }
  /** The first cue whose fact is not set (its index), or the length of the list when all are done. */
  first(g) { const i = this.list.findIndex((c) => !c.fact || !g.flag(c.fact)); return i < 0 ? this.list.length : i; }
  get cue() { return this.on ? this.list[this.index] || null : null; }
  async start(g) {
    this.index = this.first(g);
    this.got.clear();
    if (this.index >= this.list.length) { this.on = false; return false; }
    this.on = true;
    await this.call(g);
    return true;
  }
  /** The cue said, and kept up as a caption while it waits. */
  async call(g) {
    const c = this.cue;
    if (!c) return;
    g.caption(null);
    if (c.line) { await g.say(c.line); if (this.spec.caption !== false && this.cue === c) g.caption(c.line); }
  }
  stop(g) { this.on = false; this.got.clear(); g.caption(null); }
  /** A lead has done something the show may want: `action` by the one being played (or `who`). */
  async answer(g, action, who = g.store.data.active) {
    const c = this.cue;
    if (!this.on || !c) return false;
    const part = c.parts.find((p) => [].concat(p.who).includes(who) && [].concat(p.action).includes(action) && !this.got.has(`${[].concat(p.who).join("+")}|${[].concat(p.action).join("+")}`));
    this.log.push({ cue: this.index, who, action, right: !!part });
    if (!part) {
      g.caption(null);
      const wrong = c.wrong || this.spec.wrong;
      if (wrong) await wrong(g, c, who, action);
      if (this.on && this.cue === c) await this.call(g);         // the cue comes round again
      return true;
    }
    this.got.add(`${[].concat(part.who).join("+")}|${[].concat(part.action).join("+")}`);
    if (c.partDone) await c.partDone(g, part, who, action);
    if (this.got.size < c.parts.length) return true;             // more of this cue to do
    g.caption(null);
    this.got.clear();
    if (c.done) await c.done(g);
    if (c.fact) g.flag(c.fact, true);
    this.index++;
    if (this.index >= this.list.length) { this.on = false; if (this.spec.done) await this.spec.done(g); return true; }
    await this.call(g);
    return true;
  }
}

/** The picture paths a hand's spec names, for fetching ahead. */
export const handPictures = (spec) => [spec && spec.src, ...Object.values((spec && spec.states) || {}), ...((spec && spec.frames) || [])].filter(Boolean).map((p) => url(p));

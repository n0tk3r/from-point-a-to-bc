// MAP-15: the map screen and the Timer, travel on the map, and switching between leads through it. The game's `g.atlas`.
//
// The map screen is a layer of its own (#atlas: over the HUD, under the fade, the cards and the menu), built of ordinary
// HTML buttons and pictures as the HUD is, and scaled with the stage (cqw). It shows one map at a time (js/content/maps.js):
// its sheet, with the places the player has been to drawn in and named, their neighbours along the ways drawn faint, the
// ways between them, and the portraits of the family where each of them stands; at the top, the time and its date, the
// small dial (the Timer: the game's emblem, at that time's notch), the maps the player knows, and Close; under the sheet,
// the label line, which says what the pointer (or the keyboard's focus) is on and what a click there does.
//
// While it is up the world stops, as under the menu: the game clock is paused and the game is busy, so nothing in the scene
// moves, the HUD's tools, the pockets and the team bar are put away, and nothing is saved. The map's own motion (a dial
// turning, a portrait walking along the ways, the fades) runs on a timer of its own (tween, below), and a click or a key
// hurries it to its end. With less motion nothing on the map moves: a dial is at its notch at once, a portrait is where it
// is going, and one screen gives way to the next by a fade.
//
// A map whose pictures are painted (art/maps/<map>/: back.png, a picture for each place and each way, and layout.json:
// MAP-15.md, "The pictures of a map") is drawn from them. A map with no layout.json among the page's files yet, or one that
// will not load (the console says so, once), is drawn as a sketch from the pins in maps.js, as a scene with no painting is.
// Either way the positions the engine works from are one `layout` (layout(), below), and a test reads them from there.
//
// Every number is a pixel of the 800x600 stage (grid.js).

import { picture, url, hold, listed } from "./assets.js";
import { afterTo } from "./edges.js";
import { picturesOf as thoughtNames, thoughtURL } from "../art/thoughts.js";         // ENGINE-17: a refusal that is a thought shows its pictures on the label line
import { lineMs } from "./dialogue.js";                                              // ENGINE-21: a stop's line, said on the map, stays as long as a line on the stage
import { textRate } from "./save.js";

/**
 * ENGINE-17: what a `travel` (a scene's, or a place's in js/content/maps.js) says for the lead being played: true, he may
 * leave by the map; false, he may not ("Not from here."); or a line id, he may not, and that line says why ("Locked in, for
 * my comfort."), on the label line as the map's refusals are. `travel` is any of those, or a function of the game and the
 * lead ((g, who) => ...), or one for each lead ({ grandpajoe: "line.id", any: true }: `any` for whoever is not named; none
 * named and no `any`: he may). A function giving any other true value counts as true, and any other false one as false.
 */
export function travelFor(t, g, who) {
  for (let k = 0; k < 4; k++) {
    if (typeof t === "function") t = t(g, who);
    else if (t && typeof t === "object" && !Array.isArray(t)) t = Object.prototype.hasOwnProperty.call(t, who) ? t[who] : t.any;
    else break;
  }
  if (typeof t === "string") return t;
  return t === undefined || t === null ? true : !!t;
}
/** ENGINE-17: is a place drawn on its map whatever the visits say (`shown`: true, or a function of the game): a landmark,
    as the Office's B-7 is on its blueprint, which may have no scene at all. */
const shownPlace = (place, g) => !!place && (place.shown === true || (typeof place.shown === "function" && !!place.shown(g)));
/** ENGINE-21: is a place with `known` (a function of the game, or true or false) known now: true, false; undefined for a
    place with no `known` (as every place was before). */
const knownOf = (place, g) => (!place || place.known == null ? undefined : typeof place.known === "function" ? !!place.known(g) : !!place.known);
/** ENGINE-21: a stop drawn on its map now (`shown`: true, or a function of the game; none: only while a journey passes it). */
const shownStop = (stop, g) => !!stop && (stop.shown === true || (typeof stop.shown === "function" && !!stop.shown(g)));

const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const px = (v) => `${(v / 8).toFixed(3)}cqw`;          // a length in picture pixels, in the stage's own unit (800 pixels are 100cqw)
const smooth = (k) => (k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2);
const easeIn = (k) => k * k, easeOut = (k) => 1 - (1 - k) * (1 - k), linear = (k) => k;

export const FAINT = 0.28;                              // a place not yet visited that a way joins to one that has been: its picture at this opacity
export const DISC = 36, SMALL = 28, GAP = 4;            // the portraits: the team's, anyone else's, and the gap between two in a row
const NOTCH = 12, AT_A = 48;                            // the bow: rotate(48deg) at A (stop 0), 12 degrees less at each notch, -48 at B.C. (stop 8)
/** The angle of the Timer's bow at a stop (css/game.css, @keyframes turn-timer). */
export const angleOf = (stop) => AT_A - NOTCH * stop;
const SPEED = 220, LONGEST = 2500;                      // a portrait's walk along the ways: pixels a second, and the most a whole trip takes (ms)
const TIMER = { x: 180, y: 80, size: 440 };             // the Timer: 440 across, in the middle of the stage
const DIAL = { x: 348, y: 12, size: 104 };              // the small dial's place, at the top of the map screen (css/game.css, .atlas-dial)
const SHEET = [48, 140, 752, 560];                      // a sketch's sheet
const BOX = { w: 160, up: 50, down: 28 };               // a sketched place: a box round its pin, its name inside near the top, the portraits on the pin
const INK = "#1f130a";

// ---------------------------------------------------------------- the maps' check, at every start
/** Look for mistakes in the maps (js/content/maps.js) against the scenes and the eras. `scenes` is { id: scene } for every
    scene; a mark that is a function of the game is called with `game` to see which mark it gives. Plain sentences. */
export function checkMaps({ maps = {}, scenes = {}, eras = {}, sceneIds = [], game = null } = {}) {
  const problems = [], home = {};
  for (const [id, map] of Object.entries(maps)) {
    const it = `Map "${id}"`;
    if (!map || typeof map !== "object" || !map.places) { problems.push(`${it} is not a map: give it an era, a name, places and paths.`); continue; }
    if (!eras[map.era]) problems.push(`${it} is in the time "${map.era}", which is not one of the eras in js/content/world.js.`);
    else if (!Number.isInteger(eras[map.era].dial)) problems.push(`${it} is in the time "${map.era}", which has no notch on the Timer: give that era a dial in js/content/world.js.`);
    if (!map.name) problems.push(`${it} has no name for its button on the map screen.`);
    for (const [pid, place] of Object.entries(map.places)) {
      const list = (place && place.scenes) || [];
      if (!list.length && !(place && place.shown)) problems.push(`${it}, place "${pid}", lists no scene.`);      // (ENGINE-17: a landmark that is `shown` may have none)
      if (!place.label) problems.push(`${it}, place "${pid}", has no label to write on the map.`);
      if (!(place && place.on) && !(map.sketch && map.sketch.places && Array.isArray(map.sketch.places[pid]))) problems.push(`${it}, place "${pid}", has no pin in its sketch, so the map cannot be drawn before it is painted.`);      // (ENGINE-21: a place on a way is placed on it)
      list.forEach((sid, n) => {
        if (list.indexOf(sid) !== n) { problems.push(`${it}, place "${pid}", lists the scene "${sid}" twice.`); return; }
        if (!sceneIds.includes(sid)) problems.push(`${it}, place "${pid}": the scene "${sid}" is not in js/content/scenes/index.js.`);
        if (home[sid]) problems.push(`The scene "${sid}" is on two maps (${home[sid]}, and ${id}'s "${pid}"): a scene is in one place only.`);
        else home[sid] = `${id}'s "${pid}"`;
      });
    }
    for (const way of map.paths || []) {
      const name = `${it}, the way from "${way.a}" to "${way.b}"`;
      if (!map.places[way.a] || !map.places[way.b]) { problems.push(`${name}: both its places must be places of this map.`); continue; }
      if (way.journey) continue;                                                   // ENGINE-20: a way only a journey goes along (never travelled): no marks to arrive on
      for (const end of [way.a, way.b]) {
        if (!((map.places[end].scenes || []).length)) continue;                   // ENGINE-20: a way's end at a landmark with no scene: nowhere to arrive
        let mark = way.spawn && way.spawn[end];
        if (typeof mark === "function") { try { mark = mark(game); } catch (err) { problems.push(`${name}: its mark for "${end}" is a function that stopped (${err.message}).`); continue; } }
        const sid = map.places[end].scenes[0], scene = scenes[sid];
        if (!mark) problems.push(`${name} has no mark to arrive on at "${end}" (spawn: { ${end}: "<a mark of ${sid}>" }).`);
        else if (scene && !((scene.spawn || {})[mark])) problems.push(`${name} arrives at "${end}" on the mark "${mark}", which the scene "${sid}" has no spawn for.`);
      }
    }
    for (const [pid, place] of Object.entries(map.places)) {                      // ENGINE-20: the legs
      if (place && place.leg != null && typeof place.leg !== "number" && typeof place.leg !== "function") problems.push(`${it}, place "${pid}": its leg must be a number (or a function of the game giving one).`);
      if (place && place.far != null && typeof place.far !== "string" && typeof place.far !== "function" && !(typeof place.far === "object" && !Array.isArray(place.far))) problems.push(`${it}, place "${pid}": its far must be a line id (or a function of the game, or one for each leg).`);      // (ENGINE-21: or { leg: id, any: id })
      // ENGINE-21: a place that is a point of a way (`on`: the family at sea), and a place known only once a fact is true (`known`)
      if (place && place.on != null) {
        const o = place.on, w = o && (map.paths || []).find((p) => (p.a === o.a && p.b === o.b) || (p.a === o.b && p.b === o.a));
        if (!o || !w) problems.push(`${it}, place "${pid}": it is on a way (on: { a, b, at }), and "${o && o.a}" to "${o && o.b}" is no way of this map.`);
        else if (!(Number.isFinite(o.at) && o.at >= 0 && o.at <= 1) && !isPoint(o.near)) problems.push(`${it}, place "${pid}": where it is on its way is \`at\` (0 to 1, from ${o.a}) or \`near\` (a point of the map).`);
      }
      if (place && place.known != null && typeof place.known !== "function" && typeof place.known !== "boolean") problems.push(`${it}, place "${pid}": its known must be a function of the game (or true or false).`);
    }
    for (const [sid, stop] of Object.entries(map.stops || {})) {                   // ENGINE-21: the stops (a journey's pictures by the way, each with a line)
      const o = stop && stop.on, w = o && (map.paths || []).find((p) => (p.a === o.a && p.b === o.b) || (p.a === o.b && p.b === o.a));
      if (!stop || (!o && !(map.sketch && map.sketch.stops && isPoint(map.sketch.stops[sid])))) problems.push(`${it}, stop "${sid}": it needs a way it is on (on: { a, b, at }) or a pin in the sketch (sketch.stops).`);
      else if (o && !w) problems.push(`${it}, stop "${sid}": "${o.a}" to "${o.b}" is no way of this map.`);
      if (stop && stop.line != null && typeof stop.line !== "string") problems.push(`${it}, stop "${sid}": its line must be a line id.`);
    }
  }
  for (const sid of sceneIds) if (!home[sid]) problems.push(`The scene "${sid}" is on no map, so it has no Map button: give it a place in js/content/maps.js.`);
  return problems;
}

// ---------------------------------------------------------------- the layouts
/** A sketch's layout: the map's pins from maps.js, a box round each, straight ways, a plain sheet. (ENGINE-21: a place on a
    way has its pin on that way's line and nothing to draw; and the stops, from the sketch's own pins or their ways.) */
function sketchOf(id, map) {
  const places = {}, pins = (map.sketch && map.sketch.places) || {};
  for (const pid of Object.keys(map.places)) {
    const [x, y] = pins[pid] || [400, 350];
    const l = x - BOX.w / 2, r = x + BOX.w / 2, t = y - BOX.up, b = y + BOX.down;
    places[pid] = { picture: null, pin: [x, y], label: [x, t + 21], label_max: BOX.w - 14, shape: [[l, t], [r, t], [r, b], [l, b]] };
  }
  const paths = (map.paths || []).map((p) => ({ a: p.a, b: p.b, picture: null, via: [places[p.a].pin, places[p.b].pin] }));
  const L = { map: id, painted: false, sheet: SHEET, back: null, material: "a sketch", label: { color: INK, halo: null, upper: false, spacing: 0.04, size: 15 }, places, paths };
  return onWays(map, L, (pid) => pins[pid], (sid) => map.sketch && map.sketch.stops && map.sketch.stops[sid]);
}

const isPoint = (p) => Array.isArray(p) && p.length === 2 && p.every(Number.isFinite);
/** The painters' layout.json, read into the engine's own form. It throws, saying why, when it does not fit the map.
    ENGINE-21: a place or a way the painters have not drawn yet (a map that has grown since it was painted: Act Six's Akashi,
    Shosha and Osaka as a place, round twenty-one) is a stand-in on the painting (`standin`: a pin from the sketch, a plain
    box and a line in the map's ink), and the console says so once; a place on a way (`on`) needs nothing of the painters, and
    takes their pin if they give one; the stops are theirs (`stops`: [{ id, picture, pin, label }]) or stand-ins. */
function paintedOf(id, map, json) {
  const art = map.art, why = (text) => { throw new Error(text); };
  if (!json || typeof json !== "object") why("is not a layout");
  if (!(Array.isArray(json.sheet) && json.sheet.length === 4 && json.sheet.every(Number.isFinite))) why("has no sheet [left, top, right, bottom]");
  const label = { color: INK, halo: null, upper: false, spacing: 0.04, size: 15, ...(json.label || {}) };
  label.size = Math.min(18, Math.max(13, Number(label.size) || 15));
  const places = {}, given = Object.fromEntries((json.places || []).map((p) => [p.id, p])), sketch = (map.sketch && map.sketch.places) || {}, standins = [];
  for (const [pid, place] of Object.entries(map.places)) {
    const p = given[pid];
    if (place.on) continue;                                                        // (ENGINE-21: placed on its way, below)
    if (!p) {                                                                       // ENGINE-21: not painted yet: a stand-in
      if (!isPoint(sketch[pid])) why(`has no place "${pid}"`);
      const [x, y] = sketch[pid], l = x - 44, r = x + 44, t = y - 34, b = y + 16;
      places[pid] = { picture: null, standin: true, shape: [[l, t], [r, t], [r, b], [l, b]], pin: [x, y], label: [x, t - 6], label_max: 150 };
      standins.push(`the place "${pid}"`);
      continue;
    }
    if (!p.picture || !(Array.isArray(p.shape) && p.shape.length >= 3 && p.shape.every(isPoint)) || !isPoint(p.pin) || !isPoint(p.label)) why(`needs a picture, a shape, a pin and a label for the place "${pid}"`);
    places[pid] = { picture: art + p.picture, shape: p.shape, pin: p.pin, label: p.label, label_max: Number(p.label_max) || 150 };
  }
  const paths = (map.paths || []).map((way) => {
    const p = (json.paths || []).find((q) => (q.a === way.a && q.b === way.b) || (q.a === way.b && q.b === way.a));
    if (!p && places[way.a] && places[way.b]) { standins.push(`the way from "${way.a}" to "${way.b}"`); return { a: way.a, b: way.b, picture: null, standin: true, via: [places[way.a].pin, places[way.b].pin] }; }      // ENGINE-21
    if (!p) why(`has no way between "${way.a}" and "${way.b}"`);
    if (!p.picture || !(Array.isArray(p.via) && p.via.length >= 2 && p.via.every(isPoint))) why(`needs a picture and a via for the way between "${way.a}" and "${way.b}"`);
    return { a: way.a, b: way.b, picture: art + p.picture, via: p.a === way.a ? p.via : [...p.via].reverse() };      // (kept in maps.js's order: from a to b)
  });
  const L = { map: id, painted: true, sheet: json.sheet, back: art + "back.png", material: json.material || "", label, places, paths, standins };
  const theirs = Object.fromEntries((json.stops || []).filter((s) => s && s.id).map((s) => [s.id, s]));
  onWays(map, L, (pid) => (given[pid] && isPoint(given[pid].pin) ? given[pid].pin : null), (sid) => (theirs[sid] && isPoint(theirs[sid].pin) ? theirs[sid].pin : null));
  for (const [sid, s] of Object.entries(L.stops)) {                                // ENGINE-21: a stop's own picture, if the painters gave one
    const t = theirs[sid];
    if (t && t.picture) { s.picture = art + t.picture; s.standin = false; if (isPoint(t.label)) s.label = t.label; }
    else standins.push(`the stop "${sid}"`);
  }
  return L;
}

// ---------------------------------------------------------------- ENGINE-21: points along the ways
/** The length along a line of points at each of its points: [0, ...]. */
const lensOf = (line) => { const out = [0]; for (let i = 1; i < line.length; i++) out.push(out[i - 1] + Math.hypot(line[i][0] - line[i - 1][0], line[i][1] - line[i - 1][1])); return out; };
/** The point at distance s along a line (its lengths `lens`). */
function pointAt(line, lens, s) {
  if (line.length < 2) return line[0] ? [line[0][0], line[0][1]] : [0, 0];
  s = Math.max(0, Math.min(lens[lens.length - 1], s));
  let i = 1;
  while (i < lens.length - 1 && lens[i] < s) i++;
  const k = lens[i] > lens[i - 1] ? (s - lens[i - 1]) / (lens[i] - lens[i - 1]) : 1;
  return [line[i - 1][0] + (line[i][0] - line[i - 1][0]) * k, line[i - 1][1] + (line[i][1] - line[i - 1][1]) * k];
}
/** The distance along a line of the point of it nearest p, at or after `from` (the first nearest, for a line that comes back on itself). */
function nearestS(line, lens, p, from = 0) {
  let best = Infinity, at = from;
  for (let i = 1; i < line.length; i++) {
    if (lens[i] < from) continue;
    const [x1, y1] = line[i - 1], [x2, y2] = line[i], vx = x2 - x1, vy = y2 - y1, L2 = vx * vx + vy * vy;
    let k = L2 ? ((p[0] - x1) * vx + (p[1] - y1) * vy) / L2 : 0;
    k = Math.max(lens[i - 1] < from ? (from - lens[i - 1]) / (lens[i] - lens[i - 1] || 1) : 0, Math.min(1, k));
    const d = Math.hypot(x1 + vx * k - p[0], y1 + vy * k - p[1]);
    if (d < best - 0.01) { best = d; at = lens[i - 1] + (lens[i] - lens[i - 1]) * k; }
  }
  return at;
}
/** The part of a line between two distances along it (from s0 to s1; s1 below s0: the part turned round). */
function cutLine(line, lens, s0, s1) {
  const back = s1 < s0, a = Math.min(s0, s1), b = Math.max(s0, s1), out = [pointAt(line, lens, a)];
  for (let i = 0; i < line.length; i++) if (lens[i] > a && lens[i] < b) out.push([line[i][0], line[i][1]]);
  out.push(pointAt(line, lens, b));
  return back ? out.reverse() : out;
}
/** A way's line from one of its places to the other (its `via`, turned round as needed); null if the layout has no such way. */
function wayLine(L, a, b) {
  const w = L.paths.find((p) => (p.a === a && p.b === b) || (p.a === b && p.b === a));
  return w ? (w.a === a ? w.via : [...w.via].reverse()) : null;
}
/** ENGINE-21: the places of a map that are a point of a way (`on: { a, b, at | near }`: the family at sea, between Yui and Osaka),
    and the map's stops, placed on the layout L: each a pin, and nothing of its own to draw or click. `pinOf(pid)` and
    `stopPin(sid)` give a pin the layout (or the sketch) has for one, which is used as it is. */
function onWays(map, L, pinOf, stopPin) {
  const at = (o) => {
    const line = wayLine(L, o.a, o.b) || (L.places[o.a] && L.places[o.b] ? [L.places[o.a].pin, L.places[o.b].pin] : null);
    if (!line) return null;
    const lens = lensOf(line);
    return isPoint(o.near) ? pointAt(line, lens, nearestS(line, lens, o.near)) : pointAt(line, lens, Math.max(0, Math.min(1, Number(o.at) || 0)) * lens[lens.length - 1]);
  };
  for (const [pid, place] of Object.entries(map.places)) {
    if (!place.on) continue;
    const pin = (pinOf && pinOf(pid)) || at(place.on) || [400, 350];
    L.places[pid] = { picture: null, pin: pin.map((v) => Math.round(v * 10) / 10), label: null, label_max: 0, shape: null, onWay: { a: place.on.a, b: place.on.b } };
  }
  L.stops = {};
  for (const [sid, stop] of Object.entries(map.stops || {})) {
    const pin = (stopPin && stopPin(sid)) || (stop.on ? at(stop.on) : null);
    if (!pin) continue;
    L.stops[sid] = { picture: null, standin: true, pin: pin.map((v) => Math.round(v * 10) / 10), label: [Math.round(pin[0]), Math.round(pin[1] - 12)] };
  }
  return L;
}

/** Every picture a layout shows. (ENGINE-21: and its stops' pictures.) */
const picturesOf = (L) => [L.back, ...Object.values(L.places).map((p) => p.picture), ...L.paths.map((p) => p.picture), ...Object.values(L.stops || {}).map((s) => s.picture)].filter(Boolean);

// The Timer's three pieces (the emblem's, in art/emblem/): at 1024 once the game has them (DIAL-15's), else the 512s that
// the begin screen gives a sharp screen. The small dial on the map is a quarter of the Timer's size: the 512s are enough.
const PIECES = ["sky", "turn", "top"];
const SMALL_SET = { sky: "art/emblem/timer-sky-2x.png", turn: "art/emblem/timer-turn.png", top: "art/emblem/timer-top-2x.png" };
const bigSet = () => {
  const big = Object.fromEntries(PIECES.map((n) => [n, `art/emblem/timer-${n}-1024.png`]));
  return PIECES.every((n) => listed(big[n])) ? big : SMALL_SET;
};

// ---------------------------------------------------------------- the map screen
export class Atlas {
  constructor(game) {
    this.g = game;
    this.el = game.stage.querySelector("#atlas");
    this.open = false;          // the map screen is up
    this.shown = null;          // the id of the map it shows
    this.mode = null;           // "map" (the Map button, M) or "switch" (a switch: someone is waiting to be dropped into, `target`)
    this.target = null;
    this.moving = false;        // the map's own motion is under way (a dial, a walk): a click or a key hurries it (`rush`)
    this.rush = false;
    this.busy = false;          // a fade is under way: clicks and keys wait for it
    this.scenes = {};           // every scene, by its id, once the game has them all (game.js start)
    this.layouts = {};          // each map's layout, once read (layout()); a test can give one with useLayout()
    this._layouts = {};
    this._said = new Set();
    this.walked = [];           // where the portrait was seen on the last walk (for tests)
    if (!this.el) return;       // (a page without the layer)
    this.el.setAttribute("role", "dialog");
    // (in the order the keyboard goes through them: the chips, the dial, the sheet's places and portraits, Close)
    this.el.innerHTML = `
      <div class="atlas-band">
        <p class="atlas-when"><b></b><span></span></p>
        <div class="atlas-chips" role="group" aria-label="The maps you know"></div>
        <button class="atlas-dial" type="button" data-act="dial" aria-label="Turn the dial"><span class="sky"></span><span class="turn"></span><span class="top"></span></button>
      </div>
      <div class="atlas-sheets"></div>
      <button class="tool atlas-close" type="button" data-act="close" aria-label="Close the map: back to the game" title="Back to the game (Esc)"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5.5 5.5 L14.5 14.5 M14.5 5.5 L5.5 14.5"/></svg></button>
      <p class="atlas-label"></p>
      <div class="atlas-timer" aria-hidden="true"><span class="sky"></span><span class="turn"></span><span class="top"></span></div>`;
    const q = (s) => this.el.querySelector(s);
    this.sheetsEl = q(".atlas-sheets"); this.bandEl = q(".atlas-band"); this.whenEl = q(".atlas-when"); this.chipsEl = q(".atlas-chips");
    this.dialEl = q(".atlas-dial"); this.labelEl = q(".atlas-label"); this.timerEl = q(".atlas-timer");
    // While the map moves, a press (a click, a tap) hurries it, and does nothing else; during a fade a click does nothing at all.
    this.el.addEventListener("pointerdown", (event) => {
      this.hurried = this.open && this.moving;
      if (this.hurried) { this.rush = true; event.preventDefault(); event.stopPropagation(); }
    }, true);
    this.el.addEventListener("click", (event) => {
      if (this.open && (this.moving || this.busy || (this.hurried && event.detail))) { event.preventDefault(); event.stopPropagation(); }
      this.hurried = false;
    }, true);
    this.el.addEventListener("click", (event) => this.onClick(event));
    this.el.addEventListener("pointerover", (event) => { this.over = this.whatIs(event.target); this.say(); });
    this.el.addEventListener("pointerout", (event) => { if (!this.el.contains(event.relatedTarget) || !this.whatIs(event.relatedTarget)) { this.over = null; this.say(); } });
    // (the focus the map gives itself as it comes up is not the player's: the label line keeps to what can be done, until they move it)
    this.el.addEventListener("focusin", (event) => { if (this._placing) return; this.focused = this.whatIs(event.target); this.say(); });
    this.el.addEventListener("focusout", (event) => { if (!this.el.contains(event.relatedTarget)) { this.focused = null; this.say(); } });
    window.addEventListener("resize", () => { if (this.open) this.sizeFaces(); });
  }

  // ---------- what the map knows ----------
  get maps() { return this.g.maps || {}; }
  /** The map and the place a scene is on: { id, map, place }, or null. */
  mapOf(sceneId) {
    if (!this._index) {
      this._index = {};
      for (const [id, map] of Object.entries(this.maps)) for (const [pid, place] of Object.entries(map.places || {}))
        for (const sid of place.scenes || []) if (!this._index[sid]) this._index[sid] = { id, map, place: pid };
    }
    return this._index[sceneId] || null;
  }
  /** The active lead's own map: { id, map, place }, or null for a scene on no map. (ENGINE-17: his own scene's, g.here: while
      he looks down through a grille, the scene he looks down from) */
  own() { return this.g.here ? this.mapOf(this.g.here.id) : null; }
  /** A map's notch on the Timer (its era's `dial`), or null. */
  stop(mapId) { const era = this.g.eras[this.maps[mapId].era]; return era && Number.isInteger(era.dial) ? era.dial : null; }
  era(mapId) { return this.g.eras[this.maps[mapId].era] || { name: this.maps[mapId].name, date: "" }; }

  /** The leads who stand on a map: [{ id, scene, place, team, active }], at each place the team first (in the team's order,
      the one being played among them), then anyone else. A lead who is not on the team is left out where they are one of
      the scene's own people (its `actors`: Ranger and Grandpa Joe at the Last Stop in Act Four, before they lead): there
      they are part of the place, not one of the family left there. */
  facesOn(mapId) {
    const g = this.g, d = g.store.data, team = d.team.includes(d.active) ? d.team : [d.active, ...d.team], out = [];
    const j = this._journey;                                                     // ENGINE-20: a journey under way: the travellers at the place it starts from
    if (j && j.map === mapId) return j.ids.map((id) => ({ id, scene: null, place: j.from, team: true, active: id === d.active }));
    for (const id of [...team, ...g.leads.filter((who) => !team.includes(who))]) {
      const at = d.where[id], m = at && at.scene ? this.mapOf(at.scene) : null;
      if (!m || m.id !== mapId) continue;
      const onTeam = team.includes(id), sc = this.scenes[at.scene];
      if (!onTeam && sc && (sc.actors || []).some((a) => a.id === id)) continue;
      out.push({ id, scene: at.scene, place: m.place, team: onTeam, active: id === d.active });
    }
    return out;
  }
  /** Which places of a map are visited, and which faint. A place is visited once any of its scenes has been entered (the
      save's `visited`), or while someone of the team stands in it (a lead is only ever where the player has been, but a
      script can put one somewhere first, as the proof does); a place not visited that a way joins to a visited one is faint. */
  stateOf(mapId) {
    const map = this.maps[mapId], seen = new Set(this.g.store.data.visited || []);
    for (const f of this.facesOn(mapId)) if (f.team && f.scene) seen.add(f.scene);
    // ENGINE-21: a place with `known` (a function of the game: Shosha, once the family knows the way, `edo.knowWay`) is not on
    // the map at all until it is true (not even faint, nor its ways), and then is drawn in and can be travelled to, as a place
    // been to is, before anyone has set foot in it: the way there is known.
    const knows = (pid) => knownOf(map.places[pid], this.g);
    const hidden = new Set(Object.keys(map.places).filter((pid) => knows(pid) === false));
    // (ENGINE-17: `entered`, the places really been to; `visited`, what is drawn in: those and the landmarks, `shown`, which
    // neither make a map known nor make the places beside them faint)
    const entered = new Set(Object.keys(map.places).filter((pid) => !hidden.has(pid) && (knows(pid) === true || (map.places[pid].scenes || []).some((s) => seen.has(s)))));
    const j = this._journey;                                                     // ENGINE-20: a journey draws in where it starts and where it goes (and the places passed)
    if (j && j.map === mapId) for (const pid of j.places) if (map.places[pid]) { entered.add(pid); hidden.delete(pid); }
    const visited = new Set([...entered, ...Object.keys(map.places).filter((pid) => !hidden.has(pid) && shownPlace(map.places[pid], this.g))]);
    const faint = new Set();
    for (const p of map.paths || []) {
      if (entered.has(p.a) && !visited.has(p.b) && !hidden.has(p.b)) faint.add(p.b);
      if (entered.has(p.b) && !visited.has(p.a) && !hidden.has(p.a)) faint.add(p.a);
    }
    return { visited, faint, entered, hidden };
  }
  /** The maps the player knows (one of their places visited, or someone standing on it), in the dial's order: A first. */
  known() {
    const ids = Object.keys(this.maps), at = (id) => ids.indexOf(id);
    return ids.filter((id) => this.stop(id) != null && (this.stateOf(id).entered.size || this.facesOn(id).length))      // (ENGINE-17: entered: a landmark makes no map known)
      .sort((a, b) => this.stop(a) - this.stop(b) || at(a) - at(b));
  }
  /** May the lead leave the scene they are in by the map? Its `travel`: false never, or a function of the game. (ENGINE-17:
      and of the lead, or one for each lead; and the place's own `travel` too: both must let him. travelFor, above.) */
  may() { return !this.refusal(); }
  /** ENGINE-17: why the lead being played may not leave his scene by the map now, or null if he may: { line } (the line his
      scene's `travel`, or his place's, names; null for a plain refusal, "Not from here."). */
  refusal() {
    const g = this.g, here = g.here, own = this.own(), who = g.store.data.active, place = own && own.map.places[own.place];
    for (const t of [here && here.travel, place && place.travel]) {
      const r = travelFor(t, g, who);
      if (r !== true) return { line: typeof r === "string" ? r : null };
    }
    return null;
  }
  /** ENGINE-17: the refusal as the label line shows it: "Not from here.", or its line's words (or pictures, for a thought). */
  refused() {
    const r = this.refusal(), entry = r && r.line ? this.g.lines[r.line] : null;
    if (r && r.line && !entry) this.once(`The map's refusal line "${r.line}" is not in the lines files: "Not from here." is said instead.`);
    if (!entry) return { text: "Not from here.", pictures: null };
    return entry[2] != null ? { text: "", pictures: thoughtNames(entry[2], `the line "${r.line}"`) } : { text: entry[1], pictures: null };
  }
  /** SCENES-17: what a landmark says when it is clicked or pointed at (a place with no scene, never travelled to: the
      Office's B-7, RESTRICTED): its `travel` for the lead being played, when that names a line, as refused() gives one
      ({ text } or { pictures }); otherwise null, and a click on it does nothing, as before. Only on the lead's own map. */
  landmarkSays(mapId, pid) {
    const own = this.own(), place = this.maps[mapId] && this.maps[mapId].places[pid];
    if (!place || (place.scenes || []).length || !own || own.id !== mapId || place.travel == null) return null;
    const line = travelFor(place.travel, this.g, this.g.store.data.active);
    if (typeof line !== "string") return null;
    const entry = this.g.lines[line];
    if (!entry) { this.once(`The landmark "${pid}" names the line "${line}", which is not in the lines files: it says nothing.`); return null; }
    return entry[2] != null ? { text: "", pictures: thoughtNames(entry[2], `the line "${line}"`) } : { text: entry[1], pictures: null };
  }
  /**
   * ENGINE-20: the legs of a journey. A place of a map can have a `leg` (a number, or a function of the game giving one: in
   * js/content/maps.js): the family may travel by the map only between places of the leg they are in, which is the leg of the
   * place whose scenes hold the lead's scene. A place of another leg shows as visited (drawn in, its name), but refuses, with a
   * line of its own (`far` on the place: a line id, or a function of the game giving one; "Twelve days by sea."), on the label
   * line as the map's refusals are. Places with no `leg` behave as before (they are of every leg). A way between two legs is
   * drawn as any way is, once both its places are visited, but no route goes along it.
   */
  legOf(mapId, pid) {
    const place = this.maps[mapId] && this.maps[mapId].places[pid], leg = place ? (typeof place.leg === "function" ? place.leg(this.g) : place.leg) : null;
    return typeof leg === "number" && Number.isFinite(leg) ? leg : null;
  }
  /** Is a place of a map in the lead's own leg (or of no leg, or the lead's own place of no leg)? On another map: yes. */
  sameLeg(mapId, pid) {
    const own = this.own();
    if (!own || own.id !== mapId) return true;
    const mine = this.legOf(mapId, own.place), theirs = this.legOf(mapId, pid);
    return mine == null || theirs == null || mine === theirs;
  }
  /** ENGINE-20: why a place of another leg is refused: its `far` line as the label line shows it ({ text } or { pictures }), or
      the engine's own words; null for a place of the lead's own leg. */
  farSays(mapId, pid) {
    if (this.sameLeg(mapId, pid)) return null;
    // ENGINE-21: the far line may differ with the leg the lead is in ("Yui is twelve days back by sea." from Osaka, something else
    // from the hills): `far` is a line id, and a line of that id with the leg after it ("edo.map.far.yui.3") is said first if
    // the lines files have it; or one for each leg ({ 2: id, 3: id, any: id }); or a function of the game and the leg.
    const place = this.maps[mapId].places[pid], own = this.own(), leg = own && own.id === mapId ? this.legOf(mapId, own.place) : null;
    let line = place.far;
    if (typeof line === "function") line = line(this.g, leg);
    else if (line && typeof line === "object") line = Object.prototype.hasOwnProperty.call(line, leg) ? line[leg] : line.any;
    const lines = this.g.lines, perLeg = typeof line === "string" && leg != null && lines[`${line}.${leg}`] ? `${line}.${leg}` : null;
    if (perLeg) line = perLeg;
    const entry = typeof line === "string" ? lines[line] : null;
    if (typeof line === "string" && !entry) this.once(`The place "${pid}" of the map "${mapId}" names the line "${line}" for its far, which is not in the lines files: "Too far to go back." is said instead.`);
    if (!entry) return { text: "Too far to go back.", pictures: null };
    return entry[2] != null ? { text: "", pictures: thoughtNames(entry[2], `the line "${line}"`) } : { text: entry[1], pictures: null, line };      // (ENGINE-21: and which line it was)
  }
  /** The fewest ways from one place of a map to another through visited places only: { places, ways }, or null. (ENGINE-20:
      through places of the lead's own leg only, and never along a way that is only a journey's.) */
  route(mapId, from, to) {
    const map = this.maps[mapId], { entered: visited } = this.stateOf(mapId);      // (ENGINE-17: through places really been to, never a landmark only drawn)
    if (!visited.has(from) || !visited.has(to) || !this.sameLeg(mapId, to)) return null;
    const back = { [from]: null }, queue = [from];
    while (queue.length) {
      const here = queue.shift();
      if (here === to) break;
      for (const way of map.paths || []) {
        if (way.journey) continue;
        const next = way.a === here ? way.b : way.b === here ? way.a : null;
        if (next && visited.has(next) && !(next in back) && this.sameLeg(mapId, next)) { back[next] = { from: here, way }; queue.push(next); }
      }
    }
    if (!(to in back)) return null;
    const places = [to], ways = [];
    for (let p = to; back[p]; p = back[p].from) { ways.unshift(back[p].way); places.unshift(back[p].from); }
    return { places, ways };
  }
  /** Why the lead cannot travel to that place of their own map now, in words; or null if they can. */
  cannot(pid) {
    const own = this.own();
    if (!own) return "the scene the lead is in is on no map";
    if (!own.map.places[pid]) return `"${pid}" is not a place of the map "${own.id}"`;
    if (pid === own.place) return "the lead is there already";
    if (!(own.map.places[pid].scenes || []).length) return `"${pid}" has no scene to go to`;                     // ENGINE-17: a landmark
    if (!this.stateOf(own.id).entered.has(pid)) return `the player has not been to "${pid}" yet`;                 // (ENGINE-17: entered)
    if (!this.sameLeg(own.id, pid)) return `"${pid}" is in another leg of the journey (its far)`;                 // ENGINE-20: the legs
    if (!this.may()) return `the scene "${this.g.here.id}" (or its place) does not let the lead leave by the map now (its travel)`;
    if (!this.route(own.id, own.place, pid)) return `there is no way to "${pid}" through the places visited`;
    return null;
  }
  /** The mark a lead arrives on at a place along a way: the way's `spawn` for that end (a function of the game is asked now). */
  markOf(way, pid) { const m = way.spawn && way.spawn[pid]; return typeof m === "function" ? m(this.g) : m || "default"; }

  // ---------- the pictures ----------
  /** A map's layout: from its layout.json when that is among the page's files (fetched once, then held), or the sketch's. */
  layout(mapId) {
    if (this.layouts[mapId]) return Promise.resolve(this.layouts[mapId]);
    if (this._layouts[mapId]) return this._layouts[mapId];
    const map = this.maps[mapId], file = map.art ? map.art + "layout.json" : null;
    return (this._layouts[mapId] = (async () => {
      let L = null;
      if (file && listed(file)) {
        try {
          const address = await hold(file, { quiet: true });
          if (!address) throw new Error("would not load");
          let json;
          try { json = await (await fetch(address)).json(); } catch { throw new Error("is not JSON"); }
          L = paintedOf(mapId, map, json);
          if (L.standins && L.standins.length) this.once(`The map "${mapId}" is painted, but ${file} has nothing yet for ${L.standins.join(", ")}: each is drawn as a stand-in on the painting until it is painted (ENGINE-21).`);
        } catch (err) { this.once(`The map "${mapId}" is drawn as a sketch, because ${file} ${err.message}.`); }
      }
      return (this.layouts[mapId] = L || sketchOf(mapId, map));
    })());
  }
  /** For tests and tools: give a map a layout, as its layout.json would (its pictures are then fetched as named), or none
      (null: the sketch). */
  useLayout(mapId, json) {
    delete this._layouts[mapId];
    return (this.layouts[mapId] = json ? paintedOf(mapId, this.maps[mapId], json) : sketchOf(mapId, this.maps[mapId]));
  }
  once(text) { if (!this._said.has(text)) { this._said.add(text); console.warn(text); } }
  /** Quietly, after the rest of the game's pictures (game.js, gather): the dials' pictures, and every painted map's
      layout and pictures. `spare` waits for a moment the page has to spare. */
  async gather(spare) {
    for (const path of new Set([...Object.values(SMALL_SET), ...Object.values(bigSet())])) { await spare(); await hold(path, { quiet: true }); }
    for (const id of Object.keys(this.maps)) {
      const map = this.maps[id];
      if (!map.art || !listed(map.art + "layout.json")) continue;
      await spare();
      for (const path of picturesOf(await this.layout(id))) { await spare(); await hold(path, { quiet: true }); }
    }
  }

  // ---------- opening and closing ----------
  /** The map screen comes up: the world stops, as under the menu. */
  enter() {
    const g = this.g;
    this.placeClose();                          // MAP-15M: Close over the HUD's Map button, measured before the tools are put away
    this.open = true; this.rush = false; this.moving = false; this.busy = true; this.over = this.focused = null;
    g.busy++;
    g.clock.paused = true;
    g.stage.classList.add("paused");
    g.ui.hover(null); g.ui.edge = null; g.ui.arrow(null);
    g.ui.refresh();
    clearTimeout(g.ui._toast); g.ui.toastEl.classList.remove("show");      // (a note from the game would lie over the dial)
    this.el.hidden = false;
    this.el.style.opacity = 0;
    this.timerEl.style.display = "none";
    for (const el of [this.sheetsEl, this.bandEl, this.labelEl, this.el.querySelector(".atlas-close")]) el.style.opacity = "";
  }
  /** MAP-15M: Close lies exactly over the HUD's Map button (measured as the map comes up, before the tools are put away),
      so that a second click where the map was opened puts it away again, as a toggle does, and the pointer is never left
      on a chip as the map comes up. Where the Map button is not to be seen, Close keeps its own place (css/game.css). */
  placeClose() {
    const close = this.el && this.el.querySelector(".atlas-close"), button = document.getElementById("t-map");
    if (!close) return;
    for (const p of ["left", "top", "width", "height", "right"]) close.style[p] = "";
    const r = button && button.offsetParent ? button.getBoundingClientRect() : null, st = this.g.stage.getBoundingClientRect();
    if (!r || !r.width || !st.width) return;
    const cq = (px) => `${(px / st.width) * 100}cqw`;
    Object.assign(close.style, { left: cq(r.left - st.left), top: cq(r.top - st.top), width: cq(r.width), height: cq(r.height), right: "auto" });
  }
  /** And goes away again: the world goes on where it stopped. */
  exit() {
    const g = this.g;
    if (!this.open) return;
    this.open = false; this.mode = this.target = null; this.moving = this.busy = false;
    this.wasMusic = undefined;                                                 // ENGINE-19B (6)
    this.el.hidden = true;
    this.sheetsEl.innerHTML = ""; this.shown = null; this._rows = {};
    g.busy = Math.max(0, g.busy - 1);
    if (!g.ui.open) { g.clock.paused = false; g.stage.classList.remove("paused"); }
    g.ui.refresh();
  }

  /** The Map button, or M: the map of the place the lead stands in (or, given its id, another one). True if it came up. */
  async show(mapId = null) {
    const g = this.g, own = this.own();
    if (this.open || !this.el || !own || g.mode !== "play" || g.busy || g.ui.open || g.dialogue.choosing) return false;
    this.enter();
    this.mode = "map";
    g.sfx("rustle");
    const id = mapId && this.maps[mapId] ? mapId : own.id;
    await this.draw(id);
    this.band(id);
    await this.tween(200, (k) => { this.el.style.opacity = k; });
    this.busy = false;
    this.focusFirst();
    this.say();
    return true;
  }

  /** Esc, M or Close: the map is put away, and nothing has changed. */
  async close() {
    if (!this.open || this.busy || this.moving) return;
    this.busy = true;
    this.g.sfx("rustle");
    if (this.wasMusic !== undefined) { const was = this.wasMusic; this.wasMusic = undefined; this.g.music(was); }      // ENGINE-19B (6): back to the time it was
    await this.tween(180, (k) => { this.el.style.opacity = 1 - k; });
    this.exit();
  }

  /** Switching to a lead in another scene (game.js switchLead): their map, their portrait breathing; first, when their scene
      is in another time, the Timer turning from the active lead's notch to theirs. A click on them (or Enter) drops into
      their scene (pick); Esc goes back, and nothing has changed. True if the map came up. */
  async switchTo(lead) {
    const g = this.g, at = g.store.data.where[lead], there = at && at.scene ? this.mapOf(at.scene) : null;
    if (!there || this.open || !this.el) return false;
    const era = g.here ? g.here.era : null, from = era && g.eras[era] ? g.eras[era].dial : null, to = this.stop(there.id);      // (ENGINE-17: the lead's own scene, g.here)
    this.enter();
    this.mode = "switch"; this.target = lead;
    // ENGINE-19B (6): sound first. Into another time, its track starts under the dial (the scene the lead stands in: its
    // music, or its era's), so the drop into it (pick) finds it playing; Esc (close) puts back the one that was playing.
    this.wasMusic = undefined;
    if (era !== there.map.era && g.audio.ready) {
      const scene = await g.getScene(at.scene).catch(() => null), m = scene && g.musicOf(scene), now = g.audio.current ? g.audio.current.id : null;
      if (m && m !== now && g.audio.has(m)) { this.wasMusic = now; g.music(m); }                   // (MUSIC-24: a recording, or a pattern)
    }
    if (era !== there.map.era && Number.isInteger(from) && Number.isInteger(to) && from !== to) await this.timer(from, to, there.id);
    else {                                                    // the same time, or two times on one notch (home and Nevada): no turn, a fade
      g.sfx("rustle");
      await this.draw(there.id);
      this.band(there.id);
      await this.tween(220, (k) => { this.el.style.opacity = k; });
    }
    this.busy = false;
    const face = this.el.querySelector(`button.atlas-face[data-lead="${lead}"]`);
    if (face) { this.focusOn(face); this.focused = { kind: "face", id: lead }; } else this.focusFirst();       // (Enter drops into their scene: the label line says so)
    this.say();
    return true;
  }

  /** The Timer: the dial, large, in the middle of the dark screen, comes in and turns notch by notch from one time to the
      other, a click at each notch and a small bell at the end; then it shrinks and rises into the small dial's place at the
      top of the map, as the map comes up under it. A click or a key hurries it. With less motion it does not turn: it is
      shown at the time it is going to, the bell, and a fade to the map. */
  async timer(from, to, mapId) {
    const g = this.g, T = this.timerEl, calm = g.calm, set = bigSet();
    const pics = await Promise.all(PIECES.map((n) => picture(set[n]).then((p) => p || (set[n] !== SMALL_SET[n] ? picture(SMALL_SET[n]) : null))));
    PIECES.forEach((n, i) => { T.querySelector("." + n).style.backgroundImage = pics[i] ? `url("${pics[i].src}")` : ""; });
    const bow = T.querySelector(".turn"), rest = [this.sheetsEl, this.bandEl, this.labelEl, this.el.querySelector(".atlas-close")];
    for (const el of rest) el.style.opacity = 0;              // (the map is drawn under the dark meanwhile, and waits)
    this.place(T, TIMER, 0.9);
    T.style.opacity = 0; T.style.display = "";
    bow.style.transform = `rotate(${angleOf(calm ? to : from)}deg)`;
    const drawing = this.draw(mapId).then(() => this.band(mapId));
    this.moving = true; this.rush = false;
    await this.tween(250, (k) => { this.el.style.opacity = Math.min(1, 1.6 * k); T.style.opacity = k; this.place(T, TIMER, 0.9 + 0.1 * k); });     // (the dark comes up a little ahead of the dial)
    this.el.style.opacity = 1;
    if (calm) g.sfx("ding");
    else await this.turn(bow, from, to);
    await drawing;
    if (calm) await this.tween(300, (k) => { T.style.opacity = 1 - k; for (const el of rest) el.style.opacity = k; }, linear);
    else {
      this.dialEl.style.visibility = "hidden";
      await this.tween(400, (k) => {
        this.place(T, { x: TIMER.x + (DIAL.x - TIMER.x) * k, y: TIMER.y + (DIAL.y - TIMER.y) * k, size: TIMER.size + (DIAL.size - TIMER.size) * k });
        for (const el of rest) el.style.opacity = k;
      }, easeOut);
      this.dialEl.style.visibility = "";
    }
    for (const el of rest) el.style.opacity = "";
    T.style.display = "none";
    this.moving = this.rush = false;
  }
  /** Put a dial at a box of the stage ({ x, y, size } in picture pixels), scaled about its middle. */
  place(el, { x, y, size }, scale = 1) {
    el.style.left = px(x); el.style.top = px(y); el.style.width = el.style.height = px(size);
    el.style.transform = scale === 1 ? "" : `scale(${scale})`;
  }
  /** Turn a dial's bow from one stop to another, notch by notch: each a snap of 0.12 s into the notch (to a tenth of a notch
      past it), a settle of 0.06 s back, and a hold of 0.08 s, with a click (`notch`) as it lands; the bell (`ding`) at the
      end. Hurried, it is at the end at once, with the bell. */
  async turn(bow, from, to) {
    const g = this.g, step = to > from ? 1 : -1;
    for (let s = from; s !== to && !this.rush; s += step) {
      const a0 = angleOf(s), a1 = angleOf(s + step), past = a1 + (a1 - a0) / 10;
      await this.tween(120, (k) => { bow.style.transform = `rotate(${a0 + (past - a0) * k}deg)`; }, easeIn);
      if (this.rush) break;
      g.sfx("notch");
      await this.tween(60, (k) => { bow.style.transform = `rotate(${past + (a1 - past) * k}deg)`; }, easeOut);
      await this.wait(80);
    }
    bow.style.transform = `rotate(${angleOf(to)}deg)`;
    g.sfx("ding");
  }

  /** A chip, the dial, or the Left and Right keys: the small dial turns from the shown map's time to the chosen one's,
      notch by notch (two maps on one notch: no turn, one click), and the sheet changes with a short cross-fade. */
  async turnTo(mapId) {
    const g = this.g;
    if (!this.open || this.moving || this.busy || !mapId || mapId === this.shown || !this.maps[mapId]) return;
    const from = this.stop(this.shown), to = this.stop(mapId), bow = this.dialEl.querySelector(".turn");
    this.moving = true; this.rush = false;
    const old = this.sheetsEl.querySelector(".atlas-sheet"), drawing = this.draw(mapId, { under: true });
    if (from === to) g.sfx("notch");
    else if (g.calm) { bow.style.transform = `rotate(${angleOf(to)}deg)`; g.sfx("ding"); }
    else await this.turn(bow, from, to);
    const fresh = await drawing;
    this.band(mapId);
    await this.tween(260, (k) => { fresh.style.opacity = k; if (old) old.style.opacity = 1 - k; });
    fresh.style.opacity = "";
    if (old) old.remove();
    this.moving = this.rush = false;
    this.say();
  }
  /** The next (1) or the previous (-1) map the player knows, round and round; null if they know only this one. */
  next(step) {
    const list = this.known(), i = list.indexOf(this.shown);
    return list.length > 1 ? list[(i + step + list.length) % list.length] : null;
  }

  // ---------- drawing a map ----------
  /** Build a map's sheet: the drawing (painted, or the sketch), the names, the places to click and the portraits. With
      `under`, the new sheet is put under the one showing, clear, for a cross-fade. Resolves with it, once every picture it
      shows has arrived. */
  async draw(mapId, { under = false } = {}) {
    const g = this.g, L = await this.layout(mapId), map = this.maps[mapId], own = this.own(), { visited, faint, entered, hidden } = this.stateOf(mapId);
    const shows = (pid) => (visited.has(pid) ? 1 : faint.has(pid) ? FAINT : 0);
    // (ENGINE-21: a way to a place not known yet is not drawn; a way with somebody on it, been to (the sea path while the family
    // is at sea, and after), is drawn whole)
    const onIt = (p) => Object.entries(map.places).some(([pid, pl]) => pl.on && entered.has(pid) && ((pl.on.a === p.a && pl.on.b === p.b) || (pl.on.a === p.b && pl.on.b === p.a)));
    const wayShows = (p) => (hidden.has(p.a) || hidden.has(p.b) ? 0 : (visited.has(p.a) && visited.has(p.b)) || onIt(p) ? 1 : visited.has(p.a) || visited.has(p.b) ? FAINT : 0);
    if (L.painted) await Promise.all(picturesOf(L).map((p) => picture(p)));      // here before it is shown, so nothing pops in
    const sheet = document.createElement("div");
    sheet.className = "atlas-sheet " + (L.painted ? "painted" : "sketch");
    sheet.dataset.map = mapId;
    if (L.painted) sheet.style.setProperty("--map-ink", L.label.color);      // MAP-15M: the map's own ink (its names' colour), for the outline under the pointer (css/game.css)
    let html = "", ink = "";
    // a sketch's sheet: the interface's own papyrus, torn along its fibres, in the sheet's box
    if (!L.painted) { const [l, t, r, b] = L.sheet; html += `<div class="atlas-paper" style="left:${px(l)};top:${px(t)};width:${px(r - l)};height:${px(b - t)}"><div></div></div>`; }
    // the drawing: the sheet, the ways, the places (each picture whole, at 1 or faint); the sketch: ways dashed, a box for each place
    const image = (path, o, attrs) => `<image ${attrs} href="${esc(url(path))}" x="0" y="0" width="800" height="600" preserveAspectRatio="none" opacity="${o}"/>`;
    const points = (list) => list.map((v) => v.join(",")).join(" ");
    // ENGINE-21: on a painted map, a place or a way not painted yet is a stand-in in the map's own ink (a box, a dashed line)
    const standin = `fill="none" stroke="${esc(L.label.color)}" stroke-width="2.4" stroke-dasharray="7 6" stroke-linecap="round"`;
    if (L.painted) ink += image(L.back, 1, `class="back"`);
    for (const p of L.paths) {
      const o = wayShows(p);
      if (o) ink += L.painted && p.picture ? image(p.picture, o, `class="way" data-way="${p.a}-${p.b}"`) : `<polyline class="way${p.standin ? " standin" : ""}" data-way="${p.a}-${p.b}" points="${points(p.via)}" opacity="${o}"${p.standin ? " " + standin : ""}/>`;
    }
    for (const [pid, p] of Object.entries(L.places)) {
      const o = p.onWay ? 0 : shows(pid);                                          // (ENGINE-21: a place on a way has nothing of its own to draw)
      if (o) ink += L.painted && p.picture ? image(p.picture, o, `class="site" data-place="${pid}"`)
        : `<polygon class="site${p.standin ? " standin" : ""}" data-place="${pid}" points="${points(p.shape)}" opacity="${o}"${p.standin ? ` fill="rgba(255,244,214,0.35)" stroke="${esc(L.label.color)}" stroke-width="2" stroke-linejoin="round"` : ""}/>`;
    }
    // ENGINE-21: the stops (a journey's pictures by the way): shown when the map says so (`shown`), or while a journey passes them
    // (drawn at 0 until the portraits come to them: journey); a stand-in is a small ring in the map's ink, with its name
    const j = this._journey && this._journey.map === mapId ? this._journey : null, lab = L.label;
    for (const [sid, s] of Object.entries(L.stops || {})) {
      const st = (map.stops || {})[sid], on = shownStop(st, g), passing = !!j && j.stops.includes(sid);
      if (!on && !passing) continue;
      const o = on ? 1 : 0;
      if (s.picture) ink += image(s.picture, o, `class="stop" data-stop="${sid}"`);
      else ink += `<g class="stop standin" data-stop="${sid}" opacity="${o}"><circle cx="${s.pin[0]}" cy="${s.pin[1]}" r="5" fill="${esc(lab.color)}"/>` +
        `<text x="${s.label[0]}" y="${s.label[1]}" text-anchor="middle" font-size="${Math.max(11, lab.size - 3)}" fill="${esc(lab.color)}"${lab.halo ? ` stroke="${esc(lab.halo)}" stroke-width="3" paint-order="stroke"` : ""}>${esc(st.label || sid)}</text></g>`;
    }
    // the names, in the game's own face, in the map's style: only where the player has been
    for (const pid of Object.keys(L.places)) {
      if (!visited.has(pid) || L.places[pid].onWay) continue;
      const p = L.places[pid], text = lab.upper ? map.places[pid].label.toUpperCase() : map.places[pid].label;
      const halo = lab.halo ? ` stroke="${esc(lab.halo)}" stroke-width="${(lab.size / 4).toFixed(2)}" stroke-linejoin="round" paint-order="stroke"` : "";
      ink += `<text class="name" data-place="${pid}" data-max="${p.label_max}" x="${p.label[0]}" y="${p.label[1]}" text-anchor="middle" font-size="${lab.size}" fill="${esc(lab.color)}" style="letter-spacing:${Number(lab.spacing) || 0}em"${halo}>${esc(text)}</text>`;
    }
    html += `<svg class="atlas-draw" viewBox="0 0 800 600" preserveAspectRatio="none" aria-hidden="true">${ink}</svg>`;
    // the places to click: a place visited on the lead's own map is a button; any other that shows says what it is
    const mine = !!own && own.id === mapId;
    let hot = "";
    for (const [pid, p] of Object.entries(L.places)) {
      if ((!visited.has(pid) && !faint.has(pid)) || p.onWay) continue;             // (ENGINE-21: a place on a way is not clicked: its portraits are)
      const button = mine && visited.has(pid);
      hot += `<polygon class="site${visited.has(pid) ? "" : " faint"}${button && !this.cannot(pid) ? " target" : ""}" data-place="${pid}" points="${points(p.shape)}"` +
        (button ? ` tabindex="0" role="button"` : ` role="img"`) + ` aria-label="${esc(this.placeText(mapId, pid))}"/>`;
    }
    html += `<svg class="atlas-hot" viewBox="0 0 800 600" preserveAspectRatio="none">${hot}</svg>`;
    html += `<div class="atlas-faces">${this.faces(mapId, L)}</div>`;
    sheet.innerHTML = html;
    if (under) { sheet.style.opacity = 0; this.sheetsEl.prepend(sheet); }
    else { this.sheetsEl.innerHTML = ""; this.sheetsEl.appendChild(sheet); }
    // a name wider than its box is drawn narrower, to fit it
    for (const t of sheet.querySelectorAll(".atlas-draw text.name")) {
      try { const max = Number(t.dataset.max), w = t.getComputedTextLength(); if (max && w > max) { t.setAttribute("textLength", max); t.setAttribute("lengthAdjust", "spacingAndGlyphs"); } } catch { /* not laid out: as it is */ }
    }
    this.shown = mapId;
    this.sizeFaces();
    return sheet;
  }

  /** The portraits on a map, as markup: at each place, a row of discs centred on its pin (the team's 36 across, anyone
      else's 28, 4 apart). The team's are buttons, and the one being played has a ring in their colour; in a switch, the
      one being switched to breathes. Each row is kept (`rows`), for the walk and for tests. */
  faces(mapId, L) {
    const all = this.facesOn(mapId), out = [];
    this.rows = {};
    for (const pid of Object.keys(L.places)) {
      const row = all.filter((f) => f.place === pid);
      if (!row.length) continue;
      const sizes = row.map((f) => (f.team ? DISC : SMALL)), wide = sizes.reduce((a, b) => a + b, 0) + GAP * (row.length - 1);
      const y = L.places[pid].pin[1];
      let x = L.places[pid].pin[0] - wide / 2;
      this.rows[pid] = row.map((f, n) => {
        const s = sizes[n], cx = x + s / 2, cls = `atlas-face${f.team ? "" : " other"}${f.active ? " on" : ""}${this.mode === "switch" && f.id === this.target ? " pulse" : ""}`;
        const style = `left:${px(cx - s / 2)};top:${px(y - s / 2)};width:${px(s)};height:${px(s)};--who:${esc(this.g.cast[f.id].color)}`, text = esc(this.faceText(f));
        out.push(f.team
          ? `<button class="${cls}" type="button" data-lead="${esc(f.id)}" aria-label="${text}" style="${style}"><img alt="" draggable="false"></button>`
          : `<span class="${cls}" role="img" data-lead="${esc(f.id)}" aria-label="${text}" style="${style}"><img alt="" draggable="false"></span>`);
        x += s + GAP;
        return { id: f.id, cx, cy: y, size: s, team: f.team };
      });
    }
    return out.join("");
  }
  /** The portraits are pixel art drawn for the pixels they are shown at, as the team bar's are (ui.js, sizeFaces). */
  sizeFaces() {
    const dpr = window.devicePixelRatio || 1;
    for (const img of this.el.querySelectorAll(".atlas-face img")) {
      const box = img.parentElement, w = box.clientWidth, id = box.dataset.lead;
      if (!(w > 0) || !this.g.cast[id]) continue;
      let css = Math.floor(w);
      for (let c = css; c > css - 4 && c > 0; c--) if (Math.abs(c * dpr - Math.round(c * dpr)) < 0.01) { css = c; break; }
      const want = Math.max(16, Math.round(css * dpr)), key = this.g.ui.faceKey(id, want);
      if (img.dataset.key === key || !this.g.ui.faces[key]) continue;
      img.src = this.g.ui.faces[key];
      img.dataset.key = key;
      img.style.width = img.style.height = (want === Math.round(css * dpr) ? css : want / dpr) + "px";
    }
  }

  /** The band at the top: the time and its date, the chips of the maps the player knows, and the small dial at the time's notch. */
  band(mapId) {
    const era = this.era(mapId), list = this.known();
    if (!list.includes(mapId)) list.push(mapId);
    this.whenEl.querySelector("b").textContent = era.name;
    this.whenEl.querySelector("span").textContent = this.g.dateOf(era);      // (MERGE-20: dateOf: Act Six's year shows once #21 is solved)
    this.el.setAttribute("aria-label", `Map: ${era.name}`);
    const had = this.chipsEl.contains(document.activeElement);          // (the keyboard on a chip stays on the chips: on the one now pressed)
    this.chipsEl.innerHTML = list.map((id) => `<button class="tool" type="button" data-act="chip" data-map="${esc(id)}" aria-pressed="${id === mapId}" aria-label="${esc(this.chipText(id))}">${esc(this.maps[id].name)}</button>`).join("");
    if (had) this.focusOn(this.chipsEl.querySelector(`[data-map="${mapId}"]`));
    this.dialEl.querySelector(".turn").style.transform = `rotate(${angleOf(this.stop(mapId) ?? 0)}deg)`;
    for (const n of PIECES) this.dialEl.querySelector("." + n).style.backgroundImage = `url("${url(SMALL_SET[n])}")`;
  }

  // ---------- the label line ----------
  /** A chip's words: "Rome, 44 B.C." */
  chipText(id) { const era = this.era(id), date = this.g.dateOf(era); return era.name + (date ? ", " + date.replace(/^The\b/, "the") : ""); }      // (MERGE-20: dateOf)
  faceText(f) {
    const name = this.g.cast[f.id].name;
    if (!f.team) return `${name} is here. Not playable just now.`;
    return f.active ? `${name}, playing now` : `Play as ${name}`;
  }
  /** What a place says, and what a click on it does: "Go to the Forum", "The Forum: you are here", "The Forum. Not from
      here.", on another map "The Forum", and a faint one "Somewhere you haven't been yet". */
  placeText(mapId, pid) {
    const place = this.maps[mapId].places[pid], own = this.own();
    if (!this.stateOf(mapId).visited.has(pid)) return "Somewhere you haven't been yet";
    if (!own || own.id !== mapId) return place.label;
    if (pid === own.place) return `${place.label}: you are here`;
    { const lm = this.landmarkSays(mapId, pid); if (lm) return lm.pictures ? `${place.label}. (${lm.pictures.join(", ")})` : lm.text.startsWith(place.label) ? lm.text : `${place.label}. ${lm.text}`; }      // (SCENES-17: a landmark's own words)
    { const far = this.farSays(mapId, pid); if (far) return `${place.label}. ${far.pictures ? `(${far.pictures.join(", ")})` : far.text}`; }      // (ENGINE-20: a place of another leg: its own words)
    if (!this.may()) { const r = this.refused(); return `${place.label}. ${r.pictures ? `(${r.pictures.join(", ")})` : r.text}`; }      // (ENGINE-17: the scene's or the place's own words, if it names a line)
    if (!this.route(mapId, own.place, pid)) return place.label;
    return "Go " + (place.go || "to " + afterTo(place.label));
  }
  /** ENGINE-17: what the label line shows over a place: placeText's words; or, refused by a line that is a thought, the place's
      name and the pictures. */
  placeSay(mapId, pid) {
    const own = this.own(), place = this.maps[mapId].places[pid];
    if (own && own.id === mapId && pid !== own.place && this.stateOf(mapId).visited.has(pid)) {      // (SCENES-17: a landmark's own thought first)
      const lm = this.landmarkSays(mapId, pid);
      if (lm && lm.pictures) return { text: `${place.label}. `, pictures: lm.pictures };
      const far = !lm && this.farSays(mapId, pid);                                 // (ENGINE-20: a far place's, if it is a thought)
      if (far && far.pictures) return { text: `${place.label}. `, pictures: far.pictures };
    }
    if (own && own.id === mapId && pid !== own.place && this.stateOf(mapId).visited.has(pid) && !this.may()) {
      const r = this.refused();
      if (r.pictures) return { text: `${place.label}. `, pictures: r.pictures };
    }
    return this.placeText(mapId, pid);
  }
  /** ENGINE-17: the label line shows words, or { text, pictures }: the words and then the thought's pictures. */
  write(what) {
    const el = this.labelEl;
    if (what && typeof what === "object") {
      const pics = what.pictures || [];
      el.textContent = what.text || "";
      for (const n of pics) el.appendChild(Object.assign(document.createElement("img"), { src: thoughtURL(n), alt: n, className: "pic" }));
      el.setAttribute("aria-label", `${what.text || ""}${pics.length ? `(a thought: ${pics.join(", ")})` : ""}`);
    } else { el.textContent = what; el.removeAttribute("aria-label"); }
  }
  /** What a thing on the map screen is: { kind, id } for a place, a portrait, a chip, the dial or Close; or null. */
  whatIs(el) {
    const hit = el && el.closest ? el.closest("[data-lead], .atlas-hot [data-place], [data-act]") : null;
    if (!hit || !this.el.contains(hit)) return null;
    if (hit.dataset.lead) return { kind: "face", id: hit.dataset.lead };
    if (hit.dataset.place) return { kind: "place", id: hit.dataset.place };
    if (hit.dataset.act === "chip") return { kind: "chip", id: hit.dataset.map };
    return { kind: hit.dataset.act };
  }
  /** The label line: what the pointer is on, or the focus; with nothing, what can be done here (hint). */
  say(text = null) {
    if (!this.open || !this.labelEl) return;
    const mapId = this.shown, here = (x) => x && mapId && (x.kind === "place" ? !!this.maps[mapId].places[x.id] : x.kind !== "face" || !!this.el.querySelector(`.atlas-face[data-lead="${x.id}"]`));
    const it = [this.over, this.focused].find(here);                    // (what was pointed at on a map turned away from is not there any more)
    if (text == null && it && mapId) {
      if (it.kind === "place") text = this.placeSay(mapId, it.id);                                // (ENGINE-17: placeSay, for a refusal that is a thought)
      else if (it.kind === "face") { const f = this.facesOn(mapId).find((x) => x.id === it.id); text = f ? this.faceText(f) : null; }
      else if (it.kind === "chip") text = this.chipText(it.id);
      else if (it.kind === "dial") text = "Turn the dial";
      else if (it.kind === "close") text = "Back to the game (Esc)";
    }
    this.write(text == null ? this.hint() : text);                    // (ENGINE-17: write, for words or a thought's pictures)
  }
  /** With nothing under the pointer: on the lead's own map, what a click on a place does (if the scene lets them leave by
      the map, and there is a place they can go: MAP-15M), and, if anyone else of the team is on the map, what a click on them does. */
  hint() {
    if (!this.shown) return "";
    const d = this.g.store.data, own = this.own(), parts = [];
    if (own && own.id === this.shown && Object.keys(own.map.places).some((pid) => !this.cannot(pid))) parts.push("Click a place you have been to go there.");     // MAP-15M: only when there is somewhere to go (not at an act's first place, nor where the scene keeps the lead)
    if (this.facesOn(this.shown).some((f) => f.team && f.id !== d.active)) parts.push("Click someone to play as them.");
    return parts.join(" ");
  }

  // ---------- doing things ----------
  onClick(event) {
    if (!this.open || this.moving || this.busy || this.mode === "journey") return;      // (ENGINE-20: a journey takes no clicks but to hurry it)
    const it = this.whatIs(event.target);
    if (!it) return;
    if (event.detail && it.kind !== "close" && document.activeElement && document.activeElement.blur) document.activeElement.blur();     // (a mouse click leaves no focus ring behind)
    if (it.kind === "close") this.close();
    else if (it.kind === "chip") this.turnTo(it.id);
    else if (it.kind === "dial") { const n = this.next(1); if (n) this.turnTo(n); else this.g.sfx("notch"); }
    else if (it.kind === "place") this.go(it.id);
    else if (it.kind === "face") this.pick(it.id);
  }
  /** A click on a place: on the lead's own map, travel there if it can be travelled to; if the scene will not let them
      leave by the map, the label line says so ("Not from here."), and nothing else happens. */
  go(pid) {
    const own = this.own();
    if (!own || this.shown !== own.id || pid === own.place || !this.stateOf(own.id).visited.has(pid)) return;
    { const lm = this.landmarkSays(own.id, pid); if (lm) { this.say(lm.pictures ? lm : lm.text); return; } }      // (SCENES-17: a landmark says its own words, whoever clicks it)
    { const far = this.farSays(own.id, pid); if (far) { this.say(far.pictures ? { text: `${own.map.places[pid].label}. `, pictures: far.pictures } : `${own.map.places[pid].label}. ${far.text}`); return; } }      // (ENGINE-20: a place of another leg refuses with its own line)
    if (!this.may()) { const r = this.refused(); this.say(r.pictures ? r : r.text); return; }      // (ENGINE-17: the scene's or the place's own words, if it names a line)
    if (!this.cannot(pid)) this.travel(pid);
  }
  /** A click on a portrait of the team (or a number key): play as them. Standing in the scene on the stage, the controls
      change hands at once; anywhere else, the map fades out to the dark and the game drops into their scene (game.js
      dropInto), where they stand. */
  async pick(lead) {
    const g = this.g, d = g.store.data, at = d.where[lead];
    if (!this.open || this.busy || this.moving || !d.team.includes(lead) || lead === d.active || !at || !at.scene) return;
    this.busy = true;
    if (g.scene && at.scene === g.scene.id && g.actor(lead)) {
      if (this.wasMusic !== undefined) g.music(g.musicOf(g.scene));            // ENGINE-19B (6): staying in this time after all
      await this.tween(160, (k) => { this.el.style.opacity = 1 - k; });
      this.exit();
      await g.switchLead(lead);
      return;
    }
    g.sfx("rustle");
    await this.blackout();
    this.exit();
    await g.dropInto(lead);
  }

  /**
   * Travel: the active lead goes to a place of their own map, as a click on it does. Their portrait (with their party's)
   * walks along the ways drawn on the map, the fewest through places already visited, a soft click at each place passed
   * through; the map fades out to the dark; and the game goes to the place's first scene, arriving on the mark of the
   * last way as if they had walked in from the place before it (the scene its `enter` is told they came from). The party
   * comes along, as by any way out, and the game saves. It resolves when the new scene is up: true; or at once false, with
   * nothing done, if it may not be (and, called by a script, the console says why). Opens the map first if it is not up.
   */
  async travel(pid, { script = false } = {}) {
    const g = this.g;
    const why = this.cannot(pid) || (this.open ? (this.moving || this.busy ? "the map is busy" : null) : g.mode !== "play" || g.busy || g.ui.open ? "the game is busy" : null);
    if (why) { if (script) console.warn(`g.travel("${pid}"): ${why}, so nothing happens.`); return false; }
    const own = this.own();
    if (!this.open && !(await this.show(own.id))) return false;
    if (this.shown !== own.id) await this.turnTo(own.id);
    const route = this.route(own.id, own.place, pid);
    if (!route || !this.open) return false;
    this.busy = true;
    await this.walk(own.id, route);
    const last = route.ways[route.ways.length - 1], before = route.places[route.places.length - 2];
    const spawn = this.markOf(last, pid), came = own.map.places[before].scenes[0], to = own.map.places[pid].scenes[0];
    g.sfx("rustle");
    await this.blackout();
    this.exit();
    if (g.lead && g.lead._stop) g.lead._stop();
    g._leaving = null;
    await g.run(() => g.goto(to, { via: "map", spawn, came }), { settle: false });
    g.autosave();
    return !!g.scene && g.scene.id === to;
  }

  /** The walk along the ways on the map: the lead's portrait, and those of the party standing with them, together; at
      about 220 pixels a second, the whole trip never more than 2.5 seconds, a soft click at each place passed through.
      With less motion they are where they are going at once. A click or a key hurries it. */
  async walk(mapId, route) {
    const g = this.g, d = g.store.data, L = await this.layout(mapId), scene = g.here;      // (ENGINE-17: the lead's own scene)
    const party = new Set([d.active, ...(((typeof scene.party === "function" ? scene.party(g) : scene.party) || [])
      .filter((id) => d.team.includes(id) && d.where[id] && d.where[id].scene === scene.id))]);
    const movers = ((this.rows || {})[route.places[0]] || []).filter((r) => party.has(r.id));
    // the line walked: each way's via, turned round where it is walked from b to a; and where it passes a place
    const line = [], passing = [];
    route.ways.forEach((way, n) => {
      const via = L.paths.find((p) => p.a === way.a && p.b === way.b).via, pts = way.a === route.places[n] ? via : [...via].reverse();
      for (const p of line.length ? pts.slice(1) : pts) line.push(p);
      if (n < route.ways.length - 1) passing.push(line.length - 1);
    });
    await this.walkLine(movers, line, passing, { speed: SPEED, longest: LONGEST });
  }
  /** ENGINE-20: the portraits (`movers`: rows of faces(), the ones who go) along a line of points of the map, a soft click at
      each index in `passing`, at `speed` pixels a second and never longer than `longest` (or exactly `ms`); the last point at
      once with less motion. A click or a key hurries it. (The walk of travel, taken out of walk() so that a journey can use it.) */
  async walkLine(movers, line, passing, { speed = SPEED, longest = LONGEST, ms = null } = {}) {
    const g = this.g;
    this.walked = [];
    if (!movers.length || line.length < 2) return;
    const mid = movers.reduce((a, r) => a + r.cx, 0) / movers.length, y0 = movers[0].cy;
    const els = movers.map((r) => ({ r, el: this.el.querySelector(`.atlas-face[data-lead="${r.id}"]`) })).filter((m) => m.el);
    const lens = [0];
    for (let i = 1; i < line.length; i++) lens.push(lens[i - 1] + Math.hypot(line[i][0] - line[i - 1][0], line[i][1] - line[i - 1][1]));
    const total = lens[lens.length - 1];
    const at = (s) => {
      let i = 1;
      while (i < lens.length - 1 && lens[i] < s) i++;
      const k = lens[i] > lens[i - 1] ? Math.min(1, Math.max(0, (s - lens[i - 1]) / (lens[i] - lens[i - 1]))) : 1;
      return [line[i - 1][0] + (line[i][0] - line[i - 1][0]) * k, line[i - 1][1] + (line[i][1] - line[i - 1][1]) * k];
    };
    const put = ([x, y]) => {
      this.walked.push([x, y]);
      for (const { r, el } of els) { el.style.left = px(x + (r.cx - mid) - r.size / 2); el.style.top = px(y + (r.cy - y0) - r.size / 2); }
    };
    for (const { el } of els) el.classList.add("walking");
    if (g.calm || total <= 0 || g.clock.skipping) { put(line[line.length - 1]); return; }
    this.moving = true; this.rush = false;
    const took = ms != null ? ms : Math.min(longest, (total / speed) * 1000), marks = passing.map((i) => lens[i]);
    let next = 0;
    await this.tween(took, (k) => {
      const s = total * k;
      put(at(s));
      for (; next < marks.length && s >= marks[next]; next++) if (!this.rush) g.sfx("notch");
    }, linear);
    put(line[line.length - 1]);
    this.moving = this.rush = false;
  }

  /**
   * ENGINE-20: a journey shown on the map, for a cut-scene (the voyage down the coast; the walk to Himeji):
   *     await g.journey("edo", "yui", "hills", { via: ["osaka"], sound: "creak" })
   * The map comes up (a rustle), with the place the journey starts from, the places it passes and the place it goes to drawn
   * in and named (whether or not the player has been there yet: the journey is how they get there), and the team's portraits
   * at the first place (the one being played and the rest of the team: `who` names others); they go along the path, a soft
   * click at each place passed (`via`: the ids of the places between, in order); the map fades out to the dark; it is put
   * away; and the cut-scene goes on (its goto finds the stage dark: `via: "map"` or "cut"). The path is each hop's way on the
   * map (`via` in the painters' layout, turned round where it is gone along from its far end; a straight line between the pins
   * where the map has no way), or `path`, a list of points of the map given outright. `ms` is how long the whole trip takes
   * (3200; a slow journey, slower than travel's walk); `sound` a sound played as it starts (the ship's timbers: `creak`; the
   * road: `sandals`), none if not said. Resolves true when it has been shown; false at once, and nothing done, with no such
   * map or place, with the map up already, or while the cut-scene is skipped (the console says why, but for skipping). With
   * less motion the portraits are at the far end at once. Nothing of it is saved: the scene the cut-scene goes to next is.
   */
  async journey(mapId, from, to, { via = [], path = null, ms = 3200, sound = null, who = null, stops = [], segments = null } = {}) {
    const g = this.g, d = g.store.data, map = this.maps[mapId];
    // ENGINE-21: `stops` (ids of the map's stops, or { id, line, ms }: a picture by the way, and a line said over it as the portraits
    // come to it), and `segments` ([{ to, sound, ms, stops }]: the journey in parts, each to a place or a stop on the line, with a
    // sound and a pace of its own: the river path, then the road). A place may be a point of a way (`on`: the family at sea).
    const segs = Array.isArray(segments) && segments.length ? segments : null;
    const stopIds = [...(stops || []), ...(segs ? segs.flatMap((s) => s.stops || []) : [])].map((s) => (typeof s === "string" ? s : s && s.id));
    const ends = segs ? segs.map((s) => s.to).filter((t) => t != null && t !== to) : [];
    const known = (pid) => !!(map && (map.places[pid] || (map.stops || {})[pid]));
    const why = !map ? `no map called "${mapId}"` : ![from, to, ...via].every((pid) => map.places[pid]) ? `"${[from, to, ...via].find((pid) => !map.places[pid])}" is not a place of the map "${mapId}"`
      : !stopIds.every((sid) => (map.stops || {})[sid]) ? `"${stopIds.find((sid) => !(map.stops || {})[sid])}" is not a stop of the map "${mapId}"`
      : !ends.every(known) ? `the segment's end "${ends.find((t) => !known(t))}" is not a place or a stop of the map "${mapId}"`
      : this.open ? "the map is up already" : !this.el ? "there is no map layer" : null;
    if (why) { console.warn(`g.journey("${mapId}", "${from}", "${to}"): ${why}, so nothing happens.`); return false; }
    if (g.clock.skipping) return false;
    const ids = [d.active, ...(Array.isArray(who) ? who : d.team)].filter((id, i, all) => g.leads.includes(id) && all.indexOf(id) === i);
    const places = [from, ...via, to];
    this._journey = { map: mapId, from, to, places, ids, stops: stopIds, said: [] };
    this.journeyed = { stops: [], segments: [], said: [] };                     // (ENGINE-21: what the last journey did, for tests)
    try {
      this.enter();
      this.mode = "journey";
      g.sfx("rustle");
      const L = await this.layout(mapId);
      await this.draw(mapId);
      this.band(mapId);
      // (ENGINE-21: from a stage already dark, a cut-scene's fade or the last journey's end, the dark lifts off the map)
      if (Number(g.fadeEl.style.opacity) > 0.5) { this.el.style.opacity = 1; await this.tween(260, (k) => { g.fadeEl.style.opacity = 1 - k; }, linear); g.fadeEl.style.opacity = 0; g._fade = 0; }
      else await this.tween(220, (k) => { this.el.style.opacity = k; });
      this.busy = false;
      // the line: the given points, or each hop's way (its via, turned round as needed; ENGINE-21: from or to a place on a way, the
      // part of that way's line), else straight between the pins
      let line = [], passing = [];
      if (Array.isArray(path) && path.length >= 2) line = path.filter((p) => Array.isArray(p) && p.length === 2);
      else for (let n = 0; n < places.length - 1; n++) {
        const pts = this.hop(map, L, places[n], places[n + 1]);
        for (const p of line.length ? pts.slice(1) : pts) line.push(p);
        if (n < places.length - 2) passing.push(line.length - 1);
      }
      const lens = lensOf(line), total = lens[lens.length - 1] || 0;
      const movers = ((this.rows || {})[from] || []).filter((r) => ids.includes(r.id));
      // ENGINE-21: the parts: each segment's end, and each stop, as a distance along the line (in order, each after the last)
      const pinOf = (id) => (L.places[id] ? L.places[id].pin : L.stops && L.stops[id] ? L.stops[id].pin : null);
      const plan = segs || [{ to, sound, ms, stops }];
      let s = 0;
      const parts = plan.map((seg, n) => {
        const last = n === plan.length - 1, end = last || seg.to == null || seg.to === to ? total : nearestS(line, lens, pinOf(seg.to) || line[line.length - 1], s);
        const st = (seg.stops || []).map((x) => (typeof x === "string" ? { id: x } : x)).map((x) => ({ ...x, at: nearestS(line, lens, pinOf(x.id), s) })).sort((a, b) => a.at - b.at);
        const part = { from: s, to: Math.max(s, end), sound: seg.sound ?? (segs ? null : sound), ms: seg.ms, stops: st };
        s = part.to;
        return part;
      });
      const marks = passing.map((i) => lens[i]);
      const share = (a, b) => (total > 0 ? ((b - a) / total) * ms : 0);
      this.walked = [];
      for (const part of parts) {
        if (part.sound) g.sfx(part.sound);
        this.journeyed.segments.push({ from: Math.round(part.from), to: Math.round(part.to), sound: part.sound || null });
        const long = part.ms != null ? part.ms : share(part.from, part.to), span = part.to - part.from || 1;
        let at = part.from;
        for (const stop of [...part.stops, null]) {
          const end = stop ? stop.at : part.to;
          await this.walkSpan(movers, line, lens, at, end, marks, (long * (end - at)) / span);
          at = end;
          if (stop) await this.atStop(mapId, L, stop);
        }
      }
      await this.wait(260);
      g.sfx("rustle");
      await this.blackout();
    } finally {
      this._journey = null;
      this.sayOn(null);
      this.exit();
    }
    return true;
  }
  /** ENGINE-21: one hop of a journey's line, from a place to the next: the way between them (turned round as needed); from or to a
      place that is a point of a way (`on`: at sea), the part of that way's line between it and the other end; else straight. */
  hop(map, L, a, b) {
    const pa = map.places[a], pb = map.places[b], pin = (pid) => L.places[pid].pin;
    const whole = wayLine(L, a, b);
    if (whole) return whole;
    const part = (onP, end, from) => {                                            // the line of the way `onP` is on, from it to `end` (or back)
      const o = map.places[onP].on, line = wayLine(L, o.a, o.b);
      if (!line || (end !== o.a && end !== o.b)) return null;
      const lens = lensOf(line), s = nearestS(line, lens, pin(onP)), e = end === o.a ? 0 : lens[lens.length - 1];
      return from ? cutLine(line, lens, s, e) : cutLine(line, lens, e, s);
    };
    if (pa && pa.on) { const p = part(a, b, true); if (p) return p; }
    if (pb && pb.on) { const p = part(b, a, false); if (p) return p; }
    if (pa && pb && pa.on && pb.on && pa.on.a === pb.on.a && pa.on.b === pb.on.b) {      // two points of one way
      const line = wayLine(L, pa.on.a, pa.on.b), lens = lensOf(line);
      return cutLine(line, lens, nearestS(line, lens, pin(a)), nearestS(line, lens, pin(b)));
    }
    return [pin(a), pin(b)];
  }
  /** ENGINE-21: the portraits along a line from one distance to another over `ms` (a click at each place passed, `marks`); at once
      with less motion; a click or a key hurries the walk to the end of this span (the next stop's line is still said). */
  async walkSpan(movers, line, lens, s0, s1, marks, ms) {
    const g = this.g;
    this.walked = this.walked || [];
    if (!movers.length || s1 <= s0) return;
    const mid = movers.reduce((a, r) => a + r.cx, 0) / movers.length, y0 = movers[0].cy;
    const els = movers.map((r) => ({ r, el: this.el.querySelector(`.atlas-face[data-lead="${r.id}"]`) })).filter((m) => m.el);
    const put = ([x, y]) => { this.walked.push([x, y]); for (const { r, el } of els) { el.style.left = px(x + (r.cx - mid) - r.size / 2); el.style.top = px(y + (r.cy - y0) - r.size / 2); } };
    for (const { el } of els) el.classList.add("walking");
    if (g.calm || g.clock.skipping) { put(pointAt(line, lens, s1)); return; }
    this.moving = true; this.rush = false;
    put(pointAt(line, lens, s0));                                                // (where they are as it begins: the span's start)
    const ahead = marks.filter((m) => m > s0 && m <= s1);
    let next = 0;
    await this.tween(Math.max(0, ms), (k) => {
      const s = s0 + (s1 - s0) * k;
      put(pointAt(line, lens, s));
      for (; next < ahead.length && s >= ahead[next]; next++) if (!this.rush) g.sfx("notch");
    }, linear);
    put(pointAt(line, lens, s1));
    this.moving = this.rush = false;
  }
  /** ENGINE-21: the portraits have come to a stop: its picture comes in (if it was not on the map already), and its line is said
      over it, on the map (sayOn); then they go on. A stop's `line` is the map's (maps.js `stops`) unless the journey gives one. */
  async atStop(mapId, L, stop) {
    const map = this.maps[mapId], spec = (map.stops || {})[stop.id] || {}, s = (L.stops || {})[stop.id];
    const el = this.sheetsEl.querySelector(`[data-stop="${stop.id}"]`);
    this.journeyed.stops.push(stop.id);
    if (el && Number(el.getAttribute("opacity")) < 1) await this.tween(this.g.calm ? 0 : 360, (k) => el.setAttribute("opacity", k.toFixed(3)));
    const line = stop.line !== undefined ? stop.line : spec.line;
    // SCENES-21B: a stop's line may be a list (Suma's two: Mom's, then Big Sister's), each said over it in turn
    if (line) for (const id of [].concat(line)) await this.sayOn(id, s ? s.pin : null, { ms: stop.ms });
    else await this.wait(stop.ms ?? 500);
  }
  /**
   * ENGINE-21: a line said on the map screen itself (the words' own layer is under it, and the game clock is stopped while the map
   * is up): the words in the speaker's colour over a point of the map (a stop's picture), with the backing words on the stage have,
   * for as long as a line of that length stays (dialogue.js lineMs, the reader's rate), or until a click or a key; counted as seen.
   * A recorded voice is played as anywhere. sayOn(null) takes a line away. A line not in the lines files is said by nobody (the
   * console says so once) and the journey goes on.
   */
  async sayOn(id, at = null, { ms = null } = {}) {
    const g = this.g;
    if (this._sayEl) { this._sayEl.remove(); this._sayEl = null; }
    if (!id) return;
    const entry = g.lines[id];
    if (!entry) { this.once(`A journey's stop names the line "${id}", which is not in the lines files: nothing is said there.`); await this.wait(ms ?? 500); return; }
    const [who, text, thought] = entry;
    g.store.data.seenLines[id] = (g.store.data.seenLines[id] || 0) + 1;
    if (g.clock.skipping) return;
    const p = document.createElement("p"), [x, y] = at || [400, 300];
    p.className = "say atlas-say";
    p.dataset.line = id;
    p.style.color = (g.cast[who] || {}).color || "#fff";
    if (thought != null) {                                                       // a thought: its pictures, as the label line shows them
      const pics = thoughtNames(thought, `the line "${id}"`);
      for (const n of pics) p.appendChild(Object.assign(document.createElement("img"), { src: thoughtURL(n), alt: n, className: "pic" }));
      p.setAttribute("aria-label", `(a thought: ${pics.join(", ")})`);
      p.classList.add("thought-line");
    } else p.textContent = text;
    p.style.left = `${(Math.min(Math.max(x, 210), 590) / 800) * 100}%`;
    p.style.top = `${(Math.max(150, y - 18) / 600) * 100}%`;
    this.el.appendChild(p);
    this._sayEl = p;
    if (this._journey) this._journey.said.push(id);
    this.journeyed && this.journeyed.said.push(id);
    const voiced = g.settings.voices ? g.audio.voice(id) : null;
    const rate = textRate(g.settings.textSpeed), long = ms ?? lineMs(text.length, rate);
    this.rush = false; this.moving = true;                                        // (a click or a key ends the line, as it would on the stage)
    if (voiced) await Promise.race([voiced, this.wait(30000)]);
    else await this.wait(long);
    this.moving = this.rush = false;
    g.audio.stopVoice();
    if (this._sayEl === p) { p.remove(); this._sayEl = null; }
    await this.wait(120);
  }

  /** The map fades out to the dark: to the stage's own fade, which the scene that comes next fades in from. */
  async blackout() {
    const g = this.g, f = g.fadeEl, from = Number(f.style.opacity) || 0;
    f.style.background = "#000";
    await this.tween(300, (k) => { f.style.opacity = from + (1 - from) * k; }, linear);
    f.style.opacity = 1;
    g._fade = 1;
  }

  // ---------- keys ----------
  /** A key while the map is up (game.js gives it every key then: nothing else the game does with a key happens until the
      map is put away). Enter and Space act on the button with the focus, as anywhere. */
  key(event) {
    const key = event.key, g = this.g;
    if (this.moving) { if (!event.repeat) this.rush = true; if (key !== "Tab") event.preventDefault(); return; }
    if (this.busy || this.mode === "journey") { event.preventDefault(); return; }      // (ENGINE-20: a journey is put away by itself)
    if (key === "Escape" || key.toLowerCase() === "m") { event.preventDefault(); this.close(); }
    else if (key === "ArrowRight" || key === "ArrowLeft") { event.preventDefault(); const n = this.next(key === "ArrowRight" ? 1 : -1); if (n) this.turnTo(n); }
    else if (key >= "1" && key <= "9") { const to = g.ui.team()[Number(key) - 1]; if (to) this.pick(to); }
    else if ((key === "Enter" || key === " ") && document.activeElement && document.activeElement.matches && document.activeElement.matches(".atlas-hot [data-place]")) {
      event.preventDefault();                                        // (a place is a shape, not a button of the page's: Enter and Space are its click)
      this.go(document.activeElement.dataset.place);
    } else if (key === "Enter" && this.mode === "switch") {           // in a switch, Enter drops into the scene of the one breathing
      const on = document.activeElement, other = on && this.el.contains(on) && on.matches("button, [role=button]") && on.dataset.lead !== this.target;
      if (!other) { event.preventDefault(); this.pick(this.target); }
    } else if (key === "Tab") {                                      // the keyboard stays on the map while it is up
      const all = this.focusables();
      if (!all.length) return;
      const i = all.indexOf(document.activeElement);
      event.preventDefault();
      all[event.shiftKey ? (i <= 0 ? all.length - 1 : i - 1) : (i < 0 || i === all.length - 1 ? 0 : i + 1)].focus({ preventScroll: true });
    }
  }
  /** Everything on the map screen the keyboard reaches, in order: the chips, the dial, the places, the portraits, Close. */
  focusables() {
    const sheet = this.sheetsEl.lastElementChild, all = (q, within = this.el) => (within ? [...within.querySelectorAll(q)] : []);
    return [...all(".atlas-chips button"), this.dialEl, ...all(".atlas-hot [tabindex='0']", sheet), ...all("button.atlas-face", sheet), this.el.querySelector(".atlas-close")]
      .filter((e) => e && !e.disabled && e.getClientRects().length);
  }
  focusFirst() { const all = this.focusables(); if (all.length) this.focusOn(all[0]); }
  /** The map puts the focus somewhere itself (as it comes up), without the label line taking it for the player's. */
  focusOn(el) { this._placing = true; try { el.focus({ preventScroll: true }); } finally { this._placing = false; } }

  // ---------- the map's own timer (the game clock is stopped while the map is up) ----------
  /** Call step(k) as k goes from 0 to 1 over ms of real time, eased; at once to 1 when hurried (`rush`). */
  tween(ms, step, easing = smooth) {
    return new Promise((done) => {
      const t0 = performance.now();
      const frame = (now) => {
        const k = this.rush || ms <= 0 ? 1 : Math.min(1, (now - t0) / ms);
        step(easing(k));
        if (k >= 1) done(); else requestAnimationFrame(frame);
      };
      if (this.rush || ms <= 0) { step(easing(1)); done(); } else requestAnimationFrame(frame);
    });
  }
  wait(ms) { return this.tween(ms, () => {}); }
}

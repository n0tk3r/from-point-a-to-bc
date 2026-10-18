// What the Office's five scenes and its two cut-scenes share (SCENES-17: new in round seventeen; briefs/SCENES-17.md, and the
// design, briefs/out/office-hq-design.md, section 4). Not a scene (it is in no list of scenes): a module the scenes import,
// as the intro and the title import cutscenes/highway.js.
//
//   the heat         office.heat, the Comfortable Room's temperature: 72 until Ranger turns the fans off (#16), then, as the
//                    play time goes on, 77, and then 81. Worked out from the play time of #16 (office.acOffAt), so that it is
//                    the same in every scene and after any load; every scene's `tick` keeps the fact up to date.
//   who hears whom   Grandpa Joe hears Ranger when Ranger is in the Comfortable Room, or at the grille over it with the suits
//                    gone (S/work-17-write/ids.md, section 1): then a look of Ranger's (a thought) is followed by Joe's reading.
//   the stock        the Office's own stock replies (the scene field `stock`: Ranger's are thoughts here).
//   the speakers     the building talks by itself now and then (each scene's `announce`, from talk/office.js paNowAndThen).
//   now and then     what each place says by itself, a little at a time (talk/office.js nowAndThen): a scene's `chatter`.
//   where words go   for someone not on the stage (a voice through a vent, Houston on the intercom): each scene's `wordsAt`
//                    is a getter of its own, which a script may point somewhere else for a moment (WORDS.at).

import { scaleAt } from "../../engine/walk.js";
import { paNowAndThen } from "../talk/office.js";

export const BUILDING = "office";
export const who = (g) => g.store.data.active;
export const is = (g, fact) => !!g.flag(fact);
/** Has this line been said yet? (The engine counts every line it says.) */
export const heard = (g, id) => !!g.store.data.seenLines[id];

// ---------- the heat (#16, #17) ----------
export const COOL = 72, WARM = 77, HOT = 81;
// How long after the fans go off the room shows 77, and then 81, in play time (the game clock: it stops with the menu and
// the map, and runs faster in the tests). The painted thermostat has these three numbers (PAINT-17C): the heat steps
// between them, so that what Grandpa Joe reads off it and what the talk says always agree.
export const WARM_MS = 40000, HOT_MS = 130000;
/** The room's temperature now, by the story: 72 before #16; after it 77, and then 81. (A game whose fans are off with no
    time recorded, as a tester's address can make it, has been off a long while: 81.) */
export function heatNow(g) {
  if (!is(g, "office.acOff")) return COOL;
  const at = Number(g.flag("office.acOffAt"));
  if (!Number.isFinite(at)) return HOT;
  const t = (g.store.data.playMs || 0) - at;
  return t >= HOT_MS ? HOT : t >= WARM_MS ? WARM : COOL;
}
/** Keep the fact office.heat as heatNow says (each scene's tick: cheap, and a fact set only when it changes). */
export function keepHeat(g) {
  const h = heatNow(g);
  if (Number(g.flag("office.heat")) !== h) g.flag("office.heat", h);
}
export const heat = (g) => Number(g.flag("office.heat")) || heatNow(g);

// ---------- who is where, and who hears whom ----------
/** Is Ranger at that mark of the ducts (lying at a grille: `over-room` and so on), as g.where has him? */
export function rangerAt(g, mark) {
  const w = typeof g.where === "function" ? g.where("ranger") : null;
  return !!w && w.scene === "office-ducts" && w.mark === mark;
}
/** Is Ranger in that scene? */
export function rangerIn(g, scene) {
  const w = typeof g.where === "function" ? g.where("ranger") : null;
  return !!w && w.scene === scene;
}
/** Does Grandpa Joe hear Ranger now? In the Comfortable Room together, or Ranger at the grille over it and the suits gone. */
export function joeHears(g) {
  if (rangerIn(g, "office-room")) return true;
  return rangerAt(g, "over-room") && is(g, "office.alone");
}
/** Grandpa Joe is standing on the spare chair under the vent (office.onChair: the room's own fact). */
export const onChair = (g) => is(g, "office.onChair");
/** Ranger thinks (a line of his with pictures); and where Grandpa Joe can hear him, Joe says what he means (the line `<id>.joe`). */
export async function think(g, id, reading = id + ".joe") {
  await g.say(id);
  if (reading && g.lines[reading] && joeHears(g)) await g.say(reading);
}
/** A look of Ranger's, for a hotspot: his thought, and Joe's reading where Joe hears him. Listed lines for the checks. */
export const thought = (id, reading = id + ".joe") => Object.assign(async (g) => think(g, id, reading), { lines: [id, reading] });

// ---------- the Office's own stock replies (the scene field `stock`, SCENES-17's in js/engine/game.js) ----------
// Ranger's are thoughts here (no one by him to say what he means); Grandpa Joe's are the Office's first, then his own.
export const STOCK = {
  nope: { grandpajoe: ["office.nope.grandpajoe.1", "office.nope.grandpajoe.2", "office.nope.grandpajoe.3", "nope.grandpajoe.1", "nope.grandpajoe.2", "nope.grandpajoe.3"],
    ranger: ["office.nope.ranger.1", "office.nope.ranger.2", "office.nope.ranger.3"] },
  look: { grandpajoe: ["office.look.grandpajoe.1", "look.grandpajoe.1"], ranger: ["office.look.ranger.1"] },
  hint: { grandpajoe: ["office.hint.none.grandpajoe"], ranger: ["office.hint.none.ranger"] },
  see: { grandpajoe: { ranger: "office.see.grandpajoe.ranger" }, ranger: { grandpajoe: "office.see.ranger.grandpajoe" } },
  give: { grandpajoe: ["office.give.grandpajoe.1"], ranger: ["office.give.ranger.1"] },
};

// ---------- the building's speakers, now and then (each scene's `announce`) ----------
export const ANNOUNCE = { lines: (g) => paNowAndThen.filter((p) => !p.when || p.when(g)).map((p) => p.id), every: [70, 130] };

// ---------- where the words of someone not on the stage go ----------
// Each scene's `wordsAt` is a getter: `get wordsAt() { return WORDS.at || ...its own... }`. A script that wants a voice to
// come from somewhere else for a while (Going Down: the hall, under the HALL grille) sets WORDS.at, and puts it back.
export const WORDS = { at: null };

// ---------- the player has the controls and nothing is going on ----------
export function idle(g) {
  const lead = g.lead;
  return g.mode === "play" && !!g.scene && !g.busy && !g.dialogue.active && !g.dialogue.choosing && !g.near && !g.ui.open &&
    !(g.atlas && g.atlas.open) && !(lead && lead.walking) && !g.view.hotEl.classList.contains("reveal");
}

// ---------- now and then: what a place says by itself (talk/office.js nowAndThen) ----------
/**
 * A place's own talk, a little at a time: every so often, while the player has the controls and nothing is going on, one
 * exchange from `list` (a list of line ids, or { when, say }), the ones not heard yet first (as g.chat picks them). It holds
 * the controls while it is said, as any script does. Off while the people's own lives are off (`index.html?still`, the
 * tests), as their small movements are. A scene makes one, calls reset(g) in its `setup` and tick(g, dt) in its `tick`;
 * once(g) says the next one not heard yet at once (a look down through a grille), now(g) the next one at all (for tests).
 */
export function chatter(list, { first = [18, 26], every = [34, 52], when = () => true, voices = {} } = {}) {
  const st = { left: 0, n: 0, k: 0 };
  const span = ([a, b]) => (a + (b - a) * [0.5, 0.15, 0.85, 0.35, 0.65][st.k++ % 5]) * 1000;
  const open = (g) => list.filter((e) => !e.when || e.when(g));
  const lines = (e) => [].concat(e.say || e);
  const unheard = (g) => open(g).find((e) => !heard(g, lines(e)[0]));
  /** One exchange, line by line: a voice with a place of its own (`voices`: Houston in Jed's earpiece) is said there. */
  async function exchange(g, e) {
    for (const id of lines(e)) {
      const at = voices[(g.lines[id] || [])[0]];
      if (at) WORDS.at = typeof at === "function" ? at(g) : at;
      try { await g.say(id); } finally { if (at) WORDS.at = null; }
    }
  }
  async function say(g, e) { if (e) await g.run(() => exchange(g, e), { settle: false }); }
  return {
    list,
    reset() { st.left = span(first); },
    tick(g, dt) {
      if (!g.life || !g.life.enabled || !when(g) || !idle(g)) return;
      if ((st.left -= dt) > 0) return;
      st.left = span(every);
      const all = open(g);
      if (all.length) say(g, unheard(g) || all[st.n++ % all.length]);
    },
    /** The next exchange not yet heard, said now (inside a script: no run of its own). */
    async once(g) { if (!when(g)) return; const e = unheard(g); if (e) await exchange(g, e); },
    /** For tests: the next exchange, said now. */
    now(g) { const all = open(g); return say(g, unheard(g) || all[st.n++ % Math.max(1, all.length)]); },
  };
}

// ---------- people ----------
/** Someone becomes another figure of js/art/people.js (the same person at another moment), keeping his id, and his place
    and facing unless others are given; made if he is not on the stage at all (as backup.js swaps them). `scale`: his size
    (none: the depth's, at his feet). */
export function swap(g, id, kind, at = null, face = null, scale = null) {
  const cast = g.view.cast, old = cast.get(id);
  const [x, y] = at || (old ? [old.x, old.y] : [400, 500]);
  const yaw = face ?? (old ? old.yaw : "S");
  if (old && old.kind === kind && !at && face == null) return old;
  const hid = old ? old.hidden : false, op = old ? old.opacity : 1, base = old ? old.base : null;
  if (old && old.up && old.up.sprite) old.up.sprite = null;          // (a seat he got up out of stays where he left it)
  if (old && old._stop) old._stop();
  if (old) cast.remove(id);
  const s = scale ?? (g.scene ? scaleAt(g.scene, y) : 1);
  const f = cast.addFigure(id, kind, x, y, s).face(yaw);
  f.hidden = hid; f.opacity = op; f.base = base;
  return f;
}
/** Ranger wears his mirror shades for the rest of the game (#10): every scene puts them on him. */
export function shades(g) { const r = g.actor("ranger"); if (r && r.variant) r.variant("shades"); return r; }

/**
 * A look at another room for a moment, while the lead stays where he is (#19: the break room as Houston calls Jed): the
 * room's painting and its cut-outs as the facts have them, and the people named ({ id, kind, at, face }), put on the stage
 * as a cut-scene puts them; `play(g)` plays the moment; then the lead's own scene is built again, where he stood. (Its
 * `setup` runs again; not its `enter`: nobody has gone anywhere.)
 */
export async function cutAway(g, sceneId, people, play) {
  const d = g.store.data, here = g.scene, place = d.where[d.active];
  const there = await g.getScene(sceneId);
  g.rememberPlace();
  await g.fade(1, 260);
  g.view.clear();
  await g.view.show(there, g);
  for (const p of people) {
    const f = g.view.cast.addFigure(p.id, p.kind, p.at[0], p.at[1], p.scale ?? scaleAt(there, p.at[1])).face(p.face || "S");
    if (p.sit && f.sit) f.sit(true, true);
  }
  await g.view.cast.load();
  await g.fade(0, 260);
  try { await play(g); }
  finally {
    await g.fade(1, 260);
    await g.enterScene(here, place && place.x != null ? [place.x, place.y] : null);
    await g.fade(0, 300);
  }
}

/**
 * The game cuts to the other lead, as the story hands the controls over (the end of the receipt's journey: Grandpa Joe,
 * and Opal at his door). Like switching to him, but from inside a script (g.switchLead waits for the controls to be
 * free): the one being played is left where he is, the other is played where he was left, in his own scene. Nobody leaves
 * anywhere (`switching`), and there is no card (one building).
 */
export async function cutTo(g, to) {
  const d = g.store.data;
  if (d.active === to || !d.team.includes(to)) return false;
  g.rememberPlace();
  const old = g.lead;
  if (old && old._stop) old._stop();
  g.held = null;
  const place = d.where[to];
  if (!place || !place.scene) return false;
  d.active = to;
  g.sawHanded(to);
  await g.goto(place.scene, { via: "fade", at: place.x != null ? [place.x, place.y] : null, switching: true, card: false });
  return true;
}

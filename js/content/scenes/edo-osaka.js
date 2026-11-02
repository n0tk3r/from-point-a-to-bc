// SCENES-21B (round twenty-one): what Act Six's Osaka shares, the second leg of five (edo-dojima.js, the Dōjima shore;
// edo-street.js, Shinsaibashi-suji at a crossroads; edo-theatre.js, the Inari puppet theatre), and its cut-scene "The Kyoto
// Boat" (cutscenes/edo-boat.js). Not a scene (it is in no list of scenes): a module they import, as round twenty's scenes
// import edo-yui.js and edo-hills.js. The act's own shared pieces are edo-common.js's (the stock replies, LEG_START.osaka).
// The design is briefs/out/edo2-design.md, #28 to #31 and "Cut-Scene: The Kyoto Boat"; every line is WRITE-21A's
// (js/content/lines/edo-c.en.js, the talks js/content/talk/edo-c.js; S/work-21-writeA/ids.md says when each is said).
//
//   the three      Mom, Big Sister and Little Sister, a party in all three scenes (`THREE`); who is being played (`who`)
//   their clothes  O-Tami's travel kimonos all through Osaka (STOCK_DRESSED): the hats on out of doors (`edo`), on the back
//                  indoors (`edo-hatback`, the theatre); the girls in the puppeteers' black (`edo-kurogo`, PEOPLE-21B's) from
//                  the moment Jūbei takes them on (edo.hooded) until the show is over (edo.cue3): `dressFor`
//   talk           what the three say to each other in Osaka: WRITE-21A's companion talks of each scene first, then round
//                  twenty's that hold anywhere in Japan (`talkFor`)
//   people         a person turned to the lead (`faceLead`); a person's flat lines one more each time (`nth`); walking,
//                  turning and swapping (edo-yui.js's); a thing into or out of the pockets of a lead who is not played
//                  (edo-hills.js's)
//   the way back   the Dōjima steps, and every way behind them, refuse: the lighter has gone (the scenes' own lines)

import { is, STOCK_DRESSED, SEE } from "./edo-common.js";
import { THREE, who, heard, each, mine, lookUse, walkOf, look, swap, sitOnStep, standFromStep, cardWords } from "./edo-yui.js";
import { giveTo, takeFrom, carries, MATES, inPoly } from "./edo-hills.js";

export { is, THREE, who, heard, each, mine, lookUse, walkOf, look, swap, sitOnStep, standFromStep, cardWords, giveTo, takeFrom, carries, MATES, inPoly };
export const GIRLS = ["bigsis", "lilsis"];

// ---------- their clothes ----------
/** The girls are in the puppeteers' black while they are the boy puppet's hands and feet: from Jūbei's "Robes. Now."
    (edo.hooded) until the boy has knelt at his mother's door (edo.cue3). */
export const inBlack = (g) => is(g, "edo.hooded") && !is(g, "edo.cue3");
/** The three as the place wants them: the hats on out of doors (`edo`), on the back indoors (`edo-hatback`); the girls in
    `edo-kurogo` in the theatre while inBlack. A held moment's own outfit (sitting on the step) is left to its scene. */
export function dressFor(g, place) {
  const hat = place === "indoors" ? "edo-hatback" : "edo";
  for (const id of THREE) {
    const now = g.dressOf(id), black = place === "indoors" && id !== "mom" && inBlack(g);
    const want = black ? "edo-kurogo" : hat;
    if (now && now.endsWith("-step")) continue;
    if (now !== want && (now === null || now === "edo" || now === "edo-hatback" || now === "edo-kurogo")) g.dress(id, want);
  }
}

// ---------- the people of Osaka ----------
/** Turn someone of the scene to the one being played (and the one being played to them). */
export function faceLead(g, id) {
  const a = g.actor(id), l = g.lead;
  if (a && l && !a.seated) a.look(l.x, l.y);
  if (a && l && !g.stays()) l.look(a.x, a.y);
}
/** Someone's flat lines when spoken to, one more each time and the last ever after (WRITE-21A's { 1, more }): `<base>.say.1`,
    `.say.2`. The pilgrims of the Dōjima line. */
export const nth = (base, id, n = 2) => Object.assign(async (g) => {
  faceLead(g, id);
  const k = [...Array(n).keys()].map((i) => i + 1).find((i) => !heard(g, `${base}.say.${i}`));
  await g.say(`${base}.say.${k || n}`);
}, { lines: [...Array(n).keys()].map((i) => `${base}.say.${i + 1}`) });
/** A hold of someone's own (people.js), eased in, kept until let go: `pose(g, "natsu", "paddle")`; null lets it go. */
export function hold(g, id, name = null) {
  const a = g.actor(id);
  if (!a || !a.hold) return null;
  if (!name) { a.hold(false); return a; }
  a.hold(true, name);
  return a;
}
/** A small movement of someone's own, played once (or kept, with `keep`). */
export async function fidget(g, id, name, keep = false) {
  const a = g.actor(id);
  if (a && a.fidget) await a.fidget(name, keep ? { hold: true } : {});
}
/** Put a person on the stage (or take the one there) at a point, facing; faded in from nothing if asked. */
export async function put(g, id, kind, at, face = "S", { fadeIn = 0, scale = null } = {}) {
  const cast = g.view.cast;
  let f = cast.get(id);
  if (!f) f = cast.addFigure(id, kind, at[0], at[1], scale ?? g.sizeAt(at[0], at[1]));
  else f.place(at[0], at[1], scale ?? g.sizeAt(at[0], at[1]));
  f.hidden = false;
  f.face(face);
  if (fadeIn) { f.fade(0); await cast.load(); await g.tween(fadeIn, (k) => f.fade(k)); }
  else await cast.load();
  return f;
}
/** Someone goes away along points and is taken off the stage (faded for the last bit). */
export async function walkOff(g, id, points, { hurry = false, fade = 300 } = {}) {
  const a = g.actor(id);
  if (!a) return;
  await walkOf(g, id, points, hurry);
  if (fade) await g.tween(fade, (k) => a.fade(1 - k));
  g.view.cast.remove(id);
}
/** Run `fn` once the line `id` has been said (a moment staged under a talk the scene does not drive), or at once if it has
    been; nothing happens if the scene is left first. A clock loop of the game's: cheap, and gone with its moment. */
export function onLine(g, id, fn) {
  if (heard(g, id)) { fn(); return; }
  const scene = g.scene, stop = g.clock.every(() => {
    if (g.scene !== scene) { stop(); return; }
    if (heard(g, id)) { stop(); fn(); }
  });
}

// ---------- what the three say to each other in Osaka (the scenes' `talk`) ----------
// WRITE-21A's for each scene (edo.dojima.talk.*, edo.street.talk.*, edo.theatre.talk.*), with round twenty's WRITE-20A
// companion talks of the act that hold anywhere in Japan after them (as edo-hills.js TALK keeps them).
const ANYWHERE = {
  mom: { bigsis: [["edo.talk.mom.bigsis.read.a", "edo.talk.mom.bigsis.read.b", "edo.talk.mom.bigsis.read.c"]],
    lilsis: [["edo.talk.mom.lilsis.boots.a", "edo.talk.mom.lilsis.boots.b"]] },
  bigsis: { mom: [["edo.talk.bigsis.mom.tall.a", "edo.talk.bigsis.mom.tall.b"]], lilsis: [["edo.talk.bigsis.lilsis.hens.a", "edo.talk.bigsis.lilsis.hens.b"]] },
  lilsis: { mom: [["edo.talk.lilsis.mom.son.a", "edo.talk.lilsis.mom.son.b"], ["edo.talk.lilsis.mom.grace.a", "edo.talk.lilsis.mom.grace.b"]],
    bigsis: [["edo.talk.lilsis.bigsis.word.a", "edo.talk.lilsis.bigsis.word.b", "edo.talk.lilsis.bigsis.word.c"]] },
};
/** A scene's `talk`: its own exchanges ({ lilsis: { mom: [...] } }) first, then the act's ones from anywhere in Japan. */
export function talkFor(own) {
  const out = {};
  for (const a of THREE) {
    out[a] = {};
    for (const b of THREE) if (a !== b) out[a][b] = [...((own[a] || {})[b] || []), ...((ANYWHERE[a] || {})[b] || [])];
  }
  return out;
}

// ---------- the stock replies, and the looks at each other in black ----------
/** The act's stock replies; in the theatre, while the girls are in black, the looks at each other are WRITE-21A's own
    (edo.theatre.see.<who>.<whom>: six), and round twenty's SEE otherwise. */
export const STOCK_BLACK = { ...STOCK_DRESSED, see: Object.fromEntries(THREE.map((a) => [a, Object.fromEntries(THREE.filter((b) => b !== a).map((b) => [b, `edo.theatre.see.${a}.${b}`]))])) };
export const stockFor = (g, place = "outdoors") => (place === "indoors" && inBlack(g) ? STOCK_BLACK : STOCK_DRESSED);
export { STOCK_DRESSED, SEE };

// What Act Six's first stretch shares in round twenty-one (SCENES-21A: new): Suruga and the sea. The road over the Satta
// Pass (edo-kurasawa.js, edo-satta.js), the ship by day (edo-deck.js) and its compass (edo-compass.js), and the two
// cut-scenes either side of the deck (cutscenes/edo-castoff.js, cutscenes/edo-sail.js). Not a scene (it is in no list of
// scenes): a module they import, as round twenty's Yui scenes import edo-yui.js (whose helpers are used here as they are).
// The design is briefs/out/edo2-design.md, sections 3, 5 and 7 (#24 to #27); every line is WRITE-21A's
// (js/content/lines/edo-c.en.js) and every tree is talk/edo-c.js's.
//
//   helpers        the one being played, a line said once, a person turned to the lead, a thing put in a pocket that is not
//                  the lead's, a person's few words one more each time ({ 1, 2, more })
//   TALK_PASS      what the three say to each other at Nishikurasawa and at the top of the pass (WRITE-21A's companion talks)
//   TALK_DECK      and on deck
//   uttermost(g)   when #26 and #27 are both done on the deck (the heading called, the lady chirped): "The Uttermost Parts"
//   cloud          Fuji's one cap of cloud, for both scenes of the pass: on until it lifts at the top (edo.fujiClear), and
//                  hidden at Nishikurasawa from then on

import { THREE, who, is, heard, each, lookUse, walkOf, look, swap, cardWords } from "./edo-yui.js";

export { THREE, who, is, heard, each, lookUse, walkOf, look, swap, cardWords };

/** Turn someone of the scene to the one being played. */
export function faceLead(g, id) { const a = g.actor(id), l = g.lead; if (a && l) a.look(l.x, l.y); }
/** Say each line that has not been said yet (a first time's words), and nothing for one already heard. */
export async function once(g, ...ids) { for (const id of ids.flat()) if (!heard(g, id)) await g.say(id); }
/** The line of the one being played, `<base>.<who>`. */
export const mine = (g, base) => `${base}.${who(g)}`;
/** A look that changes with the story: `<base>.<state>.<who>` while `test`, else `<base>.<who>` (with the line list the checks
    read). */
export const lookBy = (base, state, test) => Object.assign((g) => g.say(`${base}${test(g) ? `.${state}` : ""}.${who(g)}`),
  { lines: THREE.flatMap((w) => [`${base}.${w}`, `${base}.${state}.${w}`]) });
/** Someone's few words, one more each time: `<base>.1`, `.2`, then `.3` ever after (WRITE-21A's { 1, 2, more }). */
export const nthOf = (base, person) => Object.assign(async (g) => {
  for (const id of [].concat(person || [])) faceLead(g, id);
  const n = [1, 2].find((k) => !heard(g, `${base}.${k}`));
  await g.say(`${base}.${n || 3}`);
}, { lines: [1, 2, 3].map((k) => `${base}.${k}`) });

/** A thing put into the pockets of one of the three who is not (or may not be) the one being played, and taken from whoever
    has it: the pockets are the save's (state.js), and the bar shows them at once. */
export function giveTo(g, whom, item) {
  const pockets = g.store.data.inventory;
  if (!pockets[whom]) pockets[whom] = [];
  if (!pockets[whom].includes(item)) pockets[whom].push(item);
  g.store.emit();
}
export function takeFromAnyone(g, item) {
  const pockets = g.store.data.inventory;
  for (const w of Object.keys(pockets)) { const i = pockets[w].indexOf(item); if (i >= 0) pockets[w].splice(i, 1); }
  g.store.emit();
}

// ---------- what the three say to each other on the road and on deck (WRITE-21A's ids.md, "Companion talks") ----------
const asked = (g, key) => (g.asked ? g.asked(key) : 0) > 0;
export const TALK_KURASAWA = {
  lilsis: { mom: [["edo.kurasawa.talk.lilsis.mom.ride.a", "edo.kurasawa.talk.lilsis.mom.ride.b"]] },
  bigsis: { mom: [["edo.kurasawa.talk.bigsis.mom.road.a", "edo.kurasawa.talk.bigsis.mom.road.b"]] },
  mom: { bigsis: [{ when: (g) => is(g, "edo.shellShared"), say: ["edo.kurasawa.talk.mom.bigsis.shell.a", "edo.kurasawa.talk.mom.bigsis.shell.b"] }] },
};
export const TALK_SATTA = {
  lilsis: { mom: [{ when: (g) => is(g, "edo.oldShoreHeard"), say: ["edo.satta.talk.lilsis.mom.forget.a", "edo.satta.talk.lilsis.mom.forget.b"] }] },
  bigsis: { lilsis: [{ when: (g) => is(g, "edo.fujiClear"), say: ["edo.satta.talk.bigsis.lilsis.view.a", "edo.satta.talk.bigsis.lilsis.view.b", "edo.satta.talk.bigsis.lilsis.view.c"] }] },
  mom: { lilsis: [["edo.satta.talk.mom.lilsis.son.a", "edo.satta.talk.mom.lilsis.son.b"]] },
};
export const TALK_DECK = {
  lilsis: { mom: [["edo.deck.talk.lilsis.mom.son.a", "edo.deck.talk.lilsis.mom.son.b"]] },
  bigsis: {
    mom: [{ when: (g) => is(g, "edo.headingCalled"), say: ["edo.deck.talk.bigsis.mom.clock.a", "edo.deck.talk.bigsis.mom.clock.b"] }],
    lilsis: [{ when: (g) => asked(g, "kota/grump"), say: ["edo.deck.talk.bigsis.lilsis.grump.a", "edo.deck.talk.bigsis.lilsis.grump.b"] }],
  },
  mom: { lilsis: [{ when: (g) => is(g, "edo.coinTraded"), say: ["edo.deck.talk.mom.lilsis.penny.a", "edo.deck.talk.mom.lilsis.penny.b"] }] },
};

// ---------- the deck's end: both puzzles done ----------
/** #26 and #27 are both done (the heading called, the lady chirped): the night at sea, Psalm 139, and on to Osaka. True if it
    played. */
export async function uttermost(g) {
  if (!is(g, "edo.headingCalled") || !is(g, "edo.chirped") || is(g, "edo.sailed")) return false;
  await g.wait(600);
  await g.cutscene("edo-sail");
  return true;
}

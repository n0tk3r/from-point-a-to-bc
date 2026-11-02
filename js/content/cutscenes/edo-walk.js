// The card "Three days later": the walk from the hills north of Osaka west along the shore road to Akashi, the beat edo.walk
// (SCENES-20B: new in round twenty, replacing MERGE-20's stub; SCENES-21B: edited in round twenty-one, briefs/SCENES-21.md, and
// the design, briefs/out/edo2-design.md, "Card: Three days later"). After #34 the family climbs out of the room under the
// storehouse (edo-chapel.js, the ladder, once edo.mirror is true), and this plays:
//   1. hats on for the road (PEOPLE-20's `edo`; Mom has lowered the mirror), and the stage goes dark;
//   2. the card on the dark, "Three days later" / "Akashi" (WRITE-20B's WALK.card, its second word WRITE-21B's: talk/edo-d.js
//      WALK), with Little Sister's one line under it (WALK.under: "Everybody else was going the OTHER way."): the stage is
//      emptied to black rather than faded, so that her words, which are drawn under the fade, show with the card;
//   3. the map: the family's portraits down out of the hills by Kōriyama and west along the road against the pilgrims, past
//      three small pictures by the way (PAINT-21F's stops: the camellia at Kōriyama's inn gate, the stone and the soba shop at
//      Suma, the pines bent by the wind at Maiko), each with its line said over it as the portraits come to it (WRITE-21B's
//      WALK.stops; Suma's two, Mom's and Big Sister's: SCENES-21B's small change to atlas.js lets a stop say a list), in
//      straw sandals (ENGINE-21's g.journey);
//   4. edo.walked, and on to the Akashi shore, on its mark `road` (the fourth leg: SCENES-21C's edo-akashi), with no era card
//      (the map has said where).
// Skipped, the same in an instant: the facts, the clothes, and the shore.
// (Round twenty-one: was "Three days later" / "Himeji", the journey from the hills to Himeji, and on to the castle approach.)

import { WALK } from "../talk/edo-d.js";

const FAMILY = ["mom", "bigsis", "lilsis"];

export default async function walk(g) {
  const L = (id, or) => (g.lines[id] ? g.lines[id][1] : or);
  // ---- 1. hats on (and the mirror lowered: Mom carries it in her sash now), and the dark ----
  await g.fade(1, 700);
  for (const id of FAMILY) { const now = g.dressOf(id); if (now === "edo-hatback" || now === "edo-mirror" || now === "edo") g.dress(id, "edo"); }
  if (g.flag("edo.mirrorUp")) g.flag("edo.mirrorUp", false);
  g.dialogue.clear();
  g.view.clear();
  g.stopLoop();
  g.ui.hud(false);
  await g.fade(0, 0);

  // ---- 2. the card, and Little Sister under it ----
  const [title, place] = WALK.card;
  await Promise.all([
    g.card(L(title, "Three days later"), L(place, "Akashi"), { plain: true, ms: 4200 }),
    (async () => { await g.wait(1300); await g.say(...WALK.under); })(),
  ]);
  for (const id of WALK.card) if (g.lines[id] && !g.clock.skipping) g.store.data.seenLines[id] = (g.store.data.seenLines[id] || 0) + 1;     // (a card's words are read, not said; SCENES-21B: and not when skipped, as edo-yui.js's cardWords has it)

  // ---- 3. the road west, on the map, past Kōriyama, Suma and Maiko (SCENES-21B) ----
  const stops = Object.entries(WALK.stops).map(([id, line]) => ({ id, line: line.length > 1 ? line : line[0] }));
  await g.journey("edo", "hills", "akashi", { sound: "sandals", stops, ms: 5200 });

  // ---- 4. the Akashi shore (after the skippable part: the arrival always plays as itself) ----
  g.flag("edo.walked", true);
  g.clock.skipping = false;
  g.ui.showSkip(false);
  await g.goto("edo-akashi", { via: "map", spawn: "road", card: false });
}

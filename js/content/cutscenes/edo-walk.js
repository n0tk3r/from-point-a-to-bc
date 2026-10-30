// The card "Three days later": the walk from the hills north of Osaka west to Himeji, the beat edo.walk (SCENES-20B: new in
// round twenty, replacing MERGE-20's stub; briefs/SCENES-20.md, and the design, briefs/out/edo-design.md, "Card: Three days
// later"). After #27 the family climbs out of the room under the storehouse (edo-chapel.js, the ladder, once edo.mirror is
// true), and this plays:
//   1. hats on for the road (PEOPLE-20's `edo`; Mom has lowered the mirror), and the stage goes dark;
//   2. the card on the dark, "Three days later" / "Himeji" (WRITE-20B's WALK.card), with Little Sister's one line under it
//      (WALK.under: "Everybody else was going the OTHER way."): the stage is emptied to black rather than faded, so that her
//      words, which are drawn under the fade, show with the card;
//   3. the map: the family's portraits along the road from the hills to Himeji, in straw sandals (ENGINE-20's g.journey);
//   4. edo.walked, and on to the castle approach at Himeji, on its mark `enter` (the third leg: SCENES-20C's edo-castle), with no
//      era card (the map has said where).
// Skipped, the same in an instant: the facts, the clothes, and the castle.
// The design's "the road's own little figures go east with their ladles" is not drawn: the journey on the map has the
// family's portraits only (ENGINE-20); ready.md says so.

import { WALK } from "../talk/edo-b.js";

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
    g.card(L(title, "Three days later"), L(place, "Himeji"), { plain: true, ms: 4200 }),
    (async () => { await g.wait(1300); await g.say(...WALK.under); })(),
  ]);
  for (const id of WALK.card) if (g.lines[id]) g.store.data.seenLines[id] = (g.store.data.seenLines[id] || 0) + 1;     // (a card's words are read, not said)

  // ---- 3. the road west, on the map ----
  await g.journey("edo", "hills", "himeji", { sound: "sandals" });

  // ---- 4. the castle (after the skippable part: the arrival always plays as itself) ----
  g.flag("edo.walked", true);
  g.clock.skipping = false;
  g.ui.showSkip(false);
  await g.goto("edo-castle", { via: "map", spawn: "enter", card: false });
}

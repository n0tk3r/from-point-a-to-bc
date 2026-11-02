// The card "The next day": the road on from the Akashi shore to Himeji, the beat edo.walk2 (SCENES-21C: new in round twenty-one,
// in place of MERGE-21's stub; briefs/SCENES-21.md, and the design, briefs/out/edo2-design.md, "Card: The next day"). Played by
// the Akashi shore (edo-akashi.js, the road west) once O-Fusa has her ladle back (edo.ladleBack) and Mom has said "West, girls.
// One more day of road.":
//   1. hats on for the road (Little Sister out of the water and in her boots on the sand, if she was not), and the dark;
//   2. the card on the dark, "The next day" / "Himeji" (WRITE-21B's WALK2.card);
//   3. the map: the family's portraits along the road from Akashi to Himeji, in straw sandals (ENGINE-21's g.journey);
//   4. edo.inHimeji, and Himeji town, Watamachi on the highway, at its mark `east` (edo-town.js), with no era card (the map has
//      said where).
// Skipped, the same in an instant: the fact, the clothes, and the town.

import { WALK2 } from "../talk/edo-d.js";

const FAMILY = ["mom", "bigsis", "lilsis"];

export default async function walk2(g) {
  const L = (id, or) => (g.lines[id] ? g.lines[id][1] : or);
  // ---- 1. hats on (Little Sister out of the water), and the dark ----
  await g.fade(1, 700);
  for (const id of FAMILY) { const now = g.dressOf(id); if (now !== "edo") g.dress(id, "edo"); }
  g.dialogue.clear();
  g.view.clear();
  g.stopLoop();
  g.ui.hud(false);
  await g.fade(0, 0);

  // ---- 2. the card ----
  const [title, place] = WALK2.card;
  await g.card(L(title, "The next day"), L(place, "Himeji"), { plain: true, ms: 3800 });
  for (const id of WALK2.card) if (g.lines[id]) g.store.data.seenLines[id] = (g.store.data.seenLines[id] || 0) + 1;     // (a card's words are read, not said)

  // ---- 3. the road on, on the map ----
  await g.journey("edo", "akashi", "himeji", { sound: "sandals" });

  // ---- 4. the town (after the skippable part: the arrival always plays as itself) ----
  g.flag("edo.inHimeji", true);
  g.clock.skipping = false;
  g.ui.showSkip(false);
  await g.goto("edo-town", { via: "map", spawn: "east", card: false });
}

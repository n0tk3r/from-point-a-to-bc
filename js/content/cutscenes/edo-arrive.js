// Cut-scene: "Meanwhile, in another time", which opens Act Six (SCENES-20A, in place of ENGINE-20's stub; the beat
// edo.arrive; the design, briefs/out/edo-design.md, "Cut-Scene: Meanwhile, in another time"; the lines are WRITE-20A's,
// edo.arrive.*, edo.card.*). After Going Down's card "Meanwhile" / "in another time": the tunnel, the years flying past,
// and out onto the beach at Yui in the morning, three figures out of a ring of light in the air that closes behind them
// with a sound like a breath let go. They count off (Mom's "Places, girls."), and Little Sister says it first: "This isn't
// ROME." Fuji; "...Is he here?" "No, sweetheart. Not here." A gull. A rooster up the beach. And the first villager to see
// them (the village woman with her basket) drops it, and will come back for it. Then the act's card, with no year on it.
//
// How it is played (ENGINE-20's rules, kept):
//   - by Going Down's hand-on (js/content/cutscenes/office-down.js, g.handOn(EDO_HANDON): the family the team, Mom played
//     first, their pockets normalised), after its card; and by the village's own `enter` for a game that has not had it
//     (edo.arrived not yet true: a save at the hand-on, the address ?scene=edo-village), which shows that card itself first;
//   - edo.arrived is set first, then the tunnel to the village (g.goto, via the wormhole, on the mark `arrive`, `card: false`:
//     NO era card, since when they are is the act's first puzzle, #21); the rest is played on the village as it stands,
//     the three kept out of sight there (edo-village.js `village.arriving`) until they step out of the door;
//   - the act's card at the end is "Act Six: By Your Grace" alone (Big Sister's line goes under it once #21 is solved);
//   - skipped, the same: the beach, the three on their marks, the basket dropped, the card not shown.

import { village, ARRIVAL } from "../scenes/edo-village.js";
import { THREE, cardWords, actCard, look, walkOf, swap } from "../scenes/edo-yui.js";
import { scaleAt } from "../../engine/walk.js";

export default async function arrive(g) {
  g.dialogue.clear();
  const ownCard = village.ownCard;                                            // (played by the village's `enter`: no Going Down, so its card here)
  village.ownCard = false;
  if (ownCard) {
    await g.fade(1, 600);
    await g.card(cardWords(g, "edo.card.meanwhile.1", "Meanwhile"), cardWords(g, "edo.card.meanwhile.2", "in another time"), { plain: true, ms: 2600 });
  }
  g.flag("edo.arrived", true);
  village.arriving = true;
  try {
    await g.goto("edo-village", { via: "wormhole", spawn: "arrive", card: false });
    // (the goto built the village with the three faded out, and has faded in on the beach; its `enter` stood aside)
    g.mode = "cutscene";
    g.ui.hud(false);
    if (!g.clock.skipping) g.ui.showSkip(true);
    await beach(g);
  } finally {
    village.arriving = false;
    for (const id of THREE) { const f = g.actor(id); if (f) { f.hidden = false; f.fade(1); } }
    const door = g.effects.get("arrival-door");
    if (door) door.show(false);
    g.clock.skipping = false;
    g.ui.showSkip(false);
    g.ui.hud(true);
    for (const id of THREE) if (g.actor(id)) g.rememberPlace(id);
  }
}

/** On the beach: the door, the three, the count, Fuji, the basket, the card. */
async function beach(g) {
  const A = ARRIVAL, cast = g.view.cast;
  await g.wait(700);
  // the door in time, on the sand by the boats (ENGINE-20's portal: the paint bends round it), tall and narrow as a doorway
  const door = g.effects.add({ id: "arrival-door", type: "portal", at: A.door.at, r: A.door.r, wide: 0.45, open: 0, base: 500, seed: 7 });
  g.sfx("portal");
  await g.tween(1100, (k) => { if (door) door.open(k); });
  // out of it, one after another, onto the sand, and to their places
  const out = { mom: [A.door.at[0], 506], bigsis: [A.door.at[0] + 10, 508], lilsis: [A.door.at[0] - 10, 508] };
  await Promise.all(THREE.map((id, n) => g.wait(n * 420).then(async () => {
    const f = g.actor(id);
    if (!f) return;
    f.place(out[id][0], out[id][1], scaleAt(g.scene, out[id][1]));
    f.face("S");
    await g.tween(320, (k) => f.fade(k));
    await g.walkTo(A.arrive[id][0], A.arrive[id][1], id);
  })));
  // and it closes behind them, with a sound like a breath let go
  g.sfx("breath");
  await g.tween(900, (k) => { if (door) door.open(1 - k); });
  if (door) door.show(false);
  // they count off
  look(g, "mom", "bigsis"); look(g, "bigsis", "mom"); look(g, "lilsis", "mom");
  await g.wait(300);
  await g.say("edo.arrive.1", "edo.arrive.2", "edo.arrive.3");
  // where's here: across the water, the mountain
  for (const id of THREE) look(g, id, [330, 160]);
  await g.wait(600);
  await g.say("edo.arrive.4", "edo.arrive.5");
  look(g, "lilsis", "mom");
  await g.say("edo.arrive.6");
  look(g, "mom", "lilsis");
  await g.wait(700);
  await g.say("edo.arrive.7");
  look(g, "mom", A.door.at);                                                   // the closed air where the door was
  await g.wait(900);
  await g.say("edo.arrive.8");
  // a gull; a rooster somewhere up the beach
  g.sfx("gull");
  await g.wait(1000);
  g.sfx("rooster");
  look(g, "lilsis", A.west);
  await g.wait(1300);
  await g.say("edo.arrive.9");
  // the first villager to see them: the village woman, her basket on her back
  const b = g.actor("basketwoman");
  if (b) {
    b.look(A.arrive.mom[0], A.arrive.mom[1]);
    if (b.hold) b.hold(true, "gasp");
    for (const id of THREE) look(g, id, [b.x, b.y]);
    await g.wait(700);
    const w = swap(g, "basketwoman", "basketwoman-dropped");               // the basket off her back, on the sand
    if (w && w.hold) w.hold(true, "gasp");
    const at = [w ? w.x + 10 : 400, (w ? w.y : 444) + 7];
    cast.addThing("dropped-basket", "basket", at[0], at[1], scaleAt(g.scene, at[1]));
    g.sfx("thunk");
    await cast.load();
    await g.wait(500);
    await g.say("edo.arrive.10");
    if (w && w.hold) w.hold(false);
    village.basketGone = true;                                              // (she will come back for it: the scene, built again, has her back)
    g.rebuildSpots();
    await walkOf(g, "basketwoman", [[470, 424], A.west], true);
    const gone = g.actor("basketwoman");
    if (gone) gone.hidden = true;
  }
  for (const id of THREE) look(g, id, A.west);
  await g.wait(400);
  look(g, "bigsis", "mom"); look(g, "lilsis", "mom");
  await g.say("edo.arrive.11");
  await g.wait(400);
  // the act's card: no year on it (that is #21)
  await actCard(g, false);
}

// The cut-scene "Hold Hands" (SCENES-20C: new in round twenty, in place of MERGE-20's stub). It ends Act Six, and the demo
// (the gate edo.end; the design, briefs/out/edo-design.md, "Cut-Scene: Hold Hands"; the lines are WRITE-20B's,
// js/content/lines/edo-b.en.js, edo.step.*, said in the order of `STEP`, js/content/talk/edo-b.js).
//
// Played on the top floor of the keep (edo-keeptop.js) when the mirror is in the warden's hands, its light on the hum and the
// doorway open in it (edo.door), the coin in Mom's hand:
//   1. The title: "Hold Hands".
//   2. "Places, girls. Hold hands. All the way through." The three of them in a row before the door, Little Sister in the
//      middle: "I'm in the MIDDLE." / "Left hand, right hand. Count of four." (SCENES-21C: Little Sister first, "My brother
//      SAID.", the Son's "Hold hands." from the women's hall the evening before; and Mom's prayer is WRITE-21B's, edited)
//   3. Mom looks once round the room, at the warden in the window with the mirror, at the sunset over the Inland Sea behind
//      him, and prays a short prayer of her own (that He knows where her son is, and she doesn't).
//   4. The goodbyes: Little Sister to the poem man ("Keep my flashlight SAFE"), his answer, Big Sister's thanks for the
//      stairs, and Mom: "Your cue, girls."
//   5. They walk into the light, hand in hand, the small one first, as he tells her; the coin goes with them in Mom's fist.
//   6. The door holds for a breath after them, and closes: he lowers the mirror. He goes back to his post at the top of the
//      stairs and sits down on the floor there with the pink light in his hands, and says one more poem, five, seven and
//      five, not frightened at all; and its last line, after a breath: "...The dark is just dark."
//   7. The tunnel.
//   8. The card: "to be continued" (after the skippable part: it always shows, as the Office's did). Then edo.done and
//      demo.done; the scene that played it (edo-keeptop.js) goes to the title.
// It carries save = false (the end of the demo is not saved before: Continue after the end comes back to the last save at
// rest, as round nineteen's end did).

import { STEP } from "../talk/edo-d.js";          // SCENES-21C: WRITE-21B's STEP (round twenty's, with Little Sister's "My brother SAID." first)

const FAMILY = ["mom", "lilsis", "bigsis"];
// In a row before the door (on the east wall, its foot at the wall's), facing it, Little Sister in the middle: set by eye on
// the top floor's floor (layout.json walk), a step back from the hum's mark; side by side across the room, which the camera
// sees as a slant (so that the three of them are seen, and not one behind another).
const ROW = { mom: [530, 379], lilsis: [553, 394], bigsis: [578, 410] };
// Into the light: at the wall's foot under the door (past the walk's edge: a straight walk, as the Nevada door's).
const INTO = { mom: [626, 377], lilsis: [634, 388], bigsis: [644, 401] };
// Where the warden sits down afterwards: his post at the top of the stairs (the top floor's mark `shinnosuke`, a step on).
const POST = [266, 452];

/** Into the door: she walks into it and is gone as she reaches it (nevada-roadside.js, `into`). */
async function into(g, id, delay) {
  const a = g.actor(id);
  if (!a) return;
  await g.wait(delay);
  const walk = g.moveTo(INTO[id][0], INTO[id][1], id);
  await g.wait(260);
  await g.tween(560, (k) => a.fade(1 - k), g.ease.in);
  await walk;
  a.fade(0);
  a.hidden = true;
}
const turn = (g, id, dir) => { const a = g.actor(id); if (a) a.face(dir); };
const lookAt = (g, id, at) => { const a = g.actor(id), b = g.actor(at); if (a && b) a.look(b.x, b.y); };

export default async function step(g) {
  const L = (id, or) => (g.lines[id] ? g.lines[id][1] : or);
  const seen = (id) => { g.store.data.seenLines[id] = (g.store.data.seenLines[id] || 0) + 1; };
  const sh = g.actor("shinnosuke"), light = g.effects.get("light");

  // ---- 1. the title
  await g.fade(1, 500);
  await g.card(L(STEP.title, "Hold Hands"), "", { plain: true, ms: 2000 });
  seen(STEP.title);
  await g.fade(0, 500);

  // ---- 2. places: in a row before the door, Little Sister in the middle. SCENES-21C: she says it first now ("My brother
  // SAID.": his "Hold hands." at the women's hall, the evening before), and Mom's "Places, girls. Hold hands." answers him
  turn(g, "mom", "E");
  lookAt(g, "lilsis", "mom");
  await g.say(STEP.places[0]);
  await g.say(STEP.places[1]);
  await Promise.all(FAMILY.map((id, n) => (g.actor(id) ? g.wait(n * 200).then(() => g.walkTo(ROW[id][0], ROW[id][1], id)) : null)));
  for (const id of FAMILY) turn(g, id, "E");
  lookAt(g, "lilsis", "mom");
  await g.say(STEP.places[2]);
  turn(g, "lilsis", "E");
  await g.say(STEP.places[3]);

  // ---- 3. Mom looks once round the room: the warden, the sunset behind him; and prays
  const mom = g.actor("mom");
  if (mom) {
    lookAt(g, "mom", "shinnosuke");
    await g.wait(1100);
    mom.face("W");
    await g.wait(900);
    mom.face("E");
    mom.pray(true);
  }
  await g.say(...STEP.prayer);
  if (mom) mom.pray(false);
  await g.wait(400);

  // ---- 4. the goodbyes
  lookAt(g, "lilsis", "shinnosuke");
  await g.say(STEP.goodbyes[0]);
  await g.say(STEP.goodbyes[1]);
  lookAt(g, "bigsis", "shinnosuke");
  await g.say(STEP.goodbyes[2]);
  for (const id of FAMILY) turn(g, id, "E");
  await g.say(STEP.goodbyes[3]);
  await g.wait(500);

  // ---- 5. into the light, hand in hand, the small one first; the coin goes with them in Mom's fist
  g.sfx("portal");
  await Promise.all([into(g, "lilsis", 0), into(g, "mom", 60), into(g, "bigsis", 120)]);
  const inv = g.store.data.inventory || {};
  for (const id of Object.keys(inv)) if (Array.isArray(inv[id]) && inv[id].includes("coin")) inv[id] = inv[id].filter((item) => item !== "coin");
  g.store.emit();

  // ---- 6. the door holds for a breath, and closes: he lowers the mirror, and sits down on the floor with the light
  await g.wait(1300);
  if (light) await g.tween(1100, (k) => light.set({ on: 1 - k }));
  if (light) light.set({ on: 0, doorK: 0 });
  if (g.stopLoop) g.stopLoop("hum");                 // (and the hum with it)
  await g.wait(500);
  if (sh) {
    // back to the top of the stairs, where the warden is, and down on the floor there, the pink light in his hands
    sh.hold(false);
    await g.walkTo(POST[0], POST[1], "shinnosuke");
    const cast = g.view.cast, s = sh.scale;
    cast.remove("shinnosuke");
    const f = cast.addFigure("shinnosuke", "shinnosuke-floor", POST[0], POST[1], s).face("SE");
    await cast.load();
    if (f.sit) await f.sit(true, true);
    f.hold(true, "light");
  }
  await g.wait(900);
  await g.say(STEP.poem[0], STEP.poem[1], STEP.poem[2]);
  await g.wait(1200);
  await g.say(STEP.poem[3]);
  await g.wait(1400);

  // ---- 7. the tunnel
  g.sfx("portal");
  await g.fade(1, 500, "#fff");
  if (!g.clock.skipping) {
    g.ui.hud(false);
    g.view.clear();
    g.effects.drop();
    g.view.setEra("tunnel");
    g.startTunnel([]);
    g.music("tunnel");
    await g.fade(0, 400, "#fff");
    await g.wait(2400);
    await g.fade(1, 500, "#fff");
    g.stopTunnel();
  }

  // ---- 8. the card (after the skippable part: it always shows), and the end of the act, and of the demo
  g.clock.skipping = false;
  g.ui.showSkip(false);
  await g.fade(1, 900);
  await g.card(L(STEP.card, "to be continued"), "", { plain: true, ms: 4200 });
  seen(STEP.card);
  g.flag("edo.done", true);
  g.flag("demo.done", true);
}
// The end of the demo is not saved before (FINAL-19's rule, now the act's: office-down.js no longer carries it).
step.save = false;

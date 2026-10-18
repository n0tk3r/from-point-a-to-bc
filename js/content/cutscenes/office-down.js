// The cut-scene "Going Down" (SCENES-17: new in round seventeen). It ends the Office's stage one, and the demo (the beat
// office.end; the design, briefs/out/office-hq-design.md, section 4; every line is in js/content/lines/office.en.js,
// office.down.*, said in the order of that file; S/work-17-write/ids.md, section 3).
//
// Played by the Rag at the door (ragTree's hook `down`, js/content/scenes/office-room.js), once the suits are "now
// authorized" to take him to the only soundproof room in the building. All of it from Ranger's duct, through the slats:
//   1. "Going Down". Through the grille over ROOM C: Grandpa Joe goes out of the open door playing the pie-tin banjo, hat
//      on, between Dale and Merle, and Wendell behind with his fingers in his ears. "Y'all ever been down to B-7?" "No,
//      sir. We have never been authorized, sir." "Well. Now you are." "It is still my birthday, Dale." "Noted, Wendell."
//      Houston, on every speaker: the music is going down to B-7.
//   2. Ranger at the grille over the HALL (there is no painting of the hall in stage one: the elevator is heard through
//      the slats under him): its own polite little tune, and "Turn that off, son. I brought my own." "Mind the--"
//      "Minding the hat, sir." The doors close on the Rag. A thought: Joe's hat, down.
//   3. Ranger at the B-7 shaft, the big fan stopped: he looks down it (down, Joe's hat, heart), looks at us in his mirror
//      shades ("...!"), and goes.
//   4. Houston, to nobody in particular: "Lamplighter test at seventeen hundred hours. Sector 44. Please do not look
//      directly at the sector."
//   5. The card: LAMPLIGHTER, and smaller, "to be continued". The end of the demo (office.done, demo.done).
// Skipped, the same: the card is after the skippable part, so it always shows; then the title (the room's script).

import { scaleAt } from "../../engine/walk.js";
import { WORDS } from "../scenes/office-common.js";

// Where they are in the Comfortable Room (its marks: the door, the hall outside it): Grandpa Joe by the table where he played,
// Dale ahead of him and Merle beside; Wendell already out in the hall, behind the doorframe.
const ROOM = { door: [186, 452], hall: [183, 428], joe: [430, 472], dale: [372, 462], merle: [470, 476], wendell: [176, 431],
  joeMid: [318, 470], merleMid: [352, 476], daleDoor: [200, 454], joeDoor: [236, 462], merleDoor: [270, 468] };
const DUCT = { hall: [535, 470], shaft: [618, 470], below: [585, 525] };

export default async function down(g) {
  const cast = g.view.cast;
  const room = await g.getScene("office-room"), ducts = await g.getScene("office-ducts");
  const roomSize = (y) => scaleAt(room, y);
  const walk = (id, points, size) => { const a = g.actor(id); return a ? a.walkPath(g.clock, points, size) : Promise.resolve(); };

  // ---- 1. the title; then the Comfortable Room seen through the slats of ROOM C: out of the door, playing
  await g.fade(1, 500);
  await g.card(g.lines["office.down.card"] ? g.lines["office.down.card"][1] : "Going Down", "", { plain: true, ms: 2200 });
  g.store.data.seenLines["office.down.card"] = (g.store.data.seenLines["office.down.card"] || 0) + 1;
  g.dialogue.clear();
  g.view.clear();
  await g.view.show(room, g);
  for (const id of ["door"]) { const p = g.plane(id); if (p) p.show(false); }
  { const p = g.plane("door-open"); if (p) p.show(true); }
  { const p = g.plane("vent-eyes"); if (p) p.show(true); }
  { const p = g.plane("vent"); if (p) p.show(false); }
  const joe = cast.addFigure("grandpajoe", "grandpajoe-play-pie", ROOM.joe[0], ROOM.joe[1], roomSize(ROOM.joe[1])).face("W");
  cast.addFigure("suit1", "suit1", ROOM.dale[0], ROOM.dale[1], roomSize(ROOM.dale[1])).face("W");
  cast.addFigure("suit2", "suit2", ROOM.merle[0], ROOM.merle[1], roomSize(ROOM.merle[1])).face("W");
  cast.addFigure("suit3", "suit3-ears", ROOM.wendell[0], ROOM.wendell[1], roomSize(ROOM.wendell[1])).face("S");
  await cast.load();
  await g.grilleOver("office-ducts");
  g.music("rag-tin");
  await g.fade(0, 600);
  await g.wait(400);
  // across the room toward the door, playing as he goes (a walk and a word, and a walk and a word)
  const step = (id, to) => walk(id, [to], roomSize);
  await Promise.all([step("suit1", ROOM.daleDoor), step("grandpajoe", ROOM.joeMid), step("suit2", ROOM.merleMid), g.say("office.down.1")]);
  { const a = g.actor("suit1"); if (a) a.look(ROOM.joeMid[0], ROOM.joeMid[1]); }
  await g.say("office.down.2");
  await Promise.all([step("grandpajoe", ROOM.joeDoor), step("suit2", ROOM.merleDoor)]);
  await g.say("office.down.3");
  { const a = g.actor("suit3"); if (a) a.look(ROOM.daleDoor[0], ROOM.daleDoor[1]); }
  await g.say("office.down.4", "office.down.5");
  // out through the door into the hall, Dale first: past the doorframe, gone
  const out = async (id, wait) => { await g.wait(wait); await walk(id, [ROOM.door, ROOM.hall], roomSize); const a = g.actor(id); if (a) a.hidden = true; };
  await Promise.all([out("suit1", 0), out("grandpajoe", 500), out("suit2", 1100), g.wait(900).then(() => walk("suit3", [[ROOM.hall[0] - 50, ROOM.hall[1] - 4]], roomSize))]);
  await g.pa("office.pa.down", { building: "office" });
  await g.fade(1, 400);

  // ---- 2. along the duct: Ranger at the grille over the HALL; the elevator, heard through the slats under him
  g.grilleOver(null);
  g.view.clear();
  await g.view.show(ducts, g);
  const r = cast.addFigure("ranger", "ranger", DUCT.hall[0], DUCT.hall[1], scaleAt(ducts, DUCT.hall[1])).face("E");
  if (r.variant) r.variant("shades");
  await cast.load();
  if (r.pose) r.pose("peek", 0);
  await g.fade(0, 400);
  WORDS.at = DUCT.below;                                                       // (the voices come up through the slats)
  try {
    g.sfx("ding");                                                             // the elevator, and its own polite little tune
    await g.wait(700);
    await g.say("office.down.6", "office.down.7", "office.down.8");
    g.sfx("latch");                                                            // the doors close on the Rag
    g.music("office");
    await g.wait(900);
  } finally { WORDS.at = null; }
  if (r.pose) r.pose(null);
  await g.say("office.down.ranger.1");

  // ---- 3. the B-7 shaft, the big fan stopped: he looks down it, at us, and goes
  await r.walkPath(g.clock, [DUCT.shaft], () => 1);
  r.face("E");
  if (r.pose) r.pose("peek", 0);
  await g.wait(500);
  await g.say("office.down.ranger.2");
  if (r.pose) r.pose(null);
  r.face("S");
  if (r.sit) await r.sit(true);
  await g.wait(400);
  await g.say("office.down.ranger.3");
  if (r.sit) await r.sit(false);
  r.face("E");
  if (!g.clock.skipping) {
    const [x, y] = [r.x, r.y];
    r.base = 600;
    await g.tween(700, (k) => { r.place(x + 40 * k, y + 120 * k * k, 1); r.fade(1 - k * k); });
  }
  r.hidden = true;
  await g.wait(800);

  // ---- 4. Houston, to nobody in particular
  await g.pa("office.pa.test", { building: "office" });
  await g.wait(600);

  // ---- 5. the card (after the skippable part: it always shows), and the end of the demo
  g.clock.skipping = false;
  g.ui.showSkip(false);
  await g.fade(1, 1000);
  const L = (id, or) => (g.lines[id] ? g.lines[id][1] : or);
  await g.card(L("office.card.1", "LAMPLIGHTER"), L("office.card.2", "to be continued"), { plain: true, ms: 4200 });
  for (const id of ["office.card.1", "office.card.2"]) g.store.data.seenLines[id] = (g.store.data.seenLines[id] || 0) + 1;
  g.flag("office.done", true);
  g.flag("demo.done", true);
}

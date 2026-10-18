// The cut-scene "A Very Small Building With A Very Long Name" (SCENES-17: new in round seventeen). It opens the Office's
// stage one (the beat office.arrive; the design, briefs/out/office-hq-design.md, section 4; every line is in
// js/content/lines/office.en.js, office.arrive.*, said in the order of that file; S/work-17-write/ids.md, section 3).
//
// The limousine has stopped in the lot (its ending, js/content/scenes/nevada-limo.js, slows the desert to nothing and puts
// up the card THE OFFICE OF PECULIAR SECTORS, "Desert Field Headquarters, the same afternoon"). Then:
//   1. The title over the lot, and the four suits get out in a row: "Sir, we have arrived, sir." "Sorry about the drive, sir."
//   2. Two of them bring Grandpa Joe out of the back, upright, hat on: "Sir, you will now be processed." "Son, I been
//      processed. Jolene does it every Sunday before church."
//   3. Jed comes round the front with the banjo's hoop round his neck and what is left of the banjo, and goes in ahead:
//      "Evidence." "Careful with her, son. She's had a day." "...We have all had a day, sir."
//   4. Across the gravel to the door between the suits: the sign on the gate ("Please look at the gravel, sir."), the
//      rooftop unit ("We are not permitted to discuss the air.").
//   5. The mat: he wipes his boots. "Sign asked nice."
//   6. At the door he looks back at the limousine's open door: "Ranger. You know what to do." "Sir, was that addressed to the
//      raccoon?" "What raccoon, son?" Dale checks the clipboard: "...The raccoon is not on the form." "Then officially,
//      there ain't one."
//   7. The door shuts on all of them but Wendell, who turns round, by regulation, to face the gate. "...It is my birthday."
//      Houston, on every speaker inside: one civilian has arrived; it is Wendell's birthday, and there is a pie.
//   8. A moment. Ranger comes out from under the limousine's seat in his mirror shades, drops to the gravel, sits up: a
//      thought of Joe's hat; a question mark; the door, plus a suit. Play as Ranger.
// Nobody touches anybody: the suits walk either side of him, and he walks.
//
// Played by the limousine's ending (or by the lot's `enter`, for a game that has not had it: a save, or the address
// index.html?scene=office-lot). It dresses the stage itself with the lot's own picture and cut-outs, whatever was on it.
// Skipped, it runs the same script with every wait cut to nothing and lands in the same place: Grandpa Joe in the
// Comfortable Room (g.putLead), Ranger by the limousine's back wheel, the two of them the team, his best bottle cap in his
// stash, and the lot.

import { scaleAt } from "../../engine/walk.js";
import { ARRIVAL as A } from "../scenes/office-lot.js";

const SUITS = ["suit1", "suit2", "suit3", "suit4"];          // Dale, Merle, Wendell, Floyd

export default async function arrive(g) {
  const d = g.store.data, lot = await g.getScene("office-lot");
  const sz = (y) => scaleAt(lot, y);
  const cast = g.view.cast;
  const walk = (id, points, hurry = false) => { const a = g.actor(id); if (!a || !points.length) return Promise.resolve(); if (hurry) a.hurry = true; return a.walkPath(g.clock, points, sz); };
  const look = (id, at) => { const a = g.actor(id), b = typeof at === "string" ? g.actor(at) : null; if (a) a.look(...(b ? [b.x, b.y] : at)); };
  const face = (id, dir) => { const a = g.actor(id); if (a) a.face(dir); };
  /** In at the front door: up to it, and through (gone behind the door's line, as the backup fades the suits into the car). */
  const goIn = async (id) => { const a = g.actor(id); if (!a) return; await Promise.all([walk(id, [A.inDoor]), g.tween(420, (k) => a.fade(1 - k))]); a.hidden = true; };

  // ---- the stage: the lot, the limousine parked with its doors shut, nobody yet
  await g.fade(1, 300);
  g.dialogue.clear();
  g.view.clear();
  if (g.effects && g.effects.drop) g.effects.drop();                          // (the limousine's desert, going by its windows, is over)
  await g.view.show(lot, g);
  const door = g.plane("door"), doorOpen = g.plane("door-open"), limo = g.plane("limo"), limoOpen = g.plane("limo-door-open");
  if (limo) limo.show(true);
  if (limoOpen) limoOpen.show(false);
  for (const id of ["fan", "grille", "nut-1", "nut-2", "nut-3", "nut-4", "switch"]) { const p = g.plane(id); if (p) p.show(true); }
  for (const id of ["grille-off", "switch-off", "trash-tipped", "trash-pipe"]) { const p = g.plane(id); if (p) p.show(false); }
  const trash = g.plane("trash");
  if (trash) trash.show(true);
  // the four suits behind the car's near side, at their doors; Grandpa Joe behind the back door; Jed round its nose
  SUITS.forEach((id, i) => { const [x, y] = A.outOfCar[3 - i]; const f = cast.addFigure(id, id === "suit3" ? "suit3-birthday" : id, x, y - 9, sz(y - 9)).face("S"); f.fade(0); });
  const joe = cast.addFigure("grandpajoe", "grandpajoe-room", A.limoDoor[0], A.limoDoor[1] - 9, sz(A.limoDoor[1] - 9)).face("S");
  joe.fade(0);
  const jed = cast.addFigure("agent", "agent-collar-banjo", A.jedFrom[0], A.jedFrom[1], sz(A.jedFrom[1])).face("W");
  const ranger = cast.addFigure("ranger", "ranger", A.sill.at[0], A.sill.at[1], A.sill.scale).face("W");
  if (ranger.variant) ranger.variant("shades");
  ranger.hidden = true; ranger.fade(0);
  await cast.load();
  await g.fade(0, 700);
  await g.wait(500);
  await g.card(g.lines["office.arrive.card"] ? g.lines["office.arrive.card"][1] : "A Very Small Building With A Very Long Name", "", { plain: true, ms: 2600 });
  g.store.data.seenLines["office.arrive.card"] = (g.store.data.seenLines["office.arrive.card"] || 0) + 1;

  // ---- 1. four doors: four men in gray step out in a row
  g.sfx("latch");
  await Promise.all(SUITS.map((id, i) => { const a = g.actor(id), [x, y] = A.outOfCar[3 - i]; return Promise.all([walk(id, [[x, y]]), g.tween(300, (k) => a.fade(k))]); }));
  SUITS.forEach((id) => face(id, "S"));
  await g.wait(300);
  await g.say("office.arrive.1", "office.arrive.2");

  // ---- 2. two of them either side of the back door, and Grandpa Joe out of it, upright, hat on
  await Promise.all([walk("suit1", [A.dale]), walk("suit2", [A.merle])]);
  if (limo) limo.show(false);
  if (limoOpen) limoOpen.show(true);                                           // (the back door, open: it stays open)
  g.sfx("latch");
  face("suit1", "E"); face("suit2", "W");
  await Promise.all([walk("grandpajoe", [A.limoDoor]), g.tween(400, (k) => joe.fade(k))]);
  joe.face("S");
  await g.say("office.arrive.3", "office.arrive.4");

  // ---- 3. Jed, round the car's nose with the evidence, and in ahead of everybody
  const jedIn = (async () => {
    await walk("agent", [[760, 412], [600, 418], ...A.walkIn.slice(1, 4)]);
  })();
  await g.wait(1600);
  look("grandpajoe", "agent");
  await g.say("office.arrive.5");
  await g.say("office.arrive.6", "office.arrive.7");
  await jedIn;
  await Promise.all([walk("agent", [A.queue.jed]), (async () => { if (door) door.show(false); if (doorOpen) doorOpen.show(true); g.sfx("unlock"); })()]);
  await goIn("agent");

  // ---- 4. across the gravel to the door, between the suits: the sign on the gate, and the rooftop unit
  const along = [A.walkIn[1], A.walkIn[2]];
  const crossing = Promise.all([
    walk("grandpajoe", along), walk("suit1", along.map(([x, y]) => [x - 26, y - 5])), walk("suit2", along.map(([x, y]) => [x + 30, y + 3])),
    walk("suit3", [[520, 432], [430, 440], [A.queue.floyd[0] - 30, A.queue.floyd[1] - 2]]), walk("suit4", [[600, 420], [470, 440], [A.queue.floyd[0] + 30, A.queue.floyd[1]]]),
  ]);
  await g.wait(900);
  look("grandpajoe", A.gateSign);
  await g.say("office.arrive.8");
  look("suit1", "grandpajoe");
  await g.say("office.arrive.9");
  await crossing;
  look("grandpajoe", A.unit);
  await g.say("office.arrive.10");
  look("suit2", "grandpajoe");
  await g.say("office.arrive.11");

  // ---- 5. the mat: he wipes his boots; Wendell to his post at the door
  await Promise.all([walk("grandpajoe", [A.walkIn[3], A.mat]), walk("suit1", [A.queue.dale]), walk("suit2", [A.queue.merle]), walk("suit3", [A.door]), walk("suit4", [A.queue.floyd])]);
  face("grandpajoe", "N"); face("suit3", "E");
  if (joe.play) await joe.play(g.clock, "pick");
  await g.say("office.arrive.12", "office.arrive.13");

  // ---- 6. at the door he looks back at the limousine's open door, and says, not loud:
  await walk("grandpajoe", [A.queue.joe]);
  look("grandpajoe", A.limoDoor);
  await g.wait(700);
  await g.say("office.arrive.14");
  look("suit3", "grandpajoe");
  await g.say("office.arrive.15");
  await g.say("office.arrive.16");
  look("suit1", A.limoDoor);
  await g.wait(400);
  face("suit1", "S");                                                           // (the clipboard)
  await g.say("office.arrive.17");
  await g.say("office.arrive.18");

  // ---- 7. in they go, all but Wendell; the door shuts; Wendell turns to face the gate, by regulation
  await goIn("suit1");
  await goIn("grandpajoe");
  await Promise.all([goIn("suit2"), g.wait(300).then(() => goIn("suit4"))]);
  if (doorOpen) doorOpen.show(false);
  if (door) door.show(true);
  g.sfx("latch");
  await g.wait(500);
  face("suit3", "W");
  await g.wait(600);
  await g.say("office.arrive.19");
  await g.pa("office.pa.arrive", { building: "office" });
  await g.pa("office.pa.pie", { building: "office" });                         // (the pie, planted: Joe hears it too)

  // ---- 8. a moment; and Ranger, out from under the seat in his mirror shades, down to the gravel
  await g.wait(1200);
  ranger.hidden = false;
  await g.tween(380, (k) => ranger.fade(k));
  await g.wait(500);
  if (ranger.pose) ranger.pose("drop", 0);
  await g.tween(300, (k) => ranger.place(A.sill.at[0] + (A.fromLimo[0] - A.sill.at[0]) * k, A.sill.at[1] + (A.fromLimo[1] - A.sill.at[1]) * k * k, A.sill.scale + (sz(A.fromLimo[1]) - A.sill.scale) * k));
  if (ranger.pose) { ranger.pose("drop", 1); await g.wait(260); ranger.pose(null); }
  ranger.face("W");
  if (ranger.sit) await ranger.sit(true);
  await g.wait(300);
  await g.say("office.arrive.ranger.1", "office.arrive.ranger.2", "office.arrive.ranger.3");

  // ---- the play goes to the two of them: Ranger here, Grandpa Joe in the Comfortable Room (as an act hands over)
  g.flag("office.arrived", true);
  d.act = 6;
  d.active = "ranger";
  g.team(["grandpajoe", "ranger"]);
  const pockets = d.inventory.ranger || (d.inventory.ranger = []);
  if (!pockets.includes("bottlecap")) pockets.push("bottlecap");               // (his best: he has had it all along; nothing to announce)
  g.store.emit();
  await g.putLead("grandpajoe", "office-room", "joe", { face: "E" });
  // The skippable part ends here: whatever was skipped, the lot is played as itself.
  g.clock.skipping = false;
  g.ui.showSkip(false);
  await g.goto("office-lot", { via: "cut", spawn: "fromLimo", card: false });
}

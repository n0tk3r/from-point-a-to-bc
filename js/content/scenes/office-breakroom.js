// Act Five, continued: the Office's break room (SCENES-17: new in round seventeen; briefs/SCENES-17.md, and the design,
// briefs/out/office-hq-design.md, section 4). A fridge (LABEL YOUR LUNCH. MGMT.), a coffee maker steaming, a sink, the
// counter with Wendell's pie in its tin and its card (HAPPY BIRTHDAY WENDELL. DO NOT EAT. (REGULATIONS)), a vending
// machine, a corkboard (FORM 7 IS NOT OPTIONAL; FOUND: ONE ROMAN SANDAL; the bowling league; and the Lamplighter test
// schedule), Floyd asleep on the couch on his regulation rest, and Jed in a plastic chair with an ice pack on his head and
// the banjo's hoop round his neck, looking right at the pie.
//
// RANGER only, from the grille over the fridge (office-ducts.js), or dropped onto the fridge's top. Three floors of his
// (layout.json levels): the fridge's top, the counter, and the room's floor; he goes from one to another by the painter's
// paths (fridge, microwave, counter; the counter's end, the floor by the machine), as a raccoon does.
//   #19 Wendell's Pie   with Jed there, a raccoon dropping in is shooed back up ("Raccoon. In the break room. ...Do you have
//                       a cheeseburger? No. Shoo, please."). Grandpa Joe gets Jed his cheeseburger (the intercom, on Jed's
//                       behalf: office-room.js); then the pie: Ranger eats it, the whole of it, and leaves his best bottle
//                       cap in the tin (a trade: he does not steal); takes the sticky tin, leaving the cap on Wendell's
//                       card, and washes it at the sink till it shines (`pietin`); and off the corkboard, the test schedule
//                       (`schedule`), for Joe. The vending machine: every button, and one packet of peanuts, for later.
//
// Every place is the painter's own measurement of the finished picture (art/scenes/office-breakroom/layout.json, PAINT-17D's
// ready.md); where a place was set by eye the comment says so.
//
// Try it: index.html?scene=office-ducts&lead=ranger&flags=office.arrived,office.inside,office.acOff,office.jedGone ("Look down" BREAK)

import { STOCK, ANNOUNCE, BUILDING, WORDS, who, is, heard, keepHeat, chatter, shades, rangerAt } from "./office-common.js";
import { nowAndThen } from "../talk/office.js";
import { icePackAt } from "../../art/people.js";

const art = "art/scenes/office-breakroom/";

// ---------- the room (layout.json: horizon 200, full 383) and Ranger's own floors (levels, ranger_marks) ----------
const FLOOR = [[206, 365], [550, 369], [559, 376], [730, 380], [764, 400], [737, 425], [147, 410]];
const COUNTER = [[285, 285], [521, 287], [525, 290], [281, 288]];
// The fridge's top: one place (5 cm under the eye: seen edge-on, his size there is the mark's, not his row's)
const FRIDGE_TOP = [[184, 201], [202, 201], [202, 207], [184, 207]];
const M = {
  fridge: [193, 204], micro: [262, 259], counter: [371, 287], sink: [338, 288], board: [456, 287], "counter-end": [510, 289],
  "counter-left": [293, 287], vending: [602, 386], floyd: [84, 412], jed: [514, 394], door: [715, 380],
};
const FRIDGE_SCALE = 0.865;
const GRILLE = [202, 133];             // the grille's middle (paths.vent-fridge): where a drop falls from, and the climb goes to
const AT_PIE = [392, 289];             // standing over the pie, eating it (set by eye: he covers the tin from us while he eats)
const THERE = [215, 165];              // Ranger's thoughts while he looks down (he is up at the grille): by it
const HOUSTON = [520, 248];            // Houston in Jed's earpiece: over his head

const floorOf = (g) => { const f = g.lead ? g.floorOf(g.lead) : null; return f ? f.name : null; };
const jedThere = (g) => !is(g, "office.jedGone");
const eyes = (g) => rangerAt(g, "over-break");
const ranger = (g) => g.actor("ranger");

// ---------- Ranger's ways between his floors (layout.json paths) ----------
/** Down from the fridge's top by the microwave's to the counter; or up from the floor at the counter's end. */
async function toCounter(g) {
  const f = floorOf(g);
  if (f === "counter") return;
  if (f === "fridge") return void (await g.climbTo("counter-left", { path: [M.micro], set: "walk", face: "E" }));
  await g.walkTo(M.vending[0], M.vending[1]);
  await g.climbTo("counter-end", { path: [[530, 376]], set: "climb", face: "W" });
}
/** Down to the floor at the counter's right end (from the fridge, by the counter). */
async function toFloor(g) {
  if (floorOf(g) === "floor") return;
  if (floorOf(g) === "fridge") await toCounter(g);
  await g.walkTo(M["counter-end"][0], M["counter-end"][1]);
  await g.climbTo("vending", { path: [[530, 376]], set: "drop", face: "E" });
}
/** Back up onto the fridge's top (from the counter by the microwave's; from the floor by the counter). */
async function toFridge(g) {
  if (floorOf(g) === "fridge") return;
  await toCounter(g);
  await g.walkTo(M["counter-left"][0], M["counter-left"][1]);
  await g.climbTo("fridge", { path: [M.micro], set: "climb", face: "W" });
}
/** To a place on the counter (his own walk along it, once he is up there), facing the thing. */
async function onCounter(g, at, face = "E") {
  await toCounter(g);
  await g.walkTo(at[0], at[1]);
  if (g.lead) g.lead.face(face);
}

// ---------- #19: the pie ----------
/** The pie, Jed gone: he eats it, the whole of it (a nibble, the lot, a pause, a satisfied lean back); and his best bottle
    cap out of his stash, set in the middle of the empty tin. He does not steal. He trades. */
async function eat(g) {
  const r = ranger(g);
  await onCounter(g, AT_PIE, "W");
  await g.say("office.pie.nibble");
  if (r) r.play(g.clock, "nibble", { ms: 2600 });
  g.sfx("slurp");
  await g.say("office.pie.eat");
  if (r) r.stop();
  await g.wait(700);
  if (r) { await r.sit(true); await g.wait(500); }
  await g.say("office.pie.full");
  await g.say("office.pie.trade");
  if (r) await r.play(g.clock, "reach");
  if (g.has("bottlecap")) g.take("bottlecap");
  g.flag("office.pieEaten", true);                                             // (the empty tin, sticky, the cap in its middle)
  if (r) { await r.sit(false); await g.walkTo(M.counter[0], M.counter[1]); r.face("E"); }
}
/** The empty tin: he takes it (sticky), and the bottle cap stays behind, on Wendell's card; to the sink, and the wash, till it
    shines. */
async function tin(g) {
  const r = ranger(g);
  await onCounter(g, M.counter, "E");
  await g.say("office.pie.sticky");
  if (r) await r.play(g.clock, "reach");
  g.flag("office.tinTaken", true);                                             // (the card fallen flat, the cap on it, a sticky ring)
  await g.say("office.pie.card");
  await g.walkTo(M.sink[0], M.sink[1]);
  if (r) { r.face("E"); await r.sit(true); }
  g.sfx("hiss");
  if (r) await r.play(g.clock, "wash", { ms: 2200 });
  await g.say("office.pie.wash");
  g.give("pietin");
  g.flag("office.tinClean", true);
  if (r) await r.sit(false);
}
async function pieUse(g) {
  if (jedThere(g)) return g.say("office.break.jed.ranger");                    // (only from above: in here, Jed would have shooed him)
  if (!is(g, "office.pieEaten")) return eat(g);
  if (!is(g, "office.tinTaken")) return tin(g);
  return g.say("office.break.card.after.ranger");
}
/** The test schedule off the corkboard, for Joe (a lamp on top, and times). */
async function schedule(g) {
  const r = ranger(g);
  await onCounter(g, M.board, "N");
  if (r) { await r.sit(true); await r.play(g.clock, "reach"); }
  await g.say("office.pie.schedule");
  g.flag("office.schedTaken", true);
  g.give("schedule");
  if (r) await r.sit(false);
}

// ---------- the vending machine, and Floyd ----------
/** Every button; one packet of peanuts falls, and he takes it for later. Then nothing more comes. */
async function vending(g) {
  if (is(g, "office.peanuts")) return g.say("office.break.vending.again.ranger");
  const r = ranger(g);
  await toFloor(g);
  await g.walkTo(M.vending[0], M.vending[1]);
  if (r) { r.face("N"); await r.sit(true); }
  for (let k = 0; k < 6; k++) { g.sfx("key"); await g.wait(150); }
  g.sfx("clunk");
  vend.packet = true;                                                          // (the packet in the tray)
  g.store.emit();
  await g.say("office.break.vending.use.ranger");
  if (r) await r.play(g.clock, "reach");
  vend.packet = false;
  g.give("peanuts");
  g.flag("office.peanuts", true);
  if (r) await r.sit(false);
}
const vend = { packet: false };
/** Waking Floyd: he says a regulation in his sleep, and does not wake. */
async function floyd(g) {
  const f = g.actor("suit4");
  await toFloor(g);
  await g.walkTo(195, 407);
  if (g.lead) g.lead.face("W");
  g.think("suit4", null);
  if (f && f.fidget) f.fidget("wake");
  await g.say("office.break.floyd.use.1");
  await g.say("office.break.floyd.use.ranger");
  g.think("suit4", "zzz", { loop: true });
}

// ---------- now and then: Jed and the pie, Floyd asleep (and Houston in Jed's earpiece) ----------
const CHAT = chatter(nowAndThen["office-breakroom"], { first: [8, 12], every: [22, 34], voices: { houston: HOUSTON } });

/** One of the room's areas: Ranger's look (from above too: `peek`) and his use in here. No place to walk to: his uses take
    him to the floor they need (toCounter, toFloor) themselves. */
function spot(id, name, shape, look, use = null, { when = null, more = {} } = {}) {
  return { id, name, ...shape, walkTo: null, look: { ranger: look }, ...(use ? { use: { ranger: use } } : {}), peek: { look: { ranger: look } },
    ...(when ? { when } : {}), ...more };
}
/** Something on the counter: his look from anywhere; his use up on the counter, at its place. */
const onTop = (at, line, face = "N") => async (g) => { await onCounter(g, at, face); await g.say(line); };
const onFloor = (at, line, face = "N") => async (g) => { await toFloor(g); await g.walkTo(at[0], at[1]); if (g.lead) g.lead.face(face); await g.say(line); };

export default {
  id: "office-breakroom",
  era: "nevada",
  name: "The break room",
  building: BUILDING,
  music: "office",

  horizon: 200, full: 383, maxScale: 1.2,
  walk: [
    { name: "floor", area: FLOOR, away: { ranger: (g) => toFloor(g) } },
    { name: "counter", area: COUNTER, horizon: 200, full: 300.71, away: { ranger: (g) => toCounter(g) } },
    { name: "fridge", area: FRIDGE_TOP, scale: FRIDGE_SCALE, away: { ranger: (g) => toFridge(g) } },
  ],
  blocked: [[[490, 385], [529, 386], [538, 403], [495, 402]]],                 // Jed's chair

  spawn: { default: M.vending, ...M },
  facing: "E",
  exits: ["office-ducts"],
  stock: STOCK,
  announce: ANNOUNCE,
  get wordsAt() { return WORDS.at || (g0.peeking ? THERE : HOUSTON); },
  tick(g, dt) { keepHeat(g); CHAT.tick(g, dt); },

  picture: art + "back.png",
  planes: [
    { id: "vent", src: art + "vent.png", plane: "back", when: (g) => !eyes(g) },
    { id: "vent-eyes", src: art + "vent-eyes.png", plane: "back", when: eyes },
    { id: "door", src: art + "door.png", plane: "back" },
    { id: "clock", frames: Array.from({ length: 60 }, (_, n) => art + `clock-${n}.png`), fps: 1, at: [423, 202], foot: [15, 30], plane: "back" },
    { id: "schedule", src: art + "schedule.png", plane: "back", when: (g) => !is(g, "office.schedTaken") },
    { id: "pie", src: art + "pie.png", plane: "back", when: (g) => !is(g, "office.pieEaten") },
    { id: "pie-eaten", src: art + "pie-eaten.png", plane: "back", when: (g) => is(g, "office.pieEaten") && !is(g, "office.tinTaken") },
    { id: "pie-gone", src: art + "pie-gone.png", plane: "back", when: (g) => is(g, "office.tinTaken") },
    { id: "vending", src: art + "vending.png", base: [[560, 373], [643, 375]], when: (g) => !is(g, "office.peanuts") && !vend.packet,
      solid: [[541, 349], [613, 350], [643, 375], [560, 373]] },
    { id: "vending-peanuts", src: art + "vending-peanuts.png", base: [[560, 373], [643, 375]], when: () => vend.packet,
      solid: [[541, 349], [613, 350], [643, 375], [560, 373]] },
    { id: "vending-taken", src: art + "vending-taken.png", base: [[560, 373], [643, 375]], when: (g) => is(g, "office.peanuts") && !vend.packet,
      solid: [[541, 349], [613, 350], [643, 375], [560, 373]] },
    { id: "chair", src: art + "chair.png", base: [[486, 385], [532, 385]], solid: [[490, 385], [529, 386], [538, 403], [495, 402]] },
    { id: "door-open", src: art + "door-open.png", base: [[705, 352], [731, 376]], when: () => false, solid: [[705, 352], [731, 376], [726, 376], [701, 351]] },
    { id: "front", src: art + "front.png", plane: "front" },
  ],
  fx: [
    { id: "steam", type: "smoke", at: [491, 265], height: 34, width: [2, 9], lean: [-4, -34], rise: 7, rate: 2.2, gust: 0.2, color: "#e8ece4", opacity: 0.3, base: [496, 365] },
  ],

  // Floyd asleep on the couch on his regulation rest (PEOPLE-17's suit4-asleep: he stirs now and then), and Jed in his
  // chair with the ice pack and the hoop, watching the pie, until his cheeseburger is called (agent-ice: the actor is
  // `agent`, Jed's cast id, so that his words stand over him).
  actors: [
    { id: "suit4", kind: "suit4-asleep", at: M.floyd, face: "E", life: { fidget: [8, 16] } },
    { id: "agent", kind: "agent-ice", at: M.jed, face: "W", when: jedThere, life: { fidget: [6, 12] } },
  ],

  // Back to front: the big things first, the small things on them over them.
  hotspots: [
    spot("couch", "couch", { poly: [[0, 330], [3, 328], [66, 308], [79, 308], [89, 310], [163, 328], [165, 332], [165, 337], [164, 378], [157, 389], [0, 488]] },
      "office.break.couch.ranger", onFloor([195, 407], "office.break.couch.use.ranger", "W")),
    spot("fridge", "fridge", { poly: [[155, 204], [156, 203], [236, 202], [245, 243], [245, 257], [228, 356], [221, 362], [194, 362], [163, 361], [154, 329]] },
      "office.break.fridge.ranger", "office.break.fridge.use.ranger"),
    spot("fridgesign", "sign", { poly: [[164, 212], [209, 212], [209, 251], [164, 251]] }, "office.break.fridgesign.ranger"),
    spot("magnets", "magnets", { poly: [[212, 262], [238, 262], [236, 300], [212, 300]] }, "office.break.magnets.ranger", "office.break.magnets.use.ranger"),
    spot("forks", "box of forks", { poly: [[175, 191], [187, 187], [199, 186], [210, 186], [216, 192], [216, 205], [175, 205]] }, "office.break.forks.ranger",
      async (g) => { await toFridge(g); await g.say("office.break.forks.use.ranger"); }),
    spot("plant", "dusty plant", { poly: [[213, 211], [216, 190], [221, 190], [228, 191], [230, 198], [224, 230], [218, 242], [216, 242], [215, 241], [213, 226]] }, "office.break.plant.ranger",
      async (g) => { await toFridge(g); await g.say("office.break.plant.use.ranger"); }),
    spot("cabinets", "counter", { poly: [[223, 288], [231, 284], [287, 272], [445, 273], [521, 274], [533, 291], [529, 363], [445, 364], [227, 358], [225, 352]] },
      (g) => g.say(is(g, "office.pieEaten") ? "office.break.counter.after.ranger" : "office.break.counter.ranger")),
    spot("microwave", "microwave", { poly: [[233, 260], [240, 257], [261, 256], [289, 257], [289, 279], [281, 286], [278, 287], [233, 285]] }, "office.break.microwave.ranger",
      onTop(M["counter-left"], "office.break.microwave.use.ranger", "W")),
    spot("rack", "dish rack", { poly: [[283, 278], [293, 266], [296, 266], [320, 271], [320, 282], [319, 284], [315, 287], [282, 287]] }, "office.break.rack.ranger"),
    spot("sink", "sink", { poly: [[316, 286], [343, 258], [344, 258], [366, 280], [366, 281], [351, 288], [316, 288]] }, "office.break.sink.ranger",
      async (g) => { if (is(g, "office.tinTaken") && !is(g, "office.tinClean")) return tin(g); await onCounter(g, M.sink, "E"); const r = ranger(g); if (r) await r.play(g.clock, "wash", { ms: 1400 }); await g.say("office.break.sink.use.ranger"); }),
    spot("board", "corkboard", { rect: [369, 213, 107, 59] }, "office.break.board.ranger", onTop(M.board, "office.break.board.use.ranger")),
    spot("form7", "notice", { poly: [[376, 218], [413, 218], [413, 243], [376, 243]] }, "office.break.form7.ranger", onTop(M.board, "office.break.board.use.ranger")),
    spot("found", "index card", { poly: [[378, 249], [402, 248], [402, 266], [379, 266]] }, "office.break.found.ranger", onTop(M.board, "office.break.board.use.ranger")),
    spot("bowling", "bowling league", { poly: [[418, 219], [442, 220], [441, 255], [417, 255]] }, "office.break.bowling.ranger", onTop(M.board, "office.break.board.use.ranger")),
    spot("menu", "takeout menu", { poly: [[404, 247], [413, 247], [414, 266], [405, 266]] }, "office.break.menu.ranger", onTop(M.board, "office.break.menu.use.ranger")),
    spot("schedule", "test schedule", { poly: [[447, 237], [468, 238], [467, 266], [446, 265]] }, "office.break.schedule.ranger", schedule,
      { when: (g) => !is(g, "office.schedTaken"), more: { verb: "Take" } }),
    spot("coffee", "coffee maker", { poly: [[477, 254], [501, 254], [504, 257], [504, 287], [480, 287], [478, 285], [477, 283]] }, "office.break.coffee.ranger",
      onTop(M["counter-end"], "office.break.coffee.ranger")),
    spot("cups", "paper cups", { poly: [[505, 267], [506, 263], [511, 263], [512, 264], [524, 277], [524, 289], [520, 289], [505, 286]] }, "office.break.cups.ranger",
      onTop(M["counter-end"], "office.break.cups.use.ranger")),
    spot("pie", "pie", { poly: [[381, 281], [386, 277], [401, 277], [403, 278], [406, 281], [406, 283], [404, 286], [402, 287], [385, 287], [381, 282]] },
      (g) => g.say(!is(g, "office.pieEaten") ? "office.break.pie.ranger" : "office.break.counter.after.ranger"), pieUse,
      { when: (g) => !is(g, "office.tinTaken"), more: { verb: "Eat" } }),
    spot("card", "card", { poly: [[398, 273], [413, 273], [413, 283], [405, 283], [399, 279], [398, 278]] },
      (g) => g.say(is(g, "office.pieEaten") ? "office.break.card.after.ranger" : "office.break.card.ranger"), onTop(M.counter, "office.break.card.use.ranger")),
    spot("clock", "clock", { poly: [[413, 179], [416, 175], [420, 174], [426, 174], [431, 176], [435, 182], [436, 191], [431, 198], [427, 199], [420, 199], [413, 194], [411, 188]] }, "office.break.clock.ranger"),
    spot("speaker", "speaker", { poly: [[690, 160], [699, 138], [728, 134], [733, 134], [738, 151], [742, 172], [720, 175], [686, 174]] }, "office.break.speaker.ranger", "office.break.speaker.use.ranger"),
    spot("door", "door", { poly: [[630, 189], [647, 188], [656, 188], [711, 189], [710, 353], [705, 353], [655, 352], [643, 351], [629, 210]] }, "office.break.door.ranger"),
    spot("vending", "vending machine", { poly: [[540, 209], [570, 194], [573, 194], [644, 211], [645, 229], [645, 238], [643, 371], [640, 375], [559, 373], [540, 348]] },
      "office.break.vending.ranger", vending),
    spot("buttons", "buttons", { poly: [[624, 244], [639, 244], [639, 291], [624, 291]] }, "office.break.buttons.ranger", vending),
    spot("tray", "tray", { poly: [[570, 337], [617, 338], [617, 362], [570, 361]] }, "office.break.tray.ranger", vending),
    spot("chair", "chair", { poly: [[491, 343], [534, 308], [535, 308], [540, 312], [543, 315], [543, 318], [533, 402], [498, 402], [493, 388], [490, 347]] },
      (g) => g.say(jedThere(g) ? "office.break.jed.ranger" : "office.break.chair.ranger"), null, { more: { plane: "chair" } }),
    // the people: Floyd on the couch, Jed in his chair
    spot("suit4", "Floyd", { rect: [62, 300, 50, 112] }, "office.break.floyd.ranger", floyd, { more: { verb: "Wake" } }),
    spot("agent", "Jed", { rect: [494, 262, 40, 132] }, "office.break.jed.ranger", null, { when: jedThere }),
    // the grille over the fridge: from the fridge's top, his way back up (and down there, the way to it)
    { id: "vent", name: "vent", verb: "Climb up", poly: [[153, 125], [207, 123], [240, 136], [244, 138], [244, 139], [197, 141], [188, 138], [151, 127]], walkTo: null,
      look: { ranger: "office.break.vent.ranger" }, use: { ranger: async (g) => { await toFridge(g); await g.climbUp({ scene: "office-ducts", spawn: "over-break", to: GRILLE }); } } },
  ],

  setup(g) {
    g0 = g;
    keepHeat(g);
    vend.packet = false;
    WORDS.at = null;
    CHAT.reset();
    shades(g);
    // Floyd asleep: his zzz over him (a thought kept up: not saved, so put up here from the story)
    if (g.actor("suit4")) g.think("suit4", "zzz", { loop: true });
    // Jed gone: his ice pack lies on the seat of his chair, where it fell
    if (!jedThere(g)) {
      const size = Math.max(10, Math.round((160 * 1.0 * ((M.jed[1] - 200) / 183)) / 2) * 2), [dx, dy] = icePackAt(270, size);
      const pack = g.view.cast.addThing("icepack", "icepack", M.jed[0] + dx, M.jed[1] - 0.262 * size * 0.98, (M.jed[1] - 200) / 183, { state: "down" });
      pack.base = M.jed[1] + 2;
      void dy;
    }
  },

  // Ranger drops onto the fridge: with Jed there, Jed sees him, asks the one question he has, and shoos him back up.
  async enter(g, from) {
    if (who(g) !== "ranger" || from !== "office-ducts") return;
    if (jedThere(g)) {
      const j = g.actor("agent"), r = g.lead;
      if (j && r) j.look(r.x, r.y + 150);
      await g.say("office.jed.ranger.1", "office.jed.ranger.2", "office.jed.ranger.3", "office.jed.ranger.4");
      if (j) j.face("W");
      await g.climbUp({ scene: "office-ducts", spawn: "over-break", to: GRILLE });
      return;
    }
    if (!is(g, "office.pieEaten") && !heard(g, "office.pie.fridge.ranger")) await g.say("office.pie.fridge.ranger");
  },

  // Ranger looks down through the grille: the first time, a pie.
  async viewed(g) {
    if (!is(g, "office.sawBreak")) { g.flag("office.sawBreak", true); await g.say("office.duct.break.first.ranger"); }
  },
};
let g0 = { peeking: null };              // (the game, for the words' place: wordsAt is read with no game handed in)

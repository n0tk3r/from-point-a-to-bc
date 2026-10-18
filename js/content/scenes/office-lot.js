// Act Five, continued: the Office's lot (SCENES-17: new in round seventeen; briefs/SCENES-17.md, and the design,
// briefs/out/office-hq-design.md, section 4). Early afternoon, the same day: a very small building with a very long name,
// a gravel lot, a flagpole, the gray limousine parked along the side with its back door left open, and on the roof an air
// conditioner the size of a minivan. Wendell is on the door, facing the gate, by regulation; it is his birthday.
//
// RANGER plays here, alone (Grandpa Joe is locked in the Comfortable Room: office-room.js). His thoughts are all there is:
// every look and try is a line with pictures (js/content/lines/office.en.js, "#16 Not On The Form").
//
//   the arrival         "A Very Small Building With A Very Long Name" (js/content/cutscenes/office-arrive.js), played by
//                       the limousine's ending; this scene's `enter` plays it for a game that has not had it yet.
//   #16 Not On The Form the door (Wendell: "You are not authorized." "Shoo, please."), the keypad, the drainpipe that
//                       ends three feet up, the limousine's hood, the grille with the fan turning: no. The trash can: he
//                       tries the lid (chained), tips the can over (a clang: Wendell turns round, sees a raccoon in a trash
//                       can, notes it), rolls it to the drainpipe and stands it up there; up the can and the pipe to the
//                       roof (two floors: the gravel, and the roof); the four wing nuts; the switch with a fan crossed out
//                       on its sticker: he pulls it, the fan runs down and the building's hum with it (office.acOff: from
//                       now on the Comfortable Room gets warmer), and in at the intake, into the ducts (office.inside).
//
// Every place is the painter's own measurement of the finished picture (art/scenes/office-lot/layout.json, PAINT-17A's
// ready.md), or was set by eye against the picture with Ranger in it; where the two differ the comment says why.
//
// Try it: index.html?scene=office-lot&lead=ranger&flags=office.arrived   (the arrival first, without office.arrived)
// Later:  &flags=office.arrived,office.trash,office.canUnder (the can under the pipe), office.grilleOff, office.acOff

import { STOCK, ANNOUNCE, BUILDING, WORDS, is, heard, keepHeat, chatter, shades } from "./office-common.js";
import { nowAndThen } from "../talk/office.js";

const art = "art/scenes/office-lot/";
const R = "ranger";

// ---------- the floors (layout.json walk_areas): the gravel, and the strip of roof in front of the unit, 3 m up ----------
const GRAVEL = [[0, 393.1], [88, 393.1], [88, 430.2], [500.7, 430.2], [488.7, 395.5], [800, 395.5], [800, 597], [0, 597]];
const ROOF = [[123.9, 247.5], [438.5, 247.5], [432.6, 231.2], [165.7, 231.2]];
const ROOF_FULL = 313.7;               // the roof's own depth: whoever stands on it is (feet - 140) / 173.7 of full size

// ---------- the marks (layout.json marks, faces) ----------
const M = {
  fromLimo: [597.5, 398.0], door: [230.9, 433.9], trash: [339.9, 434.3], pipe: [436.0, 433.9], climbFrom: [389.8, 433.9],
  roof: [405.5, 244.9], intake: [344.0, 231.8], switch: [378.3, 231.6], limoDoor: [618.2, 407.3],
  dale: [574.2, 408.4], merle: [667.8, 410.0], inDoor: [287.5, 415.6],
};
// Up the can and the drainpipe (layout.json climb: climbFrom, the lid, the elbow, just under the coping, the roof). His
// feet are above the can's base row on the lid and the pipe, so he is drawn in front of the can all the way (base 441,
// just in front of trash-pipe's 439.1: PAINT-17A).
const CLIMB = [[431.1, 386.9], [429.0, 373.7], [429.0, 273.9]];
const CLIMB_BASE = 441;
// The cans (layout.json cans): standing by the wall, tipped over (its mouth toward us), standing under the drainpipe.
const CAN = { mouth: [423.9, 431.6], push: [372, 448] };
const NUTS = [                                                                  // the order he turns them: low left, low right, high left, high right
  { n: 1, stand: [309.4, 231.6], high: false }, { n: 2, stand: [359.5, 231.6], high: false },
  { n: 3, stand: [309.4, 231.6], high: true }, { n: 4, stand: [359.5, 231.6], high: true },
];
const SILL = { at: [344.9, 214.5], scale: 0.519 };                              // the intake's sill, where he hops up and goes in
const DOOR_BACK = [334, 452];                                                   // where he backs off to, shooed from the door

/** The arrival's places, for js/content/cutscenes/office-arrive.js (layout.json marks: outOfCar, jedFrom, walkIn, queue;
    limo.sill: where Ranger stands in the open door before he drops to the gravel). */
export const ARRIVAL = {
  outOfCar: [[614.9, 400.9], [652.4, 400.9], [712.3, 400.9], [749.0, 400.9]], jedFrom: [1026.6, 400.2],
  walkIn: [[582.2, 410.6], [505.1, 426.2], [412.1, 436.4], [315.0, 437.6], [280.9, 431.8]], inDoor: [287.5, 415.6],
  queue: { jed: [280.4, 432.9], dale: [240.6, 438.1], joe: [277.5, 440.0], merle: [314.7, 438.6], floyd: [363.0, 442.5] },
  sill: { at: [607.0, 380.1], scale: 0.561 }, limoDoor: M.limoDoor, dale: M.dale, merle: M.merle, door: M.door, fromLimo: M.fromLimo,
  mat: [276.0, 443.7], gateSign: [38.4, 300], unit: [305, 160],
};

// ---------- where Ranger is ----------
const onRoof = (g) => { const f = g.floorOf(g.lead); return !!f && f.name === "roof"; };
const grilleOff = (g) => is(g, "office.grilleOff");
const acOff = (g) => is(g, "office.acOff");
const canUnder = (g) => is(g, "office.canUnder");
const tipped = (g) => is(g, "office.trash") && !canUnder(g);
const ranger = (g) => g.actor(R);

/** Wendell turns to look at a point, or back to the gate, by regulation. */
function wendell(g, at = null) {
  const w = g.actor("suit3");
  if (!w) return;
  if (at) w.look(at[0], at[1]); else w.face("W");
}

// ---------- the door, the mat and the keypad: Wendell ----------
async function door(g) {
  const r = ranger(g), first = !heard(g, "office.lot.door.use.1");
  if (r) r.face("W");
  wendell(g, r ? [r.x, r.y] : null);
  if (first) await g.say("office.lot.door.use.1", "office.lot.door.use.2", "office.lot.door.use.ranger");
  else await g.say("office.lot.door.again.1", "office.lot.door.again.2", "office.lot.door.again.ranger");
  // shooed (politely): he backs off a few steps, and Wendell turns back to the gate
  if (r) { await g.walkTo(DOOR_BACK[0], DOOR_BACK[1]); r.face("W"); }
  wendell(g);
}
async function mat(g) {
  const r = ranger(g);
  if (r) await r.play(g.clock, "wash", { ms: 1400 });                         // all four feet, carefully
  await g.say("office.lot.mat.use.ranger");
  wendell(g, r ? [r.x, r.y] : null);
  await g.say("office.lot.mat.use.1");
  wendell(g);
}
async function keypad(g) {
  const r = ranger(g), n = ["office.lot.keypad.use.1", "office.lot.keypad.use.2"].filter((id) => heard(g, id)).length;
  if (r) await r.sit(true);
  for (let k = 0; k < 4; k++) { g.sfx("key"); await g.wait(170); }            // every button; it beeps every time
  wendell(g, r ? [r.x, r.y] : null);
  await g.say(`office.lot.keypad.use.${n + 1}`, "office.lot.keypad.use.ranger");
  if (r) await r.sit(false);
  wendell(g);
}
async function wendellUse(g) {
  wendell(g, ranger(g) ? [ranger(g).x, ranger(g).y] : null);
  await g.say("office.lot.wendell.use.1", "office.lot.door.use.ranger");
  wendell(g);
}
async function wendellCap(g) {
  wendell(g, ranger(g) ? [ranger(g).x, ranger(g).y] : null);
  await g.say("office.lot.wendell.with.bottlecap.1", "office.lot.wendell.with.bottlecap.2", "office.lot.wendell.with.bottlecap.ranger");
  wendell(g);
}

// ---------- #16: the trash can ----------
/** The can standing by the wall: he tries the lid (chained: REGULATION), and tips the can over instead. A clang; Wendell
    turns round, sees a raccoon in a trash can, writes it down ("...One raccoon. In trash." "Noted."), and turns back to the
    gate. He is on a form at last. A little later Wendell reports it, and Houston tells the building (`tick`, below). */
async function tip(g) {
  const r = ranger(g);
  if (!heard(g, "office.lot.trash.lid.ranger")) {
    if (r) { await r.sit(true); await r.play(g.clock, "reach"); }
    await g.say("office.lot.trash.lid.ranger");
    if (r) await r.sit(false);
  }
  if (r) await r.play(g.clock, "reach");
  g.sfx("clang");
  g.flag("office.trash", true);                                                // (the can on its side: trash-tipped)
  // in at its mouth, nose first: he is in a trash can when Wendell turns round
  if (r) {
    r.base = 451;                                                              // (in front of the tipped can, base 450.5)
    await g.moveTo(CAN.mouth[0] - 4, CAN.mouth[1] + 4);
    r.face("W");
  }
  await g.wait(500);
  wendell(g, CAN.mouth);
  await g.wait(400);
  await g.say("office.lot.trash.wendell.1", "office.lot.trash.wendell.2");
  wendell(g);
  await g.say("office.lot.trash.noted.ranger");
  if (r) { await g.moveTo(CAN.push[0], CAN.push[1] + 4); r.base = null; r.face("E"); }
  lot.reportAt = g.store.data.playMs + 6000;                                   // (Wendell reports it, a little later)
}
/** The can on its side: he rolls it along to the foot of the drainpipe, and stands it up there. */
async function roll(g) {
  const r = ranger(g), can = g.plane("trash-tipped");
  await g.say("office.lot.trash.roll.ranger");
  if (r) { r.face("E"); r.base = 451; }
  await Promise.all([
    can ? g.tween(900, (k) => can.place(26 * k, -3 * k), g.ease.inOut) : null,
    r ? g.moveTo(CAN.push[0] + 26, CAN.push[1] - 2) : null,
  ]);
  g.sfx("clunk");
  g.flag("office.canUnder", true);                                             // (stood up under the elbow: trash-pipe)
  if (can) can.place(0, 0);
  if (r) { await g.moveTo(M.climbFrom[0], M.climbFrom[1]); r.base = null; r.face("E"); }
  await g.say("office.lot.trash.stand.ranger");
}
async function trashUse(g) {
  if (!is(g, "office.trash")) return tip(g);
  if (!canUnder(g)) return roll(g);
  return climbUp(g);
}
const trashLook = (g) => g.say(!is(g, "office.trash") ? "office.lot.trash.ranger" : canUnder(g) ? "office.lot.trash.under.ranger" : "office.lot.trash.tipped.ranger");

// ---------- the drainpipe: up to the roof, and down again ----------
/** Up the can and the pipe to the roof (the can under it), or not (it ends three feet up: just out of reach). Played from
    the gravel: the pipe itself, the can under it, or a click on the roof. */
async function climbUp(g) {
  const r = ranger(g);
  if (!r) return;
  if (onRoof(g)) return;
  if (!canUnder(g)) {
    await g.walkTo(M.pipe[0], M.pipe[1]);
    r.face("E");
    await r.sit(true);                                                         // he stretches up: just out of reach
    await r.play(g.clock, "reach");
    await g.say(heard(g, "office.lot.pipe.use.ranger") ? "office.lot.pipe.again.ranger" : "office.lot.pipe.use.ranger");
    await r.sit(false);
    return;
  }
  await g.walkTo(M.climbFrom[0], M.climbFrom[1]);
  r.face("E");
  if (!heard(g, "office.lot.pipe.climb.ranger")) await g.say("office.lot.pipe.climb.ranger");
  await g.climbTo("roof", { path: CLIMB, base: CLIMB_BASE, face: "E" });
  r.face("W");
}
/** Down again the same way (a click on the gravel from the roof, or anything down there used). */
async function climbDown(g) {
  const r = ranger(g);
  if (!r || !onRoof(g)) return;
  await g.walkTo(M.roof[0], M.roof[1]);
  await g.climbTo("climbFrom", { path: [...CLIMB].reverse(), base: CLIMB_BASE, face: "E" });
  if (r.pose) { r.pose("drop", 1); await g.wait(260); r.pose(null); }
}
const pipeUse = (g) => climbUp(g);

// ---------- on the roof: the wing nuts, the grille, the switch, the intake ----------
/** The four wing nuts, one, two, three, four (raccoons have hands): the low ones sitting up, the high ones climbing the
    grille. Each one squeaks, and goes; the fourth, and the grille comes off and leans on the unit. */
async function nuts(g) {
  const r = ranger(g);
  if (!r || grilleOff(g)) return;
  for (const nut of NUTS) {
    await g.walkTo(nut.stand[0], nut.stand[1]);
    r.face("E");
    if (nut.high) {                                                            // up the grille's louvres to the high one, and down
      const [x, y] = nut.stand, s = r.scale;
      r.base = y + 0.5;
      const up = r.play ? r.play(g.clock, "climb", { ms: 520 }) : null;
      await g.tween(520, (k) => r.place(x, y - 30 * k, s));
      await up;
      if (r.pose) r.pose("climb", 1);
      for (let k = 0; k < 2; k++) { g.sfx("squeak"); await g.wait(240); }
      const nutPlane = g.plane(`nut-${nut.n}`);
      if (nutPlane) nutPlane.show(false);
      if (r.pose) r.pose(null);
      await g.tween(380, (k) => r.place(x, y - 30 * (1 - k), s));
      r.base = null;
    } else {
      await r.sit(true);
      await r.play(g.clock, "reach");
      for (let k = 0; k < 2; k++) { g.sfx("squeak"); await g.wait(240); }
      const nutPlane = g.plane(`nut-${nut.n}`);
      if (nutPlane) nutPlane.show(false);
      await r.sit(false);
    }
    await g.wait(160);
  }
  await g.say("office.lot.grille.done.ranger");
  g.sfx("clunk");
  g.flag("office.grilleOff", true);                                            // (it leans on the unit, the nuts in a row in front of it)
  for (const n of [1, 2, 3, 4]) { const p = g.plane(`nut-${n}`); if (p) p.forced = {}; }
  r.face("W");
}
/** The switch: he reads the sticker's picture (a fan with a line through it), looks at the fan, and pulls. The fan runs
    down and stops, and the building's hum with it: from now on the Comfortable Room gets warmer (office.acOff, and the play
    time it happened, office.acOffAt: office-common.js works the heat out from it). Then Houston, on every speaker. */
async function pull(g) {
  const r = ranger(g);
  if (acOff(g)) return g.say("office.lot.switch.back.ranger");                // push it back up? No: the fans stay off
  await g.walkTo(M.switch[0], M.switch[1]);
  if (r) r.face("E");
  await g.say("office.lot.switch.use.ranger");
  if (r) { const pulling = r.play(g.clock, "pull", { ms: 1000 }); await g.wait(500); g.sfx("click"); swapSwitch(g, true); await pulling; }
  else swapSwitch(g, true);
  // the fan runs down: its frames slow to nothing (the backdrop's own fan, still, is under them), and the hum goes with it
  g.sfx("fanstop");
  const fan = g.plane("fan");
  if (fan && !g.clock.skipping) {
    let k = 1;
    const tick = fan.tick.bind(fan);
    fan.tick = (dt) => tick(dt * k);
    await g.tween(2400, (t) => { k = 1 - t; }, g.ease.out);
    fan.tick = tick;
  }
  g.flag("office.acOffAt", Math.round(g.store.data.playMs));
  g.flag("office.acOff", true);
  keepHeat(g);
  await g.wait(600);
  await g.pa("office.pa.air.1");
  await g.pa("office.pa.air.2");
  wendell(g, [400, 300]);
  await g.say("office.lot.wendell.air");                                      // (in the lot only: Wendell, into his earpiece)
  wendell(g);
  await g.pa("office.pa.air.3");
}
function swapSwitch(g, off) {
  const on = g.plane("switch"), down = g.plane("switch-off");
  if (on) on.show(!off);
  if (down) down.show(off);
}
/** In at the intake, the grille off and the fan stopped: to find Joe. Up onto the sill, and in; the ducts, at `intake`. */
async function goIn(g) {
  const r = ranger(g);
  if (!acOff(g)) return g.say("office.lot.grille.use.ranger");                // the fan turning: he leans back from it
  await g.walkTo(M.intake[0], M.intake[1]);
  if (r) r.face("N");
  await g.say("office.lot.in.ranger");
  if (r && !g.clock.skipping) {
    const [x0, y0] = [r.x, r.y], s0 = r.scale;
    r.base = M.intake[1] + 0.5;
    await g.tween(320, (k) => r.place(x0 + (SILL.at[0] - x0) * k, y0 + (SILL.at[1] - y0) * k - 8 * Math.sin(Math.PI * k), s0 + (SILL.scale - s0) * k));
    await g.tween(300, (k) => r.fade(1 - k));
  }
  g.flag("office.inside", true);
  await g.goto("office-ducts", { via: "fade", spawn: "intake", card: false });
}

// ---------- the limousine ----------
async function hood(g) {
  const r = ranger(g);
  if (r && !g.clock.skipping) {                                                // he hops up on the hood, and down: the roof is too far
    const [x, y] = [r.x, r.y], s = r.scale;
    await g.tween(260, (k) => r.place(x + 8 * k, y - 22 * Math.sin((Math.PI / 2) * k), s));
    await g.wait(300);
    await g.tween(260, (k) => r.place(x + 8 * (1 - k), y - 22 * Math.cos((Math.PI / 2) * k), s));
    r.place(x, y, s);
  }
  await g.say("office.lot.limo.use.ranger");
}

// ---------- now and then: Wendell to the gate; and his report of the raccoon ----------
const CHAT = chatter(nowAndThen["office-lot"], { first: [16, 24], every: [40, 60] });
const lot = { reportAt: null };
function tick(g, dt) {
  keepHeat(g);
  if (!g.scene || g.scene.id !== "office-lot") return;
  // a little after the can is tipped: Wendell tells Houston, and Houston tells the building
  if (is(g, "office.trash") && !is(g, "office.reported") && g.mode === "play" && !g.busy && !g.dialogue.active && !g.dialogue.choosing && !g.ui.open) {
    if (lot.reportAt == null) lot.reportAt = g.store.data.playMs + 4000;
    if (g.store.data.playMs >= lot.reportAt) {
      lot.reportAt = null;
      g.flag("office.reported", true);
      g.run(async () => {
        wendell(g, [400, 300]);
        await g.say("office.lot.trash.report");
        wendell(g);
        await g.pa("office.pa.raccoon");
      }, { settle: false });
      return;
    }
  }
  CHAT.tick(g, dt);
}

// ---------- the looks that change with the story ----------
const unitLook = (g) => g.say(!onRoof(g) ? "office.lot.unit.ranger" : acOff(g) ? "office.lot.unit.off.ranger" : "office.lot.unit.roof.ranger");
const switchLook = (g) => g.say(acOff(g) ? "office.lot.switch.off.ranger" : "office.lot.switch.ranger");

export default {
  id: "office-lot",
  era: "nevada",
  name: "The Office: the lot",
  building: BUILDING,                                      // (Houston on the speakers is heard here: g.pa)
  music: "office",

  // DEPTH (layout.json: the lens 4.9 m up, square on to the building). Two floors, joined only by Ranger's climb.
  horizon: 140, full: 588,
  walk: [
    { name: "gravel", area: GRAVEL,
      away: { ranger: (g) => climbDown(g) } },                                 // clicked from the roof: down the pipe again
    { name: "roof", area: ROOF, horizon: 140, full: ROOF_FULL,
      away: { ranger: (g) => (canUnder(g) ? climbUp(g) : g.say("office.lot.unit.use.ranger")) } },
  ],
  blocked: [[[114.5, 437.6], [115.0, 434.6], [110.6, 432.4], [102.5, 431.6], [92.7, 432.4], [83.8, 434.6], [78.1, 437.6], [77.2, 440.7], [81.5, 443.1], [89.9, 443.9], [100.0, 443.1], [109.1, 440.7]]],   // the flagpole's foot

  spawn: { default: M.fromLimo, ...M },                   // (no mark called `ranger`: g.where names the mark he is on, and his own name would win a tie)
  facing: "W",
  exits: ["office-ducts"],                                 // (no ways out at the edges: in by the intake, out by the map)
  stock: STOCK,                                            // SCENES-17: the Office's own stock replies (Ranger's are thoughts)
  announce: ANNOUNCE,
  get wordsAt() { return WORDS.at; },
  tick,

  picture: art + "back.png",
  planes: [
    // the fan behind the intake grille, turning, until the switch is pulled (stopped, it is the backdrop's own fan)
    { id: "fan", frames: [0, 1, 2, 3].map((n) => art + `fan-${n}.png`), fps: 12, at: [345, 215], foot: [27, 48], plane: "back", when: (g) => !acOff(g) },
    { id: "grille", src: art + "grille.png", plane: "back", when: (g) => !grilleOff(g) },
    ...[1, 2, 3, 4].map((n) => ({ id: `nut-${n}`, src: art + `nut-${n}.png`, plane: "back", when: (g) => !grilleOff(g) })),
    { id: "switch", src: art + "switch.png", plane: "back", when: (g) => !acOff(g) },
    { id: "door", src: art + "door.png", plane: "back" },
    { id: "awning", src: art + "awning.png", base: 443.7 },
    { id: "trash", src: art + "trash.png", base: 439.1, when: (g) => !is(g, "office.trash"),
      solid: [[404.8, 432.9], [401.3, 428.9], [392.6, 426.5], [381.7, 426.5], [372.7, 428.9], [368.9, 432.9], [371.9, 437.1], [380.9, 439.7], [392.2, 439.7], [401.4, 437.1]] },
    { id: "flagpole", src: art + "flagpole.png", base: 437.6,
      solid: [[114.5, 437.6], [115.0, 434.6], [110.6, 432.4], [102.5, 431.6], [92.7, 432.4], [83.8, 434.6], [78.1, 437.6], [77.2, 440.7], [81.5, 443.1], [89.9, 443.9], [100.0, 443.1], [109.1, 440.7]] },
    { id: "pennant", frames: [0, 1, 2, 3].map((n) => art + `pennant-${n}.png`), fps: 3, at: [126, 70], foot: [30, 26], base: 437.6 },
    { id: "limo", src: art + "limo.png", base: 393.1, when: (g) => !is(g, "office.arrived"),
      solid: [[507.2, 393.8], [800.0, 393.8], [778.4, 362.8], [494.1, 362.8]] },
    { id: "front", src: art + "front.png", plane: "front" },
    // the states (each replaces what it says): the grille off, leaning on the unit; the switch down; the door open (the
    // arrival's: a script shows it); the can tipped, and under the pipe; the limousine's back door left open
    { id: "grille-off", src: art + "grille-off.png", plane: "back", when: grilleOff,
      solid: [[248.7, 232.1], [309.8, 232.1], [311.7, 230.2], [251.9, 230.2]] },
    { id: "switch-off", src: art + "switch-off.png", plane: "back", when: acOff },
    { id: "door-open", src: art + "door-open.png", plane: "back", when: () => false },
    { id: "trash-tipped", src: art + "trash-tipped.png", base: 450.5, when: tipped,
      solid: [[374.0, 443.6], [429.9, 459.0], [449.6, 445.9], [395.0, 431.7]] },
    { id: "trash-pipe", src: art + "trash-pipe.png", base: 439.1, when: canUnder,
      solid: [[457.4, 432.9], [453.2, 428.9], [444.0, 426.5], [433.2, 426.5], [424.6, 428.9], [421.5, 432.9], [425.3, 437.1], [434.7, 439.7], [446.0, 439.7], [454.7, 437.1]] },
    { id: "limo-door-open", src: art + "limo-door-open.png", base: 393.1, when: (g) => is(g, "office.arrived"),
      solid: [[507.2, 393.8], [600.8, 393.8], [608.6, 403.7], [637.8, 403.7], [628.9, 393.8], [800.0, 393.8], [778.4, 362.8], [494.1, 362.8]] },
  ],

  // Wendell on the door, facing the gate, by regulation: his birthday button on his lapel (PEOPLE-17's suit3-birthday).
  actors: [
    { id: "suit3", kind: "suit3-birthday", at: M.door, face: "W", life: { fidget: [6, 12], still: true } },
  ],

  // Back to front: a later area lies over an earlier one. The desert first (everything else is over it).
  hotspots: [
    { id: "desert", name: "desert", poly: [[0, 112], [800, 112], [800, 318.9], [496, 318.9], [452, 220], [418, 118], [186, 118], [178, 196], [108, 249], [108, 318.9], [0, 318.9]],
      walkTo: [240, 440], face: "N", look: { ranger: "office.lot.desert.ranger" }, use: { ranger: "office.lot.desert.use.ranger" } },
    { id: "gate", name: "gate", poly: [[0, 251], [60, 251], [60, 319], [0, 336], [0, 319]], walkTo: [40, 398], face: "NW",
      look: { ranger: "office.lot.gate.ranger" }, use: { ranger: "office.lot.gate.use.ranger" } },
    { id: "fenceSign", name: "sign on the gate", poly: [[46.6, 269.7], [26.5, 273.3], [26.5, 290.2], [46.6, 286.0]], walkTo: [40, 398], face: "NW",
      look: { ranger: "office.lot.fencesign.ranger" }, use: { ranger: "office.lot.fencesign.use.ranger" } },
    { id: "flagpole", name: "flagpole", poly: [[79, 433], [93, 38], [94, 37], [98, 37], [100, 39], [113, 428], [113, 432], [112, 438], [111, 440], [110, 441], [106, 443], [101, 444], [91, 444], [87, 443], [84, 442], [80, 438], [79, 436]],
      walkTo: [73.7, 447.5], face: "N", look: { ranger: "office.lot.flag.ranger" }, use: { ranger: "office.lot.flag.use.ranger" } },
    { id: "limo", name: "limousine", poly: [[499, 320], [558, 301], [565, 300], [711, 300], [775, 321], [780, 323], [800, 333], [800, 392], [791, 393], [552, 393], [510, 392], [508, 388], [504, 379], [501, 372], [499, 321]],
      walkTo: [601.8, 400.2], face: "N", look: { ranger: "office.lot.limo.ranger" }, use: { ranger: hood } },
    { id: "limoDoor", name: "limousine's door", poly: [[588, 300], [630, 300], [630, 392], [588, 392]], walkTo: M.fromLimo, face: "N",
      when: (g) => is(g, "office.arrived"), look: { ranger: "office.lot.limo.door.ranger" }, use: { ranger: "office.lot.limo.door.ranger" } },
    { id: "window", name: "window", poly: [[152.4, 331.6], [194.4, 331.6], [194.4, 302.4], [152.4, 302.4]], walkTo: [166.2, 435.3], face: "N",
      look: { ranger: "office.lot.window.ranger" }, use: { ranger: "office.lot.window.use.ranger" } },
    { id: "sign", name: "sign", poly: [[123.8, 290.4], [430.4, 290.4], [430.4, 254.1], [123.8, 254.1]], walkTo: [278.5, 437.6], face: "N",
      look: { ranger: "office.lot.sign.ranger" }, use: { ranger: "office.lot.sign.use.ranger" } },
    { id: "door", name: "front door", poly: [[254.0, 426.2], [312.4, 426.2], [312.4, 303.5], [254.0, 303.5]], walkTo: [279.0, 436.4], face: "N",
      look: { ranger: "office.lot.door.ranger" }, use: { ranger: door } },
    { id: "keypad", name: "keypad", poly: [[318.2, 360.8], [330.5, 360.8], [330.5, 345.0], [318.2, 345.0]], walkTo: [322.9, 435.3], face: "N",
      look: { ranger: "office.lot.keypad.ranger" }, use: { ranger: keypad } },
    { id: "mat", name: "mat", poly: [[248.4, 442.0], [305.1, 442.0], [309.2, 428.9], [255.0, 428.9]], walkTo: [276.0, 443.7], face: "N",
      look: { ranger: "office.lot.mat.ranger" }, use: { ranger: mat } },
    { id: "suit3", name: "Wendell", verb: "Talk to", rect: [213, 326, 36, 108], walkTo: [262, 444], face: "W",
      look: { ranger: "office.lot.wendell.ranger" }, use: { ranger: wendellUse }, useWith: { bottlecap: wendellCap } },
    { id: "drainpipe", name: "drainpipe", verb: "Climb", poly: [[431.3, 247.5], [446.6, 247.5], [443.8, 371.4], [444.7, 385.7], [434.4, 385.7], [433.7, 371.4]],
      walkTo: M.climbFrom, face: "E", look: { ranger: "office.lot.pipe.ranger" }, use: { ranger: pipeUse } },
    // the trash can: by the wall; tipped over; under the pipe (three areas, one shown at a time)
    { id: "trash", name: "trash can", verb: "Tip", plane: "trash", when: (g) => !is(g, "office.trash"),
      poly: [[369, 397], [370, 390], [372, 388], [374, 387], [377, 386], [381, 385], [383, 385], [397, 386], [400, 387], [402, 388], [403, 389], [403, 427], [372, 435], [371, 435], [369, 400]],
      walkTo: M.trash, face: "E", look: { ranger: trashLook }, use: { ranger: trashUse }, useWith: { bottlecap: "office.lot.trash.with.bottlecap.ranger" } },
    { id: "trash-tipped", name: "trash can", verb: "Roll", plane: "trash-tipped", when: tipped,
      poly: [[378, 421], [380, 415], [382, 411], [384, 408], [387, 406], [393, 406], [398, 407], [427, 414], [429, 415], [430, 416], [453, 452], [453, 457], [452, 458], [449, 460], [445, 461], [438, 462], [434, 462], [427, 461], [424, 460], [420, 458], [381, 438], [380, 437], [379, 435], [378, 432]],
      walkTo: CAN.push, face: "E", look: { ranger: trashLook }, use: { ranger: trashUse }, useWith: { bottlecap: "office.lot.trash.with.bottlecap.ranger" } },
    { id: "trash-pipe", name: "trash can", verb: "Climb", plane: "trash-pipe", when: canUnder,
      poly: [[421, 398], [423, 389], [424, 388], [426, 387], [432, 385], [435, 385], [449, 386], [452, 387], [454, 388], [456, 390], [458, 399], [458, 400], [455, 414], [447, 427], [425, 435], [424, 435], [421, 400]],
      walkTo: M.climbFrom, face: "E", look: { ranger: trashLook }, use: { ranger: trashUse }, useWith: { bottlecap: "office.lot.trash.with.bottlecap.ranger" } },
    // the roof
    { id: "unit", name: "rooftop unit", poly: [[191.2, 221.6], [419.0, 221.6], [419.0, 105.8], [191.2, 105.8]], walkTo: M.intake, face: "N",
      look: { ranger: unitLook }, use: { ranger: unitLook } },
    { id: "grille", name: "grille", verb: "Unscrew", poly: [[314.6, 217.8], [375.3, 217.8], [375.3, 165.6], [314.6, 165.6]], walkTo: M.intake, face: "N",
      when: (g) => !grilleOff(g), look: { ranger: "office.lot.grille.ranger" }, use: { ranger: nuts } },
    ...[[312.7, 204.5], [362.0, 204.5], [312.7, 163.7], [362.0, 163.7]].map(([x, y], i) => ({
      id: `nut-${i + 1}`, name: "wing nut", verb: "Unscrew", rect: [x, y, 15.2, i < 2 ? 11 : 10.9], walkTo: NUTS[i].stand, face: "E",
      when: (g) => !grilleOff(g), look: { ranger: "office.lot.wingnuts.ranger" }, use: { ranger: nuts } })),
    // the grille off: the opening, the fan in it (turning, or stopped); and the grille itself, leaning on the unit
    { id: "grille-off", name: "grille", poly: [[247, 232], [311, 232], [311, 184], [247, 184]], walkTo: [300, 236], face: "N",
      when: grilleOff, look: { ranger: (g) => g.say(acOff(g) ? "office.lot.grille.open.ranger" : "office.lot.grille.off.ranger") }, use: { ranger: goIn } },
    { id: "intake", name: "intake", verb: "Go in", rect: [318, 167, 55, 48], walkTo: M.intake, face: "N",
      when: grilleOff, look: { ranger: (g) => g.say(acOff(g) ? "office.lot.fan.still.ranger" : "office.lot.fan.ranger") }, use: { ranger: goIn } },
    { id: "switch", name: "maintenance switch", verb: "Pull", poly: [[385.2, 223.1], [407.6, 223.1], [407.6, 200.2], [385.2, 200.2]], walkTo: M.switch, face: "E",
      look: { ranger: switchLook }, use: { ranger: pull } },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and as the stage is built for anything.
  setup(g) {
    keepHeat(g);
    CHAT.reset();
    lot.reportAt = null;
    shades(g);
  },

  async enter(g) {
    if (!is(g, "office.arrived")) { await g.cutscene("office-arrive"); return; }
  },
};

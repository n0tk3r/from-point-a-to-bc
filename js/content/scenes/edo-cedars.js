// Act Six, the second leg: the cedar path in the hills north of Osaka, at dusk, in spring rain (SCENES-20B: new in round
// twenty, replacing ENGINE-20's stub; briefs/SCENES-20.md, and the design, briefs/out/edo-design.md, #25). Stone steps
// climbing between towering cedars, trunk after trunk; the path narrows up the slope to a charcoal-burner's storehouse
// with a thatched roof; a small stone figure in a bib by the path; mist in the trees; a thin line of light under the
// storehouse's floor; a bamboo pipe in the hillside behind it (air for the room underneath, and the way a murmur of
// prayer comes out); a charcoal kiln of earth. Rain as the prints draw it: fine straight lines.
//
// The three of them come up the path from Osaka (the voyage, SCENES-20A's edo-sail, ends here on the mark `enter`):
// SCENES-21B (round twenty-one): from the Kyoto boat now (cutscenes/edo-boat.js: up the river with the puppet troupe, the ferry at
// Hirakata, the road north in the rain, ends here on the mark `enter`, edo.boated), as #32 Under The Cedars (round twenty's #25;
// acts/edo.js: it needs edo.boated); LEG_START.hills (edo-common.js) has the facts of Osaka before it. Everything below is as
// round twenty built it: the puzzles keep their old numbers here (#25 is #32, #26 is #33, #27 is #34).
//   #25 Under The Cedars   the door is barred from inside and nobody answers it (knock, then call out: the murmur stops,
//                          and the light under the floor goes out for a moment); the pipe in the hill: "The ground is
//                          PRAYING." (edo.pipeHeard); the high back window: Mom lifts Little Sister up, and she goes through
//                          (edo-storehouse.js: she lands on the sacks, alone, and unbars the door: edo.unbarred). The mat,
//                          the knock on the trapdoor and the way down are the storehouse's.
// After that the path is the way in and out of the storehouse; in the morning (#27) nobody goes out (Jinsuke keeps the
// door), and the path is seen only as the storehouse looks out at it (edo-hills.js toPath: the constable's climb).
//
// Every place is PAINT-20C's own measurement of the finished picture (art/scenes/edo-cedars/layout.json and its ready.md);
// where a place was set by eye the comment says so.
//
// Try it: index.html?scene=edo-cedars&lead=mom&flags=edo.arrived,edo.when,edo.clothes,edo.dressed,edo.fed,edo.west,edo.sailed,edo.boated   (SCENES-21B: and edo.boated)
// (dressed by script: the hills always have the travel clothes on, LEG_START.hills in edo-common.js)

import { STOCK_DRESSED, is } from "./edo-common.js";
import { THREE, who, each, sunUp, raining, hats, TALK, keepBelow, passing, MATES } from "./edo-hills.js";

const art = "art/scenes/edo-cedars/";

// ---------- the path (layout.json: horizon 250, full 600; the ground climbs, so people halve in size from the foot to the door) ----------
const WALK = [[301, 600], [322, 560], [345, 520], [361, 488], [372, 462], [334, 452], [326, 438], [420, 436], [500, 434], [556, 430], [606, 436],
  [640, 448], [640, 462], [604, 470], [560, 466], [520, 462], [496, 458], [499, 462], [502, 488], [502, 520], [501, 560], [501, 600]];
const BLOCKED = [[[270, 520], [302, 520], [302, 530], [270, 530]], [[558, 410], [684, 410], [684, 426], [558, 426]], [[246, 436], [318, 432], [318, 452], [246, 454]]];
const M = { enter: [400, 580], figure: [340, 540], pipe: [612, 452], door: [404, 444], window: [536, 444], isukeFrom: [340, 596] };
const LIFT = [514, 447];               // Mom, a step to the left of the window's place, to lift her daughter up to it (set by eye)
const SILL = [524, 372];               // the window's sill: where Little Sister goes up to, and through (the window's rect [512, 340, 22, 28])

// ---------- what the path is doing now that is not saved (made again whenever the scene is built) ----------
const here = { lit: false, dark: false, tries: 0 };
/** The lamp in the storehouse window: lit for a moment as they come up the path (then put out: Big Sister saw it go), and
    lit again from the night the family is trusted (edo.trusted) until the sun is up. */
const windowLit = (g) => here.lit || (is(g, "edo.trusted") && !sunUp(g));
/** The line of lamplight under the floor: the lamps of the room below, out for a moment when somebody calls at the door; by
    day (from O-Rin's warning on) nothing so faint shows. */
const lightBelow = (g) => !here.dark && !is(g, "edo.watch");

// ---------- #25: the door, barred; calling out ----------
/** The door, before Little Sister has unbarred it: a knock (nobody answers), then a call (the murmur stops, the light under
    the floor goes out, and comes back), turn and turn about. After: in. */
async function door(g) {
  if (is(g, "edo.unbarred")) return g.goto("edo-storehouse", { spawn: "door" });
  if (here.tries++ % 2 === 0) { g.sfx("knock"); await g.wait(500); return g.say(`edo.cedars.door.use.${who(g)}`); }
  here.dark = true; g.follow();
  await g.say(`edo.cedars.call.${who(g)}`);
  await g.wait(1400);
  here.dark = false; g.follow();
}

// ---------- #25: the pipe in the hill ----------
async function pipe(g) {
  if (g.lead) g.lead.face("N");
  await g.wait(400);                                                           // (an ear to it)
  await g.say(`edo.cedars.pipe.use.${who(g)}`);
  if (!is(g, "edo.pipeHeard")) g.flag("edo.pipeHeard", true);
}

// ---------- #25: the high back window: Mom lifts her, and she goes through ----------
/** Little Sister at the window: Mom comes over and lifts her; up to the sill, and through. On the other side she lands on
    the sacks (edo-storehouse.js `enter`), alone: the others wait on the path until she unbars the door. */
async function window(g) {
  const me = who(g);
  if (me !== "lilsis") return g.say(`edo.cedars.window.use.${me}`);
  if (is(g, "edo.unbarred")) return g.say("edo.cedars.window.lilsis");          // (the door is open now: she uses the door)
  const lil = g.lead, mom = g.actor("mom");
  if (mom) await g.walkTo(LIFT[0], LIFT[1], "mom");
  if (mom) mom.face("NE");
  lil.face("N");
  await g.say("edo.cedars.window.use.lilsis");
  if (mom) mom.play(g.clock, "reach");
  lil.hold(true, "climb");
  const [x0, y0] = [lil.x, lil.y], s0 = lil.scale;
  await g.tween(800, (k) => lil.place(x0 + (SILL[0] - x0) * k, y0 + (SILL[1] - y0) * k - 10 * Math.sin(Math.PI * k), s0));
  lil.base = 446;                                                              // (in front of the wall she climbs: she is at the sill)
  await g.say("edo.cedars.window.in.1");
  await g.tween(350, (k) => lil.fade(1 - k));
  lil.hold(false);
  lil.base = null;
  passing.by = "window";
  await g.goto("edo-storehouse", { spawn: "windowIn" });                       // (a party of one: the storehouse's `party` is nobody before the door is unbarred)
}

// ---------- the scene ----------
export default {
  id: "edo-cedars",
  era: "edo",
  name: "The cedar path",
  // (no `music`: the era's own track, `edo`, as ENGINE-20 has it; the room underground has `edo-hidden`)

  horizon: 250, full: 600,
  walk: { area: WALK },
  blocked: BLOCKED,
  spawn: { default: M.enter, ...M },
  // up the path from the river: the other two a step either side of whoever leads; out of the storehouse's door: beside it
  arrive: { enter: [[452, 586], [352, 588]], door: [[372, 448], [446, 452]] },
  facing: "N",
  party: () => THREE,
  exits: ["edo-storehouse"],
  stock: STOCK_DRESSED,
  talk: TALK,

  picture: art + "back.png",
  planes: [
    { id: "light-on", src: art + "light-on.png", plane: "back", when: lightBelow },
    { id: "window-lit", src: art + "window-lit.png", plane: "back", when: windowLit },
    { id: "cedar-l", src: art + "cedar-l.png", base: [[80, 574], [182, 516]] },
    { id: "cedar-r", src: art + "cedar-r.png", base: [[670, 518], [770, 572]] },
    { id: "front", src: art + "front.png", plane: "front" },
  ],
  // PAINT-20C's moving things (layout.json fx), in ENGINE-20's kinds. The rain's slant: the layout gives "-8" and, in the
  // same breath, "from upper left; the lines lean right as they fall; the wind from the left": the lines are drawn so
  // (the kind's slant +8: down and a little to the right). Its density, 0.0011 a square pixel, is about 530 drops at
  // once: 480 here. Its splashes on the treads (the painter's `splash: steps`): five lines across the steps.
  fx: [
    { id: "rain", type: "rain", when: raining, plane: "front", area: [[0, 0], [800, 0], [800, 600], [0, 600]], slant: 8, count: 480, length: [10, 22], speed: 520,
      color: "#dfe6ec", opacity: 0.42, behind: [[[302, 309], [568, 283.64], [568, 410], [302, 440]], [[242, 370], [318, 346], [318, 450], [242, 454]]],
      floor: [[[300, 592], [508, 592]], [[318, 562], [508, 562]], [[336, 532], [510, 532]], [[350, 502], [509, 502]], [[362, 474], [505, 474]]], splash: 2, sound: "rain", level: 0.5 },
    { id: "drip-1", type: "stream", when: raining, path: [[306, 327], [306, 434]], width: 1, color: "#cfd8e0", light: "#eef2f4", opacity: 0.5, speed: 90, splash: 2, base: 436 },
    { id: "drip-2", type: "stream", when: raining, path: [[438, 325], [438, 435]], width: 1, color: "#cfd8e0", light: "#eef2f4", opacity: 0.5, speed: 90, splash: 2, base: 436 },
    { id: "drip-3", type: "stream", when: raining, path: [[560, 301.64], [560, 405]], width: 1, color: "#cfd8e0", light: "#eef2f4", opacity: 0.5, speed: 90, splash: 2, base: 406 },
    { id: "puddle-1", type: "ripples", when: raining, at: [392, 585], radius: [1, 14], flat: 0.3, every: [0.4, 1.4], rings: 1, speed: 16, color: "#c8d4dc", opacity: 0.5, clip: [[372, 585], [412, 585], [412, 591], [372, 591]] },
    { id: "puddle-2", type: "ripples", when: raining, at: [440, 540], radius: [1, 10], flat: 0.3, every: [0.4, 1.4], rings: 1, speed: 14, color: "#c8d4dc", opacity: 0.5, clip: [[425, 540], [455, 540], [455, 545], [425, 545]] },
    { id: "puddle-3", type: "ripples", when: raining, at: [418, 506], radius: [1, 8], flat: 0.3, every: [0.5, 1.6], rings: 1, speed: 12, color: "#c8d4dc", opacity: 0.45, clip: [[407, 506], [429, 506], [429, 510], [407, 510]] },
    { id: "mist-l", type: "smoke", at: [120, 400], height: 60, width: [120, 220], lean: [160, -20], rise: 2, rate: 0.5, gust: 0.2, color: "#c3cbd3", opacity: 0.14, plane: "back" },
    { id: "mist-r", type: "smoke", at: [700, 390], height: 60, width: [120, 220], lean: [-150, -24], rise: 2, rate: 0.5, gust: 0.2, color: "#c3cbd3", opacity: 0.14, plane: "back" },
  ],

  // (The constable on his way up, in the morning, is never a person of this scene: nobody is out on the path then, since
  // Jinsuke keeps the door (edo-storehouse.js); he is seen only in the storehouse's looks out at the path (edo-hills.js
  // toPath), which put him on his step themselves. The looks at him, edo.cedars.isuke.*, are said there.)

  // Back to front: a later area lies over an earlier one (the other two first: edo-hills.js MATES).
  hotspots: [
    ...MATES,
    { id: "cedars", name: "cedars", poly: [[0, 0], [800, 0], [800, 300], [560, 330], [540, 420], [300, 420], [290, 330], [0, 300]], walkTo: [404, 520], face: "N",
      look: each("edo.cedars.cedars"), use: each("edo.cedars.cedars.use") },
    { id: "mist", name: "mist", poly: [[0, 280], [280, 300], [300, 372], [0, 400]], walkTo: [380, 500], face: "W", look: each("edo.cedars.mist"), use: each("edo.cedars.mist.use") },
    { id: "rain", name: "rain", poly: [[0, 0], [800, 0], [800, 240], [0, 240]], walkTo: [404, 540], face: "N", look: each("edo.cedars.rain"), use: each("edo.cedars.rain.use") },
    // (the stone steps are the path the family walks on: only the bottom treads are the thing to click, so that a click
    // anywhere else on them walks there)
    { id: "steps", name: "stone steps", poly: [[294, 586], [510, 586], [511, 600], [290, 600]], walkTo: [410, 560], face: "N",
      look: each("edo.cedars.steps"), use: each("edo.cedars.steps.use") },
    { id: "storehouse", name: "storehouse", poly: [[304, 438], [304, 313], [354, 249], [502, 229.18], [566, 287.64], [554, 408], [486, 432]], walkTo: [430, 448], face: "N",
      look: each("edo.cedars.storehouse"), use: each("edo.cedars.storehouse.use") },
    { id: "eaves", name: "eaves", poly: [[304, 327], [566, 301.64], [566, 285.64], [304, 311]], walkTo: [430, 448], face: "N", look: each("edo.cedars.eaves"), use: each("edo.cedars.eaves.use") },
    { id: "light", name: "light under the floor", poly: [[318, 439], [486, 433], [486, 417], [318, 423]], walkTo: [404, 444], face: "N",
      look: each("edo.cedars.light"), use: each("edo.cedars.light.use") },
    { id: "door", name: "door", poly: [[384, 428], [428, 427], [428, 345], [384, 346]], walkTo: M.door, face: "N", when: (g) => !is(g, "edo.unbarred"),
      look: each("edo.cedars.door"), use: door, verb: "Knock at" },
    { id: "door-in", name: "storehouse door", poly: [[384, 428], [428, 427], [428, 345], [384, 346]], walkTo: M.door, face: "N", when: (g) => is(g, "edo.unbarred"),
      look: each("edo.cedars.door.open"), use: door, verb: "Go in by" },
    { id: "window", name: "high window", rect: [512, 340, 22, 28], walkTo: M.window, face: "N", look: each("edo.cedars.window"), use: window },
    { id: "kiln", name: "charcoal kiln", poly: [[556, 424], [656, 424], [654, 402], [616, 382], [596, 382], [558, 402]], walkTo: [566, 452], face: "E",
      look: each("edo.cedars.kiln"), use: each("edo.cedars.kiln.use") },
    { id: "figure", name: "stone figure", rect: [272, 482, 28, 48], walkTo: M.figure, face: "W", look: each("edo.cedars.figure"), use: each("edo.cedars.figure.use") },
    { id: "pipe", name: "bamboo pipe", rect: [636, 354, 34, 24], walkTo: M.pipe, face: "N", look: each("edo.cedars.pipe"), use: pipe, verb: "Listen at" },
  ],

  setup(g) {
    here.dark = false; here.tries = 0;
    hats(g, true);                                                             // (out in the rain: the hats on)
    keepBelow(g);
    // the first evening, coming up the path: the lamp in the storehouse window is lit, until they are seen
    here.lit = !is(g, "edo.cedarsSeen");
  },

  // Coming up the path the first time: a bell a long way off, the lamp in the window, and then it goes out. (Big Sister
  // saw it go: her look at the storehouse says so.)
  async enter(g) {
    if (is(g, "edo.cedarsSeen")) return;
    g.sfx("bell");
    await g.wait(1300);
    here.lit = false;
    g.flag("edo.cedarsSeen", true);
  },
};


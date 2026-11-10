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
// PAINT-23 (round twenty-three: tools/paint/DEPTH.md, RECOMPOSE, and the act's watercolour): the picture is painted again
// from a new place, and every number below is measured again from it. We stand at the foot of the path under a great cedar
// (the front plane: its trunk up the left edge, a bough across the top right corner) and look UP the hill: the steps come in
// at the bottom left and climb in a curve to the storehouse standing higher up on the right, three-quarters on and seen from
// below (the door in its left wall, up two steps; the high window in its right wall, the wall Mom stands beside to lift her;
// the dark under its raised floor along both walls, and the line of lamplight in it); the kiln up to the left of the yard,
// the cut bank with the pipe at the right behind the storehouse's far end, the stone figure right of the lower steps; a cedar
// either side that people walk behind (cedar-l on the way to the kiln, cedar-r on the way to the pipe). The ground people
// walk on is one plane that climbs away from us: `horizon` (340) is that plane's own vanishing line and `full` (600) its
// full-size row, so the engine's sizes are true on it (edo_cedars_kit.py HillCam; eye level is lower, at row 464). Ids, names,
// logic, lines and puzzles are as they were.
//
// Every place is the painter's own measurement of the finished picture (art/scenes/edo-cedars/layout.json: tools/paint/
// edo_cedars_layout.py writes it and prints these numbers); where a place was set by eye the comment says so.
//
// Try it: index.html?scene=edo-cedars&lead=mom&flags=edo.arrived,edo.when,edo.clothes,edo.dressed,edo.fed,edo.west,edo.sailed,edo.boated   (SCENES-21B: and edo.boated)
// (dressed by script: the hills always have the travel clothes on, LEG_START.hills in edo-common.js)

import { STOCK_DRESSED, is } from "./edo-common.js";
import { THREE, who, each, sunUp, raining, hats, TALK, keepBelow, passing, MATES } from "./edo-hills.js";

const art = "art/scenes/edo-cedars/";

// ---------- the path (layout.json: horizon 340, full 600; a grown-up is 153 px at the foot of the steps, 98 at the door, 90 at the pipe) ----------
const WALK = [[128, 600], [150, 584], [178, 568], [216, 553], [258, 541], [300, 533], [340, 525], [364, 514], [372, 505], [344, 503], [276, 503],
  [270, 488], [322, 486], [378, 482], [396, 484], [420, 490], [447, 499], [478, 511], [505, 519], [526, 510], [566, 501], [604, 494], [638, 488],
  [670, 483], [708, 478], [772, 485], [778, 494], [730, 500], [700, 508], [660, 512], [610, 520], [556, 532], [500, 540], [460, 542], [430, 543],
  [392, 553], [366, 562], [344, 572], [338, 584], [340, 600]];
const BLOCKED = [[[481, 496], [441, 484], [414, 490], [450, 500]]];      // (the flat stone before the door)
const M = { enter: [258, 589], figure: [334, 575], pipe: [742, 486], door: [412, 499], window: [626, 495], isukeFrom: [232, 598] };
const LIFT = [580, 502];               // Mom, a step to the left of the window's place, beside its wall, to lift her daughter up to it
const SILL = [578, 397];               // the window's sill: where Little Sister goes up to, and through (the window's rect [565, 366, 27, 39])
/** The storehouse's whole outline and the kiln's (the layout's house_outline, kiln_outline): the drifting mist passes behind them. */
const HOUSE = [[389, 468], [505, 500], [690, 463], [686, 376], [738, 375], [737, 354], [571, 229], [501, 207], [340, 352], [340, 373], [389, 372]];
const KILN = [[319, 466], [316, 440], [305, 423], [288, 412], [269, 408], [249, 412], [233, 423], [221, 440], [217, 466], [219, 472], [241, 475], [275, 475], [306, 472]];

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
  lil.base = 501;                                                              // (in front of the wall she climbs: she is at the sill)
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

  horizon: 340, full: 600,
  walk: { area: WALK },
  blocked: BLOCKED,
  spawn: { default: M.enter, ...M },
  // up the path from the river: the other two a step either side of whoever leads; out of the storehouse's door: beside it
  arrive: { enter: [[318, 586], [200, 592]], door: [[382, 512], [454, 513]] },
  facing: "N",
  party: () => THREE,
  exits: ["edo-storehouse"],
  stock: STOCK_DRESSED,
  talk: TALK,

  picture: art + "back.png",
  planes: [
    { id: "light-on", src: art + "light-on.png", plane: "back", when: lightBelow },
    { id: "window-lit", src: art + "window-lit.png", plane: "back", when: windowLit },
    { id: "cedar-l", src: art + "cedar-l.png", base: [[299, 515], [363, 515]] },
    { id: "cedar-r", src: art + "cedar-r.png", base: [[640, 543], [720, 543]] },
    { id: "front", src: art + "front.png", plane: "front" },
  ],
  // The painter's moving things (layout.json fx), in ENGINE-20's kinds. The rain's slant +8: down and a little to the right,
  // the wind from the left. 480 drops at once. It is not drawn where the thatch shelters the two walls and the dry ground
  // under it (`behind`: from the thatch's lower edge down to the drip line, each wall), and it splashes along six treads.
  // The three drips fall from the thatch's lower edge to the pebbles of the drip line. The mists pass behind the storehouse
  // (and the kiln): their `behind`.
  fx: [
    { id: "rain", type: "rain", when: raining, plane: "front", area: [[0, 0], [800, 0], [800, 600], [0, 600]], slant: 8, count: 480, length: [10, 22], speed: 520,
      color: "#dfe6ec", opacity: 0.42, behind: [[[502.7, 338.4], [737.9, 375], [741.9, 464.1], [505.2, 517.1]], [[340.1, 373.4], [502.7, 338.4], [505.2, 517.1], [339.4, 466.3]]],
      floor: [[[121, 596], [347, 593]], [[150, 572], [342, 573]], [[182, 555], [353, 559]], [[231, 540], [393, 547]], [[283, 528], [446, 533]], [[355, 517], [476, 521]]],
      splash: 2, sound: "rain", level: 0.5 },
    { id: "drip-1", type: "stream", when: raining, path: [[387.8, 363.1], [387.6, 481.1]], width: 1, color: "#cfd8e0", light: "#eef2f4", opacity: 0.5, speed: 90, splash: 2, base: 482 },
    { id: "drip-2", type: "stream", when: raining, path: [[563.3, 347.8], [566.7, 503.3]], width: 1, color: "#cfd8e0", light: "#eef2f4", opacity: 0.5, speed: 90, splash: 2, base: 504 },
    { id: "drip-3", type: "stream", when: raining, path: [[652.1, 361.6], [656.2, 483.3]], width: 1, color: "#cfd8e0", light: "#eef2f4", opacity: 0.5, speed: 90, splash: 2, base: 484 },
    { id: "puddle-1", type: "ripples", when: raining, at: [267, 592], radius: [1, 44], flat: 0.18, every: [0.4, 1.4], rings: 1, speed: 16, color: "#c8d4dc", opacity: 0.5, clip: [[212, 587], [322, 587], [322, 597], [212, 597]] },
    { id: "puddle-2", type: "ripples", when: raining, at: [264, 557], radius: [1, 30], flat: 0.18, every: [0.4, 1.4], rings: 1, speed: 14, color: "#c8d4dc", opacity: 0.5, clip: [[226, 554], [302, 554], [302, 559], [226, 559]] },
    { id: "puddle-3", type: "ripples", when: raining, at: [372, 546], radius: [1, 26], flat: 0.18, every: [0.5, 1.6], rings: 1, speed: 12, color: "#c8d4dc", opacity: 0.45, clip: [[340, 544], [404, 544], [404, 548], [340, 548]] },
    { id: "mist-l", type: "smoke", at: [150, 432], height: 64, width: [120, 230], lean: [170, -22], rise: 2, rate: 0.5, gust: 0.2, color: "#c3cbd3", opacity: 0.14, plane: "back",
      behind: [HOUSE, KILN] },
    { id: "mist-r", type: "smoke", at: [770, 398], height: 60, width: [110, 210], lean: [-150, -26], rise: 2, rate: 0.5, gust: 0.2, color: "#c3cbd3", opacity: 0.14, plane: "back",
      behind: [HOUSE] },
  ],

  // (The constable on his way up, in the morning, is never a person of this scene: nobody is out on the path then, since
  // Jinsuke keeps the door (edo-storehouse.js); he is seen only in the storehouse's looks out at the path (edo-hills.js
  // toPath), which put him on his step themselves. The looks at him, edo.cedars.isuke.*, are said there.)

  // Back to front: a later area lies over an earlier one (the other two first: edo-hills.js MATES).
  hotspots: [
    ...MATES,
    // (the storehouse's own areas lie between the two cedars that stand before it: a click on either trunk is a click on the
    // cedars, whose outline runs down both trunks and along the roof)
    { id: "cedars", name: "cedars", poly: [[0, 0], [800, 0], [800, 362], [699, 398], [699, 470], [650, 471], [650, 289], [571, 229], [501, 207], [351, 342], [351, 470], [110, 470],
      [100, 600], [0, 600]], walkTo: [300, 548], face: "N",
      look: each("edo.cedars.cedars"), use: each("edo.cedars.cedars.use") },
    { id: "mist", name: "mist", poly: [[98, 250], [316, 250], [316, 400], [200, 440], [98, 440]], walkTo: [296, 550], face: "NW", look: each("edo.cedars.mist"), use: each("edo.cedars.mist.use") },
    { id: "rain", name: "rain", poly: [[0, 0], [800, 0], [800, 150], [0, 150]], walkTo: [304, 546], face: "N", look: each("edo.cedars.rain"), use: each("edo.cedars.rain.use") },
    // (the stone steps are the path the family walks on: only the bottom treads are the thing to click, so that a click
    // anywhere else on them walks there)
    { id: "steps", name: "stone steps", poly: [[115, 600], [353, 600], [348, 588], [143, 586]], walkTo: [262, 574], face: "N",
      look: each("edo.cedars.steps"), use: each("edo.cedars.steps.use") },
    { id: "storehouse", name: "storehouse", poly: [[389, 468], [505, 500], [650, 471], [650, 289], [571, 229], [501, 207], [351, 342], [351, 373], [389, 372]], walkTo: [470, 521], face: "N",
      look: each("edo.cedars.storehouse"), use: each("edo.cedars.storehouse.use") },
    { id: "eaves", name: "eaves", poly: [[351, 371], [503, 338], [650, 361], [650, 337], [502, 308], [351, 349]], walkTo: [470, 521], face: "N", look: each("edo.cedars.eaves"), use: each("edo.cedars.eaves.use") },
    { id: "light", name: "light under the floor", poly: [[389, 468], [505, 500], [650, 471], [650, 453], [504, 451], [389, 454]], walkTo: [470, 521], face: "N",
      look: each("edo.cedars.light"), use: each("edo.cedars.light.use") },
    { id: "door", name: "door", poly: [[450, 448], [481, 447], [480, 354], [449, 360]], walkTo: M.door, face: "NE", when: (g) => !is(g, "edo.unbarred"),
      look: each("edo.cedars.door"), use: door, verb: "Knock at" },
    { id: "door-in", name: "storehouse door", poly: [[450, 448], [481, 447], [480, 354], [449, 360]], walkTo: M.door, face: "NE", when: (g) => is(g, "edo.unbarred"),
      look: each("edo.cedars.door.open"), use: door, verb: "Go in by" },
    { id: "window", name: "high window", rect: [565, 366, 27, 39], walkTo: M.window, face: "NW", look: each("edo.cedars.window"), use: window },
    { id: "kiln", name: "charcoal kiln", poly: [[313, 436], [305, 423], [288, 412], [269, 408], [249, 412], [233, 423], [221, 440], [217, 466], [219, 472], [241, 475], [275, 475], [306, 472], [313, 469]],
      walkTo: [292, 494], face: "NW", look: each("edo.cedars.kiln"), use: each("edo.cedars.kiln.use") },
    { id: "figure", name: "stone figure", rect: [398, 510, 24, 65], walkTo: M.figure, face: "E", look: each("edo.cedars.figure"), use: each("edo.cedars.figure.use") },
    { id: "pipe", name: "bamboo pipe", rect: [716, 398, 51, 21], walkTo: M.pipe, face: "N", look: each("edo.cedars.pipe"), use: pipe, verb: "Listen at" },
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


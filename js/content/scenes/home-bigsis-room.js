// Act Three, the fifth of its five scenes: the attic. Big Sister asked for it for her thirteenth birthday and has made
// it, by herself and on pocket money, into THE RETREAT: soft light, quiet music, order, calm. It is reached from the
// landing by the attic ladder. The room is perfectly calm and tonight she is not, and it annoys her.
//
// What happens here:
//   chain B   Little Sister's flashlight is dead, and the only batteries of that size in the house are in the sound
//             machine on the low table. Only Big Sister takes them: it is her room and her machine (Mom will not take
//             a daughter's things; Little Sister may touch nothing up here, by rule and by treaty). She does it as a
//             sacrifice she intends to mention again. The music stops, and from then on the house's own tune is heard
//             up here too. Batteries and flashlight then have to meet in one pair of hands (`given`, below).
//   the timeline   her long strip of paper over the bookcase. It is where the game says how it counts the years:
//             by Archbishop Ussher's dates, from the Bible's own genealogies; and what B.C. and A.D. mean.
//   the rules   her notice by the hatch: shoes off, voices down, no chickens. Under the third, in crayon, an appeal.
// The three of them go through the house together (`party`): see home-living-room.js.
//
// Every place below is measured from the finished painting (art/scenes/home-bigsis-room/layout.json is the painter's own list).
//
// Try it: index.html?scene=home-bigsis-room&lead=bigsis&flags=home.arrived
// Later states: &flags=home.arrived,home.sawRetreat,home.sawTimeline,home.flashTaken,home.retreatQuiet,home.flashWorks

const art = "art/scenes/home-bigsis-room/";

const THREE = ["mom", "bigsis", "lilsis"];
const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
const who = (g) => g.store.data.active;
/** Are the three of them on stage? (A test, or a visitor from another act, can walk somebody else in.) */
const home = (g) => THREE.every((id) => g.actor(id));
/** The other two turn to look at a place. */
const turn = (g, at) => { for (const id of THREE) { const a = g.actor(id); if (a && a !== g.lead) a.look(at[0], at[1]); } };

// ---------- the light ----------
// Drawn live: the sound machine's little lamp, which is lit while it plays. (The thread of mist from the diffuser, drawn
// here until round four, is the engine's now, with the candles and the little fountain: see `fx`.)
const LAMP = [383, 325];
function light(g) {
  const lamp = g.q("#sound-lamp");
  if (lamp) lamp.setAttribute("opacity", g.flag("home.retreatQuiet") ? 0 : 1);
}

// ---------- the rules, on their easel by the hatch ----------
// The notice as the close-up shows it (the kit draws the sheet of paper: js/art/kit.js, `paper`). The last line is
// not in Big Sister's lettering: it is her sister's, in red crayon, in the neatest print in the house (`print`).
const RULES = {
  tape: false, tilt: 0.8, width: 500, tint: "#f6f1e6",
  lines: [
    { text: "THE RETREAT", size: 50, gap: 34, fill: "#33406e" },
    { text: "1. SHOES OFF", size: 36, anchor: "start" },
    { text: "2. VOICES DOWN", size: 36, anchor: "start" },
    { text: "3. NO CHICKENS", size: 36, anchor: "start", gap: 10 },
    { text: "AN APPEAL HAS BEEN LODGED", size: 21, anchor: "end", fill: "#d2452f", hand: true },
  ],
};
async function readRules(g) {
  g.closeup(g.art.paper(RULES), "The rules of the Retreat", { grid: [800, 600] });
  await g.say(`home.rules.${who(g)}`);
}

// ---------- the timeline: how the game counts the years ----------
const MARK = [404, 286];                         // the red mark, three quarters of the way along
/** The first time any of them looks along it, the three of them read it between them. After that, each has her own word. */
async function timeline(g) {
  const me = who(g);
  if (!g.flag("home.sawTimeline") && home(g)) {
    g.flag("home.sawTimeline", true);
    turn(g, MARK);
    await g.say("home.timeline.1", "home.timeline.2", "home.timeline.3", "home.timeline.4", "home.timeline.5", "home.timeline.6");
    await g.say("home.timeline.bigsis", "home.timeline.bigsis2", "home.timeline.mom", "home.timeline.lilsis");
    return;
  }
  if (me !== "bigsis") return g.say(`home.timeline.again.${me}`);
  await g.say(g.flag("home.timelineFact") ? "home.timeline.bigsis4" : "home.timeline.bigsis3");
  g.flag("home.timelineFact", true);
}

// ---------- chain B: the batteries are in her sound machine ----------
/** Batteries and flashlight in the same pockets: in they go, and it works. */
async function loadFlash(g, to) {
  const pockets = g.store.data.inventory[to];
  pockets.splice(pockets.indexOf("batteries"), 1);
  g.sfx("click");
  g.flag("home.flashWorks", true);
  await g.say(`home.flash.load.${to}`);
}

const TABLE = [339, 387];                        // where one stands at the sound table (its three things' walkTo, below)
const BACK = [[282, 396], [300, 420], [258, 414]];    // where the others step back to
/** The machine is small, and anybody standing in front of the table hides it. So whoever comes to the table has it to
    herself: the others step back to where they can watch, and she takes the place at its end. */
async function standBack(g) {
  const me = g.lead, others = THREE.map((id) => g.actor(id)).filter((a) => a && a !== me);
  const near = others.filter((a) => a.x > 335 && a.x < 455);             // (anybody standing between the table and us hides it, wherever her feet are)
  const taken = (m) => others.some((a) => !near.includes(a) && Math.abs(a.x - m[0]) < 30 && Math.abs(a.y - m[1]) < 12);
  const free = BACK.filter((m) => !taken(m));
  await Promise.all(near.map((a, n) => (free[n] ? g.walkTo(free[n][0], free[n][1], a.id).then(() => a.look(LAMP[0], LAMP[1])) : null)));
  if (Math.abs(me.x - TABLE[0]) > 3 || Math.abs(me.y - TABLE[1]) > 3) { await g.walkTo(TABLE[0], TABLE[1]); me.face("E"); }
}
const atTable = (action) => async (g) => { await standBack(g); return typeof action === "function" ? action(g) : g.say(action[who(g)]); };

async function soundMachine(g) {
  const me = who(g);
  if (g.flag("home.retreatQuiet")) return g.say(`home.sound.quiet.${me}`);
  const wanted = g.flag("home.flashTaken") && !g.flag("home.flashWorks");     // there is a dead flashlight in the house
  if (me !== "bigsis") return g.say(`home.sound.${wanted ? "take" : "use"}.${me}`);   // whose room it is, and whose machine
  if (!wanted) return g.say("home.sound.use.bigsis");
  turn(g, LAMP);
  await g.say("home.sound.give.1", "home.sound.give.2");
  await g.reach();
  g.sfx("hush");
  g.flag("home.retreatQuiet", true);             // the Retreat's own music stops...
  light(g);
  g.music(g.musicOf(g.scene));                   // ...and the house's tune is heard up here from now on
  await g.wait(900);
  g.give("batteries");
  await g.say("home.sound.give.3", "home.sound.give.4", "home.sound.give.5");
  if (g.has("lilflash")) await loadFlash(g, "bigsis");      // she happens to be holding the flashlight herself
}
const soundLook = (g) => g.say(`home.sound.${g.flag("home.retreatQuiet") ? "quiet" : "look"}.${who(g)}`);

// ---------- handing things on ----------
async function solveNote(g) {
  await g.say("home.note.solve.1", "home.note.solve.2", "home.note.solve.3");
  g.flag("home.knowsYear", true);
}
/** What the one who is handed something says. Big Sister is the one who can read Dad's note. */
async function given(g, item, to) {
  if (item === "note") { if (to === "bigsis" && !g.flag("home.knowsYear")) await solveNote(g); return; }
  if ((item === "batteries" || item === "lilflash") && g.holder("batteries") === to && g.holder("lilflash") === to) return loadFlash(g, to);
  await g.say(`home.give.${item}.${to}`);
}

export default {
  id: "home-bigsis-room",
  era: "home",
  name: "The Retreat",

  // Its own music, until the batteries come out of the sound machine: then the house's.
  music: (g) => (g.flag("home.retreatQuiet") ? "home" : "retreat"),

  // DEPTH, from the room's camera (layout.json).
  horizon: 120, full: 440,

  // The floor, from the low far wall (grown-ups cannot stand close under the roof there) to the hatch at the front left.
  // The desk's own ground is blocked by its cut-out (`solid`, below).
  walk: { area: [[203, 378], [483, 378], [488, 395], [562, 397], [618, 493], [589, 514], [98, 514]] },

  party: ["mom", "bigsis", "lilsis"],
  // (The painter's second mark, [373, 454], is straight in front of the sound table: whoever stood on it hid the machine.
  // That one mark is moved to the left, between the other two.)
  spawn: { default: [294, 456], mom: [294, 456], bigsis: [240, 470], lilsis: [188, 484], fromLadder: [294, 456] },
  arrive: { fromLadder: [[240, 470], [188, 484]] },
  exits: ["home-landing"],
  // The way out across the edges of the picture: the hatch is at the front, so the bottom of the picture is the way down.
  edges: {
    S: { to: "home-landing", spawn: "fromLadder", name: "down the ladder", walkTo: [172, 508] },
  },

  picture: art + "back.png",

  // CUT-OUTS. The desk and its stool stand on the floor; the hatch, the notice, the tea tray and the pouf are in front of everybody.
  planes: [
    { id: "desk", src: art + "desk.png", base: [[487, 379], [594, 379]], solid: [[483, 365], [584, 365], [603, 391], [491, 391]] },
    { id: "front", src: art + "front.png", plane: "front" },
  ],

  // THINGS THAT MOVE BY NATURE (round four: briefs/out/paint-4b-ready.md). The candles are flameless, in glass, as the
  // painting has them: the wax glows from inside, and what flickers is the little light in its top (its glow is painted).
  // The little fountain on the sound table runs all the time (a thread of water off the bamboo spout, rings on its
  // pool), and the diffuser on its stump breathes out a soft mist.
  fx: [
    // [id, at x, at y, base, size, width, glow]: six along the low wall's ledge (the last behind the gauze over the bed,
    // which lets about half of it through), two on the bookcase, two on the shelf over the pillows, two in the lanterns at
    // the bed's foot, and the tall glass by the towels
    ...[["ledge-1", 201.3, 266.2, 366, 2, 1.2, 6.3], ["ledge-2", 296.5, 266.2, 366, 2, 1.2, 6.3], ["ledge-3", 394.4, 266.2, 366, 2, 1.2, 6.3],
      ["ledge-4", 461.6, 266.2, 366, 2, 1.2, 6.3], ["ledge-5", 562.3, 266.2, 366, 2, 1.2, 6.3], ["ledge-6", 629.5, 266.2, 366, 2, 1.2, 6.3],
      ["bookcase-1", 175, 295.4, 370, 2, 1.2, 6.3], ["bookcase-2", 260.4, 297.3, 370, 2, 1.2, 6.3],
      ["bedshelf-1", 709.2, 308.8, 412, 2.2, 1.2, 7.5], ["bedshelf-2", 714, 313.9, 417, 2.2, 1.2, 7.6],
      ["foot-1", 648.8, 468, 484, 2.7, 1.2, 9.3], ["foot-2", 682.8, 479.3, 493, 2.7, 1.3, 9.5], ["floor", 96.4, 444.9, 463, 2.5, 1.2, 8.8]]
      .map(([id, x, y, base, size, width, glow]) => ({ id: `candle-${id}`, type: "flame", at: [x, y], base, size, width, color: "#fff2c8", edge: "#ffb45a", glow, glowColor: "#ffb070", glowOpacity: 0.1, flicker: 0.35,
        ...(id === "ledge-6" ? { behind: [[[643, 190], [580, 335], [700, 335]]], behindOpacity: 0.45 } : {}) })),
    // the little fountain: a thread of water from the bamboo spout onto the stones, and rings on its pool (raised water)
    { id: "fountain", type: "stream", base: 375, path: [[422.6, 315.1], [421.8, 317.3], [421.4, 320.6]], width: [0.8, 1.2], color: "#d6e8f2", light: "#ffffff", opacity: 0.75, speed: 26, splash: 1.5 },
    { id: "fountain-pool", type: "ripples", at: [421.1, 325.9], base: 375, radius: [1, 9.3], flat: 0.42, every: [0.5, 1.1], rings: 2, speed: 7, color: "#cfe4f4", trough: "#2c4a58", opacity: 0.45 },
    // the diffuser's mist, rising, spreading and fading
    { id: "diffuser-mist", type: "smoke", at: [151.6, 369.7], base: 414, color: "#f6f2f0", opacity: 0.16, height: 34, width: [2, 14], lean: [5, -34], rate: 2.5 },
  ],

  // LIGHT, drawn live. `light` (above) puts the machine's lamp out when its batteries have gone.
  live() {
    return `<g id="sound-lamp" fill="#ffd27a" shape-rendering="geometricPrecision"><circle cx="${LAMP[0]}" cy="${LAMP[1]}" r="4" opacity="0.28"/><circle cx="${LAMP[0]}" cy="${LAMP[1]}" r="1.4"/></g>`;
  },

  setup: light,

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    // (two skylights in the roof, each in its frame: the branch and the stars in the left one, the moon in the right)
    { id: "skylight", name: "skylight", rect: [216, 122, 119, 82], walkTo: [421, 419], face: "N", look: each("home.skylight") },
    { id: "skylight2", name: "skylight", rect: [465, 124, 123, 82], walkTo: [421, 419], face: "N", look: each("home.skylight") },
    { id: "window", name: "round window", poly: [[78, 205], [85, 208], [90, 217], [94, 231], [95, 247], [94, 263], [90, 277], [85, 286], [78, 289], [72, 286], [67, 277], [63, 263], [62, 247], [63, 231], [67, 217], [72, 208]], walkTo: [195, 405], face: "W", look: each("home.retreat.window") },
    { id: "plants", name: "plants", poly: [[98, 290], [128, 280], [172, 290], [186, 330], [186, 420], [112, 438], [100, 400], [98, 330]], walkTo: [170, 428], face: "W", look: each("home.plants") },
    { id: "towels", name: "robe and towels", poly: [[36, 276], [66, 276], [66, 388], [110, 402], [113, 477], [54, 477], [36, 388]], walkTo: [170, 428], face: "W", look: each("home.towels") },
    { id: "saltlamp", name: "salt lamp", poly: [[112, 337], [145, 337], [147, 368], [165, 370], [165, 414], [136, 414], [134, 403], [110, 403]], walkTo: [195, 405], face: "W", look: each("home.saltlamp") },
    { id: "bookcase", name: "bookcase", rect: [157, 296, 187, 74], walkTo: [244, 380], face: "N", look: each("home.books") },
    { id: "timeline", name: "timeline", verb: "Read", rect: [166, 273, 317, 23], walkTo: [305, 380], face: "N", look: timeline, use: timeline, useWith: { pencil: each("home.timeline.pencil") } },
    { id: "soundtable", name: "the sound table", rect: [360, 336, 82, 39], walkTo: [339, 387], face: "E", look: atTable(each("home.soundtable")) },
    {
      id: "machine", name: "sound machine", verb: "Open", rect: [362, 306, 42, 30], walkTo: [339, 387], face: "E",
      look: atTable(soundLook), use: atTable(soundMachine), useWith: { lilflash: atTable(soundMachine), batteries: atTable(each("home.sound.putback")) },
    },
    { id: "fountain", name: "fountain", rect: [405, 302, 34, 34], walkTo: [339, 387], face: "E", look: atTable(each("home.fountain")) },
    {
      id: "desk", name: "her writing desk", plane: "desk", poly: [[496, 276], [571, 276], [571, 302], [592, 302], [592, 389], [482, 389], [482, 302], [496, 302]], walkTo: [524, 398], face: "N",
      look: each("home.desk"), useWith: { pencil: each("home.desk.pencil") },
    },
    { id: "bed", name: "her bed", poly: [[638, 172], [660, 172], [718, 330], [770, 400], [770, 462], [620, 462], [572, 400], [572, 330]], walkTo: [571, 431], face: "E", look: each("home.bedbig") },
    { id: "mat", name: "exercise mat", poly: [[247, 397], [303, 397], [287, 458], [216, 458]], walkTo: [321, 426], face: "W", look: each("home.mat") },
    {
      // (She stands three pixels farther in than the painter's [172, 511]: on that spot there is no ground to either side, and the three end up standing in one another.)
      // (The area is the opening and the near side of its rail, below the floor where people stand when they come up.)
      id: "hatch", name: "the way down", verb: "Climb down", poly: [[21, 516], [244, 516], [244, 600], [21, 600]], walkTo: [172, 508], face: "S", plane: "front",
      look: each("home.hatch"), use: (g) => g.goto("home-landing", { spawn: "fromLadder" }),
    },
    { id: "rules", name: "the rules", verb: "Read", rect: [232, 470, 106, 109], walkTo: [172, 508], face: "S", plane: "front", look: readRules, use: readRules },
  ],

  given,

  // What they say to each other up here. What has not been heard comes first.
  talk: {
    mom: {
      bigsis: [
        { when: (g) => g.flag("home.flashTaken") && !g.flag("home.flashWorks") && !g.holder("batteries"), say: ["home.talk.batt.mom.bigsis.a", "home.talk.batt.mom.bigsis.b"] },
        { when: (g) => !g.flag("home.retreatQuiet"), say: ["home.talk.retreat.mom.bigsis.key.a", "home.talk.retreat.mom.bigsis.key.b"] },
        ["home.talk.retreat.mom.bigsis.1a", "home.talk.retreat.mom.bigsis.1b"],
        ["home.talk.retreat.mom.bigsis.2a", "home.talk.retreat.mom.bigsis.2b"],
      ],
      lilsis: [
        { when: (g) => !!g.holder("batteries") && !g.flag("home.flashWorks"), say: ["home.talk.batt.mom.lilsis.a", "home.talk.batt.mom.lilsis.b"] },
        ["home.talk.retreat.mom.lilsis.1a", "home.talk.retreat.mom.lilsis.1b"],
        ["home.talk.retreat.mom.lilsis.2a", "home.talk.retreat.mom.lilsis.2b"],
      ],
    },
    bigsis: {
      mom: [["home.talk.retreat.bigsis.mom.1a", "home.talk.retreat.bigsis.mom.1b"], ["home.talk.retreat.bigsis.mom.2a", "home.talk.retreat.bigsis.mom.2b", "home.talk.retreat.bigsis.mom.2c"]],
      lilsis: [["home.talk.retreat.bigsis.lilsis.1a", "home.talk.retreat.bigsis.lilsis.1b"], ["home.talk.retreat.bigsis.lilsis.2a", "home.talk.retreat.bigsis.lilsis.2b"]],
    },
    lilsis: {
      mom: [["home.talk.retreat.lilsis.mom.1a", "home.talk.retreat.lilsis.mom.1b"], ["home.talk.retreat.lilsis.mom.2a", "home.talk.retreat.lilsis.mom.2b"]],
      bigsis: [
        { when: (g) => g.flag("home.flashTaken") && !g.flag("home.flashWorks") && !g.holder("batteries"), say: ["home.talk.batt.lilsis.bigsis.a", "home.talk.batt.lilsis.bigsis.b"] },
        ["home.talk.retreat.lilsis.bigsis.1a", "home.talk.retreat.lilsis.bigsis.1b"],
        ["home.talk.retreat.lilsis.bigsis.2a", "home.talk.retreat.lilsis.bigsis.2b", "home.talk.retreat.lilsis.bigsis.2c"],
      ],
    },
  },

  // The first time up: boots off, voices down (in a manner of speaking), and what Mom makes of the room.
  async enter(g) {
    if (g.flag("home.sawRetreat") || !home(g) || !g.flag("home.arrived")) return;
    g.flag("home.sawRetreat", true);
    await g.wait(400);
    await g.say("home.retreat.first.1", "home.retreat.first.2", "home.retreat.first.3", "home.retreat.first.4");
  },
};

// Act Three, the second of its five scenes: the landing upstairs, seen from out over the living room.
// Three doors: the Son's (shut all act), Little Sister's (BEWARE OF CHICKENS) and Dad's study (locked, with a notice
// taped to it); and the attic ladder, let down from its hatch, with a card on it: THE RETREAT. That is Big Sister's.
//
// What happens here:
//   chain A   Dad's notice is a riddle: "Lost your key? It is with the other eighty-eight." Big Sister or Mom
//             works it out (a piano has eighty-eight keys); Little Sister cannot. Once Little Sister has fetched
//             the key out of the piano downstairs, whoever is holding it opens the study.
//   the Son's door   his spy-kit alarm wants a password. Little Sister knows it. Mom says: not tonight.
// The three of them go through the house together (`party`): see home-living-room.js.
//
// Every place below is measured from the painting (art/scenes/home-landing/layout.json is the painter's own list).
// The ladder stands just in front of the study door's left edge: people pass in front of its feet, not behind them.
//
// Try it: index.html?scene=home-landing&lead=bigsis&flags=home.arrived
// Later states: &flags=home.arrived,home.keyInPiano,home.hasKey,home.studyOpen

const art = "art/scenes/home-landing/";

const THREE = ["mom", "bigsis", "lilsis"];
const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
const who = (g) => g.store.data.active;
/** Are the three of them on stage? (A test, or a visitor from another act, can walk somebody else in.) */
const home = (g) => THREE.every((id) => g.actor(id));

// Dad's notice, as the close-up shows it (the kit draws the sheet of paper: js/art/kit.js, `paper`).
const NOTICE = {
  tape: true, tilt: -1.2,
  lines: [
    { text: "TRIP HEADQUARTERS", size: 44, gap: 26 },
    { text: "AUTHORIZED PERSONNEL ONLY", size: 25, gap: 44 },
    { text: "LOST YOUR KEY? IT IS WITH", size: 29 },
    { text: "THE OTHER EIGHTY-EIGHT.", size: 29, gap: 40 },
    { text: "- THE MANAGEMENT", size: 25, anchor: "end" },
  ],
};

// ---------- chain A: the notice on the study door ----------
async function readSign(g) {
  const me = who(g);
  g.closeup(g.art.paper(NOTICE), "Dad's notice on the study door", { grid: [800, 600] });
  if (me === "lilsis") return g.say("home.sign.lilsis");
  const other = me === "mom" ? "bigsis" : "mom";
  if (!g.flag("home.keyInPiano")) {              // the riddle, worked out: a piano has eighty-eight keys
    await g.say(`home.sign.${me}.1`, `home.sign.${me}.2`);
    g.flag("home.keyInPiano", true);
    g.flag("home.signRead", true);
    return g.say(`home.sign.${other}.react`);
  }
  if (!g.flag("home.signRead")) {                // they found the dead note first: now they know what made it
    g.flag("home.signRead", true);
    return g.say(`home.sign.thunk.${me}`);
  }
  await g.say(`home.sign.again.${me}`);
}

// ---------- chain A: the study door ----------
async function studyDoor(g) {
  const me = who(g);
  if (g.flag("home.studyOpen")) return g.goto("home-study", { spawn: "fromLanding" });
  const holder = g.holder("studykey");
  if (!holder) return g.say(`home.study.locked.${me}`);
  if (holder !== me) return g.say(`home.study.theirs.${me}.${holder}`);     // somebody else has it: say who
  await g.reach();
  g.sfx("unlock");
  await g.wait(450);
  g.flag("home.studyOpen", true);                // (the door stands open from now on: its cut-out follows this fact)
  await g.say(`home.study.unlock.${me}`);
  await g.goto("home-study", { spawn: "fromLanding" });
}
const studyLook = (g) => g.say(`home.study.${g.flag("home.studyOpen") ? "open" : "look"}.${who(g)}`);

// ---------- the Son's door: the one place in the act that is allowed to be sad ----------
async function sonDoor(g) {
  const me = who(g);
  if (me !== "lilsis") {                         // a knock sets the toy off. Neither of them has ever been told the password.
    await g.reach();
    g.sfx("alarm");
    await g.wait(600);
    return g.say(`home.son.use.${me}`);
  }
  if (g.flag("home.sonDoor")) return g.say("home.son.again");
  await g.reach();
  g.sfx("alarm");
  await g.wait(700);
  await g.say("home.son.alarm.1", "home.son.alarm.2");      // his own voice, on the toy's little speaker; and hers, doing his
  g.sfx("found");
  await g.wait(350);
  await g.say("home.son.alarm.3");
  const mom = g.actor("mom");
  if (mom) mom.look(g.lead.x, g.lead.y);
  await g.wait(400);
  await g.say("home.son.alarm.4", "home.son.alarm.5");      // Mom, quietly: not tonight
  g.sfx("latch");
  g.flag("home.sonDoor", true);
}

// ---------- handing things on ----------
async function solveNote(g) {
  await g.say("home.note.solve.1", "home.note.solve.2", "home.note.solve.3");
  g.flag("home.knowsYear", true);
}
/** Batteries and flashlight in the same pockets: in they go, and it works. */
async function loadFlash(g, to) {
  const pockets = g.store.data.inventory[to];
  pockets.splice(pockets.indexOf("batteries"), 1);
  g.sfx("click");
  g.flag("home.flashWorks", true);
  await g.say(`home.flash.load.${to}`);
}
/** What the one who is handed something says. Big Sister is the one who can read Dad's note. */
async function given(g, item, to) {
  if (item === "note") { if (to === "bigsis" && !g.flag("home.knowsYear")) await solveNote(g); return; }
  if ((item === "batteries" || item === "lilflash") && g.holder("batteries") === to && g.holder("lilflash") === to) return loadFlash(g, to);
  await g.say(`home.give.${item}.${to}`);
}

// The little lamp on the Son's toy alarm, beside his door handle. Light, so it is drawn live.
const ALARM = [455, 237];

export default {
  id: "home-landing",
  era: "home",
  name: "The landing",

  // DEPTH, from the room's camera (layout.json).
  horizon: 135, full: 322,

  // A strip of floor behind the railing, from the top of the stairs (far left) to the study door (near right).
  // The hall table and the hamper stand against the wall, behind its far edge.
  walk: { area: [[373, 253], [785, 329], [783, 364], [325, 264]] },

  party: ["mom", "bigsis", "lilsis"],
  spawn: {
    default: [431, 279], mom: [431, 279], bigsis: [375, 263], lilsis: [337, 262],
    fromStairs: [431, 279], fromLilsis: [590, 308], fromStudy: [721, 324],
    fromLadder: [718, 325],   // at the foot of the ladder
  },
  arrive: {
    fromStairs: [[375, 263], [337, 262]], fromLilsis: [[541, 290], [476, 287]], fromStudy: [[635, 318], [578, 301]],
    fromLadder: [[642, 328], [756, 345]],
  },
  exits: ["home-living-room", "home-study", "home-lilsis-room", "home-bigsis-room"],

  picture: art + "back.png",

  // CUT-OUTS. The whole railing is in front of everybody: people are seen through its balusters from the knee down.
  planes: [
    { id: "study-open", src: art + "study-open.png", base: [[695, 301], [778, 316]], when: (g) => !!g.flag("home.studyOpen") },   // the study door standing open, laid over the shut one
    { id: "ladder", src: art + "ladder.png", base: [[586, 307], [688, 328]], solid: [[668, 306], [705, 313], [691, 329], [651, 321]] },   // the attic ladder, let down from its hatch
    { id: "rail", src: art + "rail.png", plane: "front" },   // the railing, the banister of the stairs, the quilt hung over the rail, the hanging light out in the room
  ],

  // LIGHT, drawn live: the lamp of the Son's toy alarm.
  live() {
    return `<g class="tw" fill="#ff4a3d" shape-rendering="geometricPrecision"><circle cx="${ALARM[0]}" cy="${ALARM[1]}" r="4" opacity="0.3"/><circle cx="${ALARM[0]}" cy="${ALARM[1]}" r="1.5"/></g>`;
  },

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "window", name: "stair window", poly: [[138, 323], [238, 297], [238, 128], [138, 127]], walkTo: [353, 261], face: "W", look: each("home.landing.window") },
    { id: "rail", name: "the living room below", verb: "Look down at", poly: [[190, 430], [318, 292], [384, 296], [800, 380], [800, 600], [60, 600]], walkTo: [546, 310], face: "S", look: each("home.rail") },
    {
      id: "stairs", name: "the stairs", verb: "Go down", poly: [[271, 256], [312, 266], [300, 292], [52, 588], [20, 600], [0, 600], [0, 520], [186, 348]], walkTo: [335, 264], face: "W",
      look: each("home.landing.stairs"), use: (g) => g.goto("home-living-room", { spawn: "fromLanding" }),
    },
    {
      id: "son", name: "the Son's door", verb: "Knock on", poly: [[424, 255], [465, 262], [465, 135], [424, 135]], walkTo: [420, 265], face: "N",
      look: each("home.son.look"), use: sonDoor, useWith: { studykey: each("home.son.key") },
    },
    { id: "bag", name: "the Son's school bag", rect: [390, 186, 30, 72], walkTo: [373, 261], face: "N", look: each("home.bag") },
    { id: "photos", name: "photographs", rect: [475, 151, 54, 51], walkTo: [476, 277], face: "N", look: each("home.landing.photos") },
    { id: "hamper", name: "laundry hamper", rect: [461, 217, 44, 58], walkTo: [467, 274], face: "N", look: each("home.hamper") },
    {
      id: "lilsis", name: "Little Sister's room", verb: "Go into", poly: [[537, 274], [594, 284], [594, 135], [537, 135]], walkTo: [544, 288], face: "N",
      look: each("home.lildoor"), use: (g) => g.goto("home-lilsis-room", { spawn: "fromLanding" }),
    },
    {
      id: "halltable", name: "the hall table", verb: "Search", poly: [[604, 232], [608, 184], [636, 184], [640, 226], [680, 232], [680, 306], [600, 306], [600, 232]], walkTo: [626, 303], face: "N",
      look: each("home.halltable"), use: each("home.halltable.use"),
    },
    { id: "chart", name: "the countdown to the trip", poly: [[638, 166], [681, 166], [681, 200], [638, 200], [636, 182], [605, 182], [605, 166]], walkTo: [626, 303], face: "N", look: each("home.countdown") },
    {
      id: "study", name: "study door", verb: "Open", poly: [[695, 301], [778, 316], [778, 135], [695, 135]], walkTo: [723, 322], face: "N",
      look: studyLook, use: studyDoor, useWith: { studykey: studyDoor },
    },
    { id: "sign", name: "Dad's notice", verb: "Read", poly: [[698, 217], [774, 224], [774, 167], [698, 165]], walkTo: [723, 322], face: "N", look: readSign, use: readSign },
    {
      id: "ladder", name: "the attic ladder", verb: "Climb", poly: [[577, 79], [579, 76], [586, 76], [603, 79], [701, 314], [688, 328], [680, 326], [601, 138]], walkTo: [718, 325], face: "W",
      look: each("home.ladder"), use: (g) => g.goto("home-bigsis-room", { spawn: "fromLadder" }),
    },
  ],

  given,

  // What they say to each other up here. What has not been heard comes first.
  talk: {
    mom: {
      bigsis: [
        { when: (g) => !g.flag("home.keyInPiano"), say: ["home.talk.landing.mom.bigsis.sign.a", "home.talk.landing.mom.bigsis.sign.b"] },
        ["home.talk.landing.mom.bigsis.1a", "home.talk.landing.mom.bigsis.1b", "home.talk.landing.mom.bigsis.1c"],
        ["home.talk.landing.mom.bigsis.2a", "home.talk.landing.mom.bigsis.2b"],
      ],
      lilsis: [["home.talk.landing.mom.lilsis.1a", "home.talk.landing.mom.lilsis.1b"], ["home.talk.landing.mom.lilsis.2a", "home.talk.landing.mom.lilsis.2b", "home.talk.landing.mom.lilsis.2c"]],
    },
    bigsis: {
      mom: [["home.talk.landing.bigsis.mom.1a", "home.talk.landing.bigsis.mom.1b"], ["home.talk.landing.bigsis.mom.2a", "home.talk.landing.bigsis.mom.2b"]],
      lilsis: [["home.talk.landing.bigsis.lilsis.1a", "home.talk.landing.bigsis.lilsis.1b"], ["home.talk.landing.bigsis.lilsis.2a", "home.talk.landing.bigsis.lilsis.2b"]],
    },
    lilsis: {
      mom: [["home.talk.landing.lilsis.mom.1a", "home.talk.landing.lilsis.mom.1b"], ["home.talk.landing.lilsis.mom.2a", "home.talk.landing.lilsis.mom.2b"]],
      bigsis: [["home.talk.landing.lilsis.bigsis.1a", "home.talk.landing.lilsis.bigsis.1b"], ["home.talk.landing.lilsis.bigsis.2a", "home.talk.landing.lilsis.bigsis.2b", "home.talk.landing.lilsis.bigsis.2c"]],
    },
  },

  // The first time up: somebody says what is at the end of the landing.
  async enter(g) {
    if (g.flag("home.sawLanding") || !home(g) || !g.flag("home.arrived")) return;
    g.flag("home.sawLanding", true);
    if (g.flag("home.studyOpen")) return;
    await g.wait(300);
    await g.say("home.landing.first.1", "home.landing.first.2");
  },
};

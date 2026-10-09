// Act Three, the second of its five scenes: the landing upstairs, seen from out over the living room.
// Three doors: the Son's (NO GIRLS ALLOWED, and booby-trapped), Little Sister's (BEWARE OF CHICKENS) and Dad's study
// (locked, with a notice taped to it); and the attic ladder, let down from its hatch, with a card on it: THE RETREAT.
// That is Big Sister's.
//
// What happens here:
//   chain A   Dad's notice is a riddle: "Lost your key? It is with the other eighty-eight." Big Sister or Mom
//             works it out (a piano has eighty-eight keys); Little Sister cannot. Once Little Sister has fetched
//             the key out of the piano downstairs, whoever is holding it opens the study.
//   the Son's door   NO GIRLS ALLOWED. His spy-kit alarm still asks for the password, and Little Sister still knows
//             it; but when either sister opens the door, his toy blaster in the gap over it fires a volley of foam
//             darts onto the runner (drawn live; they stay where they fall), and Big Sister declines to go in. The
//             second time, the one dart he kept back. After that, nobody tries. Mom does not try his door tonight.
// The three of them go through the house together (`party`): see home-living-room.js.
// The ways out across the edges of the picture (`edges`): down the stairs at the left and along the bottom, up the
// ladder at the top, and into the study at the right once it is open.
//
// Every place below is measured from the painting (art/scenes/home-landing/layout.json is the painter's own list).
// The ladder stands just in front of the study door's left edge: people pass in front of its feet, not behind them.
//
// Try it: index.html?scene=home-landing&lead=bigsis&flags=home.arrived
// Later states: &flags=home.arrived,home.keyInPiano,home.hasKey,home.studyOpen,home.sonTrap,home.sonDart

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

// ---------- the Son's door: NO GIRLS ALLOWED. The one place in the act that is allowed to be sad, and it is booby-trapped ----------
// His toy blaster is hidden in the gap over his door. When a sister opens the door it fires a volley of foam darts:
// drawn live, each flies out of the slot over the door in an arc and comes down on the runner in front of it, and there
// they stay. (In this picture "out from the wall" runs down and to the left: the painter's strip of runner, where they
// land, lies below and left of the door, in front of the feet of a sister standing at it.)
// The painter's marks (layout.json, things.son.trap): `from` [444, 134], the slot `gap` [425..464, 134], and `land`
// [[393, 262], [442, 271], [420, 278], [370, 268]]. The live layer is behind the people and the railing: a dart passes
// behind whoever stands at the door, and lies on the runner between the balusters.
const TRAP = [444, 134];                         // the middle of the slot over his door
const FOAM = "#ff8a1f", TIP = "#2f6be0";         // his darts: orange foam with a blue tip, and the other way about
// The volley: where along the slot each dart comes out (x), where it comes down on the runner [x, y], the way it lies
// there (degrees; 0 points right), its foam and its tip, and how high it rises on the way out. Each comes down in a gap
// between two balusters, lying more or less along it, so that it can be seen there.
const VOLLEY = [
  [430, 382, 268, 105, FOAM, TIP, 30], [452, 425, 272, 290, TIP, FOAM, 24], [436, 403, 270, 115, FOAM, TIP, 36],
  [460, 432, 271, 250, TIP, FOAM, 20], [426, 410, 272, 95, TIP, FOAM, 26], [448, 417, 274, 125, FOAM, TIP, 32],
  [464, 440, 271, 70, FOAM, TIP, 16],
];
const LAST = [444, 421, 270, 100, TIP, FOAM, 4]; // the one he kept back: it flops out, the second time, and lands at her feet
const ASIDE = [[540, 292], [588, 303]];          // where the other two stand clear of the darts (to the right, toward her door)
const RUNNER = [410, 272];                       // the middle of where they come down: everybody looks there afterwards

/** One dart, as the live layer draws it: at [x, y], turned r degrees. In the air it trails a streak of speed. */
const dartAt = (x, y, r) => `translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${r.toFixed(1)})`;
const dart = (n, [x0, x, y, r, foam, tip], down) =>
  `<g id="dart-${n}" transform="${down ? dartAt(x, y, r) : dartAt(x0, TRAP[1], 90)}" opacity="${down ? 1 : 0}">` +
  `<path class="streak" d="M-7 0 H-16" stroke="#fff" stroke-opacity="0.45" stroke-width="1.6" stroke-linecap="round" opacity="0"/>` +
  `<rect x="-6.4" y="-1.6" width="10.4" height="3.2" rx="1.5" fill="${foam}" stroke="#2a1406" stroke-width="0.7"/>` +
  `<circle cx="4.2" cy="0" r="2.2" fill="${tip}" stroke="#2a1406" stroke-width="0.7"/></g>`;

/** Darts out of the slot over the door, one after another, each in an arc down to its place; there they stay. */
async function fire(g, darts, first, ms = 640, gap = 90) {
  const box = g.q("#son-darts");
  if (box) box.setAttribute("data-flying", "1");          // (while any dart is in the air: a test waits for this)
  await Promise.all(darts.map((d, i) => g.wait(i * gap).then(() => fly(g, first + i, d, ms))));
  if (box) box.removeAttribute("data-flying");
}
function fly(g, n, [x0, x1, y1, rest, , , lift], ms) {
  const el = g.q(`#dart-${n}`), streak = el && el.querySelector(".streak"), y0 = TRAP[1], land = 0.8;
  if (!el) return Promise.resolve();
  g.sfx("thwip");
  el.setAttribute("opacity", 1);
  if (streak) streak.setAttribute("opacity", 1);
  return g.tween(ms, (k) => {
    const f = Math.min(k / land, 1), b = k > land ? (k - land) / (1 - land) : 0;      // in the air; then one small bounce
    const x = x0 + (x1 - x0) * f, y = y0 + (y1 - y0) * f - 4 * lift * f * (1 - f) - 2.5 * Math.sin(Math.PI * b);
    const air = (Math.atan2(y1 - y0 - 4 * lift * (1 - 2 * f), x1 - x0) * 180) / Math.PI;   // nose first, along the arc
    const s = Math.max(0, Math.min(1, (f - 0.72) / 0.28)), turn = ((rest - air + 540) % 360) - 180;
    el.setAttribute("transform", dartAt(x, y, air + turn * s * s * (3 - 2 * s)));
    if (streak && f >= 1) streak.setAttribute("opacity", 0);
  }, g.ease.linear);
}

/** The other two stand clear of where the darts come down, and turn to the door. */
async function standClear(g) {
  const me = g.lead, others = THREE.map((id) => g.actor(id)).filter((a) => a && a !== me);
  const near = others.filter((a) => a.x > 350 && a.x < 520);         // (the darts come down between the newel post and her door)
  const taken = (m) => others.some((a) => !near.includes(a) && Math.abs(a.x - m[0]) < 38 && Math.abs(a.y - m[1]) < 15);
  const free = ASIDE.filter((m) => !taken(m));
  await Promise.all(near.map((a, n) => (free[n] ? g.walkTo(free[n][0], free[n][1], a.id) : null)));
  for (const a of others) a.look(TRAP[0], TRAP[1] + 90);
}

async function sonDoor(g) {
  const me = who(g);
  if (me === "mom") return g.say("home.son.use.mom");                          // Mom does not try his door tonight
  if (g.flag("home.sonDart")) return g.say(me === "lilsis" ? "home.son.again" : "home.son.again.bigsis");
  if (g.flag("home.sonTrap")) {                                               // the second time: the one he kept back
    await g.reach();
    g.sfx("latch");
    await g.wait(300);
    await fire(g, [LAST], VOLLEY.length, 900);
    g.flag("home.sonDart", true);
    g.lead.look(LAST[1], LAST[2]);
    return g.say(`home.son.dart.${me}`);
  }
  await standClear(g);
  await g.reach();
  g.sfx("alarm");
  await g.wait(600);
  await g.say("home.son.alarm.1");                                            // his own voice, on the toy's little speaker
  if (me === "lilsis") {                                                      // she knows the password, and does his voice
    await g.say("home.son.alarm.2");
    g.sfx("found");
    await g.wait(350);
    await g.say("home.son.alarm.3");
  } else await g.say("home.son.use.bigsis");                                  // she declines to guess, and simply opens it
  g.sfx("latch");                                                             // the door opens an inch...
  await g.wait(250);
  g.lead.look(TRAP[0], TRAP[1]);
  await fire(g, VOLLEY, 0);                                                   // ...and the blaster in the gap over it goes off
  g.flag("home.sonTrap", true);
  await g.wait(250);
  for (const id of THREE) { const a = g.actor(id); if (a) a.look(RUNNER[0], RUNNER[1]); }
  const big = g.actor("bigsis"), mom = g.actor("mom"), lil = g.actor("lilsis");
  if (big) await g.say("home.son.trap.bigsis");                               // the author's line, word for word
  if (me === "lilsis") await g.say("home.son.trap.lilsis");                   // the password was CORRECT
  else if (lil) await g.say("home.son.trap.lilsis.2");                        // her sister got got
  if (mom) {
    mom.look(g.lead.x, g.lead.y);
    await g.wait(300);
    await g.say(me === "lilsis" ? "home.son.alarm.4" : "home.son.trap.mom");  // Mom, quietly: not tonight
  }
  if (me === "lilsis") await g.say("home.son.alarm.5");
  g.sfx("latch");                                                             // and it is pulled shut again
}
const sonLook = (g) => g.say(`home.son.${g.flag("home.sonTrap") ? "after" : "look"}.${who(g)}`);

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

// The little lamp on the Son's toy alarm, under the alarm box's window (painted dark, for the game to light). Light, so it is drawn live.
const ALARM = [458, 191];

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
  // (The one who comes up the stairs stands a little to the right of the painter's [431, 279]: a grown-up there hides the
  // middle of the Son's sign, and the runner in front of his door is where his darts come down.)
  spawn: {
    default: [471, 284], mom: [471, 284], bigsis: [375, 263], lilsis: [337, 262],
    fromStairs: [471, 284], fromLilsis: [590, 308], fromStudy: [721, 324],
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

  // The ways out across the edges of the picture. The study door at the right end leads on only once it is open.
  edges: {
    W: { to: "home-living-room", spawn: "fromLanding", name: "down the stairs", walkTo: [335, 264] },
    S: { to: "home-living-room", spawn: "fromLanding", name: "down the stairs", walkTo: [335, 264] },
    N: { to: "home-bigsis-room", spawn: "fromLadder", name: "up the ladder to the Retreat", walkTo: [718, 325] },
    E: { to: "home-study", spawn: "fromLanding", name: "into Dad's study", walkTo: [723, 322], when: (g) => !!g.flag("home.studyOpen") },
  },

  // LIGHT, drawn live: the lamp of the Son's toy alarm; and his foam darts, which lie on the runner once they have
  // been fired (`sonDoor`, above, fires them; until then they wait, unseen, in the gap over his door).
  live(art, g) {
    const fired = !!(g && g.flag("home.sonTrap")), last = !!(g && g.flag("home.sonDart"));
    const darts = VOLLEY.map((d, n) => dart(n, d, fired)).join("") + dart(VOLLEY.length, LAST, last);
    return `<g class="tw" fill="#ff4a3d" shape-rendering="geometricPrecision"><circle cx="${ALARM[0]}" cy="${ALARM[1]}" r="4" opacity="0.3"/><circle cx="${ALARM[0]}" cy="${ALARM[1]}" r="1.5"/></g>
      <g id="son-darts" shape-rendering="geometricPrecision">${darts}</g>`;
  },

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "window", name: "stair window", poly: [[123, 115], [249, 115], [249, 279], [220, 312], [123, 318]], walkTo: [353, 261], face: "W", look: each("home.landing.window") },
    {
      // (the living room below, seen over the railing: the piano, its lamp and its stool are what stand out down there.
      // The railing itself is in front of everybody's knees, and the floor below is the way down: neither is an area.)
      id: "rail", name: "the living room below", verb: "Look down at", walkTo: [546, 310], face: "S", look: each("home.rail"),
      poly: [[588, 398], [608, 394], [636, 398], [683, 410], [686, 400], [707, 400], [712, 420], [728, 440], [728, 470], [722, 520], [716, 580], [700, 598],
        [600, 598], [588, 560]],
    },
    {
      id: "stairs", name: "the stairs", verb: "Go down", poly: [[271, 256], [312, 266], [300, 292], [52, 588], [20, 600], [0, 600], [0, 520], [186, 348]], walkTo: [335, 264], face: "W",
      look: each("home.landing.stairs"), use: (g) => g.goto("home-living-room", { spawn: "fromLanding" }),
    },
    {
      id: "son", name: "the Son's door", verb: "Knock on", poly: [[424, 255], [465, 262], [465, 135], [424, 135]], walkTo: [420, 265], face: "N",
      look: sonLook, use: sonDoor, useWith: { studykey: each("home.son.key") },
    },
    { id: "bag", name: "the Son's school bag", rect: [390, 186, 30, 72], walkTo: [373, 261], face: "N", look: each("home.bag") },
    { id: "photos", name: "photographs", rect: [475, 151, 54, 51], walkTo: [476, 277], face: "N", look: each("home.landing.photos") },
    { id: "hamper", name: "laundry hamper", poly: [[461, 217], [505, 217], [505, 276], [461, 268]], walkTo: [467, 274], face: "N", look: each("home.hamper") },   // (its foot is the foot of the wall)
    {
      id: "lilsis", name: "Little Sister's room", verb: "Go into", poly: [[537, 274], [594, 284], [594, 135], [537, 135]], walkTo: [544, 288], face: "N",
      look: each("home.lildoor"), use: (g) => g.goto("home-lilsis-room", { spawn: "fromLanding" }),
    },
    {
      id: "halltable", name: "the hall table", verb: "Search", poly: [[604, 232], [608, 184], [636, 184], [640, 226], [680, 232], [680, 309], [600, 294], [600, 232]], walkTo: [626, 303], face: "N",
      look: each("home.halltable"), use: each("home.halltable.use"),
    },
    { id: "chart", name: "the countdown to the trip", poly: [[638, 166], [681, 166], [681, 200], [638, 200], [636, 182], [605, 182], [605, 166]], walkTo: [626, 303], face: "N", look: each("home.countdown") },
    {
      id: "study", name: "study door", verb: "Open", poly: [[695, 301], [778, 316], [778, 135], [695, 135]], walkTo: [723, 322], face: "N",
      look: studyLook, use: studyDoor, useWith: { studykey: studyDoor },
    },
    { id: "sign", name: "Dad's notice", verb: "Read", poly: [[698, 217], [774, 224], [774, 167], [698, 165]], walkTo: [723, 322], face: "N", look: readSign, use: readSign },
    {
      id: "ladder", name: "the attic ladder", verb: "Climb", plane: "ladder", poly: [[577, 79], [579, 76], [586, 76], [603, 79], [701, 314], [688, 328], [680, 326], [601, 138]], walkTo: [718, 325], face: "W",
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

  // The first time up: somebody says what is at the end of the landing; and Little Sister has seen her brother's sign.
  async enter(g) {
    if (g.flag("home.sawLanding") || !home(g) || !g.flag("home.arrived")) return;
    g.flag("home.sawLanding", true);
    if (g.flag("home.studyOpen")) return;
    await g.wait(300);
    await g.say("home.landing.first.1", "home.landing.first.2", "home.landing.first.3");
  },
};

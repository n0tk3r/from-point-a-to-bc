// Act Three, the third of its five scenes: Dad's study under the roof, "Trip Headquarters".
// He and the Son planned the road trip up here. Three of the act's chains end in this room, and each needs the right one of them:
//   chain C   the family computer ("the mainframe"). Dad's note on the monitor: only Big Sister can read what it
//             means (1928). Signing in needs the internet (the router, downstairs) and that year; then it asks what
//             was promised on the wedding day, and only Mom was there. The map: one dot.
//   chain D   the answering machine has spilled its tape. Mom winds it back in with Dad's pencil (from his crossword,
//             downstairs); then any of them presses play: Dad's last message.
//   chain E   the family vault: "the year WE THE PEOPLE got it in writing". Mom's: 1787. Inside, the spare car key.
// The three of them go through the house together (`party`): see home-living-room.js.
//
// Every place below is measured from the finished painting (art/scenes/home-study/layout.json is the painter's own list).
//
// Try it: index.html?scene=home-study&lead=mom&flags=home.arrived,home.keyInPiano,home.hasKey,home.studyOpen
// Later states: add home.online,home.noteTaken,home.knowsYear,home.typed,home.foundPing,home.tapeWound,home.heardMessage,home.hasCarKey
// (they will have no pencil: for that, play it from the living room.)

const art = "art/scenes/home-study/";

const THREE = ["mom", "bigsis", "lilsis"];
const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
const who = (g) => g.store.data.active;
/** Are the three of them on stage? (A test, or a visitor from another act, can walk somebody else in.) */
const home = (g) => THREE.every((id) => g.actor(id));

// ---------- the light ----------
// Drawn live: the answering machine's little red light, which blinks until its message has been heard,
// and the glow the monitor throws, which takes the color of whatever is on the screen.
const BLINK = [193, 317];                        // the machine's light
const SCREEN = [352, 284];                       // the middle of the monitor's screen
const GLOW = { offline: "#7f8ea3", login: "#5aa0e6", map: "#f2e3b0" };
function light(g) {
  const led = g.q("#machine-led"), glow = g.q("#pc-glow");
  if (led) { const heard = !!g.flag("home.heardMessage"); led.classList.toggle("tw", !heard); led.setAttribute("opacity", heard ? 0.35 : 1); }
  if (glow) glow.setAttribute("fill", GLOW[g.flag("home.foundPing") ? "map" : g.flag("home.online") ? "login" : "offline"]);
}

/** The other two come and stand where they can see, and turn to it. */
async function gather(g, marks, at) {
  const me = g.lead, others = THREE.map((id) => g.actor(id)).filter((a) => a && a !== me);
  await Promise.all(others.map((a, n) => g.walkTo(marks[n][0], marks[n][1], a.id).then(() => a.look(at[0], at[1]))));
}

// ---------- chain C: the note. Whoever holds it, only Big Sister can read what it means ----------
async function solveNote(g) {
  await g.say("home.note.solve.1", "home.note.solve.2", "home.note.solve.3");
  g.flag("home.knowsYear", true);
}
async function takeNote(g) {
  await g.reach();
  g.flag("home.noteTaken", true);                // (the note comes off the monitor by itself: its cut-out follows this fact)
  g.give("note");
  if (who(g) === "bigsis") await solveNote(g);
  else await g.say(`home.note.take.${who(g)}`);
}

// ---------- chain C: the computer ----------
async function useComputer(g) {
  const me = who(g), show = (screen) => g.closeup(g.art.monitor(screen), "The family computer"), screens = g.art.screens;
  if (g.flag("home.foundPing")) { show(screens.map()); return g.say(`home.pc.done.${me}`); }
  if (!g.flag("home.online")) {
    show(screens.offline());
    return g.say(...(me === "bigsis" ? ["home.pc.offline.bigsis", "home.pc.offline.bigsis2"] : [`home.pc.offline.${me}`]));
  }
  if (!g.flag("home.knowsYear")) {
    show(screens.login(0));
    if (me === "lilsis") {                       // she has a go anyway
      for (let n = 1; n <= 4; n++) { show(screens.login(n)); g.sfx("key"); await g.wait(240); }
      g.sfx("wrong"); show(screens.login(4, true)); await g.wait(450); show(screens.login(0));
    }
    return g.say(`home.pc.login.${me}`);
  }
  if (!g.flag("home.typed")) {                   // the password goes in once, and stays in
    show(screens.login(0));
    await g.say(`home.pc.type.${me}`);
    for (let n = 1; n <= 4; n++) { show(screens.login(n)); g.sfx("key"); await g.wait(260); }
    await g.wait(350);
    g.flag("home.typed", true);
  }
  show(screens.question());
  await g.say(`home.pc.question.${me}`);
  if (me !== "mom") return;                      // only one person in this house was at the wedding
  for (;;) {
    const pick = await g.choose([
      { id: "love", line: "home.pc.pick.love" },
      { id: "scenic", line: "home.pc.pick.scenic" },
      { id: "directions", line: "home.pc.pick.directions" },
    ]);
    await g.say(`home.pc.pick.${pick}`);
    if (pick === "directions") break;
    g.sfx("wrong");
    await g.say(`home.pc.wrong.${pick}`);
  }
  g.sfx("found");
  show(screens.map());
  g.flag("home.foundPing", true);                // (and the screen on the desk shows the map from now on)
  light(g);
  await g.say("home.pc.right", "home.pc.map.1", "home.pc.map.2");
  if (g.flag("home.heardMessage")) await g.say("home.pc.map.six");      // the tape said 5:41. The dot says 5:47.
  await g.say("home.pc.map.3", "home.pc.map.4");
}

// ---------- chain D: the answering machine ----------
const LISTEN = [[300, 416], [268, 442]];         // where the other two stand to hear the message

async function windTape(g) {
  await g.say("home.tape.wind.1");
  await g.reach();
  g.sfx("wind");
  await g.wait(1500);
  g.flag("home.tapeWound", true);                // (the loop of tape is gone from the picture: its cut-out follows this fact)
  await g.say("home.tape.wind.2", "home.tape.wind.3", "home.tape.wind.4");
}

async function playMessage(g) {
  await gather(g, LISTEN, [182, 312]);
  await g.reach();
  g.sfx("machine");
  await g.wait(900);
  await g.say("home.msg.1", "home.msg.2", "home.msg.3", "home.msg.4");
  g.sfx("hiss");
  await g.wait(1300);
  g.flag("home.heardMessage", true);
  light(g);
  await g.say("home.msg.after.lilsis", g.flag("home.foundPing") ? "home.msg.after.bigsis.six" : "home.msg.after.bigsis", "home.msg.after.mom");
}

async function useMachine(g) {
  const me = who(g);
  if (g.flag("home.heardMessage")) return g.say(`home.msg.again.${me}`);
  if (g.flag("home.tapeWound")) return playMessage(g);
  const holder = g.holder("pencil");
  if (holder === me) return me === "mom" ? windTape(g) : g.say(`home.tape.notme.${me}`);   // Mom is the one with the knack
  await g.say(`home.tape.need.${me}`);
  if (holder) return g.say(`home.tape.has.${holder}`);                  // one of the others is holding it: say so
  if (!g.flag("home.pencilTaken")) await g.say("home.tape.where");      // the one pencil anybody can find is downstairs
}
const shineAtMachine = (g) => g.say(g.flag("home.flashWorks") ? "home.machine.flash" : "home.flash.dead");
const machineLook = (g) => g.say(g.flag("home.heardMessage") ? `home.msg.again.${who(g)}` : g.flag("home.tapeWound") ? `home.machine.ready.${who(g)}` : `home.machine.look.${who(g)}`);

// ---------- chain E: the family vault ----------
// The label, as the close-up shows it (the kit draws the piece of paper: js/art/kit.js, `paper`).
const LABEL = {
  tape: false, tilt: 1, width: 500, tint: "#f7f1d8",
  lines: [
    { text: "FAMILY VAULT", size: 46, gap: 30 },
    { text: "Combination: the year", size: 27 },
    { text: "WE THE PEOPLE", size: 36 },
    { text: "got it in writing.", size: 27, gap: 36 },
    { text: "Your mother will know. She brings it up.", size: 21 },
  ],
};
const WATCH = [[612, 438], [586, 466]];          // where the other two stand while Mom turns the dial

async function useVault(g) {
  const me = who(g);
  if (g.flag("home.hasCarKey")) return g.say(`home.vault.done.${me}`);
  g.closeup(g.art.paper(LABEL), "The label on the family vault", { grid: [800, 600] });
  await g.say(`home.vault.read.${me}`);
  if (me !== "mom") return;                      // the girls leave it to her: "Your mother will know."
  for (;;) {
    const pick = await g.choose([
      { id: "1776", line: "home.vault.pick.1776" },
      { id: "1787", line: "home.vault.pick.1787" },
      { id: "1789", line: "home.vault.pick.1789" },
      { id: "later", line: "home.vault.pick.later" },
    ]);
    await g.say(`home.vault.pick.${pick}`);
    if (pick === "later") return;
    g.sfx("dial");
    await g.wait(700);
    if (pick === "1787") break;
    g.sfx("wrong");
    await g.say(`home.vault.wrong.${pick}`);     // a wrong year costs a line, and the line is true
  }
  g.closeup();
  g.sfx("clunk");
  await g.wait(400);
  await gather(g, WATCH, [744, 362]);
  await g.say("home.vault.right.1");
  await g.reach();
  g.flag("home.hasCarKey", true);                // (the box stands open from now on: its cut-out follows this fact)
  g.give("carkey");
  await g.say("home.vault.right.2", "home.vault.right.3", "home.vault.right.4", "home.vault.right.5");
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

export default {
  id: "home-study",
  era: "home",
  name: "Dad's study: Trip Headquarters",

  // DEPTH, from the room's camera (layout.json).
  horizon: 120, full: 440,

  // The floor between the desk (far wall), the filing cabinet (left), the shelves (right) and the heap of trip things
  // (front), with a notch for the desk chair. The desk's own ground is blocked by its cut-out (`solid`, below).
  walk: { area: [[247, 374], [322, 376], [314, 389], [374, 391], [380, 376], [624, 382], [653, 391], [718, 497], [226, 473], [205, 418]] },

  party: ["mom", "bigsis", "lilsis"],
  spawn: { default: [298, 448], mom: [298, 448], bigsis: [251, 432], lilsis: [360, 457], fromLanding: [298, 448] },
  arrive: { fromLanding: [[251, 432], [360, 457]] },
  exits: ["home-landing"],
  // The way out across the edges of the picture: the door to the landing stands open at the front left, so the left
  // edge and the bottom both lead out to the landing.
  edges: {
    W: { to: "home-landing", spawn: "fromStudy", name: "out to the landing", walkTo: [252, 466] },
    S: { to: "home-landing", spawn: "fromStudy", name: "out to the landing", walkTo: [252, 466] },
  },

  picture: art + "back.png",

  // CUT-OUTS. The desk stands on the floor (nobody can get behind it); what the story changes is laid over the backdrop.
  planes: [
    { id: "desk", src: art + "desk.png", base: [[258, 367], [420, 372]], solid: [[276, 348], [425, 352], [417, 387], [246, 381]] },   // desk, chair, lamp and computer, the screen dark
    // what the monitor is showing: just the lit glass, laid over the dark monitor
    {
      id: "screen", base: [[258, 368], [420, 373]], state: (g) => (g.flag("home.foundPing") ? "map" : g.flag("home.online") ? "login" : "offline"),
      states: { offline: art + "screen-offline.png", login: art + "screen-login.png", map: art + "screen-map.png" },
    },
    { id: "note", src: art + "note.png", base: [[258, 368], [420, 373]], when: (g) => !g.flag("home.noteTaken") },   // Dad's note, until somebody takes it
    { id: "tape", src: art + "tape-out.png", base: [[152, 406], [196, 408]], when: (g) => !g.flag("home.tapeWound") },   // the loop of tape spilled out of the machine, until it is wound back in
    { id: "vault-open", src: art + "vault-open.png", base: [[668, 392], [727, 479]], when: (g) => !!g.flag("home.hasCarKey") },   // the cash box with its lid up, over the shut one
    { id: "front", src: art + "front.png", plane: "front" },   // the door's wall, frame and open leaf at the left; the heap of trip things at the bottom
  ],

  // LIGHT, drawn live. `light` (above) makes both match the story.
  live() {
    return `<defs><radialGradient id="pc-halo"><stop offset="0" stop-color="#fff" stop-opacity="0.55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
        <mask id="pc-mask"><ellipse cx="${SCREEN[0]}" cy="${SCREEN[1]}" rx="38" ry="30" fill="url(#pc-halo)"/></mask></defs>
      <rect id="pc-glow" x="${SCREEN[0] - 38}" y="${SCREEN[1] - 30}" width="76" height="60" fill="${GLOW.offline}" mask="url(#pc-mask)" opacity="0.5"/>
      <g id="machine-led" class="tw" fill="#ff4a3d" shape-rendering="geometricPrecision"><circle cx="${BLINK[0]}" cy="${BLINK[1]}" r="5" opacity="0.3"/><circle cx="${BLINK[0]}" cy="${BLINK[1]}" r="1.8"/></g>`;
  },

  setup: light,

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "window", name: "window", rect: [399, 172, 89, 100], walkTo: [456, 381], face: "N", look: each("home.study.window") },
    { id: "banner", name: "banner", poly: [[270, 134], [535, 143], [535, 177], [270, 171]], walkTo: [431, 427], face: "N", look: each("home.banner") },
    { id: "corkboard", name: "corkboard", rect: [286, 213, 68, 54], walkTo: [274, 379], face: "N", look: each("home.corkboard") },
    { id: "wallmap", name: "wall map", rect: [488, 226, 124, 98], walkTo: [558, 383], face: "N", look: each("home.wallmap"), useWith: { pencil: each("home.wallmap.pencil") } },
    {
      id: "aeroplane", name: "model biplane", walkTo: [558, 383], face: "N", look: each("home.plane"),
      poly: [[508, 170], [532, 166], [550, 196], [591, 196], [591, 224], [564, 222], [564, 240], [546, 247], [518, 232], [508, 196]],
    },
    {
      id: "globe", name: "globe", verb: "Spin", walkTo: [602, 384], face: "E", look: each("home.globe"), use: each("home.globe.use"),
      poly: [[621, 296], [630, 289], [645, 289], [653, 298], [653, 314], [644, 322], [641, 364], [652, 368], [652, 376], [624, 376], [624, 368], [633, 364], [630, 322], [621, 314]],
    },
    {
      id: "shelves", name: "shelves", walkTo: [651, 420], face: "E", look: each("home.shelves"),
      poly: [[667, 322], [684, 318], [686, 296], [708, 293], [712, 318], [745, 340], [778, 345], [784, 384], [784, 481], [727, 481], [672, 394]],
    },
    {
      id: "vault", name: "family vault", verb: "Open", rect: [712, 344, 65, 38], walkTo: [666, 460], face: "E",
      look: useVault, use: useVault, useWith: { studykey: each("home.vault.key"), carkey: each("home.vault.done") },
    },
    {
      id: "computer", name: "computer", verb: "Use", walkTo: [342, 393], face: "N", look: each("home.pc.look"), use: useComputer,
      poly: [[331, 262], [380, 262], [380, 298], [384, 306], [376, 313], [328, 313], [325, 305], [331, 298]],   // (the monitor and its keyboard)
      useWith: { note: useComputer, pencil: { lilsis: "home.pc.pencil.lilsis" } },
    },
    {
      // (She stands ten pixels nearer than the painter's [394, 382], which is under the desk's own ground: the engine stood her
      // here anyway, and from here there is room on either side for the others, so that nobody stands in anybody.)
      id: "note", name: "sticky note", verb: "Take", rect: [357, 263, 22, 21], walkTo: [391, 392], face: "W", when: (g) => !g.flag("home.noteTaken"),
      look: { mom: "home.note.look.mom", lilsis: "home.note.look.lilsis", bigsis: takeNote }, use: takeNote,
    },
    {
      id: "machine", name: "answering machine", verb: "Use", poly: [[158, 294], [208, 294], [208, 326], [194, 326], [194, 360], [160, 360]], walkTo: [243, 401], face: "W",
      look: machineLook, use: useMachine, useWith: { pencil: useMachine, lilflash: { lilsis: shineAtMachine } },
    },
    {
      id: "heap", name: "things that did not fit in the car", walkTo: [402, 477], face: "S", look: each("home.boxes"), plane: "front",
      poly: [[262, 530], [296, 522], [304, 500], [352, 498], [362, 466], [477, 466], [480, 505], [492, 500], [565, 458], [602, 462], [604, 512], [630, 512], [636, 524], [710, 524], [710, 558], [640, 600], [262, 600]],
    },
    {
      id: "door", name: "the door to the landing", verb: "Go through", poly: [[0, 300], [153, 314], [153, 600], [0, 600]], walkTo: [252, 466], face: "W", plane: "front",
      look: each("home.study.door"), use: (g) => g.goto("home-landing", { spawn: "fromStudy" }),
    },
  ],

  given,

  // What they say to each other in here. What has not been heard comes first.
  talk: {
    mom: {
      bigsis: [
        { when: (g) => g.has("note") && !g.flag("home.knowsYear"), say: ["home.talk.study.mom.bigsis.note.a", "home.talk.study.mom.bigsis.note.b"] },
        ["home.talk.study.mom.bigsis.1a", "home.talk.study.mom.bigsis.1b"],
        ["home.talk.study.mom.bigsis.2a", "home.talk.study.mom.bigsis.2b", "home.talk.study.mom.bigsis.2c"],
      ],
      lilsis: [["home.talk.study.mom.lilsis.1a", "home.talk.study.mom.lilsis.1b"], ["home.talk.study.mom.lilsis.2a", "home.talk.study.mom.lilsis.2b"]],
    },
    bigsis: {
      mom: [
        { when: (g) => !g.flag("home.hasCarKey"), say: ["home.talk.study.bigsis.mom.vault.a", "home.talk.study.bigsis.mom.vault.b"] },
        { when: (g) => !!g.flag("home.foundPing"), say: ["home.talk.study.bigsis.mom.dot.a", "home.talk.study.bigsis.mom.dot.b"] },
        ["home.talk.study.bigsis.mom.1a", "home.talk.study.bigsis.mom.1b"],
        ["home.talk.study.bigsis.mom.2a", "home.talk.study.bigsis.mom.2b"],
      ],
      lilsis: [["home.talk.study.bigsis.lilsis.1a", "home.talk.study.bigsis.lilsis.1b"], ["home.talk.study.bigsis.lilsis.2a", "home.talk.study.bigsis.lilsis.2b"]],
    },
    lilsis: {
      mom: [
        { when: (g) => !g.flag("home.tapeWound"), say: ["home.talk.study.lilsis.mom.tape.a", "home.talk.study.lilsis.mom.tape.b"] },
        ["home.talk.study.lilsis.mom.1a", "home.talk.study.lilsis.mom.1b"],
        ["home.talk.study.lilsis.mom.2a", "home.talk.study.lilsis.mom.2b"],
      ],
      bigsis: [["home.talk.study.lilsis.bigsis.1a", "home.talk.study.lilsis.bigsis.1b"], ["home.talk.study.lilsis.bigsis.2a", "home.talk.study.lilsis.bigsis.2b"]],
    },
  },

  // The first time in: what the room is, and that something in it is blinking.
  async enter(g) {
    if (g.flag("home.sawStudy") || !home(g) || !g.flag("home.arrived")) return;
    g.flag("home.sawStudy", true);
    await g.wait(300);
    await g.say("home.study.first.1", "home.study.first.2", "home.study.first.3");
  },
};

// PLACEHOLDER SCENE: the present, that evening. Mom and the girls find out where Dad's phone was last seen.
//
// It shows a team of three in one room. Each of them can do one thing the others cannot:
//   Little Sister fits into the closet under the stairs        (chain A: the router)
//   Big Sister knows the year behind Dad's password hint        (chain B: the note)
//   Mom knows what her husband promised on their wedding day    (chain C: the question), once A and B are done
// The player switches between them with the portraits, top left. A hotspot can answer
// each of them differently: { mom: ..., bigsis: ..., lilsis: ... }.
//
// Try it: index.html?scene=home-living-room

const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
const who = (g) => g.store.data.active;

/** What the monitor on the desk is showing, and whether Dad's note is still stuck to it. */
const deskState = (g) => (g.flag("home.foundPing") ? "map" : g.flag("home.online") ? "login" : "offline") + (g.flag("home.noteTaken") ? "" : ".note");
function dress(g) {
  const desk = g.actor("desk"), led = g.q("#router-led"), on = !!g.flag("home.online");
  if (desk) desk.options = { ...desk.options, state: deskState(g) };
  if (led) { led.setAttribute("fill", on ? "#4ade80" : "#ff4a3d"); led.classList.toggle("flicker", !on); }
}

// ---------- chain A: the router is in the closet under the stairs, and only one of them fits ----------
async function intoCloset(g) {
  if (g.flag("home.online")) return g.say("home.closet.again");
  const lil = g.lead;
  await g.say("home.closet.go.1");
  await g.moveTo(299, 123);                    // through the gap
  lil.fade(0);
  await g.wait(450);
  await g.say("home.closet.go.2", "home.closet.go.3");
  g.sfx("plug");
  await g.wait(500);
  g.flag("home.online", true);
  dress(g);
  g.sfx("found");
  await g.say("home.closet.go.4");
  lil.fade(1);
  await g.moveTo(284, 130);
  lil.face("S");
  await g.say("home.closet.go.5", "home.closet.go.6");
}

// ---------- chain B: the note. Whoever holds it, only Big Sister can read what it means ----------
async function solveNote(g) {
  await g.say("home.note.solve.1", "home.note.solve.2", "home.note.solve.3");
  g.flag("home.knowsYear", true);
}
async function takeNote(g) {
  await g.reach();
  g.flag("home.noteTaken", true);
  dress(g);
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
    await g.say(...(me === "bigsis" ? ["home.pc.offline.bigsis", "home.pc.offline.bigsis2"] : [`home.pc.offline.${me}`]));
    if (!g.flag("home.knowsRouter")) { await g.say("home.pc.router"); g.flag("home.knowsRouter", true); }
    return;
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
  g.flag("home.foundPing", true);
  dress(g);
  await g.say("home.pc.right", "home.pc.map.1", "home.pc.map.2", "home.pc.map.3", "home.pc.map.4");
}

// ---------- the gate: out of the front door ----------
async function leave(g) {
  if (!g.flag("home.foundPing")) return g.say(`home.door.early.${who(g)}`);
  await g.say("home.leave.1", "home.leave.2", "home.leave.3", "home.leave.4");
  g.flag("home.left", true);
  g.store.data.act = 4;
  await g.fade(1, 700);
  await g.goto("nevada-roadside", { via: "cut" });
}

async function playPiano(g) {
  const me = who(g);
  if (me === "mom") return g.say("home.piano.use.mom");
  await g.reach();
  g.sfx(me === "bigsis" ? "piano" : "plonk");
  await g.wait(me === "bigsis" ? 3300 : 500);
  if (me === "lilsis") return g.say("home.piano.use.lilsis");
  await g.say(g.flag("home.played") ? "home.piano.use.bigsis2" : "home.piano.use.bigsis");
  g.flag("home.played", true);
}

export default {
  id: "home-living-room",
  era: "home",
  name: "The living room, 9:40 p.m.",

  // Indoors the floor is short, so people shrink only a little as they walk to the back wall.
  horizon: -220, full: 192,
  walk: { area: [[6, 125], [314, 125], [314, 196], [6, 196]] },

  // Three leads are here together. They arrive with whoever is leading, each on her own mark.
  party: ["mom", "bigsis", "lilsis"],
  spawn: { default: [150, 162], mom: [134, 160], bigsis: [196, 150], lilsis: [84, 140] },
  exits: ["nevada-roadside"],

  draw(art) { return art.livingRoom(); },

  props: [
    { id: "desk", kind: "desk", at: [143, 127], scale: 0.8, options: { state: "offline.note" }, solid: [[122, 121], [164, 121], [164, 129], [122, 129]] },
    { id: "piano", kind: "piano", at: [238, 127], scale: 0.74, solid: [[214, 121], [262, 121], [262, 131], [214, 131]] },
    { id: "table", kind: "table", at: [70, 188], scale: 0.92, solid: [[26, 178], [114, 178], [116, 190], [24, 190]] },
    { id: "armchair", kind: "armchair", at: [286, 182], scale: 0.9, solid: [[266, 173], [310, 173], [312, 184], [264, 184]] },
  ],

  setup: dress,

  hotspots: [
    {
      id: "door", name: "front door", verb: "Open", rect: [8, 54, 34, 66], walkTo: [26, 129], face: "N", use: leave,
      look: (g) => g.say(`${g.flag("home.foundPing") ? "hint.home.leave" : "home.door.early"}.${who(g)}`),
    },
    { id: "window", name: "window", rect: [62, 46, 52, 48], walkTo: [88, 130], face: "N", look: each("home.window") },
    { id: "books", name: "bookcase", rect: [170, 54, 40, 66], walkTo: [190, 129], face: "N", look: each("home.books") },
    { id: "photo", name: "family photograph", rect: [226, 52, 34, 22], walkTo: [243, 135], face: "N", look: each("home.photo") },
    { id: "stairs", name: "stairs", poly: [[262, 86], [320, 28], [320, 62], [276, 106], [262, 110]], walkTo: [270, 132], face: "NE", look: each("home.stairs") },
    {
      id: "closet", name: "closet under the stairs", verb: "Open", rect: [288, 92, 26, 30], walkTo: [282, 129], face: "NE",
      look: (g) => g.say(g.flag("home.online") && who(g) !== "lilsis" ? `home.closet.done.${who(g)}` : g.flag("home.online") ? "home.closet.again" : `home.closet.look.${who(g)}`),
      use: { lilsis: intoCloset, mom: (g) => g.say(g.flag("home.online") ? "home.closet.done.mom" : "home.closet.use.mom"), bigsis: (g) => g.say(g.flag("home.online") ? "home.closet.done.bigsis" : "home.closet.use.bigsis") },
    },
    {
      id: "piano", name: "piano", verb: "Play", rect: [216, 84, 46, 44], walkTo: [238, 135], face: "N",
      look: { mom: "home.piano.look.mom", bigsis: ["home.piano.look.bigsis", "home.piano.look.bigsis2"], lilsis: "home.piano.look.lilsis" }, use: playPiano,
    },
    { id: "computer", name: "computer", verb: "Use", rect: [123, 88, 40, 38], walkTo: [143, 133], face: "N", look: each("home.pc.look"), use: useComputer },
    {
      id: "note", name: "sticky note", verb: "Take", rect: [146, 86, 11, 10], walkTo: [150, 133], face: "N", when: (g) => !g.flag("home.noteTaken"),
      look: { mom: "home.note.look.mom", lilsis: "home.note.look.lilsis", bigsis: takeNote }, use: takeNote,
    },
    { id: "table", name: "dinner table", rect: [28, 150, 84, 40], walkTo: [122, 186], face: "W", look: each("home.table") },
    { id: "armchair", name: "Dad's armchair", rect: [264, 132, 40, 50], walkTo: [256, 186], face: "E", look: each("home.chair") },
  ],

  // Handing something to a companion: Big Sister is the one who can read Dad's note.
  async given(g, item, to) {
    if (item === "note" && to === "bigsis" && !g.flag("home.knowsYear")) await solveNote(g);
  },

  // What they say to each other. What has not been heard comes first.
  talk: {
    mom: {
      bigsis: [["home.talk.mom.bigsis.1a", "home.talk.mom.bigsis.1b"], ["home.talk.mom.bigsis.2a", "home.talk.mom.bigsis.2b", "home.talk.mom.bigsis.2c"]],
      lilsis: [["home.talk.mom.lilsis.1a", "home.talk.mom.lilsis.1b", "home.talk.mom.lilsis.1c"], ["home.talk.mom.lilsis.2a", "home.talk.mom.lilsis.2b"]],
    },
    bigsis: {
      mom: [["home.talk.bigsis.mom.1a", "home.talk.bigsis.mom.1b", "home.talk.bigsis.mom.1c"], ["home.talk.bigsis.mom.2a", "home.talk.bigsis.mom.2b"]],
      lilsis: [["home.talk.bigsis.lilsis.1a", "home.talk.bigsis.lilsis.1b"], ["home.talk.bigsis.lilsis.2a", "home.talk.bigsis.lilsis.2b"]],
    },
    lilsis: {
      mom: [["home.talk.lilsis.mom.1a", "home.talk.lilsis.mom.1b"], ["home.talk.lilsis.mom.2a", "home.talk.lilsis.mom.2b", "home.talk.lilsis.mom.2c"]],
      bigsis: [["home.talk.lilsis.bigsis.1a", "home.talk.lilsis.bigsis.1b", "home.talk.lilsis.bigsis.1c"], ["home.talk.lilsis.bigsis.2a", "home.talk.lilsis.bigsis.2b"]],
    },
  },

  // Runs on arrival. It must be safe to run twice, so it checks its own fact.
  async enter(g) {
    if (g.flag("home.arrived")) return;
    await g.wait(600);
    g.sfx("ring"); await g.wait(1100);
    g.sfx("ring"); await g.wait(1100);
    g.sfx("beep"); await g.wait(600);
    await g.say("home.arrive.vm1", "home.arrive.vm2", "home.arrive.1", "home.arrive.2", "home.arrive.2b", "home.arrive.3", "home.arrive.4", "home.arrive.5", "home.arrive.6", "home.arrive.7");
    g.flag("home.arrived", true);
    g.ui.toast("Play as any of the three: use the portraits", 5200);
  },
};

// Act Three, its one scene: the family's living room, at 9:40 in the evening. The present.
// Mom and the girls find out where Dad's phone was last seen.
//
// It is a team of three in one room. Each of them can do one thing the others cannot:
//   Little Sister fits into the closet under the stairs        (chain A: the router)
//   Big Sister knows the year behind Dad's password hint        (chain B: the note)
//   Mom knows what her husband promised on their wedding day    (chain C: the question), once A and B are done
// The player switches between them with the portraits, top left. A hotspot can answer
// each of them differently: { mom: ..., bigsis: ..., lilsis: ... }.
//
// The room is a painting (art/scenes/home-living-room/). The furniture people walk round is cut out of it, and
// two of the cut-outs follow the story by themselves: the screen on the desk and Dad's note stuck to it.
//
// Try it: index.html?scene=home-living-room&lead=mom
// Later states: &flags=home.arrived,home.online,home.noteTaken,home.knowsYear,home.typed,home.foundPing

const art = "art/scenes/home-living-room/";

const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
const who = (g) => g.store.data.active;

// ---------- the router's light ----------
// The one thing here that is light, so it is drawn live: a dot in the dark of the closet, low down behind the door.
// Red and unsteady while the router is off, green and steady once it is on.
const LED = [752, 405];
const DARK = [751, 356, 6, 74];                  // the strip of dark the door leaves open (x, y, width, height): its glow stops at the door and the frame
/** Make the light match the story. Runs on arrival, after loading a save, and at the moment the plug goes in. */
function light(g) {
  const led = g.q("#router-led"), on = !!g.flag("home.online");
  if (!led) return;
  led.setAttribute("fill", on ? "#4ade80" : "#ff4a3d");
  led.classList.toggle("flicker", !on);
}

// ---------- chain A: the router is in the closet under the stairs, and only one of them fits ----------
const DOOR = [755, 443];                         // where someone stands at the closet door (the same place as the closet's walkTo, below)
const GAP = [759, 432];                          // the foot of the dark gap the door leaves: the youngest goes in here
// Whoever is standing along the back of the room on that side comes forward onto the rug to watch: out of her way, and
// out from under her words, which are shown over the piano and the foot of the stairs. Three places, so that one is
// always free; the second is a step further back than the first, so that neither one's words lie over the other's head.
const ASIDE = [[486, 520], [556, 500], [424, 540]];
const atTheBack = (a) => a.x > 380 && a.y < 470;

async function intoCloset(g) {
  if (g.flag("home.online")) return g.say("home.closet.again");
  const lil = g.lead;
  const others = ["mom", "bigsis"].map((id) => g.actor(id)).filter(Boolean), inTheWay = others.filter(atTheBack);
  if (inTheWay.length) {
    const taken = (at) => others.some((a) => !inTheWay.includes(a) && Math.abs(a.x - at[0]) < 38 && Math.abs(a.y - at[1]) < 15);
    const free = ASIDE.filter((at) => !taken(at));
    const aside = Promise.all(inTheWay.map((a, n) => g.walkTo(free[n][0], free[n][1], a.id).then(() => a.face("E"))));
    await g.wait(250);                           // (they have a step's start on her)
    await g.walkTo(DOOR[0], DOOR[1]);
    lil.face("NE");
    await aside;                                 // she waits at the door, fists on her hips, until they are out of the way
  }
  await g.say("home.closet.go.1");
  await g.moveTo(GAP[0], GAP[1]);                // through the gap
  await g.tween(220, (k) => lil.fade(1 - k));
  await g.wait(300);
  await g.say("home.closet.go.2", "home.closet.go.3");
  g.sfx("plug");
  await g.wait(500);
  g.flag("home.online", true);                   // (the screen on the desk follows by itself)
  light(g);
  g.sfx("found");
  await g.say("home.closet.go.4");
  await g.tween(220, (k) => lil.fade(k));
  await g.moveTo(DOOR[0], DOOR[1]);
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
  g.flag("home.noteTaken", true);                // (the note comes off the monitor by itself)
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
  g.flag("home.foundPing", true);                // (and the screen on the desk shows the map from now on)
  await g.say("home.pc.right", "home.pc.map.1", "home.pc.map.2", "home.pc.map.3", "home.pc.map.4");
}

// ---------- the gate: out of the front door ----------
async function leave(g) {
  if (!g.flag("home.foundPing")) return g.say(`home.door.early.${who(g)}`);
  const me = g.lead;
  for (const id of ["mom", "bigsis", "lilsis"]) { const a = g.actor(id); if (a && a !== me) a.look(me.x, me.y); }     // the other two turn to the door
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

  // Every place in this file is the painter's own measurement of the finished picture (art/scenes/home-living-room/layout.json),
  // or was set by eye against the picture with the people standing in it. The act's check script (briefs/out/home-check.mjs)
  // reads this file against that one; the few differences that are meant are listed there.

  // DEPTH: indoors the floor is short, so people shrink only a little as they walk to the back wall.
  horizon: -150, full: 585,

  // The floorboards, from the back wall (it meets the floor at row 385) to the bottom of the picture.
  walk: { area: [[8, 393], [792, 393], [792, 598], [8, 598]] },
  // Ground that things stand on. (A cut-out can block one patch of its own; the desk and the piano need two each, so they are all here.)
  blocked: [
    [[291, 419], [297, 384], [399, 384], [399, 419]],             // the desk
    [[328, 437], [368, 423], [388, 456], [347, 472]],             // its chair, pushed back from it
    [[402, 384], [492, 384], [495, 400], [403, 400]],             // the bookcase
    [[497, 384], [602, 384], [618, 428], [505, 428]],             // the piano
    [[538, 443], [593, 442], [599, 463], [542, 463]],             // its stool
    [[591, 384], [800, 384], [800, 435], [609, 435]],             // the stairs, and the closet under them
    // The dinner table and its five chairs. The painter's right-hand edge is [306, 445] to [268, 600]. With the 12 pixels the
    // engine keeps clear of blocked ground, that shuts the way between the table and the desk chair, which is the only
    // way to the front door; and at the bottom it lets someone stand in front of the table with the cloth drawn over her.
    // So that edge is drawn where the cloth is: a body's half-width out from it all the way down.
    [[45, 600], [132, 442], [291, 445], [296, 600]],
    [[594, 523], [627, 476], [728, 503], [736, 575], [699, 576], [675, 572]],   // Dad's armchair, his lamp and the little table
    [[111, 400], [119, 384], [146, 384], [139, 401]],             // the box under the window
    [[0, 399], [0, 383], [16, 384], [6, 399]],                    // the umbrella stand by the front door
    [[270, 399], [273, 384], [294, 384], [291, 399]],             // the basket beside the desk
    [[0, 600], [4, 569], [54, 569], [38, 600]],                   // the aspidistra's pot (the front plane)
  ],

  // Three leads are here together. They arrive with whoever is leading, each on her own mark.
  // Mom and Big Sister are on the painter's marks. Little Sister's was [347, 492], level with them: there, being the
  // shortest, whatever she said lay across their faces. She stands between them and a step further back, in front of
  // the bookcase, where her words are above all three heads.
  party: ["mom", "bigsis", "lilsis"],
  spawn: { default: [419, 502], mom: [419, 502], bigsis: [510, 484], lilsis: [468, 454] },
  exits: ["nevada-roadside"],

  picture: art + "back.png",

  // CUT-OUTS. The desk, the piano, the armchair and the table are furniture to walk round. The screen and the note lie
  // over the desk's dark monitor and follow the story: a script records a fact, and the picture changes.
  planes: [
    { id: "desk", src: art + "desk.png", base: 419 },             // desk, chair and computer, the screen dark. (The base is the front of the desk.)
    {
      id: "screen", base: 420,                                    // what the monitor is showing
      state: (g) => (g.flag("home.foundPing") ? "map" : g.flag("home.online") ? "login" : "offline"),
      states: { offline: art + "screen-offline.png", login: art + "screen-login.png", map: art + "screen-map.png" },
    },
    { id: "note", src: art + "note.png", base: 421, when: (g) => !g.flag("home.noteTaken") },     // Dad's note, until somebody takes it
    { id: "piano", src: art + "piano.png", base: 427 },           // piano, lamp and stool. (The base is the piano's front legs.)
    // Dad's armchair, the reading lamp behind it, the little table, his slippers. The chair is turned toward the room, so it
    // meets the floor on a slant: the base is the line of its front, from its left corner down to its near corner. (The
    // painter's base is the row 572, its nearest point: with that, someone standing in front of the chair's left corner,
    // by the slippers, was drawn behind it with her feet showing under the seat.)
    { id: "armchair", src: art + "armchair.png", base: [[594, 523], [675, 572]] },
    { id: "table", src: art + "table.png", base: 599 },           // the dinner table, all five chairs, and the lamp hanging over it
    { id: "front", src: art + "front.png", plane: "front" },      // the aspidistra at the bottom left corner
  ],

  // LIGHT, drawn live: the router's little light, in the dark of the closet. `light` (above) gives it its color.
  live() {
    const at = `cx="${LED[0] + 0.5}" cy="${LED[1] + 0.5}"`;       // the middle of that pixel
    return `<clipPath id="closet-dark"><rect x="${DARK[0]}" y="${DARK[1]}" width="${DARK[2]}" height="${DARK[3]}"/></clipPath>
      <g clip-path="url(#closet-dark)"><g id="router-led" class="flicker" fill="#ff4a3d" shape-rendering="geometricPrecision"><circle ${at} r="5" opacity="0.25"/><circle ${at} r="1.6"/></g></g>`;
  },

  setup: light,

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    {
      id: "door", name: "front door", verb: "Open", rect: [17, 243, 75, 142], walkTo: [45, 401], face: "N", use: leave,
      look: (g) => g.say(`${g.flag("home.foundPing") ? "hint.home.leave" : "home.door.early"}.${who(g)}`),
    },
    { id: "window", name: "window", rect: [91, 207, 205, 130], walkTo: [146, 407], face: "N", look: each("home.window") },
    // (The painter's place to stand at the bookcase is 450, 412: straight behind where Little Sister stands at the start. This is the bookcase's left end.)
    { id: "books", name: "bookcase", rect: [405, 249, 86, 151], walkTo: [432, 412], face: "N", look: each("home.books") },
    // The photograph hangs over the piano. From close by (the painter's 531, 467) the words of whoever looks at it lie
    // right over it, so she stands back on the rug, where she can see it and so can we.
    { id: "photo", name: "family photograph", rect: [522, 235, 55, 41], walkTo: [540, 508], face: "N", look: each("home.photo") },
    // The stairs: the rail, the steps, and the panelling under them. (The painter's shape runs straight across Dad's
    // reading lamp, which stands in front of them: this one goes round the lamp shade.)
    { id: "stairs", name: "stairs", poly: [[612, 434], [612, 342], [676, 311], [800, 230], [800, 350], [745, 350], [745, 368], [696, 368], [696, 434]], walkTo: [609, 445], face: "NE", look: each("home.stairs") },
    {
      id: "closet", name: "closet under the stairs", verb: "Open", rect: [747, 353, 50, 87], walkTo: [755, 443], face: "NE",  // the whole doorway: the frame, the dark gap and the door
      look: (g) => g.say(g.flag("home.online") && who(g) !== "lilsis" ? `home.closet.done.${who(g)}` : g.flag("home.online") ? "home.closet.again" : `home.closet.look.${who(g)}`),
      use: { lilsis: intoCloset, mom: (g) => g.say(g.flag("home.online") ? "home.closet.done.mom" : "home.closet.use.mom"), bigsis: (g) => g.say(g.flag("home.online") ? "home.closet.done.bigsis" : "home.closet.use.bigsis") },
    },
    {
      // (She stands in front of the middle of the stool. The painter's place, 574, 467, is a few pixels to the right and inside
      // the margin the engine keeps round the stool; from there a third person at the piano would be stood behind Dad's armchair.)
      id: "piano", name: "piano", verb: "Play", walkTo: [568, 469], face: "N",                                               // with its lamp and its stool
      poly: [[500, 302], [582, 302], [584, 282], [602, 282], [604, 302], [611, 304], [614, 322], [615, 427], [600, 427], [600, 463], [541, 463], [541, 427], [501, 427]],
      look: { mom: "home.piano.look.mom", bigsis: ["home.piano.look.bigsis", "home.piano.look.bigsis2"], lilsis: "home.piano.look.lilsis" }, use: playPiano,
    },
    {
      id: "computer", name: "computer", verb: "Use", walkTo: [315, 429], face: "N", look: each("home.pc.look"), use: useComputer,   // the monitor, the desk and its chair
      poly: [[322, 313], [372, 313], [372, 337], [397, 337], [397, 419], [384, 419], [384, 428], [372, 440], [372, 459], [336, 459], [336, 440], [333, 419], [293, 419], [293, 337], [322, 337]],
    },
    {
      id: "note", name: "sticky note", verb: "Take", rect: [355, 313, 17, 17], walkTo: [315, 429], face: "NE", when: (g) => !g.flag("home.noteTaken"),
      look: { mom: "home.note.look.mom", lilsis: "home.note.look.lilsis", bigsis: takeNote }, use: takeNote,
    },
    {
      id: "table", name: "dinner table", walkTo: [316, 521], face: "W", look: each("home.table"),                            // the table and the five chairs round it
      poly: [[140, 376], [279, 376], [284, 422], [282, 507], [270, 507], [270, 552], [238, 552], [238, 599], [98, 599], [98, 508], [89, 506], [89, 484], [120, 421], [140, 418]],
    },
    {
      id: "armchair", name: "Dad's armchair", walkTo: [578, 504], face: "E", look: each("home.chair"),                       // the chair and his slippers
      poly: [[628, 418], [640, 406], [660, 407], [682, 424], [696, 446], [697, 470], [701, 480], [699, 522], [678, 561], [671, 561], [641, 549], [641, 566], [608, 566], [606, 538], [598, 518], [598, 476], [612, 462], [627, 440]],
    },
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

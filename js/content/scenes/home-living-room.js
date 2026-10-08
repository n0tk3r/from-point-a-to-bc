// Act Three, the first of its five scenes: the family's living room, at 9:40 in the evening. The present.
// Mom and the girls set out to learn where Dad and the Son have got to. The act opens here and ends here.
//
// The house is five scenes, and the three of them go through it TOGETHER (`party`): when the one being played
// takes the stairs, the other two come too. The player switches between them with the portraits, top left.
//   home-living-room   the piano (the study key is inside it), the closet under the stairs (the router),
//                      Dad's crossword and his pencil, the framed Preamble (the year the vault wants), the front door
//   home-landing       upstairs: the Son's door, Little Sister's door, Dad's study door and the notice taped to it,
//                      and the ladder up to the attic
//   home-study         the family computer, the answering machine, the family vault
//   home-lilsis-room   Little Sister's room: the flock, the blanket fort, and in the fort her flashlight (dead)
//   home-bigsis-room   Big Sister's attic, the Retreat: her timeline, and the sound machine with the only batteries
//
// What happens in this room:
//   the opening        the ninth voicemail, five places set, a prayer, and where the computer is
//   chain A            someone reads Dad's riddle upstairs (or hears a dead note here): the key is in the piano.
//                      Mom can see it, Big Sister can hear it, and Little Sister can get under the keyboard for it.
//   chain B            the router is in the closet under the stairs, which is too dark until Little Sister has her
//                      flashlight, and the flashlight has batteries in it that work (Big Sister's, from the Retreat)
//   the gate           the front door: they leave when they have the dot on the map, Dad's message and a car key
// A hotspot can answer each of them differently: { mom: ..., bigsis: ..., lilsis: ... }.
//
// Every place below is measured from the finished painting (art/scenes/home-living-room/layout.json is the painter's
// own list): the table runs away from us with its head at the far end, and Dad's chair has its back to us.
//
// Try it: index.html?scene=home-living-room&lead=mom
// Later states: &flags=home.arrived,home.keyInPiano,home.hasKey,home.studyOpen,home.flashTaken,home.flashWorks,home.online,home.knowsYear,home.foundPing,home.tapeWound,home.heardMessage,home.hasCarKey

const art = "art/scenes/home-living-room/";

const THREE = ["mom", "bigsis", "lilsis"];
const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
const who = (g) => g.store.data.active;
/** Are the three of them on stage? (A test, or a visitor from another act, can walk somebody else in.) */
const home = (g) => THREE.every((id) => g.actor(id));
/** Head bowed, hands folded. */
const pray = (a, on) => a && a.pray && a.pray(on);

// ---------- the router's light ----------
// Light, so it is drawn live: a dot in the dark of the closet, low down, in the gap the door leaves.
// Red and unsteady while the router is off, green and steady once it is on.
const LED = [206, 392];
const DARK = [203, 325, 7, 82];                  // the strip of dark the door leaves open (x, y, width, height)
/** Make the light match the story. Runs on arrival, after loading a save, and at the moment the plug goes in. */
function light(g) {
  const led = g.q("#router-led"), on = !!g.flag("home.online");
  if (!led) return;
  led.setAttribute("fill", on ? "#4ade80" : "#ff4a3d");
  led.classList.toggle("flicker", !on);
}
/** The glow of a child's flashlight in the gap, while she is in there with it. */
const glow = (g, k) => { const el = g.q("#closet-glow"); if (el) el.setAttribute("opacity", k); };

// ---------- making room ----------
/** Whoever is standing close to a place walks to one of the free marks nearby, and turns to watch. */
async function makeRoom(g, at, marks, reach = 70) {
  const me = g.lead, others = THREE.map((id) => g.actor(id)).filter((a) => a && a !== me);
  const close = others.filter((a) => Math.abs(a.x - at[0]) < reach && Math.abs(a.y - at[1]) < reach * 0.6);
  const taken = (m) => others.some((a) => !close.includes(a) && Math.abs(a.x - m[0]) < 38 && Math.abs(a.y - m[1]) < 15);
  const free = marks.filter((m) => !taken(m));
  await Promise.all(close.map((a, n) => (free[n] ? g.walkTo(free[n][0], free[n][1], a.id).then(() => a.look(at[0], at[1])) : null)));
  for (const a of others) a.look(at[0], at[1]);
}

// ---------- chain B: the router is in the closet under the stairs. Only one of them fits, and it is dark ----------
const DOOR = [256, 408];                         // where someone stands at the closet door (the closet's walkTo, below)
const GAP = [212, 409];                          // the foot of the dark gap the door leaves: the youngest goes in here
const ASIDE = [[318, 428], [372, 452], [300, 468]];   // where the other two stand to watch

async function intoCloset(g) {
  if (g.flag("home.online")) return g.say("home.closet.again");
  const lil = g.lead, mine = g.has("lilflash"), lit = mine && !!g.flag("home.flashWorks");
  // A flashlight with nothing in it is no light at all: she knows it is dead from the moment she picked it up.
  if (mine && !lit) return g.say("home.closet.dead");
  // She has been in once, and will not go again without her flashlight.
  if (!mine && g.flag("home.sawDark")) return g.say(g.holder("lilflash") ? "home.closet.lent" : "home.closet.needflash");
  await makeRoom(g, DOOR, ASIDE);
  lil.face("W");
  await g.say("home.closet.go.1");
  await g.moveTo(GAP[0], GAP[1]);                // through the gap
  await g.tween(220, (k) => lil.fade(1 - k));
  await g.wait(300);
  if (!lit) {                                    // too dark to find anything: out she comes, wanting her own flashlight
    await g.say("home.closet.dark.1");
    await g.tween(220, (k) => lil.fade(k));
    await g.moveTo(DOOR[0], DOOR[1]);
    lil.face("S");
    g.flag("home.sawDark", true);
    return g.say("home.closet.dark.2", "home.closet.dark.3");
  }
  g.sfx("click");
  glow(g, 1);
  await g.say("home.closet.go.2", "home.closet.go.3");
  g.sfx("plug");
  await g.wait(500);
  g.flag("home.online", true);
  light(g);
  g.sfx("found");
  await g.say("home.closet.go.4");
  glow(g, 0);
  await g.tween(220, (k) => lil.fade(k));
  await g.moveTo(DOOR[0], DOOR[1]);
  lil.face("S");
  await g.say("home.closet.go.5", "home.closet.go.6");
}

const closetLook = (g) => g.say(g.flag("home.online") ? (who(g) === "lilsis" ? "home.closet.again" : `home.closet.done.${who(g)}`) : `home.closet.look.${who(g)}`);
const closetOthers = (g) => g.say(g.flag("home.online") ? `home.closet.done.${who(g)}` : `home.closet.use.${who(g)}`);

// ---------- chain A: the study key is in the piano ----------
const STOOL = [568, 383];                        // where someone stands to play (the piano's walkTo, below)
const UNDER = [588, 374];                        // under the keyboard, by the pedals: behind the piano's cut-out, so the bench hides her
const BESIDE = [[607, 387], [506, 392], [652, 404]];  // where the other two stand to watch (the first is at the player's elbow)

/** The dead note is found out: by Mom or by Big Sister, playing. */
async function thunk(g, me) {
  g.sfx(me === "mom" ? "hymndead" : "pianodead");
  await g.wait(me === "mom" ? 1200 : 900);       // (where the missing note falls in each phrase: js/content/sound.js)
  g.sfx("thunk");
  await g.wait(1400);
  await g.say(`home.thunk.${me}.1`, `home.thunk.${me}.2`);
  g.flag("home.keyInPiano", true);
  await g.say(`home.thunk.${me === "mom" ? "bigsis" : "mom"}.react`);
}

/** They know it is in there. Mom can see it, Big Sister can hear it, and Little Sister can go and get it. */
async function fetchKey(g) {
  const me = who(g), lil = g.lead;
  if (me === "mom") { await g.reach(); return g.say("home.key.mom.1", "home.key.mom.2", "home.key.mom.3"); }
  if (me === "bigsis") { await g.reach(); g.sfx("thunk"); await g.wait(500); return g.say("home.key.bigsis.1", "home.key.bigsis.2"); }
  await makeRoom(g, STOOL, BESIDE);
  lil.face("N");
  await g.say("home.closet.go.1");               // "I FIT!" It is hers, and it belongs here as much as at the closet.
  await g.moveTo(UNDER[0], UNDER[1]);
  await g.reach(true);
  await g.tween(200, (k) => lil.fade(1 - 0.75 * k));    // under the keyboard, behind the stool
  await g.say("home.key.get.1");
  g.sfx("panel");
  await g.wait(500);
  await g.say("home.key.get.2");
  await g.tween(200, (k) => lil.fade(0.25 + 0.75 * k));
  await g.moveTo(STOOL[0], STOOL[1]);
  lil.face("S");
  g.flag("home.hasKey", true);                   // (the piano's lower panel stays off from now on: its cut-out follows this fact)
  g.give("studykey");
  await g.say("home.key.get.3", "home.key.get.4", "home.key.get.5");
}

async function playPiano(g) {
  const me = who(g), known = g.flag("home.keyInPiano"), out = g.flag("home.hasKey");
  if (known && !out) return fetchKey(g);
  await g.reach();
  if (me === "lilsis") {
    g.sfx("plonk");
    await g.wait(500);
    return g.say("home.piano.use.lilsis");
  }
  if (!out) return thunk(g, me);                 // the key is on the hammers, and nobody knows it yet
  if (me === "bigsis") {
    g.sfx("piano");
    await g.wait(3300);
    await g.say(g.flag("home.played") ? "home.piano.use.bigsis2" : "home.piano.use.bigsis");
    g.flag("home.played", true);
    return;
  }
  g.sfx("hymn");                                 // Mom: a hymn she names, quietly, for courage
  await g.wait(3900);
  await g.say(...(g.flag("home.hymned") ? ["home.piano.use.mom3"] : ["home.piano.use.mom", "home.piano.use.mom2"]));
  g.flag("home.hymned", true);
}

const pianoLook = (g) => {
  const me = who(g);
  if (g.flag("home.keyInPiano") && !g.flag("home.hasKey")) return g.say(`home.piano.key.${me}`);
  return g.say(...(me === "bigsis" ? ["home.piano.look.bigsis", "home.piano.look.bigsis2"] : [`home.piano.look.${me}`]));
};

// ---------- Dad's pencil, on his crossword ----------
async function takePencil(g) {
  await g.reach();
  g.flag("home.pencilTaken", true);              // (the pencil comes off the crossword by itself: its cut-out follows this fact)
  g.give("pencil");
  await g.say(`home.pencil.take.${who(g)}`);
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

// ---------- the gate: out of the front door ----------
/** What is still missing, in the voice of whoever is asked: a destination, Dad's message, a car key. Null when nothing is. */
const missing = (g) => (!g.flag("home.foundPing") ? "early" : !g.flag("home.heardMessage") ? "message" : !g.flag("home.hasCarKey") ? "nokey" : null);

const FRONT = [688, 381];                        // where someone stands at the front door (its walkTo, below)
const HALL = [[640, 398], [600, 392], [664, 414]];    // where the other two step aside to, so that nobody stands in anybody

async function leave(g) {
  await makeRoom(g, FRONT, HALL);
  const me = g.lead, lack = missing(g);
  if (lack) {
    await g.say(`home.door.${lack}.${who(g)}`);
    if (!g.flag("home.triedDoor") && !g.flag("home.hasCarKey")) {      // the first time anyone tries to leave: why they will want a key, and where the spare is
      g.flag("home.triedDoor", true);
      await g.say("home.door.keys.1", "home.door.keys.2", "home.door.keys.3");
    }
    return;
  }
  for (const id of THREE) { const a = g.actor(id); if (a && a !== me) a.look(me.x, me.y); }     // the other two turn to the door
  // Mom will not start a journey without the psalm they always read first.
  await g.say("home.door.psalm.1", "home.door.psalm.2");
  for (const id of THREE) pray(g.actor(id), true);
  await g.say("home.door.psalm.3", "home.door.psalm.4");
  for (const id of THREE) pray(g.actor(id), false);
  await g.say("home.leave.1", "home.leave.2", "home.leave.3", "home.leave.4");
  g.flag("home.left", true);
  g.store.data.act = 4;
  await g.fade(1, 700);
  await g.goto("nevada-roadside", { via: "cut" });
}

export default {
  id: "home-living-room",
  era: "home",
  name: "The living room, 9:40 p.m.",

  // DEPTH, from the room's camera (layout.json).
  horizon: 150, full: 455,

  // The floor: from the back wall under the landing, round the rug, to the armchair (front left) and the head of the
  // table (front right). The piano's own ground is blocked by its cut-out (`solid`, below).
  walk: { area: [[321, 344], [102, 486], [132, 510], [288, 534], [408, 525], [466, 502], [705, 530], [739, 503], [698, 380]] },

  // Three leads are here together. They arrive with whoever is leading: on the rug when the act opens,
  // at the foot of the stairs when they come down from the landing.
  party: ["mom", "bigsis", "lilsis"],
  spawn: { default: [435, 418], mom: [435, 418], bigsis: [513, 413], lilsis: [385, 404], fromLanding: [121, 494] },
  arrive: { fromLanding: [[205, 468], [292, 500]] },
  exits: ["home-landing", "nevada-roadside"],

  picture: art + "back.png",

  // CUT-OUTS. The piano stands on the floor and people go round it; the other three are in front of everybody.
  planes: [
    // piano, lamp and bench; its lower panel is off, and leaning beside it, once the key is out
    {
      id: "piano", base: [[530, 372], [644, 383]], solid: [[536, 357], [643, 367], [645, 384], [530, 373]],
      state: (g) => (g.flag("home.hasKey") ? "open" : "shut"), states: { shut: art + "piano.png", open: art + "piano-open.png" },
    },
    { id: "armchair", src: art + "armchair.png", plane: "front" },   // Dad's chair from behind, his reading lamp, the crossword on its arm
    { id: "pencil", src: art + "pencil.png", plane: "front", when: (g) => !g.flag("home.pencilTaken") },   // his pencil, until somebody takes it
    { id: "table", src: art + "table.png", plane: "front" },   // the dinner table, its chairs, the lamp over it, the Bible
  ],

  // LIGHT, drawn live: the router's little light in the dark of the closet (`light`, above, gives it its color),
  // and the glow of Little Sister's flashlight when she is in there with it.
  live() {
    const at = `cx="${LED[0] + 0.5}" cy="${LED[1] + 0.5}"`;
    return `<clipPath id="closet-dark"><rect x="${DARK[0]}" y="${DARK[1]}" width="${DARK[2]}" height="${DARK[3]}"/></clipPath>
      <g clip-path="url(#closet-dark)" shape-rendering="geometricPrecision">
        <rect id="closet-glow" x="${DARK[0]}" y="${DARK[1]}" width="${DARK[2]}" height="${DARK[3]}" fill="#ffe9a8" opacity="0"/>
        <g id="router-led" class="flicker" fill="#ff4a3d"><circle ${at} r="5" opacity="0.25"/><circle ${at} r="1.6"/></g>
      </g>`;
  },

  setup: light,

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "landing", name: "the landing upstairs", poly: [[286, 44], [752, 32], [752, 192], [286, 192]], walkTo: [435, 418], face: "N", look: each("home.upstairs") },
    {
      id: "stairs", name: "the stairs", verb: "Go up", walkTo: [121, 494], face: "W",
      poly: [[19, 458], [100, 473], [283, 180], [283, 118], [262, 118], [196, 200], [172, 234], [120, 238], [19, 340]],
      look: each("home.stairs"), use: (g) => g.goto("home-landing", { spawn: "fromStairs" }),
    },
    { id: "window", name: "stair window", poly: [[117, 6], [216, 6], [216, 172], [197, 199], [173, 233], [117, 241]], walkTo: [174, 470], face: "W", look: each("home.window") },
    { id: "photos", name: "family photographs", poly: [[0, 76], [116, 76], [116, 240], [19, 338], [0, 345]], walkTo: [142, 488], face: "W", look: each("home.photo") },
    {
      id: "closet", name: "closet under the stairs", verb: "Open", poly: [[199, 321], [236, 307], [238, 394], [212, 411], [199, 410]], walkTo: [256, 408], face: "W",
      look: closetLook, use: { lilsis: intoCloset, any: closetOthers },
      useWith: { lilflash: { lilsis: intoCloset, any: closetOthers }, studykey: each("home.closet.key") },
    },
    { id: "books", name: "Mom's bookcase", rect: [324, 196, 80, 147], walkTo: [351, 349], face: "N", look: (g) => g.say(...(who(g) === "mom" ? ["home.shelf.mom", "home.shelf.mom2"] : [`home.shelf.${who(g)}`])) },
    { id: "kitchen", name: "kitchen", rect: [405, 205, 87, 142], walkTo: [434, 357], face: "N", look: each("home.kitchen") },
    { id: "frame", name: "'We the People'", rect: [491, 205, 48, 66], walkTo: [504, 364], face: "N", look: each("home.frame") },
    { id: "clock", name: "clock", circle: [569, 222, 15], walkTo: [525, 369], face: "N", look: each("home.clock") },
    {
      id: "piano", name: "piano", verb: "Play", walkTo: [568, 383], face: "N",
      poly: [[538, 270], [552, 258], [600, 258], [606, 248], [628, 248], [640, 270], [641, 362], [616, 366], [616, 381], [556, 378], [556, 360], [538, 357]],
      look: pianoLook, use: playPiano, useWith: { studykey: each("home.piano.keyback"), lilflash: { lilsis: playPiano } },
    },
    {
      id: "door", name: "front door", verb: "Open", rect: [649, 240, 70, 137], walkTo: [688, 381], face: "N",
      look: async (g) => { await makeRoom(g, FRONT, HALL); return g.say(missing(g) ? `home.door.look.${who(g)}` : `hint.home.leave.${who(g)}`); }, use: leave,
      useWith: { carkey: leave, studykey: each("home.door.studykey") },
    },
    { id: "sampler", name: "sampler", rect: [641, 203, 85, 39], walkTo: [689, 385], face: "N", look: each("home.sampler") },
    { id: "coats", name: "coat hooks", rect: [717, 252, 32, 146], walkTo: [693, 388], face: "E", look: each("home.coats") },
    {
      id: "armchair", name: "Dad's armchair", walkTo: [285, 525], face: "SW", look: each("home.chair"),
      poly: [[70, 484], [100, 470], [124, 478], [150, 470], [190, 482], [196, 502], [242, 522], [247, 560], [247, 600], [68, 600]],
    },
    { id: "crossword", name: "Dad's crossword", poly: [[180, 534], [226, 516], [236, 529], [234, 540], [192, 551]], walkTo: [285, 525], face: "SW", look: each("home.crossword") },
    {
      id: "pencil", name: "Dad's pencil", verb: "Take", rect: [189, 525, 37, 11], walkTo: [285, 525], face: "SW", when: (g) => !g.flag("home.pencilTaken"),
      look: each("home.pencil.look"), use: takePencil,
    },
    {
      id: "table", name: "dinner table", walkTo: [496, 504], face: "E", look: each("home.table"),
      poly: [[520, 470], [572, 462], [574, 428], [624, 428], [626, 464], [670, 470], [678, 522], [728, 536], [730, 468], [742, 468], [744, 542], [800, 572],
        [800, 600], [388, 600], [388, 490], [401, 490], [403, 562], [461, 566], [460, 456], [484, 440], [487, 503], [513, 507]],
    },
    { id: "bible", name: "family Bible", poly: [[523, 456], [577, 461], [573, 484], [520, 478]], walkTo: [496, 504], face: "E", look: each("home.bible") },
  ],

  given,

  // What they say to each other. What has not been heard comes first.
  talk: {
    mom: {
      bigsis: [
        { when: (g) => g.flag("home.keyInPiano") && !g.flag("home.hasKey"), say: ["home.talk.mom.bigsis.key.a", "home.talk.mom.bigsis.key.b"] },
        { when: (g) => g.flag("home.flashTaken") && !g.flag("home.flashWorks") && !g.holder("batteries"), say: ["home.talk.batt.mom.bigsis.a", "home.talk.batt.mom.bigsis.b"] },
        ["home.talk.mom.bigsis.1a", "home.talk.mom.bigsis.1b"],
        ["home.talk.mom.bigsis.2a", "home.talk.mom.bigsis.2b", "home.talk.mom.bigsis.2c"],
      ],
      lilsis: [
        { when: (g) => g.flag("home.sawDark") && !g.flag("home.online") && !g.holder("lilflash"), say: ["home.talk.mom.lilsis.dark.a", "home.talk.mom.lilsis.dark.b"] },
        { when: (g) => !!g.holder("batteries") && !g.flag("home.flashWorks"), say: ["home.talk.batt.mom.lilsis.a", "home.talk.batt.mom.lilsis.b"] },
        ["home.talk.mom.lilsis.1a", "home.talk.mom.lilsis.1b", "home.talk.mom.lilsis.1c"],
        ["home.talk.mom.lilsis.2a", "home.talk.mom.lilsis.2b"],
      ],
    },
    bigsis: {
      mom: [["home.talk.bigsis.mom.1a", "home.talk.bigsis.mom.1b", "home.talk.bigsis.mom.1c"], ["home.talk.bigsis.mom.2a", "home.talk.bigsis.mom.2b"]],
      lilsis: [
        { when: (g) => g.flag("home.keyInPiano") && !g.flag("home.hasKey"), say: ["home.talk.bigsis.lilsis.key.a", "home.talk.bigsis.lilsis.key.b"] },
        ["home.talk.bigsis.lilsis.1a", "home.talk.bigsis.lilsis.1b"],
        ["home.talk.bigsis.lilsis.2a", "home.talk.bigsis.lilsis.2b"],
      ],
    },
    lilsis: {
      mom: [["home.talk.lilsis.mom.1a", "home.talk.lilsis.mom.1b"], ["home.talk.lilsis.mom.2a", "home.talk.lilsis.mom.2b", "home.talk.lilsis.mom.2c"]],
      bigsis: [
        { when: (g) => g.flag("home.flashTaken") && !g.flag("home.flashWorks") && !g.holder("batteries"), say: ["home.talk.batt.lilsis.bigsis.a", "home.talk.batt.lilsis.bigsis.b"] },
        ["home.talk.lilsis.bigsis.1a", "home.talk.lilsis.bigsis.1b", "home.talk.lilsis.bigsis.1c"],
        ["home.talk.lilsis.bigsis.2a", "home.talk.lilsis.bigsis.2b"],
      ],
    },
  },

  // Runs on arrival. It must be safe to run twice, so it checks its own fact.
  async enter(g) {
    if (g.flag("home.arrived") || !home(g)) return;
    await g.wait(600);
    g.sfx("ring"); await g.wait(1100);
    g.sfx("ring"); await g.wait(1100);
    g.sfx("beep"); await g.wait(600);
    await g.say("home.arrive.vm1", "home.arrive.vm2", "home.arrive.1", "home.arrive.2", "home.arrive.2b", "home.arrive.3", "home.arrive.4");
    // First things first.
    await g.say("home.arrive.pray.1");
    for (const id of THREE) pray(g.actor(id), true);
    await g.wait(500);
    await g.say("home.arrive.pray.2", "home.arrive.pray.3", "home.arrive.pray.4", "home.arrive.pray.5");
    for (const id of THREE) pray(g.actor(id), false);
    await g.wait(300);
    await g.say("home.arrive.5", "home.arrive.6", "home.arrive.6b", "home.pc.router", "home.arrive.7");
    g.flag("home.arrived", true);
    g.ui.toast("Play as any of the three: use the portraits", 5200);
  },
};

// Act Three, the fourth of its five scenes: Little Sister's room, under the roof. A seven-year-old's kingdom of chickens.
// (Big Sister lived in here too until her thirteenth birthday. She has the attic now: home-bigsis-room.js.)
//
// What happens here:
//   chain B   the closet under the stairs is too dark, and Little Sister will not go in without her own flashlight.
//             It lives just inside her blanket fort, where nobody but she may go (NO BIG SISTERS: her sign, her rule).
//             She fetches it, clicks it, and it is DEAD: she ran it down last night, reading to the flock under the
//             blanket. The only batteries of that size in the house are upstairs, in Big Sister's sound machine.
//   the chickens   every stuffed chicken has a name and a rank or a job. Her favorite, General Feathers, is not here:
//             she went on the trip in Daddy's suitcase, to keep an eye on him, and her place on the pillow is RESERVED.
//             "Chickens KNOW." is said here first. And Mom, at the nest, says the truest thing in the room.
// The three of them go through the house together (`party`): see home-living-room.js.
//
// Every place below is measured from the finished painting (art/scenes/home-lilsis-room/layout.json is the painter's own list).
//
// Try it: index.html?scene=home-lilsis-room&lead=lilsis&flags=home.arrived
// Later states: &flags=home.arrived,home.sawDark,home.flashTaken,home.flashWorks,home.online

const art = "art/scenes/home-lilsis-room/";

const THREE = ["mom", "bigsis", "lilsis"];
const each = (id) => ({ mom: `${id}.mom`, bigsis: `${id}.bigsis`, lilsis: `${id}.lilsis` });
const who = (g) => g.store.data.active;
/** Are the three of them on stage? (A test, or a visitor from another act, can walk somebody else in.) */
const home = (g) => THREE.every((id) => g.actor(id));

// ---------- chain B: the blanket fort, and the flashlight in it ----------
/** Only one of them may go in, and she made the rule. What she brings out does not light. */
async function fort(g) {
  const me = who(g);
  if (me !== "lilsis") return g.say(`home.fort.use.${me}`);
  if (g.flag("home.flashTaken")) return g.say("home.fort.again");
  await g.reach(true);
  g.flag("home.flashTaken", true);               // (the flashlight is gone from the fort's way in: its cut-out follows this fact)
  g.give("lilflash");
  g.sfx("deadclick");
  await g.wait(500);
  await g.say(g.flag("home.sawDark") ? "home.fort.take.dark" : "home.fort.take.early");
  g.sfx("deadclick");
  await g.wait(400);
  await g.say("home.fort.take.2");
  if (home(g)) await g.say("home.fort.take.3", "home.fort.take.4");   // what it wants, and where the only ones are
}
const fortLook = (g) => g.say(`home.fort.${g.flag("home.flashTaken") ? "empty" : "look"}.${who(g)}`);

/** Her flashlight, shined at something: only when it has batteries in it that work. */
const shine = (line) => (g) => g.say(g.flag("home.flashWorks") ? line : "home.flash.dead");

// ---------- having a place to oneself ----------
// Two things in this room are small and easily hidden by whoever stands in front of them (the place on the pillow,
// the flashlight in the fort's way in), and the ground at the fort is too narrow for three. So whoever comes to the
// bed or to the fort has it to herself: the others step back to where they can watch, and she takes the place.
const BEDSIDE = [545, 424];                      // where one stands for the bed, the pillow and the lamp (their walkTo, below)
const DOORWAY = [[518, 469], [461, 475]];        // where the others step back to from the bed: two of the places they came in to
const FORT = [227, 471];                         // where one stands at the fort (its walkTo, and the flashlight's)
const RUG = [[292, 432], [334, 446]];            // where the others step back to from the fort: the edge of the fried-egg rug
async function standBack(g, place, marks, inTheWay, face) {
  const me = g.lead, others = THREE.map((id) => g.actor(id)).filter((a) => a && a !== me);
  const near = others.filter(inTheWay);
  const taken = (m) => others.some((a) => !near.includes(a) && Math.abs(a.x - m[0]) < 30 && Math.abs(a.y - m[1]) < 12);
  const free = marks.filter((m) => !taken(m));
  await Promise.all(near.map((a, n) => (free[n] ? g.walkTo(free[n][0], free[n][1], a.id).then(() => a.look(place[0], place[1] - 60)) : null)));
  if (Math.abs(me.x - place[0]) > 3 || Math.abs(me.y - place[1]) > 3) { await g.walkTo(place[0], place[1]); me.face(face); }
}
const then = (g, action) => (typeof action === "function" ? action(g) : g.say(action[who(g)]));
/** (Anybody standing between the bed and us hides the pillow, wherever her feet are.) */
const atBed = (action) => async (g) => { await standBack(g, BEDSIDE, DOORWAY, (a) => a.x > 535 && a.x < 665, "E"); return then(g, action); };
const atFort = (action) => async (g) => { await standBack(g, FORT, RUG, (a) => a.x < 284 && a.y > 420, "W"); return then(g, action); };

// ---------- Mom, at the nest ----------
const nestLook = (g) => g.say(...(who(g) === "mom" ? ["home.nest.mom", "home.nest.mom2"] : [`home.nest.${who(g)}`]));
// ---------- the reserved place on the pillow ----------
const pillowLook = (g) => g.say(...(who(g) === "lilsis" ? ["home.pillow.lilsis", "home.pillow.lilsis2"] : [`home.pillow.${who(g)}`]));
// ---------- the flock, where "Chickens KNOW." is said for the first time ----------
const flockLook = (g) => g.say(...(who(g) === "lilsis" ? ["home.flock.lilsis", "home.flock.lilsis2"] : [`home.flock.${who(g)}`]));

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

export default {
  id: "home-lilsis-room",
  era: "home",
  name: "Little Sister's room",

  // DEPTH, from the room's camera (layout.json).
  horizon: 120, full: 440,

  // The floor between the flock (far left), the bed (right), the fort (near left) and the hen house and the nest
  // (front), round the fried-egg rug. The tea party stands in the middle of it, and the way from the door to the
  // rest of the room is the gap between its table and the foot of the bed: `margin` is how near a figure's feet may
  // come to blocked ground (the engine's usual 12 by 5 would shut that gap, and nobody could reach the fort).
  walk: {
    margin: [6, 3],
    area: [[309, 369], [482, 363], [511, 405], [547, 405], [588, 455], [602, 456], [619, 477], [458, 485], [445, 450], [269, 458], [267, 472], [216, 474], [230, 427], [242, 420], [250, 388], [301, 382], [309, 377]],
  },
  blocked: [
    [[386, 404], [487, 400], [511, 440], [396, 445]],   // the tea party
  ],

  party: ["mom", "bigsis", "lilsis"],
  spawn: { default: [518, 469], mom: [518, 469], bigsis: [461, 475], lilsis: [580, 471], fromLanding: [518, 469] },
  arrive: { fromLanding: [[461, 475], [580, 471]] },
  exits: ["home-landing"],

  picture: art + "back.png",

  // CUT-OUTS. The fort and the tea party stand on the floor and people go round them; the rest is in front of everybody.
  planes: [
    { id: "fort", src: art + "fort.png", base: [[0, 484], [203, 474]] },   // the blanket fort and its sign
    { id: "flashlight", src: art + "flashlight.png", base: [[0, 485], [203, 475]], when: (g) => !g.flag("home.flashTaken") },   // her flashlight in the fort's way in, until she takes it
    { id: "teaparty", src: art + "teaparty.png", base: [[392, 445], [513, 440]] },   // the low table, the spotted teapot and the four guests
    { id: "front", src: art + "front.png", plane: "front" },   // her toy box, the crate of picture books, the hen house, the nest, the door; and the mobile of felt chickens
  ],

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "window", name: "window", poly: [[276, 146], [318, 146], [318, 100], [376, 100], [376, 146], [422, 146], [422, 303], [276, 303]], walkTo: [352, 369], face: "N", look: each("home.lilroom.window") },
    { id: "drawings", name: "her drawings", poly: [[163, 222], [190, 200], [212, 184], [276, 184], [276, 296], [163, 296]], walkTo: [299, 387], face: "N", look: each("home.drawings") },
    { id: "chart", name: "'MY CHICKENS'", rect: [398, 224, 85, 75], walkTo: [477, 368], face: "N", look: each("home.chart") },
    { id: "flock", name: "the flock", poly: [[134, 383], [138, 330], [168, 300], [190, 280], [232, 276], [264, 300], [289, 332], [289, 383]], walkTo: [299, 387], face: "W", look: flockLook },
    { id: "lamp", name: "rooster lamp", poly: [[516, 300], [548, 295], [557, 330], [556, 400], [511, 402], [509, 352], [520, 330]], walkTo: [545, 424], face: "N", look: atBed(each("home.lamp")) },
    { id: "bed", name: "her bed", poly: [[560, 345], [562, 305], [640, 300], [648, 345], [692, 410], [692, 452], [598, 452], [556, 395]], walkTo: [545, 424], face: "E", look: atBed(each("home.lilbed")) },
    { id: "pillow", name: "the place on the pillow", rect: [560, 319, 72, 46], walkTo: [545, 424], face: "E", look: atBed(pillowLook) },
    { id: "teaparty", name: "tea party", rect: [384, 352, 116, 85], walkTo: [375, 424], face: "E", look: each("home.teaparty") },
    {
      id: "fort", name: "blanket fort", verb: "Go into", poly: [[0, 400], [20, 384], [120, 344], [206, 378], [216, 440], [206, 476], [0, 488]], walkTo: [227, 471], face: "W",
      look: atFort(fortLook), use: atFort(fort), useWith: { lilflash: atFort(each("home.fort.putback")) },
    },
    {
      id: "flashlight", name: "her flashlight", verb: "Take", rect: [127, 466, 42, 15], walkTo: [227, 471], face: "W", when: (g) => !g.flag("home.flashTaken"),
      look: atFort(each("home.flashlight")), use: atFort(fort),
    },
    {
      id: "coop", name: "the hen house", walkTo: [256, 469], face: "S", look: each("home.coop"), useWith: { lilflash: { lilsis: shine("home.coop.flash") } },
      poly: [[280, 512], [285, 452], [440, 448], [448, 512], [444, 580], [376, 582], [376, 600], [352, 600], [352, 582], [285, 580]],
    },
    { id: "nest", name: "the nest", poly: [[520, 512], [553, 506], [556, 486], [572, 480], [603, 497], [606, 512], [640, 518], [640, 586], [540, 590], [520, 560]], walkTo: [524, 479], face: "S", look: nestLook },
    {
      id: "door", name: "the door to the landing", verb: "Go through", rect: [703, 296, 97, 304], walkTo: [609, 474], face: "E",
      look: each("home.lilroom.door"), use: (g) => g.goto("home-landing", { spawn: "fromLilsis" }),
    },
  ],

  given,

  // What they say to each other in here. What has not been heard comes first.
  talk: {
    mom: {
      bigsis: [
        { when: (g) => g.flag("home.flashTaken") && !g.flag("home.flashWorks") && !g.holder("batteries"), say: ["home.talk.batt.mom.bigsis.a", "home.talk.batt.mom.bigsis.b"] },
        ["home.talk.lilroom.mom.bigsis.1a", "home.talk.lilroom.mom.bigsis.1b"],
        ["home.talk.lilroom.mom.bigsis.2a", "home.talk.lilroom.mom.bigsis.2b"],
      ],
      lilsis: [
        { when: (g) => g.flag("home.sawDark") && !g.flag("home.flashTaken"), say: ["home.talk.lilroom.mom.lilsis.flash.a", "home.talk.lilroom.mom.lilsis.flash.b"] },
        { when: (g) => !!g.holder("batteries") && !g.flag("home.flashWorks"), say: ["home.talk.batt.mom.lilsis.a", "home.talk.batt.mom.lilsis.b"] },
        ["home.talk.lilroom.mom.lilsis.1a", "home.talk.lilroom.mom.lilsis.1b"],
        ["home.talk.lilroom.mom.lilsis.2a", "home.talk.lilroom.mom.lilsis.2b"],
      ],
    },
    bigsis: {
      mom: [["home.talk.lilroom.bigsis.mom.1a", "home.talk.lilroom.bigsis.mom.1b"], ["home.talk.lilroom.bigsis.mom.2a", "home.talk.lilroom.bigsis.mom.2b"]],
      lilsis: [["home.talk.lilroom.bigsis.lilsis.1a", "home.talk.lilroom.bigsis.lilsis.1b"], ["home.talk.lilroom.bigsis.lilsis.2a", "home.talk.lilroom.bigsis.lilsis.2b", "home.talk.lilroom.bigsis.lilsis.2c"]],
    },
    lilsis: {
      mom: [["home.talk.lilroom.lilsis.mom.1a", "home.talk.lilroom.lilsis.mom.1b"], ["home.talk.lilroom.lilsis.mom.2a", "home.talk.lilroom.lilsis.mom.2b"]],
      bigsis: [
        { when: (g) => g.flag("home.flashTaken") && !g.flag("home.flashWorks") && !g.holder("batteries"), say: ["home.talk.batt.lilsis.bigsis.a", "home.talk.batt.lilsis.bigsis.b"] },
        ["home.talk.lilroom.lilsis.bigsis.1a", "home.talk.lilroom.lilsis.bigsis.1b"],
        ["home.talk.lilroom.lilsis.bigsis.2a", "home.talk.lilroom.lilsis.bigsis.2b"],
      ],
    },
  },

  // The first time in: whose room it is, and whose it was.
  async enter(g) {
    if (g.flag("home.sawLilRoom") || !home(g) || !g.flag("home.arrived")) return;
    g.flag("home.sawLilRoom", true);
    await g.wait(300);
    await g.say("home.lilroom.first.1", "home.lilroom.first.2");
  },
};

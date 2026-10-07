// Act Two, the first of three scenes: the steps of the temple of Saturn, in the Forum.
// Rome, the morning of the Ides of March, 44 B.C. The Son plays.
//
// The door in time let him out inside the temple and shut behind him, and the doorkeeper has
// carried him out. The door is still in there. To get back to it he has to be what the
// doorkeeper lets in: a boy, in a clean tunic, carrying something for the god.
//
//   chain A   the washerwoman's errand (rome-street): bring the senator, down here, his clean toga.
//             She lends a tunic for it.
//   chain B   the snack-bar keeper's errand (rome-street): bring the soothsayer, on these steps, his
//             breakfast. His sacred chickens feed on the crumbs, the omen is good, and he trusts the
//             boy with the incense he cannot carry up fourteen steps himself.
//   the gate  in the tunic, with the incense, the doorkeeper lets him in (to rome-temple).
//
// Try it: index.html?scene=rome-steps&lead=son
// Later states: &flags=rome.arrived,rome.knowsRule,rome.hasToga,rome.hasBreakfast   (the things themselves are
// handed over by the people in rome-street, so start there to carry them).

const art = "art/scenes/rome-steps/";

/** Has this line been spoken yet? (The engine counts every line it says.) */
const heard = (g, id) => !!g.store.data.seenLines[id];
/** A thing worth looking at twice: the first line the first time, the second after that. */
const twice = (first, second) => (g) => g.say(heard(g, first) ? second : first);
/** Someone who can stand turns to the boy. */
const turnTo = (g, who) => { const a = g.actor(who), me = g.lead; if (a && me) a.look(me.x, me.y); };

// ---------- the doorkeeper, and the gate ----------

/** He says what he would let in. This is the puzzle stated: everything else in the act serves it.
    A boy who has run an errand or two before asking is scored on what he is carrying. */
async function explainRule(g) {
  turnTo(g, "doorkeeper");
  await g.say("rome.doorkeeper.hi.1", "rome.doorkeeper.hi.2", "rome.doorkeeper.hi.3", "rome.doorkeeper.rule.1", "rome.doorkeeper.rule.2");
  g.flag("rome.knowsRule", true);
  const tunic = g.has("tunic"), gift = g.has("incense");
  if (tunic && gift) return letIn(g);
  await g.say(tunic ? "rome.doorkeeper.need.gift.1" : gift ? "rome.doorkeeper.need.tunic.1" : "rome.doorkeeper.rule.3", "rome.doorkeeper.rule.4");
}

/** The gate of chains A and B. */
async function letIn(g) {
  turnTo(g, "doorkeeper");
  await g.say("rome.gate.1");
  await g.reach();                                                // the tunic goes on over everything (see the note in PUZZLES-rome.md)
  await g.say("rome.gate.2", "rome.gate.3", "rome.gate.4", "rome.gate.5", "rome.gate.6", "rome.gate.7", "rome.gate.8");
  g.flag("rome.inside", true);
  await g.goto("rome-temple");
}

/** Trying the doors, or showing the doorkeeper the tunic or the incense. */
async function atTheDoors(g) {
  if (g.flag("rome.inside")) {                                    // he has been let in once: after that he is known
    if (!heard(g, "rome.doorkeeper.again")) await g.say("rome.doorkeeper.again");
    return g.goto("rome-temple");
  }
  if (!g.flag("rome.knowsRule")) return explainRule(g);
  const tunic = g.has("tunic"), gift = g.has("incense");
  if (tunic && gift) return letIn(g);
  turnTo(g, "doorkeeper");
  if (tunic) return g.say("rome.doorkeeper.need.gift.1", "rome.doorkeeper.need.gift.2");
  if (gift) return g.say("rome.doorkeeper.need.tunic.1", "rome.doorkeeper.need.tunic.2");
  return g.say("rome.doorkeeper.need.both");
}

async function talkToDoorkeeper(g) {
  if (!g.flag("rome.knowsRule")) {
    await explainRule(g);                                         // the rule first; then whatever else there is to say
    if (g.flag("rome.inside")) return;                            // (he met it already, and was let in on the spot)
  } else if (!g.flag("rome.inside") && g.has("tunic") && g.has("incense")) return letIn(g);
  turnTo(g, "doorkeeper");
  for (;;) {
    const pick = await g.choose([
      { id: "rule", line: "rome.doorkeeper.ask.rule", when: (g) => !g.flag("rome.inside") },
      { id: "what", line: "rome.doorkeeper.ask.what" },
      { id: "dad", line: "rome.doorkeeper.ask.dad" },
      { id: "bye", line: "rome.doorkeeper.ask.bye" },
    ]);
    if (pick === "rule") await g.say("rome.doorkeeper.ask.rule", "rome.doorkeeper.ans.rule");
    else if (pick === "what") await g.say("rome.doorkeeper.ask.what", "rome.doorkeeper.ans.what.1", "rome.doorkeeper.ans.what.2");
    else if (pick === "dad") await g.say("rome.doorkeeper.ask.dad", "rome.doorkeeper.ans.dad.1", "rome.doorkeeper.ans.dad.2", "rome.doorkeeper.ans.dad.3", "rome.doorkeeper.ans.dad.4");
    else return g.say("rome.doorkeeper.ask.bye", "rome.doorkeeper.ans.bye");
  }
}

// ---------- chain B ends here: the soothsayer ----------

async function meetSoothsayer(g) {
  if (g.flag("rome.metSoothsayer")) return;
  await g.say("rome.soothsayer.hi.1", "rome.soothsayer.hi.2", "rome.soothsayer.hi.3", "rome.soothsayer.hi.4", "rome.soothsayer.hi.5");
  g.flag("rome.metSoothsayer", true);
}

/** His breakfast arrives. The crumbs go to the sacred chickens, they feed, and that is a good omen:
    now he will send his incense in to the god, by the boy. */
async function feedSoothsayer(g) {
  await meetSoothsayer(g);
  await g.say("rome.soothsayer.fed.1");
  await g.reach();
  g.take("breakfast");
  await g.say("rome.soothsayer.fed.2", "rome.soothsayer.fed.3", "rome.soothsayer.fed.4", "rome.soothsayer.fed.5");
  await g.reach();
  g.give("incense");
  g.flag("rome.hasIncense", true);
  await g.say("rome.soothsayer.fed.6");
}

async function talkToSoothsayer(g) {
  await meetSoothsayer(g);
  for (;;) {
    const fed = !!g.flag("rome.hasIncense");
    const pick = await g.choose([
      { id: "feed", line: "rome.soothsayer.fed.1", when: (g) => g.has("breakfast") },
      { id: "birds", line: "rome.soothsayer.ask.birds" },
      { id: "temple", line: "rome.soothsayer.ask.temple" },
      { id: "future", line: "rome.soothsayer.ask.future" },
      { id: "bye", line: "rome.soothsayer.ask.bye" },
    ]);
    if (pick === "feed") return feedSoothsayer(g);
    if (pick === "birds") {
      if (fed) await g.say("rome.soothsayer.ask.birds", "rome.soothsayer.ans.birds.fed");
      else await g.say("rome.soothsayer.ask.birds", "rome.soothsayer.ans.birds.1", "rome.soothsayer.ans.birds.2", "rome.soothsayer.ans.birds.3", "rome.soothsayer.ans.birds.4");
    } else if (pick === "temple") {
      if (fed) await g.say("rome.soothsayer.ask.temple", "rome.soothsayer.ans.temple.fed");
      else await g.say("rome.soothsayer.ask.temple", "rome.soothsayer.ans.temple.1", "rome.soothsayer.ans.temple.2", "rome.soothsayer.ans.temple.3", "rome.soothsayer.ans.temple.4");
    } else if (pick === "future") {
      await g.say("rome.soothsayer.ask.future", "rome.soothsayer.ans.future.1", "rome.soothsayer.ans.future.2", "rome.soothsayer.ans.future.3", "rome.soothsayer.ans.future.4");
    } else return g.say("rome.soothsayer.ask.bye", "rome.soothsayer.ans.bye");
  }
}

// ---------- chain A, the middle step: the senator ----------

async function meetSenator(g) {
  if (g.flag("rome.metSenator")) return;
  const senator = g.actor("senator");
  await g.moveTo(168, 508, "senator");                            // he is pacing: a few steps away,
  await g.moveTo(200, 540, "senator");                            //        and back to his mark
  if (senator) senator.face("E");
  await g.say("rome.senator.hi.1", "rome.senator.hi.2", "rome.senator.hi.3", "rome.senator.hi.4", "rome.senator.hi.5");
  g.flag("rome.metSenator", true);
}

/** The toga arrives, and the senator leaves for the Senate. (He is not on the steps again: see `actors`.) */
async function deliverToga(g) {
  await meetSenator(g);
  const senator = g.actor("senator");
  await g.say("rome.senator.toga.1");
  await g.reach();
  g.take("toga");
  await g.say("rome.senator.toga.2", "rome.senator.toga.3", "rome.senator.toga.4", "rome.senator.toga.5");
  g.flag("rome.delivered", true);
  await g.moveTo(-50, 468, "senator");                            // off the left edge of the picture, behind the laurel, the way the street goes
  if (senator) senator.fade(0);
  await g.say("rome.senator.toga.6");
}

async function talkToSenator(g) {
  await meetSenator(g);
  for (;;) {
    const pick = await g.choose([
      { id: "give", line: "rome.senator.toga.1", when: (g) => g.has("toga") },
      { id: "late", line: "rome.senator.ask.late" },
      { id: "toga", line: "rome.senator.ask.toga" },
      { id: "dad", line: "rome.senator.ask.dad" },
      { id: "bye", line: "rome.senator.ask.bye" },
    ]);
    if (pick === "give") return deliverToga(g);
    if (pick === "late") await g.say("rome.senator.ask.late", "rome.senator.ans.late.1", "rome.senator.ans.late.2", "rome.senator.ans.late.3", "rome.senator.ans.late.4");
    else if (pick === "toga") await g.say("rome.senator.ask.toga", "rome.senator.ans.toga.1", "rome.senator.ans.toga.2", "rome.senator.ans.toga.3", "rome.senator.ans.toga.4");
    else if (pick === "dad") await g.say("rome.senator.ask.dad", "rome.senator.ans.dad.1", "rome.senator.ans.dad.2");
    else return g.say("rome.senator.ask.bye", "rome.senator.ans.bye");
  }
}

export default {
  id: "rome-steps",
  era: "rome",
  name: "The steps of the temple of Saturn",

  // WHERE THINGS ARE. Every place in this file is the painter's own measurement of the finished picture
  // (art/scenes/rome-steps/layout.json), or was set by eye against the picture with the people standing in it.
  // The act's check script (check-rome.mjs) reads this file against that one; the few differences that are meant are listed there.
  // (The painter moved several things from where briefs/SCENES.md has them: the porch is at row 298, the doors at 468
  // to 538, the soothsayer sits on the fourth step, and the way to the street is off the left edge of the pavement.)

  // DEPTH. The pavement is ordinary ground. The steps are not: they climb the picture faster than the ground does.
  // minScale is the painter's: people hold the size they have at row 392 from there upward, instead of shrinking
  // away toward the horizon as they climb.
  horizon: 260, full: 590, minScale: 0.4,

  // The pavement, the whole flight of steps, and the narrow strip of porch behind the columns.
  walk: { area: [[0, 597], [797, 597], [797, 433], [797, 298], [763, 298], [648, 291], [342, 296], [396, 305], [382, 306], [461, 461], [400, 462], [340, 452], [240, 446], [120, 442], [0, 438]] },
  // Ground that things stand on. (A cut-out can block one patch of its own; the columns need six, so they are all here.)
  blocked: [
    [[238, 521], [346, 510], [327, 487], [229, 496]],             // the altar
    [[366, 498], [404, 495], [393, 485], [357, 489]],             // the tripod
    [[672, 563], [746, 553], [710, 535], [639, 544]],             // the boundary stone
    [[448, 422], [505, 419], [489, 403], [434, 406]],             // the soothsayer's cage
    // (The painter also blocks [[538,430],[581,427],[561,411],[520,413]], the ground under a folding stool. The stool and
    // the crooked staff beside it are being taken out of the picture, so that patch is left open.)
    [[0, 500], [150, 484], [158, 600], [0, 600]],                 // the statue base at the bottom left (the front plane)
    [[340, 306], [389, 306], [375, 303], [328, 304]],             // the feet of the six columns
    [[441, 305], [486, 304], [468, 301], [425, 302]],
    [[535, 303], [577, 302], [554, 300], [514, 301]],
    [[622, 301], [660, 301], [634, 298], [597, 299]],
    [[702, 300], [738, 299], [709, 297], [674, 298]],
    [[777, 298], [811, 298], [779, 296], [747, 297]],
    [[556, 293], [595, 293], [586, 292], [547, 292]],             // the doorkeeper's bench
  ],
  spawn: {
    default: [470, 508],                                          // the foot of the steps: where the doorkeeper put him down
    fromStreet: [52, 472],                                        // coming in from the street, at the left edge, behind the laurel (see `enter`)
    fromTemple: [517, 295],                                       // coming out of the doors (the same place as the doors' walkTo, below)
  },
  exits: ["rome-street", "rome-temple"],

  picture: art + "back.png",
  planes: [
    { id: "columns", src: art + "columns.png", base: [[320, 305.3], [800, 296.8]] },   // the six columns of the front: people on the porch pass behind them
    { id: "altar", src: art + "altar.png", base: [[244, 518], [338, 509]] },
    { id: "tripod", src: art + "tripod.png", base: 495 },
    { id: "stone", src: art + "stone.png", base: [[673, 558], [730, 550]] },
    { id: "front", src: art + "front.png", plane: "front" },      // the statue base and laurel at the bottom left corner
  ],

  actors: [
    // He is seen between the second and third columns, beside the doorway. The porch is a strip fourteen rows deep and the
    // columns' feet take most of it, so he blocks no ground: the one gap wide enough to come up through is where he stands.
    { id: "doorkeeper", kind: "doorkeeper", at: [492, 295], face: "S", solid: false },
    // He sits on the fourth step, beside his cage, with his feet on the third. The painter's mark (494, 404) is his seat;
    // a seated figure's place is the ground under its hips, which is one step (ten rows) straight down from the seat.
    { id: "soothsayer", kind: "soothsayer", at: [505, 414], face: "S" },
    // He paces, and in the end he walks away, so he blocks no ground. Once his toga has come he is gone.
    { id: "senator", kind: "senator", at: [200, 540], face: "E", solid: false, when: (g) => !g.flag("rome.delivered") },
  ],

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "forum", name: "Forum", rect: [0, 120, 236, 200], walkTo: [140, 470], face: "N", look: twice("rome.forum.look", "rome.forum.look2") },
    // The temple itself, traced from the picture: the side wall, the six columns and everything above them.
    { id: "temple", name: "temple", verb: "Climb", poly: [[240, 96], [345, 0], [800, 0], [800, 292], [326, 292], [244, 286]], look: "rome.temple.look", use: "rome.temple.use" },
    { id: "stairs", name: "temple steps", poly: [[700, 306], [797, 306], [797, 430], [700, 440]], look: "rome.stairs.look" },      // the far right of the flight: the rest is for walking on
    // Two things the painter put in the shade of the temple's base, which are not in the painter's list: traced from the picture.
    { id: "cart", name: "handcart", rect: [146, 312, 124, 62], walkTo: [196, 454], face: "N", look: "rome.cart.look" },            // the cart, its sealed sacks, and the low door of the vault they have come for
    {
      id: "dog", name: "sleeping dog", verb: "Call", rect: [204, 374, 56, 22], walkTo: [232, 456], face: "N",
      look: "rome.dog.look", use: "rome.dog.use", useWith: { breakfast: "rome.dog.breakfast" },
    },
    {
      // The painter's place to stand is 517, 296. One row up from it is clear of the margin the engine keeps round the third column's foot.
      id: "doors", name: "temple doors", verb: "Go through", rect: [468, 129, 70, 163], walkTo: [517, 295], face: "N",
      look: (g) => g.say(g.flag("rome.inside") ? "rome.doors.look2" : "rome.doors.look"),
      use: atTheDoors, useWith: { tunic: atTheDoors, incense: atTheDoors },
    },
    { id: "notices", name: "notice board", rect: [338, 322, 34, 52], walkTo: [425, 472], face: "N", look: "rome.board.look" },
    {
      id: "altar", name: "altar", verb: "Touch", rect: [237, 416, 102, 93], walkTo: [309, 529], face: "N",
      look: "rome.altar.look", use: "rome.altar.use", useWith: { incense: "rome.altar.incense" },
    },
    { id: "tripod", name: "bronze tripod", rect: [361, 403, 40, 89], walkTo: [431, 494], face: "W", look: "rome.tripod.look" },
    // (The painter's place to stand for the stone is 624, 568, where the inventory bar would hide his feet: he stands a little higher.)
    { id: "stone", name: "carved stone", rect: [672, 475, 62, 74], walkTo: [618, 540], face: "E", look: "rome.stone.look" },
    { id: "pigeons", name: "pigeons", verb: "Chase", rect: [536, 488, 120, 68], look: "rome.pigeons.look", use: "rome.pigeons.use" },   // the five on the pavement by the puddle
    {
      // The cage and its dish of grain. (The painter's shape, [438, 375, 131, 41], takes in the stool and staff that are leaving the picture.)
      id: "birdcage", name: "sacred chickens", verb: "Call", rect: [438, 375, 56, 34], walkTo: [524, 462], face: "NW",
      look: (g) => (g.flag("rome.hasIncense") ? g.say("rome.birdcage.fed") : twice("rome.birdcage.look", "rome.birdcage.look2")(g)),
      use: (g) => g.say(g.flag("rome.hasIncense") ? "rome.birdcage.fed" : "rome.birdcage.use"),
      useWith: { breakfast: "rome.birdcage.breakfast" },
    },
    {
      // His figure, with the staff in his hand. He is talked to from beside him, two steps down, so that the boy does not
      // stand in front of the old man.
      id: "soothsayer", name: "soothsayer", verb: "Talk to", rect: [483, 346, 44, 76], walkTo: [540, 442], face: "W",
      look: twice("rome.soothsayer.look", "rome.soothsayer.look2"), use: talkToSoothsayer,
      useWith: {
        breakfast: feedSoothsayer,
        toga: "rome.soothsayer.toga",
        coin: ["rome.soothsayer.coin.1", "rome.soothsayer.coin.2", "rome.soothsayer.coin.3"],
        quarter: "rome.soothsayer.quarter", incense: "rome.soothsayer.incense",
      },
    },
    {
      id: "senator", name: "senator", verb: "Talk to", rect: [176, 400, 50, 142], walkTo: [264, 540], face: "W",
      when: (g) => !g.flag("rome.delivered"),
      look: twice("rome.senator.look", "rome.senator.look2"), use: talkToSenator,
      useWith: { toga: deliverToga, breakfast: "rome.senator.breakfast", incense: "rome.senator.incense" },
    },
    {
      // He is small up there (68 pixels), so his area is a good deal bigger than he is: easy to click, and it still leaves
      // the top of the doorway and its right-hand side for the doors.
      id: "doorkeeper", name: "doorkeeper", verb: "Talk to", rect: [462, 212, 56, 90], walkTo: [517, 295], face: "W",
      look: twice("rome.doorkeeper.look", "rome.doorkeeper.look2"), use: talkToDoorkeeper,
      useWith: {
        tunic: atTheDoors, incense: atTheDoors,
        toga: "rome.doorkeeper.toga",
        breakfast: ["rome.doorkeeper.breakfast.1", "rome.doorkeeper.breakfast.2", "rome.doorkeeper.breakfast.3"],
        coin: "rome.doorkeeper.coin", quarter: "rome.doorkeeper.quarter", phone: "rome.doorkeeper.phone",
      },
    },
    {
      // The painter's way out is the left edge of the pavement, 40 pixels wide, behind the laurel. It is a little wider here, to be easier to find.
      id: "to-street", name: "the street", verb: "Walk to", poly: [[0, 436], [64, 439], [64, 500], [0, 500]], walkTo: [34, 470],
      look: "rome.tostreet.look", use: (g) => g.goto("rome-street", { spawn: "fromForum" }),
    },
  ],

  // Runs when the lead arrives. It must be safe to run twice, so it checks its own fact.
  async enter(g, from) {
    if (from === "rome-street") await g.walkTo(160, 474);         // out from behind the laurel at the left edge, onto the open pavement
    if (g.flag("rome.arrived")) return;
    const me = g.lead, doorkeeper = g.actor("doorkeeper");
    await g.wait(400);
    if (me) me.face("N");
    if (doorkeeper && me) doorkeeper.look(me.x, me.y);
    await g.say("rome.arrive.out");
    if (me) me.face("S");                                         // he turns and sees where he is
    await g.say("rome.arrive.1", "rome.arrive.2");
    if (me) me.face("N");                                         // and back to the temple: the door is in there
    await g.say("rome.arrive.4", "rome.arrive.5", "rome.arrive.3", "rome.arrive.6");
    if (me) me.face("W");                                         // the street is off the left edge, behind the laurel: his nose says so
    await g.say("rome.arrive.7");
    for (const thing of ["phone", "quarter", "gum"]) g.store.give(thing);   // what was in his pockets all along (no "You have..." for these)
    g.flag("rome.arrived", true);
    g.team(["son"]);                                              // he plays this act alone: Dad is still in Egypt, at his door
  },
};

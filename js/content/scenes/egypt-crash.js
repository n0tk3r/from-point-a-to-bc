// Act One, the first of four scenes: where the wagon came down, on the bank of the Nile.
// Egypt, about 1920 B.C. (the Bible's own count of years: briefs/DATING.md). Dad plays.
//
// The wagon is nose-down in the sand with the holiday luggage still tied to its roof, and his son's
// sneaker prints go up the track to the pyramid. Nearly everything Dad will need is in or on the car:
//
//   the road map (glovebox)        any time    the scribe writes his pass on the back of it       chain A
//   a reed (the reed bed)          any time    the scribe's new pen                                chain A
//   the flashlight (trunk)         any time    shows him that light opens the door                 chain B
//   a root beer (cooler)           any time    the guard's price for holding the shade             chain C
//   the sunglasses (suitcase)      any time    traded to the goldsmith for his copper mirror       chain C
//   the windshield shade (trunk)   only once he knows the door wants light ("egypt.knowsLight")    chain C
//   the door mirror (the wagon)    only then, too                                                  chain C
//
// Under the shirts in the suitcase, with the sunglasses: General Feathers, his youngest's stuffed hen, sent along
// "to keep an eye on Daddy", and her note in crayon (shown close up). No puzzle needs her. He carries her
// (`chicken`), talks to her, and shows her to people; nobody in this Egypt has ever seen a chicken.
//
// The water carrier is the first person he meets. He saw the boy go up the track, and he knows the news
// from the building site: a wall is humming, the scribe's pen has split, and the geese stand facing the pyramid.
//
// Dad is a Christian father, and this is the Egypt of his Bible. When he understands that the boy is gone, he prays
// (the first of his three prayers in the act). At the reeds he looks for a basket; at the river he wonders which of
// Abraham, Joseph and Moses he has missed and which are still to come; the pyramids get one more thought. Once the
// scribe up at the site has told him the palace gossip ("egypt.heardAbram"), he knows: Abram is in Egypt this week,
// and Joseph and Moses are still to come. What he says at the river and the reeds after that says so.
// (None of this is part of a puzzle.)
//
// Try it: index.html?scene=egypt-crash&lead=dad
// Later states: &flags=egypt.arrived,egypt.knowsLight   (the shade and the mirror can then be taken)
//               &flags=egypt.arrived,egypt.heardAbram   (he has heard the news of Abram)

const art = "art/scenes/egypt-crash/";

/** How many times a line has been spoken. (The engine counts every line it says.) */
const count = (g, id) => g.store.data.seenLines[id] || 0;
/** A thing worth looking at twice: the first line, then the second, turn about. */
const twice = (first, second) => (g) => g.say(count(g, first) <= count(g, second) ? first : second);
/** Of several lines, the one heard least: a thing with more than two things to say about it says them in turn. */
const turns = (...ids) => (g) => g.say(ids.reduce((best, id) => (count(g, id) < count(g, best) ? id : best)));
/** Someone who can stand turns to Dad. */
const turnTo = (g, who) => { const a = g.actor(who), me = g.lead; if (a && me) a.look(me.x, me.y); };
/** Head bowed, hands folded (true), or let it go (false). A figure that has no such pose simply stands. */
const pray = (a, on) => a && a.pray && a.pray(on);

// ---------- the river ----------
/** The river has the old joke, and the end of the joke: it is the Nile. And once, straight after that, what the
    Nile is to a man who knows his Bible. Before the scribe's news he wonders who he has missed and who is still to
    come, and does not settle it. After it he knows, and says so, once (even if he wondered before). */
async function lookAtRiver(g) {
  const second = count(g, "egypt.river.look") > count(g, "egypt.river.look2");
  await g.say(second ? "egypt.river.look2" : "egypt.river.look");
  if (!second) return;
  if (g.flag("egypt.heardAbram")) { if (!count(g, "egypt.river.after.1")) await g.say("egypt.river.after.1", "egypt.river.after.2", "egypt.river.after.3"); }
  else if (!count(g, "egypt.river.bible.1")) await g.say("egypt.river.bible.1", "egypt.river.bible.2", "egypt.river.bible.3", "egypt.river.bible.4");
}

// ---------- General Feathers ----------
// Little Sister's note, as the close-up shows it: crayon on a sheet torn from a pad (the kit draws the paper: js/art/kit.js, `paper`).
const NOTE = {
  tape: false, tilt: -2.5, tint: "#fbf6e6", width: 500,
  lines: [
    { text: "DADDY.", size: 46, gap: 18, anchor: "start", fill: "#c8402f", turn: -3 },
    { text: "GENERAL FEATHERS", size: 40, fill: "#5b3fa0", turn: 2 },
    { text: "IS IN CHARGE.", size: 40, gap: 22, fill: "#5b3fa0", turn: -1.5 },
    { text: "DO WHAT SHE SAYS.", size: 40, fill: "#c8402f", turn: 1.5 },
  ],
};

/** Showing her to somebody: he introduces her, and they answer, once each, in their own way. After that (and for
    anybody with no answer of their own) Dad's stock reply. `answer` is their line, and Dad's comeback if he has one. */
const showGeneral = (who, ...answer) => async (g) => {
  turnTo(g, who);
  if (count(g, answer[0])) return g.say("egypt.chicken.stock");
  await g.say("egypt.chicken.show", ...answer);
};

// ---------- the water carrier ----------
async function talkToCarrier(g) {
  turnTo(g, "carrier");
  if (!g.flag("egypt.metCarrier")) {
    await g.say("egypt.carrier.hello", "egypt.scribe.hello2", "egypt.carrier.hello2");
    g.flag("egypt.metCarrier", true);
  }
  for (;;) {
    const pick = await g.choose([
      { id: "boy", line: "egypt.ask.boy" },
      { id: "horizon", line: "egypt.carrier.ask.horizon", when: (g) => count(g, "egypt.carrier.boy.2") > 0 },     // he has to have heard the word first
      { id: "news", line: "egypt.carrier.ask.news" },
      { id: "donkey", line: "egypt.carrier.ask.donkey", when: (g) => !g.flag("egypt.knowsDonkey") },
      { id: "camels", line: "egypt.carrier.ask.camels", when: (g) => !!g.flag("egypt.knowsDonkey") },
      { id: "bye", line: "egypt.carrier.ask.bye" },
    ]);
    if (pick === "boy") await g.say("egypt.ask.boy", "egypt.carrier.boy.1", "egypt.carrier.boy.2", "egypt.carrier.boy.3");
    else if (pick === "horizon") await g.say("egypt.carrier.ask.horizon", "egypt.carrier.horizon.1", "egypt.carrier.horizon.2");
    else if (pick === "news") await g.say("egypt.carrier.ask.news", "egypt.carrier.news.1", "egypt.carrier.news.2", "egypt.carrier.news.3", "egypt.carrier.news.4");
    else if (pick === "donkey") { await g.say("egypt.carrier.ask.donkey", "egypt.carrier.donkey.1", "egypt.carrier.donkey.2"); g.flag("egypt.knowsDonkey", true); }
    else if (pick === "camels") await g.say("egypt.carrier.ask.camels", "egypt.carrier.camels.1", "egypt.carrier.camels.2", "egypt.carrier.camels.3");
    else return g.say("egypt.carrier.ask.bye", "egypt.carrier.bye");
  }
}

// ---------- chain A: a reed, and the map ----------
async function cutReed(g) {
  if (g.flag("egypt.hasReed")) return g.say("egypt.reeds.again");
  await g.reach();
  await g.say("egypt.reeds.take");
  g.give("reed");
  g.flag("egypt.hasReed", true);
  await g.reach(true);                    // and while he is in there, he parts the reeds and has a look (Exodus 2:3)
  await g.say("egypt.reeds.basket.1", g.flag("egypt.heardAbram") ? "egypt.reeds.basket.3" : "egypt.reeds.basket.2");     // (once he has the news, he knows Moses is still to come)
}

async function searchGlovebox(g) {
  if (g.flag("egypt.hasMap")) return g.say("egypt.wagon.empty");
  await g.reach();
  await g.say("egypt.wagon.use");
  g.give("map");
  g.flag("egypt.hasMap", true);
}

// ---------- the luggage on the roof. A lid, once opened, stays open: the painted cut-out follows the fact. ----------
/** Dad reaches up and, if the lid is still shut, throws it back. */
async function openLid(g, fact) {
  await g.reach();
  if (g.flag(fact)) return;
  g.flag(fact, true);
  await g.wait(250);
}

/** The trunk: the flashlight at any time; the windshield shade only when he has a use for it. */
async function searchTrunk(g) {
  await openLid(g, "egypt.trunkOpen");
  if (!g.flag("egypt.tookFlashlight")) {
    await g.say("egypt.trunk.flashlight");
    g.give("flashlight");
    g.flag("egypt.tookFlashlight", true);
    return;
  }
  if (g.flag("egypt.tookShade")) return g.say("egypt.trunk.after");
  if (!g.flag("egypt.knowsLight")) return g.say("egypt.trunk.rest", "egypt.car.noreason");
  await g.say("egypt.trunk.shade");
  g.give("shade");
  g.flag("egypt.tookShade", true);
}

/** The cooler: one root beer at a time, and there is always another. */
async function searchCooler(g) {
  await openLid(g, "egypt.coolerOpen");
  if (g.has("rootbeer")) return g.say("egypt.cooler.have");
  await g.say(g.flag("egypt.tookRootbeer") ? "egypt.cooler.more" : "egypt.cooler.take");
  g.give("rootbeer");
  g.flag("egypt.tookRootbeer", true);
}

/** The suitcase: the sunglasses on top, six shirts that stay where they are, and under the shirts General Feathers
    with her orders. Everybody opens the suitcase (the sunglasses are needed), so nobody misses her. */
async function searchSuitcase(g) {
  await openLid(g, "egypt.suitcaseOpen");
  if (g.flag("egypt.tookSunglasses") && g.flag("egypt.tookGeneral")) return g.say("egypt.suitcase.again");
  if (!g.flag("egypt.tookSunglasses")) {
    g.give("sunglasses");                 // (handed over first, so that its notice has gone by the time the note is up)
    g.flag("egypt.tookSunglasses", true);
    await g.say("egypt.suitcase.take");
  }
  await g.reach(true);                    // down under the shirts
  g.closeup(g.art.paper(NOTE), "Little Sister's note, in crayon: DADDY. GENERAL FEATHERS IS IN CHARGE. DO WHAT SHE SAYS.", { grid: [800, 600] });
  await g.say("egypt.suitcase.general.1", "egypt.suitcase.general.2");
  g.closeup();
  g.give("chicken");
  g.flag("egypt.tookGeneral", true);
  await g.say("egypt.suitcase.general.3");
}

/** The door mirror comes off only when he knows what a mirror is for. */
async function takeMirror(g) {
  if (!g.flag("egypt.knowsLight")) return g.say("egypt.car.noreason");
  await g.reach();
  g.flag("egypt.tookMirror", true);       // the mirror leaves the door (its cut-out and its clickable area follow the fact)
  await g.say("egypt.mirror.take");
  g.give("carmirror");
}

/** A piece of luggage is two clickable shapes, because an open lid stands taller than a shut one. One shows at a time. */
const lidded = (spot, fact, shut, open) => [
  { ...spot, poly: shut, when: (g) => !g.flag(fact) },
  { ...spot, poly: open, verb: "Search", when: (g) => !!g.flag(fact) },
];

export default {
  id: "egypt-crash",
  era: "egypt",
  name: "Where the wagon came down",

  // Every number below is a pixel of the painting, measured by the painter (art/scenes/egypt-crash/layout.json).
  // DEPTH: minScale stops anyone shrinking to a dot at the far end of the track.
  horizon: 262, full: 590, minScale: 0.2,

  // The sand: the left edge keeps to the bank, clear of the water; the far edge runs under the village and the dunes,
  // with a tongue up the track. Two rocks by the front edge are in the way; so are the palms, the donkey and the wagon (below).
  walk: { area: [[484, 308], [504, 308], [518, 322], [560, 340], [640, 352], [800, 360], [800, 596], [12, 596], [12, 556], [27, 541], [91, 503], [157, 451], [221, 395], [269, 347], [284, 334], [330, 326], [440, 326], [474, 318]] },
  blocked: [
    [[67, 546], [76, 536], [94, 536], [104, 546], [101, 551], [68, 551]],
    [[284, 582], [293, 573], [310, 573], [318, 582], [316, 587], [286, 587]],
  ],
  spawn: {
    default: [420, 570],            // where he climbs out
    fromSite: [500, 372],           // coming down the track (its far end is a long walk off, and he is a dot there)
  },
  exits: ["egypt-site"],

  picture: art + "back.png",

  // Each palm is its own cut-out, so that somebody standing between two of them is behind one and in front of the other.
  // The wagon's mirror and its three open lids are cut-outs laid over the wagon, pixel for pixel. Their base lines sit a
  // hair in front of the wagon's and of each other's, in the painter's order: suitcase, then trunk, then cooler.
  planes: [
    { id: "palm-3", src: art + "palm-3.png", base: 318, solid: [[292, 313], [308, 313], [309, 320], [291, 320]] },
    { id: "palm-2", src: art + "palm-2.png", base: 352, solid: [[241, 344], [263, 344], [265, 354], [239, 354]] },
    { id: "palm-1", src: art + "palm-1.png", base: 400, solid: [[174, 389], [206, 389], [209, 402], [171, 402]] },
    { id: "donkey", src: art + "donkey.png", base: 447, solid: [[296, 438], [357, 438], [384, 444], [384, 457], [357, 453], [296, 453]] },
    { id: "wagon", src: art + "wagon.png", base: [[490, 541], [790, 537]],
      solid: [[372, 549], [394, 530], [424, 514], [456, 502], [490, 499], [522, 506], [552, 512], [757, 516], [797, 536], [793, 549], [640, 553], [550, 558], [450, 558]] },   // the car, and the sand heaped at its nose
    { id: "mirror", src: art + "mirror.png", base: [[490, 541.2], [790, 537.2]], when: (g) => !g.flag("egypt.tookMirror") },
    { id: "suitcase", src: art + "suitcase-open.png", base: [[490, 541.4], [790, 537.4]], when: (g) => !!g.flag("egypt.suitcaseOpen") },
    { id: "trunk", src: art + "trunk-open.png", base: [[490, 541.6], [790, 537.6]], when: (g) => !!g.flag("egypt.trunkOpen") },
    { id: "cooler", src: art + "cooler-open.png", base: [[490, 541.8], [790, 537.8]], when: (g) => !!g.flag("egypt.coolerOpen") },
    { id: "steam", frames: [art + "steam-0.png", art + "steam-1.png", art + "steam-2.png", art + "steam-3.png"], fps: 6, at: [472, 498], foot: [30, 104], base: [[490, 542], [790, 538]] },
    { id: "papyrus", src: art + "front.png", plane: "front" },
  ],

  actors: [
    { id: "carrier", kind: "carrier", at: [260, 451], face: "SE" },       // at his donkey's head
  ],

  // The far things first: an area lower in this list lies over the ones above it.
  hotspots: [
    { id: "pyramid", name: "pyramids", poly: [[566, 76], [430, 250], [604, 262], [800, 258], [800, 204], [716, 204], [690, 232]], look: turns("egypt.pyramids.look", "egypt.pyramids.look2", "egypt.pyramids.look3") },
    {
      id: "river", name: "river", verb: "Wade into", poly: [[0, 266], [340, 266], [318, 276], [292, 300], [258, 336], [210, 384], [146, 440], [80, 492], [16, 530], [0, 540]], walkTo: [184, 446], face: "W",
      look: lookAtRiver, use: "egypt.river.use",
    },
    { id: "boat", name: "boat", rect: [84, 280, 98, 48], look: twice("egypt.boat.look", "egypt.boat.look2") },
    { id: "palms", name: "palm trees", poly: [[150, 0], [300, 0], [356, 150], [330, 212], [258, 232], [150, 190], [112, 90]], look: "egypt.palms.look" },
    { id: "reeds", name: "reeds", verb: "Pick", rect: [212, 334, 30, 42], walkTo: [229, 400], face: "W", look: "egypt.reeds.look", use: cutReed },
    { id: "block", name: "dropped block", verb: "Push", rect: [698, 326, 66, 36], walkTo: [716, 374], face: "N", look: "egypt.block.look", use: "egypt.block.use" },
    {
      id: "footprints", name: "sneaker prints", verb: "Follow", poly: [[474, 490], [492, 490], [504, 460], [508, 420], [506, 380], [500, 340], [496, 318], [480, 318], [480, 350], [486, 390], [486, 430], [478, 462]], walkTo: [424, 502], face: "NE",       // (a step clear of the steam)
      look: "egypt.footprints.look", use: "egypt.footprints.use",
      useWith: { chicken: "egypt.chicken.footprints" },
    },
    {
      id: "track", name: "track to the pyramid", verb: "Walk up", poly: [[476, 300], [508, 298], [516, 326], [472, 330]], walkTo: [500, 372], face: "N",       // he is on his way up it when the picture changes
      look: "egypt.track.look", use: (g) => g.goto("egypt-site", { spawn: "fromCrash" }),
    },
    {
      id: "donkey", name: "donkey", verb: "Pat", poly: [[290, 368], [298, 367], [340, 383], [377, 424], [380, 442], [368, 451], [305, 446], [302, 444], [275, 406]], walkTo: [320, 467], face: "N",
      look: (g) => g.say(g.flag("egypt.knowsDonkey") ? "egypt.donkey.look2" : "egypt.donkey.look"), use: "egypt.donkey.use",
      useWith: { sunglasses: "egypt.donkey.sunglasses" },
    },
    {
      id: "carrier", name: "water carrier", verb: "Talk to", rect: [244, 362, 32, 92], walkTo: [228, 486], face: "NE",
      look: "egypt.carrier.look", use: talkToCarrier,
      useWith: { rootbeer: ["egypt.carrier.rootbeer.1", "egypt.carrier.rootbeer.2"], map: ["egypt.carrier.map.1", "egypt.carrier.map.2", "egypt.carrier.map.3"], chicken: showGeneral("carrier", "egypt.carrier.chicken") },
    },
    {
      id: "wagon", name: "wagon", verb: "Start", walkTo: [604, 563], face: "N", look: "egypt.wagon.look", use: "egypt.wagon.try",
      poly: [[460, 490], [552, 474], [577, 441], [592, 432], [728, 416], [760, 434], [760, 443], [776, 471], [786, 502], [783, 512], [744, 543], [700, 543], [640, 548], [618, 540], [598, 526], [574, 516], [546, 513], [520, 507], [490, 500]],
    },
    {
      id: "hood", name: "hood", verb: "Open", poly: [[460, 490], [552, 474], [588, 495], [574, 516], [546, 513], [520, 507], [490, 500]], walkTo: [566, 563], face: "N",
      look: twice("egypt.hood.look", "egypt.hood.look2"), use: "egypt.hood.use",
      useWith: { flashlight: (g) => g.say(g.flag("egypt.knowsLight") ? "egypt.flash.dead" : "egypt.hood.flashlight"), rootbeer: "egypt.hood.rootbeer" },
    },
    {
      id: "glovebox", name: "glovebox", verb: "Search", poly: [[621, 488], [627, 463], [656, 458], [659, 483]], walkTo: [642, 563], face: "N",       // through the driver's window
      look: (g) => g.say(g.flag("egypt.hasMap") ? "egypt.wagon.empty" : "egypt.glovebox.look"), use: searchGlovebox,
    },
    ...lidded({ id: "suitcase", name: "suitcase", verb: "Open", walkTo: [648, 563], face: "N", look: (g) => g.say(g.flag("egypt.suitcaseOpen") ? "egypt.suitcase.open" : "egypt.suitcase.look"), use: searchSuitcase },
      "egypt.suitcaseOpen", [[600, 434], [599, 419], [648, 413], [651, 426], [671, 438], [671, 440], [621, 446]], [[586, 381], [639, 375], [670, 424], [672, 441], [656, 451], [620, 447], [600, 434]]),
    ...lidded({ id: "trunk", name: "trunk", verb: "Open", walkTo: [692, 563], face: "N", look: (g) => (g.flag("egypt.trunkOpen") ? twice("egypt.trunk.cables", "egypt.trunk.chair")(g) : g.say("egypt.trunk.look")), use: searchTrunk },
      "egypt.trunkOpen", [[651, 426], [647, 395], [693, 389], [709, 399], [701, 400], [706, 422], [723, 433], [724, 436], [678, 442]], [[632, 348], [678, 342], [683, 344], [721, 406], [724, 437], [677, 442], [650, 425], [643, 404]]),
    ...lidded({ id: "cooler", name: "cooler", verb: "Open", walkTo: [730, 563], face: "N", look: "egypt.cooler.look", use: searchCooler },
      "egypt.coolerOpen", [[701, 400], [730, 396], [748, 407], [749, 429], [723, 433], [706, 422]], [[701, 399], [720, 388], [732, 390], [750, 401], [761, 428], [744, 436], [721, 433], [705, 423]]),
    {
      id: "mirror", name: "door mirror", verb: "Take", rect: [617, 479, 20, 15], walkTo: [622, 563], face: "N", when: (g) => !g.flag("egypt.tookMirror"),
      look: "egypt.mirror.look", use: takeMirror,
    },
  ],

  // Runs when the lead arrives. It must be safe to run twice (a save can be loaded in the middle of it), so it checks its own fact.
  async enter(g) {
    if (g.flag("egypt.arrived")) return;
    await g.wait(500);
    await g.say("egypt.arrive.1", "egypt.arrive.2", "egypt.arrive.3");
    await g.walkTo(424, 502);                                     // to where the prints begin
    g.lead.look(492, 316);                                        // up the track
    await g.say("egypt.arrive.4", "egypt.arrive.5");
    g.lead.face("SE");                                            // he turns from the track, and bows his head where he stands
    await g.wait(300);
    pray(g.lead, true);
    await g.wait(400);
    await g.say("egypt.arrive.pray.1", "egypt.arrive.pray.2");
    pray(g.lead, false);
    await g.wait(350);                                            // (his hands are his own again before the player has him)
    g.flag("egypt.arrived", true);
  },
};

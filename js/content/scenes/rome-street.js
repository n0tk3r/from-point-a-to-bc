// Act Two, the second of three scenes: the shopping street that leads to the Forum.
// Rome, the morning of the Ides of March, 44 B.C. The Son plays.
//
// Everything he needs to get back into the temple starts here, with three people who each
// have a use for a boy with legs:
//
//   chain A   the washerwoman hands him the senator's clean toga to run up to the Forum, and
//             lends him a small tunic when he has done it (the tunic comes off the low line).
//   chain B   the snack-bar keeper feeds him, and hands him the soothsayer's breakfast to take up.
//   chain C   the fountain: one new silver coin, borrowed. Inside the temple it is his mirror.
//
// The street boy is the act's hint-giver: ask him what to do and his answer follows the story.
//
// And one person who is part of no chain: the date seller, a Jew from Judea, at the kerb of the right-hand
// pavement, by the last stepping stone. With him, and in three other places here, the family's faith and the
// Bible's history come into the act (briefs/WEAVE.md): the first time the boy walks into this street he works out
// that it is B.C., "before Christ"; at the fountain he knows the coin; a second look at the stepping stones is a
// look at the road. None of it gives, takes or opens anything. (And one line of the act's thread of chickens,
// briefs/DATING.md: shown the soothsayer's breakfast, the date seller declines, as every day, to have his fortune
// told by the soothsayer's hens.)
//
// Try it: index.html?scene=rome-street&lead=son&flags=rome.arrived
// Later states: add rome.knowsRule, rome.hasToga, rome.delivered, rome.hasBreakfast, rome.inside ... to &flags=

const art = "art/scenes/rome-street/";

/** Has this line been spoken yet? (The engine counts every line it says.) */
const heard = (g, id) => !!g.store.data.seenLines[id];
/** A thing worth looking at twice: the first line the first time, the second after that. */
const twice = (first, second) => (g) => g.say(heard(g, first) ? second : first);
/** Someone who can stand turns to the boy. */
const turnTo = (g, who) => { const a = g.actor(who), me = g.lead; if (a && me) a.look(me.x, me.y); };
/** Two poses from the people's rig, asked for through a guard, so that a figure without them simply stands. */
const hold = (a, on) => a && a.hold && a.hold(on);                // a hand kept held out
const pray = (a, on) => a && a.pray && a.pray(on);                // head bowed, hands folded

/** His sneakers light up when he stomps: a blink of red on the paving under his feet. */
async function stomp(g) {
  const glow = g.q("#stomp"), me = g.lead;
  g.sfx("plug");
  if (!glow || !me) return g.wait(300);
  glow.setAttribute("cx", me.x);
  glow.setAttribute("cy", me.y);
  for (let n = 0; n < (g.calm ? 1 : 2); n++) {                    // one soft glow for players who asked for less motion
    await g.tween(g.calm ? 300 : 110, (k) => glow.setAttribute("opacity", k));
    await g.tween(g.calm ? 500 : 190, (k) => glow.setAttribute("opacity", 1 - k));
  }
}

// ---------- chain B starts here: the snack bar ----------

/** The first visit: the keeper feeds him (step one of Operation Find Dad), and gives him the errand. */
async function firstHelping(g) {
  turnTo(g, "keeper");
  await g.say("rome.keeper.hi.1");
  await g.reach();
  await g.say("rome.keeper.hi.2", "rome.keeper.hi.3", "rome.keeper.hi.4", "rome.keeper.hi.5", "rome.keeper.hi.6",
    "rome.keeper.errand.1", "rome.keeper.errand.2", "rome.keeper.errand.3");
  await g.reach();
  g.give("breakfast");
  g.flag("rome.hasBreakfast", true);
  await g.say("rome.keeper.errand.4");
}

const payWithQuarter = ["rome.keeper.ask.pay", "rome.keeper.ans.pay.1", "rome.keeper.ans.pay.2", "rome.keeper.ans.pay.3", "rome.keeper.ans.pay.4"];

async function talkToKeeper(g) {
  if (!g.flag("rome.hasBreakfast")) await firstHelping(g);       // the errand first; then whatever else there is to say
  turnTo(g, "keeper");
  for (;;) {
    const pick = await g.choose([
      { id: "pay", line: "rome.keeper.ask.pay", when: (g) => g.has("quarter") },
      { id: "pizza", line: "rome.keeper.ask.pizza" },
      { id: "owe", line: "rome.keeper.ask.owe" },
      { id: "dad", line: "rome.keeper.ask.dad" },
      { id: "bye", line: "rome.keeper.ask.bye" },
    ]);
    if (pick === "pay") await g.say(...payWithQuarter);
    else if (pick === "pizza") await g.say("rome.keeper.ask.pizza", "rome.keeper.ans.pizza.1", "rome.keeper.ans.pizza.2", "rome.keeper.ans.pizza.3", "rome.keeper.ans.pizza.4", "rome.keeper.ans.pizza.5");
    else if (pick === "owe") await g.say("rome.keeper.ask.owe", "rome.keeper.ans.owe.1", "rome.keeper.ans.owe.2", "rome.keeper.ans.owe.3");
    else if (pick === "dad") await g.say("rome.keeper.ask.dad", "rome.keeper.ans.dad.1", "rome.keeper.ans.dad.2");
    else return g.say("rome.keeper.ask.bye", "rome.keeper.ans.bye");
  }
}

// ---------- chain A starts and ends here: the laundry ----------

/** The first visit: she sizes him up, and gives him the errand. */
async function firstWash(g) {
  turnTo(g, "washer");
  await g.say("rome.washer.hi.1", "rome.washer.hi.2", "rome.washer.hi.3", "rome.washer.hi.4", "rome.washer.errand.1", "rome.washer.errand.2");
  await g.reach();
  g.give("toga");
  g.flag("rome.hasToga", true);
  await g.say("rome.washer.errand.3");
}

/** The toga is delivered: she keeps her word. The painted tunic on the low line goes with the fact (see `planes`). */
async function getTunic(g) {
  turnTo(g, "washer");
  await g.say("rome.washer.tunic.1", "rome.washer.tunic.2");
  await g.reach();
  g.give("tunic");
  g.flag("rome.hasTunic", true);
  await g.say("rome.washer.tunic.3");
}

async function talkToWasher(g) {
  if (!g.flag("rome.hasToga")) await firstWash(g);               // the errand first; then whatever else there is to say
  else if (g.flag("rome.delivered") && !g.flag("rome.hasTunic")) return getTunic(g);
  turnTo(g, "washer");
  for (;;) {
    const pick = await g.choose([
      { id: "white", line: "rome.washer.ask.white" },
      { id: "tunic", line: "rome.washer.ask.tunic", when: (g) => !g.flag("rome.hasTunic") },
      { id: "dad", line: "rome.washer.ask.dad" },
      { id: "bye", line: "rome.washer.ask.bye" },
    ]);
    if (pick === "white") {                                       // the best fact he has ever heard
      await g.say("rome.washer.ask.white", "rome.washer.ans.white.1", "rome.washer.ans.white.2", "rome.washer.ans.white.3", "rome.washer.ans.white.4", "rome.washer.ans.white.5");
      g.flag("rome.knowsWash", true);
      if (g.has("toga")) await g.say("rome.washer.ans.white.6", "rome.washer.ans.white.7", "rome.washer.ans.white.8");
    } else if (pick === "tunic") await g.say("rome.washer.ask.tunic", "rome.washer.ans.tunic");
    else if (pick === "dad") await g.say("rome.washer.ask.dad", "rome.washer.ans.dad.1", "rome.washer.ans.dad.2");
    else return g.say("rome.washer.ask.bye", "rome.washer.ans.bye");
  }
}

/** Reaching for the small tunic on the low line. */
async function reachForTunic(g) {
  turnTo(g, "washer");
  if (!g.flag("rome.hasToga")) return g.say("rome.tunic.hands");
  if (!g.flag("rome.delivered")) return g.say("rome.washer.ans.tunic");
  return getTunic(g);
}

// ---------- chain C starts here: the fountain ----------

async function borrowWish(g) {
  if (g.flag("rome.hasCoin")) return g.say("rome.fountain.again");
  await g.reach();
  await g.say("rome.fountain.take");
  g.give("coin");
  g.flag("rome.hasCoin", true);
  await g.say("rome.fountain.shiny", "rome.fountain.wish.1", "rome.fountain.wish.2");    // new, and shiny: that is what it is for
  // His first hard look at it. It is the coin of the story he knows (Matthew 22:17-21, in his own words), and it
  // is not: he has known since he walked into this street that he is on the wrong side of that story. "Not yet."
  await g.wait(450);
  await g.say("rome.fountain.caesar.1", "rome.fountain.caesar.2", "rome.fountain.caesar.3", "rome.fountain.caesar.4");
}

// ---------- the street boy: a friend, and the act's hints ----------

async function meetUrchin(g) {
  if (g.flag("rome.metUrchin")) return;
  await g.say("rome.urchin.hi.1", "rome.urchin.hi.2");
  await stomp(g);
  await g.say("rome.urchin.hi.3");
  await stomp(g);
  await g.say("rome.urchin.hi.4", "rome.urchin.hi.5", "rome.urchin.hi.6");
  g.flag("rome.metUrchin", true);
}

/** What the boy asks him for help with, and what he answers: both follow the story. */
function askForHelp(g) {
  if (g.flag("rome.doorOpen")) return ["rome.urchin.ask.tiny", "rome.urchin.tip.toss"];
  if (g.flag("rome.inside")) return g.flag("rome.hasCoin") ? ["rome.urchin.ask.light", "rome.urchin.tip.spark"] : ["rome.urchin.ask.light", "rome.urchin.tip.shiny.1", "rome.urchin.tip.shiny.2"];
  if (!g.flag("rome.knowsRule")) return ["rome.urchin.ask.help", "rome.urchin.tip.rule"];
  if (!g.flag("rome.hasTunic")) return ["rome.urchin.ask.help", !g.flag("rome.hasToga") ? "rome.urchin.tip.toga" : !g.flag("rome.delivered") ? "rome.urchin.tip.deliver" : "rome.urchin.tip.tunic"];
  if (!g.flag("rome.hasIncense")) return g.flag("rome.hasBreakfast") ? ["rome.urchin.ask.help", "rome.urchin.tip.incense"] : ["rome.urchin.ask.help", "rome.urchin.tip.breakfast.1", "rome.urchin.tip.breakfast.2"];
  return ["rome.urchin.ask.help", "rome.urchin.tip.inside"];
}

async function talkToUrchin(g) {
  await meetUrchin(g);
  for (;;) {
    const help = askForHelp(g);
    const pick = await g.choose([
      { id: "help", line: help[0] },
      { id: "game", line: "rome.urchin.ask.game" },
      { id: "temple", line: "rome.urchin.ask.temple" },
      { id: "bye", line: "rome.urchin.ask.bye" },
    ]);
    if (pick === "help") await g.say(...help);
    else if (pick === "game") {
      await g.say("rome.urchin.ask.game", "rome.urchin.ans.game.1", "rome.urchin.ans.game.2");
      await g.reach(true);                                        // his throw
      await g.say("rome.urchin.ans.game.3", "rome.urchin.ans.game.4", "rome.urchin.ans.game.5");
    } else if (pick === "temple") await g.say("rome.urchin.ask.temple", "rome.urchin.ans.temple.1", "rome.urchin.ans.temple.2", "rome.urchin.ans.temple.3");
    else {
      await g.say("rome.urchin.ask.bye", "rome.urchin.ans.bye");
      return stomp(g);
    }
  }
}

// ---------- the date seller: part of no chain ----------
// He is there to be talked to. He hands over nothing that is carried and sets no fact of the story but his own
// "we have met". What he and the boy talk about: the dates; his God; and what he prays for, which is the heart of it.

/** Where he looks when nobody is talking to him: past the fountain, and a long way off. */
const SELLER_FACES = "SE";

async function meetDateSeller(g) {
  if (g.flag("rome.metDateSeller")) return;
  await g.say("rome.dateseller.hi.1", "rome.dateseller.hi.2", "rome.dateseller.hi.3");
  g.flag("rome.metDateSeller", true);
}

/** The first date is a gift. It is eaten on the spot: nothing goes into the backpack. */
async function tryDate(g, seller) {
  await g.say("rome.dateseller.ask.try", "rome.dateseller.ans.try.1");
  hold(seller, true);                                             // a date, held out on his open hand
  await g.reach();                                                // and taken
  hold(seller, false);
  await g.say("rome.dateseller.ans.try.2", "rome.dateseller.ans.try.3", "rome.dateseller.ans.try.4");
}

/** What the man prays for. The boy knows the town the prophet names, and a great deal more, and it is not his to
    tell. He says one true thing instead, and is blessed for it: Numbers 6:24, which he has heard every Sunday of
    his life, so that his head goes down before he knows it has. */
async function whatHePraysFor(g, seller) {
  const me = g.lead, toEachOther = () => { if (seller && me) { seller.look(me.x, me.y); me.look(seller.x, seller.y); } };
  await g.say("rome.dateseller.ask.pray", "rome.dateseller.ans.pray.1", "rome.dateseller.ans.pray.2");
  if (me) me.face("S");                                           // he turns away, to us: this part is not for the man
  await g.say("rome.dateseller.ans.pray.3", "rome.dateseller.ans.pray.4");
  toEachOther();
  await g.say("rome.dateseller.ans.pray.5");
  await g.wait(500);                                              // the man looks at him for a moment
  await g.say("rome.dateseller.ans.pray.6");
  const blessing = g.say("rome.dateseller.bless.1");
  await g.wait(650);                                              // three words in, the boy knows what this is
  pray(me, true);
  await blessing;
  await g.wait(600);
  pray(me, false);
  await g.wait(350);
  await g.say("rome.dateseller.bless.2");
}

async function talkToDateSeller(g) {
  const seller = g.actor("dateseller"), me = g.lead;
  if (seller && me) { seller.look(me.x, me.y); me.look(seller.x, seller.y); }
  await meetDateSeller(g);
  for (;;) {
    const pick = await g.choose([
      { id: "try", line: "rome.dateseller.ask.try", when: (g) => !heard(g, "rome.dateseller.ans.try.4") },      // one gift
      { id: "god", line: "rome.dateseller.ask.god" },
      // what he prays for comes up once the boy knows whom he prays to; and a blessing is not given twice for the asking
      { id: "pray", line: "rome.dateseller.ask.pray", when: (g) => heard(g, "rome.dateseller.ans.god.6") && !heard(g, "rome.dateseller.bless.2") },
      { id: "bye", line: "rome.dateseller.ask.bye" },
    ]);
    if (pick === "try") await tryDate(g, seller);
    else if (pick === "god") await g.say("rome.dateseller.ask.god", "rome.dateseller.ans.god.1", "rome.dateseller.ans.god.2", "rome.dateseller.ans.god.3", "rome.dateseller.ans.god.4", "rome.dateseller.ans.god.5", "rome.dateseller.ans.god.6");
    else if (pick === "pray") await whatHePraysFor(g, seller);
    else {
      await g.say("rome.dateseller.ask.bye", "rome.dateseller.ans.bye");
      if (seller) seller.face(SELLER_FACES);                      // and he goes back to his watching
      return;
    }
  }
}

/** A carried thing shown to him: he turns to the boy, says what he makes of it, and goes back to his watching. */
const showSeller = (...ids) => async (g) => {
  const seller = g.actor("dateseller");
  turnTo(g, "dateseller");
  await g.say(...ids);
  if (seller) seller.face(SELLER_FACES);
};

export default {
  id: "rome-street",
  era: "rome",
  name: "The street to the Forum",

  // WHERE THINGS ARE. Every place in this file is the painter's own measurement of the finished picture
  // (art/scenes/rome-street/layout.json), or was set by eye against the picture with the people standing in it.
  // The act's check script (check-rome.mjs) reads this file against that one; the few differences that are meant are listed there.
  horizon: 230, full: 590,

  // The roadway from the far end of the street to the front of the picture, and the side street across the
  // front of the snack bar. (We stand where the two meet.)
  walk: { area: [[341, 325], [245, 476], [236, 482], [2, 482], [2, 598], [796, 598], [780, 582], [502, 325], [438, 329], [362, 329]] },
  // Ground that things stand on.
  blocked: [
    [[560, 503], [705, 503], [656, 459], [534, 459]],             // the fountain
    [[232, 500], [292, 500], [300, 481], [244, 481]],             // the laundry basket
    [[624, 598], [636, 566], [700, 548], [796, 540], [796, 598]], // the jars and the cart wheel (the front plane)
    [[0, 497], [23, 497], [37, 488], [7, 488]],                   // the foot of the pier at the left edge
    // The three stepping stones. The engine keeps people 12 pixels clear of blocked ground (5 up and down), which would
    // close the gaps between the stones and shut the street. So each patch is the painter's, drawn in by that much: what
    // ends up out of bounds is the stone itself, and he walks up the street between them.
    [[323, 473], [338, 473], [341, 468], [329, 468]],             // the painter's [[311,478],[350,478],[353,463],[317,463]], drawn in
    [[391, 473], [409, 473], [408, 468], [392, 468]],             // the painter's [[379,478],[421,478],[420,463],[380,463]], drawn in
    [[461, 473], [474, 473], [469, 468], [458, 468]],             // the painter's [[449,478],[486,478],[481,463],[446,463]], drawn in
  ],
  spawn: {
    default: [420, 560],
    fromForum: [400, 338],                                        // the far end of the street, where it opens on the Forum
  },
  exits: ["rome-steps"],

  picture: art + "back.png",
  planes: [
    { id: "awning", src: art + "awning.png", base: 479 },         // the snack bar's awning and the front of its counter: the keeper is behind it
    { id: "fountain", src: art + "fountain.png", base: 501 },
    { id: "laundry", src: art + "laundry.png", plane: "front" },  // the lines of washing overhead
    { id: "tunic", src: art + "tunic.png", plane: "front", when: (g) => !g.flag("rome.hasTunic") },   // the small tunic on the low line, until it is lent
    { id: "front", src: art + "front.png", plane: "front" },      // two wine jars and a handcart wheel at the bottom right corner
  ],

  // The one piece of light in the street: his sneakers. A soft red glow on the paving under his feet, hidden until he stomps.
  live() {
    return `<defs><radialGradient id="stomp-glow"><stop offset="0" stop-color="#ff6a52" stop-opacity="0.95"/><stop offset="0.5" stop-color="#ff4a3d" stop-opacity="0.6"/><stop offset="1" stop-color="#ff4a3d" stop-opacity="0"/></radialGradient></defs>
      <ellipse id="stomp" cx="0" cy="0" rx="40" ry="12" fill="url(#stomp-glow)" opacity="0" shape-rendering="geometricPrecision"/>`;
  },

  actors: [
    { id: "keeper", kind: "keeper", at: [151, 459], face: "SE" },   // on the shop floor, a sidewalk's height above the road
    { id: "washer", kind: "washer", at: [330, 505], face: "SE" },
    { id: "urchin", kind: "urchin", at: [525, 540], face: "W" },    // sitting on the right-hand curb, his feet in the road (his hips are just behind the curb's edge, seven pixels right of the painter's mark, which is where his feet go)
    // The date seller is not in the painter's list: he was placed by eye, on the right-hand pavement at the kerb,
    // just up the street from the last stepping stone, where people cross: clear of the fountain (34 pixels to his
    // right), of the street boy and of the way down the roadway. He stands, so the engine blocks the ground under his
    // feet (473 to 511 across, rows 432 to 452). Why here and not farther up the pavement: words are written over the
    // speaker's head, and from the fountain, the stepping stones and the place the boy first stops, a man farther up
    // would be written across. Here the engine counts him as standing beside the speaker and lifts the words over him.
    { id: "dateseller", kind: "dateseller", at: [492, 444], face: SELLER_FACES },
  ],

  // Back to front: a later area lies over an earlier one. The painter lists the things small before big ("where two
  // shapes overlap, the earlier one is meant"), so they are here in the painter's order turned round, with the way out
  // underneath and the people on top.
  hotspots: [
    {
      id: "to-forum", name: "the Forum", verb: "Walk to", poly: [[376, 178], [454, 178], [454, 240], [478, 332], [326, 332], [352, 246], [376, 246]], walkTo: [400, 338], face: "N",
      look: "rome.toforum.look", use: (g) => g.goto("rome-steps", { spawn: "fromStreet" }),
    },
    { id: "notice-right", name: "more writing", poly: [[716, 372], [799, 345], [799, 520], [716, 478]], walkTo: [634, 523], face: "E", look: "rome.rufus.look" },
    { id: "balcony", name: "apartments", poly: [[641, 75], [718, 37], [718, 277], [641, 277], [568, 263], [568, 122]], walkTo: [593, 510], face: "N", look: "rome.flats.look" },
    { id: "stepping-stones", name: "stepping stones", rect: [315, 448, 168, 34], walkTo: [400, 491], face: "N", look: twice("rome.stones.look", "rome.stones.look2") },   // the second look is at the road itself
    { id: "laundry", name: "washing lines", poly: [[256, 106], [614, 102], [614, 238], [456, 238], [456, 154], [374, 154], [374, 244], [256, 244]], walkTo: [387, 481], face: "N", look: twice("rome.laundry.look", "rome.laundry.look2") },
    { id: "notices", name: "writing on the wall", rect: [4, 195, 228, 49], walkTo: [166, 537], face: "N", look: twice("rome.notices.look", "rome.notices.look2") },   // the red letters over the snack bar: MARCVS, and VOTA
    {
      id: "snack-bar", name: "snack bar", verb: "Order at", rect: [0, 245, 236, 235], walkTo: [139, 488], face: "N",
      look: twice("rome.snackbar.look", "rome.snackbar.look2"), use: talkToKeeper,
    },
    {
      id: "fountain", name: "fountain", verb: "Reach into", rect: [541, 359, 159, 144], walkTo: [532, 494], face: "E",
      look: "rome.fountain.look", use: borrowWish,
      useWith: { toga: "rome.fountain.toga", quarter: "rome.fountain.quarter", phone: "rome.fountain.phone", coin: "rome.fountain.coin" },
    },
    { id: "cat", name: "cat", verb: "Call", rect: [728, 146, 40, 62], walkTo: [609, 532], face: "E", look: "rome.cat.look", use: "rome.cat.use" },
    { id: "birdcage", name: "songbird", rect: [612, 84, 24, 44], walkTo: [593, 510], face: "N", look: "rome.songbird.look" },   // in a wicker cage on the balcony: the cat is watching it
    { id: "sign", name: "hanging sign", rect: [241, 251, 40, 42], walkTo: [310, 519], face: "N", look: "rome.sign.look" },      // the snack bar's: a wine jug and grapes. (The washerwoman stands on the painter's place for it, so he looks from the tunic's.)
    // The painter's place to stand for the price list is 42, 488, which is inside the margin the engine keeps round the
    // foot of the pier beside it: he stands a step to the right of that, and turns to it.
    { id: "price-list", name: "price list", rect: [2, 333, 43, 67], walkTo: [54, 490], face: "NW", look: "rome.pricelist.look" },
    { id: "shrine", name: "little shrine", rect: [198, 325, 31, 82], walkTo: [206, 488], face: "N", look: "rome.shrine.look" },
    {
      id: "basket", name: "laundry basket", verb: "Lift", rect: [240, 446, 50, 50], walkTo: [310, 519], face: "N",
      look: (g) => g.say(g.flag("rome.knowsWash") ? "rome.basket.look2" : "rome.basket.look"),
      use: ["rome.basket.use.1", "rome.basket.use.2"],
    },
    {
      id: "tunic", name: "small tunic", verb: "Take", rect: [253, 307, 40, 55], walkTo: [310, 519], face: "N",
      when: (g) => !g.flag("rome.hasTunic"), look: "rome.tunic.look", use: reachForTunic,
    },
    // The two things of the front cut-out, at the bottom right corner. (They are not in the painter's list: traced from front.png.)
    { id: "wheel", name: "cart wheel", poly: [[700, 548], [712, 520], [740, 506], [800, 506], [800, 600], [700, 600]], walkTo: [600, 536], face: "E", look: "rome.wheel.look" },
    { id: "jars", name: "pointed jars", poly: [[644, 600], [644, 500], [660, 480], [686, 480], [708, 498], [716, 520], [702, 548], [702, 600]], walkTo: [600, 536], face: "E", look: "rome.jars.look" },
    // The people. Each area is the figure as the engine draws it at its mark, and a little over.
    {
      id: "keeper", name: "snack-bar keeper", verb: "Talk to", rect: [128, 358, 46, 62], walkTo: [139, 488], face: "N",        // what shows of him above his counter
      look: twice("rome.keeper.look", "rome.keeper.look2"), use: talkToKeeper,
      useWith: {
        quarter: payWithQuarter,
        coin: ["rome.keeper.coin.1", "rome.keeper.coin.2", "rome.keeper.coin.3", "rome.keeper.coin.4"],
        gum: ["rome.keeper.gum.1", "rome.keeper.gum.2"],
        toga: "rome.keeper.toga", breakfast: "rome.keeper.breakfast",
      },
    },
    {
      id: "washer", name: "washerwoman", verb: "Talk to", rect: [306, 386, 48, 120], walkTo: [392, 512], face: "W",
      look: twice("rome.washer.look", "rome.washer.look2"), use: talkToWasher,
      useWith: { toga: "rome.washer.toga", coin: "rome.washer.coin", breakfast: "rome.washer.breakfast", tunic: "rome.washer.tunic.back" },
    },
    {
      id: "urchin", name: "street boy", verb: "Talk to", rect: [485, 466, 52, 80], walkTo: [452, 538], face: "E",
      look: twice("rome.urchin.look", "rome.urchin.look2"), use: talkToUrchin,
      useWith: {
        gum: ["rome.urchin.gum.1", "rome.urchin.gum.2", "rome.urchin.gum.3", "rome.urchin.gum.4"],
        coin: ["rome.urchin.coin.1", "rome.urchin.coin.2", "rome.urchin.coin.3"],
        phone: ["rome.urchin.phone.1", "rome.urchin.phone.2", "rome.urchin.phone.3", "rome.urchin.phone.4"],
        quarter: ["rome.urchin.quarter.1", "rome.urchin.quarter.2"],
        toga: "rome.urchin.toga", breakfast: "rome.urchin.breakfast",
      },
    },
    {
      // He is talked to from the roadway, at the curb below him, so that the boy looks up at him and neither hides the other.
      id: "dateseller", name: "date seller", verb: "Talk to", rect: [470, 344, 46, 102], walkTo: [446, 460], face: "E",
      look: twice("rome.dateseller.look", "rome.dateseller.look2"), use: talkToDateSeller,
      useWith: {
        quarter: showSeller("rome.dateseller.quarter.1", "rome.dateseller.quarter.2"),
        phone: showSeller("rome.dateseller.phone"), toga: showSeller("rome.dateseller.toga"), coin: showSeller("rome.dateseller.coin.1", "rome.dateseller.coin.2"),
        breakfast: showSeller("rome.dateseller.breakfast"),      // the soothsayer's, and so his hens (briefs/DATING.md): not by hens, thank you
      },
    },
  ],

  // Runs when the lead arrives. It must be safe to run twice, so each remark checks its own fact.
  // The first time, the keeper is crying his wares, and the name he cries tells the boy when he is: before Christ.
  // (Two facts, so that a game saved in this street before that was written still gets it, the next time he comes.)
  async enter(g, from) {
    if (from === "rome-steps") await g.walkTo(404, 494);          // he comes down the street toward us, between the stepping stones
    const first = !g.flag("rome.sawStreet");
    if (!first && g.flag("rome.knowsBC")) return;
    await g.wait(300);
    if (first) await g.say("rome.street.arrive.1");
    if (!g.flag("rome.knowsBC")) {
      const me = g.lead, keeper = g.actor("keeper");
      await g.say("rome.street.cry");
      if (me && keeper) me.look(keeper.x, keeper.y);              // he looks round at the snack bar
      await g.say("rome.street.bc.1");
      if (me) me.face("S");                                       // and then at nothing at all
      await g.say("rome.street.bc.2", "rome.street.bc.3", "rome.street.bc.4");
      g.flag("rome.knowsBC", true);
    }
    if (first) await g.say("rome.street.arrive.2");
    g.flag("rome.sawStreet", true);
  },
};

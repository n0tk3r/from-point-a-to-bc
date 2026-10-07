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
// Try it: index.html?scene=rome-street&lead=son&flags=rome.arrived
// Later states: add rome.knowsRule, rome.hasToga, rome.delivered, rome.hasBreakfast, rome.inside ... to &flags=

const art = "art/scenes/rome-street/";

/** Has this line been spoken yet? (The engine counts every line it says.) */
const heard = (g, id) => !!g.store.data.seenLines[id];
/** A thing worth looking at twice: the first line the first time, the second after that. */
const twice = (first, second) => (g) => g.say(heard(g, first) ? second : first);
/** Someone who can stand turns to the boy. */
const turnTo = (g, who) => { const a = g.actor(who), me = g.lead; if (a && me) a.look(me.x, me.y); };

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
    { id: "stepping-stones", name: "stepping stones", rect: [315, 448, 168, 34], walkTo: [400, 491], face: "N", look: "rome.stones.look" },
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
  ],

  // Runs when the lead arrives. It must be safe to run twice, so the remark checks its own fact.
  async enter(g, from) {
    if (from === "rome-steps") await g.walkTo(404, 494);          // he comes down the street toward us, between the stepping stones
    if (g.flag("rome.sawStreet")) return;
    await g.wait(300);
    await g.say("rome.street.arrive.1", "rome.street.arrive.2");
    g.flag("rome.sawStreet", true);
  },
};

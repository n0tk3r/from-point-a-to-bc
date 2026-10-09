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
// Whatever he takes out of the luggage on the roof POPS OUT: it jumps out of the opened lid in a little arc, lands
// on the sand at his feet with a bounce and a puff of dust, and lies there while he says what it is; then he bends
// and picks it up. It is the thing's own inventory picture (art/items/<id>.png), moved on the game's clock, with its
// shadow and the dust drawn on the live layer (popOut, below).
//
// Under the shirts in the suitcase, with the sunglasses: General Feathers, his youngest's stuffed hen, sent along
// "to keep an eye on Daddy", and her note in crayon (shown close up). No puzzle needs her. He carries her
// (`chicken`), talks to her, and shows her to people; nobody he meets here has ever seen a chicken.
//
// THE DOOR MIRROR announces itself. Now and then a glint runs across it; and the first time Dad comes up to the car
// (to look at any part of it, or to work at it: the glovebox is the first puzzle, so nobody misses it), the low sun
// off the mirror catches him in the eye: a flash at his face, he flinches and shades his eyes, and says so. Once.
// It is the hint that the mirror is very reflective, long before he needs it. Both are light, drawn by code, and laid
// in the cast just in front of the mirror and of him (glint, dazzle, below).
//
// LOT. The man sitting in the shade of the palm by the water, praying while his donkey drinks, is Lot, Abram's
// nephew (Genesis 13:1: Abram went up out of Egypt, "and Lot with him"). Praying is his state whenever nobody is
// talking to him: when Dad speaks to him he lowers his hands and looks up, and when they part he goes back to it.
// He is the first person Dad meets. He saw the boy go up the track; he knows the Egyptians call the great pyramid the
// Horizon; he has heard from the men who come for water that a wall inside hums and that the scribe's pen has split;
// and the geese face the hill. Asked who he is, he tells it as his own memory, in his own words, from Genesis 11:27
// to 13:5 and nothing beyond: and Dad understands, slowly and then all at once, that he is standing in Genesis 12
// ("egypt.heardAbram"; the river, the reeds, the site's news and the open door follow it). Asked why he is waiting,
// he tells this week, briefly, judging nobody. And the first time they part after that, a father who has lost his
// boy and a man whose uncle has no son yet and has been promised a nation have a word, and Lot prays for the boy, to
// "the God of my father's brother Abram". Lot's prayer is his own: Dad bows his head and says Amen, and his own
// three prayers in the act are as they were. Before Lot has said who he is, he is a "herdsman" on the screen.
//
// Dad is a Christian father, and this is the Egypt of his Bible. When he understands that the boy is gone, he prays
// (the first of his three prayers in the act). At the reeds he looks for a basket; at the river he wonders which of
// Abraham, Joseph and Moses he has missed and which are still to come; the pyramids get one more thought. Once Lot has
// told him who he is, he knows: Abram is in Egypt this week, and Joseph and Moses are still to come. What he says at
// the river and the reeds after that says so. (None of this is part of a puzzle.)
//
// The way out is the track up to the building site: its far end, or anywhere along the top of the picture.
//
// Try it: index.html?scene=egypt-crash&lead=dad
// Later states: &flags=egypt.arrived,egypt.knowsLight   (the shade and the mirror can then be taken)
//               &flags=egypt.arrived,egypt.metLot,egypt.knowsLot,egypt.heardAbram   (Lot has told him who he is)

const art = "art/scenes/egypt-crash/";
/** The Nile near this bank (the painter's, layout.json "fx"): where its light moves, and the donkey's rings stay. */
const NILE = [[0, 264], [344, 264], [321, 276], [295, 300], [261, 336], [213, 384], [149, 440], [83, 492], [19, 530], [0, 532]];

/** How many times a line has been spoken. (The engine counts every line it says.) */
const count = (g, id) => g.store.data.seenLines[id] || 0;
/** A thing worth looking at twice: the first line, then the second, turn about. */
const twice = (first, second) => (g) => g.say(count(g, first) <= count(g, second) ? first : second);
/** Someone turns to Dad. */
const turnTo = (g, who) => { const a = g.actor(who), me = g.lead; if (a && me) a.look(me.x, me.y); };
/** Head bowed, hands folded or lifted (true), or let it go (false). A figure that has no such pose simply stands. */
const pray = (a, on) => a && a.pray && a.pray(on);
/** How big someone (or something) is at this depth: as the engine reckons it from `horizon`, `full` and `minScale`. */
const depth = (y) => Math.min(1.12, Math.max(0.2, (y - 262) / (590 - 262)));

// ---------- the river ----------
/** The river has the old joke, and the end of the joke: it is the Nile. And once, straight after that, what the
    Nile is to a man who knows his Bible. Before Lot has told him who he is he wonders who he has missed and who is
    still to come, and does not settle it. After it he knows, and says so, once (even if he wondered before). */
async function lookAtRiver(g) {
  const second = count(g, "egypt.river.look") > count(g, "egypt.river.look2");
  await g.say(second ? "egypt.river.look2" : "egypt.river.look");
  if (!second) return;
  if (g.flag("egypt.heardAbram")) { if (!count(g, "egypt.river.after.1")) await g.say("egypt.river.after.1", "egypt.river.after.2", "egypt.river.after.3"); }
  else if (!count(g, "egypt.river.bible.1")) await g.say("egypt.river.bible.1", "egypt.river.bible.2", "egypt.river.bible.3", "egypt.river.bible.4");
}

/** The pyramids from the bank: three things to say, in turn. The third is a wonder, and once he knows that Abram is
    in Egypt this week it is a different wonder. */
function lookAtPyramids(g) {
  const third = g.flag("egypt.heardAbram") ? "egypt.pyramids.look3b" : "egypt.pyramids.look3";
  const seen = (id) => (id === third ? count(g, "egypt.pyramids.look3") + count(g, "egypt.pyramids.look3b") : count(g, id));
  return g.say(["egypt.pyramids.look", "egypt.pyramids.look2", third].reduce((best, id) => (seen(id) < seen(best) ? id : best)));
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

// ---------- Lot ----------
/** A word with Lot: he lowers his hands and looks up at Dad; when it is over, whatever happened, he goes back to his
    prayers. `script` is anything a hotspot can do (a line, a list of lines, a function). */
const withLot = (script) => async (g) => {
  const lot = g.actor("lot");
  pray(lot, false);
  turnTo(g, "lot");
  try { await g.act(script); }
  finally { pray(lot, true); }
};

async function talkToLot(g) {
  if (!g.flag("egypt.metLot")) {
    await g.say("egypt.lot.hello", "egypt.scribe.hello2", "egypt.lot.hello2");
    g.flag("egypt.metLot", true);
  }
  for (;;) {
    const pick = await g.choose([
      { id: "boy", line: "egypt.ask.boy" },
      { id: "horizon", line: "egypt.lot.ask.horizon", when: (g) => count(g, "egypt.lot.boy.2") > 0 },       // he has to have heard the word first
      { id: "news", line: "egypt.lot.ask.news" },
      { id: "who", line: "egypt.lot.ask.who", when: (g) => !g.flag("egypt.knowsLot") },                      // told once
      { id: "week", line: "egypt.lot.ask.week", when: (g) => !!g.flag("egypt.knowsLot") && !count(g, "egypt.lot.week.1") },
      { id: "bye", line: "egypt.lot.ask.bye" },
    ]);
    if (pick === "boy") await g.say("egypt.ask.boy", "egypt.lot.boy.1", "egypt.lot.boy.2", "egypt.lot.boy.3");
    else if (pick === "horizon") await g.say("egypt.lot.ask.horizon", "egypt.lot.horizon.1", "egypt.lot.horizon.2");
    else if (pick === "news") await g.say("egypt.lot.ask.news", "egypt.lot.news.1", "egypt.lot.news.2", "egypt.lot.news.3", "egypt.lot.news.4");
    else if (pick === "who") await whoHeIs(g);
    else if (pick === "week") await g.say("egypt.lot.ask.week", "egypt.lot.week.1", "egypt.lot.week.2", "egypt.lot.week.3", "egypt.lot.week.4", "egypt.lot.week.5", "egypt.lot.week.6");
    else return parting(g);
  }
}

/** Who he is, as his own memory: Genesis 11:27 to 12:10, and his own flocks and tents (13:5). Dad understands slowly
    (Ur of the Chaldees), and then all at once: he looks out over the river and says it to himself. */
async function whoHeIs(g) {
  await g.say("egypt.lot.ask.who", "egypt.lot.who.1");
  g.flag("egypt.knowsLot", true);                 // he has said who he is: from now on he is "Lot" on the screen
  await g.say("egypt.lot.who.2", "egypt.lot.who.3", "egypt.lot.who.4", "egypt.lot.who.5", "egypt.lot.who.6", "egypt.lot.who.7", "egypt.lot.who.8");
  g.flag("egypt.heardAbram", true);               // and Dad knows when he is
  await g.wait(400);
  g.lead.look(40, 330);                           // out over the river
  await g.wait(500);
  await g.say("egypt.abram.1", "egypt.abram.2", "egypt.abram.3");
  await g.wait(300);
  const lot = g.actor("lot");
  if (lot) g.lead.look(lot.x, lot.y);             // and back to the man in front of him
}

/** Goodbye. The first time after Lot has told him who he is: a word about sons, the choice the scene turns on (made
    without fuss), and Lot's prayer for the boy, with Dad's head bowed beside him; then Dad's thanks. */
async function parting(g) {
  await g.say("egypt.lot.ask.bye");
  if (!g.flag("egypt.knowsLot") || g.flag("egypt.lotPrayed")) return g.say("egypt.lot.bye");
  await g.say("egypt.lot.son.1", "egypt.lot.son.2", "egypt.lot.son.3", "egypt.abram.4", "egypt.abram.5", "egypt.lot.son.4");
  const lot = g.actor("lot");
  pray(lot, true);                                // he lifts his hands for the boy,
  await g.wait(250);
  pray(g.lead, true);                             // and Dad bows his head with him
  await g.wait(400);
  await g.say("egypt.lot.prayer", "egypt.lot.amen");
  pray(g.lead, false);
  pray(lot, false);
  await g.wait(350);                              // (his hands are his own again before he says thank you)
  g.flag("egypt.lotPrayed", true);
  await g.say("egypt.lot.thanks");
}

// His day by the water (round four: briefs/ROUND-4.md, "the people are alive"). He prays in spells, as a man waiting all
// day does: half a minute or so with his hands lifted, then they come down and he rests a while where he sits, shifts,
// rubs his knees, looks about; and now and then, while they are down, he gets up with his staff and walks a few steps
// along the bank, to his donkey or to the water's edge to look up the river for the king's men, and comes back and
// sits (his `life`, under `actors`). Then he prays again. Nothing here moves him while a script has the stage (and a
// word with him lowers his hands and lifts them again at the end, as before); `?still` (or game.life.enabled = false,
// as the tests have it) leaves him at his prayers the whole time, as in round three.
const PRAYS = [24000, 34000, 28000, 38000], RESTS = [30000, 40000, 26000, 44000];      // ms of the game's clock, in turn
/** When his hands last came down (the game's clock): he sits a little while before he gets up (his life's `when`). */
const DAY = { rested: -Infinity };
/** Something on the stage that draws nothing, and keeps Lot's spells of prayer on the game's clock while the scene is up. */
function lotsDay(g) {
  const cast = g.view && g.view.cast;
  if (!cast || !cast.addPicture || cast.get("lots-day")) return;
  const s = cast.addPicture("lots-day", {}, 0, 0, 1);
  s.picture = () => null;
  let praying = true, n = 0, left = PRAYS[0];
  s.tick = (dt) => {
    const lot = g.actor("lot"), life = g.life;
    // (only while his life goes on: not while a script has the stage, a line is being said, a close look or the menu is
    // up, or Show is on; and not at all with ?still)
    if (!lot || !life || !life.enabled || g.busy || g.mode !== "play" || (life.quiet ? !life.quiet() : g.dialogue && (g.dialogue.active || g.dialogue.choosing))) return;
    const now = !!lot.act && lot.act.low === "pray";
    if (now !== praying) { praying = now; left = (now ? PRAYS : RESTS)[n++ % 4]; if (!now) DAY.rested = g.clock.now; }   // (a word with him has ended, or begun: a spell afresh)
    if ((left -= dt) > 0) return;
    if (praying) { pray(lot, false); praying = false; left = RESTS[n++ % 4]; DAY.rested = g.clock.now; }
    else if (!life.isAway("lot") && lot.seated && !lot.walking && !lot.move) { pray(lot, true); praying = true; left = PRAYS[n++ % 4]; }
  };
}
/** Looked at, he is at his prayers (what Dad says of him says so): if his hands are down, they go up as Dad looks. */
const lookAtLot = async (g) => {
  const lot = g.actor("lot");
  if (lot && !(lot.act && lot.act.low === "pray")) { pray(lot, true); await g.wait(350); }
  await g.say(g.flag("egypt.lotPrayed") ? "egypt.lot.look2" : "egypt.lot.look");
};

const LOT = {
  id: "lot", verb: "Talk to", walkTo: [448, 444], face: "W",
  poly: [[396, 392], [404, 382], [413, 384], [425, 397], [430, 429], [418, 435], [397, 435], [392, 427]],     // his figure in every frame he has here (the staff on the sand left out)
  look: lookAtLot, use: withLot(talkToLot),
  useWith: {
    rootbeer: withLot(["egypt.lot.rootbeer.1", "egypt.lot.rootbeer.2"]),
    map: withLot(["egypt.lot.map.1", "egypt.lot.map.2", "egypt.lot.map.3"]),
    chicken: withLot(showGeneral("lot", "egypt.lot.chicken")),
  },
};

// ---------- chain A: a reed, and the map ----------
async function cutReed(g) {
  if (g.flag("egypt.hasReed")) return g.say("egypt.reeds.again");
  await g.reach();
  await g.say("egypt.reeds.take");
  g.give("reed");
  g.flag("egypt.hasReed", true);
  await g.reach(true);                    // and while he is in there, he parts the reeds and has a look (Exodus 2:3)
  await g.say("egypt.reeds.basket.1", g.flag("egypt.heardAbram") ? "egypt.reeds.basket.3" : "egypt.reeds.basket.2");     // (once he knows, he knows Moses is still to come)
}

async function searchGlovebox(g) {
  if (g.flag("egypt.hasMap")) return g.say("egypt.wagon.empty");
  await g.reach();
  await g.say("egypt.wagon.use");
  g.give("map");
  g.flag("egypt.hasMap", true);
}

// ---------- what comes out of the luggage: it jumps out, lands on the sand, and lies there a moment ----------
// The mouth of each lid on the roof, where things come out of it.
const LIDS = { suitcase: [626, 420], trunk: [682, 398], cooler: [726, 402] };
// Each thing's own picture (art/items/<id>.png, 64 pixels square): the point of it that rests on the sand (the middle
// of the bottom of its paint), and how big it is on the sand by Dad's feet, beside the 64 pixels it was painted at.
const ITEM = {
  flashlight: { foot: [28, 57], size: 0.5 },
  shade: { foot: [32, 57], size: 0.66 },
  rootbeer: { foot: [30, 62], size: 0.52 },
  sunglasses: { foot: [31, 48], size: 0.46 },
  chicken: { foot: [35, 64], size: 0.6 },
};
const DUST = 5;                                   // puffs of dust where it lands

/** Something jumps out of a lid and lands on the sand by his right foot, with a bounce, its shadow under it and a puff
    of dust; he looks at it. Resolves with the thing on the sand (null in a game with no stage to show it on). */
async function popOut(g, item, lid) {
  const me = g.lead, [x0, y0] = LIDS[lid];
  const x1 = Math.round((me ? me.x : x0) + 34), y1 = Math.min(Math.round((me ? me.y : 566) + 20), 592);      // on the sand, at his right hand
  const cast = g.view && g.view.cast, spec = ITEM[item], src = `art/items/${item}.png`;
  if (!cast || !cast.addPicture) return null;
  if (g.assets && g.assets.picture) await g.assets.picture(src);          // (it is here before it is shown, so it does not pop in late)
  const k = spec.size * depth(y1), thing = cast.addPicture("pop-" + item, { src, foot: spec.foot }, x0, y0, k * 0.85);
  thing.base = 560;                               // in the air it is in front of the car and its luggage, and behind him
  const shadow = g.q("#pop-shadow"), dust = g.q("#pop-dust");
  const shade = (x, y, near) => { if (!shadow) return; shadow.setAttribute("cx", x); shadow.setAttribute("cy", y); shadow.setAttribute("rx", 13 * k * (0.5 + 0.5 * near)); shadow.setAttribute("ry", 3.6 * k * (0.5 + 0.5 * near)); shadow.setAttribute("opacity", 0.45 * near); };
  // Up out of the lid and down onto the sand: straight across, and a parabola up and down (gravity).
  const rise = 150;
  await g.tween(620, (t) => {
    const x = x0 + (x1 - x0) * t, y = y0 + (y1 - y0) * t - 4 * rise * t * (1 - t);
    thing.place(x, y, k * (0.85 + 0.15 * t));
    shade(x, 548 + (y1 - 548) * t, t * t);
  });
  thing.base = null;                              // on the sand it stands where it lies: in front of him
  shade(x1, y1, 1);
  // a puff of dust, and a little bounce
  const puff = g.tween(520, (t) => {
    if (dust) dust.setAttribute("opacity", 0.75 * (1 - t));
    for (let n = 0; n < DUST; n++) {
      const p = g.q("#pop-dust-" + n), a = Math.PI * (0.08 + 0.84 * (n / (DUST - 1))), r = (6 + 16 * t) * k * 1.6;
      if (!p) continue;
      p.setAttribute("cx", x1 + Math.cos(a) * r * 1.4);
      p.setAttribute("cy", y1 - Math.sin(a) * r * 0.55 - 2);
      p.setAttribute("r", (2.2 + 4.5 * t) * k * 1.6);
    }
  });
  await g.tween(220, (t) => thing.place(x1, y1 - 10 * k * 4 * t * (1 - t), k));
  thing.place(x1, y1, k);
  await puff;
  if (dust) dust.setAttribute("opacity", 0);
  if (me) me.look(x1, y1);                        // and he looks at what it is
  return thing;
}

/** He bends down and picks up what is lying on the sand, and it is his. */
async function pickUp(g, item, thing) {
  const bend = g.reach(true);
  await g.wait(260);                              // (it leaves the sand as his hand gets there)
  if (thing && g.view && g.view.cast) g.view.cast.remove(thing.id);
  const shadow = g.q("#pop-shadow");
  if (shadow) shadow.setAttribute("opacity", 0);
  await bend;
  g.give(item);
}

/** Out of the lid, onto the sand, a word about it while it lies there, and into his pockets. */
async function unpack(g, item, lid, line) {
  const thing = await popOut(g, item, lid);
  try {
    await g.wait(300);                            // it lies there a moment, so that the player sees exactly what it is
    await g.say(line);
  } finally { await pickUp(g, item, thing); }
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
    await unpack(g, "flashlight", "trunk", "egypt.trunk.flashlight");
    g.flag("egypt.tookFlashlight", true);
    return;
  }
  if (g.flag("egypt.tookShade")) return g.say("egypt.trunk.after");
  if (!g.flag("egypt.knowsLight")) return g.say("egypt.trunk.rest", "egypt.car.noreason");
  await unpack(g, "shade", "trunk", "egypt.trunk.shade");
  g.flag("egypt.tookShade", true);
}

/** The cooler: one root beer at a time, and there is always another. */
async function searchCooler(g) {
  await openLid(g, "egypt.coolerOpen");
  if (g.has("rootbeer")) return g.say("egypt.cooler.have");
  await unpack(g, "rootbeer", "cooler", g.flag("egypt.tookRootbeer") ? "egypt.cooler.more" : "egypt.cooler.take");
  g.flag("egypt.tookRootbeer", true);
}

/** The suitcase: the sunglasses on top, six shirts that stay where they are, and under the shirts General Feathers
    with her orders. Everybody opens the suitcase (the sunglasses are needed), so nobody misses her. */
async function searchSuitcase(g) {
  await openLid(g, "egypt.suitcaseOpen");
  if (g.flag("egypt.tookSunglasses") && g.flag("egypt.tookGeneral")) return g.say("egypt.suitcase.again");
  if (!g.flag("egypt.tookSunglasses")) {
    await unpack(g, "sunglasses", "suitcase", "egypt.suitcase.take");
    g.flag("egypt.tookSunglasses", true);
  }
  await g.reach();                                // back up, and down under the shirts
  const general = await popOut(g, "chicken", "suitcase");
  await g.wait(600);                              // she lies on the sand a moment, for all to see
  const bend = g.reach(true);                     // he picks her up, and her orders with her
  await g.wait(260);
  if (general && g.view && g.view.cast) g.view.cast.remove(general.id);
  const shadow = g.q("#pop-shadow");
  if (shadow) shadow.setAttribute("opacity", 0);
  await bend;
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
  g.flag("egypt.tookMirror", true);       // the mirror leaves the door (its cut-out, its glint and its clickable area follow the fact)
  await g.say("egypt.mirror.take");
  g.give("carmirror");
}

/** A piece of luggage is two clickable shapes, because an open lid stands taller than a shut one. One shows at a time. */
const lidded = (spot, fact, shut, open) => [
  { ...spot, poly: shut, when: (g) => !g.flag(fact) },
  { ...spot, poly: open, verb: "Search", plane: spot.id, when: (g) => !!g.flag(fact) },
];

// ---------- the door mirror's light ----------
const MIRROR = [626, 486];                        // the middle of the glass (the cut-out mirror.png covers 620-633 by 482-490)
/** Pictures drawn by code for the light, made once, the first time they are wanted. (Only a browser draws them.) */
let LIGHT = null;
function light() {
  if (LIGHT || typeof document === "undefined") return LIGHT;
  const canvas = (w, h, draw) => { const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h); return c; };
  const star = (ctx, x, y, r, a = 1) => {
    const glow = ctx.createRadialGradient(x, y, 0, x, y, r);
    glow.addColorStop(0, `rgba(255,255,248,${a})`); glow.addColorStop(0.25, `rgba(255,246,206,${0.75 * a})`); glow.addColorStop(1, "rgba(255,236,170,0)");
    ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = `rgba(255,255,250,${0.9 * a})`;
    for (const [w, h] of [[r * 1.7, r * 0.09], [r * 0.09, r * 1.25]]) { ctx.beginPath(); ctx.ellipse(x, y, w, h, 0, 0, Math.PI * 2); ctx.fill(); }
  };
  // The glint: a bright bar that runs across the glass, left to right, and a pin of light where it is brightest.
  const glint = [];
  for (let n = 0; n < 9; n++) {
    const t = n / 8, c = canvas(40, 30, (ctx) => {
      const x = 7 + 26 * t, a = Math.sin(Math.PI * t);
      ctx.fillStyle = `rgba(255,255,244,${0.85 * a})`;
      ctx.beginPath(); ctx.moveTo(x - 2, 21); ctx.lineTo(x + 1.5, 21); ctx.lineTo(x + 5, 9); ctx.lineTo(x + 1.5, 9); ctx.closePath(); ctx.fill();
      if (n >= 3 && n <= 5) star(ctx, 20, 15, 9, n === 4 ? 1 : 0.55);
    });
    glint.push({ canvas: c, ox: 20, oy: 15 });
  }
  LIGHT = { glint, star, canvas };
  return LIGHT;
}

/** Now and then a glint runs across the door mirror: a sweep of about half a second, at irregular times. It is light,
    drawn by code, and laid on the cast just in front of the mirror; it goes when the mirror goes, and keeps still for
    a player who asked for less motion. */
function addGlint(g) {
  const cast = g.view && g.view.cast;
  if (!cast || !cast.addPicture || cast.get("glint")) return;
  const s = cast.addPicture("glint", { base: [[490, 541.3], [790, 537.3]], when: (g) => !g.flag("egypt.tookMirror") }, MIRROR[0], MIRROR[1], 1);
  const GAPS = [3600, 7400, 5200, 8900, 6100], SWEEP = 560, CYCLE = GAPS.reduce((a, b) => a + b, 0);
  s.picture = (palette, calm) => {
    const pics = light();
    if (!pics || calm || s.hidden) return null;
    let t = s.now % CYCLE;
    for (const gap of GAPS) { if (t < gap) return t < SWEEP ? pics.glint[Math.min(8, Math.floor((t / SWEEP) * 9))] : null; t -= gap; }
    return null;
  };
  s.refresh(g);
}

/** The first time he comes up to the car: the low sun off the door mirror catches him in the eye. A flash at the
    glass, a shaft of light from it to his face, a burst at his eyes; he flinches and shades them, and says so. Once. */
async function dazzle(g) {
  g.flag("egypt.dazzled", true);
  const me = g.lead, cast = g.view && g.view.cast, pics = light();
  if (!me) return;
  me.look(...MIRROR);                             // he looks up at the car
  await g.wait(150);
  // His eyes: a little below the top of his head, toward the way he is facing.
  const eyes = [me.x + 2, me.y - (me.h || 150) * me.scale * 0.9];
  let flash = null;
  if (cast && cast.addPicture) {
    const [mx, my] = MIRROR, [ex, ey] = eyes, left = Math.min(mx, ex) - 34, top = Math.min(my, ey) - 34;
    let pic = null;                               // (drawn the first time the cast asks for it: only a browser draws)
    const draw = () => pics && { canvas: pics.canvas(Math.abs(mx - ex) + 68, Math.abs(my - ey) + 68, (ctx) => {
      const a = [mx - left, my - top], b = [ex - left, ey - top], len = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1, nx = (a[1] - b[1]) / len, ny = (b[0] - a[0]) / len;
      const shaft = ctx.createLinearGradient(a[0], a[1], b[0], b[1]);
      shaft.addColorStop(0, "rgba(255,252,230,0.85)"); shaft.addColorStop(1, "rgba(255,244,200,0.35)");
      ctx.fillStyle = shaft;
      ctx.beginPath(); ctx.moveTo(a[0] + nx * 1.2, a[1] + ny * 1.2); ctx.lineTo(b[0] + nx * 5, b[1] + ny * 5); ctx.lineTo(b[0] - nx * 5, b[1] - ny * 5); ctx.lineTo(a[0] - nx * 1.2, a[1] - ny * 1.2); ctx.closePath(); ctx.fill();
      pics.star(ctx, a[0], a[1], 16);
      pics.star(ctx, b[0], b[1], 26);
    }), ox: 0, oy: 0 };
    flash = cast.addPicture("dazzle", {}, left, top, 1);
    flash.plane = "front";                        // light in the air: over the car, and over him
    flash.picture = () => (pic = pic || draw());
    flash.fade(0);
  }
  try {
    if (flash) await g.tween(120, (k) => flash.fade(k));
    me.face("SW");                                // he flinches away from it (his hand reads from the front, not from behind)...
    if (me.shade) me.shade(true);                 // ...and shades his eyes
    if (flash) await g.tween(420, (k) => flash.fade(1 - k));
  } finally {
    if (flash) cast.remove(flash.id);
  }
  await g.say("egypt.mirror.dazzle");
  if (me.shade) me.shade(false);
  await g.wait(150);
  me.face("N");                                   // and back to the car
}

/** Any part of the car: the first time he comes up to it, the mirror gets him in the eye first. */
const nearCar = (action) => async (g) => {
  if (!g.flag("egypt.dazzled")) await dazzle(g);
  return g.act(action);
};
/** The same for every way of clicking a part of the car: looking, using, and trying a carried thing on it. */
const atCar = (spot) => ({ ...spot, look: nearCar(spot.look), ...(spot.use ? { use: nearCar(spot.use) } : {}),
  ...(spot.useWith ? { useWith: Object.fromEntries(Object.entries(spot.useWith).map(([item, a]) => [item, nearCar(a)])) } : {}) });

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
  // The top of the picture is the way up the track: a click anywhere along it takes him to the foot of the track and on up.
  edges: {
    N: { to: "egypt-site", spawn: "fromCrash", name: "up the track", walkTo: [500, 372] },
  },

  picture: art + "back.png",

  // Each palm is its own cut-out, so that somebody standing between two of them is behind one and in front of the other.
  // The wagon's mirror and its three open lids are cut-outs laid over the wagon, pixel for pixel. Their base lines sit a
  // hair in front of the wagon's and of each other's, in the painter's order: suitcase, then trunk, then cooler.
  planes: [
    { id: "palm-3", src: art + "palm-3.png", base: 318, solid: [[292, 313], [308, 313], [309, 320], [291, 320]] },
    { id: "palm-2", src: art + "palm-2.png", base: 352, solid: [[241, 344], [263, 344], [265, 354], [239, 354]] },
    { id: "palm-1", src: art + "palm-1.png", base: 400, solid: [[174, 389], [206, 389], [209, 402], [171, 402]] },
    { id: "donkey", src: art + "donkey.png", base: 420, solid: [[171, 411], [226, 411], [226, 426], [171, 426]] },        // drinking at the water's edge, in front of the near palm
    { id: "wagon", src: art + "wagon.png", base: [[490, 541], [790, 537]],
      solid: [[372, 549], [394, 530], [424, 514], [456, 502], [490, 499], [522, 506], [552, 512], [757, 516], [797, 536], [793, 549], [640, 553], [550, 558], [450, 558]] },   // the car, and the sand heaped at its nose
    { id: "mirror", src: art + "mirror.png", base: [[490, 541.2], [790, 537.2]], when: (g) => !g.flag("egypt.tookMirror") },
    { id: "suitcase", src: art + "suitcase-open.png", base: [[490, 541.4], [790, 537.4]], when: (g) => !!g.flag("egypt.suitcaseOpen") },
    { id: "trunk", src: art + "trunk-open.png", base: [[490, 541.6], [790, 537.6]], when: (g) => !!g.flag("egypt.trunkOpen") },
    { id: "cooler", src: art + "cooler-open.png", base: [[490, 541.8], [790, 537.8]], when: (g) => !!g.flag("egypt.coolerOpen") },
    { id: "steam", frames: [art + "steam-0.png", art + "steam-1.png", art + "steam-2.png", art + "steam-3.png"], fps: 6, at: [472, 498], foot: [30, 104], base: [[490, 542], [790, 538]] },
    { id: "papyrus", src: art + "front.png", plane: "front" },
  ],

  // The live layer: what comes out of the luggage throws a shadow on the sand, and kicks up a puff of dust where it
  // lands (popOut). All of it is hidden until then.
  live() {
    return `<defs><filter id="pop-soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.4"/></filter></defs>
      <g shape-rendering="geometricPrecision">
        <ellipse id="pop-shadow" cx="0" cy="0" rx="10" ry="3" fill="#4a2a10" opacity="0" filter="url(#pop-soft)"/>
        <g id="pop-dust" opacity="0" fill="#ecd3a0" filter="url(#pop-soft)">${Array.from({ length: DUST }, (_, n) => `<circle id="pop-dust-${n}" cx="0" cy="0" r="2"/>`).join("")}</g>
      </g>`;
  },

  actors: [
    // Sitting on the sand in the near palm's shade, his bundle behind him. Between his prayers (lotsDay, above) he gets up
    // now and then and stays by the river: a few steps along the bank to stand by his donkey, or to the water's edge
    // to look up the river for the king's men.
    { id: "lot", kind: "lot", at: [404, 432], face: "E", solid: [[368, 418], [428, 418], [434, 430], [428, 440], [374, 440], [366, 430]],
      life: { every: [16, 30], spots: [[292, 436, "W"], [330, 392, "NW"]], stay: [4, 8], when: (g) => !(g.clock && g.clock.now - DAY.rested < 5000) } },     // (not straight up from his prayers: he sits a moment first)
  ],

  // THINGS THAT MOVE BY NATURE (round four: briefs/out/paint-4b-ready.md). Nothing that moves is painted still: the
  // painter took them out of the pictures and marked where they go (layout.json, "fx"), and the engine draws them moving.
  fx: [
    // the builders' village's two threads of cooking smoke, far off under the plateau, bending away with the wind off the river
    { id: "village-smoke-1", type: "smoke", at: [392, 286], base: 296, color: "#f4ecdc", opacity: 0.38, height: 36, width: [1.5, 10], lean: [34, -34], rate: 2 },
    { id: "village-smoke-2", type: "smoke", at: [446, 288], base: 296, color: "#f4ecdc", opacity: 0.38, height: 36, width: [1.5, 10], lean: [34, -34], rate: 2 },
    // rings on the water round the donkey's muzzle while he drinks (kept on the river), and light moving on the Nile,
    // clear of the boat and its reflection and of the reed beds
    { id: "donkey-rings", type: "ripples", at: [155.4, 420], radius: [1.5, 14.1], flat: 0.198, every: [0.8, 1.8], rings: 2, speed: 9, color: "#f2fbf8", trough: "#46809e", opacity: 0.7, clip: NILE },
    { id: "river", type: "shimmer", poly: NILE, holes: [[84, 280, 98, 62], [280, 287, 22, 24], [249, 308, 24, 33], [214, 335, 27, 41]], color: "#fff6e2", opacity: 0.4 },
    // the palms' crowns stirring in the warm wind off the river (their feet stay put), and the papyrus at the front
    { id: "palm-1-crown", type: "sway", plane: "palm-1", anchor: "bottom", at: [190, 400], amount: 1.8, period: 4.5, wave: 300, lean: 0.2 },
    { id: "palm-2-crown", type: "sway", plane: "palm-2", anchor: "bottom", at: [252, 352], amount: 1.3, period: 4.5, wave: 300, lean: 0.2 },
    { id: "palm-3-crown", type: "sway", plane: "palm-3", anchor: "bottom", at: [300, 318], amount: 0.9, period: 4.5, wave: 300, lean: 0.2 },
    { id: "papyrus", type: "sway", plane: "papyrus", anchor: "bottom", amount: 1, period: 3 },
    // now and then a kite or two crossing high over the river and the plateau, behind the palms (the building site's frames)
    { id: "kites", type: "birds", kind: "flyers", lanes: [[[-20, 46], [820, 22]], [[-20, 120], [820, 64]]], every: [18, 40], group: [1, 2], speed: 40, scale: 0.85,
      frames: { dir: "art/scenes/egypt-site/", glide: "kite-0.png", flap: ["kite-1.png", "kite-0.png", "kite-2.png", "kite-0.png"], bank: "kite-3.png", middle: [6.5, 5] } },
  ],

  // Make the picture match the story facts. Runs on arrival and after loading a save: Lot is at his prayers, and the
  // door mirror glints now and then. (And his day goes on: his spells of prayer, lotsDay above.)
  setup(g) {
    pray(g.actor("lot"), true);
    addGlint(g);
    lotsDay(g);
  },

  // The far things first: an area lower in this list lies over the ones above it.
  hotspots: [
    { id: "pyramid", name: "pyramids", poly: [[431, 250], [551, 96], [551, 87], [557, 77], [566, 77], [575, 88], [573, 96], [701, 247], [709, 247], [729, 205], [746, 241], [765, 210], [781, 235], [794, 217], [800, 224], [800, 251]], look: lookAtPyramids },     // the great one and the three small ones beside it
    {
      id: "river", name: "river", verb: "Wade into", poly: [[0, 266], [340, 266], [318, 276], [292, 300], [258, 336], [210, 384], [146, 440], [80, 492], [16, 530], [0, 540]], walkTo: [240, 470], face: "W",
      look: lookAtRiver, use: "egypt.river.use",
    },
    { id: "boat", name: "boat", poly: [[90, 317], [96, 312], [120, 305], [148, 281], [153, 281], [180, 309], [178, 316], [160, 322], [95, 322]], look: twice("egypt.boat.look", "egypt.boat.look2") },     // the hull, the cabin and the rigging
    // the three palms, each its own cut-out (the farthest first: the nearest lies over the others)
    { id: "palm-3", name: "palm tree", plane: "palm-3", poly: [[337,117], [321,125], [313,118], [273,123], [269,145], [261,152], [260,171], [264,178], [256,196], [257,206], [288,205], [297,218], [292,319], [298,323], [307,319], [307,212], [311,207], [325,211], [335,200], [349,205], [351,190], [347,183], [356,179], [353,169], [359,155], [353,150], [355,140]], look: "egypt.palms.look" },
    { id: "palm-2", name: "palm tree", plane: "palm-2", poly: [[240,59], [223,63], [221,71], [207,79], [184,81], [175,89], [180,108], [165,120], [164,128], [173,135], [173,142], [165,155], [162,177], [175,178], [170,184], [171,203], [185,191], [196,192], [212,178], [214,190], [230,193], [236,186], [240,189], [245,242], [241,353], [253,359], [262,351], [252,186], [264,178], [262,168], [274,159], [270,154], [274,148], [290,152], [294,160], [303,154], [297,139], [286,147], [276,140], [279,129], [302,130], [308,124], [315,130], [319,120], [306,108], [304,85], [280,80]], look: "egypt.palms.look" },
    { id: "palm-1", name: "palm tree", plane: "palm-1", poly: [[237,0], [196,0], [184,9], [158,0], [135,27], [132,54], [111,73], [130,88], [115,111], [118,122], [111,134], [122,139], [117,158], [127,162], [124,190], [144,178], [161,156], [166,159], [162,179], [180,177], [188,190], [176,398], [187,409], [203,401], [197,271], [209,151], [191,158], [187,169], [175,158], [187,154], [194,137], [183,144], [179,139], [200,121], [185,122], [184,114], [201,109], [210,115], [208,123], [227,119], [213,101], [196,99], [190,91], [214,82], [226,90], [225,72], [237,63], [247,78], [256,70], [266,85], [286,85], [302,95], [297,101], [275,100], [275,109], [290,103], [300,108], [314,95], [310,80], [317,75], [301,43], [263,28]], look: "egypt.palms.look" },
    { id: "reeds", name: "reeds", verb: "Pick", poly: [[216, 341], [222, 335], [231, 336], [238, 341], [239, 373], [214, 373]], walkTo: [244, 392], face: "W", look: "egypt.reeds.look", use: cutReed },
    { id: "block", name: "dropped block", verb: "Push", poly: [[706, 333], [718, 327], [743, 326], [743, 350], [736, 353], [734, 357], [699, 356], [698, 352], [706, 350]], walkTo: [716, 374], face: "N", look: "egypt.block.look", use: "egypt.block.use" },     // the block and its broken sledge
    {
      id: "footprints", name: "sneaker prints", verb: "Follow", poly: [[468, 496], [498, 496], [510, 460], [514, 420], [512, 380], [506, 340], [502, 318], [474, 318], [474, 350], [480, 390], [480, 430], [472, 462]], walkTo: [424, 502], face: "NE",       // (a step clear of the steam)
      look: "egypt.footprints.look", useWith: { chicken: "egypt.chicken.footprints" },
      // "Then so do I": following them is going up the track (he says so, walks to its foot, and the picture changes)
      use: async (g) => { await g.say("egypt.footprints.use"); await g.walkTo(500, 372); await g.goto("egypt-site", { spawn: "fromCrash" }); },
    },
    {
      // The track itself, a wide band of it: the far end and the whole stretch above the prints, with the sand on either side,
      // so that a click anywhere near it is a click on it. (The top edge of the picture is the way up as well.)
      id: "track", name: "track to the pyramid", verb: "Walk up", poly: [[452, 286], [532, 284], [544, 330], [540, 380], [530, 420], [512, 420], [506, 380], [500, 340], [496, 318], [480, 318], [480, 350], [486, 390], [486, 420], [470, 420], [460, 380], [454, 330]], walkTo: [500, 372], face: "N",       // he is on his way up it when the picture changes
      look: "egypt.track.look", use: (g) => g.goto("egypt-site", { spawn: "fromCrash" }),
    },
    {
      id: "donkey", name: "donkey", verb: "Pat", plane: "donkey", walkTo: [244, 440], face: "W",       // (just past its rump, so that he does not hide it)
      poly: [[205, 365], [205, 368], [180, 375], [175, 381], [161, 382], [161, 384], [155, 385], [156, 392], [162, 400], [158, 404], [158, 408], [153, 417], [154, 422], [159, 422], [160, 420], [220, 419], [220, 408], [222, 404], [226, 403], [227, 401], [226, 384], [223, 378], [215, 374], [210, 369], [212, 366], [210, 365]],
      look: twice("egypt.donkey.look", "egypt.donkey.look2"), use: "egypt.donkey.use",
      useWith: { sunglasses: "egypt.donkey.sunglasses" },
    },
    // Lot: a stranger on the screen until he has said who he is (one shape, one of the two showing at a time)
    { ...LOT, name: "herdsman", when: (g) => !g.flag("egypt.knowsLot") },
    { ...LOT, name: "Lot", when: (g) => !!g.flag("egypt.knowsLot") },
    atCar({
      id: "wagon", name: "wagon", verb: "Start", plane: "wagon", walkTo: [604, 563], face: "N", look: "egypt.wagon.look", use: "egypt.wagon.try",
      poly: [[455, 494], [505, 480], [553, 473], [557, 469], [572, 443], [580, 437], [592, 432], [760, 433], [775, 463], [782, 500], [786, 508], [783, 514], [747, 518], [744, 531], [732, 539], [705, 540], [693, 531], [640, 530], [622, 533], [611, 525], [600, 521], [580, 513], [566, 507], [531, 504], [470, 499]],     // the car, up to its roof rack (not the sand heaped at its nose)
    }),
    atCar({
      id: "hood", name: "hood", verb: "Open", poly: [[455, 494], [480, 486], [505, 480], [553, 473], [562, 480], [580, 489], [586, 497], [566, 506], [531, 504], [500, 501], [470, 499]], walkTo: [566, 563], face: "N",
      look: twice("egypt.hood.look", "egypt.hood.look2"), use: "egypt.hood.use",
      useWith: { flashlight: (g) => g.say(g.flag("egypt.knowsLight") ? "egypt.flash.dead" : "egypt.hood.flashlight"), rootbeer: "egypt.hood.rootbeer" },
    }),
    atCar({
      id: "glovebox", name: "glovebox", verb: "Search", poly: [[621, 488], [627, 463], [656, 458], [659, 483]], walkTo: [642, 563], face: "N",       // through the driver's window
      look: (g) => g.say(g.flag("egypt.hasMap") ? "egypt.wagon.empty" : "egypt.glovebox.look"), use: searchGlovebox,
    }),
    ...lidded({ id: "suitcase", name: "suitcase", verb: "Open", walkTo: [648, 563], face: "N", look: nearCar((g) => g.say(g.flag("egypt.suitcaseOpen") ? "egypt.suitcase.open" : "egypt.suitcase.look")), use: nearCar(searchSuitcase) },
      "egypt.suitcaseOpen", [[600, 434], [599, 419], [648, 413], [651, 426], [671, 438], [671, 440], [621, 446]], [[586, 381], [639, 375], [670, 424], [672, 441], [656, 451], [620, 447], [600, 434]]),
    ...lidded({ id: "trunk", name: "trunk", verb: "Open", walkTo: [692, 563], face: "N", look: nearCar((g) => (g.flag("egypt.trunkOpen") ? twice("egypt.trunk.cables", "egypt.trunk.chair")(g) : g.say("egypt.trunk.look"))), use: nearCar(searchTrunk) },
      "egypt.trunkOpen", [[651, 426], [647, 395], [693, 389], [709, 399], [701, 400], [706, 422], [723, 433], [724, 436], [678, 442]], [[632, 348], [678, 342], [683, 344], [721, 406], [724, 437], [677, 442], [650, 425], [643, 404]]),
    ...lidded({ id: "cooler", name: "cooler", verb: "Open", walkTo: [730, 563], face: "N", look: nearCar("egypt.cooler.look"), use: nearCar(searchCooler) },
      "egypt.coolerOpen", [[701, 400], [730, 396], [748, 407], [749, 429], [723, 433], [706, 422]], [[701, 399], [720, 388], [732, 390], [750, 401], [761, 428], [744, 436], [721, 433], [705, 423]]),
    atCar({
      id: "mirror", name: "door mirror", verb: "Take", plane: "mirror", poly: [[618, 485], [618, 487], [625, 492], [630, 492], [635, 489], [635, 484], [629, 480], [624, 481]], walkTo: [622, 563], face: "N", when: (g) => !g.flag("egypt.tookMirror"),
      look: "egypt.mirror.look", use: takeMirror,
    }),
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

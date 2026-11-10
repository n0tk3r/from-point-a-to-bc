// Act Six, the fourth leg: the Akashi shore, afternoon (SCENES-21C: new in round twenty-one, in place of ENGINE-21's stub;
// briefs/SCENES-21.md, and the design, briefs/out/edo2-design.md, "THE AKASHI SHORE" and #35). White sand and shore pines, the
// strait running hard to Awaji, Akashi's castle with no keep on its hill at the far left; octopus pots stacked on the sand,
// old Heita's boat drawn up and his tub; out in the shallows the pots' lines and floats, and among them, floating, a ladle
// with an octopus in it; an Awa pilgrim boat in the strait, sail down, its people wading ashore with their ladles held high.
//
// The three of them come here by the walk card ("Three days later" / "Akashi": SCENES-21B's edo-walk.js) at the mark `road`,
// on the Saigoku-kaidō behind the pines (from the east: the left). The leg's start is LEG_START.akashi (edo-common.js).
//
//   arriving    once: Little Sister sees the sea and "a boat full of spoons"; two Awa pilgrims wade ashore ("Mind the pots!",
//               "Ladles up!") and join their group by Heita's boat; Mom sees the little one crying (edo.akashiSeen)
//   #35 The Ladle
//     O-Fusa    fusaTree (talk/edo-d.js): she lost her ladle wading in (edo.fusaMet). Little Sister's boots are for water:
//               her use of the shallows, or of the ladle, is the wade (AKASHI.wade: edo.waded; she is dressed `edo-wading`
//               while her feet are in the shallows, which are hers alone: the scene's `zones`)
//     the pull  her use of the ladle while the octopus has it (AKASHI.pull; the first time Heita's clue and Big Sister's
//               gloss: edo.crabClue, edo.tako); Heita's tree gives the clue too
//     the crab  Mom's use of the rocks after the clue (AKASHI.crab: the crab into her pockets, edo.crab); handed to Little
//               Sister; her crab on the ladle is the swap (AKASHI.swap): the octopus lets go, the crab gets away, the ladle is
//               hers (edo.ladleFree), and Heita comes down to the water's edge and lifts the octopus, for his supper
//     the ladle back   fusaTree's `back` (by whoever has it): her slip for Shosha and Little Sister's penny for luck
//               (`fusaslip`; two pennies become one: `lastpenny`; edo.ladleBack: the beat)
//     the news  O-Sato and her sister-in-law on the road (satoTree, optional): the hall at Shosha still shut, O-Ume's rice
//               balls, the shipwright, "it opens to what a ship gives its lady" (edo.riddle)
//   the road    east refuses always (AKASHI.east); west refuses until the ladle is back (AKASHI.west), then "West, girls."
//               and the card "The next day" (cutscenes/edo-walk2.js: the beat edo.walk2)
//
// The octopus in the floating ladle is a small drawing of the scene's (PEOPLE-21B has the octopus only as a thing held: in
// Little Sister's ladle, in Heita's fist): a few pixels in the ladle's bowl, at PAINT-21D's `octopus` point. The Awa boat
// stays coming in (its `beached` state is not shown: ready.md); the komusō passes along the road now and then (a `passer`).
//
// Every place is the painter's measurement (art/scenes/edo-akashi/layout.json, PAINT-21D's ready.md), or set by eye against
// the picture with the people in it; where the two differ the comment says why.
//
// Try it: index.html?scene=edo-akashi&lead=lilsis&flags=edo.walked   (LEG_START.akashi's pockets and clothes: the play sets them)

import { STOCK_DRESSED } from "./edo-common.js";
import { THREE, who, is, heard, each, inside, standsIn, giveTo, takeAny, swapItem, dressAll, thingOf, faceEach, idle, chatter, swap, TALK } from "./edo-west.js";
import { fusaTree, leaderTree, heitaTree, satoTree, AKASHI } from "../talk/edo-d.js";

const art = "art/scenes/edo-akashi/";

// ---------- the camera and the ground (layout.json: persp.Camera(262, 590)) ----------
const HORIZON = 262, FULL = 590;
// The sand (the painter's `walk`) and the shallows (`walk_floors.shallows`) share no pixel: one floor here, the sand's water's
// edge between (544, 459) and (347, 428) carried out round the shallows, so that Little Sister can wade in by a click; the
// shallows are then a zone of that floor for her alone (`zones`). Nobody else stands in the water.
const SAND = [[797, 596], [797, 493], [718, 484], [627, 472], [544, 459], [471, 447], [405, 437], [347, 428], [294, 420], [249, 409], [212, 399],
  [180, 390], [155, 380], [141, 369], [129, 360], [119, 352], [110, 345], [106, 339], [104, 333], [2, 357], [2, 596]];
const SHALLOWS = [[372, 428], [394, 431], [417, 435], [440, 438], [465, 442], [490, 446], [517, 451], [545, 455], [533, 438], [487, 428], [427, 427], [374, 418]];
const FLOOR = [[797, 596], [797, 493], [718, 484], [627, 472], [544, 459], [545, 455], [533, 438], [487, 428], [427, 427], [374, 418], [372, 428],
  [347, 428], [294, 420], [249, 409], [212, 399], [180, 390], [155, 380], [141, 369], [129, 360], [119, 352], [110, 345], [106, 339], [104, 333], [2, 357], [2, 596]];

// ---------- the marks (layout.json marks) ----------
const M = { road: [108, 570], shore: [411, 451], fusa: [380, 437], leader: [294, 426], pots: [164, 527], heita: [295, 444], tub: [316, 464],
  shallows: [451, 445], ladle: [462, 435], rocks: [612, 516], sato: [299, 565], west: [770, 569], satosister: [352, 568],
  road_mom: [115, 572], road_bigsis: [87, 558], road_lilsis: [143, 585], shoreLeft: [79, 468] };
const OCTOPUS = [461, 430];                                  // layout.json `octopus`: in the ladle's bowl
// The Awa pilgrims: wading in (layout.json places, in the water, on no floor), then ashore with their group on the strip of sand
// between the water and Heita's boat (set by eye: behind the boat, beside their leader).
const WADE = { awapilgrim1: [376, 403], awapilgrim2: [429, 410] };
const EDGE = { awapilgrim1: [356, 425], awapilgrim2: [346, 423] };       // where each comes up out of the water
const ASHORE = { awapilgrim1: [258, 417], awapilgrim2: [234, 409] };
const HEITA_EDGE = [426, 447];          // Heita at the water's edge for his octopus (the sand, beside the shallows)
const BY_FUSA = [404, 441];             // Little Sister beside O-Fusa, when somebody else gives the ladle back
const TALK_AT = { leader: [320, 438], heita: [338, 444], sato: [246, 570], ashore: [318, 437] };

// ---------- the story, as the picture shows it ----------
const seen = (g) => is(g, "edo.akashiSeen");                // the pilgrims ashore (the arrival played)
const free = (g) => is(g, "edo.ladleFree");                  // the ladle off the octopus, in Little Sister's hands
const room = { lifted: false, wading: false, waves: false, komuso: false };

// ---------- the octopus in the ladle (a drawing of the scene's: a few pixels, in the people's colours) ----------
const OCTO = { L: "#e8a494", M: "#c06c5c", D: "#8c463e", O: "#5a2a26", E: "#160c0a" };
const OCTO_ROWS = ["...OOO...", "..OLLMO..", ".OLLMMDO.", ".OMEMEDO.", "..OMMDO..", "OMMOMOMMO", "M..D.D..M", "D.......D"];
let octoPicture = null;
function octopusPic() {
  if (octoPicture) return octoPicture;
  const c = document.createElement("canvas");
  c.width = OCTO_ROWS[0].length; c.height = OCTO_ROWS.length;
  const x = c.getContext("2d");
  OCTO_ROWS.forEach((row, j) => [...row].forEach((ch, i) => { if (OCTO[ch]) { x.fillStyle = OCTO[ch]; x.fillRect(i, j, 1, 1); } }));
  octoPicture = { canvas: c, ox: 4, oy: 6 };              // its arms over the bowl's rim at the point
  return octoPicture;
}
/** The octopus in the floating ladle, while it floats and nobody has lifted it. */
function octopus(g) {
  const want = !free(g) && !room.lifted;
  if (!want) { g.hand("octopus", null); return; }
  if (!g.hands().some((h) => h.id === "octopus")) g.hand("octopus", OCTOPUS, { draw: () => octopusPic(), plane: "floor", base: OCTOPUS[1] - 1 });
}
/** The ladle lifted out of the water by Little Sister (her hold shows it), or put back. */
function lift(g, up) {
  room.lifted = up;
  const p = g.plane("ladle");
  if (p) p.show(!up && !free(g));
  octopus(g);
}

// ---------- arriving: the two pilgrims wade ashore ----------
async function wadeAshore(g, id, delay) {
  const f = g.actor(id);
  if (!f) return;
  await g.wait(delay);
  await g.moveTo(EDGE[id][0], EDGE[id][1], id);
  const a = swap(g, id, `${id}-ashore`, EDGE[id], "W");
  await g.view.cast.load();
  await g.moveTo(ASHORE[id][0], ASHORE[id][1], id);
  if (g.actor(id)) g.actor(id).face("E");
  return a;
}
async function arrive(g) {
  const going = Promise.all([wadeAshore(g, "awapilgrim1", 600), wadeAshore(g, "awapilgrim2", 2600)]);
  await g.wait(500);
  await g.say(AKASHI.arrive[0]);
  await g.say("edo.akashi.awapilgrim1.say");
  await g.say(AKASHI.arrive[1]);
  await g.say("edo.akashi.awapilgrim2.say");
  await going;
  const lil = g.actor("lilsis"), fusa = g.actor("fusa");
  for (const id of THREE) { const a = g.actor(id); if (a && fusa) a.look(fusa.x, fusa.y); }
  await g.say(AKASHI.arrive[2]);
  if (lil) lil.look(M.fusa[0], M.fusa[1]);
  g.flag("edo.akashiSeen", true);
}

// ---------- #35: into the water ----------
/** Little Sister wades in (her use of the shallows or of the ladle, or her own walk into the water): "Boots are for WATER." */
async function wade(g, walk = true) {
  const lil = g.actor("lilsis");
  if (!lil) return;
  if (walk && !standsIn(SHALLOWS, lil)) {
    lil.face("N");
    await g.say(AKASHI.wade[0]);
    await g.walkTo(M.ladle[0], M.ladle[1], "lilsis");
  } else await g.say(AKASHI.wade[0]);
  if (g.dressOf("lilsis") !== "edo-wading") g.dress("lilsis", "edo-wading");
  lil.face("N");
  g.sfx("splash");
  const big = g.actor("bigsis");
  if (big) big.look(lil.x, lil.y);
  await g.say(AKASHI.wade[1]);
  g.flag("edo.waded", true);
  await g.say(AKASHI.wade[2]);
}
/** Little Sister to the ladle, through the water (in it already, or wading in). */
async function toLadle(g) {
  const lil = g.actor("lilsis");
  if (!lil) return;
  if (Math.hypot(lil.x - M.ladle[0], lil.y - M.ladle[1]) > 4) await g.walkTo(M.ladle[0], M.ladle[1], "lilsis");
  if (g.dressOf("lilsis") !== "edo-wading") g.dress("lilsis", "edo-wading");
  lil.face("SW");                                              // (turned to the shore with it: the ladle and its passenger seen)
}
/** Her use of the ladle while the octopus has it: she lifts it, it holds on ("Let GO, octopus."); the first time Heita says
    what it lets go for, from his boat, and Big Sister says what "tako" is. Then it goes back on the water. */
async function pull(g) {
  await toLadle(g);
  const lil = g.actor("lilsis");
  lift(g, true);
  lil.hold(true, "ladleocto");
  try {
    if (!heard(g, AKASHI.pull[0])) {
      await g.say(AKASHI.pull[0]);
      g.sfx("octopus");
      if (!is(g, "edo.crabClue")) { const h = g.actor("heita"); if (h) h.look(lil.x, lil.y); await g.say(AKASHI.pull[1]); g.flag("edo.crabClue", true); }
      if (!is(g, "edo.tako")) { await g.say(AKASHI.pull[2]); g.flag("edo.tako", true); }
    } else {
      g.sfx("octopus");
      await g.say("edo.akashi.ladlething.octopus.use.lilsis");
    }
  } finally {
    lil.hold(false);
    lift(g, false);
  }
}
/** Little Sister's crab, held out to the octopus in the ladle: it lets go of the ladle for the crab, the crab gets away, the
    ladle is hers; Heita, who has come down to the water's edge, lifts the octopus for his supper and goes back to his boat. */
async function swapCrab(g) {
  await toLadle(g);
  const lil = g.actor("lilsis");
  lift(g, true);
  lil.hold(true, "ladlecrab");
  // Heita gets up and comes down to the water's edge while she offers it
  const coming = (async () => {
    swap(g, "heita", "heita-standing", M.heita, "E");
    await g.view.cast.load();
    await g.moveTo(HEITA_EDGE[0], HEITA_EDGE[1], "heita");
    const h = g.actor("heita");
    if (h) h.look(lil.x, lil.y);
  })();
  await g.say(AKASHI.swap[0]);
  g.sfx("octopus");
  await coming;
  takeAny(g, "crab");
  g.give("ladle");
  g.sfx("pickup");
  lil.hold(true, "ladle");
  g.flag("edo.ladleFree", true);
  await g.say(AKASHI.swap[1], AKASHI.swap[2]);
  const h = g.actor("heita");
  if (h) { await h.play(g.clock, "reach"); h.hold(true, "octopus"); }
  await g.say(AKASHI.swap[3]);
  lil.hold(false);
  room.lifted = false;
  octopus(g);
  // back to his boat, the octopus into his tub, and down again; Little Sister out of the water with the ladle
  await Promise.all([
    (async () => { if (h) { await g.moveTo(M.tub[0] + 6, M.heita[1] + 2, "heita"); h.hold(false); g.sfx("splash"); } const s = swap(g, "heita", "heita", M.heita, "E"); await g.view.cast.load(); return s; })(),
    (async () => { await g.walkTo(M.shallows[0], M.shallows[1], "lilsis"); dressLil(g); const l = g.actor("lilsis"); if (l) l.look(M.fusa[0], M.fusa[1]); })(),
  ]);
}

// ---------- #35: the crab ----------
async function rocksUse(g) {
  const me = who(g);
  if (me !== "mom") return g.say(`edo.akashi.rocks.use.${me}`);
  if (is(g, "edo.crab")) return g.say(AKASHI.crabAgain);
  if (!is(g, "edo.crabClue")) return g.say("edo.akashi.rocks.use.mom");
  const mom = g.lead;
  mom.face("E");
  await g.say(AKASHI.crab[0]);
  await g.reach(true);
  g.sfx("splash");
  g.give("crab");
  g.flag("edo.crab", true);
  mom.hold(true, "crab");
  try {
    await g.say(AKASHI.crab[1]);
    const big = g.actor("bigsis");
    if (big) big.look(mom.x, mom.y);
    await g.say(AKASHI.crab[2]);
  } finally { mom.hold(false); }
}

// ---------- the ladle, afloat ----------
const ladleLook = (g) => g.say(is(g, "edo.waded") ? `edo.akashi.ladlething.octopus.${who(g)}` : `edo.akashi.ladlething.${who(g)}`);
function ladleUse(g) {
  const me = who(g);
  if (me === "lilsis") return is(g, "edo.waded") ? pull(g) : wade(g);
  return g.say(is(g, "edo.waded") ? `edo.akashi.ladlething.octopus.use.${me}` : `edo.akashi.ladlething.use.${me}`);
}
const ladleWith = {
  crab: (g) => (who(g) === "lilsis" ? swapCrab(g) : g.say(`edo.akashi.ladlething.with.crab.${who(g)}`)),
  twopennies: { lilsis: "edo.akashi.ladlething.with.twopennies.lilsis" },
  lastpenny: { lilsis: "edo.akashi.ladlething.with.lastpenny.lilsis" },
  lilflash: { lilsis: "edo.akashi.ladlething.with.lilflash.lilsis" },
};
/** The water's edge: Little Sister's use is the wade (and, once in, back to the ladle); the others' theirs. */
function shallowsUse(g) {
  if (who(g) !== "lilsis") return g.say(`edo.akashi.shallows.use.${who(g)}`);
  if (!is(g, "edo.waded")) return wade(g);
  return toLadle(g);
}
/** Little Sister in O-Tami's clothes as the water has her: wading while her feet are in the shallows. */
function dressLil(g) {
  const lil = g.actor("lilsis"), now = g.dressOf("lilsis");
  if (!lil || !(now === "edo" || now === "edo-wading" || now === "edo-hatback" || now == null)) return;
  const want = standsIn(SHALLOWS, lil, 1) ? "edo-wading" : "edo";
  if (now !== want) g.dress("lilsis", want);
}

// ---------- the people's talks ----------
/** The ladle given back to O-Fusa by whoever has it: Little Sister beside her if she is not the one. */
async function giveLadle(g) {
  const me = who(g), fusa = g.actor("fusa");
  const lilComes = me !== "lilsis" ? g.walkTo(BY_FUSA[0], BY_FUSA[1], "lilsis").then(() => faceEach(g, "lilsis", "fusa")) : null;
  faceEach(g, g.lead, "fusa");
  await g.reach();
  takeAny(g, "ladle");
  g.sfx("pickup");
  swap(g, "fusa", "fusa-ladle", M.fusa, fusa ? fusa.yaw : "S");
  await g.view.cast.load();
  if (lilComes) await lilComes;
}
/** Her name slip, for the women's hall at Shosha, into Little Sister's hands (she promised). */
async function giveSlip(g) {
  const f = g.actor("fusa"), lil = g.actor("lilsis");
  if (f) f.hold(true, "slip");
  await g.wait(500);
  if (f) f.hold(false);
  giveTo(g, "lilsis", "fusaslip");
  g.sfx("pickup");
  if (lil) { lil.hold(true, "slip"); await g.wait(500); lil.hold(false); }
}
/** Little Sister's penny, for luck: two pennies become one. */
async function givePenny(g) {
  const lil = g.actor("lilsis");
  if (lil) lil.hold(true, "coinout");
  swapItem(g, "lilsis", "twopennies", "lastpenny");
  g.sfx("pickup");
  await g.wait(400);
  if (lil) lil.hold(false);
}
const FUSA = fusaTree({ giveLadle, giveSlip, givePenny });
const LEADER = leaderTree();
const HEITA = heitaTree();
const SATO = satoTree();
async function talkTo(g, id, tree) {
  const a = g.actor(id), lead = g.lead;
  if (a && lead) a.look(lead.x, lead.y);
  await g.talk(tree);
}
/** Little Sister's first look at the pots: Heita, from his boat, has his say. */
async function potsLook(g) {
  await g.say(`edo.akashi.pots.${who(g)}`);
  if (who(g) === "lilsis" && !heard(g, AKASHI.pots)) await g.say(AKASHI.pots);
}

// ---------- the road ----------
const eastUse = (g) => g.say(AKASHI.east[who(g)]);
async function westUse(g) {
  if (!is(g, "edo.ladleBack")) return g.say(AKASHI.west[who(g)]);
  await g.say(AKASHI.westGo);
  await g.cutscene("edo-walk2");
}

// ---------- life ----------
const CHAT = chatter([
  { when: (g) => seen(g) && !is(g, "edo.ladleBack"), say: ["edo.akashi.awapilgrim2.say"] },
  { when: (g) => seen(g) && !is(g, "edo.ladleBack") && heard(g, "edo.akashi.leader.count"), say: ["edo.akashi.leader.count"] },
], { first: [30, 40], every: [50, 80] });

// ---------- the scene ----------
const thing = thingOf("akashi");
const rect = (r) => ({ rect: r });
const poly = (p) => ({ poly: p });
// People's areas: a box round each, where they stand (set against their figures at the painter's marks)
const BOX = { fusa: [369, 376, 22, 61], leader: [281, 355, 26, 44], heita: [281, 400, 30, 45], sato: [277, 442, 44, 123], satosister: [330, 443, 45, 125],
  wade1: [365, 342, 22, 61], wade2: [418, 350, 22, 60], ashore1: [247, 352, 22, 65], ashore2: [224, 351, 21, 58] };

export default {
  id: "edo-akashi",
  era: "edo",
  name: "The Akashi shore",

  horizon: HORIZON, full: FULL,
  walk: { area: FLOOR },
  // the pots, Heita's boat, his tub, the rocks, the two pines' roots (layout.json blocked)
  blocked: [[[45, 522], [291, 522], [310, 477], [106, 477]], [[75, 419], [306, 429], [276, 448], [22, 436]], [[287, 460], [347, 460], [350, 448], [294, 448]],
    [[614, 510], [856, 510], [801, 480], [588, 480]], [[37, 543], [90, 543], [103, 531], [52, 531]], [[703, 540], [755, 540], [741, 529], [690, 529]]],
  // ENGINE-21: the shallows are Little Sister's alone (her yellow boots); the others stop at the water's edge and say why
  zones: [{ area: SHALLOWS, leads: ["lilsis"], no: { mom: "edo.akashi.shallows.use.mom", bigsis: "edo.akashi.shallows.use.bigsis" } }],

  party: THREE,
  spawn: { default: M.road, ...M },
  // Off the walk card, onto the road behind the pines (the painter's road_* marks for the two who do not lead)
  arrive: { road: [M.road_bigsis, M.road_lilsis] },
  facing: "E",
  stock: STOCK_DRESSED,
  talk: TALK,
  edges: {
    W: { name: "back east", walkTo: [14, 576], use: eastUse },
    E: { name: "west, toward Himeji", walkTo: [788, 574], use: westUse },
  },
  tick(g, dt) {
    if (!room.waves && g.loop("waves", { level: 0.8 })) room.waves = true;
    dressLil(g);
    const lil = g.actor("lilsis");
    if (lil && !is(g, "edo.waded") && !room.wading && idle(g) && standsIn(SHALLOWS, lil) && who(g) === "lilsis") {
      room.wading = true;
      g.run(() => wade(g, false)).finally(() => { room.wading = false; });
    }
    const k = g.effects.get("komuso");
    if (k && k.on && !room.komuso) { room.komuso = true; if (idle(g)) g.sfx("komuso"); }
    if (k && !k.on) room.komuso = false;
    if (seen(g)) CHAT.tick(g, dt);
  },

  picture: art + "back.png",
  // CUT-OUTS, back to front (the painter's plan): the floats and the ladle on the water (behind everybody), the Awa boat in the
  // strait (it stays coming in: ready.md), Heita's boat (whoever is beyond it is behind it), his tub, the pots, the rocks, the
  // two shore pines, and the grass tufts in front.
  planes: [
    { id: "floats", src: art + "floats.png", plane: "back" },
    { id: "ladle", plane: "back", states: { afloat: art + "ladle.png" }, state: "afloat", when: (g) => !free(g) && !room.lifted },
    { id: "pilgrimboat", base: 366, states: { "coming in": art + "pilgrimboat.png", beached: art + "pilgrimboat-beached.png" }, state: "coming in" },
    { id: "heitaboat", src: art + "heitaboat.png", base: [[47, 428], [276, 439]] },
    { id: "tub", src: art + "tub.png", base: 450 },
    { id: "pots", src: art + "pots.png", base: 515 },
    { id: "rocks", src: art + "rocks.png", base: 506 },
    { id: "pine-l", src: art + "pine-l.png", base: 537 },
    { id: "pine-r", src: art + "pine-r.png", base: 535 },
    { id: "front", src: art + "front.png", plane: "front" },
    { id: "near", src: art + "near.png", plane: "front" },
  ],

  // THINGS THAT MOVE BY NATURE (layout.json fx): the little waves running in at the water's edge, the sun on the strait, the two
  // pines stirring, the ladle and the floats and the boat riding the water, gulls; and the komusō passing along the road now and
  // then, going west as they are (ENGINE-21's `passer`). (The painter's proposed boat-approach is not used: no flyer that stops.)
  fx: [
    { id: "shore-waves", type: "waves", area: [[107, 332], [109, 339], [116, 346], [127, 354], [140, 364], [156, 376], [183, 387], [221, 398], [265, 410], [321, 420], [384, 430], [456, 441], [539, 454], [633, 467], [738, 481], [797, 487], [797, 465], [746, 439], [664, 433], [584, 424], [511, 416], [446, 407], [387, 400], [334, 393], [287, 386], [248, 377], [214, 370], [188, 361], [170, 352], [156, 345], [144, 338], [135, 332], [131, 326]],
      holes: [[[452, 424], [486, 424], [486, 439], [452, 439]], [[309, 213], [425, 213], [425, 369], [309, 369]]], rows: 6, per: 9, color: "#f6eed8", opacity: 0.55, size: 9, speed: 7, toward: "S", life: 3.0, plane: "back" },
    { id: "strait-shimmer", type: "shimmer", poly: [[260, 266], [800, 264], [800, 330], [300, 320]], count: 34, size: 5, flow: [-6, 0], life: 1.6, color: "#f6eed8", opacity: 0.55, plane: "back" },
    { id: "pine-l-sway", type: "sway", plane: "pine-l", anchor: "bottom", amount: 1.2, period: 5.5, wave: 40, lean: 0.3 },
    { id: "pine-r-sway", type: "sway", plane: "pine-r", anchor: "bottom", amount: 1.0, period: 6.0, wave: 40, lean: 0.3 },
    { id: "ladle-bob", type: "bob", plane: "ladle", amount: 0.5, period: 4.0 },
    { id: "floats-bob", type: "bob", plane: "floats", amount: 1, period: 4.5 },
    { id: "boat-bob", type: "bob", plane: "pilgrimboat", amount: 1, period: 5.5, tilt: 0.8 },
    { id: "gulls", type: "birds", plane: "back", lanes: [[[-12, 200], [180, 186], [360, 204], [560, 180], [812, 196]], [[812, 150], [600, 170], [420, 152], [200, 176], [-12, 160]]], every: [8, 16], group: [1, 3], speed: 55, size: 8, scale: [0.6, 1.0], color: "#f6eed8" },
    { id: "komuso", type: "passer", kind: "komuso", path: [[-40, 586], [840, 582]], every: [55, 95], both: false, area: "komuso" },
  ],

  // The people: O-Fusa in tears at the water's edge (then her ladle held up), her group's leader with the banner, old Heita
  // mending a line by his boat, O-Sato and her sister-in-law stopped on the road, and two Awa pilgrims, wading in, then ashore.
  actors: [
    { id: "fusa", kind: "fusa", at: M.fusa, face: "S", when: (g) => !is(g, "edo.ladleBack"), life: { fidget: [4, 9], still: true } },
    { id: "fusa", kind: "fusa-ladle", at: M.fusa, face: "S", when: (g) => is(g, "edo.ladleBack"), life: { fidget: [4, 9], still: true } },
    { id: "leader", kind: "leader", at: M.leader, face: "S", life: { fidget: [6, 11], still: true } },
    { id: "heita", kind: "heita", at: M.heita, face: "E", life: { fidget: [5, 10], still: true } },
    { id: "sato", kind: "sato", at: M.sato, face: "W", life: { fidget: [6, 12], still: true } },
    { id: "satosister", kind: "satosister", at: M.satosister, face: "W", life: { fidget: [6, 12], still: true } },
    { id: "awapilgrim1", kind: "awapilgrim1", at: WADE.awapilgrim1, face: "S", when: (g) => !seen(g), solid: false, life: { fidget: false } },
    { id: "awapilgrim2", kind: "awapilgrim2", at: WADE.awapilgrim2, face: "S", when: (g) => !seen(g), solid: false, life: { fidget: false } },
    { id: "awapilgrim1", kind: "awapilgrim1-ashore", at: ASHORE.awapilgrim1, face: "E", when: seen, life: { fidget: [7, 13], still: true } },
    { id: "awapilgrim2", kind: "awapilgrim2-ashore", at: ASHORE.awapilgrim2, face: "E", when: seen, life: { fidget: [7, 13], still: true } },
  ],

  // Back to front: a later area lies over an earlier one (layout.json things; the people's boxes against their figures).
  hotspots: [
    thing("awaji", "Awaji", poly([[212, 262], [236, 258], [320, 248], [440, 238], [560, 236], [690, 234], [797, 226], [797, 263], [212, 263]]), M.shore, "N"),
    thing("strait", "strait", poly([[160, 263], [797, 263], [797, 480], [600, 470], [420, 436], [300, 418], [200, 398], [140, 380], [100, 330]]), M.shore, "N"),
    thing("pilgrimboat", "pilgrim boat", rect([308, 212, 118, 158]), M.shore, "N", { plane: "pilgrimboat" }),
    thing("potlines", "lines of floats", poly([[296, 396], [574, 445], [578, 440], [313, 392]]), M.shallows, "N"),
    thing("pilgrims", "pilgrims", rect([336, 340, 110, 80]), M.shore, "N", { when: (g) => !seen(g) }),
    thing("pilgrims", "pilgrims", rect([222, 352, 52, 66]), TALK_AT.ashore, "W", { when: seen }),
    // the sand and the road: a patch of each, so that a click elsewhere on them walks (the edges' bands are clear of the road's)
    thing("sand", "white sand", poly([[440, 490], [580, 492], [580, 526], [440, 522]]), [510, 532], "S"),
    thing("road", "road", poly([[60, 578], [740, 578], [740, 597], [60, 597]]), M.sato, "W"),
    thing("pots", "octopus pots", rect([79, 446, 221, 76]), M.pots, "N", { plane: "pots", look: potsLook }),
    thing("heitaboat", "fishing boat", rect([37, 393, 250, 48]), TALK_AT.heita, "W", { plane: "heitaboat" }),
    thing("tub", "tub", rect([298, 430, 44, 30]), M.tub, "N", { plane: "tub" }),
    thing("rocks", "rocks", rect([600, 461, 200, 46]), M.rocks, "E", { plane: "rocks", use: rocksUse }),
    // the two shore pines, by their crowns and trunks (the painter's one shape covered the rocks and the strait)
    thing("pines", "shore pines", poly([[0, 30], [250, 22], [372, 110], [300, 178], [196, 176], [120, 520], [62, 540], [0, 540]]), M.road, "N", { plane: "pine-l" }),
    { id: "pines2", name: "shore pines", poly: [[460, 40], [700, 16], [800, 40], [800, 210], [690, 190], [728, 528], [700, 540], [612, 170], [470, 200]], walkTo: M.west, face: "N",
      plane: "pine-r", look: each("edo.akashi.pines"), use: each("edo.akashi.pines.use") },
    // the castle on its hill, in the gap between the left pine's crowns (over the pine's shape)
    thing("castle", "castle", rect([2, 201, 74, 30]), M.shoreLeft, "N"),
    // the water's edge, where wading starts: Little Sister's way in (the zone)
    { id: "shallows", name: "shallows", verb: "Wade into", poly: SHALLOWS, walkTo: M.shallows, face: "N", look: each("edo.akashi.shallows"), use: shallowsUse },
    { id: "ladlething", name: "ladle", poly: [[450, 422], [488, 422], [488, 441], [450, 441]], walkTo: M.shallows, face: "N", when: (g) => !free(g),
      look: ladleLook, use: ladleUse, useWith: ladleWith },
    // the people
    { id: "awapilgrim1", name: "Awa pilgrim", rect: BOX.wade1, walkTo: M.shore, face: "N", when: (g) => !seen(g), look: each("edo.akashi.awapilgrim1"), use: each("edo.akashi.awapilgrim1.use") },
    { id: "awapilgrim2", name: "Awa pilgrim", rect: BOX.wade2, walkTo: M.shore, face: "N", when: (g) => !seen(g), look: each("edo.akashi.awapilgrim2"), use: each("edo.akashi.awapilgrim2.use") },
    { id: "awapilgrim1", name: "Awa pilgrim", rect: BOX.ashore1, walkTo: TALK_AT.ashore, face: "W", when: seen, look: each("edo.akashi.awapilgrim1"), use: each("edo.akashi.awapilgrim1.use") },
    { id: "awapilgrim2", name: "Awa pilgrim", rect: BOX.ashore2, walkTo: TALK_AT.ashore, face: "W", when: seen, look: each("edo.akashi.awapilgrim2"), use: each("edo.akashi.awapilgrim2.use") },
    { id: "leader", name: "group leader", verb: "Talk to", rect: BOX.leader, walkTo: TALK_AT.leader, face: "W", look: each("edo.akashi.leader"), use: (g) => talkTo(g, "leader", LEADER) },
    thing("banner", "banner", rect([280, 306, 30, 52]), TALK_AT.leader, "W"),
    { id: "heita", name: "Heita", verb: "Talk to", rect: BOX.heita, walkTo: TALK_AT.heita, face: "W", look: each("edo.akashi.heita"), use: (g) => talkTo(g, "heita", HEITA) },
    { id: "fusa", name: "O-Fusa", verb: "Talk to", rect: BOX.fusa, walkTo: M.shore, face: "W",
      look: (g) => g.say(is(g, "edo.ladleBack") ? `edo.akashi.fusa.after.${who(g)}` : `edo.akashi.fusa.${who(g)}`), use: (g) => talkTo(g, "fusa", FUSA),
      useWith: { ladle: (g) => talkTo(g, "fusa", FUSA) } },
    { id: "sato", name: "O-Sato", verb: "Talk to", rect: BOX.sato, walkTo: TALK_AT.sato, face: "E", look: each("edo.akashi.sato"), use: (g) => talkTo(g, "sato", SATO) },
    { id: "satosister", name: "her sister-in-law", verb: "Talk to", rect: BOX.satosister, walkTo: TALK_AT.sato, face: "E", look: each("edo.akashi.satosister"), use: (g) => talkTo(g, "satosister", SATO) },
    // the komusō on the road (his box while he passes: the passer keeps it with him; none while he is not there)
    { id: "komuso", name: "komusō", rect: [0, 0, 1, 1], look: each("edo.akashi.komuso"), use: each("edo.akashi.komuso.use") },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and as the stage is built.
  setup(g) {
    room.lifted = false; room.wading = false; room.waves = false; room.komuso = false;
    dressAll(g, "outdoors");
    dressLil(g);
    octopus(g);
    CHAT.reset();
  },

  async enter(g) {
    if (!heard(g, AKASHI.arrive[0])) await arrive(g);
  },
};

// (the names a test or a tool may want)
export const PLACES = { M, OCTOPUS, WADE, EDGE, ASHORE, HEITA_EDGE, BY_FUSA, TALK_AT, BOX };
export { SAND, SHALLOWS, FLOOR, FUSA as fusaTalk, LEADER as leaderTalk, HEITA as heitaTalk, SATO as satoTalk, octopusPic };

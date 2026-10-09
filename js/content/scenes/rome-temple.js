// Act Two, the last of three scenes: inside the temple of Saturn, which is also the treasury.
// Rome, the morning of the Ides of March, 44 B.C. The Son plays.
//
// The door in time is here, on the left wall: shut, invisible, humming. Light opens a door, and
// the more light, the bigger the door. His flashlight is in Egypt and his phone is dead, but the
// morning sun lies on the floor, and he has a new silver coin (chain C, from the fountain in rome-street):
//
//   the spark   stand in the sunlight and tip the coin: a spot of light lands on the place that
//               hums, and a door opens exactly the size of the coin. (The clerk must not see. The first
//               try goes across his eyes; he loses count, starts again, and the second try is done
//               while he counts.)
//   the toss    the coin goes through. It does not come back down. That ends the act: the story
//               moves to the rest of the family, two thousand years later, where the coin lands.
//
// Try it: index.html?scene=rome-temple&lead=son&flags=rome.arrived,rome.inside,rome.sawInside
// (he has no coin that way: fetch one from the fountain, or start at rome-street.)

const art = "art/scenes/rome-temple/";

/** Has this line been spoken yet? (The engine counts every line it says.) */
const heard = (g, id) => !!g.store.data.seenLines[id];
/** A thing worth looking at twice: the first line the first time, the second after that. */
const twice = (first, second) => (g) => g.say(heard(g, first) ? second : first);

// ---------- the light ----------
// Places for the spot of reflected sunlight. It is drawn live (see `live` below): `#glint` is the spot,
// `#ray` the faint beam from the coin to it, `#door` the door in time and `#hole` its rings.
const HAND = [404, 438];                                          // the coin, in the hands of a boy standing on the sunlit patch (he is drawn over it)
const WRONG = [[720, 240], [603, 381]];                           // the first try: down the right wall, and into the clerk's eyes
const RIGHT = [[224, 238], [190, 330]];                           // the second: down the left wall and a little left, onto the place that hums (its end is the painter's `hum.at`)

/** Put the spot of light at a place, with its beam. */
function aim(g, x, y) {
  const glint = g.q("#glint"), ray = g.q("#ray");
  if (glint) glint.setAttribute("transform", `translate(${x} ${y})`);
  if (ray) ray.setAttribute("points", `${HAND[0]},${HAND[1]} ${x - 3},${y - 6} ${x + 3},${y + 6}`);
}
/** Show or hide the spot and its beam. */
function shine(g, on) {
  const glint = g.q("#glint"), ray = g.q("#ray");
  if (glint) glint.setAttribute("opacity", on ? 1 : 0);
  if (ray) ray.setAttribute("opacity", on ? 0.2 : 0);
}
/** Slide the spot from one place to another. */
const sweep = (g, [from, to], ms) => g.tween(ms, (k) => aim(g, from[0] + (to[0] - from[0]) * k, from[1] + (to[1] - from[1]) * k));
/** How far open the door is: 0 is shut and not to be seen, 1 is the size of the coin. */
function openDoor(g, k) {
  const door = g.q("#door"), hole = g.q("#hole");
  if (door) door.setAttribute("opacity", k);
  if (hole) hole.style.transform = `scale(${Math.max(k, 0.01)})`;
}

// ---------- chain C ends here: the spark ----------

/** Touching the place that hums. The first time he works out what it wants. */
async function tryTheHum(g) {
  if (heard(g, "rome.hum.try.4")) return g.say("rome.hum.again");
  await g.say("rome.hum.try.1", "rome.hum.try.2");
  await g.reach();                                                // the phone, held up to the wall
  await g.say("rome.hum.try.3", "rome.hum.try.4");
}

/** The coin, held up in the sunlight. */
async function spark(g) {
  if (g.flag("rome.doorOpen")) return g.say("rome.sun.done");
  const me = g.lead;
  await g.say("rome.spark.1");
  // The first try. The coin goes up into the sun, and the spot lands on the wrong wall and slides down it to the clerk.
  const arm = g.reach();
  await g.wait(230);                                              // (his arm is out)
  aim(g, WRONG[0][0], WRONG[0][1]);
  shine(g, true);
  await sweep(g, WRONG, 700);
  await arm;
  await g.say("rome.spark.2");
  shine(g, false);                                                // the coin goes behind his back
  if (me) me.face("E");
  await g.say("rome.spark.3", "rome.spark.4", "rome.spark.5", "rome.spark.6");
  // The second try, while the clerk counts.
  if (me) me.face("W");
  aim(g, RIGHT[0][0], RIGHT[0][1]);
  shine(g, true);
  await Promise.all([sweep(g, RIGHT, 2600), g.say("rome.spark.7")]);
  // The light is on the place that hums. A little light: a little door.
  g.flag("rome.doorOpen", true);
  g.sfx("portal");
  await g.tween(900, (k) => openDoor(g, k), g.ease.out);
  shine(g, false);
  await g.say("rome.spark.8", "rome.spark.9");
  await g.walkTo(264, 384);                                       // over to it, for a look through (the same place as the hotspot's, below)
  if (me) me.face("W");
  await g.say("rome.spark.10");
}

// ---------- the gate: the toss ----------

/** The old ending, kept as it was. (The one addition is the wink of the door as the coin goes in.) */
async function tossCoin(g) {
  await g.say("rome.hole.coin");
  await g.reach();
  g.take("coin");                              // it comes out of the sky in Nevada, about two thousand years later
  g.sfx("portal");
  const hole = g.q("#hole");
  if (hole) g.tween(600, (k) => { hole.style.transform = `scale(${1 + 0.8 * Math.sin(Math.PI * k)})`; });   // not waited for: the timing stays the old scene's
  await g.wait(900);
  await g.say("rome.hole.coin2");
  g.flag("rome.tossed", true);
  await g.wait(400);
  await backHome(g);
}

/** Act break: leave the Son in Rome and pick the story up with the rest of the family, in the present. */
async function backHome(g) {
  const d = g.store.data;
  g.rememberPlace();
  d.act = 3;
  d.active = "mom";
  g.team(["mom", "bigsis", "lilsis"]);         // from here the player switches between these three
  await g.fade(1, 700);
  await g.card("Meanwhile", "about two thousand years later", { plain: true });
  await g.goto("home-living-room", { via: "cut" });
}

// ---------- the god, and the clerk who counts ----------

/** The soothsayer's incense, set down where it was meant to go. Nothing depends on it: it is good manners. */
async function offerIncense(g) {
  await g.say("rome.statue.incense.1");
  await g.reach();
  g.take("incense");
  g.flag("rome.offered", true);
  await g.say("rome.statue.incense.2", "rome.statue.incense.3");
}

/** Every time he is spoken to, he loses count. */
async function talkToClerk(g) {
  if (!g.flag("rome.metClerk")) {
    await g.say("rome.clerk.hi.1", "rome.clerk.hi.2", "rome.clerk.hi.3", "rome.clerk.hi.4");
    g.flag("rome.metClerk", true);
  } else await g.say("rome.clerk.again");
  for (;;) {
    const pick = await g.choose([
      { id: "count", line: "rome.clerk.ask.count" },
      { id: "feet", line: "rome.clerk.ask.feet" },
      { id: "hum", line: "rome.clerk.ask.hum" },
      // The accounts on his table are from Judea: Antipater's, and his son Herod's. The boy knows a KING Herod, from the
      // Christmas story (Matthew 2); the clerk knows a governor's son, which is what Herod is this year.
      { id: "judea", line: "rome.clerk.ask.judea" },
      { id: "dad", line: "rome.clerk.ask.dad" },
      { id: "bye", line: "rome.clerk.ask.bye" },
    ]);
    if (pick === "count") await g.say("rome.clerk.ask.count", "rome.clerk.ans.count.1", "rome.clerk.ans.count.2", "rome.clerk.ans.count.3");
    else if (pick === "feet") await g.say("rome.clerk.ask.feet", "rome.clerk.ans.feet.1", "rome.clerk.ans.feet.2", "rome.clerk.ans.feet.3");
    else if (pick === "hum") await g.say("rome.clerk.ask.hum", "rome.clerk.ans.hum.1", "rome.clerk.ans.hum.2", "rome.clerk.ans.hum.3", "rome.clerk.ans.hum.4");
    else if (pick === "judea") await g.say("rome.clerk.ask.judea", "rome.clerk.ans.judea.1", "rome.clerk.ans.judea.2", "rome.clerk.ans.judea.3", "rome.clerk.ans.judea.4");
    else if (pick === "dad") await g.say("rome.clerk.ask.dad", "rome.clerk.ans.dad.1", "rome.clerk.ans.dad.2", "rome.clerk.ans.dad.3");
    else return g.say("rome.clerk.ask.bye", "rome.clerk.ans.bye");
  }
}

const clerkAndCoin = ["rome.clerk.coin.1", "rome.clerk.coin.2", "rome.clerk.coin.3"];
const handsOff = ["rome.chests.use.1", "rome.chests.use.2", "rome.chests.use.3"];
const chests = { name: "treasure chests", verb: "Open", look: twice("rome.chests.look", "rome.chests.look2"), use: handsOff };
const tablets = { name: "bronze tablets", look: "rome.tablets.look" };
const brazier = { name: "brazier", verb: "Touch", look: "rome.brazier.look", use: "rome.brazier.use" };
const wayOut = {
  name: "the steps", verb: "Go out to", walkTo: [400, 594], look: "rome.out.look",
  use: (g) => (g.flag("rome.tossed") ? backHome(g) : g.goto("rome-steps", { spawn: "fromTemple" })),
};

export default {
  id: "rome-temple",
  era: "rome",
  name: "Inside the temple: the treasury",

  horizon: 120, full: 585,

  // Every place in this file is the painter's own measurement of the finished picture (art/scenes/rome-temple/layout.json),
  // or was set by eye against the picture with the people standing in it. The act's check script (check-rome.mjs) reads
  // this file against that one; the few differences that are meant are listed there.

  // The floor, from the foot of the god's pedestal to the doors behind us, between the chests along the walls.
  walk: { area: [[216, 598], [232, 559], [168, 554], [275, 353], [531, 353], [669, 598]] },
  // He comes in a few steps past the painter's mark (400, 570): down there the inventory bar, which lies over the
  // bottom of the picture whenever the game is waiting for a click, would hide him to the knees. (For the same reason
  // the places to stand for the sunlight, the near brazier and the chest by the door are a little higher than the painter's.)
  spawn: { default: [400, 532] },
  exits: ["rome-steps", "home-living-room"],
  // The way out across the edge of the picture (round three): the doors are behind us, so the bottom edge is the way out,
  // wherever along it he is sent (the inventory bar, which lies along the bottom, takes the clicks that land on its things).
  // It goes as the three ways out below go: out to the steps, or, in a game saved just after the coin went through, home.
  edges: {
    S: { to: "rome-steps", spawn: "fromTemple", name: "out to the steps", walkTo: [400, 594], use: wayOut.use },
  },

  picture: art + "back.png",
  planes: [
    { id: "table", src: art + "table.png", base: 488, solid: [[501, 499], [612, 499], [586, 452], [489, 452]] },    // the clerk sits behind it
    { id: "front", src: art + "front.png", plane: "front" },      // the edges of the door leaves, and a brazier at the bottom left
  ],

  // LIGHT, drawn live.
  //   The coals of the two braziers and the flame of the clerk's lamp glow, and breathe a little.
  //   The other three start out of sight; `setup` and the scripts above bring them on:
  //   #ray     the faint beam from the coin to the spot
  //   #glint   the spot of reflected sunlight
  //   #door    the door in time, the size of a coin. Inside it, #hole is the game's own wormhole, very small.
  live(art) {
    return `<defs>
        <radialGradient id="glint-glow"><stop offset="0" stop-color="#fffbe6" stop-opacity="0.95"/><stop offset="0.45" stop-color="#ffe9a8" stop-opacity="0.5"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/></radialGradient>
        <radialGradient id="ember-glow"><stop offset="0" stop-color="#ffb060" stop-opacity="0.5"/><stop offset="0.5" stop-color="#ff8a3c" stop-opacity="0.2"/><stop offset="1" stop-color="#ff8a3c" stop-opacity="0"/></radialGradient>
      </defs>
      <g shape-rendering="geometricPrecision">
        <circle class="glow" cx="137" cy="533" r="58" fill="url(#ember-glow)"/>
        <circle class="glow" cx="475" cy="305" r="30" fill="url(#ember-glow)" style="animation-delay:-1.3s;animation-duration:4.1s"/>
        <circle class="glow" cx="631" cy="404" r="26" fill="url(#ember-glow)" style="animation-delay:-2.2s;animation-duration:2.7s"/>
      </g>
      <polygon id="ray" points="0,0 0,0 0,0" fill="#ffe9a8" opacity="0" shape-rendering="geometricPrecision"/>
      <g id="glint" opacity="0" shape-rendering="geometricPrecision"><circle r="17" fill="url(#glint-glow)"/><ellipse rx="5" ry="6.5" fill="#fffdf0"/></g>
      <g id="door" opacity="0"><g class="flicker">${art.portal(190, 330, 11, "hole")}</g></g>`;
  },

  actors: [{ id: "clerk", kind: "clerk", at: [614, 464], face: "W",
    life: { every: [25, 45], spots: [[642, 436, "NE"], [596, 446, "N"]], stay: [4, 8] } }],    // up from his table, back to his rack, or along behind the table (a straight line: the floor behind it is his own)

  // THINGS THAT MOVE BY NATURE (round four: briefs/out/paint-4a-ready.md). The clerk's lamp has lost its painted flame,
  // and the engine draws it; the two braziers' coals breathe, low flames lick up from them and die down now and then
  // (`lull`), and threads of smoke rise. All the light they throw on the room stays painted.
  fx: [
    // the clerk's oil lamp on his table, in still air, and its thread of smoke (base one row in front of the table's)
    { id: "lamp-flame", type: "flame", at: [632.7, 406.7], base: 489, size: 10, width: 4.5, color: "#ffe9a0", edge: "#ff9a2c", glow: 16, glowColor: "#ffb860", glowOpacity: 0.2, flicker: 0.3 },
    { id: "lamp-smoke", type: "smoke", at: [633, 396.7], base: 489, height: 40, width: [1, 4], lean: [2, -40], rise: 10, rate: 2, gust: 0.15, color: "#3a3438", opacity: 0.2 },
    // the long bronze brazier by the door, at the front left (it is in front.png)
    { id: "brazier-embers", type: "embers", plane: "front", at: [136.7, 539.4], size: [45.1, 14], count: 30, sparks: 0.3, bed: [[81, 553], [175, 553], [189, 525], [102, 525]] },
    { id: "brazier-flame-1", type: "flame", plane: "front", at: [116.4, 541.5], size: 8, width: 4.4, color: "#ffcf6a", edge: "#ff7a20", glow: 0, flicker: 0.8, lull: 0.5 },
    { id: "brazier-flame-2", type: "flame", plane: "front", at: [139, 535.2], size: 9, width: 5, color: "#ffcf6a", edge: "#ff7a20", glow: 0, flicker: 0.8, lull: 0.5 },
    { id: "brazier-flame-3", type: "flame", plane: "front", at: [159.3, 542.9], size: 7, width: 3.9, color: "#ffcf6a", edge: "#ff7a20", glow: 0, flicker: 0.8, lull: 0.5 },
    { id: "brazier-smoke", type: "smoke", plane: "front", at: [136.7, 533.4], height: 120, width: [3, 14], lean: [6, -120], rise: 14, rate: 2.5, gust: 0.2, color: "#b8a8a0", opacity: 0.18 },
    // the pan of the brazier by the altar, far up the room: its smoke rises in front of the god (base: its feet)
    { id: "brazier2-embers", type: "embers", at: [474.7, 305.2], base: 349, size: [10.3, 2.3], count: 8, sparks: 0.1 },
    { id: "brazier2-flame-1", type: "flame", at: [471.7, 305.2], base: 349, size: 5, width: 2.5, color: "#ffcf6a", edge: "#ff7a20", glow: 0, flicker: 0.7, lull: 0.5 },
    { id: "brazier2-flame-2", type: "flame", at: [478.7, 305.7], base: 349, size: 4, width: 2, color: "#ffcf6a", edge: "#ff7a20", glow: 0, flicker: 0.7, lull: 0.5 },
    { id: "brazier2-smoke", type: "smoke", at: [474.7, 301.2], base: 349, height: 90, width: [2, 9], lean: [0, -90], rise: 12, rate: 2, gust: 0.15, color: "#b8a8a0", opacity: 0.16 },
  ],

  // Make the light match the story facts. Runs on arrival and after loading a save.
  setup(g) {
    shine(g, false);
    openDoor(g, g.flag("rome.doorOpen") ? 1 : 0);
  },

  // Back to front: a later area lies over an earlier one.
  // SHAPES (round three: the Show button outlines each thing, so each shape hugs its thing, a few pixels outside its edge).
  // They were traced from the painter's picture and cut-outs, and the clerk from the figure the engine draws at his mark.
  // A thing that is a painted cut-out names it (`plane`): Show then outlines the cut-out's own edge (the door leaves and
  // the near brazier are the cut-out "front"; the clerk's table is "table"). Each bronze tablet of the laws is a thing to
  // click, and all say the same. The patch of sunlight and the painter's way out at the bottom edge were already tight.
  // The place that hums is a bare patch of wall with nothing painted on it: its shape is a ring round the spot.
  hotspots: [
    // The way out is behind us. The painter gives it the bottom edge of the picture (the last of these three, at the
    // end of the list), which the inventory bar covers; so the two door leaves at the edges of the picture go out too.
    // (And since round three the whole bottom edge of the picture is the way out: see `edges`.)
    { id: "out-left", ...wayOut, plane: "front", poly: [[0, 0], [0, 599], [53, 599], [56, 595], [57, 1]] },
    { id: "out-right", ...wayOut, plane: "front", poly: [[743, 0], [743, 134], [741, 164], [744, 215], [742, 264], [743, 384], [741, 400], [743, 595], [746, 599], [799, 599], [799, 0]] },
    // The laws, on bronze tablets hung down the left wall, down the right, and one on the back wall. Each hangs from a nail.
    { id: "tablets", ...tablets, poly: [[59, 273], [80, 240], [83, 240], [102, 255], [102, 341], [60, 369]] },                     // the big one on the left wall
    { id: "tablets-2", ...tablets, poly: [[132, 234], [144, 207], [147, 207], [158, 222], [158, 311], [132, 328]] },
    { id: "tablets-3", ...tablets, poly: [[208, 203], [216, 186], [219, 186], [225, 199], [225, 257], [209, 268]] },
    { id: "tablets-right", ...tablets, poly: [[703, 250], [721, 236], [724, 236], [742, 265], [741, 365], [703, 340]] },        // the big one on the right wall
    { id: "tablets-right-2", ...tablets, poly: [[574, 199], [581, 190], [584, 190], [592, 206], [592, 268], [574, 262]] },
    { id: "tablets-right-3", ...tablets, poly: [[594, 211], [601, 202], [604, 202], [611, 219], [611, 279], [595, 272]] },
    { id: "tablets-right-4", ...tablets, poly: [[610, 231], [619, 221], [622, 221], [631, 239], [630, 294], [610, 291]] },
    { id: "tablets-right-5", ...tablets, poly: [[639, 219], [652, 212], [655, 212], [668, 229], [667, 296], [639, 289]] },
    { id: "tablets-back", ...tablets, poly: [[486, 184], [496, 180], [507, 174], [518, 180], [529, 184], [529, 236], [486, 236]] },           // and the one on the back wall, with its pointed top
    { id: "standards", name: "standards", poly: [[249, 184], [262, 184], [268, 180], [276, 183], [279, 195], [279, 205], [288, 210], [296, 212], [296, 238], [290, 240], [292, 312], [252, 312], [250, 250], [246, 200]], walkTo: [290, 354], face: "N", look: "rome.standards.look" },
    {
      // The seated god, his throne, and the pedestal they stand on.
      id: "statue", name: "statue of the god", verb: "Untie", poly: [[356, 160], [364, 148], [371, 141], [392, 127], [401, 127], [423, 140], [430, 145], [433, 180], [432, 262], [449, 268], [452, 272], [452, 332], [348, 332], [348, 272], [352, 268], [366, 262], [365, 215], [356, 190]], walkTo: [400, 354], face: "N",
      look: twice("rome.statue.look", "rome.statue.look2"), use: "rome.statue.use",
      useWith: { incense: offerIncense, coin: "rome.statue.coin", gum: "rome.statue.gum" },
    },
    {
      id: "altar", name: "offering bowl", poly: [[388, 298], [412, 298], [414, 301], [425, 303], [424, 332], [421, 346], [378, 346], [375, 332], [375, 303], [386, 301]], walkTo: [400, 354], face: "N",                   // the small altar table before the god, and its bowl
      look: (g) => g.say(g.flag("rome.offered") ? "rome.bowl.done" : "rome.bowl.look"),
      useWith: { incense: offerIncense },
    },
    { id: "brazier2", ...brazier, poly: [[462, 299], [488, 299], [489, 307], [482, 312], [486, 350], [463, 350], [467, 312], [461, 307]], walkTo: [469, 354], face: "N" },                          // the one by the altar
    { id: "chests", ...chests, poly: [[54, 546], [54, 482], [72, 467], [73, 447], [84, 433], [104, 430], [106, 419], [114, 413], [115, 396], [126, 392], [154, 392], [155, 385], [214, 383], [216, 396], [214, 436], [209, 445], [207, 466], [189, 474], [188, 500], [136, 524], [135, 548]], walkTo: [214, 482], face: "W" },   // down the left wall: the chests, the box of silver and the sacks
    { id: "chests2", ...chests, poly: [[219, 330], [220, 318], [231, 305], [233, 297], [240, 292], [248, 295], [249, 304], [261, 306], [262, 321], [275, 318], [288, 326], [291, 344], [262, 349], [219, 349]], walkTo: [285, 355], face: "NW" },          // the chest and sacks at the far left
    { id: "chests3", ...chests, poly: [[553, 333], [555, 320], [562, 315], [571, 318], [573, 331], [612, 331], [616, 338], [617, 416], [573, 416], [572, 368], [555, 366]], walkTo: [543, 389], face: "E" },          // down the right wall, one of them open
    { id: "chests4", ...chests, poly: [[649, 452], [662, 449], [665, 432], [688, 429], [697, 441], [716, 439], [729, 447], [731, 460], [741, 466], [741, 590], [690, 593], [688, 580], [668, 579], [650, 521]], walkTo: [622, 536], face: "E" },          // by the door on the right, with the sacks on it and the laws leaning on it
    {
      id: "cat", name: "sleeping cat", verb: "Pet", poly: [[113, 441], [120, 436], [132, 435], [142, 438], [146, 446], [145, 454], [114, 455], [112, 449]], walkTo: [196, 517], face: "W",        // on the chest nearest the brazier
      look: "rome.bankcat.look", use: ["rome.bankcat.use.1", "rome.bankcat.use.2"], useWith: { coin: "rome.bankcat.coin" },
    },
    { id: "rack", name: "clerk's rack", poly: [[612, 300], [633, 296], [636, 290], [654, 290], [657, 300], [668, 305], [668, 420], [612, 420]], walkTo: [573, 446], face: "E", look: "rome.rack.look" },   // rolls, tablets, the jar on top and the keys, behind the clerk
    { id: "brazier", ...brazier, plane: "front", poly: [[196, 512], [193, 511], [190, 514], [121, 514], [98, 516], [72, 548], [72, 587], [75, 589], [75, 599], [94, 599], [95, 589], [154, 587], [162, 588], [162, 599], [180, 599], [180, 581], [192, 576], [199, 594], [202, 596], [205, 595], [205, 591], [194, 567]], walkTo: [210, 538], face: "W" },                           // the near one, by the door
    {
      // (The painter's place to stand is 400, 555, where the inventory bar would hide his feet: he stands in the middle of the patch.)
      id: "sunpatch", name: "sunlight on the floor", verb: "Stand in", poly: [[303, 598], [368, 430], [482, 430], [478, 598]], walkTo: [404, 500], face: "NW",
      look: (g) => (g.flag("rome.doorOpen") ? g.say("rome.sun.done") : twice("rome.sun.look", "rome.sun.look2")(g)),
      use: (g) => (g.flag("rome.doorOpen") ? g.say("rome.sun.done") : g.say("rome.sun.use.1", "rome.sun.use.2")),
      useWith: { coin: spark, phone: "rome.sun.phone", gum: "rome.sun.gum", quarter: "rome.sun.quarter" },
    },
    // The place that hums is one patch of bare wall. Shut, it is a thing to touch; open, it is a door. (The door itself is drawn at 190, 330.)
    // Nothing is painted there, so its shape is a ring round the spot (Show outlines it); the open door's is a little ring round the door.
    // He stands at the far end of the floor's edge, where his head is level with the place and he can put his eye to it.
    // (The painter's place to stand, 232, 480, is nearer us: from there the place is well over his head, and the words
    // he says would lie over the door.)
    {
      id: "hum", name: "place that hums", verb: "Touch", circle: [190, 330, 20], walkTo: [264, 384], face: "W",
      when: (g) => !g.flag("rome.doorOpen"),
      look: "rome.hole.look", use: tryTheHum,
      useWith: { phone: "rome.hum.try.3", coin: "rome.hum.coin", gum: "rome.hum.gum", incense: "rome.hum.incense" },
    },
    {
      id: "hole", name: "coin-sized door", verb: "Go through", circle: [190, 330, 16], walkTo: [264, 384], face: "W",
      when: (g) => !!g.flag("rome.doorOpen"),
      look: "rome.door.look", use: ["rome.hole.use", "rome.hole.use2"],
      useWith: { coin: tossCoin, quarter: "rome.hole.quarter", phone: "rome.hole.phone", gum: "rome.hum.gum" },
    },
    {
      id: "table", name: "clerk's table", plane: "table", poly: [[502, 464], [502, 475], [506, 484], [525, 486], [528, 489], [554, 489], [557, 477], [642, 477], [643, 487], [650, 489], [653, 441], [657, 439], [657, 433], [641, 414], [648, 404], [644, 401], [637, 403], [633, 395], [629, 399], [628, 407], [634, 410], [635, 414], [598, 415], [598, 406], [589, 415], [567, 414], [567, 389], [579, 389], [575, 399], [579, 404], [586, 404], [590, 399], [584, 383], [568, 385], [563, 381], [557, 387], [542, 389], [537, 406], [541, 411], [552, 409], [548, 393], [561, 391], [560, 414], [536, 415], [540, 429], [540, 461], [524, 442], [519, 446], [513, 445], [515, 451], [509, 454]], walkTo: [515, 509], face: "NE",      // its balance, its lamp, and the sack against it
      look: "rome.table.look", use: ["rome.table.use.1", "rome.table.use.2", "rome.table.use.3"],
      useWith: { coin: clerkAndCoin, quarter: "rome.clerk.quarter" },
    },
    {
      id: "clerk", name: "clerk", verb: "Talk to", poly: [[612, 371], [604, 370], [599, 373], [596, 385], [603, 392], [600, 400], [587, 410], [580, 408], [579, 417], [583, 419], [590, 417], [595, 419], [619, 419], [622, 417], [619, 394], [614, 387], [617, 378]], walkTo: [515, 509], face: "NE",         // what shows of him above his table
      look: twice("rome.clerk.look", "rome.clerk.look2"), use: talkToClerk,
      useWith: {
        coin: clerkAndCoin, quarter: "rome.clerk.quarter", incense: "rome.clerk.incense",
        phone: ["rome.clerk.phone.1", "rome.clerk.phone.2", "rome.clerk.phone.3"],
      },
    },
    { id: "out", ...wayOut, poly: [[290, 586], [510, 586], [510, 600], [290, 600]] },   // the doors are behind us: the bottom edge
  ],

  // Runs when the lead arrives. It must be safe to run twice, so it checks its own facts.
  async enter(g) {
    if (g.flag("rome.tossed") && !g.flag("home.arrived")) return backHome(g);     // a save from just after the coin went through
    if (g.flag("rome.sawInside")) return;
    await g.wait(400);
    await g.say("rome.inside.1", "rome.inside.2", "rome.inside.3", "rome.inside.4", "rome.inside.5");
    g.flag("rome.sawInside", true);
  },
};

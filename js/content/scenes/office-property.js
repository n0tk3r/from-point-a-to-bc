// Act Five, continued: Property & Effects (SCENES-17: new in round seventeen; briefs/SCENES-17.md, and the design,
// briefs/out/office-hq-design.md, section 4). The back of the room: shelves to the ceiling, every thing on them tagged and
// dated (a Roman sandal, 1951; a clay lamp; a tin cup; a horseshoe; a cowboy hat bleached white; a goose feather; a
// cassette tape; a garden gnome, and nobody knows), archive boxes of FORM 7 by the decade, and in the tall bay on the
// lowest shelf, tag No. 3117, one banjo (damaged). Opal at her window onto the hall since 1971, on her stool, her back to
// the shelves, knitting.
//
// RANGER only, from the grille over it (office-ducts.js), or dropped onto the top shelf under it (a floor of its own: he
// stays up there, where Opal's back is turned; the aisle is hers):
//   #18 The Bearer   the receipt (Grandpa Joe's, up through the vent) dropped through the grille, or used on Opal or her
//                    counter: it flutters down onto her counter. "Claim number 3117. One banjo, damaged. One raccoon,
//                    unconfirmed." She looks up; two eyes in a mask look back. "...Confirmed." THUNK. Regulation 4. "Thank
//                    you, raccoon." She takes the banjo and her keys, and goes; Ranger goes back up, along the duct to
//                    Joe's grille, and the game cuts to Grandpa Joe, and the key in his door (office-room.js).
//   The banjo is too big to lift and would not fit in the duct; the bell is on the hall's side of the glass; everything
//   on the shelves has a tag, so it is somebody's.
//
// Every place is the painter's own measurement of the finished picture (art/scenes/office-property/layout.json, PAINT-17C's
// ready.md); where a place was set by eye the comment says so.
//
// Try it: index.html?scene=office-ducts&lead=ranger&flags=office.arrived,office.inside,office.acOff ("Look down" PROP & EFF)

import { STOCK, ANNOUNCE, BUILDING, WORDS, who, is, keepHeat, chatter, swap, shades, rangerAt, cutTo } from "./office-common.js";
import { nowAndThen } from "../talk/office.js";

const art = "art/scenes/office-property/";

// ---------- the room (layout.json: horizon 290, full 436; the aisle's front edge is 1.26 by the camera) ----------
const AISLE = [[357, 409], [537, 418], [536, 412], [611, 416], [635, 444], [585, 452], [593, 474], [278, 472]];
// The top shelf under the grille: Ranger's place in here (marks.vent: scale 1.613, sorted at 526: nearer than anybody in
// the aisle). One spot, a little wider than he is, so that he can turn round on it.
const SHELF = [[134, 194], [160, 194], [160, 201], [134, 201]];
const VENT = [147, 198], VENT_SCALE = 1.613, VENT_BASE = 526, GRILLE = [155, 142];
const OPAL = [437, 417];               // on her stool at the window, her back to us (the floor under her hips)
const COUNTER = [385, 339];            // where the receipt lands, at the counter's front edge (marks.counter)
const BANJO = [311, 472];              // the aisle in front of the banjo's bay (marks.banjo.stand)
const DOOR = [572, 417], HALL = [562, 398];
const THERE = [210, 175];              // Ranger's thoughts while he looks down (he is up at the grille): by it
const sizeAt = (y) => Math.min(1.3, Math.max(0.1, (y - 290) / (436 - 290)));

const opal = (g) => g.actor("opal");
const away = (g) => is(g, "office.receiptGiven") && !is(g, "office.banjoBack");      // (gone with the banjo, to the Comfortable Room)
const eyes = (g) => rangerAt(g, "over-property");
const lying = { now: false };          // the receipt lying on her counter (while she reads it: a script's)

// ---------- #18: the receipt, and Opal ----------
/** The receipt goes down to Opal: through the slats (Ranger looking down), or from the top shelf. It flutters along the
    aisle and lands on her counter; she reads it, looks up at the vent, stamps it, quotes Regulation 4, thanks the raccoon,
    takes the banjo and her keys, and goes. Then Ranger goes back up and along the duct to Joe's grille, and the game cuts
    to Grandpa Joe (the room's `enter`: Opal at his door). */
async function receipt(g) {
  const o = opal(g);
  if (!o || away(g)) return g.say("office.prop.with.ranger");
  await g.say("office.prop.receipt.drop.ranger");
  g.take("receipt");
  await flutter(g, "receipt", GRILLE, COUNTER);
  lying.now = true;
  const paper = g.plane("receipt");
  if (paper) paper.show(true);
  await g.say("office.prop.receipt.lying.ranger");
  // she reads it, close, through her half-moons
  if (o.hold) o.hold(true, "read");
  await g.say("office.prop.receipt.1");
  if (o.hold) o.hold(false);
  // she turns on her stool, a step at a time, until the vent is above her; two eyes in a mask look back
  o.face("NW"); await g.wait(300); o.face("W"); await g.wait(200);
  if (o.hold) o.hold(true, "up");
  await g.say("office.prop.receipt.2");
  if (o.hold) o.hold(false);
  o.face("N");
  const stamping = o.fidget ? o.fidget("thunk") : null;
  await g.wait(550);
  g.sfx("stamp");                                                              // THUNK
  if (stamping) await stamping;
  await g.say("office.prop.receipt.3", "office.prop.receipt.4", "office.prop.receipt.5");
  await g.say("office.prop.receipt.ranger");
  // off the stool, the receipt in her hand; the banjo off its shelf; and out, with her keys
  if (o.sit) await o.sit(false);
  lying.now = false;
  if (paper) paper.show(false);
  const map = g.groundFor("opal");
  await o.walkPath(g.clock, map.path([o.x, o.y], BANJO), sizeAt);
  o.face("W");
  if (o.play) await o.play(g.clock, "pick");
  g.flag("office.receiptGiven", true);                                         // (the banjo's bay is empty: the cut-out goes)
  const b = swap(g, "opal", "opal-banjo", null, "W", o.scale);
  await g.view.cast.load();
  await b.walkPath(g.clock, g.groundFor("opal").path([b.x, b.y], DOOR), sizeAt);
  const shut = g.plane("door"), open = g.plane("door-open");
  g.sfx("unlock");
  if (shut) shut.show(false);
  if (open) open.show(true);
  await Promise.all([b.walkPath(g.clock, [HALL], sizeAt), g.tween(420, (k) => b.fade(1 - k))]);
  g.view.cast.remove("opal");
  if (open) open.show(false);
  if (shut) shut.show(true);
  g.sfx("latch");
  await g.wait(500);
  // back up into the duct, along it to Joe's grille, and the game goes to Joe
  if (g.peeking) await g.backUp();
  else await g.climbUp({ scene: "office-ducts", spawn: "over-property", to: GRILLE });
  const r = g.lead;
  if (r && g.scene && g.scene.id === "office-ducts") {
    r.hurry = true;
    await g.walkTo(175, 470);
    r.face("E");
    g.rememberPlace();
  }
  await g.wait(300);
  await cutTo(g, "grandpajoe");
}
/** A small thing floats down from a point to a point, swaying as paper does, and is gone (it is on the counter now). */
async function flutter(g, item, [x0, y0], [x1, y1]) {
  if (g.clock.skipping) return;
  const pic = g.view.cast.addPicture("flutter", { src: `art/items/${item}.png`, foot: [32, 32] }, x0, y0, 0.22);
  pic.base = 599;
  await g.view.cast.load();
  await g.tween(1700, (k) => {
    const e = k * k * (3 - 2 * k);
    pic.place(x0 + (x1 - x0) * e + 18 * Math.sin(k * Math.PI * 4) * (1 - k), y0 + (y1 - y0) * k, 0.22 - 0.08 * k);
  }, (k) => k);
  g.view.cast.remove("flutter");
}
/** A thing used on the grille over Property (office-ducts.js looks down first): the receipt goes; anything else he keeps. */
async function handDown(g, item) {
  if (item === "receipt") return receipt(g);
  return g.say("office.prop.with.ranger");
}
/** The banjo: he cannot lift it; and it would not fit in the duct anyway. */
const banjoUse = (g) => g.say(g.store.data.seenLines["office.prop.banjo.use.ranger"] ? "office.prop.banjo.use2.ranger" : "office.prop.banjo.use.ranger");
const TAGGED = "office.prop.tagged.use.ranger";
/** The things handed to the grille's view (from above): the receipt on Opal or her counter; anything else, no. */
const DOWN = Object.fromEntries(["receipt", "pietin", "peanuts", "schedule", "bottlecap"].map((item) => [item, (g) => handDown(g, item)]));

/** One of the room's areas: Ranger's look (from above too), and his use in here (on the top shelf: he never walks off it). */
function spot(id, name, shape, look, use = null, { peekWith = null, drop = false, when = null, more = {} } = {}) {
  return { id, name, ...shape, walkTo: null, look: { ranger: look }, ...(use ? { use: { ranger: use } } : {}),
    peek: { look: { ranger: look }, ...(peekWith ? { useWith: peekWith } : {}), ...(drop ? { drop: true } : {}) },
    ...(peekWith ? { useWith: peekWith } : {}), ...(when ? { when } : {}), ...more };
}

const CHAT = chatter(nowAndThen["office-property"], { first: [10, 16], every: [30, 46], when: (g) => !!opal(g) && !away(g) });

export default {
  id: "office-property",
  era: "nevada",
  name: "Property & Effects",
  building: BUILDING,
  music: "office",

  horizon: 290, full: 436, maxScale: 1.3,
  walk: [
    { name: "aisle", area: AISLE, away: { ranger: "office.duct.drop.no.ranger" } },       // down there, Opal would see him
    { name: "shelf", area: SHELF, scale: VENT_SCALE, base: VENT_BASE },
  ],
  blocked: [[[454, 418], [447, 421], [434, 421], [422, 419], [419, 416], [426, 413], [439, 413], [450, 414]],            // her stool's feet
    [[500, 419], [495, 421], [483, 422], [471, 420], [467, 417], [473, 415], [484, 414], [495, 416]]],                      // her knitting basket

  spawn: { default: [450, 455], vent: VENT, opal: OPAL, banjo: BANJO, door: DOOR, counter: [400, 416] },
  facing: "E",
  exits: ["office-ducts"],
  stock: STOCK,
  announce: ANNOUNCE,
  get wordsAt() { return WORDS.at || THERE; },
  handDown,                                                // (office-ducts.js: a thing used on the grille is handed down here)
  tick(g, dt) { keepHeat(g); CHAT.tick(g, dt); },

  picture: art + "back.png",
  planes: [
    { id: "vent", src: art + "vent.png", plane: "back", when: (g) => !eyes(g) },
    { id: "vent-eyes", src: art + "vent-eyes.png", plane: "back", when: eyes },
    { id: "wall", src: art + "wall.png", base: [[364, 399], [618, 411]] },
    { id: "door", src: art + "door.png", base: [[364, 399], [618, 411]] },
    { id: "door-open", src: art + "door-open.png", base: [[364, 399], [618, 411]], when: () => false },
    { id: "receipt", src: art + "receipt.png", base: [[364, 399], [618, 411]], when: () => lying.now },
    { id: "banjo", src: art + "banjo.png", base: [[276, 457], [222, 496]], when: (g) => !is(g, "office.receiptGiven") },
    { id: "front", src: art + "front.png", plane: "front" },
  ],

  // Opal on her stool at her window, her back to the shelves, knitting (PEOPLE-17's `opal`: her life is the needles);
  // away while she takes the banjo to Grandpa Joe, and back at her window after.
  actors: [
    { id: "opal", kind: "opal", at: OPAL, face: "N", when: (g) => !away(g), life: { fidget: [2.6, 3.4] } },
  ],

  // Back to front: the two runs of shelving and their boxes first, everything on them over them.
  hotspots: [
    spot("shelves-left", "shelves", { poly: [[0, 145], [133, 169], [340, 235], [340, 411], [224, 497], [68, 600], [53, 600], [0, 555]] }, "office.prop.shelves.ranger", TAGGED, { drop: true }),
    spot("shelves-right", "shelves", { poly: [[623, 215], [774, 122], [800, 128], [800, 474], [784, 600], [733, 600], [727, 593], [623, 401]] }, "office.prop.shelves.ranger", TAGGED),
    spot("boxes", "archive boxes", { poly: [[625, 196], [630, 192], [717, 125], [781, 76], [796, 65], [800, 63], [800, 600], [741, 600], [737, 595], [625, 402]] }, "office.prop.boxes.ranger", "office.prop.boxes.use.ranger"),
    spot("boxes-left", "archive boxes", { poly: [[0, 101], [29, 98], [86, 121], [129, 210], [131, 366], [130, 442], [128, 481], [89, 576], [53, 600], [0, 600]] }, "office.prop.boxes.ranger", "office.prop.boxes.use.ranger"),
    spot("window", "window", { poly: [[388, 265], [404, 263], [499, 262], [507, 263], [507, 334], [435, 334], [388, 333]] }, "office.prop.window.ranger", "office.prop.window.use.ranger"),
    spot("sign", "sign", { rect: [423, 245, 47, 18] }, "office.prop.sign.ranger"),
    spot("bell", "bell", { rect: [472, 322, 24, 12] }, "office.prop.bell.ranger", "office.prop.bell.use.ranger"),
    spot("door", "door", { poly: [[530, 251], [573, 250], [606, 250], [606, 411], [599, 411], [530, 408]] }, "office.prop.door.ranger"),
    spot("counter", "counter", { poly: [[356, 338], [364, 334], [520, 325], [527, 346], [525, 408], [524, 414], [512, 414], [371, 407], [360, 406], [359, 401]] },
      (g) => g.say(lying.now ? "office.prop.receipt.lying.ranger" : "office.prop.counter.ranger"), null, { peekWith: DOWN }),
    spot("stamp", "date stamp", { rect: [416, 324, 22, 16] }, "office.prop.stamp.ranger", "office.prop.stamp.use.ranger", { peekWith: DOWN }),
    spot("stool", "stool", { poly: [[421, 363], [428, 361], [443, 361], [448, 362], [452, 364], [452, 368], [449, 416], [446, 421], [423, 420], [421, 368]] }, "office.prop.stool.ranger"),
    spot("knitting", "knitting", { poly: [[428, 429], [465, 396], [485, 381], [491, 382], [498, 395], [497, 419], [496, 420], [459, 430], [449, 432], [436, 432]] }, "office.prop.knitting.ranger", "office.prop.knitting.use.ranger"),
    // the tagged things on the shelves
    spot("oillamp", "clay lamp", { poly: [[263, 352], [269, 347], [289, 355], [292, 358], [292, 367], [290, 367], [266, 356], [263, 354]] }, "office.prop.lamp.ranger", TAGGED),
    spot("cup", "tin cup", { poly: [[279, 342], [288, 342], [305, 351], [306, 354], [306, 362], [305, 362], [279, 352]] }, "office.prop.cup.ranger", TAGGED),
    spot("hat", "cowboy hat", { poly: [[211, 302], [234, 296], [256, 302], [257, 303], [257, 328], [254, 329], [214, 314], [209, 309]] }, "office.prop.hat.ranger", TAGGED),
    spot("feather", "goose feather", { poly: [[146, 246], [150, 212], [152, 202], [154, 201], [185, 263], [185, 275], [179, 275], [146, 258]] }, "office.prop.feather.ranger", TAGGED),
    spot("sandal", "Roman sandal", { poly: [[172, 289], [181, 288], [186, 291], [211, 325], [211, 336], [207, 336], [188, 322], [172, 294]] }, "office.prop.sandal.ranger", TAGGED),
    spot("horseshoe", "horseshoe", { poly: [[117, 310], [120, 305], [126, 304], [163, 326], [167, 329], [165, 343], [161, 343], [117, 327]] }, "office.prop.horseshoe.ranger", TAGGED),
    spot("gnome", "garden gnome", { poly: [[163, 378], [167, 353], [173, 339], [175, 339], [205, 387], [205, 398], [201, 399], [163, 384]] }, "office.prop.gnome.ranger", TAGGED),
    spot("cassette", "cassette tape", { poly: [[142, 390], [162, 392], [166, 393], [170, 397], [170, 405], [169, 410], [163, 411], [139, 391]] }, "office.prop.tape.ranger", TAGGED),
    spot("banjo", "banjo", { poly: [[234, 437], [241, 357], [248, 352], [254, 352], [259, 356], [266, 431], [265, 444], [262, 450], [251, 455], [244, 455], [238, 452], [235, 447]] },
      "office.prop.banjo.ranger", banjoUse, { when: (g) => !is(g, "office.receiptGiven"), more: { plane: "banjo" } }),
    // Opal on her stool (down to her hem, set by eye: below it the stool's legs are the stool's, to be clicked as the stool)
    spot("opal", "Opal", { rect: [419, 298, 38, 74] }, "office.prop.opal.ranger", null, { peekWith: DOWN, when: (g) => !away(g) }),
    // the grille in the ceiling over the shelf: from the shelf, his way back up
    { id: "vent", name: "vent", verb: "Climb up", poly: [[83, 131], [155, 124], [167, 124], [221, 151], [208, 155], [155, 159], [147, 158], [89, 136]], walkTo: null,
      look: { ranger: "office.prop.vent.ranger" }, climb: { scene: "office-ducts", spawn: "over-property", to: GRILLE, who: "ranger" } },
  ],

  setup(g) {
    keepHeat(g);
    lying.now = false;
    WORDS.at = null;
    CHAT.reset();
    shades(g);
  },

  // Ranger drops onto her top shelf: the first time, she turns round on her stool and there he is. She does not mind.
  async enter(g, from) {
    const o = opal(g), r = g.lead;
    if (who(g) !== "ranger" || from !== "office-ducts" || !o || is(g, "office.opalSaw")) return;
    g.flag("office.opalSaw", true);
    await g.wait(400);
    if (r) o.look(r.x, r.y + 200);
    await g.wait(300);
    await g.say("office.prop.opal.sees");
    o.face("N");
  },

  // Ranger looks down through the grille: the first time, everything shines.
  async viewed(g) {
    if (!is(g, "office.sawProperty")) { g.flag("office.sawProperty", true); await g.say("office.duct.prop.first.ranger"); }
  },
};

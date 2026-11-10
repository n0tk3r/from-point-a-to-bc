// Act Six, the fifth leg: the foot of Mount Shosha, the women's hall, late afternoon and then sunset (SCENES-21C: new in round
// twenty-one, in place of ENGINE-21's stub; briefs/SCENES-21.md, and the design, briefs/out/edo2-design.md, "THE FOOT OF MOUNT
// SHOSHA" and #37). The mountain going up into pines and maples, a late cherry in the shade; the east path climbing in stone
// steps out of sight, a small stone at its foot and Ryōkai on the bottom step; O-Ume's thatched hut with its lantern; the women's
// hall, small and deep-roofed, its latticed double doors shut, name slips pasted round them, on the hasp a lock carved as a
// rabbit running over waves, and a rice ball on a leaf on the step; the bench where the women wait, the heap of combs and pins
// that failed; far below at the right, the Harima plain and the castle, small and white.
//
// The three come here by the map from the town ("Shosha. An hour and a half's walk, north-west."), at the mark `road`.
//
//   arriving    once: the women on the bench argue about foxes; O-Ume settles it ("A boy who calls at suppertime is a hungry
//               boy."); the map's line for the walk said as they come
//   #37 What A Ship Gives Its Lady
//     the mountain   the east path or the mountain, the first try by anyone: Ryōkai on his feet ("Women may not climb."); then
//               hers (SHOSHA.first); Mom's own first try, whenever it comes, is Psalm 61:1-2 (said once in the act); every try
//               after, the path's or the mountain's own refusal. The stone: what it says, from Ryōkai, the first time
//     O-Ume     umeTree (talk/edo-d.js): the voice, the shipwright, the riddle (edo.riddle, edo.oumeMet), her son, the rice ball
//               on the step, the slips from Osaka and Akashi (edo.natsuGiven, edo.fusaGiven), Big Sister's note against the
//               riddle (the list: edo.listRead). Ryōkai, Grandmother Tome, the young wife and the girl: their trees
//     the lock  its use opens the close-up (edo-lock.js; the first time Grandmother Tome from the bench, edo.lockSeen). The
//               hand-round of the three things (pin, coin, comb) to their right hands: the giver's line (LOCK.give), and the
//               first time Little Sister's "Everybody give your thing to the NEXT person." (LOCK.party), in `given`
//     the doors     when the comb is home (in the close-up): `openDoors`, from there: the light goes red through the trees
//               (the sunset layer and every cut-out's twin, faded: ENGINE-21's fadePlane) as the great bell sounds on the
//               mountain; the doors swing (shut, half, open; the lock with them); edo.hallOpen; O-Ume: slips first, the slips
//               from Osaka and Akashi up first, a rice ball for her, the coin back from the post and given her (SHOSHA.open);
//               the women go in, two of them come out and go home (SHOSHA.after); O-Ume takes the rice ball in (edo.umeIn);
//               Ryōkai to the west lattice; the comb back in Mom's sleeve, the pin in Big Sister's hair
//   the hall    the open doors: in (edo-hall.js)
//   the road    the town by the map (and the bottom right): not while the sun is setting here (SHOSHA_MAP.stay)
//
// Every place is the painter's measurement (art/scenes/edo-shosha/layout.json, PAINT-21E's ready.md), or set by eye against the
// picture with the people in it; where the two differ the comment says why.
//
// PAINT-23 (round twenty-three, RECOMPOSE: tools/paint/DEPTH.md): painted again from a new place, lower and turned. We stand on the
// terrace south-west of the hall under an old pine and look north-north-east along the mountain's foot (the eye 2.5 m up): the hall
// near at the right, three-quarters on (its west side with the lattice running back, its front with the doors running away), its
// peak in the old pine's bough; the women's bench before its sunlit west wall; the stone, Ryōkai's step and the path climbing past
// O-Ume's hut into the woods at the left; past the hall's corner the plain far below and the castle. Every number below was
// measured again through the new camera (tools/paint/edo_shosha_layout.py); the ids and the logic are as they were. The front plane
// is two files: the pine (it sways) and what grows at our feet (`near`).
//
// Try it: index.html?scene=edo-shosha&lead=mom&flags=edo.supperMade

import { THREE, who, is, heard, each, giveTo, takeAny, carries, moveItem, dressAll, thingOf, faceEach, swap, TALK, GIVE_SILENT, stockGive } from "./edo-west.js";
import { umeTree, ryokaiTree, tomeTree, wifeTree, girlTree, hallRyokaiTree, SHOSHA, LOCK, SHOSHA_MAP } from "../talk/edo-d.js";

const art = "art/scenes/edo-shosha/";

// ---------- the camera and the ground (layout.json: a level camera, the eye 2.52 m up, horizon 330, full 560) ----------
const HORIZON = 330, FULL = 560;
const FLOOR = [[78, 598], [794, 598], [794, 452], [741, 452], [682, 469], [652, 471], [639, 486], [519, 501], [429, 498], [353, 464], [313, 463], [224, 473], [133, 466], [115, 464], [186, 443], [187, 435], [67, 443], [60, 453], [60, 520]];

// ---------- the marks (layout.json marks) ----------
const M = { road: [663, 536], stone: [230, 489], path: [132, 475], ryokai: [189, 471], hall: [603, 500], lock: [584, 494], step: [619, 489], ume: [432, 502], hut: [152, 441], bench: [392, 515], tome: [317, 499], wife: [351, 496], girl: [384, 492], view: [737, 462], combs: [186, 525] };
const LATTICE = [363, 471];             // Ryōkai standing at the hall's west lattice, outside, once it is open (58 cm out from the wall: his face at it)
const DOORWAY = [534, 484];             // the foot of the open doors (the women go in here, and come out)
const HOMEWARD = [[581, 525], [787, 562], [830, 612]];      // the young wife and the girl, home down the road
const TALK_AT = { ryokai: [222, 487], ume: [512, 508], tome: [334, 510], wife: [370, 506], girl: [390, 508], hall: [595, 497] };

// ---------- the story, as the picture shows it ----------
const open = (g) => is(g, "edo.hallOpen");
const room = { sunset: false };
const red = (g) => open(g) || room.sunset;                    // the low red light (the lock is open)
const umeIn = (g) => is(g, "edo.umeIn");                     // O-Ume gone in with the rice ball on its leaf
const twin = (g, s) => (red(g) ? `${s}-sunset` : s);

// ---------- #37 (1): the mountain ----------
/** The east path, or the mountain, tried. The first try by anyone: Ryōkai on his feet; then hers (Mom's first is the psalm,
    once in the act); after, the thing's own refusal. */
const climb = (thing) => async (g) => {
  const me = who(g), r = g.actor("ryokai");
  const firstEver = !heard(g, SHOSHA.climb[0]);
  const mine = me === "mom" ? SHOSHA.psalm : SHOSHA.first[me];
  const myFirst = !heard(g, mine[0]);
  g.lead.face("N");
  if (firstEver) {
    const up = swap(g, "ryokai", "ryokai-standing", M.ryokai, "E");
    await g.view.cast.load();
    up.look(g.lead.x, g.lead.y);
    up.hold(true, "bar");
    await g.say(...SHOSHA.climb);
  }
  if (myFirst && me === "mom") {
    const mom = g.actor("mom");
    if (mom) { mom.face("N"); mom.pray(true); }
    try { await g.say(mine[0], mine[1], mine[2]); } finally { if (mom) mom.pray(false); }
    const big = g.actor("bigsis");
    if (big && mom) big.look(mom.x, mom.y);
    await g.say(mine[3], mine[4]);
  } else if (myFirst) await g.say(...mine);
  else await g.say(`edo.shosha.${thing}.use.${me}`);
  if (firstEver) { const s = swap(g, "ryokai", "ryokai", M.ryokai, "E"); await g.view.cast.load(); return s; }
  return r;
};
async function stoneUse(g) {
  if (heard(g, SHOSHA.stone)) return g.say(`edo.shosha.stone.use.${who(g)}`);
  const r = g.actor("ryokai");
  if (r) r.look(M.stone[0], M.stone[1]);
  await g.say(SHOSHA.stone);
}

// ---------- #37 (2): O-Ume, and the women ----------
/** A slip into O-Ume's hands: held out, taken; then her answer (the option's reply, said after: staging). */
const slipTo = (item, hold, reply) => async (g) => {
  const lead = g.lead, u = g.actor("ume");
  faceEach(g, lead, u);
  lead.hold(true, hold);
  await g.wait(450);
  lead.hold(false);
  takeAny(g, item);
  g.sfx("pickup");
  if (u) { u.hold(true, "slips"); await g.wait(400); u.hold(false); }
  await g.say(reply);
};
const REPLY = {};
const UME = (() => {
  const t = umeTree({ slipNatsu: (g) => slipTo("natsuslip", "slips", REPLY.natsuslip)(g), slipFusa: (g) => slipTo("fusaslip", "slip", REPLY.fusaslip)(g) });
  // (staging) the slip held out and taken, then her answer: the option's reply is said in the hook
  for (const id of ["natsuslip", "fusaslip"]) {
    const o = t.nodes.talk.options.find((x) => x.id === id);
    REPLY[id] = o.say[0];
    delete o.say;
  }
  return t;
})();
const RYOKAI = ryokaiTree();
const AT_LATTICE = hallRyokaiTree();          // (once the hall is open he keeps the lamp from outside, at the lattice: his words in the hall's)
const TOME = tomeTree(), WIFE = wifeTree(), GIRL = girlTree();
async function talkTo(g, id, tree) {
  const a = g.actor(id), lead = g.lead;
  if (a && lead) a.look(lead.x, lead.y);
  await g.talk(tree);
}
/** Big Sister's note against the riddle (on O-Ume, or the heap of combs): the list; after it, the short form. */
async function noteRead(g, then = null) {
  if (who(g) !== "bigsis" || !is(g, "edo.riddle")) return g.say(g.fallback("nope"));
  if (is(g, "edo.listRead")) return g.say(then || SHOSHA.listAgain);
  await g.say(...SHOSHA.list);
  g.flag("edo.listRead", true);
}
async function combsUse(g) {
  if (who(g) === "bigsis" && is(g, "edo.listRead")) return g.say(SHOSHA.combsRead);
  return g.say(`edo.shosha.combs.use.${who(g)}`);
}

// ---------- #37 (3): the lock ----------
async function lockUse(g) {
  await g.say(`edo.shosha.lock.use.${who(g)}`);
  if (!is(g, "edo.lockSeen")) {
    const t = g.actor("tome");
    if (t) t.look(M.lock[0], M.lock[1]);
    await g.say(LOCK.first);
    g.flag("edo.lockSeen", true);
  }
  await g.openCloseup("edo-lock");
}

// ---------- #37 (6): the doors open ----------
/** From the lock's close-up, once the comb is home and the bolt is out (edo-lock.js): back here, and the doors open. */
export async function openDoors(g) {
  const lock = g.plane("lock"), doors = g.plane("doors"), sun = g.plane("sunset");
  for (const id of THREE) { const a = g.actor(id); if (a) a.look(M.lock[0], 380); }
  if (lock) lock.set("open");
  g.sfx("click");
  await g.wait(500);
  // the sun low: the light goes red through the trees as the great bell sounds on the mountain
  room.sunset = true;
  g.sfx("greatbell");
  if (sun) { sun.fade(0); sun.show(true); }
  const ms = 2000, step = g.plane("stepball");
  await Promise.all([
    g.fadePlane("sunset", 1, { ms }),
    g.fadePlane("doors", "shut-sunset", { ms }),
    g.fadePlane("lock", "open-sunset", { ms }),
    g.fadePlane("stone", "sunset", { ms }), g.fadePlane("bench", "sunset", { ms }), g.fadePlane("pine", "sunset", { ms }), g.fadePlane("near", "sunset", { ms }),
    step && !step.hidden ? g.fadePlane("stepball", "there-sunset", { ms }) : null,
  ]);
  await g.wait(400);
  // the doors swing, the lock on its hasp with them
  g.sfx("shutter");
  if (doors) doors.set("half-sunset");
  if (lock) lock.show(false);
  await g.wait(280);
  if (doors) doors.set("open-sunset");
  await g.wait(400);
  g.flag("edo.hallOpen", true);
  await openLines(g);
}
/** O-Ume: slips first, Tome at the front; the slips from Osaka and Akashi; a rice ball for her; the coin from a ship. The women
    go in; two come out and go home; O-Ume takes the rice ball on its leaf in with her; Ryōkai to the lattice. */
async function openLines(g) {
  const u = g.actor("ume"), mom = g.actor("mom"), lil = g.actor("lilsis");
  if (u) u.face("W");
  await g.say(SHOSHA.open[0]);
  // Grandmother Tome to the front, and in
  const tome = g.actor("tome");
  const inGoes = (async () => {
    if (!tome) return;
    if (tome.sit) await tome.sit(false);
    await g.moveTo(DOORWAY[0], DOORWAY[1], "tome");
    await g.tween(300, (k) => tome.fade(1 - k));
    tome.hidden = true;
  })();
  // the slips from Osaka and Akashi, if they are still carried, given now
  for (const item of ["natsuslip", "fusaslip"]) {
    const from = ["mom", "bigsis", "lilsis"].find((w) => carries(g, w, item));
    if (!from) continue;
    const a = g.actor(from);
    if (a && u) faceEach(g, a, u);
    await g.say(SHOSHA.slips[item]);
    if (a) { a.hold(true, from === "mom" ? "slips" : "slip"); await g.wait(350); a.hold(false); }
    takeAny(g, item);
    g.flag(item === "natsuslip" ? "edo.natsuGiven" : "edo.fusaGiven", true);
  }
  if (u) u.hold(true, "slips");
  await g.say(SHOSHA.open[1]);
  if (u) u.hold(false);
  // a rice ball for her, from Mom's bundle
  if (mom && u) faceEach(g, mom, u);
  if (mom) mom.hold(true, "riceball");
  await g.say(SHOSHA.open[2]);
  if (mom) mom.hold(false);
  if (u) u.hold(true, "riceball");
  await g.say(SHOSHA.open[3]);
  if (u) u.hold(false);
  // the coin, back off the post (Mom has it, from the hand-round) and from Little Sister to her
  moveItem(g, "mon", "lilsis");
  if (lil && u) faceEach(g, lil, u);
  if (lil) lil.hold(true, "coinout");
  await g.say(SHOSHA.open[4]);
  if (lil) lil.hold(false);
  takeAny(g, "mon");
  g.sfx("pickup");
  await g.say(SHOSHA.open[5], SHOSHA.open[6]);
  await inGoes;
  // the comb back in Mom's sleeve, the pin in Big Sister's hair (whoever had them for the lock)
  moveItem(g, "comb", "mom");
  moveItem(g, "kanzashi", "bigsis");
  await g.say(SHOSHA.open[7]);
  // the women: Tome is in; the young wife and the girl go in, come out, and go home before dark
  await g.say(SHOSHA.after.tome);
  for (const id of ["wife", "girl"]) {
    const a = g.actor(id);
    if (!a) continue;
    if (a.sit) await a.sit(false);
  }
  await Promise.all(["wife", "girl"].map(async (id, n) => {
    const a = g.actor(id);
    if (!a) return;
    await g.wait(n * 500);
    await g.moveTo(DOORWAY[0] + 14, DOORWAY[1] + 2, id);
    await g.wait(700);
    a.face("SE");
  }));
  await g.say(SHOSHA.after.wife);
  await g.say(SHOSHA.after.girl);
  await Promise.all(["wife", "girl"].map(async (id, n) => {
    const a = g.actor(id);
    if (!a) return;
    await g.wait(n * 400);
    for (const p of HOMEWARD) await g.moveTo(p[0], p[1], id);
    a.hidden = true;
  }));
  // O-Ume takes his supper in with her; Ryōkai goes to the lattice, outside
  if (u) {
    await g.moveTo(M.step[0], M.step[1], "ume");
    await u.play(g.clock, "reach");
    g.flag("edo.umeIn", true);
    u.hold(true, "riceball");
    await g.moveTo(DOORWAY[0], DOORWAY[1], "ume");
    await g.tween(300, (k) => u.fade(1 - k));
    u.hidden = true;
  }
  const r = g.actor("ryokai");
  if (r) {
    const s = swap(g, "ryokai", "ryokai-standing", [r.x, r.y], "E");
    await g.view.cast.load();
    await g.moveTo(LATTICE[0], LATTICE[1], "ryokai");
    s.face("N");
    s.hold(true, "peer");
  }
}

// ---------- the hand-round (the lock's three things, anywhere here) ----------
const THREE_THINGS = Object.keys(LOCK.rightHands);
/** The scene's own give lines (the stock ones are silent here: GIVE_SILENT): to its right one, the giver's LOCK.give; the first
    of the three things to change hands, Little Sister's "Everybody give your thing to the NEXT person." */
export async function handRound(g, item, to, from) {
  if (THREE_THINGS.includes(item) && LOCK.rightHands[item] === to) await g.say(LOCK.give[item]);
  else await g.say(stockGive(from));
  if (THREE_THINGS.includes(item) && !heard(g, LOCK.party)) await g.say(LOCK.party);
}

// ---------- the ways ----------
const stayUse = (g) => g.say(SHOSHA_MAP.stay);
async function doorsUse(g) {
  if (!open(g)) return g.say(`edo.shosha.doors.use.${who(g)}`);
  await g.say(`edo.shosha.doors.open.use.${who(g)}`);
  await g.goto("edo-hall", { spawn: "door" });
}

// ---------- the scene ----------
const thing = thingOf("shosha");
const poly = (p) => ({ poly: p });
const BOX = { ume: [414, 407, 35, 97], ryokai: [177, 407, 24, 66], ryokaiUp: [173, 385, 32, 88], lattice: [347, 385, 32, 88], tome: [304, 428, 26, 73], wife: [337, 423, 27, 75], girl: [372, 424, 25, 70] };
const UME_HERE = (g) => !umeIn(g);
const ON_BENCH = (g) => !open(g);

export default {
  id: "edo-shosha",
  era: "edo",
  name: "The foot of Mount Shosha",
  music: "edo-shosha",

  horizon: HORIZON, full: FULL, minScale: 0.3,
  walk: { area: FLOOR },
  // the stone, the heap of combs on its cloth (layout.json blocked; the bench is its cut-out's solid; the old pine's foot and the
  // hut's firewood are off the walked ground now)
  blocked: [[[225, 476], [254, 476], [259, 472], [231, 472]], [[182, 515], [255, 516], [269, 503], [201, 502]]],

  party: THREE,
  spawn: { default: M.road, ...M },
  arrive: { road: [[600, 543], [744, 543]], lock: [[565, 499], [624, 494]], hall: [[573, 505], [646, 498]] },
  facing: "W",
  stock: GIVE_SILENT,
  talk: TALK,
  // not back to the town by the map while the sun sets here (the night's walk back is "Mind The Fire")
  travel: SHOSHA_MAP.stay,
  edges: { E: { name: "back to the town", walkTo: [790, 566], use: stayUse } },
  exits: ["edo-lock"],      // MERGE-21: the lock's close-up (g.openCloseup), as the deck names its compass: its pictures fetched ahead
  given: handRound,

  picture: art + "back.png",
  // CUT-OUTS, back to front (the painter's plan). The two lights: back.png and the plain cut-outs (gold), and once the lock is
  // open the sunset layer over it with every cut-out's -sunset twin (faded in by openDoors, then by the facts). The doors swing
  // shut, half, open (their gold half and open, and the lock's shut-sunset, are never on the stage: the light goes red before
  // they swing); the lock hangs on the hasp until they do; the rice ball on the step until O-Ume takes it in.
  planes: [
    { id: "sunset", src: art + "sunset.png", plane: "back", when: red },
    { id: "doors", plane: "back", states: { shut: art + "doors.png", half: art + "doors-half.png", open: art + "doors-open.png",
      "shut-sunset": art + "doors-sunset.png", "half-sunset": art + "doors-half-sunset.png", "open-sunset": art + "doors-open-sunset.png" },
      state: (g) => (open(g) ? "open-sunset" : twin(g, "shut")) },
    { id: "lock", plane: "back", states: { shut: art + "lock.png", open: art + "lock-open.png", "shut-sunset": art + "lock-sunset.png", "open-sunset": art + "lock-open-sunset.png" },
      state: (g) => twin(g, "shut"), when: (g) => !open(g) },
    { id: "stepball", plane: "back", states: { there: art + "stepball.png", "there-sunset": art + "stepball-sunset.png" }, state: (g) => twin(g, "there"), when: (g) => !umeIn(g) },
    { id: "stone", base: 475, states: { gold: art + "stone.png", sunset: art + "stone-sunset.png" }, state: (g) => (red(g) ? "sunset" : "gold"), solid: [[225, 476], [254, 476], [259, 472], [231, 472]] },
    // (the bench is turned with the hall: its base runs along its front edge)
    { id: "bench", base: [[292, 495], [388, 485]], states: { gold: art + "bench.png", sunset: art + "bench-sunset.png" }, state: (g) => (red(g) ? "sunset" : "gold"), solid: [[292, 495], [388, 485], [379, 481], [286, 491]] },
    // PAINT-23: the front plane, two files: the old pine's trunk up the left edge and its great bough across the top (it stirs:
    // fx pine), and what grows at our feet (its roots, moss and ferns along the bottom left; the bank's lip in the bottom right).
    // (`src` names the first state's picture as well, for the tools that measure a scene's front plane: with `states` the engine
    // draws the state's picture and only fetches `src` ahead, and it is the same file)
    { id: "pine", plane: "front", src: art + "pine.png", states: { gold: art + "pine.png", sunset: art + "pine-sunset.png" }, state: (g) => (red(g) ? "sunset" : "gold") },
    { id: "near", plane: "front", src: art + "near.png", states: { gold: art + "near.png", sunset: art + "near-sunset.png" }, state: (g) => (red(g) ? "sunset" : "gold") },
  ],

  // THINGS THAT MOVE BY NATURE (layout.json fx): the near pine stirring, a few petals from the late cherry, crows going home.
  fx: [
    { id: "pine", type: "sway", plane: "pine", anchor: "bottom", amount: 1.0, period: 4.6 },
    { id: "petals", type: "petals", from: [[149, 159], [313, 159], [313, 234], [149, 234]], floor: 380, count: 4, wind: 10, fall: 18, size: [2, 3], color: "#f2c9d4", color2: "#e2a8bc", plane: "back" },
    { id: "crows", type: "birds", lanes: [[[830, 196], [520, 70]], [[830, 250], [600, 128]]], every: [9, 18], group: [1, 2], speed: 50, size: 8, plane: "back" },
  ],

  // The people: O-Ume by her hut, Ryōkai on the bottom step by the stone (on his feet barring the path; at the lattice once the
  // hall is open), and on the bench Grandmother Tome and the young wife with her baby, the girl standing before it with her
  // grandmother's slip. Once the hall is open the women have gone in and home, and O-Ume is inside.
  actors: [
    { id: "ume", kind: "ume", at: M.ume, face: "W", when: UME_HERE, life: { fidget: [5, 10], still: true } },
    { id: "ryokai", kind: "ryokai", at: M.ryokai, face: "E", when: (g) => !open(g), life: { fidget: [5, 10], still: true } },
    { id: "ryokai", kind: "ryokai-standing", at: LATTICE, face: "N", when: open, life: { fidget: false } },
    { id: "tome", kind: "tome", at: M.tome, face: "S", when: ON_BENCH, life: { fidget: [5, 9], still: true } },
    { id: "wife", kind: "wife", at: M.wife, face: "S", when: ON_BENCH, life: { fidget: [6, 11], still: true } },
    { id: "girl", kind: "girl", at: M.girl, face: "S", when: ON_BENCH, life: { fidget: [4, 9], still: true } },
  ],

  // Back to front: a later area lies over an earlier one (layout.json things; the people's boxes against their figures).
  hotspots: [
    { id: "sky", name: "sky", poly: [[501, 0], [800, 0], [800, 300], [720, 306], [660, 312], [644, 300], [619, 240], [588, 160], [555, 80]], walkTo: M.view, face: "E",
      look: (g) => g.say(red(g) ? `edo.shosha.sky.sunset.${who(g)}` : `edo.shosha.sky.${who(g)}`), use: each("edo.shosha.sky.use") },
    thing("mountain", "Mount Shosha", poly([[100, 0], [491, 0], [545, 80], [584, 160], [615, 240], [638, 300], [616, 334], [470, 300], [300, 250], [100, 240]]), M.path, "N", { use: climb("mountain") }),
    thing("plain", "plain", poly([[618, 330], [800, 322], [800, 446], [740, 446], [680, 440], [618, 436]]), M.view, "E"),
    thing("castle", "castle", poly([[717, 303], [777, 303], [777, 343], [717, 343]]), M.view, "E"),
    thing("trees", "pines and maples", poly([[96, 190], [470, 190], [470, 300], [360, 300], [260, 330], [96, 330]]), M.hut, "N"),
    thing("cherry", "late cherry", poly([[149, 159], [313, 159], [313, 234], [149, 234]]), M.path, "N"),
    thing("hut", "O-Ume's hut", poly([[57, 441], [184, 433], [219, 361], [154, 294], [82, 292], [20, 365], [27, 359], [57, 428]]), M.hut, "N"),
    thing("lantern", "lantern", poly([[140, 361], [160, 361], [160, 393], [140, 393]]), M.hut, "N"),
    thing("pathup", "east path", poly([[139, 466], [216, 472], [317, 361], [256, 360]]), M.path, "N", { verb: "Climb", use: climb("pathup") }),
    thing("stone", "stone", poly([[222, 472], [228, 408], [237, 405], [246, 405], [252, 408], [258, 472], [252, 479], [228, 479]]), M.stone, "N", { plane: "stone", use: stoneUse }),
    // the hall: its roof and walls, round its base and up to its jewel
    thing("hall", "women's hall", poly([[407, 304], [477, 136], [721, 310], [643, 471], [433, 495], [334, 452], [279, 314]]), TALK_AT.hall, "N"),
    thing("lattice", "lattice window", poly([[408, 415], [379, 408], [379, 350], [408, 352]]), M.stone, "N"),
    thing("slips", "name slips", poly([[444, 448], [494, 444], [494, 318], [444, 317]]), M.hall, "N"),
    { id: "slips2", name: "name slips", poly: [[574, 437], [615, 434], [615, 319], [574, 318]], walkTo: M.hall, face: "N", look: each("edo.shosha.slips"), use: each("edo.shosha.slips.use") },
    { id: "doors", name: "doors", poly: [[492, 329], [527, 327], [542, 327], [574, 329], [574, 439], [499, 452], [492, 452]], walkTo: M.hall, face: "N", plane: "doors",
      when: (g) => !open(g), look: each("edo.shosha.doors"), use: doorsUse },
    { id: "doors", name: "open doors", verb: "Go in", poly: [[492, 329], [521, 327], [603, 327], [603, 449], [530, 460], [525, 460], [492, 449]], walkTo: M.hall, face: "N", plane: "doors",
      when: open, look: each("edo.shosha.doors.open"), use: doorsUse },
    thing("step", "step", poly([[518, 499], [630, 484], [598, 463], [491, 475]]), M.step, "N"),
    { id: "stepball", name: "rice ball on a leaf", poly: [[563, 467], [565, 461], [571, 457], [581, 457], [587, 461], [590, 467], [588, 476], [567, 476]], walkTo: M.step, face: "N", plane: "stepball",
      look: (g) => g.say(umeIn(g) ? `edo.shosha.stepball.in.${who(g)}` : `edo.shosha.stepball.${who(g)}`), use: (g) => g.say(umeIn(g) ? `edo.shosha.stepball.in.${who(g)}` : `edo.shosha.stepball.use.${who(g)}`) },
    { id: "lock", name: "lock", verb: "Look closer at", poly: [[524, 380], [547, 380], [547, 400], [524, 400]], walkTo: M.lock, face: "N", plane: "lock",
      look: (g) => g.say(open(g) ? `edo.shosha.lock.open.${who(g)}` : `edo.shosha.lock.${who(g)}`), use: lockUse, when: (g) => !open(g) },
    thing("bench", "bench", poly([[283, 464], [287, 456], [368, 453], [383, 453], [390, 456], [385, 480], [304, 496], [294, 496], [290, 488]]), M.bench, "N", { plane: "bench" }),
    thing("combs", "heap of combs", poly([[182, 515], [255, 516], [269, 503], [201, 502]]), M.combs, "N", { use: combsUse, useWith: { note: (g) => noteRead(g, SHOSHA.combsRead) } }),
    // the people
    { id: "ryokai", name: "Ryōkai", verb: "Talk to", rect: BOX.ryokai, walkTo: TALK_AT.ryokai, face: "W", when: (g) => !open(g), look: each("edo.shosha.ryokai"), use: (g) => talkTo(g, "ryokai", RYOKAI) },
    { id: "ryokai", name: "Ryōkai", verb: "Talk to", rect: BOX.lattice, walkTo: [330, 470], face: "E", when: open, look: each("edo.shosha.ryokai"), use: (g) => talkTo(g, "ryokai", AT_LATTICE) },
    { id: "ume", name: "O-Ume", verb: "Talk to", rect: BOX.ume, walkTo: TALK_AT.ume, face: "W", when: UME_HERE, look: each("edo.shosha.ume"), use: (g) => talkTo(g, "ume", UME),
      useWith: { note: (g) => noteRead(g), natsuslip: (g) => talkTo(g, "ume", UME), fusaslip: (g) => talkTo(g, "ume", UME) } },
    { id: "tome", name: "Grandmother Tome", verb: "Talk to", rect: BOX.tome, walkTo: TALK_AT.tome, face: "N", when: ON_BENCH, look: each("edo.shosha.tome"), use: (g) => talkTo(g, "tome", TOME) },
    { id: "wife", name: "young wife", verb: "Talk to", rect: BOX.wife, walkTo: TALK_AT.wife, face: "N", when: ON_BENCH, look: each("edo.shosha.wife"), use: (g) => talkTo(g, "wife", WIFE) },
    { id: "girl", name: "girl", verb: "Talk to", rect: BOX.girl, walkTo: TALK_AT.girl, face: "N", when: ON_BENCH, look: each("edo.shosha.girl"), use: (g) => talkTo(g, "girl", GIRL) },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and as the stage is built.
  setup(g) {
    room.sunset = false;
    dressAll(g, "outdoors", true);
    const r = g.actor("ryokai");
    if (r && open(g)) r.hold(true, "peer");
  },

  async enter(g, from) {
    if (heard(g, SHOSHA.arrive[0])) return;
    await g.wait(400);
    if (from === "edo-town") await g.say(SHOSHA_MAP.way);
    const t = g.actor("tome"), w = g.actor("wife"), u = g.actor("ume");
    if (t && w) faceEach(g, t, w);
    await g.say(SHOSHA.arrive[0], SHOSHA.arrive[1]);
    if (u) u.look(M.tome[0], M.tome[1]);
    await g.say(SHOSHA.arrive[2]);
    if (t) t.face("S");
    if (w) w.face("S");
  },
};

// (the names a test or a tool may want)
export const PLACES = { M, LATTICE, DOORWAY, HOMEWARD, TALK_AT, BOX };
export { FLOOR, UME as umeTalk, RYOKAI as ryokaiTalk, TOME as tomeTalk, WIFE as wifeTalk, GIRL as girlTalk };

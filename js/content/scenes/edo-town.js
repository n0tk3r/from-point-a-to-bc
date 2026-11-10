// Act Six, the fifth leg: Himeji town, Watamachi on the highway, midday (SCENES-21C: new in round twenty-one, in place of
// ENGINE-21's stub; briefs/SCENES-21.md, and the design, briefs/out/edo2-design.md, "HIMEJI TOWN" and #36). Looking north across
// the highway: the domain's cotton office and its paper-note office at the left; the writing school with its shutters propped
// open, the girls at their low desks and the teacher kneeling; O-Tane's side yard back to her kitchen (the well, the salt, the
// rice pot, the pickle tub, the plum jar, a cloth); her house with its noren; old Tōbei's hut by the ward gate; and far up
// above the roofs, white on its hill, the keep.
//
// The three of them come here by the card "The next day" (cutscenes/edo-walk2.js) at the mark `east`, off the highway. The
// leg's start is LEG_START.town (edo-common.js).
//
//   #36 Supper For A Voice: three things to do, one for each of them, in any order
//     O-Kiku      Little Sister's: taneTree (talk/edo-d.js) says why (edo.taneMet); kikuTree: her first day had a hamster; her
//                 hand: the two of them go in hand in hand (`edo-hand` and PEOPLE-21B's `kiku-hand`), up the step stone onto
//                 the school's floor (g.climbTo), to the two free desks; the teacher's one character, "mother"; out again,
//                 hand in hand, to O-Tane at her door; O-Kiku's one word (edo.kikuIn); then O-Kiku goes back in to her desk
//     the way     Big Sister's: shizuTree: O-Shizu thanks her for the small sister, and draws the way to Shosha on practice
//                 paper, pictures and no words (edo.knowWay: the map's `shosha` shows)
//     supper      Mom's: taneTree, once O-Kiku is in: the kitchen for an hour, O-Tane's paddle (edo.kitchenLent); then the
//                 kitchen at the back, a step at a time (COOK: water, salt, rice, pickle, the cloth: edo.cook.water, .salt,
//                 .rice, .pickle, and the plum if she likes, .plum), out of order a funny line, never a failure; the cloth
//                 tied: the rice balls in her pockets (`riceball`, edo.riceballs)
//   the way to Shosha   by the map, once the way is known and supper made (the scene's `travel`: SHOSHA_MAP.nosupper before);
//                 as they go, edo.supperMade (the beat: set in `leaving`, so that the hint's last stage, "Shosha, girls",
//                 can be heard first)
//   the lane north   to the castle, the next day only (TOWN.north before; TOWN.northAfter once supper is made)
//   the highway east refuses (edo.town.highway.use.<who>)
//
// Every place is the painter's measurement (art/scenes/edo-town/layout.json, PAINT-21E's ready.md), or set by eye against the
// picture with the people in it; where the two differ the comment says why.
//
// Try it: index.html?scene=edo-town&lead=lilsis&flags=edo.inHimeji

import { STOCK_DRESSED } from "./edo-common.js";
import { THREE, who, is, heard, each, standsIn, dressAll, thingOf, faceEach, idle, chatter, swap, TALK } from "./edo-west.js";
import { taneTree, kikuTree, shizuTree, tobeiTree, TOWN, COOK, cookLines, SHOSHA_MAP } from "../talk/edo-d.js";

const art = "art/scenes/edo-town/";

// ---------- the camera and the ground (layout.json: the land camera, horizon 290, full 590) ----------
const HORIZON = 290, FULL = 590;
const STREET = [[6, 597], [794, 597], [794, 455], [796, 455], [796, 449], [722, 449], [722, 455], [508, 455], [498, 426], [391, 426], [381, 455], [6, 455]];
const SCHOOL = [[252, 423], [368, 423], [378, 407], [275, 407]];
const SCHOOL_SCALE = 0.482;

// ---------- the marks (layout.json marks) ----------
const M = { east: [772, 556], house: [552, 463], tane: [534, 457], well: [466, 450], kitchen: [406, 428], school: [287, 463], kiku: [349, 457],
  desk: [327, 415], kikuDesk: [353, 415], shizu: [370, 410], pupil1: [274, 415], pupil2: [300, 415], gate: [757, 466], north: [757, 451],
  tobei: [699, 460], hut: [688, 463], cotton: [51, 460], note: [154, 460], keep: [560, 520] };
// The step stone at the school's right end, and the way up onto its floor (layout.json floors.school: the painter's path)
const UP = [[372, 452], [366, 432]], DOWN = [[366, 432], [372, 452]];
// Hand in hand: Little Sister, and O-Kiku on her left a step behind (walking east, her left is the far side), at the step
// stone and at O-Tane's door (set by eye: their held hands between them)
const AT_STEP = { lilsis: [366, 461], kiku: [360, 457] };
const AT_TANE = { lilsis: [502, 467], kiku: [496, 463] };     // (clear of O-Tane's ground: a save puts Little Sister back just here)
const KOMUSO = [196, 466];                  // the komusō, playing at the paper-note office's door (the design: in Himeji too)
const TALK_AT = { tane: [510, 468], kiku: [328, 467], school: [362, 463], tobei: [680, 474], komuso: [214, 480] };

// ---------- the story, as the picture shows it ----------
const kikuIn = (g) => is(g, "edo.kikuIn");
const lent = (g) => is(g, "edo.kitchenLent");
const made = (g) => is(g, "edo.riceballs");
const night = (g) => is(g, "edo.nightDone");                 // the next day (the town visited from the castle)
const STEPS = COOK.order;                                    // water, salt, rice, pickle, cloth
const stepDone = (g, s) => (s === "cloth" ? made(g) : is(g, `edo.cook.${s}`));
const doneSteps = (g) => STEPS.filter((s) => stepDone(g, s));
const room = { kikuBack: false };

// ---------- #36: O-Kiku's first day ----------
function handInHand(g, on) {
  const lil = g.actor("lilsis"), kiku = g.actor("kiku");
  const wear = (g.dressOf("lilsis") || "edo").includes("hatback") ? "edo-hatback" : "edo";
  g.dress("lilsis", on ? `${wear}-hand` : wear);
  if (kiku) swap(g, "kiku", on ? "kiku-hand" : "kiku", [kiku.x, kiku.y], kiku.yaw, kiku.scale);
  if (lil && kiku) { lil.face("E"); kiku.face("E"); }
}
/** The hook `goIn`: Little Sister takes O-Kiku's hand, and the two of them go in: along to the step stone, up onto the school's
    floor (the hats off indoors), to the two free desks. */
async function goIn(g) {
  handInHand(g, true);
  await g.view.cast.load();
  await Promise.all([g.moveTo(AT_STEP.lilsis[0], AT_STEP.lilsis[1], "lilsis"), g.moveTo(AT_STEP.kiku[0], AT_STEP.kiku[1], "kiku")]);
  g.dress("lilsis", "edo-hatback-hand");
  await Promise.all([g.climbTo("desk", { path: UP, face: "W" }), g.wait(260).then(() => g.climbTo("kikuDesk", { path: UP, who: "kiku", face: "W" }))]);
  g.dress("lilsis", "edo-hatback");
  const kiku = g.actor("kiku");
  if (kiku) swap(g, "kiku", "kiku", [kiku.x, kiku.y], "S", SCHOOL_SCALE);
  await g.view.cast.load();
  const lil = g.actor("lilsis"), sh = g.actor("shizu");
  if (lil) lil.face("S");
  if (sh) sh.look(lil.x, lil.y);
}
/** The hook `comeOut`: after the lesson, down the step again hand in hand, and along to O-Tane at her door. */
async function comeOut(g) {
  const kiku = g.actor("kiku");
  g.dress("lilsis", "edo-hatback-hand");
  if (kiku) swap(g, "kiku", "kiku-hand", [kiku.x, kiku.y], "E", SCHOOL_SCALE);
  await g.view.cast.load();
  await Promise.all([g.climbTo(AT_STEP.lilsis, { path: DOWN, face: "E" }), g.wait(260).then(() => g.climbTo(AT_STEP.kiku, { path: DOWN, who: "kiku", face: "E" }))]);
  g.dress("lilsis", "edo-hand");
  const at = g.clearOf(AT_TANE.lilsis) || AT_TANE.lilsis;     // (not into Mom or Big Sister, if one of them is talking to O-Tane)
  await Promise.all([g.moveTo(at[0], at[1], "lilsis"), g.moveTo(at[0] + AT_TANE.kiku[0] - AT_TANE.lilsis[0], at[1] + AT_TANE.kiku[1] - AT_TANE.lilsis[1], "kiku")]);
  handInHand(g, false);
  const k = g.actor("kiku"), t = g.actor("tane"), lil = g.actor("lilsis");
  if (k && t) { k.look(t.x, t.y); t.look(k.x, k.y); }
  if (lil) lil.face("E");
}
const KIKU = (() => {
  const t = kikuTree({ goIn, comeOut });
  // (staging) "Look. I can write one.": she writes it in the dust at O-Tane's door; O-Kiku's word with a smile
  t.nodes.mother.say = [];
  const after = t.nodes.mother.then;
  t.nodes.mother.then = async (g) => {
    const lil = g.actor("lilsis"), k = g.actor("kiku");
    await g.reach(true);
    await g.say("edo.town.lesson.5");
    if (k) k.hold(true, "smile");
    await g.say("edo.town.lesson.6");
    await g.say("edo.town.lesson.7");
    if (k) k.hold(false);
    if (lil) lil.look(k ? k.x : lil.x, lil.y);
    return after(g);
  };
  return t;
})();
/** O-Kiku, in, goes back to her desk by herself (after her word to her mother), and stays there. */
async function kikuBackIn(g) {
  const k = g.actor("kiku");
  if (!k || room.kikuBack) return;
  room.kikuBack = true;
  await g.moveTo(AT_STEP.kiku[0], AT_STEP.kiku[1], "kiku");
  await g.climbTo("kikuDesk", { path: UP, who: "kiku", face: "S" });
  swap(g, "kiku", "kiku", M.kikuDesk, "S", SCHOOL_SCALE);
  await g.view.cast.load();
}
async function kikuUse(g) {
  const k = g.actor("kiku"), lead = g.lead;
  if (k && lead && !kikuIn(g)) { k.look(lead.x, lead.y); }
  const was = kikuIn(g);
  await g.talk(KIKU);
  if (!was && kikuIn(g)) await kikuBackIn(g);
}

// ---------- #36: the way ----------
/** O-Shizu draws the way on a scrap of practice paper (shizuTree's `way`: its lines said here, around the drawing). */
const WAY = { first: [], again: [] };
/** The hook `drawWay` (staged here: the option's lines are said in it, around the drawing, the first time; asked again, the
    short form). */
async function drawWay(g) {
  if (g.asked("shizu/way") > 1) { await g.say(...WAY.again); return; }
  const sh = g.actor("shizu"), big = g.actor("bigsis"), first = WAY.first;
  if (sh) sh.hold(true, "writing");
  await g.say(first[0], first[1]);
  if (sh) sh.hold(true, "paper");
  await g.say(first[2], first[3]);
  if (sh) sh.hold(false);
  if (big) big.look(M.shizu[0], M.shizu[1]);
  await g.say(first[4]);
}
const SHIZU = (() => {
  const t = shizuTree({ drawWay });
  const o = t.nodes.talk.options.find((x) => x.id === "way");
  WAY.first.push(...o.say[1]); WAY.again.push(...o.say.more);
  delete o.say;
  return t;
})();

// ---------- #36: supper ----------
/** The hook `kitchen`: O-Tane holds out her rice paddle, and Mom takes it: the kitchen is hers for an hour. */
async function kitchenHook(g) {
  const t = g.actor("tane"), mom = g.actor("mom");
  if (t && mom) faceEach(g, t, mom);
  if (t) t.hold(true, "paddle");
  await g.wait(500);
  if (mom) await mom.play(g.clock, "reach");
  if (t) t.hold(false);
  g.sfx("pickup");
  if (mom) mom.hold(true, "paddle");
  await g.wait(600);
  if (mom) mom.hold(false);
}
const TANE = taneTree({ kitchen: kitchenHook });
/** A step of the kitchen, by Mom: the right one in its order, or a funny line for one out of order, or "Done that part." */
async function cook(g, step) {
  const me = who(g);
  if (me !== "mom") return g.say(lent(g) ? COOK.girls[me] : `edo.town.${THING_OF[step]}.use.${me}`);
  if (!lent(g)) return g.say(`edo.town.${THING_OF[step]}.use.mom`);
  const mom = g.lead;
  if (step === "plum") {                                     // (a free extra, once the rice is shaped)
    if (!is(g, "edo.cook.rice")) return g.say(COOK.noPlum);
    if (is(g, "edo.cook.plum")) return g.say(COOK.again);
    await g.reach();
    g.flag("edo.cook.plum", true);
    return g.say(COOK.plum);
  }
  const done = doneSteps(g), lines = cookLines(done, step), right = lines === COOK.done[step];
  if (!right) { await g.say(...lines); return; }
  if (step === "water") { await g.reach(); g.sfx("splash"); g.flag("edo.cook.water", true); await g.say(lines[0]); mom.look(M.kitchen[0], M.kitchen[1] - 40); await g.say(lines[1]); return; }
  if (step === "salt") { await g.reach(); g.flag("edo.cook.salt", true); return g.say(...lines); }
  if (step === "rice") {
    mom.hold(true, "shape");
    try { await g.say(lines[0]); g.flag("edo.cook.rice", true); const big = g.actor("bigsis"); if (big) big.look(mom.x, mom.y); await g.say(lines[1]); }
    finally { mom.hold(false); }
    return;
  }
  if (step === "pickle") { await g.reach(); g.flag("edo.cook.pickle", true); return g.say(...lines); }
  if (step === "cloth") {
    mom.hold(true, "shape");
    await g.wait(500);
    mom.hold(false);
    g.give("riceball");
    g.sfx("pickup");
    g.flag("edo.riceballs", true);
    await g.say(lines[0]);
    await g.wait(300);
    await g.say(lines[1]);
  }
}
const THING_OF = { water: "bucket", salt: "saltjar", rice: "ricepot", pickle: "pickletub", cloth: "cloth", plum: "plumjar" };
/** A kitchen thing used: before the kitchen is lent its own refusal; after the cloth is tied, "Supper's made." for Mom. */
const cookUse = (step, thing = THING_OF[step]) => (g) => {
  const me = who(g);
  if (me !== "mom") return g.say(lent(g) ? COOK.girls[me] : `edo.town.${thing}.use.${me}`);
  if (!lent(g)) return g.say(`edo.town.${thing}.use.mom`);
  if (made(g)) return g.say(COOK.after);
  return cook(g, step);
};
const bucketLook = (g) => g.say(is(g, "edo.cook.water") && !night(g) ? `edo.town.bucket.up.${who(g)}` : `edo.town.bucket.${who(g)}`);
const clothLook = (g) => g.say(made(g) && !night(g) ? `edo.town.cloth.bundle.${who(g)}` : `edo.town.cloth.${who(g)}`);
async function wellLook(g) {
  if (who(g) === "lilsis") { const m = g.actor("mom"); if (m) m.look(g.lead.x, g.lead.y); return g.say(...TOWN.well); }
  return g.say(`edo.town.well.${who(g)}`);
}
const kitchenDoorUse = (g) => g.say(who(g) === "mom" && lent(g) ? "edo.town.kitchendoor.lent.use.mom" : `edo.town.kitchendoor.use.${who(g)}`);

// ---------- the people ----------
async function talkTo(g, id, tree) {
  const a = g.actor(id), lead = g.lead;
  if (a && lead) a.look(lead.x, lead.y);
  await g.talk(tree);
}
/** The hook `sweet`: Tōbei holds a sweet out from his jar, and Little Sister takes it (she eats it; no thing to carry). */
async function sweetHook(g) {
  const t = g.actor("tobei");
  if (t) t.hold(true, "sweet");
  await g.wait(500);
  await g.reach();
  if (t) t.hold(false);
}
const TOBEI = tobeiTree({ sweet: sweetHook });

// ---------- the ways ----------
/** The lane north, through the ward gate, toward the castle: tomorrow (before supper "Tomorrow. Tonight we go and listen."; after
    it, Mom: "Shosha first, girls."); the next day, the castle approach. */
async function northUse(g) {
  if (night(g)) return g.goto("edo-castle", { spawn: "enter" });
  if (made(g) && who(g) === "mom") return g.say(TOWN.northAfter);
  return g.say(TOWN.north[who(g)]);
}
const highwayUse = (g) => g.say(`edo.town.highway.use.${who(g)}`);
/** The cotton office: Big Sister's "Somebody's very clever.", and Mom's "A matter of record". */
const cottonUse = (g) => (who(g) === "bigsis" ? g.say(...TOWN.cotton) : g.say(`edo.town.cottonoffice.use.${who(g)}`));
/** Once all three are done, a little more said about the walk to come? No: the hint says it. The beat's fact goes as they go. */
function leaving(g, to) {
  if (to === "edo-shosha" && is(g, "edo.kikuIn") && is(g, "edo.knowWay") && made(g) && !is(g, "edo.supperMade")) g.flag("edo.supperMade", true);
}

// ---------- life ----------
const nearSchool = (g) => { const l = g.actor("lilsis"); return !!l && l.x > 230 && l.x < 380 && l.y > 455 && l.y < 500; };
const CHAT = chatter([
  { when: (g) => !kikuIn(g) && nearSchool(g), say: [TOWN.pupils[0]] },
  { when: (g) => kikuIn(g) && !night(g), say: [TOWN.pupils[1]] },
], { first: [10, 16], every: [30, 50] });

// ---------- the scene ----------
const thing = thingOf("town");
const poly = (p) => ({ poly: p });
const BOX = { tane: [521, 384, 26, 74], kiku: [338, 400, 21, 58], kikuIn: [343, 366, 20, 50], shizu: [362, 371, 15, 41], pupil1: [267, 380, 13, 37],
  pupil2: [293, 380, 13, 37], tobei: [687, 399, 23, 63], komuso: [183, 382, 26, 84] };

export default {
  id: "edo-town",
  era: "edo",
  name: "Watamachi, Himeji",

  horizon: HORIZON, full: FULL, minScale: 0.3,
  // the street (the usual floor) and the writing school's raised room, a floor of its own at its own size (layout.json floors):
  // the school's things are asked from the street; Little Sister and O-Kiku go up by the step stone (g.climbTo)
  walk: [{ name: "street", area: STREET }, { name: "school", area: SCHOOL, scale: SCHOOL_SCALE, away: each("edo.town.school.use") }],
  // the well's curb, the pickle tub, the rice pot, the mortar, the pan, the bales (layout.json blocked)
  blocked: [[[506, 441], [501, 439], [490, 438], [478, 438], [468, 439], [464, 441], [469, 443], [479, 445], [493, 445], [503, 443]], [[473, 429], [470, 428], [461, 427], [453, 428], [450, 429], [453, 430], [462, 431], [470, 430]],
    [[454, 426], [451, 425], [443, 424], [435, 425], [431, 426], [435, 427], [443, 427], [451, 427]], [[460, 440], [457, 439], [449, 438], [441, 439], [438, 440], [441, 441], [449, 442], [457, 441]],
    [[404, 446], [400, 445], [392, 445], [383, 445], [379, 446], [382, 447], [391, 447], [400, 447]], [[-175, 453], [-144, 453], [-127, 449], [-157, 449]], [[-162, 458], [-131, 458], [-113, 453], [-144, 453]],
    [[74, 453], [105, 453], [115, 449], [85, 449]], [[94, 453], [125, 453], [134, 449], [104, 449]], [[73, 458], [105, 458], [115, 453], [84, 453]],
    // PAINT-23 (round twenty-three): the street behind the near post at the left edge (the front plane): nobody walks out of sight there
    [[6, 455], [34, 455], [34, 597], [6, 597]]],

  party: THREE,
  spawn: { default: M.east, ...M },
  // Off the highway from the east (the card); and back from the castle by the lane, at the gate
  arrive: { east: [[742, 576], [724, 548]], gate: [[735, 474], [776, 478]] },
  facing: "W",
  stock: STOCK_DRESSED,
  talk: TALK,
  // ENGINE-17/21: by the map, Shosha only once supper is made (and never the next day: Shosha has done its part)
  travel: (g) => (night(g) ? SHOSHA_MAP.done : made(g) ? true : SHOSHA_MAP.nosupper),
  leaving,
  edges: { E: { name: "back east along the highway", walkTo: [788, 560], use: highwayUse } },
  tick(g, dt) { CHAT.tick(g, dt); },

  picture: art + "back.png",
  // CUT-OUTS, back to front (the painter's plan): the two noren (behind everybody, stirring), the school's desks (a girl
  // kneeling behind one is behind it), the school's front (its opening clear: everybody inside is behind it), the kitchen
  // door, the jars and the cloth on the shelf, the rice pot, the pickle tub, the well and its bucket, the ward gate. By day the
  // shutters, the kitchen door and the gate are open (their shut states are "Mind The Fire"'s, by night).
  planes: [
    { id: "noren-cotton", src: art + "noren-cotton.png", plane: "back" },
    { id: "noren", src: art + "noren.png", plane: "back" },
    { id: "desks", src: art + "desks.png", base: 419 },
    { id: "shutters", base: 450, states: { open: art + "shutters.png", shut: art + "shutters-shut.png" }, state: "open" },
    { id: "kitchendoor", base: 423, states: { shut: art + "kitchendoor.png", open: art + "kitchendoor-open.png" }, state: "open" },
    { id: "saltjar", src: art + "saltjar.png", base: 424 },
    { id: "plumjar", src: art + "plumjar.png", base: 424 },
    { id: "cloth", base: 424, states: { folded: art + "cloth.png", bundle: art + "cloth-bundle.png" }, state: (g) => (made(g) && !night(g) ? "bundle" : "folded") },
    { id: "ricepot", src: art + "ricepot.png", base: 427, solid: [[454, 426], [450, 425], [443, 424], [435, 425], [432, 426], [435, 427], [443, 427], [450, 427]] },
    { id: "pickletub", src: art + "pickletub.png", base: 431, solid: [[472, 429], [469, 428], [461, 427], [454, 428], [450, 429], [454, 430], [462, 431], [469, 430]] },
    { id: "well", src: art + "well.png", base: 444, solid: [[505, 441], [500, 439], [490, 438], [478, 438], [469, 439], [465, 441], [469, 443], [480, 445], [492, 445], [502, 443]] },
    { id: "bucket", base: 445, states: { up: art + "bucket.png", down: art + "bucket-down.png" }, state: (g) => (is(g, "edo.cook.water") && !night(g) ? "up" : "down") },
    { id: "gate", base: 452, states: { open: art + "gate.png", shut: art + "gate-shut.png" }, state: "open" },
    // PAINT-23 (round twenty-three, tools/paint/DEPTH.md): the near plane, in front of everybody: the eave of a house on our own
    // side of the highway across the top left and its post down the left edge; the hem of the next shop's curtain across the
    // top right corner (it stirs). Nothing in it is clicked, and nothing clicked or stood on is behind it.
    { id: "near", src: art + "near.png", plane: "front" },
    { id: "near-noren", src: art + "near-noren.png", plane: "front" },
  ],

  // THINGS THAT MOVE BY NATURE (layout.json fx): the kitchen's smoke (hidden behind the houses' upper storeys), the two noren
  // stirring, a kite wheeling over the castle's hill, sparrows on the street.
  fx: [
    { id: "kitchen-smoke", type: "smoke", at: [436, 344], base: 423, height: 90, width: [3, 16], lean: [14, -90], rise: 12, rate: 2, color: "#e4e6ea", opacity: 0.28,
      behind: [[[236, 0], [380, 0], [380, 330], [236, 330]], [[509, 0], [660, 0], [660, 330], [509, 330]]], behindOpacity: 0.0 },
    { id: "noren", type: "sway", plane: "noren", anchor: "top", amount: 1.2, period: 3.8 },
    { id: "noren-cotton", type: "sway", plane: "noren-cotton", anchor: "top", amount: 1.0, period: 4.2 },
    { id: "kite", type: "birds", circle: { at: [600, 110], r: [70, 24] }, count: 1, speed: 12, size: 7, plane: "back" },
    { id: "sparrows", type: "birds", area: [[120, 500], [420, 494], [440, 560], [100, 566]], count: 4, look: "sparrow", size: 14, depth: true, shy: 120 },
    { id: "near-noren", type: "sway", plane: "near-noren", anchor: "top", amount: 1.6, period: 4.6 },     // PAINT-23: the near curtain stirs
  ],

  // The people: O-Tane at her door, O-Kiku outside the school in her best (then in, at her desk), O-Shizu kneeling at the
  // room's right end, two pupils at their desks, old Tōbei on his stool by his hut, and the komusō playing at a door.
  actors: [
    { id: "tane", kind: "tane", at: M.tane, face: "S", life: { fidget: [5, 10], still: true } },
    { id: "kiku", kind: "kiku", at: M.kiku, face: "S", when: (g) => !kikuIn(g), life: { fidget: [4, 9], still: true } },
    { id: "kiku", kind: "kiku", at: M.kikuDesk, scale: SCHOOL_SCALE, face: "S", when: kikuIn, life: { fidget: [6, 12], still: true } },
    { id: "shizu", kind: "shizu", at: M.shizu, scale: SCHOOL_SCALE, face: "W", life: { fidget: [6, 12], still: true } },
    { id: "pupil1", kind: "pupil1", at: M.pupil1, scale: SCHOOL_SCALE, face: "S", life: { fidget: [4, 9], still: true } },
    { id: "pupil2", kind: "pupil2", at: M.pupil2, scale: SCHOOL_SCALE, face: "S", life: { fidget: [4, 9], still: true } },
    { id: "tobei", kind: "tobei", at: M.tobei, face: "S", life: { fidget: [6, 12], still: true } },
    { id: "komuso", kind: "komuso-play", at: KOMUSO, face: "N", life: { fidget: [5, 9], still: true } },
  ],

  // Back to front: a later area lies over an earlier one (layout.json things; the people's boxes against their figures).
  hotspots: [
    // (PAINT-23: the town's roofs, row behind row up to the castle's hill, and the keep, larger and turned: their areas measured again)
    thing("roofs", "roofs", poly([[236, 189], [800, 189], [800, 252], [236, 252]]), M.keep, "N"),
    thing("keep", "the keep", poly([[633, 115], [638, 171], [633, 172], [495, 170], [500, 114], [530, 46], [538, 29], [555, 18], [577, 17], [595, 30]]), M.keep, "N"),
    thing("storehouse", "storehouse", poly([[391, 340], [505, 340], [505, 300], [391, 300]]), M.well, "N"),
    thing("cottonoffice", "cotton office", poly([[0, 452], [127, 452], [127, 104], [0, 104]]), M.cotton, "N", { use: cottonUse }),
    thing("noteoffice", "paper-note office", poly([[127, 452], [234, 452], [234, 104], [127, 104]]), M.note, "N"),
    thing("house", "O-Tane's house", poly([[513, 452], [640, 452], [640, 336], [513, 336]]), M.house, "N"),
    thing("school", "writing school", poly([[234, 452], [376, 452], [376, 336], [234, 336]]), M.school, "N"),
    // the side yard: its back wall (its floor is walked on)
    thing("passage", "side passage", poly([[387, 330], [502, 330], [502, 424], [387, 424]]), M.well, "N"),
    thing("hut", "Tōbei's hut", poly([[646, 454], [707, 454], [707, 335], [646, 335]]), M.hut, "N"),
    thing("gate", "ward gate", poly([[799, 319], [799, 455], [711, 455], [694, 330], [694, 329], [756, 301], [759, 301], [799, 318]]), M.gate, "N", { plane: "gate" }),
    thing("lane", "lane north", poly([[722, 448], [796, 448], [796, 330], [722, 330]]), M.gate, "N", { verb: "Go up", use: northUse }),
    // the highway: a strip of it at the bottom (a click elsewhere on the street walks; the east edge's band is clear of it)
    thing("highway", "highway", poly([[40, 576], [752, 576], [752, 598], [40, 598]]), [400, 570], "S"),
    // the bales of cloth at the cotton office's front (the painter's shape ran along every front: these are the bales themselves)
    thing("bales", "bales of cotton", poly([[74, 458], [134, 458], [134, 404], [74, 404]]), M.cotton, "N"),
    // the kitchen at the back of the yard, and its things: Mom's, for an hour
    thing("kitchendoor", "kitchen door", poly([[388, 346], [428, 346], [428, 426], [388, 426]]), M.kitchen, "N", { plane: "kitchendoor", use: kitchenDoorUse }),
    thing("well", "well", poly([[462, 345], [507, 345], [507, 350], [505, 443], [501, 445], [498, 446], [475, 446], [470, 445], [467, 444], [465, 443], [462, 350]]), M.well, "N",
      { plane: "well", look: wellLook, use: cookUse("water", "well") }),
    thing("bucket", "bucket", poly([[475, 378], [480, 353], [489, 353], [502, 385], [504, 394], [508, 441], [508, 446], [507, 446], [482, 417], [474, 390]]), M.well, "N",
      { plane: "bucket", look: bucketLook, use: cookUse("water") }),
    thing("ricepot", "rice pot", poly([[453, 429], [432, 429], [431, 423], [429, 414], [429, 401], [440, 398], [457, 398], [458, 398], [459, 399], [460, 400]]), M.kitchen, "N", { plane: "ricepot", use: cookUse("rice") }),
    thing("saltjar", "salt jar", poly([[428, 388], [427, 371], [430, 368], [441, 368], [444, 371], [443, 388]]), M.kitchen, "N", { plane: "saltjar", use: cookUse("salt") }),
    thing("plumjar", "plum jar", poly([[442, 387], [441, 371], [444, 368], [455, 367], [458, 370], [460, 377], [459, 382], [457, 388]]), M.kitchen, "N", { plane: "plumjar", use: cookUse("plum") }),
    thing("cloth", "cloth", poly([[472, 388], [455, 388], [454, 386], [451, 374], [451, 373], [455, 371], [471, 371], [476, 373], [476, 374], [474, 385]]), M.kitchen, "N",
      { plane: "cloth", look: clothLook, use: cookUse("cloth") }),
    thing("pickletub", "pickle tub", poly([[473, 431], [450, 431], [448, 429], [447, 415], [448, 410], [460, 403], [466, 403], [469, 405], [475, 411], [474, 429]]), M.kitchen, "N", { plane: "pickletub", use: cookUse("pickle") }),
    thing("pan", "clay pan", poly([[378, 420], [407, 420], [407, 449], [378, 449]]), M.well, "N"),
    thing("mortar", "mortar", poly([[438, 429], [459, 429], [459, 440], [438, 440]]), M.well, "N"),
    // the school's things (asked from the street: its floor is another)
    thing("desks", "desks", poly([[254, 420], [254, 407], [256, 405], [278, 404], [366, 404], [367, 405], [367, 406], [366, 420]]), M.school, "N", { plane: "desks" }),
    thing("hutsandals", "straw sandals", poly([[657, 371], [707, 371], [707, 405], [657, 405]]), M.hut, "N"),
    thing("sweets", "jar of sweets", poly([[657, 397], [675, 397], [675, 415], [657, 415]]), M.hut, "N"),
    thing("clappers", "clappers", poly([[644, 390], [657, 390], [657, 419], [644, 419]]), M.hut, "N"),
    // the people
    { id: "pupil1", name: "pupil", rect: BOX.pupil1, walkTo: M.school, face: "N", look: each("edo.town.pupil1"), use: each("edo.town.pupil1.use") },
    { id: "pupil2", name: "pupil", rect: BOX.pupil2, walkTo: M.school, face: "N", look: each("edo.town.pupil2"), use: each("edo.town.pupil2.use") },
    { id: "shizu", name: "O-Shizu", verb: "Talk to", rect: BOX.shizu, walkTo: TALK_AT.school, face: "N", look: each("edo.town.shizu"), use: (g) => talkTo(g, "shizu", SHIZU) },
    { id: "kiku", name: "O-Kiku", verb: "Talk to", rect: BOX.kiku, walkTo: TALK_AT.kiku, face: "E", when: (g) => !kikuIn(g), look: each("edo.town.kiku"), use: kikuUse },
    { id: "kiku", name: "O-Kiku", verb: "Talk to", rect: BOX.kikuIn, walkTo: TALK_AT.school, face: "N", when: kikuIn, look: each("edo.town.kiku.in"), use: kikuUse },
    { id: "tane", name: "O-Tane", verb: "Talk to", rect: BOX.tane, walkTo: TALK_AT.tane, face: "E", look: each("edo.town.tane"), use: (g) => talkTo(g, "tane", TANE) },
    { id: "tobei", name: "Tōbei", verb: "Talk to", rect: BOX.tobei, walkTo: TALK_AT.tobei, face: "E", look: each("edo.town.tobei"), use: (g) => talkTo(g, "tobei", TOBEI) },
    { id: "komuso", name: "komusō", rect: BOX.komuso, walkTo: TALK_AT.komuso, face: "W", look: each("edo.town.komuso"), use: (g) => { g.sfx("komuso"); return g.say(`edo.town.komuso.use.${who(g)}`); } },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and as the stage is built.
  setup(g) {
    room.kikuBack = false;
    dressAll(g, "outdoors", true);
    // Little Sister on the school's floor (a game saved in the lesson: there is none at rest; and none after): hat on her back
    const lil = g.actor("lilsis");
    if (lil && g.floors.length > 1 && g.floorOf(lil) && g.floorOf(lil).name === "school") g.dress("lilsis", "edo-hatback");
    const sh = g.actor("shizu");
    if (sh) sh.hold(true, "writing");
    CHAT.reset();
  },

  async enter(g) {
    if (heard(g, TOWN.arrive[0]) || is(g, "edo.nightDone")) return;          // (the arrival once: not the morning after, from the castle)
    await g.wait(400);
    const lil = g.actor("lilsis");
    if (lil) lil.look(M.keep[0], 120);
    await g.say(TOWN.arrive[0]);
    await g.say(TOWN.arrive[1], TOWN.arrive[2]);
  },
};

// (the names a test or a tool may want)
export const PLACES = { M, UP, DOWN, AT_STEP, AT_TANE, KOMUSO, TALK_AT, BOX };
export { STREET, SCHOOL, SCHOOL_SCALE, KIKU as kikuTalk, SHIZU as shizuTalk, TANE as taneTalk, TOBEI as tobeiTalk, THING_OF };

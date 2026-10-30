// Act Six, the first leg: Kihei's shop in Yui, inside (SCENES-20A: new in round twenty, in place of ENGINE-20's sketch; the
// design, briefs/out/edo-design.md, sections 5 and 7; every line is WRITE-20A's, js/content/lines/edo-a.en.js, and the
// talks are js/content/talk/edo-a.js). An earth-floored front open to the street, the bay and Fuji framed in the opening;
// tubs of fish, the long cutting board, fish hung to dry, the sushi box on its stand, the hearth and its pot; the raised
// room of mats at the back where guests are fed (its edge, the step, is where they sit), O-Tami's clothes chest, the money
// box with its strings of square-holed coins, the god-shelf high on the wall, the print of Fuji in the new blue on the
// post; the cat.
//
// Mom, Big Sister and Little Sister are here together (`party`). What happens here:
//   the clerk's pass  (#22, step 1) the first time they come in: O-Tami has them in behind the noren and talks weather at
//                     the clerk in the opening until he goes (edo.clerkPassed); Kihei, who was out front, comes in after them
//   #22 Out Of Sight  the baby on O-Tami's back, who has not slept in three days: Mom takes her, and hums, and she sleeps in
//                     the middle of her mother's sentence (edo.babySleeps), and goes into her basket; then the kimonos from
//                     the chest (edo.clothes: the three in O-Tami's clothes, the hats on their backs indoors)
//   #21 Where, And When  Kihei's red (O-Tami: a tiger year), the money box (Kan'ei coins), the print (the new blue); with all
//                     three, Big Sister works the year out aloud and the act's card comes up (edo-yui.js whenSolved)
//   #23 Kihei's Table the price that is not a price: he presses mackerel sushi in the box, sets it on the step, the three
//                     sit and eat; Little Sister's grace; the bow to the god-shelf; "Arigato"; "Okage-sama de"; the cat and the
//                     mackerel, and Little Sister under the floor; the rest wrapped for the road (sushibox; edo.fed)
//   #24 West          Kihei names the ship (edo.kiheiWest)
//   and a look and a use for each of the three at every thing, and the people's own words.
//
// Every place is the painter's (art/scenes/edo-fishshop/layout.json, PAINT-20B's ready.md: the camera, the walk, the marks,
// the seats on the step, the cut-outs and their states, the cat's frames), or was set by eye with the people in it.
//
// Try it: index.html?scene=edo-fishshop&lead=mom&flags=edo.arrived   (the clerk's pass first, without edo.clerkPassed)

import { stockFor, STOCK } from "./edo-common.js";
import { tamiTree, kiheiTree } from "../talk/edo-a.js";
import { THREE, who, is, heard, each, lookUse, dressFor, swap, walkOf, look, TALK, giveNo, COMBINE, undoMoment, sitOnStep, standFromStep, whenSolved, keepHers } from "./edo-yui.js";
import { scaleAt } from "../../engine/walk.js";

const art = "art/scenes/edo-fishshop/";

// ---------- the marks (layout.json marks and seats) ----------
const M = {
  door: [328.5, 361.6], kihei: [167.3, 393.7], press: [274.1, 420.3], tami: [214.5, 439.7], step: [421.9, 400.2],
  stepmom: [415.0, 385.4], stepbig: [421.9, 400.2], steplil: [430.1, 417.6], baby: [412.3, 429.0], hearth: [259.9, 441.9],
  print: [399.8, 362.3], money: [393.8, 387.9], godshelf: [408.3, 423.6], cat: [328.5, 403.7], under: [410.0, 397.9],
  tubs: [204.9, 380.2], board: [196.2, 392.9], chest: [402.8, 408.1], noren: [344.6, 359.5],
};
const SEAT = { mom: M.stepmom, bigsis: M.stepbig, lilsis: M.steplil };
// Behind the curtain (the clerk's pass), and where the kimonos are put on: in from the opening, by the step.
const IN = { mom: [384, 392], bigsis: [360, 424], lilsis: [410, 428] };      // (clear of the cat at her place)
const TAMI_OPEN = [292, 368];                     // O-Tami in the opening, talking weather at the clerk
const CLERK = { from: [404, 347], stop: [336, 347], to: [282, 347] };     // Tokuzo outside, along the street, in the middle bay
const HIDE = { mom: [404, 386], bigsis: [382, 408], lilsis: [410, 426] };   // the three, in out of the opening (the clerk in view past them)
const KIHEI_DOOR = [330, 366];                    // Kihei in from the street, after them
const KIHEI_PRESS = [187, 396];                   // behind the stand, the box in front of him (the stand hides his shins)
const KIHEI_OUT = [250, 404];                     // the way out of his place, round the stand's end
const KIHEI_SERVE = [402, 433];                   // at the step's end, setting the board down beside the three
const KIHEI_WAIT = [300, 424], TAMI_WAIT = [266, 433];      // the two of them, standing, while the three eat
const TAMI_SIDE = [252, 437];                     // beside O-Tami, to take the baby
const TAMI_DRESS = [318, 428];                    // O-Tami before the three with the clothes
// The food on the step: the pieces Kihei cut, on their board (sushibox-cut.png's board, its foot [188, 394] on the stand),
// set on the mats beside the three: 45 cm up at the depth of the middle seat.
const FOOD = { at: [468, 366], foot: [188, 394], scale: 0.88, base: 392 };
const BOARD_TOP = [150, 405];                     // the cat, behind the stand, up on the cutting board (out of sight)
const CAT_STOP = [356, 424];                      // and down again, the mackerel in her mouth, looking at them all

/** What the scene is doing that is not saved (made again whenever it is built). */
export const shop = { meal: false, gullAt: 0 };

// ---------- people ----------
/** Turn someone of the shop to the one being played. */
function faceLead(g, id) { const a = g.actor(id), l = g.lead; if (a && l) a.look(l.x, l.y); }
/** Kihei at his board, cutting (what he does whenever nothing else is asked of him). */
function atWork(g) {
  const k = g.actor("kihei");
  if (!k || shop.meal) return;
  k.face("W");
  if (k.hold) k.hold(true, "cut");
}
/** Kihei back to his board from wherever the meal left him. */
async function kiheiHome(g) {
  const k = g.actor("kihei");
  if (!k) return;
  if (k.hold) k.hold(false);
  await walkOf(g, "kihei", [KIHEI_OUT, [236, 398], M.kihei]);
  atWork(g);
}

// ---------- the cat (her frames are cut-outs: cat.json, PAINT-20B; painted facing E at the size of the row `full`) ----------
const CAT = { sit: ["cat-sit-0.png", "cat-sit-1.png"], sleep: ["cat-sleep-0.png", "cat-sleep-1.png"], walk: ["cat-walk-0.png", "cat-walk-1.png", "cat-walk-2.png", "cat-walk-3.png"],
  run: ["cat-run-0.png", "cat-run-1.png", "cat-run-2.png"], under: ["cat-under-0.png", "cat-under-1.png", "cat-under-2.png"] };
const CAT_FPS = { sit: 1.2, sleep: 0.8, walk: 8, run: 12, under: 6 };
const catScale = (y) => Math.max(0.3, (y - 200) / (401 - 200));
const catPlane = (pose, at, when) => ({ id: pose === "sit" ? "cat" : `cat-${pose}`, frames: CAT[pose].map((f) => art + f), fps: CAT_FPS[pose], at, foot: [32, 38],
  scale: catScale(at[1]), base: at[1], when });
const CAT_POSES = ["sit", "sleep", "walk", "run", "under"];
/** Show the cat in one pose (hide the others), facing E or W, at a place. */
function catAs(g, pose, at = null, face = null) {
  let shown = null;
  for (const p of CAT_POSES) {
    const c = g.plane(p === "sit" ? "cat" : `cat-${p}`);
    if (!c) continue;
    if (p !== pose) { c.show(false); continue; }
    c.show(true); shown = c;
    if (at) { c.place(at[0], at[1], catScale(at[1])); c.base = at[1]; }
    if (face) c.flag("mirror", face === "W");
  }
  return shown;
}
/** The cat goes from one place to another (walking or running), on the game clock. */
async function catGo(g, pose, from, to, speed) {
  const c = catAs(g, pose, from, to[0] < from[0] ? "W" : "E");
  if (!c) return;
  const ms = (Math.hypot(to[0] - from[0], (to[1] - from[1]) * 2) / speed) * 1000;
  await g.tween(ms, (k) => { const x = from[0] + (to[0] - from[0]) * k, y = from[1] + (to[1] - from[1]) * k; c.place(x, y, catScale(y)); c.base = y; });
}
/** #23: the cat takes a mackerel off the board (between Okage-sama de and Mom's "The cat has a mackerel"): up from her place
    (or awake: the baby's lullaby put her to sleep), behind the stand to the board, and down again with the fish. */
async function catGrabs(g) {
  await catGo(g, "walk", M.cat, [236, 410], 60);
  await catGo(g, "walk", [236, 410], BOARD_TOP, 60);                     // (behind the stand: out of sight)
  catAs(g, null);
  await g.wait(700);
  await catGo(g, "run", BOARD_TOP, CAT_STOP, 150);
  const c = catAs(g, "run", CAT_STOP, "E");
  if (c) c.flag("still", true);                                         // stopped, the fish in her mouth, looking at them
  for (const id of ["mom", "bigsis", "kihei", "tami"]) look(g, id, CAT_STOP);
}

// ---------- #23: Kihei's table (kiheiTree's meal, and the staging between its nodes) ----------
/** The rice into the box, the fish on the rice, the lid, his weight on it, the cut: behind his stand, the box before him. */
async function press(g) {
  shop.meal = true;
  const k = g.actor("kihei"), box = g.plane("sushibox");
  if (k && k.hold) k.hold(false);
  await walkOf(g, "kihei", [KIHEI_PRESS]);
  if (k) k.face("S");
  for (const id of THREE) look(g, id, [188, 380]);
  if (k) await k.play(g.clock, "reach");                                 // the rice, the fish
  if (box) box.set("filled");                                            // the lid on, the weight stone on the lid
  g.sfx("press");
  if (k && k.hold) k.hold(true, "press");                                // and his weight on it
  await g.wait(1500);
  g.sfx("press");
  await g.wait(700);
  if (k && k.hold) k.hold(false);
  if (k) await k.play(g.clock, "reach");
  if (box) box.set("cut");                                               // turned out on its board, and cut in six
  g.sfx("press");
  await g.wait(600);
}
/** He takes the board of cut pieces to the step and sets it down on the mats; the three sit on the step to eat. */
async function serve(g) {
  const k = g.actor("kihei"), box = g.plane("sushibox");
  if (box) box.set("empty");
  if (k && k.hold) k.hold(true, "board");
  await Promise.all([
    walkOf(g, "kihei", [KIHEI_OUT, KIHEI_SERVE]),
    sitOnStep(g, "mom", SEAT.mom), sitOnStep(g, "bigsis", SEAT.bigsis), sitOnStep(g, "lilsis", SEAT.lilsis),
  ]);
  if (k) k.look(FOOD.at[0], FOOD.at[1] + 30);
  if (k && k.hold) k.hold(false);
  const food = g.plane("food");
  if (food) food.show(true);
  await g.wait(300);
  await walkOf(g, "kihei", [KIHEI_WAIT]);
  await walkOf(g, "tami", [TAMI_WAIT]);
  for (const id of ["kihei", "tami"]) look(g, id, SEAT.bigsis);
  // Little Sister's grace: the three of them, hands folded, heads down
  for (const id of THREE) { const f = g.actor(id); if (f && f.pray) f.pray(true); }
  await g.wait(400);
}
/** After the grace: Kihei and O-Tami wait, puzzled and polite, and then bow to the god-shelf, and say nothing. */
async function bow(g) {
  for (const id of THREE) { const f = g.actor(id); if (f && f.pray) f.pray(false); }
  const k = g.actor("kihei"), t = g.actor("tami");
  await g.wait(900);
  for (const f of [k, t]) if (f) f.look(650, 170);
  await g.wait(400);
  await Promise.all([k && k.fidget ? k.fidget("ojigi") : null, t && t.fidget ? t.fidget("ojigi") : null]);
  await g.wait(300);
  for (const id of ["kihei", "tami"]) look(g, id, SEAT.bigsis);
}
/** Eating (between "Eat, girls" and the word): what each of them thinks of it (WRITE-20A's food lines, said at the table). */
async function eating(g) {
  await g.say("edo.shop.food.use.lilsis", "edo.shop.food.use.mom", "edo.shop.food.lilsis");
  await g.say("edo.shop.food.bigsis", "edo.shop.food.use.bigsis", "edo.shop.food.mom");
  const k = g.actor("kihei");
  if (is(g, "edo.arigato") && k && k.hold) k.hold(true, "smile");        // the word is coming: his face does something
}
/** The cat dashes under the raised floor with her mackerel; Little Sister goes under after her (I FIT), and comes back
    out with it, and a cobweb. */
async function under(g) {
  const k = g.actor("kihei");
  if (k && k.hold) k.hold(false);
  const c = catAs(g, "run", CAT_STOP, "E");
  if (c) c.flag("still", false);
  await catGo(g, "run", CAT_STOP, M.under, 150);
  catAs(g, "under", M.under, "E");
  await g.wait(520);
  catAs(g, null);
  const l = g.actor("lilsis");
  if (!l) return;
  await standFromStep(g, "lilsis");
  await g.walkTo(M.under[0] - 2, M.under[1] + 2, "lilsis");
  l.face("E");
  if (l.hold) l.hold(true, "crawl");
  const [x, y] = [l.x, l.y];
  await g.tween(380, (q) => { l.place(x + 10 * q, y - 2 * q); l.fade(1 - q); });
  await g.wait(1300);
  await g.tween(380, (q) => { l.place(x + 10 * (1 - q), y - 2 * (1 - q)); l.fade(q); });
  if (l.hold) l.hold(false);
  l.face("W");
  await g.walkTo(378, 428, "lilsis");                                            // (out from under the floor, and clear of the step)
  look(g, "lilsis", "mom");
  g.rememberPlace("lilsis");
}
/** O-Tami wraps the rest for the road (the board off the step) and puts it in the hands of the one being played; the
    three get up from the step; Kihei goes back to his board. */
async function giveBox(g) {
  const t = g.actor("tami"), food = g.plane("food");
  await walkOf(g, "tami", [M.godshelf]);
  if (t) t.look(FOOD.at[0], FOOD.at[1] + 30);
  if (t) await t.play(g.clock, "reach");
  if (food) food.show(false);
  await g.wait(300);
  const me = who(g);
  await standFromStep(g, me);
  const l = g.lead;
  if (t && l) { await walkOf(g, "tami", [[Math.min(l.x - 30, 396), Math.max(l.y + 6, 404)]]); t.look(l.x, l.y); await t.play(g.clock, "reach"); }
  g.give("sushibox");
  shop.meal = false;
  await Promise.all([...THREE.filter((id) => id !== me).map((id) => standFromStep(g, id)), kiheiHome(g), walkOf(g, "tami", [M.tami])]);
  const tt = g.actor("tami");
  if (tt) tt.face("W");
  await Promise.all(THREE.map((id) => g.walkTo(IN[id][0], IN[id][1], id)));         // (off the step, out into the shop)
  for (const id of THREE) look(g, id, M.kihei);
}

/** The talk as WRITE-20A wrote it, with the staging between some of its nodes (the tree's own lines, in its own order):
    a node's `then` (what comes after its lines) runs `before` first. */
function after(tree, node, before) {
  const spec = tree.nodes[node], then = spec.then;
  tree.nodes[node] = { ...spec, then: async (g) => { await before(g); return typeof then === "function" ? then(g) : then; } };
}
/** A clue just in (#21): the year, if it was the last of the three. */
async function clueIn(g) {
  // the red after the coins: the coins' second thought, which needs the tiger
  if (is(g, "edo.clue.red") && is(g, "edo.clue.coins") && !heard(g, "edo.shop.money.clue.2")) await g.say("edo.shop.money.clue.2");
  await whenSolved(g);
}
const KIHEI = kiheiTree({ press, serve, bow, under, giveBox });
after(KIHEI, "eat", eating);
after(KIHEI, "thanks", catGrabs);
for (const node of ["mom", "big"]) for (const o of KIHEI.nodes[node].options) if (o.id.startsWith("print")) o.do = clueIn;

async function kiheiTalk(g) {
  const k = g.actor("kihei");
  if (k && k.hold) k.hold(false);
  faceLead(g, "kihei");
  await g.talk(KIHEI);
  atWork(g);
}
/** Little Sister's three pennies on Kihei: no hole; he gives them back, and presses the sushi anyway. */
async function kiheiPennies(g) {
  const k = g.actor("kihei");
  if (k && k.hold) k.hold(false);
  faceLead(g, "kihei");
  if (is(g, "edo.pennyShown")) return g.say("edo.shop.penny.3");
  await g.say("edo.shop.penny.1", "edo.shop.penny.2", "edo.shop.penny.3", "edo.shop.penny.4");
  g.flag("edo.pennyShown", true);
  g.flag("edo.kiheiMet", true);
  if (!is(g, "edo.fed")) await g.talk({ ...KIHEI, start: () => "meal" });
  atWork(g);
}
async function kiheiEgg(g) {
  faceLead(g, "kihei");
  await g.say("edo.shop.egg.kihei");
  if (who(g) === "lilsis") await g.say("edo.shop.egg.lilsis");
}

// ---------- #22: O-Tami, the baby, the kimonos ----------
/** Mom takes the baby off O-Tami's back, rocks her and hums (a tune with no words: the sound `lullaby`), until she sleeps. */
async function lullaby(g) {
  const t = g.actor("tami"), m = g.actor("mom");
  await g.walkTo(TAMI_SIDE[0], TAMI_SIDE[1], "mom");
  if (m && t) { m.look(t.x, t.y); t.look(m.x, m.y); }
  if (t && t.hold) t.hold(false);
  await g.wait(300);
  swap(g, "tami", "tami");                                               // the baby off her back
  g.dress("mom", "baby");                                                // and in Mom's arms
  const mm = g.actor("mom");
  g.sfx("lullaby");
  for (let n = 0; n < 2; n++) if (mm && mm.fidget) await mm.fidget("rockbaby"); else await g.wait(3600);
  if (mm && mm.fidget) mm.fidget(null);
  const cat = g.plane("cat");                                            // the whole shop goes quiet (the cat too)
  if (cat && !is(g, "edo.catGone")) catAs(g, "sleep", M.cat, "W");
  await g.wait(500);
}
/** Mom lays the sleeping baby in her basket on the mats (after O-Tami's "The chest. Come to the chest."). */
async function layDown(g) {
  const m = g.actor("mom");
  await g.walkTo(M.baby[0], M.baby[1], "mom");
  if (m) { m.face("E"); await g.wait(400); }
  g.dress("mom", null);
  if (m) await g.actor("mom").play(g.clock, "reach");
  await g.wait(300);
  g.rebuildSpots();
}
/** The kimonos from the chest: O-Tami fetches them, and says edo.shop.dress.1 to .13; each of the three is in hers as
    O-Tami hands it over (Mom after "Arms up", Big Sister after "It was long on me", Little Sister after "Keep them"), the
    hats down their backs indoors. */
async function dress(g) {
  const t = g.actor("tami");
  await Promise.all([...THREE.map((id) => g.walkTo(IN[id][0], IN[id][1], id)), walkOf(g, "tami", [[300, 430], [372, 424], M.chest])]);
  if (t) t.face("E");
  await g.wait(600);
  if (t && t.hold) t.hold(true, "clothes");
  await walkOf(g, "tami", [TAMI_DRESS]);
  for (const id of THREE) look(g, id, TAMI_DRESS);
  const into = async (id) => {
    if (t) t.look(IN[id][0], IN[id][1]);
    const f = g.actor(id);
    if (f) await g.tween(180, (k) => f.fade(1 - k));
    g.dress(id, "edo-hatback");
    const n = g.actor(id);
    if (n) { n.fade(0); await g.tween(240, (k) => n.fade(k)); }
  };
  if (t) t.look(IN.mom[0], IN.mom[1]);
  await g.say("edo.shop.dress.1");
  await into("mom");
  await g.say("edo.shop.dress.2", "edo.shop.dress.3");
  await into("bigsis");
  await g.say("edo.shop.dress.4", "edo.shop.dress.5", "edo.shop.dress.6", "edo.shop.dress.7", "edo.shop.dress.8", "edo.shop.dress.9");
  look(g, "tami", "lilsis");
  await g.say("edo.shop.dress.10", "edo.shop.dress.11");
  await into("lilsis");
  if (t && t.hold) t.hold(false);
  await g.say("edo.shop.dress.12", "edo.shop.dress.13");
  await walkOf(g, "tami", [M.tami]);
  if (t) t.face("W");
}
const TAMI = tamiTree({ lullaby, dress });
after(TAMI, "slept", layDown);
// dressed: the act's stock replies now see them in O-Tami's clothes (edo-common.js stockFor; the tree sets edo.clothes first)
TAMI.nodes.dressedNow = { ...TAMI.nodes.dressedNow, then: (g) => { g.scene.stock = stockFor(g); return "root"; } };
for (const node of ["mom", "big", "lil"]) for (const o of TAMI.nodes[node].options) if (o.id.startsWith("red")) o.do = clueIn;

async function tamiTalk(g) {
  faceLead(g, "tami");
  await g.talk(TAMI);
  const t = g.actor("tami");
  if (t && !shop.meal) { if (t.hold) t.hold(false); }
}

// ---------- #22, step 1: the clerk's first pass (the first time they come in) ----------
async function clerkPass(g) {
  const cast = g.view.cast, t = g.actor("tami"), k = g.actor("kihei");
  // Kihei was out front: he comes in after them, and goes to his board
  const kiheiIn = !is(g, "edo.kiheiMet") && k;
  if (kiheiIn) { if (k.hold) k.hold(false); k.place(KIHEI_DOOR[0], KIHEI_DOOR[1] - 12, scaleAt(g.scene, KIHEI_DOOR[1] - 12)); k.fade(0); }
  // O-Tami, quick, to the three of them in the opening
  if (t) t.look(M.door[0], M.door[1]);
  await walkOf(g, "tami", [[300, 410], [316, 380]], true);
  await g.say("edo.shop.pass.1");
  await Promise.all([...THREE.map((id) => g.walkTo(HIDE[id][0], HIDE[id][1], id)),
    kiheiIn ? g.tween(300, (q) => k.fade(q)).then(() => walkOf(g, "kihei", [KIHEI_DOOR, KIHEI_OUT, [236, 398], M.kihei])).then(() => atWork(g)) : null]);
  for (const id of THREE) look(g, id, TAMI_OPEN);
  await g.say("edo.shop.pass.2", "edo.shop.pass.3");
  // she stands in the opening, and talks weather at the clerk, out in the street
  await walkOf(g, "tami", [TAMI_OPEN]);
  if (t) t.face("N");
  const c = cast.addFigure("tokuzo", "tokuzo", CLERK.from[0], CLERK.from[1], scaleAt(g.scene, CLERK.from[1])).face("W");
  c.fade(0);
  await cast.load();
  await Promise.all([g.tween(350, (q) => c.fade(q)), walkOf(g, "tokuzo", [CLERK.stop])]);
  c.face("S");
  if (c.hold) c.hold(true, "peerclose");
  if (t) t.look(CLERK.stop[0], CLERK.stop[1]);
  await g.say("edo.shop.pass.4", "edo.shop.pass.5", "edo.shop.pass.6", "edo.shop.pass.7");
  if (c.hold) c.hold(false);
  // his back goes past the opening
  await walkOf(g, "tokuzo", [CLERK.to]);
  await g.tween(300, (q) => c.fade(1 - q));
  cast.remove("tokuzo");
  g.flag("edo.clerkPassed", true);
  // the strangers on the beach at dawn; three travellers; and a baby who has not slept
  await walkOf(g, "tami", [[330, 396]]);
  for (const id of THREE) look(g, id, [330, 396]);
  if (t) t.look(IN.mom[0], IN.mom[1]);
  await g.say("edo.shop.pass.8", "edo.shop.pass.9", "edo.shop.pass.10", "edo.shop.pass.11", "edo.shop.pass.12");
  await walkOf(g, "tami", [[300, 430], M.tami]);
  if (t) t.face("W");
}

// ---------- the looks and uses that change with the story ----------
/** The baby: on O-Tami's back (awake: three days, not a wink) and, once she sleeps, in her basket on the mats. Mom's use
    is Mom asking for her (the same lullaby as the talk's). */
const babyLook = Object.assign((g) => g.say(`edo.shop.${is(g, "edo.babySleeps") ? "baby2" : "baby"}.${who(g)}`),
  { lines: THREE.flatMap((w) => [`edo.shop.baby.${w}`, `edo.shop.baby2.${w}`]) });
const babyUse = Object.assign(async (g) => {
  const me = who(g);
  if (is(g, "edo.babySleeps")) return g.say(`edo.shop.baby2.use.${me}`);
  if (me !== "mom") { faceLead(g, "tami"); return g.say(`edo.shop.baby.use.${me}`); }
  faceLead(g, "tami");
  await g.say("edo.shop.baby.use.mom");
  await lullaby(g);
  g.flag("edo.babySleeps", true);
  g.flag("edo.tamiMet", true);
  await g.say("edo.shop.baby.4", "edo.shop.baby.5", "edo.shop.baby.6");
  await layDown(g);
}, { lines: THREE.flatMap((w) => [`edo.shop.baby.use.${w}`, `edo.shop.baby2.use.${w}`]).concat(["edo.shop.baby.4", "edo.shop.baby.5", "edo.shop.baby.6"]) });

/** The print of Fuji in the new blue: a look, and (the first time) Kihei's word on it and Big Sister's clue (#21). */
const printLook = Object.assign(async (g) => {
  await g.say(`edo.shop.print.${who(g)}`);
  if (is(g, "edo.clue.blue")) return;
  const k = g.actor("kihei");
  if (k) { if (k.hold) k.hold(false); faceLead(g, "kihei"); }
  await g.say("edo.shop.print.kihei");
  atWork(g);
  look(g, "bigsis", [411, 228]);
  await g.say("edo.shop.print.clue", "edo.shop.print.clue.2");
  g.flag("edo.clue.blue", true);
  await clueIn(g);
}, { lines: [...THREE.map((w) => `edo.shop.print.${w}`), "edo.shop.print.kihei", "edo.shop.print.clue", "edo.shop.print.clue.2"] });
/** The money box: a look, and (the first time) Big Sister's museum case (#21: the coins). */
const moneyLook = Object.assign(async (g) => {
  await g.say(`edo.shop.money.${who(g)}`);
  if (is(g, "edo.clue.coins")) return;
  look(g, "bigsis", [452, 338]);
  await g.say("edo.shop.money.clue");
  g.flag("edo.clue.coins", true);
  await clueIn(g);
}, { lines: [...THREE.map((w) => `edo.shop.money.${w}`), "edo.shop.money.clue", "edo.shop.money.clue.2"] });
const godshelfLook = Object.assign((g) => g.say(...{ mom: ["edo.shop.godshelf.mom"], bigsis: ["edo.shop.godshelf.bigsis", "edo.shop.godshelf.bigsis.2"], lilsis: ["edo.shop.godshelf.lilsis"] }[who(g)]),
  { lines: ["edo.shop.godshelf.mom", "edo.shop.godshelf.bigsis", "edo.shop.godshelf.bigsis.2", "edo.shop.godshelf.lilsis"] });
/** The step: Little Sister sits on it (she really sits on it), and gets up again. */
const stepUse = Object.assign(async (g) => {
  const me = who(g);
  if (me !== "lilsis" || shop.meal) return g.say(`edo.shop.step.use.${me}`);
  await sitOnStep(g, "lilsis", SEAT.lilsis);
  await g.say("edo.shop.step.use.lilsis");
  await standFromStep(g, "lilsis");
}, { lines: THREE.map((w) => `edo.shop.step.use.${w}`) });
/** The gap under the floor: Little Sister's head in it (before the cat has made it hers). */
const underUse = Object.assign(async (g) => {
  const me = who(g), l = g.lead;
  if (me !== "lilsis" || !l || !l.hold) return g.say(`edo.shop.under.use.${me}`);
  l.face("E");
  l.hold(true, "crawl");
  const [x, y] = [l.x, l.y];
  await g.tween(420, (k) => l.place(x + 8 * k, y - 2 * k));
  await g.wait(700);
  await g.tween(420, (k) => l.place(x + 8 * (1 - k), y - 2 * (1 - k)));
  l.hold(false);
  await g.say("edo.shop.under.use.lilsis");
}, { lines: THREE.map((w) => `edo.shop.under.use.${w}`) });
/** Out into Yui, through the open front. */
const goOut = Object.assign(async (g) => {
  g.sfx("noren");
  await g.goto("edo-village", { spawn: "shop" });
}, { lines: [] });

// ---------- now and then: a gull out over the bay ----------
function tick(g, dt) {
  if (g.busy || g.dialogue.active) return;
  shop.gullAt -= dt;
  if (shop.gullAt > 0) return;
  shop.gullAt = 20000 + Math.random() * 20000;
  g.sfx("gull");
}

// The sea in the opening (behind the posts and the noren), rows of waves going in to the beach: ENGINE-20's `waves`.
const SEA = [[122, 216], [600, 216], [600, 286], [122, 286]];
const POSTS = [[[260, 210], [278, 210], [278, 290], [260, 290]], [[405, 210], [423, 210], [423, 290], [405, 290]], [[544, 210], [562, 210], [562, 290], [544, 290]]];

export default {
  id: "edo-fishshop",
  era: "edo",
  name: "Kihei's shop",
  // DEPTH (layout.json view: the lens 2.20 m up, below the lintel; a grown-up 119 px at the street line, 160 at full)
  horizon: 200, full: 401,
  walk: { area: [[240.4, 355.5], [532.4, 348.6], [566.8, 373.7], [414.0, 377.9], [441.5, 435.2], [261.3, 444.9], [113.9, 449.6], [127.9, 433.3], [234.0, 429.7], [241.3, 411.9], [131.5, 415.4], [166.6, 377.1], [229.0, 375.4]] },
  // the long cutting board (the tubs, the stand and the hearth block their ground as cut-outs: `solid`)
  blocked: [[[93.3, 381.1], [151.2, 379.5], [118.6, 412.5], [49.7, 414.7]]],

  party: THREE,
  spawn: { default: M.door, ...M, mom: M.door, bigsis: [300, 372], lilsis: [358, 374] },
  arrive: { door: [[300, 372], [358, 374]] },
  facing: "S",
  exits: ["edo-village"],
  stock: STOCK,                                          // (setup sets it from the story: edo-common.js stockFor; and O-Tami's dress)
  talk: TALK,
  combine: COMBINE,                                      // SCENES-20A: Dad's pencil on the sticky note (game.js useItem)
  given: keepHers,
  tick,

  picture: art + "back.png",
  planes: [
    { id: "noren", src: art + "noren.png", plane: "back" },
    { id: "driedfish", src: art + "driedfish.png", plane: "back" },
    { id: "tub-1", src: art + "tub-1.png", base: 369.7, solid: [[138.9, 359.5], [183.6, 358.4], [173.9, 369.1], [126.0, 370.3]] },
    { id: "tub-2", src: art + "tub-2.png", base: 374.3, solid: [[188.2, 364.9], [228.1, 363.9], [222.0, 373.8], [179.7, 374.9]] },
    { id: "tub-3", src: art + "tub-3.png", base: 387.8, solid: [[110.7, 377.7], [150.8, 376.7], [140.1, 387.2], [97.6, 388.4]] },
    { id: "stand", src: art + "stand.png", base: 428.0, solid: [[154.8, 415.8], [229.0, 413.4], [222.2, 428.0], [142.8, 430.7]] },
    // the sushi box on its stand: empty (the lid leaning on it), filled and pressed, turned out and cut in six (the meal)
    { id: "sushibox", base: 428.1, states: { empty: art + "sushibox-empty.png", filled: art + "sushibox-filled.png", cut: art + "sushibox-cut.png" }, state: "empty" },
    // the cut pieces on the step, beside the three, while they eat (the board off the stand)
    { id: "food", src: art + "sushibox-cut.png", at: FOOD.at, foot: FOOD.foot, scale: FOOD.scale, base: FOOD.base, when: () => false },
    { id: "hearth", src: art + "hearth.png", base: 490.1, solid: [[-12.1, 455.1], [113.2, 450.4], [79.1, 490.1], [-67.2, 496.3]] },
    // the baby's basket on the mats (her bedding: the baby sleeps in it once Mom has put her to sleep)
    { id: "basket", src: art + "basket.png", base: 479.5 },
    // Kihei's cat: at her place (the tail going), asleep once the baby is, and the rest (walk, run, under) for #23
    catPlane("sit", M.cat, (g) => !is(g, "edo.catGone") && !is(g, "edo.babySleeps")),
    catPlane("sleep", M.cat, (g) => !is(g, "edo.catGone") && is(g, "edo.babySleeps")),
    catPlane("walk", M.cat, () => false), catPlane("run", M.cat, () => false), catPlane("under", M.under, () => false),
    { id: "front", src: art + "front.png", plane: "front" },
  ],
  fx: [
    { id: "steam", type: "smoke", at: [30.6, 365.3], base: 490.1, height: 120, width: [4, 26], lean: [-12, -120], rate: 2.5, color: "#f0ece4", opacity: 0.4 },
    { id: "noren-sway", type: "sway", plane: "noren", anchor: "top", amount: 3, period: 3.2 },
    { id: "fish-sway", type: "sway", plane: "driedfish", anchor: "top", amount: 1.5, period: 4.1 },
    { id: "hearth-fire", type: "flame", at: [96.1, 446.8], base: 491.1, size: 7, lull: 0.4, glow: 20, glowColor: "#ff9a40", glowOpacity: 0.18 },
    { id: "tub-flip", type: "ripples", at: [204.7, 338.4], radius: [1, 8], flat: 0.3, every: [6, 14], base: 374.3 },
    { id: "sea", type: "waves", area: SEA, holes: POSTS, size: 6, opacity: 0.28, toward: "S", plane: "back" },
  ],

  // The people of the shop: Kihei at his board (cutting); O-Tami at her place beside the stand, the baby on her back
  // until she sleeps (then in her basket).
  actors: [
    { id: "kihei", kind: "kihei", at: M.kihei, face: "W", life: { fidget: [8, 14], still: true } },
    { id: "tami", kind: "tami-baby", at: M.tami, face: "W", when: (g) => !is(g, "edo.babySleeps"), life: { fidget: [4, 8], still: true } },
    { id: "tami", kind: "tami", at: M.tami, face: "W", when: (g) => is(g, "edo.babySleeps"), life: { fidget: [6, 11], still: true } },
  ],

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "street", name: "the street", rect: [183, 182, 435, 106], walkTo: [330, 372], face: "N", ...lookUse("edo.shop", "street") },
    { id: "out", name: "Yui", verb: "Go out to", rect: [183, 288, 435, 64], walkTo: M.door, face: "N", look: each("edo.shop.street"), use: goOut },
    { id: "noren", name: "noren", rect: [270, 158, 147, 56], walkTo: M.noren, face: "N", ...lookUse("edo.shop", "noren") },
    { id: "driedfish", name: "dried fish", rect: [0, 200, 105, 63], walkTo: [246, 372], face: "W", ...lookUse("edo.shop", "driedfish") },
    { id: "hats", name: "sedge hats", rect: [73, 190, 44, 48], walkTo: [246, 372], face: "W", ...lookUse("edo.shop", "hats") },
    { id: "sandals", name: "straw sandals", rect: [137, 164, 86, 52], walkTo: [252, 364], face: "N", ...lookUse("edo.shop", "sandals") },
    { id: "godshelf", name: "god-shelf", rect: [619, 150, 68, 41], walkTo: M.godshelf, face: "E", look: godshelfLook, use: each("edo.shop.godshelf.use") },
    { id: "step", name: "raised floor", poly: [[427.6, 343.6], [601.7, 339.7], [800, 556.1], [592.4, 582.4], [592.4, 600], [427.6, 380.5]], walkTo: M.step, face: "E",
      look: each("edo.shop.step"), use: stepUse },
    { id: "chest", name: "clothes chest", rect: [553, 279, 110, 95], walkTo: M.chest, face: "E", ...lookUse("edo.shop", "chest") },
    { id: "money", name: "money box", rect: [410, 318, 86, 39], walkTo: M.money, face: "E", look: moneyLook, use: each("edo.shop.money.use") },
    { id: "print", name: "print of Fuji", rect: [400, 200, 22, 58], walkTo: M.print, face: "N", look: printLook, use: each("edo.shop.print.use") },
    { id: "cuttingboard", name: "cutting board", rect: [47, 313, 99, 36], walkTo: M.board, face: "W", ...lookUse("edo.shop", "cuttingboard") },
    { id: "tubs", name: "tubs of fish", poly: [[98, 346], [128, 328], [228, 330], [230, 376], [151, 390], [98, 390]], walkTo: M.tubs, face: "W", ...lookUse("edo.shop", "tubs") },
    { id: "sushibox", name: "sushi box", rect: [150, 352, 80, 44], walkTo: M.press, face: "W", ...lookUse("edo.shop", "sushibox") },
    { id: "hearth", name: "hearth", rect: [0, 339, 115, 159], walkTo: M.hearth, face: "W", ...lookUse("edo.shop", "hearth") },
    { id: "basket", name: "baby", rect: [521, 360, 113, 65], walkTo: M.baby, face: "E", look: babyLook, use: babyUse, when: (g) => is(g, "edo.babySleeps") },
    { id: "under", name: "gap under the floor", poly: [[424, 352], [448, 372], [448, 414], [424, 394]], walkTo: M.under, face: "E", look: each("edo.shop.under"), use: underUse,
      when: (g) => !is(g, "edo.catGone") },
    // the cat: at her place; once she has gone under the floor with a mackerel (#23), there (the gap is hers now)
    { id: "cat", name: "cat", rect: [312, 372, 34, 34], walkTo: [356, 410], face: "W", ...lookUse("edo.shop", "cat"), when: (g) => !is(g, "edo.catGone") },
    { id: "catunder", name: "cat", poly: [[424, 352], [448, 372], [448, 414], [424, 394]], walkTo: M.under, face: "E", look: each("edo.shop.cat2"), when: (g) => is(g, "edo.catGone") },
    // the people of the shop (the game draws them; their areas go with them)
    { id: "kihei", name: "Kihei", verb: "Talk to", rect: [150, 256, 36, 138], walkTo: [252, 400], face: "W", look: each("edo.shop.kihei"), use: kiheiTalk,
      useWith: { ...giveNo("kihei"), pennies: kiheiPennies, penny: kiheiPennies, egg: kiheiEgg } },
    { id: "tami", name: "O-Tami", verb: "Talk to", rect: [198, 282, 34, 158], walkTo: [262, 438], face: "W", look: each("edo.shop.tami"), use: tamiTalk, useWith: giveNo("tami") },
    { id: "baby", name: "baby", rect: [200, 296, 30, 34], walkTo: [262, 438], face: "W", look: babyLook, use: babyUse, when: (g) => !is(g, "edo.babySleeps") },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and whenever the scene is built.
  setup(g) {
    this.stock = stockFor(g);                            // (the act's stock replies; their "see" lines once they are dressed)
    shop.meal = false; shop.gullAt = 12000;
    undoMoment(g);
    dressFor(g, "indoors");
    g.loop("waves", { level: 0.5 });                     // (the sea, through the open front)
    for (const p of ["cat", "cat-sleep", "cat-walk", "cat-run"]) { const c = g.plane(p); if (c) c.flag("mirror", true); }      // (she faces into the shop, W)
    atWork(g);
  },

  // The first time they come in: the clerk goes past, and O-Tami has them in behind the noren (#22, step 1).
  async enter(g) {
    this.stock = stockFor(g);
    if (!is(g, "edo.clerkPassed")) await clerkPass(g);
  },
};

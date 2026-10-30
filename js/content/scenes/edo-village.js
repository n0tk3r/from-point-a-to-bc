// Act Six, the first leg: Yui, on Suruga Bay, in the morning (SCENES-20A: new in round twenty, in place of ENGINE-20's
// sketch; the design, briefs/out/edo-design.md, sections 5 and 7; every line is WRITE-20A's, js/content/lines/edo-a.en.js,
// and the talks are js/content/talk/edo-a.js). The beach and the village street along the Tokaido, under the Satta pass;
// across the bay, Fuji, white and enormous. Boats on their props, nets drying on racks, the notice-board place, a hen yard
// behind a low fence, Kihei's fish shop with its noren lifting in the wind (the way into edo-fishshop), Gonroku's freighter
// at anchor far out, a cherry by the shrine path dropping the last of its petals.
//
// Mom, Big Sister and Little Sister are here together (`party`). What happens here:
//   the arrival      "Meanwhile, in another time" (js/content/cutscenes/edo-arrive.js): played by Going Down's hand-on, or by
//                    this scene's `enter` for a game that has not had it; the three step out of a door on the beach (the
//                    mark `arrive`), and the village woman drops her basket
//   #22 Out Of Sight the board (Sankichi reads the Kirishitan board aloud, under its close-up, because somebody asked; the
//                    one answer: "Then we pray quietly here." "That's MEAN." "It is."); Kihei out in front of his shop in
//                    the morning, until they go in; the clerk, Tokuzo, on his rounds once he has gone past the shop (the
//                    first pass is the shop's: edo-fishshop.js); before the kimonos O-Tami comes out and puts a hand on
//                    Mom's sleeve ("Not like that, dear. Not in that."), or Little Sister's boots are the trouble; dressed,
//                    he peers, asks, is told nothing but the truth, writes "travellers, three, going west", and goes home
//   #24 West         Little Sister at the hen yard (every hen facing west: edo.hensWest); Gonroku by his boat (no women
//                    aboard); O-Masa at the nets, asked properly (her hook takes her down the beach to him: edo.west); then,
//                    with the year worked out (#21), the goodbyes, and the voyage (js/content/cutscenes/edo-sail.js)
//   and a look and a use for each of the three at every thing, and the people's own words.
//
// Every place is the painter's own measurement of the finished picture (art/scenes/edo-village/layout.json, PAINT-20A's
// ready.md), or was set by eye against the picture with the people in it; where the two differ the comment says why.
//
// Try it: index.html?scene=edo-village&lead=mom&flags=edo.arrived   (the arrival first, without edo.arrived)

import { stockFor, STOCK } from "./edo-common.js";
import { tokuzoTree, sankichiTree, gonrokuTree, masaTree } from "../talk/edo-a.js";
import { THREE, who, is, heard, each, lookUse, dressFor, walkOf, look, TALK, giveNo, COMBINE, undoMoment, keepHers } from "./edo-yui.js";
import { scaleAt } from "../../engine/walk.js";

const art = "art/scenes/edo-village/";

// ---------- the marks (layout.json marks and stands) ----------
const M = {
  arrive: [150, 520], board: [505, 415], sankichi: [520, 411], hens: [487, 530], shop: [595, 480], boat: [92, 484], underboat: [83, 457],
  racks: [182, 447], gonroku: [278, 397], cherry: [640, 375], clerkFrom: [664, 374], clerkTo: [89, 571], east: [71, 577], west: [666, 373],
  well: [585, 388], masa: [158, 442], kiheiOut: [723, 491], tokuzoTalk: [487, 443], netmender: [262, 452], basketwoman: [392, 444],
};
const ARRIVE = { mom: [150, 520], bigsis: [196, 538], lilsis: [112, 548] };        // stands arrive_<who>
const DOOR = { at: [150, 462], r: 62 };                                              // layout.json door: the door in time they come out of
const NOREN_IN = [640, 468];                                                         // in at the shop's open front, behind the noren (base 468)
const FROM_SHOP = [[548, 494], [645, 494]];                                          // the other two, out of the shop (the lead on `shop`)
// Where the goodbyes are said: the street before the shop (Kihei and O-Tami out of it, Sankichi from the board).
const BYE = { mom: [606, 488], bigsis: [566, 494], lilsis: [532, 500], kihei: [700, 490], tami: [662, 487], sankichi: [520, 470] };
// O-Masa, down the beach beside her husband (#24): within earshot of the family, who stay where they are (she said so).
const MASA_BY_GONROKU = [300, 402];

/** What the scene is doing that is not saved (made again whenever it is built). The arrival sets `arriving` while it plays
    (js/content/cutscenes/edo-arrive.js): the three are kept out of sight until they step out of the door; `ownCard` when the
    village plays it itself (its "Meanwhile" card is then the cut-scene's); `basketGone`: the village woman has dropped her
    basket and gone up the street (until the scene is built again: she has come back for it). */
export const village = { arriving: false, ownCard: false, basketGone: false, kiheiIn: false, tokuzoHome: false, masaDown: false, gullAt: 0 };

/** The arrival's places, for js/content/cutscenes/edo-arrive.js. */
export const ARRIVAL = { door: DOOR, arrive: ARRIVE, east: M.east, basketwoman: M.basketwoman, clerkTo: M.clerkTo, from: [36, 590], drop: [356, 470], west: M.west };

// ---------- the board's close-up (#22): a notice board under its little roof, dense with brush writing ----------
/** The Kirishitan board, drawn large (800 x 600): two posts and a little gabled roof, a board of pale wood, a heading of four
    bigger marks, and dense columns of writing (strokes, never real characters: nobody here reads them but Sankichi), a seal. */
function boardDrawing() {
  let seed = 7;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  const ink = "#24305c", wood = "#ead9b0", grain = "#d8c290", post = "#5a3a22", roof = "#2c3442";
  let s = `<rect x="150" y="40" width="500" height="560" fill="#20283c" opacity="0.35"/>`;
  s += `<rect x="232" y="120" width="22" height="480" fill="${post}"/><rect x="546" y="120" width="22" height="480" fill="${post}"/>`;
  s += `<polygon points="170,128 400,52 630,128 610,146 400,78 190,146" fill="${roof}"/><rect x="180" y="140" width="440" height="10" fill="#3c4658"/>`;
  s += `<rect x="214" y="160" width="372" height="380" fill="${wood}" stroke="${post}" stroke-width="6"/>`;
  for (let i = 0; i < 9; i++) s += `<rect x="222" y="${178 + i * 40}" width="356" height="2" fill="${grain}"/>`;
  // the heading, across the top, right to left: four bigger marks ("Ordinance", Sankichi says)
  for (let i = 0; i < 4; i++) {
    const x = 520 - i * 62;
    s += `<rect x="${x}" y="176" width="34" height="5" fill="${ink}"/><rect x="${x + 14}" y="172" width="5" height="34" fill="${ink}"/><rect x="${x + 4}" y="196" width="26" height="4" fill="${ink}"/>`;
  }
  // the writing: columns from right to left, top to bottom, each mark a few short strokes
  for (let col = 0; col < 13; col++) {
    const x = 552 - col * 25;
    let y = 226;
    while (y < 512) {
      if (rnd() < 0.06) { y += 18; continue; }                                       // a gap: the end of a sentence
      const w = 10 + Math.round(rnd() * 6), h = 9 + Math.round(rnd() * 5);
      s += `<rect x="${x - w / 2}" y="${y}" width="${w}" height="2.4" fill="${ink}"/>`;
      s += `<rect x="${x - 1.5 + Math.round((rnd() - 0.5) * 6)}" y="${y - 2}" width="2.4" height="${h}" fill="${ink}"/>`;
      if (rnd() < 0.7) s += `<rect x="${x - w / 2 + 2}" y="${y + h - 3}" width="${w - 4}" height="2.2" fill="${ink}"/>`;
      if (rnd() < 0.4) s += `<rect x="${x + 3}" y="${y + 3}" width="2.2" height="${h - 5}" fill="${ink}"/>`;
      y += h + 6;
    }
  }
  s += `<rect x="236" y="494" width="26" height="26" fill="#b8402e"/><rect x="241" y="499" width="16" height="16" fill="none" stroke="#f0c8b0" stroke-width="2"/>`;
  return s;
}

// ---------- people ----------
const actor = (g, id) => g.actor(id);
/** Turn the people of a talk to the one being played. */
function faceLead(g, id) { const a = g.actor(id), l = g.lead; if (a && l) a.look(l.x, l.y); }
/** A villager's few words, one more each time (WRITE-20A: { 1: say.1, 2: say.2, more: say.3 }). */
const nth = (id) => Object.assign(async (g) => {
  faceLead(g, id);
  const n = [1, 2].find((k) => !heard(g, `edo.village.${id}.say.${k}`));
  await g.say(`edo.village.${id}.say.${n || 3}`);
}, { lines: [1, 2, 3].map((k) => `edo.village.${id}.say.${k}`) });

// ---------- #22: the board, and Sankichi ----------
const SANKICHI = sankichiTree({
  boardOpen: async (g) => {
    const s = g.actor("sankichi");
    if (s) { s.face("N"); if (s.hold) s.hold(true, "read"); }
    g.closeup(boardDrawing(), "The notice board: columns of writing under a little roof", { grid: [800, 600] });
    await g.wait(700);
  },
  boardClose: async (g) => {
    g.closeup();
    const s = g.actor("sankichi");
    if (s && s.hold) s.hold(false);
    faceLead(g, "sankichi");
    await g.wait(300);
  },
});
async function sankichiTalk(g) {
  faceLead(g, "sankichi");
  await g.talk(SANKICHI);
  const s = g.actor("sankichi");
  if (s && s.hold) s.hold(false);
}
/** The car key shown to Sankichi: a cart that goes without a horse. The coin: whose face is that. */
async function sankichiKey(g) {
  faceLead(g, "sankichi");
  const s = g.actor("sankichi");
  if (s && s.hold) s.hold(true, "stare");
  await g.say("edo.sankichi.key.1", "edo.sankichi.key.2", "edo.sankichi.key.3", "edo.sankichi.key.4");
  if (s && s.hold) s.hold(false);
  await g.say("edo.sankichi.key.5");
}
async function sankichiCoin(g) {
  faceLead(g, "sankichi");
  await g.say("edo.sankichi.coin.1", "edo.sankichi.coin.2");
}
const boardLook = (g) => g.say(...(is(g, "edo.boardRead")
  ? { mom: ["edo.village.board2.mom"], bigsis: ["edo.village.board2.bigsis", "edo.village.board2.bigsis.2"], lilsis: ["edo.village.board2.lilsis"] }
  : { mom: ["edo.village.board.mom"], bigsis: ["edo.village.board.bigsis", "edo.village.board.bigsis.2"], lilsis: ["edo.village.board.lilsis"] })[who(g)]);
boardLook.lines = ["edo.village.board2.mom", "edo.village.board2.bigsis", "edo.village.board2.bigsis.2", "edo.village.board2.lilsis", "edo.village.board.mom", "edo.village.board.bigsis", "edo.village.board.bigsis.2", "edo.village.board.lilsis"];
const boardUse = (g) => g.say(`edo.village.${is(g, "edo.boardRead") ? "board2" : "board"}.use.${who(g)}`);
boardUse.lines = THREE.flatMap((w) => [`edo.village.board.use.${w}`, `edo.village.board2.use.${w}`]);

// ---------- Kihei out in front of his shop, in the morning (until they have been in: edo.clerkPassed) ----------
async function kiheiOut(g) {
  faceLead(g, "kihei");
  await g.say("edo.kihei.open");                                                   // "...Sit." (his tree's first word, said out here)
  g.flag("edo.kiheiMet", true);
  const k = g.actor("kihei");
  village.kiheiIn = true;
  if (k) {
    await walkOf(g, "kihei", [NOREN_IN]);
    await g.tween(300, (t) => k.fade(1 - t));
    k.hidden = true;
  }
  g.sfx("noren");
  g.rebuildSpots();
}

// ---------- #22's end: the clerk ----------
/** O-Tami out of her shop to the one being played, a hand on her sleeve (before the kimonos: tokuzoTree's `notyet`), and back. */
async function tamiOut(g) {
  const l = g.lead, t = g.view.cast.addFigure("tami", is(g, "edo.babySleeps") ? "tami" : "tami-baby", NOREN_IN[0], NOREN_IN[1], scaleAt(g.scene, NOREN_IN[1])).face("W");
  t.fade(0);
  await g.view.cast.load();
  const to = l ? [l.x + 26, l.y + 3] : [500, 460];
  await Promise.all([g.tween(300, (k) => t.fade(k)), walkOf(g, "tami", [to], true)]);
  if (l) t.look(l.x, l.y);
  if (t.hold) t.hold(true, "pull");
  return t;
}
async function tamiIn(g, t) {
  if (!t) return;
  if (t.hold) t.hold(false);
  await walkOf(g, "tami", [NOREN_IN]);
  await g.tween(300, (k) => t.fade(1 - k));
  g.view.cast.remove("tami");
}
const TOKUZO = tokuzoTree({
  home: async (g) => {
    const t = g.actor("tokuzo");
    if (!t) return;
    if (t.hold) t.hold(false);
    if (t.fidget) await t.fidget("ojigi");
    village.tokuzoHome = true;                                                     // off along the street, east, and home, pleased
    await walkOf(g, "tokuzo", [[430, 470], M.clerkTo, [40, 600]]);
    t.hidden = true;
    g.rebuildSpots();
  },
});
async function tokuzoTalk(g) {
  faceLead(g, "tokuzo");
  const t = g.actor("tokuzo");
  if (!is(g, "edo.clothes") && who(g) !== "lilsis") {                               // not like that, dear: not in that
    const tami = await tamiOut(g);
    await g.talk(TOKUZO);
    await tamiIn(g, tami);
    return;
  }
  if (is(g, "edo.clothes") && !is(g, "edo.dressed") && t && t.hold) t.hold(true, "peerclose");
  await g.talk(TOKUZO);
  if (t && t.hold && !t.hidden) t.hold(false);
}

// ---------- #24: Gonroku, O-Masa, the hens ----------
const GONROKU = gonrokuTree({});
async function gonrokuTalk(g) {
  faceLead(g, "gonroku");
  const after = is(g, "edo.west");
  await g.talk(GONROKU);
  if (after) await depart(g);                                                      // the terms again; then the goodbyes, and the ship
}
const MASA = masaTree({
  toGonroku: async (g) => {
    const m = g.actor("masa");
    village.masaDown = true;
    if (m) {
      if (m.fidget) m.fidget("march");
      await walkOf(g, "masa", [[230, 430], MASA_BY_GONROKU]);
      look(g, "masa", "gonroku");
      if (m.fidget) m.fidget("point", { hold: true });
    }
    look(g, "gonroku", "masa");
    for (const id of THREE) look(g, id, MASA_BY_GONROKU);
    await g.wait(900);                                                             // (what she says to him the player hears only the end of)
    if (m && m.fidget) m.fidget(null);
  },
});
async function masaTalk(g) {
  faceLead(g, "masa");
  await g.talk(MASA);
}
/** The hens: Little Sister at the fence sees them all face west (edo.hensWest); the other two have their own words. */
async function hensUse(g) {
  const me = who(g);
  if (me !== "lilsis") return g.say(`edo.village.hens.use.${me}`);
  if (is(g, "edo.hensWest")) return g.say("edo.west.hens.again");
  const l = g.lead;
  if (l) l.face("E");
  await g.say("edo.village.hens.use.lilsis");
  const hens = [1, 2, 3, 4, 5].map((n) => g.effects.get(`hen-${n}`)).filter(Boolean);
  for (const h of hens) if (h.pose) h.pose("look", 1.4);                            // every one of them, looking the same way
  await g.say("edo.west.hens.1", "edo.west.hens.2");
  look(g, "bigsis", "lilsis");
  await g.say("edo.west.hens.3");
  look(g, "mom", [720, 540]);
  await g.say("edo.west.hens.4");
  g.flag("edo.hensWest", true);
}
hensUse.lines = ["edo.village.hens.use.mom", "edo.village.hens.use.bigsis", "edo.village.hens.use.lilsis", "edo.west.hens.again", "edo.west.hens.1", "edo.west.hens.2", "edo.west.hens.3", "edo.west.hens.4"];

// ---------- the goodbyes, and the voyage (#24's end: the first leg's gate) ----------
/** With the passage agreed (edo.west) and the year worked out (#21: Big Sister will not sail out of a year she has not named),
    the goodbyes, here in the street before the shop: Kihei and O-Tami out of it, Sankichi from the board; Little Sister to the
    shop (the baby, the cat) and to the hen yard, every hen by a name she gives it there and then. Then the ship. */
async function depart(g) {
  if (!is(g, "edo.west") || is(g, "edo.sailed")) return;
  if (!is(g, "edo.when")) { await g.say("edo.sail.notyet.bigsis"); return; }        // SCENES-20A: a line of my block (edo-a.en.js)
  await goodbyes(g);
  await g.cutscene("edo-sail");
}
async function goodbyes(g) {
  const cast = g.view.cast;
  const k = actor(g, "kihei") || cast.addFigure("kihei", "kihei", NOREN_IN[0], NOREN_IN[1], scaleAt(g.scene, NOREN_IN[1])).face("E");
  const t = actor(g, "tami") || cast.addFigure("tami", "tami-baby", NOREN_IN[0] + 8, NOREN_IN[1], scaleAt(g.scene, NOREN_IN[1])).face("E");      // (the baby asleep on her back: she has brought her out)
  for (const f of [k, t]) { f.hidden = false; f.fade(0); }
  await cast.load();
  g.sfx("noren");
  await Promise.all([
    ...THREE.map((id) => g.walkTo(BYE[id][0], BYE[id][1], id)),
    g.tween(300, (x) => k.fade(x)).then(() => walkOf(g, "kihei", [BYE.kihei])),
    g.wait(250).then(() => g.tween(300, (x) => t.fade(x))).then(() => walkOf(g, "tami", [BYE.tami])),
    walkOf(g, "sankichi", [BYE.sankichi]),
  ]);
  for (const id of THREE) look(g, id, BYE.tami);
  look(g, "kihei", "mom"); look(g, "tami", "mom"); look(g, "sankichi", "lilsis");
  await g.say("edo.west.bye.1", "edo.west.bye.2");
  await g.say("edo.west.bye.3");
  await g.say("edo.west.bye.4");
  // Little Sister to the shop (the baby, the cat), and to the hen yard
  look(g, "lilsis", [650, 400]);
  await g.say("edo.west.bye.5");
  await g.walkTo(M.hens[0], M.hens[1], "lilsis");
  look(g, "lilsis", [720, 540]);
  await g.say("edo.west.bye.6");
  look(g, "bigsis", "lilsis");
  await g.say("edo.west.bye.7", "edo.west.bye.8");
  // Sankichi: and the word, if she has not got it from him yet
  look(g, "lilsis", "sankichi");
  if (!is(g, "edo.arigato")) {
    await g.say("edo.sankichi.opt.thanks.lil", "edo.sankichi.thanks.1", "edo.sankichi.thanks.2", "edo.sankichi.thanks.3");
    g.flag("edo.arigato", true);
  }
  await g.say("edo.west.bye.9", "edo.west.bye.10");
  await g.wait(500);
}

// ---------- the looks and uses that change with the story ----------
const shipUse = Object.assign(async (g) => {
  if (is(g, "edo.west")) return depart(g);
  await g.say(`edo.village.ship.use.${who(g)}`);
}, { lines: THREE.map((w) => `edo.village.ship.use.${w}`) });
/** Little Sister under the big boat (her use): down on hands and knees into the gap, a moment, and out again. */
const underUse = Object.assign(async (g) => {
  const me = who(g), l = g.lead;
  if (me !== "lilsis" || !l || !l.hold) return g.say(`edo.village.underboat.use.${me}`);
  l.face("W");
  l.hold(true, "crawl");
  const [x, y] = [l.x, l.y];
  await g.tween(500, (k) => l.place(x - 16 * k, y - 3 * k));
  await g.wait(700);
  await g.tween(500, (k) => l.place(x - 16 * (1 - k), y - 3 * (1 - k)));
  l.hold(false);
  await g.say("edo.village.underboat.use.lilsis");
}, { lines: THREE.map((w) => `edo.village.underboat.use.${w}`) });
/** Into Kihei's shop, through the noren (each of the three has a word the first time she goes in). */
const shopUse = Object.assign(async (g) => {
  const line = `edo.village.shop.use.${who(g)}`;
  if (!heard(g, line)) await g.say(line);
  g.sfx("noren");
  await g.goto("edo-fishshop", { spawn: "door" });
}, { lines: THREE.map((w) => `edo.village.shop.use.${w}`) });

// ---------- now and then: a gull ----------
function tick(g, dt) {
  if (g.busy || g.dialogue.active) return;
  village.gullAt -= dt;
  if (village.gullAt > 0) return;
  village.gullAt = 14000 + Math.random() * 14000;
  g.sfx("gull");
}

// The fx of layout.json, and the waves (ENGINE-20's kind) on the near water, where PAINT-20A said it would go.
const BAY_NEAR = [[0, 303], [540, 303], [660, 322], [740, 318], [700, 332], [596, 340], [508, 352], [399, 367], [270, 385], [123, 406], [0, 428]];
const HEN = (n, look, perch, seed) => ({
  id: `hen-${n}`, type: "birds", perch, count: 1, depth: true, shy: 0, fly: false, turn: false, walk: 5, seed,
  moves: { stand: 3, look: 1.5, peck: 2.5, walk: 0.6, turn: 0 },
  frames: { foot: [25, 42], face: "E", sizeAt: 590, stand: [`hen-${look}-1.png`, `hen-${look}-2.png`, `hen-${look}-1.png`, `hen-${look}-3.png`], look: [`hen-${look}-4.png`],
    walk: [`hen-${look}-5.png`, `hen-${look}-6.png`], peck: [`hen-${look}-8.png`, `hen-${look}-7.png`, `hen-${look}-7.png`, `hen-${look}-8.png`, `hen-${look}-1.png`] },
});

export default {
  id: "edo-village",
  era: "edo",
  name: "Yui, on Suruga Bay",
  // DEPTH (layout.json: persp.Camera(300, 590), the eye 3.17 m up): one floor, the beach and the street (the street 30 cm up a
  // sand slope: painted, not a second floor)
  horizon: 300, full: 590,
  walk: { area: [[384, 373], [342, 379], [293, 386], [233, 395], [160, 406], [69, 419], [0, 419], [0, 596], [520, 596], [565, 584], [518, 503], [925, 503], [790, 503], [813, 498], [554, 469], [547, 466], [615, 433], [660, 410], [692, 394], [715, 382], [734, 373]] },
  // the big boat on its props, the tender, the two net racks, the board's platform, the well (layout.json blocked)
  blocked: [
    [[-26, 446], [-12, 454], [14, 460], [46, 467], [86, 473], [132, 478], [190, 481], [228, 471], [199, 462], [165, 455], [131, 450], [95, 445], [58, 442], [14, 440]],
    [[177, 398], [188, 400], [202, 402], [219, 404], [237, 405], [257, 406], [281, 407], [298, 404], [285, 402], [269, 400], [252, 398], [235, 397], [217, 396], [196, 395]],
    [[131, 438], [262, 425], [266, 421], [140, 433]], [[297, 421], [389, 412], [389, 409], [300, 418]], [[460, 419], [496, 409], [459, 406], [421, 415]], [[534, 387], [573, 387], [566, 384], [529, 384]],
  ],

  party: THREE,
  spawn: { default: M.arrive, ...M, kihei_out: M.kiheiOut, tokuzo_talk: M.tokuzoTalk, mom: ARRIVE.mom, bigsis: ARRIVE.bigsis, lilsis: ARRIVE.lilsis },      // (the painter's names too)
  arrive: { arrive: [ARRIVE.bigsis, ARRIVE.lilsis], shop: FROM_SHOP },
  facing: "S",
  exits: ["edo-fishshop"],
  stock: STOCK,                                          // (the act's own stock replies: setup sets them from the story, edo-common.js stockFor)
  talk: TALK,
  combine: COMBINE,                                      // SCENES-20A: Dad's pencil on the sticky note (game.js useItem: a thing on a thing in the pockets)
  given: keepHers,                                       // (Little Sister keeps her egg and her pennies: edo-yui.js)
  tick,

  picture: art + "back.png",
  planes: [
    { id: "ship", src: art + "ship.png", plane: "back" },
    { id: "racks", src: art + "racks.png", base: 436 },
    { id: "tender", src: art + "tender.png", base: 399 },
    { id: "board", src: art + "board.png", base: 413 },
    { id: "noren", src: art + "noren.png", base: 468 },
    { id: "boat", src: art + "boat.png", base: 451 },
    { id: "fence", src: art + "fence.png", base: 512 },
    { id: "front", src: art + "front.png", plane: "front" },
  ],
  fx: [
    { id: "bay-shimmer", type: "shimmer", poly: [[0, 303], [540, 303], [660, 322], [740, 318], [700, 332], [793, 312], [762, 317], [721, 322], [666, 330], [596, 340], [508, 352], [399, 367], [270, 385], [123, 406], [-37, 428], [0, 434]],
      count: 36, size: 5, flow: [3, 0], life: 1.8, color: "#f6eed8", opacity: 0.5, plane: "back" },
    { id: "waves", type: "waves", area: BAY_NEAR, holes: [[[146, 274], [190, 274], [190, 322], [146, 322]], [[176, 366], [298, 366], [298, 410], [176, 410]]], size: 8, opacity: 0.32, toward: "S", plane: "back" },
    { id: "shore-ripples", type: "ripples", at: [179, 399], radius: [2, 12], flat: 0.22, every: [1.6, 3.4], rings: 1, speed: 9, color: "#f6eed8", trough: "#2e3a93", opacity: 0.4, plane: "back" },
    { id: "ship-bob", type: "bob", plane: "ship", amount: 1, period: 6 },
    { id: "tender-bob", type: "bob", plane: "tender", amount: 1, period: 5, tilt: 1.0 },
    { id: "noren-sway", type: "sway", plane: "noren", anchor: "top", amount: 2.5, period: 3.2, wave: 30, lean: 0.35 },
    { id: "kitchen-smoke", type: "smoke", plane: "back", at: [574, 322], height: 58, width: [2, 11], lean: [16, -58], rise: 9, rate: 2.5, gust: 0.3, color: "#e4e6ea", opacity: 0.3 },
    { id: "gulls", type: "birds", plane: "back", lanes: [[[-12, 262], [160, 236], [340, 250], [520, 228], [640, -12]], [[-12, 206], [120, 222], [300, 200], [470, 212], [560, 300]], [[600, 240], [420, 262], [220, 248], [-12, 270]]],
      every: [7, 15], group: [1, 3], speed: 60, size: 8, scale: [0.6, 1.1], color: "#f6eed8" },
    { id: "petals", type: "petals", from: [[650, 218], [726, 218], [736, 290], [660, 290]], floor: 372, count: 6, size: 1.5, color: "#e6a5b8", plane: "back" },
    // the five hens, each a flock of one on her own perch inside the fence, all facing west along the coast (the frames face right)
    HEN(1, "brown", [[619, 562], [676, 562]], 1), HEN(2, "speckled", [[672, 543], [725, 543]], 2), HEN(3, "brown", [[726, 558], [783, 558]], 3),
    HEN(4, "speckled", [[745, 526], [795, 526]], 4), HEN(5, "brown", [[664, 518], [712, 518]], 5),
  ],

  // The people of Yui on the beach and the street (PEOPLE-20's kinds, at the painter's marks). Kihei is out in front of his
  // shop in the morning until they have been in (edo.clerkPassed); the clerk is on his rounds once he has gone past the shop.
  actors: [
    // (the net-mender sits cross-legged: his ground is the mat he sits on, so the way between the boat and the racks stays open)
    { id: "netmender", kind: "netmender", at: M.netmender, face: "W", solid: [[253, 447], [273, 447], [273, 457], [253, 457]], life: { fidget: [5, 10], still: true } },
    { id: "basketwoman", kind: "basketwoman", at: M.basketwoman, face: "E", life: { every: [24, 44], spots: [[356, 458, "E"], [430, 446, "W"]], stay: [4, 9] } },
    { id: "sankichi", kind: "sankichi", at: M.sankichi, face: "W", life: { fidget: [5, 10], every: [26, 46], spots: [[488, 432, "N"], [544, 426, "W"]], stay: [3, 7] } },
    { id: "gonroku", kind: "gonroku", at: M.gonroku, face: "W", life: { fidget: [6, 12], still: true } },
    { id: "masa", kind: "masa", at: M.masa, face: "N", life: { fidget: [6, 12], still: true } },
    { id: "kihei", kind: "kihei", at: M.kiheiOut, face: "W", when: (g) => !is(g, "edo.clerkPassed"), life: { fidget: [6, 12], still: true } },
    { id: "tokuzo", kind: "tokuzo", at: M.tokuzoTalk, face: "N", when: (g) => is(g, "edo.clerkPassed"), life: { fidget: [5, 9], still: true } },
  ],

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "gulls", name: "gulls", rect: [0, 180, 460, 110], walkTo: [300, 460], face: "N", ...lookUse("edo.village", "gulls") },
    { id: "fuji", name: "Mount Fuji", poly: [[300, 76], [612, 300], [-12, 300]], walkTo: [330, 470], face: "N", ...lookUse("edo.village", "fuji") },
    { id: "pass", name: "the pass", poly: [[520, 300], [600, 262], [680, 214], [750, 180], [800, 166], [800, 300]], walkTo: [660, 380], face: "N", ...lookUse("edo.village", "pass") },
    { id: "shrinepath", name: "shrine path", rect: [704, 206, 92, 94], walkTo: [640, 380], face: "N", ...lookUse("edo.village", "shrinepath") },
    { id: "cherry", name: "cherry tree", rect: [642, 214, 84, 76], walkTo: [640, 380], face: "N", ...lookUse("edo.village", "cherry") },
    { id: "bay", name: "the bay", poly: [[0, 302], [560, 302], [700, 330], [760, 320], [700, 345], [420, 365], [260, 388], [130, 410], [0, 442]], walkTo: [300, 460], face: "N", ...lookUse("edo.village", "bay") },
    { id: "ship", name: "Gonroku's ship", rect: [146, 274, 43, 49], walkTo: [300, 460], face: "N", look: each("edo.village.ship"), use: shipUse },
    { id: "smoke", name: "smoke", rect: [556, 262, 40, 54], walkTo: [585, 400], face: "N", ...lookUse("edo.village", "smoke") },
    { id: "roofs", name: "roofs", rect: [520, 318, 110, 58], walkTo: [585, 400], face: "N", ...lookUse("edo.village", "roofs") },
    { id: "well", name: "well", rect: [534, 315, 32, 70], walkTo: [585, 395], face: "W", ...lookUse("edo.village", "well") },
    { id: "road", name: "the road", poly: [[238, 571], [522, 451], [707, 373], [627, 373], [355, 451], [-61, 571]], walkTo: [330, 500], face: "NE", ...lookUse("edo.village", "road") },
    { id: "sand", name: "sand", poly: [[0, 460], [120, 440], [300, 420], [440, 400], [500, 430], [360, 470], [300, 500], [250, 540], [230, 596], [0, 596]], walkTo: [300, 500], face: "S", ...lookUse("edo.village", "sand") },
    // the ring on the sand where the door was (the mark `arrive`)
    { id: "arrive", name: "where the door was", poly: [[112, 494], [188, 494], [204, 510], [188, 528], [112, 528], [96, 510]], walkTo: [196, 532], face: "W", ...lookUse("edo.village", "arrive") },
    { id: "nets", name: "nets", rect: [140, 350, 245, 89], walkTo: [210, 452], face: "N", ...lookUse("edo.village", "nets") },
    { id: "boats", name: "boats", rect: [0, 375, 220, 101], walkTo: [150, 494], face: "W", ...lookUse("edo.village", "boats") },
    { id: "underboat", name: "gap under the boat", rect: [30, 446, 90, 26], walkTo: [92, 486], face: "W", look: each("edo.village.underboat"), use: underUse },
    { id: "board", name: "notice board", verb: "Read", plane: "board", rect: [420, 314, 71, 105], walkTo: [446, 431], face: "N", look: boardLook, use: boardUse },
    { id: "shop", name: "Kihei's shop", verb: "Go into", poly: [[578, 466], [800, 492], [800, 354], [578, 346]], walkTo: M.shop, face: "E", look: each("edo.village.shop"), use: shopUse },
    { id: "fence", name: "fence", rect: [549, 466, 251, 116], walkTo: M.hens, face: "E", ...lookUse("edo.village", "fence") },
    { id: "hens", name: "hens", rect: [552, 505, 238, 75], walkTo: M.hens, face: "E", look: each("edo.village.hens"), use: hensUse },
    // the people of Yui (the game draws them; their areas go with them)
    { id: "netmender", name: "net-mender", verb: "Talk to", rect: [248, 386, 30, 68], walkTo: [232, 464], face: "E", look: each("edo.village.netmender"), use: nth("netmender") },
    { id: "basketwoman", name: "village woman", verb: "Talk to", rect: [380, 372, 24, 74], walkTo: [356, 462], face: "E", look: each("edo.village.basketwoman"), use: nth("basketwoman"),
      when: () => !village.basketGone },
    { id: "sankichi", name: "Sankichi", verb: "Talk to", rect: [510, 362, 20, 51], walkTo: [512, 432], face: "N", look: each("edo.village.sankichi"), use: sankichiTalk,
      useWith: { ...giveNo("sankichi"), carkey: sankichiKey, coin: sankichiCoin } },
    { id: "tokuzo", name: "Tokuzō", verb: "Talk to", rect: [474, 366, 26, 79], walkTo: [470, 464], face: "N", look: each("edo.village.tokuzo"), use: tokuzoTalk,
      when: (g) => is(g, "edo.clerkPassed") && !village.tokuzoHome, useWith: giveNo("tokuzo") },
    { id: "gonroku", name: "Gonroku", verb: "Talk to", rect: [268, 346, 20, 53], walkTo: [286, 432], face: "N", look: each("edo.village.gonroku"), use: gonrokuTalk, useWith: giveNo("gonroku") },
    { id: "masa", name: "O-Masa", verb: "Talk to", rect: [146, 374, 26, 70], walkTo: [190, 456], face: "W", look: each("edo.village.masa"), use: masaTalk,
      when: () => !village.masaDown, useWith: giveNo("masa") },
    { id: "kihei", name: "Kihei", verb: "Talk to", rect: [706, 396, 34, 96], walkTo: [672, 492], face: "E", look: each("edo.village.kihei"), use: kiheiOut,
      when: (g) => !is(g, "edo.clerkPassed") && !village.kiheiIn, useWith: giveNo("kihei") },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and whenever the scene is built.
  setup(g) {
    this.stock = stockFor(g);                            // (the act's stock replies; their "see" lines once they are dressed)
    village.kiheiIn = false; village.tokuzoHome = false; village.masaDown = false; village.basketGone = false; village.gullAt = 9000;
    undoMoment(g);
    dressFor(g, "outdoors");
    g.loop("waves");
    if (village.arriving) for (const id of THREE) { const f = g.actor(id); if (f) f.fade(0); }      // (the arrival: not out of the door yet)
  },

  // The arrival plays here for a game that has not had it (a save at the hand-on, the address index.html?scene=edo-village),
  // as the Office's lot plays its own: the cut-scene comes back here, on the mark `arrive`, and sets edo.arrived.
  async enter(g) {
    this.stock = stockFor(g);
    if (village.arriving) return;
    if (!is(g, "edo.arrived")) { village.ownCard = true; await g.cutscene("edo-arrive"); return; }
  },
};


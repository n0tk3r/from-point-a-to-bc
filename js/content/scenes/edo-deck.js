// Act Six, the first stretch: the ship by day, Gonroku's coaster, the fifth day out, off Daiōzaki, noon (SCENES-21A: new in
// round twenty-one, in place of ENGINE-21's stub; the design, briefs/out/edo2-design.md, sections 5 and 7, #26 and #27; every
// line is WRITE-21A's, js/content/lines/edo-c.en.js, and the talks are js/content/talk/edo-c.js). The great sail of woven
// cotton filling on its yard, the mast in its iron rings, the mast step where the Funadama is sealed, the windlass with two
// sailors at its bars, the hold under its mats, the ship's boat lashed upside down, Kōta's hearth box and his rice pot,
// Gonroku at the long tiller, old Kanbei by the compass box; the sea in rows running past; Daiōzaki grey off the bow.
//
// Mom, Big Sister and Little Sister are here together (`party`); Casting Off (cutscenes/edo-castoff.js) brings them, on the
// mark `deck`, and nobody leaves the ship (no ways out; the map at sea refuses). What happens here, in either order:
//   #26 Etekō      (Big Sister) Kanbei cannot see his card in the glare: "Girl. You read?"; the compass box opens the
//                  close-up (edo-compass.js: the ship's clock runs backwards, edo.compassRead); the call: English (the crew
//                  stare), the rooster (west-and-a-bit), saru (the crew freezes: edo.saruSaid), the sea word from Kōta or
//                  Denzō (edo.seaWords), "Etekō." (edo.headingCalled)
//   #27 Don't Lift The Lid (Little Sister, Mom) Kōta met (edo.kotaMet: Little Sister's charades); Mom's lesson with the lid
//                  (edo.lidDown); what the lady in the mast was given (Denzō; the first knock on the mast step: edo.funadamaList,
//                  in Big Sister's note); a penny for his coin (edo.coinTraded: `mon`, `twopennies`); she chirps (edo.chirped)
//   both done      "The Uttermost Parts" (cutscenes/edo-sail.js): the night, Psalm 139, Osaka
// and a look and a use for each of the three at every thing.
//
// Every place is the painter's (art/scenes/edo-deck/layout.json, PAINT-21B's ready.md), but the sea's outline (the
// painter's 402 points, kept to 29 within two pixels: tools/simplify.py in SCENES-21A's folder) and the hold's.
//
// Try it: index.html?scene=edo-deck&lead=bigsis&flags=edo.arrived,edo.clothes,edo.dressed,edo.when,edo.west,edo.aboard

import { STOCK_DRESSED } from "./edo-common.js";
import { kanbeiTree, denzoTree, seijiroTree, kotaTree, gonrokuDeckTree } from "../talk/edo-c.js";
import { dressFor } from "./edo-yui.js";
import { THREE, who, is, heard, each, lookUse, walkOf, look, faceLead, once, nthOf, lookBy, uttermost, TALK_DECK } from "./edo-sea.js";

const art = "art/scenes/edo-deck/";

// ---------- the marks (layout.json marks and stands) ----------
const M = {
  deck: [400, 576], bow: [54, 551], mast: [285, 537], hearth: [219, 568], kota: [97, 553], windlass: [611, 514], kako1: [535, 506],
  kako2: [605, 471], denzo: [362, 535], seijiro: [465, 562], tiller: [753, 542], compass: [711, 554], kanbei: [612, 553], rail: [655, 475],
  deck_bigsis: [345, 582], deck_lilsis: [452, 584],
};
const MASTSTEP = [312, 500], BOX = [652, 470], POT = [169, 505], CAPE = [130, 252];
const LIL_ON_DECK = [516, 590];                    // (the painter's deck_lilsis is in front of the purser on his bale: a step to his right)
const AT_HEARTH = { mom: [196, 582], lilsis: [150, 584], bigsis: [258, 586] };       // Mom's lesson, beside the boy; Little Sister at the near corner; Big Sister a step back, out of their way

/** What the scene is doing that is not saved (made again whenever it is built). */
export const deck = { openAfter: false, gullAt: 0, peekAt: 0, peeking: 0, caskShown: false };

// ---------- the people ----------
/** The crew as they are when nobody needs them: the two at their windlass bars, the old man at his box. */
function atRest(g) {
  for (const id of ["kako1", "kako2"]) { const k = g.actor(id); if (k && k.hold) k.hold(true, "bar"); }
  const kb = g.actor("kanbei");
  if (kb) kb.face("E");
}

// #26: Kanbei, the ship's clock, the call
const KANBEI = kanbeiTree({
  // the card, looked at: the close-up opens when the talk is over (the working-out is the close-up's, at the needle)
  closeup: async () => { deck.openAfter = true; },
  // "Saru.": the whole crew freezes, Denzō's hand on the mast, the windlass men stock-still, a gull overhead
  freeze: async (g) => {
    const d = g.actor("denzo");
    if (d) { d.look(MASTSTEP[0], MASTSTEP[1]); if (d.hold) d.hold(true, "mast"); }
    for (const id of ["kako1", "kako2", "gonroku", "seijiro", "kota"]) look(g, id, "bigsis");
    g.sfx("gull");
    await g.wait(1200);
  },
  // the call: the tiller over a hair, the sail settling, the ship holding for the Kumano-nada
  hold: async (g) => {
    const k = g.actor("kanbei");
    if (k && k.hold) k.hold(true, "call");
    look(g, "gonroku", CAPE);
    g.sfx("creak");
    await g.wait(900);
    if (k && k.hold) k.hold(false);
    g.sfx("sail");
    await g.wait(500);
  },
});
async function kanbeiTalk(g) {
  faceLead(g, "kanbei");
  deck.openAfter = false;
  await g.talk(KANBEI);
  const d = g.actor("denzo");
  if (d && d.hold) d.hold(false);
  atRest(g);
  if (deck.openAfter) { deck.openAfter = false; return openClock(g); }
  await uttermost(g);
}
/** The compass box: its lid propped (the card's white shows), and the close-up of the ship's clock. */
async function openClock(g) {
  const box = g.plane("compass");
  if (box) box.set("open");
  g.sfx("click");
  await g.wait(350);
  await g.openCloseup("edo-compass");
}
const compassUse = Object.assign(async (g) => {
  await once(g, `edo.deck.compassbox.use.${who(g)}`);
  await openClock(g);
}, { lines: THREE.map((w) => `edo.deck.compassbox.use.${w}`) });

// #27: Denzō, the lady in the mast
const DENZO = denzoTree({
  // Big Sister writes the list on her sticky note in Dad's pencil
  write: async (g) => {
    const b = g.actor("bigsis");
    if (b) b.look(M.denzo[0], M.denzo[1]);
    g.sfx("paint");
    await g.wait(700);
  },
  chirp: (g) => chirp(g),
});
async function denzoTalk(g, tree = DENZO) {
  faceLead(g, "denzo");
  await g.talk(tree);
  const d = g.actor("denzo");
  if (d && d.hold) d.hold(false);
  await uttermost(g);
}
/** The first knock on the mast step, by anyone: Denzō, at once, with what she was given (the tree's own list node); a knock
    after it is the wrong try (open it: "Also, it's nailed."), and after that Denzō says the list again. */
const maststepUse = Object.assign(async (g) => {
  if (is(g, "edo.funadamaList") && !heard(g, "edo.deck.maststep.open.1")) { look(g, "bigsis", MASTSTEP); return g.say("edo.deck.maststep.open.1", "edo.deck.maststep.open.2"); }
  if (is(g, "edo.funadamaList")) { faceLead(g, "denzo"); return g.say("edo.denzo.list.again"); }        // (knocked on again: Denzō says it all over)
  await g.say(`edo.deck.maststep.use.${who(g)}`);
  g.sfx("knock");
  await denzoTalk(g, { ...DENZO, start: (q) => (is(q, "edo.funadamaList") ? DENZO.start(q) : "list") });
}, { lines: [...THREE.map((w) => `edo.deck.maststep.use.${w}`), "edo.deck.maststep.open.1", "edo.deck.maststep.open.2", "edo.denzo.list.again"] });

/** She chirps: Kōta laughs for the first time on the voyage, and from the foot of the mast two small bright notes. */
async function chirp(g) {
  const k = g.actor("kota");
  if (k && k.hold) k.hold(false);
  if (k && k.fidget) k.fidget("laughout");
  await g.wait(500);
  g.sfx("chirp");
  for (const id of [...THREE, "denzo", "gonroku", "kota", "seijiro", "kako1", "kako2"]) look(g, id, MASTSTEP);
  await g.wait(900);
}

// #27: Kōta, the lid, the coin
const KOTA = kotaTree({
  // after Mom's lesson: the lid stays on; the pot boils, starch running down under the lid; Kōta's hands hover. And Little
  // Sister, who has listened to every word, reaches for it herself (the wrong try: Mom, "What did I just say?").
  wait: async (g) => {
    const pot = g.plane("pot"), k = g.actor("kota");
    if (pot) pot.set("steam");
    // Big Sister, if she is standing where the lesson happens (she talked to him, or waited there), steps back out of it
    const b = g.actor("bigsis"), near = (p) => b && Math.hypot(b.x - p[0], b.y - p[1]) < 36;
    const aside = near(AT_HEARTH.mom) || near(AT_HEARTH.lilsis) ? g.walkTo(AT_HEARTH.bigsis[0], AT_HEARTH.bigsis[1], "bigsis") : null;
    await g.walkTo(AT_HEARTH.mom[0], AT_HEARTH.mom[1], "mom");
    if (aside) { await aside; look(g, "bigsis", POT); }
    look(g, "mom", POT);
    if (k) { k.look(POT[0], POT[1]); if (k.hold) k.hold(true, "wait"); }
    const l = g.actor("lilsis");
    if (l) {
      await g.walkTo(AT_HEARTH.lilsis[0], AT_HEARTH.lilsis[1], "lilsis");
      l.look(POT[0], POT[1]);
      await g.say("edo.deck.pot.lift.1");
      look(g, "mom", "lilsis");
      await g.say("edo.deck.pot.lift.2");
      look(g, "mom", POT);
    }
    g.sfx("hiss");
  },
  // off the fire and into bowls; the crew eat
  serve: async (g) => {
    const pot = g.plane("pot"), k = g.actor("kota");
    if (pot) pot.set("lid");
    if (k && k.hold) k.hold(false);
    if (k && k.fidget) await k.fidget("ojigi");
    for (const id of ["kako1", "kako2"]) { const a = g.actor(id); if (a && a.hold) a.hold(false); look(g, id, "kota"); }
    for (const id of ["denzo", "gonroku"]) look(g, id, "kota");
    await g.wait(900);
  },
  // Little Sister looks at her three pennies a long time
  look: async (g) => {
    const l = g.actor("lilsis");
    if (l) l.face("S");
    await g.wait(1600);
    if (l) l.look(M.kota[0], M.kota[1]);
  },
  // a penny for his coin: three pennies become two, and the one-mon coin, all Little Sister's
  trade: async (g) => {
    const l = g.actor("lilsis"), k = g.actor("kota");
    if (l && l.hold) l.hold(true, "coinout");
    if (k && k.hold) k.hold(true, "coin");
    await g.wait(700);
    g.take("pennies"); g.give("twopennies"); g.give("mon");
    g.sfx("pickup");
    if (k && k.hold) k.hold(false);
    if (l && l.hold) l.hold(true, "coin");                                            // (his coin up to her eye: the square hole)
    await g.wait(500);
  },
  chirp: (g) => chirp(g),
});
async function kotaTalk(g) {
  faceLead(g, "kota");
  await g.talk(KOTA);
  for (const id of THREE) { const f = g.actor(id); if (f && f.hold) f.hold(false); }
  atRest(g);
  await uttermost(g);
}

const GONROKU = gonrokuDeckTree({});
async function gonrokuTalk(g) { faceLead(g, "gonroku"); await g.talk(GONROKU); look(g, "gonroku", CAPE); }
const SEIJIRO = seijiroTree({});
async function seijiroTalk(g) { faceLead(g, "seijiro"); await g.talk(SEIJIRO); }

// ---------- the looks and uses that change with the story ----------
const maststepLook = lookBy("edo.deck.maststep", "after", (g) => is(g, "edo.funadamaList"));
const potLook = lookBy("edo.deck.pot", "after", (g) => is(g, "edo.lidDown"));
/** The floating cask: the first use, by any of the three, is the wrong try (Denzō: "That's for Konpira."). */
const caskUse = Object.assign(async (g) => {
  if (!heard(g, "edo.deck.cask.1")) { look(g, "denzo", "lilsis"); return g.say("edo.deck.cask.1", "edo.deck.cask.2", "edo.deck.cask.3"); }
  await g.say(`edo.deck.cask.use.${who(g)}`);
}, { lines: [...THREE.map((w) => `edo.deck.cask.use.${w}`), "edo.deck.cask.1", "edo.deck.cask.2", "edo.deck.cask.3"] });

// ---------- now and then: a gull; Kōta lifting his lid (until he has learned not to); the cask's area going with it ----------
function tick(g, dt) {
  followCask(g);
  if (g.busy || g.dialogue.active) return;
  deck.gullAt -= dt;
  if (deck.gullAt <= 0) { deck.gullAt = 14000 + Math.random() * 14000; g.sfx("gull"); }
  if (is(g, "edo.lidDown")) return;
  const pot = g.plane("pot");
  if (!pot) return;
  if (deck.peeking > 0) { deck.peeking -= dt; if (deck.peeking <= 0) pot.set("steam"); return; }
  deck.peekAt -= dt;
  if (deck.peekAt > 0) return;
  deck.peekAt = 7000 + Math.random() * 6000;
  deck.peeking = 1400;
  pot.set("lifted");                                                                      // (the painted lid propped up: his hands are off it)
  const k = g.actor("kota");
  if (k) k.look(POT[0], POT[1]);
}
/** The cask's area is where the floating cask is while it bobs past (the flyer `cask`), and is not there while it is not. */
function followCask(g) {
  const e = g.effects && g.effects.get ? g.effects.get("cask") : null, spots = g.view && g.view.spots;
  if (!spots) return;
  const i = spots.findIndex((h) => h.id === "cask");
  if (i < 0) return;
  const el = g.view.hotEl ? g.view.hotEl.querySelector(`.spot[data-i="${i}"]`) : null;
  let at = null;
  if (e && e.groups && !e.hidden) { try { const list = (e.groups(e.time / 1000, false) || [])[0]; if (list && list.length) at = list[0]; } catch { at = null; } }
  if (!at || at[0] < 4 || at[0] > 796) { deck.caskShown = false; if (el) el.style.display = "none"; return; }
  const r = [Math.round(at[0] - 26), Math.round(at[1] - 22), 52, 30];
  if (!spots[i].rect || spots[i].rect.some((v, k) => Math.abs(v - r[k]) > 1)) { spots[i].rect = r; spots[i].poly = undefined; if (g.view.reshape) g.view.reshape(i); }
  deck.caskShown = true;
  if (el) el.style.display = "";
}

const SEA = [[0, 263], [799, 263], [799, 319], [672, 319], [668, 397], [556, 404], [528, 404], [496, 360], [492, 356], [480, 353], [396, 355], [388, 360], [380, 373], [372, 404], [284, 406], [280, 378], [276, 366], [268, 358], [264, 327], [152, 327], [124, 335], [88, 359], [84, 363], [80, 384], [44, 387], [40, 383], [28, 393], [24, 424], [0, 357]];
const SAIL = [[2, 2], [452, 2], [560, 12], [660, 31], [738, 50], [741, 92], [737, 140], [726, 178], [713, 200], [640, 199], [560, 195], [470, 187], [380, 175], [290, 163], [200, 151], [110, 140], [20, 130], [2, 126]];

export default {
  id: "edo-deck",
  era: "edo",
  name: "On deck",
  music: "edo-sea",
  // DEPTH (layout.json: persp.Camera(262, 590), the eye 3.59 m over the deck): one floor, the near walkway bow to stern, the
  // mast's gangway, the bow's deck and the stern's
  horizon: 262, full: 590,
  walk: { area: [[2, 598], [798, 598], [798, 545], [739, 506], [687, 469], [505, 469], [541, 540], [372, 540], [376, 502], [264, 502], [242, 540], [77, 540], [115, 506], [82, 509], [53, 526], [25, 550], [11, 569]] },
  // the mast step, the hearth box, the bale, the windlass, the compass post, the tiller and rudder head, the coil, the bucket,
  // the water cask (layout.json blocked)
  blocked: [
    [[260, 532], [359, 532], [363, 507], [273, 507]], [[110, 563], [204, 563], [222, 535], [137, 535]], [[426, 558], [502, 558], [498, 546], [425, 546]],
    [[576, 508], [636, 508], [599, 469], [548, 469]], [[642, 547], [670, 547], [661, 537], [633, 537]], [[695, 538], [781, 525], [798, 525], [797, 514], [765, 514], [689, 532]],
    [[2, 598], [80, 598], [99, 582], [2, 582]], [[91, 598], [139, 598], [146, 592], [100, 592]], [[798, 598], [798, 598], [798, 585], [787, 585]],
    [[716, 598], [798, 598], [798, 576], [724, 584]],
  ],

  party: THREE,
  // (no mark of Mom's own on `deck` itself: standing there she is on `deck`, as LEG_START and the engine test read it; her own
  // place when nothing says where is `default`, the same point)
  spawn: { default: M.deck, ...M, bigsis: M.deck_bigsis, lilsis: M.deck_lilsis },
  arrive: { deck: [M.deck_bigsis, LIL_ON_DECK], compass: [[680, 584], [640, 588]] },
  facing: "N",
  exits: ["edo-compass"],
  stock: STOCK_DRESSED,
  talk: TALK_DECK,
  tick,

  picture: art + "back.png",
  planes: [
    { id: "swell", src: art + "swell.png", plane: "back" },
    { id: "sail", src: art + "sail.png", plane: "back" },
    { id: "rigging", src: art + "rigging.png", plane: "back" },
    { id: "mast", src: art + "mast.png", base: 525 },
    { id: "windlass", src: art + "windlass.png", base: 507 },
    { id: "tiller", src: art + "tiller.png", base: [[697, 534], [805, 524]] },
    // the compass box: shut; its lid propped open as the close-up opens (shut again whenever the deck is built)
    { id: "compass", base: 545, states: { shut: art + "compass-shut.png", open: art + "compass-open.png" }, state: "shut" },
    // Kōta's pot: boiling, lid on, starch run down under it, until the rice comes right (edo.lidDown); then the lid on, left alone
    { id: "pot", base: 560, states: { lid: art + "pot.png", lifted: art + "pot-lifted.png", steam: art + "pot-steam.png" }, state: (g) => (is(g, "edo.lidDown") ? "lid" : "steam") },
    { id: "front", src: art + "front.png", plane: "front" },
    { id: "near", src: art + "near.png", plane: "front" },
  ],
  fx: [
    // the sea's rows running past toward the stern (ENGINE-21's run), over the swell layer and under everything else
    { id: "sea-rows", type: "waves", run: true, area: SEA, toward: "E", speed: 46, rows: 10, per: 16, size: 13, life: 2.4, color: "#f6eed8", opacity: 0.6, plane: "back" },
    { id: "swell", type: "bob", plane: "swell", amount: 1, period: 9, tilt: 0.25 },
    { id: "sail-breath", type: "sway", plane: "sail", anchor: "belly", amount: 2.5, period: 4.6, lean: 0.35 },
    { id: "bow-spray", type: "spray", at: [40, 388], toward: [-50, -150], spread: 32, count: 16, every: [5, 11], life: 0.9, color: "#f6eed8", opacity: 0.75, base: 519 },
    { id: "cask", type: "birds", lanes: [[[-30, 352], [830, 352]]], every: [55, 95], group: [1, 1], speed: 40, both: false,
      frames: { glide: ["cask-1.png", "cask-2.png", "cask-3.png"], flap: ["cask-1.png", "cask-2.png", "cask-3.png"], foot: [20, 19] }, scale: 1, clip: [SEA], plane: "back" },
    { id: "gulls", type: "birds", plane: "back", lanes: [[[-12, 176], [120, 160], [260, 184], [420, 212], [600, 222], [812, 210]], [[812, 24], [770, 64], [730, 120], [600, 236], [300, 246], [-12, 214]]],
      every: [8, 16], group: [1, 2], speed: 64, size: 9, scale: [0.7, 1.1], color: "#f4f1e6", behind: [SAIL] },
    { id: "hearth-embers", type: "embers", at: [168, 518], size: [6, 2], glowOpacity: 0.16, base: 560 },
    { id: "hearth-smoke", type: "smoke", at: [153, 512], height: 46, width: [2, 10], lean: [26, -46], rise: 10, rate: 1.6, color: "#e4e6ea", opacity: 0.22, base: 560 },
    { id: "pot-steam", type: "smoke", at: [169, 505], height: 40, width: [3, 14], lean: [18, -40], rise: 14, rate: 3.0, color: "#f6eed8", opacity: 0.38, base: 560, when: (g) => !is(g, "edo.lidDown") },
  ],

  // The crew (PEOPLE-21A's kinds; Gonroku round twenty's), at the painter's marks
  actors: [
    { id: "gonroku", kind: "gonroku", at: M.tiller, face: "W", life: { fidget: [8, 14], still: true } },
    { id: "kanbei", kind: "kanbei", at: M.kanbei, face: "E", life: { fidget: [6, 11], still: true } },
    { id: "denzo", kind: "denzo", at: M.denzo, face: "W", life: { fidget: [6, 11], still: true } },
    { id: "seijiro", kind: "seijiro", at: M.seijiro, face: "S", life: { fidget: [7, 12], still: true } },
    { id: "kota", kind: "kota", at: M.kota, face: "E", life: { fidget: [6, 10], still: true } },
    { id: "kako1", kind: "kako1", at: M.kako1, face: "E", life: { fidget: [9, 15], still: true } },
    { id: "kako2", kind: "kako2", at: M.kako2, face: "W", life: { fidget: [9, 15], still: true } },
  ],

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "sea", name: "the sea", poly: SEA, walkTo: M.deck, face: "N", ...lookUse("edo.deck", "sea") },
    { id: "cape", name: "Daiōzaki", poly: [[2, 240], [120, 240], [240, 252], [268, 265], [2, 265]], walkTo: M.bow, face: "N", ...lookUse("edo.deck", "cape") },
    { id: "gulls", name: "gulls", rect: [2, 120, 330, 110], walkTo: M.deck, face: "N", ...lookUse("edo.deck", "gulls") },
    { id: "sail", name: "sail", poly: SAIL, walkTo: M.deck, face: "N", ...lookUse("edo.deck", "sail") },
    { id: "yard", name: "yard", poly: [[452, 2], [560, 3], [660, 22], [752, 38], [752, 56], [660, 40], [560, 21]], walkTo: M.windlass, face: "N", ...lookUse("edo.deck", "yard") },
    { id: "spray", name: "spray", rect: [2, 300, 70, 80], walkTo: M.bow, face: "W", ...lookUse("edo.deck", "spray") },
    // the floating cask: its area goes with it while it bobs past, and is not there while it is not (tick: followCask)
    { id: "cask", name: "floating cask", rect: [2, 338, 52, 24], walkTo: M.deck, face: "N", look: each("edo.deck.cask"), use: caskUse },
    { id: "bow", name: "the bow", rect: [0, 359, 64, 195], walkTo: M.bow, face: "W", ...lookUse("edo.deck", "bow") },
    { id: "boat", name: "the ship's boat", rect: [84, 324, 183, 50], walkTo: M.hearth, face: "N", ...lookUse("edo.deck", "boat") },
    { id: "hold", name: "the hold", poly: [[375, 403], [386, 365], [396, 357], [488, 356], [498, 363], [537, 542], [369, 542]], walkTo: M.deck, face: "N", ...lookUse("edo.deck", "hold") },
    { id: "bales", name: "bales", poly: [[244, 515], [245, 483], [245, 450], [247, 429], [253, 415], [264, 402], [276, 388], [282, 386], [283, 472], [244, 542]], walkTo: M.mast, face: "W", ...lookUse("edo.deck", "bales") },
    { id: "casks", name: "casks", rect: [254, 429, 26, 71], walkTo: M.mast, face: "W", ...lookUse("edo.deck", "casks") },
    { id: "mast", name: "mast", rect: [292, 2, 48, 290], walkTo: M.mast, face: "N", ...lookUse("edo.deck", "mast") },
    { id: "rings", name: "iron rings", rect: [292, 292, 48, 183], walkTo: M.mast, face: "N", ...lookUse("edo.deck", "rings") },
    { id: "maststep", name: "mast step", verb: "Knock on", poly: [[267, 530], [354, 530], [357, 508], [357, 475], [278, 475], [267, 494]], walkTo: M.mast, face: "N", look: maststepLook, use: maststepUse },
    { id: "windlass", name: "windlass", rect: [501, 328, 126, 181], walkTo: M.windlass, face: "N", ...lookUse("edo.deck", "windlass") },
    { id: "deckhouse", name: "deckhouse", poly: [[686, 465], [744, 506], [798, 506], [798, 320], [671, 320], [734, 357]], walkTo: M.rail, face: "E", ...lookUse("edo.deck", "deckhouse") },
    { id: "rudder", name: "rudder", rect: [779, 394, 19, 130], walkTo: [740, 566], face: "E", ...lookUse("edo.deck", "rudder") },
    { id: "tiller", name: "tiller", rect: [696, 389, 83, 135], walkTo: [740, 566], face: "N", ...lookUse("edo.deck", "tiller") },
    { id: "hearth", name: "hearth box", poly: [[119, 560], [199, 560], [211, 541], [212, 459], [145, 459], [119, 525]], walkTo: M.hearth, face: "W", ...lookUse("edo.deck", "hearth") },
    { id: "pot", name: "rice pot", rect: [147, 492, 45, 35], walkTo: M.hearth, face: "W", look: potLook, use: each("edo.deck.pot.use") },
    // the crew (the game draws them; their areas go with them)
    { id: "kota", name: "Kōta", verb: "Talk to", rect: [78, 441, 38, 112], walkTo: [150, 582], face: "W", look: each("edo.deck.kota"), use: kotaTalk },
    { id: "denzo", name: "Denzō", verb: "Talk to", rect: [341, 413, 41, 122], walkTo: [400, 572], face: "W", look: each("edo.deck.denzo"), use: (g) => denzoTalk(g) },
    { id: "seijiro", name: "Seijirō", verb: "Talk to", rect: [443, 432, 44, 130], walkTo: [420, 586], face: "E", look: each("edo.deck.seijiro"), use: seijiroTalk },
    { id: "kako1", name: "sailor", verb: "Talk to", rect: [517, 400, 36, 106], walkTo: [520, 560], face: "N", look: each("edo.deck.kako1"), use: nthOf("edo.kako", ["kako1", "kako2"]) },
    // (the sailor up on the windlass is talked to from its left: not from [600, 540], right behind Kanbei, who hid whoever stood there)
    { id: "kako2", name: "sailor", verb: "Talk to", rect: [590, 380, 31, 91], walkTo: [562, 532], face: "N", look: each("edo.deck.kako2"), use: nthOf("edo.kako", ["kako1", "kako2"]) },
    { id: "kanbei", name: "Kanbei", verb: "Talk to", rect: [590, 426, 43, 127], walkTo: [570, 574], face: "E", look: each("edo.deck.kanbei"), use: kanbeiTalk },
    // the compass box, over the old man's shoulder: the ship's clock (opens the close-up)
    { id: "compassbox", name: "compass box", verb: "Look in", rect: [622, 430, 60, 120], walkTo: M.compass, face: "W", look: each("edo.deck.compassbox"), use: compassUse },
    { id: "gonroku", name: "Gonroku", verb: "Talk to", rect: [732, 419, 42, 123], walkTo: [716, 576], face: "E", look: each("edo.deck.gonroku"), use: gonrokuTalk },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and whenever the scene is built.
  setup(g) {
    deck.openAfter = false; deck.gullAt = 9000; deck.peekAt = 4000; deck.peeking = 0; deck.caskShown = false;
    dressFor(g, "outdoors");                                                       // (on deck in the sun, the hats on: edo-yui.js)
    g.loop("sea");
    atRest(g);
    look(g, "gonroku", CAPE);
  },

  // The first time on deck (after "Four days later"): the fifth day, and the ship's talk, once each, as it comes to life.
  async enter(g) {
    // the first words, the first time on deck after Casting Off (a game opened on the deck without it, as the engine test opens
    // it with only edo.arrived, has none: nothing has brought them aboard to say them)
    if (!heard(g, "edo.deck.arrive.1") && is(g, "edo.aboard")) {
      look(g, "bigsis", CAPE);
      await g.say("edo.deck.arrive.1");
      await g.say("edo.deck.arrive.2", "edo.deck.arrive.3");
      look(g, "gonroku", CAPE);
      await g.say("edo.deck.say.gonroku");
      const d = g.actor("denzo");
      if (d) d.look(MASTSTEP[0], MASTSTEP[1]);
      await g.say("edo.deck.say.denzo");
      const k = g.actor("kanbei");
      if (k && k.fidget) k.fidget("squint");
      await g.say("edo.deck.say.kanbei");
      look(g, "kako1", M.kota); look(g, "kako2", M.kota);
      await g.say("edo.deck.say.kako1", "edo.deck.say.kako2");
      atRest(g);
      return;
    }
    await uttermost(g);                                                               // (a game saved with both done: the night)
  },
};

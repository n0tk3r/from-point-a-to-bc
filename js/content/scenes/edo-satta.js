// Act Six, the first stretch: the top of the Satta Pass, the cliff road, morning, wind (SCENES-21A: new in round twenty-one,
// in place of ENGINE-21's stub; the design, briefs/out/edo2-design.md, sections 5 and 7, #24; every line is WRITE-21A's,
// js/content/lines/edo-c.en.js, and the talks are js/content/talk/edo-c.js). The road of 1830, cut high on the mountain in
// 1655; below it the old shore, white water on the rocks ("forget your parent, forget your child"); Fuji enormous across the
// bay under its cap of cloud; the bent pine at the edge leaning toward it; the Jizō by the road, Little Sister's height, in a
// red bib and a little straw hat; Mosuke the woodcutter, who never looks; O-Shige on her stone and Kyūzō with her box.
//
// Mom, Big Sister and Little Sister are here together (`party`). What happens here (#24, steps 2 to 5):
//   the top        the first time: the wind; Mosuke trudges past; O-Shige and Kyūzō puff up the road behind them and she
//                  sits on her stone; a gust takes a folded paper out of Kyūzō's sash onto the Jizō's hat (edo.gust)
//   the pass       Little Sister lifts it off ("Sorry, sir."), or anyone with Mosuke's load pole (edo.poleLent): a woman's
//                  pass in their hands (shigepass; edo.passFound). Used on anyone or on the road west: Mom will not ("It says
//                  fifty, with a mole by the right eye.")
//   O-Shige        given it back (edo.passBack): white, then pink; and because they gave it back, Arai told kindly
//                  (edo.araiHeard): "Then not by road."; "Find a captain."; the cloud lifts off Fuji ("It CAME OUT.":
//                  edo.fujiClear); the old shore's name (edo.oldShoreHeard); "Nobody's forgetting anybody." (edo.noRoad: #24)
//   the road west  the right edge, to Okitsu: refuses, before ("Not till I know what's at Arai.") and after ("Not by road.")
// and a look and a use for each of the three at every thing.
//
// Every place is the painter's (art/scenes/edo-satta/layout.json, PAINT-21A's ready.md).
//
// Try it: index.html?scene=edo-satta&lead=lilsis&flags=edo.arrived,edo.clothes,edo.dressed,edo.hensWest

import { STOCK_DRESSED } from "./edo-common.js";
import { shigeTree, mosukeTree } from "../talk/edo-c.js";
import { scaleAt } from "../../engine/walk.js";
import { dressFor } from "./edo-yui.js";
import { THREE, who, is, heard, each, lookUse, walkOf, look, swap, faceLead, nthOf, giveTo, takeFromAnyone, lookBy, TALK_SATTA } from "./edo-sea.js";

const art = "art/scenes/edo-satta/";

// ---------- the marks (layout.json marks and stands) ----------
const M = {
  below: [24, 578], jizo: [329, 500], pine: [654, 502], view: [262, 498], stone: [196, 516], shige: [147, 501], kyuzo: [212, 504],
  mosukeFrom: [22, 572], mosukeTo: [788, 522], okitsu: [786, 514], arrive_mom: [70, 556], arrive_bigsis: [44, 572], arrive_lilsis: [96, 566],
  shige_arrive: [30, 560],
};
const MOSUKE_HOME = [482, 546];                   // resting on the road with his load, his back to the view (clear of the Jizō: x 360 to 410 hides it)
const MOSUKE_LEND = [292, 524];                   // by the Jizō, the pole held out to its hat
const FUJI = [330, 150], OLDSHORE = [110, 356];

/** What the scene is doing that is not saved (made again whenever it is built). */
export const satta = { gullAt: 0 };

// ---------- the paper on the Jizō's hat ----------
/** Lifted off the hat: by Little Sister (she is his height), or by anyone with Mosuke's pole: `line` is what she says as she
    does it. The pass in the hands of the one who lifted it (shigepass); edo.passFound. */
async function lift(g, line) {
  const me = who(g), l = g.lead;
  if (l) l.look(385, 418);
  await g.reach();
  await g.say(line);
  g.sfx("pickup");
  const p = g.plane("pass");
  if (p) await g.fadePlane("pass", 0, { ms: 300 });
  giveTo(g, me, "shigepass");
  g.flag("edo.passFound", true);
  const m = g.actor("mosuke");
  if (m && m.hold) m.hold(false);
  look(g, "bigsis", me === "bigsis" ? [385, 418] : me); look(g, "lilsis", me === "lilsis" ? [385, 418] : me);
  await g.say("edo.satta.found.1", "edo.satta.found.2");
  if (m && is(g, "edo.poleLent")) await walkOf(g, "mosuke", [MOSUKE_HOME]).then(() => m.face("W"));
}
const passUse = Object.assign(async (g) => {
  const me = who(g), pole = is(g, "edo.poleLent");
  if (me !== "lilsis" && !pole) return g.say(`edo.satta.pass.use.${me}`);
  await lift(g, pole ? `edo.satta.pass.pole.${me}` : "edo.satta.pass.use.lilsis");
}, { lines: [...THREE.map((w) => `edo.satta.pass.use.${w}`), ...THREE.map((w) => `edo.satta.pass.pole.${w}`), "edo.satta.found.1", "edo.satta.found.2"] });
/** The wrong try: the pass used on anyone, or on the road west. Mom will not. */
const passTry = Object.assign(async (g) => {
  if (heard(g, "edo.satta.passuse.1")) return g.say("edo.satta.passuse.again");
  look(g, "bigsis", "mom");
  await g.say("edo.satta.passuse.1", "edo.satta.passuse.2", "edo.satta.passuse.3");
}, { lines: ["edo.satta.passuse.1", "edo.satta.passuse.2", "edo.satta.passuse.3", "edo.satta.passuse.again"] });
const tryPass = { shigepass: passTry };

// ---------- O-Shige ----------
const SHIGE = shigeTree({
  // the pass handed back: she gets up off her stone for it, goes white, then pink, and sits down again
  giveBack: async (g) => {
    const s = g.actor("shige");
    takeFromAnyone(g, "shigepass");
    g.sfx("pickup");
    if (s && s.sit) await s.sit(false);
    if (s && s.hold) s.hold(true, "pass");
    await g.wait(900);
    if (s && s.hold) s.hold(false);
    if (s && s.sit) await s.sit(true);
    faceLead(g, "shige");
  },
  // the cloud lifts off Fuji (the one cap of cloud: ENGINE-21's layer fade); everybody turns to the mountain
  clears: async (g) => {
    for (const id of [...THREE, "shige", "kyuzo"]) look(g, id, FUJI);
    await g.wait(500);
    await g.fadePlane("cloud", 0, { ms: 1500 });
    await g.wait(300);
  },
  // they look down at the old shore under the cliffs
  shore: async (g) => {
    for (const id of [...THREE, "shige"]) look(g, id, OLDSHORE);
    await g.wait(600);
  },
});
const backNode = { mom: "givingMom", bigsis: "givingBig", lilsis: "givingLil" };
const backLine = { mom: "edo.satta.back.1", bigsis: "edo.satta.back.1.big", lilsis: "edo.satta.back.1.lil" };
async function shigeTalk(g, tree = SHIGE) {
  faceLead(g, "shige");
  const before = byes(g), road = is(g, "edo.noRoad");
  await g.talk(tree);
  if (!road && is(g, "edo.noRoad")) await mosukeBack(g);                             // (Mosuke, back the other way with a new load)
  if (byes(g) > before) await shigeGoes(g);                                          // (her goodbye: on down east, to Edo)
}
const byes = (g) => ["afterByeMom", "afterByeBig", "afterByeLil"].reduce((n, o) => n + (g.asked ? g.asked(`shige/${o}`) : 0), 0);
/** The pass used on O-Shige herself: given back (her tree, from the giving, with the giver's own words first). */
const shigePass = Object.assign(async (g) => {
  faceLead(g, "shige");
  const me = who(g);
  if (!is(g, "edo.shigeMet")) { await g.say("edo.shige.first"); g.flag("edo.shigeMet", true); }
  await g.say(backLine[me]);
  await shigeTalk(g, { ...SHIGE, start: (q) => (is(q, "edo.passBack") ? SHIGE.start(q) : backNode[me]) });
}, { lines: Object.values(backLine) });
/** After her goodbye she and Kyūzō go on down the road east, to Edo and the grandson (edo.shigeGone). */
async function shigeGoes(g) {
  const s = g.actor("shige"), k = g.actor("kyuzo");
  if (s && s.sit) await s.sit(false);
  swap(g, "shige", "shige");
  await g.view.cast.load();
  await Promise.all([walkOf(g, "shige", [[120, 540], M.below, [-30, 600]]), g.wait(500).then(() => walkOf(g, "kyuzo", [[150, 548], M.below, [-30, 600]]))]);
  for (const id of ["shige", "kyuzo"]) { const f = g.actor(id); if (f) f.hidden = true; }
  g.flag("edo.shigeGone", true);
  g.rebuildSpots();
}

// ---------- Mosuke ----------
const MOSUKE = mosukeTree({
  // his load pole, lent: he comes to the Jizō and holds it out to the hat (the next use of the paper uses it)
  pole: async (g) => {
    const m = g.actor("mosuke");
    await walkOf(g, "mosuke", [MOSUKE_LEND]);
    if (m) { m.look(385, 418); if (m.hold) m.hold(true, "pole"); }
    await g.wait(400);
  },
});
async function mosukeTalk(g) {
  faceLead(g, "mosuke");
  await g.talk(MOSUKE);
  const m = g.actor("mosuke");
  if (m && !is(g, "edo.poleLent")) m.face("W");                                       // (back to the road: he never looks at Fuji)
}
/** Mosuke passes back the other way with a new load, after "Nobody's forgetting anybody." (edo.mosukeBack). */
async function mosukeBack(g) {
  const m = g.actor("mosuke");
  if (!m || is(g, "edo.mosukeBack")) return;
  if (m.hold) m.hold(false);
  await walkOf(g, "mosuke", [M.mosukeTo, [830, 526]]);
  m.hidden = true;
  await g.wait(1400);
  m.hidden = false;
  await walkOf(g, "mosuke", [M.mosukeTo, MOSUKE_HOME]);
  m.face("W");
  g.flag("edo.mosukeBack", true);
}
const mosukeLook = Object.assign((g) => g.say(`edo.satta.mosuke.${is(g, "edo.mosukeBack") ? "again." : ""}${who(g)}`),
  { lines: THREE.flatMap((w) => [`edo.satta.mosuke.${w}`, `edo.satta.mosuke.again.${w}`]) });

// ---------- the road west: it refuses ----------
const westNo = Object.assign(async (g) => {
  const me = who(g);
  if (is(g, "edo.noRoad")) return g.say(`edo.satta.west.no.${me}`);
  if (me === "mom") return g.say(is(g, "edo.araiWarned") ? "edo.satta.west.notyet.mom" : "edo.satta.west.notyet.0.mom");
  await g.say(`edo.satta.west.notyet.${me}`);
}, { lines: [...THREE.map((w) => `edo.satta.west.no.${w}`), ...THREE.map((w) => `edo.satta.west.notyet.${w}`), "edo.satta.west.notyet.0.mom"] });

// ---------- the looks that change with the story ----------
const fujiLook = lookBy("edo.satta.fuji", "clear", (g) => is(g, "edo.fujiClear"));
const fujiUse = Object.assign((g) => g.say(`edo.satta.fuji.${is(g, "edo.fujiClear") ? "clear.use" : "use"}.${who(g)}`),
  { lines: THREE.flatMap((w) => [`edo.satta.fuji.use.${w}`, `edo.satta.fuji.clear.use.${w}`]) });
const oldshoreLook = lookBy("edo.satta.oldshore", "after", (g) => is(g, "edo.oldShoreHeard"));
const templeLook = Object.assign((g) => g.say(...(who(g) === "bigsis" ? ["edo.satta.temple.bigsis", "edo.satta.temple.bigsis.2"] : [`edo.satta.temple.${who(g)}`])),
  { lines: [...THREE.map((w) => `edo.satta.temple.${w}`), "edo.satta.temple.bigsis.2"] });
const paperOn = (g) => is(g, "edo.gust") && !is(g, "edo.passFound");
/** The Jizō: with the paper on his hat, that is what one sees first. */
const jizoLook = Object.assign((g) => g.say(paperOn(g) ? `edo.satta.jizohat.paper.${who(g)}` : `edo.satta.jizo.${who(g)}`),
  { lines: THREE.flatMap((w) => [`edo.satta.jizo.${w}`, `edo.satta.jizohat.paper.${w}`]) });
const jizohatLook = lookBy("edo.satta.jizohat", "after", (g) => is(g, "edo.passFound"));

// ---------- the first time at the top: the wind, Mosuke, O-Shige, the gust ----------
async function theTop(g) {
  const cast = g.view.cast;
  look(g, "lilsis", FUJI);
  await g.say("edo.satta.arrive.1");
  look(g, "mom", FUJI); look(g, "bigsis", FUJI);
  await g.say("edo.satta.arrive.2", "edo.satta.arrive.3");
  // Mosuke trudges past, up from behind them, and does not look
  const m = g.actor("mosuke");
  if (m) {
    m.place(M.mosukeFrom[0] - 40, M.mosukeFrom[1] + 14, scaleAt(g.scene, M.mosukeFrom[1]));
    await walkOf(g, "mosuke", [M.mosukeFrom, [200, 548], MOSUKE_HOME]);
    m.face("W");
  }
  // O-Shige and Kyūzō, puffing up the road behind them; she sits on her stone, her back to the Jizō
  const s = cast.addFigure("shige", "shige", M.shige_arrive[0] - 40, M.shige_arrive[1] + 12, scaleAt(g.scene, M.shige_arrive[1])).face("E");
  const k = cast.addFigure("kyuzo", "kyuzo", M.shige_arrive[0] - 70, M.shige_arrive[1] + 18, scaleAt(g.scene, M.shige_arrive[1])).face("E");
  await cast.load();
  for (const id of THREE) look(g, id, M.shige_arrive);
  await Promise.all([walkOf(g, "shige", [M.shige_arrive, [110, 520], M.shige]), g.wait(400).then(() => walkOf(g, "kyuzo", [M.shige_arrive, [150, 530], M.kyuzo]))]);
  look(g, "shige", "kyuzo");
  if (s.fidget) s.fidget("puff");
  await g.say("edo.satta.shige.come.1");
  look(g, "kyuzo", "shige");
  await g.say("edo.satta.shige.come.2");
  swap(g, "shige", "shige-stone", M.shige, "S");
  swap(g, "kyuzo", "kyuzo", M.kyuzo, "S");
  await cast.load();
  // the gust: the paper out of his sash and onto the little stone figure's hat; nobody of theirs sees it go
  await g.wait(500);
  g.sfx("wind");
  swap(g, "kyuzo", "kyuzo-nopass", M.kyuzo, "S");
  await cast.load();
  g.flag("edo.gust", true);
  const p = g.plane("pass");
  if (p) { p.fade(0); await g.fadePlane("pass", 1, { ms: 350 }); }
  look(g, "lilsis", [385, 418]);
  await g.say("edo.satta.gust.1");
  look(g, "bigsis", [385, 418]);
  await g.say("edo.satta.gust.2");
  g.rebuildSpots();
}

// ---------- now and then: a gull below the road ----------
function tick(g, dt) {
  if (g.busy || g.dialogue.active) return;
  satta.gullAt -= dt;
  if (satta.gullAt > 0) return;
  satta.gullAt = 15000 + Math.random() * 15000;
  g.sfx("gull");
}

const BAY = [[214, 300], [440, 296], [700, 290], [668, 300], [690, 304], [740, 312], [800, 318], [800, 470], [700, 470], [330, 474], [316, 474], [294, 460], [236, 440], [150, 430], [60, 437], [0, 452], [0, 372], [110, 357], [214, 346]];
const PINE = [[440, 196], [492, 184], [560, 186], [626, 198], [690, 226], [706, 262], [690, 284], [656, 286], [670, 330], [690, 400], [702, 478], [682, 482], [662, 404], [640, 330], [600, 270], [560, 236], [500, 226], [450, 220]];

export default {
  id: "edo-satta",
  era: "edo",
  name: "The top of the Satta Pass",
  // DEPTH (layout.json: persp.Camera(288, 590)): one floor, the road across the picture; the bank is not walked
  horizon: 288, full: 590,
  walk: { area: [[0, 566], [30, 544], [60, 526], [90, 510], [120, 499], [150, 493], [690, 493], [720, 497], [750, 503], [780, 511], [800, 517], [800, 596], [0, 596]] },
  blocked: [[[111, 497], [182, 497], [192, 488], [124, 488]]],      // O-Shige's stone

  party: THREE,
  // (the painter's `below` [24, 578] is the corner itself: the walk down goes there, but the one played comes up onto Mom's
  // arrival mark, the other two onto theirs)
  spawn: { default: M.arrive_mom, ...M, below: M.arrive_mom, mom: M.arrive_mom, bigsis: M.arrive_bigsis, lilsis: M.arrive_lilsis },
  arrive: { below: [M.arrive_bigsis, M.arrive_lilsis] },
  facing: "E",
  edges: {
    W: { to: "edo-kurasawa", spawn: "climb", name: "down to Nishikurasawa", walkTo: M.below },
    E: { name: "on west, to Okitsu", walkTo: [760, 522], use: westNo },
  },
  exits: ["edo-kurasawa"],
  stock: STOCK_DRESSED,
  talk: TALK_SATTA,
  tick,

  picture: art + "back.png",
  planes: [
    // the cap of cloud (the same cloud as at Nishikurasawa): faded out when it lifts (#24, step 5), gone ever after
    { id: "cloud", src: art + "cloud.png", plane: "back", when: (g) => !is(g, "edo.fujiClear") },
    { id: "pine", src: art + "pine.png", base: 475 },
    // O-Shige's pass on the Jizō's hat: from the gust until it is lifted off
    { id: "pass", src: art + "pass.png", base: 488, when: paperOn },
    { id: "front", src: art + "front.png", plane: "front" },
  ],
  fx: [
    { id: "pine-sway", type: "sway", plane: "pine", anchor: "bottom", at: 475, amount: 2.2, period: 3.8, wave: 40, lean: -0.4 },
    { id: "cloud-drift", type: "bob", plane: "cloud", amount: 1, period: 11, when: (g) => !is(g, "edo.fujiClear") },
    { id: "oldshore-waves", type: "waves", area: [[-10, 366], [30, 363], [70, 359], [110, 355], [150, 350], [186, 346], [214, 344], [224, 362], [196, 364], [160, 368], [120, 373], [80, 377], [40, 381], [0, 384]],
      rows: 3, per: 10, size: 3, speed: 4, toward: "N", color: "#f4f8fb", opacity: 0.7, plane: "back" },
    { id: "flank-waves", type: "waves", area: [[-10, 438], [24, 430], [60, 423], [104, 418], [150, 416], [196, 419], [236, 426], [268, 435], [294, 446], [316, 460], [316, 473], [294, 459], [268, 448], [236, 439], [196, 432], [150, 429], [104, 431], [60, 436], [24, 443], [-10, 451]],
      rows: 3, per: 12, size: 4, speed: 4, toward: "S", color: "#f4f8fb", opacity: 0.55, plane: "back" },
    { id: "bay-shimmer", type: "shimmer", poly: BAY, count: 30, size: 4, flow: [-3, 0], life: 1.8, color: "#f6eed8", opacity: 0.45, plane: "back", holes: [[[620, 300], [800, 300], [800, 476], [620, 476]]] },
    { id: "bay-waves", type: "waves", area: [[230, 340], [800, 330], [800, 470], [330, 474], [300, 440], [230, 380]], holes: [[[630, 300], [720, 300], [720, 476], [630, 476]]],
      rows: 8, per: 9, size: 5, speed: 4, toward: "S", color: "#f4f8fb", opacity: 0.35, plane: "back" },
    { id: "gulls", type: "birds", plane: "back", lanes: [[[810, 360], [600, 340], [420, 372], [260, 344], [-12, 380]], [[-12, 420], [180, 400], [380, 418], [560, 396], [810, 420]], [[810, 250], [640, 236], [470, 262], [300, 230], [-12, 258]]],
      every: [7, 14], group: [1, 2], speed: 34, size: 8, scale: [0.7, 1.15], color: "#f6eed8", behind: [[[618, 160], [800, 160], [800, 480], [618, 480]]] },
  ],

  // The people at the top (PEOPLE-21A's kinds). O-Shige and Kyūzō come up the road the first time (theTop) and stay until her
  // goodbye; Mosuke rests on the road with his load, and walks it a little now and then, never toward the view.
  actors: [
    { id: "mosuke", kind: "mosuke", at: MOSUKE_HOME, face: "W", life: { fidget: [8, 14], every: [30, 50], spots: [[600, 528, "E"], [482, 546, "W"]], stay: [6, 12] } },
    { id: "shige", kind: "shige-stone", at: M.shige, face: "S", when: (g) => is(g, "edo.gust") && !is(g, "edo.shigeGone"), life: { fidget: [6, 11], still: true } },
    { id: "kyuzo", kind: "kyuzo-nopass", at: M.kyuzo, face: "S", when: (g) => is(g, "edo.gust") && !is(g, "edo.shigeGone"), life: { fidget: [7, 13], still: true } },
  ],

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "fuji", name: "Mount Fuji", rect: [150, 30, 400, 258], walkTo: M.view, face: "N", look: fujiLook, use: fujiUse },
    { id: "cloud", name: "cloud", poly: [[241, 60], [267, 44], [294, 35], [321, 31], [348, 32], [375, 36], [401, 46], [415, 53], [415, 59], [388, 62], [361, 67], [334, 70], [308, 68], [281, 64], [254, 59], [241, 58]],
      walkTo: M.view, face: "N", ...lookUse("edo.satta", "cloud"), when: (g) => !is(g, "edo.fujiClear") },
    { id: "izu", name: "Izu", poly: [[430, 290], [452, 278], [516, 269], [584, 267], [646, 275], [700, 290]], walkTo: M.view, face: "N", ...lookUse("edo.satta", "izu") },
    { id: "bay", name: "the bay", poly: BAY, walkTo: M.view, face: "N", ...lookUse("edo.satta", "bay") },
    { id: "oldshore", name: "the old shore", poly: [[-10, 340], [70, 337], [150, 333], [186, 336], [214, 346], [214, 352], [186, 354], [150, 358], [70, 367], [-10, 374]], walkTo: M.view, face: "N",
      look: oldshoreLook, use: each("edo.satta.oldshore.use") },
    { id: "okitsu", name: "Okitsu", rect: [700, 270, 100, 46], walkTo: M.okitsu, face: "N", look: each("edo.satta.okitsu"), use: each("edo.satta.okitsu.use"), useWith: tryPass },
    { id: "temple", name: "a temple roof", rect: [726, 280, 40, 18], walkTo: M.okitsu, face: "N", look: templeLook, use: each("edo.satta.temple.use"), useWith: tryPass },
    { id: "gulls", name: "gulls", rect: [240, 300, 380, 140], walkTo: M.view, face: "N", ...lookUse("edo.satta", "gulls") },
    { id: "edge", name: "the edge", poly: [[0, 517], [50, 487], [100, 467], [150, 451], [250, 460], [350, 453], [450, 451], [600, 455], [700, 452], [750, 466], [800, 481], [800, 514], [750, 500], [700, 491], [150, 490], [100, 503], [50, 529], [0, 563]],
      walkTo: M.view, face: "N", ...lookUse("edo.satta", "edge") },
    { id: "pine", name: "pine", poly: PINE, walkTo: M.pine, face: "N", ...lookUse("edo.satta", "pine") },
    // the road, short of the edges' bands (left: down to Nishikurasawa; right: on west, which refuses)
    { id: "road", name: "the road west", poly: [[46, 532], [50, 529], [100, 503], [150, 490], [700, 491], [750, 500], [754, 501], [754, 568], [46, 568]], walkTo: [470, 548], face: "E",
      look: each("edo.satta.road"), use: westNo, useWith: tryPass },
    { id: "jizo", name: "Jizō", rect: [367, 407, 35, 84], walkTo: M.jizo, face: "N", look: jizoLook, use: each("edo.satta.jizo.use"), useWith: tryPass },
    { id: "jizohat", name: "the Jizō's hat", rect: [369, 408, 31, 18], walkTo: M.jizo, face: "N", look: jizohatLook, use: each("edo.satta.jizohat.use") },
    // the folded paper caught on the hat: the hat's whole area to click (it is small), while it is there
    { id: "pass", name: "folded paper", verb: "Take", rect: [362, 404, 42, 30], walkTo: M.jizo, face: "N", look: each("edo.satta.pass"), use: passUse, when: paperOn },
    // the people (the game draws them; their areas go with them)
    { id: "mosuke", name: "Mosuke", verb: "Talk to", rect: [458, 430, 48, 118], walkTo: [540, 562], face: "W", look: mosukeLook, use: mosukeTalk, useWith: tryPass },
    { id: "shige", name: "O-Shige", verb: "Talk to", rect: [133, 433, 27, 68], walkTo: [197, 519], face: "W", look: each("edo.satta.shige"), use: (g) => shigeTalk(g),
      useWith: { shigepass: shigePass }, when: (g) => is(g, "edo.gust") && !is(g, "edo.shigeGone") },
    { id: "kyuzo", name: "Kyūzō", verb: "Talk to", rect: [192, 402, 41, 102], walkTo: [262, 522], face: "W", look: each("edo.satta.kyuzo"), use: nthOf("edo.kyuzo", "kyuzo"),
      useWith: tryPass, when: (g) => is(g, "edo.gust") && !is(g, "edo.shigeGone") },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and whenever the scene is built.
  setup(g) {
    satta.gullAt = 8000;
    dressFor(g, "outdoors");                                                       // (O-Tami's clothes, the hats on: edo-yui.js)
    g.loop("wind");
    const m = g.actor("mosuke");
    if (m && is(g, "edo.poleLent") && !is(g, "edo.passFound")) {                      // (his pole still held out to the hat)
      m.place(MOSUKE_LEND[0], MOSUKE_LEND[1], scaleAt(g.scene, MOSUKE_LEND[1]));
      m.look(385, 418);
      if (m.hold) m.hold(true, "pole");
    }
  },

  // The first time they reach the top: the wind, the view, Mosuke, O-Shige and Kyūzō, and the gust (edo.gust).
  async enter(g) {
    if (!is(g, "edo.gust")) await theTop(g);
  },
};

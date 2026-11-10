// Act Six, the first stretch: Nishikurasawa, the rest village at the foot of the Satta Pass, morning (SCENES-21A: new in
// round twenty-one, in place of ENGINE-21's stub; the design, briefs/out/edo2-design.md, sections 5 and 7, #24; every line is
// WRITE-21A's, js/content/lines/edo-c.en.js, and the talks are js/content/talk/edo-c.js). O-Kuni's teahouse with its bench and
// its grill of turban shells hissing in their own juice, the 40th distance mound from Edo with its hackberry, the bearers'
// palanquin set down by it (Sakuji and Tora squatting on its pole), Sōshichi the Toyama peddler by his trunks, the komusō
// playing under his basket hat; across the bay Fuji under its cap of cloud; the relay courier running through now and then.
//
// Mom, Big Sister and Little Sister are here together (`party`), in O-Tami's clothes (they come from Yui's west end once
// dressed: edo-village.js). What happens here (#24, step 1):
//   O-Kuni         one shell to share, for the climb (edo.shellShared); "And your pass?" (tegata; Big Sister: "We're IN a
//                  pass."); women going west need papers at Arai (edo.araiWarned); back down, after the top (edo.kuniBack)
//   the bearers    a fare and drink money on top; Little Sister's three pennies ("...What's a penny?"); she sits in the
//                  palanquin, and bounces a very little
//   Sōshichi       use first, pay later; his ledger; a print for the child of the house (toyamaprint, Little Sister's)
//   the komusō     "Nobody sees his face, and his kind may pass any barrier." "That's a lie with a basket on it." (the wrong try)
//   the climb      the right edge: up the cliff road to the top of the pass (edo-satta, `below`)
// and a look and a use for each of the three at every thing.
//
// Every place is the painter's (art/scenes/edo-kurasawa/layout.json, PAINT-21A's ready.md): the camera, the walk, the marks,
// the cut-outs, the things' shapes and stands, the fx; the people at their marks, at the people's own heights.
// PAINT-23 (round twenty-three, RECOMPOSE: tools/paint/DEPTH.md): painted again from a new place through a new camera, in
// three planes and in watercolour: we stand on the Tokaido short of the teahouse and look along the road toward the pass
// (the teahouse three-quarters on at the left, the mound and its hackberry at the right, Fuji and the bay between; the road
// in from Yui at the bottom left, round the bend to the climb at the right edge). Every number below was measured again by
// tools/paint/edo_kurasawa_layout.py; ids, lines and logic are as they were.
//
// Try it: index.html?scene=edo-kurasawa&lead=mom&flags=edo.arrived,edo.clothes,edo.dressed

import { STOCK_DRESSED } from "./edo-common.js";
import { kuniTree, bearersTree, soshichiTree } from "../talk/edo-c.js";
import { sitOnStep, standFromStep, dressFor } from "./edo-yui.js";
import { THREE, who, is, heard, each, lookUse, walkOf, look, faceLead, once, TALK_KURASAWA } from "./edo-sea.js";

const art = "art/scenes/edo-kurasawa/";

// ---------- the marks (layout.json marks and stands) ----------
const M = {
  yui: [12, 592], teahouse: [94, 539], kuni: [261, 481], mound: [728, 471], bearers: [538, 483], peddler: [742, 538], komuso: [410, 472],
  courierFrom: [4, 588], courierTo: [796, 501], climb: [772, 498], view: [281, 508], tora: [598, 478],
  arrive_mom: [133, 566], arrive_bigsis: [31, 555], arrive_lilsis: [240, 585],
};
// Down from the top (the road comes down to the right edge): the other two beside the one played, on the climb's foot.
const FROM_TOP = [[706, 478], [668, 476]];
// O-Kuni's gift: the three round her grill (she leans over it with the shell on a leaf).
const AT_GRILL = { mom: [218, 506], bigsis: [350, 487], lilsis: [298, 501] };
// Little Sister in the palanquin: behind its front (the cut-out `kago`, its base the line [[511, 487], [629, 457]]), her seat on its cushion.
const KAGO_SEAT = [553, 467];

/** What the scene is doing that is not saved (made again whenever it is built). */
export const kurasawa = { gullAt: 0, fluteAt: 0 };

// ---------- the people's talks ----------
const KUNI = kuniTree({
  // the shell, hot, on a leaf, held out over the grill; the three come round it and share it
  shell: async (g) => {
    const k = g.actor("kuni");
    if (k && k.hold) k.hold(true, "offer");
    await Promise.all(THREE.map((id) => g.walkTo(AT_GRILL[id][0], AT_GRILL[id][1], id)));
    for (const id of THREE) look(g, id, M.kuni);
    if (k) k.look(AT_GRILL.mom[0], AT_GRILL.mom[1]);
    await g.reach();
    await g.wait(500);
    if (k && k.hold) k.hold(false);
  },
});
async function kuniTalk(g) {
  faceLead(g, "kuni");
  await g.talk(KUNI);
  const k = g.actor("kuni");
  if (k && k.hold) k.hold(false);
}

const BEARERS = bearersTree({
  // Little Sister climbs into the palanquin, sits on its cushion, bounces a very little, and climbs out
  sit: async (g) => {
    const l = g.actor("lilsis");
    if (!l) return;
    await sitOnStep(g, "lilsis", KAGO_SEAT, "S");
    for (let n = 0; n < 2; n++) { const [x, y] = [l.x, l.y]; await g.tween(160, (k) => l.place(x, y - 2 * Math.sin(k * Math.PI))); }
    look(g, "sakuji", "lilsis"); look(g, "tora", "lilsis");
    await g.wait(400);
  },
});
async function bearersTalk(g) {
  faceLead(g, "sakuji"); faceLead(g, "tora");
  const s = g.actor("sakuji");
  if (s && s.hold) s.hold(true, "fare");
  await g.talk(BEARERS);
  if (s && s.hold) s.hold(false);
  await standFromStep(g, "lilsis");                                              // (out of the palanquin, if she sat in it)
}

const SOSHICHI = soshichiTree({
  // a print from the second tier, for the child of the house: Little Sister's (the tree offers it to her alone)
  print: async (g) => {
    const s = g.actor("soshichi"), l = g.actor("lilsis");
    if (s && s.hold) s.hold(true, "print");
    if (l) await g.walkTo(706, 560, "lilsis");
    if (l) l.look(M.peddler[0], M.peddler[1]);
    await g.wait(400);
    giveLilsis(g, "toyamaprint");
    if (s && s.hold) s.hold(false);
    if (l && l.hold) l.hold(true, "print");                                      // (she looks at it: "a man making a SCARY face")
  },
});
async function soshichiTalk(g) {
  faceLead(g, "soshichi");
  await g.talk(SOSHICHI);
  const l = g.actor("lilsis");
  if (l && l.hold) l.hold(false);
}
/** The print is Little Sister's (the one being played is she, when he gives it: the tree offers it to her alone). */
function giveLilsis(g, item) {
  if (who(g) === "lilsis") { g.give(item); return; }
  const p = g.store.data.inventory.lilsis || (g.store.data.inventory.lilsis = []);
  if (!p.includes(item)) p.push(item);
  g.store.emit();
}

// ---------- the looks and uses that change with the story ----------
const shellsLook = Object.assign((g) => g.say(`edo.kurasawa.shells.${is(g, "edo.shellShared") ? "after." : ""}${who(g)}`),
  { lines: THREE.flatMap((w) => [`edo.kurasawa.shells.${w}`, `edo.kurasawa.shells.after.${w}`]) });
/** The mound: a look, and the first time while Sōshichi is there, his count. */
const moundLook = Object.assign(async (g) => {
  await g.say(`edo.kurasawa.mound.${who(g)}`);
  if (heard(g, "edo.kurasawa.mound.soshichi") || !g.actor("soshichi")) return;
  faceLead(g, "soshichi");
  await g.say("edo.kurasawa.mound.soshichi");
}, { lines: [...THREE.map((w) => `edo.kurasawa.mound.${w}`), "edo.kurasawa.mound.soshichi"] });
/** The komusō: Big Sister's look has Mom's answer; the first use by anyone is the wrong try (the basket hat past the barriers). */
const komusoLook = Object.assign((g) => g.say(...(who(g) === "bigsis" ? ["edo.kurasawa.komuso.bigsis", "edo.kurasawa.komuso.bigsis.2"] : [`edo.kurasawa.komuso.${who(g)}`])),
  { lines: [...THREE.map((w) => `edo.kurasawa.komuso.${w}`), "edo.kurasawa.komuso.bigsis.2"] });
const komusoUse = Object.assign(async (g) => {
  if (!heard(g, "edo.kurasawa.komuso.idea.1")) { look(g, "bigsis", "komuso"); look(g, "mom", "bigsis"); return g.say("edo.kurasawa.komuso.idea.1", "edo.kurasawa.komuso.idea.2"); }
  await g.say(`edo.kurasawa.komuso.use.${who(g)}`);
}, { lines: [...THREE.map((w) => `edo.kurasawa.komuso.use.${w}`), "edo.kurasawa.komuso.idea.1", "edo.kurasawa.komuso.idea.2"] });

// ---------- the ways out ----------
/** Up the cliff road to the top of the pass (the right edge, the cliff road, the road): a word the first time (and the first
    time after the top), and up. */
const climb = (line) => Object.assign(async (g) => {
  await once(g, `${line(g)}.${who(g)}`);
  await g.goto("edo-satta", { spawn: "below" });
}, { lines: THREE.flatMap((w) => [`edo.kurasawa.cliffroad.use.${w}`, `edo.kurasawa.cliffroad.again.${w}`]) });
const upTheCliff = climb((g) => (is(g, "edo.noRoad") ? "edo.kurasawa.cliffroad.again" : "edo.kurasawa.cliffroad.use"));
const roadUse = Object.assign(async (g) => {
  await g.say(`edo.kurasawa.road.use.${who(g)}`);
  await g.goto("edo-satta", { spawn: "below" });
}, { lines: THREE.map((w) => `edo.kurasawa.road.use.${w}`) });

// ---------- now and then: a gull; the komusō's few notes ----------
function tick(g, dt) {
  if (g.busy || g.dialogue.active) return;
  kurasawa.gullAt -= dt; kurasawa.fluteAt -= dt;
  if (kurasawa.gullAt <= 0) { kurasawa.gullAt = 16000 + Math.random() * 16000; g.sfx("gull"); }
  if (kurasawa.fluteAt <= 0) { kurasawa.fluteAt = 22000 + Math.random() * 18000; g.sfx("komuso"); }
}

const TEAHOUSE = [[0, 59], [22, 89], [112, 110], [357, 295], [357, 318], [287, 464], [257, 486], [0, 525]];
const BAY = [[300, 343], [440, 343], [522, 344], [536, 372], [552, 404], [554, 397], [500, 400], [440, 403], [380, 405], [330, 406], [300, 407]];
const HACKBERRY = [[400, 0], [800, 0], [800, 272], [693, 235], [679, 368], [622, 368], [608, 216], [460, 130], [400, 100]];

export default {
  id: "edo-kurasawa",
  era: "edo",
  name: "Nishikurasawa",
  // DEPTH (layout.json: persp.Camera(342, 562), focal 680: the eye 2.4 m above the road; PAINT-23): one floor, the
  // road round its bend and the trodden ground either side of it
  horizon: 342, full: 562,
  walk: { area: [[0, 600], [0, 525], [42, 517], [128, 502], [201, 490], [244, 483], [291, 475], [330, 468], [330, 464], [375, 442], [462, 442], [516, 451], [543, 457], [583, 462], [632, 466], [684, 468], [732, 467], [800, 476], [800, 556], [700, 566], [600, 574], [500, 582], [420, 588], [330, 594], [260, 600]] },
  // the grill, the signboard's foot, the trunks on their cloth, the palanquin's near half (layout.json blocked)
  blocked: [
    [[250, 497], [321, 484], [299, 478], [228, 491]], [[345, 474], [361, 471], [349, 468], [333, 471]], [[657, 557], [692, 539], [642, 530], [609, 545]], [[528, 484], [625, 459], [608, 457], [509, 481]],
  ],

  party: THREE,
  // (the painter's `yui` [16, 532] is on the edge itself, half out of the picture: the walk out goes there, but the one played
  // comes in on Mom's arrival mark, the other two on theirs)
  spawn: { default: M.arrive_mom, ...M, yui: M.arrive_mom, mom: M.arrive_mom, bigsis: M.arrive_bigsis, lilsis: M.arrive_lilsis },
  arrive: { yui: [M.arrive_bigsis, M.arrive_lilsis], climb: FROM_TOP },
  facing: "E",
  edges: {
    W: { to: "edo-village", spawn: "fromWest", name: "back to Yui", walkTo: M.yui },
    E: { to: "edo-satta", spawn: "below", name: "up the cliff road", walkTo: M.climb, use: upTheCliff },
  },
  exits: ["edo-village", "edo-satta"],
  stock: STOCK_DRESSED,
  talk: TALK_KURASAWA,
  tick,

  picture: art + "back.png",
  planes: [
    // Fuji's cap of cloud: the same cloud as at the top; once it has lifted there (edo.fujiClear) it is gone here too
    { id: "cloud", src: art + "cloud.png", plane: "back", when: (g) => !is(g, "edo.fujiClear") },
    { id: "kago", src: art + "kago.png", base: [[511, 487], [629, 457]] },
    { id: "noren", src: art + "noren.png", base: [[189, 479], [253, 469]] },
    { id: "trunks", src: art + "trunks.png", base: [[659, 558], [692, 539]] },
    { id: "grill", src: art + "grill.png", base: [[251, 495], [312, 484]] },
    { id: "front", src: art + "front.png", plane: "front" },
    // PAINT-23: the near plane: the hackberry's crown and its bough over the top right; the near end of O-Kuni's eave and its blind
    { id: "near", src: art + "near.png", plane: "front" },
  ],
  fx: [
    { id: "grill-smoke", type: "smoke", at: [275, 458], base: 489, height: 76, width: [4, 24], lean: [34, -76], rise: 12, rate: 3, gust: 0.35, color: "#e4e6ea", opacity: 0.34 },
    { id: "grill-embers", type: "embers", at: [275, 458], size: [54, 5], base: 489, glowOpacity: 0.1, sparks: 0.08 },
    { id: "bay-waves", type: "waves", area: BAY, rows: 8, per: 8, size: 4, speed: 3, toward: "S", color: "#f4f8fb", opacity: 0.36, plane: "back" },
    { id: "bay-shimmer", type: "shimmer", poly: BAY, count: 20, size: 4, flow: [3, 0], life: 1.8, color: "#f6eed8", opacity: 0.45, plane: "back" },
    { id: "noren-sway", type: "sway", plane: "noren", anchor: "top", amount: 2.0, period: 3.4, wave: 22, lean: 0.35 },
    { id: "cloud-drift", type: "bob", plane: "cloud", amount: 1, period: 11, when: (g) => !is(g, "edo.fujiClear") },
    { id: "gulls", type: "birds", plane: "back", lanes: [[[-12, 150], [180, 190], [330, 250], [440, 236], [470, -12]], [[480, -12], [440, 230], [340, 270], [200, 200], [-12, 170]]],
      every: [8, 16], group: [1, 2], speed: 50, size: 7, scale: [0.6, 1.0], color: "#f6eed8", behind: [TEAHOUSE, HACKBERRY] },
    // the relay courier (PEOPLE-21A's runner): along the road's middle, both ways, now and then (ENGINE-21's passer): in from
    // the bottom left corner (from Yui) round the bend to the climb at the right edge; sorted by his feet with the cut-outs (in
    // front of the grill, the sign and the palanquin, behind Soshichi's trunks on the verge, behind the near plane); his area goes with him
    { id: "courier", type: "passer", kind: "courier", path: [[-40, 602], M.courierFrom, [111, 568], [197, 548], [282, 528], [350, 514], [422, 503], [493, 497], [566, 494], [641, 494], [721, 496], M.courierTo, [840, 501]], every: [18, 34], both: true, area: "courier" },
  ],

  // The people of the rest village (PEOPLE-21A's kinds, at the painter's marks)
  actors: [
    { id: "kuni", kind: "kuni", at: M.kuni, face: "S", life: { fidget: [5, 10], still: true } },
    { id: "sakuji", kind: "sakuji", at: M.bearers, face: "S", life: { fidget: [5, 9], still: true } },
    { id: "tora", kind: "tora", at: M.tora, face: "S", life: { fidget: [8, 14], still: true } },
    { id: "soshichi", kind: "soshichi-free", at: M.peddler, face: "S", life: { fidget: [7, 12], still: true } },
    { id: "komuso", kind: "komuso-play", at: M.komuso, face: "W", life: { fidget: [6, 11], still: true } },
  ],

  // Back to front: a later area lies over an earlier one.
  hotspots: [
    { id: "fuji", name: "Mount Fuji", rect: [182, 122, 340, 218], walkTo: M.view, face: "N", ...lookUse("edo.kurasawa", "fuji") },
    { id: "cloud", name: "cloud", poly: [[237, 149], [248, 141], [259, 135], [271, 131], [282, 128], [293, 126], [304, 125], [316, 124], [327, 125], [338, 126], [350, 129], [361, 132], [372, 137], [383, 143], [383, 148], [372, 149]],
      walkTo: M.view, face: "N", ...lookUse("edo.kurasawa", "cloud"), when: (g) => !is(g, "edo.fujiClear") },
    { id: "bay", name: "the bay", poly: BAY, walkTo: M.view, face: "N", ...lookUse("edo.kurasawa", "bay") },
    { id: "yuishore", name: "the shore of Yui", poly: [[292, 328], [440, 330], [452, 345], [292, 345]], walkTo: M.view, face: "N", ...lookUse("edo.kurasawa", "yuishore") },
    { id: "boats", name: "boats", rect: [330, 330, 180, 62], walkTo: M.view, face: "N", ...lookUse("edo.kurasawa", "boats") },
    { id: "hackberry", name: "hackberry", poly: HACKBERRY, walkTo: M.mound, face: "N", ...lookUse("edo.kurasawa", "hackberry") },
    { id: "cliffroad", name: "the cliff road", verb: "Go up", poly: [[584, 314], [700, 276], [800, 246], [800, 262], [700, 292], [596, 326]], walkTo: M.climb, face: "E",
      look: each("edo.kurasawa.cliffroad"), use: upTheCliff },
    { id: "teahouse", name: "teahouse", poly: TEAHOUSE, walkTo: M.teahouse, face: "N", ...lookUse("edo.kurasawa", "teahouse") },
    { id: "smoke", name: "smoke", rect: [247, 395, 56, 64], walkTo: [298, 501], face: "N", ...lookUse("edo.kurasawa", "smoke") },
    { id: "signboard", name: "signboard", rect: [335, 377, 23, 95], walkTo: [363, 481], face: "N", ...lookUse("edo.kurasawa", "signboard") },
    { id: "mound", name: "distance mound", rect: [524, 350, 230, 117], walkTo: M.mound, face: "N", look: moundLook, use: each("edo.kurasawa.mound.use") },
    { id: "palanquin", name: "palanquin", rect: [484, 401, 130, 74], walkTo: [560, 501], face: "N", ...lookUse("edo.kurasawa", "palanquin") },
    { id: "trunks", name: "willow trunks", rect: [608, 443, 85, 116], walkTo: [618, 567], face: "N", ...lookUse("edo.kurasawa", "trunks") },
    { id: "bench", name: "bench", rect: [0, 460, 154, 77], walkTo: M.teahouse, face: "N", ...lookUse("edo.kurasawa", "bench") },
    // the road, short of the edges' bands (left: back to Yui; right: up the cliff road), which are its ways out
    { id: "road", name: "the road", verb: "Go up", poly: [[46, 549], [96, 517], [166, 504], [235, 492], [310, 482], [382, 474], [452, 470], [522, 467], [594, 467], [658, 468], [715, 470], [754, 471], [754, 540], [695, 535], [648, 535], [604, 536], [561, 539], [520, 543], [481, 550], [443, 560], [46, 560]], walkTo: [350, 514], face: "E", look: each("edo.kurasawa.road"), use: roadUse },
    // the people (the game draws them; their areas go with them). O-Kuni stands behind her grill: the grill and the shells over her.
    { id: "kuni", name: "O-Kuni", verb: "Talk to", rect: [246, 397, 30, 84], walkTo: [213, 499], face: "E", look: each("edo.kurasawa.kuni"), use: kuniTalk },
    { id: "grill", name: "grill", rect: [233, 449, 82, 48], walkTo: [298, 501], face: "N", ...lookUse("edo.kurasawa", "grill") },
    { id: "shells", name: "turban shells", rect: [248, 444, 47, 16], walkTo: [298, 501], face: "N", look: shellsLook, use: each("edo.kurasawa.shells.use") },
    { id: "sakuji", name: "Sakuji", verb: "Talk to", rect: [522, 395, 32, 88], walkTo: [484, 495], face: "E", look: each("edo.kurasawa.sakuji"), use: bearersTalk },
    { id: "tora", name: "Tora", verb: "Talk to", rect: [581, 381, 35, 97], walkTo: [568, 500], face: "N", look: each("edo.kurasawa.tora"), use: bearersTalk },
    { id: "soshichi", name: "Sōshichi", verb: "Talk to", rect: [719, 411, 46, 127], walkTo: [678, 562], face: "E", look: each("edo.kurasawa.soshichi"), use: soshichiTalk },
    { id: "komuso", name: "komusō", rect: [394, 386, 31, 86], walkTo: [354, 482], face: "E", look: komusoLook, use: komusoUse },
    // the courier: his area is his figure's box while he runs past (the passer moves it), and is not there while he is not
    { id: "courier", name: "courier", rect: [379, 405, 42, 115], walkTo: [350, 514], face: "S", ...lookUse("edo.kurasawa", "courier") },
  ],

  // Make the picture match the story. Runs on arrival, after loading a save, and whenever the scene is built.
  setup(g) {
    kurasawa.gullAt = 9000; kurasawa.fluteAt = 6000;
    dressFor(g, "outdoors");                                                       // (O-Tami's clothes, the hats on: edo-yui.js)
    g.loop("sizzle", { level: 0.8 });                                              // (the shells on the grill)
  },

  // The first time they come: the smell of the grill (on the mark `yui`, the three on the road from Yui).
  async enter(g) {
    if (heard(g, "edo.kurasawa.arrive.1")) return;
    look(g, "lilsis", M.kuni);
    await g.say("edo.kurasawa.arrive.1", "edo.kurasawa.arrive.2");
    look(g, "mom", M.kuni);
    await g.say("edo.kurasawa.arrive.3");
  },
};

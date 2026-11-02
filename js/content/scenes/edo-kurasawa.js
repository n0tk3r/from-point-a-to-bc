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
//
// Try it: index.html?scene=edo-kurasawa&lead=mom&flags=edo.arrived,edo.clothes,edo.dressed

import { STOCK_DRESSED } from "./edo-common.js";
import { kuniTree, bearersTree, soshichiTree } from "../talk/edo-c.js";
import { sitOnStep, standFromStep, dressFor } from "./edo-yui.js";
import { THREE, who, is, heard, each, lookUse, walkOf, look, faceLead, once, TALK_KURASAWA } from "./edo-sea.js";

const art = "art/scenes/edo-kurasawa/";

// ---------- the marks (layout.json marks and stands) ----------
const M = {
  yui: [16, 532], teahouse: [96, 494], kuni: [224, 471], mound: [598, 434], bearers: [446, 462], peddler: [376, 486], komuso: [668, 506],
  courierFrom: [6, 516], courierTo: [794, 508], climb: [784, 466], view: [300, 476], tora: [470, 470],
  arrive_mom: [40, 524], arrive_bigsis: [26, 546], arrive_lilsis: [58, 540],
};
// Down from the top (the cliff road comes in at the right edge): the other two beside the one played, on the road's foot.
const FROM_TOP = [[760, 486], [742, 500]];
// O-Kuni's gift: the three round her grill (she leans over it with the shell on a leaf).
const AT_GRILL = { mom: [190, 500], bigsis: [252, 504], lilsis: [222, 494] };
// Little Sister in the palanquin: behind its front (the cut-out `kago`, base 448), her seat on its cushion.
const KAGO_SEAT = [482, 440];

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
    if (l) await g.walkTo(340, 500, "lilsis");
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

const TEAHOUSE = [[-301, 358], [313, 358], [178, 197], [-12, 197], [0, 470]];
const BAY = [[300, 302], [520, 304], [510, 372], [546, 410], [552, 428], [527, 435], [495, 436], [461, 438], [426, 439], [391, 440], [356, 441], [320, 442], [283, 443], [300, 360]];

export default {
  id: "edo-kurasawa",
  era: "edo",
  name: "Nishikurasawa",
  // DEPTH (layout.json: persp.Camera(300, 590), as Yui's): one floor, the road and the rest place before the mound
  horizon: 300, full: 590,
  walk: { area: [[0, 476], [178, 476], [184, 470], [212, 468], [262, 468], [276, 474], [300, 466], [336, 462], [392, 452], [430, 444], [470, 436], [520, 428], [560, 426], [580, 428], [632, 436], [652, 458], [672, 478], [700, 482], [740, 472], [780, 458], [800, 452], [800, 596], [0, 596]] },
  // the grill, the signboard's foot, the trunks, the palanquin, the mound (layout.json blocked)
  blocked: [
    [[164, 482], [246, 482], [252, 475], [172, 475]], [[281, 473], [300, 473], [302, 471], [283, 471]], [[308, 476], [366, 476], [364, 468], [314, 469]],
    [[458, 449], [511, 449], [505, 441], [455, 441]],
    [[710, 411], [686, 405], [650, 401], [611, 400], [574, 400], [547, 403], [535, 408], [542, 414], [570, 419], [614, 423], [662, 424], [699, 421], [716, 416]],
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
    { id: "kago", src: art + "kago.png", base: 448 },
    { id: "noren", src: art + "noren.png", base: 467 },
    { id: "trunks", src: art + "trunks.png", base: 475 },
    { id: "grill", src: art + "grill.png", base: 481 },
    { id: "front", src: art + "front.png", plane: "front" },
  ],
  fx: [
    { id: "grill-smoke", type: "smoke", at: [214, 445], base: 481, height: 70, width: [4, 22], lean: [26, -70], rise: 12, rate: 3, gust: 0.35, color: "#e4e6ea", opacity: 0.34 },
    { id: "grill-embers", type: "embers", at: [214, 445], size: [26, 4], base: 481, glowOpacity: 0.1, sparks: 0.08 },
    { id: "bay-waves", type: "waves", area: BAY, rows: 9, per: 8, size: 4, speed: 3, toward: "S", color: "#f4f8fb", opacity: 0.38, plane: "back" },
    { id: "bay-shimmer", type: "shimmer", poly: BAY, count: 22, size: 4, flow: [3, 0], life: 1.8, color: "#f6eed8", opacity: 0.45, plane: "back" },
    { id: "noren-sway", type: "sway", plane: "noren", anchor: "top", amount: 2.2, period: 3.4, wave: 26, lean: 0.35 },
    { id: "cloud-drift", type: "bob", plane: "cloud", amount: 1, period: 11, when: (g) => !is(g, "edo.fujiClear") },
    { id: "gulls", type: "birds", plane: "back", lanes: [[[-12, 150], [200, 168], [360, 236], [452, 214], [470, -12]], [[520, -12], [430, 232], [330, 262], [180, 160], [-12, 140]]],
      every: [8, 16], group: [1, 2], speed: 55, size: 7, scale: [0.6, 1.0], color: "#f6eed8", behind: [TEAHOUSE, [[452, 60], [800, 60], [800, 300], [452, 300]]] },
    // the relay courier (PEOPLE-21A's runner): along the road's middle, both ways, now and then (ENGINE-21's passer; the
    // painter's two lanes, rows 516 and 508 at the marks), in front of everything on the far side of the road; his area goes with him
    { id: "courier", type: "passer", kind: "courier", path: [[-34, 517], M.courierFrom, M.courierTo, [834, 507]], every: [18, 34], both: true, area: "courier" },
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
    { id: "fuji", name: "Mount Fuji", rect: [150, 64, 300, 238], walkTo: M.view, face: "N", ...lookUse("edo.kurasawa", "fuji") },
    { id: "cloud", name: "cloud", poly: [[185, 101], [196, 93], [219, 83], [243, 78], [266, 76], [301, 81], [324, 89], [335, 95], [335, 100], [312, 103], [289, 108], [266, 110], [243, 109], [219, 105], [196, 101]],
      walkTo: M.view, face: "N", ...lookUse("edo.kurasawa", "cloud"), when: (g) => !is(g, "edo.fujiClear") },
    { id: "bay", name: "the bay", poly: BAY, walkTo: M.view, face: "N", ...lookUse("edo.kurasawa", "bay") },
    { id: "yuishore", name: "the shore of Yui", poly: [[270, 286], [460, 297], [460, 310], [360, 316], [300, 324], [270, 336]], walkTo: M.view, face: "N", ...lookUse("edo.kurasawa", "yuishore") },
    { id: "boats", name: "boats", rect: [338, 306, 160, 50], walkTo: M.view, face: "N", ...lookUse("edo.kurasawa", "boats") },
    { id: "hackberry", name: "hackberry", rect: [449, 61, 344, 195], walkTo: M.mound, face: "N", ...lookUse("edo.kurasawa", "hackberry") },
    { id: "cliffroad", name: "the cliff road", verb: "Go up", poly: [[640, 262], [700, 252], [800, 226], [800, 412], [700, 410], [690, 380]], walkTo: M.climb, face: "E",
      look: each("edo.kurasawa.cliffroad"), use: upTheCliff },
    { id: "teahouse", name: "teahouse", poly: TEAHOUSE, walkTo: M.teahouse, face: "N", ...lookUse("edo.kurasawa", "teahouse") },
    { id: "smoke", name: "smoke", rect: [196, 380, 50, 64], walkTo: [212, 500], face: "N", ...lookUse("edo.kurasawa", "smoke") },
    { id: "signboard", name: "signboard", rect: [279, 384, 24, 90], walkTo: [282, 492], face: "N", ...lookUse("edo.kurasawa", "signboard") },
    { id: "mound", name: "distance mound", rect: [542, 328, 162, 83], walkTo: M.mound, face: "N", look: moundLook, use: each("edo.kurasawa.mound.use") },
    { id: "palanquin", name: "palanquin", rect: [387, 385, 191, 65], walkTo: M.bearers, face: "N", ...lookUse("edo.kurasawa", "palanquin") },
    { id: "trunks", name: "willow trunks", rect: [307, 410, 61, 68], walkTo: M.peddler, face: "N", ...lookUse("edo.kurasawa", "trunks") },
    { id: "bench", name: "bench", rect: [2, 442, 151, 34], walkTo: M.teahouse, face: "N", ...lookUse("edo.kurasawa", "bench") },
    // the road, short of the edges' bands (left: back to Yui; right: up the cliff road), which are its ways out
    { id: "road", name: "the road", verb: "Go up", poly: [[46, 577], [754, 577], [754, 478], [46, 478]], walkTo: [400, 540], face: "E", look: each("edo.kurasawa.road"), use: roadUse },
    // the people (the game draws them; their areas go with them). O-Kuni stands behind her grill: the grill and the shells over her.
    { id: "kuni", name: "O-Kuni", verb: "Talk to", rect: [211, 392, 27, 79], walkTo: [184, 485], face: "E", look: each("edo.kurasawa.kuni"), use: kuniTalk },
    { id: "grill", name: "grill", rect: [177, 435, 74, 48], walkTo: [212, 500], face: "N", ...lookUse("edo.kurasawa", "grill") },
    { id: "shells", name: "turban shells", rect: [190, 439, 47, 11], walkTo: [212, 500], face: "N", look: shellsLook, use: each("edo.kurasawa.shells.use") },
    { id: "sakuji", name: "Sakuji", verb: "Talk to", rect: [432, 382, 27, 80], walkTo: [406, 476], face: "E", look: each("edo.kurasawa.sakuji"), use: bearersTalk },
    { id: "tora", name: "Tora", verb: "Talk to", rect: [456, 386, 28, 84], walkTo: [430, 484], face: "E", look: each("edo.kurasawa.tora"), use: bearersTalk },
    { id: "soshichi", name: "Sōshichi", verb: "Talk to", rect: [360, 395, 31, 91], walkTo: [336, 500], face: "E", look: each("edo.kurasawa.soshichi"), use: soshichiTalk },
    { id: "komuso", name: "komusō", rect: [651, 405, 34, 101], walkTo: [628, 520], face: "E", look: komusoLook, use: komusoUse },
    // the courier: his area is his figure's box while he runs past (the passer moves it), and is not there while he is not
    { id: "courier", name: "courier", rect: [382, 408, 35, 104], walkTo: [400, 540], face: "S", ...lookUse("edo.kurasawa", "courier") },
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
